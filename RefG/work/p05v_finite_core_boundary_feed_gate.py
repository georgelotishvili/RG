# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: finite-core boundary audit; no new coefficient
# scheme beyond the compact phase-normalized branch.

"""
PHASE 18v: Finite-core boundary feed gate.

p05u proves a conditional static theorem:

    if finite-core matching supplies the compact branch boundary data, then the
    compact exterior is locked.

This file checks the next, narrower layer: whether the existing C2 finite-core
ansatz actually supplies that boundary data at algebraic/junction/source-ledger
level.  It still does not prove the physical dynamical selection law for real
compact objects.

Closed here:
  * the C2 logarithmic core matches log A and log B through C2 at x=1;
  * h_core=-log(B_core)/2 matches h_ext and its derivatives at the boundary;
  * the induced metric and Israel shell stress vanish at the matching surface;
  * the effective C2 core source is finite and continuous at the boundary;
  * the C2 source decomposes into projected phase source plus residual medium
    stress, with residual vanishing at the boundary.

Made explicit here:
  * if the matching surface must lie on the usual exterior wormhole sheet
    r>=r_s/2, then q=r_s/r_c must satisfy q<=2;
  * if one additionally demands matching inside the formal pressure-turn radius
    r_s/4, then q>=4, which is incompatible with q<=2;
  * therefore the pressure-turn/Knudsen cutoff is not yet the same thing as a
    physical exterior-sheet branch-selection law.
"""

from __future__ import annotations

import sympy as sp

from p05_compact import (
    analyze_geodesic_completion_by_core_matching,
    derive_c2_core_action_density_integrability_theorem,
    derive_c2_core_field_equation_source,
    derive_c2_core_local_stability_interface,
    derive_c2_core_nonlinear_ivp_parameter_domain_theorem,
    derive_c2_core_proper_energy_finiteness,
    derive_c2_core_refg_medium_source_decomposition,
    derive_c2_junction_stress_closure,
)
from p05u_branch_selection_static_gate import (
    derive_static_branch_selection_conditional_gate,
)


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def _c2_log_profiles(x: sp.Symbol, q: sp.Symbol) -> dict[str, sp.Expr]:
    log_a_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    log_b_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )
    log_a_ext = q / x
    log_b_ext = -q / x
    return {
        "log_A_core": log_a_core,
        "log_B_core": log_b_core,
        "log_A_ext": log_a_ext,
        "log_B_ext": log_b_ext,
    }


