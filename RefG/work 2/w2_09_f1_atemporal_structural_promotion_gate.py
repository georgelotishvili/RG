"""Physical W2-F1 adjudication of the frozen w2_06 atemporal candidate.

The route-neutral meaning and every promotion condition come from frozen
w2_08.  This file applies them to the byte-exact w2_06 candidate; it neither
changes that candidate nor derives its imported law.  A PASS means only
structural self-differentiation relative to the declared foundation
primitives.  F2, time, modes, geometry, action, GR and observations remain
open.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


MODEL_VERSION = "W2-F1-ATEMPORAL-STRUCTURAL-PROMOTION-v1.0-internal"
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"
PROMOTION_CONTRACT_VERSION = "W2-F1-PHYSICAL-PROMOTION-CONTRACT-v1.0-internal"
ROUTER_VERSION = "W2-F1-ROUTE-TAXONOMY-v2.0-internal"
CANDIDATE_ID = "W2_F1_ATEMPORAL_SPECTRAL_SPLIT_CANDIDATE_001"
ROUTE_CLASS = "atemporal_intrastate_invariant_role_structure"
WITNESS_KIND = "INTRA_CLASS_CANONICAL_ROLES"
STABILITY_KIND = "ATEMPORAL_VARIATIONAL_STRUCTURAL"
LAW_ORIGIN_STATUS = "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED"

UNIVERSAL_GATES = frozenset({
    "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
    "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
    "G7_OBSERVATION", "G8_EXPORT",
})

REQUIRED_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "GATE_APPLICABILITY", "CROSSCHECK", "PROVENANCE", "FILES",
})

REQUIRED_CUSTOM_FIELDS = frozenset({
    "PROMOTION_CONTRACT_VERSION", "ROUTER_VERSION", "WITNESS_KIND",
    "STABILITY_KIND", "LAW_ORIGIN_STATUS", "FROZEN_PROMOTION_GATES",
    "CANDIDATE_EVIDENCE_REQUIREMENTS", "NORMALIZED_IMPORT_OWNERSHIP",
    "INVARIANT_LAW_LEDGER", "OVERLAY_OBLIGATION_MAP",
    "OUTPUT_CLASSIFICATION", "SCOPE_FIREWALL", "DEFERRED_OUTPUTS",
    "PROMOTION_POLICY", "KNOWN_LIMITATIONS", "SEMANTIC_ADJUDICATION_PROFILE",
    "NEXT_ATOMIC_TASK",
})

FROZEN_PROMOTION_GATES = {
    "f1_definition_frozen_route_neutral": "definition contains no candidate-specific rank, dimension or target",
    "witness_kind_frozen_before_evaluation": "INTER_CLASS or INTRA_CLASS is fixed before candidate scoring",
    "live_identity_and_dependencies_exact": "candidate and dependency bytes/statuses are exact",
    "complete_one_foundation_primitive_freedom_registry": "every primitive, rule, parameter and import is declared",
    "forbidden_target_intersection_empty": "no F2+, spacetime, GR, observation or desired role is an input",
    "undifferentiated_reference_trivial": "reference/input has no nontrivial canonical role witness",
    "target_free_law_certified": "law/operator class and same-order invariant ledger were frozen target-free",
    "complete_output_classification": "all accepted global output classes and excluded branches are classified",
    "intrinsic_differentiation_certified": "nontrivial output-generated role/outcome witness exists",
    "inequivalence_survives_full_quotient": "claimed difference survives every declared equivalence",
    "law_relevance_not_arbitrary_decomposition": "law forces the witness pattern rather than merely permitting a basis split",
    "realization_or_selection_noncircular": "seed, measure, outcome or atemporal selection account is complete",
    "open_domain_stability_and_robustness": "witness is stable on nonzero declared support, not one tuned point",
    "foundation_admissibility_and_import_health": "imports are honest and are not future-geometry laundering",
    "router_extension_aligned": "candidate satisfies one exact versioned route-class contract",
    "independent_crosscheck_and_controls": "independent proof plus positive, null and target-preload controls pass",
    "candidate_falsifier_absent": "the candidate's predeclared strict falsifier is not realized",
    "f1_only_scope_honest": "no temporal, operational, spacetime, action, observable or GR conclusion is inherited",
}

CANDIDATE_EVIDENCE_REQUIREMENTS = {
    "f1_definition_frozen_route_neutral": (
        "byte-exact w2_08 definition and route-neutral registry pass"
    ),
    "witness_kind_frozen_before_evaluation": (
        "w2_08 preclassifies exact w2_06 as INTRA_CLASS before this audit"
    ),
    "live_identity_and_dependencies_exact": (
        "direct SHA-256 plus reexecuted w2_06 and w2_08 reports are exact"
    ),
    "complete_one_foundation_primitive_freedom_registry": (
        "w2_06 primitive/freedom/import fields plus normalized predeclared functional ownership are complete"
    ),
    "forbidden_target_intersection_empty": (
        "no preferred direction, target projector/orbit, downstream meaning, data or GR input"
    ),
    "undifferentiated_reference_trivial": (
        "Q=0 generates only scalar idempotents 0 and identity"
    ),
    "target_free_law_certified": (
        "complete degree<=4 O(3)-invariant ledger is I2, I3 and I2^2; no target-distance term"
    ),
    "complete_output_classification": (
        "global orbit, stationary branches, boundaries, nulls and forbidden-source branch are classified"
    ),
    "intrinsic_differentiation_certified": (
        "P1 and P2 are polynomial functions of selected Q and absent canonically at Q=0"
    ),
    "inequivalence_survives_full_quotient": (
        "rank/trace 1 versus 2 survives declared O(3) conjugation; Q-sign exchange is not gauge"
    ),
    "law_relevance_not_arbitrary_decomposition": (
        "every accepted nonzero minimum is forced to the uniaxial two-root orbit"
    ),
    "realization_or_selection_noncircular": (
        "uniform imported global-argmin law selects one quotient class with no seed, representative or tie-break"
    ),
    "open_domain_stability_and_robustness": (
        "alpha,b,c>0 is open and the complete declared orbit-normal Hessian is positive"
    ),
    "foundation_admissibility_and_import_health": (
        "all imports remain explicit primitives with strictly internal meanings and zero downstream credit"
    ),
    "router_extension_aligned": (
        "all imports and must-derive fields of the exact v2 overlay class are witnessed"
    ),
    "independent_crosscheck_and_controls": (
        "global discriminant, component Hessian and independent Cayley-Hamilton audits agree; mutants fail"
    ),
    "candidate_falsifier_absent": (
        "no lower state and no non-gauge nonpositive normal direction exists in the declared domain"
    ),
    "f1_only_scope_honest": (
        "F2, temporal, mode, geometry, action, GR, observable and export flags stay false"
    ),
}

# The ninth entry is not a new assumption.  It normalizes the functional that
# the frozen w2_06 primitive registry already explicitly calls imported, but
# whose short IMPORTED_NOT_DERIVED list names only its ingredients.
NORMALIZED_IMPORT_OWNERSHIP = {
    "single_internal_carrier_Q": {
        "origin": LAW_ORIGIN_STATUS,
        "declared_at": "w2_06 IMPORTED_NOT_DERIVED and primitive registry item 1",
        "allowed_meaning": "one abstract internal carrier",
        "forbidden_inference": "particle, node, location or material object",
    },
    "Sym0_3_R_internal_configuration_space": {
        "origin": LAW_ORIGIN_STATUS,
        "declared_at": "w2_06 IMPORTED_NOT_DERIVED and primitive registry items 1/10",
        "allowed_meaning": "finite internal trial state space",
        "forbidden_inference": "physical three-space, 3+1 dimension or continuum",
    },
    "positive_definite_internal_delta_and_transpose": {
        "origin": LAW_ORIGIN_STATUS,
        "declared_at": "w2_06 IMPORTED_NOT_DERIVED and primitive registry items 2/10",
        "allowed_meaning": "internal algebraic contraction",
        "forbidden_inference": "spacetime or spatial metric",
    },
    "matrix_product_and_Tr_alg": {
        "origin": LAW_ORIGIN_STATUS,
        "declared_at": "w2_06 IMPORTED_NOT_DERIVED and primitive registry items 2/10",
        "allowed_meaning": "internal matrix/Jordan-algebra bookkeeping",
        "forbidden_inference": "persistent trace, physical propagation or observable",
    },
    "O3_internal_conjugation_relabel_equivalence": {
        "origin": LAW_ORIGIN_STATUS,
        "declared_at": "w2_06 IMPORTED_NOT_DERIVED and primitive registry items 3/10",
        "allowed_meaning": "complete declared internal relabel equivalence",
        "forbidden_inference": "physical rotation group or spacetime isotropy",
    },
    "absence_of_Q_sign_relabel_symmetry": {
        "origin": LAW_ORIGIN_STATUS,
        "declared_at": "w2_06 IMPORTED_NOT_DERIVED and primitive registry items 3/10",
        "allowed_meaning": "declared internal polarity choice",
        "forbidden_inference": "charge, arrow of time or observed polarity",
    },
    "atemporal_global_argmin_rule": {
        "origin": LAW_ORIGIN_STATUS,
        "declared_at": "w2_06 IMPORTED_NOT_DERIVED and primitive registry items 4/10",
        "allowed_meaning": "uniform atemporal admissibility law",
        "forbidden_inference": "temporal relaxation, dynamics or deeper law derivation",
    },
    "positive_open_parameter_domain_alpha_b_c": {
        "origin": LAW_ORIGIN_STATUS,
        "declared_at": "w2_06 IMPORTED_NOT_DERIVED, freedom ledger and primitive item 5",
        "allowed_meaning": "one open model domain with zero data fit",
        "forbidden_inference": "observational calibration or unique constants",
    },
    "quartic_invariant_functional_form_signs_and_truncation": {
        "origin": LAW_ORIGIN_STATUS,
        "declared_at": "w2_06 frozen CLAIM, primitive registry items 4/10 and METHOD",
        "allowed_meaning": "fixed complete O(3)-invariant polynomial through degree four",
        "forbidden_inference": "derived fundamental law, unique law or target-orbit distance",
    },
}

INVARIANT_LAW_LEDGER = {
    "carrier": "one Q in Sym_0(3,R)",
    "declared_equivalence": "Q equivalent to R Q R^T for every R in O(3)",
    "trace_constraint": "Tr_alg(Q)=0 removes the degree-one invariant",
    "invariant_ring_generators": ["I2=Tr_alg(Q^2)", "I3=Tr_alg(Q^3)"],
    "invariant_ring_theorem": (
        "real-symmetric spectral theorem plus the fundamental theorem of symmetric "
        "polynomials with e1=Tr(Q)=0"
    ),
    "invariant_ring_theorem_status": "STANDARD_EXACT_MATHEMATICAL_THEOREM__NOT_A_PHYSICAL_PRIMITIVE",
    "nonconstant_terms_through_degree_four": ["I2", "I3", "I2^2"],
    "dependent_degree_four_identity": "Tr_alg(Q^4)=I2^2/2",
    "frozen_functional": "V=-alpha I2/2-b I3/3+c I2^2/4",
    "coefficient_domain": "alpha>0, b>0, c>0",
    "irrelevant_constant": "additive constant omitted because argmin is unchanged",
    "forbidden_terms_absent": [
        "preferred basis or direction", "target projector or rank",
        "target spectrum/orbit distance", "post-output term", "hidden tie-break",
        "spacetime, GR, observable or data term",
    ],
    "origin_status": LAW_ORIGIN_STATUS,
}

OUTPUT_CLASSIFICATION = {
    "alpha_b_c_positive": "UNIQUE_NONZERO_GLOBAL_MINIMUM_QUOTIENT_CLASS_WITH_CANONICAL_1_PLUS_2_ROLES",
    "Q_zero": "STATIONARY_STRICT_VARIATIONAL_MAXIMUM__NO_CANONICAL_NONTRIVIAL_ROLE",
    "negative_stationary_root": "HIGHER_ENERGY_AND_NEGATIVE_BIAXIAL_DIRECTION__NOT_ACCEPTED",
    "O3_orientation_orbit": "DECLARED_RELABEL_EQUIVALENT__NO_REPRESENTATIVE_DIRECTION",
    "b_zero_boundary": "DEGENERATE_QUOTIENT__OUTSIDE_STRICT_ROLE_CERTIFICATE",
    "alpha_zero_boundary": "MARGINAL_ORIGIN__OUTSIDE_OPEN_DOMAIN",
    "c_zero_or_negative": "NONCOERCIVE_OR_UNBOUNDED__OUTSIDE_DOMAIN",
    "b_negative": "POLARITY_MIRROR__OUTSIDE_FROZEN_POSITIVE_DOMAIN",
    "positive_quadratic_null": "UNDIFFERENTIATED_STABLE_ORIGIN_ONLY",
    "N_one": "TRACLESS_STATE_SPACE_TRIVIAL",
    "N_two": "EQUAL_RANK_SECTORS__DOES_NOT_WITNESS_THIS_ROUTE",
    "N_four_and_general_N": "CONTROL_ONLY__N3_AND_1_PLUS_2_NOT_DERIVED_OR_UNIVERSAL",
    "explicit_linear_source": "REJECTED_PREFERRED_DIRECTION_PREWIRING",
    "invariant_target_orbit_distance": "REJECTED_TARGET_PREWIRING",
}

OVERLAY_OBLIGATION_MAP = {
    "complete_selected_quotient_classification": [
        "complete_output_classification", "realization_or_selection_noncircular",
    ],
    "canonical_state_generated_coexisting_roles": ["intrinsic_differentiation_certified"],
    "intrinsic_role_invariant": [
        "intrinsic_differentiation_certified", "inequivalence_survives_full_quotient",
    ],
    "nonexchangeability_after_full_quotient": ["inequivalence_survives_full_quotient"],
    "law_relevance_not_arbitrary_decomposition": ["law_relevance_not_arbitrary_decomposition"],
    "open_domain_structural_stability": ["open_domain_stability_and_robustness"],
    "no_representative_orientation_or_role_selection": ["realization_or_selection_noncircular"],
    "noncircular_law_and_foundation_admissibility": [
        "forbidden_target_intersection_empty", "target_free_law_certified",
        "realization_or_selection_noncircular", "foundation_admissibility_and_import_health",
    ],
}

SCOPE_FIREWALL = {
    "physical_node_or_location": False,
    "persistent_physical_imprint": False,
    "operational_relation": False,
    "temporal_formation_or_persistence": False,
    "internal_causal_order_or_clock": False,
    "independent_additive_physical_modes": False,
    "physical_space_dimension_or_continuum": False,
    "Lorentzian_metric_or_light_cone": False,
    "effective_action_or_conservation_law": False,
    "pressure_mass_particle_or_oscillon": False,
    "observable_or_data_map": False,
    "Einstein_GR_PN_PPN_or_compact_source_bridge": False,
}

DEFERRED_OUTPUTS = tuple(SCOPE_FIREWALL)

PROMOTION_POLICY = {
    "numeric_score_used": False,
    "weights_or_compensation_used": False,
    "candidate_specific_F1_definition_used": False,
    "N3_or_rank_signature_priority_bonus_used": False,
    "downstream_target_used": False,
    "preassigned_roles_used": False,
    "gauge_multiplicity_called_physical": False,
    "temporal_claim_from_structural_stability": False,
    "F2_or_later_semantics_claimed": False,
    "imported_law_called_derived_without_gate": False,
    "route_class_laundered": False,
    "fallback_rejected": False,
}

KNOWN_LIMITATIONS = {
    "foundation_law_origin": "OPEN_BEYOND_DECLARED_PRIMITIVE__NOT_REQUIRED_FOR_THIS_RELATIVE_F1_PASS",
    "functional_uniqueness": "NOT_DERIVED__OTHER_FOUNDATION_LAWS_REMAIN_POSSIBLE",
    "N3_origin": "IMPORTED__NO_PHYSICAL_DIMENSION_MEANING",
    "full_equivalence_ceiling": "NONEXCHANGEABILITY_ONLY_UNDER_COMPLETE_DECLARED_O3_RELABEL_RULE",
    "robustness_ceiling": "OPEN_ALPHA_B_C_DOMAIN_WITHIN_FROZEN_QUARTIC_LAW_CLASS",
    "RefG_resonant_environment_map": "OPEN__BELONGS_TO_F2_AND_LATER_BRIDGE",
    "temporal_formation": "OPEN__ATEMPORAL_STRUCTURE_ONLY",
    "observation": "N_A_AT_F1__FINAL_OBSERVATIONAL_VETO_REMAINS",
}

SEMANTIC_ADJUDICATION_PROFILE = {
    "fixed_basis_or_direct_sum_roles_used": False,
    "role_ranks": [1, 2],
    "full_declared_equivalence_can_swap_roles": False,
    "Q_sign_is_gauge": False,
    "law_forces_selected_role_pattern": True,
    "arbitrary_spectral_decomposition_used": False,
    "representative_direction_selected": False,
    "target_orbit_distance_term_used": False,
    "post_output_cubic_or_sign_choice_used": False,
    "parameter_support_is_open": True,
    "unregistered_higher_invariant_added": False,
    "N3_called_physical_space": False,
    "O3_called_physical_rotation": False,
    "delta_called_spacetime_metric": False,
    "Hessian_called_temporal_formation": False,
    "route_obligations_satisfied": True,
    "functional_ownership_complete": True,
}

NEXT_ATOMIC_TASK = (
    "Freeze a route-neutral W2_F2 operational-distinction/relations contract, then test "
    "whether the F1 roles acquire intrinsic readout and relations without importing nodes, "
    "space, time, modes, geometry or GR."
)

EXPECTED_DECISION_BRANCH_KEYS = frozenset({
    "valid_promoted_branch_reachable",
    "valid_not_promoted_branch_reachable",
    "invalid_audit_can_never_export_promotion",
})

EXPECTED_AUDIT_CHECK_KEYS = frozenset({
    "required_contract_and_custom_fields_exact",
    "contract_values_nonempty",
    "contract_and_runtime_model_versions_bound",
    "contract_custom_fields_exactly_bound",
    "whole_claim_contract_digest_and_types_exact",
    "static_contract_scope_freedom_and_flags_exact",
    "claim_method_conditions_falsifier_identity_zero_and_next_task_mutants_rejected",
    "own_critical_registries_digest_bound",
    "source_boundary_phrases_present",
    "dependency_bytes_exact_before_import",
    "w2_06_direct_report_reexecuted_exact",
    "w2_08_contract_report_reexecuted_exact",
    "live_identity_and_transitive_provenance_exact",
    "predeclared_functional_ownership_normalized_without_new_assumption",
    "independent_algebra_audit_schema_and_boolean_outputs_exact",
    "overlay_contract_schema_exact",
    "candidate_fact_registry_schema_and_boolean_outputs_exact",
    "all_18_promotion_evidence_values_are_exact_booleans",
    "three_validators_agree_with_exact_AND_candidate_outcome",
    "every_missing_false_truthy_string_none_and_extra_gate_mutant_rejected",
    "every_policy_true_truthy_falsey_none_missing_and_extra_mutant_rejected",
    "candidate_specific_metadata_mutants_rejected",
    "semantic_target_gauge_temporal_and_downstream_nulls_rejected",
    "import_ownership_mutants_rejected",
    "registry_target_output_scope_and_score_mutants_rejected",
    "promoted_not_promoted_and_invalid_decision_branches_fail_closed",
    "foundation_law_derivation_and_resonant_map_honestly_open",
    "runtime_closure_missing_extra_opposite_and_nonboolean_mutants_rejected",
    "audit_check_keyset_missing_extra_false_and_nonboolean_mutants_rejected",
})

EXPECTED_BRANCHES = {
    "w2_06_exact_candidate": "PROMOTE_ONLY_IF_ALL_18_FROZEN_GATES_ARE_EXACT_TRUE",
    "foundation_imports": "ADMISSIBLE_DECLARED_PRIMITIVES__NOT_DERIVED",
    "old_atemporal_nonunique_class": "DISTINCT_OPEN_ROUTE__NOT_REJECTED",
    "symmetric_seed_route": "OPEN_FALLBACK__NOT_REJECTED",
    "all_other_nonfalsified_routes": "OPEN__NOT_REJECTED",
    "F2_and_later": "OPEN__NO_AUTOMATIC_INHERITANCE",
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
    "F1_PROMOTION_CONTRACT_FROZEN": False,
    "F1_ROUTE_TAXONOMY_V2_FROZEN": False,
    "W2_06_CLASSIFICATION_ALIGNED": False,
    "W2_06_OVERLAY_CLASS_EVALUATED": False,
    "W2_06_OVERLAY_CLASS_SATISFIED": False,
    "W2_06_PROMOTED_TO_W2_F1": False,
    "W2_F1_ATEMPORAL_STRUCTURAL_RELATIVE_TO_FROZEN_PRIMITIVES": False,
    "W2_F1_SELF_DIFFERENTIATION": False,
    "FOUNDATION_LAW_DERIVED": False,
    "REFG_RESONANT_ENVIRONMENT_MAP": False,
    "W2_F2_OPERATIONAL_RELATIONS": False,
    "W2_F3_INTERNAL_ORDER_CAUSALITY": False,
    "W2_F4_INDEPENDENT_ADDITIVE_MODES": False,
    "W2_M1_DIMENSION_CONTINUUM": False,
    "W2_M2_LORENTZIAN_METRIC": False,
    "W2_A0_EFFECTIVE_ACTION_ORIGIN": False,
}

GATE_APPLICABILITY = {
    "G0_GOAL": "REQUIRED — exact w2_06 physical-F1 adjudication and conditional ceiling are frozen",
    "G1_CONVENTIONS": "REQUIRED — w2_08 witness, route, primitive-law and quotient meanings are exact",
    "G2_CORE_ALGEBRA": "REQUIRED — live w2_06 exact algebra plus independent Cayley-Hamilton audit",
    "G3_STRUCTURE": "REQUIRED — all 18 frozen promotion gates and overlay obligations are evaluated",
    "G4_INDEPENDENT_CHECK": "REQUIRED — independent invariant/projector proof and two strict validators",
    "G5_LIMITS_REGRESSION": "REQUIRED — boundaries, general-N, target, gauge, temporal and downstream mutants",
    "G6_PHYSICAL_MATCH": "N/A — F1 has no source, energy ledger or observable readout",
    "G7_OBSERVATION": "N/A — no F1 observable or dataset; observational veto remains downstream",
    "G8_EXPORT": "N/A — internal Git-ignored gate; no Canon or article export authorized",
}

EXPECTED_DEPENDENCY_SHA256 = {
    "CODES": "49d8e818f269621f31016f8ef8decabe000f01c442c45fe7a16c4906b61c1309",
    "CANON": "bf5cabae190821d1c0ffb342d3cdf101f13be5386ea993bb60fce4098f18d756",
    "INTUITIVE": "7e69e62c36c8cc25540e0a0465f3b74300693ca1bd868e54b4b349d5b9547981",
    "W2_C0": "640debaea5265d63a660fed4bacd9a2a99c2152535737003272e178efc1c5b6c",
    "W2_06": "8998aa7ee0dda8e3a882e660486a850d86f8d30a55791e81ff3088b9c9bf4d8b",
    "W2_07": "144822478a3435fdb90cf5854971bcf5e91082d6caf300a7238d218475b77b64",
    "W2_08": "3e56831c1eba7a46d9b396783c091ee57f81c623184041b1d371472e7ede4f58",
}

EXPECTED_REPORT_SHA256 = {
    "W2_06_CHECK_KEYS": "f188d7646a21f92dc85fd372bd768e25b293354c41c04bf4922e696db49b0e96",
    "W2_06_CLOSURE_FLAGS": "0517e29cd20163ee40a57fdb040aed5334773de4adaa1be59cfdc394a1b65566",
    "W2_06_PROVENANCE": "4e5df691191190b41d6a10fc0f38927185b323fd32303aa3f626912a82a036d4",
    "W2_08_CHECK_KEYS": "4c79719a2aba586b962e1509ddee52d8592517856174f1392a3ce805823d6eb6",
    "W2_08_CLOSURE_FLAGS": "ac8634a296b7bc94d6de24568c0c60f4028f209271f98e1c3f97adf7f3a81792",
    "W2_08_PROVENANCE": "5d1bb4ab7479d15d2254d469b32c5f5d4833a4f2424bde0173e428140c5a621f",
}

EXPECTED_REGISTRY_SHA256 = {
    "FROZEN_PROMOTION_GATES": "089d50b51f57d3329e76af479d44b5c91fb525e75fe180e29a7dc9159a753d2b",
    "CANDIDATE_EVIDENCE_REQUIREMENTS": "b20dd3b99cf9bd65cba99ee4fc2edec7c3df4c470473c8fac8bbb3ff163317b4",
    "NORMALIZED_IMPORT_OWNERSHIP": "f5297275eb98803f15f95c3c9495cad6cacadfaaf2558493179f13825d8a1454",
    "INVARIANT_LAW_LEDGER": "616c8424e0f00c7cbec995ac1b41d03f9dbea7bc05b1b568e1fd97eeac0f4756",
    "OUTPUT_CLASSIFICATION": "8ef10a46130b113d4fc00835c373bd3b087576a8f1782b631ea6eaf9a4ebe579",
    "OVERLAY_OBLIGATION_MAP": "e61393837f394959ed492404d4375b481489cae1bf0ea6df46ebc1019da9e23d",
    "SCOPE_FIREWALL": "9e8a03b1470083b26175c2fa2bf28eca68c6b6210b6db37f8f3af66636f293ce",
    "DEFERRED_OUTPUTS": "4c6118ebc57d70e241e6f1a7a2afc5d99128deac90613e77c65e87f625010aeb",
    "PROMOTION_POLICY": "7b3a734c485616e138d2a512d35b8c75877604f625f1c3382fd21703f9dbe4e3",
    "KNOWN_LIMITATIONS": "7ba15b5f4610fce8fe0a0c9265efb9f53956171b5c3742db6f9daf0bdbb3e2cf",
    "SEMANTIC_ADJUDICATION_PROFILE": "1963a717d07c30a938a9a6d1c26d8c2cd5b698511b74e24c366cde6b47cb8fc5",
    "EXPECTED_BRANCHES": "bf1b0c49f9b136093cbce7e908473766f2eaaa4ba1d1d930b9de5c44e5db50f5",
    "INITIAL_CLOSURE_FLAGS": "daf402d7553f0db9ed2ad13b0e71cf997c13c49e2fa2bb90b63f54c25d8c3631",
    "GATE_APPLICABILITY": "554b6cc8f96fbc68c3fd7240cb60b10cb9d9531d37b37b947b01e49d0999eb07",
}


CLAIM_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F1_ATEMPORAL_STRUCTURAL_PROMOTION_001",
    "CLAIM": (
        "ზუსტად გაყინული w2_06 კანდიდატი, მისი გამოცხადებული და გამოუყვანელი "
        "ფუძის პრიმიტივების მიმართ, აკმაყოფილებს w2_08-ის route-neutral F1-ის ყველა "
        "პირობას: ერთი უნიკალური quotient-მდგომარეობა შეიცავს Q-დან კანონიკურად "
        "მიღებულ, თანაარსებულ და სრული გამოცხადებული O(3)-გადაიარლიყების შემდეგაც "
        "არაგაცვლად შიდა როლებს. ეს ხურავს მხოლოდ ატემპორალურ სტრუქტურულ W2_F1-ს."
    ),
    "TYPE": (
        "CONDITIONAL EXACT STRUCTURAL CONSEQUENCE RELATIVE TO DECLARED PRIMITIVES; "
        "atomic W2_F1 PASS; არა MECHANISM_DERIVED, F2, spacetime, GR ან observational PASS"
    ),
    "MODEL_VERSION": (
        f"{MODEL_VERSION}; any candidate byte, promotion gate, witness, law-origin, "
        "import ownership, scope ceiling or PASS logic change requires a new version"
    ),
    "ASSUMPTIONS": [
        "w2_08-ის F1-ის განსაზღვრება და 18-პირობიანი AND-კარიბჭე უცვლელად გამოიყენება.",
        "w2_06-ის Q, Sym_0(3), N=3, შიდა delta, O(3), Q-sign არჩევანი, ფუნქციონალი და argmin-წესი შემოტანილი პრიმიტივებია.",
        "პრიმიტივის უფრო ღრმა კანონიდან გამოუყვანლობა F1-ს არ ბლოკავს, მაგრამ მას derived სტატუსს არ აძლევს.",
        "N=3, O(3), delta და 1+2 მხოლოდ შიდა ნიშნებია და არ ნიშნავს სივრცეს, ბრუნვას, მეტრიკას ან რეჟიმებს.",
        "მდგრადობა არის ატემპორალური ვარიაციული მდგრადობა გამოცხადებულ კვარტიკულ კლასში და არა დროითი ევოლუცია.",
        "დაკვირვებები F1-ში N/A-ა; საუკეთესო დაკვირვებებთან თავსებადობა საბოლოო უცვლელ ვეტოდ რჩება.",
    ],
    "DOMAIN": (
        "ზუსტად w2_06-ის ერთი შიდა Sym_0(3,R) მატარებელი, O(3)-quotient, "
        "V=-alpha I2/2-b I3/3+c I2^2/4 და alpha,b,c>0. არ მოიცავს სხვა N-ს, "
        "უფრო მაღალი რიგის კანონს, დროით დინამიკას, ფიზიკურ სივრცეს ან მონაცემებს."
    ),
    "CONVENTIONS": (
        "ფიზიკური F1 ამ ატომურ პროგრამაში ნიშნავს ფუძის ონტოლოგიაში კანონიკურ "
        "შიდა განსხვავებას და არა გარე გაზომვადობას. სრული quotient ნიშნავს ზუსტად "
        "გამოცხადებულ O(3)-conjugation equivalence-ს. Q->-Q gauge არაა. "
        "IMPORTED_NOT_DERIVED ნიშნავს დასაშვებ საწყის კანონს, არა მის წარმოშობის მტკიცებას."
    ),
    "FREEDOM_LEDGER": {
        "candidate_identity": {
            "source": "byte-exact w2_06", "range": CANDIDATE_ID,
            "scale": "candidate", "complexity": 1,
        },
        "promotion_contract": {
            "source": "byte-exact w2_08", "range": sorted(FROZEN_PROMOTION_GATES),
            "scale": "programme", "complexity": "18 exact booleans; no score",
        },
        "witness_kind": {
            "source": "w2_08 preclassification", "range": WITNESS_KIND,
            "scale": "candidate", "complexity": 1,
        },
        "route_class": {
            "source": "w2_08 taxonomy v2", "range": ROUTE_CLASS,
            "scale": "candidate", "complexity": 1,
        },
        "law_origin_status": {
            "source": "w2_08 primitive-law policy", "range": LAW_ORIGIN_STATUS,
            "scale": "foundation law", "complexity": 1,
        },
        "normalized_imports": {
            "source": "only preexisting frozen w2_06 fields", "range": sorted(NORMALIZED_IMPORT_OWNERSHIP),
            "scale": "candidate", "complexity": len(NORMALIZED_IMPORT_OWNERSHIP),
        },
        "decision_rule": {
            "source": "w2_08", "range": "logical AND of all 18 gates",
            "scale": "decision", "complexity": 1,
        },
        "data_fitted_parameters": {
            "source": "N/A — no data", "range": 0,
            "scale": "data", "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        f"{PROGRAM_CONTRACT}: atomic W2_F1 boundary and observational veto",
        "w2_06 v1.0: exact conditional spectral-split candidate",
        "w2_07 v2.6: priority only; physical F1 left open",
        "w2_08 v1.0: frozen route-neutral promotion contract and taxonomy v2",
    ],
    "METHOD": (
        "Reexecute w2_06 and w2_08; bind exact bytes, statuses, registries and provenance; "
        "normalize only already declared import ownership; independently verify the complete "
        "degree-four invariant ledger and Q-generated projectors; evaluate every frozen gate "
        "as an exact boolean; require agreement of w2_08 and independent validators; reject "
        "all missing, truthy, target-preload, gauge, temporal and downstream mutants."
    ),
    "PASS_CONDITION": [
        "the exact w2_06 and w2_08 dependency chains reexecute with all checks strictly True.",
        "all w2_06 primitives, fixed functional choices, rules, parameters and imports have explicit preexisting ownership.",
        "the complete same-order invariant law contains no target orbit, projector, direction, rank, data or future geometry.",
        "Q=0 has no canonical nontrivial role and every accepted nonzero minimum has Q-generated rank-1/rank-2 roles.",
        "the roles survive the full declared quotient and the law, rather than an arbitrary basis, forces their pattern.",
        "selection is the uniform imported argmin law with no seed, representative direction, target-distance or tie-break.",
        "the witness is exact and stable on the full open alpha,b,c>0 domain of the frozen law class.",
        "all overlay obligations and every one of the 18 frozen promotion gates are exactly True.",
        "both strict validators agree and every predeclared negative/mutation control is rejected.",
        "foundation-law derivation and every F2/later, temporal, geometry, GR, data and export flag remain False."
    ],
    "FAIL_CONDITION": (
        "Any one frozen promotion gate is missing, nonboolean or not True; any primitive or "
        "fixed law choice lacks preexisting declaration; target or downstream semantics leak "
        "into inputs; or either strict validator rejects the candidate."
    ),
    "FALSIFIER": (
        "The frozen w2_06 mathematical claim is falsified by a lower V state or a non-gauge "
        "nonpositive orbit-normal direction in alpha,b,c>0. This promotion is additionally "
        "falsified by an undeclared primitive, a target-preloaded law, a full-equivalence role "
        "swap, or a demonstrated arbitrary rather than law-forced role split."
    ),
    "RESIDUAL": (
        "0 for exact dependency, registry, invariant, projector, quotient, boolean and closure "
        "checks; no physical or observational residual is defined at F1."
    ),
    "ERROR_BOUND": "0 for exact symbolic/discrete checks in the declared finite domain; data N/A.",
    "VALIDITY_HEALTH": (
        "A PASS is conditional on the declared imported foundation law. It neither proves that "
        "this law is unique or deeper-derived nor maps Q/V to RefG's resonant effective environment. "
        "That map and all operational meanings begin at F2 and later gates."
    ),
    "BRANCHES": dict(EXPECTED_BRANCHES),
    "OBSERVABLE_MAP": "N/A — F1 internal roles are not external observables.",
    "FORWARD_MODEL": "N/A — no ideal-observable-to-data chain exists at F1.",
    "DATA_ROLE": "N/A — no data are used for construction, fitting, validation or prediction.",
    "IDENTIFIABILITY": (
        "Internal only: rank/trace distinguish the two canonical roles under declared O(3); "
        "representative orientation is gauge. Physical/observational identifiability is N/A."
    ),
    "BENCHMARK": (
        "Exact w2_06 global/Hessian proofs plus independent Cayley-Hamilton reconstruction; "
        "nulls include trivial origin, equal/gauge roles, b=0, c<=0, target-orbit distance, "
        "fixed basis, Q-sign gauge, tuned point and every temporal/downstream relabel."
    ),
    "CLOSURE_FLAGS": dict(INITIAL_CLOSURE_FLAGS),
    "GATE_APPLICABILITY": dict(GATE_APPLICABILITY),
    "CROSSCHECK": (
        "w2_06's eigenvalue-discriminant and five-coordinate Hessian routes are checked by a "
        "separate Cayley-Hamilton/invariant-ring/projector calculation and two independent strict AND validators."
    ),
    "PROVENANCE": "runtime SHA-256 of source documents and exact w2_06/w2_07/w2_08 files; stdout JSON artifact",
    "FILES": [
        "CODES.md", "Theory_Canon.md", "intuitive/RefG_GE.md",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_06_f1_atemporal_spectral_split_candidate_gate.py",
        "RefG/work 2/w2_07_f1_route_adjudication_gate.py",
        "RefG/work 2/w2_08_f1_physical_promotion_contract.py",
        "RefG/work 2/w2_09_f1_atemporal_structural_promotion_gate.py",
    ],
    "PROMOTION_CONTRACT_VERSION": PROMOTION_CONTRACT_VERSION,
    "ROUTER_VERSION": ROUTER_VERSION,
    "WITNESS_KIND": WITNESS_KIND,
    "STABILITY_KIND": STABILITY_KIND,
    "LAW_ORIGIN_STATUS": LAW_ORIGIN_STATUS,
    "FROZEN_PROMOTION_GATES": copy.deepcopy(FROZEN_PROMOTION_GATES),
    "CANDIDATE_EVIDENCE_REQUIREMENTS": copy.deepcopy(CANDIDATE_EVIDENCE_REQUIREMENTS),
    "NORMALIZED_IMPORT_OWNERSHIP": copy.deepcopy(NORMALIZED_IMPORT_OWNERSHIP),
    "INVARIANT_LAW_LEDGER": copy.deepcopy(INVARIANT_LAW_LEDGER),
    "OVERLAY_OBLIGATION_MAP": copy.deepcopy(OVERLAY_OBLIGATION_MAP),
    "OUTPUT_CLASSIFICATION": copy.deepcopy(OUTPUT_CLASSIFICATION),
    "SCOPE_FIREWALL": dict(SCOPE_FIREWALL),
    "DEFERRED_OUTPUTS": list(DEFERRED_OUTPUTS),
    "PROMOTION_POLICY": dict(PROMOTION_POLICY),
    "KNOWN_LIMITATIONS": dict(KNOWN_LIMITATIONS),
    "SEMANTIC_ADJUDICATION_PROFILE": copy.deepcopy(SEMANTIC_ADJUDICATION_PROFILE),
    "NEXT_ATOMIC_TASK": NEXT_ATOMIC_TASK,
}

# These two independent literal digests bind every standard/custom claim field
# and every freedom-ledger value.  They are filled only after the contract is
# frozen; changing the live dictionaries without a deliberate versioned rebind
# must fail closed.
EXPECTED_CLAIM_CONTRACT_SHA256 = "6c8c6af0bf309035d7d54fa60cb3e69629479ee85d627b2e1a255ecf976f3005"
EXPECTED_FREEDOM_LEDGER_SHA256 = "0082cd91606d79a873526683c8457ba3ffb87b4dac1acad9ff043607b609cf44"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_module(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def value_present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    return value is not None and bool(value)


def exact_literal_map(actual: Any, expected: dict[str, Any]) -> bool:
    return (
        isinstance(actual, dict)
        and set(actual) == set(expected)
        and all(
            type(actual[key]) is type(expected[key]) and actual[key] == expected[key]
            for key in expected
        )
    )


def exact_tree(actual: Any, expected: Any) -> bool:
    """Recursive equality that keeps bool distinct from int."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return (
            set(actual) == set(expected)
            and all(exact_tree(actual[key], expected[key]) for key in expected)
        )
    if isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(
            exact_tree(a_item, e_item)
            for a_item, e_item in zip(actual, expected)
        )
    return actual == expected


