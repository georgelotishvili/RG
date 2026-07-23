"""Authoritative F3a adjudication after the occurrence-lift lemma.

w2_27 limits the recurrence obstruction to a strict state-only clock.  w2_28
constructs a law-generated lifted history order for the supplied w2_25 flow.
Those are useful exact lemmas, but they do not complete the candidate interface
frozen by w2_23.  In particular, w2_25 still imports its carrier and law, most
same-chain physical maps and the full robustness map remain PARTIAL.  w2_28's
general stabilizer route now supplies an independent G4 crosscheck for the
scoped occurrence-order lemma, without promoting the incomplete chain.

This gate builds the complete versioned w2_23 candidate-map registry, applies
w2_23.candidate_screen directly, and records F3a_eligible=False.  No
conditional or physical F3a promotion is made.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any


CLAIM_ID = "W2_F3A_OCCURRENCE_ORDER_ADJUDICATION_001"
MODEL_VERSION = "W2-F3A-OCCURRENCE-ORDER-ADJUDICATION-v2.2-CANDIDATE-G4-FAIL-CLOSED"

REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

# Overlay only semantic status/source/definition.  required_for and depends_on
# are inherited verbatim from the authoritative w2_23 interface.
CANDIDATE_MAP_OVERLAY: dict[str, dict[str, str]] = {
    "carrier_state_domain": {
        "status": "PARTIAL",
        "source": "w2_25 imported finite A,V representation",
        "definition": "regular/coercive subset of T sl(3,R); foundation origin absent",
    },
    "self_relation_map": {
        "status": "DERIVED",
        "source": "w2_25 exact transpose split",
        "definition": "A maps to S,R and reconstructs exactly as A=S+R",
    },
    "complete_equivalence_action": {
        "status": "DERIVED",
        "source": "w2_25 declared common O(3) redundancy",
        "definition": "simultaneous conjugation on A,V; no spatial meaning",
    },
    "autonomous_transfer_law": {
        "status": "PARTIAL",
        "source": "w2_25 variational law on imported carrier and kinetic form",
        "definition": "smooth complete candidate flow; foundation law origin absent",
    },
    "transfer_composition": {
        "status": "DERIVED",
        "source": "w2_25 uniqueness plus w2_28 action-groupoid identity",
        "definition": "fixed-parametrization flow composition phi_t o phi_s=phi_(s+t)",
    },
    "undifferentiated_reference": {
        "status": "ABSENT",
        "source": "not established by w2_25 or w2_28",
        "definition": "the zero phase null is not proved to be a foundation reference",
    },
    "self_differentiation_witness": {
        "status": "PARTIAL",
        "source": "w2_25 conditional transpose-role witness",
        "definition": "representation-level F1 witness on imported A",
    },
    "state_owned_role_or_node_map": {
        "status": "PARTIAL",
        "source": "w2_25 transpose projections",
        "definition": "S,R are representation sectors, not derived physical nodes",
    },
    "common_carrier_ownership_map": {
        "status": "PARTIAL",
        "source": "w2_25 exact reconstruction A=S+R",
        "definition": "same-representation ownership only; physical kernel origin absent",
    },
    "irreducible_relational_report": {
        "status": "PARTIAL",
        "source": "w2_25 generic local quotient rank",
        "definition": "conditional joint invariants M3,M4; physical relation unproved",
    },
    "state_owned_change_or_occurrence_map": {
        "status": "PARTIAL",
        "source": "w2_25 process germ plus w2_28 history arrows",
        "definition": "law-generated mathematical occurrences; state-owned physical readout absent",
    },
    "intrinsic_process_line": {
        "status": "PARTIAL",
        "source": "w2_25 exact nonzero local quotient witness",
        "definition": "regular local representation line, not same-chain physical F3a",
    },
    "orientation_double_cover": {
        "status": "DERIVED",
        "source": "w2_25 reversal and w2_28 coherent orientation",
        "definition": "one exact global Z2 pair; statewise sign patches excluded",
    },
    "recurrence_occurrence_lift": {
        "status": "PARTIAL",
        "source": "w2_28 action-groupoid lifted-history lemma",
        "definition": "mathematical path order; no state-owned memory or physical occurrence readout",
    },
    "simultaneous_mode_inventory": {
        "status": "PARTIAL",
        "source": "w2_25 rank-eight channel and rank-two amplitude accounting",
        "definition": "representation accounting only; genuine law-derived physical modes unproved",
    },
    "mode_independence_readout": {
        "status": "PARTIAL",
        "source": "w2_25 local differential rank",
        "definition": "state-coordinate independence without physical conservation/readout",
    },
    "allowed_interventions": {
        "status": "ABSENT",
        "source": "not supplied",
        "definition": "no equivalence-invariant physical intervention class",
    },
    "direct_influence_relation": {
        "status": "ABSENT",
        "source": "not supplied",
        "definition": "no derived intervention-response relation",
    },
    "signal_support_composition": {
        "status": "ABSENT",
        "source": "not supplied",
        "definition": "no derived multi-occurrence signal support",
    },
    "forbidden_pair_domain": {
        "status": "ABSENT",
        "source": "not supplied",
        "definition": "no nonempty invariant forbidden-pair domain",
    },
    "nontransmission_test": {
        "status": "ABSENT",
        "source": "w2_25 full mixed law generically couples S,R",
        "definition": "no physical forbidden-pair zero-response result",
    },
    "open_domain_and_nulls": {
        "status": "PARTIAL",
        "source": "w2_25 coercive domain and zero-phase null",
        "definition": "candidate representation domain; full physical quotient domain absent",
    },
    "perturbation_class": {
        "status": "PARTIAL",
        "source": "w2_24 complete degree-four class and w2_25 coercive subdomain",
        "definition": "law-class audit without full F3a structural-stability proof",
    },
    "independent_crosscheck": {
        "status": "PARTIAL",
        "source": "w2_28 general stabilizer/homogeneous-orbit route",
        "definition": (
            "scoped G4 crosscheck of occurrence order via closed-subgroup classification, "
            "R/H orbit topology and universal cover; candidate-wide crosscheck remains open"
        ),
    },
}

EXPECTED_F3A_GATES: dict[str, bool] = {
    "same_chain_kernel_F1_F2_predecessors_valid": False,
    "state_owned_changes_or_occurrences_derived": False,
    "autonomous_target_free_transfer_law_derived": False,
    "nonzero_intrinsic_process_line_on_open_domain": True,
    "transfer_composition_and_occurrence_order_consistent": True,
    "positive_reparameterisation_gauge_proved": True,
    "law_selected_orientation_or_global_Z2_pair_proved": True,
    "global_orientation_choice_consistent": True,
    "statewise_sign_patching_excluded": True,
    "labels_and_execution_schedule_neutral": True,
    "recurrence_has_derived_occurrence_lift_or_is_absent": False,
    "two_way_order_of_same_occurrence_excluded": True,
    "perturbation_and_initial_state_stability_proved": False,
    "independent_second_derivation_passes": False,
    "clock_rate_spatial_causality_and_metric_remain_open": True,
}

BLOCKER_REGISTRY: dict[str, str] = {
    "same_chain_physical_kernel_origin": (
        "F0 origin is false, so conditional F1/F2 representation witnesses are not "
        "same-chain physical predecessors"
    ),
    "carrier_and_law_maps": (
        "carrier_state_domain and autonomous_transfer_law remain PARTIAL"
    ),
    "physical_occurrence_map": (
        "w2_28 supplies history order but not a DERIVED state-owned physical occurrence readout"
    ),
    "reference_and_relational_chain": (
        "undifferentiated_reference is ABSENT and F1/F2 ownership maps remain PARTIAL"
    ),
    "robustness": (
        "the complete F3a perturbation and initial-state stability requirement is unproved"
    ),
    "candidate_wide_G4_scope": (
        "the occurrence-order G4 route passes, but independent_crosscheck remains "
        "PARTIAL for the complete candidate chain"
    ),
}


def frozen_outcomes() -> dict[str, bool]:
    return {
        "law_generated_lifted_history_order_lemma_proved": True,
        "w2_23_candidate_screen_schema_valid": True,
        "w2_23_F3a_eligible": False,
        "conditional_structural_F3a_promoted": False,
        "full_physical_F3a_promoted": False,
        "same_chain_physical_kernel_origin_proved": False,
        "G4_occurrence_order_independent_check_passed": True,
        "candidate_wide_G4_independent_check_passed": False,
        "physical_time_clock_or_memory_proved": False,
        "F4_may_be_audited_on_its_independent_branch": True,
        "F4_simultaneous_physical_modes_proved": False,
        "F3b_causal_separability_nontransmission_proved": False,
        "space_metric_GR_or_observation_proved": False,
    }


EXPECTED_OUTCOMES = frozen_outcomes()


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "lifted_history_order_representation_lemma_closed": True,
        "conditional_F3a_structural_representation_closed": False,
        "F0_common_resonant_kernel_origin_proved": False,
        "F1_self_differentiation_on_derived_kernel_proved": False,
        "F2_operational_relations_on_derived_kernel_proved": False,
        "F3a_intrinsic_process_orientation_proved": False,
        "physical_time_clock_memory_or_thermodynamic_arrow_proved": False,
        "F4_simultaneous_physical_modes_proved": False,
        "F3b_causal_separability_nontransmission_proved": False,
        "dimension_continuum_metric_or_GR_proved": False,
        "observational_validation_proved": False,
    }


EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "The w2_25 flow plus the w2_28 occurrence lift proves an exact "
        "representation-level lifted-history order lemma. The complete versioned "
        "candidate interface fails the authoritative w2_23 F3a eligibility screen "
        "because same-chain physical origin, several required DERIVED maps and "
        "full robustness are missing. The scoped occurrence-order G4 crosscheck passes."
    ),
    "TYPE": "EXACT_OCCURRENCE_ORDER_LEMMA_AND_F3A_INELIGIBILITY_ADJUDICATION",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "w2_23 is the authoritative eligibility contract. w2_25 remains an "
        "imported conditional A,V representation. w2_27 and w2_28 supply only "
        "their declared scoped recurrence and occurrence-order lemmas."
    ),
    "DOMAIN": (
        "The positive lemma holds on regular histories of the supplied w2_25 "
        "flow. F3a eligibility is evaluated on the complete w2_23 interface."
    ),
    "CONVENTIONS": (
        "A mathematical lifted-history order is distinct from a state-owned "
        "physical occurrence map, calibrated time and full F3a closure. PARTIAL "
        "and ABSENT never count as DERIVED. The scoped occurrence-order G4 result "
        "does not become a candidate-wide independent crosscheck."
    ),
    "FREEDOM_LEDGER": {
        "candidate_representation": {
            "source": "w2_25 import",
            "allowed_range": "A,V in T sl(3,R), n=3, common O(3)",
            "scale": "whole conditional candidate",
            "complexity": "charged in w2_25, not foundation-derived",
        },
        "occurrence_lift": {
            "source": "w2_28 supplied-flow construction",
            "allowed_range": "mathematical history order only",
            "scale": "regular histories",
            "complexity": 0,
        },
        "status_changes": {
            "source": "structured predecessor evidence only",
            "allowed_range": "no hand promotion from PARTIAL/ABSENT to DERIVED",
            "scale": "all candidate maps",
            "complexity": 0,
        },
        "data_or_target": {
            "source": "none",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_23_common_resonant_kernel_contract.py: authoritative candidate_screen",
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py: conditional representation maps",
        "RefG/work 2/w2_27_f3a_recurrence_scope_no_go_gate.py: scoped state-clock no-go",
        "RefG/work 2/w2_28_f3a_flow_groupoid_occurrence_lift_gate.py: occurrence-order lemma",
        "CODES.md G4_INDEPENDENT_CHECK: independent derivation requirement",
    ],
    "METHOD": (
        "Overlay every w2_23 interface entry with versioned w2_25/w2_28 status, "
        "build the exact F3a gate map, and call w2_23.candidate_screen directly. "
        "Enumerate all non-DERIVED required maps and all false F3a gates."
    ),
    "PASS_CONDITION": (
        "The adjudication passes only when predecessors are valid, the complete "
        "map schema is exact, w2_23.candidate_screen is valid but returns "
        "F3a_eligible=False, every blocker is exposed, and all F3a physical and "
        "conditional closure flags remain false. The occurrence-order G4 result "
        "must be true while candidate-wide G4 remains false."
    ),
    "FAIL_CONDITION": (
        "Any omitted interface map, hand-upgraded status, hidden false gate, "
        "bypassed candidate_screen, overstated G4 scope, F3a eligibility or "
        "promotion, malformed evidence, or frozen-payload mutation invalidates "
        "the adjudication."
    ),
    "FALSIFIER": (
        "This ineligibility result is superseded by a new versioned candidate "
        "that makes every F3A_REQUIRED_MAP DERIVED, passes every F3A_GATE_KEY, "
        "and is accepted by the "
        "unchanged w2_23 candidate_screen."
    ),
    "RESIDUAL": (
        "Inherited zero algebraic residuals for the scoped history-order lemma; "
        "F3a blockers are categorical statuses, not numerical residuals."
    ),
    "ERROR_BOUND": "No numerical approximation, fit or tolerance is used.",
    "VALIDITY_HEALTH": (
        "The occurrence-order lemma retains the w2_28 regular-flow scope. F3a "
        "ineligibility remains valid until every listed map and gate is closed "
        "in a new versioned candidate."
    ),
    "BRANCHES": {
        "lifted_history_order": "EXACT_REPRESENTATION_LEMMA",
        "authoritative_F3a_screen": "VALID_BUT_INELIGIBLE",
        "same_chain_kernel_origin": "OPEN_BLOCKER",
        "G4_occurrence_order_crosscheck": "SCOPED_PASS_NO_PROMOTION",
        "candidate_wide_G4_crosscheck": "PARTIAL_OPEN",
        "conditional_or_physical_F3a": "NOT_PROMOTED",
        "F4_independent_branch": "MAY_BE_AUDITED_SEPARATELY",
        "F3b_space_metric_GR_observation": "OPEN",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "pre-spatial structural adjudication"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "no physical time or observable"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, target, fit or validation"},
    "IDENTIFIABILITY": (
        "The registry distinguishes exact mathematical maps, conditional partial "
        "maps, absent maps and physical closure without conflating their status."
    ),
    "BENCHMARK": (
        "The unchanged w2_23 candidate_screen is the decision benchmark. Its "
        "synthetic all-DERIVED control must be eligible while this candidate is not."
    ),
    "CLOSURE_FLAGS": frozen_closure_flags(),
    "CROSSCHECK": (
        "Compare map-derived blockers with gate-derived blockers and exercise the "
        "authoritative screen on current, map-complete-only, gate-complete-only "
        "and fully synthetic reports."
    ),
    "PROVENANCE": {
        "date": "2026-07-23",
        "data": "none",
        "code_version": "w2_29 gate v2.2 candidate-wide G4 fail-closed",
        "dependency_policy": "structured maps and direct authoritative screen",
    },
    "FILES": [
        "RefG/work 2/w2_29_f3a_occurrence_order_adjudication_gate.py",
        "RefG/work 2/w2_23_common_resonant_kernel_contract.py",
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py",
        "RefG/work 2/w2_27_f3a_recurrence_scope_no_go_gate.py",
        "RefG/work 2/w2_28_f3a_flow_groupoid_occurrence_lift_gate.py",
    ],
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def _canonical_sha256(payload: Any) -> str:
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest().upper()


EXPECTED_CANDIDATE_MAP_OVERLAY_SHA256 = (
    "58FD506EDF867CDD4D35B50C21E53B071A378803D0A93C8A17BC866A091B7AD2"
)
EXPECTED_F3A_GATES_SHA256 = (
    "16816ED0386808327943CB0DF1B26C5BC0B7A0F764E4962618904A5ACE5257C2"
)
EXPECTED_BLOCKER_REGISTRY_SHA256 = (
    "693C07A275AD9493E38E83D67CA4497347B3BB190FE150C99F407E284D1416C2"
)
EXPECTED_VERSIONED_CANDIDATE_MAPS_SHA256 = (
    "4670692FDD9782206A931D0846BBB1B1CF650EFDEE3148567458B68499B076F9"
)
EXPECTED_SCIENTIFIC_CONTRACT_SHA256 = (
    "8283A9AEBF78CCE7A2609D3CAC500CD08AA2A105E397ACFFCD312EACB7375F76"
)


def _load_sibling(filename: str, module_name: str) -> ModuleType:
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _exact_bool_map(actual: Any, keys: frozenset[str]) -> bool:
    return (
        isinstance(actual, dict)
        and set(actual) == set(keys)
        and all(type(value) is bool for value in actual.values())
    )


def build_versioned_candidate_maps(w223: ModuleType) -> dict[str, dict[str, Any]]:
    candidate_maps = deepcopy(w223.CANDIDATE_INTERFACE)
    if set(CANDIDATE_MAP_OVERLAY) != set(w223.REQUIRED_CANDIDATE_MAPS):
        return {}
    for name in w223.REQUIRED_CANDIDATE_MAPS:
        candidate_maps[name].update(CANDIDATE_MAP_OVERLAY[name])
    return candidate_maps


def dependency_reports() -> tuple[dict[str, bool], dict[str, Any]]:
    w223 = _load_sibling(
        "w2_23_common_resonant_kernel_contract.py", "w2_29_dep_w223"
    )
    w225 = _load_sibling(
        "w2_25_joint_common_kernel_candidate_gate.py", "w2_29_dep_w225"
    )
    w227 = _load_sibling(
        "w2_27_f3a_recurrence_scope_no_go_gate.py", "w2_29_dep_w227"
    )
    w228 = _load_sibling(
        "w2_28_f3a_flow_groupoid_occurrence_lift_gate.py", "w2_29_dep_w228"
    )
    report25, report27, report28 = w225.run(), w227.run(), w228.run()
    shared_statuses_exact = all(
        CANDIDATE_MAP_OVERLAY[name]["status"] == entry["status"]
        for name, entry in w225.CANDIDATE_MAPS.items()
        if name != "recurrence_occurrence_lift"
    )
    controls = {
        "w2_23_authoritative_contract_exact": all((
            w223.CLAIM_ID == "W2_F0_COMMON_RESONANT_KERNEL_CONTRACT_001",
            w223._canonical_sha256(w223.CLAIM_CONTRACT)
            == w223.EXPECTED_SCIENTIFIC_CONTRACT_SHA256,
        )),
        "w2_25_valid_and_physical_origin_false": all((
            report25["valid"] is True,
            report25["outcomes"]["foundation_common_kernel_origin_proved"] is False,
            report25["physical_closure_flags"]["F3a_intrinsic_process_orientation_proved"] is False,
        )),
        "w2_27_valid_scoped_no_go": all((
            report27["valid"] is True,
            report27["closure_flags"]["law_derived_occurrence_lift_proved"] is False,
        )),
        "w2_28_valid_occurrence_order_without_physical_readout": all((
            report28["valid"] is True,
            report28["outcomes"]["conditional_w2_25_occurrence_lift_available"] is True,
            report28["outcomes"][
                "G4_occurrence_order_independent_derivation_passed"
            ] is True,
            report28["outcomes"]["candidate_wide_G4_independent_check_passed"] is False,
            report28["outcomes"]["formal_proof_assistant_certificate_produced"] is False,
            report28["outcomes"]["physical_occurrence_ontology_proved"] is False,
        )),
        "w2_25_map_statuses_preserved_and_w2_28_lift_only_partial": all((
            shared_statuses_exact,
            w225.CANDIDATE_MAPS["recurrence_occurrence_lift"]["status"] == "ABSENT",
            CANDIDATE_MAP_OVERLAY["recurrence_occurrence_lift"]["status"] == "PARTIAL",
            report28["outcomes"]["conditional_w2_25_occurrence_lift_available"] is True,
            report28["outcomes"]["physical_occurrence_ontology_proved"] is False,
        )),
    }
    return controls, {
        "w223": w223, "w225_module": w225,
        "w225": report25, "w227": report27, "w228": report28,
    }


def build_f3a_gates(reports: dict[str, Any], maps: dict[str, dict[str, Any]]) -> dict[str, bool]:
    r25, r28 = reports["w225"], reports["w228"]
    p25 = r25["controls"]["process"]
    h25 = r25["controls"]["health"]
    g28 = r28["controls"]["action_groupoid"]
    p28 = r28["controls"]["periodic_lift"]
    o28 = r28["controls"]["orientation_and_neutrality"]
    return {
        "same_chain_kernel_F1_F2_predecessors_valid": all((
            r25["outcomes"]["foundation_common_kernel_origin_proved"],
            r25["physical_closure_flags"]["F1_self_differentiation_proved_on_derived_kernel"],
            r25["physical_closure_flags"]["F2_operational_relations_proved_on_derived_kernel"],
        )),
        "state_owned_changes_or_occurrences_derived": (
            maps["state_owned_change_or_occurrence_map"]["status"] == "DERIVED"
        ),
        "autonomous_target_free_transfer_law_derived": (
            maps["autonomous_transfer_law"]["status"] == "DERIVED"
        ),
        "nonzero_intrinsic_process_line_on_open_domain": all((
            p25["nonzero_local_intrinsic_process_line_exact_witness"],
            h25["full_polynomial_vector_field_is_smooth"],
        )),
        "transfer_composition_and_occurrence_order_consistent": all((
            maps["transfer_composition"]["status"] == "DERIVED",
            g28["flow_composition_exact"], p28["lifted_order_is_antisymmetric"],
        )),
        "positive_reparameterisation_gauge_proved": all((
            o28["strict_history_recoordinate_has_positive_derivative"],
            o28["strict_history_recoordinate_preserves_order"],
        )),
        "law_selected_orientation_or_global_Z2_pair_proved": all((
            maps["orientation_double_cover"]["status"] == "DERIVED",
            p25["global_Z2_history_reversal_exact"],
        )),
        "global_orientation_choice_consistent": o28[
            "connected_discrete_orientation_has_exactly_two_coherent_assignments"
        ],
        "statewise_sign_patching_excluded": o28["statewise_sign_patch_fails_coherence"],
        "labels_and_execution_schedule_neutral": all((
            g28["arrows_are_law_generated_not_external_event_numbers"],
            o28["solver_subdivision_neutral_exact"],
        )),
        "recurrence_has_derived_occurrence_lift_or_is_absent": (
            maps["recurrence_occurrence_lift"]["status"] == "DERIVED"
        ),
        "two_way_order_of_same_occurrence_excluded": all((
            p28["lifted_order_is_antisymmetric"],
            p28["state_return_does_not_identify_lifted_occurrence"],
        )),
        "perturbation_and_initial_state_stability_proved": (
            maps["perturbation_class"]["status"] == "DERIVED"
        ),
        "independent_second_derivation_passes": (
            maps["independent_crosscheck"]["status"] == "DERIVED"
            and r28["outcomes"]["candidate_wide_G4_independent_check_passed"] is True
        ),
        "clock_rate_spatial_causality_and_metric_remain_open": all((
            r28["outcomes"]["physical_time_or_clock_proved"] is False,
            r25["outcomes"]["F3b_causal_separability_nontransmission_proved"] is False,
            r25["outcomes"]["physical_space_time_metric_or_GR_proved"] is False,
        )),
    }


def adjudication_controls(
    reports: dict[str, Any], maps: dict[str, dict[str, Any]], gates: dict[str, bool]
) -> tuple[dict[str, bool], dict[str, Any]]:
    w223 = reports["w223"]
    f3b_gates = {key: False for key in w223.F3B_GATE_KEYS}
    screen = w223.candidate_screen(maps, gates, False, f3b_gates, False)
    map_blockers = sorted(
        name for name in w223.F3A_REQUIRED_MAPS
        if maps[name]["status"] != "DERIVED"
    )
    gate_blockers = sorted(name for name, value in gates.items() if value is False)
    controls = {
        "complete_candidate_map_schema_valid": w223._candidate_interface_schema_valid(maps),
        "authoritative_screen_valid": screen["valid"] is True,
        "authoritative_F3a_ineligible": screen["F3a_eligible"] is False,
        "authoritative_F3b_ineligible": screen["F3b_eligible"] is False,
        "authoritative_screen_never_promotes": screen["promoted"] is False,
        "required_map_blocker_set_nonempty": len(map_blockers) > 0,
        "false_F3a_gate_blocker_set_nonempty": len(gate_blockers) > 0,
        "same_chain_origin_blocker_explicit": (
            "same_chain_kernel_F1_F2_predecessors_valid" in gate_blockers
        ),
        "scoped_G4_crosscheck_passes_without_candidate_wide_promotion": all((
            "independent_crosscheck" in map_blockers,
            "independent_second_derivation_passes" in gate_blockers,
            maps["independent_crosscheck"]["status"] == "PARTIAL",
            reports["w228"]["outcomes"][
                "G4_occurrence_order_independent_derivation_passed"
            ] is True,
            reports["w228"]["outcomes"][
                "candidate_wide_G4_independent_check_passed"
            ] is False,
        )),
        "occurrence_lift_not_gamed_to_DERIVED": (
            maps["recurrence_occurrence_lift"]["status"] == "PARTIAL"
        ),
        "only_scoped_history_order_lemma_closed": all((
            reports["w228"]["outcomes"][
                "conditional_w2_25_occurrence_lift_available"
            ] is True,
            reports["w228"]["outcomes"]["physical_occurrence_ontology_proved"] is False,
            EXPECTED_CLOSURE_FLAGS["lifted_history_order_representation_lemma_closed"] is True,
            EXPECTED_CLOSURE_FLAGS["conditional_F3a_structural_representation_closed"] is False,
        )),
    }
    diagnostics = {
        "authoritative_screen": screen,
        "required_map_blockers": map_blockers,
        "false_F3a_gate_blockers": gate_blockers,
        "candidate_map_statuses": {name: entry["status"] for name, entry in maps.items()},
    }
    return controls, diagnostics


def fail_closed_controls(
    w223: ModuleType, maps: dict[str, dict[str, Any]], gates: dict[str, bool]
) -> dict[str, bool]:
    f3b_false = {key: False for key in w223.F3B_GATE_KEYS}
    all_maps = deepcopy(maps)
    for entry in all_maps.values():
        entry["status"] = "DERIVED"
    all_gates = {key: True for key in w223.F3A_GATE_KEYS}

    current = w223.candidate_screen(maps, gates, False, f3b_false, False)
    maps_only = w223.candidate_screen(all_maps, gates, False, f3b_false, False)
    gates_only = w223.candidate_screen(maps, all_gates, False, f3b_false, False)
    synthetic = w223.candidate_screen(all_maps, all_gates, False, f3b_false, False)

    missing = deepcopy(maps)
    missing.pop(w223.REQUIRED_CANDIDATE_MAPS[0])
    extra = deepcopy(maps)
    extra["external_clock"] = deepcopy(next(iter(maps.values())))
    overlay_mutation = deepcopy(CANDIDATE_MAP_OVERLAY)
    overlay_mutation["independent_crosscheck"]["status"] = "DERIVED"
    gates_mutation = deepcopy(EXPECTED_F3A_GATES)
    gates_mutation["independent_second_derivation_passes"] = True
    blockers_mutation = deepcopy(BLOCKER_REGISTRY)
    blockers_mutation.pop("robustness")
    contract_mutation = deepcopy(CLAIM_CONTRACT)
    contract_mutation["CLOSURE_FLAGS"]["conditional_F3a_structural_representation_closed"] = True
    return {
        "current_candidate_valid_but_ineligible": all((
            current["valid"], not current["F3a_eligible"], not current["promoted"],
        )),
        "all_maps_derived_but_false_gates_still_ineligible": (
            maps_only["valid"] and not maps_only["F3a_eligible"]
        ),
        "all_gates_true_but_incomplete_maps_still_ineligible": (
            gates_only["valid"] and not gates_only["F3a_eligible"]
        ),
        "fully_synthetic_control_eligible_but_never_promoted": all((
            synthetic["valid"], synthetic["F3a_eligible"], not synthetic["promoted"],
        )),
        "missing_and_extra_maps_fail_screen_schema": all((
            not w223.candidate_screen(missing, gates, False, f3b_false, False)["valid"],
            not w223.candidate_screen(extra, gates, False, f3b_false, False)["valid"],
        )),
        "overlay_mutation_detected": (
            _canonical_sha256(overlay_mutation) != EXPECTED_CANDIDATE_MAP_OVERLAY_SHA256
        ),
        "gate_mutation_detected": (
            _canonical_sha256(gates_mutation) != EXPECTED_F3A_GATES_SHA256
        ),
        "blocker_mutation_detected": (
            _canonical_sha256(blockers_mutation) != EXPECTED_BLOCKER_REGISTRY_SHA256
        ),
        "candidate_map_mutation_detected": (
            _canonical_sha256(all_maps) != EXPECTED_VERSIONED_CANDIDATE_MAPS_SHA256
        ),
        "scientific_contract_mutation_detected": (
            _canonical_sha256(contract_mutation) != EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        ),
    }


def definition_controls(maps: dict[str, dict[str, Any]], w223: ModuleType) -> dict[str, bool]:
    return {
        "scientific_contract_schema_exact": set(CLAIM_CONTRACT) == set(REQUIRED_SCIENTIFIC_FIELDS),
        "claim_identity_model_and_type_exact": all((
            CLAIM_CONTRACT["CLAIM_ID"] == CLAIM_ID,
            CLAIM_CONTRACT["MODEL_VERSION"] == MODEL_VERSION,
            CLAIM_CONTRACT["TYPE"]
            == "EXACT_OCCURRENCE_ORDER_LEMMA_AND_F3A_INELIGIBILITY_ADJUDICATION",
        )),
        "candidate_map_overlay_hash_exact": (
            _canonical_sha256(CANDIDATE_MAP_OVERLAY)
            == EXPECTED_CANDIDATE_MAP_OVERLAY_SHA256
        ),
        "F3a_gate_hash_exact": (
            _canonical_sha256(EXPECTED_F3A_GATES) == EXPECTED_F3A_GATES_SHA256
        ),
        "blocker_registry_hash_exact": (
            _canonical_sha256(BLOCKER_REGISTRY) == EXPECTED_BLOCKER_REGISTRY_SHA256
        ),
        "versioned_candidate_maps_hash_exact": (
            _canonical_sha256(maps) == EXPECTED_VERSIONED_CANDIDATE_MAPS_SHA256
        ),
        "scientific_contract_hash_exact": (
            _canonical_sha256(CLAIM_CONTRACT) == EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        ),
        "candidate_map_order_and_schema_exact": all((
            tuple(maps) == w223.REQUIRED_CANDIDATE_MAPS,
            w223._candidate_interface_schema_valid(maps),
        )),
        "outcome_and_closure_ledgers_exact": all((
            frozen_outcomes() == EXPECTED_OUTCOMES,
            frozen_closure_flags() == EXPECTED_CLOSURE_FLAGS,
            CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS,
        )),
    }


def run() -> dict[str, Any]:
    dependency, reports = dependency_reports()
    w223 = reports["w223"]
    maps = build_versioned_candidate_maps(w223)
    gates = build_f3a_gates(reports, maps)
    adjudication, diagnostics = adjudication_controls(reports, maps, gates)
    fail_closed = fail_closed_controls(w223, maps, gates)
    definition = definition_controls(maps, w223)
    valid = all((
        all(dependency.values()),
        _exact_bool_map(gates, w223.F3A_GATE_KEYS),
        gates == EXPECTED_F3A_GATES,
        all(adjudication.values()), all(fail_closed.values()), all(definition.values()),
        diagnostics["authoritative_screen"]["F3a_eligible"] is False,
    ))
    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": bool(valid),
        "candidate_status": (
            "LIFTED_HISTORY_ORDER_LEMMA_PASS__AUTHORITATIVE_F3A_INELIGIBLE"
            if valid else "INVALID_NO_PROMOTION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The lifted-history order is an exact representation lemma, but F3a "
            "is not eligible. The authoritative w2_23 screen rejects closure "
            "because the physical same-chain kernel/origin is unproved, required "
            "maps remain PARTIAL or ABSENT and robustness is incomplete. The "
            "independent general-orbit G4 check passes for the scoped occurrence-order "
            "lemma; candidate-wide G4 remains false and no conditional or physical "
            "F3a status is promoted."
        ),
        "outcomes": frozen_outcomes(),
        "closure_flags": frozen_closure_flags(),
        "dependency_controls": dependency,
        "F3a_gates": gates,
        "blocker_registry": BLOCKER_REGISTRY,
        "adjudication_controls": adjudication,
        "diagnostics": diagnostics,
        "controls": {"definition": definition, "fail_closed": fail_closed},
        "next_gate": (
            "F4 may be audited on its independent branch; F3a remains open until "
            "the complete candidate maps, same-chain origin and robustness close"
        ),
        "hashes": {
            "candidate_map_overlay": _canonical_sha256(CANDIDATE_MAP_OVERLAY),
            "F3a_gates": _canonical_sha256(EXPECTED_F3A_GATES),
            "blocker_registry": _canonical_sha256(BLOCKER_REGISTRY),
            "versioned_candidate_maps": _canonical_sha256(maps),
            "scientific_contract": _canonical_sha256(CLAIM_CONTRACT),
        },
    }


def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_ID,
            "model_version": MODEL_VERSION,
            "valid": False,
            "candidate_status": "INVALID_NO_PROMOTION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
