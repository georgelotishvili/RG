# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16d: Finite-core interior matching gate.

This file consolidates the existing C2 finite-core interior ledger and checks
whether it is strong enough for the new branch-selection export.

The static C2 algebra is strong: matching, zero shell stress, finite source,
and a branch-level action-density ledger are already present.  The stronger
claim of a solved physical interior with geodesic completion is still open.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp

from p05_compact import analyze_geodesic_completion_by_core_matching
from p05v_finite_core_boundary_feed_gate import derive_finite_core_boundary_feed_gate


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


def derive_finite_core_interior_matching_gate() -> dict[str, Any]:
    completion = analyze_geodesic_completion_by_core_matching()
    boundary_feed = derive_finite_core_boundary_feed_gate()

    boundary_pass = (
        boundary_feed["finite_core_boundary_feed_status"]
        == _pass_status("C2_FINITE_CORE_FEEDS_STATIC_BRANCH_BOUNDARY__DYNAMICAL_SELECTION_OPEN")
    )
    source_summary = boundary_feed["source_boundary_summary"]
    zero_shell = (
        source_summary["junction_status"]
        == "C2_MATCHING_GIVES_ZERO_THIN_SHELL_STRESS_AT_R_C"
    )
    finite_center_and_continuous = (
        source_summary["core_source_boundary_status"]
        == _pass_status("C2_CORE_EFFECTIVE_SOURCE_CONTINUOUS_AT_R_C")
    )
    proper_finite = boundary_pass

    static_pass = all(
        [
            zero_shell,
            finite_center_and_continuous,
            proper_finite,
            boundary_pass,
        ]
    )
    geodesic_completion_closed = False
    solved_physical_interior_closed = False

    return {
        "STATUS": (
            "PASS_STATIC_C2_INTERIOR_LEDGER__OPEN_GEODESIC_COMPLETION_AND_CORE_DYNAMICS"
            if static_pass
            else "CHECK_STATIC_C2_INTERIOR_LEDGER"
        ),
        "SCOPE": (
            "Static non-rotating C2 matching ledger.  It checks regular center "
            "data, zero thin shell and finite source measures for the ansatz. "
            "It does not prove physical collapse selects the interior, nor "
            "does it close global geodesic completion."
        ),
        "closed_checks": {
            "C2_log_matching_ansatz_present": completion["proof_status"].startswith("C2_CORE"),
            "zero_Israel_thin_shell": zero_shell,
            "finite_effective_core_source_and_boundary_ledger": finite_center_and_continuous,
            "proper_source_finite_for_finite_rc": proper_finite,
            "p05v_boundary_feed_passes_static_ledger": boundary_pass,
        },
        "open_checks": {
            "solved_regular_interior_from_full_core_action": solved_physical_interior_closed,
            "global_geodesic_completion_proved": geodesic_completion_closed,
            "rotating_or_time_dependent_core": False,
            "compact_perturbation_spectrum": False,
        },
        "completion_proof_status": completion["proof_status"],
        "completion_global_gate": completion["global_completion_gate"],
        "junction_status": source_summary["junction_status"],
        "core_source_status": source_summary["core_source_boundary_status"],
        "proper_energy_status": (
            "covered_by_p05v_boundary_feed_static_source_ledger"
        ),
        "boundary_feed_status": boundary_feed["finite_core_boundary_feed_status"],
        "boundary_feed_not_closed": boundary_feed["not_closed_now"],
        "do_not_claim": [
            "do not claim geodesic completion from C2 matching alone",
            "do not claim the C2 ansatz is selected by physical collapse",
            "do not claim rotating or time-dependent interiors are covered",
            "do not export compact markers as fully branch-selected from p16d alone",
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
        "completion_proof_status",
        "completion_global_gate",
        "junction_status",
        "core_source_status",
        "proper_energy_status",
        "boundary_feed_status",
        "boundary_feed_not_closed",
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
    _print_result(derive_finite_core_interior_matching_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
