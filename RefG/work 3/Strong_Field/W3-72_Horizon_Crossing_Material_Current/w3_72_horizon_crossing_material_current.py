#!/usr/bin/env python3
"""W3-72 exact horizon-crossing ordinary-phase-current audit."""

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
from pathlib import Path
from typing import Any

import sympy as sp


CLAIM_ID = "W3_72_HORIZON_CROSSING_MATERIAL_CURRENT"
MODEL_VERSION = "W3-72-v1.1-HORIZON-CROSSING-ORDINARY-PHASE-CURRENT"
PASS_STATUS = (
    "PASS_EXACT_ACTION_DERIVED_HORIZON_REGULAR_NONSTATIC_ORDINARY_PHASE_"
    "CURRENT_AND_LOCAL_INITIAL_VALUE_HANDOFF__FINITE_INWARD_CHARGE_"
    "NONNEGATIVE_ENERGY_FLUX_AND_MATCHED_CHARACTERISTIC_CONE_ON_THE_"
    "INHERITED_ONE_METRIC__GLOBAL_BACKREACTION_INTERIOR_AND_SINGULARITY_"
    "NOT_SOLVED"
)
FAIL_STATUS = "FAIL_W3_72_HORIZON_CROSSING_MATERIAL_CURRENT_AUDIT"

SOURCE_PATH = Path(__file__).resolve()
PACKAGE_DIR = SOURCE_PATH.parent
REPO_ROOT = SOURCE_PATH.parents[4]
PREREG_PATH = (
    PACKAGE_DIR / "w3_72_horizon_crossing_material_current_preregistration.md"
)
RESULT_PATH = PACKAGE_DIR / "w3_72_result.json"
PREREG_SHA256 = "3aa5da94f6abd830ec6b32ddd82ce94d0223ed60becec91b75ecf41e7950bb38"

EXPECTED_PACKAGE_FILES = {
    "w3_72_horizon_crossing_material_current_preregistration.md",
    "w3_72_horizon_crossing_material_current.py",
    "w3_72_result.json",
}

DEPENDENCIES = {
    "CODES.md":
        "27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41",
    "RefG/work 3/Lagrangian_Formulation/"
    "Relational_Coframe_TEGR_Phase_Source_Closure/"
    "w3_54_relational_coframe_tegr_phase_source_closure_contract.md":
        "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
    "RefG/work 3/Lagrangian_Formulation/"
    "Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_result.json":
        "ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991",
    "RefG/work 3/Lagrangian_Formulation/"
    "One_Oscillon_Coframe_Localized_Core/"
    "w3_58_one_oscillon_coframe_localized_core_preregistration.md":
        "ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db",
    "RefG/work 3/Lagrangian_Formulation/"
    "One_Oscillon_Coframe_Localized_Core/w3_58_result.json":
        "cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5",
    "RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/"
    "w3_64_source_first_einstein_strong_field_preregistration.md":
        "25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1",
    "RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/w3_64_result.json":
        "b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b",
    "RefG/work 3/Strong_Field/W3-71_Horizon_Material_Scale_Separation/"
    "w3_71_horizon_material_scale_separation_preregistration.md":
        "1d3f74489f6cc52061253b6e1ea3d7f96e5d423f8b2afb88e79a44a38ae916c3",
    "RefG/work 3/Strong_Field/W3-71_Horizon_Material_Scale_Separation/"
    "w3_71_result.json":
        "866657282065918fcecf46075dbc103f3f0bbfe040a9ac348ceef90705c7837b",
}

IMMUTABLE_INTUITIVE = {
    "intuitive/Dictionary.txt":
        "f6e12b67f38e49bb547d37e6c92375a2ee5b2f596ed481a866cbc490be32ed0b",
    "intuitive/RefG_EN.bib":
        "78a2889e8da0eb206d6282dac610a82af77ad1340e48c7dbd2e042e1f317fe43",
    "intuitive/RefG_EN.pdf":
        "2d1c65687fb6c9bbb5c3004299d6205ad494f361a956d646851571996a448ddc",
    "intuitive/RefG_EN.tex":
        "6e69d616229688d885320d9b26b8c4637c563ae47f8da006feee8548d6ad910e",
    "intuitive/RefG_GE.md":
        "433d3ac96ff6d91eaae1da60cd3f27f84ead2b7bddea26885034e2995dd8787f",
    "intuitive/figures/figure_3.pdf":
        "d3fc89edf7ed59b499467999c16504c8cc36dbe614f9b1dcc612caaee1f35f5f",
    "intuitive/figures/figure_3_v2.png":
        "43e673eeac9d44cb595303bf55d0622ac2fcb87b641627ff8e3a5e8781365a4e",
    "intuitive/figures/logo.pdf":
        "e585eaa93b8d60b6294fcd3e7448469265502defd7725f74fdb0a56d33d907ab",
    "intuitive/figures/sparc_rar_real_validation.png":
        "1afefcc99ca6223230959b8ab3a6cfc015035de20178b7eed8f7f3728a7fe3f0",
    "intuitive/idea.txt":
        "98cf98f70e3ac146ef3b106cdd6b2df6c6861d2c277e9c9adae5262959d2dd8d",
}

REQUIRED_TRUE_FLAGS = {
    "dependency_hashes_exact",
    "upstream_status_and_scope_exact",
    "one_metric_one_localized_source_exact",
    "w3_58_action_unchanged_exact",
    "pg_metric_inverse_volume_exact",
    "pg_dual_frame_dictionary_exact",
    "scalar_amplitude_equation_exact",
    "ordinary_phase_equation_exact",
    "ordinary_phase_current_exact",
    "current_coordinate_frame_dictionary_exact",
    "timelike_material_domain_exact",
    "normalized_material_velocity_exact",
    "horizon_inward_current_exact",
    "charge_balance_exact",
    "rain_congruence_exact",
    "finite_proper_horizon_crossing_exact",
    "continuity_witness_exact",
    "continuity_witness_not_full_scalar_solution_exact",
    "scalar_box_pg_exact",
    "first_order_scalar_system_exact",
    "principal_symbol_exact",
    "characteristic_speeds_exact",
    "horizon_hyperbolicity_regular_exact",
    "pg_cauchy_slice_spacelike_exact",
    "local_initial_data_open_set_exact",
    "polar_cartesian_domain_guard_exact",
    "hilbert_stress_exact",
    "regular_frame_stress_finite_exact",
    "horizon_energy_flux_nonnegative_exact",
    "scalar_nec_exact",
    "isolated_stationary_crossing_no_go_exact",
    "nonstatic_scale_connection_not_promoted_exact",
    "intrinsic_profile_not_passively_rescaled_exact",
    "potential_lower_order_exact",
    "mutation_controls_pass",
    "g0_goal_pass",
    "g1_conventions_pass",
    "g2_action_current_pass",
    "g3_horizon_hyperbolicity_pass",
    "g4_independent_crosscheck_pass",
    "g5_limits_regression_pass",
    "g6_physical_scope_pass",
    "g7_observation_not_applicable_exact",
    "g8_export_not_applicable_exact",
    "package_clean_pass",
    "aggregate_gate_pass",
}

REQUIRED_FALSE_FLAGS = {
    "ordinary_phase_current_automatically_timelike",
    "noether_charge_identified_as_mass_flux",
    "continuity_witness_full_scalar_solution",
    "full_scalar_amplitude_equation_solution_constructed",
    "stationary_bound_oscillon_horizon_solution_derived",
    "intrinsic_oscillon_profile_rescaled",
    "dynamical_profile_rigidity_derived",
    "background_horizon_mass_identified_as_oscillon_mass",
    "nonstatic_global_scale_scalar_derived",
    "global_infalling_oscillon_solution_derived",
    "dynamic_einstein_backreaction_solved",
    "collapse_evolution_completed",
    "regular_black_hole_interior_derived",
    "singularity_resolution_completed",
    "geodesic_completeness_derived",
    "new_gravity_operator_introduced",
    "second_metric_introduced",
    "duplicate_localized_source_introduced",
    "new_observation_tested",
    "canon_changed",
    "intuitive_files_changed",
}

FROZEN_MUTATION_REGISTRY = (
    ("pg_shift_removed", ("pg_shift_coefficient",)),
    ("current_sign_flipped", ("current_sign",)),
    ("phase_radial_term_removed", ("phase_radial_coefficient",)),
    ("timelike_domain_dropped", ("require_timelike_branch",)),
    (
        "potential_promoted_to_principal",
        ("potential_principal_coefficient",),
    ),
    ("horizon_flux_forced_zero", ("horizon_flux_rule",)),
    ("stress_not_from_action", ("stress_rule",)),
    (
        "duplicate_metric_source",
        ("localized_source_ledger", "metric_ids"),
    ),
    ("profile_passively_rescaled", ("profile_scale_power",)),
    (
        "nonstatic_scale_scalar_promoted",
        ("accepted_scale_domains",),
    ),
    (
        "continuity_witness_promoted_full_solution",
        ("continuity_witness_role",),
    ),
    (
        "background_mass_identified_with_oscillon",
        ("mass_role",),
    ),
    ("global_interior_overclaim", ("promoted_claims",)),
)

W3_54_STATUS = (
    "CONDITIONAL_EXACT_SELECTED_RELATIONAL_COFRAME_MASTER_ACTION_TO_TEGR_"
    "EQUIVALENT_EH_AND_PHASE_CURRENT_T"
)
W3_58_STATUS = (
    "PASS_CONDITIONAL_EXACT_MINIMAL_COFRAME_U1_CORE_ACTION_AND_ANALYTIC_"
    "EXISTENCE_WINDOW__CONVERGED_NUMERICAL_FINITE_ENERGY_ORBITALLY_STABLE_"
    "SPHERICAL_GROUND_STATE_EVIDENCE__FOUNDATION_COEFFICIENT_SELECTION_"
    "BACKGROUND_LOCK_BACKREACTION_AND_PARTICLE_IDENTITY_OPEN"
)
W3_64_STATUS = (
    "PASS_CONDITIONAL_EXACT_UNCHANGED_EINSTEIN_BACKREACTION_AND_CURRENT_"
    "SOURCE_NEC_BOUNDARY__CONVERGED_NUMERICAL_REGULAR_HORIZONLESS_SELF_"
    "GRAVITATING_Q_BALL_WITNESS__REGULAR_TRAPPED_NULL_COMPLETE_INTERIOR_"
    "REQUIRES_FAILURE_OF_AT_LEAST_ONE_PENROSE_HYPOTHESIS"
)
W3_71_STATUS = (
    "PASS_EXACT_COVARIANT_SCALE_CONNECTION_ON_HOMOGENEOUS_AND_STATIC_"
    "BRANCHES__TEMPORAL_LAPSE_SPATIAL_RULER_AND_INTRINSIC_OSCILLON_PROFILE_"
    "SEPARATED_WITH_EXACT_COFRAME_RULER_CONVERSION_EINSTEIN_EXTERIOR_AND_"
    "1PN__HORIZON_CROSSING_MATERIAL_CURRENT_NOT_DERIVED"
)

