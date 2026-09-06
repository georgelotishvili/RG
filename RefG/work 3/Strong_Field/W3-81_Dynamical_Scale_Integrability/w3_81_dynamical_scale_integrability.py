#!/usr/bin/env python3
"""W3-81 full-action Cauchy-jet diagnostic; finite stdout JSON, no file writes."""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import hashlib
import importlib.util
import json
import math
import platform
from pathlib import Path
import sympy as sp

SOURCE=Path(__file__).resolve()
ROOT=SOURCE.parents[4]
CONTRACT=SOURCE.with_name('w3_81_dynamical_scale_integrability_contract.md')
CONTRACT_SHA='43b5bc7586afc323dbb64129bcb74f154b990c54dd82e33603a394f59c1aff88'
SF='RefG/work 3/Strong_Field/'
W73=SF+'W3-73_Coupled_Horizon_Regular_Einstein_Complex_Scalar/w3_73_coupled_horizon_regular_einstein_complex_scalar.py'
PINS={
 'CODES.md':'27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41',
 SF+'W3-71_Horizon_Material_Scale_Separation/w3_71_horizon_material_scale_separation_preregistration.md':
 '1d3f74489f6cc52061253b6e1ea3d7f96e5d423f8b2afb88e79a44a38ae916c3',
 W73:'47f2c97b64544f124cc2a5cb8d04825188664493cb5d770b6c3faf4ce2d5d7ca',
 SF+'W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction_contract.md':
 '7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa',
 SF+'W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction.py':
 '4efe86c593db5ad9f5dfb7a1efe1aa0f4d5f2ea0af410d25ba1c7743534c5672',
 SF+'W3-80_Resonant_Constitutive_Candidate/w3_80_neutral_resonant_condensate_contract.md':
 '27e359b9980df14a287ca89cc38a895eb5015a732154d7a055fd7666b418d841',
 SF+'W3-80_Resonant_Constitutive_Candidate/w3_80_neutral_resonant_condensate.py':
 'da4c0c7574e5ef9b8347562d628bff31b9be8c14c5417f29c185f977c0eb7381'}
FALSE_FLAGS=('universal_scale_map_derived','P_F_bridge_derived','full_time_evolution_solved',
             'singularity_resolved','observational_pass','active_theory_changed','intuitive_files_changed')

def clean(value):
    return sp.factor(sp.simplify(value))

def audit(values):
    residuals={key:clean(value) for key,value in values.items()}
    return dict(all_pass=all(value==0 for value in residuals.values()),
                residuals={key:sp.sstr(value) for key,value in residuals.items()},
                checks={key:bool(value==0) for key,value in residuals.items()})

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def provenance():
    dependencies={key:dict(expected=value,actual=sha(ROOT/key)) for key,value in PINS.items()}
    files=sorted(p.name for p in SOURCE.parent.iterdir())
    out=dict(dependencies=dependencies,contract_sha256=sha(CONTRACT),expected_contract_sha256=CONTRACT_SHA,
             source_sha256=sha(SOURCE),package_files=files,python=platform.python_version(),
             sympy=sp.__version__,bytecode_disabled=sys.dont_write_bytecode)
    out['all_pass']=(all(v['expected']==v['actual'] for v in dependencies.values())
        and out['contract_sha256']==CONTRACT_SHA and sys.dont_write_bytecode
        and files==sorted([SOURCE.name,CONTRACT.name]))
    return out

def geometry():
    spec=importlib.util.spec_from_file_location('w81_w73_geometry',ROOT/W73)
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module,module.geometry_base()  # Pure geometry only; never the old main/result reader.

