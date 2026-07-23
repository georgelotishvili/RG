"""Direct-block EFT diagnostic for the displayed minimal RefG action.

At the silent point the direct material-label velocity Hessian vanishes.  By
continuity, that unreduced block cannot possess a strictly positive uniform
lower bound on a neighborhood that includes the silent point.  For F_min, the
velocity-bearing part of the cubic Lagrangian is proportional to the linear
clock--volume deformation; its direct Hessian reverses sign between opposite
off-shell deformations.

Neither statement is a reduced physical-mode theorem.  Constraint, gauge or
auxiliary removal has not been completed, the opposite deformations have not
been shown to be on-shell backgrounds, and no numerical strong-coupling scale
is derived.  The result is therefore a necessary warning, not an EFT/theory
failure: promotion is not authorized and the physical verdict remains OPEN.
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

import sympy as sp


CLAIM_ID = "W2_MINIMAL_ACTION_DIRECT_BLOCK_EFT_WARNING_GATE_002"
MODEL_VERSION = "W2-MINIMAL-ACTION-DIRECT-BLOCK-EFT-WARNING-v2.1-PINNED"
HERE = Path(__file__).resolve().parent

UPSTREAM_PIN_SPEC: dict[str, Any] = {
    "claim_id": "W2_EXACT_EXTERIOR_DIRECT_BLOCK_WARNING_GATE_002",
    "model_version": "W2-EXTERIOR-DIRECT-BLOCK-WARNING-v2.1-PINNED",
    "scientific_contract_sha256": (
        "E1A2ABFDC6FDE009A391DA2D0BE3D55759C3EE95A8070B64CE3FD53612E210FC"
    ),
    "outcomes_sha256": (
        "BB2DC16DE55CECD5C4CCCD62E251E62233EA1A62207952ED1158B010932425D5"
    ),
    "upstream_pin_sha256": (
        "B3FD1F929A13B624B1310E5973529DBF785AF6FEA7E22582E072757252368409"
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

EVIDENCE_KEYS = frozenset({
    "Fmin_full_quadratic_coefficient_in_unreduced_bookkeeping_exact",
    "Fmin_full_cubic_coefficient_with_abstract_nonvelocity_terms_exact",
    "Fmin_velocity_bearing_cubic_subpart_exact",
    "Fmin_direct_cubic_velocity_hessian_exact",
    "silent_direct_material_velocity_hessian_zero",
    "opposite_offshell_deformations_reverse_direct_Fmin_hessian",
    "opposite_direct_coefficients_have_opposite_sign_for_c_nonzero",
    "generic_continuity_excludes_positive_direct_lower_bound_at_silent_point",
    "excluded_C2_operator_changes_direct_velocity_rank",
})

UPSTREAM_KEYS = frozenset({
    "w2_35_code_imported_valid_and_self_pinned",
    "w2_32_through_w2_34_integrity_enforced_transitively",
    "w2_34_unreduced_Fmin_hessian_report_consumed",
    "upstream_physical_verdict_remains_open",
})

DECISION_KEYS = frozenset({
    "necessary_direct_block_warning",
    "constraint_or_gauge_removal_open",
    "promotion_not_authorized",
    "physical_verdict_open",
    "physical_EFT_health_proved",
    "physical_EFT_failure_proved",
    "numerical_cutoff_derived",
})


def frozen_outcomes() -> dict[str, bool]:
    return {
        "silent_direct_material_quadratic_velocity_hessian_zero_proved": True,
        "Fmin_velocity_bearing_cubic_subpart_proved": True,
        "Fmin_direct_unreduced_offshell_hessian_sign_reversal_proved": True,
        "generic_direct_block_uniform_positive_lower_bound_including_silent_point": False,
        "generic_silent_response_sign_flip_proved": False,
        "on_shell_two_sided_Fmin_background_family_proved": False,
        "constraint_or_gauge_removal_of_null_directions_excluded": False,
        "reduced_physical_kinetic_sign_flip_proved": False,
        "physical_strong_coupling_or_EFT_failure_proved": False,
        "physical_EFT_health_proved": False,
        "amplitude_independent_canonical_normalization_proved": False,
        "numerical_strong_coupling_scale_derived": False,
        "uniform_EFT_control_proved": False,
        "excluded_C2_operator_changes_direct_quadratic_rank_proved": True,
        "completion_operator_adopted_in_current_action": False,
        "dynamic_promotion_authorized": False,
        "physical_verdict_closed": False,
        "exact_static_exterior_embedding_retained": True,
    }


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "exact_static_background_closure_retained": True,
        "direct_block_warning_closed": True,
        "constraint_reduced_physical_kinetic_health_closed": False,
        "constraint_or_gauge_removal_closed": False,
        "uniform_strong_coupling_scale_closed": False,
        "minimal_action_dynamic_viability_closed": False,
        "physical_EFT_verdict_closed": False,
        "completion_action_selected": False,
        "full_PPN_and_observation_closed": False,
    }


EXPECTED_OUTCOMES = frozen_outcomes()
EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "The displayed minimal action has an exact direct-block warning at its "
        "silent branch: the unreduced material velocity Hessian vanishes there, "
        "and F_min's velocity-bearing cubic subpart gives a direct off-shell "
        "Hessian with opposite signs on opposite clock--volume deformations. "
        "No physical EFT failure is inferred before constraint reduction."
    ),
    "TYPE": "EXACT_DIRECT_BLOCK_EFT_DIAGNOSTIC_WITH_OPEN_PHYSICAL_VERDICT",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "F is smooth at the silent point, F_,B vanishes there, and the frozen "
        "minimal action contains no C^A C_A or other omitted completion operator. "
        "The F_min sign-reversal statement uses c nonzero and refers only to the "
        "direct unreduced off-shell Hessian."
    ),
    "DOMAIN": (
        "A perturbative neighborhood containing the silent Minkowski point. The "
        "direct-block continuity result also applies pointwise on the normalized "
        "silent exterior, without asserting a reduced exterior spectrum."
    ),
    "CONVENTIONS": (
        "A direct Hessian is not a physical reduced kinetic matrix. A uniform "
        "positive direct-block lower bound would require K_direct>=lambda I with "
        "lambda>0 even at the silent point; K_direct(0)=0 disproves only that bound."
    ),
    "FREEDOM_LEDGER": {
        "Fmin_scale_c": "real nonzero coefficient; no sign chosen from a target",
        "generic_response": "smooth silent-point class; no assumed leading parity or sign",
        "completion_C2": "negative control only; coefficient remains zero in current action",
        "constraint_reduction": "absent and explicitly open",
        "data_or_fit": "none",
    },
    "DEPENDENCIES": {
        "transitive_files": [
            "RefG/work 2/w2_32_effective_action_dynamics_contract.py",
            "RefG/work 2/w2_33_adm_dirac_constraint_gate.py",
            "RefG/work 2/w2_34_silent_vacuum_reduced_spectrum_gate.py",
        ],
        "immediate_file": "RefG/work 2/w2_35_exponential_exterior_coupled_symbol_gate.py",
        "frozen_immediate_pin": UPSTREAM_PIN_SPEC,
    },
    "METHOD": (
        "Import w2_35, which code-imports and enforces the self-pinned w2_32--w2_34 "
        "reports. Expand the complete F_min normal form schematically through cubic "
        "order, retaining abstract nonvelocity Q2 and det(E1) terms, then extract only "
        "the velocity-bearing subpart. Test the direct Hessian on opposite off-shell "
        "deformations. Use K_direct(0)=0, not a fabricated generic odd expansion, to "
        "exclude a positive direct-block lower bound containing the silent point."
    ),
    "PASS_CONDITION": (
        "PASS means the exact direct-block formulas, upstream integrity, scope limits, "
        "hashes and mutation controls agree. It requires promotion_not_authorized and "
        "physical_verdict_open; it is not an EFT-health pass or fail."
    ),
    "FAIL_CONDITION": (
        "A coefficient/sign error, upstream invalidity, generic sign-flip assertion, "
        "conflation of the velocity subpart with the full cubic response, or a physical "
        "strong-coupling verdict without reduction invalidates this audit."
    ),
    "FALSIFIER": (
        "A counterexample to a displayed direct-block identity falsifies that identity. "
        "The full nonlinear Dirac/gauge reduction is required work, not a burden placed "
        "on a competing interpretation; it will decide the currently open verdict."
    ),
    "RESIDUAL": "Zero exact polynomial residuals for every asserted perturbative coefficient.",
    "ERROR_BOUND": "No numerical approximation and no numerical cutoff or physical scale claim.",
    "VALIDITY_HEALTH": (
        "Continuity proves only loss of a uniform lower bound for the direct block. "
        "The F_min sign reversal is special, off-shell and unreduced. Generic sign "
        "reversal, a physical ghost and strong coupling all remain unproved. A future "
        "healthy verdict requires positive reduced health evidence; absence of failure "
        "is not evidence of health."
    ),
    "BRANCHES": {
        "generic_silent_F_direct_block": "ZERO_LOWER_BOUND_AT_SILENT_POINT_ONLY",
        "F_min_direct_block": "OFFSHELL_CUBIC_SIGN_REVERSAL_WARNING",
        "constraint_or_gauge_removal": "OPEN",
        "reduced_physical_EFT_verdict": "OPEN",
        "excluded_C2_completion": "NEGATIVE_CONTROL_ONLY",
        "exact_static_exterior": "RETAINED",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "pre-observational direct-block diagnostic"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "reduced dynamics is open"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, target or fitted coefficient"},
    "IDENTIFIABILITY": (
        "Generic continuity and F_min-specific off-shell sign reversal are separate. "
        "Neither identifies a physical mode before constraint reduction."
    ),
    "BENCHMARK": (
        "The F_min direct Hessian must match w2_34 after the L_F=-M_*^4 F sign. "
        "Adding C^A C_A must change the direct quadratic rank but remains unselected."
    ),
    "CLOSURE_FLAGS": frozen_closure_flags(),
    "CROSSCHECK": (
        "The imported w2_34 Hessian is checked against the independently expanded "
        "velocity-bearing F_min subpart; w2_35 supplies the upstream integrity chain."
    ),
    "PROVENANCE": {"date": "2026-07-23", "data": "none", "code_version": "w2_36 v2.1"},
    "FILES": ["RefG/work 2/w2_36_strong_coupling_eft_gate.py"],
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def _sha(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()


EXPECTED_CONTRACT_SHA256 = "A59F75F22715AFDA1C4AAEFE74950C78DFE8503E94D1C229736642B45AA5AF72"
EXPECTED_OUTCOMES_SHA256 = "3710B602FB2320DCCADD7456DF9C1B62562009DA9CC8DA5ECC93364BD88228D0"
EXPECTED_UPSTREAM_PIN_SHA256 = "484109A06D62489EDD33CAB0195CF04722F584103761A09BDE5542AE8499E99C"


def _load_module(filename: str, tag: str) -> ModuleType:
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(tag, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def load_w35_and_report() -> dict[str, Any]:
    module = _load_module(
        "w2_35_exponential_exterior_coupled_symbol_gate.py", "w2_35_for_w2_36",
    )
    report = module.run()
    return {"module": module, "report": report}


def upstream_integrity_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    loaded = load_w35_and_report()
    w35, report = loaded["module"], loaded["report"]
    upstream = report.get("upstream_controls", {})
    upstream_loaded = w35.load_upstream_reports()
    w34 = upstream_loaded["modules"]["w2_34"]
    r34 = upstream_loaded["reports"]["w2_34"]
    controls = {
        "w2_35_code_imported_valid_and_self_pinned": all((
            w35.CLAIM_ID == UPSTREAM_PIN_SPEC["claim_id"],
            w35.MODEL_VERSION == UPSTREAM_PIN_SPEC["model_version"],
            w35.EXPECTED_CONTRACT_SHA256
            == UPSTREAM_PIN_SPEC["scientific_contract_sha256"],
            w35.EXPECTED_OUTCOMES_SHA256 == UPSTREAM_PIN_SPEC["outcomes_sha256"],
            w35.EXPECTED_UPSTREAM_PIN_SHA256
            == UPSTREAM_PIN_SPEC["upstream_pin_sha256"],
            report.get("valid") is True,
            report.get("artifact") == UPSTREAM_PIN_SPEC["claim_id"],
            report.get("model_version") == UPSTREAM_PIN_SPEC["model_version"],
            report.get("hashes", {}).get("scientific_contract")
            == UPSTREAM_PIN_SPEC["scientific_contract_sha256"],
            report.get("hashes", {}).get("outcomes")
            == UPSTREAM_PIN_SPEC["outcomes_sha256"],
        )),
        "w2_32_through_w2_34_integrity_enforced_transitively": all((
            bool(upstream),
            all(type(item) is bool and item for item in upstream.values()),
            report.get("decision", {}).get("physical_verdict_open") is True,
            report.get("decision", {}).get("physical_health_proved") is False,
            report.get("decision", {}).get("physical_failure_proved") is False,
        )),
        "w2_34_unreduced_Fmin_hessian_report_consumed": all((
            r34.get("valid") is True,
            r34.get("artifact") == w34.CLAIM_ID,
            r34.get("model_version") == w34.MODEL_VERSION,
            r34.get("outcomes", {}).get(
                "Fmin_cubic_material_velocity_hessian_polynomial_nontrivial_for_c_nonzero"
            ) is True,
            r34.get("outcomes", {}).get(
                "reduced_physical_spectrum_or_DOF_health_proved"
            ) is False,
            r34.get("hash_controls", {}).get("all_scientific_hashes_pinned") is True,
        )),
        "upstream_physical_verdict_remains_open": all((
            report["outcomes"]["full_constraint_reduced_exterior_symbol_derived"] is False,
            report["outcomes"]["constraint_or_gauge_removal_of_null_directions_excluded"] is False,
            report["outcomes"]["physical_strong_coupling_or_instability_proved"] is False,
            report["outcomes"]["physical_dynamic_health_proved"] is False,
        )),
    }
    diagnostics = {
        "w2_35_status": report.get("status"),
        "w2_35_hashes": report.get("hashes"),
        "w2_32_through_w2_34": report.get("upstream_diagnostics"),
    }
    return controls, diagnostics


def exact_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    eps = sp.symbols("epsilon", real=True)
    c = sp.symbols("c", nonzero=True, real=True)
    M4 = sp.symbols("M_star4", positive=True, real=True)
    delta, lower = sp.symbols("delta lambda_lower", positive=True, real=True)
    q1, q2, det_e1 = sp.symbols("Q_1 Q_2 det_E1", real=True)
    v_symbols = sp.symbols("v_1:4", real=True)
    v = sp.Matrix(v_symbols)
    v_sq = sp.expand(v.dot(v))

    # Q=epsilon*Q1+epsilon^2*(Q2-v^2).  The 16 det(E) contribution begins
    # as 16 epsilon^3 det(E1) and contains no material velocity at this order.
    q_scaled = eps * q1 + eps**2 * (q2 - v_sq)
    fmin_scaled = sp.expand(c * (q_scaled**2 + 16 * eps**3 * det_e1))
    lag_scaled = sp.expand(-M4 * fmin_scaled)
    quadratic = lag_scaled.coeff(eps, 2)
    cubic = lag_scaled.coeff(eps, 3)
    expected_quadratic = -M4 * c * q1**2
    expected_cubic = sp.expand(
        2 * M4 * c * q1 * v_sq - 2 * M4 * c * q1 * q2 - 16 * M4 * c * det_e1
    )
    velocity_bearing_cubic = sp.expand(cubic - cubic.subs({item: 0 for item in v_symbols}))
    expected_velocity_bearing = 2 * M4 * c * q1 * v_sq
    direct_hessian = sp.hessian(velocity_bearing_cubic, v_symbols)
    expected_direct_hessian = 4 * M4 * c * q1 * sp.eye(3)
    silent_hessian = direct_hessian.subs(q1, 0)
    plus_hessian = direct_hessian.subs(q1, delta)
    minus_hessian = direct_hessian.subs(q1, -delta)
    plus_coefficient = 4 * M4 * c * delta
    minus_coefficient = -4 * M4 * c * delta

    # Consume w2_35's independently differentiated silent material Hessian.
    # Its Rayleigh quotient, rather than a hand-entered zero, is the continuity
    # counterexample to a strictly positive direct lower bound.
    loaded = load_w35_and_report()
    w35 = loaded["module"]
    _, w35_exact_diagnostics = w35.exact_controls()
    imported_silent_hessian = w35_exact_diagnostics[
        "silent_material_velocity_hessian"
    ]
    unit_vector = sp.Matrix([1, 0, 0])
    silent_rayleigh_quotient = sp.simplify(
        (unit_vector.T * imported_silent_hessian * unit_vector)[0]
    )
    lower_bound_contradiction = sp.simplify(silent_rayleigh_quotient < lower)

    lam = sp.symbols("lambda_C", nonzero=True, real=True)
    completion_lagrangian = lam * v_sq
    completion_hessian = sp.hessian(completion_lagrangian, v_symbols)

    # Consume w2_34's exact symbolic F-Hessian and compare it after the
    # L_F=-M_*^4 F sign.  Here Q1 is the imported y1+Tr(E1), not a fitted map.
    upstream_loaded = w35.load_upstream_reports()
    w34 = upstream_loaded["modules"]["w2_34"]
    w34_audit = w34.exact_audit()
    w34_compact = w34_audit["compact_results"]
    w34_linear = w34_compact["linear_invariants"]
    w34_q1 = sp.expand(w34_linear["y1"] + w34_linear["trace_E1"])
    w34_c = w34_audit["symbols"]["c"]
    w34_F_hessian = w34_compact["leading_cubic_material_velocity_hessian_Fmin"]
    local_hessian_on_w34_symbols = direct_hessian.subs({c: w34_c, q1: w34_q1})
    imported_w34_L_hessian = -M4 * w34_F_hessian

    controls = {
        "Fmin_full_quadratic_coefficient_in_unreduced_bookkeeping_exact": (
            sp.simplify(quadratic - expected_quadratic) == 0
        ),
        "Fmin_full_cubic_coefficient_with_abstract_nonvelocity_terms_exact": (
            sp.simplify(cubic - expected_cubic) == 0
        ),
        "Fmin_velocity_bearing_cubic_subpart_exact": (
            sp.simplify(velocity_bearing_cubic - expected_velocity_bearing) == 0
        ),
        "Fmin_direct_cubic_velocity_hessian_exact": all((
            direct_hessian == expected_direct_hessian,
            sp.simplify(
                local_hessian_on_w34_symbols - imported_w34_L_hessian
            ) == sp.zeros(3),
        )),
        "silent_direct_material_velocity_hessian_zero": silent_hessian == sp.zeros(3),
        "opposite_offshell_deformations_reverse_direct_Fmin_hessian": (
            sp.simplify(plus_hessian + minus_hessian) == sp.zeros(3)
        ),
        "opposite_direct_coefficients_have_opposite_sign_for_c_nonzero": (
            (sp.simplify(plus_coefficient * minus_coefficient) < 0) is sp.true
        ),
        "generic_continuity_excludes_positive_direct_lower_bound_at_silent_point": (
            imported_silent_hessian == sp.zeros(3)
            and lower_bound_contradiction is sp.true
        ),
        "excluded_C2_operator_changes_direct_velocity_rank": all((
            completion_hessian == 2 * lam * sp.eye(3),
            completion_hessian.det() == 8 * lam**3,
        )),
    }
    diagnostics = {
        "Fmin_scaled_normal_form_through_cubic": fmin_scaled,
        "full_quadratic_lagrangian_coefficient": quadratic,
        "full_cubic_lagrangian_coefficient": cubic,
        "velocity_bearing_cubic_subpart": velocity_bearing_cubic,
        "direct_cubic_material_velocity_hessian": direct_hessian,
        "w2_34_imported_Fmin_F_hessian": w34_F_hessian,
        "w2_34_imported_Fmin_L_hessian": imported_w34_L_hessian,
        "silent_direct_hessian": silent_hessian,
        "plus_offshell_direct_hessian": plus_hessian,
        "minus_offshell_direct_hessian": minus_hessian,
        "generic_continuity_counterexample_point": {
            "w2_35_imported_silent_hessian": imported_silent_hessian,
            "silent_rayleigh_quotient": silent_rayleigh_quotient,
            "claimed_positive_lower_bound": lower,
        },
        "excluded_C2_completion_hessian": completion_hessian,
    }
    return controls, diagnostics


def _strict_bool_map(value: Any, keys: frozenset[str]) -> bool:
    return isinstance(value, dict) and set(value) == set(keys) and all(
        type(item) is bool for item in value.values()
    )


def warning_decision(
    evidence: dict[str, bool],
    upstream: dict[str, bool],
    *,
    constraint_reduction_complete: bool,
    reduced_classification_complete: bool,
    reduced_EFT_health_evidence: bool,
    reduced_EFT_failure_evidence: bool,
    numerical_cutoff_evidence: bool,
) -> dict[str, bool]:
    exact = _strict_bool_map(evidence, EVIDENCE_KEYS) and all(evidence.values())
    upstream_ok = _strict_bool_map(upstream, UPSTREAM_KEYS) and all(upstream.values())
    warning = bool(exact and upstream_ok)
    constraint_open = bool(warning and not constraint_reduction_complete)
    classification_complete = bool(
        warning and constraint_reduction_complete and reduced_classification_complete
    )
    physical_health = bool(
        classification_complete
        and reduced_EFT_health_evidence
        and not reduced_EFT_failure_evidence
    )
    physical_failure = bool(
        classification_complete
        and reduced_EFT_failure_evidence
        and not reduced_EFT_health_evidence
    )
    verdict_open = bool(warning and not physical_health and not physical_failure)
    return {
        "necessary_direct_block_warning": warning,
        "constraint_or_gauge_removal_open": constraint_open,
        "promotion_not_authorized": bool(warning and not physical_health),
        "physical_verdict_open": verdict_open,
        "physical_EFT_health_proved": physical_health,
        "physical_EFT_failure_proved": physical_failure,
        "numerical_cutoff_derived": bool(
            classification_complete and numerical_cutoff_evidence
        ),
    }


def definition_controls() -> dict[str, bool]:
    changed_contract = deepcopy(CLAIM_CONTRACT)
    changed_contract["BRANCHES"]["reduced_physical_EFT_verdict"] = "FAIL"
    changed_outcomes = deepcopy(EXPECTED_OUTCOMES)
    changed_outcomes["generic_silent_response_sign_flip_proved"] = True
    promoted_outcomes = deepcopy(EXPECTED_OUTCOMES)
    promoted_outcomes["physical_strong_coupling_or_EFT_failure_proved"] = True
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
        "hashes_exact": all((
            _sha(CLAIM_CONTRACT) == EXPECTED_CONTRACT_SHA256,
            _sha(EXPECTED_OUTCOMES) == EXPECTED_OUTCOMES_SHA256,
        )),
        "upstream_pin_hash_exact": (
            _sha(UPSTREAM_PIN_SPEC) == EXPECTED_UPSTREAM_PIN_SHA256
        ),
        "generic_sign_flip_explicitly_not_claimed": (
            EXPECTED_OUTCOMES["generic_silent_response_sign_flip_proved"] is False
        ),
        "physical_failure_explicitly_not_claimed": all((
            EXPECTED_OUTCOMES["physical_strong_coupling_or_EFT_failure_proved"] is False,
            EXPECTED_OUTCOMES["physical_verdict_closed"] is False,
            CLAIM_CONTRACT["BRANCHES"]["reduced_physical_EFT_verdict"] == "OPEN",
        )),
        "overclaim_mutations_detected": all((
            _sha(changed_contract) != EXPECTED_CONTRACT_SHA256,
            _sha(changed_outcomes) != EXPECTED_OUTCOMES_SHA256,
            _sha(promoted_outcomes) != EXPECTED_OUTCOMES_SHA256,
        )),
    }


def mutation_controls(
    evidence: dict[str, bool], upstream: dict[str, bool], decision: dict[str, bool],
) -> dict[str, bool]:
    missing = dict(evidence)
    missing.pop(next(iter(EVIDENCE_KEYS)))
    upstream_false = dict(upstream)
    upstream_false[next(iter(upstream_false))] = False
    unresolved_failure_assertion = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=False,
        reduced_classification_complete=False,
        reduced_EFT_health_evidence=False,
        reduced_EFT_failure_evidence=True,
        numerical_cutoff_evidence=True,
    )
    resolved_healthy = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=True,
        reduced_classification_complete=True,
        reduced_EFT_health_evidence=True,
        reduced_EFT_failure_evidence=False,
        numerical_cutoff_evidence=True,
    )
    resolved_failure_without_cutoff = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=True,
        reduced_classification_complete=True,
        reduced_EFT_health_evidence=False,
        reduced_EFT_failure_evidence=True,
        numerical_cutoff_evidence=False,
    )
    resolved_failure_with_cutoff = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=True,
        reduced_classification_complete=True,
        reduced_EFT_health_evidence=False,
        reduced_EFT_failure_evidence=True,
        numerical_cutoff_evidence=True,
    )
    classified_without_evidence = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=True,
        reduced_classification_complete=True,
        reduced_EFT_health_evidence=False,
        reduced_EFT_failure_evidence=False,
        numerical_cutoff_evidence=False,
    )
    contradictory_evidence = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=True,
        reduced_classification_complete=True,
        reduced_EFT_health_evidence=True,
        reduced_EFT_failure_evidence=True,
        numerical_cutoff_evidence=False,
    )
    return {
        "each_single_false_evidence_item_blocks_warning": all(
            not all({**evidence, key: False}.values()) for key in EVIDENCE_KEYS
        ),
        "missing_extra_nonboolean_evidence_rejected": all((
            not _strict_bool_map(missing, EVIDENCE_KEYS),
            not _strict_bool_map({**evidence, "extra": True}, EVIDENCE_KEYS),
            not _strict_bool_map({**evidence, next(iter(EVIDENCE_KEYS)): 1}, EVIDENCE_KEYS),
        )),
        "upstream_invalidity_blocks_chain": all((
            not all(upstream_false.values()),
            warning_decision(
                evidence,
                upstream_false,
                constraint_reduction_complete=False,
                reduced_classification_complete=False,
                reduced_EFT_health_evidence=False,
                reduced_EFT_failure_evidence=False,
                numerical_cutoff_evidence=False,
            )["necessary_direct_block_warning"] is False,
        )),
        "unreduced_failure_and_cutoff_assertions_are_not_conclusions": all((
            unresolved_failure_assertion["physical_EFT_failure_proved"] is False,
            unresolved_failure_assertion["numerical_cutoff_derived"] is False,
        )),
        "positive_health_evidence_can_resolve_without_failure": all((
            resolved_healthy["promotion_not_authorized"] is False,
            resolved_healthy["physical_verdict_open"] is False,
            resolved_healthy["physical_EFT_health_proved"] is True,
            resolved_healthy["physical_EFT_failure_proved"] is False,
            resolved_healthy["numerical_cutoff_derived"] is True,
        )),
        "failure_and_cutoff_require_their_own_reduced_evidence": all((
            decision["physical_EFT_failure_proved"] is False,
            decision["numerical_cutoff_derived"] is False,
            resolved_failure_without_cutoff["physical_EFT_failure_proved"] is True,
            resolved_failure_without_cutoff["numerical_cutoff_derived"] is False,
            resolved_failure_with_cutoff["numerical_cutoff_derived"] is True,
        )),
        "classification_without_positive_evidence_remains_open": all((
            classified_without_evidence["promotion_not_authorized"] is True,
            classified_without_evidence["physical_verdict_open"] is True,
            classified_without_evidence["physical_EFT_health_proved"] is False,
            classified_without_evidence["physical_EFT_failure_proved"] is False,
        )),
        "contradictory_health_and_failure_promotes_neither": all((
            contradictory_evidence["promotion_not_authorized"] is True,
            contradictory_evidence["physical_verdict_open"] is True,
            contradictory_evidence["physical_EFT_health_proved"] is False,
            contradictory_evidence["physical_EFT_failure_proved"] is False,
        )),
    }


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, sp.MatrixBase):
        return [[_json_safe(item) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(sp.simplify(value))
    return value


def run() -> dict[str, Any]:
    upstream, upstream_diagnostics = upstream_integrity_controls()
    evidence, diagnostics = exact_controls()
    definition = definition_controls()
    decision = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=False,
        reduced_classification_complete=False,
        reduced_EFT_health_evidence=False,
        reduced_EFT_failure_evidence=False,
        numerical_cutoff_evidence=False,
    )
    mutations = mutation_controls(evidence, upstream, decision)
    valid = bool(
        _strict_bool_map(evidence, EVIDENCE_KEYS)
        and all(evidence.values())
        and _strict_bool_map(upstream, UPSTREAM_KEYS)
        and all(upstream.values())
        and all(definition.values())
        and all(mutations.values())
        and _strict_bool_map(decision, DECISION_KEYS)
        and decision == {
            "necessary_direct_block_warning": True,
            "constraint_or_gauge_removal_open": True,
            "promotion_not_authorized": True,
            "physical_verdict_open": True,
            "physical_EFT_health_proved": False,
            "physical_EFT_failure_proved": False,
            "numerical_cutoff_derived": False,
        }
    )
    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": valid,
        "status": (
            "PASS_EXACT_DIRECT_BLOCK_EFT_DIAGNOSTIC__NECESSARY_WARNING__"
            "PROMOTION_NOT_AUTHORIZED__PHYSICAL_VERDICT_OPEN__NO_CUTOFF_CLAIM"
            if valid else "INVALID_AUDIT_NO_ADJUDICATION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "outcomes": frozen_outcomes(),
        "closure_flags": frozen_closure_flags(),
        "decision": decision,
        "evidence": evidence,
        "upstream_controls": upstream,
        "upstream_diagnostics": upstream_diagnostics,
        "controls": {"definition": definition, "mutation": mutations},
        "diagnostics": _json_safe(diagnostics),
        "hashes": {
            "scientific_contract": _sha(CLAIM_CONTRACT),
            "outcomes": _sha(EXPECTED_OUTCOMES),
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
            "status": "INVALID_AUDIT_NO_ADJUDICATION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(_json_safe(report), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
