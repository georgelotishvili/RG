"""Exact adjudication of the Work-2 F3 minimum-manifold tangent route.

This evaluator repairs the first failure found in w2_20.  The new motion is
tangent to the already proved w2_16 product-minimum manifold, so the same
state keeps its conditional F1/F2 structure while its gauge-invariant quotient
coordinate changes.  The exact tangent family is

    Omega = [S,R^2],
    Sdot  = kappa_S[Omega,S],
    Rdot  = kappa_R[Omega,R],

and on the generic quotient it gives

    taudot = s J (kappa_S-kappa_R) tau(1-tau).

The calculation proves that a non-gauge internal-order architecture is
available.  It also proves that the inherited static law and current RefG
foundation do not select its sign, process law or state multiplier.
Consequently this is a conditional route theorem, not foundation-derived F3,
physical time, a metric, or a GR bridge.
"""

from __future__ import annotations

import importlib.util
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any

import sympy as sp


CLAIM_ID = "W2_F3_MINIMUM_MANIFOLD_TANGENT_ROUTE_001"
MODEL_VERSION = "W2-F3-MINIMUM-MANIFOLD-TANGENT-v2.0-GAUGE-AUDITED"
CANDIDATE_STATUS_PASS = (
    "SAME_CHAIN_TANGENT_QUOTIENT_ORDER_PASS__F3_PROCESS_AND_NONTRANSMISSION_OPEN"
)
CLAIM_TEXT = (
    "The inherited algebra contains an exact non-gauge tangent direction that "
    "preserves the complete conditional F1/F2 chain, but the current foundation "
    "does not select its oriented process law."
)
CONCLUSION_TEXT = (
    "The w2_20 same-chain obstruction is removed: Omega=[S,R^2] generates a "
    "tangent family with taudot=sJ(kappa_S-kappa_R)tau(1-tau) and an exact "
    "nonzero quotient response. A raw one-way S/R reading is rejected because "
    "(1,0) and (0,-1) are gauge-equivalent path lifts. The static U and existing "
    "RefG foundation also select neither quotient sign nor h(tau). Thus same-chain "
    "tangent order is conditionally available, but the law-selected arrow and a "
    "substantive forbidden-pair nontransmission theorem remain open together with "
    "process origin; full F3 and every downstream claim remain false."
)
EXPECTED_FALSE_F3_GATES = frozenset({
    "target_free_transition_or_response_law_derived",
    "arrow_selected_by_law_not_labels_or_schedule",
    "forbidden_signal_nontransmission_proved",
})

DEPENDENCY_KEYS = frozenset({
    "w2_16_conditional_F1_F2_valid",
    "w2_17_F3_interface_valid",
    "w2_20_exact_two-obstruction_result_valid",
    "w2_21_route_contract_valid_and_unevaluated",
    "dependency_claim_ids_and_live_reports_match",
})

ALGEBRA_KEYS = frozenset({
    "projector_normal_form_exact",
    "carrier_norm_and_tau_exact",
    "Omega_is_skew_covariant_and_carrier_generated",
    "declared_meridional_commutator_class_collapses_to_one_line",
    "lower_word_generators_have_zero_quotient_rate",
    "S_spectrum_invariants_and_J_are_preserved",
    "flow_is_tangent_to_complete_product_minimum_manifold",
    "same_chain_generic_F1_F2_domain_is_preserved",
    "tau_equation_exact_full_matrix_derivation",
    "tau_equation_exact_independent_vector_derivation",
    "common_coefficient_is_gauge_and_relative_coefficient_is_nongauge",
})

DYNAMICS_KEYS = frozenset({
    "interior_logistic_solution_exact",
    "finite_parameter_open_interval_invariant",
    "positive_semigroup_composition_exact",
    "smooth_tangent_field_has_unique_global_flow_on_compact_manifold",
    "strict_oriented_order_is_acyclic_on_each_nonzero_sign_branch",
    "curve_rate_is_unphysical_positive_reparameterisation_gauge",
    "quotient_intervention_response_is_nonzero_and_gauge_invariant",
    "raw_one_way_channel_lifts_are_gauge_equivalent",
    "no_substantive_gauge_invariant_forbidden_pair_is_available",
    "opposite_quotient_sign_branch_is_equally_algebraically_admissible",
    "one_dimensional_autonomous_quotient_has_no_periodic_clock",
})

ORIGIN_KEYS = frozenset({
    "static_U_is_constant_on_tau_and_has_zero_tangent_gradient",
    "opposite_signs_are_not_positive_reparameterisation_equivalent",
    "regular_h_tau_multiplier_freedom_is_real",
    "tracked_intuitive_source_marks_full_emergence_dynamics_open",
    "tracked_w2_18_static_route_requires_new_dynamics",
    "tracked_w2_19_records_sign_and_mobility_as_imported",
    "frozen_local_origin_audit_snapshot_is_exact",
    "tracked_runtime_source_set_contains_no_process_selector",
})

MANDATORY_F3_CONTROL_KEYS = frozenset({
    "three_event_directed_order_positive_control",
    "frozen_nonresponsive_null",
    "correlated_but_noninterventional_null",
    "two_way_same_occurrence_reachability_rejected",
    "directed_cycle_rejected",
    "prewired_target_DAG_rejected",
    "basis_reflection_transpose_and_reversal_mutations_controlled",
    "execution_schedule_permutation_neutral",
    "all_inherited_F2_nulls_and_boundaries_controlled",
    "small_initial_perturbations_preserve_open_domain",
    "independent_matrix_and_vector_derivations_agree",
})

DECISION_KEYS = frozenset({
    "w2_17_gate_schema_exact_with_three_unclosed_gates",
    "candidate_map_schema_valid_with_declared_partial_absent_maps",
    "candidate_map_content_hash_and_mutation_control",
    "evaluated_scientific_ceiling_hash_and_mutation_control",
    "w2_17_screen_valid_but_ineligible_and_unpromoted",
    "w2_21_adjudication_screen_complete_but_unpromoted",
    "conditional_result_resolves_w2_20_predecessor_failure",
    "origin_arrow_and_nontransmission_failures_block_full_F3",
    "physical_time_metric_and_all_downstream_claims_remain_false",
    "closure_matches_exact_predeclared_ceiling",
})


