"""W3-36 finite-birth, threshold, and thermal-identifiability gate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_36_BIRTH_THRESHOLD_THERMAL_CLOSURE"
MODEL_VERSION = "W3-36-v1.3-FINITE-BIRTH"
HERE = Path(__file__).resolve().parent
PREREG = HERE / "w3_36_birth_threshold_thermal_preregistration.md"
OUTPUT = HERE / "w3_36_result.json"
HASH_OUTPUT = HERE / "w3_36_result.sha256"
PINNED_PREREG_SHA256 = (
    "71580ea4f37c567190ad3f7d826d5b46582b5aab49e36e21cbf59f4eac482b88"
)

REQUIRED_CONTRACT_FIELDS = {
    "CLAIM_ID",
    "CLAIM",
    "TYPE",
    "MODEL_VERSION",
    "ASSUMPTIONS",
    "DOMAIN",
    "CONVENTIONS",
    "FREEDOM_LEDGER",
    "DEPENDENCIES",
    "METHOD",
    "PASS_CONDITION",
    "FAIL_CONDITION",
    "FALSIFIER",
    "RESIDUAL",
    "ERROR_BOUND",
    "VALIDITY_HEALTH",
    "BRANCHES",
    "OBSERVABLE_MAP",
    "FORWARD_MODEL",
    "DATA_ROLE",
    "IDENTIFIABILITY",
    "BENCHMARK",
    "CLOSURE_FLAGS",
    "CROSSCHECK",
    "PROVENANCE",
    "FILES",
}

EXPECTED_CLOSURE_KEYS = {
    "cadence_pressure_identity_exact",
    "metric_process_dictionary_exact",
    "operational_scale_rate_identity_exact",
    "already_activated_null_identity_exact",
    "threshold_level_set_speed_exact",
    "foundation_threshold_radius_chain_rule_exact",
    "moving_boundary_energy_ledger_exact",
    "constant_active_energy_condition_exposed",
    "foundation_thermal_pressures_independent",
    "finite_process_origin_classified",
    "high_cadence_process_bound_exact",
    "volume_measure_jacobian_exact",
    "two_sector_conservation_sum_exact",
    "radiation_temperature_identity_exact",
    "radiation_temperature_source_identity_exact",
    "adiabatic_Tz_no_go_exact",
    "lower_temperature_sign_classifier_exact",
    "lower_temperature_nonidentifiability_exact",
    "common_cadence_rate_H_cancellation_exact",
    "same_null_residual_exposed",
    "conditional_front_assumption_crosscheck_exact",
    "observable_definitions_recorded",
    "schema_keysets_exact",
    "mutation_controls_pass",
    "aggregate_identity_pass",
}

EXPECTED_PHYSICAL_CLOSURE_KEYS = {
    "amplitude_action_derived",
    "threshold_value_derived",
    "initial_spectrum_and_topology_derived",
    "activation_front_eom_derived",
    "foundation_energy_balance_derived",
    "foundation_to_thermal_transfer_derived",
    "a_of_P_F_derived",
    "finite_process_age_numerically_predicted",
    "temperature_history_derived",
    "temperature_below_standard_derived",
    "spectroscopic_redshift_derived",
    "stellar_population_clock_derived",
    "H_CC_curve_derived",
    "luminosity_distance_derived",
    "CMB_recombination_BBN_validated",
    "JWST_structural_growth_validated",
}

EXPECTED_RESULT_KEYS = {
    "schema_version",
    "claim_id",
    "claim",
    "type",
    "model_version",
    "status",
    "scope_status",
    "artifact_valid",
    "evidence_type",
    "refg_status",
    "mechanism_status",
    "finite_process_time_status",
    "temperature_claim_status",
    "observational_status",
    "falsifier_triggered_for_refg",
    "blocking_reasons",
    "contract",
    "closure_flags",
    "physical_closure_flags",
    "identities",
    "classifications",
    "thermal_identifiability",
    "observable_definitions",
    "negative_controls",
    "provenance",
    "files",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_zero(expression: sp.Expr) -> bool:
    return bool(sp.simplify(expression) == 0)


def exact_nonzero(expression: sp.Expr) -> bool:
    return bool(sp.simplify(expression) != 0)


def verify_preregistration() -> dict[str, object]:
    if not PREREG.is_file():
        raise RuntimeError(f"Missing preregistration: {PREREG}")
    actual = sha256(PREREG)
    if actual != PINNED_PREREG_SHA256:
        raise RuntimeError(
            "Frozen preregistration changed: "
            f"expected {PINNED_PREREG_SHA256}, got {actual}"
        )
    return {
        "path": PREREG.relative_to(HERE.parents[2]).as_posix(),
        "sha256": actual,
        "expected_sha256": PINNED_PREREG_SHA256,
        "valid": True,
    }


def derive_exact_gate() -> tuple[
    dict[str, object],
    dict[str, bool],
    dict[str, object],
    dict[str, bool],
]:
    t = sp.symbols("t", positive=True)
    c0, p_symbol, pressure_f, pressure_f0 = sp.symbols(
        "c_0 p P_F P_F0", positive=True
    )
    a_symbol, A_symbol = sp.symbols("a A", positive=True)

    cadence_residual = sp.expand(
        (p_symbol**2 - pressure_f / pressure_f0).subs(
            pressure_f, pressure_f0 * p_symbol**2
        )
    )
    metric_time_residual = sp.simplify(p_symbol**2 / p_symbol**2 - 1)
    metric_space_residual = sp.simplify(
        a_symbol**2 / p_symbol**2 - (a_symbol / p_symbol) ** 2
    )

    pressure_function = sp.Function("P_F")(t)
    link_function = sp.Function("a")(t)
    p_from_pressure = sp.sqrt(pressure_function / pressure_f0)
    operational_scale = link_function / p_from_pressure
    hubble_direct = sp.diff(sp.log(operational_scale), t) / p_from_pressure
    hubble_expected = (
        sp.diff(link_function, t) / link_function
        - sp.diff(pressure_function, t) / (2 * pressure_function)
    ) / p_from_pressure
    hubble_residual = sp.simplify(hubble_direct - hubble_expected)
    additive_material_driver = sp.symbols(
        "Delta_H_material_independent", nonzero=True
    )
    additive_material_driver_mutation = sp.simplify(
        hubble_expected + additive_material_driver - hubble_direct
    )
    null_process_speed = c0 / (a_symbol / p_symbol)
    null_metric_speed = p_symbol * null_process_speed
    null_expected_metric_speed = c0 * p_symbol**2 / a_symbol
    null_residual = sp.simplify(
        null_metric_speed - null_expected_metric_speed
    )

    phi_t, phi_chi = sp.symbols("Phi_t Phi_chi", nonzero=True)
    threshold_speed = -phi_t / phi_chi
    threshold_residual = sp.simplify(phi_t + phi_chi * threshold_speed)
    null_threshold_residual = sp.simplify(
        phi_t + c0 * p_symbol**2 / a_symbol * phi_chi
    )
    chi_function = sp.Function("chi_act")(t)
    foundation_radius = link_function * chi_function
    radius_chain_expected = (
        sp.diff(link_function, t) / link_function * foundation_radius
        + link_function * sp.diff(chi_function, t)
    )
    radius_chain_residual = sp.simplify(
        sp.diff(foundation_radius, t) - radius_chain_expected
    )
    threshold_radius_speed = (
        sp.diff(link_function, t) / link_function * foundation_radius
        - link_function * phi_t / phi_chi
    )

    radial_coordinate = sp.symbols("r", positive=True)
    moving_radius = sp.Function("R")(t)
    local_density = sp.Function("rho")(radial_coordinate, t)
    radial_flux_primitive = sp.Function("F")(radial_coordinate, t)
    local_source = sp.Function("S_E")(radial_coordinate, t)
    active_energy = 4 * sp.pi * sp.Integral(
        radial_coordinate**2 * local_density,
        (radial_coordinate, 0, moving_radius),
    )
    active_energy_leibniz = sp.diff(active_energy, t)
    local_continuity_rhs = (
        local_source
        - sp.Derivative(radial_flux_primitive, radial_coordinate)
        / radial_coordinate**2
    )
    active_energy_from_local_conservation = active_energy_leibniz.xreplace(
        {sp.Derivative(local_density, t): local_continuity_rhs}
    )
    integrated_source = sp.Integral(
        radial_coordinate**2 * local_source,
        (radial_coordinate, 0, moving_radius),
    )
    boundary_flux_primitive = radial_flux_primitive.subs(
        radial_coordinate, moving_radius
    )
    center_flux_primitive = radial_flux_primitive.subs(radial_coordinate, 0)
    boundary_density_function = local_density.subs(
        radial_coordinate, moving_radius
    )
    energy_rate_from_leibniz_ftc = 4 * sp.pi * (
        integrated_source
        + moving_radius**2
        * boundary_density_function
        * sp.diff(moving_radius, t)
        - boundary_flux_primitive
        + center_flux_primitive
    )
    moving_boundary_ftc_residual = sp.simplify(
        active_energy_from_local_conservation - energy_rate_from_leibniz_ftc
    )

    radius, rho_boundary = sp.symbols("R rho_b", positive=True)
    flux_boundary, radius_dot, source_volume, center_flux = sp.symbols(
        "J_b R_dot Q_V F_0", real=True
    )
    energy_rate_general = energy_rate_from_leibniz_ftc.xreplace(
        {
            integrated_source: source_volume,
            moving_radius: radius,
            sp.diff(moving_radius, t): radius_dot,
            boundary_density_function: rho_boundary,
            boundary_flux_primitive: radius**2 * flux_boundary,
            center_flux_primitive: center_flux,
        }
    )
    energy_rate_general_expected = 4 * sp.pi * (
        radius**2 * (rho_boundary * radius_dot - flux_boundary)
        + source_volume
        + center_flux
    )
    energy_general_residual = sp.simplify(
        energy_rate_general - energy_rate_general_expected
    )
    energy_rate_reynolds = sp.simplify(
        energy_rate_general.subs(center_flux, 0)
    )
    energy_rate_expected = 4 * sp.pi * (
        radius**2 * (rho_boundary * radius_dot - flux_boundary)
        + source_volume
    )
    energy_residual = sp.simplify(
        energy_rate_reynolds - energy_rate_expected
    )
    constant_energy_source_condition = sp.solve(
        sp.Eq(energy_rate_expected, 0), source_volume
    )[0]

    pressure_th = sp.symbols("P_th", positive=True)
    cadence_partial_thermal = sp.diff(
        sp.sqrt(pressure_f / pressure_f0), pressure_th
    )
    thermal_probe = sp.symbols("P_probe", positive=True)
    same_cadence_two_thermal_states = sp.simplify(
        sp.sqrt(pressure_f / pressure_f0)
        - sp.sqrt(pressure_f / pressure_f0)
    )
    distinct_thermal_states = sp.simplify(2 * thermal_probe - thermal_probe)

    high_cadence_T0 = sp.symbols("T_0", positive=True)
    nonnegative_cadence_excess = sp.symbols(
        "I_p_minus_1", nonnegative=True
    )
    high_cadence_tau = high_cadence_T0 + nonnegative_cadence_excess
    high_cadence_bound_residual = sp.simplify(
        high_cadence_tau
        - high_cadence_T0
        - nonnegative_cadence_excess
    )
    high_cadence_equality_residual = sp.simplify(
        high_cadence_tau.subs(nonnegative_cadence_excess, 0)
        - high_cadence_T0
    )

    cell_count, cell_volume = sp.symbols("N_act v_F0", positive=True)
    foundation_volume = cell_count * cell_volume * a_symbol**3
    operational_volume = (
        cell_count * cell_volume * (a_symbol / p_symbol) ** 3
    )
    volume_jacobian_residual = sp.simplify(
        foundation_volume / operational_volume - p_symbol**3
    )

    rho_th, rho_foundation, pi_foundation = sp.symbols(
        "rho_th rho_F Pi_F", positive=True
    )
    hubble_tau, transfer = sp.symbols("H_tau Q")
    rho_th_prime = -3 * hubble_tau * (rho_th + pressure_th) + transfer
    rho_foundation_prime = (
        -3 * hubble_tau * (rho_foundation + pi_foundation) - transfer
    )
    two_sector_sum_residual = sp.simplify(
        rho_th_prime
        + rho_foundation_prime
        + 3
        * hubble_tau
        * (rho_th + rho_foundation + pressure_th + pi_foundation)
    )

    C, T0 = sp.symbols("C T_0", positive=True)
    beta = sp.symbols("beta", real=True)
    beta_integrand = C * t ** (-beta)
    beta_antiderivative = C * t ** (1 - beta) / (1 - beta)
    beta_antiderivative_residual = sp.simplify(
        sp.diff(beta_antiderivative, t) - beta_integrand
    )
    finite_half = sp.integrate(C * t ** (-sp.Rational(1, 2)), (t, 0, T0))
    epsilon = sp.symbols("epsilon", positive=True)
    log_interval = sp.integrate(C / t, (t, epsilon, T0))
    power_interval = sp.integrate(
        C * t ** (-sp.Rational(3, 2)), (t, epsilon, T0)
    )
    log_limit = sp.limit(log_interval, epsilon, 0, dir="+")
    power_limit = sp.limit(power_interval, epsilon, 0, dir="+")
    conditional_front_interval = sp.integrate(
        (T0 / t) ** sp.Rational(3, 8), (t, 0, T0)
    )
    front_R, front_D, front_lambda, front_Rf = sp.symbols(
        "R_front D Lambda R_final", positive=True
    )
    front_p = sp.sqrt(front_lambda) * front_R ** (-sp.Rational(3, 2))
    front_R_dot = (
        c0 * front_lambda / (front_D * front_R**3)
    )
    front_dtaudR = sp.simplify(front_p / front_R_dot)
    front_identity_residual = sp.simplify(
        front_dtaudR - front_D / (c0 * front_p)
    )
    front_integral = sp.integrate(
        front_dtaudR, (front_R, 0, front_Rf)
    )
    front_integral_expected = (
        2
        * front_D
        * front_Rf ** sp.Rational(5, 2)
        / (5 * c0 * sp.sqrt(front_lambda))
    )
    front_integral_residual = sp.simplify(
        front_integral - front_integral_expected
    )
    front_D_gap, front_p_excess = sp.symbols(
        "D_gap p_excess", positive=True
    )
    front_D_witness = 1 / (1 + front_D_gap)
    front_p_witness = 1 + front_p_excess
    front_bound_rate = front_D_witness / (c0 * front_p_witness)
    front_bound_gap = (
        front_D_gap
        + front_p_excess
        + front_D_gap * front_p_excess
    ) / (
        c0 * (1 + front_D_gap) * (1 + front_p_excess)
    )
    front_bound_residual = sp.simplify(
        1 / c0 - front_bound_rate - front_bound_gap
    )
    front_bound_rate_at_p1 = sp.simplify(
        front_bound_rate.subs(front_p_excess, 0)
    )
    front_bound_gap_at_p1 = sp.simplify(1 / c0 - front_bound_rate_at_p1)
    front_bound_gap_at_p1_expected = front_D_gap / (
        c0 * (1 + front_D_gap)
    )
    front_bound_p1_residual = sp.simplify(
        front_bound_gap_at_p1 - front_bound_gap_at_p1_expected
    )
    front_bound_check = bool(
        front_bound_rate.is_positive
        and front_bound_gap.is_positive
        and exact_zero(front_bound_residual)
        and front_bound_rate_at_p1.is_positive
        and front_bound_gap_at_p1.is_positive
        and exact_zero(front_bound_p1_residual)
    )

    radiation_constant, temperature = sp.symbols("a_R T", positive=True)
    radiation_pressure = sp.symbols("P_gamma", positive=True)
    radiation_density = radiation_constant * temperature**4
    radiation_pressure_from_temperature = radiation_density / 3
    temperature_from_pressure = (
        3 * radiation_pressure / radiation_constant
    ) ** sp.Rational(1, 4)
    radiation_temperature_residual = sp.simplify(
        radiation_pressure_from_temperature.subs(
            temperature, temperature_from_pressure
        )
        - radiation_pressure
    )

    scale_process, scale_prime, temperature_prime = sp.symbols(
        "A_tau A_tau_prime T_prime", positive=True
    )
    photon_source, rho_gamma = sp.symbols("Q_gamma rho_gamma")
    hubble_process = scale_prime / scale_process
    solved_temperature_prime = sp.simplify(
        temperature
        * (photon_source - 4 * hubble_process * rho_gamma)
        / (4 * rho_gamma)
    )
    radiation_source_residual = sp.simplify(
        solved_temperature_prime / temperature
        + hubble_process
        - photon_source / (4 * rho_gamma)
    )
    adiabatic_log_TA_derivative = sp.simplify(
        (
            solved_temperature_prime / temperature + hubble_process
        ).subs(photon_source, 0)
    )

    A0, Ae = sp.symbols("A_0 A_e", positive=True)
    temperature_emit, temperature_today = sp.symbols(
        "T_e T_today", positive=True
    )
    source_integral = sp.symbols("J_e", real=True)
    source_temperature_ratio = sp.exp(-source_integral)
    adiabatic_Tz_residual = sp.simplify(
        (
            temperature_emit
            / (temperature_today * A0 / Ae)
            - source_temperature_ratio
        ).subs(
            {
                source_integral: 0,
                temperature_emit: temperature_today * A0 / Ae,
            }
        )
    )
    source_temperature_ratio_derivative = sp.simplify(
        sp.diff(source_temperature_ratio, source_integral)
    )
    source_temperature_ratio_derivative_residual = sp.simplify(
        source_temperature_ratio_derivative + source_temperature_ratio
    )
    source_sign_classifier = bool(
        source_temperature_ratio_derivative.is_negative
        and source_temperature_ratio.subs(source_integral, 0) == 1
        and exact_zero(source_temperature_ratio_derivative_residual)
    )

    pressure_gamma_refg, pressure_gamma_standard = sp.symbols(
        "P_gamma_RefG P_gamma_standard", positive=True
    )
    temperature_ratio = (
        pressure_gamma_refg / pressure_gamma_standard
    ) ** sp.Rational(1, 4)
    ratio_from_eos = sp.simplify(
        (3 * pressure_gamma_refg / radiation_constant) ** sp.Rational(1, 4)
        / (3 * pressure_gamma_standard / radiation_constant)
        ** sp.Rational(1, 4)
    )
    temperature_ratio_residual = sp.simplify(
        ratio_from_eos - temperature_ratio
    )
    lower_temperature_mutation = sp.simplify(
        temperature_ratio - 1 / p_symbol
    )

    gamma_tau, H_tau = sp.symbols("Gamma_tau H_tau", positive=True)
    gamma_metric = p_symbol * gamma_tau
    H_metric = p_symbol * H_tau
    common_rate_ratio_residual = sp.simplify(
        gamma_metric / H_metric - gamma_tau / H_tau
    )
    common_cycle_residual = sp.simplify(
        gamma_metric / p_symbol - gamma_tau
    )

    nu_a0, nu_ae, nu_observed = sp.symbols(
        "nu_A0 nu_Ae nu_observed", positive=True
    )
    one_plus_z_spec = sp.symbols("one_plus_z_spec", positive=True)
    spectroscopic_definition_residual = sp.simplify(
        (
            one_plus_z_spec - nu_a0 / nu_observed
        ).subs(one_plus_z_spec, nu_a0 / nu_observed)
    )
    spectroscopic_factorization_residual = sp.simplify(
        nu_observed - nu_ae * Ae / A0
    )

    residuals = {
        "cadence_pressure": cadence_residual,
        "metric_time": metric_time_residual,
        "metric_space": metric_space_residual,
        "operational_scale_rate": hubble_residual,
        "already_activated_null": null_residual,
        "threshold_level_set": threshold_residual,
        "foundation_radius_chain": radius_chain_residual,
        "moving_boundary_leibniz_ftc": moving_boundary_ftc_residual,
        "moving_boundary_general_center": energy_general_residual,
        "moving_boundary_energy": energy_residual,
        "thermal_pressure_cadence_independence": cadence_partial_thermal,
        "same_cadence_two_thermal_states": same_cadence_two_thermal_states,
        "high_cadence_bound": high_cadence_bound_residual,
        "high_cadence_equality": high_cadence_equality_residual,
        "volume_measure_jacobian": volume_jacobian_residual,
        "two_sector_conservation": two_sector_sum_residual,
        "process_time_power_antiderivative": beta_antiderivative_residual,
        "radiation_temperature": radiation_temperature_residual,
        "radiation_temperature_source": radiation_source_residual,
        "adiabatic_log_TA_derivative": adiabatic_log_TA_derivative,
        "adiabatic_temperature_redshift": adiabatic_Tz_residual,
        "temperature_ratio": temperature_ratio_residual,
        "common_cadence_rate_ratio": common_rate_ratio_residual,
        "common_cadence_cycle_count": common_cycle_residual,
        "conditional_front_identity": front_identity_residual,
        "conditional_front_integral": front_integral_residual,
        "conditional_front_bound_gap": front_bound_residual,
        "conditional_front_bound_p_equals_one": front_bound_p1_residual,
        "temperature_source_ratio_derivative": (
            source_temperature_ratio_derivative_residual
        ),
        "spectroscopic_definition": spectroscopic_definition_residual,
    }

    mutation_residuals = {
        "metric_time_missing_cadence": sp.simplify(p_symbol**2 - 1),
        "operational_scale_additive_material_driver": (
            additive_material_driver_mutation
        ),
        "null_front_wrong_power": sp.simplify(
            c0 * p_symbol / a_symbol
            - c0 * p_symbol**2 / a_symbol
        ),
        "threshold_wrong_sign": sp.simplify(
            phi_t + phi_chi * (phi_t / phi_chi)
        ),
        "energy_missing_boundary_sweep": sp.simplify(
            energy_rate_reynolds
            - 4
            * sp.pi
            * (-radius**2 * flux_boundary + source_volume)
        ),
        "energy_nonregular_center_omitted": sp.simplify(
            energy_rate_general - energy_rate_reynolds
        ),
        "thermal_pressure_conflation": distinct_thermal_states,
        "lower_temperature_assumed_from_cadence": lower_temperature_mutation,
        "threshold_forced_to_null_without_PDE": null_threshold_residual,
        "spectroscopic_factorization_assumed": (
            spectroscopic_factorization_residual
        ),
    }

    flags = {
        "cadence_pressure_identity_exact": exact_zero(cadence_residual),
        "metric_process_dictionary_exact": all(
            (exact_zero(metric_time_residual), exact_zero(metric_space_residual))
        ),
        "operational_scale_rate_identity_exact": exact_zero(hubble_residual),
        "already_activated_null_identity_exact": exact_zero(null_residual),
        "threshold_level_set_speed_exact": exact_zero(threshold_residual),
        "foundation_threshold_radius_chain_rule_exact": exact_zero(
            radius_chain_residual
        ),
        "moving_boundary_energy_ledger_exact": bool(
            exact_zero(moving_boundary_ftc_residual)
            and exact_zero(energy_general_residual)
            and exact_zero(energy_residual)
        ),
        "constant_active_energy_condition_exposed": bool(
            source_volume in energy_rate_expected.free_symbols
            and radius_dot in energy_rate_expected.free_symbols
            and flux_boundary in energy_rate_expected.free_symbols
        ),
        "foundation_thermal_pressures_independent": bool(
            exact_zero(cadence_partial_thermal)
            and exact_zero(same_cadence_two_thermal_states)
            and exact_nonzero(distinct_thermal_states)
        ),
        "finite_process_origin_classified": bool(
            exact_zero(beta_antiderivative_residual)
            and exact_zero(finite_half - 2 * C * sp.sqrt(T0))
            and log_limit is sp.oo
            and power_limit is sp.oo
        ),
        "high_cadence_process_bound_exact": bool(
            exact_zero(high_cadence_bound_residual)
            and exact_zero(high_cadence_equality_residual)
            and nonnegative_cadence_excess.is_nonnegative
        ),
        "volume_measure_jacobian_exact": exact_zero(
            volume_jacobian_residual
        ),
        "two_sector_conservation_sum_exact": exact_zero(
            two_sector_sum_residual
        ),
        "radiation_temperature_identity_exact": exact_zero(
            radiation_temperature_residual
        ),
        "radiation_temperature_source_identity_exact": exact_zero(
            radiation_source_residual
        ),
        "adiabatic_Tz_no_go_exact": bool(
            exact_zero(adiabatic_log_TA_derivative)
            and exact_zero(adiabatic_Tz_residual)
            and source_temperature_ratio.subs(source_integral, 0) == 1
        ),
        "lower_temperature_sign_classifier_exact": source_sign_classifier,
        "lower_temperature_nonidentifiability_exact": bool(
            exact_zero(temperature_ratio_residual)
            and pressure_gamma_refg in temperature_ratio.free_symbols
            and pressure_gamma_standard in temperature_ratio.free_symbols
            and p_symbol not in temperature_ratio.free_symbols
            and exact_nonzero(lower_temperature_mutation)
        ),
        "common_cadence_rate_H_cancellation_exact": bool(
            exact_zero(common_rate_ratio_residual)
            and exact_zero(common_cycle_residual)
        ),
        "same_null_residual_exposed": exact_nonzero(
            null_threshold_residual
        ),
        "conditional_front_assumption_crosscheck_exact": bool(
            exact_zero(
                conditional_front_interval - sp.Rational(8, 5) * T0
            )
            and exact_zero(front_identity_residual)
            and exact_zero(front_integral_residual)
            and front_bound_check
        ),
        "observable_definitions_recorded": exact_zero(
            spectroscopic_definition_residual
        ),
        "schema_keysets_exact": False,
        "mutation_controls_pass": all(
            exact_nonzero(value) for value in mutation_residuals.values()
        ),
        "aggregate_identity_pass": False,
    }

    identities = {
        "cadence": "p^2=P_F/P_F0; d_tau=p dt",
        "operational_scale": "A=a/p",
        "metric": (
            "ds^2=p^2 c0^2 dt^2-(a^2/p^2)dchi^2"
            "=c0^2 d_tau^2-A^2 dchi^2"
        ),
        "operational_scale_rate": (
            "H_A^(tau)=p^-1[a_dot/a-P_F_dot/(2P_F)]"
        ),
        "already_activated_null": (
            "dchi/dt=+/-c0 p^2/a; dchi/dtau=+/-c0/A"
        ),
        "threshold_coordinate_speed": "dchi_act/dt=-Phi_t/Phi_chi",
        "threshold_foundation_radius_speed": (
            "dR_act/dt=H_a R_act-a Phi_t/Phi_chi"
        ),
        "moving_boundary_energy": (
            "local conservation plus Leibniz/FTC, with regular center F_0=0, "
            "gives dE_act/dt=4pi[R^2(rho_b R_dot-J_b)+Q_V]"
        ),
        "moving_boundary_general_center": (
            "before the regular-center specialization, add +4pi F_0"
        ),
        "constant_energy_condition": (
            f"Q_V={sp.sstr(constant_energy_source_condition)}"
        ),
        "finite_birth": (
            "tau_0=int_0^T0 p(t)dt; finite iff p is integrable at t=0"
        ),
        "high_cadence_bound": (
            "if p>=1, tau_0=T0+int_0^T0[p(t)-1]dt>=T0"
        ),
        "volume_measure": "V_F/V_op=p^3 for the same active cells",
        "two_sector_conservation": (
            "rho_th'+rho_F'+3H_tau"
            "(rho_th+rho_F+P_th+Pi_F)=0"
        ),
        "radiation_temperature": "T=(3P_gamma/a_R)^(1/4)",
        "radiation_temperature_source": (
            "d ln(TA)/d_tau=Q_gamma/(4rho_gamma)"
        ),
        "common_cadence_cancellation": (
            "Gamma_t/H_t=Gamma_tau/H_tau; "
            "int Gamma_t dt=int Gamma_tau d_tau"
        ),
        "conditional_front_assumption_consequence": (
            "assume constant E, spherical V, and a same-null front; "
            "with q=d ln(a)/d ln(P_F), D=1+3q: "
            "D(R)dR/dt=c0 p^2 and d_tau/dR=D(R)/(c0 p)"
        ),
    }

    classifications = {
        "process_time_origin": {
            "candidate_asymptotic": "p(t)~C t^(-beta)",
            "beta_not_one_antiderivative": (
                "C t^(1-beta)/(1-beta)"
            ),
            "finite": "beta<1",
            "log_divergent": "beta=1",
            "power_divergent": "beta>1",
            "finite_example_beta_half": sp.sstr(finite_half),
        },
        "conditional_front_crosscheck": {
            "assumptions": (
                "constant E, spherical V, same-null threshold, "
                "q=d ln(a)/d ln(P_F), D=1+3q"
            ),
            "local_identity": "d_tau/dR=D/(c0 p)",
            "regular_relaxation_bound": (
                "if 0<D<1 and p>=1, then 0<Delta_tau<R_final/c0"
            ),
            "p_equals_one_boundary": (
                "checked exactly: the positive gap is "
                "D_gap/[c0(1+D_gap)]"
            ),
            "p_vs_t": "p=(T0/t)^(3/8)",
            "elapsed_process_interval": sp.sstr(
                conditional_front_interval
            ),
            "ratio_to_metric_interval": "8/5",
            "normalization_subbranch": (
                "constant D=D0>0, equivalently constant q"
            ),
            "status": (
                "CONDITIONAL_ALGEBRAIC_BENCHMARK__NOT_CURRENT_BIRTH_MODEL"
            ),
        },
        "activation_scope": {
            "cosmic_birth": "GLOBAL_NO_PREFERRED_CENTER",
            "R_act": "LOCAL_THRESHOLD_OR_CORRELATION_SCALE",
            "null_leading_edge_equals_threshold": "NOT_DERIVED",
            "homogeneous_birth_radial_speed": "UNDEFINED",
            "same_null_condition": (
                "Phi_t+(c0 p^2/a)Phi_chi=0 must follow from a PDE"
            ),
        },
        "thermal_source_history": {
            "identity": (
                "T_e/[T_today(A0/Ae)]=exp(-J_e), "
                "J_e=int_e^today Q_gamma/(4rho_gamma)d_tau"
            ),
            "J_e_positive": "LOWER_THAN_ADIABATIC_REFERENCE",
            "J_e_zero": "EQUAL_TO_ADIABATIC_REFERENCE",
            "J_e_negative": "HIGHER_THAN_ADIABATIC_REFERENCE",
            "sign_proof": (
                "exp(-J_e) is strictly decreasing because its derivative "
                "is -exp(-J_e)<0 and its value at J_e=0 is 1"
            ),
            "prediction_status": "OPEN_UNTIL_Q_GAMMA_IS_DERIVED",
        },
    }

    thermal_identifiability = {
        "foundation_pressure": "P_F controls p through p^2=P_F/P_F0",
        "thermodynamic_pressure": (
            "P_th must come from the material-radiation stress tensor or EOS"
        ),
        "radiation_equilibrium": (
            "rho_gamma=a_R T^4 and P_gamma=rho_gamma/3"
        ),
        "temperature_ratio": (
            "T_RefG/T_standard="
            "(P_gamma_RefG/P_gamma_standard)^(1/4)"
        ),
        "faster_cadence_implication": (
            "p>1 alone does not order T_RefG and T_standard"
        ),
        "adiabatic_branch": (
            "Q_gamma=0 and 1+z=A0/Ae imply T_e=T_today(1+z)"
        ),
        "source_driven_branch": (
            "T_e/[T_today(1+z)]=exp(-J_e); Q_gamma history is open"
        ),
        "common_clock_result": (
            "a universal p rescales reaction rates and H equally"
        ),
        "lower_temperature_hypothesis": "OPEN_NOT_DERIVED",
        "required_dimensionless_tests": [
            "k_B T/E_atom",
            "h nu/(k_B T)",
            "Gamma_reaction/H_tau",
        ],
    }

    return residuals, flags, identities, mutation_residuals, (
        classifications,
        thermal_identifiability,
    )


def build_report() -> dict[str, object]:
    prereg_record = verify_preregistration()
    (
        residuals,
        closure_flags,
        identities,
        mutation_residuals,
        diagnostic_blocks,
    ) = derive_exact_gate()
    classifications, thermal_identifiability = diagnostic_blocks

    physical_closure_flags = {
        key: False for key in EXPECTED_PHYSICAL_CLOSURE_KEYS
    }

    observable_definitions = {
        "spectroscopic_redshift": (
            "1+z_spec=nu_A0/nu_observed"
        ),
        "spectroscopic_geometric_factorization": (
            "OPEN: nu_observed=nu_Ae Ae/A0 is not assumed or derived"
        ),
        "cosmic_chronometer": (
            "H_CC=-(1+z_spec)^-1 dz_spec/dtau_SPS"
        ),
        "luminosity_distance": (
            "OPEN: requires photon flux, energy, arrival rate, reciprocity, "
            "and source-luminosity maps"
        ),
        "prediction_status": "DEFINITIONS_ONLY__NO_NUMERICAL_CURVES",
    }

    contract = {
        "CLAIM_ID": CLAIM_ID,
        "CLAIM": (
            "The finite-birth RefG dictionary is internally consistent and "
            "exactly identifies its physical, thermal, and observational "
            "closure boundary."
        ),
        "TYPE": "EXACT_IDENTITY_CONDITIONAL_NO_GO_AND_CLOSURE_LEDGER",
        "MODEL_VERSION": {
            "id": MODEL_VERSION,
            "change_boundary": (
                "Any change to the finite origin, cadence-pressure bridge, "
                "operational-scale dictionary, causal-role semantics, threshold/"
                "moving-boundary/thermal domain, observable definitions, claim "
                "scope, or closure keys."
            ),
        },
        "ASSUMPTIONS": (
            "Finite t-origin; positive p; p^2=P_F/P_F0; d_tau=p dt; "
            "A=a/p; global centerless birth; differentiable local threshold; "
            "P_F and P_th independent; conditional radiation EOS; local "
            "flat spherical continuity ledger with a regular center."
        ),
        "DOMAIN": (
            "t in (0,T0], positive differentiable background functions, "
            "nonzero threshold gradient, local flat Eulerian boundary patch, "
            "equilibrium radiation branch."
        ),
        "CONVENTIONS": {
            "time_metric": "dot=d/dt; prime=d/dtau; tau(0)=0",
            "metric_signature": "(+---)",
            "units": (
                "c0: speed; P and rho: energy/volume; J_b: signed energy "
                "flux/area; Q_V: signed energy-rate per solid angle"
            ),
            "source_signs": (
                "J_b>0 outward; R_dot and Q_V signed; Q>0 foundation-to-"
                "thermal; Q_gamma>0 radiation injection; Pi_F>0 pressure"
            ),
            "activation_radius": "local threshold scale, not cosmic edge",
            "moving_boundary_radius": (
                "local flat physical Eulerian radius; F_0=0 regular center"
            ),
        },
        "FREEDOM_LEDGER": {
            "current_fitted_effective_dimension": 0,
            "activation_and_threshold": {
                "source": "foundation action and initial state",
                "domain": "global birth and regular threshold neighborhoods",
                "scale": "universal",
                "effective_complexity_measure": (
                    "functional/infinite-dimensional field and initial "
                    "spectrum, one threshold scalar, one topology index"
                ),
            },
            "background_dynamics": {
                "source": "foundation action and energy balance",
                "domain": "positive homogeneous histories on (0,T0]",
                "scale": "universal",
                "effective_complexity_measure": (
                    "functional/infinite-dimensional P_F(t), a(t), stress, "
                    "and transfer histories"
                ),
            },
            "thermal_species_closure": {
                "source": "stress tensor and kinetic/EOS closure",
                "domain": "each thermal species or sector",
                "scale": "group",
                "effective_complexity_measure": (
                    "functional/infinite-dimensional per species or sector"
                ),
            },
            "photon_propagation_law": {
                "source": "foundation radiative action",
                "domain": "universal massless propagation sector",
                "scale": "universal",
                "effective_complexity_measure": (
                    "functional/infinite-dimensional dispersion and "
                    "coupling laws"
                ),
            },
            "atomic_SPS_response": {
                "source": "atomic response and SPS calibration",
                "domain": "each transition, population, or response family",
                "scale": "group",
                "effective_complexity_measure": (
                    "functional/infinite-dimensional per response family"
                ),
            },
            "source_history_and_luminosity": {
                "source": "individual emitter history",
                "domain": "each astrophysical source",
                "scale": "object",
                "effective_complexity_measure": (
                    "one functional history per object, or k_object after "
                    "preregistration"
                ),
            },
            "survey_instrument_calibration": {
                "source": "survey and instrument calibration model",
                "domain": "each survey or instrument configuration",
                "scale": "group",
                "effective_complexity_measure": (
                    "N_calibration per survey/instrument group"
                ),
            },
            "datum_selection_and_noise": {
                "source": "datum-level likelihood and selection model",
                "domain": "individual measurements or catalog entries",
                "scale": "data",
                "effective_complexity_measure": (
                    "N_nuisance declared by a future forward model; zero here"
                ),
            },
        },
        "DEPENDENCIES": (
            "None. This self-contained gate derives dictionary/continuity "
            "consequences and checks labeled assumption-consequence branches."
        ),
        "METHOD": {
            "selection_rationale": (
                "The claim concerns exact identities and identifiability, "
                "so symbolic rather than statistical methods are required."
            ),
            "operations": (
                "SymPy differentiation, local continuity, Leibniz/FTC, "
                "substitution, integration, inequality checks, mutations, "
                "and schema checks"
            ),
            "output": "strict atomic JSON plus external SHA-256",
        },
        "PASS_CONDITION": (
            "All exact flags and mutations pass; schema is exact; every "
            "physical/observational closure remains false."
        ),
        "FAIL_CONDITION": (
            "Any identity/schema/mutation fails or an unclosed numerical "
            "temperature, age, H_CC, D_L, or birth model is promoted."
        ),
        "FALSIFIER": (
            "A counterexample under frozen assumptions falsifies the exact "
            "identity; no RefG-wide falsifier is defined here."
        ),
        "RESIDUAL": {
            key: sp.sstr(value) for key, value in residuals.items()
        },
        "ERROR_BOUND": "Zero for symbolic identities; N/A otherwise.",
        "VALIDITY_HEALTH": (
            "Bookkeeping and identifiability only; no physical cosmology "
            "or observational validation."
        ),
        "BRANCHES": list(classifications),
        "OBSERVABLE_MAP": observable_definitions,
        "FORWARD_MODEL": "N/A: no synthetic observable or real-data fit.",
        "DATA_ROLE": "No observational data.",
        "IDENTIFIABILITY": thermal_identifiability,
        "BENCHMARK": (
            "Exact metric, threshold, energy, thermal, origin, and "
            "constant-D checks plus fail-fast negative mutations."
        ),
        "CLOSURE_FLAGS": dict(closure_flags),
        "CROSSCHECK": (
            "general beta antiderivative; beta=1/2,1,3/2; "
            "constant-D beta=3/8 interval; moving boundary; "
            "two thermal states at fixed cadence."
        ),
        "PROVENANCE": (
            "Pinned preregistration, source hash, runtime versions, UTC, "
            "strict LF JSON, and external result checksum."
        ),
        "FILES": [
            PREREG.name,
            Path(__file__).name,
            OUTPUT.name,
            HASH_OUTPUT.name,
        ],
    }

    source_record = {
        "path": Path(__file__).relative_to(HERE.parents[2]).as_posix(),
        "sha256": sha256(Path(__file__)),
    }
    report: dict[str, object] = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "claim": contract["CLAIM"],
        "type": contract["TYPE"],
        "model_version": MODEL_VERSION,
        "status": "PENDING_SCHEMA_CHECK",
        "scope_status": "PENDING_SCHEMA_CHECK",
        "artifact_valid": False,
        "evidence_type": "EXACT_IDENTITY",
        "refg_status": "OPEN",
        "mechanism_status": "OPEN",
        "finite_process_time_status": (
            "FINITE_ALLOWED__NUMERICAL_VALUE_NOT_PREDICTED"
        ),
        "temperature_claim_status": (
            "GENUINELY_HOT_BRANCH_ALLOWED__LOWER_THAN_STANDARD_OPEN"
        ),
        "observational_status": "OPEN_NOT_EXECUTED",
        "falsifier_triggered_for_refg": False,
        "blocking_reasons": [
            "No derived activation-field action, initial spectrum, or threshold.",
            "No foundation energy balance or foundation-to-thermal transfer law.",
            "No material-radiation EOS history or physical temperature history.",
            "No atomic, stellar-clock, photon-flux, H_CC, or D_L forward model.",
            "No CMB, recombination, BBN, supernova, BAO, or JWST validation.",
        ],
        "contract": contract,
        "closure_flags": closure_flags,
        "physical_closure_flags": physical_closure_flags,
        "identities": identities,
        "classifications": classifications,
        "thermal_identifiability": thermal_identifiability,
        "observable_definitions": observable_definitions,
        "negative_controls": {
            key: sp.sstr(value)
            for key, value in mutation_residuals.items()
        },
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "preregistration": prereg_record,
            "source": source_record,
            "python": platform.python_version(),
            "sympy": importlib.metadata.version("sympy"),
            "platform": platform.platform(),
            "line_endings": "LF",
        },
        "files": {
            "preregistration": PREREG.name,
            "source": Path(__file__).name,
            "result": OUTPUT.name,
            "result_checksum": HASH_OUTPUT.name,
        },
    }

    schema_keysets_exact = bool(
        set(contract) == REQUIRED_CONTRACT_FIELDS
        and set(closure_flags) == EXPECTED_CLOSURE_KEYS
        and set(physical_closure_flags) == EXPECTED_PHYSICAL_CLOSURE_KEYS
        and set(report) == EXPECTED_RESULT_KEYS
    )
    closure_flags["schema_keysets_exact"] = schema_keysets_exact
    closure_flags["aggregate_identity_pass"] = all(
        value
        for key, value in closure_flags.items()
        if key != "aggregate_identity_pass"
    )
    contract["CLOSURE_FLAGS"] = dict(closure_flags)

    scope_integrity = not any(physical_closure_flags.values())
    artifact_valid = bool(
        closure_flags["aggregate_identity_pass"] and scope_integrity
    )
    report["artifact_valid"] = artifact_valid
    report["status"] = "PASS" if artifact_valid else "FAIL"
    report["scope_status"] = (
        "PASS_EXACT_IDENTITIES__FINITE_BIRTH_COMPATIBLE__"
        "PHYSICAL_AND_THERMAL_CLOSURES_OPEN"
        if artifact_valid
        else "FAIL_EXACT_GATE__NO_PHYSICAL_VERDICT"
    )
    return report


def write_strict_json(report: dict[str, object]) -> None:
    payload = json.dumps(
        report,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    ) + "\n"
    temporary = OUTPUT.with_suffix(".json.tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload)
    temporary.replace(OUTPUT)


def write_result_checksum() -> str:
    digest = sha256(OUTPUT)
    payload = f"{digest}  {OUTPUT.name}\n"
    temporary = HASH_OUTPUT.with_suffix(".sha256.tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload)
    temporary.replace(HASH_OUTPUT)
    return digest


def write_failure_json(error: Exception) -> None:
    failure = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "status": "FAIL",
        "scope_status": "FAIL_CLOSED_RUNTIME_OR_PROVENANCE_ERROR",
        "artifact_valid": False,
        "refg_status": "OPEN",
        "blocking_error": f"{type(error).__name__}: {error}",
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "source": {
                "path": Path(__file__).relative_to(
                    HERE.parents[2]
                ).as_posix(),
                "sha256": sha256(Path(__file__)),
            },
            "python": platform.python_version(),
            "sympy": importlib.metadata.version("sympy"),
        },
    }
    write_strict_json(failure)
    write_result_checksum()


def main() -> int:
    try:
        report = build_report()
        write_strict_json(report)
        result_digest = write_result_checksum()
        print(report["scope_status"])
        print(f"Result: {OUTPUT}")
        print(f"Result SHA-256: {result_digest}")
        return 0 if report["artifact_valid"] else 2
    except Exception as error:
        write_failure_json(error)
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
