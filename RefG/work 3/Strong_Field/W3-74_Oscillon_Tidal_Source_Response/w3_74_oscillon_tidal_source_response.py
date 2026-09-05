'''W3-74: action-derived static test-core tidal response; no pressure EOS added.'''

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import platform
import sys
from pathlib import Path

sys.dontwritebytecode = True

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import simpson, solve_bvp
from scipy.interpolate import CubicSpline
from scipy.linalg import eigh_tridiagonal, solve_banded
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
WORK3 = HERE.parents[1]
ROOT = WORK3.parents[1]
PREREG = HERE / 'w3_74_oscillon_tidal_source_response_preregistration.md'
OUTPUT = HERE / 'w3_74_result.json'
VERSION = 'W3-74-v1.0-FIXED-CHARGE-TEST-CORE-STATIC-TIDE'
PREREG_HASH = '3c102542ee6e7b28da8cff90e676ae8eb6f05a0b7308d51139b4422b100e22d3'
CORE = 'Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/'
PINS = {
    CORE + 'w3_58_one_oscillon_coframe_localized_core.py':
        'b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57',
    CORE + 'w3_58_one_oscillon_coframe_localized_core_preregistration.md':
        'ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db',
    CORE + 'w3_58_result.json':
        'cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5',
    'Strong_Field/W3-73_Coupled_Horizon_Regular_Einstein_Complex_Scalar/'
    'w3_73_coupled_horizon_regular_einstein_complex_scalar_preregistration.md':
        '8a3c3887fc0a28edc8fced67da0bc66ccaff39ade1f6e5b7e339f579fc02c49e',
}
PROTECTED = {
    'CODES.md': '27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41',
    'intuitive/RefG_GE.md': '433d3ac96ff6d91eaae1da60cd3f27f84ead2b7bddea26885034e2995dd8787f',
    'intuitive/Dictionary.txt': 'f6e12b67f38e49bb547d37e6c92375a2ee5b2f596ed481a866cbc490be32ed0b',
}
A, OMEGA, X_CANON = 0.25, 0.8, 80.0
ANGULAR = 4.0 * math.pi / 5.0
TRUE_KEYS = (
    'dependencies_pinned', 'linear_action_and_source_exact',
    'fixed_charge_selection_exact', 'proper_length_map_exact',
    'response_converged_numerical', 'quadrupole_hessian_positive_numerical',
    'independent_crosscheck_pass', 'mutation_controls_pass',
)
OPEN_KEYS = (
    'foundation_pressure_feedback_derived',
    'uniform_mass_radius_tail_scaling_derived',
    'full_self_gravitating_tidal_love_number', 'nonlinear_collapse_solved',
    'singularity_resolution_proved', 'observational_pass',
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(value, reference, floor=1e-30):
    return abs(value - reference) / max(abs(reference), floor)


def native(value):
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key:native(item) for key,item in value.items()}
    if isinstance(value, (tuple,list)):
        return [native(item) for item in value]
    return value


def dependencies():
    records = {name: {'actual': sha(WORK3 / name), 'expected': expected}
               for name, expected in PINS.items()}
    records['preregistration'] = {'actual': sha(PREREG), 'expected': PREREG_HASH}
    records.update({name: {'actual': sha(ROOT / name), 'expected': expected}
                    for name, expected in PROTECTED.items()})
    for item in records.values():
        item['pass'] = item['actual'] == item['expected']
    core_result = json.loads((WORK3 / (CORE + 'w3_58_result.json')).read_text('utf-8'))
    core_flags = core_result['closure_flags']
    inherited = {key: core_flags.get(key, False) for key in (
        'aggregate_gate_pass', 'finite_energy_ground_state_constructed_numerical',
        'hessian_operators_exact', 'negative_charge_slope_numerical',
        'hilbert_stress_from_same_action_exact',
    )}
    return {'records': records, 'inherited_flags': inherited,
            'pass': all(item['pass'] for item in records.values()) and all(inherited.values())}