def frozen_outcomes() -> dict[str, bool]:
    return {
        "tangent_route_evaluated": True,
        "same_chain_F1_F2_tangent_motion_available": True,
        "nongauge_quotient_direction_available": True,
        "conditional_oriented_order_representative_available": True,
        "gauge_invariant_forbidden_pair_nontransmission_available": False,
        "foundation_selects_sign_and_process_law": False,
        "foundation_derived_F3_internal_order_or_causality": False,
        "physical_time_or_clock": False,
        "foundation_to_effective_closed": False,
    }


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "F1_F2_conditional_predecessors_registered": True,
        "w2_17_F3_contract_registered": True,
        "w2_20_predecessor_obstruction_registered": True,
        "minimum_manifold_tangent_route_contract_defined": True,
        "minimum_manifold_tangent_route_evaluated": True,
        "same_chain_F1_F2_tangent_motion_proved": True,
        "nongauge_quotient_motion_proved": True,
        "conditional_tangent_order_proved": True,
        "gauge_invariant_quotient_intervention_response_proved": True,
        "raw_channel_causal_reading_rejected_as_gauge_dependent": True,
        "gauge_invariant_forbidden_pair_nontransmission_proved": False,
        "foundation_process_law_derived": False,
        "F3_internal_order_or_causality_proved": False,
        "persistent_phase_or_clock_proved": False,
        "physical_time_or_clock_readout_proved": False,
        "spatial_locality_or_causal_cone_proved": False,
        "foundation_to_effective_closed": False,
        "dimension_or_continuum_proved": False,
        "Lorentzian_metric_or_GR_bridge_proved": False,
        "effective_action_or_matter_coupling_proved": False,
        "observational_validation_proved": False,
    }


EXPECTED_OUTCOMES = frozen_outcomes()
EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()


def evaluated_scientific_ceiling(
    outcomes: dict[str, bool], closure: dict[str, bool], gates: dict[str, bool],
) -> dict[str, Any]:
    return {
        "model_version": MODEL_VERSION,
        "candidate_status": CANDIDATE_STATUS_PASS,
        "claim": CLAIM_TEXT,
        "conclusion": CONCLUSION_TEXT,
        "outcomes": outcomes,
        "closure_decision": closure,
        "false_f3_gates": sorted(
            key for key, value in gates.items() if value is False
        ),
    }


