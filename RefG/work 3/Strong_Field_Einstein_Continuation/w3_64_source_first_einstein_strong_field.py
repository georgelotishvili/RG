from __future__ import annotations

import hashlib
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp


HERE = Path(__file__).resolve().parent
WORK3 = HERE.parent
PREREG = HERE / 'w3_64_source_first_einstein_strong_field_preregistration.md'
OUTPUT = HERE / 'w3_64_result.json'
W3_54 = (
    WORK3 / 'Lagrangian_Formulation' /
    'Relational_Coframe_TEGR_Phase_Source_Closure' /
    'w3_54_relational_coframe_tegr_phase_source_closure_contract.md'
)
W3_58_PREREG = (
    WORK3 / 'Lagrangian_Formulation' /
    'One_Oscillon_Coframe_Localized_Core' /
    'w3_58_one_oscillon_coframe_localized_core_preregistration.md'
)
W3_58_RESULT = W3_58_PREREG.with_name('w3_58_result.json')

EXPECTED_HASHES = {
    'w3_54_contract': '6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879',
    'w3_58_preregistration': 'ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db',
    'w3_58_result': 'cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5',
}

A_BENCH = 0.25
F0_BENCH = 1.820210505787701
ALPHA_GRID = (0.0, 0.01, 0.02, 0.03, 0.04)
RADIUS_BENCH = 80.0
TOL_BENCH = 1.0e-7
INITIAL_NODES = 801
MAX_NODES = 100000
EPS = 1.0e-5
TAIL_FIT_MIN_SAMPLES = 50
MUTATION_RESIDUAL_NODES = 12001
MUTATION_RESIDUAL_CENTRE_CUT = 0.02
MUTATION_RESIDUAL_OUTER_CUT = 1.0
W3_58_TARGET = {
    'Omega': 0.8,
    'energy': 14.10656628973206,
    'charge': 15.151640960024233,
    'charge_rms_radius': 2.7289469321707824,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_change(value: float, reference: float) -> float:
    return abs(value - reference) / max(abs(value), abs(reference), 1.0e-30)


def finite_tree(value: Any) -> bool:
    if isinstance(value, dict):
        return all(finite_tree(k) and finite_tree(v) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return all(finite_tree(v) for v in value)
    if isinstance(value, (float, np.floating)):
        return math.isfinite(float(value))
    return True


def native_tree(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): native_tree(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [native_tree(v) for v in value]
    if isinstance(value, np.ndarray):
        return [native_tree(v) for v in value.tolist()]
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def dependency_gate() -> dict[str, Any]:
    paths = {
        'w3_54_contract': W3_54,
        'w3_58_preregistration': W3_58_PREREG,
        'w3_58_result': W3_58_RESULT,
    }
    records: dict[str, Any] = {}
    for name, path in paths.items():
        actual = sha256(path)
        records[name] = {
            'path': str(path.relative_to(WORK3)),
            'expected_sha256': EXPECTED_HASHES[name],
            'actual_sha256': actual,
            'hash_exact': actual == EXPECTED_HASHES[name],
        }
    upstream = json.loads(W3_58_RESULT.read_text(encoding='utf-8'))
    upstream_pass = bool(
        upstream.get('artifact_valid')
        and upstream.get('closure_flags', {}).get('aggregate_gate_pass')
        and not upstream.get('scope_flags', {}).get(
            'localized_gravitational_backreaction_derived'
        )
    )
    source_ledger_pass = bool(
        upstream.get('controls', {}).get('source_ledger_base_exact')
        and upstream.get('controls', {}).get('total_source_expression')
        == 'T_total=T_C+T_O'
        and upstream.get('controls', {}).get('source_action_map')
        == [['S_C', 'T_C'], ['S_O', 'T_O']]
    )
    upstream_action_variation_pass = bool(
        upstream.get('closure_flags', {}).get('euler_lagrange_equations_exact')
        and upstream.get('closure_flags', {}).get('hilbert_stress_from_same_action_exact')
        and upstream.get('closure_flags', {}).get('ordinary_phase_u1_action_defined_exact')
        and upstream.get('closure_flags', {}).get('w3_54_common_coframe_minimal_coupling_exact')
    )
    prereg_text = PREREG.read_text(encoding='utf-8')
    required_markers = (
        '**CLAIM_ID:** `W3_64_SOURCE_FIRST_EINSTEIN_STRONG_FIELD_GATE`',
        'Exactly three files belong to the package:',
        'second metric or vacuum slot',
        'No profile, switching function, curvature threshold, equation of state',
        'The Penrose implication is restricted',
        'Continuation proceeds in increasing `alpha`',
        'W3-58',
        'This closes the first source-first strong-field gate and stops.',
    )
    marker_records = {
        marker: marker in prereg_text for marker in required_markers
    }
    all_pass = bool(
        all(item['hash_exact'] for item in records.values())
        and upstream_pass
        and source_ledger_pass
        and upstream_action_variation_pass
        and all(marker_records.values())
    )
    return {
        'records': records,
        'upstream_w3_58_pass': upstream_pass,
        'upstream_source_ledger_exact': source_ledger_pass,
        'upstream_action_and_hilbert_variation_exact': upstream_action_variation_pass,
        'preregistration_markers': marker_records,
        'all_pass': all_pass,
    }


def spherical_einstein_tensor_gate() -> dict[str, Any]:
    t, x, theta, phi = sp.symbols('t x theta phi', real=True)
    coords = (t, x, theta, phi)
    n_fun = sp.Function('N')(x)
    sigma_fun = sp.Function('sigma')(x)
    metric = sp.diag(
        -sigma_fun**2 * n_fun,
        1 / n_fun,
        x**2,
        x**2 * sp.sin(theta)**2,
    )
    inverse = sp.simplify(metric.inv())
    dimension = 4
    gamma = [
        [[sp.S.Zero for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for upper in range(dimension):
        for left in range(dimension):
            for right in range(dimension):
                gamma[upper][left][right] = sp.simplify(sum(
                    inverse[upper, lower] * (
                        sp.diff(metric[lower, right], coords[left])
                        + sp.diff(metric[lower, left], coords[right])
                        - sp.diff(metric[left, right], coords[lower])
                    ) / 2
                    for lower in range(dimension)
                ))
    ricci = sp.MutableDenseMatrix.zeros(dimension, dimension)
    for left in range(dimension):
        for right in range(dimension):
            expression = sp.S.Zero
            for index in range(dimension):
                expression += sp.diff(
                    gamma[index][left][right], coords[index]
                )
                expression -= sp.diff(
                    gamma[index][left][index], coords[right]
                )
                for contracted in range(dimension):
                    expression += (
                        gamma[index][index][contracted]
                        * gamma[contracted][left][right]
                        - gamma[index][right][contracted]
                        * gamma[contracted][left][index]
                    )
            ricci[left, right] = sp.simplify(expression)
    ricci_scalar = sp.simplify(sum(
        inverse[left, right] * ricci[left, right]
        for left in range(dimension) for right in range(dimension)
    ))
    einstein_covariant = sp.simplify(
        ricci - metric * ricci_scalar / 2
    )
    einstein_mixed = sp.simplify(inverse * einstein_covariant)
    g_t_t = sp.simplify(einstein_mixed[0, 0])
    g_r_r = sp.simplify(einstein_mixed[1, 1])
    expected_t_t = (
        (n_fun - 1) / x**2 + sp.diff(n_fun, x) / x
    )
    expected_r_r = (
        expected_t_t
        + 2 * n_fun * sp.diff(sigma_fun, x) / (sigma_fun * x)
    )

    alpha = sp.symbols('alpha', positive=True, finite=True)
    mass_fun = sp.Function('M')(x)
    n_mass = 1 - 2 * alpha * mass_fun / x
    mass_reduction = sp.simplify(
        expected_t_t.subs({
            sp.diff(n_fun, x): sp.diff(n_mass, x),
            n_fun: n_mass,
        })
        + 2 * alpha * sp.diff(mass_fun, x) / x**2
    )
    newton_g, mass_scale, coupling = sp.symbols(
        'G m_s lambda', positive=True, finite=True
    )
    alpha_definition = 4 * sp.pi * newton_g * mass_scale**2 / coupling
    physical_mass = 4 * sp.pi * mass_scale * mass_fun / coupling
    physical_radius = x / mass_scale
    dimensional_compactness = sp.simplify(
        2 * newton_g * physical_mass / physical_radius
        - 2 * alpha_definition * mass_fun / x
    )
    checks = {
        'einstein_mixed_tt_exact': sp.simplify(g_t_t - expected_t_t) == 0,
        'einstein_mixed_rr_exact': sp.simplify(g_r_r - expected_r_r) == 0,
        'misner_sharp_mass_reduction_exact': mass_reduction == 0,
        'misner_sharp_physical_normalization_exact': dimensional_compactness == 0,
        'lapse_difference_reduction_exact': sp.simplify(
            (expected_r_r - expected_t_t)
            - 2 * n_fun * sp.diff(sigma_fun, x) / (sigma_fun * x)
        ) == 0,
    }
    return {
        'checks': checks,
        'all_pass': bool(all(checks.values())),
        'mixed_components': {
            'G_t_t': str(expected_t_t),
            'G_r_r': str(expected_r_r),
            'G_r_r_minus_G_t_t': str(
                sp.simplify(expected_r_r - expected_t_t)
            ),
        },
    }


def reduced_scalar_action_gate() -> dict[str, Any]:
    x = sp.symbols('x', positive=True, finite=True)
    omega, a = sp.symbols('Omega a', positive=True, finite=True)
    f = sp.Function('f')(x)
    n_fun = sp.Function('N')(x)
    sigma_fun = sp.Function('sigma')(x)
    potential_expr = f**2 / 2 - f**4 / 4 + a * f**6 / 6
    reduced_lagrangian = sigma_fun * x**2 * (
        n_fun * sp.diff(f, x)**2 / 2
        - omega**2 * f**2 / (2 * sigma_fun**2 * n_fun)
        + potential_expr
    )
    euler_lagrange = sp.simplify(
        sp.diff(
            sp.diff(reduced_lagrangian, sp.diff(f, x)), x
        ) - sp.diff(reduced_lagrangian, f)
    )
    target = sp.diff(
        sigma_fun * x**2 * n_fun * sp.diff(f, x), x
    ) + sigma_fun * x**2 * (
        omega**2 * f / (sigma_fun**2 * n_fun)
        - (f - f**3 + a * f**5)
    )
    check = sp.simplify(euler_lagrange - target) == 0
    normalized_equation = sp.expand(target / (sigma_fun * x**2))
    flat_equation = sp.simplify(normalized_equation.subs({
        n_fun: 1,
        sigma_fun: 1,
        sp.diff(n_fun, x): 0,
        sp.diff(sigma_fun, x): 0,
    }))
    expected_flat = (
        sp.diff(f, x, 2) + 2 * sp.diff(f, x) / x
        + omega**2 * f - f + f**3 - a * f**5
    )
    flat_check = sp.simplify(flat_equation - expected_flat) == 0
    return {
        'reduced_lagrangian': str(reduced_lagrangian),
        'euler_lagrange_matches_covariant_radial_equation_exact': check,
        'alpha_zero_flat_equation_exact': flat_check,
        'all_pass': bool(check and flat_check),
    }


def anisotropic_conservation_gate() -> dict[str, Any]:
    x = sp.symbols('x', positive=True, finite=True)
    omega, a = sp.symbols('Omega a', positive=True, finite=True)
    f = sp.Function('f')(x)
    n_fun = sp.Function('N')(x)
    sigma_fun = sp.Function('sigma')(x)
    fp = sp.diff(f, x)
    potential_expr = f**2 / 2 - f**4 / 4 + a * f**6 / 6
    force = f - f**3 + a * f**5
    phase = omega**2 * f**2 / (2 * sigma_fun**2 * n_fun)
    gradient = n_fun * fp**2 / 2
    rho = gradient + phase + potential_expr
    p_r = gradient + phase - potential_expr
    p_t = -gradient + phase - potential_expr
    fpp_on_shell = (
        (force - omega**2 * f / (sigma_fun**2 * n_fun)) / n_fun
        - (
            sp.diff(n_fun, x) / n_fun
            + sp.diff(sigma_fun, x) / sigma_fun
            + 2 / x
        ) * fp
    )
    phi_prime = (
        sp.diff(sigma_fun, x) / sigma_fun
        + sp.diff(n_fun, x) / (2 * n_fun)
    )
    tov_residual = (
        sp.diff(p_r, x)
        + (rho + p_r) * phi_prime
        - 2 * (p_t - p_r) / x
    )
    on_shell = sp.factor(sp.simplify(
        tov_residual.subs(sp.diff(f, x, 2), fpp_on_shell)
    ))
    return {
        'identity': (
            'p_r_prime+(rho+p_r)Phi_prime-2(p_t-p_r)/x=0, '
            'Phi_prime=sigma_prime/sigma+N_prime/(2N)'
        ),
        'on_shell_residual': str(on_shell),
        'anisotropic_tov_from_scalar_equation_exact': on_shell == 0,
        'all_pass': bool(on_shell == 0),
    }


def dimensionless_reduction_gate() -> dict[str, Any]:
    mass_scale, coupling, sextic = sp.symbols(
        'm_s lambda g_6', positive=True, finite=True
    )
    f, fp, omega_dim, n_metric, sigma = sp.symbols(
        'f f_prime Omega N sigma', positive=True, finite=True
    )
    chi = mass_scale * f / sp.sqrt(coupling)
    chi_r = mass_scale**2 * fp / sp.sqrt(coupling)
    omega_physical = mass_scale * omega_dim
    a_definition = sextic * mass_scale**2 / coupling**2
    scalar_scale = mass_scale**3 / sp.sqrt(coupling)
    density_scale = mass_scale**4 / coupling
    force_physical = (
        mass_scale**2 * chi
        - coupling * chi**3
        + sextic * chi**5
    )
    potential_physical = (
        mass_scale**2 * chi**2 / 2
        - coupling * chi**4 / 4
        + sextic * chi**6 / 6
    )
    gradient_physical = n_metric * chi_r**2 / 2
    phase_physical = omega_physical**2 * chi**2 / (
        2 * sigma**2 * n_metric
    )
    checks = {
        'field_rescaling_exact': sp.simplify(
            chi * sp.sqrt(coupling) / mass_scale - f
        ) == 0,
        'potential_force_reduction_exact': sp.simplify(
            force_physical / scalar_scale
            - (f - f**3 + a_definition * f**5)
        ) == 0,
        'potential_density_reduction_exact': sp.simplify(
            potential_physical / density_scale
            - (f**2 / 2 - f**4 / 4 + a_definition * f**6 / 6)
        ) == 0,
        'gradient_density_reduction_exact': sp.simplify(
            gradient_physical / density_scale - n_metric * fp**2 / 2
        ) == 0,
        'phase_density_reduction_exact': sp.simplify(
            phase_physical / density_scale
            - omega_dim**2 * f**2 / (2 * sigma**2 * n_metric)
        ) == 0,
    }
    return {
        'checks': checks,
        'definitions': {
            'x': 'm_s r',
            'f': 'sqrt(lambda) chi/m_s',
            'Omega': 'omega/m_s',
            'a': 'g_6 m_s^2/lambda^2',
            'density_scale': 'm_s^4/lambda',
        },
        'all_pass': bool(all(checks.values())),
    }


def symbolic_gate() -> dict[str, Any]:
    einstein_tensor = spherical_einstein_tensor_gate()
    reduced_scalar = reduced_scalar_action_gate()
    conservation = anisotropic_conservation_gate()
    dimensionless = dimensionless_reduction_gate()
    f, fp, omega, sigma, n, a = sp.symbols(
        'f fp omega sigma N a', positive=True, finite=True
    )
    v = f**2 / 2 - f**4 / 4 + a * f**6 / 6
    force = sp.diff(v, f)
    rho = n * fp**2 / 2 + omega**2 * f**2 / (2 * sigma**2 * n) + v
    p_r = n * fp**2 / 2 + omega**2 * f**2 / (2 * sigma**2 * n) - v
    p_t = -n * fp**2 / 2 + omega**2 * f**2 / (2 * sigma**2 * n) - v

    f0, sigma0, alpha = sp.symbols(
        'f0 sigma0 alpha', positive=True, finite=True
    )
    force0 = f0 - f0**3 + a * f0**5
    v0 = f0**2 / 2 - f0**4 / 4 + a * f0**6 / 6
    f2 = (force0 - omega**2 * f0 / sigma0**2) / 6
    rho0 = omega**2 * f0**2 / (2 * sigma0**2) + v0
    m3 = rho0 / 3
    s2 = alpha * omega**2 * f0**2 / (2 * sigma0**2)

    scalar_nec_r = sp.simplify(rho + p_r)
    scalar_nec_t = sp.simplify(rho + p_t)
    benchmark_force = sp.factor(force.subs(a, sp.Rational(1, 4)))
    x_tail, k_tail, d_tail = sp.symbols(
        'x_tail k_tail d_tail', positive=True, finite=True
    )
    omega_tail = sp.symbols('Omega_tail', positive=True, finite=True)
    yukawa_tail = sp.exp(-k_tail * x_tail) / x_tail
    yukawa_equation = sp.simplify(
        sp.diff(yukawa_tail, x_tail, 2)
        + 2 * sp.diff(yukawa_tail, x_tail) / x_tail
        - k_tail**2 * yukawa_tail
    )
    schwarzschild_power = (
        -1 + d_tail * (2 * omega_tail**2 - 1) / k_tail
    )
    schwarzschild_order_one_over_x = sp.simplify(
        -2 * k_tail * (schwarzschild_power + 1)
        - 2 * d_tail * (1 - omega_tail**2)
        + 2 * d_tail * omega_tail**2
    )
    n_c = sp.symbols('n_C', positive=True, finite=True)
    rho_c = sp.Function('rho_C')(n_c)
    p_c = n_c * sp.diff(rho_c, n_c) - rho_c
    collective_nec = sp.simplify(rho_c + p_c)
    k_chi, k_theta = sp.symbols('k_chi k_theta', real=True, finite=True)
    chi = sp.symbols('chi', nonnegative=True, finite=True)
    covariant_scalar_nec = k_chi**2 + chi**2 * k_theta**2
    x_round = sp.symbols('x_round', positive=True, finite=True)
    theta_plus = 2 * sp.sqrt(n) / x_round
    theta_minus = -2 * sp.sqrt(n) / x_round
    x_limit, mass_limit = sp.symbols(
        'x_limit M_limit', positive=True, finite=True
    )
    n_definition_limit = 1 - 2 * alpha * mass_limit / x_limit
    lapse_rhs_limit = alpha * x_limit * (
        fp**2 + omega**2 * f**2 /
        (sigma**2 * n_definition_limit**2)
    )
    alpha_zero_metric_decoupling_exact = bool(
        sp.simplify(n_definition_limit.subs(alpha, 0) - 1) == 0
        and sp.simplify(lapse_rhs_limit.subs(alpha, 0)) == 0
    )
    checks = {
        'potential_force_exact': sp.simplify(
            force - (f - f**3 + a * f**5)
        ) == 0,
        'scalar_radial_nec_exact': sp.simplify(
            scalar_nec_r - (n * fp**2 + omega**2 * f**2 / (sigma**2 * n))
        ) == 0,
        'scalar_tangential_nec_exact': sp.simplify(
            scalar_nec_t - omega**2 * f**2 / (sigma**2 * n)
        ) == 0,
        'vacuum_source_zero_exact': all(
            sp.simplify(expr.subs({f: 0, fp: 0})) == 0
            for expr in (rho, p_r, p_t)
        ),
        'benchmark_force_factor_exact': sp.simplify(
            benchmark_force - f * (f**2 - 2)**2 / 4
        ) == 0,
        'flat_yukawa_tail_solution_exact': yukawa_equation == 0,
        'schwarzschild_tail_power_exact': sp.simplify(
            schwarzschild_order_one_over_x
        ) == 0,
        'centre_scalar_series_exact': sp.simplify(
            6 * f2 + omega**2 * f0 / sigma0**2 - force0
        ) == 0,
        'centre_mass_series_exact': sp.simplify(3 * m3 - rho0) == 0,
        'centre_lapse_series_exact': sp.simplify(
            2 * s2 - alpha * omega**2 * f0**2 / sigma0**2
        ) == 0,
        'collective_nec_identity_exact': sp.simplify(
            collective_nec - n_c * sp.diff(rho_c, n_c)
        ) == 0,
        'covariant_scalar_nec_exact': bool(
            sp.ask(sp.Q.nonnegative(covariant_scalar_nec))
        ),
        'round_sphere_null_expansion_product_exact': sp.simplify(
            theta_plus * theta_minus + 4 * n / x_round**2
        ) == 0,
        'einstein_tensor_direct_derivation_exact': einstein_tensor['all_pass'],
        'reduced_scalar_euler_lagrange_exact': reduced_scalar['all_pass'],
        'dimensionless_mass_normalization_exact': einstein_tensor['checks'][
            'misner_sharp_physical_normalization_exact'
        ],
        'alpha_zero_scalar_equation_exact': reduced_scalar[
            'alpha_zero_flat_equation_exact'
        ],
        'alpha_zero_metric_decoupling_exact': (
            alpha_zero_metric_decoupling_exact
        ),
        'alpha_zero_equation_limit_exact': bool(
            reduced_scalar['alpha_zero_flat_equation_exact']
            and alpha_zero_metric_decoupling_exact
        ),
        'anisotropic_tov_conservation_exact': conservation['all_pass'],
        'dimensionless_field_reduction_exact': dimensionless['all_pass'],
    }
    return {
        'checks': checks,
        'all_pass': bool(all(checks.values())),
        'einstein_tensor_derivation': einstein_tensor,
        'reduced_scalar_action_derivation': reduced_scalar,
        'anisotropic_conservation_derivation': conservation,
        'dimensionless_reduction': dimensionless,
        'identities': {
            'metric': 'ds^2=-sigma^2 N dt^2+N^-1 dx^2+x^2 dOmega^2',
            'mass_definition': 'N=1-2 alpha M/x',
            'mass_equation': 'M_prime=x^2 rho',
            'lapse_equation': '(ln sigma)_prime=alpha x[f_prime^2+Omega^2 f^2/(sigma^2 N^2)]',
            'alpha_zero_metric_limit': (
                'alpha=0 gives N=1 and (ln sigma)_prime=0; '
                'sigma(infinity)=1 then fixes sigma=1'
            ),
            'scalar_equation': '(sigma x^2 N f_prime)_prime/(sigma x^2)+Omega^2 f/(sigma^2 N)-v_prime(f)=0',
            'scalar_nec_radial': str(scalar_nec_r),
            'scalar_nec_tangential': str(scalar_nec_t),
            'collective_nec': 'rho_C+p_C=n_C rho_C_prime>0',
            'covariant_scalar_nec': (
                'T_mu_nu k^mu k^nu=(k.dchi)^2+chi^2(k.dtheta_O)^2>=0'
            ),
            'round_sphere_expansions': 'theta_plus theta_minus=-4N/x^2',
            'tail': (
                'f~C exp(-k x) x^s, k=sqrt(1-Omega^2), '
                's=-1+alpha M_infinity(2Omega^2-1)/k'
            ),
        },
    }


def potential(f: np.ndarray | float) -> np.ndarray | float:
    return f**2 / 2.0 - f**4 / 4.0 + A_BENCH * f**6 / 6.0


def potential_force(f: np.ndarray | float) -> np.ndarray | float:
    return f - f**3 + A_BENCH * f**5


def omega_from_parameter(parameter: np.ndarray | float) -> float:
    z = float(np.asarray(parameter).reshape(-1)[0])
    if z >= 0.0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def omega_parameter(omega: float) -> np.ndarray:
    if not (0.0 < omega < 1.0):
        raise ValueError('Localization requires 0<Omega<1')
    return np.array([math.log(omega / (1.0 - omega))], dtype=float)


def matter_arrays(
    f: np.ndarray,
    fp: np.ndarray,
    mass: np.ndarray,
    log_sigma: np.ndarray,
    x: np.ndarray,
    alpha: float,
    omega: float,
) -> dict[str, np.ndarray]:
    sigma = np.exp(log_sigma)
    n_metric = 1.0 - 2.0 * alpha * mass / x
    phase = omega**2 * f**2 / (2.0 * sigma**2 * n_metric)
    gradient = n_metric * fp**2 / 2.0
    v = potential(f)
    return {
        'sigma': sigma,
        'N': n_metric,
        'rho': gradient + phase + v,
        'p_r': gradient + phase - v,
        'p_t': -gradient + phase - v,
        'gradient': gradient,
        'phase': phase,
        'potential': v,
    }


def solve_flat_seed(radius: float = RADIUS_BENCH) -> object:
    x = np.linspace(0.0, radius, INITIAL_NODES)
    q = np.exp(np.clip(x - 4.0, -700.0, 700.0))
    f = 1.8 / (1.0 + q)
    fp = -1.8 * q / (1.0 + q) ** 2
    y = np.vstack((f, fp))
    omega = W3_58_TARGET['Omega']
    k = math.sqrt(1.0 - omega**2)

    def fun(_x: np.ndarray, yy: np.ndarray) -> np.ndarray:
        ff = yy[0]
        return np.vstack((yy[1], (1.0 - omega**2) * ff - ff**3 + A_BENCH * ff**5))

    def bc(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
        return np.array([
            ya[1],
            yb[1] + (k + 1.0 / radius) * yb[0],
        ])

    solution = solve_bvp(
        fun,
        bc,
        x,
        y,
        S=np.array([[0.0, 0.0], [0.0, -2.0]]),
        tol=TOL_BENCH,
        max_nodes=MAX_NODES,
        verbose=0,
    )
    if not solution.success:
        raise RuntimeError(f'Flat seed failed: {solution.message}')
    return solution


def initial_coupled_seed(x: np.ndarray, flat: object) -> tuple[np.ndarray, np.ndarray]:
    f, fp = flat.sol(x)
    omega = W3_58_TARGET['Omega']
    rho = fp**2 / 2.0 + omega**2 * f**2 / 2.0 + potential(f)
    rho0 = omega**2 * F0_BENCH**2 / 2.0 + potential(F0_BENCH)
    mass = np.empty_like(x)
    mass[0] = rho0 * x[0]**3 / 3.0
    mass[1:] = mass[0] + cumulative_trapezoid(x**2 * rho, x=x)
    log_sigma = np.zeros_like(x)
    return np.vstack((f, fp, mass, log_sigma)), omega_parameter(omega)


def seed_from_solution(
    x: np.ndarray,
    solution: object,
    alpha: float,
) -> tuple[np.ndarray, np.ndarray]:
    source_radius = float(solution.x[-1])
    omega = omega_from_parameter(solution.p)
    inside = x <= source_radius
    y = np.empty((4, x.size), dtype=float)
    y[:, inside] = solution.sol(x[inside])
    if np.any(~inside):
        edge = solution.sol(source_radius)
        k = math.sqrt(1.0 - omega**2)
        d = alpha * float(edge[2])
        tail_power = -1.0 + d * (2.0 * omega**2 - 1.0) / k
        xx = x[~inside]
        tail = (
            edge[0]
            * (xx / source_radius) ** tail_power
            * np.exp(-k * (xx - source_radius))
        )
        y[0, ~inside] = tail
        y[1, ~inside] = (-k + tail_power / xx) * tail
        y[2, ~inside] = edge[2]
        y[3, ~inside] = 0.0
    return y, np.array(solution.p, dtype=float)


def curved_equations(alpha: float):
    def equations(x: np.ndarray, y: np.ndarray, parameter: np.ndarray) -> np.ndarray:
        f, fp, mass, log_sigma = y
        omega = omega_from_parameter(parameter)
        fields = matter_arrays(f, fp, mass, log_sigma, x, alpha, omega)
        sigma = fields['sigma']
        n_metric = fields['N']
        rho = fields['rho']
        mass_prime = x**2 * rho
        log_sigma_prime = alpha * x * (
            fp**2 + omega**2 * f**2 / (sigma**2 * n_metric**2)
        )
        n_prime = -2.0 * alpha * (mass_prime / x - mass / x**2)
        fp_prime = (
            (potential_force(f) - omega**2 * f / (sigma**2 * n_metric)) / n_metric
            - (n_prime / n_metric + log_sigma_prime + 2.0 / x) * fp
        )
        return np.vstack((fp, fp_prime, mass_prime, log_sigma_prime))

    return equations


def curved_boundary(radius: float, alpha: float):
    def boundary(
        ya: np.ndarray,
        yb: np.ndarray,
        parameter: np.ndarray,
    ) -> np.ndarray:
        omega = omega_from_parameter(parameter)
        sigma_a = math.exp(float(ya[3]))
        force0 = float(potential_force(F0_BENCH))
        f2 = (force0 - omega**2 * F0_BENCH / sigma_a**2) / 6.0
        rho0 = omega**2 * F0_BENCH**2 / (2.0 * sigma_a**2) + float(
            potential(F0_BENCH)
        )
        mass3 = rho0 / 3.0
        k = math.sqrt(1.0 - omega**2)
        d = alpha * float(yb[2])
        tail_power = -1.0 + d * (2.0 * omega**2 - 1.0) / k
        return np.array([
            ya[0] - F0_BENCH - f2 * EPS**2,
            ya[1] - 2.0 * f2 * EPS,
            ya[2] - mass3 * EPS**3,
            yb[3],
            yb[1] + (k - tail_power / radius) * yb[0],
        ])

    return boundary


def solve_coupled(
    alpha: float,
    radius: float = RADIUS_BENCH,
    tolerance: float = TOL_BENCH,
    seed: object | None = None,
    flat: object | None = None,
) -> object:
    x = np.linspace(EPS, radius, INITIAL_NODES)
    if seed is None:
        if flat is None:
            flat = solve_flat_seed(radius)
        y, parameter = initial_coupled_seed(x, flat)
    else:
        y, parameter = seed_from_solution(x, seed, alpha)
    solution = solve_bvp(
        curved_equations(alpha),
        curved_boundary(radius, alpha),
        x,
        y,
        p=parameter,
        tol=tolerance,
        max_nodes=MAX_NODES,
        verbose=0,
    )
    if not solution.success:
        raise RuntimeError(
            f'Coupled BVP failed for alpha={alpha}, X={radius}, tol={tolerance}: '
            f'{solution.message}'
        )
    test_x = np.linspace(EPS, radius, 4001)
    test_y = solution.sol(test_x)
    omega = omega_from_parameter(solution.p)
    n_metric = 1.0 - 2.0 * alpha * test_y[2] / test_x
    if not (0.0 < omega < 1.0 and float(np.min(n_metric)) > 0.0):
        raise RuntimeError('Candidate left the localized horizonless continuation segment')
    return solution


def normalized_l2(
    x: np.ndarray,
    residual: np.ndarray,
    scale: np.ndarray,
) -> float:
    numerator = simpson(x**2 * residual**2, x=x)
    denominator = simpson(x**2 * scale**2, x=x)
    return float(math.sqrt(numerator / max(denominator, 1.0e-30)))


def independent_residuals(
    solution: object,
    alpha: float,
    radius: float,
    points: int = 20001,
) -> dict[str, Any]:
    x_all = np.linspace(EPS, radius, points)
    f_all, fp_all, mass_all, log_sigma_all = solution.sol(x_all)
    omega = omega_from_parameter(solution.p)
    fields_all = matter_arrays(
        f_all, fp_all, mass_all, log_sigma_all, x_all, alpha, omega
    )
    mask = (x_all >= 0.02) & (x_all <= radius - 1.0)
    x = x_all[mask]
    f = f_all[mask]
    fp = fp_all[mask]
    mass = mass_all[mask]
    log_sigma = log_sigma_all[mask]
    sigma = fields_all['sigma'][mask]
    n_metric = fields_all['N'][mask]
    rho = fields_all['rho'][mask]
    p_r = fields_all['p_r'][mask]
    p_t = fields_all['p_t'][mask]

    fpp = np.gradient(fp, x, edge_order=2)
    mass_prime = np.gradient(mass, x, edge_order=2)
    log_sigma_prime = np.gradient(log_sigma, x, edge_order=2)
    n_prime = np.gradient(n_metric, x, edge_order=2)
    p_r_prime = np.gradient(p_r, x, edge_order=2)

    scalar_terms = (
        n_metric * fpp,
        (n_prime + n_metric * (log_sigma_prime + 2.0 / x)) * fp,
        omega**2 * f / (sigma**2 * n_metric),
        -potential_force(f),
    )
    scalar_residual = sum(scalar_terms)
    scalar_scale = sum(np.abs(term) for term in scalar_terms)

    mass_terms = (mass_prime, -x**2 * rho)
    mass_residual = sum(mass_terms)
    mass_scale = sum(np.abs(term) for term in mass_terms)

    lapse_rhs = alpha * x * (
        fp**2 + omega**2 * f**2 / (sigma**2 * n_metric**2)
    )
    lapse_terms = (log_sigma_prime, -lapse_rhs)
    lapse_residual = sum(lapse_terms)
    lapse_scale = sum(np.abs(term) for term in lapse_terms)

    phi_prime = alpha * (mass + x**3 * p_r) / (x**2 * n_metric)
    tov_terms = (
        p_r_prime,
        (rho + p_r) * phi_prime,
        -2.0 * (p_t - p_r) / x,
    )
    tov_residual = sum(tov_terms)
    tov_scale = sum(np.abs(term) for term in tov_terms)

    records = {
        'grid_points': points,
        'centre_cut': 0.02,
        'outer_cut': 1.0,
        'scalar_equation_normalized_l2': normalized_l2(
            x, scalar_residual, scalar_scale
        ),
        'mass_equation_normalized_l2': normalized_l2(
            x, mass_residual, mass_scale
        ),
        'lapse_equation_normalized_l2': normalized_l2(
            x, lapse_residual, lapse_scale
        ),
        'anisotropic_tov_normalized_l2': normalized_l2(
            x, tov_residual, tov_scale
        ),
    }
    records['threshold'] = 3.0e-4
    records['pass'] = bool(
        max(
            records['scalar_equation_normalized_l2'],
            records['mass_equation_normalized_l2'],
            records['lapse_equation_normalized_l2'],
            records['anisotropic_tov_normalized_l2'],
        ) < records['threshold']
    )
    return records


def profile_observables(
    solution: object,
    alpha: float,
    radius: float,
    points: int = 16001,
    with_residuals: bool = True,
) -> dict[str, Any]:
    x = np.linspace(EPS, radius, points)
    f, fp, mass, log_sigma = solution.sol(x)
    first_derivatives = solution.sol(x, 1)
    second_derivatives = solution.sol(x, 2)
    omega = omega_from_parameter(solution.p)
    fields = matter_arrays(f, fp, mass, log_sigma, x, alpha, omega)
    sigma = fields['sigma']
    n_metric = fields['N']
    rho = fields['rho']
    p_r = fields['p_r']
    p_t = fields['p_t']

    charge_density = omega * f**2 / (sigma * n_metric)
    charge = simpson(x**2 * charge_density, x=x)
    proper_energy = simpson(x**2 * rho / np.sqrt(n_metric), x=x)
    mass_integral = simpson(x**2 * rho, x=x)
    charge_radius = math.sqrt(
        simpson(x**4 * charge_density, x=x) / max(charge, 1.0e-30)
    )
    compactness = 2.0 * alpha * mass / x
    ricci_over_m2 = 2.0 * alpha * (rho - p_r - 2.0 * p_t)

    expected_tail = math.sqrt(1.0 - omega**2)
    tail_power_expected = (
        -1.0
        + alpha * float(mass[-1]) * (2.0 * omega**2 - 1.0) / expected_tail
    )
    positive_tail = (
        (f > 1.0e-12) & (f < 1.0e-5) & (x > 3.0)
    )
    tail_fit_sample_count = int(np.count_nonzero(positive_tail))
    if tail_fit_sample_count >= TAIL_FIT_MIN_SAMPLES:
        xt = x[positive_tail]
        fit_matrix = np.column_stack((
            xt,
            np.log(xt),
            1.0 / xt,
            1.0 / xt**2,
            np.ones_like(xt),
        ))
        fit_coefficients = np.linalg.lstsq(
            fit_matrix, np.log(f[positive_tail]), rcond=None
        )[0]
        tail_exponent = -float(fit_coefficients[0])
        tail_power_fitted = float(fit_coefficients[1])
    else:
        tail_exponent = 0.0
        tail_power_fitted = 0.0

    sigma0 = float(sigma[0])
    force0 = float(potential_force(F0_BENCH))
    f2 = (force0 - omega**2 * F0_BENCH / sigma0**2) / 6.0
    rho0 = omega**2 * F0_BENCH**2 / (2.0 * sigma0**2) + float(
        potential(F0_BENCH)
    )
    mass3 = rho0 / 3.0
    s2 = alpha * omega**2 * F0_BENCH**2 / (2.0 * sigma0**2)
    n2 = -2.0 * alpha * mass3
    phi2 = s2 + n2 / 2.0
    lambda2 = -n2 / 2.0
    centre_riemann = (
        2.0 * phi2,
        2.0 * phi2,
        2.0 * lambda2,
        -n2,
    )
    centre_kretschmann = 4.0 * (
        centre_riemann[0]**2
        + 2.0 * centre_riemann[1]**2
        + 2.0 * centre_riemann[2]**2
        + centre_riemann[3]**2
    )

    curvature_mask = x >= 0.02
    xc = x[curvature_mask]
    nc = n_metric[curvature_mask]
    mc = mass[curvature_mask]
    mass_prime = first_derivatives[2, curvature_mask]
    mass_second = second_derivatives[2, curvature_mask]
    s_prime = first_derivatives[3, curvature_mask]
    s_second = second_derivatives[3, curvature_mask]
    n_prime = -2.0 * alpha * (mass_prime / xc - mc / xc**2)
    n_second = -2.0 * alpha * (
        mass_second / xc - 2.0 * mass_prime / xc**2 + 2.0 * mc / xc**3
    )
    phi_prime = s_prime + n_prime / (2.0 * nc)
    phi_second = s_second + 0.5 * (
        n_second / nc - (n_prime / nc)**2
    )
    lambda_prime = -n_prime / (2.0 * nc)
    riemann_trtr = nc * (
        phi_second + phi_prime**2 - phi_prime * lambda_prime
    )
    riemann_ttheta = nc * phi_prime / xc
    riemann_rtheta = nc * lambda_prime / xc
    riemann_thetaphi = (1.0 - nc) / xc**2
    kretschmann = 4.0 * (
        riemann_trtr**2
        + 2.0 * riemann_ttheta**2
        + 2.0 * riemann_rtheta**2
        + riemann_thetaphi**2
    )
    centre = {
        'f_value_residual': float(abs(f[0] - F0_BENCH - f2 * EPS**2)),
        'f_derivative_residual': float(abs(fp[0] - 2.0 * f2 * EPS)),
        'mass_cubic_residual': float(abs(mass[0] - rho0 * EPS**3 / 3.0)),
        'isotropy_residual': float(abs(p_r[0] - p_t[0])),
        'M_over_x_cubed': float(mass[0] / EPS**3),
        'Kretschmann_over_m_four': float(centre_kretschmann),
    }
    tail_index = int(np.searchsorted(x, 0.75 * radius))
    observables: dict[str, Any] = {
        'alpha': alpha,
        'Omega': omega,
        'adaptive_nodes': int(solution.x.size),
        'collocation_rms_residual_max': float(np.max(solution.rms_residuals)),
        'central_amplitude': float(f[0]),
        'minimum_amplitude': float(np.min(f)),
        'maximum_outward_derivative': float(np.max(fp[1:])),
        'central_lapse_sigma': sigma0,
        'central_redshift_to_infinity': float(1.0 / sigma0 - 1.0),
        'misner_sharp_adm_mass_dimensionless': float(mass[-1]),
        'mass_integral_dimensionless': float(mass_integral),
        'mass_integral_relative_residual': relative_change(
            float(mass_integral), float(mass[-1])
        ),
        'proper_energy_dimensionless': float(proper_energy),
        'noether_charge_dimensionless': float(charge),
        'charge_rms_radius_dimensionless': float(charge_radius),
        'adm_mass_per_mass_charge': float(mass[-1] / charge),
        'maximum_compactness_2alphaM_over_x': float(np.max(compactness)),
        'minimum_N': float(np.min(n_metric)),
        'minimum_sigma': float(np.min(sigma)),
        'minimum_scalar_radial_nec': float(np.min(rho + p_r)),
        'minimum_scalar_tangential_nec': float(np.min(rho + p_t)),
        'maximum_abs_Ricci_over_m_squared': float(np.max(np.abs(ricci_over_m2))),
        'maximum_Kretschmann_over_m_four': float(max(
            centre_kretschmann, float(np.max(kretschmann))
        )),
        'maximum_abs_M_over_x_cubed': float(np.max(np.abs(mass / x**3))),
        'tail_exponent_fitted': tail_exponent,
        'tail_exponent_expected': expected_tail,
        'tail_exponent_absolute_error': float(abs(tail_exponent - expected_tail)),
        'tail_power_fitted': tail_power_fitted,
        'tail_power_expected': float(tail_power_expected),
        'tail_power_absolute_error': float(
            abs(tail_power_fitted - tail_power_expected)
        ),
        'tail_fit_sample_count': tail_fit_sample_count,
        'tail_fit_minimum_samples': TAIL_FIT_MIN_SAMPLES,
        'tail_fit_model': 'ln f=c-k_fit x+s_fit ln x+b_1/x+b_2/x^2',
        'outer_mass_fraction_after_0_75X': float(
            (mass[-1] - mass[tail_index]) / max(abs(mass[-1]), 1.0e-30)
        ),
        'outer_sigma_normalization_residual': float(abs(log_sigma[-1])),
        'robin_boundary_residual': float(
            abs(
                fp[-1]
                + (expected_tail - tail_power_expected / radius) * f[-1]
            )
        ),
        'centre_series': centre,
    }
    if with_residuals:
        observables['independent_finite_grid_residuals'] = independent_residuals(
            solution, alpha, radius
        )
    return observables


def continuation_gate() -> tuple[dict[str, Any], object]:
    flat = solve_flat_seed(RADIUS_BENCH)
    previous: object | None = None
    records: list[dict[str, Any]] = []
    canonical: object | None = None
    for alpha in ALPHA_GRID:
        solution = solve_coupled(
            alpha,
            radius=RADIUS_BENCH,
            tolerance=TOL_BENCH,
            seed=previous,
            flat=flat,
        )
        observables = profile_observables(
            solution, alpha, RADIUS_BENCH, points=16001
        )
        records.append({
            'alpha': alpha,
            'observables': observables,
        })
        previous = solution
        canonical = solution
    if canonical is None:
        raise RuntimeError('Continuation produced no solution')

    flat_obs = records[0]['observables']
    regression_changes = {
        'Omega': relative_change(flat_obs['Omega'], W3_58_TARGET['Omega']),
        'energy': relative_change(
            flat_obs['proper_energy_dimensionless'], W3_58_TARGET['energy']
        ),
        'charge': relative_change(
            flat_obs['noether_charge_dimensionless'], W3_58_TARGET['charge']
        ),
        'charge_rms_radius': relative_change(
            flat_obs['charge_rms_radius_dimensionless'],
            W3_58_TARGET['charge_rms_radius'],
        ),
    }
    regression_threshold = 3.0e-4
    regression_pass = max(regression_changes.values()) < regression_threshold

    point_checks = []
    for item in records:
        obs = item['observables']
        centre = obs['centre_series']
        point_checks.append(bool(
            0.0 < obs['Omega'] < 1.0
            and obs['minimum_N'] > 0.0
            and obs['minimum_sigma'] > 0.0
            and obs['minimum_amplitude'] >= -1.0e-10
            and obs['maximum_outward_derivative'] <= 1.0e-8
            and obs['maximum_compactness_2alphaM_over_x'] < 1.0
            and obs['tail_exponent_absolute_error'] < 3.0e-3
            and obs['tail_power_absolute_error'] < 3.0e-3
            and obs['independent_finite_grid_residuals']['pass']
            and max(
                centre['f_value_residual'],
                centre['f_derivative_residual'],
                centre['mass_cubic_residual'],
                centre['isotropy_residual'],
            ) < 3.0e-3
        ))
    return {
        'alpha_grid': list(ALPHA_GRID),
        'records': records,
        'flat_limit_regression': {
            'relative_changes': regression_changes,
            'threshold': regression_threshold,
            'pass': regression_pass,
        },
        'all_continuation_points_pass': bool(all(point_checks)),
        'pass': bool(regression_pass and all(point_checks)),
    }, canonical


def convergence_gate(canonical: object) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for radius in (60.0, 80.0, 100.0):
        for tolerance in (1.0e-6, 3.0e-7, 1.0e-7):
            solution = solve_coupled(
                ALPHA_GRID[-1],
                radius=radius,
                tolerance=tolerance,
                seed=canonical,
            )
            observables = profile_observables(
                solution,
                ALPHA_GRID[-1],
                radius,
                points=8001,
                with_residuals=False,
            )
            records.append({
                'radius': radius,
                'tolerance': tolerance,
                'observables': observables,
            })
    reference = next(
        item['observables'] for item in records
        if item['radius'] == 80.0 and item['tolerance'] == 1.0e-7
    )
    tracked = (
        'Omega',
        'misner_sharp_adm_mass_dimensionless',
        'noether_charge_dimensionless',
        'charge_rms_radius_dimensionless',
        'maximum_Kretschmann_over_m_four',
    )
    maximum_relative_change = max(
        relative_change(item['observables'][key], reference[key])
        for item in records for key in tracked
    )
    convergence_threshold = 5.0e-4

    quadrature_records: list[dict[str, Any]] = []
    for points in (4001, 8001, 16001):
        obs = profile_observables(
            canonical,
            ALPHA_GRID[-1],
            RADIUS_BENCH,
            points=points,
            with_residuals=False,
        )
        quadrature_records.append({
            'points': points,
            'observables': {key: obs[key] for key in tracked},
        })
    quadrature_reference = quadrature_records[-1]['observables']
    quadrature_maximum_relative_change = max(
        relative_change(item['observables'][key], quadrature_reference[key])
        for item in quadrature_records for key in tracked
    )
    quadrature_threshold = 5.0e-4
    curvature_relative_change = max(
        relative_change(
            item['observables']['maximum_Kretschmann_over_m_four'],
            reference['maximum_Kretschmann_over_m_four'],
        )
        for item in records
    )
    curvature_quadrature_relative_change = max(
        relative_change(
            item['observables']['maximum_Kretschmann_over_m_four'],
            quadrature_reference['maximum_Kretschmann_over_m_four'],
        )
        for item in quadrature_records
    )
    curvature_pass = bool(
        curvature_relative_change < convergence_threshold
        and curvature_quadrature_relative_change < quadrature_threshold
    )
    pass_flag = bool(
        maximum_relative_change < convergence_threshold
        and quadrature_maximum_relative_change < quadrature_threshold
        and curvature_pass
    )
    return {
        'domain_tolerance_records': records,
        'tracked_observables': list(tracked),
        'maximum_relative_change': maximum_relative_change,
        'threshold': convergence_threshold,
        'quadrature_records': quadrature_records,
        'quadrature_maximum_relative_change': quadrature_maximum_relative_change,
        'quadrature_threshold': quadrature_threshold,
        'curvature_relative_change': curvature_relative_change,
        'curvature_quadrature_relative_change': curvature_quadrature_relative_change,
        'curvature_pass': curvature_pass,
        'pass': pass_flag,
    }


def regularity_and_no_go_gate(
    canonical_observables: dict[str, Any],
    symbolic: dict[str, Any],
) -> dict[str, Any]:
    centre = canonical_observables['centre_series']
    witness_regular = bool(
        canonical_observables['minimum_N'] > 0.0
        and canonical_observables['minimum_sigma'] > 0.0
        and math.isfinite(canonical_observables['maximum_abs_Ricci_over_m_squared'])
        and math.isfinite(canonical_observables['maximum_Kretschmann_over_m_four'])
        and math.isfinite(canonical_observables['maximum_abs_M_over_x_cubed'])
        and centre['isotropy_residual'] < 1.0e-8
    )
    scalar_nec_exact = bool(
        symbolic['checks']['scalar_radial_nec_exact']
        and symbolic['checks']['scalar_tangential_nec_exact']
        and symbolic['checks']['covariant_scalar_nec_exact']
    )
    collective_nec_exact = bool(
        symbolic['checks']['collective_nec_identity_exact']
    )
    numerical_nec = bool(
        canonical_observables['minimum_scalar_radial_nec'] >= -1.0e-12
        and canonical_observables['minimum_scalar_tangential_nec'] >= -1.0e-12
    )
    round_sphere_expansions_exact = bool(
        symbolic['checks']['round_sphere_null_expansion_product_exact']
    )
    spherical_killing_horizon_present = bool(
        canonical_observables['minimum_N'] <= 0.0
    )
    round_sphere_trapped_surface_present = bool(
        not round_sphere_expansions_exact
        or canonical_observables['minimum_N'] < 0.0
    )
    return {
        'regular_horizonless_witness_pass': witness_regular,
        'scalar_source_nec_exact': scalar_nec_exact,
        'collective_source_nec_exact': collective_nec_exact,
        'canonical_numerical_nec_pass': numerical_nec,
        'round_sphere_null_expansion_product_exact': round_sphere_expansions_exact,
        'spherical_killing_horizon_present': spherical_killing_horizon_present,
        'round_sphere_trapped_surface_present': round_sphere_trapped_surface_present,
        'general_closed_surface_trapping_search_performed': False,
        'penrose_boundary': {
            'statement': (
                'If a globally hyperbolic spacetime with a noncompact Cauchy '
                'hypersurface contains a closed future-trapped surface and obeys '
                'null convergence, future null geodesic completeness is impossible.'
            ),
            'application': (
                'The retained scalar and collective sources satisfy the null energy '
                'condition on their selected domains. Within this retained '
                'Einstein-NEC source class, a trapped null-complete regular interior '
                'is excluded whenever the remaining Penrose hypotheses hold.'
            ),
            'conditional_no_go_exact': bool(scalar_nec_exact and collective_nec_exact),
        },
        'pass': bool(
            witness_regular
            and scalar_nec_exact
            and collective_nec_exact
            and numerical_nec
            and round_sphere_expansions_exact
            and not spherical_killing_horizon_present
            and not round_sphere_trapped_surface_present
        ),
    }


def mutation_gate(canonical_solution: object) -> dict[str, Any]:
    base = {
        'metric_count': 1,
        'localized_rhs_sources': ('T_O',),
        'retained_nec_catalogue': ('T_C', 'T_O'),
        'collective_source_readded_locally': False,
        'w3_51_metric_used_in_strong_field': False,
        'collective_nec_sign': 1,
    }

    def valid(model: dict[str, Any]) -> bool:
        return bool(
            model['metric_count'] == 1
            and model['localized_rhs_sources'] == ('T_O',)
            and model['retained_nec_catalogue'] == ('T_C', 'T_O')
            and not model['collective_source_readded_locally']
            and not model['w3_51_metric_used_in_strong_field']
            and model['collective_nec_sign'] == 1
        )

    structural_mutations = {
        'second_metric': {'metric_count': 2},
        'duplicate_scalar_source_registry': {
            'localized_rhs_sources': ('T_O', 'T_O')
        },
        'collective_source_local_readdition': {
            'collective_source_readded_locally': True
        },
        'weak_field_metric_extrapolation': {'w3_51_metric_used_in_strong_field': True},
        'collective_nec_sign_flip': {'collective_nec_sign': -1},
    }
    structural_detections: dict[str, bool] = {}
    for name, changes in structural_mutations.items():
        candidate = dict(base)
        candidate.update(changes)
        structural_detections[name] = not valid(candidate)

    alpha = ALPHA_GRID[-1]
    x = np.linspace(
        MUTATION_RESIDUAL_CENTRE_CUT,
        RADIUS_BENCH - MUTATION_RESIDUAL_OUTER_CUT,
        MUTATION_RESIDUAL_NODES,
    )
    f, fp, mass, log_sigma = canonical_solution.sol(x)
    derivatives = canonical_solution.sol(x, 1)
    omega = omega_from_parameter(canonical_solution.p)
    fields = matter_arrays(f, fp, mass, log_sigma, x, alpha, omega)
    sigma = fields['sigma']
    n_metric = fields['N']
    mass_prime = derivatives[2]
    log_sigma_prime = derivatives[3]
    mass_source = x**2 * fields['rho']
    lapse_source = alpha * x * (
        fp**2 + omega**2 * f**2 / (sigma**2 * n_metric**2)
    )

    base_mass_residual = normalized_l2(
        x, mass_prime - mass_source, np.abs(mass_prime) + np.abs(mass_source)
    )
    base_lapse_residual = normalized_l2(
        x,
        log_sigma_prime - lapse_source,
        np.abs(log_sigma_prime) + np.abs(lapse_source),
    )
    equation_mutations = {
        'duplicate_scalar_source': normalized_l2(
            x,
            mass_prime - 2.0 * mass_source,
            np.abs(mass_prime) + 2.0 * np.abs(mass_source),
        ),
        'einstein_sign_flip': normalized_l2(
            x,
            mass_prime + mass_source,
            np.abs(mass_prime) + np.abs(mass_source),
        ),
        'missing_lapse_source': normalized_l2(
            x,
            log_sigma_prime,
            np.maximum(np.abs(log_sigma_prime), 1.0e-30),
        ),
    }
    base_threshold = 3.0e-4
    mutation_detection_threshold = 0.1
    equation_detections = {
        name: value > mutation_detection_threshold
        for name, value in equation_mutations.items()
    }
    equation_detections['duplicate_scalar_source'] = bool(
        equation_detections['duplicate_scalar_source']
        and structural_detections['duplicate_scalar_source_registry']
    )
    detections = {**structural_detections, **equation_detections}
    base_pass = bool(
        valid(base)
        and base_mass_residual < base_threshold
        and base_lapse_residual < base_threshold
    )
    return {
        'localized_rhs_sources': list(base['localized_rhs_sources']),
        'retained_nec_catalogue': list(base['retained_nec_catalogue']),
        'base_mass_residual': base_mass_residual,
        'base_lapse_residual': base_lapse_residual,
        'base_threshold': base_threshold,
        'equation_mutation_residual_grid_points': MUTATION_RESIDUAL_NODES,
        'equation_mutation_residual_centre_cut': MUTATION_RESIDUAL_CENTRE_CUT,
        'equation_mutation_residual_outer_cut': MUTATION_RESIDUAL_OUTER_CUT,
        'equation_mutation_residuals': equation_mutations,
        'mutation_detection_threshold': mutation_detection_threshold,
        'base_pass': base_pass,
        'detections': detections,
        'pass': bool(base_pass and all(detections.values())),
    }


def package_gate() -> dict[str, Any]:
    expected = {
        PREREG.name,
        Path(__file__).name,
        OUTPUT.name,
    }
    actual_before_write = {
        path.name for path in HERE.iterdir() if path.is_file()
    }
    subdirectories = [path.name for path in HERE.iterdir() if path.is_dir()]
    unexpected = sorted(actual_before_write - expected)
    missing_before_write = sorted(expected - actual_before_write)
    return {
        'expected_exact_final_files': sorted(expected),
        'actual_files_before_result_write': sorted(actual_before_write),
        'expected_missing_before_result_write': missing_before_write,
        'unexpected_files': unexpected,
        'subdirectories': subdirectories,
        'pass': bool(not unexpected and not subdirectories),
    }


def main() -> None:
    dependencies = dependency_gate()
    symbolic = symbolic_gate()
    continuation, canonical_solution = continuation_gate()
    canonical_observables = continuation['records'][-1]['observables']
    convergence = convergence_gate(canonical_solution)
    regularity_no_go = regularity_and_no_go_gate(
        canonical_observables, symbolic
    )
    mutations = mutation_gate(canonical_solution)
    package = package_gate()

    closure_flags = {
        'dependency_hashes_exact': dependencies['all_pass'],
        'one_einstein_metric_exact': bool(
            mutations['base_pass'] and mutations['detections']['second_metric']
        ),
        'one_localized_hilbert_source_exact': bool(
            dependencies['upstream_source_ledger_exact']
            and dependencies['upstream_action_and_hilbert_variation_exact']
            and symbolic['checks']['vacuum_source_zero_exact']
            and mutations['detections']['duplicate_scalar_source']
            and mutations['detections']['collective_source_local_readdition']
        ),
        'einstein_scalar_odes_exact': bool(
            symbolic['all_pass']
            and dependencies['upstream_action_and_hilbert_variation_exact']
        ),
        'dimensionless_field_reduction_exact': symbolic['checks'][
            'dimensionless_field_reduction_exact'
        ],
        'dimensionless_mass_normalization_exact': symbolic['checks'][
            'dimensionless_mass_normalization_exact'
        ],
        'alpha_zero_equation_limit_exact': symbolic['checks'][
            'alpha_zero_equation_limit_exact'
        ],
        'regular_centre_series_exact': bool(
            symbolic['checks']['centre_scalar_series_exact']
            and symbolic['checks']['centre_mass_series_exact']
            and symbolic['checks']['centre_lapse_series_exact']
        ),
        'asymptotic_schwarzschild_yukawa_map_exact': bool(
            symbolic['checks']['schwarzschild_tail_power_exact']
            and symbolic['checks']['vacuum_source_zero_exact']
        ),
        'misner_sharp_adm_mass_roles_exact': bool(
            symbolic['einstein_tensor_derivation']['checks'][
                'misner_sharp_mass_reduction_exact'
            ]
            and symbolic['einstein_tensor_derivation']['checks'][
                'misner_sharp_physical_normalization_exact'
            ]
        ),
        'ordinary_scalar_nec_exact': regularity_no_go['scalar_source_nec_exact'],
        'covariant_scalar_nec_exact': symbolic['checks'][
            'covariant_scalar_nec_exact'
        ],
        'collective_phase_nec_exact': regularity_no_go['collective_source_nec_exact'],
        'anisotropic_tov_conservation_exact': symbolic['checks'][
            'anisotropic_tov_conservation_exact'
        ],
        'round_sphere_null_expansion_exact': symbolic['checks'][
            'round_sphere_null_expansion_product_exact'
        ],
        'penrose_trapped_surface_implication_registered_exact': bool(
            regularity_no_go['penrose_boundary']['conditional_no_go_exact']
        ),
        'alpha_zero_w3_58_regression_pass': continuation['flat_limit_regression']['pass'],
        'regular_horizonless_backreaction_witness_numerical': bool(
            continuation['all_continuation_points_pass']
            and regularity_no_go['regular_horizonless_witness_pass']
            and convergence['curvature_pass']
        ),
        'domain_tolerance_convergence_pass': convergence['pass'],
        'curvature_convergence_pass': convergence['curvature_pass'],
        'independent_residual_recomputation_pass': bool(
            canonical_observables['independent_finite_grid_residuals']['pass']
        ),
        'mutation_controls_pass': mutations['pass'],
    }
    aggregate_pass = bool(all(closure_flags.values()) and package['pass'])
    closure_flags['aggregate_gate_pass'] = aggregate_pass

    status = (
        'PASS_CONDITIONAL_EXACT_UNCHANGED_EINSTEIN_BACKREACTION_AND_'
        'CURRENT_SOURCE_NEC_BOUNDARY__CONVERGED_NUMERICAL_REGULAR_'
        'HORIZONLESS_SELF_GRAVITATING_Q_BALL_WITNESS__REGULAR_TRAPPED_'
        'NULL_COMPLETE_INTERIOR_REQUIRES_FAILURE_OF_AT_LEAST_ONE_'
        'PENROSE_HYPOTHESIS'
        if aggregate_pass else
        'FAIL_W3_64_SOURCE_FIRST_EINSTEIN_STRONG_FIELD_GATE'
    )
    result: dict[str, Any] = {
        'schema_version': 'W3-64-result-v1.1',
        'claim_id': 'W3_64_SOURCE_FIRST_EINSTEIN_STRONG_FIELD_GATE',
        'model_version': 'W3-64-v1.1-EH-SEXTIC-U1-SOURCE-FIRST-SCHWARZSCHILD-TAIL',
        'status': status,
        'artifact_valid': False,
        'closure_flags': closure_flags,
        'evidence_type': {
            'action_equations_nec_and_no_go_boundary': 'CONDITIONAL_EXACT',
            'self_gravitating_profile': 'CONVERGED_NUMERICAL_EVIDENCE',
            'computer_assisted_proof': False,
            'observational_test': False,
        },
        'dependencies': dependencies,
        'symbolic': symbolic,
        'numerical': {
            'benchmark': {
                'a': A_BENCH,
                'f0': F0_BENCH,
                'alpha_grid': list(ALPHA_GRID),
                'X': RADIUS_BENCH,
                'tolerance': TOL_BENCH,
            },
            'continuation': continuation,
            'canonical_observables': canonical_observables,
            'convergence': convergence,
            'pass': bool(continuation['pass'] and convergence['pass']),
        },
        'regularity_and_penrose_boundary': regularity_no_go,
        'controls': mutations,
        'source_ledger': {
            'localized_einstein_rhs': ['T_O'],
            'homogeneous_collective_T_C_readded_locally': False,
            'retained_nec_catalogue': ['T_C', 'T_O'],
            'interpretation': (
                'The isolated asymptotically flat witness is sourced only by T_O. '
                'T_C is retained solely for the separate source-class NEC boundary.'
            ),
        },
        'package': package,
        'mass_ledger': {
            'w3_58_flat_proper_energy': 'fixed-coframe core energy',
            'w3_64_proper_energy': 'integral x^2 rho/sqrt(N) dx',
            'w3_64_misner_sharp_adm_mass': 'M(infinity)=integral x^2 rho dx',
            'w3_51_active_gauss_mass': 'not identified with the above',
            'operational_m_eff': 'readout quantity; not identified with the above',
        },
        'scope_flags': {
            'selected_core_einstein_backreaction_completed': aggregate_pass,
            'regular_horizonless_compact_object_witness_constructed': aggregate_pass,
            'physical_alpha_from_foundation_derived': False,
            'localized_core_coefficients_from_nodes_derived': False,
            'regular_trapped_black_hole_from_current_sources_derived': False,
            'singularity_resolution_completed': False,
            'rotation_completed': False,
            'collapse_evolution_completed': False,
            'backreacted_radial_stability_completed': False,
            'love_number_or_qnm_derived': False,
            'new_gravity_operator_introduced': False,
            'fitted_equation_of_state_introduced': False,
            'second_metric_introduced': False,
            'observational_likelihood_evaluated': False,
            'near_horizon_endpoint_derived': False,
            'fixed_alpha_equilibrium_branch_derived': False,
            'geodesic_completeness_derived': False,
        },
        'scientific_boundary': (
            'W3-64 closes the exact nonlinear Einstein-scalar backreaction system '
            'and constructs a converged, numerically curvature-finite, regular-centre, '
            'asymptotically Schwarzschild, horizonless continuation segment across '
            'the registered coupling grid. Both retained source sectors satisfy the '
            'null energy condition on their selected domains. Whenever a future '
            'configuration contains a closed trapped surface and satisfies the '
            'remaining Penrose hypotheses, future null-geodesic completeness is '
            'excluded. This fixes the boundary of the current source class; it is '
            'not a singularity-resolution, geodesic-completeness, near-horizon, '
            'fixed-alpha stability, or regular trapped-black-hole result.'
        ),
        'references': {
            'Penrose_1965': 'https://doi.org/10.1103/PhysRevLett.14.57',
            'Kaup_1968': 'https://doi.org/10.1103/PhysRev.172.1331',
            'Bekenstein_1972': 'https://doi.org/10.1103/PhysRevLett.28.452',
            'Coleman_1985': 'https://doi.org/10.1016/0550-3213(85)90286-X',
        },
        'provenance': {
            'created_utc': datetime.now(timezone.utc).isoformat(),
            'python': platform.python_version(),
            'platform': platform.platform(),
            'numpy': np.__version__,
            'scipy': scipy.__version__,
            'sympy': sp.__version__,
            'source_sha256': sha256(Path(__file__)),
            'preregistration_sha256': sha256(PREREG),
            'network_used_by_verifier': False,
            'archived_theory_used': False,
        },
    }
    result = native_tree(result)
    result['artifact_valid'] = bool(
        aggregate_pass and finite_tree(result)
    )
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print(status)
    print(json.dumps({
        'artifact_valid': result['artifact_valid'],
        'Omega': canonical_observables['Omega'],
        'ADM_mass': canonical_observables['misner_sharp_adm_mass_dimensionless'],
        'charge': canonical_observables['noether_charge_dimensionless'],
        'maximum_compactness': canonical_observables[
            'maximum_compactness_2alphaM_over_x'
        ],
        'minimum_N': canonical_observables['minimum_N'],
        'central_lapse': canonical_observables['central_lapse_sigma'],
        'convergence_maximum_relative_change': convergence[
            'maximum_relative_change'
        ],
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
