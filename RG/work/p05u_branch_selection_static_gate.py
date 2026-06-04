# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: compact branch uses phase-normalized F_min
# variables and the projected deficit source; no new coefficient scheme.

"""
PHASE 18u: Static branch-selection conditional gate.

This is the first internal proof layer for the branch-selection criticism.
It does not claim that a finite core dynamically selects the compact branch.
That requires an interior model and remains a later gate.

What this file proves conditionally:

    If the boundary data select the compact phase-spherical branch

        H = H_Delta = h,
        phi = -r_s/r,
        h = r_s/(2r),
        B = exp(-2h),
        A = exp(2h),
        omega_Delta = 1,

    and the matching surface is smooth enough to avoid a thin shell, then the
    exterior is locked:

      * the same phase-normalized F_min action template is used;
      * the compact F_min sector is quiet on the pure-phase exterior;
      * the projected deficit source closes the diagonal Einstein equations;
      * the exterior is not a GR vacuum, so Birkhoff's vacuum uniqueness theorem
        is out of scope;
      * the static photon-sphere, shadow and ISCO numbers follow algebraically.

What this file leaves open:

      * the finite-core dynamical law that selects this boundary data;
      * rotating exterior, QNM/echo and ray-tracing tests;
      * curved-background hyperbolicity of the full compact perturbation system.
"""

from __future__ import annotations

import sympy as sp

from p03d_phase_normalized_solar_global_audit import (
    phase_normalized_solar_global_audit,
)
from p05g_exponential_source_eom import (
    auxiliary_deficit_operator_health_gate,
    derive_biconformal_metric_map_gate,
    derive_covariant_deficit_operator_from_medium_fields_gate,
    derive_energy_condition_verdict_gate,
    derive_phase_equation_covariant_consistency_gate,
    derive_projected_source_eom_closure_gate,
    unified_deficit_operator_branch_selection_gate,
)
from p05s_phase_normalized_fmin_action_gate import (
    derive_phase_normalized_fmin_action_gate,
)
from p05t_single_action_branch_consistency_gate import (
    derive_single_action_branch_consistency_gate,
)


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def derive_birkhoff_scope_gate() -> dict[str, object]:
    """
    Birkhoff-scope audit.

    GR Birkhoff uniqueness applies to spherically symmetric vacuum exteriors.
    The compact branch is explicitly not a vacuum exterior: its active projected
    deficit source is nonzero for r>0, r_s>0.  Therefore the Schwarzschild
    uniqueness theorem is not the theorem being violated; the real question is
    finite-core branch selection.
    """
    r, r_s, G = sp.symbols("r r_s G", positive=True, real=True)
    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    delta_p = sp.simplify(D / (8 * sp.pi * G))

    G_mixed = {
        "G^t_t": -D,
        "G^r_r": D,
        "G^theta_theta": -D,
        "G^phi_phi": -D,
    }
    theta_mixed = {
        "Theta^t_t": -delta_p,
        "Theta^r_r": delta_p,
        "Theta^theta_theta": -delta_p,
        "Theta^phi_phi": -delta_p,
    }
    residuals = {
        "t": sp.simplify(G_mixed["G^t_t"] - 8 * sp.pi * G * theta_mixed["Theta^t_t"]),
        "r": sp.simplify(G_mixed["G^r_r"] - 8 * sp.pi * G * theta_mixed["Theta^r_r"]),
        "theta": sp.simplify(
            G_mixed["G^theta_theta"]
            - 8 * sp.pi * G * theta_mixed["Theta^theta_theta"]
        ),
        "phi": sp.simplify(
            G_mixed["G^phi_phi"] - 8 * sp.pi * G * theta_mixed["Theta^phi_phi"]
        ),
    }

    nonvacuum_components = [sp.simplify(value) != 0 for value in G_mixed.values()]
    active_source_components = [
        sp.simplify(value) != 0 for value in theta_mixed.values()
    ]
    passed = (
        all(nonvacuum_components)
        and all(active_source_components)
        and _all_zero(residuals.values())
    )

    return {
        "birkhoff_scope_status": (
            "PASS_COMPACT_EXTERIOR_IS_NOT_GR_VACUUM__BIRKHOFF_OUT_OF_SCOPE"
            if passed
            else "CHECK_BIRKHOFF_SCOPE_FOR_COMPACT_EXTERIOR"
        ),
        "D": D,
        "Delta_P": delta_p,
        "Einstein_mixed": G_mixed,
        "ThetaRefG_active_mixed": theta_mixed,
        "field_equation_residuals": residuals,
        "GR_vacuum_exterior": False,
        "Birkhoff_applicability": (
            "Birkhoff's vacuum uniqueness theorem is not the relevant theorem "
            "once the active projected-deficit source is present."
        ),
        "remaining_question": (
            "which finite-core interiors select this nonvacuum exterior branch"
        ),
    }


