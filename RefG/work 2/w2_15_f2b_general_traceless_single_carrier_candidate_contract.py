"""Frozen, outcome-neutral contract for the selected revised W2-F2b candidate.

This file does not claim that F2b or full F2 is proved.  It freezes one abstract
traceless endomorphism A and the two channels derived from A by transpose,

    S=(A+A.T)/2,       R=(A-A.T)/2,

before any candidate outcome is evaluated.  The old F1 state is the exact
R=0 restriction.  The next artifact must revalidate F1 and F2a and then pass
every frozen w2_13 gate in one identity-pinned aggregate candidate.

S and R have no spacetime, material, vortex, pressure or observable meaning
here.  Such interpretations remain later derivation duties.
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
    "W2-F2B-GENERAL-TRACELESS-SINGLE-CARRIER-CANDIDATE-CONTRACT-"
    "v1.0-internal"
)
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"
W213_MODEL = "W2-F2B-NODE-IMPRINT-RELATIONAL-COMPLETION-CONTRACT-v1.0-internal"
W213_STATUS = "W2_F2B_CONTRACT_FROZEN__NO_CANDIDATE_EVALUATED__FULL_F2_OPEN"
W214_MODEL = (
    "W2-F2B-SINGLE-GENERATOR-COMMUTATIVE-SPECTRAL-REPACKAGING-NO-GO-"
    "v1.0-internal"
)
W214_STATUS = "EXACT_SINGLE_GENERATOR_COMMUTATIVE_SPECTRAL_REPACKAGING_NO_GO__F2B_OPEN"

C0_SHA256 = "3E0EFB2D635E7E5605F9D7EDFA99538644D7C21311989C478C4A6AF1854890EB"
W213_SOURCE = "0BABF2EB701845452E2E809B1420857D04A842FCC5FEB24BD732523E2C88E347"
W214_SOURCE = "CB44AA3C6F698BF787A18696EF1FCB2C3C8C7D72AD29A558F68FFF834AEBEB56"
W213_PAYLOAD = "1B7D2921C78DB177CE401E04B5359ED28988DB2CF86E89A3159407BDF0B18733"
W213_VALIDATOR = "98F4A8B70742F9F709629486DC1D948BC22CAB12C74F7DBCA99E3B616FE3FC68"
W214_PAYLOAD = "D81E577D3C1F46CE1BC8E3F464AC06DEC79054344780B44876F5A623AC1A1DA0"
W214_VALIDATOR = "A59353C5BBBEADAC35C6EA014BF02D8C6E96C6B3409843AF00C00BF36AFD673B"

READY_STATUS = "W2_F2B_REVISED_SINGLE_CARRIER_CONTRACT_READY_FOR_REVIEW__UNEVALUATED"
FROZEN_STATUS = "W2_F2B_REVISED_SINGLE_CARRIER_CONTRACT_FROZEN__UNEVALUATED"
INVALID_STATUS = "W2_F2B_REVISED_SINGLE_CARRIER_CONTRACT_INVALID__NO_EVALUATION"
EXPECTED_PAYLOAD_SHA256 = "C4808257C0334AAC9CD83C59208B6240650B12D01EF92F9F39D13DCCBBBDBF76"
EXPECTED_VALIDATOR_SHA256 = "A82E1433B8C1F487964FC89514F30310BDAB80B30B2125434982A1919B83975B"

ROOT = Path(__file__).resolve().parents[2]
C0_PATH = Path(__file__).with_name("w2_00_foundation_to_einstein_contract.md")
W213_PATH = Path(__file__).with_name(
    "w2_13_f2b_node_imprint_and_relational_completion_contract.py"
)
W214_PATH = Path(__file__).with_name(
    "w2_14_f2b_single_generator_commutative_spectral_repackaging_gate.py"
)

NEXT_ATOMIC_TASK = (
    "Create w2_16_f2b_general_traceless_single_carrier_candidate_gate.py and, without "
    "altering this frozen candidate, exactly derive its accepted quotient, revalidate F1 "
    "and w2_12 F2a, evaluate all w2_13 screening gates, audit the flat relative modulus "
    "and complete common action, run positive/null/adversarial controls, and close full F2 "
    "only if every gate and independent review passes."
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
    "CANDIDATE_DEFINITION", "LAW_AND_BRANCH", "NODE_AND_CARRIER_ANSATZ",
    "EQUIVALENCE_AND_PAIR_DOMAIN", "OPEN_DOMAIN_AND_NULLS", "OUTCOME_BLINDNESS",
    "REVALIDATION_DUTIES", "F2B_GATE_DUTIES", "FORBIDDEN_UPGRADES",
    "SCOPE_CEILING", "GATE_APPLICABILITY", "EXPORT_STATUS",
    "INDEPENDENT_REVIEW", "NEXT_TASK_POLICY", "NEXT_ATOMIC_TASK",
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
    "candidate_contract_frozen": True,
    "candidate_evaluated": False,
    "new_single_carrier_imported": True,
    "symmetric_and_skew_channels_derived": True,
    "old_f1_exact_restriction_declared": True,
    "f1_revalidated_in_extended_state": False,
    "f2a_revalidated_in_extended_state": False,
    "state_supported_nodes_proved": False,
    "atemporal_state_carrier_proved": False,
    "irreducible_pair_relation_proved": False,
    "complete_common_action_proved": False,
    "flat_relative_modulus_accepted": False,
    "full_W2_F2_operational_relations": False,
    "time_memory_or_causality": False,
    "physical_space_metric_or_observable": False,
    "GR_PN_or_PPN_bridge": False,
    "observational_validation": False,
}
EXPECTED_EXPORT_STATUS = {
    "CANON": False, "ARTICLE": False, "GITHUB": False, "ZENODO": False,
}
EXPECTED_CANDIDATE_KEYS = frozenset({
    "primitive", "derived_channels", "ambient_algebra", "equivalence",
    "old_restriction", "new_content", "semantic_boundary",
})
EXPECTED_LAW_KEYS = frozenset({
    "invariants", "law", "parameter_domain", "accepted_branch",
    "relative_modulus", "mixed_coefficients", "undefined_points",
})
EXPECTED_NODE_KEYS = frozenset({
    "symmetric_node", "skew_node", "ownership", "carrier", "joint_report",
    "unary_reductions", "candidate_only_not_result",
})
EXPECTED_EQUIVALENCE_KEYS = frozenset({
    "common_action", "why_not_independent_gauge", "typed_nodes",
    "pair_domain", "relabel_policy", "report_invariance_duty",
})
EXPECTED_NULL_KEYS = frozenset({
    "predeclared_open_domain", "reference_zero", "symmetric_only",
    "skew_only", "commuting_branch", "factorized_pair_rule",
    "projective_bare_overlap", "undefined_normalization",
})
EXPECTED_BLINDNESS_KEYS = frozenset({
    "candidate_selected_before_outcomes", "no_observational_constants",
    "no_target_relation_table", "no_spacetime_import", "all_result_flags_false",
    "failure_does_not_authorize_patch", "new_version_on_revision",
})
EXPECTED_REVALIDATION_KEYS = frozenset({
    "exact_old_law_restriction", "full_extended_f1",
    "embedded_f2a_operator_family", "same_aggregate_identity",
    "new_flat_directions_classified", "no_automatic_inheritance",
})
EXPECTED_F2B_DUTY_KEYS = frozenset({
    "w213_exact_screen_imported", "state_node_support",
    "joint_carrier_support", "common_action_and_pair_domain",
    "same_unary_different_joint", "irreducible_quotient",
    "complete_invariance", "open_domain_and_nulls", "no_f3_semantics",
    "candidate_specific_independent_audit",
})
EXPECTED_FREEDOM_KEYS = frozenset({
    "ambient_dimension", "single_carrier_A", "transpose_split",
    "common_basis_action", "inherited_alpha_b_c", "new_eta_d",
    "mixed_couplings", "node_maps", "carrier_map", "joint_report",
    "relative_modulus", "preferred_basis_axis_or_labels",
    "physical_interpretation", "data_fitted_parameters",
})
EXPECTED_FREEDOM_ENTRY_KEYS = frozenset({
    "source", "allowed_range", "scale", "complexity",
})
EXPECTED_GATE_KEYS = frozenset({
    "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
    "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
    "G7_OBSERVATION", "G8_EXPORT",
})
EXPECTED_DEFINITION_CONTROL_KEYS = frozenset({
    "transpose_split_exact", "channels_have_required_symmetry_and_trace",
    "single_carrier_reconstruction_exact", "old_law_restriction_exact",
    "skew_invariant_nonnegative_prototype", "candidate_parameter_domain_open",
    "commutator_report_joint_not_unary_syntax", "all_candidate_outcomes_false",
})
EXPECTED_MUTATION_KEYS = frozenset({
    "missing_or_extra_contract_fields_rejected", "registry_drift_rejected",
    "scope_and_export_overclaims_rejected", "outcome_injection_rejected",
    "physical_semantics_injection_rejected", "dependency_identity_mutation_rejected",
})
EXPECTED_AUDIT_KEYS = frozenset({
    "payload_validator_and_contract_schema_exact",
    "w213_and_scoped_no_go_dependencies_exact",
    "candidate_definition_coherence_exact",
    "candidate_outcome_neutrality_exact",
    "mutation_controls_exact",
    "closure_scope_export_boundaries_exact",
    "review_schema_fail_closed",
    "review_attestations_complete",
    "next_task_is_exact_candidate_evaluation",
})
EXPECTED_REVIEW_KEYS = frozenset({
    "candidate_architecture_review", "fail_closed_code_review", "new_reader_scope_review",
})
EXPECTED_REVIEW_REQUIREMENTS = {
    "candidate_architecture_review": (
        "independent extension-economy, law, same-chain and anti-target audit"
    ),
    "fail_closed_code_review": (
        "independent schema, identity, mutation and no-premature-closure audit"
    ),
    "new_reader_scope_review": (
        "independent standalone clarity, provenance and semantic-boundary audit"
    ),
}

REVIEW_ATTESTED_PAYLOAD_IDS = {
    "candidate_architecture_review": "C4808257C0334AAC9CD83C59208B6240650B12D01EF92F9F39D13DCCBBBDBF76",
    "fail_closed_code_review": "C4808257C0334AAC9CD83C59208B6240650B12D01EF92F9F39D13DCCBBBDBF76",
    "new_reader_scope_review": "C4808257C0334AAC9CD83C59208B6240650B12D01EF92F9F39D13DCCBBBDBF76",
}
REVIEW_ATTESTED_VALIDATOR_IDS = {
    "candidate_architecture_review": "A82E1433B8C1F487964FC89514F30310BDAB80B30B2125434982A1919B83975B",
    "fail_closed_code_review": "A82E1433B8C1F487964FC89514F30310BDAB80B30B2125434982A1919B83975B",
    "new_reader_scope_review": "A82E1433B8C1F487964FC89514F30310BDAB80B30B2125434982A1919B83975B",
}


def candidate_definition() -> dict[str, str]:
    return {
        "primitive": (
            "One abstract real traceless endomorphism A in sl(3,R); A is the only new "
            "accepted-state primitive in this version."
        ),
        "derived_channels": (
            "S=(A+A^T)/2 in Sym_0(3,R) and R=(A-A^T)/2 in so(3); they are exact "
            "transpose projections of A, not separately imported fields."
        ),
        "ambient_algebra": (
            "The inherited real 3x3 endomorphism algebra with identity, transpose, product "
            "and trace; no tensor product, spacetime or external graph is added."
        ),
        "equivalence": (
            "One common internal basis change A -> O A O^T for O in O(3), acting "
            "simultaneously on S and R."
        ),
        "old_restriction": (
            "R=0 and S=Q gives exactly the frozen F1 carrier and law; this is an exact "
            "restriction, not automatic proof for the extended accepted branch."
        ),
        "new_content": (
            "The skew transpose channel and its two positive law parameters eta,d.  No "
            "preferred direction, node labels, pair table or physical interpretation is added."
        ),
        "semantic_boundary": (
            "A,S,R are pre-spatial internal algebra objects.  Symmetric and skew do not yet "
            "mean pressure, strain, rotation, vortex, matter, geometry or an observable."
        ),
    }


def law_and_branch() -> dict[str, str]:
    return {
        "invariants": "I2=Tr(S^2), I3=Tr(S^3), J=-Tr(R^2)>=0.",
        "law": (
            "U(A)=-alpha I2/2-b I3/3+c I2^2/4-eta J/2+d J^2/4."
        ),
        "parameter_domain": "alpha,b,c,eta,d>0; no fitted or observed constants.",
        "accepted_branch": (
            "Global minima must be derived, not assumed: expected candidate branch has the "
            "old uniaxial S amplitude s_+>0, J=eta/d>0, and an unfixed relative orientation."
        ),
        "relative_modulus": (
            "The law is separable in S and R, so relative orientation is a candidate flat "
            "modulus.  Its legitimacy, stability class and non-gauge status are mandatory "
            "w2_16 tests, not conclusions of this contract."
        ),
        "mixed_coefficients": (
            "Every mixed invariant coefficient is fixed exactly to zero by this candidate law; "
            "this architectural choice is charged and must survive robustness criticism."
        ),
        "undefined_points": (
            "U itself is polynomial and defined everywhere.  Only normalized diagnostic "
            "relations may be undefined at s=0 or J=0; raw carriers remain defined."
        ),
    }


def node_and_carrier_ansatz() -> dict[str, str]:
    return {
        "symmetric_node": (
            "Candidate node N_S is the nonzero transpose-even restriction S of the same A."
        ),
        "skew_node": (
            "Candidate node N_R is the nonzero transpose-odd restriction R of the same A."
        ),
        "ownership": (
            "The proposed ownership certificate is the equivariant projection/reconstruction "
            "pair A -> (S,R) and A=S+R; w2_16 must prove that this meets w2_13 rather than "
            "merely renaming matrix sectors."
        ),
        "carrier": (
            "Candidate joint carrier C=[S,R]=SR-RS, generated by the inherited product from "
            "the two coexisting restrictions of one state."
        ),
        "joint_report": (
            "Raw report K=Tr(C^T C).  On the proposed nonzero branch the optional normalized "
            "report tau=K/(s^2 J) must be derived with its exact domain; no value is preassigned."
        ),
        "unary_reductions": (
            "Complete candidate unary data are the separate O(3)-invariant classes of S and R; "
            "on the accepted branch these reduce to the S spectrum and J respectively."
        ),
        "candidate_only_not_result": (
            "Calling these objects node, carrier and report is an ansatz.  Every corresponding "
            "proof flag remains false until the separately reviewed evaluation."
        ),
    }


def equivalence_and_pair_domain() -> dict[str, str]:
    return {
        "common_action": (
            "Pairs inherit one diagonal/common O(3) conjugation from the single endomorphism A."
        ),
        "why_not_independent_gauge": (
            "Independent rotations of S and R do not preserve their product as restrictions of "
            "one endomorphism algebra; w2_16 must audit whether they are global degeneracy "
            "motions or hidden gauge, rather than deciding this by wording."
        ),
        "typed_nodes": (
            "Transpose parity distinguishes N_S and N_R covariantly; they cannot be exchanged "
            "by the declared common O(3) basis action."
        ),
        "pair_domain": (
            "The proposed domain is the two typed same-state nodes and their ordered cross pair; "
            "self pairs are reference unary/null controls."
        ),
        "relabel_policy": (
            "No arbitrary labels occur.  Any representation-level renaming preserving transpose "
            "type and the common action must leave the reported scalar unchanged."
        ),
        "report_invariance_duty": (
            "w2_16 must prove K and any normalized quotient invariant under the complete accepted "
            "equivalence, including every discrete equivalence found in the audit."
        ),
    }


def open_domain_and_nulls() -> dict[str, str]:
    return {
        "predeclared_open_domain": (
            "alpha,b,c,eta,d>0 and accepted states with S!=0, R!=0, [S,R]!=0; the "
            "generic relative-orientation interior must be characterized exactly."
        ),
        "reference_zero": "A=0 gives S=R=C=K=0 but need not be an accepted minimum.",
        "symmetric_only": "R=0 gives the exact old law restriction and C=K=0.",
        "skew_only": "S=0 gives C=K=0.",
        "commuting_branch": "[S,R]=0 gives C=K=0 and is outside the positive relational domain.",
        "factorized_pair_rule": (
            "Any report reconstructed only from separate unary invariants and typed equality is null."
        ),
        "projective_bare_overlap": (
            "A freely selected projector overlap without state reconstruction remains the w2_14 null."
        ),
        "undefined_normalization": (
            "tau is undefined when s=0 or J=0; no limiting value may be silently assigned."
        ),
    }


def outcome_blindness() -> dict[str, bool]:
    return {
        "candidate_selected_before_outcomes": True,
        "no_observational_constants": True,
        "no_target_relation_table": True,
        "no_spacetime_import": True,
        "all_result_flags_false": True,
        "failure_does_not_authorize_patch": True,
        "new_version_on_revision": True,
    }


def revalidation_duties() -> dict[str, str]:
    return {
        "exact_old_law_restriction": "Prove U(S,R=0)=V_F1(S) identically.",
        "full_extended_f1": (
            "Derive all global minima, quotient classes, stabilizer and normal/flat Hessian sectors."
        ),
        "embedded_f2a_operator_family": (
            "Recompute the extended Hessian and prove the exact old S-sector F2a family survives."
        ),
        "same_aggregate_identity": (
            "Pin one source identity for the state, law, nodes, carrier, quotient and all gates."
        ),
        "new_flat_directions_classified": (
            "Distinguish common gauge rotations, independent global degeneracy motions, physical "
            "relative moduli and unstable directions exactly."
        ),
        "no_automatic_inheritance": (
            "The old F1/F2a results are lemmas only; no extended-state pass is inherited by name."
        ),
    }


def f2b_gate_duties() -> dict[str, str]:
    return {
        "w213_exact_screen_imported": "Use every exact w2_13 screening key without deletion.",
        "state_node_support": "Prove both proposed nodes coexist and are state/law generated.",
        "joint_carrier_support": "Prove [S,R] belongs to the accepted state and links both nodes.",
        "common_action_and_pair_domain": "Derive the full action and admissible pairs.",
        "same_unary_different_joint": (
            "Exhibit exact accepted states with equal complete unary classes and unequal joint report."
        ),
        "irreducible_quotient": (
            "Prove the joint report cannot factor through unary data, typed equality or w2_14 nulls."
        ),
        "complete_invariance": "Prove representative and relabelling invariance.",
        "open_domain_and_nulls": "Prove nonzero open support and every predeclared null.",
        "no_f3_semantics": "Keep formation, persistence, propagation, memory and causality absent.",
        "candidate_specific_independent_audit": "Require three exact reviews before any closure.",
    }


def freedom_ledger() -> dict[str, dict[str, Any]]:
    zero = {"source": "none", "allowed_range": 0, "scale": "candidate", "complexity": 0}
    return {
        "ambient_dimension": {
            "source": "inherited F1 matrix representation", "allowed_range": 3,
            "scale": "internal representation", "complexity": 0,
        },
        "single_carrier_A": {
            "source": "new version primitive", "allowed_range": "sl(3,R)",
            "scale": "one accepted-state carrier", "complexity": 8,
        },
        "transpose_split": {
            "source": "derived exact projection", "allowed_range": "S plus R",
            "scale": "fixed map", "complexity": 0,
        },
        "common_basis_action": {
            "source": "inherited internal delta and matrix algebra", "allowed_range": "O(3)",
            "scale": "one common action", "complexity": 0,
        },
        "inherited_alpha_b_c": {
            "source": "exact F1 law", "allowed_range": "alpha,b,c>0",
            "scale": "three universal parameters", "complexity": 3,
        },
        "new_eta_d": {
            "source": "new skew radial law", "allowed_range": "eta,d>0",
            "scale": "two universal parameters", "complexity": 2,
        },
        "mixed_couplings": {
            "source": "candidate architectural zero", "allowed_range": 0,
            "scale": "all mixed invariant coefficients", "complexity": 0,
        },
        "node_maps": {
            "source": "transpose projections", "allowed_range": "fixed",
            "scale": "S,R", "complexity": 0,
        },
        "carrier_map": {
            "source": "inherited matrix commutator", "allowed_range": "fixed",
            "scale": "[S,R]", "complexity": 0,
        },
        "joint_report": {
            "source": "inherited trace norm", "allowed_range": "fixed K and derived tau",
            "scale": "one raw and one normalized scalar", "complexity": 0,
        },
        "relative_modulus": {
            "source": "accepted-state quotient if proved", "allowed_range": "to be derived",
            "scale": "not a fitted parameter", "complexity": 0,
        },
        "preferred_basis_axis_or_labels": {**zero, "scale": "description"},
        "physical_interpretation": {**zero, "scale": "semantics"},
        "data_fitted_parameters": {**zero, "scale": "data"},
    }


def gate_applicability() -> dict[str, str]:
    return {
        "G0_GOAL": "REQUIRED - one selected revised candidate frozen before outcomes",
        "G1_CONVENTIONS": "REQUIRED - state, law, equivalence, domain and nulls exact",
        "G2_CORE_ALGEBRA": "DEFERRED_TO_W2_16 - derive minima, quotient and relation",
        "G3_STRUCTURE": "DEFERRED_TO_W2_16 - revalidate F1/F2a and all F2b gates",
        "G4_INDEPENDENT_CHECK": "REQUIRED - three contract reviews, then three result reviews",
        "G5_LIMITS_REGRESSION": "REQUIRED - old restriction and predeclared nulls",
        "G6_PHYSICAL_MATCH": "N/A - no physical semantics at F2",
        "G7_OBSERVATION": "N/A - no observable or data",
        "G8_EXPORT": "N/A - internal and Git-ignored",
    }


def review_attestations() -> dict[str, dict[str, Any]]:
    return {
        "candidate_architecture_review": {
            "passed": True,
            "reviewer": "/root/f2_independent_review",
            "artifact": EXPECTED_REVIEW_REQUIREMENTS["candidate_architecture_review"],
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS["candidate_architecture_review"],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS["candidate_architecture_review"],
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
        "CLAIM_ID": "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CONTRACT_001",
        "CLAIM": (
            "Freeze, without evaluating outcomes, the selected revised one-carrier candidate "
            "A=S+R whose transpose-derived noncommuting channels may supply the state nodes "
            "and joint carrier absent from the exact w2_14 class."
        ),
        "TYPE": "OUTCOME_NEUTRAL_REVISED_CANDIDATE_CONTRACT",
        "MODEL_VERSION": MODEL_VERSION,
        "ASSUMPTIONS": (
            "The exact C0, w2_13 F2b contract and w2_14 scoped no-go are valid.  The new A and "
            "its polynomial law are imported mathematical hypotheses, not derived RefG facts."
        ),
        "DOMAIN": (
            "A in sl(3,R), S=(A+A^T)/2, R=(A-A^T)/2, alpha,b,c,eta,d>0; "
            "the accepted branch and relational open subset must be derived in w2_16."
        ),
        "CONVENTIONS": (
            "Real 3x3 endomorphisms, Euclidean internal transpose/trace, common O(3) conjugation, "
            "commutator [S,R]=SR-RS, and no spacetime or physical interpretation."
        ),
        "FREEDOM_LEDGER": freedom_ledger(),
        "DEPENDENCIES": (
            "Frozen W2-C0 exact runtime identity; private governance is not a runtime file; "
            "exact w2_13 completion contract; exact w2_14 scoped no-go."
        ),
        "METHOD": (
            "Precommit one candidate identity, complete law, domain, proposed nodes/carrier, "
            "equivalence, nulls, freedom ledger and every downstream proof duty before evaluation."
        ),
        "PASS_CONDITION": (
            "Only this contract freezes: exact dependencies, definition coherence, outcome "
            "neutrality, fail-closed mutations and three reviews.  It cannot pass F2b."
        ),
        "FAIL_CONDITION": (
            "Any missing freedom, changed law, hidden primitive, physical import, premature result "
            "flag, dependency drift, review failure or ambiguous common action invalidates the freeze."
        ),
        "FALSIFIER": (
            "A proof that this artifact evaluated a candidate outcome, hid a target, omitted a "
            "candidate freedom or failed to specify a unique downstream object falsifies the freeze."
        ),
        "RESIDUAL": "N/A for outcomes; exact zero for contract identities.",
        "ERROR_BOUND": "N/A; no numerical or observational statement.",
        "VALIDITY_HEALTH": (
            "Conditional only on the imported abstract A and law.  The separable mixed-coupling "
            "choice and flat relative modulus are explicit risks that w2_16 may reject."
        ),
        "BRANCHES": {
            "contract": "FROZEN_ONLY_AFTER_REVIEWS",
            "candidate_outcome": "UNEVALUATED",
            "old_R_zero_restriction": "DECLARED_REQUIRES_EXACT_CHECK",
            "generic_noncommuting_branch": "DECLARED_REQUIRES_DERIVATION",
            "commuting_or_zero_branches": "PREDECLARED_NULLS",
            "flat_relative_modulus": "OPEN_HEALTH_AND_EQUIVALENCE_GATE",
            "full_c0_f2": "OPEN",
        },
        "OBSERVABLE_MAP": {"status": "N/A", "reason": "atemporal internal contract"},
        "FORWARD_MODEL": {"status": "N/A", "reason": "no observable"},
        "DATA_ROLE": {"status": "N/A", "reason": "no data, target or fit"},
        "IDENTIFIABILITY": (
            "All five law parameters, the exact zero mixed couplings, state algebra, common action, "
            "node maps, carrier and reports are explicitly enumerated and identity-frozen.  No "
            "observational or inferential identifiability is claimed."
        ),
        "BENCHMARK": (
            "w2_14 is the null boundary: deleting R or replacing [S,R] by commutative spectral "
            "repackaging must return the rejected class."
        ),
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "CROSSCHECK": (
            "Exact transpose decomposition and old-law restriction, identity hashes, mutation "
            "tests, three contract reviews and a separately identity-pinned w2_16 evaluator."
        ),
        "PROVENANCE": {
            "date": "2026-07-21",
            "reviewed_payload_sha256": EXPECTED_PAYLOAD_SHA256,
            "source_identities": {
                "w2_00": C0_SHA256,
                "w2_13": W213_SOURCE, "w2_14": W214_SOURCE,
            },
            "output_artifact": (
                "RefG/work 2/w2_15_f2b_general_traceless_single_carrier_candidate_contract.py"
            ),
        },
        "FILES": (
            "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
            "RefG/work 2/w2_13_f2b_node_imprint_and_relational_completion_contract.py",
            "RefG/work 2/w2_14_f2b_single_generator_commutative_spectral_repackaging_gate.py",
            "RefG/work 2/w2_15_f2b_general_traceless_single_carrier_candidate_contract.py",
        ),
        "CANDIDATE_DEFINITION": candidate_definition(),
        "LAW_AND_BRANCH": law_and_branch(),
        "NODE_AND_CARRIER_ANSATZ": node_and_carrier_ansatz(),
        "EQUIVALENCE_AND_PAIR_DOMAIN": equivalence_and_pair_domain(),
        "OPEN_DOMAIN_AND_NULLS": open_domain_and_nulls(),
        "OUTCOME_BLINDNESS": outcome_blindness(),
        "REVALIDATION_DUTIES": revalidation_duties(),
        "F2B_GATE_DUTIES": f2b_gate_duties(),
        "FORBIDDEN_UPGRADES": (
            "candidate contract renamed a proof or full-F2 closure",
            "S or R imported independently instead of derived from one A",
            "flat modulus declared physical or stable without exact audit",
            "independent channel rotations silently declared gauge or non-gauge",
            "commutator syntax alone declared irreducible relational content",
            "normalized tau assigned at s=0 or J=0",
            "pressure strain vortex matter geometry time memory or observation imported",
            "failed candidate patched in place after seeing outcomes",
        ),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "GATE_APPLICABILITY": gate_applicability(),
        "EXPORT_STATUS": dict(EXPECTED_EXPORT_STATUS),
        "INDEPENDENT_REVIEW": dict(EXPECTED_REVIEW_REQUIREMENTS),
        "NEXT_TASK_POLICY": {
            "frozen": NEXT_ATOMIC_TASK,
            "pending": "Complete exact contract reviews before evaluating this candidate.",
            "invalid": "Restore or replace the contract as a new version before evaluation.",
        },
        "NEXT_ATOMIC_TASK": NEXT_ATOMIC_TASK,
    }


CLAIM_CONTRACT = build_contract()


def exact_tree_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(exact_tree_equal(left[k], right[k]) for k in left)
    if isinstance(left, (tuple, list)):
        return len(left) == len(right) and all(exact_tree_equal(a, b) for a, b in zip(left, right))
    return bool(left == right)


def exact_bool_map(actual: Any, expected: dict[str, bool]) -> bool:
    return bool(
        isinstance(actual, dict)
        and set(actual) == set(expected)
        and all(type(actual[key]) is bool and actual[key] is expected[key] for key in expected)
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
        set(contract.get("CANDIDATE_DEFINITION", {})) == EXPECTED_CANDIDATE_KEYS,
        set(contract.get("LAW_AND_BRANCH", {})) == EXPECTED_LAW_KEYS,
        set(contract.get("NODE_AND_CARRIER_ANSATZ", {})) == EXPECTED_NODE_KEYS,
        set(contract.get("EQUIVALENCE_AND_PAIR_DOMAIN", {})) == EXPECTED_EQUIVALENCE_KEYS,
        set(contract.get("OPEN_DOMAIN_AND_NULLS", {})) == EXPECTED_NULL_KEYS,
        set(contract.get("OUTCOME_BLINDNESS", {})) == EXPECTED_BLINDNESS_KEYS,
        set(contract.get("REVALIDATION_DUTIES", {})) == EXPECTED_REVALIDATION_KEYS,
        set(contract.get("F2B_GATE_DUTIES", {})) == EXPECTED_F2B_DUTY_KEYS,
        exact_true_map(contract.get("OUTCOME_BLINDNESS"), EXPECTED_BLINDNESS_KEYS),
        isinstance(freedom, dict) and set(freedom) == EXPECTED_FREEDOM_KEYS,
        isinstance(freedom, dict) and all(
            isinstance(entry, dict) and set(entry) == EXPECTED_FREEDOM_ENTRY_KEYS
            for entry in freedom.values()
        ),
        isinstance(contract.get("FORBIDDEN_UPGRADES"), tuple),
        exact_bool_map(contract.get("CLOSURE_FLAGS"), EXPECTED_C0_CLOSURE_FLAGS),
        exact_bool_map(contract.get("SCOPE_CEILING"), EXPECTED_SCOPE_CEILING),
        set(contract.get("GATE_APPLICABILITY", {})) == EXPECTED_GATE_KEYS,
        exact_bool_map(contract.get("EXPORT_STATUS"), EXPECTED_EXPORT_STATUS),
        exact_tree_equal(contract.get("INDEPENDENT_REVIEW"), EXPECTED_REVIEW_REQUIREMENTS),
        set(contract.get("NEXT_TASK_POLICY", {})) == {"frozen", "pending", "invalid"},
    ))


def semantic_guard(contract: Any) -> bool:
    try:
        fields = (
            contract["CLAIM"], contract["METHOD"], contract["PASS_CONDITION"],
            contract["VALIDITY_HEALTH"], contract["BRANCHES"],
            contract["CANDIDATE_DEFINITION"], contract["LAW_AND_BRANCH"],
            contract["NODE_AND_CARRIER_ANSATZ"], contract["SCOPE_CEILING"],
            contract["NEXT_ATOMIC_TASK"],
        )
        corpus = "\n".join(
            item if isinstance(item, str) else json.dumps(item, sort_keys=True)
            for item in fields
        ).lower()
    except (KeyError, TypeError, ValueError):
        return False
    forbidden = (
        "candidate passes f2b", "full f2 is closed", "node is proved",
        "carrier is proved", "flat modulus is physical", "time emerges",
        "metric emerges", "gr is derived", "observationally validated",
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
    paths = (C0_PATH, W213_PATH, W214_PATH)
    if not all(path.is_file() for path in paths):
        return False, {}
    try:
        c0_text = C0_PATH.read_text(encoding="utf-8")
        w214 = load_module(W214_PATH, "refg_w214_for_w215")
        w214_report = w214.run_audit()
    except Exception:
        return False, {}
    w214_reviews = w214_report.get("INDEPENDENT_REVIEW_ATTESTATIONS", {})
    files = CLAIM_CONTRACT["FILES"]
    checks = all((
        C0_PATH.relative_to(ROOT).as_posix() == files[0],
        W213_PATH.relative_to(ROOT).as_posix() == files[1],
        W214_PATH.relative_to(ROOT).as_posix() == files[2],
        Path(__file__).resolve().relative_to(ROOT).as_posix() == files[3],
        file_sha256(C0_PATH) == C0_SHA256,
        file_sha256(W213_PATH) == W213_SOURCE,
        file_sha256(W214_PATH) == W214_SOURCE,
        f"`{PROGRAM_CONTRACT}`" in c0_text,
        "### `W2_F2_OPERATIONAL_RELATIONS`" in c0_text,
        w214.MODEL_VERSION == W214_MODEL,
        w214_report.get("STATUS") == W214_STATUS,
        w214_report.get("AUDIT_VALID") is True,
        w214_report.get("CLASS_EVALUATED") is True,
        w214_report.get("CANDIDATE_EVALUATED") is False,
        w214_report.get("NO_GO_PROVED") is True,
        w214_report.get("FULL_W2_F2_OPERATIONAL_RELATIONS") is False,
        w214_report.get("DETACHED_PAYLOAD_SHA256") == W214_PAYLOAD,
        w214_report.get("DETACHED_VALIDATOR_SHA256") == W214_VALIDATOR,
        len(w214_reviews) == 3,
        all(entry.get("passed") is True for entry in w214_reviews.values()),
    ))
    return bool(checks), {
        "w214_module": w214, "w214_report": w214_report,
    }


def definition_controls() -> dict[str, bool]:
    entries = sp.symbols("a0:9", real=True)
    a = sp.Matrix(3, 3, entries)
    a = a - sp.trace(a) * sp.eye(3) / 3
    s_matrix = sp.simplify((a + a.T) / 2)
    r_matrix = sp.simplify((a - a.T) / 2)

    alpha, b, c, eta, d = sp.symbols("alpha b c eta d", positive=True)
    q1, q2, q4, q5, q6 = sp.symbols("q1 q2 q4 q5 q6", real=True)
    q = sp.Matrix([
        [q1, q4, q5],
        [q4, q2, q6],
        [q5, q6, -q1 - q2],
    ])
    q_i2 = sp.trace(q**2)
    q_i3 = sp.trace(q**3)
    zero_r = sp.zeros(3)
    q_j = -sp.trace(zero_r**2)
    restricted_law = (
        -alpha * q_i2 / 2 - b * q_i3 / 3 + c * q_i2**2 / 4
        - eta * q_j / 2 + d * q_j**2 / 4
    )
    exact_old_q_law = -alpha * q_i2 / 2 - b * q_i3 / 3 + c * q_i2**2 / 4
    restricted = sp.simplify(restricted_law - exact_old_q_law)

    x, y, z = sp.symbols("x y z", real=True)
    prototype_r = sp.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    prototype_j = sp.simplify(-sp.trace(prototype_r**2))
    prototype_s = sp.diag(2, -1, -1)
    commutator = sp.simplify(prototype_s * prototype_r - prototype_r * prototype_s)

    return {
        "transpose_split_exact": all((
            matrix_zero(a - s_matrix - r_matrix),
            matrix_zero((s_matrix + r_matrix) - a),
        )),
        "channels_have_required_symmetry_and_trace": all((
            matrix_zero(s_matrix.T - s_matrix),
            matrix_zero(r_matrix.T + r_matrix),
            sp.simplify(sp.trace(s_matrix)) == 0,
            sp.simplify(sp.trace(r_matrix)) == 0,
        )),
        "single_carrier_reconstruction_exact": matrix_zero(a - (s_matrix + r_matrix)),
        "old_law_restriction_exact": restricted == 0,
        "skew_invariant_nonnegative_prototype": prototype_j == 2 * (x**2 + y**2 + z**2),
        "candidate_parameter_domain_open": (
            CLAIM_CONTRACT["LAW_AND_BRANCH"]["parameter_domain"]
            == "alpha,b,c,eta,d>0; no fitted or observed constants."
        ),
        "commutator_report_joint_not_unary_syntax": all((
            not matrix_zero(commutator),
            "[S,R]" in CLAIM_CONTRACT["NODE_AND_CARRIER_ANSATZ"]["carrier"],
            "Tr(C^T C)" in CLAIM_CONTRACT["NODE_AND_CARRIER_ANSATZ"]["joint_report"],
        )),
        "all_candidate_outcomes_false": all(
            value is False
            for key, value in CLAIM_CONTRACT["SCOPE_CEILING"].items()
            if key not in {
                "candidate_contract_frozen", "new_single_carrier_imported",
                "symmetric_and_skew_channels_derived", "old_f1_exact_restriction_declared",
            }
        ),
    }


def review_schema_valid(attestations: Any, require_pass: bool) -> bool:
    fields = {
        "passed", "reviewer", "artifact", "reviewed_payload_sha256",
        "reviewed_validator_sha256",
    }
    reviewers = {
        "candidate_architecture_review": "/root/f2_independent_review",
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
        missing = copy.deepcopy(base)
        missing.pop(key)
        mutants.append(missing)
        nonboolean = copy.deepcopy(base)
        nonboolean[key]["passed"] = 1
        mutants.append(nonboolean)
        wrong_hash = copy.deepcopy(base)
        wrong_hash[key]["reviewed_payload_sha256"] = "WRONG"
        mutants.append(wrong_hash)
    extra = copy.deepcopy(base)
    extra["fabricated_review"] = copy.deepcopy(next(iter(base.values())))
    mutants.append(extra)
    return all(not review_schema_valid(mutant, require_pass=False) for mutant in mutants)


def mutation_controls() -> dict[str, bool]:
    base = copy.deepcopy(CLAIM_CONTRACT)

    def rejected(candidate: Any) -> bool:
        return not strict_contract_valid(candidate)

    structural_mutants: list[Any] = []
    for key in EXPECTED_STANDARD_FIELDS | EXPECTED_CUSTOM_FIELDS:
        mutant = copy.deepcopy(base)
        mutant.pop(key)
        structural_mutants.append(mutant)
    extra = copy.deepcopy(base)
    extra["UNREGISTERED_FIELD"] = True
    structural_mutants.append(extra)

    registry_mutants = []
    for field in (
        "CANDIDATE_DEFINITION", "LAW_AND_BRANCH", "NODE_AND_CARRIER_ANSATZ",
        "EQUIVALENCE_AND_PAIR_DOMAIN", "OPEN_DOMAIN_AND_NULLS",
        "OUTCOME_BLINDNESS", "REVALIDATION_DUTIES", "F2B_GATE_DUTIES",
        "FREEDOM_LEDGER", "GATE_APPLICABILITY",
    ):
        mutant = copy.deepcopy(base)
        mutant[field].pop(next(iter(mutant[field])))
        registry_mutants.append(mutant)

    scope_mutants = []
    scope = copy.deepcopy(base)
    scope["SCOPE_CEILING"]["full_W2_F2_operational_relations"] = True
    scope_mutants.append(scope)
    export = copy.deepcopy(base)
    export["EXPORT_STATUS"]["GITHUB"] = True
    scope_mutants.append(export)

    outcome_mutants = []
    for key in (
        "candidate_evaluated", "f1_revalidated_in_extended_state",
        "f2a_revalidated_in_extended_state", "state_supported_nodes_proved",
        "atemporal_state_carrier_proved", "irreducible_pair_relation_proved",
        "complete_common_action_proved", "flat_relative_modulus_accepted",
    ):
        mutant = copy.deepcopy(base)
        mutant["SCOPE_CEILING"][key] = True
        outcome_mutants.append(mutant)

    semantics = copy.deepcopy(base)
    semantics["CANDIDATE_DEFINITION"]["semantic_boundary"] = "metric emerges"
    dependency = copy.deepcopy(base)
    dependency["PROVENANCE"]["source_identities"]["w2_14"] = "WRONG"

    return {
        "missing_or_extra_contract_fields_rejected": all(map(rejected, structural_mutants)),
        "registry_drift_rejected": all(map(rejected, registry_mutants)),
        "scope_and_export_overclaims_rejected": all(map(rejected, scope_mutants)),
        "outcome_injection_rejected": all(map(rejected, outcome_mutants)),
        "physical_semantics_injection_rejected": rejected(semantics),
        "dependency_identity_mutation_rejected": rejected(dependency),
    }


def safe_contract_valid() -> bool:
    try:
        return strict_contract_valid(CLAIM_CONTRACT)
    except Exception:
        return False


def _run_audit_unchecked() -> dict[str, Any]:
    if not strict_contract_valid(CLAIM_CONTRACT):
        raise ValueError("contract payload or schema invalid")
    if detached_validator_sha256() != EXPECTED_VALIDATOR_SHA256:
        raise ValueError("validator source identity invalid")

    dependency_ok, _dependencies = dependencies_valid()
    definitions = definition_controls()
    mutations = mutation_controls()
    attestations = review_attestations()
    review_structure = review_schema_valid(attestations, require_pass=False)

    checks = {
        "payload_validator_and_contract_schema_exact": all((
            strict_contract_valid(CLAIM_CONTRACT),
            detached_validator_sha256() == EXPECTED_VALIDATOR_SHA256,
            registry_shapes_valid(CLAIM_CONTRACT),
        )),
        "w213_and_scoped_no_go_dependencies_exact": dependency_ok,
        "candidate_definition_coherence_exact": exact_true_map(
            definitions, EXPECTED_DEFINITION_CONTROL_KEYS,
        ),
        "candidate_outcome_neutrality_exact": all((
            exact_true_map(CLAIM_CONTRACT["OUTCOME_BLINDNESS"], EXPECTED_BLINDNESS_KEYS),
            CLAIM_CONTRACT["BRANCHES"]["candidate_outcome"] == "UNEVALUATED",
            CLAIM_CONTRACT["SCOPE_CEILING"]["candidate_evaluated"] is False,
            CLAIM_CONTRACT["SCOPE_CEILING"]["full_W2_F2_operational_relations"] is False,
        )),
        "mutation_controls_exact": exact_true_map(mutations, EXPECTED_MUTATION_KEYS),
        "closure_scope_export_boundaries_exact": all((
            exact_bool_map(CLAIM_CONTRACT["CLOSURE_FLAGS"], EXPECTED_C0_CLOSURE_FLAGS),
            exact_bool_map(CLAIM_CONTRACT["SCOPE_CEILING"], EXPECTED_SCOPE_CEILING),
            exact_bool_map(CLAIM_CONTRACT["EXPORT_STATUS"], EXPECTED_EXPORT_STATUS),
        )),
        "review_schema_fail_closed": all((review_structure, review_schema_controls())),
        "review_attestations_complete": review_schema_valid(attestations, require_pass=True),
        "next_task_is_exact_candidate_evaluation": all((
            CLAIM_CONTRACT["NEXT_TASK_POLICY"]["frozen"] == NEXT_ATOMIC_TASK,
            "w2_16_f2b_general_traceless_single_carrier_candidate_gate.py" in NEXT_ATOMIC_TASK,
            "revalidate F1" in NEXT_ATOMIC_TASK,
            "all w2_13 screening gates" in NEXT_ATOMIC_TASK,
            "close full F2 only if every gate" in NEXT_ATOMIC_TASK,
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
        "F1_REVALIDATED_IN_EXTENDED_STATE": False,
        "F2A_REVALIDATED_IN_EXTENDED_STATE": False,
        "F2B_RELATIONAL_COMPLETION_PROVED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "PROMOTED": False,
        "DETACHED_PAYLOAD_SHA256": detached_payload_sha256(CLAIM_CONTRACT),
        "DETACHED_VALIDATOR_SHA256": detached_validator_sha256(),
        "DEFINITION_CONTROLS": definitions,
        "MUTATION_CONTROLS": mutations,
        "AUDIT_CHECKS": checks,
        "INDEPENDENT_REVIEW_ATTESTATIONS": attestations,
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "PROMOTION_CEILING": "CONTRACT_FREEZE_ONLY__NO_CANDIDATE_RESULT",
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
        "F1_REVALIDATED_IN_EXTENDED_STATE": False,
        "F2A_REVALIDATED_IN_EXTENDED_STATE": False,
        "F2B_RELATIONAL_COMPLETION_PROVED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "PROMOTED": False,
        "DETACHED_PAYLOAD_SHA256": "",
        "DETACHED_VALIDATOR_SHA256": "",
        "DEFINITION_CONTROLS": {key: False for key in EXPECTED_DEFINITION_CONTROL_KEYS},
        "MUTATION_CONTROLS": {key: False for key in EXPECTED_MUTATION_KEYS},
        "AUDIT_CHECKS": {key: False for key in EXPECTED_AUDIT_KEYS},
        "INDEPENDENT_REVIEW_ATTESTATIONS": {},
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "SCOPE_CEILING": {
            key: False if key == "candidate_contract_frozen" else value
            for key, value in EXPECTED_SCOPE_CEILING.items()
        },
        "PROMOTION_CEILING": "INVALID__NO_EVALUATION_OR_PROMOTION",
        "NEXT_ATOMIC_TASK": "UNAVAILABLE_UNTIL_EXACT_CONTRACT_RESTORED",
        "ERROR": f"{type(error).__name__}: {error}",
    }


def run_audit() -> dict[str, Any]:
    try:
        return _run_audit_unchecked()
    except Exception as error:
        return fail_closed_invalid_report(error)


def main() -> int:
    report = run_audit()
    try:
        rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    except (TypeError, ValueError) as error:
        report = fail_closed_invalid_report(error)
        report["NEXT_ATOMIC_TASK"] = "UNAVAILABLE_UNTIL_JSON_SAFE"
        rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    return 0 if report["AUDIT_VALID"] is True else 1


if __name__ == "__main__":
    sys.exit(main())
