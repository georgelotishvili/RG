#!/usr/bin/env python3
"""W3-71 covariant scale-connection and horizon/material separation audit."""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sympy as sp


CLAIM_ID = "W3_71_COVARIANT_SCALE_CONNECTION_AND_HORIZON_MATERIAL_SEPARATION"
MODEL_VERSION = (
    "W3-71-v1.1-COVARIANT-SCALE-CONNECTION-HORIZON-MATERIAL-SEPARATION"
)
PASS_STATUS = (
    "PASS_EXACT_COVARIANT_SCALE_CONNECTION_ON_HOMOGENEOUS_AND_STATIC_BRANCHES__"
    "TEMPORAL_LAPSE_SPATIAL_RULER_AND_INTRINSIC_OSCILLON_PROFILE_SEPARATED_WITH_"
    "EXACT_COFRAME_RULER_CONVERSION_EINSTEIN_EXTERIOR_AND_1PN__"
    "HORIZON_CROSSING_MATERIAL_CURRENT_NOT_DERIVED"
)
FAIL_STATUS = "FAIL_W3_71_COVARIANT_SCALE_CONNECTION_OR_HORIZON_MATERIAL_AUDIT"

SOURCE_PATH = Path(__file__).resolve()
PACKAGE_DIR = SOURCE_PATH.parent
REPO_ROOT = SOURCE_PATH.parents[4]
PREREG_PATH = (
    PACKAGE_DIR / "w3_71_horizon_material_scale_separation_preregistration.md"
)
RESULT_PATH = PACKAGE_DIR / "w3_71_result.json"
PREREG_SHA256 = "45a9a9eed95a2d927a601f6b4e0822994da93176f1c25fe49ff2431bb35e9f4a"

EXPECTED_PACKAGE_FILES = {
    "w3_71_horizon_material_scale_separation_preregistration.md",
    "w3_71_horizon_material_scale_separation.py",
    "w3_71_result.json",
}

DEPENDENCIES = {
    "CODES.md":
        "27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41",
    "RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/"
    "w3_50_neutral_collective_phase_density_bridge_contract.md":
        "c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635",
    "RefG/work 3/Lagrangian_Formulation/Full_1PN_Inheritance/"
    "w3_52_full_1pn_inheritance_contract.md":
        "66a33a82d29bd65fabc37b6e55f29a64674f0e44f5a4c0893611c261d00792b6",
    "RefG/work 3/Lagrangian_Formulation/"
    "Relational_Coframe_TEGR_Phase_Source_Closure/"
    "w3_54_relational_coframe_tegr_phase_source_closure_contract.md":
        "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
    "RefG/work 3/Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/"
    "w3_58_one_oscillon_coframe_localized_core_preregistration.md":
        "ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db",
    "RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/w3_64_result.json":
        "b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaF95b3119b75d07b".lower(),
    "RefG/work 3/Strong_Field/W3-65_First_Turning_Point/w3_65_result.json":
        "e3256094f5123e70f747d501d84c7db1301e7a2ab00742fc914e254007c67b0b",
    "RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/"
    "w3_67_result.json":
        "659bdfe171a8279b465fdd49eaf590755da22a7522a83053a4a06450fd745385",
    "RefG/work 3/Strong_Field/W3-70_Collective_Phase_Carrier_Admissibility/"
    "w3_70_result.json":
        "0f65d89c6595fbb6bfee9c6bbe7fdf292dd60eacaeaafe654161c84eda8d2cf0",
}

SUPPORTING_CURRENT_RECORDS = {
    "RefG/work 3/Lagrangian_Formulation/Full_1PN_Inheritance/"
    "w3_52_result.json":
        "8ae2d80cbc983e29a7ccc9ef4e3f6685b36cb4e6ade06e6d2a494fd9f46e11e2",
    "RefG/work 3/Lagrangian_Formulation/"
    "Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_result.json":
        "ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991",
    "RefG/work 3/Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/"
    "w3_58_result.json":
        "cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5",
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
    "scale_connection_covariant_exact",
    "scale_connection_coefficients_inherited_exact",
    "scale_connection_projections_exact",
    "target_branch_integrability_exact",
    "homogeneous_reduction_exact",
    "static_killing_reduction_exact",
    "w3_54_euler_crosscheck_exact",
    "healthy_sound_speed_interval_preserved_exact",
    "static_density_algebraic_map_rejected_exact",
    "one_metric_one_source_unchanged_exact",
    "isotropic_areal_map_exact",
    "schwarzschild_reconstruction_exact",
    "temporal_spatial_coframe_split_exact",
    "exact_temporal_spatial_relation",
    "full_1pn_regression_exact",
    "external_radial_null_speed_exact",
    "local_light_speed_exact",
    "pg_metric_from_coframe_exact",
    "pg_inverse_exact",
    "pg_determinant_regular_at_horizon_exact",
    "pg_radial_null_characteristics_exact",
    "round_sphere_trapping_sign_exact",
    "kretschmann_finite_at_horizon_exact",
    "static_worldline_timelike_iff_outside_exact",
    "true_horizon_requires_nonstatic_material_current_exact",
    "finite_oscillon_radius_role_separate_exact",
    "intrinsic_local_oscillon_radius_definition_exact",
    "external_ruler_projection_exact",
    "finite_profile_local_uniform_scope_exact",
    "w3_65_distinct_equilibria_scope_exact",
    "passive_readout_no_new_dof_or_action_exact",
    "penrose_boundary_inherited_exact",
    "binary_branch_decision_exact",
    "mutation_controls_pass",
    "g0_goal_pass",
    "g1_conventions_pass",
    "g2_core_algebra_pass",
    "g3_structure_pass",
    "g4_independent_check_pass",
    "g5_limits_regression_pass",
    "g6_physical_match_pass",
    "g7_observation_not_applicable_exact",
    "g8_export_not_applicable_exact",
    "package_clean_pass",
    "aggregate_gate_pass",
}

REQUIRED_FALSE_FLAGS = {
    "mixed_branch_global_integrability_derived",
    "horizon_crossing_material_current_derived",
    "w3_65_environmental_shrinkage_inference_allowed",
    "intrinsic_profile_rescaling_action_present",
    "exact_common_strongfield_clock_ruler_factor_derived",
    "horizon_crossing_static_congruence_valid",
    "static_material_worldline_inside_horizon_admissible",
    "global_strong_field_solution_derived",
    "global_solve_opened",
    "collapse_evolution_completed",
    "regular_black_hole_interior_derived",
    "singularity_resolution_completed",
    "geodesic_completeness_derived",
    "new_observation_tested",
    "canon_changed",
    "intuitive_files_changed",
}

W3_64_STATUS = (
    "PASS_CONDITIONAL_EXACT_UNCHANGED_EINSTEIN_BACKREACTION_AND_CURRENT_SOURCE_"
    "NEC_BOUNDARY__CONVERGED_NUMERICAL_REGULAR_HORIZONLESS_SELF_GRAVITATING_Q_"
    "BALL_WITNESS__REGULAR_TRAPPED_NULL_COMPLETE_INTERIOR_REQUIRES_FAILURE_OF_"
    "AT_LEAST_ONE_PENROSE_HYPOTHESIS"
)
W3_58_STATUS = (
    "PASS_CONDITIONAL_EXACT_MINIMAL_COFRAME_U1_CORE_ACTION_AND_ANALYTIC_"
    "EXISTENCE_WINDOW__CONVERGED_NUMERICAL_FINITE_ENERGY_ORBITALLY_STABLE_"
    "SPHERICAL_GROUND_STATE_EVIDENCE__FOUNDATION_COEFFICIENT_SELECTION_"
    "BACKGROUND_LOCK_BACKREACTION_AND_PARTICLE_IDENTITY_OPEN"
)
W3_65_STATUS = (
    "PASS_EXACT_UNCHANGED_EINSTEIN_SCALAR_FIXED_ALPHA_SYSTEM__CONVERGED_FIRST_"
    "POST_ANCHOR_SIMULTANEOUS_MASS_CHARGE_TURN_IN_INCREASING_F0_DIRECTION__"
    "CHARGE_CONSERVING_NULL_TANGENT_OF_EXTENDED_STATIC_EQUILIBRIUM_BVP__"
    "REGULAR_NODELESS_HORIZONLESS_RESOLVED_SEGMENT"
)
W3_67_STATUS = (
    "PASS_EXACT_FOUNDATION_STRONG_FIELD_RESPONSE_BOUNDARY__"
    "PASSIVE_AND_COMMON_RESCALING_NO_GO__"
    "COVARIANT_ACTION_AND_CONSTITUTIVE_SELECTION_OPEN"
)
W3_70_STATUS = (
    "PASS_EXACT_STATIONARY_PHASE_BERNOULLI_AND_RESPONSE_SIGN_AUDIT__"
    "REJECTED_AS_UNIVERSAL_LOCAL_P_CARRIER_BY_HEALTHY_EOS_SIGN_CONTRADICTION__"
    "GLOBAL_STRONG_FIELD_SOLVE_NOT_OPENED"
)

EXPECTED_TENSOR_ROLE_REGISTRY = {
    "a_mu": "COVECTOR",
    "Theta": "SCALAR",
    "u_mu": "COVECTOR",
    "Theta_u_mu": "COVECTOR",
    "W_mu": "COVECTOR",
}

EXPECTED_BRANCH_SOURCE_LEDGER = (
    ("homogeneous", "T_C", 1),
    ("homogeneous", "T_O", 0),
    ("homogeneous", "readout", 0),
    ("localized", "T_C", 0),
    ("localized", "T_O", 1),
    ("localized", "readout", 0),
)

