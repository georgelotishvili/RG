"""W86: one finite localized W84 feedback experiment; stdout only."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import platform
import re
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve()
ROOT = HERE.parents[4]
CONTRACT = HERE.with_name("w3_86_localized_node_link_feedback_contract.md")
CONTRACT_SHA = "d39071b760d27a2882f3a442f0b69578905d0d157130e114c2ef92c9f323b070"
W84_PATH = HERE.parent.parent / "W3-84_Minimal_Node_Link_Candidate" / "w3_84_node_link.py"
N, T, ALPHA = 48, 8.0, np.pi / 6
TIMES = np.arange(401, dtype=float) / 50
H0 = 2 * (1 - np.cos(ALPHA))
QBOUND = np.sqrt(2 * H0)
W84 = None


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_scalar(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"Unsupported JSON type: {type(value).__name__}")


def initial(size=N):
    state = np.zeros((4, size))
    state[0, size // 2] = ALPHA
    state[2] = 1.0
    return state


def production_force(position, frozen=False, mutation=None):
    force = W84.forces(position)
    if mutation == "reverse_current":
        force[0] *= -1
    elif mutation == "omit_opening_force":
        force[1] = -position[1]
    elif mutation == "freeze_phase_coupling":
        current = np.sin(np.roll(position[0], -1) - position[0])
        force[0] = current - np.roll(current, 1)
    if frozen:
        force[1] = 0
    return force


def link_power(state):
    theta, q, n, P = state
    delta = np.roll(theta, -1) - theta
    _, kp, _ = W84.coupling(q)
    return float(-np.sum(P * kp * (1 - np.cos(delta))))


def cumulative_quadratic(values, dt):
    """Full Simpson panels plus their exact quadratic half-panel integral."""
    out = np.zeros(len(values))
    if (len(values) - 1) % 2:
        raise ValueError("Endpoint must complete a two-step panel")
    for k in range(0, len(values) - 2, 2):
        a, b, c = values[k:k + 3]
        out[k + 1] = out[k] + dt * (5*a + 8*b - c) / 12
        out[k + 2] = out[k] + dt * (a + 4*b + c) / 3
    return out


def evolve(size, dt, frozen=False):
    print(f"W86 Verlet N={size} dt={dt} frozen={frozen}", file=sys.stderr, flush=True)
    state = initial(size)
    position, momentum = state[:2], state[2:]
    steps = int(round(T/dt))
    stride = int(round(0.02/dt))
    if abs(steps*dt-T) > 1e-12 or abs(stride*dt-0.02) > 1e-12:
        raise ValueError("Nonintegral fixed schedule")
    saved = np.empty((len(TIMES), 4, size))
    powers = np.empty(steps+1)
    energy_error = charge_error = bound_ratio = 0.0
    min_n = min_d = float("inf")
    finite = True

    def monitor(k):
        nonlocal energy_error, charge_error, min_n, min_d, bound_ratio, finite
        h = W84.energy(position, momentum)
        lengths = np.exp(position[1])
        finite = finite and bool(np.isfinite(state).all() and np.isfinite(h)
                                 and np.isfinite(lengths).all())
        energy_error = max(energy_error, abs(h-H0)/H0)
        charge_error = max(charge_error, abs(float(np.sum(momentum[0]))-size)/size)
        min_n = min(min_n, float(momentum[0].min()))
        min_d = min(min_d, float(lengths.min()))
        bound_ratio = max(bound_ratio,
                          float(max(np.max(np.abs(momentum[0]-1)),
                                    np.max(np.abs(momentum[1])),
                                    np.max(np.abs(position[1])))/QBOUND))
        powers[k] = 0.0 if frozen else link_power(state)
        if k % stride == 0:
            saved[k//stride] = state

    monitor(0)
    for k in range(1, steps+1):
        momentum += 0.5*dt*production_force(position, frozen)
        position += dt*W84.velocities(momentum)
        momentum += 0.5*dt*production_force(position, frozen)
        monitor(k)
    work = cumulative_quadratic(powers, dt)[::stride]
    mechanics = np.sum((saved[:, 1]**2+saved[:, 3]**2)/2, axis=1)
    work_error = float(np.max(np.abs(mechanics-mechanics[0]-work))/H0)
    summary = {
        "N":size, "dt":dt, "frozen_links":frozen,
        "max_relative_energy_error":energy_error,
        "max_relative_charge_error":charge_error,
        "min_n":min_n, "min_d":min_d, "max_energy_bound_ratio":bound_ratio,
        "finite_domain":finite and min_n>0 and min_d>0 and bound_ratio<=1.0001,
        "max_work_residual_over_H0":work_error,
    }
    return {"states":saved, "work":work, "summary":summary}


def independent_rhs(t, flat, frozen=False):
    """Separate direct Hamiltonian implementation, not W84 production calls."""
    state = flat.reshape(4, -1)
    theta, q, n, P = state
    delta = np.concatenate((theta[1:]-theta[:-1], [theta[0]-theta[-1]]))
    length = np.exp(q)
    stiffness = np.exp(1-q-length)
    flow = stiffness*np.sin(delta)
    n_rate = flow-np.concatenate(([flow[-1]], flow[:-1]))
    P_rate = -q+(1+length)*stiffness*(1-np.cos(delta))
    if frozen:
        return np.array([n-1, np.zeros_like(P), n_rate, np.zeros_like(P)]).ravel()
    return np.array([n-1, P, n_rate, P_rate]).ravel()


def independent_energy(states):
    theta, q, n, P = np.moveaxis(states, 1, 0)
    delta = np.concatenate((theta[:, 1:]-theta[:, :-1],
                            (theta[:, :1]-theta[:, -1:])), axis=1)
    coupling = np.exp(1-q-np.exp(q))
    return np.sum(0.5*((n-1)**2+P**2+q**2)+coupling*(1-np.cos(delta)), axis=1)


def dop853(frozen=False):
    print(f"W86 independent DOP853 frozen={frozen}", file=sys.stderr, flush=True)
    solution = solve_ivp(lambda t, y: independent_rhs(t, y, frozen),
                         (0, T), initial().ravel(), method="DOP853",
                         t_eval=TIMES, rtol=1e-11, atol=1e-13, max_step=0.02)
    if not solution.success or len(solution.t) != len(TIMES):
        raise RuntimeError(solution.message)
    states = solution.y.T.reshape(len(TIMES), 4, N)
    energies = independent_energy(states)
    lengths = np.exp(states[:, 1])
    bound = max(float(np.max(np.abs(states[:, 2]-1))),
                float(np.max(np.abs(states[:, 3]))),
                float(np.max(np.abs(states[:, 1]))))/QBOUND
    summary = {
        "method":"DOP853", "N":N, "frozen_links":frozen,
        "max_relative_energy_error":float(np.max(np.abs(energies-H0))/H0),
        "max_relative_charge_error":float(np.max(np.abs(states[:, 2].sum(axis=1)-N))/N),
        "min_n":float(states[:, 2].min()), "min_d":float(lengths.min()),
        "max_energy_bound_ratio":float(bound),
        "finite_domain":bool(np.isfinite(states).all() and np.isfinite(energies).all()
                            and np.isfinite(lengths).all()
                            and states[:, 2].min()>0 and lengths.min()>0
                            and bound<=1.0001),
        "health_sampling":"all fixed output states; adaptive internal stages are not stored",
    }
    return {"states":states, "nfev":solution.nfev, "summary":summary,
            "independent_relative_energy_error":summary["max_relative_energy_error"]}


def offshell_checks():
    size = 12
    i = np.arange(size)
    position = np.array([.12*np.cos(.37*i)+.04*np.sin(.81*i),
                         .08*np.sin(.41*i)+.03*np.cos(.67*i)])
    momentum = np.array([1+.11*np.sin(.23*i), .06*np.cos(.29*i)])
    numerical = np.empty_like(position)
    h = 1e-6
    for j in range(2*size):
        plus, minus = position.copy(), position.copy()
        plus.flat[j] += h
        minus.flat[j] -= h
        numerical.flat[j] = -(W84.energy(plus, momentum)-W84.energy(minus, momentum))/(2*h)
    normalizer = max(1.0, float(np.max(np.abs(numerical))))

    def evaluate(mutation=None):
        theta, q = position
        n, P = momentum
        delta = np.roll(theta, -1)-theta
        K, Kp, _ = W84.coupling(q)
        current = K*np.sin(delta)
        if mutation == "reverse_current":
            current *= -1
        if mutation == "freeze_phase_coupling":
            current = np.sin(delta)
        force = production_force(position, mutation=mutation)
        v = n-1
        # Differentiate the actual full bond energy, not an imposed flux identity.
        bond_rate = P*force[1]+q*P+Kp*P*(1-np.cos(delta))
        bond_rate += K*np.sin(delta)*(np.roll(v, -1)-v)
        node_rate = v*force[0]+(bond_rate+np.roll(bond_rate, 1))/2
        flux = -current*(v+np.roll(v, -1))/2
        if mutation == "reverse_energy_flux":
            flux *= -1
        energy_residual = float(np.max(np.abs(node_rate+flux-np.roll(flux, 1))))
        force_residual = float(np.max(np.abs(force-numerical))/normalizer)
        charge_residual = float(abs(np.sum(force[0])))
        return {"force_gradient_residual":force_residual,
                "local_energy_residual":energy_residual,
                "global_charge_residual":charge_residual,
                "passed":force_residual<2e-7 and energy_residual<1e-12
                         and charge_residual<1e-12}

    baseline = evaluate()
    mutations = {name:evaluate(name) for name in
                 ("reverse_current", "omit_opening_force",
                  "freeze_phase_coupling", "reverse_energy_flux")}
    seed = initial()
    force = W84.forces(seed[:2])
    expected = np.zeros_like(force)
    c = N//2
    expected[0, c] = -2*np.sin(ALPHA)
    expected[0, [c-1, c+1]] = np.sin(ALPHA)
    expected[1, [c-1, c]] = 2*(1-np.cos(ALPHA))
    seed_error = max(abs(W84.energy(seed[:2], seed[2:])-H0),
                     abs(float(np.sum(seed[2]))-N),
                     float(np.max(np.abs(force-expected))))
    # Quadrature must integrate every prefix of a quadratic, including odd ones.
    test_t = np.arange(9)/10
    quad_error = float(np.max(np.abs(
        cumulative_quadratic(2+3*test_t+test_t**2, 0.1)
        -(2*test_t+1.5*test_t**2+test_t**3/3))))
    return {"baseline":baseline, "mutations":mutations,
            "initial_exact_regression_residual":seed_error,
            "quadrature_quadratic_prefix_residual":quad_error,
            "passed":baseline["passed"] and seed_error<1e-12 and quad_error<1e-12,
            "mutations_detected":all(not row["passed"] for row in mutations.values())}


def histories(states):
    theta, q, n, P = np.moveaxis(states, 1, 0)
    size = theta.shape[1]
    delta = np.roll(theta, -1, axis=1)-theta
    K, Kp, Kpp = W84.coupling(q)
    potential = K*(1-np.cos(delta))
    link = (P**2+q**2)/2
    phase_node = (n-1)**2/2+(potential+np.roll(potential, 1, axis=1))/2
    link_node = (link+np.roll(link, 1, axis=1))/2
    total_node = phase_node+link_node
    labels = np.arange(size)-size//2
    centre = np.abs(labels)<=2
    outer = np.abs(labels)>=20
    phase = phase_node.sum(axis=1)
    mechanics = link_node.sum(axis=1)
    total = total_node.sum(axis=1)
    A = K*np.cos(delta)
    b = Kp*np.sin(delta)
    D = 1+Kpp*(1-np.cos(delta))
    return {
        "phase_energy_fraction":phase/H0,
        "link_energy_fraction":mechanics/H0,
        "central_phase_fraction":phase_node[:, centre].sum(axis=1)/H0,
        "central_link_fraction":link_node[:, centre].sum(axis=1)/H0,
        "central_total_fraction":total_node[:, centre].sum(axis=1)/H0,
        "phase_label_RMS":np.sqrt((phase_node*labels**2).sum(axis=1)/phase),
        "total_label_RMS":np.sqrt((total_node*labels**2).sum(axis=1)/total),
        "max_d":np.exp(q).max(axis=1),
        "min_d":np.exp(q).min(axis=1),
        "min_instantaneous_schur":(A-b*b/D).min(axis=1),
        "outer_energy_fraction":total_node[:, outer].sum(axis=1)/H0,
    }


def state_error(a, b):
    return float(np.max(np.abs(a-b))/ALPHA)


def metric_error(metric, pairs):
    return max(float(np.max(np.abs(a[metric]-b[metric]))) for a, b in pairs)


def main():
    global W84
    content = CONTRACT.read_text(encoding="utf-8")
    pins = {}
    for line in content.splitlines():
        match = re.fullmatch(r"- (.+): ([a-f0-9]{64})", line)
        if match:
            path, expected = match.groups()
            pins[path] = {"expected":expected, "actual":sha(ROOT/path)}
    contract_hash = sha(CONTRACT)
    files = sorted(p.name for p in HERE.parent.iterdir())
    provenance_ok = (contract_hash==CONTRACT_SHA and len(pins)==7
                     and all(row["expected"]==row["actual"] for row in pins.values())
                     and files==sorted([HERE.name, CONTRACT.name]))
    report = {
        "stage":"W3-86-v1.0",
        "claim":"W3_86_LOCALIZED_RECIPROCAL_NODE_LINK_FEEDBACK",
        "type":"FINITE_NUMERICAL_EVIDENCE_IN_EXISTING_NEW_GRAPH_HYPOTHESIS",
        "provenance":{"source_sha256":sha(HERE), "contract_sha256":contract_hash,
                      "implementation_note":"The first production attempt completed integrations but JSON serialization rejected numpy.bool_. Scalar serialization was corrected and DOP853 conservation diagnostics were included in the pre-existing all-run gate. Physics, schedules and budgets unchanged.",
                      "pins":pins, "exact_two_files":files,
                      "versions":{"Python":platform.python_version(),
                                  "NumPy":np.__version__, "SciPy":scipy.__version__}},
        "scope":{key:False for key in (
            "oscillon_identified", "microscopic_RefG_law_derived", "Einstein_source_derived",
            "horizon_formed", "singularity_resolved", "asymptotic_stability",
            "observational_pass", "active_theory_changed", "intuitive_files_changed")},
    }
    if not provenance_ok:
        report.update(status="UNRESOLVED", failed_gates=["provenance"])
        return report
    spec = importlib.util.spec_from_file_location("w84_inherited", W84_PATH)
    W84 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(W84)
    algebra = offshell_checks()
    report["force_flux_and_controls"] = algebra
    if not algebra["passed"] or not algebra["mutations_detected"]:
        report.update(status="UNRESOLVED", failed_gates=["force_flux_or_mutations"])
        return report

    runs = [evolve(N, dt) for dt in (.004, .002, .001)]
    frozen = [evolve(N, dt, True) for dt in (.002, .001)]
    wide = evolve(96, .001)
    independent = dop853()
    independent_frozen = dop853(True)
    coarse, medium, fine = runs
    fm, ff = frozen
    block = wide["states"][:, :, 24:72]
    errors = {
        "full_coarse_medium":state_error(coarse["states"], medium["states"]),
        "full_medium_fine":state_error(medium["states"], fine["states"]),
        "frozen_medium_fine":state_error(fm["states"], ff["states"]),
        "full_fine_DOP853":state_error(fine["states"], independent["states"]),
        "frozen_fine_DOP853":state_error(ff["states"], independent_frozen["states"]),
        "N48_N96":state_error(fine["states"], block),
    }
    hs = [histories(r["states"]) for r in runs]
    hfrozen = [histories(r["states"]) for r in frozen]
    hi = histories(independent["states"])
    hif = histories(independent_frozen["states"])
    # Width/error metrics on the full N96 ring include its tiny exterior tails.
    hw = histories(wide["states"])
    h = hs[-1]
    hcontrol = hfrozen[-1]
    pairs = [(hs[1], h), (hfrozen[0], hcontrol), (h, hi), (hcontrol, hif), (h, hw)]
    width_error = metric_error("phase_label_RMS", pairs)
    central_error = metric_error("central_total_fraction", pairs)
    all_summaries = [r["summary"] for r in runs+frozen+[wide]]
    all_summaries += [independent["summary"], independent_frozen["summary"]]
    work_error = max(r["summary"]["max_work_residual_over_H0"] for r in runs+[wide])
    energy_error = max(s["max_relative_energy_error"] for s in all_summaries)
    e_state = max(value for key, value in errors.items() if key!="full_coarse_medium")
    state_threshold = 10*max(e_state, 1e-8)
    work_threshold = 10*max(work_error, energy_error, 1e-8)
    difference = np.abs(fine["states"][:, [0, 2]]-ff["states"][:, [0, 2]])/ALPHA
    response = float(np.max(difference))
    dilation = float(np.max(h["max_d"])-1)
    exchanged = float(np.max(h["link_energy_fraction"]))
    width_delta = float(h["phase_label_RMS"][-1]-hcontrol["phase_label_RMS"][-1])
    width_threshold = 10*max(width_error, 1e-8)
    centre_final = float(h["central_total_fraction"][-1])
    centre_threshold = 10*max(central_error, 1e-8)
    width_outcome = ("wider" if width_delta>width_threshold else
                     "narrower" if width_delta<-width_threshold else "unresolved")
    retention = ("majority redistributed outside central five labels"
                 if centre_final<.5-centre_threshold else
                 "majority retained within this finite interval"
                 if centre_final>.5+centre_threshold else "undecided")
    local_feedback = (response>state_threshold and dilation>state_threshold
                      and exchanged>work_threshold)

    flags = {
        "provenance":provenance_ok,
        "force_and_flux_checks":algebra["passed"],
        "finite_domain":all(s["finite_domain"] for s in all_summaries),
        "energy_charge_balance":all(s["max_relative_energy_error"]<2e-5
                                   and s["max_relative_charge_error"]<1e-11
                                   for s in all_summaries),
        "link_work_balance":work_error<2e-5,
        "timestep_refinement":errors["full_medium_fine"]<2e-5
            and (errors["full_medium_fine"]<1e-9
                 or errors["full_medium_fine"]<=.4*errors["full_coarse_medium"])
            and errors["frozen_medium_fine"]<2e-5,
        "independent_integrator":errors["full_fine_DOP853"]<2e-5
            and errors["frozen_fine_DOP853"]<2e-5,
        "boundary_control":errors["N48_N96"]<1e-6
            and float(np.max(h["outer_energy_fraction"]))<1e-6,
        "mutation_controls":algebra["mutations_detected"],
    }
    # Rehash protected inputs at exit; a concurrent change invalidates provenance.
    end_pins = {path:sha(ROOT/path) for path in pins}
    flags["provenance"] = flags["provenance"] and all(
        end_pins[path]==row["actual"] for path, row in pins.items())
    flags["provenance"] = flags["provenance"] and sha(CONTRACT)==CONTRACT_SHA
    report.update({
        "closure_flags":flags,
        "status":"PASS" if all(flags.values()) else "UNRESOLVED",
        "failed_gates":[key for key, value in flags.items() if not value],
        "initial":{"N":N, "alpha":ALPHA, "H0":H0, "T":T,
                   "node_phase_action":1, "q":0, "P":0},
        "runs":all_summaries,
        "refinement":errors,
        "independent_checks":{
            "full_DOP853_nfev":independent["nfev"],
            "frozen_DOP853_nfev":independent_frozen["nfev"],
            "full_relative_energy_error":independent["independent_relative_energy_error"],
            "frozen_relative_energy_error":independent_frozen["independent_relative_energy_error"]},
        "physical_outcome":{
            "classification_valid":all(flags.values()),
            "resolved_local_reciprocal_feedback":local_feedback if all(flags.values()) else None,
            "max_phase_charge_difference_over_alpha":response,
            "final_phase_charge_difference_over_alpha":float(difference[-1].max()),
            "max_dilation":dilation,
            "endpoint_max_dilation":float(h["max_d"][-1]-1),
            "minimum_bond_length":float(h["min_d"].min()),
            "peak_link_energy_fraction":exchanged,
            "endpoint_link_energy_fraction":float(h["link_energy_fraction"][-1]),
            "endpoint_central_phase_fraction":float(h["central_phase_fraction"][-1]),
            "endpoint_central_link_fraction":float(h["central_link_fraction"][-1]),
            "endpoint_central_total_fraction":centre_final,
            "endpoint_full_phase_RMS":float(h["phase_label_RMS"][-1]),
            "endpoint_frozen_phase_RMS":float(hcontrol["phase_label_RMS"][-1]),
            "phase_width_comparison":width_outcome if all(flags.values()) else "unresolved",
            "phase_width_difference":width_delta, "phase_width_error":width_error,
            "central_fraction_error":central_error,
            "central_retention":retention if all(flags.values()) else "unresolved",
            "minimum_instantaneous_schur":float(h["min_instantaneous_schur"].min()),
            "state_resolution_threshold":state_threshold,
            "work_resolution_threshold":work_threshold,
            "scope":"Finite reciprocal graph response; packet width is not signal speed. Stored link energy is not an oscillon. No asymptotic trapping, relativistic horizon or singularity conclusion."
        },
        "times":TIMES.tolist(),
        "full_history":{key:value.tolist() for key, value in h.items()},
        "frozen_history":{key:value.tolist() for key, value in hcontrol.items()},
        "mechanical_work_over_H0":(fine["work"]/H0).tolist(),
        "exit_protected_hashes":end_pins,
    })
    return report


if __name__ == "__main__":
    try:
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            result = main()
        print(json.dumps(result, allow_nan=False, separators=(",", ":"), default=json_scalar))
        sys.exit(0 if result.get("status")=="PASS" else 1)
    except Exception as exc:
        print(json.dumps({"stage":"W3-86-v1.0", "status":"UNRESOLVED",
                          "failure_type":type(exc).__name__, "failure":str(exc)},
                         allow_nan=False))
        raise
