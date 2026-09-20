"""Nonuniform foundation/matter test of the already postulated rate-limited action.

Contract: FOUNDATION_RATE_LIMITED_RADIAL_V1 in foundation_oscillon_minimum_closure.md.
Run python -X utf8 -B this_file.py [--output results.json].
No strong-field evolution or new constitutive law is introduced here.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

sys.dont_write_bytecode = True
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from threadpoolctl import threadpool_limits

HERE = Path(__file__).resolve().parent
CLAIM = "FOUNDATION_RATE_LIMITED_RADIAL_V1"
ALPHA, END, SAMPLE, EPSILON = .003, 24., .12, .05
PINS = {
    "common_scale_time_response.py":
        "c49f1163a1983ec8057eb51978959bfa49b12b3ec65e914f64f2966d3c785a3c",
    "foundation_rate_limited_dynamics.py":
        "93447a6a656535846f95e762dbe726a06218b0f4b004724d6cf1288f9a3122b6",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = load("inherited_common_scale_radial", HERE / "common_scale_time_response.py")


class Radial(old.RadialHamiltonian):
    def __init__(self, dr, b, radius=60., scale=1.):
        self.b, self.scale, self.background_u = b, scale, -math.log(scale)
        self.cells = int(round(radius/dr))
        self.dr = radius*scale/self.cells
        self.radius = radius*scale
        faces = np.arange(self.cells+1)*self.dr
        self.r = (np.arange(self.cells)+.5)*self.dr
        self.volume = np.diff(faces**3)/3
        self.weight = 4*np.pi*self.volume
        self.conductance = faces[1:-1]**2/self.dr
        half = self.radius**2/(self.dr/2)
        self.boundary_u = half*self.radius/(half+self.radius)
        self.boundary_matter = half

    def parts(self, state):
        u, a, c, pu, pa, pc = state[:6]
        p = np.exp(-u)
        z = ALPHA*p**3*pu/self.b
        gamma = np.sqrt(1+z*z)
        q = a*a+c*c
        V = self.potential(q)
        kinetic = self.b**2/(ALPHA*p*p)*z*z/(gamma+1)
        force = self.b**2/(ALPHA*p*p)*z*z*(gamma+3)/(gamma*(gamma+1))
        source = 2*p**4*(pa*pa+pc*pc)-2*V/(p*p)
        return p, z, gamma, q, V, kinetic, force, source

    def rhs(self, state):
        u, a, c, pu, pa, pc = state[:6]
        p, z, gamma, q, V, kinetic, force, source = self.parts(state)
        potential_slope = 1-q+q*q/4
        return np.vstack((
            ALPHA*p**4*pu/gamma, p**4*pa, p**4*pc,
            self.laplace(u-self.background_u, self.boundary_u)/ALPHA+force+source,
            self.laplace(a, self.boundary_matter)-a*potential_slope/p**2,
            self.laplace(c, self.boundary_matter)-c*potential_slope/p**2, p,
        ))

    def energy(self, state):
        """Independent scalar discrete Hamiltonian; supports complex-step."""
        u, a, c, pu, pa, pc = state[:6]
        p = np.exp(-u)
        z = ALPHA*p**3*pu/self.b
        q = a*a+c*c
        kinetic = self.b**2/(ALPHA*p*p)*z*z/(np.sqrt(1+z*z)+1)
        local = kinetic+p**4*(pa*pa+pc*pc)/2+(q/2-q*q/4+q*q*q/24)/p**2
        return (np.dot(self.weight, local)+4*np.pi*(
            self.gradient_energy(u-self.background_u, self.boundary_u)/ALPHA
            +self.gradient_energy(a, self.boundary_matter)
            +self.gradient_energy(c, self.boundary_matter)))

    def observe(self, state, t, p_initial):
        u, a, c, pu, pa, pc, tau = state
        ut, at, ct, put, pat, pct, _ = self.rhs(state)
        p, z, gamma, q, V, kinetic, force, source = self.parts(state)
        lap = self.laplace(u-self.background_u, self.boundary_u)
        H_u = float(np.dot(self.weight, kinetic)+4*np.pi*
                    self.gradient_energy(u-self.background_u, self.boundary_u)/ALPHA)
        H_m = float(np.dot(self.weight, p**4*(pa*pa+pc*pc)/2+V/p**2)
                    +4*np.pi*(self.gradient_energy(a, self.boundary_matter)
                              +self.gradient_energy(c, self.boundary_matter)))
        charge_density = a*pc-c*pa
        charge = float(np.dot(self.weight, charge_density))
        radius_squared = float(np.dot(self.weight*self.r**2, charge_density)/charge)
        if radius_squared <= 0:
            raise FloatingPointError("Charge radius is undefined")
        charge_rate = float(np.dot(self.weight, at*pc+a*pct-ct*pa-c*pat))
        exchange = float(np.dot(self.weight, ut*source))
        energy_u_rate = float(np.dot(self.weight, ut*(put-force))+4*np.pi*
            self.gradient_energy_rate(u-self.background_u, ut, self.boundary_u)/ALPHA)
        energy_m_rate = float(np.dot(self.weight,
            p**4*(pa*pat+pc*pct)-2*p**4*(pa*pa+pc*pc)*ut
            +2*V*ut/p**2+(1-q+q*q/4)*(a*at+c*ct)/p**2)
            +4*np.pi*(self.gradient_energy_rate(a, at, self.boundary_matter)
                       +self.gradient_energy_rate(c, ct, self.boundary_matter)))
        utt = -ut*ut*(1+3/gamma**2)+ALPHA*p**4*put/gamma**3
        ptt = p*(ut*ut-utt)
        terms = np.vstack((
            -p**5*lap/gamma**3,
            -ALPHA*p**5*source/gamma**3,
            p*ut*ut+self.b**2*p**3*z*z*(gamma**2+gamma+2)/((gamma+1)*gamma**3),
        ))
        # Centre readouts are even extrapolations, not extra evolved cells.
        centre = lambda x: float((9*x[0]-x[1])/8)
        # Only the core phase is read: field zeros in the outer tail do not
        # define a phase clock.
        if np.any(q[:2] <= 1e-20):
            raise FloatingPointError("Core phase clock is undefined at a field zero")
        core_freq = centre((a[:2]*ct[:2]-c[:2]*at[:2])/q[:2])
        centre_p = math.exp(-centre(u))
        lower = p_initial/(1+self.b*p_initial*t)
        tau_lower = np.log1p(self.b*p_initial*t)/self.b
        own_lower = p_initial*np.exp(-self.b*tau)
        gradient = np.diff(u)/self.dr
        q_gradient = (np.diff(a)/self.dr)**2+(np.diff(c)/self.dr)**2
        energy_gradient_face = gradient**2/(2*ALPHA)+q_gradient/2
        return {
            "time": t, "central_p": centre_p, "central_tau": centre(tau),
            "central_p_t": -centre_p*centre(ut),
            "central_coordinate_frequency": core_freq,
            "central_local_frequency": core_freq/centre_p,
            "charge_radius": math.sqrt(radius_squared),
            "mean_p_by_charge": float(np.dot(self.weight, p*charge_density)/charge),
            "charge": charge, "charge_dot": charge_rate,
            "negative_charge_fraction": float(np.dot(self.weight, np.maximum(-charge_density, 0))/abs(charge)),
            "energy": H_u+H_m, "energy_foundation": H_u, "energy_matter": H_m,
            "exchange_to_foundation": exchange,
            "foundation_energy_rate": energy_u_rate, "matter_energy_rate": energy_m_rate,
            "exchange_residual": max(abs(energy_u_rate-exchange), abs(energy_m_rate+exchange))/(1+abs(exchange)),
            "minimum_p": float(np.min(p)), "maximum_p": float(np.max(p)),
            "max_rate_fraction": float(np.max(np.abs(z/gamma))),
            "maximum_gradient_u": float(np.max(np.abs(gradient))),
            "maximum_local_energy": float(np.max(kinetic+p**4*(pa*pa+pc*pc)/2+V/p**2)),
            "maximum_face_gradient_energy": float(np.max(energy_gradient_face)),
            "acceleration_budget_residual": float(np.max(np.abs(ptt-np.sum(terms, axis=0))/(1+np.abs(ptt)))),
            "first_cell_acceleration": float(ptt[0]),
            "first_cell_acceleration_terms": terms[:, 0].tolist(),
            "external_pressure_bound_margin": float(np.min(p-lower)),
            "proper_clock_integral_margin": float(np.min(tau-tau_lower)),
            "own_clock_pressure_bound_margin": float(np.min(p-own_lower)),
        }


def initial(model, solution, compressed):
    x = model.r/model.scale
    f_eq, _, u_eq, _, _ = solution.sol(x)
    omega = float(solution.p[0])
    zero = np.zeros_like(x)
    base_pc = np.exp(4*u_eq)*omega*f_eq
    base_charge = float(np.dot(model.weight/model.scale**3, f_eq*base_pc))
    correction = 1.
    if compressed:
        z = np.clip((x-8)/4, 0, 1)
        delta = EPSILON*(1-10*z**3+15*z**4-6*z**5)
        f, _, mapped_u, _, _ = solution.sol(x*np.exp(delta))
        u = mapped_u+delta
        pc = np.exp(4*u)*omega*np.exp(-delta)*f
        correction = base_charge/float(np.dot(model.weight/model.scale**3, f*pc))
        pc *= correction
    else:
        f, u, pc = f_eq, u_eq, base_pc
    state = np.vstack((u+model.background_u, f, zero, zero, zero, pc/model.scale**3, zero))
    return state, {"phase_momentum_correction": correction,
                   "initial_foundation_momentum": 0., "reference_charge": base_charge,
                   "common_scale_shift": EPSILON if compressed else 0.}


def evolve(dr, b, solution, compressed, started, radius=60., scale=1., dt_factor=.2,
           method="rk4", rtol=1e-10, formation=False):
    model = Radial(dr, b, radius, scale)
    y, info = initial(model, solution, compressed)
    if formation:
        # The retained W58 profile at zero gravitational coupling supplies
        # localized matter. No deficit/gradient/kinetic energy is preloaded.
        if scale != 1. or compressed:
            raise ValueError("Formation contract is uncompressed with scale=1")
        f = solution.sol(model.r)[0]
        y[:] = 0.
        y[1] = f
        y[5] = .8*f
        info = {"initial_foundation_energy": 0., "initial_foundation_momentum": 0.,
                "initial_pressure_factor": 1., "phase_momentum_correction": 1.,
                "zero_coupling_seed_omega": .8}
    p_initial = np.exp(-y[0])
    dt = dt_factor*dr/scale
    steps = int(round(END/(dt_factor*dr)))
    sample_steps = int(round(SAMPLE/(dt_factor*dr)))
    history = []
    if method == "dop853":
        # Integrate normalized canonical variables so the error controller
        # uses the same tolerances under the exact operational similarity.
        normalization = np.ones_like(y)
        normalization[3:6] = scale**-3
        offset = np.zeros_like(y)
        offset[0] = model.background_u
        def ode(t, normalized):
            if time.monotonic()-started > 300:
                raise TimeoutError("Declared 300-second runtime exceeded")
            state = normalized.reshape(y.shape)*normalization+offset
            return (model.rhs(state)/normalization).ravel()
        with threadpool_limits(limits=1):
            solved = solve_ivp(
                ode, (0., END/scale), ((y-offset)/normalization).ravel(),
                method="DOP853", t_eval=np.linspace(0., END/scale, 201),
                rtol=rtol, atol=rtol/100, max_step=dt)
        if not solved.success:
            raise RuntimeError(solved.message)
        history = [
            model.observe(solved.y[:, j].reshape(y.shape)*normalization+offset,
                          float(t), p_initial)
            for j, t in enumerate(solved.t)]
        steps = -1  # RK4 loop skipped; exactly the same diagnostics follow.
    for k in range(steps+1):
        if k % sample_steps == 0:
            history.append(model.observe(y, k*dt, p_initial))
            if time.monotonic()-started > 300:
                raise TimeoutError("Declared 300-second runtime exceeded")
        if k == steps:
            break
        k1 = model.rhs(y)
        k2 = model.rhs(y+dt*k1/2)
        k3 = model.rhs(y+dt*k2/2)
        k4 = model.rhs(y+dt*k3)
        y += dt*(k1+2*k2+2*k3+k4)/6
        if not np.all(np.isfinite(y)):
            raise FloatingPointError("Nonfinite radial state")
    E0, Q0 = history[0]["energy"], history[0]["charge"]
    maxkey = lambda key: max(row[key] for row in history)
    summary = {
        "dr": model.dr, "b": b, "radius": model.radius, "scale": scale, "dt": dt,
        "method": method,
        "rtol": rtol if method == "dop853" else None, "formation": formation,
        "compressed": compressed, "initial": info,
        "energy_relative_drift": max(abs(row["energy"]/E0-1) for row in history),
        "charge_relative_drift": max(abs(row["charge"]/Q0-1) for row in history),
        "maximum_charge_rhs_relative": max(abs(row["charge_dot"]/Q0) for row in history),
        "minimum_p": min(row["minimum_p"] for row in history),
        "maximum_rate_fraction": maxkey("max_rate_fraction"),
        "maximum_gradient_u": maxkey("maximum_gradient_u"),
        "maximum_local_energy": maxkey("maximum_local_energy"),
        "maximum_face_gradient_energy": maxkey("maximum_face_gradient_energy"),
        "maximum_exchange_residual": maxkey("exchange_residual"),
        "maximum_acceleration_budget_residual": maxkey("acceleration_budget_residual"),
        "bound_minimum_margins": {key: min(row[key] for row in history) for key in (
            "external_pressure_bound_margin", "proper_clock_integral_margin",
            "own_clock_pressure_bound_margin")},
        "checkpoints": [history[i] for i in (0, 50, 100, 150, 200)],
    }
    checks = {
        "energy": summary["energy_relative_drift"] < 2e-6,
        "charge": summary["charge_relative_drift"] < 2e-7,
        "exchange": summary["maximum_exchange_residual"] < 1e-9,
        "acceleration_budget": summary["maximum_acceleration_budget_residual"] < 1e-9,
        "positive_p": summary["minimum_p"] > 0,
        "proper_rate_cap": summary["maximum_rate_fraction"] < 1,
        "two_clock_bounds": min(summary["bound_minimum_margins"].values()) >= -1e-7,
    }
    summary["checks"] = checks
    print(json.dumps({"finished_run": {key: summary[key] for key in (
        "dr", "b", "radius", "scale", "compressed", "energy_relative_drift",
        "charge_relative_drift", "maximum_rate_fraction")}, "checks": checks}), flush=True)
    return summary, history


def hamiltonian_check():
    model = Radial(.6, .01, radius=3., scale=.7)
    rng = np.random.default_rng(20260920)
    y = rng.uniform(-.2, .2, (7, model.cells))
    y[0] += model.background_u
    y[3] *= 200
    y[4:6] += .7
    flow = model.rhs(y)
    grad = np.zeros((6, model.cells))
    for i in range(6):
        for j in range(model.cells):
            point = y.astype(complex)
            point[i, j] += 1j*1e-28
            grad[i, j] = np.imag(model.energy(point))/1e-28/model.weight[j]
    expected = np.vstack((grad[3:], -grad[:3], np.exp(-y[0])))
    error = float(np.max(np.abs(flow-expected)/(1+np.abs(expected))))
    # Negative control: a source-free update is detectably not this Hamiltonian.
    _, _, _, _, _, _, _, source = model.parts(y)
    missing = flow.copy()
    missing[3] -= source
    missing_error = float(np.max(np.abs(missing-expected)/(1+np.abs(expected))))
    zero = np.zeros_like(y)
    zero[0] = model.background_u
    vacuum_flow = model.rhs(zero)
    vacuum_residual = float(np.max(np.abs(vacuum_flow[:6])))
    return {"passed": bool(error < 1e-9 and missing_error > 1e-3 and vacuum_residual == 0),
            "maximum_scaled_residual": error,
            "omitted_matter_source_negative_control": missing_error,
            "uniform_zero_energy_vacuum_residual": vacuum_residual,
            "nonzero_outer_traces_tested": True, "random_seed": 20260920}


def compare(first, second, key):
    a = np.array([row[key] for row in first])
    b = np.array([row[key] for row in second])
    absolute = float(np.max(np.abs(a-b)))
    return {"max_absolute": absolute, "relative": absolute/max(float(np.max(np.abs(b))), 1e-30)}


def scaling_comparison(reference, scaled):
    powers = {"central_p": 1, "minimum_p": 1, "charge_radius": 1,
              "central_coordinate_frequency": 1, "energy": 1, "energy_matter": 1,
              "energy_foundation": 1, "charge": 0, "central_tau": 0,
              "central_local_frequency": 0, "exchange_to_foundation": 2,
              "time": -1, "central_p_t": 2, "max_rate_fraction": 0,
              "maximum_gradient_u": -1}
    result = {}
    for key, power in powers.items():
        a = np.array([row[key] for row in reference])
        restored = np.array([row[key] for row in scaled])/.1**power
        result[key] = {"power": power, "normalized_history_error":
            float(np.max(np.abs(a-restored)))/max(1., float(np.max(np.abs(a))))}
    return result


def complete_from(path):
    """Reuse accepted physics/grid runs; resolve only the outstanding precision
    check and add a separately declared matter-generated deficit control."""
    started = time.monotonic()
    expected_base = "ac63382b79d68f206b3655b0fd353a98ff1fa4fe29f42467cb7657b2f8793d84"
    if digest(path) != expected_base:
        raise ValueError("The registered base result changed")
    result = json.loads(path.read_text(encoding="utf-8"))
    if result["sources"] != PINS or any(digest(HERE/name) != value for name, value in PINS.items()):
        raise ValueError("Inherited model changed")
    if not all(value for key, value in result["checks"].items()
               if key != "common_scale_evolving_solution"):
        raise ValueError("Only the scaling precision check may be outstanding")
    solution, _ = old.equilibrium()
    reference, ref_history = evolve(.06, .01, solution, True, started,
                                    method="dop853", rtol=1e-12)
    scaled, scaled_history = evolve(.06, .01, solution, True, started,
                                   scale=.1, method="dop853", rtol=1e-12)
    result["previous_scaling_check"] = result["common_scale_evolution"]
    result["common_scale_evolution"] = scaling_comparison(ref_history, scaled_history)
    result["checks"]["common_scale_evolving_solution"] = max(
        x["normalized_history_error"] for x in result["common_scale_evolution"].values()) < 1e-8
    result["checks"]["refined_scaling_integrity"] = all(
        all(row["checks"].values()) for row in (reference, scaled))
    result["runs"].extend((reference, scaled))
    result["refined_scaling_histories"] = {"reference": ref_history, "scaled": scaled_history}
    # This source preparation is the same uncharged complex-field reference
    # used to seed the existing equilibrium, not a new matter model.
    candidate = old.load_module("source_for_formation", old.CANDIDATE)
    w58 = old.load_module("w58_for_formation", candidate.W58)
    bare = w58.solve_profile(.8, radius=80, tolerance=1e-8)
    # Adapt only the initial_state interface; its values are replaced by the
    # formation branch immediately afterwards.
    class InitialProfile:
        p = np.array([.8])
        @staticmethod
        def sol(x):
            f, fp = bare.sol(x)
            zero = np.zeros_like(x)
            return np.vstack((f, fp, zero, zero, zero))
    seed = InitialProfile()
    formation_runs, formation_histories = [], {}
    initial_signs = []
    for dr in (.12, .06, .03):
        run_summary, history = evolve(dr, .01, seed, False, started, method="dop853",
                                     formation=True)
        formation_runs.append(run_summary)
        formation_histories[dr] = history
        model = Radial(dr, .01)
        f = bare.sol(model.r)[0]
        q = f*f
        # Exact signed source S=q(7/25+q/2-q²/12), at p=1 and omega=4/5.
        source = q*(7/25+q/2-q*q/12)
        signs = {"dr": dr, "maximum_q": float(np.max(q)),
                 "source_coefficient_minimum": float(np.min(7/25+q/2-q*q/12)),
                 "initial_central_acceleration": history[0]["first_cell_acceleration"],
                 "initial_source_formula_residual":
                     abs(history[0]["first_cell_acceleration"]+ALPHA*source[0]),
                 "foundation_energy_initial": history[0]["energy_foundation"],
                 "foundation_energy_final": history[-1]["energy_foundation"],
                 "minimum_p": min(row["minimum_p"] for row in history),
                 "maximum_gradient": max(row["maximum_gradient_u"] for row in history)}
        initial_signs.append(signs)
    comparison = {}
    for key in ("central_p", "charge_radius"):
        coarse = compare(formation_histories[.12], formation_histories[.06], key)
        fine = compare(formation_histories[.06], formation_histories[.03], key)
        comparison[key] = {"coarse_medium": coarse, "medium_fine": fine}
        result["checks"]["formation_grid_"+key] = (
            fine["relative"] < .003 and (fine["max_absolute"] < coarse["max_absolute"]
                                        or max(fine["max_absolute"], coarse["max_absolute"]) < 1e-9))
    result["checks"]["formation_integrity"] = all(all(x["checks"].values()) for x in formation_runs)
    result["checks"]["matter_generates_deficit_and_gradient"] = all(
        x["source_coefficient_minimum"] > 0 and x["initial_central_acceleration"] < 0
        and x["initial_source_formula_residual"] < 1e-12
        and x["foundation_energy_initial"] == 0 and x["foundation_energy_final"] > 0
        and x["minimum_p"] < .999 and x["maximum_gradient"] > 1e-5 for x in initial_signs)
    result["formation_control"] = {"initial_signs": initial_signs, "runs": formation_runs,
                                    "refinement": comparison,
                                    "fine_history": formation_histories[.03]}
    passed = all(result["checks"].values())
    result["status"] = "PASS_DECLARED_RADIAL_TEST" if passed else "FAIL"
    result["new_verified_flags"] = {
        "selected_nonuniform_response_observables": passed,
        "common_scale_nonlinear_evolution": bool(
            result["checks"]["common_scale_evolving_solution"] and
            result["checks"]["refined_scaling_integrity"] and
            result["checks"]["nonlinear_response_active"]),
        "matter_generated_deficit_control": bool(result["checks"]["formation_integrity"] and
                                                result["checks"]["matter_generates_deficit_and_gradient"])}
    result["reused_results"] = {"file": str(path), "sha256": expected_base,
                               "original_status": "FAIL",
                               "outstanding_gate": "common_scale_evolving_solution",
                               "original_verifier_sha256": result["self_sha256"],
                               "original_wall_seconds": result["wall_seconds"]}
    result["self_sha256"] = digest(Path(__file__))
    result["ledger_sha256_at_run"] = digest(HERE/"foundation_oscillon_minimum_closure.md")
    result["completion_wall_seconds"] = time.monotonic()-started
    result["wall_seconds"] += result["completion_wall_seconds"]
    return result


def run(method="rk4"):
    started = time.monotonic()
    ledger = HERE / "foundation_oscillon_minimum_closure.md"
    if CLAIM not in ledger.read_text(encoding="utf-8-sig"):
        raise ValueError("Declared contract missing")
    provenance = {name: digest(HERE/name) for name in PINS}
    if provenance != PINS:
        raise RuntimeError("Inherited implementation changed")
    independent = hamiltonian_check()
    if not independent["passed"]:
        raise AssertionError(independent)
    solution, charge = old.equilibrium()
    summaries, histories = [], {}
    for dr in (.12, .06, .03):
        for b in (.01, 1.):
            for compressed in (False, True):
                result, history = evolve(dr, b, solution, compressed, started, method=method)
                summaries.append(result)
                histories[(dr, b, compressed)] = history
    checks = {"independent_discrete_H": independent["passed"],
              "all_evolution_gates": all(all(row["checks"].values()) for row in summaries)}
    refinement = {}
    for b in (.01, 1.):
        for compressed in (False, True):
            for key in ("central_p", "charge_radius"):
                coarse = compare(histories[(.12, b, compressed)], histories[(.06, b, compressed)], key)
                fine = compare(histories[(.06, b, compressed)], histories[(.03, b, compressed)], key)
                name = f"b{b}_compressed{compressed}_{key}"
                refinement[name] = {"coarse_medium": coarse, "medium_fine": fine}
                checks[name] = (fine["relative"] < .003 and
                    (fine["max_absolute"] < coarse["max_absolute"] or
                     max(fine["max_absolute"], coarse["max_absolute"]) < 1e-9))
    fine = histories[(.03, .01, True)]
    half, half_history = evolve(.03, .01, solution, True, started, dt_factor=.1, method=method)
    summaries.append(half)
    # Re-solve the same source with a more remote boundary. Previous profile
    # is only the initial BVP guess; its extrapolation is not accepted as data.
    candidate = old.load_module("source_for_extended_boundary", old.CANDIDATE)
    far_solution = candidate.coupled_profile(solution, charge, ALPHA, 90., 3e-8, previous=solution)
    far, far_history = evolve(.03, .01, far_solution, True, started, radius=90., method=method)
    summaries.append(far)
    diagnostics = {}
    for name, history in (("half_timestep", half_history), ("far_boundary", far_history)):
        diagnostics[name] = {key: compare(fine, history, key) for key in ("central_p", "charge_radius")}
        checks[name] = all(item["relative"] < .003 for item in diagnostics[name].values())
    scaled, scaled_history = evolve(.06, .01, solution, True, started, scale=.1, method=method)
    summaries.append(scaled)
    scaling = {}
    # Corresponding local times, not the same distant-coordinate instant.
    powers = {"central_p": 1, "minimum_p": 1, "charge_radius": 1,
              "central_coordinate_frequency": 1, "energy": 1, "energy_matter": 1,
              "energy_foundation": 1, "charge": 0, "central_tau": 0,
              "central_local_frequency": 0, "exchange_to_foundation": 2,
              "time": -1, "central_p_t": 2, "max_rate_fraction": 0,
              "maximum_gradient_u": -1}
    reference = histories[(.06, .01, True)]
    for key, power in powers.items():
        a = np.array([row[key] for row in reference])
        restored = np.array([row[key] for row in scaled_history])/.1**power
        error = float(np.max(np.abs(a-restored)))/max(1., float(np.max(np.abs(a))))
        scaling[key] = {"power": power, "normalized_history_error": error}
    checks["common_scale_evolving_solution"] = max(x["normalized_history_error"] for x in scaling.values()) < 1e-8
    checks["extra_runs_evolution_gates"] = all(all(x["checks"].values()) for x in (half, far, scaled))
    checks["nonlinear_response_active"] = max(
        row["maximum_rate_fraction"] for row in summaries if row["compressed"] and row["b"] == .01) > .3
    initial_errors = {}
    for dr in (.12, .06, .03):
        first, second = histories[(dr, .01, True)][0], histories[(dr, 1., True)][0]
        initial_errors[str(dr)] = {key: abs(first[key]-second[key]) for key in
                                  ("energy", "charge", "first_cell_acceleration")}
    checks["same_initial_energy_charge_acceleration"] = max(
        item for row in initial_errors.values() for item in row.values()) < 1e-10
    # Motion is reported as measured; returning to equilibrium is not a gate.
    responses = {}
    for b in (.01, 1.):
        equilibrium, compressed = histories[(.03, b, False)], histories[(.03, b, True)]
        dp = np.array([x["central_p"]-y["central_p"] for x, y in zip(compressed, equilibrium)])
        dpt = np.array([x["central_p_t"]-y["central_p_t"] for x, y in zip(compressed, equilibrium)])
        dr = np.array([x["charge_radius"]-y["charge_radius"] for x, y in zip(compressed, equilibrium)])
        responses[str(b)] = {
            "central_p_response_initial_final_min_max": [float(dp[0]), float(dp[-1]), float(np.min(dp)), float(np.max(dp))],
            "radius_response_initial_final_min_max": [float(dr[0]), float(dr[-1]), float(np.min(dr)), float(np.max(dr))],
            "pressure_restoring_motion_sampled": bool(np.any((dp*dp[0]>0) & (dp*dpt < -1e-9))),
            "final_relaxation_claimed": False,
        }
    passed = all(checks.values())
    return {
        "claim_id": CLAIM, "status": "PASS_DECLARED_RADIAL_TEST" if passed else "FAIL",
        "numerical_method": method,
        "checks": checks, "independent_hamiltonian": independent,
        "runs": summaries, "refinement": refinement, "extra_comparisons": diagnostics,
        "common_scale_evolution": scaling, "initial_b_comparison": initial_errors,
        "measured_response": responses, "fine_compressed_history": fine,
        "sources": provenance, "self_sha256": digest(Path(__file__)),
        "ledger_sha256_at_run": digest(ledger),
        "software": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "wall_seconds": time.monotonic()-started,
        "inherited_postulate": "Finite proper foundation response rate b; no new law added.",
        "new_verified_flags": {"finite_nonuniform_conservative_response": passed,
                               "common_scale_nonlinear_evolution": bool(
                                   checks["common_scale_evolving_solution"] and
                                   checks["all_evolution_gates"] and
                                   checks["extra_runs_evolution_gates"] and
                                   checks["nonlinear_response_active"])},
        "closure_flags": {key: False for key in ("full_theory", "background_tension_EOS",
            "b_observationally_calibrated", "global_PDE_regularity", "curvature_bounded",
            "geodesic_completeness", "singularity_resolution", "observational_pass")},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--method", choices=("rk4", "dop853"), default="rk4")
    parser.add_argument("--complete-from", type=Path)
    args = parser.parse_args()
    result = complete_from(args.complete_from) if args.complete_from else run(args.method)
    encoded = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        destination = args.output.resolve()
        if destination.parent != HERE:
            raise ValueError("Results must stay in the authorized working package")
        destination.write_text(encoded+"\n", encoding="utf-8")
        print(json.dumps({key: result[key] for key in
                          ("status", "checks", "wall_seconds", "measured_response")}, indent=2))
        print("Results: "+str(destination))
    else:
        print(encoded)
    if result["status"] != "PASS_DECLARED_RADIAL_TEST":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