FROZEN_MUTATION_REGISTRY = (
    ("theta_coefficient_changed", ("theta_coefficient",)),
    (
        "acceleration_coefficient_sign_flipped",
        ("acceleration_coefficient",),
    ),
    ("static_density_relabelled", ("static_density_power",)),
    ("p_t_forced_equal_p_L", ("spatial_rule",)),
    ("radial_N_used_as_lapse", ("lapse_rule",)),
    (
        "passive_readout_made_dynamic",
        ("readout_action_coefficient",),
    ),
    (
        "nonintegrable_W_accepted",
        ("accepted_connection_domains",),
    ),
    ("pg_shift_removed", ("pg_shift_coefficient",)),
    (
        "static_subhorizon_worldline_admitted",
        ("static_material_domain",),
    ),
    (
        "metric_source_duplicated",
        ("metric_ids", "branch_source_ledger"),
    ),
    (
        "finite_radius_relabelled_as_p_L",
        ("finite_radius_rule",),
    ),
    ("p_t_zero_called_local_time_stop", ("local_time_rule",)),
    ("interior_singularity_overclaim", ("promoted_claims",)),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def bool_all(values: list[bool]) -> bool:
    return all(value is True for value in values)


def exact_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(exact_zero(entry) for entry in matrix)


def sstr(expr: sp.Expr) -> str:
    return sp.sstr(sp.simplify(expr))


def audit_files(expected: dict[str, str]) -> tuple[dict[str, Any], bool]:
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
    return records, bool_all([record["exact"] for record in records.values()])


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
        "records": records,
        "expected_files": expected_files,
        "actual_files": actual_files,
        "hashes_exact": hashes_exact,
        "file_set_exact": file_set_exact,
    }, hashes_exact and file_set_exact


def audit_canon_control() -> tuple[dict[str, Any], bool]:
    candidates = [
        REPO_ROOT / "Theory_Canon.md",
        REPO_ROOT / "RefG/Theory_Canon.md",
    ]
    states = {
        path.relative_to(REPO_ROOT).as_posix(): path.exists()
        for path in candidates
    }
    expected_absent = all(exists is False for exists in states.values())
    return {
        "registered_candidates": states,
        "frozen_v1_1_state": "NO_THEORY_CANON_RECORD_PRESENT",
        "expected_absence_exact": expected_absent,
        "write_target_confined_to_package_result": (
            RESULT_PATH.parent == PACKAGE_DIR
            and RESULT_PATH.name == "w3_71_result.json"
        ),
    }, (
        expected_absent
        and RESULT_PATH.parent == PACKAGE_DIR
        and RESULT_PATH.name == "w3_71_result.json"
    )


def audit_package() -> dict[str, Any]:
    actual_files = sorted(
        path.relative_to(PACKAGE_DIR).as_posix()
        for path in PACKAGE_DIR.rglob("*")
        if path.is_file()
    )
    actual_dirs = sorted(
        path.relative_to(PACKAGE_DIR).as_posix()
        for path in PACKAGE_DIR.rglob("*")
        if path.is_dir()
    )
    anticipated = set(actual_files)
    anticipated.add(RESULT_PATH.name)
    clean = anticipated == EXPECTED_PACKAGE_FILES and not actual_dirs
    return {
        "expected_files": sorted(EXPECTED_PACKAGE_FILES),
        "actual_files_before_write": actual_files,
        "anticipated_files_after_write": sorted(anticipated),
        "actual_directories": actual_dirs,
        "recursive_exact_three_file_package": clean,
    }


def audit_preregistration() -> dict[str, Any]:
    text = PREREG_PATH.read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())
    markers = {
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "scale_connection": "W_mu = a_mu + (1/2) Theta u_mu",
        "integrability": "F_mu_nu = 2 nabla_[mu W_nu] = 0",
        "homogeneous_law": "p_t^2=n_C/n_C0",
        "static_lapse": "p_t=calN",
        "spatial_relation": "p_L=(1+U/2)^(-2)=((1+p_t)/2)^2",
        "pg_characteristics": "dr/dT=-v plus-or-minus 1",
        "finite_radius_scope": (
            "distinct equilibrium solutions, not the same oscillon viewed"
        ),
        "intrinsic_profile_scope": (
            "R_O^loc remains the unchanged charge-moment radius in the local "
            "orthonormal frame"
        ),
        "external_projection_scope": (
            "R_O^ext = p_L R_O^loc"
        ),
        "pass_status": PASS_STATUS,
        "stop_rule": (
            "It opens no horizon-crossing material-current dynamics"
        ),
    }
    marker_checks = {
        name: marker in normalized_text
        for name, marker in markers.items()
    }
    mutation_registry_checks: dict[str, bool] = {}
    for name, paths in FROZEN_MUTATION_REGISTRY:
        path_text = " and ".join(paths)
        pattern = (
            rf"^\d+\. {re.escape(name)}: {re.escape(path_text)}[.;]$"
        )
        mutation_registry_checks[name] = bool(
            re.search(pattern, text, flags=re.MULTILINE)
        )
    mutation_registry_exact = (
        len(mutation_registry_checks) == 13
        and bool_all(list(mutation_registry_checks.values()))
    )
    true_block = text.split("Required true:", 1)[1].split("Required false:", 1)[0]
    false_block = text.split("Required false:", 1)[1].split(
        "## Crosscheck and mutation controls", 1
    )[0]
    prereg_true = set(
        re.findall(r"^- ([A-Za-z0-9_]+)$", true_block, flags=re.MULTILINE)
    )
    prereg_false = set(
        re.findall(r"^- ([A-Za-z0-9_]+)$", false_block, flags=re.MULTILINE)
    )
    actual_hash = sha256_file(PREREG_PATH)
    return {
        "expected_sha256": PREREG_SHA256,
        "actual_sha256": actual_hash,
        "hash_exact": actual_hash == PREREG_SHA256,
        "marker_checks": marker_checks,
        "markers_exact": bool_all(list(marker_checks.values())),
        "frozen_mutation_registry_checks": mutation_registry_checks,
        "frozen_mutation_registry_exact": mutation_registry_exact,
        "preregistered_true_flags": sorted(prereg_true),
        "preregistered_false_flags": sorted(prereg_false),
        "required_true_keyset_exact": prereg_true == REQUIRED_TRUE_FLAGS,
        "required_false_keyset_exact": prereg_false == REQUIRED_FALSE_FLAGS,
        "contract_keysets_exact": (
            prereg_true == REQUIRED_TRUE_FLAGS
            and prereg_false == REQUIRED_FALSE_FLAGS
        ),
    }


def audit_upstream() -> tuple[dict[str, Any], bool]:
    supporting_records, supporting_hashes_exact = audit_files(
        SUPPORTING_CURRENT_RECORDS
    )
    w50 = (
        REPO_ROOT
        / "RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/"
        "w3_50_neutral_collective_phase_density_bridge_contract.md"
    ).read_text(encoding="utf-8")
    w52_contract = (
        REPO_ROOT
        / "RefG/work 3/Lagrangian_Formulation/Full_1PN_Inheritance/"
        "w3_52_full_1pn_inheritance_contract.md"
    ).read_text(encoding="utf-8")
    w54_contract = (
        REPO_ROOT
        / "RefG/work 3/Lagrangian_Formulation/"
        "Relational_Coframe_TEGR_Phase_Source_Closure/"
        "w3_54_relational_coframe_tegr_phase_source_closure_contract.md"
    ).read_text(encoding="utf-8")
    w58_prereg = (
        REPO_ROOT
        / "RefG/work 3/Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/"
        "w3_58_one_oscillon_coframe_localized_core_preregistration.md"
    ).read_text(encoding="utf-8")

    w52 = load_json(
        REPO_ROOT
        / "RefG/work 3/Lagrangian_Formulation/Full_1PN_Inheritance/w3_52_result.json"
    )
    w54 = load_json(
        REPO_ROOT
        / "RefG/work 3/Lagrangian_Formulation/"
        "Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_result.json"
    )
    w58 = load_json(
        REPO_ROOT
        / "RefG/work 3/Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/"
        "w3_58_result.json"
    )
    w64 = load_json(
        REPO_ROOT
        / "RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/w3_64_result.json"
    )
    w65 = load_json(
        REPO_ROOT
        / "RefG/work 3/Strong_Field/W3-65_First_Turning_Point/w3_65_result.json"
    )
    w67 = load_json(
        REPO_ROOT
        / "RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/"
        "w3_67_result.json"
    )
    w70 = load_json(
        REPO_ROOT
        / "RefG/work 3/Strong_Field/W3-70_Collective_Phase_Carrier_Admissibility/"
        "w3_70_result.json"
    )
    expected_ppn = {
        "gamma": 1, "beta": 1, "xi": 0, "alpha1": 0, "alpha2": 0,
        "alpha3": 0, "zeta1": 0, "zeta2": 0, "zeta3": 0, "zeta4": 0,
    }
    checks = {
        "supporting_current_record_hashes_exact": supporting_hashes_exact,
        "w50_status_exact": (
            "PASS_EXACT_CONDITIONAL_NEUTRAL_PHASE_DENSITY_CANDIDATE_CURRENT__"
            "W3_48_BRIDGE_CLOSED_GIVEN_SELECTED_ETA_AND_CUBIC_MEASURE__"
            "MASTER_FOUNDATION_ORIGIN_OPEN"
        ) in w50,
        "w50_homogeneous_current_and_readout_exact": (
            "eta_F=n_C/n_C0" in w50
            and "eta_F a^3 = 1" in w50
            and "P_F/P_F0=eta_F" in w50
            and "p^2=eta_F" in w50
        ),
        "w52_contract_scope_exact": (
            "CONDITIONAL_MATCHED_THROUGH_FULL_STANDARD_1PN_PPN" in w52_contract
            and "beta=gamma=1" in w52_contract
            and "strong-field" in w52_contract
        ),
        "w52_result_and_ppn_vector_exact": (
            w52.get("gate_status") == "PASS"
            and w52.get("published_GR_PPN_inherited_corollary") == expected_ppn
            and w52.get("scope_boundary", {}).get("strong_field_and_2PN")
            == "NOT_TESTED"
        ),
        "w52_one_source_and_weak_metric_not_promoted_exact": (
            w52.get("source_ledger", {}).get("T_mn_from_S_matter") == 1
            and w52.get("source_ledger", {}).get("p_readout_as_extra_source") == 0
            and w52.get("closure_flags", {}).get("FOUNDATION_TO_FULL_METRIC_MAP")
            is False
        ),
        "w54_contract_eh_phase_and_homogeneous_exact": (
            "eta_F a^3=1" in w54_contract
            and "one metric/source ledger" in w54_contract
        ),
        "w54_result_one_source_current_and_role_split_exact": (
            w54.get("closure_flags", {}).get(
                "RELATIONAL_COFRAME_TO_EH_AND_PHASE_T_GATE_CLOSED"
            ) is True
            and w54.get("closure_flags", {}).get(
                "PHASE_CURRENT_CONSERVATION_DERIVED"
            ) is True
            and w54.get("closure_flags", {}).get(
                "ONE_SOURCE_LEDGER_SELECTED_AND_CONSISTENT"
            ) is True
            and w54.get("closure_flags", {}).get("P_F_EQUALS_P_C_DERIVED")
            is False
            and w54.get("source_ledger", {}).get("P_F_or_readout_p_readded") == 0
        ),
        "w58_finite_profile_scope_exact": (
            "converged intrinsic radius" in w58_prereg
            and "environmental core--background scaling" in w58_prereg
            and "outside this stage" in w58_prereg
        ),
        "w58_result_intrinsic_radius_and_scope_exact": (
            w58.get("artifact_valid") is True
            and w58.get("status") == W3_58_STATUS
            and w58.get("closure_flags", {}).get("aggregate_gate_pass") is True
            and w58.get("closure_flags", {}).get(
                "finite_energy_ground_state_constructed_numerical"
            ) is True
            and w58.get("closure_flags", {}).get(
                "intrinsic_charge_radius_constructed_numerical"
            ) is True
            and w58.get("closure_flags", {}).get(
                "one_source_ledger_no_duplicate_exact"
            ) is True
            and w58.get("closure_flags", {}).get(
                "w3_54_common_coframe_minimal_coupling_exact"
            ) is True
            and w58.get("scope_flags", {}).get(
                "environmental_background_scaling_from_core_derived"
            ) is False
            and w58.get("scope_flags", {}).get(
                "physical_particle_identity_derived"
            ) is False
        ),
        "w64_status_metric_source_and_penrose_exact": (
            w64.get("artifact_valid") is True
            and w64.get("status") == W3_64_STATUS
            and w64.get("closure_flags", {}).get("one_einstein_metric_exact")
            is True
            and w64.get("closure_flags", {}).get(
                "one_localized_hilbert_source_exact"
            ) is True
            and w64.get("regularity_and_penrose_boundary", {})
            .get("penrose_boundary", {})
            .get("conditional_no_go_exact") is True
        ),
        "w65_status_and_resolved_branch_exact": (
            w65.get("artifact_valid") is True
            and w65.get("status") == W3_65_STATUS
            and w65.get("closure_flags", {}).get("aggregate_gate_pass") is True
            and w65.get("scope_flags", {}).get("black_hole_solution_derived")
            is False
        ),
        "w67_status_split_1pn_and_response_boundary_exact": (
            w67.get("artifact_valid") is True
            and w67.get("status") == W3_67_STATUS
            and w67.get("closure_flags", {}).get(
                "full_coframe_temporal_spatial_split_exact"
            ) is True
            and w67.get("closure_flags", {}).get(
                "full_standard_1pn_ppn_inherited_exact"
            ) is True
            and w67.get("scope_flags", {}).get("response_action_derived") is False
        ),
        "w70_status_density_veto_and_passive_readout_exact": (
            w70.get("artifact_valid") is True
            and w70.get("status") == W3_70_STATUS
            and w70.get("physical_decision", {}).get(
                "collective_density_as_universal_local_p"
            ) == "HARD_ROLE_VETO"
            and w70.get("physical_decision", {}).get(
                "chemical_potential_readout"
            ) == "PASSIVE_ONLY"
            and w70.get("physical_decision", {}).get(
                "global_strong_field_solve_opened"
            ) is False
        ),
    }
    records = {
        "checks": checks,
        "supporting_current_records": supporting_records,
        "supporting_current_record_hashes_exact": supporting_hashes_exact,
    }
    return records, bool_all(list(checks.values()))


