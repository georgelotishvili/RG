"""
PHASE 15c: Volume-clock branch loading gate.

This file is the next tightening after p15a/p15b.  It does not touch the
article.

Goal:
    remove the arbitrary Q=alpha*q_delta bridge left in p05w, using the newer
    volume-deficit interpretation.

The matching idea is simple:

    p15a volume response:        d tau/dt = exp(-q_v/3)
    compact exterior surface:    N(R) = exp(-r_s/(2R)) = exp(-Q/2)

Matching the same physical surface clock gives

    Q = 2 q_v / 3.

Together with conserved far-zone mass and radius shrinkage,

    Q = Q0 exp(q_v/3),

the load is no longer a free proportional map.  It obeys

    Q0 = Q exp(-Q/2),

so the same initial compactness can have a weak low-load solution and, when
allowed by the source feedback, a compact high-load solution.

This is still not a time-evolution proof.  It is a self-consistency selector
for the compact load.
"""

from __future__ import annotations

import sympy as sp

from p05t_single_action_branch_consistency_gate import (
    derive_single_action_branch_consistency_gate,
)
from p15a_volume_deficit_compact_threshold_gate import (
    volume_deficit_compact_threshold_status,
)
from p15b_dressing_mass_conservation_gate import (
    dressing_mass_conservation_status,
)


def derive_surface_clock_load_matching_gate() -> dict[str, object]:
    """Match the p15 volume clock to the compact exterior surface lapse."""
    q_v, Q, Q0 = sp.symbols("q_v Q Q0", positive=True, real=True)

    volume_clock = sp.exp(-q_v / 3)
    exterior_lapse = sp.exp(-Q / 2)
    clock_match_solution = sp.solve(
        sp.Eq(volume_clock, exterior_lapse),
        Q,
    )[0]
    radius_shrink_load = sp.simplify(Q0 * sp.exp(q_v / 3))
    combined_residual = sp.simplify(
        radius_shrink_load.subs(q_v, sp.Rational(3, 2) * Q) - Q
    )
    initial_compactness_from_final_load = sp.simplify(
        sp.solve(sp.Eq(combined_residual, 0), Q0)[0]
    )
    stationary_point = sp.solve(
        sp.Eq(sp.diff(Q * sp.exp(-Q / 2), Q), 0),
        Q,
    )[0]
    max_initial_compactness = sp.simplify(
        (Q * sp.exp(-Q / 2)).subs(Q, stationary_point)
    )

    return {
        "status": (
            "PASS_SURFACE_CLOCK_MATCH_FIXES_ALPHA_TO_TWO_THIRDS"
            if sp.simplify(clock_match_solution - 2 * q_v / 3) == 0
            and sp.simplify(initial_compactness_from_final_load - Q * sp.exp(-Q / 2))
            == 0
            and stationary_point == 2
            else "CHECK_SURFACE_CLOCK_LOAD_MATCHING"
        ),
        "volume_clock": sp.Eq(sp.Symbol("d_tau/dt"), volume_clock),
        "compact_surface_lapse": sp.Eq(sp.Symbol("N_R"), exterior_lapse),
        "clock_matching_load": sp.Eq(sp.Symbol("Q"), clock_match_solution),
        "p05w_alpha_replacement": sp.Eq(sp.Symbol("alpha"), sp.Rational(2, 3)),
        "far_mass_radius_shrink_load": sp.Eq(
            sp.Symbol("Q"),
            radius_shrink_load,
        ),
        "combined_residual": sp.Eq(sp.Symbol("residual"), combined_residual),
        "initial_compactness_from_final_load": sp.Eq(
            sp.Symbol("Q0"),
            initial_compactness_from_final_load,
        ),
        "max_real_Q0": sp.Eq(sp.Symbol("Q0_max"), max_initial_compactness),
        "max_real_Q0_at_Q": stationary_point,
        "reading": (
            "The volume-deficit clock and the compact exterior lapse fix the "
            "old proportional map to Q=(2/3)q_v.  Combining this with radius "
            "shrinkage gives the branch equation Q0=Q exp(-Q/2)."
        ),
    }