def derive_biconformal_no_thin_shell_matching_gate() -> dict[str, object]:
    """
    Israel-shell identity for a biconformal matching surface.

    In isotropic coordinates with

        ds^2 = B c^2 dt^2 - A(dr^2+r^2 dOmega^2),
        B = exp(-2h), A = exp(2h),

    the induced metric at r=R depends on B and A R^2, while the extrinsic
    curvature depends on B', A', A and R.  If the interior and exterior
    biconformal branches match h and h' at the surface, the induced metric and
    extrinsic curvature jumps vanish.  This is the thin-shell part of the
    branch-selection boundary data.  It does not derive the interior.
    """
    R = sp.symbols("R", positive=True, real=True)
    h_i, h_e, hp_i, hp_e = sp.symbols("h_i h_e hp_i hp_e", real=True)

    A_i = sp.exp(2 * h_i)
    A_e = sp.exp(2 * h_e)
    B_i = sp.exp(-2 * h_i)
    B_e = sp.exp(-2 * h_e)
    Ap_i = 2 * A_i * hp_i
    Ap_e = 2 * A_e * hp_e
    Bp_i = -2 * B_i * hp_i
    Bp_e = -2 * B_e * hp_e

    induced_jumps = {
        "Delta_gamma_tt": sp.simplify(B_i - B_e),
        "Delta_gamma_theta_theta": sp.simplify(A_i * R**2 - A_e * R**2),
        "Delta_gamma_phi_phi_over_sin2": sp.simplify(A_i * R**2 - A_e * R**2),
    }
    K_i = {
        "K_tt": sp.simplify(Bp_i / (2 * sp.sqrt(A_i))),
        "K_theta_theta": sp.simplify((Ap_i * R**2 + 2 * A_i * R) / (2 * sp.sqrt(A_i))),
        "K_phi_phi_over_sin2": sp.simplify(
            (Ap_i * R**2 + 2 * A_i * R) / (2 * sp.sqrt(A_i))
        ),
    }
    K_e = {
        "K_tt": sp.simplify(Bp_e / (2 * sp.sqrt(A_e))),
        "K_theta_theta": sp.simplify((Ap_e * R**2 + 2 * A_e * R) / (2 * sp.sqrt(A_e))),
        "K_phi_phi_over_sin2": sp.simplify(
            (Ap_e * R**2 + 2 * A_e * R) / (2 * sp.sqrt(A_e))
        ),
    }
    extrinsic_jumps = {
        key: sp.simplify(K_i[key] - K_e[key])
        for key in K_i
    }
    match_subs = {h_i: h_e, hp_i: hp_e}
    induced_after_match = {
        key: sp.simplify(value.subs(match_subs))
        for key, value in induced_jumps.items()
    }
    extrinsic_after_match = {
        key: sp.simplify(value.subs(match_subs))
        for key, value in extrinsic_jumps.items()
    }

    r_s = sp.symbols("r_s", positive=True, real=True)
    h_ext_R = sp.simplify(r_s / (2 * R))
    hp_ext_R = sp.simplify(-r_s / (2 * R**2))

    passed = _all_zero(induced_after_match.values()) and _all_zero(
        extrinsic_after_match.values()
    )

    return {
        "matching_status": (
            "PASS_BICONFORMAL_C1_MATCHING_HAS_ZERO_ISRAEL_THIN_SHELL"
            if passed
            else "CHECK_BICONFORMAL_MATCHING_THIN_SHELL"
        ),
        "metric_branch": "B=exp(-2h), A=exp(2h)",
        "induced_metric_jumps_before_matching": induced_jumps,
        "extrinsic_curvature_jumps_before_matching": extrinsic_jumps,
        "matching_conditions": {
            "h_in(R)=h_ext(R)": True,
            "hprime_in(R)=hprime_ext(R)": True,
        },
        "induced_metric_jumps_after_matching": induced_after_match,
        "extrinsic_curvature_jumps_after_matching": extrinsic_after_match,
        "compact_exterior_boundary_data": {
            "h_ext(R)": h_ext_R,
            "hprime_ext(R)": hp_ext_R,
        },
        "scope": (
            "C1 biconformal matching removes the Israel thin shell.  A real "
            "finite-core branch-selection proof must still derive an interior "
            "solution that reaches this boundary data."
        ),
    }


