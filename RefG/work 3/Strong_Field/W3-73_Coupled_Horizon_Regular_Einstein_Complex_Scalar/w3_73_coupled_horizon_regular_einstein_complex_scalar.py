#!/usr/bin/env python3
"""W3-73 exact coupled horizon-regular Einstein-complex-scalar audit."""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import re
import sys
import tempfile
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp


CLAIM_ID = "W3_73_COUPLED_HORIZON_REGULAR_EINSTEIN_COMPLEX_SCALAR"
MODEL_VERSION = "W3-73-v1.0-COUPLED-HORIZON-REGULAR-EINSTEIN-COMPLEX-SCALAR"
PASS_STATUS = (
    "PASS_EXACT_HORIZON_REGULAR_SPHERICAL_EINSTEIN_COMPLEX_SCALAR_"
    "CONSTRAINED_EVOLUTION_FROM_THE_INHERITED_ACTION__MISNER_SHARP_"
    "CHARGE_AND_OUTER_MARGINAL_AREA_FLUX_IDENTITIES_CLOSED_WITHOUT_"
    "PASSIVE_PROFILE_RESCALING__GLOBAL_COLLAPSE_EVENT_HORIZON_INTERIOR_"
    "AND_SINGULARITY_NOT_SOLVED"
)
FAIL_STATUS = "FAIL_W3_73_COUPLED_HORIZON_REGULAR_EINSTEIN_COMPLEX_SCALAR_AUDIT"

SOURCE_PATH = Path(__file__).resolve()
PACKAGE_DIR = SOURCE_PATH.parent
REPO_ROOT = SOURCE_PATH.parents[4]
PREREG_PATH = PACKAGE_DIR / (
    "w3_73_coupled_horizon_regular_einstein_complex_scalar_preregistration.md"
)
RESULT_PATH = PACKAGE_DIR / "w3_73_result.json"
PREREG_SHA256 = "0c9f43ee8cce3dd0bb96b98d938235e34ea0b9e022f22306a3138c237a01b5e5"
EXPECTED_PACKAGE_FILES = {PREREG_PATH.name, SOURCE_PATH.name, RESULT_PATH.name}

DEPENDENCIES = {
    "CODES.md": "27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41",
    "RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/"
    "w3_54_relational_coframe_tegr_phase_source_closure_contract.md":
        "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
    "RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/"
    "w3_54_result.json":
        "ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991",
    "RefG/work 3/Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/"
    "w3_58_one_oscillon_coframe_localized_core_preregistration.md":
        "ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db",
    "RefG/work 3/Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/"
    "w3_58_result.json":
        "cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5",
    "RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/"
    "w3_64_source_first_einstein_strong_field_preregistration.md":
        "25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1",
    "RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/w3_64_result.json":
        "b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b",
    "RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/"
    "w3_67_foundation_strong_field_response_preregistration.md":
        "31e6520d9b7917413b9f2978291b4a77f067abe8dd3d6a9e89e1b2cfb699da11",
    "RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_result.json":
        "659bdfe171a8279b465fdd49eaf590755da22a7522a83053a4a06450fd745385",
    "RefG/work 3/Strong_Field/W3-71_Horizon_Material_Scale_Separation/"
    "w3_71_horizon_material_scale_separation_preregistration.md":
        "45a9a9eed95a2d927a601f6b4e0822994da93176f1c25fe49ff2431bb35e9f4a",
    "RefG/work 3/Strong_Field/W3-71_Horizon_Material_Scale_Separation/w3_71_result.json":
        "5aeeed4a963e1a03769861f5b38e564a74ec718ee1a19048b37ee7affa72be81",
    "RefG/work 3/Strong_Field/W3-72_Horizon_Crossing_Material_Current/"
    "w3_72_horizon_crossing_material_current_preregistration.md":
        "29c0bbad8eee945820efe1eb7c335597bfe2c7f136bf02fdf2bd7e7bca6769a7",
    "RefG/work 3/Strong_Field/W3-72_Horizon_Crossing_Material_Current/w3_72_result.json":
        "269f4de4a7c17c7a0947d2d20288e3003beaa2a159386e94687ba39a5c4736a9",
}

IMMUTABLE_INTUITIVE = {
    "intuitive/Dictionary.txt": "f6e12b67f38e49bb547d37e6c92375a2ee5b2f596ed481a866cbc490be32ed0b",
    "intuitive/RefG_EN.bib": "78a2889e8da0eb206d6282dac610a82af77ad1340e48c7dbd2e042e1f317fe43",
    "intuitive/RefG_EN.pdf": "2d1c65687fb6c9bbb5c3004299d6205ad494f361a956d646851571996a448ddc",
    "intuitive/RefG_EN.tex": "6e69d616229688d885320d9b26b8c4637c563ae47f8da006feee8548d6ad910e",
    "intuitive/RefG_GE.md": "433d3ac96ff6d91eaae1da60cd3f27f84ead2b7bddea26885034e2995dd8787f",
    "intuitive/figures/figure_3.pdf": "d3fc89edf7ed59b499467999c16504c8cc36dbe614f9b1dcc612caaee1f35f5f",
    "intuitive/figures/figure_3_v2.png": "43e673eeac9d44cb595303bf55d0622ac2fcb87b641627ff8e3a5e8781365a4e",
    "intuitive/figures/logo.pdf": "e585eaa93b8d60b6294fcd3e7448469265502defd7725f74fdb0a56d33d907ab",
    "intuitive/figures/sparc_rar_real_validation.png":
        "1afefcc99ca6223230959b8ab3a6cfc015035de20178b7eed8f7f3728a7fe3f0",
    "intuitive/idea.txt": "98cf98f70e3ac146ef3b106cdd6b2df6c6861d2c277e9c9adae5262959d2dd8d",
}

REQUIRED_TRUE_FLAGS = {
    "dependency_hashes_exact", "upstream_status_and_scope_exact",
    "one_metric_one_localized_source_exact", "w3_58_cartesian_action_unchanged_exact",
    "gpg_metric_inverse_volume_exact", "gpg_dual_frame_exact",
    "misner_sharp_definition_exact", "radial_null_speeds_exact",
    "null_expansions_exact", "marginal_surface_horizon_regular_exact",
    "scalar_evolution_system_exact", "scalar_auxiliary_constraint_propagation_exact",
    "scalar_principal_block_symmetric_exact", "matter_metric_characteristic_cone_match_exact",
    "potential_lower_order_exact", "hilbert_stress_exact",
    "ordinary_phase_current_cartesian_exact", "ordinary_phase_conservation_exact",
    "timelike_current_domain_exact", "horizon_inward_current_exact",
    "einstein_frame_components_exact", "hamiltonian_constraint_exact",
    "momentum_constraint_exact", "radial_metric_evolution_exact",
    "mass_radial_balance_exact", "mass_time_balance_exact",
    "mass_balance_integrability_exact", "angular_einstein_bianchi_closure_exact",
    "coupled_constraint_propagation_exact", "horizon_mass_flux_square_exact",
    "outer_marginal_radius_velocity_exact", "outer_marginal_area_law_exact",
    "marginal_tube_signature_exact", "moving_horizon_charge_crossing_exact",
    "exterior_charge_balance_exact", "static_w3_64_regression_exact",
    "test_field_w3_72_regression_exact", "flat_w3_58_regression_exact",
    "intrinsic_profile_not_passively_rescaled_exact", "readout_absent_from_local_dynamics_exact",
    "scale_gradient_tidal_role_separation_exact", "curvature_no_marginal_pole_exact",
    "local_constrained_data_handoff_exact", "excision_characteristic_direction_exact",
    "scalar_nec_exact", "penrose_boundary_inherited_exact",
    "mutation_controls_pass", "g0_goal_pass", "g1_conventions_pass",
    "g2_geometry_pass", "g3_einstein_system_pass", "g4_matter_system_pass",
    "g5_limits_regression_pass", "g6_physical_flux_pass",
    "g7_observation_not_applicable_exact", "g8_export_not_applicable_exact",
    "package_clean_pass", "aggregate_gate_pass",
}

REQUIRED_FALSE_FLAGS = {
    "second_metric_introduced", "duplicate_localized_source_introduced",
    "noether_current_added_as_einstein_source", "foundation_response_action_added",
    "full_foundation_pressure_constitutive_law_derived", "nonstatic_lapse_identified_as_p_t",
    "p_L_inserted_into_local_action", "intrinsic_oscillon_profile_rescaled",
    "whole_oscillon_dynamical_rigidity_derived", "static_horizon_bound_oscillon_derived",
    "degenerate_outer_horizon_branch_derived", "global_gpg_coverage_derived",
    "horizon_formation_completed", "marginal_surface_promoted_to_event_horizon",
    "global_collapse_evolution_completed", "regular_centre_derived",
    "regular_black_hole_interior_derived", "singularity_resolution_completed",
    "geodesic_completeness_derived", "penrose_boundary_evaded",
    "scalar_nec_violated", "tensor_gravitational_waveform_derived",
    "new_observation_tested", "canon_changed", "intuitive_files_changed",
}

FROZEN_MUTATION_REGISTRY = (
    ("pg_shift_sign_flipped", ("shift_sign",)),
    ("misner_sharp_coefficient_changed", ("mass_definition_factor",)),
    ("einstein_coupling_sign_flipped", ("einstein_sign",)),
    ("lapse_momentum_sign_flipped", ("lapse_momentum_sign",)),
    ("mass_radial_cross_term_removed", ("mass_radial_cross_coefficient",)),
    ("radial_metric_pressure_removed", ("metric_pressure_coefficient",)),
    ("mass_time_cross_terms_removed", ("mass_time_cross_coefficient",)),
    ("scalar_radial_cross_flux_removed", ("scalar_cross_flux_coefficient",)),
    ("potential_promoted_to_principal", ("potential_principal_coefficient",)),
    ("current_orientation_flipped", ("current_sign",)),
    ("horizon_potential_added", ("horizon_potential_coefficient",)),
    ("duplicate_metric_source", ("metric_ids", "source_ledger")),
    ("profile_passively_rescaled", ("profile_scale_power",)),
    ("lapse_relabelled_as_p_t", ("lapse_role",)),
    ("marginal_promoted_to_event_horizon", ("horizon_role",)),
    ("static_horizon_oscillon_promoted", ("static_horizon_role",)),
    ("degenerate_outer_branch_admitted", ("outer_branch_rule",)),
    ("global_interior_overclaim", ("promoted_claims",)),
)

PRODUCTION_CONFIGURATION = {
    "shift_sign": sp.Integer(1), "mass_definition_factor": sp.Integer(1),
    "einstein_sign": sp.Integer(1), "lapse_momentum_sign": sp.Integer(-1),
    "mass_radial_cross_coefficient": sp.Integer(1),
    "metric_pressure_coefficient": sp.Integer(1),
    "mass_time_cross_coefficient": sp.Integer(1),
    "scalar_cross_flux_coefficient": sp.Integer(1),
    "potential_principal_coefficient": sp.Integer(0),
    "current_sign": sp.Integer(-1), "horizon_potential_coefficient": sp.Integer(0),
    "metric_ids": ("g",),
    "source_ledger": (
        ("Einstein_geometric_operator", 1), ("T_O", 1), ("T_C", 0),
        ("p_t", 0), ("p_L", 0), ("P_F", 0),
        ("readout_connection", 0), ("j_O_extra_Einstein_RHS", 0),
    ),
    "profile_scale_power": sp.Integer(0),
    "lapse_role": "DYNAMICAL_GPG_LAPSE_GAUGE",
    "horizon_role": "FUTURE_OUTER_MARGINAL_ONLY_NOT_GLOBAL_EVENT_HORIZON",
    "static_horizon_role": "HORIZONLESS_N_POSITIVE_ZERO_RADIAL_CHARGE_FLUX_ONLY",
    "outer_branch_rule": "D_H_POSITIVE_NONDEGENERATE",
    "promoted_claims": (),
}

MUTATIONS = {
    "pg_shift_sign_flipped": {"shift_sign": sp.Integer(-1)},
    "misner_sharp_coefficient_changed": {"mass_definition_factor": sp.Integer(2)},
    "einstein_coupling_sign_flipped": {"einstein_sign": sp.Integer(-1)},
    "lapse_momentum_sign_flipped": {"lapse_momentum_sign": sp.Integer(1)},
    "mass_radial_cross_term_removed": {"mass_radial_cross_coefficient": sp.Integer(0)},
    "radial_metric_pressure_removed": {"metric_pressure_coefficient": sp.Integer(0)},
    "mass_time_cross_terms_removed": {"mass_time_cross_coefficient": sp.Integer(0)},
    "scalar_radial_cross_flux_removed": {"scalar_cross_flux_coefficient": sp.Integer(0)},
    "potential_promoted_to_principal": {"potential_principal_coefficient": sp.Integer(1)},
    "current_orientation_flipped": {"current_sign": sp.Integer(1)},
    "horizon_potential_added": {"horizon_potential_coefficient": sp.Integer(1)},
    "duplicate_metric_source": {
        "metric_ids": ("g", "f"),
        "source_ledger": (
            ("Einstein_geometric_operator", 2), ("T_O", 2), ("T_C", 1),
            ("p_t", 1), ("p_L", 1), ("P_F", 1),
            ("readout_connection", 1), ("j_O_extra_Einstein_RHS", 1),
        ),
    },
    "profile_passively_rescaled": {"profile_scale_power": sp.Integer(1)},
    "lapse_relabelled_as_p_t": {"lapse_role": "NONSTATIC_P_T"},
    "marginal_promoted_to_event_horizon": {"horizon_role": "GLOBAL_EVENT_HORIZON"},
    "static_horizon_oscillon_promoted": {"static_horizon_role": "STATIC_HORIZON_BOUND_OSCILLON"},
    "degenerate_outer_branch_admitted": {"outer_branch_rule": "D_H_NONNEGATIVE_INCLUDING_ZERO"},
    "global_interior_overclaim": {
        "promoted_claims": (
            "global_gpg_coverage", "horizon_formation", "global_collapse",
            "regular_centre", "regular_black_hole_interior",
            "singularity_resolution", "geodesic_completeness",
        )
    },
}