def derive_c2_boundary_data_feeds_p05u_gate() -> dict[str, object]:
    """
    Does the C2 ansatz supply the exact p05u boundary data?

    p05u asks for h_ext(R)=r_s/(2R) and h'_ext(R)=-r_s/(2R^2).  In C2
    variables x=r/r_c and q=r_s/r_c, this is h_ext(1)=q/2 and
    dh_ext/dx(1)=-q/2.  The C2 core matches h through second derivative.
    """
    x, q, r_c, r_s = sp.symbols("x q r_c r_s", positive=True, real=True)
    profiles = _c2_log_profiles(x, q)
    h_core = sp.simplify(-profiles["log_B_core"] / 2)
    h_ext = sp.simplify(-profiles["log_B_ext"] / 2)

    h_match = {
        "h_core_minus_h_ext": sp.simplify((h_core - h_ext).subs(x, 1)),
        "h_x_core_minus_h_x_ext": sp.simplify(
            (sp.diff(h_core, x) - sp.diff(h_ext, x)).subs(x, 1)
        ),
        "h_xx_core_minus_h_xx_ext": sp.simplify(
            (sp.diff(h_core, x, 2) - sp.diff(h_ext, x, 2)).subs(x, 1)
        ),
    }
    log_match = {}
    for name in ("A", "B"):
        core = profiles[f"log_{name}_core"]
        ext = profiles[f"log_{name}_ext"]
        log_match[f"log_{name}_value"] = sp.simplify((core - ext).subs(x, 1))
        log_match[f"log_{name}_slope"] = sp.simplify(
            (sp.diff(core, x) - sp.diff(ext, x)).subs(x, 1)
        )
        log_match[f"log_{name}_curvature"] = sp.simplify(
            (sp.diff(core, x, 2) - sp.diff(ext, x, 2)).subs(x, 1)
        )

    p05u_boundary = {
        "h_ext(R)": sp.simplify(r_s / (2 * r_c)),
        "hprime_ext(R)": sp.simplify(-r_s / (2 * r_c**2)),
    }
    c2_boundary = {
        "h_ext(x=1)": sp.simplify(h_ext.subs(x, 1)),
        "dh_ext_dx(x=1)": sp.simplify(sp.diff(h_ext, x).subs(x, 1)),
        "h_ext(R)_with_q=rs/rc": sp.simplify(h_ext.subs(x, 1).subs(q, r_s / r_c)),
        "hprime_ext(R)_with_q=rs/rc": sp.simplify(
            (sp.diff(h_ext, x).subs(x, 1) / r_c).subs(q, r_s / r_c)
        ),
    }
    feeds_p05u = {
        "h_value": sp.simplify(c2_boundary["h_ext(R)_with_q=rs/rc"] - p05u_boundary["h_ext(R)"]),
        "h_radial_slope": sp.simplify(
            c2_boundary["hprime_ext(R)_with_q=rs/rc"] - p05u_boundary["hprime_ext(R)"]
        ),
    }

    existing_completion = analyze_geodesic_completion_by_core_matching()

    passed = (
        _all_zero(h_match.values())
        and _all_zero(log_match.values())
        and _all_zero(feeds_p05u.values())
        and existing_completion["proof_status"]
        == "C2_CORE_MATCHING_ANSATZ__JUNCTION_STRESS_CLOSED__EFFECTIVE_CORE_SOURCE_DERIVED__MEDIUM_SOURCE_DECOMPOSITION_SEPARATE"
    )

    return {
        "boundary_feed_status": (
            "PASS_C2_CORE_BOUNDARY_DATA_FEEDS_P05U_COMPACT_BRANCH"
            if passed
            else "CHECK_C2_CORE_BOUNDARY_DATA_FEED"
        ),
        "h_core": h_core,
        "h_ext": h_ext,
        "h_C2_match_at_x1": h_match,
        "log_A_log_B_C2_match_at_x1": log_match,
        "p05u_required_boundary": p05u_boundary,
        "C2_boundary_data": c2_boundary,
        "C2_minus_p05u_boundary": feeds_p05u,
        "existing_completion_status": existing_completion["proof_status"],
        "core_radius_rule": existing_completion["core_radius"],
        "core_compactness_rule": existing_completion["core_compactness_q"],
        "scope": (
            "This proves that the C2 ansatz reaches the boundary data needed "
            "by p05u.  It does not prove that physical collapse selects this "
            "ansatz or this radius."
        ),
    }


