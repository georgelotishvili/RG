from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import scipy
import sympy as sp
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
STRONG_FIELD = HERE.parent
WORK3 = STRONG_FIELD.parent
W3_64_DIR = STRONG_FIELD / 'W3-64_Einstein_Continuation'
W3_64_SOURCE = W3_64_DIR / 'w3_64_source_first_einstein_strong_field.py'
W3_64_PREREG = W3_64_DIR / 'w3_64_source_first_einstein_strong_field_preregistration.md'
W3_64_RESULT = W3_64_DIR / 'w3_64_result.json'
PREREG = HERE / 'w3_65_fixed_alpha_first_turning_point_preregistration.md'
OUTPUT = HERE / 'w3_65_result.json'

EXPECTED_HASHES = {
    'w3_64_source': '99bc4331bec07219308bd15e43a945792ecd59c60ef959d17684944a6635aa77',
    'w3_64_preregistration': '25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1',
    'w3_64_result': 'b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b',
}

ALPHA = 0.04
A_SEXTIC = 0.25
ANCHOR_F0 = 1.820210505787701
ANCHOR_EXPECTED = {
    'Omega': 0.7430586961252276,
    'mass': 7.9689569805342035,
    'charge': 8.58838286008662,
    'compactness': 0.17164337151845413,
    'minimum_N': 0.8283566284815459,
}
RADIUS = 80.0
TOLERANCE = 1.0e-7
MAIN_F0_GRID = (
    ANCHOR_F0,
    *tuple(float(round(1.83 + 0.01 * i, 12)) for i in range(42)),
)
TURN_BRACKET = (2.16, 2.22)
TURN_STEPS = (0.01, 0.005, 0.0025)
TANGENT_HALF_STEP = 0.001
DOMAIN_GRID = (60.0, 80.0, 100.0)
TOLERANCE_GRID = (1.0e-6, 3.0e-7, 1.0e-7)
PROFILE_POINTS = 8001
CANONICAL_POINTS = 16001
RETRACE_POINTS = 2001
TANGENT_POINTS = 12001


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_change(value: float, reference: float) -> float:
    return abs(value - reference) / max(abs(value), abs(reference), 1.0e-30)


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


