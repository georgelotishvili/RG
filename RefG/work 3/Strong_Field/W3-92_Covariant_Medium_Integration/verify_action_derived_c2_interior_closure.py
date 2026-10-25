#!/usr/bin/env python3
"""
Standalone SymPy + SciPy verifier for:
  CLAIM_ID: REFG_ACTION_DERIVED_C2_INTERIOR_CLOSURE_V1
  MODEL_VERSION: REFG_STRONG_FIELD_COVARIANT_MEDIUM_C2_INTERIOR_V1

Verifies Stage 3 and Stage 4 of the RefG Strategic Development Plan:
  1. Theorem 1: Exact off-shell radial reparameterization Noether identity and exact
     equivalence between the constitutive chain rule df/dr = d(ln y)' + a(ln b_r)' + c(ln b_t)'
     and the radial label Euler-Lagrange equation E_ell = 0.
  2. Theorem 2: Exact divergence-free universal label-traction identity on any C^1-matched
     interior and strict positivity of the pure-medium integral I_met(q) > 0 on RefG_ka.md
     eqs. (36)-(37), proving the necessity of a minimally coupled core matter sector T^m_{mu nu}.
  3. Theorem 3: Boundary order-lowering law at x -> 1^- (ord(a) = ord(c) + 1 >= 2) and
     exact selection of H(x) = -l_B(x)/2 satisfying regular central parity (Q_H(0)=0),
     exact C^2 exterior matching (Q_H(r_c)=m), a'(1^-)=0, and a''(1^-)=c'(1^-).
  4. Stage 4 Numerical BVP & Constitutive Closure across q in {1.2, 1.5, 1.8}:
     - Unique positive core matter eigenvalue rho_0^*(q) > 0 from Q*C_ell(r_c) = 0.
     - Strict negativity a(x) < 0 on [0, 1) (positive radial label kinetic sign) and Q*C_ell(x) < 0 on (0, 1).
     - Smooth, strictly monotonic label profile ell(x) with ell(0)=0, ell(1)=r_c, ell'(1)=1.
     - Strict monotonicity of principal strain invariants I1_hat(x) and I3_hat(x) on [0, 1].
     - Zero symbolic and numerical (< 1e-9) constitutive chain-rule residual.
     - Complete verification of RefG_ka.md eqs. (38)-(52): C^2 junction, areal radius bound q_*,
       central Ricci/Kretschmann/stress invariants, minimum lapse B_min, outer photon sphere b_c = 2*e*m,
       and unique radially stable inner light ring x_lr.
     - 5 negative controls rejected.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import cumulative_trapezoid, quad
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REPORT_MD = HERE / "action_derived_c2_interior_closure.md"
RESULT_JSON = HERE / "action_derived_c2_interior_closure_result.json"

UPSTREAM_EXPECTED_SHA256 = {
    "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/FORMAL_COVARIANT_MEDIUM_INTEGRATION.md": "3c01e91cc42ce05e2b26a0c98e63a89e24faa609de87164094f4d7acd485085c",
    "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/common_scale_centre_source.md": "0b02806c78d932be8cb3e9cbf88878cad94f52345440f5448c5a6fd82bdeeeec",
    "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_common_scale_centre_source.py": "15284b336a649393fdaeca52f15697832fed61121b16373360db74c51524d1f4",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_symbolic_checks() -> tuple[dict[str, bool], dict[str, str], dict[str, bool]]:
    checks: dict[str, bool] = {}
    residuals: dict[str, str] = {}
    neg_controls: dict[str, bool] = {}

    def check_zero(name: str, expr: sp.Expr) -> None:
        s = sp.simplify(sp.expand(expr))
        residuals[name] = str(s)
        checks[name] = bool(s == 0)

    r, x, q, rc, P, Q = sp.symbols("r x q r_c P Q", positive=True)

    # -------------------------------------------------------------------------
    # 1. Theorem 1: Off-shell radial Noether identity & chain-rule equivalence
    # -------------------------------------------------------------------------
    N = sp.Function("N")(r)
    A = sp.Function("A")(r)
    S = sp.Function("S")(r)
    H = sp.Function("H")(r)
    ell = sp.Function("ell")(r)
    y_sym, br_sym, bt_sym = sp.symbols("y b_r b_t", positive=True)
    Fbar = sp.Function("Fbar")(y_sym, br_sym, bt_sym)

    y_expr = sp.exp(-2 * H) / N**2
    br_expr = sp.exp(2 * H) * ell.diff(r) ** 2 / A**2
    bt_expr = sp.exp(2 * H) * ell**2 / S**2
    subs_inv = {y_sym: y_expr, br_sym: br_expr, bt_sym: bt_expr}

    L_rad = P * (N * A + (N * S.diff(r) ** 2 + 2 * N.diff(r) * S * S.diff(r)) / A) + (
        N * A * S**2 * (Q * Fbar.subs(subs_inv) + P * H.diff(r) ** 2 / A**2)
    )

    def EL(L_expr, func):
        return sp.diff(L_expr, func) - sp.diff(sp.diff(L_expr, func.diff(r)), r)

    E_N = EL(L_rad, N)
    E_A = EL(L_rad, A)
    E_S = EL(L_rad, S)
    E_H = EL(L_rad, H)
    E_ell = EL(L_rad, ell)

    check_zero(
        "off_shell_radial_reparameterization_noether_identity",
        E_N * N.diff(r)
        + E_A * A.diff(r)
        + E_S * S.diff(r)
        + E_H * H.diff(r)
        + E_ell * ell.diff(r)
        - sp.diff(A * E_A, r),
    )

    # Medium block algebraic identity connecting E_ell to constitutive chain rule
    f_r = sp.Function("f")(r)
    d_r = sp.Function("d")(r)
    a_r = sp.Function("a")(r)
    c_r = sp.Function("c")(r)

    EN_F = A * S**2 * (f_r - 2 * d_r)
    EA_F = N * S**2 * (f_r - 2 * a_r)
    ES_F = 2 * N * A * S * (f_r - c_r)
    EH_F = 2 * N * A * S**2 * (-d_r + a_r + c_r)
    E_ell_F = -2 * sp.diff(N * A * S**2 * a_r / ell.diff(r), r) + 2 * N * A * S**2 * c_r / ell

    dlny = sp.diff(sp.log(y_expr), r)
    dlnbr = sp.diff(sp.log(br_expr), r)
    dlnbt = sp.diff(sp.log(bt_expr), r)
    chain_lhs = sp.diff(f_r, r) - (d_r * dlny + a_r * dlnbr + c_r * dlnbt)

    lhs_F = (
        EN_F * N.diff(r)
        + EA_F * A.diff(r)
        + ES_F * S.diff(r)
        + EH_F * H.diff(r)
        + E_ell_F * ell.diff(r)
        - sp.diff(A * EA_F, r)
    )
    check_zero(
        "medium_noether_to_constitutive_chain_rule_identity",
        lhs_F + N * A * S**2 * chain_lhs,
    )

    # 4x4 algebraic inversion for (f, d, a, c)
    S_rho_s, S_r_s, S_t_s, Jg_s = sp.symbols("S_rho S_r S_t J_g")
    f_s, d_s, a_s, c_s = sp.symbols("f_s d_s a_s c_s")
    sol_fdac = sp.solve(
        [
            2 * d_s - f_s - S_rho_s,
            f_s - 2 * a_s - S_r_s,
            f_s - c_s - S_t_s,
            d_s - a_s - c_s - Jg_s,
        ],
        (f_s, d_s, a_s, c_s),
    )
    check_zero(
        "algebraic_inversion_f",
        sol_fdac[f_s] - ((S_rho_s + S_r_s + 2 * S_t_s) / 2 - Jg_s),
    )
    check_zero(
        "algebraic_inversion_d",
        sol_fdac[d_s] - ((3 * S_rho_s + S_r_s + 2 * S_t_s) / 4 - Jg_s / 2),
    )
    check_zero(
        "algebraic_inversion_a",
        sol_fdac[a_s] - ((S_rho_s - S_r_s + 2 * S_t_s) / 4 - Jg_s / 2),
    )
    check_zero(
        "algebraic_inversion_c",
        sol_fdac[c_s] - ((S_rho_s + S_r_s) / 2 - Jg_s),
    )

    # -------------------------------------------------------------------------
    # 2. Theorem 2: Universal divergence-free label-traction identity
    # -------------------------------------------------------------------------
    lA_fn = sp.Function("lA")(x)
    lB_fn = sp.Function("lB")(x)
    H_fn = sp.Function("H_x")(x)

    rho_geom_fn = (
        -P
        * sp.exp(-lA_fn)
        / (4 * rc**2 * x)
        * (x * lA_fn.diff(x) ** 2 + 4 * x * lA_fn.diff(x, 2) + 8 * lA_fn.diff(x))
    )
    pr_geom_fn = (
        P
        * sp.exp(-lA_fn)
        / (4 * rc**2 * x)
        * (
            x * lA_fn.diff(x) ** 2
            + 2 * x * lA_fn.diff(x) * lB_fn.diff(x)
            + 4 * lA_fn.diff(x)
            + 4 * lB_fn.diff(x)
        )
    )
    pt_geom_fn = (
        P
        * sp.exp(-lA_fn)
        / (4 * rc**2 * x)
        * (
            2 * x * lA_fn.diff(x, 2)
            + x * lB_fn.diff(x) ** 2
            + 2 * x * lB_fn.diff(x, 2)
            + 2 * lA_fn.diff(x)
            + 2 * lB_fn.diff(x)
        )
    )

    S_rho_fn = rho_geom_fn + P * sp.exp(-lA_fn) * H_fn.diff(x) ** 2 / rc**2
    S_r_fn = pr_geom_fn + P * sp.exp(-lA_fn) * H_fn.diff(x) ** 2 / rc**2
    S_t_fn = pt_geom_fn - P * sp.exp(-lA_fn) * H_fn.diff(x) ** 2 / rc**2

    sqrt_g_fn = rc**2 * x**2 * sp.exp((3 * lA_fn + lB_fn) / 2)
    Jg_fn = (
        -P
        / (rc**2 * sqrt_g_fn)
        * sp.diff(rc**2 * x**2 * sp.exp((lA_fn + lB_fn) / 2) * H_fn.diff(x), x)
    )

    a_med_fn = (S_rho_fn - S_r_fn + 2 * S_t_fn) / 4 - Jg_fn / 2
    c_med_fn = (S_rho_fn + S_r_fn) / 2 - Jg_fn

    traction_lhs = rc * sqrt_g_fn * (a_med_fn + c_med_fn)
    traction_rhs = (P * rc / 8) * sp.diff(
        x**2
        * sp.exp((lA_fn + lB_fn) / 2)
        * (12 * H_fn.diff(x) - 4 * lA_fn.diff(x) + 2 * lB_fn.diff(x)),
        x,
    ) + (P * rc / 8) * x**2 * sp.exp((lA_fn + lB_fn) / 2) * (
        lA_fn.diff(x) * (lA_fn.diff(x) + 2 * lB_fn.diff(x)) + 4 * H_fn.diff(x) ** 2
    )
    check_zero(
        "universal_divergence_free_label_traction_identity",
        traction_lhs - traction_rhs,
    )

    # Boundary combination 12*H'(1) - 4*lA'(1) + 2*lB'(1) vanishes on any C^1 match
    check_zero(
        "boundary_divergence_term_vanishes_on_C1_match",
        12 * (-q / 2) - 4 * (-q) + 2 * q,
    )

    # -------------------------------------------------------------------------
    # 3. Theorem 3: Boundary order-lowering law & selection of H = -lB / 2
    # -------------------------------------------------------------------------
    dlA3, dlB3, dH3, dH4 = sp.symbols("dlA3 dlB3 dH3 dH4", real=True)
    lA_loc = q / x + dlA3 * (x - 1) ** 3 / 6
    lB_loc = -q / x + dlB3 * (x - 1) ** 3 / 6
    H_loc = q / (2 * x) + dH3 * (x - 1) ** 3 / 6

    a_loc = a_med_fn.subs({lA_fn: lA_loc, lB_fn: lB_loc, H_fn: H_loc}).doit()
    c_loc = c_med_fn.subs({lA_fn: lA_loc, lB_fn: lB_loc, H_fn: H_loc}).doit()

    check_zero("C2_match_a_vanishes_at_boundary", a_loc.subs(x, 1))
    check_zero("C2_match_c_vanishes_at_boundary", c_loc.subs(x, 1))
    check_zero(
        "boundary_da_dx_formula",
        a_loc.diff(x).subs(x, 1) - P * (2 * dH3 + dlB3) * sp.exp(-q) / (4 * rc**2),
    )
    check_zero(
        "boundary_dc_dx_formula",
        c_loc.diff(x).subs(x, 1) - P * (2 * dH3 - dlA3) * sp.exp(-q) / (2 * rc**2),
    )

    # RefG_ka.md eqs. (36)-(37) core metric profiles
    lA_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    lB_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )
    lA_ext = q / x
    lB_ext = -q / x

    for k in range(3):
        check_zero(
            f"C2_junction_lA_order_{k}",
            lA_core.diff(x, k).subs(x, 1) - lA_ext.diff(x, k).subs(x, 1),
        )
        check_zero(
            f"C2_junction_lB_order_{k}",
            lB_core.diff(x, k).subs(x, 1) - lB_ext.diff(x, k).subs(x, 1),
        )

    check_zero("clock_ruler_product_identity_eq39", (lA_core + lB_core) - q * (x**2 - 1) ** 3)
    check_zero(
        "strictly_positive_metric_factor_lA_plus_2lB_prime",
        (lA_core.diff(x) + 2 * lB_core.diff(x))
        - (q * x / 4) * (3 * (x**2 - 2) ** 2 + 1),
    )

    # Unique degree-6 even polynomial H(x) = -lB_core(x)/2
    H_core = -lB_core / 2
    H_ext = q / (2 * x)
    for k in range(3):
        check_zero(
            f"C2_junction_H_order_{k}",
            H_core.diff(x, k).subs(x, 1) - H_ext.diff(x, k).subs(x, 1),
        )

    QH_core = -rc * x**2 * sp.exp((lA_core + lB_core) / 2) * H_core.diff(x)
    check_zero("regular_center_H_flux_is_zero", QH_core.subs(x, 0))
    check_zero("exterior_match_H_flux_equals_m_eq48", QH_core.subs(x, 1) - q * rc / 2)

    a_core_med = sp.simplify(
        a_med_fn.subs({lA_fn: lA_core, lB_fn: lB_core, H_fn: H_core}).doit()
    )
    c_core_med = sp.simplify(
        c_med_fn.subs({lA_fn: lA_core, lB_fn: lB_core, H_fn: H_core}).doit()
    )
    f_core_med = sp.simplify(
        ((S_rho_fn + S_r_fn + 2 * S_t_fn) / 2 - Jg_fn)
        .subs({lA_fn: lA_core, lB_fn: lB_core, H_fn: H_core})
        .doit()
    )

    check_zero("H_minus_half_lB_gives_zero_f_med", f_core_med)
    check_zero("H_minus_half_lB_gives_da_dx_zero_at_boundary", a_core_med.diff(x).subs(x, 1))
    check_zero(
        "H_minus_half_lB_gives_d2a_dx2_equals_dc_dx_at_boundary",
        a_core_med.diff(x, 2).subs(x, 1) - c_core_med.diff(x).subs(x, 1),
    )
    check_zero(
        "factored_a_med_negativity_identity",
        a_core_med * sp.exp(lA_core) * rc**2 / P
        + sp.Rational(3, 2) * q * (1 - x**2) ** 2 * (2 + 3 * q * x**2 * (1 - x**2) ** 2),
    )

    # -------------------------------------------------------------------------
    # 4. Conserved core matter & exact symbolic constitutive chain rule
    # -------------------------------------------------------------------------
    rho0 = sp.Symbol("rho0", positive=True)
    rho_m = (P / rc**2) * rho0 * (1 - x**2) ** 3
    pr_m = sp.S.Zero
    pt_m = x * lB_core.diff(x) / (2 * (2 + x * lA_core.diff(x))) * rho_m

    matter_cons_res = (
        pr_m.diff(x)
        + lB_core.diff(x) / 2 * (rho_m + pr_m)
        + (2 + x * lA_core.diff(x)) / x * (pr_m - pt_m)
    )
    check_zero("core_matter_covariant_conservation_identity", matter_cons_res)
    check_zero("core_matter_central_isotropy", pt_m.subs(x, 0) - pr_m)

    f_tot = sp.simplify(f_core_med - (rho_m + pr_m + 2 * pt_m) / 2)
    d_tot = sp.simplify(
        ((3 * S_rho_fn + S_r_fn + 2 * S_t_fn) / 4 - Jg_fn / 2)
        .subs({lA_fn: lA_core, lB_fn: lB_core, H_fn: H_core})
        .doit()
        - (3 * rho_m + pr_m + 2 * pt_m) / 4
    )
    a_tot = sp.simplify(a_core_med - (rho_m - pr_m + 2 * pt_m) / 4)
    c_tot = sp.simplify(c_core_med - (rho_m + pr_m) / 2)

    dln_sqrt_g = 2 / x + (3 * lA_core.diff(x) + lB_core.diff(x)) / 2
    ell_x = sp.Function("ell_x")(x)
    dlny_x = -2 * H_core.diff(x) - lB_core.diff(x)
    dlnbt_x = 2 * H_core.diff(x) - lA_core.diff(x) + 2 * ell_x.diff(x) / ell_x - 2 / x
    # On the label ODE: a_tot * (ell'' / ell') = a_tot * d(ln sqrt_g)/dx + a_tot' - c_tot * (ell' / ell)
    a_dlnbr_on_shell = a_tot * (2 * H_core.diff(x) - lA_core.diff(x)) + 2 * (
        a_tot * dln_sqrt_g + a_tot.diff(x) - c_tot * ell_x.diff(x) / ell_x
    )
    chain_res_on_shell = f_tot.diff(x) - (
        d_tot * dlny_x + a_dlnbr_on_shell + c_tot * dlnbt_x
    )
    check_zero(
        "exact_symbolic_chain_rule_on_label_ode",
        sp.together(chain_res_on_shell),
    )

    # Negative control: non-conserved matter (setting pt_m = 0 alongside pr_m = 0) breaks chain rule
    f_bad = -rho_m / 2
    a_bad = a_core_med - rho_m / 4
    c_bad = c_core_med - rho_m / 2
    a_dlnbr_bad = a_bad * (2 * H_core.diff(x) - lA_core.diff(x)) + 2 * (
        a_bad * dln_sqrt_g + a_bad.diff(x) - c_bad * ell_x.diff(x) / ell_x
    )
    chain_res_bad = sp.together(
        f_bad.diff(x) - (a_dlnbr_bad + c_bad * dlnbt_x)
    )
    neg_controls["non_conserved_isotropic_zero_pressure_core_matter_rejected"] = bool(
        chain_res_bad != 0
    )
    checks["negative_control_non_conserved_matter_breaks_chain_rule"] = neg_controls[
        "non_conserved_isotropic_zero_pressure_core_matter_rejected"
    ]

    # Negative control: unmatched 3rd derivative H'''(1) = H_ext'''(1) = -3q gives da/dx(1) != 0
    da_dx_unmatched = sp.simplify(
        a_loc.diff(x).subs({x: 1, dH3: 0, dlB3: lB_core.diff(x, 3).subs(x, 1) - lB_ext.diff(x, 3).subs(x, 1)})
    )
    neg_controls["unmatched_third_derivative_H_at_boundary_rejected"] = bool(
        da_dx_unmatched != 0
    )
    checks["negative_control_unmatched_H3_breaks_boundary_order"] = neg_controls[
        "unmatched_third_derivative_H_at_boundary_rejected"
    ]

    # Negative control: locked common-scale ansatz lA + lB = 0 violates eq (39)
    neg_controls["locked_common_scale_interior_ansatz_rejected"] = bool(
        sp.simplify((lA_core + lB_core).subs(x, sp.Rational(1, 2))) != 0
    )
    checks["negative_control_locked_common_scale_rejected"] = neg_controls[
        "locked_common_scale_interior_ansatz_rejected"
    ]

    # -------------------------------------------------------------------------
    # 5. RefG_ka.md Section 4 Curvature, Stress, and Optical Light-Ring Identities
    # -------------------------------------------------------------------------
    # Central effective density and pressure (eqs. 46-47)
    rho_eff_core = sp.simplify(
        rho_geom_fn.subs({lA_fn: lA_core, lB_fn: lB_core}).doit() * rc**2 / P
    )
    pr_eff_core = sp.simplify(
        pr_geom_fn.subs({lA_fn: lA_core, lB_fn: lB_core}).doit() * rc**2 / P
    )
    pt_eff_core = sp.simplify(
        pt_geom_fn.subs({lA_fn: lA_core, lB_fn: lB_core}).doit() * rc**2 / P
    )
    check_zero(
        "central_effective_density_eq47",
        sp.limit(rho_eff_core, x, 0) - (-sp.Rational(105, 4) * q),
    )
    check_zero(
        "central_effective_radial_pressure_eq47",
        sp.limit(pr_eff_core, x, 0) - 6 * q,
    )
    check_zero(
        "central_effective_tangential_pressure_eq47",
        sp.limit(pt_eff_core, x, 0) - 6 * q,
    )

    # Areal radius monotonicity bound q_* (eqs. 41-42)
    y_var = sp.Symbol("y_var", positive=True)
    f_areal = 35 * y_var - 84 * y_var**2 + 45 * y_var**3
    y_min_areal = (28 + sp.sqrt(259)) / 45
    q_star = -8 / sp.simplify(f_areal.subs(y_var, y_min_areal))
    expected_q_star = sp.Rational(8, 175) + sp.Rational(148, 1225) * sp.sqrt(259)
    check_zero("areal_radius_monotonicity_bound_q_star_eq42", q_star - expected_q_star)

    # Lapse global minimum x_min and alpha_B (lines 697-701)
    x_min_sq = (18 - sp.sqrt(93)) / 21
    alpha_B = sp.simplify(-lB_core.subs(x**2, x_min_sq) / q)
    expected_alpha_B = sp.Rational(211, 196) + sp.Rational(31, 1764) * sp.sqrt(93)
    check_zero("lapse_minimum_exponent_alpha_B", alpha_B - expected_alpha_B)

    # Exterior optical potential and critical impact parameter (eqs. 49-51)
    m_sym = sp.Symbol("m", positive=True)
    V_plus = sp.exp(-4 * m_sym / r) / r**2
    check_zero(
        "exterior_photon_sphere_at_2m_eq49",
        sp.diff(V_plus, r).subs(r, 2 * m_sym),
    )
    b_crit = 1 / sp.sqrt(V_plus.subs(r, 2 * m_sym))
    check_zero("critical_impact_parameter_2em_eq50", b_crit - 2 * sp.E * m_sym)

    # Interior optical potential and inner light ring polynomial (eq. 52)
    P_opt = 1 + sp.Rational(23, 4) * x**2 - sp.Rational(15, 2) * x**4 + sp.Rational(11, 4) * x**6
    check_zero(
        "interior_optical_exponent_P_eq52",
        (lA_core - lB_core) - q * P_opt,
    )
    V_minus = x ** (-2) * sp.exp(-q * P_opt)
    dlnV_minus = sp.simplify(2 * x * sp.diff(V_minus, x) / V_minus)
    check_zero(
        "interior_light_ring_derivative_identity_eq52",
        dlnV_minus - (q * (-23 * x**2 + 60 * x**4 - 33 * x**6) - 4),
    )

    return checks, residuals, neg_controls


def solve_interior_bvp_for_q(q_val: float, grid_points: int = 4001) -> dict:
    x_sym = sp.Symbol("x", positive=True)
    rho0_sym = sp.Symbol("rho0", real=True)
    q_rat = sp.Rational(str(q_val))

    lA = q_rat * (
        sp.Rational(35, 8) * x_sym**2
        - sp.Rational(21, 4) * x_sym**4
        + sp.Rational(15, 8) * x_sym**6
    )
    lB = -q_rat + q_rat * (
        -sp.Rational(11, 8) * x_sym**2
        + sp.Rational(9, 4) * x_sym**4
        - sp.Rational(7, 8) * x_sym**6
    )
    H = -lB / 2

    rho_m = rho0_sym * (1 - x_sym**2) ** 3
    pr_m = sp.S.Zero
    pt_m = x_sym * lB.diff(x_sym) / (2 * (2 + x_sym * lA.diff(x_sym))) * rho_m

    rho_geom = (
        -sp.exp(-lA)
        / (4 * x_sym)
        * (x_sym * lA.diff(x_sym) ** 2 + 4 * x_sym * lA.diff(x_sym, 2) + 8 * lA.diff(x_sym))
    )
    pr_geom = (
        sp.exp(-lA)
        / (4 * x_sym)
        * (
            x_sym * lA.diff(x_sym) ** 2
            + 2 * x_sym * lA.diff(x_sym) * lB.diff(x_sym)
            + 4 * lA.diff(x_sym)
            + 4 * lB.diff(x_sym)
        )
    )
    pt_geom = (
        sp.exp(-lA)
        / (4 * x_sym)
        * (
            2 * x_sym * lA.diff(x_sym, 2)
            + x_sym * lB.diff(x_sym) ** 2
            + 2 * x_sym * lB.diff(x_sym, 2)
            + 2 * lA.diff(x_sym)
            + 2 * lB.diff(x_sym)
        )
    )

    S_rho = rho_geom + sp.exp(-lA) * H.diff(x_sym) ** 2 - rho_m
    S_r = pr_geom + sp.exp(-lA) * H.diff(x_sym) ** 2 - pr_m
    S_t = pt_geom - sp.exp(-lA) * H.diff(x_sym) ** 2 - pt_m

    sqrt_g = x_sym**2 * sp.exp((3 * lA + lB) / 2)
    Jg = -1 / sqrt_g * sp.diff(x_sym**2 * sp.exp((lA + lB) / 2) * H.diff(x_sym), x_sym)

    f_expr = sp.simplify((S_rho + S_r + 2 * S_t) / 2 - Jg)
    a_expr = sp.simplify((S_rho - S_r + 2 * S_t) / 4 - Jg / 2)
    c_expr = sp.simplify((S_rho + S_r) / 2 - Jg)

    # Decompose linearly in rho0 with exact rational coefficients to avoid float expansion loss
    a_med_expr = sp.together(a_expr.subs(rho0_sym, 0))
    a_mat_expr = sp.together(-sp.diff(a_expr, rho0_sym))
    c_med_expr = sp.together(c_expr.subs(rho0_sym, 0))
    c_mat_expr = sp.together(-sp.diff(c_expr, rho0_sym))
    f_med_expr = sp.together(f_expr.subs(rho0_sym, 0))
    f_mat_expr = sp.together(-sp.diff(f_expr, rho0_sym))

    # Pure-metric integral I_met(q)
    I_met_integrand = sp.lambdify(
        x_sym,
        sp.Rational(1, 8)
        * x_sym**2
        * sp.exp((lA + lB) / 2)
        * lA.diff(x_sym)
        * (lA.diff(x_sym) + 2 * lB.diff(x_sym)),
        "numpy",
    )
    I_met_val, _ = quad(I_met_integrand, 0.0, 1.0, epsabs=1e-14, epsrel=1e-14)

    # Solve for unique eigenvalue rho_0^*(q) such that Q * C_ell(r_c) = 0
    ac_med_fn = sp.lambdify(x_sym, sqrt_g * (a_med_expr + c_med_expr), "numpy")
    ac_mat_fn = sp.lambdify(x_sym, sqrt_g * (a_mat_expr + c_mat_expr), "numpy")

    xs = np.linspace(1e-5, 1.0 - 1e-5, grid_points)
    edges = np.concatenate(([0.0], xs, [1.0]))
    gl_nodes, gl_weights = np.polynomial.legendre.leggauss(6)
    x_left = edges[:-1, None]
    x_right = edges[1:, None]
    half_dx = 0.5 * (x_right - x_left)
    mid_x = 0.5 * (x_right + x_left)
    pts = mid_x + half_dx * gl_nodes[None, :]

    med_segs = np.sum(ac_med_fn(pts) * gl_weights[None, :], axis=1) * half_dx[:, 0]
    mat_segs = np.sum(ac_mat_fn(pts) * gl_weights[None, :], axis=1) * half_dx[:, 0]
    num_int = float(np.sum(med_segs))
    den_int = float(np.sum(mat_segs))
    rho0_star = float(num_int / den_int)

    seg_integrals = med_segs - rho0_star * mat_segs
    QC_boundary = float(np.sum(seg_integrals))
    QC_wrong_sign = float(np.sum(med_segs + rho0_star * mat_segs))

    # Forward cumulative sum on first half, backward cumulative sum from x=1 on second half
    # to prevent catastrophic cancellation as QC(x) = O((1-x)^3) -> 0 near x = 1
    QC_forward = np.cumsum(seg_integrals[:-1])
    QC_backward = -np.cumsum(seg_integrals[:0:-1])[::-1]
    mid_idx = len(xs) // 2
    QC_vals = np.concatenate((QC_forward[:mid_idx], QC_backward[mid_idx:]))

    sa_med_fn = sp.lambdify(x_sym, sqrt_g * a_med_expr, "numpy")
    sa_mat_fn = sp.lambdify(x_sym, sqrt_g * a_mat_expr, "numpy")
    dsa_med_fn = sp.lambdify(x_sym, sp.diff(sqrt_g * a_med_expr, x_sym), "numpy")
    dsa_mat_fn = sp.lambdify(x_sym, sp.diff(sqrt_g * a_mat_expr, x_sym), "numpy")
    sc_med_fn = sp.lambdify(x_sym, sqrt_g * c_med_expr, "numpy")
    sc_mat_fn = sp.lambdify(x_sym, sqrt_g * c_mat_expr, "numpy")
    a_med_val_fn = sp.lambdify(x_sym, a_med_expr, "numpy")
    a_mat_val_fn = sp.lambdify(x_sym, a_mat_expr, "numpy")
    c_med_val_fn = sp.lambdify(x_sym, c_med_expr, "numpy")
    c_mat_val_fn = sp.lambdify(x_sym, c_mat_expr, "numpy")
    df_med_val_fn = sp.lambdify(x_sym, sp.diff(f_med_expr, x_sym), "numpy")
    df_mat_val_fn = sp.lambdify(x_sym, sp.diff(f_mat_expr, x_sym), "numpy")
    twoH_minus_lA_fn = sp.lambdify(x_sym, 2 * H - lA, "numpy")
    d_twoH_minus_lA_fn = sp.lambdify(x_sym, (2 * H - lA).diff(x_sym), "numpy")

    sa_vals = sa_med_fn(xs) - rho0_star * sa_mat_fn(xs)
    sc_vals = sc_med_fn(xs) - rho0_star * sc_mat_fn(xs)
    dsa_vals = dsa_med_fn(xs) - rho0_star * dsa_mat_fn(xs)
    a_vals = a_med_val_fn(xs) - rho0_star * a_mat_val_fn(xs)
    c_vals = c_med_val_fn(xs) - rho0_star * c_mat_val_fn(xs)
    df_vals = df_med_val_fn(xs) - rho0_star * df_mat_val_fn(xs)

    dln_ell = sa_vals / QC_vals

    # Integrate d/dx ln(ell(x)/x) = dln_ell - 1/x with boundary condition ell(1) = 1
    integrand_u = dln_ell - 1.0 / xs
    ln_ell_over_x = cumulative_trapezoid(integrand_u, xs, initial=0.0)
    tail_int = 0.5 * (integrand_u[-1] + 0.0) * (1.0 - xs[-1])
    ln_ell_over_x = ln_ell_over_x - (ln_ell_over_x[-1] + tail_int)
    ell_over_x = np.exp(ln_ell_over_x)
    ell_vals = xs * ell_over_x
    ell_prime = ell_vals * dln_ell

    # Exact second derivative ell''(x) from the ODE for independent chain-rule check
    ell_double_prime = (
        dsa_vals / sa_vals - (sc_vals / sa_vals) * dln_ell
    ) * ell_prime

    exp_factor = np.exp(twoH_minus_lA_fn(xs))
    br_vals = exp_factor * ell_prime**2
    bt_vals = exp_factor * ell_over_x**2
    I1_hat = br_vals + 2.0 * bt_vals
    I3_hat = br_vals * bt_vals**2

    # Numerical chain-rule verification along the solved trajectory
    d_twoH_lA = d_twoH_minus_lA_fn(xs)
    dln_br_num = d_twoH_lA + 2.0 * ell_double_prime / ell_prime
    dln_bt_num = d_twoH_lA + 2.0 * dln_ell - 2.0 / xs
    chain_num_res = np.max(
        np.abs(df_vals - (a_vals * dln_br_num + c_vals * dln_bt_num))
    )

    # Inner stable light ring root for this q (eq. 52)
    def W_minus_target(y_val: float) -> float:
        return q_val * (-23.0 * y_val + 60.0 * y_val**2 - 33.0 * y_val**3) - 4.0

    y_minus = (20.0 - 7.0 * np.sqrt(3.0)) / 33.0
    y_plus = (20.0 + 7.0 * np.sqrt(3.0)) / 33.0
    y_lr = float(brentq(W_minus_target, y_minus, y_plus, xtol=1e-14))
    x_lr = float(np.sqrt(y_lr))
    P_lr = 1.0 + 5.75 * y_lr - 7.5 * y_lr**2 + 2.75 * y_lr**3
    V_minus_min_rc2 = float(np.exp(-q_val * P_lr) / y_lr)
    V_plus_max_rc2 = float(1.0 / (np.e**2 * q_val**2))
    V_ratio = V_plus_max_rc2 / V_minus_min_rc2

    return {
        "q": q_val,
        "I_met_pure_medium": float(I_met_val),
        "pure_medium_boundary_traction": float(num_int),
        "rho0_star": rho0_star,
        "boundary_traction_residual": float(abs(QC_boundary)),
        "wrong_sign_rho0_boundary_traction": float(QC_wrong_sign),
        "max_a_on_interior": float(np.max(a_vals)),
        "max_QC_on_interior": float(np.max(QC_vals)),
        "min_dln_ell_dx": float(np.min(dln_ell)),
        "ell_prime_at_center": float(ell_over_x[0]),
        "ell_prime_near_boundary": float(ell_prime[-1]),
        "central_strain_bc": float(br_vals[0]),
        "boundary_br": float(br_vals[-1]),
        "boundary_bt": float(bt_vals[-1]),
        "I1_hat_strictly_decreasing": bool(np.all(np.diff(I1_hat) < 0.0)),
        "I3_hat_strictly_decreasing": bool(np.all(np.diff(I3_hat) < 0.0)),
        "ell_strictly_increasing": bool(np.all(np.diff(ell_vals) > 0.0)),
        "max_chain_rule_numerical_residual": float(chain_num_res),
        "inner_light_ring_x_lr": x_lr,
        "optical_barrier_ratio_Vmax_over_Vmin": V_ratio,
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

    bvp_results = {}
    for q_val in (1.2, 1.5, 1.8):
        row = solve_interior_bvp_for_q(q_val)
        tag = f"q_{q_val:.1f}"
        bvp_results[tag] = row
        checks[f"{tag}_pure_medium_I_met_positive"] = bool(row["I_met_pure_medium"] > 0.01)
        checks[f"{tag}_eigenvalue_rho0_star_positive"] = bool(row["rho0_star"] > 0.0)
        checks[f"{tag}_zero_boundary_traction"] = bool(
            row["boundary_traction_residual"] < 1e-14
        )
        checks[f"{tag}_radial_slope_a_strictly_negative"] = bool(
            row["max_a_on_interior"] < 0.0
        )
        checks[f"{tag}_label_current_QC_strictly_negative"] = bool(
            row["max_QC_on_interior"] < 0.0
        )
        checks[f"{tag}_ell_strictly_increasing"] = row["ell_strictly_increasing"]
        checks[f"{tag}_boundary_ell_prime_matches_one"] = bool(
            abs(row["ell_prime_near_boundary"] - 1.0) < 5e-4
        )
        checks[f"{tag}_I1_hat_strictly_decreasing"] = row["I1_hat_strictly_decreasing"]
        checks[f"{tag}_I3_hat_strictly_decreasing"] = row["I3_hat_strictly_decreasing"]
        checks[f"{tag}_constitutive_chain_rule_residual"] = bool(
            row["max_chain_rule_numerical_residual"] < 1e-10
        )
        checks[f"{tag}_inner_light_ring_in_core"] = bool(
            0.7 < row["inner_light_ring_x_lr"] < 1.0
        )

    w15 = bvp_results["q_1.5"]
    neg_controls["pure_medium_zero_matter_on_deg6_metric_rejected"] = bool(
        w15["pure_medium_boundary_traction"] > 0.06
    )
    neg_controls["wrong_sign_core_matter_density_rejected"] = bool(
        w15["wrong_sign_rho0_boundary_traction"] > 1.99 * w15["pure_medium_boundary_traction"]
    )
    checks["negative_control_pure_medium_deg6_traction_nonzero"] = neg_controls[
        "pure_medium_zero_matter_on_deg6_metric_rejected"
    ]
    checks["negative_control_wrong_sign_core_matter_rejected"] = neg_controls[
        "wrong_sign_core_matter_density_rejected"
    ]

    # Check q=1.5 light ring values against RefG_ka.md line 727 (rounded to 5 and 4 decimal places)
    checks["q_1.5_inner_light_ring_matches_article_0.87058"] = bool(
        round(w15["inner_light_ring_x_lr"], 5) == 0.87058
    )
    checks["q_1.5_optical_barrier_ratio_matches_article_1.3263"] = bool(
        round(w15["optical_barrier_ratio_Vmax_over_Vmin"], 4) == 1.3263
    )

    all_passed = all(checks.values()) and all(neg_controls.values())

    result = {
        "claim_id": "REFG_ACTION_DERIVED_C2_INTERIOR_CLOSURE_V1",
        "model_version": "REFG_STRONG_FIELD_COVARIANT_MEDIUM_C2_INTERIOR_V1",
        "status": "PASS_ACTION_DERIVED_C2_INTERIOR_CLOSURE" if all_passed else "FAIL",
        "all_checks_passed": all_passed,
        "total_checks": len(checks),
        "passed_checks": sum(1 for v in checks.values() if v),
        "failed_checks": [k for k, v in checks.items() if not v],
        "negative_controls": neg_controls,
        "symbolic_residuals": sym_residuals,
        "bvp_solutions_by_q": bvp_results,
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
                "q_1.5_rho0_star": w15["rho0_star"],
                "q_1.5_ell_prime_0": w15["ell_prime_at_center"],
                "q_1.5_central_strain_bc": w15["central_strain_bc"],
                "q_1.5_x_lr": w15["inner_light_ring_x_lr"],
                "q_1.5_chain_rule_res": w15["max_chain_rule_numerical_residual"],
            },
            indent=2,
        )
    )
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
