# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16i: consolidated branch-selection status after the chi derivation.

This gate does not introduce new physics.  It collects the p16..p16h chain
into one branch-selection ledger and records, after p16g/p16h fixed chi=1, the
exact remaining boundary.  It separates what is now gate-closeable from what is
research-grade (interior solution, action Noether/ADM map, rotating exterior,
QNM/echo, full nonlinear collapse).

State after the chi work:

  * chi is a metric-readout exponent, independent of the polynomial
    coefficients and of omega_Delta (p16g).
  * the external gravitating source is the bulk/volume ADM channel, so chi=1
    is selected, not assumed (p16h, via the p15g balanced ADM filter).
  * therefore the static selector q_v = S e^{-chi q_v} loses its free exponent:
    with chi=1 the realizing window 1<Q<2 is a parameter-free load band,
    equivalently r_s/2 < r_c < r_s, equivalently e^{-1/2} < C0 < 2/e for the
    deficit-input compactness C0 = Q e^{-Q/2}.

What is still NOT closed: the bare-to-input compactness map and the dynamical
endpoint that decides whether a physical collapse leaves r_c in (r_s/2, r_s).
The compact geodesic markers therefore stay conditional.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp

from p16_source_coefficient_identification import (
    derive_source_coefficient_identification_gate,
)
from p16b_dynamical_branch_attractor import derive_reduced_branch_attractor_gate
from p16g_deficit_feedback_exponent_derivation import (
    derive_deficit_feedback_exponent_gate,
)
from p16h_external_source_channel_from_adm_bridge import (
    derive_external_source_channel_gate,
)
from p16j_geodesic_completeness_regular_object import (
    derive_geodesic_completeness_gate,
)
from p16k_interior_effective_source_ledger import (
    derive_interior_effective_source_ledger,
)