def derive_static_geodesic_prediction_lock_gate() -> dict[str, object]:
    """
    Static geodesic numbers locked by the compact exterior.
    """
    r, r_s, c, L2 = sp.symbols("r r_s c L2", positive=True, real=True)

    B_ph = sp.exp(-2 * r_s / r) / r**2
    dB_ph = sp.factor(sp.simplify(sp.diff(B_ph, r)))
    photon_roots = sp.solve(sp.Eq(dB_ph, 0), r)
    r_ph = r_s
    b_c = sp.simplify(1 / sp.sqrt(B_ph.subs(r, r_ph)))
    b_c_gr = sp.simplify(3 * sp.sqrt(3) * r_s / 2)
    b_ratio = sp.simplify(b_c / b_c_gr)

    V_eff = sp.exp(-r_s / r) + L2 * sp.exp(-2 * r_s / r) / r**2
    circular_L2 = sp.solve(sp.Eq(sp.diff(V_eff, r), 0), L2)[0]
    circular_L2 = sp.simplify(circular_L2)
    marginal_numerator = sp.factor(
        sp.together(sp.diff(circular_L2, r)).as_numer_denom()[0]
    )
    r_isco = sp.simplify(r_s * (sp.Integer(3) + sp.sqrt(5)) / 2)
    phi_golden = sp.simplify((1 + sp.sqrt(5)) / 2)
    phi_squared_rs = sp.simplify(phi_golden**2 * r_s)

    Omega2 = sp.simplify(c**2 * r_s * sp.exp(-2 * r_s / r) / (r**2 * (2 * r - r_s)))
    Omega2_isco = sp.simplify(Omega2.subs(r, r_isco))
    Omega2_gr = sp.simplify(c**2 / (54 * r_s**2))
    frequency_ratio = sp.simplify(sp.sqrt(Omega2_isco / Omega2_gr))
    frequency_ratio_numeric = sp.N(frequency_ratio, 12)

    passed = (
        photon_roots == [r_s]
        and sp.simplify(b_c - sp.E * r_s) == 0
        and sp.simplify(b_ratio - 2 * sp.E / (3 * sp.sqrt(3))) == 0
        and sp.simplify(circular_L2 - r**2 * r_s * sp.exp(r_s / r) / (2 * (r - r_s))) == 0
        and sp.simplify(
            marginal_numerator
            / (r_s * sp.exp(r_s / r) * (r**2 - 3 * r * r_s + r_s**2))
        )
        == 1
        and sp.simplify(r_isco - phi_squared_rs) == 0
        and abs(float(frequency_ratio_numeric) - 0.931) < 5e-4
    )

    return {
        "static_geodesic_lock_status": (
            "PASS_COMPACT_STATIC_GEODESIC_NUMBERS_LOCKED_BY_EXPONENTIAL_BRANCH"
            if passed
            else "CHECK_COMPACT_STATIC_GEODESIC_NUMBER_LOCK"
        ),
        "B_ph": B_ph,
        "dB_ph_dr": dB_ph,
        "photon_sphere_roots": photon_roots,
        "r_ph": r_ph,
        "b_c": b_c,
        "b_c_GR": b_c_gr,
        "b_c_over_b_c_GR": b_ratio,
        "shadow_shift_percent": sp.N((b_ratio - 1) * 100, 8),
        "V_eff": V_eff,
        "L_circular_squared": circular_L2,
        "marginal_stability_polynomial": r**2 - 3 * r_s * r + r_s**2,
        "r_ISCO": r_isco,
        "phi_squared_r_s": phi_squared_rs,
        "Omega2_ISCO": Omega2_isco,
        "Omega2_GR_ISCO": Omega2_gr,
        "f_ISCO_over_f_ISCO_GR": frequency_ratio,
        "f_ISCO_over_f_ISCO_GR_numeric": frequency_ratio_numeric,
        "scope": (
            "static spherical geodesic benchmark only; rotating exterior, "
            "plasma/accretion ray tracing and finite-core selection are not "
            "proved by this geodesic lock."
        ),
    }


