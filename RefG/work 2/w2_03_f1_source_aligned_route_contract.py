"""W2-F1 კანდიდატების თვითკმარი სამეცნიერო მარშრუტის კონტრაქტი.

ეს ფაილი ფიზიკურ მექანიზმს არ ამტკიცებს. იგი მხოლოდ არჩევს დასაშვებ
input/output საზღვარს და კრძალავს სასურველი შედეგის პრიმიტივად შეტანას.
"""
from __future__ import annotations

import json
import sys
from typing import Any


MODEL_VERSION = "W2-F1-SOURCE-ALIGNED-ROUTE-CONTRACT-v1.8-internal"

SOURCE_CONSTRAINTS = {
    "one_ontological_foundation": True,
    "one_foundation_is_not_forced_to_be_singleton_state_space": True,
    "no_foundational_spacetime_location_or_clock": True,
    "stable_inequivalent_differentiation_must_be_output": True,
    "node_trace_relation_are_outputs_and_deferred_to_F2": True,
}

CANDIDATE_CLASSES: dict[str, dict[str, list[str]]] = {
    "symmetric_instability_or_bifurcation": {
        "imports_to_declare": [
            "configuration_space", "nontrivial_symmetry", "symmetric_branch",
            "invariant_rule",
        ],
        "must_derive": [
            "open_domain_instability", "stable_inequivalent_branch",
            "target_free_selection_or_seed_account",
        ],
    },
    "atemporal_nonunique_solution_structure": {
        "imports_to_declare": [
            "solution_space", "equivalence_rule", "self_consistency_law",
        ],
        "must_derive": [
            "inequivalent_stable_solutions",
            "noncircular_physical_selection_account",
        ],
    },
    "stochastic_or_quantum_outcome": {
        "imports_to_declare": [
            "state_space", "symmetric_probability_or_state", "outcome_rule",
        ],
        "must_derive": [
            "internal_not_external_outcomes", "stable_inequivalence",
            "no_preferred_outcome_injection",
        ],
    },
    "state_space_generating_rule": {
        "imports_to_declare": ["generative_grammar", "equivalence_rule"],
        "must_derive": [
            "nontrivial_generated_states", "stable_inequivalence",
            "termination_or_consistency",
        ],
    },
    "nontrivial_relational_state_space": {
        "imports_to_declare": [
            "relational_state_space", "relabel_equivalence", "law",
        ],
        "must_derive": [
            "stable_inequivalent_relational_sectors",
            "no_node_or_trace_preloading",
        ],
    },
    "other_explicit_target_free_mechanism": {
        "imports_to_declare": ["complete_primitive_and_rule_registry"],
        "must_derive": [
            "stable_target_free_inequivalent_differentiation",
            "noncircularity_and_health",
        ],
    },
}

FORBIDDEN_PREWIRED_INPUTS = {
    "physical_x_coordinate", "clock_time", "spacetime_point",
    "three_plus_one_geometry", "fixed_spatial_lattice",
    "preferred_locality_graph", "external_master_clock",
    "computational_step_as_physical_time", "Lorentzian_signature",
    "light_cone", "metric_g_munu", "pressure", "H", "Phi", "p",
    "Omega", "physical_phase", "oscillon", "mass", "particle",
    "Einstein_Hilbert_action", "Einstein_equation", "G_Newton", "M_Pl",
    "desired_GR_coefficients", "desired_1PN_coefficients",
    "desired_PPN_coefficients", "post_data_switch", "post_data_mode",
    "post_data_profile", "node", "persistent_trace",
    "operational_relation", "preferred_geometry", "observed_answer",
}

F1_REQUIRED_OUTPUT = "stable_target_free_inequivalent_differentiation"
DEFERRED_OUTPUTS = {
    "recurrence_or_phase_relation", "persistent_trace", "node",
    "operational_relation", "internal_causal_order", "additive_modes",
}
DOWNSTREAM_TARGETS_NOT_F1_PRIMITIVES = {
    "two_logical_limits_and_bounded_resonant_regime",
    "manifested_multichannel_environment",
}

