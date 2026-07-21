"""Route-neutral contract for promoting a candidate to programme-level W2-F1.

This is a scientific definition and scope boundary, not a promotion result.
It allows either several inequivalent accepted outcomes or canonical,
nonexchangeable roles inside one accepted quotient class.  Candidate-specific
features such as N=3 or a 1+2 split are forbidden from defining F1.
"""
from __future__ import annotations

import copy
import json
import sys
from typing import Any


MODEL_VERSION = "W2-F1-PHYSICAL-PROMOTION-CONTRACT-v1.0-scientific"
ROUTER_VERSION = "W2-F1-ROUTE-TAXONOMY-v2.0-scientific"
NEW_ROUTE_CLASS = "atemporal_intrastate_invariant_role_structure"
W2_06_CANDIDATE_ID = "W2_F1_ATEMPORAL_SPECTRAL_SPLIT_CANDIDATE_001"

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
        "A fully declared target-free law of one pre-spatiotemporal foundation "
        "yields, on nonzero declared support, a structurally stable accepted "
        "structure with intrinsic differentiation absent from the undifferentiated input."
    ),
    "inter_class_route": "multiple inequivalent accepted outcomes may witness differentiation",
    "intra_class_route": (
        "one unique quotient state may witness differentiation through canonical "
        "coexisting roles; multiple vacua are not required"
    ),
    "physical_ceiling": (
        "F1 establishes only candidate-level intrinsic roles; operational distinction, "
        "nodes, relations, time, locality, modes, spacetime, and observables remain open"
    ),
    "proof_strength": "structural self-differentiation relative to declared frozen primitives",
}

F1_ROLE_SEMANTICS = {
    "generated_from_output": (
        "roles are canonical functions of the accepted state and law, not fixed basis vectors, "
        "labels, or an input direct-sum partition"
    ),
    "absent_at_reference": (
        "the undifferentiated reference has no nontrivial canonical role witness; a route "
        "without such a reference must prove the same no-preloading statement"
    ),
    "full_equivalence": "no declared gauge, relabelling, or automorphism exchanges the roles",
    "intrinsic_invariant": "inequivalence is certified without downstream semantic labels",
    "law_relevance": "the accepted law forces the role pattern; an arbitrary split is insufficient",
    "structural_stability": (
        "the witness persists under declared admissible perturbations; no temporal claim follows"
    ),
}

PROMOTION_AND_GATES = {
    "f1_definition_frozen_route_neutral": "definition contains no candidate-specific target",
    "witness_kind_frozen_before_evaluation": "INTER_CLASS or INTRA_CLASS fixed before evaluation",
    "complete_one_foundation_primitive_freedom_registry": "all primitives and imports declared",
    "forbidden_target_intersection_empty": "no F2+, spacetime, GR, observation, or desired role input",
    "undifferentiated_reference_trivial": "reference has no nontrivial canonical role witness",
    "target_free_law_certified": "law and invariant ledger are target-free",
    "complete_output_classification": "all accepted and excluded output classes classified",
    "intrinsic_differentiation_certified": "nontrivial output-generated witness exists",
    "inequivalence_survives_full_quotient": "difference survives every declared equivalence",
    "law_relevance_not_arbitrary_decomposition": "law forces rather than merely permits the split",
    "realization_or_selection_noncircular": "selection account has no hidden target or representative",
    "open_domain_stability_and_robustness": "witness holds on nonzero open support",
    "foundation_admissibility_and_import_health": "imports are honest and not future-geometry laundering",
    "router_extension_aligned": "candidate satisfies one exact route-class contract",
    "independent_crosscheck_and_controls": "independent proof and boundary/null controls pass",
    "candidate_falsifier_absent": "the predeclared strict falsifier is not realized",
    "f1_only_scope_honest": "no F2, temporal, spacetime, gravity, or observational claim is inherited",
}

PRIMITIVE_LAW_POLICY = {
    "allowed_origin_statuses": (
        "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED",
        "DERIVED_BY_SEPARATE_FROZEN_GATE",
    ),
    "no_infinite_regress": (
        "F1 may establish consequences relative to declared primitives without pretending "
        "that every primitive was derived"
    ),
    "primitive_admissibility": (
        "an imported law must be predeclared, target-free, uniform, noncircular, "
        "fully registered, and tested on an open domain"
    ),
    "argmin_guard": (
        "a unique argmin cannot justify its own law; target orbit, target rank, "
        "post-output terms, tuned points, and hidden tie-breakers are forbidden"
    ),
    "status_ceiling": (
        "an imported admissible law remains IMPORTED_NOT_DERIVED even when its consequences are exact"
    ),
}

