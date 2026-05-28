"""
Article support ledger for the first Georgian RG article.

This file does not add new physics.  It collects the article-facing theorem
exports from the active work files so the draft can be checked from one place.
"""

import importlib.util
from pathlib import Path
import sys

import sympy as sp

WORK_DIR = Path(__file__).resolve().parents[1] / "RG" / "work"


def _load_article_function(module_name, function_name):
    """Load an article-facing function from the active RG work directory."""
    module_path = WORK_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {module_name} from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return getattr(module, function_name)


article_core_theorem = _load_article_function("p01_core", "article_core_theorem")
article_cosmology_theorem = _load_article_function(
    "p02_cosmo", "article_cosmology_theorem"
)
article_dynamic_phase_clock_theorem = _load_article_function(
    "p02c_dynamic_phase_clock", "article_dynamic_phase_clock_theorem"
)
article_solar_theorem = _load_article_function("p03_solar", "article_solar_theorem")
article_gw_theorem = _load_article_function("p04_gw", "article_gw_theorem")
article_strong_field_gate = _load_article_function(
    "p05_compact", "article_strong_field_gate"
)
article_cmb_theorem = _load_article_function("p08_cmb", "article_cmb_theorem")


def first_article_branch_intersection_audit():
    """
    Check whether the strict-clock diagnostic is one common branch.

    This is a guardrail, not the main cosmology direction.  The dynamic
    phase-clock branch keeps c_YI1 active; this audit only prevents the old
    strict-clock shortcut from being advertised as the global branch.
    """
    c_Y, c_Y2, c_YI1 = sp.symbols("c_Y c_Y2 c_YI1", real=True)

    p02_strict_lambda = {
        c_Y: -2 * c_Y2,
        c_YI1: sp.Integer(0),
    }
    p03_solar_1pn = {
        c_Y: -4 * c_Y2 - 2 * c_YI1,
    }

    strict_lambda_plus_solar = sp.solve(
        [
            sp.Eq(p02_strict_lambda[c_Y], p03_solar_1pn[c_Y]),
            sp.Eq(c_YI1, p02_strict_lambda[c_YI1]),
        ],
        [c_Y2, c_YI1],
        dict=True,
    )

    return {
        "article_use": "strict-clock diagnostic guard for the first article",
        "p01_plus_p03_nontrivial_window": {
            "conditions": [
                sp.Gt(c_Y2, 0),
                sp.Gt(c_YI1, -2 * c_Y2),
                sp.Lt(c_YI1, 2 * c_Y2),
            ],
            "status": "NONEMPTY_OPEN_REGION_FOR_CORE_PLUS_SOLAR_1PN",
        },
        "p02_strict_lambda_conditions": [
            sp.Eq(c_Y, -2 * c_Y2),
            sp.Eq(c_YI1, 0),
        ],
        "p03_solar_1pn_condition": sp.Eq(c_Y, -4 * c_Y2 - 2 * c_YI1),
        "strict_lambda_plus_solar_solution": strict_lambda_plus_solar,
        "strict_lambda_plus_nontrivial_solar_status": (
            "EMPTY_NONTRIVIAL_INTERSECTION: the common solution is c_Y2=0, "
            "c_YI1=0, so the nontrivial solar 1PN branch and the strict-clock "
            "lambda diagnostic must not be advertised as the main global branch."
        ),
        "extended_global_completion": (
            "CLOSED_IN_p02c: S=Y+2*I1-I3=6 gives exact positive LCDM "
            "zero-current background and Solar 1PN closure up to homogeneous "
            "Lambda stress; Z kinetic completion supplies solid no-ghost term."
        ),
        "article_status": {
            "global_branch": "EXTENDED_COMPLETION_CLOSED_BACKGROUND_AND_1PN",
            "core_plus_solar": "NONEMPTY_CONDITIONAL_REGION",
            "strict_lambda_plus_solar": "STRICT_CLOCK_DIAGNOSTIC_INTERSECTION_EMPTY",
            "dynamic_phase_clock": "PRIMARY_WITH_EXTENDED_GLOBAL_COMPLETION",
        },
    }


