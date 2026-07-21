"""Versioned W2-F1 route adjudication after the first exact concrete candidate.

This gate does not decide physical truth.  It compares the prior provisional
generic-seed route with the exact atemporal spectral candidate using a frozen
veto-first evidence rule.  The winner is only the primary route for the next
promotion audit; every non-falsified alternative remains open and the physical
W2_F1 flag remains false.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


MODEL_VERSION = "W2-F1-ROUTE-ADJUDICATION-v2.6-internal"
PRIOR_ROUTE = "SYMMETRIC_BIFURCATION_WITH_TARGET_FREE_GENERIC_SEED"
SELECTED_ROUTE = "ATEMPORAL_SPECTRAL_SPLIT_WITH_UNIQUE_QUOTIENT_MINIMUM"
NO_EXCLUSIVE_PRIMARY = "NO_EXCLUSIVE_PRIMARY"
FROZEN_ROUTE_IDENTITIES = {
    "prior_w2_05_evidence": "SYMMETRIC_BIFURCATION_WITH_TARGET_FREE_GENERIC_SEED",
    "candidate_w2_06_evidence": "ATEMPORAL_SPECTRAL_SPLIT_WITH_UNIQUE_QUOTIENT_MINIMUM",
}

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
    "DECISION_RULE", "MANDATORY_VETOES", "COMMON_AUDIT_OBLIGATIONS",
    "ATEMPORAL_OBLIGATION_MAP", "PROMOTION_OBLIGATIONS", "TRADEOFFS_NOT_SCORED",
    "REVERSAL_TRIGGERS", "SUPERSESSION_RULE", "ROUTE_CLASSIFICATION",
    "PROHIBITED_PRIORITY_BASES", "ROUTE_IDENTITIES",
})

MANDATORY_VETO_KEYS = frozenset({
    "source_boundary_admissible",
    "target_free_inputs",
    "dependency_chain_exact",
    "route_specific_certificate_valid",
    "route_class_status_honest",
    "imported_choices_honestly_open",
    "physical_F1_honestly_open",
    "alternatives_preserved",
})

COMMON_AUDIT_OBLIGATION_KEYS = frozenset({
    "concrete_unlabelled_state_space_and_equivalence",
    "exact_nontrivial_solution_or_outcome_classification",
    "stability_certificate_under_declared_scope",
    "mathematical_inequivalence_certificate_after_declared_equivalence",
    "complete_target_free_realization_or_selection_origin",
})

SEED_ONLY_OBLIGATION_KEYS = frozenset({
    "G_sym_invariant_seed_distribution",
    "individual_nonsymmetric_seed_realization",
    "open_or_nonzero_measure_successful_seed_basin",
    "internal_seed_sampling_or_outcome_mechanism",
})

ALL_EVIDENCE_KEYS = MANDATORY_VETO_KEYS | COMMON_AUDIT_OBLIGATION_KEYS

EXPECTED_DECISION_POLICY = {
    "numeric_score_used": False,
    "weights_used": False,
    "check_count_used": False,
    "recency_used": False,
    "file_order_used": False,
    "route_label_used_as_evidence": False,
    "N3_or_1plus2_priority_bonus_used": False,
    "physical_route_dominance_claimed": False,
    "seed_route_rejected": False,
    "route_class_contract_claimed_satisfied": False,
    "route_specific_obligations_mixed_into_common_profile": False,
}

EXPECTED_NEGATIVE_WINNERS = {
    "failed_math": PRIOR_ROUTE,
    "target_leak": PRIOR_ROUTE,
    "premature_f1": PRIOR_ROUTE,
    "hidden_seed": PRIOR_ROUTE,
    "dependency_failure": PRIOR_ROUTE,
    "hidden_or_derived_N3_import": PRIOR_ROUTE,
    "router_class_laundering": PRIOR_ROUTE,
    "O3_gauge_role_change": PRIOR_ROUTE,
    "empty_promotion_obligations": NO_EXCLUSIVE_PRIMARY,
    "deleted_promotion_obligation": NO_EXCLUSIVE_PRIMARY,
    "duplicated_promotion_obligation": NO_EXCLUSIVE_PRIMARY,
    "fallback_removed": NO_EXCLUSIVE_PRIMARY,
    "truthy_nonboolean_fallback_claim": NO_EXCLUSIVE_PRIMARY,
    "duplicated_obligation": PRIOR_ROUTE,
    "injected_score_evidence": PRIOR_ROUTE,
    "injected_score_policy": NO_EXCLUSIVE_PRIMARY,
    "numeric_score_switch": NO_EXCLUSIVE_PRIMARY,
    "weighted_preference": NO_EXCLUSIVE_PRIMARY,
    "check_count_preference": NO_EXCLUSIVE_PRIMARY,
    "recency_preference": NO_EXCLUSIVE_PRIMARY,
    "file_order_preference": NO_EXCLUSIVE_PRIMARY,
    "route_label_preference": NO_EXCLUSIVE_PRIMARY,
    "N3_or_1plus2_priority_bonus": NO_EXCLUSIVE_PRIMARY,
    "seed_route_rejected": NO_EXCLUSIVE_PRIMARY,
    "physical_dominance_claimed": NO_EXCLUSIVE_PRIMARY,
    "route_class_claimed_satisfied": NO_EXCLUSIVE_PRIMARY,
    "route_specific_obligation_counted_as_common": NO_EXCLUSIVE_PRIMARY,
    "tie": NO_EXCLUSIVE_PRIMARY,
    "incomparable": NO_EXCLUSIVE_PRIMARY,
}

EXPECTED_ATEMPORAL_OBLIGATION_MAP = {
    "single_carrier": "SOURCE_CONSTRAINT_RETAINED",
    "concrete_unlabelled_configuration_space": "CLOSED_CONDITIONAL_W2_06",
    "nontrivial_exact_symmetry_G_sym": "CLOSED_CONDITIONAL_W2_06",
    "G_sym_fixed_symmetric_branch_q0": "CLOSED_CONDITIONAL_W2_06",
    "q0_no_nontrivial_distinguishable_internal_role_or_relational_structure_mod_equivalence": "CLOSED_CONDITIONAL_W2_06",
    "symmetry_role_global_physical_vs_gauge_or_relabel": "CLOSED_AS_INTERNAL_RELABEL_W2_06",
    "target_free_G_sym_invariant_rule_or_functional": "CLOSED_CONDITIONAL_W2_06",
    "open_parameter_domain_with_q0_instability": "CLOSED_CONDITIONAL_W2_06",
    "stable_nonfixed_solution_orbit": "CLOSED_CONDITIONAL_W2_06",
    "G_sym_invariant_seed_distribution": "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE",
    "individual_nonsymmetric_seed_realization": "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE",
    "open_or_nonzero_measure_successful_seed_basin": "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE",
    "internal_seed_sampling_or_outcome_mechanism": "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE",
    "seed_or_selection_origin": "OPEN__ATEMPORAL_GLOBAL_ARGMIN_ORIGIN_UNJUSTIFIED",
    "physical_inequivalence_after_gauge_quotient": "CONDITIONAL_RANK_ROLE_CERTIFICATE__PROMOTION_MEANING_OPEN",
    "no_preferred_direction_or_observed_target_in_inputs": "REQUIRED_GUARD_SATISFIED_W2_06",
}

EXPECTED_PROMOTION_OBLIGATIONS = (
    "freeze_whether_F1_accepts_one_quotient_minimum_with_unequal_internal_rank_roles",
    "resolve_router_mismatch_by_versioned_class_reclassification_or_exact_contract_mapping",
    "justify_Sym0_3_internal_algebra_as_a_RefG_foundation_candidate_not_only_a_toy_representation",
    "justify_global_argmin_as_the_frozen_atemporal_foundation_rule_without_circular_selection",
    "retain_N3_internal_not_spatial_and_Q_sign_choice_as_explicit_imports_or_replace_them_and_test_dimension_family_robustness",
    "justify_orbit_normal_variational_stability_as_the_required_atemporal_F1_stability_not_temporal_persistence",
    "decide_whether_conditional_rank_role_inequivalence_is_physical_enough_for_programme_W2_F1",
)

EXPECTED_ROUTE_CLASSIFICATION = {
    "dependency_registration_label": "atemporal_nonunique_solution_structure",
    "existing_class_contract_satisfied": False,
    "mismatch": (
        "w2_03 requires multiple inequivalent stable solutions, whereas w2_06 proves one "
        "quotient minimum containing two unequal-rank internal sectors"
    ),
    "temporary_audit_bucket": "other_explicit_target_free_mechanism",
    "temporary_bucket_contract_satisfied": False,
    "priority_effect": "NEXT_AUDIT_PRIORITY_ALLOWED_IF_MISMATCH_IS_DISCLOSED",
    "promotion_effect": "PHYSICAL_F1_HARD_VETO_UNTIL_ROUTER_ALIGNMENT_IS_RESOLVED",
}

EXPECTED_PROHIBITED_PRIORITY_BASES = (
    "scalar_score_or_weight",
    "number_of_checks_or_closed_slots",
    "elegance_or_simplicity",
    "file_recency_or_order",
    "route_name_or_prior_label",
    "N3_or_1plus2_resemblance_to_future_space",
    "future_GR_or_observational_target",
    "route_specific_obligation_mislabeled_as_common",
)

EXPECTED_TRADEOFFS = {
    "prior_route_generality": "the seed route commits to less concrete structure but has no concrete passing model",
    "atemporal_import_load": "N=3, internal delta, O(3), matrix algebra, polynomial functional and argmin are imported",
    "quotient_scope": "one quotient minimum survives; the result is unequal role-types, not multiple vacua or objects",
    "dynamical_scope": "atemporal minimization is not a temporal formation history",
    "empirical_scope": "neither route has an F1-level physical observable or data comparison",
}

EXPECTED_REVERSAL_TRIGGERS = (
    "w2_06_exact_falsifier_or_dependency_failure",
    "promotion_audit_rejects_rank_roles_as_the_required_F1_output",
    "imported_internal_algebra_or_argmin_rule_is_found_circular_or_target_laundered",
    "a_concrete_seed_or_other_route_closes_the_same_frozen_F1_meaning_with_strictly_better_health",
    "future_observation_or_downstream_consistency_veto",
)

EXPECTED_FREEDOM_SLOTS = frozenset({
    "candidate_set", "mandatory_veto_rule", "common_obligation_partial_order",
    "tie_rule", "fallback_rule", "promotion_scope", "data_fitted_parameters",
})

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
    "ROUTE_ADJUDICATION_VALIDATED": False,
    "ATEMPORAL_PRIMARY_FOR_NEXT_F1_AUDIT": False,
    "SEED_ROUTE_FALLBACK_OPEN": False,
    "PHYSICAL_ROUTE_DOMINANCE": False,
    "SEED_ROUTE_REJECTED": False,
    "ROUTE_CLASS_CONTRACT_SATISFIED": False,
    "W2_F1_SELF_DIFFERENTIATION": False,
    "W2_F2_OPERATIONAL_RELATIONS": False,
    "W2_F3_INTERNAL_ORDER_CAUSALITY": False,
    "W2_F4_INDEPENDENT_ADDITIVE_MODES": False,
    "W2_M1_DIMENSION_CONTINUUM": False,
    "W2_M2_LORENTZIAN_METRIC": False,
    "W2_A0_EFFECTIVE_ACTION_ORIGIN": False,
}

GATE_APPLICABILITY = {
    "G0_GOAL": "REQUIRED — evidence-ordering claim, vetoes, tie rule and scope are frozen",
    "G1_CONVENTIONS": "REQUIRED — development priority is separated from physical truth and rejection",
    "G2_CORE_ALGEBRA": "N/A — no new physical algebra; exact dependency reports are consumed",
    "G3_STRUCTURE": "REQUIRED — veto-first partial ordering and obligation translation are checked",
    "G4_INDEPENDENT_CHECK": "REQUIRED — live report extraction and the same symmetric adjudicator on invariance and negative controls",
    "G5_LIMITS_REGRESSION": "REQUIRED — tie, incomparable, label/order, score, class-laundering and premature-F1 controls",
    "G6_PHYSICAL_MATCH": "N/A — no source, energy ledger or observable map",
    "G7_OBSERVATION": "N/A — no physical prediction or dataset",
    "G8_EXPORT": "N/A — internal Git-ignored route decision; no Canon/article export authorized",
}

EXPECTED_BRANCHES = {
    SELECTED_ROUTE: "PRIMARY_ONLY_FOR_NEXT_W2_F1_AUDIT__ROUTER_CONTRACT_UNRESOLVED",
    PRIOR_ROUTE: "OPEN_FALLBACK__NOT_REJECTED",
    "symmetric_instability_or_bifurcation": "CLASS_OPEN__SEED_INSTANCE_IS_FALLBACK__NOT_REJECTED",
    "atemporal_nonunique_solution_structure": "ALTERNATIVE_OPEN__NOT_REJECTED",
    "stochastic_or_quantum_outcome": "ALTERNATIVE_OPEN__NOT_REJECTED",
    "state_space_generating_rule": "ALTERNATIVE_OPEN__NOT_REJECTED",
    "nontrivial_relational_state_space": "ALTERNATIVE_OPEN__NOT_REJECTED",
    "other_explicit_target_free_mechanism": "ALTERNATIVE_OPEN__NOT_REJECTED",
    "w2_06_route_class_contract": "UNRESOLVED__NOT_CLAIMED_SATISFIED",
    "programme_physical_W2_F1": "OPEN__NOT_PROMOTED_BY_ROUTE_DECISION",
}

EXPECTED_CLOSURE_KEYS = frozenset(INITIAL_CLOSURE_FLAGS)
EXPECTED_GATE_APPLICABILITY = dict(GATE_APPLICABILITY)


CLAIM_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F1_ROUTE_ADJUDICATION_001",
    "CLAIM": (
        "მიმდინარე გაყინულ მტკიცებულებაში w2_06-ის ატემპორალური სპექტრული გზა "
        "ირჩევა მხოლოდ შემდეგი W2_F1 აუდიტის მთავარ სამუშაო ობიექტად: იგი ყველა სავალდებულო "
        "ვეტოს გადის და საერთო გაყინულ აუდიტის ვალდებულებებზე w2_05-ის ჯერ მხოლოდ სქემურ "
        "გზას მკაცრად მოიცავს, არაფერს ასუსტებს. ეს არის სიმრავლეთა ჩართვით მიღებული "
        "არაწონიანი Pareto-პრიორიტეტი და არა ჩეკების დათვლა. w2_05-ის seed-გზა და სხვა "
        "არაგაბათილებული კლასები ღია fallback-ებად რჩება; ფიზიკური W2_F1 არ იხურება."
    ),
    "TYPE": "ARCHITECTURE_DECISION / EVIDENCE_ORDERING; არა physical mechanism, dominance theorem ან W2_F1 closure",
    "MODEL_VERSION": (
        f"{MODEL_VERSION}; candidate set, evidence, veto, tie, fallback, obligation map, "
        "promotion scope or PASS logic changes require a new version"
    ),
    "ASSUMPTIONS": [
        "w2_05 არის seed-გზის წინა დროებითი პრიორიტეტი და არა უცვლელი ან ფიზიკური ჭეშმარიტება.",
        "w2_06 არის ზუსტი პირობითი ატემპორალური კანდიდატი და programme-wide physical W2_F1-ს არ ხურავს.",
        "განვითარების პრიორიტეტი შეიძლება შეიცვალოს მხოლოდ live მტკიცებულებითა და წინასწარ გაყინული წესით.",
        "საერთო აუდიტის ვალდებულებები და route-specific ღია ფასები ცალ-ცალკე იწერება; რიცხვით score-ში არ ერთიანდება.",
        "w2_06 ვერ ასრულებს atemporal_nonunique_solution_structure კლასის ამჟამინდელ კონტრაქტს: quotient-ში ერთი მინიმუმია და არა რამდენიმე არაეკვივალენტური ამონახსნი.",
        "დაკვირვებითი თავსებადობა ერთადერთი უცვლელი ღერძია; ამ წინაფიზიკურ ეტაპზე data role N/A-ა და მომავალი ვეტო გადაწყვეტილებას აუქმებს."
    ],
    "DOMAIN": (
        "მხოლოდ შემდეგი W2_F1 promotion-audit-ის სამუშაო პრიორიტეტი. არ ირჩევს "
        "სამყაროს ჭეშმარიტ ონტოლოგიას, არ უარყოფს fallback-ებს და არ გადასცემს PASS-ს F2 ან შემდეგ კარიბჭეებს."
    ),
    "CONVENTIONS": (
        "PRIMARY ნიშნავს next-audit priority-ს; OPEN_FALLBACK ნიშნავს ცოცხალ ალტერნატივას; "
        "CLOSED_CONDITIONAL ნიშნავს მხოლოდ w2_06-ის გაყინულ მათემატიკურ დომენს; "
        "NOT_APPLICABLE მხოლოდ ოთხ seed-specific ველს ეხება, ხოლო global-argmin არჩევის "
        "წარმოშობა OPEN რჩება. სხვა route-ში seed-ველები კვლავ სავალდებულოა. არ გამოიყენება "
        "scalar score, თვითნებური weight, ჩეკების რაოდენობა, სიახლე ან N=3/1+2 მსგავსება."
    ),
    "FREEDOM_LEDGER": {
        "candidate_set": {"source": "w2_03/w2_05/w2_06 live registries", "range": "one selected plus all open fallbacks", "scale": "programme", "complexity": "finite declared set"},
        "mandatory_veto_rule": {"source": "CODES and W2-C0", "range": sorted(MANDATORY_VETO_KEYS), "scale": "universal", "complexity": len(MANDATORY_VETO_KEYS)},
        "common_obligation_partial_order": {"source": "frozen methodological choice", "range": sorted(COMMON_AUDIT_OBLIGATION_KEYS), "scale": "decision", "complexity": "set inclusion; never a scalar count"},
        "tie_rule": {"source": "frozen methodological choice", "range": "equal or incomparable profiles yield NO_EXCLUSIVE_PRIMARY", "scale": "decision", "complexity": 1},
        "fallback_rule": {"source": "CODES revision rule", "range": "no nonfalsified route is rejected by priority", "scale": "programme", "complexity": 1},
        "promotion_scope": {"source": "W2-C0 atomic boundary", "range": "next W2_F1 audit only", "scale": "programme", "complexity": 1},
        "data_fitted_parameters": {"source": "N/A — no data", "range": 0, "scale": "data", "complexity": 0},
    },
    "DEPENDENCIES": [
        "w2_03 v1.8: admissible route classes and source boundary",
        "w2_04 v1.7: equivariant fixed-set no-go",
        "w2_05 v1.7: prior provisional seed-route decision and open obligations",
        "w2_06 v1.0: exact atemporal spectral candidate; physical W2_F1 open",
    ],
    "METHOD": (
        "Use one symmetric adjudicator and a veto-first partial order rather than a weighted "
        "score. Among eligible routes, A outranks B only when A's CLOSED common-obligation set "
        "strictly contains B's set. Equal or incomparable sets return NO_EXCLUSIVE_PRIMARY. "
        "Route-specific costs remain outside the common set; promotion obligations and all "
        "nonfalsified alternatives remain explicit."
    ),
    "PASS_CONDITION": [
        "all dependency statuses, versions and physical-F1 flags are reexecuted and exact.",
        "the prior and candidate evidence ledgers are derived from live reports, not hand-marked PASS values.",
        "the symmetric partial order selects the same evidence-rich route under argument-order and route-label changes.",
        "the candidate's CLOSED common obligations strictly contain the prior route's with no regression; no counts or weights are used.",
        "only four seed-specific obligations are N/A; the physical origin of the global-argmin rule remains OPEN.",
        "the current route-class mismatch is detected and disclosed rather than laundered into class conformance.",
        "N=3, 1+2, internal algebra, polarity and argmin remain promotion costs rather than priority bonuses or hidden derivations.",
        "the prior seed route and every other nonfalsified class remain OPEN.",
        "programme-wide physical W2_F1 and every downstream flag remain False."
    ],
    "FAIL_CONDITION": (
        "Any mandatory veto fails, profiles tie or are incomparable, a numeric/count/recency/label "
        "preference enters, the router mismatch is hidden, promotion obligations are hidden, a "
        "fallback is rejected, or route priority is presented as physical closure."
    ),
    "FALSIFIER": (
        "Failure of w2_06, a target/source leak, rejection of its narrow rank-role output by "
        "the frozen F1 meaning, or a concrete alternative with strictly better declared health "
        "reopens this decision under a new version."
    ),
    "RESIDUAL": "0 for exact set/status/obligation and decision-rule checks; physical residual N/A.",
    "ERROR_BOUND": "0 for discrete registry logic; no numerical or observational estimate is made.",
    "VALIDITY_HEALTH": (
        "The decision compares evidentiary readiness, not ontological probability. The atemporal "
        "route carries more committed structure and has one quotient minimum, not multiple "
        "objects. Promotion obligations and reversal triggers remain active."
    ),
    "BRANCHES": dict(EXPECTED_BRANCHES),
    "OBSERVABLE_MAP": "N/A — route priority has no physical observable.",
    "FORWARD_MODEL": "N/A — no ideal-observable-to-data chain.",
    "DATA_ROLE": "N/A — no data used; future observations retain veto authority.",
    "IDENTIFIABILITY": "Exact route names and evidence predicates; physical identifiability N/A.",
    "BENCHMARK": (
        "Ties and incomparable profiles yield no exclusive primary. Invariance controls reverse "
        "argument order and rename routes; negative controls inject failed math, scores, duplicate "
        "obligations, hidden imports, router laundering, physical closure and fallback rejection."
    ),
    "CLOSURE_FLAGS": dict(INITIAL_CLOSURE_FLAGS),
    "GATE_APPLICABILITY": dict(GATE_APPLICABILITY),
    "CROSSCHECK": "Live report extraction plus order/label invariance and synthetic mutations are evaluated by the same symmetric adjudicator used for the real decision.",
    "PROVENANCE": "runtime SHA-256 of sources, w2_03-w2_06 and this source; stdout JSON artifact",
    "FILES": [
        "CODES.md", "Theory_Canon.md", "intuitive/RefG_GE.md",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_03_f1_source_aligned_route_contract.py",
        "RefG/work 2/w2_04_f1_equivariant_fixed_set_no_go_gate.py",
        "RefG/work 2/w2_05_f1_primary_route_specification.py",
        "RefG/work 2/w2_06_f1_atemporal_spectral_split_candidate_gate.py",
        "RefG/work 2/w2_07_f1_route_adjudication_gate.py",
    ],
    "DECISION_RULE": "veto-first strict set inclusion on frozen common obligations; tie or incomparability yields NO_EXCLUSIVE_PRIMARY",
    "MANDATORY_VETOES": sorted(MANDATORY_VETO_KEYS),
    "COMMON_AUDIT_OBLIGATIONS": sorted(COMMON_AUDIT_OBLIGATION_KEYS),
    "ATEMPORAL_OBLIGATION_MAP": dict(EXPECTED_ATEMPORAL_OBLIGATION_MAP),
    "PROMOTION_OBLIGATIONS": list(EXPECTED_PROMOTION_OBLIGATIONS),
    "TRADEOFFS_NOT_SCORED": dict(EXPECTED_TRADEOFFS),
    "REVERSAL_TRIGGERS": list(EXPECTED_REVERSAL_TRIGGERS),
    "ROUTE_CLASSIFICATION": dict(EXPECTED_ROUTE_CLASSIFICATION),
    "PROHIBITED_PRIORITY_BASES": list(EXPECTED_PROHIBITED_PRIORITY_BASES),
    "ROUTE_IDENTITIES": dict(FROZEN_ROUTE_IDENTITIES),
    "SUPERSESSION_RULE": (
        "This file supersedes only w2_05's development-priority choice. It does not rewrite "
        "w2_05 history, inherit physical PASS or reject the seed route."
    ),
}


EXPECTED_FREEDOM_LEDGER = {
    key: copy.deepcopy(value) for key, value in CLAIM_CONTRACT["FREEDOM_LEDGER"].items()
}
_SEPARATELY_BOUND_FIELDS = {
    "MODEL_VERSION", "FREEDOM_LEDGER", "BRANCHES", "CLOSURE_FLAGS",
    "GATE_APPLICABILITY", "ATEMPORAL_OBLIGATION_MAP", "PROMOTION_OBLIGATIONS",
    "TRADEOFFS_NOT_SCORED", "REVERSAL_TRIGGERS", "MANDATORY_VETOES",
    "COMMON_AUDIT_OBLIGATIONS", "ROUTE_CLASSIFICATION",
    "PROHIBITED_PRIORITY_BASES", "ROUTE_IDENTITIES",
}
EXPECTED_SEMANTIC_FIELDS = {
    key: copy.deepcopy(value)
    for key, value in CLAIM_CONTRACT.items()
    if key not in _SEPARATELY_BOUND_FIELDS
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value_present(value: Any) -> bool:
    return bool(value.strip()) if isinstance(value, str) else bool(value)


def text_sequence_valid(value: Any) -> bool:
    return (
        isinstance(value, (list, tuple)) and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def freedom_ledger_valid(ledger: Any) -> bool:
    required = {"source", "range", "scale", "complexity"}
    literal_vetoes = sorted({
        "source_boundary_admissible", "target_free_inputs",
        "dependency_chain_exact", "route_specific_certificate_valid",
        "route_class_status_honest", "imported_choices_honestly_open",
        "physical_F1_honestly_open", "alternatives_preserved",
    })
    literal_common = sorted({
        "concrete_unlabelled_state_space_and_equivalence",
        "exact_nontrivial_solution_or_outcome_classification",
        "stability_certificate_under_declared_scope",
        "mathematical_inequivalence_certificate_after_declared_equivalence",
        "complete_target_free_realization_or_selection_origin",
    })
    literal_ledger = {
        "candidate_set": {
            "source": "w2_03/w2_05/w2_06 live registries",
            "range": "one selected plus all open fallbacks",
            "scale": "programme", "complexity": "finite declared set",
        },
        "mandatory_veto_rule": {
            "source": "CODES and W2-C0", "range": literal_vetoes,
            "scale": "universal", "complexity": 8,
        },
        "common_obligation_partial_order": {
            "source": "frozen methodological choice", "range": literal_common,
            "scale": "decision", "complexity": "set inclusion; never a scalar count",
        },
        "tie_rule": {
            "source": "frozen methodological choice",
            "range": "equal or incomparable profiles yield NO_EXCLUSIVE_PRIMARY",
            "scale": "decision", "complexity": 1,
        },
        "fallback_rule": {
            "source": "CODES revision rule",
            "range": "no nonfalsified route is rejected by priority",
            "scale": "programme", "complexity": 1,
        },
        "promotion_scope": {
            "source": "W2-C0 atomic boundary", "range": "next W2_F1 audit only",
            "scale": "programme", "complexity": 1,
        },
        "data_fitted_parameters": {
            "source": "N/A — no data", "range": 0,
            "scale": "data", "complexity": 0,
        },
    }
    return (
        isinstance(ledger, dict)
        and set(ledger) == set(literal_ledger)
        and EXPECTED_FREEDOM_SLOTS == set(literal_ledger)
        and ledger == literal_ledger
        and EXPECTED_FREEDOM_LEDGER == literal_ledger
        and all(
            isinstance(entry, dict)
            and set(entry) == required
            and all(
                value is not None
                and (not isinstance(value, str) or bool(value.strip()))
                for value in entry.values()
            )
            for entry in ledger.values()
        )
    )


def load_gate(path: Path, module_name: str) -> tuple[Any, dict[str, Any]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.run_gate()


def report_value(report: dict[str, Any], upper: str, lower: str) -> Any:
    return report.get(upper, report.get(lower))


def route_identities_valid(
    prior_route: str,
    candidate_route: str,
    registry: dict[str, str],
) -> bool:
    # Deliberately literal and independent of the mutable module registries:
    # a runtime swap of both route constants must not rewrite this witness.
    literal_registry = {
        "prior_w2_05_evidence": "SYMMETRIC_BIFURCATION_WITH_TARGET_FREE_GENERIC_SEED",
        "candidate_w2_06_evidence": "ATEMPORAL_SPECTRAL_SPLIT_WITH_UNIQUE_QUOTIENT_MINIMUM",
    }
    return (
        registry == literal_registry
        and prior_route == "SYMMETRIC_BIFURCATION_WITH_TARGET_FREE_GENERIC_SEED"
        and candidate_route == "ATEMPORAL_SPECTRAL_SPLIT_WITH_UNIQUE_QUOTIENT_MINIMUM"
    )


def live_route_evidence_identities_valid(
    prior_route: str,
    candidate_route: str,
    registry: dict[str, str],
    prior_report: dict[str, Any],
    candidate_contract: dict[str, Any],
) -> bool:
    return all((
        route_identities_valid(prior_route, candidate_route, registry),
        prior_report.get("PRIMARY_ROUTE")
        == "SYMMETRIC_BIFURCATION_WITH_TARGET_FREE_GENERIC_SEED",
        candidate_contract.get("CLAIM_ID")
        == "W2_F1_ATEMPORAL_SPECTRAL_SPLIT_CANDIDATE_001",
        candidate_contract.get("MODEL_VERSION", "").startswith(
            "W2-F1-ATEMPORAL-SPECTRAL-SPLIT-v1.0-internal;"
        ),
    ))


def promotion_obligations_valid(obligations: Any) -> bool:
    # Independent literal witness: deletion, duplication or replacement cannot
    # self-authorize by mutating EXPECTED_PROMOTION_OBLIGATIONS.
    literal_obligations = (
        "freeze_whether_F1_accepts_one_quotient_minimum_with_unequal_internal_rank_roles",
        "resolve_router_mismatch_by_versioned_class_reclassification_or_exact_contract_mapping",
        "justify_Sym0_3_internal_algebra_as_a_RefG_foundation_candidate_not_only_a_toy_representation",
        "justify_global_argmin_as_the_frozen_atemporal_foundation_rule_without_circular_selection",
        "retain_N3_internal_not_spatial_and_Q_sign_choice_as_explicit_imports_or_replace_them_and_test_dimension_family_robustness",
        "justify_orbit_normal_variational_stability_as_the_required_atemporal_F1_stability_not_temporal_persistence",
        "decide_whether_conditional_rank_role_inequivalence_is_physical_enough_for_programme_W2_F1",
    )
    return isinstance(obligations, (tuple, list)) and tuple(obligations) == literal_obligations


def decision_policy_valid(policy: Any) -> bool:
    # A second, literal witness prevents EXPECTED_DECISION_POLICY from
    # self-authorizing a score, weight, count, recency, label or target bonus.
    forbidden_switches = frozenset({
        "numeric_score_used", "weights_used", "check_count_used",
        "recency_used", "file_order_used", "route_label_used_as_evidence",
        "N3_or_1plus2_priority_bonus_used", "physical_route_dominance_claimed",
        "seed_route_rejected", "route_class_contract_claimed_satisfied",
        "route_specific_obligations_mixed_into_common_profile",
    })
    return (
        isinstance(policy, dict)
        and set(policy) == forbidden_switches
        and all(policy.get(key) is False for key in forbidden_switches)
    )


def atemporal_obligation_map_valid(
    obligation_map: Any,
    prior_obligations: dict[str, str],
    candidate_checks: dict[str, bool],
    candidate_contract: dict[str, Any],
) -> bool:
    """Bind every translated w2_05 obligation to a live w2_06 witness."""
    literal_map = {
        "single_carrier": "SOURCE_CONSTRAINT_RETAINED",
        "concrete_unlabelled_configuration_space": "CLOSED_CONDITIONAL_W2_06",
        "nontrivial_exact_symmetry_G_sym": "CLOSED_CONDITIONAL_W2_06",
        "G_sym_fixed_symmetric_branch_q0": "CLOSED_CONDITIONAL_W2_06",
        "q0_no_nontrivial_distinguishable_internal_role_or_relational_structure_mod_equivalence": "CLOSED_CONDITIONAL_W2_06",
        "symmetry_role_global_physical_vs_gauge_or_relabel": "CLOSED_AS_INTERNAL_RELABEL_W2_06",
        "target_free_G_sym_invariant_rule_or_functional": "CLOSED_CONDITIONAL_W2_06",
        "open_parameter_domain_with_q0_instability": "CLOSED_CONDITIONAL_W2_06",
        "stable_nonfixed_solution_orbit": "CLOSED_CONDITIONAL_W2_06",
        "G_sym_invariant_seed_distribution": "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE",
        "individual_nonsymmetric_seed_realization": "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE",
        "open_or_nonzero_measure_successful_seed_basin": "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE",
        "internal_seed_sampling_or_outcome_mechanism": "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE",
        "seed_or_selection_origin": "OPEN__ATEMPORAL_GLOBAL_ARGMIN_ORIGIN_UNJUSTIFIED",
        "physical_inequivalence_after_gauge_quotient": "CONDITIONAL_RANK_ROLE_CERTIFICATE__PROMOTION_MEANING_OPEN",
        "no_preferred_direction_or_observed_target_in_inputs": "REQUIRED_GUARD_SATISFIED_W2_06",
    }
    literal_seed_only = {
        "G_sym_invariant_seed_distribution",
        "individual_nonsymmetric_seed_realization",
        "open_or_nonzero_measure_successful_seed_basin",
        "internal_seed_sampling_or_outcome_mechanism",
    }
    if obligation_map != literal_map or set(prior_obligations) != set(literal_map):
        return False
    na_keys = {
        key for key, value in obligation_map.items()
        if value == "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE"
    }
    freedom = candidate_contract.get("FREEDOM_LEDGER", {})
    imported = set(candidate_contract.get("IMPORTED_NOT_DERIVED", ()))
    selection_rule = candidate_contract.get("SELECTION_RULE", "")
    live_witnesses = {
        "single_carrier": (
            freedom.get("ontological_carrier_count", {}).get("range") == 1
            and "single_internal_carrier_Q" in imported
        ),
        "concrete_unlabelled_configuration_space": all((
            candidate_checks.get("primitive_registry_values_nonblank") is True,
            candidate_checks.get("O3_invariance_exact") is True,
        )),
        "nontrivial_exact_symmetry_G_sym": candidate_checks.get("O3_invariance_exact") is True,
        "G_sym_fixed_symmetric_branch_q0": candidate_checks.get("origin_stationary_and_strictly_unstable") is True,
        "q0_no_nontrivial_distinguishable_internal_role_or_relational_structure_mod_equivalence": candidate_checks.get("origin_has_no_nontrivial_Q_generated_projector") is True,
        "symmetry_role_global_physical_vs_gauge_or_relabel": candidate_checks.get("faithful_O3_mod_center_action_not_O3_mod_SO3") is True,
        "target_free_G_sym_invariant_rule_or_functional": all((
            candidate_checks.get("target_leakage_absent") is True,
            candidate_checks.get("O3_invariance_exact") is True,
        )),
        "open_parameter_domain_with_q0_instability": candidate_checks.get("origin_stationary_and_strictly_unstable") is True,
        "stable_nonfixed_solution_orbit": all((
            candidate_checks.get("sharp_discriminant_bound_and_global_orbit") is True,
            candidate_checks.get("orbit_normal_hessian_positive_with_only_orbit_zero_modes") is True,
        )),
        "G_sym_invariant_seed_distribution": freedom.get("seed_or_randomness", {}).get("range") == 0,
        "individual_nonsymmetric_seed_realization": "no representative direction" in selection_rule,
        "open_or_nonzero_measure_successful_seed_basin": freedom.get("seed_or_randomness", {}).get("range") == 0,
        "internal_seed_sampling_or_outcome_mechanism": freedom.get("seed_or_randomness", {}).get("range") == 0,
        "seed_or_selection_origin": (
            "atemporal_global_argmin_rule" in imported
            and candidate_contract.get("CLOSURE_FLAGS", {}).get("W2_F1_SELF_DIFFERENTIATION") is False
        ),
        "physical_inequivalence_after_gauge_quotient": all((
            candidate_checks.get("Q_generated_rank_1_rank_2_projectors") is True,
            candidate_contract.get("CLOSURE_FLAGS", {}).get("W2_F1_SELF_DIFFERENTIATION") is False,
        )),
        "no_preferred_direction_or_observed_target_in_inputs": all((
            candidate_checks.get("target_leakage_absent") is True,
            "no representative direction" in selection_rule,
        )),
    }
    return na_keys == literal_seed_only and all(live_witnesses.values())


def route_class_labels_valid(
    classification: Any,
    live_route_classes: set[str],
) -> bool:
    return (
        isinstance(classification, dict)
        and classification.get("dependency_registration_label")
        == "atemporal_nonunique_solution_structure"
        and classification.get("temporary_audit_bucket")
        == "other_explicit_target_free_mechanism"
        and classification.get("dependency_registration_label") in live_route_classes
        and classification.get("temporary_audit_bucket") in live_route_classes
    )


def route_classification_semantics_valid(classification: Any) -> bool:
    literal_classification = {
        "dependency_registration_label": "atemporal_nonunique_solution_structure",
        "existing_class_contract_satisfied": False,
        "mismatch": (
            "w2_03 requires multiple inequivalent stable solutions, whereas w2_06 proves one "
            "quotient minimum containing two unequal-rank internal sectors"
        ),
        "temporary_audit_bucket": "other_explicit_target_free_mechanism",
        "temporary_bucket_contract_satisfied": False,
        "priority_effect": "NEXT_AUDIT_PRIORITY_ALLOWED_IF_MISMATCH_IS_DISCLOSED",
        "promotion_effect": "PHYSICAL_F1_HARD_VETO_UNTIL_ROUTER_ALIGNMENT_IS_RESOLVED",
    }
    return classification == literal_classification


def branch_semantics_valid(branches: Any) -> bool:
    literal_branches = {
        "ATEMPORAL_SPECTRAL_SPLIT_WITH_UNIQUE_QUOTIENT_MINIMUM": (
            "PRIMARY_ONLY_FOR_NEXT_W2_F1_AUDIT__ROUTER_CONTRACT_UNRESOLVED"
        ),
        "SYMMETRIC_BIFURCATION_WITH_TARGET_FREE_GENERIC_SEED": (
            "OPEN_FALLBACK__NOT_REJECTED"
        ),
        "symmetric_instability_or_bifurcation": (
            "CLASS_OPEN__SEED_INSTANCE_IS_FALLBACK__NOT_REJECTED"
        ),
        "atemporal_nonunique_solution_structure": "ALTERNATIVE_OPEN__NOT_REJECTED",
        "stochastic_or_quantum_outcome": "ALTERNATIVE_OPEN__NOT_REJECTED",
        "state_space_generating_rule": "ALTERNATIVE_OPEN__NOT_REJECTED",
        "nontrivial_relational_state_space": "ALTERNATIVE_OPEN__NOT_REJECTED",
        "other_explicit_target_free_mechanism": "ALTERNATIVE_OPEN__NOT_REJECTED",
        "w2_06_route_class_contract": "UNRESOLVED__NOT_CLAIMED_SATISFIED",
        "programme_physical_W2_F1": "OPEN__NOT_PROMOTED_BY_ROUTE_DECISION",
    }
    return branches == literal_branches


def critical_architecture_registries_valid(contract: dict[str, Any]) -> bool:
    literal_common = {
        "concrete_unlabelled_state_space_and_equivalence",
        "exact_nontrivial_solution_or_outcome_classification",
        "stability_certificate_under_declared_scope",
        "mathematical_inequivalence_certificate_after_declared_equivalence",
        "complete_target_free_realization_or_selection_origin",
    }
    literal_vetoes = {
        "source_boundary_admissible", "target_free_inputs",
        "dependency_chain_exact", "route_specific_certificate_valid",
        "route_class_status_honest", "imported_choices_honestly_open",
        "physical_F1_honestly_open", "alternatives_preserved",
    }
    literal_prohibited = (
        "scalar_score_or_weight", "number_of_checks_or_closed_slots",
        "elegance_or_simplicity", "file_recency_or_order",
        "route_name_or_prior_label", "N3_or_1plus2_resemblance_to_future_space",
        "future_GR_or_observational_target",
        "route_specific_obligation_mislabeled_as_common",
    )
    literal_tradeoffs = {
        "prior_route_generality": "the seed route commits to less concrete structure but has no concrete passing model",
        "atemporal_import_load": "N=3, internal delta, O(3), matrix algebra, polynomial functional and argmin are imported",
        "quotient_scope": "one quotient minimum survives; the result is unequal role-types, not multiple vacua or objects",
        "dynamical_scope": "atemporal minimization is not a temporal formation history",
        "empirical_scope": "neither route has an F1-level physical observable or data comparison",
    }
    literal_reversals = (
        "w2_06_exact_falsifier_or_dependency_failure",
        "promotion_audit_rejects_rank_roles_as_the_required_F1_output",
        "imported_internal_algebra_or_argmin_rule_is_found_circular_or_target_laundered",
        "a_concrete_seed_or_other_route_closes_the_same_frozen_F1_meaning_with_strictly_better_health",
        "future_observation_or_downstream_consistency_veto",
    )
    literal_supersession = (
        "This file supersedes only w2_05's development-priority choice. It does not rewrite "
        "w2_05 history, inherit physical PASS or reject the seed route."
    )
    return all((
        COMMON_AUDIT_OBLIGATION_KEYS == literal_common,
        set(contract.get("COMMON_AUDIT_OBLIGATIONS", ())) == literal_common,
        MANDATORY_VETO_KEYS == literal_vetoes,
        set(contract.get("MANDATORY_VETOES", ())) == literal_vetoes,
        tuple(contract.get("PROHIBITED_PRIORITY_BASES", ())) == literal_prohibited,
        contract.get("TRADEOFFS_NOT_SCORED") == literal_tradeoffs,
        tuple(contract.get("REVERSAL_TRIGGERS", ())) == literal_reversals,
        contract.get("SUPERSESSION_RULE") == literal_supersession,
    ))


def initial_closure_flags_valid(flags: Any) -> bool:
    literal_keys = {
        "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
        "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
        "G7_OBSERVATION", "G8_EXPORT", "ROUTE_ADJUDICATION_VALIDATED",
        "ATEMPORAL_PRIMARY_FOR_NEXT_F1_AUDIT", "SEED_ROUTE_FALLBACK_OPEN",
        "PHYSICAL_ROUTE_DOMINANCE", "SEED_ROUTE_REJECTED",
        "ROUTE_CLASS_CONTRACT_SATISFIED", "W2_F1_SELF_DIFFERENTIATION",
        "W2_F2_OPERATIONAL_RELATIONS", "W2_F3_INTERNAL_ORDER_CAUSALITY",
        "W2_F4_INDEPENDENT_ADDITIVE_MODES", "W2_M1_DIMENSION_CONTINUUM",
        "W2_M2_LORENTZIAN_METRIC", "W2_A0_EFFECTIVE_ACTION_ORIGIN",
    }
    return (
        isinstance(flags, dict)
        and set(flags) == literal_keys
        and all(value is False for value in flags.values())
    )


def adjudicate(
    left_name: str,
    left: dict[str, bool],
    right_name: str,
    right: dict[str, bool],
    promotion_obligations: tuple[str, ...] | list[str],
    alternatives_preserved: Any,
    decision_policy: dict[str, bool],
) -> dict[str, Any]:
    """Return an order- and label-neutral veto/Pareto adjudication.

    No scalarization occurs here.  Eligible routes are compared only by strict
    set inclusion of the same frozen common-obligation keys.  Exact evidence
    schemas prevent a duplicated/split obligation or an injected score from
    changing that partial order.
    """
    names_valid = (
        isinstance(left_name, str)
        and bool(left_name.strip())
        and isinstance(right_name, str)
        and bool(right_name.strip())
        and left_name != right_name
    )
    left_schema_exact = set(left) == ALL_EVIDENCE_KEYS
    right_schema_exact = set(right) == ALL_EVIDENCE_KEYS
    policy_exact = decision_policy_valid(decision_policy)
    obligations_valid = promotion_obligations_valid(promotion_obligations)
    left_veto_failures = sorted(
        key for key in MANDATORY_VETO_KEYS if left.get(key) is not True
    )
    right_veto_failures = sorted(
        key for key in MANDATORY_VETO_KEYS if right.get(key) is not True
    )
    left_eligible = left_schema_exact and not left_veto_failures
    right_eligible = right_schema_exact and not right_veto_failures
    left_closed = {
        key for key in COMMON_AUDIT_OBLIGATION_KEYS if left.get(key) is True
    }
    right_closed = {
        key for key in COMMON_AUDIT_OBLIGATION_KEYS if right.get(key) is True
    }

    raw_winner = NO_EXCLUSIVE_PRIMARY
    relation = "NEITHER_ELIGIBLE"
    if left_eligible and right_eligible:
        if left_closed > right_closed:
            raw_winner, relation = left_name, "LEFT_STRICTLY_CONTAINS_RIGHT"
        elif right_closed > left_closed:
            raw_winner, relation = right_name, "RIGHT_STRICTLY_CONTAINS_LEFT"
        elif left_closed == right_closed:
            relation = "EQUAL_COMMON_PROFILES"
        else:
            relation = "INCOMPARABLE_COMMON_PROFILES"
    elif left_eligible:
        raw_winner, relation = left_name, "RIGHT_INELIGIBLE_BY_VETO_OR_SCHEMA"
    elif right_eligible:
        raw_winner, relation = right_name, "LEFT_INELIGIBLE_BY_VETO_OR_SCHEMA"

    global_decision_valid = all((
        names_valid,
        obligations_valid,
        alternatives_preserved is True,
        policy_exact,
    ))
    winner = raw_winner if global_decision_valid else NO_EXCLUSIVE_PRIMARY
    return {
        "exclusive_primary": winner,
        "partial_order_relation": relation,
        "left_name": left_name,
        "right_name": right_name,
        "left_evidence_schema_exact": left_schema_exact,
        "right_evidence_schema_exact": right_schema_exact,
        "left_veto_failures": left_veto_failures,
        "right_veto_failures": right_veto_failures,
        "left_closed_common_obligations": sorted(left_closed),
        "right_closed_common_obligations": sorted(right_closed),
        "promotion_obligations_valid": obligations_valid,
        "alternatives_preserved": alternatives_preserved,
        "decision_policy_exact": policy_exact,
        "route_names_valid": names_valid,
    }


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
        "SOURCE": Path(__file__).resolve(),
    }
    modules: dict[str, Any] = {}
    reports: dict[str, dict[str, Any]] = {}
    for name in ("W2_03", "W2_04", "W2_05", "W2_06"):
        modules[name], reports[name] = load_gate(paths[name], f"{name.lower()}_w2_07_dependency")

    expected_statuses = {
        "W2_03": "ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_G1_AND_PHYSICAL_F1_OPEN",
        "W2_04": "CONDITIONAL_EXACT_FIXED_SET_THEOREM_PASS__INTERNAL__W2_F1_OPEN",
        "W2_05": "PRIMARY_ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_MODEL_AND_W2_F1_OPEN",
        "W2_06": "EXACT_ATEMPORAL_SPECTRAL_CANDIDATE_PASS__W2_F1_PROMOTION_OPEN",
    }
    expected_versions = {
        "W2_03": "W2-F1-SOURCE-ALIGNED-ROUTE-CONTRACT-v1.8-internal",
        "W2_04": "W2-F1-EQUIVARIANT-FIXED-SET-NO-GO-v1.7-internal",
        "W2_05": "W2-F1-PRIMARY-ROUTE-SPEC-v1.7-internal",
        "W2_06": "W2-F1-ATEMPORAL-SPECTRAL-SPLIT-v1.0-internal",
    }
    statuses = {
        name: report_value(report, "STATUS", "status") for name, report in reports.items()
    }
    versions = {
        name: report_value(report, "MODEL_VERSION", "model_version") for name, report in reports.items()
    }
    dependency_chain_exact = all(
        statuses[name] == expected_statuses[name]
        and versions[name] == expected_versions[name]
        for name in expected_statuses
    )
    dependency_f1_open = all(
        report_value(report, "CLOSURE_FLAGS", "closure_flags").get(
            "W2_F1_SELF_DIFFERENTIATION"
        ) is False
        for report in reports.values()
    )
    expected_dependency_check_keys = {
        "W2_03": {
            "required_contract_fields_present", "contract_values_nonempty",
            "required_text_sequences_valid", "contract_and_runtime_model_versions_bound",
            "singleton_no_go_dependency_reexecuted_and_verified", "source_constraints_valid",
            "G0_to_G8_applicability_complete", "contract_and_global_registries_bound",
            "freedom_ledger_schema_complete", "branch_registry_exact",
            "required_current_route_classes_present",
            "all_candidate_classes_have_import_and_derivation_ledgers", "F1_result_not_prewired",
            "deferred_outputs_not_prewired", "forbidden_effective_inputs_absent",
            "downstream_targets_not_prewired", "actual_import_violations_empty",
            "embedded_prewired_negative_control_rejected", "source_phrase_presence_only",
            "initial_closure_flags_false",
        },
        "W2_04": {
            "full_CODES_section_5_contract", "contract_values_nonempty",
            "required_text_sequences_valid", "contract_and_runtime_model_versions_bound",
            "G0_to_G8_applicability_complete", "contract_and_global_registries_bound",
            "freedom_ledger_schema_complete", "branch_registry_exact",
            "conventions_and_freedom_ledger_complete", "direct_universal_proof_declared",
            "independent_stabilizer_inclusion_crosscheck",
            "three_state_exhaustive_stabilizer_inclusion",
            "four_state_exhaustive_stabilizer_inclusion", "route_dependency_status_verified",
            "three_state_C2_action_law", "four_state_C2_action_law",
            "three_state_complete_enumeration", "four_state_complete_enumeration",
            "finite_enumerations_are_controls_not_universal_proof",
            "unique_invariant_minimum_is_fixed", "degenerate_nonfixed_minimum_orbit_control",
            "non_equivariant_escape_detected", "physical_flags_honest",
        },
        "W2_05": {
            "required_contract_fields_present", "contract_values_nonempty",
            "required_text_sequences_valid", "contract_and_runtime_model_versions_bound",
            "G0_to_G8_applicability_complete", "contract_and_global_registries_bound",
            "branch_registry_exact", "real_route_registry_has_no_issues",
            "all_route_obligations_declared", "open_items_honestly_open",
            "alternative_classes_remain_open", "known_toy_limits_complete",
            "freedom_ledger_complete", "route_negative_controls_pass",
            "initial_closure_flags_false", "dependencies_exist",
            "dependency_statuses_reexecuted_and_verified", "dependency_W2_F1_flags_open",
        },
        "W2_06": {
            "required_contract_and_custom_fields_present", "contract_values_nonempty",
            "required_text_sequences_valid", "contract_and_runtime_model_versions_bound",
            "semantic_contract_fields_exactly_bound", "registries_exactly_bound",
            "primitive_registry_values_nonblank", "freedom_ledger_exact_and_complete",
            "G0_to_G8_applicability_complete", "dependencies_reexecuted_status_version_exact",
            "dependency_physical_F1_flags_open", "atemporal_route_registered_and_open",
            "target_leakage_absent", "source_boundary_phrases_present",
            "internal_coordinate_gram_positive", "origin_stationary_and_strictly_unstable",
            "sharp_discriminant_bound_and_global_orbit",
            "independent_stationary_branches_and_energy_order", "O3_invariance_exact",
            "faithful_O3_mod_center_action_not_O3_mod_SO3",
            "orbit_normal_hessian_positive_with_only_orbit_zero_modes",
            "Q_generated_rank_1_rank_2_projectors",
            "origin_has_no_nontrivial_Q_generated_projector",
            "N1_N2_N4_generalN_b0_polarity_coercivity_and_source_controls",
            "all_physical_and_export_flags_honestly_open",
        },
    }
    dependency_check_schemas_exact = all(
        set(reports[name].get("CHECKS", {})) == expected_dependency_check_keys[name]
        for name in expected_dependency_check_keys
    )
    dependency_check_values_strict_true = all(
        all(value is True for value in reports[name]["CHECKS"].values())
        for name in expected_dependency_check_keys
    )
    truthy_fail_report_mutant = copy.deepcopy(reports["W2_06"])
    truthy_fail_report_mutant["CHECKS"][
        "N1_N2_N4_generalN_b0_polarity_coercivity_and_source_controls"
    ] = "FAIL"
    missing_check_report_mutant = copy.deepcopy(reports["W2_06"])
    missing_check_report_mutant["CHECKS"].pop("independent_stationary_branches_and_energy_order")
    extra_check_report_mutant = copy.deepcopy(reports["W2_06"])
    extra_check_report_mutant["CHECKS"]["EXTRA_SELF_AUTHORIZED_CHECK"] = True
    dependency_check_mutants_rejected = all((
        not all(value is True for value in truthy_fail_report_mutant["CHECKS"].values()),
        set(missing_check_report_mutant["CHECKS"]) != expected_dependency_check_keys["W2_06"],
        set(extra_check_report_mutant["CHECKS"]) != expected_dependency_check_keys["W2_06"],
    ))

    all_required_fields = REQUIRED_FIELDS | REQUIRED_CUSTOM_FIELDS
    required_fields_present = all_required_fields.issubset(CLAIM_CONTRACT)
    contract_values_nonempty = all(value_present(CLAIM_CONTRACT.get(key)) for key in all_required_fields)
    text_sequences_valid = all(
        text_sequence_valid(CLAIM_CONTRACT.get(key))
        for key in (
            "ASSUMPTIONS", "DEPENDENCIES", "PASS_CONDITION", "FILES",
            "PROMOTION_OBLIGATIONS", "REVERSAL_TRIGGERS",
        )
    )
    version_bound = (
        isinstance(CLAIM_CONTRACT.get("MODEL_VERSION"), str)
        and CLAIM_CONTRACT["MODEL_VERSION"].startswith(f"{MODEL_VERSION};")
    )
    semantic_contract_bound = all(
        CLAIM_CONTRACT.get(key) == value for key, value in EXPECTED_SEMANTIC_FIELDS.items()
    )
    registries_bound = all((
        CLAIM_CONTRACT.get("BRANCHES") == EXPECTED_BRANCHES,
        CLAIM_CONTRACT.get("ATEMPORAL_OBLIGATION_MAP") == EXPECTED_ATEMPORAL_OBLIGATION_MAP,
        tuple(CLAIM_CONTRACT.get("PROMOTION_OBLIGATIONS", ())) == EXPECTED_PROMOTION_OBLIGATIONS,
        CLAIM_CONTRACT.get("TRADEOFFS_NOT_SCORED") == EXPECTED_TRADEOFFS,
        tuple(CLAIM_CONTRACT.get("REVERSAL_TRIGGERS", ())) == EXPECTED_REVERSAL_TRIGGERS,
        set(CLAIM_CONTRACT.get("MANDATORY_VETOES", ())) == MANDATORY_VETO_KEYS,
        set(CLAIM_CONTRACT.get("COMMON_AUDIT_OBLIGATIONS", ())) == COMMON_AUDIT_OBLIGATION_KEYS,
        CLAIM_CONTRACT.get("ROUTE_CLASSIFICATION") == EXPECTED_ROUTE_CLASSIFICATION,
        tuple(CLAIM_CONTRACT.get("PROHIBITED_PRIORITY_BASES", ())) == EXPECTED_PROHIBITED_PRIORITY_BASES,
        CLAIM_CONTRACT.get("ROUTE_IDENTITIES") == FROZEN_ROUTE_IDENTITIES,
        CLAIM_CONTRACT.get("GATE_APPLICABILITY") == EXPECTED_GATE_APPLICABILITY,
        GATE_APPLICABILITY == EXPECTED_GATE_APPLICABILITY,
        initial_closure_flags_valid(CLAIM_CONTRACT.get("CLOSURE_FLAGS")),
        initial_closure_flags_valid(INITIAL_CLOSURE_FLAGS),
        set(CLAIM_CONTRACT.get("CLOSURE_FLAGS", {})) == EXPECTED_CLOSURE_KEYS,
        set(INITIAL_CLOSURE_FLAGS) == EXPECTED_CLOSURE_KEYS,
    ))
    falsey_zero_closure_mutant = dict(INITIAL_CLOSURE_FLAGS)
    falsey_zero_closure_mutant["W2_F1_SELF_DIFFERENTIATION"] = 0
    falsey_none_closure_mutant = dict(INITIAL_CLOSURE_FLAGS)
    falsey_none_closure_mutant["ROUTE_CLASS_CONTRACT_SATISFIED"] = None
    falsey_empty_closure_mutant = dict(INITIAL_CLOSURE_FLAGS)
    falsey_empty_closure_mutant["G8_EXPORT"] = ""
    falsey_closure_mutants_rejected = all((
        not initial_closure_flags_valid(falsey_zero_closure_mutant),
        not initial_closure_flags_valid(falsey_none_closure_mutant),
        not initial_closure_flags_valid(falsey_empty_closure_mutant),
    ))
    freedom_ledger_complete = freedom_ledger_valid(CLAIM_CONTRACT.get("FREEDOM_LEDGER"))
    promotion_scope_ledger_mutant = copy.deepcopy(CLAIM_CONTRACT["FREEDOM_LEDGER"])
    promotion_scope_ledger_mutant["promotion_scope"]["range"] = "physical W2_F1 closure"
    tie_rule_ledger_mutant = copy.deepcopy(CLAIM_CONTRACT["FREEDOM_LEDGER"])
    tie_rule_ledger_mutant["tie_rule"]["range"] = "prior route wins every tie"
    fallback_ledger_mutant = copy.deepcopy(CLAIM_CONTRACT["FREEDOM_LEDGER"])
    fallback_ledger_mutant["fallback_rule"]["range"] = "seed route rejected"
    weighted_ledger_mutant = copy.deepcopy(CLAIM_CONTRACT["FREEDOM_LEDGER"])
    weighted_ledger_mutant["common_obligation_partial_order"]["complexity"] = (
        "weighted score"
    )
    freedom_ledger_mutants_rejected = all(
        not freedom_ledger_valid(mutant)
        for mutant in (
            promotion_scope_ledger_mutant, tie_rule_ledger_mutant,
            fallback_ledger_mutant, weighted_ledger_mutant,
        )
    )
    critical_registry_semantics_bound = critical_architecture_registries_valid(
        CLAIM_CONTRACT
    )
    common_registry_mutant = copy.deepcopy(CLAIM_CONTRACT)
    common_registry_mutant["COMMON_AUDIT_OBLIGATIONS"] = [
        "w2_06_specific_rank_projector_bonus"
    ]
    veto_registry_mutant = copy.deepcopy(CLAIM_CONTRACT)
    veto_registry_mutant["MANDATORY_VETOES"] = [
        key for key in veto_registry_mutant["MANDATORY_VETOES"]
        if key != "target_free_inputs"
    ]
    prohibited_registry_mutant = copy.deepcopy(CLAIM_CONTRACT)
    prohibited_registry_mutant["PROHIBITED_PRIORITY_BASES"] = [
        key for key in prohibited_registry_mutant["PROHIBITED_PRIORITY_BASES"]
        if key != "scalar_score_or_weight"
    ]
    tradeoff_registry_mutant = copy.deepcopy(CLAIM_CONTRACT)
    tradeoff_registry_mutant["TRADEOFFS_NOT_SCORED"]["atemporal_import_load"] = (
        "N=3 and the 1+2 split are derived and physically preferred"
    )
    reversal_registry_mutant = copy.deepcopy(CLAIM_CONTRACT)
    reversal_registry_mutant["REVERSAL_TRIGGERS"] = []
    supersession_registry_mutant = copy.deepcopy(CLAIM_CONTRACT)
    supersession_registry_mutant["SUPERSESSION_RULE"] = "w2_05 seed route is rejected"
    critical_registry_mutants_rejected = all(
        not critical_architecture_registries_valid(mutant)
        for mutant in (
            common_registry_mutant, veto_registry_mutant,
            prohibited_registry_mutant, tradeoff_registry_mutant,
            reversal_registry_mutant, supersession_registry_mutant,
        )
    )
    local_route_identities_bound = route_identities_valid(
        PRIOR_ROUTE, SELECTED_ROUTE, CLAIM_CONTRACT.get("ROUTE_IDENTITIES", {})
    )
    route_identities_bound = live_route_evidence_identities_valid(
        PRIOR_ROUTE, SELECTED_ROUTE, CLAIM_CONTRACT.get("ROUTE_IDENTITIES", {}),
        reports["W2_05"], modules["W2_06"].CLAIM_CONTRACT,
    )
    swapped_route_identities_rejected = not route_identities_valid(
        SELECTED_ROUTE, PRIOR_ROUTE, CLAIM_CONTRACT.get("ROUTE_IDENTITIES", {})
    )
    wrong_prior_identity_report = dict(reports["W2_05"])
    wrong_prior_identity_report["PRIMARY_ROUTE"] = "WRONG_PRIOR_ROUTE"
    wrong_candidate_identity_contract = dict(modules["W2_06"].CLAIM_CONTRACT)
    wrong_candidate_identity_contract["CLAIM_ID"] = "WRONG_CANDIDATE_CLAIM"
    wrong_live_route_identities_rejected = all((
        not live_route_evidence_identities_valid(
            PRIOR_ROUTE, SELECTED_ROUTE,
            CLAIM_CONTRACT.get("ROUTE_IDENTITIES", {}),
            wrong_prior_identity_report, modules["W2_06"].CLAIM_CONTRACT,
        ),
        not live_route_evidence_identities_valid(
            PRIOR_ROUTE, SELECTED_ROUTE,
            CLAIM_CONTRACT.get("ROUTE_IDENTITIES", {}),
            reports["W2_05"], wrong_candidate_identity_contract,
        ),
    ))
    gate_applicability_complete = (
        set(GATE_APPLICABILITY) == UNIVERSAL_GATES
        and all(isinstance(value, str) and value.strip() for value in GATE_APPLICABILITY.values())
    )

    prior_obligations = reports["W2_05"].get("ROUTE_OBLIGATIONS", {})
    obligation_registry_exact = (
        set(prior_obligations) == set(EXPECTED_ATEMPORAL_OBLIGATION_MAP)
        and set(CLAIM_CONTRACT["ATEMPORAL_OBLIGATION_MAP"]) == set(prior_obligations)
    )
    seed_obligations_really_open = all(
        prior_obligations.get(key) == "OPEN" for key in SEED_ONLY_OBLIGATION_KEYS
    )
    atemporal_seed_fields_na = all(
        CLAIM_CONTRACT["ATEMPORAL_OBLIGATION_MAP"].get(key)
        == "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE"
        for key in SEED_ONLY_OBLIGATION_KEYS
    )
    selection_origin_honestly_open = all((
        prior_obligations.get("seed_or_selection_origin") == "OPEN",
        CLAIM_CONTRACT["ATEMPORAL_OBLIGATION_MAP"].get("seed_or_selection_origin")
        == "OPEN__ATEMPORAL_GLOBAL_ARGMIN_ORIGIN_UNJUSTIFIED",
        "justify_global_argmin_as_the_frozen_atemporal_foundation_rule_without_circular_selection"
        in CLAIM_CONTRACT["PROMOTION_OBLIGATIONS"],
    ))
    atemporal_rule_has_no_seed = all((
        modules["W2_06"].CLAIM_CONTRACT["FREEDOM_LEDGER"]["seed_or_randomness"]["range"] == 0,
        "no representative direction" in modules["W2_06"].CLAIM_CONTRACT["SELECTION_RULE"],
        reports["W2_06"]["CLOSURE_FLAGS"]["W2_F1_SELF_DIFFERENTIATION"] is False,
    ))

    route_classes = set(reports["W2_03"].get("CANDIDATE_CLASSES", {}))
    expected_route_classes = {
        "symmetric_instability_or_bifurcation", "atemporal_nonunique_solution_structure",
        "stochastic_or_quantum_outcome", "state_space_generating_rule",
        "nontrivial_relational_state_space", "other_explicit_target_free_mechanism",
    }
    route_classes_exact = route_classes == expected_route_classes
    candidate_checks = reports["W2_06"]["CHECKS"]
    route_classification = CLAIM_CONTRACT["ROUTE_CLASSIFICATION"]
    registration_label = route_classification["dependency_registration_label"]
    temporary_bucket = route_classification["temporary_audit_bucket"]
    route_class_labels_live_bound = route_class_labels_valid(
        route_classification, route_classes
    )
    route_classification_semantics_bound = route_classification_semantics_valid(
        route_classification
    )
    atemporal_class_contract = reports["W2_03"]["CANDIDATE_CLASSES"].get(
        registration_label, {}
    )
    temporary_class_contract = reports["W2_03"]["CANDIDATE_CLASSES"].get(
        temporary_bucket, {}
    )
    route_class_mismatch_detected = all((
        route_class_labels_live_bound,
        route_classification_semantics_bound,
        "inequivalent_stable_solutions" in atemporal_class_contract.get("must_derive", ()),
        "complete_primitive_and_rule_registry" in temporary_class_contract.get("imports_to_declare", ()),
        "stable_target_free_inequivalent_differentiation" in temporary_class_contract.get("must_derive", ()),
        "noncircularity_and_health" in temporary_class_contract.get("must_derive", ()),
        candidate_checks["sharp_discriminant_bound_and_global_orbit"],
        "quotient minimum is unique" in modules["W2_06"].CLAIM_CONTRACT["SELECTION_RULE"],
        route_classification["existing_class_contract_satisfied"] is False,
        route_classification["temporary_bucket_contract_satisfied"] is False,
        "resolve_router_mismatch_by_versioned_class_reclassification_or_exact_contract_mapping"
        in CLAIM_CONTRACT["PROMOTION_OBLIGATIONS"],
    ))
    bad_registration_mutant = dict(route_classification)
    bad_registration_mutant["dependency_registration_label"] = (
        "nonexistent_registration_label"
    )
    bad_bucket_mutant = dict(route_classification)
    bad_bucket_mutant["temporary_audit_bucket"] = "nonexistent_temporary_bucket"
    bad_route_class_labels_rejected = all((
        not route_class_labels_valid(bad_registration_mutant, route_classes),
        not route_class_labels_valid(bad_bucket_mutant, route_classes),
    ))
    no_mismatch_mutant = dict(route_classification)
    no_mismatch_mutant["mismatch"] = "NO_MISMATCH"
    dominance_mutant = dict(route_classification)
    dominance_mutant["priority_effect"] = "PHYSICAL_ROUTE_DOMINANCE"
    no_promotion_veto_mutant = dict(route_classification)
    no_promotion_veto_mutant["promotion_effect"] = "PHYSICAL_F1_SATISFIED"
    premature_class_closure_mutant = dict(route_classification)
    premature_class_closure_mutant["existing_class_contract_satisfied"] = True
    route_class_semantic_mutants_rejected = all(
        not route_classification_semantics_valid(mutant)
        for mutant in (
            no_mismatch_mutant, dominance_mutant, no_promotion_veto_mutant,
            premature_class_closure_mutant,
        )
    )
    obligation_map_live_bound = atemporal_obligation_map_valid(
        CLAIM_CONTRACT["ATEMPORAL_OBLIGATION_MAP"], prior_obligations,
        candidate_checks, modules["W2_06"].CLAIM_CONTRACT,
    )
    fail_map_mutant = dict(CLAIM_CONTRACT["ATEMPORAL_OBLIGATION_MAP"])
    fail_map_mutant["stable_nonfixed_solution_orbit"] = "FAIL_UNSUPPORTED"
    unsupported_na_mutant = dict(CLAIM_CONTRACT["ATEMPORAL_OBLIGATION_MAP"])
    unsupported_na_mutant["seed_or_selection_origin"] = (
        "NOT_APPLICABLE_ATEMPORAL_UNIQUE_QUOTIENT_RULE"
    )
    physical_closure_mutant = dict(CLAIM_CONTRACT["ATEMPORAL_OBLIGATION_MAP"])
    physical_closure_mutant["physical_inequivalence_after_gauge_quotient"] = (
        "CLOSED_PHYSICAL_W2_F1"
    )
    obligation_map_mutants_rejected = all(
        not atemporal_obligation_map_valid(
            mutant, prior_obligations, candidate_checks,
            modules["W2_06"].CLAIM_CONTRACT,
        )
        for mutant in (fail_map_mutant, unsupported_na_mutant, physical_closure_mutant)
    )
    branch_semantics_bound = branch_semantics_valid(CLAIM_CONTRACT["BRANCHES"])
    selected_branch_mutant = dict(CLAIM_CONTRACT["BRANCHES"])
    selected_branch_mutant[SELECTED_ROUTE] = "PHYSICAL_ROUTE_DOMINANCE"
    class_branch_mutant = dict(CLAIM_CONTRACT["BRANCHES"])
    class_branch_mutant["w2_06_route_class_contract"] = "SATISFIED"
    physical_branch_mutant = dict(CLAIM_CONTRACT["BRANCHES"])
    physical_branch_mutant["programme_physical_W2_F1"] = "CLOSED_PHYSICAL_W2_F1"
    branch_semantic_mutants_rejected = all(
        not branch_semantics_valid(mutant)
        for mutant in (
            selected_branch_mutant, class_branch_mutant, physical_branch_mutant,
        )
    )
    alternatives_preserved = all((
        branch_semantics_bound,
        CLAIM_CONTRACT["BRANCHES"].get(PRIOR_ROUTE) == "OPEN_FALLBACK__NOT_REJECTED",
        CLAIM_CONTRACT["BRANCHES"].get("symmetric_instability_or_bifurcation")
        == "CLASS_OPEN__SEED_INSTANCE_IS_FALLBACK__NOT_REJECTED",
        all(
            CLAIM_CONTRACT["BRANCHES"].get(name) == "ALTERNATIVE_OPEN__NOT_REJECTED"
            for name in (
                "atemporal_nonunique_solution_structure", "stochastic_or_quantum_outcome",
                "state_space_generating_rule", "nontrivial_relational_state_space",
                "other_explicit_target_free_mechanism",
            )
        ),
        route_classes_exact,
    ))

    prior_certificate_valid = all((
        statuses["W2_05"] == expected_statuses["W2_05"],
        set(reports["W2_05"]["CHECKS"]) == expected_dependency_check_keys["W2_05"],
        all(value is True for value in reports["W2_05"]["CHECKS"].values()),
    ))
    candidate_certificate_valid = all((
        statuses["W2_06"] == expected_statuses["W2_06"],
        set(reports["W2_06"]["CHECKS"]) == expected_dependency_check_keys["W2_06"],
        all(value is True for value in reports["W2_06"]["CHECKS"].values()),
    ))
    prior_evidence = {
        "source_boundary_admissible": reports["W2_05"]["CHECKS"]["real_route_registry_has_no_issues"],
        "target_free_inputs": reports["W2_05"]["CHECKS"]["route_negative_controls_pass"],
        "dependency_chain_exact": dependency_chain_exact,
        "route_specific_certificate_valid": prior_certificate_valid,
        "route_class_status_honest": route_classes_exact,
        "imported_choices_honestly_open": obligation_registry_exact,
        "physical_F1_honestly_open": reports["W2_05"]["CLOSURE_FLAGS"]["W2_F1_SELF_DIFFERENTIATION"] is False,
        "alternatives_preserved": reports["W2_05"]["CHECKS"]["alternative_classes_remain_open"],
        "concrete_unlabelled_state_space_and_equivalence": prior_obligations.get("concrete_unlabelled_configuration_space") != "OPEN",
        "exact_nontrivial_solution_or_outcome_classification": False,
        "stability_certificate_under_declared_scope": False,
        "mathematical_inequivalence_certificate_after_declared_equivalence": prior_obligations.get("physical_inequivalence_after_gauge_quotient") != "OPEN",
        "complete_target_free_realization_or_selection_origin": False,
    }
    candidate_evidence = {
        "source_boundary_admissible": candidate_checks["source_boundary_phrases_present"],
        "target_free_inputs": candidate_checks["target_leakage_absent"],
        "dependency_chain_exact": dependency_chain_exact,
        "route_specific_certificate_valid": candidate_certificate_valid,
        "route_class_status_honest": route_class_mismatch_detected,
        "imported_choices_honestly_open": all((
            candidate_checks["registries_exactly_bound"],
            candidate_checks["primitive_registry_values_nonblank"],
            selection_origin_honestly_open,
        )),
        "physical_F1_honestly_open": reports["W2_06"]["CLOSURE_FLAGS"]["W2_F1_SELF_DIFFERENTIATION"] is False,
        "alternatives_preserved": alternatives_preserved,
        "concrete_unlabelled_state_space_and_equivalence": all((
            candidate_checks["primitive_registry_values_nonblank"],
            candidate_checks["O3_invariance_exact"],
            candidate_checks["faithful_O3_mod_center_action_not_O3_mod_SO3"],
            "Sym_0(3,R)" in modules["W2_06"].CLAIM_CONTRACT["DOMAIN"],
        )),
        "exact_nontrivial_solution_or_outcome_classification": candidate_checks["sharp_discriminant_bound_and_global_orbit"],
        "stability_certificate_under_declared_scope": candidate_checks["orbit_normal_hessian_positive_with_only_orbit_zero_modes"],
        "mathematical_inequivalence_certificate_after_declared_equivalence": candidate_checks["Q_generated_rank_1_rank_2_projectors"],
        "complete_target_free_realization_or_selection_origin": False,
    }

    decision_policy = copy.deepcopy(EXPECTED_DECISION_POLICY)
    real_decision = adjudicate(
        PRIOR_ROUTE,
        prior_evidence,
        SELECTED_ROUTE,
        candidate_evidence,
        EXPECTED_PROMOTION_OBLIGATIONS,
        alternatives_preserved,
        decision_policy,
    )

    failed_math = dict(candidate_evidence)
    failed_math["exact_nontrivial_solution_or_outcome_classification"] = False
    failed_math["route_specific_certificate_valid"] = False
    target_leak = dict(candidate_evidence)
    target_leak["target_free_inputs"] = False
    premature_f1 = dict(candidate_evidence)
    premature_f1["physical_F1_honestly_open"] = False
    hidden_seed = dict(candidate_evidence)
    hidden_seed["route_specific_certificate_valid"] = False
    dependency_failure = dict(candidate_evidence)
    dependency_failure["dependency_chain_exact"] = False
    hidden_import = dict(candidate_evidence)
    hidden_import["imported_choices_honestly_open"] = False
    class_laundering = dict(candidate_evidence)
    class_laundering["route_class_status_honest"] = False
    gauge_role_change = dict(candidate_evidence)
    gauge_role_change["route_specific_certificate_valid"] = False
    duplicated_obligation = dict(candidate_evidence)
    duplicated_obligation["exact_nontrivial_solution_or_outcome_classification_duplicate"] = True
    injected_score = dict(candidate_evidence)
    injected_score["score"] = True
    tied_candidate = dict(prior_evidence)
    incomparable_left = dict(prior_evidence)
    incomparable_right = dict(prior_evidence)
    incomparable_left["concrete_unlabelled_state_space_and_equivalence"] = True
    incomparable_right["exact_nontrivial_solution_or_outcome_classification"] = True
    policy_with_score = dict(decision_policy)
    policy_with_score["scalar_score"] = True
    policy_numeric_score = dict(decision_policy)
    policy_numeric_score["numeric_score_used"] = True
    policy_with_weight = dict(decision_policy)
    policy_with_weight["weights_used"] = True
    policy_with_check_count = dict(decision_policy)
    policy_with_check_count["check_count_used"] = True
    policy_with_recency = dict(decision_policy)
    policy_with_recency["recency_used"] = True
    policy_with_file_order = dict(decision_policy)
    policy_with_file_order["file_order_used"] = True
    policy_with_route_label = dict(decision_policy)
    policy_with_route_label["route_label_used_as_evidence"] = True
    policy_with_N3_bonus = dict(decision_policy)
    policy_with_N3_bonus["N3_or_1plus2_priority_bonus_used"] = True
    policy_rejects_seed = dict(decision_policy)
    policy_rejects_seed["seed_route_rejected"] = True
    policy_claims_dominance = dict(decision_policy)
    policy_claims_dominance["physical_route_dominance_claimed"] = True
    policy_claims_class = dict(decision_policy)
    policy_claims_class["route_class_contract_claimed_satisfied"] = True
    policy_mixes_route_specific = dict(decision_policy)
    policy_mixes_route_specific["route_specific_obligations_mixed_into_common_profile"] = True

    reverse_argument_order = adjudicate(
        SELECTED_ROUTE, candidate_evidence, PRIOR_ROUTE, prior_evidence,
        EXPECTED_PROMOTION_OBLIGATIONS, alternatives_preserved, decision_policy,
    )
    renamed_routes = adjudicate(
        "EVIDENCE_RICH_ROUTE", candidate_evidence,
        "SCHEMA_ONLY_ROUTE", prior_evidence,
        EXPECTED_PROMOTION_OBLIGATIONS, alternatives_preserved, decision_policy,
    )
    reverse_key_order = adjudicate(
        PRIOR_ROUTE, dict(reversed(list(prior_evidence.items()))),
        SELECTED_ROUTE, dict(reversed(list(candidate_evidence.items()))),
        EXPECTED_PROMOTION_OBLIGATIONS, alternatives_preserved, decision_policy,
    )
    invariance_controls = {
        "argument_order_reversal": reverse_argument_order,
        "route_renaming": renamed_routes,
        "evidence_key_order_reversal": reverse_key_order,
    }
    invariance_controls_pass = all((
        reverse_argument_order["exclusive_primary"] == SELECTED_ROUTE,
        renamed_routes["exclusive_primary"] == "EVIDENCE_RICH_ROUTE",
        reverse_key_order["exclusive_primary"] == SELECTED_ROUTE,
    ))

    hypothetical_complete_seed = dict(candidate_evidence)
    hypothetical_complete_seed["complete_target_free_realization_or_selection_origin"] = True
    better_seed_forward = adjudicate(
        SELECTED_ROUTE, candidate_evidence,
        "HYPOTHETICAL_COMPLETE_SEED_ROUTE", hypothetical_complete_seed,
        EXPECTED_PROMOTION_OBLIGATIONS, alternatives_preserved, decision_policy,
    )
    better_seed_reversed = adjudicate(
        "HYPOTHETICAL_COMPLETE_SEED_ROUTE", hypothetical_complete_seed,
        SELECTED_ROUTE, candidate_evidence,
        EXPECTED_PROMOTION_OBLIGATIONS, alternatives_preserved, decision_policy,
    )
    reversal_controls = {
        "concrete_seed_strictly_contains_atemporal": better_seed_forward,
        "same_reversal_under_argument_order_swap": better_seed_reversed,
    }
    reversal_controls_pass = all((
        better_seed_forward["exclusive_primary"] == "HYPOTHETICAL_COMPLETE_SEED_ROUTE",
        better_seed_reversed["exclusive_primary"] == "HYPOTHETICAL_COMPLETE_SEED_ROUTE",
    ))

    def compare_candidate(
        evidence: dict[str, bool],
        obligations: tuple[str, ...] | list[str] = EXPECTED_PROMOTION_OBLIGATIONS,
        keep_alternatives: Any = alternatives_preserved,
        policy: dict[str, bool] = decision_policy,
    ) -> dict[str, Any]:
        return adjudicate(
            PRIOR_ROUTE, prior_evidence, SELECTED_ROUTE, evidence,
            obligations, keep_alternatives, policy,
        )

    controls = {
        "failed_math": compare_candidate(failed_math),
        "target_leak": compare_candidate(target_leak),
        "premature_f1": compare_candidate(premature_f1),
        "hidden_seed": compare_candidate(hidden_seed),
        "dependency_failure": compare_candidate(dependency_failure),
        "hidden_or_derived_N3_import": compare_candidate(hidden_import),
        "router_class_laundering": compare_candidate(class_laundering),
        "O3_gauge_role_change": compare_candidate(gauge_role_change),
        "empty_promotion_obligations": compare_candidate(candidate_evidence, obligations=()),
        "deleted_promotion_obligation": compare_candidate(
            candidate_evidence, obligations=EXPECTED_PROMOTION_OBLIGATIONS[:-1]
        ),
        "duplicated_promotion_obligation": compare_candidate(
            candidate_evidence,
            obligations=EXPECTED_PROMOTION_OBLIGATIONS + (EXPECTED_PROMOTION_OBLIGATIONS[-1],),
        ),
        "fallback_removed": compare_candidate(candidate_evidence, keep_alternatives=False),
        "truthy_nonboolean_fallback_claim": compare_candidate(
            candidate_evidence, keep_alternatives="NO"
        ),
        "duplicated_obligation": compare_candidate(duplicated_obligation),
        "injected_score_evidence": compare_candidate(injected_score),
        "injected_score_policy": compare_candidate(candidate_evidence, policy=policy_with_score),
        "numeric_score_switch": compare_candidate(candidate_evidence, policy=policy_numeric_score),
        "weighted_preference": compare_candidate(candidate_evidence, policy=policy_with_weight),
        "check_count_preference": compare_candidate(candidate_evidence, policy=policy_with_check_count),
        "recency_preference": compare_candidate(candidate_evidence, policy=policy_with_recency),
        "file_order_preference": compare_candidate(candidate_evidence, policy=policy_with_file_order),
        "route_label_preference": compare_candidate(candidate_evidence, policy=policy_with_route_label),
        "N3_or_1plus2_priority_bonus": compare_candidate(candidate_evidence, policy=policy_with_N3_bonus),
        "seed_route_rejected": compare_candidate(candidate_evidence, policy=policy_rejects_seed),
        "physical_dominance_claimed": compare_candidate(candidate_evidence, policy=policy_claims_dominance),
        "route_class_claimed_satisfied": compare_candidate(candidate_evidence, policy=policy_claims_class),
        "route_specific_obligation_counted_as_common": compare_candidate(candidate_evidence, policy=policy_mixes_route_specific),
        "tie": compare_candidate(tied_candidate),
        "incomparable": adjudicate(
            "LEFT_ROUTE", incomparable_left, "RIGHT_ROUTE", incomparable_right,
            EXPECTED_PROMOTION_OBLIGATIONS, alternatives_preserved, decision_policy,
        ),
    }
    negative_controls_pass = all((
        set(controls) == set(EXPECTED_NEGATIVE_WINNERS),
        all(
            controls[name]["exclusive_primary"] == expected_winner
            for name, expected_winner in EXPECTED_NEGATIVE_WINNERS.items()
        ),
    ))

    source_rule_present = all((
        "ყველაფერი სხვა გადასინჯვადია" in paths["CODES"].read_text(encoding="utf-8"),
        "დროის არმქონე კანდიდატში თვითგარჩევა შეიძლება იყოს ამონახსნთა სტრუქტურული არჩევა" in paths["W2_C0"].read_text(encoding="utf-8"),
        "ერთი წინასივრცითი და წინასაათური ფუძის" in paths["INTUITIVE"].read_text(encoding="utf-8"),
    ))
    promotion_costs_explicit = all(
        value_present(value) for value in CLAIM_CONTRACT["TRADEOFFS_NOT_SCORED"].values()
    ) and bool(CLAIM_CONTRACT["PROMOTION_OBLIGATIONS"])

    decision_pass = all((
        required_fields_present, contract_values_nonempty, text_sequences_valid,
        version_bound, semantic_contract_bound, registries_bound,
        falsey_closure_mutants_rejected,
        freedom_ledger_complete, freedom_ledger_mutants_rejected,
        critical_registry_semantics_bound,
        critical_registry_mutants_rejected, local_route_identities_bound,
        route_identities_bound, swapped_route_identities_rejected,
        wrong_live_route_identities_rejected, gate_applicability_complete,
        dependency_chain_exact, dependency_f1_open,
        dependency_check_schemas_exact, dependency_check_values_strict_true,
        dependency_check_mutants_rejected, obligation_registry_exact,
        seed_obligations_really_open, atemporal_seed_fields_na,
        selection_origin_honestly_open, atemporal_rule_has_no_seed,
        route_classes_exact, route_class_labels_live_bound,
        route_classification_semantics_bound, bad_route_class_labels_rejected,
        route_class_semantic_mutants_rejected, route_class_mismatch_detected,
        obligation_map_live_bound, obligation_map_mutants_rejected,
        branch_semantics_bound, branch_semantic_mutants_rejected,
        alternatives_preserved, source_rule_present, promotion_costs_explicit,
        real_decision["exclusive_primary"] == SELECTED_ROUTE,
        invariance_controls_pass, reversal_controls_pass, negative_controls_pass,
    ))

    closure_flags = dict(INITIAL_CLOSURE_FLAGS)
    closure_flags["G0_GOAL"] = all((
        required_fields_present, contract_values_nonempty, text_sequences_valid,
        version_bound, semantic_contract_bound, registries_bound,
        falsey_closure_mutants_rejected,
        freedom_ledger_complete, freedom_ledger_mutants_rejected,
        critical_registry_semantics_bound,
        critical_registry_mutants_rejected, local_route_identities_bound,
        route_identities_bound, swapped_route_identities_rejected,
        wrong_live_route_identities_rejected, gate_applicability_complete,
    ))
    closure_flags["G1_CONVENTIONS"] = closure_flags["G0_GOAL"] and all((
        dependency_chain_exact, dependency_f1_open,
        dependency_check_schemas_exact, dependency_check_values_strict_true,
        dependency_check_mutants_rejected, source_rule_present,
    ))
    closure_flags["G3_STRUCTURE"] = closure_flags["G1_CONVENTIONS"] and all((
        obligation_registry_exact, seed_obligations_really_open,
        atemporal_seed_fields_na, selection_origin_honestly_open,
        atemporal_rule_has_no_seed, obligation_map_live_bound,
        obligation_map_mutants_rejected, route_classes_exact,
        route_class_labels_live_bound, route_classification_semantics_bound,
        bad_route_class_labels_rejected, route_class_semantic_mutants_rejected,
        route_class_mismatch_detected, branch_semantics_bound,
        branch_semantic_mutants_rejected, alternatives_preserved,
        promotion_costs_explicit,
        real_decision["exclusive_primary"] == SELECTED_ROUTE,
    ))
    closure_flags["G4_INDEPENDENT_CHECK"] = (
        closure_flags["G3_STRUCTURE"]
        and invariance_controls_pass
        and reversal_controls_pass
    )
    closure_flags["G5_LIMITS_REGRESSION"] = (
        closure_flags["G4_INDEPENDENT_CHECK"] and negative_controls_pass
    )
    closure_flags["ROUTE_ADJUDICATION_VALIDATED"] = decision_pass
    closure_flags["ATEMPORAL_PRIMARY_FOR_NEXT_F1_AUDIT"] = decision_pass
    closure_flags["SEED_ROUTE_FALLBACK_OPEN"] = decision_pass and alternatives_preserved
    physical_flags_honest = all(
        closure_flags[key] is False for key in (
            "W2_F1_SELF_DIFFERENTIATION", "W2_F2_OPERATIONAL_RELATIONS",
            "W2_F3_INTERNAL_ORDER_CAUSALITY", "W2_F4_INDEPENDENT_ADDITIVE_MODES",
            "W2_M1_DIMENSION_CONTINUUM", "W2_M2_LORENTZIAN_METRIC",
            "W2_A0_EFFECTIVE_ACTION_ORIGIN", "G6_PHYSICAL_MATCH",
            "G7_OBSERVATION", "G8_EXPORT", "PHYSICAL_ROUTE_DOMINANCE",
            "SEED_ROUTE_REJECTED", "ROUTE_CLASS_CONTRACT_SATISFIED",
        )
    )
    certified_pass = decision_pass and physical_flags_honest

    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": (
            "ATEMPORAL_CANDIDATE_SELECTED_FOR_NEXT_F1_ADJUDICATION__SEED_ROUTE_OPEN_FALLBACK__PHYSICAL_W2_F1_OPEN"
            if certified_pass
            else "ROUTE_ADJUDICATION_FAIL__PHYSICAL_F1_OPEN"
        ),
        "SELECTED_ROUTE": SELECTED_ROUTE if certified_pass else "NONE",
        "PRIOR_ROUTE": PRIOR_ROUTE,
        "CHECKS": {
            "required_contract_and_custom_fields_present": required_fields_present,
            "contract_values_nonempty": contract_values_nonempty,
            "required_text_sequences_valid": text_sequences_valid,
            "contract_and_runtime_model_versions_bound": version_bound,
            "semantic_contract_fields_exactly_bound": semantic_contract_bound,
            "registries_exactly_bound": registries_bound,
            "zero_None_and_empty_string_closure_flag_mutants_rejected": falsey_closure_mutants_rejected,
            "freedom_ledger_exact_and_complete": freedom_ledger_complete,
            "promotion_scope_tie_fallback_and_weighted_ledger_mutants_rejected": freedom_ledger_mutants_rejected,
            "critical_common_veto_tradeoff_reversal_and_supersession_registries_exact": critical_registry_semantics_bound,
            "critical_architecture_registry_mutants_rejected": critical_registry_mutants_rejected,
            "local_route_identity_registry_exact": local_route_identities_bound,
            "w2_05_w2_06_route_evidence_identities_exactly_bound": route_identities_bound,
            "route_identity_swap_rejected": swapped_route_identities_rejected,
            "wrong_live_w2_05_and_w2_06_identity_mutants_rejected": wrong_live_route_identities_rejected,
            "G0_to_G8_applicability_complete": gate_applicability_complete,
            "dependencies_reexecuted_status_version_exact": dependency_chain_exact,
            "dependency_physical_F1_flags_open": dependency_f1_open,
            "dependency_check_schemas_exact": dependency_check_schemas_exact,
            "every_dependency_check_value_is_boolean_True": dependency_check_values_strict_true,
            "truthy_FAIL_missing_and_extra_dependency_check_mutants_rejected": dependency_check_mutants_rejected,
            "prior_obligation_registry_exact": obligation_registry_exact,
            "prior_seed_obligations_really_open": seed_obligations_really_open,
            "four_seed_specific_fields_NA_only_under_atemporal_rule": atemporal_seed_fields_na,
            "global_argmin_selection_origin_honestly_open": selection_origin_honestly_open,
            "atemporal_rule_needs_no_seed_or_orientation": atemporal_rule_has_no_seed,
            "all_translated_obligation_statuses_bound_to_live_witnesses": obligation_map_live_bound,
            "FAIL_unsupported_NA_and_physical_closure_map_mutants_rejected": obligation_map_mutants_rejected,
            "route_class_registry_exact": route_classes_exact,
            "route_registration_and_temporary_bucket_labels_live_bound": route_class_labels_live_bound,
            "route_class_mismatch_priority_and_promotion_semantics_exact": route_classification_semantics_bound,
            "nonexistent_route_class_labels_rejected": bad_route_class_labels_rejected,
            "route_class_semantic_laundering_mutants_rejected": route_class_semantic_mutants_rejected,
            "route_class_contract_mismatch_detected_and_disclosed": route_class_mismatch_detected,
            "all_branch_status_semantics_exact": branch_semantics_bound,
            "physical_dominance_class_closure_and_F1_branch_mutants_rejected": branch_semantic_mutants_rejected,
            "all_nonfalsified_alternatives_preserved": alternatives_preserved,
            "source_revision_and_atemporal_rules_present": source_rule_present,
            "promotion_costs_and_obligations_explicit": promotion_costs_explicit,
            "real_veto_Pareto_decision_selects_atemporal": real_decision["exclusive_primary"] == SELECTED_ROUTE,
            "argument_label_and_key_order_invariance_controls_pass": invariance_controls_pass,
            "hypothetical_better_seed_route_reverses_priority": reversal_controls_pass,
            "negative_tie_and_incomparable_controls_reject_false_primary": negative_controls_pass,
            "all_physical_and_export_flags_honestly_open": physical_flags_honest,
        },
        "PRIOR_EVIDENCE": prior_evidence,
        "CANDIDATE_EVIDENCE": candidate_evidence,
        "ROUTE_IDENTITIES": dict(FROZEN_ROUTE_IDENTITIES),
        "DECISION": real_decision,
        "DECISION_POLICY": decision_policy,
        "INVARIANCE_CONTROLS": invariance_controls,
        "REVERSAL_CONTROLS": reversal_controls,
        "NEGATIVE_CONTROLS": controls,
        "EXPECTED_NEGATIVE_WINNERS": dict(EXPECTED_NEGATIVE_WINNERS),
        "ATEMPORAL_OBLIGATION_MAP": EXPECTED_ATEMPORAL_OBLIGATION_MAP,
        "ROUTE_CLASSIFICATION": EXPECTED_ROUTE_CLASSIFICATION,
        "PROMOTION_OBLIGATIONS": list(EXPECTED_PROMOTION_OBLIGATIONS),
        "PROHIBITED_PRIORITY_BASES": list(EXPECTED_PROHIBITED_PRIORITY_BASES),
        "TRADEOFFS_NOT_SCORED": EXPECTED_TRADEOFFS,
        "REVERSAL_TRIGGERS": list(EXPECTED_REVERSAL_TRIGGERS),
        "DEPENDENCY_STATUSES": statuses,
        "DEPENDENCY_VERSIONS": versions,
        "NEXT_ATOMIC_TASK": (
            "First freeze the exact programme-level meaning of W2_F1 and resolve the router "
            "mismatch. Then audit whether one quotient minimum with unequal-rank internal "
            "roles, the imported Sym_0(3)/N=3/O(3) algebra, orbit-normal stability and the "
            "global-argmin law suffice for physical F1; otherwise return to an open fallback."
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
    return 0 if report["STATUS"].startswith("ATEMPORAL_CANDIDATE_SELECTED") else 1


if __name__ == "__main__":
    raise SystemExit(main())
