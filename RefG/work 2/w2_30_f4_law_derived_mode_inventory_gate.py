"""Exact full-spectrum audit of the finite full-law A,V representation.

The common constant O(3) action is a global symmetry of the positive kinetic
law.  It is not a time-local gauge symmetry: its three orbit tangents have
strictly positive kinetic norm.  At the frozen nonzero stationary orbit the
full generalized spectrum therefore contains five positive oscillatory modes
and three zero-frequency symmetry/Goldstone modes.

The kinetic-horizontal five-dimensional tangent is also calculated.  It is
only a conditional linear zero-Noether-momentum reduction candidate.  No full
momentum map reduction, mechanical connection, Routhian or reduced symplectic
dynamics is supplied, so the five-mode slice is not promoted to a physical
branch or to F4.
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


CLAIM_ID = "W2_F4_FULL_LAW_FINITE_CELL_NORMAL_MODE_AUDIT_001"
MODEL_VERSION = "W2-F4-FULL-LAW-FINITE-CELL-NORMAL-MODES-v1.2-INTEGRITY-HARDENED"

REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

EVIDENCE_KEYS = frozenset({
    "w2_25_structured_dependency_valid",
    "stationary_full_mixed_law_witness_exact",
    "positive_kinetic_gram_exact",
    "three_global_symmetry_zero_frequency_directions_exact",
    "symmetry_directions_have_positive_kinetic_norm_exact",
    "full_spectrum_has_five_positive_and_three_zero_frequencies_exact",
    "horizontal_zero_momentum_linear_tangent_candidate_exact",
    "full_and_horizontal_characteristic_polynomials_agree_exactly",
    "full_Routh_or_symplectic_reduction_absent",
    "finite_cell_physical_promotion_ceiling_enforced",
})

WITNESS_SPEC: dict[str, Any] = {
    "coordinate_order": ("a", "bb", "cc", "dd", "ee", "x", "y", "z"),
    "background": (1, 2, 0, 0, 0, 0, 0, 1),
    "coefficients": {
        "alpha": "737/4", "eta": "78", "b": "5/4", "gamma": "43",
        "c": "12", "e": "13", "d": "20", "delta": "3",
    },
    "coercive_domain_check": "c>0, d>0, e>|delta|",
    "physical_interpretation": "none; exact conditional representation witness",
}

REDUCTION_STATUS: dict[str, Any] = {
    "constant_O3_global_symmetry": True,
    "time_local_O3_gauge_symmetry": False,
    "orbit_tangent_kinetic_null": False,
    "full_Noether_momentum_formula_derived": True,
    "Noether_momentum_conservation_proved": True,
    "linear_momentum_zero_horizontal_tangent_available": True,
    "full_momentum_level_reduction_constructed": False,
    "mechanical_connection_constructed": False,
    "locked_inertia_reduction_constructed": False,
    "Routhian_constructed": False,
    "reduced_symplectic_form_constructed": False,
    "nonlinear_reduced_equations_constructed": False,
    "unique_physical_branch_selected": False,
}


def frozen_outcomes() -> dict[str, bool]:
    return {
        "conditional_full_law_stationary_orbit_proved": True,
        "full_linear_spectrum_five_positive_three_zero_proved": True,
        "three_zero_modes_are_global_symmetry_Goldstone_directions": True,
        "three_symmetry_directions_are_description_gauge_nulls": False,
        "conditional_five_mode_zero_momentum_linear_tangent_candidate_proved": True,
        "full_Routh_or_symplectic_reduction_proved": False,
        "conditional_stationary_orbit_is_locally_nondegenerate_transverse_to_O3": True,
        "stationary_branch_unique_or_law_selected": False,
        "F4_simultaneous_physical_modes_proved": False,
        "physical_nodes_or_occurrences_derived": False,
        "signal_support_or_locality_derived": False,
        "foundation_carrier_or_law_origin_proved": False,
        "space_time_metric_GR_or_PN_proved": False,
    }


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "F0_common_resonant_kernel_derived": False,
        "F1_self_differentiation_proved_on_derived_kernel": False,
        "F2_operational_relations_proved_on_derived_kernel": False,
        "F3a_intrinsic_process_orientation_proved": False,
        "F4_simultaneous_modes_proved": False,
        "F3b_causal_separability_nontransmission_proved": False,
        "dimension_continuum_metric_or_GR_proved": False,
        "observational_validation_proved": False,
    }


EXPECTED_OUTCOMES = frozen_outcomes()
EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "At the frozen nonzero stationary orbit of the complete mixed w2_25 law, the eight-"
        "coordinate finite carrier has five positive oscillatory modes and three zero-frequency "
        "global-O(3) symmetry/Goldstone modes with positive kinetic norm. The five-dimensional "
        "horizontal calculation is only a zero-Noether-momentum linear tangent candidate because "
        "the full Routh or symplectic reduction is absent."
    ),
    "TYPE": "EXACT_FULL_LINEAR_SPECTRUM_AND_REDUCTION_CEILING_AUDIT",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "The exact w2_25 full degree-four mixed law, Frobenius kinetic form and common-O(3) "
        "equivalence are used unchanged. The carrier and every representation structure remain "
        "imported hypotheses."
    ),
    "DOMAIN": (
        "The frozen exact stationary O(3) orbit and its full eight-coordinate linearized dynamics. "
        "The five-dimensional horizontal calculation is restricted to the tangent level."
    ),
    "CONVENTIONS": (
        "Squared frequencies are generalized eigenvalues of H v=lambda M v. Constant O(3) is a "
        "global symmetry. Because C^T M C is positive, its orbit tangents are genuine zero-frequency "
        "symmetry directions and cannot be removed as time-local gauge nulls."
    ),
    "FREEDOM_LEDGER": {
        "law_coefficient_witness": {
            "source": "frozen before evaluation", "range": "eight declared exact values",
            "complexity": "8 universal candidate choices; no data were used",
        },
        "stationary_orbit_witness": {
            "source": "frozen before evaluation", "range": "one O(3) orbit in the 8-coordinate carrier",
            "complexity": "5 transverse state choices subject to 5 exact stationarity equations",
        },
        "branch_selection": {
            "source": "not supplied by the law", "range": "existence and local continuation only",
            "complexity": "uniqueness and dynamical branch selection remain open",
        },
        "horizontal_slice_basis": {
            "source": "kinetic-orthogonal complement of the O(3) orbit",
            "range": "one linear tangent section at zero symmetry momentum", "complexity": 0,
        },
        "symmetry_reduction_structures": {
            "source": "not supplied", "range": "momentum level, connection, Routhian and reduced symplectic form absent",
            "complexity": "physical five-mode reduction remains open",
        },
        "physical_nodes_graph_metric_or_data": {
            "source": "absent", "range": 0, "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py: exact conditional full-law representation",
        "CODES.md: fail-closed claim and status rules",
    ],
    "METHOD": (
        "Differentiate the unchanged full law exactly, verify stationarity, construct M, H and the "
        "O(3) orbit tangent matrix C, certify C^T M C>0, factor the full generalized spectrum, and "
        "audit the horizontal tangent calculation without assuming a completed symmetry reduction."
    ),
    "PASS_CONDITION": (
        "Every exact evidence field is true, every malformed or single-false evidence map fails "
        "closed, and all physical closure flags remain false."
    ),
    "FAIL_CONDITION": (
        "A nonzero gradient, wrong symmetry kernel, nonpositive orbit kinetic norm, a full spectrum "
        "different from five positive plus three zero roots, determinant mismatch, an invented "
        "Routh reduction, dependency drift or physical promotion invalidates this audit."
    ),
    "FALSIFIER": (
        "Any exact failure of stationarity, positive orbit kinetic norm, symmetry kernel or the "
        "five-positive/three-zero generalized spectrum falsifies the full linear claim."
    ),
    "RESIDUAL": "Zero for stationarity, symmetry-Hessian-null, orthogonality and characteristic identities.",
    "ERROR_BOUND": "Zero; exact rational and symbolic arithmetic only.",
    "VALIDITY_HEALTH": (
        "The Hessian is positive transverse to the symmetry orbit. Local stationary-orbit "
        "continuation is therefore claimed only in a local slice, for sufficiently small O(3)-"
        "invariant perturbations within the declared smooth invariant-law family. Generic symmetry-"
        "breaking perturbations are excluded. This proves neither uniqueness nor law selection, and "
        "the fixed horizontal tangent is not a nonlinear reduced phase space."
    ),
    "BRANCHES": {
        "frozen_full_mixed_stationary_orbit": "EXACT_FULL_LINEAR_SPECTRUM_PASS",
        "O3_orbit_directions": "THREE_ZERO_FREQUENCY_GLOBAL_SYMMETRY_GOLDSTONE_MODES",
        "horizontal_five_mode_tangent": "CONDITIONAL_ZERO_MOMENTUM_LINEAR_CANDIDATE",
        "full_symmetry_reduction": "OPEN",
        "physical_F4": "OPEN_FOUNDATION_AND_NODE_MAP_ABSENT",
        "spacetime_or_causal_support": "OPEN",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "internal pre-spatial modes only"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "no physical measurement model"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, fit or target"},
    "IDENTIFIABILITY": (
        "The five simple positive roots identify five transverse oscillatory eigenspaces. The three "
        "zero roots identify the tangent to the stationary symmetry orbit, with nonzero kinetic norm."
    ),
    "BENCHMARK": (
        "The full determinant must equal the horizontal determinant times exactly three symmetry "
        "zero roots, while C^T M C must be positive definite."
    ),
    "CLOSURE_FLAGS": frozen_closure_flags(),
    "CROSSCHECK": (
        "Compare the full and horizontal characteristic polynomials, verify ker(H)=span(C), and "
        "independently verify that C has positive kinetic norm rather than presymplectic degeneracy."
    ),
    "PROVENANCE": {"date": "2026-07-23", "data": "none", "code_version": "w2_30 v1.2 integrity-hardened"},
    "FILES": [
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py",
        "RefG/work 2/w2_30_f4_law_derived_mode_inventory_gate.py",
    ],
}
CLAIM_CONTRACT = SCIENTIFIC_CONTRACT

# Filled from the frozen literal payloads; runtime checks and mutation controls
# make scientific-payload drift fail closed.
EXPECTED_WITNESS_SPEC_SHA256 = (
    "F1A9E839D7A9E07FC9413E244AD90EC40B408AD6698EA2560FAD489E9D636B32"
)
EXPECTED_SCIENTIFIC_CONTRACT_SHA256 = (
    "66BCDAC93EE0F2D8E46ACF5E1CEAD2BBA2319A75A691763AB823E5CAB182588D"
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
        isinstance(value, dict)
        and set(value) == keys
        and all(type(item) is bool for item in value.values())
    )


def _all_false(value: dict[str, bool]) -> bool:
    return all(type(item) is bool and item is False for item in value.values())


def _canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def payload_integrity_screen(witness: Any, contract: Any) -> bool:
    return bool(
        isinstance(witness, dict)
        and isinstance(contract, dict)
        and set(contract) == REQUIRED_SCIENTIFIC_FIELDS
        and _canonical_sha256(witness) == EXPECTED_WITNESS_SPEC_SHA256
        and _canonical_sha256(contract) == EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        and contract.get("CLOSURE_FLAGS") == EXPECTED_CLOSURE_FLAGS
    )


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, sp.MatrixBase):
        return [[str(sp.simplify(item)) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


def _coordinate_vector(dS: sp.MatrixBase, dR: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix([
        dS[0, 0], dS[1, 1], dS[1, 2], dS[0, 1], dS[0, 2],
        dR[2, 1], dR[0, 2], dR[1, 0],
    ])


@lru_cache(maxsize=1)
def linearized_objects() -> dict[str, Any]:
    w225 = _load_sibling(
        "w2_25_joint_common_kernel_candidate_gate.py", "w225_for_w230_objects"
    )
    objects = w225.algebra_objects()
    coordinates = objects["coordinates"]
    velocities = objects["velocity_coordinates"]
    coefficients = objects["coefficients"]
    background = dict(zip(coordinates, WITNESS_SPEC["background"]))
    parameter_point = {
        coefficients[name]: sp.Rational(exact_value)
        for name, exact_value in WITNESS_SPEC["coefficients"].items()
    }
    substitution = background | parameter_point
    kinetic = (
        sp.trace(objects["VS"].T * objects["VS"])
        + sp.trace(objects["VR"].T * objects["VR"])
    ) / 2
    gram = sp.hessian(kinetic, velocities)
    hessian = sp.hessian(objects["U"], coordinates).subs(substitution)

    S0 = objects["S"].subs(background)
    R0 = objects["R"].subs(background)
    generators = (
        sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]]),
        sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]]),
    )
    orbit = sp.Matrix.hstack(*(
        _coordinate_vector(O * S0 - S0 * O, O * R0 - R0 * O)
        for O in generators
    ))
    # Columns span the exact kinetic-orthogonal complement of the orbit.
    slice_basis = sp.zeros(8, 5)
    slice_basis[0, 0] = 1
    slice_basis[1, 1] = 1
    slice_basis[7, 2] = 1
    slice_basis[2, 3], slice_basis[6, 3] = 1, 5
    slice_basis[4, 4], slice_basis[5, 4] = 1, 4
    horizontal_gram = sp.simplify(slice_basis.T * gram * slice_basis)
    horizontal_hessian = sp.simplify(slice_basis.T * hessian * slice_basis)
    return {
        "dependency": w225,
        "objects": objects,
        "background": background,
        "parameter_point": parameter_point,
        "substitution": substitution,
        "gram": gram,
        "hessian": hessian,
        "orbit": orbit,
        "generators": generators,
        "slice_basis": slice_basis,
        "horizontal_gram": horizontal_gram,
        "horizontal_hessian": horizontal_hessian,
    }


def dependency_controls() -> dict[str, bool]:
    data = linearized_objects()
    w225 = data["dependency"]
    report = w225.run()
    outcomes = report.get("outcomes", {})
    maps = w225.CANDIDATE_MAPS
    return {
        "identity_and_candidate_valid": all((
            w225.CLAIM_ID == "W2_JOINT_COMMON_KERNEL_REVERSIBLE_FULL_LAW_CANDIDATE_001",
            report.get("valid") is True,
        )),
        "conditional_ceiling_consumed_exactly": all((
            outcomes.get("conditional_representation_F4_state_accounting_available") is True,
            outcomes.get("full_F3a_intrinsic_process_order_proved") is False,
            outcomes.get("F3b_causal_separability_nontransmission_proved") is False,
            outcomes.get("foundation_common_kernel_origin_proved") is False,
        )),
        "node_and_support_maps_remain_unpromoted": all((
            maps["state_owned_role_or_node_map"]["status"] == "PARTIAL",
            maps["simultaneous_mode_inventory"]["status"] == "PARTIAL",
            maps["signal_support_composition"]["status"] == "ABSENT",
            maps["forbidden_pair_domain"]["status"] == "ABSENT",
            maps["nontransmission_test"]["status"] == "ABSENT",
        )),
        "w2_25_physical_flags_all_false": _all_false(
            report.get("physical_closure_flags", {})
        ),
    }


def exact_mode_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    data = linearized_objects()
    o = data["objects"]
    substitution = data["substitution"]
    M, K = data["gram"], data["hessian"]
    C, B = data["orbit"], data["slice_basis"]
    MQ, HQ = data["horizontal_gram"], data["horizontal_hessian"]
    gradient_zero = all(
        sp.simplify(entry.subs(substitution)) == 0
        for matrix in (o["GS"], o["GR"]) for entry in matrix
    )
    lam = sp.symbols("lambda", real=True)
    cubic = 48 * lam**3 - 20520 * lam**2 + 1055719 * lam - 68720
    expected_horizontal = sp.expand(
        -sp.Rational(221, 4) * (lam - 208) * (4 * lam - 629) * cubic
    )
    expected_full = sp.expand(
        lam**3 * (lam - 208) * (4 * lam - 629) * cubic
    )
    horizontal_characteristic = sp.expand((HQ - lam * MQ).det())
    full_characteristic = sp.expand((K - lam * M).det())
    D = sp.simplify(MQ.inv() * HQ)
    full_D = sp.simplify(M.inv() * K)
    kernel_basis = sp.Matrix.hstack(*K.nullspace())
    orbit_metric = sp.simplify(C.T * M * C)
    A, V = o["S"] + o["R"], o["VS"] + o["VR"]
    force_gradient = o["GS"] + o["GR"]
    noether_charges = sp.Matrix([
        sp.expand(sp.trace(V.T * (Omega * A - A * Omega)))
        for Omega in data["generators"]
    ])
    noether_rates = sp.Matrix([
        sp.expand(
            sp.trace((-force_gradient).T * (Omega * A - A * Omega))
            + sp.trace(V.T * (Omega * V - V * Omega))
        )
        for Omega in data["generators"]
    ])
    linear_momentum_map = noether_charges.jacobian(
        o["velocity_coordinates"]
    ).subs(data["background"])
    core = HQ[:3, :3]
    core_minors = tuple(sp.factor(core[:i, :i].det()) for i in range(1, 4))
    positive_roots = all((
        sp.Poly(cubic, lam).count_roots(0, sp.oo) == 3,
        sp.Poly(cubic, lam).count_roots(-sp.oo, 0) == 0,
        sp.discriminant(cubic, lam) > 0,
        sp.expand(cubic.subs(lam, 208)) != 0,
        sp.expand(cubic.subs(lam, sp.Rational(629, 4))) != 0,
    ))
    expected_named_parameters = {
        "alpha": sp.Rational(737, 4), "eta": sp.Integer(78),
        "b": sp.Rational(5, 4), "gamma": sp.Integer(43),
        "c": sp.Integer(12), "e": sp.Integer(13),
        "d": sp.Integer(20), "delta": sp.Integer(3),
    }
    actual_named_parameters = {
        name: data["parameter_point"][o["coefficients"][name]]
        for name in expected_named_parameters
    }
    controls = {
        "stationary_full_mixed_law_witness_exact": all((
            gradient_zero,
            tuple(WITNESS_SPEC["background"]) == (1, 2, 0, 0, 0, 0, 0, 1),
            actual_named_parameters == expected_named_parameters,
            data["parameter_point"][o["coefficients"]["c"]] > 0,
            data["parameter_point"][o["coefficients"]["d"]] > 0,
            data["parameter_point"][o["coefficients"]["e"]]
            > abs(data["parameter_point"][o["coefficients"]["delta"]]),
            all(data["parameter_point"][o["coefficients"][name]] != 0
                for name in ("gamma", "e", "delta")),
        )),
        "positive_kinetic_gram_exact": all((
            M.rank() == 8, M.is_positive_definite is True,
            MQ.rank() == 5, MQ.is_positive_definite is True,
        )),
        "three_global_symmetry_zero_frequency_directions_exact": all((
            C.rank() == 3, K.rank() == 5, len(K.nullspace()) == 3,
            _matrix_zero(K * C),
            kernel_basis.rank() == 3,
            sp.Matrix.hstack(C, kernel_basis).rank() == 3,
            REDUCTION_STATUS["constant_O3_global_symmetry"] is True,
            REDUCTION_STATUS["time_local_O3_gauge_symmetry"] is False,
        )),
        "symmetry_directions_have_positive_kinetic_norm_exact": all((
            orbit_metric == sp.diag(52, 34, 2),
            orbit_metric.is_positive_definite is True,
            REDUCTION_STATUS["orbit_tangent_kinetic_null"] is False,
        )),
        "full_spectrum_has_five_positive_and_three_zero_frequencies_exact": all((
            positive_roots,
            sp.expand(full_characteristic - expected_full) == 0,
            K.rank() == 5,
            len(K.nullspace()) == 3,
        )),
        "horizontal_zero_momentum_linear_tangent_candidate_exact": all((
            B.rank() == 5, sp.Matrix.hstack(C, B).rank() == 8,
            _matrix_zero(C.T * M * B),
            _matrix_zero(noether_rates),
            _matrix_zero(linear_momentum_map - C.T * M),
            _matrix_zero(linear_momentum_map * B),
            core_minors == (sp.Rational(805, 2), sp.Rational(10919, 16), 8590),
            HQ.is_positive_definite is True, HQ.det() != 0,
            _matrix_zero(full_D * B - B * D),
            REDUCTION_STATUS["full_Noether_momentum_formula_derived"] is True,
            REDUCTION_STATUS["Noether_momentum_conservation_proved"] is True,
            REDUCTION_STATUS["linear_momentum_zero_horizontal_tangent_available"] is True,
        )),
        "full_and_horizontal_characteristic_polynomials_agree_exactly": all((
            sp.expand(horizontal_characteristic - expected_horizontal) == 0,
            sp.expand(full_characteristic - expected_full) == 0,
            sp.expand(full_characteristic
                      + sp.Rational(4, 221) * lam**3 * horizontal_characteristic) == 0,
        )),
        "full_Routh_or_symplectic_reduction_absent": all((
            REDUCTION_STATUS["full_momentum_level_reduction_constructed"] is False,
            REDUCTION_STATUS["mechanical_connection_constructed"] is False,
            REDUCTION_STATUS["locked_inertia_reduction_constructed"] is False,
            REDUCTION_STATUS["Routhian_constructed"] is False,
            REDUCTION_STATUS["reduced_symplectic_form_constructed"] is False,
            REDUCTION_STATUS["nonlinear_reduced_equations_constructed"] is False,
            EXPECTED_OUTCOMES["full_Routh_or_symplectic_reduction_proved"] is False,
        )),
        "finite_cell_physical_promotion_ceiling_enforced": all((
            EXPECTED_OUTCOMES["F4_simultaneous_physical_modes_proved"] is False,
            EXPECTED_OUTCOMES["physical_nodes_or_occurrences_derived"] is False,
            EXPECTED_OUTCOMES["signal_support_or_locality_derived"] is False,
            _all_false(CLAIM_CONTRACT["CLOSURE_FLAGS"]),
        )),
    }
    certificate = {
        "kinetic_gram": M,
        "full_hessian": K,
        "orbit_tangent_matrix": C,
        "orbit_kinetic_gram": orbit_metric,
        "linearized_Noether_momentum_matrix": linear_momentum_map,
        "Noether_momentum_rate_residuals": noether_rates,
        "horizontal_slice": B,
        "horizontal_gram": MQ,
        "horizontal_hessian": HQ,
        "horizontal_characteristic_factorization": sp.factor(horizontal_characteristic),
        "full_characteristic_factorization": sp.factor(full_characteristic),
        "full_squared_frequency_spectrum": {
            "zero_symmetry_multiplicity": 3,
            "explicit": (sp.Integer(208), sp.Rational(629, 4)),
            "remaining": "three simple positive roots of 48*x^3-20520*x^2+1055719*x-68720",
        },
        "core_sylvester_minors": core_minors,
        "reduction_status": REDUCTION_STATUS,
    }
    return controls, certificate


def audit_screen(evidence: Any) -> dict[str, bool]:
    schema = _exact_bool_map(evidence, EVIDENCE_KEYS)
    audit_pass = bool(schema and all(evidence.values()))
    return {
        "schema_valid": schema,
        "audit_pass": audit_pass,
        "full_linear_spectrum_proved": audit_pass,
        "full_symmetry_reduction_proved": False,
        "physical_F4_promoted": False,
    }


def decision_controls(evidence: dict[str, bool]) -> dict[str, bool]:
    base = audit_screen(evidence)
    false_blocked = all(
        not audit_screen({**evidence, key: False})["audit_pass"]
        for key in EVIDENCE_KEYS
    )
    missing = dict(evidence)
    missing.pop(next(iter(EVIDENCE_KEYS)))
    extra = {**evidence, "extra": True}
    nonboolean = {**evidence, next(iter(EVIDENCE_KEYS)): 1}
    symmetry_contaminated = linearized_objects()["slice_basis"].copy()
    symmetry_contaminated[:, 4] = linearized_objects()["orbit"][:, 0]
    contaminated_H = sp.simplify(
        symmetry_contaminated.T * linearized_objects()["hessian"] * symmetry_contaminated
    )
    witness_mutations: list[dict[str, Any]] = []
    for key in WITNESS_SPEC:
        mutated = deepcopy(WITNESS_SPEC)
        mutated[key] = "__MUTATED__"
        witness_mutations.append(mutated)
    for name in WITNESS_SPEC["coefficients"]:
        mutated = deepcopy(WITNESS_SPEC)
        mutated["coefficients"][name] = "999999"
        witness_mutations.append(mutated)
    for index in range(len(WITNESS_SPEC["background"])):
        mutated = deepcopy(WITNESS_SPEC)
        background = list(mutated["background"])
        background[index] = int(background[index]) + 1
        mutated["background"] = tuple(background)
        witness_mutations.append(mutated)
    contract_mutations: list[dict[str, Any]] = []
    for key in CLAIM_CONTRACT:
        mutated = deepcopy(CLAIM_CONTRACT)
        mutated[key] = "__MUTATED__"
        contract_mutations.append(mutated)
    return {
        "positive_evidence_passes_full_spectrum_without_reduction_or_F4": all((
            base["schema_valid"], base["audit_pass"],
            base["full_linear_spectrum_proved"],
            not base["full_symmetry_reduction_proved"],
            not base["physical_F4_promoted"],
        )),
        "each_single_false_item_blocks_audit": false_blocked,
        "malformed_evidence_fails_closed": all((
            not audit_screen(missing)["schema_valid"],
            not audit_screen(extra)["schema_valid"],
            not audit_screen(nonboolean)["schema_valid"],
        )),
        "symmetry_contaminated_horizontal_candidate_is_detected": all((
            contaminated_H.det() == 0, contaminated_H.is_positive_definite is not True,
        )),
        "witness_and_contract_payload_mutations_fail_closed": all((
            payload_integrity_screen(WITNESS_SPEC, CLAIM_CONTRACT),
            all(not payload_integrity_screen(item, CLAIM_CONTRACT)
                for item in witness_mutations),
            all(not payload_integrity_screen(WITNESS_SPEC, item)
                for item in contract_mutations),
        )),
        "outcome_and_closure_ledgers_exact": all((
            frozen_outcomes() == EXPECTED_OUTCOMES,
            frozen_closure_flags() == EXPECTED_CLOSURE_FLAGS,
            CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS,
        )),
    }


def run() -> dict[str, Any]:
    dependency = dependency_controls()
    modes, certificate = exact_mode_controls()
    evidence = {
        "w2_25_structured_dependency_valid": all(dependency.values()),
        **modes,
    }
    decisions = decision_controls(evidence)
    definition = {
        "contract_schema_exact": set(CLAIM_CONTRACT) == REQUIRED_SCIENTIFIC_FIELDS,
        "frozen_payload_hashes_exact": payload_integrity_screen(
            WITNESS_SPEC, CLAIM_CONTRACT
        ),
        "witness_coordinate_schema_exact": tuple(WITNESS_SPEC["coordinate_order"])
        == ("a", "bb", "cc", "dd", "ee", "x", "y", "z"),
        "all_physical_flags_false": _all_false(CLAIM_CONTRACT["CLOSURE_FLAGS"]),
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
            "PASS_FULL_LINEAR_SPECTRUM_5_POSITIVE_3_GOLDSTONE__REDUCTION_AND_F4_OPEN"
            if valid else "FAIL_INVALID_NO_PROMOTION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The complete mixed finite-cell law has five positive oscillatory modes and three "
            "zero-frequency global-O(3) symmetry/Goldstone modes with positive kinetic norm. "
            "The horizontal five-mode calculation is only a zero-Noether-momentum linear tangent "
            "candidate; full Routh/symplectic reduction, physical F4 and spacetime remain open."
        ),
        "outcomes": frozen_outcomes(),
        "closure_flags": frozen_closure_flags(),
        "dependency_controls": dependency,
        "controls": {"definition": definition, "modes": modes, "decision": decisions},
        "certificate": certificate,
        "hashes": {
            "witness_spec": _canonical_sha256(WITNESS_SPEC),
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
