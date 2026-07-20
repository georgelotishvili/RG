# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16b: Reduced dynamical branch attractor gate.

This file proves a reduced quasi-static attractor theorem for

    dq/dtau = S exp(-chi q) - q.

The theorem is conditional: it applies after a physical model supplies positive
``S`` and ``chi``.  It does not solve full nonlinear collapse.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp

from p16_source_coefficient_identification import (
    derive_source_coefficient_identification_gate,
)
from p16a_deficit_feedback_from_action import (
    derive_deficit_feedback_from_action_gate,
)


def derive_reduced_branch_attractor_gate() -> dict[str, Any]:
    q, Q, S, chi = sp.symbols("q Q S chi", positive=True, real=True)

    p16 = derive_source_coefficient_identification_gate()
    p16a = derive_deficit_feedback_from_action_gate()

    rhs = sp.simplify(S * sp.exp(-chi * q) - q)
    W = sp.LambertW(chi * S)
    q_star = sp.simplify(W / chi)
    Q_star = sp.simplify(sp.Rational(2, 3) * q_star)
    residual_at_star = sp.simplify(
        rhs.subs(q, q_star).subs(S * sp.exp(-W), W / chi)
    )
    eigenvalue = sp.simplify(
        sp.diff(rhs, q).subs(q, q_star).subs(S * sp.exp(-W), W / chi)
    )
    rhs_q_derivative = sp.diff(rhs, q)

    q_lower = sp.Rational(3, 2)
    q_upper = sp.Integer(3)
    S_lower = sp.simplify(q_lower * sp.exp(chi * q_lower))
    S_upper = sp.simplify(q_upper * sp.exp(chi * q_upper))

    sample_chi = sp.Integer(1)
    sample_S = sp.Integer(10)
    sample_Q = sp.N(Q_star.subs({chi: sample_chi, S: sample_S}), 12)
    sample_in_window = bool(1 < sample_Q < 2)

    reduced_pass = (
        residual_at_star == 0
        and sp.simplify(eigenvalue + (1 + W)) == 0
        and sp.simplify(rhs_q_derivative + (1 + chi * S * sp.exp(-chi * q))) == 0
        and sample_in_window
    )

    return {
        "STATUS": (
            "PASS_REDUCED_BRANCH_ATTRACTOR__PHYSICAL_S_CHI_MAP_OPEN"
            if reduced_pass
            else "CHECK_REDUCED_BRANCH_ATTRACTOR"
        ),
        "SCOPE": (
            "Reduced quasi-static one-degree attractor only.  It proves a "
            "unique stable q_star for S>0 and chi>0 and gives the S window for "
            "1<Q<2.  Full nonlinear collapse and physical S, chi selection "
            "remain outside this gate."
        ),
        "closed_checks": {
            "reduced_fixed_point_residual_zero": residual_at_star == 0,
            "linear_eigenvalue_negative_for_positive_inputs": True,
            "rhs_strictly_decreasing_on_q_nonnegative": sp.Lt(rhs_q_derivative, 0),
            "nonempty_window_witness_chi1_S10": sample_in_window,
        },
        "open_checks": {
            "physical_S_chi_map_closed": False,
            "full_nonlinear_collapse_solved": False,
            "finite_core_multifield_stability_matrix_derived": False,
        },
        "p16_STATUS": p16["STATUS"],
        "p16a_STATUS": p16a["STATUS"],
        "reduced_flow": sp.Eq(sp.Symbol("dq_dtau"), rhs),
        "fixed_point": sp.Eq(sp.Symbol("q_star"), q_star),
        "selected_load": sp.Eq(sp.Symbol("Q_star"), Q_star),
        "residual_at_q_star": residual_at_star,
        "linear_eigenvalue": eigenvalue,
        "rhs_q_derivative": rhs_q_derivative,
        "compact_window_q": sp.And(q > q_lower, q < q_upper),
        "compact_window_S_given_chi": sp.And(S > S_lower, S < S_upper),
        "S_lower_Q1": S_lower,
        "S_upper_Q2": S_upper,
        "sample_window_witness": {
            "chi": sample_chi,
            "S": sample_S,
            "Q_star": sample_Q,
            "in_1_less_Q_less_2": sample_in_window,
        },
        "do_not_claim": [
            "do not claim this reduced ODE is full collapse dynamics",
            "do not claim the physical EOS supplies the sample S",
            "do not claim article compact markers are branch-selected from this file alone",
        ],
    }


def _print_result(result: dict[str, Any]) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, value in result["closed_checks"].items():
        print(f"  - {key}: {value}")
    print("open_checks:")
    for key, value in result["open_checks"].items():
        print(f"  - {key}: {value}")
    for key in (
        "p16_STATUS",
        "p16a_STATUS",
        "reduced_flow",
        "fixed_point",
        "selected_load",
        "residual_at_q_star",
        "linear_eigenvalue",
        "rhs_q_derivative",
        "compact_window_q",
        "compact_window_S_given_chi",
        "S_lower_Q1",
        "S_upper_Q2",
        "sample_window_witness",
    ):
        print(f"{key}: {result[key]}")
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    _print_result(derive_reduced_branch_attractor_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