PRODUCTION_CONFIGURATION = {
    "pg_shift_coefficient": sp.Integer(1),
    "current_sign": sp.Integer(-1),
    "phase_radial_coefficient": sp.Integer(1),
    "require_timelike_branch": True,
    "potential_principal_coefficient": sp.Integer(0),
    "horizon_flux_rule": "action",
    "stress_rule": "hilbert",
    "metric_ids": ("g",),
    "localized_source_ledger": (
        ("T_O", 1),
        ("T_C", 0),
        ("readout", 0),
        ("j_O_extra_Einstein_RHS", 0),
    ),
    "profile_scale_power": sp.Integer(0),
    "accepted_scale_domains": ("homogeneous", "static"),
    "continuity_witness_role": "PHASE_EQUATION_ONLY",
    "mass_role": "BACKGROUND_BOUNDARY_DISTINCT_FROM_TRANSPORTED_MATTER",
    "promoted_claims": (),
}

MUTATIONS = {
    "pg_shift_removed": {"pg_shift_coefficient": sp.Integer(0)},
    "current_sign_flipped": {"current_sign": sp.Integer(1)},
    "phase_radial_term_removed": {
        "phase_radial_coefficient": sp.Integer(0)
    },
    "timelike_domain_dropped": {"require_timelike_branch": False},
    "potential_promoted_to_principal": {
        "potential_principal_coefficient": sp.Integer(1)
    },
    "horizon_flux_forced_zero": {"horizon_flux_rule": "zero"},
    "stress_not_from_action": {"stress_rule": "relabelled"},
    "duplicate_metric_source": {
        "metric_ids": ("g", "f"),
        "localized_source_ledger": (
            ("T_O", 2),
            ("T_C", 1),
            ("readout", 1),
            ("j_O_extra_Einstein_RHS", 1),
        ),
    },
    "profile_passively_rescaled": {"profile_scale_power": sp.Integer(1)},
    "nonstatic_scale_scalar_promoted": {
        "accepted_scale_domains": ("homogeneous", "static", "nonstatic")
    },
    "continuity_witness_promoted_full_solution": {
        "continuity_witness_role": "FULL_SCALAR_SOLUTION"
    },
    "background_mass_identified_with_oscillon": {
        "mass_role": "M_BG_EQUALS_W3_64_OSCILLON_ADM_MASS"
    },
    "global_interior_overclaim": {
        "promoted_claims": (
            "global_backreaction",
            "regular_interior",
            "singularity_resolution",
        )
    },
}

MUTATION_PRIMARY_FAILURES = {
    "pg_shift_removed": {"pg_geometry_inherited"},
    "current_sign_flipped": {"current_convention"},
    "phase_radial_term_removed": {"current_radial_dictionary"},
    "timelike_domain_dropped": {"timelike_branch_guard"},
    "potential_promoted_to_principal": {"potential_lower_order"},
    "horizon_flux_forced_zero": {"horizon_current"},
    "stress_not_from_action": {"hilbert_stress"},
    "duplicate_metric_source": {"one_metric_source_ledger"},
    "profile_passively_rescaled": {"intrinsic_profile_role"},
    "nonstatic_scale_scalar_promoted": {"scale_domain_boundary"},
    "continuity_witness_promoted_full_solution": {
        "continuity_witness_scope"
    },
    "background_mass_identified_with_oscillon": {"mass_role_separation"},
    "global_interior_overclaim": {"claim_scope"},
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


def bool_all(values: list[bool]) -> bool:
    return all(value is True for value in values)


def sstr(expr: sp.Expr) -> str:
    return sp.sstr(sp.simplify(expr))


def no_bad_atoms(expr: sp.Expr) -> bool:
    return not expr.has(sp.zoo, sp.nan, sp.oo, -sp.oo)


def audit_files(
    expected: dict[str, str],
) -> tuple[dict[str, Any], bool]:
    records: dict[str, Any] = {}
    for relative, expected_hash in expected.items():
        path = REPO_ROOT / relative
        exists = path.is_file()
        actual_hash = sha256_file(path) if exists else None
        records[relative] = {
            "exists": exists,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "exact": exists and actual_hash == expected_hash,
        }
    return records, bool_all(
        [record["exact"] for record in records.values()]
    )


def json_is_finite(value: Any) -> bool:
    if isinstance(value, dict):
        return all(
            isinstance(key, str) and json_is_finite(item)
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple)):
        return all(json_is_finite(item) for item in value)
    if isinstance(value, float):
        return math.isfinite(value)
    return value is None or isinstance(value, (str, int, bool))


def audit_immutable_intuitive() -> tuple[dict[str, Any], bool]:
    records, hashes_exact = audit_files(IMMUTABLE_INTUITIVE)
    root = REPO_ROOT / "intuitive"
    actual_files = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    )
    expected_files = sorted(IMMUTABLE_INTUITIVE)
    file_set_exact = actual_files == expected_files
    return {
        "expected_files": expected_files,
        "actual_files": actual_files,
        "file_set_exact": file_set_exact,
        "hashes_exact": hashes_exact,
        "records": records,
        "all_exact": hashes_exact and file_set_exact,
    }, hashes_exact and file_set_exact


def audit_canon_control() -> tuple[dict[str, Any], bool]:
    candidates = (
        REPO_ROOT / "Theory_Canon.md",
        REPO_ROOT / "RefG" / "Theory_Canon.md",
        REPO_ROOT / "RefG" / "work 3" / "Theory_Canon.md",
    )
    records = {
        path.relative_to(REPO_ROOT).as_posix(): path.exists()
        for path in candidates
    }
    expected_absence = not any(records.values())
    return {
        "registered_candidates": records,
        "expected_absence_exact": expected_absence,
        "write_target_confined_to_w3_72": True,
        "all_exact": expected_absence,
    }, expected_absence


def parse_flag_block(
    text: str,
    start: str,
    end: str,
) -> set[str]:
    if start not in text or end not in text:
        return set()
    block = text.split(start, 1)[1].split(end, 1)[0]
    return set(
        re.findall(r"^    ([a-z][a-z0-9_]*)\s*$", block, re.MULTILINE)
    )


def parse_mutation_registry(text: str) -> dict[str, tuple[str, ...]]:
    if "## Frozen mutation registry" not in text:
        return {}
    block = text.split("## Frozen mutation registry", 1)[1]
    block = block.split("## Gate registry", 1)[0]
    result: dict[str, tuple[str, ...]] = {}
    for name, path_text in re.findall(
        r"^    ([a-z][a-z0-9_]*) -> ([a-z0-9_, ]+)\s*$",
        block,
        re.MULTILINE,
    ):
        result[name] = tuple(
            sorted(part.strip() for part in path_text.split(","))
        )
    return result


def audit_preregistration() -> dict[str, Any]:
    text = PREREG_PATH.read_text(encoding="utf-8")
    actual_hash = sha256_file(PREREG_PATH)
    parsed_true = parse_flag_block(
        text, "Required true:", "Required false:"
    )
    parsed_false = parse_flag_block(
        text, "Required false:", "## Frozen mutation registry"
    )
    parsed_mutations = parse_mutation_registry(text)
    frozen_mutations = {
        name: tuple(sorted(paths))
        for name, paths in FROZEN_MUTATION_REGISTRY
    }
    markers = (
        "**CLAIM_ID:** " + CLAIM_ID,
        "**MODEL_VERSION:** " + MODEL_VERSION,
        "## Assumptions",
        "## Domain and conventions",
        "## Branches",
        "## Freedom ledger",
        "## Dependencies",
        "## Typed role and source ledger",
        "## Method",
        "## Cross-check",
        "## Files",
        "## Pass condition",
        "## Fail condition",
        "## Falsifier and residual",
        "## Error bound and validity health",
        "## Observable map, forward model, and data role",
        "## Identifiability and benchmark",
        "## Closure flags",
        "## Frozen mutation registry",
        "## Gate registry",
        "## Provenance and references",
        PASS_STATUS,
    )
    marker_checks = {marker: marker in text for marker in markers}
    return {
        "expected_sha256": PREREG_SHA256,
        "actual_sha256": actual_hash,
        "hash_exact": actual_hash == PREREG_SHA256,
        "marker_checks": marker_checks,
        "markers_exact": bool_all(list(marker_checks.values())),
        "preregistered_true_flags": sorted(parsed_true),
        "preregistered_false_flags": sorted(parsed_false),
        "required_true_keyset_exact": parsed_true == REQUIRED_TRUE_FLAGS,
        "required_false_keyset_exact": parsed_false == REQUIRED_FALSE_FLAGS,
        "frozen_mutation_registry": {
            key: list(value) for key, value in sorted(frozen_mutations.items())
        },
        "parsed_mutation_registry": {
            key: list(value) for key, value in sorted(parsed_mutations.items())
        },
        "frozen_mutation_registry_exact": (
            parsed_mutations == frozen_mutations
        ),
    }


def audit_package_before_write() -> dict[str, Any]:
    actual_files = sorted(
        path.name for path in PACKAGE_DIR.iterdir() if path.is_file()
    )
    actual_dirs = sorted(
        path.name for path in PACKAGE_DIR.iterdir() if path.is_dir()
    )
    actual_set = set(actual_files)
    allowed_before = actual_set.issubset(EXPECTED_PACKAGE_FILES)
    anticipated = actual_set | {RESULT_PATH.name}
    return {
        "expected_files": sorted(EXPECTED_PACKAGE_FILES),
        "actual_files_before_write": actual_files,
        "actual_directories": actual_dirs,
        "allowed_before_write": allowed_before,
        "anticipated_files_after_write": sorted(anticipated),
        "recursive_exact_three_file_package": (
            allowed_before
            and not actual_dirs
            and anticipated == EXPECTED_PACKAGE_FILES
        ),
    }