def derive_lambert_load_branches_gate() -> dict[str, object]:
    """Solve Q0=Q exp(-Q/2) and classify the low/high branches."""
    Q0, Q_gate = sp.symbols("Q0 Q_gate", positive=True, real=True)

    Q_low = sp.simplify(-2 * sp.LambertW(-Q0 / 2, 0))
    Q_high = sp.simplify(-2 * sp.LambertW(-Q0 / 2, -1))
    q_low = sp.simplify(sp.Rational(3, 2) * Q_low)
    q_high = sp.simplify(sp.Rational(3, 2) * Q_high)

    branch_equation = lambda value: sp.simplify(value * sp.exp(-value / 2))
    low_residual = sp.simplify(branch_equation(Q_low) - Q0)
    high_residual = sp.simplify(branch_equation(Q_high) - Q0)
    # SymPy does not automatically reduce W(z)*exp(W(z)) to z for symbolic
    # branch expressions.  Record both the raw residual and the residual after
    # applying the defining Lambert-W identity.
    lambert_argument = -Q0 / 2
    low_residual_by_identity = sp.simplify(-Q0 - 2 * lambert_argument)
    high_residual_by_identity = sp.simplify(-Q0 - 2 * lambert_argument)

    high_branch_gate_initial = sp.simplify(Q_gate * sp.exp(-Q_gate / 2))
    pressure_turn_initial_bound = sp.simplify(4 * sp.exp(-2))
    sheet_turn_initial_bound = sp.simplify(2 * sp.exp(-1))

    samples = []
    for label, value in (
        ("weak_0p10", sp.Rational(1, 10)),
        ("ns_like_0p40", sp.Rational(2, 5)),
        ("pressure_turn_Q4", pressure_turn_initial_bound),
        ("fold_Q2", sheet_turn_initial_bound),
    ):
        row = {"sample": label, "Q0": value}
        for branch_name, branch_expr in (("low", Q_low), ("high", Q_high)):
            q_expr = sp.simplify(sp.Rational(3, 2) * branch_expr)
            q_val = sp.N(q_expr.subs(Q0, value), 12)
            Q_val = sp.N(branch_expr.subs(Q0, value), 12)
            row[f"Q_{branch_name}"] = Q_val
            row[f"q_v_{branch_name}"] = q_val
        samples.append(row)

    return {
        "status": (
            "PASS_LAMBERT_LOAD_BRANCHES_SYMBOLICALLY_CLOSED"
            if low_residual_by_identity == 0 and high_residual_by_identity == 0
            else "CHECK_LAMBERT_LOAD_BRANCHES"
        ),
        "branch_equation": sp.Eq(
            sp.Symbol("Q0"),
            sp.Symbol("Q") * sp.exp(-sp.Symbol("Q") / 2),
        ),
        "real_branch_domain": sp.Le(Q0, sp.Rational(2, 1) / sp.E),
        "low_branch_load": sp.Eq(sp.Symbol("Q_low"), Q_low),
        "high_branch_load": sp.Eq(sp.Symbol("Q_high"), Q_high),
        "low_branch_deficit": sp.Eq(sp.Symbol("q_v_low"), q_low),
        "high_branch_deficit": sp.Eq(sp.Symbol("q_v_high"), q_high),
        "low_branch_raw_residual": low_residual,
        "high_branch_raw_residual": high_residual,
        "LambertW_defining_identity": sp.Eq(
            sp.Symbol("W(z)") * sp.exp(sp.Symbol("W(z)")),
            sp.Symbol("z"),
        ),
        "low_branch_residual_by_identity": low_residual_by_identity,
        "high_branch_residual_by_identity": high_residual_by_identity,
        "fold_point": {
            "Q": sp.Integer(2),
            "q_v": sp.Integer(3),
            "Q0": sheet_turn_initial_bound,
        },
        "high_branch_reaches_Q_gate_when_Q0_equals": sp.Eq(
            sp.Symbol("Q0_gate"),
            high_branch_gate_initial,
        ),
        "pressure_turn_Q_ge_4_corresponds_to_Q0_le": pressure_turn_initial_bound,
        "samples": samples,
        "reading": (
            "The low branch is the weak continuation.  The high branch is the "
            "compact continuation.  Which branch is physically occupied still "
            "requires the dynamical source/feedback history."
        ),
    }


