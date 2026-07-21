"""Outcome-neutral contract for the Work-2 F3 internal-causality gate.

The inherited w2_16 endpoint contains exact, atemporal F1/F2 structure but no
transition law.  This file freezes what a later candidate must supply before
an internal ordering may be called causal.  In particular, a state ranking,
matrix correlation, Krylov depth, graph written into the input, or execution
order of an algorithm is not by itself physical influence.

This is a definition artifact.  It can validate the F3 contract and its
fail-closed logic; it cannot evaluate a candidate or close F3.
"""

from __future__ import annotations

import json
from typing import Any


F3_GATE_KEYS = frozenset({
    "same_chain_F1_F2_predecessors_valid",
    "state_owned_events_or_changes_derived",
    "target_free_transition_or_response_law_derived",
    "candidate_dynamics_health_and_state_space_closure_proved",
    "allowed_interventions_defined",
    "directed_intervention_response_proved",
    "correlation_and_static_ranking_excluded",
    "complete_equivalence_invariance_proved",
    "arrow_selected_by_law_not_labels_or_schedule",
    "nontrivial_direct_influence_on_predeclared_open_domain",
    "strict_relation_irreflexive_asymmetric_and_acyclic",
    "effective_order_transitive_and_reflexive_closure_antisymmetric",
    "forbidden_signal_nontransmission_proved",
    "computational_schedule_neutrality_proved",
    "null_reverse_and_target_leak_controls_pass",
    "perturbation_and_initial_condition_stability_proved",
    "independent_second_derivation_passes",
    "physical_time_metric_and_downstream_gates_remain_open",
})
EXPECTED_F3_GATE_KEYS = frozenset(F3_GATE_KEYS)

REQUIRED_CANDIDATE_MAPS = (
    "state_space",
    "event_or_change_map",
    "complete_equivalence_action",
    "transition_or_response_law",
    "signal_support_or_update_composition",
    "allowed_interventions",
    "intervention_to_response_map",
    "direct_influence_relation",
    "transitive_effective_order",
    "forbidden_pairs",
    "no_transmission_test",
    "open_domain",
    "null_branches",
    "perturbation_class",
    "independent_crosscheck",
)
EXPECTED_REQUIRED_CANDIDATE_MAPS = tuple(REQUIRED_CANDIDATE_MAPS)
CANDIDATE_MAP_ENTRY_KEYS = frozenset({"status", "source", "definition"})
CANDIDATE_MAP_STATUSES = frozenset({"DERIVED", "PARTIAL", "ABSENT", "NOT_APPLICABLE"})

FORBIDDEN_PRELOADS = (
    "physical position, physical time, external clock, or 3+1 split",
    "lattice, locality graph, causal DAG, time layers, or event numbering",
    "Lorentzian metric, light cone, GR, Einstein equations, or PN/PPN target",
    "preferred basis, axis, orientation, labels, or state-external seed",
    "history, lag, memory, retarded kernel, or update arrow not derived from the law",
    "correlation, commutator sign, eigenvalue rank, or Krylov depth renamed causality",
    "algorithmic iteration or execution schedule renamed physical process order",
    "post-selection of the branch or convention that gives the desired arrow",
)
EXPECTED_FORBIDDEN_PRELOADS = tuple(FORBIDDEN_PRELOADS)

MANDATORY_CONTROLS = (
    "known directed acyclic influence positive control",
    "frozen or nonresponsive null",
    "correlated but noninterventional null",
    "two-way reachability between the same event occurrences rejection",
    "directed-cycle rejection",
    "prewired target-DAG rejection",
    "basis, label, reflection, and reversal mutations",
    "execution-schedule permutation",
    "F2 nulls S=0, R=0, tau=0, tau=1, tuned branch, and singular normalization",
    "small-perturbation and allowed-initial-condition stability",
    "independent derivation not trained on the first result",
)
EXPECTED_MANDATORY_CONTROLS = tuple(MANDATORY_CONTROLS)