def symbolic():
    phi, f, fp, a, om = sp.symbols('phi f fp a om', real=True)
    x = sp.symbols('x', positive=True)
    q = sp.symbols('q', real=True)
    h = sp.Function('h')(x)
    u = sp.Function('U')(x)
    p2 = (3*q**2-1)/2
    v = f**2/2-f**4/4+a*f**6/6
    w = 2*om**2*f**2-2*v
    s = 2*x**2*(sp.diff(v, f)-2*om**2*f)
    gradient = sp.sqrt((1+2*phi)*(1-2*phi))
    volume = sp.sqrt((1+2*phi)*(1-2*phi)**3)
    clock_volume = sp.sqrt((1-2*phi)**3/(1+2*phi))
    rho = (om**2*f**2+fp**2)/2+v
    pr = (om**2*f**2+fp**2)/2-v
    pt = (om**2*f**2-fp**2)/2-v
    h2 = -sp.diff(h,x,2)-2*sp.diff(h,x)/x+6*h/x**2+u*h
    z = sp.Function('z')(x)
    y = sp.Function('y')(x)
    eqs = {
        'gradient_metric_coefficient': sp.diff(gradient,phi).subs(phi,0),
        'potential_metric_coefficient': sp.diff(volume,phi).subs(phi,0)+2,
        'clock_metric_coefficient': sp.diff(clock_volume,phi).subs(phi,0)+4,
        'inherited_positive_charge_sign': -f**2*(-om)-om*f**2,
        'action_equals_hilbert_source': rho+pr+2*pt-w,
        'forcing_is_negative_source_variation': s+x**2*sp.diff(w,f),
        'hessian_from_same_potential': sp.diff(v,f,2)-om**2-(1-om**2-3*f**2+5*a*f**4),
        'quadrupole_angular_eigenvalue': sp.diff((1-q**2)*sp.diff(p2,q),q)+6*p2,
        'zero_charge_and_monopole': sp.integrate(p2,(q,-1,1)),
        'quadrupole_norm': 2*sp.pi*sp.integrate(p2**2,(q,-1,1))-4*sp.pi/5,
        'regular_response_transform': h2.subs(h,x**2*z).doit()/x**2
                                      -(-sp.diff(z,x,2)-6*sp.diff(z,x)/x+u*z),
        'symmetric_response_transform': x*h2.subs(h,y/x).doit()
                                      -(-sp.diff(y,x,2)+(6/x**2+u)*y),
        'energy_identity_with_boundary': x**2*h*h2
            -(x**2*sp.diff(h,x)**2+6*h**2+x**2*u*h**2)
            +sp.diff(x**2*h*sp.diff(h,x),x),
    }
    xx, yy, zz = sp.symbols('xx yy zz', real=True)
    tidal = (2*zz**2-xx**2-yy**2)/2
    eqs['vacuum_tidal_laplacian'] = sum(sp.diff(tidal,c,2) for c in (xx,yy,zz))
    rc, hc, fcprime, xi = sp.symbols('rc hc fcprime xi', nonzero=True)
    displacement = -hc/fcprime
    length = displacement-rc**3/3
    shifted_length = -(hc-xi*fcprime)/fcprime-rc**3/3-xi
    eqs['proper_contour_coordinate_invariance'] = shifted_length-length
    eqs['axis_difference'] = (length-length*(-sp.Rational(1,2)))+sp.Rational(3,2)*(hc/fcprime+rc**3/3)
    residuals = {key: str(sp.simplify(value)) for key,value in eqs.items()}
    mutations = {
        'reversed_forcing': sp.simplify(-s+x**2*sp.diff(w,f)) != 0,
        'energy_density_only': sp.simplify(x**2*sp.diff(rho-w,f)) != 0,
        'missing_angular_barrier': sp.simplify(6*h/x**2) != 0,
        'missing_proper_ruler': sp.simplify(-(hc-xi*fcprime)/fcprime-displacement) != 0,
        'monopole_replaces_quadrupole': sp.integrate(1,(q,-1,1)) != sp.integrate(p2,(q,-1,1)),
    }
    return {'exact_residuals': residuals, 'mutations_detected': mutations,
            'pass': all(value == '0' for value in residuals.values()),
            'mutations_pass': all(mutations.values())}


