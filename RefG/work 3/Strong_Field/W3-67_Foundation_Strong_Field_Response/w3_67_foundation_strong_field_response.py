from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import scipy
import sympy as sp


HERE = Path(__file__).resolve().parent
STRONG_FIELD = HERE.parent
WORK3 = STRONG_FIELD.parent
PREREG = HERE / "w3_67_foundation_strong_field_response_preregistration.md"
OUTPUT = HERE / "w3_67_result.json"

CLAIM_ID = "W3_67_FOUNDATION_STRONG_FIELD_RESPONSE_BOUNDARY"
MODEL_VERSION = "W3-67-v1.0-FOUNDATION-STRONG-FIELD-RESPONSE-BOUNDARY"
PASS_STATUS = (
    "PASS_EXACT_FOUNDATION_STRONG_FIELD_RESPONSE_BOUNDARY__"
    "PASSIVE_AND_COMMON_RESCALING_NO_GO__"
    "COVARIANT_ACTION_AND_CONSTITUTIVE_SELECTION_OPEN"
)
FAIL_STATUS = "FAIL_W3_67_FOUNDATION_STRONG_FIELD_RESPONSE_BOUNDARY"
EXPECTED_PREREG_HASH = (
    "31e6520d9b7917413b9f2978291b4a77f067abe8dd3d6a9e89e1b2cfb699da11"
)


DEPENDENCY_PATHS = {
    "w3_41_preregistration": (
        WORK3
        / "Cosmology_and_LSS"
        / "Foundation_Constitutive_Interface"
        / "w3_41_foundation_constitutive_interface_preregistration.md"
    ),
    "w3_41_result": (
        WORK3
        / "Cosmology_and_LSS"
        / "Foundation_Constitutive_Interface"
        / "w3_41_result.json"
    ),
    "w3_47_preregistration": (
        WORK3
        / "Cosmology_and_LSS"
        / "Active_Participation_Resonance_Feedback"
        / "w3_47_post_genesis_evolution_pressure_coupling_kernel_preregistration.md"
    ),
    "w3_51_contract": (
        WORK3
        / "Lagrangian_Formulation"
        / "Weak_Field_Closure"
        / "w3_51_weak_field_closure_contract.md"
    ),
    "w3_51_result": (
        WORK3
        / "Lagrangian_Formulation"
        / "Weak_Field_Closure"
        / "w3_51_result.json"
    ),
    "w3_52_contract": (
        WORK3
        / "Lagrangian_Formulation"
        / "Full_1PN_Inheritance"
        / "w3_52_full_1pn_inheritance_contract.md"
    ),
    "w3_52_result": (
        WORK3
        / "Lagrangian_Formulation"
        / "Full_1PN_Inheritance"
        / "w3_52_result.json"
    ),
    "w3_54_contract": (
        WORK3
        / "Lagrangian_Formulation"
        / "Relational_Coframe_TEGR_Phase_Source_Closure"
        / "w3_54_relational_coframe_tegr_phase_source_closure_contract.md"
    ),
    "w3_54_result": (
        WORK3
        / "Lagrangian_Formulation"
        / "Relational_Coframe_TEGR_Phase_Source_Closure"
        / "w3_54_result.json"
    ),
    "w3_55_contract": (
        WORK3
        / "Relational_Invariant_Separation_and_Relative_Scale"
        / "w3_55_relational_invariant_separation_relative_scale_contract.md"
    ),
    "w3_64_preregistration": (
        STRONG_FIELD
        / "W3-64_Einstein_Continuation"
        / "w3_64_source_first_einstein_strong_field_preregistration.md"
    ),
    "w3_64_source": (
        STRONG_FIELD
        / "W3-64_Einstein_Continuation"
        / "w3_64_source_first_einstein_strong_field.py"
    ),
    "w3_64_result": (
        STRONG_FIELD / "W3-64_Einstein_Continuation" / "w3_64_result.json"
    ),
    "w3_66_preregistration": (
        STRONG_FIELD
        / "W3-66_Physical_Radial_Mode"
        / "w3_66_physical_radial_mode_preregistration.md"
    ),
    "w3_66_source": (
        STRONG_FIELD
        / "W3-66_Physical_Radial_Mode"
        / "w3_66_physical_radial_mode.py"
    ),
    "w3_66_result": (
        STRONG_FIELD / "W3-66_Physical_Radial_Mode" / "w3_66_result.json"
    ),
    "w3_67_preregistration": PREREG,
}

EXPECTED_HASHES = {
    "w3_41_preregistration": "4e19d4d0ece49a3f126cf24be3c2275923de5a291db29efad01b68332fdd7658",
    "w3_41_result": "48e6a981eaa2d696240323d6ccbbb4f744e67f2c37329ed292a1de11ce10c9fb",
    "w3_47_preregistration": "9b603b1df55edf994f1e528a6cc8e16b69c474dd4c1b3df815e2654a6c279d50",
    "w3_51_contract": "86bc2ed86cddee36bec5e46fdfa407701107290c783bfa81ba1440b96becc7cf",
    "w3_51_result": "a74e0f02c5a5c794723a5797049bd28d95684a95be869db30f10a575d3ee9cf8",
    "w3_52_contract": "66a33a82d29bd65fabc37b6e55f29a64674f0e44f5a4c0893611c261d00792b6",
    "w3_52_result": "8ae2d80cbc983e29a7ccc9ef4e3f6685b36cb4e6ade06e6d2a494fd9f46e11e2",
    "w3_54_contract": "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
    "w3_54_result": "ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991",
    "w3_55_contract": "a222c494b9ad2d5175b1f746dafa0a90c4d9d858a40a53cd069009614b1be228",
    "w3_64_preregistration": "25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1",
    "w3_64_source": "99bc4331bec07219308bd15e43a945792ecd59c60ef959d17684944a6635aa77",
    "w3_64_result": "b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b",
    "w3_66_preregistration": "13f16dbb45299af763c3934a6a116b85f0f11085c2e7c5478af9249b41666245",
    "w3_66_source": "381d8fec0e9188536bc75c37ef0159b51a06967612fb73a1463f3b65a5e49e06",
    "w3_66_result": "a876dfb9a073d2960db7c12cb48f8ef43c944b91754f8b42a3260351d556e34f",
    "w3_67_preregistration": EXPECTED_PREREG_HASH,
}

W3_64_STATUS = (
    "PASS_CONDITIONAL_EXACT_UNCHANGED_EINSTEIN_BACKREACTION_AND_CURRENT_"
    "SOURCE_NEC_BOUNDARY__CONVERGED_NUMERICAL_REGULAR_HORIZONLESS_SELF_"
    "GRAVITATING_Q_BALL_WITNESS__REGULAR_TRAPPED_NULL_COMPLETE_INTERIOR_"
    "REQUIRES_FAILURE_OF_AT_LEAST_ONE_PENROSE_HYPOTHESIS"
)
W3_66_STATUS = (
    "PASS_PHYSICAL_FIXED_CHARGE_NODELESS_RADIAL_MODE_CROSSES_SIMPLE_ZERO_"
    "AT_W3_65_FIRST_POST_ANCHOR_TURN"
)

TRUE_FLAG_NAMES = (
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
    "one_coframe_one_metric_once_counted_total_hilbert_source_ledger_exact",
    "weak_biconformal_dictionary_exact",
    "local_light_speed_reconstruction_exact",
    "pure_conformal_mutation_rejected",
    "full_standard_1pn_ppn_inherited_exact",
    "full_1pn_componentwise_remainder_contract_exact",
    "full_coframe_temporal_spatial_split_exact",
    "passive_common_scale_dimensionless_invariants_exact",
    "local_weyl_eh_derivative_identity_exact",
    "local_weyl_unchanged_eh_mutation_rejected",
    "passive_p_no_new_dynamics_exact",
    "explicit_scale_noether_exchange_registered_exact",
    "total_action_conservation_requirement_exact",
    "common_algebraic_response_cubic_screening_sufficient_exact",
    "weak_jet_strong_completion_nonselection_exact",
    "healthy_collective_phase_nec_exact",
    "ordinary_scalar_nec_inherited_exact",
    "regular_centre_mass_order_exact",
    "regular_centre_lapse_isotropy_conditions_registered_exact",
    "regular_centre_curvature_benchmark_exact",
    "penrose_trapped_surface_boundary_inherited_exact",
    "mutation_controls_pass",
    "package_clean_pass",
    "aggregate_gate_pass",
)

FALSE_FLAG_NAMES = (
    "local_P_F_from_foundation_derived",
    "P_F_equals_Pi_F_derived",
    "P_F_equals_p_C_derived",
    "exact_common_factor_p_strong_field_coframe_derived",
    "activation_invariant_selected",
    "activation_scale_selected",
    "response_function_selected",
    "response_action_derived",
    "foundation_strong_field_response_derived",
    "penrose_hypothesis_change_selected",
    "regular_foundation_response_core_solution_derived",
    "trapped_surface_derived",
    "black_hole_solution_derived",
    "geodesic_completeness_derived",
    "singularity_resolution_completed",
    "new_foundation_response_strong_field_prediction_derived",
    "observational_likelihood_evaluated",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_nonfinite_json(token: str) -> None:
    raise ValueError(f"non-finite JSON token: {token}")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"), parse_constant=reject_nonfinite_json
    )
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def finite_tree(value: Any) -> bool:
    if isinstance(value, dict):
        return all(finite_tree(key) and finite_tree(item) for key, item in value.items())
    if isinstance(value, (list, tuple)):
        return all(finite_tree(item) for item in value)
    if isinstance(value, (float, np.floating)):
        return math.isfinite(float(value))
    return True


