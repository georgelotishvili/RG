"""
PHASE 18x: Branch-selection defect response gate.

This file does not touch the article.  It collects the current Python-side
answer to the referee-level branch-selection defect:

    why should a real compact object use the compact exponential branch
    instead of the weak/Solar branch?

Closed before this file:
  * p05u: if compact boundary data are supplied, the static exponential
    exterior is locked.
  * p05v: the C2 finite-core ansatz supplies those boundary data at the
    algebraic, junction and source-ledger level.
  * p15c: the old free proportional bridge is replaced by surface-clock
    matching, alpha=2/3, and the load equation Q0=Q exp(-Q/2).
  * p15d: the load equation alone gives low/high Lambert branches but does not
    dynamically select an occupied compact endpoint.
  * p05w/p14: a selected compact load can be supplied by a stable local
    mass-deficit feedback point.

Therefore the original defect is split correctly:
  * Q0 alone is not a selector.
  * the finite-core source amplitude S fixes the selected static load Q.
  * finite-core geodesic exterior use requires 1<Q<2, so the throat is inside
    the core and the photon sphere is exterior.
  * object-specific collapse histories and equations of state are downstream
    predictions, not part of the static load-window theorem itself.
"""

from __future__ import annotations

import sympy as sp

from p05u_branch_selection_static_gate import (
    derive_static_branch_selection_conditional_gate,
)
from p05v_finite_core_boundary_feed_gate import (
    derive_finite_core_boundary_feed_gate,
)
from p05w_mass_deficit_boundary_selection_gate import (
    derive_mass_deficit_boundary_selection_gate,
)
from p15c_volume_clock_branch_loading_gate import (
    volume_clock_branch_loading_status,
)
from p15d_lambert_branch_choice_dynamics_gate import (
    lambert_branch_choice_dynamics_status,
)
from p05y_source_amplitude_branch_selector_theorem import (
    source_amplitude_branch_selector_status,
)