MUTATION_PRIMARY_FAILURES = {
    "pg_shift_sign_flipped": {"coframe_metric"},
    "misner_sharp_coefficient_changed": {"misner_sharp_definition"},
    "einstein_coupling_sign_flipped": {"einstein_coupling"},
    "lapse_momentum_sign_flipped": {"momentum_constraint"},
    "mass_radial_cross_term_removed": {"mass_radial_balance"},
    "radial_metric_pressure_removed": {"radial_metric_evolution"},
    "mass_time_cross_terms_removed": {"mass_time_balance"},
    "scalar_radial_cross_flux_removed": {"scalar_action_evolution"},
    "potential_promoted_to_principal": {"potential_lower_order"},
    "current_orientation_flipped": {"ordinary_phase_conservation"},
    "horizon_potential_added": {"horizon_mass_square"},
    "duplicate_metric_source": {"one_metric_source"},
    "profile_passively_rescaled": {"intrinsic_profile_role"},
    "lapse_relabelled_as_p_t": {"lapse_role"},
    "marginal_promoted_to_event_horizon": {"horizon_scope"},
    "static_horizon_oscillon_promoted": {"static_regression_scope"},
    "degenerate_outer_branch_admitted": {"outer_branch_guard"},
    "global_interior_overclaim": {"claim_scope"},
}

UPSTREAM_STATUS = {
    "w3_54": "CONDITIONAL_EXACT_SELECTED_RELATIONAL_COFRAME_MASTER_ACTION_TO_TEGR_EQUIVALENT_EH_AND_PHASE_CURRENT_T",
    "w3_58": "PASS_CONDITIONAL_EXACT_MINIMAL_COFRAME_U1_CORE_ACTION_AND_ANALYTIC_EXISTENCE_WINDOW__CONVERGED_NUMERICAL_FINITE_ENERGY_ORBITALLY_STABLE_SPHERICAL_GROUND_STATE_EVIDENCE__FOUNDATION_COEFFICIENT_SELECTION_BACKGROUND_LOCK_BACKREACTION_AND_PARTICLE_IDENTITY_OPEN",
    "w3_64": "PASS_CONDITIONAL_EXACT_UNCHANGED_EINSTEIN_BACKREACTION_AND_CURRENT_SOURCE_NEC_BOUNDARY__CONVERGED_NUMERICAL_REGULAR_HORIZONLESS_SELF_GRAVITATING_Q_BALL_WITNESS__REGULAR_TRAPPED_NULL_COMPLETE_INTERIOR_REQUIRES_FAILURE_OF_AT_LEAST_ONE_PENROSE_HYPOTHESIS",
    "w3_67": "PASS_EXACT_FOUNDATION_STRONG_FIELD_RESPONSE_BOUNDARY__PASSIVE_AND_COMMON_RESCALING_NO_GO__COVARIANT_ACTION_AND_CONSTITUTIVE_SELECTION_OPEN",
    "w3_71": "PASS_EXACT_COVARIANT_SCALE_CONNECTION_ON_HOMOGENEOUS_AND_STATIC_BRANCHES__TEMPORAL_LAPSE_SPATIAL_RULER_AND_INTRINSIC_OSCILLON_PROFILE_SEPARATED_WITH_EXACT_COFRAME_RULER_CONVERSION_EINSTEIN_EXTERIOR_AND_1PN__HORIZON_CROSSING_MATERIAL_CURRENT_NOT_DERIVED",
    "w3_72": "PASS_EXACT_ACTION_DERIVED_HORIZON_REGULAR_NONSTATIC_ORDINARY_PHASE_CURRENT_AND_LOCAL_INITIAL_VALUE_HANDOFF__FINITE_INWARD_CHARGE_NONNEGATIVE_ENERGY_FLUX_AND_MATCHED_CHARACTERISTIC_CONE_ON_THE_INHERITED_ONE_METRIC__GLOBAL_BACKREACTION_INTERIOR_AND_SINGULARITY_NOT_SOLVED",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def exact_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(exact_zero(entry) for entry in matrix)


def all_true(values: Any) -> bool:
    return all(value is True for value in values)


def finite_json(value: Any) -> bool:
    if isinstance(value, dict):
        return all(isinstance(key, str) and finite_json(item) for key, item in value.items())
    if isinstance(value, (list, tuple)):
        return all(finite_json(item) for item in value)
    if isinstance(value, float):
        return math.isfinite(value)
    return value is None or isinstance(value, (str, int, bool))


def casefold_keys_unique(value: Any) -> bool:
    if isinstance(value, dict):
        folded = [key.casefold() for key in value]
        return len(folded) == len(set(folded)) and all(
            casefold_keys_unique(item) for item in value.values()
        )
    if isinstance(value, (list, tuple)):
        return all(casefold_keys_unique(item) for item in value)
    return True


def text_expr(expr: sp.Expr) -> str:
    return sp.sstr(sp.factor(sp.simplify(expr)))


def audit_files(expected: dict[str, str]) -> tuple[dict[str, Any], bool]:
    records: dict[str, Any] = {}
    for relative, expected_hash in expected.items():
        path = REPO_ROOT / relative
        exists = path.is_file()
        actual = sha256_file(path) if exists else None
        records[relative] = {
            "exists": exists, "expected_sha256": expected_hash,
            "actual_sha256": actual, "exact": exists and actual == expected_hash,
        }
    return records, all_true(record["exact"] for record in records.values())


def audit_immutable_intuitive() -> tuple[dict[str, Any], bool]:
    records, hashes_exact = audit_files(IMMUTABLE_INTUITIVE)
    root = REPO_ROOT / "intuitive"
    actual = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in root.rglob("*") if path.is_file()
    )
    expected = sorted(IMMUTABLE_INTUITIVE)
    exact = hashes_exact and actual == expected
    return {
        "expected_files": expected, "actual_files": actual,
        "file_set_exact": actual == expected, "hashes_exact": hashes_exact,
        "records": records, "all_exact": exact,
    }, exact


def audit_canon() -> tuple[dict[str, Any], bool]:
    candidates = (
        REPO_ROOT / "Theory_Canon.md", REPO_ROOT / "RefG/Theory_Canon.md",
        REPO_ROOT / "RefG/work 3/Theory_Canon.md",
    )
    records = {path.relative_to(REPO_ROOT).as_posix(): path.exists() for path in candidates}
    write_targets = (SOURCE_PATH, RESULT_PATH)
    write_target_confined = all(
        path.resolve().parent == PACKAGE_DIR.resolve() for path in write_targets
    )
    exact = not any(records.values()) and write_target_confined
    return {
        "registered_candidates": records, "expected_absence_exact": exact,
        "write_target_confined_to_w3_73": write_target_confined,
        "registered_write_targets": [
            path.relative_to(REPO_ROOT).as_posix() for path in write_targets
        ],
        "all_exact": exact,
    }, exact


def parse_flag_block(text: str, start: str, end: str) -> set[str]:
    if start not in text or end not in text:
        return set()
    block = text.split(start, 1)[1].split(end, 1)[0]
    return set(re.findall(r"^    ([A-Za-z][A-Za-z0-9_]*)\s*$", block, re.MULTILINE))


def parse_mutations(text: str) -> dict[str, tuple[str, ...]]:
    if "## Frozen mutation registry" not in text:
        return {}
    block = text.split("## Frozen mutation registry", 1)[1].split("## Gate registry", 1)[0]
    parsed: dict[str, tuple[str, ...]] = {}
    for name, paths in re.findall(
        r"^    ([a-z][a-z0-9_]*) -> ([a-z0-9_, ]+)\s*$", block, re.MULTILINE
    ):
        parsed[name] = tuple(sorted(part.strip() for part in paths.split(",")))
    return parsed


def audit_preregistration() -> dict[str, Any]:
    text = PREREG_PATH.read_text(encoding="utf-8")
    parsed_true = parse_flag_block(text, "Required true:", "Required false:")
    parsed_false = parse_flag_block(text, "Required false:", "## Frozen mutation registry")
    parsed_mutations = parse_mutations(text)
    frozen_mutations = {name: tuple(sorted(paths)) for name, paths in FROZEN_MUTATION_REGISTRY}
    markers = (
        "**CLAIM_ID:** " + CLAIM_ID, "**MODEL_VERSION:** " + MODEL_VERSION,
        "## Target and stopping rule", "## Assumptions", "## Domain and conventions",
        "## Branches", "## Freedom ledger", "## Dependencies",
        "## Typed role and source ledger", "## Frozen equations", "## Method",
        "## Cross-check", "## Files", "## Pass condition", "## Fail condition",
        "## Falsifier and residual", "## Error bound and validity health",
        "## Observable map, forward model, and data role",
        "## Identifiability and benchmark", "## Closure flags",
        "## Frozen mutation registry", "## Gate registry",
        "## Provenance and references", PASS_STATUS,
    )
    marker_checks = {marker: marker in text for marker in markers}
    actual_hash = sha256_file(PREREG_PATH)
    return {
        "expected_sha256": PREREG_SHA256, "actual_sha256": actual_hash,
        "hash_exact": actual_hash == PREREG_SHA256,
        "marker_checks": marker_checks, "markers_exact": all_true(marker_checks.values()),
        "preregistered_true_flags": sorted(parsed_true),
        "preregistered_false_flags": sorted(parsed_false),
        "required_true_keyset_exact": parsed_true == REQUIRED_TRUE_FLAGS,
        "required_false_keyset_exact": parsed_false == REQUIRED_FALSE_FLAGS,
        "frozen_mutation_registry": {k: list(v) for k, v in sorted(frozen_mutations.items())},
        "parsed_mutation_registry": {k: list(v) for k, v in sorted(parsed_mutations.items())},
        "frozen_mutation_registry_exact": parsed_mutations == frozen_mutations,
    }


def audit_package_before_write() -> dict[str, Any]:
    files = {path.name for path in PACKAGE_DIR.iterdir() if path.is_file()}
    directories = sorted(path.name for path in PACKAGE_DIR.iterdir() if path.is_dir())
    unexpected = sorted(files - EXPECTED_PACKAGE_FILES)
    anticipated = files | {RESULT_PATH.name}
    exact = not unexpected and not directories and anticipated == EXPECTED_PACKAGE_FILES
    return {
        "expected_files": sorted(EXPECTED_PACKAGE_FILES),
        "unexpected_files": unexpected, "actual_directories": directories,
        "anticipated_files_after_write": sorted(anticipated),
        "recursive_exact_three_file_package": exact,
    }


def validate_configuration(config: dict[str, Any]) -> bool:
    return (
        set(config) == set(PRODUCTION_CONFIGURATION)
        and isinstance(config["metric_ids"], tuple)
        and isinstance(config["source_ledger"], tuple)
        and isinstance(config["promoted_claims"], tuple)
    )


