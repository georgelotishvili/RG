"""PROFILE_RELAXED_RESPONSE_V1: same-action static restoring susceptibility.

The frozen contract is in foundation_oscillon_minimum_closure.md.  A smooth
conjugate load is a constrained-energy diagnostic only.  Both stationary
profiles and the frequency vary at fixed total Q.  No physical source,
friction, pressure floor, strong-field evolution or new action is installed.
Run with python -B; results are stdout-only and imports are hash-pinned.
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
from scipy.integrate import simpson, solve_bvp
import sympy as sp

HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "foundation_oscillon_minimum_closure.md"
CANDIDATE = HERE / "common_scale_finite_source_candidate.py"
CANDIDATE_SHA256 = "6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8"
ALPHA = .003
WIDTH = 3.
LOADS = (-1., -.5, 0., .5, 1.)
PROBES = (1., .5)
RESOLUTIONS = ((40., 1e-7, 8001), (60., 1e-9, 16001))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def relative(value, reference):
    return abs(float(value)-float(reference))/max(abs(float(reference)), 1e-30)


def weight(r):
    return np.exp(-r*r/(2*WIDTH*WIDTH))/((2*np.pi)**1.5*WIDTH**3)


def symbolic_checks():
    checks = {}

    def exact(name, expression):
        residual = sp.simplify(expression)
        checks[name] = {"passed": residual == 0, "residual": str(residual)}

    lam, b, H, zprime = sp.symbols("lambda b H z_prime", real=True)
    chi = -b*b/H
    exact("differentiated_stationarity", (H*zprime+b).subs(zprime, -b/H))
    exact("relaxed_susceptibility", (b*zprime-chi).subs(zprime, -b/H))
    exact("constrained_energy_envelope", (-lam*b*zprime+lam*chi).subs(zprime, -b/H))
    h11, h12, h22 = sp.symbols("h11 h12 h22", real=True)
    matrix = sp.Matrix([[h11, h12], [h12, h22]])
    exact("inverse_hessian_equals_schur_stiffness",
          1/matrix.inv()[0, 0]-(h11-h12*h12/h22))
    T, Gf, Gu, V, integral_w, B = sp.symbols("T G_f G_u V Wnorm B", real=True)
    E = T+Gf+Gu+V
    source = 4*T-2*V
    virial = Gf+Gu+3*V-3*T
    exact("probed_energy_gauss_from_virial",
          E-(source-lam*integral_w)-lam*(integral_w-B)-(virial+lam*B))
    U, ordinary, foundation = sp.symbols("U B C", positive=True)
    q, j0, gf0, v0, gu0 = sp.symbols("Q J0 Gf0 V0 Gu0", positive=True)
    scale = sp.exp(-U)
    # y=x/scale, f=f0(y), u=U*h(y); h=1 throughout a neighborhood
    # of the compact support of f0. d^3x=scale^3 d^3y and each
    # spatial derivative contributes 1/scale. Constants below are
    # unscaled integrals; Gu0 includes 1/(2*alpha).
    j_factor = sp.exp(4*U)*scale**3
    gf_factor = scale**3/scale**2
    v_factor = sp.exp(2*U)*scale**3
    gu_factor = U**2*scale**3/scale**2
    exact("moving_profile_phase_inertia_volume_factor", j_factor-sp.exp(U))
    exact("moving_profile_matter_gradient_factor", gf_factor-scale)
    exact("moving_profile_potential_volume_factor", v_factor-scale)
    exact("moving_profile_foundation_gradient_factor", gu_factor-U**2*scale)
    exact("moving_profile_fixed_charge_frequency", q/(j_factor*j0)-scale*q/j0)
    profile_energy = q*q/(2*j_factor*j0)+gf_factor*gf0+v_factor*v0+gu_factor*gu0
    exact("moving_profile_energy_from_all_transformed_terms",
          profile_energy-scale*(q*q/(2*j0)+gf0+v0+U**2*gu0))
    moving_energy = sp.exp(-U)*(ordinary+foundation*U**2)
    exact("moving_scale_family_energy_derivative",
          sp.diff(moving_energy, U)-sp.exp(-U)*(2*foundation*U-ordinary-foundation*U**2))
    exact("moving_scale_family_large_U_limit", sp.limit(moving_energy, U, sp.oo))
    checks["negative_control_omitted_scale_factor"] = {
        "passed": bool(sp.limit(ordinary+foundation*U**2, U, sp.oo) == sp.oo),
        "correct_limit": "0", "omitted_exp_minus_U_limit": "infinity",
        "scope": "algebra of the explicitly derived moving-profile family in the ledger",
    }
    return checks


def probed_profile(model, baseline, charge, radius, tolerance, lam):
    """Stationarity of E_Q+lambda integral(w*u); same Q and asymptotics."""
    x = np.linspace(0., radius, 1001)
    singular = np.zeros((5, 5))
    singular[1, 1] = singular[3, 3] = -2

    def rhs(r, y, parameter):
        f, fp, u, up = y[:4]
        omega = parameter[0]
        e2 = np.exp(2*u)
        e4 = e2*e2
        return np.vstack((
            fp, e2*model.potential_prime(f)-e4*omega**2*f,
            up, -ALPHA*(2*e4*omega**2*f*f-2*e2*model.potential(f))+ALPHA*lam*weight(r),
            omega*e4*r*r*f*f,
        ))

    def boundary(left, right, parameter):
        k = math.sqrt(max(1-parameter[0]**2, 1e-12))
        return np.array((left[1], left[3], left[4],
                         right[1]+(k+1/radius)*right[0],
                         right[3]+right[2]/radius,
                         right[4]-charge/(4*np.pi)))

    solution = solve_bvp(rhs, boundary, x, baseline.sol(x), p=baseline.p.copy(),
                         S=singular, tol=tolerance, max_nodes=20000, verbose=0)
    if not solution.success:
        raise RuntimeError(f"Probed BVP failed R={radius}, lambda={lam}: {solution.message}")
    return solution


def numerical_run(model):
    original = load(model.W58, "profile_response_w58_no_write")
    reference = original.solve_profile(.8, radius=80., tolerance=1e-8)
    rref = np.linspace(0., 80., 24001)
    fref, _ = reference.sol(rref)
    charge = float(4*np.pi*.8*simpson(rref*rref*fref*fref, x=rref))
    checks, records, summaries = {}, [], []

    def gate(name, condition, observed, threshold):
        checks[name] = {"passed": bool(condition), "observed": observed, "threshold": threshold}

    for radius, tolerance, points in RESOLUTIONS:
        baseline = model.coupled_profile(reference, charge, ALPHA, radius, tolerance)
        r = np.linspace(0., radius, points)
        wr = weight(r)

        def integrate(value):
            return float(4*np.pi*simpson(r*r*value, x=r))

        norm_w = integrate(wr)
        # Maxwell radial Gaussian survival probability, stable even when 1-CDF rounds to zero.
        x = radius/WIDTH
        truncated_weight = math.erfc(x/math.sqrt(2))+math.sqrt(2/math.pi)*x*math.exp(-x*x/2)
        by_load = {}
        for lam in LOADS:
            solution = (baseline if lam == 0. else
                        probed_profile(model, baseline, charge, radius, tolerance, lam))
            row = model.observables(solution, ALPHA, radius, points, charge)
            f, _, u, up, _ = solution.sol(r)
            inertia = integrate(np.exp(4*u)*f*f)
            energy_q = row["energy"]-row["phase_energy"]+charge*charge/(2*inertia)
            average = integrate(wr*u)
            dilation_average = -integrate(wr*r*up)
            gauss_residual = row["mass_gauss"]-(row["mass_source"]-lam*norm_w)
            virial_residual = row["virial"]+lam*dilation_average
            row.update(lambda_probe=lam, tolerance=tolerance, averaged_u=average,
                       geometric_scale=math.exp(-average), phase_inertia=inertia,
                       fixed_charge_energy=energy_q,
                       finite_box_weight_normalization=norm_w,
                       omitted_gaussian_weight=truncated_weight,
                       average_dilation_derivative=dilation_average,
                       probed_gauss_absolute_residual=gauss_residual,
                       probed_virial_absolute_residual=virial_residual,
                       probed_energy_gauss_absolute_residual=(
                           row["energy"]-row["mass_gauss"]-lam*(norm_w-dilation_average)),
                       probed_balance_diagnostics_are_acceptance_gates=False)
            records.append(row)
            by_load[lam] = row
            prefix = f"R{radius:g}_lambda{lam:g}"
            gate(prefix+"_charge", row["charge_relative_residual"] < 1e-7,
                 row["charge_relative_residual"], "<1e-7")
            gate(prefix+"_collocation", row["collocation_max_rms_residual"] <= 2*tolerance,
                 row["collocation_max_rms_residual"], f"<={2*tolerance}")
            gate(prefix+"_localized_nonzero_weak",
                 row["minimum_f"] >= -1e-9 and row["central_amplitude"] > .1
                 and 0 < row["omega"] < 1 and row["maximum_abs_u"] < .1,
                 [row["minimum_f"], row["central_amplitude"], row["omega"], row["maximum_abs_u"]],
                 "f_min>=-1e-9; f0>.1; 0<omega<1; max|u|<.1")
        zero = by_load[0.]
        gate(f"R{radius:g}_baseline_energy_mass", zero["mass_energy_relative"] < 2e-5,
             zero["mass_energy_relative"], "<2e-5")
        responses = []
        for h in PROBES:
            minus, plus = by_load[-h], by_load[h]
            chi = (plus["averaged_u"]-minus["averaged_u"])/(2*h)
            curvature = (plus["fixed_charge_energy"]+minus["fixed_charge_energy"]
                         -2*zero["fixed_charge_energy"])/(h*h)
            curvature_error = abs(curvature/(-chi)-1)
            tail_derivative = ((plus["exterior_u_coefficient"]-minus["exterior_u_coefficient"])
                               /(plus["averaged_u"]-minus["averaged_u"]))
            responses.append({
                "h": h, "susceptibility_chi": chi, "derived_stiffness_K_A": -1/chi,
                "derived_stiffness_K_geometric_scale": -1/(chi*zero["geometric_scale"]**2),
                "symmetric_energy_curvature_in_lambda": curvature,
                "energy_curvature_relative_error": curvature_error,
                "exterior_C_derivative_wrt_average": tail_derivative,
                "adiabatic_foundation_inertia_linear_tail_coefficient": 4*np.pi*tail_derivative**2/ALPHA,
                "central_amplitude_derivative_wrt_average": (
                    (plus["central_amplitude"]-minus["central_amplitude"])
                    /(plus["averaged_u"]-minus["averaged_u"])),
                "charge_radius_derivative_wrt_average": (
                    (plus["charge_rms_radius"]-minus["charge_rms_radius"])
                    /(plus["averaged_u"]-minus["averaged_u"])),
            })
            gate(f"R{radius:g}_h{h}_negative_chi", chi < 0, chi, "<0")
            gate(f"R{radius:g}_h{h}_energy_curvature", curvature_error < .01,
                 curvature_error, "<.01")
            wrong_error = abs(curvature/chi-1)
            gate(f"R{radius:g}_h{h}_negative_control_reversed_sign", wrong_error >= .01,
                 wrong_error, "wrong-sign identity must fail .01")

        coarse, fine = responses
        change_h = relative(coarse["susceptibility_chi"], fine["susceptibility_chi"])
        gate(f"R{radius:g}_susceptibility_h_refinement", change_h < .005, change_h, "<.005")
        # Five-point degree-four interpolation of A(lambda)-A(0); integrate -lambda A'(lambda).
        values = [by_load[lam]["averaged_u"]-zero["averaged_u"] for lam in LOADS]
        polynomial = np.polynomial.Polynomial(np.polynomial.polynomial.polyfit(LOADS, values, 4))
        work_primitive = (-np.polynomial.Polynomial([0., 1.])*polynomial.deriv()).integ()
        work_checks = []
        for lam in (-1., 1.):
            predicted = float(work_primitive(lam)-work_primitive(0.))
            observed = by_load[lam]["fixed_charge_energy"]-zero["fixed_charge_energy"]
            error = relative(predicted, observed)
            work_checks.append({"lambda": lam, "actual_energy_change": observed,
                                "integrated_minus_lambda_dA": predicted, "relative_residual": error})
            gate(f"R{radius:g}_lambda{lam}_integrated_envelope", error < .01, error, "<.01")
        summaries.append({"radius": radius, "responses": responses,
                          "susceptibility_h_refinement": change_h,
                          "integrated_envelope": work_checks,
                          "baseline_averaged_u": zero["averaged_u"],
                          "baseline_geometric_scale": zero["geometric_scale"]})
    for index, h in enumerate(PROBES):
        cross_r = relative(summaries[0]["responses"][index]["susceptibility_chi"],
                           summaries[1]["responses"][index]["susceptibility_chi"])
        gate(f"h{h}_susceptibility_radius_refinement", cross_r < .005, cross_r, "<.005")
    return {"fixed_charge": charge, "alpha": ALPHA, "gaussian_width": WIDTH,
            "records": records, "summaries": summaries, "checks": checks}


def run(symbolic_only=False):
    if not CONTRACT.exists() or "PROFILE_RELAXED_RESPONSE_V1" not in CONTRACT.read_text(encoding="utf-8"):
        raise RuntimeError("Frozen response contract is missing")
    if digest(CANDIDATE) != CANDIDATE_SHA256:
        raise RuntimeError("Existing scalar candidate dependency changed")
    model = load(CANDIDATE, "profile_response_candidate_no_write")
    if digest(model.W58) != model.W58_SHA256:
        raise RuntimeError("Existing W58 dependency changed")
    exact = symbolic_checks()
    numerical = None if symbolic_only else numerical_run(model)
    exact_pass = all(row["passed"] for row in exact.values())
    numeric_pass = numerical is not None and all(row["passed"] for row in numerical["checks"].values())
    unchanged = digest(CANDIDATE) == CANDIDATE_SHA256 and digest(model.W58) == model.W58_SHA256
    return {
        "claim_id": "PROFILE_RELAXED_RESPONSE_V1", "symbolic_only": symbolic_only,
        "passed": exact_pass and (symbolic_only or numeric_pass) and unchanged,
        "symbolic_checks": exact, "numerical": numerical, "unchanged_dependencies": unchanged,
        "closure_flags": {
            "derived_local_static_response": exact_pass and numeric_pass and unchanged,
            "old_mode_coercivity_import_rejected_by_ledger_family": exact_pass,
            "full_spatial_RefG_closure": False, "guaranteed_global_positive_pressure": False,
            "damping_derived": False, "finite_global_one_mode_inertia_derived": False,
            "observational_pass": False, "singularity_resolution": False,
        },
        "scope": {
            "probe": "constrained-energy multiplier only; removed at lambda=0",
            "observable": "fixed smooth weighted u; geometric scale is exp(-A), not average(exp(-u))",
            "response": "local static radial profile response at alpha=.003 and inherited Q",
            "energy": "fixed-Q physical energy; multiplier energy excluded; exterior tail included",
            "inertia": "nonzero dC/dA yields an instantaneous tail inertia growing linearly with outer cutoff",
            "dynamics": "causal PDE and phase transport remain distinct from static profile tangents",
        },
        "provenance": {"self_sha256": digest(Path(__file__)), "ledger_sha256": digest(CONTRACT),
                       "candidate_sha256": digest(CANDIDATE), "W58_sha256": digest(model.W58),
                       "python": sys.version.split()[0], "numpy": np.__version__,
                       "scipy": scipy.__version__, "sympy": sp.__version__},
        "writes_files": False,
    }


if __name__ == "__main__":
    try:
        if any(arg != "--symbolic-only" for arg in sys.argv[1:]):
            raise ValueError("Only --symbolic-only is supported")
        report = run(symbolic_only="--symbolic-only" in sys.argv[1:])
    except Exception as exc:
        report = {"claim_id": "PROFILE_RELAXED_RESPONSE_V1", "passed": False,
                  "exception_type": type(exc).__name__, "exception": str(exc), "writes_files": False}
    print(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False))
    raise SystemExit(0 if report["passed"] else 1)
