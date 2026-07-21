"""Provisional W2-F1 primary research route after the two exact no-go bounds.

This file selects a route for development, not a physical truth. The selection
is mutable and all physical closure flags remain false.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


MODEL_VERSION = "W2-F1-PRIMARY-ROUTE-SPEC-v1.7-internal"
REGISTERED_PRIMARY_ROUTE = "SYMMETRIC_BIFURCATION_WITH_TARGET_FREE_GENERIC_SEED"
PRIMARY_ROUTE = REGISTERED_PRIMARY_ROUTE
UNIVERSAL_GATES = frozenset({
    "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
    "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
    "G7_OBSERVATION", "G8_EXPORT",
})

REQUIRED_FIELDS = {
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "GATE_APPLICABILITY", "CROSSCHECK", "PROVENANCE", "FILES",
}

EXPECTED_ROUTE_OBLIGATIONS = {
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
ROUTE_OBLIGATIONS = dict(EXPECTED_ROUTE_OBLIGATIONS)

EXPECTED_EXCLUDED_SHORTCUTS = {
    "exact_q0_plus_single_valued_equivariant_update": "w2_04 no-go",
    "strict_singleton_state_space": "w2_02 no-go",
    "prelabelled_recurrence_trace_or_node": "target leakage",
    "instability_without_seed_realization": "exact q0 never leaves by itself",
    "gauge_related_minima_called_physical_multiplicity": "equivalence error",
    "observed_geometry_or_GR_inserted_as_boundary_condition": "target leakage",
}
EXCLUDED_SHORTCUTS = dict(EXPECTED_EXCLUDED_SHORTCUTS)

ALTERNATIVE_CLASSES_REMAIN_OPEN = {
    "atemporal_nonunique_solution_structure",
    "stochastic_or_quantum_outcome",
    "state_space_generating_rule",
    "nontrivial_relational_state_space",
    "other_explicit_target_free_mechanism",
}

EXPECTED_KNOWN_TOY_LIMITS = {
    "w2_01_imports": "R2, O(2), quartic functional and broken-sign parameter domain are not derived",
    "tangent_zero_mode": "a zero Hessian tangent is not yet a physical Goldstone mode",
    "variational_vs_temporal": "q=0 instability is variational; temporal decay is not proved",
    "orbit_vs_realization": "existence of a solution orbit is distinct from realization of one branch",
    "F2_boundary": "absence of node/trace/relation leaves F2 open and is not by itself an F1 failure",
}
KNOWN_TOY_LIMITS = dict(EXPECTED_KNOWN_TOY_LIMITS)

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
    "ROUTE_SPEC_VALIDATED": False,
    "ROUTE_NEGATIVE_CONTROLS": False,
    "PRIMARY_ROUTE_SELECTED_FOR_DEVELOPMENT": False,
    "W2_F1_SELF_DIFFERENTIATION": False,
    "W2_F2_OPERATIONAL_RELATIONS": False,
    "W2_F3_INTERNAL_ORDER_CAUSALITY": False,
    "W2_F4_INDEPENDENT_ADDITIVE_MODES": False,
}

GATE_APPLICABILITY = {
    "G0_GOAL": "REQUIRED — provisional route claim, scope, obligations and revision rule",
    "G1_CONVENTIONS": "OPEN — concrete state space, G_sym role, equivalence and seed law are not fixed",
    "G2_CORE_ALGEBRA": "OPEN — no concrete functional or equation",
    "G3_STRUCTURE": "OPEN — instability, basin, branch stability and non-gauge inequivalence unproved",
    "G4_INDEPENDENT_CHECK": "OPEN — no concrete candidate to rederive",
    "G5_LIMITS_REGRESSION": "N/A — no physical solution; route-specific negative controls use a separate flag",
    "G6_PHYSICAL_MATCH": "N/A — no source, energy ledger or observable map",
    "G7_OBSERVATION": "N/A — no data or prediction",
    "G8_EXPORT": "N/A — internal Git-ignored route decision; no export authorized",
}
EXPECTED_CLOSURE_KEYS = frozenset(INITIAL_CLOSURE_FLAGS)
EXPECTED_GATE_APPLICABILITY = dict(GATE_APPLICABILITY)

CLAIM_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F1_PRIMARY_ROUTE_SPECIFICATION_001",
    "CLAIM": (
        "შემდეგი კონკრეტული W2-F1 კანდიდატის სამუშაო პრიორიტეტად ირჩევა ერთი "
        "მატარებლის ზუსტად სიმეტრიული ტოტის ბიფურკაცია, რომელსაც არასიმეტრიული "
        "მიმართულება წინასწარ არ აქვს ჩადებული და რომლის branch realization-ს "
        "G_sym-ინვარიანტული seed-განაწილება, არასიმეტრიული ინდივიდუალური realization "
        "და შინაგანი outcome მექანიზმი ახლავს. Set-valued ატემპორალური არჩევა ცალკე "
        "ღია ალტერნატიულ კლასად რჩება. "
        "ეს არის გადასინჯვადი კვლევითი არჩევანი და არა ფიზიკური დახურვა."
    ),
    "TYPE": "CANDIDATE / ARCHITECTURE_DECISION; არა EXACT_IDENTITY და არა MECHANISM_DERIVED",
    "MODEL_VERSION": f"{MODEL_VERSION}; route, obligations, controls or PASS-logic changes require a new version",
    "ASSUMPTIONS": [
        "w2_02 strict-singleton no-go მოქმედია თავის პირობით დომენში.",
        "w2_04 equivariant fixed-set no-go მოქმედია თავის პირობით დომენში.",
        "w2_01 მხოლოდ Landau-class toy positive control-ია.",
        "ყველა route choice დაკვირვებებთან შეუსაბამობისას ან უკეთესი მექანიზმის აღმოჩენისას გადაიხედება.",
    ],
    "DOMAIN": "მხოლოდ მომდევნო F1 candidate-ის კვლევითი პრიორიტეტი; კონკრეტული ფიზიკური მოდელი ჯერ არ არსებობს.",
    "CONVENTIONS": (
        "G_sym არის კანდიდატის შიდა სიმეტრიის ჯგუფი და არა Newton-ის G. seed-ების "
        "განაწილება G_sym-ინვარიანტულია, ხოლო generic realization შეიძლება არასიმეტრიული "
        "იყოს; iteration parameter ფიზიკურ საათურ დროს ავტომატურად არ ნიშნავს."
    ),
    "FREEDOM_LEDGER": {
        "route_choice": {"source": "methodological decision", "range": PRIMARY_ROUTE, "scale": "programme", "complexity": 1},
        "configuration_space": {"source": "future candidate", "range": "OPEN", "scale": "model", "complexity": "OPEN"},
        "symmetry_G_sym": {"source": "future candidate", "range": "OPEN/nontrivial; global-vs-gauge role required", "scale": "model", "complexity": "OPEN"},
        "parameter_and_open_domain": {"source": "future candidate", "range": "OPEN", "scale": "branch", "complexity": "OPEN"},
        "gauge_or_relabel_equivalence": {"source": "future candidate", "range": "OPEN", "scale": "model", "complexity": "OPEN"},
        "q0_undifferentiatedness_criterion": {"source": "future candidate", "range": "OPEN/mod declared equivalence", "scale": "branch", "complexity": "OPEN"},
        "stability_criterion": {"source": "future candidate", "range": "OPEN", "scale": "branch", "complexity": "OPEN"},
        "functional_or_rule": {"source": "future candidate", "range": "OPEN/target-free", "scale": "model", "complexity": "OPEN"},
        "seed_distribution": {"source": "future candidate", "range": "OPEN/G_sym-invariant", "scale": "model", "complexity": "OPEN"},
        "successful_seed_basin_measure": {"source": "future candidate", "range": "OPEN/open or nonzero measure", "scale": "branch", "complexity": "OPEN"},
        "seed_sampling_or_outcome": {"source": "future candidate", "range": "OPEN/internal", "scale": "realization", "complexity": "OPEN"},
        "data_fitted_parameters": {"source": "N/A", "range": 0, "scale": "data", "complexity": 0},
    },
    "DEPENDENCIES": [
        "w2_03 route contract: admissible classes only",
        "w2_02 v1.5: strict singleton no-go",
        "w2_04 v1.7: equivariant fixed-set no-go",
        "w2_01 v1.2: toy O(2) positive control",
    ],
    "METHOD": "No-go elimination, target-leakage guard and provisional continuity with the existing toy mechanism class; no minimality theorem is claimed.",
    "PASS_CONDITION": [
        "route specification contains every open obligation and excluded shortcut.",
        "no open physical obligation is marked derived.",
        "all alternative candidate classes remain OPEN rather than REJECTED.",
        "w2_01-ის ვიწრო toy limits სრულადაა აღრიცხული და ფიზიკურ F1-ად არ გადადის.",
        "physical W2_F1 flag remains False.",
    ],
    "FAIL_CONDITION": "route is presented as physical fact, hides an imported primitive, or prewires a preferred branch/geometry.",
    "FALSIFIER": (
        "A concrete implementation of this route necessarily violates source constraints, "
        "cannot create stable inequivalent sectors without target leakage, or an alternative "
        "class closes the same obligations with fewer unsupported primitives."
    ),
    "RESIDUAL": "N/A — no field equation; registry completeness only.",
    "ERROR_BOUND": "0 for key/set checks; physical uncertainty N/A because no physical output exists.",
    "VALIDITY_HEALTH": (
        "Route adoption does not imply existence, uniqueness, stability, causality or observation. "
        "Instability alone is explicitly insufficient without a seed/outcome account, and "
        "this route has not been proved to minimize primitive count against all alternatives."
    ),
    "BRANCHES": {
        PRIMARY_ROUTE: "PRIMARY_DEVELOPMENT_CANDIDATE__PHYSICS_OPEN",
        **{name: "ALTERNATIVE_OPEN__NOT_REJECTED" for name in ALTERNATIVE_CLASSES_REMAIN_OPEN},
    },
    "OBSERVABLE_MAP": "N/A — no physical variables yet.",
    "FORWARD_MODEL": "N/A — no bridge to observables or data.",
    "DATA_ROLE": "N/A — no data used for route selection.",
    "IDENTIFIABILITY": "N/A physically; future candidate must separate gauge orbit from physically inequivalent sectors.",
    "BENCHMARK": (
        "Positive methodological control: all obligations OPEN and no target direction. "
        "Negative controls: preferred seed, gauge-only multiplicity, and instability without realization mechanism."
    ),
    "CLOSURE_FLAGS": dict(INITIAL_CLOSURE_FLAGS),
    "GATE_APPLICABILITY": dict(GATE_APPLICABILITY),
    "CROSSCHECK": "w2_01–w2_04 reports are re-executed and their exact status/F1 flags checked; route-specific negative controls use the same validator as the real registry.",
    "PROVENANCE": "runtime SHA-256 of Work2 dependencies and this source",
    "FILES": [
        "CODES.md", "Theory_Canon.md", "intuitive/RefG_GE.md",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_01_self_differentiation_candidate_gate.py",
        "RefG/work 2/w2_02_f1_singleton_no_go_gate.py",
        "RefG/work 2/w2_03_f1_source_aligned_route_contract.py",
        "RefG/work 2/w2_04_f1_equivariant_fixed_set_no_go_gate.py",
        "RefG/work 2/w2_05_f1_primary_route_specification.py",
    ],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


REQUIRED_OBLIGATION_KEYS = frozenset(EXPECTED_ROUTE_OBLIGATIONS)

REQUIRED_SHORTCUT_KEYS = {
    "exact_q0_plus_single_valued_equivariant_update",
    "strict_singleton_state_space", "prelabelled_recurrence_trace_or_node",
    "instability_without_seed_realization",
    "gauge_related_minima_called_physical_multiplicity",
    "observed_geometry_or_GR_inserted_as_boundary_condition",
}


def load_gate_report(path: Path, module_name: str) -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_gate()


def freedom_ledger_schema_valid(ledger: Any) -> bool:
    required = {"source", "range", "scale", "complexity"}
    return isinstance(ledger, dict) and bool(ledger) and all(
        isinstance(entry, dict)
        and set(entry) == required
        and all(
            value is not None
            and (not isinstance(value, str) or bool(value.strip()))
            for value in entry.values()
        )
        for entry in ledger.values()
    )


def validate_route_registry(
    route: str,
    obligations: dict[str, str],
    shortcuts: dict[str, str],
) -> list[str]:
    issues: list[str] = []
    if route != REGISTERED_PRIMARY_ROUTE:
        issues.append("unregistered_primary_route")
    forbidden_route_tokens = {"OBSERVED", "PREWIRED", "TARGET_VALUE", "GR_GEOMETRY", "PPN_VALUE"}
    if any(token in route.upper() for token in forbidden_route_tokens):
        issues.append("target_leakage_in_route_name")
    if set(obligations) != REQUIRED_OBLIGATION_KEYS:
        issues.append("obligation_registry_mismatch")
    if obligations != EXPECTED_ROUTE_OBLIGATIONS:
        issues.append("obligation_status_registry_mismatch")
    if any(value not in {"OPEN", "REQUIRED", "SOURCE_CONSTRAINT"} for value in obligations.values()):
        issues.append("dishonest_obligation_status")
    if obligations.get("no_preferred_direction_or_observed_target_in_inputs") != "REQUIRED":
        issues.append("target_leakage_guard_missing")
    if shortcuts != EXPECTED_EXCLUDED_SHORTCUTS:
        issues.append("excluded_shortcut_registry_mismatch")
    return issues


def run_gate() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    work2 = root / "RefG" / "work 2"
    paths = {
        "CODES": root / "CODES.md",
        "CANON": root / "Theory_Canon.md",
        "INTUITIVE": root / "intuitive" / "RefG_GE.md",
        "W2_C0": work2 / "w2_00_foundation_to_einstein_contract.md",
        "W2_01": work2 / "w2_01_self_differentiation_candidate_gate.py",
        "W2_02": work2 / "w2_02_f1_singleton_no_go_gate.py",
        "W2_03": work2 / "w2_03_f1_source_aligned_route_contract.py",
        "W2_04": work2 / "w2_04_f1_equivariant_fixed_set_no_go_gate.py",
        "SOURCE": Path(__file__).resolve(),
    }
    dependency_reports = {
        "W2_01": load_gate_report(paths["W2_01"], "w2_01_dependency"),
        "W2_02": load_gate_report(paths["W2_02"], "w2_02_dependency"),
        "W2_03": load_gate_report(paths["W2_03"], "w2_03_dependency"),
        "W2_04": load_gate_report(paths["W2_04"], "w2_04_dependency"),
    }
    dependency_statuses = {
        name: report.get("STATUS") or report.get("status") or "MISSING"
        for name, report in dependency_reports.items()
    }
    expected_statuses = {
        "W2_01": "EXACT_IDENTITY_PASS__TOY_POSITIVE_CONTROL__W2_F1_OPEN",
        "W2_02": "EXACT_SINGLETON_NO_GO_PASS__W2_F1_OPEN",
        "W2_03": "ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_G1_AND_PHYSICAL_F1_OPEN",
        "W2_04": "CONDITIONAL_EXACT_FIXED_SET_THEOREM_PASS__INTERNAL__W2_F1_OPEN",
    }
    dependency_versions = {
        name: report.get("MODEL_VERSION") or report.get("model_version") or "MISSING"
        for name, report in dependency_reports.items()
    }
    expected_versions = {
        "W2_01": "W2-F1-RADIAL-LANDAU-v1.2-frozen",
        "W2_02": "W2-F1-SINGLETON-NO-GO-v1.5-corrected-internal",
        "W2_03": "W2-F1-SOURCE-ALIGNED-ROUTE-CONTRACT-v1.8-internal",
        "W2_04": "W2-F1-EQUIVARIANT-FIXED-SET-NO-GO-v1.7-internal",
    }
    dependency_statuses_verified = all(
        dependency_statuses[name] == expected_statuses[name]
        and dependency_versions[name] == expected_versions[name]
        for name in expected_statuses
    )
    dependency_f1_flags_open = all(
        (report.get("CLOSURE_FLAGS") or report.get("closure_flags") or {}).get(
            "W2_F1_SELF_DIFFERENTIATION"
        ) is False
        for report in dependency_reports.values()
    )

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
        and ROUTE_OBLIGATIONS == EXPECTED_ROUTE_OBLIGATIONS
    )
    real_registry_issues = validate_route_registry(PRIMARY_ROUTE, ROUTE_OBLIGATIONS, EXCLUDED_SHORTCUTS)
    all_obligations_declared = ROUTE_OBLIGATIONS == EXPECTED_ROUTE_OBLIGATIONS
    open_items_honest = not any(
        issue in {"dishonest_obligation_status", "obligation_status_registry_mismatch"}
        for issue in real_registry_issues
    )
    route_contract_classes = set(dependency_reports["W2_03"].get("CANDIDATE_CLASSES", {}))
    expected_alternative_classes = route_contract_classes - {"symmetric_instability_or_bifurcation"}
    expected_branches = {
        REGISTERED_PRIMARY_ROUTE: "PRIMARY_DEVELOPMENT_CANDIDATE__PHYSICS_OPEN",
        **{
            name: "ALTERNATIVE_OPEN__NOT_REJECTED"
            for name in expected_alternative_classes
        },
    }
    branch_registry_exact = CLAIM_CONTRACT.get("BRANCHES") == expected_branches
    alternatives_open = (
        set(ALTERNATIVE_CLASSES_REMAIN_OPEN) == expected_alternative_classes
        and branch_registry_exact
    )
    toy_limits_complete = KNOWN_TOY_LIMITS == EXPECTED_KNOWN_TOY_LIMITS
    required_freedom_slots = {
        "route_choice", "configuration_space", "symmetry_G_sym",
        "parameter_and_open_domain", "gauge_or_relabel_equivalence",
        "q0_undifferentiatedness_criterion", "stability_criterion",
        "functional_or_rule", "seed_distribution", "successful_seed_basin_measure",
        "seed_sampling_or_outcome", "data_fitted_parameters",
    }
    freedom_ledger_complete = (
        set(CLAIM_CONTRACT.get("FREEDOM_LEDGER", {})) == required_freedom_slots
        and freedom_ledger_schema_valid(CLAIM_CONTRACT.get("FREEDOM_LEDGER"))
    )

    missing_obligation_control = dict(ROUTE_OBLIGATIONS)
    missing_obligation_control.pop("seed_or_selection_origin")
    preferred_direction_control = dict(ROUTE_OBLIGATIONS)
    preferred_direction_control["no_preferred_direction_or_observed_target_in_inputs"] = "VIOLATED"
    prematurely_closed_control = dict(ROUTE_OBLIGATIONS)
    prematurely_closed_control["seed_or_selection_origin"] = "REQUIRED"
    control_issues = {
        "empty_shortcuts": validate_route_registry(PRIMARY_ROUTE, ROUTE_OBLIGATIONS, {}),
        "prewired_route": validate_route_registry("OBSERVED_GR_GEOMETRY_PREWIRED", ROUTE_OBLIGATIONS, EXCLUDED_SHORTCUTS),
        "neutral_unregistered_route": validate_route_registry("UNREGISTERED_NEUTRAL_ROUTE", ROUTE_OBLIGATIONS, EXCLUDED_SHORTCUTS),
        "missing_obligation": validate_route_registry(PRIMARY_ROUTE, missing_obligation_control, EXCLUDED_SHORTCUTS),
        "preferred_direction": validate_route_registry(PRIMARY_ROUTE, preferred_direction_control, EXCLUDED_SHORTCUTS),
        "prematurely_closed_obligation": validate_route_registry(PRIMARY_ROUTE, prematurely_closed_control, EXCLUDED_SHORTCUTS),
    }
    negative_controls = {
        "empty_shortcut_registry_rejected_by_expected_code": "excluded_shortcut_registry_mismatch" in control_issues["empty_shortcuts"],
        "prewired_route_rejected_by_target_leakage_code": "target_leakage_in_route_name" in control_issues["prewired_route"],
        "neutral_unregistered_route_rejected_by_registration_code": "unregistered_primary_route" in control_issues["neutral_unregistered_route"],
        "missing_obligation_rejected_by_expected_code": "obligation_registry_mismatch" in control_issues["missing_obligation"],
        "preferred_direction_rejected_by_guard_code": "target_leakage_guard_missing" in control_issues["preferred_direction"],
        "premature_closure_rejected_by_status_registry_code": "obligation_status_registry_mismatch" in control_issues["prematurely_closed_obligation"],
    }
    negative_controls_pass = all(negative_controls.values())
    initial_flags_false = not any(INITIAL_CLOSURE_FLAGS.values())
    dependencies_exist = all(path.is_file() for path in paths.values())
    passed = all((
        full_contract, contract_values_nonempty, text_sequences_valid,
        version_contract_bound,
        gate_applicability_complete,
        contract_registries_bound, branch_registry_exact,
        not real_registry_issues,
        all_obligations_declared, open_items_honest, alternatives_open,
        toy_limits_complete, freedom_ledger_complete, negative_controls_pass,
        initial_flags_false, dependencies_exist, dependency_statuses_verified,
        dependency_f1_flags_open,
    ))
    closure_flags = dict(INITIAL_CLOSURE_FLAGS)
    closure_flags["G0_GOAL"] = passed
    closure_flags["ROUTE_SPEC_VALIDATED"] = passed
    closure_flags["ROUTE_NEGATIVE_CONTROLS"] = passed and negative_controls_pass
    closure_flags["PRIMARY_ROUTE_SELECTED_FOR_DEVELOPMENT"] = passed
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": "PRIMARY_ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_MODEL_AND_W2_F1_OPEN" if passed else "PRIMARY_ROUTE_SCHEMA_VALIDATION_FAIL",
        "PRIMARY_ROUTE": PRIMARY_ROUTE,
        "CHECKS": {
            "required_contract_fields_present": full_contract,
            "contract_values_nonempty": contract_values_nonempty,
            "required_text_sequences_valid": text_sequences_valid,
            "contract_and_runtime_model_versions_bound": version_contract_bound,
            "G0_to_G8_applicability_complete": gate_applicability_complete,
            "contract_and_global_registries_bound": contract_registries_bound,
            "branch_registry_exact": branch_registry_exact,
            "real_route_registry_has_no_issues": not real_registry_issues,
            "all_route_obligations_declared": all_obligations_declared,
            "open_items_honestly_open": open_items_honest,
            "alternative_classes_remain_open": alternatives_open,
            "known_toy_limits_complete": toy_limits_complete,
            "freedom_ledger_complete": freedom_ledger_complete,
            "route_negative_controls_pass": negative_controls_pass,
            "initial_closure_flags_false": initial_flags_false,
            "dependencies_exist": dependencies_exist,
            "dependency_statuses_reexecuted_and_verified": dependency_statuses_verified,
            "dependency_W2_F1_flags_open": dependency_f1_flags_open,
        },
        "NEGATIVE_CONTROLS": negative_controls,
        "NEGATIVE_CONTROL_ISSUES": control_issues,
        "DEPENDENCY_STATUSES": dependency_statuses,
        "DEPENDENCY_VERSIONS": dependency_versions,
        "ROUTE_OBLIGATIONS": ROUTE_OBLIGATIONS,
        "EXCLUDED_SHORTCUTS": EXCLUDED_SHORTCUTS,
        "ALTERNATIVE_CLASSES_REMAIN_OPEN": sorted(ALTERNATIVE_CLASSES_REMAIN_OPEN),
        "KNOWN_TOY_LIMITS": KNOWN_TOY_LIMITS,
        "NEXT_ATOMIC_TASK": (
            "Propose one concrete configuration space, nontrivial G_sym with declared "
            "global-vs-gauge role, target-free functional/rule and an operational criterion "
            "that q0 has no nontrivial distinguishable internal role/relational structure "
            "modulo the declared equivalence; derive q0 stability change, a non-gauge stable "
            "branch, a G_sym-invariant seed distribution, an open/nonzero-measure basin of "
            "successful nonsymmetric realizations, and an internal seed/outcome origin "
            "before introducing node, trace, relation, spacetime or observations."
        ),
        "GATE_APPLICABILITY": GATE_APPLICABILITY,
        "CLOSURE_FLAGS": closure_flags,
        "PROVENANCE": {name: sha256(path) for name, path in paths.items()},
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["STATUS"].startswith("PRIMARY_ROUTE_SCHEMA_VALIDATED") else 1


if __name__ == "__main__":
    raise SystemExit(main())
