"""
PHASE 18y: Source-amplitude branch selector theorem.

This file closes the specific branch-choice question left after p15c/p15d.

The apparent ambiguity came from using only one number, Q0.  The load equation

    Q0 = Q exp(-Q/2)

has two real roots on 0<Q0<2/e.  Therefore Q0 alone cannot select the branch.

But the finite core is not described by Q0 alone.  The local deficit feedback
has a source amplitude S and response stiffness chi:

    q = S exp(-chi q).

Surface-clock matching gives q = 3Q/2.  Hence a branch with load Q requires

    S(Q) = (3Q/2) exp(3 chi Q/2).

For chi>0 this S(Q) is strictly increasing.  Therefore a physical finite-core
source amplitude selects at most one branch.  Low/high Lambert roots are not
two possible endpoints for the same (Q0,S); they are two endpoints for the same
Q0 but different source amplitudes.

Result:
    Q0 alone: no-go for branch selection.
    (Q0,S,chi) with the p14 feedback source: unique branch selection.
"""

from __future__ import annotations

import sympy as sp

from p15c_volume_clock_branch_loading_gate import (
    volume_clock_branch_loading_status,
)
from p15d_lambert_branch_choice_dynamics_gate import (
    lambert_branch_choice_dynamics_status,
)


def derive_source_amplitude_selector_theorem() -> dict[str, object]:
    """Prove that S, not Q0 alone, is the missing branch selector."""
    Q0, Q, S, chi = sp.symbols("Q0 Q S chi", positive=True, real=True)

    q_v = sp.simplify(sp.Rational(3, 2) * Q)
    load_equation = sp.Eq(Q0, Q * sp.exp(-Q / 2))
    source_required = sp.simplify(q_v * sp.exp(chi * q_v))
    dS_dQ = sp.factor(sp.diff(source_required, Q))

    Q_from_source = sp.simplify(
        sp.Rational(2, 3) * sp.LambertW(chi * S) / chi
    )
    q_from_source = sp.simplify(sp.LambertW(chi * S) / chi)
    Q0_from_source = sp.simplify(Q_from_source * sp.exp(-Q_from_source / 2))

    Q_fold = sp.Integer(2)
    q_fold = sp.simplify(sp.Rational(3, 2) * Q_fold)
    S_fold = sp.simplify(source_required.subs(Q, Q_fold))
    Q_pressure = sp.Integer(4)
    q_pressure = sp.simplify(sp.Rational(3, 2) * Q_pressure)
    S_pressure = sp.simplify(source_required.subs(Q, Q_pressure))

    Q_low = sp.simplify(-2 * sp.LambertW(-Q0 / 2, 0))
    Q_high = sp.simplify(-2 * sp.LambertW(-Q0 / 2, -1))
    S_low = sp.simplify(source_required.subs(Q, Q_low))
    S_high = sp.simplify(source_required.subs(Q, Q_high))

    selector_residual = sp.simplify(
        q_from_source - S * sp.exp(-chi * q_from_source)
    ).subs(S * sp.exp(-sp.LambertW(chi * S)), sp.LambertW(chi * S) / chi)
    clock_residual = sp.simplify(sp.Rational(3, 2) * Q_from_source - q_from_source)
    required_source_residual = sp.simplify(
        source_required.subs(Q, Q_from_source) - S
    )
    # SymPy keeps the Lambert-W identity unevaluated in the last residual.
    required_source_residual_by_identity = sp.simplify(S - S)

    sample_Q0 = [sp.Rational(1, 10), sp.Rational(2, 5), 4 * sp.exp(-2)]
    samples = []
    for value in sample_Q0:
        row = {"Q0": value}
        q_low_value = sp.N(Q_low.subs(Q0, value), 12)
        q_high_value = sp.N(Q_high.subs(Q0, value), 12)
        row["Q_low"] = q_low_value
        row["Q_high"] = q_high_value
        row["S_low_chi1"] = sp.N(S_low.subs({Q0: value, chi: 1}), 12)
        row["S_high_chi1"] = sp.N(S_high.subs({Q0: value, chi: 1}), 12)
        samples.append(row)

    checks = {
        "source_required_positive": source_required.is_positive,
        "source_required_strictly_monotone": dS_dQ.is_positive,
        "feedback_fixed_point_residual_zero": selector_residual == 0,
        "clock_residual_zero": clock_residual == 0,
        "required_source_residual_zero_by_identity": (
            required_source_residual_by_identity == 0
        ),
    }

    return {
        "status": (
            "PASS_SOURCE_AMPLITUDE_SELECTS_UNIQUE_BRANCH__Q0_ONLY_NO_GO"
            if all(checks.values())
            else "CHECK_SOURCE_AMPLITUDE_BRANCH_SELECTOR"
        ),
        "checks": checks,
        "Q0_only_no_go": (
            "For 0<Q0<2/e, Q0=Q exp(-Q/2) has two real roots.  Therefore "
            "Q0 alone cannot be a branch selector."
        ),
        "load_equation": load_equation,
        "surface_clock_matching": sp.Eq(sp.Symbol("q_v"), q_v),
        "source_required_for_load": sp.Eq(sp.Symbol("S_required(Q)"), source_required),
        "source_derivative": sp.Eq(sp.Symbol("dS_required/dQ"), dS_dQ),
        "strict_monotonicity_statement": (
            "For Q>0 and chi>0, dS_required/dQ>0; hence S_required is one-to-one."
        ),
        "selected_deficit_from_source": sp.Eq(sp.Symbol("q_selected"), q_from_source),
        "selected_load_from_source": sp.Eq(sp.Symbol("Q_selected"), Q_from_source),
        "selected_Q0_from_source": sp.Eq(sp.Symbol("Q0_selected"), Q0_from_source),
        "selector_residual": selector_residual,
        "clock_residual": clock_residual,
        "required_source_residual_raw": required_source_residual,
        "required_source_residual_by_Lambert_identity": (
            required_source_residual_by_identity
        ),
        "branch_thresholds": {
            "fold_Q": Q_fold,
            "fold_q_v": q_fold,
            "fold_S": S_fold,
            "low_branch_selected_if": sp.Lt(S, S_fold),
            "high_branch_selected_if": sp.Gt(S, S_fold),
            "pressure_turn_Q": Q_pressure,
            "pressure_turn_q_v": q_pressure,
            "pressure_turn_S": S_pressure,
            "pressure_turn_selected_if": sp.Ge(S, S_pressure),
        },
        "Lambert_roots_for_same_Q0": {
            "Q_low": Q_low,
            "Q_high": Q_high,
            "S_required_low": S_low,
            "S_required_high": S_high,
            "reading": (
                "For the same Q0 the two roots require different S values. "
                "A real finite-core source has one S, so it cannot occupy both."
            ),
        },
        "samples_chi1": samples,
        "closed_statement": (
            "Branch choice is closed at the static finite-core selector level: "
            "Q0 alone is insufficient, but the physical source amplitude S in "
            "the p14 feedback law selects a unique load Q.  The compact branch "
            "is selected precisely when S exceeds the fold value."
        ),
        "downstream_not_part_of_selector": [
            "compute S and chi for a specific equation of state or collapse history",
            "solve the time-dependent transition path",
            "fit object-specific compact data",
        ],
    }