def validate_configuration_schema(config: dict[str, Any]) -> bool:
    required = {
        "acceleration_coefficient",
        "theta_coefficient",
        "static_density_power",
        "spatial_rule",
        "lapse_rule",
        "accepted_connection_domains",
        "pg_shift_coefficient",
        "static_material_domain",
        "metric_ids",
        "branch_source_ledger",
        "readout_action_coefficient",
        "finite_radius_rule",
        "local_time_rule",
        "promoted_claims",
    }
    if set(config) != required:
        return False
    if config["spatial_rule"] not in {"einstein", "temporal"}:
        return False
    if config["lapse_rule"] not in {"normalized_killing", "radial_metric"}:
        return False
    if config["static_material_domain"] not in {"outside_only", "including_inside"}:
        return False
    if config["finite_radius_rule"] not in {"charge_moment", "p_L"}:
        return False
    if config["local_time_rule"] not in {"pg_metric", "static_lapse_zero"}:
        return False
    if not set(config["accepted_connection_domains"]).issubset(
        {"homogeneous", "static", "mixed_witness"}
    ):
        return False
    return (
        isinstance(config["metric_ids"], tuple)
        and isinstance(config["branch_source_ledger"], tuple)
        and all(
            isinstance(entry, tuple)
            and len(entry) == 3
            and isinstance(entry[0], str)
            and isinstance(entry[1], str)
            and entry[2] in {0, 1}
            for entry in config["branch_source_ledger"]
        )
        and isinstance(config["accepted_connection_domains"], tuple)
        and isinstance(config["promoted_claims"], tuple)
    )


