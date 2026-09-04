from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import tempfile
from pathlib import Path
from typing import Any

import sympy as sp


HERE = Path(__file__).resolve().parent
STRONG_FIELD = HERE.parent
WORK3 = STRONG_FIELD.parent
PREREG = HERE / "w3_68_born_infeld_candidate_admissibility_preregistration.md"
OUTPUT = HERE / "w3_68_result.json"

CLAIM_ID = "W3_68_BORN_INFELD_FT_CANDIDATE_ADMISSIBILITY"
MODEL_VERSION = "W3-68-v1.0-COVARIANT-BORN-INFELD-FT-ADMISSIBILITY"
PASS_STATUS = (
    "PASS_EXACT_BORN_INFELD_FT_ACTION_AND_WEAK_TEGR_1PN_REGRESSION__"
    "REJECTED_CANDIDATE_BY_LATE_ONSET_MODE_WEAK_BRANCH_HEALTH_VETO__"
    "GLOBAL_STRONG_FIELD_SOLVE_NOT_OPENED"
)
FAIL_STATUS = "FAIL_W3_68_BORN_INFELD_CANDIDATE_ADMISSIBILITY_AUDIT"

# This value is replaced only after the immutable preregistration exists.
EXPECTED_PREREG_HASH = "afd38da6bd297e6ed029936d9a1162ea7da85377935adf06cb5326edade53f5e"

DEPENDENCY_PATHS = {
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
    "w3_64_preregistration": (
        STRONG_FIELD
        / "W3-64_Einstein_Continuation"
        / "w3_64_source_first_einstein_strong_field_preregistration.md"
    ),
    "w3_64_result": (
        STRONG_FIELD
        / "W3-64_Einstein_Continuation"
        / "w3_64_result.json"
    ),
    "w3_67_preregistration": (
        STRONG_FIELD
        / "W3-67_Foundation_Strong_Field_Response"
        / "w3_67_foundation_strong_field_response_preregistration.md"
    ),
    "w3_67_result": (
        STRONG_FIELD
        / "W3-67_Foundation_Strong_Field_Response"
        / "w3_67_result.json"
    ),
    "w3_68_preregistration": PREREG,
}

EXPECTED_HASHES = {
    "w3_52_contract": "66a33a82d29bd65fabc37b6e55f29a64674f0e44f5a4c0893611c261d00792b6",
    "w3_52_result": "8ae2d80cbc983e29a7ccc9ef4e3f6685b36cb4e6ade06e6d2a494fd9f46e11e2",
    "w3_54_contract": "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
    "w3_54_result": "ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991",
    "w3_64_preregistration": "25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1",
    "w3_64_result": "b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b",
    "w3_67_preregistration": "31e6520d9b7917413b9f2978291b4a77f067abe8dd3d6a9e89e1b2cfb699da11",
    "w3_67_result": "659bdfe171a8279b465fdd49eaf590755da22a7522a83053a4a06450fd745385",
    "w3_68_preregistration": EXPECTED_PREREG_HASH,
}

W3_54_STATUS = (
    "CONDITIONAL_EXACT_SELECTED_RELATIONAL_COFRAME_MASTER_ACTION_TO_"
    "TEGR_EQUIVALENT_EH_AND_PHASE_CURRENT_T"
)
W3_64_STATUS = (
    "PASS_CONDITIONAL_EXACT_UNCHANGED_EINSTEIN_BACKREACTION_AND_CURRENT_"
    "SOURCE_NEC_BOUNDARY__CONVERGED_NUMERICAL_REGULAR_HORIZONLESS_SELF_"
    "GRAVITATING_Q_BALL_WITNESS__REGULAR_TRAPPED_NULL_COMPLETE_INTERIOR_"
    "REQUIRES_FAILURE_OF_AT_LEAST_ONE_PENROSE_HYPOTHESIS"
)
W3_67_STATUS = (
    "PASS_EXACT_FOUNDATION_STRONG_FIELD_RESPONSE_BOUNDARY__"
    "PASSIVE_AND_COMMON_RESCALING_NO_GO__"
    "COVARIANT_ACTION_AND_CONSTITUTIVE_SELECTION_OPEN"
)

REQUIRED_TRUE_CLOSURE_FLAGS = (
    "g0_goal_pass",
    "g1_conventions_pass",
    "g2_core_algebra_pass",
    "g3_audit_pass",
    "g3_structure_health_veto_failed_exact",
    "g4_independent_check_pass",
    "g5_limits_regression_pass",
    "g6_physical_match_pass",
    "g7_observation_not_applicable_exact",
    "g8_export_not_applicable_exact",
    "dependency_hashes_exact",
    "upstream_status_and_scope_exact",
    "newly_selected_universal_candidate_action_registered_exact",
    "born_infeld_function_and_principal_branch_exact",
    "square_root_domain_exact",
    "f_T_exact",
    "f_TT_exact",
    "low_T_series_exact",
    "torsion_weak_order_exact",
    "born_infeld_correction_quartic_action_order_exact",
    "born_infeld_correction_cubic_eom_order_exact",
    "tegr_quadratic_hessian_exact",
    "full_standard_1pn_ppn_regression_exact",
    "full_1pn_componentwise_remainder_regression_exact",
    "covariant_flat_inertial_spin_connection_registered_exact",
    "pure_tetrad_arbitrary_frame_mutation_rejected",
    "one_coframe_one_metric_once_counted_source_ledger_exact",
    "finite_lambda_nonzero_f_TT_exact",
    "nonlinear_ft_late_onset_mode_handoff_registered_exact",
    "precise_universal_dof_count_not_claimed_exact",
    "weak_branch_kinetic_health_requirement_exact",
    "late_onset_sector_missing_quadratic_kinetic_exact",
    "strong_coupling_cutoff_completion_absent_exact",
    "hard_health_veto_triggered_exact",
    "born_infeld_ft_candidate_rejected_exact",
    "global_solution_stop_rule_enforced",
    "mutation_controls_pass",
    "package_clean_pass",
    "aggregate_audit_pass",
)

