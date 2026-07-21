"""Exact candidate audit for the narrow W2-F2a intrastate comparison gate.

The candidate is the Frobenius-Riesz Hessian of the already accepted F1
quartic functional.  On the generic accepted branch it generates two normal
spectral sectors and one uniform, atemporal comparison kernel.  The result is
only a law-defined internal comparison: it is not a physical response, mode,
node, imprint, interaction, time, geometry, observable, or full W2-F2.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

import sympy as sp


MODEL_VERSION = "W2-F2A-INTRASTATE-HESSIAN-COMPARISON-v1.0-internal"
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"
F2A_MODEL_VERSION = "W2-F2A-INTERNAL-OPERATIONAL-DISTINCTION-CONTRACT-v1.2-internal"
F2A_FROZEN_STATUS = "W2_F2A_CONTRACT_FROZEN__NO_CANDIDATE_EVALUATED__FULL_F2_OPEN"
F2A_PAYLOAD_SHA256 = "4F09319C5DE3569AFA7FC2AA8FEA2190438D2E15EECC4DFCA815D69999FD37E2"
F2A_VALIDATOR_SHA256 = "8AAA08C517DC623CFEA2DB18223F9EC7670F1A01D085AFD2CDFB0E1851C31666"
W211_MODEL_VERSION = "W2-F2-SINGLE-ORBIT-READOUT-NO-GO-v1.0-internal"
W211_STATUS = "CONDITIONAL_EXACT_SINGLE_ORBIT_WHOLE_STATE_READOUT_NO_GO__F2A_OPEN"
W211_PAYLOAD_SHA256 = "488F32736333427A1164963917B04A5962AB73ED5326BD8A90E24380AFD37EC6"
W211_VALIDATOR_SHA256 = "EC3514B0CCB1DE0425E3E18B447C408EC0D58F30798CE58DD37C12CAA167091D"
F1_MODEL_VERSION = "RefG-F1-ATEMPORAL-STRUCTURAL-PROOF-v1.0"
F1_STATUS = "CONDITIONAL_ATEMPORAL_STRUCTURAL_F1_RELATIVE_TO_IMPORTED_PRIMITIVES"

C0_SHA256 = "3E0EFB2D635E7E5605F9D7EDFA99538644D7C21311989C478C4A6AF1854890EB"
F2A_SOURCE_SHA256 = "44ADB77E4B78D5D36E7F597C8401FD91A9E0DD0F0D86E20541F1EB790EF8308D"
W211_SOURCE_SHA256 = "B1BF8B9F21844B9AFC5EB5932A5B864C8DA253139FC7C55A5BCB9494ADB86786"
F1_SOURCE_SHA256 = "8B29AF84AE0F94063CF0E7FDAB47A7CE364C7D6B1789D71051548A98A96C770E"

READY_STATUS = "W2_F2A_HESSIAN_COMPARISON_READY_FOR_INDEPENDENT_REVIEW__FULL_F2_OPEN"
PASS_STATUS = "CONDITIONAL_EXACT_F2A_INTRASTATE_HESSIAN_COMPARISON__FULL_F2_OPEN"
NEGATIVE_STATUS = "W2_F2A_HESSIAN_COMPARISON_COMPLETE_NOT_PROMOTED__F2A_OPEN"
INVALID_STATUS = "W2_F2A_HESSIAN_COMPARISON_INVALID__NO_CANDIDATE_EVALUATION"
EXPECTED_PAYLOAD_SHA256 = "2D6621D8932D4DB3272ED2777DC4D08C3C5CB0A625508D695043C23424DA0455"
EXPECTED_VALIDATOR_SHA256 = "3B6CA4D52EEB5797F5304A3EC2B779CBC9F0FF91695C65902AE5DAFF1EA8DC49"

ROOT = Path(__file__).resolve().parents[2]
C0_PATH = Path(__file__).with_name("w2_00_foundation_to_einstein_contract.md")
F2A_PATH = Path(__file__).with_name(
    "w2_10_f2a_internal_operational_distinction_contract.py"
)
W211_PATH = Path(__file__).with_name(
    "w2_11_f2_single_orbit_readout_no_go_gate.py"
)
F1_PATH = Path(__file__).with_name("w2_09a_f1_proof") / "refg_f1_atemporal_structural_proof.py"

NEXT_ATOMIC_TASK = (
    "Create w2_13_f2b_node_imprint_and_relational_completion_contract.py: freeze "
    "the remaining full-C0-F2 obligations for a state-supported node, atemporal "
    "imprint/correlation carrier, and any stronger irreducibly pairwise relation; "
    "keep persistence in F3 and start full W2_F2 false."
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
    "CANDIDATE_DEFINITION", "LAW_DERIVATION", "RELATA_CONSTRUCTION",
    "COMPARISON_MAP", "QP_ONLY_NULL_BOUNDARY", "CANDIDATE_GATE_EVIDENCE",
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
    "foundation_law_derived": False,
    "functional_uniqueness_derived": False,
    "N3_physical_origin_derived": False,
    "physical_node_or_location": False,
    "atemporal_imprint_or_correlation_carrier": False,
    "persistent_physical_imprint": False,
    "irreducibly_pairwise_coupling": False,
    "physical_response_intervention_or_measurement": False,
    "independent_additive_physical_modes": False,
    "temporal_formation_persistence_or_causality": False,
    "physical_dimension_or_continuum": False,
    "Lorentzian_metric_or_light_cone": False,
    "effective_action_or_conservation_law": False,
    "RefG_environment_map": False,
    "mass_pressure_particle_or_oscillon": False,
    "full_W2_F2_operational_relations": False,
    "GR_PN_or_PPN_bridge": False,
    "external_observable_or_data_map": False,
    "observational_validation": False,
}
EXPECTED_EXPORT_STATUS = {
    "CANON": False,
    "ARTICLE": False,
    "GITHUB": False,
    "ZENODO": False,
}

EXPECTED_CANDIDATE_KEYS = frozenset({
    "route", "accepted_state", "carrier", "generic_domain",
    "degenerate_boundary", "reference_boundary", "claim_ceiling",
})
EXPECTED_LAW_KEYS = frozenset({
    "functional", "first_principle_map", "riesz_operator", "covariance",
    "ownership",
})
EXPECTED_RELATA_KEYS = frozenset({
    "normal_domain", "radial_sector", "biaxial_sector", "orbit_sector",
    "spectral_generation", "undefined_boundary",
})
EXPECTED_COMPARISON_KEYS = frozenset({
    "domain", "codomain", "uniform_rule", "reported_relation",
    "generic_result", "tuned_null", "semantic_ceiling",
})
EXPECTED_QP_NULL_KEYS = frozenset({
    "spectral_algebra", "block_scalar_boundary", "rank_equality_null",
    "duplicated_mode_null", "why_hessian_is_extra_content",
})
EXPECTED_GATE_EVIDENCE_KEYS = frozenset({
    "source", "all_19_gates_runtime_computed", "false_gate_policy",
    "review_policy",
})
EXPECTED_NEXT_POLICY_KEYS = frozenset({
    "positive", "negative", "invalid_or_pending",
})
EXPECTED_FREEDOM_KEYS = frozenset({
    "inherited_f1_parameters", "route_choice", "hessian_candidate_choice",
    "normalization_choice", "tangent_carrier", "new_numerical_parameters",
    "data_fitted_parameters", "chosen_representative_basis_or_axis",
    "new_physical_primitives",
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
    "semantic_candidate_review", "fail_closed_code_review",
    "new_reader_scope_review",
})
EXPECTED_REVIEW_REQUIREMENTS = {
    "semantic_candidate_review": "independent theorem, F2a-semantics and caveat audit",
    "fail_closed_code_review": "independent exact-code and adversarial audit",
    "new_reader_scope_review": "independent provenance, contract and overclaim audit",
}
EXPECTED_DERIVATION_CONTROL_KEYS = frozenset({
    "coordinate_hessian_matches_coordinate_free_second_variation",
    "riesz_operator_matches_hessian_and_is_self_adjoint",
    "on_shell_spectral_decomposition_exact",
    "characteristic_polynomial_and_multiplicities_exact",
    "accepted_positive_branch_eigenvalues_exact",
})
EXPECTED_RELATA_CONTROL_KEYS = frozenset({
    "q_generated_sector_projectors_exact",
    "sector_projectors_idempotent_orthogonal_complete",
    "sector_ranks_one_two_two_exact",
    "generic_spectral_polynomials_generate_relata",
    "orbit_sector_excluded_as_declared_equivalence",
})
EXPECTED_COMPARISON_CONTROL_KEYS = frozenset({
    "one_predeclared_rule_covers_all_four_ordered_pairs",
    "normalized_comparison_table_exact",
    "label_free_contrast_and_sum_exact",
    "generic_open_domain_separation_exact",
    "comparison_not_a_physical_or_temporal_response",
})
EXPECTED_QP_NULL_CONTROL_KEYS = frozenset({
    "qp_spectral_algebra_closes_in_two_dimensions",
    "qp_only_effects_are_block_scalar",
    "free_block_weights_fit_arbitrary_two_unary_targets",
    "projector_overlap_is_bare_delta",
    "traceless_p1_p2_carriers_duplicate_one_q_mode",
})
EXPECTED_NULL_CONTROL_KEYS = frozenset({
    "tuned_surface_collapses_to_scalar_delta",
    "origin_hessian_is_scalar_and_generates_no_relata",
    "self_only_postselection_is_rejected_by_full_pair_domain",
    "rank_only_comparator_cannot_reproduce_generic_weights",
    "preferred_axis_and_representative_entries_absent",
    "invalid_f1_boundaries_do_not_inherit_candidate",
})
EXPECTED_COVARIANCE_CONTROL_KEYS = frozenset({
    "manifest_complete_o3_covariance_from_invariant_second_derivative",
    "exact_generator_covariance_crosscheck",
    "frobenius_pairing_and_supertrace_report_invariant",
    "label_swap_leaves_reported_contrast_invariant",
    "parameter_motion_not_confused_with_one_orbit_equivalence",
})
EXPECTED_MUTATION_KEYS = frozenset({
    "missing_or_extra_contract_fields_rejected",
    "registry_drift_rejected",
    "closure_scope_export_overclaims_rejected",
    "semantic_overclaims_rejected",
    "malformed_candidate_gate_maps_rejected",
})
EXPECTED_AUDIT_KEYS = frozenset({
    "payload_validator_and_contract_schema_exact",
    "c0_f2a_w211_f1_dependencies_exact",
    "candidate_control_schemas_exact",
    "candidate_gate_schema_and_screen_valid",
    "mutation_controls_exact",
    "closure_scope_export_boundaries_exact",
    "review_attestation_schema_fail_closed",
    "review_attestations_complete",
    "next_task_policy_exact",
})

REVIEW_ATTESTED_PAYLOAD_IDS = {
    "semantic_candidate_review": "2D6621D8932D4DB3272ED2777DC4D08C3C5CB0A625508D695043C23424DA0455",
    "fail_closed_code_review": "2D6621D8932D4DB3272ED2777DC4D08C3C5CB0A625508D695043C23424DA0455",
    "new_reader_scope_review": "2D6621D8932D4DB3272ED2777DC4D08C3C5CB0A625508D695043C23424DA0455",
}
REVIEW_ATTESTED_VALIDATOR_IDS = {
    "semantic_candidate_review": "3B6CA4D52EEB5797F5304A3EC2B779CBC9F0FF91695C65902AE5DAFF1EA8DC49",
    "fail_closed_code_review": "3B6CA4D52EEB5797F5304A3EC2B779CBC9F0FF91695C65902AE5DAFF1EA8DC49",
    "new_reader_scope_review": "3B6CA4D52EEB5797F5304A3EC2B779CBC9F0FF91695C65902AE5DAFF1EA8DC49",
}


def candidate_definition() -> dict[str, str]:
    return {
        "route": "INTRASTATE_UNIFORM_EFFECT_FAMILY",
        "accepted_state": (
            "The public F1 accepted uniaxial Q orbit at alpha,b,c>0 and its positive root s."
        ),
        "carrier": (
            "The inherited linear state space Sym0(3), used only as an atemporal tangent and "
            "comparison carrier; no physical mode meaning is assigned."
        ),
        "generic_domain": "alpha,b,c>0 with b^2 != 3 alpha c on the accepted positive branch.",
        "degenerate_boundary": (
            "At b^2=3 alpha c the two normal Hessian weights coincide and this candidate does "
            "not establish F2a distinction."
        ),
        "reference_boundary": (
            "At Q=0 the Hessian is scalar on Sym0(3), no two normal spectral relata are "
            "generated, and no singular continuation is allowed."
        ),
        "claim_ceiling": (
            "Conditional exact law-defined atemporal internal comparison only; full F2 and all "
            "physical, temporal, geometric and observational meanings remain open or excluded."
        ),
    }


def law_derivation() -> dict[str, str]:
    return {
        "functional": (
            "Use exactly the inherited F1 quartic V(Q)=-alpha Tr(Q^2)/2-b Tr(Q^3)/3+"
            "c Tr(Q^2)^2/4; do not add a target or coefficient."
        ),
        "first_principle_map": (
            "Differentiate the same frozen V twice at accepted Q to obtain one symmetric "
            "bilinear Hessian on every pair of inherited carrier variations."
        ),
        "riesz_operator": (
            "Use the inherited positive Frobenius contraction once to represent that Hessian "
            "by a unique self-adjoint operator L_Q."
        ),
        "covariance": (
            "O(3)-invariance of V implies L_{RQR^T}(RUR^T)=R L_Q(U) R^T under the complete "
            "declared internal equivalence."
        ),
        "ownership": (
            "The Hessian is mathematically derived from the imported F1 law, but selecting its "
            "normalized sector comparison as the F2a candidate is one declared architecture "
            "choice and is not claimed foundation-unique."
        ),
    }


def relata_construction() -> dict[str, str]:
    return {
        "normal_domain": (
            "Remove the two tangent directions of the declared O(3) orbit; the remaining "
            "three-dimensional normal carrier is the candidate comparison domain."
        ),
        "radial_sector": "The simple nonzero Hessian eigenspace generated by Pi_r, rank one.",
        "biaxial_sector": "The second nonzero Hessian eigenspace generated by Pi_b, rank two.",
        "orbit_sector": (
            "The rank-two zero eigenspace Pi_o is an equivalence-orbit tangent and is a null, "
            "not a third physical or operational relatum."
        ),
        "spectral_generation": (
            "On the generic domain Pi_r and Pi_b are exact spectral polynomials of the single "
            "law-derived L_Q, so neither a basis, axis, target projector nor desired table is input."
        ),
        "undefined_boundary": (
            "The separate Pi_r/Pi_b generation by L_Q is undefined as a distinction when their "
            "eigenvalues coincide; Q=0 is separately null."
        ),
    }


def comparison_map() -> dict[str, str]:
    return {
        "domain": "All four ordered pairs in {Pi_r,Pi_b} x {Pi_r,Pi_b}, fixed before outcomes.",
        "codomain": "One shared exact real scalar codomain.",
        "uniform_rule": (
            "K_Q(A,B)=Tr_End(A L_Q B)/((lambda_r+lambda_b) sqrt(rank(A)rank(B))) "
            "for every admitted pair, with no per-relatum selector."
        ),
        "reported_relation": (
            "Report the label-free normalized spectrum and squared contrast; the displayed 2x2 "
            "table is a derived diagnostic, not an inserted equality table."
        ),
        "generic_result": (
            "K has diagonal weights lambda_r/(lambda_r+lambda_b) and "
            "lambda_b/(lambda_r+lambda_b), zero cross entries, and unequal diagonal weights "
            "exactly on the declared generic domain."
        ),
        "tuned_null": (
            "At b^2=3 alpha c the weights both equal 1/2, leaving only a scalar delta skeleton; "
            "that boundary is a failed separation, not a promoted result."
        ),
        "semantic_ceiling": (
            "K is a narrow atemporal comparison.  Its diagonal factorization is not claimed to "
            "be irreducibly pairwise coupling, interaction, intervention or measurement."
        ),
    }


def qp_only_null_boundary() -> dict[str, str]:
    return {
        "spectral_algebra": "R[Q]=span{I,Q}=span{P1,P2} on the accepted uniaxial branch.",
        "block_scalar_boundary": (
            "Every target-free Q-only covariant matrix effect is a P1/P2 block scalar and adds "
            "no off-diagonal carrier."
        ),
        "rank_equality_null": (
            "Projector overlaps alone give a bare delta table; free block weights can fit any "
            "two desired unary answers and therefore do not predict F2a."
        ),
        "duplicated_mode_null": (
            "P1-I/3=Q/s and P2-2I/3=-Q/s, so the two traceless role carriers are one mode with "
            "opposite sign, not two independent modes."
        ),
        "why_hessian_is_extra_content": (
            "The accepted law's second derivative acts on the whole inherited carrier and has "
            "normal curvature sectors not supplied by the Q-only matrix effect algebra."
        ),
    }


def freedom_ledger() -> dict[str, dict[str, Any]]:
    zero = {"source": "none", "allowed_range": 0, "scale": "candidate", "complexity": 0}
    return {
        "inherited_f1_parameters": {
            "source": "public F1 imported alpha,b,c", "allowed_range": "alpha,b,c>0",
            "scale": "three inherited universal model parameters; not fitted here", "complexity": 3,
        },
        "route_choice": {
            "source": "declared INTRASTATE_UNIFORM_EFFECT_FAMILY candidate",
            "allowed_range": "one frozen categorical route", "scale": "architecture", "complexity": 1,
        },
        "hessian_candidate_choice": {
            "source": "unique second derivative of frozen V; its use as F2a candidate is declared",
            "allowed_range": "D^2 V only", "scale": "architecture", "complexity": 1,
        },
        "normalization_choice": {
            "source": "declared common positive lambda_r+lambda_b normalization",
            "allowed_range": "one frozen scale-free normalization", "scale": "report", "complexity": 1,
        },
        "tangent_carrier": {
            "source": "inherited linear Sym0(3) state space", "allowed_range": "its full tangent space",
            "scale": "standard mathematics; no physical mode import", "complexity": 0,
        },
        "new_numerical_parameters": dict(zero),
        "data_fitted_parameters": {**zero, "scale": "data"},
        "chosen_representative_basis_or_axis": {**zero, "scale": "description"},
        "new_physical_primitives": {**zero, "scale": "foundation"},
    }


def forbidden_inputs() -> tuple[str, ...]:
    return (
        "preferred representative, fixed axis, ordered eigenbasis, target projector, or matrix entry",
        "preloaded Pi_r/Pi_b split, desired response values, literal delta table, or rank lookup",
        "per-relatum post-selected selector or self-only comparison domain",
        "free block weights, fitted coefficients, hidden higher operator, or unregistered carrier",
        "orbit tangent counted as a physical or operational relatum",
        "Q=0 division, tuned-surface promotion, rejected branch, or parameter-fibre mixing",
        "physical effect, response, intervention, node, imprint, mode, particle, or measurement",
        "time, causality, persistence, geometry, action, GR, observable, data, or observation",
    )


def gate_applicability() -> dict[str, str]:
    return {
        "G0_GOAL": "REQUIRED - narrow F2a candidate and full-F2 ceiling frozen",
        "G1_CONVENTIONS": "REQUIRED - tangent, quotient-normal and comparison meanings fixed",
        "G2_CORE_ALGEBRA": "REQUIRED - exact Hessian, Riesz, spectrum and comparison identities",
        "G3_STRUCTURE": "REQUIRED - generated relata, uniform rule and non-tautology boundary",
        "G4_INDEPENDENT_CHECK": "REQUIRED - semantic, fail-closed and new-reader audits",
        "G5_LIMITS_REGRESSION": "REQUIRED - Q/P-only, tuned, origin, self-test and leakage nulls",
        "G6_PHYSICAL_MATCH": "N/A - no physical response, node, source, energy or imprint claim",
        "G7_OBSERVATION": "N/A - no observable, forward model or data",
        "G8_EXPORT": "N/A - internal Work2 candidate; no Canon, article, GitHub or Zenodo export",
    }


def review_requirements() -> dict[str, str]:
    return dict(EXPECTED_REVIEW_REQUIREMENTS)


def review_attestations() -> dict[str, dict[str, Any]]:
    return {
        "semantic_candidate_review": {
            "passed": True,
            "reviewer": "/root/f2_independent_review",
            "artifact": EXPECTED_REVIEW_REQUIREMENTS["semantic_candidate_review"],
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS[
                "semantic_candidate_review"
            ],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS[
                "semantic_candidate_review"
            ],
        },
        "fail_closed_code_review": {
            "passed": True,
            "reviewer": "/root/w209_no_go",
            "artifact": EXPECTED_REVIEW_REQUIREMENTS["fail_closed_code_review"],
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS[
                "fail_closed_code_review"
            ],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS[
                "fail_closed_code_review"
            ],
        },
        "new_reader_scope_review": {
            "passed": True,
            "reviewer": "/root/f2_contract_map",
            "artifact": EXPECTED_REVIEW_REQUIREMENTS["new_reader_scope_review"],
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS[
                "new_reader_scope_review"
            ],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS[
                "new_reader_scope_review"
            ],
        },
    }


def build_contract() -> dict[str, Any]:
    return {
        "CLAIM_ID": "W2_F2A_INTRASTATE_HESSIAN_COMPARISON_CANDIDATE_001",
        "CLAIM": (
            "Evaluate and, only on the declared generic branch, establish that the accepted F1 "
            "law's Hessian generates two internal relata and one invariant nontrivial atemporal "
            "comparison map; do not close full C0 F2."
        ),
        "TYPE": "CONDITIONAL_EXACT_F2A_CANDIDATE_EVALUATION",
        "MODEL_VERSION": MODEL_VERSION,
        "ASSUMPTIONS": (
            "The exact audited F1 result and its nine imported primitives are valid dependencies.",
            "The frozen F2a contract fixes the meaning of operational as a law-defined internal map.",
            "The w2_11 no-go applies to invariant whole-state readouts on one orbit, not to a "
            "derived intrastate comparison family.",
            "The C0 frozen header and PASS audit are operative; its older OPEN sentence is stale.",
        ),
        "DOMAIN": (
            "Accepted F1 positive branch with alpha,b,c>0 and b^2!=3 alpha c.  The tuned surface, "
            "Q=0, rejected stationary branch and invalid F1 coefficient boundaries are explicit nulls."
        ),
        "CONVENTIONS": (
            "Sym0(3) uses the inherited Frobenius contraction.  O(3) conjugation is internal "
            "equivalence.  Orbit tangents are quotient nulls.  Hessian/effect/response words in "
            "this file are algebraic and atemporal, never physical."
        ),
        "FREEDOM_LEDGER": freedom_ledger(),
        "DEPENDENCIES": {
            "research_rules": (
                "the frozen W2-C0 file is the exact public runtime contract source; private "
                "governance remains C0 provenance and is not a runtime file"
            ),
            "programme_contract": PROGRAM_CONTRACT,
            "frozen_f2a_contract": F2A_MODEL_VERSION,
            "single_orbit_no_go": W211_MODEL_VERSION,
            "conditional_public_f1": F1_MODEL_VERSION,
        },
        "METHOD": (
            "Differentiate the frozen F1 functional twice, construct its unique Frobenius-Riesz "
            "operator, derive the normal sector projectors as spectral polynomials, evaluate one "
            "predeclared comparison on all ordered sector pairs, and run exact nulls and reviews."
        ),
        "PASS_CONDITION": (
            "Exact dependencies and detached identities, all candidate derivations and controls, "
            "all 19 frozen F2a screening gates, exact scope boundaries, and three independent "
            "reviews pass on the generic domain."
        ),
        "FAIL_CONDITION": (
            "Any dependency/schema drift is INVALID.  Any well-formed false screening gate gives "
            "a completed non-promoted candidate.  The tuned and origin branches fail separation."
        ),
        "FALSIFIER": (
            "The Hessian is not the second derivative of frozen V, its Riesz spectrum/projectors "
            "or covariance identities fail, the generic weights coincide, a target is required, "
            "or the reference/tuned null fabricates a split."
        ),
        "RESIDUAL": "0 for every declared symbolic identity; no differential field equation is claimed.",
        "ERROR_BOUND": "0 for exact symbolic/discrete checks; numerical and data errors are N/A.",
        "VALIDITY_HEALTH": (
            "Conditional on imported F1 primitives and the generic open domain.  Normalization is "
            "regular there.  Stability is inherited from F1; dynamics, conservation, causality, "
            "physical degrees of freedom and observations are not established."
        ),
        "BRANCHES": {
            "generic_hessian_comparison": "CANDIDATE_FOR_EXACT_POSITIVE_F2A",
            "tuned_b2_equals_3_alpha_c": "EXACT_DEGENERACY__NO_F2A_SEPARATION_BY_THIS_CANDIDATE",
            "undifferentiated_Q_zero": "REFERENCE_NULL__NO_GENERATED_RELATA",
            "qp_only_matrix_effect": "NULL__RANK_UNARY_OR_EQUALITY_CONTENT_ONLY",
            "strong_pairwise_coupling": "NOT_PROVED__REMAINS_FOR_LATER_STRONGER_GATE",
            "full_c0_f2": "OPEN",
        },
        "OBSERVABLE_MAP": {"status": "N/A", "reason": "internal algebraic comparison only"},
        "FORWARD_MODEL": {"status": "N/A", "reason": "no observable or data chain"},
        "DATA_ROLE": {"status": "N/A", "reason": "no data used, fitted, or validated"},
        "IDENTIFIABILITY": (
            "Representative axes and sector labels are gauge.  The unordered normalized Hessian "
            "weights and squared contrast are exact invariants; physical identifiability is N/A."
        ),
        "BENCHMARK": (
            "Predeclared nulls are the scalar-normal tuned Hessian, Q=0 scalar Hessian, Q/P-only "
            "rank/equality algebra, self-only selectors, fixed targets, and incomplete equivalence."
        ),
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "CROSSCHECK": (
            "Coordinate differentiation, coordinate-free second variation, generalized Riesz "
            "diagonalization, spectral-polynomial reconstruction and exact covariance checks agree."
        ),
        "PROVENANCE": {
            "date": "2026-07-21",
            "reviewed_payload_sha256": EXPECTED_PAYLOAD_SHA256,
            "source_identities": {
                "w2_00": C0_SHA256,
                "w2_10": F2A_SOURCE_SHA256,
                "w2_11": W211_SOURCE_SHA256,
                "public_f1": F1_SOURCE_SHA256,
            },
            "output_artifact": (
                "RefG/work 2/w2_12_f2_intrastate_uniform_effect_family_candidate_gate.py"
            ),
        },
        "FILES": (
            "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
            "RefG/work 2/w2_10_f2a_internal_operational_distinction_contract.py",
            "RefG/work 2/w2_11_f2_single_orbit_readout_no_go_gate.py",
            "RefG/work 2/w2_09a_f1_proof/refg_f1_atemporal_structural_proof.py",
            "RefG/work 2/w2_12_f2_intrastate_uniform_effect_family_candidate_gate.py",
        ),
        "CANDIDATE_DEFINITION": candidate_definition(),
        "LAW_DERIVATION": law_derivation(),
        "RELATA_CONSTRUCTION": relata_construction(),
        "COMPARISON_MAP": comparison_map(),
        "QP_ONLY_NULL_BOUNDARY": qp_only_null_boundary(),
        "CANDIDATE_GATE_EVIDENCE": {
            "source": "w2_10 screening_gate_keys and screen_candidate",
            "all_19_gates_runtime_computed": "Every frozen gate is an exact bool from this candidate audit.",
            "false_gate_policy": "A false scientific gate is a valid non-promotion, not schema invalidity.",
            "review_policy": "F2a proof requires three detached reviews after the exact candidate screen.",
        },
        "FORBIDDEN_INPUTS": forbidden_inputs(),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "GATE_APPLICABILITY": gate_applicability(),
        "EXPORT_STATUS": dict(EXPECTED_EXPORT_STATUS),
        "INDEPENDENT_REVIEW": review_requirements(),
        "NEXT_TASK_POLICY": {
            "positive": NEXT_ATOMIC_TASK,
            "negative": "Remain in F2a and freeze a new versioned candidate; no automatic fallback.",
            "invalid_or_pending": "Restore or review this exact artifact before any downstream task.",
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


def exact_bool_schema(actual: Any, keys: frozenset[str]) -> bool:
    return bool(
        isinstance(actual, dict)
        and set(actual) == set(keys)
        and all(type(actual[key]) is bool for key in keys)
    )


def exact_true_map(actual: Any, keys: frozenset[str]) -> bool:
    return bool(
        exact_bool_schema(actual, keys)
        and all(actual[key] is True for key in keys)
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
        set(contract.get("CANDIDATE_DEFINITION", {})) == EXPECTED_CANDIDATE_KEYS,
        set(contract.get("LAW_DERIVATION", {})) == EXPECTED_LAW_KEYS,
        set(contract.get("RELATA_CONSTRUCTION", {})) == EXPECTED_RELATA_KEYS,
        set(contract.get("COMPARISON_MAP", {})) == EXPECTED_COMPARISON_KEYS,
        set(contract.get("QP_ONLY_NULL_BOUNDARY", {})) == EXPECTED_QP_NULL_KEYS,
        set(contract.get("CANDIDATE_GATE_EVIDENCE", {})) == EXPECTED_GATE_EVIDENCE_KEYS,
        set(contract.get("NEXT_TASK_POLICY", {})) == EXPECTED_NEXT_POLICY_KEYS,
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
    ))


def semantic_guard(contract: dict[str, Any]) -> bool:
    fields = (
        contract["CLAIM"], contract["DOMAIN"], contract["METHOD"],
        contract["VALIDITY_HEALTH"], *contract["CANDIDATE_DEFINITION"].values(),
        *contract["COMPARISON_MAP"].values(), *contract["SCOPE_CEILING"].keys(),
    )
    corpus = "\n".join(str(field) for field in fields).lower()
    forbidden = (
        "closes full f2", "physical response is proved", "physical mode is proved",
        "time emerges", "causality emerges", "node is proved", "imprint is proved",
        "gr is derived", "observationally validated", "irreducibly pairwise coupling is proved",
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
    paths = (C0_PATH, F2A_PATH, W211_PATH, F1_PATH)
    if not all(path.is_file() for path in paths):
        return False, {}
    c0_text = C0_PATH.read_text(encoding="utf-8")
    f2a = load_module(F2A_PATH, "refg_f2a_for_w212")
    w211 = load_module(W211_PATH, "refg_w211_for_w212")
    f2a_report = f2a.run_audit()
    w211_report = w211.run_audit()
    f2a_reviews = f2a_report.get("INDEPENDENT_REVIEW_ATTESTATIONS", {})
    w211_reviews = w211_report.get("INDEPENDENT_REVIEW_ATTESTATIONS", {})
    screening_controls = f2a.screening_controls()
    expected_imports = {
        "single_internal_carrier_Q", "Sym0_3_R_internal_state_space",
        "positive_internal_contraction_and_transpose",
        "matrix_product_and_algebraic_trace",
        "O3_conjugation_as_complete_declared_equivalence", "Q_sign_not_gauge",
        "quartic_functional_form_signs_and_truncation",
        "open_parameter_domain_alpha_b_c_positive", "atemporal_global_argmin_rule",
    }
    checks = all((
        C0_PATH.relative_to(ROOT).as_posix() == CLAIM_CONTRACT["FILES"][0],
        F2A_PATH.relative_to(ROOT).as_posix() == CLAIM_CONTRACT["FILES"][1],
        W211_PATH.relative_to(ROOT).as_posix() == CLAIM_CONTRACT["FILES"][2],
        F1_PATH.relative_to(ROOT).as_posix() == CLAIM_CONTRACT["FILES"][3],
        Path(__file__).resolve().relative_to(ROOT).as_posix() == CLAIM_CONTRACT["FILES"][4],
        file_sha256(C0_PATH) == C0_SHA256,
        file_sha256(F2A_PATH) == F2A_SOURCE_SHA256,
        file_sha256(W211_PATH) == W211_SOURCE_SHA256,
        file_sha256(F1_PATH) == F1_SOURCE_SHA256,
        f"`{PROGRAM_CONTRACT}`" in c0_text,
        "### `W2_F2_OPERATIONAL_RELATIONS`" in c0_text,
        "PASS_FOR_W2_C0_FREEZE" in c0_text,
        f2a.MODEL_VERSION == F2A_MODEL_VERSION,
        f2a_report.get("STATUS") == F2A_FROZEN_STATUS,
        f2a_report.get("AUDIT_VALID") is True,
        f2a_report.get("DETACHED_PAYLOAD_SHA256") == F2A_PAYLOAD_SHA256,
        f2a_report.get("DETACHED_VALIDATOR_SHA256") == F2A_VALIDATOR_SHA256,
        f2a_report.get("PROMOTED") is False,
        f2a_report.get("FULL_W2_F2_OPERATIONAL_RELATIONS") is False,
        f2a_report.get("SUBGATE_CLOSURE_FLAGS", {}).get("W2_F2A_CONTRACT_FROZEN") is True,
        f2a_report.get("SUBGATE_CLOSURE_FLAGS", {}).get("W2_F2A_CANDIDATE_EVALUATED") is False,
        f2a_report.get("SUBGATE_CLOSURE_FLAGS", {}).get(
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED"
        ) is False,
        set(f2a_reviews) == {
            "semantic_contract_review", "fail_closed_code_review", "new_reader_scope_review",
        },
        all(entry.get("passed") is True for entry in f2a_reviews.values()),
        len(f2a.screening_gate_keys()) == 19,
        set(f2a.screening_gate_keys()) == set(f2a.candidate_screening_gates()),
        exact_true_map(screening_controls, frozenset(screening_controls)),
        w211.MODEL_VERSION == W211_MODEL_VERSION,
        w211_report.get("STATUS") == W211_STATUS,
        w211_report.get("AUDIT_VALID") is True,
        w211_report.get("NO_GO_PROVED") is True,
        w211_report.get("DETACHED_PAYLOAD_SHA256") == W211_PAYLOAD_SHA256,
        w211_report.get("DETACHED_VALIDATOR_SHA256") == W211_VALIDATOR_SHA256,
        w211_report.get("F2A_CANDIDATE_EVALUATED") is False,
        w211_report.get("FULL_W2_F2_OPERATIONAL_RELATIONS") is False,
        w211_report.get("SUBGATE_CLOSURE_FLAGS", {}).get(
            "W2_F2A_SINGLE_ORBIT_WHOLE_STATE_INVARIANT_ROUTE_REJECTED"
        ) is True,
        w211_report.get("SUBGATE_CLOSURE_FLAGS", {}).get(
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED"
        ) is False,
        "intrastate_uniform_effect_family" in w211_report.get("PRESERVED_ROUTES", {}),
        set(w211_reviews) == {
            "semantic_theorem_review", "fail_closed_code_review", "new_reader_scope_review",
        },
        all(entry.get("passed") is True for entry in w211_reviews.values()),
        w211_report.get("CLOSURE_FLAGS") == EXPECTED_C0_CLOSURE_FLAGS,
        f2a.F1_MODEL_VERSION == F1_MODEL_VERSION,
        f2a.F1_STATUS == F1_STATUS,
        set(load_module(F1_PATH, "refg_f1_registry_for_w212").IMPORTED_PRIMITIVES)
        == expected_imports,
    ))
    return bool(checks), {
        "f2a_module": f2a,
        "f2a_report": f2a_report,
        "w211_report": w211_report,
    }


def matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def vector_of(matrix: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix([
        matrix[0, 0], matrix[1, 1], matrix[0, 1], matrix[0, 2], matrix[1, 2],
    ])


def superoperator_matrix(
    basis: tuple[sp.Matrix, ...], operation: Callable[[sp.Matrix], sp.Matrix],
) -> sp.Matrix:
    return sp.Matrix.hstack(*(vector_of(sp.simplify(operation(item))) for item in basis))


def candidate_algebra() -> dict[str, Any]:
    alpha, b, c, s = sp.symbols("alpha b c s", positive=True, real=True)
    x, y, u, v, w = sp.symbols("x y u v w", real=True)
    coordinates = (x, y, u, v, w)
    Q = sp.Matrix([
        [x, u, v],
        [u, y, w],
        [v, w, -x - y],
    ])
    basis = tuple(Q.diff(variable) for variable in coordinates)
    gram = sp.Matrix([
        [sp.trace(left * right) for right in basis]
        for left in basis
    ])
    I2 = sp.expand(sp.trace(Q**2))
    I3 = sp.expand(sp.trace(Q**3))
    potential = sp.expand(-alpha * I2 / 2 - b * I3 / 3 + c * I2**2 / 4)
    coordinate_hessian = sp.hessian(potential, coordinates)

    Q_star = s * sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
    star_substitution = {x: 2*s/3, y: -s/3, u: 0, v: 0, w: 0}
    on_shell = {alpha: (2*c*s**2 - b*s)/3}
    hessian_star = sp.simplify(coordinate_hessian.subs(star_substitution).subs(on_shell))
    riesz = sp.simplify(gram.inv() * hessian_star)

    def second_variation(q: sp.MatrixBase, left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Expr:
        q_i2 = sp.trace(q**2)
        return sp.simplify(
            (-alpha + c*q_i2) * sp.trace(left*right)
            + 2*c*sp.trace(q*left)*sp.trace(q*right)
            - b*sp.trace(q*(left*right + right*left))
        )

    formula_hessian = sp.Matrix([
        [second_variation(Q_star, left, right).subs(on_shell) for right in basis]
        for left in basis
    ])

    def riesz_action(q: sp.MatrixBase, variation: sp.MatrixBase) -> sp.Matrix:
        q_i2 = sp.trace(q**2)
        qv = sp.trace(q*variation)
        return sp.simplify(
            (-alpha + c*q_i2)*variation
            + 2*c*qv*q
            - b*(q*variation + variation*q - sp.Rational(2, 3)*qv*sp.eye(3))
        )

    formula_riesz = superoperator_matrix(
        basis, lambda variation: riesz_action(Q_star, variation).subs(on_shell)
    )

    radial_mode = sp.Matrix([sp.Rational(2, 3), -sp.Rational(1, 3), 0, 0, 0])
    biaxial_diagonal = sp.Matrix([0, 1, 0, 0, 0])
    biaxial_23 = sp.Matrix([0, 0, 0, 0, 1])
    orbit_12 = sp.Matrix([0, 0, 1, 0, 0])
    orbit_13 = sp.Matrix([0, 0, 0, 1, 0])
    modes = sp.Matrix.hstack(
        radial_mode, biaxial_diagonal, biaxial_23, orbit_12, orbit_13
    )
    lambda_r = sp.simplify(s*(4*c*s - b)/3)
    lambda_b = b*s
    mode_riesz = sp.simplify(modes.inv()*riesz*modes)
    expected_mode_riesz = sp.diag(lambda_r, lambda_b, lambda_b, 0, 0)

    pi_r = sp.simplify(modes*sp.diag(1, 0, 0, 0, 0)*modes.inv())
    pi_b = sp.simplify(modes*sp.diag(0, 1, 1, 0, 0)*modes.inv())
    pi_o = sp.simplify(modes*sp.diag(0, 0, 0, 1, 1)*modes.inv())

    I2_star = sp.simplify(sp.trace(Q_star**2))
    P1 = sp.simplify(sp.eye(3)/3 + Q_star/s)
    P2 = sp.simplify(sp.eye(3) - P1)

    def radial_action(variation: sp.MatrixBase) -> sp.Matrix:
        return sp.simplify(sp.trace(Q_star*variation)*Q_star/I2_star)

    def orbit_action(variation: sp.MatrixBase) -> sp.Matrix:
        return sp.simplify(P1*variation*P2 + P2*variation*P1)

    q_pi_r = superoperator_matrix(basis, radial_action)
    q_pi_o = superoperator_matrix(basis, orbit_action)
    q_pi_b = sp.simplify(sp.eye(5) - q_pi_r - q_pi_o)

    spectral_parameter = sp.symbols("spectral_parameter", real=True)
    characteristic = sp.factor((spectral_parameter*sp.eye(5) - riesz).det())
    expected_characteristic = sp.factor(
        spectral_parameter**2
        * (spectral_parameter-lambda_b)**2
        * (spectral_parameter-lambda_r)
    )
    spectral_pi_r = sp.simplify(
        riesz*(riesz-lambda_b*sp.eye(5))/(lambda_r*(lambda_r-lambda_b))
    )
    spectral_pi_b = sp.simplify(
        riesz*(riesz-lambda_r*sp.eye(5))/(lambda_b*(lambda_b-lambda_r))
    )
    spectral_pi_o = sp.simplify(
        (riesz-lambda_r*sp.eye(5))*(riesz-lambda_b*sp.eye(5))/(lambda_r*lambda_b)
    )

    lambda_sum = sp.simplify(lambda_r + lambda_b)

    def comparison(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Expr:
        denominator = lambda_sum*sp.sqrt(sp.trace(left)*sp.trace(right))
        return sp.simplify(sp.trace(left*riesz*right)/denominator)

    comparison_table = sp.Matrix([
        [comparison(pi_r, pi_r), comparison(pi_r, pi_b)],
        [comparison(pi_b, pi_r), comparison(pi_b, pi_b)],
    ])
    expected_table = sp.diag(lambda_r/lambda_sum, lambda_b/lambda_sum)

    D = sp.sqrt(b**2 + 24*alpha*c)
    s_plus = sp.simplify((b + D)/(4*c))
    lambda_r_plus = sp.simplify(lambda_r.subs(s, s_plus))
    lambda_b_plus = sp.simplify(lambda_b.subs(s, s_plus))
    expected_lambda_r_plus = sp.simplify(s_plus*D/3)
    expected_lambda_b_plus = b*s_plus
    mu_r = sp.simplify(lambda_r_plus/(lambda_r_plus+lambda_b_plus))
    mu_b = sp.simplify(lambda_b_plus/(lambda_r_plus+lambda_b_plus))
    expected_mu_r = D/(D+3*b)
    expected_mu_b = 3*b/(D+3*b)
    contrast = sp.simplify(mu_r-mu_b)
    contrast_factor = sp.simplify(8*(3*alpha*c-b**2)/(D+3*b)**2)
    contrast_sq = sp.simplify(contrast**2)
    tuned = {alpha: b**2/(3*c)}
    tuned_mu_r = sp.simplify(mu_r.subs(tuned))
    tuned_mu_b = sp.simplify(mu_b.subs(tuned))

    zero_substitution = {variable: 0 for variable in coordinates}
    origin_hessian = sp.simplify(coordinate_hessian.subs(zero_substitution))
    origin_riesz = sp.simplify(gram.inv()*origin_hessian)

    a1, a2, target_1, target_2 = sp.symbols(
        "a1 a2 target_1 target_2", real=True
    )
    block_effect = a1*P1 + a2*P2
    block_response_1 = sp.simplify(sp.trace(P1*block_effect)/sp.trace(P1))
    block_response_2 = sp.simplify(sp.trace(P2*block_effect)/sp.trace(P2))
    fitted_effect = target_1*P1 + target_2*P2
    overlap_table = sp.Matrix([
        [sp.trace(P1*P1)/sp.trace(P1), sp.trace(P1*P2)/sp.trace(P2)],
        [sp.trace(P2*P1)/sp.trace(P1), sp.trace(P2*P2)/sp.trace(P2)],
    ])
    rank_only_table = sp.Matrix([
        [sp.trace(pi_r*pi_r)/sp.sqrt(sp.trace(pi_r)**2),
         sp.trace(pi_r*pi_b)/sp.sqrt(sp.trace(pi_r)*sp.trace(pi_b))],
        [sp.trace(pi_b*pi_r)/sp.sqrt(sp.trace(pi_b)*sp.trace(pi_r)),
         sp.trace(pi_b*pi_b)/sp.sqrt(sp.trace(pi_b)**2)],
    ])

    theta_12, theta_13, theta_23 = sp.symbols(
        "theta_12 theta_13 theta_23", real=True
    )
    rotations = (
        sp.Matrix([[sp.cos(theta_12), -sp.sin(theta_12), 0],
                   [sp.sin(theta_12), sp.cos(theta_12), 0], [0, 0, 1]]),
        sp.Matrix([[sp.cos(theta_13), 0, -sp.sin(theta_13)], [0, 1, 0],
                   [sp.sin(theta_13), 0, sp.cos(theta_13)]]),
        sp.Matrix([[1, 0, 0], [0, sp.cos(theta_23), -sp.sin(theta_23)],
                   [0, sp.sin(theta_23), sp.cos(theta_23)]]),
        sp.diag(-1, 1, 1),
    )
    covariance_checks: list[bool] = []
    for transform in rotations:
        covariance_checks.append(
            matrix_zero(sp.trigsimp(transform.T*transform-sp.eye(3)))
        )
        rotated_q = sp.trigsimp(transform*Q_star*transform.T)
        for variation in basis:
            rotated_variation = sp.trigsimp(transform*variation*transform.T)
            lhs = riesz_action(rotated_q, rotated_variation)
            rhs = transform*riesz_action(Q_star, variation)*transform.T
            covariance_checks.append(matrix_zero(sp.trigsimp(lhs-rhs)))

    derivation_controls = {
        "coordinate_hessian_matches_coordinate_free_second_variation": (
            matrix_zero(hessian_star-formula_hessian)
        ),
        "riesz_operator_matches_hessian_and_is_self_adjoint": all((
            matrix_zero(riesz-formula_riesz),
            matrix_zero(gram*riesz-hessian_star),
            matrix_zero(riesz.T*gram-gram*riesz),
        )),
        "on_shell_spectral_decomposition_exact": all((
            matrix_zero(mode_riesz-expected_mode_riesz),
            matrix_zero(riesz-(lambda_r*pi_r+lambda_b*pi_b)),
        )),
        "characteristic_polynomial_and_multiplicities_exact": (
            characteristic == expected_characteristic
        ),
        "accepted_positive_branch_eigenvalues_exact": all((
            lambda_r_plus == expected_lambda_r_plus,
            lambda_b_plus == expected_lambda_b_plus,
            sp.ask(sp.Q.positive(expected_lambda_r_plus)) is True,
            sp.ask(sp.Q.positive(expected_lambda_b_plus)) is True,
        )),
    }
    relata_controls = {
        "q_generated_sector_projectors_exact": all((
            matrix_zero(pi_r-q_pi_r), matrix_zero(pi_b-q_pi_b), matrix_zero(pi_o-q_pi_o),
        )),
        "sector_projectors_idempotent_orthogonal_complete": all((
            matrix_zero(pi_r**2-pi_r), matrix_zero(pi_b**2-pi_b),
            matrix_zero(pi_o**2-pi_o), matrix_zero(pi_r*pi_b),
            matrix_zero(pi_r*pi_o), matrix_zero(pi_b*pi_o),
            matrix_zero(pi_r+pi_b+pi_o-sp.eye(5)),
        )),
        "sector_ranks_one_two_two_exact": (
            (pi_r.rank(), pi_b.rank(), pi_o.rank()) == (1, 2, 2)
        ),
        "generic_spectral_polynomials_generate_relata": all((
            matrix_zero(spectral_pi_r-pi_r), matrix_zero(spectral_pi_b-pi_b),
            matrix_zero(spectral_pi_o-pi_o),
        )),
        "orbit_sector_excluded_as_declared_equivalence": all((
            matrix_zero(riesz*pi_o),
            CLAIM_CONTRACT["RELATA_CONSTRUCTION"]["orbit_sector"].startswith("The rank-two zero"),
            CLAIM_CONTRACT["SCOPE_CEILING"]["independent_additive_physical_modes"] is False,
        )),
    }
    comparison_controls = {
        "one_predeclared_rule_covers_all_four_ordered_pairs": all((
            comparison_table.shape == (2, 2),
            CLAIM_CONTRACT["COMPARISON_MAP"]["domain"].startswith("All four ordered pairs"),
            "per-relatum selector" in CLAIM_CONTRACT["COMPARISON_MAP"]["uniform_rule"],
        )),
        "normalized_comparison_table_exact": matrix_zero(comparison_table-expected_table),
        "label_free_contrast_and_sum_exact": all((
            sp.simplify(mu_r-expected_mu_r) == 0,
            sp.simplify(mu_b-expected_mu_b) == 0,
            sp.simplify(mu_r+mu_b-1) == 0,
            sp.simplify(contrast_sq-(mu_b-mu_r)**2) == 0,
        )),
        "generic_open_domain_separation_exact": all((
            sp.simplify(contrast-contrast_factor) == 0,
            sp.simplify(D**2-9*b**2-8*(3*alpha*c-b**2)) == 0,
            tuned_mu_r == sp.Rational(1, 2), tuned_mu_b == sp.Rational(1, 2),
            "b^2 != 3 alpha c" in CLAIM_CONTRACT["CANDIDATE_DEFINITION"]["generic_domain"],
        )),
        "comparison_not_a_physical_or_temporal_response": all((
            CLAIM_CONTRACT["SCOPE_CEILING"]["physical_response_intervention_or_measurement"]
            is False,
            CLAIM_CONTRACT["SCOPE_CEILING"]["temporal_formation_persistence_or_causality"]
            is False,
            "not claimed" in CLAIM_CONTRACT["COMPARISON_MAP"]["semantic_ceiling"],
        )),
    }
    qp_null_controls = {
        "qp_spectral_algebra_closes_in_two_dimensions": all((
            matrix_zero(Q_star**2-(s/3)*Q_star-(2*s**2/9)*sp.eye(3)),
            matrix_zero(P1+P2-sp.eye(3)), matrix_zero(P1*P2),
        )),
        "qp_only_effects_are_block_scalar": all((
            matrix_zero(P1*block_effect*P2), matrix_zero(P2*block_effect*P1),
            block_response_1 == a1, block_response_2 == a2,
        )),
        "free_block_weights_fit_arbitrary_two_unary_targets": all((
            sp.simplify(sp.trace(P1*fitted_effect)/sp.trace(P1)-target_1) == 0,
            sp.simplify(sp.trace(P2*fitted_effect)/sp.trace(P2)-target_2) == 0,
        )),
        "projector_overlap_is_bare_delta": overlap_table == sp.eye(2),
        "traceless_p1_p2_carriers_duplicate_one_q_mode": all((
            matrix_zero(P1-sp.eye(3)/3-Q_star/s),
            matrix_zero(P2-2*sp.eye(3)/3+Q_star/s),
        )),
    }
    null_controls = {
        "tuned_surface_collapses_to_scalar_delta": all((
            tuned_mu_r == sp.Rational(1, 2), tuned_mu_b == sp.Rational(1, 2),
            sp.simplify(contrast_sq.subs(tuned)) == 0,
        )),
        "origin_hessian_is_scalar_and_generates_no_relata": all((
            matrix_zero(origin_hessian+alpha*gram),
            matrix_zero(origin_riesz+alpha*sp.eye(5)),
            sp.factor((spectral_parameter*sp.eye(5)-origin_riesz).det())
            == (spectral_parameter+alpha)**5,
            "no two normal spectral relata" in CLAIM_CONTRACT["CANDIDATE_DEFINITION"][
                "reference_boundary"
            ],
        )),
        "self_only_postselection_is_rejected_by_full_pair_domain": all((
            comparison_table[0, 1] == 0, comparison_table[1, 0] == 0,
            "All four ordered pairs" in CLAIM_CONTRACT["COMPARISON_MAP"]["domain"],
            any("self-only" in item for item in CLAIM_CONTRACT["FORBIDDEN_INPUTS"]),
        )),
        "rank_only_comparator_cannot_reproduce_generic_weights": all((
            rank_only_table == sp.eye(2),
            sp.simplify(mu_r-mu_b-contrast_factor) == 0,
        )),
        "preferred_axis_and_representative_entries_absent": all((
            CLAIM_CONTRACT["FREEDOM_LEDGER"]["chosen_representative_basis_or_axis"][
                "complexity"
            ] == 0,
            any("preferred representative" in item for item in CLAIM_CONTRACT["FORBIDDEN_INPUTS"]),
            set(potential.free_symbols) == {alpha, b, c, x, y, u, v, w},
        )),
        "invalid_f1_boundaries_do_not_inherit_candidate": all((
            sp.simplify(lambda_b.subs(b, 0)) == 0,
            "alpha,b,c>0" in CLAIM_CONTRACT["DOMAIN"],
            "rejected stationary branch" in CLAIM_CONTRACT["DOMAIN"],
        )),
    }
    covariance_controls = {
        "manifest_complete_o3_covariance_from_invariant_second_derivative": all((
            derivation_controls["coordinate_hessian_matches_coordinate_free_second_variation"],
            CLAIM_CONTRACT["LAW_DERIVATION"]["covariance"].startswith("O(3)-invariance"),
        )),
        "exact_generator_covariance_crosscheck": all(covariance_checks),
        "frobenius_pairing_and_supertrace_report_invariant": all((
            gram.det() != 0,
            matrix_zero(riesz.T*gram-gram*riesz),
            comparison_table == comparison_table.T,
        )),
        "label_swap_leaves_reported_contrast_invariant": (
            sp.simplify(contrast_sq-(mu_b-mu_r)**2) == 0
        ),
        "parameter_motion_not_confused_with_one_orbit_equivalence": all((
            sp.trace(Q_star**2) == 2*s**2/3,
            sp.simplify((2*s**2/3).subs(s, 1)-(2*s**2/3).subs(s, 2)) != 0,
            "parameter-fibre mixing" in " ".join(CLAIM_CONTRACT["FORBIDDEN_INPUTS"]),
        )),
    }
    return {
        "DERIVATION_CONTROLS": derivation_controls,
        "RELATA_CONTROLS": relata_controls,
        "COMPARISON_CONTROLS": comparison_controls,
        "QP_ONLY_NULL_CONTROLS": qp_null_controls,
        "NULL_CONTROLS": null_controls,
        "COVARIANCE_CONTROLS": covariance_controls,
        "DIAGNOSTICS": {
            "hessian_characteristic_polynomial": str(characteristic),
            "sector_ranks": [int(pi_r.rank()), int(pi_b.rank()), int(pi_o.rank())],
            "lambda_r_positive_branch": str(lambda_r_plus),
            "lambda_b_positive_branch": str(lambda_b_plus),
            "normalized_weights": [str(mu_r), str(mu_b)],
            "contrast": str(contrast),
            "tuned_weights": [str(tuned_mu_r), str(tuned_mu_b)],
            "comparison_table": str(comparison_table),
        },
    }


def review_schema_valid(attestations: Any, require_pass: bool) -> bool:
    fields = {
        "passed", "reviewer", "artifact", "reviewed_payload_sha256",
        "reviewed_validator_sha256",
    }
    expected_reviewers = {
        "semantic_candidate_review": "/root/f2_independent_review",
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
    wrong_payload["semantic_candidate_review"]["reviewed_payload_sha256"] = "WRONG"
    mutants.append(wrong_payload)
    wrong_validator = copy.deepcopy(base)
    wrong_validator["new_reader_scope_review"]["reviewed_validator_sha256"] = "WRONG"
    mutants.append(wrong_validator)
    wrong_reviewer = copy.deepcopy(base)
    wrong_reviewer["semantic_candidate_review"]["reviewer"] = "/root/self"
    mutants.append(wrong_reviewer)
    return all(not review_schema_valid(mutant, require_pass=False) for mutant in mutants)


def control_schemas_valid(algebra: Any) -> bool:
    if not isinstance(algebra, dict) or set(algebra) != {
        "DERIVATION_CONTROLS", "RELATA_CONTROLS", "COMPARISON_CONTROLS",
        "QP_ONLY_NULL_CONTROLS", "NULL_CONTROLS", "COVARIANCE_CONTROLS",
        "DIAGNOSTICS",
    }:
        return False
    return all((
        exact_bool_schema(algebra["DERIVATION_CONTROLS"], EXPECTED_DERIVATION_CONTROL_KEYS),
        exact_bool_schema(algebra["RELATA_CONTROLS"], EXPECTED_RELATA_CONTROL_KEYS),
        exact_bool_schema(algebra["COMPARISON_CONTROLS"], EXPECTED_COMPARISON_CONTROL_KEYS),
        exact_bool_schema(algebra["QP_ONLY_NULL_CONTROLS"], EXPECTED_QP_NULL_CONTROL_KEYS),
        exact_bool_schema(algebra["NULL_CONTROLS"], EXPECTED_NULL_CONTROL_KEYS),
        exact_bool_schema(algebra["COVARIANCE_CONTROLS"], EXPECTED_COVARIANCE_CONTROL_KEYS),
        isinstance(algebra["DIAGNOSTICS"], dict),
    ))


def candidate_gate_map(
    dependency_valid: bool, algebra: dict[str, Any], review_structure_valid: bool,
) -> dict[str, bool]:
    derivation = algebra["DERIVATION_CONTROLS"]
    relata = algebra["RELATA_CONTROLS"]
    comparison = algebra["COMPARISON_CONTROLS"]
    qp_null = algebra["QP_ONLY_NULL_CONTROLS"]
    nulls = algebra["NULL_CONTROLS"]
    covariance = algebra["COVARIANCE_CONTROLS"]
    all_controls = all(
        value is True
        for group in (derivation, relata, comparison, qp_null, nulls, covariance)
        for value in group.values()
    )
    freedom = CLAIM_CONTRACT["FREEDOM_LEDGER"]
    return {
        "f1_dependency_valid": bool(dependency_valid),
        "candidate_domain_map_and_branches_explicit": all((
            set(CLAIM_CONTRACT["CANDIDATE_DEFINITION"]) == EXPECTED_CANDIDATE_KEYS,
            "b^2!=3 alpha c" in CLAIM_CONTRACT["DOMAIN"],
            "tuned_b2_equals_3_alpha_c" in CLAIM_CONTRACT["BRANCHES"],
            "undifferentiated_Q_zero" in CLAIM_CONTRACT["BRANCHES"],
        )),
        "relata_generated_not_preloaded": all((
            relata["q_generated_sector_projectors_exact"],
            relata["generic_spectral_polynomials_generate_relata"],
            freedom["chosen_representative_basis_or_axis"]["complexity"] == 0,
        )),
        "uniform_comparison_family_generated_not_preloaded": all((
            derivation["coordinate_hessian_matches_coordinate_free_second_variation"],
            derivation["riesz_operator_matches_hessian_and_is_self_adjoint"],
            comparison["one_predeclared_rule_covers_all_four_ordered_pairs"],
            freedom["new_numerical_parameters"]["complexity"] == 0,
        )),
        "outputs_share_one_comparison_codomain": all((
            comparison["normalized_comparison_table_exact"],
            CLAIM_CONTRACT["COMPARISON_MAP"]["codomain"] == "One shared exact real scalar codomain.",
        )),
        "exact_nontrivial_separation_witness": all((
            comparison["generic_open_domain_separation_exact"],
            comparison["label_free_contrast_and_sum_exact"],
        )),
        "relation_not_reduced_to_preassigned_unary_or_bare_equality_data": all((
            exact_true_map(qp_null, EXPECTED_QP_NULL_CONTROL_KEYS),
            nulls["tuned_surface_collapses_to_scalar_delta"],
            comparison["generic_open_domain_separation_exact"],
            "not claimed to be irreducibly pairwise" in CLAIM_CONTRACT["COMPARISON_MAP"][
                "semantic_ceiling"
            ],
        )),
        "postselected_self_test_null_rejected": all((
            nulls["self_only_postselection_is_rejected_by_full_pair_domain"],
            comparison["one_predeclared_rule_covers_all_four_ordered_pairs"],
        )),
        "quotient_covariance_and_reported_invariance": exact_true_map(
            covariance, EXPECTED_COVARIANCE_CONTROL_KEYS
        ),
        "undifferentiated_reference_null": (
            nulls["origin_hessian_is_scalar_and_generates_no_relata"]
        ),
        "non_tuned_domain_and_regular_normalization": all((
            derivation["accepted_positive_branch_eigenvalues_exact"],
            comparison["generic_open_domain_separation_exact"],
            nulls["tuned_surface_collapses_to_scalar_delta"],
        )),
        "extra_primitive_ledger_complete": all((
            set(freedom) == EXPECTED_FREEDOM_KEYS,
            freedom["hessian_candidate_choice"]["complexity"] == 1,
            freedom["normalization_choice"]["complexity"] == 1,
            freedom["new_physical_primitives"]["complexity"] == 0,
            freedom["data_fitted_parameters"]["complexity"] == 0,
        )),
        "joint_admissibility_composition_and_common_action_derived": all((
            CLAIM_CONTRACT["CANDIDATE_DEFINITION"]["route"]
            == "INTRASTATE_UNIFORM_EFFECT_FAMILY",
            covariance["manifest_complete_o3_covariance_from_invariant_second_derivative"],
            "All four ordered pairs" in CLAIM_CONTRACT["COMPARISON_MAP"]["domain"],
        )),
        "full_f2_node_and_imprint_obligations_not_claimed": all((
            CLAIM_CONTRACT["CLOSURE_FLAGS"]["W2_F2_OPERATIONAL_RELATIONS"] is False,
            CLAIM_CONTRACT["SCOPE_CEILING"]["physical_node_or_location"] is False,
            CLAIM_CONTRACT["SCOPE_CEILING"]["atemporal_imprint_or_correlation_carrier"] is False,
            CLAIM_CONTRACT["SCOPE_CEILING"]["full_W2_F2_operational_relations"] is False,
        )),
        "operational_semantics_not_upgraded": all((
            comparison["comparison_not_a_physical_or_temporal_response"],
            CLAIM_CONTRACT["SCOPE_CEILING"]["irreducibly_pairwise_coupling"] is False,
            semantic_guard(CLAIM_CONTRACT),
        )),
        "external_observable_and_data_map_absent": all((
            CLAIM_CONTRACT["OBSERVABLE_MAP"]["status"] == "N/A",
            CLAIM_CONTRACT["FORWARD_MODEL"]["status"] == "N/A",
            CLAIM_CONTRACT["DATA_ROLE"]["status"] == "N/A",
            CLAIM_CONTRACT["SCOPE_CEILING"]["external_observable_or_data_map"] is False,
        )),
        "f3_temporal_and_causal_imports_absent": all((
            CLAIM_CONTRACT["CLOSURE_FLAGS"]["W2_F3_INTERNAL_ORDER_CAUSALITY"] is False,
            CLAIM_CONTRACT["SCOPE_CEILING"]["temporal_formation_persistence_or_causality"]
            is False,
        )),
        "positive_null_and_adversarial_controls_pass": bool(all_controls),
        "candidate_specific_independent_audit_required": bool(review_structure_valid),
    }


def mutation_controls(f2a_module: Any) -> dict[str, bool]:
    base = build_contract()
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
        "CANDIDATE_DEFINITION", "LAW_DERIVATION", "RELATA_CONSTRUCTION",
        "COMPARISON_MAP", "QP_ONLY_NULL_BOUNDARY", "CANDIDATE_GATE_EVIDENCE",
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
    missing_forbidden = copy.deepcopy(base)
    missing_forbidden["FORBIDDEN_INPUTS"] = missing_forbidden["FORBIDDEN_INPUTS"][:-1]
    registry_mutants.append(missing_forbidden)

    boundary_mutants: list[dict[str, Any]] = []
    for registry, key in (
        ("CLOSURE_FLAGS", "W2_F2_OPERATIONAL_RELATIONS"),
        ("SCOPE_CEILING", "physical_node_or_location"),
        ("SCOPE_CEILING", "irreducibly_pairwise_coupling"),
        ("EXPORT_STATUS", "GITHUB"),
    ):
        mutant = copy.deepcopy(base)
        mutant[registry][key] = True
        boundary_mutants.append(mutant)

    semantic_mutants: list[dict[str, Any]] = []
    for field, text in (
        ("CLAIM", " This closes full F2."),
        ("METHOD", " Physical response is proved."),
        ("VALIDITY_HEALTH", " Time emerges."),
    ):
        mutant = copy.deepcopy(base)
        mutant[field] += text
        semantic_mutants.append(mutant)
    pair_overclaim = copy.deepcopy(base)
    pair_overclaim["COMPARISON_MAP"]["semantic_ceiling"] = (
        "Irreducibly pairwise coupling is proved."
    )
    semantic_mutants.append(pair_overclaim)

    gate_keys = f2a_module.screening_gate_keys()
    all_true = {key: True for key in gate_keys}
    malformed: list[Any] = []
    for key in gate_keys:
        missing = dict(all_true)
        missing.pop(key)
        malformed.append(missing)
        nonboolean = dict(all_true)
        nonboolean[key] = 1
        malformed.append(nonboolean)
    extra_gate = dict(all_true)
    extra_gate["UNREGISTERED"] = True
    malformed.append(extra_gate)

    return {
        "missing_or_extra_contract_fields_rejected": all(
            not strict_contract_valid(mutant) for mutant in field_mutants
        ),
        "registry_drift_rejected": all(
            not strict_contract_valid(mutant) for mutant in registry_mutants
        ),
        "closure_scope_export_overclaims_rejected": all(
            not strict_contract_valid(mutant) for mutant in boundary_mutants
        ),
        "semantic_overclaims_rejected": all(
            not strict_contract_valid(mutant) for mutant in semantic_mutants
        ),
        "malformed_candidate_gate_maps_rejected": all(
            f2a_module.screen_candidate(mutant, True)["VALID"] is False
            for mutant in malformed
        ),
    }


def _run_audit_unchecked() -> dict[str, Any]:
    if not strict_contract_valid(CLAIM_CONTRACT):
        raise ValueError("contract payload or schema invalid")
    if detached_validator_sha256() != EXPECTED_VALIDATOR_SHA256:
        raise ValueError("validator source identity invalid")

    dependency_ok, dependencies = dependencies_valid()
    f2a_module = dependencies.get("f2a_module")
    if f2a_module is None:
        raise ValueError("F2a screening dependency unavailable")
    algebra = candidate_algebra()
    controls_schema = control_schemas_valid(algebra)
    review_structure = review_schema_valid(review_attestations(), require_pass=False)
    gates = candidate_gate_map(dependency_ok, algebra, review_structure)
    mutations = mutation_controls(f2a_module)

    base_structural = all((
        strict_contract_valid(CLAIM_CONTRACT),
        detached_validator_sha256() == EXPECTED_VALIDATOR_SHA256,
        dependency_ok,
        controls_schema,
        set(gates) == set(f2a_module.screening_gate_keys()),
        all(type(value) is bool for value in gates.values()),
        exact_true_map(mutations, EXPECTED_MUTATION_KEYS),
        exact_bool_map(CLAIM_CONTRACT["CLOSURE_FLAGS"], EXPECTED_C0_CLOSURE_FLAGS),
        exact_bool_map(CLAIM_CONTRACT["SCOPE_CEILING"], EXPECTED_SCOPE_CEILING),
        exact_bool_map(CLAIM_CONTRACT["EXPORT_STATUS"], EXPECTED_EXPORT_STATUS),
        review_schema_controls(),
        "w2_13_f2b_node_imprint_and_relational_completion_contract.py"
        in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
        "start full W2_F2 false" in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
    ))
    screen = f2a_module.screen_candidate(gates, bool(base_structural))
    attestations = review_attestations()
    checks = {
        "payload_validator_and_contract_schema_exact": all((
            strict_contract_valid(CLAIM_CONTRACT),
            detached_validator_sha256() == EXPECTED_VALIDATOR_SHA256,
        )),
        "c0_f2a_w211_f1_dependencies_exact": dependency_ok,
        "candidate_control_schemas_exact": controls_schema,
        "candidate_gate_schema_and_screen_valid": all((
            set(gates) == set(f2a_module.screening_gate_keys()),
            all(type(value) is bool for value in gates.values()),
            screen.get("VALID") is True,
            screen.get("PROMOTED") is False,
        )),
        "mutation_controls_exact": exact_true_map(mutations, EXPECTED_MUTATION_KEYS),
        "closure_scope_export_boundaries_exact": all((
            exact_bool_map(CLAIM_CONTRACT["CLOSURE_FLAGS"], EXPECTED_C0_CLOSURE_FLAGS),
            exact_bool_map(CLAIM_CONTRACT["SCOPE_CEILING"], EXPECTED_SCOPE_CEILING),
            exact_bool_map(CLAIM_CONTRACT["EXPORT_STATUS"], EXPECTED_EXPORT_STATUS),
        )),
        "review_attestation_schema_fail_closed": review_schema_controls(),
        "review_attestations_complete": review_schema_valid(attestations, require_pass=True),
        "next_task_policy_exact": all((
            set(CLAIM_CONTRACT["NEXT_TASK_POLICY"]) == EXPECTED_NEXT_POLICY_KEYS,
            "w2_13_f2b_node_imprint_and_relational_completion_contract.py"
            in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
            "start full W2_F2 false" in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
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
    candidate_evaluated = audit_valid
    f2a_proved = bool(audit_valid and screen.get("ELIGIBLE") is True)
    status = (
        PASS_STATUS if f2a_proved else
        NEGATIVE_STATUS if candidate_evaluated else
        READY_STATUS if structural_ready else
        INVALID_STATUS
    )
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": status,
        "AUDIT_VALID": audit_valid,
        "STRUCTURAL_READY_FOR_REVIEW": structural_ready,
        "CANDIDATE_EVALUATED": candidate_evaluated,
        "F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": f2a_proved,
        "PROMOTED_TO_F2A": f2a_proved,
        "PROMOTED_BEYOND_F2A": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "DETACHED_PAYLOAD_SHA256": detached_payload_sha256(CLAIM_CONTRACT),
        "DETACHED_VALIDATOR_SHA256": detached_validator_sha256(),
        "F2A_SCREEN": screen,
        "CANDIDATE_GATE_MAP": gates,
        "DERIVATION_CONTROLS": algebra["DERIVATION_CONTROLS"],
        "RELATA_CONTROLS": algebra["RELATA_CONTROLS"],
        "COMPARISON_CONTROLS": algebra["COMPARISON_CONTROLS"],
        "QP_ONLY_NULL_CONTROLS": algebra["QP_ONLY_NULL_CONTROLS"],
        "NULL_CONTROLS": algebra["NULL_CONTROLS"],
        "COVARIANCE_CONTROLS": algebra["COVARIANCE_CONTROLS"],
        "DIAGNOSTICS": algebra["DIAGNOSTICS"],
        "MUTATION_CONTROLS": mutations,
        "AUDIT_CHECKS": checks,
        "INDEPENDENT_REVIEW_ATTESTATIONS": attestations,
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F2A_CANDIDATE_EVALUATED": candidate_evaluated,
            "W2_F2A_INTRASTATE_HESSIAN_COMPARISON_PROVED": f2a_proved,
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": f2a_proved,
            "W2_F2A_IRREDUCIBLY_PAIRWISE_COUPLING_PROVED": False,
        },
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "PROMOTION_CEILING": "F2A_INTERNAL_ATEMPORAL_COMPARISON_ONLY",
        "NEXT_ATOMIC_TASK": CLAIM_CONTRACT["NEXT_ATOMIC_TASK"] if f2a_proved else (
            CLAIM_CONTRACT["NEXT_TASK_POLICY"]["negative"]
            if candidate_evaluated else CLAIM_CONTRACT["NEXT_TASK_POLICY"]["invalid_or_pending"]
        ),
    }


def fail_closed_invalid_report(error: Exception) -> dict[str, Any]:
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": INVALID_STATUS,
        "AUDIT_VALID": False,
        "STRUCTURAL_READY_FOR_REVIEW": False,
        "CANDIDATE_EVALUATED": False,
        "F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": False,
        "PROMOTED_TO_F2A": False,
        "PROMOTED_BEYOND_F2A": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "DETACHED_PAYLOAD_SHA256": "",
        "DETACHED_VALIDATOR_SHA256": "",
        "F2A_SCREEN": {
            "VALID": False, "ELIGIBLE": False, "PROMOTED": False,
            "STATUS": "INVALID_SCREEN__NO_ELIGIBILITY",
        },
        "CANDIDATE_GATE_MAP": {},
        "DERIVATION_CONTROLS": {
            key: False for key in EXPECTED_DERIVATION_CONTROL_KEYS
        },
        "RELATA_CONTROLS": {key: False for key in EXPECTED_RELATA_CONTROL_KEYS},
        "COMPARISON_CONTROLS": {
            key: False for key in EXPECTED_COMPARISON_CONTROL_KEYS
        },
        "QP_ONLY_NULL_CONTROLS": {
            key: False for key in EXPECTED_QP_NULL_CONTROL_KEYS
        },
        "NULL_CONTROLS": {key: False for key in EXPECTED_NULL_CONTROL_KEYS},
        "COVARIANCE_CONTROLS": {
            key: False for key in EXPECTED_COVARIANCE_CONTROL_KEYS
        },
        "DIAGNOSTICS": {},
        "MUTATION_CONTROLS": {key: False for key in EXPECTED_MUTATION_KEYS},
        "AUDIT_CHECKS": {key: False for key in EXPECTED_AUDIT_KEYS},
        "INDEPENDENT_REVIEW_ATTESTATIONS": {},
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F2A_CANDIDATE_EVALUATED": False,
            "W2_F2A_INTRASTATE_HESSIAN_COMPARISON_PROVED": False,
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": False,
            "W2_F2A_IRREDUCIBLY_PAIRWISE_COUPLING_PROVED": False,
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
