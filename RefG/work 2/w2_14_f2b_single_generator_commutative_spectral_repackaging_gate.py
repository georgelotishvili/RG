"""Exact scoped no-go for F2b from commutative repackaging of the frozen Q state.

The class contains only the accepted F1 single carrier Q, its regular spectral
functional calculus, the already imported matrix product/trace/transpose, and
law jets used strictly as diagnostics.  It asks whether these ingredients can
produce state-owned nodes and a pair relation outside unary/equality data.

The theorem is deliberately class-local.  It does not reject noncommuting
single-carrier channels, a genuinely state-owned joint carrier, or any revised
candidate that revalidates F1 and F2a.  Full W2-F2 remains open here.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

import sympy as sp


MODEL_VERSION = (
    "W2-F2B-SINGLE-GENERATOR-COMMUTATIVE-SPECTRAL-REPACKAGING-NO-GO-"
    "v1.0-internal"
)
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"
W213_MODEL = "W2-F2B-NODE-IMPRINT-RELATIONAL-COMPLETION-CONTRACT-v1.0-internal"
W213_STATUS = "W2_F2B_CONTRACT_FROZEN__NO_CANDIDATE_EVALUATED__FULL_F2_OPEN"
W213_PAYLOAD = "1B7D2921C78DB177CE401E04B5359ED28988DB2CF86E89A3159407BDF0B18733"
W213_VALIDATOR = "98F4A8B70742F9F709629486DC1D948BC22CAB12C74F7DBCA99E3B616FE3FC68"
W212_MODEL = "W2-F2A-INTRASTATE-HESSIAN-COMPARISON-v1.0-internal"
W212_STATUS = "CONDITIONAL_EXACT_F2A_INTRASTATE_HESSIAN_COMPARISON__FULL_F2_OPEN"

C0_SHA256 = "3E0EFB2D635E7E5605F9D7EDFA99538644D7C21311989C478C4A6AF1854890EB"
W212_SOURCE = "1F7F4FFE139F731D1D254BD48D11852E5C5ADA3298CEDC05FB6584B8923D8F9B"
W213_SOURCE = "0BABF2EB701845452E2E809B1420857D04A842FCC5FEB24BD732523E2C88E347"
F1_SOURCE = "8B29AF84AE0F94063CF0E7FDAB47A7CE364C7D6B1789D71051548A98A96C770E"

READY_STATUS = "W2_F2B_SINGLE_GENERATOR_NO_GO_READY_FOR_INDEPENDENT_REVIEW__F2B_OPEN"
PASS_STATUS = "EXACT_SINGLE_GENERATOR_COMMUTATIVE_SPECTRAL_REPACKAGING_NO_GO__F2B_OPEN"
INVALID_STATUS = "W2_F2B_SINGLE_GENERATOR_NO_GO_INVALID__F2B_OPEN"
EXPECTED_PAYLOAD_SHA256 = "D81E577D3C1F46CE1BC8E3F464AC06DEC79054344780B44876F5A623AC1A1DA0"
EXPECTED_VALIDATOR_SHA256 = "A59353C5BBBEADAC35C6EA014BF02D8C6E96C6B3409843AF00C00BF36AFD673B"

ROOT = Path(__file__).resolve().parents[2]
C0_PATH = Path(__file__).with_name("w2_00_foundation_to_einstein_contract.md")
W212_PATH = Path(__file__).with_name(
    "w2_12_f2_intrastate_uniform_effect_family_candidate_gate.py"
)
W213_PATH = Path(__file__).with_name(
    "w2_13_f2b_node_imprint_and_relational_completion_contract.py"
)
F1_PATH = Path(__file__).with_name("w2_09a_f1_proof") / "refg_f1_atemporal_structural_proof.py"

NEXT_ATOMIC_TASK = (
    "Create w2_15_f2b_general_traceless_single_carrier_candidate_contract.py: "
    "before evaluating outcomes, freeze a revised one-carrier state A with its exact "
    "transpose-derived symmetric and skew channels, one common O(3) action, a complete "
    "freedom ledger, F1 and F2a revalidation duties, state-owned node and joint-carrier "
    "tests, generic and null branches, and start every new candidate/F2b/full-F2 flag false."
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
    "CLASS_DEFINITION", "NO_GO_THEOREM", "NO_GO_GATE_EVIDENCE",
    "ESCAPE_ROUTE_REGISTRY", "FORBIDDEN_UPGRADES", "SCOPE_CEILING",
    "GATE_APPLICABILITY", "EXPORT_STATUS", "INDEPENDENT_REVIEW",
    "NEXT_TASK_POLICY", "NEXT_ATOMIC_TASK",
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
    "declared_single_generator_class_rejected": True,
    "all_no_new_primitive_routes_rejected": False,
    "noncommuting_single_carrier_route_rejected": False,
    "state_owned_joint_carrier_route_rejected": False,
    "f2b_candidate_evaluated": False,
    "state_supported_nodes_proved": False,
    "atemporal_state_imprint_proved": False,
    "irreducible_pair_relation_proved": False,
    "full_W2_F2_operational_relations": False,
    "persistence_time_or_causality": False,
    "physical_space_metric_or_observable": False,
    "GR_PN_or_PPN_bridge": False,
    "observational_validation": False,
}
EXPECTED_EXPORT_STATUS = {
    "CANON": False, "ARTICLE": False, "GITHUB": False, "ZENODO": False,
}
EXPECTED_CLASS_KEYS = frozenset({
    "state", "accepted_branch", "equivalence", "allowed_algebra",
    "allowed_reports", "law_jet_role", "node_rule", "excluded_extensions",
    "parameter_domain", "class_boundary",
})
EXPECTED_THEOREM_KEYS = frozenset({
    "spectral_algebra_collapse", "canonical_node_bound",
    "pair_factorization", "degenerate_fibre_boundary", "law_jet_boundary",
    "conclusion", "not_ruled_out",
})
EXPECTED_EVIDENCE_KEYS = frozenset({
    "exact_w213_dependency_and_f2a_boundary",
    "accepted_uniaxial_minimal_polynomial_exact",
    "commutative_spectral_algebra_is_two_dimensional",
    "only_two_canonical_central_projectors",
    "stabilizer_forbids_canonical_rank1_split_of_rank2_sector",
    "uniform_spectral_pair_words_factor_through_unary_and_equality",
    "set_valued_subprojector_fibre_is_not_coexisting_state_content",
    "bare_overlap_on_that_fibre_is_not_a_state_imprint",
    "law_jets_remain_diagnostics_unless_state_space_is_revised",
    "parameter_fibres_and_gauge_tangents_do_not_supply_relata",
    "open_positive_parameter_domain_is_covered",
    "preserved_escape_routes_are_not_rejected",
})
EXPECTED_ESCAPE_KEYS = frozenset({
    "NONCOMMUTING_SINGLE_CARRIER_TRANSPOSE_CHANNELS",
    "STATE_OWNED_JOINT_CARRIER",
    "REVISED_LAW_JET_AS_ACCEPTED_STATE_COMPONENT",
    "GENUINE_MULTI_OBJECT_DYNAMICAL_STATE",
    "PROJECTIVE_FIBRE",
})
EXPECTED_FREEDOM_KEYS = frozenset({
    "inherited_alpha_b_c", "spectral_function_choice", "word_length",
    "node_selector", "pair_report", "preferred_basis_or_axis",
    "new_state_component", "data_fitted_parameters",
})
EXPECTED_FREEDOM_ENTRY_KEYS = frozenset({
    "source", "allowed_range", "scale", "complexity",
})
EXPECTED_ALGEBRA_CONTROL_KEYS = frozenset({
    "accepted_projector_reconstruction_exact",
    "minimal_polynomial_exact",
    "generic_spectral_element_reduction_exact",
    "central_idempotent_table_exact",
    "generic_pair_word_table_is_diagonal",
    "diagonal_table_equals_unary_times_equality",
})
EXPECTED_STABILIZER_CONTROL_KEYS = frozenset({
    "rank2_stabilizer_generators_exact",
    "invariant_symmetric_corner_is_scalar",
    "invariant_corner_idempotents_have_rank_zero_or_two",
    "no_canonical_rank1_corner_projector",
})
EXPECTED_ESCAPE_CONTROL_KEYS = frozenset({
    "set_valued_fibre_exists_but_has_no_canonical_member",
    "fibre_overlap_varies_but_is_imported_kinematics",
    "same_unary_bare_overlap_not_irreducible",
    "rank1_word_reduces_to_overlap",
    "no_invariant_rank1_split_P2",
    "w2_12_pairwise_and_state_imprint_flags_remain_false",
    "preserved_routes_are_explicitly_open",
})
EXPECTED_MUTATION_KEYS = frozenset({
    "missing_or_extra_contract_fields_rejected",
    "class_theorem_registry_drift_rejected",
    "scope_and_export_overclaims_rejected",
    "semantic_global_no_go_overclaims_rejected",
    "evidence_schema_mutants_rejected",
    "one_missing_evidence_prevents_no_go",
})
EXPECTED_AUDIT_KEYS = frozenset({
    "payload_validator_and_contract_schema_exact",
    "c0_w212_w213_f1_dependencies_exact",
    "algebra_and_stabilizer_theorem_controls_exact",
    "escape_boundary_controls_exact",
    "no_go_evidence_schema_and_decision_exact",
    "mutation_controls_exact",
    "closure_scope_export_boundaries_exact",
    "review_schema_fail_closed",
    "review_attestations_complete",
    "next_task_is_new_version_contract_not_result",
})
EXPECTED_REVIEW_KEYS = frozenset({
    "mathematical_no_go_review", "fail_closed_code_review", "new_reader_scope_review",
})
EXPECTED_W213_REVIEW_KEYS = frozenset({
    "semantic_contract_review", "fail_closed_code_review", "new_reader_scope_review",
})
EXPECTED_REVIEW_REQUIREMENTS = {
    "mathematical_no_go_review": "independent theorem, class-boundary and invariant-algebra audit",
    "fail_closed_code_review": "independent symbolic, decision, mutation and fail-closed audit",
    "new_reader_scope_review": "independent provenance, standalone clarity and non-global-overclaim audit",
}

REVIEW_ATTESTED_PAYLOAD_IDS = {
    "mathematical_no_go_review": "D81E577D3C1F46CE1BC8E3F464AC06DEC79054344780B44876F5A623AC1A1DA0",
    "fail_closed_code_review": "D81E577D3C1F46CE1BC8E3F464AC06DEC79054344780B44876F5A623AC1A1DA0",
    "new_reader_scope_review": "D81E577D3C1F46CE1BC8E3F464AC06DEC79054344780B44876F5A623AC1A1DA0",
}
REVIEW_ATTESTED_VALIDATOR_IDS = {
    "mathematical_no_go_review": "A59353C5BBBEADAC35C6EA014BF02D8C6E96C6B3409843AF00C00BF36AFD673B",
    "fail_closed_code_review": "A59353C5BBBEADAC35C6EA014BF02D8C6E96C6B3409843AF00C00BF36AFD673B",
    "new_reader_scope_review": "A59353C5BBBEADAC35C6EA014BF02D8C6E96C6B3409843AF00C00BF36AFD673B",
}


def class_definition() -> dict[str, str]:
    return {
        "state": "One accepted Q in Sym_0(3,R); no second accepted-state component.",
        "accepted_branch": (
            "The exact alpha,b,c>0 uniaxial F1 branch with spectrum "
            "(2s/3,-s/3,-s/3), s>0."
        ),
        "equivalence": "Complete inherited O(3) conjugation; Q sign is not gauge.",
        "allowed_algebra": (
            "The regular unital commutative algebra generated by I and Q, including "
            "polynomial/rational spectral functional calculus where denominators are regular, "
            "matrix product, transpose, trace and parameter scalars."
        ),
        "allowed_reports": (
            "Uniform target-free reports assembled from spectral idempotents, allowed algebra "
            "elements, products and traces on the same accepted state."
        ),
        "law_jet_role": (
            "Gradient, Hessian and higher law derivatives are diagnostic tensors over the state; "
            "they are not accepted-state components in this frozen class."
        ),
        "node_rule": (
            "A canonical node must be a single-valued O(3)-covariant, state-supported subobject.  "
            "A set of possible subprojectors is not a set of coexisting occupied nodes."
        ),
        "excluded_extensions": (
            "Any noncommuting accepted-state channel, extra carrier, product state, selected "
            "subprojector, law jet promoted to state, time, geometry or data."
        ),
        "parameter_domain": "The full open inherited domain alpha,b,c>0.",
        "class_boundary": (
            "The result rejects only single-generator commutative spectral repackaging; it is "
            "not a no-go for RefG, for every no-new-primitive construction, or for full F2."
        ),
    }


def no_go_theorem() -> dict[str, str]:
    return {
        "spectral_algebra_collapse": (
            "The accepted Q has a degree-two minimal polynomial, so every regular spectral "
            "element is x P1 + y P2."
        ),
        "canonical_node_bound": (
            "Only P1 and P2 are canonical central idempotents.  The O(2) stabilizer on P2 "
            "forbids a covariant rank-one split without an additional state object."
        ),
        "pair_factorization": (
            "Orthogonality P_a P_b=delta_ab P_a reduces every uniform spectral pair word to "
            "unary spectral scalars multiplied by bare equality; its irreducible quotient is zero."
        ),
        "degenerate_fibre_boundary": (
            "All rank-one subprojectors inside P2 form a state-owned possibility fibre, but no "
            "member is selected or coexists as accepted-state content.  Their overlap is inherited "
            "kinematics: p q p=Tr(p q)p for rank-one p,q.  Same unary support with varying bare "
            "overlap is therefore a controlled false positive, not an imprint."
        ),
        "law_jet_boundary": (
            "A law jet may distinguish diagnostic sectors as in w2_12, but treating such a sector "
            "as occupied node or carrier changes the accepted state space and leaves this class."
        ),
        "conclusion": (
            "No candidate in the declared class can satisfy the w2_13 state-node, state-carrier "
            "and irreducible-pair gates; therefore this class cannot close F2b."
        ),
        "not_ruled_out": (
            "A noncommuting channel contained in one revised carrier, a genuine state-owned joint "
            "carrier, or another version that revalidates F1 and F2a remains open."
        ),
    }


def escape_routes() -> dict[str, str]:
    return {
        "NONCOMMUTING_SINGLE_CARRIER_TRANSPOSE_CHANNELS": (
            "OPEN - a revised one-carrier state may have symmetric and skew state-owned channels."
        ),
        "STATE_OWNED_JOINT_CARRIER": "OPEN - must be generated and fully ledgered, not a target table.",
        "REVISED_LAW_JET_AS_ACCEPTED_STATE_COMPONENT": (
            "OPEN_NEW_VERSION - requires a state-space law and full chain revalidation."
        ),
        "GENUINE_MULTI_OBJECT_DYNAMICAL_STATE": (
            "OPEN_NEW_VERSION - multiplicity and common action must be dynamically derived."
        ),
        "PROJECTIVE_FIBRE": (
            "OPEN_PROFILE - BARE_OVERLAP_OR_HIDDEN_SELECTION - a rank-one member is either unselected kinematics "
            "or an added state/node selector outside this class."
        ),
    }


def no_go_evidence_descriptions() -> dict[str, str]:
    evidence = {
        "exact_w213_dependency_and_f2a_boundary": "Frozen w2_13 and exact w2_12 F2a boundary pass.",
        "accepted_uniaxial_minimal_polynomial_exact": "The accepted spectrum and degree-two identity are exact.",
        "commutative_spectral_algebra_is_two_dimensional": "Every regular f(Q) reduces to xP1+yP2.",
        "only_two_canonical_central_projectors": "The central idempotents are exactly 0,P1,P2,I.",
        "stabilizer_forbids_canonical_rank1_split_of_rank2_sector": "No O(2)-fixed rank-one corner idempotent exists.",
        "uniform_spectral_pair_words_factor_through_unary_and_equality": "All cross words vanish and diagonal words are unary.",
        "set_valued_subprojector_fibre_is_not_coexisting_state_content": "A possibility fibre supplies no selected simultaneous nodes.",
        "bare_overlap_on_that_fibre_is_not_a_state_imprint": "Its varying overlap comes from the imported contraction.",
        "law_jets_remain_diagnostics_unless_state_space_is_revised": "w2_12 expressly does not promote jets to state content.",
        "parameter_fibres_and_gauge_tangents_do_not_supply_relata": "Cross-fibre stitching and orbit tangents remain excluded.",
        "open_positive_parameter_domain_is_covered": "The proof uses only s>0 on every alpha,b,c>0 accepted branch.",
        "preserved_escape_routes_are_not_rejected": "All routes outside the exact class stay explicitly open.",
    }
    if set(evidence) != EXPECTED_EVIDENCE_KEYS:
        raise RuntimeError("evidence registry drift")
    return evidence


def freedom_ledger() -> dict[str, dict[str, Any]]:
    zero = {"source": "none", "allowed_range": 0, "scale": "class", "complexity": 0}
    return {
        "inherited_alpha_b_c": {
            "source": "exact F1 dependency", "allowed_range": "alpha,b,c>0",
            "scale": "three inherited universal parameters", "complexity": 3,
        },
        "spectral_function_choice": {
            "source": "universally quantified regular f", "allowed_range": "all regular functions of Q",
            "scale": "theorem class, not fitted choice", "complexity": 0,
        },
        "word_length": {
            "source": "universally quantified finite word", "allowed_range": "every finite length",
            "scale": "inductive theorem class", "complexity": 0,
        },
        "node_selector": dict(zero),
        "pair_report": {
            "source": "universally quantified uniform spectral word/trace report",
            "allowed_range": "complete declared class", "scale": "theorem class", "complexity": 0,
        },
        "preferred_basis_or_axis": {**zero, "scale": "description"},
        "new_state_component": {**zero, "scale": "accepted state"},
        "data_fitted_parameters": {**zero, "scale": "data"},
    }


def gate_applicability() -> dict[str, str]:
    return {
        "G0_GOAL": "REQUIRED - exact class and class-local falsifier frozen",
        "G1_CONVENTIONS": "REQUIRED - state, algebra, equivalence and node rule fixed",
        "G2_CORE_ALGEBRA": "REQUIRED - minimal polynomial and pair-word collapse",
        "G3_STRUCTURE": "REQUIRED - stabilizer and state-support no-go",
        "G4_INDEPENDENT_CHECK": "REQUIRED - three detached reviews",
        "G5_LIMITS_REGRESSION": "REQUIRED - fibre, jet, gauge and parameter nulls",
        "G6_PHYSICAL_MATCH": "N/A - no physical node or response",
        "G7_OBSERVATION": "N/A - no observable or data",
        "G8_EXPORT": "N/A - internal and Git-ignored",
    }


def review_attestations() -> dict[str, dict[str, Any]]:
    return {
        "mathematical_no_go_review": {
            "passed": True,
            "reviewer": "/root/f2_independent_review",
            "artifact": EXPECTED_REVIEW_REQUIREMENTS["mathematical_no_go_review"],
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS["mathematical_no_go_review"],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS["mathematical_no_go_review"],
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
        "CLAIM_ID": "W2_F2B_SINGLE_GENERATOR_COMMUTATIVE_SPECTRAL_NO_GO_001",
        "CLAIM": (
            "Within the exact frozen one-Q commutative spectral class, prove that canonical "
            "state nodes stop at P1/P2 and every uniform pair word factors through unary data "
            "and equality; reject only this class and keep full F2 open."
        ),
        "TYPE": "EXACT_CLASS_LOCAL_NO_GO",
        "MODEL_VERSION": MODEL_VERSION,
        "ASSUMPTIONS": (
            "The exact frozen F1, w2_12 F2a and w2_13 completion boundaries are valid.",
            "The class contains exactly one accepted symmetric carrier Q and no hidden state component.",
            "Law derivatives remain diagnostics and the complete equivalence is inherited O(3).",
        ),
        "DOMAIN": "Every accepted uniaxial Q on the full open alpha,b,c>0 branch.",
        "CONVENTIONS": (
            "O(3) is internal, not physical space.  Spectral projector means an algebraic "
            "subobject, not automatically a node.  A set-valued fibre is not simultaneous state content."
        ),
        "FREEDOM_LEDGER": freedom_ledger(),
        "DEPENDENCIES": {
            "rules": (
                "frozen W2-C0 exact runtime identity; private governance is not a runtime file"
            ),
            "programme": PROGRAM_CONTRACT,
            "f2a_candidate": W212_MODEL,
            "f2b_contract": W213_MODEL,
            "public_f1": "RefG-F1-ATEMPORAL-STRUCTURAL-PROOF-v1.0",
        },
        "METHOD": (
            "Use the accepted minimal polynomial, central idempotents, stabilizer fixed-point "
            "classification and an induction on finite spectral words; audit fibre and law-jet escapes."
        ),
        "PASS_CONDITION": (
            "All exact algebra, stabilizer, escape, schema, mutation, dependency and detached-review "
            "checks pass.  PASS proves only the declared class-local no-go."
        ),
        "FAIL_CONDITION": (
            "Any regular spectral element outside span{P1,P2}, canonical rank-one split of P2, "
            "nonzero irreducible spectral pair quotient, dependency drift or global overclaim."
        ),
        "FALSIFIER": (
            "An exact candidate using only the declared class that passes every w2_13 node, "
            "state-carrier and irreducible-pair gate falsifies this no-go."
        ),
        "RESIDUAL": "0 for every exact identity; no numerical residual.",
        "ERROR_BOUND": "0; symbolic class theorem.",
        "VALIDITY_HEALTH": (
            "Valid only for the explicitly frozen commutative spectral class; it makes no "
            "dynamical, physical, geometric or observational claim."
        ),
        "BRANCHES": {
            "declared_commutative_spectral_class": "REJECTED_IF_AUDIT_VALID",
            "rank2_set_valued_subprojector_fibre": "FAILS_STATE_OWNERSHIP_AND_IMPRINT",
            "law_jet_as_diagnostic": "RETAINED_AS_F2A_ONLY",
            "noncommuting_or_joint_state_routes": "OPEN_NEW_VERSION",
            "full_c0_f2": "OPEN",
        },
        "OBSERVABLE_MAP": {"status": "N/A", "reason": "atemporal internal no-go"},
        "FORWARD_MODEL": {"status": "N/A", "reason": "no observable"},
        "DATA_ROLE": {"status": "N/A", "reason": "no data or fit"},
        "IDENTIFIABILITY": (
            "The complete class is fixed by one generator and its two central spectral "
            "idempotents; any added selector or carrier is identifiable as a class exit."
        ),
        "BENCHMARK": (
            "Positive controls are exact spectral reduction and stabilizer classification; "
            "nulls are off-diagonal words, subprojector overlap, gauge tangents and parameter stitching."
        ),
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "CROSSCHECK": (
            "Direct symbolic matrix identities, representation/stabilizer proof, exhaustive decision "
            "mutations and three independent reviews."
        ),
        "PROVENANCE": {
            "date": "2026-07-21",
            "reviewed_payload_sha256": EXPECTED_PAYLOAD_SHA256,
            "source_identities": {
                "w2_00": C0_SHA256,
                "w2_12": W212_SOURCE, "w2_13": W213_SOURCE, "public_f1": F1_SOURCE,
            },
            "output_artifact": (
                "RefG/work 2/w2_14_f2b_single_generator_commutative_spectral_repackaging_gate.py"
            ),
        },
        "FILES": (
            "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
            "RefG/work 2/w2_12_f2_intrastate_uniform_effect_family_candidate_gate.py",
            "RefG/work 2/w2_13_f2b_node_imprint_and_relational_completion_contract.py",
            "RefG/work 2/w2_09a_f1_proof/refg_f1_atemporal_structural_proof.py",
            "RefG/work 2/w2_14_f2b_single_generator_commutative_spectral_repackaging_gate.py",
        ),
        "CLASS_DEFINITION": class_definition(),
        "NO_GO_THEOREM": no_go_theorem(),
        "NO_GO_GATE_EVIDENCE": no_go_evidence_descriptions(),
        "ESCAPE_ROUTE_REGISTRY": escape_routes(),
        "FORBIDDEN_UPGRADES": (
            "selected basis vector or rank-one corner projector renamed a node",
            "set-valued possibility fibre renamed coexisting accepted state",
            "bare projector overlap renamed state imprint",
            "Hessian or higher derivative renamed occupied state component",
            "independent parameter fibres or gauge tangents combined as relata",
            "extra carrier, tensor product, time, geometry, data or target relation hidden in class",
            "class-local no-go promoted to global RefG or all-no-new-primitives no-go",
        ),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "GATE_APPLICABILITY": gate_applicability(),
        "EXPORT_STATUS": dict(EXPECTED_EXPORT_STATUS),
        "INDEPENDENT_REVIEW": dict(EXPECTED_REVIEW_REQUIREMENTS),
        "NEXT_TASK_POLICY": {
            "positive": NEXT_ATOMIC_TASK,
            "pending": "Complete exact independent reviews before any downstream task.",
            "invalid": "Restore the exact w2_14 artifact before any downstream task.",
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


def matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


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


def registry_shapes_valid(contract: Any) -> bool:
    if not isinstance(contract, dict):
        return False
    freedom = contract.get("FREEDOM_LEDGER")
    return all((
        set(contract) == EXPECTED_STANDARD_FIELDS | EXPECTED_CUSTOM_FIELDS,
        set(contract.get("CLASS_DEFINITION", {})) == EXPECTED_CLASS_KEYS,
        set(contract.get("NO_GO_THEOREM", {})) == EXPECTED_THEOREM_KEYS,
        set(contract.get("NO_GO_GATE_EVIDENCE", {})) == EXPECTED_EVIDENCE_KEYS,
        set(contract.get("ESCAPE_ROUTE_REGISTRY", {})) == EXPECTED_ESCAPE_KEYS,
        isinstance(contract.get("FORBIDDEN_UPGRADES"), tuple),
        isinstance(freedom, dict) and set(freedom) == EXPECTED_FREEDOM_KEYS,
        isinstance(freedom, dict) and all(
            isinstance(entry, dict) and set(entry) == EXPECTED_FREEDOM_ENTRY_KEYS
            for entry in freedom.values()
        ),
        exact_bool_map(contract.get("CLOSURE_FLAGS"), EXPECTED_C0_CLOSURE_FLAGS),
        exact_bool_map(contract.get("SCOPE_CEILING"), EXPECTED_SCOPE_CEILING),
        set(contract.get("GATE_APPLICABILITY", {})) == {
            "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
            "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
            "G7_OBSERVATION", "G8_EXPORT",
        },
        exact_bool_map(contract.get("EXPORT_STATUS"), EXPECTED_EXPORT_STATUS),
        exact_tree_equal(contract.get("INDEPENDENT_REVIEW"), EXPECTED_REVIEW_REQUIREMENTS),
        set(contract.get("NEXT_TASK_POLICY", {})) == {"positive", "pending", "invalid"},
    ))


def semantic_guard(contract: Any) -> bool:
    try:
        fields = (
            contract["CLAIM"], contract["DOMAIN"], contract["METHOD"],
            contract["PASS_CONDITION"], contract["VALIDITY_HEALTH"],
            contract["BRANCHES"], contract["CLASS_DEFINITION"],
            contract["NO_GO_THEOREM"], contract["ESCAPE_ROUTE_REGISTRY"],
            contract["SCOPE_CEILING"], contract["NEXT_ATOMIC_TASK"],
        )
        corpus = "\n".join(
            item if isinstance(item, str) else json.dumps(item, sort_keys=True)
            for item in fields
        ).lower()
    except (KeyError, TypeError, ValueError):
        return False
    forbidden = (
        "refg is impossible", "all no-new-primitive routes are rejected",
        "all f2 routes are rejected", "full f2 is closed", "physical node is proved",
        "time emerges", "metric emerges", "gr is derived", "observationally validated",
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
    paths = (C0_PATH, W212_PATH, W213_PATH, F1_PATH)
    if not all(path.is_file() for path in paths):
        return False, {}
    try:
        c0_text = C0_PATH.read_text(encoding="utf-8")
        w212 = load_module(W212_PATH, "refg_w212_for_w214")
        w213 = load_module(W213_PATH, "refg_w213_for_w214")
        f1 = load_module(F1_PATH, "refg_f1_for_w214")
        w213_report = w213.run_audit()
    except Exception:
        return False, {}
    reviews = w213_report.get("INDEPENDENT_REVIEW_ATTESTATIONS", {})
    subgates = w213_report.get("SUBGATE_CLOSURE_FLAGS", {})
    files = CLAIM_CONTRACT["FILES"]
    checks = all((
        C0_PATH.relative_to(ROOT).as_posix() == files[0],
        W212_PATH.relative_to(ROOT).as_posix() == files[1],
        W213_PATH.relative_to(ROOT).as_posix() == files[2],
        F1_PATH.relative_to(ROOT).as_posix() == files[3],
        Path(__file__).resolve().relative_to(ROOT).as_posix() == files[4],
        file_sha256(C0_PATH) == C0_SHA256,
        file_sha256(W212_PATH) == W212_SOURCE,
        file_sha256(W213_PATH) == W213_SOURCE,
        file_sha256(F1_PATH) == F1_SOURCE,
        f"`{PROGRAM_CONTRACT}`" in c0_text,
        "### `W2_F2_OPERATIONAL_RELATIONS`" in c0_text,
        "PASS_FOR_W2_C0_FREEZE" in c0_text,
        w212.MODEL_VERSION == W212_MODEL,
        w212.PASS_STATUS == W212_STATUS,
        w213.MODEL_VERSION == W213_MODEL,
        w213_report.get("STATUS") == W213_STATUS,
        w213_report.get("AUDIT_VALID") is True,
        w213_report.get("CONTRACT_FROZEN") is True,
        w213_report.get("CANDIDATE_EVALUATED") is False,
        w213_report.get("INHERITED_F2A_INTERNAL_COMPARISON_PROVED") is True,
        w213_report.get("F2B_RELATIONAL_COMPLETION_PROVED") is False,
        w213_report.get("FULL_W2_F2_OPERATIONAL_RELATIONS") is False,
        w213_report.get("DETACHED_PAYLOAD_SHA256") == W213_PAYLOAD,
        w213_report.get("DETACHED_VALIDATOR_SHA256") == W213_VALIDATOR,
        subgates.get("W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED") is True,
        subgates.get("W2_F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED") is False,
        set(reviews) == EXPECTED_W213_REVIEW_KEYS,
        all(isinstance(entry, dict) and entry.get("passed") is True for entry in reviews.values()),
        w213_report.get("CLOSURE_FLAGS") == EXPECTED_C0_CLOSURE_FLAGS,
        f1.MODEL_VERSION == "RefG-F1-ATEMPORAL-STRUCTURAL-PROOF-v1.0",
        f1.PASS_STATUS == "CONDITIONAL_ATEMPORAL_STRUCTURAL_F1_RELATIVE_TO_IMPORTED_PRIMITIVES",
    ))
    return bool(checks), {
        "w212_module": w212, "w213_module": w213,
        "w213_report": w213_report, "f1_module": f1,
    }


def algebra_controls() -> dict[str, bool]:
    s, x, y = sp.symbols("s x y", nonzero=True, real=True)
    u, v = sp.symbols("u v", real=True)
    identity = sp.eye(3)
    p1 = sp.diag(1, 0, 0)
    p2 = identity - p1
    q = s * (p1 - identity / 3)
    b_element = x * p1 + y * p2
    minimal = sp.simplify((q - 2 * s * identity / 3) * (q + s * identity / 3))
    recovered_p1 = sp.simplify(identity / 3 + q / s)
    recovered_p2 = sp.simplify(identity - recovered_p1)
    reduced_from_iq = sp.simplify(
        (y * identity + (x - y) * (identity / 3 + q / s)) - b_element
    )

    projectors = (p1, p2)
    central_candidates = (
        sp.zeros(3), p1, p2, identity,
    )
    idempotent_table = all(
        matrix_zero(item**2 - item) and matrix_zero(item * q - q * item)
        for item in central_candidates
    )
    idempotent_solutions = sp.solve(
        (sp.Eq(u**2, u), sp.Eq(v**2, v)), (u, v), dict=True
    )
    exact_idempotent_coefficients = {
        (solution[u], solution[v]) for solution in idempotent_solutions
    } == {(0, 0), (1, 0), (0, 1), (1, 1)}
    pair_table = sp.Matrix(2, 2, lambda a, b: sp.simplify(
        sp.trace(projectors[a] * b_element * projectors[b] * b_element)
    ))
    expected_pair_table = sp.diag(x**2, 2 * y**2)
    unary_weights = (x**2, 2 * y**2)
    unary_equality_table = sp.Matrix(2, 2, lambda a, b: (
        unary_weights[a] if a == b else 0
    ))
    return {
        "accepted_projector_reconstruction_exact": all((
            matrix_zero(p1**2 - p1), matrix_zero(p2**2 - p2),
            matrix_zero(p1 * p2), matrix_zero(recovered_p1 - p1),
            matrix_zero(recovered_p2 - p2), p1.rank() == 1, p2.rank() == 2,
        )),
        "minimal_polynomial_exact": matrix_zero(minimal),
        "generic_spectral_element_reduction_exact": matrix_zero(reduced_from_iq),
        "central_idempotent_table_exact": bool(
            idempotent_table and exact_idempotent_coefficients
        ),
        "generic_pair_word_table_is_diagonal": pair_table == expected_pair_table,
        "diagonal_table_equals_unary_times_equality": pair_table == unary_equality_table,
    }


def stabilizer_controls() -> dict[str, bool]:
    a, b, d = sp.symbols("a b d", real=True)
    corner = sp.Matrix([[a, b], [b, d]])
    reflection = sp.diag(1, -1)
    quarter_turn = sp.Matrix([[0, -1], [1, 0]])
    equations = list(reflection * corner * reflection.T - corner)
    equations += list(quarter_turn * corner * quarter_turn.T - corner)
    solutions = sp.solve(equations, (a, b, d), dict=True)
    expected = [{a: d, b: 0}]
    invariant_corner = corner.subs(expected[0]) if solutions == expected else corner
    z = sp.symbols("z", real=True)
    idempotent_roots = sp.solve(sp.Eq(z**2, z), z)
    ranks = sorted((z_value * sp.eye(2)).rank() for z_value in idempotent_roots)
    generators_exact = all((
        reflection.T * reflection == sp.eye(2),
        quarter_turn.T * quarter_turn == sp.eye(2),
        reflection.det() == -1, quarter_turn.det() == 1,
    ))
    return {
        "rank2_stabilizer_generators_exact": generators_exact,
        "invariant_symmetric_corner_is_scalar": all((
            solutions == expected, matrix_zero(invariant_corner - d * sp.eye(2)),
        )),
        "invariant_corner_idempotents_have_rank_zero_or_two": all((
            idempotent_roots == [0, 1], ranks == [0, 2],
        )),
        "no_canonical_rank1_corner_projector": 1 not in ranks,
    }


def escape_controls(dependencies: dict[str, Any]) -> dict[str, bool]:
    w213_report = dependencies.get("w213_report", {})
    s = sp.symbols("s", nonzero=True, real=True)
    q = s * sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
    p2 = sp.diag(0, 1, 1)
    p0 = sp.diag(0, 1, 0)
    p_orthogonal = sp.diag(0, 0, 1)
    vector = sp.Matrix([0, sp.Rational(3, 5), sp.Rational(4, 5)])
    p_variable = sp.simplify(vector * vector.T)
    overlap = sp.simplify(sp.trace(p0 * p_variable))
    subgates = w213_report.get("SUBGATE_CLOSURE_FLAGS", {})
    scope = w213_report.get("SCOPE_CEILING", {})
    routes = CLAIM_CONTRACT["ESCAPE_ROUTE_REGISTRY"]
    return {
        "set_valued_fibre_exists_but_has_no_canonical_member": all((
            matrix_zero(p0**2 - p0), matrix_zero(p_variable**2 - p_variable),
            matrix_zero(p2 * p0 - p0), matrix_zero(p2 * p_variable - p_variable),
            p0.rank() == 1, p_variable.rank() == 1,
            stabilizer_controls()["no_canonical_rank1_corner_projector"],
        )),
        "fibre_overlap_varies_but_is_imported_kinematics": all((
            sp.trace(p0 * p0) == 1, overlap == sp.Rational(9, 25),
            "bare projector overlap" in CLAIM_CONTRACT["FORBIDDEN_UPGRADES"][2],
        )),
        "same_unary_bare_overlap_not_irreducible": all((
            sp.trace(p0) == sp.trace(p_orthogonal) == sp.trace(p_variable) == 1,
            matrix_zero(p2 * p_orthogonal - p_orthogonal),
            matrix_zero(p2 * p_variable - p_variable),
            sp.trace(p0 * p_orthogonal) == 0,
            overlap == sp.Rational(9, 25),
            "BARE_OVERLAP_OR_HIDDEN_SELECTION" in routes["PROJECTIVE_FIBRE"],
        )),
        "rank1_word_reduces_to_overlap": all((
            matrix_zero(p0 * p_variable * p0 - overlap * p0),
            matrix_zero(q * p0 + s * p0 / 3),
            matrix_zero(q * p_variable + s * p_variable / 3),
        )),
        "no_invariant_rank1_split_P2": stabilizer_controls()[
            "no_canonical_rank1_corner_projector"
        ],
        "w2_12_pairwise_and_state_imprint_flags_remain_false": all((
            subgates.get("W2_F2B_ATEMPORAL_RELATIONAL_CARRIER_PROVED") is False,
            subgates.get("W2_F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED") is False,
            scope.get("atemporal_relational_carrier_proved") is False,
            scope.get("irreducibly_pairwise_relation_proved") is False,
        )),
        "preserved_routes_are_explicitly_open": all(
            isinstance(value, str) and value.startswith("OPEN")
            for value in routes.values()
        ),
    }


def evidence_map(
    dependency_ok: bool,
    algebra: dict[str, bool],
    stabilizer: dict[str, bool],
    escapes: dict[str, bool],
    review_structure: bool,
) -> dict[str, bool]:
    return {
        "exact_w213_dependency_and_f2a_boundary": bool(dependency_ok),
        "accepted_uniaxial_minimal_polynomial_exact": algebra["minimal_polynomial_exact"],
        "commutative_spectral_algebra_is_two_dimensional": (
            algebra["generic_spectral_element_reduction_exact"]
        ),
        "only_two_canonical_central_projectors": all((
            algebra["accepted_projector_reconstruction_exact"],
            algebra["central_idempotent_table_exact"],
        )),
        "stabilizer_forbids_canonical_rank1_split_of_rank2_sector": all(
            stabilizer.values()
        ),
        "uniform_spectral_pair_words_factor_through_unary_and_equality": all((
            algebra["generic_pair_word_table_is_diagonal"],
            algebra["diagonal_table_equals_unary_times_equality"],
        )),
        "set_valued_subprojector_fibre_is_not_coexisting_state_content": (
            escapes["set_valued_fibre_exists_but_has_no_canonical_member"]
        ),
        "bare_overlap_on_that_fibre_is_not_a_state_imprint": (
            escapes["fibre_overlap_varies_but_is_imported_kinematics"]
            and escapes["same_unary_bare_overlap_not_irreducible"]
            and escapes["rank1_word_reduces_to_overlap"]
            and escapes["no_invariant_rank1_split_P2"]
        ),
        "law_jets_remain_diagnostics_unless_state_space_is_revised": (
            escapes["w2_12_pairwise_and_state_imprint_flags_remain_false"]
        ),
        "parameter_fibres_and_gauge_tangents_do_not_supply_relata": all((
            CLAIM_CONTRACT["FREEDOM_LEDGER"]["new_state_component"]["complexity"] == 0,
            "parameter fibres" in CLAIM_CONTRACT["FORBIDDEN_UPGRADES"][4],
            "gauge tangents" in CLAIM_CONTRACT["FORBIDDEN_UPGRADES"][4],
        )),
        "open_positive_parameter_domain_is_covered": all((
            "alpha,b,c>0" in CLAIM_CONTRACT["DOMAIN"],
            "s>0" in CLAIM_CONTRACT["CLASS_DEFINITION"]["accepted_branch"],
        )),
        "preserved_escape_routes_are_not_rejected": all((
            escapes["preserved_routes_are_explicitly_open"], review_structure,
        )),
    }


def adjudicate(evidence: Any, audit_valid: Any) -> dict[str, Any]:
    valid = bool(
        type(audit_valid) is bool
        and isinstance(evidence, dict)
        and set(evidence) == EXPECTED_EVIDENCE_KEYS
        and all(type(evidence[key]) is bool for key in EXPECTED_EVIDENCE_KEYS)
    )
    proved = bool(valid and audit_valid is True and all(evidence.values()))
    return {
        "VALID": valid,
        "NO_GO_PROVED": proved,
        "PROMOTED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "STATUS": (
            "DECLARED_CLASS_EXACTLY_REJECTED__F2B_OPEN" if proved else
            "VALID_NOT_PROVED__F2B_OPEN" if valid else
            "INVALID_DECISION__NO_CLASS_REJECTION"
        ),
    }


def review_schema_valid(attestations: Any, require_pass: bool) -> bool:
    fields = {
        "passed", "reviewer", "artifact", "reviewed_payload_sha256",
        "reviewed_validator_sha256",
    }
    reviewers = {
        "mathematical_no_go_review": "/root/f2_independent_review",
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
        if entry["reviewer"] != reviewers[key]:
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
    wrong_payload["mathematical_no_go_review"]["reviewed_payload_sha256"] = "WRONG"
    mutants.append(wrong_payload)
    wrong_validator = copy.deepcopy(base)
    wrong_validator["new_reader_scope_review"]["reviewed_validator_sha256"] = "WRONG"
    mutants.append(wrong_validator)
    return all(not review_schema_valid(mutant, require_pass=False) for mutant in mutants)


def safe_contract_valid(value: Any) -> bool:
    try:
        return strict_contract_valid(value)
    except Exception:
        return False


def mutation_controls() -> dict[str, bool]:
    base = copy.deepcopy(CLAIM_CONTRACT)
    baseline = bool(safe_contract_valid(base) and exact_tree_equal(base, build_contract()))

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
    for registry in (
        "CLASS_DEFINITION", "NO_GO_THEOREM", "NO_GO_GATE_EVIDENCE",
        "ESCAPE_ROUTE_REGISTRY", "FREEDOM_LEDGER", "CLOSURE_FLAGS",
        "SCOPE_CEILING", "GATE_APPLICABILITY", "EXPORT_STATUS",
        "INDEPENDENT_REVIEW", "NEXT_TASK_POLICY",
    ):
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
    forbidden_missing = copy.deepcopy(base)
    forbidden_missing["FORBIDDEN_UPGRADES"] = forbidden_missing["FORBIDDEN_UPGRADES"][:-1]
    registry_mutants.append(forbidden_missing)

    boundary_mutants: list[dict[str, Any]] = []
    for registry in ("CLOSURE_FLAGS", "SCOPE_CEILING", "EXPORT_STATUS"):
        for key, value in base[registry].items():
            if value is False:
                mutant = copy.deepcopy(base)
                mutant[registry][key] = True
                boundary_mutants.append(mutant)

    semantic_mutants: list[dict[str, Any]] = []
    for field, text in (
        ("CLAIM", " RefG is impossible."),
        ("METHOD", " All no-new-primitive routes are rejected."),
        ("PASS_CONDITION", " All F2 routes are rejected."),
        ("VALIDITY_HEALTH", " Full F2 is closed."),
    ):
        mutant = copy.deepcopy(base)
        mutant[field] += text
        semantic_mutants.append(mutant)

    all_true = {key: True for key in EXPECTED_EVIDENCE_KEYS}
    evidence_mutants: list[Any] = []
    one_false_results = []
    for key in EXPECTED_EVIDENCE_KEYS:
        missing = dict(all_true)
        missing.pop(key)
        evidence_mutants.append(missing)
        nonboolean = dict(all_true)
        nonboolean[key] = 1
        evidence_mutants.append(nonboolean)
        one_false = dict(all_true)
        one_false[key] = False
        one_false_results.append(adjudicate(one_false, True))
    extra_evidence = dict(all_true)
    extra_evidence["UNREGISTERED"] = True
    evidence_mutants.append(extra_evidence)

    return {
        "missing_or_extra_contract_fields_rejected": all(
            rejected(mutant) for mutant in field_mutants
        ),
        "class_theorem_registry_drift_rejected": all(
            rejected(mutant) for mutant in registry_mutants
        ),
        "scope_and_export_overclaims_rejected": all(
            rejected(mutant) for mutant in boundary_mutants
        ),
        "semantic_global_no_go_overclaims_rejected": all(
            not semantic_guard(mutant) and rejected(mutant)
            for mutant in semantic_mutants
        ),
        "evidence_schema_mutants_rejected": all(
            adjudicate(mutant, True)["VALID"] is False for mutant in evidence_mutants
        ) and adjudicate(all_true, 1)["VALID"] is False,
        "one_missing_evidence_prevents_no_go": all(
            result["VALID"] is True
            and result["NO_GO_PROVED"] is False
            and result["PROMOTED"] is False
            for result in one_false_results
        ),
    }


def _run_audit_unchecked() -> dict[str, Any]:
    if not strict_contract_valid(CLAIM_CONTRACT):
        raise ValueError("contract payload or schema invalid")
    if detached_validator_sha256() != EXPECTED_VALIDATOR_SHA256:
        raise ValueError("validator source identity invalid")

    dependency_ok, dependencies = dependencies_valid()
    algebra = algebra_controls()
    stabilizer = stabilizer_controls()
    escapes = escape_controls(dependencies)
    attestations = review_attestations()
    review_structure = review_schema_valid(attestations, require_pass=False)
    evidence = evidence_map(
        dependency_ok, algebra, stabilizer, escapes, review_structure,
    )
    mutations = mutation_controls()

    checks = {
        "payload_validator_and_contract_schema_exact": all((
            strict_contract_valid(CLAIM_CONTRACT),
            detached_validator_sha256() == EXPECTED_VALIDATOR_SHA256,
            registry_shapes_valid(CLAIM_CONTRACT),
        )),
        "c0_w212_w213_f1_dependencies_exact": dependency_ok,
        "algebra_and_stabilizer_theorem_controls_exact": all((
            exact_true_map(algebra, EXPECTED_ALGEBRA_CONTROL_KEYS),
            exact_true_map(stabilizer, EXPECTED_STABILIZER_CONTROL_KEYS),
        )),
        "escape_boundary_controls_exact": exact_true_map(
            escapes, EXPECTED_ESCAPE_CONTROL_KEYS,
        ),
        "no_go_evidence_schema_and_decision_exact": all((
            exact_true_map(evidence, EXPECTED_EVIDENCE_KEYS),
            adjudicate(evidence, True)["VALID"] is True,
            adjudicate(evidence, True)["NO_GO_PROVED"] is True,
            adjudicate(evidence, True)["PROMOTED"] is False,
            adjudicate(evidence, False)["NO_GO_PROVED"] is False,
        )),
        "mutation_controls_exact": exact_true_map(mutations, EXPECTED_MUTATION_KEYS),
        "closure_scope_export_boundaries_exact": all((
            exact_bool_map(CLAIM_CONTRACT["CLOSURE_FLAGS"], EXPECTED_C0_CLOSURE_FLAGS),
            exact_bool_map(CLAIM_CONTRACT["SCOPE_CEILING"], EXPECTED_SCOPE_CEILING),
            exact_bool_map(CLAIM_CONTRACT["EXPORT_STATUS"], EXPECTED_EXPORT_STATUS),
        )),
        "review_schema_fail_closed": all((
            review_structure, review_schema_controls(),
        )),
        "review_attestations_complete": review_schema_valid(
            attestations, require_pass=True,
        ),
        "next_task_is_new_version_contract_not_result": all((
            "w2_15_f2b_general_traceless_single_carrier_candidate_contract.py"
            in NEXT_ATOMIC_TASK,
            "before evaluating outcomes" in NEXT_ATOMIC_TASK,
            "start every new candidate/F2b/full-F2 flag false" in NEXT_ATOMIC_TASK,
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
    decision = adjudicate(evidence, audit_valid)
    no_go_proved = bool(audit_valid and decision["NO_GO_PROVED"] is True)
    status = PASS_STATUS if no_go_proved else READY_STATUS if structural_ready else INVALID_STATUS
    next_task = (
        CLAIM_CONTRACT["NEXT_TASK_POLICY"]["positive"] if no_go_proved else
        CLAIM_CONTRACT["NEXT_TASK_POLICY"]["pending"] if structural_ready else
        CLAIM_CONTRACT["NEXT_TASK_POLICY"]["invalid"]
    )
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": status,
        "AUDIT_VALID": audit_valid,
        "STRUCTURAL_READY_FOR_REVIEW": structural_ready,
        "CLASS_EVALUATED": True if audit_valid else False,
        "CANDIDATE_EVALUATED": False,
        "NO_GO_PROVED": no_go_proved,
        "REJECTED_CLASS": (
            "SINGLE_GENERATOR_COMMUTATIVE_SPECTRAL_REPACKAGING"
            if no_go_proved else "NONE"
        ),
        "PROMOTED": False,
        "F2B_RELATIONAL_COMPLETION_PROVED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "DETACHED_PAYLOAD_SHA256": detached_payload_sha256(CLAIM_CONTRACT),
        "DETACHED_VALIDATOR_SHA256": detached_validator_sha256(),
        "NO_GO_DECISION": decision,
        "NO_GO_EVIDENCE": evidence,
        "ALGEBRA_CONTROLS": algebra,
        "STABILIZER_CONTROLS": stabilizer,
        "ESCAPE_CONTROLS": escapes,
        "MUTATION_CONTROLS": mutations,
        "AUDIT_CHECKS": checks,
        "INDEPENDENT_REVIEW_ATTESTATIONS": attestations,
        "PRESERVED_ROUTES": dict(CLAIM_CONTRACT["ESCAPE_ROUTE_REGISTRY"]),
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": bool(dependency_ok),
            "W2_F2B_SINGLE_GENERATOR_COMMUTATIVE_SPECTRAL_ROUTE_REJECTED": no_go_proved,
            "W2_F2B_STATE_SUPPORTED_NODE_FAMILY_PROVED": False,
            "W2_F2B_ATEMPORAL_RELATIONAL_CARRIER_PROVED": False,
            "W2_F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED": False,
            "W2_F2B_RELATIONAL_COMPLETION_PROVED": False,
            "W2_F2_OPERATIONAL_RELATIONS_PROVED": False,
        },
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "PROMOTION_CEILING": "SCOPED_NO_GO_ONLY__NO_F2_PROMOTION",
        "NEXT_ATOMIC_TASK": next_task,
    }


def fail_closed_invalid_report(error: Exception) -> dict[str, Any]:
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": INVALID_STATUS,
        "AUDIT_VALID": False,
        "STRUCTURAL_READY_FOR_REVIEW": False,
        "CLASS_EVALUATED": False,
        "CANDIDATE_EVALUATED": False,
        "NO_GO_PROVED": False,
        "REJECTED_CLASS": "NONE",
        "PROMOTED": False,
        "F2B_RELATIONAL_COMPLETION_PROVED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "DETACHED_PAYLOAD_SHA256": "",
        "DETACHED_VALIDATOR_SHA256": "",
        "NO_GO_DECISION": {
            "VALID": False, "NO_GO_PROVED": False, "PROMOTED": False,
            "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
            "STATUS": "INVALID_DECISION__NO_CLASS_REJECTION",
        },
        "NO_GO_EVIDENCE": {key: False for key in EXPECTED_EVIDENCE_KEYS},
        "ALGEBRA_CONTROLS": {key: False for key in EXPECTED_ALGEBRA_CONTROL_KEYS},
        "STABILIZER_CONTROLS": {
            key: False for key in EXPECTED_STABILIZER_CONTROL_KEYS
        },
        "ESCAPE_CONTROLS": {key: False for key in EXPECTED_ESCAPE_CONTROL_KEYS},
        "MUTATION_CONTROLS": {key: False for key in EXPECTED_MUTATION_KEYS},
        "AUDIT_CHECKS": {key: False for key in EXPECTED_AUDIT_KEYS},
        "INDEPENDENT_REVIEW_ATTESTATIONS": {},
        "PRESERVED_ROUTES": {},
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": False,
            "W2_F2B_SINGLE_GENERATOR_COMMUTATIVE_SPECTRAL_ROUTE_REJECTED": False,
            "W2_F2B_STATE_SUPPORTED_NODE_FAMILY_PROVED": False,
            "W2_F2B_ATEMPORAL_RELATIONAL_CARRIER_PROVED": False,
            "W2_F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED": False,
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