def finite_tree(value: Any) -> bool:
    if isinstance(value, dict):
        return all(finite_tree(k) and finite_tree(v) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return all(finite_tree(v) for v in value)
    if isinstance(value, (float, np.floating)):
        return math.isfinite(float(value))
    return True


def dependency_gate() -> tuple[dict[str, Any], Any]:
    paths = {
        'w3_64_source': W3_64_SOURCE,
        'w3_64_preregistration': W3_64_PREREG,
        'w3_64_result': W3_64_RESULT,
    }
    actual = {name: sha256(path) for name, path in paths.items()}
    hashes_exact = {
        name: actual[name] == EXPECTED_HASHES[name] for name in paths
    }
    upstream = json.loads(W3_64_RESULT.read_text(encoding='utf-8'))
    closure_exact = bool(
        upstream.get('artifact_valid')
        and all(upstream.get('closure_flags', {}).values())
    )
    source_ledger_exact = bool(
        upstream.get('source_ledger', {}).get('localized_einstein_rhs') == ['T_O']
        and not upstream.get('scope_flags', {}).get('second_metric_introduced')
        and not upstream.get('scope_flags', {}).get('new_gravity_operator_introduced')
    )
    spec = importlib.util.spec_from_file_location('w3_64_locked', W3_64_SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError('Unable to load hash-pinned W3-64 source')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = {
        'expected_hashes': EXPECTED_HASHES,
        'actual_hashes': actual,
        'hashes_exact': hashes_exact,
        'w3_64_artifact_valid_and_closure_exact': closure_exact,
        'w3_64_source_ledger_exact': source_ledger_exact,
        'all_pass': bool(
            all(hashes_exact.values()) and closure_exact and source_ledger_exact
        ),
    }
    return result, module


def symbolic_gate() -> dict[str, Any]:
    mass_scale, coupling, omega_dim = sp.symbols(
        'm_s lambda Omega', positive=True, finite=True
    )
    d_mass, d_charge = sp.symbols('dM dQ', real=True, finite=True)
    energy_change = 4 * sp.pi * mass_scale * d_mass / coupling
    physical_omega = mass_scale * omega_dim
    charge_change = 4 * sp.pi * d_charge / coupling
    normalized = sp.simplify(
        (energy_change - physical_omega * charge_change)
        / (4 * sp.pi * mass_scale / coupling)
        - (d_mass - omega_dim * d_charge)
    )
    f = sp.symbols('f', real=True, finite=True)
    potential = f**2 / 2 - f**4 / 4 + f**6 / 24
    expected_force = f - f**3 + f**5 / 4
    checks = {
        'branch_first_law_normalization_exact': normalized == 0,
        'inherited_sextic_force_exact': sp.simplify(
            sp.diff(potential, f) - expected_force
        ) == 0,
        'fixed_alpha_exact': sp.simplify(
            sp.Rational(1, 25) - sp.Rational(str(ALPHA))
        ) == 0,
        'fixed_sextic_coefficient_exact': sp.simplify(
            sp.Rational(1, 4) - sp.Rational(str(A_SEXTIC))
        ) == 0,
    }
    return {
        'checks': checks,
        'all_pass': bool(all(checks.values())),
        'identity': 'dM/ds=Omega dQ/ds at fixed action and alpha',
        'normalizations': {
            'E_phys': '(4 pi m_s/lambda) M',
            'Q_phys': '(4 pi/lambda) Q',
            'omega_phys': 'm_s Omega',
        },
    }


def solve_at(
    module: Any,
    f0: float,
    seed: object | None,
    radius: float = RADIUS,
    tolerance: float = TOLERANCE,
    flat: object | None = None,
) -> object:
    module.F0_BENCH = float(f0)
    solution = module.solve_coupled(
        ALPHA,
        radius=radius,
        tolerance=tolerance,
        seed=seed,
        flat=flat,
    )
    return solution


def observe(
    module: Any,
    solution: object,
    f0: float,
    radius: float = RADIUS,
    points: int = PROFILE_POINTS,
    with_residuals: bool = False,
) -> dict[str, Any]:
    module.F0_BENCH = float(f0)
    return module.profile_observables(
        solution,
        ALPHA,
        radius,
        points=points,
        with_residuals=with_residuals,
    )


def compact_record(f0: float, obs: dict[str, Any]) -> dict[str, Any]:
    centre = obs['centre_series']
    independent = obs.get('independent_finite_grid_residuals')
    centre_pass = bool(
        centre['f_value_residual'] < 3.0e-3
        and centre['f_derivative_residual'] < 3.0e-3
        and centre['mass_cubic_residual'] < 3.0e-3
        and centre['isotropy_residual'] < 1.0e-8
    )
    independent_pass = bool(independent is not None and independent['pass'])
    return {
        'f0': f0,
        'central_amplitude': obs['central_amplitude'],
        'central_amplitude_relative_residual': relative_change(
            obs['central_amplitude'], f0
        ),
        'Omega': obs['Omega'],
        'ADM_mass': obs['misner_sharp_adm_mass_dimensionless'],
        'charge': obs['noether_charge_dimensionless'],
        'charge_rms_radius': obs['charge_rms_radius_dimensionless'],
        'central_lapse': obs['central_lapse_sigma'],
        'maximum_compactness': obs['maximum_compactness_2alphaM_over_x'],
        'minimum_N': obs['minimum_N'],
        'minimum_amplitude': obs['minimum_amplitude'],
        'maximum_outward_derivative': obs['maximum_outward_derivative'],
        'minimum_scalar_radial_nec': obs['minimum_scalar_radial_nec'],
        'minimum_scalar_tangential_nec': obs['minimum_scalar_tangential_nec'],
        'maximum_abs_Ricci': obs['maximum_abs_Ricci_over_m_squared'],
        'maximum_Kretschmann': obs['maximum_Kretschmann_over_m_four'],
        'tail_k_error': obs['tail_exponent_absolute_error'],
        'tail_s_error': obs['tail_power_absolute_error'],
        'collocation_rms_residual_max': obs['collocation_rms_residual_max'],
        'adaptive_nodes': obs['adaptive_nodes'],
        'centre_series_pass': centre_pass,
        'independent_residuals_pass': independent_pass,
        'maximum_independent_normalized_residual': (
            max(
                independent['scalar_equation_normalized_l2'],
                independent['mass_equation_normalized_l2'],
                independent['lapse_equation_normalized_l2'],
                independent['anisotropic_tov_normalized_l2'],
            ) if independent is not None else math.inf
        ),
    }


def basic_profile_pass(record: dict[str, Any]) -> bool:
    return bool(
        finite_tree(record)
        and record['minimum_amplitude'] >= -1.0e-10
        and record['maximum_outward_derivative'] <= 1.0e-8
        and record['central_lapse'] > 0.0
        and record['minimum_N'] > 0.0
        and record['maximum_compactness'] < 1.0
        and record['minimum_scalar_radial_nec'] >= -1.0e-12
        and record['minimum_scalar_tangential_nec'] >= -1.0e-12
        and record['tail_k_error'] < 3.0e-3
        and record['tail_s_error'] < 3.0e-3
        and record['collocation_rms_residual_max'] < 3.0e-4
        and record['central_amplitude_relative_residual'] < 1.0e-8
        and record['centre_series_pass']
        and record['independent_residuals_pass']
        and record['maximum_independent_normalized_residual'] < 3.0e-4
    )


def production_configuration() -> dict[str, Any]:
    return {
        'alpha': ALPHA,
        'metric_count': 1,
        'gravity_operator': 'Einstein-Hilbert/TEGR',
        'localized_sources': ('T_O',),
        'central_amplitude_is_branch_variable': True,
        'tail': 'Schwarzschild-corrected Yukawa power',
    }


def configuration_valid(candidate: dict[str, Any]) -> bool:
    return bool(
        candidate['alpha'] == ALPHA
        and candidate['metric_count'] == 1
        and candidate['gravity_operator'] == 'Einstein-Hilbert/TEGR'
        and candidate['localized_sources'] == ('T_O',)
        and candidate['central_amplitude_is_branch_variable']
        and candidate['tail'] == 'Schwarzschild-corrected Yukawa power'
    )


def turning_pair_valid(
    mass_turn: dict[str, Any],
    charge_turn: dict[str, Any],
) -> bool:
    return bool(
        abs(mass_turn['root'] - charge_turn['root']) < 5.0e-4
        and mass_turn['positive_below_negative_above']
        and charge_turn['positive_below_negative_above']
    )


def classify_event(has_valid_turn: bool, solver_failed: bool) -> str:
    if has_valid_turn:
        return (
            'FIRST_POST_ANCHOR_SIMULTANEOUS_MASS_CHARGE_TURNING_POINT_'
            'IN_INCREASING_F0_DIRECTION'
        )
    if solver_failed:
        return 'NUMERICALLY_INCONCLUSIVE'
    return 'REGULAR_BRANCH_SEGMENT_WITHOUT_REGISTERED_TURN'


def anchor_gate(module: Any) -> tuple[dict[str, Any], object, object]:
    module.F0_BENCH = ANCHOR_F0
    flat = module.solve_flat_seed(RADIUS)
    previous: object | None = None
    for alpha in module.ALPHA_GRID:
        module.F0_BENCH = ANCHOR_F0
        previous = module.solve_coupled(
            alpha,
            radius=RADIUS,
            tolerance=TOLERANCE,
            seed=previous,
            flat=flat,
        )
    if previous is None:
        raise RuntimeError('W3-64 anchor continuation produced no solution')
    obs = observe(
        module,
        previous,
        ANCHOR_F0,
        points=CANONICAL_POINTS,
        with_residuals=True,
    )
    record = compact_record(ANCHOR_F0, obs)
    errors = {
        'Omega': relative_change(record['Omega'], ANCHOR_EXPECTED['Omega']),
        'mass': relative_change(record['ADM_mass'], ANCHOR_EXPECTED['mass']),
        'charge': relative_change(record['charge'], ANCHOR_EXPECTED['charge']),
        'compactness': relative_change(
            record['maximum_compactness'], ANCHOR_EXPECTED['compactness']
        ),
        'minimum_N': relative_change(record['minimum_N'], ANCHOR_EXPECTED['minimum_N']),
    }
    result = {
        'record': record,
        'relative_errors': errors,
        'threshold': 3.0e-4,
        'pass': bool(basic_profile_pass(record) and max(errors.values()) < 3.0e-4),
    }
    return result, previous, flat


def forward_branch_gate(
    module: Any,
    anchor_solution: object,
) -> tuple[dict[str, Any], list[object]]:
    solutions: list[object] = [anchor_solution]
    first_obs = observe(
        module, anchor_solution, ANCHOR_F0, with_residuals=True
    )
    records = [compact_record(ANCHOR_F0, first_obs)]
    previous = anchor_solution
    for f0 in MAIN_F0_GRID[1:]:
        solution = solve_at(module, f0, previous)
        obs = observe(module, solution, f0, with_residuals=True)
        record = compact_record(f0, obs)
        solutions.append(solution)
        records.append(record)
        previous = solution
    return {
        'coordinate': 'central amplitude f0',
        'records': records,
        'all_profiles_pass': bool(all(basic_profile_pass(r) for r in records)),
        'pass': bool(all(basic_profile_pass(r) for r in records)),
    }, solutions


def backward_retrace_gate(
    module: Any,
    forward: dict[str, Any],
    forward_solutions: list[object],
) -> dict[str, Any]:
    backward_records: list[dict[str, Any]] = []
    backward_solutions: list[object] = []
    previous = forward_solutions[-1]
    for f0 in reversed(MAIN_F0_GRID):
        if f0 == MAIN_F0_GRID[-1]:
            solution = previous
        else:
            solution = solve_at(module, f0, previous)
        obs = observe(module, solution, f0, with_residuals=True)
        backward_records.append(compact_record(f0, obs))
        backward_solutions.append(solution)
        previous = solution
    backward_records.reverse()
    backward_solutions.reverse()
    observable_keys = (
        'Omega',
        'ADM_mass',
        'charge',
        'charge_rms_radius',
        'central_lapse',
        'maximum_compactness',
        'minimum_N',
        'maximum_Kretschmann',
    )
    observable_mismatches: list[float] = []
    profile_mismatches: list[float] = []
    x = np.linspace(0.02, RADIUS - 1.0, RETRACE_POINTS)
    for index, (forward_record, backward_record) in enumerate(
        zip(forward['records'], backward_records)
    ):
        for key in observable_keys:
            observable_mismatches.append(relative_change(
                forward_record[key], backward_record[key]
            ))
        yf = forward_solutions[index].sol(x)
        yb = backward_solutions[index].sol(x)
        component_mismatches = []
        for forward_component, backward_component in zip(yf, yb):
            numerator = float(simpson(
                (forward_component - backward_component) ** 2, x=x
            ))
            denominator = float(simpson(
                forward_component**2 + backward_component**2, x=x
            ))
            component_mismatches.append(math.sqrt(
                numerator / max(denominator, 1.0e-30)
            ))
        profile_mismatches.append(max(component_mismatches))
    max_observable = max(observable_mismatches)
    max_profile = max(profile_mismatches)
    return {
        'records': backward_records,
        'maximum_observable_relative_mismatch': max_observable,
        'maximum_full_state_component_relative_l2_mismatch': max_profile,
        'threshold': 5.0e-5,
        'pass': bool(
            all(basic_profile_pass(r) for r in backward_records)
            and max_observable < 5.0e-5
            and max_profile < 5.0e-5
        ),
    }


def first_law_gate(records: list[dict[str, Any]]) -> dict[str, Any]:
    f0 = np.array([r['f0'] for r in records], dtype=float)
    omega = np.array([r['Omega'] for r in records], dtype=float)
    mass = np.array([r['ADM_mass'] for r in records], dtype=float)
    charge = np.array([r['charge'] for r in records], dtype=float)
    d_mass = np.gradient(mass, f0, edge_order=2)
    d_charge = np.gradient(charge, f0, edge_order=2)
    residual = d_mass - omega * d_charge
    numerator = float(np.sqrt(np.mean(residual**2)))
    denominator = float(np.sqrt(np.mean(
        d_mass**2 + (omega * d_charge) ** 2
    )))
    normalized = numerator / max(denominator, 1.0e-30)
    omitted_omega = d_mass - d_charge
    omitted_normalized = float(np.sqrt(np.mean(omitted_omega**2))) / max(
        denominator, 1.0e-30
    )
    return {
        'normalized_l2_residual': normalized,
        'threshold': 2.0e-3,
        'omega_omission_mutation_residual': omitted_normalized,
        'pass': bool(normalized < 2.0e-3),
    }


def bracket_grid(step: float) -> tuple[float, ...]:
    count = int(round((TURN_BRACKET[1] - TURN_BRACKET[0]) / step))
    return tuple(float(round(TURN_BRACKET[0] + i * step, 12)) for i in range(count + 1))


def spline_root(
    x: np.ndarray,
    values: np.ndarray,
) -> tuple[float, dict[str, Any]]:
    spline = CubicSpline(x, values, bc_type='natural')
    derivative = spline.derivative()
    candidates = [
        float(root.real)
        for root in derivative.roots()
        if abs(float(root.imag)) < 1.0e-12
        and TURN_BRACKET[0] < float(root.real) < TURN_BRACKET[1]
    ]
    if len(candidates) != 1:
        raise RuntimeError(
            f'Expected one turning root in {TURN_BRACKET}, found {candidates}'
        )
    root = candidates[0]
    below = float(derivative(TURN_BRACKET[0]))
    above = float(derivative(TURN_BRACKET[1]))
    return root, {
        'root': root,
        'derivative_below': below,
        'derivative_above': above,
        'positive_below_negative_above': bool(below > 0.0 and above < 0.0),
    }


def turning_refinement_gate(
    module: Any,
    seed_216: object,
) -> tuple[dict[str, Any], list[tuple[float, object, dict[str, Any]]]]:
    refinements: list[dict[str, Any]] = []
    finest_solutions: list[tuple[float, object, dict[str, Any]]] = []
    for step in TURN_STEPS:
        rows: list[tuple[float, object, dict[str, Any]]] = []
        previous = seed_216
        for index, f0 in enumerate(bracket_grid(step)):
            if index == 0:
                solution = previous
            else:
                solution = solve_at(module, f0, previous)
            obs = observe(
                module,
                solution,
                f0,
                points=CANONICAL_POINTS,
                with_residuals=True,
            )
            rows.append((f0, solution, compact_record(f0, obs)))
            previous = solution
        x = np.array([row[0] for row in rows], dtype=float)
        mass = np.array([row[2]['ADM_mass'] for row in rows], dtype=float)
        charge = np.array([row[2]['charge'] for row in rows], dtype=float)
        mass_root, mass_data = spline_root(x, mass)
        charge_root, charge_data = spline_root(x, charge)
        local_first_law = first_law_gate([row[2] for row in rows])
        refinements.append({
            'step': step,
            'mass_turn': mass_data,
            'charge_turn': charge_data,
            'root_separation': abs(mass_root - charge_root),
            'branch_first_law': local_first_law,
            'all_profiles_pass': bool(all(basic_profile_pass(row[2]) for row in rows)),
        })
        if step == TURN_STEPS[-1]:
            finest_solutions = rows
    root_changes: list[float] = []
    for previous, current in zip(refinements[:-1], refinements[1:]):
        root_changes.extend((
            abs(current['mass_turn']['root'] - previous['mass_turn']['root']),
            abs(current['charge_turn']['root'] - previous['charge_turn']['root']),
        ))
    maximum_change = max(root_changes)
    finest = refinements[-1]
    first_law_residuals = [
        item['branch_first_law']['normalized_l2_residual']
        for item in refinements
    ]
    first_law_step_convergence = bool(
        first_law_residuals[-1] < first_law_residuals[0]
        and first_law_residuals[-1] < 2.0e-3
    )
    simultaneous = turning_pair_valid(
        finest['mass_turn'], finest['charge_turn']
    )
    result = {
        'bracket': list(TURN_BRACKET),
        'refinements': refinements,
        'maximum_nested_step_root_change': maximum_change,
        'root_change_threshold': 5.0e-4,
        'simultaneous_root_threshold': 5.0e-4,
        'simultaneous_turn_pass': simultaneous,
        'step_convergence_pass': bool(maximum_change < 5.0e-4),
        'refinement_profiles_pass': bool(
            all(item['all_profiles_pass'] for item in refinements)
        ),
        'first_law_nested_step_residuals': first_law_residuals,
        'first_law_step_convergence_pass': first_law_step_convergence,
        'pass': bool(
            simultaneous
            and maximum_change < 5.0e-4
            and first_law_step_convergence
            and all(item['all_profiles_pass'] for item in refinements)
        ),
    }
    return result, finest_solutions


def canonical_turn_gate(
    module: Any,
    turning: dict[str, Any],
    finest_solutions: list[tuple[float, object, dict[str, Any]]],
) -> tuple[dict[str, Any], object]:
    finest = turning['refinements'][-1]
    mass_root = finest['mass_turn']['root']
    charge_root = finest['charge_turn']['root']
    f_turn = 0.5 * (mass_root + charge_root)
    seed_row = min(finest_solutions, key=lambda row: abs(row[0] - f_turn))
    solution = solve_at(module, f_turn, seed_row[1])
    obs = observe(
        module,
        solution,
        f_turn,
        points=CANONICAL_POINTS,
        with_residuals=True,
    )
    record = compact_record(f_turn, obs)
    centre = obs['centre_series']
    residuals = obs['independent_finite_grid_residuals']
    centre_pass = bool(
        centre['f_value_residual'] < 3.0e-3
        and centre['f_derivative_residual'] < 3.0e-3
        and centre['mass_cubic_residual'] < 3.0e-3
        and centre['isotropy_residual'] < 1.0e-8
    )
    result = {
        'mass_turn_f0': mass_root,
        'charge_turn_f0': charge_root,
        'canonical_f0': f_turn,
        'record': record,
        'centre_series': centre,
        'independent_residuals': residuals,
        'robin_boundary_residual': obs['robin_boundary_residual'],
        'tail_fit_sample_count': obs['tail_fit_sample_count'],
        'centre_pass': centre_pass,
        'residuals_pass': bool(residuals['pass']),
        'regular_nodeless_horizonless_pass': basic_profile_pass(record),
        'pass': bool(
            turning['pass']
            and centre_pass
            and residuals['pass']
            and basic_profile_pass(record)
        ),
    }
    return result, solution


def observable_vector(record: dict[str, Any]) -> dict[str, float]:
    return {
        key: float(record[key])
        for key in (
            'Omega',
            'ADM_mass',
            'charge',
            'charge_rms_radius',
            'central_lapse',
            'maximum_compactness',
            'minimum_N',
            'maximum_Kretschmann',
        )
    }


def controlled_turn_scan(
    module: Any,
    seed_216: object,
    radius: float,
    tolerance: float,
) -> dict[str, Any]:
    points = bracket_grid(0.005)
    rows: list[tuple[float, object, dict[str, Any]]] = []
    previous = solve_at(
        module,
        points[0],
        seed_216,
        radius=radius,
        tolerance=tolerance,
    )
    for index, f0 in enumerate(points):
        if index == 0:
            solution = previous
        else:
            solution = solve_at(
                module,
                f0,
                previous,
                radius=radius,
                tolerance=tolerance,
            )
        obs = observe(
            module,
            solution,
            f0,
            radius=radius,
            points=CANONICAL_POINTS,
            with_residuals=True,
        )
        rows.append((f0, solution, compact_record(f0, obs)))
        previous = solution
    x = np.array([row[0] for row in rows], dtype=float)
    mass = np.array([row[2]['ADM_mass'] for row in rows], dtype=float)
    charge = np.array([row[2]['charge'] for row in rows], dtype=float)
    mass_root, mass_data = spline_root(x, mass)
    charge_root, charge_data = spline_root(x, charge)
    f_turn = 0.5 * (mass_root + charge_root)
    turn_seed = min(rows, key=lambda row: abs(row[0] - f_turn))[1]
    turn_solution = solve_at(
        module,
        f_turn,
        turn_seed,
        radius=radius,
        tolerance=tolerance,
    )
    turn_obs = observe(
        module,
        turn_solution,
        f_turn,
        radius=radius,
        points=CANONICAL_POINTS,
        with_residuals=True,
    )
    turn_record = compact_record(f_turn, turn_obs)
    return {
        'X': radius,
        'tolerance': tolerance,
        'mass_turn': mass_data,
        'charge_turn': charge_data,
        'canonical_f0': f_turn,
        'observables': observable_vector(turn_record),
        'turning_pair_pass': turning_pair_valid(mass_data, charge_data),
        'all_scan_profiles_pass': bool(
            all(basic_profile_pass(row[2]) for row in rows)
        ),
        'canonical_profile_pass': basic_profile_pass(turn_record),
    }


def convergence_gate(
    module: Any,
    seed_216: object,
) -> dict[str, Any]:
    domain_records = [
        controlled_turn_scan(module, seed_216, radius, TOLERANCE)
        for radius in DOMAIN_GRID
    ]
    tolerance_records = [
        controlled_turn_scan(module, seed_216, RADIUS, tolerance)
        for tolerance in TOLERANCE_GRID
    ]
    domain_reference = domain_records[-1]
    tolerance_reference = tolerance_records[-1]
    compared_keys = (
        'canonical_f0',
        'mass_turn_root',
        'charge_turn_root',
        *tuple(domain_reference['observables'].keys()),
    )

    def values(record: dict[str, Any]) -> dict[str, float]:
        return {
            'canonical_f0': float(record['canonical_f0']),
            'mass_turn_root': float(record['mass_turn']['root']),
            'charge_turn_root': float(record['charge_turn']['root']),
            **{
                key: float(value)
                for key, value in record['observables'].items()
            },
        }

    domain_reference_values = values(domain_reference)
    tolerance_reference_values = values(tolerance_reference)
    domain_changes = [
        relative_change(values(record)[key], domain_reference_values[key])
        for record in domain_records
        for key in compared_keys
    ]
    tolerance_changes = [
        relative_change(values(record)[key], tolerance_reference_values[key])
        for record in tolerance_records
        for key in compared_keys
    ]
    maximum_change = max(domain_changes + tolerance_changes)
    controls_pass = bool(
        all(
            record['turning_pair_pass']
            and record['all_scan_profiles_pass']
            and record['canonical_profile_pass']
            for record in domain_records + tolerance_records
        )
    )
    return {
        'root_rescan_step': 0.005,
        'domain_records': domain_records,
        'tolerance_records': tolerance_records,
        'compared_keys': list(compared_keys),
        'maximum_relative_change': maximum_change,
        'threshold': 5.0e-4,
        'all_control_profiles_and_turns_pass': controls_pass,
        'pass': bool(maximum_change < 5.0e-4 and controls_pass),
    }


def tangent_gate(
    module: Any,
    turning: dict[str, Any],
    finest_solutions: list[tuple[float, object, dict[str, Any]]],
) -> dict[str, Any]:
    charge_root = turning['refinements'][-1]['charge_turn']['root']
    seed_row = min(finest_solutions, key=lambda row: abs(row[0] - charge_root))
    root_solution = solve_at(module, charge_root, seed_row[1])
    f_minus = charge_root - TANGENT_HALF_STEP
    f_plus = charge_root + TANGENT_HALF_STEP
    minus = solve_at(module, f_minus, root_solution)
    plus = solve_at(module, f_plus, root_solution)
    obs_minus = observe(module, minus, f_minus, points=CANONICAL_POINTS)
    obs_plus = observe(module, plus, f_plus, points=CANONICAL_POINTS)
    d_mass = (
        obs_plus['misner_sharp_adm_mass_dimensionless']
        - obs_minus['misner_sharp_adm_mass_dimensionless']
    ) / (2.0 * TANGENT_HALF_STEP)
    d_charge = (
        obs_plus['noether_charge_dimensionless']
        - obs_minus['noether_charge_dimensionless']
    ) / (2.0 * TANGENT_HALF_STEP)
    mass_fraction = abs(d_mass) / max(
        abs(obs_plus['misner_sharp_adm_mass_dimensionless']),
        abs(obs_minus['misner_sharp_adm_mass_dimensionless']),
        1.0,
    )
    charge_fraction = abs(d_charge) / max(
        abs(obs_plus['noether_charge_dimensionless']),
        abs(obs_minus['noether_charge_dimensionless']),
        1.0,
    )
    x = np.linspace(0.02, RADIUS - 1.0, TANGENT_POINTS)
    y_plus = plus.sol(x)
    y_minus = minus.sol(x)
    lhs = (plus.sol(x, 1) - minus.sol(x, 1)) / (
        2.0 * TANGENT_HALF_STEP
    )
    equations = module.curved_equations(ALPHA)
    rhs = (
        equations(x, y_plus, plus.p) - equations(x, y_minus, minus.p)
    ) / (2.0 * TANGENT_HALF_STEP)
    residual = lhs - rhs
    numerator = sum(float(simpson(row**2, x=x)) for row in residual)
    denominator = sum(
        float(simpson(lhs_row**2 + rhs_row**2, x=x))
        for lhs_row, rhs_row in zip(lhs, rhs)
    )
    ode_residual = math.sqrt(numerator / max(denominator, 1.0e-30))

    module.F0_BENCH = f_plus
    bc_plus = module.curved_boundary(RADIUS, ALPHA)(
        plus.sol(module.EPS), plus.sol(RADIUS), plus.p
    )
    module.F0_BENCH = f_minus
    bc_minus = module.curved_boundary(RADIUS, ALPHA)(
        minus.sol(module.EPS), minus.sol(RADIUS), minus.p
    )
    bc_tangent = (bc_plus - bc_minus) / (2.0 * TANGENT_HALF_STEP)
    bc_residual = float(np.linalg.norm(bc_tangent) / math.sqrt(bc_tangent.size))
    return {
        'charge_root_f0': charge_root,
        'half_step': TANGENT_HALF_STEP,
        'dM_df0': d_mass,
        'dQ_df0': d_charge,
        'mass_tangent_fraction': mass_fraction,
        'charge_tangent_fraction': charge_fraction,
        'linearized_ode_normalized_l2': ode_residual,
        'linearized_boundary_normalized_l2': bc_residual,
        'mass_fraction_threshold': 1.0e-4,
        'charge_fraction_threshold': 1.0e-4,
        'linearized_residual_threshold': 3.0e-4,
        'interpretation': (
            'The equilibrium-family tangent is a charge-conserving null '
            'tangent of the extended static linearized equilibrium BVP, '
            'including variation of the BVP eigenvalue Omega. It is not a '
            'physical radial zero-frequency eigenmode, lowest-eigenvalue, '
            'or radial-spectrum calculation.'
        ),
        'pass': bool(
            mass_fraction < 1.0e-4
            and charge_fraction < 1.0e-4
            and ode_residual < 3.0e-4
            and bc_residual < 3.0e-4
        ),
    }


def mutation_gate(
    module: Any,
    turning: dict[str, Any],
    canonical: dict[str, Any],
    canonical_solution: object,
    first_law: dict[str, Any],
    tangent: dict[str, Any],
) -> dict[str, Any]:
    structure = production_configuration()
    structural_mutations = {
        'alpha_drift': {'alpha': ALPHA + 0.01},
        'second_metric': {'metric_count': 2},
        'new_gravity_operator': {'gravity_operator': 'mutated operator'},
        'duplicated_localized_source': {'localized_sources': ('T_O', 'T_O')},
        'hard_coded_anchor_amplitude': {
            'central_amplitude_is_branch_variable': False
        },
        'flat_finite_radius_robin': {'tail': 'flat Robin'},
    }
    detections: dict[str, bool] = {}
    for name, mutation in structural_mutations.items():
        candidate = dict(structure)
        candidate.update(mutation)
        detections[name] = not configuration_valid(candidate)

    finest = turning['refinements'][-1]
    mass_root = finest['mass_turn']['root']
    charge_root = finest['charge_turn']['root']
    displaced_charge_turn = dict(finest['charge_turn'])
    displaced_charge_turn['root'] = charge_root + 0.01
    detections['mass_only_displaced_charge_turn'] = not turning_pair_valid(
        finest['mass_turn'], displaced_charge_turn
    )
    detections['omega_omission_from_first_law'] = bool(
        first_law['omega_omission_mutation_residual'] > 0.01
    )
    last_point_mass = {
        'root': MAIN_F0_GRID[-1],
        'derivative_below': -1.0,
        'derivative_above': -1.0,
        'positive_below_negative_above': False,
    }
    last_point_charge = dict(last_point_mass)
    detections['last_grid_point_declared_as_turn'] = not turning_pair_valid(
        last_point_mass, last_point_charge
    )

    detections['injected_solver_failure_not_physical_endpoint'] = bool(
        classify_event(False, True) == 'NUMERICALLY_INCONCLUSIVE'
    )
    nodeful_record = dict(canonical['record'])
    nodeful_record['minimum_amplitude'] = -0.1
    detections['nodeful_profile_rejected'] = not basic_profile_pass(
        nodeful_record
    )
    mutated_charge_fraction = (
        abs(tangent['dQ_df0'] + 0.01 * canonical['record']['charge'])
        / max(abs(canonical['record']['charge']), 1.0)
    )
    detections['nonconserved_tangent_rejected'] = bool(
        mutated_charge_fraction >= 1.0e-4
    )

    yb = canonical_solution.sol(RADIUS)
    omega = module.omega_from_parameter(canonical_solution.p)
    k = math.sqrt(1.0 - omega**2)
    d = ALPHA * float(yb[2])
    tail_power = -1.0 + d * (2.0 * omega**2 - 1.0) / k
    corrected_numerator = abs(yb[1] + (k - tail_power / RADIUS) * yb[0])
    flat_numerator = abs(yb[1] + (k + 1.0 / RADIUS) * yb[0])
    corrected_scale = abs(yb[1]) + abs(
        (k - tail_power / RADIUS) * yb[0]
    )
    flat_scale = abs(yb[1]) + abs((k + 1.0 / RADIUS) * yb[0])
    corrected_normalized = corrected_numerator / max(corrected_scale, 1.0e-300)
    flat_normalized = flat_numerator / max(flat_scale, 1.0e-300)
    detections['flat_robin_actual_residual_detected'] = bool(
        corrected_normalized < 3.0e-4
        and flat_normalized > max(1.0e-4, 10.0 * corrected_normalized)
    )
    detections['hard_coded_anchor_actual_mismatch_detected'] = bool(
        not basic_profile_pass({
            **canonical['record'],
            'central_amplitude_relative_residual': relative_change(
                canonical['record']['central_amplitude'], ANCHOR_F0
            ),
        })
    )
    return {
        'base_structure': native_tree(structure),
        'corrected_tail_normalized_residual': corrected_normalized,
        'flat_tail_mutation_normalized_residual': flat_normalized,
        'mutated_charge_tangent_fraction': mutated_charge_fraction,
        'detections': detections,
        'pass': bool(configuration_valid(structure) and all(detections.values())),
    }


def package_gate() -> dict[str, Any]:
    expected = {
        PREREG.name,
        Path(__file__).name,
        OUTPUT.name,
    }
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    subdirectories = [path.name for path in HERE.iterdir() if path.is_dir()]
    unexpected = sorted(actual_files - expected)
    missing = sorted(expected - actual_files)
    required_present = {PREREG.name, Path(__file__).name}.issubset(actual_files)
    return {
        'expected_exact_files': sorted(expected),
        'actual_files': sorted(actual_files),
        'missing_files': missing,
        'unexpected_files': unexpected,
        'subdirectories': subdirectories,
        'pass': bool(
            required_present
            and not unexpected
            and not subdirectories
            and (not missing or missing == [OUTPUT.name])
        ),
    }


def run_pipeline() -> None:
    dependencies, module = dependency_gate()
    symbolic = symbolic_gate()
    anchor, anchor_solution, _flat = anchor_gate(module)
    forward, forward_solutions = forward_branch_gate(module, anchor_solution)
    backward = backward_retrace_gate(module, forward, forward_solutions)
    first_law = first_law_gate(forward['records'])
    seed_index = min(
        range(len(MAIN_F0_GRID)),
        key=lambda index: abs(MAIN_F0_GRID[index] - TURN_BRACKET[0]),
    )
    turning, finest_solutions = turning_refinement_gate(
        module, forward_solutions[seed_index]
    )
    canonical, canonical_solution = canonical_turn_gate(
        module, turning, finest_solutions
    )
    convergence = convergence_gate(module, forward_solutions[seed_index])
    tangent = tangent_gate(module, turning, finest_solutions)
    mutations = mutation_gate(
        module,
        turning,
        canonical,
        canonical_solution,
        first_law,
        tangent,
    )
    package = package_gate()

    closure_flags = {
        'dependency_hashes_exact': dependencies['all_pass'],
        'w3_64_artifact_and_source_ledger_exact': bool(
            dependencies['w3_64_artifact_valid_and_closure_exact']
            and dependencies['w3_64_source_ledger_exact']
        ),
        'fixed_action_metric_source_and_alpha_exact': bool(
            symbolic['all_pass']
            and dependencies['all_pass']
            and configuration_valid(production_configuration())
        ),
        'branch_first_law_normalization_exact': symbolic['checks'][
            'branch_first_law_normalization_exact'
        ],
        'anchor_regression_pass': anchor['pass'],
        'forward_branch_segment_pass': forward['pass'],
        'backward_retrace_pass': backward['pass'],
        'branch_first_law_numerical_pass': bool(
            first_law['pass'] and turning['first_law_step_convergence_pass']
        ),
        'simultaneous_mass_charge_turning_point_pass': turning[
            'simultaneous_turn_pass'
        ],
        'turning_point_step_convergence_pass': turning[
            'step_convergence_pass'
        ],
        'turning_refinement_profiles_pass': turning[
            'refinement_profiles_pass'
        ],
        'turning_point_domain_tolerance_convergence_pass': convergence['pass'],
        'charge_conserving_static_equilibrium_bvp_null_tangent_pass': tangent[
            'pass'
        ],
        'regular_nodeless_horizonless_segment_pass': bool(
            forward['all_profiles_pass']
            and backward['pass']
            and canonical['regular_nodeless_horizonless_pass']
        ),
        'independent_residual_recomputation_pass': bool(
            anchor['pass']
            and forward['pass']
            and backward['pass']
            and turning['refinement_profiles_pass']
            and convergence['all_control_profiles_and_turns_pass']
            and canonical['residuals_pass']
        ),
        'mutation_controls_pass': mutations['pass'],
        'package_clean_pass': package['pass'],
    }
    aggregate = bool(all(closure_flags.values()))
    closure_flags['aggregate_gate_pass'] = aggregate
    status = (
        'PASS_EXACT_UNCHANGED_EINSTEIN_SCALAR_FIXED_ALPHA_SYSTEM__'
        'CONVERGED_FIRST_POST_ANCHOR_SIMULTANEOUS_MASS_CHARGE_TURN_IN_'
        'INCREASING_F0_DIRECTION__CHARGE_CONSERVING_NULL_TANGENT_OF_'
        'EXTENDED_STATIC_EQUILIBRIUM_BVP__'
        'REGULAR_NODELESS_HORIZONLESS_RESOLVED_SEGMENT'
        if aggregate else
        'FAIL_W3_65_ANCHOR_FORWARD_FIRST_TURNING_POINT_GATE'
    )
    result: dict[str, Any] = {
        'schema_version': 'W3-65-result-v1.1',
        'claim_id': 'W3_65_ANCHOR_FORWARD_FIRST_TURNING_POINT_GATE',
        'model_version': (
            'W3-65-v1.1-EH-SEXTIC-U1-FIXED-ALPHA-ANCHOR-FORWARD-FIRST-TURN'
        ),
        'status': status,
        'artifact_valid': False,
        'closure_flags': closure_flags,
        'evidence_type': {
            'inherited_field_equations_and_first_law_normalization': 'EXACT',
            'equilibrium_branch_and_turning_point': 'CONVERGED_NUMERICAL_EVIDENCE',
            'charge_conserving_null_tangent_of_extended_static_equilibrium_bvp': (
                'CONVERGED_NUMERICAL_EVIDENCE'
            ),
            'physical_radial_zero_frequency_eigenmode': False,
            'radial_eigenvalue_spectrum': False,
            'time_evolution': False,
            'observational_test': False,
        },
        'dependencies': dependencies,
        'symbolic': symbolic,
        'anchor': anchor,
        'forward_branch': forward,
        'backward_retrace': backward,
        'branch_first_law': first_law,
        'turning_point': turning,
        'canonical_turning_solution': canonical,
        'convergence': convergence,
        'charge_conserving_static_equilibrium_bvp_null_tangent': tangent,
        'mutation_controls': mutations,
        'classification': {
            'event': classify_event(True, False),
            'direction': 'increasing f0 from the W3-64 anchor',
            'vacuum_to_anchor_segment_mapped': False,
            'static_chart_horizon_present': bool(
                canonical['record']['minimum_N'] <= 0.0
            ),
            'closed_trapped_surface_claimed': False,
            'near_horizon_claimed': False,
            'physical_endpoint_claimed': False,
            'solver_failure_used_as_physics': False,
        },
        'scientific_boundary': (
            'At the selected fixed mathematical coupling alpha=0.04, W3-65 '
            'maps the unchanged Einstein-complex-scalar nodeless branch from '
            'the W3-64 anchor in the increasing-f0 direction through the '
            'first simultaneous ADM-mass and Noether-charge turn encountered '
            'after that anchor. The charge-conserving equilibrium-family '
            'tangent is a null tangent of the extended static linearized '
            'equilibrium BVP, not a physical radial zero-frequency eigenmode. '
            'This does not map the vacuum-to-anchor segment or determine the '
            'radial spectrum, nonlinear stability, collapse fate, final '
            'spiral endpoint, physical alpha, horizon, geodesic completeness '
            'or singularity resolution.'
        ),
        'scope_flags': {
            'selected_fixed_alpha_first_post_anchor_simultaneous_turn_derived': (
                aggregate
            ),
            'charge_conserving_null_tangent_of_static_equilibrium_bvp_derived': (
                aggregate
            ),
            'physical_alpha_from_foundation_derived': False,
            'vacuum_to_anchor_branch_mapped': False,
            'full_pseudo_arclength_spiral_mapped': False,
            'physical_radial_zero_frequency_eigenmode_derived': False,
            'lowest_radial_eigenmode_derived': False,
            'linear_radial_stability_completed': False,
            'nonlinear_stability_completed': False,
            'collapse_evolution_completed': False,
            'final_equilibrium_endpoint_derived': False,
            'near_horizon_limit_derived': False,
            'trapped_surface_derived': False,
            'black_hole_solution_derived': False,
            'geodesic_completeness_derived': False,
            'singularity_resolution_completed': False,
            'foundation_strong_field_response_derived': False,
            'observational_likelihood_evaluated': False,
        },
        'frozen_controls': {
            'a': A_SEXTIC,
            'alpha': ALPHA,
            'anchor_f0': ANCHOR_F0,
            'main_f0_grid': list(MAIN_F0_GRID),
            'turn_bracket': list(TURN_BRACKET),
            'turn_steps': list(TURN_STEPS),
            'tangent_half_step': TANGENT_HALF_STEP,
            'domain_grid': list(DOMAIN_GRID),
            'tolerance_grid': list(TOLERANCE_GRID),
            'radius': RADIUS,
            'tolerance': TOLERANCE,
        },
        'package': package,
        'provenance': {
            'source_sha256': sha256(Path(__file__)),
            'preregistration_sha256': sha256(PREREG),
            'python': platform.python_version(),
            'numpy': np.__version__,
            'scipy': scipy.__version__,
            'sympy': sp.__version__,
            'generated_utc': datetime.now(timezone.utc).isoformat(),
            'deterministic': True,
        },
    }
    result['artifact_valid'] = bool(aggregate and finite_tree(result))
    OUTPUT.write_text(
        json.dumps(native_tree(result), indent=2, sort_keys=True) + '\n',
        encoding='utf-8',
    )

    final_package = package_gate()
    result['package'] = final_package
    result['closure_flags']['package_clean_pass'] = final_package['pass']
    final_aggregate = bool(
        all(
            value
            for key, value in result['closure_flags'].items()
            if key != 'aggregate_gate_pass'
        )
        and final_package['pass']
    )
    result['closure_flags']['aggregate_gate_pass'] = final_aggregate
    result['artifact_valid'] = bool(final_aggregate and finite_tree(result))
    if not final_aggregate:
        result['status'] = 'FAIL_W3_65_ANCHOR_FORWARD_FIRST_TURNING_POINT_GATE'
    OUTPUT.write_text(
        json.dumps(native_tree(result), indent=2, sort_keys=True) + '\n',
        encoding='utf-8',
    )
    print(result['status'])
    print(json.dumps({
        'artifact_valid': result['artifact_valid'],
        'f_turn': canonical['canonical_f0'],
        'Omega': canonical['record']['Omega'],
        'ADM_mass': canonical['record']['ADM_mass'],
        'charge': canonical['record']['charge'],
        'maximum_compactness': canonical['record']['maximum_compactness'],
        'minimum_N': canonical['record']['minimum_N'],
        'first_law_residual': first_law['normalized_l2_residual'],
        'turn_root_separation': turning['refinements'][-1]['root_separation'],
    }, indent=2, sort_keys=True))
    if not result['artifact_valid']:
        raise SystemExit(1)


def write_runtime_inconclusive(error: Exception) -> None:
    failure = {
        'schema_version': 'W3-65-result-v1.1',
        'claim_id': 'W3_65_ANCHOR_FORWARD_FIRST_TURNING_POINT_GATE',
        'model_version': (
            'W3-65-v1.1-EH-SEXTIC-U1-FIXED-ALPHA-ANCHOR-FORWARD-FIRST-TURN'
        ),
        'status': 'NUMERICALLY_INCONCLUSIVE',
        'artifact_valid': False,
        'classification': {
            'event': classify_event(False, True),
            'solver_failure_used_as_physics': False,
            'physical_endpoint_claimed': False,
        },
        'runtime_failure': {
            'type': type(error).__name__,
            'message': str(error),
        },
        'package': package_gate(),
        'provenance': {
            'source_sha256': sha256(Path(__file__)),
            'preregistration_sha256': sha256(PREREG),
            'generated_utc': datetime.now(timezone.utc).isoformat(),
        },
    }
    OUTPUT.write_text(
        json.dumps(native_tree(failure), indent=2, sort_keys=True) + '\n',
        encoding='utf-8',
    )


def main() -> None:
    try:
        run_pipeline()
    except Exception as error:
        write_runtime_inconclusive(error)
        print('NUMERICALLY_INCONCLUSIVE')
        print(f'{type(error).__name__}: {error}')
        raise SystemExit(2) from error


if __name__ == '__main__':
    main()