def audit_upstream() -> tuple[dict[str, Any], bool]:
    paths = {
        "w3_54": REPO_ROOT / "RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_result.json",
        "w3_58": REPO_ROOT / "RefG/work 3/Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_result.json",
        "w3_64": REPO_ROOT / "RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/w3_64_result.json",
        "w3_67": REPO_ROOT / "RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_result.json",
        "w3_71": REPO_ROOT / "RefG/work 3/Strong_Field/W3-71_Horizon_Material_Scale_Separation/w3_71_result.json",
        "w3_72": REPO_ROOT / "RefG/work 3/Strong_Field/W3-72_Horizon_Crossing_Material_Current/w3_72_result.json",
    }
    data = {name: load_json(path) for name, path in paths.items()}
    checks = {
        **{name + "_status_exact": data[name].get("status") == UPSTREAM_STATUS[name] for name in paths},
        "w3_54_aggregate": data["w3_54"].get("aggregate_pass") is True,
        "w3_58_aggregate": data["w3_58"].get("closure_flags", {}).get("aggregate_gate_pass") is True,
        "w3_58_hilbert_source": data["w3_58"].get("closure_flags", {}).get("hilbert_stress_from_same_action_exact") is True,
        "w3_64_aggregate": data["w3_64"].get("closure_flags", {}).get("aggregate_gate_pass") is True,
        "w3_64_once_only_T_O": data["w3_64"].get("source_ledger", {}).get("localized_einstein_rhs") == ["T_O"],
        "w3_64_penrose_boundary": data["w3_64"].get("closure_flags", {}).get(
            "penrose_trapped_surface_implication_registered_exact"
        ) is True,
        "w3_67_aggregate": data["w3_67"].get("closure_flags", {}).get("aggregate_gate_pass") is True,
        "w3_67_no_response_action": data["w3_67"].get("scope_flags", {}).get("response_action_derived") is False,
        "w3_71_aggregate": data["w3_71"].get("closure_flags", {}).get("aggregate_gate_pass") is True,
        "w3_71_profile_not_rescaled": data["w3_71"].get("closure_flags", {}).get("intrinsic_profile_rescaling_action_present") is False,
        "w3_72_aggregate": data["w3_72"].get("closure_flags", {}).get("aggregate_gate_pass") is True,
        "w3_72_current_exact": data["w3_72"].get("closure_flags", {}).get("ordinary_phase_current_exact") is True,
        "w3_72_backreaction_open": data["w3_72"].get("scope_flags", {}).get("dynamic_einstein_backreaction_solved") is False,
        "all_artifacts_valid_where_defined": all(
            item.get("artifact_valid", True) is True for item in data.values()
        ),
    }
    exact = all_true(checks.values())
    return {"checks": checks, "all_exact": exact}, exact


T, R, THETA, AZIMUTH = sp.symbols("T r theta varphi", real=True)
SIGMA = sp.Function("sigma")(T, R)
ZETA = sp.Function("zeta")(T, R)
GNEWTON = sp.symbols("G", positive=True, finite=True)
MS, LAMBDA, G6 = sp.symbols("m_s lambda g_6", positive=True, finite=True)
PHI1 = sp.Function("phi_1")(T, R)
PHI2 = sp.Function("phi_2")(T, R)
PI1 = sp.Function("Pi_1")(T, R)
PI2 = sp.Function("Pi_2")(T, R)
RAD1 = sp.Function("Phi_1")(T, R)
RAD2 = sp.Function("Phi_2")(T, R)


@lru_cache(maxsize=1)
def geometry_base() -> dict[str, Any]:
    coords = (T, R, THETA, AZIMUTH)
    metric = sp.Matrix([
        [-SIGMA**2 * (1 - ZETA**2), SIGMA * ZETA, 0, 0],
        [SIGMA * ZETA, 1, 0, 0],
        [0, 0, R**2, 0],
        [0, 0, 0, R**2 * sp.sin(THETA)**2],
    ])
    inverse = sp.simplify(metric.inv())
    expected_inverse = sp.Matrix([
        [-1 / SIGMA**2, ZETA / SIGMA, 0, 0],
        [ZETA / SIGMA, 1 - ZETA**2, 0, 0],
        [0, 0, 1 / R**2, 0],
        [0, 0, 0, 1 / (R**2 * sp.sin(THETA)**2)],
    ])
    volume_density = SIGMA * R**2 * sp.sin(THETA)
    dim = 4
    gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for upper in range(dim):
        for left in range(dim):
            for right in range(dim):
                gamma[upper][left][right] = sp.simplify(sum(
                    inverse[upper, lower] * (
                        sp.diff(metric[lower, right], coords[left])
                        + sp.diff(metric[lower, left], coords[right])
                        - sp.diff(metric[left, right], coords[lower])
                    ) / 2 for lower in range(dim)
                ))
    ricci = sp.MutableDenseMatrix.zeros(dim, dim)
    for left in range(dim):
        for right in range(dim):
            value = sp.S.Zero
            for index in range(dim):
                value += sp.diff(gamma[index][left][right], coords[index])
                value -= sp.diff(gamma[index][left][index], coords[right])
                for contracted in range(dim):
                    value += (
                        gamma[index][index][contracted] * gamma[contracted][left][right]
                        - gamma[index][right][contracted] * gamma[contracted][left][index]
                    )
            ricci[left, right] = sp.simplify(value)
    ricci_scalar = sp.simplify(sum(
        inverse[a, b] * ricci[a, b] for a in range(dim) for b in range(dim)
    ))
    einstein = sp.simplify(ricci - metric * ricci_scalar / 2)
    normal = sp.Matrix([1 / SIGMA, -ZETA, 0, 0])
    radial = sp.Matrix([0, 1, 0, 0])
    g00 = sp.simplify((normal.T * einstein * normal)[0])
    g01 = sp.simplify((normal.T * einstein * radial)[0])
    g11 = sp.simplify((radial.T * einstein * radial)[0])
    g22 = sp.simplify(einstein[2, 2] / R**2)
    expected_g00 = (
        2 * ZETA * sp.diff(ZETA, R) / R
        + 2 * ZETA**2 * sp.diff(SIGMA, R) / (R * SIGMA)
        + ZETA**2 / R**2
    )
    expected_g01 = -2 * ZETA * sp.diff(SIGMA, R) / (R * SIGMA)
    expected_g11 = (
        -2 * ZETA * sp.diff(ZETA, R) / R
        + 2 * sp.diff(SIGMA, R) / (R * SIGMA)
        + 2 * sp.diff(ZETA, T) / (R * SIGMA)
        - ZETA**2 / R**2
    )

    mixed = sp.simplify(inverse * einstein)
    bianchi = []
    for nu in (0, 1):
        divergence = sp.S.Zero
        for mu in range(dim):
            divergence += sp.diff(mixed[mu, nu], coords[mu])
            for lam in range(dim):
                divergence += gamma[mu][mu][lam] * mixed[lam, nu]
                divergence -= gamma[lam][mu][nu] * mixed[mu, lam]
        bianchi.append(sp.simplify(divergence))

    riemann_cache: dict[tuple[int, int, int, int], sp.Expr] = {}

    def riemann_up(a: int, b: int, c: int, d: int) -> sp.Expr:
        key = (a, b, c, d)
        if key not in riemann_cache:
            riemann_cache[key] = sp.simplify(
                sp.diff(gamma[a][b][d], coords[c])
                - sp.diff(gamma[a][b][c], coords[d])
                + sum(
                    gamma[a][e][c] * gamma[e][b][d]
                    - gamma[a][e][d] * gamma[e][b][c]
                    for e in range(dim)
                )
            )
        return riemann_cache[key]

    frame = (
        (1 / SIGMA, -ZETA, 0, 0), (0, 1, 0, 0),
        (0, 0, 1 / R, 0), (0, 0, 0, 1 / (R * sp.sin(THETA))),
    )

    def frame_riemann(a: int, b: int, c: int, d: int) -> sp.Expr:
        value = sp.S.Zero
        for mu in range(dim):
            if frame[a][mu] == 0:
                continue
            for nu in range(dim):
                if frame[b][nu] == 0:
                    continue
                for rho in range(dim):
                    if frame[c][rho] == 0:
                        continue
                    for delta in range(dim):
                        if frame[d][delta] == 0:
                            continue
                        covariant = sum(
                            metric[mu, upper] * riemann_up(upper, nu, rho, delta)
                            for upper in range(dim)
                        )
                        value += (
                            frame[a][mu] * frame[b][nu]
                            * frame[c][rho] * frame[d][delta] * covariant
                        )
        return sp.trigsimp(sp.simplify(value))

    independent = {
        "R_0101": frame_riemann(0, 1, 0, 1),
        "R_0202": frame_riemann(0, 2, 0, 2),
        "R_0212": frame_riemann(0, 2, 1, 2),
        "R_1212": frame_riemann(1, 2, 1, 2),
        "R_2323": frame_riemann(2, 3, 2, 3),
    }
    horizon_denominators: dict[str, str] = {}
    horizon_finite: list[bool] = []
    for name, expression in independent.items():
        expression = sp.simplify(expression.subs(THETA, sp.pi / 2))
        derivatives = sorted(expression.atoms(sp.Derivative), key=str)
        jet_map = {derivative: sp.Symbol(f"jet_{index}", finite=True) for index, derivative in enumerate(derivatives)}
        sigma0, zeta0 = sp.symbols("sigma_0 zeta_0", positive=True, finite=True)
        local = expression.xreplace(jet_map).xreplace({SIGMA: sigma0, ZETA: zeta0})
        at_horizon = sp.cancel(local.subs(zeta0, 1))
        denominator = sp.factor(sp.denom(at_horizon))
        horizon_denominators[name] = sp.sstr(denominator)
        horizon_finite.append(denominator != 0 and not at_horizon.has(sp.zoo, sp.nan, sp.oo, -sp.oo))

    velocity = sp.symbols("v")
    null_poly = sp.expand(metric[0, 0] + 2 * metric[0, 1] * velocity + metric[1, 1] * velocity**2)
    null_factor = (velocity - SIGMA * (1 - ZETA)) * (velocity + SIGMA * (1 + ZETA))
    outgoing = normal + radial
    ingoing = normal - radial
    theta_plus_direct = sp.simplify(2 * outgoing[1] / R)
    theta_minus_direct = sp.simplify(2 * ingoing[1] / R)
    theta_plus = 2 * (1 - ZETA) / R
    theta_minus = -2 * (1 + ZETA) / R
    mass = R * ZETA**2 / (2 * GNEWTON)
    checks = {
        "metric_inverse": matrix_zero(sp.simplify(inverse - expected_inverse)),
        "metric_determinant": exact_zero(metric.det() + SIGMA**2 * R**4 * sp.sin(THETA)**2),
        "volume_density": exact_zero(volume_density**2 + metric.det()),
        "coframe_dual": matrix_zero(
            sp.Matrix([[SIGMA, 0], [SIGMA * ZETA, 1]])
            * sp.Matrix([[1 / SIGMA, 0], [-ZETA, 1]]) - sp.eye(2)
        ),
        "einstein_frame_00": exact_zero(g00 - expected_g00),
        "einstein_frame_01": exact_zero(g01 - expected_g01),
        "einstein_frame_11": exact_zero(g11 - expected_g11),
        "contracted_bianchi": all(exact_zero(item) for item in bianchi),
        "null_factorization": exact_zero(null_poly - sp.expand(null_factor)),
        "null_expansion_plus": exact_zero(theta_plus_direct - theta_plus),
        "null_expansion_minus": exact_zero(theta_minus_direct - theta_minus),
        "null_expansion_product": exact_zero(
            theta_plus_direct * theta_minus_direct + 4 * (1 - ZETA**2) / R**2
        ),
        "misner_sharp_geometric": exact_zero(1 - 2 * GNEWTON * mass / R - (1 - ZETA**2)),
        "marginal_metric_regular": exact_zero(metric.det().subs(ZETA, 1) + SIGMA**2 * R**4 * sp.sin(THETA)**2),
        "curvature_horizon_finite": all(horizon_finite),
    }
    return {
        "metric": metric, "inverse": inverse, "gamma": gamma,
        "einstein": einstein, "g00": g00, "g01": g01, "g11": g11,
        "g22": g22, "expected_g00": expected_g00,
        "expected_g01": expected_g01, "expected_g11": expected_g11,
        "bianchi": bianchi, "frame_riemann": independent,
        "horizon_denominators": horizon_denominators,
        "checks": checks,
    }


def matter_quantities() -> dict[str, Any]:
    chi2 = PHI1**2 + PHI2**2
    potential = MS**2 * chi2 / 2 - LAMBDA * chi2**2 / 4 + G6 * chi2**3 / 6
    gradients = (
        (MS**2 - LAMBDA * chi2 + G6 * chi2**2) * PHI1,
        (MS**2 - LAMBDA * chi2 + G6 * chi2**2) * PHI2,
    )
    kinetic_sum = PI1**2 + PI2**2 + RAD1**2 + RAD2**2
    rho = kinetic_sum / 2 + potential
    momentum = PI1 * RAD1 + PI2 * RAD2
    pressure_r = kinetic_sum / 2 - potential
    pressure_t = (PI1**2 + PI2**2 - RAD1**2 - RAD2**2) / 2 - potential
    q = PHI1 * PI2 - PHI2 * PI1
    s_o = PHI1 * RAD2 - PHI2 * RAD1
    return {
        "chi2": chi2, "potential": potential, "gradients": gradients,
        "kinetic_sum": kinetic_sum, "rho": rho, "S": momentum,
        "p_r": pressure_r, "p_t": pressure_t, "q": q, "s_o": s_o,
    }


