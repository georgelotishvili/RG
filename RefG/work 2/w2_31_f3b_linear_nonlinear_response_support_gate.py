"""Exact linear-tangent response and local-section diagnostic after w2_30.

The five-channel calculation is exact only on the kinetic-horizontal,
zero-Noether-momentum linear tangent candidate.  The fixed affine section is
not a full nonlinear reduced phase space.  Expanding the potential on it gives
an exact local-section interaction diagnostic, not full Routh-reduced response
or causal support.

The diagnostic has residual parities and a connected five-channel interaction
graph.  Neither result supplies transmitter/receiver occurrences, a propagation
front or a causal cone.  F3b and locality remain open.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any

import sympy as sp


CLAIM_ID = "W2_F3B_FINITE_CELL_LINEAR_NONLINEAR_SUPPORT_AUDIT_001"
MODEL_VERSION = "W2-F3B-FINITE-CELL-RESPONSE-SUPPORT-v1.2-INTEGRITY-HARDENED"

REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

EVIDENCE_KEYS = frozenset({
    "w2_30_and_scope_dependencies_valid",
    "global_symmetry_orbit_has_positive_kinetic_norm_exact",
    "zero_momentum_horizontal_linear_response_operator_exact",
    "linear_tangent_support_is_three_plus_one_plus_one_exact",
    "normal_mode_diagonal_zeros_are_selection_rules_exact",
    "local_section_residual_parity_diagnostic_exact",
    "local_section_interaction_graph_diagnostic_exact",
    "local_section_core_vertex_diagnostic_exact",
    "full_Routh_or_symplectic_reduction_absent",
    "linear_selection_zeros_not_promoted_to_causal_support",
    "finite_cell_F3b_ceiling_enforced",
})

CHANNEL_SPEC: dict[str, Any] = {
    "ordered_slice_channels": (
        "diagonal_symmetric_1", "diagonal_symmetric_2", "axial_skew",
        "transverse_c_y", "transverse_e_x",
    ),
    "semantic_status": "zero-Noether-momentum horizontal linear tangent channels at one stationary orbit",
    "physical_place_or_event_labels": False,
    "linear_support_expected": (
        (1, 1, 1, 0, 0),
        (1, 1, 1, 0, 0),
        (1, 1, 1, 0, 0),
        (0, 0, 0, 1, 0),
        (0, 0, 0, 0, 1),
    ),
}


def frozen_outcomes() -> dict[str, bool]:
    return {
        "conditional_zero_momentum_linear_tangent_response_derived": True,
        "conditional_linear_tangent_selection_rules_proved": True,
        "local_section_residual_parity_diagnostic_computed": True,
        "local_section_interaction_graph_connected": True,
        "full_nonlinear_reduced_response_derived": False,
        "full_nonlinear_support_or_factorization_adjudicated": False,
        "full_Routh_or_symplectic_reduction_proved": False,
        "physical_mode_occurrences_derived": False,
        "physical_forbidden_pair_domain_derived": False,
        "finite_propagation_front_or_causal_cone_derived": False,
        "F3b_causal_separability_nontransmission_proved": False,
        "general_finite_carrier_F3b_no_go_proved": False,
        "current_finite_cell_sufficient_for_locality_promotion": False,
    }


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "F4_simultaneous_physical_modes_proved": False,
        "state_owned_physical_mode_occurrences_derived": False,
        "allowed_physical_interventions_derived": False,
        "direct_physical_influence_relation_derived": False,
        "nonempty_invariant_forbidden_pair_domain_derived": False,
        "signal_support_composition_derived": False,
        "forbidden_pair_nontransmission_proved": False,
        "F3b_causal_separability_nontransmission_proved": False,
        "dimension_continuum_metric_or_GR_proved": False,
        "observational_validation_proved": False,
    }


EXPECTED_OUTCOMES = frozen_outcomes()
EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "For the exact w2_30 witness, derive the zero-Noether-momentum horizontal linear-tangent "
        "response, audit the fixed affine section's potential interactions as a local diagnostic, "
        "and decide whether either result closes F3b."
    ),
    "TYPE": "EXACT_LINEAR_TANGENT_RESPONSE_LOCAL_SECTION_DIAGNOSTIC_AND_F3B_CEILING",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "The w2_30 witness, horizontal tangent, kinetic metric and Hessian are consumed unchanged. "
        "The three O(3) directions are global-symmetry modes with positive kinetic norm. The transfer "
        "parameter remains uncalibrated and no full symmetry reduction is assumed."
    ),
    "DOMAIN": (
        "Exact linear response on the horizontal tangent and degree-three/four potential vertices "
        "on its fixed affine local section. No nonlinear reduced dynamics, continuum, receiver "
        "domain or spacetime limit is assumed."
    ),
    "CONVENTIONS": (
        "For Q(0)=0 and Q'(0)=u, Q(sigma)=sigma*u-sigma^3*D*u/6+... with "
        "D=M_h^{-1}H_h on the horizontal tangent. Linear support records exact tangent-response "
        "coefficients. Mixed monomials of U(A_*+Bq) form only a local-section potential-interaction "
        "diagnostic; they are not the equations of a Routh-reduced system or a causal cone."
    ),
    "FREEDOM_LEDGER": {
        "background_law_and_slice": {
            "source": "w2_30 frozen witness", "range": "unchanged",
            "complexity": "inherits its 8 coefficient and 5 transverse-state choices",
        },
        "interventions": {
            "source": "diagnostic zero-momentum horizontal initial velocities", "range": "five tangent channels",
            "complexity": 5,
        },
        "nonlinear_reduction": {
            "source": "absent", "range": "no connection, Routhian or reduced symplectic dynamics",
            "complexity": "full nonlinear support remains unassessed",
        },
        "support_threshold": {
            "source": "exact algebra", "range": "zero versus nonzero", "complexity": 0,
        },
        "physical_event_graph_distance_clock_or_metric": {
            "source": "absent", "range": 0, "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_30_f4_law_derived_mode_inventory_gate.py: full 5-positive plus 3-Goldstone spectrum and linear tangent candidate",
        "RefG/work 2/w2_26_f3b_causal_separation_gate.py: mode-selective support is not classified by 1D order",
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py: physical support maps remain absent",
    ],
    "METHOD": (
        "Compute the horizontal tangent D and its analytic response exactly; verify C^T M C>0, "
        "C^T M B=0 and full-linear invariance of span(B). Separately expand U(A_*+Bq), verify local "
        "parities and enumerate its mixed vertices, while keeping every full nonlinear reduction "
        "and support field false."
    ),
    "PASS_CONDITION": (
        "The audit passes only if the linear tangent identities and local-section diagnostics are "
        "exact, the missing nonlinear reduction is explicit, and every physical F3b flag stays false."
    ),
    "FAIL_CONDITION": (
        "A wrong tangent response, missed local-section term, false parity, treating the affine "
        "section as full reduced dynamics, dependency drift or F3b promotion invalidates the audit."
    ),
    "FALSIFIER": (
        "An exact error in the linear tangent or local-section calculation falsifies its respective "
        "claim. A future completed reduction or physical support map lies outside this scope and "
        "reopens F3b rather than validating the current diagnostic retroactively."
    ),
    "RESIDUAL": "Zero for the response operator, parity and interaction-derivative identities.",
    "ERROR_BOUND": "Zero; exact rational polynomial algebra only.",
    "VALIDITY_HEALTH": (
        "The affine-section pair graph records local potential vertices only. Curvature, mechanical "
        "connection and momentum-dependent terms of a true reduction may change nonlinear response. "
        "Physical F3b additionally requires derived occurrences, receivers and support composition."
    ),
    "BRANCHES": {
        "zero_momentum_linear_horizontal_tangent": "EXACT_THREE_PLUS_ONE_PLUS_ONE",
        "normal_spectral_basis": "FIVE_DIAGONAL_INTERNAL_MODES",
        "affine_local_section_potential_graph": "CONNECTED_DIAGNOSTIC_ONLY",
        "full_nonlinear_reduced_response": "OPEN_REDUCTION_ABSENT",
        "residual_parity": "EXACT_LOCAL_SECTION_SELECTION_DIAGNOSTIC",
        "physical_F3b": "OPEN_SUPPORT_DOMAIN_ABSENT",
        "general_finite_carrier_no_go": "NOT_CLAIMED",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "no physical transmitter or receiver"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "internal response is not a data model"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, fit, calibration or target"},
    "IDENTIFIABILITY": (
        "The calculation distinguishes full symmetry modes, horizontal tangent response, local-"
        "section parity and full nonlinear reduced dynamics. None identifies physical location."
    ),
    "BENCHMARK": (
        "Linear D must give the exact 3+1+1 pattern and preserve the horizontal tangent. The affine "
        "section must yield the declared complete diagnostic graph, while any mutation that calls "
        "it full reduced support or F3b must fail."
    ),
    "CLOSURE_FLAGS": frozen_closure_flags(),
    "CROSSCHECK": (
        "Cross-check the tangent operator from the full eight-coordinate linear law. Cross-check the "
        "separate affine-section diagnostic by direct derivatives and monomial enumeration."
    ),
    "PROVENANCE": {"date": "2026-07-23", "data": "none", "code_version": "w2_31 v1.2 integrity-hardened"},
    "FILES": [
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py",
        "RefG/work 2/w2_26_f3b_causal_separation_gate.py",
        "RefG/work 2/w2_30_f4_law_derived_mode_inventory_gate.py",
        "RefG/work 2/w2_31_f3b_linear_nonlinear_response_support_gate.py",
    ],
}
CLAIM_CONTRACT = SCIENTIFIC_CONTRACT

EXPECTED_CHANNEL_SPEC_SHA256 = (
    "F0A8D07BC052FC4F0D8011A7B4256DCF234FCEFE3D0F210660A2B2D2071FE088"
)
EXPECTED_SCIENTIFIC_CONTRACT_SHA256 = (
    "5787FC8413471912E1E535EC180FC5504F27AE40B1D60CBEC0615675EFE36E2C"
)


def _load_sibling(filename: str, module_name: str) -> ModuleType:
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def _exact_bool_map(value: Any, keys: frozenset[str]) -> bool:
    return bool(
        isinstance(value, dict) and set(value) == keys
        and all(type(item) is bool for item in value.values())
    )


def _all_false(value: dict[str, bool]) -> bool:
    return all(type(item) is bool and item is False for item in value.values())


def _canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def payload_integrity_screen(channel_spec: Any, contract: Any) -> bool:
    return bool(
        isinstance(channel_spec, dict)
        and isinstance(contract, dict)
        and set(contract) == REQUIRED_SCIENTIFIC_FIELDS
        and _canonical_sha256(channel_spec) == EXPECTED_CHANNEL_SPEC_SHA256
        and _canonical_sha256(contract) == EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        and contract.get("CLOSURE_FLAGS") == EXPECTED_CLOSURE_FLAGS
    )


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if isinstance(value, sp.MatrixBase):
        return [[str(sp.simplify(item)) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


def dependency_controls() -> tuple[dict[str, bool], dict[str, ModuleType]]:
    w230 = _load_sibling(
        "w2_30_f4_law_derived_mode_inventory_gate.py", "w230_for_w231"
    )
    w226 = _load_sibling(
        "w2_26_f3b_causal_separation_gate.py", "w226_for_w231"
    )
    report30 = w230.run()
    report26 = w226.run()
    objects = w230.linearized_objects()
    w225 = objects["dependency"]
    report25 = w225.run()
    closure26 = report26.get("closure_flags", {})
    outcomes30 = report30.get("outcomes", {})
    controls = {
        "w2_30_full_spectrum_and_linear_tangent_audit_valid": all((
            w230.CLAIM_ID == "W2_F4_FULL_LAW_FINITE_CELL_NORMAL_MODE_AUDIT_001",
            report30.get("valid") is True,
            outcomes30.get("full_linear_spectrum_five_positive_three_zero_proved") is True,
            outcomes30.get("three_zero_modes_are_global_symmetry_Goldstone_directions") is True,
            outcomes30.get("three_symmetry_directions_are_description_gauge_nulls") is False,
            outcomes30.get("conditional_five_mode_zero_momentum_linear_tangent_candidate_proved") is True,
            outcomes30.get("full_Routh_or_symplectic_reduction_proved") is False,
            outcomes30.get("F4_simultaneous_physical_modes_proved") is False,
            outcomes30.get("stationary_branch_unique_or_law_selected") is False,
        )),
        "w2_26_scope_boundary_valid": all((
            w226.CLAIM_ID == "W2_F3B_CONNECTED_1D_ORBIT_INCOMPARABILITY_ONLY_NO_GO_001",
            report26.get("valid") is True,
            closure26.get("connected_1D_general_F3b_no_go_proved") is False,
            closure26.get("F4_mode_selective_nontransmission_impossible_proved") is False,
            closure26.get("F3b_causal_separability_nontransmission_proved") is False,
        )),
        "w2_25_physical_support_maps_absent": all((
            report25.get("valid") is True,
            w225.CANDIDATE_MAPS["signal_support_composition"]["status"] == "ABSENT",
            w225.CANDIDATE_MAPS["forbidden_pair_domain"]["status"] == "ABSENT",
            w225.CANDIDATE_MAPS["nontransmission_test"]["status"] == "ABSENT",
        )),
    }
    return controls, {"w230": w230, "w226": w226, "w225": w225}


def response_controls(w230: ModuleType) -> tuple[dict[str, bool], dict[str, Any]]:
    data = w230.linearized_objects()
    o = data["objects"]
    M, H, B = data["horizontal_gram"], data["horizontal_hessian"], data["slice_basis"]
    full_M, full_H, C = data["gram"], data["hessian"], data["orbit"]
    D = sp.simplify(M.inv() * H)
    full_D = sp.simplify(full_M.inv() * full_H)
    orbit_metric = sp.simplify(C.T * full_M * C)
    expected_D = sp.Matrix([
        [sp.Rational(1231, 12), sp.Rational(757, 6), sp.Rational(70, 3), 0, 0],
        [sp.Rational(592, 3), sp.Rational(2939, 12), sp.Rational(190, 3), 0, 0],
        [55, 75, 80, 0, 0],
        [0, 0, 0, 208, 0],
        [0, 0, 0, 0, sp.Rational(629, 4)],
    ])
    support = tuple(
        tuple(1 if sp.simplify(D[i, j]) != 0 else 0 for j in range(5))
        for i in range(5)
    )
    core = D[:3, :3]
    core_power_support = tuple(
        tuple(
            tuple(1 if sp.simplify((D**power)[i, j]) != 0 else 0 for j in range(3))
            for i in range(3)
        )
        for power in range(1, 4)
    )
    lam = sp.symbols("lambda", real=True)
    characteristic = sp.Poly(sp.expand((H - lam * M).det()), lam)

    Q = sp.symbols("q0:5", real=True)
    coordinate_substitution = {
        o["coordinates"][i]: data["background"][o["coordinates"][i]]
        + sum(B[i, j] * Q[j] for j in range(5))
        for i in range(8)
    }
    Uq = sp.expand(
        o["U"].subs(data["parameter_point"]).subs(coordinate_substitution)
    )
    zero = {item: 0 for item in Q}
    polynomial = sp.Poly(Uq, *Q)
    hyperedges: list[tuple[int, ...]] = []
    pair_edges: set[tuple[int, int]] = set()
    for monomial, coefficient in polynomial.terms():
        vertices = tuple(index for index, power in enumerate(monomial) if power)
        if sum(monomial) >= 3 and len(vertices) >= 2 and coefficient != 0:
            hyperedges.append(vertices)
            pair_edges.update(itertools.combinations(vertices, 2))
    complete_edges = set(itertools.combinations(range(5), 2))

    parity_q3 = sp.expand(Uq.subs(Q[3], -Q[3]) - Uq)
    parity_q4 = sp.expand(Uq.subs(Q[4], -Q[4]) - Uq)
    invariant_q3 = sp.expand(sp.diff(Uq, Q[3]).subs(Q[3], 0))
    invariant_q4 = sp.expand(sp.diff(Uq, Q[4]).subs(Q[4], 0))
    T_core_33 = sp.Matrix([[
        sp.diff(Uq, Q[i], Q[3], Q[3]).subs(zero) for i in range(3)
    ]])
    T_core_44 = sp.Matrix([[
        sp.diff(Uq, Q[i], Q[4], Q[4]).subs(zero) for i in range(3)
    ]])
    quartic_3344 = sp.diff(Uq, Q[3], Q[3], Q[4], Q[4]).subs(zero)
    observability_3 = sp.Matrix.vstack(
        T_core_33, T_core_33 * core, T_core_33 * core**2
    )
    observability_4 = sp.Matrix.vstack(
        T_core_44, T_core_44 * core, T_core_44 * core**2
    )

    rotation = sp.eye(5)
    rotation[:2, :2] = sp.Matrix([[1, 1], [1, -1]])
    rotated_D = sp.simplify(rotation.inv() * D * rotation)
    spectral_simple = sp.gcd(characteristic, characteristic.diff()).degree() == 0
    controls = {
        "global_symmetry_orbit_has_positive_kinetic_norm_exact": all((
            orbit_metric == sp.diag(52, 34, 2),
            orbit_metric.is_positive_definite is True,
            w230.REDUCTION_STATUS["constant_O3_global_symmetry"] is True,
            w230.REDUCTION_STATUS["time_local_O3_gauge_symmetry"] is False,
            w230.REDUCTION_STATUS["orbit_tangent_kinetic_null"] is False,
        )),
        "zero_momentum_horizontal_linear_response_operator_exact": all((
            _matrix_zero(D - expected_D),
            _matrix_zero(M * D - D.T * M),
            _matrix_zero(C.T * full_M * B),
            _matrix_zero(full_D * B - B * D),
            sp.hessian(Uq, Q).subs(zero) == H,
            w230.REDUCTION_STATUS["full_Noether_momentum_formula_derived"] is True,
            w230.REDUCTION_STATUS["Noether_momentum_conservation_proved"] is True,
        )),
        "linear_tangent_support_is_three_plus_one_plus_one_exact": all((
            support == CHANNEL_SPEC["linear_support_expected"],
            core_power_support == (((1, 1, 1),) * 3,) * 3,
            _matrix_zero(D[:3, 3:]), _matrix_zero(D[3:, :3]),
        )),
        "normal_mode_diagonal_zeros_are_selection_rules_exact": all((
            spectral_simple,
            D.is_diagonalizable() is True,
            rotated_D[0, 1] != 0,
            CHANNEL_SPEC["physical_place_or_event_labels"] is False,
        )),
        "local_section_residual_parity_diagnostic_exact": all((
            parity_q3 == 0, parity_q4 == 0,
            invariant_q3 == 0, invariant_q4 == 0,
        )),
        "local_section_interaction_graph_diagnostic_exact": all((
            pair_edges == complete_edges,
            quartic_3344 == 67856,
            len(hyperedges) == 30,
        )),
        "local_section_core_vertex_diagnostic_exact": all((
            T_core_33 == sp.Matrix([[sp.Rational(8269, 2), 7990, 4892]]),
            T_core_44 == sp.Matrix([[4320, sp.Rational(6789, 2), 3244]]),
            observability_3.rank() == 3,
            observability_4.rank() == 3,
            observability_3.det() == sp.Rational(1324265686436833567, 4),
            observability_4.det() == -sp.Rational(308307214435391971, 3),
        )),
        "full_Routh_or_symplectic_reduction_absent": all((
            w230.REDUCTION_STATUS["full_momentum_level_reduction_constructed"] is False,
            w230.REDUCTION_STATUS["mechanical_connection_constructed"] is False,
            w230.REDUCTION_STATUS["Routhian_constructed"] is False,
            w230.REDUCTION_STATUS["reduced_symplectic_form_constructed"] is False,
            w230.REDUCTION_STATUS["nonlinear_reduced_equations_constructed"] is False,
            EXPECTED_OUTCOMES["full_nonlinear_reduced_response_derived"] is False,
            EXPECTED_OUTCOMES["full_nonlinear_support_or_factorization_adjudicated"] is False,
        )),
        "linear_selection_zeros_not_promoted_to_causal_support": all((
            EXPECTED_OUTCOMES["conditional_linear_tangent_selection_rules_proved"] is True,
            EXPECTED_OUTCOMES["physical_forbidden_pair_domain_derived"] is False,
            EXPECTED_OUTCOMES["finite_propagation_front_or_causal_cone_derived"] is False,
        )),
        "finite_cell_F3b_ceiling_enforced": all((
            EXPECTED_OUTCOMES["F3b_causal_separability_nontransmission_proved"] is False,
            EXPECTED_OUTCOMES["general_finite_carrier_F3b_no_go_proved"] is False,
            EXPECTED_OUTCOMES["current_finite_cell_sufficient_for_locality_promotion"] is False,
            _all_false(CLAIM_CONTRACT["CLOSURE_FLAGS"]),
        )),
    }
    certificate = {
        "zero_momentum_horizontal_linear_operator_D": D,
        "linear_tangent_support": support,
        "response_series": "Q=sigma*u-sigma^3*D*u/6+sigma^5*D^2*u/120+...",
        "global_symmetry_orbit_kinetic_gram": orbit_metric,
        "local_affine_section_diagnostic": {
            "interaction_hyperedge_count": len(hyperedges),
            "interaction_pair_edges": tuple(sorted(pair_edges)),
            "residual_parities": ("q3 -> -q3", "q4 -> -q4"),
            "core_to_q3_squared_vertex": T_core_33,
            "core_to_q4_squared_vertex": T_core_44,
            "q3_squared_q4_squared_vertex": quartic_3344,
        },
        "local_section_core_observability_determinants": (
            observability_3.det(), observability_4.det(),
        ),
        "full_reduction_status": w230.REDUCTION_STATUS,
    }
    return controls, certificate


def audit_screen(evidence: Any) -> dict[str, bool]:
    schema = _exact_bool_map(evidence, EVIDENCE_KEYS)
    passed = bool(schema and all(evidence.values()))
    return {
        "schema_valid": schema,
        "response_audit_pass": passed,
        "physical_F3b_promoted": False,
    }


def decision_controls(evidence: dict[str, bool]) -> dict[str, bool]:
    base = audit_screen(evidence)
    missing = dict(evidence)
    missing.pop(next(iter(EVIDENCE_KEYS)))
    channel_mutations: list[dict[str, Any]] = []
    for key in CHANNEL_SPEC:
        mutated = deepcopy(CHANNEL_SPEC)
        mutated[key] = "__MUTATED__"
        channel_mutations.append(mutated)
    for row in range(5):
        for column in range(5):
            mutated = deepcopy(CHANNEL_SPEC)
            support = [list(item) for item in mutated["linear_support_expected"]]
            support[row][column] = 1 - int(support[row][column])
            mutated["linear_support_expected"] = tuple(tuple(item) for item in support)
            channel_mutations.append(mutated)
    contract_mutations: list[dict[str, Any]] = []
    for key in CLAIM_CONTRACT:
        mutated = deepcopy(CLAIM_CONTRACT)
        mutated[key] = "__MUTATED__"
        contract_mutations.append(mutated)
    return {
        "positive_map_passes_response_audit_without_F3b": all((
            base["schema_valid"], base["response_audit_pass"],
            not base["physical_F3b_promoted"],
        )),
        "each_single_false_item_blocks_audit": all(
            not audit_screen({**evidence, key: False})["response_audit_pass"]
            for key in EVIDENCE_KEYS
        ),
        "missing_extra_or_nonboolean_map_fails_closed": all((
            not audit_screen(missing)["schema_valid"],
            not audit_screen({**evidence, "extra": True})["schema_valid"],
            not audit_screen({**evidence, next(iter(EVIDENCE_KEYS)): 1})["schema_valid"],
        )),
        "channel_and_contract_payload_mutations_fail_closed": all((
            payload_integrity_screen(CHANNEL_SPEC, CLAIM_CONTRACT),
            all(not payload_integrity_screen(item, CLAIM_CONTRACT)
                for item in channel_mutations),
            all(not payload_integrity_screen(CHANNEL_SPEC, item)
                for item in contract_mutations),
        )),
        "outcome_and_closure_ledgers_exact": all((
            frozen_outcomes() == EXPECTED_OUTCOMES,
            frozen_closure_flags() == EXPECTED_CLOSURE_FLAGS,
            CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS,
        )),
    }


def run() -> dict[str, Any]:
    dependency, modules = dependency_controls()
    response, certificate = response_controls(modules["w230"])
    evidence = {
        "w2_30_and_scope_dependencies_valid": all(dependency.values()),
        **response,
    }
    decisions = decision_controls(evidence)
    definition = {
        "contract_schema_exact": set(CLAIM_CONTRACT) == REQUIRED_SCIENTIFIC_FIELDS,
        "frozen_payload_hashes_exact": payload_integrity_screen(
            CHANNEL_SPEC, CLAIM_CONTRACT
        ),
        "channel_schema_exact": len(CHANNEL_SPEC["ordered_slice_channels"]) == 5,
        "physical_closure_flags_all_false": _all_false(CLAIM_CONTRACT["CLOSURE_FLAGS"]),
    }
    valid = bool(
        all(dependency.values())
        and _exact_bool_map(evidence, EVIDENCE_KEYS) and all(evidence.values())
        and all(decisions.values()) and all(definition.values())
    )
    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": valid,
        "status": (
            "PASS_ZERO_MOMENTUM_LINEAR_TANGENT_RESPONSE__LOCAL_SECTION_DIAGNOSTIC__F3B_OPEN"
            if valid else "FAIL_INVALID_NO_PROMOTION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The zero-Noether-momentum horizontal linear-tangent response is exact. The fixed "
            "affine section has a connected five-channel potential-interaction graph, but this is "
            "only a local diagnostic because full Routh/symplectic reduction is absent. No physical "
            "occurrence pair or signal support is derived, so F3b and locality remain open."
        ),
        "outcomes": frozen_outcomes(),
        "closure_flags": frozen_closure_flags(),
        "dependency_controls": dependency,
        "controls": {"definition": definition, "response": response, "decision": decisions},
        "certificate": certificate,
        "hashes": {
            "channel_spec": _canonical_sha256(CHANNEL_SPEC),
            "scientific_contract": _canonical_sha256(CLAIM_CONTRACT),
        },
    }


def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_ID, "model_version": MODEL_VERSION, "valid": False,
            "status": "FAIL_INVALID_NO_PROMOTION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(_json_safe(report), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
