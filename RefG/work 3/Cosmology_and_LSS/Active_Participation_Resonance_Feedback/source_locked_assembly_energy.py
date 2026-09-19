"""SOURCE_LOCKED_EQUILIBRIUM_ENERGY_RESPONSE_V1 -- stdout-only audit.

Primary exact claim: the unchanged fixed-Q scalar stationary action obeys
de*(g)/dg=-G(g)/g, where G is its positive gradient plus exterior-tail
response energy. This introduces no new dynamics into that action.

Separate AdditiveReplicaToy: N identical additive copies of its ordinary
sector, fixed Q per copy, restricted to a symmetric common profile, at
fixed alpha0=.001. Its functional is N F+S/alpha0, equivalently
M(N)=N e*(alpha0*N). Real N is a formal continuation parameter; integer
N=1,2,3 labels replicas, not measured particle number or coalescence.
Incoherence alone does not derive this additive rule for overlapping
excitations of the original nonlinear single field. Cross interactions
are excluded by the stated toy definition, not shown to vanish.

Frozen numerical gates and all allowed points are in the companion
source_locked_assembly_energy.md, saved before numerical execution.
No new EOS, current, radiation model, damping or pressure floor is added.
Global concavity, nonsymmetric stability and actual assembly dynamics
are not claimed. Positive Hessians refer to the sampled constrained
radial common-profile class only. Full RefG and singularities stay open.

Run with python -B. --symbolic-only skips every numerical solve.
Imported existing files are hash-pinned and never edited or written.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True

import numpy as np
import scipy
from scipy.integrate import simpson
import sympy as sp

HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "source_locked_assembly_energy.md"
CANDIDATE = HERE / "common_scale_finite_source_candidate.py"
CANDIDATE_SHA256 = "6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8"
ALPHA0 = .001
RESOLUTIONS = ((40., 1e-7, 8001), (60., 1e-9, 16001))
BASE_N = tuple(1.+.25*k for k in range(9))
PROBES = (.02, .01)
ALL_N = tuple(sorted(set(BASE_N + tuple(2.+sign*h for h in PROBES for sign in (-1, 1)))))
HESSIAN_CELLS = {40.: (240, 480), 60.: (360, 720)}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(value, reference):
    return abs(float(value)-float(reference))/max(abs(float(reference)), 1e-30)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def symbolic_checks():
    checks = {}

    def exact(name, expression):
        residual = sp.simplify(sp.expand(expression))
        checks[name] = {"passed": residual == 0, "residual": str(residual)}

    z, g, N, alpha, zdot = sp.symbols("z g N alpha dz_dg", positive=True)
    F, S = sp.Function("F"), sp.Function("S")
    energy = F(z)+S(z)/g
    scale_energy = S(z)/g
    exact("partial_coupling_derivative",
          sp.diff(energy, g)+scale_energy/g)
    on_shell_derivative = (sp.diff(energy, g)+sp.diff(energy, z)*zdot).subs(
        sp.diff(F(z), z), -sp.diff(S(z), z)/g)
    exact("fixed_charge_stationary_envelope",
          on_shell_derivative+scale_energy/g)
    toy = N*F(z)+S(z)/alpha
    exact("replica_energy_reduction", toy-N*energy.subs(g, alpha*N))
    exact("replica_on_shell_stationarity",
          sp.diff(toy, z)-N*sp.diff(energy, z).subs(g, alpha*N))
    e, G = sp.Function("e"), sp.Function("G")
    mass = N*e(alpha*N)
    eprime_at, esecond_at = sp.symbols("e_prime_at_alphaN e_second_at_alphaN")

    def evaluated_derivatives(expression):
        # SymPy uses a bound Dummy inside Subs after applying the chain
        # rule. Replace that actual node, rather than a nonmatching
        # positive-symbol placeholder for its bound variable.
        return expression.replace(
            lambda node: isinstance(node, sp.Subs)
            and isinstance(node.expr, sp.Derivative)
            and node.expr.expr.func == e,
            lambda node: eprime_at if node.expr.derivative_count == 1 else esecond_at,
        )

    first = evaluated_derivatives(sp.diff(mass, N))
    exact("replica_first_derivative_is_ordinary_energy",
          first.subs(eprime_at, -G(alpha*N)/(alpha*N))
          -(e(alpha*N)-G(alpha*N)))
    average_prime = evaluated_derivatives(sp.diff(mass/N, N))
    exact("average_energy_decreases",
          average_prime.subs(eprime_at, -G(alpha*N)/(alpha*N))+G(alpha*N)/N)
    second = evaluated_derivatives(sp.diff(mass, N, 2))
    exact("replica_second_derivative",
          second-(2*alpha*eprime_at+alpha**2*N*esecond_at))
    e1, eN, G1, GN = sp.symbols("e1 eN G1 GN", real=True)
    ordinary_loss = N*((e1-G1)-(eN-GN))
    binding = N*(e1-eN)
    response_change = N*(GN-G1)
    exact("stationary_energy_ledger", ordinary_loss-binding-response_change)
    H, Fz = sp.symbols("H Fz", real=True)
    stationary_branch_response = -Fz/H
    exact("conditional_radial_concavity",
          Fz*stationary_branch_response+Fz**2/H)
    flux = sp.symbols("minus_four_pi_r_squared_u_prime", real=True)
    exact("aggregate_gauss_normalization", flux/alpha-N*flux/(alpha*N))
    f, u, omega = sp.symbols("f u omega", real=True)
    V = f*f/2-f**4/4+f**6/24
    source = 2*sp.exp(4*u)*omega**2*f*f-2*sp.exp(2*u)*V
    exact("zero_ordinary_state_has_zero_source", source.subs(f, 0))
    exact("ordinary_potential_positive_certificate",
          V-f*f/8-f*f*(f*f-3)**2/24)
    return checks


def closure_flags(exact_passed, numerical_passed):
    return {
        "stationary_single_field_envelope_identity": exact_passed,
        "finite_weak_replica_energy_evidence": exact_passed and numerical_passed,
        "new_single_field_dynamics_introduced": False,
        "replica_additivity_derived_from_incoherence": False,
        "full_RefG_closure": False,
        "stored_tension_EOS_derived": False,
        "singularity_resolution": False,
        "time_assembly_simulated": False,
        "replica_N_identified_as_particle_count": False,
        "universal_stability": False,
        "global_branch_concavity_proved": False,
        "observational_pass": False,
    }


def numerical_run(model):
    if not CONTRACT.exists():
        raise RuntimeError("Frozen companion contract must exist before numerical execution")
    if digest(model.W58) != model.W58_SHA256:
        raise RuntimeError("Frozen W58 dependency changed")
    original = load(model.W58, "assembly_w58_no_write")
    reference = original.solve_profile(.8, radius=80., tolerance=1e-8)
    rr = np.linspace(0., 80., 24001)
    ff, fp = reference.sol(rr)
    charge = float(4*np.pi*.8*simpson(rr**2*ff**2, x=rr))
    energy0 = float(4*np.pi*simpson(
        rr**2*(fp*fp/2+.8**2*ff*ff/2+model.potential(ff)), x=rr))
    checks, cases, summaries, hessians = {}, [], [], []
    solutions = {}

    def gate(name, condition, observed, threshold):
        checks[name] = {"passed": bool(condition), "observed": observed, "threshold": threshold}

    for radius, tolerance, points in RESOLUTIONS:
        by_n, previous = {}, None
        for copies in ALL_N:
            effective_g = ALPHA0*copies
            solution = model.coupled_profile(reference, charge, effective_g,
                                             radius, tolerance, previous)
            previous = solution
            if copies == 2.:
                solutions[radius] = solution
            row = model.observables(solution, effective_g, radius, points, charge)
            response = row["foundation_gradient_energy"]
            ordinary = row["energy"]-response
            # Exact integral for the leading flat, quadratic tail ansatz
            # f(r)=f(R)R/r exp[-k(r-R)]. This is an estimate, not an enclosure
            # of the full curved nonlinear tail.
            decay = math.sqrt(max(1-row["omega"]**2, 1e-30))
            matter_tail = (2*np.pi*row["endpoint_amplitude"]**2*radius**2
                           *(1/decay+1/radius))
            row.update(
                N=copies, external_alpha0=ALPHA0, effective_g=effective_g,
                ordinary_energy_per_copy=ordinary,
                aggregate_energy=copies*row["energy"],
                aggregate_gauss_mass=copies*row["mass_gauss"],
                aggregate_ordinary_energy=copies*ordinary,
                aggregate_response_energy=copies*response,
                leading_flat_matter_tail_estimate=matter_tail,
                matter_tail_estimate_relative=matter_tail/max(row["energy"], 1e-30),
                tolerance=tolerance,
            )
            cases.append(row)
            by_n[round(copies, 6)] = row
            prefix = f"R{radius:g}_N{copies:.2f}"
            gate(prefix+"_charge", row["charge_relative_residual"] < 1e-7,
                 row["charge_relative_residual"], "<1e-7")
            mass_virial = max(row[key] for key in
                              ("mass_energy_relative", "mass_source_relative", "virial_relative"))
            gate(prefix+"_mass_source_virial", mass_virial < 2e-5, mass_virial, "<2e-5")
            gate(prefix+"_weak", row["maximum_abs_u"] < .1, row["maximum_abs_u"], "<.1")
            gate(prefix+"_collocation", row["collocation_max_rms_residual"] <= 2*tolerance,
                 row["collocation_max_rms_residual"], f"<={2*tolerance}")
            gate(prefix+"_localized_nodeless_nonzero",
                 row["minimum_f"] >= -1e-9 and row["central_amplitude"] > .1
                 and 0 < row["omega"] < 1,
                 [row["minimum_f"], row["central_amplitude"], row["omega"]],
                 "f_min>=-1e-9; f(0)>.1; 0<Omega<1")
            gate(prefix+"_matter_tail_estimate",
                 row["matter_tail_estimate_relative"] < 1e-12,
                 row["matter_tail_estimate_relative"], "leading-flat estimate/E <1e-12")

        one, centre, three = by_n[1.], by_n[2.], by_n[3.]
        for row in by_n.values():
            copies = row["N"]
            loss = copies*(one["ordinary_energy_per_copy"]-row["ordinary_energy_per_copy"])
            binding = copies*(one["energy"]-row["energy"])
            response_change = copies*(row["foundation_gradient_energy"]
                                      -one["foundation_gradient_energy"])
            ledger_residual = loss-binding-response_change
            row.update(ordinary_loss_from_isolated_gravitating_copies=loss,
                       binding_from_isolated_gravitating_copies=binding,
                       response_energy_change_from_isolated_copies=response_change,
                       stationary_ledger_residual=ledger_residual)
            gate(f"R{radius:g}_N{copies:.2f}_ledger",
                 abs(ledger_residual) < 1e-12*max(abs(loss), abs(binding), 1.),
                 ledger_residual, "algebraic ledger within 1e-12 of its energy scale")

        derivative_rows = []
        for h in PROBES:
            minus, plus = by_n[round(2.-h, 6)], by_n[round(2.+h, 6)]
            dm = (plus["aggregate_energy"]-minus["aggregate_energy"])/(2*h)
            ddm = (plus["aggregate_energy"]-2*centre["aggregate_energy"]
                   +minus["aggregate_energy"])/(h*h)
            de = (plus["energy"]-minus["energy"])/(2*ALPHA0*h)
            expected_de = -centre["foundation_gradient_energy"]/centre["effective_g"]
            derivative_rows.append({
                "h_in_N": h, "first_mass_derivative": dm,
                "expected_ordinary_energy_per_copy": centre["ordinary_energy_per_copy"],
                "first_derivative_relative_error": relative(dm, centre["ordinary_energy_per_copy"]),
                "second_mass_derivative": ddm,
                "single_field_energy_derivative_g": de,
                "expected_single_field_envelope": expected_de,
                "single_field_envelope_relative_error": relative(de, expected_de),
            })
            gate(f"R{radius:g}_h{h}_Mprime",
                 relative(dm, centre["ordinary_energy_per_copy"]) < 2e-5,
                 relative(dm, centre["ordinary_energy_per_copy"]), "<2e-5")
            gate(f"R{radius:g}_h{h}_single_envelope",
                 relative(de, expected_de) < 2e-5, relative(de, expected_de), "<2e-5")
            gate(f"R{radius:g}_h{h}_negative_second", ddm < 0, ddm, "<0 sampled only")
        dcoarse, dfine = derivative_rows
        first_refine = relative(dcoarse["first_mass_derivative"], dfine["first_mass_derivative"])
        envelope_refine = relative(dcoarse["single_field_energy_derivative_g"],
                                   dfine["single_field_energy_derivative_g"])
        second_refine = relative(dcoarse["second_mass_derivative"], dfine["second_mass_derivative"])
        gate(f"R{radius:g}_first_derivative_refines", first_refine < 2e-5, first_refine, "<2e-5")
        gate(f"R{radius:g}_single_field_envelope_refines", envelope_refine < 2e-5,
             envelope_refine, "<2e-5")
        gate(f"R{radius:g}_second_derivative_resolved", second_refine < .01, second_refine, "<.01")

        base = [by_n[n] for n in BASE_N]
        evalues = np.array([item["energy"] for item in base])
        mvalues = np.array([item["aggregate_energy"] for item in base])
        gate(f"R{radius:g}_per_copy_decreases", np.all(np.diff(evalues) < 0),
             np.diff(evalues).tolist(), "all successive e(N) differences<0")
        gate(f"R{radius:g}_total_increases", np.all(np.diff(mvalues) > 0),
             np.diff(mvalues).tolist(), "all successive M(N) differences>0")
        increments = [centre["aggregate_energy"]-one["aggregate_energy"],
                      three["aggregate_energy"]-centre["aggregate_energy"]]
        gate(f"R{radius:g}_integer_increments_decrease", increments[0] > increments[1] > 0,
             increments, "M2-M1 > M3-M2 >0")

        nn = np.array(BASE_N)
        integrand = np.array([item["foundation_gradient_energy"]/item["N"] for item in base])
        no_tail_integrand = np.array([
            (item["foundation_gradient_energy"]-item["foundation_exterior_tail_energy"])/item["N"]
            for item in base])
        target = one["energy"]-three["energy"]
        integral_fine = float(simpson(integrand, x=nn))
        integral_coarse = float(simpson(integrand[::2], x=nn[::2]))
        integral_without_tail = float(simpson(no_tail_integrand, x=nn))
        integral_error_fine = relative(integral_fine, target)
        integral_error_coarse = relative(integral_coarse, target)
        gate(f"R{radius:g}_binding_integral_fine", integral_error_fine < 2e-5,
             integral_error_fine, "<2e-5")
        gate(f"R{radius:g}_binding_integral_coarse", integral_error_coarse < 2e-5,
             integral_error_coarse, "<2e-5")
        integral_refine = relative(integral_coarse, integral_fine)
        gate(f"R{radius:g}_binding_integral_refines", integral_refine < 2e-5,
             integral_refine, "<2e-5")
        wrong_envelope = centre["ordinary_energy_per_copy"]+centre["foundation_exterior_tail_energy"]
        wrong_envelope_error = relative(dfine["first_mass_derivative"], wrong_envelope)
        wrong_binding_error = relative(integral_without_tail, target)
        gate(f"R{radius:g}_negative_control_no_tail_envelope",
             wrong_envelope_error >= 2e-5, wrong_envelope_error, "wrong formula must fail 2e-5")
        gate(f"R{radius:g}_negative_control_no_tail_binding",
             wrong_binding_error >= 2e-5, wrong_binding_error, "wrong integral must fail 2e-5")
        summaries.append({
            "radius": radius, "derivatives_at_N2": derivative_rows,
            "first_derivative_h_halving_change": first_refine,
            "single_field_envelope_h_halving_change": envelope_refine,
            "second_derivative_h_halving_change": second_refine,
            "integer_increment_M2_minus_M1": increments[0],
            "integer_increment_M3_minus_M2": increments[1],
            "binding_integral_target_e1_minus_e3": target,
            "binding_integral_step_half": integral_coarse,
            "binding_integral_step_quarter": integral_fine,
            "binding_integral_h_halving_change": integral_refine,
            "binding_integral_without_tail": integral_without_tail,
            "no_tail_binding_relative_error": wrong_binding_error,
            "no_tail_envelope_relative_error": wrong_envelope_error,
        })

        for cells in HESSIAN_CELLS[radius]:
            hh = model.radial_hessian(solutions[radius], ALPHA0*2, radius, cells, charge)
            hh.update(N=2., effective_g=2*ALPHA0,
                      scope="per-copy Hessian; same sign as aggregate common-profile Hessian, no nonsymmetric replica modes")
            hessians.append(hh)
            gate(f"R{radius:g}_cells{cells}_radial_hessian",
                 hh["positive_sampled_fixed_charge_hessian"]
                 and max(hh["eigen_equation_absolute_residuals"]) < 1e-7,
                 [hh["smallest_two_eigenvalues"], hh["eigen_equation_absolute_residuals"]],
                 "sampled minimum>0; eigen-equation residual<1e-7")

    d2_values = [item["derivatives_at_N2"][-1]["second_mass_derivative"] for item in summaries]
    second_cross_radius = relative(d2_values[0], d2_values[1])
    gate("second_mass_derivative_cross_radius", second_cross_radius < .01,
         second_cross_radius, "<.01")
    coarse_rows = {round(item["N"], 6): item for item in cases if item["radius"] == 40.}
    fine_rows = {round(item["N"], 6): item for item in cases if item["radius"] == 60.}
    changes = {str(n): {key: relative(coarse_rows[n][key], fine_rows[n][key])
                        for key in ("energy", "mass_gauss", "omega", "central_p",
                                    "foundation_gradient_energy", "ordinary_energy_per_copy",
                                    "charge_rms_radius")}
               for n in coarse_rows}
    maximum_cross_radius_change = max(value for row in changes.values() for value in row.values())
    gate("maximum_cross_radius_observable_change", maximum_cross_radius_change < 2e-5,
         maximum_cross_radius_change, "<2e-5")
    primary_table = []
    for copies in (1., 2., 3.):
        row = fine_rows[copies]
        primary_table.append({
            "N": copies,
            "total_mass_energy": row["aggregate_energy"],
            "total_mass_normalized_to_N1": row["aggregate_energy"]/fine_rows[1.]["aggregate_energy"],
            "energy_per_copy": row["energy"],
            "ordinary_energy_per_copy": row["ordinary_energy_per_copy"],
            "response_energy_per_copy": row["foundation_gradient_energy"],
            "total_ordinary_energy": row["aggregate_ordinary_energy"],
            "total_response_energy": row["aggregate_response_energy"],
            "binding_from_N_isolated_gravitating_copies": row["binding_from_isolated_gravitating_copies"],
            "ordinary_loss_from_N_isolated_gravitating_copies": row["ordinary_loss_from_isolated_gravitating_copies"],
            "response_energy_change_from_N_isolated_gravitating_copies": row["response_energy_change_from_isolated_copies"],
            "central_p": row["central_p"],
            "coordinate_charge_rms_radius": row["charge_rms_radius"],
        })
    return {
        "reference_charge_per_replica": charge, "uncoupled_reference_energy": energy0,
        "external_alpha0": ALPHA0, "base_N_grid": list(BASE_N),
        "all_solved_N": list(ALL_N), "cases": cases, "summaries": summaries,
        "primary_table_fine_N1_N2_N3": primary_table,
        "cross_radius_changes": changes, "maximum_cross_radius_change": maximum_cross_radius_change,
        "second_derivative_cross_radius_change": second_cross_radius,
        "hessians": hessians, "checks": checks,
        "matter_tail_note": "leading flat quadratic-profile estimate, not a rigorous bound on the full curved tail",
        "ledger_note": "energy decomposition identity; independent tests are envelope finite differences, binding quadrature and boundary/source mass",
    }


def run(symbolic_only=False):
    if digest(CANDIDATE) != CANDIDATE_SHA256:
        raise RuntimeError("Frozen existing scalar candidate dependency changed")
    exact = symbolic_checks()
    model = load(CANDIDATE, "assembly_existing_candidate_no_write")
    if digest(model.W58) != model.W58_SHA256:
        raise RuntimeError("Frozen W58 dependency changed")
    numerical = None if symbolic_only else numerical_run(model)
    exact_failed = [name for name, row in exact.items() if not row["passed"]]
    numeric_failed = ([] if numerical is None else
                      [name for name, row in numerical["checks"].items() if not row["passed"]])
    unchanged = (digest(CANDIDATE) == CANDIDATE_SHA256
                 and digest(model.W58) == model.W58_SHA256)
    exact_passed = not exact_failed and unchanged
    passed = exact_passed and not numeric_failed
    return {
        "claim_id": "SOURCE_LOCKED_EQUILIBRIUM_ENERGY_RESPONSE_V1",
        "passed": passed, "symbolic_only": symbolic_only,
        "symbolic_checks": exact, "symbolic_check_count": len(exact),
        "numerical_check_count": 0 if numerical is None else len(numerical["checks"]),
        "failed_symbolic": exact_failed, "failed_numerical": numeric_failed,
        "unchanged_dependencies": unchanged,
        "identities": [
            "e*(g)=F(z*(g);Q)+S(z*(g))/g; G=S/g>=0; de*/dg=−G/g on shell at fixed Q",
            "AdditiveReplicaToy: M(N)=N e*(alpha0 N), F_N=N F, G_N=N G",
            "d(M/N)/dN=−G/N; M'=F>0; M''=alpha0(2e'+g e'')",
            "If the relevant constrained Hessian is positive, M''=−grad(F)^T H_N^-1 grad(F)<=0",
            "N(F1−FN)=N(e1−eN)+N(GN−G1)",
            "e1−e3=integral_1^3 G(alpha0 N)/N dN",
        ],
        "scope": {
            "primary": "exact existing-action stationary energy response",
            "replicas": "separately declared additive-copy toy; common profile and Q per copy",
            "real_N": "formal differentiation only; not fractional actual particle counts",
            "assembly": "stationary energy differences, no formation/outgoing-energy dynamics",
            "concavity": "sampled finite differences and conditional constrained-Hessian theorem only",
        },
        "closure_flags": closure_flags(exact_passed, passed and numerical is not None),
        "numerical": numerical,
        "provenance": {
            "self_sha256": digest(Path(__file__)),
            "contract_sha256": digest(CONTRACT) if CONTRACT.exists() else None,
            "candidate_sha256": digest(CANDIDATE),
            "W58_sha256": digest(model.W58),
            "python": sys.version.split()[0], "numpy": np.__version__,
            "scipy": scipy.__version__, "sympy": sp.__version__,
        },
        "writes_files": False,
    }


if __name__ == "__main__":
    try:
        if any(arg != "--symbolic-only" for arg in sys.argv[1:]):
            raise ValueError("Only --symbolic-only is supported")
        report = run(symbolic_only="--symbolic-only" in sys.argv[1:])
    except Exception as exc:
        report = {
            "claim_id": "SOURCE_LOCKED_EQUILIBRIUM_ENERGY_RESPONSE_V1", "passed": False,
            "exception_type": type(exc).__name__, "exception": str(exc),
            "closure_flags": closure_flags(False, False), "writes_files": False,
        }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["passed"] else 1)
