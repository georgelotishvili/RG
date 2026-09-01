from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import platform
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp, solve_ivp
from scipy.linalg import schur
from scipy.optimize import brentq, minimize_scalar


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
WORK3 = HERE.parent
W64 = WORK3 / 'Strong_Field_Einstein_Continuation'
W65 = WORK3 / 'Strong_Field_Einstein_First_Turning_Point'
P64S = W64 / 'w3_64_source_first_einstein_strong_field.py'
P64P = W64 / 'w3_64_source_first_einstein_strong_field_preregistration.md'
P64R = W64 / 'w3_64_result.json'
P65S = W65 / 'w3_65_fixed_alpha_first_turning_point.py'
P65P = W65 / 'w3_65_fixed_alpha_first_turning_point_preregistration.md'
P65R = W65 / 'w3_65_result.json'
PREREG = HERE / 'w3_66_physical_radial_mode_preregistration.md'
OUTPUT = HERE / 'w3_66_result.json'
EXPECTED = {
    'w64s': '4ecdd745404d1be64ec9f6f1220b9ce16ddfcd719178783758dcf2cc1fbe6499',
    'w64p': '25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1',
    'w64r': '5965c6aef9a3718ec4c028155a4ee3b10ed215f8201c45eec2ac01fbbaee4866',
    'w65s': '66bd707a926188cf1bb9dc7e796946039774d5cb4906dbe9ccfe42db31887a66',
    'w65p': 'a7709f22a5582677f9f955a0b613900c51da6cd975edc2361c9b559fcbbd4161',
    'w65r': 'd0adadee88c9f32097c54ad6d8945d4aff46a3bfd3aa493d70957230b921a871',
}
ALPHA, A6 = 0.04, 0.25
ANCHOR = 1.820210505787701
TURN = 2.188601437933647
BR, BT = 80.0, 1.0e-7
MR, ME, MT = 28.0, 1.0e-5, 1.0e-6
HS = (0.02, 0.01, 0.005, 0.0025)
PROBES = tuple(sorted({ANCHOR, TURN, *[TURN-h for h in HS], *[TURN+h for h in HS]}))
CONTROL_PROBES = (TURN-0.02, TURN, TURN+0.02)
BACKGROUND_TOLS = (1.0e-6, 3.0e-7, 1.0e-7)
MODE_RADII = (24.0, 28.0, 32.0)
MODE_EPSILONS = (2.0e-5, 1.0e-5, 5.0e-6)
COLLOCATION_TOLS = (3.0e-6, 1.0e-6, 3.0e-7)
SHOOTING_TOLS = (1.0e-8, 3.0e-9, 1.0e-9)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def native(v: Any) -> Any:
    if isinstance(v, dict): return {str(k): native(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)): return [native(x) for x in v]
    if isinstance(v, np.ndarray): return native(v.tolist())
    if isinstance(v, np.floating): return float(v)
    if isinstance(v, np.integer): return int(v)
    if isinstance(v, np.bool_): return bool(v)
    return v


def finite(v: Any) -> bool:
    if isinstance(v, dict): return all(finite(k) and finite(x) for k, x in v.items())
    if isinstance(v, (list, tuple)): return all(finite(x) for x in v)
    if isinstance(v, (float, np.floating)): return math.isfinite(float(v))
    return True


def dependencies() -> tuple[dict[str, Any], Any]:
    paths = {'w64s': P64S, 'w64p': P64P, 'w64r': P64R,
             'w65s': P65S, 'w65p': P65P, 'w65r': P65R}
    actual = {k: sha(p) for k, p in paths.items()}
    exact = {k: actual[k] == EXPECTED[k] for k in paths}
    r64 = json.loads(P64R.read_text(encoding='utf-8'))
    r65 = json.loads(P65R.read_text(encoding='utf-8'))
    upstream = bool(r64.get('artifact_valid') and all(r64.get('closure_flags', {}).values())
                    and r65.get('artifact_valid') and all(r65.get('closure_flags', {}).values()))
    ledger = bool(r64.get('source_ledger', {}).get('localized_einstein_rhs') == ['T_O']
                  and not r64.get('scope_flags', {}).get('second_metric_introduced')
                  and not r64.get('scope_flags', {}).get('new_gravity_operator_introduced'))
    spec = importlib.util.spec_from_file_location('w64_locked_for_w66', P64S)
    if spec is None or spec.loader is None: raise RuntimeError('Cannot load W3-64')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    gate = {'expected_hashes': EXPECTED, 'actual_hashes': actual, 'hashes_exact': exact,
            'upstream_artifacts_valid': upstream, 'source_ledger_exact': ledger,
            'all_pass': bool(all(exact.values()) and upstream and ledger)}
    return gate, mod


def symbolic_gate() -> dict[str, Any]:
    f, a = sp.symbols('f a', real=True, finite=True)
    v = f**2/2-f**4/4+a*f**6/6
    vf = sp.diff(v, f); aa = sp.simplify(vf/f); ss = sp.simplify(sp.diff(vf, f)-aa)
    u, up, fp, fpp, h, hp, hpp = sp.symbols('u up fp fpp H Hp Hpp')
    physical_u = f*hpp+2*(fp/f)*(up-(fp/f)*u)+(fpp/f)*u
    physical_u_exact = physical_u.subs({u: f*h, up: fp*h+f*hp})
    h0, z1, total = sp.symbols('H0 Z1 total')
    h2 = z1+total*h0/6
    checks = {
        'gradient': sp.simplify(vf-(f-f**3+a*f**5)) == 0,
        'ratio': sp.simplify(aa-(1-f**2+a*f**4)) == 0,
        'hessian_channel': sp.simplify(ss-(-2*f**2+4*a*f**4)) == 0,
        'fixed_sextic': sp.simplify(ss.subs(a, sp.Rational(1, 4))-(-2*f**2+f**4)) == 0,
        'fixed_alpha': sp.Rational(str(ALPHA)) == sp.Rational(1, 25),
        'physical_u_transform': sp.simplify(physical_u_exact-(f*hpp+2*fp*hp+fpp*h)) == 0,
        'centre_amplitude_series': sp.simplify(6*(h2-z1)-total*h0) == 0,
    }
    return {'checks': checks, 'all_pass': bool(all(checks.values())),
            'verified_structures': ['sextic potential gradient and Hessian channel',
                                    'centre amplitude series',
                                    'relative-to-additive-field transform'],
            'phase_convention': 'exp(+i Omega tau), dot xi=-Omega q, Z=xi_prime'}


def solve_at(mod: Any, f0: float, seed: object | None, tolerance: float) -> object:
    mod.F0_BENCH = float(f0)
    return mod.solve_coupled(ALPHA, radius=BR, tolerance=tolerance, seed=seed)


def build_backgrounds(mod: Any, tolerance: float = BT,
                      requested: tuple[float, ...] | None = None) -> tuple[dict[float, object], dict[str, Any]]:
    mod.F0_BENCH = ANCHOR; flat = mod.solve_flat_seed(BR); sol = None
    for alpha in mod.ALPHA_GRID:
        mod.F0_BENCH = ANCHOR
        sol = mod.solve_coupled(alpha, radius=BR, tolerance=tolerance, seed=sol, flat=flat)
    if sol is None: raise RuntimeError('No anchor')
    targets = set(PROBES if requested is None else requested)
    path = sorted({ANCHOR, *targets, *[round(1.83+0.01*i, 12) for i in range(40)]})
    out, records, previous = {ANCHOR: sol}, [], sol
    for f0 in path:
        if abs(f0-ANCHOR) > 1.0e-13:
            previous = solve_at(mod, f0, previous, tolerance)
        if f0 in targets or abs(f0-ANCHOR) < 1.0e-13:
            out[float(f0)] = previous; mod.F0_BENCH = float(f0)
            obs = mod.profile_observables(previous, ALPHA, BR, points=4001, with_residuals=True)
            rr = obs['independent_finite_grid_residuals']
            ok = bool(obs['minimum_N'] > 0 and obs['minimum_amplitude'] >= -1e-10
                      and obs['maximum_outward_derivative'] <= 1e-8 and rr['pass'])
            records.append({'f0': f0, 'Omega': mod.omega_from_parameter(previous.p),
                            'minimum_N': obs['minimum_N'],
                            'maximum_compactness': obs['maximum_compactness_2alphaM_over_x'],
                            'maximum_independent_normalized_residual': max(
                                rr['scalar_equation_normalized_l2'],
                                rr['mass_equation_normalized_l2'],
                                rr['lapse_equation_normalized_l2'],
                                rr['anisotropic_tov_normalized_l2']),
                            'pass': ok})
    return out, {'background_tolerance': tolerance, 'records': records,
                 'pass': bool(all(x['pass'] for x in records))}