def exact_true_map(actual: Any, expected_keys: Any) -> bool:
    return (
        isinstance(actual, dict)
        and set(actual) == set(expected_keys)
        and all(type(value) is bool and value is True for value in actual.values())
    )


def exact_true_map_mutation_controls(
    baseline: Any,
    expected_keys: Any,
) -> dict[str, bool]:
    controls: dict[str, bool] = {
        "baseline_exact": exact_true_map(baseline, expected_keys),
    }
    if not isinstance(baseline, dict):
        return controls
    for key in expected_keys:
        missing = dict(baseline)
        missing.pop(key, None)
        controls[f"missing::{key}"] = not exact_true_map(missing, expected_keys)
        for label, bad_value in (
            ("false", False), ("integer_one", 1), ("string_true", "true"),
            ("none", None),
        ):
            mutant = dict(baseline)
            mutant[key] = bad_value
            controls[f"{label}::{key}"] = not exact_true_map(
                mutant, expected_keys
            )
    extra = dict(baseline)
    extra["UNREGISTERED_TRUE_CHECK"] = True
    controls["extra_true_key"] = not exact_true_map(extra, expected_keys)
    return controls


def expected_true_map_mutation_control_keys(expected_keys: Any) -> set[str]:
    keys = {"baseline_exact", "extra_true_key"}
    for key in expected_keys:
        keys.add(f"missing::{key}")
        for label in ("false", "integer_one", "string_true", "none"):
            keys.add(f"{label}::{key}")
    return keys


def matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def registry_bundle() -> dict[str, Any]:
    return {
        "FROZEN_PROMOTION_GATES": FROZEN_PROMOTION_GATES,
        "CANDIDATE_EVIDENCE_REQUIREMENTS": CANDIDATE_EVIDENCE_REQUIREMENTS,
        "NORMALIZED_IMPORT_OWNERSHIP": NORMALIZED_IMPORT_OWNERSHIP,
        "INVARIANT_LAW_LEDGER": INVARIANT_LAW_LEDGER,
        "OUTPUT_CLASSIFICATION": OUTPUT_CLASSIFICATION,
        "OVERLAY_OBLIGATION_MAP": OVERLAY_OBLIGATION_MAP,
        "SCOPE_FIREWALL": SCOPE_FIREWALL,
        "DEFERRED_OUTPUTS": DEFERRED_OUTPUTS,
        "PROMOTION_POLICY": PROMOTION_POLICY,
        "KNOWN_LIMITATIONS": KNOWN_LIMITATIONS,
        "SEMANTIC_ADJUDICATION_PROFILE": SEMANTIC_ADJUDICATION_PROFILE,
        "EXPECTED_BRANCHES": EXPECTED_BRANCHES,
        "INITIAL_CLOSURE_FLAGS": INITIAL_CLOSURE_FLAGS,
        "GATE_APPLICABILITY": GATE_APPLICABILITY,
    }


