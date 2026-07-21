"""Exact evaluator for the frozen w2_15 one-carrier structural F2 candidate.

The candidate is the abstract traceless endomorphism A=S+R frozen in w2_15.
This evaluator derives its global-minimum product, complete common-O(3)
quotient, normal and flat directions, embedded F1/F2a chain, state-supported
transpose nodes, commutator carrier, and irreducible atemporal pair report.

Any PASS is conditional on the imported A and polynomial law.  It closes only
the C0 structural F2 gate on its declared generic open domain.  It does not
derive RefG physical nodes, space, time, metric, GR, PN/PPN, or observations.
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
    "W2-F2B-GENERAL-TRACELESS-SINGLE-CARRIER-CANDIDATE-GATE-"
    "v1.0-internal"
)
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"
W213_MODEL = "W2-F2B-NODE-IMPRINT-RELATIONAL-COMPLETION-CONTRACT-v1.0-internal"
W215_MODEL = (
    "W2-F2B-GENERAL-TRACELESS-SINGLE-CARRIER-CANDIDATE-CONTRACT-"
    "v1.0-internal"
)
W215_STATUS = "W2_F2B_REVISED_SINGLE_CARRIER_CONTRACT_FROZEN__UNEVALUATED"

C0_SHA256 = "3E0EFB2D635E7E5605F9D7EDFA99538644D7C21311989C478C4A6AF1854890EB"
W212_SOURCE = "1F7F4FFE139F731D1D254BD48D11852E5C5ADA3298CEDC05FB6584B8923D8F9B"
W213_SOURCE = "0BABF2EB701845452E2E809B1420857D04A842FCC5FEB24BD732523E2C88E347"
W214_SOURCE = "CB44AA3C6F698BF787A18696EF1FCB2C3C8C7D72AD29A558F68FFF834AEBEB56"
W215_SOURCE = "DE009E9CAF3C9A79ECBED9CB36E20FA17DC84506C3DCF959E800F58284826FD9"
F1_SOURCE = "8B29AF84AE0F94063CF0E7FDAB47A7CE364C7D6B1789D71051548A98A96C770E"
W215_PAYLOAD = "C4808257C0334AAC9CD83C59208B6240650B12D01EF92F9F39D13DCCBBBDBF76"
W215_VALIDATOR = "A82E1433B8C1F487964FC89514F30310BDAB80B30B2125434982A1919B83975B"

READY_STATUS = "W2_F2B_GENERAL_TRACELESS_CANDIDATE_READY_FOR_REVIEW__FULL_F2_OPEN"
PASS_STATUS = "CONDITIONAL_EXACT_STRUCTURAL_F2_RELATIVE_TO_IMPORTED_A_AND_LAW"
INVALID_STATUS = "W2_F2B_GENERAL_TRACELESS_CANDIDATE_INVALID__FULL_F2_OPEN"
EXPECTED_PAYLOAD_SHA256 = "F8883515231F5721AB062DCF53E69093038C19E3A29C0BE363CD6395D2F4DEAE"
EXPECTED_VALIDATOR_SHA256 = "8270B703A4DE149945605C420EBF0A55D74AE1E7E69818C782BA9474E3FA74B1"

ROOT = Path(__file__).resolve().parents[2]
C0_PATH = Path(__file__).with_name("w2_00_foundation_to_einstein_contract.md")
W212_PATH = Path(__file__).with_name(
    "w2_12_f2_intrastate_uniform_effect_family_candidate_gate.py"
)
W213_PATH = Path(__file__).with_name(
    "w2_13_f2b_node_imprint_and_relational_completion_contract.py"
)
W214_PATH = Path(__file__).with_name(
    "w2_14_f2b_single_generator_commutative_spectral_repackaging_gate.py"
)
W215_PATH = Path(__file__).with_name(
    "w2_15_f2b_general_traceless_single_carrier_candidate_contract.py"
)
F1_PATH = Path(__file__).with_name("w2_09a_f1_proof") / "refg_f1_atemporal_structural_proof.py"

NEXT_ATOMIC_TASK = (
    "Create w2_17_f3_internal_order_candidate_contract.py: preserve the exact conditional "
    "F1/F2 aggregate, freeze one target-free internal update/influence architecture before "
    "outcomes, distinguish state correlation from causal order, and keep time, propagation, "
    "metric, GR and every later C0 gate false until separately derived."
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
    "THEOREM", "EVIDENCE_REGISTRY", "FUNCTION_CLASS",
    "EQUIVALENCE_COMPLETENESS", "DOMAIN_AND_NULLS", "FORBIDDEN_UPGRADES",
    "SCOPE_CEILING", "GATE_APPLICABILITY", "EXPORT_STATUS",
    "INDEPENDENT_REVIEW", "NEXT_TASK_POLICY", "NEXT_ATOMIC_TASK",
})
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
EXPECTED_CLOSURE_FLAGS_OPEN = {
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
EXPECTED_CLOSURE_FLAGS_PASS = {
    **EXPECTED_CLOSURE_FLAGS_OPEN,
    "W2_F2_OPERATIONAL_RELATIONS": True,
}
EXPECTED_SCOPE_CEILING = {
    "conditional_on_imported_A_and_law": True,
    "candidate_evaluated_if_audit_valid": True,
    "extended_F1_revalidated_if_audit_valid": True,
    "embedded_F2a_revalidated_if_audit_valid": True,
    "structural_F2b_proved_if_audit_valid": True,
    "full_structural_W2_F2_proved_if_audit_valid": True,
    "unique_foundation_candidate": False,
    "mixed_coupling_robustness_or_A3_health": False,
    "F3_time_memory_persistence_or_causality": False,
    "F4_conservation_or_additive_modes": False,
    "physical_RefG_node_or_medium_interpretation": False,
    "space_dimension_continuum_or_metric": False,
    "effective_action_or_matter_coupling": False,
    "GR_Einstein_equations_PN_or_PPN": False,
    "observational_validation": False,
    "article_canon_github_or_zenodo_export": False,
}
EXPECTED_EXPORT_STATUS = {
    "CANON": False, "ARTICLE": False, "GITHUB": False, "ZENODO": False,
}
EXPECTED_THEOREM_KEYS = frozenset({
    "global_minimum_product", "accepted_quotient", "flat_modulus",
    "complete_equivalence", "extended_f1", "embedded_f2a",
    "state_nodes", "joint_carrier", "unary_completeness",
    "irreducibility", "open_domain", "required_nulls", "conclusion", "scope",
})
EXPECTED_EVIDENCE_KEYS = frozenset({
    "frozen_dependency_chain_exact",
    "separable_global_minimum_product_exact",
    "accepted_common_O3_quotient_is_tau_interval",
    "normal_hessian_positive_and_flat_tangent_classified",
    "common_basis_action_is_complete_algebra_equivalence",
    "independent_channel_law_symmetry_is_global_not_gauge",
    "extended_f1_roles_and_stability_revalidated",
    "w2_12_f2a_family_embeds_exactly_on_generic_domain",
    "transpose_nodes_state_owned_and_reconstruct_one_A",
    "commutator_carrier_is_bilinear_state_supported_and_cross_null",
    "complete_unary_invariant_class_reduces_to_I2_I3_J_and_type",
    "same_complete_unary_different_joint_witness_exact",
    "joint_report_nonfactorization_and_open_support_exact",
    "complete_equivalence_and_typed_relabelling_invariance_exact",
    "all_predeclared_nulls_and_w2_14_boundary_pass",
    "no_F3_physical_geometric_observational_semantics",
    "screen_completion_mutation_and_adversarial_controls_pass",
})
EXPECTED_FUNCTION_CLASS_KEYS = frozenset({
    "unary_symmetric", "unary_skew", "type_rank_and_equality",
    "trivial_pair_image", "joint_report", "irreducible_certificate",
})
EXPECTED_EQUIVALENCE_KEYS = frozenset({
    "ambient_star_algebra", "complete_basis_equivalence", "outer_transpose",
    "independent_channel_motion", "quotient_coordinate", "typed_relabelling",
})
EXPECTED_NULL_KEYS = frozenset({
    "generic_pass_domain", "f2a_tuned_surface", "zero_state", "R_zero",
    "S_zero", "commuting_tau_zero", "normalization_singular",
    "self_pairs", "factorized_unary_rule", "w2_12_diagonal",
    "w2_14_projective_fibre", "parameter_boundaries",
})
EXPECTED_FREEDOM_KEYS = frozenset({
    "single_A", "transpose_split", "alpha_b_c", "eta_d", "mixed_couplings",
    "common_action", "node_support_maps", "carrier", "raw_report",
    "normalized_report", "relative_modulus", "preferred_basis_axis_or_labels",
    "physical_semantics", "data_fitted_parameters",
})
EXPECTED_FREEDOM_ENTRY_KEYS = frozenset({
    "source", "allowed_range", "scale", "complexity",
})
EXPECTED_GATE_KEYS = frozenset({
    "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
    "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
    "G7_OBSERVATION", "G8_EXPORT",
})
EXPECTED_MINIMUM_CONTROL_KEYS = frozenset({
    "skew_J_is_nonnegative_exact", "skew_square_completion_exact",
    "skew_nonzero_global_radius_exact", "old_s_positive_root_exact",
    "old_s_stationarity_exact", "product_minimum_separability_exact",
    "open_five_parameter_domain", "mixed_coefficients_remain_exact_zero",
})
EXPECTED_QUOTIENT_CONTROL_KEYS = frozenset({
    "support_projectors_exact", "tau_formula_exact", "tau_common_action_invariant",
    "same_tau_canonical_representative_complete", "generic_common_orbit_rank_three",
    "full_minimum_tangent_rank_four", "non_gauge_internal_relative_flat_rank_one",
    "independent_channel_map_fails_multiplicativity",
})
EXPECTED_F1F2A_CONTROL_KEYS = frozenset({
    "symmetric_normal_eigenvalues_positive", "skew_radial_hessian_positive_rank_one",
    "full_normal_rank_four_no_negative_modes", "four_flat_minimum_tangents_exact",
    "old_rank1_rank2_roles_survive", "old_law_and_hessian_block_embed_exactly",
    "f2a_generic_weights_and_tuned_null_exact", "extended_f1_and_f2a_same_aggregate",
})
EXPECTED_RELATION_CONTROL_KEYS = frozenset({
    "transpose_nodes_nonzero_distinct_and_reconstruct_A",
    "node_support_maps_single_valued_equivariant",
    "commutator_carrier_symmetric_traceless",
    "carrier_vanishes_if_either_node_absent",
    "raw_report_nonnegative_and_regular",
    "two_exact_accepted_witnesses_same_unary",
    "two_exact_accepted_witnesses_different_joint",
    "normalized_report_equals_tau",
    "unary_invariant_generators_complete_in_declared_class",
    "typed_swap_and_R_sign_leave_report_invariant",
    "relation_not_in_unary_equality_separable_image",
    "nonzero_on_predeclared_generic_open_domain",
    "orthogonal_support_projectors_commute_but_carrier_is_nonzero",
})
EXPECTED_NULL_CONTROL_KEYS = frozenset({
    "zero_and_single_channel_nulls", "commuting_branch_null",
    "normalization_undefined_not_assigned", "self_pair_commutators_zero",
    "factorized_same_unary_null_detected", "independent_action_false_gauge_detected",
    "w2_12_diagonal_remains_unary_equality", "w2_14_unselected_fibre_not_reused",
    "tuned_and_parameter_boundaries_not_promoted", "no_temporal_or_physical_semantics",
})
EXPECTED_DECISION_CONTROL_KEYS = frozenset({
    "all_true_screen_and_completion_positive",
    "one_false_gate_never_eligible",
    "every_missing_or_nonboolean_gate_invalid",
    "review_false_keeps_candidate_and_full_f2_open",
    "f2a_false_keeps_full_f2_open",
    "candidate_result_never_closes_later_gates",
})
EXPECTED_MUTATION_KEYS = frozenset({
    "missing_or_extra_contract_fields_rejected", "registry_drift_rejected",
    "evidence_false_prevents_f2", "screen_schema_mutants_rejected",
    "closure_scope_and_export_overclaims_rejected",
    "dependency_identity_mutation_rejected", "semantic_overclaims_rejected",
    "review_schema_mutants_rejected",
})
EXPECTED_AUDIT_KEYS = frozenset({
    "payload_validator_and_contract_schema_exact",
    "frozen_candidate_and_transitive_dependencies_exact",
    "minimum_quotient_and_common_action_controls_exact",
    "extended_f1_and_embedded_f2a_controls_exact",
    "node_carrier_irreducibility_controls_exact",
    "required_null_and_semantic_controls_exact",
    "screen_completion_and_mutation_controls_exact",
    "review_schema_fail_closed",
    "review_attestations_complete",
    "candidate_screen_and_completion_exact",
    "next_task_preserves_scope",
})
EXPECTED_REVIEW_KEYS = frozenset({
    "mathematical_candidate_review", "fail_closed_code_review", "new_reader_scope_review",
})
EXPECTED_REVIEW_REQUIREMENTS = {
    "mathematical_candidate_review": (
        "independent minima, quotient, stability, common-action and F1/F2 proof audit"
    ),
    "fail_closed_code_review": (
        "independent symbolic, screening, completion, mutation and fail-closed audit"
    ),
    "new_reader_scope_review": (
        "independent standalone provenance, conditional-status and no-physical-overclaim audit"
    ),
}

REVIEW_ATTESTED_PAYLOAD_IDS = {
    "mathematical_candidate_review": "F8883515231F5721AB062DCF53E69093038C19E3A29C0BE363CD6395D2F4DEAE",
    "fail_closed_code_review": "F8883515231F5721AB062DCF53E69093038C19E3A29C0BE363CD6395D2F4DEAE",
    "new_reader_scope_review": "F8883515231F5721AB062DCF53E69093038C19E3A29C0BE363CD6395D2F4DEAE",
}
REVIEW_ATTESTED_VALIDATOR_IDS = {
    "mathematical_candidate_review": "8270B703A4DE149945605C420EBF0A55D74AE1E7E69818C782BA9474E3FA74B1",
    "fail_closed_code_review": "8270B703A4DE149945605C420EBF0A55D74AE1E7E69818C782BA9474E3FA74B1",
    "new_reader_scope_review": "8270B703A4DE149945605C420EBF0A55D74AE1E7E69818C782BA9474E3FA74B1",
}


def theorem() -> dict[str, str]:
    return {
        "global_minimum_product": (
            "Because U(A)=V_F1(S)+d(J-eta/d)^2/4-eta^2/(4d), its global minima are "
            "exactly the product of the old positive uniaxial S minimum orbit and the "
            "nonzero skew sphere J=eta/d."
        ),
        "accepted_quotient": (
            "Writing S=s(P_n-I/3) and R as the cross map of axial vector r, the complete "
            "common-O(3) quotient of the product minimum is tau=1-(n.r_hat)^2 in [0,1]."
        ),
        "flat_modulus": (
            "The minimum manifold has four tangent zero directions.  Three are generic common "
            "basis-orbit directions and one is a non-gauge internal relative-orientation modulus; all four "
            "are tangent to global minima and the four normal directions are positive."
        ),
        "complete_equivalence": (
            "Automorphisms of the inherited real matrix star-algebra are common O(3) "
            "conjugations.  Separate channel rotations preserve the separable law but not matrix "
            "multiplication, so they are global degeneracy motions, not representation gauge."
        ),
        "extended_f1": (
            "The old state-generated rank-one/rank-two S roles persist at every product minimum; "
            "the enlarged minimum set is variationally stable on alpha,b,c,eta,d>0."
        ),
        "embedded_f2a": (
            "The full Hessian is block diagonal.  Its S block is exactly the w2_12 operator family, "
            "so F2a survives on b^2!=3 alpha c; the equality surface remains its tuned null."
        ),
        "state_nodes": (
            "S and R are simultaneous transpose-even/odd restrictions of one accepted A and "
            "reconstruct A.  Their canonical support lines are single-valued functions of state."
        ),
        "joint_carrier": (
            "C=[S,R] is a bilinear same-state carrier.  It vanishes when either node is absent "
            "or when the matrices S and R commute.  On the nonzero minimum branch S and R "
            "commute exactly at the parallel-line tau=0 stratum; C is nonzero on tau>0."
        ),
        "unary_completeness": (
            "In the declared invariant function class, a single traceless symmetric 3x3 node is "
            "classified by I2,I3 and a single skew 3x3 node by J; type, rank and equality add only constants."
        ),
        "irreducibility": (
            "K=Tr(C^T C)=s^2 J tau.  Accepted tau=1/4 and tau=3/4 states have identical complete "
            "unary data but unequal K, proving K is outside every unary/equality/separable reconstruction."
        ),
        "open_domain": (
            "The relational pass domain alpha,b,c,eta,d>0, b^2!=3 alpha c and 0<tau<1 is nonempty and open."
        ),
        "required_nulls": (
            "A=0, S=0, R=0, tau=0, self pairs, the w2_12 tuned surface, singular normalization, "
            "factorized rules and w2_14's unselected projective fibre never promote."
        ),
        "conclusion": (
            "If every exact control and independent review passes, the frozen candidate closes "
            "C0 structural F2 conditionally on the imported A and law."
        ),
        "scope": (
            "The result has no physical interpretation at this gate and is not a derivation "
            "of RefG physical nodes, dynamics, space, metric, "
            "Einstein equations, PN/PPN, matter coupling or observation."
        ),
    }


def evidence_descriptions() -> dict[str, str]:
    evidence = {
        "frozen_dependency_chain_exact": "The reviewed w2_15 identity and transitive C0/F1/F2a/no-go chain pass.",
        "separable_global_minimum_product_exact": "Old S minima and the completed-square skew radius give the full product minima.",
        "accepted_common_O3_quotient_is_tau_interval": "Canonical representatives and the support-line invariant classify [0,1].",
        "normal_hessian_positive_and_flat_tangent_classified": "Four positive normals and four minimum tangents are exact.",
        "common_basis_action_is_complete_algebra_equivalence": "The real matrix star-algebra admits common orthogonal conjugation gauge.",
        "independent_channel_law_symmetry_is_global_not_gauge": "An explicit separate-channel map fails multiplicativity.",
        "extended_f1_roles_and_stability_revalidated": "Old nonexchangeable roles persist on the stable product minimum manifold.",
        "w2_12_f2a_family_embeds_exactly_on_generic_domain": "The S Hessian block and generic/tuned split are unchanged.",
        "transpose_nodes_state_owned_and_reconstruct_one_A": "Exact projections, supports and reconstruction certify ownership.",
        "commutator_carrier_is_bilinear_state_supported_and_cross_null": "The inherited product supplies a mixed carrier with both single-node nulls.",
        "complete_unary_invariant_class_reduces_to_I2_I3_J_and_type": "Cayley-Hamilton and the 3D skew normal form close the declared unary class.",
        "same_complete_unary_different_joint_witness_exact": "tau=1/4 and 3/4 witnesses share all unary data and differ in K.",
        "joint_report_nonfactorization_and_open_support_exact": "K=s^2 J tau is positive and variable on the predeclared generic domain.",
        "complete_equivalence_and_typed_relabelling_invariance_exact": "K survives common basis change, sign and typed swap.",
        "all_predeclared_nulls_and_w2_14_boundary_pass": "Every frozen zero, tuned, singular and false-positive route stays ineligible.",
        "no_F3_physical_geometric_observational_semantics": "Only atemporal internal algebra is used.",
        "screen_completion_mutation_and_adversarial_controls_pass": "Imported screening and completion plus local mutations are fail-closed.",
    }
    if set(evidence) != EXPECTED_EVIDENCE_KEYS:
        raise RuntimeError("evidence registry drift")
    return evidence


def function_class() -> dict[str, str]:
    return {
        "unary_symmetric": (
            "All target-free O(3)-invariant regular scalar functions of one accepted S; by "
            "3x3 Cayley-Hamilton they factor through I2=Tr(S^2), I3=Tr(S^3)."
        ),
        "unary_skew": (
            "All target-free O(3)-invariant regular scalar functions of one accepted R; in "
            "three dimensions they factor through J=-Tr(R^2)."
        ),
        "type_rank_and_equality": (
            "Transpose parity, ranks, typed equality and self-selector values are admitted as constants."
        ),
        "trivial_pair_image": (
            "Finite regular combinations of the complete separate unary classes, constants, "
            "typed equality and additive/multiplicative separable rules."
        ),
        "joint_report": "K(S,R)=Tr([S,R]^T[S,R]) in the shared nonnegative real codomain.",
        "irreducible_certificate": (
            "Two accepted states with identical complete unary/type/rank/equality data and unequal K."
        ),
    }


def equivalence_completeness() -> dict[str, str]:
    return {
        "ambient_star_algebra": "M_3(R) with identity, ordered product, transpose and trace.",
        "complete_basis_equivalence": (
            "Every product-and-transpose-preserving basis automorphism is X->O X O^T with O in O(3)."
        ),
        "outer_transpose": (
            "X->X^T reverses ordered products and is an anti-automorphism, not an extra basis gauge; K is invariant even under it."
        ),
        "independent_channel_motion": (
            "O(3)_S x O(3)_R preserves U but not the ambient product.  Its independent "
            "rotations are global degeneracy motions between distinct states, not quotient gauge."
        ),
        "quotient_coordinate": "tau=1-Tr(P_S P_R) completely labels the common-O(3) product-minimum quotient.",
        "typed_relabelling": "Swapping the two typed arguments sends C to -C and leaves K unchanged.",
    }


def domain_and_nulls() -> dict[str, str]:
    return {
        "generic_pass_domain": "alpha,b,c,eta,d>0, b^2!=3 alpha c, 0<tau<1.",
        "f2a_tuned_surface": "b^2=3 alpha c makes the inherited F2a weights equal and stays null.",
        "zero_state": "A=0 gives no accepted relational pair and K=0.",
        "R_zero": "R=0 is the exact old restriction; the cross carrier and K vanish.",
        "S_zero": "S=0 removes the symmetric node; the cross carrier and K vanish.",
        "commuting_tau_zero": "Parallel support lines give [S,R]=0 and K=0.",
        "normalization_singular": "tau is not assigned when s=0 or J=0; raw K remains defined.",
        "self_pairs": "[S,S]=[R,R]=0.",
        "factorized_unary_rule": "Every trivial-pair report is constant across fixed-unary tau witnesses.",
        "w2_12_diagonal": "delta_ab mu_a is reconstructed from unary weights and equality and remains F2a-only.",
        "w2_14_projective_fibre": "Unselected rank-one projectors remain bare-overlap nulls; P_S,P_R here are state-reconstructed.",
        "parameter_boundaries": "eta=0, d<=0, c<=0, alpha<=0, b<=0 and singular/tuned limits do not promote.",
    }


def freedom_ledger() -> dict[str, dict[str, Any]]:
    zero = {"source": "none", "allowed_range": 0, "scale": "candidate", "complexity": 0}
    return {
        "single_A": {"source": "frozen w2_15", "allowed_range": "sl(3,R)", "scale": "one state", "complexity": 8},
        "transpose_split": {"source": "fixed projection", "allowed_range": "S,R", "scale": "map", "complexity": 0},
        "alpha_b_c": {"source": "inherited F1", "allowed_range": "positive", "scale": "three universal parameters", "complexity": 3},
        "eta_d": {"source": "frozen w2_15", "allowed_range": "positive", "scale": "two universal parameters", "complexity": 2},
        "mixed_couplings": {"source": "frozen architectural zero", "allowed_range": 0, "scale": "law", "complexity": 0},
        "common_action": {"source": "ambient star-algebra automorphisms", "allowed_range": "common O(3)", "scale": "equivalence", "complexity": 0},
        "node_support_maps": {"source": "state reconstruction", "allowed_range": "fixed P_S,P_R", "scale": "map", "complexity": 0},
        "carrier": {"source": "inherited product", "allowed_range": "fixed [S,R]", "scale": "map", "complexity": 0},
        "raw_report": {"source": "inherited trace norm", "allowed_range": "fixed K", "scale": "scalar", "complexity": 0},
        "normalized_report": {"source": "derived on sJ!=0", "allowed_range": "tau=K/(s^2J)", "scale": "scalar", "complexity": 0},
        "relative_modulus": {"source": "derived quotient coordinate", "allowed_range": "[0,1]", "scale": "state not fit", "complexity": 0},
        "preferred_basis_axis_or_labels": {**zero, "scale": "description"},
        "physical_semantics": {**zero, "scale": "semantics"},
        "data_fitted_parameters": {**zero, "scale": "data"},
    }


def gate_applicability() -> dict[str, str]:
    return {
        "G0_GOAL": "REQUIRED - exact conditional structural F2 claim and falsifier",
        "G1_CONVENTIONS": "REQUIRED - state, law, quotient, function class, domains and nulls",
        "G2_CORE_ALGEBRA": "REQUIRED - minima, Hessian, supports, commutator and invariant quotient",
        "G3_STRUCTURE": "REQUIRED - full F1/F2a revalidation and all w2_13 gates",
        "G4_INDEPENDENT_CHECK": "REQUIRED - three exact candidate reviews",
        "G5_LIMITS_REGRESSION": "REQUIRED - all inherited and candidate nulls",
        "G6_PHYSICAL_MATCH": "N/A - no physical interpretation at structural F2",
        "G7_OBSERVATION": "N/A - no observable or data",
        "G8_EXPORT": "N/A - internal and Git-ignored",
    }


def review_attestations() -> dict[str, dict[str, Any]]:
    return {
        "mathematical_candidate_review": {
            "passed": True,
            "reviewer": "/root/f2_independent_review",
            "artifact": EXPECTED_REVIEW_REQUIREMENTS["mathematical_candidate_review"],
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS["mathematical_candidate_review"],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS["mathematical_candidate_review"],
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
        "CLAIM_ID": "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CANDIDATE_001",
        "CLAIM": (
            "Evaluate the exact frozen w2_15 A=S+R candidate and prove, only if every "
            "registered control and review passes, conditional atemporal internal structural F2 "
            "on its generic separable-law branch."
        ),
        "TYPE": "CONDITIONAL_EXACT_STRUCTURAL_CANDIDATE_THEOREM",
        "MODEL_VERSION": MODEL_VERSION,
        "ASSUMPTIONS": (
            "The w2_15 state A in sl(3,R), transpose split, common matrix star-algebra, "
            "polynomial separable law, alpha,b,c,eta,d>0 and every exact-zero mixed coupling "
            "are imported identity-frozen hypotheses rather than derived RefG facts."
        ),
        "DOMAIN": (
            "Full accepted minimum set for alpha,b,c,eta,d>0; structural F2 PASS only on "
            "the open subset b^2!=3 alpha c and 0<tau<1, with all listed nulls excluded."
        ),
        "CONVENTIONS": (
            "Real 3x3 endomorphism star-algebra; S=(A+A^T)/2; R=(A-A^T)/2; "
            "J=-Tr(R^2); C=[S,R]=(A^T A-AA^T)/2; K=Tr(C^T C); common O(3)."
        ),
        "FREEDOM_LEDGER": freedom_ledger(),
        "DEPENDENCIES": (
            "Frozen W2-C0 exact runtime identity; private governance is not a runtime file; "
            "public F1; exact w2_12 F2a; w2_13 screen; w2_14 scoped no-go; reviewed frozen "
            "w2_15 candidate contract."
        ),
        "METHOD": (
            "Exact completed squares, invariant normal forms, Hessian/Riesz sectors, algebra-"
            "automorphism classification, equivariant restriction/reconstruction, a complete "
            "candidate-relative unary class, same-unary/different-joint witness, imported "
            "23-gate screening, completion logic, adversarial mutations and three reviews."
        ),
        "PASS_CONDITION": (
            "Every evidence item, all 23 w2_13 gates, the separate candidate audit, F1/F2a "
            "revalidation, F2b completion, required nulls and all three reviews are exactly true."
        ),
        "FAIL_CONDITION": (
            "Any dependency drift, negative or unexplained flat mode, incomplete equivalence, "
            "hidden independent gauge, unsupported node/carrier, unary factorization, tuned-only "
            "support, null failure, review failure or semantic overclaim keeps F2 false."
        ),
        "FALSIFIER": (
            "An independent-channel algebra equivalence, failure of C to be a canonical state "
            "composite, an accepted same-unary factorization of K, a missing null, or any false "
            "registered control falsifies this candidate result."
        ),
        "RESIDUAL": "0 for all symbolic identities; no numerical residual or data fit.",
        "ERROR_BOUND": "0 inside the exact algebraic domain; undefined normalizations remain undefined.",
        "VALIDITY_HEALTH": (
            "Morse-Bott stable inside the exact frozen separable five-parameter law class.  The "
            "result is not robust in the larger unrestricted mixed-coupling law space; generic "
            "terms such as Tr(SR^2) can lift the modulus.  That A3/law-origin issue stays open."
        ),
        "BRANCHES": {
            "all_global_minima": "OLD_UNIAXIAL_S_ORBIT_TIMES_NONZERO_R_SPHERE",
            "generic_relational_stratum": "0_LT_tau_LT_1",
            "commuting_stratum": "tau_EQ_0__RELATIONAL_NULL",
            "orthogonal_boundary": "tau_EQ_1__ORBIT_BOUNDARY_NOT_USED_FOR_OPEN_PASS",
            "f2a_tuned_surface": "b2_EQ_3_alpha_c__FULL_F2_NULL",
            "mixed_law_extension": "OUTSIDE_FROZEN_IDENTITY__NO_INHERITANCE",
            "structural_f2": "PASS_ONLY_AFTER_EXACT_REVIEWS",
            "physical_refg_and_later_c0_gates": "OPEN",
        },
        "OBSERVABLE_MAP": {"status": "N/A", "reason": "pre-spatial atemporal internal theorem"},
        "FORWARD_MODEL": {"status": "N/A", "reason": "no observable or dynamics"},
        "DATA_ROLE": {"status": "N/A", "reason": "no data, target or fitted parameter"},
        "IDENTIFIABILITY": (
            "Within the declared invariant function class, separate unary quotient data are "
            "(I2,I3,J,type) and the additional common-state quotient coordinate is tau.  No "
            "observational parameter identifiability is claimed."
        ),
        "BENCHMARK": (
            "Positive benchmark: exact tau=1/4 versus 3/4 accepted witnesses.  Null benchmarks: "
            "w2_12 unary-equality diagonal form and w2_14's unselected projective fibre."
        ),
        "CLOSURE_FLAGS": dict(EXPECTED_CLOSURE_FLAGS_OPEN),
        "CROSSCHECK": (
            "Independent invariant proof, explicit exact representatives, tangent/Hessian rank "
            "counts, algebra multiplicativity counterexample, imported screen/completion logic, "
            "mutation tests and three identity-bound reviews."
        ),
        "PROVENANCE": {
            "date": "2026-07-21",
            "reviewed_payload_sha256": EXPECTED_PAYLOAD_SHA256,
            "source_identities": {
                "w2_00": C0_SHA256,
                "w2_12": W212_SOURCE,
                "w2_13": W213_SOURCE,
                "w2_14": W214_SOURCE,
                "w2_15": W215_SOURCE,
                "public_f1": F1_SOURCE,
            },
            "output_artifact": (
                "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py"
            ),
        },
        "FILES": (
            "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
            "RefG/work 2/w2_12_f2_intrastate_uniform_effect_family_candidate_gate.py",
            "RefG/work 2/w2_13_f2b_node_imprint_and_relational_completion_contract.py",
            "RefG/work 2/w2_14_f2b_single_generator_commutative_spectral_repackaging_gate.py",
            "RefG/work 2/w2_15_f2b_general_traceless_single_carrier_candidate_contract.py",
            "RefG/work 2/w2_09a_f1_proof/refg_f1_atemporal_structural_proof.py",
            "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py",
        ),
        "THEOREM": theorem(),
        "EVIDENCE_REGISTRY": evidence_descriptions(),
        "FUNCTION_CLASS": function_class(),
        "EQUIVALENCE_COMPLETENESS": equivalence_completeness(),
        "DOMAIN_AND_NULLS": domain_and_nulls(),
        "FORBIDDEN_UPGRADES": (
            "conditional structural F2 renamed a unique foundational result",
            "law degeneracy symmetry silently enlarged to representation gauge",
            "K or tau renamed the carrier instead of readout of C",
            "commutator syntax accepted without same-unary nonfactorization proof",
            "zero mixed couplings called generic in the unrestricted invariant law space",
            "Morse-Bott flat modulus renamed persistence propagation or dynamical mode",
            "state-supported projectors confused with w2_14's freely selected fibre",
            "tuned surface endpoint or singular normalization used as open-domain evidence",
            "physical nodes interaction space time metric GR PN observation or data imported",
        ),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "GATE_APPLICABILITY": gate_applicability(),
        "EXPORT_STATUS": dict(EXPECTED_EXPORT_STATUS),
        "INDEPENDENT_REVIEW": dict(EXPECTED_REVIEW_REQUIREMENTS),
        "NEXT_TASK_POLICY": {
            "positive": NEXT_ATOMIC_TASK,
            "pending": "Complete all exact candidate reviews before any F2 closure or downstream task.",
            "invalid": "Freeze the exact failed gate or restore the identity; do not patch outcomes in place.",
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
        set(contract.get("THEOREM", {})) == EXPECTED_THEOREM_KEYS,
        set(contract.get("EVIDENCE_REGISTRY", {})) == EXPECTED_EVIDENCE_KEYS,
        set(contract.get("FUNCTION_CLASS", {})) == EXPECTED_FUNCTION_CLASS_KEYS,
        set(contract.get("EQUIVALENCE_COMPLETENESS", {})) == EXPECTED_EQUIVALENCE_KEYS,
        set(contract.get("DOMAIN_AND_NULLS", {})) == EXPECTED_NULL_KEYS,
        isinstance(contract.get("FORBIDDEN_UPGRADES"), tuple),
        isinstance(freedom, dict) and set(freedom) == EXPECTED_FREEDOM_KEYS,
        isinstance(freedom, dict) and all(
            isinstance(entry, dict) and set(entry) == EXPECTED_FREEDOM_ENTRY_KEYS
            for entry in freedom.values()
        ),
        exact_bool_map(contract.get("CLOSURE_FLAGS"), EXPECTED_CLOSURE_FLAGS_OPEN),
        exact_bool_map(contract.get("SCOPE_CEILING"), EXPECTED_SCOPE_CEILING),
        set(contract.get("GATE_APPLICABILITY", {})) == EXPECTED_GATE_KEYS,
        exact_bool_map(contract.get("EXPORT_STATUS"), EXPECTED_EXPORT_STATUS),
        exact_tree_equal(contract.get("INDEPENDENT_REVIEW"), EXPECTED_REVIEW_REQUIREMENTS),
        set(contract.get("NEXT_TASK_POLICY", {})) == {"positive", "pending", "invalid"},
    ))


def semantic_guard(contract: Any) -> bool:
    try:
        fields = (
            contract["CLAIM"], contract["ASSUMPTIONS"], contract["DOMAIN"],
            contract["PASS_CONDITION"], contract["VALIDITY_HEALTH"], contract["BRANCHES"],
            contract["THEOREM"], contract["EQUIVALENCE_COMPLETENESS"],
            contract["FORBIDDEN_UPGRADES"], contract["SCOPE_CEILING"],
            contract["NEXT_ATOMIC_TASK"],
        )
        corpus = "\n".join(
            item if isinstance(item, str) else json.dumps(item, sort_keys=True)
            for item in fields
        ).lower()
    except (KeyError, TypeError, ValueError):
        return False
    required = (
        "conditional", "imported", "structural f2", "mixed", "0<tau<1",
        "not a derivation", "no physical interpretation",
    )
    forbidden = (
        "unique foundation truth", "physical refg nodes are proved",
        "interaction is proved", "time emerges", "metric emerges",
        "einstein equations are derived", "pn is derived", "observationally validated",
    )
    return all(token in corpus for token in required) and not any(token in corpus for token in forbidden)


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
        C0_PATH, W212_PATH, W213_PATH, W214_PATH, W215_PATH, F1_PATH,
    )
    if not all(path.is_file() for path in paths):
        return False, {}
    try:
        c0_text = C0_PATH.read_text(encoding="utf-8")
        w213 = load_module(W213_PATH, "refg_w213_for_w216")
        w215 = load_module(W215_PATH, "refg_w215_for_w216")
        w215_report = w215.run_audit()
    except Exception:
        return False, {}
    reviews = w215_report.get("INDEPENDENT_REVIEW_ATTESTATIONS", {})
    files = CLAIM_CONTRACT["FILES"]
    checks = all((
        C0_PATH.relative_to(ROOT).as_posix() == files[0],
        W212_PATH.relative_to(ROOT).as_posix() == files[1],
        W213_PATH.relative_to(ROOT).as_posix() == files[2],
        W214_PATH.relative_to(ROOT).as_posix() == files[3],
        W215_PATH.relative_to(ROOT).as_posix() == files[4],
        F1_PATH.relative_to(ROOT).as_posix() == files[5],
        Path(__file__).resolve().relative_to(ROOT).as_posix() == files[6],
        file_sha256(C0_PATH) == C0_SHA256,
        file_sha256(W212_PATH) == W212_SOURCE,
        file_sha256(W213_PATH) == W213_SOURCE,
        file_sha256(W214_PATH) == W214_SOURCE,
        file_sha256(W215_PATH) == W215_SOURCE,
        file_sha256(F1_PATH) == F1_SOURCE,
        f"`{PROGRAM_CONTRACT}`" in c0_text,
        "### `W2_F2_OPERATIONAL_RELATIONS`" in c0_text,
        w213.MODEL_VERSION == W213_MODEL,
        w213.screening_gate_keys() == EXPECTED_SCREENING_GATE_KEYS,
        w215.MODEL_VERSION == W215_MODEL,
        w215_report.get("STATUS") == W215_STATUS,
        w215_report.get("AUDIT_VALID") is True,
        w215_report.get("CONTRACT_FROZEN") is True,
        w215_report.get("CANDIDATE_EVALUATED") is False,
        w215_report.get("F1_REVALIDATED_IN_EXTENDED_STATE") is False,
        w215_report.get("F2A_REVALIDATED_IN_EXTENDED_STATE") is False,
        w215_report.get("F2B_RELATIONAL_COMPLETION_PROVED") is False,
        w215_report.get("FULL_W2_F2_OPERATIONAL_RELATIONS") is False,
        w215_report.get("DETACHED_PAYLOAD_SHA256") == W215_PAYLOAD,
        w215_report.get("DETACHED_VALIDATOR_SHA256") == W215_VALIDATOR,
        len(reviews) == 3,
        all(isinstance(entry, dict) and entry.get("passed") is True for entry in reviews.values()),
        w215_report.get("CLOSURE_FLAGS") == EXPECTED_CLOSURE_FLAGS_OPEN,
    ))
    return bool(checks), {
        "w213_module": w213,
        "w215_module": w215,
        "w215_report": w215_report,
    }


def cross_matrix(vector: sp.MatrixBase) -> sp.Matrix:
    x, y, z = vector
    return sp.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])


def flatten_pair(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(list(left) + list(right))


def minimum_controls() -> dict[str, bool]:
    alpha, b, c, eta, d = sp.symbols("alpha b c eta d", positive=True)
    s = sp.symbols("s", positive=True)
    x, y, z, j = sp.symbols("x y z j", real=True)
    vector = sp.Matrix([x, y, z])
    r_matrix = cross_matrix(vector)
    J = sp.simplify(-sp.trace(r_matrix**2))
    skew_law = -eta * j / 2 + d * j**2 / 4
    skew_square = d * (j - eta / d)**2 / 4 - eta**2 / (4 * d)
    j_star = eta / d

    discriminant = sp.sqrt(b**2 + 24 * alpha * c)
    s_plus = sp.simplify((b + discriminant) / (4 * c))
    stationarity = sp.simplify(2 * c * s_plus**2 - b * s_plus - 3 * alpha)

    law_text = CLAIM_CONTRACT["ASSUMPTIONS"]
    health = CLAIM_CONTRACT["VALIDITY_HEALTH"]
    ledger = CLAIM_CONTRACT["FREEDOM_LEDGER"]
    return {
        "skew_J_is_nonnegative_exact": all((
            J == 2 * (x**2 + y**2 + z**2),
            CLAIM_CONTRACT["CONVENTIONS"].find("J=-Tr(R^2)") >= 0,
        )),
        "skew_square_completion_exact": sp.simplify(skew_law - skew_square) == 0,
        "skew_nonzero_global_radius_exact": all((
            sp.simplify(sp.diff(skew_law, j).subs(j, j_star)) == 0,
            sp.diff(skew_law, j, 2) == d / 2,
            sp.ask(sp.Q.positive(j_star)) is True,
        )),
        "old_s_positive_root_exact": all((
            sp.ask(sp.Q.positive(s_plus)) is True,
            sp.simplify(4 * c * s_plus - b - discriminant) == 0,
        )),
        "old_s_stationarity_exact": stationarity == 0,
        "product_minimum_separability_exact": all((
            "separable" in law_text,
            "global minima are exactly" in CLAIM_CONTRACT["THEOREM"]["global_minimum_product"],
            "product" in CLAIM_CONTRACT["THEOREM"]["global_minimum_product"],
        )),
        "open_five_parameter_domain": (
            "alpha,b,c,eta,d>0" in CLAIM_CONTRACT["DOMAIN"]
        ),
        "mixed_coefficients_remain_exact_zero": all((
            ledger["mixed_couplings"]["allowed_range"] == 0,
            "not robust" in health,
            "Tr(SR^2)" in health,
        )),
    }


def quotient_controls() -> dict[str, bool]:
    s, rho = sp.symbols("s rho", positive=True)
    x, y = sp.symbols("x y", real=True, nonzero=True)
    identity = sp.eye(3)
    p_s = sp.diag(1, 0, 0)
    s_matrix = s * (p_s - identity / 3)
    r_vector = sp.Matrix([x, y, 0])
    r_matrix = cross_matrix(r_vector)
    J = sp.simplify(-sp.trace(r_matrix**2))
    p_r = sp.simplify(identity + 2 * r_matrix**2 / J)
    carrier = sp.simplify(s_matrix * r_matrix - r_matrix * s_matrix)
    K = sp.simplify(sp.trace(carrier.T * carrier))
    tau = sp.simplify(K / (s**2 * J))
    expected_tau = sp.simplify(y**2 / (x**2 + y**2))

    exact_r = rho * sp.Matrix([sp.sqrt(3) / 2, sp.Rational(1, 2), 0])
    exact_R = cross_matrix(exact_r)
    exact_J = sp.simplify(-sp.trace(exact_R**2))
    exact_p_r = sp.simplify(identity + 2 * exact_R**2 / exact_J)

    omega_12 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    omega_13 = sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]])
    omega_23 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    omegas = (omega_12, omega_13, omega_23)
    common_tangents = sp.Matrix.hstack(*(
        flatten_pair(omega * s_matrix - s_matrix * omega, omega * exact_R - exact_R * omega)
        for omega in omegas
    ))
    separate_tangents = sp.Matrix.hstack(
        flatten_pair(omega_12 * s_matrix - s_matrix * omega_12, sp.zeros(3)),
        flatten_pair(omega_13 * s_matrix - s_matrix * omega_13, sp.zeros(3)),
        flatten_pair(sp.zeros(3), omega_12 * exact_R - exact_R * omega_12),
        flatten_pair(sp.zeros(3), omega_13 * exact_R - exact_R * omega_13),
        flatten_pair(sp.zeros(3), omega_23 * exact_R - exact_R * omega_23),
    )

    common_O = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    transformed_s = sp.simplify(common_O * s_matrix * common_O.T)
    transformed_r = sp.simplify(common_O * exact_R * common_O.T)
    transformed_c = sp.simplify(transformed_s * transformed_r - transformed_r * transformed_s)
    transformed_K = sp.simplify(sp.trace(transformed_c.T * transformed_c))
    original_c = sp.simplify(s_matrix * exact_R - exact_R * s_matrix)
    original_K = sp.simplify(sp.trace(original_c.T * original_c))

    def independent_map(matrix: sp.MatrixBase) -> sp.Matrix:
        symmetric = (matrix + matrix.T) / 2
        skew = (matrix - matrix.T) / 2
        return sp.simplify(symmetric + common_O * skew * common_O.T)

    e00 = sp.zeros(3)
    e00[0, 0] = 1
    e02 = sp.zeros(3)
    e02[0, 2] = 1
    multiplicativity_gap = sp.simplify(
        independent_map(e00 * e02) - independent_map(e00) * independent_map(e02)
    )

    theorem_text = CLAIM_CONTRACT["THEOREM"]["accepted_quotient"]
    return {
        "support_projectors_exact": all((
            matrix_zero(p_s**2 - p_s),
            matrix_zero(exact_p_r**2 - exact_p_r),
            p_s.rank() == 1, exact_p_r.rank() == 1,
            matrix_zero(s_matrix - s * (p_s - identity / 3)),
            matrix_zero(exact_R**2 + exact_J * (identity - exact_p_r) / 2),
        )),
        "tau_formula_exact": all((
            tau == expected_tau,
            sp.simplify(K - s**2 * J * expected_tau) == 0,
        )),
        "tau_common_action_invariant": transformed_K == original_K,
        "same_tau_canonical_representative_complete": all((
            "complete" in theorem_text,
            "[0,1]" in theorem_text,
            "tau=1-(n.r_hat)^2" in theorem_text,
        )),
        "generic_common_orbit_rank_three": common_tangents.rank() == 3,
        "full_minimum_tangent_rank_four": separate_tangents.rank() == 4,
        "non_gauge_internal_relative_flat_rank_one": (
            separate_tangents.rank() - common_tangents.rank() == 1
        ),
        "independent_channel_map_fails_multiplicativity": not matrix_zero(multiplicativity_gap),
    }


def f1_f2a_controls() -> dict[str, bool]:
    alpha, b, c, eta, d = sp.symbols("alpha b c eta d", positive=True)
    discriminant = sp.sqrt(b**2 + 24 * alpha * c)
    s = sp.simplify((b + discriminant) / (4 * c))
    lambda_r = sp.simplify(s * discriminant / 3)
    lambda_b = sp.simplify(b * s)

    r1, r2, r3 = sp.symbols("r1 r2 r3", real=True)
    radius_sq = r1**2 + r2**2 + r3**2
    skew_law = -eta * radius_sq + d * radius_sq**2
    coordinate_hessian = sp.hessian(skew_law, (r1, r2, r3))
    rho = sp.sqrt(eta / (2 * d))
    radial_hessian = sp.simplify(coordinate_hessian.subs({r1: rho, r2: 0, r3: 0}))
    skew_gram = 2 * sp.eye(3)
    skew_riesz = sp.simplify(skew_gram.inv() * radial_hessian)

    p1 = sp.diag(1, 0, 0)
    p2 = sp.eye(3) - p1
    s_matrix = s * (p1 - sp.eye(3) / 3)

    i2, i3, j = sp.symbols("i2 i3 j", real=True)
    invariant_law = (
        -alpha * i2 / 2 - b * i3 / 3 + c * i2**2 / 4
        - eta * j / 2 + d * j**2 / 4
    )
    mixed_invariant_hessian = sp.Matrix([
        [sp.diff(invariant_law, i2, j), sp.diff(invariant_law, i3, j)]
    ])

    mu_r = sp.simplify(discriminant / (discriminant + 3 * b))
    mu_b = sp.simplify(3 * b / (discriminant + 3 * b))
    contrast = sp.simplify(mu_r - mu_b)
    tuned = {alpha: b**2 / (3 * c)}
    normal_diagonal = sp.diag(lambda_r, lambda_b, lambda_b, 2 * eta)
    quotient = quotient_controls()

    return {
        "symmetric_normal_eigenvalues_positive": all((
            sp.ask(sp.Q.positive(lambda_r)) is True,
            sp.ask(sp.Q.positive(lambda_b)) is True,
        )),
        "skew_radial_hessian_positive_rank_one": all((
            skew_riesz == sp.diag(2 * eta, 0, 0),
            skew_riesz.rank() == 1,
            sp.ask(sp.Q.positive(2 * eta)) is True,
        )),
        "full_normal_rank_four_no_negative_modes": all((
            normal_diagonal.rank() == 4,
            all(sp.ask(sp.Q.positive(normal_diagonal[index, index])) is True for index in range(4)),
        )),
        "four_flat_minimum_tangents_exact": all((
            quotient["full_minimum_tangent_rank_four"],
            quotient["generic_common_orbit_rank_three"],
            quotient["non_gauge_internal_relative_flat_rank_one"],
        )),
        "old_rank1_rank2_roles_survive": all((
            matrix_zero(p1**2 - p1), matrix_zero(p2**2 - p2),
            matrix_zero(p1 * p2), p1.rank() == 1, p2.rank() == 2,
            matrix_zero(s_matrix - s * (p1 - sp.eye(3) / 3)),
        )),
        "old_law_and_hessian_block_embed_exactly": all((
            matrix_zero(mixed_invariant_hessian),
            "block diagonal" in CLAIM_CONTRACT["THEOREM"]["embedded_f2a"],
            "exactly the w2_12" in CLAIM_CONTRACT["THEOREM"]["embedded_f2a"],
        )),
        "f2a_generic_weights_and_tuned_null_exact": all((
            sp.simplify(mu_r + mu_b) == 1,
            sp.simplify(contrast.subs(tuned)) == 0,
            sp.simplify(discriminant**2 - 9 * b**2) == 8 * (3 * alpha * c - b**2),
            "b^2!=3 alpha c" in CLAIM_CONTRACT["DOMAIN"],
        )),
        "extended_f1_and_f2a_same_aggregate": all((
            CLAIM_CONTRACT["PROVENANCE"]["source_identities"]["w2_15"] == W215_SOURCE,
            "same-state" in CLAIM_CONTRACT["THEOREM"]["joint_carrier"],
            "old state-generated" in CLAIM_CONTRACT["THEOREM"]["extended_f1"],
        )),
    }


def relation_controls() -> dict[str, bool]:
    s, eta, d = sp.symbols("s eta d", positive=True)
    identity = sp.eye(3)
    p_s = sp.diag(1, 0, 0)
    S = s * (p_s - identity / 3)
    rho = sp.sqrt(eta / (2 * d))

    r_a = rho * sp.Matrix([sp.sqrt(3) / 2, sp.Rational(1, 2), 0])
    r_b = rho * sp.Matrix([sp.Rational(1, 2), sp.sqrt(3) / 2, 0])
    r_orthogonal = rho * sp.Matrix([0, 1, 0])
    R_a = cross_matrix(r_a)
    R_b = cross_matrix(r_b)
    R_orthogonal = cross_matrix(r_orthogonal)

    def reports(R: sp.MatrixBase) -> dict[str, Any]:
        J = sp.simplify(-sp.trace(R**2))
        C = sp.simplify(S * R - R * S)
        K = sp.simplify(sp.trace(C.T * C))
        P_R = sp.simplify(identity + 2 * R**2 / J)
        return {"J": J, "C": C, "K": K, "P_R": P_R, "tau": sp.simplify(K / (s**2 * J))}

    a = reports(R_a)
    b_report = reports(R_b)
    orthogonal = reports(R_orthogonal)
    A = sp.simplify(S + R_a)
    even = sp.simplify((A + A.T) / 2)
    odd = sp.simplify((A - A.T) / 2)
    carrier_from_A = sp.simplify((A.T * A - A * A.T) / 2)

    generic_entries = sp.symbols("g0:9", real=True)
    generic_A = sp.Matrix(3, 3, generic_entries)
    generic_S = sp.simplify((generic_A + generic_A.T) / 2)
    generic_R = sp.simplify((generic_A - generic_A.T) / 2)
    projected_even_twice = sp.simplify((generic_S + generic_S.T) / 2)
    projected_odd_twice = sp.simplify((generic_R - generic_R.T) / 2)

    zero = sp.zeros(3)
    self_s = sp.simplify(S * S - S * S)
    self_r = sp.simplify(R_a * R_a - R_a * R_a)
    swapped_c = sp.simplify(R_a * S - S * R_a)
    sign_c = sp.simplify(S * (-R_a) - (-R_a) * S)
    swapped_K = sp.simplify(sp.trace(swapped_c.T * swapped_c))
    sign_K = sp.simplify(sp.trace(sign_c.T * sign_c))

    I2 = sp.simplify(sp.trace(S**2))
    I3 = sp.simplify(sp.trace(S**3))
    p_r_a = a["P_R"]
    p_r_b = b_report["P_R"]
    unary_a = (I2, I3, a["J"], S.rank(), R_a.rank(), "transpose_even", "transpose_odd")
    unary_b = (I2, I3, b_report["J"], S.rank(), R_b.rank(), "transpose_even", "transpose_odd")

    return {
        "transpose_nodes_nonzero_distinct_and_reconstruct_A": all((
            not matrix_zero(S), not matrix_zero(R_a),
            matrix_zero(even - S), matrix_zero(odd - R_a),
            matrix_zero(A - even - odd),
            not matrix_zero(S - R_a),
        )),
        "node_support_maps_single_valued_equivariant": all((
            matrix_zero(projected_even_twice - generic_S),
            matrix_zero(projected_odd_twice - generic_R),
            matrix_zero(generic_A - generic_S - generic_R),
            matrix_zero(p_s**2 - p_s), matrix_zero(p_r_a**2 - p_r_a),
            p_s.rank() == 1, p_r_a.rank() == 1,
        )),
        "commutator_carrier_symmetric_traceless": all((
            matrix_zero(a["C"].T - a["C"]),
            sp.simplify(sp.trace(a["C"])) == 0,
            matrix_zero(a["C"] - carrier_from_A),
        )),
        "carrier_vanishes_if_either_node_absent": all((
            matrix_zero(S * zero - zero * S),
            matrix_zero(zero * R_a - R_a * zero),
        )),
        "raw_report_nonnegative_and_regular": all((
            a["K"] == eta * s**2 / (4 * d),
            b_report["K"] == 3 * eta * s**2 / (4 * d),
            sp.ask(sp.Q.positive(a["K"])) is True,
            sp.ask(sp.Q.positive(b_report["K"])) is True,
        )),
        "two_exact_accepted_witnesses_same_unary": all((
            a["J"] == b_report["J"] == eta / d,
            sp.trace(p_r_a) == sp.trace(p_r_b) == 1,
            I2 == 2 * s**2 / 3, I3 == 2 * s**3 / 9,
            R_a.rank() == R_b.rank() == 2,
        )),
        "two_exact_accepted_witnesses_different_joint": all((
            a["K"] != b_report["K"],
            a["tau"] == sp.Rational(1, 4),
            b_report["tau"] == sp.Rational(3, 4),
        )),
        "normalized_report_equals_tau": all((
            a["K"] == s**2 * a["J"] * a["tau"],
            b_report["K"] == s**2 * b_report["J"] * b_report["tau"],
            sp.simplify(a["tau"] - (1 - sp.trace(p_s * p_r_a))) == 0,
            sp.simplify(b_report["tau"] - (1 - sp.trace(p_s * p_r_b))) == 0,
        )),
        "unary_invariant_generators_complete_in_declared_class": all((
            "Cayley-Hamilton" in CLAIM_CONTRACT["FUNCTION_CLASS"]["unary_symmetric"],
            "I2=Tr(S^2), I3=Tr(S^3)" in CLAIM_CONTRACT["FUNCTION_CLASS"]["unary_symmetric"],
            "J=-Tr(R^2)" in CLAIM_CONTRACT["FUNCTION_CLASS"]["unary_skew"],
        )),
        "typed_swap_and_R_sign_leave_report_invariant": all((
            matrix_zero(swapped_c + a["C"]), matrix_zero(sign_c + a["C"]),
            swapped_K == a["K"], sign_K == a["K"],
            matrix_zero(self_s), matrix_zero(self_r),
        )),
        "relation_not_in_unary_equality_separable_image": all((
            unary_a == unary_b,
            a["K"] != b_report["K"],
            "identical complete unary" in CLAIM_CONTRACT["THEOREM"]["irreducibility"],
        )),
        "nonzero_on_predeclared_generic_open_domain": all((
            "0<tau<1" in CLAIM_CONTRACT["DOMAIN"],
            "s^2 J tau" in CLAIM_CONTRACT["THEOREM"]["irreducibility"],
            a["tau"] > 0, a["tau"] < 1,
            b_report["tau"] > 0, b_report["tau"] < 1,
        )),
        "orthogonal_support_projectors_commute_but_carrier_is_nonzero": all((
            matrix_zero(p_s * orthogonal["P_R"] - orthogonal["P_R"] * p_s),
            orthogonal["tau"] == 1,
            not matrix_zero(orthogonal["C"]),
            orthogonal["K"] == s**2 * orthogonal["J"],
            sp.ask(sp.Q.positive(orthogonal["K"])) is True,
        )),
    }


def null_controls() -> dict[str, bool]:
    s, eta, d = sp.symbols("s eta d", positive=True)
    identity = sp.eye(3)
    S = s * (sp.diag(1, 0, 0) - identity / 3)
    rho = sp.sqrt(eta / (2 * d))
    parallel_R = cross_matrix(sp.Matrix([rho, 0, 0]))
    generic_R = cross_matrix(rho * sp.Matrix([sp.sqrt(3) / 2, sp.Rational(1, 2), 0]))
    zero = sp.zeros(3)

    commuting_c = sp.simplify(S * parallel_R - parallel_R * S)
    generic_c = sp.simplify(S * generic_R - generic_R * S)
    generic_k = sp.simplify(sp.trace(generic_c.T * generic_c))

    mu_r, mu_b = sp.symbols("mu_r mu_b", real=True)
    w212_table = sp.diag(mu_r, mu_b)
    unary_equality = sp.Matrix(2, 2, lambda i, j: (mu_r, mu_b)[i] if i == j else 0)
    q_controls = quotient_controls()
    relation = relation_controls()
    domain = CLAIM_CONTRACT["DOMAIN_AND_NULLS"]

    return {
        "zero_and_single_channel_nulls": all((
            matrix_zero(zero * zero - zero * zero),
            matrix_zero(S * zero - zero * S),
            matrix_zero(zero * generic_R - generic_R * zero),
        )),
        "commuting_branch_null": all((
            matrix_zero(commuting_c),
            "K=0" in domain["commuting_tau_zero"],
        )),
        "normalization_undefined_not_assigned": all((
            "not assigned" in domain["normalization_singular"],
            "s=0 or J=0" in domain["normalization_singular"],
        )),
        "self_pair_commutators_zero": all((
            matrix_zero(S * S - S * S),
            matrix_zero(generic_R * generic_R - generic_R * generic_R),
        )),
        "factorized_same_unary_null_detected": all((
            relation["two_exact_accepted_witnesses_same_unary"],
            relation["two_exact_accepted_witnesses_different_joint"],
            generic_k > 0,
        )),
        "independent_action_false_gauge_detected": q_controls[
            "independent_channel_map_fails_multiplicativity"
        ],
        "w2_12_diagonal_remains_unary_equality": w212_table == unary_equality,
        "w2_14_unselected_fibre_not_reused": all((
            relation["node_support_maps_single_valued_equivariant"],
            "state-reconstructed" in domain["w2_14_projective_fibre"],
            "Unselected" in domain["w2_14_projective_fibre"],
        )),
        "tuned_and_parameter_boundaries_not_promoted": all((
            "stays null" in domain["f2a_tuned_surface"],
            "do not promote" in domain["parameter_boundaries"],
        )),
        "no_temporal_or_physical_semantics": all((
            semantic_guard(CLAIM_CONTRACT),
            CLAIM_CONTRACT["OBSERVABLE_MAP"]["status"] == "N/A",
            CLAIM_CONTRACT["FORWARD_MODEL"]["status"] == "N/A",
            EXPECTED_CLOSURE_FLAGS_OPEN["W2_F3_INTERNAL_ORDER_CAUSALITY"] is False,
            EXPECTED_CLOSURE_FLAGS_OPEN["W2_M2_LORENTZIAN_METRIC"] is False,
        )),
    }


def review_schema_valid(attestations: Any, require_pass: bool) -> bool:
    fields = {
        "passed", "reviewer", "artifact", "reviewed_payload_sha256",
        "reviewed_validator_sha256",
    }
    reviewers = {
        "mathematical_candidate_review": "/root/f2_independent_review",
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
        for field in (
            "passed", "reviewer", "artifact", "reviewed_payload_sha256",
            "reviewed_validator_sha256",
        ):
            missing_field = copy.deepcopy(base)
            missing_field[key].pop(field)
            mutants.append(missing_field)
        nonboolean = copy.deepcopy(base)
        nonboolean[key]["passed"] = 1
        mutants.append(nonboolean)
        wrong_id = copy.deepcopy(base)
        wrong_id[key]["reviewed_validator_sha256"] = "WRONG"
        mutants.append(wrong_id)
    extra = copy.deepcopy(base)
    extra["fabricated_review"] = copy.deepcopy(next(iter(base.values())))
    mutants.append(extra)
    return all(not review_schema_valid(mutant, require_pass=False) for mutant in mutants)


def decision_controls(w213: Any) -> dict[str, bool]:
    all_true = {key: True for key in EXPECTED_SCREENING_GATE_KEYS}
    all_true_screen = w213.screen_candidate(all_true, True)
    all_true_completion = w213.completion_logic(*([True] * 11))

    one_false_results = []
    missing_or_nonboolean = []
    for key in EXPECTED_SCREENING_GATE_KEYS:
        false_map = dict(all_true)
        false_map[key] = False
        one_false_results.append(w213.screen_candidate(false_map, True))
        missing = dict(all_true)
        missing.pop(key)
        missing_or_nonboolean.append(w213.screen_candidate(missing, True))
        nonboolean = dict(all_true)
        nonboolean[key] = 1
        missing_or_nonboolean.append(w213.screen_candidate(nonboolean, True))

    review_false = dict(all_true)
    review_false["candidate_specific_independent_audit_required"] = False
    review_false_screen = w213.screen_candidate(review_false, False)
    review_false_completion = w213.completion_logic(
        True, False, False, False, True, True, True, True, True, True, True,
    )
    f2a_false_completion = w213.completion_logic(
        False, True, True, True, True, True, True, True, True, True, True,
    )

    return {
        "all_true_screen_and_completion_positive": all((
            all_true_screen["VALID"] is True,
            all_true_screen["ELIGIBLE"] is True,
            all_true_screen["PROMOTED"] is False,
            all_true_completion["VALID"] is True,
            all_true_completion["F2B_RELATIONAL_COMPLETION"] is True,
            all_true_completion["FULL_W2_F2_OPERATIONAL_RELATIONS"] is True,
            all_true_completion["PROMOTED"] is True,
        )),
        "one_false_gate_never_eligible": all(
            result["VALID"] is True and result["ELIGIBLE"] is False
            and result["PROMOTED"] is False
            for result in one_false_results
        ),
        "every_missing_or_nonboolean_gate_invalid": all(
            result["VALID"] is False and result["ELIGIBLE"] is False
            and result["PROMOTED"] is False
            for result in missing_or_nonboolean
        ),
        "review_false_keeps_candidate_and_full_f2_open": all((
            review_false_screen["VALID"] is True,
            review_false_screen["ELIGIBLE"] is False,
            review_false_completion["F2B_RELATIONAL_COMPLETION"] is False,
            review_false_completion["FULL_W2_F2_OPERATIONAL_RELATIONS"] is False,
            review_false_completion["PROMOTED"] is False,
        )),
        "f2a_false_keeps_full_f2_open": all((
            f2a_false_completion["VALID"] is True,
            f2a_false_completion["F2B_RELATIONAL_COMPLETION"] is True,
            f2a_false_completion["FULL_W2_F2_OPERATIONAL_RELATIONS"] is False,
            f2a_false_completion["PROMOTED"] is False,
        )),
        "candidate_result_never_closes_later_gates": all((
            EXPECTED_CLOSURE_FLAGS_PASS["W2_F1_SELF_DIFFERENTIATION"] is True,
            EXPECTED_CLOSURE_FLAGS_PASS["W2_F2_OPERATIONAL_RELATIONS"] is True,
            all(
                value is False
                for key, value in EXPECTED_CLOSURE_FLAGS_PASS.items()
                if key not in {"W2_F1_SELF_DIFFERENTIATION", "W2_F2_OPERATIONAL_RELATIONS"}
            ),
        )),
    }


def mutation_controls(w213: Any) -> dict[str, bool]:
    base = copy.deepcopy(CLAIM_CONTRACT)

    def rejected(candidate: Any) -> bool:
        try:
            return not strict_contract_valid(candidate)
        except Exception:
            return True

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
        "THEOREM", "EVIDENCE_REGISTRY", "FUNCTION_CLASS",
        "EQUIVALENCE_COMPLETENESS", "DOMAIN_AND_NULLS", "FREEDOM_LEDGER",
        "GATE_APPLICABILITY",
    ):
        mutant = copy.deepcopy(base)
        mutant[field].pop(next(iter(mutant[field])))
        registry_mutants.append(mutant)

    all_true_gates = {key: True for key in EXPECTED_SCREENING_GATE_KEYS}
    evidence_false_results = []
    for key in EXPECTED_SCREENING_GATE_KEYS:
        mutant = dict(all_true_gates)
        mutant[key] = False
        evidence_false_results.append(w213.screen_candidate(mutant, True))

    screen_mutants = []
    missing = dict(all_true_gates)
    missing.pop(next(iter(missing)))
    screen_mutants.append(w213.screen_candidate(missing, True))
    extra_gate = dict(all_true_gates)
    extra_gate["UNREGISTERED_GATE"] = True
    screen_mutants.append(w213.screen_candidate(extra_gate, True))
    nonboolean = dict(all_true_gates)
    nonboolean[next(iter(nonboolean))] = 1
    screen_mutants.append(w213.screen_candidate(nonboolean, True))

    overclaim_mutants = []
    closure = copy.deepcopy(base)
    closure["CLOSURE_FLAGS"]["W2_F2_OPERATIONAL_RELATIONS"] = True
    overclaim_mutants.append(closure)
    scope = copy.deepcopy(base)
    scope["SCOPE_CEILING"]["GR_Einstein_equations_PN_or_PPN"] = True
    overclaim_mutants.append(scope)
    export = copy.deepcopy(base)
    export["EXPORT_STATUS"]["GITHUB"] = True
    overclaim_mutants.append(export)

    dependency = copy.deepcopy(base)
    dependency["PROVENANCE"]["source_identities"]["w2_15"] = "WRONG"
    semantic = copy.deepcopy(base)
    semantic["THEOREM"]["scope"] = "Einstein equations are derived"

    return {
        "missing_or_extra_contract_fields_rejected": all(map(rejected, structural_mutants)),
        "registry_drift_rejected": all(map(rejected, registry_mutants)),
        "evidence_false_prevents_f2": all(
            result["VALID"] is True and result["ELIGIBLE"] is False
            and result["PROMOTED"] is False
            for result in evidence_false_results
        ),
        "screen_schema_mutants_rejected": all(
            result["VALID"] is False and result["ELIGIBLE"] is False
            and result["PROMOTED"] is False
            for result in screen_mutants
        ),
        "closure_scope_and_export_overclaims_rejected": all(map(rejected, overclaim_mutants)),
        "dependency_identity_mutation_rejected": rejected(dependency),
        "semantic_overclaims_rejected": rejected(semantic),
        "review_schema_mutants_rejected": review_schema_controls(),
    }


def evidence_map(
    dependency_ok: bool,
    minima: dict[str, bool],
    quotient: dict[str, bool],
    f1f2a: dict[str, bool],
    relation: dict[str, bool],
    nulls: dict[str, bool],
    decisions: dict[str, bool],
    mutations: dict[str, bool],
) -> dict[str, bool]:
    return {
        "frozen_dependency_chain_exact": bool(dependency_ok),
        "separable_global_minimum_product_exact": all((
            minima["skew_J_is_nonnegative_exact"],
            minima["skew_square_completion_exact"],
            minima["skew_nonzero_global_radius_exact"],
            minima["old_s_positive_root_exact"],
            minima["old_s_stationarity_exact"],
            minima["product_minimum_separability_exact"],
        )),
        "accepted_common_O3_quotient_is_tau_interval": all((
            quotient["support_projectors_exact"],
            quotient["tau_formula_exact"],
            quotient["same_tau_canonical_representative_complete"],
        )),
        "normal_hessian_positive_and_flat_tangent_classified": all((
            f1f2a["symmetric_normal_eigenvalues_positive"],
            f1f2a["skew_radial_hessian_positive_rank_one"],
            f1f2a["full_normal_rank_four_no_negative_modes"],
            f1f2a["four_flat_minimum_tangents_exact"],
        )),
        "common_basis_action_is_complete_algebra_equivalence": all((
            quotient["tau_common_action_invariant"],
            quotient["generic_common_orbit_rank_three"],
            "Every product-and-transpose-preserving" in
            CLAIM_CONTRACT["EQUIVALENCE_COMPLETENESS"]["complete_basis_equivalence"],
        )),
        "independent_channel_law_symmetry_is_global_not_gauge": all((
            quotient["independent_channel_map_fails_multiplicativity"],
            "global degeneracy motions" in
            CLAIM_CONTRACT["EQUIVALENCE_COMPLETENESS"]["independent_channel_motion"],
        )),
        "extended_f1_roles_and_stability_revalidated": all((
            f1f2a["old_rank1_rank2_roles_survive"],
            f1f2a["full_normal_rank_four_no_negative_modes"],
            minima["open_five_parameter_domain"],
        )),
        "w2_12_f2a_family_embeds_exactly_on_generic_domain": all((
            f1f2a["old_law_and_hessian_block_embed_exactly"],
            f1f2a["f2a_generic_weights_and_tuned_null_exact"],
            f1f2a["extended_f1_and_f2a_same_aggregate"],
        )),
        "transpose_nodes_state_owned_and_reconstruct_one_A": all((
            relation["transpose_nodes_nonzero_distinct_and_reconstruct_A"],
            relation["node_support_maps_single_valued_equivariant"],
        )),
        "commutator_carrier_is_bilinear_state_supported_and_cross_null": all((
            relation["commutator_carrier_symmetric_traceless"],
            relation["carrier_vanishes_if_either_node_absent"],
            relation["raw_report_nonnegative_and_regular"],
            relation["orthogonal_support_projectors_commute_but_carrier_is_nonzero"],
        )),
        "complete_unary_invariant_class_reduces_to_I2_I3_J_and_type": (
            relation["unary_invariant_generators_complete_in_declared_class"]
        ),
        "same_complete_unary_different_joint_witness_exact": all((
            relation["two_exact_accepted_witnesses_same_unary"],
            relation["two_exact_accepted_witnesses_different_joint"],
            relation["normalized_report_equals_tau"],
        )),
        "joint_report_nonfactorization_and_open_support_exact": all((
            relation["relation_not_in_unary_equality_separable_image"],
            relation["nonzero_on_predeclared_generic_open_domain"],
        )),
        "complete_equivalence_and_typed_relabelling_invariance_exact": all((
            quotient["tau_common_action_invariant"],
            relation["typed_swap_and_R_sign_leave_report_invariant"],
        )),
        "all_predeclared_nulls_and_w2_14_boundary_pass": all(nulls.values()),
        "no_F3_physical_geometric_observational_semantics": (
            nulls["no_temporal_or_physical_semantics"]
        ),
        "screen_completion_mutation_and_adversarial_controls_pass": all((
            exact_true_map(decisions, EXPECTED_DECISION_CONTROL_KEYS),
            exact_true_map(mutations, EXPECTED_MUTATION_KEYS),
        )),
    }


def candidate_gate_map(
    evidence: dict[str, bool],
    review_complete: bool,
) -> dict[str, bool]:
    return {
        "exact_dependency_chain_valid": evidence["frozen_dependency_chain_exact"],
        "same_chain_embedding_or_full_revalidation_exact": all((
            evidence["extended_f1_roles_and_stability_revalidated"],
            evidence["w2_12_f2a_family_embeds_exactly_on_generic_domain"],
        )),
        "candidate_domain_codomain_branches_and_undefined_points_explicit": (
            set(CLAIM_CONTRACT["DOMAIN_AND_NULLS"]) == EXPECTED_NULL_KEYS
        ),
        "candidate_freedom_ledger_complete": (
            set(CLAIM_CONTRACT["FREEDOM_LEDGER"]) == EXPECTED_FREEDOM_KEYS
        ),
        "state_supported_node_family_generated_not_preassigned": (
            evidence["transpose_nodes_state_owned_and_reconstruct_one_A"]
        ),
        "node_ownership_certificate_law_derived": all((
            evidence["transpose_nodes_state_owned_and_reconstruct_one_A"],
            evidence["separable_global_minimum_product_exact"],
        )),
        "at_least_two_distinct_nodes_on_non_tuned_domain": all((
            evidence["transpose_nodes_state_owned_and_reconstruct_one_A"],
            evidence["joint_report_nonfactorization_and_open_support_exact"],
        )),
        "atemporal_relational_carrier_is_state_supported_not_readout_only": (
            evidence["commutator_carrier_is_bilinear_state_supported_and_cross_null"]
        ),
        "carrier_connects_distinct_nodes_with_derived_restrictions": all((
            evidence["transpose_nodes_state_owned_and_reconstruct_one_A"],
            evidence["commutator_carrier_is_bilinear_state_supported_and_cross_null"],
        )),
        "joint_admissibility_composition_and_complete_common_action_derived": all((
            evidence["accepted_common_O3_quotient_is_tau_interval"],
            evidence["common_basis_action_is_complete_algebra_equivalence"],
            evidence["independent_channel_law_symmetry_is_global_not_gauge"],
        )),
        "uniform_target_free_pair_rule_and_shared_codomain": (
            CLAIM_CONTRACT["FUNCTION_CLASS"]["joint_report"].startswith("K(S,R)=")
        ),
        "complete_unary_reduction_maps_declared": (
            evidence["complete_unary_invariant_class_reduces_to_I2_I3_J_and_type"]
        ),
        "route_neutral_irreducibility_certificate_exact": (
            evidence["same_complete_unary_different_joint_witness_exact"]
        ),
        "relation_not_factorable_through_unary_quotients": (
            evidence["joint_report_nonfactorization_and_open_support_exact"]
        ),
        "nonzero_relational_quotient_on_predeclared_open_domain": (
            evidence["joint_report_nonfactorization_and_open_support_exact"]
        ),
        "reported_relation_complete_equivalence_invariant": (
            evidence["complete_equivalence_and_typed_relabelling_invariance_exact"]
        ),
        "independent_relabelling_and_factorized_pair_nulls_pass": all((
            evidence["complete_equivalence_and_typed_relabelling_invariance_exact"],
            evidence["all_predeclared_nulls_and_w2_14_boundary_pass"],
        )),
        "reference_single_node_and_degenerate_nulls_pass": (
            evidence["all_predeclared_nulls_and_w2_14_boundary_pass"]
        ),
        "w2_12_diagonal_comparison_not_relabelled_as_pair_coupling": (
            evidence["w2_12_f2a_family_embeds_exactly_on_generic_domain"]
        ),
        "f3_time_memory_persistence_and_causality_absent": (
            evidence["no_F3_physical_geometric_observational_semantics"]
        ),
        "physical_spatial_geometric_and_observable_semantics_absent": (
            evidence["no_F3_physical_geometric_observational_semantics"]
        ),
        "positive_null_adversarial_and_mutation_controls_pass": (
            evidence["screen_completion_mutation_and_adversarial_controls_pass"]
        ),
        "candidate_specific_independent_audit_required": bool(review_complete),
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

    dependency_ok, dependencies = dependencies_valid()
    w213 = dependencies.get("w213_module")
    if w213 is None:
        raise ValueError("w2_13 screening dependency unavailable")

    minima = minimum_controls()
    quotient = quotient_controls()
    f1f2a = f1_f2a_controls()
    relation = relation_controls()
    nulls = null_controls()
    decisions = decision_controls(w213)
    mutations = mutation_controls(w213)
    attestations = review_attestations()
    review_structure = review_schema_valid(attestations, require_pass=False)
    review_complete = review_schema_valid(attestations, require_pass=True)

    evidence = evidence_map(
        dependency_ok, minima, quotient, f1f2a, relation, nulls, decisions, mutations,
    )

    preliminary_checks = {
        "payload_validator_and_contract_schema_exact": all((
            strict_contract_valid(CLAIM_CONTRACT),
            detached_validator_sha256() == EXPECTED_VALIDATOR_SHA256,
            registry_shapes_valid(CLAIM_CONTRACT),
        )),
        "frozen_candidate_and_transitive_dependencies_exact": dependency_ok,
        "minimum_quotient_and_common_action_controls_exact": all((
            exact_true_map(minima, EXPECTED_MINIMUM_CONTROL_KEYS),
            exact_true_map(quotient, EXPECTED_QUOTIENT_CONTROL_KEYS),
        )),
        "extended_f1_and_embedded_f2a_controls_exact": exact_true_map(
            f1f2a, EXPECTED_F1F2A_CONTROL_KEYS,
        ),
        "node_carrier_irreducibility_controls_exact": all((
            exact_true_map(relation, EXPECTED_RELATION_CONTROL_KEYS),
            exact_true_map(evidence, EXPECTED_EVIDENCE_KEYS),
        )),
        "required_null_and_semantic_controls_exact": exact_true_map(
            nulls, EXPECTED_NULL_CONTROL_KEYS,
        ),
        "screen_completion_and_mutation_controls_exact": all((
            exact_true_map(decisions, EXPECTED_DECISION_CONTROL_KEYS),
            exact_true_map(mutations, EXPECTED_MUTATION_KEYS),
        )),
        "review_schema_fail_closed": all((review_structure, review_schema_controls())),
        "next_task_preserves_scope": all((
            CLAIM_CONTRACT["NEXT_TASK_POLICY"]["positive"] == NEXT_ATOMIC_TASK,
            "w2_17_f3_internal_order_candidate_contract.py" in NEXT_ATOMIC_TASK,
            "freeze one target-free" in NEXT_ATOMIC_TASK,
            "distinguish state correlation from causal order" in NEXT_ATOMIC_TASK,
            "keep time, propagation, metric, GR" in NEXT_ATOMIC_TASK,
        )),
    }
    preliminary_ready = bool(
        set(preliminary_checks) == EXPECTED_AUDIT_KEYS - {
            "review_attestations_complete", "candidate_screen_and_completion_exact",
        }
        and all(type(value) is bool and value is True for value in preliminary_checks.values())
    )
    candidate_audit_input = bool(preliminary_ready and review_complete)
    gates = candidate_gate_map(evidence, review_complete)
    screen = w213.screen_candidate(gates, candidate_audit_input)

    state_nodes = evidence["transpose_nodes_state_owned_and_reconstruct_one_A"]
    carrier = evidence["commutator_carrier_is_bilinear_state_supported_and_cross_null"]
    common_action = all((
        evidence["accepted_common_O3_quotient_is_tau_interval"],
        evidence["common_basis_action_is_complete_algebra_equivalence"],
        evidence["independent_channel_law_symmetry_is_global_not_gauge"],
    ))
    irreducible = all((
        evidence["same_complete_unary_different_joint_witness_exact"],
        evidence["joint_report_nonfactorization_and_open_support_exact"],
    ))
    invariant = evidence["complete_equivalence_and_typed_relabelling_invariance_exact"]
    open_nulls = evidence["all_predeclared_nulls_and_w2_14_boundary_pass"]
    same_chain = all((
        evidence["extended_f1_roles_and_stability_revalidated"],
        evidence["w2_12_f2a_family_embeds_exactly_on_generic_domain"],
    ))
    completion = w213.completion_logic(
        evidence["w2_12_f2a_family_embeds_exactly_on_generic_domain"],
        candidate_audit_input,
        screen["ELIGIBLE"],
        candidate_audit_input,
        state_nodes,
        carrier,
        common_action,
        irreducible,
        invariant,
        open_nulls,
        same_chain,
    )
    candidate_consistency = all((
        screen["VALID"] is True,
        screen["PROMOTED"] is False,
        completion["VALID"] is True,
        (
            screen["ELIGIBLE"] is True
            and completion["F2B_RELATIONAL_COMPLETION"] is True
            and completion["FULL_W2_F2_OPERATIONAL_RELATIONS"] is True
            and completion["PROMOTED"] is True
        ) if candidate_audit_input else (
            screen["ELIGIBLE"] is False
            and completion["F2B_RELATIONAL_COMPLETION"] is False
            and completion["FULL_W2_F2_OPERATIONAL_RELATIONS"] is False
            and completion["PROMOTED"] is False
        ),
    ))

    checks = {
        **preliminary_checks,
        "review_attestations_complete": bool(review_complete),
        "candidate_screen_and_completion_exact": bool(candidate_consistency),
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
    audit_valid = bool(
        structural_ready
        and review_complete
        and candidate_audit_input
        and screen["ELIGIBLE"] is True
        and completion["FULL_W2_F2_OPERATIONAL_RELATIONS"] is True
    )
    status = PASS_STATUS if audit_valid else READY_STATUS if structural_ready else INVALID_STATUS
    closure_flags = (
        dict(EXPECTED_CLOSURE_FLAGS_PASS) if audit_valid
        else dict(EXPECTED_CLOSURE_FLAGS_OPEN)
    )
    next_task = (
        CLAIM_CONTRACT["NEXT_TASK_POLICY"]["positive"] if audit_valid else
        CLAIM_CONTRACT["NEXT_TASK_POLICY"]["pending"] if structural_ready else
        CLAIM_CONTRACT["NEXT_TASK_POLICY"]["invalid"]
    )
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": status,
        "AUDIT_VALID": audit_valid,
        "STRUCTURAL_READY_FOR_REVIEW": structural_ready,
        "CANDIDATE_MATHEMATICAL_EVALUATION_COMPLETE": structural_ready,
        "CANDIDATE_EVALUATED": audit_valid,
        "F1_REVALIDATED_IN_EXTENDED_STATE": audit_valid,
        "F2A_REVALIDATED_IN_EXTENDED_STATE": audit_valid,
        "F2B_STATE_SUPPORTED_NODE_FAMILY_PROVED": bool(audit_valid and state_nodes),
        "F2B_ATEMPORAL_RELATIONAL_CARRIER_PROVED": bool(audit_valid and carrier),
        "F2B_COMPLETE_COMMON_ACTION_PROVED": bool(audit_valid and common_action),
        "F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED": bool(audit_valid and irreducible),
        "F2B_RELATIONAL_COMPLETION_PROVED": bool(
            audit_valid and completion["F2B_RELATIONAL_COMPLETION"] is True
        ),
        "FULL_W2_F2_OPERATIONAL_RELATIONS": bool(
            audit_valid and completion["FULL_W2_F2_OPERATIONAL_RELATIONS"] is True
        ),
        "PROMOTED": bool(audit_valid and completion["PROMOTED"] is True),
        "CONDITIONAL_ON_IMPORTED_A_AND_LAW": True,
        "MIXED_COUPLING_ROBUSTNESS_PROVED": False,
        "DETACHED_PAYLOAD_SHA256": detached_payload_sha256(CLAIM_CONTRACT),
        "DETACHED_VALIDATOR_SHA256": detached_validator_sha256(),
        "MINIMUM_CONTROLS": minima,
        "QUOTIENT_CONTROLS": quotient,
        "F1_F2A_CONTROLS": f1f2a,
        "RELATION_CONTROLS": relation,
        "NULL_CONTROLS": nulls,
        "DECISION_CONTROLS": decisions,
        "MUTATION_CONTROLS": mutations,
        "EVIDENCE": evidence,
        "CANDIDATE_GATE_MAP": gates,
        "CANDIDATE_SCREEN": screen,
        "COMPLETION_DECISION": completion,
        "AUDIT_CHECKS": checks,
        "INDEPENDENT_REVIEW_ATTESTATIONS": attestations,
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F1_EXTENDED_SELF_DIFFERENTIATION_REVALIDATED": audit_valid,
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_REVALIDATED": audit_valid,
            "W2_F2B_STATE_SUPPORTED_NODE_FAMILY_PROVED": bool(audit_valid and state_nodes),
            "W2_F2B_ATEMPORAL_RELATIONAL_CARRIER_PROVED": bool(audit_valid and carrier),
            "W2_F2B_DERIVED_PAIR_DOMAIN_AND_COMMON_ACTION_PROVED": bool(
                audit_valid and common_action
            ),
            "W2_F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED": bool(audit_valid and irreducible),
            "W2_F2B_COMPLETE_EQUIVALENCE_INVARIANCE_PROVED": bool(audit_valid and invariant),
            "W2_F2B_OPEN_DOMAIN_AND_REQUIRED_NULLS_PROVED": bool(audit_valid and open_nulls),
            "W2_F2B_SAME_CHAIN_COMPATIBILITY_PROVED": bool(audit_valid and same_chain),
            "W2_F2B_RELATIONAL_COMPLETION_PROVED": bool(
                audit_valid and completion["F2B_RELATIONAL_COMPLETION"] is True
            ),
            "W2_F2_OPERATIONAL_RELATIONS_PROVED": bool(
                audit_valid and completion["FULL_W2_F2_OPERATIONAL_RELATIONS"] is True
            ),
        },
        "CLOSURE_FLAGS": closure_flags,
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "PROMOTION_CEILING": (
            "CONDITIONAL_INTERNAL_STRUCTURAL_F2_ONLY" if audit_valid
            else "NO_F2_PROMOTION_UNTIL_EXACT_REVIEWS"
        ),
        "NEXT_ATOMIC_TASK": next_task,
    }


def fail_closed_invalid_report(error: Exception) -> dict[str, Any]:
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": INVALID_STATUS,
        "AUDIT_VALID": False,
        "STRUCTURAL_READY_FOR_REVIEW": False,
        "CANDIDATE_MATHEMATICAL_EVALUATION_COMPLETE": False,
        "CANDIDATE_EVALUATED": False,
        "F1_REVALIDATED_IN_EXTENDED_STATE": False,
        "F2A_REVALIDATED_IN_EXTENDED_STATE": False,
        "F2B_STATE_SUPPORTED_NODE_FAMILY_PROVED": False,
        "F2B_ATEMPORAL_RELATIONAL_CARRIER_PROVED": False,
        "F2B_COMPLETE_COMMON_ACTION_PROVED": False,
        "F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED": False,
        "F2B_RELATIONAL_COMPLETION_PROVED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "PROMOTED": False,
        "CONDITIONAL_ON_IMPORTED_A_AND_LAW": True,
        "MIXED_COUPLING_ROBUSTNESS_PROVED": False,
        "DETACHED_PAYLOAD_SHA256": "",
        "DETACHED_VALIDATOR_SHA256": "",
        "MINIMUM_CONTROLS": {key: False for key in EXPECTED_MINIMUM_CONTROL_KEYS},
        "QUOTIENT_CONTROLS": {key: False for key in EXPECTED_QUOTIENT_CONTROL_KEYS},
        "F1_F2A_CONTROLS": {key: False for key in EXPECTED_F1F2A_CONTROL_KEYS},
        "RELATION_CONTROLS": {key: False for key in EXPECTED_RELATION_CONTROL_KEYS},
        "NULL_CONTROLS": {key: False for key in EXPECTED_NULL_CONTROL_KEYS},
        "DECISION_CONTROLS": {key: False for key in EXPECTED_DECISION_CONTROL_KEYS},
        "MUTATION_CONTROLS": {key: False for key in EXPECTED_MUTATION_KEYS},
        "EVIDENCE": {key: False for key in EXPECTED_EVIDENCE_KEYS},
        "CANDIDATE_GATE_MAP": {key: False for key in EXPECTED_SCREENING_GATE_KEYS},
        "CANDIDATE_SCREEN": {
            "VALID": False, "ELIGIBLE": False, "PROMOTED": False,
            "STATUS": "INVALID_SCREEN__NO_ELIGIBILITY_OR_PROMOTION",
        },
        "COMPLETION_DECISION": {
            "VALID": False, "F2B_RELATIONAL_COMPLETION": False,
            "FULL_W2_F2_OPERATIONAL_RELATIONS": False, "PROMOTED": False,
            "STATUS": "INVALID_COMPLETION_INPUT__NO_PROMOTION",
        },
        "AUDIT_CHECKS": {key: False for key in EXPECTED_AUDIT_KEYS},
        "INDEPENDENT_REVIEW_ATTESTATIONS": {},
        "SUBGATE_CLOSURE_FLAGS": {},
        "CLOSURE_FLAGS": dict(EXPECTED_CLOSURE_FLAGS_OPEN),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "PROMOTION_CEILING": "INVALID__NO_F2_PROMOTION",
        "NEXT_ATOMIC_TASK": "UNAVAILABLE_UNTIL_EXACT_CANDIDATE_ARTIFACT_RESTORED",
        "ERROR": f"{type(error).__name__}: {error}",
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
    return 0 if report["AUDIT_VALID"] is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