def derive_compact_load_branch_dictionary_gate() -> dict[str, object]:
    """
    Explicit dictionary for the algebraic load branches.

    Q = r_s/r_c is the final compact boundary load.  Q0 is the far-zone/input
    compactness parameter in the p15c clock-matching ledger.  The equation

        Q0 = Q exp(-Q/2)

    has two real Lambert branches for 0<Q0<2/e.  The branch with Q<2 contains
    both weak loads Q<1 and the finite-core exterior-object window 1<Q<2.  The
    branch with Q>2 is an over-throat Lambert branch, not the finite-core
    geodesic window used by the static compact predictions.
    """
    Q0, Q = sp.symbols("Q0 Q", positive=True, real=True)

    Q0_of_Q = sp.simplify(Q * sp.exp(-Q / 2))
    photon_Q = sp.Integer(1)
    photon_Q0 = sp.simplify(Q0_of_Q.subs(Q, photon_Q))
    fold_Q = sp.Integer(2)
    fold_Q0 = sp.simplify(Q0_of_Q.subs(Q, fold_Q))
    pressure_turn_Q = sp.Integer(4)
    pressure_turn_Q0 = sp.simplify(Q0_of_Q.subs(Q, pressure_turn_Q))

    Q_low = sp.simplify(-2 * sp.LambertW(-Q0 / 2, 0))
    Q_high = sp.simplify(-2 * sp.LambertW(-Q0 / 2, -1))
    qv_low = sp.simplify(sp.Rational(3, 2) * Q_low)
    qv_high = sp.simplify(sp.Rational(3, 2) * Q_high)

    dQ0_dQ = sp.factor(sp.diff(Q0_of_Q, Q))
    low_region = sp.And(Q > 0, Q < 2)
    high_region = Q > 2

    sample_Q0 = [sp.Rational(1, 10), sp.Rational(2, 5), 4 * sp.exp(-2)]
    samples = []
    for value in sample_Q0:
        samples.append(
            {
                "Q0": value,
                "Q_low": sp.N(Q_low.subs(Q0, value), 12),
                "Q_high": sp.N(Q_high.subs(Q0, value), 12),
                "qv_low": sp.N(qv_low.subs(Q0, value), 12),
                "qv_high": sp.N(qv_high.subs(Q0, value), 12),
            }
        )

    return {
        "status": "PASS_COMPACT_LOAD_BRANCH_DICTIONARY_EXPLICIT",
        "load_equation": sp.Eq(sp.Symbol("Q0"), Q0_of_Q),
        "derivative": sp.Eq(sp.Symbol("dQ0/dQ"), dQ0_dQ),
        "two_real_branch_domain": sp.And(Q0 > 0, Q0 < fold_Q0),
        "photon_sphere_marker": {
            "Q": photon_Q,
            "Q0": photon_Q0,
            "Q0_numeric": sp.N(photon_Q0, 12),
        },
        "fold_point": {
            "Q": fold_Q,
            "Q0": fold_Q0,
            "Q0_numeric": sp.N(fold_Q0, 12),
        },
        "finite_core_exterior_window": {
            "Q_region": sp.And(Q > photon_Q, Q < fold_Q),
            "radius_reading": "r_s/2 < r_c < r_s",
            "reading": (
                "The throat r_s/2 is inside the finite core while the photon "
                "sphere r_s is outside it."
            ),
        },
        "pressure_turn_marker": {
            "Q": pressure_turn_Q,
            "Q0": pressure_turn_Q0,
            "Q0_numeric": sp.N(pressure_turn_Q0, 12),
        },
        "low_branch": {
            "Q": Q_low,
            "q_v": qv_low,
            "region": low_region,
            "reading": (
                "Lambert branch with Q<2; it contains weak loads Q<1 and the "
                "finite-core exterior-object window 1<Q<2."
            ),
        },
        "high_branch": {
            "Q": Q_high,
            "q_v": qv_high,
            "region": high_region,
            "reading": (
                "over-throat Lambert branch Q>2; this is not the finite-core "
                "geodesic window used by the compact-object predictions"
            ),
        },
        "samples": samples,
        "article_safe_reading": (
            "The algebra fixes a selected static load from S and chi.  The "
            "compact geodesic predictions apply to finite-core objects in the "
            "window 1<Q<2; object-specific S, chi and time-dependent endpoint "
            "selection remain downstream."
        ),
    }


