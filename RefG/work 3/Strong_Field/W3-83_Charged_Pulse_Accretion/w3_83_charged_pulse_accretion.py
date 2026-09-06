"""W3-83 frozen finite charged-pulse evolution. Writes finite JSON to stdout only."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
import platform
import time
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import cumulative_simpson, simpson, solve_ivp
from scipy.interpolate import CubicSpline, RectBivariateSpline, make_interp_spline
from scipy.optimize import linear_sum_assignment, least_squares

HERE = Path(__file__).resolve()
ROOT = HERE.parents[4]
CONTRACT_HASH = 'd25441d2fbf5954ac6b6e3c2b3feb2139474a3b12446bf9b202f6f98b6264e6e'
PREFIX = 'RefG/work 3/Strong_Field/'
PINS = {
    'CODES.md': '27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41',
    PREFIX + 'W3-73_Coupled_Horizon_Regular_Einstein_Complex_Scalar/w3_73_coupled_horizon_regular_einstein_complex_scalar.py': '47f2c97b64544f124cc2a5cb8d04825188664493cb5d770b6c3faf4ce2d5d7ca',
    PREFIX + 'W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction_contract.md': '7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa',
    PREFIX + 'W3-80_Resonant_Constitutive_Candidate/w3_80_neutral_resonant_condensate_contract.md': '27e359b9980df14a287ca89cc38a895eb5015a732154d7a055fd7666b418d841',
}
TIMES = np.arange(401, dtype=float) / 100
FIXED_RADII = (1., 2., 4., 8., 12.)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(a, b, p, q, f, g, quartic=1):
    x = a*a + b*b
    potential = x/2 + quartic*x*x/4
    kinetic = (p*p + q*q + f*f + g*g)/2
    return (kinetic + potential, p*f + q*g, kinetic - potential,
            (p*p + q*q - f*f - g*g)/2 - potential,
            ((1 + quartic*x)*a, (1 + quartic*x)*b))


def mass_flux(r, sigma, z, p, q, f, g, sign=1):
    return sign*4*np.pi*sigma*r*r*((p + z*f)*(z*p + f) + (q + z*g)*(z*q + g))


def mass_source(r, z, rho, S, factor=1):
    return factor*4*np.pi*r*r*(rho + z*S)


def charge_flux(r, sigma, z, a, b, p, q, f, g, sign=1):
    return sign*4*np.pi*sigma*r*r*(z*(a*q - b*p) + a*g - b*f)


def derivative(y, h):
    out = np.empty_like(y)
    out[..., 2:-2] = (y[..., :-4] - 8*y[..., 1:-3] + 8*y[..., 3:-1] - y[..., 4:])/(12*h)
    out[..., 0] = (-25*y[..., 0] + 48*y[..., 1] - 36*y[..., 2] + 16*y[..., 3] - 3*y[..., 4])/(12*h)
    out[..., 1] = (-3*y[..., 0] - 10*y[..., 1] + 18*y[..., 2] - 6*y[..., 3] + y[..., 4])/(12*h)
    out[..., -1] = (25*y[..., -1] - 48*y[..., -2] + 36*y[..., -3] - 16*y[..., -4] + 3*y[..., -5])/(12*h)
    out[..., -2] = (3*y[..., -1] + 10*y[..., -2] - 18*y[..., -3] + 6*y[..., -4] - y[..., -5])/(12*h)
    return out


def bump(r, amplitude):
    rr = np.asarray(r, dtype=float)
    x = rr - 5
    inside = np.abs(x) < 1
    phi = np.zeros_like(rr)
    grad = np.zeros_like(rr)
    xx = x[inside]
    phi[inside] = amplitude*np.exp(1 - 1/(1-xx*xx))
    grad[inside] = -2*xx*phi[inside]/(1-xx*xx)**2
    return phi, grad


def initial(r, amplitude):
    a, f = bump(r, amplitude)
    Y = np.zeros((7, len(r)))
    Y[0], Y[2], Y[3], Y[4] = a, f+a/r, a, f

    def ode(x, m):
        aa, ff = bump(x, amplitude)
        rho, S, _, _, _ = source(aa, 0, ff+aa/x, aa, ff, 0)
        return [float(mass_source(x, np.sqrt(2*m[0]/x), rho, S))]

    sol = solve_ivp(ode, (r[0], r[-1]), [1.], method='DOP853',
                    rtol=1e-12, atol=1e-14, max_step=.01, t_eval=r)
    if not sol.success:
        raise RuntimeError('Initial mass-constraint integration: ' + sol.message)
    Y[6] = sol.y[0]
    return Y


def geometry(Y, r):
    if not np.isfinite(Y).all() or np.min(Y[6]) <= 0:
        raise RuntimeError('Nonfinite field or nonpositive Misner-Sharp mass')
    rho, S, pr, pt, force = source(*Y[:6])
    z = np.sqrt(2*Y[6]/r)
    ell = cumulative_simpson(-4*np.pi*r*S/z, x=r, initial=0)
    sigma = np.exp(ell-ell[-1])
    if not np.isfinite(sigma).all() or np.min(sigma) <= 0 or z[0] <= 1:
        raise RuntimeError('Lapse positivity/finite or inner outflow domain failed')
    return sigma, z, rho, S, pr, pt, np.asarray(force)


def symbolic_checks():
    # These same helpers enter the actual finite-difference RHS and diagnostics.
    a, b, p, q, f, g, r, sig, z = sp.symbols('a b p q f g r sigma z', real=True)
    V = (a*a+b*b)/2 + (a*a+b*b)**2/4
    # Canonical Hilbert stress T_ab=sum(d_a phi d_b phi)+eta_ab L.
    eta = sp.diag(-1, 1, 1, 1)
    da, db = sp.Matrix([p, f, 0, 0]), sp.Matrix([q, g, 0, 0])
    L = -(da.dot(eta*da)+db.dot(eta*db))/2 - V
    T = da*da.T + db*db.T + eta*L
    rho, S, pr, pt, forces = source(a, b, p, q, f, g)
    hilbert = [sp.simplify(x-y) for x, y in zip((rho, S, pr, pt), (T[0, 0], T[0, 1], T[1, 1], T[2, 2]))]
    # Obtain charge divergence from the full component field equations.
    t, x = sp.symbols('T r', real=True)
    A, B, P, Q, F, G, N, Z = [sp.Function(name)(t, x) for name in ('a','b','p','q','f','g','N','Z')]
    at, bt = N*(P+Z*F), N*(Q+Z*G)
    ptime = sp.diff(N*x*x*(F+Z*P), x)/x**2 - N*(1+A*A+B*B)*A
    qtime = sp.diff(N*x*x*(G+Z*Q), x)/x**2 - N*(1+A*A+B*B)*B
    density_time = x*x*(at*Q + A*qtime - bt*P - B*ptime)
    spatial_subs = {sp.diff(A, x): F, sp.diff(B, x): G}

    def validator(quartic=1, msign=1, qsign=1, norm=1):
        rr, ss, _, _, force = source(a, b, p, q, f, g, quartic)
        # np.pi is factored off before symbolic comparisons; no approximate pi algebra.
        mf = mass_flux(r, sig, z, p, q, f, g, msign)/(4*np.pi)
        expected_mf = sig*r*r*(z*(T[0, 0]+T[1, 1])+(1+z*z)*T[0, 1])
        ms = mass_source(r, z, rr, ss, norm)/(4*np.pi)
        qf = charge_flux(x, N, Z, A, B, P, Q, F, G, qsign)/(4*np.pi)
        residuals = {
            'force_a': sp.simplify(force[0]-sp.diff(V, a)),
            'force_b': sp.simplify(force[1]-sp.diff(V, b)),
            'mass_flux': sp.simplify(sp.expand(mf-expected_mf)),
            'mass_source': sp.simplify(sp.expand(ms-r*r*(T[0, 0]+z*T[0, 1]))),
            'charge_divergence': sp.simplify(sp.expand((density_time-sp.diff(qf, x)).subs(spatial_subs))),
        }
        return {'accepted': all(v == 0 for v in residuals.values()),
                'residuals': {k: str(v) for k, v in residuals.items()}}

    baseline = validator()
    controls = {name: validator(**kwargs) for name, kwargs in (
        ('missing_quartic_force', {'quartic': 0}),
        ('reversed_mass_flux', {'msign': -1}),
        ('wrong_charge_flux_sign', {'qsign': -1}),
        ('misnormalized_mass_source', {'norm': 2}))}
    return {'hilbert_residuals': [str(v) for v in hilbert], 'baseline': baseline,
            'controls': controls,
            'passed': all(v == 0 for v in hilbert) and baseline['accepted'] and all(not v['accepted'] for v in controls.values())}


def evolve(label, h, dt, rout=14., amplitude=.02):
    started = time.monotonic()
    print('W83 ' + label + ': starting full evolution', file=sys.stderr, flush=True)
    r = np.linspace(1., rout, round((rout-1)/h)+1)
    Y = initial(r, amplitude)
    states = np.empty((len(TIMES), 7, len(r)))
    states[0] = Y
    max_courant = 0.
    causal_upper = 0.
    min_sigma, min_mass, min_inner_z = 1e100, 1e100, 1e100

    def rhs(state):
        nonlocal min_sigma, min_mass, min_inner_z
        sig, z, rho, S, pr, pt, force = geometry(state, r)
        min_sigma = min(min_sigma, float(sig.min()))
        min_mass = min(min_mass, float(state[6].min()))
        min_inner_z = min(min_inner_z, float(z[0]))
        out = np.empty_like(state)
        out[:2] = sig*(state[2:4]+z*state[4:6])
        out[4:6] = derivative(out[:2], h)
        out[2:4] = derivative(sig*r*r*(state[4:6]+z*state[2:4]), h)/(r*r)-sig*force
        out[6] = mass_flux(r, sig, z, *state[2:6])
        out[:, -1] = 0  # Frozen vacuum outer endpoint; inner endpoint freely evolves.
        speeds = sig*(1+z)
        return out, float(speeds.max()), float(speeds[r >= 6-1e-12].max())

    try:
        for j in range(1, len(TIMES)):
            t = TIMES[j-1]
            while t < TIMES[j]-1e-14:
                step = min(dt, TIMES[j]-t)
                k1, c1, e1 = rhs(Y)
                k2, c2, e2 = rhs(Y+step*k1/2)
                k3, c3, e3 = rhs(Y+step*k2/2)
                k4, c4, e4 = rhs(Y+step*k3)
                cc = step*max(c1,c2,c3,c4)/h
                if cc >= .45:
                    raise RuntimeError('Actual characteristic Courant number >= .45: ' + str(cc))
                max_courant = max(max_courant, cc)
                causal_upper += step*max(e1,e2,e3,e4)
                Y = Y+step*(k1+2*k2+2*k3+k4)/6
                t += step
            geometry(Y, r)
            states[j] = Y
            if j % 100 == 0:
                print('W83 %s: T=%.2f, m_inner=%.10g' % (label, TIMES[j], Y[6,0]), file=sys.stderr, flush=True)
    except (RuntimeError, FloatingPointError, ValueError) as exc:
        return {'label': label, 'completed': False, 'failure': str(exc),
                'last_stored_time': float(TIMES[j-1]), 'h': h, 'dt': dt, 'rout': rout}
    result = diagnose(states, r, h, label, dt, amplitude)
    result['health'].update(max_stage_courant=max_courant,
                            stage_upper_exterior_travel=causal_upper,
                            min_stage_sigma=min_sigma, min_stage_mass=min_mass,
                            min_stage_inner_zeta=min_inner_z)
    result['wall_seconds'] = time.monotonic()-started
    return result


def relative_norm(left, right):
    return float(np.linalg.norm(left-right)/max(np.linalg.norm(left), np.linalg.norm(right), 1e-8))


def critical_events(states, r, transitions):
    """Solve actual double-root conditions, without interpolating the outer envelope."""
    if not transitions:
        return []
    mass = RectBivariateSpline(TIMES, r, states[:,6], kx=3, ky=3, s=0)
    events = []
    for change in transitions:
        previous, current = change['previous_roots'], change['roots']
        creation = len(current) > len(previous)
        large, small = (current, previous) if creation else (previous, current)
        rows, cols = linear_sum_assignment(np.abs(np.subtract.outer(small,large)))
        unmatched = [value for k,value in enumerate(large) if k not in cols]
        lo, hi = change['time_bracket']
        if len(unmatched) != 2:
            events.append({'label':'unresolved multiple transition','passed':False,
                           'time_bracket':[lo,hi],'unmatched_roots':unmatched})
            continue

        def equations(point):
            t, x = point
            return np.array([x-2*mass.ev(t,x),1-2*mass.ev(t,x,dy=1)])

        def jacobian(point):
            t, x = point
            return np.array([[-2*mass.ev(t,x,dx=1),1-2*mass.ev(t,x,dy=1)],
                             [-2*mass.ev(t,x,dx=1,dy=1),-2*mass.ev(t,x,dy=2)]])

        seed_time, pair_seed = (lo+hi)/2,float(np.mean(unmatched))
        mid_h = CubicSpline(r,r-2*mass.ev(np.full_like(r,seed_time),r))
        stationary = [x for x in mid_h.derivative().roots(extrapolate=False) if r[0]<x<r[-1]]
        refined_seed = float(min(stationary,key=lambda x:abs(x-pair_seed))) if stationary else pair_seed
        solution = least_squares(equations, [seed_time,refined_seed], jac=jacobian,
                                 bounds=([lo,r[0]],[hi,r[-1]]),
                                 x_scale=[hi-lo,max(np.ptp(unmatched),r[1]-r[0])],
                                 xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=200)
        t, x = map(float,solution.x)
        residual = equations(solution.x)/np.array([2.,1.])
        admissible = lo <= t <= hi and r[0] < x < r[-1]
        events.append({'label':'creation' if creation else 'annihilation',
                       'time':t,'radius':x,'time_bracket':[lo,hi],
                       'unmatched_roots':unmatched,'solver_success':bool(solution.success),
                       'unmatched_pair_seed':[seed_time,pair_seed],
                       'stationary_refined_seed':[seed_time,refined_seed],
                       'dimensionless_residuals':residual.tolist(),
                       'passed':bool(admissible and np.max(np.abs(residual))<1e-8)})
    return events


def diagnose(states, r, h, label, dt, amplitude):
    nout = len(TIMES)
    H = {name: np.empty(nout) for name in (
        'r_h','D_h','horizon_speed','horizon_charge_flux','m_inner','Q_domain',
        'charge_flux_inner','charge_flux_outer','mass_constraint_full',
        'mass_constraint_interior','aux_constraint_full','aux_constraint_interior',
        'mass_reconstruction_abs','peak_rho','peak_abs_pressure','peak_abs_ricci',
        'outer_stress','max_exterior_speed','sigma_inner')}
    all_roots, jumps, root_flux_rows = [], [], []
    # Independent derivative of the STORED mass history, never an RHS accumulator.
    stored_mass_t = make_interp_spline(TIMES, states[:,6]-states[0,6], k=5, axis=0).derivative()(TIMES)
    fixed_m, fixed_flux = np.empty((nout, len(FIXED_RADII))), np.empty((nout, len(FIXED_RADII)))
    fixed_indices = np.array([round((x-1)/h) for x in FIXED_RADII])
    Q_horizon_exterior = np.empty(nout)
    vacuum_error = 0.
    for j, Y in enumerate(states):
        sig, z, rho, S, pr, pt, _ = geometry(Y, r)
        mr, phir = derivative(Y[6], h), derivative(Y[:2], h)
        ms = mass_source(r, z, rho, S)
        q = Y[0]*Y[3]-Y[1]*Y[2]
        fluxq = charge_flux(r, sig, z, *Y[:6])
        # Independent stress form, not the production factorized RHS/its RK accumulator.
        energy_flux = 4*np.pi*sig*r*r*(z*(rho+pr)+(1+z*z)*S)
        radial_m = Y[6,0]+cumulative_simpson(ms, x=r, initial=0)
        hspline = CubicSpline(r, r-2*Y[6])
        roots = [float(x) for x in hspline.roots(extrapolate=False) if r[0] <= x <= r[-1]]
        roots = sorted(set(roots))
        if not roots:
            raise RuntimeError('No marginal root on frozen annulus at output ' + str(j))
        all_roots.append(roots)
        rh = roots[-1]
        field_spline = CubicSpline(r, Y, axis=1)
        yh = field_spline(rh)
        sigma_spline = CubicSpline(r, sig)
        sigh = float(sigma_spline(rh))
        dh = float(hspline(rh, 1))
        mth = 4*np.pi*sigh*rh*rh*np.sum((yh[2:4]+yh[4:6])**2)
        speed = 2*mth/dh if dh != 0 else 0.
        qh = yh[0]*yh[3]-yh[1]*yh[2]
        sh = yh[0]*yh[5]-yh[1]*yh[4]
        if 2 <= j <= 398:
            all_y = field_spline(roots)
            all_sig = sigma_spline(roots)
            rates = 4*np.pi*all_sig*np.array(roots)**2*np.sum((all_y[2:4]+all_y[4:6])**2,axis=0)
            measured = CubicSpline(r,stored_mass_t[j])(roots)
            root_flux_rows.append({'time':float(TIMES[j]),'roots':roots,
                                   'stored_mass_derivative':measured.tolist(),
                                   'null_flux_source':rates.tolist()})
        if j and len(roots) != len(all_roots[j-1]):
            jumps.append({'time_bracket': [float(TIMES[j-1]),float(TIMES[j])],
                          'previous_roots': all_roots[j-1], 'roots': roots})
        values = {
            'r_h': rh, 'D_h': dh, 'horizon_speed': speed,
            'horizon_charge_flux': 4*np.pi*rh*rh*(sigh*(qh+sh)+qh*speed),
            'm_inner': Y[6,0], 'Q_domain': 4*np.pi*simpson(r*r*q, x=r),
            'charge_flux_inner': fluxq[0], 'charge_flux_outer': fluxq[-1],
            'mass_constraint_full': relative_norm(mr, ms),
            'mass_constraint_interior': relative_norm(mr[4:-4], ms[4:-4]),
            'aux_constraint_full': relative_norm(Y[4:6], phir),
            'aux_constraint_interior': relative_norm(Y[4:6,4:-4], phir[:,4:-4]),
            'mass_reconstruction_abs': np.max(np.abs(Y[6]-radial_m)),
            'peak_rho': rho.max(), 'peak_abs_pressure': max(np.abs(pr).max(),np.abs(pt).max()),
            'peak_abs_ricci': np.max(np.abs(8*np.pi*(rho-pr-2*pt))),
            'outer_stress': np.max(np.abs(np.stack((rho,S,pr,pt))[:,r>=r[-1]-2])),
            'max_exterior_speed': np.max(sig[r>=6-1e-12]*(1+z[r>=6-1e-12])),
            'sigma_inner': sig[0],
        }
        for key, value in values.items():
            H[key][j] = value
        # Integral of actual charge density, independently of horizon-flux formula.
        charge_integral = CubicSpline(r, 4*np.pi*r*r*q).antiderivative()
        Q_horizon_exterior[j] = charge_integral(r[-1])-charge_integral(rh)
        fixed_m[j] = Y[6,fixed_indices]
        fixed_flux[j] = energy_flux[fixed_indices]
        if amplitude == 0:
            vacuum_error = max(vacuum_error, float(np.max(np.abs(Y[:6]))),
                               float(np.max(np.abs(Y[6]-1))), float(np.max(np.abs(sig-1))), abs(rh-2))
    q0 = H['Q_domain'][0]
    excess = states[0,6,-1]-1
    qscale, mscale = (q0 if q0 > 0 else 1.), (excess if excess > 0 else 1.)
    H['captured_inner_charge'] = cumulative_simpson(H['charge_flux_inner'], x=TIMES, initial=0)
    H['charge_balance_residual'] = H['Q_domain']+cumulative_simpson(H['charge_flux_inner']-H['charge_flux_outer'], x=TIMES, initial=0)-q0
    integrated_mass = cumulative_simpson(fixed_flux, x=TIMES, axis=0, initial=0)
    mass_errors = np.max(np.abs(fixed_m-fixed_m[0]-integrated_mass), axis=0)/mscale
    # An envelope through a root birth is NOT an integrated smooth horizon.
    smooth = len(jumps) == 0 and all(len(v) == 1 for v in all_roots) and np.all(H['D_h'] > 0)
    if smooth:
        H['integrated_horizon_radius'] = H['r_h'][0]+cumulative_simpson(H['horizon_speed'], x=TIMES, initial=0)
        horizon_error = float(np.max(np.abs(H['r_h']-H['integrated_horizon_radius']))/H['r_h'][0])
    else:
        horizon_error = None
    events = critical_events(states,r,jumps)
    root_rate_scale = max(excess/4,max((abs(x) for row in root_flux_rows for x in row['null_flux_source']),default=0),1e-100)
    root_rate_error = max((abs(a-b) for row in root_flux_rows for a,b in zip(row['stored_mass_derivative'],row['null_flux_source'])),default=0)/root_rate_scale
    terminal = TIMES >= 2
    terminal_smooth = all(len(v)==1 for v in all_roots[200:]) and np.all(H['D_h'][terminal]>0)
    terminal_integral = H['r_h'][200]+cumulative_simpson(H['horizon_speed'][terminal],x=TIMES[terminal],initial=0)
    terminal_error = float(np.max(np.abs(H['r_h'][terminal]-terminal_integral))/H['r_h'][0])
    H['Q_outside_outer_marginal_sphere'] = Q_horizon_exterior
    metrics = {
        'mass_constraint_full_max': float(H['mass_constraint_full'].max()),
        'mass_constraint_interior_max': float(H['mass_constraint_interior'].max()),
        'aux_constraint_full_max': float(H['aux_constraint_full'].max()),
        'aux_constraint_interior_max': float(H['aux_constraint_interior'].max()),
        'mass_reconstruction_relative_max': float(H['mass_reconstruction_abs'].max()/mscale),
        'charge_balance_relative_max': float(np.abs(H['charge_balance_residual']).max()/qscale),
        'mass_flux_relative_max': float(mass_errors.max()),
        'mass_flux_by_radius': dict(zip(map(str,FIXED_RADII),map(float,mass_errors))),
        'horizon_flux_relative_max': horizon_error,
        'horizon_smooth_single_branch': bool(smooth),
        'min_outer_D_h': float(H['D_h'].min()),
        'sampled_exterior_travel': float(simpson(H['max_exterior_speed'], x=TIMES)),
        'outer_stress_relative_max': float(H['outer_stress'].max()/max(H['peak_rho'][0],1e-100)),
        'vacuum_absolute_error': vacuum_error,
        'all_root_flux_relative_max':float(root_rate_error),
        'all_root_flux_normalization':float(root_rate_scale),
        'terminal_horizon_smooth':bool(terminal_smooth),
        'terminal_horizon_integral_relative_max':terminal_error,
        'critical_events_passed':all(event['passed'] for event in events),
    }
    return {'label':label, 'completed': True, 'h':h, 'dt':dt, 'rout':float(r[-1]),
            'initial': {'outer_mass':float(states[0,6,-1]),'pulse_excess_mass':float(excess),
                        'Q':float(q0),'horizon':float(H['r_h'][0]),'sigma_inner':float(H['sigma_inner'][0])},
            'metrics':metrics, 'health':{}, 'root_topology_events':jumps, 'critical_events':events,
            'all_roots':all_roots,'all_root_flux_checks':root_flux_rows,
            'terminal_integrated_horizon_radius':terminal_integral.tolist(),
            'history':{k:v.tolist() for k,v in H.items()},
            'final':{k:float(H[k][-1]) for k in ('r_h','m_inner','Q_domain','captured_inner_charge')},
            'horizon_area_initial':float(4*np.pi*H['r_h'][0]**2),
            'horizon_area_final':float(4*np.pi*H['r_h'][-1]**2)}


def compare(a, b, reference, horizon_mask=None):
    scales = {'r_h':reference['initial']['horizon'],
              'm_inner':reference['initial']['pulse_excess_mass'],
              'Q_domain':reference['initial']['Q'],
              'captured_inner_charge':reference['initial']['Q']}
    differences = {}
    for key,scale in scales.items():
        error = np.abs(np.array(a['history'][key])-b['history'][key])/scale
        if key == 'r_h' and horizon_mask is not None:
            error = error[horizon_mask]
        differences[key] = float(np.max(error))
    return differences


def compare_events(a,b,reference):
    ea,eb = a['critical_events'],b['critical_events']
    matched = len(ea)==len(eb) and all(x['label']==y['label'] for x,y in zip(ea,eb))
    valid = matched and all(x['passed'] for x in ea+eb)
    if not valid:
        return {'matched_valid_events':False,'errors':[]}
    errors = [{'time':abs(x['time']-y['time'])/4,
               'radius':abs(x['radius']-y['radius'])/reference['initial']['horizon']}
              for x,y in zip(ea,eb)]
    return {'matched_valid_events':True,'errors':errors}


def main():
    contract = HERE.with_name('w3_83_charged_pulse_accretion_contract.md')
    hashes = {path:{'expected':target,'actual':sha(ROOT/path)} for path,target in PINS.items()}
    provenance = {'pins':hashes,'source_sha256':sha(HERE),'contract_sha256':sha(contract),
                  'exact_two_files':sorted(p.name for p in HERE.parent.iterdir()) == sorted([HERE.name,contract.name]),
                  'versions':{'Python':platform.python_version(),'NumPy':np.__version__,'SciPy':scipy.__version__,'SymPy':sp.__version__}}
    pinned = all(row['actual']==row['expected'] for row in hashes.values()) and sha(contract)==CONTRACT_HASH and provenance['exact_two_files']
    result = {'stage':'W3-83-v1.1','claim':'W3_83_FULL_COLLECTIVE_CHARGED_PULSE_ACCRETION',
              'provenance':provenance,'provenance_passed':pinned,'times':TIMES.tolist()}
    result['scope'] = {key:False for key in ('first_horizon_formation','full_collapse_endpoint',
        'singularity_resolution','foundation_pressure_map','observational_pass','intuitive_files_changed')}
    if not pinned:
        result.update(status='UNRESOLVED', failure='Frozen provenance or exact-two-file check failed')
        return result
    symbolic = symbolic_checks()
    result['production_identity_controls'] = symbolic
    if not symbolic['passed']:
        result.update(status='UNRESOLVED',failure='Production symbolic baseline or mutation control failed')
        return result
    runs = {}
    for label,h,dt,rout,amp in (
        ('coarse',.04,.004,14.,.02),('medium',.02,.002,14.,.02),
        ('fine',.01,.001,14.,.02),('ultrafine',.005,.0005,14.,.02),
        ('time_crosscheck',.02,.001,14.,.02),
        ('boundary_crosscheck',.02,.002,18.,.02),('vacuum',.04,.004,14.,0.)):
        runs[label] = evolve(label,h,dt,rout,amp)
    result['runs'] = runs
    completed = all(v['completed'] for v in runs.values())
    result['closure_flags'] = {'finite_evolution':completed,'mutation_controls':symbolic['passed']}
    if not completed:
        result.update(status='UNRESOLVED',physical_outcome='unresolved',failure='At least one frozen evolution failed its domain')
        return result
    result['baseline_v1_0'] = {
        'historical_status':'UNRESOLVED',
        'historical_source_sha256':'af9e26509a0957625f961e744fb95f94c2feebd74478df7946d61af1929a1b44',
        'failed_gates':['smooth_horizon_flux_trajectory','refinement'],
        'recomputed_coarse_medium':compare(runs['coarse'],runs['medium'],runs['fine']),
        'recomputed_medium_fine':compare(runs['medium'],runs['fine'],runs['fine']),
        'original_fine_metrics':runs['fine']['metrics']}
    co,me,fi = runs['medium'],runs['fine'],runs['ultrafine']
    horizon_mask = np.ones(len(TIMES),dtype=bool)
    event_times = [event['time'] for run in (co,me,fi) for event in run['critical_events'] if event['passed']]
    for event_time in event_times:
        horizon_mask &= np.abs(TIMES-event_time) > .02
    cm,mf = compare(co,me,fi,horizon_mask),compare(me,fi,fi,horizon_mask)
    # Original time/boundary crosschecks are both on h=.02, not the primary medium h=.01.
    tc = compare(runs['medium'],runs['time_crosscheck'],fi,horizon_mask)
    bc = compare(runs['medium'],runs['boundary_crosscheck'],fi,horizon_mask)
    ec,ef = compare_events(co,me,fi),compare_events(me,fi,fi)
    event_refinement = ec['matched_valid_events'] and ef['matched_valid_events'] and all(
        y[k]<.001 and (y[k]<1e-7 or y[k]<=.5*x[k])
        for x,y in zip(ec['errors'],ef['errors']) for k in ('time','radius'))
    residuals = [runs[name]['metrics']['mass_constraint_interior_max'] for name in ('medium','fine','ultrafine')]
    refinement_observables = all(mf[k]<.001 and (mf[k]<1e-7 or mf[k] <= .5*cm[k]) for k in mf)
    refinement_constraint = all(b<1e-7 or b<=.5*a for a,b in zip(residuals,residuals[1:]))
    fm = fi['metrics']
    gates = {
        'finite_evolution':completed,
        'constraints':fm['mass_constraint_interior_max']<.005 and fm['aux_constraint_interior_max']<.002 and fm['mass_reconstruction_relative_max']<.001,
        'current_balance':fm['charge_balance_relative_max']<.0002,
        'independent_mass_flux_balance':fm['mass_flux_relative_max']<.0002,
        'event_resolved_horizon_topology':event_refinement and fm['critical_events_passed'],
        'all_root_null_flux':fm['all_root_flux_relative_max']<.0002,
        'terminal_horizon_flux_trajectory':fm['terminal_horizon_smooth'] and fm['terminal_horizon_integral_relative_max']<.0002,
        'refinement':refinement_observables and refinement_constraint,
        'independent_time_check':max(tc.values())<.0002,
        'exterior_boundary_check':max(bc.values())<.0002 and fm['sampled_exterior_travel']<8 and fi['health']['stage_upper_exterior_travel']<8 and fm['outer_stress_relative_max']<1e-10,
        'vacuum_control':runs['vacuum']['metrics']['vacuum_absolute_error']<1e-11,
        'mutation_controls':symbolic['passed'],
    }
    result['closure_flags'] = gates
    result['comparisons'] = {'coarse_medium':cm,'medium_fine':mf,'time_step':tc,'outer_boundary':bc,
                             'primary_spacing_triple':[.02,.01,.005],
                             'critical_events_coarse_medium':ec,'critical_events_medium_fine':ef,
                             'horizon_only_excluded_times':TIMES[~horizon_mask].tolist(),
                             'horizon_event_union_times':event_times,'horizon_exclusion_half_width':.02,
                             'mass_constraint_maxima':residuals,'observable_refinement_passed':refinement_observables,
                             'constraint_refinement_passed':refinement_constraint}
    passed = all(gates.values())
    growth = fi['final']['r_h']-fi['initial']['horizon']
    massgain = fi['final']['m_inner']-1
    result['measured_change'] = {'outer_horizon_radius':growth,'inner_mass':massgain,
        'horizon_refinement_error':mf['r_h']*fi['initial']['horizon'],
        'inner_mass_refinement_error':mf['m_inner']*fi['initial']['pulse_excess_mass'],
        'captured_charge_fraction':fi['final']['captured_inner_charge']/fi['initial']['Q'],
        'remaining_domain_charge_fraction':fi['final']['Q_domain']/fi['initial']['Q']}
    resolved_growth = growth>10*mf['r_h']*fi['initial']['horizon'] and massgain>10*mf['m_inner']*fi['initial']['pulse_excess_mass']
    result['status'] = 'PASS' if passed else 'UNRESOLVED'
    result['physical_outcome'] = ('resolved accretion/horizon growth' if resolved_growth else 'resolved small/no change') if passed else 'unresolved under the frozen full acceptance gate'
    result['failed_gates'] = [key for key,value in gates.items() if not value]
    result['interpretation'] = ('Full canonical collective scalar on one Einstein metric; no EOS elimination or additional fluid source. '
        'The explicit v1.1 amendment tests every observed marginal-root critical event and checks flux at every sampled root; '
        'only the fixed terminal [2,4] single-root interval receives a smooth trajectory integral. '
        'The earlier outermost-root envelope is never spliced into a fictitious smooth horizon. '
        'Curvature diagnostic is the local Einstein trace scalar 8pi(rho-pr-2pT), not a centre-completeness test.')
    return result


if __name__ == '__main__':
    try:
        with np.errstate(over='raise',invalid='raise',divide='raise'):
            output = main()
        print(json.dumps(output, ensure_ascii=True, allow_nan=False, separators=(',',':')))
        sys.exit(0 if output.get('status') == 'PASS' else 1)
    except Exception as exc:
        print(json.dumps({'stage':'W3-83-v1.1','status':'UNRESOLVED',
                          'failure_type':type(exc).__name__,'failure':str(exc)},allow_nan=False))
        raise
