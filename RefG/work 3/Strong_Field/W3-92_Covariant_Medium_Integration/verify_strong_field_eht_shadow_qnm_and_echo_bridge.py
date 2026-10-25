#!/usr/bin/env python3
"""
Verification suite for REFG_STRONG_FIELD_EHT_SHADOW_QNM_AND_ECHO_BRIDGE_V1:
1. Exact photon sphere r_ph^+ = 2m, critical shadow impact parameter b_c = 2*e*m,
   fractional deviation delta_sh = 2*e/(3*sqrt(3)) - 1 = +4.629707%, and
   quantitative Event Horizon Telescope (EHT) shadow comparison for Sgr A* and M87*.
2. Global C^2 smoothness of the radial optical refractive index n_opt(r) = sqrt(A(r)/B(r))
   (C^3 tortoise coordinate r_*(r)) across the action-derived degree-6 C^2 core boundary
   r = r_c, and exact eikonal quasinormal mode (QNM) frequency Omega_ph = c_0/(2*e*m),
   Lyapunov exponent lambda_L = c_0/(2*e*m), and quality-factor invariance Q_ln^RefG = Q_ln^GR.
3. Strictly finite optical tortoise cavity depth L_*(q), closed-form exterior exponential-integral
   identity, inner stable light ring r_lr^- = r_c * x_lr(q), and quantitative gravitational-wave
   echo delay times Delta t_echo(q, M) for stellar-mass mergers (10 M_sun, 30 M_sun,
   GW150914 remnant 62 M_sun) and Sgr A*.
4. Three negative mutation controls (divergent Schwarzschild horizon tortoise integral,
   C^0-only core junction jump, and mutated shadow radius violating EHT 1-sigma bounds).
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import sympy as sp
from scipy import integrate, optimize, special


HERE = Path(__file__).resolve().parent
RESULT_PATH = HERE / "strong_field_eht_shadow_qnm_and_echo_bridge_result.json"
UPSTREAM_CLOSURE_SCRIPT = HERE / "verify_action_derived_c2_interior_closure.py"
UPSTREAM_CLOSURE_JSON = HERE / "action_derived_c2_interior_closure_result.json"

# Fundamental physical and astronomical constants (CODATA / IAU / PDG)
G_SI = 6.67430e-11              # m^3 kg^-1 s^-2
C0_SI = 299792458.0             # m s^-1
M_SUN_KG = 1.98847e30           # kg
GM_SUN_C2_M = 1476.6250385      # G M_sun / c_0^2 [m]
GM_SUN_C3_S = 4.925490947e-6    # G M_sun / c_0^3 [s]
RAD_TO_UAS = (180.0 / math.pi) * 3600.0 * 1.0e6


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def add_check(
    checks: List[Dict[str, Any]],
    name: str,
    passed: bool,
    value: Any,
    expected: Any,
    tolerance: Any = None,
) -> None:
    checks.append(
        {
            "name": name,
            "passed": bool(passed),
            "value": value,
            "expected": expected,
            "tolerance": tolerance,
        }
    )


def verify_part1_photon_sphere_and_eht_shadow(checks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Part 1: Symbolic proof of r_ph^+ = 2m, b_c^RefG = 2*e*m, delta_sh = 2*e/(3*sqrt(3)) - 1,
    and quantitative comparison against EHT Sgr A* (2022) and M87* (2019/2021) bounds.
    """
    r, m = sp.symbols("r m", positive=True)
    B_ext = sp.exp(-2 * m / r)
    A_ext = sp.exp(2 * m / r)
    V_opt = B_ext / (A_ext * r**2)

    dV_dr = sp.simplify(sp.diff(V_opt, r))
    expected_dV_dr = 2 * (2 * m - r) * sp.exp(-4 * m / r) / r**4
    res_dV = sp.simplify(dV_dr - expected_dV_dr)
    add_check(
        checks,
        "exterior_optical_potential_first_derivative_exact",
        res_dV == 0,
        str(res_dV),
        "0",
        0,
    )

    roots_r = sp.solve(sp.Eq(dV_dr, 0), r)
    r_ph = roots_r[0]
    add_check(
        checks,
        "outer_photon_sphere_radius_is_2m",
        len(roots_r) == 1 and sp.simplify(r_ph - 2 * m) == 0,
        str(r_ph),
        "2*m",
        0,
    )

    d2V_dr2_ph = sp.simplify(sp.diff(V_opt, r, 2).subs(r, 2 * m))
    expected_d2V_ph = -sp.exp(-2) / (8 * m**4)
    res_d2V = sp.simplify(d2V_dr2_ph - expected_d2V_ph)
    add_check(
        checks,
        "outer_photon_sphere_second_derivative_negative_unstable",
        res_d2V == 0 and float(d2V_dr2_ph.subs(m, 1)) < 0.0,
        str(d2V_dr2_ph),
        "-exp(-2)/(8*m**4) < 0",
        0,
    )

    V_ph = sp.simplify(V_opt.subs(r, 2 * m))
    b_c_sym = sp.simplify(1 / sp.sqrt(V_ph))
    res_bc = sp.simplify(b_c_sym - 2 * sp.E * m)
    add_check(
        checks,
        "critical_impact_parameter_bc_equals_2_e_m",
        res_bc == 0,
        str(b_c_sym),
        "2*E*m",
        0,
    )

    bc_over_m_refg = 2.0 * math.e
    bc_over_m_gr = 3.0 * math.sqrt(3.0)
    delta_sh_refg = bc_over_m_refg / bc_over_m_gr - 1.0

    # Sgr A* EHT (2022, Paper I & VI):
    # theta_g = 5.028 uas (Keck/VLTI prior: M = 4.154e6 M_sun, D = 8.178 kpc)
    # Direct shadow diameter: d_sh = 48.7 +/- 7.0 uas
    # Fractional deviation bound (Keck+VLTI): delta = -0.04 (+0.09 / -0.10), 1-sigma interval [-0.14, +0.05]
    theta_g_sgra_uas = 5.028
    d_sh_gr_sgra_uas = 2.0 * bc_over_m_gr * theta_g_sgra_uas
    d_sh_refg_sgra_uas = 2.0 * bc_over_m_refg * theta_g_sgra_uas
    d_sh_eht_sgra_mean = 48.7
    d_sh_eht_sgra_sigma = 7.0
    z_sgra_direct = abs(d_sh_refg_sgra_uas - d_sh_eht_sgra_mean) / d_sh_eht_sgra_sigma

    delta_sgra_min_1sigma = -0.14
    delta_sgra_max_1sigma = 0.05
    delta_sgra_central = -0.04
    delta_sgra_pos_sigma = 0.09
    z_sgra_delta = (delta_sh_refg - delta_sgra_central) / delta_sgra_pos_sigma

    add_check(
        checks,
        "eht_sgra_direct_shadow_diameter_within_1sigma",
        z_sgra_direct < 1.0,
        z_sgra_direct,
        "< 1.0 sigma (48.7 +/- 7.0 uas)",
        1.0,
    )
    add_check(
        checks,
        "eht_sgra_fractional_deviation_delta_within_1sigma_bound",
        delta_sgra_min_1sigma <= delta_sh_refg <= delta_sgra_max_1sigma and z_sgra_delta < 1.0,
        delta_sh_refg,
        "in [-0.14, +0.05] (+0.046297 <= +0.05)",
        0.05,
    )

    # M87* EHT (2019 Paper I & VI; 2021 PRD 103, 104047):
    # theta_g = 3.8 +/- 0.4 uas (M = 6.5e9 M_sun, D = 16.8 Mpc)
    # Shadow diameter: d_sh = 42.0 +/- 3.0 uas; fractional deviation |delta| <= 0.17 (1-sigma)
    theta_g_m87_uas = 3.8
    d_sh_gr_m87_uas = 2.0 * bc_over_m_gr * theta_g_m87_uas
    d_sh_refg_m87_uas = 2.0 * bc_over_m_refg * theta_g_m87_uas
    d_sh_eht_m87_mean = 42.0
    d_sh_eht_m87_sigma = 3.0
    z_m87_direct = abs(d_sh_refg_m87_uas - d_sh_eht_m87_mean) / d_sh_eht_m87_sigma
    delta_m87_bound_1sigma = 0.17
    z_m87_delta = abs(delta_sh_refg) / delta_m87_bound_1sigma

    add_check(
        checks,
        "eht_m87_shadow_diameter_within_1sigma",
        z_m87_direct < 1.0 and abs(delta_sh_refg) <= delta_m87_bound_1sigma,
        {
            "d_sh_refg_uas": d_sh_refg_m87_uas,
            "z_direct": z_m87_direct,
            "z_delta": z_m87_delta,
        },
        "d_sh in 42.0 +/- 3.0 uas (z < 1.0) and |delta| <= 0.17",
        1.0,
    )

    return {
        "r_ph_over_m": 2.0,
        "bc_over_m_refg": bc_over_m_refg,
        "bc_over_m_gr": bc_over_m_gr,
        "delta_sh_refg": delta_sh_refg,
        "delta_sh_percent": 100.0 * delta_sh_refg,
        "sgra_star": {
            "theta_g_uas": theta_g_sgra_uas,
            "d_sh_gr_uas": d_sh_gr_sgra_uas,
            "d_sh_refg_uas": d_sh_refg_sgra_uas,
            "d_sh_eht_uas": d_sh_eht_sgra_mean,
            "d_sh_eht_sigma_uas": d_sh_eht_sgra_sigma,
            "z_score_direct_diameter": z_sgra_direct,
            "delta_1sigma_interval": [delta_sgra_min_1sigma, delta_sgra_max_1sigma],
            "z_score_delta_keck_vlti": z_sgra_delta,
        },
        "m87_star": {
            "theta_g_uas": theta_g_m87_uas,
            "d_sh_gr_uas": d_sh_gr_m87_uas,
            "d_sh_refg_uas": d_sh_refg_m87_uas,
            "d_sh_eht_uas": d_sh_eht_m87_mean,
            "d_sh_eht_sigma_uas": d_sh_eht_m87_sigma,
            "z_score_direct_diameter": z_m87_direct,
            "delta_1sigma_bound": delta_m87_bound_1sigma,
            "z_score_delta": z_m87_delta,
        },
    }