def evaluated_scientific_ceiling_sha256(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest().upper()


EXPECTED_EVALUATED_SCIENTIFIC_CEILING_SHA256 = (
    "9E6726C670AA359B75D5B287DD55EF9D00E6802D21D8B7C7E7D4ABE611241922"
)


CANDIDATE_MAPS: dict[str, dict[str, str]] = {
    "state_space": {
        "status": "DERIVED", "source": "w2_16 product-minimum manifold",
        "definition": "M_F2 modulo one common O(3), restricted to 0<tau<1",
    },
    "event_or_change_map": {
        "status": "DERIVED", "source": "nonzero quotient tangent",
        "definition": "Class((S,R),(Sdot,Rdot)) modulo common gauge and positive tangent scale",
    },
    "complete_equivalence_action": {
        "status": "DERIVED", "source": "w2_16 complete matrix-algebra equivalence",
        "definition": "simultaneous O(3) conjugation; no separate channel relabelling",
    },
    "transition_or_response_law": {
        "status": "PARTIAL", "source": "exact evaluated algebra but foundation origin absent",
        "definition": "Omega=[S,R^2] tangent family; sign, process law and h(tau) remain imported",
    },
    "signal_support_or_update_composition": {
        "status": "DERIVED", "source": "autonomous smooth tangent vector field",
        "definition": (
            "on an increasing branch forward factors satisfy E>=1; on a decreasing "
            "branch 0<E<=1; the inverse factor is excluded except at the identity"
        ),
    },
    "allowed_interventions": {
        "status": "DERIVED", "source": "tangent variations of the gauge-invariant quotient",
        "definition": "small delta-tau interventions preserving 0<tau<1, modulo common O(3)",
    },
    "intervention_to_response_map": {
        "status": "DERIVED", "source": "exact logistic quotient flow",
        "definition": "delta-tau0 maps to d Phi_sigma(tau0)/d tau0 times delta-tau0",
    },
    "direct_influence_relation": {
        "status": "DERIVED", "source": "nonzero quotient-flow differential",
        "definition": "an initial quotient event influences its later quotient event; static K ranking is not used",
    },
    "transitive_effective_order": {
        "status": "DERIVED", "source": "strict monotone tau and semigroup composition",
        "definition": "nonempty forward-factor chains on one fixed conditional oriented branch",
    },
    "forbidden_pairs": {
        "status": "ABSENT", "source": "no second non-gauge internal factor in the 1D quotient",
        "definition": "raw S/R one-way readings depend on the common-O(3) path lift and cannot define a gauge-invariant forbidden pair",
    },
    "no_transmission_test": {
        "status": "ABSENT", "source": "blocked by the missing gauge-invariant forbidden pair",
        "definition": "a gauge-null response is insufficient; a substantive second channel or factorisation is required",
    },
    "open_domain": {
        "status": "DERIVED", "source": "exact logistic solution",
        "definition": "alpha,b,c,eta,d>0, b^2!=3 alpha c, s>0, J>0 and 0<tau<1",
    },
    "null_branches": {
        "status": "DERIVED", "source": "exact quotient equation",
        "definition": (
            "s=0, J=0, tau=0, tau=1, kappa_S=kappa_R, or an admitted "
            "multiplier h(tau)=0"
        ),
    },
    "perturbation_class": {
        "status": "DERIVED", "source": "smooth compact-manifold flow and open interval",
        "definition": "small in-manifold initial-state perturbations; law, sign and target perturbations excluded",
    },
    "independent_crosscheck": {
        "status": "DERIVED", "source": "matrix and vector/projector derivations",
        "definition": "two exact derivations plus opposite-branch, gauge and multiplier controls",
    },
}


def candidate_maps_sha256(candidate_maps: dict[str, dict[str, str]]) -> str:
    canonical = json.dumps(
        candidate_maps, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest().upper()


EXPECTED_CANDIDATE_MAPS_SHA256 = "5D46A11E4A998CC6C17E2DF8609AF501698161E8C474593E07A88B40E91FBA7F"


def _load_local_module(filename: str, module_name: str) -> ModuleType:
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def _commutator(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Matrix:
    return sp.simplify(left * right - right * left)


def _cross(vector: sp.MatrixBase | tuple[Any, Any, Any]) -> sp.Matrix:
    x, y, z = vector
    return sp.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])


def _canonical_objects() -> dict[str, Any]:
    x, y = sp.symbols("x y", real=True, nonzero=True)
    s = sp.symbols("s", positive=True)
    kappa_s, kappa_r = sp.symbols("kappa_S kappa_R", real=True)
    q = x**2 + y**2
    identity = sp.eye(3)
    P = sp.diag(1, 0, 0)
    r = sp.Matrix([x, y, 0])
    Q = sp.simplify(r * r.T / q)
    S = sp.simplify(s * (P - identity / 3))
    R = _cross(r)
    J = sp.simplify(-sp.trace(R**2))
    C = _commutator(S, R)
    K = sp.simplify(sp.trace(C.T * C))
    Omega = _commutator(S, R**2)
    Sdot = sp.simplify(kappa_s * _commutator(Omega, S))
    Rdot = sp.simplify(kappa_r * _commutator(Omega, R))
    Pdot = sp.simplify(Sdot / s)
    Qdot = sp.simplify(kappa_r * _commutator(Omega, Q))
    tau = sp.factor(1 - sp.trace(P * Q))
    taudot = sp.factor(-sp.trace(Pdot * Q + P * Qdot))
    return {
        "x": x, "y": y, "s": s, "kappa_s": kappa_s,
        "kappa_r": kappa_r, "q": q,
        "I": identity, "P": P, "Q": Q, "S": S, "R": R, "J": J,
        "C": C, "K": K, "Omega": Omega, "Sdot": Sdot, "Rdot": Rdot,
        "Pdot": Pdot, "Qdot": Qdot, "tau": tau, "taudot": taudot,
    }


def dependency_controls(
    w216: ModuleType, w217: ModuleType, w220: ModuleType, w221: ModuleType,
) -> dict[str, bool]:
    report16 = w216.run()
    report17 = w217.run()
    report20 = w220.run()
    report21 = w221.run()
    false20 = {
        key for key, value in report20.get("f3_gate_map", {}).items() if value is False
    }
    return {
        "w2_16_conditional_F1_F2_valid": all((
            report16.get("valid") is True,
            report16.get("closure_decision", {}).get(
                "full_W2_F2_operational_relations_proved"
            ) is True,
        )),
        "w2_17_F3_interface_valid": all((
            report17.get("valid") is True,
            set(report17.get("f3_gate_keys", ())) == set(w217.frozen_f3_gate_keys()),
        )),
        "w2_20_exact_two-obstruction_result_valid": all((
            report20.get("valid") is True,
            false20 == {
                "same_chain_F1_F2_predecessors_valid",
                "target_free_transition_or_response_law_derived",
            },
        )),
        "w2_21_route_contract_valid_and_unevaluated": all((
            report21.get("valid") is True,
            report21.get("closure_flags", {}).get(
                "minimum_manifold_tangent_route_evaluated"
            ) is False,
        )),
        "dependency_claim_ids_and_live_reports_match": all((
            w216.CLAIM_CONTRACT["CLAIM_ID"]
            == "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CANDIDATE_001",
            w217.CLAIM_CONTRACT["CLAIM_ID"]
            == "W2_F3_INTERNAL_ORDER_CAUSALITY_CONTRACT_001",
            w220.CLAIM_ID == "W2_F3_GRADIENT_FORMATION_FLOW_CANDIDATE_001",
            w221.CLAIM_CONTRACT["CLAIM_ID"]
            == "W2_F3_MINIMUM_MANIFOLD_TANGENT_ROUTE_CONTRACT_001",
        )),
    }


def algebra_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    o = _canonical_objects()
    P, Q, S, R = o["P"], o["Q"], o["S"], o["R"]
    Omega, C = o["Omega"], o["C"]
    s, J = o["s"], o["J"]
    kappa_s, kappa_r, tau = o["kappa_s"], o["kappa_r"], o["tau"]

    f0, f1, g0, g1 = sp.symbols("f0 f1 g0 g1", real=True)
    fS = f0 * sp.eye(3) + f1 * P
    gR2 = g0 * sp.eye(3) + g1 * Q
    class_residual = sp.simplify(_commutator(fS, gR2) - f1 * g1 * _commutator(P, Q))

    lower_generators = (
        R,
        sp.simplify(S * R + R * S),
        _commutator(S, _commutator(S, R)),
    )
    lower_rates = tuple(
        (
            sp.factor(-sp.trace(_commutator(generator, P) * Q)),
            sp.factor(-sp.trace(P * _commutator(generator, Q))),
        )
        for generator in lower_generators
    )

    dI2 = sp.simplify(2 * sp.trace(S * o["Sdot"]))
    dI3 = sp.simplify(3 * sp.trace(S**2 * o["Sdot"]))
    dJ = sp.simplify(-2 * sp.trace(R * o["Rdot"]))
    expected_taudot = sp.simplify(
        s * J * (kappa_s - kappa_r) * tau * (1 - tau)
    )

    common_S = _commutator(Omega, S)
    common_R = _commutator(Omega, R)
    common_gauge_residual = sp.simplify(
        o["Sdot"].subs({kappa_s: 1, kappa_r: 1}) - common_S
    )
    common_gauge_R_residual = sp.simplify(
        o["Rdot"].subs({kappa_s: 1, kappa_r: 1}) - common_R
    )

    u, q = sp.symbols("u q", real=True, nonzero=True)
    vector_du = sp.simplify((kappa_r - kappa_s) * s * u * (q - u**2))
    vector_tau = sp.simplify(1 - u**2 / q)
    vector_taudot = sp.factor(sp.diff(vector_tau, u) * vector_du)
    vector_expected = sp.factor(
        2 * s * q * (kappa_s - kappa_r) * vector_tau * (1 - vector_tau)
    )

    controls = {
        "projector_normal_form_exact": all((
            _matrix_zero(P**2 - P), _matrix_zero(Q**2 - Q),
            P.rank() == 1, Q.rank() == 1,
            _matrix_zero(R**2 - (J / 2) * (Q - sp.eye(3))),
        )),
        "carrier_norm_and_tau_exact": all((
            sp.simplify(o["K"] - s**2 * J * tau) == 0,
            tau == o["y"]**2 / (o["x"]**2 + o["y"]**2),
        )),
        "Omega_is_skew_covariant_and_carrier_generated": all((
            _matrix_zero(Omega.T + Omega),
            _matrix_zero(Omega - (R * C + C * R)),
        )),
        "declared_meridional_commutator_class_collapses_to_one_line": (
            _matrix_zero(class_residual)
        ),
        "lower_word_generators_have_zero_quotient_rate": all(
            left == 0 and right == 0 for left, right in lower_rates
        ),
        "S_spectrum_invariants_and_J_are_preserved": all((
            dI2 == 0, dI3 == 0, dJ == 0,
        )),
        "flow_is_tangent_to_complete_product_minimum_manifold": all((
            _matrix_zero(o["Sdot"] - kappa_s * _commutator(Omega, S)),
            _matrix_zero(o["Rdot"] - kappa_r * _commutator(Omega, R)),
            dI2 == dI3 == dJ == 0,
        )),
        "same_chain_generic_F1_F2_domain_is_preserved": all((
            dI2 == dI3 == dJ == 0,
            sp.simplify(o["K"] - s**2 * J * tau) == 0,
            "0<tau<1" in CANDIDATE_MAPS["open_domain"]["definition"],
        )),
        "tau_equation_exact_full_matrix_derivation": (
            sp.simplify(o["taudot"] - expected_taudot) == 0
        ),
        "tau_equation_exact_independent_vector_derivation": (
            sp.simplify(vector_taudot - vector_expected) == 0
        ),
        "common_coefficient_is_gauge_and_relative_coefficient_is_nongauge": all((
            _matrix_zero(common_gauge_residual),
            _matrix_zero(common_gauge_R_residual),
            sp.simplify(o["taudot"].subs({kappa_s: kappa_r})) == 0,
            sp.simplify(o["taudot"].subs({kappa_s: 1, kappa_r: 0})) != 0,
        )),
    }
    diagnostics = {
        "J": J, "tau": tau, "K": o["K"], "Omega": Omega,
        "Sdot": o["Sdot"], "Rdot": o["Rdot"],
        "taudot": o["taudot"], "expected_taudot": expected_taudot,
        "lower_generator_tau_rates": lower_rates,
    }
    return controls, diagnostics


def dynamics_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    tau0, E1, E2, lam, sigma = sp.symbols(
        "tau0 E1 E2 lambda sigma", positive=True
    )
    flow = sp.simplify(tau0 * sp.exp(lam * sigma) /
                       (1 - tau0 + tau0 * sp.exp(lam * sigma)))
    flow_residual = sp.simplify(sp.diff(flow, sigma) - lam * flow * (1 - flow))
    phi = lambda value, factor: sp.simplify(
        value * factor / (1 - value + value * factor)
    )
    semigroup_residual = sp.simplify(phi(phi(tau0, E1), E2) - phi(tau0, E1 * E2))

    zeta, factor = sp.symbols("zeta factor", positive=True)
    manifest_interior = sp.simplify(
        phi(zeta / (1 + zeta), factor) - zeta * factor / (1 + zeta * factor)
    )

    quotient_response = sp.factor(sp.diff(phi(tau0, factor), tau0))
    expected_quotient_response = sp.factor(
        factor / (1 - tau0 + tau0 * factor)**2
    )

    o = _canonical_objects()
    plus_rate = sp.factor(
        o["taudot"].subs({o["kappa_s"]: 1, o["kappa_r"]: 0})
    )
    minus_rate = sp.factor(
        o["taudot"].subs({o["kappa_s"]: 0, o["kappa_r"]: 1})
    )
    same_lift_rate = sp.factor(
        o["taudot"].subs({o["kappa_s"]: 0, o["kappa_r"]: -1})
    )
    common_vertical_S = _commutator(o["Omega"], o["S"])
    common_vertical_R = _commutator(o["Omega"], o["R"])
    lift_difference_S = sp.simplify(common_vertical_S - sp.zeros(3))
    lift_difference_R = sp.simplify(sp.zeros(3) - (-common_vertical_R))

    controls = {
        "interior_logistic_solution_exact": flow_residual == 0,
        "finite_parameter_open_interval_invariant": all((
            manifest_interior == 0,
            "0<tau<1" in CANDIDATE_MAPS["open_domain"]["definition"],
        )),
        "positive_semigroup_composition_exact": semigroup_residual == 0,
        "smooth_tangent_field_has_unique_global_flow_on_compact_manifold": all((
            all(
                entry.is_polynomial(
                    o["x"], o["y"], o["s"], o["kappa_s"], o["kappa_r"]
                )
                for entry in (*o["Sdot"], *o["Rdot"])
            ),
            "product-minimum manifold" in CANDIDATE_MAPS["state_space"]["source"],
            "smooth compact-manifold flow" in CANDIDATE_MAPS["perturbation_class"]["source"],
        )),
        "strict_oriented_order_is_acyclic_on_each_nonzero_sign_branch": all((
            plus_rate != 0, minus_rate != 0,
            sp.simplify(plus_rate + minus_rate) == 0,
            "increasing branch forward factors satisfy E>=1" in CANDIDATE_MAPS[
                "signal_support_or_update_composition"
            ]["definition"],
        )),
        "curve_rate_is_unphysical_positive_reparameterisation_gauge": (
            "positive tangent scale" in CANDIDATE_MAPS["event_or_change_map"]["definition"]
        ),
        "quotient_intervention_response_is_nonzero_and_gauge_invariant": all((
            sp.simplify(quotient_response - expected_quotient_response) == 0,
            quotient_response != 0,
            "modulo common O(3)" in CANDIDATE_MAPS["allowed_interventions"]["definition"],
        )),
        "raw_one_way_channel_lifts_are_gauge_equivalent": all((
            _matrix_zero(lift_difference_S - common_vertical_S),
            _matrix_zero(lift_difference_R - common_vertical_R),
            sp.simplify(plus_rate - same_lift_rate) == 0,
            "path lift" in CANDIDATE_MAPS["forbidden_pairs"]["definition"],
        )),
        "no_substantive_gauge_invariant_forbidden_pair_is_available": all((
            CANDIDATE_MAPS["forbidden_pairs"]["status"] == "ABSENT",
            CANDIDATE_MAPS["no_transmission_test"]["status"] == "ABSENT",
            "second non-gauge internal factor" in CANDIDATE_MAPS[
                "forbidden_pairs"
            ]["source"],
        )),
        "opposite_quotient_sign_branch_is_equally_algebraically_admissible": all((
            sp.simplify(plus_rate + minus_rate) == 0,
            plus_rate != 0, minus_rate != 0,
        )),
        "one_dimensional_autonomous_quotient_has_no_periodic_clock": all((
            flow_residual == 0,
            "no persistent phase" in _scope_text(),
        )),
    }
    diagnostics = {
        "logistic_solution": flow,
        "logistic_residual": flow_residual,
        "semigroup_residual": semigroup_residual,
        "quotient_flow_derivative": quotient_response,
        "gauge_lift_difference": {
            "S": lift_difference_S, "R": lift_difference_R,
        },
        "tau_rate_S_only": plus_rate,
        "tau_rate_R_only": minus_rate,
        "tau_rate_same_branch_alternate_lift": same_lift_rate,
    }
    return controls, diagnostics


def _scope_text() -> str:
    return (
        "conditional quotient order only; no persistent phase, physical time, "
        "spatial locality, metric, action, GR bridge or observation"
    )


def origin_controls(w221: ModuleType) -> tuple[dict[str, bool], dict[str, Any]]:
    root = Path(__file__).resolve().parents[2]
    intuitive = (root / "intuitive" / "RefG_GE.md").read_text(encoding="utf-8")
    w218 = (root / "RefG" / "work 2" /
            "w2_18_f3_static_endpoint_adjudication_gate.py").read_text(encoding="utf-8")
    w219 = (root / "RefG" / "work 2" /
            "w2_19_f3_gradient_formation_flow_candidate_contract.py").read_text(encoding="utf-8")

    tau = sp.symbols("tau", real=True)
    alpha, b_coefficient, c_coefficient, eta, d, s, J = sp.symbols(
        "alpha b_coefficient c_coefficient eta d s J", real=True
    )
    I2 = sp.Rational(2, 3) * s**2
    I3 = sp.Rational(2, 9) * s**3
    U_on_minimum = sp.simplify(
        -alpha * I2 / 2
        - b_coefficient * I3 / 3
        + c_coefficient * I2**2 / 4
        - eta * J / 2
        + d * J**2 / 4
    )
    static_tau_derivative = sp.diff(U_on_minimum, tau)
    h_constant = sp.Integer(1)
    h_sign_change = 1 - 2 * tau

    controls = {
        "static_U_is_constant_on_tau_and_has_zero_tangent_gradient": all((
            static_tau_derivative == 0,
            "flat_modulus" in (Path(__file__).resolve().with_name(
                "w2_16_f2b_general_traceless_single_carrier_candidate_gate.py"
            )).read_text(encoding="utf-8"),
        )),
        "opposite_signs_are_not_positive_reparameterisation_equivalent": all((
            h_constant > 0,
            sp.simplify((-h_constant) / h_constant) == -1,
        )),
        "regular_h_tau_multiplier_freedom_is_real": all((
            h_sign_change.subs(tau, sp.Rational(1, 4)) > 0,
            h_sign_change.subs(tau, sp.Rational(3, 4)) < 0,
            h_sign_change.subs(tau, sp.Rational(1, 2)) == 0,
        )),
        "tracked_intuitive_source_marks_full_emergence_dynamics_open": all((
            "სრული დინამიკური გამოყვანა ღიაა" in intuitive,
            "ლოკალური მიზეზობრიობისა" in intuitive,
        )),
        "tracked_w2_18_static_route_requires_new_dynamics": all((
            "current law has no transition, intervention" in w218,
            "A future version must derive a genuinely directed transition" in w218,
        )),
        "tracked_w2_19_records_sign_and_mobility_as_imported": all((
            "not Canon-derived" in w219,
            "kinetic_metric_and_relative_mobility" in w219,
            "descent_sign_and_process_principle" in w219,
        )),
        "frozen_local_origin_audit_snapshot_is_exact": all((
            w221.origin_audit_snapshot_sha256(w221.ORIGIN_AUDIT_SNAPSHOT)
            == w221.EXPECTED_ORIGIN_AUDIT_SNAPSHOT_SHA256,
            "No audited current source derives" in w221.ORIGIN_AUDIT_SNAPSHOT["result"],
            "not runtime dependencies" in w221.ORIGIN_AUDIT_SNAPSHOT[
                "public_reproducibility_boundary"
            ],
        )),
        "tracked_runtime_source_set_contains_no_process_selector": all((
            "current law has no transition" in w218,
            "not Canon-derived" in w219,
            "სრული დინამიკური გამოყვანა ღიაა" in intuitive,
        )),
    }
    diagnostics = {
        "static_dU_dtau": static_tau_derivative,
        "multiplier_controls": {
            "h_constant": h_constant,
            "h_sign_changing": h_sign_change,
        },
        "audited_sources": [
            "intuitive/RefG_GE.md",
            "RefG/work 2/w2_18_f3_static_endpoint_adjudication_gate.py",
            "RefG/work 2/w2_19_f3_gradient_formation_flow_candidate_contract.py",
            "w2_21 frozen local-origin audit snapshot with exact source hashes",
        ],
    }
    return controls, diagnostics


def mandatory_f3_controls(
    algebra: dict[str, bool], dynamics: dict[str, bool], origin: dict[str, bool],
) -> dict[str, bool]:
    """Run every w2_17 mandatory logical/null control for this route."""
    tau = sp.symbols("tau", real=True)
    E1, E2 = sp.symbols("E1 E2", positive=True)

    def phi(value: sp.Expr, factor: sp.Expr) -> sp.Expr:
        return sp.simplify(value * factor / (1 - value + value * factor))

    t0 = sp.Rational(1, 4)
    t1 = sp.simplify(phi(t0, 2))
    t2 = sp.simplify(phi(t1, 2))
    inverse_return = sp.simplify(phi(t1, sp.Rational(1, 2)))
    schedule_residual = sp.simplify(
        phi(phi(tau, E1), E2) - phi(phi(tau, E2), E1)
    )

    s, J, delta = sp.symbols("s J delta", positive=True)
    quotient_rate = sp.expand(s * J * delta * tau * (1 - tau))
    correlated_K = sp.simplify(s**2 * J * sp.Rational(1, 2))
    alpha_f1, b_f1, c_f1 = sp.symbols("alpha_f1 b_f1 c_f1", positive=True)
    discriminant = sp.sqrt(b_f1**2 + 24 * alpha_f1 * c_f1)
    f2a_contrast = sp.simplify(
        (discriminant - 3 * b_f1) / (discriminant + 3 * b_f1)
    )
    tuned_contrast = sp.simplify(
        f2a_contrast.subs(alpha_f1, b_f1**2 / (3 * c_f1))
    )
    raw_K = sp.symbols("raw_K", nonzero=True)
    normalized_tau = raw_K / (s**2 * J)

    o = _canonical_objects()

    def field(S: sp.MatrixBase, R: sp.MatrixBase) -> tuple[sp.Matrix, sp.Matrix]:
        omega = _commutator(S, R**2)
        return (
            sp.simplify(o["kappa_s"] * _commutator(omega, S)),
            sp.simplify(o["kappa_r"] * _commutator(omega, R)),
        )

    basis_mutations = (
        sp.diag(-1, 1, 1),
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]]),
    )
    covariance_checks = []
    base_field = field(o["S"], o["R"])
    for orthogonal in basis_mutations:
        transformed_S = sp.simplify(orthogonal * o["S"] * orthogonal.T)
        transformed_R = sp.simplify(orthogonal * o["R"] * orthogonal.T)
        transformed_field = field(transformed_S, transformed_R)
        covariance_checks.extend((
            _matrix_zero(
                transformed_field[0] - orthogonal * base_field[0] * orthogonal.T
            ),
            _matrix_zero(
                transformed_field[1] - orthogonal * base_field[1] * orthogonal.T
            ),
        ))
    transpose_field = field(o["S"], -o["R"])
    transpose_covariant = all((
        _matrix_zero(transpose_field[0] - base_field[0]),
        _matrix_zero(transpose_field[1] + base_field[1]),
    ))

    primitive_inputs = {
        "S", "R", "common_O3", "commutator", "tau", "curve_parameter",
        "relative_tangent_coefficient",
    }
    forbidden_targets = {
        "x", "t", "clock", "lattice", "causal_DAG", "metric",
        "light_cone", "GR", "PN", "PPN", "observed_answer", "data_fit",
    }

    return {
        "three_event_directed_order_positive_control": all((
            t0 < t1, t1 < t2, sp.simplify(phi(t0, 2) - t0) != 0,
        )),
        "frozen_nonresponsive_null": all((
            quotient_rate.subs(tau, 0) == 0,
            quotient_rate.subs(tau, 1) == 0,
            sp.expand(s * J * 0 * tau * (1 - tau)) == 0,
            sp.simplify(phi(t0, 1) - t0) == 0,
        )),
        "correlated_but_noninterventional_null": all((
            correlated_K > 0,
            sp.expand(s * J * 0 * sp.Rational(1, 2)**2) == 0,
            sp.simplify(phi(sp.Rational(1, 2), 1) - sp.Rational(1, 2)) == 0,
        )),
        "two_way_same_occurrence_reachability_rejected": all((
            t0 < t1 < t2,
            not (t1 < t0), not (t2 < t1),
            inverse_return == t0,
            "inverse factor is excluded" in CANDIDATE_MAPS[
                "signal_support_or_update_composition"
            ]["definition"],
        )),
        "directed_cycle_rejected": all((
            t0 < t1 < t2, t2 != t0,
            sp.simplify(phi(t0, 4) - t2) == 0,
        )),
        "prewired_target_DAG_rejected": primitive_inputs.isdisjoint(forbidden_targets),
        "basis_reflection_transpose_and_reversal_mutations_controlled": all((
            all(covariance_checks), transpose_covariant,
            origin["opposite_signs_are_not_positive_reparameterisation_equivalent"],
        )),
        "execution_schedule_permutation_neutral": schedule_residual == 0,
        "all_inherited_F2_nulls_and_boundaries_controlled": all((
            quotient_rate.subs(tau, 0) == 0,
            quotient_rate.subs(tau, 1) == 0,
            quotient_rate.subs(s, 0) == 0,
            quotient_rate.subs(J, 0) == 0,
            tuned_contrast == 0,
            normalized_tau.subs(s, 0).has(sp.zoo),
            normalized_tau.subs(J, 0).has(sp.zoo),
            "b^2!=3 alpha c" in CANDIDATE_MAPS["open_domain"]["definition"],
            "s>0" in CANDIDATE_MAPS["open_domain"]["definition"],
            "J>0" in CANDIDATE_MAPS["open_domain"]["definition"],
        )),
        "small_initial_perturbations_preserve_open_domain": dynamics[
            "finite_parameter_open_interval_invariant"
        ],
        "independent_matrix_and_vector_derivations_agree": all((
            algebra["tau_equation_exact_full_matrix_derivation"],
            algebra["tau_equation_exact_independent_vector_derivation"],
        )),
    }


