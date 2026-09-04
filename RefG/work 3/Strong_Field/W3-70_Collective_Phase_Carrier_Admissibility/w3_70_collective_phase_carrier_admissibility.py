#!/usr/bin/env python3
"""W3-70 exact collective-phase carrier admissibility audit."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sympy as sp


CLAIM_ID = "W3_70_COLLECTIVE_PHASE_CARRIER_ADMISSIBILITY"
MODEL_VERSION = "W3-70-v1.0-COLLECTIVE-PHASE-CARRIER-ADMISSIBILITY"
PASS_STATUS = (
    "PASS_EXACT_STATIONARY_PHASE_BERNOULLI_AND_RESPONSE_SIGN_AUDIT__"
    "REJECTED_AS_UNIVERSAL_LOCAL_P_CARRIER_BY_HEALTHY_EOS_SIGN_CONTRADICTION__"
    "GLOBAL_STRONG_FIELD_SOLVE_NOT_OPENED"
)
FAIL_STATUS = "FAIL_W3_70_COLLECTIVE_PHASE_CARRIER_AUDIT"

SOURCE_PATH = Path(__file__).resolve()
PACKAGE_DIR = SOURCE_PATH.parent
REPO_ROOT = SOURCE_PATH.parents[4]
PREREG_PATH = PACKAGE_DIR / "w3_70_collective_phase_carrier_admissibility_preregistration.md"
RESULT_PATH = PACKAGE_DIR / "w3_70_result.json"
PREREG_SHA256 = "e91aaa5e6141eaaef13e35b9a00e824c1c11b61e66120f70591dbe14337e2204"

EXPECTED_PACKAGE_FILES = {
    "w3_70_collective_phase_carrier_admissibility_preregistration.md",
    "w3_70_collective_phase_carrier_admissibility.py",
    "w3_70_result.json",
}

DEPENDENCIES = {
    "RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/"
    "w3_50_neutral_collective_phase_density_bridge_contract.md":
        "c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635",
    "RefG/work 3/Lagrangian_Formulation/Weak_Field_Closure/"
    "w3_51_weak_field_closure_contract.md":
        "86bc2ed86cddee36bec5e46fdfa407701107290c783bfa81ba1440b96becc7cf",
    "RefG/work 3/Lagrangian_Formulation/Weak_Field_Closure/w3_51_result.json":
        "a74e0f02c5a5c794723a5797049bd28d95684a95be869db30f10a575d3ee9cf8",
    "RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/"
    "w3_54_relational_coframe_tegr_phase_source_closure_contract.md":
        "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
    "RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/"
    "w3_54_result.json":
        "ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991",
    "RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/"
    "w3_67_foundation_strong_field_response_preregistration.md":
        "31e6520d9b7917413b9f2978291b4a77f067abe8dd3d6a9e89e1b2cfb699da11",
    "RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_result.json":
        "659bdfe171a8279b465fdd49eaf590755da22a7522a83053a4a06450fd745385",
    "RefG/work 3/Strong_Field/W3-69_Algebraic_Material_Response_Candidate/"
    "w3_69_algebraic_material_response_candidate_preregistration.md":
        "b5ef9e7a7740fae6d8fbf8b42058ea275afb96b6a801c5c4a5ce0e83cebd0c38",
    "RefG/work 3/Strong_Field/W3-69_Algebraic_Material_Response_Candidate/"
    "w3_69_result.json":
        "ad3d0315acfe2276ecf0d7f3c6d60d89e06bae39afc18fc34d35138742626f22",
}

IMMUTABLE_CONTROLS = {
    "CODES.md": "27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41",
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
    "g0_goal_pass",
    "g1_conventions_pass",
    "g2_core_algebra_pass",
    "g3_structure_pass",
    "g4_independent_check_pass",
    "g5_limits_regression_pass",
    "g6_physical_match_pass",
    "g7_observation_not_applicable_exact",
    "g8_export_not_applicable_exact",
    "dependency_hashes_exact",
    "upstream_status_and_scope_exact",
    "immutable_controls_exact",
    "candidate_local_extension_registered_exact",
    "static_total_lapse_and_no_flux_branch_registered_exact",
    "phase_bernoulli_first_integral_exact",
    "sound_speed_log_slope_exact",
    "positive_mass_operational_lapse_sign_exact",
    "healthy_density_response_sign_exact",
    "candidate_joint_residual_requires_cs2_minus_half_exact",
    "required_cs2_violates_w3_54_health_exact",
    "zero_sound_speed_regular_response_rejected_exact",
    "inverse_density_control_matches_at_cs2_half_exact",
    "inverse_density_control_breaks_homogeneous_dictionary_exact",
    "chemical_potential_lapse_readout_exact",
    "chemical_potential_map_is_passive_exact",
    "temporal_only_scope_and_coframe_split_preserved_exact",
    "one_metric_one_source_no_new_action_exact",
    "upstream_einstein_and_1pn_branch_unchanged_exact",
    "candidate_role_rejected_before_global_solve_exact",
    "next_missing_premise_narrowed_exact",
    "mutation_controls_pass",
    "package_clean_pass",
    "aggregate_gate_pass",
}

REQUIRED_FALSE_FLAGS = {
    "candidate_admissible",
    "collective_density_universal_local_operational_p_derived",
    "accepted_homogeneous_phase_law_falsified",
    "healthy_barotropic_eos_realizes_frozen_candidate",
    "P_F_equals_p_C_derived",
    "exact_common_factor_full_strong_field_coframe_derived",
    "branch_discriminator_derived",
    "multivariate_response_bridge_derived",
    "alternative_carrier_selected",
    "active_mixed_response_action_derived",
    "foundation_strong_field_response_derived",
    "global_strong_field_solve_opened",
    "black_hole_solution_derived",
    "penrose_hypothesis_change_selected",
    "singularity_resolution_completed",
    "new_strong_field_prediction_derived",
    "observation_tested",
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


def bool_all(values: list[bool]) -> bool:
    return all(value is True for value in values)


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


def audit_immutable_controls() -> tuple[dict[str, Any], bool]:
    records, hashes_exact = audit_files(IMMUTABLE_CONTROLS)
    intuitive_root = REPO_ROOT / "intuitive"
    actual_intuitive_files = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in intuitive_root.rglob("*")
        if path.is_file()
    )
    expected_intuitive_files = sorted(
        path for path in IMMUTABLE_CONTROLS if path.startswith("intuitive/")
    )
    file_set_exact = actual_intuitive_files == expected_intuitive_files
    result = {
        "records": records,
        "expected_intuitive_files": expected_intuitive_files,
        "actual_intuitive_files": actual_intuitive_files,
        "intuitive_file_set_exact": file_set_exact,
        "hashes_exact": hashes_exact,
    }
    return result, hashes_exact and file_set_exact


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
    anticipated_files = set(actual_files)
    anticipated_files.add(RESULT_PATH.name)
    clean = anticipated_files == EXPECTED_PACKAGE_FILES and not actual_dirs
    return {
        "expected_files": sorted(EXPECTED_PACKAGE_FILES),
        "actual_files_before_write": actual_files,
        "anticipated_files_after_write": sorted(anticipated_files),
        "actual_directories": actual_dirs,
        "recursive_exact_three_file_package": clean,
    }


def audit_preregistration() -> dict[str, Any]:
    text = PREREG_PATH.read_text(encoding="utf-8")
    required_markers = {
        "claim_id": "`W3_70_COLLECTIVE_PHASE_CARRIER_ADMISSIBILITY`",
        "model_version": "`W3-70-v1.0-COLLECTIVE-PHASE-CARRIER-ADMISSIBILITY`",
        "candidate_map": "p_n(x)^2 = n_C(x)/n_infinity",
        "total_lapse": "calN=sqrt(-xi^2)",
        "bernoulli": "mu(n_C) calN = omega_C = mu_infinity",
        "health": "c_s^2=-1/2",
        "global_witness": "mu(n_C)=mu_infinity (n_C/n_infinity)^(-1/2)",
        "inverse_control": "p_inv^2=n_infinity/n_C",
        "pass_status": PASS_STATUS,
        "stop_rule": "No new action, equation of state, mixed coupling",
    }
    marker_checks = {key: value in text for key, value in required_markers.items()}
    true_block = text.split("Required true:", 1)[1].split("Required false:", 1)[0]
    false_block = text.split("Required false:", 1)[1].split("### CROSSCHECK", 1)[0]
    prereg_true_flags = set(re.findall(r"^- `([A-Za-z0-9_]+)`$", true_block, re.MULTILINE))
    prereg_false_flags = set(
        re.findall(r"^- `([A-Za-z0-9_]+)`$", false_block, re.MULTILINE)
    )
    true_keyset_exact = prereg_true_flags == REQUIRED_TRUE_FLAGS
    false_keyset_exact = prereg_false_flags == REQUIRED_FALSE_FLAGS
    return {
        "expected_sha256": PREREG_SHA256,
        "actual_sha256": sha256_file(PREREG_PATH),
        "hash_exact": sha256_file(PREREG_PATH) == PREREG_SHA256,
        "required_markers": marker_checks,
        "markers_exact": bool_all(list(marker_checks.values())),
        "preregistered_true_flags": sorted(prereg_true_flags),
        "preregistered_false_flags": sorted(prereg_false_flags),
        "required_true_keyset_exact": true_keyset_exact,
        "required_false_keyset_exact": false_keyset_exact,
        "contract_keysets_exact": true_keyset_exact and false_keyset_exact,
    }


def audit_upstream() -> tuple[dict[str, Any], bool]:
    w50_path = REPO_ROOT / (
        "RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/"
        "w3_50_neutral_collective_phase_density_bridge_contract.md"
    )
    w51_path = REPO_ROOT / (
        "RefG/work 3/Lagrangian_Formulation/Weak_Field_Closure/w3_51_result.json"
    )
    w54_path = REPO_ROOT / (
        "RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/"
        "w3_54_result.json"
    )
    w67_path = REPO_ROOT / (
        "RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_result.json"
    )
    w69_path = REPO_ROOT / (
        "RefG/work 3/Strong_Field/W3-69_Algebraic_Material_Response_Candidate/"
        "w3_69_result.json"
    )
    w50 = w50_path.read_text(encoding="utf-8")
    w51 = load_json(w51_path)
    w54 = load_json(w54_path)
    w67 = load_json(w67_path)
    w69 = load_json(w69_path)

    checks = {
        "w50_status_exact": (
            "PASS_EXACT_CONDITIONAL_NEUTRAL_PHASE_DENSITY_CANDIDATE_CURRENT__"
            "W3_48_BRIDGE_CLOSED_GIVEN_SELECTED_ETA_AND_CUBIC_MEASURE__"
            "MASTER_FOUNDATION_ORIGIN_OPEN"
        ) in w50,
        "w50_density_map_exact": (
            "eta_F=n_C/n_C0" in w50 and "p^2=eta_F" in w50
        ),
        "w50_homogeneous_domain_exact": "homogeneous" in w50.lower(),
        "w51_pass": w51.get("gate_status") == "PASS",
        "w51_beta_gamma_one": (
            str(w51.get("derived", {}).get("PPN_beta")) == "1"
            and str(w51.get("derived", {}).get("PPN_gamma")) == "1"
        ),
        "w51_strong_field_not_tested": (
            w51.get("scope_boundary", {}).get("strong_field") == "NOT_TESTED"
        ),
        "w54_status_exact": w54.get("status") == (
            "CONDITIONAL_EXACT_SELECTED_RELATIONAL_COFRAME_MASTER_ACTION_TO_TEGR_"
            "EQUIVALENT_EH_AND_PHASE_CURRENT_T"
        ),
        "w54_phase_equation_exact": (
            w54.get("phase_source", {}).get("J_variation")
            == "partial_mu theta_C + rho_C'(n_C) u_mu/c0 = 0"
        ),
        "w54_phase_current_and_source_exact": (
            w54.get("closure_flags", {}).get("PHASE_CURRENT_CONSERVATION_DERIVED") is True
            and w54.get("closure_flags", {}).get("PHASE_HILBERT_T_DERIVED") is True
            and w54.get("closure_flags", {}).get(
                "ONE_SOURCE_LEDGER_SELECTED_AND_CONSISTENT"
            ) is True
        ),
        "w54_eh_exact": (
            w54.get("closure_flags", {}).get(
                "RELATIONAL_COFRAME_TO_EH_AND_PHASE_T_GATE_CLOSED"
            ) is True
        ),
        "w54_pressure_roles_unmerged": (
            w54.get("closure_flags", {}).get("P_F_EQUALS_P_C_DERIVED") is False
        ),
        "w67_valid_status": (
            w67.get("artifact_valid") is True
            and w67.get("status") == (
                "PASS_EXACT_FOUNDATION_STRONG_FIELD_RESPONSE_BOUNDARY__"
                "PASSIVE_AND_COMMON_RESCALING_NO_GO__"
                "COVARIANT_ACTION_AND_CONSTITUTIVE_SELECTION_OPEN"
            )
        ),
        "w67_full_1pn_inherited": (
            w67.get("closure_flags", {}).get("full_standard_1pn_ppn_inherited_exact")
            is True
        ),
        "w67_response_open": (
            w67.get("scope_flags", {}).get("response_action_derived") is False
            and w67.get("scope_flags", {}).get(
                "foundation_strong_field_response_derived"
            ) is False
        ),
        "w69_valid_role_veto": (
            w69.get("artifact_valid") is True
            and w69.get("physical_decision", {}).get(
                "refg_operational_p_identification"
            ) == "HARD_VETO"
        ),
        "w69_global_solve_unopened": (
            w69.get("physical_decision", {}).get("global_strong_field_solve_opened")
            is False
        ),
    }
    return {"checks": checks}, bool_all(list(checks.values()))


def exact_symbolic_audit(
    candidate_power: sp.Rational = sp.Rational(1, 2),
    bernoulli_sign: int = 1,
) -> dict[str, Any]:
    dlog_lapse, cs2 = sp.symbols("dlog_lapse cs2", nonzero=True, real=True)
    dlog_n = dlog_lapse / candidate_power
    joint_residual = sp.expand(
        cs2 * dlog_n + sp.Integer(bernoulli_sign) * dlog_lapse
    )
    required_cs2 = sp.solve(sp.Eq(joint_residual, 0), cs2)[0]

    inverse_power = -sp.Rational(1, 2)
    inverse_dlog_n = dlog_lapse / inverse_power
    inverse_required_cs2 = sp.solve(
        sp.Eq(
            cs2 * inverse_dlog_n
            + sp.Integer(bernoulli_sign) * dlog_lapse,
            0,
        ),
        cs2,
    )[0]

    u = sp.symbols("u", positive=True)
    weak_dlog_lapse = -u
    weak_dlog_mu = -sp.Integer(bernoulli_sign) * weak_dlog_lapse
    weak_dlog_n = weak_dlog_mu / cs2
    weak_dlog_p_density = sp.simplify(candidate_power * weak_dlog_n)
    weak_dlog_p_operational = weak_dlog_lapse
    weak_difference = sp.simplify(
        weak_dlog_p_density - weak_dlog_p_operational
    )

    y = sp.symbols("y", positive=True)
    mu_density_witness = y ** required_cs2
    chemical_homogeneous_required = sp.solve(
        sp.Eq(-cs2, sp.Rational(1, 2)),
        cs2,
    )[0]
    n = sp.symbols("n", positive=True)
    rho = sp.Function("rho", positive=True)(n)
    mu = sp.diff(rho, n)
    pressure = n * mu - rho
    sound_speed_thermodynamic = sp.simplify(
        sp.diff(pressure, n) / sp.diff(rho, n)
    )
    sound_speed_log_slope = sp.simplify(n * sp.diff(mu, n) / mu)
    sound_speed_residual = sp.simplify(
        sound_speed_thermodynamic - sound_speed_log_slope
    )
    healthy_probe = sp.simplify(
        weak_dlog_n.subs({u: 1, cs2: sp.Rational(1, 2)})
    )
    operational_probe = sp.simplify(weak_dlog_lapse.subs(u, 1))
    zero_cs2_residual = sp.simplify(
        sp.Integer(bernoulli_sign) * dlog_lapse
    )

    return {
        "bernoulli_sign": bernoulli_sign,
        "bernoulli_first_integral_is_mu_times_calN_constant": (
            bernoulli_sign == 1
        ),
        "candidate_power_dlogp_dlogn": sstr(candidate_power),
        "candidate_dlogn_over_dlogcalN": sstr(1 / candidate_power),
        "bernoulli_joint_residual": sstr(joint_residual),
        "required_cs2": sstr(required_cs2),
        "required_cs2_is_minus_half": required_cs2 == -sp.Rational(1, 2),
        "required_cs2_in_closed_health_interval": bool(
            required_cs2.is_real and 0 <= required_cs2 <= 1
        ),
        "inverse_power_dlogp_dlogn": sstr(inverse_power),
        "inverse_required_cs2": sstr(inverse_required_cs2),
        "inverse_required_cs2_is_plus_half": (
            inverse_required_cs2 == sp.Rational(1, 2)
        ),
        "weak_dlogcalN": sstr(weak_dlog_lapse),
        "weak_dlogmu": sstr(weak_dlog_mu),
        "weak_dlogn": sstr(weak_dlog_n),
        "weak_dlogp_density": sstr(weak_dlog_p_density),
        "weak_dlogp_operational": sstr(weak_dlog_p_operational),
        "weak_dictionary_difference": sstr(weak_difference),
        "sound_speed_thermodynamic": sstr(sound_speed_thermodynamic),
        "sound_speed_log_slope": sstr(sound_speed_log_slope),
        "sound_speed_definition_residual": sstr(sound_speed_residual),
        "sound_speed_log_slope_exact": sound_speed_residual == 0,
        "healthy_density_probe_at_u1_cs2half": sstr(healthy_probe),
        "healthy_density_rises_for_positive_u": bool(healthy_probe > 0),
        "operational_p_probe_at_u1": sstr(operational_probe),
        "operational_p_falls_for_positive_u": bool(operational_probe < 0),
        "zero_cs2_regular_linear_response_residual": sstr(zero_cs2_residual),
        "zero_cs2_regular_linear_response_possible": zero_cs2_residual == 0,
        "mu_density_witness": sstr(mu_density_witness),
        "mu_density_witness_log_slope": sstr(required_cs2),
        "chemical_homogeneous_required_cs2": sstr(
            chemical_homogeneous_required
        ),
        "chemical_map_power_of_calN": str(bernoulli_sign),
        "chemical_map_equals_lapse_exact": bernoulli_sign == 1,
    }


def evaluate_configuration(config: dict[str, Any]) -> dict[str, bool]:
    expected = {
        "candidate_power": sp.Rational(1, 2),
        "bernoulli_sign": 1,
        "health_min": 0,
        "health_max": 1,
        "zero_cs_response_accepted": False,
        "homogeneous_slope": sp.Rational(1, 2),
        "total_lapse_used": True,
        "temporal_only": True,
        "new_action_inserted": False,
        "new_source_inserted": False,
        "candidate_accepted": False,
        "global_solve_opened": False,
    }
    symbolic = exact_symbolic_audit(
        sp.Rational(config["candidate_power"]),
        int(config["bernoulli_sign"]),
    )
    required_cs2 = sp.Rational(symbolic["required_cs2"])
    health_min = sp.Rational(config["health_min"])
    health_max = sp.Rational(config["health_max"])

    checks = {
        "candidate_definition_exact": (
            sp.Rational(config["candidate_power"]) == expected["candidate_power"]
        ),
        "bernoulli_sign_exact": config["bernoulli_sign"] == expected["bernoulli_sign"],
        "health_registry_exact": (
            health_min == expected["health_min"]
            and health_max == expected["health_max"]
        ),
        "required_cs2_exact": (
            symbolic["required_cs2_is_minus_half"] is True
        ),
        "health_veto_exact": (
            not (health_min <= required_cs2 <= health_max)
        ),
        "zero_sound_endpoint_exact": (
            config["zero_cs_response_accepted"]
            is expected["zero_cs_response_accepted"]
        ),
        "homogeneous_slope_exact": (
            sp.Rational(config["homogeneous_slope"])
            == expected["homogeneous_slope"]
        ),
        "total_lapse_exact": (
            config["total_lapse_used"] is expected["total_lapse_used"]
        ),
        "temporal_scope_exact": (
            config["temporal_only"] is expected["temporal_only"]
        ),
        "no_new_action_exact": (
            config["new_action_inserted"] is expected["new_action_inserted"]
        ),
        "no_new_source_exact": (
            config["new_source_inserted"] is expected["new_source_inserted"]
        ),
        "candidate_rejection_exact": (
            config["candidate_accepted"] is expected["candidate_accepted"]
        ),
        "global_solve_stop_exact": (
            config["global_solve_opened"] is expected["global_solve_opened"]
        ),
    }
    checks["aggregate"] = bool_all(list(checks.values()))
    return checks


PRODUCTION_CONFIGURATION = {
    "candidate_power": sp.Rational(1, 2),
    "bernoulli_sign": 1,
    "health_min": 0,
    "health_max": 1,
    "zero_cs_response_accepted": False,
    "homogeneous_slope": sp.Rational(1, 2),
    "total_lapse_used": True,
    "temporal_only": True,
    "new_action_inserted": False,
    "new_source_inserted": False,
    "candidate_accepted": False,
    "global_solve_opened": False,
}


def run_mutation_controls() -> dict[str, Any]:
    mutations = {
        "wrong_bernoulli_sign": {"bernoulli_sign": -1},
        "inverse_map_substituted_for_candidate": {
            "candidate_power": -sp.Rational(1, 2)
        },
        "negative_sound_speed_declared_healthy": {"health_min": -1},
        "zero_sound_response_silently_accepted": {
            "zero_cs_response_accepted": True
        },
        "homogeneous_dictionary_reversed": {
            "homogeneous_slope": -sp.Rational(1, 2)
        },
        "radial_metric_function_used_as_total_lapse": {"total_lapse_used": False},
        "temporal_factor_promoted_to_full_coframe": {"temporal_only": False},
        "new_action_silently_inserted": {"new_action_inserted": True},
        "duplicate_source_silently_inserted": {"new_source_inserted": True},
        "candidate_promoted_despite_veto": {"candidate_accepted": True},
        "global_solve_promoted": {"global_solve_opened": True},
    }
    records: dict[str, Any] = {}
    for name, change in mutations.items():
        mutated = dict(PRODUCTION_CONFIGURATION)
        mutated.update(change)
        checks = evaluate_configuration(mutated)
        records[name] = {
            "change": {key: str(value) for key, value in change.items()},
            "aggregate_after_mutation": checks["aggregate"],
            "detected": checks["aggregate"] is False,
            "failed_checks": sorted(
                key for key, value in checks.items()
                if key != "aggregate" and value is False
            ),
        }
    return {
        "records": records,
        "all_detected": bool_all(
            [record["detected"] for record in records.values()]
        ),
    }


def build_flags(
    dependency_exact: bool,
    upstream_exact: bool,
    immutable_exact: bool,
    package_exact: bool,
    prereg_exact: bool,
    symbolic: dict[str, Any],
    production_checks: dict[str, bool],
    mutations_exact: bool,
) -> tuple[dict[str, bool], bool]:
    candidate_admissible = bool(
        symbolic["required_cs2_in_closed_health_interval"]
        and production_checks["candidate_definition_exact"]
        and production_checks["bernoulli_sign_exact"]
    )

    true_flags = {
        "g0_goal_pass": prereg_exact,
        "g1_conventions_pass": production_checks["total_lapse_exact"],
        "g2_core_algebra_pass": (
            symbolic["required_cs2_is_minus_half"] is True
            and symbolic["inverse_required_cs2_is_plus_half"] is True
        ),
        "g3_structure_pass": (
            production_checks["candidate_rejection_exact"]
            and production_checks["no_new_action_exact"]
        ),
        "g4_independent_check_pass": (
            symbolic["healthy_density_rises_for_positive_u"] is True
            and symbolic["operational_p_falls_for_positive_u"] is True
        ),
        "g5_limits_regression_pass": upstream_exact,
        "g6_physical_match_pass": candidate_admissible is False,
        "g7_observation_not_applicable_exact": True,
        "g8_export_not_applicable_exact": True,
        "dependency_hashes_exact": dependency_exact,
        "upstream_status_and_scope_exact": upstream_exact,
        "immutable_controls_exact": immutable_exact,
        "candidate_local_extension_registered_exact": (
            prereg_exact and production_checks["candidate_definition_exact"]
        ),
        "static_total_lapse_and_no_flux_branch_registered_exact": (
            prereg_exact and production_checks["total_lapse_exact"]
        ),
        "phase_bernoulli_first_integral_exact": (
            production_checks["bernoulli_sign_exact"]
            and symbolic[
                "bernoulli_first_integral_is_mu_times_calN_constant"
            ] is True
        ),
        "sound_speed_log_slope_exact": (
            symbolic["sound_speed_log_slope_exact"] is True
        ),
        "positive_mass_operational_lapse_sign_exact": (
            symbolic["operational_p_falls_for_positive_u"] is True
        ),
        "healthy_density_response_sign_exact": (
            symbolic["healthy_density_rises_for_positive_u"] is True
        ),
        "candidate_joint_residual_requires_cs2_minus_half_exact": (
            symbolic["required_cs2_is_minus_half"] is True
        ),
        "required_cs2_violates_w3_54_health_exact": (
            symbolic["required_cs2_in_closed_health_interval"] is False
            and production_checks["health_registry_exact"]
        ),
        "zero_sound_speed_regular_response_rejected_exact": (
            symbolic["zero_cs2_regular_linear_response_possible"] is False
            and production_checks["zero_sound_endpoint_exact"]
        ),
        "inverse_density_control_matches_at_cs2_half_exact": (
            symbolic["inverse_required_cs2_is_plus_half"] is True
        ),
        "inverse_density_control_breaks_homogeneous_dictionary_exact": (
            symbolic["inverse_power_dlogp_dlogn"] == "-1/2"
            and production_checks["homogeneous_slope_exact"]
        ),
        "chemical_potential_lapse_readout_exact": (
            symbolic["chemical_map_equals_lapse_exact"] is True
        ),
        "chemical_potential_map_is_passive_exact": (
            production_checks["no_new_action_exact"]
            and production_checks["no_new_source_exact"]
        ),
        "temporal_only_scope_and_coframe_split_preserved_exact": (
            production_checks["temporal_scope_exact"] and upstream_exact
        ),
        "one_metric_one_source_no_new_action_exact": (
            production_checks["no_new_action_exact"]
            and production_checks["no_new_source_exact"]
            and upstream_exact
        ),
        "upstream_einstein_and_1pn_branch_unchanged_exact": upstream_exact,
        "candidate_role_rejected_before_global_solve_exact": (
            candidate_admissible is False
            and production_checks["candidate_rejection_exact"]
            and production_checks["global_solve_stop_exact"]
        ),
        "next_missing_premise_narrowed_exact": prereg_exact,
        "mutation_controls_pass": mutations_exact,
        "package_clean_pass": package_exact,
    }

    false_flags = {
        "candidate_admissible": candidate_admissible,
        "collective_density_universal_local_operational_p_derived": False,
        "accepted_homogeneous_phase_law_falsified": False,
        "healthy_barotropic_eos_realizes_frozen_candidate": False,
        "P_F_equals_p_C_derived": False,
        "exact_common_factor_full_strong_field_coframe_derived": False,
        "branch_discriminator_derived": False,
        "multivariate_response_bridge_derived": False,
        "alternative_carrier_selected": False,
        "active_mixed_response_action_derived": False,
        "foundation_strong_field_response_derived": False,
        "global_strong_field_solve_opened": False,
        "black_hole_solution_derived": False,
        "penrose_hypothesis_change_selected": False,
        "singularity_resolution_completed": False,
        "new_strong_field_prediction_derived": False,
        "observation_tested": False,
    }

    keysets_exact = (
        set(true_flags) | {"aggregate_gate_pass"} == REQUIRED_TRUE_FLAGS
        and set(false_flags) == REQUIRED_FALSE_FLAGS
    )
    aggregate = (
        keysets_exact
        and bool_all(list(true_flags.values()))
        and all(value is False for value in false_flags.values())
    )
    true_flags["aggregate_gate_pass"] = aggregate
    flags = {**true_flags, **false_flags}
    return flags, aggregate


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temp_path = Path(handle.name)
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
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def main() -> int:
    dependency_records, dependency_exact = audit_files(DEPENDENCIES)
    immutable_records, immutable_exact = audit_immutable_controls()
    package = audit_package()
    prereg = audit_preregistration()
    upstream, upstream_exact = audit_upstream()
    symbolic = exact_symbolic_audit()
    production_checks = evaluate_configuration(PRODUCTION_CONFIGURATION)
    mutations = run_mutation_controls()

    prereg_exact = bool(
        prereg["hash_exact"]
        and prereg["markers_exact"]
        and prereg["contract_keysets_exact"]
    )
    package_exact = bool(package["recursive_exact_three_file_package"])
    flags, aggregate = build_flags(
        dependency_exact=dependency_exact,
        upstream_exact=upstream_exact,
        immutable_exact=immutable_exact,
        package_exact=package_exact,
        prereg_exact=prereg_exact,
        symbolic=symbolic,
        production_checks=production_checks,
        mutations_exact=mutations["all_detected"],
    )

    true_keyset = sorted(
        key for key in flags if key in REQUIRED_TRUE_FLAGS
    )
    false_keyset = sorted(
        key for key in flags if key in REQUIRED_FALSE_FLAGS
    )
    validation = {
        "required_true_keyset_exact": set(true_keyset) == REQUIRED_TRUE_FLAGS,
        "required_false_keyset_exact": set(false_keyset) == REQUIRED_FALSE_FLAGS,
        "all_required_true": bool_all(
            [flags[key] for key in REQUIRED_TRUE_FLAGS]
        ),
        "all_required_false": all(
            flags[key] is False for key in REQUIRED_FALSE_FLAGS
        ),
        "production_configuration_aggregate": production_checks["aggregate"],
        "candidate_rejection_is_computed": (
            flags["candidate_admissible"] is False
            and flags[
                "candidate_joint_residual_requires_cs2_minus_half_exact"
            ] is True
            and flags["required_cs2_violates_w3_54_health_exact"] is True
        ),
        "actual_global_solve_state_controls_stop_rule": (
            PRODUCTION_CONFIGURATION["global_solve_opened"] is False
            and production_checks["global_solve_stop_exact"] is True
            and flags["global_strong_field_solve_opened"] is False
        ),
    }
    validation["all_exact"] = bool_all(list(validation.values()))
    artifact_valid = aggregate and validation["all_exact"]
    status = PASS_STATUS if artifact_valid else FAIL_STATUS

    payload: dict[str, Any] = {
        "schema_version": "W3-70-result-v1.0",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "status": status,
        "artifact_valid": artifact_valid,
        "candidate_admissible": flags["candidate_admissible"],
        "evidence_type": (
            "EXACT_STATIONARY_PHASE_FIRST_INTEGRAL_AND_CONSTITUTIVE_SIGN_"
            "AUDIT_WITH_HARD_CARRIER_ROLE_REJECTION"
        ),
        "claim": {
            "tested_candidate": "p_n^2=n_C/n_infinity",
            "stationary_temporal_identification": "p_n=calN=sqrt(-xi^2)",
            "exact_decision": (
                "The frozen single-density extension requires c_s^2=-1/2 "
                "and is rejected by the W3-54 health interval [0,1]."
            ),
            "accepted_upstream_law_falsified": False,
        },
        "candidate": {
            "new_field_count": 0,
            "new_metric_count": 0,
            "new_action_operator_count": 0,
            "new_source_count": 0,
            "density_reference_positive": True,
            "homogeneous_map_role": "INHERITED_ONLY_ON_FROZEN_HOMOGENEOUS_BRANCH",
            "local_stationary_extension_role": "NEWLY_TESTED_AND_REJECTED",
        },
        "stationary_branch": {
            "timelike_killing_field": "xi",
            "total_lapse": "calN=sqrt(-xi^2)",
            "asymptotic_normalization": "calN_infinity=1",
            "flow_alignment": "u_C=xi/calN",
            "radial_phase_flux": 0,
            "first_integral": "mu(n_C)*calN=mu_infinity",
            "mu_definition": "rho_C_prime(n_C)/c0",
            "sound_speed_definition": (
                "c_s^2=dln(mu)/dln(n_C)=n_C*rho_C_second/rho_C_prime"
            ),
            "health_interval": "[0,1]",
        },
        "exact_algebra": symbolic,
        "controls": {
            "inverse_density": {
                "map": "p_inv^2=n_infinity/n_C",
                "required_cs2": symbolic["inverse_required_cs2"],
                "static_health": "PASS_AT_CS2_ONE_HALF",
                "homogeneous_dictionary": "REVERSES_FROZEN_W3_50_SLOPE",
            },
            "chemical_potential": {
                "map": "p_mu=mu_infinity/mu",
                "stationary_result": "p_mu=calN",
                "role": "PASSIVE_READOUT_ONLY_WITHOUT_NEW_ACTION",
                "homogeneous_compatibility_required_cs2": symbolic[
                    "chemical_homogeneous_required_cs2"
                ],
            },
            "zero_sound_speed": {
                "regular_linear_response_possible": symbolic[
                    "zero_cs2_regular_linear_response_possible"
                ],
                "decision": "REJECTED_FOR_NONCONSTANT_LAPSE",
            },
        },
        "dependencies": {
            "records": dependency_records,
            "all_exact": dependency_exact,
        },
        "upstream_regression": {
            **upstream,
            "all_exact": upstream_exact,
        },
        "immutable_controls": {
            **immutable_records,
            "all_exact": immutable_exact,
        },
        "preregistration": prereg,
        "production_checks": production_checks,
        "mutation_controls": mutations,
        "package": {
            **package,
            "actual_files_after_successful_write": sorted(EXPECTED_PACKAGE_FILES),
        },
        "closure_flags": flags,
        "gate_registry": {
            "G0_GOAL": flags["g0_goal_pass"],
            "G1_CONVENTIONS": flags["g1_conventions_pass"],
            "G2_CORE_ALGEBRA": flags["g2_core_algebra_pass"],
            "G3_STRUCTURE": flags["g3_structure_pass"],
            "G4_INDEPENDENT_CHECK": flags["g4_independent_check_pass"],
            "G5_LIMITS_REGRESSION": flags["g5_limits_regression_pass"],
            "G6_PHYSICAL_MATCH": flags["g6_physical_match_pass"],
            "G7_OBSERVATION": "N/A_EXACT",
            "G8_EXPORT": "N/A_EXACT",
        },
        "physical_decision": {
            "collective_density_as_universal_local_p": "HARD_ROLE_VETO",
            "reason": (
                "Stationary Bernoulli balance and p_n^2=n_C/n_infinity "
                "require the unhealthy value c_s^2=-1/2."
            ),
            "phase_sector_original_roles": "UNCHANGED",
            "inverse_density_control": "NEW_MODEL_VERSION_REQUIRED",
            "chemical_potential_readout": "PASSIVE_ONLY",
            "global_strong_field_solve_opened": False,
            "next_exact_input": (
                "A covariantly derived branch-sensitive constitutive bridge "
                "using additional state information, or a different healthy "
                "carrier, with action/source, 1PN, and mode-health closure."
            ),
        },
        "scientific_boundary": {
            "whole_phase_sector_rejected": False,
            "homogeneous_w3_50_law_rejected": False,
            "all_local_carriers_excluded": False,
            "exact_full_strong_field_coframe_represented_by_lapse": False,
            "foundation_response_derived": False,
            "black_hole_solution_derived": False,
            "singularity_resolution_completed": False,
            "new_observation_tested": False,
        },
        "stop_rule": {
            "candidate_decision_complete": artifact_valid,
            "actual_global_solve_opened": False,
            "alternative_action_search_opened": False,
            "manuscript_or_canon_changed": False,
        },
        "validation": validation,
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "source_sha256": sha256_file(SOURCE_PATH),
            "preregistration_sha256": sha256_file(PREREG_PATH),
            "python": sys.version,
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "network_used_by_verifier": False,
            "archived_theory_used": False,
        },
    }

    write_json_atomic(RESULT_PATH, payload)
    print(json.dumps({
        "artifact_valid": artifact_valid,
        "candidate_admissible": flags["candidate_admissible"],
        "result": str(RESULT_PATH),
        "status": status,
    }, indent=2, sort_keys=True))
    return 0 if artifact_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
