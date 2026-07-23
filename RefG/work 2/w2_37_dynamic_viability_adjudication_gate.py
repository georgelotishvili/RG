"""Fail-closed adjudication of the displayed minimal RefG action.

This current-state certificate consumes the complete, self-pinned
w2_32--w2_36 chain.  The chain
proves exact background and unreduced action identities, including a direct
material-block degeneracy at the silent point.  It does not yet contain the
nonlinear constraint/gauge reduction needed to classify that degeneracy as a
physical pathology or as an auxiliary/gauge effect.

The only admissible present verdict is therefore deliberately asymmetric:
the exact static exterior is retained, dynamic continuation to the next gate
and the later PPN handoff are not authorized, and neither the minimal action
nor RefG as a theory is rejected.  A valid PASS below certifies this
adjudication logic; it is not a physical dynamics PASS.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any


CLAIM_ID = "W2_MINIMAL_ACTION_DYNAMIC_VIABILITY_ADJUDICATION_001"
MODEL_VERSION = "W2-MINIMAL-ACTION-DYNAMIC-ADJUDICATION-v1.0"

HERE = Path(__file__).resolve().parent
UPSTREAM_PATH = HERE / "w2_36_strong_coupling_eft_gate.py"

EXPECTED_UPSTREAM_CLAIM_ID = "W2_MINIMAL_ACTION_DIRECT_BLOCK_EFT_WARNING_GATE_002"
EXPECTED_UPSTREAM_MODEL_VERSION = "W2-MINIMAL-ACTION-DIRECT-BLOCK-EFT-WARNING-v2.1-PINNED"
EXPECTED_UPSTREAM_CONTRACT_SHA256 = (
    "A59F75F22715AFDA1C4AAEFE74950C78DFE8503E94D1C229736642B45AA5AF72"
)
EXPECTED_UPSTREAM_OUTCOMES_SHA256 = (
    "3710B602FB2320DCCADD7456DF9C1B62562009DA9CC8DA5ECC93364BD88228D0"
)
EXPECTED_UPSTREAM_PIN_SHA256 = (
    "484109A06D62489EDD33CAB0195CF04722F584103761A09BDE5542AE8499E99C"
)

UPSTREAM_SOURCE_SHA256 = {
    "w2_32_effective_action_dynamics_contract.py": (
        "992735E06C8EF276B70D0BA2D9FD195A80F892137C0BE186C4769A97D4229B87"
    ),
    "w2_33_adm_dirac_constraint_gate.py": (
        "8C3B2E8B5FBA47DB8B31A31F858AEA8078F2285D616AE47E56C56033E544009A"
    ),
    "w2_34_silent_vacuum_reduced_spectrum_gate.py": (
        "33E7F187F0D4FC6A6BFD10A1A2BD4EB223F8B0F210DE46640506EAEAC244F141"
    ),
    "w2_35_exponential_exterior_coupled_symbol_gate.py": (
        "8AF989AFC97B8CC862E4C2F10ADC9F6E16EDBC599E68D12E07FEE21BBA43F6DA"
    ),
    "w2_36_strong_coupling_eft_gate.py": (
        "53811BE8D13C9F4417FB6C8EB0BE1E439E07FCA3FA1693321F8B031009D2325D"
    ),
}

REQUIRED_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

STATE_KEYS = frozenset({
    "transitive_chain_valid",
    "exact_static_exterior_retained",
    "direct_block_warning_established",
    "constraint_reduction_complete",
    "reduced_physical_classification_complete",
    "reduced_physical_health_evidence",
    "reduced_physical_failure_evidence",
    "numerical_cutoff_evidence",
})

DECISION_KEYS = frozenset({
    "adjudication_valid",
    "exact_static_exterior_retained",
    "dynamic_promotion_authorized",
    "dynamic_promotion_not_authorized",
    "physical_verdict_open",
    "minimal_action_rejected",
    "full_RefG_rejected",
    "PPN_handoff_authorized",
    "versioned_completion_adopted",
})


def frozen_outcomes() -> dict[str, bool]:
    return {
        "w2_32_through_w2_36_transitive_integrity_proved": True,
        "exact_static_exterior_embedding_retained": True,
        "silent_direct_block_warning_established": True,
        "full_nonlinear_constraint_reduction_completed": False,
        "reduced_physical_spectrum_classified": False,
        "physical_dynamic_health_proved": False,
        "physical_dynamic_failure_proved": False,
        "numerical_strong_coupling_cutoff_derived": False,
        "minimal_action_dynamic_promotion_authorized": False,
        "minimal_action_rejected": False,
        "full_RefG_theory_rejected": False,
        "PPN_handoff_authorized": False,
        "versioned_completion_adopted": False,
        "next_full_constraint_reduction_gate_defined": True,
    }


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "effective_action_scope_synchronized": True,
        "exact_static_background_embedding_retained": True,
        "unreduced_direct_block_warning_closed": True,
        "full_nonlinear_Dirac_reduction_closed": False,
        "gauge_invariant_reduced_spectrum_closed": False,
        "physical_stability_and_hyperbolicity_closed": False,
        "strong_coupling_scale_closed": False,
        "minimal_action_dynamic_viability_closed": False,
        "foundation_to_effective_action_origin_closed": False,
        "Einstein_PPN_handoff_closed": False,
        "observational_validation_closed": False,
    }


EXPECTED_OUTCOMES = frozen_outcomes()
EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()

DEPENDENCY_SPEC: dict[str, Any] = {
    "filename": "w2_36_strong_coupling_eft_gate.py",
    "claim_id": EXPECTED_UPSTREAM_CLAIM_ID,
    "model_version": EXPECTED_UPSTREAM_MODEL_VERSION,
    "scientific_contract_sha256": EXPECTED_UPSTREAM_CONTRACT_SHA256,
    "outcomes_sha256": EXPECTED_UPSTREAM_OUTCOMES_SHA256,
    "upstream_pin_sha256": EXPECTED_UPSTREAM_PIN_SHA256,
    "source_sha256": UPSTREAM_SOURCE_SHA256,
    "transitive_requirement": (
        "w2_36 must execute w2_35, whose code-enforced chain executes and pins w2_32--w2_34"
    ),
}

NEXT_GATE_SPEC: dict[str, Any] = {
    "gate": "FULL_NONLINEAR_DIRAC_AND_GAUGE_INVARIANT_REDUCTION",
    "same_action_version": True,
    "required_work": [
        "derive every secondary and tertiary constraint without assuming its rank",
        "classify first- and second-class constraints on and near the silent stratum",
        "derive the reduced physical Hamiltonian and an independent covariant/SVT spectrum",
        "decide whether the null direct directions are auxiliary, gauge, or physical",
        "only for physical modes compute kinetic signs, characteristics and an EFT cutoff",
    ],
    "branching_rule": {
        "healthy_reduced_modes": "continue to the full exact-exterior coupled spectrum",
        "physical_null_interacting_mode": "reject only this frozen minimal action version",
        "unresolved_rank_or_boundary_dependence": "remain OPEN and do not enter PPN",
    },
    "prohibited_shortcuts": [
        "promoting an unreduced Hessian warning to a physical failure",
        "promoting exact static embedding to dynamic or PPN health",
        "adding a completion operator inside the frozen minimal action",
    ],
    "completion_rule": (
        "Any C^A C_A, D_H^2 or other repair is a separately frozen action version and reruns "
        "the complete dynamics chain; none is adopted here."
    ),
}

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "Adjudicate the self-pinned minimal-action dynamics chain without overclaiming: "
        "retain the exact static exterior and the exact unreduced direct-block warning, "
        "block dynamic continuation until full constraint reduction and keep the later PPN "
        "handoff closed, while rejecting neither the minimal action nor RefG as the physical "
        "classification remains open."
    ),
    "TYPE": "CURRENT_STATE_FAIL_CLOSED_ADJUDICATION_WITH_OPEN_PHYSICAL_VERDICT",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "The frozen displayed minimal action is audited exactly as written. It is a "
        "target-conditioned effective candidate, not a foundation-derived action. No omitted "
        "completion operator, observational target or desired GR/PPN answer is inserted."
    ),
    "DOMAIN": (
        "The w2_32--w2_36 action, gauge-fixed ADM, silent-Minkowski, exact-exterior and "
        "unreduced perturbative domains already declared by those self-pinned gates."
    ),
    "CONVENTIONS": (
        "Artifact validity and physical validity are distinct. OPEN means neither PASS nor "
        "REJECTED. A static exact solution is not a dynamics-health certificate."
    ),
    "FREEDOM_LEDGER": {
        "current_action": "frozen minimal version; no hidden repair",
        "constraint_reduction": "not yet completed",
        "completion": "permitted only as a future separately versioned candidate",
        "fit_or_data": "none",
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_32_effective_action_dynamics_contract.py",
        "RefG/work 2/w2_33_adm_dirac_constraint_gate.py",
        "RefG/work 2/w2_34_silent_vacuum_reduced_spectrum_gate.py",
        "RefG/work 2/w2_35_exponential_exterior_coupled_symbol_gate.py",
        "RefG/work 2/w2_36_strong_coupling_eft_gate.py",
    ],
    "METHOD": (
        "Execute w2_36 and require its transitive upstream controls, scientific hashes and exact "
        "source-file hashes. Build a "
        "strict Boolean evidence state and apply a decision table that forbids health or failure "
        "without completed reduction and mutually exclusive reduced evidence. Freeze the result "
        "as a versioned snapshot; a changed upstream verdict requires a new certificate version."
    ),
    "PASS_CONDITION": (
        "PASS means only that the transitive evidence and fail-closed decision table agree: the "
        "static result is retained, promotion is blocked and the physical verdict is OPEN."
    ),
    "FAIL_CONDITION": (
        "Upstream drift, a non-Boolean state, contradictory reduced evidence, promotion without "
        "a healthy reduced classification, rejection without reduced failure evidence, or PPN "
        "handoff while dynamics is open invalidates the adjudication."
    ),
    "FALSIFIER": (
        "A complete nonlinear Dirac plus independent gauge-invariant reduction replaces OPEN. "
        "Healthy physical modes authorize only the next spectrum gate, not PPN; a proved "
        "physical null interacting mode rejects only this frozen minimal action version."
    ),
    "RESIDUAL": "Exact Boolean and hash equality; no fitted residual.",
    "ERROR_BOUND": "Zero for declared identities; physical spectrum and cutoff remain uncomputed.",
    "VALIDITY_HEALTH": (
        "The decision table tests both forbidden overclaims and both legitimate future resolutions."
    ),
    "BRANCHES": {
        "exact_static_exterior": "RETAINED",
        "minimal_action_physical_dynamics": "OPEN__PROMOTION_NOT_AUTHORIZED",
        "minimal_action_rejection": "NOT_ESTABLISHED",
        "full_RefG_rejection": "NOT_ESTABLISHED",
        "PPN_handoff": "BLOCKED_BY_OPEN_DYNAMICS",
        "versioned_completion": "AVAILABLE_BY_PROTOCOL__NOT_ADOPTED",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "dynamics has not reached PPN"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "reduced physical evolution is open"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, calibration or target"},
    "IDENTIFIABILITY": (
        "The present evidence identifies a direct-block rank warning, not its reduced physical class."
    ),
    "BENCHMARK": NEXT_GATE_SPEC,
    "CLOSURE_FLAGS": frozen_closure_flags(),
    "CROSSCHECK": (
        "Healthy and failed reduced future states are separately injected into the decision table; "
        "each resolves OPEN in the correct direction, while unresolved overclaims are rejected."
    ),
    "PROVENANCE": {
        "date": "2026-07-23",
        "data": "none",
        "target_conditioned_effective_action": True,
        "foundation_origin_claimed": False,
        "manuscript_modified": False,
        "current_state_snapshot_certificate": True,
    },
    "FILES": ["RefG/work 2/w2_37_dynamic_viability_adjudication_gate.py"],
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def _sha(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


EXPECTED_DEPENDENCY_SHA256 = (
    "445ED8FEBA651742310C0D6F2D8E7C9D0183B655B26C047CC981914E161CCEE7"
)
EXPECTED_CONTRACT_SHA256 = (
    "5485865361891B8E64CD1B7C5043E747C8E535F9203B3CD67FF5D719C60DA024"
)
EXPECTED_OUTCOMES_SHA256 = (
    "D40F84E60B322693704482DD565684DB1DF4C35BC09C14E0983576F06167F2FC"
)
EXPECTED_NEXT_GATE_SHA256 = (
    "7842745FFF6CE14B8822890756F5DF1C237C31805C70B34CEB156DCF00154593"
)


def _load_module(path: Path, tag: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(tag, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def load_upstream() -> tuple[ModuleType, dict[str, Any]]:
    module = _load_module(UPSTREAM_PATH, "w2_36_for_w2_37")
    return module, module.run()


def _strict_bool_map(value: Any, keys: frozenset[str]) -> bool:
    return isinstance(value, dict) and set(value) == set(keys) and all(
        type(item) is bool for item in value.values()
    )


def _source_pins_match(expected: dict[str, str]) -> bool:
    return expected == UPSTREAM_SOURCE_SHA256 and all(
        _file_sha256(HERE / filename) == digest
        for filename, digest in expected.items()
    )


def upstream_state(
    source_sha256: dict[str, str] | None = None,
) -> tuple[dict[str, bool], dict[str, Any]]:
    source_pins = UPSTREAM_SOURCE_SHA256 if source_sha256 is None else source_sha256
    module, report = load_upstream()
    upstream_controls = report.get("upstream_controls", {})
    evidence = report.get("evidence", {})
    decision = report.get("decision", {})
    outcomes = report.get("outcomes", {})
    closures = report.get("closure_flags", {})
    hashes = report.get("hashes", {})

    chain_valid = all((
        report.get("valid") is True,
        module.CLAIM_ID == EXPECTED_UPSTREAM_CLAIM_ID,
        module.MODEL_VERSION == EXPECTED_UPSTREAM_MODEL_VERSION,
        report.get("artifact") == module.CLAIM_ID,
        report.get("model_version") == EXPECTED_UPSTREAM_MODEL_VERSION,
        hashes.get("scientific_contract") == EXPECTED_UPSTREAM_CONTRACT_SHA256,
        hashes.get("outcomes") == EXPECTED_UPSTREAM_OUTCOMES_SHA256,
        module.EXPECTED_CONTRACT_SHA256 == EXPECTED_UPSTREAM_CONTRACT_SHA256,
        module.EXPECTED_OUTCOMES_SHA256 == EXPECTED_UPSTREAM_OUTCOMES_SHA256,
        module.EXPECTED_UPSTREAM_PIN_SHA256 == EXPECTED_UPSTREAM_PIN_SHA256,
        bool(upstream_controls),
        all(type(item) is bool and item for item in upstream_controls.values()),
        bool(evidence),
        all(type(item) is bool and item for item in evidence.values()),
        _source_pins_match(source_pins),
    ))
    static_retained = all((
        outcomes.get("exact_static_exterior_embedding_retained") is True,
        closures.get("exact_static_background_closure_retained") is True,
    ))
    warning = all((
        decision.get("necessary_direct_block_warning") is True,
        evidence.get("silent_direct_material_velocity_hessian_zero") is True,
        outcomes.get("silent_direct_material_quadratic_velocity_hessian_zero_proved") is True,
    ))
    reduction_complete = all((
        closures.get("constraint_reduced_physical_kinetic_health_closed") is True,
        closures.get("constraint_or_gauge_removal_closed") is True,
    ))
    classification_complete = all((
        reduction_complete,
        outcomes.get("physical_verdict_closed") is True,
    ))
    physical_health = all((
        classification_complete,
        outcomes.get("physical_EFT_health_proved") is True,
        outcomes.get("physical_strong_coupling_or_EFT_failure_proved") is False,
    ))
    physical_failure = all((
        classification_complete,
        outcomes.get("physical_strong_coupling_or_EFT_failure_proved") is True,
    ))
    cutoff = outcomes.get("numerical_strong_coupling_scale_derived") is True

    state = {
        "transitive_chain_valid": bool(chain_valid),
        "exact_static_exterior_retained": bool(static_retained),
        "direct_block_warning_established": bool(warning),
        "constraint_reduction_complete": bool(reduction_complete),
        "reduced_physical_classification_complete": bool(classification_complete),
        "reduced_physical_health_evidence": bool(physical_health),
        "reduced_physical_failure_evidence": bool(physical_failure),
        "numerical_cutoff_evidence": bool(cutoff),
    }
    diagnostics = {
        "upstream_artifact": report.get("artifact"),
        "upstream_model_version": report.get("model_version"),
        "upstream_status": report.get("status"),
        "upstream_hashes": hashes,
        "upstream_source_hashes": {
            filename: _file_sha256(HERE / filename)
            for filename in source_pins
        },
        "transitive_upstream_controls": upstream_controls,
        "upstream_decision": decision,
    }
    return state, diagnostics


def adjudicate(state: dict[str, bool]) -> dict[str, bool]:
    strict = _strict_bool_map(state, STATE_KEYS)
    base = bool(strict and state["transitive_chain_valid"])
    reduction = bool(base and state["constraint_reduction_complete"])
    classification = bool(base and state["reduced_physical_classification_complete"])
    health = bool(base and state["reduced_physical_health_evidence"])
    failure = bool(base and state["reduced_physical_failure_evidence"])
    warning = bool(base and state["direct_block_warning_established"])

    consistency = all((
        not classification or reduction,
        not health or classification,
        not failure or classification,
        not (health and failure),
        not classification or (health != failure),
        # A controlled numerical cutoff can belong to either a healthy or a
        # failed reduced theory; it requires classification, not failure.
        not state.get("numerical_cutoff_evidence", False) or classification,
    )) if strict else False
    valid = bool(base and consistency and state["exact_static_exterior_retained"] and warning)
    authorize = bool(valid and reduction and classification and health and not failure)
    reject_minimal = bool(valid and reduction and classification and failure and not health)
    open_verdict = bool(valid and not authorize and not reject_minimal)
    return {
        "adjudication_valid": valid,
        "exact_static_exterior_retained": bool(valid and state["exact_static_exterior_retained"]),
        "dynamic_promotion_authorized": authorize,
        "dynamic_promotion_not_authorized": bool(valid and not authorize),
        "physical_verdict_open": open_verdict,
        "minimal_action_rejected": reject_minimal,
        "full_RefG_rejected": False,
        # Even a healthy silent reduction opens only the next exterior-spectrum
        # gate.  Source matching and the remaining dynamics gates still precede PPN.
        "PPN_handoff_authorized": False,
        "versioned_completion_adopted": False,
    }


def definition_controls() -> dict[str, bool]:
    changed_contract = deepcopy(CLAIM_CONTRACT)
    changed_contract["BRANCHES"]["minimal_action_rejection"] = "REJECTED"
    changed_outcomes = deepcopy(EXPECTED_OUTCOMES)
    changed_outcomes["PPN_handoff_authorized"] = True
    changed_source_pins = deepcopy(UPSTREAM_SOURCE_SHA256)
    changed_source_pins[sorted(changed_source_pins)[0]] = "0" * 64
    return {
        "contract_schema_exact": set(CLAIM_CONTRACT) == set(REQUIRED_FIELDS),
        "claim_identity_exact": all((
            CLAIM_CONTRACT["CLAIM_ID"] == CLAIM_ID,
            CLAIM_CONTRACT["MODEL_VERSION"] == MODEL_VERSION,
        )),
        "ledgers_exact": all((
            frozen_outcomes() == EXPECTED_OUTCOMES,
            frozen_closure_flags() == EXPECTED_CLOSURE_FLAGS,
            CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS,
        )),
        "dependency_hash_exact": _sha(DEPENDENCY_SPEC) == EXPECTED_DEPENDENCY_SHA256,
        "contract_hash_exact": _sha(CLAIM_CONTRACT) == EXPECTED_CONTRACT_SHA256,
        "outcomes_hash_exact": _sha(EXPECTED_OUTCOMES) == EXPECTED_OUTCOMES_SHA256,
        "next_gate_hash_exact": _sha(NEXT_GATE_SPEC) == EXPECTED_NEXT_GATE_SHA256,
        "contract_overclaim_mutation_detected": (
            _sha(changed_contract) != EXPECTED_CONTRACT_SHA256
        ),
        "PPN_promotion_mutation_detected": (
            _sha(changed_outcomes) != EXPECTED_OUTCOMES_SHA256
        ),
        "source_hash_mismatch_mutation_detected": (
            upstream_state(changed_source_pins)[0]["transitive_chain_valid"] is False
        ),
    }


def mutation_controls(state: dict[str, bool]) -> dict[str, bool]:
    chain_broken = deepcopy(state)
    chain_broken["transitive_chain_valid"] = False
    premature_health = deepcopy(state)
    premature_health["reduced_physical_health_evidence"] = True
    premature_failure = deepcopy(state)
    premature_failure["reduced_physical_failure_evidence"] = True
    premature_cutoff = deepcopy(state)
    premature_cutoff["numerical_cutoff_evidence"] = True
    healthy = deepcopy(state)
    healthy.update({
        "constraint_reduction_complete": True,
        "reduced_physical_classification_complete": True,
        "reduced_physical_health_evidence": True,
        "numerical_cutoff_evidence": True,
    })
    failed = deepcopy(state)
    failed.update({
        "constraint_reduction_complete": True,
        "reduced_physical_classification_complete": True,
        "reduced_physical_failure_evidence": True,
    })
    contradictory = deepcopy(healthy)
    contradictory["reduced_physical_failure_evidence"] = True
    classification_without_resolution = deepcopy(state)
    classification_without_resolution.update({
        "constraint_reduction_complete": True,
        "reduced_physical_classification_complete": True,
    })

    chain_decision = adjudicate(chain_broken)
    premature_health_decision = adjudicate(premature_health)
    premature_failure_decision = adjudicate(premature_failure)
    premature_cutoff_decision = adjudicate(premature_cutoff)
    healthy_decision = adjudicate(healthy)
    failed_decision = adjudicate(failed)
    contradictory_decision = adjudicate(contradictory)
    unresolved_classification_decision = adjudicate(classification_without_resolution)
    nonboolean = deepcopy(state)
    nonboolean["constraint_reduction_complete"] = 0
    missing_key = deepcopy(state)
    missing_key.pop("constraint_reduction_complete")
    extra_key = {**state, "undeclared_state": False}
    nonboolean_decision = adjudicate(nonboolean)
    missing_key_decision = adjudicate(missing_key)
    extra_key_decision = adjudicate(extra_key)

    return {
        "single_broken_dependency_invalidates_adjudication": (
            chain_decision["adjudication_valid"] is False
        ),
        "premature_health_assertion_is_rejected": (
            premature_health_decision["adjudication_valid"] is False
        ),
        "premature_failure_assertion_is_rejected": (
            premature_failure_decision["adjudication_valid"] is False
        ),
        "premature_cutoff_assertion_is_rejected": (
            premature_cutoff_decision["adjudication_valid"] is False
        ),
        "completed_healthy_reduction_authorizes_only_next_handoff": all((
            healthy_decision["adjudication_valid"] is True,
            healthy_decision["dynamic_promotion_authorized"] is True,
            healthy_decision["minimal_action_rejected"] is False,
            healthy_decision["physical_verdict_open"] is False,
            healthy_decision["PPN_handoff_authorized"] is False,
        )),
        "completed_failed_reduction_rejects_only_minimal_version": all((
            failed_decision["adjudication_valid"] is True,
            failed_decision["minimal_action_rejected"] is True,
            failed_decision["full_RefG_rejected"] is False,
            failed_decision["PPN_handoff_authorized"] is False,
        )),
        "contradictory_health_and_failure_is_rejected": (
            contradictory_decision["adjudication_valid"] is False
        ),
        "completed_classification_without_resolution_is_rejected": (
            unresolved_classification_decision["adjudication_valid"] is False
        ),
        "nonboolean_state_is_rejected": all((
            not _strict_bool_map(nonboolean, STATE_KEYS),
            nonboolean_decision["adjudication_valid"] is False,
        )),
        "missing_or_extra_state_key_is_rejected": all((
            not _strict_bool_map(missing_key, STATE_KEYS),
            not _strict_bool_map(extra_key, STATE_KEYS),
            missing_key_decision["adjudication_valid"] is False,
            extra_key_decision["adjudication_valid"] is False,
        )),
    }


def run() -> dict[str, Any]:
    state, diagnostics = upstream_state()
    decision = adjudicate(state)
    definition = definition_controls()
    mutations = mutation_controls(state)
    expected_decision = {
        "adjudication_valid": True,
        "exact_static_exterior_retained": True,
        "dynamic_promotion_authorized": False,
        "dynamic_promotion_not_authorized": True,
        "physical_verdict_open": True,
        "minimal_action_rejected": False,
        "full_RefG_rejected": False,
        "PPN_handoff_authorized": False,
        "versioned_completion_adopted": False,
    }
    valid = bool(
        _strict_bool_map(state, STATE_KEYS)
        and _strict_bool_map(decision, DECISION_KEYS)
        and decision == expected_decision
        and all(type(item) is bool and item for item in definition.values())
        and all(type(item) is bool and item for item in mutations.values())
        and EXPECTED_OUTCOMES == {
            "w2_32_through_w2_36_transitive_integrity_proved": state["transitive_chain_valid"],
            "exact_static_exterior_embedding_retained": decision["exact_static_exterior_retained"],
            "silent_direct_block_warning_established": state["direct_block_warning_established"],
            "full_nonlinear_constraint_reduction_completed": state["constraint_reduction_complete"],
            "reduced_physical_spectrum_classified": state["reduced_physical_classification_complete"],
            "physical_dynamic_health_proved": state["reduced_physical_health_evidence"],
            "physical_dynamic_failure_proved": state["reduced_physical_failure_evidence"],
            "numerical_strong_coupling_cutoff_derived": state["numerical_cutoff_evidence"],
            "minimal_action_dynamic_promotion_authorized": decision["dynamic_promotion_authorized"],
            "minimal_action_rejected": decision["minimal_action_rejected"],
            "full_RefG_theory_rejected": decision["full_RefG_rejected"],
            "PPN_handoff_authorized": decision["PPN_handoff_authorized"],
            "versioned_completion_adopted": decision["versioned_completion_adopted"],
            "next_full_constraint_reduction_gate_defined": bool(NEXT_GATE_SPEC),
        }
    )
    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": valid,
        "status": (
            "PASS_FAIL_CLOSED_DYNAMIC_ADJUDICATION__EXACT_STATIC_EXTERIOR_RETAINED__"
            "MINIMAL_ACTION_PROMOTION_NOT_AUTHORIZED__PHYSICAL_VERDICT_OPEN"
            if valid else "INVALID_ADJUDICATION_NO_SCIENTIFIC_PROMOTION_OR_REJECTION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "state": state,
        "decision": decision,
        "outcomes": frozen_outcomes(),
        "closure_flags": frozen_closure_flags(),
        "next_gate": NEXT_GATE_SPEC,
        "controls": {"definition": definition, "mutation": mutations},
        "upstream_diagnostics": diagnostics,
        "hashes": {
            "dependency_spec": _sha(DEPENDENCY_SPEC),
            "scientific_contract": _sha(CLAIM_CONTRACT),
            "outcomes": _sha(EXPECTED_OUTCOMES),
            "next_gate": _sha(NEXT_GATE_SPEC),
        },
    }


def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_ID,
            "model_version": MODEL_VERSION,
            "valid": False,
            "status": "INVALID_ADJUDICATION_NO_SCIENTIFIC_PROMOTION_OR_REJECTION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