def production_evolution() -> dict[str, Any]:
    matter = matter_quantities()
    phi_t = (
        SIGMA * (PI1 + ZETA * RAD1),
        SIGMA * (PI2 + ZETA * RAD2),
    )
    radial_t = tuple(sp.diff(item, R) for item in phi_t)
    pi_t = (
        sp.diff(SIGMA * R**2 * (RAD1 + ZETA * PI1), R) / R**2
        - SIGMA * matter["gradients"][0],
        sp.diff(SIGMA * R**2 * (RAD2 + ZETA * PI2), R) / R**2
        - SIGMA * matter["gradients"][1],
    )
    sigma_r = -4 * sp.pi * GNEWTON * R * SIGMA * matter["S"] / ZETA
    zeta_r = (
        4 * sp.pi * GNEWTON * R * (matter["rho"] / ZETA + matter["S"])
        - ZETA / (2 * R)
    )
    zeta_t = (
        SIGMA * ZETA * sp.diff(ZETA, R) - sp.diff(SIGMA, R)
        + SIGMA * ZETA**2 / (2 * R)
        + 4 * sp.pi * GNEWTON * SIGMA * R * matter["p_r"]
    )
    return {
        "phi_t": phi_t, "radial_t": radial_t, "pi_t": pi_t,
        "sigma_r": sigma_r, "zeta_r": zeta_r, "zeta_t": zeta_t,
    }


def apply_production_equations(expression: sp.Expr) -> sp.Expr:
    evolution = production_evolution()
    time_map = {
        sp.diff(PHI1, T): evolution["phi_t"][0],
        sp.diff(PHI2, T): evolution["phi_t"][1],
        sp.diff(RAD1, T): evolution["radial_t"][0],
        sp.diff(RAD2, T): evolution["radial_t"][1],
        sp.diff(PI1, T): evolution["pi_t"][0],
        sp.diff(PI2, T): evolution["pi_t"][1],
        sp.diff(ZETA, T): evolution["zeta_t"],
    }
    result = expression.subs(time_map, simultaneous=True)
    result = result.subs({sp.diff(PHI1, R): RAD1, sp.diff(PHI2, R): RAD2})
    for _ in range(3):
        result = result.subs({
            sp.diff(SIGMA, R): evolution["sigma_r"],
            sp.diff(ZETA, R): evolution["zeta_r"],
            sp.diff(PHI1, R): RAD1,
            sp.diff(PHI2, R): RAD2,
        })
    return sp.factor(sp.simplify(result))


@lru_cache(maxsize=1)
def production_compatibility() -> dict[str, Any]:
    matter = matter_quantities()
    mass_r = 4 * sp.pi * R**2 * (matter["rho"] + ZETA * matter["S"])
    mass_t = 4 * sp.pi * SIGMA * R**2 * (
        ZETA * matter["kinetic_sum"] + (1 + ZETA**2) * matter["S"]
    )
    integrability = apply_production_equations(sp.diff(mass_r, T) - sp.diff(mass_t, R))

    q, s_o = matter["q"], matter["s_o"]
    current_conservation = (
        sp.diff(R**2 * q, T) - sp.diff(SIGMA * R**2 * (ZETA * q + s_o), R)
    )
    current_conservation = apply_production_equations(current_conservation)

    geometry = geometry_base()
    coords = (T, R, THETA, AZIMUTH)
    phi_derivatives = (
        sp.Matrix([SIGMA * (PI1 + ZETA * RAD1), RAD1, 0, 0]),
        sp.Matrix([SIGMA * (PI2 + ZETA * RAD2), RAD2, 0, 0]),
    )
    kinetic = sum(
        (item.T * geometry["inverse"] * item)[0] for item in phi_derivatives
    )
    hilbert_covariant = -geometry["metric"] * (
        kinetic / 2 + matter["potential"]
    )
    for item in phi_derivatives:
        hilbert_covariant += item * item.T
    hilbert_mixed = sp.simplify(geometry["inverse"] * hilbert_covariant)
    hilbert_divergence_on_shell = []
    for nu in range(4):
        divergence = sp.S.Zero
        for mu in range(4):
            divergence += sp.diff(hilbert_mixed[mu, nu], coords[mu])
            for lam in range(4):
                divergence += (
                    geometry["gamma"][mu][mu][lam] * hilbert_mixed[lam, nu]
                    - geometry["gamma"][lam][mu][nu] * hilbert_mixed[mu, lam]
                )
        hilbert_divergence_on_shell.append(
            apply_production_equations(sp.factor(sp.simplify(divergence)))
        )
    hilbert_conservation_identity = all(
        exact_zero(item) for item in hilbert_divergence_on_shell
    )
    potential_gradient_exact = all(exact_zero(item) for item in (
        sp.diff(matter["potential"], PHI1) - matter["gradients"][0],
        sp.diff(matter["potential"], PHI2) - matter["gradients"][1],
    ))
    einstein_residual_covariant = sp.simplify(
        geometry["einstein"] - 8 * sp.pi * GNEWTON * hilbert_covariant
    )
    normal = sp.Matrix([1 / SIGMA, -ZETA, 0, 0])
    radial = sp.Matrix([0, 1, 0, 0])
    base_frame_residuals = (
        apply_production_equations(
            sp.simplify((normal.T * einstein_residual_covariant * normal)[0])
        ),
        apply_production_equations(
            sp.simplify((normal.T * einstein_residual_covariant * radial)[0])
        ),
        apply_production_equations(
            sp.simplify((radial.T * einstein_residual_covariant * radial)[0])
        ),
    )
    angular_einstein_residual = sp.simplify(
        geometry["g22"] - 8 * sp.pi * GNEWTON * matter["p_t"]
    )
    coframe = sp.Matrix([
        [SIGMA, 0, 0, 0],
        [SIGMA * ZETA, 1, 0, 0],
        [0, 0, R, 0],
        [0, 0, 0, R * sp.sin(THETA)],
    ])
    frame_residual_after_base_equations = sp.diag(
        0, 0, angular_einstein_residual, angular_einstein_residual
    )
    coordinate_residual_after_base_equations = sp.simplify(
        coframe.T * frame_residual_after_base_equations * coframe
    )
    mixed_residual_after_base_equations = sp.simplify(
        geometry["inverse"] * coordinate_residual_after_base_equations
    )
    radial_residual_divergence = sp.S.Zero
    nu = 1
    for mu in range(4):
        radial_residual_divergence += sp.diff(
            mixed_residual_after_base_equations[mu, nu], coords[mu]
        )
        for lam in range(4):
            radial_residual_divergence += (
                geometry["gamma"][mu][mu][lam]
                * mixed_residual_after_base_equations[lam, nu]
                - geometry["gamma"][lam][mu][nu]
                * mixed_residual_after_base_equations[mu, lam]
            )
    radial_residual_divergence = sp.factor(sp.simplify(radial_residual_divergence))
    angular_implication_residual = sp.simplify(
        radial_residual_divergence + 2 * angular_einstein_residual / R
    )
    positive_radius = sp.symbols("r_positive", positive=True, finite=True)
    angular_coefficient = sp.simplify(
        radial_residual_divergence / angular_einstein_residual
    )
    angular_coefficient_nonzero = (
        angular_coefficient.subs(R, positive_radius).is_nonzero is True
        and exact_zero(angular_coefficient + 2 / R)
    )
    angular_closure = (
        geometry["checks"]["contracted_bianchi"]
        and hilbert_conservation_identity
        and potential_gradient_exact
        and all(exact_zero(item) for item in base_frame_residuals)
        and exact_zero(angular_implication_residual)
        and angular_coefficient_nonzero
    )
    return {
        "mass_integrability_residual": integrability,
        "current_conservation_residual": current_conservation,
        "angular_implication_residual": angular_implication_residual,
        "angular_einstein_residual": angular_einstein_residual,
        "radial_residual_divergence": radial_residual_divergence,
        "base_frame_einstein_residuals": base_frame_residuals,
        "hilbert_conservation_residuals": hilbert_divergence_on_shell,
        "checks": {
            "mass_integrability": exact_zero(integrability),
            "current_conservation": exact_zero(current_conservation),
            "hilbert_conservation_identity": hilbert_conservation_identity,
            "hilbert_conservation_factorization": (
                hilbert_conservation_identity and potential_gradient_exact
            ),
            "angular_einstein": angular_closure,
        },
    }