def derive_c2_source_boundary_continuity_gate() -> dict[str, object]:
    """
    Does the finite-core source ledger attach continuously to the compact
    exterior source at the boundary?
    """
    junction = derive_c2_junction_stress_closure()
    core_source = derive_c2_core_field_equation_source()
    core_energy = derive_c2_core_proper_energy_finiteness()
    medium = derive_c2_core_refg_medium_source_decomposition()
    action_density = derive_c2_core_action_density_integrability_theorem()
    local_stability = derive_c2_core_local_stability_interface()

    metric_jumps_zero = _all_zero(junction["metric_jump_at_rc"].values())
    first_jumps_zero = _all_zero(junction["first_derivative_jump_at_rc"].values())
    junction_zero = _all_zero(junction["extrinsic_curvature_jump"].values()) and _all_zero(
        junction["Israel_surface_stress"].values()
    )
    boundary_source_continuous = _all_zero(
        core_source["boundary_Einstein_jump_core_minus_exterior"].values()
    )
    phase_match = _all_zero(medium["phase_C2_match_at_boundary"].values())

    passed = (
        metric_jumps_zero
        and first_jumps_zero
        and junction_zero
        and boundary_source_continuous
        and phase_match
        and medium["boundary_residuals_zero"]
        and core_source["finite_center_status"]
        == "PASS_C2_CORE_EFFECTIVE_SOURCE_FINITE_AT_CENTER"
        and core_source["boundary_status"]
        == "PASS_C2_CORE_EFFECTIVE_SOURCE_CONTINUOUS_AT_R_C"
        and core_energy["proper_energy_status"]
        == "C2_CORE_EFFECTIVE_PROPER_SOURCE_FINITE_FOR_FINITE_R_C"
        and action_density["integrability_status"]
        == "PASS_BRANCH_LEVEL_FULL_DIAGONAL_ACTION_DENSITY_INTEGRABILITY"
        and local_stability["interface_status"]
        == "PASS_COMPACT_CORE_P01_LOCAL_STABILITY_INTERFACE"
    )

    return {
        "source_boundary_status": (
            "PASS_C2_CORE_SOURCE_LEDGER_CONTINUOUS_AND_FINITE_AT_BOUNDARY"
            if passed
            else "CHECK_C2_CORE_SOURCE_BOUNDARY_LEDGER"
        ),
        "junction_status": junction["junction_status"],
        "metric_jumps_zero": metric_jumps_zero,
        "first_derivative_jumps_zero": first_jumps_zero,
        "junction_zero": junction_zero,
        "core_field_equation_status": core_source["field_equation_status"],
        "core_source_center_status": core_source["finite_center_status"],
        "core_source_boundary_status": core_source["boundary_status"],
        "boundary_Einstein_jump_core_minus_exterior": core_source[
            "boundary_Einstein_jump_core_minus_exterior"
        ],
        "proper_energy_status": core_energy["proper_energy_status"],
        "medium_source_status": medium["realization_status"],
        "phase_C2_match_at_boundary": medium["phase_C2_match_at_boundary"],
        "residual_boundary": medium["residual_boundary"],
        "boundary_residuals_zero": medium["boundary_residuals_zero"],
        "action_density_integrability_status": action_density["integrability_status"],
        "local_stability_interface_status": local_stability["interface_status"],
        "scope": (
            "Tensor and action-density boundary ledger only.  The full coupled "
            "core evolution and perturbative spectrum are still open."
        ),
    }


def derive_throat_cutoff_domain_gate() -> dict[str, object]:
    """
    Separate exterior-sheet matching from pressure-turn/Knudsen cutoff language.
    """
    q, r_s, r_c, N = sp.symbols("q r_s r_c N", positive=True, real=True)
    throat = r_s / 2
    formal_pressure_turn = r_s / 4
    core_radius = r_s / q

    exterior_sheet_condition_q = sp.Le(q, 2)
    at_or_inside_pressure_turn_q = sp.Ge(q, 4)
    exterior_and_pressure_turn_overlap = False

    kn_q = sp.LambertW(N)
    kn_exterior_sheet_N_bound = 2 * sp.E**2
    kn_pressure_turn_N_bound = 4 * sp.E**4

    return {
        "throat_cutoff_domain_status": (
            "PASS_DOMAIN_CONSTRAINTS_EXPLICIT__PRESSURE_TURN_CUTOFF_NOT_BRANCH_SELECTION_PROOF"
        ),
        "q_definition": sp.Eq(q, r_s / r_c),
        "core_radius": core_radius,
        "throat_radius": throat,
        "formal_pressure_turn_radius": formal_pressure_turn,
        "exterior_sheet_matching_condition": {
            "r_c >= r_s/2": exterior_sheet_condition_q,
            "Kn_parameter_bound_if_q=W(N)": sp.Le(N, kn_exterior_sheet_N_bound),
        },
        "at_or_inside_pressure_turn_condition": {
            "r_c <= r_s/4": at_or_inside_pressure_turn_q,
            "Kn_parameter_bound_if_q=W(N)": sp.Ge(N, kn_pressure_turn_N_bound),
        },
        "exterior_sheet_and_pressure_turn_overlap": exterior_and_pressure_turn_overlap,
        "Kn_q_rule": sp.Eq(q, kn_q),
        "interpretation": (
            "The C2 matching algebra works for symbolic q>0.  If the physical "
            "matching surface must stay on the usual exterior wormhole sheet, "
            "then q<=2.  A separate demand to match at/inside the formal "
            "pressure-turn radius would require q>=4.  Those conditions do not "
            "overlap, so the pressure-turn/Knudsen story cannot be exported as "
            "the physical branch-selection law without an additional derivation."
        ),
    }