BASE_ROUTE_TAXONOMY = {
    "symmetric_instability_or_bifurcation": {
        "imports_to_declare": (
            "configuration space", "nontrivial symmetry", "symmetric branch", "invariant rule",
        ),
        "must_derive": ("open-domain instability", "stable inequivalent branch", "target-free selection"),
    },
    "atemporal_nonunique_solution_structure": {
        "imports_to_declare": ("solution space", "equivalence rule", "self-consistency law"),
        "must_derive": ("inequivalent stable quotient solutions", "noncircular selection"),
    },
    "stochastic_or_quantum_outcome": {
        "imports_to_declare": ("state space", "symmetric probability or state", "outcome rule"),
        "must_derive": ("internal outcomes", "stable inequivalence", "no preferred injection"),
    },
    "state_space_generating_rule": {
        "imports_to_declare": ("generative grammar", "equivalence rule"),
        "must_derive": ("nontrivial generated states", "stable inequivalence", "consistency"),
    },
    "nontrivial_relational_state_space": {
        "imports_to_declare": ("relational state space", "relabel equivalence", "law"),
        "must_derive": ("stable inequivalent relational sectors", "no node or trace preloading"),
    },
    "other_explicit_target_free_mechanism": {
        "imports_to_declare": ("complete primitive and rule registry",),
        "must_derive": (
            "stable target-free inequivalent differentiation", "noncircularity and health",
        ),
    },
}

ROUTE_TAXONOMY_OVERLAY = {
    NEW_ROUTE_CLASS: {
        "imports_to_declare": (
            "one-foundation internal state space",
            "complete equivalence rule",
            "undifferentiated reference or no-preloading certificate",
            "target-free atemporal selection law",
            "structural stability criterion and parameter domain",
        ),
        "must_derive": (
            "complete selected quotient classification",
            "canonical state-generated coexisting roles",
            "intrinsic role invariant",
            "nonexchangeability after full quotient",
            "law relevance rather than arbitrary decomposition",
            "open-domain structural stability",
            "no representative orientation or role selection",
            "noncircular law and foundation admissibility",
        ),
    }
}

EFFECTIVE_ROUTE_TAXONOMY = {
    **copy.deepcopy(BASE_ROUTE_TAXONOMY),
    **copy.deepcopy(ROUTE_TAXONOMY_OVERLAY),
}

CANDIDATE_CLASSIFICATION = {
    "candidate_claim_id": W2_06_CANDIDATE_ID,
    "historical_label": "atemporal_nonunique_solution_structure",
    "historical_label_status": "presence only; its multiple-solution contract is not satisfied",
    "effective_class": NEW_ROUTE_CLASS,
    "witness_kind": "INTRA_CLASS_CANONICAL_ROLES",
    "stability_kind": "ATEMPORAL_VARIATIONAL_STRUCTURAL",
    "promotion_status": "not evaluated by this contract",
}

FORBIDDEN_PROMOTION_SHORTCUTS = {
    "candidate_specific_definition": "N=3, 1+2, Q, rank, projector, or argmin cannot define F1",
    "future_geometry_laundering": (
        "internal N=3/O(3)/delta cannot be called space/rotation/metric, and internal 1+2 "
        "cannot be read as spacetime 3+1"
    ),
    "mere_decomposition": "a fixed basis or arbitrary projector split cannot close F1",
    "gauge_multiplicity": "relabelled representatives are not physically different",
    "argmin_self_justification": "an argmin does not derive the law that defines it",
    "structural_to_temporal": "a positive Hessian is not temporal formation or persistence",
    "F2_plus_borrowing": "nodes, relations, time, modes, geometry, and GR cannot close F1",
    "partial_AND_or_score": "no score or compensation replaces a failed gate",
    "fallback_rejection": "a promotion choice cannot reject a nonfalsified route",
    "tuned_or_posthoc_rule": "a tuned point, target-distance functional, or post-result term is forbidden",
    "route_class_laundering": "registry presence or a local rename is not route-contract satisfaction",
}

DEFERRED_OUTPUTS = (
    "operational node, trace, and relation",
    "internal causal order or clock",
    "independent additive modes",
    "physical continuum, Lorentzian metric, and light cone",
    "effective action and degrees-of-freedom health",
    "energy, pressure, mass, particle, or oscillon",
    "observable/data map and Einstein/PN bridge",
)