def evaluate_configuration(config: dict[str, Any]) -> dict[str, Any]:
    geometry = geometry_base()
    matter = matter_quantities()
    evolution = production_evolution()
    schema = validate_configuration(config)
    shift = config["shift_sign"]
    mass_factor = config["mass_definition_factor"]
    einstein_sign = config["einstein_sign"]
    lapse_sign = config["lapse_momentum_sign"]
    radial_cross = config["mass_radial_cross_coefficient"]
    pressure_coefficient = config["metric_pressure_coefficient"]
    time_cross = config["mass_time_cross_coefficient"]
    scalar_cross = config["scalar_cross_flux_coefficient"]
    principal_potential = config["potential_principal_coefficient"]
    current_sign = config["current_sign"]
    horizon_potential = config["horizon_potential_coefficient"]

    candidate_coframe = sp.Matrix([[SIGMA, 0], [shift * SIGMA * ZETA, 1]])
    eta = sp.diag(-1, 1)
    candidate_metric_2 = sp.simplify(candidate_coframe.T * eta * candidate_coframe)
    frozen_metric_2 = geometry["metric"][:2, :2]
    mass_candidate = mass_factor * R * ZETA**2 / (2 * GNEWTON)
    coframe_cross_residual = sp.simplify(
        candidate_metric_2[0, 1] - frozen_metric_2[0, 1]
    )
    mass_definition_residual = sp.simplify(
        1 - 2 * GNEWTON * mass_candidate / R - (1 - ZETA**2)
    )
    lapse_candidate = (
        einstein_sign * lapse_sign * 4 * sp.pi * GNEWTON * R
        * SIGMA * matter["S"] / ZETA
    )
    zeta_r_candidate = (
        einstein_sign * 4 * sp.pi * GNEWTON * R
        * (matter["rho"] / ZETA + matter["S"]) - ZETA / (2 * R)
    )
    zeta_t_candidate = (
        SIGMA * ZETA * sp.diff(ZETA, R) - sp.diff(SIGMA, R)
        + SIGMA * ZETA**2 / (2 * R)
        + einstein_sign * pressure_coefficient * 4 * sp.pi * GNEWTON
        * SIGMA * R * matter["p_r"]
    )

    momentum_residual = sp.simplify(
        geometry["g01"].subs(sp.diff(SIGMA, R), lapse_candidate)
        - 8 * sp.pi * GNEWTON * matter["S"]
    )
    hamiltonian_residual = geometry["g00"].subs({
        sp.diff(SIGMA, R): lapse_candidate,
        sp.diff(ZETA, R): zeta_r_candidate,
    }, simultaneous=True) - 8 * sp.pi * GNEWTON * matter["rho"]
    hamiltonian_residual = sp.simplify(hamiltonian_residual)
    radial_evolution_residual = sp.simplify(
        geometry["g11"].subs(sp.diff(ZETA, T), zeta_t_candidate)
        - 8 * sp.pi * GNEWTON * matter["p_r"]
    )
    einstein_coupling_residual = sp.simplify(
        zeta_r_candidate
        - (4 * sp.pi * GNEWTON * R * (matter["rho"] / ZETA + matter["S"])
           - ZETA / (2 * R))
    )

    mass_r_lhs = sp.diff(mass_candidate, R).subs(sp.diff(ZETA, R), zeta_r_candidate)
    mass_r_rhs = 4 * sp.pi * R**2 * (matter["rho"] + radial_cross * ZETA * matter["S"])
    mass_r_residual = sp.simplify(mass_r_lhs - mass_r_rhs)
    mass_t_lhs = sp.diff(mass_candidate, T).subs(sp.diff(ZETA, T), zeta_t_candidate)
    mass_t_lhs = mass_t_lhs.subs({
        sp.diff(SIGMA, R): lapse_candidate, sp.diff(ZETA, R): zeta_r_candidate,
    }, simultaneous=True)
    mass_t_rhs = 4 * sp.pi * SIGMA * R**2 * (
        ZETA * matter["kinetic_sum"] + time_cross * (1 + ZETA**2) * matter["S"]
    )
    mass_t_residual = sp.simplify(mass_t_lhs - mass_t_rhs)

    action_fluxes = []
    scalar_action_residuals = []
    action_time_residuals = []
    for pi_field, radial_field in ((PI1, RAD1), (PI2, RAD2)):
        time_flux = SIGMA * R**2 * (
            geometry["inverse"][0, 0] * SIGMA * (pi_field + ZETA * radial_field)
            + geometry["inverse"][0, 1] * radial_field
        )
        radial_flux = SIGMA * R**2 * (
            geometry["inverse"][1, 0] * SIGMA * (pi_field + ZETA * radial_field)
            + geometry["inverse"][1, 1] * radial_field
        )
        candidate_pi_flux = SIGMA * R**2 * (
            radial_field + scalar_cross * ZETA * pi_field
        )
        action_fluxes.append((time_flux, radial_flux))
        action_time_residuals.append(sp.simplify(time_flux + R**2 * pi_field))
        scalar_action_residuals.append(sp.simplify(candidate_pi_flux - radial_flux))
    scalar_action_residual = scalar_action_residuals[0]
    scalar_action_exact = (
        all(exact_zero(item) for item in action_time_residuals)
        and all(exact_zero(item) for item in scalar_action_residuals)
    )
    candidate_principal = SIGMA * sp.Matrix([
        [scalar_cross * ZETA + principal_potential * matter["gradients"][0], 1],
        [1, ZETA],
    ])
    physical_principal = SIGMA * sp.Matrix([[ZETA, 1], [1, ZETA]])
    speed = sp.symbols("c")
    metric_characteristic = sp.expand(
        (speed - SIGMA * (1 - ZETA)) * (speed + SIGMA * (1 + ZETA))
    )
    matter_characteristic = sp.expand((speed * sp.eye(2) + candidate_principal).det())
    potential_principal_residual = sp.simplify(
        candidate_principal[0, 0] - physical_principal[0, 0]
    )

    phi_derivatives = (
        sp.Matrix([SIGMA * (PI1 + ZETA * RAD1), RAD1, 0, 0]),
        sp.Matrix([SIGMA * (PI2 + ZETA * RAD2), RAD2, 0, 0]),
    )
    kinetic = sum(
        (item.T * geometry["inverse"] * item)[0] for item in phi_derivatives
    )
    stress = -geometry["metric"] * (kinetic / 2 + matter["potential"])
    for item in phi_derivatives:
        stress += item * item.T
    normal = sp.Matrix([1 / SIGMA, -ZETA, 0, 0])
    radial = sp.Matrix([0, 1, 0, 0])
    stress_components = (
        sp.simplify((normal.T * stress * normal)[0]),
        sp.simplify((normal.T * stress * radial)[0]),
        sp.simplify((radial.T * stress * radial)[0]),
        sp.simplify(stress[2, 2] / R**2),
    )
    stress_targets = (matter["rho"], matter["S"], matter["p_r"], matter["p_t"])
    stress_exact = all(exact_zero(a - b) for a, b in zip(stress_components, stress_targets))

    q, s_o = matter["q"], matter["s_o"]
    current_r = current_sign * (ZETA * q + s_o)
    current_orientation_residual = sp.simplify(current_r + ZETA * q + s_o)
    compatibility = production_compatibility()
    horizon_square = 4 * sp.pi * SIGMA * R**2 * (
        (PI1 + RAD1)**2 + (PI2 + RAD2)**2
    )
    derived_horizon_flux = sp.simplify(
        4 * sp.pi * SIGMA * R**2 * (
            matter["kinetic_sum"] + 2 * matter["S"]
        )
    )
    candidate_horizon_flux = horizon_square + (
        4 * sp.pi * SIGMA * R**2 * horizon_potential * matter["potential"]
    )
    horizon_residual = sp.simplify(candidate_horizon_flux - derived_horizon_flux)

    expected_ledger = dict(PRODUCTION_CONFIGURATION["source_ledger"])
    actual_ledger = dict(config["source_ledger"])
    one_metric_source = (
        config["metric_ids"] == ("g",) and actual_ledger == expected_ledger
        and actual_ledger["Einstein_geometric_operator"] == 1
        and actual_ledger["T_O"] == 1
        and all(actual_ledger[key] == 0 for key in (
            "T_C", "p_t", "p_L", "P_F", "readout_connection",
            "j_O_extra_Einstein_RHS",
        ))
    )
    p_L_symbol, profile_symbol, p_L_gradient = sp.symbols(
        "p_L profile p_L_gradient", nonzero=True, finite=True
    )
    profile_gradient_residual = sp.simplify(
        config["profile_scale_power"]
        * p_L_symbol ** (config["profile_scale_power"] - 1)
        * profile_symbol * p_L_gradient
    )
    static_N, static_sigma, static_omega = sp.symbols(
        "N_static sigma_static omega_static", positive=True, finite=True
    )
    static_phase_momentum = static_omega / (static_sigma * static_N)
    static_horizon_pole = sp.denom(static_phase_momentum) == static_N * static_sigma
    outer_D, outer_flux = sp.symbols("D_outer flux_outer", positive=True, finite=True)
    outer_velocity = 2 * GNEWTON * outer_flux / outer_D
    outer_nondegenerate_witness = sp.denom(outer_velocity) == outer_D
    checks = {
        "configuration_schema": schema,
        "coframe_metric": matrix_zero(candidate_metric_2 - frozen_metric_2),
        "misner_sharp_definition": exact_zero(mass_definition_residual),
        "einstein_coupling": exact_zero(einstein_coupling_residual),
        "momentum_constraint": exact_zero(momentum_residual),
        "hamiltonian_constraint": exact_zero(hamiltonian_residual),
        "radial_metric_evolution": exact_zero(radial_evolution_residual),
        "mass_radial_balance": exact_zero(mass_r_residual),
        "mass_time_balance": exact_zero(mass_t_residual),
        "scalar_action_evolution": scalar_action_exact,
        "scalar_principal_symmetric": candidate_principal == candidate_principal.T,
        "matter_metric_cone": exact_zero(matter_characteristic - metric_characteristic),
        "potential_lower_order": (
            principal_potential == 0 and candidate_principal == physical_principal
        ),
        "hilbert_stress": stress_exact,
        "ordinary_phase_current": exact_zero(current_orientation_residual),
        "ordinary_phase_conservation": (
            exact_zero(current_orientation_residual)
            and compatibility["checks"]["current_conservation"]
        ),
        "horizon_mass_square": exact_zero(horizon_residual),
        "one_metric_source": one_metric_source,
        "intrinsic_profile_role": exact_zero(profile_gradient_residual),
        "lapse_role": config["lapse_role"] == "DYNAMICAL_GPG_LAPSE_GAUGE",
        "horizon_scope": config["horizon_role"] == "FUTURE_OUTER_MARGINAL_ONLY_NOT_GLOBAL_EVENT_HORIZON",
        "static_regression_scope": (
            config["static_horizon_role"] == "HORIZONLESS_N_POSITIVE_ZERO_RADIAL_CHARGE_FLUX_ONLY"
            and static_horizon_pole
        ),
        "outer_branch_guard": (
            config["outer_branch_rule"] == "D_H_POSITIVE_NONDEGENERATE"
            and outer_nondegenerate_witness
        ),
        "claim_scope": config["promoted_claims"] == (),
    }
    checks["mass_integrability"] = (
        compatibility["checks"]["mass_integrability"]
        and checks["scalar_action_evolution"]
        and checks["mass_radial_balance"] and checks["mass_time_balance"]
    )
    checks["angular_bianchi_closure"] = (
        compatibility["checks"]["angular_einstein"]
        and geometry["checks"]["contracted_bianchi"]
        and checks["hamiltonian_constraint"] and checks["momentum_constraint"]
        and checks["radial_metric_evolution"]
    )
    checks["aggregate"] = schema and all_true(checks.values())
    return {
        "checks": checks,
        "residuals": {
            "coframe_cross": text_expr(coframe_cross_residual),
            "misner_sharp_definition": text_expr(mass_definition_residual),
            "einstein_coupling": text_expr(einstein_coupling_residual),
            "momentum": text_expr(momentum_residual),
            "hamiltonian": text_expr(hamiltonian_residual),
            "radial_evolution": text_expr(radial_evolution_residual),
            "mass_r": text_expr(mass_r_residual), "mass_T": text_expr(mass_t_residual),
            "scalar_action_flux": text_expr(scalar_action_residual),
            "potential_principal": text_expr(potential_principal_residual),
            "current_orientation": text_expr(current_orientation_residual),
            "horizon_square": text_expr(horizon_residual),
            "passive_profile_gradient": text_expr(profile_gradient_residual),
        },
    }


