"""Exact no-go for invariant whole-state readouts on one accepted F1 orbit.

The theorem rejects only a narrow route: a complete-equivalence-invariant
whole-state readout cannot distinguish representatives of one transitive
orbit.  Covariant F1 roles, law-derived internal effect families, derived
joint-state relations, and multiple-orbit routes remain open.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import sys
from typing import Any, Callable

import sympy as sp


MODEL_VERSION = "W2-F2-SINGLE-ORBIT-READOUT-NO-GO-v1.0-internal"
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"
F2A_MODEL_VERSION = "W2-F2A-INTERNAL-OPERATIONAL-DISTINCTION-CONTRACT-v1.2-internal"
F2A_FROZEN_STATUS = "W2_F2A_CONTRACT_FROZEN__NO_CANDIDATE_EVALUATED__FULL_F2_OPEN"
F2A_PAYLOAD_SHA256 = "4F09319C5DE3569AFA7FC2AA8FEA2190438D2E15EECC4DFCA815D69999FD37E2"
F2A_VALIDATOR_SHA256 = "8AAA08C517DC623CFEA2DB18223F9EC7670F1A01D085AFD2CDFB0E1851C31666"
F1_MODEL_VERSION = "RefG-F1-ATEMPORAL-STRUCTURAL-PROOF-v1.0"
F1_STATUS = "CONDITIONAL_ATEMPORAL_STRUCTURAL_F1_RELATIVE_TO_IMPORTED_PRIMITIVES"
C0_SHA256 = "3E0EFB2D635E7E5605F9D7EDFA99538644D7C21311989C478C4A6AF1854890EB"
F1_SOURCE_SHA256 = "8B29AF84AE0F94063CF0E7FDAB47A7CE364C7D6B1789D71051548A98A96C770E"
F2A_SOURCE_SHA256 = "44ADB77E4B78D5D36E7F597C8401FD91A9E0DD0F0D86E20541F1EB790EF8308D"
READY_STATUS = "W2_F2_SINGLE_ORBIT_NO_GO_READY_FOR_INDEPENDENT_REVIEW__F2A_OPEN"
PASS_STATUS = "CONDITIONAL_EXACT_SINGLE_ORBIT_WHOLE_STATE_READOUT_NO_GO__F2A_OPEN"
INVALID_STATUS = "W2_F2_SINGLE_ORBIT_NO_GO_INVALID__F2A_OPEN"
EXPECTED_PAYLOAD_SHA256 = "488F32736333427A1164963917B04A5962AB73ED5326BD8A90E24380AFD37EC6"
EXPECTED_VALIDATOR_SHA256 = "EC3514B0CCB1DE0425E3E18B447C408EC0D58F30798CE58DD37C12CAA167091D"

ROOT = Path(__file__).resolve().parents[2]
C0_PATH = Path(__file__).with_name("w2_00_foundation_to_einstein_contract.md")
F2A_PATH = Path(__file__).with_name(
    "w2_10_f2a_internal_operational_distinction_contract.py"
)
F1_PATH = Path(__file__).with_name("w2_09a_f1_proof") / "refg_f1_atemporal_structural_proof.py"

NEXT_ATOMIC_TASK = (
    "Create w2_12_f2_intrastate_uniform_effect_family_candidate_gate.py: test whether "
    "the accepted F1 state generates both relata and one uniform comparison/effect "
    "family with an invariant nontrivial response, without preloaded selectors or a "
    "bare equality table; keep full C0 F2 open."
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
    "THEOREM", "REJECTED_ROUTE", "PRESERVED_ROUTES", "SCOPE_CEILING",
    "FORBIDDEN_INPUTS", "GATE_APPLICABILITY", "EXPORT_STATUS", "INDEPENDENT_REVIEW",
    "NEXT_ATOMIC_TASK",
})
EXPECTED_THEOREM_KEYS = frozenset({
    "fixed_parameter_domain", "accepted_orbit", "invariant_readout",
    "covariant_output", "exact_statement", "proof", "f1_corollary",
    "claim_ceiling",
})
EXPECTED_REJECTED_ROUTE_KEYS = frozenset({
    "route", "class_definition", "rejection_reason", "status",
})
EXPECTED_PRESERVED_ROUTE_KEYS = frozenset({
    "intrastate_uniform_effect_family", "derived_joint_common_action",
    "multiple_accepted_orbits", "endogenous_atemporal_response",
})
EXPECTED_FREEDOM_KEYS = frozenset({
    "inherited_f1_parameters", "new_parameters", "data_fitted_parameters",
    "chosen_representative", "extra_physical_primitives",
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
    "F2a_internal_operational_distinction_proved": False,
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
EXPECTED_GATE_KEYS = frozenset({
    "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
    "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
    "G7_OBSERVATION", "G8_EXPORT",
})
EXPECTED_EXPORT_STATUS = {
    "G8_EXPORT": False, "GITHUB": False, "ZENODO": False,
    "CANON": False, "ARTICLE": False,
}
EXPECTED_REVIEW_KEYS = frozenset({
    "semantic_theorem_review", "fail_closed_code_review", "new_reader_scope_review",
})
EXPECTED_REVIEW_REQUIREMENTS = {
    "semantic_theorem_review": "REQUIRED_ON_EXACT_PAYLOAD_AND_VALIDATOR",
    "fail_closed_code_review": "REQUIRED_ON_EXACT_PAYLOAD_AND_VALIDATOR",
    "new_reader_scope_review": "REQUIRED_ON_EXACT_PAYLOAD_AND_VALIDATOR",
}
REVIEW_ATTESTED_PAYLOAD_IDS = {
    "semantic_theorem_review": "488F32736333427A1164963917B04A5962AB73ED5326BD8A90E24380AFD37EC6",
    "fail_closed_code_review": "488F32736333427A1164963917B04A5962AB73ED5326BD8A90E24380AFD37EC6",
    "new_reader_scope_review": "488F32736333427A1164963917B04A5962AB73ED5326BD8A90E24380AFD37EC6",
}
REVIEW_ATTESTED_VALIDATOR_IDS = {
    "semantic_theorem_review": "EC3514B0CCB1DE0425E3E18B447C408EC0D58F30798CE58DD37C12CAA167091D",
    "fail_closed_code_review": "EC3514B0CCB1DE0425E3E18B447C408EC0D58F30798CE58DD37C12CAA167091D",
    "new_reader_scope_review": "EC3514B0CCB1DE0425E3E18B447C408EC0D58F30798CE58DD37C12CAA167091D",
}
EXPECTED_FINITE_CHECK_KEYS = frozenset({
    "complete_group_and_transitive_orbit_exact",
    "invariant_whole_state_readouts_constant",
    "covariant_representative_varies_but_quotient_constant",
    "incomplete_equivalence_sampling_trap_rejected",
    "multiple_orbit_escape_preserved",
    "common_action_pair_invariant_and_independent_action_null",
    "constant_structured_output_not_entrywise_trivial",
})
EXPECTED_F1_CHECK_KEYS = frozenset({
    "symbolic_orbit_invariants_constant",
    "projectors_covariant_and_internal_roles_preserved",
    "representative_entries_vary_and_are_not_invariant_reports",
    "preferred_axis_is_not_a_single_valued_state_readout",
    "parameter_variation_is_not_same_fixed_parameter_orbit",
})
EXPECTED_MUTATION_KEYS = frozenset({
    "missing_or_extra_contract_fields_rejected",
    "registry_drift_rejected",
    "scope_closure_export_overclaims_rejected",
    "semantic_route_overclaims_rejected",
})
EXPECTED_AUDIT_KEYS = frozenset({
    "payload_validator_and_contract_schema_exact",
    "c0_f2a_and_f1_dependencies_exact",
    "general_theorem_and_route_boundary_exact",
    "finite_group_controls_exact",
    "f1_symbolic_specialization_exact",
    "f1_reference_and_role_regressions_preserved",
    "scope_closure_gate_and_export_boundaries_exact",
    "mutation_controls_exact",
    "review_attestation_schema_fail_closed",
    "review_attestations_complete",
    "next_task_is_intrastate_effect_candidate_only",
})


def theorem_registry() -> dict[str, str]:
    return {
        "fixed_parameter_domain": (
            "Fix one accepted model parameter point; parameter changes are not state motion."
        ),
        "accepted_orbit": (
            "For a group G acting on X, the accepted set A is exactly one transitive orbit "
            "G.x, so A/G contains one class."
        ),
        "invariant_readout": (
            "A whole-state report r:A->Z is invariant only if r(g.q)=r(q) for every "
            "declared equivalence g and every q in A."
        ),
        "covariant_output": (
            "A representative output F:A->Y may obey F(g.q)=rho(g).F(q); its representative "
            "can vary, while its quotient class pi_Y(F(q)) is invariant."
        ),
        "exact_statement": (
            "Every complete-equivalence-invariant whole-state report on one transitive orbit "
            "is constant, and every equivariant output has constant quotient class there."
        ),
        "proof": (
            "For q1=g1.x and q2=g2.x, let k=g2 g1^{-1}; then q2=k.q1 and invariance gives "
            "r(q2)=r(k.q1)=r(q1).  Equivariance puts F(q1),F(q2) in one rho(G)-orbit."
        ),
        "f1_corollary": (
            "On the fixed-parameter accepted F1 O(3)-orbit, invariant whole-state reports "
            "cannot select an orientation or distinguish accepted representatives."
        ),
        "claim_ceiling": (
            "Constancy does not erase covariant intrastate roles, does not make a constant "
            "structured table entrywise trivial, and does not reject derived relational routes."
        ),
    }


def rejected_route() -> dict[str, str]:
    return {
        "route": "ONE_ORBIT_INVARIANT_WHOLE_STATE_READOUT",
        "class_definition": (
            "one fixed-parameter transitive accepted orbit plus one single-state report that is "
            "invariant under the complete declared equivalence"
        ),
        "rejection_reason": "the report is exactly constant by transitivity and invariance",
        "status": "REJECTED_BY_EXACT_NO_GO_ONLY_IN_THIS_DECLARED_CLASS",
    }


def preserved_routes() -> dict[str, str]:
    return {
        "intrastate_uniform_effect_family": (
            "OPEN: generated relata plus an independently law-derived uniform comparison/effect "
            "family may have invariant internal structure, including a derived delta response."
        ),
        "derived_joint_common_action": (
            "OPEN: a derived joint domain and common diagonal action may support relational "
            "invariants; independent relabelling remains the null."
        ),
        "multiple_accepted_orbits": (
            "OPEN: an invariant report may distinguish different accepted quotient classes."
        ),
        "endogenous_atemporal_response": (
            "OPEN: an atemporal law-derived response carrier may be tested separately; "
            "persistence and directed influence remain behind F3."
        ),
    }


def freedom_ledger() -> dict[str, dict[str, Any]]:
    zero = {"source": "none", "allowed_range": 0, "scale": "theorem", "complexity": 0}
    return {
        "inherited_f1_parameters": {
            "source": "imported F1 open domain alpha,b,c>0; fixed during each orbit theorem",
            "allowed_range": "positive open domain, one fixed fibre at a time",
            "scale": "three inherited model parameters; not fitted here",
            "complexity": 3,
        },
        "new_parameters": dict(zero),
        "data_fitted_parameters": {**zero, "scale": "data"},
        "chosen_representative": {
            "source": "for algebraic crosscheck only; no representative is an output",
            "allowed_range": "any point on the same declared orbit",
            "scale": "description",
            "complexity": 0,
        },
        "extra_physical_primitives": {**zero, "scale": "foundation"},
    }


def forbidden_inputs() -> tuple[str, ...]:
    return (
        "preferred representative, fixed axis, ordered eigenbasis, target projector, or Q11 readout",
        "parameter variation, the origin, the rejected stationary branch, or minus-Q added to one orbit",
        "preloaded response/equality table, self-selector, external label, apparatus, or observable",
        "unregistered pair state, composition rule, common action, or restricted equivalence subgroup",
        "sampled rotations, random points, tolerance, floating-point constancy, or numerical promotion",
        "physical space, time, causality, mode, metric, action, GR, node, record, or measurement semantics",
    )


def gate_applicability() -> dict[str, str]:
    return {
        "G0_GOAL": "REQUIRED - narrow no-go class and ceiling frozen",
        "G1_CONVENTIONS": "REQUIRED - complete action, orbit, covariance and invariance fixed",
        "G2_CORE_ALGEBRA": "REQUIRED - exact transitivity and symbolic F1 identities",
        "G3_STRUCTURE": "REQUIRED - no-go and escape classes kept disjoint",
        "G4_INDEPENDENT_CHECK": "REQUIRED - semantic, code and new-reader audits",
        "G5_LIMITS_REGRESSION": "REQUIRED - incomplete group, multi-orbit, pair and F1 controls",
        "G6_PHYSICAL_MATCH": "N/A - no physical source, charge, node or measurement claim",
        "G7_OBSERVATION": "N/A - no observable, data or observational comparison",
        "G8_EXPORT": "N/A - internal Work2 theorem; no Canon, article, GitHub or Zenodo export",
    }


def review_requirements() -> dict[str, str]:
    return dict(EXPECTED_REVIEW_REQUIREMENTS)


def review_attestations() -> dict[str, dict[str, Any]]:
    return {
        "semantic_theorem_review": {
            "passed": True,
            "reviewer": "/root/f2_independent_review",
            "artifact": "independent theorem and escape-boundary verdict",
            "reviewed_payload_sha256": REVIEW_ATTESTED_PAYLOAD_IDS[
                "semantic_theorem_review"
            ],
            "reviewed_validator_sha256": REVIEW_ATTESTED_VALIDATOR_IDS[
                "semantic_theorem_review"
            ],
        },
        "fail_closed_code_review": {
            "passed": True,
            "reviewer": "/root/w209_no_go",
            "artifact": "independent fail-closed and adversarial-code verdict",
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
            "artifact": "independent contract, provenance and new-reader verdict",
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
        "CLAIM_ID": "W2_F2_SINGLE_ORBIT_WHOLE_STATE_READOUT_NO_GO_001",
        "CLAIM": (
            "At one fixed parameter point, every complete-equivalence-invariant whole-state "
            "report is constant on one transitive accepted orbit; this rejects only that route."
        ),
        "TYPE": "CONDITIONAL_EXACT_ROUTE_CLASS_NO_GO_WITH_SYMBOLIC_AND_EXHAUSTIVE_CONTROLS",
        "MODEL_VERSION": MODEL_VERSION,
        "ASSUMPTIONS": (
            "The frozen F2a contract and audited conditional F1 result are valid dependencies.",
            "One model parameter point is fixed and the accepted F1 minima form one full orbit.",
            "The declared O(3) conjugation is internal equivalence, not physical spatial rotation.",
            "The whole-state report is invariant under the complete declared equivalence.",
        ),
        "DOMAIN": (
            "One fixed-parameter transitive accepted orbit.  Multiple orbits, joint states, "
            "intrastate effect families, time, geometry, observables and data are outside the no-go."
        ),
        "CONVENTIONS": (
            "Orbit representatives are descriptions of one quotient class.  Invariant means a "
            "trivial output action; covariant means an explicitly declared output action."
        ),
        "FREEDOM_LEDGER": freedom_ledger(),
        "DEPENDENCIES": {
            "research_rules": (
                "the frozen W2-C0 file is the exact public runtime contract source; private "
                "governance remains C0 provenance and is not a runtime file"
            ),
            "programme_contract": PROGRAM_CONTRACT,
            "frozen_f2a_contract": F2A_MODEL_VERSION,
            "conditional_public_f1": F1_MODEL_VERSION,
            "c0_status_resolution": (
                "the frozen header and PASS_FOR_W2_C0_FREEZE audit are operative; the older "
                "section-3 sentence saying that the freeze audit is OPEN is recorded as stale "
                "text and supplies no scientific premise"
            ),
        },
        "METHOD": (
            "Prove the transitive-orbit theorem directly; exhaust a finite S3 action as an "
            "independent control; specialize exactly to the symbolic accepted F1 O(3) orbit."
        ),
        "PASS_CONDITION": (
            "The exact theorem, complete dependencies, finite and symbolic controls, escape-route "
            "firewalls, mutation controls and all detached independent reviews pass."
        ),
        "FAIL_CONDITION": (
            "Any incomplete equivalence, parameter/state conflation, preferred representative, "
            "F1-role erasure, escape-route rejection, malformed schema or review failure."
        ),
        "FALSIFIER": (
            "Two points of one transitive orbit and a genuinely complete-equivalence-invariant "
            "single-state report with unequal outputs."
        ),
        "RESIDUAL": "0 for the exact group-action identity and symbolic matrix identities.",
        "ERROR_BOUND": "0; no floating-point or observational calculation is used.",
        "VALIDITY_HEALTH": (
            "Exact only for one transitive orbit at fixed parameters and the complete declared "
            "equivalence.  It is not a no-go for all operational or relational constructions."
        ),
        "BRANCHES": {
            "one_orbit_invariant_whole_state": "REJECTED_IF_AUDIT_VALID",
            "covariant_representative_output": "VALID_BUT_NOT_AN_INVARIANT_REPORT",
            "intrastate_uniform_effect_family": "OPEN_UNEVALUATED",
            "derived_joint_common_action": "OPEN_UNEVALUATED",
            "multiple_accepted_orbits": "OPEN_UNEVALUATED",
        },
        "OBSERVABLE_MAP": {"status": "N/A", "reason": "internal theorem only"},
        "FORWARD_MODEL": {"status": "N/A", "reason": "no measurement or data chain"},
        "DATA_ROLE": {"status": "N/A", "reason": "no data used"},
        "IDENTIFIABILITY": (
            "A single quotient class is identifiable only as that class.  Representative entries "
            "and axes are description-dependent; different classes and internal relational "
            "structures require separate derived maps."
        ),
        "BENCHMARK": (
            "Finite complete versus incomplete group actions, one versus multiple orbits, common "
            "versus independent pair actions, and the exact F1 symbolic orbit are fixed controls."
        ),
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "CROSSCHECK": (
            "Direct analytic proof, exhaustive finite-group enumeration and an independent SymPy "
            "specialization share only the declared group-action assumptions."
        ),
        "PROVENANCE": {
            "date": "2026-07-21",
            "contract_version": MODEL_VERSION,
            "c0_version": PROGRAM_CONTRACT,
            "f2a_version": F2A_MODEL_VERSION,
            "f1_version": F1_MODEL_VERSION,
            "source_identities": {
                "c0": C0_SHA256,
                "f2a": F2A_SOURCE_SHA256,
                "f1": F1_SOURCE_SHA256,
            },
            "reviewed_payload_sha256": EXPECTED_PAYLOAD_SHA256,
            "payload_identity_rule": (
                "SHA-256 of the contract with only this digest replaced by "
                "<DETACHED_PAYLOAD_ID>"
            ),
            "validator_identity_rule": (
                "normalized-source SHA-256; only detached validator identity literals and review "
                "verdict booleans are normalized"
            ),
            "output_artifact": (
                "RefG/work 2/w2_11_f2_single_orbit_readout_no_go_gate.py"
            ),
        },
        "FILES": (
            "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
            "RefG/work 2/w2_10_f2a_internal_operational_distinction_contract.py",
            "RefG/work 2/w2_09a_f1_proof/refg_f1_atemporal_structural_proof.py",
            "RefG/work 2/w2_11_f2_single_orbit_readout_no_go_gate.py",
        ),
        "THEOREM": theorem_registry(),
        "REJECTED_ROUTE": rejected_route(),
        "PRESERVED_ROUTES": preserved_routes(),
        "FORBIDDEN_INPUTS": forbidden_inputs(),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
        "GATE_APPLICABILITY": gate_applicability(),
        "EXPORT_STATUS": dict(EXPECTED_EXPORT_STATUS),
        "INDEPENDENT_REVIEW": review_requirements(),
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
    return (
        isinstance(actual, dict)
        and set(actual) == set(expected)
        and all(type(actual[key]) is bool for key in expected)
        and all(actual[key] is expected[key] for key in expected)
    )


def exact_true_map(actual: Any, expected_keys: frozenset[str]) -> bool:
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
    try:
        payload = copy.deepcopy(contract)
        payload["PROVENANCE"]["reviewed_payload_sha256"] = "<DETACHED_PAYLOAD_ID>"
        canonical = json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
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
        source,
        count=1,
        flags=re.MULTILINE,
    )
    pattern = re.compile(
        r'^REVIEW_ATTESTED_VALIDATOR_IDS = \{.*?^\}\r?\n',
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(source)
    if count != 1 or match is None:
        return ""
    normalized = re.sub(
        r'"(?:[A-F0-9]{64}|PENDING)"',
        '"<ATTESTED_VALIDATOR_ID>"',
        match.group(0),
    )
    source = source[:match.start()] + normalized + source[match.end():]
    source, verdicts = re.subn(
        r'("passed":\s*)(?:True|False)',
        r'\1<DETACHED_REVIEW_VERDICT>',
        source,
    )
    if verdicts != len(EXPECTED_REVIEW_KEYS):
        return ""
    return hashlib.sha256(source.encode("utf-8")).hexdigest().upper()


def registry_shapes_valid(contract: dict[str, Any]) -> bool:
    freedom = contract.get("FREEDOM_LEDGER")
    return all((
        set(contract) == EXPECTED_STANDARD_FIELDS | EXPECTED_CUSTOM_FIELDS,
        set(contract.get("THEOREM", {})) == EXPECTED_THEOREM_KEYS,
        set(contract.get("REJECTED_ROUTE", {})) == EXPECTED_REJECTED_ROUTE_KEYS,
        set(contract.get("PRESERVED_ROUTES", {})) == EXPECTED_PRESERVED_ROUTE_KEYS,
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
        contract["PASS_CONDITION"], contract["VALIDITY_HEALTH"],
        *contract["THEOREM"].values(), *contract["PRESERVED_ROUTES"].values(),
    )
    corpus = "\n".join(fields).lower()
    forbidden = (
        "closes full f2", "proves f2a operational distinction",
        "o(3) is physical space", "o(3) is physical rotation",
        "all relational routes are rejected", "time emerges", "causality emerges",
    )
    return not any(token in corpus for token in forbidden)


def strict_contract_valid(contract: Any) -> bool:
    return bool(
        isinstance(contract, dict)
        and exact_tree_equal(contract, build_contract())
        and registry_shapes_valid(contract)
        and contract["MODEL_VERSION"] == MODEL_VERSION
        and contract["PROVENANCE"]["reviewed_payload_sha256"]
        == EXPECTED_PAYLOAD_SHA256
        and detached_payload_sha256(contract) == EXPECTED_PAYLOAD_SHA256
        and semantic_guard(contract)
    )


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def dependencies_valid() -> tuple[bool, dict[str, Any]]:
    if not all(path.is_file() for path in (C0_PATH, F2A_PATH, F1_PATH)):
        return False, {}
    c0 = C0_PATH.read_text(encoding="utf-8")
    f2a = load_module(F2A_PATH, "refg_f2a_for_w211")
    f2a_report = f2a.run_audit()
    f1 = load_module(F1_PATH, "refg_f1_for_w211")
    f1_report = f1.run_proof()
    spectral = f1_report.get("SECTION_RESULTS", {}).get("spectral", {}).get("checks", {})
    expected_imports = {
        "single_internal_carrier_Q", "Sym0_3_R_internal_state_space",
        "positive_internal_contraction_and_transpose",
        "matrix_product_and_algebraic_trace",
        "O3_conjugation_as_complete_declared_equivalence", "Q_sign_not_gauge",
        "quartic_functional_form_signs_and_truncation",
        "open_parameter_domain_alpha_b_c_positive", "atemporal_global_argmin_rule",
    }
    expected_f1_scope = {
        "foundation_law_derived", "functional_uniqueness_derived",
        "N3_physical_origin_derived", "temporal_formation_or_persistence",
        "physical_node_or_location", "operational_relations", "causal_order_or_clock",
        "independent_additive_physical_modes", "physical_dimension_or_continuum",
        "Lorentzian_metric_or_light_cone", "effective_action_or_conservation_law",
        "RefG_resonant_environment_map", "mass_pressure_particle_or_oscillon",
        "GR_PN_or_PPN_bridge", "observable_or_data_map",
    }
    expected_f1_evidence = {
        "public_definition_accepts_both_witness_kinds", "selected_witness_kind_explicit",
        "external_file_dependency_registry_empty", "primitive_registry_exactly_declared",
        "explicit_orientation_target_inputs_absent", "undifferentiated_reference_trivial",
        "law_O3_invariant_and_representative_target_free", "output_classification_complete",
        "intrinsic_differentiation_certified", "inequivalence_survives_declared_quotient",
        "law_forces_roles_not_arbitrary_basis", "law_selects_no_representative_orientation",
        "open_domain_structural_stability", "all_registered_primitives_labelled_imported",
        "no_go_route_boundaries_respected", "independent_crosschecks_and_controls",
        "listed_falsifier_checks_pass", "scope_ceiling_registry_exactly_false",
    }
    f2a_reviews = f2a_report.get("INDEPENDENT_REVIEW_ATTESTATIONS", {})
    f1_evidence = f1_report.get("PROMOTION_EVIDENCE", {})
    checks = all((
        C0_PATH.relative_to(ROOT).as_posix() == CLAIM_CONTRACT["FILES"][0],
        F2A_PATH.relative_to(ROOT).as_posix() == CLAIM_CONTRACT["FILES"][1],
        F1_PATH.relative_to(ROOT).as_posix() == CLAIM_CONTRACT["FILES"][2],
        Path(__file__).resolve().relative_to(ROOT).as_posix() == CLAIM_CONTRACT["FILES"][3],
        file_sha256(C0_PATH) == C0_SHA256,
        file_sha256(F1_PATH) == F1_SOURCE_SHA256,
        file_sha256(F2A_PATH) == F2A_SOURCE_SHA256,
        f"`{PROGRAM_CONTRACT}`" in c0,
        "### `W2_F2_OPERATIONAL_RELATIONS`" in c0,
        "### `W2_F3_INTERNAL_ORDER_CAUSALITY`" in c0,
        f2a.MODEL_VERSION == F2A_MODEL_VERSION,
        f2a_report.get("STATUS") == F2A_FROZEN_STATUS,
        f2a_report.get("AUDIT_VALID") is True,
        f2a_report.get("DETACHED_PAYLOAD_SHA256") == F2A_PAYLOAD_SHA256,
        f2a_report.get("DETACHED_VALIDATOR_SHA256") == F2A_VALIDATOR_SHA256,
        f2a_report.get("PROMOTED") is False,
        f2a_report.get("FULL_W2_F2_OPERATIONAL_RELATIONS") is False,
        f2a_report.get("SUBGATE_CLOSURE_FLAGS", {}).get("W2_F2A_CONTRACT_FROZEN")
        is True,
        f2a_report.get("SUBGATE_CLOSURE_FLAGS", {}).get("W2_F2A_CANDIDATE_EVALUATED")
        is False,
        f2a_report.get("SUBGATE_CLOSURE_FLAGS", {}).get(
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED"
        ) is False,
        set(f2a_reviews) == {
            "semantic_contract_review", "fail_closed_code_review",
            "new_reader_scope_review",
        },
        all(entry.get("passed") is True for entry in f2a_reviews.values()),
        f1.MODEL_VERSION == F1_MODEL_VERSION,
        f1_report.get("STATUS") == F1_STATUS,
        f1_report.get("AUDIT_VALID") is True,
        f1_report.get("PROMOTED") is True,
        set(f1_report.get("IMPORTED_PRIMITIVES", {})) == expected_imports,
        set(f1_report.get("IMPORTED_PRIMITIVES", {}).values())
        == {"IMPORTED_NOT_DERIVED"},
        set(f1_report.get("SCOPE_CEILING", {})) == expected_f1_scope,
        all(value is False for value in f1_report.get("SCOPE_CEILING", {}).values()),
        set(f1_evidence) == expected_f1_evidence,
        all(value is True for value in f1_evidence.values()),
        spectral.get("unique_nonzero_global_minimum_quotient_orbit_certified") is True,
        spectral.get("Q_generated_rank_1_rank_2_projectors_exact") is True,
        spectral.get("roles_nonexchangeable_and_Q_sign_not_law_symmetry") is True,
        spectral.get("origin_is_stationary_unstable_and_role_trivial") is True,
        spectral.get("negative_stationary_branch_rejected") is True,
        spectral.get("law_has_no_target_direction_projector_or_data_symbol") is True,
    ))
    return checks, {"f2a": f2a_report, "f1": f1_report}


Permutation = tuple[int, ...]
State = tuple[int, ...]


def act(permutation: Permutation, state: State) -> State:
    return tuple(state[index] for index in permutation)


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Composition compatible with act(left, act(right, state))."""
    return tuple(right[index] for index in left)


def inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for index, image in enumerate(permutation):
        result[image] = index
    return tuple(result)


def parity(permutation: Permutation) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def is_invariant(
    group: tuple[Permutation, ...], orbit: tuple[State, ...],
    readout: Callable[[State], Any],
) -> bool:
    return all(readout(act(g, state)) == readout(state) for g in group for state in orbit)


def finite_group_controls() -> dict[str, bool]:
    group = tuple(itertools.permutations(range(3)))
    identity = (0, 1, 2)
    seed = (0, 1, 2)
    orbit = tuple(sorted({act(g, seed) for g in group}))
    transitive = all(any(act(g, left) == right for g in group) for left in orbit for right in orbit)
    sorted_readout = lambda state: tuple(sorted(state))
    sum_readout = sum
    representative_readout = lambda state: state[0]
    covariant_output = lambda state: state
    quotient_output = lambda state: tuple(sorted(covariant_output(state)))

    even_group = tuple(g for g in group if parity(g) == 1)
    even_sample = tuple(sorted({act(g, seed) for g in even_group}))
    orientation = parity

    second_seed = (0, 1, 3)
    two_orbits = orbit + tuple(sorted({act(g, second_seed) for g in group}))
    orbit_labels = {tuple(sorted(state)) for state in two_orbits}

    e1, e2 = (1, 0, 0), (0, 1, 0)
    dot = lambda left, right: sum(a * b for a, b in zip(left, right))
    common_invariant = all(
        dot(act(g, left), act(g, right)) == dot(left, right)
        for g in group for left in (e1, e2) for right in (e1, e2)
    )
    independent_null = any(
        dot(act(g, e1), act(h, e1)) != dot(e1, e1)
        for g in group for h in group
    )

    structured = lambda _state: ((1, 0), (0, 1))
    structured_outputs = {structured(state) for state in orbit}
    return {
        "complete_group_and_transitive_orbit_exact": all((
            len(group) == 6, len(orbit) == 6, transitive,
            identity in group,
            all(compose(left, right) in group for left in group for right in group),
            all(
                compose(compose(first, second), third)
                == compose(first, compose(second, third))
                for first in group for second in group for third in group
            ),
            all(
                compose(g, inverse(g)) == identity
                and compose(inverse(g), g) == identity
                for g in group
            ),
            all(
                act(left, act(right, state)) == act(compose(left, right), state)
                for left in group for right in group for state in orbit
            ),
            all(act(g, state) in orbit for g in group for state in orbit),
        )),
        "invariant_whole_state_readouts_constant": all((
            is_invariant(group, orbit, sorted_readout),
            is_invariant(group, orbit, sum_readout),
            len({sorted_readout(state) for state in orbit}) == 1,
            len({sum_readout(state) for state in orbit}) == 1,
        )),
        "covariant_representative_varies_but_quotient_constant": all((
            all(covariant_output(act(g, state)) == act(g, covariant_output(state))
                for g in group for state in orbit),
            len({representative_readout(state) for state in orbit}) > 1,
            not is_invariant(group, orbit, representative_readout),
            len({quotient_output(state) for state in orbit}) == 1,
        )),
        "incomplete_equivalence_sampling_trap_rejected": all((
            len(even_sample) == 3,
            len({orientation(state) for state in even_sample}) == 1,
            is_invariant(even_group, orbit, orientation),
            len({orientation(state) for state in orbit}) == 2,
            not is_invariant(group, orbit, orientation),
        )),
        "multiple_orbit_escape_preserved": all((
            len(orbit_labels) == 2,
            is_invariant(group, tuple(two_orbits), sorted_readout),
        )),
        "common_action_pair_invariant_and_independent_action_null": all((
            common_invariant, independent_null, dot(e1, e1) == 1, dot(e1, e2) == 0,
        )),
        "constant_structured_output_not_entrywise_trivial": all((
            len(structured_outputs) == 1,
            {entry for row in structured(seed) for entry in row} == {0, 1},
        )),
    }


def matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.trigsimp(sp.simplify(entry)) == 0 for entry in matrix)


def f1_symbolic_controls() -> dict[str, bool]:
    theta = sp.symbols("theta", real=True)
    s = sp.symbols("s", nonzero=True, real=True)
    rotation = sp.Matrix([
        [sp.cos(theta), -sp.sin(theta), 0],
        [sp.sin(theta), sp.cos(theta), 0],
        [0, 0, 1],
    ])
    identity = sp.eye(3)
    q0 = s * sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
    qt = sp.trigsimp(rotation * q0 * rotation.T)
    i2_0, i3_0 = sp.trace(q0**2), sp.trace(q0**3)
    i2_t, i3_t = sp.trigsimp(sp.trace(qt**2)), sp.trigsimp(sp.trace(qt**3))

    p1_0 = sp.simplify(identity / 3 + q0 / s)
    p2_0 = sp.simplify(identity - p1_0)
    p1_t = sp.trigsimp(identity / 3 + qt / s)
    p2_t = sp.trigsimp(identity - p1_t)
    p1_covariance = sp.trigsimp(p1_t - rotation * p1_0 * rotation.T)
    p2_covariance = sp.trigsimp(p2_t - rotation * p2_0 * rotation.T)
    at_zero = sp.simplify(p1_t.subs(theta, 0))
    at_quarter = sp.simplify(p1_t.subs(theta, sp.pi / 2))

    n = sp.Matrix([1, 0, 0])
    minus_n = -n
    q_of_n = s * (n * n.T - identity / 3)
    q_of_minus_n = s * (minus_n * minus_n.T - identity / 3)
    central = -identity

    q_scale_1 = q0.subs(s, 1)
    q_scale_2 = q0.subs(s, 2)
    return {
        "symbolic_orbit_invariants_constant": all((
            matrix_zero(rotation.T * rotation - identity),
            sp.simplify(rotation.det()) == 1,
            sp.trigsimp(i2_t - i2_0) == 0,
            sp.trigsimp(i3_t - i3_0) == 0,
            sp.simplify(i2_0 - 2 * s**2 / 3) == 0,
            sp.simplify(i3_0 - 2 * s**3 / 9) == 0,
        )),
        "projectors_covariant_and_internal_roles_preserved": all((
            matrix_zero(p1_covariance), matrix_zero(p2_covariance),
            matrix_zero(p1_t**2 - p1_t), matrix_zero(p2_t**2 - p2_t),
            matrix_zero(p1_t * p2_t), matrix_zero(p1_t + p2_t - identity),
            sp.trigsimp(sp.trace(p1_t)) == 1,
            sp.trigsimp(sp.trace(p2_t)) == 2,
            p1_0.rank() == 1, p2_0.rank() == 2,
        )),
        "representative_entries_vary_and_are_not_invariant_reports": all((
            at_zero != at_quarter,
            at_zero[0, 0] == 1, at_quarter[0, 0] == 0,
            sp.trace(at_zero) == sp.trace(at_quarter) == 1,
        )),
        "preferred_axis_is_not_a_single_valued_state_readout": all((
            q_of_n == q_of_minus_n, n != minus_n,
            central * q_of_n * central.T == q_of_n,
            central * n == minus_n,
        )),
        "parameter_variation_is_not_same_fixed_parameter_orbit": all((
            sp.trace(q_scale_1**2) == sp.Rational(2, 3),
            sp.trace(q_scale_2**2) == sp.Rational(8, 3),
            sp.trace(q_scale_1**2) != sp.trace(q_scale_2**2),
        )),
    }


