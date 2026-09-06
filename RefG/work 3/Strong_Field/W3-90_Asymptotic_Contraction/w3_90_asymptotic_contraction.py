"""W90: exact non-bouncing contraction discriminator; stdout only."""
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
    'intuitive/RefG_GE.md': '7c28f8848ae5ac441efae05e5a551973f37cca711202a0865e007793e282acd1',
    'intuitive/RefG_EN.tex': '6e69d616229688d885320d9b26b8c4637c563ae47f8da006feee8548d6ad910e',
    'intuitive/idea.txt': 'a73a06e1ed5b75298fae1bf22c88418e175b6628b12fa08a9e9c3992da59b48e',
    BASE+'W3-71_Horizon_Material_Scale_Separation/w3_71_horizon_material_scale_separation_preregistration.md': '1d3f74489f6cc52061253b6e1ea3d7f96e5d423f8b2afb88e79a44a38ae916c3',
    BASE+'W3-81_Dynamical_Scale_Integrability/w3_81_dynamical_scale_integrability_contract.md': '43b5bc7586afc323dbb64129bcb74f154b990c54dd82e33603a394f59c1aff88',
    BASE+'W3-82_Dynamical_Clock_Radar_Readout/w3_82_dynamical_clock_radar_contract.md': '3c389016254c2c554bec346e6012857c41daaa01a10e2fbba876be1d971d63d8',
    BASE+'W3-87_State_Dependent_Gravitational_Response/w3_87_state_dependent_response_contract.md': '7c47bcd4efe292a91d13717a3ec3962776488b01c521dfb27b9df1e989fcee80',
    BASE+'W3-87_State_Dependent_Gravitational_Response/w3_87_state_dependent_response.py': 'a789d47cb4899becd3e15c9891ed82c63efa733bc3af6e4e2a7911b56f01064a',
    BASE+'W3-89_Spherical_Interior_Turning_Point/w3_89_spherical_turning_point_contract.md': '83631ea6fba1bbed07e2df59af0b8a5afe450ba24f77d7ba8d94f8ecfdfdc334',
    BASE+'W3-89_Spherical_Interior_Turning_Point/w3_89_spherical_turning_point.py': '95ad5ca49e59e87fb7de2c9e871c6b77531636b14aee7efbfeaf040a29872953',
    BASE+'W3-90_Asymptotic_Contraction/w3_90_asymptotic_contraction_contract.md': '73001ef614886fc0515a62b182117f97dc569a46d67a33b6c402f59ea84f7aec',
}
CHECKS, DETAILS, MUTATIONS = {}, {}, {}
t, x, th, ph = s.symbols('tau x theta phi', real=True)
N, a, b, j = [s.Function(k, positive=True)(t) for k in ('N', 'a', 'b', 'j')]
K, n, P = s.symbols('K n P', positive=True)
Ha, Hb, dHa, dHb = s.symbols('Ha Hb dotHa dotHb', real=True)
F, rho = s.Function('F'), s.Function('rho')
volume = a*b*b
nv = j/volume
REPL = {s.diff(N,t): 0, N: 1, s.diff(j,t): 0,
        s.diff(a,t,2): a*(dHa+Ha**2), s.diff(b,t,2): b*(dHb+Hb**2),
        s.diff(a,t): a*Ha, s.diff(b,t): b*Hb, j: n*volume}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def simplify(expression):
    return s.simplify(s.sympify(expression).doit())


def red(expression):
    return simplify(s.sympify(expression).doit().subs(REPL, simultaneous=True))


def check(group, name, condition):
    CHECKS.setdefault(group, {})[name] = bool(condition)


def zero(group, name, expression):
    residual = simplify(expression)
    check(group, name, residual == 0)
    if residual != 0:
        DETAILS.setdefault('failed_residuals', {})[name] = str(residual)
    return residual


def reject(name, residual, witness):
    residual = simplify(residual)
    certificate = simplify(residual.xreplace(witness))
    check('mutation_controls_checked', name,
          certificate != 0 and certificate.equals(0) is False)
    MUTATIONS[name] = {'residual': str(residual), 'witness': str(certificate)}


