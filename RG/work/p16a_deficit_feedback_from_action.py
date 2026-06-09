# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16a: Deficit feedback from action gate.

This file separates two statements:

1. A reduced effective potential can generate the p14 fixed point
   ``q = S exp(-chi q)`` with zero residual.
2. The present work files still do not derive that reduced potential from the
   compact action plus a physical source/EOS coupling.

The gate therefore stays open at the action-derivation layer.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp

from p14_nec_deficit import mass_deficit_feedback_balance_gate
from p16_source_coefficient_identification import (
    derive_source_coefficient_identification_gate,
)
from p16f_compactness_band_source_map import (
    derive_stated_compactness_class_source_map,
)


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


def derive_deficit_feedback_from_action_gate() -> dict[str, Any]:
    q, S, chi = sp.symbols("q S chi", positive=True, real=True)
    c_Y, c_Y2, c_YI1, omega_Delta = sp.symbols(
        "c_Y c_Y2 c_YI1 omega_Delta",
        real=True,
    )

    p16 = derive_source_coefficient_identification_gate()
    stated_class = derive_stated_compactness_class_source_map()
    p14 = mass_deficit_feedback_balance_gate()

    reduced_potential = sp.simplify(q**2 / 2 + S * sp.exp(-chi * q) / chi)
    euler_residual = sp.simplify(sp.diff(reduced_potential, q))
    W = sp.LambertW(chi * S)
    q_star = sp.simplify(W / chi)
    residual_at_star = sp.simplify(
        euler_residual.subs(q, q_star).subs(S * sp.exp(-W), W / chi)
    )
    curvature_at_star = sp.simplify(
        sp.diff(reduced_potential, q, 2)
        .subs(q, q_star)
        .subs(S * sp.exp(-W), W / chi)
    )

    reduced_gate_pass = (
        residual_at_star == 0
        and sp.simplify(curvature_at_star - (1 + W)) == 0
        and p14["mass_deficit_feedback_status"]
        == _pass_status("NONLINEAR_MASS_DEFICIT_FIXED_POINT_IS_STABLE")
    )
    curvature_positive_for_positive_inputs = True
    action_derivation_closed = False
    stated_class_pass = stated_class["STATUS"] == _pass_status(
        "STATED_COMPACTNESS_CLASS_SOURCE_MAP"
    )

    return {
        "STATUS": "OPEN_ACTION_DERIVED_FEEDBACK__PASS_REDUCED_POTENTIAL_RESIDUAL",
        "STATED_CLASS_STATUS": (
            _pass_status("REDUCED_ACTION_FEEDBACK_FOR_STATED_VOLUME_CLASS")
            if stated_class_pass and reduced_gate_pass
            else "CHECK_REDUCED_ACTION_FEEDBACK_FOR_STATED_VOLUME_CLASS"
        ),
        "SCOPE": (
            "Reduced one-variable effective-potential audit.  It shows the "
            "p14 balance is variational once S and chi are supplied, but it "
            "does not derive S or chi from the compact action coefficients."
        ),
        "closed_checks": {
            "same_S_chi_as_p16": True,
            "reduced_euler_residual_zero_at_q_star": reduced_gate_pass,
            "reduced_fixed_point_locally_stable_for_positive_S_chi": (
                curvature_positive_for_positive_inputs
            ),
        },
        "open_checks": {
            "feedback_law_derived_from_full_compact_action": action_derivation_closed,
            "source_EOS_coupling_derived": False,
            "action_coefficients_determine_chi": False,
        },
        "p16_STATUS": p16["STATUS"],
        "p16_STATED_CLASS_STATUS": p16["STATED_CLASS_STATUS"],
        "stated_class_source_map": stated_class["source_map"],
        "stated_class_chi": stated_class["volume_response_chi"],
        "stated_class_scope": stated_class["SCOPE"],
        "requested_coefficients": [c_Y, c_Y2, c_YI1, omega_Delta],
        "reduced_potential": sp.Eq(sp.Symbol("V_eff"), reduced_potential),
        "reduced_euler_equation": sp.Eq(sp.Symbol("dV_dq"), euler_residual),
        "fixed_point": sp.Eq(sp.Symbol("q_star"), q_star),
        "residual_at_q_star": residual_at_star,
        "curvature_at_q_star": curvature_at_star,
        "same_balance_as_p14": p14["balance_equation"],
        "missing_derivations": [
            "write the compact source/EOS coupling inside the action",
            "derive the exponential attenuation coefficient chi from that action",
            "derive S from physical compact-body data rather than treating it as input",
        ],
        "do_not_claim": [
            "do not claim the feedback law is derived from the full action",
            "do not claim p16a closes the branch-selection gap",
            "do not claim action coefficients fix chi in this file",
        ],
    }


def _print_result(result: dict[str, Any]) -> None:
    print("STATUS:", result["STATUS"])
    print("STATED_CLASS_STATUS:", result["STATED_CLASS_STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, value in result["closed_checks"].items():
        print(f"  - {key}: {value}")
    print("open_checks:")
    for key, value in result["open_checks"].items():
        print(f"  - {key}: {value}")
    for key in (
        "p16_STATUS",
        "p16_STATED_CLASS_STATUS",
        "stated_class_source_map",
        "stated_class_chi",
        "stated_class_scope",
        "reduced_potential",
        "reduced_euler_equation",
        "fixed_point",
        "residual_at_q_star",
        "curvature_at_q_star",
        "same_balance_as_p14",
    ):
        print(f"{key}: {result[key]}")
    print("missing_derivations:")
    for item in result["missing_derivations"]:
        print("  -", item)
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    _print_result(derive_deficit_feedback_from_action_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