def background_module():
    path = WORK3 / (CORE + 'w3_58_one_oscillon_coframe_localized_core.py')
    spec = importlib.util.spec_from_file_location('w3_58_read_only', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if (module.A_BENCH, module.OMEGA_BENCH) != (A, OMEGA):
        raise ValueError('Inherited benchmark changed')
    return module


def coefficients(background, x):
    f = background.sol(x)[0]
    potential = 1-OMEGA**2-3*f**2+5*A*f**4
    forcing_z = 2*((1-2*OMEGA**2)*f-f**3+A*f**5)
    return potential, forcing_z


def collocation(background, radius, tolerance):
    x = np.linspace(0.0, radius, 801)

    def fun(xx, zz):
        pot, source = coefficients(background, xx)
        return np.vstack((zz[1], pot*zz[0]-source))

    sol = solve_bvp(fun, lambda za,zb: np.array([za[1],zb[0]]), x,
                    np.zeros((2,x.size)), S=np.array([[0.0,0.0],[0.0,-6.0]]),
                    tol=tolerance, max_nodes=100000)
    if not sol.success:
        raise RuntimeError('Response BVP failed: '+sol.message)
    return sol


def fd_response(background, radius, spacing):
    count = round(radius/spacing)
    x = np.linspace(0.0,radius,count+1)
    dx = x[1]-x[0]
    inner = x[1:-1]
    pot, source_z = coefficients(background,inner)
    diag = 2/dx**2+6/inner**2+pot
    off = np.full(inner.size-1,-1/dx**2)
    bands = np.zeros((3,inner.size))
    bands[0,1:], bands[1,:], bands[2,:-1] = off, diag, off
    source_y = inner**3*source_z
    yy = solve_banded((1,1),bands,source_y)
    y = np.zeros(x.size)
    y[1:-1] = yy
    h = np.zeros(x.size)
    h[1:] = y[1:]/x[1:]
    smallest = float(eigh_tridiagonal(diag,off,select='i',select_range=(0,0),
                                      eigvals_only=True)[0])
    applied = diag*yy
    applied[1:] += off*yy[:-1]
    applied[:-1] += off*yy[1:]
    residual = float(np.max(np.abs(applied-source_y))/max(np.max(abs(source_y)),1e-30))
    # Independent analytic manufactured source; y=x^3*(1-x/X).
    known = inner**3*(1-inner/radius)
    known_second = 6*inner-12*inner**2/radius
    manufactured_source = -known_second+(6/inner**2+pot)*known
    recovered = solve_banded((1,1),bands,manufactured_source)
    manufactured_error = float(np.linalg.norm(recovered-known)/np.linalg.norm(known))
    return x,h,{'smallest_hessian_eigenvalue':smallest,
                'discrete_equation_relative_residual':residual,
                'manufactured_relative_error':manufactured_error}


def contour(background, radius):
    level = float(background.sol(0)[0])/2
    rc = brentq(lambda r:float(background.sol(r)[0])-level,0.0,radius,xtol=1e-13)
    return rc,float(background.sol(rc)[1])


def observables(background, radius, hfun, points=16001):
    x = np.linspace(0.0,radius,points)
    h = hfun(x)
    _, source_z = coefficients(background,x)
    source = x**2*source_z
    rc,fp = contour(background,radius)
    hc = float(hfun(rc))
    c = ANGULAR*simpson(x**2*source*h,x=x)
    k_coordinate = -1.5*hc/fp
    k_ruler = -0.5*rc**3
    return {'C_profile':float(c),
            'intrinsic_source_moment_derivative_fixed_gauge':float(-c),
            'K_shape':float(k_coordinate+k_ruler),
            'K_coordinate_part':float(k_coordinate), 'K_ruler_part':float(k_ruler),
            'contour_radius':rc, 'contour_slope':fp, 'contour_h':hc}


def bvp_diagnostics(background, response, radius):
    x = np.linspace(0.001,radius,16001)
    z,zp = response.sol(x)
    zpp = response.sol(x,1)[1]
    pot,source_z = coefficients(background,x)
    residual = -zpp-6*zp/x+pot*z-source_z
    terms = abs(zpp)+abs(6*zp/x)+abs(pot*z)+abs(source_z)
    norm = math.sqrt(simpson(x**6*residual**2,x=x)/simpson(x**6*terms**2,x=x))
    x = np.linspace(0.0,radius,16001)
    z,zp = response.sol(x)
    h,hp = x**2*z,2*x*z+x**2*zp
    pot,source_z = coefficients(background,x)
    work = simpson(x**4*source_z*h,x=x)
    boundary = radius**2*h[-1]*hp[-1]
    energy = simpson(x**2*hp**2+6*h**2+x**2*pot*h**2,x=x)-boundary
    f = background.sol(x)[0]
    core_mask = f >= f[0]*1e-3
    max_fractional = float(np.max(abs(h[core_mask]/f[core_mask])))
    illustrative_epsilon = min(1e-6,1e-3/radius**2,1e-3/max(max_fractional,1e-30))
    return {'equation_normalized_weighted_l2_residual':norm,
            'energy_identity_relative_residual':relative(energy,work),
            'energy_boundary_term':float(boundary),
            'collocation_rms_residual_max':float(np.max(response.rms_residuals)),
            'maximum_core_fractional_response_per_epsilon':max_fractional,
            'core_definition':'f >= 0.001*f(0), used only for perturbative-domain reporting',
            'illustrative_epsilon':illustrative_epsilon,
            'illustrative_metric_smallness':illustrative_epsilon*radius**2,
            'illustrative_core_shape_smallness':illustrative_epsilon*max_fractional}


def numerical():
    inherited = background_module()
    canonical = inherited.solve_profile(OMEGA,radius=X_CANON,tolerance=1e-8)
    bg_obs = inherited.profile_observables(canonical,OMEGA,X_CANON,16001)
    response = collocation(canonical,X_CANON,1e-8)
    hfun = lambda x: np.asarray(x)**2*response.sol(x)[0]
    obs = observables(canonical,X_CANON,hfun)
    diag = bvp_diagnostics(canonical,response,X_CANON)
    records = []

    def record(label, values):
        row = {'case':label,**values}
        row['C_relative_change'] = relative(values['C_profile'],obs['C_profile'])
        row['K_relative_change'] = relative(values['K_shape'],obs['K_shape'],1.0)
        records.append(row)
        print(label+': C='+format(values['C_profile'],'.10g')
              +', K='+format(values['K_shape'],'.10g'),flush=True)

    record('canonical_collocation',obs)
    for points in (8001,16001):
        record('quadrature_'+str(points),observables(canonical,X_CANON,hfun,points))
    response_lo = collocation(canonical,X_CANON,1e-7)
    record('response_tolerance_1e-7',observables(canonical,X_CANON,
           lambda x:np.asarray(x)**2*response_lo.sol(x)[0]))
    bg_lo = inherited.solve_profile(OMEGA,radius=X_CANON,tolerance=1e-7,seed=canonical)
    rsp_lo = collocation(bg_lo,X_CANON,1e-8)
    record('background_tolerance_1e-7',observables(bg_lo,X_CANON,
           lambda x:np.asarray(x)**2*rsp_lo.sol(x)[0]))
    fd_rows = []
    for dx in (0.04,0.02,0.01):
        x,h,fd_diag = fd_response(canonical,X_CANON,dx)
        values = observables(canonical,X_CANON,CubicSpline(x,h))
        fd_rows.append({'dx':dx,**values,**fd_diag})
        record('finite_difference_dx_'+str(dx),{**values,**fd_diag})
    for radius in (40.0,60.0):
        bg = inherited.solve_profile(OMEGA,radius=radius,tolerance=1e-8,seed=canonical)
        rsp = collocation(bg,radius,1e-8)
        record('collocation_domain_'+str(radius),observables(bg,radius,
               lambda x:np.asarray(x)**2*rsp.sol(x)[0]))
        x,h,fd_diag = fd_response(bg,radius,0.01)
        record('finite_difference_domain_'+str(radius),
               {**observables(bg,radius,CubicSpline(x,h)),**fd_diag})
    c_spread = max(row['C_relative_change'] for row in records)
    k_spread = max(row['K_relative_change'] for row in records)
    finest,previous = fd_rows[-1],fd_rows[-2]
    gap_change = relative(finest['smallest_hessian_eigenvalue'],previous['smallest_hessian_eigenvalue'])
    finite_difference_residual = max(row['discrete_equation_relative_residual'] for row in fd_rows)
    manufactured = [row['manufactured_relative_error'] for row in fd_rows]
    tests = {
        'background_nonzero_nodeless': bg_obs['central_amplitude']>0.1
             and bg_obs['minimum_amplitude']>=-1e-12 and bg_obs['charge_dimensionless']>0,
        'background_equation': bg_obs['equation_normalized_weighted_l2_residual']<1e-5,
        'background_solver': bg_obs['collocation_rms_residual_max']<=1e-8,
        'background_virial': bg_obs['virial_relative']<1e-5,
        'contour_monotone': obs['contour_slope']<0 and bg_obs['maximum_positive_derivative']<=1e-10,
        'response_equation': diag['equation_normalized_weighted_l2_residual']<1e-5,
        'response_solver': diag['collocation_rms_residual_max']<=1e-8,
        'response_energy_identity':diag['energy_identity_relative_residual']<1e-5,
        'response_mesh_domain_tolerance_quadrature':c_spread<2e-3 and k_spread<2e-3,
        'positive_profile_susceptibility':obs['C_profile']>0,
        'positive_hessian':min(row['smallest_hessian_eigenvalue'] for row in fd_rows)>1e-4,
        'hessian_mesh_convergence':gap_change<2e-3,
        'response_finest_vs_next_mesh':relative(finest['C_profile'],previous['C_profile'])<2e-3
                    and relative(finest['K_shape'],previous['K_shape'],1.0)<2e-3,
        'independent_response_equation':finite_difference_residual<1e-5,
        'independent_response_coefficients':relative(finest['C_profile'],obs['C_profile'])<2e-3
                      and relative(finest['K_shape'],obs['K_shape'],1.0)<2e-3,
        'manufactured_recovery':max(manufactured)<2e-3
                     and manufactured[2]<manufactured[1]<manufactured[0],
    }
    return {'canonical':obs,'background':bg_obs,'diagnostics':diag,
            'convergence':records,'finite_difference_mesh':fd_rows,
            'numerical_error_estimates':{'C_max_relative_spread':c_spread,
               'K_max_relative_spread':k_spread,'hessian_mesh_relative_change':gap_change,
               'interval_certified':False},'tests':tests,'pass':all(tests.values())}


def main():
    flags = {key:False for key in TRUE_KEYS+OPEN_KEYS+('local_tidal_response_pass',)}
    dep = dependencies()
    exact = symbolic()
    flags['dependencies_pinned'] = dep['pass']
    flags['linear_action_and_source_exact'] = exact['pass']
    flags['fixed_charge_selection_exact'] = exact['pass'] and dep['pass']
    flags['proper_length_map_exact'] = exact['exact_residuals']['proper_contour_coordinate_invariance']=='0'
    flags['mutation_controls_pass'] = exact['mutations_pass']
    result = {'claim_id':'W3_74_OSCILLON_TIDAL_SOURCE_RESPONSE','model_version':VERSION,
              'dependencies':dep,'symbolic':exact,
              'provenance':{'script_sha256':sha(Path(__file__)),
                    'preregistration_sha256':sha(PREREG),'python':platform.python_version(),
                    'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},
              'scope':'Static linear vacuum tide, fixed ordinary charge, prescribed external metric, negligible core self-gravity.',
              'normalizations':{
                  'background_W3_58':'Inherited background energy E*lambda/(4*pi*m), charge Q*lambda/(4*pi).',
                  'C_profile':'Full angular normalization; profile energy shift = -(m/lambda)*epsilon^2*C_profile/2.',
                  'source_moment':'d[integral x^2*P2*W(f_epsilon) d^3x]/d epsilon at zero = -C_profile; intrinsic profile term only.',
                  'K_shape':'m*d(ell_pole-ell_equator)/d epsilon; epsilon=E_zz/(2*m^2).',
                  'radii':'Dimensionless x=m*r; physical proper lengths use 1/m.'},
              'open_reason':'The inherited action gives a geometric tidal response. A dynamical pressure-depletion law and uniform mass/radius/tail scaling are not specified by this calculation.'}
    if dep['pass'] and exact['pass']:
        nums = numerical()
        result['numerical'] = nums
        flags['response_converged_numerical'] = nums['pass']
        flags['quadrupole_hessian_positive_numerical'] = nums['tests']['positive_hessian'] and nums['tests']['hessian_mesh_convergence']
        flags['independent_crosscheck_pass'] = all(nums['tests'][k] for k in
            ('independent_response_equation','independent_response_coefficients','manufactured_recovery'))
    flags['local_tidal_response_pass'] = all(flags[key] for key in TRUE_KEYS)
    result['closure_flags'] = flags
    result['status'] = ('PASS_LINEAR_TEST_CORE_TIDAL_RESPONSE_NUMERICAL_BENCHMARK'
         if flags['local_tidal_response_pass'] else
         'FAIL_EXACT_OR_DEPENDENCY' if not (dep['pass'] and exact['pass']) else
         'NUMERICALLY_INCONCLUSIVE')
    # Sole generated artifact; reject NaN instead of exporting invalid JSON.
    result = native(result)
    OUTPUT.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'closure_flags':flags},indent=2))
    if not flags['local_tidal_response_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
