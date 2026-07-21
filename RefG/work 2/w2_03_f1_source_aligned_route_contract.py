"""RefG W2-F1 route contract: source constraints and admissible candidate classes.

This is a mechanical architecture router, not a physical candidate and not an
emergence proof. It prevents one ontology from being confused with a singleton
state space and prevents desired F1/F2 outputs from being inserted as inputs.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


MODEL_VERSION = "W2-F1-SOURCE-ALIGNED-ROUTE-CONTRACT-v1.8-internal"
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"
UNIVERSAL_GATES = frozenset({
    "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
    "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
    "G7_OBSERVATION", "G8_EXPORT",
})
REQUIRED_SOURCE_CONSTRAINT_KEYS = frozenset({
    "one_ontological_foundation",
    "one_foundation_is_not_forced_to_be_singleton_state_space",
    "no_foundational_spacetime_location_or_clock",
    "stable_inequivalent_differentiation_must_be_output",
    "node_trace_relation_are_outputs_and_analytically_deferred_to_F2",
})

REQUIRED_FIELDS = {
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "GATE_APPLICABILITY", "CROSSCHECK", "PROVENANCE", "FILES",
}

SOURCE_CONSTRAINTS = {
    "one_ontological_foundation": True,
    "one_foundation_is_not_forced_to_be_singleton_state_space": True,
    "no_foundational_spacetime_location_or_clock": True,
    "stable_inequivalent_differentiation_must_be_output": True,
    "node_trace_relation_are_outputs_and_analytically_deferred_to_F2": True,
}

# These are slots a concrete candidate must fill and justify. They are not
# consequences of the Canon and are deliberately not marked as derived.
CANDIDATE_CLASSES = {
    "symmetric_instability_or_bifurcation": {
        "imports_to_declare": ["configuration_space", "nontrivial_symmetry", "symmetric_branch", "invariant_rule"],
        "must_derive": ["open_domain_instability", "stable_inequivalent_branch", "target_free_selection_or_seed_account"],
    },
    "atemporal_nonunique_solution_structure": {
        "imports_to_declare": ["solution_space", "equivalence_rule", "self_consistency_law"],
        "must_derive": ["inequivalent_stable_solutions", "noncircular_physical_selection_account"],
    },
    "stochastic_or_quantum_outcome": {
        "imports_to_declare": ["state_space", "symmetric_probability_or_state", "outcome_rule"],
        "must_derive": ["internal_not_external_outcomes", "stable_inequivalence", "no_preferred_outcome_injection"],
    },
    "state_space_generating_rule": {
        "imports_to_declare": ["generative_grammar", "equivalence_rule"],
        "must_derive": ["nontrivial_generated_states", "stable_inequivalence", "termination_or_consistency"],
    },
    "nontrivial_relational_state_space": {
        "imports_to_declare": ["relational_state_space", "relabel_equivalence", "law"],
        "must_derive": ["stable_inequivalent_relational_sectors", "no_node_or_trace_preloading"],
    },
    "other_explicit_target_free_mechanism": {
        "imports_to_declare": ["complete_primitive_and_rule_registry"],
        "must_derive": ["stable_target_free_inequivalent_differentiation", "noncircularity_and_health"],
    },
}

FORBIDDEN_PREWIRED_INPUTS = {
    "physical_x_coordinate", "clock_time", "spacetime_point", "three_plus_one_geometry",
    "fixed_spatial_lattice", "preferred_locality_graph", "external_master_clock",
    "computational_step_as_physical_time", "Lorentzian_signature", "light_cone",
    "metric_g_munu", "pressure", "H", "Phi", "p", "Omega", "physical_phase",
    "oscillon", "mass", "particle", "Einstein_Hilbert_action", "Einstein_equation",
    "G_Newton", "M_Pl", "desired_GR_coefficients", "desired_1PN_coefficients",
    "desired_PPN_coefficients", "post_data_switch", "post_data_mode",
    "post_data_profile", "node", "persistent_trace", "operational_relation",
    "preferred_geometry", "observed_answer",
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

INITIAL_CLOSURE_FLAGS = {
    "G0_GOAL": False,
    "G1_CONVENTIONS": False,
    "G2_CORE_ALGEBRA": False,
    "G3_STRUCTURE": False,
    "G4_INDEPENDENT_CHECK": False,
    "G5_LIMITS_REGRESSION": False,
    "G6_PHYSICAL_MATCH": False,
    "G7_OBSERVATION": False,
    "G8_EXPORT": False,
    "W2_F1_SELF_DIFFERENTIATION": False,
    "W2_F2_OPERATIONAL_RELATIONS": False,
    "W2_F3_INTERNAL_ORDER_CAUSALITY": False,
    "W2_F4_INDEPENDENT_ADDITIVE_MODES": False,
}

GATE_APPLICABILITY = {
    "G0_GOAL": "REQUIRED — route schema, scope, classes, inputs and outputs are checked",
    "G1_CONVENTIONS": "OPEN — only a concrete candidate can freeze its variables, symmetry and equivalence",
    "G2_CORE_ALGEBRA": "N/A — this router contains no physical algebra",
    "G3_STRUCTURE": "OPEN — existence/stability belongs to a concrete candidate",
    "G4_INDEPENDENT_CHECK": "OPEN — semantic source audit is separate from mechanical checks",
    "G5_LIMITS_REGRESSION": "N/A — no physical solution or approximation",
    "G6_PHYSICAL_MATCH": "N/A — no source, charge, energy or observable map",
    "G7_OBSERVATION": "N/A — no data or prediction",
    "G8_EXPORT": "N/A — internal Git-ignored route schema; no export authorized",
}
EXPECTED_CLOSURE_KEYS = frozenset(INITIAL_CLOSURE_FLAGS)
EXPECTED_GATE_APPLICABILITY = dict(GATE_APPLICABILITY)
EXPECTED_CANDIDATE_CLASS_NAMES = frozenset(CANDIDATE_CLASSES)
EXPECTED_FREEDOM_SLOTS = frozenset({
    "ontological_carrier_count", "candidate_class",
    "concrete_primitives", "data_fitted_parameters",
})

CLAIM_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F1_SOURCE_ALIGNED_ROUTE_CONTRACT_001",
    "CLAIM": (
        "ეს კონტრაქტი სრულ ფიზიკურ კანდიდატს არ ირჩევს. იგი ადგენს საერთო საზღვარს: "
        "ერთი ონტოლოგიური ფუძე არ უდრის აუცილებლობით ერთელემენტიან მდგომარეობათა "
        "სივრცეს; W2-F1 კანდიდატმა უნდა გამოაცხადოს განსხვავების წყარო დასაშვები "
        "კლასიდან და სამიზნისგან დამოუკიდებლად მიიღოს მდგრადი არაეკვივალენტური "
        "დიფერენციაცია, ხოლო კვანძი, კვალი და ფარდობა შემდგომ შედეგებად დატოვოს."
    ),
    "TYPE": "DEFINITION / ROUTE_CONTRACT; არა concrete candidate და არა MECHANISM_DERIVED",
    "MODEL_VERSION": f"{MODEL_VERSION}; registry, scope or PASS-logic changes require a new version",
    "ASSUMPTIONS": [
        "Theory_Canon-ის ფუძე/გამოვლენილი გარემოს გამიჯვნა მოქმედია.",
        "W2-C0:119-ში ჩამოთვლილი deterministic, variational, stochastic, quantum და relational escape classes ღიაა და სია ამომწურავად არ ცხადდება.",
        "ამ ფაილის მექანიკური PASS არც ერთ candidate class-ს ფიზიკურად არ ამტკიცებს.",
    ],
    "DOMAIN": "W2-F1 კანდიდატთა კლასიფიკაცია და input/output საზღვარი; კონკრეტული state space, symmetry და law OPEN.",
    "CONVENTIONS": "F1 ნიშნავს მხოლოდ მდგრად არაეკვივალენტურ თვითგარჩევას; node/trace/relation ანალიზურად F2/F3 რუკაში მოწმდება. ეს კარიბჭეთა დაყოფაა და არა წინასწარ საათურ დროში ფიზიკური ქრონოლოგიის მტკიცება.",
    "FREEDOM_LEDGER": {
        "ontological_carrier_count": {"source": "Canon", "range": 1, "scale": "universal", "complexity": 0},
        "candidate_class": {"source": "research choice", "range": sorted(CANDIDATE_CLASSES), "scale": "model", "complexity": len(CANDIDATE_CLASSES)},
        "concrete_primitives": {"source": "future candidate", "range": "OPEN", "scale": "model", "complexity": "OPEN"},
        "data_fitted_parameters": {"source": "N/A", "range": 0, "scale": "data", "complexity": 0},
    },
    "DEPENDENCIES": [
        f"{PROGRAM_CONTRACT}: program boundary only",
        "w2_02 v1.5: strict singleton conditional no-go",
        "Theory_Canon.md:180-184",
        "intuitive/RefG_GE.md:119-139,751,792",
    ],
    "METHOD": "Source constraints, candidate imports and required outputs are separated into machine-readable registries.",
    "PASS_CONDITION": [
        "CODES §5-ის ყველა ველი არსებობს.",
        "ყველა მიმდინარე candidate class აცხადებს imported primitives-სა და must-derive ვალდებულებებს; სხვა მკაფიო target-free მექანიზმის სლოტიც ღიაა.",
        "F1 output არ გვხვდება candidate imports-ში.",
        "node/trace/relation არ გვხვდება ფუძის დაშვებულ input-ში.",
        "კონკრეტული კანდიდატის G1 და ყველა ფიზიკური closure flag False რჩება.",
    ],
    "FAIL_CONDITION": "მიმდინარე route-ის რეესტრი არასრულია ან სასურველ F1/F2 შედეგს/აკრძალულ ეფექტურ ცვლადს input-ად შეიტანს.",
    "FALSIFIER": "კონტრაქტში prewired output-ის ან დაურეგისტრირებელი თავისუფლების პირდაპირი აღმოჩენა.",
    "RESIDUAL": "N/A — definition/router; only set-intersection and required-field diagnostics are computed.",
    "ERROR_BOUND": "0 მხოლოდ მექანიკურ set/key checks-ზე; სემანტიკური source alignment ცალკე manual audit-ია.",
    "VALIDITY_HEALTH": "ხურავს მხოლოდ route-level G0-ს. concrete-candidate G1 და F1 მთლიანად OPEN რჩება.",
    "BRANCHES": {name: "ADMISSIBLE_CLASS__NOT_SELECTED__PHYSICAL_STATUS_OPEN" for name in CANDIDATE_CLASSES},
    "OBSERVABLE_MAP": "N/A — F1 route contract has no observable.",
    "FORWARD_MODEL": "N/A — physical bridge not constructed.",
    "DATA_ROLE": "N/A — no data used.",
    "IDENTIFIABILITY": "Mechanical only: forbidden-input intersection must be empty; physical identifiability N/A.",
    "BENCHMARK": "Embedded negative control injects recurrence and persistent trace as primitives and must be rejected.",
    "CLOSURE_FLAGS": dict(INITIAL_CLOSURE_FLAGS),
    "GATE_APPLICABILITY": dict(GATE_APPLICABILITY),
    "CROSSCHECK": "Mechanical registry check plus separate direct source-phrase presence check; neither substitutes semantic audit.",
    "PROVENANCE": "runtime SHA-256 for CODES, Canon, intuitive source, W2-C0, w2_02 and this file",
    "FILES": [
        "CODES.md", "Theory_Canon.md", "intuitive/RefG_GE.md",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_02_f1_singleton_no_go_gate.py",
        "RefG/work 2/w2_03_f1_source_aligned_route_contract.py",
    ],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def import_violations(imports: set[str]) -> set[str]:
    """One validator used for both the real registry and negative controls."""
    return imports & (
        FORBIDDEN_PREWIRED_INPUTS
        | DEFERRED_OUTPUTS
        | DOWNSTREAM_TARGETS_NOT_F1_PRIMITIVES
        | {F1_REQUIRED_OUTPUT}
    )


def freedom_ledger_schema_valid(ledger: Any) -> bool:
    required = {"source", "range", "scale", "complexity"}
    return (
        isinstance(ledger, dict)
        and set(ledger) == EXPECTED_FREEDOM_SLOTS
        and all(
        isinstance(entry, dict)
        and set(entry) == required
        and all(
            value is not None
            and (not isinstance(value, str) or bool(value.strip()))
            for value in entry.values()
        )
        for entry in ledger.values()
        )
    )


def candidate_registry_schema_valid(registry: Any) -> bool:
    required = {"imports_to_declare", "must_derive"}
    return (
        isinstance(registry, dict)
        and set(registry) == EXPECTED_CANDIDATE_CLASS_NAMES
        and all(
            isinstance(spec, dict)
            and set(spec) == required
            and all(
                isinstance(spec[key], (list, tuple))
                and bool(spec[key])
                and all(isinstance(item, str) and item.strip() for item in spec[key])
                and len(set(spec[key])) == len(spec[key])
                for key in required
            )
            for spec in registry.values()
        )
    )


def load_gate_report(path: Path, module_name: str) -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_gate()


def run_gate() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    paths = {
        "CODES": root / "CODES.md",
        "CANON": root / "Theory_Canon.md",
        "INTUITIVE": root / "intuitive" / "RefG_GE.md",
        "W2_C0": root / "RefG" / "work 2" / "w2_00_foundation_to_einstein_contract.md",
        "W2_02": root / "RefG" / "work 2" / "w2_02_f1_singleton_no_go_gate.py",
        "SOURCE": Path(__file__).resolve(),
    }
    canon_text = paths["CANON"].read_text(encoding="utf-8")
    intuitive_text = paths["INTUITIVE"].read_text(encoding="utf-8")
    w2c0_text = paths["W2_C0"].read_text(encoding="utf-8")

    dependency_report = load_gate_report(paths["W2_02"], "w2_02_singleton_dependency")
    dependency_no_go_pass = (
        dependency_report.get("status") == "EXACT_SINGLETON_NO_GO_PASS__W2_F1_OPEN"
        and dependency_report.get("model_version") == "W2-F1-SINGLETON-NO-GO-v1.5-corrected-internal"
        and dependency_report.get("closure_flags", {}).get("W2_F1_SELF_DIFFERENTIATION") is False
    )
    required_route_classes = {
        "symmetric_instability_or_bifurcation",
        "atemporal_nonunique_solution_structure",
        "stochastic_or_quantum_outcome",
        "state_space_generating_rule",
        "nontrivial_relational_state_space",
        "other_explicit_target_free_mechanism",
    }
    full_contract = REQUIRED_FIELDS.issubset(CLAIM_CONTRACT)
    contract_values_nonempty = all(
        value.strip() if isinstance(value, str) else bool(value)
        for value in (CLAIM_CONTRACT.get(key) for key in REQUIRED_FIELDS)
    )
    text_sequences_valid = all(
        isinstance(CLAIM_CONTRACT.get(key), (list, tuple))
        and bool(CLAIM_CONTRACT[key])
        and all(isinstance(item, str) and item.strip() for item in CLAIM_CONTRACT[key])
        for key in ("ASSUMPTIONS", "DEPENDENCIES", "PASS_CONDITION", "FILES")
    )
    version_contract_bound = (
        isinstance(CLAIM_CONTRACT.get("MODEL_VERSION"), str)
        and CLAIM_CONTRACT["MODEL_VERSION"].startswith(f"{MODEL_VERSION};")
    )
    source_constraints_valid = (
        set(SOURCE_CONSTRAINTS) == REQUIRED_SOURCE_CONSTRAINT_KEYS
        and all(value is True for value in SOURCE_CONSTRAINTS.values())
    )
    gate_applicability_complete = (
        set(GATE_APPLICABILITY) == UNIVERSAL_GATES
        and all(isinstance(value, str) and value.strip() for value in GATE_APPLICABILITY.values())
    )
    contract_registries_bound = (
        GATE_APPLICABILITY == EXPECTED_GATE_APPLICABILITY
        and CLAIM_CONTRACT.get("GATE_APPLICABILITY") == EXPECTED_GATE_APPLICABILITY
        and set(INITIAL_CLOSURE_FLAGS) == EXPECTED_CLOSURE_KEYS
        and not any(INITIAL_CLOSURE_FLAGS.values())
        and set(CLAIM_CONTRACT.get("CLOSURE_FLAGS", {})) == EXPECTED_CLOSURE_KEYS
        and not any(CLAIM_CONTRACT.get("CLOSURE_FLAGS", {}).values())
    )
    freedom_ledger_complete = freedom_ledger_schema_valid(CLAIM_CONTRACT.get("FREEDOM_LEDGER"))
    required_route_classes_present = set(CANDIDATE_CLASSES) == required_route_classes
    all_classes_complete = candidate_registry_schema_valid(CANDIDATE_CLASSES)
    imports = {
        item
        for spec in CANDIDATE_CLASSES.values()
        for item in spec["imports_to_declare"]
    } if all_classes_complete else set()
    expected_branches = {
        name: "ADMISSIBLE_CLASS__NOT_SELECTED__PHYSICAL_STATUS_OPEN"
        for name in CANDIDATE_CLASSES
    }
    branch_registry_exact = CLAIM_CONTRACT.get("BRANCHES") == expected_branches
    actual_import_violations = import_violations(imports)
    f1_not_prewired = F1_REQUIRED_OUTPUT not in actual_import_violations
    deferred_not_prewired = not (DEFERRED_OUTPUTS & actual_import_violations)
    forbidden_effective_inputs_absent = not (FORBIDDEN_PREWIRED_INPUTS & actual_import_violations)
    downstream_targets_not_prewired = not (DOWNSTREAM_TARGETS_NOT_F1_PRIMITIVES & actual_import_violations)

    embedded_bad_candidate_inputs = {
        "configuration_space", "recurrence_or_phase_relation", "persistent_trace",
        "metric_g_munu", "manifested_multichannel_environment",
    }
    negative_control_violations = import_violations(embedded_bad_candidate_inputs)
    negative_control_rejected = {
        "recurrence_or_phase_relation", "persistent_trace", "metric_g_munu",
        "manifested_multichannel_environment",
    }.issubset(negative_control_violations)

    source_phrase_presence = (
        "მდგრადი კვალი, ფაზური ფარდობა და კვანძური ურთიერთობა" in canon_text
        and "ზოგად მცირე შეშფოთებას" in w2c0_text
        and "გაყინულ სტოქასტიკურ ან კვანტურ წყაროს" in w2c0_text
        and "ორ ასიმპტოტურ ზღვარს" in intuitive_text
    )
    initial_flags_false = not any(INITIAL_CLOSURE_FLAGS.values())
    passed = all((
        full_contract, contract_values_nonempty, text_sequences_valid,
        version_contract_bound,
        source_constraints_valid, dependency_no_go_pass,
        gate_applicability_complete, required_route_classes_present, all_classes_complete,
        contract_registries_bound, freedom_ledger_complete, branch_registry_exact,
        not actual_import_violations, f1_not_prewired, deferred_not_prewired,
        forbidden_effective_inputs_absent, downstream_targets_not_prewired,
        negative_control_rejected, source_phrase_presence, initial_flags_false,
    ))
    closure_flags = dict(INITIAL_CLOSURE_FLAGS)
    closure_flags["G0_GOAL"] = passed
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": "ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_G1_AND_PHYSICAL_F1_OPEN" if passed else "ROUTE_SCHEMA_VALIDATION_FAIL",
        "CHECKS": {
            "required_contract_fields_present": full_contract,
            "contract_values_nonempty": contract_values_nonempty,
            "required_text_sequences_valid": text_sequences_valid,
            "contract_and_runtime_model_versions_bound": version_contract_bound,
            "singleton_no_go_dependency_reexecuted_and_verified": dependency_no_go_pass,
            "source_constraints_valid": source_constraints_valid,
            "G0_to_G8_applicability_complete": gate_applicability_complete,
            "contract_and_global_registries_bound": contract_registries_bound,
            "freedom_ledger_schema_complete": freedom_ledger_complete,
            "branch_registry_exact": branch_registry_exact,
            "required_current_route_classes_present": required_route_classes_present,
            "all_candidate_classes_have_import_and_derivation_ledgers": all_classes_complete,
            "F1_result_not_prewired": f1_not_prewired,
            "deferred_outputs_not_prewired": deferred_not_prewired,
            "forbidden_effective_inputs_absent": forbidden_effective_inputs_absent,
            "downstream_targets_not_prewired": downstream_targets_not_prewired,
            "actual_import_violations_empty": not actual_import_violations,
            "embedded_prewired_negative_control_rejected": negative_control_rejected,
            "source_phrase_presence_only": source_phrase_presence,
            "initial_closure_flags_false": initial_flags_false,
        },
        "SOURCE_CONSTRAINTS": SOURCE_CONSTRAINTS,
        "CANDIDATE_CLASSES": CANDIDATE_CLASSES,
        "FORBIDDEN_PREWIRED_INPUTS": sorted(FORBIDDEN_PREWIRED_INPUTS),
        "F1_REQUIRED_OUTPUT": F1_REQUIRED_OUTPUT,
        "DEFERRED_OUTPUTS": sorted(DEFERRED_OUTPUTS),
        "DOWNSTREAM_TARGETS_NOT_F1_PRIMITIVES": sorted(DOWNSTREAM_TARGETS_NOT_F1_PRIMITIVES),
        "GATE_APPLICABILITY": GATE_APPLICABILITY,
        "CLOSURE_FLAGS": closure_flags,
        "PROVENANCE": {name: sha256(path) for name, path in paths.items()},
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["STATUS"].startswith("ROUTE_SCHEMA_VALIDATED") else 1


if __name__ == "__main__":
    raise SystemExit(main())