def mutation_controls() -> dict[str, bool]:
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
    for registry in (
        "THEOREM", "REJECTED_ROUTE", "PRESERVED_ROUTES", "FREEDOM_LEDGER",
        "SCOPE_CEILING", "CLOSURE_FLAGS", "GATE_APPLICABILITY",
        "EXPORT_STATUS", "INDEPENDENT_REVIEW",
    ):
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
    extra_forbidden = copy.deepcopy(base)
    extra_forbidden["FORBIDDEN_INPUTS"] += ("unregistered",)
    registry_mutants.append(extra_forbidden)

    boundary_mutants: list[dict[str, Any]] = []
    for registry, key in (
        ("CLOSURE_FLAGS", "W2_F2_OPERATIONAL_RELATIONS"),
        ("SCOPE_CEILING", "F2a_internal_operational_distinction_proved"),
        ("EXPORT_STATUS", "GITHUB"),
    ):
        mutant = copy.deepcopy(base)
        mutant[registry][key] = True
        boundary_mutants.append(mutant)

    semantic_mutants: list[dict[str, Any]] = []
    for field, text in (
        ("CLAIM", " This closes full F2."),
        ("DOMAIN", " O(3) is physical space."),
        ("METHOD", " All relational routes are rejected."),
    ):
        mutant = copy.deepcopy(base)
        mutant[field] += text
        semantic_mutants.append(mutant)
    erased_escape = copy.deepcopy(base)
    erased_escape["PRESERVED_ROUTES"]["intrastate_uniform_effect_family"] = "REJECTED"
    semantic_mutants.append(erased_escape)

    return {
        "missing_or_extra_contract_fields_rejected": all(
            not strict_contract_valid(mutant) for mutant in field_mutants
        ),
        "registry_drift_rejected": all(
            not strict_contract_valid(mutant) for mutant in registry_mutants
        ),
        "scope_closure_export_overclaims_rejected": all(
            not strict_contract_valid(mutant) for mutant in boundary_mutants
        ),
        "semantic_route_overclaims_rejected": all(
            not strict_contract_valid(mutant) for mutant in semantic_mutants
        ),
    }


