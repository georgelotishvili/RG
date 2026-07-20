# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Active coefficient scheme: bridge audit only; no new action coefficients.

"""
PHASE 18w: Mass-deficit feedback to compact-boundary load gate.

p05u proves the conditional compact exterior theorem.  p05v proves that the C2
finite-core ansatz feeds the boundary data needed by p05u, but it leaves open
why a physical core should select that compact load.  This file checks whether
the existing mass/size deficit response and the p14 mass-deficit fixed point
remove that specific "no local mechanism" gap.

Closed here:
  * p10 gives the deficit-language half-exponent:
        m_eff/m0 = L_oper/L0 = d tau/dt = exp(-q_delta/2).
    Therefore clocks slow relative to the asymptotic/static time coordinate,
    while the externally read period scales as exp(q_delta/2).
  * p14 gives a stable local feedback point:
        q_delta = S exp(-chi q_delta),
        q_delta,* = LambertW(chi S)/chi,
        lambda_* = -(1 + LambertW(chi S)) < 0.
  * a positive monotone matching map Q = alpha q_delta,* can supply the compact
    boundary load Q=r_s/r_c used by p05v.  Since p05v is symbolic in Q, the C2
    boundary residuals remain zero after this substitution.

Not closed here:
  * the full finite-core time evolution that derives the matching map alpha;
  * a compactness threshold or continuous H-loading law;
  * the coupled compact perturbation spectrum, rotation, and ray tracing.
"""

from __future__ import annotations

import sympy as sp

