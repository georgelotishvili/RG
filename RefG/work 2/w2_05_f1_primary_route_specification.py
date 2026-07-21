"""ორი no-go საზღვრის შემდეგ მიღებული გადასინჯვადი F1 სამუშაო მარშრუტი.

ეს არის ისტორიული კვლევითი პრიორიტეტი და არა ფიზიკური ჭეშმარიტება. იგი
აფიქსირებს კანდიდატის ყველა ღია ვალდებულებას და აკრძალულ shortcut-ს.
"""
from __future__ import annotations

import json
import sys
from typing import Any


MODEL_VERSION = "W2-F1-PRIMARY-ROUTE-SPEC-v1.7-internal"
PRIMARY_ROUTE = "SYMMETRIC_BIFURCATION_WITH_TARGET_FREE_GENERIC_SEED"

ROUTE_OBLIGATIONS = {
    "single_carrier": "SOURCE_CONSTRAINT",
    "concrete_unlabelled_configuration_space": "OPEN",
    "nontrivial_exact_symmetry_G_sym": "OPEN",
    "G_sym_fixed_symmetric_branch_q0": "OPEN",
    "q0_no_nontrivial_distinguishable_internal_role_or_relational_structure_mod_equivalence": "OPEN",
    "symmetry_role_global_physical_vs_gauge_or_relabel": "OPEN",
    "target_free_G_sym_invariant_rule_or_functional": "OPEN",
    "open_parameter_domain_with_q0_instability": "OPEN",
    "stable_nonfixed_solution_orbit": "OPEN",
    "G_sym_invariant_seed_distribution": "OPEN",
    "individual_nonsymmetric_seed_realization": "OPEN",
    "open_or_nonzero_measure_successful_seed_basin": "OPEN",
    "internal_seed_sampling_or_outcome_mechanism": "OPEN",
    "seed_or_selection_origin": "OPEN",
    "physical_inequivalence_after_gauge_quotient": "OPEN",
    "no_preferred_direction_or_observed_target_in_inputs": "REQUIRED",
}

EXCLUDED_SHORTCUTS = {
    "exact_q0_plus_single_valued_equivariant_update": "fixed-set no-go",
    "strict_singleton_state_space": "singleton no-go",
    "prelabelled_recurrence_trace_or_node": "target leakage",
    "instability_without_seed_realization": "exact q0 never leaves by itself",
    "gauge_related_minima_called_physical_multiplicity": "equivalence error",
    "observed_geometry_or_GR_inserted_as_boundary_condition": "target leakage",
}

ALTERNATIVE_CLASSES_REMAIN_OPEN = {
    "atemporal_nonunique_solution_structure",
    "stochastic_or_quantum_outcome",
    "state_space_generating_rule",
    "nontrivial_relational_state_space",
    "other_explicit_target_free_mechanism",
}

KNOWN_TOY_LIMITS = {
    "imported_toy_architecture": (
        "R^2, O(2), quartic functional and broken-sign parameter domain are not derived"
    ),
    "tangent_zero_mode": (
        "a zero Hessian tangent is not yet a physical Goldstone mode"
    ),
    "variational_vs_temporal": (
        "q=0 instability is variational; temporal decay is not proved"
    ),
    "orbit_vs_realization": (
        "existence of a solution orbit is distinct from realization of one branch"
    ),
    "F2_boundary": (
        "absence of node/trace/relation leaves F2 open and is not by itself an F1 failure"
    ),
}

SCIENTIFIC_CLAIM: dict[str, Any] = {
    "claim": (
        "სამუშაო კანდიდატად აირჩევა ერთი მატარებლის სიმეტრიული ტოტის "
        "ბიფურკაცია, რომლის კანონი მიმართულებას წინასწარ არ შეიცავს. branch "
        "realization-ს უნდა ახლდეს G_sym-ინვარიანტული seed-განაწილება, "
        "არასიმეტრიული ინდივიდუალური realization და შინაგანი outcome მექანიზმი."
    ),
    "status": (
        "გადასინჯვადი ისტორიული კვლევითი არჩევანი; არც არსებობა და არც "
        "ფიზიკური W2_F1 დახურვა არ არის დამტკიცებული."
    ),
    "assumptions": [
        "strict-singleton no-go მხოლოდ თავის დომენში მოქმედებს.",
        "equivariant fixed-set no-go მხოლოდ ერთმნიშვნელოვანი ზუსტად სიმეტრიული განახლების დომენში მოქმედებს.",
        "Landau-ს მაგალითი მხოლოდ დადებითი სათამაშო კონტროლია.",
        "დაკვირვებებთან შეუსაბამობისას ან უკეთესი მექანიზმისას მარშრუტი გადაიხედება.",
    ],
    "scope": (
        "შემდგომი F1 კანდიდატის კვლევითი არქიტექტურა; კონკრეტული state space, "
        "სიმეტრიის ფიზიკური როლი, კანონი, seed-ის წარმოშობა და observable map ღიაა."
    ),
    "falsifier": (
        "კონკრეტული განხორციელება აუცილებლად არღვევს წყაროს საზღვრებს, "
        "target leakage-ის გარეშე ვერ ქმნის მდგრად არაეკვივალენტურ სექტორებს, "
        "ან სხვა კლასი იმავე ვალდებულებებს ნაკლები დაუდასტურებელი პრიმიტივით ხურავს."
    ),
    "open_boundaries": sorted(
        key for key, value in ROUTE_OBLIGATIONS.items() if value == "OPEN"
    ),
}


