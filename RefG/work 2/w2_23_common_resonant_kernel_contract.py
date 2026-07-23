"""Outcome-neutral contract for the revised Work-2 foundation route.

The smallest admissible starting point is one ontological identity represented
by one self-relation carrier together with one autonomous, target-free transfer
law.  The law is structure carried by the one identity, not a second substance.
A literal singleton with no nontrivial state/relation space and no law remains
inside the already proved singleton no-go boundary.

This contract introduces no candidate and proves no physical result.  It
separates intrinsic process orientation (F3a) from causal separability and
nontransmission (F3b).  A coherent global reversal is allowed at F3a; local or
statewise sign patching and an execution schedule are not.  F3b can be tested
only after F4 has supplied simultaneous, independently accountable modes.

The older w2_09, w2_16 and w2_22 artifacts are imported only to verify their
identities and conditional ceilings.  Their representation-specific results do
not supply the new carrier, transfer law, nodes, process, causal support, space,
metric or gravity.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any


CLAIM_ID = "W2_F0_COMMON_RESONANT_KERNEL_CONTRACT_001"
MODEL_VERSION = "W2-C0-v1.1-PROPOSED-COMMON-RESONANT-KERNEL-CONTRACT-v1.0"

REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

INTERFACE_ENTRY_KEYS = frozenset({
    "status", "source", "definition", "required_for", "depends_on",
})
INTERFACE_STATUSES = frozenset({
    "UNSUPPLIED", "DERIVED", "PARTIAL", "ABSENT", "NOT_APPLICABLE",
})

REQUIRED_CANDIDATE_MAPS = (
    "carrier_state_domain",
    "self_relation_map",
    "complete_equivalence_action",
    "autonomous_transfer_law",
    "transfer_composition",
    "undifferentiated_reference",
    "self_differentiation_witness",
    "state_owned_role_or_node_map",
    "common_carrier_ownership_map",
    "irreducible_relational_report",
    "state_owned_change_or_occurrence_map",
    "intrinsic_process_line",
    "orientation_double_cover",
    "recurrence_occurrence_lift",
    "simultaneous_mode_inventory",
    "mode_independence_readout",
    "allowed_interventions",
    "direct_influence_relation",
    "signal_support_composition",
    "forbidden_pair_domain",
    "nontransmission_test",
    "open_domain_and_nulls",
    "perturbation_class",
    "independent_crosscheck",
)

F3A_GATE_KEYS = frozenset({
    "same_chain_kernel_F1_F2_predecessors_valid",
    "state_owned_changes_or_occurrences_derived",
    "autonomous_target_free_transfer_law_derived",
    "nonzero_intrinsic_process_line_on_open_domain",
    "transfer_composition_and_occurrence_order_consistent",
    "positive_reparameterisation_gauge_proved",
    "law_selected_orientation_or_global_Z2_pair_proved",
    "global_orientation_choice_consistent",
    "statewise_sign_patching_excluded",
    "labels_and_execution_schedule_neutral",
    "recurrence_has_derived_occurrence_lift_or_is_absent",
    "two_way_order_of_same_occurrence_excluded",
    "perturbation_and_initial_state_stability_proved",
    "independent_second_derivation_passes",
    "clock_rate_spatial_causality_and_metric_remain_open",
})

F3B_GATE_KEYS = frozenset({
    "F3a_intrinsic_process_orientation_valid",
    "F4_simultaneous_modes_valid",
    "state_owned_mode_occurrences_derived",
    "nonpreloaded_signal_support_derived",
    "allowed_interventions_defined",
    "direct_influence_relation_derived",
    "nonempty_invariant_forbidden_pair_domain_derived",
    "signal_composition_law_derived",
    "forbidden_pair_nontransmission_proved",
    "common_carrier_interaction_not_mistaken_for_independence",
    "labels_schedule_and_global_reversal_neutral",
    "null_boundary_and_target_leak_controls_pass",
    "perturbation_stability_proved",
    "independent_second_derivation_passes",
    "continuum_light_cone_metric_and_GR_remain_open",
})

F3A_REQUIRED_MAPS = frozenset({
    "carrier_state_domain",
    "self_relation_map",
    "complete_equivalence_action",
    "autonomous_transfer_law",
    "transfer_composition",
    "undifferentiated_reference",
    "self_differentiation_witness",
    "state_owned_role_or_node_map",
    "common_carrier_ownership_map",
    "irreducible_relational_report",
    "state_owned_change_or_occurrence_map",
    "intrinsic_process_line",
    "orientation_double_cover",
    "recurrence_occurrence_lift",
    "open_domain_and_nulls",
    "perturbation_class",
    "independent_crosscheck",
})

F3B_REQUIRED_MAPS = frozenset(F3A_REQUIRED_MAPS).union({
    "simultaneous_mode_inventory",
    "mode_independence_readout",
    "allowed_interventions",
    "direct_influence_relation",
    "signal_support_composition",
    "forbidden_pair_domain",
    "nontransmission_test",
})

FORBIDDEN_PRELOADS = (
    "a strict singleton state space with a no-law update renamed self-differentiation",
    "separately imported nodes, roles, channels, particles or mode labels",
    "physical position, spatial coordinate, clock time, external clock or 3+1 split",
    "prewired adjacency graph, causal DAG, update layers or event numbering",
    "a fixed internal dimension, including dimension 3, selected for the desired output",
    "O(3) or another representation group imported as physical space or isotropy",
    "a preferred basis, axis, orientation, branch, projector or target relation",
    "a Lorentzian metric, light cone, manifold, volume form or continuum",
    "Einstein equations, Einstein-Hilbert action, GR, PN or PPN coefficients",
    "a computational iteration or execution schedule renamed physical process",
    "a state-dependent sign choice patched after inspecting the desired order",
    "observational data, fitted constants or target answers at this pre-spatial gate",
)

PRIMITIVE_POLICY: dict[str, Any] = {
    "ontological_identity_count": 1,
    "minimal_mathematical_representation": (
        "one self-relation carrier with a nontrivial candidate state/relation domain"
    ),
    "law_requirement": (
        "one autonomous target-free transfer law acting on that same carrier"
    ),
    "law_ontology": (
        "the transfer law is structure of the one identity, not a second carrier or substance"
    ),
    "strict_singleton_boundary": (
        "a literal one-state closed singleton with no nontrivial relation domain and no law "
        "cannot be promoted"
    ),
    "irreducibility_duty": (
        "a candidate must prove that apparent components are state-derived roles of the one "
        "carrier rather than hidden independent primitives"
    ),
    "target_free_duty": (
        "the carrier, law, equivalence, branch and perturbation class are frozen before outcomes"
    ),
    "imported_physical_structures": {
        "nodes": False,
        "space": False,
        "clock_time": False,
        "graph": False,
        "fixed_dimension": False,
        "O3": False,
        "metric": False,
        "GR": False,
    },
}

F3A_ORIENTATION_POLICY: dict[str, Any] = {
    "object": (
        "an equivalence-invariant intrinsic process line or oriented semigroup on the derived "
        "quotient/occurrence domain"
    ),
    "global_reversal": (
        "an exact pair of globally reversed coherent orientations is admissible; the early gate "
        "does not demand an absolute future label"
    ),
    "positive_reparameterisation": (
        "strictly positive state-regular rescaling is gauge only after one coherent orientation "
        "has been fixed"
    ),
    "forbidden_patch": (
        "local, statewise or schedule-dependent sign changes are new dynamics and cannot be gauge"
    ),
    "recurrence": (
        "a recurrent state is admissible only when the law derives distinct occurrences or a "
        "phase/record lift; returning to one state cannot create a two-way order of one occurrence"
    ),
    "scope": "no clock calibration, spatial causal cone or thermodynamic arrow is inferred",
}

F3B_SEPARABILITY_POLICY: dict[str, Any] = {
    "dependency": "F3b requires both F3a and F4 simultaneous-mode closure",
    "reason": (
        "forbidden transmission is nonvacuous only after the same carrier has produced multiple "
        "simultaneous, independently accountable mode occurrences"
    ),
    "support_origin": (
        "signal support and forbidden pairs must come from the carrier transfer law; a graph or "
        "light cone cannot be inserted"
    ),
    "nonvacuity": (
        "the forbidden-pair domain is nonempty, invariant and defined on a predeclared open domain"
    ),
    "scope": "continuum locality, finite metric speed and a Lorentzian cone remain later gates",
}

ROUTE_ARCHITECTURE: dict[str, Any] = {
    "F0_COMMON_RESONANT_KERNEL": {
        "depends_on": [],
        "requires": [
            "one self-relation carrier",
            "one autonomous target-free transfer law",
            "complete equivalence and perturbation class",
            "carrier-law origin and robustness audit",
        ],
    },
    "F1_SELF_DIFFERENTIATION": {
        "depends_on": ["F0_COMMON_RESONANT_KERNEL"],
        "requires": ["stable intrinsic differentiation from an undifferentiated reference"],
    },
    "F2_OPERATIONAL_RELATIONS": {
        "depends_on": ["F1_SELF_DIFFERENTIATION"],
        "requires": ["state-owned roles/nodes and an irreducible same-carrier relation"],
    },
    "F3a_INTRINSIC_PROCESS_ORIENTATION": {
        "depends_on": ["F0_COMMON_RESONANT_KERNEL", "F1_SELF_DIFFERENTIATION", "F2_OPERATIONAL_RELATIONS"],
        "requires": [
            "law-derived intrinsic process",
            "coherent orientation modulo global Z2 reversal",
            "schedule neutrality and no statewise sign patching",
        ],
    },
    "F4_SIMULTANEOUS_MODES": {
        "depends_on": ["F1_SELF_DIFFERENTIATION", "F2_OPERATIONAL_RELATIONS"],
        "requires": ["coexisting independently accountable effective modes"],
    },
    "F3b_CAUSAL_SEPARABILITY_NONTRANSMISSION": {
        "depends_on": ["F3a_INTRINSIC_PROCESS_ORIENTATION", "F4_SIMULTANEOUS_MODES"],
        "requires": [
            "derived signal support and direct influence",
            "nonempty invariant forbidden pairs",
            "forbidden-pair nontransmission",
        ],
    },
    "M1_DIMENSION_CONTINUUM": {
        "depends_on": ["F3b_CAUSAL_SEPARABILITY_NONTRANSMISSION", "F4_SIMULTANEOUS_MODES"],
        "requires": ["derived local counting/measure and continuum correspondence"],
    },
    "M2_LORENTZIAN_METRIC": {
        "depends_on": ["M1_DIMENSION_CONTINUUM", "F3b_CAUSAL_SEPARABILITY_NONTRANSMISSION"],
        "requires": ["one regular Lorentzian metric from derived order/support and measure"],
    },
}

CONDITIONAL_LEMMA_REGISTRY: dict[str, Any] = {
    "w2_09_atemporal_F1_representation": {
        "path": "RefG/work 2/w2_09_f1_atemporal_structural_promotion_gate.py",
        "identifier_kind": "CANDIDATE_ID",
        "identifier": "W2_F1_ATEMPORAL_SPECTRAL_SPLIT_CANDIDATE_001",
        "status": "CONDITIONAL_REPRESENTATION_LEMMA",
        "allowed_role": "exact atemporal structural-F1 existence lemma relative to imported primitives",
        "forbidden_inheritance": (
            "no common-kernel origin, transfer law, physical node, time, space or metric closure"
        ),
    },
    "w2_16_atemporal_F1_F2_representation": {
        "path": "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py",
        "identifier_kind": "CLAIM_ID",
        "identifier": "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CANDIDATE_001",
        "status": "CONDITIONAL_REPRESENTATION_LEMMA",
        "allowed_role": "exact same-representation F1/F2 existence lemma relative to imported carrier and law",
        "forbidden_inheritance": (
            "no carrier/law origin, mixed-law robustness, process, simultaneous physical modes, "
            "space or metric closure"
        ),
    },
    "w2_22_tangent_process_representation": {
        "path": "RefG/work 2/w2_22_f3_minimum_manifold_tangent_route_gate.py",
        "identifier_kind": "CLAIM_ID",
        "identifier": "W2_F3_MINIMUM_MANIFOLD_TANGENT_ROUTE_001",
        "status": "CONDITIONAL_REPRESENTATION_LEMMA",
        "allowed_role": "exact availability lemma for one non-gauge tangent quotient direction",
        "forbidden_inheritance": (
            "no foundation-selected transfer law, F3a promotion, F3b nontransmission, clock, "
            "space or metric closure"
        ),
    },
}


def _unsupplied(
    definition: str,
    required_for: list[str],
    depends_on: list[str],
) -> dict[str, Any]:
    return {
        "status": "UNSUPPLIED",
        "source": "future versioned common-kernel candidate",
        "definition": definition,
        "required_for": required_for,
        "depends_on": depends_on,
    }


CANDIDATE_INTERFACE: dict[str, dict[str, Any]] = {
    "carrier_state_domain": _unsupplied(
        "nontrivial states/relations of the one self-relation carrier",
        ["F0"], [],
    ),
    "self_relation_map": _unsupplied(
        "how one carrier state acts on or compares with the same carrier without imported nodes",
        ["F0", "F2"], ["carrier_state_domain"],
    ),
    "complete_equivalence_action": _unsupplied(
        "all descriptions that represent one physical carrier state",
        ["F0", "F1", "F2", "F3a", "F3b"], ["carrier_state_domain"],
    ),
    "autonomous_transfer_law": _unsupplied(
        "target-free state/occurrence transfer rule generated by the same carrier",
        ["F0", "F3a", "F3b"], ["carrier_state_domain", "self_relation_map"],
    ),
    "transfer_composition": _unsupplied(
        "law-derived composition of transfers, with no execution schedule interpreted physically",
        ["F0", "F3a", "F3b"], ["autonomous_transfer_law"],
    ),
    "undifferentiated_reference": _unsupplied(
        "candidate reference class with no nontrivial state-generated roles",
        ["F1"], ["carrier_state_domain", "complete_equivalence_action"],
    ),
    "self_differentiation_witness": _unsupplied(
        "stable intrinsic distinction surviving the complete equivalence",
        ["F1"], ["undifferentiated_reference", "autonomous_transfer_law"],
    ),
    "state_owned_role_or_node_map": _unsupplied(
        "roles/nodes reconstructed from one accepted carrier state rather than imported labels",
        ["F2"], ["self_differentiation_witness"],
    ),
    "common_carrier_ownership_map": _unsupplied(
        "reconstruction proving that all roles are restrictions/imprints of one carrier",
        ["F2", "F4"], ["state_owned_role_or_node_map", "self_relation_map"],
    ),
    "irreducible_relational_report": _unsupplied(
        "joint report not reconstructible from separate unary role data",
        ["F2"], ["state_owned_role_or_node_map", "common_carrier_ownership_map"],
    ),
    "state_owned_change_or_occurrence_map": _unsupplied(
        "changes or occurrences defined by the carrier law rather than an algorithmic index",
        ["F3a"], ["autonomous_transfer_law", "irreducible_relational_report"],
    ),
    "intrinsic_process_line": _unsupplied(
        "nonzero quotient process direction modulo positive reparameterisation",
        ["F3a"], ["state_owned_change_or_occurrence_map", "transfer_composition"],
    ),
    "orientation_double_cover": _unsupplied(
        "coherent orientation structure allowing at most one exact global Z2 reversal",
        ["F3a"], ["intrinsic_process_line", "complete_equivalence_action"],
    ),
    "recurrence_occurrence_lift": _unsupplied(
        "law-derived occurrence/phase/record lift for recurrent states, or a proof of nonrecurrence",
        ["F3a"], ["state_owned_change_or_occurrence_map", "transfer_composition"],
    ),
    "simultaneous_mode_inventory": _unsupplied(
        "coexisting effective modes of one carrier, not successive frames or labels",
        ["F4", "F3b"], ["common_carrier_ownership_map", "irreducible_relational_report"],
    ),
    "mode_independence_readout": _unsupplied(
        "independent state accounting before later conservation/additivity laws",
        ["F4", "F3b"], ["simultaneous_mode_inventory"],
    ),
    "allowed_interventions": _unsupplied(
        "equivalence-invariant perturbations of derived mode occurrences",
        ["F3b"], ["mode_independence_readout", "state_owned_change_or_occurrence_map"],
    ),
    "direct_influence_relation": _unsupplied(
        "nonzero intervention response obtained from the transfer law",
        ["F3b"], ["allowed_interventions", "autonomous_transfer_law"],
    ),
    "signal_support_composition": _unsupplied(
        "derived support and composition of influence without a prewired graph",
        ["F3b", "M1"], ["direct_influence_relation", "transfer_composition"],
    ),
    "forbidden_pair_domain": _unsupplied(
        "nonempty invariant pairs outside direct/effective signal support",
        ["F3b"], ["signal_support_composition", "simultaneous_mode_inventory"],
    ),
    "nontransmission_test": _unsupplied(
        "zero response for every declared forbidden pair under allowed interventions",
        ["F3b"], ["forbidden_pair_domain", "allowed_interventions"],
    ),
    "open_domain_and_nulls": _unsupplied(
        "predeclared open candidate domain, boundaries, singular points and null branches",
        ["F0", "F1", "F2", "F3a", "F4", "F3b"], ["carrier_state_domain"],
    ),
    "perturbation_class": _unsupplied(
        "all symmetry-allowed law/state perturbations used for robustness",
        ["F0", "F1", "F2", "F3a", "F4", "F3b"], ["complete_equivalence_action"],
    ),
    "independent_crosscheck": _unsupplied(
        "second derivation or algorithm not trained on the first result",
        ["F0", "F1", "F2", "F3a", "F4", "F3b"], [],
    ),
}


def frozen_physical_closure_flags() -> dict[str, bool]:
    return {
        "F0_common_resonant_kernel_derived": False,
        "F0_self_relation_carrier_origin_proved": False,
        "F0_autonomous_transfer_law_origin_proved": False,
        "F0_carrier_law_robustness_proved": False,
        "F1_self_differentiation_proved_on_derived_kernel": False,
        "F2_operational_relations_proved_on_derived_kernel": False,
        "F3a_intrinsic_process_orientation_proved": False,
        "F4_simultaneous_modes_proved": False,
        "F3b_causal_separability_nontransmission_proved": False,
        "foundation_to_effective_closed": False,
        "M1_dimension_continuum_proved": False,
        "M2_Lorentzian_metric_proved": False,
        "A0_effective_action_origin_proved": False,
        "A1_action_variation_proved": False,
        "A2_conservation_no_double_count_proved": False,
        "A3_degree_of_freedom_health_proved": False,
        "A4_universal_matter_metric_proved": False,
        "E1_reduced_action_matching_proved": False,
        "E2_exact_Einstein_entrance_proved": False,
        "source_matching_or_PN_PPN_handoff_proved": False,
        "observational_validation_proved": False,
    }


EXPECTED_PHYSICAL_CLOSURE_FLAGS = frozen_physical_closure_flags()

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "Freeze an outcome-neutral revised Work-2 route whose minimal irreducible primitive is "
        "one ontological identity represented by one self-relation carrier plus one autonomous "
        "target-free transfer law, and separate intrinsic process orientation F3a from F4-dependent "
        "causal separability/nontransmission F3b."
    ),
    "TYPE": "OUTCOME_NEUTRAL_REVISED_PROGRAM_CONTRACT",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "The frozen W2-C0 contract remains historical baseline and is not edited here. A strict "
        "singleton/no-law system cannot self-differentiate. One ontology may nevertheless have a "
        "nontrivial self-relation state domain and a law without becoming several substances. "
        "The registered w2_09, w2_16 and w2_22 results are conditional mathematical lemmas only."
    ),
    "DOMAIN": (
        "Candidate-neutral, pre-spatial and pre-clock. A later candidate must freeze its exact "
        "carrier domain, equivalence, autonomous law, open branches, nulls and perturbation class "
        "before any F0/F1/F2/F3a/F4/F3b outcome is evaluated."
    ),
    "CONVENTIONS": (
        "The word identity counts ontological carriers, not states. Self-relation denotes a "
        "candidate-internal comparison/action and carries no spatial meaning. Transfer is an "
        "autonomous law relation and carries no clock calibration. Positive process "
        "reparameterisation is distinguished from a global Z2 reversal and from forbidden "
        "statewise sign patching."
    ),
    "FREEDOM_LEDGER": {
        "ontological_identity": {
            "source": "revised primitive policy",
            "allowed_range": "exactly one",
            "scale": "ontology",
            "complexity": 1,
        },
        "self_relation_carrier": {
            "source": "future candidate; unsupplied here",
            "allowed_range": "one irreducible carrier with a nontrivial state/relation domain",
            "scale": "foundation",
            "complexity": "candidate must declare every algebraic freedom",
        },
        "autonomous_transfer_law": {
            "source": "future candidate; unsupplied here",
            "allowed_range": "one target-free law on the same carrier",
            "scale": "foundation",
            "complexity": "all coefficients, functions, kernels and branches must be charged",
        },
        "complete_equivalence": {
            "source": "future candidate; unsupplied here",
            "allowed_range": "full descriptive redundancy only",
            "scale": "representation",
            "complexity": 0,
        },
        "global_orientation_Z2": {
            "source": "allowed coherent orientation ambiguity",
            "allowed_range": "one global reversal pair or a uniquely law-selected orientation",
            "scale": "whole connected process domain",
            "complexity": 0,
        },
        "positive_process_reparameterisation": {
            "source": "process gauge after coherent orientation",
            "allowed_range": "strictly positive regular multipliers",
            "scale": "process path",
            "complexity": 0,
        },
        "candidate_parameters_functions_and_initial_data": {
            "source": "future candidate ledger",
            "allowed_range": "must be frozen and classified before evaluation",
            "scale": "universal/group/state/data as applicable",
            "complexity": "fully charged",
        },
        "computational_index": {
            "source": "algorithm only",
            "allowed_range": "no physical interpretation",
            "scale": "implementation",
            "complexity": 0,
        },
        "preloaded_physical_structure_or_data": {
            "source": "forbidden",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "CODES.md: claim contract, gate, status and evidence rules",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md: unchanged frozen baseline",
        "RefG/work 2/w2_09_f1_atemporal_structural_promotion_gate.py: conditional representation lemma only",
        "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py: conditional representation lemma only",
        "RefG/work 2/w2_22_f3_minimum_manifold_tangent_route_gate.py: conditional representation lemma only",
    ],
    "METHOD": (
        "Freeze the primitive policy, exact candidate interface, revised dependency graph, F3a "
        "orientation policy, F3b separability policy, forbidden preloads, lemma registry and every "
        "physical false flag. Validate exact schemas and deterministic hashes, identity-check safe "
        "legacy module constants, and exercise positive, negative, malformed and mutation controls."
    ),
    "PASS_CONDITION": (
        "This file passes only as an outcome-neutral contract if every required field, interface "
        "entry, dependency, policy, hash, legacy-ceiling check and fail-closed control is exact, "
        "and every physical closure flag remains boolean False. Contract validity cannot promote "
        "a future candidate or inherit a legacy conditional result."
    ),
    "FAIL_CONDITION": (
        "Any schema/hash/dependency drift, supplied or promoted candidate outcome, hidden primitive, "
        "legacy-result inheritance, forbidden preload, absolute-arrow requirement, statewise sign "
        "patch, schedule semantics, F3b eligibility before F4, vacuous forbidden-pair domain, "
        "nonboolean field or true physical closure flag invalidates this contract."
    ),
    "FALSIFIER": (
        "The contract is falsified if its screen accepts malformed evidence, promotes any physical "
        "claim, treats a strict singleton/no-law system as a viable differentiating kernel, imports "
        "nodes/space/time/graph/dimension/group/metric/GR, upgrades a conditional legacy lemma to "
        "origin, rejects a coherent global reversal merely for lacking an absolute future label, "
        "allows statewise orientation patches, or permits F3b without F4 and a nonempty derived "
        "forbidden-pair domain."
    ),
    "RESIDUAL": "N/A: this contract evaluates definitions and logic, not a candidate equation.",
    "ERROR_BOUND": "N/A: no approximation, numerical evolution, data or likelihood is used.",
    "VALIDITY_HEALTH": (
        "Every later candidate must separately prove state-domain closure, existence, uniqueness or "
        "declared branching, law robustness under all allowed perturbations, recurrence handling, "
        "constraint preservation and the health required by its claimed domain."
    ),
    "BRANCHES": {
        "strict_singleton_no_law": "INADMISSIBLE_NO_SELF_DIFFERENTIATION_BOUNDARY",
        "one_carrier_plus_autonomous_law": "OPEN_FUTURE_CANDIDATE",
        "legacy_matrix_representations": "CONDITIONAL_LEMMAS_NO_INHERITANCE",
        "F3a_unique_orientation": "ADMISSIBLE_IF_LAW_DERIVED",
        "F3a_global_Z2_orientation_pair": "ADMISSIBLE_IF_GLOBALLY_COHERENT",
        "F3a_statewise_sign_patch": "REJECTED_NEW_DYNAMICS_NOT_GAUGE",
        "F3b_before_F4": "INELIGIBLE",
        "physical_time_space_metric_GR": "OPEN_LATER_GATES",
    },
    "OBSERVABLE_MAP": {
        "status": "N/A",
        "reason": "pre-spatial outcome-neutral program contract",
    },
    "FORWARD_MODEL": {
        "status": "N/A",
        "reason": "an internal transfer-law interface is not a data forward model",
    },
    "DATA_ROLE": {
        "status": "N/A",
        "reason": "no data, target, fit, validation or prediction is used",
    },
    "IDENTIFIABILITY": (
        "A later candidate must distinguish ontology count from state dimension, physical roles from "
        "representation sectors, process orientation from parameter speed, a global reversal from "
        "statewise patches, and causal nontransmission from algebraic cross-channel zeros."
    ),
    "BENCHMARK": (
        "Contract controls use a complete synthetic interface as the positive logic case; strict "
        "singleton/no-law, imported labels, local sign flips, schedule order, F3b without F4, empty "
        "forbidden pairs, missing/extra/nonboolean maps and gates, and mutated frozen payloads are "
        "negative cases. These controls are not physical candidates."
    ),
    "CLOSURE_FLAGS": frozen_physical_closure_flags(),
    "CROSSCHECK": (
        "Recompute every canonical SHA-256 hash, import only stable legacy constants, compare exact "
        "schemas, mutate each protected payload class, and verify that a complete synthetic report "
        "can be eligible while this contract still never promotes it."
    ),
    "PROVENANCE": {
        "date": "2026-07-23",
        "data": "none",
        "code_version": "w2_23 contract v1.0",
        "legacy_role": "identity-checked conditional lemmas only",
    },
    "FILES": [
        "RefG/work 2/w2_23_common_resonant_kernel_contract.py",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_09_f1_atemporal_structural_promotion_gate.py",
        "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py",
        "RefG/work 2/w2_22_f3_minimum_manifold_tangent_route_gate.py",
    ],
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def _canonical_sha256(payload: Any) -> str:
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest().upper()


# Filled from the literal payloads above.  They are intentionally independent
# of this source file's byte hash, so the contract can verify itself without a
# self-referential checksum.
EXPECTED_PRIMITIVE_POLICY_SHA256 = (
    "7BFE3FD7202DAD8ACF7BA5FC85A48580405EF7C843AE458429CFAD6E412370A2"
)
EXPECTED_F3A_POLICY_SHA256 = (
    "1F2E37E7DCCC516E2CB73835F394335DBD8B2526B4E3C75A0D5A9695F6E5B7EC"
)
EXPECTED_F3B_POLICY_SHA256 = (
    "9F8725DDF24C0A0BF74305094D85B186293F6E5150F19154ECD5A6EAFE647D55"
)
EXPECTED_ROUTE_ARCHITECTURE_SHA256 = (
    "B77727A3119CA9D80CF06FFB025B27B8C606BFF2B582E423D147FF5D0BF42E4B"
)
EXPECTED_LEMMA_REGISTRY_SHA256 = (
    "B4FDEFA35145D66DA6D425545AFB8BFB42D3568D0673212CA0FE2FDE7ADB5385"
)
EXPECTED_CANDIDATE_INTERFACE_SHA256 = (
    "D35CC81EE3ABB662A725947A19FF0900A5F1517C325D643EE9A8EB4262E41D1A"
)
EXPECTED_SCIENTIFIC_CONTRACT_SHA256 = (
    "29780C0570D19B091B786B8794C4974C540EE4D5B201C80878581661E7407D6D"
)


def _load_sibling(filename: str, module_name: str) -> ModuleType:
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _exact_bool_map(actual: Any, expected_keys: frozenset[str]) -> bool:
    return (
        isinstance(actual, dict)
        and set(actual) == set(expected_keys)
        and all(type(value) is bool for value in actual.values())
    )


def _all_false_boolean_map(actual: Any, expected: dict[str, bool]) -> bool:
    return (
        isinstance(actual, dict)
        and actual == expected
        and all(type(value) is bool and value is False for value in actual.values())
    )


def _candidate_interface_schema_valid(candidate_maps: Any) -> bool:
    if not isinstance(candidate_maps, dict) or tuple(candidate_maps) != REQUIRED_CANDIDATE_MAPS:
        return False
    for entry in candidate_maps.values():
        if not isinstance(entry, dict) or set(entry) != set(INTERFACE_ENTRY_KEYS):
            return False
        if entry["status"] not in INTERFACE_STATUSES:
            return False
        if not isinstance(entry["source"], str) or not isinstance(entry["definition"], str):
            return False
        if not isinstance(entry["required_for"], list) or not all(
            isinstance(value, str) for value in entry["required_for"]
        ):
            return False
        if not isinstance(entry["depends_on"], list) or not all(
            isinstance(value, str) and value in candidate_maps
            for value in entry["depends_on"]
        ):
            return False
    return True


def _derived_maps(candidate_maps: dict[str, dict[str, Any]], required: frozenset[str]) -> bool:
    return all(candidate_maps[name]["status"] == "DERIVED" for name in required)


def candidate_screen(
    candidate_maps: Any,
    f3a_gates: Any,
    f4_simultaneous_modes: Any,
    f3b_gates: Any,
    forbidden_pair_nonempty: Any,
) -> dict[str, bool]:
    """Fail-closed eligibility screen; this contract never promotes a candidate."""
    maps_valid = _candidate_interface_schema_valid(candidate_maps)
    f3a_schema_valid = _exact_bool_map(f3a_gates, F3A_GATE_KEYS)
    f3b_schema_valid = _exact_bool_map(f3b_gates, F3B_GATE_KEYS)
    scalar_types_valid = (
        type(f4_simultaneous_modes) is bool
        and type(forbidden_pair_nonempty) is bool
    )
    valid = maps_valid and f3a_schema_valid and f3b_schema_valid and scalar_types_valid
    f3a_eligible = bool(
        valid
        and _derived_maps(candidate_maps, F3A_REQUIRED_MAPS)
        and all(f3a_gates.values())
    )
    f3b_eligible = bool(
        valid
        and f3a_eligible
        and f4_simultaneous_modes is True
        and _derived_maps(candidate_maps, F3B_REQUIRED_MAPS)
        and all(f3b_gates.values())
        and forbidden_pair_nonempty is True
    )
    return {
        "valid": bool(valid),
        "F3a_eligible": f3a_eligible,
        "F3b_eligible": f3b_eligible,
        "promoted": False,
    }


def _all_derived_interface() -> dict[str, dict[str, Any]]:
    candidate = deepcopy(CANDIDATE_INTERFACE)
    for entry in candidate.values():
        entry["status"] = "DERIVED"
        entry["source"] = "synthetic logic control only"
    return candidate


def _dependency_controls() -> dict[str, bool]:
    w209 = _load_sibling(
        "w2_09_f1_atemporal_structural_promotion_gate.py", "w2_23_dep_w209"
    )
    w216 = _load_sibling(
        "w2_16_f2b_general_traceless_single_carrier_candidate_gate.py", "w2_23_dep_w216"
    )
    w222 = _load_sibling(
        "w2_22_f3_minimum_manifold_tangent_route_gate.py", "w2_23_dep_w222"
    )

    w216_scope = w216.CLAIM_CONTRACT["SCOPE_CEILING"]
    w216_closure = w216.CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"]
    w222_closure = w222.EXPECTED_CLOSURE_FLAGS
    return {
        "w2_09_identity_exact": all((
            w209.CANDIDATE_ID
            == CONDITIONAL_LEMMA_REGISTRY["w2_09_atemporal_F1_representation"]["identifier"],
            w209.MODEL_VERSION == "W2-F1-ATEMPORAL-STRUCTURAL-PROMOTION-v1.0-scientific",
        )),
        "w2_09_origin_ceiling_is_conditional": all((
            w209.LAW_ORIGIN_STATUS == "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
            not any(w209.SCOPE_FIREWALL.values()),
            w209.SCOPE_FIREWALL.get("operational_relation") is False,
            w209.SCOPE_FIREWALL.get("internal_causal_order_or_clock") is False,
            w209.SCOPE_FIREWALL.get("independent_additive_physical_modes") is False,
        )),
        "w2_16_identity_exact": all((
            w216.CLAIM_CONTRACT["CLAIM_ID"]
            == CONDITIONAL_LEMMA_REGISTRY["w2_16_atemporal_F1_F2_representation"]["identifier"],
            w216.CLAIM_CONTRACT["TYPE"] == "CONDITIONAL_EXACT_STRUCTURAL_CANDIDATE_THEOREM",
        )),
        "w2_16_origin_robustness_and_process_ceiling_conditional": all((
            w216_closure.get("conditional_on_imported_A_and_law") is True,
            w216_scope.get("mixed_coupling_robustness_or_A3_health") is False,
            w216_scope.get("F3_time_memory_persistence_or_causality") is False,
            w216_scope.get("F4_conservation_or_additive_modes") is False,
        )),
        "w2_22_identity_exact": all((
            w222.CLAIM_ID
            == CONDITIONAL_LEMMA_REGISTRY["w2_22_tangent_process_representation"]["identifier"],
            w222.MODEL_VERSION == "W2-F3-MINIMUM-MANIFOLD-TANGENT-v2.0-GAUGE-AUDITED",
        )),
        "w2_22_process_and_causal_ceiling_conditional": all((
            "F3_PROCESS_AND_NONTRANSMISSION_OPEN" in w222.CANDIDATE_STATUS_PASS,
            w222_closure.get("foundation_process_law_derived") is False,
            w222_closure.get("F3_internal_order_or_causality_proved") is False,
            w222_closure.get("gauge_invariant_forbidden_pair_nontransmission_proved") is False,
        )),
        "legacy_modules_registered_only_as_conditional_lemmas": all(
            entry["status"] == "CONDITIONAL_REPRESENTATION_LEMMA"
            for entry in CONDITIONAL_LEMMA_REGISTRY.values()
        ),
    }


DEFINITION_CONTROL_KEYS = frozenset({
    "scientific_contract_schema_exact",
    "claim_and_model_identity_exact",
    "primitive_policy_hash_exact",
    "F3a_policy_hash_exact",
    "F3b_policy_hash_exact",
    "route_architecture_hash_exact",
    "lemma_registry_hash_exact",
    "candidate_interface_hash_exact",
    "scientific_contract_hash_exact",
    "candidate_interface_schema_exact_and_unsupplied",
    "forbidden_preload_registry_exact",
    "one_identity_carrier_plus_law_not_strict_singleton",
    "no_physical_structure_preloaded",
    "F3a_global_reversal_allowed_without_statewise_patch",
    "F3b_depends_exactly_on_F3a_and_F4",
    "legacy_roles_conditional_and_no_inheritance",
    "all_physical_closure_flags_exactly_false",
    "dependency_constants_and_ceilings_exact",
})

FAIL_CLOSED_CONTROL_KEYS = frozenset({
    "complete_synthetic_report_eligible_but_never_promoted",
    "each_false_F3a_gate_blocks_F3a_and_F3b",
    "each_false_F3b_gate_blocks_only_F3b",
    "F4_false_blocks_F3b_not_F3a",
    "empty_forbidden_pair_domain_blocks_F3b",
    "missing_extra_nonboolean_F3a_gate_invalid",
    "missing_extra_nonboolean_F3b_gate_invalid",
    "missing_extra_malformed_candidate_map_invalid",
    "partial_required_map_blocks_eligibility",
    "contract_content_mutation_detected",
    "primitive_policy_mutation_detected",
    "route_dependency_mutation_detected",
    "lemma_role_mutation_detected",
    "physical_closure_mutation_rejected",
    "hashes_are_repeatably_deterministic",
})


def definition_controls() -> dict[str, bool]:
    dependency = _dependency_controls()
    preload_keys = tuple(PRIMITIVE_POLICY["imported_physical_structures"])
    expected_preload_keys = (
        "nodes", "space", "clock_time", "graph", "fixed_dimension", "O3", "metric", "GR"
    )
    return {
        "scientific_contract_schema_exact": set(CLAIM_CONTRACT) == set(REQUIRED_SCIENTIFIC_FIELDS),
        "claim_and_model_identity_exact": all((
            CLAIM_CONTRACT["CLAIM_ID"] == CLAIM_ID,
            CLAIM_CONTRACT["MODEL_VERSION"] == MODEL_VERSION,
            CLAIM_CONTRACT["TYPE"] == "OUTCOME_NEUTRAL_REVISED_PROGRAM_CONTRACT",
        )),
        "primitive_policy_hash_exact": (
            _canonical_sha256(PRIMITIVE_POLICY) == EXPECTED_PRIMITIVE_POLICY_SHA256
        ),
        "F3a_policy_hash_exact": (
            _canonical_sha256(F3A_ORIENTATION_POLICY) == EXPECTED_F3A_POLICY_SHA256
        ),
        "F3b_policy_hash_exact": (
            _canonical_sha256(F3B_SEPARABILITY_POLICY) == EXPECTED_F3B_POLICY_SHA256
        ),
        "route_architecture_hash_exact": (
            _canonical_sha256(ROUTE_ARCHITECTURE) == EXPECTED_ROUTE_ARCHITECTURE_SHA256
        ),
        "lemma_registry_hash_exact": (
            _canonical_sha256(CONDITIONAL_LEMMA_REGISTRY) == EXPECTED_LEMMA_REGISTRY_SHA256
        ),
        "candidate_interface_hash_exact": (
            _canonical_sha256(CANDIDATE_INTERFACE) == EXPECTED_CANDIDATE_INTERFACE_SHA256
        ),
        "scientific_contract_hash_exact": (
            _canonical_sha256(CLAIM_CONTRACT) == EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        ),
        "candidate_interface_schema_exact_and_unsupplied": all((
            _candidate_interface_schema_valid(CANDIDATE_INTERFACE),
            all(entry["status"] == "UNSUPPLIED" for entry in CANDIDATE_INTERFACE.values()),
        )),
        "forbidden_preload_registry_exact": all((
            len(FORBIDDEN_PRELOADS) == 12,
            len(set(FORBIDDEN_PRELOADS)) == len(FORBIDDEN_PRELOADS),
            all(isinstance(value, str) and value for value in FORBIDDEN_PRELOADS),
        )),
        "one_identity_carrier_plus_law_not_strict_singleton": all((
            PRIMITIVE_POLICY["ontological_identity_count"] == 1,
            "self-relation carrier" in PRIMITIVE_POLICY["minimal_mathematical_representation"],
            "autonomous target-free transfer law" in PRIMITIVE_POLICY["law_requirement"],
            "cannot be promoted" in PRIMITIVE_POLICY["strict_singleton_boundary"],
        )),
        "no_physical_structure_preloaded": all((
            preload_keys == expected_preload_keys,
            not any(PRIMITIVE_POLICY["imported_physical_structures"].values()),
        )),
        "F3a_global_reversal_allowed_without_statewise_patch": all((
            "globally reversed" in F3A_ORIENTATION_POLICY["global_reversal"],
            "statewise" in F3A_ORIENTATION_POLICY["forbidden_patch"],
            "absolute future" in F3A_ORIENTATION_POLICY["global_reversal"],
            "law_selected_orientation_or_global_Z2_pair_proved" in F3A_GATE_KEYS,
            "statewise_sign_patching_excluded" in F3A_GATE_KEYS,
        )),
        "F3b_depends_exactly_on_F3a_and_F4": (
            ROUTE_ARCHITECTURE["F3b_CAUSAL_SEPARABILITY_NONTRANSMISSION"]["depends_on"]
            == ["F3a_INTRINSIC_PROCESS_ORIENTATION", "F4_SIMULTANEOUS_MODES"]
            and F3B_SEPARABILITY_POLICY["dependency"]
            == "F3b requires both F3a and F4 simultaneous-mode closure"
        ),
        "legacy_roles_conditional_and_no_inheritance": all(
            entry["status"] == "CONDITIONAL_REPRESENTATION_LEMMA"
            and entry["forbidden_inheritance"]
            for entry in CONDITIONAL_LEMMA_REGISTRY.values()
        ),
        "all_physical_closure_flags_exactly_false": _all_false_boolean_map(
            CLAIM_CONTRACT["CLOSURE_FLAGS"], EXPECTED_PHYSICAL_CLOSURE_FLAGS
        ),
        "dependency_constants_and_ceilings_exact": (
            set(dependency) == {
                "w2_09_identity_exact",
                "w2_09_origin_ceiling_is_conditional",
                "w2_16_identity_exact",
                "w2_16_origin_robustness_and_process_ceiling_conditional",
                "w2_22_identity_exact",
                "w2_22_process_and_causal_ceiling_conditional",
                "legacy_modules_registered_only_as_conditional_lemmas",
            }
            and all(dependency.values())
        ),
    }


def fail_closed_controls() -> dict[str, bool]:
    maps = _all_derived_interface()
    f3a = {key: True for key in F3A_GATE_KEYS}
    f3b = {key: True for key in F3B_GATE_KEYS}
    baseline = candidate_screen(maps, f3a, True, f3b, True)

    false_f3a_results = []
    for key in F3A_GATE_KEYS:
        mutated = dict(f3a)
        mutated[key] = False
        false_f3a_results.append(candidate_screen(maps, mutated, True, f3b, True))

    false_f3b_results = []
    for key in F3B_GATE_KEYS:
        mutated = dict(f3b)
        mutated[key] = False
        false_f3b_results.append(candidate_screen(maps, f3a, True, mutated, True))

    malformed_f3a = []
    missing = dict(f3a)
    missing.pop(next(iter(F3A_GATE_KEYS)))
    malformed_f3a.append(missing)
    extra = dict(f3a)
    extra["extra"] = True
    malformed_f3a.append(extra)
    nonboolean = dict(f3a)
    nonboolean[next(iter(F3A_GATE_KEYS))] = 1
    malformed_f3a.append(nonboolean)

    malformed_f3b = []
    missing = dict(f3b)
    missing.pop(next(iter(F3B_GATE_KEYS)))
    malformed_f3b.append(missing)
    extra = dict(f3b)
    extra["extra"] = True
    malformed_f3b.append(extra)
    nonboolean = dict(f3b)
    nonboolean[next(iter(F3B_GATE_KEYS))] = "True"
    malformed_f3b.append(nonboolean)

    malformed_maps: list[Any] = []
    missing_map = deepcopy(maps)
    missing_map.pop(REQUIRED_CANDIDATE_MAPS[0])
    malformed_maps.append(missing_map)
    extra_map = deepcopy(maps)
    extra_map["extra"] = deepcopy(next(iter(maps.values())))
    malformed_maps.append(extra_map)
    malformed_entry = deepcopy(maps)
    malformed_entry[REQUIRED_CANDIDATE_MAPS[0]].pop("source")
    malformed_maps.append(malformed_entry)

    partial_maps = deepcopy(maps)
    partial_maps["autonomous_transfer_law"]["status"] = "PARTIAL"

    mutated_contract = deepcopy(CLAIM_CONTRACT)
    mutated_contract["CLAIM"] += " MUTATED"
    mutated_primitive = deepcopy(PRIMITIVE_POLICY)
    mutated_primitive["ontological_identity_count"] = 2
    mutated_route = deepcopy(ROUTE_ARCHITECTURE)
    mutated_route["F3b_CAUSAL_SEPARABILITY_NONTRANSMISSION"]["depends_on"] = [
        "F3a_INTRINSIC_PROCESS_ORIENTATION"
    ]
    mutated_lemmas = deepcopy(CONDITIONAL_LEMMA_REGISTRY)
    mutated_lemmas["w2_22_tangent_process_representation"]["allowed_role"] += " PROMOTED"
    mutated_closure = deepcopy(EXPECTED_PHYSICAL_CLOSURE_FLAGS)
    mutated_closure["F3a_intrinsic_process_orientation_proved"] = True

    return {
        "complete_synthetic_report_eligible_but_never_promoted": all((
            baseline["valid"], baseline["F3a_eligible"], baseline["F3b_eligible"],
            not baseline["promoted"],
        )),
        "each_false_F3a_gate_blocks_F3a_and_F3b": all(
            result["valid"]
            and not result["F3a_eligible"]
            and not result["F3b_eligible"]
            and not result["promoted"]
            for result in false_f3a_results
        ),
        "each_false_F3b_gate_blocks_only_F3b": all(
            result["valid"]
            and result["F3a_eligible"]
            and not result["F3b_eligible"]
            and not result["promoted"]
            for result in false_f3b_results
        ),
        "F4_false_blocks_F3b_not_F3a": (
            (lambda result: all((
                result["valid"], result["F3a_eligible"],
                not result["F3b_eligible"], not result["promoted"],
            )))(candidate_screen(maps, f3a, False, f3b, True))
        ),
        "empty_forbidden_pair_domain_blocks_F3b": (
            (lambda result: all((
                result["valid"], result["F3a_eligible"],
                not result["F3b_eligible"], not result["promoted"],
            )))(candidate_screen(maps, f3a, True, f3b, False))
        ),
        "missing_extra_nonboolean_F3a_gate_invalid": all(
            not candidate_screen(maps, item, True, f3b, True)["valid"]
            for item in malformed_f3a
        ),
        "missing_extra_nonboolean_F3b_gate_invalid": all(
            not candidate_screen(maps, f3a, True, item, True)["valid"]
            for item in malformed_f3b
        ),
        "missing_extra_malformed_candidate_map_invalid": all(
            not candidate_screen(item, f3a, True, f3b, True)["valid"]
            for item in malformed_maps
        ),
        "partial_required_map_blocks_eligibility": (
            (lambda result: all((
                result["valid"], not result["F3a_eligible"],
                not result["F3b_eligible"], not result["promoted"],
            )))(candidate_screen(partial_maps, f3a, True, f3b, True))
        ),
        "contract_content_mutation_detected": (
            _canonical_sha256(mutated_contract) != EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        ),
        "primitive_policy_mutation_detected": (
            _canonical_sha256(mutated_primitive) != EXPECTED_PRIMITIVE_POLICY_SHA256
        ),
        "route_dependency_mutation_detected": (
            _canonical_sha256(mutated_route) != EXPECTED_ROUTE_ARCHITECTURE_SHA256
        ),
        "lemma_role_mutation_detected": (
            _canonical_sha256(mutated_lemmas) != EXPECTED_LEMMA_REGISTRY_SHA256
        ),
        "physical_closure_mutation_rejected": (
            not _all_false_boolean_map(mutated_closure, EXPECTED_PHYSICAL_CLOSURE_FLAGS)
        ),
        "hashes_are_repeatably_deterministic": all((
            _canonical_sha256(PRIMITIVE_POLICY) == _canonical_sha256(deepcopy(PRIMITIVE_POLICY)),
            _canonical_sha256(ROUTE_ARCHITECTURE) == _canonical_sha256(deepcopy(ROUTE_ARCHITECTURE)),
            _canonical_sha256(CANDIDATE_INTERFACE) == _canonical_sha256(deepcopy(CANDIDATE_INTERFACE)),
            _canonical_sha256(CLAIM_CONTRACT) == _canonical_sha256(deepcopy(CLAIM_CONTRACT)),
        )),
    }


def run() -> dict[str, Any]:
    dependency = _dependency_controls()
    definition = definition_controls()
    fail_closed = fail_closed_controls()
    valid = bool(
        _exact_bool_map(definition, DEFINITION_CONTROL_KEYS)
        and all(definition.values())
        and _exact_bool_map(fail_closed, FAIL_CLOSED_CONTROL_KEYS)
        and all(fail_closed.values())
        and all(dependency.values())
        and _all_false_boolean_map(
            CLAIM_CONTRACT["CLOSURE_FLAGS"], EXPECTED_PHYSICAL_CLOSURE_FLAGS
        )
    )
    hashes = {
        "primitive_policy": _canonical_sha256(PRIMITIVE_POLICY),
        "F3a_orientation_policy": _canonical_sha256(F3A_ORIENTATION_POLICY),
        "F3b_separability_policy": _canonical_sha256(F3B_SEPARABILITY_POLICY),
        "route_architecture": _canonical_sha256(ROUTE_ARCHITECTURE),
        "conditional_lemma_registry": _canonical_sha256(CONDITIONAL_LEMMA_REGISTRY),
        "candidate_interface": _canonical_sha256(CANDIDATE_INTERFACE),
        "scientific_contract": _canonical_sha256(CLAIM_CONTRACT),
    }
    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": valid,
        "contract_status": (
            "OUTCOME_NEUTRAL_COMMON_RESONANT_KERNEL_CONTRACT_VALID"
            if valid else "INVALID_CONTRACT_NO_PROMOTION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The revised primitive and F3a/F3b route are definition-frozen. No carrier, law, "
            "self-differentiation, node, process, simultaneous mode, causal separation, space, "
            "metric, Einstein bridge or observation is proved."
        ),
        "primitive_policy": PRIMITIVE_POLICY,
        "route_architecture": ROUTE_ARCHITECTURE,
        "conditional_lemma_registry": CONDITIONAL_LEMMA_REGISTRY,
        "candidate_interface": CANDIDATE_INTERFACE,
        "F3a_gate_keys": sorted(F3A_GATE_KEYS),
        "F3b_gate_keys": sorted(F3B_GATE_KEYS),
        "physical_closure_flags": CLAIM_CONTRACT["CLOSURE_FLAGS"],
        "hashes": hashes,
        "dependency_controls": dependency,
        "controls": {
            "definition": definition,
            "fail_closed": fail_closed,
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
            "contract_status": "INVALID_CONTRACT_NO_PROMOTION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