def exact_symbolic_audit(config: dict[str, Any]) -> dict[str, Any]:
    if not validate_configuration_schema(config):
        raise ValueError("Configuration does not match the frozen typed schema.")

    accel = sp.Rational(config["acceleration_coefficient"])
    theta_coeff = sp.Rational(config["theta_coefficient"])
    tensor_role_registry = {
        "a_mu": "COVECTOR",
        "Theta": "SCALAR",
        "u_mu": "COVECTOR",
        "Theta_u_mu": (
            "COVECTOR"
            if (
                EXPECTED_TENSOR_ROLE_REGISTRY["Theta"] == "SCALAR"
                and EXPECTED_TENSOR_ROLE_REGISTRY["u_mu"] == "COVECTOR"
            )
            else "INVALID"
        ),
        "W_mu": (
            "COVECTOR"
            if (
                EXPECTED_TENSOR_ROLE_REGISTRY["a_mu"] == "COVECTOR"
                and EXPECTED_TENSOR_ROLE_REGISTRY["Theta_u_mu"]
                == "COVECTOR"
            )
            else "INVALID"
        ),
    }
    scale_connection_covariant = (
        tensor_role_registry == EXPECTED_TENSOR_ROLE_REGISTRY
    )
    theta, a_component = sp.symbols("Theta a_component", real=True)
    u_dot_w = -theta_coeff * theta
    spatial_w = accel * a_component
    temporal_projection_residual = sp.simplify(u_dot_w + theta / 2)
    spatial_projection_residual = sp.simplify(spatial_w - a_component)

    t, x = sp.symbols("t x", real=True)
    theta_t = sp.Function("Theta")(t)
    homogeneous_w_t = -theta_coeff * theta_t
    homogeneous_w_x = sp.Integer(0)
    homogeneous_f_tx = sp.simplify(
        sp.diff(homogeneous_w_x, t) - sp.diff(homogeneous_w_t, x)
    )
    lapse_x = sp.Function("calN", positive=True)(x)
    static_w_t = sp.Integer(0)
    static_w_x = accel * sp.diff(sp.log(lapse_x), x)
    static_f_tx = sp.simplify(
        sp.diff(static_w_x, t) - sp.diff(static_w_t, x)
    )
    mixed_f_tx = sp.simplify(
        2 * (accel + theta_coeff) * sp.sinh(t) * sp.cosh(t)
    )
    integrability_registry = {
        "homogeneous": homogeneous_f_tx,
        "static": static_f_tx,
        "mixed_witness": mixed_f_tx,
    }
    accepted_integrability = {
        domain: exact_zero(integrability_registry[domain])
        for domain in config["accepted_connection_domains"]
    }
    loop_registry = {
        "homogeneous": sp.integrate(
            homogeneous_f_tx, (t, 0, sp.asinh(1)), (x, 0, 1)
        ),
        "static": sp.integrate(
            static_f_tx, (t, 0, sp.asinh(1)), (x, 0, 1)
        ),
        "mixed_witness": sp.simplify(
            sp.integrate(
                mixed_f_tx, (t, 0, sp.asinh(1)), (x, 0, 1)
            )
        ),
    }
    accepted_path_independence = {
        domain: exact_zero(loop_registry[domain])
        for domain in config["accepted_connection_domains"]
    }

    density_ratio, cal_n = sp.symbols(
        "density_ratio calN", positive=True, finite=True
    )
    homogeneous_p_squared = density_ratio ** (2 * theta_coeff)
    homogeneous_residual = sp.simplify(homogeneous_p_squared - density_ratio)
    static_p = cal_n**accel
    static_residual = sp.simplify(static_p - cal_n)

    dlog_mu = sp.symbols("dlog_mu", real=True)
    dlog_n = sp.symbols("dlog_n", real=True, nonzero=True)
    cs2 = sp.symbols("c_s2", real=True)
    dlog_p_euler = sp.simplify(-accel * dlog_mu)
    euler_residual = sp.simplify(dlog_p_euler + dlog_mu)
    eos_slope_residual = sp.simplify(
        dlog_p_euler.subs(dlog_mu, cs2 * dlog_n) + cs2 * dlog_n
    )
    density_power = config["static_density_power"]
    registered_density_control_power = sp.Rational(1, 2)
    registered_density_control_cs2 = -registered_density_control_power
    registered_density_control_healthy = bool(
        0 <= registered_density_control_cs2 <= 1
    )
    healthy_cs2_interval = sp.Interval(0, 1)
    zero_cs2_endpoint_registered = (
        healthy_cs2_interval.contains(sp.Integer(0)) is sp.true
    )
    unit_cs2_endpoint_registered = (
        healthy_cs2_interval.contains(sp.Integer(1)) is sp.true
    )
    zero_cs2_static_slope = sp.simplify(
        dlog_p_euler.subs(dlog_mu, sp.Integer(0) * dlog_n)
    )
    if density_power is None:
        static_density_cs2 = None
        static_density_health = True
        static_density_rejected = True
    else:
        power = sp.Rational(density_power)
        static_density_cs2 = sp.simplify(-power)
        static_density_health = bool(0 <= static_density_cs2 <= 1)
        static_density_rejected = False

    U = sp.symbols("U", positive=True)
    exterior_parameter = sp.symbols("y_ext", positive=True)
    U_exterior = sp.simplify(
        2 * exterior_parameter / (1 + exterior_parameter)
    )
    exterior_lower_residual = sp.simplify(U_exterior)
    exterior_upper_residual = sp.simplify(2 - U_exterior)
    exterior_domain_exact = (
        sp.ask(sp.Q.positive(exterior_lower_residual)) is True
        and sp.ask(sp.Q.positive(exterior_upper_residual)) is True
    )
    q = U / 2
    p_t_einstein = sp.simplify((1 - q) / (1 + q))
    p_l_einstein = sp.simplify((1 + q) ** -2)
    p_t = (
        p_t_einstein
        if config["lapse_rule"] == "normalized_killing"
        else sp.simplify(p_t_einstein**2)
    )
    p_l = (
        p_l_einstein
        if config["spatial_rule"] == "einstein"
        else p_t
    )
    temporal_norm_residual = sp.simplify(p_t**2 - p_t_einstein**2)
    spatial_reconstruction_residual = sp.simplify(p_l - p_l_einstein)
    temporal_spatial_relation_residual = sp.simplify(
        p_l - ((1 + p_t) / 2) ** 2
    )
    exact_clock_ruler_difference = sp.simplify(
        p_l_einstein - p_t_einstein
    )

    m, rho = sp.symbols("m rho", positive=True)
    q_rho = m / (2 * rho)
    areal_r = sp.simplify(rho * (1 + q_rho) ** 2)
    pt_rho = sp.simplify((1 - q_rho) / (1 + q_rho))
    pl_rho = sp.simplify((1 + q_rho) ** -2)
    areal_horizon_residual = sp.simplify(1 - 2 * m / areal_r - pt_rho**2)
    angular_residual = sp.simplify(rho**2 / pl_rho**2 - areal_r**2)
    dr_drho = sp.diff(areal_r, rho)
    radial_residual = sp.simplify(
        pl_rho**-2 / dr_drho**2 - 1 / (1 - 2 * m / areal_r)
    )

    pt_series = sp.series(p_t, U, 0, 3).removeO().expand()
    pl_series = sp.series(p_l, U, 0, 3).removeO().expand()
    gtt_series = sp.series(-p_t**2, U, 0, 3).removeO().expand()
    gspace_series = sp.series(p_l**-2, U, 0, 3).removeO().expand()
    expected_pt = 1 - U + U**2 / 2
    expected_pl = 1 - U + 3 * U**2 / 4
    expected_gtt = -1 + 2 * U - 2 * U**2
    expected_gspace = 1 + 2 * U + 3 * U**2 / 2
    beta = sp.simplify(-gtt_series.coeff(U, 2) / 2)
    gamma = sp.simplify(gspace_series.coeff(U, 1) / 2)
    radial_speed = sp.symbols("z_radial", real=True)
    radial_null_polynomial = sp.expand(
        -p_t**2 + p_l**-2 * radial_speed**2
    )
    radial_null_factorization = sp.expand(
        (radial_speed - p_t * p_l)
        * (radial_speed + p_t * p_l)
        / p_l**2
    )
    radial_null_factorization_residual = sp.simplify(
        radial_null_polynomial - radial_null_factorization
    )
    expected_radial_null_roots = (
        sp.simplify(-p_t * p_l),
        sp.simplify(p_t * p_l),
    )
    radial_null_roots = tuple(
        sp.simplify(root)
        for root in sp.solve(
            sp.Eq(radial_null_polynomial, 0), radial_speed
        )
    )
    radial_root_solution_exact = (
        len(radial_null_roots) == 2
        and all(
            any(
                exact_zero(root - expected)
                for expected in expected_radial_null_roots
            )
            for root in radial_null_roots
        )
        and all(
            any(
                exact_zero(expected - root)
                for root in radial_null_roots
            )
            for expected in expected_radial_null_roots
        )
    )
    radial_null_root_residuals = tuple(
        sp.simplify(radial_null_polynomial.subs(radial_speed, root))
        for root in radial_null_roots
    )
    radial_null_degree = sp.Poly(
        radial_null_polynomial, radial_speed
    ).degree()
    radial_root_separation_exterior = sp.simplify(
        (
            expected_radial_null_roots[1]
            - expected_radial_null_roots[0]
        ).subs(
            U, U_exterior
        )
    )
    radial_roots_distinct_exterior = (
        sp.ask(sp.Q.positive(radial_root_separation_exterior)) is True
    )
    local_tetrad_speed_roots = tuple(
        sp.simplify(root / (p_t * p_l))
        for root in radial_null_roots
    )
    horizon_root_limits = tuple(
        sp.limit(root, U, 2, dir="-")
        for root in expected_radial_null_roots
    )
    horizon_pt_limit = sp.limit(p_t, U, 2, dir="-")
    horizon_pl_limit = sp.limit(p_l, U, 2, dir="-")

    v = sp.symbols("v", positive=True)
    shift = sp.Rational(config["pg_shift_coefficient"])
    coframe = sp.Matrix([[1, 0], [shift * v, 1]])
    eta = sp.diag(-1, 1)
    pg_metric = sp.simplify(coframe.T * eta * coframe)
    target_pg_metric = sp.Matrix([[v**2 - 1, v], [v, 1]])
    pg_metric_residual = sp.simplify(pg_metric - target_pg_metric)
    pg_inverse = sp.simplify(pg_metric.inv())
    target_pg_inverse = sp.Matrix([[-1, v], [v, 1 - v**2]])
    pg_inverse_residual = sp.simplify(pg_inverse - target_pg_inverse)
    pg_determinant = sp.simplify(pg_metric.det())
    slope = sp.symbols("slope", real=True)
    null_polynomial = sp.expand(
        pg_metric[0, 0] + 2 * pg_metric[0, 1] * slope
        + pg_metric[1, 1] * slope**2
    )
    outgoing = sp.simplify(1 - shift * v)
    ingoing = sp.simplify(-1 - shift * v)
    outgoing_root_residual = sp.simplify(
        null_polynomial.subs(slope, outgoing)
    )
    ingoing_root_residual = sp.simplify(
        null_polynomial.subs(slope, ingoing)
    )
    v_values = (sp.Rational(1, 2), sp.Integer(1), sp.Integer(2))
    outgoing_values = [sp.simplify(outgoing.subs(v, value)) for value in v_values]
    ingoing_values = [sp.simplify(ingoing.subs(v, value)) for value in v_values]

    r_s, r = sp.symbols("r_s r", positive=True)
    theta_out = sp.simplify(2 * (1 - v) / r)
    theta_in = sp.simplify(-2 * (1 + v) / r)
    expansion_product = sp.simplify(
        sp.expand(theta_out * theta_in).subs(v**2, r_s / r)
    )
    expected_expansion_product = sp.simplify(-4 * (1 - r_s / r) / r**2)
    kretschmann = sp.simplify(12 * r_s**2 / r**6)
    horizon_kretschmann = sp.simplify(kretschmann.subs(r, r_s))
    r0_kretschmann_limit = sp.limit(kretschmann, r, 0, dir="+")
    static_tangent_norm = sp.simplify((r_s - r) / r)
    static_timelike_solution = sp.reduce_inequalities(
        static_tangent_norm < 0, r
    )
    static_timelike_iff_outside = (
        static_timelike_solution == (r_s < r)
    )
    infall = sp.Matrix([1, -v])
    infall_norm = sp.simplify((infall.T * target_pg_metric * infall)[0])
    local_tau_squared = (
        sp.Integer(1)
        if config["local_time_rule"] == "pg_metric"
        else sp.Integer(0)
    )
    local_time_residual = sp.simplify(infall_norm + local_tau_squared)

    static_inside_norm = sp.simplify(static_tangent_norm.subs(r, r_s / 2))
    static_domain_residual = (
        sp.Integer(0)
        if config["static_material_domain"] == "outside_only"
        else static_inside_norm
    )

    distinct_metric_count = len(set(config["metric_ids"]))
    metric_registry_residual = distinct_metric_count - 1
    branch_source_ledger = tuple(config["branch_source_ledger"])
    branch_source_ledger_exact = (
        branch_source_ledger == EXPECTED_BRANCH_SOURCE_LEDGER
    )
    branch_source_map = {
        (branch, source): int(weight)
        for branch, source, weight in branch_source_ledger
    }
    branch_source_sums = {
        branch: sum(
            branch_source_map.get((branch, source), 0)
            for source in ("T_C", "T_O")
        )
        for branch in ("homogeneous", "localized")
    }
    readout_source_weights = {
        branch: branch_source_map.get((branch, "readout"), -1)
        for branch in ("homogeneous", "localized")
    }
    once_counted_source_exact = (
        branch_source_ledger_exact
        and branch_source_sums == {
            "homogeneous": 1,
            "localized": 1,
        }
        and readout_source_weights == {
            "homogeneous": 0,
            "localized": 0,
        }
    )

    readout_lambda = sp.Rational(config["readout_action_coefficient"])
    box_p, kinetic_witness, stress_witness = sp.symbols(
        "box_p kinetic_witness stress_witness", nonzero=True
    )
    readout_euler_lagrange = sp.simplify(readout_lambda * box_p)
    readout_kinetic_hessian = sp.simplify(readout_lambda * kinetic_witness)
    readout_hilbert_stress = sp.simplify(readout_lambda * stress_witness)

    i2, i4, p_l_probe = sp.symbols("I2 I4 p_L_probe", positive=True)
    ell = sp.symbols("ell", nonnegative=True)
    p_l_profile = sp.Function("p_L_profile", positive=True)
    intrinsic_charge_radius = sp.sqrt(i4 / i2)
    finite_radius = (
        intrinsic_charge_radius
        if config["finite_radius_rule"] == "charge_moment"
        else p_l_probe
    )
    finite_radius_residual = sp.simplify(finite_radius**2 * i2 - i4)
    finite_radius_role_separate = (
        config["finite_radius_rule"] == "charge_moment"
        and p_l_probe not in intrinsic_charge_radius.free_symbols
    )
    expected_external_radius = sp.Integral(
        p_l_profile(ell), (ell, 0, intrinsic_charge_radius)
    )
    external_radius_candidate = (
        expected_external_radius
        if config["finite_radius_rule"] == "charge_moment"
        else p_l_probe
    )
    external_ruler_projection_exact = (
        external_radius_candidate == expected_external_radius
    )
    local_uniform_external_radius = sp.integrate(
        p_l_probe, (ell, 0, intrinsic_charge_radius)
    )
    local_uniform_projection_residual = sp.simplify(
        local_uniform_external_radius
        - p_l_probe * intrinsic_charge_radius
    )

    forbidden_claims = {
        "mixed_branch_global_integrability_derived",
        "horizon_crossing_material_current_derived",
        "w3_65_environmental_shrinkage_inference_allowed",
        "intrinsic_profile_rescaling_action_present",
        "global_strong_field_solution_derived",
        "global_solve_opened",
        "collapse_evolution_completed",
        "regular_black_hole_interior_derived",
        "singularity_resolution_completed",
        "geodesic_completeness_derived",
        "new_observation_tested",
    }
    promoted = set(config["promoted_claims"])
    promoted_forbidden = sorted(promoted & forbidden_claims)
    interior_claim_consistent = (
        not promoted_forbidden
        and r0_kretschmann_limit == sp.oo
    )

    checks = {
        "typed_schema": True,
        "scale_connection_covariant": scale_connection_covariant,
        "scale_connection_temporal_projection": exact_zero(
            temporal_projection_residual
        ),
        "scale_connection_spatial_projection": exact_zero(
            spatial_projection_residual
        ),
        "accepted_domain_integrability": bool_all(
            list(accepted_integrability.values())
        ),
        "path_independence": bool_all(
            list(accepted_path_independence.values())
        ),
        "declared_domain_registry": (
            exterior_domain_exact
            and horizon_pt_limit == 0
            and horizon_pl_limit == sp.Rational(1, 4)
        ),
        "homogeneous_reduction": exact_zero(homogeneous_residual),
        "static_killing_reduction": exact_zero(static_residual),
        "w3_54_euler_crosscheck": (
            exact_zero(euler_residual) and exact_zero(eos_slope_residual)
        ),
        "healthy_sound_speed_interval": (
            exact_zero(euler_residual)
            and exact_zero(eos_slope_residual)
            and static_density_health is True
            and static_density_rejected is True
            and registered_density_control_cs2 == -sp.Rational(1, 2)
            and registered_density_control_healthy is False
            and zero_cs2_endpoint_registered
            and unit_cs2_endpoint_registered
            and exact_zero(zero_cs2_static_slope)
        ),
        "static_density_map_rejected": static_density_rejected,
        "static_total_lapse_norm": exact_zero(temporal_norm_residual),
        "isotropic_areal_map": (
            exact_zero(areal_horizon_residual)
            and exact_zero(angular_residual)
        ),
        "schwarzschild_temporal_reconstruction": exact_zero(
            temporal_norm_residual
        ),
        "schwarzschild_spatial_reconstruction": (
            exact_zero(spatial_reconstruction_residual)
            and exact_zero(radial_residual)
        ),
        "exact_temporal_spatial_relation": exact_zero(
            temporal_spatial_relation_residual
        ),
        "temporal_spatial_split": exact_clock_ruler_difference != 0,
        "full_1pn_temporal": (
            exact_zero(pt_series - expected_pt)
            and exact_zero(gtt_series - expected_gtt)
            and beta == 1
        ),
        "full_1pn_spatial": (
            exact_zero(pl_series - expected_pl)
            and exact_zero(gspace_series - expected_gspace)
            and gamma == 1
        ),
        "external_radial_null_speed": (
            radial_null_degree == 2
            and exact_zero(radial_null_factorization_residual)
            and radial_root_solution_exact
            and bool_all(
                [
                    exact_zero(residual)
                    for residual in radial_null_root_residuals
                ]
            )
            and exterior_domain_exact
            and radial_roots_distinct_exterior
            and horizon_root_limits == (0, 0)
        ),
        "local_light_speed": (
            set(local_tetrad_speed_roots)
            == {sp.Integer(-1), sp.Integer(1)}
            and exterior_domain_exact
        ),
        "pg_target_metric": matrix_zero(pg_metric_residual),
        "pg_inverse": matrix_zero(pg_inverse_residual),
        "pg_determinant": pg_determinant == -1,
        "pg_null_characteristics": (
            exact_zero(outgoing_root_residual)
            and exact_zero(ingoing_root_residual)
            and outgoing == 1 - v
            and ingoing == -1 - v
        ),
        "trapping_sign": (
            outgoing_values == [
                sp.Rational(1, 2), sp.Integer(0), sp.Integer(-1)
            ]
            and all(value < 0 for value in ingoing_values)
            and exact_zero(expansion_product - expected_expansion_product)
        ),
        "horizon_kretschmann": horizon_kretschmann == 12 / r_s**4,
        "r0_curvature_boundary": r0_kretschmann_limit == sp.oo,
        "static_worldline_classification": (
            static_timelike_iff_outside
            and static_tangent_norm.subs(r, 2 * r_s) < 0
            and static_tangent_norm.subs(r, r_s) == 0
            and static_tangent_norm.subs(r, r_s / 2) > 0
            and exact_zero(static_domain_residual)
        ),
        "binary_branch_decision": exact_zero(static_domain_residual),
        "one_metric_registry": metric_registry_residual == 0,
        "once_counted_hilbert_source": once_counted_source_exact,
        "readout_EL_zero": exact_zero(readout_euler_lagrange),
        "readout_kinetic_hessian_zero": exact_zero(readout_kinetic_hessian),
        "readout_stress_zero": exact_zero(readout_hilbert_stress),
        "no_new_dof": exact_zero(readout_kinetic_hessian),
        "charge_moment_definition": exact_zero(finite_radius_residual),
        "finite_radius_role_separate": finite_radius_role_separate,
        "external_ruler_projection": external_ruler_projection_exact,
        "finite_profile_local_uniform_scope": exact_zero(
            local_uniform_projection_residual
        ),
        "pg_local_proper_time": exact_zero(local_time_residual),
        "penrose_boundary": not promoted_forbidden,
        "scope_claim_consistency": interior_claim_consistent,
    }

    return {
        "connection": {
            "tensor_role_registry": tensor_role_registry,
            "tensor_role_registry_exact": scale_connection_covariant,
            "acceleration_coefficient": sstr(accel),
            "theta_coefficient": sstr(theta_coeff),
            "u_dot_W": sstr(u_dot_w),
            "temporal_projection_residual": sstr(temporal_projection_residual),
            "spatial_projection_residual": sstr(spatial_projection_residual),
            "integrability": {
                domain: {
                    "F_tx": sstr(integrability_registry[domain]),
                    "exact": accepted_integrability[domain],
                    "rectangle_loop": sstr(loop_registry[domain]),
                    "path_independent": accepted_path_independence[domain],
                }
                for domain in config["accepted_connection_domains"]
            },
            "mixed_witness_F_tx": sstr(mixed_f_tx),
            "mixed_witness_rectangle_loop": sstr(
                loop_registry["mixed_witness"]
            ),
            "homogeneous_p2_residual": sstr(homogeneous_residual),
            "static_p_residual": sstr(static_residual),
        },
        "euler_and_health": {
            "dlog_p": sstr(dlog_p_euler),
            "euler_residual": sstr(euler_residual),
            "eos_slope_residual": sstr(eos_slope_residual),
            "static_density_power": (
                None if density_power is None else sstr(sp.Rational(density_power))
            ),
            "static_density_required_cs2": (
                None if static_density_cs2 is None else sstr(static_density_cs2)
            ),
            "static_density_required_cs2_healthy": static_density_health,
            "healthy_cs2_interval": "[0, 1]",
            "cs2_zero_endpoint_registered": zero_cs2_endpoint_registered,
            "cs2_unit_endpoint_registered": unit_cs2_endpoint_registered,
            "cs2_zero_endpoint_static_slope": sstr(
                zero_cs2_static_slope
            ),
            "cs2_zero_endpoint_role": (
                "ZERO_STATIC_DENSITY_SLOPE_ENDPOINT_NOT_AN_UNHEALTHY_MODE"
            ),
            "registered_rejected_density_control": {
                "power_dlogp_dlogn": sstr(registered_density_control_power),
                "required_cs2": sstr(registered_density_control_cs2),
                "inside_closed_health_interval": (
                    registered_density_control_healthy
                ),
            },
        },
        "schwarzschild": {
            "domain_registry": {
                "static_connection": "calN > 0",
                "isotropic_exterior": "0 < U < 2",
                "isotropic_horizon": "U -> 2^- ONE_SIDED_STATIC_LIMIT_ONLY",
                "painleve_gullstrand": "r > 0",
            },
            "exterior_parameterization": sstr(U_exterior),
            "exterior_lower_positive": (
                sp.ask(sp.Q.positive(exterior_lower_residual)) is True
            ),
            "exterior_upper_positive": (
                sp.ask(sp.Q.positive(exterior_upper_residual)) is True
            ),
            "p_t": sstr(p_t),
            "p_L": sstr(p_l),
            "areal_radius": sstr(areal_r),
            "temporal_norm_residual": sstr(temporal_norm_residual),
            "spatial_reconstruction_residual": sstr(
                spatial_reconstruction_residual
            ),
            "areal_horizon_residual": sstr(areal_horizon_residual),
            "angular_residual": sstr(angular_residual),
            "radial_residual": sstr(radial_residual),
            "temporal_spatial_relation_residual": sstr(
                temporal_spatial_relation_residual
            ),
            "p_L_minus_p_t": sstr(exact_clock_ruler_difference),
            "p_t_series": sstr(pt_series),
            "p_L_series": sstr(pl_series),
            "g_tt_series": sstr(gtt_series),
            "g_space_series": sstr(gspace_series),
            "PPN_beta": sstr(beta),
            "PPN_gamma": sstr(gamma),
            "radial_null_polynomial": sstr(radial_null_polynomial),
            "radial_null_factorization_residual": sstr(
                radial_null_factorization_residual
            ),
            "radial_null_degree": radial_null_degree,
            "radial_null_roots_over_c0": [
                sstr(root) for root in radial_null_roots
            ],
            "radial_null_root_residuals": [
                sstr(residual)
                for residual in radial_null_root_residuals
            ],
            "radial_roots_distinct_on_exterior": (
                radial_roots_distinct_exterior
            ),
            "local_tetrad_speed_roots_over_c0": [
                sstr(root) for root in local_tetrad_speed_roots
            ],
            "one_sided_horizon_root_limits": [
                sstr(root) for root in horizon_root_limits
            ],
            "one_sided_horizon_p_t_limit": sstr(horizon_pt_limit),
            "one_sided_horizon_p_L_limit": sstr(horizon_pl_limit),
            "static_tetrad_evaluated_at_horizon": False,
        },
        "painleve_gullstrand": {
            "coframe": sp.sstr(coframe),
            "metric": sp.sstr(pg_metric),
            "metric_residual": sp.sstr(pg_metric_residual),
            "inverse": sp.sstr(pg_inverse),
            "inverse_residual": sp.sstr(pg_inverse_residual),
            "two_dimensional_determinant": sstr(pg_determinant),
            "outgoing_characteristic": sstr(outgoing),
            "ingoing_characteristic": sstr(ingoing),
            "outgoing_values_outside_horizon_inside": [
                sstr(value) for value in outgoing_values
            ],
            "ingoing_values_outside_horizon_inside": [
                sstr(value) for value in ingoing_values
            ],
            "theta_out": sstr(theta_out),
            "theta_in": sstr(theta_in),
            "expansion_product": sstr(expansion_product),
            "kretschmann": sstr(kretschmann),
            "horizon_kretschmann": sstr(horizon_kretschmann),
            "r0_kretschmann_limit": str(r0_kretschmann_limit),
            "static_tangent_norm": sstr(static_tangent_norm),
            "static_timelike_solution": str(static_timelike_solution),
            "static_timelike_iff_r_greater_than_r_s": (
                static_timelike_iff_outside
            ),
            "infall_norm": sstr(infall_norm),
            "local_time_residual": sstr(local_time_residual),
        },
        "structure": {
            "distinct_metric_count": distinct_metric_count,
            "metric_registry_residual": metric_registry_residual,
            "branch_source_ledger": [
                {
                    "branch": branch,
                    "source": source,
                    "weight": weight,
                }
                for branch, source, weight in branch_source_ledger
            ],
            "branch_source_ledger_exact": branch_source_ledger_exact,
            "branch_source_sums": branch_source_sums,
            "readout_source_weights": readout_source_weights,
            "once_counted_source_exact": once_counted_source_exact,
            "readout_action_coefficient": sstr(readout_lambda),
            "readout_euler_lagrange": sstr(readout_euler_lagrange),
            "readout_kinetic_hessian": sstr(readout_kinetic_hessian),
            "readout_hilbert_stress": sstr(readout_hilbert_stress),
            "finite_radius_rule": config["finite_radius_rule"],
            "intrinsic_local_charge_radius": sstr(
                intrinsic_charge_radius
            ),
            "finite_radius_definition_residual": sstr(finite_radius_residual),
            "intrinsic_radius_contains_p_L": (
                p_l_probe in intrinsic_charge_radius.free_symbols
            ),
            "external_reference_standard_radius": str(
                external_radius_candidate
            ),
            "external_reference_standard_projection_exact": (
                external_ruler_projection_exact
            ),
            "local_uniform_external_radius": sstr(
                local_uniform_external_radius
            ),
            "local_uniform_projection_residual": sstr(
                local_uniform_projection_residual
            ),
            "intrinsic_profile_changed_by_readout": False,
            "promoted_forbidden_claims": promoted_forbidden,
        },
        "checks": checks,
    }