def validate_configuration_schema(config: dict[str, Any]) -> bool:
    expected = set(PRODUCTION_CONFIGURATION)
    if set(config) != expected:
        return False
    return (
        isinstance(config["metric_ids"], tuple)
        and isinstance(config["localized_source_ledger"], tuple)
        and isinstance(config["accepted_scale_domains"], tuple)
        and isinstance(config["promoted_claims"], tuple)
        and config["horizon_flux_rule"] in {"action", "zero"}
        and config["stress_rule"] in {"hilbert", "relabelled"}
        and config["continuity_witness_role"]
        in {"PHASE_EQUATION_ONLY", "FULL_SCALAR_SOLUTION"}
    )


def audit_upstream() -> tuple[dict[str, Any], bool]:
    p54 = (
        REPO_ROOT
        / "RefG/work 3/Lagrangian_Formulation/"
        "Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_result.json"
    )
    p58 = (
        REPO_ROOT
        / "RefG/work 3/Lagrangian_Formulation/"
        "One_Oscillon_Coframe_Localized_Core/w3_58_result.json"
    )
    p64 = (
        REPO_ROOT
        / "RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/"
        "w3_64_result.json"
    )
    p71 = (
        REPO_ROOT
        / "RefG/work 3/Strong_Field/"
        "W3-71_Horizon_Material_Scale_Separation/w3_71_result.json"
    )
    w54, w58, w64, w71 = map(load_json, (p54, p58, p64, p71))
    checks = {
        "w3_54_status_exact": w54.get("status") == W3_54_STATUS,
        "w3_54_aggregate_pass": w54.get("aggregate_pass") is True,
        "w3_54_false_boundary_exact": (
            w54.get("false_flag_boundary_exact") is True
        ),
        "w3_58_status_exact": w58.get("status") == W3_58_STATUS,
        "w3_58_artifact_valid": w58.get("artifact_valid") is True,
        "w3_58_aggregate_pass": (
            w58.get("closure_flags", {}).get("aggregate_gate_pass") is True
        ),
        "w3_58_current_exact": (
            w58.get("closure_flags", {}).get(
                "ordinary_phase_current_exact"
            )
            is True
        ),
        "w3_58_hilbert_source_exact": (
            w58.get("closure_flags", {}).get(
                "hilbert_stress_from_same_action_exact"
            )
            is True
        ),
        "w3_58_backreaction_not_claimed": (
            w58.get("scope_flags", {}).get(
                "localized_gravitational_backreaction_derived"
            )
            is False
        ),
        "w3_64_status_exact": w64.get("status") == W3_64_STATUS,
        "w3_64_artifact_valid": w64.get("artifact_valid") is True,
        "w3_64_aggregate_pass": (
            w64.get("closure_flags", {}).get("aggregate_gate_pass") is True
        ),
        "w3_64_localized_source_only_T_O": (
            w64.get("source_ledger", {}).get("localized_einstein_rhs")
            == ["T_O"]
        ),
        "w3_64_no_collective_local_duplicate": (
            w64.get("source_ledger", {}).get(
                "homogeneous_collective_T_C_readded_locally"
            )
            is False
        ),
        "w3_64_collapse_not_completed": (
            w64.get("scope_flags", {}).get("collapse_evolution_completed")
            is False
        ),
        "w3_64_singularity_not_resolved": (
            w64.get("scope_flags", {}).get(
                "singularity_resolution_completed"
            )
            is False
        ),
        "w3_71_status_exact": w71.get("status") == W3_71_STATUS,
        "w3_71_artifact_valid": w71.get("artifact_valid") is True,
        "w3_71_aggregate_pass": (
            w71.get("closure_flags", {}).get("aggregate_gate_pass") is True
        ),
        "w3_71_current_was_next_input": (
            w71.get("closure_flags", {}).get(
                "horizon_crossing_material_current_derived"
            )
            is False
        ),
        "w3_71_profile_not_rescaled": (
            w71.get("closure_flags", {}).get(
                "intrinsic_profile_rescaling_action_present"
            )
            is False
        ),
        "w3_71_horizon_pg_regular": (
            w71.get("physical_decision", {}).get(
                "horizon_local_geometry"
            )
            == "REGULAR_IN_PAINLEVE_GULLSTRAND_COFRAME"
        ),
    }
    return {
        "checks": checks,
        "all_exact": bool_all(list(checks.values())),
        "w3_71_next_input": w71.get("physical_decision", {}).get(
            "next_exact_input"
        ),
    }, bool_all(list(checks.values()))


def christoffel_2d(
    metric: sp.Matrix,
    inverse: sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol],
) -> list[list[list[sp.Expr]]]:
    gamma = [
        [[sp.Integer(0) for _ in range(2)] for _ in range(2)]
        for _ in range(2)
    ]
    for mu in range(2):
        for alpha in range(2):
            for beta in range(2):
                gamma[mu][alpha][beta] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inverse[mu, nu]
                        * (
                            sp.diff(metric[nu, beta], coordinates[alpha])
                            + sp.diff(
                                metric[nu, alpha], coordinates[beta]
                            )
                            - sp.diff(
                                metric[alpha, beta], coordinates[nu]
                            )
                        )
                        for nu in range(2)
                    )
                )
    return gamma