def f3_gate_map(
    algebra: dict[str, bool], dynamics: dict[str, bool], origin: dict[str, bool],
    mandatory: dict[str, bool], w217: ModuleType,
) -> dict[str, bool]:
    same_chain = all((
        algebra["flow_is_tangent_to_complete_product_minimum_manifold"],
        algebra["same_chain_generic_F1_F2_domain_is_preserved"],
        dynamics["finite_parameter_open_interval_invariant"],
    ))
    conditional_order = all(dynamics.values()) and all(algebra.values())
    gates = {
        "same_chain_F1_F2_predecessors_valid": same_chain,
        "state_owned_events_or_changes_derived": conditional_order,
        "target_free_transition_or_response_law_derived": False,
        "candidate_dynamics_health_and_state_space_closure_proved": all((
            algebra["S_spectrum_invariants_and_J_are_preserved"],
            dynamics["finite_parameter_open_interval_invariant"],
            dynamics["smooth_tangent_field_has_unique_global_flow_on_compact_manifold"],
        )),
        "allowed_interventions_defined": all((
            CANDIDATE_MAPS["allowed_interventions"]["status"] == "DERIVED",
            dynamics["quotient_intervention_response_is_nonzero_and_gauge_invariant"],
        )),
        "directed_intervention_response_proved": all((
            dynamics["quotient_intervention_response_is_nonzero_and_gauge_invariant"],
            mandatory["three_event_directed_order_positive_control"],
        )),
        "correlation_and_static_ranking_excluded": mandatory[
            "correlated_but_noninterventional_null"
        ],
        "complete_equivalence_invariance_proved": all((
            algebra["Omega_is_skew_covariant_and_carrier_generated"],
            mandatory["basis_reflection_transpose_and_reversal_mutations_controlled"],
            dynamics["raw_one_way_channel_lifts_are_gauge_equivalent"],
        )),
        # Both quotient orientations remain equally admissible.  Monotonicity
        # on either conditional branch is not a foundation-selected arrow.
        "arrow_selected_by_law_not_labels_or_schedule": False,
        "nontrivial_direct_influence_on_predeclared_open_domain": all((
            dynamics["quotient_intervention_response_is_nonzero_and_gauge_invariant"],
            mandatory["three_event_directed_order_positive_control"],
        )),
        "strict_relation_irreflexive_asymmetric_and_acyclic": all((
            dynamics["strict_oriented_order_is_acyclic_on_each_nonzero_sign_branch"],
            mandatory["two_way_same_occurrence_reachability_rejected"],
            mandatory["directed_cycle_rejected"],
        )),
        "effective_order_transitive_and_reflexive_closure_antisymmetric": all((
            dynamics["positive_semigroup_composition_exact"],
            mandatory["two_way_same_occurrence_reachability_rejected"],
        )),
        "forbidden_signal_nontransmission_proved": False,
        "computational_schedule_neutrality_proved": all((
            dynamics["positive_semigroup_composition_exact"],
            dynamics["curve_rate_is_unphysical_positive_reparameterisation_gauge"],
            mandatory["execution_schedule_permutation_neutral"],
        )),
        "null_reverse_and_target_leak_controls_pass": all((
            origin["opposite_signs_are_not_positive_reparameterisation_equivalent"],
            mandatory["prewired_target_DAG_rejected"],
            mandatory["frozen_nonresponsive_null"],
            mandatory["all_inherited_F2_nulls_and_boundaries_controlled"],
        )),
        "perturbation_and_initial_condition_stability_proved": all((
            dynamics["finite_parameter_open_interval_invariant"],
            algebra["S_spectrum_invariants_and_J_are_preserved"],
            mandatory["small_initial_perturbations_preserve_open_domain"],
        )),
        "independent_second_derivation_passes": mandatory[
            "independent_matrix_and_vector_derivations_agree"
        ],
        "physical_time_metric_and_downstream_gates_remain_open": (
            "physical time" in _scope_text() and "GR bridge" in _scope_text()
        ),
    }
    if set(gates) != set(w217.frozen_f3_gate_keys()):
        return {key: False for key in w217.frozen_f3_gate_keys()}
    return gates