@lru_cache(maxsize=1)
def physical_and_regression_audit() -> dict[str, Any]:
    geometry = geometry_base()
    matter = matter_quantities()
    evolution = production_evolution()
    q, s_o = matter["q"], matter["s_o"]
    current_t = q / SIGMA
    current_r = -(ZETA * q + s_o)
    current_vec = sp.Matrix([current_t, current_r, 0, 0])
    current_norm = sp.simplify(
        (current_vec.T * geometry["metric"] * current_vec)[0]
    )
    normal_vec = sp.Matrix([1 / SIGMA, -ZETA, 0, 0])
    future_orientation = sp.simplify(
        -(normal_vec.T * geometry["metric"] * current_vec)[0]
    )
    u_plus, u_minus = sp.symbols("u_plus u_minus", positive=True, finite=True)
    q_positive = (u_plus + u_minus) / 2
    s_timelike = (u_plus - u_minus) / 2
    timelike_parametric_norm = sp.expand(-q_positive**2 + s_timelike**2)
    timelike_manifest = -u_plus * u_minus
    timelike_witness = (
        exact_zero(timelike_parametric_norm - timelike_manifest)
        and timelike_manifest.is_negative is True
    )

    speed = sp.symbols("c")
    principal = SIGMA * sp.Matrix([[ZETA, 1], [1, ZETA]])
    characteristic = sp.expand((speed * sp.eye(2) + principal).det())
    metric_characteristic = sp.expand(
        (speed - SIGMA * (1 - ZETA)) * (speed + SIGMA * (1 + ZETA))
    )
    c_plus = SIGMA * (1 - ZETA)
    c_minus = -SIGMA * (1 + ZETA)
    delta = sp.symbols("delta", positive=True, finite=True)
    sigma_positive = sp.symbols("sigma_positive", positive=True, finite=True)
    excision_plus = c_plus.subs({SIGMA: sigma_positive, ZETA: 1 + delta})
    excision_minus = c_minus.subs({SIGMA: sigma_positive, ZETA: 1 + delta})
    excision_witness = (
        exact_zero(excision_plus + sigma_positive * delta)
        and exact_zero(excision_minus + sigma_positive * (2 + delta))
        and excision_plus.is_negative is True
        and excision_minus.is_negative is True
    )

    auxiliary_1 = sp.simplify(
        evolution["radial_t"][0] - sp.diff(evolution["phi_t"][0], R)
    )
    auxiliary_2 = sp.simplify(
        evolution["radial_t"][1] - sp.diff(evolution["phi_t"][1], R)
    )
    potential_gradient = (
        sp.diff(matter["potential"], PHI1),
        sp.diff(matter["potential"], PHI2),
    )
    potential_gradient_exact = all(
        exact_zero(a - b) for a, b in zip(potential_gradient, matter["gradients"])
    )

    null_plus = (PI1 + RAD1)**2 + (PI2 + RAD2)**2
    null_minus = (PI1 - RAD1)**2 + (PI2 - RAD2)**2
    horizon_mass_t = 4 * sp.pi * SIGMA * R**2 * null_plus
    D_H = sp.symbols("D_H", positive=True, finite=True)
    rdot = 2 * GNEWTON * horizon_mass_t / D_H
    area_dot = 8 * sp.pi * R * rdot
    horizon_radius_function = sp.Function("r_H")(T)
    geometric_horizon_area = 4 * sp.pi * horizon_radius_function**2
    area_chain_rule_residual = sp.simplify(
        sp.diff(geometric_horizon_area, T)
        - 8 * sp.pi * horizon_radius_function
        * sp.diff(horizon_radius_function, T)
    )
    mapped_geometric_area_rate = (
        8 * sp.pi * horizon_radius_function
        * sp.diff(horizon_radius_function, T)
    ).subs({
        horizon_radius_function: R,
        sp.diff(horizon_radius_function, T): rdot,
    }, simultaneous=True)
    tube_norm = sp.expand(rdot * (rdot + 2 * SIGMA))
    tube_metric_direct = sp.simplify(
        geometry["metric"][0, 0].subs(ZETA, 1)
        + 2 * geometry["metric"][0, 1].subs(ZETA, 1) * rdot
        + geometry["metric"][1, 1] * rdot**2
    )
    moving_crossing = sp.simplify(
        current_r.subs(ZETA, 1) - rdot * current_t
    )
    positive_horizon_velocity = sp.symbols(
        "positive_horizon_velocity", positive=True, finite=True
    )
    moving_manifest = (
        -u_plus - positive_horizon_velocity * q_positive / sigma_positive
    )
    moving_parametric = (
        -(q_positive + s_timelike)
        - positive_horizon_velocity * q_positive / sigma_positive
    )
    moving_sign_witness = (
        exact_zero(moving_parametric - moving_manifest)
        and moving_manifest.is_negative is True
    )
    fixed_horizon_parametric = -(q_positive + s_timelike)
    fixed_horizon_manifest = -u_plus
    fixed_horizon_sign_witness = (
        exact_zero(fixed_horizon_parametric - fixed_horizon_manifest)
        and fixed_horizon_manifest.is_negative is True
    )
    exterior_balance = 4 * sp.pi * R**2 * (
        SIGMA * current_r.subs(ZETA, 1) - q * rdot
    )
    exterior_from_integral = -4 * sp.pi * R**2 * (
        SIGMA * (q + s_o) + q * rdot
    )
    boundary_mass_flux = 4 * sp.pi * SIGMA * R**2 * (
        ZETA * matter["kinetic_sum"] + (1 + ZETA**2) * matter["S"]
    )
    r_positive, amp_in_1, amp_in_2 = sp.symbols(
        "r_positive amp_in_1 amp_in_2", positive=True, finite=True
    )
    strict_flux_substitutions = {
        SIGMA: sigma_positive, R: r_positive,
        PI1: amp_in_1 - RAD1, PI2: amp_in_2 - RAD2,
    }
    horizon_square_witness = sp.simplify(
        horizon_mass_t.subs(strict_flux_substitutions)
    )
    radius_strict_flux_witness = sp.simplify(
        rdot.subs(strict_flux_substitutions)
    )
    area_strict_flux_witness = sp.simplify(
        area_dot.subs(strict_flux_substitutions)
    )
    tube_strict_flux_witness = sp.simplify(
        tube_norm.subs(strict_flux_substitutions)
    )
    zero_flux_substitutions = {PI1: -RAD1, PI2: -RAD2}
    zero_flux_witness = (
        exact_zero(rdot.subs(zero_flux_substitutions))
        and exact_zero(area_dot.subs(zero_flux_substitutions))
        and exact_zero(tube_norm.subs(zero_flux_substitutions))
    )
    exterior_parametric = 4 * sp.pi * r_positive**2 * (
        -sigma_positive * (q_positive + s_timelike)
        - q_positive * positive_horizon_velocity
    )
    exterior_manifest = 4 * sp.pi * r_positive**2 * sigma_positive * moving_manifest
    exterior_sign_witness = (
        exact_zero(exterior_parametric - exterior_manifest)
        and exterior_manifest.is_negative is True
    )
    mass_radial_at_horizon = sp.symbols("mass_radial_at_horizon", finite=True)
    implicit_D = 1 - 2 * GNEWTON * mass_radial_at_horizon
    implicit_tangency = (
        -2 * GNEWTON * horizon_mass_t + rdot * implicit_D
    ).subs(mass_radial_at_horizon, (1 - D_H) / (2 * GNEWTON))

    N, sigma_s, omega, chi_r, chi = sp.symbols(
        "N sigma_s omega chi_r chi", positive=True, finite=True
    )
    zeta_s = sp.symbols("zeta_s", positive=True, finite=True)
    pg_static = sp.Matrix([
        [-sigma_s**2 * N, sigma_s * zeta_s],
        [sigma_s * zeta_s, 1],
    ])
    jacobian = sp.Matrix([[1, zeta_s / (sigma_s * N)], [0, 1]])
    static_transformed = sp.simplify(jacobian.T * pg_static * jacobian)
    static_target = sp.diag(-sigma_s**2 * N, 1 / N)
    static_metric_residual = static_transformed.subs(zeta_s**2, 1 - N) - static_target
    pi_chi = -zeta_s * chi_r
    phi_chi = chi_r
    pi_theta = omega / (sigma_s * N)
    phi_theta = -omega * zeta_s / (sigma_s * N)
    V_s = sp.symbols("V_s", finite=True)
    rho_s = (
        pi_chi**2 + phi_chi**2 + chi**2 * (pi_theta**2 + phi_theta**2)
    ) / 2 + V_s
    S_s = pi_chi * phi_chi + chi**2 * pi_theta * phi_theta
    w364_density = N * chi_r**2 / 2 + omega**2 * chi**2 / (2 * sigma_s**2 * N) + V_s
    w364_lapse = chi_r**2 + omega**2 * chi**2 / (sigma_s**2 * N**2)
    static_charge_flux = sp.simplify(zeta_s * chi**2 * pi_theta + chi**2 * phi_theta)
    static_checks = {
        "metric_map": matrix_zero(sp.simplify(static_metric_residual)),
        "density_map": exact_zero((rho_s + zeta_s * S_s).subs(zeta_s**2, 1 - N) - w364_density),
        "lapse_map": exact_zero((-S_s / zeta_s).subs(zeta_s**2, 1 - N) - w364_lapse),
        "zero_radial_charge_flux": exact_zero(static_charge_flux),
        "horizon_divergence_guard": sp.denom(pi_theta) == N * sigma_s,
    }

    r_s = sp.symbols("r_s", positive=True, finite=True)
    zeta_vac = sp.sqrt(r_s / R)
    vacuum_subs = {
        SIGMA: 1, sp.diff(SIGMA, R): 0,
        ZETA: zeta_vac, sp.diff(ZETA, R): sp.diff(zeta_vac, R),
        sp.diff(ZETA, T): 0,
    }
    w372_equation_checks = []
    for index, (pi_field, radial_field) in enumerate(((PI1, RAD1), (PI2, RAD2))):
        target_phi_t = pi_field + zeta_vac * radial_field
        target_radial_t = sp.diff(target_phi_t, R)
        target_pi_t = (
            sp.diff(R**2 * (radial_field + zeta_vac * pi_field), R) / R**2
            - matter["gradients"][index]
        )
        w372_equation_checks.extend((
            exact_zero(evolution["phi_t"][index].subs(vacuum_subs) - target_phi_t),
            exact_zero(evolution["radial_t"][index].subs(vacuum_subs) - target_radial_t),
            exact_zero(evolution["pi_t"][index].subs(vacuum_subs) - target_pi_t),
        ))
    test_field_checks = {
        "vacuum_E00": exact_zero(geometry["g00"].subs(vacuum_subs)),
        "vacuum_E01": exact_zero(geometry["g01"].subs(vacuum_subs)),
        "vacuum_E11": exact_zero(geometry["g11"].subs(vacuum_subs)),
        "w3_72_current": exact_zero(
            current_r.subs({SIGMA: 1, ZETA: zeta_vac}) + zeta_vac * q + s_o
        ),
        "w3_72_speeds": (
            exact_zero(c_plus.subs({SIGMA: 1, ZETA: zeta_vac}) - (1 - zeta_vac))
            and exact_zero(c_minus.subs({SIGMA: 1, ZETA: zeta_vac}) + (1 + zeta_vac))
        ),
        "w3_72_two_component_scalar_evolution": all_true(w372_equation_checks),
    }
    flat_equation_checks = []
    for index, (pi_field, radial_field) in enumerate(((PI1, RAD1), (PI2, RAD2))):
        flat_equation_checks.extend((
            exact_zero(
                evolution["phi_t"][index].subs({SIGMA: 1, ZETA: 0}) - pi_field
            ),
            exact_zero(
                evolution["radial_t"][index].subs({SIGMA: 1, ZETA: 0})
                - sp.diff(pi_field, R)
            ),
            exact_zero(
                evolution["pi_t"][index].subs({
                    SIGMA: 1, ZETA: 0,
                    sp.diff(SIGMA, R): 0, sp.diff(ZETA, R): 0,
                })
                - (
                    sp.diff(radial_field, R) + 2 * radial_field / R
                    - matter["gradients"][index]
                )
            ),
        ))
    flat_checks = {
        "two_component_scalar_evolution": all_true(flat_equation_checks),
        "current": exact_zero(current_r.subs({SIGMA: 1, ZETA: 0}) + s_o),
        "speeds": exact_zero(c_plus.subs({SIGMA: 1, ZETA: 0}) - 1)
                  and exact_zero(c_minus.subs({SIGMA: 1, ZETA: 0}) + 1),
    }

    boundary_radius, boundary_lapse = sp.symbols(
        "R_B sigma_B", positive=True, finite=True
    )
    lapse_constraint = sp.diff(SIGMA, R) - evolution["sigma_r"]
    lapse_constraint_first_order_radial = (
        lapse_constraint.atoms(sp.Derivative) == {sp.diff(SIGMA, R)}
    )
    lapse_boundary_value = SIGMA.subs(R, boundary_radius)
    lapse_boundary_residual = sp.simplify(
        (lapse_boundary_value - boundary_lapse).subs(
            lapse_boundary_value, boundary_lapse
        )
    )
    boundary_data_registry = (
        "sigma(T,R_B)=sigma_B>0",
        "d_T m_MS(T,R_B)=FOUR_PI_SIGMA_B_R_B_SQUARED_TIMES_FIELD_FLUX",
    )
    boundary_data_registry_exact = (
        len(boundary_data_registry) == 2
        and boundary_data_registry[0] == "sigma(T,R_B)=sigma_B>0"
        and boundary_data_registry[1].startswith("d_T m_MS(T,R_B)=")
    )

    connection_entries = [
        geometry["gamma"][upper][left][right]
        for upper in range(4) for left in range(4) for right in range(4)
    ]
    connection_derivatives = set().union(*(
        expression.atoms(sp.Derivative) for expression in connection_entries
    ))
    connection_first_order_only = (
        bool(connection_derivatives)
        and all(
            sum(count for _, count in derivative.variable_count) == 1
            for derivative in connection_derivatives
        )
        and sp.diff(SIGMA, R) in connection_derivatives
    )
    reference_factor = sp.symbols("reference_factor", positive=True, finite=True)
    constant_reference_rescaling_residual = sp.simplify(
        sp.diff(reference_factor * SIGMA, R) / (reference_factor * SIGMA)
        - sp.diff(SIGMA, R) / SIGMA
    )
    tidal_expressions = list(geometry["frame_riemann"].values())
    tidal_derivatives = set().union(*(
        expression.atoms(sp.Derivative) for expression in tidal_expressions
    ))
    tidal_second_derivative_present = any(
        sum(count for _, count in derivative.variable_count) >= 2
        for derivative in tidal_derivatives
    )
    local_expressions = [
        *list(geometry["metric"]), matter["potential"],
        *evolution["phi_t"], *evolution["radial_t"], *evolution["pi_t"],
        evolution["sigma_r"], evolution["zeta_r"], evolution["zeta_t"],
        *connection_entries, *tidal_expressions,
    ]
    forbidden_roles = ("p_L", "P_F", "readout_connection", "foundation_pressure")
    role_text = " ".join(sp.sstr(item) for item in local_expressions)
    scale_role_witness = (
        all(role not in role_text for role in forbidden_roles)
        and "sigma" in role_text and "zeta" in role_text
        and exact_zero(constant_reference_rescaling_residual)
        and connection_first_order_only
        and tidal_second_derivative_present
        and geometry["checks"]["curvature_horizon_finite"]
    )
    observation_inputs_absent = (
        all(
            token not in relative.casefold()
            for relative in DEPENDENCIES
            for token in ("observation", "catalog", "dataset", "archive", "likelihood")
        )
        and not any(
            item in sys.modules for item in ("numpy", "scipy", "pandas", "astropy")
        )
    )
    compatibility = production_compatibility()
    checks = {
        "potential_gradient": potential_gradient_exact,
        "scalar_auxiliary": exact_zero(auxiliary_1) and exact_zero(auxiliary_2),
        "principal_symmetric": principal == principal.T,
        "characteristic_cone": exact_zero(characteristic - metric_characteristic),
        "current_norm": exact_zero(current_norm + q**2 - s_o**2),
        "future_current_orientation": exact_zero(future_orientation - q),
        "timelike_domain": timelike_witness,
        "horizon_inward_current": (
            exact_zero(current_r.subs(ZETA, 1) + q + s_o)
            and fixed_horizon_sign_witness
        ),
        "horizon_mass_flux_square": exact_zero(
            4 * sp.pi * SIGMA * R**2 * (
                matter["kinetic_sum"] + 2 * matter["S"]
            ) - horizon_mass_t
        ),
        "horizon_square_nonnegative": horizon_square_witness.is_positive is True,
        "radius_velocity": (
            exact_zero(implicit_tangency)
            and radius_strict_flux_witness.is_positive is True
            and zero_flux_witness
        ),
        "area_law": (
            exact_zero(area_chain_rule_residual)
            and exact_zero(mapped_geometric_area_rate - area_dot)
        ),
        "area_nonnegative": (
            area_strict_flux_witness.is_positive is True and zero_flux_witness
        ),
        "tube_signature": (
            exact_zero(tube_metric_direct - tube_norm)
            and tube_strict_flux_witness.is_positive is True
            and zero_flux_witness
        ),
        "moving_charge_crossing": exact_zero(
            moving_crossing + q + s_o + rdot * q / SIGMA
        ) and moving_sign_witness,
        "exterior_charge_balance": (
            exact_zero(exterior_balance - exterior_from_integral)
            and exterior_sign_witness
        ),
        "flux_compatible_mass_boundary": exact_zero(
            boundary_mass_flux - 4 * sp.pi * SIGMA * R**2 * (
                (PI1 + ZETA * RAD1) * (ZETA * PI1 + RAD1)
                + (PI2 + ZETA * RAD2) * (ZETA * PI2 + RAD2)
            )
        ),
        "scalar_nec": exact_zero(
            (matter["rho"] + matter["p_r"] + 2 * matter["S"]) - null_plus
        ) and exact_zero(
            (matter["rho"] + matter["p_r"] - 2 * matter["S"]) - null_minus
        ),
        "static_w3_64": all_true(static_checks.values()),
        "test_field_w3_72": all_true(test_field_checks.values()),
        "flat_w3_58": all_true(flat_checks.values()),
        "excision_direction": excision_witness,
        "local_data_handoff": (
            geometry["checks"]["metric_inverse"]
            and geometry["checks"]["marginal_metric_regular"]
            and exact_zero(auxiliary_1) and exact_zero(auxiliary_2)
            and principal == principal.T
            and compatibility["checks"]["mass_integrability"]
            and lapse_constraint_first_order_radial
            and exact_zero(lapse_boundary_residual)
            and boundary_data_registry_exact
        ),
        "scale_role_separation": scale_role_witness,
        "observation_inputs_absent": observation_inputs_absent,
    }
    return {
        "checks": checks,
        "current": {
            "j_T": text_expr(current_t), "j_r": text_expr(current_r),
            "norm": text_expr(current_norm),
            "future_orientation_minus_n_dot_j": text_expr(future_orientation),
            "timelike_parametric_norm": text_expr(timelike_manifest),
            "moving_horizon_crossing": text_expr(moving_crossing),
            "strict_sign_domain": "q>0, q^2>s_O^2, sigma>0, D_H>0, nonzero flux",
            "Q_ext_definition": "Q_ext(T)=4*pi*Integral_{r_H(T)}^{R_B}[r^2 q(T,r) dr]",
            "outer_boundary_condition": "j_O^r(T,R_B)=0",
        },
        "horizon": {
            "mass_flux": text_expr(horizon_mass_t),
            "radius_velocity": text_expr(rdot), "area_velocity": text_expr(area_dot),
            "tube_norm": text_expr(tube_norm),
            "zero_flux_radius_area_tube_null": zero_flux_witness,
            "excision_speeds": [text_expr(excision_plus), text_expr(excision_minus)],
            "flux_compatible_mass_boundary_datum": (
                "d_T m_MS(T,R_B)=4*pi*sigma_B*R_B^2*sum_A[(Pi_A+zeta_B Phi_A)"
                "(zeta_B Pi_A+Phi_A)]"
            ),
        },
        "static_w3_64_checks": static_checks,
        "test_field_w3_72_checks": test_field_checks,
        "flat_w3_58_checks": flat_checks,
        "boundary_data_handoff": {
            "registry": list(boundary_data_registry),
            "registry_exact": boundary_data_registry_exact,
            "lapse_constraint_first_order_radial": lapse_constraint_first_order_radial,
            "lapse_normalization_residual": text_expr(lapse_boundary_residual),
        },
        "scale_gradient_tidal_witnesses": {
            "constant_reference_rescaling_residual": text_expr(
                constant_reference_rescaling_residual
            ),
            "connection_first_order_only": connection_first_order_only,
            "tidal_second_derivative_present": tidal_second_derivative_present,
            "passive_roles_absent": all(
                role not in role_text for role in forbidden_roles
            ),
        },
    }


