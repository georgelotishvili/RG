"""Fail-closed contract for the narrow W2-F2a internal-distinction subgate.

F2a is deliberately weaker than the frozen C0 W2_F2 gate.  It can qualify a
candidate for a separate audit of atemporal internal operational distinction;
it cannot close full F2, create a node or persistent imprint, or export time,
causality, modes, geometry, GR, observables, or data claims.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from typing import Any


MODEL_VERSION = "W2-F2A-INTERNAL-OPERATIONAL-DISTINCTION-CONTRACT-v1.2-internal"
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"
F1_MODEL_VERSION = "RefG-F1-ATEMPORAL-STRUCTURAL-PROOF-v1.0"
F1_STATUS = "CONDITIONAL_ATEMPORAL_STRUCTURAL_F1_RELATIVE_TO_IMPORTED_PRIMITIVES"
READY_STATUS = "W2_F2A_CONTRACT_READY_FOR_INDEPENDENT_REVIEW__FULL_F2_OPEN"
FROZEN_STATUS = "W2_F2A_CONTRACT_FROZEN__NO_CANDIDATE_EVALUATED__FULL_F2_OPEN"
INVALID_STATUS = "W2_F2A_CONTRACT_INVALID__FULL_F2_OPEN"

ROOT = Path(__file__).resolve().parents[2]
C0_PATH = Path(__file__).with_name("w2_00_foundation_to_einstein_contract.md")
F1_PATH = Path(__file__).with_name("w2_09a_f1_proof") / "refg_f1_atemporal_structural_proof.py"

# These literals are deliberately independent of the factories below.  They
# prevent a factory and its validator from drifting together unnoticed.
EXPECTED_PAYLOAD_SHA256 = "4F09319C5DE3569AFA7FC2AA8FEA2190438D2E15EECC4DFCA815D69999FD37E2"
EXPECTED_VALIDATOR_SHA256 = "8AAA08C517DC623CFEA2DB18223F9EC7670F1A01D085AFD2CDFB0E1851C31666"
EXPECTED_STANDARD_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})
EXPECTED_CUSTOM_FIELDS = frozenset({
    "F2A_DEFINITION", "WITNESS_ROUTES", "ROUTE_POLICY",
    "CANDIDATE_SCREENING_GATES", "FORBIDDEN_INPUTS", "SCOPE_CEILING",
    "GATE_APPLICABILITY", "EXPORT_STATUS", "INDEPENDENT_REVIEW",
    "NEXT_ATOMIC_TASK",
})
EXPECTED_DEFINITION_KEYS = frozenset({
    "subgate_boundary", "intrinsic_map", "operational_meaning",
    "generated_relata_and_comparisons", "irreducible_relation", "equivalence",
    "reference_and_domain", "scope",
})
EXPECTED_WITNESS_ROUTE_KEYS = frozenset({
    "INTRASTATE_UNIFORM_EFFECT_FAMILY", "PAIRWISE_RELATIONAL_INVARIANT",
    "ENDOGENOUS_ATEMPORAL_RESPONSE",
})
EXPECTED_ROUTE_POLICY = {
    "enumerated_routes_exhaustive": False,
    "unlisted_routes_allowed_if_all_gates_pass": True,
    "candidate_route_must_be_explicit": True,
    "contract_selects_preferred_route": False,
}
EXPECTED_SCREENING_GATE_KEYS = frozenset({
    "f1_dependency_valid", "candidate_domain_map_and_branches_explicit",
    "relata_generated_not_preloaded",
    "uniform_comparison_family_generated_not_preloaded",
    "outputs_share_one_comparison_codomain", "exact_nontrivial_separation_witness",
    "relation_not_reduced_to_preassigned_unary_or_bare_equality_data",
    "postselected_self_test_null_rejected",
    "quotient_covariance_and_reported_invariance",
    "undifferentiated_reference_null", "non_tuned_domain_and_regular_normalization",
    "extra_primitive_ledger_complete",
    "joint_admissibility_composition_and_common_action_derived",
    "full_f2_node_and_imprint_obligations_not_claimed",
    "operational_semantics_not_upgraded", "external_observable_and_data_map_absent",
    "f3_temporal_and_causal_imports_absent",
    "positive_null_and_adversarial_controls_pass",
    "candidate_specific_independent_audit_required",
})
EXPECTED_FREEDOM_KEYS = frozenset({
    "candidate_specific_parameters", "data_fitted_parameters",
    "new_physical_primitives", "candidate_witness_route",
})
EXPECTED_FREEDOM_ENTRY_KEYS = frozenset({
    "source", "allowed_range", "scale", "complexity",
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
    "full_W2_F2_operational_relations": False,
    "physical_node_or_location": False,
    "persistent_physical_imprint": False,
    "temporal_formation_or_persistence": False,
    "internal_order_or_causality": False,
    "independent_additive_modes": False,
    "physical_dimension_or_continuum": False,
    "Lorentzian_metric_or_light_cone": False,
    "effective_action_or_conservation_law": False,
    "RefG_environment_map": False,
    "mass_pressure_particle_or_oscillon": False,
    "GR_PN_or_PPN_bridge": False,
    "external_observable_or_data_map": False,
    "observational_validation": False,
}
EXPECTED_GATE_APPLICABILITY_KEYS = frozenset({
    "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
    "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
    "G7_OBSERVATION", "G8_EXPORT",
})
EXPECTED_EXPORT_STATUS = {
    "G8_EXPORT": False, "GITHUB": False, "ZENODO": False,
    "CANON": False, "ARTICLE": False,
}
EXPECTED_REVIEW_KEYS = frozenset({
    "semantic_contract_review", "fail_closed_code_review", "new_reader_scope_review",
})
EXPECTED_REVIEW_REQUIREMENTS = {
    "semantic_contract_review": "REQUIRED_ON_EXACT_DETACHED_PAYLOAD",
    "fail_closed_code_review": "REQUIRED_ON_EXACT_DETACHED_PAYLOAD",
    "new_reader_scope_review": "REQUIRED_ON_EXACT_DETACHED_PAYLOAD",
}
REVIEW_ATTESTED_PAYLOAD_IDS = {
    "semantic_contract_review": "4F09319C5DE3569AFA7FC2AA8FEA2190438D2E15EECC4DFCA815D69999FD37E2",
    "fail_closed_code_review": "4F09319C5DE3569AFA7FC2AA8FEA2190438D2E15EECC4DFCA815D69999FD37E2",
    "new_reader_scope_review": "4F09319C5DE3569AFA7FC2AA8FEA2190438D2E15EECC4DFCA815D69999FD37E2",
}
REVIEW_ATTESTED_VALIDATOR_IDS = {
    "semantic_contract_review": "8AAA08C517DC623CFEA2DB18223F9EC7670F1A01D085AFD2CDFB0E1851C31666",
    "fail_closed_code_review": "8AAA08C517DC623CFEA2DB18223F9EC7670F1A01D085AFD2CDFB0E1851C31666",
    "new_reader_scope_review": "8AAA08C517DC623CFEA2DB18223F9EC7670F1A01D085AFD2CDFB0E1851C31666",
}
EXPECTED_SCREENING_CONTROL_KEYS = frozenset({
    "all_true_only_eligible_never_promoted", "one_false_not_eligible",
    "every_missing_gate_invalid", "every_nonboolean_gate_invalid",
    "extra_gate_invalid", "invalid_audit_never_eligible", "nonboolean_audit_invalid",
})
EXPECTED_MUTATION_CONTROL_KEYS = frozenset({
    "every_missing_or_extra_field_rejected",
    "semantic_target_and_overclaim_mutants_rejected",
    "every_registry_missing_or_nonboolean_mutant_rejected",
    "closure_scope_export_policy_and_hidden_input_mutants_rejected",
})
EXPECTED_AUDIT_CHECK_KEYS = frozenset({
    "detached_payload_validator_identities_and_contract_types_exact",
    "dependency_versions_registries_and_full_c0_boundary_valid",
    "auxiliary_candidate_target_guard_clear",
    "freedom_gate_closure_scope_and_export_registries_complete",
    "candidate_screen_is_eligibility_only_and_fail_closed",
    "all_contract_mutation_families_rejected",
    "review_attestation_schema_fail_closed",
    "independent_reviews_complete",
    "next_task_is_single_orbit_no_go_only",
})


def standard_fields() -> frozenset[str]:
    return EXPECTED_STANDARD_FIELDS


def custom_fields() -> frozenset[str]:
    return EXPECTED_CUSTOM_FIELDS


def f2a_definition() -> dict[str, str]:
    return {
        "subgate_boundary": (
            "F2a tests only atemporal internal operational distinction.  Full C0 F2 remains "
            "open until its node, atemporal state-supported imprint/correlation carrier, relation, "
            "and invariant obligations are separately met; persistence belongs only to F3."
        ),
        "intrinsic_map": (
            "A candidate must derive one uniform internal comparison rule from its accepted "
            "state and declared law, with explicit domain, codomain, and undefined boundary."
        ),
        "operational_meaning": (
            "Here operational means only a law-defined internal comparison map.  It does not "
            "mean intervention, physical effect, response, or measurement unless those are "
            "separately derived."
        ),
        "generated_relata_and_comparisons": (
            "Both the compared relata and the admissible comparisons must be generated rather "
            "than inserted as names, a fixed split, a desired table, or post-selected self-tests."
        ),
        "irreducible_relation": (
            "The reported relation must not be mere preassigned unary name, type, rank, "
            "cardinality, or bare equality data.  A uniformly law-derived effect family may "
            "produce a delta response table, but the table alone is not a derivation.  The "
            "relation must be nonconstant on the complete declared quotient or genuinely "
            "pairwise with derived joint admissibility and common action."
        ),
        "equivalence": (
            "Representatives may transform covariantly, but the reported comparison must survive "
            "the complete declared equivalence."
        ),
        "reference_and_domain": (
            "The undifferentiated reference must remain null, and success must hold on a declared "
            "non-tuned domain rather than at one singular or post-selected point."
        ),
        "scope": (
            "F2a is not a physical node, persistent record, temporal process, causal influence, "
            "mode, geometry, action, GR bridge, external observable, or observational result."
        ),
    }


def witness_routes() -> dict[str, str]:
    return {
        "INTRASTATE_UNIFORM_EFFECT_FAMILY": (
            "A uniformly generated comparison family separates internal relata without using "
            "each relatum as its own post-selected test."
        ),
        "PAIRWISE_RELATIONAL_INVARIANT": (
            "A jointly admissible state family has an irreducibly pairwise invariant under its "
            "derived complete common action; independent relabellings remain a required null."
        ),
        "ENDOGENOUS_ATEMPORAL_RESPONSE": (
            "The law derives an atemporal internal response carrier; persistence and directed "
            "influence remain excluded."
        ),
    }


def route_policy() -> dict[str, bool]:
    return dict(EXPECTED_ROUTE_POLICY)


def candidate_screening_gates() -> dict[str, str]:
    return {
        "f1_dependency_valid": "The declared F1 predecessor is valid and promoted.",
        "candidate_domain_map_and_branches_explicit": (
            "The full domain, codomain, map, branches, and undefined points are explicit."
        ),
        "relata_generated_not_preloaded": "Compared relata are generated by state and law.",
        "uniform_comparison_family_generated_not_preloaded": (
            "One uniform comparison family is derived before individual outcomes are read."
        ),
        "outputs_share_one_comparison_codomain": "All outputs obey one comparison rule.",
        "exact_nontrivial_separation_witness": "At least two outputs are exactly separated.",
        "relation_not_reduced_to_preassigned_unary_or_bare_equality_data": (
            "The relation is not inserted as names, types, ranks, counts, or bare equality.  A "
            "delta response is admissible only when its uniform effect family is independently "
            "derived from the law."
        ),
        "postselected_self_test_null_rejected": (
            "A relatum tested only by its own derived selector is rejected as tautological."
        ),
        "quotient_covariance_and_reported_invariance": (
            "Representative covariance and reported-output invariance are exact."
        ),
        "undifferentiated_reference_null": "No singular division creates false multiplicity.",
        "non_tuned_domain_and_regular_normalization": (
            "The witness persists on a declared nonzero domain with regular normalization."
        ),
        "extra_primitive_ledger_complete": (
            "Every extra primitive and architectural freedom is explicit for later status labelling."
        ),
        "joint_admissibility_composition_and_common_action_derived": (
            "Any multi-state route derives its multiplicity, composition rule, and common action; "
            "independent-equivalence controls erase spurious relations."
        ),
        "full_f2_node_and_imprint_obligations_not_claimed": (
            "This subgate does not claim the full C0 node or imprint obligations."
        ),
        "operational_semantics_not_upgraded": (
            "A comparison map is not relabelled as intervention, physical response, or measurement."
        ),
        "external_observable_and_data_map_absent": "No apparatus, observable, or data map is used.",
        "f3_temporal_and_causal_imports_absent": (
            "No iteration history, update order, lag, memory, retarded kernel, hysteresis, "
            "directed influence, time, or causality is imported."
        ),
        "positive_null_and_adversarial_controls_pass": (
            "Positive, reference-null, relabel, target, equality-table, and leakage controls pass."
        ),
        "candidate_specific_independent_audit_required": (
            "A separate module must derive the facts and perform an independent audit."
        ),
    }


def freedom_ledger() -> dict[str, dict[str, Any]]:
    return {
        "candidate_specific_parameters": {
            "source": "none at contract level", "allowed_range": 0,
            "scale": "contract", "complexity": 0,
        },
        "data_fitted_parameters": {
            "source": "N/A — no data", "allowed_range": 0,
            "scale": "data", "complexity": 0,
        },
        "new_physical_primitives": {
            "source": "none at contract level; candidate additions require a new ledger",
            "allowed_range": 0, "scale": "foundation", "complexity": 0,
        },
        "candidate_witness_route": {
            "source": "chosen and declared by each later candidate",
            "allowed_range": "any explicit route satisfying every gate; listed routes non-exhaustive",
            "scale": "one categorical architectural choice per candidate",
            "complexity": "one declared categorical choice, not a fitted parameter",
        },
    }


def closure_flags() -> dict[str, bool]:
    return dict(EXPECTED_C0_CLOSURE_FLAGS)


def scope_ceiling() -> dict[str, bool]:
    return dict(EXPECTED_SCOPE_CEILING)


def gate_applicability() -> dict[str, str]:
    return {
        "G0_GOAL": "REQUIRED — narrow F2a claim and full-F2 ceiling fixed before candidates",
        "G1_CONVENTIONS": "REQUIRED — internal map and equivalence meanings fixed",
        "G2_CORE_ALGEBRA": "REQUIRED — exact screening schema and decision logic",
        "G3_STRUCTURE": "REQUIRED — route-neutral relation and non-tautology conditions",
        "G4_INDEPENDENT_CHECK": "REQUIRED — external semantic, code, and new-reader audits",
        "G5_LIMITS_REGRESSION": "REQUIRED — reference, tuned, relabel, equality, and leakage nulls",
        "G6_PHYSICAL_MATCH": "N/A — no source, charge, energy, node, or observable claim",
        "G7_OBSERVATION": "N/A — no observable, forward model, or data",
        "G8_EXPORT": "N/A — internal contract; not for Canon, article, GitHub, or Zenodo",
    }


def forbidden_inputs() -> tuple[str, ...]:
    return (
        "preassigned node, location, physical imprint, or persistent record",
        "preferred labels, fixed split, desired response table, or target relation",
        "post-selected self-selector or equality table presented as new operational content",
        "unregistered multiplicity, composition rule, pair state, or common equivalence",
        "external apparatus, observable, fitted datum, or benchmark answer",
        "iteration history, update order, lag, memory, retarded kernel, or hysteresis",
        "directed influence, time, causal arrow, adjacency, distance, or continuum",
        "physical mode, metric, connection, action, GR equation, or observed geometry",
    )


def independent_review_requirements() -> dict[str, str]:
    return dict(EXPECTED_REVIEW_REQUIREMENTS)


def review_attestations() -> dict[str, dict[str, Any]]:
    """Detached review metadata; changing a verdict cannot alter the payload."""
    return {
        "semantic_contract_review": {
            "passed": True,
            "reviewer": "/root/f2_independent_review",
            "artifact": "independent semantic verdict for this detached payload",
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS[
                "semantic_contract_review"
            ],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS[
                "semantic_contract_review"
            ],
        },
        "fail_closed_code_review": {
            "passed": True,
            "reviewer": "/root/w209_no_go",
            "artifact": "independent fail-closed code verdict for this detached payload",
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS[
                "fail_closed_code_review"
            ],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS[
                "fail_closed_code_review"
            ],
        },
        "new_reader_scope_review": {
            "passed": True,
            "reviewer": "/root/f2_independent_review",
            "artifact": "independent new-reader scope verdict for this detached payload",
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS[
                "new_reader_scope_review"
            ],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS[
                "new_reader_scope_review"
            ],
        },
    }


def build_contract() -> dict[str, Any]:
    next_task = (
        "Create w2_11_f2_single_orbit_readout_no_go_gate.py: distinguish invariant "
        "whole-state outputs from covariant representative outputs, prove constancy on one "
        "accepted quotient orbit, and preserve the valid F1 intrastate roles without calling "
        "them F2 relations."
    )
    return {
        "CLAIM_ID": "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_CONTRACT_001",
        "CLAIM": (
            "Freeze a candidate-neutral subgate for atemporal internal operational distinction; "
            "do not evaluate a candidate and do not weaken or close full C0 W2_F2."
        ),
        "TYPE": "DEFINITIONAL_SUBGATE_CONTRACT_WITH_FAIL_CLOSED_SCREENING",
        "MODEL_VERSION": MODEL_VERSION,
        "ASSUMPTIONS": (
            "The audited conditional F1 result is the sole scientific predecessor.",
            "F1 imports remain imported and F1 provides no automatic F2 content.",
            "The full frozen C0 F2 node, atemporal imprint/correlation carrier, relation, and "
            "invariant threshold is unchanged; imprint persistence remains an F3 question.",
        ),
        "DOMAIN": (
            "Atemporal internal distinction candidates descending from valid F1; full F2, nodes, "
            "persistent imprints, histories, spacetime, dynamics, GR, observables, and data excluded."
        ),
        "CONVENTIONS": (
            "Only complete-equivalence-invariant reported comparisons count.  Representative "
            "covariance is not an invariant result; computational order is not physical time."
        ),
        "FREEDOM_LEDGER": freedom_ledger(),
        "DEPENDENCIES": {
            "programme_contract": PROGRAM_CONTRACT,
            "public_f1_model_version": F1_MODEL_VERSION,
            "public_f1_required_status": F1_STATUS,
            "f1_does_not_preclose_f2": True,
        },
        "METHOD": (
            "Freeze exact F2a semantics and a screening schema before candidates; the screen can "
            "only declare eligibility for a separate candidate-specific proof and audit."
        ),
        "PASS_CONDITION": (
            "Exact detached payload identity, C0/F1 versioned boundary, complete independent "
            "registries, auxiliary target guard, all mutation controls, and all reviews pass."
        ),
        "FAIL_CONDITION": (
            "Any drift, target preload, hidden freedom, tautological self-test, missing full-F2 "
            "ceiling, temporal/causal leak, malformed schema, or incomplete independent review."
        ),
        "FALSIFIER": (
            "A modified semantic or registry field validates, a self-asserted gate map promotes a "
            "candidate, or this subgate can set full W2_F2 true."
        ),
        "RESIDUAL": "0 for exact contract/schema checks; no candidate equation is evaluated.",
        "ERROR_BOUND": "0 for exact discrete checks; numerical and data errors are N/A.",
        "VALIDITY_HEALTH": (
            "Valid only as an internal F2a contract.  Any candidate needs a non-tuned domain, "
            "regular normalization, explicit extra-primitive ledger, and separate audit."
        ),
        "BRANCHES": {
            "intrastate_uniform": "OPEN_UNEVALUATED",
            "pairwise_relational": "OPEN_UNEVALUATED",
            "endogenous_response": "OPEN_UNEVALUATED",
            "unlisted_exact_route": "OPEN_IF_ALL_GATES_PASS",
        },
        "OBSERVABLE_MAP": {"status": "N/A", "reason": "internal F2a map only"},
        "FORWARD_MODEL": {"status": "N/A", "reason": "no observable or data chain"},
        "DATA_ROLE": {"status": "N/A", "reason": "no data used"},
        "IDENTIFIABILITY": (
            "A later candidate must prove exact separation on the complete declared quotient; "
            "preassigned unary labels, types, ranks, counts, bare equality, post-selected self-tests, "
            "and independent per-state equivalences are null controls.  A delta response is not "
            "excluded when a uniform effect family is itself derived from the accepted law."
        ),
        "BENCHMARK": (
            "Undifferentiated reference, tuned point, relabel-only classifier, self/equality table, "
            "preloaded target, hidden pair structure, independent per-state relabelling, and temporal "
            "leakage are fixed nulls."
        ),
        "CLOSURE_FLAGS": closure_flags(),
        "CROSSCHECK": (
            "This module supplies mutation tests only; independent semantic, fail-closed, and "
            "new-reader audits are recorded separately and are mandatory for freeze."
        ),
        "PROVENANCE": {
            "date": "2026-07-21", "contract_version": MODEL_VERSION,
            "c0_version": PROGRAM_CONTRACT, "f1_version": F1_MODEL_VERSION,
            "reviewed_payload_sha256": EXPECTED_PAYLOAD_SHA256,
            "payload_identity_rule": (
                "SHA-256 of the complete contract after replacing only this digest field with "
                "the fixed <DETACHED_PAYLOAD_ID> sentinel"
            ),
            "validator_identity_rule": (
                "A separate normalized-source SHA-256 binds the validator and control logic; "
                "only detached identity literals and review verdict booleans are normalized"
            ),
            "review_artifacts": "detached review_attestations registry in this output module",
            "model_change_boundary": (
                "any semantic payload change requires a new model version, payload identity, "
                "and fresh reviews"
            ),
            "output_artifact": (
                "RefG/work 2/w2_10_f2a_internal_operational_distinction_contract.py"
            ),
        },
        "FILES": (
            "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
            "RefG/work 2/w2_09a_f1_proof/refg_f1_atemporal_structural_proof.py",
            "RefG/work 2/w2_10_f2a_internal_operational_distinction_contract.py",
        ),
        "F2A_DEFINITION": f2a_definition(),
        "WITNESS_ROUTES": witness_routes(),
        "ROUTE_POLICY": route_policy(),
        "CANDIDATE_SCREENING_GATES": candidate_screening_gates(),
        "FORBIDDEN_INPUTS": forbidden_inputs(),
        "SCOPE_CEILING": scope_ceiling(),
        "GATE_APPLICABILITY": gate_applicability(),
        "EXPORT_STATUS": dict(EXPECTED_EXPORT_STATUS),
        "INDEPENDENT_REVIEW": independent_review_requirements(),
        "NEXT_ATOMIC_TASK": next_task,
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
    return (
        isinstance(actual, dict)
        and set(actual) == set(expected)
        and all(type(actual[key]) is bool for key in expected)
        and all(actual[key] is expected[key] for key in expected)
    )


def exact_true_control_map(actual: Any, expected_keys: frozenset[str]) -> bool:
    return (
        isinstance(actual, dict)
        and set(actual) == set(expected_keys)
        and all(type(actual[key]) is bool and actual[key] is True for key in expected_keys)
    )


def detached_payload_sha256(contract: Any) -> str:
    if not isinstance(contract, dict) or not isinstance(contract.get("PROVENANCE"), dict):
        return ""
    if "reviewed_payload_sha256" not in contract["PROVENANCE"]:
        return ""
    payload = copy.deepcopy(contract)
    payload["PROVENANCE"]["reviewed_payload_sha256"] = "<DETACHED_PAYLOAD_ID>"
    try:
        canonical = json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError):
        return ""
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()


def detached_validator_sha256() -> str:
    """Bind validator source while excluding only detached identity/attestation slots."""
    try:
        source = Path(__file__).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""
    source, expected_count = re.subn(
        r'^EXPECTED_VALIDATOR_SHA256 = "[^"]*"$',
        'EXPECTED_VALIDATOR_SHA256 = "<DETACHED_VALIDATOR_ID>"',
        source,
        count=1,
        flags=re.MULTILINE,
    )
    mapping_pattern = re.compile(
        r'^REVIEW_ATTESTED_VALIDATOR_IDS = \{.*?^\}\r?\n',
        flags=re.MULTILINE | re.DOTALL,
    )
    mapping_match = mapping_pattern.search(source)
    if expected_count != 1 or mapping_match is None:
        return ""
    normalized_mapping = re.sub(
        r'"(?:[A-F0-9]{64}|PENDING)"',
        '"<ATTESTED_VALIDATOR_ID>"',
        mapping_match.group(0),
    )
    source = source[:mapping_match.start()] + normalized_mapping + source[mapping_match.end():]
    source, verdict_count = re.subn(
        r'("passed":\s*)(?:True|False)',
        r'\1<DETACHED_REVIEW_VERDICT>',
        source,
    )
    if verdict_count != len(EXPECTED_REVIEW_KEYS):
        return ""
    return hashlib.sha256(source.encode("utf-8")).hexdigest().upper()


def registry_shapes_valid(contract: dict[str, Any]) -> bool:
    freedom = contract.get("FREEDOM_LEDGER")
    return all((
        set(contract.get("F2A_DEFINITION", {})) == EXPECTED_DEFINITION_KEYS,
        set(contract.get("WITNESS_ROUTES", {})) == EXPECTED_WITNESS_ROUTE_KEYS,
        exact_bool_map(contract.get("ROUTE_POLICY"), EXPECTED_ROUTE_POLICY),
        set(contract.get("CANDIDATE_SCREENING_GATES", {})) == EXPECTED_SCREENING_GATE_KEYS,
        isinstance(freedom, dict) and set(freedom) == EXPECTED_FREEDOM_KEYS,
        isinstance(freedom, dict) and all(
            isinstance(entry, dict) and set(entry) == EXPECTED_FREEDOM_ENTRY_KEYS
            for entry in freedom.values()
        ),
        exact_bool_map(contract.get("CLOSURE_FLAGS"), EXPECTED_C0_CLOSURE_FLAGS),
        exact_bool_map(contract.get("SCOPE_CEILING"), EXPECTED_SCOPE_CEILING),
        set(contract.get("GATE_APPLICABILITY", {})) == EXPECTED_GATE_APPLICABILITY_KEYS,
        exact_bool_map(contract.get("EXPORT_STATUS"), EXPECTED_EXPORT_STATUS),
        exact_tree_equal(contract.get("INDEPENDENT_REVIEW"), EXPECTED_REVIEW_REQUIREMENTS),
        isinstance(contract.get("FORBIDDEN_INPUTS"), tuple),
    ))


def review_attestation_schema_valid(attestations: Any, require_pass: bool) -> bool:
    expected_fields = {
        "passed", "reviewer", "artifact", "reviewed_payload_sha256",
        "reviewed_validator_sha256",
    }
    if not isinstance(attestations, dict) or set(attestations) != EXPECTED_REVIEW_KEYS:
        return False
    for entry in attestations.values():
        if not isinstance(entry, dict) or set(entry) != expected_fields:
            return False
        if type(entry["passed"]) is not bool:
            return False
        if require_pass and entry["passed"] is not True:
            return False
        if not isinstance(entry["reviewer"], str) or not entry["reviewer"]:
            return False
        if not isinstance(entry["artifact"], str) or not entry["artifact"]:
            return False
        if entry["reviewed_payload_sha256"] != EXPECTED_PAYLOAD_SHA256:
            return False
        if entry["reviewed_validator_sha256"] != EXPECTED_VALIDATOR_SHA256:
            return False
    return True


def review_attestation_schema_controls() -> bool:
    base = review_attestations()
    if not review_attestation_schema_valid(base, require_pass=False):
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
    wrong_validator["fail_closed_code_review"]["reviewed_validator_sha256"] = "WRONG"
    mutants.append(wrong_validator)
    return (
        review_attestation_schema_valid(base, require_pass=False)
        and all(
            not review_attestation_schema_valid(mutant, require_pass=False)
            for mutant in mutants
        )
    )


def semantic_guard(contract: dict[str, Any]) -> bool:
    fields = (
        contract["CLAIM"], *contract["ASSUMPTIONS"], contract["DOMAIN"],
        contract["CONVENTIONS"], contract["METHOD"], contract["PASS_CONDITION"],
        contract["IDENTIFIABILITY"], contract["BENCHMARK"], contract["CROSSCHECK"],
        *contract["F2A_DEFINITION"].values(), *contract["WITNESS_ROUTES"].values(),
        *contract["CANDIDATE_SCREENING_GATES"].values(),
    )
    corpus = "\n".join(fields).lower()
    candidate_tokens = (
        "sym_0", "sym0", "o(3)", "p₁", "p₂", "p1", "p2", "rank-1",
        "rank 1", "rank-2", "rank 2", "projector", "eigenspace", "spectral",
        "quartic", "alpha", "3x3", "desired response table",
    )
    return not any(token in corpus for token in candidate_tokens)


def strict_contract_valid(contract: Any) -> bool:
    if not isinstance(contract, dict):
        return False
    if set(contract) != EXPECTED_STANDARD_FIELDS | EXPECTED_CUSTOM_FIELDS:
        return False
    if not exact_tree_equal(contract, build_contract()):
        return False
    if contract["MODEL_VERSION"] != MODEL_VERSION:
        return False
    if contract["PROVENANCE"].get("reviewed_payload_sha256") != EXPECTED_PAYLOAD_SHA256:
        return False
    if detached_payload_sha256(contract) != EXPECTED_PAYLOAD_SHA256:
        return False
    if not semantic_guard(contract):
        return False
    if not registry_shapes_valid(contract):
        return False
    return True


def load_f1() -> tuple[Any, dict[str, Any]]:
    spec = importlib.util.spec_from_file_location("refg_f1_for_f2a", F1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load F1 proof: {F1_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.run_proof()


def dependency_versions_and_boundaries_valid() -> bool:
    if not C0_PATH.is_file() or not F1_PATH.is_file():
        return False
    if C0_PATH.relative_to(ROOT).as_posix() != CLAIM_CONTRACT["FILES"][0]:
        return False
    if F1_PATH.relative_to(ROOT).as_posix() != CLAIM_CONTRACT["FILES"][1]:
        return False
    c0 = C0_PATH.read_text(encoding="utf-8")
    module, report = load_f1()
    expected_imports = {
        "single_internal_carrier_Q", "Sym0_3_R_internal_state_space",
        "positive_internal_contraction_and_transpose",
        "matrix_product_and_algebraic_trace",
        "O3_conjugation_as_complete_declared_equivalence", "Q_sign_not_gauge",
        "quartic_functional_form_signs_and_truncation",
        "open_parameter_domain_alpha_b_c_positive", "atemporal_global_argmin_rule",
    }
    expected_scope = {
        "foundation_law_derived", "functional_uniqueness_derived",
        "N3_physical_origin_derived", "temporal_formation_or_persistence",
        "physical_node_or_location", "operational_relations", "causal_order_or_clock",
        "independent_additive_physical_modes", "physical_dimension_or_continuum",
        "Lorentzian_metric_or_light_cone", "effective_action_or_conservation_law",
        "RefG_resonant_environment_map", "mass_pressure_particle_or_oscillon",
        "GR_PN_or_PPN_bridge", "observable_or_data_map",
    }
    return all((
        f"**კონტრაქტის ვერსია:** `{PROGRAM_CONTRACT}`" in c0,
        "### `W2_F2_OPERATIONAL_RELATIONS`" in c0,
        "კვანძი, კვალი, ურთიერთფარდობა და გარჩევადობის ინვარიანტი შედეგი უნდა იყოს"
        in c0,
        "შინაგანი ოპერაციული რუკა და იარლიყისგან დამოუკიდებელი გარჩევადობა" in c0,
        module.MODEL_VERSION == F1_MODEL_VERSION,
        report.get("MODEL_VERSION") == F1_MODEL_VERSION,
        report.get("STATUS") == module.PASS_STATUS == F1_STATUS,
        report.get("AUDIT_VALID") is True,
        report.get("PROMOTED") is True,
        set(report.get("IMPORTED_PRIMITIVES", {})) == expected_imports,
        set(report.get("IMPORTED_PRIMITIVES", {}).values()) == {"IMPORTED_NOT_DERIVED"},
        set(report.get("SCOPE_CEILING", {})) == expected_scope,
        all(value is False for value in report.get("SCOPE_CEILING", {}).values()),
    ))


def screening_gate_keys() -> frozenset[str]:
    return EXPECTED_SCREENING_GATE_KEYS


def screen_candidate(gates: Any, candidate_audit_valid: Any) -> dict[str, Any]:
    schema = (
        isinstance(gates, dict)
        and set(gates) == EXPECTED_SCREENING_GATE_KEYS
        and all(type(value) is bool for value in gates.values())
    )
    audit_type = type(candidate_audit_valid) is bool
    valid = bool(schema and audit_type and candidate_audit_valid)
    eligible = bool(valid and all(value is True for value in gates.values()))
    status = (
        "ELIGIBLE_FOR_SEPARATE_CANDIDATE_SPECIFIC_AUDIT"
        if eligible else
        "SCREEN_COMPLETE_NOT_ELIGIBLE"
        if valid else
        "INVALID_SCREEN__NO_ELIGIBILITY"
    )
    return {"VALID": valid, "ELIGIBLE": eligible, "PROMOTED": False, "STATUS": status}


def screening_controls() -> dict[str, bool]:
    keys = screening_gate_keys()
    all_true = {key: True for key in keys}
    one_false = dict(all_true)
    one_false[next(iter(keys))] = False
    missing_every = all(
        screen_candidate({k: True for k in keys if k != omitted}, True)["VALID"] is False
        for omitted in keys
    )
    nonboolean_every = all(
        screen_candidate({k: (1 if k == changed else True) for k in keys}, True)["VALID"] is False
        for changed in keys
    )
    extra = dict(all_true)
    extra["unregistered"] = True
    return {
        "all_true_only_eligible_never_promoted": (
            screen_candidate(all_true, True) == {
                "VALID": True, "ELIGIBLE": True, "PROMOTED": False,
                "STATUS": "ELIGIBLE_FOR_SEPARATE_CANDIDATE_SPECIFIC_AUDIT",
            }
        ),
        "one_false_not_eligible": screen_candidate(one_false, True)["ELIGIBLE"] is False,
        "every_missing_gate_invalid": missing_every,
        "every_nonboolean_gate_invalid": nonboolean_every,
        "extra_gate_invalid": screen_candidate(extra, True)["VALID"] is False,
        "invalid_audit_never_eligible": screen_candidate(all_true, False)["ELIGIBLE"] is False,
        "nonboolean_audit_invalid": screen_candidate(all_true, 1)["VALID"] is False,
    }


def mutation_controls() -> dict[str, bool]:
    base = build_contract()

    field_mutants = []
    for field in standard_fields() | custom_fields():
        mutant = copy.deepcopy(base)
        mutant.pop(field)
        field_mutants.append(mutant)
    extra = copy.deepcopy(base)
    extra["UNREGISTERED"] = True
    field_mutants.append(extra)

    semantic_mutants = []
    for field, injected in (
        ("CLAIM", " This proves physical time, causality, and GR."),
        ("METHOD", " Force P1 and P2 as the desired answer."),
        ("IDENTIFIABILITY", " Names and cardinality alone suffice."),
        ("CROSSCHECK", " none"),
    ):
        mutant = copy.deepcopy(base)
        mutant[field] += injected
        semantic_mutants.append(mutant)
    assumption = copy.deepcopy(base)
    assumption["ASSUMPTIONS"] += ("Import a desired two-object relation table.",)
    semantic_mutants.append(assumption)
    route = copy.deepcopy(base)
    route["WITNESS_ROUTES"]["INTRASTATE_UNIFORM_EFFECT_FAMILY"] += (
        " Use a rank-1 target projector."
    )
    semantic_mutants.append(route)

    registry_mutants = []
    for registry in (
        "F2A_DEFINITION", "WITNESS_ROUTES", "ROUTE_POLICY",
        "CANDIDATE_SCREENING_GATES", "SCOPE_CEILING", "CLOSURE_FLAGS",
        "GATE_APPLICABILITY", "EXPORT_STATUS", "INDEPENDENT_REVIEW",
    ):
        for key in base[registry]:
            missing = copy.deepcopy(base)
            missing[registry].pop(key)
            registry_mutants.append(missing)
        extra_registry_key = copy.deepcopy(base)
        extra_registry_key[registry]["UNREGISTERED"] = False
        registry_mutants.append(extra_registry_key)
    for registry in ("ROUTE_POLICY", "SCOPE_CEILING", "CLOSURE_FLAGS", "EXPORT_STATUS"):
        for key in base[registry]:
            nonboolean = copy.deepcopy(base)
            nonboolean[registry][key] = 1
            registry_mutants.append(nonboolean)

    boundary_mutants = []
    for path, key, value in (
        ("CLOSURE_FLAGS", "W2_F2_OPERATIONAL_RELATIONS", True),
        ("SCOPE_CEILING", "full_W2_F2_operational_relations", True),
        ("EXPORT_STATUS", "GITHUB", True),
        ("ROUTE_POLICY", "contract_selects_preferred_route", True),
    ):
        mutant = copy.deepcopy(base)
        mutant[path][key] = value
        boundary_mutants.append(mutant)
    observable = copy.deepcopy(base)
    observable["OBSERVABLE_MAP"]["reason"] = "internal, nevertheless detector output"
    boundary_mutants.append(observable)
    hidden = copy.deepcopy(base)
    hidden["FREEDOM_LEDGER"]["new_physical_primitives"]["source"] = "one hidden primitive"
    boundary_mutants.append(hidden)

    return {
        "every_missing_or_extra_field_rejected": all(
            not strict_contract_valid(mutant) for mutant in field_mutants
        ),
        "semantic_target_and_overclaim_mutants_rejected": all(
            not strict_contract_valid(mutant) for mutant in semantic_mutants
        ),
        "every_registry_missing_or_nonboolean_mutant_rejected": all(
            not strict_contract_valid(mutant) for mutant in registry_mutants
        ),
        "closure_scope_export_policy_and_hidden_input_mutants_rejected": all(
            not strict_contract_valid(mutant) for mutant in boundary_mutants
        ),
    }


def audit_check_schema_controls() -> bool:
    base = {key: True for key in EXPECTED_AUDIT_CHECK_KEYS}
    missing = all(
        not exact_true_control_map(
            {key: True for key in EXPECTED_AUDIT_CHECK_KEYS if key != omitted},
            EXPECTED_AUDIT_CHECK_KEYS,
        )
        for omitted in EXPECTED_AUDIT_CHECK_KEYS
    )
    extra = dict(base)
    extra["fabricated"] = True
    nonboolean = dict(base)
    nonboolean[next(iter(EXPECTED_AUDIT_CHECK_KEYS))] = 1
    return all((
        exact_true_control_map(base, EXPECTED_AUDIT_CHECK_KEYS),
        missing,
        not exact_true_control_map(extra, EXPECTED_AUDIT_CHECK_KEYS),
        not exact_true_control_map(nonboolean, EXPECTED_AUDIT_CHECK_KEYS),
    ))


def _run_audit_unchecked() -> dict[str, Any]:
    if not strict_contract_valid(CLAIM_CONTRACT):
        raise ValueError("contract payload or schema invalid")
    if detached_validator_sha256() != EXPECTED_VALIDATOR_SHA256:
        raise ValueError("validator source identity invalid")

    screen_controls = screening_controls()
    mutants = mutation_controls()
    reviews = review_attestations()
    checks = {
        "detached_payload_validator_identities_and_contract_types_exact": all((
            strict_contract_valid(CLAIM_CONTRACT),
            detached_validator_sha256() == EXPECTED_VALIDATOR_SHA256,
        )),
        "dependency_versions_registries_and_full_c0_boundary_valid": (
            dependency_versions_and_boundaries_valid()
        ),
        "auxiliary_candidate_target_guard_clear": semantic_guard(CLAIM_CONTRACT),
        "freedom_gate_closure_scope_and_export_registries_complete": all((
            registry_shapes_valid(CLAIM_CONTRACT),
            exact_tree_equal(CLAIM_CONTRACT["FREEDOM_LEDGER"], freedom_ledger()),
            exact_tree_equal(CLAIM_CONTRACT["GATE_APPLICABILITY"], gate_applicability()),
        )),
        "candidate_screen_is_eligibility_only_and_fail_closed": exact_true_control_map(
            screen_controls, EXPECTED_SCREENING_CONTROL_KEYS
        ),
        "all_contract_mutation_families_rejected": exact_true_control_map(
            mutants, EXPECTED_MUTATION_CONTROL_KEYS
        ),
        "review_attestation_schema_fail_closed": all((
            review_attestation_schema_controls(),
            audit_check_schema_controls(),
        )),
        "independent_reviews_complete": review_attestation_schema_valid(
            reviews, require_pass=True
        ),
        "next_task_is_single_orbit_no_go_only": all((
            "single_orbit_readout_no_go" in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
            "GR" not in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
            "time" not in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"].lower(),
        )),
    }
    checks_schema_exact = (
        isinstance(checks, dict)
        and set(checks) == EXPECTED_AUDIT_CHECK_KEYS
        and all(type(checks[key]) is bool for key in EXPECTED_AUDIT_CHECK_KEYS)
    )
    structural_ready = bool(
        checks_schema_exact
        and all(
            checks[key] is True
            for key in EXPECTED_AUDIT_CHECK_KEYS
            if key != "independent_reviews_complete"
        )
    )
    frozen = structural_ready and checks["independent_reviews_complete"] is True
    status = FROZEN_STATUS if frozen else READY_STATUS if structural_ready else INVALID_STATUS
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "DETACHED_PAYLOAD_SHA256": detached_payload_sha256(CLAIM_CONTRACT),
        "DETACHED_VALIDATOR_SHA256": detached_validator_sha256(),
        "STATUS": status,
        "AUDIT_VALID": frozen,
        "STRUCTURAL_READY_FOR_REVIEW": structural_ready,
        "PROMOTED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F2A_CONTRACT_FROZEN": frozen,
            "W2_F2A_CANDIDATE_EVALUATED": False,
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": False,
        },
        "CLAIM_CEILING": (
            "F2A law-defined internal relational distinction only; not full F2 and not a "
            "physical operation, intervention, response, record, or measurement."
        ),
        "AUDIT_CHECKS": checks,
        "SCREENING_CONTROLS": screen_controls,
        "MUTATION_CONTROLS": mutants,
        "INDEPENDENT_REVIEW_ATTESTATIONS": reviews,
        "CLOSURE_FLAGS": CLAIM_CONTRACT["CLOSURE_FLAGS"],
        "SCOPE_CEILING": CLAIM_CONTRACT["SCOPE_CEILING"],
        "NEXT_ATOMIC_TASK": CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
    }


def fail_closed_invalid_report(error: Exception) -> dict[str, Any]:
    """Return a stable non-promoting report for every malformed audit state."""
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "DETACHED_PAYLOAD_SHA256": "",
        "DETACHED_VALIDATOR_SHA256": "",
        "STATUS": INVALID_STATUS,
        "AUDIT_VALID": False,
        "STRUCTURAL_READY_FOR_REVIEW": False,
        "PROMOTED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F2A_CONTRACT_FROZEN": False,
            "W2_F2A_CANDIDATE_EVALUATED": False,
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": False,
        },
        "CLAIM_CEILING": (
            "F2A invalid; no scientific, operational, physical, or observational claim exports."
        ),
        "AUDIT_CHECKS": {key: False for key in EXPECTED_AUDIT_CHECK_KEYS},
        "SCREENING_CONTROLS": {
            key: False for key in EXPECTED_SCREENING_CONTROL_KEYS
        },
        "MUTATION_CONTROLS": {
            key: False for key in EXPECTED_MUTATION_CONTROL_KEYS
        },
        "INDEPENDENT_REVIEW_ATTESTATIONS": {},
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "NEXT_ATOMIC_TASK": "UNAVAILABLE_UNTIL_CONTRACT_RESTORED",
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
        report["NEXT_ATOMIC_TASK"] = "UNAVAILABLE_UNTIL_CONTRACT_RESTORED"
        rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    return 0 if report["AUDIT_VALID"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