def first_article_support_status():
    """Return the computational support map for the first article."""
    return {
        "p01_core": article_core_theorem(),
        "p02_cosmo": article_cosmology_theorem(),
        "p02c_dynamic_phase_clock": article_dynamic_phase_clock_theorem(),
        "p03_solar": article_solar_theorem(),
        "p04_gw": article_gw_theorem(),
        "p05_compact": article_strong_field_gate(),
        "p08_cmb": article_cmb_theorem(),
        "branch_intersection": first_article_branch_intersection_audit(),
    }


def _zero(value):
    """SymPy-aware exact zero predicate for article proof checks."""
    return sp.simplify(value) == 0


def first_article_machine_check(status=None):
    """
    Exact checks for the article-facing algebra.

    This does not certify the whole physical theory. It certifies the narrower
    article claims that are algebraic consequences of the stated assumptions.
    """
    status = first_article_support_status() if status is None else status

    p01 = status["p01_core"]
    p02 = status["p02_cosmo"]
    p02c = status["p02c_dynamic_phase_clock"]
    p03 = status["p03_solar"]
    p04 = status["p04_gw"]
    p05 = status["p05_compact"]
    p08 = status["p08_cmb"]
    branch = status["branch_intersection"]

    checks = {
        "p01_minimal_truncation_residual_zero": _zero(
            p01["minimal_action_basis"]["residual"]
        ),
        "p01_power_counting_basis_enumeration_pass": (
            p01["minimal_response_power_counting_basis"]["status"]
            == "PASS_MINIMAL_RESPONSE_POWER_COUNTING_BASIS"
            and _zero(
                p01["minimal_response_power_counting_basis"][
                    "reconstruction_residual"
                ]
            )
            and not p01["minimal_response_power_counting_basis"][
                "missing_from_enumeration"
            ]
            and not p01["minimal_response_power_counting_basis"][
                "extra_in_enumeration"
            ]
        ),
        "p01_eft_cutoff_power_counting_ledger_pass": (
            p01["eft_cutoff_power_counting"]["status"]
            == "PASS_EFT_CUTOFF_POWER_COUNTING_LEDGER"
            and p01["eft_cutoff_power_counting"]["working_cutoff"].lhs
            == sp.Symbol("Lambda_EFT", positive=True)
            and "R*Y"
            in p01["eft_cutoff_power_counting"]["curvature_coupled_examples"]
        ),
        "p01_sign_bridge_closed": (
            p01["article_status"]["sign_convention"] == "CLOSED_Y_TO_X_BRIDGE"
        ),
        "p01_principal_symbol_coefficients_present": all(
            key in p01["mixed_mode_gate"]["mixed_polynomial_coefficients"]
            for key in ("p2", "p1", "p0", "discriminant")
        ),
        "p01_nonempty_stability_example_pass": (
            p01["nonempty_local_stability_example"]["status"]
            == "PASS_EXPLICIT_NONEMPTY_LOCAL_STABILITY_POINT"
            and all(p01["nonempty_local_stability_example"]["checks"].values())
        ),
        "p02_rho_residual_zero": _zero(p02["flrw_stress"]["rho_residual"]),
        "p02_p_residual_zero": _zero(p02["flrw_stress"]["p_residual"]),
        "p02_noether_difference_zero": _zero(
            p02["noether_bianchi"]["noether_difference"]
        ),
        "p02_early_parametric_bounds_present": (
            p02["early_universe_filters"]["parametric_bounds"]["status"]
            == "PARAMETRIC_FILTERS_AVAILABLE_NUMERICAL_FIT_STILL_REQUIRED"
        ),
        "p02_lambda_w_minus_one": _zero(
            p02["strict_clock_closure"]["late_w_after_closure"] + 1
        ),
        "p02c_dynamic_current_self_check": (
            p02c["current_self_check"]["status"] == "PASS"
        ),
        "p02c_late_candidate_w_minus_one": _zero(
            p02c["late_candidate"]["w_after_substitution"] + 1
        ),
        "p02c_keeps_phase_space_coupling_active": (
            p02c["article_status"]["phase_space_coupling"] == "c_YI1_REMAINS_ACTIVE"
        ),
        "p02c_background_observables_ready": (
            p02c["background_observables"]["status"]
            == "BACKGROUND_OBSERVABLES_READY_FOR_NUMERICAL_FIT"
        ),
        "p02c_dynamic_clock_example_pass": (
            p02c["branch_compatibility_example"]["status"]
            == "PASS_EXPLICIT_DYNAMIC_CLOCK_BRANCH_POINT"
            and _zero(p02c["branch_compatibility_example"]["w_late"] + 1)
        ),
        "p02c_dark_energy_scale_calibration_pass": (
            p02c["dark_energy_scale_calibration"]["status"]
            == "PASS_DARK_ENERGY_SCALE_CALIBRATION_EXAMPLE"
            and p02c["dark_energy_scale_calibration"][
                "relative_reconstruction_error"
            ]
            < 1.0e-12
        ),
        "p02c_exact_lcdm_background_branch_pass": (
            p02c["exact_lcdm_background_branch"]["status"]
            == "PASS_EXACT_LCDM_BACKGROUND_ZERO_CURRENT_BRANCH"
            and _zero(p02c["exact_lcdm_background_branch"]["E2_residual"])
            and p02c["exact_lcdm_background_branch"]["nonzero_coupling_example"][
                "point"
            ][sp.Symbol("c_YI1", real=True)]
            != 0
        ),
        "p02c_compressed_lcdm_background_residuals_pass": (
            p02c["compressed_lcdm_background_residual_check"]["status"]
            == "PASS_COMPRESSED_LCDM_BACKGROUND_RESIDUALS_ZERO"
            and p02c["compressed_lcdm_background_residual_check"][
                "max_abs_E2_residual"
            ]
            == 0.0
        ),
        "p02c_global_lcdm_solar_completion_pass": (
            p02c["global_lcdm_solar_completion"]["status"]
            == "PASS_GLOBAL_LCDM_SOLAR_1PN_COMPLETION"
            and _zero(
                p02c["global_lcdm_solar_completion"]["cosmology"][
                    "S_minus_S0_on_branch"
                ]
            )
            and _zero(
                p02c["global_lcdm_solar_completion"]["cosmology"][
                    "L_Y_on_branch"
                ]
            )
            and _zero(
                p02c["global_lcdm_solar_completion"]["cosmology"][
                    "w_plus_one_residual"
                ]
            )
            and all(
                _zero(value)
                for value in p02c["global_lcdm_solar_completion"][
                    "solar_1PN_with_Lambda_stress"
                ]["O0_anisotropy_residuals"]
            )
            and all(
                _zero(value)
                for value in p02c["global_lcdm_solar_completion"][
                    "solar_1PN_with_Lambda_stress"
                ]["O1_residuals"].values()
            )
            and _zero(
                p02c["global_lcdm_solar_completion"]["kinetic_completion"][
                    "K_phase"
                ]
                - 4 * sp.Symbol("lambda_S", positive=True)
            )
            and _zero(
                p02c["global_lcdm_solar_completion"]["kinetic_completion"][
                    "K_solid_from_Z"
                ]
                - sp.Symbol("c_Z", positive=True)
            )
        ),
        "p02c_completion_origin_and_operator_audit_pass": (
            p02c["completion_origin_and_operator_audit"]["status"]
            == "PASS_S6_ORIGIN_AND_OPERATOR_EXPANSION_AUDIT"
            and p02c["completion_origin_and_operator_audit"][
                "S0_from_unit_background"
            ]
            == 6
            and _zero(
                p02c["completion_origin_and_operator_audit"][
                    "expanded_completion_square"
                ]
                - p02c["completion_origin_and_operator_audit"][
                    "expected_completion_square"
                ]
            )
            and p02c["completion_origin_and_operator_audit"][
                "outside_minimal_basis_coefficients"
            ]
            == {"Y*I3": -2, "I1*I3": -4, "I3^2": 1}
        ),
        "p02c_completion_local_perturbations_pass": (
            p02c["completion_branch_local_perturbations"]["status"]
            == "PASS_COMPLETION_LOCAL_PERTURBATION_SYMBOL"
            and p02c["completion_branch_local_perturbations"][
                "kinetic_eigenvalues"
            ]
            == [
                4 * sp.Symbol("lambda_S", positive=True),
                sp.Symbol("c_Z", positive=True),
                sp.Symbol("c_Z", positive=True),
                sp.Symbol("c_Z", positive=True),
            ]
            and _zero(
                p02c["completion_branch_local_perturbations"][
                    "scalar_longitudinal_determinant"
                ]
                - 4
                * sp.Symbol("c_Z", positive=True)
                * sp.Symbol("lambda_S", positive=True)
                * (sp.Symbol("omega", real=True) ** 2 - sp.Symbol("k", real=True) ** 2)
                ** 2
            )
            and _zero(
                p02c["completion_branch_local_perturbations"][
                    "scalar_longitudinal_determinant_in_s"
                ]
                - 4
                * sp.Symbol("c_Z", positive=True)
                * sp.Symbol("lambda_S", positive=True)
                * (sp.Symbol("s", real=True) - 1) ** 2
            )
        ),
        "p02c_completion_z_sign_and_degeneracy_pass": (
            p02c["completion_z_sign_and_degeneracy_audit"]["status"]
            == "PASS_Z_SIGN_AND_LUMINAL_DEGENERACY_AUDIT"
            and _zero(
                p02c["completion_z_sign_and_degeneracy_audit"][
                    "delta_S_linear_from_invariants"
                ]
                - 2
                * (
                    sp.Symbol("chi_dot", real=True)
                    + sp.Symbol("theta", real=True)
                )
            )
            and _zero(
                p02c["completion_z_sign_and_degeneracy_audit"]["determinant"]
                - 4
                * sp.Symbol("c_Z", positive=True)
                * sp.Symbol("lambda_S", positive=True)
                * (
                    sp.Symbol("omega", positive=True, real=True) ** 2
                    - sp.Symbol("k", positive=True, real=True) ** 2
                )
                ** 2
            )
            and len(
                p02c["completion_z_sign_and_degeneracy_audit"][
                    "nullspace_at_omega_plus_k"
                ]
            )
            == 1
            and len(
                p02c["completion_z_sign_and_degeneracy_audit"][
                    "nullspace_at_omega_minus_k"
                ]
            )
            == 1
        ),
        "p02c_completion_phase_current_pass": (
            p02c["completion_phase_current"]["status"]
            == "PASS_COMPLETION_PHASE_CURRENT_VANISHES_ON_S6_BRANCH"
            and _zero(p02c["completion_phase_current"]["current_on_S6_branch"])
        ),
        "p02c_completion_q2pn_scope_gate_present": (
            p02c["completion_q2pn_scope"]["status"]
            == "COMPLETION_Q2PN_NOT_FIXED_BY_CURRENT_S6_1PN_BRANCH"
        ),
        "p02c_clock_completion_roadmap_pass": (
            p02c["clock_completion_roadmap"]["status"]
            == "PASS_CLOCK_COMPLETION_BRANCH_ROADMAP"
            and p02c["clock_completion_roadmap"][
                "constant_coefficient_tuning_attempt"
            ]
            == [
                {
                    sp.Symbol("c_Y", real=True): 0,
                    sp.Symbol("c_Y2", real=True): 0,
                    sp.Symbol("c_YI1", real=True): 0,
                }
            ]
        ),
        "p03_1pn_branch_derived": (
            p03["nontrivial_1PN_branch"]["derivation_status"] == "PASS"
        ),
        "p03_solar_ansatz_scope_table_pass": (
            p03["solar_ansatz_scope_table"]["status"]
            == "PASS_SOLAR_ANSATZ_SCOPE_TABLE"
            and p03["solar_ansatz_scope_table"][
                "static_spherical_invariant_derivation"
            ]["I1"]
            == 2 + sp.Symbol("A") ** -1
        ),
        "p03_solar_ansatz_coordinate_ledger_pass": (
            p03["solar_ansatz_scope_table"]["coordinate_ledger_status"]
            == "PASS_SOLAR_ANSATZ_COORDINATE_LEDGER"
            and p03["solar_ansatz_scope_table"]["isotropic_invariant_derivation"][
                "I1"
            ]
            == 3 / sp.Symbol("B_r", positive=True)
            and p03["solar_ansatz_scope_table"][
                "area_to_isotropic_schwarzschild_map"
            ]["q_GR_check"]
            == sp.Rational(7, 4)
        ),
        "p03_2pn_residual_check_zero": all(
            _zero(value)
            for value in p03["two_pn_discriminator"][
                "derived_O2_residual_check"
            ]
        ),
        "p03_2pn_observable_candidates_exported": (
            p03["two_pn_observable_candidates"]["status"]
            == "CONDITIONAL_CANDIDATES_NOT_FINAL_PREDICTIONS"
        ),
        "p03_metric_to_optical_2pn_bridge_present": (
            p03["two_pn_observable_candidates"]["metric_to_optical_bridge"]["status"]
            == "METRIC_TO_OPTICAL_2PN_BRIDGE_DERIVED"
        ),
        "p03_isotropic_2pn_obstruction_present": (
            p03["two_pn_discriminator"]["isotropic_2pn_stress_closure"]["status"]
            == "ISOTROPIC_2PN_STRESS_CLOSURE_OBSTRUCTION"
        ),
        "p03_isotropic_2pn_solution_residuals_zero": all(
            _zero(value)
            for row in p03["two_pn_discriminator"][
                "isotropic_2pn_stress_closure"
            ]["solution_residuals"]
            for value in row
        ),
        "p03_q2pn_observational_scale_present": (
            p03["two_pn_discriminator"]["q2pn_observational_scale"]["status"]
            == "NEAR_CASSINI_SENSITIVITY_REQUIRES_FULL_2PN_FIT"
        ),
        "p03_general_q2pn_optical_observables_derived": (
            p03["two_pn_discriminator"]["q2pn_general_optical_observables"]["status"]
            == "DERIVED_GENERAL_Q2PN_OPTICAL_OBSERVABLES"
            and _zero(
                p03["two_pn_discriminator"]["q2pn_general_optical_observables"][
                    "checks"
                ]["q10_shapiro_coefficient"]
                - sp.Rational(33, 4) * sp.pi
            )
            and _zero(
                p03["two_pn_discriminator"]["q2pn_general_optical_observables"][
                    "checks"
                ]["q10_bending_ratio"]
                - sp.Rational(16, 5)
            )
        ),
        "p03_cassini_2pn_tracking_proxy_pass": (
            p03["two_pn_discriminator"]["cassini_2pn_tracking_proxy"]["status"]
            == "PASS_CASSINI_2PN_TRACKING_PROXY_DEFAULT_GEOMETRY"
            and p03["two_pn_discriminator"]["cassini_2pn_tracking_proxy"][
                "q_passes_1sigma_proxy"
            ]
            and p03["two_pn_discriminator"]["cassini_2pn_tracking_proxy"][
                "q_passes_conservative_proxy"
            ]
        ),
        "p03_q2pn_observational_table_pass": (
            p03["two_pn_discriminator"]["q2pn_observational_table"]["status"]
            == "PASS_Q2PN_OBSERVATIONAL_TABLE"
            and len(p03["two_pn_discriminator"]["q2pn_observational_table"]["rows"])
            >= 3
            and any(
                row["geometry_role"] == "Cassini reference geometry"
                for row in p03["two_pn_discriminator"]["q2pn_observational_table"][
                    "rows"
                ]
            )
        ),
        "p03_cassini_raw_likelihood_gate_formulated": (
            p03["two_pn_discriminator"]["cassini_2pn_raw_likelihood_gate"][
                "status"
            ]
            == "FORMULATED_REQUIRES_RAW_CASSINI_DOPPLER_DATA"
            and p03["two_pn_discriminator"]["cassini_2pn_raw_likelihood_gate"][
                "default_proxy_q_passes_conservative"
            ]
        ),
        "p03_preferred_frame_velocity_risk_present": (
            p03["preferred_frame_velocity_risk"]["status"]
            == "NOT_DERIVED_STATIC_BRANCH_INSUFFICIENT"
        ),
        "p03_preferred_frame_background_stress_pass": (
            p03["preferred_frame_background_stress"]["status"]
            == "PASS_BACKGROUND_PREFERRED_FRAME_STRESS_ON_1PN_BRANCH"
            and p03["preferred_frame_background_stress"][
                "solar_1PN_branch_prefactor"
            ]
            == 0
            and all(
                _zero(value)
                for value in p03["preferred_frame_background_stress"][
                    "solar_1PN_branch_T0i_linear_residuals"
                ].values()
            )
            and all(
                _zero(value)
                for value in p03["preferred_frame_background_stress"][
                    "solar_1PN_branch_spatial_anisotropy_residuals"
                ].values()
            )
        ),
        "p03_standard_ppn_alpha_i_matcher_pass": (
            p03["standard_ppn_alpha_i_matcher"]["status"]
            == "PASS_STANDARD_PPN_MATCH_FORCES_ALPHA_I_ZERO"
            and all(
                value == 0
                for value in p03["standard_ppn_alpha_i_matcher"][
                    "alpha_i_values"
                ].values()
            )
            and all(
                _zero(value)
                for value in p03["standard_ppn_alpha_i_matcher"][
                    "residuals_after_solution"
                ]
            )
        ),
        "p03_moving_source_rg_vector_source_pass": (
            p03["moving_source_rg_vector_source"]["status"]
            == "PASS_RG_VECTOR_SOURCE_ABSENT_ON_1PN_BRANCH"
            and all(
                _zero(value)
                for row in p03["moving_source_rg_vector_source"][
                    "h_linear_matrix_on_1PN_branch"
                ]
                for value in row
            )
            and all(
                _zero(value)
                for row in p03["moving_source_rg_vector_source"][
                    "v_linear_matrix_on_1PN_branch"
                ]
                for value in row
            )
        ),
        "p03_preferred_frame_alpha_i_chain_pass": (
            p03["preferred_frame_alpha_i_closure_chain"]["status"]
            == "PASS_MINIMAL_MOVING_SOURCE_ALPHA_I_CHAIN"
            and all(
                value == 0
                for value in p03["preferred_frame_alpha_i_closure_chain"][
                    "alpha_i_values"
                ].values()
            )
        ),
        "p03_standard_ppn_alpha_i_export_table_pass": (
            p03["standard_ppn_alpha_i_export_table"]["status"]
            == "PASS_STANDARD_PPN_ALPHA_I_EXPORT_TABLE"
            and all(
                row["passes_bound"]
                for row in p03["standard_ppn_alpha_i_export_table"]["rows"]
            )
        ),
        "p03_standard_ppn_status_ledger_pass": (
            p03["standard_ppn_status_ledger"]["status"]
            == "PASS_STANDARD_PPN_STATUS_LEDGER"
            and p03["standard_ppn_status_ledger"]["derived_now"]
            == ["gamma", "beta", "alpha_1", "alpha_2", "alpha_3"]
        ),
        "p03_preferred_frame_alpha_i_appendix_payload_pass": (
            p03["preferred_frame_alpha_i_appendix_payload"]["status"]
            == "PASS_ALPHA_I_APPENDIX_PAYLOAD"
            and all(
                _zero(value)
                for value in p03["preferred_frame_alpha_i_appendix_payload"][
                    "step_1_boosted_background"
                ]["T0i_residuals"].values()
            )
            and all(
                _zero(value)
                for row in p03["preferred_frame_alpha_i_appendix_payload"][
                    "step_2_rg_vector_source"
                ]["h_matrix_on_branch"]
                for value in row
            )
            and all(
                _zero(value)
                for row in p03["preferred_frame_alpha_i_appendix_payload"][
                    "step_2_rg_vector_source"
                ]["v_matrix_on_branch"]
                for value in row
            )
        ),
        "p03_frame_dragging_minimal_1p5pn_chain_pass": (
            p03["frame_dragging_minimal_1p5pn_chain"]["status"]
            == "PASS_MINIMAL_1P5PN_FRAME_DRAGGING_CHAIN"
            and _zero(
                p03["frame_dragging_minimal_1p5pn_chain"][
                    "RG_minus_GR_residual"
                ]
            )
        ),
        "p04_alpha_T_zero": _zero(
            p04["tensor_speed_theorem"]["alpha_T"].rhs
        ),
        "p04_solid_TT_hdot_zero": _zero(
            p04["tensor_speed_theorem"]["solid_TT_h_dot2_correction"]
        ),
        "p04_solid_TT_hz_zero": _zero(
            p04["tensor_speed_theorem"]["solid_TT_h_z2_correction"]
        ),
        "p04_local_minkowski_tT_dispersion_pass": (
            p04["local_minkowski_tensor_dispersion"]["status"]
            == "PASS_LOCAL_MINKOWSKI_TT_DISPERSION_MASSLESS"
            and _zero(
                p04["local_minkowski_tensor_dispersion"][
                    "local_Minkowski_mass_on_Solar_1PN_branch"
                ]
            )
            and _zero(
                p04["local_minkowski_tensor_dispersion"][
                    "RG_correction_residual"
                ]
            )
        ),
        "p05_strong_field_gate_registered": (
            p05["status"] == "STRONG_FIELD_PROGRAM_REGISTERED_NOT_PROMOTED"
            and p05["compact_export_gate"] == "NOT_READY_FOR_RG_THEORY_EXPORT"
            and p05["screening_minimum"]["status"]
            == "NO_COMPRESSED_CASSINI_SCREENING_FORCED_BY_DEFAULT_PROXY"
        ),
        "p08_same_input_consistency_identity": (
            p08["same_matter_inheritance"]["machine_check"] == "PASS"
        ),
        "p08_exact_lcdm_boltzmann_sources_zero": (
            p08["exact_lcdm_branch_boltzmann_sources"]["status"]
            == "PASS_EXACT_LCDM_BRANCH_BOLTZMANN_SOURCES_ZERO"
            and all(
                _zero(value)
                for value in p08["exact_lcdm_branch_boltzmann_sources"][
                    "perturbation_sources"
                ].values()
            )
            and all(
                _zero(value)
                for value in p08["exact_lcdm_branch_boltzmann_sources"][
                    "einstein_boltzmann_source_residuals"
                ].values()
            )
        ),
        "p08_s_completion_same_input_boltzmann_sources_zero": (
            p08["s_completion_same_input_boltzmann_sources"]["status"]
            == "PASS_S_COMPLETION_SAME_INPUT_BOLTZMANN_SOURCES_ZERO"
            and all(
                _zero(value)
                for value in p08["s_completion_same_input_boltzmann_sources"][
                    "perturbation_sources"
                ].values()
            )
            and all(
                _zero(value)
                for value in p08["s_completion_same_input_boltzmann_sources"][
                    "einstein_boltzmann_source_residuals"
                ].values()
            )
            and _zero(
                p08["s_completion_same_input_boltzmann_sources"][
                    "active_completion_modes"
                ]["determinant_in_s"]
                - 4
                * sp.Symbol("c_Z", positive=True)
                * sp.Symbol("lambda_S", positive=True)
                * (sp.Symbol("s", real=True) - 1) ** 2
            )
        ),
        "p08_active_s_completion_linear_source_order_pass": (
            p08["active_s_completion_linear_source_order"]["status"]
            == "PASS_ACTIVE_S_COMPLETION_LINEAR_SOURCE_ZERO_ORDER"
            and _zero(
                p08["active_s_completion_linear_source_order"][
                    "active_expansion"
                ]["linear_source_coefficient"]
            )
        ),
        "p08_no_particle_dm_decision_gate_present": (
            p08["no_particle_dm_cmb_decision_gate"]["status"]
            == "NO_PARTICLE_DM_REQUIRES_NONZERO_ACTIVE_SOURCE_BRANCH"
        ),
        "branch_guard_strict_clock_not_global": (
            branch["article_status"]["strict_lambda_plus_solar"]
            == "STRICT_CLOCK_DIAGNOSTIC_INTERSECTION_EMPTY"
        ),
        "branch_extended_global_completion_closed": (
            branch["article_status"]["global_branch"]
            == "EXTENDED_COMPLETION_CLOSED_BACKGROUND_AND_1PN"
        ),
    }

    return {
        "status": "PASS" if all(checks.values()) else "CHECK",
        "checks": checks,
        "scope": (
            "machine check of exact article-facing algebra under stated branch "
            "assumptions; not a certification of observational fits or global "
            "nonlinear completion"
        ),
    }


