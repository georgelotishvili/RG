'''W3-56 reduced one-oscillon coframe-lock candidate gate.'''

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


CLAIM_ID = 'W3_56_ONE_OSCILLON_COFRAME_LOCK_BRIDGE'
MODEL_VERSION = 'W3-56-v1.0-REDUCED-ONE-OSCILLON-COFRAME-LOCK'
PASS_STATUS = (
    'PASS_EXACT_INTERNAL_ALGEBRA_OF_SELECTED_FIXED_BACKGROUND_RESPONSE_AND_'
    'BICONFORMAL_PULLBACK_WITNESS__W3_50_OSCILLON_CORE_SPECTRAL_GATE_'
    'PRESSURE_STRESS_COVARIANT_BACKREACTION_AND_UNIVERSALITY_OPEN'
)
HERE = Path(__file__).resolve().parent
WORK3 = HERE.parents[1]
PREREG = HERE / 'w3_56_one_oscillon_coframe_lock_bridge_preregistration.md'
OUTPUT = HERE / 'w3_56_result.json'
HASH_OUTPUT = HERE / 'w3_56_result.sha256'
PINNED_PREREG_SHA256 = (
    '2621326161bfb65a651e56bfdeade2e3b290efe39cf2211467851850d030dc5c'
)

DEPENDENCY_CONTRACTS = {
    'W3_50': (
        WORK3 / 'Cosmology_and_LSS'
        / 'Active_Participation_Resonance_Feedback'
        / 'w3_50_neutral_collective_phase_density_bridge_contract.md',
        '1cb66438a6bf53f1a661a014328204c05edfe847f81d876defe69eaa400591db',
    ),
    'W3_54': (
        WORK3 / 'Lagrangian_Formulation'
        / 'Relational_Coframe_TEGR_Phase_Source_Closure'
        / 'w3_54_relational_coframe_tegr_phase_source_closure_contract.md',
        '6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879',
    ),
    'W3_51': (
        WORK3 / 'Lagrangian_Formulation' / 'Weak_Field_Closure'
        / 'w3_51_weak_field_closure_contract.md',
        '2129386227019d5a7939aa071c786d2f1e40f383e93b34cc42161a245afbd412',
    ),
    'W3_52': (
        WORK3 / 'Lagrangian_Formulation' / 'Full_1PN_Inheritance'
        / 'w3_52_full_1pn_inheritance_contract.md',
        '66a33a82d29bd65fabc37b6e55f29a64674f0e44f5a4c0893611c261d00792b6',
    ),
}

REQUIRED_CONTRACT_FIELDS = {
    'CLAIM_ID', 'CLAIM', 'TYPE', 'MODEL_VERSION', 'ASSUMPTIONS',
    'DOMAIN', 'CONVENTIONS', 'FREEDOM_LEDGER', 'DEPENDENCIES',
    'METHOD', 'PASS_CONDITION', 'FAIL_CONDITION', 'FALSIFIER',
    'RESIDUAL', 'ERROR_BOUND', 'VALIDITY_HEALTH', 'BRANCHES',
    'OBSERVABLE_MAP', 'FORWARD_MODEL', 'DATA_ROLE', 'IDENTIFIABILITY',
    'BENCHMARK', 'CLOSURE_FLAGS', 'CROSSCHECK', 'PROVENANCE', 'FILES',
}

REQUIRED_EXACT_KEYS = {
    'primitive_response_target_symbols_absent_exact',
    'completed_square_bounded_exact',
    'positive_stationary_response_exact',
    'response_hessian_positive_exact',
    'dependency_hashes_pinned_exact',
    'density_amplitude_identity_exact',
    'selected_restoring_readout_square_law_exact',
    'w3_54_eos_underdetermination_exact',
    'action_angle_reparametrization_exact',
    'process_time_transverse_equations_exact',
    'proper_cadence_invariant_exact',
    'selected_probe_coordinate_spectrum_factorization_exact',
    'dimensionless_spectrum_invariant_exact',
    'field_pullback_jacobian_exact',
    'biconformal_field_pullback_exact_constant_patch',
    'coordinate_signal_speed_square_exact',
    'coordinate_radius_linear_exact',
    'external_energy_and_defined_mass_linear_exact',
    'finite_localized_scaling_witness_exact',
    'positive_field_coefficients_exact',
    'phase_roles_distinct_exact',
    'single_probe_coframe_no_duplicate_source_bookkeeping_registered_exact',
    'registered_contract_keysets_exact',
    'mutation_controls_pass',
    'aggregate_candidate_pass',
}