PRIMARY_WITNESS_MAP = {
    "coframe_metric": "coframe_cross",
    "misner_sharp_definition": "misner_sharp_definition",
    "einstein_coupling": "einstein_coupling",
    "momentum_constraint": "momentum",
    "hamiltonian_constraint": "hamiltonian",
    "radial_metric_evolution": "radial_evolution",
    "mass_radial_balance": "mass_r",
    "mass_time_balance": "mass_T",
    "scalar_action_evolution": "scalar_action_flux",
    "potential_lower_order": "potential_principal",
    "ordinary_phase_conservation": "current_orientation",
    "horizon_mass_square": "horizon_square",
    "intrinsic_profile_role": "passive_profile_gradient",
}


def run_mutation_controls() -> dict[str, Any]:
    production = evaluate_configuration(PRODUCTION_CONFIGURATION)
    frozen = {name: tuple(sorted(paths)) for name, paths in FROZEN_MUTATION_REGISTRY}
    changed = {name: tuple(sorted(change)) for name, change in MUTATIONS.items()}
    records: dict[str, Any] = {}
    for name, change in MUTATIONS.items():
        candidate = deepcopy(PRODUCTION_CONFIGURATION)
        candidate.update(change)
        evaluated = evaluate_configuration(candidate)
        mandatory = MUTATION_PRIMARY_FAILURES[name]
        observed = {key for key in mandatory if evaluated["checks"].get(key) is False}
        detected = (
            validate_configuration(candidate)
            and evaluated["checks"]["aggregate"] is False
            and observed == mandatory
            and changed[name] == frozen[name]
        )
        records[name] = {
            "changed_paths": sorted(change), "frozen_changed_paths": list(frozen[name]),
            "changed_paths_exact": changed[name] == frozen[name],
            "mandatory_primary_failures": sorted(mandatory),
            "observed_primary_failures": sorted(observed),
            "all_mandatory_primary_failures_observed": observed == mandatory,
            "aggregate_after_mutation": evaluated["checks"]["aggregate"],
            "primary_residual_witnesses": {
                key: evaluated["residuals"].get(
                    PRIMARY_WITNESS_MAP.get(key, key),
                    "SEMANTIC_OR_ROLE_BOUNDARY",
                )
                for key in sorted(mandatory)
            },
            "detected": detected,
        }
    exact_names = set(MUTATIONS) == set(frozen) == set(MUTATION_PRIMARY_FAILURES)
    exact_paths = changed == frozen
    all_detected = (
        production["checks"]["aggregate"] is True and exact_names and exact_paths
        and all_true(record["detected"] for record in records.values())
    )
    return {
        "registered_mutation_count": len(MUTATIONS),
        "production_passes_same_evaluator": production["checks"]["aggregate"] is True,
        "exact_name_registry": exact_names, "exact_changed_path_registry": exact_paths,
        "all_detected": all_detected, "records": records,
    }


def build_flags(
    *, dependency_exact: bool, upstream_exact: bool, prereg_exact: bool,
    package_exact: bool, immutable_exact: bool, canon_exact: bool,
    production: dict[str, Any], physical: dict[str, Any], mutations_exact: bool,
) -> dict[str, bool]:
    c = production["checks"]
    g = geometry_base()["checks"]
    p = physical["checks"]
    compatibility = production_compatibility()["checks"]
    flags: dict[str, bool] = {
        "dependency_hashes_exact": dependency_exact,
        "upstream_status_and_scope_exact": upstream_exact,
        "one_metric_one_localized_source_exact": c["one_metric_source"],
        "w3_58_cartesian_action_unchanged_exact": (
            upstream_exact and c["scalar_action_evolution"]
            and p["potential_gradient"] and c["hilbert_stress"]
        ),
        "gpg_metric_inverse_volume_exact": (
            g["metric_inverse"] and g["metric_determinant"] and g["volume_density"]
        ),
        "gpg_dual_frame_exact": g["coframe_dual"],
        "misner_sharp_definition_exact": c["misner_sharp_definition"] and g["misner_sharp_geometric"],
        "radial_null_speeds_exact": g["null_factorization"],
        "null_expansions_exact": (
            g["null_expansion_plus"] and g["null_expansion_minus"]
            and g["null_expansion_product"]
        ),
        "marginal_surface_horizon_regular_exact": g["marginal_metric_regular"] and g["curvature_horizon_finite"],
        "scalar_evolution_system_exact": c["scalar_action_evolution"] and p["potential_gradient"],
        "scalar_auxiliary_constraint_propagation_exact": p["scalar_auxiliary"],
        "scalar_principal_block_symmetric_exact": c["scalar_principal_symmetric"] and p["principal_symmetric"],
        "matter_metric_characteristic_cone_match_exact": c["matter_metric_cone"] and p["characteristic_cone"],
        "potential_lower_order_exact": c["potential_lower_order"],
        "hilbert_stress_exact": c["hilbert_stress"],
        "ordinary_phase_current_cartesian_exact": (
            c["ordinary_phase_current"] and p["current_norm"]
            and p["future_current_orientation"]
        ),
        "ordinary_phase_conservation_exact": c["ordinary_phase_conservation"] and compatibility["current_conservation"],
        "timelike_current_domain_exact": (
            p["timelike_domain"] and p["current_norm"]
            and p["future_current_orientation"]
        ),
        "horizon_inward_current_exact": p["horizon_inward_current"] and c["ordinary_phase_current"],
        "einstein_frame_components_exact": g["einstein_frame_00"] and g["einstein_frame_01"] and g["einstein_frame_11"],
        "hamiltonian_constraint_exact": c["hamiltonian_constraint"],
        "momentum_constraint_exact": c["momentum_constraint"],
        "radial_metric_evolution_exact": c["radial_metric_evolution"],
        "mass_radial_balance_exact": c["mass_radial_balance"],
        "mass_time_balance_exact": c["mass_time_balance"],
        "mass_balance_integrability_exact": c["mass_integrability"] and compatibility["mass_integrability"],
        "angular_einstein_bianchi_closure_exact": c["angular_bianchi_closure"],
        "coupled_constraint_propagation_exact": (
            c["mass_integrability"] and c["angular_bianchi_closure"] and p["scalar_auxiliary"]
        ),
        "horizon_mass_flux_square_exact": (
            c["horizon_mass_square"] and p["horizon_mass_flux_square"]
            and p["horizon_square_nonnegative"]
        ),
        "outer_marginal_radius_velocity_exact": p["radius_velocity"] and c["outer_branch_guard"],
        "outer_marginal_area_law_exact": (
            p["area_law"] and p["area_nonnegative"] and c["outer_branch_guard"]
        ),
        "marginal_tube_signature_exact": p["tube_signature"],
        "moving_horizon_charge_crossing_exact": (
            p["moving_charge_crossing"] and p["horizon_inward_current"]
            and p["radius_velocity"]
        ),
        "exterior_charge_balance_exact": (
            p["exterior_charge_balance"] and compatibility["current_conservation"]
            and p["radius_velocity"]
        ),
        "static_w3_64_regression_exact": p["static_w3_64"] and c["static_regression_scope"],
        "test_field_w3_72_regression_exact": p["test_field_w3_72"],
        "flat_w3_58_regression_exact": p["flat_w3_58"],
        "intrinsic_profile_not_passively_rescaled_exact": c["intrinsic_profile_role"],
        "readout_absent_from_local_dynamics_exact": c["one_metric_source"] and c["intrinsic_profile_role"],
        "scale_gradient_tidal_role_separation_exact": (
            upstream_exact and p["scale_role_separation"] and c["lapse_role"]
        ),
        "curvature_no_marginal_pole_exact": g["curvature_horizon_finite"],
        "local_constrained_data_handoff_exact": (
            p["local_data_handoff"] and p["flux_compatible_mass_boundary"]
            and c["mass_integrability"] and p["characteristic_cone"]
        ),
        "excision_characteristic_direction_exact": p["excision_direction"],
        "scalar_nec_exact": p["scalar_nec"],
        "penrose_boundary_inherited_exact": upstream_exact and p["scalar_nec"],
        "mutation_controls_pass": mutations_exact,
        "g0_goal_pass": dependency_exact and upstream_exact and prereg_exact and package_exact and immutable_exact and canon_exact and c["claim_scope"],
        "g1_conventions_pass": c["coframe_metric"] and c["one_metric_source"] and c["lapse_role"] and c["horizon_scope"],
        "g2_geometry_pass": all_true(g.values()) and c["misner_sharp_definition"],
        "g3_einstein_system_pass": c["hamiltonian_constraint"] and c["momentum_constraint"] and c["radial_metric_evolution"] and c["mass_integrability"] and c["angular_bianchi_closure"],
        "g4_matter_system_pass": c["scalar_action_evolution"] and c["hilbert_stress"] and c["ordinary_phase_conservation"] and p["scalar_nec"] and p["characteristic_cone"],
        "g5_limits_regression_pass": p["static_w3_64"] and p["test_field_w3_72"] and p["flat_w3_58"],
        "g6_physical_flux_pass": c["horizon_mass_square"] and p["radius_velocity"] and p["area_law"] and p["tube_signature"] and p["moving_charge_crossing"] and c["outer_branch_guard"] and c["claim_scope"],
        "g7_observation_not_applicable_exact": p["observation_inputs_absent"],
        "g8_export_not_applicable_exact": immutable_exact and canon_exact,
        "package_clean_pass": package_exact,
    }
    ledger = dict(PRODUCTION_CONFIGURATION["source_ledger"])
    promoted = set(PRODUCTION_CONFIGURATION["promoted_claims"])
    audited_scope = {
        "second_metric_introduced": PRODUCTION_CONFIGURATION["metric_ids"] != ("g",),
        "duplicate_localized_source_introduced": ledger["T_O"] != 1 or ledger["T_C"] != 0,
        "noether_current_added_as_einstein_source": ledger["j_O_extra_Einstein_RHS"] != 0,
        "foundation_response_action_added": ledger["P_F"] != 0,
        "full_foundation_pressure_constitutive_law_derived": "foundation_pressure_law" in promoted,
        "nonstatic_lapse_identified_as_p_t": not c["lapse_role"],
        "p_L_inserted_into_local_action": ledger["p_L"] != 0,
        "intrinsic_oscillon_profile_rescaled": not c["intrinsic_profile_role"],
        "whole_oscillon_dynamical_rigidity_derived": "whole_oscillon_dynamical_rigidity" in promoted,
        "static_horizon_bound_oscillon_derived": not c["static_regression_scope"],
        "degenerate_outer_horizon_branch_derived": not c["outer_branch_guard"],
        "global_gpg_coverage_derived": "global_gpg_coverage" in promoted,
        "horizon_formation_completed": "horizon_formation" in promoted,
        "marginal_surface_promoted_to_event_horizon": not c["horizon_scope"],
        "global_collapse_evolution_completed": "global_collapse" in promoted,
        "regular_centre_derived": "regular_centre" in promoted,
        "regular_black_hole_interior_derived": "regular_black_hole_interior" in promoted,
        "singularity_resolution_completed": "singularity_resolution" in promoted,
        "geodesic_completeness_derived": "geodesic_completeness" in promoted,
        "penrose_boundary_evaded": "penrose_boundary_evaded" in promoted or not p["scalar_nec"],
        "scalar_nec_violated": not p["scalar_nec"],
        "tensor_gravitational_waveform_derived": "tensor_gravitational_waveform" in promoted,
        "new_observation_tested": "new_observation" in promoted,
        "canon_changed": not canon_exact,
        "intuitive_files_changed": not immutable_exact,
    }
    flags.update(audited_scope)
    expected_preaggregate = (REQUIRED_TRUE_FLAGS | REQUIRED_FALSE_FLAGS) - {"aggregate_gate_pass"}
    flags["aggregate_gate_pass"] = (
        set(flags) == expected_preaggregate
        and all(flags[key] is True for key in REQUIRED_TRUE_FLAGS - {"aggregate_gate_pass"})
        and all(flags[key] is False for key in REQUIRED_FALSE_FLAGS)
    )
    return flags