def run_gate() -> dict[str, Any]:
    # This verifies only internal consistency of the scientific definition.
    route_neutral = all(
        token not in F1_DEFINITION["route_neutral_core"]
        for token in ("N=3", "1+2", "projector", "Q", "rank")
    )
    expected_gate_keys = {
        "f1_definition_frozen_route_neutral", "witness_kind_frozen_before_evaluation",
        "complete_one_foundation_primitive_freedom_registry", "forbidden_target_intersection_empty",
        "undifferentiated_reference_trivial", "target_free_law_certified",
        "complete_output_classification", "intrinsic_differentiation_certified",
        "inequivalence_survives_full_quotient", "law_relevance_not_arbitrary_decomposition",
        "realization_or_selection_noncircular", "open_domain_stability_and_robustness",
        "foundation_admissibility_and_import_health", "router_extension_aligned",
        "independent_crosscheck_and_controls", "candidate_falsifier_absent",
        "f1_only_scope_honest",
    }
    gates_complete = set(PROMOTION_AND_GATES) == expected_gate_keys
    expected_base_classes = {
        "symmetric_instability_or_bifurcation", "atemporal_nonunique_solution_structure",
        "stochastic_or_quantum_outcome", "state_space_generating_rule",
        "nontrivial_relational_state_space", "other_explicit_target_free_mechanism",
    }
    base_taxonomy_complete = all((
        set(BASE_ROUTE_TAXONOMY) == expected_base_classes,
        all(
            set(contract) == {"imports_to_declare", "must_derive"}
            and bool(contract["imports_to_declare"])
            and bool(contract["must_derive"])
            for contract in BASE_ROUTE_TAXONOMY.values()
        ),
    ))
    taxonomy_aligned = (
        NEW_ROUTE_CLASS in EFFECTIVE_ROUTE_TAXONOMY
        and set(ROUTE_TAXONOMY_OVERLAY[NEW_ROUTE_CLASS])
        == {"imports_to_declare", "must_derive"}
    )
    law_policy_honest = all((
        "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED"
        in PRIMITIVE_LAW_POLICY["allowed_origin_statuses"],
        "IMPORTED_NOT_DERIVED" in PRIMITIVE_LAW_POLICY["status_ceiling"],
        "target orbit" in PRIMITIVE_LAW_POLICY["argmin_guard"],
    ))
    expected_shortcuts = {
        "candidate_specific_definition", "future_geometry_laundering",
        "mere_decomposition", "gauge_multiplicity", "argmin_self_justification",
        "structural_to_temporal", "F2_plus_borrowing", "partial_AND_or_score",
        "fallback_rejection", "tuned_or_posthoc_rule", "route_class_laundering",
    }
    shortcuts_explicit = set(FORBIDDEN_PROMOTION_SHORTCUTS) == expected_shortcuts
    contract_valid = all((
        route_neutral, gates_complete, base_taxonomy_complete, taxonomy_aligned,
        law_policy_honest, shortcuts_explicit,
    ))
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "ROUTER_VERSION": ROUTER_VERSION,
        "STATUS": (
            "F1_PROMOTION_CONTRACT_AND_ROUTE_TAXONOMY_DEFINED__CANDIDATE_NOT_EVALUATED"
            if contract_valid else "F1_PROMOTION_CONTRACT_INVALID__PHYSICAL_F1_OPEN"
        ),
        "CHECKS": {
            "route_neutral_definition": route_neutral,
            "all_promotion_gates_present": gates_complete,
            "base_route_taxonomy_complete": base_taxonomy_complete,
            "overlay_route_class_aligned": taxonomy_aligned,
            "primitive_law_status_honest": law_policy_honest,
            "promotion_shortcuts_explicit": shortcuts_explicit,
        },
        "F1_DEFINITION": F1_DEFINITION,
        "F1_ROLE_SEMANTICS": F1_ROLE_SEMANTICS,
        "WITNESS_KINDS": WITNESS_KINDS,
        "PROMOTION_AND_GATES": PROMOTION_AND_GATES,
        "PRIMITIVE_LAW_POLICY": PRIMITIVE_LAW_POLICY,
        "EFFECTIVE_ROUTE_TAXONOMY": EFFECTIVE_ROUTE_TAXONOMY,
        "CANDIDATE_CLASSIFICATION": CANDIDATE_CLASSIFICATION,
        "FORBIDDEN_PROMOTION_SHORTCUTS": FORBIDDEN_PROMOTION_SHORTCUTS,
        "DEFERRED_OUTPUTS": list(DEFERRED_OUTPUTS),
        "PROMOTION_AUTHORIZED": False,
        "CLOSURE_FLAGS": {
            "F1_PROMOTION_CONTRACT_FROZEN": contract_valid,
            "F1_ROUTE_TAXONOMY_V2_FROZEN": contract_valid,
            "W2_06_OVERLAY_CLASS_EVALUATED": False,
            "W2_06_PROMOTED_TO_W2_F1": False,
            "W2_F1_SELF_DIFFERENTIATION": False,
        },
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["STATUS"].startswith("F1_PROMOTION_CONTRACT_AND") else 1


if __name__ == "__main__":
    raise SystemExit(main())
