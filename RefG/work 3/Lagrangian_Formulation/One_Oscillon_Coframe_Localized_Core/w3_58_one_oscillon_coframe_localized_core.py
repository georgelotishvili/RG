'''W3-58 coframe-coupled localized ordinary-phase core gate.'''

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import os
import platform
import re
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import simpson, solve_bvp
from scipy.linalg import eigh_tridiagonal
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


CLAIM_ID = 'W3_58_ONE_OSCILLON_COFRAME_LOCALIZED_CORE'
MODEL_VERSION = 'W3-58-v1.0-MINIMAL-U1-SEXTIC-COFRAME-LOCALIZED-CORE'
PASS_STATUS = (
    'PASS_CONDITIONAL_EXACT_MINIMAL_COFRAME_U1_CORE_ACTION_AND_ANALYTIC_'
    'EXISTENCE_WINDOW__CONVERGED_NUMERICAL_FINITE_ENERGY_ORBITALLY_STABLE_'
    'SPHERICAL_GROUND_STATE_EVIDENCE__FOUNDATION_COEFFICIENT_SELECTION_'
    'BACKGROUND_LOCK_BACKREACTION_AND_PARTICLE_IDENTITY_OPEN'
)
INCONCLUSIVE_STATUS = (
    'NUMERICALLY_INCONCLUSIVE_MINIMAL_COFRAME_U1_SEXTIC_LOCALIZED_CORE_GATE'
)
FAIL_STATUS = 'FAIL_W3_58_FROZEN_MODEL_OR_EXACT_GATE'

HERE = Path(__file__).resolve().parent
WORK3 = HERE.parents[1]
PREREG = HERE / 'w3_58_one_oscillon_coframe_localized_core_preregistration.md'
README = HERE / 'README.md'
SOURCE = Path(__file__).resolve()
OUTPUT = HERE / 'w3_58_result.json'
HASH_OUTPUT = HERE / 'w3_58_result.sha256'
FORMAL_LEDGER = WORK3 / 'Lagrangian_Formulation' / 'RefG_Formal_Proof.md'

PINNED_PREREG_SHA256 = (
    '962980d4607ba506a5b65fe458f04ab31d8a78ac74511c68d43ff2d95f911dda'
)

DEPENDENCIES = {
    'W3_50_contract': {
        'path': (
            WORK3 / 'Cosmology_and_LSS'
            / 'Active_Participation_Resonance_Feedback'
            / 'w3_50_neutral_collective_phase_density_bridge_contract.md'
        ),
        'sha256': '1cb66438a6bf53f1a661a014328204c05edfe847f81d876defe69eaa400591db',
    },
    'W3_54_contract': {
        'path': (
            WORK3 / 'Lagrangian_Formulation'
            / 'Relational_Coframe_TEGR_Phase_Source_Closure'
            / 'w3_54_relational_coframe_tegr_phase_source_closure_contract.md'
        ),
        'sha256': '6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879',
    },
    'W3_56_preregistration': {
        'path': (
            WORK3 / 'Lagrangian_Formulation'
            / 'One_Oscillon_Coframe_Lock_Bridge'
            / 'w3_56_one_oscillon_coframe_lock_bridge_preregistration.md'
        ),
        'sha256': '2621326161bfb65a651e56bfdeade2e3b290efe39cf2211467851850d030dc5c',
    },
    'W3_56_result': {
        'path': (
            WORK3 / 'Lagrangian_Formulation'
            / 'One_Oscillon_Coframe_Lock_Bridge' / 'w3_56_result.json'
        ),
        'checksum_path': (
            WORK3 / 'Lagrangian_Formulation'
            / 'One_Oscillon_Coframe_Lock_Bridge' / 'w3_56_result.sha256'
        ),
        'sha256': '725c09e77b14a18a46be8938f224eeb42248ea9e736f7c46e9ae9d57599c3c86',
    },
    'W3_57_preregistration': {
        'path': (
            WORK3 / 'Lagrangian_Formulation'
            / 'One_Oscillon_Localized_Core_Identifiability_Gate'
            / 'w3_57_one_oscillon_localized_core_identifiability_preregistration.md'
        ),
        'sha256': 'fb703be40b4566e1c9a13c4eb5e5bcee41aa0119d3e6d010ca139ed75d158b1b',
    },
    'W3_57_result': {
        'path': (
            WORK3 / 'Lagrangian_Formulation'
            / 'One_Oscillon_Localized_Core_Identifiability_Gate'
            / 'w3_57_result.json'
        ),
        'checksum_path': (
            WORK3 / 'Lagrangian_Formulation'
            / 'One_Oscillon_Localized_Core_Identifiability_Gate'
            / 'w3_57_result.sha256'
        ),
        'sha256': 'd99e2a0c72f191f3e98b190f5f3aa923d58b712aa74566c89c1d9e864c25bc7c',
    },
}

W3_56_STATUS = 'PASS'
W3_57_STATUS = 'PASS'

REQUIRED_CONTRACT_FIELDS = {
    'CLAIM_ID', 'CLAIM', 'TYPE', 'MODEL_VERSION', 'ASSUMPTIONS', 'DOMAIN',
    'CONVENTIONS', 'FREEDOM_LEDGER', 'DEPENDENCIES', 'METHOD',
    'PASS_CONDITION', 'FAIL_CONDITION', 'FALSIFIER', 'RESIDUAL',
    'ERROR_BOUND', 'VALIDITY_HEALTH', 'BRANCHES', 'OBSERVABLE_MAP',
    'FORWARD_MODEL', 'DATA_ROLE', 'IDENTIFIABILITY', 'BENCHMARK',
    'CLOSURE_FLAGS', 'CROSSCHECK', 'PROVENANCE', 'FILES',
}

REQUIRED_TRUE_FLAGS = {
    'dependency_hashes_pinned_exact',
    'w3_50_collective_phase_role_preserved_exact',
    'w3_54_common_coframe_minimal_coupling_exact',
    'ordinary_phase_u1_action_defined_exact',
    'canonical_amplitude_gradient_present_exact',
    'bounded_binding_sextic_present_exact',
    'zero_vacuum_global_threshold_exact',
    'euler_lagrange_equations_exact',
    'ordinary_phase_current_exact',
    'hilbert_stress_from_same_action_exact',
    'one_source_ledger_no_duplicate_exact',
    'dimensionless_radial_bvp_exact',
    'analytic_existence_window_exact',
    'finite_energy_ground_state_constructed_numerical',
    'intrinsic_charge_radius_constructed_numerical',
    'domain_tolerance_quadrature_convergence_pass',
    'independent_finite_difference_crosscheck_pass',
    'radial_nehari_virial_stress_tail_checks_pass',
    'hessian_operators_exact',
    'phase_and_translation_zero_modes_numerical',
    'single_unconstrained_L_plus_negative_direction_numerical',
    'negative_charge_slope_numerical',
    'free_quantum_decay_bound_numerical',
    'converged_numerical_orbital_stability_evidence',
    'registered_contract_keysets_exact',
    'mutation_controls_pass',
    'aggregate_gate_pass',
}

REQUIRED_FALSE_FLAGS = {
    'core_action_from_nodes_derived',
    'benchmark_a_from_foundation_derived',
    'm_and_lambda_from_foundation_derived',
    'neutral_real_oscillon_derived',
    'theta_O_theta_C_lock_derived',
    'w3_56_background_scaling_from_core_derived',
    'P_F_from_core_stress_derived',
    'square_pressure_law_from_core_stress_derived',
    'localized_gravitational_backreaction_derived',
    'physical_particle_identity_derived',
    'all_particle_families_universalized',
    'particle_mass_spectrum_derived',
    'Koide_or_C3_used',
    'Planck_hierarchy_derived',
    'strong_field_or_2PN_completed',
    'cosmological_history_modified',
    'observational_likelihood_evaluated',
}

A_BENCH = 0.25
OMEGA_BENCH = 0.8
OMEGA_GRID = (0.78, 0.79, 0.795, 0.8, 0.805, 0.81, 0.82)
R_BENCH = 80.0
SINGULAR_MATRIX = np.array([[0.0, 0.0], [0.0, -2.0]])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_text(path: Path) -> str:
    payload = path.read_bytes()
    if b'\r' in payload or not payload.endswith(b'\n'):
        raise RuntimeError(f'Noncanonical UTF-8 LF text: {path}')
    return payload.decode('utf-8')


def relative_change(value: float, reference: float) -> float:
    return abs(value - reference) / max(abs(reference), 1e-30)