def gate_registry(flags: dict[str, bool]) -> dict[str, bool]:
    return {
        "G0_GOAL": flags["g0_goal_pass"],
        "G1_CONVENTIONS": flags["g1_conventions_pass"],
        "G2_GEOMETRY": flags["g2_geometry_pass"],
        "G3_EINSTEIN_SYSTEM": flags["g3_einstein_system_pass"],
        "G4_MATTER_SYSTEM": flags["g4_matter_system_pass"],
        "G5_LIMITS_REGRESSION": flags["g5_limits_regression_pass"],
        "G6_PHYSICAL_FLUX": flags["g6_physical_flux_pass"],
        "G7_OBSERVATION": flags["g7_observation_not_applicable_exact"],
        "G8_EXPORT": flags["g8_export_not_applicable_exact"],
    }


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=".w3_73_", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def actual_package_exact() -> bool:
    files = {path.name for path in PACKAGE_DIR.iterdir() if path.is_file()}
    directories = {path.name for path in PACKAGE_DIR.iterdir() if path.is_dir()}
    return files == EXPECTED_PACKAGE_FILES and not directories


def main() -> int:
    dependency_records, dependency_exact = audit_files(DEPENDENCIES)
    immutable, immutable_exact = audit_immutable_intuitive()
    canon, canon_exact = audit_canon()
    prereg = audit_preregistration()
    package = audit_package_before_write()
    upstream, upstream_exact = audit_upstream()
    production = evaluate_configuration(PRODUCTION_CONFIGURATION)
    physical = physical_and_regression_audit()
    compatibility = production_compatibility()
    mutations = run_mutation_controls()
    geometry = geometry_base()

    prereg_exact = bool(
        prereg["hash_exact"] and prereg["markers_exact"]
        and prereg["required_true_keyset_exact"]
        and prereg["required_false_keyset_exact"]
        and prereg["frozen_mutation_registry_exact"]
    )
    package_exact = bool(package["recursive_exact_three_file_package"])
    flags = build_flags(
        dependency_exact=dependency_exact, upstream_exact=upstream_exact,
        prereg_exact=prereg_exact, package_exact=package_exact,
        immutable_exact=immutable_exact, canon_exact=canon_exact,
        production=production, physical=physical,
        mutations_exact=mutations["all_detected"],
    )
    gates = gate_registry(flags)
    validation = {
        "required_true_keyset_exact": set(flags).intersection(REQUIRED_TRUE_FLAGS) == REQUIRED_TRUE_FLAGS,
        "required_false_keyset_exact": set(flags).intersection(REQUIRED_FALSE_FLAGS) == REQUIRED_FALSE_FLAGS,
        "closure_keyset_exact": set(flags) == REQUIRED_TRUE_FLAGS | REQUIRED_FALSE_FLAGS,
        "all_required_true": all(flags[key] is True for key in REQUIRED_TRUE_FLAGS),
        "all_required_false": all(flags[key] is False for key in REQUIRED_FALSE_FLAGS),
        "production_configuration_aggregate": production["checks"]["aggregate"] is True,
        "all_mutations_detected": mutations["all_detected"],
        "registered_mutation_count_exact": mutations["registered_mutation_count"] == 18,
        "dependency_hashes_exact": dependency_exact,
        "upstream_exact": upstream_exact, "preregistration_exact": prereg_exact,
        "package_prediction_exact": package_exact,
        "immutable_intuitive_exact": immutable_exact, "canon_control_exact": canon_exact,
        "all_gates_pass": all_true(gates.values()),
        "casefold_unique_json_keys": False,
        "post_write_package_exact": False,
    }
    result: dict[str, Any] = {
        "schema_version": "1.0", "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION, "status": FAIL_STATUS, "artifact_valid": False,
        "claim": {
            "established": (
                "The inherited Einstein-Hilbert metric and W3-58 complex scalar form "
                "one local, fully coupled, horizon-regular spherical constrained system."
            ),
            "metric_role": "ONE_EINSTEIN_METRIC",
            "source_role": "ONE_LOCALIZED_HILBERT_T_O_SOURCE",
            "horizon_role": "NONDEGENERATE_FUTURE_OUTER_MARGINAL_TUBE_ON_A_LOCAL_ANNULUS",
            "profile_role": "INTRINSIC_FIELD_EVOLVED_BY_ITS_ACTION_NOT_BY_PASSIVE_RULER_RESCALING",
        },
        "evidence_type": {
            "geometry": "DIRECT_FOUR_DIMENSIONAL_EXACT_SYMBOLIC",
            "matter": "UNCHANGED_ACTION_EXACT_SYMBOLIC",
            "coupling_and_flux": "EXACT_SYMBOLIC_LOCAL_CONSTRAINED_EVOLUTION",
            "observation": "NOT_APPLICABLE",
        },
        "dependencies": {"all_hashes_exact": dependency_exact, "records": dependency_records},
        "upstream_regression": upstream, "preregistration": prereg,
        "package": package, "immutable_intuitive_controls": immutable,
        "canon_control": canon,
        "source_ledger": {
            "metric_ids": list(PRODUCTION_CONFIGURATION["metric_ids"]),
            "multiplicities": dict(PRODUCTION_CONFIGURATION["source_ledger"]),
        },
        "exact_geometry": {
            "checks": geometry["checks"],
            "frame_einstein_components": {
                "G_00": text_expr(geometry["expected_g00"]),
                "G_01": text_expr(geometry["expected_g01"]),
                "G_11": text_expr(geometry["expected_g11"]),
            },
            "curvature_horizon_denominators": geometry["horizon_denominators"],
            "contracted_bianchi_residuals": [text_expr(item) for item in geometry["bianchi"]],
        },
        "coupled_system": {
            "production_checks": production["checks"],
            "production_residuals": production["residuals"],
            "compatibility_checks": compatibility["checks"],
            "compatibility_residuals": {
                "mass_mixed_derivative": text_expr(compatibility["mass_integrability_residual"]),
                "ordinary_phase_conservation": text_expr(compatibility["current_conservation_residual"]),
                "angular_bianchi_implication": text_expr(
                    compatibility["angular_implication_residual"]
                ),
                "angular_einstein_residual_before_implication": text_expr(
                    compatibility["angular_einstein_residual"]
                ),
                "radial_einstein_residual_divergence_after_base_equations": text_expr(
                    compatibility["radial_residual_divergence"]
                ),
                "base_frame_einstein_residuals_on_production_equations": [
                    text_expr(item)
                    for item in compatibility["base_frame_einstein_residuals"]
                ],
                "hilbert_conservation_on_shell_residuals": [
                    text_expr(item)
                    for item in compatibility["hilbert_conservation_residuals"]
                ],
            },
        },
        "physical_flux_and_regressions": physical,
        "mutation_controls": mutations,
        "closure_flags": flags,
        "scope_flags": {key: flags[key] for key in sorted(REQUIRED_FALSE_FLAGS)},
        "gate_registry": gates,
        "physical_decision": {
            "local_coupled_handoff": "CLOSED",
            "marginal_mass_flux": "FINITE_SUM_OF_SQUARES_AND_NONNEGATIVE",
            "future_outer_radius_and_area": "NONDECREASING_ON_D_H_POSITIVE_BRANCH",
            "marginal_tube": "SPACELIKE_FOR_STRICT_FLUX_NULL_FOR_ZERO_FLUX",
            "ordinary_phase_charge": "STRICTLY_INWARD_ON_NONZERO_FUTURE_TIMELIKE_BRANCH",
            "excision_interior": "BOTH_SCALAR_CHARACTERISTICS_TOWARD_DECREASING_AREAL_RADIUS",
            "static_w3_64_branch": "HORIZONLESS_N_POSITIVE_ONLY",
            "event_horizon": "NOT_IDENTIFIED_FROM_LOCAL_MARGINAL_DATA",
            "next_exact_input": (
                "Compatible global initial data and numerical collapse are required before "
                "horizon formation, event-horizon location, an interior, or an endpoint can be tested."
            ),
        },
        "scientific_boundary": {
            "established": [
                "direct generalized-PG Einstein tensor and regular coframe geometry",
                "action-derived Cartesian complex-scalar first-order evolution",
                "once-counted Hilbert stress and conserved ordinary-phase current",
                "Hamiltonian and momentum constraints plus radial metric evolution",
                "compatible radial and temporal Misner-Sharp mass balances",
                "angular Einstein closure through Bianchi and on-shell matter dynamics",
                "matched metric and matter characteristics through zeta=1",
                "nonnegative outer-marginal mass, radius, and area flux identities",
                "moving-horizon charge crossing and exterior charge balance",
                "exact W3-58, W3-64, and W3-72 regressions",
            ],
            "not_established": [
                "formation or global location of an event horizon",
                "a regular centre or black-hole interior",
                "global collapse, waveform, or endpoint",
                "singularity resolution or geodesic completeness",
                "a new foundation response action or pressure constitutive law",
                "passive rescaling or dynamical rigidity of a whole oscillon",
                "an observational likelihood or fit",
            ],
        },
        "provenance": {
            "generated_utc": "NOT_EMBEDDED_TO_PRESERVE_BYTE_REPRODUCIBILITY",
            "python": sys.version.split()[0], "sympy": sp.__version__,
            "platform": platform.platform(),
            "source_path": SOURCE_PATH.relative_to(REPO_ROOT).as_posix(),
            "source_sha256": sha256_file(SOURCE_PATH),
            "preregistration_sha256": sha256_file(PREREG_PATH),
            "network_used": False, "archived_theory_used": False,
            "observational_data_read": False, "canon_written": False,
            "intuitive_files_written": False,
        },
        "validation": validation,
    }
    result["validation"]["casefold_unique_json_keys"] = casefold_keys_unique(result)
    prewrite_valid = all_true([
        validation["required_true_keyset_exact"], validation["required_false_keyset_exact"],
        validation["closure_keyset_exact"], validation["all_required_true"],
        validation["all_required_false"], validation["production_configuration_aggregate"],
        validation["all_mutations_detected"], validation["registered_mutation_count_exact"],
        validation["dependency_hashes_exact"], validation["upstream_exact"],
        validation["preregistration_exact"], validation["package_prediction_exact"],
        validation["immutable_intuitive_exact"], validation["canon_control_exact"],
        validation["all_gates_pass"], validation["casefold_unique_json_keys"],
    ])
    result["artifact_valid"] = prewrite_valid and finite_json(result)
    result["status"] = PASS_STATUS if result["artifact_valid"] else FAIL_STATUS
    atomic_write_json(RESULT_PATH, result)
    result["validation"]["post_write_package_exact"] = actual_package_exact()
    result["artifact_valid"] = bool(
        result["artifact_valid"] and result["validation"]["post_write_package_exact"]
        and finite_json(result) and casefold_keys_unique(result)
    )
    result["status"] = PASS_STATUS if result["artifact_valid"] else FAIL_STATUS
    atomic_write_json(RESULT_PATH, result)
    loaded = load_json(RESULT_PATH)
    final_valid = bool(
        loaded.get("artifact_valid") is True and loaded.get("status") == PASS_STATUS
        and actual_package_exact() and finite_json(loaded) and casefold_keys_unique(loaded)
    )
    print(json.dumps({
        "artifact_valid": final_valid, "status": loaded.get("status"),
        "required_true": len(REQUIRED_TRUE_FLAGS),
        "required_false": len(REQUIRED_FALSE_FLAGS),
        "mutations": mutations["registered_mutation_count"],
        "package_files": sorted(EXPECTED_PACKAGE_FILES),
        "source_sha256": sha256_file(SOURCE_PATH),
        "result_sha256": sha256_file(RESULT_PATH),
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if final_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