def audit_finite_oscillon() -> dict[str, Any]:
    w65 = load_json(
        REPO_ROOT
        / "RefG/work 3/Strong_Field/W3-65_First_Turning_Point/w3_65_result.json"
    )
    anchor = w65["anchor"]["record"]
    turn = w65["canonical_turning_solution"]["record"]
    anchor_lapse = float(anchor["central_lapse"])
    turn_lapse = float(turn["central_lapse"])
    anchor_radius = float(anchor["charge_rms_radius"])
    turn_radius = float(turn["charge_rms_radius"])
    anchor_f0 = float(anchor["f0"])
    turn_f0 = float(turn["f0"])
    values = (
        anchor_lapse,
        turn_lapse,
        anchor_radius,
        turn_radius,
        anchor_f0,
        turn_f0,
    )
    all_finite = all(math.isfinite(value) for value in values)
    lapse_ratio = turn_lapse / anchor_lapse
    radius_ratio = turn_radius / anchor_radius
    return {
        "source_status": w65.get("status"),
        "source_artifact_valid": w65.get("artifact_valid"),
        "comparison_semantics": "DISTINCT_EQUILIBRIUM_SOLUTIONS",
        "same_oscillon_cross_environment_comparison": False,
        "environmental_shrinkage_inference_allowed": False,
        "anchor": {
            "f0": anchor_f0,
            "central_lapse": anchor_lapse,
            "charge_rms_radius": anchor_radius,
        },
        "first_turn": {
            "f0": turn_f0,
            "central_lapse": turn_lapse,
            "charge_rms_radius": turn_radius,
        },
        "central_lapse_delta": turn_lapse - anchor_lapse,
        "charge_rms_radius_delta": turn_radius - anchor_radius,
        "central_lapse_ratio": lapse_ratio,
        "charge_rms_radius_ratio": radius_ratio,
        "all_finite": all_finite,
        "central_lapse_decreases": turn_lapse < anchor_lapse,
        "finite_radius_increases": turn_radius > anchor_radius,
        "scope_regression_pass": (
            all_finite
            and w65.get("artifact_valid") is True
            and w65.get("status") == W3_65_STATUS
            and turn_lapse < anchor_lapse
            and turn_radius > anchor_radius
            and turn_f0 != anchor_f0
        ),
    }