def registry_bundle_valid(bundle: Any) -> bool:
    return (
        isinstance(bundle, dict)
        and set(bundle) == set(EXPECTED_REGISTRY_SHA256)
        and all(
            canonical_sha256(bundle[name]) == digest
            for name, digest in EXPECTED_REGISTRY_SHA256.items()
        )
    )


def freedom_ledger_valid(ledger: Any) -> bool:
    expected = CLAIM_CONTRACT["FREEDOM_LEDGER"]
    return (
        isinstance(ledger, dict)
        and exact_tree(ledger, expected)
        and canonical_sha256(ledger) == EXPECTED_FREEDOM_LEDGER_SHA256
        and type(ledger["candidate_identity"]["range"]) is str
        and ledger["candidate_identity"]["range"] == CANDIDATE_ID
        and type(ledger["data_fitted_parameters"]["range"]) is int
        and ledger["data_fitted_parameters"]["range"] == 0
        and type(ledger["data_fitted_parameters"]["complexity"]) is int
        and ledger["data_fitted_parameters"]["complexity"] == 0
    )


def claim_contract_valid(contract: Any) -> bool:
    all_fields = REQUIRED_FIELDS | REQUIRED_CUSTOM_FIELDS
    return all((
        isinstance(contract, dict),
        isinstance(contract, dict) and set(contract) == all_fields,
        isinstance(contract, dict)
        and canonical_sha256(contract) == EXPECTED_CLAIM_CONTRACT_SHA256,
        isinstance(contract, dict)
        and freedom_ledger_valid(contract.get("FREEDOM_LEDGER")),
    ))


def normalized_imports_valid(ownership: Any, module_06: Any) -> bool:
    if not isinstance(ownership, dict) or set(ownership) != set(NORMALIZED_IMPORT_OWNERSHIP):
        return False
    required = {"origin", "declared_at", "allowed_meaning", "forbidden_inference"}
    schema_valid = all(
        isinstance(entry, dict)
        and set(entry) == required
        and entry["origin"] == LAW_ORIGIN_STATUS
        and all(isinstance(value, str) and value.strip() for value in entry.values())
        for entry in ownership.values()
    )
    contract_06 = getattr(module_06, "CLAIM_CONTRACT", {})
    primitive_registry = contract_06.get("PRIMITIVE_REGISTRY", {})
    frozen_imports = tuple(contract_06.get("IMPORTED_NOT_DERIVED", ()))
    expected_short_imports = tuple(
        getattr(module_06, "EXPECTED_IMPORTED_NOT_DERIVED", ())
    )
    functional_predeclared = all((
        "V(Q)=-alpha Tr_alg(Q^2)/2-b Tr_alg(Q^3)/3+"
        in contract_06.get("CLAIM", ""),
        "კვარტიკულამდე ფუნქციონალი" in primitive_registry.get(
            "10_imported_not_derived", ""
        ),
        "V(Q)-ის გლობალური argmin" in primitive_registry.get("4_rule", ""),
        "eigenvalue discriminant" in contract_06.get("METHOD", ""),
        contract_06.get("FREEDOM_LEDGER", {}).get("algebraic_invariants", {}).get(
            "range"
        ) == "I2 and I3",
        all(
            name in contract_06.get("FREEDOM_LEDGER", {})
            for name in ("alpha", "b", "c", "variational_rule")
        ),
    ))
    short_imports_owned = (
        frozen_imports == expected_short_imports
        and set(frozen_imports).issubset(ownership)
        and set(ownership) - set(frozen_imports)
        == {"quartic_invariant_functional_form_signs_and_truncation"}
    )
    no_new_assumption = (
        ownership["quartic_invariant_functional_form_signs_and_truncation"]["declared_at"]
        == "w2_06 frozen CLAIM, primitive registry items 4/10 and METHOD"
    )
    return all((
        schema_valid,
        functional_predeclared,
        short_imports_owned,
        no_new_assumption,
        canonical_sha256(ownership)
        == EXPECTED_REGISTRY_SHA256["NORMALIZED_IMPORT_OWNERSHIP"],
    ))


def invariant_law_audit() -> dict[str, Any]:
    alpha, b, c, s = sp.symbols("alpha b c s", positive=True, real=True)
    x, y, u, v, w = sp.symbols("x y u v w", real=True)
    Q = sp.Matrix([
        [x, u, v],
        [u, y, w],
        [v, w, -x - y],
    ])
    I2 = sp.expand(sp.trace(Q**2))
    I3 = sp.expand(sp.trace(Q**3))
    cayley_hamilton = sp.simplify(Q**3 - I2 * Q / 2 - I3 * sp.eye(3) / 3)
    degree_four_residual = sp.expand(sp.trace(Q**4) - I2**2 / 2)

    Q_star = s * sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
    I2_star = sp.simplify(sp.trace(Q_star**2))
    I3_star = sp.simplify(sp.trace(Q_star**3))
    amplitude_from_state = sp.simplify(3 * I3_star / I2_star)
    P1 = sp.simplify(sp.eye(3) / 3 + Q_star / amplitude_from_state)
    P2 = sp.simplify(sp.eye(3) - P1)
    projector_exact = all((
        matrix_is_zero(P1**2 - P1),
        matrix_is_zero(P2**2 - P2),
        matrix_is_zero(P1 * P2),
        sp.trace(P1) == 1,
        sp.trace(P2) == 2,
        P1.rank() == 1,
        P2.rank() == 2,
        matrix_is_zero(Q_star - amplitude_from_state * (P1 - sp.eye(3) / 3)),
    ))

    discriminant = sp.sqrt(b**2 + 24 * alpha * c)
    s_star = sp.simplify((b + discriminant) / (4 * c))
    stationary_residual = sp.simplify(2 * c * s_star**2 - b * s_star - 3 * alpha)
    radial_positive = sp.simplify(4 * c * s_star - b)
    biaxial_positive = sp.simplify(b * s_star)
    V_star = sp.simplify(
        -alpha * I2_star / 2 - b * I3_star / 3 + c * I2_star**2 / 4
    )
    V_minus_star = sp.simplify(
        -alpha * I2_star / 2 + b * I3_star / 3 + c * I2_star**2 / 4
    )
    sign_exchange_gap = sp.simplify(V_minus_star - V_star)
    invariant_monomials_through_degree_four = [
        (power_I2, power_I3)
        for power_I2 in range(3)
        for power_I3 in range(2)
        if 0 < 2 * power_I2 + 3 * power_I3 <= 4
    ]

    checks = {
        "traceless_three_by_three_Cayley_Hamilton_exact": matrix_is_zero(
            cayley_hamilton
        ),
        "degree_four_invariant_reduces_to_I2_squared": degree_four_residual == 0,
        "O3_invariant_ring_generation_theorem_scope_explicit": all((
            INVARIANT_LAW_LEDGER["invariant_ring_generators"]
            == ["I2=Tr_alg(Q^2)", "I3=Tr_alg(Q^3)"],
            INVARIANT_LAW_LEDGER["invariant_ring_theorem"]
            == (
                "real-symmetric spectral theorem plus the fundamental theorem of symmetric "
                "polynomials with e1=Tr(Q)=0"
            ),
            INVARIANT_LAW_LEDGER["invariant_ring_theorem_status"]
            == "STANDARD_EXACT_MATHEMATICAL_THEOREM__NOT_A_PHYSICAL_PRIMITIVE",
        )),
        "all_invariant_monomials_through_degree_four_enumerated": (
            invariant_monomials_through_degree_four == [(0, 1), (1, 0), (2, 0)]
            and INVARIANT_LAW_LEDGER["nonconstant_terms_through_degree_four"]
            == ["I2", "I3", "I2^2"]
        ),
        "frozen_same_order_invariant_ledger_exact": (
            INVARIANT_LAW_LEDGER["nonconstant_terms_through_degree_four"]
            == ["I2", "I3", "I2^2"]
            and INVARIANT_LAW_LEDGER["dependent_degree_four_identity"]
            == "Tr_alg(Q^4)=I2^2/2"
        ),
        "amplitude_is_intrinsic_state_invariant": amplitude_from_state == s,
        "Q_generated_projectors_exact": projector_exact,
        "rank_and_trace_prevent_O3_exchange": (
            sp.trace(P1) != sp.trace(P2) and P1.rank() != P2.rank()
        ),
        "positive_stationary_root_exact": stationary_residual == 0,
        "radial_normal_eigenvalue_positive_certificate": radial_positive == discriminant,
        "biaxial_normal_eigenvalue_positive_certificate": (
            biaxial_positive == b * (b + discriminant) / (4 * c)
            and b.is_positive is True
            and c.is_positive is True
        ),
        "role_exchange_is_Q_sign_and_not_law_symmetry": (
            matrix_is_zero(
                amplitude_from_state * (P2 - sp.Rational(2, 3) * sp.eye(3))
                + Q_star
            )
            and sign_exchange_gap == 4 * b * s**3 / 27
        ),
    }
    return {
        "CHECKS": checks,
        "DIAGNOSTICS": {
            "I2_star": str(I2_star),
            "I3_star": str(I3_star),
            "amplitude_from_state": str(amplitude_from_state),
            "P1": str(P1),
            "P2": str(P2),
            "projector_ranks": [int(P1.rank()), int(P2.rank())],
            "stationary_residual": str(stationary_residual),
            "radial_positive_certificate": str(radial_positive),
            "biaxial_positive_certificate": str(biaxial_positive),
            "Q_sign_exchange_energy_gap": str(sign_exchange_gap),
            "invariant_monomials_(power_I2,power_I3)_through_degree_four": (
                invariant_monomials_through_degree_four
            ),
        },
    }


def local_candidate_promotion_valid(
    evidence: Any,
    policy: Any,
    metadata: Any,
) -> bool:
    expected_metadata = {
        "candidate_id": CANDIDATE_ID,
        "route_class": ROUTE_CLASS,
        "witness_kind": WITNESS_KIND,
        "stability_kind": STABILITY_KIND,
        "law_origin_status": LAW_ORIGIN_STATUS,
    }
    return all((
        isinstance(evidence, dict),
        isinstance(evidence, dict) and set(evidence) == set(FROZEN_PROMOTION_GATES),
        isinstance(evidence, dict)
        and all(type(value) is bool and value is True for value in evidence.values()),
        isinstance(policy, dict),
        isinstance(policy, dict) and set(policy) == set(PROMOTION_POLICY),
        isinstance(policy, dict)
        and all(type(value) is bool and value is False for value in policy.values()),
        exact_literal_map(metadata, expected_metadata),
    ))


def promotion_evidence_schema_valid(evidence: Any) -> bool:
    return (
        isinstance(evidence, dict)
        and set(evidence) == set(FROZEN_PROMOTION_GATES)
        and all(type(value) is bool for value in evidence.values())
    )


def semantic_profile_schema_valid(profile: Any) -> bool:
    if not isinstance(profile, dict) or set(profile) != set(SEMANTIC_ADJUDICATION_PROFILE):
        return False
    boolean_fields = set(SEMANTIC_ADJUDICATION_PROFILE) - {"role_ranks"}
    ranks = profile.get("role_ranks")
    return all((
        all(type(profile[key]) is bool for key in boolean_fields),
        type(ranks) is list,
        type(ranks) is list and len(ranks) == 2,
        type(ranks) is list
        and all(type(rank) is int and rank > 0 for rank in ranks),
    ))


def semantic_profile_to_evidence(
    base_evidence: Any,
    profile: Any,
    independently_derived_role_ranks: Any,
) -> dict[str, bool]:
    """Derive semantic gate values from structured candidate facts."""
    if not promotion_evidence_schema_valid(base_evidence):
        return {gate: False for gate in FROZEN_PROMOTION_GATES}
    evidence = dict(base_evidence)
    if not semantic_profile_schema_valid(profile):
        return {gate: False for gate in FROZEN_PROMOTION_GATES}
    independently_derived_ranks_valid = all((
        type(independently_derived_role_ranks) is list,
        type(independently_derived_role_ranks) is list
        and len(independently_derived_role_ranks) == 2,
        type(independently_derived_role_ranks) is list
        and all(
            type(rank) is int and rank > 0
            for rank in independently_derived_role_ranks
        ),
    ))
    if not independently_derived_ranks_valid:
        return {gate: False for gate in FROZEN_PROMOTION_GATES}

    def restrict(gate: str, condition: bool) -> None:
        evidence[gate] = bool(evidence[gate] is True and condition is True)

    ranks = profile["role_ranks"]
    role_ranks_cross_bound = all((
        exact_tree(ranks, independently_derived_role_ranks),
        ranks == [1, 2],
    ))
    no_target_preload = all((
        profile["target_orbit_distance_term_used"] is False,
        profile["post_output_cubic_or_sign_choice_used"] is False,
    ))
    internal_only = all((
        profile["N3_called_physical_space"] is False,
        profile["O3_called_physical_rotation"] is False,
        profile["delta_called_spacetime_metric"] is False,
    ))

    restrict(
        "intrinsic_differentiation_certified",
        all((
            profile["fixed_basis_or_direct_sum_roles_used"] is False,
            role_ranks_cross_bound,
        )),
    )
    restrict(
        "inequivalence_survives_full_quotient",
        all((
            role_ranks_cross_bound,
            profile["full_declared_equivalence_can_swap_roles"] is False,
            profile["Q_sign_is_gauge"] is False,
        )),
    )
    restrict(
        "law_relevance_not_arbitrary_decomposition",
        all((
            profile["law_forces_selected_role_pattern"] is True,
            profile["arbitrary_spectral_decomposition_used"] is False,
        )),
    )
    restrict(
        "realization_or_selection_noncircular",
        profile["representative_direction_selected"] is False,
    )
    restrict("target_free_law_certified", no_target_preload)
    restrict("forbidden_target_intersection_empty", no_target_preload)
    restrict(
        "open_domain_stability_and_robustness",
        profile["parameter_support_is_open"] is True,
    )
    restrict(
        "live_identity_and_dependencies_exact",
        profile["unregistered_higher_invariant_added"] is False,
    )
    restrict(
        "complete_one_foundation_primitive_freedom_registry",
        all((
            profile["unregistered_higher_invariant_added"] is False,
            profile["functional_ownership_complete"] is True,
        )),
    )
    restrict("foundation_admissibility_and_import_health", internal_only)
    restrict(
        "f1_only_scope_honest",
        profile["Hessian_called_temporal_formation"] is False,
    )
    restrict(
        "router_extension_aligned",
        profile["route_obligations_satisfied"] is True,
    )
    return evidence