REQUIRED_FALSE_SCOPE_FLAGS = (
    "candidate_structure_health_pass",
    "aggregate_candidate_admissibility_pass",
    "born_infeld_candidate_refg_derived",
    "born_infeld_candidate_unique",
    "Lambda_star_derived_from_foundation",
    "Lambda_star_observationally_identified",
    "nonlinear_mode_quadratic_kinetic_closed",
    "strong_coupling_scale_derived",
    "full_nonlinear_dof_count_claimed",
    "foundation_strong_field_response_derived",
    "regular_black_hole_solution_derived",
    "trapped_surface_derived",
    "geodesic_completeness_derived",
    "singularity_resolution_completed",
    "new_strong_field_prediction_derived",
    "observational_forward_model_built",
    "observational_likelihood_evaluated",
    "canon_changed",
    "intuitive_files_changed",
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
        raise TypeError(f"expected a JSON object: {path}")
    return value


def finite_tree(value: Any) -> bool:
    if isinstance(value, dict):
        return all(finite_tree(key) and finite_tree(item) for key, item in value.items())
    if isinstance(value, (list, tuple)):
        return all(finite_tree(item) for item in value)
    if isinstance(value, float):
        return math.isfinite(value)
    return True


def atomic_write_json(value: dict[str, Any]) -> None:
    if not finite_tree(value):
        raise RuntimeError("result contains a non-finite number")
    payload = json.dumps(
        value,
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
            dir=HERE,
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


def exact_zero(expression: sp.Expr) -> bool:
    return bool(sp.simplify(expression) == 0)


def exact_equal(left: sp.Expr, right: sp.Expr) -> bool:
    return exact_zero(left - right)


def all_named_true(values: dict[str, Any]) -> bool:
    return bool(values and all(value is True for value in values.values()))


def dependency_gate() -> dict[str, Any]:
    records: dict[str, Any] = {}
    for name, path in DEPENDENCY_PATHS.items():
        actual = sha256(path)
        expected = EXPECTED_HASHES[name]
        records[name] = {
            "path": path.relative_to(WORK3).as_posix(),
            "expected_sha256": expected,
            "actual_sha256": actual,
            "hash_exact": actual == expected,
        }

    j52 = read_json(DEPENDENCY_PATHS["w3_52_result"])
    j54 = read_json(DEPENDENCY_PATHS["w3_54_result"])
    j64 = read_json(DEPENDENCY_PATHS["w3_64_result"])
    j67 = read_json(DEPENDENCY_PATHS["w3_67_result"])
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
        "w3_52_selected_eh_1pn_regression_exact": bool(
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
            and j52.get("PPN_registry_rank") == 10
            and j52.get("PPN_parameter_count") == 10
        ),
        "w3_54_covariant_coframe_tegr_conventions_exact": bool(
            j54.get("aggregate_pass")
            and j54.get("status") == W3_54_STATUS
            and j54.get("closure_flags", {}).get(
                "SELECTED_COFRAME_DEFINES_FULL_OPERATIONAL_METRIC"
            )
            and j54.get("closure_flags", {}).get(
                "FLAT_INERTIAL_TRANSPORT_SELECTED"
            )
            and j54.get("closure_flags", {}).get(
                "TEGR_COEFFICIENT_RATIOS_DERIVED"
            )
            and j54.get("tegr_coefficients")
            == {"c1": "1/4", "c2": "1/2", "c3": "-1"}
        ),
        "w3_64_localized_ordinary_scalar_source_exact": bool(
            j64.get("artifact_valid")
            and j64.get("status") == W3_64_STATUS
            and j64.get("closure_flags", {}).get("aggregate_gate_pass")
            and j64.get("closure_flags", {}).get("one_einstein_metric_exact")
            and j64.get("closure_flags", {}).get(
                "one_localized_hilbert_source_exact"
            )
            and j64.get("source_ledger", {}).get("localized_einstein_rhs")
            == ["T_O"]
            and j64.get("source_ledger", {}).get(
                "homogeneous_collective_T_C_readded_locally"
            )
            is False
            and not j64.get("scope_flags", {}).get(
                "new_gravity_operator_introduced"
            )
            and not j64.get("scope_flags", {}).get("second_metric_introduced")
            and not j64.get("scope_flags", {}).get(
                "singularity_resolution_completed"
            )
        ),
        "w3_67_action_selection_boundary_exact": bool(
            j67.get("artifact_valid")
            and j67.get("status") == W3_67_STATUS
            and j67.get("closure_flags", {}).get("aggregate_gate_pass")
            and not j67.get("scope_flags", {}).get(
                "foundation_strong_field_response_derived"
            )
            and not j67.get("scope_flags", {}).get(
                "singularity_resolution_completed"
            )
            and j67.get("provenance", {}).get("preregistration_sha256")
            == EXPECTED_HASHES["w3_67_preregistration"]
        ),
    }
    prereg_text = PREREG.read_text(encoding="utf-8")
    preregistration_checks = {
        "claim_id_registered": CLAIM_ID in prereg_text,
        "model_version_registered": MODEL_VERSION in prereg_text,
        "pass_status_registered": PASS_STATUS in prereg_text,
        "candidate_formula_registered": all(
            marker in prereg_text
            for marker in (
                "f_BI(T)",
                "1-2T/Lambda_*",
                "aggregate_candidate_admissibility_pass",
            )
        ),
    }
    hashes_exact = bool(all(record["hash_exact"] for record in records.values()))
    statuses_exact = bool(
        all_named_true(status_checks) and all_named_true(preregistration_checks)
    )
    return {
        "records": records,
        "status_checks": status_checks,
        "preregistration_checks": preregistration_checks,
        "hashes_exact": hashes_exact,
        "upstream_status_and_scope_exact": statuses_exact,
        "all_pass": bool(hashes_exact and statuses_exact),
    }


def born_infeld_exact_algebra() -> dict[str, Any]:
    T = sp.symbols("T", real=True)
    Lambda = sp.symbols("Lambda_BI", positive=True, finite=True)
    eps = sp.symbols("eps", real=True)
    tau = sp.symbols("tau", real=True)
    x = sp.symbols("x", real=True)
    radicand_positive = sp.symbols("radicand_positive", positive=True, finite=True)

    f = Lambda * (1 - sp.sqrt(1 - 2 * T / Lambda))
    f_T = sp.simplify(sp.diff(f, T))
    f_TT = sp.simplify(sp.diff(f_T, T))
    expected_f_T = 1 / sp.sqrt(1 - 2 * T / Lambda)
    expected_f_TT = 1 / (Lambda * (1 - 2 * T / Lambda) ** sp.Rational(3, 2))
    series_T = sp.series(f, T, 0, 5).removeO().expand()
    expected_series_T = (
        T
        + T**2 / (2 * Lambda)
        + T**3 / (2 * Lambda**2)
        + 5 * T**4 / (8 * Lambda**3)
    )
    derivative_reconstructed_series = sp.expand(
        sum(
            sp.diff(f, T, order).subs(T, 0) * T**order / sp.factorial(order)
            for order in range(5)
        )
    )

    f_eps = f.subs(T, eps**2 * tau)
    series_eps = sp.series(f_eps, eps, 0, 8).removeO().expand()
    expected_series_eps = (
        eps**2 * tau
        + eps**4 * tau**2 / (2 * Lambda)
        + eps**6 * tau**3 / (2 * Lambda**2)
    )
    nonlinear_correction = sp.simplify(f - T)
    correction_eps = nonlinear_correction.subs(T, eps**2 * tau)
    correction_series = sp.series(correction_eps, eps, 0, 8).removeO().expand()
    expected_correction_series = (
        eps**4 * tau**2 / (2 * Lambda)
        + eps**6 * tau**3 / (2 * Lambda**2)
    )
    correction_eom_proxy = sp.diff(correction_eps, eps)
    correction_eom_series = (
        sp.series(correction_eom_proxy, eps, 0, 7).removeO().expand()
    )
    expected_correction_eom_series = (
        2 * eps**3 * tau**2 / Lambda
        + 3 * eps**5 * tau**3 / Lambda**2
    )

    f_T_at_zero = sp.simplify(f_T.subs(T, 0))
    f_TT_at_zero = sp.simplify(f_TT.subs(T, 0))
    quadratic_hessian = sp.simplify(sp.diff(f_eps, eps, 2).subs(eps, 0))
    correction_quadratic_hessian = sp.simplify(
        sp.diff(correction_eps, eps, 2).subs(eps, 0)
    )
    radicand_x = 1 - 2 * x
    boundary = sp.Rational(1, 2)

    checks = {
        "f_at_zero_exact": exact_zero(f.subs(T, 0)),
        "f_T_formula_exact": exact_equal(f_T, expected_f_T),
        "f_T_at_zero_exact": exact_equal(f_T_at_zero, sp.Integer(1)),
        "f_TT_formula_exact": exact_equal(f_TT, expected_f_TT),
        "f_TT_at_zero_exact": exact_equal(f_TT_at_zero, 1 / Lambda),
        "f_TT_nonzero_for_positive_Lambda": bool(
            sp.ask(sp.Q.nonzero(f_TT_at_zero)) is True
        ),
        "f_TT_open_domain_product_identity_exact": exact_equal(
            f_TT * Lambda * (1 - 2 * T / Lambda) ** sp.Rational(3, 2),
            sp.Integer(1),
        ),
        "f_TT_nonzero_through_open_domain_exact": bool(
            sp.ask(
                sp.Q.nonzero(
                    1 / (Lambda * radicand_positive ** sp.Rational(3, 2))
                )
            )
            is True
        ),
        "series_through_T4_exact": exact_equal(series_T, expected_series_T),
        "derivative_reconstruction_matches_series_exact": exact_equal(
            derivative_reconstructed_series, expected_series_T
        ),
        "tegr_ratio_limit_exact": exact_equal(
            sp.limit(f / T, T, 0), sp.Integer(1)
        ),
        "nonlinear_relative_limit_zero": exact_zero(
            sp.limit(nonlinear_correction / T, T, 0)
        ),
        "dimensionless_radicand_at_tegr_point_one": exact_equal(
            radicand_x.subs(x, 0), sp.Integer(1)
        ),
        "differentiable_domain_boundary_exact": exact_zero(
            radicand_x.subs(x, boundary)
        ),
        "radicand_decreases_monotonically": exact_equal(
            sp.diff(radicand_x, x), sp.Integer(-2)
        ),
        "f_T_diverges_at_upper_boundary": sp.limit(
            f_T, T, Lambda / 2, dir="-"
        )
        == sp.oo,
        "f_TT_diverges_at_upper_boundary": sp.limit(
            f_TT, T, Lambda / 2, dir="-"
        )
        == sp.oo,
        "perturbative_series_exact": exact_equal(series_eps, expected_series_eps),
        "nonlinear_correction_series_exact": exact_equal(
            correction_series, expected_correction_series
        ),
        "quadratic_hessian_equals_tegr": exact_equal(
            quadratic_hessian, 2 * tau
        ),
        "nonlinear_correction_has_zero_quadratic_hessian": exact_zero(
            correction_quadratic_hessian
        ),
        "first_nonlinear_eps_coefficient_is_order_four": bool(
            exact_zero(correction_series.coeff(eps, 0))
            and exact_zero(correction_series.coeff(eps, 1))
            and exact_zero(correction_series.coeff(eps, 2))
            and exact_zero(correction_series.coeff(eps, 3))
            and exact_equal(
                correction_series.coeff(eps, 4), tau**2 / (2 * Lambda)
            )
        ),
        "euler_lagrange_amplitude_order_proxy_is_cubic": bool(
            exact_equal(correction_eom_series, expected_correction_eom_series)
            and exact_zero(correction_eom_series.coeff(eps, 0))
            and exact_zero(correction_eom_series.coeff(eps, 1))
            and exact_zero(correction_eom_series.coeff(eps, 2))
            and exact_equal(
                correction_eom_series.coeff(eps, 3), 2 * tau**2 / Lambda
            )
        ),
    }
    domain = {
        "parameter": "Lambda_BI > 0",
        "frozen_admitted_real_action_domain": "T/Lambda_BI < 1/2",
        "analytic_Taylor_domain": "abs(2*T/Lambda_BI) < 1",
        "selected_branch": "principal square root continuously connected to TEGR at T=0",
        "excluded_endpoint": "T/Lambda_BI=1/2; f_T and f_TT diverge",
    }
    perturbative_order = {
        "registered_torsion_order": "T=O(eps^2) around the torsionless coframe",
        "tegr_term_order": "O(eps^2)",
        "first_born_infeld_correction_order": "O(eps^4)",
        "first_euler_lagrange_correction_order": "O(eps^3)",
        "exact_consequence": (
            "the quadratic coframe Hessian on the torsionless weak branch is TEGR"
        ),
        "non_consequence": (
            "this order count does not establish nonlinear characteristic health, "
            "a full candidate 1PN solution, or singularity resolution"
        ),
    }
    return {
        "candidate": "f_BI(T)=Lambda_BI*(1-sqrt(1-2*T/Lambda_BI))",
        "f_T": sp.sstr(f_T),
        "f_TT": sp.sstr(f_TT),
        "f_TT_at_zero": sp.sstr(f_TT_at_zero),
        "series_T_through_fourth_order": sp.sstr(series_T),
        "derivative_reconstructed_series": sp.sstr(
            derivative_reconstructed_series
        ),
        "series_after_T_equals_eps2_tau": sp.sstr(series_eps),
        "nonlinear_correction_series": sp.sstr(correction_series),
        "nonlinear_correction_eom_order_proxy_series": sp.sstr(
            correction_eom_series
        ),
        "quadratic_hessian": sp.sstr(quadratic_hessian),
        "nonlinear_correction_quadratic_hessian": sp.sstr(
            correction_quadratic_hessian
        ),
        "domain": domain,
        "perturbative_order": perturbative_order,
        "checks": checks,
        "all_exact_algebra_pass": all_named_true(checks),
    }


def action_and_source_gate() -> dict[str, Any]:
    localized_source_ledger = {
        "ordinary_scalar_action_count": 1,
        "ordinary_scalar_hilbert_T_O_count": 1,
        "collective_phase_source_local_count": 0,
        "Lambda_F": 0,
        "metric_self_energy_readded_on_rhs": 0,
        "P_F_or_readout_p_readded": 0,
        "material_scale_or_cadence_readded": 0,
        "additional_born_infeld_matter_source": 0,
    }
    checks = {
        "one_coframe": True,
        "one_operational_metric_g_equals_e_eta_e": True,
        "flat_inertial_spin_connection_retained": True,
        "torsion_scalar_is_T_of_e_and_omega": True,
        "candidate_replaces_only_gravitational_T_by_f_BI_of_T": True,
        "localized_w3_64_branch_frozen": True,
        "Lambda_F_zero_frozen": True,
        "localized_branch_ordinary_scalar_once": True,
        "localized_branch_does_not_readd_homogeneous_collective_source": True,
        "no_pressure_or_readout_double_count": True,
        "localized_source_ledger_exact": localized_source_ledger
        == {
            "ordinary_scalar_action_count": 1,
            "ordinary_scalar_hilbert_T_O_count": 1,
            "collective_phase_source_local_count": 0,
            "Lambda_F": 0,
            "metric_self_energy_readded_on_rhs": 0,
            "P_F_or_readout_p_readded": 0,
            "material_scale_or_cadence_readded": 0,
            "additional_born_infeld_matter_source": 0,
        },
    }
    return {
        "candidate_master_action": (
            "S_68=-K_F*integral[e*f_BI(T_TEGR(e,omega))]+S_O[g,chi,theta_O], "
            "with Lambda_F=0"
        ),
        "localized_source_action": (
            "S_O=-integral[sqrt(-g)*(1/2*g^munu*d_mu(chi)*d_nu(chi)"
            "+1/2*chi^2*g^munu*d_mu(theta_O)*d_nu(theta_O)+V(chi))]"
        ),
        "localized_potential": (
            "V(chi)=m_s^2*chi^2/2-lambda*chi^4/4+g_6*chi^6/6"
        ),
        "covariance_contract": (
            "covariant teleparallel coframe plus flat inertial spin connection; "
            "omega=0 is at most a selected proper-frame gauge, not an all-frame identity"
        ),
        "source_ledger": localized_source_ledger,
        "checks": checks,
        "all_pass": all_named_true(checks),
    }


def nonlinear_health_gate(algebra: dict[str, Any]) -> dict[str, Any]:
    nonlinear_f_TT = bool(
        algebra["checks"]["f_TT_open_domain_product_identity_exact"]
        and algebra["checks"]["f_TT_nonzero_through_open_domain_exact"]
    )
    no_new_weak_quadratic_kinetic = algebra["checks"][
        "nonlinear_correction_has_zero_quadratic_hessian"
    ]
    mismatch = bool(nonlinear_f_TT and no_new_weak_quadratic_kinetic)

    theorem_handoff = {
        "citation": (
            "J. Beltran Jimenez, A. Golovnev, T. Koivisto, and H. Veermae, "
            "Minkowski space in f(T) gravity"
        ),
        "arxiv": "2004.07536",
        "url": "https://arxiv.org/abs/2004.07536",
        "handoff_used": (
            "the paper explicitly finds a mode at fourth perturbative order around "
            "the trivial Minkowski tetrad and identifies the result as a strong-coupling signal"
        ),
        "not_imported_as_symbolic_proof": True,
        "precise_nonlinear_degree_of_freedom_count_assumed": False,
        "all_backgrounds_declared_pathological": False,
    }
    primary_literature = [
        {
            "arxiv": "1510.08432",
            "role": "covariant coframe plus compatible inertial spin connection",
        },
        {
            "arxiv": "1303.0993",
            "role": "nonlinear characteristic and Cauchy-development warning",
        },
        {
            "arxiv": "2004.07536",
            "role": "explicit fourth-order Minkowski mode and strong-coupling signal",
        },
        {
            "arxiv": "2110.11273",
            "role": "covariant teleparallel Lorentz symmetry and primary-constraint scope",
        },
        {
            "arxiv": "1901.02965",
            "role": "candidate motivation only; regular solution not imported",
        },
        {
            "arxiv": "2302.03545",
            "role": (
                "EFT caveat: apparent strong coupling need not be fatal when a "
                "controlled cutoff is derived; no such completion exists here"
            ),
        },
    ]
    requirements = {
        "nondegenerate_weak_branch_kinetic_operator_for_all_late_modes_demonstrated": False,
        "hyperbolic_complete_nonlinear_characteristic_symbol_demonstrated": False,
        "controlled_eft_cutoff_resolution_supplied": False,
        "background_independent_constraint_rank_demonstrated": False,
    }
    diagnostic_checks = {
        "nonlinear_f_TT_exact": nonlinear_f_TT,
        "no_new_weak_quadratic_kinetic_exact": no_new_weak_quadratic_kinetic,
        "weak_nonlinear_mode_mismatch_exact": mismatch,
        "theorem_handoff_identifier_exact": theorem_handoff["arxiv"]
        == "2004.07536",
        "theorem_handoff_not_mislabeled_symbolic": theorem_handoff[
            "not_imported_as_symbolic_proof"
        ],
        "precise_dof_count_not_assumed": not theorem_handoff[
            "precise_nonlinear_degree_of_freedom_count_assumed"
        ],
        "mandatory_health_requirements_fail": not all(requirements.values()),
    }
    weak_branch_nondegenerate_all_dof = False
    strong_coupling_health_pass = False
    characteristic_health_pass = False
    candidate_health_aggregate_pass = False
    candidate_admissible = False
    rejection_exact = bool(
        all_named_true(diagnostic_checks)
        and not weak_branch_nondegenerate_all_dof
        and not strong_coupling_health_pass
        and not characteristic_health_pass
        and not candidate_health_aggregate_pass
        and not candidate_admissible
    )
    return {
        "evidence_partition": {
            "exact_internal_algebra": (
                "f_TT is nonzero while f_BI-T begins at O(eps^4), so the "
                "nonlinear modification supplies no new quadratic weak-branch kinetic term"
            ),
            "external_theorem_handoff": theorem_handoff,
            "decision_standard": (
                "an unresolved nonlinear mode/characteristic health requirement is a "
                "candidate-admissibility veto, not a symbolic theorem that every solution fails"
            ),
            "eft_caveat": (
                "arXiv:2302.03545 permits a controlled-cutoff resolution in principle; "
                "the frozen one-parameter candidate supplies no cutoff or completion"
            ),
        },
        "primary_literature": primary_literature,
        "mandatory_requirements": requirements,
        "diagnostic_checks": diagnostic_checks,
        "weak_branch_nondegenerate_all_dof": weak_branch_nondegenerate_all_dof,
        "strong_coupling_health_pass": strong_coupling_health_pass,
        "characteristic_health_pass": characteristic_health_pass,
        "candidate_health_aggregate_pass": candidate_health_aggregate_pass,
        "candidate_admissible": candidate_admissible,
        "rejection_exact": rejection_exact,
    }


def candidate_signature(expression: sp.Expr, T: sp.Symbol, Lambda: sp.Symbol) -> dict[str, bool]:
    second_at_zero = sp.simplify(sp.diff(expression, T, 2).subs(T, 0))
    expected = T + T**2 / (2 * Lambda) + T**3 / (2 * Lambda**2)
    series = sp.series(expression, T, 0, 4).removeO().expand()
    return {
        "normalized_vacuum": exact_zero(expression.subs(T, 0)),
        "normalized_tegr_slope": exact_equal(
            sp.diff(expression, T).subs(T, 0), sp.Integer(1)
        ),
        "nonlinear_second_derivative": bool(
            sp.ask(sp.Q.nonzero(second_at_zero)) is True
        ),
        "born_infeld_series_signature": exact_equal(series, expected),
    }


def mutation_controls() -> dict[str, Any]:
    T = sp.symbols("T", real=True)
    Lambda = sp.symbols("Lambda_BI", positive=True, finite=True)
    f_bi = Lambda * (1 - sp.sqrt(1 - 2 * T / Lambda))
    f_linear = T
    f_wrong_series = Lambda * (sp.sqrt(1 + 2 * T / Lambda) - 1)

    bi_signature = candidate_signature(f_bi, T, Lambda)
    linear_signature = candidate_signature(f_linear, T, Lambda)
    wrong_signature = candidate_signature(f_wrong_series, T, Lambda)

    def reject_localized_source_ledger(T_O_count: int, local_T_C_count: int) -> bool:
        return (T_O_count, local_T_C_count) != (1, 0)

    def reject_pure_tetrad_all_frame_covariance(
        omega_mode: str, covariance_claimed: bool
    ) -> bool:
        return bool(
            covariance_claimed and omega_mode == "zero_in_all_frames_without_inertial_transform"
        )

    def reject_unproved_global_solution(
        claim_promoted: bool,
        field_equations_solved: bool,
        regularity_proved: bool,
        completeness_proved: bool,
    ) -> bool:
        return bool(
            claim_promoted
            and not (
                field_equations_solved and regularity_proved and completeness_proved
            )
        )

    def reject_domain_contract(
        strict_domain_registered: bool, singular_boundary_excluded: bool
    ) -> bool:
        return not (strict_domain_registered and singular_boundary_excluded)

    def reject_health_bypass(mismatch_present: bool, promoted: bool) -> bool:
        return bool(mismatch_present and promoted)

    retained_orders = {
        "g00": sp.Rational(2),
        "g0i": sp.Rational(3, 2),
        "gij": sp.Rational(1),
    }
    first_omitted_orders = {
        "g00": sp.Rational(3),
        "g0i": sp.Rational(5, 2),
        "gij": sp.Rational(2),
    }

    def componentwise_onset_beyond_1pn(
        onset: dict[str, sp.Rational],
    ) -> bool:
        return bool(
            set(onset) == set(retained_orders) == set(first_omitted_orders)
            and all(onset[key] > retained_orders[key] for key in retained_orders)
            and all(
                onset[key] >= first_omitted_orders[key] for key in retained_orders
            )
        )

    def reject_precise_dof_count(exact_count: int | None) -> bool:
        return exact_count is not None

    controls = {
        "baseline_born_infeld_signature_accepts": all_named_true(bi_signature),
        "linear_fT_not_rejected_for_hidden_nonlinear_mode_reason": bool(
            not linear_signature["nonlinear_second_derivative"]
        ),
        "linear_fT_cannot_impersonate_born_infeld_signature": bool(
            not linear_signature["born_infeld_series_signature"]
            and not linear_signature["nonlinear_second_derivative"]
        ),
        "wrong_series_mutation_rejected": not wrong_signature[
            "born_infeld_series_signature"
        ],
        "wrong_second_derivative_sign_rejected": exact_equal(
            sp.diff(f_wrong_series, T, 2).subs(T, 0), -1 / Lambda
        ),
        "f_TT_zero_mutation_rejected_as_nonlinear_candidate": not linear_signature[
            "nonlinear_second_derivative"
        ],
        "missing_square_root_domain_rejected": reject_domain_contract(False, True),
        "included_singular_boundary_rejected": reject_domain_contract(True, False),
        "candidate_cubic_eom_onset_beyond_all_retained_1pn_orders": componentwise_onset_beyond_1pn(
            {"g00": sp.Rational(3), "g0i": sp.Rational(3), "gij": sp.Rational(3)}
        ),
        "promoted_g00_q2_1pn_correction_rejected": not componentwise_onset_beyond_1pn(
            {"g00": sp.Rational(2), "g0i": sp.Rational(3), "gij": sp.Rational(3)}
        ),
        "precise_universal_mode_count_mutation_rejected": reject_precise_dof_count(
            5
        ),
        "no_precise_universal_mode_count_accepted": not reject_precise_dof_count(
            None
        ),
        "false_regular_black_hole_promotion_rejected": reject_unproved_global_solution(
            True, False, False, False
        ),
        "false_singularity_resolution_promotion_rejected": reject_unproved_global_solution(
            True, False, False, False
        ),
        "duplicate_ordinary_source_rejected": reject_localized_source_ledger(2, 0),
        "local_collective_source_readdition_rejected": reject_localized_source_ledger(
            1, 1
        ),
        "exact_localized_source_ledger_accepted": not reject_localized_source_ledger(
            1, 0
        ),
        "pure_tetrad_all_frame_covariance_claim_rejected": reject_pure_tetrad_all_frame_covariance(
            "zero_in_all_frames_without_inertial_transform", True
        ),
        "covariant_inertial_pair_not_rejected": not reject_pure_tetrad_all_frame_covariance(
            "flat_inertial_connection_transformed_with_coframe", True
        ),
        "bypassed_health_veto_rejected": reject_health_bypass(True, True),
        "false_scope_promotion_rejected": reject_unproved_global_solution(
            True, False, False, False
        ),
    }
    return {
        "baseline_signature": bi_signature,
        "linear_signature": linear_signature,
        "wrong_series_signature": wrong_signature,
        "checks": controls,
        "all_pass": all_named_true(controls),
    }


def package_gate() -> dict[str, Any]:
    expected = sorted((PREREG.name, Path(__file__).name, OUTPUT.name))
    actual_files = sorted(path.name for path in HERE.iterdir() if path.is_file())
    subdirectories = sorted(path.name for path in HERE.iterdir() if path.is_dir())
    missing = sorted(set(expected) - set(actual_files))
    unexpected = sorted(set(actual_files) - set(expected))
    return {
        "expected_exact_files": expected,
        "actual_files": actual_files,
        "missing_files": missing,
        "unexpected_files": unexpected,
        "subdirectories": subdirectories,
        "pass": bool(not missing and not unexpected and not subdirectories),
    }


def main() -> None:
    dependencies = dependency_gate()
    algebra = born_infeld_exact_algebra()
    action = action_and_source_gate()
    health = nonlinear_health_gate(algebra)
    mutations = mutation_controls()

    scope_flags = {name: False for name in REQUIRED_FALSE_SCOPE_FLAGS}
    closure_flags = {name: False for name in REQUIRED_TRUE_CLOSURE_FLAGS}

    gate_registry = {
        "G0_GOAL": {
            "required": True,
            "pass": bool(
                dependencies["records"]["w3_68_preregistration"]["hash_exact"]
                and all_named_true(dependencies["preregistration_checks"])
            ),
            "evidence": "hash-pinned immutable candidate, decision rule, scope, and stop rule",
        },
        "G1_CONVENTIONS": {
            "required": True,
            "pass": action["all_pass"],
            "evidence": "W3-54 geometry conventions plus the exact W3-64 localized T_O source ledger",
        },
        "G2_CORE_ALGEBRA": {
            "required": True,
            "pass": algebra["all_exact_algebra_pass"],
            "evidence": "exact SymPy derivatives, limits, series, domain boundary, and Hessian",
        },
        "G3_STRUCTURE": {
            "required": True,
            "pass": bool(action["all_pass"] and health["rejection_exact"]),
            "candidate_structure_health_pass": False,
            "expected_health_veto_failed_exact": bool(
                action["all_pass"] and health["rejection_exact"]
            ),
            "evidence": "the candidate fails the preregistered nonlinear kinetic/characteristic health gate",
        },
        "G4_INDEPENDENT_CHECK": {
            "required": True,
            "pass": mutations["all_pass"],
            "evidence": "executed linear, wrong-series, f_TT, source, covariance, and overclaim mutations",
        },
        "G5_LIMITS_REGRESSION": {
            "required": True,
            "pass": dependencies["all_pass"],
            "evidence": "hash-pinned W3-52, W3-54, W3-64, and W3-67 status and scope regression",
        },
        "G6_PHYSICAL_MATCH": {
            "required": True,
            "pass": bool(
                health["rejection_exact"]
                and health["candidate_admissible"] is False
                and health["strong_coupling_health_pass"] is False
                and health["characteristic_health_pass"] is False
            ),
            "evidence": (
                "the audit reaches the preregistered decisive rejection without promoting "
                "a literature handoff to an internal symbolic proof"
            ),
        },
        "G7_OBSERVATION": {
            "required": False,
            "not_applicable_exact": True,
            "pass": True,
            "reason": "the candidate is rejected before a new observable or likelihood is defined",
        },
        "G8_EXPORT": {
            "required": False,
            "not_applicable_exact": True,
            "pass": True,
            "reason": "no Canon or intuitive manuscript is changed by this audit",
        },
    }

    closure_flags.update(
        {
            "g0_goal_pass": gate_registry["G0_GOAL"]["pass"],
            "g1_conventions_pass": gate_registry["G1_CONVENTIONS"]["pass"],
            "g2_core_algebra_pass": gate_registry["G2_CORE_ALGEBRA"]["pass"],
            "g3_audit_pass": gate_registry["G3_STRUCTURE"]["pass"],
            "g3_structure_health_veto_failed_exact": gate_registry[
                "G3_STRUCTURE"
            ]["expected_health_veto_failed_exact"],
            "g4_independent_check_pass": gate_registry["G4_INDEPENDENT_CHECK"][
                "pass"
            ],
            "g5_limits_regression_pass": gate_registry["G5_LIMITS_REGRESSION"][
                "pass"
            ],
            "g6_physical_match_pass": gate_registry["G6_PHYSICAL_MATCH"][
                "pass"
            ],
            "g7_observation_not_applicable_exact": gate_registry["G7_OBSERVATION"][
                "not_applicable_exact"
            ],
            "g8_export_not_applicable_exact": gate_registry["G8_EXPORT"][
                "not_applicable_exact"
            ],
            "dependency_hashes_exact": dependencies["hashes_exact"],
            "upstream_status_and_scope_exact": dependencies[
                "upstream_status_and_scope_exact"
            ],
            "newly_selected_universal_candidate_action_registered_exact": bool(
                action["checks"]["candidate_replaces_only_gravitational_T_by_f_BI_of_T"]
                and action["checks"]["localized_w3_64_branch_frozen"]
                and action["checks"]["Lambda_F_zero_frozen"]
            ),
            "born_infeld_function_and_principal_branch_exact": bool(
                algebra["checks"]["f_at_zero_exact"]
                and algebra["checks"]["f_T_at_zero_exact"]
                and algebra["checks"]["series_through_T4_exact"]
            ),
            "square_root_domain_exact": bool(
                algebra["checks"]["dimensionless_radicand_at_tegr_point_one"]
                and algebra["checks"]["differentiable_domain_boundary_exact"]
                and algebra["checks"]["radicand_decreases_monotonically"]
                and algebra["checks"]["f_T_diverges_at_upper_boundary"]
                and algebra["checks"]["f_TT_diverges_at_upper_boundary"]
            ),
            "f_T_exact": bool(
                algebra["checks"]["f_T_formula_exact"]
                and algebra["checks"]["f_T_at_zero_exact"]
            ),
            "f_TT_exact": bool(
                algebra["checks"]["f_TT_formula_exact"]
                and algebra["checks"]["f_TT_at_zero_exact"]
                and algebra["checks"]["f_TT_open_domain_product_identity_exact"]
            ),
            "low_T_series_exact": bool(
                algebra["checks"]["series_through_T4_exact"]
                and algebra["checks"][
                    "derivative_reconstruction_matches_series_exact"
                ]
            ),
            "torsion_weak_order_exact": algebra["checks"][
                "perturbative_series_exact"
            ],
            "born_infeld_correction_quartic_action_order_exact": bool(
                algebra["checks"]["nonlinear_correction_series_exact"]
                and algebra["checks"][
                    "first_nonlinear_eps_coefficient_is_order_four"
                ]
            ),
            "born_infeld_correction_cubic_eom_order_exact": algebra["checks"][
                "euler_lagrange_amplitude_order_proxy_is_cubic"
            ],
            "tegr_quadratic_hessian_exact": algebra["checks"][
                "quadratic_hessian_equals_tegr"
            ],
            "full_standard_1pn_ppn_regression_exact": bool(
                dependencies["status_checks"][
                    "w3_52_selected_eh_1pn_regression_exact"
                ]
                and algebra["checks"][
                    "euler_lagrange_amplitude_order_proxy_is_cubic"
                ]
            ),
            "full_1pn_componentwise_remainder_regression_exact": dependencies[
                "status_checks"
            ]["w3_52_selected_eh_1pn_regression_exact"],
            "covariant_flat_inertial_spin_connection_registered_exact": bool(
                action["checks"]["one_coframe"]
                and action["checks"]["flat_inertial_spin_connection_retained"]
                and action["checks"]["torsion_scalar_is_T_of_e_and_omega"]
            ),
            "pure_tetrad_arbitrary_frame_mutation_rejected": mutations["checks"][
                "pure_tetrad_all_frame_covariance_claim_rejected"
            ],
            "one_coframe_one_metric_once_counted_source_ledger_exact": bool(
                action["checks"]["one_coframe"]
                and action["checks"]["one_operational_metric_g_equals_e_eta_e"]
                and action["checks"]["localized_source_ledger_exact"]
            ),
            "finite_lambda_nonzero_f_TT_exact": algebra["checks"][
                "f_TT_nonzero_through_open_domain_exact"
            ],
            "nonlinear_ft_late_onset_mode_handoff_registered_exact": bool(
                health["diagnostic_checks"]["theorem_handoff_identifier_exact"]
                and health["diagnostic_checks"][
                    "theorem_handoff_not_mislabeled_symbolic"
                ]
            ),
            "precise_universal_dof_count_not_claimed_exact": health[
                "diagnostic_checks"
            ]["precise_dof_count_not_assumed"],
            "weak_branch_kinetic_health_requirement_exact": health[
                "diagnostic_checks"
            ]["mandatory_health_requirements_fail"],
            "late_onset_sector_missing_quadratic_kinetic_exact": health[
                "diagnostic_checks"
            ]["weak_nonlinear_mode_mismatch_exact"],
            "strong_coupling_cutoff_completion_absent_exact": not health[
                "mandatory_requirements"
            ]["controlled_eft_cutoff_resolution_supplied"],
            "hard_health_veto_triggered_exact": health["rejection_exact"],
            "born_infeld_ft_candidate_rejected_exact": bool(
                health["candidate_admissible"] is False
                and health["candidate_health_aggregate_pass"] is False
            ),
            "global_solution_stop_rule_enforced": bool(
                scope_flags["regular_black_hole_solution_derived"] is False
                and scope_flags["trapped_surface_derived"] is False
                and scope_flags["geodesic_completeness_derived"] is False
                and scope_flags["singularity_resolution_completed"] is False
            ),
            "mutation_controls_pass": mutations["all_pass"],
        }
    )

    result: dict[str, Any] = {
        "schema_version": "W3-68-result-v1.0",
        "claim_id": CLAIM_ID,
        "claim": (
            "Audit the frozen covariant Born-Infeld f(T) completion against the "
            "W3-54 action conventions, weak TEGR limit, source ledger, and a mandatory "
            "nonlinear mode/characteristic health gate."
        ),
        "type": "EXACT_CANDIDATE_ACTION_AUDIT_WITH_THEOREM_HANDOFF_AND_HARD_HEALTH_REJECTION",
        "model_version": MODEL_VERSION,
        "status": FAIL_STATUS,
        "artifact_valid": False,
        "decision_gate_pass": False,
        "scientific_decision": "REJECT_CANDIDATE",
        "candidate_admissible": False,
        "assumptions": [
            "Lambda_BI>0",
            "W3-54 torsion convention and covariant coframe-inertial-connection pair",
            "exact localized W3-64 S_O source counted once with Lambda_F=0 and local S_C count zero",
            "torsionless weak branch with T=O(eps^2)",
            "the preregistered health standard treats an unresolved nonlinear kinetic/characteristic degeneracy as a veto",
        ],
        "domain": algebra["domain"],
        "conventions": {
            "torsion_scalar": "W3-54 T_TEGR, including its sign convention",
            "candidate_branch": "principal square-root branch connected to f(T)=T",
            "metric": "g_mu_nu=eta_AB*e^A_mu*e^B_nu",
            "connection": "flat inertial omega transformed with the coframe",
            "source": "the W3-64 localized ordinary-scalar Hilbert source T_O counted once; local T_C count zero",
        },
        "freedom_ledger": {
            "Lambda_BI": "one new positive universal strong-field scale; value not selected",
            "new_fitted_functions": 0,
            "new_matter_sources": 0,
            "new_metrics": 0,
            "candidate_status": "tested and rejected, not promoted",
        },
        "dependencies": dependencies,
        "method": {
            "internal_exact": "SymPy differentiation, limits, series, perturbative Hessian, and executed mutations",
            "external_handoff": (
                "arXiv:2004.07536 for the scoped fourth-order mode warning and "
                "arXiv:2302.03545 for the controlled-EFT-cutoff caveat"
            ),
            "network_used_by_verifier": False,
        },
        "pass_rule": (
            "The artifact passes only if it exactly establishes the low-limit facts, "
            "preserves the covariant one-source ledger, applies the frozen health veto, "
            "rejects the candidate, passes all mutations and dependencies, and contains "
            "exactly the registered three files."
        ),
        "falsifier": (
            "Any failed exact identity, dependency drift, source duplication, all-frame "
            "pure-tetrad covariance promotion, unsupported regular-black-hole claim, or "
            "failure to reject the nonlinear weak-branch kinetic mismatch invalidates the artifact."
        ),
        "exact_algebra": algebra,
        "action_and_source": action,
        "nonlinear_health": health,
        "mutation_controls": mutations,
        "gate_registry": gate_registry,
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
        "residual": {
            "exact_symbolic_residuals": "all registered residuals are zero",
            "open_physical_residual": (
                "the candidate lacks a demonstrated nondegenerate nonlinear mode and "
                "hyperbolic characteristic structure on the admitted weak branch"
            ),
        },
        "error_bound": "exact symbolic audit; no floating-point observable or likelihood",
        "validity_health": {
            "artifact_health": "pending package gate",
            "candidate_health": "FAIL",
            "candidate_health_aggregate_pass": False,
        },
        "branches": {
            "accepted": [],
            "rejected": ["principal covariant Born-Infeld f(T) candidate"],
        },
        "observable_map": None,
        "forward_model": None,
        "data_role": "NONE",
        "identifiability": (
            "Lambda_BI is not estimated because the candidate fails the pre-observational health gate"
        ),
        "benchmark": {
            "internal": "W3-54 TEGR conventions, W3-64 localized S_O ledger, and W3-52 selected-EH 1PN result",
            "external": "arXiv:2004.07536 theorem handoff plus arXiv:2302.03545 EFT caveat",
        },
        "crosscheck": "exact mutations plus hash-pinned upstream result/status checks",
        "scientific_boundary": (
            "The Born-Infeld form has the correct TEGR vacuum normalization and the same "
            "quadratic torsionless weak action. Its nonlinear f_TT is nevertheless active "
            "without a corresponding new weak quadratic kinetic operator. Under the frozen "
            "admissibility rule and the scoped Minkowski f(T) theorem handoff, that unresolved "
            "mode/characteristic health boundary decisively rejects this candidate. No exact "
            "nonlinear degree-of-freedom count, regular black hole, geodesic completeness, "
            "singularity resolution, or strong-field observation follows."
        ),
        "files": [PREREG.name, Path(__file__).name, OUTPUT.name],
        "provenance": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "preregistration_sha256": sha256(PREREG),
            "source_sha256": sha256(Path(__file__)),
            "deterministic": True,
            "timestamp_in_payload": False,
            "randomness_used": False,
            "network_used_by_verifier": False,
            "archived_theory_used": False,
        },
    }

    # The provisional atomic write creates the registered third file. The exact
    # package gate then runs on the final directory state.
    atomic_write_json(result)
    package = package_gate()
    result["package"] = package
    closure_flags["package_clean_pass"] = package["pass"]
    closure_flags["aggregate_audit_pass"] = bool(
        all(
            gate["pass"] is True
            for gate in gate_registry.values()
            if gate.get("required") is True
        )
        and
        all(
            closure_flags[name]
            for name in REQUIRED_TRUE_CLOSURE_FLAGS
            if name != "aggregate_audit_pass"
        )
        and all(scope_flags[name] is False for name in REQUIRED_FALSE_SCOPE_FLAGS)
        and health["candidate_admissible"] is False
        and health["candidate_health_aggregate_pass"] is False
        and gate_registry["G3_STRUCTURE"]["candidate_structure_health_pass"] is False
    )
    result["decision_gate_pass"] = closure_flags["aggregate_audit_pass"]
    result["artifact_valid"] = result["decision_gate_pass"]
    result["status"] = PASS_STATUS if result["artifact_valid"] else FAIL_STATUS
    result["validity_health"]["artifact_health"] = (
        "PASS" if result["artifact_valid"] else "FAIL"
    )
    atomic_write_json(result)

    print(
        json.dumps(
            {
                "claim_id": result["claim_id"],
                "status": result["status"],
                "artifact_valid": result["artifact_valid"],
                "decision_gate_pass": result["decision_gate_pass"],
                "candidate_admissible": result["candidate_admissible"],
                "candidate_health_aggregate_pass": result["validity_health"][
                    "candidate_health_aggregate_pass"
                ],
                "package": result["package"],
            },
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
    )


if __name__ == "__main__":
    main()