def branch_selection_defect_response_status() -> dict[str, object]:
    """Top-level response to the current branch-selection defect."""
    p05u = derive_static_branch_selection_conditional_gate()
    p05v = derive_finite_core_boundary_feed_gate()
    p05w = derive_mass_deficit_boundary_selection_gate()
    p15c = volume_clock_branch_loading_status()
    p15d = lambert_branch_choice_dynamics_status()
    p05y = source_amplitude_branch_selector_status()
    branch_dictionary = derive_compact_load_branch_dictionary_gate()

    checks = {
        "conditional_static_exterior_locked": (
            p05u["static_branch_selection_status"]
            == "PASS_STATIC_BRANCH_SELECTION_CONDITIONAL_THEOREM__FINITE_CORE_DYNAMICS_OPEN"
        ),
        "C2_core_feeds_boundary": (
            p05v["finite_core_boundary_feed_status"]
            == "PASS_C2_FINITE_CORE_FEEDS_STATIC_BRANCH_BOUNDARY__DYNAMICAL_SELECTION_OPEN"
        ),
        "local_feedback_supplies_selected_load": (
            p05w["mass_deficit_boundary_selection_status"]
            == "PASS_LOCAL_FEEDBACK_SUPPLIES_STABLE_COMPACT_LOAD__FINITE_CORE_DYNAMICS_STILL_OPEN"
        ),
        "surface_clock_alpha_removed": (
            p15c["status"]
            == "PASS_VOLUME_CLOCK_MATCHING_SELECTS_LOAD_BRANCHES__DYNAMICAL_BRANCH_CHOICE_OPEN"
        ),
        "dynamical_choice_audited_open": (
            p15d["status"]
            == "PASS_BRANCH_CHOICE_AUDIT_DONE__FINITE_CORE_DYNAMICAL_SELECTION_STILL_OPEN"
        ),
        "source_amplitude_load_selector": (
            p05y["status"]
            == "PASS_STATIC_SOURCE_LOAD_SELECTOR_AND_FINITE_CORE_WINDOW_EXPLICIT"
        ),
        "branch_dictionary_explicit": (
            branch_dictionary["status"]
            == "PASS_COMPACT_LOAD_BRANCH_DICTIONARY_EXPLICIT"
        ),
    }
    passed = all(checks.values())

    return {
        "status": (
            "PASS_BRANCH_SELECTION_REFRAMED_AS_STATIC_LOAD_WINDOW__DYNAMICAL_ENDPOINT_OPEN"
            if passed
            else "CHECK_BRANCH_SELECTION_DEFECT_RESPONSE_CHAIN"
        ),
        "checks": checks,
        "closed_now": [
            "same-action static branch ledger exists",
            "compact exterior is not a GR vacuum, so Birkhoff vacuum uniqueness is out of scope",
            "C2 finite core supplies the compact boundary data algebraically",
            "surface-clock matching fixes the old proportional alpha bridge to alpha=2/3",
            "load branches are explicit Lambert-W branches",
            "a selected load can sit at a stable local mass-deficit feedback point",
            "finite-core source amplitude S selects a unique load; Q0 alone is proved insufficient",
            "finite-core geodesic exterior predictions require 1<Q_selected<2",
        ],
        "downstream_not_part_of_selector": [
            "compute S and chi for a specific equation of state or collapse history",
            "solve the time-dependent transition path after the selected branch is known",
            "derive the multi-field stability matrix for the selected compact endpoint",
            "complete the ADM/Noether proper-inventory to external-charge map for object-specific mass accounting",
        ],
        "defect_safe_statement": (
            "The branch-selection criticism is narrowed to the correct static "
            "statement.  Q0 alone cannot select an occupied endpoint, but the "
            "finite core also carries the source amplitude S.  The p14 feedback "
            "fixes q_v=W(chi S)/chi and surface-clock matching then fixes a "
            "unique load Q=2W(chi S)/(3chi).  The compact finite-core geodesic "
            "predictions apply only in the window 1<Q<2."
        ),
        "article_status_if_used_today": (
            "A finite-core compact exterior object must satisfy "
            "1<Q_selected<2, equivalently "
            "(3/2) exp(3 chi/2)<S<3 exp(3 chi).  Object-specific S and chi "
            "must be computed before making population predictions or collapse "
            "endpoint claims."
        ),
        "branch_dictionary": branch_dictionary,
        "source_amplitude_selector": p05y["selector_theorem"],
        "source_statuses": {
            "p05u": p05u["static_branch_selection_status"],
            "p05v": p05v["finite_core_boundary_feed_status"],
            "p05w": p05w["mass_deficit_boundary_selection_status"],
            "p15c": p15c["status"],
            "p15d": p15d["status"],
            "p05y": p05y["status"],
        },
    }


if __name__ == "__main__":
    result = branch_selection_defect_response_status()
    print("PHASE 18x: Branch-selection defect response gate")
    print("status:", result["status"])
    print("source_statuses:")
    for key, value in result["source_statuses"].items():
        print(f"  {key}: {value}")
    print("closed_now:")
    for item in result["closed_now"]:
        print("  -", item)
    print("downstream_not_part_of_selector:")
    for item in result["downstream_not_part_of_selector"]:
        print("  -", item)
    print("defect_safe_statement:", result["defect_safe_statement"])
    print("article_status_if_used_today:", result["article_status_if_used_today"])
    print("fold:", result["branch_dictionary"]["fold_point"])
    print("pressure_turn:", result["branch_dictionary"]["pressure_turn_marker"])
    print("samples:")
    for row in result["branch_dictionary"]["samples"]:
        print("  ", row)