DEFINITION_CONTROL_KEYS = frozenset({
    "full_scientific_contract_schema_present",
    "candidate_interface_maps_complete_and_unique",
    "f3_gate_schema_complete_and_unique",
    "forbidden_preloads_explicit",
    "positive_null_adversarial_and_independent_controls_explicit",
    "strict_and_reflexive_order_conventions_distinguished",
    "correlation_computation_and_causality_distinguished",
    "first_candidate_class_and_falsifier_frozen",
    "closure_schema_exact_and_boolean",
    "all_candidate_and_downstream_outcomes_false",
})
FAIL_CLOSED_CONTROL_KEYS = frozenset({
    "complete_true_map_and_interface_eligible_but_not_promoted",
    "each_single_false_gate_blocks_eligibility",
    "missing_nonboolean_or_extra_gate_invalid",
    "missing_malformed_or_incomplete_candidate_map_invalid_or_ineligible",
})

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F3_INTERNAL_ORDER_CAUSALITY_CONTRACT_001",
    "CLAIM": (
        "Freeze a target-free, fail-closed interface that distinguishes atemporal internal "
        "order from genuine dynamic influence and permits W2_F3 to pass only after an "
        "equivalence-invariant causal order and forbidden-signal nontransmission are proved."
    ),
    "TYPE": "OUTCOME_NEUTRAL_ATOMIC_GATE_CONTRACT",
    "MODEL_VERSION": (
        "W2-C0 through w2_16; this version imports only the conditional atemporal F1/F2 "
        "endpoint and adds no state variable, time parameter, graph, dynamics, or semantics."
    ),
    "ASSUMPTIONS": (
        "The frozen W2-C0 contract is authoritative and w2_16 has validly established only "
        "conditional atemporal structural F1/F2 from its imported A=S+R state and law."
    ),
    "DOMAIN": (
        "Candidate-neutral. Each evaluator must predeclare its own open domain, branches, "
        "undefined points, intervention class, forbidden pairs, and perturbation class."
    ),
    "CONVENTIONS": (
        "Use a strict direct/effective relation x<y for direction: it must be irreflexive, "
        "asymmetric, transitive after closure, and acyclic. Its reflexive closure x<=y must be "
        "antisymmetric. A program-step index has no physical meaning at this gate."
    ),
    "FREEDOM_LEDGER": {
        "inherited_F2_state": {
            "source": "w2_16 conditional endpoint",
            "allowed_range": "A=S+R on its declared generic F2 domain",
            "scale": "one atemporal internal state",
            "complexity": 0,
        },
        "candidate_dynamic_primitives": {
            "source": "not supplied by this contract",
            "allowed_range": "must be frozen by a versioned candidate before evaluation",
            "scale": "candidate-specific",
            "complexity": "must be charged explicitly",
        },
        "intervention_and_signal_maps": {
            "source": "not supplied by this contract",
            "allowed_range": "must be derived from the candidate law",
            "scale": "candidate-specific",
            "complexity": "must be charged explicitly",
        },
        "equivalence": {
            "source": "inherited common O(3), enlarged only with proof",
            "allowed_range": "complete representation equivalence",
            "scale": "global description",
            "complexity": 0,
        },
        "external_time_metric_graph_or_target": {
            "source": "forbidden",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
        "data_fitted_freedoms": {
            "source": "none at F3",
            "allowed_range": 0,
            "scale": "data",
            "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md: W2_F3 atomic boundary",
        "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py: "
        "conditional atemporal F1/F2 only",
    ],
    "METHOD": (
        "Predeclare the candidate interface, exact causal axioms, no-transmission test, "
        "freedom ledger, controls, fail conditions, falsifier, and downstream scope before "
        "running a separate evaluator."
    ),
    "PASS_CONDITION": (
        "This contract passes only as a definition when every required map, gate, control, "
        "forbidden preload, closure flag, and fail-closed schema rule is explicit. A future F3 "
        "candidate is only schema-eligible if every required map is exactly registered with "
        "DERIVED status and every F3_GATE_KEYS entry is exactly boolean True; scientific "
        "promotion remains the separate evaluator's evidence-based decision."
    ),
    "FAIL_CONDITION": (
        "Any missing/nonboolean gate, missing candidate map, static correlation presented as "
        "influence, event cycle, two-way same-event reachability, forbidden transmission, "
        "ill-posed dynamics, convention dependence, target preload, tuned-only result, or "
        "failed predecessor keeps F3 false."
    ),
    "FALSIFIER": (
        "This contract is falsified if its screen promotes a partial or malformed report, or "
        "allows a causal PASS without a law-derived intervention response and exact "
        "forbidden-signal control."
    ),
    "RESIDUAL": "N/A: no candidate equation is evaluated in this definition artifact.",
    "ERROR_BOUND": "N/A: no approximation, numerical fit, or observation is used.",
    "VALIDITY_HEALTH": (
        "The interface is candidate-neutral. Every candidate must prove its applicable "
        "well-posedness, state-space closure, constraint preservation and dynamic health here. "
        "Conservation, continuum behavior and physical clock readout remain separate later gates."
    ),
    "BRANCHES": {
        "atemporal_state_filtration": "ADMISSIBLE_INTERMEDIATE_RESULT_NOT_F3_CAUSAL_PASS",
        "dynamic_intervention_response": "REQUIRED_FOR_F3",
        "static_correlation_or_ranking": "MANDATORY_NULL",
        "event_cycle_or_two_way_same_event_reachability": "F3_FAIL",
        "prewired_graph_clock_or_metric": "TARGET_LEAK_FAIL",
        "physical_time_and_clock_readout": "OPEN_LATER_BRIDGE",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "pre-spatial internal gate"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "no data or physical dynamics yet"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, fit, or target"},
    "IDENTIFIABILITY": (
        "A future candidate must distinguish directed intervention response from every "
        "equivalence-related algebraic transpose/skew-sign involution and from correlation-only "
        "models on a predeclared open domain. No candidate is identified here."
    ),
    "BENCHMARK": (
        "A three-event DAG is the logical positive control; empty, correlation-only, two-way "
        "same-event, cyclic, and prewired-target cases are mandatory negative controls. These are screen "
        "benchmarks, not imported physical models."
    ),
    "CLOSURE_FLAGS": {
        "F1_conditional_structural_predecessor_registered": True,
        "F2_conditional_structural_predecessor_registered": True,
        "F3_contract_defined": True,
        "F3_candidate_evaluated": False,
        "atemporal_internal_order_proved": False,
        "F3_internal_order_or_causality_proved": False,
        "physical_time_or_clock_readout_proved": False,
        "persistence_or_memory_proved": False,
        "F4_independent_additive_modes_proved": False,
        "foundation_to_effective_closed": False,
        "W2_M1_dimension_or_continuum_proved": False,
        "W2_M2_Lorentzian_metric_proved": False,
        "effective_action_or_matter_coupling_proved": False,
        "Einstein_GR_PN_or_PPN_bridge_proved": False,
        "observational_validation_proved": False,
    },
    "CROSSCHECK": (
        "A separate evaluator must use both graph/response diagnostics and an independent "
        "algebraic or intervention derivation; this file tests every malformed gate mutation."
    ),
    "PROVENANCE": {
        "date": "2026-07-22",
        "data": "none",
        "code_version": "w2_17 contract version 001",
        "hash": "N/A; source-control commit is the provenance record and no self-hash is embedded",
        "output": "JSON contract-validation report",
    },
    "FILES": [
        "CODES.md",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py",
        "RefG/work 2/w2_17_f3_internal_order_causality_contract.py",
        "RefG/work 2/w2_18_f3_static_endpoint_adjudication_gate.py",
    ],
    "REQUIRED_CANDIDATE_MAPS": REQUIRED_CANDIDATE_MAPS,
    "FORBIDDEN_PRELOADS": FORBIDDEN_PRELOADS,
    "MANDATORY_CONTROLS": MANDATORY_CONTROLS,
    "FIRST_EVALUATION_CLASS": {
        "name": "CURRENT_F2_STATIC_ENDPOINT_ONLY",
        "allowed_primitives": "Only w2_16 A,S,R,U, their inherited algebra, and common O(3)",
        "question": (
            "What invariant internal filtration can be derived without adding a "
            "transition, response, history, clock, graph, metric, or external orientation?"
        ),
        "causal_falsifier": (
            "If the algebraic transpose/skew-sign involution A<->A^T lies in the same accepted "
            "O(3) orbit and the inherited law "
            "defines no intervention, transition, signal, or no-transmission map, then causal "
            "promotion of this static-only class is rejected while noncausal algebraic results "
            "remain valid."
        ),
    },
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT
EXPECTED_CLOSURE_FLAGS = dict(CLAIM_CONTRACT["CLOSURE_FLAGS"])


def _all_true(value: Any) -> bool:
    if isinstance(value, dict):
        return bool(value) and all(_all_true(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return bool(value) and all(_all_true(item) for item in value)
    return value is True


def exact_true_map(value: Any, expected_keys: frozenset[str]) -> bool:
    return bool(
        isinstance(value, dict)
        and set(value) == expected_keys
        and all(item is True for item in value.values())
    )


def frozen_f3_gate_keys() -> frozenset[str]:
    """Independent literal registry used against mutable module/contract ledgers."""
    return frozenset({
        "same_chain_F1_F2_predecessors_valid",
        "state_owned_events_or_changes_derived",
        "target_free_transition_or_response_law_derived",
        "candidate_dynamics_health_and_state_space_closure_proved",
        "allowed_interventions_defined",
        "directed_intervention_response_proved",
        "correlation_and_static_ranking_excluded",
        "complete_equivalence_invariance_proved",
        "arrow_selected_by_law_not_labels_or_schedule",
        "nontrivial_direct_influence_on_predeclared_open_domain",
        "strict_relation_irreflexive_asymmetric_and_acyclic",
        "effective_order_transitive_and_reflexive_closure_antisymmetric",
        "forbidden_signal_nontransmission_proved",
        "computational_schedule_neutrality_proved",
        "null_reverse_and_target_leak_controls_pass",
        "perturbation_and_initial_condition_stability_proved",
        "independent_second_derivation_passes",
        "physical_time_metric_and_downstream_gates_remain_open",
    })


def frozen_required_candidate_maps() -> tuple[str, ...]:
    return (
        "state_space",
        "event_or_change_map",
        "complete_equivalence_action",
        "transition_or_response_law",
        "signal_support_or_update_composition",
        "allowed_interventions",
        "intervention_to_response_map",
        "direct_influence_relation",
        "transitive_effective_order",
        "forbidden_pairs",
        "no_transmission_test",
        "open_domain",
        "null_branches",
        "perturbation_class",
        "independent_crosscheck",
    )


def frozen_forbidden_preloads() -> tuple[str, ...]:
    return (
        "physical position, physical time, external clock, or 3+1 split",
        "lattice, locality graph, causal DAG, time layers, or event numbering",
        "Lorentzian metric, light cone, GR, Einstein equations, or PN/PPN target",
        "preferred basis, axis, orientation, labels, or state-external seed",
        "history, lag, memory, retarded kernel, or update arrow not derived from the law",
        "correlation, commutator sign, eigenvalue rank, or Krylov depth renamed causality",
        "algorithmic iteration or execution schedule renamed physical process order",
        "post-selection of the branch or convention that gives the desired arrow",
    )


def frozen_mandatory_controls() -> tuple[str, ...]:
    return (
        "known directed acyclic influence positive control",
        "frozen or nonresponsive null",
        "correlated but noninterventional null",
        "two-way reachability between the same event occurrences rejection",
        "directed-cycle rejection",
        "prewired target-DAG rejection",
        "basis, label, reflection, and reversal mutations",
        "execution-schedule permutation",
        "F2 nulls S=0, R=0, tau=0, tau=1, tuned branch, and singular normalization",
        "small-perturbation and allowed-initial-condition stability",
        "independent derivation not trained on the first result",
    )


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "F1_conditional_structural_predecessor_registered": True,
        "F2_conditional_structural_predecessor_registered": True,
        "F3_contract_defined": True,
        "F3_candidate_evaluated": False,
        "atemporal_internal_order_proved": False,
        "F3_internal_order_or_causality_proved": False,
        "physical_time_or_clock_readout_proved": False,
        "persistence_or_memory_proved": False,
        "F4_independent_additive_modes_proved": False,
        "foundation_to_effective_closed": False,
        "W2_M1_dimension_or_continuum_proved": False,
        "W2_M2_Lorentzian_metric_proved": False,
        "effective_action_or_matter_coupling_proved": False,
        "Einstein_GR_PN_or_PPN_bridge_proved": False,
        "observational_validation_proved": False,
    }


def frozen_first_evaluation_class() -> dict[str, str]:
    return {
        "name": "CURRENT_F2_STATIC_ENDPOINT_ONLY",
        "allowed_primitives": "Only w2_16 A,S,R,U, their inherited algebra, and common O(3)",
        "question": (
            "What invariant internal filtration can be derived without adding a transition, "
            "response, history, clock, graph, metric, or external orientation?"
        ),
        "causal_falsifier": (
            "If the algebraic transpose/skew-sign involution A<->A^T lies in the same accepted "
            "O(3) orbit and the inherited law defines no intervention, transition, signal, or "
            "no-transmission map, then causal promotion of this static-only class is rejected "
            "while noncausal algebraic results remain valid."
        ),
    }


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_safe(item) for item in value]
    return str(value)


def candidate_map_fixture(status: str = "DERIVED") -> dict[str, dict[str, str]]:
    """Build a schema fixture for logic tests, never candidate evidence."""
    if status not in CANDIDATE_MAP_STATUSES:
        raise ValueError(f"unsupported candidate-map status: {status}")
    return {
        key: {
            "status": status,
            "source": "LOGIC_TEST_FIXTURE_NOT_SCIENTIFIC_EVIDENCE",
            "definition": f"schema fixture for {key}",
        }
        for key in frozen_required_candidate_maps()
    }


def candidate_map_schema_valid(candidate_maps: Any) -> bool:
    if not isinstance(candidate_maps, dict) or set(candidate_maps) != set(
        frozen_required_candidate_maps()
    ):
        return False
    for entry in candidate_maps.values():
        if not isinstance(entry, dict) or set(entry) != CANDIDATE_MAP_ENTRY_KEYS:
            return False
        if entry["status"] not in CANDIDATE_MAP_STATUSES:
            return False
        if not isinstance(entry["source"], str) or not entry["source"].strip():
            return False
        if not isinstance(entry["definition"], str) or not entry["definition"].strip():
            return False
    return True


def candidate_screen(gates: Any, candidate_maps: Any = None) -> dict[str, bool]:
    """Fail closed: schema eligibility is not scientific promotion."""
    gate_schema_valid = bool(
        isinstance(gates, dict)
        and set(gates) == frozen_f3_gate_keys()
        and all(type(value) is bool for value in gates.values())
    )
    map_schema_valid = candidate_map_schema_valid(candidate_maps)
    maps_complete = bool(
        map_schema_valid
        and all(entry["status"] == "DERIVED" for entry in candidate_maps.values())
    )
    valid = bool(gate_schema_valid and map_schema_valid)
    return {
        "valid": valid,
        "eligible": bool(valid and maps_complete and all(gates.values())),
        "promoted": False,
    }


def definition_controls() -> dict[str, bool]:
    required_top_level = {
        "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
        "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD", "PASS_CONDITION",
        "FAIL_CONDITION", "FALSIFIER", "RESIDUAL", "ERROR_BOUND", "VALIDITY_HEALTH",
        "BRANCHES", "OBSERVABLE_MAP", "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY",
        "BENCHMARK", "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
        "REQUIRED_CANDIDATE_MAPS", "FORBIDDEN_PRELOADS", "MANDATORY_CONTROLS",
        "FIRST_EVALUATION_CLASS",
    }
    closure = CLAIM_CONTRACT["CLOSURE_FLAGS"]
    outcome_keys = {
        "F3_candidate_evaluated",
        "atemporal_internal_order_proved",
        "F3_internal_order_or_causality_proved",
        "physical_time_or_clock_readout_proved",
        "persistence_or_memory_proved",
        "F4_independent_additive_modes_proved",
        "foundation_to_effective_closed",
        "W2_M1_dimension_or_continuum_proved",
        "W2_M2_Lorentzian_metric_proved",
        "effective_action_or_matter_coupling_proved",
        "Einstein_GR_PN_or_PPN_bridge_proved",
        "observational_validation_proved",
    }
    return {
        "full_scientific_contract_schema_present": required_top_level <= set(CLAIM_CONTRACT),
        "candidate_interface_maps_complete_and_unique": (
            REQUIRED_CANDIDATE_MAPS == EXPECTED_REQUIRED_CANDIDATE_MAPS
            == frozen_required_candidate_maps()
            and tuple(CLAIM_CONTRACT.get("REQUIRED_CANDIDATE_MAPS", ()))
            == frozen_required_candidate_maps()
            and len(REQUIRED_CANDIDATE_MAPS) == len(set(REQUIRED_CANDIDATE_MAPS)) == 15
        ),
        "f3_gate_schema_complete_and_unique": (
            F3_GATE_KEYS == EXPECTED_F3_GATE_KEYS == frozen_f3_gate_keys()
            and len(F3_GATE_KEYS) == 18
        ),
        "forbidden_preloads_explicit": all((
            FORBIDDEN_PRELOADS == EXPECTED_FORBIDDEN_PRELOADS
            == frozen_forbidden_preloads(),
            tuple(CLAIM_CONTRACT.get("FORBIDDEN_PRELOADS", ()))
            == frozen_forbidden_preloads(),
            len(FORBIDDEN_PRELOADS) == 8,
        )),
        "positive_null_adversarial_and_independent_controls_explicit": (
            MANDATORY_CONTROLS == EXPECTED_MANDATORY_CONTROLS
            == frozen_mandatory_controls()
            and tuple(CLAIM_CONTRACT.get("MANDATORY_CONTROLS", ()))
            == frozen_mandatory_controls()
            and len(MANDATORY_CONTROLS) == 11
        ),
        "strict_and_reflexive_order_conventions_distinguished": all(
            token in CLAIM_CONTRACT["CONVENTIONS"]
            for token in ("irreflexive", "asymmetric", "transitive", "antisymmetric")
        ),
        "correlation_computation_and_causality_distinguished": all(
            token in CLAIM_CONTRACT["FAIL_CONDITION"]
            for token in ("static correlation", "convention dependence", "target preload")
        ),
        "first_candidate_class_and_falsifier_frozen": (
            CLAIM_CONTRACT.get("FIRST_EVALUATION_CLASS")
            == frozen_first_evaluation_class()
        ),
        "closure_schema_exact_and_boolean": (
            closure == EXPECTED_CLOSURE_FLAGS == frozen_closure_flags()
            and all(type(value) is bool for value in closure.values())
        ),
        "all_candidate_and_downstream_outcomes_false": all(
            closure[key] is False for key in outcome_keys
        ),
    }


def fail_closed_controls() -> dict[str, bool]:
    all_true = {key: True for key in frozen_f3_gate_keys()}
    complete_maps = candidate_map_fixture("DERIVED")
    baseline = candidate_screen(all_true, complete_maps)
    false_results = []
    malformed_results = []
    for key in frozen_f3_gate_keys():
        one_false = dict(all_true)
        one_false[key] = False
        false_results.append(candidate_screen(one_false, complete_maps))

        missing = dict(all_true)
        missing.pop(key)
        malformed_results.append(candidate_screen(missing, complete_maps))

        nonboolean = dict(all_true)
        nonboolean[key] = 1
        malformed_results.append(candidate_screen(nonboolean, complete_maps))

    extra = dict(all_true)
    extra["self_attested_pass"] = True
    malformed_results.append(candidate_screen(extra, complete_maps))

    missing_map = dict(complete_maps)
    missing_map.pop(next(iter(missing_map)))
    malformed_entry = {key: dict(value) for key, value in complete_maps.items()}
    malformed_entry[next(iter(malformed_entry))]["status"] = "SELF_ATTESTED_PASS"
    partial_maps = candidate_map_fixture("PARTIAL")
    return {
        "complete_true_map_and_interface_eligible_but_not_promoted": all((
            baseline["valid"], baseline["eligible"], not baseline["promoted"]
        )),
        "each_single_false_gate_blocks_eligibility": all(
            result["valid"] and not result["eligible"] and not result["promoted"]
            for result in false_results
        ),
        "missing_nonboolean_or_extra_gate_invalid": all(
            not result["valid"] and not result["eligible"] and not result["promoted"]
            for result in malformed_results
        ),
        "missing_malformed_or_incomplete_candidate_map_invalid_or_ineligible": all((
            not candidate_screen(all_true, missing_map)["valid"],
            not candidate_screen(all_true, malformed_entry)["valid"],
            candidate_screen(all_true, partial_maps)["valid"],
            not candidate_screen(all_true, partial_maps)["eligible"],
            not candidate_screen(all_true, partial_maps)["promoted"],
        )),
    }


def run() -> dict[str, Any]:
    controls = {
        "definition": definition_controls(),
        "fail_closed": fail_closed_controls(),
    }
    valid = bool(
        exact_true_map(controls["definition"], DEFINITION_CONTROL_KEYS)
        and exact_true_map(controls["fail_closed"], FAIL_CLOSED_CONTROL_KEYS)
    )
    return {
        "artifact": CLAIM_CONTRACT["CLAIM_ID"],
        "valid": valid,
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The F3 causal-candidate interface is defined and fail-closed. No candidate has "
            "been evaluated and no internal causal order, physical time, metric, or later gate "
            "is proved by this contract."
        ),
        "f3_gate_keys": sorted(frozen_f3_gate_keys()),
        "closure_flags": CLAIM_CONTRACT["CLOSURE_FLAGS"],
        "controls": controls,
    }


def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_CONTRACT.get("CLAIM_ID", "unknown"),
            "valid": False,
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(_json_safe(report), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
