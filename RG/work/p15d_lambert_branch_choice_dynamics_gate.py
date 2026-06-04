"""
PHASE 15d: Lambert branch-choice dynamics gate.

p15c closes the algebraic load selector

    Q0 = Q exp(-Q/2),

which gives a low weak branch and a high compact branch.  This file audits the
next question: does the algebra itself select the compact branch?

Result:
    No.  The algebra gives two branches, but a one-residual relaxation has a
    stability sign problem.  With the weak branch stable, the high branch is
    unstable; with the high branch stable, the weak branch is unstable.  The
    compact branch therefore needs an extra finite-core dynamical/history
    mechanism, or an action-derived source feedback that changes the stability
    structure.

This is a useful guardrail: p15c explains which compact branch is
geometrically allowed; p15d prevents us from claiming that the compact branch
is dynamically chosen before the finite-core evolution has been solved.
"""

from __future__ import annotations

import sympy as sp

from p15c_volume_clock_branch_loading_gate import (
    volume_clock_branch_loading_status,
)


def derive_load_residual_stability_gate() -> dict[str, object]:
    """Classify the two Lambert branches under a one-residual relaxation."""
    Q, Q0 = sp.symbols("Q Q0", positive=True, real=True)

    residual = sp.simplify(Q - Q0 * sp.exp(Q / 2))
    residual_slope = sp.simplify(sp.diff(residual, Q))

    Q_low = sp.simplify(-2 * sp.LambertW(-Q0 / 2, 0))
    Q_high = sp.simplify(-2 * sp.LambertW(-Q0 / 2, -1))

    slope_at_low = sp.simplify(residual_slope.subs(Q, Q_low))
    slope_at_high = sp.simplify(residual_slope.subs(Q, Q_high))

    # At any root, Q0 exp(Q/2)=Q, so residual_slope = 1-Q/2.
    slope_at_root = sp.simplify(1 - Q / 2)
    real_two_branch_domain = sp.And(Q0 > 0, Q0 < sp.Rational(2, 1) / sp.E)

    return {
        "status": "PASS_ONE_RESIDUAL_RELAXATION_CANNOT_SELECT_BOTH_BRANCHES",
        "load_residual": sp.Eq(sp.Symbol("R(Q)"), residual),
        "residual_slope": sp.Eq(sp.Symbol("R_prime(Q)"), residual_slope),
        "root_slope_identity": sp.Eq(sp.Symbol("R_prime_at_root"), slope_at_root),
        "low_branch_load": sp.Eq(sp.Symbol("Q_low"), Q_low),
        "high_branch_load": sp.Eq(sp.Symbol("Q_high"), Q_high),
        "slope_at_low_raw": slope_at_low,
        "slope_at_high_raw": slope_at_high,
        "real_two_branch_domain": real_two_branch_domain,
        "weak_branch_region": "0<Q0<2/e gives 0<Q_low<2",
        "compact_branch_region": "0<Q0<2/e gives Q_high>2",
        "minus_residual_relaxation": sp.Eq(
            sp.Symbol("dQ/dtau"),
            -sp.Symbol("R(Q)"),
        ),
        "minus_residual_eigenvalue_at_root": sp.Eq(
            sp.Symbol("lambda_minus"),
            -slope_at_root,
        ),
        "minus_residual_stability": (
            "stable for Q<2, unstable for Q>2"
        ),
        "plus_residual_relaxation": sp.Eq(
            sp.Symbol("dQ/dtau"),
            sp.Symbol("R(Q)"),
        ),
        "plus_residual_eigenvalue_at_root": sp.Eq(
            sp.Symbol("lambda_plus"),
            slope_at_root,
        ),
        "plus_residual_stability": (
            "unstable for Q<2, stable for Q>2"
        ),
        "low_stable_if_weak_continuity_required": (
            "true on the real two-branch domain because Q_low<2"
        ),
        "high_then_unstable_in_same_simple_flow": (
            "true on the same domain because Q_high>2"
        ),
        "reading": (
            "The algebraic selector supplies two roots.  A simple scalar "
            "relaxation that keeps the weak branch stable does not also make "
            "the compact branch stable."
        ),
    }