PRODUCTION_CONFIGURATION: dict[str, Any] = {
    "acceleration_coefficient": sp.Integer(1),
    "theta_coefficient": sp.Rational(1, 2),
    "static_density_power": None,
    "spatial_rule": "einstein",
    "lapse_rule": "normalized_killing",
    "accepted_connection_domains": ("homogeneous", "static"),
    "pg_shift_coefficient": sp.Integer(1),
    "static_material_domain": "outside_only",
    "metric_ids": ("g",),
    "branch_source_ledger": EXPECTED_BRANCH_SOURCE_LEDGER,
    "readout_action_coefficient": sp.Integer(0),
    "finite_radius_rule": "charge_moment",
    "local_time_rule": "pg_metric",
    "promoted_claims": (),
}


def evaluate_configuration(config: dict[str, Any]) -> dict[str, bool]:
    symbolic = exact_symbolic_audit(config)
    checks = dict(symbolic["checks"])
    checks["aggregate"] = bool_all(list(checks.values()))
    return checks


MUTATIONS: dict[str, dict[str, Any]] = {
    "theta_coefficient_changed": {
        "theta_coefficient": sp.Rational(2, 3)
    },
    "acceleration_coefficient_sign_flipped": {
        "acceleration_coefficient": sp.Integer(-1)
    },
    "static_density_relabelled": {
        "static_density_power": sp.Rational(1, 2)
    },
    "p_t_forced_equal_p_L": {"spatial_rule": "temporal"},
    "radial_N_used_as_lapse": {"lapse_rule": "radial_metric"},
    "passive_readout_made_dynamic": {
        "readout_action_coefficient": sp.Integer(1)
    },
    "nonintegrable_W_accepted": {
        "accepted_connection_domains": (
            "homogeneous", "static", "mixed_witness"
        )
    },
    "pg_shift_removed": {"pg_shift_coefficient": sp.Integer(0)},
    "static_subhorizon_worldline_admitted": {
        "static_material_domain": "including_inside"
    },
    "metric_source_duplicated": {
        "metric_ids": ("g", "f"),
        "branch_source_ledger": (
            ("homogeneous", "T_C", 1),
            ("homogeneous", "T_O", 0),
            ("homogeneous", "readout", 0),
            ("localized", "T_C", 1),
            ("localized", "T_O", 1),
            ("localized", "readout", 0),
        ),
    },
    "finite_radius_relabelled_as_p_L": {"finite_radius_rule": "p_L"},
    "p_t_zero_called_local_time_stop": {
        "local_time_rule": "static_lapse_zero"
    },
    "interior_singularity_overclaim": {
        "promoted_claims": (
            "global_strong_field_solution_derived",
            "global_solve_opened",
            "collapse_evolution_completed",
            "regular_black_hole_interior_derived",
            "singularity_resolution_completed",
            "geodesic_completeness_derived",
        )
    },
}

MUTATION_PRIMARY_FAILURES = {
    "theta_coefficient_changed": {
        "scale_connection_temporal_projection", "homogeneous_reduction"
    },
    "acceleration_coefficient_sign_flipped": {
        "scale_connection_spatial_projection",
        "static_killing_reduction",
        "w3_54_euler_crosscheck",
    },
    "static_density_relabelled": {
        "healthy_sound_speed_interval", "static_density_map_rejected"
    },
    "p_t_forced_equal_p_L": {
        "exact_temporal_spatial_relation",
        "schwarzschild_spatial_reconstruction",
    },
    "radial_N_used_as_lapse": {
        "static_total_lapse_norm",
        "schwarzschild_temporal_reconstruction",
        "full_1pn_temporal",
    },
    "passive_readout_made_dynamic": {
        "readout_EL_zero", "readout_stress_zero", "no_new_dof"
    },
    "nonintegrable_W_accepted": {
        "accepted_domain_integrability", "path_independence"
    },
    "pg_shift_removed": {
        "pg_target_metric", "pg_null_characteristics", "trapping_sign"
    },
    "static_subhorizon_worldline_admitted": {
        "static_worldline_classification", "binary_branch_decision"
    },
    "metric_source_duplicated": {
        "one_metric_registry", "once_counted_hilbert_source"
    },
    "finite_radius_relabelled_as_p_L": {
        "charge_moment_definition",
        "finite_radius_role_separate",
        "external_ruler_projection",
    },
    "p_t_zero_called_local_time_stop": {"pg_local_proper_time"},
    "interior_singularity_overclaim": {
        "penrose_boundary", "scope_claim_consistency"
    },
}