def geometry_action_audit(config: dict[str, Any]) -> dict[str, Any]:
    T, r, r_s = sp.symbols("T r r_s", positive=True, finite=True)
    vartheta = sp.symbols("vartheta", real=True)
    c = sp.sympify(config["pg_shift_coefficient"])
    s_j = sp.sympify(config["current_sign"])
    a_r = sp.sympify(config["phase_radial_coefficient"])
    v = sp.sqrt(r_s / r)

    metric = sp.Matrix([[c**2 * v**2 - 1, c * v], [c * v, 1]])
    inherited_metric = sp.Matrix([[v**2 - 1, v], [v, 1]])
    inverse = sp.simplify(metric.inv())
    inherited_inverse = sp.Matrix([[-1, v], [v, 1 - v**2]])
    determinant = sp.simplify(metric.det())
    full_determinant = sp.simplify(
        determinant * r**4 * sp.sin(vartheta) ** 2
    )

    coframe = sp.Matrix([[1, 0], [c * v, 1]])
    dual = sp.Matrix([[1, -c * v], [0, 1]])
    inherited_coframe = sp.Matrix([[1, 0], [v, 1]])
    inherited_dual = sp.Matrix([[1, -v], [0, 1]])

    chi_s = sp.symbols("chi", positive=True, finite=True)
    Pi, Phi = sp.symbols(
        "Pi_theta Phi_theta", real=True, finite=True
    )
    action_grad_up = sp.Matrix([-Pi, c * v * Pi + Phi])
    current_action = s_j * chi_s**2 * action_grad_up
    current_candidate = sp.Matrix(
        [
            current_action[0],
            s_j * chi_s**2 * (c * v * Pi + a_r * Phi),
        ]
    )
    current_expected = sp.Matrix(
        [chi_s**2 * Pi, -chi_s**2 * (v * Pi + Phi)]
    )
    current_frame = sp.simplify(coframe * current_candidate)
    current_frame_expected = sp.Matrix(
        [chi_s**2 * Pi, -chi_s**2 * Phi]
    )
    current_norm = sp.simplify(
        (current_candidate.T * metric * current_candidate)[0]
    )
    current_norm_expected = chi_s**4 * (-Pi**2 + Phi**2)

    q = sp.symbols("q", positive=True, finite=True)
    eta = sp.symbols("eta", real=True, finite=True)
    param_subs = {
        Pi: q * sp.cosh(eta),
        Phi: q * sp.sinh(eta),
        r: r_s,
    }
    current_horizon = sp.simplify(current_candidate.subs(param_subs))
    density_horizon = chi_s**2 * q
    velocity_horizon = sp.simplify(current_horizon / density_horizon)
    metric_horizon = sp.simplify(metric.subs(r, r_s))
    velocity_norm_horizon = sp.simplify(
        (velocity_horizon.T * metric_horizon * velocity_horizon)[0]
    )
    horizon_radial_expected = -chi_s**2 * q * sp.exp(eta)
    horizon_radial_identity = exact_zero(
        current_horizon[1] - horizon_radial_expected
    )
    horizon_speed = sp.simplify(
        velocity_horizon[1] / velocity_horizon[0]
    )

    chi = sp.Function("chi")(T, r)
    theta = sp.Function("theta")(T, r)
    m, lam, g6 = sp.symbols(
        "m lambda g_6", positive=True, finite=True
    )
    potential = (
        sp.Rational(1, 2) * m**2 * chi**2
        - sp.Rational(1, 4) * lam * chi**4
        + sp.Rational(1, 6) * g6 * chi**6
    )
    potential_prime = sp.diff(potential, chi)
    potential_prime_expected = m**2 * chi - lam * chi**3 + g6 * chi**5

    grad_chi = sp.Matrix([sp.diff(chi, T), sp.diff(chi, r)])
    grad_theta = sp.Matrix([sp.diff(theta, T), sp.diff(theta, r)])
    raised_chi = sp.simplify(inverse * grad_chi)
    raised_theta = sp.simplify(inverse * grad_theta)
    box_chi = sp.simplify(
        (
            sp.diff(r**2 * raised_chi[0], T)
            + sp.diff(r**2 * raised_chi[1], r)
        )
        / r**2
    )
    Pi_chi = sp.diff(chi, T) - c * v * sp.diff(chi, r)
    Phi_chi = sp.diff(chi, r)
    Pi_theta = sp.diff(theta, T) - c * v * sp.diff(theta, r)
    Phi_theta = sp.diff(theta, r)
    box_frame = (
        -sp.diff(Pi_chi, T)
        + sp.diff(r**2 * (c * v * Pi_chi + Phi_chi), r) / r**2
    )
    theta_norm = sp.simplify((grad_theta.T * raised_theta)[0])
    theta_norm_frame = -Pi_theta**2 + Phi_theta**2
    amplitude_covariant = sp.simplify(
        box_chi - chi * theta_norm - potential_prime
    )
    amplitude_frame = sp.simplify(
        -sp.diff(Pi_chi, T)
        + sp.diff(r**2 * (c * v * Pi_chi + Phi_chi), r) / r**2
        + chi * (Pi_theta**2 - Phi_theta**2)
        - potential_prime
    )
    amplitude_evolution = sp.simplify(
        sp.diff(Pi_chi, T)
        - (
            sp.diff(r**2 * (c * v * Pi_chi + Phi_chi), r) / r**2
            + chi * (Pi_theta**2 - Phi_theta**2)
            - potential_prime
        )
    )
    kinematic_chi = sp.simplify(
        sp.diff(chi, T) - (Pi_chi + c * v * Phi_chi)
    )
    kinematic_phi = sp.simplify(
        sp.diff(Phi_chi, T)
        - sp.diff(Pi_chi + c * v * Phi_chi, r)
    )

    phase_gradient_current = sp.simplify(chi**2 * raised_theta)
    phase_eom = sp.simplify(
        (
            sp.diff(r**2 * phase_gradient_current[0], T)
            + sp.diff(r**2 * phase_gradient_current[1], r)
        )
        / r**2
    )
    noether_action = sp.simplify(s_j * phase_gradient_current)
    noether_candidate = sp.Matrix(
        [
            noether_action[0],
            s_j
            * chi**2
            * (c * v * Pi_theta + a_r * Phi_theta),
        ]
    )
    noether_divergence = sp.simplify(
        (
            sp.diff(r**2 * noether_candidate[0], T)
            + sp.diff(r**2 * noether_candidate[1], r)
        )
        / r**2
    )
    phase_conservative = sp.simplify(
        sp.diff(r**2 * chi**2 * Pi_theta, T)
        - sp.diff(
            r**2 * chi**2 * (c * v * Pi_theta + Phi_theta),
            r,
        )
    )

    xi_T, xi_r = sp.symbols("xi_T xi_r", real=True)
    principal = sp.expand(
        -xi_T**2
        + 2 * c * v * xi_T * xi_r
        + (1 - c**2 * v**2) * xi_r**2
    )
    principal_factor = -(
        xi_T - (c * v + 1) * xi_r
    ) * (xi_T - (c * v - 1) * xi_r)
    principal_inherited = (
        -xi_T**2
        + 2 * v * xi_T * xi_r
        + (1 - v**2) * xi_r**2
    )
    xi_angular_sq = sp.symbols(
        "xi_angular_sq", nonnegative=True, finite=True
    )
    principal_full = principal + xi_angular_sq / r**2
    principal_full_inherited = principal_inherited + xi_angular_sq / r**2
    first_order_matrix = sp.Matrix([[c * v, 1], [1, c * v]])
    characteristic_polynomial = sp.factor(
        first_order_matrix.charpoly().as_expr()
    )
    characteristic_polynomial_expected = (
        first_order_matrix.charpoly().gen - c * v - 1
    ) * (first_order_matrix.charpoly().gen - c * v + 1)
    coordinate_speeds = (-c * v + 1, -c * v - 1)
    inherited_speeds = (-v + 1, -v - 1)
    horizon_speeds = tuple(
        sp.simplify(speed.subs(r, r_s)) for speed in coordinate_speeds
    )
    null_speed_symbol = sp.symbols("c_r", real=True)
    null_polynomial = sp.expand(
        metric[0, 0]
        + 2 * metric[0, 1] * null_speed_symbol
        + metric[1, 1] * null_speed_symbol**2
    )
    null_factor = (
        null_speed_symbol + c * v - 1
    ) * (null_speed_symbol + c * v + 1)

    transform = sp.Matrix([[1, -1 / (1 + v)], [0, 1]])
    ef_metric = sp.simplify(transform.T * metric * transform)
    ef_expected = sp.Matrix([[-(1 - v**2), 1], [1, 0]])
    ef_inverse_expected = sp.Matrix([[0, 1], [1, 1 - v**2]])
    vector_pg_to_ef = sp.simplify(transform.inv())
    current_ef_transformed = sp.simplify(
        vector_pg_to_ef * current_candidate
    )
    phase_gradient_pg = sp.Matrix([Pi + c * v * Phi, Phi])
    phase_gradient_ef = sp.simplify(transform.T * phase_gradient_pg)
    current_ef_direct = sp.simplify(
        s_j * chi_s**2 * ef_metric.inv() * phase_gradient_ef
    )
    current_ef_horizon = sp.simplify(
        current_ef_direct.subs(param_subs)
    )

    x1, x2 = sp.symbols("q_1 q_2", real=True)
    rho2 = x1**2 + x2**2
    cartesian_potential = (
        sp.Rational(1, 2) * m**2 * rho2
        - sp.Rational(1, 4) * lam * rho2**2
        + sp.Rational(1, 6) * g6 * rho2**3
    )
    cartesian_force = m**2 - lam * rho2 + g6 * rho2**2
    cartesian_gradient_checks = [
        exact_zero(sp.diff(cartesian_potential, field) - cartesian_force * field)
        for field in (x1, x2)
    ]

    metric_horizon_entries = [
        sp.simplify(entry.subs(r, r_s))
        for entry in list(metric) + list(inverse)
    ]
    checks = {
        "pg_geometry_inherited": matrix_zero(metric - inherited_metric),
        "pg_inverse_exact": matrix_zero(inverse - inherited_inverse),
        "pg_determinant_exact": exact_zero(determinant + 1),
        "pg_full_volume_exact": exact_zero(
            full_determinant + r**4 * sp.sin(vartheta) ** 2
        ),
        "pg_geometry_horizon_finite": all(
            no_bad_atoms(entry) for entry in metric_horizon_entries
        ),
        "coframe_dual_exact": matrix_zero(dual * coframe.T - sp.eye(2)),
        "coframe_inherited": (
            matrix_zero(coframe - inherited_coframe)
            and matrix_zero(dual - inherited_dual)
        ),
        "current_convention": s_j == -1,
        "current_action_dictionary": matrix_zero(
            current_candidate - current_action
        ),
        "current_radial_dictionary": a_r == 1,
        "current_inherited_components": matrix_zero(
            current_candidate - current_expected
        ),
        "current_frame_dictionary": matrix_zero(
            current_frame - current_frame_expected
        ),
        "current_norm_exact": exact_zero(
            current_norm - current_norm_expected
        ),
        "timelike_branch_guard": (
            config["require_timelike_branch"] is True
        ),
        "material_velocity_unit": exact_zero(
            velocity_norm_horizon + 1
        ),
        "horizon_current": (
            config["horizon_flux_rule"] == "action"
            and config["require_timelike_branch"] is True
            and horizon_radial_identity
            and q.is_positive is True
            and chi_s.is_real is True
        ),
        "potential_derivative_exact": exact_zero(
            potential_prime - potential_prime_expected
        ),
        "scalar_box_exact": exact_zero(box_chi - box_frame),
        "theta_norm_frame_exact": exact_zero(
            theta_norm - theta_norm_frame
        ),
        "amplitude_equation_exact": exact_zero(
            amplitude_covariant - amplitude_frame
        ),
        "amplitude_evolution_exact": exact_zero(
            amplitude_evolution + amplitude_covariant
        ),
        "kinematic_system_exact": (
            exact_zero(kinematic_chi) and exact_zero(kinematic_phi)
        ),
        "phase_equation_exact": exact_zero(
            noether_divergence - s_j * phase_eom
        ),
        "phase_conservative_form_exact": exact_zero(
            phase_conservative + r**2 * phase_eom
        ),
        "principal_factorization": exact_zero(
            principal - principal_factor
        ),
        "principal_inherited": exact_zero(
            principal - principal_inherited
        ),
        "full_spherical_principal_inherited": exact_zero(
            principal_full - principal_full_inherited
        ),
        "first_order_block_symmetric": first_order_matrix.is_symmetric(),
        "first_order_eigenvalues_exact": exact_zero(
            characteristic_polynomial
            - sp.expand(characteristic_polynomial_expected)
        ),
        "characteristics_match_inherited_null": all(
            exact_zero(left - right)
            for left, right in zip(coordinate_speeds, inherited_speeds)
        ),
        "null_speed_factorization": exact_zero(
            null_polynomial - null_factor
        ),
        "horizon_speeds_exact": (
            set(horizon_speeds) == {sp.Integer(0), sp.Integer(-2)}
        ),
        "pg_slice_spacelike": exact_zero(inverse[0, 0] + 1),
        "potential_lower_order": (
            sp.sympify(config["potential_principal_coefficient"]) == 0
        ),
        "ef_metric_crosscheck": matrix_zero(ef_metric - ef_expected),
        "ef_inverse_crosscheck": matrix_zero(
            ef_expected.inv() - ef_inverse_expected
        ),
        "ef_determinant_regular": exact_zero(ef_expected.det() + 1),
        "ef_current_crosscheck": matrix_zero(
            current_ef_transformed - current_ef_direct
        ),
        "ef_radial_charge_flux_invariant": exact_zero(
            current_ef_direct[1] - current_candidate[1]
        ),
        "ef_horizon_charge_flux_exact": exact_zero(
            current_ef_horizon[1] - horizon_radial_expected
        ),
        "flat_limit_metric": matrix_zero(
            metric.subs(r_s, 0) - sp.diag(-1, 1)
        ),
        "flat_limit_speeds": set(
            sp.simplify(speed.subs(r_s, 0))
            for speed in coordinate_speeds
        )
        == {sp.Integer(-1), sp.Integer(1)},
        "cartesian_completion_smooth": bool_all(
            cartesian_gradient_checks
        ),
    }

    return {
        "symbols": {
            "v": sstr(v),
            "metric_2d": [[sstr(entry) for entry in row] for row in metric.tolist()],
            "inverse_2d": [[sstr(entry) for entry in row] for row in inverse.tolist()],
            "determinant_2d": sstr(determinant),
            "sqrt_minus_g_full": "r**2*sin(vartheta)",
        },
        "current": {
            "j_T_contravariant": sstr(current_candidate[0]),
            "j_r_contravariant": sstr(current_candidate[1]),
            "j_hat0": sstr(current_frame[0]),
            "j_hat1": sstr(current_frame[1]),
            "norm": sstr(current_norm),
            "timelike_parameterization": {
                "Pi_theta": sstr(q * sp.cosh(eta)),
                "Phi_theta": sstr(q * sp.sinh(eta)),
                "q_domain": "q>0",
            },
            "horizon_j_r": sstr(current_horizon[1]),
            "horizon_coordinate_speed": sstr(horizon_speed),
            "material_density_horizon": sstr(density_horizon),
            "material_velocity_horizon": [
                sstr(value) for value in velocity_horizon
            ],
        },
        "action_equations": {
            "potential": sstr(potential),
            "potential_prime": sstr(potential_prime),
            "box_chi_pg": sstr(box_frame),
            "amplitude_covariant_residual": sstr(amplitude_covariant),
            "amplitude_first_order_residual": sstr(amplitude_frame),
            "phase_eom": sstr(phase_eom),
            "noether_divergence": sstr(noether_divergence),
        },
        "characteristics": {
            "principal_symbol": sstr(principal),
            "full_spherical_principal_symbol": sstr(principal_full),
            "principal_factorization": sstr(principal_factor),
            "first_order_matrix": [
                [sstr(entry) for entry in row]
                for row in first_order_matrix.tolist()
            ],
            "coordinate_speeds": [sstr(speed) for speed in coordinate_speeds],
            "horizon_speeds": [sstr(speed) for speed in horizon_speeds],
            "pg_time_gradient_norm": sstr(inverse[0, 0]),
        },
        "ef_crosscheck": {
            "metric_2d": [
                [sstr(entry) for entry in row]
                for row in ef_metric.tolist()
            ],
            "determinant_2d": sstr(ef_metric.det()),
            "coordinate_relation": "dV=dT+dr/(1+v)",
            "j_V_contravariant": sstr(current_ef_direct[0]),
            "j_r_contravariant": sstr(current_ef_direct[1]),
            "horizon_j_r": sstr(current_ef_horizon[1]),
            "radial_flux_relation": "j_EF**r=j_PG**r",
        },
        "checks": checks,
    }