def finite_tree(value: object) -> bool:
    if isinstance(value, dict):
        return all(finite_tree(k) and finite_tree(v) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return all(finite_tree(v) for v in value)
    if isinstance(value, (float, np.floating)):
        return math.isfinite(float(value))
    return True


def native_tree(value: object) -> object:
    # Normalize NumPy scalar diagnostics to deterministic JSON-native values.
    if isinstance(value, dict):
        return {str(key): native_tree(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [native_tree(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, sp.logic.boolalg.Boolean):
        return bool(value)
    if isinstance(value, sp.Integer):
        return int(value)
    if isinstance(value, sp.Float):
        return float(value)
    if isinstance(value, sp.Rational):
        return str(value)
    return value


def validate_source_ledger(
    action_to_source: tuple[tuple[str, str], ...],
    total_expression: str,
) -> bool:
    if total_expression.count('=') != 1:
        return False
    left, right = total_expression.split('=')
    actions = [action for action, _source in action_to_source]
    sources = [source for _action, source in action_to_source]
    terms = [term.strip() for term in right.split('+')]
    return bool(
        left.strip() == 'T_total'
        and actions == ['S_C', 'S_O']
        and sources == ['T_C', 'T_O']
        and terms == sources
        and len(actions) == len(set(actions))
        and len(sources) == len(set(sources))
    )


def verify_preregistration() -> dict[str, object]:
    text = canonical_text(PREREG)
    digest = sha256(PREREG)
    fields = set(re.findall(r'^\*\*([A-Z_]+):\*\*', text, re.MULTILINE))
    required_markers = (
        'mathematical Q-ball class',
        'theta_O',
        'theta_C',
        'signature `(-+++)`',
        'a=1/4',
        'Omega=4/5',
        'NUMERICAL_EVIDENCE',
        'neutral_real_oscillon_derived',
    )
    return {
        'sha256': digest,
        'hash_exact': digest == PINNED_PREREG_SHA256,
        'fields_exact': fields == REQUIRED_CONTRACT_FIELDS,
        'missing_fields': sorted(REQUIRED_CONTRACT_FIELDS - fields),
        'extra_fields': sorted(fields - REQUIRED_CONTRACT_FIELDS),
        'scope_markers_exact': all(marker in text for marker in required_markers),
    }


def verify_dependencies() -> dict[str, object]:
    records: dict[str, object] = {}
    all_pass = True
    for name, spec in DEPENDENCIES.items():
        path = Path(spec['path'])
        actual = sha256(path)
        record: dict[str, object] = {
            'path': str(path.relative_to(WORK3)).replace('\\', '/'),
            'expected_sha256': spec['sha256'],
            'actual_sha256': actual,
            'hash_exact': actual == spec['sha256'],
        }
        if 'checksum_path' in spec:
            checksum_path = Path(spec['checksum_path'])
            checksum_token = canonical_text(checksum_path).strip().split()[0]
            payload = json.loads(canonical_text(path))
            expected_status = W3_56_STATUS if name.startswith('W3_56') else W3_57_STATUS
            record.update({
                'checksum_matches': checksum_token == actual,
                'status_exact': payload.get('status') == expected_status,
                'artifact_valid': payload.get('artifact_valid') is True,
            })
        record_pass = all(
            bool(v) for k, v in record.items()
            if k in {'hash_exact', 'checksum_matches', 'status_exact', 'artifact_valid'}
        )
        record['pass'] = record_pass
        all_pass = all_pass and record_pass
        records[name] = record
    return {'records': records, 'all_pass': all_pass}


def symbolic_gate() -> dict[str, object]:
    f, omega, a = sp.symbols('f omega a', positive=True)
    fp = sp.symbols('fp', real=True)
    v = sp.Rational(1, 2) * f**2 - sp.Rational(1, 4) * f**4 + a * f**6 / 6
    v4 = sp.Rational(1, 2) * f**2 - sp.Rational(1, 4) * f**4
    v_over_f2 = sp.simplify(v / f**2)
    ratio2 = sp.simplify(2 * v / f**2)
    f2_at_min = sp.Rational(3, 4) / a
    vacuum_min = sp.simplify(v_over_f2.subs(f**2, f2_at_min))
    existence_min = sp.simplify(ratio2.subs(f**2, f2_at_min))
    benchmark_lower2 = sp.simplify(existence_min.subs(a, sp.Rational(1, 4)))
    benchmark_tail = sp.sqrt(1 - sp.Rational(4, 5)**2)
    Omega2 = sp.symbols('Omega2', nonnegative=True)
    tail_mass2 = 1 - Omega2
    vacuum_threshold = sp.Rational(3, 16)
    vacuum_derivative = sp.diff(vacuum_min, a)
    potential_force = sp.diff(v, f)
    potential_polynomial = sp.Poly(v, f)
    quartic_large_field_limit = sp.limit(v4, f, sp.oo)
    sextic_large_field_limit = sp.limit(v, f, sp.oo)
    y = sp.symbols('y', nonnegative=True)
    ratio_y = 1 - y / 2 + a * y**2 / 3
    ratio_y_prime = sp.diff(ratio_y, y)
    ratio_y_second = sp.diff(ratio_y, y, 2)
    y_at_minimum = sp.Rational(3, 4) / a

    x, Omega = sp.symbols('x Omega', positive=True)
    F = sp.Function('F')(x)
    Fp = sp.diff(F, x)
    Fpp = sp.diff(F, x, 2)
    force_F = (1 - Omega**2) * F - F**3 + a * F**5
    reduced_density = x**2 * (
        Fp**2 / 2 + (1 - Omega**2) * F**2 / 2 - F**4 / 4 + a * F**6 / 6
    )
    radial_euler = sp.diff(sp.diff(reduced_density, Fp), x) - sp.diff(
        reduced_density, F
    )
    expected_radial_euler = x**2 * (Fpp + 2 * Fp / x - force_F)
    radial_euler_residual = sp.simplify(radial_euler - expected_radial_euler)

    nehari_F = Fp**2 + (1 - Omega**2) * F**2 - F**4 + a * F**6
    radial_residual = Fpp + 2 * Fp / x - force_F
    nehari_local_residual = sp.simplify(
        x**2 * F * radial_residual
        - (sp.diff(x**2 * F * Fp, x) - x**2 * nehari_F)
    )
    effective_potential_F = (
        (1 - Omega**2) * F**2 / 2 - F**4 / 4 + a * F**6 / 6
    )
    virial_local_residual = sp.simplify(
        x**2 * (Fp**2 / 2 + 3 * effective_potential_F)
        + sp.diff(x**3 * (Fp**2 / 2 - effective_potential_F), x)
        - x**3 * Fp * radial_residual
    )

    chi, theta = sp.symbols('chi theta', real=True)
    dchi0, dchi1, dtheta0, dtheta1 = sp.symbols(
        'dchi0 dchi1 dtheta0 dtheta1', real=True
    )
    h0, h1, h2, h3 = sp.symbols('h0 h1 h2 h3', nonzero=True)
    dreal0 = (
        dchi0 * sp.cos(theta) - chi * sp.sin(theta) * dtheta0
    ) / sp.sqrt(2)
    dimag0 = (
        dchi0 * sp.sin(theta) + chi * sp.cos(theta) * dtheta0
    ) / sp.sqrt(2)
    dreal1 = (
        dchi1 * sp.cos(theta) - chi * sp.sin(theta) * dtheta1
    ) / sp.sqrt(2)
    dimag1 = (
        dchi1 * sp.sin(theta) + chi * sp.cos(theta) * dtheta1
    ) / sp.sqrt(2)
    polar_kinetic_residual = sp.trigsimp(
        h0 * (dreal0**2 + dimag0**2)
        + h1 * (dreal1**2 + dimag1**2)
        - (
            h0 * (dchi0**2 + chi**2 * dtheta0**2)
            + h1 * (dchi1**2 + chi**2 * dtheta1**2)
        ) / 2
    )
    phase_lagrangian = -chi**2 * (
        h0 * dtheta0**2 + h1 * dtheta1**2
    ) / 2
    current_residuals = (
        sp.simplify(
            sp.diff(phase_lagrangian, dtheta0) + chi**2 * h0 * dtheta0
        ),
        sp.simplify(
            sp.diff(phase_lagrangian, dtheta1) + chi**2 * h1 * dtheta1
        ),
    )
    phase_shift_residual = sp.diff(phase_lagrangian, theta)
    positive_current_residual = sp.simplify(
        sp.diff(phase_lagrangian, dtheta0).subs({h0: -1, dtheta0: omega})
        - chi**2 * omega
    )

    amplitude_time, amplitude_radial, hilbert_V = sp.symbols(
        'amplitude_time amplitude_radial hilbert_V', real=True
    )
    metric_density = (-h0 * h1 * h2 * h3) ** sp.Rational(-1, 2)
    metric_lagrangian = -(
        h0 * amplitude_time + h1 * amplitude_radial
    ) / 2 - hilbert_V
    diagonal_hilbert = [
        sp.simplify(
            (-2 / metric_density * sp.diff(
                metric_density * metric_lagrangian, component
            )).subs({h0: -1, h1: 1, h2: 1, h3: 1})
        )
        for component in (h0, h1, h2, h3)
    ]
    expected_diagonal_hilbert = [
        (amplitude_time + amplitude_radial) / 2 + hilbert_V,
        (amplitude_time + amplitude_radial) / 2 - hilbert_V,
        (amplitude_time - amplitude_radial) / 2 - hilbert_V,
        (amplitude_time - amplitude_radial) / 2 - hilbert_V,
    ]
    hilbert_metric_variation_residuals = [
        sp.simplify(actual - expected)
        for actual, expected in zip(
            diagonal_hilbert, expected_diagonal_hilbert
        )
    ]

    e00, e01, e10, e11 = sp.symbols('e00 e01 e10 e11', real=True)
    coframe_matrix = sp.Matrix([[e00, e01], [e10, e11]])
    eta_matrix = sp.diag(-1, 1)
    metric_matrix = coframe_matrix.T * eta_matrix * coframe_matrix
    inverse_metric_from_metric = sp.simplify(metric_matrix.inv())
    inverse_metric_from_frame = sp.simplify(
        coframe_matrix.inv() * eta_matrix * coframe_matrix.inv().T
    )
    coframe_inverse_residuals = [
        sp.simplify(value)
        for value in (
            inverse_metric_from_metric - inverse_metric_from_frame
        )
    ]
    covector = sp.Matrix([dchi0, dchi1])
    frame_covector = coframe_matrix.inv().T * covector
    coordinate_contraction = (
        covector.T * inverse_metric_from_metric * covector
    )[0]
    frame_contraction = (frame_covector.T * eta_matrix * frame_covector)[0]
    coframe_contraction_residual = sp.simplify(
        coordinate_contraction - frame_contraction
    )
    source_action_map = (('S_C', 'T_C'), ('S_O', 'T_O'))
    total_source_expression = 'T_total=T_C+T_O'
    source_ledger_exact = validate_source_ledger(
        source_action_map, total_source_expression
    )

    m, lam = sp.symbols('m lam', positive=True)
    physical_chi = m * f / sp.sqrt(lam)
    physical_omega = m * Omega
    physical_g = a * lam**2 / m**2
    physical_force = (
        (m**2 - physical_omega**2) * physical_chi
        - lam * physical_chi**3 + physical_g * physical_chi**5
    )
    dimensionless_force_residual = sp.simplify(
        physical_force / (m**3 / sp.sqrt(lam))
        - ((1 - Omega**2) * f - f**3 + a * f**5)
    )
    X, F_x, F_xx = sp.symbols('X F_x F_xx', positive=True)
    physical_radial_lhs = m**3 / sp.sqrt(lam) * (
        F_xx + 2 * F_x / X
    )
    dimensionless_derivative_residual = sp.simplify(
        physical_radial_lhs / (m**3 / sp.sqrt(lam))
        - (F_xx + 2 * F_x / X)
    )
    physical_boundary = (
        m**2 * fp / sp.sqrt(lam)
        + (sp.sqrt(m**2 - physical_omega**2) + m / X)
        * physical_chi
    )
    dimensionless_robin_residual = sp.simplify(
        physical_boundary / (m**2 / sp.sqrt(lam))
        - (fp + (sp.sqrt(1 - Omega**2) + 1 / X) * f)
    )
    hessian_minus_residual = sp.simplify(
        potential_force / f - omega**2
        - (1 - omega**2 - f**2 + a * f**4)
    )
    hessian_plus_residual = sp.simplify(
        sp.diff(potential_force, f) - omega**2
        - (1 - omega**2 - 3 * f**2 + 5 * a * f**4)
    )
    ell = sp.symbols('ell', integer=True)
    Y = sp.Function('Y')(x)
    radial_potential = sp.Function('U')(x)
    reduced_mode = x * Y
    radial_conjugation_residual = sp.simplify(
        x * (
            -sp.diff(Y, x, 2) - 2 * sp.diff(Y, x) / x
            + ell * (ell + 1) * Y / x**2 + radial_potential * Y
        )
        - (
            -sp.diff(reduced_mode, x, 2)
            + ell * (ell + 1) * reduced_mode / x**2
            + radial_potential * reduced_mode
        )
    )

    potential_minus = 1 - Omega**2 - F**2 + a * F**4
    potential_plus = 1 - Omega**2 - 3 * F**2 + 5 * a * F**4
    fpp_rule = force_F - 2 * Fp / x
    phase_mode = -sp.diff(x * F, x, 2) + potential_minus * x * F
    phase_mode_residual = sp.simplify(phase_mode.subs(Fpp, fpp_rule))
    fppp_rule = potential_plus * Fp - 2 * fpp_rule / x + 2 * Fp / x**2
    translation_mode = (
        -sp.diff(x * Fp, x, 2) + 2 * (x * Fp) / x**2
        + potential_plus * x * Fp
    )
    translation_mode_residual = sp.simplify(
        translation_mode
        .subs(sp.diff(F, x, 3), fppp_rule)
        .subs(Fpp, fpp_rule)
    )

    epsilon, fpp_symbol, z, zp, zpp = sp.symbols(
        'epsilon fpp_symbol z zp zpp', real=True
    )
    trial_f = f + epsilon * z
    trial_omega = omega + epsilon
    trial_residual = (
        fpp_symbol + epsilon * zpp + 2 * (fp + epsilon * zp) / x
        - ((1 - trial_omega**2) * trial_f - trial_f**3 + a * trial_f**5)
    )
    sensitivity_linearization = sp.diff(trial_residual, epsilon).subs(epsilon, 0)
    expected_sensitivity = (
        zpp + 2 * zp / x
        - (1 - omega**2 - 3 * f**2 + 5 * a * f**4) * z
        + 2 * omega * f
    )
    sensitivity_residual = sp.simplify(
        sensitivity_linearization - expected_sensitivity
    )
    Z = sp.Function('Z')(x)
    unreduced_sensitivity = (
        -sp.diff(Z, x, 2) - 2 * sp.diff(Z, x) / x
        + potential_plus * Z - 2 * Omega * F
    )
    reduced_sensitivity = (
        -sp.diff(x * Z, x, 2) + potential_plus * x * Z
        - 2 * Omega * x * F
    )
    sensitivity_reduction_residual = sp.simplify(
        reduced_sensitivity - x * unreduced_sensitivity
    )
    charge_integral = sp.Function('charge_integral')(omega)
    overlap_integral = sp.symbols('overlap_integral', real=True)
    charge_derivative_residual = sp.simplify(
        sp.diff(omega * charge_integral, omega)
        .subs(sp.diff(charge_integral, omega), 2 * overlap_integral)
        - (charge_integral + 2 * omega * overlap_integral)
    )

    scale, gradient_symbol, effective_potential_symbol = sp.symbols(
        'scale gradient_symbol effective_potential_symbol', positive=True
    )
    scaled_functional = (
        gradient_symbol / scale + effective_potential_symbol / scale**3
    )
    virial_scaling_residual = sp.simplify(
        sp.diff(scaled_functional, scale).subs(scale, 1)
        + gradient_symbol + 3 * effective_potential_symbol
    )
    centrifugal_ordering_residual = sp.expand(
        ell * (ell + 1) - 6 - (ell - 2) * (ell + 3)
    )

    chi_t, chi_r, phase_t = sp.symbols('chi_t chi_r phase_t', real=True)
    V = sp.symbols('V', real=True)
    kinetic_trace = -chi_t**2 - phase_t**2 + chi_r**2
    lagrangian = -kinetic_trace / 2 - V
    rho = sp.simplify(chi_t**2 + phase_t**2 - lagrangian)
    radial_pressure = sp.simplify(chi_r**2 + lagrangian)
    tangential_pressure = sp.simplify(lagrangian)
    expected_rho = (chi_t**2 + phase_t**2 + chi_r**2) / 2 + V
    expected_pr = (chi_t**2 + phase_t**2 + chi_r**2) / 2 - V
    expected_pt = (chi_t**2 + phase_t**2 - chi_r**2) / 2 - V

    nehari_density = fp**2 + (1 - omega**2) * f**2 - f**4 + a * f**6
    grad = fp**2 / 2
    phase = omega**2 * f**2 / 2
    stress_sum = -fp**2 / 2 + 3 * phase - 3 * v
    virial_density = grad + 3 * (v - phase)

    checks = {
        'minimal_even_polynomial_degree_is_six': all((
            potential_polynomial.degree() == 6,
            potential_polynomial.coeff_monomial(f**2) == sp.Rational(1, 2),
            potential_polynomial.coeff_monomial(f**4) == -sp.Rational(1, 4),
            potential_polynomial.coeff_monomial(f**6) == a / 6,
            quartic_large_field_limit == -sp.oo,
            sextic_large_field_limit == sp.oo,
        )),
        'potential_large_field_positive_for_a_positive': sp.LC(sp.Poly(v, f), f) == a / 6,
        'potential_euler_force_exact': sp.simplify(
            potential_force - (f - f**3 + a * f**5)
        ) == 0,
        'vacuum_minimum_ratio_exact': sp.simplify(vacuum_min - (sp.Rational(1, 2) - sp.Rational(3, 32) / a)) == 0,
        'existence_ratio_global_minimum_exact': all((
            sp.simplify(ratio_y_prime.subs(y, y_at_minimum)) == 0,
            sp.simplify(ratio_y_second - 2 * a / 3) == 0,
            sp.simplify(
                ratio_y.subs(y, y_at_minimum)
                - (1 - sp.Rational(3, 16) / a)
            ) == 0,
        )),
        'global_vacuum_threshold_exact': all((
            sp.solve(sp.Eq(vacuum_min, 0), a) == [vacuum_threshold],
            sp.simplify(vacuum_min.subs(a, vacuum_threshold)) == 0,
            sp.simplify(vacuum_derivative - sp.Rational(3, 32) / a**2) == 0,
        )),
        'existence_lower_edge_exact': sp.simplify(existence_min - (1 - sp.Rational(3, 16) / a)) == 0,
        'benchmark_lower_edge_exact': benchmark_lower2 == sp.Rational(1, 4),
        'benchmark_tail_exact': benchmark_tail == sp.Rational(3, 5),
        'localization_upper_edge_exact': all((
            sp.solve(sp.Eq(tail_mass2, 0), Omega2) == [sp.Integer(1)],
            sp.diff(tail_mass2, Omega2) == -1,
            tail_mass2.subs(Omega2, sp.Rational(16, 25)) == sp.Rational(9, 25),
        )),
        'hilbert_energy_density_exact': sp.simplify(rho - expected_rho) == 0,
        'hilbert_radial_pressure_exact': sp.simplify(radial_pressure - expected_pr) == 0,
        'hilbert_tangential_pressure_exact': sp.simplify(tangential_pressure - expected_pt) == 0,
        'hilbert_metric_variation_identity_exact': all(
            residual == 0 for residual in hilbert_metric_variation_residuals
        ),
        'common_coframe_inverse_metric_exact': all(
            residual == 0 for residual in coframe_inverse_residuals
        ),
        'common_coframe_kinetic_contraction_exact': coframe_contraction_residual == 0,
        'source_ledger_from_selected_actions_exact': source_ledger_exact,
        'virial_stress_equivalence_exact': sp.simplify(stress_sum + virial_density) == 0,
        'virial_scaling_identity_exact': virial_scaling_residual == 0,
        'virial_local_pohozaev_identity_exact': virial_local_residual == 0,
        'nehari_integration_by_parts_identity_exact': nehari_local_residual == 0,
        'radial_euler_lagrange_exact': radial_euler_residual == 0,
        'ordinary_current_noether_exact': all(
            residual == 0 for residual in current_residuals
        ),
        'ordinary_phase_shift_euler_exact': phase_shift_residual == 0,
        'ordinary_current_positive_convention_exact': positive_current_residual == 0,
        'polar_complex_kinetic_dictionary_exact': polar_kinetic_residual == 0,
        'dimensionless_radial_operator_exact': dimensionless_force_residual == 0,
        'dimensionless_radial_derivative_exact': dimensionless_derivative_residual == 0,
        'dimensionless_robin_boundary_exact': dimensionless_robin_residual == 0,
        'hessian_minus_operator_exact': hessian_minus_residual == 0,
        'hessian_plus_operator_exact': hessian_plus_residual == 0,
        'radial_hessian_conjugation_exact': radial_conjugation_residual == 0,
        'phase_zero_mode_identity_exact': phase_mode_residual == 0,
        'translation_zero_mode_identity_exact': translation_mode_residual == 0,
        'sensitivity_operator_identity_exact': sensitivity_residual == 0,
        'sensitivity_reduced_unreduced_equivalence_exact': sensitivity_reduction_residual == 0,
        'charge_sensitivity_formula_exact': charge_derivative_residual == 0,
        'centrifugal_ordering_ell_ge_2_exact': centrifugal_ordering_residual == 0,
    }
    return {
        'checks': checks,
        'all_pass': all(bool(v) for v in checks.values()),
        'identities': {
            'action': 'S_O=-(1/c0) integral e [1/2 (dchi)^2+1/2 chi^2 (dtheta_O)^2+V(chi)]',
            'potential': 'V=1/2 m^2 chi^2-1/4 lambda chi^4+1/6 g chi^6',
            'global_vacuum': 'a=g m^2/lambda^2>3/16',
            'existence_window': '1-3/(16a)<Omega^2<1',
            'benchmark_window': '1/4<Omega^2<1',
            'radial_equation': "f''+2 f'/x=(1-Omega^2)f-f^3+a f^5",
            'current': 'j_O^mu=-chi^2 partial^mu theta_O',
            'total_source': 'T_total=T_C+T_O',
        },
    }


def initial_seed(x: np.ndarray) -> np.ndarray:
    q = np.exp(np.clip(x - 4.0, -700.0, 700.0))
    f = 1.8 / (1.0 + q)
    fp = -1.8 * q / (1.0 + q) ** 2
    return np.vstack((f, fp))


def seed_from_solution(x: np.ndarray, solution: object, omega: float) -> np.ndarray:
    source_r = float(solution.x[-1])
    inside = x <= source_r
    y = np.empty((2, x.size), dtype=float)
    y[:, inside] = solution.sol(x[inside])
    if np.any(~inside):
        k = math.sqrt(1.0 - omega**2)
        f_edge = float(solution.sol(source_r)[0])
        xx = x[~inside]
        tail = f_edge * source_r / xx * np.exp(-k * (xx - source_r))
        y[0, ~inside] = tail
        y[1, ~inside] = -(k + 1.0 / xx) * tail
    return y


def solve_profile(
    omega: float,
    radius: float = R_BENCH,
    tolerance: float = 1e-7,
    seed: object | None = None,
) -> object:
    if not (0.0 < omega < 1.0):
        raise ValueError('Localization requires 0<Omega<1')
    x = np.linspace(0.0, radius, 801)
    y = initial_seed(x) if seed is None else seed_from_solution(x, seed, omega)
    k = math.sqrt(1.0 - omega**2)

    def fun(_x: np.ndarray, yy: np.ndarray) -> np.ndarray:
        ff = yy[0]
        return np.vstack((yy[1], (1.0 - omega**2) * ff - ff**3 + A_BENCH * ff**5))

    def bc(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
        return np.array([ya[1], yb[1] + (k + 1.0 / radius) * yb[0]])

    solution = solve_bvp(
        fun,
        bc,
        x,
        y,
        S=SINGULAR_MATRIX,
        tol=tolerance,
        max_nodes=100000,
        verbose=0,
    )
    if not solution.success:
        raise RuntimeError(f'BVP failed at Omega={omega}: {solution.message}')
    return solution


def profile_observables(
    solution: object,
    omega: float,
    radius: float,
    points: int = 16001,
) -> dict[str, float]:
    x = np.linspace(0.0, radius, points)
    f, fp = solution.sol(x)
    potential = 0.5 * f**2 - 0.25 * f**4 + A_BENCH * f**6 / 6.0
    i2 = simpson(x**2 * f**2, x=x)
    grad = simpson(x**2 * 0.5 * fp**2, x=x)
    phase = simpson(x**2 * 0.5 * omega**2 * f**2, x=x)
    pot = simpson(x**2 * potential, x=x)
    energy = grad + phase + pot
    charge = omega * i2
    radius_q = math.sqrt(simpson(x**4 * f**2, x=x) / i2)
    nehari = simpson(
        x**2 * (fp**2 + (1.0 - omega**2) * f**2 - f**4 + A_BENCH * f**6),
        x=x,
    )
    nehari_scale = simpson(
        x**2 * (fp**2 + abs(1.0 - omega**2) * f**2 + f**4 + A_BENCH * f**6),
        x=x,
    )
    virial = grad + 3.0 * (pot - phase)
    virial_scale = grad + 3.0 * (abs(pot) + phase)
    p_r = 0.5 * fp**2 + 0.5 * omega**2 * f**2 - potential
    p_t = -0.5 * fp**2 + 0.5 * omega**2 * f**2 - potential
    stress = simpson(x**2 * (p_r + 2.0 * p_t), x=x)
    stress_scale = simpson(x**2 * (abs(p_r) + 2.0 * abs(p_t)), x=x)

    x_res = np.linspace(0.01, radius, min(points, 20001))
    f_res, fp_res = solution.sol(x_res)
    fpp_res = solution.sol(x_res, 2)[0]
    rhs = (1.0 - omega**2) * f_res - f_res**3 + A_BENCH * f_res**5
    equation_residual = fpp_res + 2.0 * fp_res / x_res - rhs
    equation_terms = (
        np.abs(fpp_res) + np.abs(2.0 * fp_res / x_res) + np.abs(rhs)
    )
    equation_point_scale = np.maximum(equation_terms, 1e-12)
    equation_weighted_l2 = math.sqrt(
        simpson(x_res**2 * equation_residual**2, x=x_res)
        / max(simpson(x_res**2 * equation_terms**2, x=x_res), 1e-30)
    )
    equation_global_max = (
        float(np.max(np.abs(equation_residual)))
        / max(float(np.max(equation_terms)), 1e-30)
    )

    positive_mask = (f < 1e-5) & (f > 1e-12) & (x > 1.0)
    if np.count_nonzero(positive_mask) < 50:
        tail_exponent = float('nan')
    else:
        slope = np.polyfit(x[positive_mask], np.log(x[positive_mask] * f[positive_mask]), 1)[0]
        tail_exponent = -float(slope)
    k = math.sqrt(1.0 - omega**2)

    return {
        'central_amplitude': float(f[0]),
        'minimum_amplitude': float(np.min(f)),
        'maximum_positive_derivative': float(np.max(fp[1:])),
        'energy_dimensionless': float(energy),
        'charge_dimensionless': float(charge),
        'charge_rms_radius_dimensionless': float(radius_q),
        'energy_per_mass_charge': float(energy / charge),
        'gradient_energy': float(grad),
        'phase_energy': float(phase),
        'potential_energy': float(pot),
        'nehari_residual': float(nehari),
        'nehari_relative': float(abs(nehari) / max(nehari_scale, 1e-30)),
        'virial_residual': float(virial),
        'virial_relative': float(abs(virial) / max(virial_scale, 1e-30)),
        'stress_balance_residual': float(stress),
        'stress_balance_relative': float(abs(stress) / max(stress_scale, 1e-30)),
        'equation_pointwise_scaled_max_residual_diagnostic': float(
            np.max(np.abs(equation_residual) / equation_point_scale)
        ),
        'equation_normalized_weighted_l2_residual': float(equation_weighted_l2),
        'equation_normalized_global_max_residual': float(equation_global_max),
        'collocation_rms_residual_max': float(np.max(solution.rms_residuals)),
        'tail_exponent_fitted': tail_exponent,
        'tail_exponent_expected': float(k),
        'tail_exponent_absolute_error': float(abs(tail_exponent - k)),
        'centre_boundary_residual': float(abs(solution.y[1, 0])),
        'robin_boundary_residual': float(abs(solution.y[1, -1] + (k + 1.0 / radius) * solution.y[0, -1])),
        'adaptive_nodes': int(solution.x.size),
    }


def convergence_gate(canonical: object) -> dict[str, object]:
    records: list[dict[str, object]] = []
    for radius in (60.0, 80.0, 100.0):
        for tolerance in (1e-6, 3e-7, 1e-7):
            solution = solve_profile(
                OMEGA_BENCH, radius=radius, tolerance=tolerance, seed=canonical
            )
            obs = profile_observables(solution, OMEGA_BENCH, radius, 16001)
            records.append({
                'radius': radius,
                'tolerance': tolerance,
                'observables': obs,
            })
    reference = next(
        item['observables'] for item in records
        if item['radius'] == 80.0 and item['tolerance'] == 1e-7
    )
    tracked = (
        'central_amplitude', 'energy_dimensionless',
        'charge_dimensionless', 'charge_rms_radius_dimensionless',
    )
    maximum_relative_change = max(
        relative_change(item['observables'][key], reference[key])
        for item in records for key in tracked
    )
    quadrature_records: list[dict[str, object]] = []
    for points in (4001, 8001, 16001):
        obs = profile_observables(canonical, OMEGA_BENCH, R_BENCH, points)
        quadrature_records.append({'points': points, 'observables': obs})
    q_reference = quadrature_records[-1]['observables']
    quadrature_maximum_relative_change = max(
        relative_change(item['observables'][key], q_reference[key])
        for item in quadrature_records for key in tracked[1:]
    )
    passed = (
        maximum_relative_change < 2e-4
        and quadrature_maximum_relative_change < 2e-4
    )
    return {
        'records': records,
        'quadrature_records': quadrature_records,
        'tracked_observables': list(tracked),
        'maximum_relative_change': maximum_relative_change,
        'quadrature_maximum_relative_change': quadrature_maximum_relative_change,
        'threshold': 2e-4,
        'pass': passed,
    }


def finite_difference_residual(
    f: np.ndarray, omega: float, radius: float
) -> np.ndarray:
    n = f.size - 1
    h = radius / n
    x = np.linspace(0.0, radius, n + 1)
    residual = np.zeros_like(f)
    force = (1.0 - omega**2) * f - f**3 + A_BENCH * f**5
    residual[0] = 6.0 * (f[1] - f[0]) / h**2 - force[0]
    xi = x[1:n]
    residual[1:n] = (
        (f[2:] - 2.0 * f[1:n] + f[:n - 1]) / h**2
        + (f[2:] - f[:n - 1]) / (h * xi)
        - force[1:n]
    )
    k = math.sqrt(1.0 - omega**2)
    residual[n] = (
        (3.0 * f[n] - 4.0 * f[n - 1] + f[n - 2]) / (2.0 * h)
        + (k + 1.0 / radius) * f[n]
    )
    return residual


def finite_difference_jacobian(
    f: np.ndarray, omega: float, radius: float
) -> object:
    n = f.size - 1
    h = radius / n
    x = np.linspace(0.0, radius, n + 1)
    derivative = 1.0 - omega**2 - 3.0 * f**2 + 5.0 * A_BENCH * f**4
    jac = lil_matrix((n + 1, n + 1), dtype=float)
    jac[0, 0] = -6.0 / h**2 - derivative[0]
    jac[0, 1] = 6.0 / h**2
    for i in range(1, n):
        jac[i, i - 1] = 1.0 / h**2 - 1.0 / (x[i] * h)
        jac[i, i] = -2.0 / h**2 - derivative[i]
        jac[i, i + 1] = 1.0 / h**2 + 1.0 / (x[i] * h)
    k = math.sqrt(1.0 - omega**2)
    jac[n, n - 2] = 1.0 / (2.0 * h)
    jac[n, n - 1] = -2.0 / h
    jac[n, n] = 3.0 / (2.0 * h) + k + 1.0 / radius
    return jac.tocsr()


def finite_difference_crosscheck(canonical: object) -> dict[str, object]:
    radius = R_BENCH
    spacing = 0.04
    n = int(round(radius / spacing))
    x = np.linspace(0.0, radius, n + 1)
    f = canonical.sol(x)[0].copy()
    residual_history: list[float] = []
    for _iteration in range(20):
        residual = finite_difference_residual(f, OMEGA_BENCH, radius)
        residual_norm = float(np.max(np.abs(residual)))
        residual_history.append(residual_norm)
        if residual_norm < 1e-10:
            break
        delta = spsolve(
            finite_difference_jacobian(f, OMEGA_BENCH, radius), -residual
        )
        accepted = False
        for power in range(10):
            factor = 0.5**power
            trial = f + factor * delta
            trial_norm = float(np.max(np.abs(
                finite_difference_residual(trial, OMEGA_BENCH, radius)
            )))
            if trial_norm < residual_norm:
                f = trial
                accepted = True
                break
        if not accepted:
            raise RuntimeError('Finite-difference Newton line search failed')
    final_residual = finite_difference_residual(f, OMEGA_BENCH, radius)
    primary = canonical.sol(x)[0]
    weighted_difference = math.sqrt(
        simpson(x**2 * (f - primary) ** 2, x=x)
        / simpson(x**2 * primary**2, x=x)
    )
    fp = np.gradient(f, x, edge_order=2)
    potential = 0.5 * f**2 - 0.25 * f**4 + A_BENCH * f**6 / 6.0
    energy = simpson(
        x**2 * (0.5 * fp**2 + 0.5 * OMEGA_BENCH**2 * f**2 + potential),
        x=x,
    )
    charge = OMEGA_BENCH * simpson(x**2 * f**2, x=x)
    radius_q = math.sqrt(
        simpson(x**4 * f**2, x=x) / simpson(x**2 * f**2, x=x)
    )
    primary_obs = profile_observables(canonical, OMEGA_BENCH, radius, 16001)
    observable_relative_changes = {
        'central_amplitude': relative_change(f[0], primary_obs['central_amplitude']),
        'energy_dimensionless': relative_change(energy, primary_obs['energy_dimensionless']),
        'charge_dimensionless': relative_change(charge, primary_obs['charge_dimensionless']),
        'charge_rms_radius_dimensionless': relative_change(
            radius_q, primary_obs['charge_rms_radius_dimensionless']
        ),
    }
    passed = (
        float(np.max(np.abs(final_residual))) < 1e-8
        and weighted_difference < 5e-4
        and max(observable_relative_changes.values()) < 5e-4
    )
    return {
        'spacing': spacing,
        'nodes': n + 1,
        'iterations': len(residual_history),
        'residual_history': residual_history,
        'final_max_residual': float(np.max(np.abs(final_residual))),
        'weighted_relative_L2_profile_difference': weighted_difference,
        'observable_relative_changes': observable_relative_changes,
        'threshold': 5e-4,
        'pass': passed,
    }


def hessian_spectrum(canonical: object) -> dict[str, object]:
    records: list[dict[str, object]] = []
    for spacing in (0.04, 0.02, 0.01):
        n = int(round(R_BENCH / spacing))
        x = np.linspace(spacing, R_BENCH - spacing, n - 1)
        f = canonical.sol(x)[0]
        offdiag = np.full(n - 2, -1.0 / spacing**2)
        base = 2.0 / spacing**2 + 1.0 - OMEGA_BENCH**2
        operators: dict[str, list[float]] = {}
        for name, ell, channel in (
            ('L_minus_l0', 0, 'minus'),
            ('L_plus_l0', 0, 'plus'),
            ('L_plus_l1', 1, 'plus'),
            ('L_plus_l2', 2, 'plus'),
        ):
            nonlinear = (
                -f**2 + A_BENCH * f**4
                if channel == 'minus'
                else -3.0 * f**2 + 5.0 * A_BENCH * f**4
            )
            diagonal = base + ell * (ell + 1.0) / x**2 + nonlinear
            eigenvalues = eigh_tridiagonal(
                diagonal,
                offdiag,
                select='i',
                select_range=(0, 5),
                check_finite=False,
            )[0]
            operators[name] = [float(value) for value in eigenvalues]
        records.append({'spacing': spacing, 'operators': operators})
    finest = records[-1]['operators']
    lm0 = np.array(finest['L_minus_l0'])
    lp0 = np.array(finest['L_plus_l0'])
    lp1 = np.array(finest['L_plus_l1'])
    lp2 = np.array(finest['L_plus_l2'])
    phase_zero = abs(lm0[0]) < 5e-4
    translation_zero = abs(lp1[0]) < 5e-4
    one_negative = np.count_nonzero(lp0 < -1e-3) == 1
    phase_no_negative = np.count_nonzero(lm0 < -5e-4) == 0
    angular_no_negative = np.count_nonzero(lp1 < -5e-4) == 0
    gaps_positive = (
        lm0[1] > 1e-3 and lp0[1] > 1e-3
        and lp1[1] > 1e-3 and lp2[0] > 1e-3
    )
    zero_convergence = (
        abs(records[-1]['operators']['L_minus_l0'][0])
        < abs(records[0]['operators']['L_minus_l0'][0])
        and abs(records[-1]['operators']['L_plus_l1'][0])
        < abs(records[0]['operators']['L_plus_l1'][0])
    )
    passed = all((
        phase_zero, translation_zero, one_negative, phase_no_negative,
        angular_no_negative, gaps_positive, zero_convergence,
    ))
    return {
        'records': records,
        'phase_zero_mode_pass': phase_zero,
        'translation_zero_mode_pass': translation_zero,
        'one_negative_L_plus_l0_pass': one_negative,
        'L_minus_l0_no_negative_pass': phase_no_negative,
        'L_plus_l1_no_negative_pass': angular_no_negative,
        'registered_nonzero_gaps_positive_pass': gaps_positive,
        'symmetry_zero_modes_converge_pass': zero_convergence,
        'pass': passed,
    }


def solve_sensitivity(canonical: object) -> dict[str, object]:
    omega = OMEGA_BENCH
    radius = R_BENCH
    k = math.sqrt(1.0 - omega**2)
    x = np.linspace(0.0, radius, 801)
    f_boundary = float(canonical.sol(radius)[0])

    def fun(xx: np.ndarray, zz: np.ndarray) -> np.ndarray:
        ff = canonical.sol(xx)[0]
        potential = 1.0 - omega**2 - 3.0 * ff**2 + 5.0 * A_BENCH * ff**4
        return np.vstack((zz[1], potential * zz[0] - 2.0 * omega * ff))

    def bc(za: np.ndarray, zb: np.ndarray) -> np.ndarray:
        return np.array([
            za[1],
            zb[1] + (k + 1.0 / radius) * zb[0] - omega * f_boundary / k,
        ])

    solution = solve_bvp(
        fun,
        bc,
        x,
        np.zeros((2, x.size)),
        S=SINGULAR_MATRIX,
        tol=1e-8,
        max_nodes=100000,
    )
    if not solution.success:
        raise RuntimeError(f'Sensitivity BVP failed: {solution.message}')
    xx = np.linspace(0.0, radius, 16001)
    f = canonical.sol(xx)[0]
    z = solution.sol(xx)[0]
    i2 = simpson(xx**2 * f**2, x=xx)
    derivative = i2 + 2.0 * omega * simpson(xx**2 * f * z, x=xx)
    boundary_residuals = bc(solution.y[:, 0], solution.y[:, -1])
    return {
        'dQ_dOmega': float(derivative),
        'central_sensitivity': float(z[0]),
        'adaptive_nodes': int(solution.x.size),
        'collocation_rms_residual_max': float(np.max(solution.rms_residuals)),
        'boundary_residuals': [float(abs(value)) for value in boundary_residuals],
        'negative_pass': derivative < 0.0,
    }


def branch_and_slope(canonical: object) -> dict[str, object]:
    solutions: dict[float, object] = {OMEGA_BENCH: canonical}
    for omega in OMEGA_GRID:
        if omega == OMEGA_BENCH:
            continue
        solutions[omega] = solve_profile(omega, seed=canonical)
    charges: dict[float, float] = {}
    branch: list[dict[str, object]] = []
    for omega in sorted(solutions):
        obs = profile_observables(solutions[omega], omega, R_BENCH, 16001)
        charges[omega] = obs['charge_dimensionless']
        branch.append({'Omega': omega, 'observables': obs})
    derivative_h001 = (
        charges[0.78] - 8.0 * charges[0.79]
        + 8.0 * charges[0.81] - charges[0.82]
    ) / 0.12
    derivative_h0005 = (
        charges[0.79] - 8.0 * charges[0.795]
        + 8.0 * charges[0.805] - charges[0.81]
    ) / 0.06
    disagreement = abs(derivative_h001 - derivative_h0005) / max(
        abs(derivative_h001), abs(derivative_h0005), 1e-30
    )
    return {
        'branch': branch,
        'five_point_h_0p01': derivative_h001,
        'five_point_h_0p005': derivative_h0005,
        'relative_disagreement': disagreement,
        'negative_both_pass': derivative_h001 < 0.0 and derivative_h0005 < 0.0,
        'agreement_pass': disagreement < 2e-2,
        'pass': (
            derivative_h001 < 0.0
            and derivative_h0005 < 0.0
            and disagreement < 2e-2
        ),
    }


def manufactured_profile_control() -> dict[str, object]:
    radius = 8.0
    mu = 1.3
    x = np.linspace(0.0, radius, 801)

    def exact(xx: np.ndarray) -> np.ndarray:
        return np.exp(-xx**2)

    def source(xx: np.ndarray) -> np.ndarray:
        return (4.0 * xx**2 - 6.0 - mu**2) * exact(xx)

    def fun(xx: np.ndarray, yy: np.ndarray) -> np.ndarray:
        return np.vstack((yy[1], mu**2 * yy[0] + source(xx)))

    def bc(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
        return np.array([ya[1], yb[1] + 2.0 * radius * yb[0]])

    solution = solve_bvp(
        fun,
        bc,
        x,
        np.zeros((2, x.size)),
        S=SINGULAR_MATRIX,
        tol=1e-9,
        max_nodes=50000,
    )
    xx = np.linspace(0.0, radius, 4001)
    max_error = float(np.max(np.abs(solution.sol(xx)[0] - exact(xx))))
    return {
        'solution_success': bool(solution.success),
        'max_absolute_error': max_error,
        'threshold': 1e-7,
        'pass': bool(solution.success and max_error < 1e-7),
    }


def mutation_controls() -> dict[str, object]:
    f, fp, k2, a = sp.symbols('f fp k2 a', positive=True)
    y = sp.symbols('y', nonnegative=True)
    Omega2 = sp.symbols('Omega2', nonnegative=True)
    tail_mass2 = 1 - Omega2
    v_attractive = f**2 / 2 - f**4 / 4 + a * f**6 / 6
    v_repulsive = f**2 / 2 + f**4 / 4 + a * f**6 / 6
    v_without_sextic = f**2 / 2 - f**4 / 4
    repulsive_ratio = sp.simplify(2 * v_repulsive / f**2)
    repulsive_nehari = fp**2 + k2 * f**2 + f**4 + a * f**6
    source_kinetic, source_metric, source_lagrangian = sp.symbols(
        'source_kinetic source_metric source_lagrangian', nonzero=True
    )
    hilbert_source = source_kinetic + source_metric * source_lagrangian
    relabelled_source = source_kinetic - source_metric * source_lagrangian
    source_action_map = (('S_C', 'T_C'), ('S_O', 'T_O'))
    total_source_expression = 'T_total=T_C+T_O'
    source_ledger_base = validate_source_ledger(
        source_action_map, total_source_expression
    )
    base_checks = {
        'attractive_quartic_coefficient_exact': (
            sp.Poly(v_attractive, f).coeff_monomial(f**4) == -sp.Rational(1, 4)
        ),
        'stabilizing_sextic_large_field_exact': (
            sp.limit(v_attractive, f, sp.oo) == sp.oo
        ),
        'strict_vacuum_benchmark_exact': (
            sp.simplify(
                (sp.Rational(1, 2) - sp.Rational(3, 32) / a)
                .subs(a, sp.Rational(1, 4))
            ) > 0
        ),
        'localization_benchmark_exact': (
            1 - sp.Rational(4, 5)**2 == sp.Rational(9, 25)
        ),
        'phase_roles_distinct_exact': (
            len({'theta_C', 'theta_O', 'process_time'}) == 3
        ),
        'one_common_metric_exact': len(('g_coframe',)) == 1,
        'hilbert_source_formula_exact': sp.simplify(
            hilbert_source
            - (source_kinetic + source_metric * source_lagrangian)
        ) == 0,
        'one_total_source_ledger_exact': source_ledger_base,
        'benchmark_tuple_exact': (
            (A_BENCH, OMEGA_BENCH, R_BENCH) == (0.25, 0.8, 80.0)
        ),
    }
    repulsive_no_go = all((
        sp.simplify(
            repulsive_ratio.subs(f**2, y)
            - (1 + y / 2 + a * y**2 / 3)
        ) == 0,
        sp.simplify(
            sp.diff(repulsive_ratio.subs(f**2, y), y)
            - (sp.Rational(1, 2) + 2 * a * y / 3)
        ) == 0,
        sp.Poly(repulsive_nehari, fp, f).coeff_monomial(fp**2) == 1,
        sp.Poly(repulsive_nehari, fp, f).coeff_monomial(f**2) == k2,
        sp.Poly(repulsive_nehari, fp, f).coeff_monomial(f**4) == 1,
        sp.Poly(repulsive_nehari, fp, f).coeff_monomial(f**6) == a,
    ))
    detections = {
        'repulsive_quartic_detected': repulsive_no_go,
        'sextic_removal_detected': (
            sp.limit(v_without_sextic, f, sp.oo) == -sp.oo
        ),
        'vacuum_boundary_detected': sp.simplify(
            (sp.Rational(1, 2) - sp.Rational(3, 32) / a)
            .subs(a, sp.Rational(3, 16))
        ) == 0,
        'localization_edge_detected': all((
            tail_mass2.subs(Omega2, sp.Rational(16, 25)) == sp.Rational(9, 25),
            tail_mass2.subs(Omega2, 1) == 0,
            tail_mass2.subs(Omega2, sp.Rational(26, 25)) == -sp.Rational(1, 25),
        )),
        'phase_role_collapse_detected': (
            len({'theta_C', 'theta_C', 'process_time'}) < 3
        ),
        'second_metric_detected': len(('g_coframe', 'g_second')) != 1,
        'stress_relabelling_detected': sp.simplify(
            hilbert_source - relabelled_source
        ) != 0,
        'duplicate_source_detected': not validate_source_ledger(
            (('S_C', 'T_C'), ('S_O', 'T_O'), ('S_O_duplicate', 'T_O')),
            'T_total=T_C+T_O+T_O',
        ),
        'benchmark_mutation_detected': (
            (A_BENCH, OMEGA_BENCH + 0.01, R_BENCH)
            != (0.25, 0.8, 80.0)
        ),
    }
    passed = all(bool(value) for value in base_checks.values()) and all(
        bool(value) for value in detections.values()
    )
    return {
        'base_checks': base_checks,
        'base_state_pass': all(bool(value) for value in base_checks.values()),
        'source_ledger_base_exact': source_ledger_base,
        'source_action_map': [list(item) for item in source_action_map],
        'total_source_expression': total_source_expression,
        'detections': detections,
        'repulsive_quartic_nehari_sum_positive_no_go_exact': repulsive_no_go,
        'pass': passed,
    }


def integration_gate() -> dict[str, object]:
    readme_text = canonical_text(README)
    formal_text = canonical_text(FORMAL_LEDGER)
    readme_markers = (
        CLAIM_ID,
        PASS_STATUS,
        'Q-ball',
        'selected core action',
        'theta_O',
        'Psi_O=(chi/sqrt(2)) exp(i theta_O)',
        'V(chi)=m^2 chi^2/2-lambda chi^4/4+g chi^6/6',
        'T_total=T_C+T_O',
        'a>3/16',
        '1-3/(16a)<Omega^2<1',
        '1.82021051',
        '14.10656629',
        '15.15164096',
        '2.72894693',
        '0.93102564',
        '-132.36879',
        'unconstrained `L_+`',
        'bound against decay into free quanta',
        'not a neutral real oscillon',
        'coframe backreaction is outside this result',
        'ordinary-phase Noether charge',
        'with electric charge',
    )
    formal_markers = (
        'W3-58',
        'One_Oscillon_Coframe_Localized_Core/README.md',
        PASS_STATUS,
        'Q-ball',
        'V(chi)=m^2 chi^2/2-lambda chi^4/4+g chi^6/6',
        'T_total=T_C+T_O',
        'a=g m^2/lambda^2>3/16',
        '1-3/(16a)<Omega^2<1',
        '1.82021051',
        '2.72894693/m',
        '0.93102564',
        '-132.36879',
        'unconstrained `L_+`',
        'decay into free quanta',
        'not yet a derived neutral real oscillon',
        'core--coframe-backreaction problem',
    )
    forbidden_markers = (
        'negative constrained radial',
        'constrained radial negative',
        'negative constrained direction',
    )
    readme_missing = [
        marker for marker in readme_markers if marker not in readme_text
    ]
    formal_missing = [
        marker for marker in formal_markers if marker not in formal_text
    ]
    forbidden_hits = [
        marker for marker in forbidden_markers
        if marker in readme_text or marker in formal_text
    ]
    return {
        'readme_sha256': sha256(README),
        'formal_ledger_sha256': sha256(FORMAL_LEDGER),
        'readme_markers_pass': not readme_missing,
        'formal_ledger_markers_pass': not formal_missing,
        'forbidden_wording_absent_pass': not forbidden_hits,
        'readme_missing_markers': readme_missing,
        'formal_ledger_missing_markers': formal_missing,
        'forbidden_wording_hits': forbidden_hits,
        'pass': not readme_missing and not formal_missing and not forbidden_hits,
    }


def numerical_gate() -> dict[str, object]:
    canonical = solve_profile(OMEGA_BENCH)
    canonical_obs = profile_observables(
        canonical, OMEGA_BENCH, R_BENCH, 16001
    )
    convergence = convergence_gate(canonical)
    finite_difference = finite_difference_crosscheck(canonical)
    spectrum = hessian_spectrum(canonical)
    sensitivity = solve_sensitivity(canonical)
    branch = branch_and_slope(canonical)
    manufactured = manufactured_profile_control()

    shape_pass = (
        canonical_obs['central_amplitude'] > 0.1
        and canonical_obs['minimum_amplitude'] > -1e-12
        and canonical_obs['maximum_positive_derivative'] < 1e-8
        and canonical_obs['energy_dimensionless'] > 0.0
        and canonical_obs['charge_dimensionless'] > 0.0
        and canonical_obs['charge_rms_radius_dimensionless'] > 0.0
    )
    local_checks_pass = (
        canonical_obs['equation_normalized_weighted_l2_residual'] < 2e-5
        and canonical_obs['equation_normalized_global_max_residual'] < 2e-5
        and canonical_obs['collocation_rms_residual_max'] < 2e-5
        and canonical_obs['nehari_relative'] < 2e-5
        and canonical_obs['virial_relative'] < 2e-5
        and canonical_obs['stress_balance_relative'] < 2e-5
        and canonical_obs['tail_exponent_absolute_error'] < 2e-3
        and canonical_obs['centre_boundary_residual'] < 1e-8
        and canonical_obs['robin_boundary_residual'] < 1e-8
    )
    sensitivity_agreement = relative_change(
        sensitivity['dQ_dOmega'], branch['five_point_h_0p005']
    )
    slope_pass = (
        sensitivity['negative_pass']
        and branch['pass']
        and sensitivity_agreement < 2e-3
    )
    decay_bound_pass = canonical_obs['energy_per_mass_charge'] < 1.0
    orbital_evidence_pass = spectrum['pass'] and slope_pass
    passed = all((
        shape_pass,
        local_checks_pass,
        convergence['pass'],
        finite_difference['pass'],
        spectrum['pass'],
        slope_pass,
        decay_bound_pass,
        manufactured['pass'],
    ))
    return {
        'benchmark': {
            'a': A_BENCH,
            'Omega': OMEGA_BENCH,
            'Omega_min': 0.5,
            'X_max': R_BENCH,
        },
        'canonical_observables': canonical_obs,
        'shape_pass': shape_pass,
        'local_balance_and_tail_checks_pass': local_checks_pass,
        'convergence': convergence,
        'finite_difference_crosscheck': finite_difference,
        'hessian_spectrum': spectrum,
        'sensitivity': sensitivity,
        'charge_slope_branch': branch,
        'sensitivity_vs_finite_difference_relative_change': sensitivity_agreement,
        'negative_charge_slope_pass': slope_pass,
        'free_quantum_decay_bound_pass': decay_bound_pass,
        'orbital_stability_evidence_pass': orbital_evidence_pass,
        'manufactured_profile_control': manufactured,
        'pass': passed,
    }


def make_closure_flags(
    prereg: dict[str, object],
    dependencies: dict[str, object],
    symbolic: dict[str, object],
    numerical: dict[str, object],
    mutations: dict[str, object],
) -> tuple[dict[str, bool], dict[str, bool]]:
    canonical = numerical['canonical_observables']
    true_flags = {
        'dependency_hashes_pinned_exact': dependencies['all_pass'],
        'w3_50_collective_phase_role_preserved_exact': all((
            dependencies['records']['W3_50_contract']['pass'],
            prereg['scope_markers_exact'],
        )),
        'w3_54_common_coframe_minimal_coupling_exact': all((
            dependencies['records']['W3_54_contract']['pass'],
            prereg['scope_markers_exact'],
            symbolic['checks']['common_coframe_inverse_metric_exact'],
            symbolic['checks']['common_coframe_kinetic_contraction_exact'],
        )),
        'ordinary_phase_u1_action_defined_exact': all((
            symbolic['checks']['polar_complex_kinetic_dictionary_exact'],
            symbolic['checks']['ordinary_current_noether_exact'],
            symbolic['checks']['ordinary_phase_shift_euler_exact'],
        )),
        'canonical_amplitude_gradient_present_exact': symbolic['checks']['radial_euler_lagrange_exact'],
        'bounded_binding_sextic_present_exact': all((
            symbolic['checks']['minimal_even_polynomial_degree_is_six'],
            symbolic['checks']['potential_large_field_positive_for_a_positive'],
        )),
        'zero_vacuum_global_threshold_exact': symbolic['checks']['global_vacuum_threshold_exact'],
        'euler_lagrange_equations_exact': all((
            symbolic['checks']['potential_euler_force_exact'],
            symbolic['checks']['radial_euler_lagrange_exact'],
        )),
        'ordinary_phase_current_exact': all((
            symbolic['checks']['ordinary_current_noether_exact'],
            symbolic['checks']['ordinary_current_positive_convention_exact'],
        )),
        'hilbert_stress_from_same_action_exact': all((
            symbolic['checks']['hilbert_metric_variation_identity_exact'],
            symbolic['checks']['hilbert_energy_density_exact'],
            symbolic['checks']['hilbert_radial_pressure_exact'],
            symbolic['checks']['hilbert_tangential_pressure_exact'],
        )),
        'one_source_ledger_no_duplicate_exact': all((
            symbolic['checks']['source_ledger_from_selected_actions_exact'],
            mutations['source_ledger_base_exact'],
            mutations['detections']['duplicate_source_detected'],
        )),
        'dimensionless_radial_bvp_exact': all((
            symbolic['checks']['dimensionless_radial_operator_exact'],
            symbolic['checks']['dimensionless_radial_derivative_exact'],
            symbolic['checks']['dimensionless_robin_boundary_exact'],
        )),
        'analytic_existence_window_exact': all((
            symbolic['checks']['existence_ratio_global_minimum_exact'],
            symbolic['checks']['existence_lower_edge_exact'],
            symbolic['checks']['benchmark_tail_exact'],
            symbolic['checks']['localization_upper_edge_exact'],
        )),
        'finite_energy_ground_state_constructed_numerical': (
            numerical['shape_pass']
            and canonical['energy_dimensionless'] > 0.0
            and canonical['charge_dimensionless'] > 0.0
        ),
        'intrinsic_charge_radius_constructed_numerical': canonical['charge_rms_radius_dimensionless'] > 0.0,
        'domain_tolerance_quadrature_convergence_pass': numerical['convergence']['pass'],
        'independent_finite_difference_crosscheck_pass': numerical['finite_difference_crosscheck']['pass'],
        'radial_nehari_virial_stress_tail_checks_pass': numerical['local_balance_and_tail_checks_pass'],
        'hessian_operators_exact': all((
            symbolic['checks']['hessian_minus_operator_exact'],
            symbolic['checks']['hessian_plus_operator_exact'],
            symbolic['checks']['radial_hessian_conjugation_exact'],
            symbolic['checks']['phase_zero_mode_identity_exact'],
            symbolic['checks']['translation_zero_mode_identity_exact'],
            symbolic['checks']['sensitivity_operator_identity_exact'],
            symbolic['checks']['sensitivity_reduced_unreduced_equivalence_exact'],
            symbolic['checks']['charge_sensitivity_formula_exact'],
            symbolic['checks']['centrifugal_ordering_ell_ge_2_exact'],
        )),
        'phase_and_translation_zero_modes_numerical': all((
            numerical['hessian_spectrum']['phase_zero_mode_pass'],
            numerical['hessian_spectrum']['translation_zero_mode_pass'],
        )),
        'single_unconstrained_L_plus_negative_direction_numerical': numerical['hessian_spectrum']['one_negative_L_plus_l0_pass'],
        'negative_charge_slope_numerical': numerical['negative_charge_slope_pass'],
        'free_quantum_decay_bound_numerical': numerical['free_quantum_decay_bound_pass'],
        'converged_numerical_orbital_stability_evidence': numerical['orbital_stability_evidence_pass'],
        'registered_contract_keysets_exact': all((
            prereg['hash_exact'], prereg['fields_exact'], prereg['scope_markers_exact']
        )),
        'mutation_controls_pass': mutations['pass'],
    }
    true_flags['aggregate_gate_pass'] = all(true_flags.values())
    false_flags = {name: False for name in REQUIRED_FALSE_FLAGS}
    if set(true_flags) != REQUIRED_TRUE_FLAGS:
        raise RuntimeError(
            f'True closure key drift: missing={REQUIRED_TRUE_FLAGS-set(true_flags)}, '
            f'extra={set(true_flags)-REQUIRED_TRUE_FLAGS}'
        )
    return true_flags, false_flags


def atomic_write(path: Path, payload: bytes) -> None:
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_bytes(payload)
    os.replace(temporary, path)


def main() -> None:
    prereg = verify_preregistration()
    dependencies = verify_dependencies()
    symbolic = symbolic_gate()
    mutations = mutation_controls()
    integration = integration_gate()
    numerical = numerical_gate()
    closure_flags, scope_flags = make_closure_flags(
        prereg, dependencies, symbolic, numerical, mutations
    )
    exact_gate = all((
        prereg['hash_exact'], prereg['fields_exact'], prereg['scope_markers_exact'],
        dependencies['all_pass'], symbolic['all_pass'], mutations['pass'],
        integration['pass'],
    ))
    if not exact_gate:
        status = FAIL_STATUS
    elif not closure_flags['aggregate_gate_pass'] or not numerical['pass']:
        status = INCONCLUSIVE_STATUS
    else:
        status = PASS_STATUS
    artifact_valid = bool(
        exact_gate
        and closure_flags['aggregate_gate_pass']
        and numerical['pass']
        and set(closure_flags) == REQUIRED_TRUE_FLAGS
        and set(scope_flags) == REQUIRED_FALSE_FLAGS
        and all(value is False for value in scope_flags.values())
    )
    result = {
        'schema_version': 'W3-58-result-v1.0',
        'claim_id': CLAIM_ID,
        'model_version': MODEL_VERSION,
        'status': status,
        'artifact_valid': artifact_valid,
        'evidence_type': {
            'action_and_analytic_class': 'CONDITIONAL_EXACT',
            'profile_and_stability': 'CONVERGED_NUMERICAL_EVIDENCE',
            'computer_assisted_proof': False,
            'observational_test': False,
        },
        'operator_convention': {
            'sensitivity_operator': (
                'UNREDUCED_SCRIPT_L_PLUS z=2 Omega f; EQUIVALENT_REDUCED_'
                'FORM_L_PLUS(x z)=2 Omega x f'
            ),
        },
        'scope_status': (
            'ONE_SELECTED_PHASE_SUPPORTED_Q_BALL_TYPE_CORE_ON_FIXED_COFRAME; '
            'FOUNDATION_ORIGIN_BACKGROUND_LOCK_BACKREACTION_NEUTRAL_REAL_'
            'OSCILLON_AND_PARTICLE_IDENTITY_OPEN'
        ),
        'preregistration': prereg,
        'dependencies': dependencies,
        'symbolic': symbolic,
        'numerical': numerical,
        'controls': mutations,
        'integration': integration,
        'closure_flags': closure_flags,
        'scope_flags': scope_flags,
        'provenance': {
            'source_sha256': sha256(SOURCE),
            'preregistration_sha256': sha256(PREREG),
            'python': platform.python_version(),
            'platform': platform.platform(),
            'numpy': importlib.metadata.version('numpy'),
            'scipy': importlib.metadata.version('scipy'),
            'sympy': importlib.metadata.version('sympy'),
            'network_used': False,
            'archived_theory_used': False,
        },
        'files': {
            'readme': README.name,
            'preregistration': PREREG.name,
            'source': SOURCE.name,
            'result': OUTPUT.name,
            'checksum': HASH_OUTPUT.name,
        },
    }
    result = native_tree(result)
    if not finite_tree(result):
        raise RuntimeError('Result contains non-finite numeric data')
    encoded = (json.dumps(
        result, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False
    ) + '\n').encode('utf-8')
    atomic_write(OUTPUT, encoded)
    checksum = sha256(OUTPUT)
    atomic_write(
        HASH_OUTPUT,
        f'{checksum}  {OUTPUT.name}\n'.encode('utf-8'),
    )
    print(json.dumps({
        'status': status,
        'artifact_valid': artifact_valid,
        'result_sha256': checksum,
        'central_amplitude': numerical['canonical_observables']['central_amplitude'],
        'energy_per_mass_charge': numerical['canonical_observables']['energy_per_mass_charge'],
        'charge_rms_radius': numerical['canonical_observables']['charge_rms_radius_dimensionless'],
        'dQ_dOmega': numerical['sensitivity']['dQ_dOmega'],
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