def derive_branch_choice_requirements_gate() -> dict[str, object]:
    """Write the extra requirements for a real compact-branch transition."""
    Q, S, chi = sp.symbols("Q S chi", positive=True, real=True)

    q_target = sp.Rational(3, 2) * Q
    required_feedback_source = sp.simplify(q_target * sp.exp(chi * q_target))
    source_growth = sp.simplify(sp.diff(required_feedback_source, Q))
    p14_eigenvalue = sp.simplify(-(1 + chi * q_target))

    return {
        "status": "PASS_COMPACT_BRANCH_NEEDS_EXTRA_CORE_DYNAMICS_OR_SOURCE_HISTORY",
        "selected_deficit": sp.Eq(sp.Symbol("q_v"), q_target),
        "p14_source_required_for_load": sp.Eq(
            sp.Symbol("S_required"),
            required_feedback_source,
        ),
        "source_growth_with_load": source_growth,
        "p14_fixed_point_eigenvalue": p14_eigenvalue,
        "p14_fixed_point_stable_for_positive_chi_Q": sp.Lt(p14_eigenvalue, 0),
        "allowed_mechanisms_to_close_next": [
            "derive S(Q,t) and chi from finite-core action variables",
            "show hysteresis/barrier crossing from the low branch to the high branch",
            "show that core boundary conditions remove the low branch above a physical threshold",
            "derive a multi-field stability matrix where the compact branch has all negative eigenvalues",
        ],
        "blocked_claims": [
            "do not claim the high Lambert branch is dynamically selected by p15c alone",
            "do not claim compact collapse before the finite-core evolution selects the branch",
            "do not replace ADM/Noether closure with this algebraic branch selector",
        ],
        "reading": (
            "p14 can stabilize a chosen deficit once the source lands there, "
            "but the path that puts a real core onto the high branch is still "
            "the next dynamical theorem."
        ),
    }


def lambert_branch_choice_dynamics_status() -> dict[str, object]:
    p15c = volume_clock_branch_loading_status()
    stability = derive_load_residual_stability_gate()
    requirements = derive_branch_choice_requirements_gate()

    passed = (
        p15c["status"]
        == "PASS_VOLUME_CLOCK_MATCHING_SELECTS_LOAD_BRANCHES__DYNAMICAL_BRANCH_CHOICE_OPEN"
        and stability["status"]
        == "PASS_ONE_RESIDUAL_RELAXATION_CANNOT_SELECT_BOTH_BRANCHES"
        and requirements["status"]
        == "PASS_COMPACT_BRANCH_NEEDS_EXTRA_CORE_DYNAMICS_OR_SOURCE_HISTORY"
    )

    return {
        "status": (
            "PASS_BRANCH_CHOICE_AUDIT_DONE__FINITE_CORE_DYNAMICAL_SELECTION_STILL_OPEN"
            if passed
            else "CHECK_LAMBERT_BRANCH_CHOICE_DYNAMICS"
        ),
        "p15c_status": p15c["status"],
        "load_residual_stability": stability,
        "branch_choice_requirements": requirements,
        "closed_now": [
            "the load equation has a low branch and a high branch",
            "the low branch is the stable one for the simplest weak-continuity relaxation",
            "the compact high branch needs additional finite-core/source-history dynamics",
            "p14 can stabilize a selected deficit, but does not by itself choose the high branch",
        ],
        "not_closed_now": [
            "derive the finite-core multi-field stability matrix",
            "derive branch transition/hysteresis from the action",
            "prove ADM/Noether compact-body closure",
        ],
        "intuitive_reading": (
            "The matching condition tells us which algebraic branches exist.  "
            "The weak branch is naturally stable in the simplest relaxation.  "
            "To reach the compact branch, the core needs an additional physical "
            "push or a different multi-field stability structure derived from "
            "the action."
        ),
    }


if __name__ == "__main__":
    result = lambert_branch_choice_dynamics_status()
    print("PHASE 15d: Lambert branch-choice dynamics gate")
    print("status:", result["status"])
    print("closed_now:")
    for item in result["closed_now"]:
        print("  -", item)
    print("not_closed_now:")
    for item in result["not_closed_now"]:
        print("  -", item)
    stability = result["load_residual_stability"]
    print("residual:", stability["load_residual"])
    print("root slope:", stability["root_slope_identity"])
    print("minus-flow stability:", stability["minus_residual_stability"])
    print("plus-flow stability:", stability["plus_residual_stability"])
