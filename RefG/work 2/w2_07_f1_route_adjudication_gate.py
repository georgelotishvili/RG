"""Scientific route adjudication for the W2-F1 candidate.

This file records why the atemporal spectral route became the next route to
test.  It is a development-priority decision, not a theorem of physical truth.
The generic-seed route and every other nonfalsified route remain open.
"""
from __future__ import annotations

import json
import importlib.util
import sys
from pathlib import Path
from typing import Any


MODEL_VERSION = "W2-F1-ROUTE-ADJUDICATION-v2.6-scientific"
PRIOR_ROUTE = "SYMMETRIC_BIFURCATION_WITH_TARGET_FREE_GENERIC_SEED"
SELECTED_ROUTE = "ATEMPORAL_SPECTRAL_SPLIT_WITH_UNIQUE_QUOTIENT_MINIMUM"
NO_EXCLUSIVE_PRIMARY = "NO_EXCLUSIVE_PRIMARY"

MANDATORY_VETOES = (
    "source boundary is admissible",
    "inputs are target-free",
    "route-specific mathematical certificate is valid",
    "route status and imported choices are stated honestly",
    "physical F1 remains open before promotion",
    "nonfalsified alternatives are preserved",
)

COMMON_OBLIGATIONS = (
    "concrete unlabelled state space and equivalence",
    "exact nontrivial solution or outcome classification",
    "stability certificate within the declared scope",
    "inequivalence certificate after the full declared equivalence",
    "complete target-free realization or selection origin",
)

ATEMPORAL_OBLIGATION_MAP = {
    "single_carrier": "retained",
    "concrete_unlabelled_configuration_space": "closed conditionally by w2_06",
    "nontrivial_exact_symmetry": "closed conditionally by w2_06",
    "undifferentiated_reference": "Q=0 has no nontrivial generated projector",
    "target_free_invariant_rule": "closed conditionally by w2_06",
    "stable_nonfixed_solution_orbit": "closed conditionally by w2_06",
    "seed_distribution_and_basin": "not applicable to an atemporal unique-quotient rule",
    "selection_origin": "open: global argmin is an imported primitive",
    "physical_inequivalence": "conditional rank-role certificate; meaning remains open",
}

PROMOTION_OBLIGATIONS = (
    "freeze a route-neutral meaning of F1",
    "classify the unique-quotient role route explicitly",
    "justify Sym_0(3,R) as a foundation candidate rather than a toy representation",
    "state that the global-argmin law is imported and test it for circularity",
    "retain N=3, O(3), delta, and Q-sign choice as explicit imports",
    "distinguish variational structural stability from temporal persistence",
    "decide whether rank-role inequivalence is sufficient for programme F1",
)

TRADEOFFS = {
    "seed route": "less imported structure, but no concrete passing realization yet",
    "atemporal route": "exact candidate, but imports N=3, O(3), matrix algebra, V, and argmin",
    "quotient scope": "one quotient minimum with unequal roles, not multiple objects or vacua",
    "empirical scope": "neither route has an F1 observable or data comparison",
}

REVERSAL_TRIGGERS = (
    "a mathematical falsifier of the spectral candidate",
    "rejection of rank roles by the route-neutral F1 contract",
    "circular or target-loaded imported algebra or argmin law",
    "a competing route closes the same meaning with stronger health",
    "downstream inconsistency or observational falsification",
)


def load_sibling(filename: str, module_name: str) -> Any:
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def adjudicate(
    left_name: str,
    left: dict[str, bool],
    right_name: str,
    right: dict[str, bool],
) -> dict[str, Any]:
    """Veto-first, nonnumeric comparison on the same obligation keys."""
    expected = set(COMMON_OBLIGATIONS)
    left_valid = set(left) == expected and all(type(v) is bool for v in left.values())
    right_valid = set(right) == expected and all(type(v) is bool for v in right.values())
    left_closed = {key for key, value in left.items() if value is True}
    right_closed = {key for key, value in right.items() if value is True}

    winner = NO_EXCLUSIVE_PRIMARY
    relation = "INELIGIBLE_OR_INCOMPARABLE"
    if left_valid and right_valid:
        if left_closed > right_closed:
            winner, relation = left_name, "LEFT_STRICTLY_CONTAINS_RIGHT"
        elif right_closed > left_closed:
            winner, relation = right_name, "RIGHT_STRICTLY_CONTAINS_LEFT"
        elif left_closed == right_closed:
            relation = "EQUAL_COMMON_PROFILES"
        else:
            relation = "INCOMPARABLE_COMMON_PROFILES"
    return {
        "exclusive_primary": winner,
        "partial_order_relation": relation,
        "left_closed": sorted(left_closed),
        "right_closed": sorted(right_closed),
    }