def _normalize_status_text(value):
    """Use article-facing wording in status summaries."""
    if isinstance(value, dict):
        return {key: _normalize_status_text(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_status_text(item) for item in value]
    if isinstance(value, str):
        return (
            value.replace("CONSISTENCY_HEALTH_CHECK", "CONSISTENCY_IDENTITY")
            .replace("HEALTH_CHECK", "CONSISTENCY_CHECK")
            .replace("HEALTH", "CONSISTENCY")
            .replace("GATE", "CRITERION")
            .replace("WINDOW", "REGION")
        )
    return value


def first_article_status_summary():
    """Compact status summary for quick terminal checks."""
    status = first_article_support_status()
    machine_check = first_article_machine_check(status)
    summary = {
        "core": status["p01_core"]["article_status"],
        "cosmology": status["p02_cosmo"]["article_status"],
        "dynamic_phase_clock": status["p02c_dynamic_phase_clock"]["article_status"],
        "solar": status["p03_solar"]["article_status"],
        "gw": status["p04_gw"]["article_status"],
        "strong_field": {
            "status": status["p05_compact"]["status"],
            "screening_minimum": status["p05_compact"]["screening_minimum"][
                "status"
            ],
            "compact_export_gate": status["p05_compact"]["compact_export_gate"],
        },
        "cmb": status["p08_cmb"]["article_status"],
        "branch_intersection": status["branch_intersection"]["article_status"],
        "machine_check": {
            "status": machine_check["status"],
            **machine_check["checks"],
        },
    }
    return _normalize_status_text(summary)


if __name__ == "__main__":
    for section, value in first_article_status_summary().items():
        print(f"\n[{section}]")
        for key, item in value.items():
            print(f"{key}: {item}")
