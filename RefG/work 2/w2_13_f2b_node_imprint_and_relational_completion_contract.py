"""Fail-closed contract for the remaining W2-F2 relational completion gates.

The inherited w2_12 result proves only a narrow, atemporal F2a comparison.
This module freezes the additional candidate-neutral obligations for internal
state-supported nodes, an atemporal relational carrier, irreducible pair
content, complete-equivalence invariance, and same-chain compatibility.

No F2b candidate is evaluated here.  Full W2-F2, persistence, time, physical
location, interaction, geometry, observables, and data all remain open.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
from fractions import Fraction
from itertools import permutations
from pathlib import Path
from typing import Any


MODEL_VERSION = "W2-F2B-NODE-IMPRINT-RELATIONAL-COMPLETION-CONTRACT-v1.0-internal"
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"
F2A_CONTRACT_MODEL = "W2-F2A-INTERNAL-OPERATIONAL-DISTINCTION-CONTRACT-v1.2-internal"
F2A_CONTRACT_STATUS = "W2_F2A_CONTRACT_FROZEN__NO_CANDIDATE_EVALUATED__FULL_F2_OPEN"
F2A_CONTRACT_PAYLOAD = "4F09319C5DE3569AFA7FC2AA8FEA2190438D2E15EECC4DFCA815D69999FD37E2"
F2A_CONTRACT_VALIDATOR = "8AAA08C517DC623CFEA2DB18223F9EC7670F1A01D085AFD2CDFB0E1851C31666"
W211_MODEL = "W2-F2-SINGLE-ORBIT-READOUT-NO-GO-v1.0-internal"
W211_STATUS = "CONDITIONAL_EXACT_SINGLE_ORBIT_WHOLE_STATE_READOUT_NO_GO__F2A_OPEN"
W211_PAYLOAD = "488F32736333427A1164963917B04A5962AB73ED5326BD8A90E24380AFD37EC6"
W211_VALIDATOR = "EC3514B0CCB1DE0425E3E18B447C408EC0D58F30798CE58DD37C12CAA167091D"
W212_MODEL = "W2-F2A-INTRASTATE-HESSIAN-COMPARISON-v1.0-internal"
W212_STATUS = "CONDITIONAL_EXACT_F2A_INTRASTATE_HESSIAN_COMPARISON__FULL_F2_OPEN"
W212_PAYLOAD = "2D6621D8932D4DB3272ED2777DC4D08C3C5CB0A625508D695043C23424DA0455"
W212_VALIDATOR = "3B6CA4D52EEB5797F5304A3EC2B779CBC9F0FF91695C65902AE5DAFF1EA8DC49"
F1_MODEL = "RefG-F1-ATEMPORAL-STRUCTURAL-PROOF-v1.0"
F1_STATUS = "CONDITIONAL_ATEMPORAL_STRUCTURAL_F1_RELATIVE_TO_IMPORTED_PRIMITIVES"

C0_SHA256 = "3E0EFB2D635E7E5605F9D7EDFA99538644D7C21311989C478C4A6AF1854890EB"
F2A_CONTRACT_SOURCE = "44ADB77E4B78D5D36E7F597C8401FD91A9E0DD0F0D86E20541F1EB790EF8308D"
W211_SOURCE = "B1BF8B9F21844B9AFC5EB5932A5B864C8DA253139FC7C55A5BCB9494ADB86786"
W212_SOURCE = "1F7F4FFE139F731D1D254BD48D11852E5C5ADA3298CEDC05FB6584B8923D8F9B"
F1_SOURCE = "8B29AF84AE0F94063CF0E7FDAB47A7CE364C7D6B1789D71051548A98A96C770E"

READY_STATUS = "W2_F2B_CONTRACT_READY_FOR_INDEPENDENT_REVIEW__NO_CANDIDATE_EVALUATED__FULL_F2_OPEN"
FROZEN_STATUS = "W2_F2B_CONTRACT_FROZEN__NO_CANDIDATE_EVALUATED__FULL_F2_OPEN"
INVALID_STATUS = "W2_F2B_CONTRACT_INVALID__NO_CANDIDATE_EVALUATION__FULL_F2_OPEN"
EXPECTED_PAYLOAD_SHA256 = "1B7D2921C78DB177CE401E04B5359ED28988DB2CF86E89A3159407BDF0B18733"
EXPECTED_VALIDATOR_SHA256 = "98F4A8B70742F9F709629486DC1D948BC22CAB12C74F7DBCA99E3B616FE3FC68"

ROOT = Path(__file__).resolve().parents[2]
C0_PATH = Path(__file__).with_name("w2_00_foundation_to_einstein_contract.md")
F2A_CONTRACT_PATH = Path(__file__).with_name(
    "w2_10_f2a_internal_operational_distinction_contract.py"
)
W211_PATH = Path(__file__).with_name("w2_11_f2_single_orbit_readout_no_go_gate.py")
W212_PATH = Path(__file__).with_name(
    "w2_12_f2_intrastate_uniform_effect_family_candidate_gate.py"
)
F1_PATH = Path(__file__).with_name("w2_09a_f1_proof") / "refg_f1_atemporal_structural_proof.py"

NEXT_ATOMIC_TASK = (
    "Create w2_14_f2b_single_generator_commutative_spectral_repackaging_gate.py: "
    "within the exact frozen F1+w2_12 single-generator commutative spectral class "
    "and without new primitives, test whether at least two state-supported internal "
    "nodes, an atemporal relational carrier and an irreducibly pairwise quotient "
    "invariant can be generated; accept either a scoped exact positive result or a "
    "scoped no-go that rejects only this declared class, preserve noncommuting, higher-"
    "variation and genuine joint-state routes, start candidate-evaluated false, and "
    "keep full W2_F2 false until a separately reviewed positive candidate closes every "
    "F2b subgate."
)

EXPECTED_STANDARD_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})
EXPECTED_CUSTOM_FIELDS = frozenset({
    "F2B_DEFINITION", "F2B_SUBGATE_REGISTRY", "CANDIDATE_SCREENING_GATES",
    "RUNTIME_CLOSURE_LOGIC", "WITNESS_ROUTES", "ROUTE_POLICY",
    "FORBIDDEN_INPUTS", "SCOPE_CEILING", "GATE_APPLICABILITY",
    "EXPORT_STATUS", "INDEPENDENT_REVIEW", "NEXT_TASK_POLICY",
    "NEXT_ATOMIC_TASK",
})

EXPECTED_C0_CLOSURE_FLAGS = {
    "W2_F1_SELF_DIFFERENTIATION": True,
    "W2_F2_OPERATIONAL_RELATIONS": False,
    "W2_F3_INTERNAL_ORDER_CAUSALITY": False,
    "W2_F4_INDEPENDENT_ADDITIVE_MODES": False,
    "W2_M1_DIMENSION_CONTINUUM": False,
    "W2_M2_LORENTZIAN_METRIC": False,
    "W2_A0_EFFECTIVE_ACTION_ORIGIN": False,
    "W2_A1_ACTION_VARIATION": False,
    "W2_A2_CONSERVATION_NO_DOUBLE_COUNT": False,
    "W2_A3_DOF_HEALTH": False,
    "W2_A4_UNIVERSAL_MATTER_METRIC": False,
    "W2_E1_REDUCED_ACTION_MATCHING": False,
    "W2_E2_EXACT_EINSTEIN_BRANCH": False,
    "W2_E3_SOURCE_WORLDTUBE_MATCHING": False,
    "W2_L1_WEAK_SOURCE_PN_PPN_HANDOFF": False,
    "W2_L2_COMPACT_SOURCE_EIH_HANDOFF": False,
}
EXPECTED_SCOPE_CEILING = {
    "f2b_candidate_evaluated": False,
    "state_supported_internal_node_family_proved": False,
    "atemporal_relational_carrier_proved": False,
    "irreducibly_pairwise_relation_proved": False,
    "same_chain_compatibility_proved": False,
    "full_W2_F2_operational_relations": False,
    "physical_node_or_location": False,
    "persistent_imprint_or_memory": False,
    "physical_coupling_response_or_intervention": False,
    "temporal_order_persistence_or_causality": False,
    "independent_additive_physical_modes": False,
    "physical_dimension_or_continuum": False,
    "Lorentzian_metric_or_light_cone": False,
    "effective_action_or_conservation_law": False,
    "RefG_environment_map": False,
    "mass_pressure_particle_or_oscillon": False,
    "GR_PN_or_PPN_bridge": False,
    "external_observable_or_data_map": False,
    "observational_validation": False,
}
EXPECTED_EXPORT_STATUS = {
    "CANON": False, "ARTICLE": False, "GITHUB": False, "ZENODO": False,
}
EXPECTED_DEFINITION_KEYS = frozenset({
    "subgate_boundary", "internal_node", "state_support", "atemporal_imprint",
    "pair_domain", "irreducible_relation", "invariance", "same_chain",
    "persistence_boundary", "full_f2_condition",
})
EXPECTED_SUBGATE_KEYS = frozenset({
    "inherited_f2a_internal_comparison", "state_supported_node_family",
    "atemporal_relational_carrier", "derived_pair_domain_and_common_action",
    "irreducibly_pairwise_relation", "complete_equivalence_invariance",
    "open_domain_and_required_nulls", "same_chain_compatibility",
    "relational_completion", "full_c0_f2",
})
EXPECTED_WITNESS_ROUTE_KEYS = frozenset({
    "INHERITED_F1_HESSIAN_ALGEBRA", "STATE_SUBOBJECT_INCIDENCE",
    "JOINT_STATE_CONNECTED_CARRIER", "LAW_DERIVED_MIXED_CARRIER",
    "OTHER_EXACT_ROUTE",
})
EXPECTED_ROUTE_POLICY_KEYS = frozenset({
    "candidate_route_must_be_explicit", "no_preferred_route",
    "listed_routes_exhaustive", "unlisted_route_allowed_if_all_gates_pass",
    "incompatible_cross_chain_stitching_allowed",
    "modular_subproofs_require_one_pinned_aggregate_candidate",
})
EXPECTED_ROUTE_POLICY = {
    "candidate_route_must_be_explicit": True,
    "no_preferred_route": True,
    "listed_routes_exhaustive": False,
    "unlisted_route_allowed_if_all_gates_pass": True,
    "incompatible_cross_chain_stitching_allowed": False,
    "modular_subproofs_require_one_pinned_aggregate_candidate": True,
}
EXPECTED_SCREENING_GATE_KEYS = frozenset({
    "exact_dependency_chain_valid",
    "same_chain_embedding_or_full_revalidation_exact",
    "candidate_domain_codomain_branches_and_undefined_points_explicit",
    "candidate_freedom_ledger_complete",
    "state_supported_node_family_generated_not_preassigned",
    "node_ownership_certificate_law_derived",
    "at_least_two_distinct_nodes_on_non_tuned_domain",
    "atemporal_relational_carrier_is_state_supported_not_readout_only",
    "carrier_connects_distinct_nodes_with_derived_restrictions",
    "joint_admissibility_composition_and_complete_common_action_derived",
    "uniform_target_free_pair_rule_and_shared_codomain",
    "complete_unary_reduction_maps_declared",
    "route_neutral_irreducibility_certificate_exact",
    "relation_not_factorable_through_unary_quotients",
    "nonzero_relational_quotient_on_predeclared_open_domain",
    "reported_relation_complete_equivalence_invariant",
    "independent_relabelling_and_factorized_pair_nulls_pass",
    "reference_single_node_and_degenerate_nulls_pass",
    "w2_12_diagonal_comparison_not_relabelled_as_pair_coupling",
    "f3_time_memory_persistence_and_causality_absent",
    "physical_spatial_geometric_and_observable_semantics_absent",
    "positive_null_adversarial_and_mutation_controls_pass",
    "candidate_specific_independent_audit_required",
})
EXPECTED_FREEDOM_KEYS = frozenset({
    "inherited_f1_parameters", "inherited_f2a_architecture",
    "candidate_route", "node_construction", "carrier_construction",
    "joint_composition_and_common_action", "pair_rule",
    "normalization_or_threshold", "candidate_specific_parameters",
    "preferred_labels_basis_or_axis", "future_candidate_internal_primitives",
    "new_physical_primitives",
    "data_fitted_parameters",
})
EXPECTED_FREEDOM_ENTRY_KEYS = frozenset({
    "source", "allowed_range", "scale", "complexity",
})
EXPECTED_GATE_KEYS = frozenset({
    "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
    "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
    "G7_OBSERVATION", "G8_EXPORT",
})
EXPECTED_REVIEW_KEYS = frozenset({
    "semantic_contract_review", "fail_closed_code_review", "new_reader_scope_review",
})
EXPECTED_REVIEW_REQUIREMENTS = {
    "semantic_contract_review": "independent F2b definition and full-F2 closure audit",
    "fail_closed_code_review": "independent screening, closure and adversarial-code audit",
    "new_reader_scope_review": "independent provenance, standalone clarity and scope audit",
}
EXPECTED_SCREEN_CONTROL_KEYS = frozenset({
    "all_true_only_eligible_never_promoted", "one_false_not_eligible",
    "every_missing_gate_invalid", "every_nonboolean_gate_invalid",
    "extra_gate_invalid", "invalid_audit_never_eligible",
    "nonboolean_audit_invalid",
})
EXPECTED_COMPLETION_CONTROL_KEYS = frozenset({
    "all_true_closes_f2b_and_full_f2", "f2a_false_keeps_full_f2_open",
    "every_f2b_component_is_independently_necessary",
    "every_nonboolean_input_invalid", "contract_inputs_never_close_candidate_or_full_f2",
    "screen_ineligible_keeps_completion_open",
})
EXPECTED_SYNTHETIC_CONTROL_KEYS = frozenset({
    "same_unary_different_joint_positive_witness_detected",
    "factorized_unary_equality_null_detected",
    "w2_12_diagonal_form_classified_as_f2a_only",
    "synthetic_control_never_promotes_refg",
})
EXPECTED_MUTATION_KEYS = frozenset({
    "missing_or_extra_contract_fields_rejected", "registry_drift_rejected",
    "closure_scope_export_overclaims_rejected", "semantic_overclaims_rejected",
    "target_and_cross_chain_injections_rejected", "screen_schema_mutants_rejected",
    "false_positive_route_profiles_not_eligible",
})
EXPECTED_AUDIT_KEYS = frozenset({
    "payload_validator_and_contract_schema_exact",
    "c0_f2a_w211_w212_f1_dependencies_exact",
    "screening_and_completion_decision_controls_exact",
    "synthetic_positive_and_required_null_controls_exact",
    "mutation_controls_exact", "candidate_neutrality_and_no_evaluation_exact",
    "closure_scope_export_boundaries_exact", "review_schema_fail_closed",
    "review_attestations_complete", "next_task_is_neutral_sufficiency_gate",
})

REVIEW_ATTESTED_PAYLOAD_IDS = {
    "semantic_contract_review": "1B7D2921C78DB177CE401E04B5359ED28988DB2CF86E89A3159407BDF0B18733",
    "fail_closed_code_review": "1B7D2921C78DB177CE401E04B5359ED28988DB2CF86E89A3159407BDF0B18733",
    "new_reader_scope_review": "1B7D2921C78DB177CE401E04B5359ED28988DB2CF86E89A3159407BDF0B18733",
}
REVIEW_ATTESTED_VALIDATOR_IDS = {
    "semantic_contract_review": "98F4A8B70742F9F709629486DC1D948BC22CAB12C74F7DBCA99E3B616FE3FC68",
    "fail_closed_code_review": "98F4A8B70742F9F709629486DC1D948BC22CAB12C74F7DBCA99E3B616FE3FC68",
    "new_reader_scope_review": "98F4A8B70742F9F709629486DC1D948BC22CAB12C74F7DBCA99E3B616FE3FC68",
}


def f2b_definition() -> dict[str, str]:
    return {
        "subgate_boundary": (
            "F2a's exact atemporal comparison is inherited but does not supply nodes, a "
            "state-supported carrier, irreducible pair content, or full C0 F2."
        ),
        "internal_node": (
            "A node is a state/law-generated internal relatum with nonzero support in the same "
            "accepted state and quotient-covariant identity.  Ownership must have one registered "
            "exact certificate: equivariant restriction/support, embedding/reconstruction, a "
            "state-owned constraint/fibre, or incidence/assembly where that structure is used.  "
            "A node is not a spatial point, label, rank, basis vector or tangent diagnostic."
        ),
        "state_support": (
            "State support requires an explicit equivariant state/law map, exact node and carrier "
            "support or restriction maps, collapse on the declared reference null, and a nonzero "
            "relational quotient on the accepted domain; the word belongs is not evidence."
        ),
        "atemporal_imprint": (
            "Imprint means relational information present in one accepted state.  It is not "
            "memory, survival, a historical record, lag, hysteresis or persistence."
        ),
        "pair_domain": (
            "At least two simultaneous nodes, admissible ordered or unordered pairs, composition "
            "where used, and the complete common action must be derived before outcomes."
        ),
        "irreducible_relation": (
            "Freeze a declared candidate-relative function class and prove complete within that "
            "class the image of unary marginals, bare or preloaded equality, and separable rules; "
            "then prove a nonzero relation class modulo that null.  A same-unary/different-joint "
            "witness, a nonzero connected quotient, or another registered exact no-factorization "
            "certificate may suffice.  Coordinate off-diagonality or diagonality alone is neither "
            "a witness nor a null; w2_12 fails only because delta_ab mu_a is reconstructible from "
            "unary weights and bare spectral equality."
        ),
        "invariance": (
            "Carrier representatives may transform covariantly, but the reported joint relation "
            "must survive the complete declared equivalence and node relabelling."
        ),
        "same_chain": (
            "F2b must extend the exact same F1-to-F2a theory by a proved embedding/restriction, or "
            "the new version must revalidate F1 and F2a.  Modular subproof artifacts are allowed "
            "only inside one identity-pinned aggregate candidate that jointly revalidates every "
            "subgate; incompatible witnesses cannot be stitched."
        ),
        "persistence_boundary": (
            "Formation, memory, persistence, decay, causal direction, propagation, intervention "
            "and no-signalling belong only to F3 or later gates."
        ),
        "full_f2_condition": (
            "Full C0 F2 requires inherited F2a plus state-supported nodes, atemporal carrier, "
            "a derived pair domain and complete common action, an irreducible pair relation, "
            "complete invariance, nonzero open-domain support with required nulls, and same-chain "
            "compatibility, all in one identity-pinned and separately audited aggregate candidate."
        ),
    }


def subgate_registry() -> dict[str, str]:
    return {
        "inherited_f2a_internal_comparison": "PROVED_BY_EXACT_W2_12_DEPENDENCY",
        "state_supported_node_family": "OPEN_UNEVALUATED",
        "atemporal_relational_carrier": "OPEN_UNEVALUATED",
        "derived_pair_domain_and_common_action": "OPEN_UNEVALUATED",
        "irreducibly_pairwise_relation": "OPEN_UNEVALUATED",
        "complete_equivalence_invariance": "OPEN_UNEVALUATED",
        "open_domain_and_required_nulls": "OPEN_UNEVALUATED",
        "same_chain_compatibility": "OPEN_UNEVALUATED",
        "relational_completion": "OPEN_UNEVALUATED",
        "full_c0_f2": "OPEN_UNEVALUATED",
    }


def witness_routes() -> dict[str, str]:
    return {
        "INHERITED_F1_HESSIAN_ALGEBRA": (
            "Test the inherited algebra without new primitives; it may yield a scoped positive "
            "result or a scoped single-generator no-go."
        ),
        "STATE_SUBOBJECT_INCIDENCE": (
            "The accepted state derives supported subobjects and an intrinsic incidence/composition "
            "carrier whose joint quotient exceeds all unary reductions."
        ),
        "JOINT_STATE_CONNECTED_CARRIER": (
            "A derived joint-state carrier has fixed unary reductions but a nonzero connected or "
            "nonseparable relational quotient."
        ),
        "LAW_DERIVED_MIXED_CARRIER": (
            "A law-derived mixed carrier has exact cross-support on generated nodes without being "
            "a free adjacency, target table or physical interaction claim."
        ),
        "OTHER_EXACT_ROUTE": "Any unlisted candidate is allowed only if every frozen gate passes.",
    }


def candidate_screening_gates() -> dict[str, str]:
    descriptions = {
        "exact_dependency_chain_valid": "Exact C0, F1, F2a and no-go dependencies are valid.",
        "same_chain_embedding_or_full_revalidation_exact": (
            "The candidate extends the same theory chain or revalidates every inherited gate."
        ),
        "candidate_domain_codomain_branches_and_undefined_points_explicit": (
            "State, node, carrier, pair and report domains, branches and undefined points are fixed."
        ),
        "candidate_freedom_ledger_complete": "Every new object, map, parameter and choice is charged.",
        "state_supported_node_family_generated_not_preassigned": (
            "At least two same-state nodes are generated rather than named, copied or indexed."
        ),
        "node_ownership_certificate_law_derived": (
            "One registered route-neutral ownership certificate and every map it uses are exact, "
            "equivariant and law-derived; incidence or assembly is required only where used."
        ),
        "at_least_two_distinct_nodes_on_non_tuned_domain": (
            "Invariant node plurality persists on a declared open non-tuned domain."
        ),
        "atemporal_relational_carrier_is_state_supported_not_readout_only": (
            "The carrier belongs to the admissible state and is not only a diagnostic operator/table."
        ),
        "carrier_connects_distinct_nodes_with_derived_restrictions": (
            "The carrier has derived support on admissible distinct-node pairs."
        ),
        "joint_admissibility_composition_and_complete_common_action_derived": (
            "Multiplicity, joint admissibility, composition where used, and the complete common "
            "action are derived."
        ),
        "uniform_target_free_pair_rule_and_shared_codomain": (
            "One target-free pair rule and codomain are frozen before pair outcomes."
        ),
        "complete_unary_reduction_maps_declared": (
            "The candidate-relative function class is declared and its unary, bare-equality, rank, "
            "type and separable reconstruction image is proved complete within that class."
        ),
        "route_neutral_irreducibility_certificate_exact": (
            "A registered exact certificate is supplied: same-complete-unary/different-joint, "
            "nonzero connected quotient, invariant mixed nonadditivity, or another proved "
            "no-factorization route."
        ),
        "relation_not_factorable_through_unary_quotients": (
            "The reported relation has a nonzero quotient outside the complete unary/trivial class."
        ),
        "nonzero_relational_quotient_on_predeclared_open_domain": (
            "The nonzero quotient persists on a predeclared nonempty open domain with regular "
            "normalization or threshold; isolated, tuned, singular and post-selected points fail."
        ),
        "reported_relation_complete_equivalence_invariant": (
            "The report is exact under the complete equivalence and node relabelling."
        ),
        "independent_relabelling_and_factorized_pair_nulls_pass": (
            "Independent-action, equality, additive, separable and self-selector nulls pass."
        ),
        "reference_single_node_and_degenerate_nulls_pass": (
            "Undifferentiated, one-node, tuned, singular and rejected branches do not promote."
        ),
        "w2_12_diagonal_comparison_not_relabelled_as_pair_coupling": (
            "The inherited delta_ab mu_a table supplies no F2b relation because it reconstructs "
            "from unary weights plus bare equality, not merely because it is diagonal."
        ),
        "f3_time_memory_persistence_and_causality_absent": (
            "No history, update, lag, memory, persistence, causal direction or intervention is imported."
        ),
        "physical_spatial_geometric_and_observable_semantics_absent": (
            "No physical location, mode, geometry, metric, observable, data or measurement is claimed."
        ),
        "positive_null_adversarial_and_mutation_controls_pass": (
            "Synthetic satisfiability, route-specific nulls and adversarial mutations pass exactly."
        ),
        "candidate_specific_independent_audit_required": (
            "A separate frozen candidate module and three independent reviews are mandatory."
        ),
    }
    if set(descriptions) != EXPECTED_SCREENING_GATE_KEYS:
        raise RuntimeError("screening-gate registry drift")
    return descriptions


def freedom_ledger() -> dict[str, dict[str, Any]]:
    unselected = {
        "source": "unselected at contract level; candidate must replace this entry",
        "allowed_range": "no candidate value admitted by this contract",
        "scale": "architecture", "complexity": 0,
    }
    zero = {"source": "none", "allowed_range": 0, "scale": "contract", "complexity": 0}
    return {
        "inherited_f1_parameters": {
            "source": "public F1 alpha,b,c", "allowed_range": "alpha,b,c>0",
            "scale": "three inherited, already charged, non-fitted parameters", "complexity": 3,
        },
        "inherited_f2a_architecture": {
            "source": "exact w2_12 Hessian route and normalization",
            "allowed_range": "pinned dependency; no new choice here",
            "scale": "inherited architecture", "complexity": 0,
        },
        "candidate_route": dict(unselected),
        "node_construction": dict(unselected),
        "carrier_construction": dict(unselected),
        "joint_composition_and_common_action": dict(unselected),
        "pair_rule": dict(unselected),
        "normalization_or_threshold": dict(unselected),
        "candidate_specific_parameters": dict(unselected),
        "preferred_labels_basis_or_axis": {**zero, "scale": "description"},
        "future_candidate_internal_primitives": {
            "source": (
                "none introduced by w2_13; any future internal primitive requires a new "
                "version, explicit ledger and full inherited-chain revalidation"
            ),
            "allowed_range": "unselected at contract level; never hidden or retrofitted",
            "scale": "candidate architecture", "complexity": 0,
        },
        "new_physical_primitives": {
            **zero,
            "allowed_range": "prohibited at internal F2; no physical semantics admitted",
            "scale": "foundation",
        },
        "data_fitted_parameters": {**zero, "scale": "data"},
    }


def forbidden_inputs() -> tuple[str, ...]:
    return (
        "preassigned node, index, container slot, multiplicity, physical point or location",
        "fixed labels, axis, basis, split, representative entry, eigenvector or gauge tangent",
        "projector, rank, type, sign copy, complement or Hessian sector merely renamed a node",
        "diagnostic operator, scalar or table merely renamed a state-supported imprint",
        "desired pair table, target relation, free adjacency, incidence, distance or pair weight",
        "per-pair selector, self-test, bare equality, overlap, count, additive or separable unary table",
        "unregistered product, tensor factor, ensemble, pair state, composition or common action",
        "F2a and F2b witnesses stitched from incompatible theory versions or parameter fibres",
        "tuned point, singular normalization, rejected branch, origin division or finite tolerance",
        "history, update order, cache, lag, memory, hysteresis, retarded kernel or persistence",
        "causal arrow, intervention, signal, physical mode, geometry, metric, action, GR or observable",
        "external apparatus, data, benchmark answer, fitted relation or post-selected successful pair",
    )


def gate_applicability() -> dict[str, str]:
    return {
        "G0_GOAL": "REQUIRED - remaining F2 obligations and full-F2 ceiling frozen",
        "G1_CONVENTIONS": "REQUIRED - node, state support, imprint and irreducibility fixed",
        "G2_CORE_ALGEBRA": "REQUIRED - exact screen and full-F2 AND logic",
        "G3_STRUCTURE": "REQUIRED - same-chain, ownership and unary-quotient exclusions",
        "G4_INDEPENDENT_CHECK": "REQUIRED - semantic, fail-closed and new-reader reviews",
        "G5_LIMITS_REGRESSION": "REQUIRED - reference, factorized, gauge, tuned and temporal nulls",
        "G6_PHYSICAL_MATCH": "N/A - internal atemporal relation only; no physical location or coupling",
        "G7_OBSERVATION": "N/A - no observable, forward model or data",
        "G8_EXPORT": "N/A - internal contract; no Canon, article, GitHub or Zenodo export",
    }


def review_attestations() -> dict[str, dict[str, Any]]:
    return {
        "semantic_contract_review": {
            "passed": True,
            "reviewer": "/root/f2_independent_review",
            "artifact": EXPECTED_REVIEW_REQUIREMENTS["semantic_contract_review"],
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS["semantic_contract_review"],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS["semantic_contract_review"],
        },
        "fail_closed_code_review": {
            "passed": True,
            "reviewer": "/root/w209_no_go",
            "artifact": EXPECTED_REVIEW_REQUIREMENTS["fail_closed_code_review"],
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS["fail_closed_code_review"],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS["fail_closed_code_review"],
        },
        "new_reader_scope_review": {
            "passed": True,
            "reviewer": "/root/f2_contract_map",
            "artifact": EXPECTED_REVIEW_REQUIREMENTS["new_reader_scope_review"],
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS["new_reader_scope_review"],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS["new_reader_scope_review"],
        },
    }


def build_contract() -> dict[str, Any]:
    return {
        "CLAIM_ID": "W2_F2B_NODE_IMPRINT_RELATIONAL_COMPLETION_CONTRACT_001",
        "CLAIM": (
            "Freeze a candidate-neutral completion contract for state-supported internal nodes, "
            "an atemporal relational/imprint carrier, irreducibly pairwise quotient content, "
            "complete invariance and same-chain compatibility; evaluate no candidate and do not "
            "close full C0 W2_F2."
        ),
        "TYPE": "DEFINITIONAL_SUBGATE_CONTRACT_WITH_FAIL_CLOSED_SCREENING_AND_CLOSURE_LOGIC",
        "MODEL_VERSION": MODEL_VERSION,
        "ASSUMPTIONS": (
            "The frozen W2-C0 contract governs this public runtime audit; private governance "
            "rules remain provenance and are not required to execute it.",
            "The exact public F1 result, frozen F2a contract and w2_11 no-go remain valid.",
            "The exact w2_12 result proves only a law-defined atemporal F2a comparison on its "
            "generic domain; its factorized diagonal report is not F2b pair content.",
            "The C0 frozen header and PASS_FOR_W2_C0_FREEZE are operative; the older section-3 "
            "sentence saying the freeze audit is OPEN is stale and supplies no premise.",
            "Persistence, memory and directed influence belong to F3, not this contract."
        ),
        "DOMAIN": (
            "Atemporal F2b candidates extending the exact F1-to-w2_12 theory chain, or a new "
            "version that revalidates that chain.  Physical locations, histories, dynamics, time, "
            "causality, geometry, observables and data are excluded."
        ),
        "CONVENTIONS": (
            "Node means generated internal state-supported relatum, never spatial point.  Imprint "
            "means atemporal joint correlation carrier, never memory.  Irreducible means outside "
            "the proved complete candidate-relative unary/bare-equality/separable null quotient.  "
            "Diagonality alone decides nothing.  Computational order is not time and only "
            "complete-equivalence-invariant reports count."
        ),
        "FREEDOM_LEDGER": freedom_ledger(),
        "DEPENDENCIES": {
            "research_rules": (
                "frozen W2-C0 exact runtime identity; private governance is not a runtime file"
            ),
            "programme_contract": PROGRAM_CONTRACT,
            "frozen_f2a_contract": F2A_CONTRACT_MODEL,
            "single_orbit_no_go": W211_MODEL,
            "proved_f2a_candidate": W212_MODEL,
            "conditional_public_f1": F1_MODEL,
            "c0_status_resolution": (
                "frozen header and PASS audit operative; older section-3 OPEN sentence stale"
            ),
        },
        "METHOD": (
            "Freeze exact definitions, 23 candidate gates, full-F2 boolean conjunction, witness "
            "routes, nulls, freedom accounting, mutation controls and detached reviews without "
            "choosing or evaluating candidate algebra."
        ),
        "PASS_CONDITION": (
            "Exact payload and validator identities, pinned dependencies, complete registries, "
            "screen and closure truth tables, synthetic satisfiability and null controls, all "
            "mutations and three detached reviews pass.  PASS freezes only this contract."
        ),
        "FAIL_CONDITION": (
            "Any dependency/schema drift, hidden freedom, partial-gate promotion, F2a-to-F2b "
            "relabel, cross-version stitching, temporal leak, overclaim, malformed boolean or "
            "incomplete review invalidates the contract."
        ),
        "FALSIFIER": (
            "A malformed or partial candidate becomes eligible, a contract mutation evaluates a "
            "candidate or closes full F2, or labels/unary factorization/readout-only content can "
            "satisfy the frozen F2b screen."
        ),
        "RESIDUAL": "0 for exact schema and boolean identities; candidate scientific residual is N/A.",
        "ERROR_BOUND": "0 for exact discrete controls; candidate numerical and data errors are N/A.",
        "VALIDITY_HEALTH": (
            "Contract-only and valid relative to pinned dependencies.  It proves no candidate, "
            "physical degrees of freedom, stability, dynamics, conservation, causality or observation."
        ),
        "BRANCHES": {
            "contract_only": "FROZEN_IF_AUDITED__NO_CANDIDATE_EVALUATED",
            "inherited_f1_hessian_algebra": "OPEN_UNEVALUATED",
            "state_subobject_incidence": "OPEN_UNEVALUATED",
            "joint_state_connected_carrier": "OPEN_UNEVALUATED",
            "law_derived_mixed_carrier": "OPEN_UNEVALUATED",
            "unlisted_exact_route": "OPEN_IF_ALL_GATES_PASS",
            "w2_12_diagonal_comparison": "RETAINED_AS_F2A__NOT_F2B",
            "temporal_memory_route": "EXCLUDED_TO_F3",
            "full_c0_f2": "OPEN",
        },
        "OBSERVABLE_MAP": {"status": "N/A", "reason": "internal atemporal contract only"},
        "FORWARD_MODEL": {"status": "N/A", "reason": "no observable or data chain"},
        "DATA_ROLE": {"status": "N/A", "reason": "no data, fit, validation or prediction"},
        "IDENTIFIABILITY": (
            "A candidate must freeze complete equivalence, node permutation action, all unary "
            "reductions and the pair report, then prove a nonzero joint quotient.  Physical "
            "identifiability is N/A."
        ),
        "BENCHMARK": (
            "Nulls are reference/one-node states, factorized unary pairs, independent relabelling, "
            "bare equality/rank/count, readout-only functionals, the w2_12 diagonal table, free "
            "targets, incompatible-chain stitching and temporal leakage."
        ),
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "CROSSCHECK": (
            "Exact schema enumeration, screening truth table, full-F2 conjunction truth table, "
            "synthetic same-unary/different-joint control, dependency rerun, mutation families and "
            "three independent reviews."
        ),
        "PROVENANCE": {
            "date": "2026-07-21",
            "reviewed_payload_sha256": EXPECTED_PAYLOAD_SHA256,
            "source_identities": {
                "w2_00": C0_SHA256,
                "w2_10": F2A_CONTRACT_SOURCE,
                "w2_11": W211_SOURCE,
                "w2_12": W212_SOURCE,
                "public_f1": F1_SOURCE,
            },
            "output_artifact": (
                "RefG/work 2/w2_13_f2b_node_imprint_and_relational_completion_contract.py"
            ),
        },
        "FILES": (
            "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
            "RefG/work 2/w2_10_f2a_internal_operational_distinction_contract.py",
            "RefG/work 2/w2_11_f2_single_orbit_readout_no_go_gate.py",
            "RefG/work 2/w2_12_f2_intrastate_uniform_effect_family_candidate_gate.py",
            "RefG/work 2/w2_09a_f1_proof/refg_f1_atemporal_structural_proof.py",
            "RefG/work 2/w2_13_f2b_node_imprint_and_relational_completion_contract.py",
        ),
        "F2B_DEFINITION": f2b_definition(),
        "F2B_SUBGATE_REGISTRY": subgate_registry(),
        "CANDIDATE_SCREENING_GATES": candidate_screening_gates(),
        "RUNTIME_CLOSURE_LOGIC": {
            "f2b": (
                "candidate_audit_valid AND screen_eligible AND candidate_evaluated AND "
                "state_supported_node_family AND atemporal_relational_carrier AND "
                "derived_pair_domain_and_common_action AND irreducibly_pairwise_relation AND "
                "complete_equivalence_invariance AND open_domain_and_required_nulls AND "
                "same_chain_compatibility"
            ),
            "full_f2": "inherited_f2a_internal_comparison AND f2b",
            "contract_rule": (
                "This contract supplies no candidate inputs and cannot set f2b or full_f2 true.  "
                "Modular evidence counts only through one identity-pinned aggregate candidate."
            ),
        },
        "WITNESS_ROUTES": witness_routes(),
        "ROUTE_POLICY": dict(EXPECTED_ROUTE_POLICY),
        "FORBIDDEN_INPUTS": forbidden_inputs(),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "GATE_APPLICABILITY": gate_applicability(),
        "EXPORT_STATUS": dict(EXPECTED_EXPORT_STATUS),
        "INDEPENDENT_REVIEW": dict(EXPECTED_REVIEW_REQUIREMENTS),
        "NEXT_TASK_POLICY": {
            "frozen": NEXT_ATOMIC_TASK,
            "pending": "Complete exact independent reviews before any downstream task.",
            "invalid": "Restore the exact w2_13 contract before any downstream task.",
        },
        "NEXT_ATOMIC_TASK": NEXT_ATOMIC_TASK,
    }


CLAIM_CONTRACT = build_contract()


def exact_tree_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            exact_tree_equal(left[key], right[key]) for key in left
        )
    if isinstance(left, (tuple, list)):
        return len(left) == len(right) and all(
            exact_tree_equal(a, b) for a, b in zip(left, right)
        )
    return bool(left == right)


def exact_bool_map(actual: Any, expected: dict[str, bool]) -> bool:
    return bool(
        isinstance(actual, dict)
        and set(actual) == set(expected)
        and all(type(actual[key]) is bool for key in expected)
        and all(actual[key] is expected[key] for key in expected)
    )


def exact_true_map(actual: Any, keys: frozenset[str]) -> bool:
    return bool(
        isinstance(actual, dict)
        and set(actual) == set(keys)
        and all(type(actual[key]) is bool and actual[key] is True for key in keys)
    )


def detached_payload_sha256(contract: Any) -> str:
    if not isinstance(contract, dict) or not isinstance(contract.get("PROVENANCE"), dict):
        return ""
    if "reviewed_payload_sha256" not in contract["PROVENANCE"]:
        return ""
    try:
        payload = copy.deepcopy(contract)
        payload["PROVENANCE"]["reviewed_payload_sha256"] = "<DETACHED_PAYLOAD_ID>"
        canonical = json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
        )
    except Exception:
        return ""
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()


def detached_validator_sha256() -> str:
    try:
        source = Path(__file__).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""
    source, count = re.subn(
        r'^EXPECTED_VALIDATOR_SHA256 = "[^"]*"$',
        'EXPECTED_VALIDATOR_SHA256 = "<DETACHED_VALIDATOR_ID>"',
        source, count=1, flags=re.MULTILINE,
    )
    pattern = re.compile(
        r'^REVIEW_ATTESTED_VALIDATOR_IDS = \{.*?^\}\r?\n',
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(source)
    if count != 1 or match is None:
        return ""
    normalized = re.sub(
        r'"(?:[A-F0-9]{64}|PENDING)"', '"<ATTESTED_VALIDATOR_ID>"', match.group(0)
    )
    source = source[:match.start()] + normalized + source[match.end():]
    source, verdicts = re.subn(
        r'("passed":\s*)(?:True|False)', r'\1<DETACHED_REVIEW_VERDICT>', source,
    )
    if verdicts != len(EXPECTED_REVIEW_KEYS):
        return ""
    return hashlib.sha256(source.encode("utf-8")).hexdigest().upper()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def registry_shapes_valid(contract: dict[str, Any]) -> bool:
    freedom = contract.get("FREEDOM_LEDGER")
    return all((
        set(contract) == EXPECTED_STANDARD_FIELDS | EXPECTED_CUSTOM_FIELDS,
        set(contract.get("F2B_DEFINITION", {})) == EXPECTED_DEFINITION_KEYS,
        set(contract.get("F2B_SUBGATE_REGISTRY", {})) == EXPECTED_SUBGATE_KEYS,
        set(contract.get("CANDIDATE_SCREENING_GATES", {})) == EXPECTED_SCREENING_GATE_KEYS,
        set(contract.get("RUNTIME_CLOSURE_LOGIC", {})) == {"f2b", "full_f2", "contract_rule"},
        set(contract.get("WITNESS_ROUTES", {})) == EXPECTED_WITNESS_ROUTE_KEYS,
        exact_bool_map(contract.get("ROUTE_POLICY"), EXPECTED_ROUTE_POLICY),
        exact_tree_equal(contract.get("FORBIDDEN_INPUTS"), forbidden_inputs()),
        isinstance(freedom, dict) and set(freedom) == EXPECTED_FREEDOM_KEYS,
        isinstance(freedom, dict) and all(
            isinstance(value, dict) and set(value) == EXPECTED_FREEDOM_ENTRY_KEYS
            for value in freedom.values()
        ),
        exact_bool_map(contract.get("CLOSURE_FLAGS"), EXPECTED_C0_CLOSURE_FLAGS),
        exact_bool_map(contract.get("SCOPE_CEILING"), EXPECTED_SCOPE_CEILING),
        set(contract.get("GATE_APPLICABILITY", {})) == EXPECTED_GATE_KEYS,
        exact_bool_map(contract.get("EXPORT_STATUS"), EXPECTED_EXPORT_STATUS),
        exact_tree_equal(contract.get("INDEPENDENT_REVIEW"), EXPECTED_REVIEW_REQUIREMENTS),
        set(contract.get("NEXT_TASK_POLICY", {})) == {"frozen", "pending", "invalid"},
    ))


def semantic_guard(contract: dict[str, Any]) -> bool:
    try:
        fields = (
            contract["CLAIM"], contract["DOMAIN"], contract["METHOD"],
            contract["PASS_CONDITION"], contract["VALIDITY_HEALTH"],
            contract["BRANCHES"], contract["F2B_DEFINITION"],
            contract["F2B_SUBGATE_REGISTRY"], contract["RUNTIME_CLOSURE_LOGIC"],
            contract["WITNESS_ROUTES"], contract["SCOPE_CEILING"],
            contract["NEXT_TASK_POLICY"], contract["NEXT_ATOMIC_TASK"],
        )
        corpus = "\n".join(
            json.dumps(field, ensure_ascii=False, sort_keys=True)
            if not isinstance(field, str) else field
            for field in fields
        ).lower()
    except (KeyError, TypeError, ValueError):
        return False
    forbidden = (
        "closes full f2", "candidate is evaluated", "physical location is proved",
        "persistent imprint is proved", "time emerges", "causality emerges",
        "gr is derived", "observationally validated",
    )
    return not any(token in corpus for token in forbidden)


def strict_contract_valid(contract: Any) -> bool:
    return bool(
        isinstance(contract, dict)
        and exact_tree_equal(contract, build_contract())
        and registry_shapes_valid(contract)
        and contract["MODEL_VERSION"] == MODEL_VERSION
        and contract["PROVENANCE"]["reviewed_payload_sha256"] == EXPECTED_PAYLOAD_SHA256
        and detached_payload_sha256(contract) == EXPECTED_PAYLOAD_SHA256
        and semantic_guard(contract)
    )


def dependencies_valid() -> tuple[bool, dict[str, Any]]:
    paths = (
        C0_PATH, F2A_CONTRACT_PATH, W211_PATH, W212_PATH, F1_PATH,
    )
    if not all(path.is_file() for path in paths):
        return False, {}
    try:
        c0_text = C0_PATH.read_text(encoding="utf-8")
        f2a_contract = load_module(F2A_CONTRACT_PATH, "refg_f2a_contract_for_w213")
        w211 = load_module(W211_PATH, "refg_w211_for_w213")
        w212 = load_module(W212_PATH, "refg_w212_for_w213")
        f1 = load_module(F1_PATH, "refg_f1_for_w213")
        w212_report = w212.run_audit()
    except Exception:
        return False, {}

    w212_reviews = w212_report.get("INDEPENDENT_REVIEW_ATTESTATIONS", {})
    w212_gates = w212_report.get("CANDIDATE_GATE_MAP", {})
    w212_subgates = w212_report.get("SUBGATE_CLOSURE_FLAGS", {})
    expected_w212_reviews = {
        "semantic_candidate_review", "fail_closed_code_review", "new_reader_scope_review",
    }
    expected_imports = {
        "single_internal_carrier_Q", "Sym0_3_R_internal_state_space",
        "positive_internal_contraction_and_transpose",
        "matrix_product_and_algebraic_trace",
        "O3_conjugation_as_complete_declared_equivalence", "Q_sign_not_gauge",
        "quartic_functional_form_signs_and_truncation",
        "open_parameter_domain_alpha_b_c_positive", "atemporal_global_argmin_rule",
    }
    exact_files = CLAIM_CONTRACT["FILES"]
    checks = all((
        C0_PATH.relative_to(ROOT).as_posix() == exact_files[0],
        F2A_CONTRACT_PATH.relative_to(ROOT).as_posix() == exact_files[1],
        W211_PATH.relative_to(ROOT).as_posix() == exact_files[2],
        W212_PATH.relative_to(ROOT).as_posix() == exact_files[3],
        F1_PATH.relative_to(ROOT).as_posix() == exact_files[4],
        Path(__file__).resolve().relative_to(ROOT).as_posix() == exact_files[5],
        file_sha256(C0_PATH) == C0_SHA256,
        file_sha256(F2A_CONTRACT_PATH) == F2A_CONTRACT_SOURCE,
        file_sha256(W211_PATH) == W211_SOURCE,
        file_sha256(W212_PATH) == W212_SOURCE,
        file_sha256(F1_PATH) == F1_SOURCE,
        f"`{PROGRAM_CONTRACT}`" in c0_text,
        "### `W2_F2_OPERATIONAL_RELATIONS`" in c0_text,
        "PASS_FOR_W2_C0_FREEZE" in c0_text,
        f2a_contract.MODEL_VERSION == F2A_CONTRACT_MODEL,
        f2a_contract.FROZEN_STATUS == F2A_CONTRACT_STATUS,
        f2a_contract.EXPECTED_PAYLOAD_SHA256 == F2A_CONTRACT_PAYLOAD,
        f2a_contract.EXPECTED_VALIDATOR_SHA256 == F2A_CONTRACT_VALIDATOR,
        w211.MODEL_VERSION == W211_MODEL,
        w211.PASS_STATUS == W211_STATUS,
        w211.EXPECTED_PAYLOAD_SHA256 == W211_PAYLOAD,
        w211.EXPECTED_VALIDATOR_SHA256 == W211_VALIDATOR,
        w212.MODEL_VERSION == W212_MODEL,
        w212_report.get("STATUS") == W212_STATUS,
        w212_report.get("AUDIT_VALID") is True,
        w212_report.get("CANDIDATE_EVALUATED") is True,
        w212_report.get("F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED") is True,
        w212_report.get("PROMOTED_TO_F2A") is True,
        w212_report.get("PROMOTED_BEYOND_F2A") is False,
        w212_report.get("FULL_W2_F2_OPERATIONAL_RELATIONS") is False,
        w212_report.get("DETACHED_PAYLOAD_SHA256") == W212_PAYLOAD,
        w212_report.get("DETACHED_VALIDATOR_SHA256") == W212_VALIDATOR,
        w212_subgates.get("W2_F2A_INTRASTATE_HESSIAN_COMPARISON_PROVED") is True,
        w212_subgates.get("W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED") is True,
        w212_subgates.get("W2_F2A_IRREDUCIBLY_PAIRWISE_COUPLING_PROVED") is False,
        isinstance(w212_gates, dict),
        len(w212_gates) == 19,
        all(type(value) is bool and value is True for value in w212_gates.values()),
        set(w212_reviews) == expected_w212_reviews,
        all(
            isinstance(entry, dict) and entry.get("passed") is True
            for entry in w212_reviews.values()
        ),
        w212_report.get("CLOSURE_FLAGS") == EXPECTED_C0_CLOSURE_FLAGS,
        "w2_13_f2b_node_imprint_and_relational_completion_contract.py"
        in w212_report.get("NEXT_ATOMIC_TASK", ""),
        f1.MODEL_VERSION == F1_MODEL,
        f1.PASS_STATUS == F1_STATUS,
        set(f1.IMPORTED_PRIMITIVES) == expected_imports,
    ))
    return bool(checks), {
        "f2a_contract_module": f2a_contract,
        "w211_module": w211,
        "w212_module": w212,
        "w212_report": w212_report,
        "f1_module": f1,
    }


def screening_gate_keys() -> frozenset[str]:
    return EXPECTED_SCREENING_GATE_KEYS


def screen_candidate(gates: Any, candidate_audit_valid: Any) -> dict[str, Any]:
    audit_boolean = type(candidate_audit_valid) is bool
    gates_valid = bool(
        isinstance(gates, dict)
        and set(gates) == EXPECTED_SCREENING_GATE_KEYS
        and all(type(gates[key]) is bool for key in EXPECTED_SCREENING_GATE_KEYS)
    )
    valid = bool(audit_boolean and gates_valid)
    eligible = bool(
        valid
        and candidate_audit_valid is True
        and all(gates[key] is True for key in EXPECTED_SCREENING_GATE_KEYS)
    )
    return {
        "VALID": valid,
        "ELIGIBLE": eligible,
        "PROMOTED": False,
        "STATUS": (
            "ELIGIBLE_FOR_SEPARATE_F2B_COMPLETION_DECISION__NOT_PROMOTED"
            if eligible else
            "VALID_NOT_ELIGIBLE__NOT_PROMOTED" if valid else
            "INVALID_SCREEN__NO_ELIGIBILITY_OR_PROMOTION"
        ),
    }


def screening_controls() -> dict[str, bool]:
    all_true = {key: True for key in EXPECTED_SCREENING_GATE_KEYS}
    all_true_result = screen_candidate(all_true, True)

    one_false_results = []
    missing_results = []
    nonboolean_results = []
    for key in EXPECTED_SCREENING_GATE_KEYS:
        one_false = dict(all_true)
        one_false[key] = False
        one_false_results.append(screen_candidate(one_false, True))

        missing = dict(all_true)
        missing.pop(key)
        missing_results.append(screen_candidate(missing, True))

        nonboolean = dict(all_true)
        nonboolean[key] = 1
        nonboolean_results.append(screen_candidate(nonboolean, True))

    extra = dict(all_true)
    extra["UNREGISTERED_GATE"] = True
    invalid_audit = screen_candidate(all_true, False)
    nonboolean_audit = screen_candidate(all_true, 1)
    return {
        "all_true_only_eligible_never_promoted": all((
            all_true_result["VALID"] is True,
            all_true_result["ELIGIBLE"] is True,
            all_true_result["PROMOTED"] is False,
        )),
        "one_false_not_eligible": all(
            result["VALID"] is True and result["ELIGIBLE"] is False
            and result["PROMOTED"] is False
            for result in one_false_results
        ),
        "every_missing_gate_invalid": all(
            result["VALID"] is False and result["ELIGIBLE"] is False
            and result["PROMOTED"] is False
            for result in missing_results
        ),
        "every_nonboolean_gate_invalid": all(
            result["VALID"] is False and result["ELIGIBLE"] is False
            and result["PROMOTED"] is False
            for result in nonboolean_results
        ),
        "extra_gate_invalid": screen_candidate(extra, True)["VALID"] is False,
        "invalid_audit_never_eligible": all((
            invalid_audit["VALID"] is True,
            invalid_audit["ELIGIBLE"] is False,
            invalid_audit["PROMOTED"] is False,
        )),
        "nonboolean_audit_invalid": all((
            nonboolean_audit["VALID"] is False,
            nonboolean_audit["ELIGIBLE"] is False,
            nonboolean_audit["PROMOTED"] is False,
        )),
    }


def completion_logic(
    inherited_f2a_internal_comparison: Any,
    candidate_audit_valid: Any,
    screen_eligible: Any,
    candidate_evaluated: Any,
    state_supported_node_family: Any,
    atemporal_relational_carrier: Any,
    derived_pair_domain_and_common_action: Any,
    irreducibly_pairwise_relation: Any,
    complete_equivalence_invariance: Any,
    open_domain_and_required_nulls: Any,
    same_chain_compatibility: Any,
) -> dict[str, Any]:
    inputs = (
        inherited_f2a_internal_comparison,
        candidate_audit_valid,
        screen_eligible,
        candidate_evaluated,
        state_supported_node_family,
        atemporal_relational_carrier,
        derived_pair_domain_and_common_action,
        irreducibly_pairwise_relation,
        complete_equivalence_invariance,
        open_domain_and_required_nulls,
        same_chain_compatibility,
    )
    valid = all(type(value) is bool for value in inputs)
    if not valid:
        f2b = False
        full_f2 = False
    else:
        f2b = all(value is True for value in inputs[1:])
        full_f2 = bool(inherited_f2a_internal_comparison is True and f2b)
    return {
        "VALID": bool(valid),
        "F2B_RELATIONAL_COMPLETION": bool(f2b),
        "FULL_W2_F2_OPERATIONAL_RELATIONS": bool(full_f2),
        "PROMOTED": bool(full_f2),
        "STATUS": (
            "FULL_W2_F2_CLOSED_BY_SEPARATELY_AUDITED_CANDIDATE"
            if full_f2 else
            "VALID_COMPLETION_OPEN" if valid else
            "INVALID_COMPLETION_INPUT__NO_PROMOTION"
        ),
    }


def completion_controls() -> dict[str, bool]:
    all_true_inputs = [True] * 11
    all_true = completion_logic(*all_true_inputs)

    f2a_false_inputs = list(all_true_inputs)
    f2a_false_inputs[0] = False
    f2a_false = completion_logic(*f2a_false_inputs)

    independently_necessary = []
    for index in range(1, len(all_true_inputs)):
        values = list(all_true_inputs)
        values[index] = False
        independently_necessary.append(completion_logic(*values))

    malformed = []
    for index in range(len(all_true_inputs)):
        values = list(all_true_inputs)
        values[index] = 1
        malformed.append(completion_logic(*values))

    contract_inputs = completion_logic(
        True, False, False, False, False, False, False, False, False, False, False,
    )
    screen_ineligible = completion_logic(
        True, True, False, True, True, True, True, True, True, True, True,
    )
    return {
        "all_true_closes_f2b_and_full_f2": all((
            all_true["VALID"] is True,
            all_true["F2B_RELATIONAL_COMPLETION"] is True,
            all_true["FULL_W2_F2_OPERATIONAL_RELATIONS"] is True,
            all_true["PROMOTED"] is True,
        )),
        "f2a_false_keeps_full_f2_open": all((
            f2a_false["VALID"] is True,
            f2a_false["F2B_RELATIONAL_COMPLETION"] is True,
            f2a_false["FULL_W2_F2_OPERATIONAL_RELATIONS"] is False,
            f2a_false["PROMOTED"] is False,
        )),
        "every_f2b_component_is_independently_necessary": all(
            result["VALID"] is True
            and result["F2B_RELATIONAL_COMPLETION"] is False
            and result["FULL_W2_F2_OPERATIONAL_RELATIONS"] is False
            and result["PROMOTED"] is False
            for result in independently_necessary
        ),
        "every_nonboolean_input_invalid": all(
            result["VALID"] is False
            and result["F2B_RELATIONAL_COMPLETION"] is False
            and result["FULL_W2_F2_OPERATIONAL_RELATIONS"] is False
            and result["PROMOTED"] is False
            for result in malformed
        ),
        "contract_inputs_never_close_candidate_or_full_f2": all((
            contract_inputs["VALID"] is True,
            contract_inputs["F2B_RELATIONAL_COMPLETION"] is False,
            contract_inputs["FULL_W2_F2_OPERATIONAL_RELATIONS"] is False,
            contract_inputs["PROMOTED"] is False,
        )),
        "screen_ineligible_keeps_completion_open": all((
            screen_ineligible["VALID"] is True,
            screen_ineligible["F2B_RELATIONAL_COMPLETION"] is False,
            screen_ineligible["FULL_W2_F2_OPERATIONAL_RELATIONS"] is False,
            screen_ineligible["PROMOTED"] is False,
        )),
    }


def synthetic_controls() -> dict[str, bool]:
    marker = "SYNTHETIC_EXTRA_CARRIER_NOT_REFG"

    def synthetic_report(state: Any) -> tuple[Any, Any] | None:
        if not isinstance(state, tuple) or len(state) != 3:
            return None
        tag, unary, carrier = state
        if tag != marker or not isinstance(unary, tuple) or len(unary) != 3:
            return None
        if (
            not isinstance(carrier, tuple)
            or len(carrier) != 3
            or any(not isinstance(row, tuple) or len(row) != 3 for row in carrier)
        ):
            return None
        if any(carrier[i][j] != carrier[j][i] for i in range(3) for j in range(3)):
            return None
        unary_report = tuple(sorted(unary))
        joint_report = tuple(sorted(
            (min(unary[i], unary[j]), max(unary[i], unary[j]), carrier[i][j])
            for i in range(3) for j in range(i + 1, 3)
        ))
        return unary_report, joint_report

    def relabel_state(state: tuple[Any, ...], permutation: tuple[int, ...]) -> tuple[Any, ...]:
        tag, unary, carrier = state
        return (
            tag,
            tuple(unary[i] for i in permutation),
            tuple(tuple(carrier[i][j] for j in permutation) for i in permutation),
        )

    unary = (2, 3, 5)
    positive_left = (
        marker, unary, ((0, 7, 0), (7, 0, 0), (0, 0, 0)),
    )
    positive_right = (
        marker, unary, ((0, 0, 0), (0, 0, 11), (0, 11, 0)),
    )
    left_report = synthetic_report(positive_left)
    right_report = synthetic_report(positive_right)
    same_unary_different_joint = bool(
        left_report is not None
        and right_report is not None
        and left_report[0] == right_report[0]
        and left_report[1] != right_report[1]
        and all(
            synthetic_report(relabel_state(positive_left, permutation)) == left_report
            for permutation in permutations(range(3))
        )
        and all(
            synthetic_report(relabel_state(positive_right, permutation)) == right_report
            for permutation in permutations(range(3))
        )
    )

    factorized_literal = ((12, 11, 17), (11, 19, 23), (17, 23, 39))
    factorized_generated = tuple(tuple(
        unary[i] * unary[j] + unary[i] + unary[j] + (4 if i == j else 0)
        for j in range(3)
    ) for i in range(3))
    factorized_residual = tuple(tuple(
        factorized_literal[i][j] - factorized_generated[i][j]
        for j in range(3)
    ) for i in range(3))

    weights = (Fraction(2, 7), Fraction(5, 7))
    w212_diagonal = ((weights[0], Fraction(0)), (Fraction(0), weights[1]))
    w212_unary_equality_reconstruction = tuple(tuple(
        weights[i] if i == j else Fraction(0) for j in range(2)
    ) for i in range(2))

    synthetic_gate_map = {key: True for key in EXPECTED_SCREENING_GATE_KEYS}
    for key in (
        "same_chain_embedding_or_full_revalidation_exact",
        "candidate_freedom_ledger_complete",
        "candidate_specific_independent_audit_required",
    ):
        synthetic_gate_map[key] = False
    synthetic_only_screen = screen_candidate(synthetic_gate_map, True)
    synthetic_only_completion = completion_logic(
        True, False, False, False, True, True, True, True, True, True, True,
    )
    return {
        "same_unary_different_joint_positive_witness_detected": same_unary_different_joint,
        "factorized_unary_equality_null_detected": all(
            entry == 0 for row in factorized_residual for entry in row
        ),
        "w2_12_diagonal_form_classified_as_f2a_only": all((
            w212_diagonal == w212_unary_equality_reconstruction,
            weights[0] != weights[1],
            w212_diagonal[0][1] == 0,
            w212_diagonal[1][0] == 0,
        )),
        "synthetic_control_never_promotes_refg": all((
            synthetic_only_screen["VALID"] is True,
            synthetic_only_screen["PROMOTED"] is False,
            synthetic_only_screen["ELIGIBLE"] is False,
            synthetic_only_completion["F2B_RELATIONAL_COMPLETION"] is False,
            synthetic_only_completion["FULL_W2_F2_OPERATIONAL_RELATIONS"] is False,
            synthetic_only_completion["PROMOTED"] is False,
        )),
    }


def review_schema_valid(attestations: Any, require_pass: bool) -> bool:
    fields = {
        "passed", "reviewer", "artifact", "reviewed_payload_sha256",
        "reviewed_validator_sha256",
    }
    expected_reviewers = {
        "semantic_contract_review": "/root/f2_independent_review",
        "fail_closed_code_review": "/root/w209_no_go",
        "new_reader_scope_review": "/root/f2_contract_map",
    }
    if not isinstance(attestations, dict) or set(attestations) != EXPECTED_REVIEW_KEYS:
        return False
    for key, entry in attestations.items():
        if not isinstance(entry, dict) or set(entry) != fields:
            return False
        if type(entry["passed"]) is not bool or (require_pass and entry["passed"] is not True):
            return False
        if entry["reviewer"] != expected_reviewers[key]:
            return False
        if entry["artifact"] != EXPECTED_REVIEW_REQUIREMENTS[key]:
            return False
        if entry["reviewed_payload_sha256"] != EXPECTED_PAYLOAD_SHA256:
            return False
        if entry["reviewed_validator_sha256"] != EXPECTED_VALIDATOR_SHA256:
            return False
    return True


def review_schema_controls() -> bool:
    base = review_attestations()
    if not review_schema_valid(base, require_pass=False):
        return False
    mutants: list[Any] = []
    for key in EXPECTED_REVIEW_KEYS:
        missing_review = copy.deepcopy(base)
        missing_review.pop(key)
        mutants.append(missing_review)
        for field in (
            "passed", "reviewer", "artifact", "reviewed_payload_sha256",
            "reviewed_validator_sha256",
        ):
            missing_field = copy.deepcopy(base)
            missing_field[key].pop(field)
            mutants.append(missing_field)
    extra = copy.deepcopy(base)
    extra["fabricated_review"] = copy.deepcopy(next(iter(base.values())))
    mutants.append(extra)
    nonboolean = copy.deepcopy(base)
    nonboolean["fail_closed_code_review"]["passed"] = 1
    mutants.append(nonboolean)
    wrong_payload = copy.deepcopy(base)
    wrong_payload["semantic_contract_review"]["reviewed_payload_sha256"] = "WRONG"
    mutants.append(wrong_payload)
    wrong_validator = copy.deepcopy(base)
    wrong_validator["new_reader_scope_review"]["reviewed_validator_sha256"] = "WRONG"
    mutants.append(wrong_validator)
    wrong_reviewer = copy.deepcopy(base)
    wrong_reviewer["semantic_contract_review"]["reviewer"] = "/root/self"
    mutants.append(wrong_reviewer)
    return all(not review_schema_valid(mutant, require_pass=False) for mutant in mutants)


def safe_contract_valid(value: Any) -> bool:
    try:
        return strict_contract_valid(value)
    except Exception:
        return False


def positive_input_guard(contract: Any) -> bool:
    try:
        freedom = contract["FREEDOM_LEDGER"]
        return all((
            contract["ROUTE_POLICY"]["incompatible_cross_chain_stitching_allowed"] is False,
            contract["ROUTE_POLICY"][
                "modular_subproofs_require_one_pinned_aggregate_candidate"
            ] is True,
            freedom["preferred_labels_basis_or_axis"]["complexity"] == 0,
            freedom["data_fitted_parameters"]["complexity"] == 0,
            freedom["future_candidate_internal_primitives"]["complexity"] == 0,
            freedom["new_physical_primitives"]["complexity"] == 0,
            "desired target" not in freedom["pair_rule"]["source"].lower(),
            "free adjacency" not in freedom["pair_rule"]["source"].lower(),
            "free adjacency" not in freedom["carrier_construction"]["source"].lower(),
            "incompatible witnesses cannot be stitched"
            in contract["F2B_DEFINITION"]["same_chain"],
        ))
    except (KeyError, TypeError, AttributeError):
        return False


def mutation_controls() -> dict[str, bool]:
    base = copy.deepcopy(CLAIM_CONTRACT)
    baseline = bool(
        safe_contract_valid(base)
        and exact_tree_equal(base, build_contract())
        and positive_input_guard(base)
    )

    def rejected(mutant: Any) -> bool:
        return bool(
            baseline
            and not safe_contract_valid(mutant)
            and detached_payload_sha256(mutant) != EXPECTED_PAYLOAD_SHA256
        )

    field_mutants: list[dict[str, Any]] = []
    for field in EXPECTED_STANDARD_FIELDS | EXPECTED_CUSTOM_FIELDS:
        mutant = copy.deepcopy(base)
        mutant.pop(field)
        field_mutants.append(mutant)
    extra = copy.deepcopy(base)
    extra["UNREGISTERED"] = True
    field_mutants.append(extra)

    registry_mutants: list[dict[str, Any]] = []
    registries = (
        "F2B_DEFINITION", "F2B_SUBGATE_REGISTRY", "CANDIDATE_SCREENING_GATES",
        "RUNTIME_CLOSURE_LOGIC", "WITNESS_ROUTES", "ROUTE_POLICY",
        "FREEDOM_LEDGER", "CLOSURE_FLAGS", "SCOPE_CEILING", "GATE_APPLICABILITY",
        "EXPORT_STATUS", "INDEPENDENT_REVIEW", "NEXT_TASK_POLICY",
    )
    for registry in registries:
        for key in base[registry]:
            mutant = copy.deepcopy(base)
            mutant[registry].pop(key)
            registry_mutants.append(mutant)
        mutant = copy.deepcopy(base)
        mutant[registry]["UNREGISTERED"] = False
        registry_mutants.append(mutant)

    for freedom_key in EXPECTED_FREEDOM_KEYS:
        for field in EXPECTED_FREEDOM_ENTRY_KEYS:
            mutant = copy.deepcopy(base)
            mutant["FREEDOM_LEDGER"][freedom_key].pop(field)
            registry_mutants.append(mutant)
        mutant = copy.deepcopy(base)
        mutant["FREEDOM_LEDGER"][freedom_key]["UNREGISTERED"] = False
        registry_mutants.append(mutant)

    for registry in ("ROUTE_POLICY", "CLOSURE_FLAGS", "SCOPE_CEILING", "EXPORT_STATUS"):
        for key, value in base[registry].items():
            if type(value) is bool:
                mutant = copy.deepcopy(base)
                mutant[registry][key] = 1
                registry_mutants.append(mutant)

    missing_forbidden = copy.deepcopy(base)
    missing_forbidden["FORBIDDEN_INPUTS"] = missing_forbidden["FORBIDDEN_INPUTS"][:-1]
    registry_mutants.append(missing_forbidden)
    extra_forbidden = copy.deepcopy(base)
    extra_forbidden["FORBIDDEN_INPUTS"] += ("unregistered forbidden-input entry",)
    registry_mutants.append(extra_forbidden)

    boundary_mutants: list[dict[str, Any]] = []
    for registry in ("CLOSURE_FLAGS", "SCOPE_CEILING", "EXPORT_STATUS"):
        for key, value in base[registry].items():
            if value is False:
                mutant = copy.deepcopy(base)
                mutant[registry][key] = True
                boundary_mutants.append(mutant)
    for key, value in base["F2B_SUBGATE_REGISTRY"].items():
        if value == "OPEN_UNEVALUATED":
            mutant = copy.deepcopy(base)
            mutant["F2B_SUBGATE_REGISTRY"][key] = "PROVED_WITHOUT_CANDIDATE"
            boundary_mutants.append(mutant)
    closes_by_rule = copy.deepcopy(base)
    closes_by_rule["RUNTIME_CLOSURE_LOGIC"]["contract_rule"] = (
        "This contract evaluates a candidate and closes full F2."
    )
    boundary_mutants.append(closes_by_rule)

    semantic_mutants: list[dict[str, Any]] = []
    for field, text in (
        ("CLAIM", " This closes full F2."),
        ("METHOD", " Candidate is evaluated."),
        ("METHOD", " Physical location is proved."),
        ("VALIDITY_HEALTH", " Persistent imprint is proved."),
        ("VALIDITY_HEALTH", " Time emerges."),
        ("VALIDITY_HEALTH", " Causality emerges."),
        ("VALIDITY_HEALTH", " GR is derived."),
        ("VALIDITY_HEALTH", " Observationally validated."),
    ):
        mutant = copy.deepcopy(base)
        mutant[field] += text
        semantic_mutants.append(mutant)

    injection_mutants: list[dict[str, Any]] = []
    target = copy.deepcopy(base)
    target["FREEDOM_LEDGER"]["pair_rule"]["source"] = "desired target relation table"
    injection_mutants.append(target)
    adjacency = copy.deepcopy(base)
    adjacency["FREEDOM_LEDGER"]["carrier_construction"]["source"] = "free adjacency"
    injection_mutants.append(adjacency)
    stitched = copy.deepcopy(base)
    stitched["ROUTE_POLICY"]["incompatible_cross_chain_stitching_allowed"] = True
    injection_mutants.append(stitched)
    stitched_definition = copy.deepcopy(base)
    stitched_definition["F2B_DEFINITION"]["same_chain"] = (
        "Unrelated witnesses from incompatible versions may be stitched."
    )
    injection_mutants.append(stitched_definition)
    preferred = copy.deepcopy(base)
    preferred["FREEDOM_LEDGER"]["preferred_labels_basis_or_axis"]["complexity"] = 1
    injection_mutants.append(preferred)
    fitted = copy.deepcopy(base)
    fitted["FREEDOM_LEDGER"]["data_fitted_parameters"]["complexity"] = 1
    injection_mutants.append(fitted)
    hidden = copy.deepcopy(base)
    hidden["FREEDOM_LEDGER"]["future_candidate_internal_primitives"]["complexity"] = 1
    injection_mutants.append(hidden)

    all_true = {key: True for key in EXPECTED_SCREENING_GATE_KEYS}
    malformed_screens: list[Any] = []
    for key in EXPECTED_SCREENING_GATE_KEYS:
        missing = dict(all_true)
        missing.pop(key)
        malformed_screens.append(missing)
        nonboolean = dict(all_true)
        nonboolean[key] = 1
        malformed_screens.append(nonboolean)
    extra_gate = dict(all_true)
    extra_gate["UNREGISTERED"] = True
    malformed_screens.append(extra_gate)

    false_positive_failures = (
        ("state_supported_node_family_generated_not_preassigned",
         "node_ownership_certificate_law_derived"),
        ("atemporal_relational_carrier_is_state_supported_not_readout_only",),
        ("candidate_freedom_ledger_complete", "uniform_target_free_pair_rule_and_shared_codomain"),
        ("route_neutral_irreducibility_certificate_exact",
         "relation_not_factorable_through_unary_quotients"),
        ("same_chain_embedding_or_full_revalidation_exact",),
        ("reported_relation_complete_equivalence_invariant",),
        ("nonzero_relational_quotient_on_predeclared_open_domain",),
        ("f3_time_memory_persistence_and_causality_absent",),
        ("physical_spatial_geometric_and_observable_semantics_absent",),
        ("w2_12_diagonal_comparison_not_relabelled_as_pair_coupling",
         "relation_not_factorable_through_unary_quotients"),
    )
    false_positive_profiles = []
    for failures in false_positive_failures:
        profile = dict(all_true)
        for key in failures:
            profile[key] = False
        false_positive_profiles.append(screen_candidate(profile, True))

    return {
        "missing_or_extra_contract_fields_rejected": all(
            rejected(mutant) for mutant in field_mutants
        ),
        "registry_drift_rejected": all(
            rejected(mutant) for mutant in registry_mutants
        ),
        "closure_scope_export_overclaims_rejected": all(
            rejected(mutant) for mutant in boundary_mutants
        ),
        "semantic_overclaims_rejected": all(
            not semantic_guard(mutant) and rejected(mutant)
            for mutant in semantic_mutants
        ),
        "target_and_cross_chain_injections_rejected": all(
            not positive_input_guard(mutant) and rejected(mutant)
            for mutant in injection_mutants
        ),
        "screen_schema_mutants_rejected": all(
            screen_candidate(mutant, True)["VALID"] is False
            for mutant in malformed_screens
        ) and screen_candidate(all_true, 1)["VALID"] is False,
        "false_positive_route_profiles_not_eligible": all(
            result["VALID"] is True
            and result["ELIGIBLE"] is False
            and result["PROMOTED"] is False
            for result in false_positive_profiles
        ),
    }


def _run_audit_unchecked() -> dict[str, Any]:
    if not strict_contract_valid(CLAIM_CONTRACT):
        raise ValueError("contract payload or schema invalid")
    if detached_validator_sha256() != EXPECTED_VALIDATOR_SHA256:
        raise ValueError("validator source identity invalid")

    dependency_ok, _dependencies = dependencies_valid()
    screen_controls = screening_controls()
    completion_control_map = completion_controls()
    synthetic_control_map = synthetic_controls()
    mutations = mutation_controls()
    attestations = review_attestations()

    contract_gates = {key: False for key in EXPECTED_SCREENING_GATE_KEYS}
    contract_screen = screen_candidate(contract_gates, False)
    contract_completion = completion_logic(
        bool(dependency_ok), False, False, False, False,
        False, False, False, False, False, False,
    )
    review_structure = review_schema_valid(attestations, require_pass=False)

    checks = {
        "payload_validator_and_contract_schema_exact": all((
            strict_contract_valid(CLAIM_CONTRACT),
            detached_validator_sha256() == EXPECTED_VALIDATOR_SHA256,
            registry_shapes_valid(CLAIM_CONTRACT),
        )),
        "c0_f2a_w211_w212_f1_dependencies_exact": dependency_ok,
        "screening_and_completion_decision_controls_exact": all((
            exact_true_map(screen_controls, EXPECTED_SCREEN_CONTROL_KEYS),
            exact_true_map(completion_control_map, EXPECTED_COMPLETION_CONTROL_KEYS),
        )),
        "synthetic_positive_and_required_null_controls_exact": exact_true_map(
            synthetic_control_map, EXPECTED_SYNTHETIC_CONTROL_KEYS,
        ),
        "mutation_controls_exact": exact_true_map(mutations, EXPECTED_MUTATION_KEYS),
        "candidate_neutrality_and_no_evaluation_exact": all((
            exact_bool_map(
                {key: False for key in contract_gates},
                {key: False for key in EXPECTED_SCREENING_GATE_KEYS},
            ),
            contract_screen["VALID"] is True,
            contract_screen["ELIGIBLE"] is False,
            contract_screen["PROMOTED"] is False,
            contract_completion["VALID"] is True,
            contract_completion["F2B_RELATIONAL_COMPLETION"] is False,
            contract_completion["FULL_W2_F2_OPERATIONAL_RELATIONS"] is False,
            contract_completion["PROMOTED"] is False,
        )),
        "closure_scope_export_boundaries_exact": all((
            exact_bool_map(CLAIM_CONTRACT["CLOSURE_FLAGS"], EXPECTED_C0_CLOSURE_FLAGS),
            exact_bool_map(CLAIM_CONTRACT["SCOPE_CEILING"], EXPECTED_SCOPE_CEILING),
            exact_bool_map(CLAIM_CONTRACT["EXPORT_STATUS"], EXPECTED_EXPORT_STATUS),
            CLAIM_CONTRACT["F2B_SUBGATE_REGISTRY"][
                "inherited_f2a_internal_comparison"
            ] == "PROVED_BY_EXACT_W2_12_DEPENDENCY",
            all(
                value == "OPEN_UNEVALUATED"
                for key, value in CLAIM_CONTRACT["F2B_SUBGATE_REGISTRY"].items()
                if key != "inherited_f2a_internal_comparison"
            ),
        )),
        "review_schema_fail_closed": all((
            review_structure,
            review_schema_controls(),
        )),
        "review_attestations_complete": review_schema_valid(
            attestations, require_pass=True,
        ),
        "next_task_is_neutral_sufficiency_gate": all((
            CLAIM_CONTRACT["NEXT_TASK_POLICY"]["frozen"] == NEXT_ATOMIC_TASK,
            "w2_14_f2b_single_generator_commutative_spectral_repackaging_gate.py"
            in NEXT_ATOMIC_TASK,
            "single-generator commutative spectral class" in NEXT_ATOMIC_TASK,
            "without new primitives" in NEXT_ATOMIC_TASK,
            "scoped exact positive result or a scoped no-go" in NEXT_ATOMIC_TASK,
            "rejects only this declared class" in NEXT_ATOMIC_TASK,
            "keep full W2_F2 false" in NEXT_ATOMIC_TASK,
        )),
    }
    schema_exact = bool(
        set(checks) == EXPECTED_AUDIT_KEYS
        and all(type(checks[key]) is bool for key in EXPECTED_AUDIT_KEYS)
    )
    structural_ready = bool(
        schema_exact
        and all(
            checks[key] is True
            for key in EXPECTED_AUDIT_KEYS
            if key != "review_attestations_complete"
        )
    )
    audit_valid = bool(structural_ready and checks["review_attestations_complete"])
    status = FROZEN_STATUS if audit_valid else READY_STATUS if structural_ready else INVALID_STATUS
    next_task = (
        CLAIM_CONTRACT["NEXT_TASK_POLICY"]["frozen"] if audit_valid else
        CLAIM_CONTRACT["NEXT_TASK_POLICY"]["pending"] if structural_ready else
        CLAIM_CONTRACT["NEXT_TASK_POLICY"]["invalid"]
    )
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": status,
        "AUDIT_VALID": audit_valid,
        "STRUCTURAL_READY_FOR_REVIEW": structural_ready,
        "CONTRACT_FROZEN": audit_valid,
        "CANDIDATE_EVALUATED": False,
        "INHERITED_F2A_INTERNAL_COMPARISON_PROVED": bool(dependency_ok),
        "F2B_RELATIONAL_COMPLETION_PROVED": False,
        "PROMOTED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "DETACHED_PAYLOAD_SHA256": detached_payload_sha256(CLAIM_CONTRACT),
        "DETACHED_VALIDATOR_SHA256": detached_validator_sha256(),
        "CANDIDATE_GATE_MAP": contract_gates,
        "CANDIDATE_SCREEN": contract_screen,
        "CONTRACT_COMPLETION_DECISION": contract_completion,
        "SCREENING_CONTROLS": screen_controls,
        "COMPLETION_CONTROLS": completion_control_map,
        "SYNTHETIC_CONTROLS": synthetic_control_map,
        "MUTATION_CONTROLS": mutations,
        "AUDIT_CHECKS": checks,
        "INDEPENDENT_REVIEW_ATTESTATIONS": attestations,
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": bool(dependency_ok),
            "W2_F2B_CANDIDATE_EVALUATED": False,
            "W2_F2B_STATE_SUPPORTED_NODE_FAMILY_PROVED": False,
            "W2_F2B_ATEMPORAL_RELATIONAL_CARRIER_PROVED": False,
            "W2_F2B_DERIVED_PAIR_DOMAIN_AND_COMMON_ACTION_PROVED": False,
            "W2_F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED": False,
            "W2_F2B_COMPLETE_EQUIVALENCE_INVARIANCE_PROVED": False,
            "W2_F2B_OPEN_DOMAIN_AND_REQUIRED_NULLS_PROVED": False,
            "W2_F2B_SAME_CHAIN_COMPATIBILITY_PROVED": False,
            "W2_F2B_RELATIONAL_COMPLETION_PROVED": False,
            "W2_F2_OPERATIONAL_RELATIONS_PROVED": False,
        },
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "PROMOTION_CEILING": "CONTRACT_ONLY__NO_CANDIDATE_PROMOTION",
        "NEXT_ATOMIC_TASK": next_task,
    }


def fail_closed_invalid_report(error: Exception) -> dict[str, Any]:
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": INVALID_STATUS,
        "AUDIT_VALID": False,
        "STRUCTURAL_READY_FOR_REVIEW": False,
        "CONTRACT_FROZEN": False,
        "CANDIDATE_EVALUATED": False,
        "INHERITED_F2A_INTERNAL_COMPARISON_PROVED": False,
        "F2B_RELATIONAL_COMPLETION_PROVED": False,
        "PROMOTED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "DETACHED_PAYLOAD_SHA256": "",
        "DETACHED_VALIDATOR_SHA256": "",
        "CANDIDATE_GATE_MAP": {key: False for key in EXPECTED_SCREENING_GATE_KEYS},
        "CANDIDATE_SCREEN": {
            "VALID": False, "ELIGIBLE": False, "PROMOTED": False,
            "STATUS": "INVALID_SCREEN__NO_ELIGIBILITY_OR_PROMOTION",
        },
        "CONTRACT_COMPLETION_DECISION": {
            "VALID": False,
            "F2B_RELATIONAL_COMPLETION": False,
            "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
            "PROMOTED": False,
            "STATUS": "INVALID_COMPLETION_INPUT__NO_PROMOTION",
        },
        "SCREENING_CONTROLS": {
            key: False for key in EXPECTED_SCREEN_CONTROL_KEYS
        },
        "COMPLETION_CONTROLS": {
            key: False for key in EXPECTED_COMPLETION_CONTROL_KEYS
        },
        "SYNTHETIC_CONTROLS": {
            key: False for key in EXPECTED_SYNTHETIC_CONTROL_KEYS
        },
        "MUTATION_CONTROLS": {key: False for key in EXPECTED_MUTATION_KEYS},
        "AUDIT_CHECKS": {key: False for key in EXPECTED_AUDIT_KEYS},
        "INDEPENDENT_REVIEW_ATTESTATIONS": {},
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": False,
            "W2_F2B_CANDIDATE_EVALUATED": False,
            "W2_F2B_STATE_SUPPORTED_NODE_FAMILY_PROVED": False,
            "W2_F2B_ATEMPORAL_RELATIONAL_CARRIER_PROVED": False,
            "W2_F2B_DERIVED_PAIR_DOMAIN_AND_COMMON_ACTION_PROVED": False,
            "W2_F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED": False,
            "W2_F2B_COMPLETE_EQUIVALENCE_INVARIANCE_PROVED": False,
            "W2_F2B_OPEN_DOMAIN_AND_REQUIRED_NULLS_PROVED": False,
            "W2_F2B_SAME_CHAIN_COMPATIBILITY_PROVED": False,
            "W2_F2B_RELATIONAL_COMPLETION_PROVED": False,
            "W2_F2_OPERATIONAL_RELATIONS_PROVED": False,
        },
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "PROMOTION_CEILING": "NONE__INVALID",
        "NEXT_ATOMIC_TASK": "UNAVAILABLE_UNTIL_EXACT_ARTIFACT_RESTORED",
        "FAIL_CLOSED_REASON": f"{type(error).__name__}: {error}",
    }


def run_audit() -> dict[str, Any]:
    try:
        return _run_audit_unchecked()
    except Exception as error:
        return fail_closed_invalid_report(error)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_audit()
    try:
        rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    except (TypeError, ValueError) as error:
        report = fail_closed_invalid_report(error)
        report["NEXT_ATOMIC_TASK"] = "UNAVAILABLE_UNTIL_JSON_SAFE"
        rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    return 0 if report["AUDIT_VALID"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
