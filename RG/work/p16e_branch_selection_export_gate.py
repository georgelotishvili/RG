# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16e: Branch-selection export gate.

This is the only file allowed to decide whether compact markers may be exported
as branch-selected predictions.  The rule is strict: p16 through p16d must all
pass at the requested physical layer.

Because the physical ``S, chi`` map and EOS realization are still open, this
gate keeps the article language conditional.
"""

from __future__ import annotations

import sys
from typing import Any

from p16_source_coefficient_identification import (
    derive_source_coefficient_identification_gate,
)
from p16a_deficit_feedback_from_action import (
    derive_deficit_feedback_from_action_gate,
)
from p16b_dynamical_branch_attractor import derive_reduced_branch_attractor_gate
from p16c_eos_to_window_map import derive_eos_to_window_map_gate
from p16d_finite_core_interior_matching import (
    derive_finite_core_interior_matching_gate,
)
from p16f_compactness_band_source_map import (
    derive_stated_compactness_class_source_map,
)


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


def derive_branch_selection_export_gate() -> dict[str, Any]:
    p16 = derive_source_coefficient_identification_gate()
    p16a = derive_deficit_feedback_from_action_gate()
    p16b = derive_reduced_branch_attractor_gate()
    p16c = derive_eos_to_window_map_gate()
    p16d = derive_finite_core_interior_matching_gate()
    p16f = derive_stated_compactness_class_source_map()

    required_passes = {
        "p16_source_coefficient_identification": p16["STATUS"].startswith(
            _pass_status("SOURCE_COEFFICIENT_IDENTIFICATION")
        ),
        "p16a_action_derived_feedback": p16a["STATUS"].startswith(
            _pass_status("ACTION_DERIVED_FEEDBACK")
        ),
        "p16b_reduced_attractor": p16b["STATUS"].startswith(
            _pass_status("REDUCED_BRANCH_ATTRACTOR")
        ),
        "p16c_eos_to_window_map": p16c["STATUS"].startswith(
            _pass_status("EOS_TO_WINDOW_MAP")
        ),
        "p16d_finite_core_interior": p16d["STATUS"].startswith(
            _pass_status("FINITE_CORE_INTERIOR_MATCHING")
        ),
    }
    article_move_allowed = all(required_passes.values())
    stated_class_passes = {
        "p16f_compactness_source_map": p16f["STATUS"].startswith(
            _pass_status("STATED_COMPACTNESS_CLASS_SOURCE_MAP")
        ),
        "p16_source_has_stated_class_map": p16["STATED_CLASS_STATUS"].startswith(
            _pass_status("STATED_COMPACTNESS_CLASS_SOURCE_MAP")
        ),
        "p16a_reduced_action_feedback_for_class": p16a["STATED_CLASS_STATUS"].startswith(
            _pass_status("REDUCED_ACTION_FEEDBACK_FOR_STATED_VOLUME_CLASS")
        ),
        "p16b_reduced_attractor": required_passes["p16b_reduced_attractor"],
        "p16c_n1_polytrope_map": p16c["STATUS"].startswith(
            _pass_status("EOS_TO_WINDOW_MAP_FOR_N1_POLYTROPE_REALIZING_CLASS")
        ),
        "p16d_static_C2_interior_ledger": p16d["STATUS"].startswith(
            _pass_status("STATIC_C2_INTERIOR_LEDGER")
        ),
    }
    stated_class_article_move_allowed = all(stated_class_passes.values())

    return {
        "STATUS": (
            _pass_status("BRANCH_SELECTION_EXPORT_ALLOWED_FOR_STATED_COMPACT_CLASS")
            if article_move_allowed
            else "OPEN_EXPORT_GATE_KEEP_ARTICLE_CONDITIONAL"
        ),
        "SCOPE": (
            "Article-export decision gate.  It allows branch-selected compact "
            "predictions only if source coefficients, action feedback, reduced "
            "attractor, EOS window and finite-core interior all pass at the "
            "physical layer requested by the prompt."
        ),
        "ARTICLE_MOVE_ALLOWED": article_move_allowed,
        "STATED_CLASS_ARTICLE_MOVE_ALLOWED": stated_class_article_move_allowed,
        "required_passes": required_passes,
        "stated_class_passes": stated_class_passes,
        "input_statuses": {
            "p16": p16["STATUS"],
            "p16_STATED_CLASS": p16["STATED_CLASS_STATUS"],
            "p16a": p16a["STATUS"],
            "p16a_STATED_CLASS": p16a["STATED_CLASS_STATUS"],
            "p16b": p16b["STATUS"],
            "p16c": p16c["STATUS"],
            "p16d": p16d["STATUS"],
            "p16f": p16f["STATUS"],
        },
        "safe_article_language": (
            "General compact markers remain conditional.  A restricted "
            "stated-class statement is allowed for the volume-response "
            "principal-branch class with e^{-1/2}<C0<2/e, including the n=1 "
            "polytropic realizing band recorded in p16f."
        ),
        "stated_class_language": (
            "For the volume-response compact class chi=1 on the principal "
            "exterior-sheet branch, one physical input C0 selects "
            "Q=-2 W_0(-C0/2).  If e^{-1/2}<C0<2/e, then 1<Q<2 and the "
            "reduced source map S(C0)=q(C0) exp(q(C0)) has a stable fixed "
            "point.  For the n=1 polytrope p=K rho_c^2 this is realized when "
            "e^{-1/2}<4K rho_c/c^2<2/e."
        ),
        "blocked_upgrade": [
            "replace the stated-class S(C0) map by arbitrary-EOS action functions",
            "derive the feedback attenuation chi from the compact action coefficients",
            "upgrade the n=1 realizing class to relativistic TOV and observational EOS families",
            "upgrade the C2 interior from static ansatz ledger to solved physical endpoint",
        ],
        "do_not_claim": [
            "do not claim arbitrary compact markers are dynamically branch-selected",
            "do not claim arbitrary EOS compactness bands have been produced",
            "do not claim full nonlinear collapse has been solved",
            "do not remove global conditional wording from compact predictions",
        ],
    }


def _print_result(result: dict[str, Any]) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("ARTICLE_MOVE_ALLOWED:", result["ARTICLE_MOVE_ALLOWED"])
    print("STATED_CLASS_ARTICLE_MOVE_ALLOWED:", result["STATED_CLASS_ARTICLE_MOVE_ALLOWED"])
    print("required_passes:")
    for key, value in result["required_passes"].items():
        print(f"  - {key}: {value}")
    print("stated_class_passes:")
    for key, value in result["stated_class_passes"].items():
        print(f"  - {key}: {value}")
    print("input_statuses:")
    for key, value in result["input_statuses"].items():
        print(f"  - {key}: {value}")
    print("safe_article_language:", result["safe_article_language"])
    print("stated_class_language:", result["stated_class_language"])
    print("blocked_upgrade:")
    for item in result["blocked_upgrade"]:
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
    _print_result(derive_branch_selection_export_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