VALIDATOR_RESULT_KEYS = frozenset({
    "w2_08_primary", "w2_08_independent", "w2_09_candidate_specific",
})


def validator_consensus_valid(evidence: Any, results: Any) -> bool:
    if not promotion_evidence_schema_valid(evidence):
        return False
    if not isinstance(results, dict) or set(results) != VALIDATOR_RESULT_KEYS:
        return False
    if any(type(value) is not bool for value in results.values()):
        return False
    expected_outcome = all(value is True for value in evidence.values())
    return all(value is expected_outcome for value in results.values())


def raw_validator_promotion(results: Any) -> bool:
    return (
        isinstance(results, dict)
        and set(results) == VALIDATOR_RESULT_KEYS
        and all(type(value) is bool and value is True for value in results.values())
    )


def effective_promotion(audit_valid: bool, raw_promoted: bool) -> bool:
    return bool(
        type(audit_valid) is bool
        and type(raw_promoted) is bool
        and audit_valid
        and raw_promoted
    )


def adjudication_status(audit_valid: bool, raw_promoted: bool) -> str:
    if type(audit_valid) is not bool or type(raw_promoted) is not bool or not audit_valid:
        return "W2_06_PHYSICAL_F1_ADJUDICATION_INVALID__PROGRAMME_W2_F1_OPEN"
    if raw_promoted:
        return (
            "W2_06_PHYSICAL_F1_ADJUDICATION_COMPLETE__PROMOTED_STRUCTURAL_"
            "RELATIVE_TO_IMPORTED_PRIMITIVES__F2_AND_LATER_OPEN"
        )
    return (
        "W2_06_PHYSICAL_F1_ADJUDICATION_COMPLETE__NOT_PROMOTED__"
        "CONDITIONAL_MATHEMATICS_RETAINED__FALLBACKS_OPEN"
    )


def expected_runtime_closure(contract_valid: bool, promoted: bool) -> dict[str, bool]:
    closure = dict(INITIAL_CLOSURE_FLAGS)
    exact_contract_valid = type(contract_valid) is bool and contract_valid is True
    exact_promoted = type(promoted) is bool and promoted is True
    for key in (
        "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
        "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION",
        "F1_PROMOTION_CONTRACT_FROZEN", "F1_ROUTE_TAXONOMY_V2_FROZEN",
        "W2_06_CLASSIFICATION_ALIGNED", "W2_06_OVERLAY_CLASS_EVALUATED",
    ):
        closure[key] = exact_contract_valid
    for key in (
        "W2_06_OVERLAY_CLASS_SATISFIED", "W2_06_PROMOTED_TO_W2_F1",
        "W2_F1_ATEMPORAL_STRUCTURAL_RELATIVE_TO_FROZEN_PRIMITIVES",
        "W2_F1_SELF_DIFFERENTIATION",
    ):
        closure[key] = bool(exact_contract_valid and exact_promoted)
    return closure


def runtime_closure_valid(
    closure: Any,
    contract_valid: bool,
    promoted: bool,
) -> bool:
    return all((
        type(contract_valid) is bool,
        type(promoted) is bool,
        exact_literal_map(
            closure, expected_runtime_closure(contract_valid, promoted)
        ),
    ))


def w2_06_report_valid(module_06: Any, report: Any) -> bool:
    if not isinstance(report, dict):
        return False
    checks = report.get("CHECKS", {})
    closure = report.get("CLOSURE_FLAGS", {})
    digests = {
        "W2_06_CHECK_KEYS": canonical_sha256(sorted(checks)),
        "W2_06_CLOSURE_FLAGS": canonical_sha256(closure),
        "W2_06_PROVENANCE": canonical_sha256(report.get("PROVENANCE")),
    }
    return all((
        getattr(module_06, "MODEL_VERSION", None)
        == "W2-F1-ATEMPORAL-SPECTRAL-SPLIT-v1.0-internal",
        report.get("MODEL_VERSION")
        == "W2-F1-ATEMPORAL-SPECTRAL-SPLIT-v1.0-internal",
        report.get("STATUS")
        == "EXACT_ATEMPORAL_SPECTRAL_CANDIDATE_PASS__W2_F1_PROMOTION_OPEN",
        isinstance(checks, dict) and len(checks) == 25,
        all(type(value) is bool and value is True for value in checks.values()),
        digests == {
            key: EXPECTED_REPORT_SHA256[key]
            for key in (
                "W2_06_CHECK_KEYS", "W2_06_CLOSURE_FLAGS", "W2_06_PROVENANCE"
            )
        },
        closure.get("ATEMPORAL_SPECTRAL_SPLIT_EXACT") is True,
        closure.get("QUOTIENT_STABILITY_EXACT") is True,
        closure.get("W2_F1_CONDITIONAL_CANDIDATE") is True,
        closure.get("W2_F1_SELF_DIFFERENTIATION") is False,
        closure.get("G6_PHYSICAL_MATCH") is False,
        closure.get("G7_OBSERVATION") is False,
        closure.get("G8_EXPORT") is False,
        getattr(module_06, "CLAIM_CONTRACT", {}).get("CLAIM_ID") == CANDIDATE_ID,
    ))


def w2_08_report_valid(module_08: Any, report: Any) -> bool:
    if not isinstance(report, dict):
        return False
    checks = report.get("CHECKS", {})
    closure = report.get("CLOSURE_FLAGS", {})
    digests = {
        "W2_08_CHECK_KEYS": canonical_sha256(sorted(checks)),
        "W2_08_CLOSURE_FLAGS": canonical_sha256(closure),
        "W2_08_PROVENANCE": canonical_sha256(report.get("PROVENANCE")),
    }
    classification = report.get("CANDIDATE_CLASSIFICATION", {})
    evaluation = report.get("CANDIDATE_EVALUATION", {})
    return all((
        getattr(module_08, "MODEL_VERSION", None) == PROMOTION_CONTRACT_VERSION,
        report.get("MODEL_VERSION") == PROMOTION_CONTRACT_VERSION,
        report.get("ROUTER_VERSION") == ROUTER_VERSION,
        report.get("STATUS")
        == "W2_F1_PROMOTION_CONTRACT_FROZEN__ATEMPORAL_INTRASTATE_CLASS_ALIGNED__W2_06_ADJUDICATION_OPEN",
        isinstance(checks, dict) and len(checks) == 31,
        all(type(value) is bool and value is True for value in checks.values()),
        digests == {
            key: EXPECTED_REPORT_SHA256[key]
            for key in (
                "W2_08_CHECK_KEYS", "W2_08_CLOSURE_FLAGS", "W2_08_PROVENANCE"
            )
        },
        report.get("PROMOTION_AND_GATES") == FROZEN_PROMOTION_GATES,
        getattr(module_08, "PROMOTION_AND_GATES", None) == FROZEN_PROMOTION_GATES,
        classification.get("candidate_claim_id") == CANDIDATE_ID,
        classification.get("effective_v2_class") == ROUTE_CLASS,
        classification.get("witness_kind_for_w2_09") == WITNESS_KIND,
        classification.get("stability_kind_for_w2_09") == STABILITY_KIND,
        classification.get("promotion_status")
        == "NOT_EVALUATED__PROGRAMME_W2_F1_OPEN",
        isinstance(evaluation, dict)
        and set(evaluation) == set(FROZEN_PROMOTION_GATES)
        and all(
            type(value) is str and value == "OPEN__TO_BE_ADJUDICATED_IN_W2_09"
            for value in evaluation.values()
        ),
        closure.get("F1_PROMOTION_CONTRACT_FROZEN") is True,
        closure.get("F1_ROUTE_TAXONOMY_V2_FROZEN") is True,
        closure.get("W2_06_CLASSIFICATION_ALIGNED") is True,
        closure.get("W2_06_OVERLAY_CLASS_EVALUATED") is False,
        closure.get("W2_F1_SELF_DIFFERENTIATION") is False,
    ))


def source_boundaries_valid(texts: dict[str, str]) -> bool:
    return all((
        "ერთადერთი უცვლელი ღერძია საუკეთესო ხელმისაწვდომ დაკვირვებებთან სრული თავსებადობა"
        in texts["CODES"],
        "განსაზღვრება ან კონსტრუქცია ქმნის თანმიმდევრულ ობიექტს, მაგრამ მის ფიზიკურ წარმოშობას თავისით არ ამტკიცებს"
        in texts["CODES"],
        "დროის არმქონე კანდიდატში თვითგარჩევა შეიძლება იყოს ამონახსნთა სტრუქტურული არჩევა და არა დროითი მოვლენა"
        in texts["W2_C0"],
        "W2_F1" in texts["W2_C0"] and "target-free, მდგრადი თვითგარჩევა" in texts["W2_C0"],
        "ფუძიდან გამოვლენილ გარემომდე გადასვლა სტრუქტურული თვითგარჩევაა და არა წინასწარ არსებულ საათში მომხდარი მოვლენა"
        in texts["CANON"],
        "მრავლობითობა ბუნებაში მხოლოდ მაშინ ჩნდება, როდესაც ფუძის თვითგარჩევით წარმოქმნილი განსხვავება სტაბილურ ფიზიკურ კვალს ტოვებს"
        in texts["INTUITIVE"],
    ))