def full_source_variation():
    R,m,lam=sp.symbols('R m lambda',positive=True)
    eps=sp.symbols('epsilon',real=True)
    eta=sp.diag(-1,1,1,1)
    a=sp.Matrix(sp.symbols('R_0:4',real=True)); q=sp.Matrix(sp.symbols('theta_0:4',real=True))
    potential=m*m*R*R/2+lam*R**4/4
    lag=-(a.T*eta*a)[0]/2-R*R*(q.T*eta*q)[0]/2-potential
    expected=eta*a*a.T*eta+R*R*eta*q*q.T*eta+eta*lag
    residuals={}
    for i in range(4):
        residuals[f'phase_Noether_{i}']=sp.diff(lag,q[i])+R*R*(eta*q)[i]
    for i in range(4):
        for j in range(i,4):
            delta=sp.zeros(4); delta[i,j]=1; delta[j,i]=1
            g=eta+eps*delta; inverse=g.inv()
            density=sp.sqrt(-g.det())*(-(a.T*inverse*a)[0]/2-R*R*(q.T*inverse*q)[0]/2-potential)
            weight=sp.Rational(1,2) if i==j else 1
            residuals[f'Hilbert_variation_{i}{j}']=sp.diff(density,eps).subs(eps,0)-weight*expected[i,j]
    principal=sp.Matrix(2,2,lambda i,j:sum(sp.diff(lag,(a,q)[i][u],(a,q)[j][v])*q[u]*q[v]
                                         for u in range(4) for v in range(4)))
    residuals['full_polar_metric_null_principal']=principal.det()-R*R*(q.T*eta*q)[0]**2
    return audit(residuals)