def action():
    phase = s.Function('phase')(t)
    adot, bdot = s.diff(a,t), s.diff(b,t)
    L = (-2*K*F(nv)*(a*bdot**2+2*b*adot*bdot)/N
         +2*K*N*a*F(nv)-N*volume*rho(nv)+j*s.diff(phase,t))
    def EL(q):
        return s.diff(L,q)-s.diff(s.diff(L,s.diff(q,t)),t)
    # All variations precede the lapse gauge and conserved-current reduction.
    EN, Ea, Ej, Ephase = [EL(q) for q in (N,a,j,phase)]
    constraint = red(EN)/volume
    radial = red(Ea)/(2*K*b*b*F(n))
    mu = simplify(s.diff(phase,t)-red(Ej))
    beta = n*s.diff(F(n),n)/F(n)
    torsion = 4*Ha*Hb+2*Hb**2-2/b**2
    pressure = n*s.diff(rho(n),n)-rho(n)
    zero('action_identity_checked','lapse', constraint-
         (2*K*F(n)*(2*Ha*Hb+Hb**2+1/b**2)-rho(n)))
    zero('action_identity_checked','radial', radial-
         (2*dHb+(1-beta)*(3*Hb**2+1/b**2)+pressure/(2*K*F(n))))
    zero('action_identity_checked','current', mu-
         (s.diff(rho(n),n)+K*torsion*s.diff(F(n),n)))
    zero('action_identity_checked','conserved_j', Ephase+s.diff(j,t))
    ndot = red(s.diff(nv,t))
    zero('action_identity_checked','density_transport',ndot+n*(Ha+2*Hb))
    fdot = s.diff(F(n),n)*ndot
    # An off-shell EL combination avoids differentiating a pointwise rho constraint.
    derived = simplify((radial-constraint/(2*K*F(n)))/2)
    def transport(coefficient=1):
        return dHb+Hb**2+(coefficient*fdot/F(n)-Ha)*Hb+n*mu/(4*K*F(n))
    zero('action_identity_checked','EL_to_transport',transport()-derived)
    weighted_dt = red(s.diff(F(nv)*bdot/a,t))
    source = simplify(weighted_dt-F(n)*b*derived/a)
    zero('action_identity_checked','weighted_proper_time',source+b*n*mu/(4*K*a))
    zero('action_identity_checked','stationary_regression',
         derived.subs(Hb,0)-(dHb+n*mu.subs(Hb,0)/(4*K*F(n))))
    f0 = s.symbols('constant_F',positive=True)
    zero('action_identity_checked','constant_F',
         derived.xreplace({s.diff(F(n),n):0,F(n):f0})-
         (dHb+Hb**2-Ha*Hb+n*s.diff(rho(n),n)/(4*K*f0)))
    reject('drop_Fdot',transport(0)-derived,
           {Ha:s.Integer(1),Hb:s.Integer(1),n:s.Integer(1),
            F(n):s.Integer(1),s.diff(F(n),n):s.Integer(1)})
    # Same source validator as the current baseline, with one vertex removed.
    reject('drop_induced_current_frequency',s.diff(rho(n),n)-mu,
           {Ha:s.Integer(0),Hb:s.Integer(0),b:s.Integer(1),K:s.Integer(1),
            s.diff(F(n),n):s.Integer(1)})
    DETAILS['action'] = {'mu_eff':str(mu),
        'weighted_proper_time_source':str(source),
        'constraint_elimination':'Off-shell linear combination; no rho derivative substitution.'}
    return mu, derived