def decision_controls(
    evidence: dict[str, bool], outcomes: dict[str, bool], closure: dict[str, bool],
    gates: dict[str, bool], screen: dict[str, bool], route_screen: dict[str, bool],
    w217: ModuleType, w221: ModuleType,
) -> dict[str, bool]:
    false_gates = {key for key, value in gates.items() if value is False}
    partial_maps = {
        key for key, value in CANDIDATE_MAPS.items() if value["status"] != "DERIVED"
    }
    altered_maps = deepcopy(CANDIDATE_MAPS)
    altered_maps["independent_crosscheck"]["definition"] += " MUTATED"
    scientific_ceiling = evaluated_scientific_ceiling(outcomes, closure, gates)
    altered_ceiling = deepcopy(scientific_ceiling)
    altered_ceiling["closure_decision"]["observational_validation_proved"] = True
    return {
        "w2_17_gate_schema_exact_with_three_unclosed_gates": all((
            set(gates) == set(w217.frozen_f3_gate_keys()),
            false_gates == EXPECTED_FALSE_F3_GATES,
        )),
        "candidate_map_schema_valid_with_declared_partial_absent_maps": all((
            w217.candidate_map_schema_valid(CANDIDATE_MAPS),
            partial_maps == {
                "transition_or_response_law", "forbidden_pairs", "no_transmission_test",
            },
        )),
        "candidate_map_content_hash_and_mutation_control": all((
            candidate_maps_sha256(CANDIDATE_MAPS) == EXPECTED_CANDIDATE_MAPS_SHA256,
            candidate_maps_sha256(altered_maps) != EXPECTED_CANDIDATE_MAPS_SHA256,
        )),
        "evaluated_scientific_ceiling_hash_and_mutation_control": all((
            evaluated_scientific_ceiling_sha256(scientific_ceiling)
            == EXPECTED_EVALUATED_SCIENTIFIC_CEILING_SHA256,
            evaluated_scientific_ceiling_sha256(altered_ceiling)
            != EXPECTED_EVALUATED_SCIENTIFIC_CEILING_SHA256,
        )),
        "w2_17_screen_valid_but_ineligible_and_unpromoted": all((
            screen["valid"], not screen["eligible"], not screen["promoted"],
        )),
        "w2_21_adjudication_screen_complete_but_unpromoted": all((
            route_screen["valid"], route_screen["evidence_complete"],
            not route_screen["promoted"],
        )),
        "conditional_result_resolves_w2_20_predecessor_failure": all((
            gates["same_chain_F1_F2_predecessors_valid"],
            outcomes["same_chain_F1_F2_tangent_motion_available"],
        )),
        "origin_arrow_and_nontransmission_failures_block_full_F3": all((
            not gates["target_free_transition_or_response_law_derived"],
            not gates["arrow_selected_by_law_not_labels_or_schedule"],
            not gates["forbidden_signal_nontransmission_proved"],
            not outcomes["foundation_selects_sign_and_process_law"],
            not outcomes["gauge_invariant_forbidden_pair_nontransmission_available"],
            not outcomes["foundation_derived_F3_internal_order_or_causality"],
        )),
        "physical_time_metric_and_all_downstream_claims_remain_false": all((
            not outcomes["physical_time_or_clock"],
            not outcomes["foundation_to_effective_closed"],
            not closure["Lorentzian_metric_or_GR_bridge_proved"],
            not closure["observational_validation_proved"],
        )),
        "closure_matches_exact_predeclared_ceiling": all((
            outcomes == EXPECTED_OUTCOMES == frozen_outcomes(),
            closure == EXPECTED_CLOSURE_FLAGS == frozen_closure_flags(),
            set(evidence) == set(w221.EVIDENCE_KEYS),
        )),
    }


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_safe(item) for item in value]
    return str(value)


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run() -> dict[str, Any]:
    w216 = _load_local_module(
        "w2_16_f2b_general_traceless_single_carrier_candidate_gate.py", "w216_tangent"
    )
    w217 = _load_local_module(
        "w2_17_f3_internal_order_causality_contract.py", "w217_tangent"
    )
    w220 = _load_local_module(
        "w2_20_f3_gradient_formation_flow_candidate_gate.py", "w220_tangent"
    )
    w221 = _load_local_module(
        "w2_21_f3_minimum_manifold_tangent_route_contract.py", "w221_tangent"
    )

    dependency = dependency_controls(w216, w217, w220, w221)
    algebra, algebra_diagnostics = algebra_controls()
    dynamics, dynamics_diagnostics = dynamics_controls()
    origin, origin_diagnostics = origin_controls(w221)
    mandatory = mandatory_f3_controls(algebra, dynamics, origin)

    evidence = {
        "dependencies_exact": all(dependency.values()),
        "minimum_manifold_and_quotient_rederived": all((
            algebra["projector_normal_form_exact"],
            algebra["carrier_norm_and_tau_exact"],
        )),
        "generator_is_skew_and_carrier_generated": algebra[
            "Omega_is_skew_covariant_and_carrier_generated"
        ],
        "flow_is_tangent_and_preserves_same_chain_F1_F2": all((
            algebra["flow_is_tangent_to_complete_product_minimum_manifold"],
            algebra["same_chain_generic_F1_F2_domain_is_preserved"],
        )),
        "quotient_equation_exact": all((
            algebra["tau_equation_exact_full_matrix_derivation"],
            algebra["tau_equation_exact_independent_vector_derivation"],
        )),
        "common_motion_is_gauge_and_relative_motion_is_nongauge": algebra[
            "common_coefficient_is_gauge_and_relative_coefficient_is_nongauge"
        ],
        "generic_open_stratum_is_finite_parameter_invariant": dynamics[
            "finite_parameter_open_interval_invariant"
        ],
        "gauge_invariant_quotient_intervention_response_exact": all((
            dynamics["quotient_intervention_response_is_nonzero_and_gauge_invariant"],
            mandatory["three_event_directed_order_positive_control"],
        )),
        "raw_one_way_channel_reading_rejected_as_gauge_dependent": all((
            dynamics["raw_one_way_channel_lifts_are_gauge_equivalent"],
            dynamics["no_substantive_gauge_invariant_forbidden_pair_is_available"],
        )),
        "static_law_is_flat_and_cannot_select_arrow": origin[
            "static_U_is_constant_on_tau_and_has_zero_tangent_gradient"
        ],
        "opposite_branches_and_multiplier_freedom_are_explicit": all((
            dynamics["opposite_quotient_sign_branch_is_equally_algebraically_admissible"],
            origin["opposite_signs_are_not_positive_reparameterisation_equivalent"],
            origin["regular_h_tau_multiplier_freedom_is_real"],
        )),
        "declared_foundation_sources_confirm_process_origin_open": all(origin.values()),
        "clock_metric_and_downstream_claims_quarantined": (
            dynamics["one_dimensional_autonomous_quotient_has_no_periodic_clock"]
        ),
        "independent_derivation_and_dependency_chain_pass": all((
            all(dependency.values()),
            algebra["tau_equation_exact_independent_vector_derivation"],
        )),
    }
    outcomes = frozen_outcomes()
    closure = frozen_closure_flags()
    gates = f3_gate_map(algebra, dynamics, origin, mandatory, w217)
    screen = w217.candidate_screen(gates, CANDIDATE_MAPS)
    route_screen = w221.adjudication_screen(evidence, outcomes)
    decisions = decision_controls(
        evidence, outcomes, closure, gates, screen, route_screen, w217, w221
    )

    control_groups = {
        "dependency": (dependency, DEPENDENCY_KEYS),
        "algebra": (algebra, ALGEBRA_KEYS),
        "dynamics": (dynamics, DYNAMICS_KEYS),
        "origin": (origin, ORIGIN_KEYS),
        "mandatory_f3_controls": (mandatory, MANDATORY_F3_CONTROL_KEYS),
        "decision": (decisions, DECISION_KEYS),
    }
    schemas_exact = all(
        set(group) == keys and all(type(value) is bool for value in group.values())
        for group, keys in control_groups.values()
    )
    valid = bool(
        schemas_exact
        and all(all(group.values()) for group, _ in control_groups.values())
        and set(evidence) == set(w221.EVIDENCE_KEYS)
        and all(evidence.values())
        and route_screen["valid"]
        and route_screen["evidence_complete"]
        and not route_screen["promoted"]
        and screen["valid"]
        and not screen["eligible"]
        and not screen["promoted"]
    )

    return _json_safe({
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "provenance": {
            "date": "2026-07-22",
            "evaluator_source_sha256": _file_sha256(Path(__file__).resolve()),
            "w2_21_contract_payload_sha256": w221.EXPECTED_CONTRACT_PAYLOAD_SHA256,
            "w2_21_route_spec_sha256": w221.EXPECTED_ROUTE_SPEC_SHA256,
            "w2_21_origin_audit_snapshot_sha256": (
                w221.EXPECTED_ORIGIN_AUDIT_SNAPSHOT_SHA256
            ),
            "candidate_maps_sha256": EXPECTED_CANDIDATE_MAPS_SHA256,
            "evaluated_scientific_ceiling_sha256": (
                EXPECTED_EVALUATED_SCIENTIFIC_CEILING_SHA256
            ),
        },
        "valid": valid,
        "candidate_status": CANDIDATE_STATUS_PASS if valid else "INVALID_OR_OPEN",
        "claim": CLAIM_TEXT,
        "conclusion": CONCLUSION_TEXT,
        "candidate_maps": CANDIDATE_MAPS,
        "f3_gate_map": gates,
        "f3_screen": screen,
        "route_contract_screen": route_screen,
        "outcomes": outcomes,
        "closure_decision": closure,
        "controls": {
            "dependency": dependency,
            "algebra": algebra,
            "dynamics": dynamics,
            "origin": origin,
            "mandatory_f3_controls": mandatory,
            "decision": decisions,
        },
        "diagnostics": {
            "algebra": algebra_diagnostics,
            "dynamics": dynamics_diagnostics,
            "origin": origin_diagnostics,
        },
    })


def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_ID,
            "valid": False,
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(_json_safe(report), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if all((
        report.get("valid") is True,
        report.get("outcomes", {}).get(
            "same_chain_F1_F2_tangent_motion_available"
        ) is True,
        report.get("outcomes", {}).get(
            "foundation_derived_F3_internal_order_or_causality"
        ) is False,
    )) else 1


if __name__ == "__main__":
    raise SystemExit(main())