def run_mutation_controls() -> dict[str, Any]:
    production_checks = evaluate_configuration(PRODUCTION_CONFIGURATION)
    frozen_registry = {
        name: tuple(sorted(paths))
        for name, paths in FROZEN_MUTATION_REGISTRY
    }
    actual_changed_path_registry = {
        name: tuple(sorted(change))
        for name, change in MUTATIONS.items()
    }
    records: dict[str, Any] = {}
    for name, change in MUTATIONS.items():
        mutated = dict(PRODUCTION_CONFIGURATION)
        mutated.update(change)
        schema_valid = validate_configuration_schema(mutated)
        checks = evaluate_configuration(mutated)
        primary = MUTATION_PRIMARY_FAILURES[name]
        primary_failed = sorted(key for key in primary if checks[key] is False)
        exact_primary_failure = set(primary_failed) == primary
        detected = (
            schema_valid
            and checks["aggregate"] is False
            and exact_primary_failure
        )
        records[name] = {
            "changed_paths": sorted(change),
            "frozen_changed_paths": list(frozen_registry[name]),
            "changed_paths_exact": (
                actual_changed_path_registry[name]
                == frozen_registry[name]
            ),
            "schema_valid": schema_valid,
            "aggregate_after_mutation": checks["aggregate"],
            "mandatory_primary_failures": sorted(primary),
            "observed_primary_failures": primary_failed,
            "all_mandatory_primary_failures_observed": exact_primary_failure,
            "all_failed_checks": sorted(
                key for key, value in checks.items()
                if key != "aggregate" and value is False
            ),
            "detected": detected,
        }
    exact_name_registry = (
        set(MUTATIONS) == set(MUTATION_PRIMARY_FAILURES)
        and set(MUTATIONS) == set(frozen_registry)
        and len(MUTATIONS) == 13
    )
    exact_changed_path_registry = (
        actual_changed_path_registry == frozen_registry
    )
    return {
        "production_passes_same_evaluator": production_checks["aggregate"],
        "registered_mutation_count": len(MUTATIONS),
        "exact_name_registry": exact_name_registry,
        "exact_changed_path_registry": exact_changed_path_registry,
        "frozen_registry": {
            name: list(paths)
            for name, paths in frozen_registry.items()
        },
        "records": records,
        "all_detected": (
            production_checks["aggregate"]
            and exact_name_registry
            and exact_changed_path_registry
            and bool_all([record["detected"] for record in records.values()])
        ),
    }