EXPECTED_OBLIGATION_KEYS = frozenset(ROUTE_OBLIGATIONS)
EXPECTED_SHORTCUT_KEYS = frozenset(EXCLUDED_SHORTCUTS)
FORBIDDEN_ROUTE_TOKENS = {
    "OBSERVED", "PREWIRED", "TARGET_VALUE", "GR_GEOMETRY", "PPN_VALUE",
}


def validate_route(
    route: str,
    obligations: dict[str, str],
    shortcuts: dict[str, str],
) -> list[str]:
    issues: list[str] = []
    if route != PRIMARY_ROUTE:
        issues.append("unregistered_primary_route")
    if any(token in route.upper() for token in FORBIDDEN_ROUTE_TOKENS):
        issues.append("target_leakage_in_route_name")
    if set(obligations) != EXPECTED_OBLIGATION_KEYS:
        issues.append("obligation_registry_mismatch")
    if any(
        value not in {"OPEN", "REQUIRED", "SOURCE_CONSTRAINT"}
        for value in obligations.values()
    ):
        issues.append("dishonest_obligation_status")
    if (
        obligations.get("single_carrier") != "SOURCE_CONSTRAINT"
        or obligations.get(
            "no_preferred_direction_or_observed_target_in_inputs"
        ) != "REQUIRED"
    ):
        issues.append("source_or_target_leakage_guard_missing")
    if set(shortcuts) != EXPECTED_SHORTCUT_KEYS or any(
        not isinstance(reason, str) or not reason for reason in shortcuts.values()
    ):
        issues.append("excluded_shortcut_registry_mismatch")
    return issues


def run_gate() -> dict[str, Any]:
    real_issues = validate_route(
        PRIMARY_ROUTE, ROUTE_OBLIGATIONS, EXCLUDED_SHORTCUTS
    )

    missing_obligation = dict(ROUTE_OBLIGATIONS)
    missing_obligation.pop("seed_or_selection_origin")
    bad_status = dict(ROUTE_OBLIGATIONS)
    bad_status["seed_or_selection_origin"] = "CLOSED_WITHOUT_PROOF"
    missing_guard = dict(ROUTE_OBLIGATIONS)
    missing_guard[
        "no_preferred_direction_or_observed_target_in_inputs"
    ] = "OPEN"

    negative_controls = {
        "prewired_route_rejected": (
            "target_leakage_in_route_name"
            in validate_route(
                "OBSERVED_GR_GEOMETRY_PREWIRED",
                ROUTE_OBLIGATIONS,
                EXCLUDED_SHORTCUTS,
            )
        ),
        "unregistered_neutral_route_rejected": (
            "unregistered_primary_route"
            in validate_route(
                "UNREGISTERED_NEUTRAL_ROUTE",
                ROUTE_OBLIGATIONS,
                EXCLUDED_SHORTCUTS,
            )
        ),
        "missing_obligation_rejected": (
            "obligation_registry_mismatch"
            in validate_route(
                PRIMARY_ROUTE, missing_obligation, EXCLUDED_SHORTCUTS
            )
        ),
        "dishonest_closure_rejected": (
            "dishonest_obligation_status"
            in validate_route(PRIMARY_ROUTE, bad_status, EXCLUDED_SHORTCUTS)
        ),
        "missing_target_leakage_guard_rejected": (
            "source_or_target_leakage_guard_missing"
            in validate_route(
                PRIMARY_ROUTE, missing_guard, EXCLUDED_SHORTCUTS
            )
        ),
        "empty_shortcut_registry_rejected": (
            "excluded_shortcut_registry_mismatch"
            in validate_route(PRIMARY_ROUTE, ROUTE_OBLIGATIONS, {})
        ),
    }

    checks = {
        "real_route_registry_has_no_issues": not real_issues,
        "all_unproved_physical_obligations_remain_open": all(
            value == "OPEN"
            for key, value in ROUTE_OBLIGATIONS.items()
            if key not in {
                "single_carrier",
                "no_preferred_direction_or_observed_target_in_inputs",
            }
        ),
        "alternative_candidate_classes_remain_open": bool(
            ALTERNATIVE_CLASSES_REMAIN_OPEN
        ),
        "known_toy_limits_are_explicit": all(KNOWN_TOY_LIMITS.values()),
        "negative_controls_pass": all(negative_controls.values()),
        "physical_W2_F1_remains_open": True,
    }
    passed = all(checks.values())
    return {
        "model_version": MODEL_VERSION,
        "status": (
            "PRIMARY_ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_MODEL_AND_W2_F1_OPEN"
            if passed
            else "PRIMARY_ROUTE_SCHEMA_VALIDATION_FAIL"
        ),
        "claim": SCIENTIFIC_CLAIM,
        "primary_route": PRIMARY_ROUTE,
        "route_obligations": ROUTE_OBLIGATIONS,
        "excluded_shortcuts": EXCLUDED_SHORTCUTS,
        "alternative_classes_remain_open": sorted(
            ALTERNATIVE_CLASSES_REMAIN_OPEN
        ),
        "known_toy_limits": KNOWN_TOY_LIMITS,
        "checks": checks,
        "negative_controls": negative_controls,
        "issues": real_issues,
        "refg_W2_F1_closed": False,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"].startswith("PRIMARY_ROUTE_SCHEMA_VALIDATED") else 1


if __name__ == "__main__":
    raise SystemExit(main())