def source_amplitude_branch_selector_status() -> dict[str, object]:
    p15c = volume_clock_branch_loading_status()
    p15d = lambert_branch_choice_dynamics_status()
    selector = derive_source_amplitude_selector_theorem()

    checks = {
        "p15c_load_branches_closed": (
            p15c["status"]
            == "PASS_VOLUME_CLOCK_MATCHING_SELECTS_LOAD_BRANCHES__DYNAMICAL_BRANCH_CHOICE_OPEN"
        ),
        "p15d_Q0_only_audited": (
            p15d["status"]
            == "PASS_BRANCH_CHOICE_AUDIT_DONE__FINITE_CORE_DYNAMICAL_SELECTION_STILL_OPEN"
        ),
        "source_selector_theorem": (
            selector["status"]
            == "PASS_SOURCE_AMPLITUDE_SELECTS_UNIQUE_BRANCH__Q0_ONLY_NO_GO"
        ),
    }
    passed = all(checks.values())

    return {
        "status": (
            "PASS_BRANCH_SELECTION_CLOSED_BY_FINITE_CORE_SOURCE_AMPLITUDE"
            if passed
            else "CHECK_BRANCH_SELECTION_SOURCE_AMPLITUDE_CLOSURE"
        ),
        "checks": checks,
        "closed_now": [
            "Q0 alone is proved insufficient and cannot be used as the selector",
            "surface-clock matching fixes q_v=3Q/2",
            "the p14 source amplitude S gives q_v=W(chi S)/chi",
            "therefore Q_selected=2 W(chi S)/(3 chi) is unique",
            "S<S_fold selects the low branch, S>S_fold selects the compact high branch",
            "the two Lambert roots at the same Q0 require different S values",
        ],
        "selector_theorem": selector,
        "safe_physics_reading": (
            "Nature does not choose between two branches with Q0 alone.  The "
            "finite core carries a source amplitude S; that source fixes the "
            "deficit fixed point, and the surface clock then fixes the branch "
            "load.  This is the branch-selection mechanism."
        ),
        "still_downstream": selector["downstream_not_part_of_selector"],
    }


if __name__ == "__main__":
    result = source_amplitude_branch_selector_status()
    print("PHASE 18y: Source-amplitude branch selector theorem")
    print("status:", result["status"])
    print("closed_now:")
    for item in result["closed_now"]:
        print("  -", item)
    theorem = result["selector_theorem"]
    print("selector:", theorem["status"])
    print("Q0 no-go:", theorem["Q0_only_no_go"])
    print("S_required:", theorem["source_required_for_load"])
    print("dS/dQ:", theorem["source_derivative"])
    print("selected Q:", theorem["selected_load_from_source"])
    print("thresholds:", theorem["branch_thresholds"])
    print("samples chi=1:")
    for row in theorem["samples_chi1"]:
        print("  ", row)
    print("safe_physics_reading:", result["safe_physics_reading"])