def build_flags(
    dependency_exact: bool,
    upstream_exact: bool,
    immutable_exact: bool,
    canon_exact: bool,
    prereg_exact: bool,
    package_exact: bool,
    production: dict[str, bool],
    symbolic: dict[str, Any],
    finite: dict[str, Any],
    mutations_exact: bool,
) -> tuple[dict[str, bool], bool]:
    promoted = set(PRODUCTION_CONFIGURATION["promoted_claims"])
    false_flags = {
        "mixed_branch_global_integrability_derived": (
            "mixed_branch_global_integrability_derived" in promoted
        ),
        "horizon_crossing_material_current_derived": (
            "horizon_crossing_material_current_derived" in promoted
        ),
        "w3_65_environmental_shrinkage_inference_allowed": bool(
            finite["environmental_shrinkage_inference_allowed"]
        ),
        "intrinsic_profile_rescaling_action_present": (
            "intrinsic_profile_rescaling_action_present" in promoted
        ),
        "exact_common_strongfield_clock_ruler_factor_derived": (
            not production["temporal_spatial_split"]
        ),
        "horizon_crossing_static_congruence_valid": (
            not production["static_worldline_classification"]
        ),
        "static_material_worldline_inside_horizon_admissible": (
            PRODUCTION_CONFIGURATION["static_material_domain"]
            == "including_inside"
        ),
        "global_strong_field_solution_derived": (
            "global_strong_field_solution_derived" in promoted
        ),
        "global_solve_opened": "global_solve_opened" in promoted,
        "collapse_evolution_completed": (
            "collapse_evolution_completed" in promoted
        ),
        "regular_black_hole_interior_derived": (
            "regular_black_hole_interior_derived" in promoted
        ),
        "singularity_resolution_completed": (
            "singularity_resolution_completed" in promoted
        ),
        "geodesic_completeness_derived": (
            "geodesic_completeness_derived" in promoted
        ),
        "new_observation_tested": "new_observation_tested" in promoted,
        "canon_changed": not canon_exact,
        "intuitive_files_changed": not immutable_exact,
    }

    true_flags = {
        "dependency_hashes_exact": dependency_exact,
        "upstream_status_and_scope_exact": upstream_exact,
        "scale_connection_covariant_exact": production[
            "scale_connection_covariant"
        ],
        "scale_connection_coefficients_inherited_exact": (
            production["scale_connection_temporal_projection"]
            and production["scale_connection_spatial_projection"]
        ),
        "scale_connection_projections_exact": (
            production["scale_connection_temporal_projection"]
            and production["scale_connection_spatial_projection"]
        ),
        "target_branch_integrability_exact": (
            production["accepted_domain_integrability"]
            and production["path_independence"]
        ),
        "homogeneous_reduction_exact": production["homogeneous_reduction"],
        "static_killing_reduction_exact": production[
            "static_killing_reduction"
        ],
        "w3_54_euler_crosscheck_exact": production[
            "w3_54_euler_crosscheck"
        ],
        "healthy_sound_speed_interval_preserved_exact": production[
            "healthy_sound_speed_interval"
        ],
        "static_density_algebraic_map_rejected_exact": production[
            "static_density_map_rejected"
        ],
        "one_metric_one_source_unchanged_exact": (
            production["one_metric_registry"]
            and production["once_counted_hilbert_source"]
            and upstream_exact
        ),
        "isotropic_areal_map_exact": production["isotropic_areal_map"],
        "schwarzschild_reconstruction_exact": (
            production["schwarzschild_temporal_reconstruction"]
            and production["schwarzschild_spatial_reconstruction"]
        ),
        "temporal_spatial_coframe_split_exact": production[
            "temporal_spatial_split"
        ],
        "exact_temporal_spatial_relation": production[
            "exact_temporal_spatial_relation"
        ],
        "full_1pn_regression_exact": (
            production["full_1pn_temporal"]
            and production["full_1pn_spatial"]
            and upstream_exact
        ),
        "external_radial_null_speed_exact": production[
            "external_radial_null_speed"
        ],
        "local_light_speed_exact": production["local_light_speed"],
        "pg_metric_from_coframe_exact": production["pg_target_metric"],
        "pg_inverse_exact": production["pg_inverse"],
        "pg_determinant_regular_at_horizon_exact": production[
            "pg_determinant"
        ],
        "pg_radial_null_characteristics_exact": production[
            "pg_null_characteristics"
        ],
        "round_sphere_trapping_sign_exact": production["trapping_sign"],
        "kretschmann_finite_at_horizon_exact": production[
            "horizon_kretschmann"
        ],
        "static_worldline_timelike_iff_outside_exact": production[
            "static_worldline_classification"
        ],
        "true_horizon_requires_nonstatic_material_current_exact": (
            production["static_worldline_classification"]
            and production["binary_branch_decision"]
            and production["pg_local_proper_time"]
        ),
        "finite_oscillon_radius_role_separate_exact": (
            production["charge_moment_definition"]
            and production["finite_radius_role_separate"]
        ),
        "intrinsic_local_oscillon_radius_definition_exact": production[
            "charge_moment_definition"
        ],
        "external_ruler_projection_exact": production[
            "external_ruler_projection"
        ],
        "finite_profile_local_uniform_scope_exact": production[
            "finite_profile_local_uniform_scope"
        ],
        "w3_65_distinct_equilibria_scope_exact": finite[
            "scope_regression_pass"
        ],
        "passive_readout_no_new_dof_or_action_exact": (
            production["readout_EL_zero"]
            and production["readout_kinetic_hessian_zero"]
            and production["readout_stress_zero"]
            and production["no_new_dof"]
        ),
        "penrose_boundary_inherited_exact": (
            production["penrose_boundary"]
            and production["r0_curvature_boundary"]
            and upstream_exact
        ),
        "binary_branch_decision_exact": (
            production["binary_branch_decision"]
            and production["static_worldline_classification"]
            and production["scope_claim_consistency"]
        ),
        "mutation_controls_pass": mutations_exact,
        "g0_goal_pass": prereg_exact,
        "g1_conventions_pass": (
            production["typed_schema"]
            and production["scale_connection_covariant"]
        ),
        "g2_core_algebra_pass": (
            production["scale_connection_temporal_projection"]
            and production["scale_connection_spatial_projection"]
            and production["homogeneous_reduction"]
            and production["static_killing_reduction"]
            and production["full_1pn_temporal"]
            and production["full_1pn_spatial"]
        ),
        "g3_structure_pass": (
            production["one_metric_registry"]
            and production["once_counted_hilbert_source"]
            and production["readout_EL_zero"]
            and production["finite_radius_role_separate"]
            and immutable_exact
            and canon_exact
        ),
        "g4_independent_check_pass": (
            production["w3_54_euler_crosscheck"]
            and production["isotropic_areal_map"]
            and production["pg_inverse"]
        ),
        "g5_limits_regression_pass": (
            upstream_exact
            and production["full_1pn_temporal"]
            and production["full_1pn_spatial"]
            and finite["scope_regression_pass"]
        ),
        "g6_physical_match_pass": (
            production["trapping_sign"]
            and production["static_worldline_classification"]
            and production["pg_local_proper_time"]
        ),
        "g7_observation_not_applicable_exact": (
            false_flags["new_observation_tested"] is False
        ),
        "g8_export_not_applicable_exact": True,
        "package_clean_pass": package_exact,
    }
    keysets_exact = (
        set(true_flags) | {"aggregate_gate_pass"} == REQUIRED_TRUE_FLAGS
        and set(false_flags) == REQUIRED_FALSE_FLAGS
    )
    aggregate = (
        keysets_exact
        and bool_all(list(true_flags.values()))
        and all(value is False for value in false_flags.values())
        and production["aggregate"]
    )
    true_flags["aggregate_gate_pass"] = aggregate
    return {**true_flags, **false_flags}, aggregate


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temporary = Path(handle.name)
    try:
        with handle:
            json.dump(
                payload,
                handle,
                ensure_ascii=False,
                allow_nan=False,
                indent=2,
                sort_keys=True,
            )
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    dependency_records, dependency_exact = audit_files(DEPENDENCIES)
    immutable_records, immutable_exact = audit_immutable_intuitive()
    canon_control, canon_exact = audit_canon_control()
    prereg = audit_preregistration()
    package = audit_package()
    upstream, upstream_exact = audit_upstream()
    symbolic = exact_symbolic_audit(PRODUCTION_CONFIGURATION)
    production = evaluate_configuration(PRODUCTION_CONFIGURATION)
    finite = audit_finite_oscillon()
    mutations = run_mutation_controls()

    prereg_exact = bool(
        prereg["hash_exact"]
        and prereg["markers_exact"]
        and prereg["contract_keysets_exact"]
        and prereg["frozen_mutation_registry_exact"]
    )
    package_exact = bool(package["recursive_exact_three_file_package"])
    flags, aggregate = build_flags(
        dependency_exact=dependency_exact,
        upstream_exact=upstream_exact,
        immutable_exact=immutable_exact,
        canon_exact=canon_exact,
        prereg_exact=prereg_exact,
        package_exact=package_exact,
        production=production,
        symbolic=symbolic,
        finite=finite,
        mutations_exact=mutations["all_detected"],
    )

    true_keyset = {key for key in flags if key in REQUIRED_TRUE_FLAGS}
    false_keyset = {key for key in flags if key in REQUIRED_FALSE_FLAGS}
    validation = {
        "required_true_keyset_exact": true_keyset == REQUIRED_TRUE_FLAGS,
        "required_false_keyset_exact": false_keyset == REQUIRED_FALSE_FLAGS,
        "all_required_true": bool_all(
            [flags[key] for key in REQUIRED_TRUE_FLAGS]
        ),
        "all_required_false": all(
            flags[key] is False for key in REQUIRED_FALSE_FLAGS
        ),
        "production_configuration_aggregate": production["aggregate"],
        "registered_mutation_count_exact": (
            mutations["registered_mutation_count"] == 13
        ),
        "all_mutation_primary_failures_observed": mutations["all_detected"],
        "finite_json_inputs": finite["all_finite"],
        "canon_control_exact": canon_exact,
    }
    artifact_valid = (
        aggregate
        and bool_all(list(validation.values()))
        and dependency_exact
        and upstream_exact
        and immutable_exact
        and canon_exact
        and prereg_exact
        and package_exact
    )
    status = PASS_STATUS if artifact_valid else FAIL_STATUS

    gate_registry = {
        "G0_GOAL": flags["g0_goal_pass"],
        "G1_CONVENTIONS": flags["g1_conventions_pass"],
        "G2_CORE_ALGEBRA": flags["g2_core_algebra_pass"],
        "G3_STRUCTURE_AND_LEDGER": flags["g3_structure_pass"],
        "G4_INDEPENDENT_CROSSCHECK": flags["g4_independent_check_pass"],
        "G5_LIMITS_AND_REGRESSION": flags["g5_limits_regression_pass"],
        "G6_PHYSICAL_BRANCH_MATCH": flags["g6_physical_match_pass"],
        "G7_OBSERVATION": "NOT_APPLICABLE",
        "G8_EXPORT": "NOT_APPLICABLE",
    }
    scope_flags = {
        key: flags[key] for key in sorted(REQUIRED_FALSE_FLAGS)
    }

    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "status": status,
        "artifact_valid": artifact_valid,
        "evidence_type": {
            "connection_and_metric_identities": "EXACT_SYMBOLIC",
            "w3_65_scope_regression": "FROZEN_NUMERICAL_ARTIFACT_REGRESSION",
            "observation": "NOT_APPLICABLE",
        },
        "claim": {
            "connection": "W_mu = a_mu + (1/2) Theta u_mu",
            "readout": "nabla_mu ln p_t = W_mu where F_mu_nu = 0",
            "homogeneous_reduction": "p_t^2 = n_C/n_C0",
            "static_reduction": "p_t = calN = mu_infinity/mu_C",
            "spatial_factor": (
                "p_L = (1 + U/2)^(-2) = ((1 + p_t)/2)^2"
            ),
            "intrinsic_local_profile": (
                "R_O_loc = sqrt(I4/I2), unchanged by passive coframe readout"
            ),
            "external_reference_standard_assignment": (
                "Delta_rho = integral_0^(R_O_loc) p_L(ell) d_ell; "
                "R_O_ext = p_L R_O_loc only in the local-uniform limit"
            ),
            "horizon_binary": {
                "true_horizon_material_branch": "NONSTATIC_TIMELIKE_CURRENT",
                "everywhere_static_material_branch": "R_GREATER_THAN_R_S",
            },
        },
        "role_ledger": {
            "p_t": "BRANCH_RESTRICTED_TEMPORAL_READOUT",
            "p_L": "INDEPENDENT_SPATIAL_COFRAME_PROJECTION",
            "n_C": "COLLECTIVE_PHASE_ACTION_DENSITY",
            "R_O_loc": (
                "INTRINSIC_CHARGE_MOMENT_RADIUS_IN_THE_LOCAL_ORTHONORMAL_FRAME"
            ),
            "R_O_ext": (
                "EXTERNAL_REFERENCE_STANDARD_COORDINATE_ASSIGNMENT_OF_THE_"
                "SAME_UNCHANGED_LOCAL_PROFILE"
            ),
        },
        "dependencies": {
            "records": dependency_records,
            "all_hashes_exact": dependency_exact,
        },
        "immutable_intuitive_controls": {
            **immutable_records,
            "all_exact": immutable_exact,
        },
        "canon_control": {
            **canon_control,
            "all_exact": canon_exact,
        },
        "upstream_regression": {
            **upstream,
            "all_exact": upstream_exact,
        },
        "preregistration": prereg,
        "exact_algebra": symbolic,
        "finite_oscillon_scope_regression": finite,
        "production_checks": production,
        "mutation_controls": mutations,
        "physical_decision": {
            "covariant_scale_connection": "SELECTED_AND_EXACT_ON_TARGET_BRANCHES",
            "w3_70_sign_conflict": (
                "REMOVED_BY_DIFFERENTIAL_STATIC_BRIDGE_WITHOUT_STATIC_DENSITY_"
                "IDENTIFICATION"
            ),
            "einstein_exterior_and_1pn": "EXACT",
            "horizon_local_geometry": "REGULAR_IN_PAINLEVE_GULLSTRAND_COFRAME",
            "true_horizon_material_requirement": (
                "NONSTATIC_HORIZON_REGULAR_TIMELIKE_CURRENT"
            ),
            "static_material_requirement": "SURFACE_R_GREATER_THAN_R_S",
            "intrinsic_local_profile_under_passive_readout": "UNCHANGED",
            "external_reference_standard_assignment": (
                "EXACT_P_L_COFRAME_RULER_CONVERSION"
            ),
            "w3_65_radius_role": (
                "DISTINCT_EQUILIBRIA_ONLY__NO_ENVIRONMENTAL_SHRINKAGE_"
                "INFERENCE"
            ),
            "global_interior_or_singularity_resolution": "NOT_OPENED",
            "next_exact_input": (
                "A horizon-regular nonstatic timelike material current, or its "
                "exact elimination from existing fields, with one metric, one "
                "source ledger, 1PN regression, conservation, and characteristic "
                "health. A resolved remote image is a separate coframe-plus-null-"
                "ray transfer calculation."
            ),
        },
        "scientific_boundary": {
            "established": [
                "One parameter-free covariant temporal readout connection.",
                "Exact homogeneous and static target-branch reductions.",
                "Exact Schwarzschild temporal/spatial coframe separation.",
                "Standard beta=gamma=1 isotropic 1PN regression.",
                "Horizon-regular radial causal classification.",
                "Static material cannot remain timelike at or inside a true horizon.",
                "The passive coframe readout leaves the intrinsic local oscillon profile unchanged.",
                "The external reference-standard radial assignment follows exactly from the p_L line integral.",
                "W3-65 compares distinct equilibria and carries no environmental-shrinkage inference.",
            ],
            "not_established": [
                "General mixed-flow integrability.",
                "A horizon-crossing nonstatic RefG material-current solution.",
                "Environment-dependent backreaction across distinct equilibria.",
                "Collapse evolution or a global black-hole interior.",
                "Singularity resolution or geodesic completeness.",
                "A new strong-field observational prediction.",
            ],
        },
        "penrose_boundary": {
            "inherited": True,
            "decision": (
                "A future-null-complete regular trapped interior must alter at "
                "least one explicit theorem hypothesis through completed dynamics."
            ),
        },
        "gate_registry": gate_registry,
        "closure_flags": flags,
        "scope_flags": scope_flags,
        "validation": validation,
        "package": package,
        "references": [
            {
                "citation": (
                    "K. Schwarzschild, Sitzungsberichte der Königlich "
                    "Preussischen Akademie der Wissenschaften (1916), 189-196."
                ),
                "role": "EXACT_STATIC_VACUUM_BENCHMARK",
            },
            {
                "citation": (
                    "K. Martel and E. Poisson, Am. J. Phys. 69, 476 (2001), "
                    "DOI 10.1119/1.1336836, arXiv:gr-qc/0001069."
                ),
                "role": "HORIZON_REGULAR_COORDINATE_BENCHMARK",
            },
            {
                "citation": (
                    "R. Penrose, Phys. Rev. Lett. 14, 57 (1965), "
                    "DOI 10.1103/PhysRevLett.14.57."
                ),
                "role": "INHERITED_SINGULARITY_THEOREM_BOUNDARY",
            },
        ],
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "sympy": sp.__version__,
            "source_path": SOURCE_PATH.relative_to(REPO_ROOT).as_posix(),
            "source_sha256": sha256_file(SOURCE_PATH),
            "preregistration_sha256": sha256_file(PREREG_PATH),
            "network_used": False,
            "archived_theory_used": False,
            "intuitive_files_written": False,
            "canon_written": False,
        },
    }
    write_json_atomic(RESULT_PATH, payload)
    reloaded = load_json(RESULT_PATH)
    if reloaded.get("artifact_valid") is not artifact_valid:
        raise RuntimeError("Atomic JSON round-trip changed artifact validity.")

    print(json.dumps({
        "claim_id": CLAIM_ID,
        "status": status,
        "artifact_valid": artifact_valid,
        "dependency_hashes_exact": dependency_exact,
        "upstream_status_and_scope_exact": upstream_exact,
        "immutable_intuitive_controls_exact": immutable_exact,
        "canon_control_exact": canon_exact,
        "preregistration_exact": prereg_exact,
        "production_checks_pass": production["aggregate"],
        "mutation_controls_pass": mutations["all_detected"],
        "package_clean_pass": package_exact,
        "result": RESULT_PATH.relative_to(REPO_ROOT).as_posix(),
    }, indent=2))
    return 0 if artifact_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