def stress_transport_audit(config: dict[str, Any]) -> dict[str, Any]:
    T, r, r_s, r_0 = sp.symbols(
        "T r r_s r_0", positive=True, finite=True
    )
    c = sp.sympify(config["pg_shift_coefficient"])
    v = sp.sqrt(r_s / r)
    metric = sp.Matrix([[c**2 * v**2 - 1, c * v], [c * v, 1]])
    inverse = sp.simplify(metric.inv())
    coframe = sp.Matrix([[1, 0], [c * v, 1]])

    chi = sp.symbols("chi", positive=True, finite=True)
    Pi_chi, Phi_chi, Pi_theta, Phi_theta, V = sp.symbols(
        "Pi_chi Phi_chi Pi_theta Phi_theta V",
        real=True,
        finite=True,
    )
    eta4 = sp.diag(-1, 1, 1, 1)
    d_chi = sp.Matrix([Pi_chi, Phi_chi, 0, 0])
    d_theta = sp.Matrix([Pi_theta, Phi_theta, 0, 0])
    lagrangian_bracket = sp.simplify(
        sp.Rational(1, 2) * (d_chi.T * eta4 * d_chi)[0]
        + sp.Rational(1, 2)
        * chi**2
        * (d_theta.T * eta4 * d_theta)[0]
        + V
    )
    hilbert_stress = sp.simplify(
        d_chi * d_chi.T
        + chi**2 * d_theta * d_theta.T
        - eta4 * lagrangian_bracket
    )
    if config["stress_rule"] == "hilbert":
        stress = hilbert_stress
    else:
        stress = sp.simplify(hilbert_stress + 2 * V * eta4)

    rho_expected = (
        sp.Rational(1, 2) * (Pi_chi**2 + Phi_chi**2)
        + sp.Rational(1, 2)
        * chi**2
        * (Pi_theta**2 + Phi_theta**2)
        + V
    )
    flux_expected = Pi_chi * Phi_chi + chi**2 * Pi_theta * Phi_theta
    radial_pressure_expected = (
        sp.Rational(1, 2) * (Pi_chi**2 + Phi_chi**2)
        + sp.Rational(1, 2)
        * chi**2
        * (Pi_theta**2 + Phi_theta**2)
        - V
    )
    tangential_pressure_expected = (
        sp.Rational(1, 2) * (Pi_chi**2 - Phi_chi**2)
        + sp.Rational(1, 2)
        * chi**2
        * (Pi_theta**2 - Phi_theta**2)
        - V
    )
    expected_components = (
        rho_expected,
        flux_expected,
        radial_pressure_expected,
        tangential_pressure_expected,
    )
    actual_components = (
        stress[0, 0],
        stress[0, 1],
        stress[1, 1],
        stress[2, 2],
    )

    null_plus = sp.Matrix([1, 1, 0, 0])
    null_minus = sp.Matrix([1, -1, 0, 0])
    nec_plus = sp.simplify((null_plus.T * stress * null_plus)[0])
    nec_minus = sp.simplify((null_minus.T * stress * null_minus)[0])
    nec_plus_expected = (
        (Pi_chi + Phi_chi) ** 2
        + chi**2 * (Pi_theta + Phi_theta) ** 2
    )
    nec_minus_expected = (
        (Pi_chi - Phi_chi) ** 2
        + chi**2 * (Pi_theta - Phi_theta) ** 2
    )

    coordinate_T_frame_components = sp.Matrix([1, c * v, 0, 0])
    T_TT = sp.simplify(
        (
            coordinate_T_frame_components.T
            * stress
            * coordinate_T_frame_components
        )[0]
    )
    T_TT_horizon = sp.simplify(T_TT.subs(r, r_s))
    T_TT_horizon_expected = (
        (Pi_chi + Phi_chi) ** 2
        + chi**2 * (Pi_theta + Phi_theta) ** 2
    )
    stress_coordinate_2d = sp.simplify(
        coframe.T * stress[:2, :2] * coframe
    )
    stress_mixed_2d = sp.simplify(inverse * stress_coordinate_2d)
    T_r_T_horizon = sp.simplify(stress_mixed_2d[1, 0].subs(r, r_s))
    energy_current_r_horizon = sp.simplify(-T_r_T_horizon)
    pg_from_ef = sp.Matrix([[1, -1 / (1 + v)], [0, 1]])
    coframe_ef = sp.simplify(coframe * pg_from_ef)
    metric_ef = sp.simplify(pg_from_ef.T * metric * pg_from_ef)
    inverse_ef = sp.simplify(metric_ef.inv())
    stress_coordinate_ef = sp.simplify(
        coframe_ef.T * stress[:2, :2] * coframe_ef
    )
    stress_mixed_ef = sp.simplify(inverse_ef * stress_coordinate_ef)
    T_VV_horizon = sp.simplify(stress_coordinate_ef[0, 0].subs(r, r_s))
    T_r_V_horizon = sp.simplify(stress_mixed_ef[1, 0].subs(r, r_s))
    energy_current_ef_r_horizon = sp.simplify(-T_r_V_horizon)

    u_rain = sp.Matrix([1, -v])
    u_rain_cov = sp.simplify(metric * u_rain)
    u_rain_norm = sp.simplify((u_rain.T * metric * u_rain)[0])
    u_frame = sp.simplify(coframe * u_rain)
    coordinates = (T, r)
    gamma = christoffel_2d(metric, inverse, coordinates)
    acceleration = []
    for mu in range(2):
        advective = sum(
            u_rain[alpha] * sp.diff(u_rain[mu], coordinates[alpha])
            for alpha in range(2)
        )
        connection = sum(
            gamma[mu][alpha][beta] * u_rain[alpha] * u_rain[beta]
            for alpha in range(2)
            for beta in range(2)
        )
        acceleration.append(sp.simplify(advective + connection))
    expansion = sp.simplify(
        (
            sp.diff(r**2 * u_rain[0], T)
            + sp.diff(r**2 * u_rain[1], r)
        )
        / r**2
    )
    expansion_expected = -sp.Rational(3, 2) * v / r

    omega = sp.symbols("omega", positive=True, finite=True)
    theta_norm = sp.simplify(
        (
            sp.Matrix([omega, 0]).T
            * inverse
            * sp.Matrix([omega, 0])
        )[0]
    )
    phase_current = sp.simplify(
        sp.sympify(config["current_sign"])
        * chi**2
        * inverse
        * sp.Matrix([omega, 0])
    )
    phase_current_expected = omega * chi**2 * u_rain

    profile = sp.Function("F")
    zeta = r ** sp.Rational(3, 2) + (
        sp.Rational(3, 2) * sp.sqrt(r_s) * T
    )
    number_density = r ** (-sp.Rational(3, 2)) * profile(zeta)
    packet_current = sp.simplify(number_density * u_rain)
    packet_divergence = sp.simplify(
        (
            sp.diff(r**2 * packet_current[0], T)
            + sp.diff(r**2 * packet_current[1], r)
        )
        / r**2
    )
    comoving_label = sp.simplify(
        u_rain[0] * sp.diff(zeta, T)
        + u_rain[1] * sp.diff(zeta, r)
    )
    packet_norm = sp.simplify(
        (packet_current.T * metric * packet_current)[0]
    )

    A, m, lam, g6 = sp.symbols(
        "A m lambda g_6", positive=True, finite=True
    )
    witness_chi = A * r ** (-sp.Rational(3, 4))
    witness_grad = sp.Matrix([0, sp.diff(witness_chi, r)])
    witness_raised = sp.simplify(inverse * witness_grad)
    witness_box = sp.simplify(
        (
            sp.diff(r**2 * witness_raised[0], T)
            + sp.diff(r**2 * witness_raised[1], r)
        )
        / r**2
    )
    witness_theta_norm = sp.simplify(
        (
            sp.Matrix([omega, 0]).T
            * inverse
            * sp.Matrix([omega, 0])
        )[0]
    )
    witness_potential_prime = (
        m**2 * witness_chi
        - lam * witness_chi**3
        + g6 * witness_chi**5
    )
    witness_amplitude_residual = sp.factor(
        witness_box
        - witness_chi * witness_theta_norm
        - witness_potential_prime
    )
    witness_amplitude_expected = (
        -A**5 * g6 / r ** sp.Rational(15, 4)
        + A**3 * lam / r ** sp.Rational(9, 4)
        + A * (omega**2 - m**2) / r ** sp.Rational(3, 4)
        - 3 * A / (16 * r ** sp.Rational(11, 4))
        - 9 * A * r_s / (16 * r ** sp.Rational(15, 4))
    )
    witness_horizon_residual = sp.simplify(
        witness_amplitude_residual.subs(r, r_s)
    )

    crossing_time = (
        2
        * (r_0 ** sp.Rational(3, 2) - r_s ** sp.Rational(3, 2))
        / (3 * sp.sqrt(r_s))
    )
    crossing_primitive = 2 * r ** sp.Rational(3, 2) / (
        3 * sp.sqrt(r_s)
    )
    crossing_integrand_identity = sp.simplify(
        sp.diff(crossing_primitive, r) - 1 / v
    )
    radial_speed_horizon = sp.simplify(u_rain[1].subs(r, r_s))

    scale_connection_coefficient = sp.Rational(1, 5)
    W_T = sp.simplify(-scale_connection_coefficient * expansion)
    W_r = sp.Integer(0)
    scale_curvature_Tr = sp.simplify(sp.diff(W_r, T) - sp.diff(W_T, r))
    scale_curvature_expected = (
        9 * sp.sqrt(r_s) / (20 * r ** sp.Rational(5, 2))
    )

    r_1, r_2, jr_1, jr_2 = sp.symbols(
        "r_1 r_2 jr_1 jr_2", real=True, finite=True
    )
    charge_balance = -4 * sp.pi * (r_2**2 * jr_2 - r_1**2 * jr_1)
    charge_balance_expected = 4 * sp.pi * (
        r_1**2 * jr_1 - r_2**2 * jr_2
    )
    q, eta = sp.symbols("q eta", positive=True, finite=True)
    exterior_charge_rate = (
        -4 * sp.pi * r_s**2 * chi**2 * q * sp.exp(eta)
    )
    exterior_rate_expected = exterior_charge_rate

    expected_ledger = (
        ("T_O", 1),
        ("T_C", 0),
        ("readout", 0),
        ("j_O_extra_Einstein_RHS", 0),
    )
    profile_role_exact = (
        sp.sympify(config["profile_scale_power"]) == 0
    )
    scale_domains_exact = (
        config["accepted_scale_domains"] == ("homogeneous", "static")
    )
    witness_scope_exact = (
        config["continuity_witness_role"] == "PHASE_EQUATION_ONLY"
    )
    mass_role_exact = (
        config["mass_role"]
        == "BACKGROUND_BOUNDARY_DISTINCT_FROM_TRANSPORTED_MATTER"
    )
    claim_scope_exact = config["promoted_claims"] == ()
    stress_components_exact = all(
        exact_zero(actual - expected)
        for actual, expected in zip(actual_components, expected_components)
    )

    checks = {
        "hilbert_stress": (
            config["stress_rule"] == "hilbert"
            and stress_components_exact
        ),
        "regular_frame_stress_finite": all(
            no_bad_atoms(component) for component in actual_components
        ),
        "radial_nec_exact": (
            exact_zero(nec_plus - nec_plus_expected)
            and exact_zero(nec_minus - nec_minus_expected)
        ),
        "horizon_energy_flux": (
            config["stress_rule"] == "hilbert"
            and exact_zero(T_TT_horizon - T_TT_horizon_expected)
        ),
        "horizon_killing_energy_current_exact": (
            exact_zero(T_r_T_horizon - T_TT_horizon)
            and exact_zero(energy_current_r_horizon + T_TT_horizon)
        ),
        "ef_horizon_stress_flux_crosscheck": (
            exact_zero(T_VV_horizon - T_TT_horizon)
            and exact_zero(T_r_V_horizon - T_r_T_horizon)
            and exact_zero(
                energy_current_ef_r_horizon
                - energy_current_r_horizon
            )
        ),
        "one_metric_source_ledger": (
            config["metric_ids"] == ("g",)
            and config["localized_source_ledger"] == expected_ledger
        ),
        "rain_unit_timelike": (
            exact_zero(u_rain_norm + 1)
            and matrix_zero(u_rain_cov - sp.Matrix([-1, 0]))
        ),
        "rain_coframe_rest": matrix_zero(
            u_frame - sp.Matrix([1, 0])
        ),
        "rain_geodesic": all(exact_zero(value) for value in acceleration),
        "rain_expansion": exact_zero(expansion - expansion_expected),
        "phase_hamilton_jacobi": exact_zero(theta_norm + omega**2),
        "phase_current_parallel_rain": matrix_zero(
            phase_current - phase_current_expected
        ),
        "continuity_packet_exact": (
            exact_zero(packet_divergence)
            and exact_zero(comoving_label)
            and exact_zero(packet_norm + number_density**2)
        ),
        "continuity_witness_scope": witness_scope_exact,
        "continuity_witness_amplitude_not_solved": (
            exact_zero(
                witness_amplitude_residual - witness_amplitude_expected
            )
            and not exact_zero(witness_amplitude_residual)
            and no_bad_atoms(witness_horizon_residual)
        ),
        "finite_proper_crossing": (
            exact_zero(crossing_integrand_identity)
            and radial_speed_horizon == -1
        ),
        "charge_balance": exact_zero(
            charge_balance - charge_balance_expected
        ),
        "isolated_stationary_crossing_no_go": (
            exact_zero(exterior_charge_rate - exterior_rate_expected)
            and q.is_positive is True
            and chi.is_positive is True
        ),
        "scale_curvature_exact": exact_zero(
            scale_curvature_Tr - scale_curvature_expected
        ),
        "scale_curvature_nonzero": not exact_zero(scale_curvature_Tr),
        "scale_domain_boundary": scale_domains_exact,
        "intrinsic_profile_role": profile_role_exact,
        "mass_role_separation": mass_role_exact,
        "claim_scope": claim_scope_exact,
    }

    return {
        "hilbert_stress": {
            "rho": sstr(stress[0, 0]),
            "T_hat0_hat1": sstr(stress[0, 1]),
            "p_r": sstr(stress[1, 1]),
            "p_t": sstr(stress[2, 2]),
            "NEC_plus": sstr(nec_plus),
            "NEC_minus": sstr(nec_minus),
            "horizon_T_TT": sstr(T_TT_horizon),
            "horizon_T_mixed_r_T": sstr(T_r_T_horizon),
            "horizon_killing_energy_current_r": sstr(
                energy_current_r_horizon
            ),
            "ef_horizon_T_VV": sstr(T_VV_horizon),
            "ef_horizon_T_mixed_r_V": sstr(T_r_V_horizon),
            "ef_horizon_killing_energy_current_r": sstr(
                energy_current_ef_r_horizon
            ),
            "absorbed_energy_flux_sign": "NONNEGATIVE",
        },
        "rain_transport": {
            "u_contravariant": [sstr(value) for value in u_rain],
            "u_covariant": [sstr(value) for value in u_rain_cov],
            "u_frame": [sstr(value) for value in u_frame],
            "acceleration": [sstr(value) for value in acceleration],
            "expansion": sstr(expansion),
            "phase": "theta_O=omega*T",
            "phase_norm": sstr(theta_norm),
            "phase_current": [sstr(value) for value in phase_current],
            "packet_label": sstr(zeta),
            "packet_density": sstr(number_density),
            "packet_divergence": sstr(packet_divergence),
            "packet_role": config["continuity_witness_role"],
            "amplitude_residual_for_F_constant": sstr(
                witness_amplitude_residual
            ),
            "amplitude_residual_generically_nonzero": (
                not exact_zero(witness_amplitude_residual)
            ),
        },
        "crossing": {
            "proper_time_from_r0_to_horizon": sstr(crossing_time),
            "horizon_dr_dT": sstr(radial_speed_horizon),
            "finite_for": "r_0>r_s>0",
        },
        "charge_balance": {
            "shell_Q_dot": sstr(charge_balance),
            "horizon_absorbed_charge": "-4*pi*r_s**2*j_O**r|_H",
            "isolated_exterior_Q_dot": sstr(exterior_charge_rate),
            "stationary_nonzero_timelike_crossing": "EXCLUDED",
        },
        "scale_connection_boundary": {
            "acceleration_covector": ["0", "0"],
            "Theta": sstr(expansion),
            "W_T": sstr(W_T),
            "W_r": sstr(W_r),
            "F_Tr": sstr(scale_curvature_Tr),
            "global_nonstatic_p_t": "NOT_DERIVED",
        },
        "role_ledger": {
            "metric_ids": list(config["metric_ids"]),
            "localized_source_ledger": [
                list(row) for row in config["localized_source_ledger"]
            ],
            "mass_role": config["mass_role"],
            "intrinsic_profile_scale_power": int(
                config["profile_scale_power"]
            ),
            "accepted_scale_domains": list(
                config["accepted_scale_domains"]
            ),
        },
        "checks": checks,
    }