def run_gate() -> dict[str, Any]:
    route_module = load_sibling(
        "w2_05_f1_primary_route_specification.py", "w2_05_live_scientific"
    )
    candidate_module = load_sibling(
        "w2_06_f1_atemporal_spectral_split_candidate_gate.py", "w2_06_live_scientific"
    )
    route_report = route_module.run_gate()
    candidate_report = candidate_module.run_gate()
    route_checks = route_report.get("checks", {})
    candidate_checks = candidate_report.get("CHECKS", {})
    route_obligations = route_report.get("route_obligations", {})

    route_live_valid = all((
        route_report.get("status")
        == "PRIMARY_ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_MODEL_AND_W2_F1_OPEN",
        bool(route_checks),
        all(value is True for value in route_checks.values()),
        route_report.get("refg_W2_F1_closed") is False,
    ))
    candidate_live_valid = all((
        candidate_report.get("STATUS")
        == "EXACT_ATEMPORAL_SPECTRAL_CANDIDATE_PASS__PHYSICAL_F1_OPEN",
        bool(candidate_checks),
        all(value is True for value in candidate_checks.values()),
        candidate_report.get("CLOSURE_FLAGS", {}).get("W2_F1_SELF_DIFFERENTIATION")
        is False,
    ))
    alternatives_preserved = all(
        route in set(route_report.get("alternative_classes_remain_open", ()))
        for route in (
            "atemporal_nonunique_solution_structure",
            "nontrivial_relational_state_space",
            "other_explicit_target_free_mechanism",
            "state_space_generating_rule",
            "stochastic_or_quantum_outcome",
        )
    )

    seed_evidence = {
        COMMON_OBLIGATIONS[0]: (
            route_obligations.get("concrete_unlabelled_configuration_space") != "OPEN"
        ),
        COMMON_OBLIGATIONS[1]: False,
        COMMON_OBLIGATIONS[2]: False,
        COMMON_OBLIGATIONS[3]: (
            route_obligations.get("physical_inequivalence_after_gauge_quotient") != "OPEN"
        ),
        COMMON_OBLIGATIONS[4]: False,
    }
    spectral_evidence = {
        COMMON_OBLIGATIONS[0]: all((
            candidate_live_valid,
            "one internal carrier Q in Sym_0(3,R)"
            in candidate_report.get("ASSUMPTIONS", ()),
            candidate_checks.get("O3_invariance_and_faithful_quotient") is True,
        )),
        COMMON_OBLIGATIONS[1]: all((
            candidate_checks.get("sharp_bound_and_unique_global_orbit") is True,
            candidate_checks.get("stationary_branches_exhaustive_and_energy_ordered") is True,
        )),
        COMMON_OBLIGATIONS[2]: (
            candidate_checks.get("orbit_normal_hessian_positive") is True
        ),
        COMMON_OBLIGATIONS[3]: all((
            candidate_checks.get("state_generated_rank_1_rank_2_projectors") is True,
            candidate_checks.get("O3_invariance_and_faithful_quotient") is True,
        )),
        # The mathematical argmin is explicit, but its deeper origin remains imported.
        COMMON_OBLIGATIONS[4]: False,
    }
    decision = adjudicate(PRIOR_ROUTE, seed_evidence, SELECTED_ROUTE, spectral_evidence)
    live_evidence_valid = route_live_valid and candidate_live_valid and alternatives_preserved
    exact_priority = live_evidence_valid and decision["exclusive_primary"] == SELECTED_ROUTE
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": (
            "ATEMPORAL_ROUTE_PRIMARY_FOR_NEXT_F1_AUDIT__PHYSICAL_F1_OPEN"
            if exact_priority else "NO_EXCLUSIVE_PRIMARY__PHYSICAL_F1_OPEN"
        ),
        "DECISION": decision,
        "LIVE_EVIDENCE": {
            "seed_route": seed_evidence,
            "spectral_route": spectral_evidence,
            "route_report_valid": route_live_valid,
            "candidate_report_valid": candidate_live_valid,
            "alternatives_preserved": alternatives_preserved,
        },
        "MANDATORY_VETOES": list(MANDATORY_VETOES),
        "ATEMPORAL_OBLIGATION_MAP": ATEMPORAL_OBLIGATION_MAP,
        "PROMOTION_OBLIGATIONS": list(PROMOTION_OBLIGATIONS),
        "TRADEOFFS_NOT_SCORED": TRADEOFFS,
        "REVERSAL_TRIGGERS": list(REVERSAL_TRIGGERS),
        "BRANCHES": {
            SELECTED_ROUTE: "primary only for the next F1 audit",
            PRIOR_ROUTE: "open fallback; not rejected",
            "all_other_nonfalsified_routes": "open",
            "programme_W2_F1": "open",
        },
        "SCOPE_CEILING": (
            "route priority only; no physical dominance, F1 closure, geometry, or observation"
        ),
        "CLOSURE_FLAGS": {
            "ROUTE_ADJUDICATION_VALIDATED": exact_priority,
            "ATEMPORAL_PRIMARY_FOR_NEXT_F1_AUDIT": exact_priority,
            "SEED_ROUTE_FALLBACK_OPEN": True,
            "PHYSICAL_ROUTE_DOMINANCE": False,
            "SEED_ROUTE_REJECTED": False,
            "W2_F1_SELF_DIFFERENTIATION": False,
        },
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