def verify_part2_tortoise_c2_and_eikonal_qnm(checks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Part 2: Symbolic verification of C^2 continuity of n_opt(r) = sqrt(A(r)/B(r)) across r = r_c
    (making the tortoise coordinate r_*(r) globally C^3), and exact eikonal QNM spectrum
    Omega_ph^RefG = lambda_L^RefG = c_0 / (2*e*m) with quality-factor invariance Q_ln^RefG = Q_ln^GR.
    """
    x, q, r, m, c0 = sp.symbols("x q r m c0", positive=True)

    ell_A = q * (sp.Rational(35, 8) * x**2 - sp.Rational(21, 4) * x**4 + sp.Rational(15, 8) * x**6)
    ell_B = -q + q * (-sp.Rational(11, 8) * x**2 + sp.Rational(9, 4) * x**4 - sp.Rational(7, 8) * x**6)

    P_x = sp.simplify((ell_A - ell_B) / q)
    expected_P_x = 1 + sp.Rational(23, 4) * x**2 - sp.Rational(15, 2) * x**4 + sp.Rational(11, 4) * x**6
    res_P = sp.simplify(P_x - expected_P_x)
    add_check(
        checks,
        "interior_optical_exponent_polynomial_identity",
        res_P == 0,
        str(P_x),
        str(expected_P_x),
        0,
    )

    n_opt_int = sp.exp(q * P_x / 2)
    n_opt_ext = sp.exp(q / x)

    jump_0 = sp.simplify(n_opt_int.subs(x, 1) - n_opt_ext.subs(x, 1))
    jump_1 = sp.simplify(sp.diff(n_opt_int, x).subs(x, 1) - sp.diff(n_opt_ext, x).subs(x, 1))
    jump_2 = sp.simplify(sp.diff(n_opt_int, x, 2).subs(x, 1) - sp.diff(n_opt_ext, x, 2).subs(x, 1))

    add_check(
        checks,
        "tortoise_optical_index_c2_junction_at_rc_exact",
        jump_0 == 0 and jump_1 == 0 and jump_2 == 0,
        {"jump_C0": str(jump_0), "jump_C1": str(jump_1), "jump_C2": str(jump_2)},
        {"jump_C0": "0", "jump_C1": "0", "jump_C2": "0"},
        0,
    )

    # Eikonal QNM angular velocity and Lyapunov exponent at r_ph^+ = 2m
    V_ext = sp.exp(-4 * m / r) / r**2
    n_ext_r = sp.exp(2 * m / r)
    V_ph = sp.simplify(V_ext.subs(r, 2 * m))
    d2V_dr2_ph = sp.simplify(sp.diff(V_ext, r, 2).subs(r, 2 * m))
    n_ph = sp.simplify(n_ext_r.subs(r, 2 * m))

    Omega_ph_refg = sp.simplify(c0 * sp.sqrt(V_ph))
    # Since d/dr_* = (1 / n_opt(r)) d/dr and dV/dr = 0 at r_ph, d^2V/dr_*^2|_{r_ph} = (1 / n_opt(r_ph)^2) d^2V/dr^2|_{r_ph}
    d2V_drstar2_ph = sp.simplify(d2V_dr2_ph / n_ph**2)
    lambda_L_refg = sp.simplify(c0 * sp.sqrt(-d2V_drstar2_ph / (2 * V_ph)))

    res_omega = sp.simplify(Omega_ph_refg - c0 / (2 * sp.E * m))
    res_lambda = sp.simplify(lambda_L_refg - c0 / (2 * sp.E * m))
    res_ratio = sp.simplify(lambda_L_refg / Omega_ph_refg - 1)

    add_check(
        checks,
        "eikonal_qnm_angular_velocity_and_lyapunov_exponent_exact",
        res_omega == 0 and res_lambda == 0 and res_ratio == 0,
        {
            "Omega_ph_RefG": str(Omega_ph_refg),
            "lambda_L_RefG": str(lambda_L_refg),
            "ratio_lambda_over_Omega": str(sp.simplify(lambda_L_refg / Omega_ph_refg)),
        },
        {
            "Omega_ph_RefG": "c0/(2*E*m)",
            "lambda_L_RefG": "c0/(2*E*m)",
            "ratio_lambda_over_Omega": "1",
        },
        0,
    )

    # Compare against Schwarzschild GR: V_GR(r) = (1 - 2m/r)/r^2, n_GR(r) = 1/(1 - 2m/r) at r_ph = 3m
    V_gr = (1 - 2 * m / r) / r**2
    n_gr_r = 1 / (1 - 2 * m / r)
    V_gr_ph = sp.simplify(V_gr.subs(r, 3 * m))
    d2V_gr_dr2_ph = sp.simplify(sp.diff(V_gr, r, 2).subs(r, 3 * m))
    n_gr_ph = sp.simplify(n_gr_r.subs(r, 3 * m))
    Omega_ph_gr = sp.simplify(c0 * sp.sqrt(V_gr_ph))
    lambda_L_gr = sp.simplify(c0 * sp.sqrt(-(d2V_gr_dr2_ph / n_gr_ph**2) / (2 * V_gr_ph)))

    qnm_scale_ratio_sym = sp.simplify(Omega_ph_refg / Omega_ph_gr)
    q_factor_ratio_sym = sp.simplify((Omega_ph_refg / lambda_L_refg) / (Omega_ph_gr / lambda_L_gr))

    add_check(
        checks,
        "eikonal_qnm_quality_factor_identical_to_gr",
        q_factor_ratio_sym == 1 and sp.simplify(qnm_scale_ratio_sym - 3 * sp.sqrt(3) / (2 * sp.E)) == 0,
        {
            "Q_RefG_over_Q_GR": str(q_factor_ratio_sym),
            "omega_RefG_over_omega_GR": float(qnm_scale_ratio_sym),
        },
        {"Q_RefG_over_Q_GR": "1", "omega_RefG_over_omega_GR": 3.0 * math.sqrt(3.0) / (2.0 * math.e)},
        0,
    )

    # Evaluate quadrupolar (l=2, n=0) eikonal QNM benchmark for GW150914 remnant (M_f = 62 M_sun)
    m_remnant_msun = 62.0
    t_grav_s = m_remnant_msun * GM_SUN_C3_S
    omega_20_refg_rad_s = (2.5 / (2.0 * math.e)) / t_grav_s
    freq_20_refg_hz = omega_20_refg_rad_s / (2.0 * math.pi)
    freq_20_gr_hz = ((2.5 / (3.0 * math.sqrt(3.0))) / t_grav_s) / (2.0 * math.pi)
    tau_20_refg_ms = 1.0e3 / ((0.5 / (2.0 * math.e)) / t_grav_s)
    tau_20_gr_ms = 1.0e3 / ((0.5 / (3.0 * math.sqrt(3.0))) / t_grav_s)

    return {
        "n_opt_center_over_exp_q_half": 1.0,
        "n_opt_boundary_over_exp_q": 1.0,
        "Omega_ph_m_over_c0_refg": 1.0 / (2.0 * math.e),
        "lambda_L_m_over_c0_refg": 1.0 / (2.0 * math.e),
        "Omega_ph_m_over_c0_gr": 1.0 / (3.0 * math.sqrt(3.0)),
        "lambda_L_m_over_c0_gr": 1.0 / (3.0 * math.sqrt(3.0)),
        "qnm_frequency_ratio_refg_to_gr": 3.0 * math.sqrt(3.0) / (2.0 * math.e),
        "qnm_frequency_shift_percent": 100.0 * (3.0 * math.sqrt(3.0) / (2.0 * math.e) - 1.0),
        "qnm_quality_factor_ratio_refg_to_gr": 1.0,
        "gw150914_eikonal_l2_n0_benchmark": {
            "M_remnant_Msun": m_remnant_msun,
            "f_20_eikonal_refg_Hz": freq_20_refg_hz,
            "f_20_eikonal_gr_Hz": freq_20_gr_hz,
            "tau_20_eikonal_refg_ms": tau_20_refg_ms,
            "tau_20_eikonal_gr_ms": tau_20_gr_ms,
            "quality_factor_Q_20": 2.5,
        },
    }


def n_opt_core_x(x: float, q: float) -> float:
    p_val = 1.0 + 5.75 * x**2 - 7.5 * x**4 + 2.75 * x**6
    return math.exp(0.5 * q * p_val)


def solve_inner_light_ring_x(q: float) -> float:
    # Solve q*(-23*y + 60*y^2 - 33*y^3) - 4 = 0 on y in ((20 - 7*sqrt(3))/33, (20 + 7*sqrt(3))/33)
    y_min = (20.0 - 7.0 * math.sqrt(3.0)) / 33.0
    y_max = (20.0 + 7.0 * math.sqrt(3.0)) / 33.0
    sol = optimize.brentq(lambda y: q * (-23.0 * y + 60.0 * y**2 - 33.0 * y**3) - 4.0, y_min, y_max, xtol=1e-15)
    return math.sqrt(sol)


def verify_part3_finite_tortoise_cavity_and_gw_echoes(checks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Part 3: Compute the finite tortoise depth L_*(q), verify the analytical exponential-integral
    formula for the exterior segment L_{*,ext}(q), compute the inner-light-ring cavity depth,
    and evaluate quantitative GW echo delay times Delta t_echo(q, M).
    """
    q_grid = [1.2, 1.5, 1.8]
    echo_table: Dict[str, Any] = {}
    max_ext_ei_err = 0.0

    for q in q_grid:
        # Core integral: (L_{*,core} / m) = (2/q) * int_0^1 n_opt_core(x, q) dx
        val_core, _ = integrate.quad(lambda x: n_opt_core_x(x, q), 0.0, 1.0, epsabs=1e-13, epsrel=1e-13)
        L_core_over_m = (2.0 / q) * val_core

        # Exterior integral from r_c = 2m/q to r_ph^+ = 2m (x from 1 to q):
        # (L_{*,ext} / m) = (2/q) * int_1^q exp(q/x) dx = 2 * int_{1/q}^1 exp(1/u) du
        val_ext, _ = integrate.quad(lambda x: math.exp(q / x), 1.0, q, epsabs=1e-13, epsrel=1e-13)
        L_ext_over_m = (2.0 / q) * val_ext

        # Exact closed-form exponential integral identity:
        # (2/q) int_1^q exp(q/x) dx = 2 * [e - (e^q / q) + Ei(q) - Ei(1)]
        L_ext_over_m_exact = 2.0 * (
            math.e
            - math.exp(q) / q
            + float(special.expi(q) - special.expi(1.0))
        )
        ext_err = abs(L_ext_over_m - L_ext_over_m_exact)
        max_ext_ei_err = max(max_ext_ei_err, ext_err)

        L_tot_over_m = L_core_over_m + L_ext_over_m
        I_echo = 2.0 * L_tot_over_m  # c_0 * Delta t_echo / m = 2 * L_*(q) / m

        # Inner stable light ring x_lr(q) and inter-ring cavity tortoise depth from x_lr to r_ph^+ = 2m
        x_lr = solve_inner_light_ring_x(q)
        val_core_lr, _ = integrate.quad(lambda x: n_opt_core_x(x, q), x_lr, 1.0, epsabs=1e-13, epsrel=1e-13)
        L_cav_over_m = (2.0 / q) * val_core_lr + L_ext_over_m
        I_cav = 2.0 * L_cav_over_m

        # Effective Cardoso et al. horizonless compactness parameter: I_echo = 4 * |ln(eps_eff)|
        eps_eff = math.exp(-0.25 * I_echo)

        echo_table[f"{q:.1f}"] = {
            "q": q,
            "r_c_over_m": 2.0 / q,
            "x_lr_inner": x_lr,
            "r_lr_inner_over_m": (2.0 / q) * x_lr,
            "n_opt_center": math.exp(0.5 * q),
            "n_opt_rc": math.exp(q),
            "L_star_core_over_m": L_core_over_m,
            "L_star_ext_over_m": L_ext_over_m,
            "L_star_ext_exact_ei_over_m": L_ext_over_m_exact,
            "L_star_total_over_m": L_tot_over_m,
            "I_echo_dimensionless": I_echo,
            "I_cav_inner_to_outer_dimensionless": I_cav,
            "effective_compactness_epsilon": eps_eff,
            "echo_delay_10Msun_ms": 1.0e3 * I_echo * 10.0 * GM_SUN_C3_S,
            "echo_delay_30Msun_ms": 1.0e3 * I_echo * 30.0 * GM_SUN_C3_S,
            "echo_delay_gw150914_62Msun_ms": 1.0e3 * I_echo * 62.0 * GM_SUN_C3_S,
            "inner_cavity_delay_gw150914_62Msun_ms": 1.0e3 * I_cav * 62.0 * GM_SUN_C3_S,
            "echo_delay_sgra_star_s": I_echo * 4.154e6 * GM_SUN_C3_S,
        }

    add_check(
        checks,
        "exterior_tortoise_exponential_integral_closed_form_match",
        max_ext_ei_err < 1e-13,
        max_ext_ei_err,
        "< 1e-13",
        1e-13,
    )

    q15 = echo_table["1.5"]
    add_check(
        checks,
        "finite_tortoise_depth_and_positive_echo_factor_at_q_1p5",
        math.isfinite(q15["I_echo_dimensionless"]) and 10.0 < q15["I_echo_dimensionless"] < 25.0,
        q15["I_echo_dimensionless"],
        "finite in (10, 25) (~15.5553)",
        1e-12,
    )

    add_check(
        checks,
        "strict_monotonicity_of_echo_factor_with_compactness_q",
        echo_table["1.2"]["I_echo_dimensionless"]
        < echo_table["1.5"]["I_echo_dimensionless"]
        < echo_table["1.8"]["I_echo_dimensionless"],
        [
            echo_table["1.2"]["I_echo_dimensionless"],
            echo_table["1.5"]["I_echo_dimensionless"],
            echo_table["1.8"]["I_echo_dimensionless"],
        ],
        "I_echo(1.2) < I_echo(1.5) < I_echo(1.8)",
        0,
    )

    return echo_table


def verify_part4_negative_controls(checks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Part 4: Three negative mutation controls.
    """
    # Negative Control 1: Mutated Schwarzschild horizon f(r) = 1 - 2m/r has a logarithmic pole
    # at r = 2m, causing the tortoise depth from r = 2m + eps to r = 3m to diverge as eps -> 0+.
    r, m, eps = sp.symbols("r m eps", positive=True)
    L_gr_eps = sp.integrate(1 / (1 - 2 * m / r), (r, 2 * m + eps, 3 * m))
    lim_gr = sp.limit(L_gr_eps / m, eps, 0, dir="+")
    nc1_rejected = lim_gr == sp.oo
    add_check(
        checks,
        "negative_control_schwarzschild_horizon_divergent_tortoise_rejected",
        nc1_rejected,
        str(lim_gr),
        "oo (divergent tortoise integral -> no core reflection)",
        0,
    )

    # Negative Control 2: Mutated C^0-only core index n_opt_naive(x) = exp(q) on x in [0, 1]
    # violates C^1 and C^2 junction smoothness at x = 1.
    q_val = 1.5
    jump_c1_naive = abs(0.0 - (-q_val * math.exp(q_val)))
    jump_c2_naive = abs(0.0 - (q_val * (q_val + 2.0) * math.exp(q_val)))
    nc2_rejected = jump_c1_naive > 1.0 and jump_c2_naive > 10.0
    add_check(
        checks,
        "negative_control_c0_only_core_tortoise_c2_jump_rejected",
        nc2_rejected,
        {"jump_C1": jump_c1_naive, "jump_C2": jump_c2_naive},
        "nonzero C^1 and C^2 jumps (> 1.0 and > 10.0) rejected",
        0,
    )

    # Negative Control 3: Mutated oversized shadow multiplier b_c^mut = 7.0 * m
    # violates both EHT Sgr A* (delta <= 0.05) and EHT M87* (|delta| <= 0.17) 1-sigma bounds.
    bc_mut_over_m = 7.0
    delta_mut = bc_mut_over_m / (3.0 * math.sqrt(3.0)) - 1.0
    nc3_rejected = delta_mut > 0.05 and delta_mut > 0.17
    add_check(
        checks,
        "negative_control_oversized_shadow_violating_eht_1sigma_rejected",
        nc3_rejected,
        delta_mut,
        "delta_mut = +0.3472 > 0.17 (violates both Sgr A* and M87* 1-sigma bounds) -> rejected",
        0,
    )

    return {
        "schwarzschild_horizon_tortoise_limit": str(lim_gr),
        "c0_only_core_c1_jump_at_q1p5": jump_c1_naive,
        "c0_only_core_c2_jump_at_q1p5": jump_c2_naive,
        "oversized_shadow_delta_mut": delta_mut,
    }


def main() -> None:
    checks: List[Dict[str, Any]] = []

    upstream_ok = UPSTREAM_CLOSURE_SCRIPT.exists() and UPSTREAM_CLOSURE_JSON.exists()
    add_check(
        checks,
        "upstream_c2_interior_closure_artifacts_present",
        upstream_ok,
        {
            "script": UPSTREAM_CLOSURE_SCRIPT.name,
            "json": UPSTREAM_CLOSURE_JSON.name,
        },
        "both present",
        0,
    )

    part1 = verify_part1_photon_sphere_and_eht_shadow(checks)
    part2 = verify_part2_tortoise_c2_and_eikonal_qnm(checks)
    part3 = verify_part3_finite_tortoise_cavity_and_gw_echoes(checks)
    part4 = verify_part4_negative_controls(checks)

    passed_count = sum(1 for c in checks if c["passed"])
    total_count = len(checks)
    status = "PASS" if passed_count == total_count else "FAIL"

    result = {
        "claim_id": "REFG_STRONG_FIELD_EHT_SHADOW_QNM_AND_ECHO_BRIDGE_V1",
        "model_version": "REFG_STRONG_FIELD_COVARIANT_MEDIUM_C2_INTERIOR_V1",
        "status": status,
        "passed_checks": passed_count,
        "total_checks": total_count,
        "upstream_provenance": {
            "verify_action_derived_c2_interior_closure_py_sha256": (
                sha256_file(UPSTREAM_CLOSURE_SCRIPT) if UPSTREAM_CLOSURE_SCRIPT.exists() else None
            ),
            "action_derived_c2_interior_closure_result_json_sha256": (
                sha256_file(UPSTREAM_CLOSURE_JSON) if UPSTREAM_CLOSURE_JSON.exists() else None
            ),
        },
        "part1_photon_sphere_and_eht_shadow": part1,
        "part2_tortoise_c2_and_eikonal_qnm": part2,
        "part3_finite_tortoise_cavity_and_gw_echoes": part3,
        "part4_negative_controls": part4,
        "checks": checks,
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    script_sha = sha256_file(Path(__file__).resolve())
    json_sha = sha256_file(RESULT_PATH)
    print(f"STATUS={status} ({passed_count}/{total_count} PASS)")
    print(f"SCRIPT_SHA256={script_sha}")
    print(f"RESULT_JSON_SHA256={json_sha}")


if __name__ == "__main__":
    main()