def review_schema_valid(attestations: Any, require_pass: bool) -> bool:
    fields = {
        "passed", "reviewer", "artifact", "reviewed_payload_sha256",
        "reviewed_validator_sha256",
    }
    if not isinstance(attestations, dict) or set(attestations) != EXPECTED_REVIEW_KEYS:
        return False
    for entry in attestations.values():
        if not isinstance(entry, dict) or set(entry) != fields:
            return False
        if type(entry["passed"]) is not bool or (require_pass and entry["passed"] is not True):
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
    wrong_payload["semantic_theorem_review"]["reviewed_payload_sha256"] = "WRONG"
    mutants.append(wrong_payload)
    wrong_validator = copy.deepcopy(base)
    wrong_validator["new_reader_scope_review"]["reviewed_validator_sha256"] = "WRONG"
    mutants.append(wrong_validator)
    return all(not review_schema_valid(mutant, require_pass=False) for mutant in mutants)


def _run_audit_unchecked() -> dict[str, Any]:
    if not strict_contract_valid(CLAIM_CONTRACT):
        raise ValueError("contract payload or schema invalid")
    if detached_validator_sha256() != EXPECTED_VALIDATOR_SHA256:
        raise ValueError("validator source identity invalid")
    dependency_valid, dependencies = dependencies_valid()
    finite = finite_group_controls()
    symbolic = f1_symbolic_controls()
    mutations = mutation_controls()
    attestations = review_attestations()
    f1_spectral = dependencies.get("f1", {}).get("SECTION_RESULTS", {}).get(
        "spectral", {}
    ).get("checks", {})
    checks = {
        "payload_validator_and_contract_schema_exact": all((
            strict_contract_valid(CLAIM_CONTRACT),
            detached_validator_sha256() == EXPECTED_VALIDATOR_SHA256,
        )),
        "c0_f2a_and_f1_dependencies_exact": dependency_valid,
        "general_theorem_and_route_boundary_exact": all((
            set(CLAIM_CONTRACT["THEOREM"]) == EXPECTED_THEOREM_KEYS,
            CLAIM_CONTRACT["REJECTED_ROUTE"]["status"]
            == "REJECTED_BY_EXACT_NO_GO_ONLY_IN_THIS_DECLARED_CLASS",
            set(CLAIM_CONTRACT["PRESERVED_ROUTES"]) == EXPECTED_PRESERVED_ROUTE_KEYS,
        )),
        "finite_group_controls_exact": exact_true_map(finite, EXPECTED_FINITE_CHECK_KEYS),
        "f1_symbolic_specialization_exact": exact_true_map(symbolic, EXPECTED_F1_CHECK_KEYS),
        "f1_reference_and_role_regressions_preserved": all((
            f1_spectral.get("origin_is_stationary_unstable_and_role_trivial") is True,
            f1_spectral.get("Q_generated_rank_1_rank_2_projectors_exact") is True,
            f1_spectral.get("roles_nonexchangeable_and_Q_sign_not_law_symmetry") is True,
            CLAIM_CONTRACT["SCOPE_CEILING"]["F2a_internal_operational_distinction_proved"]
            is False,
        )),
        "scope_closure_gate_and_export_boundaries_exact": all((
            registry_shapes_valid(CLAIM_CONTRACT),
            exact_bool_map(CLAIM_CONTRACT["CLOSURE_FLAGS"], EXPECTED_C0_CLOSURE_FLAGS),
            exact_bool_map(CLAIM_CONTRACT["SCOPE_CEILING"], EXPECTED_SCOPE_CEILING),
            exact_bool_map(CLAIM_CONTRACT["EXPORT_STATUS"], EXPECTED_EXPORT_STATUS),
        )),
        "mutation_controls_exact": exact_true_map(mutations, EXPECTED_MUTATION_KEYS),
        "review_attestation_schema_fail_closed": review_schema_controls(),
        "review_attestations_complete": review_schema_valid(attestations, require_pass=True),
        "next_task_is_intrastate_effect_candidate_only": all((
            "w2_12_f2_intrastate_uniform_effect_family_candidate_gate.py"
            in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
            "full C0 F2 open" in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
            "time" not in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"].lower(),
            "GR" not in CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
        )),
    }
    schema_exact = (
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
    status = PASS_STATUS if audit_valid else READY_STATUS if structural_ready else INVALID_STATUS
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": status,
        "AUDIT_VALID": audit_valid,
        "STRUCTURAL_READY_FOR_REVIEW": structural_ready,
        "NO_GO_PROVED": audit_valid,
        "PROMOTED": False,
        "F2A_CANDIDATE_EVALUATED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "DETACHED_PAYLOAD_SHA256": detached_payload_sha256(CLAIM_CONTRACT),
        "DETACHED_VALIDATOR_SHA256": detached_validator_sha256(),
        "REJECTED_ROUTE": CLAIM_CONTRACT["REJECTED_ROUTE"],
        "PRESERVED_ROUTES": CLAIM_CONTRACT["PRESERVED_ROUTES"],
        "FINITE_GROUP_CONTROLS": finite,
        "F1_SYMBOLIC_CONTROLS": symbolic,
        "MUTATION_CONTROLS": mutations,
        "AUDIT_CHECKS": checks,
        "INDEPENDENT_REVIEW_ATTESTATIONS": attestations,
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F2A_SINGLE_ORBIT_WHOLE_STATE_INVARIANT_ROUTE_REJECTED": audit_valid,
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": False,
            "W2_F2A_CANDIDATE_EVALUATED": False,
        },
        "CLOSURE_FLAGS": CLAIM_CONTRACT["CLOSURE_FLAGS"],
        "SCOPE_CEILING": CLAIM_CONTRACT["SCOPE_CEILING"],
        "NEXT_ATOMIC_TASK": CLAIM_CONTRACT["NEXT_ATOMIC_TASK"],
    }


