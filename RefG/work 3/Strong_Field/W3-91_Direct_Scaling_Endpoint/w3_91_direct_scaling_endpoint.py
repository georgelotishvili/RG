"""W91: diagnostic strong extrapolation of W51; stdout only, no file writes."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

# First endpoint bae6a279... had two undecided SymPy positivity queries, not
# nonzero physical residuals. The exact sinh certificate below resolves them.

HERE = Path(__file__).resolve()
ROOT = HERE.parents[4]
PINS = {
    'CODES.md':'27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41',
    'intuitive/RefG_GE.md':'7c28f8848ae5ac441efae05e5a551973f37cca711202a0865e007793e282acd1',
    'intuitive/RefG_EN.tex':'6e69d616229688d885320d9b26b8c4637c563ae47f8da006feee8548d6ad910e',
    'intuitive/idea.txt':'a73a06e1ed5b75298fae1bf22c88418e175b6628b12fa08a9e9c3992da59b48e',
    'intuitive/Dictionary.txt':'f6e12b67f38e49bb547d37e6c92375a2ee5b2f596ed481a866cbc490be32ed0b',
    'RefG/work 3/Lagrangian_Formulation/Weak_Field_Closure/w3_51_weak_field_closure_contract.md':'86bc2ed86cddee36bec5e46fdfa407701107290c783bfa81ba1440b96becc7cf',
    'RefG/work 3/Lagrangian_Formulation/Weak_Field_Closure/w3_51_weak_field_closure.py':'59f0aff2c4fd63daccba7ba22a48863ab1d5f84b15605444cf28fc0ea9318f4a',
    'RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_foundation_strong_field_response_preregistration.md':'31e6520d9b7917413b9f2978291b4a77f067abe8dd3d6a9e89e1b2cfb699da11',
    'RefG/work 3/Strong_Field/W3-91_Direct_Scaling_Endpoint/w3_91_direct_scaling_endpoint_contract.md':'d6dfe89f13e34210a7dbd3b4e68e7dff7fb488c93fdc73251a9d03c4b84459c8',
}
CHECKS, DETAILS, MUTATIONS = {}, {}, {}
t,theta,phi = s.symbols('t theta phi',real=True)
r,m,E,eps,ri = s.symbols('r m E epsilon r_i',positive=True)
Omega0 = s.symbols('Omega_0',positive=True)
coords = (t,r,theta,phi)
p = s.exp(-m/r)
coframe = s.diag(p,1/p,r/p,r*s.sin(theta)/p)
metric = coframe.T*s.diag(-1,1,1,1)*coframe
gd = [metric[i,i] for i in range(4)]


def simp(expression):
    return s.simplify(s.sympify(expression).doit())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(group,name,condition):
    CHECKS.setdefault(group,{})[name] = bool(condition)


def zero(group,name,expression):
    residual = simp(expression)
    check(group,name,residual == 0)
    if residual != 0:
        DETAILS.setdefault('failed_residuals',{})[name] = str(residual)
    return residual


def reject(name,residual,witness):
    residual = simp(residual)
    value = simp(residual.subs(witness))
    check('mutation_controls_checked',name,value != 0 and value.equals(0) is False)
    MUTATIONS[name] = {'residual':str(residual),'nonzero_witness':str(value)}


def geometry():
    Gamma = {}
    for i in range(4):
        for j in range(4):
            for k in range(4):
                z = simp((s.diff(metric[i,k],coords[j])+s.diff(metric[i,j],coords[k])
                          -s.diff(metric[j,k],coords[i]))/(2*gd[i]))
                if z != 0:
                    Gamma[i,j,k] = z
    def G(i,j,k):
        return Gamma.get((i,j,k),s.S.Zero)
    Riemann = {}
    kretsch = s.S.Zero
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    z = simp(s.diff(G(a,b,d),coords[c])-s.diff(G(a,b,c),coords[d])
                             +sum(G(a,l,c)*G(l,b,d)-G(a,l,d)*G(l,b,c) for l in range(4)))
                    if z != 0:
                        Riemann[a,b,c,d] = gd[a]*z
                        kretsch += gd[a]*z*z/(gd[b]*gd[c]*gd[d])
    Ricci = s.zeros(4)
    for b in range(4):
        for d in range(4):
            Ricci[b,d] = simp(sum(Riemann.get((a,b,a,d),0)/gd[a] for a in range(4)))
            zero('metric_geometry_checked',f'Ricci_{b}{d}',
                 Ricci[b,d]-(-2*m*m/r**4 if b==d==1 else 0))
    scalar = simp(sum(Ricci[i,i]/gd[i] for i in range(4)))
    zero('metric_geometry_checked','Ricci_scalar',scalar+2*m*m*p*p/r**4)
    weights = [1/p,p,p/r,p/(r*s.sin(theta))]
    sections = [simp(Riemann.get((a,b,a,b),0)*weights[a]**2*weights[b]**2)
                for a,b in ((0,1),(0,2),(1,2),(2,3))]
    targets = [2*m*(m-r)*p*p/r**4,m*(r-m)*p*p/r**4,
               -m*p*p/r**3,m*(2*r-m)*p*p/r**4]
    for name,actual,target in zip(('A','Bc','C','D'),sections,targets):
        zero('metric_geometry_checked','static_section_'+name,actual-target)
        zero('metric_geometry_checked','static_endpoint_'+name,s.limit(actual,r,0,dir='+'))
    A,Bc,C,D = sections
    zero('metric_geometry_checked','static_frame_Kretschmann',kretsch-4*(A*A+2*Bc*Bc+2*C*C+D*D))
    zero('metric_geometry_checked','Kretschmann_polynomial',
         kretsch-4*m*m*p**4*(7*m*m-16*m*r+12*r*r)/r**8)
    zero('metric_geometry_checked','scalar_endpoint',s.limit(scalar,r,0,dir='+'))
    zero('metric_geometry_checked','Kretschmann_endpoint',s.limit(kretsch,r,0,dir='+'))
    check('metric_geometry_checked','flat_Riemann',all(simp(z.subs(m,0))==0 for z in Riemann.values()))
    check('metric_geometry_checked','positive_p',p.is_positive)
    zero('metric_geometry_checked','areal_radius',metric[2,2]-(r/p)**2)
    DETAILS['geometry'] = {'metric':'diag(-p^2,p^-2,r^2*p^-2,r^2*sin(theta)^2*p^-2)',
        'p':str(p),'areal_radius':str(r/p),'Ricci_scalar':str(scalar),
        'Kretschmann':str(simp(kretsch)),'static_sections':dict(zip(('A','Bc','C','D'),map(str,sections)))}
    return G,Ricci,Riemann,sections


def trajectories(G):
    radial_square = s.symbols('radial_speed_squared',real=True)
    ut = E/(-gd[0])
    ur2 = s.solve(gd[0]*ut**2+gd[1]*radial_square+1,radial_square)[0]
    u = s.Matrix([ut,-s.sqrt(ur2),0,0])
    w = -u[1]
    def norm(k,g=metric):
        return simp((k.T*g*k)[0])
    def transport(k,z):
        return [simp(k[1]*s.diff(z[i],r)+sum(G(i,j,l)*k[j]*z[l] for j in range(4) for l in range(4)))
                for i in range(4)]
    zero('geodesics_checked','timelike_Killing_energy',-gd[0]*u[0]-E)
    zero('geodesics_checked','timelike_normalization',norm(u)+1)
    zero('geodesics_checked','timelike_radial_square',ur2-(E*E-p*p))
    for i,z in enumerate(transport(u,u)):
        zero('geodesics_checked',f'timelike_geodesic_{i}',z)
    kt = eps/(-gd[0])
    kr2 = s.solve(gd[0]*kt**2+gd[1]*radial_square,radial_square)[0]
    rays = {}
    for direction in (-1,1):
        k = s.Matrix([kt,direction*s.sqrt(kr2),0,0])
        rays[direction] = k
        zero('geodesics_checked',f'null_energy_{direction}',-gd[0]*k[0]-eps)
        zero('geodesics_checked',f'null_norm_{direction}',norm(k))
        zero('geodesics_checked',f'null_affine_speed_{direction}',k[1]-direction*eps)
        for i,z in enumerate(transport(k,k)):
            zero('geodesics_checked',f'null_geodesic_{direction}_{i}',z)
    no_spatial = s.diag(-p*p,1,r*r,r*r*s.sin(theta)**2)
    reject('omit_spatial_ruler_factor',norm(u,no_spatial)+1,{m:1,r:1,E:1})
    bad_affine = s.Matrix([kt,-eps*p*p,0,0])
    reject('coordinate_speed_as_affine_speed',norm(bad_affine),{m:1,r:1,eps:1})
    DETAILS['trajectory'] = {'domain':'m>0,r_i>0,E>=1; geodesic test centre only.',
        'timelike':list(map(str,u)),'null_inward':list(map(str,rays[-1])),
        'starting_radius':'finite; the infinite-distance fall from infinity is not the elapsed-time interval.'}
    return u,w,rays,transport


def readouts(u,w,k):
    static_u = s.Matrix([1/p,0,0,0])
    gamma = simp(-(u.T*metric*static_u)[0])
    v = simp((u[1]/p)/gamma)
    zero('external_readout_checked','local_gamma',gamma-E/p)
    zero('external_readout_checked','local_velocity',v+w/E)
    zero('external_readout_checked','Lorentz_norm',gamma**2*(1-v*v)-1)
    def clock_residual(candidate):
        return simp(candidate*u[0]-1)
    moving_clock = 1/u[0]
    zero('external_readout_checked','moving_clock',clock_residual(p*p/E))
    reject('stationary_clock_as_moving_clock',clock_residual(p),{m:1,r:1,E:1})
    reject('double_count_clock_factor',clock_residual(p*moving_clock),{m:1,r:1,E:1})
    zero('clock_interpretation_checked','proper_phase_clock',Omega0*moving_clock*u[0]-Omega0)
    coord_velocity = simp(u[1]/u[0])
    zero('external_readout_checked','coordinate_velocity',coord_velocity+p*p*w/E)
    ell,dr = s.symbols('rest_length dr',real=True)
    stationary_footprint = s.solve(ell-dr/p,dr)[0]/ell
    moving_footprint = s.solve(ell-gamma*dr/p,dr)[0]/ell
    zero('external_readout_checked','stationary_ruler',stationary_footprint-p)
    zero('external_readout_checked','equal_static_t_moving_ruler',moving_footprint-p*p/E)
    omega_em = simp(-(u.T*metric*k)[0])
    omega_infinity = s.limit(simp(-(static_u.T*metric*k)[0]),r,s.oo)
    ratio = simp(omega_infinity/omega_em)
    zero('external_readout_checked','outgoing_emitted_frequency',omega_em-eps*(E+w)/p**2)
    zero('external_readout_checked','asymptotic_received_frequency',omega_infinity-eps)
    zero('external_readout_checked','frequency_ratio',ratio-p*p/(E+w))
    zero('external_readout_checked','rationalized_frequency_ratio',ratio-(E-w))
    # Arrival differences at a fixed detector: the lower integration limit moves.
    rstar_prime = simp(k[0]/k[1])
    arrival_rate = simp(u[0]-rstar_prime*u[1])
    zero('external_readout_checked','arrival_derivative',arrival_rate-(E+w)/p**2)
    zero('external_readout_checked','pulse_frequency_reciprocity',arrival_rate*ratio-1)
    for name,z in (('static_clock',p),('moving_clock',moving_clock),('coordinate_motion',coord_velocity),
                   ('stationary_ruler',stationary_footprint),('moving_ruler',moving_footprint),('received_frequency',ratio)):
        zero('external_readout_checked',name+'_endpoint',s.limit(z,r,0,dir='+'))
    DETAILS['readout'] = {'moving_clock':str(simp(moving_clock)),
        'coordinate_velocity':str(coord_velocity),'moving_radial_snapshot':str(simp(moving_footprint)),
        'stationary_and_transverse_factor':str(p),'photon_ratio':str(ratio),'arrival_rate':str(arrival_rate),
        'protocol':'Infinitesimal rod at equal static t; photon receiver uses normalized retarded arrival differences.',
        'not_computed':'Finite image, core deformation, self-gravity or local oscillon survival.'}
    return arrival_rate


def clock_interpretation(u,w,arrival):
    rate = u[0]
    lower,upper = rate.subs(r,ri),rate.subs(r,ri/2)
    zero('clock_interpretation_checked','rate_derivative',s.diff(rate,r)+2*m*rate/r**2)
    check('clock_interpretation_checked','rate_decreases_with_radius',s.diff(rate,r).is_negative)
    zero('clock_interpretation_checked','segment_lower',lower-E*s.exp(2*m/ri))
    zero('clock_interpretation_checked','segment_upper',upper-E*s.exp(4*m/ri))
    # r=ri/(1+y), 0<=y<=1; z=1-y for the complementary upper-end gap.
    y,z = s.symbols('segment_y segment_complement',nonnegative=True)
    gap_l = 2*lower*s.exp(m*y/ri)*s.sinh(m*y/ri)
    gap_u = 2*upper*s.exp(-m*z/ri)*s.sinh(m*z/ri)
    zero('clock_interpretation_checked','lower_gap_certificate',
         (rate.subs(r,ri/(1+y))-lower-gap_l).rewrite(s.exp))
    zero('clock_interpretation_checked','upper_gap_certificate',
         (upper-rate.subs(r,ri/(2-z))-gap_u).rewrite(s.exp))
    measure = s.symbols('positive_proper_time_measure',positive=True)
    check('clock_interpretation_checked','integrated_lower_gap',(gap_l*measure).is_nonnegative)
    check('clock_interpretation_checked','integrated_upper_gap',(gap_u*measure).is_nonnegative)
    check('clock_interpretation_checked','finite_segment_rate_bounds',lower.is_finite and upper.is_finite)
    check('clock_interpretation_checked','unbounded_elapsed_ratio',s.limit(lower,ri,0,dir='+')==s.oo)
    zero('clock_interpretation_checked','arrival_ratio_lower_gap',arrival/rate-1-w/E)
    zero('clock_interpretation_checked','arrival_ratio_upper_gap',2-arrival/rate-p*p/(E*(E+w)))
    ee,ww,pp = s.symbols('positive_energy positive_inward_speed positive_scale',positive=True)
    check('clock_interpretation_checked','strict_arrival_bounds',
          (ww/ee).is_positive and (pp*pp/(ee*(ee+ww))).is_positive)
    DETAILS['clock_comparison'] = {'segment':'r_i to r_i/2, r_i>0',
        'elapsed_ratio_bound':'E*exp(2m/r_i) <= Delta_t/Delta_tau <= E*exp(4m/r_i)',
        'phase_clock':'dchi=Omega_0*d tau; dchi/dt=Omega_0*p^2/E',
        'arrival_comparison':'Delta_t < Delta_t_arr < 2*Delta_t for normalized detector timestamps.',
        'scope':'Each finite segment has finite durations; arbitrarily large ratios need no infinite own duration.'}


def elapsed(u,w,k,arrival_rate):
    pi = p.subs(r,ri)
    wi = s.sqrt(E*E-pi*pi)
    zero('elapsed_time_checked','proper_integrand',-1/u[1]-1/w)
    zero('elapsed_time_checked','lower_integrand_certificate',
         1/w-1/E-p*p/(E*w*(E+w)))
    zero('elapsed_time_checked','upper_integrand_certificate',
         1/wi-1/w-(pi*pi-p*p)/(wi*w*(wi+w)))
    # These positive denominators and the monotone p establish the entire finite interval bound.
    ww,wwi,pp,ee = s.symbols('w_positive wi_positive p_positive E_positive',positive=True)
    delta = s.symbols('pi_squared_minus_p_squared',nonnegative=True)
    check('elapsed_time_checked','lower_gap_positive',(pp*pp/(ee*ww*(ee+ww))).is_positive)
    check('elapsed_time_checked','upper_gap_nonnegative',(delta/(wwi*ww*(wwi+ww))).is_nonnegative)
    check('elapsed_time_checked','p_increases_with_r',s.diff(p,r).is_positive)
    initial_gap = 2*pi*s.sinh(m/ri)
    zero('elapsed_time_checked','initial_gap_certificate',(1-pi*pi-initial_gap).rewrite(s.exp))
    check('elapsed_time_checked','initial_p_below_one',initial_gap.is_positive)
    energy_margin = s.symbols('E_squared_minus_one',nonnegative=True)
    check('elapsed_time_checked','E_ge_1_implies_positive_initial_w_squared',
          (energy_margin+initial_gap).is_positive)
    lam,lam0 = s.symbols('lambda lambda0',real=True)
    rray = ri+k[1]*(lam-lam0)
    zero('elapsed_time_checked','finite_affine_endpoint',rray.subs(lam,lam0+ri/eps))
    check('elapsed_time_checked','affine_interval_finite',(ri/eps).is_finite)
    time_integrand = simp(-u[0]/u[1])
    zero('elapsed_time_checked','external_time_comparison',time_integrand-p**-2-1/(w*(E+w)))
    check('elapsed_time_checked','external_time_gap_positive',(1/(ww*(ee+ww))).is_positive)
    check('elapsed_time_checked','exponential_dominates_inverse_square',
          s.limit(r*r/(m*m*p*p),r,0,dir='+')==s.oo)
    cutoff,z = s.symbols('cutoff z',positive=True)
    lower_integral = s.integrate(m*m/z**2,(z,cutoff,ri))
    check('elapsed_time_checked','comparison_integral_diverges',s.limit(lower_integral,cutoff,0,dir='+')==s.oo)
    zero('elapsed_time_checked','arrival_integrand_comparison',arrival_rate/w-time_integrand-p**-2)
    DETAILS['elapsed'] = {'proper_time_bound':'r_i/E <= Delta_tau <= r_i/sqrt(E^2-p_i^2) < infinity',
        'affine_interval':str(ri/eps),'external_time':'Diverges by exact inverse-square comparison.',
        'arrival_time':'Normalized arrival differences diverge; proper duration remains finite.'}
    DETAILS['verification_audit'] = {
        'first_endpoint_sha256':'bae6a279d6d67daf2238f82064d238af25ea674a968e2c71c96e9b4b2a46193c',
        'first_failed_gates':['initial_p_below_one','E_ge_1_implies_positive_initial_w_squared'],
        'correction':'Undecided sign queries replaced by 2*p_i*sinh(m/r_i)>0; its identity is simplified in exponential form.',
        'intermediate_sha256':'05df80afd55b8f66040c1bc811e8200c25e7e2e19eaf0071997266d7e3742d5a',
        'intermediate_issue':'Positive certificate accepted; mixed sinh/exp identity needed an explicit exponential rewrite.',
        'physical_contract_changed':False}


def falling_curvature(Ricci,Riemann,sections,u,w,k,transport):
    B = r/p
    Rkk = simp((k.T*Ricci*k)[0])
    Ruu = simp((u.T*Ricci*u)[0])
    def null_projection(candidate):
        return simp((k.T*candidate*k)[0]+2*eps**2*s.diff(B,r,2)/B)
    zero('falling_curvature_checked','areal_second_derivative',s.diff(B,r,2)/B-m*m/r**4)
    zero('falling_curvature_checked','null_warped_geometry',null_projection(Ricci))
    zero('falling_curvature_checked','null_Ricci',Rkk+2*eps*eps*m*m/r**4)
    zero('falling_curvature_checked','timelike_Ricci',Ruu+2*m*m*(E*E-p*p)/r**4)
    bad = Ricci.copy(); bad[1,1] = 0
    reject('remove_radial_Ricci',null_projection(bad),{m:1,r:1,eps:1})
    e2 = s.Matrix([0,0,p/r,0])
    zero('falling_curvature_checked','transverse_unit',(e2.T*metric*e2)[0]-1)
    zero('falling_curvature_checked','transverse_orthogonal',(e2.T*metric*u)[0])
    for i,z in enumerate(transport(u,e2)):
        zero('falling_curvature_checked',f'transverse_parallel_transport_{i}',z)
    tide = simp(sum(z*u[a]*e2[b]*u[c]*e2[d] for (a,b,c,d),z in Riemann.items()))
    A,Bc,C,D = sections
    zero('falling_curvature_checked','boosted_tidal_crosscheck',tide-(E/p)**2*(Bc+(w/E)**2*C))
    zero('falling_curvature_checked','physical_transverse_tide',tide-(-E*E*m*m/r**4+m*p*p/r**3))
    for name,z in (('null_Ricci',Rkk),('timelike_Ricci',Ruu),('transported_tide',tide)):
        check('falling_curvature_checked',name+'_unbounded',s.limit(z,r,0,dir='+')==-s.oo)
    check('falling_curvature_checked','internal_cycle_tide_unbounded',
          s.limit(tide/Omega0**2,r,0,dir='+')==-s.oo)
    DETAILS['endpoint'] = {'Rkk':str(Rkk),'Ruu':str(Ruu),'parallel_transverse_tidal':str(tide),
        'interpretation':'Finite-proper/affine endpoint with unbounded freely transported curvature; static scalars vanish.',
        'finite_domain':'Metric and transported curvature are finite at every r>0; divergence concerns only the limiting endpoint.',
        'scope':'Endpoint curvature is separate from the verified exterior-clock comparison; neither rejects the full RefG action.'}


def main():
    before = {p:sha(ROOT/p) for p in PINS}
    for path,target in PINS.items():
        check('provenance',path,before[path]==target)
    if not all(CHECKS['provenance'].values()):
        print(json.dumps({'status':'FAIL','checks':CHECKS,'source_hashes':before},indent=2,allow_nan=False))
        return 1
    G,Ricci,Riemann,sections = geometry()
    u,w,rays,transport = trajectories(G)
    arrival = readouts(u,w,rays[1])
    elapsed(u,w,rays[-1],arrival)
    clock_interpretation(u,w,arrival)
    falling_curvature(Ricci,Riemann,sections,u,w,rays[-1],transport)
    check('provenance','protected_sources_unchanged',all(sha(ROOT/path)==before[path] for path in PINS))
    flags = {g:bool(rows and all(rows.values())) for g,rows in CHECKS.items()}
    passed = all(flags.values())
    external_groups = ('provenance','metric_geometry_checked','geodesics_checked',
                       'external_readout_checked','elapsed_time_checked','clock_interpretation_checked')
    external_mutations = ('omit_spatial_ruler_factor','coordinate_speed_as_affine_speed',
                          'stationary_clock_as_moving_clock','double_count_clock_factor')
    flags['external_asymptotic_suppression_verified'] = (
        all(flags[g] for g in external_groups)
        and all(CHECKS['mutation_controls_checked'][name] for name in external_mutations))
    flags['exponential_endpoint_pp_curvature_singular'] = (
        all(flags[g] for g in ('provenance','metric_geometry_checked','geodesics_checked',
                              'elapsed_time_checked','falling_curvature_checked'))
        and CHECKS['mutation_controls_checked']['remove_radial_Ricci'])
    flags['proper_time_infinity_required'] = False
    flags.update({name:False for name in ('full_RefG_rejected','W51_weak_result_rejected','W87_rejected',
        'singularity_resolved','regular_black_hole','full_action_solution','microscopic_completion',
        'observational_pass','active_theory_changed','intuitive_files_changed')})
    print(json.dumps({'package':'W3-91-v1.1','status':'PASS' if passed else 'FAIL',
        'physical_status':{
            'exterior_clock_target':'VERIFIED' if flags['external_asymptotic_suppression_verified'] else 'UNRESOLVED',
            'limiting_endpoint':'PP_CURVATURE_SINGULAR' if flags['exponential_endpoint_pp_curvature_singular'] else 'UNRESOLVED'},
        'revision':{'previous_verifier_sha256':'eb2ff9525907d74a0812c51423f159f10be75e5a4fefaad22158992cfa4416b8',
            'change':'Removed the incorrectly attributed infinite-own-time requirement; separated clock and curvature decisions.',
            'metric_and_geodesic_formulas_changed':False},
        'check_count':sum(map(len,CHECKS.values())),'checks':CHECKS,'closure_flags':flags,
        'negative_controls':MUTATIONS,'details':DETAILS,'source_hashes':before,
        'verifier_sha256':sha(HERE),'versions':{'Python':platform.python_version(),'SymPy':s.__version__}},
        indent=2,allow_nan=False))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