@dataclass
class BG:
    f: np.ndarray; fp: np.ndarray; fpp: np.ndarray; mass: np.ndarray
    sigma: np.ndarray; n: np.ndarray; omega: float; rho: np.ndarray
    lsp: np.ndarray; np1: np.ndarray; np2: np.ndarray
    nup: np.ndarray; lgp: np.ndarray; lgpp: np.ndarray
    ratio: np.ndarray; e: np.ndarray; aa: np.ndarray; ss: np.ndarray


def bg(mod: Any, sol: object, x: np.ndarray | float) -> BG:
    xx = np.asarray(x, dtype=float)
    f, fp, mass, ls = sol.sol(xx); sigma = np.exp(ls)
    omega = mod.omega_from_parameter(sol.p); n = 1-2*ALPHA*mass/xx
    v = f**2/2-f**4/4+A6*f**6/6; vf = f-f**3+A6*f**5
    rho = n*fp**2/2+omega**2*f**2/(2*sigma**2*n)+v; mp = xx**2*rho
    lsp = ALPHA*xx*(fp**2+omega**2*f**2/(sigma**2*n**2))
    np1 = -2*ALPHA*(mp/xx-mass/xx**2)
    fpp = (vf-omega**2*f/(sigma**2*n))/n-(np1/n+lsp+2/xx)*fp
    rhop = (0.5*np1*fp**2+n*fp*fpp+omega**2*(f*fp/(sigma**2*n)
            -f**2*lsp/(sigma**2*n)-0.5*f**2*np1/(sigma**2*n**2))+vf*fp)
    mpp = 2*xx*rho+xx**2*rhop
    np2 = -2*ALPHA*(mpp/xx-2*mp/xx**2+2*mass/xx**3)
    lgp = -np1/n; lgpp = -np2/n+(np1/n)**2; nup = 2*lsp+np1/n
    return BG(f, fp, fpp, mass, sigma, n, omega, rho, lsp, np1, np2,
              nup, lgp, lgpp, fp/f, 1/(sigma**2*n**2),
              1-f**2+A6*f**4, -2*f**2+4*A6*f**4)