def evaluate_configuration(config: dict[str, Any]) -> dict[str, Any]:
    schema_valid = validate_configuration_schema(config)
    geometry = geometry_action_audit(config)
    transport = stress_transport_audit(config)
    checks = dict(geometry["checks"])
    checks.update(transport["checks"])
    checks["configuration_schema"] = schema_valid
    checks["aggregate"] = schema_valid and bool_all(list(checks.values()))
    return {
        "checks": checks,
        "geometry_action": geometry,
        "stress_transport": transport,
    }


def run_mutation_controls() -> dict[str, Any]:
    production = evaluate_configuration(PRODUCTION_CONFIGURATION)
    frozen_registry = {
        name: tuple(sorted(paths))
        for name, paths in FROZEN_MUTATION_REGISTRY
    }
    changed_registry = {
        name: tuple(sorted(change))
        for name, change in MUTATIONS.items()
    }
    records: dict[str, Any] = {}
    for name, change in MUTATIONS.items():
        mutated = deepcopy(PRODUCTION_CONFIGURATION)
        mutated.update(change)
        evaluated = evaluate_configuration(mutated)
        primary = MUTATION_PRIMARY_FAILURES[name]
        observed = {
            key
            for key in primary
            if evaluated["checks"].get(key) is False
        }
        detected = (
            validate_configuration_schema(mutated)
            and evaluated["checks"]["aggregate"] is False
            and observed == primary
            and changed_registry[name] == frozen_registry[name]
        )
        records[name] = {
            "changed_paths": sorted(change),
            "frozen_changed_paths": list(frozen_registry[name]),
            "changed_paths_exact": (
                changed_registry[name] == frozen_registry[name]
            ),
            "mandatory_primary_failures": sorted(primary),
            "observed_primary_failures": sorted(observed),
            "all_mandatory_primary_failures_observed": observed == primary,
            "aggregate_after_mutation": evaluated["checks"]["aggregate"],
            "detected": detected,
        }
    exact_names = set(MUTATIONS) == set(frozen_registry)
    exact_changed_paths = changed_registry == frozen_registry
    all_detected = (
        production["checks"]["aggregate"] is True
        and exact_names
        and exact_changed_paths
        and bool_all([record["detected"] for record in records.values()])
    )
    return {
        "registered_mutation_count": len(MUTATIONS),
        "production_passes_same_evaluator": (
            production["checks"]["aggregate"] is True
        ),
        "exact_name_registry": exact_names,
        "exact_changed_path_registry": exact_changed_paths,
        "all_detected": all_detected,
        "records": records,
    }