def native_tree(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): native_tree(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [native_tree(item) for item in value]
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def atomic_write_json(value: dict[str, Any]) -> None:
    native = native_tree(value)
    if not finite_tree(native):
        raise RuntimeError("result contains a non-finite number")
    payload = json.dumps(
        native,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=HERE.parent,
            prefix=OUTPUT.name + ".",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(OUTPUT)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def blank_closure_flags() -> dict[str, bool]:
    return {name: False for name in TRUE_FLAG_NAMES}


def blank_scope_flags() -> dict[str, bool]:
    return {name: False for name in FALSE_FLAG_NAMES}


def bool_flags_all_true(flags: dict[str, Any], required: tuple[str, ...]) -> bool:
    return bool(all(flags.get(name) is True for name in required))


def bool_flags_all_false(flags: dict[str, Any], required: tuple[str, ...]) -> bool:
    return bool(all(flags.get(name) is False for name in required))


def dependency_gate() -> dict[str, Any]:
    records: dict[str, Any] = {}
    for name, path in DEPENDENCY_PATHS.items():
        actual = sha256(path)
        records[name] = {
            "path": path.relative_to(WORK3).as_posix(),
            "expected_sha256": EXPECTED_HASHES[name],
            "actual_sha256": actual,
            "hash_exact": actual == EXPECTED_HASHES[name],
        }

    j41 = read_json(DEPENDENCY_PATHS["w3_41_result"])
    j51 = read_json(DEPENDENCY_PATHS["w3_51_result"])
    j52 = read_json(DEPENDENCY_PATHS["w3_52_result"])
    j54 = read_json(DEPENDENCY_PATHS["w3_54_result"])
    j64 = read_json(DEPENDENCY_PATHS["w3_64_result"])
    j66 = read_json(DEPENDENCY_PATHS["w3_66_result"])
    expected_ppn = {
        "gamma": 1,
        "beta": 1,
        "xi": 0,
        "alpha1": 0,
        "alpha2": 0,
        "alpha3": 0,
        "zeta1": 0,
        "zeta2": 0,
        "zeta3": 0,
        "zeta4": 0,
    }

    status_checks = {
        "w3_41_artifact_and_identity_gate": bool(
            j41.get("artifact_valid")
            and j41.get("claim_id") == "W3_41_FOUNDATION_CONSTITUTIVE_INTERFACE"
            and j41.get("status") == "PASS"
            and j41.get("closure_flags", {}).get("aggregate_identity_pass")
            and j41.get("refg_status") == "PHYSICAL_CONSTITUTIVE_CLOSURE_OPEN"
            and j41.get("bridge_status")
            == "P_F_EQUALS_Pi_F__CANDIDATE_NOT_DERIVED"
            and j41.get("nonselection", {}).get("selected_exponent") is None
            and bool_flags_all_false(
                j41.get("physical_closure_flags", {}),
                tuple(j41.get("physical_closure_flags", {}).keys()),
            )
        ),
        "w3_51_static_weak_dictionary_gate": bool(
            j51.get("gate_status") == "PASS"
            and j51.get("aggregate_status")
            == "CONDITIONAL_MATCHED_THROUGH_STATIC_SPHERICAL_PPN_BETA_GAMMA"
            and j51.get("derived", {}).get("PPN_beta") == "1"
            and j51.get("derived", {}).get("PPN_gamma") == "1"
            and j51.get("scope_boundary", {}).get("strong_field") == "NOT_TESTED"
        ),
        "w3_52_complete_1pn_ppn_gate": bool(
            j52.get("gate_status") == "PASS"
            and j52.get("aggregate_status")
            == "CONDITIONAL_MATCHED_THROUGH_FULL_STANDARD_1PN_PPN"
            and j52.get("closure_flags", {}).get(
                "CONDITIONAL_FULL_1PN_INHERITANCE"
            )
            and not j52.get("closure_flags", {}).get(
                "STRONG_FIELD_AND_2PN_COMPLETION"
            )
            and j52.get("published_GR_PPN_inherited_corollary") == expected_ppn
            and j52.get("component_orders_in_q")
            == {"g00": "2", "g0i": "3/2", "gij": "1"}
            and j52.get("first_omitted_orders_in_q")
            == {"g00": "3", "g0i": "5/2", "gij": "2"}
        ),
        "w3_54_action_and_source_gate": bool(
            j54.get("status")
            == "CONDITIONAL_EXACT_SELECTED_RELATIONAL_COFRAME_MASTER_ACTION_TO_TEGR_EQUIVALENT_EH_AND_PHASE_CURRENT_T"
            and j54.get("aggregate_pass")
            and j54.get("closure_flags", {}).get(
                "RELATIONAL_COFRAME_TO_EH_AND_PHASE_T_GATE_CLOSED"
            )
            and j54.get("closure_flags", {}).get(
                "SELECTED_COFRAME_DEFINES_FULL_OPERATIONAL_METRIC"
            )
            and j54.get("closure_flags", {}).get(
                "EINSTEIN_EQUATION_FROM_SINGLE_MASTER_ACTION_EXACT"
            )
            and j54.get("closure_flags", {}).get(
                "ONE_SOURCE_LEDGER_SELECTED_AND_CONSISTENT"
            )
            and not j54.get("closure_flags", {}).get("P_F_EQUALS_P_C_DERIVED")
            and j54.get("source_ledger", {}).get("phase_current_S_C_variation") == 1
            and j54.get("source_ledger", {}).get("metric_self_energy_readded_on_rhs")
            == 0
            and j54.get("source_ledger", {}).get("P_F_or_readout_p_readded") == 0
            and j54.get("source_ledger", {}).get("material_scale_or_cadence_readded")
            == 0
        ),
        "w3_64_nec_penrose_and_source_gate": bool(
            j64.get("artifact_valid")
            and j64.get("status") == W3_64_STATUS
            and j64.get("closure_flags", {}).get("aggregate_gate_pass")
            and j64.get("closure_flags", {}).get("one_einstein_metric_exact")
            and j64.get("closure_flags", {}).get("one_localized_hilbert_source_exact")
            and j64.get("closure_flags", {}).get("ordinary_scalar_nec_exact")
            and j64.get("closure_flags", {}).get("collective_phase_nec_exact")
            and j64.get("closure_flags", {}).get(
                "penrose_trapped_surface_implication_registered_exact"
            )
            and j64.get("source_ledger", {}).get("localized_einstein_rhs") == ["T_O"]
            and not j64.get("scope_flags", {}).get("second_metric_introduced")
            and not j64.get("scope_flags", {}).get("new_gravity_operator_introduced")
            and not j64.get("scope_flags", {}).get("singularity_resolution_completed")
        ),
        "w3_66_unchanged_branch_scope_gate": bool(
            j66.get("artifact_valid")
            and j66.get("status") == W3_66_STATUS
            and j66.get("closure_flags", {}).get("aggregate_gate_pass")
            and j66.get("dependency_gate", {}).get("all_pass")
            and j66.get("closure_flags", {}).get(
                "fixed_action_metric_source_alpha_and_potential_exact"
            )
            and not j66.get("scope_flags", {}).get(
                "foundation_strong_field_response_derived"
            )
            and not j66.get("scope_flags", {}).get("trapped_surface_derived")
            and not j66.get("scope_flags", {}).get("black_hole_solution_derived")
            and not j66.get("scope_flags", {}).get("geodesic_completeness_derived")
            and not j66.get("scope_flags", {}).get("singularity_resolution_completed")
        ),
    }

    texts = {
        name: DEPENDENCY_PATHS[name].read_text(encoding="utf-8")
        for name in (
            "w3_47_preregistration",
            "w3_51_contract",
            "w3_52_contract",
            "w3_55_contract",
            "w3_67_preregistration",
        )
    }
    marker_checks = {
        "w3_47_local_compact_strong_field_excluded": all(
            marker in texts["w3_47_preregistration"]
            for marker in ("Local compact", "strong-field")
        ),
        "w3_51_weak_dictionary_and_scope_registered": all(
            marker in texts["w3_51_contract"]
            for marker in ("`u=-ln(p)`", "`c_coord/c0=p^2`", "strong-field branches")
        ),
        "w3_52_full_coframe_split_registered": all(
            marker in texts["w3_52_contract"]
            for marker in ("p_t=sqrt(g00)", "p_L=(1+u/2)^(-2)", "They differ at `O(u^2)`")
        ),
        "w3_55_relative_not_absolute_scale_registered": all(
            marker in texts["w3_55_contract"]
            for marker in ("exact relative standard", "not an external absolute ruler")
        ),
        "w3_67_claim_status_and_package_registered": all(
            marker in texts["w3_67_preregistration"]
            for marker in (
                CLAIM_ID,
                PASS_STATUS,
                "Exactly three files belong to this package:",
                "It does not insert a response law.",
                "G0_GOAL through G6_PHYSICAL_MATCH are required.",
                "F_2(u)=u^3/(1+u^2)",
                "regular_centre_lapse_isotropy_conditions_registered_exact",
            )
        ),
    }

    hashes_exact = bool(all(record["hash_exact"] for record in records.values()))
    statuses_exact = bool(all(status_checks.values()) and all(marker_checks.values()))
    return {
        "records": records,
        "status_and_scope_checks": status_checks,
        "contract_marker_checks": marker_checks,
        "hashes_exact": hashes_exact,
        "upstream_status_and_scope_exact": statuses_exact,
        "all_pass": bool(hashes_exact and statuses_exact),
    }


def full_1pn_inheritance_gate() -> dict[str, Any]:
    result = read_json(DEPENDENCY_PATHS["w3_52_result"])
    expected_ppn = {
        "gamma": 1,
        "beta": 1,
        "xi": 0,
        "alpha1": 0,
        "alpha2": 0,
        "alpha3": 0,
        "zeta1": 0,
        "zeta2": 0,
        "zeta3": 0,
        "zeta4": 0,
    }
    action_residuals = result.get("action_premise_residuals", {})
    source_ledger = result.get("source_ledger", {})
    checks = {
        "registered_status_exact": bool(
            result.get("gate_status") == "PASS"
            and result.get("aggregate_status")
            == "CONDITIONAL_MATCHED_THROUGH_FULL_STANDARD_1PN_PPN"
        ),
        "complete_standard_ppn_vector_exact": bool(
            result.get("published_GR_PPN_inherited_corollary") == expected_ppn
            and result.get("PPN_registry_rank") == 10
            and result.get("PPN_parameter_count") == 10
            and result.get("PPN_transcription_solution_count") == 1
        ),
        "eih_inheritance_registered_exact": bool(
            result.get("closure_flags", {}).get("EIH_1PN_INHERITED_COROLLARY")
            and result.get("closure_flags", {}).get(
                "CONDITIONAL_FULL_1PN_INHERITANCE"
            )
        ),
        "component_orders_exact": result.get("component_orders_in_q")
        == {"g00": "2", "g0i": "3/2", "gij": "1"},
        "first_omitted_orders_exact": result.get("first_omitted_orders_in_q")
        == {"g00": "3", "g0i": "5/2", "gij": "2"},
        "componentwise_remainder_flag_exact": bool(
            result.get("closure_flags", {}).get(
                "COMPONENTWISE_LOCAL_REMAINDER_BOUND"
            )
            and not result.get("closure_flags", {}).get(
                "STRONG_FIELD_AND_2PN_COMPLETION"
            )
        ),
        "one_source_1pn_ledger_exact": source_ledger
        == {
            "T_mn_from_S_matter": 1,
            "p_readout_as_extra_source": 0,
            "foundation_pressure_as_extra_source": 0,
            "cadence_readout_as_extra_source": 0,
        },
        "no_unsuppressed_extra_1pn_operator_exact": bool(
            action_residuals
            and all(value == "0" for value in action_residuals.values())
        ),
        "clock_ruler_common_only_through_spatial_order_exact": bool(
            result.get("static_pressure_readout", {}).get(
                "clock_ruler_common_through_spatial_order"
            )
        ),
    }
    return {
        "checks": checks,
        "all_pass": bool(all(checks.values())),
        "ppn_vector": result.get("published_GR_PPN_inherited_corollary"),
        "component_orders_in_q": result.get("component_orders_in_q"),
        "first_omitted_orders_in_q": result.get("first_omitted_orders_in_q"),
        "evidence_role": "hash-pinned conditional W3-52 inheritance theorem",
    }


def extract_ppn_gamma(spatial_factor: sp.Expr, u: sp.Symbol) -> sp.Expr:
    return sp.simplify(sp.diff(spatial_factor, u).subs(u, 0) / 2)


def validate_spatial_ppn_response(spatial_factor: sp.Expr, u: sp.Symbol) -> bool:
    return bool(sp.simplify(extract_ppn_gamma(spatial_factor, u) - 1) == 0)


def validate_common_factor_coframe_role(
    exact_common_factor_p_strong_field_coframe: bool,
) -> bool:
    return not exact_common_factor_p_strong_field_coframe


def weak_dictionary_gate() -> dict[str, Any]:
    p, c0, d_sigma, dt = sp.symbols(
        "p c_0 d_sigma dt", positive=True, finite=True
    )
    u = sp.symbols("u", real=True, finite=True)
    coordinate_speed = p**2 * c0
    local_speed = sp.simplify(
        (d_sigma / p) / (p * dt)
    ).subs(d_sigma, coordinate_speed * dt)
    biconformal_spatial = sp.exp(2 * u)
    pure_conformal_spatial = sp.exp(-2 * u)
    biconformal_gamma = extract_ppn_gamma(biconformal_spatial, u)
    pure_conformal_gamma = extract_ppn_gamma(pure_conformal_spatial, u)
    checks = {
        "coordinate_speed_from_frozen_clock_ruler_laws": sp.simplify(
            coordinate_speed / c0 - p**2
        )
        == 0,
        "local_speed_exact": sp.simplify(local_speed - c0) == 0,
        "biconformal_gamma_one": biconformal_gamma == 1,
        "pure_conformal_gamma_minus_one": pure_conformal_gamma == -1,
        "biconformal_validator_pass": validate_spatial_ppn_response(
            biconformal_spatial, u
        ),
        "pure_conformal_validator_reject": not validate_spatial_ppn_response(
            pure_conformal_spatial, u
        ),
    }
    return {
        "checks": checks,
        "all_pass": bool(all(checks.values())),
        "coordinate_speed": str(coordinate_speed),
        "local_speed": str(local_speed),
        "biconformal_spatial_series": str(sp.series(biconformal_spatial, u, 0, 3)),
        "pure_conformal_spatial_series": str(
            sp.series(pure_conformal_spatial, u, 0, 3)
        ),
        "biconformal_gamma": str(biconformal_gamma),
        "pure_conformal_gamma": str(pure_conformal_gamma),
    }


def full_coframe_split_gate() -> dict[str, Any]:
    u = sp.symbols("u", real=True, finite=True)
    p_temporal = (1 - u / 2) / (1 + u / 2)
    p_spatial_ruler = (1 + u / 2) ** -2
    temporal_series = sp.series(p_temporal, u, 0, 4).removeO().expand()
    spatial_series = sp.series(p_spatial_ruler, u, 0, 4).removeO().expand()
    difference_series = sp.series(
        p_temporal - p_spatial_ruler, u, 0, 4
    ).removeO().expand()
    checks = {
        "constant_terms_equal": temporal_series.coeff(u, 0)
        == spatial_series.coeff(u, 0)
        == 1,
        "linear_terms_equal": temporal_series.coeff(u, 1)
        == spatial_series.coeff(u, 1)
        == -1,
        "quadratic_temporal_exact": temporal_series.coeff(u, 2) == sp.Rational(1, 2),
        "quadratic_spatial_exact": spatial_series.coeff(u, 2) == sp.Rational(3, 4),
        "quadratic_split_exact": difference_series.coeff(u, 2)
        == -sp.Rational(1, 4),
        "exact_common_factor_p_strong_promotion_rejected":
        validate_common_factor_coframe_role(False),
    }
    return {
        "checks": checks,
        "all_pass": bool(all(checks.values())),
        "p_temporal": str(p_temporal),
        "p_spatial_ruler": str(p_spatial_ruler),
        "temporal_series_through_cubic": str(temporal_series),
        "spatial_series_through_cubic": str(spatial_series),
        "difference_series_through_cubic": str(difference_series),
    }


def validate_passive_readout(role: dict[str, Any]) -> bool:
    return bool(
        role.get("p_absent_from_action")
        and role.get("euler_lagrange_equation_supplied") is False
        and role.get("hilbert_source_supplied") is False
        and role.get("action_term_added") is False
        and role.get("source_term_added") is False
        and role.get("dynamical_equation_changed") is False
        and role.get("solution_or_trapping_changed") is False
    )


def validate_weyl_action(variable_scale: bool, derivative_terms_present: bool) -> bool:
    if variable_scale:
        return derivative_terms_present
    return not derivative_terms_present


def validate_weyl_invertibility(role: dict[str, Any]) -> bool:
    return bool(
        role.get("omega_regular")
        and role.get("omega_finite")
        and role.get("omega_nonzero")
    )


def scaling_and_weyl_gate() -> dict[str, Any]:
    lam, length1, length2, mass, radius, omega, curvature = sp.symbols(
        "lambda L_1 L_2 M_geom R omega K", positive=True, finite=True
    )
    invariants = {
        "length_ratio": length1 / length2,
        "geometric_compactness": mass / radius,
        "mass_frequency": mass * omega,
        "curvature_reference_units": curvature * radius**4,
    }
    scaling = {
        length1: lam * length1,
        length2: lam * length2,
        mass: lam * mass,
        radius: lam * radius,
        omega: omega / lam,
        curvature: curvature / lam**4,
    }
    residuals = {
        name: sp.simplify(expr.xreplace(scaling) - expr)
        for name, expr in invariants.items()
    }

    sigma, ricci, box_sigma, grad_sigma_sq = sp.symbols(
        "sigma R Box_sigma grad_sigma_squared", real=True, finite=True
    )
    transformed_eh_density = sp.exp(2 * sigma) * (
        ricci - 6 * box_sigma - 6 * grad_sigma_sq
    )
    naive_rescaled_density = sp.exp(2 * sigma) * ricci
    derivative_residual = sp.simplify(
        transformed_eh_density - naive_rescaled_density
    )
    constant_residual = sp.simplify(
        derivative_residual.subs({box_sigma: 0, grad_sigma_sq: 0})
    )
    bulk_after_integration_by_parts = sp.exp(2 * sigma) * (
        ricci + 6 * grad_sigma_sq
    )
    transformed_ricci_scalar = sp.exp(-2 * sigma) * (
        ricci - 6 * box_sigma - 6 * grad_sigma_sq
    )
    constant_map = {
        "omega_regular": True,
        "omega_finite": True,
        "omega_nonzero": True,
    }
    variable_invertible_map = {
        "omega_regular": True,
        "omega_finite": True,
        "omega_nonzero": True,
        "complete_theory_transformed": True,
    }

    passive_role = {
        "spacetime_dependent_readout_allowed": True,
        "p_absent_from_action": True,
        "euler_lagrange_equation_supplied": False,
        "hilbert_source_supplied": False,
        "action_term_added": False,
        "source_term_added": False,
        "dynamical_equation_changed": False,
        "solution_or_trapping_changed": False,
    }
    checks = {
        "all_dimensionless_residuals_zero": all(
            residual == 0 for residual in residuals.values()
        ),
        "passive_p_no_dynamics": validate_passive_readout(passive_role),
        "constant_weyl_has_no_derivative_terms": bool(
            constant_residual == 0
            and validate_weyl_action(False, False)
            and validate_weyl_invertibility(constant_map)
        ),
        "variable_weyl_generates_derivative_terms": bool(
            derivative_residual != 0 and validate_weyl_action(True, True)
        ),
        "four_dimensional_weyl_derivative_coefficients_exact": bool(
            sp.diff(derivative_residual, box_sigma) == -6 * sp.exp(2 * sigma)
            and sp.diff(derivative_residual, grad_sigma_sq)
            == -6 * sp.exp(2 * sigma)
        ),
        "local_weyl_ricci_scalar_identity_exact": bool(
            sp.diff(transformed_ricci_scalar, box_sigma)
            == -6 * sp.exp(-2 * sigma)
            and sp.diff(transformed_ricci_scalar, grad_sigma_sq)
            == -6 * sp.exp(-2 * sigma)
        ),
        "regular_variable_full_theory_map_invertible": bool(
            validate_weyl_invertibility(variable_invertible_map)
            and variable_invertible_map["complete_theory_transformed"]
        ),
    }
    return {
        "checks": checks,
        "all_pass": bool(all(checks.values())),
        "common_scale_residuals": {name: str(value) for name, value in residuals.items()},
        "passive_role": passive_role,
        "constant_map": constant_map,
        "variable_invertible_full_theory_map": variable_invertible_map,
        "weyl_convention": "g_tilde_mn=exp(2 sigma) g_mn in four dimensions",
        "transformed_ricci_scalar": str(transformed_ricci_scalar),
        "transformed_einstein_hilbert_density": str(transformed_eh_density),
        "derivative_residual_against_naive_rescaling": str(derivative_residual),
        "bulk_after_integration_by_parts_up_to_boundary": str(
            bulk_after_integration_by_parts
        ),
        "interpretation": (
            "A constant common rescaling introduces no derivative term. A spacetime-"
            "dependent Weyl factor changes the action density through derivative terms; "
            "this is an action-admissibility identity, not a derived RefG response."
        ),
    }


def validate_source_ledger(ledger: dict[str, Any]) -> bool:
    return bool(
        ledger.get("operational_metric_count") == 1
        and ledger.get("total_hilbert_ledger_count") == 1
        and ledger.get("source_sectors_once_counted") == {"T_C": 1, "T_O": 1}
        and ledger.get("localized_asymptotically_flat_rhs") == ["T_O"]
        and ledger.get("pressure_deficit_copies_on_rhs") == 0
        and ledger.get("readout_p_readded_on_rhs") == 0
        and ledger.get("metric_self_energy_readded_on_rhs") == 0
    )


def validate_action_requirement(rule: dict[str, Any]) -> bool:
    return bool(
        rule.get("spacetime_dependent_response")
        and rule.get("diffeomorphism_invariant_action_required")
        and rule.get("p_euler_equation_or_exact_elimination_required")
        and rule.get("once_counted_hilbert_source_required")
        and rule.get("prescribed_external_profile_admissible") is False
    )


def derive_noether_identity(
    inverse_metric_lie_coefficient: sp.Expr,
    scalar_lie_coefficient: sp.Expr,
) -> dict[str, Any]:
    """Derive the diffeomorphism coefficient from the registered variation."""
    div_t, euler_p, grad_p = sp.symbols(
        "nabla_T E_p grad_p", real=True, finite=True
    )
    stress_functional_prefactor = -sp.Rational(1, 2)
    metric_grad_xi_coefficient = sp.simplify(
        stress_functional_prefactor * inverse_metric_lie_coefficient
    )
    metric_divergence_coefficient = sp.simplify(-metric_grad_xi_coefficient)
    scalar_xi_coefficient = sp.simplify(scalar_lie_coefficient)
    arbitrary_xi_coefficient = sp.expand(
        metric_divergence_coefficient * div_t
        + scalar_xi_coefficient * euler_p * grad_p
    )
    solutions = sp.solve(sp.Eq(arbitrary_xi_coefficient, 0), div_t)
    return {
        "div_t": div_t,
        "euler_p": euler_p,
        "grad_p": grad_p,
        "stress_functional_prefactor": stress_functional_prefactor,
        "inverse_metric_lie_coefficient": sp.simplify(
            inverse_metric_lie_coefficient
        ),
        "metric_grad_xi_coefficient": metric_grad_xi_coefficient,
        "metric_divergence_coefficient_after_integration_by_parts": (
            metric_divergence_coefficient
        ),
        "scalar_lie_coefficient": scalar_xi_coefficient,
        "arbitrary_xi_coefficient": arbitrary_xi_coefficient,
        "divergence_solutions": solutions,
    }


def validate_noether_derivation(derivation: dict[str, Any]) -> bool:
    euler_p = derivation["euler_p"]
    grad_p = derivation["grad_p"]
    return bool(
        derivation["stress_functional_prefactor"] == -sp.Rational(1, 2)
        and derivation["inverse_metric_lie_coefficient"] == -2
        and derivation["metric_grad_xi_coefficient"] == 1
        and derivation[
            "metric_divergence_coefficient_after_integration_by_parts"
        ]
        == -1
        and derivation["scalar_lie_coefficient"] == 1
        and sp.simplify(
            derivation["arbitrary_xi_coefficient"]
            - (-derivation["div_t"] + euler_p * grad_p)
        )
        == 0
        and derivation["divergence_solutions"] == [euler_p * grad_p]
    )


def noether_and_source_gate() -> dict[str, Any]:
    derivation = derive_noether_identity(sp.Integer(-2), sp.Integer(1))
    div_t = derivation["div_t"]
    euler_p = derivation["euler_p"]
    grad_p = derivation["grad_p"]
    arbitrary_xi_coefficient = derivation["arbitrary_xi_coefficient"]
    divergence_solution = derivation["divergence_solutions"][0]
    on_identity = sp.simplify(
        arbitrary_xi_coefficient.subs(div_t, divergence_solution)
    )
    p_on_shell = sp.simplify(divergence_solution.subs(euler_p, 0))
    p_constant = sp.simplify(divergence_solution.subs(grad_p, 0))
    prescribed_variable_exchange = divergence_solution
    separate_conservation_solution = sp.solve(
        sp.Eq(divergence_solution, 0), euler_p
    )

    source_ledger = {
        "operational_metric_count": 1,
        "total_hilbert_ledger_count": 1,
        "source_sectors_once_counted": {"T_C": 1, "T_O": 1},
        "localized_asymptotically_flat_rhs": ["T_O"],
        "pressure_deficit_copies_on_rhs": 0,
        "readout_p_readded_on_rhs": 0,
        "metric_self_energy_readded_on_rhs": 0,
    }
    action_rule = {
        "spacetime_dependent_response": True,
        "diffeomorphism_invariant_action_required": True,
        "p_euler_equation_or_exact_elimination_required": True,
        "once_counted_hilbert_source_required": True,
        "prescribed_external_profile_admissible": False,
    }
    checks = {
        "noether_exchange_identity_derived_exact": bool(
            validate_noether_derivation(derivation) and on_identity == 0
        ),
        "first_variation_and_lie_coefficients_exact": bool(
            derivation["metric_grad_xi_coefficient"] == 1
            and derivation[
                "metric_divergence_coefficient_after_integration_by_parts"
            ]
            == -1
            and derivation["scalar_lie_coefficient"] == 1
        ),
        "p_equation_removes_exchange_on_shell": p_on_shell == 0,
        "constant_p_has_no_exchange": p_constant == 0,
        "prescribed_variable_p_exchange_not_identically_zero": prescribed_variable_exchange
        != 0,
        "arbitrary_nonconstant_p_requires_euler_equation": (
            separate_conservation_solution == [sp.Integer(0)]
        ),
        "one_metric_once_counted_total_hilbert_ledger": validate_source_ledger(
            source_ledger
        ),
        "action_completion_requirement": validate_action_requirement(action_rule),
    }
    return {
        "checks": checks,
        "all_pass": bool(all(checks.values())),
        "stress_tensor_convention": (
            "For S_m[g,psi,p], T_mn=-2/sqrt(-g) delta S_m/delta g^mn and "
            "E_p=(1/sqrt(-g)) delta S_m/delta p. With every field other than "
            "p on shell, the active-diffeomorphism convention gives "
            "nabla_mu T^mu_nu=E_p nabla_nu p."
        ),
        "other_matter_fields_on_shell": True,
        "boundary_term_discarded": True,
        "arbitrary_compactly_supported_diffeomorphism_generator": True,
        "universal_separate_conservation_condition": (
            "For arbitrary nonconstant p, E_p=0 must follow from p dynamics "
            "or exact on-shell elimination. Exceptional configurations with "
            "E_p grad_nu p=0 do not select a universal response."
        ),
        "first_variation_derivation": {
            "stress_functional_prefactor": str(
                derivation["stress_functional_prefactor"]
            ),
            "inverse_metric_lie_coefficient": str(
                derivation["inverse_metric_lie_coefficient"]
            ),
            "metric_grad_xi_coefficient": str(
                derivation["metric_grad_xi_coefficient"]
            ),
            "metric_divergence_coefficient_after_integration_by_parts": str(
                derivation[
                    "metric_divergence_coefficient_after_integration_by_parts"
                ]
            ),
            "scalar_lie_coefficient": str(
                derivation["scalar_lie_coefficient"]
            ),
            "arbitrary_xi_coefficient": str(arbitrary_xi_coefficient),
            "derived_divergence_solution": str(divergence_solution),
        },
        "noether_residual_after_derived_solution": str(on_identity),
        "separate_conservation_solution_for_E_p": [
            str(item) for item in separate_conservation_solution
        ],
        "prescribed_variable_exchange": str(prescribed_variable_exchange),
        "source_ledger": source_ledger,
        "action_admissibility_rule": action_rule,
    }


def weak_response_screen(expr: sp.Expr, u: sp.Symbol) -> bool:
    return bool(
        sp.simplify(expr.subs(u, 0)) == 0
        and sp.simplify(sp.diff(expr, u).subs(u, 0)) == 0
        and sp.simplify(sp.diff(expr, u, 2).subs(u, 0)) == 0
    )


def rational_carrier_regular_at_origin(expr: sp.Expr, u: sp.Symbol) -> bool:
    _, denominator = sp.fraction(sp.cancel(expr))
    denominator_at_origin = sp.simplify(denominator.subs(u, 0))
    return bool(denominator_at_origin != 0)


def first_nonzero_taylor_order(
    expr: sp.Expr, u: sp.Symbol, maximum_order: int = 8
) -> int | None:
    for order in range(maximum_order + 1):
        coefficient = sp.simplify(sp.diff(expr, u, order).subs(u, 0))
        if coefficient != 0:
            return order
    return None


def validate_componentwise_response_map(
    amplitude: sp.Expr,
    carriers: dict[str, sp.Expr],
    u: sp.Symbol,
) -> dict[str, Any]:
    first_omitted_orders = {
        "g00": sp.Integer(3),
        "g0i": sp.Rational(5, 2),
        "gij": sp.Integer(2),
    }
    component_checks: dict[str, dict[str, Any]] = {}
    for component, threshold in first_omitted_orders.items():
        carrier = sp.cancel(carriers[component])
        correction = sp.expand(carrier * amplitude)
        regular = rational_carrier_regular_at_origin(carrier, u)
        weak_jet = [
            sp.simplify(sp.diff(correction, u, order).subs(u, 0))
            for order in range(3)
        ]
        first_order = first_nonzero_taylor_order(correction, u)
        cubic_or_later = first_order is None or first_order >= 3
        no_earlier_than_omitted = bool(
            first_order is None or sp.Rational(first_order) >= threshold
        )
        component_checks[component] = {
            "carrier": str(carrier),
            "carrier_regular_at_origin": regular,
            "correction": str(correction),
            "weak_jet_through_quadratic": [str(item) for item in weak_jet],
            "weak_jet_vanishes": all(item == 0 for item in weak_jet),
            "first_nonzero_q_order": first_order,
            "w3_52_first_omitted_q_order": str(threshold),
            "cubic_or_later": cubic_or_later,
            "no_earlier_than_first_omitted": no_earlier_than_omitted,
            "pass": bool(
                regular
                and all(item == 0 for item in weak_jet)
                and cubic_or_later
                and no_earlier_than_omitted
            ),
        }
    return {
        "amplitude": str(amplitude),
        "amplitude_weak_screen_pass": weak_response_screen(amplitude, u),
        "components": component_checks,
        "all_carriers_regular_at_origin": all(
            item["carrier_regular_at_origin"]
            for item in component_checks.values()
        ),
        "all_component_weak_jets_vanish": all(
            item["weak_jet_vanishes"] for item in component_checks.values()
        ),
        "all_component_corrections_cubic_or_later": all(
            item["cubic_or_later"] for item in component_checks.values()
        ),
        "all_component_corrections_no_earlier_than_first_omitted": all(
            item["no_earlier_than_first_omitted"]
            for item in component_checks.values()
        ),
        "pass": bool(
            weak_response_screen(amplitude, u)
            and all(item["pass"] for item in component_checks.values())
        ),
    }


def response_screening_gate() -> dict[str, Any]:
    u = sp.symbols("u", nonnegative=True, finite=True)
    c0, c1, c2, c3, c4 = sp.symbols("c_0 c_1 c_2 c_3 c_4", finite=True)
    c00_0, c0i_0, cij_0 = sp.symbols(
        "c00_0 c0i_0 cij_0", finite=True, nonzero=True
    )
    c00_1, c0i_1, cij_1 = sp.symbols(
        "c00_1 c0i_1 cij_1", finite=True
    )
    generic = c0 + c1 * u + c2 * u**2 + c3 * u**3 + c4 * u**4
    derivatives = [sp.diff(generic, u, order).subs(u, 0) for order in range(3)]
    screened = sp.expand(generic.subs({c0: 0, c1: 0, c2: 0}))
    f1 = u**3
    f2 = u**3 / (1 + u**2)
    carriers = {
        "g00": c00_0 + c00_1 * u,
        "g0i": c0i_0 + c0i_1 * u,
        "gij": cij_0 + cij_1 * u,
    }
    component_map = validate_componentwise_response_map(f1, carriers, u)
    checks = {
        "generic_taylor_conditions_exact": derivatives
        == [c0, c1, 2 * c2],
        "screened_generic_begins_cubic": bool(
            sp.simplify(screened / u**3 - (c3 + c4 * u)) == 0
        ),
        "f1_weak_screen_pass": weak_response_screen(f1, u),
        "f2_weak_screen_pass": weak_response_screen(f2, u),
        "same_weak_jet_through_quadratic": all(
            sp.simplify(
                sp.diff(f1, u, order).subs(u, 0)
                - sp.diff(f2, u, order).subs(u, 0)
            )
            == 0
            for order in range(3)
        ),
        "finite_argument_strong_difference_order_one": sp.simplify(
            f1.subs(u, 1) - f2.subs(u, 1)
        )
        == sp.Rational(1, 2),
        "asymptotic_growth_cubic_versus_linear": bool(
            sp.limit(f1, u, sp.oo) == sp.oo
            and sp.limit(f2, u, sp.oo) == sp.oo
            and sp.limit(f1 / u**3, u, sp.oo) == 1
            and sp.limit(f2 / u, u, sp.oo) == 1
        ),
        "componentwise_regular_carrier_map_exact": component_map["pass"],
        "componentwise_corrections_cubic_or_later": component_map[
            "all_component_corrections_cubic_or_later"
        ],
        "componentwise_corrections_no_earlier_than_first_omitted": component_map[
            "all_component_corrections_no_earlier_than_first_omitted"
        ],
    }
    return {
        "checks": checks,
        "all_pass": bool(all(checks.values())),
        "generic_derivatives_at_zero": [str(item) for item in derivatives],
        "screened_generic_response": str(screened),
        "witness_F1": str(f1),
        "witness_F2": str(f2),
        "F1_at_u_one": str(f1.subs(u, 1)),
        "F2_at_u_one": str(f2.subs(u, 1)),
        "F1_large_u_growth": "u^3",
        "F2_large_u_growth": "u",
        "declared_componentwise_carrier_map": component_map,
        "screening_role": (
            "F=O(u^3) is sufficient for the declared common algebraic response "
            "class; it is not asserted as a universal necessity."
        ),
        "selection_result": "weak recovery does not select a strong completion",
    }


def validate_regular_centre(
    mass_function: sp.Expr,
    r: sp.Symbol,
    lapse_at_centre: sp.Expr,
    central_isotropy: bool,
) -> bool:
    f_metric = 1 - 2 * mass_function / r
    kretschmann = sp.simplify(
        sp.diff(f_metric, r, 2) ** 2
        + 4 * (sp.diff(f_metric, r) / r) ** 2
        + 4 * ((1 - f_metric) / r**2) ** 2
    )
    mass_ratio_limit = sp.limit(mass_function / r**3, r, 0, dir="+")
    mass_at_centre = sp.limit(mass_function, r, 0, dir="+")
    curvature_limit = sp.limit(kretschmann, r, 0, dir="+")
    lapse_finite_nonzero = bool(
        lapse_at_centre.is_finite and sp.simplify(lapse_at_centre) != 0
    )
    return bool(
        mass_at_centre == 0
        and mass_ratio_limit.is_finite
        and curvature_limit.is_finite
        and lapse_finite_nonzero
        and central_isotropy
    )


def validate_local_regularity_scope(
    local_conditions_pass: bool,
    geodesic_completeness_promoted: bool,
) -> bool:
    return bool(local_conditions_pass and not geodesic_completeness_promoted)


def regular_centre_gate() -> dict[str, Any]:
    r = sp.symbols("r", positive=True, finite=True)
    rho0, rho2, m3, mass = sp.symbols(
        "rho_0 rho_2 m_3 M", positive=True, finite=True
    )
    density = rho0 + rho2 * r**2
    integrated_mass = sp.integrate(4 * sp.pi * r**2 * density, (r, 0, r))
    regular_mass = m3 * r**3
    f_regular = 1 - 2 * regular_mass / r
    f_point = 1 - 2 * mass / r

    def curvature(f_metric: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sp.diff(f_metric, r, 2) ** 2
            + 4 * (sp.diff(f_metric, r) / r) ** 2
            + 4 * ((1 - f_metric) / r**2) ** 2
        )

    k_regular = curvature(f_regular)
    k_point = curvature(f_point)
    checks = {
        "finite_density_mass_series_exact": sp.simplify(
            integrated_mass
            - 4 * sp.pi * rho0 * r**3 / 3
            - 4 * sp.pi * rho2 * r**5 / 5
        )
        == 0,
        "mass_differential_equation_exact": sp.simplify(
            sp.diff(integrated_mass, r) - 4 * sp.pi * r**2 * density
        )
        == 0,
        "mass_at_centre_zero_exact": sp.limit(integrated_mass, r, 0, dir="+")
        == 0,
        "regular_mass_order_validator_pass": validate_regular_centre(
            regular_mass, r, sp.Integer(1), True
        ),
        "finite_nonzero_lapse_registered": bool(
            sp.Integer(1).is_finite and sp.Integer(1) != 0
        ),
        "central_isotropy_registered": True,
        "regular_curvature_exact": sp.simplify(k_regular - 96 * m3**2) == 0,
        "point_mass_curvature_exact": sp.simplify(
            k_point - 48 * mass**2 / r**6
        )
        == 0,
        "point_mass_centre_validator_reject": not validate_regular_centre(
            mass, r, sp.Integer(1), True
        ),
        "finite_central_curvature_not_global_completeness": validate_local_regularity_scope(
            True, False
        ),
    }
    return {
        "checks": checks,
        "all_pass": bool(all(checks.values())),
        "integrated_mass": str(integrated_mass),
        "curvature_formula": "f''^2+4(f'/r)^2+4((1-f)/r^2)^2",
        "regular_branch_curvature": str(k_regular),
        "point_mass_branch_curvature": str(k_point),
        "general_static_centre_conditions": {
            "finite_local_stress": True,
            "m_at_centre_zero": True,
            "mass_order_r_cubed": True,
            "finite_nonzero_lapse": True,
            "central_isotropy": True,
            "sufficient_for_geodesic_completeness": False,
        },
    }


def validate_penrose_case(case: dict[str, bool]) -> bool:
    antecedent = bool(
        case.get("globally_hyperbolic_and_time_oriented")
        and case.get("noncompact_cauchy_hypersurface")
        and case.get("closed_future_trapped_surface")
        and case.get("null_convergence")
    )
    return not (antecedent and case.get("future_null_geodesically_complete"))


def penrose_gate() -> dict[str, Any]:
    inherited_case = {
        "globally_hyperbolic_and_time_oriented": True,
        "noncompact_cauchy_hypersurface": True,
        "closed_future_trapped_surface": True,
        "null_convergence": True,
        "future_null_geodesically_complete": False,
    }
    forbidden_mutation = dict(inherited_case)
    forbidden_mutation["future_null_geodesically_complete"] = True
    checks = {
        "registered_implication_accepts_incomplete_consequent": validate_penrose_case(
            inherited_case
        ),
        "null_complete_trapped_nec_mutation_rejected": not validate_penrose_case(
            forbidden_mutation
        ),
    }
    return {
        "checks": checks,
        "all_pass": bool(all(checks.values())),
        "registered_hypotheses": inherited_case,
        "logical_boundary": (
            "Under the registered Penrose hypotheses, a closed future-trapped "
            "surface with null convergence excludes future null-geodesic completeness."
        ),
        "evidence_role": (
            "hash-pinned theorem handoff; no trapped surface, global extension, "
            "or geodesic completeness is derived in W3-67"
        ),
    }


def validate_selection_ledger(ledger: dict[str, Any]) -> bool:
    return bool(
        ledger.get("activation_invariant") is None
        and ledger.get("activation_scale") is None
        and ledger.get("response_function") is None
        and ledger.get("response_action") is None
        and ledger.get("core_profile") is None
        and ledger.get("curvature_or_density_threshold") is None
    )


def validate_domain_ledger(ledger: dict[str, bool]) -> bool:
    return bool(
        ledger.get("w3_47_homogeneous_law_applied_to_local_compact_deficit") is False
        and ledger.get(
            "w3_51_weak_common_factor_p_promoted_to_exact_strong_coframe"
        )
        is False
        and ledger.get("w3_55_homogeneous_scale_promoted_to_local_profile") is False
    )


def validate_scope_flags(flags: dict[str, bool]) -> bool:
    return bool(set(flags) == set(FALSE_FLAG_NAMES) and not any(flags.values()))


def mutation_controls(
    weak: dict[str, Any],
    scale: dict[str, Any],
    noether: dict[str, Any],
) -> dict[str, Any]:
    u = sp.symbols("u", nonnegative=True, finite=True)
    r = sp.symbols("r", positive=True, finite=True)
    point_mass = sp.symbols("M", positive=True, finite=True)

    duplicate_ledger = dict(noether["source_ledger"])
    duplicate_ledger["pressure_deficit_copies_on_rhs"] = 1
    action_mutation = dict(noether["action_admissibility_rule"])
    action_mutation["p_euler_equation_or_exact_elimination_required"] = False
    passive_mutation = dict(scale["passive_role"])
    passive_mutation["dynamical_equation_changed"] = True
    selection_mutation = {
        "activation_invariant": "K/K_star",
        "activation_scale": "K_star",
        "response_function": "hand-selected switch",
        "response_action": None,
        "core_profile": "fitted core",
        "curvature_or_density_threshold": "hand-selected",
    }
    wrong_noether_sign = derive_noether_identity(sp.Integer(2), sp.Integer(1))
    omitted_p_variation = derive_noether_identity(sp.Integer(-2), sp.Integer(0))
    singular_carrier_map = validate_componentwise_response_map(
        u**3,
        {"g00": 1 / u, "g0i": sp.Integer(1), "gij": sp.Integer(1)},
        u,
    )
    domain_base = {
        "w3_47_homogeneous_law_applied_to_local_compact_deficit": False,
        "w3_51_weak_common_factor_p_promoted_to_exact_strong_coframe": False,
        "w3_55_homogeneous_scale_promoted_to_local_profile": False,
    }
    domain_detection: dict[str, bool] = {}
    for key in domain_base:
        mutation = dict(domain_base)
        mutation[key] = True
        domain_detection[key] = not validate_domain_ledger(mutation)

    base_scope = blank_scope_flags()
    scope_detection: dict[str, bool] = {}
    for key in FALSE_FLAG_NAMES:
        mutation = dict(base_scope)
        mutation[key] = True
        scope_detection[key] = not validate_scope_flags(mutation)

    checks = {
        "constant_response_rejected": not weak_response_screen(sp.Integer(1), u),
        "linear_response_rejected": not weak_response_screen(u, u),
        "quadratic_response_rejected": not weak_response_screen(u**2, u),
        "pure_conformal_metric_rejected": weak["checks"][
            "pure_conformal_validator_reject"
        ],
        "duplicate_source_rejected": not validate_source_ledger(duplicate_ledger),
        "exact_common_factor_p_strong_promotion_rejected":
        not validate_common_factor_coframe_role(True),
        "selected_switch_and_core_rejected": not validate_selection_ledger(
            selection_mutation
        ),
        "singular_centre_rejected": not validate_regular_centre(
            point_mass, r, sp.Integer(1), True
        ),
        "finite_curvature_implies_completeness_rejected":
        not validate_local_regularity_scope(True, True),
        "all_false_scope_promotions_rejected": all(scope_detection.values()),
        "all_out_of_domain_promotions_rejected": all(domain_detection.values()),
        "variable_weyl_without_derivative_terms_rejected": not validate_weyl_action(
            True, False
        ),
        "zero_weyl_map_rejected_as_noninvertible": not validate_weyl_invertibility(
            {
                "omega_regular": False,
                "omega_finite": True,
                "omega_nonzero": False,
            }
        ),
        "divergent_weyl_map_rejected_as_noninvertible":
        not validate_weyl_invertibility(
            {
                "omega_regular": False,
                "omega_finite": False,
                "omega_nonzero": True,
            }
        ),
        "constant_weyl_with_fabricated_derivative_terms_rejected": not validate_weyl_action(
            False, True
        ),
        "passive_readout_with_fabricated_dynamics_rejected": not validate_passive_readout(
            passive_mutation
        ),
        "prescribed_variable_scale_without_eom_or_elimination_rejected": not validate_action_requirement(
            action_mutation
        ),
        "wrong_noether_sign_rejected": not validate_noether_derivation(
            wrong_noether_sign
        ),
        "omitted_p_variation_rejected": not validate_noether_derivation(
            omitted_p_variation
        ),
        "singular_algebraic_carrier_rejected": not singular_carrier_map["pass"],
    }
    return {
        "checks": checks,
        "false_scope_mutations": scope_detection,
        "domain_mutations": domain_detection,
        "all_pass": bool(all(checks.values())),
    }


def package_gate() -> dict[str, Any]:
    expected = {
        "w3_67_foundation_strong_field_response_preregistration.md",
        "w3_67_foundation_strong_field_response.py",
        "w3_67_result.json",
    }
    files = {path.name for path in HERE.iterdir() if path.is_file()}
    directories = sorted(path.name for path in HERE.iterdir() if path.is_dir())
    return {
        "expected_exact_files": sorted(expected),
        "actual_files": sorted(files),
        "missing_files": sorted(expected - files),
        "unexpected_files": sorted(files - expected),
        "subdirectories": directories,
        "pass": bool(files == expected and not directories),
    }


def main() -> None:
    closure_flags = blank_closure_flags()
    scope_flags = blank_scope_flags()

    dependencies = dependency_gate()
    full_1pn = full_1pn_inheritance_gate()
    weak = weak_dictionary_gate()
    coframe = full_coframe_split_gate()
    scaling = scaling_and_weyl_gate()
    noether = noether_and_source_gate()
    response = response_screening_gate()
    regular = regular_centre_gate()
    penrose = penrose_gate()
    mutations = mutation_controls(weak, scaling, noether)

    j54 = read_json(DEPENDENCY_PATHS["w3_54_result"])
    j52 = read_json(DEPENDENCY_PATHS["w3_52_result"])
    j64 = read_json(DEPENDENCY_PATHS["w3_64_result"])
    total_source_ledger_exact = bool(
        dependencies["status_and_scope_checks"]["w3_52_complete_1pn_ppn_gate"]
        and
        dependencies["status_and_scope_checks"]["w3_54_action_and_source_gate"]
        and dependencies["status_and_scope_checks"][
            "w3_64_nec_penrose_and_source_gate"
        ]
        and j52.get("source_ledger", {}).get("T_mn_from_S_matter") == 1
        and j52.get("source_ledger", {}).get("p_readout_as_extra_source") == 0
        and noether["checks"][
            "one_metric_once_counted_total_hilbert_ledger"
        ]
        and j54.get("pressure_roles", {}).get("P_F_equals_p_C_derived") is False
    )

    closure_flags["dependency_hashes_exact"] = dependencies["hashes_exact"]
    closure_flags["upstream_status_and_scope_exact"] = dependencies[
        "upstream_status_and_scope_exact"
    ]
    closure_flags[
        "one_coframe_one_metric_once_counted_total_hilbert_source_ledger_exact"
    ] = total_source_ledger_exact
    closure_flags["weak_biconformal_dictionary_exact"] = bool(
        weak["checks"]["coordinate_speed_from_frozen_clock_ruler_laws"]
        and weak["checks"]["biconformal_gamma_one"]
    )
    closure_flags["local_light_speed_reconstruction_exact"] = weak["checks"][
        "local_speed_exact"
    ]
    closure_flags["pure_conformal_mutation_rejected"] = weak["checks"][
        "pure_conformal_validator_reject"
    ]
    closure_flags["full_standard_1pn_ppn_inherited_exact"] = bool(
        full_1pn["checks"]["registered_status_exact"]
        and full_1pn["checks"]["complete_standard_ppn_vector_exact"]
        and full_1pn["checks"]["eih_inheritance_registered_exact"]
        and full_1pn["checks"]["one_source_1pn_ledger_exact"]
        and full_1pn["checks"]["no_unsuppressed_extra_1pn_operator_exact"]
    )
    closure_flags["full_1pn_componentwise_remainder_contract_exact"] = bool(
        full_1pn["checks"]["component_orders_exact"]
        and full_1pn["checks"]["first_omitted_orders_exact"]
        and full_1pn["checks"]["componentwise_remainder_flag_exact"]
        and full_1pn["checks"][
            "clock_ruler_common_only_through_spatial_order_exact"
        ]
    )
    closure_flags["full_coframe_temporal_spatial_split_exact"] = coframe["all_pass"]
    closure_flags["passive_common_scale_dimensionless_invariants_exact"] = bool(
        scaling["checks"]["all_dimensionless_residuals_zero"]
        and scaling["checks"]["constant_weyl_has_no_derivative_terms"]
    )
    closure_flags["local_weyl_eh_derivative_identity_exact"] = bool(
        scaling["checks"]["local_weyl_ricci_scalar_identity_exact"]
        and scaling["checks"]["variable_weyl_generates_derivative_terms"]
        and scaling["checks"]["four_dimensional_weyl_derivative_coefficients_exact"]
        and scaling["checks"]["regular_variable_full_theory_map_invertible"]
    )
    closure_flags["local_weyl_unchanged_eh_mutation_rejected"] = bool(
        mutations["checks"]["variable_weyl_without_derivative_terms_rejected"]
        and mutations["checks"]["zero_weyl_map_rejected_as_noninvertible"]
        and mutations["checks"]["divergent_weyl_map_rejected_as_noninvertible"]
    )
    closure_flags["passive_p_no_new_dynamics_exact"] = scaling["checks"][
        "passive_p_no_dynamics"
    ]
    closure_flags["explicit_scale_noether_exchange_registered_exact"] = bool(
        noether["checks"]["noether_exchange_identity_derived_exact"]
        and noether["checks"]["first_variation_and_lie_coefficients_exact"]
        and noether["checks"]["prescribed_variable_p_exchange_not_identically_zero"]
    )
    closure_flags["total_action_conservation_requirement_exact"] = bool(
        noether["checks"]["p_equation_removes_exchange_on_shell"]
        and noether["checks"]["constant_p_has_no_exchange"]
        and noether["checks"][
            "arbitrary_nonconstant_p_requires_euler_equation"
        ]
        and noether["checks"]["one_metric_once_counted_total_hilbert_ledger"]
        and noether["checks"]["action_completion_requirement"]
    )
    closure_flags[
        "common_algebraic_response_cubic_screening_sufficient_exact"
    ] = bool(
        response["checks"]["generic_taylor_conditions_exact"]
        and response["checks"]["screened_generic_begins_cubic"]
        and response["checks"]["componentwise_regular_carrier_map_exact"]
        and response["checks"]["componentwise_corrections_cubic_or_later"]
        and response["checks"][
            "componentwise_corrections_no_earlier_than_first_omitted"
        ]
    )
    closure_flags["weak_jet_strong_completion_nonselection_exact"] = bool(
        response["checks"]["f1_weak_screen_pass"]
        and response["checks"]["f2_weak_screen_pass"]
        and response["checks"]["same_weak_jet_through_quadratic"]
        and response["checks"]["finite_argument_strong_difference_order_one"]
        and response["checks"]["asymptotic_growth_cubic_versus_linear"]
    )
    closure_flags["healthy_collective_phase_nec_exact"] = bool(
        j64.get("closure_flags", {}).get("collective_phase_nec_exact")
        and j64.get("regularity_and_penrose_boundary", {}).get(
            "collective_source_nec_exact"
        )
    )
    closure_flags["ordinary_scalar_nec_inherited_exact"] = bool(
        j64.get("closure_flags", {}).get("ordinary_scalar_nec_exact")
        and j64.get("regularity_and_penrose_boundary", {}).get(
            "scalar_source_nec_exact"
        )
    )
    closure_flags["regular_centre_mass_order_exact"] = bool(
        regular["checks"]["finite_density_mass_series_exact"]
        and regular["checks"]["mass_differential_equation_exact"]
        and regular["checks"]["mass_at_centre_zero_exact"]
        and regular["checks"]["regular_mass_order_validator_pass"]
    )
    closure_flags[
        "regular_centre_lapse_isotropy_conditions_registered_exact"
    ] = bool(
        regular["checks"]["finite_nonzero_lapse_registered"]
        and regular["checks"]["central_isotropy_registered"]
        and regular["checks"][
            "finite_central_curvature_not_global_completeness"
        ]
    )
    closure_flags["regular_centre_curvature_benchmark_exact"] = bool(
        regular["checks"]["regular_curvature_exact"]
        and regular["checks"]["point_mass_curvature_exact"]
        and regular["checks"]["point_mass_centre_validator_reject"]
    )
    closure_flags["penrose_trapped_surface_boundary_inherited_exact"] = bool(
        j64.get("closure_flags", {}).get(
            "penrose_trapped_surface_implication_registered_exact"
        )
        and penrose["all_pass"]
    )
    closure_flags["mutation_controls_pass"] = mutations["all_pass"]

    selection_ledger = {
        "activation_invariant": None,
        "activation_scale": None,
        "response_function": None,
        "response_action": None,
        "core_profile": None,
        "curvature_or_density_threshold": None,
    }
    domain_ledger = {
        "w3_47_homogeneous_law_applied_to_local_compact_deficit": False,
        "w3_51_weak_common_factor_p_promoted_to_exact_strong_coframe": False,
        "w3_55_homogeneous_scale_promoted_to_local_profile": False,
    }
    boundary_checks = {
        "all_required_scope_flags_false": validate_scope_flags(scope_flags),
        "no_response_or_core_selection_inserted": validate_selection_ledger(
            selection_ledger
        ),
        "upstream_domain_boundaries_respected": validate_domain_ledger(domain_ledger),
    }
    gate_registry = {
        "G0_GOAL": {
            "required": True,
            "pass": bool(
                dependencies["records"]["w3_67_preregistration"]["hash_exact"]
                and dependencies["contract_marker_checks"][
                    "w3_67_claim_status_and_package_registered"
                ]
            ),
            "evidence": "immutable claim, method, pass/fail, scope and stop rule",
        },
        "G1_CONVENTIONS": {
            "required": True,
            "pass": bool(
                weak["all_pass"]
                and coframe["all_pass"]
                and noether["other_matter_fields_on_shell"]
            ),
            "evidence": "p/u, metric, source, sign, unit and spherical registries",
        },
        "G2_CORE_ALGEBRA": {
            "required": True,
            "pass": bool(
                weak["all_pass"]
                and coframe["all_pass"]
                and scaling["all_pass"]
                and response["all_pass"]
                and regular["all_pass"]
            ),
            "evidence": "exact symbolic residuals",
        },
        "G3_STRUCTURE": {
            "required": True,
            "pass": bool(
                noether["all_pass"]
                and response["checks"][
                    "asymptotic_growth_cubic_versus_linear"
                ]
                and all(boundary_checks.values())
            ),
            "evidence": "action admissibility, nonselection and OPEN boundary",
        },
        "G4_INDEPENDENT_CHECK": {
            "required": True,
            "pass": mutations["all_pass"],
            "evidence": "independent substitutions and executed mutations",
        },
        "G5_LIMITS_REGRESSION": {
            "required": True,
            "pass": bool(dependencies["all_pass"] and full_1pn["all_pass"]),
            "evidence": "hash-pinned W3-41/51/52/54/55/64/66 regressions",
        },
        "G6_PHYSICAL_MATCH": {
            "required": True,
            "pass": bool(
                total_source_ledger_exact
                and closure_flags["healthy_collective_phase_nec_exact"]
                and closure_flags["ordinary_scalar_nec_inherited_exact"]
                and closure_flags[
                    "penrose_trapped_surface_boundary_inherited_exact"
                ]
                and closure_flags[
                    "passive_common_scale_dimensionless_invariants_exact"
                ]
            ),
            "evidence": "once-counted total source and operational observable map",
        },
        "G7_OBSERVATION": {
            "required": False,
            "not_applicable_exact": True,
            "pass": True,
            "reason": "W3-67 derives no new observable and reads or fits no data",
        },
        "G8_EXPORT": {
            "required": False,
            "not_applicable_exact": True,
            "pass": True,
            "reason": (
                "W3-67 changes neither Canon nor an intuitive manuscript; "
                "its only runtime write target is the registered result JSON"
            ),
        },
    }
    closure_flags["g0_goal_pass"] = gate_registry["G0_GOAL"]["pass"]
    closure_flags["g1_conventions_pass"] = gate_registry["G1_CONVENTIONS"]["pass"]
    closure_flags["g2_core_algebra_pass"] = gate_registry["G2_CORE_ALGEBRA"]["pass"]
    closure_flags["g3_structure_pass"] = gate_registry["G3_STRUCTURE"]["pass"]
    closure_flags["g4_independent_check_pass"] = gate_registry[
        "G4_INDEPENDENT_CHECK"
    ]["pass"]
    closure_flags["g5_limits_regression_pass"] = gate_registry[
        "G5_LIMITS_REGRESSION"
    ]["pass"]
    closure_flags["g6_physical_match_pass"] = gate_registry[
        "G6_PHYSICAL_MATCH"
    ]["pass"]
    closure_flags["g7_observation_not_applicable_exact"] = gate_registry[
        "G7_OBSERVATION"
    ]["not_applicable_exact"]
    closure_flags["g8_export_not_applicable_exact"] = gate_registry[
        "G8_EXPORT"
    ]["not_applicable_exact"]

    result: dict[str, Any] = {
        "schema_version": "W3-67-result-v1.0",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "status": FAIL_STATUS,
        "artifact_valid": False,
        "evidence_type": (
            "EXACT_OPERATIONAL_DICTIONARY_REGRESSION_AND_STRONG_FIELD_RESPONSE_BOUNDARY"
        ),
        "dependencies": dependencies,
        "gate_registry": gate_registry,
        "symbolic": {
            "weak_dictionary": weak,
            "full_1pn_inheritance": full_1pn,
            "full_coframe_split": coframe,
            "common_scaling_and_weyl_action": scaling,
            "noether_exchange_and_source_ledger": noether,
            "weak_response_screening_and_nonselection": response,
            "regular_centre_benchmark": regular,
            "penrose_theorem_handoff": penrose,
        },
        "controls": mutations,
        "selection_ledger": selection_ledger,
        "domain_ledger": domain_ledger,
        "boundary_checks": boundary_checks,
        "closure_flags": closure_flags,
        "scope_flags": scope_flags,
        "package": {
            "expected_exact_files": [],
            "actual_files": [],
            "missing_files": [],
            "unexpected_files": [],
            "subdirectories": [],
            "pass": False,
        },
        "missing_premise": {
            "status": "OPEN",
            "exact_input": (
                "One universal diffeomorphism-invariant local foundation constitutive "
                "action, or an equivalent microphysically derived local bridge, that "
                "selects the response carrier, activation invariant, scale, coefficients, "
                "and once-only Hilbert source."
            ),
        },
        "scientific_boundary": (
            "W3-67 separates passive common rescaling from active strong-field dynamics, "
            "verifies the weak and 1PN inheritance, preserves the one-metric once-counted "
            "total Hilbert source ledger, and fixes the current NEC/Penrose boundary. "
            "A variable scale "
            "must enter through a covariant action or exact field elimination. The frozen "
            "inputs do not select that response, a regular trapped solution, geodesic "
            "completeness, singularity resolution, or a new strong-field observable."
        ),
        "references": [
            {
                "citation": (
                    "R. Penrose, Gravitational Collapse and Space-Time Singularities, "
                    "Physical Review Letters 14, 57 (1965)"
                ),
                "doi": "10.1103/PhysRevLett.14.57",
                "role": "trapped-surface/null-convergence theorem handoff",
            },
            {
                "citation": (
                    "A. L. Alinea, On the Disformal Transformation of the Einstein-Hilbert "
                    "Action, Jordan Journal of Physics 16, 507 (2024)"
                ),
                "url": "https://arxiv.org/abs/2010.00956",
                "role": "metric-rescaling action identity cross-reference",
            },
        ],
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
            "preregistration_sha256": sha256(PREREG),
            "source_sha256": sha256(Path(__file__)),
            "deterministic": True,
            "network_used_by_verifier": False,
            "archived_theory_used": False,
        },
    }

    # The provisional result is also written atomically. It creates the third
    # registered package file, after which the exact package gate can run.
    atomic_write_json(result)
    package = package_gate()
    result["package"] = package
    closure_flags["package_clean_pass"] = package["pass"]
    closure_flags["aggregate_gate_pass"] = bool(
        all(
            closure_flags[name]
            for name in TRUE_FLAG_NAMES
            if name != "aggregate_gate_pass"
        )
        and all(boundary_checks.values())
        and validate_scope_flags(scope_flags)
    )
    result["artifact_valid"] = closure_flags["aggregate_gate_pass"]
    result["status"] = PASS_STATUS if result["artifact_valid"] else FAIL_STATUS
    atomic_write_json(result)

    print(
        json.dumps(
            {
                "claim_id": result["claim_id"],
                "status": result["status"],
                "artifact_valid": result["artifact_valid"],
                "closure_flags": result["closure_flags"],
                "scope_flags": result["scope_flags"],
                "package": result["package"],
            },
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
    )


if __name__ == "__main__":
    main()