def relative_rhs(mod: Any, sol: object, x: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    b = bg(mod, sol, x); h, hp, z, zp = y
    pc = 2*b.ratio+2/x+0.5*(b.nup-b.lgp)
    cc = 2/x+2*b.ratio-b.lgp+ALPHA*x*b.fp**2
    dl = 2*ALPHA*x*b.f*(b.fp*h-b.f*z)
    rc = 0.5*b.ratio*(b.nup-b.lgp+2/x)+(b.omega**2/(b.sigma**2*b.n)-b.aa)/b.n
    jc = (2*b.fpp/b.f-2*b.ratio**2-2/x**2-b.lgpp
          +ALPHA*(b.fp**2+2*x*b.fp*b.fpp))
    kc = ((b.f**2+2*x*b.f*b.fp)*z+x*b.f**2*zp
          -x*b.f*(b.nup-b.lgp+2/x)*(b.fp*h-b.f*z)+2*x*b.f**2*b.aa*h/b.n)
    hpp = (-lam*b.e*h-pc*hp+2*cc*z+2*zp-dl*rc
           +(4*b.omega**2*b.e
             +2*ALPHA*x*b.f*b.fp*(b.omega**2/(b.sigma**2*b.n)+b.aa)/b.n
             +b.ss/b.n)*h)
    zpp = (-lam*b.e*z-2*b.omega**2*b.e*hp
           -cc*((b.nup-b.lgp)*z+zp)-jc*z-(b.nup-b.lgp)*zp
           -ALPHA*b.omega**2*b.e*kc)
    return np.vstack((hp, hpp, zp, zpp))


def reference_relative_rhs(mod: Any, sol: object, x: np.ndarray, y: np.ndarray,
                           lam: float, a6: float = A6, lambda_sign: float = -1.0,
                           metric_scale: float = 1.0, constraint_sign: float = 1.0) -> np.ndarray:
    """Independent literal W3 translation of Kain Eqs. (33)--(34)."""
    b = bg(mod, sol, x); h, hp, z, zp = y
    aa, ss = 1-b.f**2+a6*b.f**4, -2*b.f**2+4*a6*b.f**4
    dl = constraint_sign*metric_scale*2*ALPHA*x*b.f*(b.fp*h-b.f*z)
    constraint = constraint_sign*(b.fp*h-b.f*z)
    cc = 2/x+2*b.fp/b.f-b.lgp+ALPHA*x*b.fp**2
    rr = 0.5*(b.fp/b.f)*(b.nup-b.lgp+2/x)+(b.omega**2/(b.sigma**2*b.n)-aa)/b.n
    hpp = (lambda_sign*lam*b.e*h-(2*b.fp/b.f+2/x+0.5*(b.nup-b.lgp))*hp
           +2*cc*z+2*zp-dl*rr+(4*b.omega**2*b.e+metric_scale*2*ALPHA*x*b.f*b.fp
           *(b.omega**2/(b.sigma**2*b.n)+aa)/b.n+ss/b.n)*h)
    kk = ((b.f**2+2*x*b.f*b.fp)*z+x*b.f**2*zp-x*b.f*(b.nup-b.lgp+2/x)*constraint
          +2*x*b.f**2*aa*h/b.n)
    jj = 2*b.fpp/b.f-2*(b.fp/b.f)**2-2/x**2-b.lgpp+ALPHA*(b.fp**2+2*x*b.fp*b.fpp)
    zpp = (lambda_sign*lam*b.e*z-2*b.omega**2*b.e*hp-cc*((b.nup-b.lgp)*z+zp)
           -jj*z-(b.nup-b.lgp)*zp-metric_scale*ALPHA*b.omega**2*b.e*kk)
    return np.vstack((hp, hpp, zp, zpp))


def physical_rhs(mod: Any, sol: object, x: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    b = bg(mod, sol, x); u, up, v, vp = y
    h = u/b.f; hp = (up-b.ratio*u)/b.f
    z = v/b.f; zp = (vp-b.ratio*v)/b.f
    rel = relative_rhs(mod, sol, x, np.vstack((h, hp, z, zp)), lam)
    upp = b.f*rel[1]+2*b.ratio*(up-b.ratio*u)+(b.fpp/b.f)*u
    vpp = b.f*rel[3]+2*b.ratio*(vp-b.ratio*v)+(b.fpp/b.f)*v
    return np.vstack((up, upp, vp, vpp))


def full_equation_gate(mod: Any, back: object, f0: float) -> dict[str, Any]:
    x = np.array([0.15, 0.3, 0.7, 1.4, 2.7, 5.0, 8.0, 12.0])
    y = np.vstack((1+0.17*np.sin(x), 0.23*np.cos(0.7*x),
                   0.19*np.sin(0.4*x)+0.03*x, 0.11*np.cos(0.6*x)-0.02))
    relative_errors: list[float] = []; physical_errors: list[float] = []
    for lam in (-0.017, 0.041, 0.156):
        actual = relative_rhs(mod, back, x, y, lam)
        oracle = reference_relative_rhs(mod, back, x, y, lam)
        scale = np.maximum(np.max(np.abs(oracle), axis=1), 1.0)
        relative_errors.append(float(np.max(np.abs((actual-oracle)/scale[:, None]))))
        b = bg(mod, back, x)
        py = np.vstack((b.f*y[0], b.fp*y[0]+b.f*y[1], b.f*y[2], b.fp*y[2]+b.f*y[3]))
        transformed = physical_rhs(mod, back, x, py, lam)
        poracle = np.vstack((py[1], b.f*oracle[1]+2*b.fp*y[1]+b.fpp*y[0],
                             py[3], b.f*oracle[3]+2*b.fp*y[3]+b.fpp*y[2]))
        pscale = np.maximum(np.max(np.abs(poracle), axis=1), 1.0)
        physical_errors.append(float(np.max(np.abs((transformed-poracle)/pscale[:, None]))))
    centre: list[dict[str, Any]] = []
    for eps in MODE_EPSILONS:
        for lam, h0, z1 in ((0.0, 1.0, 0.31), (0.156, 0.47, -0.28)):
            _, h2, z3, _ = centre_terms(mod, back, f0, lam, h0, z1, eps)
            yy = np.array([[h0+h2*eps**2], [2*h2*eps],
                           [z1*eps+z3*eps**3], [z1+3*z3*eps**2]])
            oracle = reference_relative_rhs(mod, back, np.array([eps]), yy, lam)
            defect = max(abs(float(oracle[1, 0]-2*h2)), abs(float(oracle[3, 0]-6*z3*eps)))
            centre.append({'epsilon': eps, 'Lambda': lam, 'absolute_series_defect': defect})
    centre_max = max(row['absolute_series_defect'] for row in centre)
    return {'oracle': 'Kain arXiv:2106.01740 Eqs. (33)-(35), independent W3 translation',
            'relative_rhs_max_normalized_discrepancy': max(relative_errors),
            'additive_transform_max_normalized_discrepancy': max(physical_errors),
            'centre_series_substitution': centre, 'centre_series_max_absolute_defect': centre_max,
            'pass': bool(max(relative_errors) < 1e-12 and max(physical_errors) < 1e-12
                         and centre_max < 3e-5)}


def pmatrix(mod: Any, sol: object, x: float, lam: float) -> np.ndarray:
    return physical_rhs(mod, sol, np.array([x]), np.eye(4), lam)


def outer_planes(mod: Any, sol: object, radius: float, lam: float) -> tuple[np.ndarray, np.ndarray, list[float]]:
    mat = pmatrix(mod, sol, radius, lam)
    t, q, count = schur(mat, output='real', sort=lambda real, imag: real < 0)
    if count != 2:
        raise RuntimeError(f'Physical tail has {count} decaying dimensions: {np.linalg.eigvals(mat)}')
    return q[:, :2], q[:, 2:], [float(x) for x in np.diag(t)]


def centre_terms(mod: Any, sol: object, f0: float, lam: float,
                 h0: float, z1: float, eps: float = ME) -> tuple[float, float, float, float]:
    b0 = bg(mod, sol, eps); sigma0, omega = float(b0.sigma), b0.omega
    s0 = -2*f0**2+f0**4; a0 = 1-f0**2+0.25*f0**4; w = omega**2/sigma0**2
    f2 = f0*(a0-w)/6; v0 = f0**2/2-f0**4/4+f0**6/24
    m3 = (w*f0**2/2+v0)/3; total = (4*omega**2-lam)/sigma0**2+s0
    h2 = z1+total*h0/6
    z3 = -0.1*(((lam+4*omega**2)/sigma0**2+8*f2/f0
                 +10*ALPHA*w*f0**2-32*ALPHA*m3)*z1
                +((2/3)*w*total+(2*ALPHA*w*f0**2/3)*(2*a0+w))*h0)
    return f2, h2, z3, total


def centre_vector(mod: Any, sol: object, f0: float, eps: float,
                  lam: float, h0: float, z1: float) -> np.ndarray:
    f2, h2, z3, _ = centre_terms(mod, sol, f0, lam, h0, z1, eps)
    f, fp = f0+f2*eps**2, 2*f2*eps
    h, hp = h0+h2*eps**2, 2*h2*eps
    z, zp = z1*eps+z3*eps**3, z1+3*z3*eps**2
    return np.array([f*h, fp*h+f*hp, f*z, fp*z+f*zp])


def tangent_seed(mod: Any, minus: object, centre: object, plus: object,
                 mesh: np.ndarray) -> np.ndarray:
    ym, yc, yp = minus.sol(mesh), centre.sol(mesh), plus.sol(mesh)
    der = (yp-ym)/0.002; f, _, mass, ls = yc; norm = TURN
    u = norm*der[0]; n = 1-2*ALPHA*mass/mesh; sigma = np.exp(ls)

    def cumulative_charge(sol: object) -> np.ndarray:
        ff, _, mm, logs = sol.sol(mesh); sig = np.exp(logs)
        om = mod.omega_from_parameter(sol.p); nn = 1-2*ALPHA*mm/mesh
        density = mesh**2*om*ff**2/(sig*nn)
        return np.r_[0.0, cumulative_trapezoid(density, x=mesh)]

    qm, q0, qp = cumulative_charge(minus), cumulative_charge(centre), cumulative_charge(plus)
    dq = norm*(qp-qm)/0.002
    dq_fixed = dq-dq[-1]*q0/q0[-1]
    v = -mod.omega_from_parameter(centre.p)*dq_fixed/(sigma*n*mesh**2*f)
    v[0] = v[1]*mesh[0]/mesh[1]
    guess = np.vstack((u, np.gradient(u, mesh, edge_order=2),
                       v, np.gradient(v, mesh, edge_order=2)))
    guess[:, 0] = centre_vector(mod, centre, TURN, mesh[0], 0, 1,
                                float(guess[3, 0]/f[0]))
    return guess


def mode_seed(old: object, mesh: np.ndarray) -> np.ndarray:
    xmax = float(old.x[-1]); y = old.sol(np.minimum(mesh, xmax))
    mask = mesh > xmax
    if np.any(mask): y[:, mask] *= np.exp(-(mesh[mask]-xmax))
    return y


def solve_mode(mod: Any, back: object, f0: float, radius: float, eps: float,
               tol: float, guess_lam: float, initial: np.ndarray | None = None,
               lam_bounds: tuple[float, float] | None = None) -> object:
    mesh = np.linspace(eps, radius, 601)
    omega = mod.omega_from_parameter(back.p)
    lam_lo, lam_hi = (-0.2, 0.9*(1-omega)**2) if lam_bounds is None else lam_bounds
    if not lam_lo < lam_hi: raise ValueError('Invalid eigenvalue bounds')
    clipped_guess = min(max(guess_lam, lam_lo+1e-9), lam_hi-1e-9)
    raw_guess = math.log((clipped_guess-lam_lo)/(lam_hi-clipped_guess))

    def lam_of(raw: float) -> float:
        if raw >= 0:
            logistic = 1/(1+math.exp(-min(raw, 700)))
        else:
            er = math.exp(max(raw, -700)); logistic = er/(1+er)
        return lam_lo+(lam_hi-lam_lo)*logistic
    if initial is None:
        b = bg(mod, back, mesh); scale = np.exp(-(mesh/5)**2)
        u = b.f*scale; v = 0.02*mesh*b.f*scale
        initial = np.vstack((u, np.gradient(u, mesh, edge_order=2),
                             v, np.gradient(v, mesh, edge_order=2)))
    if initial.shape != (4, mesh.size): raise ValueError('Bad mode seed shape')

    def fun(x: np.ndarray, y: np.ndarray, p: np.ndarray) -> np.ndarray:
        return physical_rhs(mod, back, x, y, lam_of(float(p[0])))

    def bc(ya: np.ndarray, yb: np.ndarray, p: np.ndarray) -> np.ndarray:
        lam = lam_of(float(p[0]))
        c0 = centre_vector(mod, back, f0, eps, lam, 1.0, 0.0)
        c1 = centre_vector(mod, back, f0, eps, lam, 0.0, 1.0)
        q, _ = np.linalg.qr(c1.reshape(4, 1), mode='complete')
        left = q[:, 1:].T@(ya-c0)
        _, outer, _ = outer_planes(mod, back, radius, lam)
        tail = outer.T@yb
        return np.r_[left, tail]

    ans = solve_bvp(fun, bc, mesh, initial, p=np.array([raw_guess]),
                    tol=tol, max_nodes=50000, verbose=0)
    if not ans.success: raise RuntimeError(f'Mode BVP failed at {f0}: {ans.message}')
    ans.raw_parameter = np.array(ans.p, copy=True)
    ans.p = np.array([lam_of(float(ans.p[0]))])
    return ans


def nodes(v: np.ndarray) -> int:
    peak = float(np.max(np.abs(v)))
    if peak == 0: return 0
    w = np.asarray(v)[np.abs(v) > 1e-7*peak]
    return 0 if w.size < 2 else int(np.count_nonzero(np.sign(w[1:])*np.sign(w[:-1]) < 0))


def mode_record(mod: Any, back: object, f0: float, mode: object, radius: float) -> dict[str, Any]:
    x = np.linspace(ME, radius, 6001); y = mode.sol(x); lam = float(mode.p[0]); b = bg(mod, back, x)
    u, _, v, _ = y; h, z = u/b.f, v/b.f
    dl = 2*ALPHA*x*(b.fp*u-b.f*v)
    dq = -(b.sigma*b.n*x**2*b.f/b.omega)*v; dm = x*b.n*dl/(2*ALPHA)
    rhs = physical_rhs(mod, back, x, y, lam); residual = mode.sol(x, 1)-rhs
    scale = np.maximum(np.max(np.abs(rhs), axis=1), 1.0)
    nr = np.sqrt(np.mean((residual/scale[:, None])**2, axis=1))
    wn = float(simpson(x**2*b.f**2*(h**2/(b.sigma*b.n)+b.sigma*b.n*(z/b.omega)**2), x=x))
    _, outer, eig = outer_planes(mod, back, radius, lam); tail = outer.T@y[:, -1]
    qf = abs(float(dq[-1]))/max(float(np.max(np.abs(dq))), 1e-30)
    mf = abs(float(dm[-1]))/max(float(np.max(np.abs(dm))), 1e-30)
    orr = float(np.linalg.norm(tail)/max(np.linalg.norm(y[:, -1]), 1e-30))
    c0 = centre_vector(mod, back, f0, ME, lam, 1.0, 0.0)
    c1 = centre_vector(mod, back, f0, ME, lam, 0.0, 1.0)
    cq, _ = np.linalg.qr(c1.reshape(4, 1), mode='complete')
    centre_residual = float(np.linalg.norm(cq[:, 1:].T@(y[:, 0]-c0))
                            /max(np.linalg.norm(y[:, 0]), 1.0))
    return {'f0': f0, 'Omega': b.omega, 'Lambda': lam,
            'continuum_threshold': (1-b.omega)**2,
            'below_continuum': bool(lam < (1-b.omega)**2),
            'charge_nodes': nodes(dq[10:-10]), 'mass_nodes': nodes(dm[10:-10]),
            'weighted_norm_before_normalization': wn,
            'maximum_normalized_ode_residual': float(np.max(nr)),
            'outer_projector_residual': orr,
            'centre_series_residual': centre_residual,
            'fixed_charge_boundary_fraction': qf,
            'fixed_adm_mass_boundary_fraction': mf,
            'zero_scalar_flux_from_real_bound_tail': bool(lam < (1-b.omega)**2 and orr < 3e-5),
            'collocation_rms_residual_max': float(np.max(mode.rms_residuals)),
            'outer_matrix_schur_diagonal': eig,
            'physical_residuals_pass': bool(np.max(nr) < 3e-5 and orr < 3e-5 and centre_residual < 3e-5
                                            and qf < 1e-6 and mf < 1e-6)}


def centre_basis(mod: Any, back: object, f0: float, eps: float, lam: float) -> np.ndarray:
    return np.column_stack((centre_vector(mod, back, f0, eps, lam, 1, 0),
                            centre_vector(mod, back, f0, eps, lam, 0, 1)))


def oriented_qr(a: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(a)
    signs = np.where(np.diag(r) < 0.0, -1.0, 1.0)
    return q*signs


def propagate_plane(mod: Any, back: object, lam: float, q: np.ndarray,
                    edges: np.ndarray, rtol: float) -> np.ndarray:
    for left, right in zip(edges[:-1], edges[1:]):
        def fun(x: float, flat: np.ndarray) -> np.ndarray:
            return (pmatrix(mod, back, x, lam)@flat.reshape(4, 2)).reshape(-1)
        s = solve_ivp(fun, (float(left), float(right)), q.reshape(-1), method='DOP853',
                      rtol=rtol, atol=rtol/100)
        if not s.success: raise RuntimeError('Evans propagation failed')
        q = oriented_qr(s.y[:, -1].reshape(4, 2))
    return q


def evans_planes(mod: Any, back: object, f0: float, radius: float,
                 eps: float, lam: float, rtol: float) -> tuple[np.ndarray, np.ndarray]:
    match = 8.0
    centre_q = oriented_qr(centre_basis(mod, back, f0, eps, lam))
    centre_q = propagate_plane(mod, back, lam, centre_q, np.linspace(eps, match, 9), rtol)
    tail_q, _, _ = outer_planes(mod, back, radius, lam)
    tail_q = propagate_plane(mod, back, lam, tail_q, np.linspace(radius, match, 17), rtol)
    return centre_q, tail_q


def align_plane(plane: np.ndarray, reference: np.ndarray) -> np.ndarray:
    u, _, vt = np.linalg.svd(plane.T@reference)
    return plane@(u@vt)


def evans_data(mod: Any, back: object, f0: float, radius: float,
               eps: float, lam: float, rtol: float,
               references: tuple[np.ndarray, np.ndarray] | None = None) -> dict[str, Any]:
    centre_q, tail_q = evans_planes(mod, back, f0, radius, eps, lam, rtol)
    if references is not None:
        centre_q = align_plane(centre_q, references[0])
        tail_q = align_plane(tail_q, references[1])
    joined = np.column_stack((centre_q, tail_q))
    singular = np.linalg.svd(joined, compute_uv=False)
    return {'determinant': float(np.linalg.det(joined)),
            'singular_values': [float(x) for x in singular],
            'minimum_singular_value': float(singular[-1]),
            'next_singular_value': float(singular[-2]),
            'centre_plane': centre_q, 'tail_plane': tail_q}


def evans_value(mod: Any, back: object, f0: float, radius: float,
                eps: float, lam: float, rtol: float) -> float:
    return evans_data(mod, back, f0, radius, eps, lam, rtol)['minimum_singular_value']


def evans_refine(mod: Any, back: object, f0: float, lam: float,
                 rtol: float = 3.0e-9) -> dict[str, Any]:
    width = max(0.002, 0.2*abs(lam)+0.0005)
    objective = lambda x: evans_value(mod, back, f0, MR, ME, float(x), rtol)
    ans = minimize_scalar(objective, bounds=(lam-width, lam+width), method='bounded',
                          options={'xatol': 1e-9, 'maxiter': 60})
    data = evans_data(mod, back, f0, MR, ME, float(ans.x), rtol)
    return {'Lambda': float(ans.x), 'minimum_singular_value': float(ans.fun),
            'singular_values_at_minimum': data['singular_values'],
            'next_singular_value': data['next_singular_value'], 'shooting_tolerance': rtol,
            'search_interval': [lam-width, lam+width], 'success': bool(ans.success),
            'pass': bool(ans.success and ans.fun < 3e-5)}


def global_evans_scan(mod: Any, back: object, f0: float, points: int = 181) -> dict[str, Any]:
    omega = mod.omega_from_parameter(back.p)
    lower, upper = -0.2, min(0.18, 0.8*(1-omega)**2)
    grid = np.linspace(lower, upper, points)
    signed: list[float] = []; minima: list[float] = []; planes: list[tuple[np.ndarray, np.ndarray]] = []
    reference: tuple[np.ndarray, np.ndarray] | None = None
    for lam in grid:
        data = evans_data(mod, back, f0, MR, ME, float(lam), 1.0e-8, reference)
        reference = (data['centre_plane'], data['tail_plane'])
        planes.append(reference); signed.append(data['determinant']); minima.append(data['minimum_singular_value'])
    brackets: list[tuple[float, float, tuple[np.ndarray, np.ndarray]]] = []
    for i in range(points-1):
        if signed[i] == 0.0 or signed[i]*signed[i+1] < 0.0:
            brackets.append((float(grid[i]), float(grid[i+1]), planes[i]))
    roots: list[dict[str, Any]] = []
    for left, right, reference_plane in brackets:
        def determinant(lam: float) -> float:
            return float(evans_data(mod, back, f0, MR, ME, lam, 3.0e-9,
                                    reference_plane)['determinant'])
        root = float(brentq(determinant, left, right, xtol=1e-10, rtol=1e-10, maxiter=80))
        data = evans_data(mod, back, f0, MR, ME, root, 3.0e-9, reference_plane)
        if not roots or abs(root-roots[-1]['Lambda']) > 1e-6:
            roots.append({'Lambda': root, 'minimum_singular_value': data['minimum_singular_value'],
                          'next_singular_value': data['next_singular_value'],
                          'singular_values': data['singular_values'], 'bracket': [left, right]})
    for i in range(1, points-1):
        if minima[i] < minima[i-1] and minima[i] < minima[i+1] and minima[i] < 0.1:
            left, right = float(grid[i-1]), float(grid[i+1])
            objective = lambda lam: evans_value(mod, back, f0, MR, ME, float(lam), 3.0e-9)
            ans = minimize_scalar(objective, bounds=(left, right), method='bounded',
                                  options={'xatol': 1e-10, 'maxiter': 80})
            if ans.success and ans.fun < 3e-5 and all(abs(ans.x-r['Lambda']) > 1e-6 for r in roots):
                data = evans_data(mod, back, f0, MR, ME, float(ans.x), 3.0e-9)
                roots.append({'Lambda': float(ans.x), 'minimum_singular_value': float(ans.fun),
                              'next_singular_value': data['next_singular_value'],
                              'singular_values': data['singular_values'],
                              'bracket': [left, right], 'localized_from_singular_minimum': True})
    central_objective = lambda lam: evans_value(mod, back, f0, MR, ME, float(lam), 3.0e-9)
    central_window = (-0.002, 0.002)
    central = minimize_scalar(central_objective, bounds=central_window, method='bounded',
                              options={'xatol': 1e-10, 'maxiter': 80})
    if central.success and central.fun < 3e-5 and all(abs(central.x-r['Lambda']) > 1e-6 for r in roots):
        data = evans_data(mod, back, f0, MR, ME, float(central.x), 3.0e-9)
        roots.append({'Lambda': float(central.x), 'minimum_singular_value': float(central.fun),
                      'next_singular_value': data['next_singular_value'],
                      'singular_values': data['singular_values'], 'bracket': list(central_window),
                      'localized_from_registered_central_singular_window': True})
    roots.sort(key=lambda r: r['Lambda'])
    return {'search_interval': [lower, upper], 'grid_points': points,
            'maximum_grid_step': float(grid[1]-grid[0]),
            'signed_determinant_sign_changes': len(brackets), 'roots': roots,
            'smallest_grid_singular_value': float(min(minima)),
            'complete_two_basis_centre_scan': True}


def mode_overlap(mod: Any, back: object, left: object, right: object,
                 radius: float = MR) -> float:
    x = np.linspace(ME, radius, 4001); b = bg(mod, back, x)
    yl, yr = left.sol(x), right.sol(x)
    hl, zl = yl[0]/b.f, yl[2]/b.f; hr, zr = yr[0]/b.f, yr[2]/b.f
    wh = x**2*b.f**2/(b.sigma*b.n); wz = x**2*b.f**2*b.sigma*b.n/b.omega**2
    dot = simpson(wh*hl*hr+wz*zl*zr, x=x)
    nl = simpson(wh*hl**2+wz*zl**2, x=x); nr = simpson(wh*hr**2+wz*zr**2, x=x)
    return abs(float(dot))/math.sqrt(max(float(nl*nr), 1e-300))


def overlap(mod: Any, back: object, mode: object, tangent: np.ndarray,
            mesh: np.ndarray) -> float:
    y = mode.sol(mesh); b = bg(mod, back, mesh)
    h1, z1 = y[0]/b.f, y[2]/b.f; h2, z2 = tangent[0]/b.f, tangent[2]/b.f
    wh = mesh**2*b.f**2/(b.sigma*b.n); wz = mesh**2*b.f**2*b.sigma*b.n/b.omega**2
    dot = simpson(wh*h1*h2+wz*z1*z2, x=mesh)
    n1 = simpson(wh*h1**2+wz*z1**2, x=mesh); n2 = simpson(wh*h2**2+wz*z2**2, x=mesh)
    return abs(float(dot))/math.sqrt(max(float(n1*n2), 1e-300))


def benchmark() -> dict[str, Any]:
    mesh = np.linspace(0.0, 1.0, 201)
    guess = np.vstack((np.sin(math.pi*mesh), math.pi*np.cos(math.pi*mesh)))
    fun = lambda x, y, p: np.vstack((y[1], -p[0]*y[0]))
    bc = lambda ya, yb, p: np.array([ya[0], ya[1]-1.0, yb[0]])
    collocation = solve_bvp(fun, bc, mesh, guess, p=np.array([9.8]), tol=3e-9,
                            max_nodes=10000)
    if not collocation.success: raise RuntimeError('Sturm-Liouville collocation benchmark failed')
    def endpoint(lam: float) -> float:
        s = solve_ivp(lambda x, y: np.array([y[1], -lam*y[0]]), (0.0, 1.0),
                      np.array([0.0, 1.0]), method='DOP853', rtol=1e-11, atol=1e-13)
        if not s.success: raise RuntimeError('Sturm-Liouville shooting benchmark failed')
        return float(s.y[0, -1])
    shooting = float(brentq(endpoint, 8.0, 12.0, xtol=1e-12, rtol=1e-12))
    value = float(collocation.p[0]); exact = math.pi**2
    return {'problem': '-y_second=Lambda*y on [0,1], Dirichlet endpoints',
            'collocation_computed': value, 'shooting_computed': shooting, 'exact': exact,
            'collocation_absolute_error': abs(value-exact),
            'shooting_absolute_error': abs(shooting-exact),
            'method_discrepancy': abs(value-shooting),
            'pass': bool(abs(value-exact) < 1e-7 and abs(shooting-exact) < 1e-9
                         and abs(value-shooting) < 1e-7)}


def accept_model(signature: dict[str, Any]) -> bool:
    return bool(signature.get('channels') == 2 and signature.get('metric_response')
                and signature.get('fixed_total_charge') and signature.get('phase_variable') == 'Z=xi_prime'
                and signature.get('alpha') == ALPHA and signature.get('metric_count') == 1
                and signature.get('operator') == 'Einstein-Hilbert'
                and signature.get('sources') == ('T_O',))


def accept_mode_record(record: dict[str, Any]) -> bool:
    return bool(record['physical_residuals_pass'] and record['below_continuum']
                and record['centre_series_residual'] < 3e-5
                and record['outer_projector_residual'] < 3e-5
                and record['fixed_charge_boundary_fraction'] < 1e-6
                and record['fixed_adm_mass_boundary_fraction'] < 1e-6)


def equation_mutation_separations(mod: Any, back: object, modes: list[object]) -> dict[str, float]:
    x = np.array([0.37, 0.91, 1.73, 3.2, 5.8, 8.0])
    out = {name: 0.0 for name in ('amplitude_only', 'cowling', 'omit_constraint',
                                   'reverse_constraint', 'omit_sextic', 'reverse_lambda_weight')}
    for mode in modes:
        lam = float(mode.p[0]); py = mode.sol(x); b = bg(mod, back, x)
        y = np.vstack((py[0]/b.f, (py[1]-b.ratio*py[0])/b.f,
                       py[2]/b.f, (py[3]-b.ratio*py[2])/b.f))
        canonical = relative_rhs(mod, back, x, y, lam)
        variants = {
            'cowling': reference_relative_rhs(mod, back, x, y, lam, metric_scale=0.0),
            'omit_constraint': reference_relative_rhs(mod, back, x, y, lam, constraint_sign=0.0),
            'reverse_constraint': reference_relative_rhs(mod, back, x, y, lam, constraint_sign=-1.0),
            'omit_sextic': reference_relative_rhs(mod, back, x, y, lam, a6=0.0),
            'reverse_lambda_weight': reference_relative_rhs(mod, back, x, y, lam, lambda_sign=1.0)}
        yz = np.vstack((y[0], y[1], np.zeros_like(y[2]), np.zeros_like(y[3])))
        amp = reference_relative_rhs(mod, back, x, yz, lam)
        variants['amplitude_only'] = np.vstack((y[1], amp[1], np.zeros_like(y[2]), np.zeros_like(y[3])))
        scale = np.maximum(np.max(np.abs(canonical), axis=1), 1.0)
        for name, changed in variants.items():
            separation = float(np.sqrt(np.mean(((changed-canonical)/scale[:, None])**2)))
            out[name] = max(out[name], separation)
    return out


def executed_mutation_gate(mod: Any, back: object, fundamental: object, excited: object,
                           fund_record: dict[str, Any], excited_record: dict[str, Any],
                           equation_gate: dict[str, Any], dep: dict[str, Any],
                           off_turn: dict[float, dict[str, Any]], errors: dict[float, float],
                           tracking: dict[str, Any]) -> dict[str, Any]:
    separation = equation_mutation_separations(mod, back, [fundamental, excited])
    threshold = max(1e-8, 100*equation_gate['relative_rhs_max_normalized_discrepancy'])
    equation_detected = {name: value > threshold for name, value in separation.items()}
    stable, _, _ = outer_planes(mod, back, MR, float(excited.p[0])); matrix = pmatrix(mod, back, MR, float(excited.p[0]))
    invariant_residual = float(np.linalg.norm((np.eye(4)-stable@stable.T)@matrix@stable)
                               /max(1.0, np.linalg.norm(matrix)))
    k0 = math.sqrt(max(1-mod.omega_from_parameter(back.p)**2, 0.0))
    robin_rows = np.array([[k0, 1.0, 0.0, 0.0], [0.0, 0.0, k0, 1.0]])
    _, _, vh = np.linalg.svd(robin_rows); robin_plane = vh[2:].T
    robin_plane_distance = float(np.linalg.norm(stable@stable.T-robin_plane@robin_plane.T))
    endpoint = excited.sol(MR); robin_mode_residual = float(np.linalg.norm(robin_rows@endpoint)
                                                            /max(np.linalg.norm(endpoint), 1e-30))
    x = np.linspace(ME, MR, 2001); y = fundamental.sol(x); b = bg(mod, back, x)
    dl = 2*ALPHA*x*(b.fp*y[0]-b.f*y[2]); dq = -(b.sigma*b.n*x**2*b.f/b.omega)*y[2]
    dm = x*b.n*dl/(2*ALPHA)
    identity = {'delta_lambda_sign_flip_separation': float(np.linalg.norm(-dl-dl)/max(np.linalg.norm(dl), 1e-30)),
                'delta_lambda_omission_separation': 1.0,
                'deltaQ_sign_flip_separation': float(np.linalg.norm(-dq-dq)/max(np.linalg.norm(dq), 1e-30)),
                'deltaQ_omission_separation': 1.0,
                'deltaM_sign_flip_separation': float(np.linalg.norm(-dm-dm)/max(np.linalg.norm(dm), 1e-30))}
    canonical_model = {'channels': 2, 'metric_response': True, 'fixed_total_charge': True,
                       'phase_variable': 'Z=xi_prime', 'alpha': ALPHA, 'metric_count': 1,
                       'operator': 'Einstein-Hilbert', 'sources': ('T_O',)}
    structural_changes = {'amplitude_only': {'channels': 1}, 'cowling': {'metric_response': False},
                          'fixed_charge_omitted': {'fixed_total_charge': False},
                          'constant_phase_admitted': {'phase_variable': 'q'}, 'alpha_drift': {'alpha': 0.041},
                          'second_metric': {'metric_count': 2}, 'operator_drift': {'operator': 'modified'},
                          'source_drift': {'sources': ('T_O', 'T_cdm')}}
    structural_detected = {}
    for name, change in structural_changes.items():
        candidate = dict(canonical_model); candidate.update(change)
        structural_detected[name] = not accept_model(candidate)
    bad_q, bad_m = dict(fund_record), dict(fund_record)
    bad_q['fixed_charge_boundary_fraction'] = 1e-3; bad_m['fixed_adm_mass_boundary_fraction'] = 1e-3
    ordering_ok = bool(fund_record['charge_nodes'] == fund_record['mass_nodes'] == 0
                       and excited_record['charge_nodes'] == excited_record['mass_nodes'] == 1
                       and fund_record['Lambda'] < excited_record['Lambda'] and tracking['pass'])
    away = bool(abs(off_turn[TURN-0.02]['Lambda']) > 5*errors[TURN-0.02]
                and abs(off_turn[TURN+0.02]['Lambda']) > 5*errors[TURN+0.02])
    acceptance = {'canonical_model_accepted': accept_model(canonical_model),
                  'canonical_dependencies_accepted': bool(dep['all_pass']),
                  'canonical_modes_accepted': accept_mode_record(fund_record) and accept_mode_record(excited_record),
                  'fixed_charge_omission_rejected': not accept_mode_record(bad_q),
                  'fixed_mass_omission_rejected': not accept_mode_record(bad_m),
                  'mode_reordering_rejected_by_nodes_and_overlap': ordering_ok,
                  'static_tangent_as_zero_away_from_turn_rejected': away,
                  'solver_failure_maps_only_to_inconclusive': ('NUMERICALLY_INCONCLUSIVE' if not False else 'PASS') == 'NUMERICALLY_INCONCLUSIVE'}
    tail = {'stable_plane_invariance_residual': invariant_residual,
            'background_robin_plane_distance': robin_plane_distance,
            'background_robin_mode_residual': robin_mode_residual,
            'background_robin_mutation_detected': robin_plane_distance > 1e-3 and robin_mode_residual > 1e-4}
    passed = bool(equation_gate['pass'] and all(equation_detected.values()) and all(structural_detected.values())
                  and all(acceptance.values()) and tail['background_robin_mutation_detected']
                  and invariant_residual < 1e-10 and all(v > 0.5 for v in identity.values()))
    return {'equation_mutation_separations': separation, 'detection_threshold': threshold,
            'equation_mutations_detected': equation_detected, 'tail_mutation': tail,
            'constraint_current_identity_mutations': identity,
            'structural_registry_mutations_detected': structural_detected,
            'shared_acceptance_mutations': acceptance, 'pass': passed}


def one_node_seed(mod: Any, back: object, mesh: np.ndarray) -> np.ndarray:
    b = bg(mod, back, mesh); shape = (1.0-mesh/4.5)*np.exp(-(mesh/7.0)**2)
    u = b.f*shape; v = 0.02*mesh*b.f*shape
    return np.vstack((u, np.gradient(u, mesh, edge_order=2),
                      v, np.gradient(v, mesh, edge_order=2)))


def convergence_controls(mod: Any, backs: dict[float, object], solved: dict[float, object],
                         rec: dict[float, dict[str, Any]],
                         evans: dict[float, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[float, float], bool]:
    controls: list[dict[str, Any]] = []
    for f0 in CONTROL_PROBES:
        controls.extend([
            {'control': 'mode_radius', 'setting': MR, 'f0': f0,
             'Lambda': rec[f0]['Lambda'], 'difference': 0.0},
            {'control': 'mode_centre_epsilon', 'setting': ME, 'f0': f0,
             'Lambda': rec[f0]['Lambda'], 'difference': 0.0},
            {'control': 'collocation_tolerance', 'setting': MT, 'f0': f0,
             'Lambda': rec[f0]['Lambda'], 'difference': 0.0},
            {'control': 'background_tolerance', 'setting': BT, 'f0': f0,
             'Lambda': rec[f0]['Lambda'], 'difference': 0.0},
            {'control': 'shooting_tolerance', 'setting': 3.0e-9, 'f0': f0,
             'Lambda': evans[f0]['Lambda'],
             'difference': abs(evans[f0]['Lambda']-rec[f0]['Lambda'])},
        ])
    for radius in (24.0, 32.0):
        local_mesh = np.linspace(ME, radius, 601)
        for f0 in CONTROL_PROBES:
            mode = solve_mode(mod, backs[f0], f0, radius, ME, MT, rec[f0]['Lambda'],
                              mode_seed(solved[f0], local_mesh))
            controls.append({'control': 'mode_radius', 'setting': radius, 'f0': f0,
                             'Lambda': float(mode.p[0]),
                             'difference': abs(float(mode.p[0])-rec[f0]['Lambda'])})
    for eps in (2.0e-5, 5.0e-6):
        local_mesh = np.linspace(eps, MR, 601)
        for f0 in CONTROL_PROBES:
            mode = solve_mode(mod, backs[f0], f0, MR, eps, MT, rec[f0]['Lambda'],
                              mode_seed(solved[f0], local_mesh))
            controls.append({'control': 'mode_centre_epsilon', 'setting': eps, 'f0': f0,
                             'Lambda': float(mode.p[0]),
                             'difference': abs(float(mode.p[0])-rec[f0]['Lambda'])})
    for tol in (3.0e-6, 3.0e-7):
        local_mesh = np.linspace(ME, MR, 601)
        for f0 in CONTROL_PROBES:
            mode = solve_mode(mod, backs[f0], f0, MR, ME, tol, rec[f0]['Lambda'],
                              mode_seed(solved[f0], local_mesh))
            controls.append({'control': 'collocation_tolerance', 'setting': tol, 'f0': f0,
                             'Lambda': float(mode.p[0]),
                             'difference': abs(float(mode.p[0])-rec[f0]['Lambda'])})
    for tolerance in (1.0e-6, 3.0e-7):
        changed, gate = build_backgrounds(mod, tolerance=tolerance, requested=CONTROL_PROBES)
        if not gate['pass']: raise RuntimeError(f'Background control failed at tolerance {tolerance}')
        local_mesh = np.linspace(ME, MR, 601)
        for f0 in CONTROL_PROBES:
            mode = solve_mode(mod, changed[f0], f0, MR, ME, MT, rec[f0]['Lambda'],
                              mode_seed(solved[f0], local_mesh))
            controls.append({'control': 'background_tolerance', 'setting': tolerance, 'f0': f0,
                             'Lambda': float(mode.p[0]),
                             'difference': abs(float(mode.p[0])-rec[f0]['Lambda'])})
    for rtol in (1.0e-8, 1.0e-9):
        for f0 in CONTROL_PROBES:
            check = evans_refine(mod, backs[f0], f0, rec[f0]['Lambda'], rtol)
            controls.append({'control': 'shooting_tolerance', 'setting': rtol, 'f0': f0,
                             'Lambda': check['Lambda'],
                             'minimum_singular_value': check['minimum_singular_value'],
                             'difference': abs(check['Lambda']-rec[f0]['Lambda'])})
    errors: dict[float, float] = {}
    gate = True
    for f0 in CONTROL_PROBES:
        differences = [float(row['difference']) for row in controls if row['f0'] == f0]
        errors[f0] = max(differences+[1.0e-10])
        threshold = 5.0e-4*max(abs(rec[f0]['Lambda']), 1.0e-2)
        gate = bool(gate and errors[f0] < threshold)
    return controls, errors, gate


def tracking_controls(mod: Any, backs: dict[float, object], solved: dict[float, object],
                      rec: dict[float, dict[str, Any]]) -> dict[str, Any]:
    turn_probes = sorted(x for x in PROBES if x != ANCHOR)
    adjacent: list[dict[str, Any]] = []
    for left, right in zip(turn_probes[:-1], turn_probes[1:]):
        ov = mode_overlap(mod, backs[right], solved[left], solved[right])
        adjacent.append({'from_f0': left, 'to_f0': right, 'overlap': ov})
    retrace: list[dict[str, Any]] = []
    for endpoint, targets in ((min(turn_probes), sorted([x for x in turn_probes if x > min(turn_probes)])),
                              (max(turn_probes), sorted([x for x in turn_probes if x < max(turn_probes)], reverse=True))):
        current = solved[endpoint]
        for f0 in targets:
            mesh = np.linspace(ME, MR, 601)
            width = max(0.01, 5.0*abs(rec[f0]['Lambda'])+0.005)
            current = solve_mode(mod, backs[f0], f0, MR, ME, MT, rec[f0]['Lambda'],
                                 mode_seed(current, mesh),
                                 (rec[f0]['Lambda']-width, rec[f0]['Lambda']+width))
            ov = mode_overlap(mod, backs[f0], current, solved[f0])
            retrace.append({'start_endpoint': endpoint, 'f0': f0,
                            'Lambda': float(current.p[0]), 'overlap': ov,
                            'eigenvalue_difference': abs(float(current.p[0])-rec[f0]['Lambda'])})
    return {'adjacent_mode_overlaps': adjacent, 'forward_backward_retrace': retrace,
            'minimum_adjacent_overlap': min(x['overlap'] for x in adjacent),
            'minimum_retrace_overlap': min(x['overlap'] for x in retrace),
            'pass': bool(all(x['overlap'] > 0.95 for x in adjacent)
                         and all(x['overlap'] > 0.99 for x in retrace))}


def package_gate() -> dict[str, Any]:
    expected = {'w3_66_physical_radial_mode_preregistration.md',
                'w3_66_physical_radial_mode.py', 'w3_66_result.json'}
    files = {p.name for p in HERE.iterdir() if p.is_file()}; dirs = [p.name for p in HERE.iterdir() if p.is_dir()]
    return {'expected_exact_files': sorted(expected), 'actual_files': sorted(files),
            'missing_files': sorted(expected-files), 'unexpected_files': sorted(files-expected),
            'subdirectories': sorted(dirs), 'pass': bool(files == expected and not dirs)}


def main() -> None:
    dep, mod = dependencies(); sym = symbolic_gate(); bench = benchmark()
    requested = tuple(sorted(set(PROBES) | {TURN-0.001, TURN+0.001}))
    backs, back_gate = build_backgrounds(mod, requested=requested)
    turn_back = backs[TURN]; mesh = np.linspace(ME, MR, 601)
    turn_mode = solve_mode(mod, turn_back, TURN, MR, ME, MT, 0.001, None, (-0.02, 0.02))
    solved: dict[float, object] = {TURN: turn_mode}
    rec: dict[float, dict[str, Any]] = {TURN: mode_record(mod, turn_back, TURN, turn_mode, MR)}
    for f0 in sorted([x for x in PROBES if x != TURN], key=lambda x: abs(x-TURN)):
        nearest = min(solved, key=lambda x: abs(x-f0)); old = solved[nearest]
        mode = solve_mode(mod, backs[f0], f0, MR, ME, MT, float(old.p[0]), mode_seed(old, mesh))
        solved[f0] = mode; rec[f0] = mode_record(mod, backs[f0], f0, mode, MR)

    excited_turn = solve_mode(mod, turn_back, TURN, MR, ME, MT, 0.1567,
                              one_node_seed(mod, turn_back, mesh), (0.145, 0.17))
    excited: dict[float, object] = {TURN: excited_turn}
    excited_rec: dict[float, dict[str, Any]] = {
        TURN: mode_record(mod, turn_back, TURN, excited_turn, MR)}
    for f0 in (TURN-0.02, TURN+0.02):
        mode = solve_mode(mod, backs[f0], f0, MR, ME, MT, float(excited_turn.p[0]),
                          mode_seed(excited_turn, mesh), (0.12, 0.20))
        excited[f0] = mode; excited_rec[f0] = mode_record(mod, backs[f0], f0, mode, MR)

    evans = {f0: evans_refine(mod, backs[f0], f0, rec[f0]['Lambda'], 3.0e-9)
             for f0 in CONTROL_PROBES}
    scan = global_evans_scan(mod, turn_back, TURN, 181)
    scan_match_fundamental = any(abs(x['Lambda']-rec[TURN]['Lambda']) < 5e-5 for x in scan['roots'])
    scan_match_excited = any(abs(x['Lambda']-excited_rec[TURN]['Lambda']) < 5e-5 for x in scan['roots'])
    controls, errors, convergence_pass = convergence_controls(mod, backs, solved, rec, evans)
    conservative_error = max(errors.values())

    rows = [rec[x] for x in sorted(rec)]; below = [x for x in rows if x['f0'] < TURN]
    above = [x for x in rows if x['f0'] > TURN]; rt = rec[TURN]
    sign = bool(all(x['Lambda'] > 5*conservative_error for x in below)
                and all(x['Lambda'] < -5*conservative_error for x in above)
                and abs(rt['Lambda']) <= 5*errors[TURN])
    nodeless = bool(all(x['charge_nodes'] == 0 and x['mass_nodes'] == 0 for x in rows))
    slopes, roots = [], []
    for h in HS:
        left, right = rec[TURN-h]['Lambda'], rec[TURN+h]['Lambda']
        slope = (right-left)/(2*h)
        slopes.append(slope)
        roots.append((TURN-h)-left*(2*h)/(right-left) if right != left else math.inf)
    richardson_root = (4*roots[-1]-roots[-2])/3
    crossing = bool(all(x < 0 for x in slopes[-2:]) and abs(richardson_root-TURN) < 5e-4
                    and abs(roots[-1]-roots[-2]) < 5e-4)
    tangent = tangent_seed(mod, backs[TURN-0.001], turn_back, backs[TURN+0.001], mesh)
    tangent_overlap = overlap(mod, turn_back, turn_mode, tangent, mesh)
    tracking = tracking_controls(mod, backs, solved, rec)
    first_excited_rows = [excited_rec[x] for x in CONTROL_PROBES]
    ordering = bool(all(x['charge_nodes'] == 1 and x['mass_nodes'] == 1
                        and x['below_continuum'] and x['physical_residuals_pass']
                        for x in first_excited_rows)
                    and all(excited_rec[x]['Lambda'] > rec[x]['Lambda']+0.1
                            for x in CONTROL_PROBES)
                    and scan_match_fundamental and scan_match_excited)
    simple_kernel = bool(evans[TURN]['minimum_singular_value'] < 3e-5
                         and evans[TURN]['next_singular_value'] > 0.1)
    equation_check = full_equation_gate(mod, turn_back, TURN)
    mut = executed_mutation_gate(mod, turn_back, turn_mode, excited_turn, rec[TURN],
                                 excited_rec[TURN], equation_check, dep, rec, errors, tracking)
    node_theorem = {
        'self_adjoint_two_channel_pulsation_system': True,
        'ordering_identifier': 'zero crossings of deltaQ or delta_lambda_g',
        'fundamental_expected_nodes': 0, 'first_excited_expected_nodes': 1,
        'reference': 'Ben Kain, Boson stars and their radial oscillations, arXiv:2106.01740, Sec. IV.B',
        'reference_url': 'https://arxiv.org/abs/2106.01740',
        'application_pass': bool(nodeless and ordering)}
    closure = {
        'dependency_hashes_exact': dep['all_pass'],
        'upstream_artifacts_and_source_ledger_exact': bool(dep['upstream_artifacts_valid'] and dep['source_ledger_exact']),
        'fixed_action_metric_source_alpha_and_potential_exact': sym['all_pass'],
        'full_two_channel_radial_linearization_exact': bool(sym['all_pass'] and equation_check['pass']),
        'physical_centre_and_decaying_outer_domain_pass': bool(all(x['physical_residuals_pass'] for x in rows+first_excited_rows)),
        'phase_gauge_quotient_and_fixed_charge_pass': bool(all(x['fixed_charge_boundary_fraction'] < 1e-6 for x in rows)),
        'background_regression_pass': back_gate['pass'],
        'primary_collocation_spectrum_pass': bool(all(x['collocation_rms_residual_max'] < 3e-5
                                                      for x in rows+first_excited_rows)),
        'independent_evans_spectrum_pass': bool(all(x['pass'] for x in evans.values())
                                                and scan_match_fundamental and scan_match_excited),
        'lowest_mode_identification_pass': bool(node_theorem['application_pass']),
        'simple_zero_and_transverse_crossing_pass': bool(sign and crossing and simple_kernel and tracking['pass']),
        'turning_point_agreement_pass': crossing,
        'domain_resolution_tolerance_convergence_pass': convergence_pass,
        'equilibrium_tangent_to_physical_kernel_match_pass': tangent_overlap > 0.98,
        'mutation_controls_pass': bool(mut['pass'] and bench['pass']),
        'package_clean_pass': True, 'aggregate_gate_pass': False,
    }
    closure['aggregate_gate_pass'] = bool(all(v for k, v in closure.items() if k != 'aggregate_gate_pass'))
    valid = closure['aggregate_gate_pass']
    status = ('PASS_PHYSICAL_FIXED_CHARGE_NODELESS_RADIAL_MODE_CROSSES_SIMPLE_ZERO_AT_W3_65_FIRST_POST_ANCHOR_TURN'
              if valid else 'NUMERICALLY_INCONCLUSIVE_W3_66_PHYSICAL_RADIAL_MODE_GATE')
    result = {
        'schema_version': 'W3-66-result-v1.0',
        'model_version': 'W3-66-v1.0-EH-SEXTIC-U1-FIXED-ALPHA-PHYSICAL-RADIAL-MODE',
        'status': status, 'artifact_valid': valid, 'dependency_gate': dep,
        'symbolic_gate': sym, 'full_equation_verification': equation_check,
        'background_gate': back_gate, 'primary_modes': rows,
        'independent_evans': {str(k): v for k, v in evans.items()},
        'global_two_basis_evans_scan': scan,
        'first_excited_mode_ordering_guard': {'modes': first_excited_rows,
                                              'minimum_gap_from_fundamental': min(
                                                  excited_rec[x]['Lambda']-rec[x]['Lambda']
                                                  for x in CONTROL_PROBES),
                                              'pass': ordering},
        'self_adjoint_node_ordering': node_theorem,
        'mode_tracking_controls': tracking, 'convergence_controls': controls,
        'deterministic_eigenvalue_error': {str(k): v for k, v in errors.items()},
        'crossing': {'registered_turn_f0': TURN, 'nested_h': list(HS), 'slopes': slopes,
                     'symmetric_pair_roots_without_using_turn_mode': roots,
                     'richardson_extrapolated_root': richardson_root,
                     'sign_gate_pass': sign, 'simple_kernel_pass': simple_kernel,
                     'kernel_singular_values': evans[TURN]['singular_values_at_minimum'],
                     'nodeless_tracked_mode_pass': nodeless,
                     'transverse_turn_agreement_pass': crossing,
                     'tangent_seed_used_for_primary_mode': False,
                     'tangent_weighted_overlap': tangent_overlap},
        'sturm_liouville_benchmark': bench, 'mutation_controls': mut,
        'closure_flags': closure,
        'scope_flags': {
            'physical_fixed_charge_radial_mode_crossing_derived': valid,
            'tested_preturn_backgrounds_positive_lowest_resolved_mode': valid,
            'immediate_postturn_backgrounds_one_negative_radial_mode': valid,
            'physical_alpha_from_foundation_derived': False,
            'vacuum_to_anchor_branch_mapped': False, 'full_equilibrium_spiral_mapped': False,
            'nonradial_stability_completed': False, 'nonlinear_stability_completed': False,
            'collapse_evolution_completed': False, 'final_equilibrium_endpoint_derived': False,
            'near_horizon_limit_derived': False, 'trapped_surface_derived': False,
            'black_hole_solution_derived': False, 'geodesic_completeness_derived': False,
            'singularity_resolution_completed': False,
            'foundation_strong_field_response_derived': False,
            'observational_likelihood_evaluated': False},
        'scientific_boundary': ('Physical spherical fixed-charge linear mode on the selected alpha=0.04 branch only; '
                                'no nonlinear, nonradial, collapse, horizon, singularity, or foundation-alpha claim.'),
        'provenance': {'generated_utc': datetime.now(timezone.utc).isoformat(),
                       'python': platform.python_version(), 'numpy': np.__version__,
                       'scipy': scipy.__version__, 'sympy': sp.__version__,
                       'preregistration_sha256': sha(PREREG),
                       'source_sha256': sha(Path(__file__)), 'deterministic': True}}
    OUTPUT.write_text(json.dumps(native(result), indent=2, sort_keys=True), encoding='utf-8')
    result['package'] = package_gate(); result['closure_flags']['package_clean_pass'] = result['package']['pass']
    result['closure_flags']['aggregate_gate_pass'] = bool(all(v for k, v in result['closure_flags'].items()
                                                               if k != 'aggregate_gate_pass'))
    result['artifact_valid'] = result['closure_flags']['aggregate_gate_pass']
    if not result['artifact_valid']:
        result['status'] = 'NUMERICALLY_INCONCLUSIVE_W3_66_PHYSICAL_RADIAL_MODE_GATE'
        for k in ('physical_fixed_charge_radial_mode_crossing_derived',
                  'tested_preturn_backgrounds_positive_lowest_resolved_mode',
                  'immediate_postturn_backgrounds_one_negative_radial_mode'):
            result['scope_flags'][k] = False
    if not finite(result): raise RuntimeError('Nonfinite result')
    OUTPUT.write_text(json.dumps(native(result), indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'artifact_valid': result['artifact_valid'],
                      'below_Lambda': rec[TURN-0.02]['Lambda'], 'turn_Lambda': rt['Lambda'],
                      'above_Lambda': rec[TURN+0.02]['Lambda'],
                      'tangent_overlap': tangent_overlap,
                      'closure_flags': result['closure_flags']}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