def matter_geometry_jet(w,g):
    t=w.T; r=sp.symbols('r',positive=True)
    m,lam,R0,A,b,G=sp.symbols('m lambda R0 A b G',positive=True)
    mu=sp.sqrt(m*m+lam*R0*R0); rho=m*m*R0*R0+3*lam*R0**4/4
    pressure=lam*R0**4/4; enthalpy=rho+pressure; density=R0*R0*mu
    replacement={w.R:r}; cv=lambda value:value.xreplace(replacement)
    sig=cv(w.SIGMA); z=cv(w.ZETA); metric=cv(g['metric']); inv=cv(g['inverse'])
    amp=sp.Function('amplitude')(t,r); phase=sp.Function('phase')(t,r)
    grads=lambda f:sp.Matrix([sp.diff(f,t),sp.diff(f,r),0,0])
    da,dt=grads(amp),grads(phase); X=-(dt.T*inv*dt)[0]
    potential=m*m*amp*amp/2+lam*amp**4/4
    lag=-(da.T*inv*da)[0]/2-amp*amp*(dt.T*inv*dt)[0]/2-potential
    measure=sig*r*r
    def euler(f):
        return (sp.diff(measure*lag,f)-sp.diff(sp.diff(measure*lag,sp.diff(f,t)),t)
                -sp.diff(sp.diff(measure*lag,sp.diff(f,r)),r))/measure
    def box(f):
        v=inv*grads(f)
        return (sp.diff(measure*v[0],t)+sp.diff(measure*v[1],r))/measure
    current=-amp*amp*inv*dt
    continuity=(sp.diff(measure*current[0],t)+sp.diff(measure*current[1],r))/measure
    amplitude_eq=box(amp)+amp*X-sp.diff(potential,amp)
    z0=sp.sqrt(A/r+b*r*r); theta0=clean(-sp.diff(z0,r)-2*z0/r)
    b_source=8*sp.pi*G*rho/3
    zt=clean((z0*sp.diff(z0,r)+z0*z0/(2*r)+4*sp.pi*G*r*pressure).subs(b,b_source))
    Rtt,Ptt=sp.symbols('R_TT theta_TT',real=True)
    jets={amp:R0,phase:0,sig:1,z:z0,sp.diff(sig,t):0,sp.diff(sig,r):0,
          sp.diff(sig,r,2):0,sp.diff(sig,t,r):0,sp.diff(z,t):zt,
          sp.diff(z,r):sp.diff(z0,r),sp.diff(z,r,2):sp.diff(z0,r,2),
          sp.diff(z,t,r):sp.diff(zt,r),sp.diff(amp,t):0,sp.diff(amp,r):0,
          sp.diff(amp,t,2):Rtt,sp.diff(amp,t,r):0,sp.diff(amp,r,2):0,
          sp.diff(phase,t):mu,sp.diff(phase,r):0,sp.diff(phase,t,2):Ptt,
          sp.diff(phase,t,r):0,sp.diff(phase,r,2):0}
    at=lambda expr:clean(expr.subs(jets,simultaneous=True).doit())
    equations=(at(amplitude_eq),at(continuity))
    solution=sp.solve(equations,(Rtt,Ptt),dict=True)[0]
    jets.update({sp.diff(amp,t,2):solution[Rtt],sp.diff(phase,t,2):solution[Ptt],
                 sp.diff(phase,t,2,r):sp.diff(solution[Ptt],r)})
    mut=at(sp.diff(sp.sqrt(X),t)); nt=at(sp.diff(amp*amp*sp.sqrt(X),t))
    PiR=sp.diff(amp,t)/sig-z*sp.diff(amp,r); PhiR=sp.diff(amp,r)
    PiT=sp.diff(phase,t)/sig-z*sp.diff(phase,r); PhiT=sp.diff(phase,r)
    kin=(PiR**2+PhiR**2+amp*amp*(PiT**2+PhiT**2))/2
    stresses=[kin+potential,PiR*PhiR+amp*amp*PiT*PhiT,kin-potential,
              (PiR**2-PhiR**2+amp*amp*(PiT**2-PhiT**2))/2-potential]
    source_checks={'PG_amplitude_action_variation':euler(amp)-amplitude_eq,
                   'PG_phase_action_variation':euler(phase)+continuity}
    covstress=da*da.T+amp*amp*dt*dt.T+metric*lag
    normal=sp.Matrix([1/sig,-z,0,0]); radial=sp.Matrix([0,1,0,0])
    direct=[(normal.T*covstress*normal)[0],(normal.T*covstress*radial)[0],
            (radial.T*covstress*radial)[0],covstress[2,2]/r**2]
    for i in range(4):
        source_checks[f'Hilbert_frame_projection_{i}']=direct[i]-stresses[i]
    source=audit(source_checks)
    matter_checks={'amplitude_equation':at(amplitude_eq),'phase_equation':at(continuity),
                   'amplitude_second_time_derivative':solution[Rtt],
                   'phase_second_time_derivative':solution[Ptt]+mu*theta0,
                   'chemical_potential_derivative':mut+mu*theta0,
                   'derived_mixed_phase_derivative':sp.diff(solution[Ptt],r)+mu*sp.diff(theta0,r),
                   'density_current_balance':nt+density*theta0,
                   'initial_current_T':at(current[0])-density,
                   'initial_current_r':at(current[1])+z0*density}
    for i,target in enumerate((rho,0,pressure,pressure)):
        matter_checks[f'initial_stress_{i}']=at(stresses[i])-target
    stress_time=[at(sp.diff(expr,t)) for expr in stresses]
    for i,target in enumerate((-enthalpy*theta0,0,-enthalpy*theta0,-enthalpy*theta0)):
        matter_checks[f'stress_time_derivative_{i}']=stress_time[i]-target
    # Independent Cartesian equations and reconstruction of the two polar jets.
    fields=[sp.Function('phi1')(t,r),sp.Function('phi2')(t,r)]
    ftt=sp.symbols('phi1_TT phi2_TT',real=True)
    cartjets=dict(jets)
    for i,f in enumerate(fields):
        cartjets.update({f:(R0,0)[i],sp.diff(f,t):(0,mu*R0)[i],sp.diff(f,r):0,
                        sp.diff(f,t,2):ftt[i],sp.diff(f,t,r):0,sp.diff(f,r,2):0})
    cart_eq=[box(f)-m*m*f-lam*(fields[0]**2+fields[1]**2)*f for f in fields]
    cartsol=sp.solve([clean(e.subs(cartjets,simultaneous=True)) for e in cart_eq],ftt,dict=True)[0]
    matter_checks['Cartesian_to_polar_amplitude_jet']=cartsol[ftt[0]]+R0*mu*mu-solution[Rtt]
    matter_checks['Cartesian_to_polar_phase_jet']=cartsol[ftt[1]]/R0-solution[Ptt]
    matter=audit(matter_checks)
    geo_checks={}
    for key,target in (('g00',rho),('g01',0),('g11',pressure),('g22',pressure)):
        geo_checks['Einstein_'+key]=at(cv(g[key])).subs(b,b_source)-8*sp.pi*G*target
    mass=r*z*z/(2*G)
    mass_r=at(sp.diff(mass,r)); mass_t=at(sp.diff(mass,t))
    geo_checks.update(initial_mass=at(mass).subs(b,b_source)-A/(2*G)-4*sp.pi*rho*r**3/3,
        mass_radial=mass_r.subs(b,b_source)-4*sp.pi*r*r*rho,
        mass_temporal=mass_t-4*sp.pi*r*r*z0*enthalpy,
        mass_integrability=4*sp.pi*r*r*stress_time[0]-sp.diff(4*sp.pi*r*r*z0*enthalpy,r),
        zeta_time_evolution=zt-4*sp.pi*G*r*enthalpy)
    lapse_rhs=-4*sp.pi*G*r*sig*stresses[1]/z
    geo_checks['differentiated_lapse_momentum_constraint']=at(sp.diff(lapse_rhs,t))
    geo_checks['Lorentzian_PG_determinant']=at(metric.det())+r**4*sp.sin(w.THETA)**2
    gravity=audit(geo_checks)
    return source,matter,gravity,dict(t=t,r=r,m=m,lam=lam,R0=R0,mu=mu,rho=rho,
        pressure=pressure,n=density,A=A,b=b,G=G,b_source=b_source,z0=z0,Theta=theta0,
        mu_T=mut,phase_TT=solution[Ptt],R_TT=solution[Rtt],zeta_T=zt,
        phase_equation_initial=equations[1],phase_TT_symbol=Ptt,Einstein00=at(cv(g['g00'])))

