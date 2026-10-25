#!/usr/bin/env python3
"""
Standalone SymPy + SciPy verifier for:
  CLAIM_ID: REFG_COVARIANT_GALACTIC_BRIDGE_AUDIT_V1
  MODEL_VERSION: REFG_COVARIANT_GALACTIC_BRIDGE_V1

Verifies Stage 5 of the RefG Strategic Development Plan:
  1. Theorem 1: Canonical quadratic-gradient weak-field reduction to linear Poisson equation
     and no-go for flat asymptotic rotation curves without non-quadratic IR completion.
  2. Theorem 2: Exact equivalence between the w3_10 constitutive potential W(g_v, g_N),
     the interpolating functions mu_1(x) = x/(1+x), nu_1(y) = (1+sqrt(1+4/y))/2, and the
     covariant AQUAL k-essence action with closed-form elementary potential
     F_1(x^2) = x^2 - 2x + 2*ln(1+x), alongside the n=2 Solar-System-safe
     completion F_2(x^2) = x*sqrt(1+x^2) - asinh(x), exact BTFR V_f^4 = G*M*a_0, and
     strict ellipticity on (0, infinity).
  3. Theorem 3: Common-scale refractive metric n = exp(-2*Phi/c^2), PPN gamma = 1,
     exact factor-of-2 weak lensing bending angle alpha_inf = 2*pi*sqrt(G*M*a_0)/c^2,
     numerical transition from inner Schwarzschild deflection 4*G*M/(c^2*b) to outer
     isothermal plateau, and quantitative Solar-System screening audit at 1 AU and 9.54 AU.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPORT_MD = HERE / "covariant_galactic_bridge_audit.md"
RESULT_JSON = HERE / "covariant_galactic_bridge_result.json"

UPSTREAM_EXPECTED_SHA256 = {
    "RefG/work 3/Galactic_Dynamics/w3_10_galactic_action_and_btfr.py": "3b2a937e8a15146dd827b0903980947c54593297134be700d1b7c7a44cc40bc3",
    "RefG/work 3/Galactic_Dynamics/w3_11_sparc_rar_validation.py": "8368471ac28bc11114f54fd956907ae6c2e732ae96badd2d155be4225e38937c",
    "RefG/work 3/Galactic_Dynamics/w3_12_aqual_disk_solution.py": "99087f21bef3675cec074a4584ed7bd064e9bf4be3e2df45d3356d12583118ac",
    "RefG/work 3/Galactic_Dynamics/w3_13_refractive_lensing.py": "b3ed8bea1d9dab33bd9e8bd5e10dd0255c1c017cf042c8fc7859668d3210463f",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_symbolic_checks() -> tuple[dict[str, bool], dict[str, str], dict[str, bool]]:
    checks: dict[str, bool] = {}
    residuals: dict[str, str] = {}
    neg_controls: dict[str, bool] = {}

    def check_zero(name: str, expr: sp.Expr) -> None:
        s = sp.simplify(expr)
        residuals[name] = str(s)
        checks[name] = bool(s == 0)

    x, y, g, g_N, g_v, a0, G, M, r, b, z, c, Phi = sp.symbols(
        "x y g g_N g_v a_0 G M r b z c Phi", positive=True
    )

    # -------------------------------------------------------------------------
    # 1. Theorem 1: Canonical quadratic-gradient weak-field limit & no-go
    # -------------------------------------------------------------------------
    N_wf = sp.exp(Phi / c**2)
    H_wf = -Phi / c**2
    Y_hat_wf = N_wf * sp.exp(H_wf)
    check_zero("common_scale_weak_field_Y_hat_equals_one", Y_hat_wf - 1)

    g_quad = G * M / r**2
    v_sq_quad = r * g_quad
    lim_v_sq_quad = sp.limit(v_sq_quad, r, sp.oo)
    check_zero("canonical_quadratic_asymptotic_velocity_vanishes", lim_v_sq_quad)
    neg_controls["pure_quadratic_gradient_action_flat_rotation_rejected"] = bool(
        lim_v_sq_quad == 0
    )
    checks["negative_control_pure_quadratic_gradient_rejected"] = neg_controls[
        "pure_quadratic_gradient_action_flat_rotation_rejected"
    ]

    # -------------------------------------------------------------------------
    # 2. Theorem 2: Exact equivalence between w3_10 and Covariant AQUAL k-essence
    # -------------------------------------------------------------------------
    W_pot = sp.Rational(1, 3) * g_v**3 + sp.Rational(1, 2) * g_N * g_v**2 - a0 * g_N * g_v
    dW_dgv = sp.diff(W_pot, g_v)
    check_zero("w3_10_constitutive_stationarity_polynomial", dW_dgv - (g_v**2 + g_N * g_v - a0 * g_N))

    gv_sol = (-g_N + sp.sqrt(g_N**2 + 4 * a0 * g_N)) / 2
    g_tot = sp.simplify(g_N + gv_sol)
    check_zero("w3_10_total_acceleration_formula", g_tot - (g_N + sp.sqrt(g_N**2 + 4 * a0 * g_N)) / 2)

    # Substitute g_v = g - g_N into dW/dg_v
    aqual_alg = sp.simplify(dW_dgv.subs(g_v, g - g_N))
    check_zero("w3_10_to_aqual_algebraic_identity", aqual_alg - (g**2 - g * g_N - a0 * g_N))

    # Interpolating functions mu_1(x) and nu_1(y)
    mu1 = x / (1 + x)
    nu1 = (1 + sp.sqrt(1 + 4 / y)) / 2
    check_zero(
        "mu1_nu1_reciprocity_identity",
        mu1.subs(x, y * nu1) * nu1 - 1,
    )

    # Interpolating functions mu_2(x) and nu_2(y) (n=2 standard family)
    mu2 = x / sp.sqrt(1 + x**2)
    nu2 = sp.sqrt((1 + sp.sqrt(1 + 4 / y**2)) / 2)
    check_zero(
        "mu2_nu2_reciprocity_identity",
        sp.expand((mu2.subs(x, y * nu2) * nu2) ** 2 - 1),
    )

    # Closed-form covariant k-essence potentials F_1(x^2) and F_2(x^2)
    # Since s = x^2, dF/ds = (1/(2x)) dF/dx
    F1 = x**2 - 2 * x + 2 * sp.log(1 + x)
    dF1_ds = sp.simplify(sp.diff(F1, x) / (2 * x))
    check_zero("covariant_k_essence_F1_derivative_matches_mu1", dF1_ds - mu1)
    check_zero("covariant_k_essence_F1_vanishes_at_zero", F1.subs(x, 0))

    F2 = x * sp.sqrt(1 + x**2) - sp.asinh(x)
    dF2_ds = sp.simplify(sp.diff(F2, x) / (2 * x))
    check_zero("covariant_k_essence_F2_derivative_matches_mu2", dF2_ds - mu2)
    check_zero("covariant_k_essence_F2_vanishes_at_zero", F2.subs(x, 0))

    # Deep-IR (x -> 0) and Newtonian (x -> oo) limits of F1 and F2
    F1_ir_series = sp.series(F1, x, 0, 6).removeO()
    expected_F1_ir = sp.Rational(2, 3) * x**3 - sp.Rational(1, 2) * x**4 + sp.Rational(2, 5) * x**5
    check_zero("F1_deep_IR_p3_aqual_series", F1_ir_series - expected_F1_ir)

    F2_ir_series = sp.series(F2, x, 0, 6).removeO()
    expected_F2_ir = sp.Rational(2, 3) * x**3 - sp.Rational(1, 5) * x**5
    check_zero("F2_deep_IR_p3_aqual_series", F2_ir_series - expected_F2_ir)

    check_zero("F1_high_acceleration_quadratic_limit", sp.limit(F1 / x**2, x, sp.oo) - 1)
    check_zero("F2_high_acceleration_quadratic_limit", sp.limit(F2 / x**2, x, sp.oo) - 1)

    # Exact Baryonic Tully-Fisher Relation V_f^4 = G*M*a_0 for both families
    g_ir_1 = sp.sqrt(r**2 * g_tot.subs(g_N, G * M / r**2) ** 2)
    v4_asymp_1 = sp.limit((r * g_tot.subs(g_N, G * M / r**2)) ** 2, r, sp.oo)
    check_zero("exact_btfr_limit_mu1_family", v4_asymp_1 - G * M * a0)

    g_tot_2 = (G * M / r**2) * nu2.subs(y, G * M / (a0 * r**2))
    v4_asymp_2 = sp.limit((r * g_tot_2) ** 2, r, sp.oo)
    check_zero("exact_btfr_limit_mu2_family", v4_asymp_2 - G * M * a0)

    # Ellipticity eigenvalues and ratios
    lam_par_1 = sp.simplify(sp.diff(x * mu1, x))
    check_zero("ellipticity_radial_eigenvalue_mu1", lam_par_1 - x * (2 + x) / (1 + x) ** 2)
    check_zero(
        "ellipticity_ratio_mu1",
        sp.simplify(lam_par_1 / mu1) - (1 + 1 / (1 + x)),
    )

    lam_par_2 = sp.simplify(sp.diff(x * mu2, x))
    check_zero(
        "ellipticity_radial_eigenvalue_mu2",
        lam_par_2 - x * (2 + x**2) / (1 + x**2) ** sp.Rational(3, 2),
    )
    check_zero(
        "ellipticity_ratio_mu2",
        sp.simplify(lam_par_2 / mu2) - (1 + 1 / (1 + x**2)),
    )

    # Negative control: non-monotone / decreasing flux x*mu(x) violates ellipticity
    mu_bad = x / (1 + x**3)
    lam_par_bad = sp.simplify(sp.diff(x * mu_bad, x).subs(x, 2))
    neg_controls["non_elliptic_decreasing_flux_interpolator_rejected"] = bool(
        lam_par_bad < 0
    )
    checks["negative_control_non_elliptic_interpolator_rejected"] = neg_controls[
        "non_elliptic_decreasing_flux_interpolator_rejected"
    ]

    # -------------------------------------------------------------------------
    # 3. Theorem 3: Common-scale refractive index, PPN gamma=1, and lensing
    # -------------------------------------------------------------------------
    u_phi = sp.Symbol("u_phi", real=True)
    n_series = sp.series(sp.exp(-2 * u_phi), u_phi, 0, 3).removeO()
    check_zero(
        "common_scale_refractive_index_weak_field_series",
        n_series - (1 - 2 * u_phi + 2 * u_phi**2),
    )

    # Deep-IR logarithmic potential Phi = V_f^2 ln(r), deflection angle integral
    Vf = sp.Symbol("V_f", positive=True)
    r_los = sp.sqrt(b**2 + z**2)
    Phi_ir = Vf**2 * sp.log(r_los)
    grad_perp_ln_n = -sp.Rational(2, 1) / c**2 * sp.diff(Phi_ir, b)
    alpha_gal = -sp.integrate(grad_perp_ln_n, (z, -sp.oo, sp.oo))
    check_zero(
        "deep_IR_weak_lensing_deflection_angle",
        alpha_gal - 2 * sp.pi * Vf**2 / c**2,
    )
    check_zero(
        "deep_IR_lensing_matches_btfr_mass",
        alpha_gal.subs(Vf, (G * M * a0) ** sp.Rational(1, 4))
        - 2 * sp.pi * sp.sqrt(G * M * a0) / c**2,
    )

    # Negative control: Newtonian time-only metric (gamma_PPN = 0, n = 1 - Phi/c^2) misses factor of 2
    alpha_time_only = sp.integrate(sp.diff(Phi_ir, b) / c**2, (z, -sp.oo, sp.oo))
    neg_controls["time_only_metric_missing_factor_of_two_lensing_rejected"] = bool(
        sp.simplify(alpha_gal / alpha_time_only) == 2
    )
    checks["negative_control_time_only_metric_lensing_rejected"] = neg_controls[
        "time_only_metric_missing_factor_of_two_lensing_rejected"
    ]

    # High-acceleration anomalous acceleration series for mu_1 and mu_2
    dg_mu1_lead = sp.limit(a0 * y * (nu1 - 1), y, sp.oo)
    check_zero("mu1_high_acceleration_residual_equals_a0", dg_mu1_lead - a0)

    dg_mu2_lead = sp.limit(y * (y * (nu2 - 1)), y, sp.oo)
    check_zero("mu2_high_acceleration_residual_scales_as_inv_y", dg_mu2_lead - sp.Rational(1, 2))
    neg_controls["unscreened_mu1_outer_solar_system_ephemeris_tension_flagged"] = bool(
        dg_mu1_lead == a0
    )
    checks["negative_control_mu1_outer_solar_system_flagged"] = neg_controls[
        "unscreened_mu1_outer_solar_system_ephemeris_tension_flagged"
    ]

    return checks, residuals, neg_controls


def run_numerical_audit() -> dict:
    G_SI = 6.67430e-11
    c_SI = 2.99792458e8
    M_sun = 1.98847e30
    AU_m = 1.495978707e11
    a0_SI = 1.2e-10

    r_M_sun = float(np.sqrt(G_SI * M_sun / a0_SI))

    def eval_planet(r_au: float) -> dict[str, float]:
        r_m = r_au * AU_m
        g_N = G_SI * M_sun / r_m**2
        y = g_N / a0_SI
        # Exact algebraic formulas written in cancellation-safe form:
        # nu_1(y) - 1 = (sqrt(1 + 4/y) - 1)/2 = 2 / (y * (1 + sqrt(1 + 4/y)))
        delta_g_mu1 = a0_SI * (2.0 / (1.0 + np.sqrt(1.0 + 4.0 / y)))
        # nu_2(y) - 1 = (2 / (y^2 * (1 + sqrt(1 + 4/y^2)))) / (1 + sqrt((1 + sqrt(1 + 4/y^2))/2))
        u2 = 2.0 / (y**2 * (1.0 + np.sqrt(1.0 + 4.0 / y**2)))
        delta_g_mu2 = g_N * (u2 / (1.0 + np.sqrt(1.0 + u2)))
        return {
            "r_AU": r_au,
            "g_N_m_s2": float(g_N),
            "y_gN_over_a0": float(y),
            "delta_g_mu1_m_s2": float(delta_g_mu1),
            "frac_delta_g_mu1": float(delta_g_mu1 / g_N),
            "delta_g_mu2_m_s2": float(delta_g_mu2),
            "frac_delta_g_mu2": float(delta_g_mu2 / g_N),
        }

    earth = eval_planet(1.0)
    saturn = eval_planet(9.54)

    # Dimensionless lensing deflection profile across impact parameter u_b = b / r_M
    # In units of alpha_inf = 2*pi*sqrt(G*M*a_0)/c^2:
    # alpha(b) / alpha_inf = (2 / pi) * int_0^oo g_hat(u_b * cosh(t)) dt
    # where g_hat(u) = (1/u^2) * nu_1(1/u^2)
    def alpha_ratio_integrand(u_z: float, u_b: float) -> float:
        u_r2 = u_b**2 + u_z**2
        y_loc = 1.0 / u_r2
        g_loc = 0.5 * (y_loc + np.sqrt(y_loc**2 + 4.0 * y_loc))
        return (2.0 / np.pi) * g_loc * (u_b / np.sqrt(u_r2))

    u_b_inner = 1e-3
    alpha_inner_norm, _ = quad(
        alpha_ratio_integrand, 0.0, np.inf, args=(u_b_inner,), epsabs=1e-11, epsrel=1e-11
    )
    # Expected inner GR deflection in units of alpha_inf is (4*G*M/(c^2*b)) / (2*pi*sqrt(G*M*a0)/c^2) = 2 / (pi * u_b)
    gr_inner_expected = 2.0 / (np.pi * u_b_inner)
    inner_gr_rel_err = abs(alpha_inner_norm - gr_inner_expected) / gr_inner_expected

    u_b_outer = 1e3
    alpha_outer_norm, _ = quad(
        alpha_ratio_integrand, 0.0, np.inf, args=(u_b_outer,), epsabs=1e-11, epsrel=1e-11
    )
    outer_plateau_rel_err = abs(alpha_outer_norm - 1.0)

    # Galactic RAR comparison between mu_1 and mu_2 across g_bar in [1e-13, 1e-8] m/s^2
    g_bar_grid = np.logspace(-13, -8, 500)
    y_grid = g_bar_grid / a0_SI
    g_mu1 = g_bar_grid * 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y_grid))
    g_mu2 = g_bar_grid * np.sqrt(0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y_grid**2)))
    max_rar_dex_diff = float(np.max(np.abs(np.log10(g_mu1) - np.log10(g_mu2))))

    # Milky Way benchmark (M_bar = 6e10 M_sun)
    M_gal = 6.0e10 * M_sun
    Vf_mw_kms = float((G_SI * M_gal * a0_SI) ** 0.25 / 1e3)
    alpha_mw_arcsec = float(
        (2.0 * np.pi * np.sqrt(G_SI * M_gal * a0_SI) / c_SI**2) * (180.0 / np.pi) * 3600.0
    )

    return {
        "solar_system_transition_radius_AU": float(r_M_sun / AU_m),
        "earth_1AU": earth,
        "saturn_9.54AU": saturn,
        "lensing_inner_GR_match_u_b_1e-3_rel_err": float(inner_gr_rel_err),
        "lensing_outer_plateau_match_u_b_1e3_rel_err": float(outer_plateau_rel_err),
        "max_rar_log10_diff_mu1_vs_mu2_dex": max_rar_dex_diff,
        "milky_way_6e10_Msun_Vf_km_s": Vf_mw_kms,
        "milky_way_6e10_Msun_asymptotic_lensing_arcsec": alpha_mw_arcsec,
    }


def main() -> int:
    checks, sym_residuals, neg_controls = run_symbolic_checks()

    upstream_hashes: dict[str, dict[str, str | bool]] = {}
    for rel_path, expected_sha in UPSTREAM_EXPECTED_SHA256.items():
        abs_path = ROOT / rel_path
        actual_sha = sha256_file(abs_path) if abs_path.exists() else "MISSING"
        matched = bool(actual_sha == expected_sha)
        upstream_hashes[rel_path] = {
            "expected_sha256": expected_sha,
            "actual_sha256": actual_sha,
            "matched": matched,
        }
        checks[f"upstream_sha256_{Path(rel_path).name}"] = matched

    num_audit = run_numerical_audit()

    checks["lensing_inner_limit_matches_schwarzschild_4GM_c2b"] = bool(
        num_audit["lensing_inner_GR_match_u_b_1e-3_rel_err"] < 2e-3
    )
    checks["lensing_outer_limit_matches_isothermal_plateau"] = bool(
        num_audit["lensing_outer_plateau_match_u_b_1e3_rel_err"] < 2e-3
    )
    checks["earth_1AU_mu1_fractional_deviation_below_3e-8"] = bool(
        num_audit["earth_1AU"]["frac_delta_g_mu1"] < 3e-8
    )
    checks["saturn_mu2_anomalous_acceleration_below_1e-15_m_s2"] = bool(
        num_audit["saturn_9.54AU"]["delta_g_mu2_m_s2"] < 1e-15
    )
    checks["saturn_mu2_fractional_deviation_below_1e-11"] = bool(
        num_audit["saturn_9.54AU"]["frac_delta_g_mu2"] < 1e-11
    )
    checks["galactic_rar_mu1_mu2_difference_below_sparc_scatter"] = bool(
        num_audit["max_rar_log10_diff_mu1_vs_mu2_dex"] < 0.11
    )
    checks["milky_way_btfr_flat_velocity_in_physical_range"] = bool(
        170.0 < num_audit["milky_way_6e10_Msun_Vf_km_s"] < 185.0
    )

    all_passed = all(checks.values()) and all(neg_controls.values())

    result = {
        "claim_id": "REFG_COVARIANT_GALACTIC_BRIDGE_AUDIT_V1",
        "model_version": "REFG_COVARIANT_GALACTIC_BRIDGE_V1",
        "status": "PASS_COVARIANT_GALACTIC_BRIDGE_AND_SCREENING_AUDIT" if all_passed else "FAIL",
        "all_checks_passed": all_passed,
        "total_checks": len(checks),
        "passed_checks": sum(1 for v in checks.values() if v),
        "failed_checks": [k for k, v in checks.items() if not v],
        "negative_controls": neg_controls,
        "symbolic_residuals": sym_residuals,
        "numerical_audit": num_audit,
        "checks": checks,
        "provenance": {
            "python_version": sys.version.split()[0],
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "sympy_version": sp.__version__,
            "verifier_sha256": sha256_file(Path(__file__).resolve()),
            "report_sha256": sha256_file(REPORT_MD) if REPORT_MD.exists() else "MISSING",
            "upstream_sha256": upstream_hashes,
        },
    }

    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "all_checks_passed": all_passed,
                "passed_checks": result["passed_checks"],
                "total_checks": result["total_checks"],
                "failed_checks": result["failed_checks"],
                "saturn_delta_g_mu1": num_audit["saturn_9.54AU"]["delta_g_mu1_m_s2"],
                "saturn_delta_g_mu2": num_audit["saturn_9.54AU"]["delta_g_mu2_m_s2"],
                "mw_Vf_km_s": num_audit["milky_way_6e10_Msun_Vf_km_s"],
                "mw_lensing_arcsec": num_audit["milky_way_6e10_Msun_asymptotic_lensing_arcsec"],
            },
            indent=2,
        )
    )
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