def fail_closed_invalid_report(error: Exception) -> dict[str, Any]:
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": INVALID_STATUS,
        "AUDIT_VALID": False,
        "STRUCTURAL_READY_FOR_REVIEW": False,
        "NO_GO_PROVED": False,
        "PROMOTED": False,
        "F2A_CANDIDATE_EVALUATED": False,
        "FULL_W2_F2_OPERATIONAL_RELATIONS": False,
        "DETACHED_PAYLOAD_SHA256": "",
        "DETACHED_VALIDATOR_SHA256": "",
        "REJECTED_ROUTE": {},
        "PRESERVED_ROUTES": {},
        "FINITE_GROUP_CONTROLS": {key: False for key in EXPECTED_FINITE_CHECK_KEYS},
        "F1_SYMBOLIC_CONTROLS": {key: False for key in EXPECTED_F1_CHECK_KEYS},
        "MUTATION_CONTROLS": {key: False for key in EXPECTED_MUTATION_KEYS},
        "AUDIT_CHECKS": {key: False for key in EXPECTED_AUDIT_KEYS},
        "INDEPENDENT_REVIEW_ATTESTATIONS": {},
        "SUBGATE_CLOSURE_FLAGS": {
            "W2_F2A_SINGLE_ORBIT_WHOLE_STATE_INVARIANT_ROUTE_REJECTED": False,
            "W2_F2A_INTERNAL_OPERATIONAL_DISTINCTION_PROVED": False,
            "W2_F2A_CANDIDATE_EVALUATED": False,
        },
        "CLOSURE_FLAGS": dict(EXPECTED_C0_CLOSURE_FLAGS),
        "SCOPE_CEILING": dict(EXPECTED_SCOPE_CEILING),
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
        report["NEXT_ATOMIC_TASK"] = "UNAVAILABLE"
        rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    return 0 if report["AUDIT_VALID"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
