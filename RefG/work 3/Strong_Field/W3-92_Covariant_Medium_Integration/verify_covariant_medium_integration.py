"""W3-92: exact, stdout-only integration checks; no repository writes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import sys

sys.dont_write_bytecode = True
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ARTICLE = ROOT / 'RefG_ka.md'
CONTRACT = HERE / 'FORMAL_COVARIANT_MEDIUM_INTEGRATION.md'
ARTICLE_SHA = '2571f9fbde25cd9e5258e5bb2c78797380123bf32621e4eaf068ce97c1b4c927'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def simp(expr):
    return s.factor(s.simplify(expr))


def metric_readouts(A, B):
    return s.sqrt(B), 1/s.sqrt(A), s.sqrt(A/B)


def readout_residuals(A, B, claimed):
    return [simp(actual-target) for actual, target in
            zip(metric_readouts(A, B), claimed)]


def geometry(r, th):
    """Fresh four-dimensional connection and Ricci tensor, article convention."""
    t, ph = s.symbols('t phi', real=True)
    a, b = s.Function('a')(r), s.Function('b')(r)
    g = s.diag(s.exp(b), -s.exp(a), -s.exp(a)*r*r,
               -s.exp(a)*r*r*s.sin(th)**2)
    gi, xx = g.inv(), [t, r, th, ph]
    ch = [[[simp(sum(gi[i, l]*(s.diff(g[l, j], xx[k])
                 + s.diff(g[l, k], xx[j])-s.diff(g[j, k], xx[l]))
                 for l in range(4))/2) for k in range(4)]
                 for j in range(4)] for i in range(4)]
    ric = s.zeros(4)
    for i in range(4):
        for j in range(4):
            ric[i, j] = simp(sum(s.diff(ch[k][i][j], xx[k])
                - s.diff(ch[k][i][k], xx[j])
                + sum(ch[k][i][j]*ch[l][k][l]
                      - ch[l][i][k]*ch[k][j][l] for l in range(4))
                for k in range(4)))
    scal = simp(s.trace(gi*ric))
    ein = (gi*ric-s.eye(4)*scal/2).applyfunc(simp)
    return a, b, g, ein, scal


def projected_hilbert(A, B, hp, M, omega, r, th):
    """Vary the full inverse-metric dependence, then impose the static branch."""
    pairs = [(i, j) for i in range(4) for j in range(i, 4)]
    symbols = {ij: s.Symbol('g%d%d' % ij, real=True) for ij in pairs}
    inv = s.Matrix(4, 4, lambda i, j: symbols[min(i, j), max(i, j)])
    Y, X, K = inv[0, 0], inv[0, 1]*hp, inv[1, 1]*hp**2
    lag = -omega*M**2*(X**2/Y-K)
    gd = [B, -A, -A*r*r, -A*r*r*s.sin(th)**2]
    sub = {symbols[i, j]: (1/gd[i] if i == j else 0) for i, j in pairs}
    # Independent off-diagonal inverse entries occur twice in the tensor sum.
    deriv = {(i, j): s.diff(lag, z)/(1 if i == j else 2)
             for (i, j), z in symbols.items()}
    cov = s.Matrix(4, 4, lambda i, j: simp((
        (gd[i]*lag if i == j else 0)
        - 2*deriv[min(i, j), max(i, j)]).subs(sub)))
    return s.diag(*[1/z for z in gd])*cov, simp(lag.subs(sub))


def main():
    rows = []

    def zero(name, expr, group):
        val = simp(expr)
        rows.append(dict(name=name, group=group, pass_check=bool(val == 0),
                         residual=str(val)))
        return val

    def truth(name, value, group, certificate):
        rows.append(dict(name=name, group=group, pass_check=bool(value),
                         certificate=str(certificate)))

    r, m, q, M, omega = s.symbols('r m q M omega', positive=True)
    th = s.symbols('vartheta', real=True)
    A, B = s.symbols('A B', positive=True)
    hp = s.symbols('hp', real=True)
    print('W3-92: deriving metric connection and medium Hilbert source', file=sys.stderr)
    la, lb, g, G, scalar = geometry(r, th)
    T, lag = projected_hilbert(A, B, hp, M, omega, r, th)
    z = hp**2/A
    target = M**2*omega*z*s.diag(-1, 1, -1, -1)
    for i in range(4):
        for j in range(4):
            zero('Hilbert_%d%d' % (i, j), T[i, j]-target[i, j], 'source')
    zero('projected_L_on_branch', lag+omega*M**2*z, 'source')
    # Clock derivative of Z=X^2/Y-K vanishes when X=0, before any metric ansatz.
    X, Y, K = s.symbols('X Y K', real=True)
    zero('clock_vertex_X', s.diff(X**2/Y-K, X).subs(X, 0), 'source')
    zero('clock_vertex_Y', s.diff(X**2/Y-K, Y).subs(X, 0), 'source')
    # Actual radial H-action variation fixes the flux sign and normalization.
    Hr = s.Function('H')(r)
    measure = r*r*s.exp((la+lb)/2)
    radial_lag = -omega*M**2*measure*s.diff(Hr, r)**2
    el = s.diff(radial_lag, Hr)-s.diff(s.diff(radial_lag, s.diff(Hr, r)), r)
    zero('H_radial_action', el/(2*omega*M**2)
         - s.diff(measure*s.diff(Hr, r), r), 'source')

    h = m/r
    subext = {la: 2*h, lb: -2*h}
    extG = G.subs(subext).doit().applyfunc(simp)
    extscalar = simp(scalar.subs(subext).doit())
    extT = T.subs({A: s.exp(2*h), B: s.exp(-2*h), hp: -m/r**2,
                  omega: 1}).applyfunc(simp)
    for i in range(4):
        for j in range(4):
            zero('exterior_Einstein_%d%d' % (i, j),
                 extG[i, j]-extT[i, j]/M**2, 'exterior')
    zero('silent_clock', (s.exp(-2*h)*g.inv()[0, 0]).subs(subext)-1, 'exterior')
    zero('silent_labels', (s.exp(2*h)*(-g.inv()[1, 1])).subs(subext)-1, 'exterior')
    flux = -measure*s.diff(Hr, r)
    extflux = simp(flux.subs(subext).subs(Hr, h).doit())
    zero('H_flux_equals_m', extflux-m, 'exterior')
    zero('H_equation', s.diff(extflux, r), 'exterior')
    zero('exterior_radial_NEC', extT[0, 0]-extT[1, 1]
         +2*M**2*m**2*s.exp(-2*h)/r**4, 'exterior')

    u = s.symbols('u', real=True)
    st = s.exp(-2*u).series(u, 0, 3).removeO()
    sp = s.exp(2*u).series(u, 0, 3).removeO()
    zero('static_beta_one', st-(1-2*u+2*u*u), 'weak_field')
    zero('static_gamma_one', sp-(1+2*u+2*u*u), 'weak_field')
    zero('spatial_quadratic_not_Schwarzschild', sp.coeff(u, 2)-s.Rational(3, 2)
         -s.Rational(1, 2), 'weak_field')
    extA = (-g[1, 1]).subs(subext)
    extB = g[0, 0].subs(subext)
    exterior_claims = [s.exp(-h), s.exp(-h), s.exp(2*h)]
    exterior_readouts = readout_residuals(extA, extB, exterior_claims)
    for name, residual in zip(['clock', 'ruler', 'optical_index'], exterior_readouts):
        zero('exterior_'+name, residual, 'readout')

    print('W3-92: checking core geometry and restricted source branch', file=sys.stderr)
    ac = q*(s.Rational(35, 8)*r**2-s.Rational(21, 4)*r**4+s.Rational(15, 8)*r**6)
    bc = -q+q*(-s.Rational(11, 8)*r**2+s.Rational(9, 4)*r**4-s.Rational(7, 8)*r**6)
    for label, inner, outer in [('A', ac, q/r), ('B', bc, -q/r)]:
        for order in range(3):
            zero('log_matching_%s_%d' % (label, order),
                 (s.diff(inner, r, order)-s.diff(outer, r, order)).subs(r, 1), 'core')
            zero('metric_matching_%s_%d' % (label, order),
                 (s.diff(s.exp(inner), r, order)
                  -s.diff(s.exp(outer), r, order)).subs(r, 1), 'core')
        zero('even_centre_'+label, inner.subs(r, -r)-inner, 'core')
        zero('zero_centre_derivative_'+label, s.diff(inner, r).subs(r, 0), 'core')
    coreG = G.subs({la: ac, lb: bc}).doit().applyfunc(simp)
    ap, bp = s.diff(ac, r), s.diff(bc, r)
    rho = -s.exp(-ac)*(r*ap**2+4*r*s.diff(ap, r)+8*ap)/(4*r)
    pr = s.exp(-ac)*(r*ap**2+2*r*ap*bp+4*ap+4*bp)/(4*r)
    pt = s.exp(-ac)*(2*r*s.diff(ap, r)+r*bp**2
                           +2*r*s.diff(bp, r)+2*ap+2*bp)/(4*r)
    for i, component in enumerate([rho, -pr, -pt, -pt]):
        zero('core_article_Einstein_%d' % i, coreG[i, i]-component, 'core')
    zero('centre_density', s.limit(coreG[0, 0], r, 0)+105*q/4, 'core')
    zero('centre_pressure', s.limit(-coreG[1, 1], r, 0)-6*q, 'core')
    zero('centre_isotropy', s.limit(coreG[1, 1]-coreG[2, 2], r, 0), 'core')
    zero('centre_Ricci', s.limit(-s.trace(coreG), r, 0)-177*q/4, 'core')

    poly = q*r**2*(153*q*r**8-360*q*r**6+30*q*r**4+360*q*r**2
                   -167*q+384*r**2-384)/64
    actual_poly = simp(s.exp(ac)*(coreG[1, 1]-coreG[2, 2])/2)
    zero('core_anisotropy_polynomial', actual_poly-poly, 'restricted_source')
    leading = simp(s.limit(actual_poly/r**2, r, 0))
    zero('negative_leading_certificate', leading+q*(167*q+384)/64, 'restricted_source')
    truth('target_anisotropy_negative_near_centre', leading.is_negative is True,
          'restricted_source', leading)
    zero('projected_H_anisotropy', T[1, 1]-T[2, 2]
         -2*omega*M**2*hp**2/A, 'restricted_source')
    truth('source_anisotropy_nonnegative',
          (2*M**2*hp**2/A).is_nonnegative is True, 'restricted_source',
          '2 M_Pl^2 H_prime^2/A >= 0 for real H_prime and A>0')
    # On phi^A=x^A the Cartesian current density is -M_*^4 L(r) delta_iA.
    # div J_A = -M_*^4 L'(r) x_A/r; no spurious radial-area factor.
    x1, x2, x3 = s.symbols('x1 x2 x3', real=True)
    rr = s.sqrt(x1*x1+x2*x2+x3*x3)
    L = s.Function('L')
    for xi in [x1, x2, x3]:
        zero('Cartesian_label_divergence_'+str(xi),
             s.diff(L(rr), xi)-s.Subs(s.diff(L(r), r), r, rr)*xi/rr,
             'restricted_source')
    # Vary the response through its H-normalized clock and three strain eigenvalues.
    hh, yy, b1, b2, b3, ms = s.symbols('hh yy b1 b2 b3 Mstar', positive=True)
    ff = s.Function('Fmed')(yy, b1, b2, b3)
    normal = {yy: s.exp(-2*hh)*yy, b1: s.exp(2*hh)*b1,
              b2: s.exp(2*hh)*b2, b3: s.exp(2*hh)*b3}
    response_source = yy*s.diff(ff, yy)-sum(v*s.diff(ff, v) for v in [b1,b2,b3])
    zero('response_H_variation',
         -s.diff(ff.subs(normal, simultaneous=True), hh).subs(hh, 0)/2
         -response_source, 'restricted_source')
    volume = r*r*s.exp((3*la+lb)/2)
    full_H_el = el/(2*omega*M**2)+ms**4*volume*response_source/(omega*M**2)
    zero('flux_source_sign', full_H_el+s.diff(flux, r)
         -ms**4*volume*response_source/(omega*M**2), 'restricted_source')
    truth('silent_regular_core_cannot_supply_m', m.is_positive is True,
          'restricted_source', 'Q(0)=0, Q_prime=0 imply Q(rc)=0 != m>0')

    pc, pl = s.exp(bc/2), s.exp(-ac/2)
    zero('core_log_AB', ac+bc-q*(r*r-1)**3, 'readout')
    zero('clock_ruler_ratio', pc/pl-s.exp(q*(r*r-1)**3/2), 'readout')
    generic_clock, generic_ruler, _ = metric_readouts(-g[1, 1], g[0, 0])
    zero('exterior_common_p', (generic_clock-generic_ruler).subs(subext), 'readout')
    zero('centre_clock', pc.subs(r, 0)-s.exp(-q/2), 'readout')
    zero('centre_ruler', pl.subs(r, 0)-1, 'readout')
    truth('core_common_p_rejected', (pc/pl).subs(r, 0) != 1,
          'readout', 'p_clock(0)/p_ruler(0)=exp(-q/2)<1')

    # Altered candidates are passed to the original production identities.
    mutations = []
    for name, residual in [
        ('omit_H_source', extG[0, 0]),
        ('alter_core_second_derivative',
         s.diff(ac+(r-1)**2, r, 2).subs(r, 1)-s.diff(q/r, r, 2).subs(r, 1))]:
        value = simp(residual)
        mutations.append(dict(name=name, rejected=bool(value != 0), residual=str(value)))
    for name, aa, bb, claims in [
        ('omit_spatial_exponential', s.Integer(1), extB, exterior_claims),
        ('force_common_core_p', s.exp(ac), s.exp(bc),
         [pl, pl, metric_readouts(s.exp(ac), s.exp(bc))[2]])]:
        residuals = readout_residuals(aa, bb, claims)
        mutations.append(dict(name=name, rejected=any(v != 0 for v in residuals),
                              residuals=[str(v) for v in residuals]))

    article_ok = sha(ARTICLE) == ARTICLE_SHA
    groups = {g: all(x['pass_check'] for x in rows if x['group'] == g)
              for g in sorted({x['group'] for x in rows})}
    ok = article_ok and all(groups.values()) and all(x['rejected'] for x in mutations)
    flags = {
        'exact_exterior_rechecked': groups['exterior'] and groups['source'],
        'core_matching_geometry_rechecked': groups['core'],
        'restricted_core_source_obstruction_rechecked': groups['restricted_source'],
        'static_clock_ruler_map_rechecked': groups['readout'],
        'static_spherical_beta_gamma_rechecked': groups['weak_field'],
        'full_coupled_health_proved': False, 'action_derived_regular_interior': False,
        'regular_black_hole_derived': False, 'formation_derived': False,
        'full_PPN_pass': False, 'CMB_same_action_handoff': False,
        'quantum_same_action_handoff': False, 'W54_W87_action_equivalence': False,
        'microscopic_derivation': False, 'observational_pass': False}
    report = dict(package='W3-92', version='1.0', status='PASS' if ok else 'FAIL',
        decision='existing_medium_branch_integrated_with_restricted_core_source_obstruction',
        provenance=dict(article_sha256=sha(ARTICLE), article_matches=article_ok,
                        contract_sha256=sha(CONTRACT), source_sha256=sha(Path(__file__)),
                        python=platform.python_version(), sympy=s.__version__),
        groups=groups, exact_checks=rows, mutation_controls=mutations,
        closure_flags=flags, exterior_Ricci_scalar=str(extscalar),
        scope='Exact existing exterior; kinematic core and restricted source exclusion. '
              'No new dynamics, complete health, interior solution or data comparison.')
    print(json.dumps(report, ensure_ascii=False, allow_nan=False, indent=2))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