def christoffels(metric,coords):
    inverse=metric.inv()
    return [[[clean(sum(inverse[i,l]*(sp.diff(metric[l,k],coords[j])+sp.diff(metric[l,j],coords[k])
                         -sp.diff(metric[j,k],coords[l]))/2 for l in range(2)))
              for k in range(2)] for j in range(2)] for i in range(2)]

def normalized_gradient_identity():
    q0,q1=sp.symbols('theta_t theta_r',real=True)
    h00,h01,h11=sp.symbols('theta_tt theta_tr theta_rr',real=True)
    eta=sp.diag(-1,1); q=sp.Matrix([q0,q1]); H=sp.Matrix([[h00,h01],[h01,h11]])
    mu=sp.sqrt(-(q.T*eta*q)[0]); cov=-q/mu; up=eta*cov
    dmu=sp.Matrix([sum(sp.diff(mu,q[j])*H[j,i] for j in range(2)) for i in range(2)])
    du=sp.Matrix(2,2,lambda i,b:sum(sp.diff(cov[i],q[j])*H[j,b] for j in range(2)))
    acceleration=du*up
    projected=-(sp.eye(2)+cov*up.T)*dmu/mu
    return audit({f'normalized_gradient_acceleration_{i}':acceleration[i]-projected[i] for i in range(2)})