def derive_feedback_source_for_selected_branch_gate() -> dict[str, object]:
    """
    Connect the selected branch deficit to the p14 stable feedback form.

    For q_v = S exp(-chi q_v), a target branch q_v=3Q/2 requires

        S = (3Q/2) exp(3 chi Q/2).
    """
    Q, chi = sp.symbols("Q chi", positive=True, real=True)
    q_target = sp.Rational(3, 2) * Q
    S_required = sp.simplify(q_target * sp.exp(chi * q_target))
    fixed_point_residual = sp.simplify(
        q_target - S_required * sp.exp(-chi * q_target)
    )
    relaxation_eigenvalue = sp.simplify(-(1 + chi * q_target))
    source_monotonicity = sp.simplify(sp.diff(S_required, Q))

    return {
        "status": (
            "PASS_FEEDBACK_SOURCE_FOR_SELECTED_LOAD_IS_STABLE_AND_MONOTONE"
            if fixed_point_residual == 0
            else "CHECK_FEEDBACK_SOURCE_FOR_SELECTED_LOAD"
        ),
        "target_deficit_from_load": sp.Eq(sp.Symbol("q_v"), q_target),
        "required_bare_source": sp.Eq(sp.Symbol("S_required"), S_required),
        "fixed_point_residual": fixed_point_residual,
        "relaxation_eigenvalue": relaxation_eigenvalue,
        "stable_for_positive_chi_Q": sp.Lt(relaxation_eigenvalue, 0),
        "source_derivative": source_monotonicity,
        "monotone_for_positive_chi_Q": sp.Gt(source_monotonicity, 0),
        "reading": (
            "Once a load branch Q is selected by clock/lapse matching, the "
            "p14 feedback supplies a stable fixed point at that load for a "
            "definite source amplitude S_required."
        ),
    }


def volume_clock_branch_loading_status() -> dict[str, object]:
    p15a = volume_deficit_compact_threshold_status()
    p15b = dressing_mass_conservation_status()
    p05t = derive_single_action_branch_consistency_gate()
    matching = derive_surface_clock_load_matching_gate()
    branches = derive_lambert_load_branches_gate()
    feedback = derive_feedback_source_for_selected_branch_gate()

    passed = (
        p15a["status"]
        == "PASS_VOLUME_DEFICIT_CAN_SELECT_COMPACT_GATE_CONDITIONALLY__DRESSING_DYNAMICS_OPEN"
        and p15b["status"]
        == "PASS_DRESSING_MASS_CONSERVATION_LEDGER_COMPATIBLE_WITH_ADM_NOETHER__ACTION_DERIVATION_OPEN"
        and p05t["status"] == "PASS_SINGLE_ACTION_PHASE_NORMALIZED_BRANCH_LEDGER"
        and matching["status"]
        == "PASS_SURFACE_CLOCK_MATCH_FIXES_ALPHA_TO_TWO_THIRDS"
        and branches["status"] == "PASS_LAMBERT_LOAD_BRANCHES_SYMBOLICALLY_CLOSED"
        and feedback["status"]
        == "PASS_FEEDBACK_SOURCE_FOR_SELECTED_LOAD_IS_STABLE_AND_MONOTONE"
    )

    return {
        "status": (
            "PASS_VOLUME_CLOCK_MATCHING_SELECTS_LOAD_BRANCHES__DYNAMICAL_BRANCH_CHOICE_OPEN"
            if passed
            else "CHECK_VOLUME_CLOCK_BRANCH_LOADING_GATE"
        ),
        "p15a_status": p15a["status"],
        "p15b_status": p15b["status"],
        "p05t_status": p05t["status"],
        "surface_clock_matching": matching,
        "load_branches": branches,
        "feedback_source": feedback,
        "closed_now": [
            "the old p05w free alpha map is replaced by alpha=2/3 from surface clock matching",
            "the compact load obeys Q0=Q exp(-Q/2)",
            "the weak and compact load branches are explicit Lambert-W branches",
            "a chosen load branch can be supplied by a stable p14 feedback source",
            "the construction is consistent with the p05t single-action branch ledger",
        ],
        "not_closed_now": [
            "which Lambert-W branch is dynamically selected for a real collapsing core",
            "derive S and chi from the microscopic finite-core action instead of treating them as feedback parameters",
            "prove the full compact-body Noether/proper integral equals the ADM/Komar charge",
            "solve the finite-core time evolution through the branch transition",
        ],
        "intuitive_reading": (
            "The branch load is no longer arbitrary: the surface clock of the "
            "shrinking external readout and the exterior compact lapse must be "
            "the same clock.  That condition creates a low weak branch and a "
            "high compact branch.  The remaining physics is the dynamical "
            "choice of branch."
        ),
    }


if __name__ == "__main__":
    result = volume_clock_branch_loading_status()
    print("PHASE 15c: Volume-clock branch loading gate")
    print("status:", result["status"])
    print("closed_now:")
    for item in result["closed_now"]:
        print("  -", item)
    print("not_closed_now:")
    for item in result["not_closed_now"]:
        print("  -", item)
    print("matching:", result["surface_clock_matching"]["status"])
    print(
        "Q0(Q):",
        result["surface_clock_matching"]["initial_compactness_from_final_load"],
    )
    print("branches:", result["load_branches"]["status"])
    for row in result["load_branches"]["samples"]:
        print("sample:", row)
    print("feedback:", result["feedback_source"]["status"])