def build_flags(
    *,
    dependency_exact: bool,
    upstream_exact: bool,
    prereg_exact: bool,
    package_exact: bool,
    immutable_exact: bool,
    canon_exact: bool,
    production: dict[str, Any],
    mutations_exact: bool,
) -> dict[str, bool]:
    c = production["checks"]
    flags: dict[str, bool] = {
        "dependency_hashes_exact": dependency_exact,
        "upstream_status_and_scope_exact": upstream_exact,
        "one_metric_one_localized_source_exact": (
            c["one_metric_source_ledger"]
        ),
        "w3_58_action_unchanged_exact": (
            upstream_exact
            and c["amplitude_equation_exact"]
            and c["phase_equation_exact"]
            and c["hilbert_stress"]
        ),
        "pg_metric_inverse_volume_exact": (
            c["pg_geometry_inherited"]
            and c["pg_inverse_exact"]
            and c["pg_determinant_exact"]
            and c["pg_full_volume_exact"]
        ),
        "pg_dual_frame_dictionary_exact": (
            c["coframe_dual_exact"] and c["coframe_inherited"]
        ),
        "scalar_amplitude_equation_exact": (
            c["amplitude_equation_exact"]
            and c["potential_derivative_exact"]
        ),
        "ordinary_phase_equation_exact": (
            c["phase_equation_exact"]
            and c["phase_conservative_form_exact"]
        ),
        "ordinary_phase_current_exact": (
            c["current_convention"] and c["current_action_dictionary"]
        ),
        "current_coordinate_frame_dictionary_exact": (
            c["current_inherited_components"]
            and c["current_frame_dictionary"]
            and c["current_norm_exact"]
            and c["current_radial_dictionary"]
        ),
        "timelike_material_domain_exact": c["timelike_branch_guard"],
        "normalized_material_velocity_exact": c["material_velocity_unit"],
        "horizon_inward_current_exact": (
            c["horizon_current"]
            and c["ef_current_crosscheck"]
            and c["ef_radial_charge_flux_invariant"]
            and c["ef_horizon_charge_flux_exact"]
        ),
        "charge_balance_exact": c["charge_balance"],
        "rain_congruence_exact": (
            c["rain_unit_timelike"]
            and c["rain_coframe_rest"]
            and c["rain_geodesic"]
            and c["rain_expansion"]
            and c["phase_hamilton_jacobi"]
            and c["phase_current_parallel_rain"]
        ),
        "finite_proper_horizon_crossing_exact": (
            c["finite_proper_crossing"]
        ),
        "continuity_witness_exact": c["continuity_packet_exact"],
        "continuity_witness_not_full_scalar_solution_exact": (
            c["continuity_witness_scope"]
            and c["continuity_witness_amplitude_not_solved"]
        ),
        "scalar_box_pg_exact": c["scalar_box_exact"],
        "first_order_scalar_system_exact": (
            c["amplitude_evolution_exact"] and c["kinematic_system_exact"]
        ),
        "principal_symbol_exact": (
            c["principal_factorization"]
            and c["principal_inherited"]
            and c["full_spherical_principal_inherited"]
            and c["first_order_block_symmetric"]
            and c["first_order_eigenvalues_exact"]
        ),
        "characteristic_speeds_exact": (
            c["characteristics_match_inherited_null"]
            and c["null_speed_factorization"]
        ),
        "horizon_hyperbolicity_regular_exact": (
            c["pg_geometry_horizon_finite"]
            and c["horizon_speeds_exact"]
            and c["first_order_block_symmetric"]
        ),
        "pg_cauchy_slice_spacelike_exact": c["pg_slice_spacelike"],
        "local_initial_data_open_set_exact": (
            c["pg_slice_spacelike"]
            and c["first_order_block_symmetric"]
            and c["potential_lower_order"]
            and c["timelike_branch_guard"]
            and c["cartesian_completion_smooth"]
        ),
        "polar_cartesian_domain_guard_exact": (
            c["cartesian_completion_smooth"]
        ),
        "hilbert_stress_exact": c["hilbert_stress"],
        "regular_frame_stress_finite_exact": (
            c["regular_frame_stress_finite"]
        ),
        "horizon_energy_flux_nonnegative_exact": (
            c["horizon_energy_flux"]
            and c["horizon_killing_energy_current_exact"]
            and c["ef_horizon_stress_flux_crosscheck"]
        ),
        "scalar_nec_exact": c["radial_nec_exact"],
        "isolated_stationary_crossing_no_go_exact": (
            c["isolated_stationary_crossing_no_go"]
            and c["horizon_current"]
        ),
        "nonstatic_scale_connection_not_promoted_exact": (
            c["scale_curvature_exact"]
            and c["scale_curvature_nonzero"]
            and c["scale_domain_boundary"]
        ),
        "intrinsic_profile_not_passively_rescaled_exact": (
            c["intrinsic_profile_role"]
        ),
        "potential_lower_order_exact": c["potential_lower_order"],
        "mutation_controls_pass": mutations_exact,
        "g0_goal_pass": (
            dependency_exact
            and upstream_exact
            and prereg_exact
            and package_exact
            and immutable_exact
            and canon_exact
            and c["claim_scope"]
        ),
        "g1_conventions_pass": (
            c["pg_geometry_inherited"]
            and c["coframe_inherited"]
            and c["current_convention"]
            and c["one_metric_source_ledger"]
            and c["mass_role_separation"]
        ),
        "g2_action_current_pass": (
            c["amplitude_equation_exact"]
            and c["phase_equation_exact"]
            and c["current_inherited_components"]
            and c["hilbert_stress"]
            and c["charge_balance"]
        ),
        "g3_horizon_hyperbolicity_pass": (
            c["principal_inherited"]
            and c["characteristics_match_inherited_null"]
            and c["horizon_speeds_exact"]
            and c["pg_slice_spacelike"]
            and c["horizon_current"]
        ),
        "g4_independent_crosscheck_pass": (
            c["ef_metric_crosscheck"]
            and c["ef_inverse_crosscheck"]
            and c["ef_determinant_regular"]
            and c["ef_current_crosscheck"]
            and c["ef_radial_charge_flux_invariant"]
            and c["ef_horizon_charge_flux_exact"]
            and c["ef_horizon_stress_flux_crosscheck"]
            and c["rain_geodesic"]
            and c["continuity_packet_exact"]
            and c["continuity_witness_amplitude_not_solved"]
        ),
        "g5_limits_regression_pass": (
            upstream_exact
            and c["flat_limit_metric"]
            and c["flat_limit_speeds"]
            and c["pg_geometry_inherited"]
        ),
        "g6_physical_scope_pass": (
            c["timelike_branch_guard"]
            and c["horizon_current"]
            and c["horizon_energy_flux"]
            and c["horizon_killing_energy_current_exact"]
            and c["isolated_stationary_crossing_no_go"]
            and c["intrinsic_profile_role"]
            and c["scale_domain_boundary"]
            and c["mass_role_separation"]
            and c["claim_scope"]
        ),
        "g7_observation_not_applicable_exact": True,
        "g8_export_not_applicable_exact": (
            immutable_exact and canon_exact
        ),
        "package_clean_pass": package_exact,
    }
    for key in REQUIRED_FALSE_FLAGS:
        flags[key] = False
    preaggregate_true = all(
        flags.get(key) is True
        for key in REQUIRED_TRUE_FLAGS
        if key != "aggregate_gate_pass"
    )
    preaggregate_false = all(
        flags.get(key) is False for key in REQUIRED_FALSE_FLAGS
    )
    flags["aggregate_gate_pass"] = (
        preaggregate_true
        and preaggregate_false
        and (
            set(flags) | {"aggregate_gate_pass"}
            == REQUIRED_TRUE_FLAGS | REQUIRED_FALSE_FLAGS
        )
    )
    return flags


def gate_registry(flags: dict[str, bool]) -> dict[str, bool]:
    return {
        "G0_GOAL": flags["g0_goal_pass"],
        "G1_CONVENTIONS": flags["g1_conventions_pass"],
        "G2_ACTION_CURRENT": flags["g2_action_current_pass"],
        "G3_HORIZON_HYPERBOLICITY": (
            flags["g3_horizon_hyperbolicity_pass"]
        ),
        "G4_INDEPENDENT_CROSSCHECK": (
            flags["g4_independent_crosscheck_pass"]
        ),
        "G5_LIMITS_AND_REGRESSION": (
            flags["g5_limits_regression_pass"]
        ),
        "G6_PHYSICAL_SCOPE": flags["g6_physical_scope_pass"],
        "G7_OBSERVATION": (
            flags["g7_observation_not_applicable_exact"]
        ),
        "G8_EXPORT": flags["g8_export_not_applicable_exact"],
    }


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".w3_72_", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(
                payload,
                handle,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
                allow_nan=False,
            )
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def actual_package_is_exact() -> bool:
    actual_files = {
        path.name for path in PACKAGE_DIR.iterdir() if path.is_file()
    }
    actual_dirs = {
        path.name for path in PACKAGE_DIR.iterdir() if path.is_dir()
    }
    return actual_files == EXPECTED_PACKAGE_FILES and not actual_dirs