def curl_and_controls(c):
    t,r=c['t'],c['r']; mu=sp.symbols('mu0',positive=True)
    z=sp.Function('z0')(r); zdot=sp.Function('zeta_dot')(r)
    Theta=-sp.diff(z,r)-2*z/r
    zjet=z+t*zdot
    metric=sp.Matrix([[zjet*zjet-1,zjet],[zjet,1]])
    inverse=metric.inv(); gamma=christoffels(metric,(t,r))
    # These Taylor representatives encode only the already derived initial jets;
    # no finite-T solution or time stepping is asserted.
    theta=mu*t-mu*Theta*t*t/2
    gradient=sp.Matrix([sp.diff(theta,t),sp.diff(theta,r)])
    X=-(gradient.T*inverse*gradient)[0]
    chemical=sp.sqrt(X); cov=-gradient/chemical; up=inverse*cov
    expansion=sp.diff(up[0],t)+sp.diff(up[1],r)+2*up[1]/r
    acceleration=sp.Matrix([sum(up[b]*(sp.diff(cov[a],(t,r)[b])
                -sum(gamma[d][b][a]*cov[d] for d in range(2))) for b in range(2)) for a in range(2)])
    at=lambda expr:clean(expr.subs(t,0).doit())
    arT=at(sp.diff(acceleration[1],t))
    W=acceleration+expansion*cov/5
    actual_curl=at(sp.diff(W[1],t)-sp.diff(W[0],r))
    projected_arT=-sp.diff(c['mu_T']/c['mu'],r)
    to_state=lambda expr:clean(expr.subs(z,c['z0']).doit())
    actual=to_state(actual_curl); direct_ar=to_state(arT)
    residuals={'phase_jet_representative':to_state(at(sp.diff(theta,t,2))).subs(mu,c['mu'])-c['phase_TT'],
      'flow_normalization':at((cov.T*up)[0])+1,'initial_flow_time':at(up[0])-1,
      'initial_flow_radial':at(up[1])+z,'initial_covariant_radial_velocity':at(cov[1]),
      'initial_covariant_radial_velocity_derivative':at(sp.diff(cov[1],t)),
      'expansion_direct':at(expansion)-Theta,'initial_acceleration_r':at(acceleration[1]),
      'initial_acceleration_T':at(acceleration[0]),
      'independent_acceleration_derivative':direct_ar-projected_arT,
      'curl_direct_vs_projected':actual-(projected_arT+sp.diff(c['Theta'],r)/5)}
    curl=audit(residuals)
    expected_derivative=9*c['A']**2/(4*r**4*c['z0']**3)
    branches={'radial_Theta_derivative':sp.diff(c['Theta'],r)-expected_derivative,
       'homogeneous_curl':clean(actual.subs(c['A'],0)),
       'homogeneous_expansion_gradient':sp.diff(c['Theta'].subs(c['A'],0),r),
       'homogeneous_current_and_scale':c['mu_T']/c['mu']/5+c['Theta']/5}
    lapse=sp.Function('N',positive=True)(r)
    static_metric=sp.diag(-lapse*lapse,1); static_gamma=christoffels(static_metric,(t,r))
    u=sp.Matrix([1/lapse,0]); uc=static_metric*u
    static_div=(sp.diff(lapse*r*r*u[0],t)+sp.diff(lapse*r*r*u[1],r))/(lapse*r*r)
    static_ar=sum(u[b]*(sp.diff(uc[1],(t,r)[b])-sum(static_gamma[d][b][1]*uc[d] for d in range(2))) for b in range(2))
    static_at=sum(u[b]*(sp.diff(uc[0],(t,r)[b])-sum(static_gamma[d][b][0]*uc[d] for d in range(2))) for b in range(2))
    branches.update(static_expansion=static_div,static_lapse_connection=static_ar-sp.diff(sp.log(lapse),r),
                    static_connection_time=static_at,static_curl=sp.diff(static_ar,t)-sp.diff(static_at,r))
    branch=audit(branches)
    curl['diagnostic']={'F_Tr':sp.sstr(actual),'Theta':sp.sstr(c['Theta']),
        'Theta_r':sp.sstr(clean(sp.diff(c['Theta'],r))),
        'F_Tr_positive_in_declared_domain':bool(actual.is_positive),
        'geometric_curl_not_physical_clock_holonomy':True}
    return curl,branch,actual,direct_ar

def production_validator(c,actual_curl,arT,config):
    r=c['r']; candidate_muT=sp.S.Zero if config['force_minimum_evolution'] else c['mu_T']
    phase_residual=c['phase_equation_initial'].subs(c['phase_TT_symbol'],candidate_muT)
    candidate_ar=0 if config['zero_acceleration_derivative'] else arT
    candidate_curl=candidate_ar+sp.Rational(config['expansion_coefficient'])*sp.diff(c['Theta'],r)
    return audit({'Christoffel_acceleration_derivative':candidate_ar-arT,
       'declared_connection_curl':candidate_curl-actual_curl,
       'one_collective_Einstein_source':c['Einstein00'].subs(c['b'],c['b_source'])
                                  -8*sp.pi*c['G']*config['source_count']*c['rho'],
       'full_phase_equation_with_derived_amplitude_jet':phase_residual})

def mutations(c,F,arT):
    base=dict(force_minimum_evolution=False,zero_acceleration_derivative=False,
              expansion_coefficient=sp.Rational(1,5),source_count=1)
    controls={}; production=production_validator(c,F,arT,base)
    for name,key,value in (('zero_acceleration_jet','zero_acceleration_derivative',True),
                          ('deleted_expansion_connection','expansion_coefficient',0),
                          ('doubled_collective_source','source_count',2),
                          ('time_differentiated_minimum','force_minimum_evolution',True)):
        config=dict(base); config[key]=value; test=production_validator(c,F,arT,config)
        controls[name]=dict(detected=not test['all_pass'],
           failed_identities=[k for k,v in test['checks'].items() if not v],
           residuals={k:v for k,v in test['residuals'].items() if v!='0'})
    return dict(production=production,controls=controls,
                all_pass=production['all_pass'] and all(v['detected'] for v in controls.values()))

