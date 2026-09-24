"""Fixed-charge radial ADM Hessian of the weak full-action body.

Exploratory discretization selected before this saved verification; the report
records that history. No W66 strong-field campaign or dynamical eigenfrequency
calculation is called. Import verify_radial_stability(background) to reuse a BVP.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.dont_write_bytecode = True
import numpy as np
import scipy
from scipy.integrate import cumulative_trapezoid, simpson
from scipy.linalg import cho_factor, cho_solve, eigh

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "Lagrangian_Formulation" / "Oscillon_Inertia" / "verify_oscillon_inertia.py"
WEAK_EQUILIBRIUM_SHA256 = "32cf32e9cfd590f93928eff16cbfe5494836df8b9d72bfd88b3cf3ba7da22076"
ALPHA, CHARGE = .001, 190.401136223484
SPECS = ((24., 200), (24., 400), (32., 400))
CRITERIA = {
    "momentum_block_lower_threshold": .9,
    "constrained_hessian_lower_threshold": .3,
    "same_domain_refinement_absolute_tolerance": 3e-5,
    "normalized_charge_projection_tolerance": 1e-11,
    "symmetry_absolute_tolerance": 1e-10,
    "negative_curvature_mutation_upper_threshold": -.5,
    "energy_second_difference_finest_relative_tolerance": 2e-6,
    "energy_second_difference_contraction_upper": .3,
    "energy_quadrature_relative_tolerance": 1e-7,
    "stationarity_absolute_tolerance": 1e-7,
    "background_BVP_residual_tolerance": 1e-6,
}


def locked_equilibrium_source():
    actual = hashlib.sha256(OLD.read_bytes()).hexdigest()
    if actual != WEAK_EQUILIBRIUM_SHA256:
        raise RuntimeError("Weak-equilibrium dependency changed; review the radial Hessian contract before reuse")
    return {"expected_sha256": WEAK_EQUILIBRIUM_SHA256, "actual_sha256": actual, "pass": True}


def omega(background):
    return float(1 / (1 + np.exp(-background.p[0])))


def potential(f):
    return f*f/2-f**4/4+f**6/24


def finite_element_record(background, radius, intervals, alpha=ALPHA):
    """All P1 amplitude and phase-momentum directions; constrained Schur test."""
    n = intervals-1
    spacing = radius/intervals
    xi = np.array([.5-.5/np.sqrt(3), .5+.5/np.sqrt(3)])
    x = ((np.arange(intervals)[:, None]+xi[None, :])*spacing).ravel()
    weights = np.full(2*intervals, spacing/2)
    shape = np.zeros((2*intervals, n)); derivative = np.zeros_like(shape)
    for element in range(intervals):
        ids = np.array([2*element, 2*element+1])
        if element > 0:
            shape[ids, element-1] = 1-xi
            derivative[ids, element-1] = -1/spacing
        if element < n:
            shape[ids, element] = xi
            derivative[ids, element] = 1/spacing
    f, fp, mass, logsigma = background.sol(x)[:4]
    sigma = np.exp(logsigma); metric = 1-2*alpha*mass/x; om = omega(background)
    vf = f-f**3+f**5/4; vff = 1-3*f*f+5*f**4/4
    # H maps (a,b) coefficients to delta h; delta f=a/r, delta P=r f b.
    ha = 2*(x*fp)[:, None]*derivative-2*(fp+x*f*om**2/(sigma**2*metric**2))[:, None]*shape
    hb = 2*(x*f*om/(sigma*metric))[:, None]*shape
    hmap = np.hstack((ha, hb))
    source = np.hstack(((x*vf)[:, None]*shape, np.zeros_like(shape)))+.5*metric[:, None]*hmap
    # Ordered Gauss-2 Volterra rule: full preceding weights, half own weight.
    volterra = np.tril(np.ones((2*intervals, 2*intervals)), -1)+.5*np.eye(2*intervals)
    dm = (volterra@((weights*sigma)[:, None]*source))/sigma[:, None]
    radial_derivative = derivative-shape/x[:, None]
    haa = shape.T@((weights*(sigma*vff+3*om**2/(sigma*metric)))[:, None]*shape)
    haa += radial_derivative.T@((weights*sigma*metric)[:, None]*radial_derivative)
    hbb = shape.T@((weights*sigma*metric)[:, None]*shape)
    hab = shape.T@((-2*om*weights)[:, None]*shape)
    full = np.block([[haa, hab], [hab.T, hbb]])
    gravity = -alpha*hmap.T@((weights*sigma/x)[:, None]*dm)
    full += gravity+gravity.T
    haa, hab, hbb = full[:n, :n], full[:n, n:], full[n:, n:]
    norm = shape.T@(weights[:, None]*shape)
    momentum_lowest = float(eigh(hbb, norm, subset_by_index=(0, 0), check_finite=False)[0][0])
    factor = cho_factor(hbb, check_finite=False)
    invcross = cho_solve(factor, hab.T, check_finite=False)
    q = shape.T@(weights*x*f)
    invq = cho_solve(factor, q, check_finite=False)
    denominator = float(q@invq)
    crossq = hab@invq
    minimized_momentum = -invcross+np.outer(invq, crossq)/denominator
    reduced = haa-hab@invcross+np.outer(crossq, crossq)/denominator
    values = eigh(reduced, norm, subset_by_index=(0, 5), check_finite=False)[0]
    charge_residual = float(np.linalg.norm(q@minimized_momentum)
                            /max(np.linalg.norm(q)*np.linalg.norm(minimized_momentum), 1e-30))
    symmetry = float(np.max(np.abs(reduced-reduced.T)))
    # Diagnostic curvature mutation V'' -> V''-1/sigma gives reduced -> reduced-norm.
    negative = float(eigh(reduced-norm, norm, subset_by_index=(0, 0), check_finite=False)[0][0])
    checks = {
        "momentum_block_positive": momentum_lowest > CRITERIA["momentum_block_lower_threshold"],
        "all_resolved_constrained_radial_directions_positive": float(values[0]) > CRITERIA["constrained_hessian_lower_threshold"],
        "full_momentum_minimizer_preserves_fixed_charge": charge_residual < CRITERIA["normalized_charge_projection_tolerance"],
        "quadratic_form_symmetric": symmetry < CRITERIA["symmetry_absolute_tolerance"],
        "negative_curvature_control_rejected": negative < CRITERIA["negative_curvature_mutation_upper_threshold"],
        "regular_metric_on_quadrature": float(np.min(metric)) > 0 and float(np.min(sigma)) > 0,
    }
    return {
        "radius": radius, "intervals": intervals, "spacing": spacing,
        "internal_modes_per_channel": n, "independent_constrained_directions": 2*n-1,
        "momentum_block_lowest_generalized_eigenvalue": momentum_lowest,
        "constrained_schur_lowest_six_generalized_eigenvalues": values.tolist(),
        "normalized_charge_projection_residual": charge_residual,
        "quadratic_form_symmetry_residual": symmetry,
        "negative_curvature_control_lowest": negative,
        "checks": checks, "all_passed": all(checks.values()),
    }


def energy_second_difference_check(background, alpha=ALPHA):
    """Independent nonlinear ADM integrating-factor energy, fixed mesh."""
    om = omega(background); records = []
    for points in (16001, 32001):
        r = np.linspace(1e-6, 40., points)
        f, fp, mass, ls = background.sol(r)[:4]
        sigma = np.exp(ls); metric = 1-2*alpha*mass/r
        eta = np.exp(-r*r/4); etap = -r*eta/2
        b0, b1 = r*np.exp(-r*r/9), r*np.exp(-r*r/16)
        k = simpson(r*f*b0, x=r)/simpson(r*f*b1, x=r)
        b = b0-k*b1; phase_momentum = om*r*r*f*f/(sigma*metric); zeta = r*f*b
        h = r*r*fp*fp+phase_momentum**2/(r*r*f*f)
        dh = 2*r*r*fp*etap+2*phase_momentum*zeta/(r*r*f*f)-2*phase_momentum**2*eta/(r*r*f**3)
        d2h = (2*r*r*etap*etap+2*zeta*zeta/(r*r*f*f)
               -8*phase_momentum*zeta*eta/(r*r*f**3)+6*phase_momentum**2*eta*eta/(r*r*f**4))
        exponent = cumulative_trapezoid(alpha*h/r, x=r, initial=0)
        weight = np.exp(exponent-exponent[-1])
        source = r*r*(f-f**3+f**5/4)*eta+.5*metric*dh
        dm = np.exp(-exponent)*cumulative_trapezoid(np.exp(exponent)*source, x=r, initial=0)
        second = float(simpson(weight*(r*r*(1-3*f*f+5*f**4/4)*eta*eta
                                       +.5*metric*d2h-2*alpha*dh*dm/r), x=r))

        def energy(epsilon):
            ff, pp, pq = f+epsilon*eta, fp+epsilon*etap, phase_momentum+epsilon*zeta
            hh = r*r*pp*pp+pq*pq/(r*r*ff*ff)
            aa = cumulative_trapezoid(alpha*hh/r, x=r, initial=0)
            return float(simpson(np.exp(aa-aa[-1])*(r*r*potential(ff)+hh/2), x=r))

        base = energy(0); differences = []
        for epsilon in (.004, .002, .001):
            fd = (energy(epsilon)+energy(-epsilon)-2*base)/epsilon**2
            differences.append({"epsilon": epsilon, "second_difference": fd,
                                "relative_gap": abs(fd/second-1)})
        records.append({"points": points, "analytic_second_variation_m": second,
                        "nonlinear_ADM_m": base, "fixed_charge_variation_over_4pi": float(simpson(zeta, x=r)),
                        "stationarity_first_variation_m": float(dm[-1]), "differences": differences})
    fine = records[-1]; gaps = [r["relative_gap"] for r in fine["differences"]]
    checks = {
        "nonlinear_energy_second_difference_agrees": gaps[-1] < CRITERIA["energy_second_difference_finest_relative_tolerance"],
        "second_difference_quadratic_contraction": all(gaps[j+1]/gaps[j] < CRITERIA["energy_second_difference_contraction_upper"] for j in (0, 1)),
        "quadrature_convergence": abs(records[0]["analytic_second_variation_m"]/fine["analytic_second_variation_m"]-1) < CRITERIA["energy_quadrature_relative_tolerance"],
        "fixed_charge_control": max(abs(r["fixed_charge_variation_over_4pi"]) for r in records) < 1e-11,
        "equilibrium_stationarity_control": max(abs(r["stationarity_first_variation_m"]) for r in records) < CRITERIA["stationarity_absolute_tolerance"],
    }
    return {"records": records, "checks": checks, "all_passed": all(checks.values())}


def verify_radial_stability(background, alpha=ALPHA, charge=CHARGE):
    """Verification API; reuses caller's five-field weak fixed-charge BVP."""
    dependency = locked_equilibrium_source()
    if alpha != ALPHA or charge != CHARGE:
        raise ValueError("This contract covers only alpha=.001, Q=190.401136223484")
    if background.x[-1] < 40:
        raise ValueError("Background domain must reach radius 40")
    rows = [finite_element_record(background, radius, intervals, alpha) for radius, intervals in SPECS]
    energy = energy_second_difference_check(background, alpha)
    lowest = lambda row: row["constrained_schur_lowest_six_generalized_eigenvalues"][0]
    refinement = abs(lowest(rows[0])-lowest(rows[1]))
    r = np.linspace(background.x[0], background.x[-1], 8001)
    f, fp, mass, ls = background.sol(r)[:4]
    sigma = np.exp(ls); metric = 1-2*alpha*mass/r; om = omega(background)
    actual_charge = float(4*np.pi*(simpson(om*r*r*f*f/(sigma*metric), x=r)+om*f[0]**2*r[0]**3/(3*sigma[0])))
    background_residual = float(np.max(background.rms_residuals))
    checks = {
        "weak_equilibrium_source_hash_locked": dependency["pass"],
        "background_BVP_residual_pass": background_residual < CRITERIA["background_BVP_residual_tolerance"],
        "same_fixed_charge_body": abs(actual_charge/charge-1) < 2e-6,
        "weak_regular_background": float(np.min(sigma*np.sqrt(metric))) > .9 and float(np.min(metric)) > .9,
        "all_full_radial_FE_forms_pass": all(row["all_passed"] for row in rows),
        "same_domain_refinement_pass": refinement < CRITERIA["same_domain_refinement_absolute_tolerance"],
        "larger_domain_positive_margin_pass": lowest(rows[-1]) > CRITERIA["constrained_hessian_lower_threshold"],
        "independent_nonlinear_energy_crosscheck_pass": energy["all_passed"],
    }
    passed = all(checks.values())
    return {
        "claim_id": "REFG_WEAK_SAME_ACTION_FIXED_CHARGE_RADIAL_ADM_HESSIAN_V1",
        "status": "NUMERICAL_EVIDENCE_POSITIVE_CONSTRAINED_RADIAL_ADM_HESSIAN" if passed else "RADIAL_HESSIAN_VERIFICATION_FAILED",
        "all_passed": passed, "checks": checks, "criteria": CRITERIA,
        "weak_equilibrium_dependency": dependency,
        "background_BVP_max_residual": background_residual,
        "alpha": alpha, "charge_target": charge, "charge_quadrature": float(actual_charge),
        "Omega": om, "f_at_inner_boundary": float(f[0]),
        "minimum_F": float(np.min(metric)), "minimum_lapse": float(np.min(sigma*np.sqrt(metric))),
        "finite_element_records": rows, "same_domain_refinement_difference": refinement,
        "larger_domain_lowest_change": lowest(rows[-1])-lowest(rows[1]),
        "asymptotic_reduced_Hessian_threshold": 1-om*om,
        "energy_crosscheck": energy,
        "scope": {
            "full_discrete_fixed_charge_radial_form_tested": passed,
            "radial_linear_energy_stability_numerical_evidence": passed,
            "exact_continuum_spectral_proof": False,
            "oscillation_eigenfrequencies_computed": False,
            "nonradial_stability_computed": False, "nonlinear_stability_proved": False,
            "strong_field_campaign_performed": False, "collapse_or_horizon_computed": False,
        },
        "selection_history": "Method and thresholds selected after exploratory calculations; saved verification is a reproducibility/regression test, not untouched prediction.",
    }


def main():
    locked_equilibrium_source()
    spec = importlib.util.spec_from_file_location("radial_weak_inertia_seed", OLD)
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
    flat = module.load_seed_module().solve_profile(.8, radius=80., tolerance=1e-8)
    background = module.equilibrium(flat, 60., 3e-8, 1e-5)
    result = verify_radial_stability(background)
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    result["provenance"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__,
        "source_sha256": sha(Path(__file__)), "contract_sha256": sha(HERE/"radial_stability_revision.md"),
        "weak_equilibrium_source_sha256": sha(OLD),
        "weak_equilibrium_BVP_max_residual": float(max(background.rms_residuals)),
    }
    output = HERE/"radial_stability_result.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
