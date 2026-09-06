"""W3-85: external regular-metric benchmark; restricted source test, no writes."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import sympy as s

HERE = Path(__file__).resolve()
ROOT = HERE.parents[4]
CONTRACT_SHA = '733e949038352162920075604e2b94faf3266ea7f5fbb102ef161d8f95225ab6'
PINS = {
    'CODES.md':'27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41',
    'intuitive/RefG_GE.md':'7c28f8848ae5ac441efae05e5a551973f37cca711202a0865e007793e282acd1',
    'RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field_preregistration.md':'25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1',
    'RefG/work 3/Strong_Field/W3-73_Coupled_Horizon_Regular_Einstein_Complex_Scalar/w3_73_coupled_horizon_regular_einstein_complex_scalar_preregistration.md':'8a3c3887fc0a28edc8fced67da0bc66ccaff39ade1f6e5b7e339f579fc02c49e',
    'RefG/work 3/Strong_Field/W3-84_Minimal_Node_Link_Candidate/w3_84_node_link.py':'acd70be11d4734b5b208fa5b7166475166c48ee5f090640a05e19dfa081c3916',
}
r,M,ell = s.symbols('r M ell',positive=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(expr):
    return s.factor(s.cancel(s.trigsimp(expr)))


def records(residuals,certificates=None,**evidence):
    values = {name:clean(value) for name,value in residuals.items()}
    cert = {} if certificates is None else {name:bool(value) for name,value in certificates.items()}
    return dict(passed=all(value==0 for value in values.values()) and all(cert.values()),
                residuals={name:str(value) for name,value in values.items()},
                certificates=cert,**evidence)


def radial_action():
    print('W85: independent lapse and metric variations',file=sys.stderr,flush=True)
    f,n = s.Function('f')(r),s.Function('n')(r)
    H = s.Function('H')
    psi = (1-f)/r**2
    lagrangian = n*s.diff(r**3*H(psi),r)/12
    en = s.diff(lagrangian,n)
    ef = s.diff(lagrangian,f)-s.diff(s.diff(lagrangian,s.diff(f,r)),r)
    hp = s.diff(H(s.Symbol('psi')),s.Symbol('psi')).subs(s.Symbol('psi'),psi)
    baseline = records({'lapse_EL':en-s.diff(r**3*H(psi),r)/12,
                        'metric_EL':ef-r*s.diff(n,r)*hp/12})
    x = s.symbols('psi')
    response = 6*x/(1-ell**2*x)
    solution = s.solve(s.Eq(r**3*response,12*M),x)[0]
    metric = clean(1-r**2*solution)
    einstein_psi = s.solve(s.Eq(r**3*6*x,12*M),x)[0]
    denominator = r**3+2*M*ell**2
    solution_checks = records({
        'radial_constraint':r**3*response.subs(x,solution)-12*M,
        'psi_solution':solution-2*M/denominator,
        'metric_solution':metric-(1-2*M*r**2/denominator),
        'Einstein_control':1-r**2*einstein_psi-(1-2*M/r),
        'Einstein_normalization':s.diff(response,x).subs(x,0)-6,
        'response_monotonicity':s.diff(response,x)-6/(1-ell**2*x)**2,
        'domain_gap':1-ell**2*solution-r**3/denominator,
    },{'denominator_positive':denominator.is_positive,
       'psi_positive':solution.is_positive,
       'domain_gap_positive':(r**3/denominator).is_positive},
        H=str(response),psi=str(solution),f=str(metric),
        lapse='H_prime>0 and E_f=0 imply n_prime=0; n(infinity)=1 fixes n=1')
    # Premature gauge fixing removes the independently derived lapse equation.
    einstein_L = lagrangian.replace(H,lambda z:6*z).doit()
    fixed_L = einstein_L.subs(n,1).doit()
    fixed_en = s.diff(fixed_L,n)
    fixed_ef = clean(s.diff(fixed_L,f)-s.diff(s.diff(fixed_L,s.diff(f,r)),r))
    full_en = s.diff(einstein_L,n)
    lost_constraint = clean((fixed_en-full_en).subs(f,1-r**2).doit())
    wrong_H = 6*x/(1+ell**2*x)
    wrong_psi = s.solve(s.Eq(r**3*wrong_H,12*M),x)[0]
    wrong_constraint = clean(r**3*response.subs(x,wrong_psi)-12*M)
    pole = (2*M*ell**2)**s.Rational(1,3)
    wrong_den = r**3-2*M*ell**2
    pole_residue = clean(2*M/s.diff(wrong_den,r).subs(r,pole))
    controls = {
        'premature_lapse_fix':{'rejected':fixed_en==0 and fixed_ef==0 and lost_constraint!=0,
            'fixed_lapse_equation':str(fixed_en),'fixed_metric_equation':str(fixed_ef),
            'baseline_lapse_residual_on_f_1_minus_r2':str(lost_constraint)},
        'reverse_response_denominator':{'rejected':wrong_constraint!=0 and bool(pole.is_positive) and bool(pole_residue.is_positive),
            'own_constraint_residual':str(clean(r**3*wrong_H.subs(x,wrong_psi)-12*M)),
            'baseline_constraint_residual':str(wrong_constraint),'psi':str(wrong_psi),
            'positive_pole':str(pole),'simple_pole_residue':str(pole_residue),
            'denominator_at_pole':str(clean(wrong_den.subs(r,pole)))},
    }
    return metric,baseline,solution_checks,controls


def metric_geometry():
    print('W85: direct metric connection, Riemann, Ricci and Einstein tensors',file=sys.stderr,flush=True)
    t,theta,phi = s.symbols('t theta phi',real=True)
    coords = (t,r,theta,phi)
    f = s.Function('f')(r)
    g = s.diag(-f,1/f,r**2,r**2*s.sin(theta)**2)
    inv = g.inv()
    gamma = {}
    for a in range(4):
        for b in range(4):
            for c in range(4):
                value = clean(sum(inv[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in range(4)))
                if value!=0:
                    gamma[a,b,c] = value
    Gm = lambda a,b,c:gamma.get((a,b,c),s.S.Zero)
    riemann = {}
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    value = clean(s.diff(Gm(a,d,b),coords[c])-s.diff(Gm(a,c,b),coords[d])
                        +sum(Gm(a,c,j)*Gm(j,d,b)-Gm(a,d,j)*Gm(j,c,b) for j in range(4)))
                    if value!=0:
                        riemann[a,b,c,d] = value
    ricci = s.Matrix(4,4,lambda b,d:clean(sum(riemann.get((a,b,a,d),0) for a in range(4))))
    R = clean(sum(inv[a,b]*ricci[a,b] for a in range(4) for b in range(4)))
    einstein = (ricci-g*R/2).applyfunc(clean)
    K = clean(sum(g[a,a]*inv[b,b]*inv[c,c]*inv[d,d]*value**2
                  for (a,b,c,d),value in riemann.items()))
    source = {'rho':clean(einstein[0,0]/(8*s.pi*f)),
              'pr':clean(f*einstein[1,1]/(8*s.pi)),
              'pt':clean(einstein[2,2]/(8*s.pi*r**2))}
    residuals = {
        'Ricci_scalar':R-(-s.diff(f,r,2)-4*s.diff(f,r)/r+2*(1-f)/r**2),
        'Kretschmann':K-(s.diff(f,r,2)**2+4*(s.diff(f,r)/r)**2+4*((1-f)/r**2)**2),
        'angular_Einstein_equality':einstein[3,3]/s.sin(theta)**2-einstein[2,2],
    }
    residuals.update({f'off_diagonal_Einstein_{a}{b}':einstein[a,b] for a in range(4) for b in range(a+1,4)})
    return f,R,K,source,records(residuals,connection_nonzero=len(gamma),Riemann_nonzero=len(riemann),
                               Ricci=str(R),Kretschmann=str(K),effective_source={k:str(v) for k,v in source.items()})


def geometry_and_horizons(metric,f,R,K):
    actual_R = clean(R.subs(f,metric).doit())
    actual_K = clean(K.subs(f,metric).doit())
    radial_components = ((1-metric)/r**2,s.diff(metric,r)/r,s.diff(metric,r,2))
    residuals = {
        'centre_R':s.limit(actual_R,r,0)-12/ell**2,
        'centre_K':s.limit(actual_K,r,0)-24/ell**4,
        'centre_f_order':s.limit((metric-1+r**2/ell**2)/r**5,r,0)-1/(2*M*ell**4),
        'centre_cartesian_coefficient':s.limit((1/metric-1)/r**2,r,0)-1/ell**2,
        'ADM_mass':s.limit(r*(1-metric)/2,r,s.oo)-M,
        'asymptotic_correction':s.limit(r**4*(metric-1+2*M/r),r,s.oo)-4*M**2*ell**2,
        'asymptotic_remainder_order':s.limit(r**7*(metric-1+2*M/r-4*M**2*ell**2/r**4),r,s.oo)+8*M**3*ell**4,
        'asymptotic_R':s.limit(actual_R,r,s.oo),
        'asymptotic_K':s.limit(actual_K,r,s.oo),
        'EF_determinant':s.Matrix([[-metric,1],[1,0]]).det()+1,
    }
    for j,(component,target) in enumerate(zip(radial_components,(1/ell**2,-2/ell**2,-2/ell**2))):
        residuals[f'centre_Riemann_function_{j}'] = s.limit(component,r,0)-target
        residuals[f'asymptotic_Riemann_function_{j}'] = s.limit(component,r,s.oo)
    centre = records(residuals,{'positive_common_denominator':(r**3+2*M*ell**2).is_positive},
                     Ricci=str(actual_R),Kretschmann=str(actual_K),
                     finite_frame_functions=[str(clean(v)) for v in radial_components],
                     local_extension='At r=0 the static Cartesian spatial correction is O(r^2); at finite horizons the ingoing EF determinant is -1. No global completeness conclusion.')
    polynomial = r**3-2*M*r**2+2*M*ell**2
    stationary = 4*M/3
    critical_M = 3*s.sqrt(3)*ell/4
    critical_r = s.sqrt(3)*ell
    minimum = clean(polynomial.subs(r,stationary))
    horizon_checks = records({
        'metric_numerator':metric*(r**3+2*M*ell**2)-polynomial,
        'derivative_factorization':s.diff(polynomial,r)-3*r*(r-stationary),
        'positive_minimum':s.diff(polynomial,r,2).subs(r,stationary)-4*M,
        'minimum_sign_factor':minimum-2*M*(ell**2-16*M**2/27),
        'critical_minimum':minimum.subs(M,critical_M),
        'critical_root':polynomial.subs({M:critical_M,r:critical_r}),
        'critical_derivative':s.diff(polynomial,r).subs({M:critical_M,r:critical_r}),
        'critical_second_derivative':s.diff(polynomial,r,2).subs({M:critical_M,r:critical_r})-3*s.sqrt(3)*ell,
    },{'origin_positive':polynomial.subs(r,0).is_positive,
       'minimum_radius_positive':stationary.is_positive,
       'minimum_second_derivative_positive':(4*M).is_positive},
        polynomial=str(polynomial),critical_mass=str(critical_M),critical_radius=str(critical_r),
        analytic_classification={'M_below_critical':'no positive roots',
            'M_equal_critical':'one positive double root','M_above_critical':'two positive simple roots'},
        certificate='For r>0, P decreases from positive P(0) to its unique minimum at 4M/3, then increases to positive infinity; the minimum sign gives all three cases.')
    coefficients = [float(v) for v in s.Poly(polynomial.subs({M:2,ell:1}),r).all_coeffs()]
    roots = np.roots(coefficients)
    root_records = []
    for root in sorted(roots,key=lambda z:z.real):
        value = complex(root)
        denominator = abs(value)**3+4*abs(value)**2+4
        residual = abs(np.polyval(coefficients,value))/denominator
        root_records.append({'real':float(value.real),'imag':float(value.imag),'relative_polynomial_residual':float(residual)})
    numerical_ok = all(abs(v['imag'])<1e-12 and v['relative_polynomial_residual']<1e-11 for v in root_records)
    numerical_ok = numerical_ok and sum(v['real']>0 for v in root_records)==2 and sum(v['real']<0 for v in root_records)==1
    horizon_checks['illustration'] = dict(M=2,ell=1,roots=root_records,passed=bool(numerical_ok))
    horizon_checks['passed'] = horizon_checks['passed'] and bool(numerical_ok)
    return centre,horizon_checks


def source_test(metric,f,geometric_source):
    print('W85: Einstein source, NEC and canonical representability',file=sys.stderr,flush=True)
    rho,pr,pt = [clean(geometric_source[name].subs(f,metric).doit()) for name in ('rho','pr','pt')]
    mass = clean(r*(1-metric)/2)
    denom = r**3+2*M*ell**2
    target_rho = 3*M**2*ell**2/(2*s.pi*denom**2)
    transverse_nec = 9*M**2*ell**2*r**3/(2*s.pi*denom**3)

    def validate(candidate_rho,candidate_pr,candidate_pt):
        return records({'rho_Einstein':candidate_rho-rho,'radial_Einstein':candidate_pr-pr,
            'tangential_Einstein':candidate_pt-pt,
            'radial_conservation':s.diff(candidate_pr,r)+2*(candidate_pr-candidate_pt)/r
                +(candidate_rho+candidate_pr)*s.diff(metric,r)/(2*metric)})

    baseline = validate(rho,pr,pt)
    flipped = validate(rho,pr,-pt)
    sources = records({'mass_density':rho-s.diff(mass,r)/(4*s.pi*r**2),
        'mass_tangential_pressure':pt+s.diff(mass,r,2)/(8*s.pi*r),
        'explicit_density':rho-target_rho,'radial_NEC':rho+pr,
        'transverse_NEC':rho+pt-transverse_nec,
        'density_gradient':s.diff(rho,r)+9*M**2*ell**2*r**2/(s.pi*denom**3),
        'central_radial_isotropy':s.limit(pr+rho,r,0),
        'central_tangential_isotropy':s.limit(pt+rho,r,0)},
        {'density_positive':target_rho.is_positive,'transverse_NEC_positive':transverse_nec.is_positive,
         'negative_density_gradient':(9*M**2*ell**2*r**2/(s.pi*denom**3)).is_positive},
        rho=str(rho),p_r=str(pr),p_t=str(pt),rho_plus_p_t=str(clean(rho+pt)),
        conservation=baseline,source_ledger='Either modified-gravity vacuum OR Einstein with G_ab/(8pi), never both.')
    sources['passed'] = sources['passed'] and baseline['passed']
    # Actual Hilbert differentiation, before substituting the physical inverse metric.
    itt,irr = s.symbols('g_inv_tt g_inv_rr',nonzero=True,real=True)
    lapse,lapse_f = s.symbols('n f',positive=True)
    chi,chi_r,omega = s.symbols('chi chi_r omega',real=True)
    V = s.Function('V')
    matter_L = -(irr*chi_r**2+itt*chi**2*omega**2)/2-V(chi)
    Ttt = -2*s.diff(matter_L,itt)+matter_L/itt
    Trr = -2*s.diff(matter_L,irr)+matter_L/irr
    substitution = {itt:-1/(lapse**2*lapse_f),irr:lapse_f}
    scalar_rho = clean(Ttt.subs(substitution)/(lapse**2*lapse_f))
    scalar_pr = clean(lapse_f*Trr.subs(substitution))
    positive_sum = lapse_f*chi_r**2+omega**2*chi**2/(lapse**2*lapse_f)
    z = s.symbols('omega_chi',real=True)
    zero_derivative_density = scalar_rho.subs(omega**2*chi**2,z**2).subs({chi_r:0,z:0})
    profile = s.Function('chi')(r)
    constant_source_gradient = s.diff(V(profile),r).subs(s.diff(profile,r),0)
    canonical = records({'Hilbert_NEC':scalar_rho+scalar_pr-positive_sum,
        'zero_kinetic_density':zero_derivative_density-V(chi),
        'zero_kinetic_pressure':scalar_pr.subs(omega**2*chi**2,z**2).subs({chi_r:0,z:0})+V(chi),
        'constant_profile_density_gradient':constant_source_gradient},
        {'positive_radial_coefficient':lapse_f.is_positive,
         'positive_phase_coefficient':(1/(lapse**2*lapse_f)).is_positive,
         'nonnegative_radial_square':s.ask(s.Q.nonnegative(chi_r**2)),
         'nonnegative_phase_square':s.ask(s.Q.nonnegative(omega**2*chi**2)),
         'target_density_nonconstant':s.diff(rho,r)!=0},
        scalar_density=str(scalar_rho),scalar_pressure=str(scalar_pr),null_sum=str(positive_sum),
        equality_certificate='On f>0,n>0, a sum of these nonnegative squares is zero only if chi_prime=0 and omega*chi=0. Each positive-weight field in a finite sum obeys the same implication. Its remaining constant potential cannot match rho_prime<0.',
        restricted_domain='Static exterior of this one-function target; canonical positive-kinetic fields only.')
    return sources,canonical,{'flip_tangential_pressure':dict(rejected=not flipped['passed'],**flipped)}


def main():
    contract = HERE.with_name('w3_85_regular_centre_contract.md')
    pins = {name:dict(actual=sha(ROOT/name),expected=value) for name,value in PINS.items()}
    package = sorted(p.name for p in HERE.parent.iterdir())==sorted((HERE.name,contract.name))
    provenance = dict(source_sha256=sha(HERE),contract_sha256=sha(contract),pins=pins,exact_two_files=package,
                      versions=dict(Python=platform.python_version(),SymPy=s.__version__,NumPy=np.__version__))
    result = dict(stage='W3-85-v1.0',provenance=provenance,
        scope={name:False for name in ('RefG_response_derived','RefG_regular_black_hole','global_geodesic_completeness',
            'generic_stability','formation','observational_pass','active_theory_changed','intuitive_files_changed')})
    if sha(contract)!=CONTRACT_SHA or not package or any(v['actual']!=v['expected'] for v in pins.values()):
        return dict(result,status='UNRESOLVED',failure='Frozen provenance or exact two-file package mismatch')
    metric,variation,radial,mutations = radial_action()
    f,R,K,source,geometry = metric_geometry()
    centre,horizons = geometry_and_horizons(metric,f,R,K)
    sources,canonical,source_mutations = source_test(metric,f,source)
    mutations.update(source_mutations)
    flags = dict(variation=variation['passed'],radial_solution=radial['passed'],
        geometric_curvature=geometry['passed'],regular_centre=centre['passed'],horizons=horizons['passed'],
        source_conservation=sources['passed'],null_energy_counterexample=sources['passed'] and centre['passed'],
        canonical_source_exclusion=canonical['passed'] and sources['passed'],
        mutation_controls=all(v['rejected'] for v in mutations.values()))
    passed = all(flags.values())
    result.update(status='PASS' if passed else 'UNRESOLVED',closure_flags=flags,
        failed_gates=[name for name,value in flags.items() if not value],variation=variation,radial_solution=radial,
        direct_geometry=geometry,centre_and_limits=centre,horizons=horizons,effective_source=sources,
        canonical_source=canonical,mutations=mutations,
        source_decision='REJECTED_FOR_THIS_METRIC_SOURCE_PAIR' if passed else 'UNRESOLVED',
        interpretation='The published reduced-action benchmark has a regular centre and NEC-compatible effective Einstein stress. The retained canonical scalar cannot supply this exact static exterior. The unconditional GE NEC-violation wording is disproved; the conditional Penrose statements retain their global hypotheses. The literature response is not derived from RefG or W84.')
    return result


if __name__=='__main__':
    try:
        report = main()
        print(json.dumps(report,allow_nan=False,separators=(',',':')))
        sys.exit(0 if report.get('status')=='PASS' else 1)
    except Exception as exc:
        print(json.dumps(dict(stage='W3-85-v1.0',status='UNRESOLVED',failure_type=type(exc).__name__,failure=str(exc)),allow_nan=False))
        raise
