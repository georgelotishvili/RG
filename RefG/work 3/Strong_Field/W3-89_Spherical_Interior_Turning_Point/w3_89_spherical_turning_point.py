"""W89: exact local KS turning-point test; stdout only, no file writes.

First endpoint SHA56eb739ebe91472ab94db3faaefdeec0b64bc755f9b7df6b43b3089b89f7b06d
failed source_sign and mu_gamma_beta: a pointwise rho value was substituted inside
its derivative. Independent jets now remain fixed during the constraint substitution.
The frozen contract, action, targets and acceptance conditions are unchanged.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve()
ROOT = HERE.parents[4]
BASE = 'RefG/work 3/Strong_Field/'
PINS = {
    'CODES.md': '27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41',
    BASE+'W3-87_State_Dependent_Gravitational_Response/w3_87_state_dependent_response_contract.md': '7c47bcd4efe292a91d13717a3ec3962776488b01c521dfb27b9df1e989fcee80',
    BASE+'W3-87_State_Dependent_Gravitational_Response/w3_87_state_dependent_response.py': 'a789d47cb4899becd3e15c9891ed82c63efa733bc3af6e4e2a7911b56f01064a',
    BASE+'W3-89_Spherical_Interior_Turning_Point/w3_89_spherical_turning_point_contract.md': '83631ea6fba1bbed07e2df59af0b8a5afe450ba24f77d7ba8d94f8ecfdfdc334',
    'intuitive/RefG_GE.md': '7c28f8848ae5ac441efae05e5a551973f37cca711202a0865e007793e282acd1',
    'intuitive/RefG_EN.tex': '6e69d616229688d885320d9b26b8c4637c563ae47f8da006feee8548d6ad910e',
    'intuitive/idea.txt': 'a73a06e1ed5b75298fae1bf22c88418e175b6628b12fa08a9e9c3992da59b48e',
    'intuitive/Dictionary.txt': 'f6e12b67f38e49bb547d37e6c92375a2ee5b2f596ed481a866cbc490be32ed0b',
}
CHECKS, DETAILS, CONTROLS = {}, {}, {}
t, x, th, ph = s.symbols('t x theta phi', real=True)
coords = (t, x, th, ph)
N, a, b, j = [s.Function(k, positive=True)(t) for k in ('N', 'a', 'b', 'j')]
ft = s.Function('F_state')(t)
K, n = s.symbols('K n', positive=True)
F, rho = s.Function('F'), s.Function('rho')
Ha, Hb, dHa, dHb = s.symbols('Ha Hb dotHa dotHb', real=True)
gd = [-N*N, a*a, b*b, b*b*s.sin(th)**2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(group, name, condition):
    CHECKS.setdefault(group, {})[name] = bool(condition)


def zero(group, name, expression):
    residual = s.simplify(expression.doit())
    check(group, name, residual == 0)
    if residual != 0:
        DETAILS.setdefault('failed_residuals', {})[name] = str(residual)
    return residual


def reject(name, residual, witness=None):
    residual = s.simplify(residual.doit())
    certificate = s.simplify(residual.subs(witness or {}).doit())
    check('mutation_controls', name, certificate != 0 and certificate.equals(0) is False)
    CONTROLS[name] = {'residual': str(residual), 'nonzero_certificate': str(certificate)}


def geometry(ks=True):
    E = s.diag(N, a, b, b*s.sin(th)); inv = E.inv(); vol = E.det()
    om = [s.zeros(4) for _ in coords]
    def put(A, B, mu, value):
        om[mu][A, B], om[mu][B, A] = value, -value
    if ks:
        put(1, 2, 3, s.sin(th)); put(1, 3, 2, -1)
    else:
        put(1, 2, 2, -1); put(1, 3, 3, -s.sin(th))
    put(2, 3, 3, -s.cos(th))
    prefix = 'KS' if ks else 'static_control'
    for mu in range(4):
        for nu in range(mu+1, 4):
            R = om[nu].diff(coords[mu])-om[mu].diff(coords[nu])+om[mu]*om[nu]-om[nu]*om[mu]
            for A in range(4):
                for B in range(A+1, 4):
                    zero('flat_spin_pair', f'{prefix}_flat_{mu}{nu}_{A}{B}', R[A, B])
    Q = {(A, B, nu): s.simplify(vol*(inv[nu, A]*inv[0, B]-inv[nu, B]*inv[0, A])*s.diff(ft, t)/2)
         for A in range(4) for B in range(4) for nu in range(4)}
    spin = {}
    for A in range(4):
        for B in range(A+1, 4):
            div = sum(s.diff(Q[A, B, nu], coords[nu])-sum(om[nu][c, A]*Q[c, B, nu]+om[nu][c, B]*Q[A, c, nu] for c in range(4)) for nu in range(4))
            spin[A, B] = s.simplify(div)
            if ks:
                zero('flat_spin_pair', f'KS_spin_{A}{B}', div)
    if not ks:
        reject('static_spherical_spin', spin[0, 1], {s.diff(ft, t): 1, a: 1, b: 1, th: s.pi/2})
    tor = {}
    for r in range(4):
        for mu in range(4):
            for nu in range(4):
                value = sum(inv[r, A]*(s.diff(E[A, nu], coords[mu])-s.diff(E[A, mu], coords[nu])+sum(om[mu][A, B]*E[B, nu]-om[nu][A, B]*E[B, mu] for B in range(4))) for A in range(4))
                value = s.simplify(value)
                if value != 0:
                    tor[r, mu, nu] = value
    I1 = sum(gd[r]*v*v/(gd[mu]*gd[nu]) for (r, mu, nu), v in tor.items())
    I2 = sum(v*tor.get((nu, mu, r), 0)/gd[mu] for (r, mu, nu), v in tor.items())
    trace = [sum(tor.get((r, r, mu), 0) for r in range(4)) for mu in range(4)]
    T = s.simplify(I1/4+I2/2-sum(trace[mu]**2/gd[mu] for mu in range(4)))
    target = 4*s.diff(a,t)*s.diff(b,t)/(N*N*a*b)+2*s.diff(b,t)**2/(N*N*b*b)-2/b**2
    zero('torsion_scalar', prefix+'_T', T-target)
    if ks:
        reject('omit_intrinsic_sphere_term', T-(target+2/b**2))
        J = s.Matrix([j*s.sin(th), 0, 0, 0])
        zero('lapse_preserving_KS_variation', 'current_density_squared', -(J.T*s.diag(*gd)*J)[0]/vol**2-(j/(a*b*b))**2)
    return T


def action(T):
    nv = j/(a*b*b); volume = a*b*b; phase = s.Function('phase')(t)
    L = -K*N*volume*F(nv)*T-N*volume*rho(nv)+j*s.diff(phase,t)
    target_L = -2*K*F(nv)*(a*s.diff(b,t)**2+2*b*s.diff(a,t)*s.diff(b,t))/N+2*K*N*a*F(nv)-N*volume*rho(nv)+j*s.diff(phase,t)
    zero('lapse_preserving_KS_variation', 'action_from_torsion', L-target_L)
    def EL(lag, q):
        return s.diff(lag,q)-s.diff(s.diff(lag,s.diff(q,t)),t)
    repl = {s.diff(N,t): 0, N: 1, s.diff(j,t): 0,
            s.diff(a,t,2): a*(dHa+Ha**2), s.diff(b,t,2): b*(dHb+Hb**2),
            s.diff(a,t): a*Ha, s.diff(b,t): b*Hb, j: n*volume}
    def red(e):
        return s.simplify(e.doit().subs(repl, simultaneous=True))
    beta = n*s.diff(F(n),n)/F(n); pressure = n*s.diff(rho(n),n)-rho(n)
    radial = 2*dHb+(1-beta)*(3*Hb**2+1/b**2)+pressure/(2*K*F(n))
    angular = dHa+dHb+(1-beta)*(Ha**2+Ha*Hb+Hb**2)-beta/b**2+pressure/(2*K*F(n))
    constraint = 2*K*F(n)*(2*Ha*Hb+Hb**2+1/b**2)-rho(n)
    mu = s.diff(rho(n),n)+K*red(T)*s.diff(F(n),n)
    EN, Ea, Eb, Ej, Ephase = [EL(L,q) for q in (N,a,b,j,phase)]
    zero('lapse_preserving_KS_variation', 'lapse', red(EN)/volume-constraint)
    zero('lapse_preserving_KS_variation', 'radial_direct', red(Ea)/(2*K*b*b*F(n))-radial)
    zero('lapse_preserving_KS_variation', 'angular_direct', red(Eb)/(4*K*a*b*F(n))-angular)
    zero('lapse_preserving_KS_variation', 'phase_current', Ephase+s.diff(j,t))
    zero('lapse_preserving_KS_variation', 'current_phase', red(Ej)-(s.diff(phase,t)-mu))
    X,Y = s.Function('X')(t),s.Function('Y')(t)
    LL = L.subs({a:s.exp(X),b:s.exp(Y)}).doit()
    log_repl = {s.diff(X,t,2):dHa,s.diff(Y,t,2):dHb,s.diff(X,t):Ha,s.diff(Y,t):Hb,
                X:s.log(a),Y:s.log(b),N:1,s.diff(N,t):0,s.diff(j,t):0,j:n*volume}
    for name,q,normalizer,target in (('radial_log',X,2*K*volume*F(n),radial),('angular_log',Y,4*K*volume*F(n),angular)):
        computed = EL(LL,q).subs(log_repl, simultaneous=True)
        zero('lapse_preserving_KS_variation',name,computed/normalizer-target)
    f0=s.symbols('constant_F',positive=True)
    frozen = EL(L.subs(F(nv),f0),a)
    reject('freeze_F_during_scale_variation', red(frozen).subs(f0,F(n))/(2*K*b*b*F(n))-radial,
           {s.diff(F(n),n):1,F(n):2,n:1,b:1,Hb:0})
    reject('omit_torsion_from_current', red(Ej)-(s.diff(phase,t)-s.diff(rho(n),n)),
           {s.diff(F(n),n):1,K:1,Ha:0,Hb:0,b:1})
    turn_constraint={rho(n):2*K*F(n)/b**2}
    # A constraint on rho at one point is not a functional equation of state.
    rp_jet,fp_jet=s.symbols('rho_prime_jet F_prime_jet',real=True)
    freeze={s.diff(rho(n),n):rp_jet,s.diff(F(n),n):fp_jet}
    def constrain(e):
        return s.simplify(e.xreplace(freeze).subs(turn_constraint).xreplace({v:k for k,v in freeze.items()}))
    acc=s.solve(radial.subs(Hb,0),dHb)[0]
    acc=constrain(acc)
    mut=s.simplify(mu.subs(Hb,0))
    zero('turning_point_identity','source_sign',acc+n*mut/(4*K*F(n)))
    gamma=n*s.diff(rho(n),n)/rho(n)
    zero('turning_point_identity','beta_gamma',acc-constrain((beta-gamma)/(2*b**2)))
    zero('turning_point_identity','mu_gamma_beta',mut-constrain((rho(n)/n)*(gamma-beta)))
    mp,fp=s.symbols('positive_mu positive_F',positive=True)
    signed_acc=-n*mp/(4*K*fp)
    check('turning_point_identity','positive_clock_maximum',signed_acc.is_negative)
    check('turning_point_identity','negative_clock_minimum',(-signed_acc).is_positive)
    check('turning_point_identity','zero_clock_boundary',signed_acc.subs(mp,0)==0)
    reject('reverse_turning_sign',acc-n*mut/(4*K*F(n)),
           {s.diff(rho(n),n):1,s.diff(F(n),n):0,F(n):1,K:1,n:1,b:1})
    DETAILS['turning_point']={'acceleration':str(acc),'mu_eff':str(mut),
        'identity':'bddot/b = -n*mu_eff/(4*K*F) at bdot=0',
        'mu_zero':'degenerate turning point requires higher-order analysis'}


def current_block():
    eps=s.symbols('epsilon',real=True)
    z0,z1,z2,z3,pd,g1,g2,g3=s.symbols('dJ0 dJ1 dJ2 dJ3 pi_dot g1 g2 g3',real=True)
    mu,h=s.symbols('mu h',real=True); energy=s.Function('E')
    perturb=s.sqrt((n+eps*z0)**2-eps**2*(z1*z1+z2*z2+z3*z3))
    lag=(n+eps*z0)*(mu+eps*pd)+eps**2*(z1*g1+z2*g2+z3*g3)-energy(perturb)
    L2=(s.diff(lag,eps,2).subs(eps,0)/2).doit().subs({s.diff(energy(n),n):mu,s.diff(energy(n),n,2):h})
    first=z0*pd+z1*g1+z2*g2+z3*g3-h*z0*z0/2+mu*(z1*z1+z2*z2+z3*z3)/(2*n)
    zero('fixed_geometry_current_diagnostic','canonical_expansion',L2-first)
    solutions=s.solve([s.diff(L2,q) for q in (z0,z1,z2,z3)],(z0,z1,z2,z3),dict=True)[0]
    eliminated=s.simplify(L2.subs(solutions))
    grad2=g1*g1+g2*g2+g3*g3
    target=pd*pd/(2*h)-n*grad2/(2*mu)
    zero('fixed_geometry_current_diagnostic','auxiliary_elimination',eliminated-target)
    reject('reverse_spatial_phase_sign',eliminated-(pd*pd/(2*h)+n*grad2/(2*mu)),
           {n:1,mu:1,g1:1,g2:0,g3:0})
    hp,mp=s.symbols('positive_h positive_mu',positive=True)
    temporal=s.diff(eliminated,pd,2); spatial=s.diff(eliminated,g1,2)
    check('fixed_geometry_current_diagnostic','ordinary_temporal',temporal.subs(h,hp).is_positive)
    check('fixed_geometry_current_diagnostic','ordinary_spatial',spatial.subs(mu,mp).is_negative)
    check('fixed_geometry_current_diagnostic','negative_mu_positive_h_wrong_gradient',spatial.subs(mu,-mp).is_positive)
    check('fixed_geometry_current_diagnostic','negative_h_wrong_temporal',temporal.subs(h,-hp).is_negative)
    Hess=s.hessian(L2,(z0,z1,z2,z3))
    zero('fixed_geometry_current_diagnostic','zero_mu_spatial_inversion',Hess[1,1].subs(mu,0))
    zero('fixed_geometry_current_diagnostic','zero_h_temporal_inversion',Hess[0,0].subs(h,0))
    zero('fixed_geometry_current_diagnostic','current_hessian',Hess.det()+h*mu**3/n**3)
    DETAILS['fixed_geometry_current']={'quadratic_action':str(eliminated),
        'scope':'Fixed metric and torsion; complete coupled constraints and health are not evaluated.'}


def curvature():
    metric=s.diag(*gd); Gamma={}
    for r in range(4):
        for m in range(4):
            for v in range(4):
                value=s.simplify((s.diff(metric[r,v],coords[m])+s.diff(metric[r,m],coords[v])-s.diff(metric[m,v],coords[r]))/(2*gd[r]))
                if value!=0:Gamma[r,m,v]=value
    def G(r,m,v):return Gamma.get((r,m,v),s.Integer(0))
    Riemann={}
    for r in range(4):
        for c in range(4):
            for m in range(4):
                for v in range(4):
                    value=s.simplify(s.diff(G(r,v,c),coords[m])-s.diff(G(r,m,c),coords[v])+sum(G(r,m,k)*G(k,v,c)-G(r,v,k)*G(k,m,c) for k in range(4)))
                    if value!=0:Riemann[r,c,m,v]=value
    kretsch=sum(gd[r]*value**2/(gd[c]*gd[m]*gd[v]) for (r,c,m,v),value in Riemann.items())
    aa=(s.diff(a,t,2)-s.diff(a,t)*s.diff(N,t)/N)/(N*N*a)
    bb=(s.diff(b,t,2)-s.diff(b,t)*s.diff(N,t)/N)/(N*N*b)
    ha=s.diff(a,t)/(N*a);hb=s.diff(b,t)/(N*b)
    target=4*(aa**2+2*bb**2+2*(ha*hb)**2+(hb**2+1/b**2)**2)
    zero('curvature_regression','metric_Kretschmann',s.trigsimp(kretsch-target))
    A,B,ha0,hb0=s.symbols('proper_acc_a proper_acc_b proper_Ha proper_Hb',real=True)
    lower=4*(A*A+2*B*B+2*(ha0*hb0)**2+hb0**4+2*hb0**2/b**2)
    check('curvature_regression','K_minus_4_over_b4_nonnegative',lower.is_nonnegative)
    M,r=s.symbols('M areal_r',positive=True)
    av=s.sqrt(2*M/r-1);bv=-av;haM=M/(r*r*av);hbM=bv/r
    dha=s.diff(haM,r)*bv;dhb=s.diff(hbM,r)*bv
    zero('curvature_regression','Schwarzschild_lapse',2*haM*hbM+hbM**2+1/r**2)
    zero('curvature_regression','Schwarzschild_radial',2*dhb+3*hbM**2+1/r**2)
    zero('curvature_regression','Schwarzschild_angular',dha+dhb+haM**2+haM*hbM+hbM**2)
    schwarz=4*((2*M/r**3)**2+2*(-M/r**3)**2+2*(haM*hbM)**2+(hbM**2+1/r**2)**2)
    zero('curvature_regression','Schwarzschild_invariant',schwarz-48*M*M/r**6)
    DETAILS['curvature']={'KS_lower_bound':'Kretschmann >= 4/b^4',
        'Schwarzschild':'48*M^2/b^6, 0<b<2M; vacuum geometry regression only'}


def main():
    before={p:sha(ROOT/p) for p in PINS}
    for p,target in PINS.items():check('provenance',p,before[p]==target)
    if not all(CHECKS['provenance'].values()):
        print(json.dumps({'status':'FAIL','checks':CHECKS,'reason':'dependency hash mismatch'},indent=2));return 1
    T=geometry();geometry(False);action(T);current_block();curvature()
    check('provenance','protected_sources_unchanged',all(sha(ROOT/p)==before[p] for p in PINS))
    flags={group:bool(rows and all(rows.values())) for group,rows in CHECKS.items()}
    passed=all(flags.values())
    flags['Conditional_positive_clock_local_bounce_excluded']=passed
    flags.update({k:False for k in ('global_singularity_resolved','regular_black_hole',
        'all_regular_branches_excluded','full_coupled_health','microscopic_F_derived',
        'observational_pass','active_theory_changed','intuitive_files_changed')})
    print(json.dumps({'package':'W3-89-v1.0','status':'PASS' if passed else 'FAIL',
        'check_count':sum(map(len,CHECKS.values())),'checks':CHECKS,'closure_flags':flags,
        'negative_controls':CONTROLS,'details':DETAILS,'source_hashes':before,
        'verifier_sha256':sha(HERE),'versions':{'Python':platform.python_version(),'SymPy':s.__version__}},indent=2,allow_nan=False))
    return 0 if passed else 1


if __name__=='__main__':
    raise SystemExit(main())