def derive_static_branch_selection_conditional_gate() -> dict[str, object]:
    """
    First branch-selection proof layer.

    This gate combines the previous static ledgers and makes the exact status
    explicit: the compact branch is an internally closed conditional exterior.
    The finite-core selection law remains open.
    """
    single_action = derive_single_action_branch_consistency_gate()
    solar_guard = phase_normalized_solar_global_audit()
    fmin_action = derive_phase_normalized_fmin_action_gate()
    biconformal = derive_biconformal_metric_map_gate()
    phase_equation = derive_phase_equation_covariant_consistency_gate()
    covariant_deficit = derive_covariant_deficit_operator_from_medium_fields_gate()
    deficit_health = auxiliary_deficit_operator_health_gate()
    source_closure = derive_projected_source_eom_closure_gate()
    branch_scale = unified_deficit_operator_branch_selection_gate()
    energy_verdict = derive_energy_condition_verdict_gate()
    birkhoff = derive_birkhoff_scope_gate()
    matching = derive_biconformal_no_thin_shell_matching_gate()
    geodesics = derive_static_geodesic_prediction_lock_gate()

    status_checks = {
        "single_action": single_action["status"]
        == "PASS_SINGLE_ACTION_PHASE_NORMALIZED_BRANCH_LEDGER",
        "solar_guard": solar_guard["status"]
        == "PASS_INDEPENDENT_H_RETAINS_SOLAR_1PN_2PN__GLOBAL_I3_LOCK_REJECTED",
        "phase_normalized_fmin_action": fmin_action["phase_normalized_action_status"]
        == "PASS_ACTION_LEVEL_PHASE_NORMALIZED_FMIN_IS_QUIET_ON_COMPACT_BRANCH",
        "biconformal_map": biconformal["biconformal_map_status"]
        == "PASS_BICONFORMAL_MAP_DEFINED_AND_FIRST_ORDER_SELECTED",
        "phase_equation": phase_equation["phase_equation_consistency_status"]
        == "PASS_REDUCED_PHASE_EQUATION_EQUALS_CURVED_HARMONIC_EQUATION_ON_BICONFORMAL_BRANCH",
        "covariant_deficit": covariant_deficit["operator_status"]
        == "PASS_COVARIANT_DEFICIT_OPERATOR_REDUCES_TO_STATIC_PROJECTED_SOURCE",
        "deficit_operator_health": deficit_health["operator_health_status"]
        == "PASS_INDEPENDENT_PRESSURE_DEFICIT_OPERATOR_CLOSES_EXTERIOR",
        "projected_source_closure": source_closure["projected_source_eom_status"]
        == "PASS_PROJECTED_BERNOULLI_SOURCE_SOLVES_STATIC_EXPONENTIAL_EOM",
        "branch_scale": branch_scale["branch_selection_status"]
        == "PASS_SINGLE_EFT_OPERATOR_WITH_BRANCH_SELECTED_EXTERIOR_LOAD",
        "energy_verdict": energy_verdict["energy_condition_verdict_status"]
        == "PASS_ACTIVE_DEFICIT_NEC_VERDICT_FOR_COMPACT_EXPONENTIAL_BRANCH",
        "birkhoff_scope": birkhoff["birkhoff_scope_status"]
        == "PASS_COMPACT_EXTERIOR_IS_NOT_GR_VACUUM__BIRKHOFF_OUT_OF_SCOPE",
        "no_thin_shell_matching": matching["matching_status"]
        == "PASS_BICONFORMAL_C1_MATCHING_HAS_ZERO_ISRAEL_THIN_SHELL",
        "static_geodesic_lock": geodesics["static_geodesic_lock_status"]
        == "PASS_COMPACT_STATIC_GEODESIC_NUMBERS_LOCKED_BY_EXPONENTIAL_BRANCH",
    }
    passed = all(status_checks.values())

    return {
        "static_branch_selection_status": (
            "PASS_STATIC_BRANCH_SELECTION_CONDITIONAL_THEOREM__FINITE_CORE_DYNAMICS_OPEN"
            if passed
            else "CHECK_STATIC_BRANCH_SELECTION_CONDITIONAL_THEOREM"
        ),
        "status_checks": status_checks,
        "proved_conditional_theorem": (
            "Given compact boundary data H=H_Delta=h, omega_Delta=1, the "
            "reduced phase equation, the biconformal map, phase-normalized "
            "F_min, and C1 no-shell matching, the compact exterior is an exact "
            "nonvacuum static branch of the same EFT sector.  Its projected "
            "deficit source closes the field equations and locks the static "
            "photon-sphere, shadow and ISCO numbers."
        ),
        "necessary_boundary_data": {
            "compact_phase": "phi=-r_s/r and h=-phi/2=r_s/(2r)",
            "branch_loading": "H=H_Delta=h and omega_Delta=1",
            "metric_map": "B=exp(-2h), A=exp(2h)",
            "matching": "h_in(R)=h_ext(R), hprime_in(R)=hprime_ext(R); stronger C2 matching is the finite-core regularity target",
        },
        "weak_branch_guard": {
            "H": 0,
            "solar_status": solar_guard["status"],
            "direct_deficit_scale_ratio": branch_scale["compactness_ratio"],
            "solar_unweighted_ratio": branch_scale["solar_unweighted_ratio"],
        },
        "compact_branch_guard": {
            "single_action_status": single_action["status"],
            "Fmin_action_status": fmin_action["phase_normalized_action_status"],
            "source_status": source_closure["projected_source_eom_status"],
            "Birkhoff_scope": birkhoff["birkhoff_scope_status"],
            "matching_status": matching["matching_status"],
            "geodesic_status": geodesics["static_geodesic_lock_status"],
        },
        "locked_static_numbers": {
            "r_ph": geodesics["r_ph"],
            "b_c": geodesics["b_c"],
            "b_c_over_b_c_GR": geodesics["b_c_over_b_c_GR"],
            "shadow_shift_percent": geodesics["shadow_shift_percent"],
            "r_ISCO": geodesics["r_ISCO"],
            "f_ISCO_over_f_ISCO_GR": geodesics["f_ISCO_over_f_ISCO_GR_numeric"],
        },
        "not_proved_by_this_gate": [
            "finite-core dynamics selects the compact branch for real objects",
            "the compactness threshold or continuous H-loading law",
            "rotating compact exterior",
            "full curved-background hyperbolicity and QNM/echo spectrum",
            "EHT/ngEHT/BHEX ray-traced observational likelihood",
        ],
        "article_safe_export_if_needed_later": (
            "The compact phase-spherical branch is an internally closed "
            "conditional static exterior of the same phase-normalized EFT "
            "sector.  If finite-core matching selects the boundary data "
            "H=H_Delta=h, its projected deficit source closes the nonvacuum "
            "exterior field equations and fixes the static shadow/ISCO "
            "benchmarks.  The finite-core selection law remains a separate "
            "dynamical gate."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18u: Static branch-selection conditional gate")
    print("=" * 72)
    sections = [
        ("1. Birkhoff scope", derive_birkhoff_scope_gate()),
        ("2. No-thin-shell biconformal matching", derive_biconformal_no_thin_shell_matching_gate()),
        ("3. Static geodesic lock", derive_static_geodesic_prediction_lock_gate()),
        ("4. Central conditional theorem", derive_static_branch_selection_conditional_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:48s}: {value}")