def null_geometry(mu, equation):
    coords = (t,x,th,ph)
    gd = [-s.Integer(1),a*a,b*b,b*b*s.sin(th)**2]
    metric = s.diag(*gd)
    Gamma = {}
    for i in range(4):
        for m in range(4):
            for v in range(4):
                z = simplify((s.diff(metric[i,v],coords[m])+s.diff(metric[i,m],coords[v])
                              -s.diff(metric[m,v],coords[i]))/(2*gd[i]))
                if z != 0:
                    Gamma[i,m,v] = z
    def G(i,m,v):
        return Gamma.get((i,m,v),s.S.Zero)
    Ricci = s.zeros(4)
    for m in range(4):
        for v in range(4):
            Ricci[m,v] = simplify(sum(
                s.diff(G(c,m,v),coords[c])-s.diff(G(c,m,c),coords[v])
                +sum(G(c,c,d)*G(d,m,v)-G(c,v,d)*G(d,m,c) for d in range(4))
                for c in range(4)))
    def null_residual(k):
        return simplify((k.T*metric*k)[0])
    for direction in (-1,1):
        k = s.Matrix([P/a,direction*P/a**2,0,0])
        zero('null_geometry_checked',f'null_{direction}',null_residual(k))
        zero('null_geometry_checked',f'Killing_momentum_{direction}',a*a*k[1]-direction*P)
        for i in range(4):
            acc = k[0]*s.diff(k[i],t)+sum(G(i,m,v)*k[m]*k[v] for m in range(4) for v in range(4))
            zero('null_geometry_checked',f'affine_geodesic_{direction}_{i}',acc)
    k = s.Matrix([P/a,P/a**2,0,0])
    reject('reverse_affine_conversion',null_residual(s.Matrix([P*a,P/a**2,0,0])),
           {a:s.Integer(2),P:s.Integer(1)})
    bprime = P*s.diff(b,t)/a
    bsecond = P*s.diff(bprime,t)/a
    Rkk = simplify((k.T*Ricci*k)[0])
    zero('null_geometry_checked','Ricci_radial_projection',Rkk+2*bsecond/b)
    Qprime = red(P*s.diff(F(nv)*bprime,t)/a)
    source = simplify(Qprime-P**2*F(n)*b*equation/a**2)
    zero('weighted_focusing_checked','affine_source',source+P**2*b*n*mu/(4*K*a**2))
    Fprime = red(P*s.diff(F(nv),t)/a)
    focusing = n*mu*(P/a)**2/(2*K*F(n))+2*Fprime*red(bprime)/(F(n)*b)
    zero('weighted_focusing_checked','Ricci_action_source',
         red(Rkk)-focusing+2*P**2*equation/a**2)
    zero('weighted_focusing_checked','proper_to_affine',
         source-(P/a)*(-P*b*n*mu/(4*K*a)))
    coefficient = simplify(source/mu)
    zero('weighted_focusing_checked','source_sign_coefficient',coefficient+P**2*b*n/(4*K*a**2))
    check('weighted_focusing_checked','positive_mu_decreases_Q',coefficient.is_negative)
    fp,vneg,ff = s.symbols('positive_Fprime inward_speed positive_F',positive=True)
    check('weighted_focusing_checked','growing_F_defocusing_term',(-2*fp*vneg/(ff*b)).is_negative)
    zero('weighted_focusing_checked','zero_source_constant_Q',
         source.xreplace({s.diff(rho(n),n):s.Integer(0),s.diff(F(n),n):s.Integer(0)}))
    DETAILS['null_geometry'] = {'Ricci_projection':str(Rkk), 'Q_prime_on_shell':str(source),
        'focusing':'Rkk = n*mu*(P/a)^2/(2*K*F) + 2*(dlnF/dlambda)*(db/dlambda)/b',
        'domain':'Future radial affine rays in the same nondegenerate KS patch.'}


def comparison():
    lam,z = s.symbols('lambda s',nonnegative=True)
    q0,b0,fmax = s.symbols('q0 b0 Fmax',positive=True)
    f = s.Function('f',positive=True)
    loss = s.Function('additional_inward_weight',nonnegative=True)
    b_of_lam = b0-s.Integral((q0+loss(z))/f(z),(z,0,lam))
    zero('comparison_condition_checked','integral_derivative',
         s.diff(b_of_lam,lam)+(q0+loss(lam))/f(lam))
    check('comparison_condition_checked','inverse_F_necessary_gap',
          (loss(lam)/f(lam)).is_nonnegative)
    # 0<F<=Fmax, -Q=q0+loss: exact nonnegative certificate for the comparison.
    frac = s.symbols('fraction',positive=True)
    delta = s.symbols('Fmax_minus_F',nonnegative=True)
    diff = (q0+loss(lam))/frac-q0/fmax
    certificate = loss(lam)/frac+q0*delta/(frac*fmax)
    zero('comparison_condition_checked','bounded_F_comparison_identity',
         diff-certificate.subs(delta,fmax-frac))
    check('comparison_condition_checked','bounded_F_comparison_nonnegative',certificate.is_nonnegative)
    linear = b0-q0*lam/fmax
    zero('comparison_condition_checked','linear_bound_derivative',s.diff(linear,lam)+q0/fmax)
    zero('comparison_condition_checked','finite_affine_bound',linear.subs(lam,b0*fmax/q0))
    integral = s.integrate(1/(1+z),(z,0,lam))
    zero('comparison_condition_checked','unbounded_F_control_integral',integral-s.log(1+lam))
    check('comparison_condition_checked','unbounded_F_control_diverges',s.limit(integral,lam,s.oo)==s.oo)
    DETAILS['comparison'] = {'origin':'lambda-lambda0 measured from within the bounded-F future tail.',
        'exact_condition':'Integral (-Q)/F dlambda = b0-b_star < b0',
        'necessary_condition':'Integral dlambda/F finite; F cannot be uniformly bounded above.',
        'bounded_F_bound':'b <= b0-q0*(lambda-lambda0)/Fmax',
        'not_inferred':['pointwise F tends to infinity','mu tends to zero','unbounded F is sufficient'],
        'boundary_scope':'b reaches zero or the patch/assumptions end first; extension is separate.'}


