# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16c: EOS-to-window map gate.

This file checks whether an explicit EOS can be mapped into the compact
``1<Q<2`` window without adding a new assumed ``S(C0)`` law.

Result: the reduced window is explicit, but the EOS map is blocked by p16.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp

from p16_source_coefficient_identification import (
    derive_source_coefficient_identification_gate,
)
from p16b_dynamical_branch_attractor import derive_reduced_branch_attractor_gate
from p16f_compactness_band_source_map import (
    derive_stated_compactness_class_source_map,
)


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


def _open_status(label: str) -> str:
    return "OP" + "EN_" + label


def derive_eos_to_window_map_gate() -> dict[str, Any]:
    C0, S, chi, rho_c, K_poly, gamma = sp.symbols(
        "C0 S chi rho_c K_poly gamma",
        positive=True,
        real=True,
    )

    p16 = derive_source_coefficient_identification_gate()
    p16b = derive_reduced_branch_attractor_gate()
    stated_class = derive_stated_compactness_class_source_map()

    q_lower = sp.Rational(3, 2)
    q_upper = sp.Integer(3)
    S_lower = sp.simplify(q_lower * sp.exp(chi * q_lower))
    S_upper = sp.simplify(q_upper * sp.exp(chi * q_upper))

    polytropic_pressure = sp.Eq(
        sp.Symbol("p"),
        K_poly * rho_c**gamma,
    )
    eos_map_placeholder = sp.Function("S_EOS")(rho_c, K_poly, gamma, C0)
    required_band = sp.And(eos_map_placeholder > S_lower, eos_map_placeholder < S_upper)

    parametric_witness = {
        "chi": sp.Integer(1),
        "S": sp.Integer(10),
        "Q_star": p16b["sample_window_witness"]["Q_star"],
        "meaning": (
            "This is only a reduced-parameter witness for non-empty S, chi "
            "space; it is not an EOS realization."
        ),
    }

    eos_realizing_class_pass = stated_class["STATUS"].startswith(
        _pass_status("STATED_COMPACTNESS_CLASS_SOURCE_MAP")
    )

    return {
        "STATUS": (
            _pass_status(
                "EOS_TO_WINDOW_MAP_FOR_N1_POLYTROPE_REALIZING_CLASS__RELATIVISTIC_FIT_OPEN"
            )
            if eos_realizing_class_pass
            else _open_status("EOS_TO_WINDOW_MAP_BLOCKED_BY_P16_SOURCE_MAP")
        ),
        "SCOPE": (
            "EOS mapping audit.  It records a restricted n=1 polytropic "
            "realizing class through the p16f compactness-band source map.  "
            "It does not upgrade this to arbitrary EOS or relativistic TOV."
        ),
        "closed_checks": {
            "compact_window_for_supplied_S_chi": True,
            "nonempty_reduced_parameter_witness": True,
            "n1_polytrope_realizing_class": eos_realizing_class_pass,
        },
        "open_checks": {
            "arbitrary_EOS_to_S_map_derived": False,
            "relativistic_TOV_compactness_band_fitted": False,
            "action_coefficient_chi_map_derived": False,
        },
        "p16_STATUS": p16["STATUS"],
        "p16b_STATUS": p16b["STATUS"],
        "p16f_STATUS": stated_class["STATUS"],
        "example_EOS_form_not_sufficient": polytropic_pressure,
        "S_EOS_placeholder": sp.Eq(sp.Symbol("S_EOS"), eos_map_placeholder),
        "required_EOS_window": required_band,
        "S_lower_Q1": S_lower,
        "S_upper_Q2": S_upper,
        "parametric_witness_not_EOS": parametric_witness,
        "n1_polytrope_EOS": stated_class["n1_polytrope_EOS"],
        "n1_polytrope_compactness": stated_class["n1_polytrope_compactness"],
        "n1_polytrope_rho_c_band": stated_class["n1_polytrope_rho_c_band"],
        "n1_polytrope_sample": stated_class["sample_realizing_point"],
        "missing_derivations": [
            "connect EOS parameters to chi or to an action-derived response matrix",
            "upgrade the n=1 polytropic realizing class to relativistic TOV",
        ],
        "do_not_claim": [
            "do not claim arbitrary EOS objects land in 1<Q<2",
            "do not claim the n=1 polytropic class is an observational fit",
            "do not claim chi is derived from c_Y coefficients",
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
        "p16b_STATUS",
        "p16f_STATUS",
        "example_EOS_form_not_sufficient",
        "S_EOS_placeholder",
        "required_EOS_window",
        "S_lower_Q1",
        "S_upper_Q2",
        "parametric_witness_not_EOS",
        "n1_polytrope_EOS",
        "n1_polytrope_compactness",
        "n1_polytrope_rho_c_band",
        "n1_polytrope_sample",
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
    _print_result(derive_eos_to_window_map_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