def derive_finite_core_boundary_feed_gate() -> dict[str, object]:
    """
    Second-layer finite-core gate.

    This is the strongest statement available before the true dynamical
    branch-selection law: the existing finite-core C2 ansatz feeds the p05u
    compact boundary theorem at boundary/source-ledger level.
    """
    p05u = derive_static_branch_selection_conditional_gate()
    boundary = derive_c2_boundary_data_feeds_p05u_gate()
    source = derive_c2_source_boundary_continuity_gate()
    domain = derive_throat_cutoff_domain_gate()
    ivp_domain = derive_c2_core_nonlinear_ivp_parameter_domain_theorem()

    status_checks = {
        "p05u_static_conditional_theorem": p05u["static_branch_selection_status"]
        == "PASS_STATIC_BRANCH_SELECTION_CONDITIONAL_THEOREM__FINITE_CORE_DYNAMICS_OPEN",
        "C2_boundary_feeds_p05u": boundary["boundary_feed_status"]
        == "PASS_C2_CORE_BOUNDARY_DATA_FEEDS_P05U_COMPACT_BRANCH",
        "C2_source_boundary_continuity": source["source_boundary_status"]
        == "PASS_C2_CORE_SOURCE_LEDGER_CONTINUOUS_AND_FINITE_AT_BOUNDARY",
        "domain_constraints_explicit": domain["throat_cutoff_domain_status"]
        == "PASS_DOMAIN_CONSTRAINTS_EXPLICIT__PRESSURE_TURN_CUTOFF_NOT_BRANCH_SELECTION_PROOF",
        "core_deformation_parameter_domain": ivp_domain["theorem_status"]
        == "PASS_SUFFICIENT_PARAMETER_DOMAIN_FOR_NONLINEAR_CORE_DEFORMATION_IVP",
    }
    passed = all(status_checks.values())

    return {
        "finite_core_boundary_feed_status": (
            "PASS_C2_FINITE_CORE_FEEDS_STATIC_BRANCH_BOUNDARY__DYNAMICAL_SELECTION_OPEN"
            if passed
            else "CHECK_C2_FINITE_CORE_BOUNDARY_FEED"
        ),
        "status_checks": status_checks,
        "closed_now": (
            "The C2 finite-core ansatz reaches the compact boundary data used "
            "by p05u; its junction shell vanishes; its effective core source is "
            "finite and continuous; its projected-phase residual medium source "
            "vanishes at the boundary; and the radial residual deformation has "
            "a sufficient positive-branch IVP domain."
        ),
        "not_closed_now": [
            "physical collapse or finite-core dynamics selects this C2 ansatz",
            "compactness threshold / continuous H-loading law",
            "whether the physical cutoff surface is at the throat, outside it, or in a two-sheet/core replacement geometry",
            "full coupled compact perturbation spectrum, QNMs and echoes",
            "rotating exterior and ray-traced observational comparison",
        ],
        "domain_warning": domain["interpretation"],
        "C2_boundary_summary": {
            "h_C2_match_at_x1": boundary["h_C2_match_at_x1"],
            "C2_minus_p05u_boundary": boundary["C2_minus_p05u_boundary"],
            "core_radius_rule": boundary["core_radius_rule"],
            "core_compactness_rule": boundary["core_compactness_rule"],
        },
        "source_boundary_summary": {
            "junction_status": source["junction_status"],
            "core_source_boundary_status": source["core_source_boundary_status"],
            "boundary_residuals_zero": source["boundary_residuals_zero"],
            "local_stability_interface_status": source["local_stability_interface_status"],
        },
        "sufficient_IVP_condition": ivp_domain["sufficient_kappa_condition"],
        "program_safe_statement": (
            "A C2 finite-core candidate can feed the compact static branch at "
            "boundary and tensor-ledger level.  This upgrades the p05u "
            "conditional theorem from a free boundary assumption to a concrete "
            "candidate core-matching ansatz, but it still does not prove the "
            "physical branch-selection dynamics."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18v: Finite-core boundary feed gate")
    print("=" * 72)
    sections = [
        ("1. C2 boundary data feed", derive_c2_boundary_data_feeds_p05u_gate()),
        ("2. C2 source boundary continuity", derive_c2_source_boundary_continuity_gate()),
        ("3. Throat/cutoff domain", derive_throat_cutoff_domain_gate()),
        ("4. Central finite-core boundary feed", derive_finite_core_boundary_feed_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:52s}: {value}")