def numerical(c,F):
    values={c['m']:1,c['lam']:1,c['R0']:1,c['A']:1,c['b']:sp.Rational(1,100),
            c['G']:3/(1400*sp.pi)}
    fn=sp.lambdify(c['r'],c['Theta'].subs(values),'math')
    derivative=sp.lambdify(c['r'],sp.diff(c['Theta'],c['r']).subs(values),'math')
    curl=sp.lambdify(c['r'],F.subs(values),'math'); records=[]
    for r in (2.0,3.0,4.0):
        exact=float(derivative(r)); differences=[]
        for fractional_h in (1e-3,5e-4):
            h=r*fractional_h; fd=(fn(r+h)-fn(r-h))/(2*h)
            differences.append(dict(h_over_r=fractional_h,value=fd,relative_error=abs(fd-exact)/abs(exact)))
        errors=[v['relative_error'] for v in differences]
        Fvalue=float(curl(r)); z2=1/r+0.01*r*r
        finite=all(math.isfinite(v) for v in [exact,Fvalue,z2,fn(r)]+[item['value'] for item in differences])
        records.append(dict(r=r,Theta=fn(r),Theta_r=exact,F_Tr=Fvalue,F_Tr_positive=Fvalue>0,
           zeta_squared=z2,differences=differences,
           passed=finite and z2<1 and max(errors)<2e-5 and errors[1]<=0.35*errors[0]+1e-10))
    relation=clean((c['b']-c['b_source']).subs(values))
    return dict(parameters={'m_C':1,'lambda_C':1,'R0':1,'rho0':'7/4','P0':'1/4',
               'mu0':'sqrt(2)','A':1,'b':'1/100','G':'3/(1400*pi)'},records=records,
               b_source_relation_exact=relation==0,all_pass=relation==0 and all(row['passed'] for row in records))

def main():
    print('W81: pins, full action and independent Einstein geometry',file=sys.stderr,flush=True)
    prov=provenance()
    if not prov['all_pass']:
        print(json.dumps(dict(status='FAIL_PROVENANCE',provenance=prov),allow_nan=False)); return 1
    action=full_source_variation(); w,g=geometry()
    source,matter,gravity,c=matter_geometry_jet(w,g)
    print('W81: direct Christoffel/phase-gradient curl and frozen crosschecks',file=sys.stderr,flush=True)
    identity=normalized_gradient_identity(); curl,branches,F,arT=curl_and_controls(c)
    controls=mutations(c,F,arT); nums=numerical(c,F)
    groups=dict(action=action,source=source,matter_jet=matter,Einstein_jet=gravity,
                gradient_identity=identity,curl=curl,branches=branches)
    verified=prov['all_pass'] and all(v['all_pass'] for v in groups.values()) and controls['all_pass'] and nums['all_pass']
    nonzero=bool(F.is_positive) and all(row['F_Tr_positive'] for row in nums['records'])
    rejected=bool(verified and nonzero)
    flags=dict(action_source_checked=action['all_pass'] and source['all_pass'],
      einstein_cauchy_jet_checked=gravity['all_pass'],matter_cauchy_jet_checked=matter['all_pass'],
      independent_curl_checked=identity['all_pass'] and curl['all_pass'],branch_regressions_checked=branches['all_pass'],
      numerical_crosscheck_passed=nums['all_pass'],mutation_controls_passed=controls['all_pass'],
      universal_extension_rejected=rejected)
    flags.update({key:False for key in FALSE_FLAGS})
    result=dict(claim_id='W3_81_FULL_CONDENSATE_DYNAMIC_SCALE_INTEGRABILITY',model_version='W3-81-v1.0',
      status='PASS_EXACT_LOCAL_DYNAMIC_COUNTEREXAMPLE_TEST' if verified else 'FAIL_W81_DIAGNOSTIC',
      proposed_universal_extension='REJECTED' if rejected else 'OPEN',artifact_valid=bool(verified),
      provenance=prov,closure_flags=flags,exact_groups=groups,numerical=nums,negative_controls=controls,
      initial_jets={key:sp.sstr(c[key]) for key in ('mu_T','phase_TT','R_TT','zeta_T')},
      minimum_relation_time_derivative=sp.sstr(clean(2*c['mu']*c['mu_T'])),
      scope='Only W=d ln p_t on every full condensate flow is tested; W71 restricted branches and W80 action are unchanged.',
      output_files_written=[])
    print(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2))
    return 0 if verified else 1

if __name__=='__main__':
    raise SystemExit(main())