def derive_branch_selection_consolidated_status() -> dict[str, Any]:
    Q = sp.symbols("Q", positive=True, real=True)

    p16 = derive_source_coefficient_identification_gate()
    p16b = derive_reduced_branch_attractor_gate()
    p16g = derive_deficit_feedback_exponent_gate()
    p16h = derive_external_source_channel_gate()
    p16j = derive_geodesic_completeness_gate()
    p16k = derive_interior_effective_source_ledger()
    geometry_closed = p16j["STATUS"].startswith(
        "PASS_GEODESICALLY_COMPLETE_REGULAR_HORIZONLESS_GEOMETRY"
    )
    interior_ledger_closed = p16k["STATUS"].startswith(
        "PASS_INTERIOR_EFFECTIVE_SOURCE_BOUNDED_JUNCTION_CONTINUOUS"
    )

    chi = sp.Integer(1)  # derived in p16g + p16h

    # Parameter-free window after chi=1: load band and compactness band.
    q_v = sp.Rational(3, 2) * Q
    S_required = sp.simplify(q_v * sp.exp(chi * q_v))         # (3Q/2) e^{3Q/2}
    C0_of_Q = sp.simplify(Q * sp.exp(-Q / 2))                 # input compactness
    window = {
        "load_band_Q": sp.And(Q > 1, Q < 2),
        "core_radius_band": "r_s/2 < r_c < r_s",
        "C0_at_Q1": sp.simplify(C0_of_Q.subs(Q, 1)),
        "C0_at_Q2": sp.simplify(C0_of_Q.subs(Q, 2)),
        "S_at_Q1": sp.simplify(S_required.subs(Q, 1)),
        "S_at_Q2": sp.simplify(S_required.subs(Q, 2)),
    }
    C0_lower = sp.exp(-sp.Rational(1, 2))
    C0_upper = 2 * sp.exp(-1)
    band_matches = (
        sp.simplify(window["C0_at_Q1"] - C0_lower) == 0
        and sp.simplify(window["C0_at_Q2"] - C0_upper) == 0
    )

    chi_derived = (
        p16g["STATUS"].startswith("PASS_CHI_IS_METRIC_READOUT_EXPONENT")
        and p16h["STATUS"].startswith(
            "PASS_EXTERNAL_GRAVITATING_SOURCE_IS_BULK_VOLUME_CHANNEL_CHI_ONE"
        )
        and sp.simplify(p16g["chi_by_channel"]["volume"].rhs - 1) == 0
        and sp.simplify(p16h["external_source_exponent"].rhs - 1) == 0
    )

    gate_closeable_open = [
        "bare-to-input compactness map: relate the physical r_s/R of a solved "
        "regular interior to the deficit-input C0 = Q e^{-Q/2} (extends p16d)",
        "relativistic-TOV realizing band: replace the n=1 Newtonian polytrope "
        "of p16c by a relativistic EOS and recompute the realizing compactness",
    ]
    closed_since_first_consolidation = [
        "geodesic completeness of the cored object (p16j): no horizon, regular "
        "center, bounded curvature, finite proper depth, finite-affine reach to "
        "an extendible center -- the markers are markers of a complete geometry",
        "interior effective-source ledger (p16k): bounded stresses, exact "
        "junction continuity with the exterior deficit signature -2*Delta_P, "
        "finite isotropic center",
    ]
    research_grade_open = [
        "action-level matter-inventory to ADM/Noether map (the p15g + p06 open "
        "item); chi=1 is fixed at the metric-readout/ADM level, not yet from a "
        "full action inventory theorem",
        "dynamical collapse endpoint that decides whether r_c lands in "
        "(r_s/2, r_s); p16b is a reduced quasi-static attractor, not collapse",
        "physical-EOS / medium-action derivation of the C2 core source "
        "(the p16k ledger is geometry-defined, not EOS-derived)",
        "rotating exterior, QNM/echo / light-ring stability, and ray-traced "
        "plasma/accretion modeling",
    ]

    return {
        "STATUS": (
            "PASS_CHI_FIXED_TO_ONE__PARAMETER_FREE_WINDOW__STATIC_GEOMETRY_"
            "COMPLETE_AND_INTERIOR_LEDGER_CLOSED__EOS_DYNAMICS_ROTATION_OPEN"
            if (chi_derived and band_matches and geometry_closed and interior_ledger_closed)
            else "CHECK_BRANCH_SELECTION_CONSOLIDATED_STATUS"
        ),
        "SCOPE": (
            "Consolidation only.  It records that chi=1 is now derived and the "
            "realizing window is parameter-free, and it classifies the residual "
            "into gate-closeable and research-grade items.  It exports nothing "
            "to the article and keeps the compact markers conditional."
        ),
        "chi_value_now_derived": chi,
        "chi_derived_checks": {
            "p16g_readout_exponent": p16g["STATUS"].startswith(
                "PASS_CHI_IS_METRIC_READOUT_EXPONENT"
            ),
            "p16h_bulk_volume_channel": p16h["STATUS"].startswith(
                "PASS_EXTERNAL_GRAVITATING_SOURCE_IS_BULK_VOLUME_CHANNEL_CHI_ONE"
            ),
            "p16g_volume_channel_chi_one": sp.simplify(
                p16g["chi_by_channel"]["volume"].rhs - 1
            )
            == 0,
            "p16h_source_exponent_one": sp.simplify(
                p16h["external_source_exponent"].rhs - 1
            )
            == 0,
        },
        "parameter_free_window": window,
        "input_compactness_band": sp.And(sp.Gt(sp.Symbol("C0"), C0_lower), sp.Lt(sp.Symbol("C0"), C0_upper)),
        "input_compactness_band_numeric": (sp.N(C0_lower, 6), sp.N(C0_upper, 6)),
        "required_source_band_numeric": (sp.N(window["S_at_Q1"], 6), sp.N(window["S_at_Q2"], 6)),
        "band_matches_p16f": band_matches,
        "what_chi_work_changed": (
            "Before p16g/p16h the window depended on a free exponent chi (p16f "
            "assumed chi=1).  Now chi=1 is derived, so the window is a "
            "parameter-free load/compactness band, not a chi-conditional one."
        ),
        "still_conditional_because": [
            "C0 is the deficit-input compactness, not the bare r_s/R; the map "
            "needs a solved regular interior",
            "no dynamics shows a physical collapse leaves r_c in (r_s/2, r_s)",
            "rotating, QNM/echo and ray-tracing layers are untouched",
        ],
        "closed_since_first_consolidation": closed_since_first_consolidation,
        "gate_closeable_open": gate_closeable_open,
        "research_grade_open": research_grade_open,
        "p16_source_status": p16["STATUS"],
        "p16b_attractor_status": p16b["STATUS"],
        "p16g_status": p16g["STATUS"],
        "p16h_status": p16h["STATUS"],
        "p16j_status": p16j["STATUS"],
        "p16k_status": p16k["STATUS"],
        "article_export": "KEEP_COMPACT_MARKERS_CONDITIONAL__NO_ARTICLE_CHANGE",
        "do_not_claim": [
            "do not claim the compact markers are now branch-selected predictions",
            "do not claim a physical object is proven to land in the window",
            "do not claim the action inventory-to-ADM map is derived",
            "do not remove global conditional wording from compact predictions",
        ],
    }


def _print_result(result: dict[str, Any]) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("chi_value_now_derived:", result["chi_value_now_derived"])
    print("chi_derived_checks:")
    for key, value in result["chi_derived_checks"].items():
        print(f"  - {key}: {value}")
    print("parameter_free_window:")
    for key, value in result["parameter_free_window"].items():
        print(f"  - {key}: {value}")
    print("input_compactness_band_numeric:", result["input_compactness_band_numeric"])
    print("required_source_band_numeric:", result["required_source_band_numeric"])
    print("band_matches_p16f:", result["band_matches_p16f"])
    print("what_chi_work_changed:", result["what_chi_work_changed"])
    print("still_conditional_because:")
    for item in result["still_conditional_because"]:
        print("  -", item)
    print("closed_since_first_consolidation:")
    for item in result["closed_since_first_consolidation"]:
        print("  -", item)
    print("gate_closeable_open:")
    for item in result["gate_closeable_open"]:
        print("  -", item)
    print("research_grade_open:")
    for item in result["research_grade_open"]:
        print("  -", item)
    print("input_statuses:")
    for key in (
        "p16_source_status",
        "p16b_attractor_status",
        "p16g_status",
        "p16h_status",
        "p16j_status",
        "p16k_status",
    ):
        print(f"  - {key}: {result[key]}")
    print("article_export:", result["article_export"])
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    _print_result(derive_branch_selection_consolidated_status())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
