"""Route-neutral physical W2-F1 promotion contract and router overlay.

This file freezes what programme-level self-differentiation means before the
selected w2_06 candidate is evaluated.  It also versions the route taxonomy so
that one unique quotient state may contain canonical, coexisting and
nonexchangeable internal roles.  It does not promote w2_06 and leaves every
physical W2 flag false.  Candidate adjudication belongs to w2_09.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


MODEL_VERSION = "W2-F1-PHYSICAL-PROMOTION-CONTRACT-v1.0-internal"
ROUTER_VERSION = "W2-F1-ROUTE-TAXONOMY-v2.0-internal"
NEW_ROUTE_CLASS = "atemporal_intrastate_invariant_role_structure"
W2_06_CANDIDATE_ID = "W2_F1_ATEMPORAL_SPECTRAL_SPLIT_CANDIDATE_001"

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
    "ROUTER_VERSION", "F1_DEFINITION", "F1_ROLE_SEMANTICS",
    "WITNESS_KINDS", "PROMOTION_AND_GATES", "PRIMITIVE_LAW_POLICY",
    "ROUTE_SUPPORT_POLICIES", "BASE_ROUTE_TAXONOMY_V1",
    "ROUTE_TAXONOMY_OVERLAY_V2", "EFFECTIVE_ROUTE_TAXONOMY_V2",
    "CANDIDATE_CLASSIFICATION", "CANDIDATE_EVALUATION_TEMPLATE",
    "W2_06_PREAUDIT_LEDGER", "FORBIDDEN_PROMOTION_SHORTCUTS",
    "DEFERRED_OUTPUTS", "SUPERSESSION_SCOPE", "REGISTRY_SHA256", "NEXT_AUDIT",
})

WITNESS_KINDS = {
    "INTER_CLASS_INEQUIVALENT_OUTCOMES": (
        "several accepted stable outcomes survive the full declared equivalence"
    ),
    "INTRA_CLASS_CANONICAL_ROLES": (
        "one accepted equivalence class contains at least two canonical, coexisting, "
        "nonexchangeable internal roles"
    ),
}

F1_DEFINITION = {
    "route_neutral_core": (
        "A fully declared target-free law of one pre-spatiotemporal foundation yields, "
        "on nonzero declared support, a structurally stable accepted structure with "
        "nontrivial intrinsic differentiation that was absent from the undifferentiated input."
    ),
    "inter_class_route": "multiple inequivalent accepted outcomes may witness differentiation",
    "intra_class_route": (
        "one unique quotient state may witness differentiation through canonical coexisting "
        "roles; multiple vacua or quotient solutions are not required"
    ),
    "physical_ceiling": (
        "F1 establishes candidate-level intrinsic roles only; operational distinction, nodes, "
        "relations, time, locality, modes, spacetime and observables remain later gates"
    ),
    "proof_strength": "STRUCTURAL_SELF_DIFFERENTIATION_RELATIVE_TO_FROZEN_PRIMITIVES",
}

F1_ROLE_SEMANTICS = {
    "generated_from_output": (
        "roles or outcomes are functorial/canonical functions of the accepted state and law, "
        "not fixed basis vectors, labels or an input direct-sum partition"
    ),
    "absent_at_reference": (
        "the undifferentiated reference has no nontrivial canonical role witness; a route "
        "without a distinguished reference must prove the same no-preloading statement"
    ),
    "full_equivalence": (
        "no allowed gauge, relabel or automorphism exchanges the claimed inequivalent roles"
    ),
    "intrinsic_invariant": (
        "inequivalence is certified by an intrinsic invariant without downstream semantic labels"
    ),
    "law_relevance": (
        "the accepted-law classification forces the role pattern on the declared support; "
        "arbitrary decomposition or projector algebra alone is insufficient"
    ),
    "structural_stability": (
        "the witness persists under the route's declared admissible perturbations; this is not "
        "a temporal formation or persistence claim unless a separate evolution law exists"
    ),
}

PROMOTION_AND_GATES = {
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

PRIMITIVE_LAW_POLICY = {
    "allowed_origin_statuses": [
        "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
        "DERIVED_BY_SEPARATE_FROZEN_GATE",
    ],
    "no_infinite_regress": (
        "F1 may derive a mechanism relative to honestly frozen primitives; it need not derive "
        "every primitive law from a deeper law"
    ),
    "primitive_admissibility": (
        "an imported law is admissible only if it is predeclared, target-free, uniform, "
        "noncircular, accompanied by its complete freedom ledger and tested on an open domain"
    ),
    "argmin_guard": (
        "a unique global argmin does not derive its own law: target orbit/projector/direction/rank, "
        "post-output term selection, tuned coefficient point and hidden tie-breaker are forbidden"
    ),
    "status_ceiling": (
        "an imported admissible law remains IMPORTED_NOT_DERIVED even when its consequences are exact"
    ),
}

ROUTE_SUPPORT_POLICIES = {
    "symmetric_instability_or_bifurcation": (
        "open parameter domain, symmetry-respecting seed/outcome law, nonzero-measure basin and "
        "declared dynamical stability"
    ),
    "atemporal_nonunique_solution_structure": (
        "multiple inequivalent stable quotient solutions and a noncircular physical selection account"
    ),
    NEW_ROUTE_CLASS: (
        "one selected quotient class with canonical coexisting roles, full-quotient "
        "nonexchangeability, open-domain structural stability and no representative selection"
    ),
    "stochastic_or_quantum_outcome": (
        "internally defined symmetric probability/state, nonzero outcome support and no preferred injection"
    ),
    "state_space_generating_rule": (
        "nontrivial generated states, termination/consistency and nonzero declared generative support"
    ),
    "nontrivial_relational_state_space": (
        "stable inequivalent relational sectors under the full relabel equivalence"
    ),
    "other_explicit_target_free_mechanism": (
        "complete primitive/rule registry, stable target-free inequivalence and noncircular health"
    ),
}

BASE_ROUTE_TAXONOMY_V1 = {
    "symmetric_instability_or_bifurcation": {
        "imports_to_declare": ["configuration_space", "nontrivial_symmetry", "symmetric_branch", "invariant_rule"],
        "must_derive": ["open_domain_instability", "stable_inequivalent_branch", "target_free_selection_or_seed_account"],
    },
    "atemporal_nonunique_solution_structure": {
        "imports_to_declare": ["solution_space", "equivalence_rule", "self_consistency_law"],
        "must_derive": ["inequivalent_stable_solutions", "noncircular_physical_selection_account"],
    },
    "stochastic_or_quantum_outcome": {
        "imports_to_declare": ["state_space", "symmetric_probability_or_state", "outcome_rule"],
        "must_derive": ["internal_not_external_outcomes", "stable_inequivalence", "no_preferred_outcome_injection"],
    },
    "state_space_generating_rule": {
        "imports_to_declare": ["generative_grammar", "equivalence_rule"],
        "must_derive": ["nontrivial_generated_states", "stable_inequivalence", "termination_or_consistency"],
    },
    "nontrivial_relational_state_space": {
        "imports_to_declare": ["relational_state_space", "relabel_equivalence", "law"],
        "must_derive": ["stable_inequivalent_relational_sectors", "no_node_or_trace_preloading"],
    },
    "other_explicit_target_free_mechanism": {
        "imports_to_declare": ["complete_primitive_and_rule_registry"],
        "must_derive": ["stable_target_free_inequivalent_differentiation", "noncircularity_and_health"],
    },
}

ROUTE_TAXONOMY_OVERLAY_V2 = {
    NEW_ROUTE_CLASS: {
        "imports_to_declare": [
            "one_foundation_internal_state_space",
            "complete_equivalence_and_automorphism_rule",
            "undifferentiated_reference_or_no_preloading_certificate",
            "target_free_atemporal_selection_or_consistency_law",
            "declared_structural_stability_criterion_and_parameter_domain",
        ],
        "must_derive": [
            "complete_selected_quotient_classification",
            "canonical_state_generated_coexisting_roles",
            "intrinsic_role_invariant",
            "nonexchangeability_after_full_quotient",
            "law_relevance_not_arbitrary_decomposition",
            "open_domain_structural_stability",
            "no_representative_orientation_or_role_selection",
            "noncircular_law_and_foundation_admissibility",
        ],
    }
}

EFFECTIVE_ROUTE_TAXONOMY_V2 = {
    **copy.deepcopy(BASE_ROUTE_TAXONOMY_V1),
    **copy.deepcopy(ROUTE_TAXONOMY_OVERLAY_V2),
}

CANDIDATE_CLASSIFICATION = {
    "candidate_claim_id": W2_06_CANDIDATE_ID,
    "historical_w2_03_label": "atemporal_nonunique_solution_structure",
    "historical_label_status": "PRESENCE_ONLY__CONTRACT_NOT_SATISFIED",
    "effective_v2_class": NEW_ROUTE_CLASS,
    "witness_kind_for_w2_09": "INTRA_CLASS_CANONICAL_ROLES",
    "stability_kind_for_w2_09": "ATEMPORAL_VARIATIONAL_STRUCTURAL",
    "current_evidence_status": "CONDITIONAL_EXACT_INTERNAL_ROLE_CERTIFICATE_RETAINED",
    "promotion_status": "NOT_EVALUATED__PROGRAMME_W2_F1_OPEN",
}

CANDIDATE_EVALUATION_TEMPLATE = {
    key: "OPEN__TO_BE_ADJUDICATED_IN_W2_09" for key in PROMOTION_AND_GATES
}

W2_06_PREAUDIT_LEDGER = {
    "conditional_exact_mathematics": "AVAILABLE_FROM_FROZEN_W2_06_AND_W2_07",
    "route_neutral_F1_semantics": "FROZEN_HERE__NOT_YET_APPLIED",
    "overlay_class_contract": "DEFINED_HERE__NOT_YET_EVALUATED",
    "primitive_foundation_admissibility": "OPEN",
    "argmin_law_noncircularity": "OPEN",
    "law_relevance_of_internal_roles": "OPEN",
    "declared_scope_robustness": "OPEN",
    "N1_N2_N4_and_general_N_controls": "OPEN__MUST_BE_REEXECUTED_IN_W2_09",
    "N3_O3_delta_matrix_Qsign_and_1plus2_import_origin": (
        "OPEN__NO_GEOMETRY_DIMENSION_OR_RANK_BONUS_ALLOWED"
    ),
    "b0_polarity_coercivity_and_forbidden_source_controls": (
        "OPEN__MUST_BE_REEXECUTED_IN_W2_09"
    ),
    "programme_W2_F1": "OPEN",
}

FORBIDDEN_PROMOTION_SHORTCUTS = {
    "candidate_specific_definition": "N=3, 1+2, rank, Q, projector or argmin cannot define route-neutral F1",
    "future_geometry_laundering": "internal N=3/O(3)/delta or 1+2 cannot mean space, rotation, metric or 3+1",
    "mere_decomposition": "fixed basis, arbitrary direct sum or projector identities alone cannot close F1",
    "gauge_multiplicity": "gauge/relabel representatives cannot be called physically different",
    "argmin_self_justification": "unique argmin cannot prove the origin or admissibility of its own law",
    "tuned_or_posthoc_rule": "one tuned point, target-distance functional or post-result term is forbidden",
    "structural_to_temporal": "positive Hessian cannot be called formation, evolution or temporal persistence",
    "F2_plus_borrowing": "node, trace, relation, clock, mode, dimension, metric, action or GR cannot close F1",
    "partial_AND_or_score": "no score, weight, check count or compensation can replace one missing gate",
    "route_class_laundering": "presence in a registry or local rename is not route-contract satisfaction",
    "fallback_rejection": "priority or promotion audit cannot reject a nonfalsified alternative",
}

DEFERRED_OUTPUTS = (
    "operational_node_trace_relation", "internal_causal_order_or_clock",
    "independent_additive_modes", "physical_space_dimension_or_continuum",
    "Lorentzian_metric_or_light_cone", "effective_action_and_DOF_health",
    "energy_pressure_mass_particle_or_oscillon", "observable_or_data_map",
    "Einstein_GR_PN_PPN_or_compact_source_handoff",
)

SUPERSESSION_SCOPE = {
    "historical_w2_03": "remains valid as the v1 route-source contract and is not rewritten",
    "taxonomy_authority": (
        "ROUTER_VERSION is the exact v2 superset used by w2_09 and later F1 promotion audits"
    ),
    "historical_w2_06_registration_check": (
        "retained as presence-only history; it is not proof of v1 or v2 class satisfaction"
    ),
    "historical_w2_07_priority": "retained; audit priority is not physical promotion",
    "fallbacks": "every nonfalsified route remains open",
}

PROMOTION_POLICY_DEFAULTS = {
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

ALLOWED_LAW_ORIGIN_STATUSES = frozenset(
    PRIMITIVE_LAW_POLICY["allowed_origin_statuses"]
)

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
    "W2_F1_SELF_DIFFERENTIATION": False,
    "W2_F2_OPERATIONAL_RELATIONS": False,
    "W2_F3_INTERNAL_ORDER_CAUSALITY": False,
    "W2_F4_INDEPENDENT_ADDITIVE_MODES": False,
    "W2_M1_DIMENSION_CONTINUUM": False,
    "W2_M2_LORENTZIAN_METRIC": False,
    "W2_A0_EFFECTIVE_ACTION_ORIGIN": False,
}

GATE_APPLICABILITY = {
    "G0_GOAL": "REQUIRED — route-neutral F1 definition, witness kinds and AND gate are frozen",
    "G1_CONVENTIONS": "REQUIRED — pre-spatial scope, equivalence, primitive-law and status meanings are frozen",
    "G2_CORE_ALGEBRA": "N/A — no candidate algebra is evaluated in this definition/router contract",
    "G3_STRUCTURE": "REQUIRED — route taxonomy v2, overlay class and w2_06 classification are checked",
    "G4_INDEPENDENT_CHECK": "REQUIRED — live dependency binding plus INTER/INTRA positive controls",
    "G5_LIMITS_REGRESSION": "REQUIRED — partial-AND, target, class, temporal and downstream mutants",
    "G6_PHYSICAL_MATCH": "N/A — w2_06 physical promotion is explicitly deferred to w2_09",
    "G7_OBSERVATION": "N/A — no observable or data comparison exists at this contract stage",
    "G8_EXPORT": "N/A — internal Git-ignored contract; no Canon/article export authorized",
}

EXPECTED_BRANCHES = {
    "definition_and_router_contract": "FROZEN_IF_GATE_PASSES",
    "w2_06_physical_promotion": "OPEN__DEFERRED_TO_W2_09",
    NEW_ROUTE_CLASS: "VERSIONED_OVERLAY_CLASS__CONTRACT_NOT_YET_EVALUATED",
    "atemporal_nonunique_solution_structure": "OPEN_DISTINCT_CLASS__NOT_REJECTED",
    "symmetric_seed_route": "OPEN_FALLBACK__NOT_REJECTED",
    "all_other_nonfalsified_routes": "OPEN__NOT_REJECTED",
    "programme_W2_F1": "OPEN__MUST_REMAIN_FALSE_IN_W2_08",
}

EXPECTED_DEPENDENCY_SHA256 = {
    "CODES": "49d8e818f269621f31016f8ef8decabe000f01c442c45fe7a16c4906b61c1309",
    "CANON": "bf5cabae190821d1c0ffb342d3cdf101f13be5386ea993bb60fce4098f18d756",
    "INTUITIVE": "7e69e62c36c8cc25540e0a0465f3b74300693ca1bd868e54b4b349d5b9547981",
    "W2_C0": "640debaea5265d63a660fed4bacd9a2a99c2152535737003272e178efc1c5b6c",
    "W2_03": "a62b4cbf60f135c2111944a1729d4f5ff296edf208269d6137c1a771e588b449",
    "W2_04": "1bd4663ea4e644f14d4605d9abd6a52581343bbbfb7746b907af0cffdd40b81b",
    "W2_05": "ba61ed421e15c7695275de419686998bcdbb9ef03b96ef7d52c9e3e89eee1aaa",
    "W2_06": "8998aa7ee0dda8e3a882e660486a850d86f8d30a55791e81ff3088b9c9bf4d8b",
    "W2_07": "144822478a3435fdb90cf5854971bcf5e91082d6caf300a7238d218475b77b64",
}

EXPECTED_REGISTRY_SHA256 = {
    "WITNESS_KINDS": "b8c2f5d6ecc5f95decadb8840b7801c9a5c73a2ef715b696234e49f1591e8bfe",
    "F1_DEFINITION": "2121d8b2e0f92836bc760c688f0d110f7c871926da3418dd2142ef2c9b4d46d8",
    "F1_ROLE_SEMANTICS": "85f5e98c00c57bf4cc41931a9e8ff0733b65eb17a1d24f798f29e7bf1d914879",
    "PROMOTION_AND_GATES": "089d50b51f57d3329e76af479d44b5c91fb525e75fe180e29a7dc9159a753d2b",
    "PRIMITIVE_LAW_POLICY": "a1945697c49f21e71b59c4f90860f3d5ce849c5886e11dce5c41fbb295f4662b",
    "ROUTE_SUPPORT_POLICIES": "a350634d31a990c890080e855a69c23c6d127a548b675ce06bdbf243989257c1",
    "BASE_ROUTE_TAXONOMY_V1": "17b6d279c7b9be7cc1e392ed6ab9673e2f971a76bcca73db889b13beb42f0dfd",
    "ROUTE_TAXONOMY_OVERLAY_V2": "6466d25078b28b6a8efb32ea166cdfbbbe0fc21b90f164f9cf554aff195db275",
    "EFFECTIVE_ROUTE_TAXONOMY_V2": "4c154b927414c110e3642d1a78f6f663b53961095370313d646c23c65b5eedd5",
    "CANDIDATE_CLASSIFICATION": "0587ff98197af7a102d59d4dc00dfeee60caca01d16921f12a7d2a4280eb6998",
    "CANDIDATE_EVALUATION_TEMPLATE": "b0895b8a0a4b9740105ff6aee3e926a516064801fddbbe13859eea64362eed17",
    "W2_06_PREAUDIT_LEDGER": "49441a54dc76ec835c1b24e22d40c5e483c15520e01841b332a43c2a7cdc7769",
    "FORBIDDEN_PROMOTION_SHORTCUTS": "61058c93482cfb3b176766ef6ddccbd6bc9086a192b526e2b08026257a41e0b3",
    "DEFERRED_OUTPUTS": "4680c15ec8e81fd5b816ef86be6a02977150c35cf48f5da240e3c9148cdf9dfc",
    "SUPERSESSION_SCOPE": "e25494afc22e45c7a5661745fbe26dd2095d56a0e850065d4d107663195dc3d6",
    "PROMOTION_POLICY_DEFAULTS": "7b3a734c485616e138d2a512d35b8c75877604f625f1c3382fd21703f9dbe4e3",
    "INITIAL_CLOSURE_FLAGS": "e3938694c9b89530460831eb6596bafb230c558d03067d518ad7dd8226683557",
    "GATE_APPLICABILITY": "1f7cf1b44f4be5e36c9451b1499532bf67123ca1030d8b4e3f94523026781670",
    "EXPECTED_BRANCHES": "d962c8432fac54b8c56d223e4e6ba78f25531b23d4bcf41272b822a2c0ee8201",
}

EXPECTED_W2_07_REPORT_SHA256 = {
    "CHECK_KEYS": "1808d28c48ce63e2022cc7dc92dd54e09e47d787fde96e0a4201d4030911361f",
    "CLOSURE_FLAGS": "3ca3a66a67b2399d0411b2aa8fa7ef00cf7962bda07e70c8acc22b3b05c6f860",
    "DEPENDENCY_STATUSES": "d9f6efe350592f9eccc34d23be9cfb25e61824f55f411b4027c55f097e214cae",
    "DEPENDENCY_VERSIONS": "7a4ae5966497abaaa50d32e4b2427fbdec79b57a466591afc98671090cb22043",
    "ROUTE_CLASSIFICATION": "578573e23c4ef2c45ae9b5d8e51f8a1b267e8496c26cb6f14b4f029ce295e4da",
    "ATEMPORAL_OBLIGATION_MAP": "87b597d0053dd0430c46d77bb263366241872b405d042e103a7999bdeadf9c4a",
}

CLAIM_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F1_PHYSICAL_PROMOTION_CONTRACT_001",
    "CLAIM": (
        "W2_F1-ის route-neutral მნიშვნელობა უშვებს როგორც რამდენიმე არაეკვივალენტურ "
        "შედეგს, ისე ერთი უნიკალური quotient-მდგომარეობის შიგნით კანონიკურად მიღებულ, "
        "თანაარსებულ და სრული ეკვივალენტობის შემდეგაც შეუცვლელ როლებს; ეს ფაილი მხოლოდ "
        "ამ promotion-კრიტერიუმსა და route-taxonomy v2-ს ყინავს და w2_06-ს ჯერ არ აფასებს."
    ),
    "TYPE": "DEFINITION / VERSIONED ROUTER EXTENSION / PROMOTION CONTRACT; არა physical F1 PASS",
    "MODEL_VERSION": (
        f"{MODEL_VERSION}; any definition, witness, gate, route class, law policy or PASS logic "
        "change requires a new version and reopens w2_09"
    ),
    "ASSUMPTIONS": [
        "F1 ნიშნავს intrinsic stable differentiation-ს; operational relation იწყება F2-ში.",
        "ერთი quotient-მდგომარეობის შიდა კანონიკური როლები ლოგიკურად განსხვავდება რამდენიმე quotient-ამონახსნისგან.",
        "ფუძის კანონი შეიძლება იყოს პატიოსნად გამოცხადებული პრიმიტივი; მისი შედეგი ამ პრიმიტივის მიმართ გამოითვლება.",
        "w2_06-ის ზუსტი მათემატიკა ინარჩუნებს conditional სტატუსს და აქ ფიზიკურ promotion-ს არ იღებს.",
        "დაკვირვებითი თავსებადობა რჩება საბოლოო უცვლელ ვეტოდ, თუმცა ამ წინაფიზიკურ კარიბჭეში data role N/A-ა.",
    ],
    "DOMAIN": (
        "W2_F1 promotion-ის განსაზღვრება, witness-ტიპები, route taxonomy და მომავალი w2_09 "
        "აუდიტის exact AND-კარიბჭე; არ მოიცავს F2-ს, სივრცე-დროს, მოქმედებას, GR-ს ან მონაცემებს."
    ),
    "CONVENTIONS": (
        "quotient ნიშნავს სრული გამოცხადებული gauge/relabel equivalence-ის კლასს; INTRA_CLASS "
        "ნიშნავს ერთ კლასში თანაარსებულ კანონიკურ როლებს; structural stability არ ნიშნავს "
        "საათურ persistence-ს; physical F1 აქ არის პროგრამული ატომური კარიბჭე და არა დაკვირვებითი ჭეშმარიტება."
    ),
    "FREEDOM_LEDGER": {
        "F1_definition": {"source": "W2-C0 and source-aligned logical split from F2", "range": "route-neutral literal registry", "scale": "programme", "complexity": 1},
        "witness_kind": {"source": "frozen architecture", "range": sorted(WITNESS_KINDS), "scale": "candidate", "complexity": 1},
        "law_origin_status": {"source": "primitive-law policy", "range": sorted(ALLOWED_LAW_ORIGIN_STATUSES), "scale": "candidate", "complexity": 1},
        "promotion_gate": {"source": "frozen exact AND rule", "range": sorted(PROMOTION_AND_GATES), "scale": "candidate", "complexity": "all gates; no scalarization"},
        "router_overlay": {"source": "versioned response to w2_07 mismatch", "range": [NEW_ROUTE_CLASS], "scale": "programme", "complexity": 1},
        "data_fitted_parameters": {"source": "N/A — no data", "range": 0, "scale": "data", "complexity": 0},
    },
    "DEPENDENCIES": [
        "W2-C0 v1.0 frozen programme contract",
        "w2_03 v1.8 historical source-aligned route taxonomy",
        "w2_04 v1.7 and w2_05 v1.7 transitive no-go/primary-route dependencies",
        "w2_06 v1.0 conditional exact atemporal candidate",
        "w2_07 v2.6 exact route-adjudication decision with physical W2_F1 open",
    ],
    "METHOD": (
        "Freeze semantics before evaluation; construct taxonomy v2 as the exact noncolliding "
        "union of live w2_03 classes and one route-neutral overlay; validate an uncompensated "
        "boolean AND rule with candidate-independent INTER/INTRA controls and adversarial mutants."
    ),
    "PASS_CONDITION": [
        "all contract fields and critical registries are exact and independently digest-bound.",
        "live W2-C0/w2_03/w2_06/w2_07 identities, hashes, statuses and scope flags are exact.",
        "F1 definition contains no N=3, 1+2, rank, Q, projector, spatial or GR target.",
        "taxonomy v2 is the exact historical taxonomy plus one noncolliding route-neutral class.",
        "w2_06 is classified under the overlay only for future audit; no overlay obligation is marked passed.",
        "generic INTER_CLASS and INTRA_CLASS positive controls pass the same boolean AND validator.",
        "every missing, false, truthy, extra, score, target, temporal, route-laundering and downstream mutant fails.",
        "W2_F1 and every downstream physical/export flag remain exactly False."
    ],
    "FAIL_CONDITION": (
        "Any definition or taxonomy drift, dependency mismatch, candidate-specific target in F1, "
        "partial/weighted promotion, premature candidate evaluation, route laundering or downstream closure."
    ),
    "FALSIFIER": (
        "A route-neutral counterexample showing the frozen definition accepts a prewired/gauge/arbitrary "
        "decomposition or rejects a valid stable intrinsic differentiation invalidates this contract version."
    ),
    "RESIDUAL": "0 for exact registry, set, status and boolean-logic checks; candidate physical residual N/A.",
    "ERROR_BOUND": "0 for discrete contract logic; no numerical or observational approximation is made.",
    "VALIDITY_HEALTH": (
        "This gate certifies only a definition/router architecture. Candidate algebra, law admissibility, "
        "physical-role meaning, stability and falsifier are evaluated separately in w2_09."
    ),
    "BRANCHES": dict(EXPECTED_BRANCHES),
    "OBSERVABLE_MAP": "N/A — F1 contract has no external observable.",
    "FORWARD_MODEL": "N/A — no ideal-observable-to-data chain.",
    "DATA_ROLE": "N/A — no data used; later observations retain veto authority.",
    "IDENTIFIABILITY": (
        "At F1, only full-equivalence intrinsic-role/outcome inequivalence is tested; operational "
        "and observational identifiability are deferred."
    ),
    "BENCHMARK": (
        "Candidate-independent INTER/INTRA positives, trivial/gauge/prewired/arbitrary-decomposition "
        "nulls and exact partial-AND failures; no empirical benchmark."
    ),
    "CLOSURE_FLAGS": dict(INITIAL_CLOSURE_FLAGS),
    "GATE_APPLICABILITY": dict(GATE_APPLICABILITY),
    "CROSSCHECK": (
        "The same validator accepts abstract INTER_CLASS and INTRA_CLASS witnesses and rejects "
        "candidate-specific labels, proving the criterion is not tailored to w2_06."
    ),
    "PROVENANCE": "runtime SHA-256 of sources and frozen Work2 dependencies; stdout JSON artifact",
    "FILES": [
        "CODES.md", "Theory_Canon.md", "intuitive/RefG_GE.md",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_03_f1_source_aligned_route_contract.py",
        "RefG/work 2/w2_04_f1_equivariant_fixed_set_no_go_gate.py",
        "RefG/work 2/w2_05_f1_primary_route_specification.py",
        "RefG/work 2/w2_06_f1_atemporal_spectral_split_candidate_gate.py",
        "RefG/work 2/w2_07_f1_route_adjudication_gate.py",
        "RefG/work 2/w2_08_f1_physical_promotion_contract.py",
    ],
    "ROUTER_VERSION": ROUTER_VERSION,
    "F1_DEFINITION": copy.deepcopy(F1_DEFINITION),
    "F1_ROLE_SEMANTICS": copy.deepcopy(F1_ROLE_SEMANTICS),
    "WITNESS_KINDS": copy.deepcopy(WITNESS_KINDS),
    "PROMOTION_AND_GATES": copy.deepcopy(PROMOTION_AND_GATES),
    "PRIMITIVE_LAW_POLICY": copy.deepcopy(PRIMITIVE_LAW_POLICY),
    "ROUTE_SUPPORT_POLICIES": copy.deepcopy(ROUTE_SUPPORT_POLICIES),
    "BASE_ROUTE_TAXONOMY_V1": copy.deepcopy(BASE_ROUTE_TAXONOMY_V1),
    "ROUTE_TAXONOMY_OVERLAY_V2": copy.deepcopy(ROUTE_TAXONOMY_OVERLAY_V2),
    "EFFECTIVE_ROUTE_TAXONOMY_V2": copy.deepcopy(EFFECTIVE_ROUTE_TAXONOMY_V2),
    "CANDIDATE_CLASSIFICATION": copy.deepcopy(CANDIDATE_CLASSIFICATION),
    "CANDIDATE_EVALUATION_TEMPLATE": copy.deepcopy(CANDIDATE_EVALUATION_TEMPLATE),
    "W2_06_PREAUDIT_LEDGER": copy.deepcopy(W2_06_PREAUDIT_LEDGER),
    "FORBIDDEN_PROMOTION_SHORTCUTS": copy.deepcopy(FORBIDDEN_PROMOTION_SHORTCUTS),
    "DEFERRED_OUTPUTS": list(DEFERRED_OUTPUTS),
    "SUPERSESSION_SCOPE": copy.deepcopy(SUPERSESSION_SCOPE),
    "REGISTRY_SHA256": dict(EXPECTED_REGISTRY_SHA256),
    "NEXT_AUDIT": (
        "w2_09 must apply every frozen boolean promotion gate to the exact w2_06 candidate, "
        "without changing this definition, overlay class, witness kind or law-origin policy."
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
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


def route_registry_schema_valid(registry: Any) -> bool:
    return (
        isinstance(registry, dict)
        and bool(registry)
        and all(
            isinstance(name, str)
            and bool(name.strip())
            and isinstance(spec, dict)
            and set(spec) == {"imports_to_declare", "must_derive"}
            and all(
                isinstance(spec[field], list)
                and bool(spec[field])
                and len(spec[field]) == len(set(spec[field]))
                and all(isinstance(item, str) and item.strip() for item in spec[field])
                for field in ("imports_to_declare", "must_derive")
            )
            for name, spec in registry.items()
        )
    )


def taxonomy_v2_valid(
    base: Any,
    overlay: Any,
    effective: Any,
    live_v1: Any,
) -> bool:
    if not all(
        isinstance(value, dict) for value in (base, overlay, effective, live_v1)
    ):
        return False
    overlay_spec = (
        overlay.get(NEW_ROUTE_CLASS, {}) if isinstance(overlay, dict) else {}
    )
    overlay_derivations = overlay_spec.get("must_derive", [])
    return all((
        route_registry_schema_valid(base),
        route_registry_schema_valid(overlay),
        route_registry_schema_valid(effective),
        base == live_v1,
        set(overlay) == {NEW_ROUTE_CLASS},
        not (set(base) & set(overlay)),
        effective == {**copy.deepcopy(base), **copy.deepcopy(overlay)},
        set(effective) - set(base) == {NEW_ROUTE_CLASS},
        effective.get("atemporal_nonunique_solution_structure")
        == base.get("atemporal_nonunique_solution_structure"),
        base.get("atemporal_nonunique_solution_structure", {}).get("must_derive")
        == ["inequivalent_stable_solutions", "noncircular_physical_selection_account"],
        "canonical_state_generated_coexisting_roles"
        in overlay_derivations,
        "nonexchangeability_after_full_quotient"
        in overlay_derivations,
        "law_relevance_not_arbitrary_decomposition"
        in overlay_derivations,
        not any(
            token in " ".join(overlay_derivations).lower()
            for token in ("rank_1", "rank_2", "1+2", "n=3", "projector_q")
        ),
    ))


def definition_is_route_neutral(definition: Any) -> bool:
    if not isinstance(definition, dict) or set(definition) != {
        "route_neutral_core", "inter_class_route", "intra_class_route",
        "physical_ceiling", "proof_strength",
    }:
        return False
    if not all(isinstance(value, str) and value.strip() for value in definition.values()):
        return False
    defining_text = " ".join(
        definition[key]
        for key in (
            "route_neutral_core", "inter_class_route", "intra_class_route",
            "proof_strength",
        )
    ).lower()
    candidate_tokens = (
        "n=3", "1+2", "rank-1", "rank-2", "rank_1", "rank_2",
        "projector", "sym_0", "sym0", "o(3)", "argmin", "w2_06",
        "einstein", "general relativity",
    )
    return all((
        not any(token in defining_text for token in candidate_tokens),
        "target-free" in defining_text,
        "multiple inequivalent accepted outcomes" in defining_text,
        "one unique quotient state" in defining_text,
        "multiple vacua or quotient solutions are not required" in defining_text,
        "F1 establishes candidate-level intrinsic roles only"
        in definition["physical_ceiling"],
    ))


def role_semantics_valid(semantics: Any) -> bool:
    required = {
        "generated_from_output", "absent_at_reference", "full_equivalence",
        "intrinsic_invariant", "law_relevance", "structural_stability",
    }
    return (
        isinstance(semantics, dict)
        and set(semantics) == required
        and all(isinstance(value, str) and value.strip() for value in semantics.values())
        and "not fixed basis vectors" in semantics["generated_from_output"]
        and "no allowed gauge, relabel or automorphism exchanges"
        in semantics["full_equivalence"]
        and "arbitrary decomposition or projector algebra alone is insufficient"
        in semantics["law_relevance"]
        and "not a temporal formation or persistence claim"
        in semantics["structural_stability"]
    )


def frozen_registry_bundle() -> dict[str, Any]:
    return {
        "WITNESS_KINDS": WITNESS_KINDS,
        "F1_DEFINITION": F1_DEFINITION,
        "F1_ROLE_SEMANTICS": F1_ROLE_SEMANTICS,
        "PROMOTION_AND_GATES": PROMOTION_AND_GATES,
        "PRIMITIVE_LAW_POLICY": PRIMITIVE_LAW_POLICY,
        "ROUTE_SUPPORT_POLICIES": ROUTE_SUPPORT_POLICIES,
        "BASE_ROUTE_TAXONOMY_V1": BASE_ROUTE_TAXONOMY_V1,
        "ROUTE_TAXONOMY_OVERLAY_V2": ROUTE_TAXONOMY_OVERLAY_V2,
        "EFFECTIVE_ROUTE_TAXONOMY_V2": EFFECTIVE_ROUTE_TAXONOMY_V2,
        "CANDIDATE_CLASSIFICATION": CANDIDATE_CLASSIFICATION,
        "CANDIDATE_EVALUATION_TEMPLATE": CANDIDATE_EVALUATION_TEMPLATE,
        "W2_06_PREAUDIT_LEDGER": W2_06_PREAUDIT_LEDGER,
        "FORBIDDEN_PROMOTION_SHORTCUTS": FORBIDDEN_PROMOTION_SHORTCUTS,
        "DEFERRED_OUTPUTS": DEFERRED_OUTPUTS,
        "SUPERSESSION_SCOPE": SUPERSESSION_SCOPE,
        "PROMOTION_POLICY_DEFAULTS": PROMOTION_POLICY_DEFAULTS,
        "INITIAL_CLOSURE_FLAGS": INITIAL_CLOSURE_FLAGS,
        "GATE_APPLICABILITY": GATE_APPLICABILITY,
        "EXPECTED_BRANCHES": EXPECTED_BRANCHES,
    }


def frozen_registry_bundle_valid(bundle: Any) -> bool:
    return (
        isinstance(bundle, dict)
        and set(bundle) == set(EXPECTED_REGISTRY_SHA256)
        and all(
            canonical_sha256(bundle[name]) == expected
            for name, expected in EXPECTED_REGISTRY_SHA256.items()
        )
    )


def candidate_classification_valid(classification: Any) -> bool:
    return classification == CANDIDATE_CLASSIFICATION and all((
        classification.get("candidate_claim_id") == W2_06_CANDIDATE_ID,
        classification.get("historical_w2_03_label")
        == "atemporal_nonunique_solution_structure",
        classification.get("historical_label_status")
        == "PRESENCE_ONLY__CONTRACT_NOT_SATISFIED",
        classification.get("effective_v2_class") == NEW_ROUTE_CLASS,
        classification.get("witness_kind_for_w2_09")
        == "INTRA_CLASS_CANONICAL_ROLES",
        classification.get("promotion_status")
        == "NOT_EVALUATED__PROGRAMME_W2_F1_OPEN",
    ))


def evaluation_template_open(template: Any) -> bool:
    return (
        isinstance(template, dict)
        and set(template) == set(PROMOTION_AND_GATES)
        and all(
            type(value) is str and value == "OPEN__TO_BE_ADJUDICATED_IN_W2_09"
            for value in template.values()
        )
    )


def promotion_evidence_valid(
    evidence: Any,
    witness_kind: Any,
    law_origin_status: Any,
    policy: Any,
) -> bool:
    return all((
        isinstance(evidence, dict),
        isinstance(evidence, dict) and set(evidence) == set(PROMOTION_AND_GATES),
        isinstance(evidence, dict)
        and all(type(value) is bool and value is True for value in evidence.values()),
        type(witness_kind) is str and witness_kind in WITNESS_KINDS,
        type(law_origin_status) is str
        and law_origin_status in ALLOWED_LAW_ORIGIN_STATUSES,
        isinstance(policy, dict),
        isinstance(policy, dict) and set(policy) == set(PROMOTION_POLICY_DEFAULTS),
        isinstance(policy, dict)
        and all(type(value) is bool and value is False for value in policy.values()),
    ))


def independent_promotion_audit(
    evidence: Any,
    witness_kind: Any,
    law_origin_status: Any,
    policy: Any,
) -> bool:
    if not isinstance(evidence, dict) or tuple(sorted(evidence)) != tuple(sorted(PROMOTION_AND_GATES)):
        return False
    if [key for key in sorted(evidence) if evidence[key] is not True]:
        return False
    if any(type(evidence[key]) is not bool for key in evidence):
        return False
    if witness_kind not in tuple(sorted(WITNESS_KINDS)) or type(witness_kind) is not str:
        return False
    if (
        type(law_origin_status) is not str
        or law_origin_status not in tuple(sorted(ALLOWED_LAW_ORIGIN_STATUSES))
    ):
        return False
    if not isinstance(policy, dict) or tuple(sorted(policy)) != tuple(sorted(PROMOTION_POLICY_DEFAULTS)):
        return False
    return not [
        key for key in sorted(policy)
        if type(policy[key]) is not bool or policy[key] is not False
    ]


def source_boundaries_valid(texts: dict[str, str]) -> bool:
    return all((
        "ერთადერთი უცვლელი ღერძია საუკეთესო ხელმისაწვდომ დაკვირვებებთან სრული თავსებადობა"
        in texts["CODES"],
        "დროის არმქონე კანდიდატში თვითგარჩევა შეიძლება იყოს ამონახსნთა სტრუქტურული არჩევა და არა დროითი მოვლენა"
        in texts["W2_C0"],
        "ფუძიდან გამოვლენილ გარემომდე გადასვლა სტრუქტურული თვითგარჩევაა და არა წინასწარ არსებულ საათში მომხდარი მოვლენა"
        in texts["CANON"],
        "მრავლობითობა ბუნებაში მხოლოდ მაშინ ჩნდება, როდესაც ფუძის თვითგარჩევით წარმოქმნილი განსხვავება სტაბილურ ფიზიკურ კვალს ტოვებს"
        in texts["INTUITIVE"],
    ))


def w2_03_identity_valid(module: Any) -> bool:
    return all((
        getattr(module, "MODEL_VERSION", None)
        == "W2-F1-SOURCE-ALIGNED-ROUTE-CONTRACT-v1.8-internal",
        getattr(module, "CANDIDATE_CLASSES", None) == BASE_ROUTE_TAXONOMY_V1,
        getattr(module, "CLAIM_CONTRACT", {}).get("CLOSURE_FLAGS", {}).get(
            "W2_F1_SELF_DIFFERENTIATION"
        ) is False,
    ))


def w2_06_identity_valid(module: Any) -> bool:
    contract = getattr(module, "CLAIM_CONTRACT", {})
    closure = contract.get("CLOSURE_FLAGS", {})
    freedom = contract.get("FREEDOM_LEDGER", {})
    return all((
        getattr(module, "MODEL_VERSION", None)
        == "W2-F1-ATEMPORAL-SPECTRAL-SPLIT-v1.0-internal",
        contract.get("CLAIM_ID") == W2_06_CANDIDATE_ID,
        contract.get("PRIMITIVE_REGISTRY")
        == getattr(module, "EXPECTED_PRIMITIVE_REGISTRY", None),
        contract.get("IMPORTED_NOT_DERIVED")
        == list(getattr(module, "EXPECTED_IMPORTED_NOT_DERIVED", ())),
        contract.get("BRANCHES") == getattr(module, "EXPECTED_BRANCHES", None),
        freedom.get("seed_or_randomness", {}).get("range") == 0,
        "unique" in contract.get("SELECTION_RULE", "").lower(),
        "no representative direction" in contract.get("SELECTION_RULE", ""),
        closure.get("W2_F1_SELF_DIFFERENTIATION") is False,
        closure.get("W2_F2_OPERATIONAL_RELATIONS") is False,
        closure.get("W2_M1_DIMENSION_CONTINUUM") is False,
        closure.get("W2_M2_LORENTZIAN_METRIC") is False,
    ))


def w2_07_report_valid(module: Any, report: Any) -> bool:
    if not isinstance(report, dict):
        return False
    checks = report.get("CHECKS", {})
    closure = report.get("CLOSURE_FLAGS", {})
    classification = report.get("ROUTE_CLASSIFICATION", {})
    decision = report.get("DECISION", {})
    obligation_map = report.get("ATEMPORAL_OBLIGATION_MAP", {})
    seed_only = {
        "G_sym_invariant_seed_distribution",
        "individual_nonsymmetric_seed_realization",
        "open_or_nonzero_measure_successful_seed_basin",
        "internal_seed_sampling_or_outcome_mechanism",
    }
    na_keys = {
        key for key, value in obligation_map.items()
        if value == "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE"
    }
    digest_checks = {
        "CHECK_KEYS": canonical_sha256(sorted(checks)),
        "CLOSURE_FLAGS": canonical_sha256(closure),
        "DEPENDENCY_STATUSES": canonical_sha256(report.get("DEPENDENCY_STATUSES")),
        "DEPENDENCY_VERSIONS": canonical_sha256(report.get("DEPENDENCY_VERSIONS")),
        "ROUTE_CLASSIFICATION": canonical_sha256(classification),
        "ATEMPORAL_OBLIGATION_MAP": canonical_sha256(obligation_map),
    }
    return all((
        report.get("MODEL_VERSION") == "W2-F1-ROUTE-ADJUDICATION-v2.6-internal",
        report.get("STATUS")
        == "ATEMPORAL_CANDIDATE_SELECTED_FOR_NEXT_F1_ADJUDICATION__SEED_ROUTE_OPEN_FALLBACK__PHYSICAL_W2_F1_OPEN",
        report.get("SELECTED_ROUTE")
        == "ATEMPORAL_SPECTRAL_SPLIT_WITH_UNIQUE_QUOTIENT_MINIMUM",
        report.get("PRIOR_ROUTE")
        == "SYMMETRIC_BIFURCATION_WITH_TARGET_FREE_GENERIC_SEED",
        isinstance(checks, dict) and len(checks) == 44,
        all(type(value) is bool and value is True for value in checks.values()),
        digest_checks == EXPECTED_W2_07_REPORT_SHA256,
        closure.get("ATEMPORAL_PRIMARY_FOR_NEXT_F1_AUDIT") is True,
        closure.get("SEED_ROUTE_FALLBACK_OPEN") is True,
        closure.get("ROUTE_CLASS_CONTRACT_SATISFIED") is False,
        closure.get("PHYSICAL_ROUTE_DOMINANCE") is False,
        closure.get("SEED_ROUTE_REJECTED") is False,
        closure.get("W2_F1_SELF_DIFFERENTIATION") is False,
        closure.get("G6_PHYSICAL_MATCH") is False,
        classification == getattr(module, "EXPECTED_ROUTE_CLASSIFICATION", None),
        classification.get("existing_class_contract_satisfied") is False,
        classification.get("temporary_bucket_contract_satisfied") is False,
        classification.get("promotion_effect")
        == "PHYSICAL_F1_HARD_VETO_UNTIL_ROUTER_ALIGNMENT_IS_RESOLVED",
        obligation_map.get("seed_or_selection_origin")
        == "OPEN__ATEMPORAL_GLOBAL_ARGMIN_ORIGIN_UNJUSTIFIED",
        na_keys == seed_only,
        decision.get("exclusive_primary")
        == "ATEMPORAL_SPECTRAL_SPLIT_WITH_UNIQUE_QUOTIENT_MINIMUM",
        decision.get("alternatives_preserved") is True,
        decision.get("right_evidence_schema_exact") is True,
        decision.get("right_veto_failures") == [],
    ))


def expected_runtime_closure(contract_pass: bool) -> dict[str, bool]:
    closure = dict(INITIAL_CLOSURE_FLAGS)
    for key in (
        "G0_GOAL", "G1_CONVENTIONS", "G3_STRUCTURE",
        "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION",
        "F1_PROMOTION_CONTRACT_FROZEN", "F1_ROUTE_TAXONOMY_V2_FROZEN",
        "W2_06_CLASSIFICATION_ALIGNED",
    ):
        closure[key] = bool(contract_pass)
    return closure


def runtime_closure_valid(closure: Any, contract_pass: bool) -> bool:
    return exact_literal_map(closure, expected_runtime_closure(contract_pass))


def run_gate() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    work2 = root / "RefG" / "work 2"
    paths = {
        "CODES": root / "CODES.md",
        "CANON": root / "Theory_Canon.md",
        "INTUITIVE": root / "intuitive" / "RefG_GE.md",
        "W2_C0": work2 / "w2_00_foundation_to_einstein_contract.md",
        "W2_03": work2 / "w2_03_f1_source_aligned_route_contract.py",
        "W2_04": work2 / "w2_04_f1_equivariant_fixed_set_no_go_gate.py",
        "W2_05": work2 / "w2_05_f1_primary_route_specification.py",
        "W2_06": work2 / "w2_06_f1_atemporal_spectral_split_candidate_gate.py",
        "W2_07": work2 / "w2_07_f1_route_adjudication_gate.py",
        "SOURCE": Path(__file__).resolve(),
    }
    dependency_hashes = {
        name: sha256(paths[name]) for name in EXPECTED_DEPENDENCY_SHA256
    }
    dependency_bytes_exact = dependency_hashes == EXPECTED_DEPENDENCY_SHA256

    # w2_07 reexecutes its full dependency chain.  w2_03 and w2_06 are imported
    # here only to bind their frozen registries and identities independently.
    module_03 = load_module(paths["W2_03"], "w2_03_w2_08_identity")
    module_06 = load_module(paths["W2_06"], "w2_06_w2_08_identity")
    module_07 = load_module(paths["W2_07"], "w2_07_w2_08_dependency")
    report_07 = module_07.run_gate()

    texts = {
        name: paths[name].read_text(encoding="utf-8")
        for name in ("CODES", "CANON", "INTUITIVE", "W2_C0")
    }

    expected_w2_07_provenance = {
        "CODES": EXPECTED_DEPENDENCY_SHA256["CODES"],
        "CANON": EXPECTED_DEPENDENCY_SHA256["CANON"],
        "INTUITIVE": EXPECTED_DEPENDENCY_SHA256["INTUITIVE"],
        "W2_C0": EXPECTED_DEPENDENCY_SHA256["W2_C0"],
        "W2_03": EXPECTED_DEPENDENCY_SHA256["W2_03"],
        "W2_04": EXPECTED_DEPENDENCY_SHA256["W2_04"],
        "W2_05": EXPECTED_DEPENDENCY_SHA256["W2_05"],
        "W2_06": EXPECTED_DEPENDENCY_SHA256["W2_06"],
        "SOURCE": EXPECTED_DEPENDENCY_SHA256["W2_07"],
    }
    dependency_provenance_exact = (
        report_07.get("PROVENANCE") == expected_w2_07_provenance
    )

    current_bundle = frozen_registry_bundle()
    actual_registry_hashes = {
        name: canonical_sha256(value) for name, value in current_bundle.items()
    }
    registry_hashes_exact = actual_registry_hashes == EXPECTED_REGISTRY_SHA256

    claimed_custom_values = {
        "ROUTER_VERSION": ROUTER_VERSION,
        "F1_DEFINITION": F1_DEFINITION,
        "F1_ROLE_SEMANTICS": F1_ROLE_SEMANTICS,
        "WITNESS_KINDS": WITNESS_KINDS,
        "PROMOTION_AND_GATES": PROMOTION_AND_GATES,
        "PRIMITIVE_LAW_POLICY": PRIMITIVE_LAW_POLICY,
        "ROUTE_SUPPORT_POLICIES": ROUTE_SUPPORT_POLICIES,
        "BASE_ROUTE_TAXONOMY_V1": BASE_ROUTE_TAXONOMY_V1,
        "ROUTE_TAXONOMY_OVERLAY_V2": ROUTE_TAXONOMY_OVERLAY_V2,
        "EFFECTIVE_ROUTE_TAXONOMY_V2": EFFECTIVE_ROUTE_TAXONOMY_V2,
        "CANDIDATE_CLASSIFICATION": CANDIDATE_CLASSIFICATION,
        "CANDIDATE_EVALUATION_TEMPLATE": CANDIDATE_EVALUATION_TEMPLATE,
        "W2_06_PREAUDIT_LEDGER": W2_06_PREAUDIT_LEDGER,
        "FORBIDDEN_PROMOTION_SHORTCUTS": FORBIDDEN_PROMOTION_SHORTCUTS,
        "DEFERRED_OUTPUTS": list(DEFERRED_OUTPUTS),
        "SUPERSESSION_SCOPE": SUPERSESSION_SCOPE,
        "REGISTRY_SHA256": EXPECTED_REGISTRY_SHA256,
    }
    claim_custom_values_bound = all(
        CLAIM_CONTRACT.get(name) == value
        for name, value in claimed_custom_values.items()
    )
    contract_keyset_exact = (
        set(CLAIM_CONTRACT) == REQUIRED_FIELDS | REQUIRED_CUSTOM_FIELDS
    )
    contract_values_nonempty = all(
        value_present(value) for value in CLAIM_CONTRACT.values()
    )
    contract_model_bound = (
        CLAIM_CONTRACT.get("CLAIM_ID") == "W2_F1_PHYSICAL_PROMOTION_CONTRACT_001"
        and isinstance(CLAIM_CONTRACT.get("MODEL_VERSION"), str)
        and CLAIM_CONTRACT["MODEL_VERSION"].startswith(MODEL_VERSION)
    )
    contract_static_flags_exact = all((
        exact_literal_map(
            CLAIM_CONTRACT.get("CLOSURE_FLAGS"), INITIAL_CLOSURE_FLAGS
        ),
        CLAIM_CONTRACT.get("GATE_APPLICABILITY") == GATE_APPLICABILITY,
        CLAIM_CONTRACT.get("BRANCHES") == EXPECTED_BRANCHES,
        CLAIM_CONTRACT.get("DATA_ROLE", "").startswith("N/A"),
        CLAIM_CONTRACT.get("OBSERVABLE_MAP", "").startswith("N/A"),
        CLAIM_CONTRACT.get("FORWARD_MODEL", "").startswith("N/A"),
    ))

    taxonomy_exact = taxonomy_v2_valid(
        BASE_ROUTE_TAXONOMY_V1,
        ROUTE_TAXONOMY_OVERLAY_V2,
        EFFECTIVE_ROUTE_TAXONOMY_V2,
        getattr(module_03, "CANDIDATE_CLASSES", None),
    )
    definition_exact = definition_is_route_neutral(F1_DEFINITION)
    roles_exact = role_semantics_valid(F1_ROLE_SEMANTICS)
    witnesses_exact = (
        set(WITNESS_KINDS)
        == {"INTER_CLASS_INEQUIVALENT_OUTCOMES", "INTRA_CLASS_CANONICAL_ROLES"}
        and all(isinstance(value, str) and value.strip() for value in WITNESS_KINDS.values())
    )
    primitive_policy_exact = all((
        set(ALLOWED_LAW_ORIGIN_STATUSES)
        == {
            "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
            "DERIVED_BY_SEPARATE_FROZEN_GATE",
        },
        "unique global argmin does not derive its own law"
        in PRIMITIVE_LAW_POLICY["argmin_guard"],
        "IMPORTED_NOT_DERIVED" in PRIMITIVE_LAW_POLICY["status_ceiling"],
    ))
    classification_exact = candidate_classification_valid(CANDIDATE_CLASSIFICATION)
    candidate_evaluation_still_open = evaluation_template_open(
        CANDIDATE_EVALUATION_TEMPLATE
    )
    preaudit_honest = all((
        W2_06_PREAUDIT_LEDGER.get("overlay_class_contract")
        == "DEFINED_HERE__NOT_YET_EVALUATED",
        W2_06_PREAUDIT_LEDGER.get("primitive_foundation_admissibility") == "OPEN",
        W2_06_PREAUDIT_LEDGER.get("argmin_law_noncircularity") == "OPEN",
        W2_06_PREAUDIT_LEDGER.get("N1_N2_N4_and_general_N_controls")
        == "OPEN__MUST_BE_REEXECUTED_IN_W2_09",
        W2_06_PREAUDIT_LEDGER.get(
            "N3_O3_delta_matrix_Qsign_and_1plus2_import_origin"
        ) == "OPEN__NO_GEOMETRY_DIMENSION_OR_RANK_BONUS_ALLOWED",
        W2_06_PREAUDIT_LEDGER.get(
            "b0_polarity_coercivity_and_forbidden_source_controls"
        ) == "OPEN__MUST_BE_REEXECUTED_IN_W2_09",
        W2_06_PREAUDIT_LEDGER.get("programme_W2_F1") == "OPEN",
    ))

    all_true_evidence = {name: True for name in PROMOTION_AND_GATES}
    clean_policy = dict(PROMOTION_POLICY_DEFAULTS)
    inter_positive = promotion_evidence_valid(
        all_true_evidence,
        "INTER_CLASS_INEQUIVALENT_OUTCOMES",
        "DERIVED_BY_SEPARATE_FROZEN_GATE",
        clean_policy,
    )
    intra_positive = promotion_evidence_valid(
        all_true_evidence,
        "INTRA_CLASS_CANONICAL_ROLES",
        "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
        clean_policy,
    )
    independent_positives = all((
        independent_promotion_audit(
            all_true_evidence,
            "INTER_CLASS_INEQUIVALENT_OUTCOMES",
            "DERIVED_BY_SEPARATE_FROZEN_GATE",
            clean_policy,
        ),
        independent_promotion_audit(
            all_true_evidence,
            "INTRA_CLASS_CANONICAL_ROLES",
            "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
            clean_policy,
        ),
    ))

    gate_mutation_results: dict[str, bool] = {}
    for gate in PROMOTION_AND_GATES:
        missing = dict(all_true_evidence)
        missing.pop(gate)
        false_value = dict(all_true_evidence)
        false_value[gate] = False
        truthy_value = dict(all_true_evidence)
        truthy_value[gate] = 1
        gate_mutation_results[gate] = all((
            not promotion_evidence_valid(
                missing,
                "INTRA_CLASS_CANONICAL_ROLES",
                "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
                clean_policy,
            ),
            not promotion_evidence_valid(
                false_value,
                "INTRA_CLASS_CANONICAL_ROLES",
                "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
                clean_policy,
            ),
            not promotion_evidence_valid(
                truthy_value,
                "INTRA_CLASS_CANONICAL_ROLES",
                "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
                clean_policy,
            ),
        ))
    extra_gate = dict(all_true_evidence)
    extra_gate["candidate_specific_rank_bonus"] = True
    extra_gate_rejected = not promotion_evidence_valid(
        extra_gate,
        "INTRA_CLASS_CANONICAL_ROLES",
        "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
        clean_policy,
    )

    policy_mutation_results: dict[str, bool] = {}
    for key in PROMOTION_POLICY_DEFAULTS:
        true_policy = dict(clean_policy)
        true_policy[key] = True
        truthy_policy = dict(clean_policy)
        truthy_policy[key] = 1
        falsey_nonboolean_policy = dict(clean_policy)
        falsey_nonboolean_policy[key] = 0
        missing_policy = dict(clean_policy)
        missing_policy.pop(key)
        policy_mutation_results[key] = all((
            not promotion_evidence_valid(
                all_true_evidence,
                "INTRA_CLASS_CANONICAL_ROLES",
                "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
                true_policy,
            ),
            not promotion_evidence_valid(
                all_true_evidence,
                "INTRA_CLASS_CANONICAL_ROLES",
                "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
                truthy_policy,
            ),
            not promotion_evidence_valid(
                all_true_evidence,
                "INTRA_CLASS_CANONICAL_ROLES",
                "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
                falsey_nonboolean_policy,
            ),
            not promotion_evidence_valid(
                all_true_evidence,
                "INTRA_CLASS_CANONICAL_ROLES",
                "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
                missing_policy,
            ),
        ))
    extra_policy = dict(clean_policy)
    extra_policy["priority_override"] = False
    class _StringSubclass(str):
        pass

    law_status_subclass = _StringSubclass(
        "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED"
    )
    witness_subclass = _StringSubclass("INTRA_CLASS_CANONICAL_ROLES")
    bad_labels_rejected = all((
        not promotion_evidence_valid(
            all_true_evidence,
            "RANK_1_PLUS_RANK_2",
            "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
            clean_policy,
        ),
        not promotion_evidence_valid(
            all_true_evidence,
            "INTRA_CLASS_CANONICAL_ROLES",
            "UNIQUE_ARGMIN_PROVES_ITS_OWN_ORIGIN",
            clean_policy,
        ),
        not promotion_evidence_valid(
            all_true_evidence,
            "INTRA_CLASS_CANONICAL_ROLES",
            "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
            extra_policy,
        ),
        not promotion_evidence_valid(
            all_true_evidence,
            witness_subclass,
            "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
            clean_policy,
        ),
        not promotion_evidence_valid(
            all_true_evidence,
            "INTRA_CLASS_CANONICAL_ROLES",
            law_status_subclass,
            clean_policy,
        ),
        not independent_promotion_audit(
            all_true_evidence,
            witness_subclass,
            "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
            clean_policy,
        ),
        not independent_promotion_audit(
            all_true_evidence,
            "INTRA_CLASS_CANONICAL_ROLES",
            law_status_subclass,
            clean_policy,
        ),
        not promotion_evidence_valid(
            CANDIDATE_EVALUATION_TEMPLATE,
            "INTRA_CLASS_CANONICAL_ROLES",
            "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
            clean_policy,
        ),
    ))

    semantic_null_gate = {
        "trivial_reference": "undifferentiated_reference_trivial",
        "gauge_or_relabel_multiplicity": "inequivalence_survives_full_quotient",
        "fixed_basis_or_preloaded_roles": "intrinsic_differentiation_certified",
        "arbitrary_projector_decomposition": "law_relevance_not_arbitrary_decomposition",
        "target_distance_or_posthoc_argmin": "target_free_law_certified",
        "tuned_single_point": "open_domain_stability_and_robustness",
        "unjustified_selection_origin": "realization_or_selection_noncircular",
        "future_geometry_laundering": "foundation_admissibility_and_import_health",
        "temporal_claim_from_hessian": "f1_only_scope_honest",
        "route_label_without_contract": "router_extension_aligned",
    }
    semantic_null_results: dict[str, bool] = {}
    for name, failed_gate in semantic_null_gate.items():
        null_evidence = dict(all_true_evidence)
        null_evidence[failed_gate] = False
        semantic_null_results[name] = not promotion_evidence_valid(
            null_evidence,
            "INTRA_CLASS_CANONICAL_ROLES",
            "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
            clean_policy,
        )

    definition_mutant = copy.deepcopy(F1_DEFINITION)
    definition_mutant["route_neutral_core"] += " N=3 rank-1+rank-2 projector argmin."
    overlay_mutant = copy.deepcopy(ROUTE_TAXONOMY_OVERLAY_V2)
    overlay_mutant[NEW_ROUTE_CLASS]["must_derive"].append("rank_1_rank_2")
    removed_base_mutant = copy.deepcopy(BASE_ROUTE_TAXONOMY_V1)
    removed_base_mutant.pop("stochastic_or_quantum_outcome")
    collision_overlay_mutant = {
        "atemporal_nonunique_solution_structure": copy.deepcopy(
            ROUTE_TAXONOMY_OVERLAY_V2[NEW_ROUTE_CLASS]
        )
    }
    classification_mutant = copy.deepcopy(CANDIDATE_CLASSIFICATION)
    classification_mutant["effective_v2_class"] = "atemporal_nonunique_solution_structure"
    evaluation_mutant = dict(CANDIDATE_EVALUATION_TEMPLATE)
    evaluation_mutant["router_extension_aligned"] = True

    bundle_mutants: dict[str, dict[str, Any]] = {}
    for name in (
        "candidate_specific_definition", "candidate_specific_overlay",
        "premature_candidate_evaluation", "wrong_candidate_classification",
    ):
        bundle_mutants[name] = copy.deepcopy(current_bundle)
    bundle_mutants["candidate_specific_definition"]["F1_DEFINITION"] = definition_mutant
    bundle_mutants["candidate_specific_overlay"]["ROUTE_TAXONOMY_OVERLAY_V2"] = overlay_mutant
    bundle_mutants["premature_candidate_evaluation"]["CANDIDATE_EVALUATION_TEMPLATE"] = evaluation_mutant
    bundle_mutants["wrong_candidate_classification"]["CANDIDATE_CLASSIFICATION"] = classification_mutant

    registry_mutation_results = {
        "candidate_specific_definition_rejected": (
            not definition_is_route_neutral(definition_mutant)
            and not frozen_registry_bundle_valid(
                bundle_mutants["candidate_specific_definition"]
            )
        ),
        "candidate_specific_overlay_rejected": not frozen_registry_bundle_valid(
            bundle_mutants["candidate_specific_overlay"]
        ),
        "historical_class_removal_rejected": not taxonomy_v2_valid(
            removed_base_mutant,
            ROUTE_TAXONOMY_OVERLAY_V2,
            EFFECTIVE_ROUTE_TAXONOMY_V2,
            getattr(module_03, "CANDIDATE_CLASSES", None),
        ),
        "overlay_collision_rejected": not taxonomy_v2_valid(
            BASE_ROUTE_TAXONOMY_V1,
            collision_overlay_mutant,
            EFFECTIVE_ROUTE_TAXONOMY_V2,
            getattr(module_03, "CANDIDATE_CLASSES", None),
        ),
        "malformed_taxonomy_types_fail_closed": all((
            not taxonomy_v2_valid(
                None,
                ROUTE_TAXONOMY_OVERLAY_V2,
                EFFECTIVE_ROUTE_TAXONOMY_V2,
                getattr(module_03, "CANDIDATE_CLASSES", None),
            ),
            not taxonomy_v2_valid(
                BASE_ROUTE_TAXONOMY_V1,
                [],
                EFFECTIVE_ROUTE_TAXONOMY_V2,
                getattr(module_03, "CANDIDATE_CLASSES", None),
            ),
            not taxonomy_v2_valid(
                BASE_ROUTE_TAXONOMY_V1,
                ROUTE_TAXONOMY_OVERLAY_V2,
                "not-a-registry",
                getattr(module_03, "CANDIDATE_CLASSES", None),
            ),
            not taxonomy_v2_valid(
                BASE_ROUTE_TAXONOMY_V1,
                ROUTE_TAXONOMY_OVERLAY_V2,
                EFFECTIVE_ROUTE_TAXONOMY_V2,
                None,
            ),
        )),
        "wrong_candidate_classification_rejected": (
            not candidate_classification_valid(classification_mutant)
            and not frozen_registry_bundle_valid(
                bundle_mutants["wrong_candidate_classification"]
            )
        ),
        "premature_candidate_pass_rejected": (
            not evaluation_template_open(evaluation_mutant)
            and not frozen_registry_bundle_valid(
                bundle_mutants["premature_candidate_evaluation"]
            )
        ),
    }

    true_contract_closure = expected_runtime_closure(True)
    protected_false_flags = {
        "G2_CORE_ALGEBRA", "G6_PHYSICAL_MATCH", "G7_OBSERVATION", "G8_EXPORT",
        "W2_06_OVERLAY_CLASS_EVALUATED", "W2_06_OVERLAY_CLASS_SATISFIED",
        "W2_06_PROMOTED_TO_W2_F1", "W2_F1_SELF_DIFFERENTIATION",
        "W2_F2_OPERATIONAL_RELATIONS", "W2_F3_INTERNAL_ORDER_CAUSALITY",
        "W2_F4_INDEPENDENT_ADDITIVE_MODES", "W2_M1_DIMENSION_CONTINUUM",
        "W2_M2_LORENTZIAN_METRIC", "W2_A0_EFFECTIVE_ACTION_ORIGIN",
    }
    closure_mutation_results: dict[str, bool] = {}
    for key in protected_false_flags:
        closed = dict(true_contract_closure)
        closed[key] = True
        truthy_closed = dict(true_contract_closure)
        truthy_closed[key] = 1
        closure_mutation_results[key] = all((
            not runtime_closure_valid(closed, True),
            not runtime_closure_valid(truthy_closed, True),
        ))

    checks = {
        "required_contract_and_custom_fields_exact": contract_keyset_exact,
        "contract_values_nonempty": contract_values_nonempty,
        "contract_and_runtime_model_versions_bound": contract_model_bound,
        "contract_custom_registries_exactly_bound": claim_custom_values_bound,
        "contract_static_scope_and_flags_exact": contract_static_flags_exact,
        "dependency_bytes_exact_before_import": dependency_bytes_exact,
        "dependency_runtime_provenance_exact": dependency_provenance_exact,
        "source_boundary_phrases_present": source_boundaries_valid(texts),
        "w2_03_historical_taxonomy_identity_exact": w2_03_identity_valid(module_03),
        "w2_06_conditional_candidate_identity_exact": w2_06_identity_valid(module_06),
        "w2_07_reexecuted_status_checks_and_open_flags_exact": w2_07_report_valid(
            module_07, report_07
        ),
        "critical_registries_independently_digest_bound": (
            registry_hashes_exact and frozen_registry_bundle_valid(current_bundle)
        ),
        "route_neutral_F1_definition_exact": definition_exact,
        "route_neutral_role_semantics_exact": roles_exact,
        "both_witness_kinds_available_without_candidate_bias": witnesses_exact,
        "primitive_law_origin_and_argmin_policy_exact": primitive_policy_exact,
        "taxonomy_v2_exact_noncolliding_superset": taxonomy_exact,
        "w2_06_reclassified_only_for_future_audit": classification_exact,
        "all_w2_06_promotion_obligations_still_open": candidate_evaluation_still_open,
        "preaudit_open_items_honestly_open": preaudit_honest,
        "generic_INTER_CLASS_positive_control_passes": inter_positive,
        "generic_INTRA_CLASS_positive_control_passes": intra_positive,
        "independent_promotion_validator_agrees_on_positives": independent_positives,
        "every_missing_false_and_truthy_gate_mutant_rejected": all(
            gate_mutation_results.values()
        ),
        "extra_gate_mutant_rejected": extra_gate_rejected,
        "every_policy_true_truthy_falsey_nonboolean_and_missing_mutant_rejected": all(
            policy_mutation_results.values()
        ),
        "invalid_witness_law_policy_and_open_template_rejected": bad_labels_rejected,
        "trivial_gauge_prewired_arbitrary_target_temporal_nulls_rejected": all(
            semantic_null_results.values()
        ),
        "definition_taxonomy_classification_and_evaluation_mutants_rejected": all(
            registry_mutation_results.values()
        ),
        "contract_only_runtime_closure_shape_exact": runtime_closure_valid(
            true_contract_closure, True
        ),
        "physical_temporal_downstream_and_export_closure_mutants_rejected": all(
            closure_mutation_results.values()
        ),
    }
    passed = all(type(value) is bool and value is True for value in checks.values())
    closure_flags = expected_runtime_closure(passed)
    closure_self_consistent = runtime_closure_valid(closure_flags, passed)
    status = (
        "W2_F1_PROMOTION_CONTRACT_FROZEN__ATEMPORAL_INTRASTATE_CLASS_ALIGNED__W2_06_ADJUDICATION_OPEN"
        if passed and closure_self_consistent
        else "W2_F1_PROMOTION_CONTRACT_FAIL__PROGRAMME_W2_F1_OPEN"
    )

    return {
        "MODEL_VERSION": MODEL_VERSION,
        "ROUTER_VERSION": ROUTER_VERSION,
        "STATUS": status,
        "CHECKS": checks,
        "PROMOTION_GATE_RESULT": "NOT_APPLIED_TO_W2_06__OPEN_FOR_W2_09",
        "F1_DEFINITION": F1_DEFINITION,
        "F1_ROLE_SEMANTICS": F1_ROLE_SEMANTICS,
        "WITNESS_KINDS": WITNESS_KINDS,
        "PROMOTION_AND_GATES": PROMOTION_AND_GATES,
        "PRIMITIVE_LAW_POLICY": PRIMITIVE_LAW_POLICY,
        "ROUTE_TAXONOMY_OVERLAY_V2": ROUTE_TAXONOMY_OVERLAY_V2,
        "EFFECTIVE_ROUTE_CLASS_NAMES": sorted(EFFECTIVE_ROUTE_TAXONOMY_V2),
        "CANDIDATE_CLASSIFICATION": CANDIDATE_CLASSIFICATION,
        "CANDIDATE_EVALUATION": CANDIDATE_EVALUATION_TEMPLATE,
        "W2_06_PREAUDIT_LEDGER": W2_06_PREAUDIT_LEDGER,
        "POSITIVE_CONTROLS": {
            "INTER_CLASS": inter_positive,
            "INTRA_CLASS": intra_positive,
            "INDEPENDENT_VALIDATOR": independent_positives,
        },
        "GATE_MUTATION_CONTROLS": gate_mutation_results,
        "POLICY_MUTATION_CONTROLS": policy_mutation_results,
        "SEMANTIC_NULL_CONTROLS": semantic_null_results,
        "REGISTRY_MUTATION_CONTROLS": registry_mutation_results,
        "CLOSURE_MUTATION_CONTROLS": closure_mutation_results,
        "DEPENDENCY_STATUS": report_07.get("DEPENDENCY_STATUSES"),
        "DEPENDENCY_VERSIONS": report_07.get("DEPENDENCY_VERSIONS"),
        "DEPENDENCY_SHA256_EXPECTED": EXPECTED_DEPENDENCY_SHA256,
        "REGISTRY_SHA256": actual_registry_hashes,
        "NEXT_ATOMIC_TASK": (
            "w2_09 must adjudicate the exact frozen w2_06 candidate against every w2_08 "
            "promotion gate without changing this F1 definition, witness kind, overlay class "
            "or primitive-law policy; failure keeps w2_06 conditional and all fallbacks open."
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
    return 0 if report["STATUS"].startswith("W2_F1_PROMOTION_CONTRACT_FROZEN") else 1


if __name__ == "__main__":
    raise SystemExit(main())