def run_gate() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    work2 = root / "RefG" / "work 2"
    paths = {
        "CODES": root / "CODES.md",
        "CANON": root / "Theory_Canon.md",
        "INTUITIVE": root / "intuitive" / "RefG_GE.md",
        "W2_C0": work2 / "w2_00_foundation_to_einstein_contract.md",
        "W2_06": work2 / "w2_06_f1_atemporal_spectral_split_candidate_gate.py",
        "W2_07": work2 / "w2_07_f1_route_adjudication_gate.py",
        "W2_08": work2 / "w2_08_f1_physical_promotion_contract.py",
        "SOURCE": Path(__file__).resolve(),
    }

    dependency_hashes = {
        name: sha256(paths[name]) for name in EXPECTED_DEPENDENCY_SHA256
    }
    dependency_bytes_exact = dependency_hashes == EXPECTED_DEPENDENCY_SHA256

    # The promotion contract runs first and reexecutes the prior chain.  The
    # candidate is then rerun directly to expose its exact evidence to this gate.
    module_08 = load_module(paths["W2_08"], "w2_08_w2_09_dependency")
    report_08 = module_08.run_gate()
    module_06 = load_module(paths["W2_06"], "w2_06_w2_09_candidate")
    report_06 = module_06.run_gate()

    texts = {
        name: paths[name].read_text(encoding="utf-8")
        for name in ("CODES", "CANON", "INTUITIVE", "W2_C0")
    }
    report_06_exact = w2_06_report_valid(module_06, report_06)
    report_08_exact = w2_08_report_valid(module_08, report_08)
    live_identity_exact = all((
        dependency_bytes_exact,
        report_06_exact,
        report_08_exact,
        report_08.get("PROVENANCE", {}).get("W2_06")
        == EXPECTED_DEPENDENCY_SHA256["W2_06"],
        report_08.get("PROVENANCE", {}).get("W2_07")
        == EXPECTED_DEPENDENCY_SHA256["W2_07"],
        report_08.get("PROVENANCE", {}).get("SOURCE")
        == EXPECTED_DEPENDENCY_SHA256["W2_08"],
    ))

    all_contract_fields = REQUIRED_FIELDS | REQUIRED_CUSTOM_FIELDS
    contract_fields_exact = set(CLAIM_CONTRACT) == all_contract_fields
    contract_values_nonempty = all(
        value_present(CLAIM_CONTRACT.get(key)) for key in all_contract_fields
    )
    contract_model_bound = all((
        CLAIM_CONTRACT.get("CLAIM_ID") == "W2_F1_ATEMPORAL_STRUCTURAL_PROMOTION_001",
        isinstance(CLAIM_CONTRACT.get("MODEL_VERSION"), str),
        CLAIM_CONTRACT.get("MODEL_VERSION", "").startswith(MODEL_VERSION),
    ))
    claimed_custom = {
        "PROMOTION_CONTRACT_VERSION": PROMOTION_CONTRACT_VERSION,
        "ROUTER_VERSION": ROUTER_VERSION,
        "WITNESS_KIND": WITNESS_KIND,
        "STABILITY_KIND": STABILITY_KIND,
        "LAW_ORIGIN_STATUS": LAW_ORIGIN_STATUS,
        "FROZEN_PROMOTION_GATES": FROZEN_PROMOTION_GATES,
        "CANDIDATE_EVIDENCE_REQUIREMENTS": CANDIDATE_EVIDENCE_REQUIREMENTS,
        "NORMALIZED_IMPORT_OWNERSHIP": NORMALIZED_IMPORT_OWNERSHIP,
        "INVARIANT_LAW_LEDGER": INVARIANT_LAW_LEDGER,
        "OVERLAY_OBLIGATION_MAP": OVERLAY_OBLIGATION_MAP,
        "OUTPUT_CLASSIFICATION": OUTPUT_CLASSIFICATION,
        "SCOPE_FIREWALL": SCOPE_FIREWALL,
        "DEFERRED_OUTPUTS": list(DEFERRED_OUTPUTS),
        "PROMOTION_POLICY": PROMOTION_POLICY,
        "KNOWN_LIMITATIONS": KNOWN_LIMITATIONS,
        "SEMANTIC_ADJUDICATION_PROFILE": SEMANTIC_ADJUDICATION_PROFILE,
        "NEXT_ATOMIC_TASK": NEXT_ATOMIC_TASK,
    }
    contract_custom_bound = all(
        CLAIM_CONTRACT.get(key) == value for key, value in claimed_custom.items()
    )
    static_contract_exact = all((
        freedom_ledger_valid(CLAIM_CONTRACT.get("FREEDOM_LEDGER")),
        CLAIM_CONTRACT.get("BRANCHES") == EXPECTED_BRANCHES,
        exact_literal_map(
            CLAIM_CONTRACT.get("CLOSURE_FLAGS"), INITIAL_CLOSURE_FLAGS
        ),
        CLAIM_CONTRACT.get("GATE_APPLICABILITY") == GATE_APPLICABILITY,
        set(GATE_APPLICABILITY) == UNIVERSAL_GATES,
        all(
            isinstance(value, str) and value.strip()
            for value in GATE_APPLICABILITY.values()
        ),
        CLAIM_CONTRACT.get("DATA_ROLE", "").startswith("N/A"),
        CLAIM_CONTRACT.get("OBSERVABLE_MAP", "").startswith("N/A"),
        CLAIM_CONTRACT.get("FORWARD_MODEL", "").startswith("N/A"),
    ))
    whole_claim_contract_exact = claim_contract_valid(CLAIM_CONTRACT)
    claim_contract_mutants: dict[str, dict[str, Any]] = {}
    for field in ("CLAIM", "METHOD", "FAIL_CONDITION", "FALSIFIER"):
        mutant = copy.deepcopy(CLAIM_CONTRACT)
        mutant[field] = f"{mutant[field]} MUTATED"
        claim_contract_mutants[f"{field.lower()}_drift_rejected"] = mutant
    pass_mutant = copy.deepcopy(CLAIM_CONTRACT)
    pass_mutant["PASS_CONDITION"].append("post-hoc pass condition")
    claim_contract_mutants["pass_condition_drift_rejected"] = pass_mutant
    identity_mutant = copy.deepcopy(CLAIM_CONTRACT)
    identity_mutant["FREEDOM_LEDGER"]["candidate_identity"]["range"] = (
        "SOME_OTHER_CANDIDATE"
    )
    claim_contract_mutants["candidate_identity_drift_rejected"] = identity_mutant
    false_zero_mutant = copy.deepcopy(CLAIM_CONTRACT)
    false_zero_mutant["FREEDOM_LEDGER"]["data_fitted_parameters"]["range"] = False
    claim_contract_mutants["false_is_not_accepted_as_zero"] = false_zero_mutant
    next_task_mutant = copy.deepcopy(CLAIM_CONTRACT)
    next_task_mutant["NEXT_ATOMIC_TASK"] = "Skip directly to GR."
    claim_contract_mutants["next_atomic_task_drift_rejected"] = next_task_mutant
    missing_claim_field = copy.deepcopy(CLAIM_CONTRACT)
    missing_claim_field.pop("CLAIM")
    claim_contract_mutants["missing_standard_field_rejected"] = missing_claim_field
    extra_claim_field = copy.deepcopy(CLAIM_CONTRACT)
    extra_claim_field["UNREGISTERED_OVERRIDE"] = False
    claim_contract_mutants["extra_field_rejected"] = extra_claim_field
    claim_contract_mutation_controls = {
        name: not claim_contract_valid(mutant)
        for name, mutant in claim_contract_mutants.items()
    }
    own_bundle = registry_bundle()
    own_registries_exact = registry_bundle_valid(own_bundle)

    contract_06 = getattr(module_06, "CLAIM_CONTRACT", {})
    checks_06 = report_06.get("CHECKS", {})
    closure_06 = report_06.get("CLOSURE_FLAGS", {})
    import_ownership_exact = normalized_imports_valid(
        NORMALIZED_IMPORT_OWNERSHIP, module_06
    )
    candidate_registry_complete = all((
        checks_06.get("required_contract_and_custom_fields_present") is True,
        checks_06.get("registries_exactly_bound") is True,
        checks_06.get("primitive_registry_values_nonblank") is True,
        checks_06.get("freedom_ledger_exact_and_complete") is True,
        tuple(contract_06.get("IMPORTED_NOT_DERIVED", ()))
        == tuple(getattr(module_06, "EXPECTED_IMPORTED_NOT_DERIVED", ())),
        import_ownership_exact,
    ))

    algebra_audit = invariant_law_audit()
    independently_derived_role_ranks = algebra_audit.get("DIAGNOSTICS", {}).get(
        "projector_ranks"
    )
    independent_algebra_exact = all(
        type(value) is bool and value is True
        for value in algebra_audit["CHECKS"].values()
    )
    invariant_ledger_exact = all((
        independent_algebra_exact,
        canonical_sha256(INVARIANT_LAW_LEDGER)
        == EXPECTED_REGISTRY_SHA256["INVARIANT_LAW_LEDGER"],
        checks_06.get("O3_invariance_exact") is True,
        checks_06.get("N1_N2_N4_generalN_b0_polarity_coercivity_and_source_controls")
        is True,
    ))

    freedom_06 = contract_06.get("FREEDOM_LEDGER", {})
    primitive_06 = contract_06.get("PRIMITIVE_REGISTRY", {})
    forbidden_target_firewall = all((
        checks_06.get("target_leakage_absent") is True,
        "N=3 შიდა trial dimension-ია და არა 3-space"
        in contract_06.get("DOMAIN", ""),
        "Tr_alg არ ნიშნავს persistent trace-ს"
        in contract_06.get("CONVENTIONS", ""),
        contract_06.get("METRIC_ROUTE", "").startswith("N/A"),
        "no representative direction" in contract_06.get("SELECTION_RULE", ""),
        freedom_06.get("seed_or_randomness", {}).get("range") == 0,
        freedom_06.get("data_fitted_parameters", {}).get("range") == 0,
        SCOPE_FIREWALL == {key: False for key in SCOPE_FIREWALL},
        "target spectrum/orbit distance"
        in INVARIANT_LAW_LEDGER["forbidden_terms_absent"],
        PROMOTION_POLICY["downstream_target_used"] is False,
        PROMOTION_POLICY["N3_or_rank_signature_priority_bonus_used"] is False,
    ))

    reference_trivial = all((
        checks_06.get("origin_has_no_nontrivial_Q_generated_projector") is True,
        checks_06.get("origin_stationary_and_strictly_unstable") is True,
        OUTPUT_CLASSIFICATION["Q_zero"]
        == "STATIONARY_STRICT_VARIATIONAL_MAXIMUM__NO_CANONICAL_NONTRIVIAL_ROLE",
    ))
    target_free_law = all((
        invariant_ledger_exact,
        forbidden_target_firewall,
        checks_06.get("O3_invariance_exact") is True,
        "target projector or rank" in INVARIANT_LAW_LEDGER["forbidden_terms_absent"],
        INVARIANT_LAW_LEDGER["origin_status"] == LAW_ORIGIN_STATUS,
    ))
    output_classification_complete = all((
        checks_06.get("sharp_discriminant_bound_and_global_orbit") is True,
        checks_06.get("independent_stationary_branches_and_energy_order") is True,
        checks_06.get("N1_N2_N4_generalN_b0_polarity_coercivity_and_source_controls")
        is True,
        contract_06.get("BRANCHES") == getattr(module_06, "EXPECTED_BRANCHES", None),
        canonical_sha256(OUTPUT_CLASSIFICATION)
        == EXPECTED_REGISTRY_SHA256["OUTPUT_CLASSIFICATION"],
        set(OUTPUT_CLASSIFICATION) == {
            "alpha_b_c_positive", "Q_zero", "negative_stationary_root",
            "O3_orientation_orbit", "b_zero_boundary", "alpha_zero_boundary",
            "c_zero_or_negative", "b_negative", "positive_quadratic_null",
            "N_one", "N_two", "N_four_and_general_N", "explicit_linear_source",
            "invariant_target_orbit_distance",
        },
    ))
    intrinsic_roles = all((
        checks_06.get("Q_generated_rank_1_rank_2_projectors") is True,
        algebra_audit["CHECKS"].get("amplitude_is_intrinsic_state_invariant") is True,
        algebra_audit["CHECKS"].get("Q_generated_projectors_exact") is True,
        reference_trivial,
    ))
    full_declared_quotient_inequivalence = all((
        checks_06.get("faithful_O3_mod_center_action_not_O3_mod_SO3") is True,
        algebra_audit["CHECKS"].get("rank_and_trace_prevent_O3_exchange") is True,
        algebra_audit["CHECKS"].get("role_exchange_is_Q_sign_and_not_law_symmetry")
        is True,
        "Q->-Q gauge არაა" in contract_06.get("CONVENTIONS", ""),
        KNOWN_LIMITATIONS["full_equivalence_ceiling"]
        == "NONEXCHANGEABILITY_ONLY_UNDER_COMPLETE_DECLARED_O3_RELABEL_RULE",
    ))
    law_forces_roles = all((
        checks_06.get("sharp_discriminant_bound_and_global_orbit") is True,
        checks_06.get("independent_stationary_branches_and_energy_order") is True,
        checks_06.get("Q_generated_rank_1_rank_2_projectors") is True,
        algebra_audit["CHECKS"].get("Q_generated_projectors_exact") is True,
        PROMOTION_POLICY["preassigned_roles_used"] is False,
        "preselected basis" not in contract_06.get("SELECTION_RULE", "").lower(),
    ))
    selection_noncircular = all((
        "atemporal_global_argmin_rule" in contract_06.get("IMPORTED_NOT_DERIVED", []),
        "global argmin followed by O(3) quotient"
        in contract_06.get("SELECTION_RULE", ""),
        "no representative direction" in contract_06.get("SELECTION_RULE", ""),
        freedom_06.get("seed_or_randomness", {}).get("range") == 0,
        output_classification_complete,
        target_free_law,
        NORMALIZED_IMPORT_OWNERSHIP["atemporal_global_argmin_rule"]["origin"]
        == LAW_ORIGIN_STATUS,
        PROMOTION_POLICY["imported_law_called_derived_without_gate"] is False,
    ))
    open_domain_stability = all((
        checks_06.get("orbit_normal_hessian_positive_with_only_orbit_zero_modes")
        is True,
        checks_06.get("sharp_discriminant_bound_and_global_orbit") is True,
        algebra_audit["CHECKS"].get("radial_normal_eigenvalue_positive_certificate")
        is True,
        algebra_audit["CHECKS"].get("biaxial_normal_eigenvalue_positive_certificate")
        is True,
        all(
            freedom_06.get(name, {}).get("range") == "(0,infinity)"
            for name in ("alpha", "b", "c")
        ),
        KNOWN_LIMITATIONS["robustness_ceiling"]
        == "OPEN_ALPHA_B_C_DOMAIN_WITHIN_FROZEN_QUARTIC_LAW_CLASS",
    ))
    foundation_import_health = all((
        candidate_registry_complete,
        forbidden_target_firewall,
        import_ownership_exact,
        all(
            entry["origin"] == LAW_ORIGIN_STATUS
            for entry in NORMALIZED_IMPORT_OWNERSHIP.values()
        ),
        "Sym_0(3,R)" in primitive_06.get("10_imported_not_derived", ""),
        "კვარტიკულამდე ფუნქციონალი" in primitive_06.get(
            "10_imported_not_derived", ""
        ),
        KNOWN_LIMITATIONS["foundation_law_origin"].startswith("OPEN_"),
        KNOWN_LIMITATIONS["RefG_resonant_environment_map"].startswith("OPEN_"),
        PROMOTION_POLICY["F2_or_later_semantics_claimed"] is False,
    ))

    preliminary_evidence: dict[str, bool] = {
        "f1_definition_frozen_route_neutral": all((
            report_08_exact,
            getattr(module_08, "F1_DEFINITION", None)
            == report_08.get("F1_DEFINITION"),
            getattr(module_08, "definition_is_route_neutral")(
                getattr(module_08, "F1_DEFINITION", None)
            ),
        )),
        "witness_kind_frozen_before_evaluation": all((
            report_08.get("CANDIDATE_CLASSIFICATION", {}).get(
                "witness_kind_for_w2_09"
            ) == WITNESS_KIND,
            WITNESS_KIND in getattr(module_08, "WITNESS_KINDS", {}),
        )),
        "live_identity_and_dependencies_exact": live_identity_exact,
        "complete_one_foundation_primitive_freedom_registry": candidate_registry_complete,
        "forbidden_target_intersection_empty": forbidden_target_firewall,
        "undifferentiated_reference_trivial": reference_trivial,
        "target_free_law_certified": target_free_law,
        "complete_output_classification": output_classification_complete,
        "intrinsic_differentiation_certified": intrinsic_roles,
        "inequivalence_survives_full_quotient": full_declared_quotient_inequivalence,
        "law_relevance_not_arbitrary_decomposition": law_forces_roles,
        "realization_or_selection_noncircular": selection_noncircular,
        "open_domain_stability_and_robustness": open_domain_stability,
        "foundation_admissibility_and_import_health": foundation_import_health,
        "router_extension_aligned": False,
        "independent_crosscheck_and_controls": all((
            checks_06.get("independent_stationary_branches_and_energy_order") is True,
            checks_06.get("orbit_normal_hessian_positive_with_only_orbit_zero_modes")
            is True,
            independent_algebra_exact,
        )),
        "candidate_falsifier_absent": all((
            checks_06.get("sharp_discriminant_bound_and_global_orbit") is True,
            checks_06.get("orbit_normal_hessian_positive_with_only_orbit_zero_modes")
            is True,
            closure_06.get("ATEMPORAL_SPECTRAL_SPLIT_EXACT") is True,
        )),
        "f1_only_scope_honest": all((
            checks_06.get("all_physical_and_export_flags_honestly_open") is True,
            exact_literal_map(SCOPE_FIREWALL, {key: False for key in SCOPE_FIREWALL}),
            closure_06.get("W2_F2_OPERATIONAL_RELATIONS") is False,
            closure_06.get("W2_F3_INTERNAL_ORDER_CAUSALITY") is False,
            closure_06.get("W2_F4_INDEPENDENT_ADDITIVE_MODES") is False,
            closure_06.get("W2_M1_DIMENSION_CONTINUUM") is False,
            closure_06.get("W2_M2_LORENTZIAN_METRIC") is False,
            closure_06.get("W2_A0_EFFECTIVE_ACTION_ORIGIN") is False,
        )),
    }

    overlay = getattr(module_08, "ROUTE_TAXONOMY_OVERLAY_V2", {}).get(
        ROUTE_CLASS, {}
    )
    expected_overlay_imports = {
        "one_foundation_internal_state_space",
        "complete_equivalence_and_automorphism_rule",
        "undifferentiated_reference_or_no_preloading_certificate",
        "target_free_atemporal_selection_or_consistency_law",
        "declared_structural_stability_criterion_and_parameter_domain",
    }
    overlay_imports_satisfied = all((
        set(overlay.get("imports_to_declare", ())) == expected_overlay_imports,
        candidate_registry_complete,
        full_declared_quotient_inequivalence,
        reference_trivial,
        target_free_law,
        selection_noncircular,
        open_domain_stability,
    ))
    semantic_pre_overlay_evidence = semantic_profile_to_evidence(
        preliminary_evidence,
        SEMANTIC_ADJUDICATION_PROFILE,
        independently_derived_role_ranks,
    )
    overlay_derivations_satisfied = all((
        set(overlay.get("must_derive", ())) == set(OVERLAY_OBLIGATION_MAP),
        all(
            all(semantic_pre_overlay_evidence[gate] is True for gate in gates)
            for gates in OVERLAY_OBLIGATION_MAP.values()
        ),
    ))
    preliminary_evidence["router_extension_aligned"] = all((
        report_08.get("CANDIDATE_CLASSIFICATION", {}).get("effective_v2_class")
        == ROUTE_CLASS,
        overlay_imports_satisfied,
        overlay_derivations_satisfied,
    ))
    candidate_fact_evidence = semantic_profile_to_evidence(
        preliminary_evidence,
        SEMANTIC_ADJUDICATION_PROFILE,
        independently_derived_role_ranks,
    )

    metadata = {
        "candidate_id": CANDIDATE_ID,
        "route_class": ROUTE_CLASS,
        "witness_kind": WITNESS_KIND,
        "stability_kind": STABILITY_KIND,
        "law_origin_status": LAW_ORIGIN_STATUS,
    }

    def validator_results_for(
        evidence: Any,
        policy: Any = PROMOTION_POLICY,
        local_metadata: Any = metadata,
    ) -> dict[str, bool]:
        return {
            "w2_08_primary": getattr(module_08, "promotion_evidence_valid")(
                evidence, WITNESS_KIND, LAW_ORIGIN_STATUS, policy
            ),
            "w2_08_independent": getattr(
                module_08, "independent_promotion_audit"
            )(evidence, WITNESS_KIND, LAW_ORIGIN_STATUS, policy),
            "w2_09_candidate_specific": local_candidate_promotion_valid(
                evidence, policy, local_metadata
            ),
        }

    def all_validators_reject(
        evidence: Any,
        policy: Any = PROMOTION_POLICY,
        local_metadata: Any = metadata,
    ) -> bool:
        results = validator_results_for(evidence, policy, local_metadata)
        return all(type(value) is bool and value is False for value in results.values())

    gate_mutation_controls: dict[str, bool] = {}
    for gate in FROZEN_PROMOTION_GATES:
        mutants: list[dict[str, Any]] = []
        missing = dict(candidate_fact_evidence)
        missing.pop(gate)
        mutants.append(missing)
        for bad_value in (False, 1, "true", None):
            mutant = dict(candidate_fact_evidence)
            mutant[gate] = bad_value
            mutants.append(mutant)
        gate_mutation_controls[gate] = all(
            all_validators_reject(mutant) for mutant in mutants
        )
    extra_gate = dict(candidate_fact_evidence)
    extra_gate["N3_resemblance_bonus"] = True
    extra_gate_rejected = all_validators_reject(extra_gate)

    policy_mutation_controls: dict[str, bool] = {}
    for key in PROMOTION_POLICY:
        mutants: list[dict[str, Any]] = []
        missing = dict(PROMOTION_POLICY)
        missing.pop(key)
        mutants.append(missing)
        for bad_value in (True, 1, 0, None):
            mutant = dict(PROMOTION_POLICY)
            mutant[key] = bad_value
            mutants.append(mutant)
        policy_mutation_controls[key] = all(
            all_validators_reject(candidate_fact_evidence, mutant)
            for mutant in mutants
        )
    extra_policy = dict(PROMOTION_POLICY)
    extra_policy["GR_override"] = False
    extra_policy_rejected = all_validators_reject(
        candidate_fact_evidence, extra_policy
    )

    metadata_mutation_controls: dict[str, bool] = {}
    metadata_bad_values = {
        "candidate_id": "SOME_OTHER_CANDIDATE",
        "route_class": "atemporal_nonunique_solution_structure",
        "witness_kind": "INTER_CLASS_INEQUIVALENT_OUTCOMES",
        "stability_kind": "TEMPORAL_ATTRACTOR_STABILITY",
        "law_origin_status": "DERIVED_BY_SEPARATE_FROZEN_GATE",
    }
    for key, bad_value in metadata_bad_values.items():
        mutant = dict(metadata)
        mutant[key] = bad_value
        metadata_mutation_controls[key] = not local_candidate_promotion_valid(
            candidate_fact_evidence, PROMOTION_POLICY, mutant
        )

    semantic_profile_mutations = {
        "fixed_basis_or_direct_sum_roles": (
            {"fixed_basis_or_direct_sum_roles_used": True},
            ("intrinsic_differentiation_certified",),
        ),
        "equal_rank_roles": (
            {"role_ranks": [1, 1]},
            (
                "intrinsic_differentiation_certified",
                "inequivalence_survives_full_quotient",
            ),
        ),
        "wrong_distinct_role_ranks": (
            {"role_ranks": [1, 3]},
            (
                "intrinsic_differentiation_certified",
                "inequivalence_survives_full_quotient",
            ),
        ),
        "full_equivalence_role_swap": (
            {"full_declared_equivalence_can_swap_roles": True},
            ("inequivalence_survives_full_quotient",),
        ),
        "arbitrary_spectral_decomposition": (
            {
                "law_forces_selected_role_pattern": False,
                "arbitrary_spectral_decomposition_used": True,
            },
            ("law_relevance_not_arbitrary_decomposition",),
        ),
        "Q_sign_declared_gauge": (
            {"Q_sign_is_gauge": True},
            ("inequivalence_survives_full_quotient",),
        ),
        "preferred_representative_direction": (
            {"representative_direction_selected": True},
            ("realization_or_selection_noncircular",),
        ),
        "target_orbit_distance_or_posthoc_cubic": (
            {
                "target_orbit_distance_term_used": True,
                "post_output_cubic_or_sign_choice_used": True,
            },
            ("target_free_law_certified", "forbidden_target_intersection_empty"),
        ),
        "tuned_single_parameter_point": (
            {"parameter_support_is_open": False},
            ("open_domain_stability_and_robustness",),
        ),
        "unregistered_higher_invariant_law": (
            {"unregistered_higher_invariant_added": True},
            (
                "live_identity_and_dependencies_exact",
                "complete_one_foundation_primitive_freedom_registry",
            ),
        ),
        "N3_called_space_or_O3_rotation_or_delta_metric": (
            {
                "N3_called_physical_space": True,
                "O3_called_physical_rotation": True,
                "delta_called_spacetime_metric": True,
            },
            ("foundation_admissibility_and_import_health",),
        ),
        "Hessian_called_temporal_formation": (
            {"Hessian_called_temporal_formation": True},
            ("f1_only_scope_honest",),
        ),
        "route_label_without_obligations": (
            {"route_obligations_satisfied": False},
            ("router_extension_aligned",),
        ),
        "missing_functional_ownership": (
            {"functional_ownership_complete": False},
            ("complete_one_foundation_primitive_freedom_registry",),
        ),
    }
    semantic_null_controls: dict[str, bool] = {}
    for name, (updates, failed_gates) in semantic_profile_mutations.items():
        mutant_profile = copy.deepcopy(SEMANTIC_ADJUDICATION_PROFILE)
        mutant_profile.update(updates)
        mutant_evidence = semantic_profile_to_evidence(
            preliminary_evidence,
            mutant_profile,
            independently_derived_role_ranks,
        )
        semantic_null_controls[name] = all((
            all(mutant_evidence[gate] is False for gate in failed_gates),
            all_validators_reject(mutant_evidence),
        ))

    import_mutants: list[dict[str, Any]] = []
    missing_functional = copy.deepcopy(NORMALIZED_IMPORT_OWNERSHIP)
    missing_functional.pop("quartic_invariant_functional_form_signs_and_truncation")
    import_mutants.append(missing_functional)
    derived_functional = copy.deepcopy(NORMALIZED_IMPORT_OWNERSHIP)
    derived_functional["quartic_invariant_functional_form_signs_and_truncation"][
        "origin"
    ] = "DERIVED_BY_THIS_GATE"
    import_mutants.append(derived_functional)
    spatial_N3 = copy.deepcopy(NORMALIZED_IMPORT_OWNERSHIP)
    spatial_N3["Sym0_3_R_internal_configuration_space"]["allowed_meaning"] = (
        "physical three-space"
    )
    import_mutants.append(spatial_N3)
    hidden_functional_source = copy.deepcopy(NORMALIZED_IMPORT_OWNERSHIP)
    hidden_functional_source["quartic_invariant_functional_form_signs_and_truncation"][
        "declared_at"
    ] = "added after w2_06 output"
    import_mutants.append(hidden_functional_source)
    import_mutations_rejected = all(
        not normalized_imports_valid(mutant, module_06)
        for mutant in import_mutants
    )

    registry_mutation_controls: dict[str, bool] = {}
    target_ledger_bundle = copy.deepcopy(own_bundle)
    target_ledger_bundle["INVARIANT_LAW_LEDGER"]["frozen_functional"] = (
        "V plus distance to desired rank-1/rank-2 target orbit"
    )
    registry_mutation_controls["invariant_target_orbit_law_rejected"] = (
        not registry_bundle_valid(target_ledger_bundle)
    )
    removed_output_bundle = copy.deepcopy(own_bundle)
    removed_output_bundle["OUTPUT_CLASSIFICATION"].pop("negative_stationary_root")
    registry_mutation_controls["incomplete_output_classification_rejected"] = (
        not registry_bundle_valid(removed_output_bundle)
    )
    downstream_bundle = copy.deepcopy(own_bundle)
    downstream_bundle["SCOPE_FIREWALL"]["physical_space_dimension_or_continuum"] = True
    registry_mutation_controls["downstream_scope_closure_rejected"] = (
        not registry_bundle_valid(downstream_bundle)
    )
    score_bundle = copy.deepcopy(own_bundle)
    score_bundle["PROMOTION_POLICY"]["numeric_score_used"] = True
    registry_mutation_controls["score_policy_rejected"] = not registry_bundle_valid(
        score_bundle
    )
    semantic_profile_bundle = copy.deepcopy(own_bundle)
    semantic_profile_bundle["SEMANTIC_ADJUDICATION_PROFILE"][
        "N3_called_physical_space"
    ] = True
    registry_mutation_controls["semantic_profile_drift_rejected"] = (
        not registry_bundle_valid(semantic_profile_bundle)
    )

    controls_pass = all((
        all(gate_mutation_controls.values()),
        extra_gate_rejected,
        all(policy_mutation_controls.values()),
        extra_policy_rejected,
        all(metadata_mutation_controls.values()),
        all(semantic_null_controls.values()),
        import_mutations_rejected,
        all(registry_mutation_controls.values()),
    ))
    promotion_evidence = dict(candidate_fact_evidence)
    promotion_evidence["independent_crosscheck_and_controls"] = all((
        candidate_fact_evidence["independent_crosscheck_and_controls"],
        controls_pass,
    ))

    validator_results = validator_results_for(promotion_evidence)
    raw_candidate_promoted = raw_validator_promotion(validator_results)
    validators_agree_with_exact_AND = validator_consensus_valid(
        promotion_evidence, validator_results
    )

    expected_algebra_check_keys = {
        "traceless_three_by_three_Cayley_Hamilton_exact",
        "degree_four_invariant_reduces_to_I2_squared",
        "O3_invariant_ring_generation_theorem_scope_explicit",
        "all_invariant_monomials_through_degree_four_enumerated",
        "frozen_same_order_invariant_ledger_exact",
        "amplitude_is_intrinsic_state_invariant",
        "Q_generated_projectors_exact",
        "rank_and_trace_prevent_O3_exchange",
        "positive_stationary_root_exact",
        "radial_normal_eigenvalue_positive_certificate",
        "biaxial_normal_eigenvalue_positive_certificate",
        "role_exchange_is_Q_sign_and_not_law_symmetry",
    }
    algebra_audit_schema_exact = all((
        isinstance(algebra_audit, dict),
        set(algebra_audit) == {"CHECKS", "DIAGNOSTICS"},
        isinstance(algebra_audit.get("CHECKS"), dict),
        set(algebra_audit.get("CHECKS", {})) == expected_algebra_check_keys,
        all(
            type(value) is bool
            for value in algebra_audit.get("CHECKS", {}).values()
        ),
        isinstance(algebra_audit.get("DIAGNOSTICS"), dict),
    ))
    overlay_contract_schema_exact = all((
        set(overlay.get("imports_to_declare", ())) == expected_overlay_imports,
        set(overlay.get("must_derive", ())) == set(OVERLAY_OBLIGATION_MAP),
    ))
    candidate_facts = {
        "candidate_primitive_and_freedom_registry_complete": candidate_registry_complete,
        "independent_invariant_and_projector_consequences_exact": independent_algebra_exact,
        "forbidden_target_and_future_semantics_firewall_exact": forbidden_target_firewall,
        "output_classification_and_boundaries_complete": output_classification_complete,
        "overlay_imports_satisfied": overlay_imports_satisfied,
        "overlay_must_derive_obligations_satisfied": overlay_derivations_satisfied,
        "semantic_profile_schema_valid": semantic_profile_schema_valid(
            SEMANTIC_ADJUDICATION_PROFILE
        ),
        "semantic_role_ranks_cross_bound_to_independent_projectors": all((
            exact_tree(
                SEMANTIC_ADJUDICATION_PROFILE["role_ranks"],
                independently_derived_role_ranks,
            ),
            independently_derived_role_ranks == [1, 2],
        )),
    }

    all_true_evidence = {gate: True for gate in FROZEN_PROMOTION_GATES}
    one_failed_evidence = dict(all_true_evidence)
    one_failed_evidence["intrinsic_differentiation_certified"] = False
    all_true_validator_results = {
        key: True for key in VALIDATOR_RESULT_KEYS
    }
    all_false_validator_results = {
        key: False for key in VALIDATOR_RESULT_KEYS
    }
    decision_branch_controls = {
        "valid_promoted_branch_reachable": all((
            validator_consensus_valid(
                all_true_evidence, all_true_validator_results
            ),
            raw_validator_promotion(all_true_validator_results),
            effective_promotion(True, True),
            adjudication_status(True, True).startswith(
                "W2_06_PHYSICAL_F1_ADJUDICATION_COMPLETE__PROMOTED"
            ),
        )),
        "valid_not_promoted_branch_reachable": all((
            validator_consensus_valid(
                one_failed_evidence, all_false_validator_results
            ),
            raw_validator_promotion(all_false_validator_results) is False,
            effective_promotion(True, False) is False,
            adjudication_status(True, False).startswith(
                "W2_06_PHYSICAL_F1_ADJUDICATION_COMPLETE__NOT_PROMOTED"
            ),
            expected_runtime_closure(True, False)[
                "W2_06_OVERLAY_CLASS_EVALUATED"
            ] is True,
            expected_runtime_closure(True, False)[
                "W2_06_PROMOTED_TO_W2_F1"
            ] is False,
        )),
        "invalid_audit_can_never_export_promotion": all((
            effective_promotion(False, True) is False,
            adjudication_status(False, True)
            == "W2_06_PHYSICAL_F1_ADJUDICATION_INVALID__PROGRAMME_W2_F1_OPEN",
            expected_runtime_closure(False, True)[
                "W2_06_PROMOTED_TO_W2_F1"
            ] is False,
            not runtime_closure_valid(
                expected_runtime_closure(True, True), 1, True
            ),
        )),
    }
    decision_branch_map_mutation_controls = exact_true_map_mutation_controls(
        decision_branch_controls, EXPECTED_DECISION_BRANCH_KEYS
    )

    audit_checks = {
        "required_contract_and_custom_fields_exact": contract_fields_exact,
        "contract_values_nonempty": contract_values_nonempty,
        "contract_and_runtime_model_versions_bound": contract_model_bound,
        "contract_custom_fields_exactly_bound": contract_custom_bound,
        "whole_claim_contract_digest_and_types_exact": whole_claim_contract_exact,
        "static_contract_scope_freedom_and_flags_exact": static_contract_exact,
        "claim_method_conditions_falsifier_identity_zero_and_next_task_mutants_rejected": all(
            claim_contract_mutation_controls.values()
        ),
        "own_critical_registries_digest_bound": own_registries_exact,
        "source_boundary_phrases_present": source_boundaries_valid(texts),
        "dependency_bytes_exact_before_import": dependency_bytes_exact,
        "w2_06_direct_report_reexecuted_exact": report_06_exact,
        "w2_08_contract_report_reexecuted_exact": report_08_exact,
        "live_identity_and_transitive_provenance_exact": live_identity_exact,
        "predeclared_functional_ownership_normalized_without_new_assumption": import_ownership_exact,
        "independent_algebra_audit_schema_and_boolean_outputs_exact": algebra_audit_schema_exact,
        "overlay_contract_schema_exact": overlay_contract_schema_exact,
        "candidate_fact_registry_schema_and_boolean_outputs_exact": all((
            set(candidate_facts) == {
                "candidate_primitive_and_freedom_registry_complete",
                "independent_invariant_and_projector_consequences_exact",
                "forbidden_target_and_future_semantics_firewall_exact",
                "output_classification_and_boundaries_complete",
                "overlay_imports_satisfied",
                "overlay_must_derive_obligations_satisfied",
                "semantic_profile_schema_valid",
                "semantic_role_ranks_cross_bound_to_independent_projectors",
            },
            all(type(value) is bool for value in candidate_facts.values()),
        )),
        "all_18_promotion_evidence_values_are_exact_booleans": (
            promotion_evidence_schema_valid(promotion_evidence)
        ),
        "three_validators_agree_with_exact_AND_candidate_outcome": (
            validators_agree_with_exact_AND
        ),
        "every_missing_false_truthy_string_none_and_extra_gate_mutant_rejected": all((
            all(gate_mutation_controls.values()), extra_gate_rejected,
        )),
        "every_policy_true_truthy_falsey_none_missing_and_extra_mutant_rejected": all((
            all(policy_mutation_controls.values()), extra_policy_rejected,
        )),
        "candidate_specific_metadata_mutants_rejected": all(
            metadata_mutation_controls.values()
        ),
        "semantic_target_gauge_temporal_and_downstream_nulls_rejected": all(
            semantic_null_controls.values()
        ),
        "import_ownership_mutants_rejected": import_mutations_rejected,
        "registry_target_output_scope_and_score_mutants_rejected": all(
            registry_mutation_controls.values()
        ),
        "promoted_not_promoted_and_invalid_decision_branches_fail_closed": all(
            (
                exact_true_map(
                    decision_branch_controls, EXPECTED_DECISION_BRANCH_KEYS
                ),
                exact_true_map(
                    decision_branch_map_mutation_controls,
                    expected_true_map_mutation_control_keys(
                        EXPECTED_DECISION_BRANCH_KEYS
                    ),
                ),
            )
        ),
        "foundation_law_derivation_and_resonant_map_honestly_open": all((
            KNOWN_LIMITATIONS["foundation_law_origin"].startswith("OPEN_"),
            KNOWN_LIMITATIONS["RefG_resonant_environment_map"].startswith("OPEN_"),
            INITIAL_CLOSURE_FLAGS["FOUNDATION_LAW_DERIVED"] is False,
            INITIAL_CLOSURE_FLAGS["REFG_RESONANT_ENVIRONMENT_MAP"] is False,
        )),
    }
    audit_valid_before_closure = all(
        type(value) is bool and value is True
        for value in audit_checks.values()
    )

    provisional_closure = expected_runtime_closure(
        audit_valid_before_closure, raw_candidate_promoted
    )
    closure_baseline_valid = runtime_closure_valid(
        provisional_closure, audit_valid_before_closure, raw_candidate_promoted
    )
    closure_mutation_controls: dict[str, bool] = {}
    for key, value in provisional_closure.items():
        opposite = dict(provisional_closure)
        opposite[key] = not value
        nonboolean = dict(provisional_closure)
        nonboolean[key] = 1 if value is False else 0
        missing = dict(provisional_closure)
        missing.pop(key)
        closure_mutation_controls[key] = all((
            not runtime_closure_valid(
                opposite, audit_valid_before_closure, raw_candidate_promoted
            ),
            not runtime_closure_valid(
                nonboolean, audit_valid_before_closure, raw_candidate_promoted
            ),
            not runtime_closure_valid(
                missing, audit_valid_before_closure, raw_candidate_promoted
            ),
        ))
    extra_closure = dict(provisional_closure)
    extra_closure["GR_BRIDGE_AUTOMATICALLY_CLOSED"] = False
    extra_closure_rejected = not runtime_closure_valid(
        extra_closure, audit_valid_before_closure, raw_candidate_promoted
    )
    closure_controls_pass = all((
        closure_baseline_valid,
        all(closure_mutation_controls.values()),
        extra_closure_rejected,
    ))
    audit_checks[
        "runtime_closure_missing_extra_opposite_and_nonboolean_mutants_rejected"
    ] = closure_controls_pass
    audit_key_control_name = (
        "audit_check_keyset_missing_extra_false_and_nonboolean_mutants_rejected"
    )
    audit_checks[audit_key_control_name] = True
    audit_check_map_mutation_controls = exact_true_map_mutation_controls(
        audit_checks, EXPECTED_AUDIT_CHECK_KEYS
    )
    audit_checks[audit_key_control_name] = exact_true_map(
        audit_check_map_mutation_controls,
        expected_true_map_mutation_control_keys(EXPECTED_AUDIT_CHECK_KEYS),
    )

    audit_integrity_valid = exact_true_map(
        audit_checks, EXPECTED_AUDIT_CHECK_KEYS
    )
    closure_flags = expected_runtime_closure(
        audit_integrity_valid, raw_candidate_promoted
    )
    closure_self_consistent = runtime_closure_valid(
        closure_flags, audit_integrity_valid, raw_candidate_promoted
    )
    final_audit_valid = bool(audit_integrity_valid and closure_self_consistent)
    if not final_audit_valid:
        closure_flags = expected_runtime_closure(False, raw_candidate_promoted)
    effective_promoted = effective_promotion(
        final_audit_valid, raw_candidate_promoted
    )
    status = adjudication_status(final_audit_valid, raw_candidate_promoted)

    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": status,
        "PROMOTION_CONTRACT_VERSION": PROMOTION_CONTRACT_VERSION,
        "ROUTER_VERSION": ROUTER_VERSION,
        "CANDIDATE_ID": CANDIDATE_ID,
        "ROUTE_CLASS": ROUTE_CLASS,
        "WITNESS_KIND": WITNESS_KIND,
        "STABILITY_KIND": STABILITY_KIND,
        "LAW_ORIGIN_STATUS": LAW_ORIGIN_STATUS,
        "AUDIT_CHECKS": audit_checks,
        "AUDIT_VALID": final_audit_valid,
        "CANDIDATE_FACTS": candidate_facts,
        "PROMOTION_EVIDENCE": promotion_evidence,
        "RAW_VALIDATOR_PROMOTION": raw_candidate_promoted,
        "PROMOTED": effective_promoted,
        "PROMOTION_CEILING": (
            "STRUCTURAL_SELF_DIFFERENTIATION_RELATIVE_TO_DECLARED_IMPORTED_PRIMITIVES; "
            "not foundation-law derivation, F2, time, modes, geometry, action, GR or observation"
        ),
        "NORMALIZED_IMPORT_OWNERSHIP": NORMALIZED_IMPORT_OWNERSHIP,
        "INVARIANT_LAW_LEDGER": INVARIANT_LAW_LEDGER,
        "INDEPENDENT_ALGEBRA_AUDIT": algebra_audit,
        "OUTPUT_CLASSIFICATION": OUTPUT_CLASSIFICATION,
        "OVERLAY_OBLIGATION_MAP": OVERLAY_OBLIGATION_MAP,
        "KNOWN_LIMITATIONS": KNOWN_LIMITATIONS,
        "SCOPE_FIREWALL": SCOPE_FIREWALL,
        "PROMOTION_POLICY": PROMOTION_POLICY,
        "SEMANTIC_ADJUDICATION_PROFILE": SEMANTIC_ADJUDICATION_PROFILE,
        "VALIDATOR_RESULTS": validator_results,
        "DECISION_BRANCH_CONTROLS": decision_branch_controls,
        "DECISION_BRANCH_MAP_MUTATION_CONTROLS": (
            decision_branch_map_mutation_controls
        ),
        "AUDIT_CHECK_MAP_MUTATION_CONTROLS": audit_check_map_mutation_controls,
        "CLAIM_CONTRACT_MUTATION_CONTROLS": claim_contract_mutation_controls,
        "GATE_MUTATION_CONTROLS": gate_mutation_controls,
        "POLICY_MUTATION_CONTROLS": policy_mutation_controls,
        "METADATA_MUTATION_CONTROLS": metadata_mutation_controls,
        "SEMANTIC_NULL_CONTROLS": semantic_null_controls,
        "REGISTRY_MUTATION_CONTROLS": registry_mutation_controls,
        "CLOSURE_MUTATION_CONTROLS": closure_mutation_controls,
        "FALLBACK_STATUS": {
            "symmetric_seed_route": "OPEN_NOT_REJECTED",
            "atemporal_nonunique_solution_structure": "OPEN_NOT_REJECTED",
            "all_other_nonfalsified_routes": "OPEN_NOT_REJECTED",
        },
        "NEXT_ATOMIC_TASK": NEXT_ATOMIC_TASK,
        "CLAIM_CONTRACT_SHA256_EXPECTED": EXPECTED_CLAIM_CONTRACT_SHA256,
        "CLAIM_CONTRACT_SHA256_LIVE": canonical_sha256(CLAIM_CONTRACT),
        "GATE_APPLICABILITY": GATE_APPLICABILITY,
        "CLOSURE_FLAGS": closure_flags,
        "DEPENDENCY_SHA256_EXPECTED": EXPECTED_DEPENDENCY_SHA256,
        "PROVENANCE": {name: sha256(path) for name, path in paths.items()},
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["STATUS"].startswith(
        "W2_06_PHYSICAL_F1_ADJUDICATION_COMPLETE"
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