def readout():
    q = s.symbols('q',nonnegative=True)
    gtt = -(1-q)**2/(1+q)**2
    grr = (1+q)**4
    pt,pL = (1-q)/(1+q),(1+q)**-2
    def ruler_residual(candidate):
        return simplify(candidate**2*grr-1)
    zero('readout_scope_checked','clock_metric',pt**2+gtt)
    zero('readout_scope_checked','ruler_metric',ruler_residual(pL))
    zero('readout_scope_checked','coordinate_null_speed',gtt+grr*(pt*pL)**2)
    velocity = s.symbols('coordinate_velocity',real=True)
    metric_roots = s.solve(gtt+grr*velocity**2,velocity)
    local_residuals = [simplify((root/(pt*pL))**2-1) for root in metric_roots]
    check('readout_scope_checked','local_light_speed',
          len(metric_roots)==2 and all(residual==0 for residual in local_residuals))
    zero('readout_scope_checked','weak_order_agreement',s.diff(pt-pL,q).subs(q,0))
    zero('readout_scope_checked','clock_horizon_limit',s.limit(pt,q,1,dir='-'))
    zero('readout_scope_checked','ruler_horizon_limit',s.limit(pL,q,1,dir='-')-s.Rational(1,4))
    reject('conflate_clock_and_ruler',ruler_residual(pt),{q:s.Rational(1,2)})
    u = s.symbols('external_time',nonnegative=True)
    clock = (1+u)**-2
    check('readout_scope_checked','clock_control_positive',clock.is_positive)
    zero('readout_scope_checked','clock_control_asymptote',s.limit(clock,u,s.oo))
    zero('readout_scope_checked','clock_control_finite_proper_integral',s.integrate(clock,(u,0,s.oo))-1)
    DETAILS['readout'] = {'static_domain':'0 <= q < 1; horizon values are one-sided limits only.',
        'horizon':{'p_t':'0','p_L':'1/4'},
        'clock_control':'p_t=(1+t)^(-2)>0, tends to zero, but its integral is 1; not a spacetime.',
        'unprovided_maps':['p_L=b','p_L=1/F','n=p_L^(-3)','mu=p_t'],
        'roles':'Areal radius, phase frequency, operational ruler and observer/ray measurements remain distinct.'}


def main():
    before = {p:sha(ROOT/p) for p in PINS}
    for p,target in PINS.items():
        check('provenance',p,before[p]==target)
    if not all(CHECKS['provenance'].values()):
        print(json.dumps({'status':'FAIL','checks':CHECKS,'source_hashes':before},indent=2,allow_nan=False))
        return 1
    mu,equation = action()
    null_geometry(mu,equation)
    comparison()
    readout()
    check('provenance','protected_sources_unchanged',all(sha(ROOT/p)==before[p] for p in PINS))
    flags = {g:bool(v and all(v.values())) for g,v in CHECKS.items()}
    passed = all(flags.values())
    flags['conditional_bounded_F_obstruction'] = passed
    flags.update({name:False for name in ('external_shrinkage_trajectory_derived','microscopic_F_derived',
        'full_coupled_health','actual_asymptote_constructed','singularity_resolved','regular_black_hole',
        'global_completion','observational_pass','active_theory_changed','intuitive_files_changed')})
    print(json.dumps({'package':'W3-90-v1.0','status':'PASS' if passed else 'FAIL',
        'check_count':sum(map(len,CHECKS.values())),'checks':CHECKS,'closure_flags':flags,
        'negative_controls':MUTATIONS,'details':DETAILS,'source_hashes':before,
        'verifier_sha256':sha(HERE),'versions':{'Python':platform.python_version(),'SymPy':s.__version__}},
        indent=2,allow_nan=False))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