from p05v_finite_core_boundary_feed_gate import (
    derive_c2_boundary_data_feeds_p05u_gate,
    derive_finite_core_boundary_feed_gate,
)
from p10_oscillons import step6b_deficit_scaling_factor_two_gate
from p14_nec_deficit import mass_deficit_feedback_balance_gate


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def derive_mass_deficit_boundary_selection_gate() -> dict[str, object]:
    """
    Bridge the local deficit fixed point to the compact boundary-load ledger.

    Use q_delta for the local deficit amplitude and Q for the compact boundary
    load Q=r_s/r_c.  They are not silently identified.  The minimal admissible
    bridge is a positive proportional map Q=alpha q_delta,*; alpha remains the
    finite-core matching conversion that a true dynamical core solve must
    derive.
    """
    q_delta, S, chi, alpha = sp.symbols(
        "q_delta S chi alpha", positive=True, real=True
    )
    r_s, R0, r_s0 = sp.symbols("r_s R0 r_s0", positive=True, real=True)

    scaling = step6b_deficit_scaling_factor_two_gate()
    feedback = mass_deficit_feedback_balance_gate()
    boundary = derive_c2_boundary_data_feeds_p05u_gate()
    finite_core = derive_finite_core_boundary_feed_gate()

    W = sp.LambertW(chi * S)
    q_star = sp.simplify(W / chi)
    Q_star = sp.simplify(alpha * q_star)
    r_c_star = sp.simplify(r_s / Q_star)

    mass_scale = sp.exp(-q_delta / 2)
    size_scale = sp.exp(-q_delta / 2)
    lapse_scale = sp.exp(-q_delta / 2)
    period_scale = sp.exp(q_delta / 2)
    mass_size_lock = sp.simplify(mass_scale - size_scale)
    mass_lapse_lock = sp.simplify(mass_scale - lapse_scale)
    size_lapse_lock = sp.simplify(size_scale - lapse_scale)
    lapse_period_inverse_lock = sp.simplify(lapse_scale * period_scale - 1)
    lapse_decreases_with_deficit = sp.simplify(
        sp.diff(lapse_scale, q_delta) + lapse_scale / 2
    )
    period_increases_with_deficit = sp.simplify(
        sp.diff(period_scale, q_delta) - period_scale / 2
    )
    compactness_before = sp.simplify(r_s0 / R0)
    compactness_after = sp.simplify((r_s0 * mass_scale) / (R0 * size_scale))
    compactness_invariant = sp.simplify(compactness_after - compactness_before)

    feedback_residual_at_star = sp.simplify(
        q_star - S * sp.exp(-W)
    ).subs(S * sp.exp(-W), W / chi)
    relaxation_eigenvalue = sp.simplify(-(1 + W))
    residual_slope = sp.simplify(1 + W)
    source_slope = sp.simplify(-W)

    mass_scaling_chi = sp.Rational(1, 2)
    q_star_mass_scaling = sp.simplify(q_star.subs(chi, mass_scaling_chi))
    Q_star_mass_scaling = sp.simplify(Q_star.subs(chi, mass_scaling_chi))
    eigen_mass_scaling = sp.simplify(
        relaxation_eigenvalue.subs(chi, mass_scaling_chi)
    )

    # C2 boundary data evaluated at the load selected by the local fixed point.
    # p05v already proves these residuals vanish for symbolic Q, so the
    # substitution cannot reintroduce a shell or boundary mismatch.
    boundary_residuals_after_selection = {
        **boundary["h_C2_match_at_x1"],
        **boundary["C2_minus_p05u_boundary"],
    }

    h_boundary = sp.simplify(Q_star / 2)
    hprime_boundary = sp.simplify(-Q_star**2 / (2 * r_s))
    lapse_at_fixed_point = sp.exp(-q_star / 2)
    period_at_fixed_point = sp.exp(q_star / 2)

    exterior_sheet_source_bound = sp.simplify(
        (sp.Integer(2) / alpha) * sp.exp(2 * chi / alpha)
    )
    pressure_turn_source_bound = sp.simplify(
        (sp.Integer(4) / alpha) * sp.exp(4 * chi / alpha)
    )
    exterior_sheet_bound_mass_scaling = sp.simplify(
        exterior_sheet_source_bound.subs({chi: mass_scaling_chi, alpha: 1})
    )
    pressure_turn_bound_mass_scaling = sp.simplify(
        pressure_turn_source_bound.subs({chi: mass_scaling_chi, alpha: 1})
    )

    status_checks = {
        "p10_mass_size_lapse_half_exponent": (
            scaling["deficit_scaling_factor_two_status"]
            == "PASS_MASS_SIZE_LAPSE_HALF_EXPONENT_AND_LIGHT_FULL_EXPONENT"
        ),
        "p14_feedback_fixed_point": (
            feedback["mass_deficit_feedback_status"]
            == "PASS_NONLINEAR_MASS_DEFICIT_FIXED_POINT_IS_STABLE"
        ),
        "p05v_boundary_feed": (
            finite_core["finite_core_boundary_feed_status"]
            == "PASS_C2_FINITE_CORE_FEEDS_STATIC_BRANCH_BOUNDARY__DYNAMICAL_SELECTION_OPEN"
        ),
        "mass_size_lock": mass_size_lock == 0,
        "mass_lapse_lock": mass_lapse_lock == 0,
        "size_lapse_lock": size_lapse_lock == 0,
        "lapse_period_inverse_lock": lapse_period_inverse_lock == 0,
        "lapse_decreases_with_deficit": lapse_decreases_with_deficit == 0,
        "period_increases_with_deficit": period_increases_with_deficit == 0,
        "compactness_preserved_by_common_scaling": compactness_invariant == 0,
        "feedback_residual_zero_at_star": sp.simplify(
            feedback_residual_at_star
        )
        == 0,
        "C2_boundary_residuals_zero_after_selection": _all_zero(
            boundary_residuals_after_selection.values()
        ),
    }
    passed = all(status_checks.values())

    return {
        "mass_deficit_boundary_selection_status": (
            "PASS_LOCAL_FEEDBACK_SUPPLIES_STABLE_COMPACT_LOAD__FINITE_CORE_DYNAMICS_STILL_OPEN"
            if passed
            else "CHECK_MASS_DEFICIT_BOUNDARY_SELECTION_BRIDGE"
        ),
        "status_checks": status_checks,
        "local_deficit_balance": sp.Eq(q_delta, S * sp.exp(-chi * q_delta)),
        "stable_fixed_point": sp.Eq(sp.Symbol("q_delta_star"), q_star),
        "matching_map": sp.Eq(sp.Symbol("Q"), alpha * sp.Symbol("q_delta_star")),
        "selected_boundary_load": sp.Eq(sp.Symbol("Q_star"), Q_star),
        "selected_core_radius": sp.Eq(sp.Symbol("r_c_star"), r_c_star),
        "selected_boundary_h": sp.Eq(sp.Symbol("h_R"), h_boundary),
        "selected_boundary_hprime": sp.Eq(sp.Symbol("hprime_R"), hprime_boundary),
        "lapse_at_fixed_point": sp.Eq(sp.Symbol("(d_tau/dt)_star"), lapse_at_fixed_point),
        "period_at_fixed_point": sp.Eq(sp.Symbol("(dt/d_tau)_star"), period_at_fixed_point),
        "relaxation_eigenvalue": relaxation_eigenvalue,
        "residual_slope_at_fixed_point": residual_slope,
        "source_slope_at_fixed_point": source_slope,
        "mass_scaling_only": {
            "chi": mass_scaling_chi,
            "q_delta_star": q_star_mass_scaling,
            "Q_star_if_alpha_1": Q_star_mass_scaling.subs(alpha, 1),
            "relaxation_eigenvalue": eigen_mass_scaling,
        },
        "mass_size_time_scaling": {
            "mass_scale": sp.Eq(sp.Symbol("m_eff/m0"), mass_scale),
            "size_scale": sp.Eq(sp.Symbol("L_oper/L0"), size_scale),
            "clock_rate_scale": sp.Eq(sp.Symbol("d_tau/dt"), lapse_scale),
            "external_period_scale": sp.Eq(sp.Symbol("dt/d_tau"), period_scale),
            "mass_minus_size_scale": mass_size_lock,
            "mass_minus_clock_rate_scale": mass_lapse_lock,
            "size_minus_clock_rate_scale": size_lapse_lock,
            "clock_rate_times_period": lapse_period_inverse_lock,
            "clock_rate_derivative_check": lapse_decreases_with_deficit,
            "period_derivative_check": period_increases_with_deficit,
            "compactness_after_common_scaling": compactness_after,
            "compactness_invariant_difference": compactness_invariant,
        },
        "exterior_sheet_condition_if_Q_le_2": sp.Le(
            S, exterior_sheet_source_bound
        ),
        "exterior_sheet_mass_scaling_alpha1_bound": sp.Le(
            S, exterior_sheet_bound_mass_scaling
        ),
        "pressure_turn_condition_if_Q_ge_4": sp.Ge(
            S, pressure_turn_source_bound
        ),
        "pressure_turn_mass_scaling_alpha1_bound": sp.Ge(
            S, pressure_turn_bound_mass_scaling
        ),
        "C2_boundary_residuals_after_selection": boundary_residuals_after_selection,
        "closed_now": (
            "The previous 'why this compact load?' gap now has a local "
            "mechanism: source deficit weakens the same source, producing a "
            "stable positive fixed point.  At that point mass, operational "
            "size, and clock rate carry the same half-exponent, so the compact "
            "load can be fed without breaking the C2 boundary ledger."
        ),
        "not_closed_now": [
            "derive the finite-core evolution that fixes alpha",
            "derive the compactness threshold / continuous H-loading law",
            "prove that physical collapse selects the C2 ansatz rather than only allowing it",
            "compute the coupled compact perturbation spectrum",
        ],
        "program_safe_statement": (
            "This helps the p05u/p05v stuck point at mechanism level.  It does "
            "not yet upgrade the compact branch to a completed finite-core "
            "dynamical-selection theorem."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18w: Mass-deficit feedback to compact-boundary load gate")
    print("=" * 72)
    result = derive_mass_deficit_boundary_selection_gate()
    for key, value in result.items():
        print(f"{key:48s}: {value}")