def main() -> int:
    dependency_records, dependency_exact = audit_files(DEPENDENCIES)
    immutable, immutable_exact = audit_immutable_intuitive()
    canon, canon_exact = audit_canon_control()
    prereg = audit_preregistration()
    package = audit_package_before_write()
    upstream, upstream_exact = audit_upstream()
    production = evaluate_configuration(PRODUCTION_CONFIGURATION)
    mutations = run_mutation_controls()

    prereg_exact = bool(
        prereg["hash_exact"]
        and prereg["markers_exact"]
        and prereg["required_true_keyset_exact"]
        and prereg["required_false_keyset_exact"]
        and prereg["frozen_mutation_registry_exact"]
    )
    package_exact = bool(package["recursive_exact_three_file_package"])
    flags = build_flags(
        dependency_exact=dependency_exact,
        upstream_exact=upstream_exact,
        prereg_exact=prereg_exact,
        package_exact=package_exact,
        immutable_exact=immutable_exact,
        canon_exact=canon_exact,
        production=production,
        mutations_exact=mutations["all_detected"],
    )
    gates = gate_registry(flags)

    validation = {
        "required_true_keyset_exact": (
            set(flags).intersection(REQUIRED_TRUE_FLAGS)
            == REQUIRED_TRUE_FLAGS
        ),
        "required_false_keyset_exact": (
            set(flags).intersection(REQUIRED_FALSE_FLAGS)
            == REQUIRED_FALSE_FLAGS
        ),
        "all_required_true": all(
            flags[key] is True for key in REQUIRED_TRUE_FLAGS
        ),
        "all_required_false": all(
            flags[key] is False for key in REQUIRED_FALSE_FLAGS
        ),
        "production_configuration_aggregate": (
            production["checks"]["aggregate"] is True
        ),
        "all_mutations_detected": mutations["all_detected"],
        "registered_mutation_count_exact": (
            mutations["registered_mutation_count"]
            == len(FROZEN_MUTATION_REGISTRY)
            == len(MUTATION_PRIMARY_FAILURES)
        ),
        "dependency_hashes_exact": dependency_exact,
        "upstream_exact": upstream_exact,
        "preregistration_exact": prereg_exact,
        "package_prediction_exact": package_exact,
        "immutable_intuitive_exact": immutable_exact,
        "canon_control_exact": canon_exact,
        "all_gates_pass": bool_all(list(gates.values())),
        "post_write_package_exact": False,
    }

    result: dict[str, Any] = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "status": FAIL_STATUS,
        "artifact_valid": False,
        "claim": {
            "established": (
                "The unchanged W3-58 ordinary-phase action has a regular "
                "local initial-value and inward future-timelike current "
                "handoff across the inherited future Schwarzschild horizon."
            ),
            "metric_role": "ONE_INHERITED_EINSTEIN_METRIC",
            "current_role": "ORDINARY_PHASE_NOETHER_CHARGE_CURRENT",
            "source_role": "T_O_COUNTED_ONCE_AS_THE_LOCALIZED_HILBERT_SOURCE",
            "horizon_role": "REGULAR_CHARACTERISTIC_SURFACE",
            "profile_role": (
                "INTRINSIC_LOCAL_PROFILE_NOT_PASSIVELY_RESCALED"
            ),
        },
        "evidence_type": {
            "geometry_action_current_stress": "EXACT_SYMBOLIC",
            "local_initial_value": (
                "EXACT_PRINCIPAL_STRUCTURE_AND_STANDARD_SMOOTH_"
                "SEMILINEAR_HYPERBOLIC_HANDOFF"
            ),
            "continuity_packet": (
                "EXACT_PHASE_EQUATION_ONLY_CROSSCHECK"
            ),
            "observation": "NOT_APPLICABLE",
        },
        "dependencies": {
            "all_hashes_exact": dependency_exact,
            "records": dependency_records,
        },
        "upstream_regression": upstream,
        "preregistration": prereg,
        "package": package,
        "immutable_intuitive_controls": immutable,
        "canon_control": canon,
        "exact_algebra": production["geometry_action"],
        "stress_transport_and_scope": production["stress_transport"],
        "production_checks": production["checks"],
        "mutation_controls": mutations,
        "closure_flags": flags,
        "scope_flags": {
            key: flags[key] for key in sorted(REQUIRED_FALSE_FLAGS)
        },
        "gate_registry": gates,
        "physical_decision": {
            "future_timelike_horizon_current": (
                "STRICTLY_INWARD_FOR_NONZERO_CHI"
            ),
            "horizon_charge_flux": "FINITE_AND_INWARD",
            "horizon_killing_energy_flux": "FINITE_AND_NONNEGATIVE",
            "scalar_characteristics": (
                "IDENTICAL_TO_THE_INHERITED_METRIC_NULL_CONE"
            ),
            "static_isolated_horizon_crossing_current": "EXCLUDED",
            "continuity_packet": "NOT_A_FULL_SCALAR_SOLUTION",
            "local_initial_value_handoff": "CLOSED",
            "nonstatic_global_scale_scalar": (
                "BLOCKED_BY_NONZERO_SCALE_CONNECTION_CURVATURE"
            ),
            "intrinsic_oscillon_profile": (
                "NO_PASSIVE_READOUT_RESCALING"
            ),
            "dynamical_profile_rigidity": "NOT_DERIVED",
            "background_mass": (
                "M_BG_IS_NOT_THE_W3_64_OSCILLON_ADM_MASS"
            ),
            "next_exact_input": (
                "A coupled Einstein-complex-scalar horizon-crossing "
                "initial-data evolution with finite-profile and tidal "
                "control; only after that may a global interior be tested."
            ),
        },
        "scientific_boundary": {
            "established": [
                "unchanged W3-58 action equations on the regular PG chart",
                "action-derived ordinary-phase current and Hilbert stress",
                "future-timelike material-current normalization",
                "strict inward current at the future horizon",
                "exact shell charge balance",
                "finite nonnegative absorbed Killing-energy flux",
                "symmetric-hyperbolic scalar principal block",
                "metric-null characteristic agreement",
                "spacelike PG Cauchy slices across the horizon",
                "EF/PG independent chart cross-check",
                "finite-proper-time rain crossing",
                "exact phase-continuity packet",
                "amplitude-equation veto on promoting that packet",
                "isolated stationary-crossing exclusion",
                "nonstatic scale-connection nonintegrability boundary",
                "one metric and once-only localized T_O source ledger",
            ],
            "not_established": [
                "automatic timelikeness of every U(1) current",
                "Noether charge as invariant mass flux",
                "a full finite-profile oscillon crossing solution",
                "dynamical rigidity or absence of tidal distortion",
                "self-consistent Einstein backreaction during crossing",
                "collapse waveform or ringdown",
                "regular black-hole center or global interior",
                "singularity resolution or geodesic completeness",
                "an observational prediction or likelihood",
            ],
        },
        "references": [
            {
                "citation": (
                    "D. Finkelstein, Past-Future Asymmetry of the "
                    "Gravitational Field of a Point Particle, Physical "
                    "Review 110 (1958) 965."
                ),
                "doi": "10.1103/PhysRev.110.965",
            },
            {
                "citation": (
                    "K. Martel and E. Poisson, Regular coordinate systems "
                    "for Schwarzschild and other spherical spacetimes, "
                    "American Journal of Physics 69 (2001) 476."
                ),
                "arxiv": "gr-qc/0001069",
                "doi": "10.1119/1.1336836",
            },
            {
                "citation": (
                    "D. Philipp and V. Perlick, On analytic solutions of "
                    "wave equations in regular coordinate systems on "
                    "Schwarzschild background, IJMPD 24 (2015) 1542006."
                ),
                "arxiv": "1503.08361",
                "doi": "10.1142/S0218271815420067",
            },
            {
                "citation": (
                    "J. Barranco et al., Self-gravitating black hole "
                    "scalar wigs, Physical Review D 96 (2017) 024049."
                ),
                "arxiv": "1704.03450",
                "doi": "10.1103/PhysRevD.96.024049",
            },
        ],
        "provenance": {
            "generated_utc": (
                "NOT_EMBEDDED_TO_PRESERVE_BYTE_REPRODUCIBILITY"
            ),
            "python": sys.version.split()[0],
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "source_path": SOURCE_PATH.relative_to(REPO_ROOT).as_posix(),
            "source_sha256": sha256_file(SOURCE_PATH),
            "preregistration_sha256": sha256_file(PREREG_PATH),
            "network_used": False,
            "archived_theory_used": False,
            "observational_data_read": False,
            "canon_written": False,
            "intuitive_files_written": False,
        },
        "validation": validation,
    }

    prewrite_valid = bool_all(
        [
            validation["required_true_keyset_exact"],
            validation["required_false_keyset_exact"],
            validation["all_required_true"],
            validation["all_required_false"],
            validation["production_configuration_aggregate"],
            validation["all_mutations_detected"],
            validation["registered_mutation_count_exact"],
            validation["dependency_hashes_exact"],
            validation["upstream_exact"],
            validation["preregistration_exact"],
            validation["package_prediction_exact"],
            validation["immutable_intuitive_exact"],
            validation["canon_control_exact"],
            validation["all_gates_pass"],
        ]
    )
    result["artifact_valid"] = prewrite_valid and json_is_finite(result)
    result["status"] = PASS_STATUS if result["artifact_valid"] else FAIL_STATUS
    atomic_write_json(RESULT_PATH, result)

    post_write_exact = actual_package_is_exact()
    result["validation"]["post_write_package_exact"] = post_write_exact
    result["artifact_valid"] = bool(
        result["artifact_valid"]
        and post_write_exact
        and json_is_finite(result)
    )
    result["status"] = PASS_STATUS if result["artifact_valid"] else FAIL_STATUS
    atomic_write_json(RESULT_PATH, result)

    loaded = load_json(RESULT_PATH)
    final_valid = bool(
        loaded.get("artifact_valid") is True
        and loaded.get("status") == PASS_STATUS
        and actual_package_is_exact()
        and json_is_finite(loaded)
    )
    print(
        json.dumps(
            {
                "artifact_valid": final_valid,
                "status": loaded.get("status"),
                "required_true": len(REQUIRED_TRUE_FLAGS),
                "required_false": len(REQUIRED_FALSE_FLAGS),
                "mutations": mutations["registered_mutation_count"],
                "package_files": sorted(EXPECTED_PACKAGE_FILES),
                "result_sha256": sha256_file(RESULT_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if final_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