REQUIRED_SCOPE_KEYS = {
    'selected_operator_from_nodes_derived',
    'P_F_readout_from_covariant_stress_derived',
    'covariant_TEGR_embedding_derived',
    'joint_B_b_dynamics_stable',
    'localized_backreaction_derived',
    'reference_oscillon_core_from_foundation_derived',
    'environment_independence_of_H0_derived',
    'finite_energy_oscillon_solution_constructed',
    'W3_50_localized_spectral_gate_closed',
    'one_source_one_coframe_from_action_derived',
    'full_nonlinear_oscillon_PDE_solved',
    'all_particle_families_universalized',
    'particle_mass_spectrum_derived',
    'Koide_or_C3_used',
    'Planck_hierarchy_derived',
    'strong_field_or_2PN_completed',
    'cosmological_history_derived',
    'observational_likelihood_evaluated',
}

REQUIRED_MUTATION_KEYS = {
    'pressure_floor_detected',
    'nonlinear_drive_detected',
    'additive_coordinate_stiffness_detected',
    'proper_frequency_contamination_detected',
    'wrong_spatial_coframe_detected',
    'target_insertion_detected',
    'phase_role_collapse_detected',
    'duplicate_source_detected',
    'probe_backreaction_detected',
}

EXPECTED_RESULT_KEYS = {
    'schema_version', 'claim_id', 'claim', 'type', 'model_version',
    'status', 'scope_status', 'artifact_valid', 'evidence_type',
    'blocking_boundaries', 'contract', 'closure_flags', 'scope_flags',
    'identities', 'benchmark', 'semantic_constraints',
    'negative_controls', 'diagnostics', 'provenance', 'files',
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_zero(value: object) -> bool:
    return sp.simplify(value) == 0


def exact_nonzero(value: object) -> bool:
    return sp.simplify(value) != 0


def verify_preregistration() -> dict[str, object]:
    payload = PREREG.read_bytes()
    if b'\r' in payload or not payload.endswith(b'\n'):
        raise RuntimeError('Preregistration is not canonical UTF-8 LF text')
    actual_hash = hashlib.sha256(payload).hexdigest()
    if actual_hash != PINNED_PREREG_SHA256:
        raise RuntimeError(f'Frozen preregistration changed: {actual_hash}')
    text = payload.decode('utf-8')
    fields = set(re.findall(r'^\*\*([A-Z_]+):\*\*', text, re.MULTILINE))
    if fields != REQUIRED_CONTRACT_FIELDS:
        raise RuntimeError(
            f'Contract field drift: missing={REQUIRED_CONTRACT_FIELDS-fields}, '
            f'extra={fields-REQUIRED_CONTRACT_FIELDS}'
        )
    claim_match = re.search(
        r'^\*\*CLAIM:\*\*\s*(.+)$', text, re.MULTILINE
    )
    if claim_match is None:
        raise RuntimeError('Claim field is missing')
    return {
        'path': PREREG.name,
        'sha256': actual_hash,
        'field_names': sorted(fields),
        'registered_claim': claim_match.group(1).strip(),
        'valid': True,
    }


def verify_dependency_contracts() -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for claim, (path, expected_hash) in DEPENDENCY_CONTRACTS.items():
        if not path.is_file():
            raise RuntimeError(f'Missing dependency contract: {path}')
        actual_hash = sha256(path)
        if actual_hash != expected_hash:
            raise RuntimeError(
                f'Pinned dependency changed for {claim}: {actual_hash}'
            )
        records[claim] = {
            'path': path.relative_to(WORK3).as_posix(),
            'sha256': actual_hash,
            'valid': True,
        }
    return records


def validate_response(
    raw_response: sp.Expr, q: sp.Symbol
) -> dict[str, sp.Expr]:
    reference = sp.simplify(raw_response.subs(q, 1))
    normalized = sp.simplify(raw_response / reference)
    return {
        'normalized': normalized,
        'linear_residual': sp.simplify(normalized - q),
        'square_readout_residual': sp.simplify(normalized**2 - q**2),
    }


def validate_coordinate_factor(
    raw_factor: sp.Expr, q: sp.Symbol, expected: sp.Expr
) -> sp.Expr:
    normalized = sp.simplify(raw_factor / raw_factor.subs(q, 1))
    return sp.simplify(normalized - expected)


def validate_primitive_symbols(
    expression: sp.Expr, forbidden_names: set[str]
) -> bool:
    names = {symbol.name for symbol in expression.free_symbols}
    return not bool(names & forbidden_names)


def validate_semantics(
    phase_roles: dict[str, str],
    sources: tuple[str, ...],
    coframe_count: int,
) -> dict[str, bool]:
    distinct = len(set(phase_roles.values())) == len(phase_roles)
    single_source = len(sources) == 1
    duplicate_source = any(
        source == 'P_F_independent_source' for source in sources
    )
    return {
        'phase_roles_distinct': distinct,
        'single_coframe': coframe_count == 1,
        'single_registered_source': single_source,
        'no_duplicate_pressure_source': not duplicate_source,
        'valid': bool(
            distinct
            and coframe_count == 1
            and single_source
            and not duplicate_source
        ),
    }


def derive_candidate(
    dependencies: dict[str, dict[str, object]]
) -> tuple[
    dict[str, str], dict[str, bool], dict[str, bool],
    dict[str, bool], dict[str, object]
]:
    K, lam, B, B0, b, n_C, n_C0 = sp.symbols(
        'K lambda B B0 b n_C n_C0', positive=True
    )
    response_potential = K * (b - lam * B) ** 2 / 2
    response_equation = sp.diff(response_potential, b)
    b_star = lam * B
    b0 = lam * B0
    beta = sp.simplify(b_star / b0)
    response_hessian = sp.diff(response_potential, b, 2)
    pressure_f = sp.simplify(K * b_star**2 / 2)
    pressure_f0 = sp.simplify(K * b0**2 / 2)
    eta_from_amplitude = sp.simplify(B**2 / B0**2)
    eta_from_density = sp.simplify(
        (n_C / n_C0).subs({n_C: B**2, n_C0: B0**2})
    )

    primitive_names = {symbol.name for symbol in response_potential.free_symbols}
    target_names = {'p', 'P_F', 'P_F0', 'eta_F'}
    primitive_target_free = validate_primitive_symbols(
        response_potential, target_names
    )
    residuals: dict[str, object] = {
        'response_stationarity': response_equation.subs(b, b_star),
        'completed_square_minimum': response_potential.subs(b, b_star),
        'normalized_response': beta - B / B0,
        'density_amplitude_identity': eta_from_density - eta_from_amplitude,
        'selected_restoring_readout_square_law': (
            pressure_f / pressure_f0 - beta**2
        ),
        'selected_restoring_readout_density_map': (
            pressure_f / pressure_f0 - eta_from_amplitude
        ),
        'K_cancels_from_beta': sp.diff(beta, K),
        'lambda_cancels_from_beta': sp.diff(beta, lam),
        'K_cancels_from_pressure_ratio': sp.diff(
            pressure_f / pressure_f0, K
        ),
        'lambda_cancels_from_pressure_ratio': sp.diff(
            pressure_f / pressure_f0, lam
        ),
    }

    eta = sp.symbols('eta', positive=True)
    gamma_phase = sp.Rational(3, 2)
    gamma_alternative = sp.Rational(4, 3)
    phase_ratio_gamma_phase = eta ** (gamma_phase - 1)
    pressure_ratio_gamma_phase = eta**gamma_phase
    phase_ratio_alternative = eta ** (gamma_alternative - 1)
    residuals['w3_54_gamma_three_halves_phase_identity'] = (
        phase_ratio_gamma_phase - sp.sqrt(eta)
    )
    residuals['w3_54_gamma_three_halves_pressure_relation'] = (
        pressure_ratio_gamma_phase - eta * phase_ratio_gamma_phase
    )
    w3_54_eos_underdetermination = bool(
        exact_zero(
            residuals['w3_54_gamma_three_halves_phase_identity']
        )
        and exact_zero(
            residuals['w3_54_gamma_three_halves_pressure_relation']
        )
        and exact_nonzero(
            (pressure_ratio_gamma_phase - eta).subs(eta, 4)
        )
        and exact_nonzero(
            (
                phase_ratio_gamma_phase - phase_ratio_alternative
            ).subs(eta, 4)
        )
        and 1 < gamma_alternative <= 2
        and 1 < gamma_phase <= 2
    )

    J_O, omega0, alpha = sp.symbols('J_O omega0 alpha', positive=True)
    Q, Pi = sp.symbols('Q Pi', real=True)
    omega_q, energy0 = sp.symbols('omega_q E0', positive=True)
    theta_O = sp.symbols('theta_O', real=True)
    H0 = (
        energy0 + omega0 * J_O + alpha * J_O**2 / 2
        + Pi**2 / 2 + omega_q**2 * Q**2 / 2
    )
    H_t = sp.expand(beta * H0)
    theta_rate_t = sp.diff(H_t, J_O)
    theta_rate_tau = sp.simplify(theta_rate_t / beta)
    q_rate = sp.diff(H_t, Pi)
    pi_rate = -sp.diff(H_t, Q)
    process_q_rate = sp.simplify(q_rate / beta)
    process_pi_rate = sp.simplify(pi_rate / beta)
    transverse_matrix = sp.Matrix([
        [0, beta],
        [-beta * omega_q**2, 0],
    ])
    coordinate_transverse_frequency = sp.simplify(
        sp.sqrt(-sp.trace(transverse_matrix**2) / 2)
    )
    proper_orbit_energy = H0.subs({Q: 0, Pi: 0})
    coordinate_orbit_energy = H_t.subs({Q: 0, Pi: 0})

    residuals.update({
        'action_angle_J_conservation': -sp.diff(H_t, theta_O),
        'proper_phase_rate': theta_rate_tau - (omega0 + alpha * J_O),
        'coordinate_phase_factor': (
            theta_rate_t - beta * (omega0 + alpha * J_O)
        ),
        'process_time_q_equation': process_q_rate - Pi,
        'process_time_pi_equation': process_pi_rate + omega_q**2 * Q,
        'coordinate_transverse_factor_constant_patch': (
            coordinate_transverse_frequency - beta * omega_q
        ),
        'dimensionless_spectrum_ratio': (
            coordinate_transverse_frequency / theta_rate_t
            - omega_q / (omega0 + alpha * J_O)
        ),
        'proper_energy_invariant': H_t / beta - H0,
        'external_energy_factor': (
            coordinate_orbit_energy / proper_orbit_energy - beta
        ),
        'external_mass_factor': (
            coordinate_orbit_energy / proper_orbit_energy - beta
        ),
        'canonical_q_rate': q_rate - beta * Pi,
        'canonical_pi_rate': pi_rate + beta * omega_q**2 * Q,
    })

    Z, c0, mu, k, k_star = sp.symbols(
        'Z c0 mu k k_star', positive=True
    )
    time_jacobian = beta
    spatial_jacobian = beta ** -3
    action_measure_factor = sp.simplify(
        time_jacobian * spatial_jacobian
    )
    proper_time_derivative_factor = beta ** -1
    proper_spatial_derivative_factor = beta
    kinetic_coefficient = sp.simplify(
        Z * action_measure_factor
        * proper_time_derivative_factor**2 / 2
    )
    gradient_coefficient = sp.simplify(
        Z * c0**2 * action_measure_factor
        * proper_spatial_derivative_factor**2 / 2
    )
    potential_coefficient = action_measure_factor
    time_weight = 2 * kinetic_coefficient
    gradient_weight = 2 * gradient_coefficient
    mass_weight = sp.simplify(Z * mu**2 * potential_coefficient)
    omega_t_sq = sp.simplify(
        gradient_weight / time_weight * k**2
        + mass_weight / time_weight
    )
    omega_star_sq = c0**2 * k_star**2 + mu**2
    pulled_dispersion = sp.simplify(
        omega_t_sq.subs(k, k_star / beta) - beta**2 * omega_star_sq
    )
    coordinate_signal_speed = sp.sqrt(beta**4 * c0**2)

    T_ref, G_ref, V_ref = sp.symbols(
        'T_ref G_ref V_ref', positive=True
    )
    energy_ref = T_ref + G_ref + V_ref
    coordinate_volume_factor = beta**3
    pulled_time_derivative_factor = beta
    pulled_spatial_derivative_factor = beta ** -1
    kinetic_energy_factor = sp.simplify(
        (time_weight / Z)
        * pulled_time_derivative_factor**2
        * coordinate_volume_factor
    )
    gradient_energy_factor = sp.simplify(
        (gradient_weight / (Z * c0**2))
        * pulled_spatial_derivative_factor**2
        * coordinate_volume_factor
    )
    potential_energy_factor = sp.simplify(
        potential_coefficient * coordinate_volume_factor
    )
    energy_t = (
        kinetic_energy_factor * T_ref
        + gradient_energy_factor * G_ref
        + potential_energy_factor * V_ref
    )
    mass_ref = energy_ref / c0**2
    mass_t = energy_t / c0**2
    residuals.update({
        'field_action_measure_jacobian': (
            action_measure_factor - beta**-2
        ),
        'field_time_derivative_map': (
            proper_time_derivative_factor - beta**-1
        ),
        'field_spatial_derivative_map': (
            proper_spatial_derivative_factor - beta
        ),
        'field_time_kinetic_coefficient': (
            kinetic_coefficient - Z / (2 * beta**4)
        ),
        'field_spatial_gradient_coefficient': (
            gradient_coefficient - Z * c0**2 / 2
        ),
        'field_potential_coefficient': (
            potential_coefficient - beta**-2
        ),
        'pulled_dispersion': pulled_dispersion,
        'coordinate_signal_speed': coordinate_signal_speed - beta**2 * c0,
        'transformed_energy': energy_t / energy_ref - beta,
        'defined_external_mass': mass_t / mass_ref - beta,
        'kinetic_energy_scaling': kinetic_energy_factor - beta,
        'gradient_energy_scaling': gradient_energy_factor - beta,
        'potential_energy_scaling': potential_energy_factor - beta,
    })

    r, x, radius0, witness_energy = sp.symbols(
        'r x R0 E_w', positive=True
    )
    density_ref = (
        witness_energy
        * sp.exp(-r**2 / radius0**2)
        / (sp.pi ** sp.Rational(3, 2) * radius0**3)
    )
    total_ref = sp.integrate(
        4 * sp.pi * r**2 * density_ref, (r, 0, sp.oo)
    )
    moment_ref = sp.integrate(
        4 * sp.pi * r**4 * density_ref, (r, 0, sp.oo)
    )
    density_scaled = (
        beta ** -2
        * witness_energy
        * sp.exp(-(x / beta) ** 2 / radius0**2)
        / (sp.pi ** sp.Rational(3, 2) * radius0**3)
    )
    total_scaled = sp.integrate(
        4 * sp.pi * x**2 * density_scaled, (x, 0, sp.oo)
    )
    moment_scaled = sp.integrate(
        4 * sp.pi * x**4 * density_scaled, (x, 0, sp.oo)
    )
    rms_ratio_sq = sp.simplify(
        (moment_scaled / total_scaled) / (moment_ref / total_ref)
    )
    residuals.update({
        'localized_witness_energy': total_ref - witness_energy,
        'localized_witness_second_moment': (
            moment_ref - sp.Rational(3, 2) * witness_energy * radius0**2
        ),
        'beta_linked_witness_energy': total_scaled - beta * witness_energy,
        'beta_linked_witness_rms_radius': rms_ratio_sq - beta**2,
    })

    phase_roles = {
        'collective': 'theta_C',
        'oscillon': str(theta_O),
        'time': 'tau',
    }
    selected_sources = ('phase_Hilbert_source',)
    selected_semantics = validate_semantics(
        phase_roles, selected_sources, 1
    )
    semantic_constraints = {
        'primitive_response_symbols': sorted(primitive_names),
        'primitive_target_symbols_absent': primitive_target_free,
        'pressure_readout': (
            'P_F^(R)_SELECTED_POSITIVE_RESTORING_CHANNEL__'
            'NOT_TOTAL_U__NOT_HILBERT_STRESS__NOT_p_C'
        ),
        'background_split': 'FIXED_BACKGROUND_THEN_ONE_OSCILLON_PROBE',
        'phase_roles': phase_roles,
        'phase_roles_distinct': selected_semantics['phase_roles_distinct'],
        'coframe_count': 1,
        'registered_sources': selected_sources,
        'source_ledger_rule': (
            'P_F_READOUT_NOT_REGISTERED_AS_SECOND_HILBERT_SOURCE'
        ),
        'source_ledger_status': (
            'SELECTED_REDUCED_BOOKKEEPING__NOT_DERIVED_FROM_ACTION_VARIATION'
        ),
        'H0_environment_independence_status': (
            'SELECTED_PROBE_CONSTRUCTION__NOT_DERIVED_FROM_W3_50_CORE'
        ),
        'exact_profile_domain': 'CONSTANT_POSITIVE_BETA',
        'varying_background_domain': (
            'PROCESS_TIME_HAMILTON_EQUATIONS_EXACT__'
            'PROFILE_AND_COORDINATE_SPECTRUM_LOCAL_ADIABATIC_ONLY'
        ),
    }

    q, floor, delta, epsilon, backreaction = sp.symbols(
        'q floor delta epsilon backreaction', positive=True
    )
    selected_response_validation = validate_response(q, q)
    selected_coordinate_cadence_validation = validate_coordinate_factor(
        q, q, q
    )
    selected_proper_frequency_validation = validate_coordinate_factor(
        sp.Integer(1), q, sp.Integer(1)
    )
    selected_spatial_coframe_validation = validate_coordinate_factor(
        q, q, q
    )
    floor_validation = validate_response(q + floor, q)
    nonlinear_validation = validate_response(q**2, q)
    backreaction_validation = validate_response(
        q - backreaction, q
    )
    additive_stiffness_residual = validate_coordinate_factor(
        sp.sqrt(q**2 + delta), q, q
    ).subs({q: 2, delta: 1})
    proper_frequency_residual = validate_coordinate_factor(
        1 + epsilon * (q - 1), q, sp.Integer(1)
    ).subs({q: 2, epsilon: 1})
    wrong_spatial_residual = validate_coordinate_factor(
        1 / q, q, q
    ).subs(q, 2)
    P_target = sp.symbols('P_target', positive=True)
    target_mutation = K * (b - sp.sqrt(P_target)) ** 2 / 2
    collapsed_roles = {
        'collective': 'theta_C',
        'oscillon': 'theta_C',
        'time': 'tau',
    }
    duplicate_sources = ('phase_Hilbert_source', 'P_F_independent_source')
    collapsed_semantics = validate_semantics(
        collapsed_roles, selected_sources, 1
    )
    duplicate_semantics = validate_semantics(
        phase_roles, duplicate_sources, 1
    )
    negative_controls = {
        'pressure_floor_detected': exact_nonzero(
            floor_validation['square_readout_residual'].subs(
                {q: 2, floor: 1}
            )
        ),
        'nonlinear_drive_detected': exact_nonzero(
            nonlinear_validation['linear_residual'].subs(q, 2)
        ),
        'additive_coordinate_stiffness_detected': exact_nonzero(
            additive_stiffness_residual
        ),
        'proper_frequency_contamination_detected': exact_nonzero(
            proper_frequency_residual
        ),
        'wrong_spatial_coframe_detected': exact_nonzero(wrong_spatial_residual),
        'target_insertion_detected': not validate_primitive_symbols(
            target_mutation, target_names | {'P_target'}
        ),
        'phase_role_collapse_detected': not collapsed_semantics['valid'],
        'duplicate_source_detected': not duplicate_semantics['valid'],
        'probe_backreaction_detected': exact_nonzero(
            backreaction_validation['linear_residual'].subs(
                {q: 2, backreaction: sp.Rational(1, 4)}
            )
        ),
    }

    closure_flags = {
        'primitive_response_target_symbols_absent_exact': (
            primitive_target_free
        ),
        'completed_square_bounded_exact': (
            exact_zero(residuals['completed_square_minimum'])
            and response_hessian.is_positive
        ),
        'positive_stationary_response_exact': (
            exact_zero(residuals['response_stationarity'])
            and b_star.is_positive
        ),
        'response_hessian_positive_exact': bool(response_hessian.is_positive),
        'dependency_hashes_pinned_exact': all(
            record['valid'] for record in dependencies.values()
        ),
        'density_amplitude_identity_exact': exact_zero(
            residuals['density_amplitude_identity']
        ),
        'selected_restoring_readout_square_law_exact': bool(
            exact_zero(
                residuals['selected_restoring_readout_square_law']
            )
            and exact_zero(
                residuals['selected_restoring_readout_density_map']
            )
            and exact_zero(
                selected_response_validation['linear_residual']
            )
            and exact_zero(
                selected_response_validation['square_readout_residual']
            )
        ),
        'w3_54_eos_underdetermination_exact': (
            w3_54_eos_underdetermination
        ),
        'action_angle_reparametrization_exact': all(
            exact_zero(residuals[key]) for key in (
                'action_angle_J_conservation',
                'canonical_q_rate',
                'canonical_pi_rate',
                'proper_energy_invariant',
            )
        ),
        'process_time_transverse_equations_exact': all(
            exact_zero(residuals[key]) for key in (
                'process_time_q_equation',
                'process_time_pi_equation',
            )
        ),
        'proper_cadence_invariant_exact': exact_zero(
            residuals['proper_phase_rate']
        ) and exact_zero(selected_proper_frequency_validation),
        'selected_probe_coordinate_spectrum_factorization_exact': all(
            exact_zero(residuals[key]) for key in (
                'coordinate_phase_factor',
                'coordinate_transverse_factor_constant_patch',
            )
        ) and exact_zero(selected_coordinate_cadence_validation),
        'dimensionless_spectrum_invariant_exact': exact_zero(
            residuals['dimensionless_spectrum_ratio']
        ),
        'field_pullback_jacobian_exact': all(
            exact_zero(residuals[key]) for key in (
                'field_action_measure_jacobian',
                'field_time_derivative_map',
                'field_spatial_derivative_map',
            )
        ),
        'biconformal_field_pullback_exact_constant_patch': all(
            exact_zero(residuals[key]) for key in (
                'field_time_kinetic_coefficient',
                'field_spatial_gradient_coefficient',
                'field_potential_coefficient',
                'pulled_dispersion',
            )
        ),
        'coordinate_signal_speed_square_exact': exact_zero(
            residuals['coordinate_signal_speed']
        ),
        'coordinate_radius_linear_exact': exact_zero(
            residuals['beta_linked_witness_rms_radius']
        ) and exact_zero(selected_spatial_coframe_validation),
        'external_energy_and_defined_mass_linear_exact': (
            exact_zero(residuals['external_energy_factor'])
            and exact_zero(residuals['external_mass_factor'])
            and exact_zero(residuals['transformed_energy'])
            and exact_zero(residuals['defined_external_mass'])
            and exact_zero(residuals['kinetic_energy_scaling'])
            and exact_zero(residuals['gradient_energy_scaling'])
            and exact_zero(residuals['potential_energy_scaling'])
        ),
        'finite_localized_scaling_witness_exact': all(
            exact_zero(residuals[key]) for key in (
                'localized_witness_energy',
                'localized_witness_second_moment',
                'beta_linked_witness_energy',
                'beta_linked_witness_rms_radius',
            )
        ),
        'positive_field_coefficients_exact': bool(
            kinetic_coefficient.is_positive
            and gradient_coefficient.is_positive
            and potential_coefficient.is_positive
        ),
        'phase_roles_distinct_exact': selected_semantics[
            'phase_roles_distinct'
        ],
        'single_probe_coframe_no_duplicate_source_bookkeeping_registered_exact': bool(
            selected_semantics['single_coframe']
            and selected_semantics['single_registered_source']
            and selected_semantics['no_duplicate_pressure_source']
        ),
        'registered_contract_keysets_exact': False,
        'mutation_controls_pass': all(negative_controls.values()),
        'aggregate_candidate_pass': False,
    }

    scope_flags = {key: False for key in REQUIRED_SCOPE_KEYS}
    benchmark_subs = {B: 2 * B0}
    benchmark = {
        'B_over_B0': 2,
        'p': sp.sstr(beta.subs(benchmark_subs)),
        'P_F_over_P_F0': sp.sstr(
            (pressure_f / pressure_f0).subs(benchmark_subs)
        ),
        'eta_F': sp.sstr(eta_from_amplitude.subs(benchmark_subs)),
        'coordinate_cadence_ratio': sp.sstr(beta.subs(benchmark_subs)),
        'coordinate_radius_ratio': sp.sstr(beta.subs(benchmark_subs)),
        'external_energy_mass_ratio': sp.sstr(beta.subs(benchmark_subs)),
        'coordinate_signal_speed_ratio': sp.sstr(
            beta.subs(benchmark_subs) ** 2
        ),
        'proper_ratios': '1',
    }
    diagnostics = {
        'response_potential': sp.sstr(response_potential),
        'response_solution': sp.sstr(b_star),
        'response_hessian': sp.sstr(response_hessian),
        'pressure_readout': sp.sstr(K * b**2 / 2),
        'normalized_response': sp.sstr(beta),
        'normalized_pressure': sp.sstr(pressure_f / pressure_f0),
        'w3_54_eos_no_go': {
            'family': 'rho_C=kappa*n_C^gamma',
            'healthy_gamma_interval': '1<gamma<=2',
            'gamma_for_sqrt_phase': sp.sstr(gamma_phase),
            'phase_ratio': sp.sstr(phase_ratio_gamma_phase),
            'pressure_ratio': sp.sstr(pressure_ratio_gamma_phase),
            'pressure_ratio_is_not_eta_at_eta_4': exact_nonzero(
                (pressure_ratio_gamma_phase - eta).subs(eta, 4)
            ),
            'alternative_gamma': sp.sstr(gamma_alternative),
            'alternative_phase_ratio': sp.sstr(phase_ratio_alternative),
            'underdetermination_verified': w3_54_eos_underdetermination,
        },
        'field_pullback_factors': {
            'action_measure': sp.sstr(action_measure_factor),
            'proper_time_derivative': sp.sstr(
                proper_time_derivative_factor
            ),
            'proper_spatial_derivative': sp.sstr(
                proper_spatial_derivative_factor
            ),
            'coordinate_volume_on_solution': sp.sstr(
                coordinate_volume_factor
            ),
            'pulled_time_derivative_on_solution': sp.sstr(
                pulled_time_derivative_factor
            ),
            'pulled_spatial_derivative_on_solution': sp.sstr(
                pulled_spatial_derivative_factor
            ),
        },
        'field_lagrangian_coefficients': {
            'time_kinetic': sp.sstr(kinetic_coefficient),
            'spatial_gradient': sp.sstr(gradient_coefficient),
            'potential': sp.sstr(potential_coefficient),
        },
        'field_energy_component_factors': {
            'kinetic': sp.sstr(kinetic_energy_factor),
            'gradient': sp.sstr(gradient_energy_factor),
            'potential': sp.sstr(potential_energy_factor),
        },
        'dispersion': sp.sstr(omega_t_sq),
        'residuals': {
            key: sp.sstr(sp.simplify(value))
            for key, value in residuals.items()
        },
        'benchmark': benchmark,
        'semantic_constraints': semantic_constraints,
    }
    return (
        diagnostics['residuals'], closure_flags, scope_flags,
        negative_controls, diagnostics
    )


def build_report() -> dict[str, object]:
    prereg = verify_preregistration()
    dependencies = verify_dependency_contracts()
    residuals, closure_flags, scope_flags, mutations, diagnostics = (
        derive_candidate(dependencies)
    )
    source_bytes = Path(__file__).read_bytes()
    if b'\r' in source_bytes or not source_bytes.endswith(b'\n'):
        raise RuntimeError('Verifier source is not canonical UTF-8 LF text')

    provenance = {
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'preregistration': prereg,
        'dependency_contracts': dependencies,
        'source': {'path': Path(__file__).name, 'sha256': sha256(Path(__file__))},
        'python': platform.python_version(),
        'sympy': importlib.metadata.version('sympy'),
        'platform': platform.platform(),
        'line_endings': 'LF',
    }
    result: dict[str, object] = {
        'schema_version': '1.0',
        'claim_id': CLAIM_ID,
        'claim': prereg['registered_claim'],
        'type': (
            'EXACT_INTERNAL_ALGEBRA_OF_SELECTED_QUADRATIC_AUXILIARY_'
            'RESPONSE_AND_BICONFORMAL_PROBE_WITNESS'
        ),
        'model_version': MODEL_VERSION,
        'status': 'PENDING',
        'scope_status': 'PENDING',
        'artifact_valid': False,
        'evidence_type': (
            'SELECTED_FIXED_BACKGROUND_RESPONSE_AND_'
            'BICONFORMAL_PULLBACK_CONSISTENCY_WITNESS'
        ),
        'blocking_boundaries': [
            (
                'The quadratic auxiliary operator is selected rather than '
                'derived from the foundation nodes.'
            ),
            (
                'P_F^(R)=K*b^2/2 is a selected restoring-channel intensity; '
                'it is not the on-shell total potential, a Hilbert stress, '
                'or W3-54 thermodynamic p_C.'
            ),
            (
                'The environment-independence of H_0 and the common '
                'biconformal factor are selected probe premises, not '
                'outputs of a localized W3-50 oscillon core.'
            ),
            (
                'The finite Gaussian profile is an independent scaling '
                'witness, not a solved oscillon field or Floquet spectrum.'
            ),
            (
                'A covariant W3-54 embedding, action-derived source ledger, '
                'localized backreaction, and universality remain open.'
            ),
        ],
        'contract': {
            'field_names': prereg['field_names'],
            'preregistration_sha256': prereg['sha256'],
            'dependency_contract_sha256': {
                key: record['sha256']
                for key, record in dependencies.items()
            },
            'primitive_operator_class': 'K*(b-lambda*B)^2/2',
            'pressure_readout': 'P_F^(R)=K*b^2/2',
            'probe_action': (
                'S=integral dt [J_O*theta_O_dot+Pi*Q_dot-beta*H_0]'
            ),
            'profile_pullback': 'tau=beta*t; y=x/beta',
        },
        'closure_flags': closure_flags,
        'scope_flags': scope_flags,
        'identities': residuals,
        'benchmark': diagnostics['benchmark'],
        'semantic_constraints': diagnostics['semantic_constraints'],
        'negative_controls': mutations,
        'diagnostics': {
            key: value for key, value in diagnostics.items()
            if key not in {
                'residuals', 'benchmark', 'semantic_constraints'
            }
        },
        'provenance': provenance,
        'files': {
            'readme': 'README.md',
            'preregistration': PREREG.name,
            'source': Path(__file__).name,
            'result': OUTPUT.name,
            'checksum': HASH_OUTPUT.name,
        },
    }

    keysets_exact = bool(
        set(result) == EXPECTED_RESULT_KEYS
        and set(closure_flags) == REQUIRED_EXACT_KEYS
        and set(scope_flags) == REQUIRED_SCOPE_KEYS
        and set(mutations) == REQUIRED_MUTATION_KEYS
        and set(prereg['field_names']) == REQUIRED_CONTRACT_FIELDS
    )
    closure_flags['registered_contract_keysets_exact'] = keysets_exact
    closure_flags['aggregate_candidate_pass'] = all(
        value for key, value in closure_flags.items()
        if key != 'aggregate_candidate_pass'
    )
    artifact_valid = bool(
        closure_flags['aggregate_candidate_pass']
        and all(value is False for value in scope_flags.values())
    )
    result['artifact_valid'] = artifact_valid
    result['status'] = 'PASS' if artifact_valid else 'FAIL'
    result['scope_status'] = PASS_STATUS if artifact_valid else 'FAIL_W3_56_GATE'
    if not artifact_valid:
        raise RuntimeError('W3-56 aggregate candidate gate failed')
    return result


def write_atomic(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('w', encoding='utf-8', newline='\n') as handle:
        handle.write(text)
    temporary.replace(path)


def write_report(report: dict[str, object]) -> str:
    payload = json.dumps(
        report, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False
    ) + '\n'
    write_atomic(OUTPUT, payload)
    digest = sha256(OUTPUT)
    write_atomic(HASH_OUTPUT, f'{digest}  {OUTPUT.name}\n')
    return digest


def write_failure(error: Exception) -> None:
    failure = {
        'schema_version': '1.0-failure',
        'claim_id': CLAIM_ID,
        'model_version': MODEL_VERSION,
        'status': 'FAIL',
        'artifact_valid': False,
        'error': f'{type(error).__name__}: {error}',
        'generated_utc': datetime.now(timezone.utc).isoformat(),
    }
    payload = json.dumps(
        failure, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False
    ) + '\n'
    write_atomic(OUTPUT, payload)
    digest = sha256(OUTPUT)
    write_atomic(HASH_OUTPUT, f'{digest}  {OUTPUT.name}\n')


def main() -> int:
    try:
        report = build_report()
        digest = write_report(report)
    except Exception as error:
        write_failure(error)
        print(f'FAIL: {error}', file=sys.stderr)
        return 2
    print(report['scope_status'])
    print(f'Result: {OUTPUT}')
    print(f'Result SHA-256: {digest}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
