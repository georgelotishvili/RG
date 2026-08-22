#!/usr/bin/env python3
"""W3-45 exact conditional active-phase Lambda interface gate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path
from types import ModuleType

import sympy as sp


sys.dont_write_bytecode = True


CLAIM_ID = "W3_45_ACTIVE_PHASE_LAMBDA_INTERFACE"
MODEL_VERSION = "W3-COSMOLOGY-v1.3-ACTIVE-PHASE-LAMBDA-INTERFACE"
PASS_STATUS = (
    "PASS_EXACT_CONDITIONAL_ACTIVE_PHASE_LAMBDA_INTERFACE__"
    "ABSOLUTE_ENERGY_NORMALIZATION_AND_LAMBDA_VALUE_OPEN"
)
W3_39_SCOPE_STATUS = (
    "PASS_EXACT_CONSERVATION_SIGN_AND_CENTERED_BIRTH_SYMMETRY_NO_GO__"
    "GENESIS_MECHANISM_OPEN"
)
W3_40_SCOPE_STATUS = (
    "PASS_EXACT_CAUSAL_LOCK_DICTIONARY__DYNAMICS_AND_OBSERVABLES_OPEN"
)
W3_41_SCOPE_STATUS = (
    "PASS_EXACT_CONSTITUTIVE_INTERFACE__RECONSTRUCTION_DEGENERACY_"
    "PROVED__PHYSICAL_BRIDGE_AND_DYNAMICS_OPEN"
)
BACKGROUND_PASS_STATUS = (
    "PASS_CONDITIONAL_BACKGROUND_EQUATION__"
    "MICROPHYSICS_PARAMETERS_AND_OBSERVABLES_OPEN"
)

EXPECTED_HASHES = {
    "preregistration": (
        "a312202a239eb25c24e66920ef400241528639345ce26967e64b96dba6757e79"
    ),
    "w3_39_result": (
        "ff2440311e2c4ceb5fe5a2393b6730d2a3c2a2c49dd5b2ceaf7e32f0a0ab1160"
    ),
    "w3_39_checksum": (
        "6a15bdd5234330443b27d865d7b9c223b9edb3de621480d954b8df1f55f6e294"
    ),
    "w3_40_result": (
        "e8104a664484ea0735387446c94367cca1035877ee6a26413eeddaf158b5be64"
    ),
    "w3_40_checksum": (
        "f3c2d845d8cba658a527c7501c35bac96ae3e3c607f9375ec514160dc97ccdfa"
    ),
    "w3_41_preregistration": (
        "ab852e070871c707ed46e1ac2edde995931c12bd3a0d117e784c258e9f7ba99b"
    ),
    "w3_41_source": (
        "849fb7a649af526ebcdf00e114bc4cd93e6cdd81b2a1cbd246dfa4c77db18f05"
    ),
    "operational_background_source": (
        "57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055"
    ),
}
EXPECTED_DEPENDENCY_KEYS = frozenset(
    {
        "preregistration",
        "w3_39_result",
        "w3_39_checksum",
        "w3_40_result",
        "w3_40_checksum",
        "w3_41_preregistration",
        "w3_41_source",
        "operational_background_source",
    }
)

RESIDUAL_KEYS = frozenset(
    {
        "general_pressure_identity",
        "constant_density_pressure",
        "vacuum_equation_of_state",
        "constant_density_continuity",
        "reduced_action_match",
        "effective_action_single_representation",
        "friedmann_source_match",
        "power_energy_equation_of_state",
        "power_density_log_slope",
        "fixed_total_energy_pressure",
        "fixed_total_energy_equation_of_state",
        "latent_phase_gap",
        "common_phase_shift_cancellation",
        "local_eom_constant_shift",
        "bare_phase_reparameterization",
    }
)
EXPECTED_RESIDUAL_KEYS = frozenset(
    {
        "general_pressure_identity",
        "constant_density_pressure",
        "vacuum_equation_of_state",
        "constant_density_continuity",
        "reduced_action_match",
        "effective_action_single_representation",
        "friedmann_source_match",
        "power_energy_equation_of_state",
        "power_density_log_slope",
        "fixed_total_energy_pressure",
        "fixed_total_energy_equation_of_state",
        "latent_phase_gap",
        "common_phase_shift_cancellation",
        "local_eom_constant_shift",
        "bare_phase_reparameterization",
    }
)
MUTATION_KEYS = frozenset(
    {
        "wrong_pressure_sign",
        "fixed_total_energy_promoted_to_lambda",
        "quadratic_volume_energy_promoted_to_lambda",
        "wrong_lambda_factor_two",
        "wrong_latent_sign",
        "double_counted_phase_contribution",
        "hidden_bare_term",
        "vacuum_pressure_renamed_cadence_pressure",
    }
)
EXPECTED_MUTATION_KEYS = frozenset(
    {
        "wrong_pressure_sign",
        "fixed_total_energy_promoted_to_lambda",
        "quadratic_volume_energy_promoted_to_lambda",
        "wrong_lambda_factor_two",
        "wrong_latent_sign",
        "double_counted_phase_contribution",
        "hidden_bare_term",
        "vacuum_pressure_renamed_cadence_pressure",
    }
)

REQUIRED_TRUE_FLAGS = (
    "dependency_hashes_exact",
    "dependency_checksums_valid",
    "canonical_dependency_text",
    "upstream_w3_39_verified",
    "upstream_w3_40_verified",
    "upstream_w3_41_verified",
    "operational_background_verified",
    "pressure_roles_distinct",
    "single_driver_semantics_preserved",
    "general_pressure_identity_exact",
    "constant_density_pressure_exact",
    "vacuum_equation_of_state_exact",
    "constant_density_continuity_exact",
    "reduced_action_match_exact",
    "friedmann_source_match_exact",
    "extensive_scaling_unique",
    "fixed_total_energy_rejected_as_lambda",
    "phase_latent_sign_dictionary_exact",
    "potential_shift_nonselection_exact",
    "bare_phase_split_degeneracy_exact",
    "single_representation_no_double_counting",
    "mutation_controls_pass",
    "schema_keysets_exact",
)
EXPECTED_REQUIRED_TRUE_FLAGS = (
    "dependency_hashes_exact",
    "dependency_checksums_valid",
    "canonical_dependency_text",
    "upstream_w3_39_verified",
    "upstream_w3_40_verified",
    "upstream_w3_41_verified",
    "operational_background_verified",
    "pressure_roles_distinct",
    "single_driver_semantics_preserved",
    "general_pressure_identity_exact",
    "constant_density_pressure_exact",
    "vacuum_equation_of_state_exact",
    "constant_density_continuity_exact",
    "reduced_action_match_exact",
    "friedmann_source_match_exact",
    "extensive_scaling_unique",
    "fixed_total_energy_rejected_as_lambda",
    "phase_latent_sign_dictionary_exact",
    "potential_shift_nonselection_exact",
    "bare_phase_split_degeneracy_exact",
    "single_representation_no_double_counting",
    "mutation_controls_pass",
    "schema_keysets_exact",
)
REQUIRED_FALSE_FLAGS = (
    "active_phase_potential_derived",
    "epsilon_star_value_derived",
    "Lambda_value_derived",
    "bare_lambda_zero_derived",
    "foundation_to_operational_matching_derived",
    "phase_offset_identified_with_P_F",
    "phase_offset_identified_with_Pi_F",
    "genesis_energy_source_derived",
    "radiative_stability_controlled",
    "observational_pass",
    "new_parameter_fitted",
)
EXPECTED_REQUIRED_FALSE_FLAGS = (
    "active_phase_potential_derived",
    "epsilon_star_value_derived",
    "Lambda_value_derived",
    "bare_lambda_zero_derived",
    "foundation_to_operational_matching_derived",
    "phase_offset_identified_with_P_F",
    "phase_offset_identified_with_Pi_F",
    "genesis_energy_source_derived",
    "radiative_stability_controlled",
    "observational_pass",
    "new_parameter_fitted",
)
EXPECTED_CLOSURE_FLAG_KEYS = frozenset(
    {
        "dependency_hashes_exact",
        "dependency_checksums_valid",
        "canonical_dependency_text",
        "upstream_w3_39_verified",
        "upstream_w3_40_verified",
        "upstream_w3_41_verified",
        "operational_background_verified",
        "pressure_roles_distinct",
        "single_driver_semantics_preserved",
        "general_pressure_identity_exact",
        "constant_density_pressure_exact",
        "vacuum_equation_of_state_exact",
        "constant_density_continuity_exact",
        "reduced_action_match_exact",
        "friedmann_source_match_exact",
        "extensive_scaling_unique",
        "fixed_total_energy_rejected_as_lambda",
        "phase_latent_sign_dictionary_exact",
        "potential_shift_nonselection_exact",
        "bare_phase_split_degeneracy_exact",
        "single_representation_no_double_counting",
        "mutation_controls_pass",
        "schema_keysets_exact",
        "active_phase_potential_derived",
        "epsilon_star_value_derived",
        "Lambda_value_derived",
        "bare_lambda_zero_derived",
        "foundation_to_operational_matching_derived",
        "phase_offset_identified_with_P_F",
        "phase_offset_identified_with_Pi_F",
        "genesis_energy_source_derived",
        "radiative_stability_controlled",
        "observational_pass",
        "new_parameter_fitted",
        "active_phase_lambda_interface_pass",
    }
)
EXPECTED_REPORT_KEYS = frozenset(
    {
        "schema_version",
        "claim_id",
        "model_version",
        "decision_status",
        "scope",
        "data_role",
        "dependency_hashes",
        "dependency_hashes_exact",
        "upstream_statuses",
        "closure_flags",
        "required_true_flags",
        "required_false_flags",
        "residuals",
        "scaling_dictionary",
        "phase_dictionary",
        "lambda_dictionary",
        "pressure_roles",
        "mutation_residuals",
        "mutation_detection",
        "runtime",
        "direct_files_read",
        "writes_files",
        "source_sha256",
    }
)

HERE = Path(__file__).resolve().parent
COSMOLOGY_DIR = HERE.parent
WORK3_DIR = COSMOLOGY_DIR.parent
GENESIS_DIR = WORK3_DIR / "Genesis_Scenario"
W3_40_DIR = COSMOLOGY_DIR / "Expansion_Relaxation_Causal_Lock"
W3_41_DIR = COSMOLOGY_DIR / "Foundation_Constitutive_Interface"

PREREG_PATH = HERE / "w3_45_active_phase_lambda_interface_preregistration.md"
W3_39_RESULT_PATH = GENESIS_DIR / "w3_39_result.json"
W3_39_CHECKSUM_PATH = GENESIS_DIR / "w3_39_result.sha256"
W3_40_RESULT_PATH = W3_40_DIR / "w3_40_result.json"
W3_40_CHECKSUM_PATH = W3_40_DIR / "w3_40_result.sha256"
W3_41_PREREG_PATH = (
    W3_41_DIR / "w3_41_foundation_constitutive_interface_preregistration.md"
)
W3_41_SOURCE_PATH = (
    W3_41_DIR / "w3_41_foundation_constitutive_interface.py"
)
BACKGROUND_SOURCE_PATH = (
    COSMOLOGY_DIR / "w3_cosmology_operational_geometric_flrw.py"
)
DEPENDENCY_PATHS = {
    "preregistration": PREREG_PATH,
    "w3_39_result": W3_39_RESULT_PATH,
    "w3_39_checksum": W3_39_CHECKSUM_PATH,
    "w3_40_result": W3_40_RESULT_PATH,
    "w3_40_checksum": W3_40_CHECKSUM_PATH,
    "w3_41_preregistration": W3_41_PREREG_PATH,
    "w3_41_source": W3_41_SOURCE_PATH,
    "operational_background_source": BACKGROUND_SOURCE_PATH,
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_lf(path: Path) -> bool:
    raw = path.read_bytes()
    return bool(
        raw
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\r\n" not in raw
        and b"\r" not in raw
        and raw.endswith(b"\n")
    )


def _load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"Expected JSON object: {path}")
    return value


def _checksum_matches(result_path: Path, checksum_path: Path) -> bool:
    parts = checksum_path.read_text(encoding="utf-8").strip().split()
    return bool(
        len(parts) == 2
        and parts[0] == _sha256(result_path)
        and parts[1] == result_path.name
    )


def _symbolic_gate() -> dict[str, object]:
    A, V0, V, c0, G, H, A_dot, N = sp.symbols(
        "A V0 V c0 G H A_dot N",
        positive=True,
    )
    epsilon_star, k, C_cell = sp.symbols(
        "epsilon_star k C_cell",
        positive=True,
    )
    n = sp.Symbol("n", real=True)
    epsilon_of_A = sp.Function("epsilon")(A)

    V_op = V0 * A**3
    E_general = epsilon_of_A * V_op
    P_general = sp.simplify(
        -sp.diff(E_general, A) / sp.diff(V_op, A)
    )
    general_pressure_expected = (
        -epsilon_of_A - A * sp.diff(epsilon_of_A, A) / 3
    )

    E_star = epsilon_star * V_op
    P_star = sp.simplify(-sp.diff(E_star, A) / sp.diff(V_op, A))
    w_star = sp.simplify(P_star / epsilon_star)
    continuity = sp.simplify(
        0 + 3 * (A_dot / A) * (epsilon_star + P_star)
    )

    lambda_phase = 8 * sp.pi * G * epsilon_star / c0**4
    reduced_phase_term = -N * A**3 * epsilon_star
    reduced_lambda_term = (
        -N * A**3 * lambda_phase * c0**4 / (8 * sp.pi * G)
    )
    friedmann_phase = 8 * sp.pi * G * epsilon_star / (3 * c0**2)
    friedmann_lambda = lambda_phase * c0**2 / 3

    E_power = k * V**n
    density_power = sp.simplify(E_power / V)
    pressure_power = sp.simplify(-sp.diff(E_power, V))
    w_power = sp.simplify(pressure_power / density_power)
    density_log_slope = sp.simplify(
        V * sp.diff(density_power, V) / density_power
    )
    extensive_solutions = {
        "constant_density": sp.solve(
            sp.Eq(density_log_slope, 0),
            n,
        ),
        "w_equals_minus_one": sp.solve(
            sp.Eq(w_power, -1),
            n,
        ),
    }

    density_cell = C_cell / V
    pressure_cell = -sp.diff(C_cell, V)
    w_cell = sp.simplify(pressure_cell / density_cell)

    epsilon_U, epsilon_A, shift = sp.symbols(
        "epsilon_U epsilon_A shift",
        real=True,
    )
    latent_L = epsilon_U - epsilon_A
    phase_gap = epsilon_A - epsilon_U
    latent_residual = sp.simplify(phase_gap + latent_L)
    shifted_gap_residual = sp.simplify(
        ((epsilon_A + shift) - (epsilon_U + shift)) - phase_gap
    )

    phi = sp.Symbol("phi", real=True)
    potential = sp.Function("U")
    local_eom_shift_residual = sp.simplify(
        sp.diff(potential(phi) + shift, phi)
        - sp.diff(potential(phi), phi)
    )

    lambda_bare, delta_epsilon = sp.symbols(
        "Lambda_bare delta_epsilon",
        real=True,
    )
    kappa = 8 * sp.pi * G / c0**4
    lambda_effective = lambda_bare + kappa * epsilon_star
    lambda_reparameterized = (
        lambda_bare
        - kappa * delta_epsilon
        + kappa * (epsilon_star + delta_epsilon)
    )
    reduced_split_term = -N * A**3 * (
        lambda_bare * c0**4 / (8 * sp.pi * G)
        + epsilon_star
    )
    reduced_effective_term = (
        -N
        * A**3
        * lambda_effective
        * c0**4
        / (8 * sp.pi * G)
    )

    residuals = {
        "general_pressure_identity": sp.simplify(
            P_general - general_pressure_expected
        ),
        "constant_density_pressure": sp.simplify(
            P_star + epsilon_star
        ),
        "vacuum_equation_of_state": sp.simplify(w_star + 1),
        "constant_density_continuity": continuity,
        "reduced_action_match": sp.simplify(
            reduced_phase_term - reduced_lambda_term
        ),
        "effective_action_single_representation": sp.simplify(
            reduced_split_term - reduced_effective_term
        ),
        "friedmann_source_match": sp.simplify(
            friedmann_phase - friedmann_lambda
        ),
        "power_energy_equation_of_state": sp.simplify(w_power + n),
        "power_density_log_slope": sp.simplify(
            density_log_slope - (n - 1)
        ),
        "fixed_total_energy_pressure": pressure_cell,
        "fixed_total_energy_equation_of_state": w_cell,
        "latent_phase_gap": latent_residual,
        "common_phase_shift_cancellation": shifted_gap_residual,
        "local_eom_constant_shift": local_eom_shift_residual,
        "bare_phase_reparameterization": sp.simplify(
            lambda_reparameterized - lambda_effective
        ),
    }

    P_F = sp.Symbol("P_F", positive=True)
    mutation_residuals = {
        "wrong_pressure_sign": sp.simplify(
            sp.diff(E_star, A) / sp.diff(V_op, A) - P_star
        ),
        "fixed_total_energy_promoted_to_lambda": sp.simplify(
            pressure_cell + density_cell
        ),
        "quadratic_volume_energy_promoted_to_lambda": sp.simplify(
            w_power.subs(n, 2) + 1
        ),
        "wrong_lambda_factor_two": sp.simplify(
            4 * sp.pi * G * epsilon_star / c0**4 - lambda_phase
        ),
        "wrong_latent_sign": sp.simplify(phase_gap - latent_L),
        "double_counted_phase_contribution": sp.simplify(
            lambda_bare + 2 * lambda_phase - lambda_effective
        ),
        "hidden_bare_term": sp.simplify(
            lambda_phase - lambda_effective
        ),
        "vacuum_pressure_renamed_cadence_pressure": sp.simplify(
            P_star - P_F
        ),
    }
    mutation_substitutions = {
        V: sp.Integer(2),
        C_cell: sp.Integer(1),
        epsilon_star: sp.Integer(1),
        epsilon_A: sp.Integer(1),
        epsilon_U: sp.Integer(0),
        c0: sp.Integer(1),
        G: sp.Integer(1),
        lambda_bare: sp.Integer(1),
        P_F: sp.Integer(1),
    }
    mutation_detection = {
        key: sp.simplify(value.subs(mutation_substitutions)) != 0
        for key, value in mutation_residuals.items()
    }

    phase_dictionary = {
        "epsilon_star": "epsilon_A-epsilon_U=-L",
        "positive_Lambda_phase": "L<0__input-requiring activation branch",
        "zero_Lambda_phase": "L=0__neutral phase gap",
        "negative_Lambda_phase": "L>0__release branch",
        "sign_checks": {
            "L_minus_one_gives_positive_Lambda": bool(-(-1) > 0),
            "L_zero_gives_zero_Lambda": bool(-0 == 0),
            "L_plus_one_gives_negative_Lambda": bool(-(1) < 0),
        },
    }

    return {
        "residuals": residuals,
        "extensive_solutions": extensive_solutions,
        "scaling_dictionary": {
            "general_pressure": str(P_general),
            "constant_density_total_energy": str(E_star),
            "constant_density_pressure": str(P_star),
            "constant_density_w": str(w_star),
            "power_density": str(density_power),
            "power_pressure": str(pressure_power),
            "power_w": str(w_power),
            "fixed_total_energy_density": str(density_cell),
            "fixed_total_energy_pressure": str(pressure_cell),
            "fixed_total_energy_w": str(w_cell),
        },
        "phase_dictionary": phase_dictionary,
        "lambda_dictionary": {
            "Lambda_phase": str(lambda_phase),
            "Lambda_effective": str(lambda_effective),
            "reparameterization": (
                "epsilon_star->epsilon_star+delta_epsilon; "
                "Lambda_bare->Lambda_bare-"
                "8*pi*G*delta_epsilon/c0**4"
            ),
            "positive_branch": "epsilon_star>0 => Lambda_phase>0",
            "representation_rule": (
                "phase offset appears once inside Lambda_effective"
            ),
        },
        "mutation_residuals": mutation_residuals,
        "mutation_detection": mutation_detection,
    }


def build_report() -> dict[str, object]:
    actual_hashes = {
        key: _sha256(path) for key, path in DEPENDENCY_PATHS.items()
    }
    dependency_hashes_exact = {
        key: actual_hashes[key] == EXPECTED_HASHES[key]
        for key in EXPECTED_DEPENDENCY_KEYS
    }
    canonical_dependencies = all(
        _canonical_lf(path) for path in DEPENDENCY_PATHS.values()
    )
    checksums_valid = bool(
        _checksum_matches(W3_39_RESULT_PATH, W3_39_CHECKSUM_PATH)
        and _checksum_matches(W3_40_RESULT_PATH, W3_40_CHECKSUM_PATH)
    )

    w3_39 = _read_json(W3_39_RESULT_PATH)
    w3_40 = _read_json(W3_40_RESULT_PATH)
    w3_41_module = _load_module(
        W3_41_SOURCE_PATH,
        "w3_41_dependency_for_w3_45",
    )
    w3_41 = w3_41_module.build_report()
    background_module = _load_module(
        BACKGROUND_SOURCE_PATH,
        "operational_background_dependency_for_w3_45",
    )
    background = background_module.build_report()

    w3_39_verified = bool(
        w3_39.get("status") == "PASS"
        and w3_39.get("scope_status") == W3_39_SCOPE_STATUS
        and w3_39.get("phase_mechanism_status")
        == "OPEN_SIGN_NOT_SELECTED"
        and w3_39["closure_flags"]["latent_sign_classifier_exact"]
        and not w3_39["physical_closure_flags"][
            "phase_free_energy_EOS_derived"
        ]
        and not w3_39["physical_closure_flags"][
            "latent_heat_sign_derived"
        ]
    )
    w3_40_verified = bool(
        w3_40.get("status") == "PASS"
        and w3_40.get("scope_status") == W3_40_SCOPE_STATUS
        and w3_40["semantic_constraints"]["primary_process"]
        == "FOUNDATION_EXPANSION"
        and w3_40["semantic_constraints"]["effect_counting"]
        == "ONE_PRIMARY_DRIVER_WITH_DEPENDENT_RESPONSE__NO_DOUBLE_COUNTING"
    )
    w3_41_verified = bool(
        w3_41.get("status") == "PASS"
        and w3_41.get("scope_status") == W3_41_SCOPE_STATUS
        and w3_41.get("bridge_status")
        == "P_F_EQUALS_Pi_F__CANDIDATE_NOT_DERIVED"
        and not w3_41["physical_closure_flags"][
            "foundation_pressure_equals_mechanical_pressure_derived"
        ]
    )
    pressure_roles = w3_41["pressure_roles"]
    pressure_roles_distinct = bool(
        pressure_roles["roles_distinct"]
        and pressure_roles["P_F"]
        == "cadence-controlling foundation scalar"
        and pressure_roles["Pi_F"]
        == "mechanical generalized pressure conjugate to V_F"
        and pressure_roles["P_th"]
        == "matter-radiation thermodynamic pressure"
    )
    background_verified = bool(
        background.get("decision_status") == BACKGROUND_PASS_STATUS
        and background.get("data_role") == "NO_DATA_READ_OR_FITTED"
        and background["closure_flags"]["conditional_background_pass"]
        and not background["closure_flags"]["Lambda_value_derived"]
        and background.get("writes_files") is False
    )

    symbolic = _symbolic_gate()
    residuals = symbolic["residuals"]
    mutation_residuals = symbolic["mutation_residuals"]
    mutation_detection = symbolic["mutation_detection"]
    all_residuals_zero = all(value == 0 for value in residuals.values())
    extensive_scaling_unique = bool(
        symbolic["extensive_solutions"]["constant_density"] == [1]
        and symbolic["extensive_solutions"]["w_equals_minus_one"] == [1]
    )
    fixed_total_energy_rejected = bool(
        residuals["fixed_total_energy_pressure"] == 0
        and residuals["fixed_total_energy_equation_of_state"] == 0
        and symbolic["scaling_dictionary"]["fixed_total_energy_density"]
        == "C_cell/V"
    )
    phase_signs_exact = bool(
        residuals["latent_phase_gap"] == 0
        and all(symbolic["phase_dictionary"]["sign_checks"].values())
    )
    potential_shift_exact = bool(
        residuals["common_phase_shift_cancellation"] == 0
        and residuals["local_eom_constant_shift"] == 0
    )

    flags = {
        "dependency_hashes_exact": bool(
            frozenset(actual_hashes) == EXPECTED_DEPENDENCY_KEYS
            and all(dependency_hashes_exact.values())
        ),
        "dependency_checksums_valid": checksums_valid,
        "canonical_dependency_text": canonical_dependencies,
        "upstream_w3_39_verified": w3_39_verified,
        "upstream_w3_40_verified": w3_40_verified,
        "upstream_w3_41_verified": w3_41_verified,
        "operational_background_verified": background_verified,
        "pressure_roles_distinct": pressure_roles_distinct,
        "single_driver_semantics_preserved": w3_40_verified,
        "general_pressure_identity_exact": (
            residuals["general_pressure_identity"] == 0
        ),
        "constant_density_pressure_exact": (
            residuals["constant_density_pressure"] == 0
        ),
        "vacuum_equation_of_state_exact": (
            residuals["vacuum_equation_of_state"] == 0
        ),
        "constant_density_continuity_exact": (
            residuals["constant_density_continuity"] == 0
        ),
        "reduced_action_match_exact": (
            residuals["reduced_action_match"] == 0
        ),
        "friedmann_source_match_exact": (
            residuals["friedmann_source_match"] == 0
        ),
        "extensive_scaling_unique": extensive_scaling_unique,
        "fixed_total_energy_rejected_as_lambda": (
            fixed_total_energy_rejected
        ),
        "phase_latent_sign_dictionary_exact": phase_signs_exact,
        "potential_shift_nonselection_exact": potential_shift_exact,
        "bare_phase_split_degeneracy_exact": (
            residuals["bare_phase_reparameterization"] == 0
        ),
        "single_representation_no_double_counting": bool(
            residuals["effective_action_single_representation"] == 0
            and mutation_detection["double_counted_phase_contribution"]
        ),
        "mutation_controls_pass": all(mutation_detection.values()),
        "schema_keysets_exact": False,
        "active_phase_potential_derived": False,
        "epsilon_star_value_derived": False,
        "Lambda_value_derived": False,
        "bare_lambda_zero_derived": False,
        "foundation_to_operational_matching_derived": False,
        "phase_offset_identified_with_P_F": False,
        "phase_offset_identified_with_Pi_F": False,
        "genesis_energy_source_derived": False,
        "radiative_stability_controlled": False,
        "observational_pass": False,
        "new_parameter_fitted": False,
        "active_phase_lambda_interface_pass": False,
    }

    report: dict[str, object] = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "decision_status": "PENDING_SCHEMA_CHECK",
        "scope": (
            "EXACT_CONDITIONAL_ACTIVE_PHASE_TO_EXISTING_LAMBDA_"
            "INTERFACE_AND_NONSELECTION_ONLY"
        ),
        "data_role": "NO_DATA_READ_OR_FITTED",
        "dependency_hashes": actual_hashes,
        "dependency_hashes_exact": dependency_hashes_exact,
        "upstream_statuses": {
            "w3_39": w3_39["scope_status"],
            "w3_40": w3_40["scope_status"],
            "w3_41": w3_41["scope_status"],
            "operational_background": background["decision_status"],
        },
        "closure_flags": flags,
        "required_true_flags": list(REQUIRED_TRUE_FLAGS),
        "required_false_flags": list(REQUIRED_FALSE_FLAGS),
        "residuals": {
            key: str(value) for key, value in residuals.items()
        },
        "scaling_dictionary": symbolic["scaling_dictionary"],
        "phase_dictionary": symbolic["phase_dictionary"],
        "lambda_dictionary": symbolic["lambda_dictionary"],
        "pressure_roles": {
            **pressure_roles,
            "P_star": (
                "negative vacuum stress conjugate to operational volume"
            ),
        },
        "mutation_residuals": {
            key: str(value) for key, value in mutation_residuals.items()
        },
        "mutation_detection": mutation_detection,
        "runtime": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
        "direct_files_read": [
            str(path.relative_to(WORK3_DIR))
            for path in DEPENDENCY_PATHS.values()
        ],
        "writes_files": False,
        "source_sha256": _sha256(Path(__file__).resolve()),
    }

    schema_keysets_exact = bool(
        frozenset(DEPENDENCY_PATHS) == EXPECTED_DEPENDENCY_KEYS
        and frozenset(EXPECTED_HASHES) == EXPECTED_DEPENDENCY_KEYS
        and RESIDUAL_KEYS == EXPECTED_RESIDUAL_KEYS
        and frozenset(residuals) == EXPECTED_RESIDUAL_KEYS
        and MUTATION_KEYS == EXPECTED_MUTATION_KEYS
        and frozenset(mutation_residuals) == EXPECTED_MUTATION_KEYS
        and frozenset(mutation_detection) == EXPECTED_MUTATION_KEYS
        and REQUIRED_TRUE_FLAGS == EXPECTED_REQUIRED_TRUE_FLAGS
        and REQUIRED_FALSE_FLAGS == EXPECTED_REQUIRED_FALSE_FLAGS
        and set(REQUIRED_TRUE_FLAGS).isdisjoint(REQUIRED_FALSE_FLAGS)
        and frozenset(flags) == EXPECTED_CLOSURE_FLAG_KEYS
        and frozenset(report) == EXPECTED_REPORT_KEYS
        and all_residuals_zero
        and "active_phase_lambda_interface_pass"
        not in REQUIRED_TRUE_FLAGS
    )
    flags["schema_keysets_exact"] = schema_keysets_exact
    aggregate_pass = bool(
        all(flags[name] for name in REQUIRED_TRUE_FLAGS)
        and all(not flags[name] for name in REQUIRED_FALSE_FLAGS)
    )
    flags["active_phase_lambda_interface_pass"] = aggregate_pass
    report["decision_status"] = PASS_STATUS if aggregate_pass else "FAIL"
    return report


def main() -> int:
    report = build_report()
    print(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
    )
    return 0 if report["decision_status"] == PASS_STATUS else 2


if __name__ == "__main__":
    raise SystemExit(main())