SCIENTIFIC_CLAIM: dict[str, Any] = {
    "claim": (
        "ერთი ონტოლოგიური ფუძე არ უდრის აუცილებლობით ერთელემენტიან "
        "მდგომარეობათა სივრცეს. F1 კანდიდატმა გამოცხადებული კლასიდან, "
        "სამიზნის წინასწარ ჩადების გარეშე, უნდა მიიღოს მდგრადი "
        "არაეკვივალენტური დიფერენციაცია; კვანძი, კვალი და ურთიერთობა შემდგომ "
        "შედეგებად რჩება."
    ),
    "assumptions": [
        "ერთი ონტოლოგიური ფუძის მოთხოვნა მოქმედია.",
        "strict-singleton no-go მხოლოდ თავის პირობით დომენში მოქმედებს.",
        "დეტერმინისტული, ვარიაციული, სტოქასტიკური, კვანტური, გენერაციული და "
        "რელაციური escape-კლასები წინასწარ დახურული არაა.",
        "ამ მარშრუტის PASS არც ერთ კლასს ფიზიკურად არ ამტკიცებს.",
    ],
    "scope": (
        "F1 კანდიდატების კლასიფიკაცია და input/output საზღვარი; კონკრეტული "
        "state space, symmetry, law, სტაბილურობა და ფიზიკური რუკა ღიაა."
    ),
    "falsifier": (
        "კანდიდატურ input-ში სასურველი F1/F2 შედეგის, ეფექტური სივრცე-დროის "
        "ცვლადის ან დაურეგისტრირებელი თავისუფლების აღმოჩენა."
    ),
    "open_boundaries": [
        "კონკრეტული პრიმიტივები და ეკვივალენტობა",
        "არსებობა, სტაბილურობა და არაცირკულარული არჩევა",
        "ფიზიკური F1 promotion",
        "F2 კვანძი, კვალი და ოპერაციული ურთიერთობა",
    ],
}


def import_violations(imports: set[str]) -> set[str]:
    return imports & (
        FORBIDDEN_PREWIRED_INPUTS
        | DEFERRED_OUTPUTS
        | DOWNSTREAM_TARGETS_NOT_F1_PRIMITIVES
        | {F1_REQUIRED_OUTPUT}
    )


def candidate_registry_valid(
    registry: dict[str, dict[str, list[str]]]
) -> bool:
    return bool(registry) and all(
        set(spec) == {"imports_to_declare", "must_derive"}
        and all(
            isinstance(spec[key], list)
            and bool(spec[key])
            and len(spec[key]) == len(set(spec[key]))
            and all(isinstance(item, str) and item for item in spec[key])
            for key in spec
        )
        for spec in registry.values()
    )


def run_gate() -> dict[str, Any]:
    registry_valid = candidate_registry_valid(CANDIDATE_CLASSES)
    imports = {
        item
        for specification in CANDIDATE_CLASSES.values()
        for item in specification["imports_to_declare"]
    }
    violations = import_violations(imports)

    deliberately_bad_imports = {
        "configuration_space", "recurrence_or_phase_relation",
        "persistent_trace", "metric_g_munu",
        "manifested_multichannel_environment",
    }
    detected_bad_imports = import_violations(deliberately_bad_imports)
    negative_control = {
        "recurrence_or_phase_relation", "persistent_trace", "metric_g_munu",
        "manifested_multichannel_environment",
    }.issubset(detected_bad_imports)

    checks = {
        "source_constraints_explicit": all(SOURCE_CONSTRAINTS.values()),
        "all_candidate_classes_declare_imports_and_derivations": registry_valid,
        "candidate_imports_do_not_contain_F1_result": (
            F1_REQUIRED_OUTPUT not in imports
        ),
        "deferred_outputs_are_not_imported": not (DEFERRED_OUTPUTS & imports),
        "effective_spacetime_and_target_inputs_are_absent": not violations,
        "prewired_negative_control_is_rejected": negative_control,
        "physical_F1_remains_open": True,
    }
    passed = all(checks.values())
    return {
        "model_version": MODEL_VERSION,
        "status": (
            "ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_G1_AND_PHYSICAL_F1_OPEN"
            if passed
            else "ROUTE_SCHEMA_VALIDATION_FAIL"
        ),
        "claim": SCIENTIFIC_CLAIM,
        "source_constraints": SOURCE_CONSTRAINTS,
        "candidate_classes": CANDIDATE_CLASSES,
        "forbidden_prewired_inputs": sorted(FORBIDDEN_PREWIRED_INPUTS),
        "deferred_outputs": sorted(DEFERRED_OUTPUTS),
        "checks": checks,
        "violations": sorted(violations),
        "refg_W2_F1_closed": False,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"].startswith("ROUTE_SCHEMA_VALIDATED") else 1


if __name__ == "__main__":
    raise SystemExit(main())
