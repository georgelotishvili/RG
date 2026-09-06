#!/usr/bin/env python3
"""W3-80 new neutral-condensate candidate; finite JSON stdout, no file writes."""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as sp

SOURCE = Path(__file__).resolve()
ROOT = SOURCE.parents[4]
CONTRACT = SOURCE.with_name('w3_80_neutral_resonant_condensate_contract.md')
CONTRACT_SHA = '27e359b9980df14a287ca89cc38a895eb5015a732154d7a055fd7666b418d841'
PINS = {
 'CODES.md':'27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41',
 'RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/'
 'w3_54_relational_coframe_tegr_phase_source_closure_contract.md':
 '6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879',
 'RefG/work 3/Cosmology_and_LSS/CMB_Closure/w3_62_cmb_einstein_source_linear_closure_preregistration.md':
 'b4068791b63e9a072a897e9aa85eae96c588b0d33533effb9664ffbd667ae810',
 'RefG/work 3/Strong_Field/W3-79_Collective_Current_Backreaction/'
 'w3_79_collective_current_backreaction_contract.md':
 '7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa',
 'RefG/work 3/Strong_Field/W3-79_Collective_Current_Backreaction/'
 'w3_79_collective_current_backreaction.py':
 '4efe86c593db5ad9f5dfb7a1efe1aa0f4d5f2ea0af410d25ba1c7743534c5672',
}
FALSE_FLAGS = ('physical_foundation_nodes_identified','P_F_bridge_derived',
 'all_signal_speeds_slow','ordinary_to_collective_origin_derived',
 'exact_finite_density_CMB_dust','full_curved_gradient_control',
 'strong_field_collapse_solved','singularity_resolved','observational_pass',
 'active_theory_changed','intuitive_files_changed')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def audit(residuals, inequalities=None):
    expressions={key:sp.factor(sp.simplify(value)) for key,value in residuals.items()}
    checks={key:bool(value==0) for key,value in expressions.items()}
    signs={} if inequalities is None else {key:bool(value) for key,value in inequalities.items()}
    return dict(all_pass=all(checks.values()) and all(signs.values()), checks=checks,
                sign_checks=signs,residuals={key:sp.sstr(value) for key,value in expressions.items()})

def provenance():
    deps={name:dict(actual=sha(ROOT/name),expected=value) for name,value in PINS.items()}
    files=sorted(path.name for path in SOURCE.parent.iterdir())
    result=dict(dependencies=deps,source_sha256=sha(SOURCE),contract_sha256=sha(CONTRACT),
                expected_contract_sha256=CONTRACT_SHA,package_files=files,
                python=platform.python_version(),sympy=sp.__version__,numpy=np.__version__,
                scipy=scipy.__version__,bytecode_disabled=sys.dont_write_bytecode)
    result['all_pass']=(all(item['actual']==item['expected'] for item in deps.values())
        and result['contract_sha256']==CONTRACT_SHA and sys.dont_write_bytecode
        and files==sorted([SOURCE.name,CONTRACT.name]))
    return result

def action_checks():
    """Differentiate the full covariant matter integrand before its reduction.

    General local covariant gradients and all ten independent metric variations
    are retained. Tensoriality permits evaluating the variation in a Lorentz frame.
    """
    m,lam,R=sp.symbols('m lambda R',positive=True)
    eps=sp.symbols('epsilon',real=True)
    g=sp.diag(-1,1,1,1)
    a=sp.Matrix(sp.symbols('R_0:4',real=True))
    b=sp.Matrix(sp.symbols('theta_0:4',real=True))
    U=m*m*R*R/2+lam*R**4/4
    lag=-(a.T*g*a)[0]/2-R*R*(b.T*g*b)[0]/2-U
    current=-R*R*g*b
    stress_up=g*a*a.T*g+R*R*g*b*b.T*g+g*lag
    residuals={'amplitude_Euler_algebraic':sp.diff(lag,R)+R*(b.T*g*b)[0]+sp.diff(U,R)}
    for i in range(4):
        residuals[f'amplitude_Euler_gradient_{i}']=sp.diff(lag,a[i])+(g*a)[i]
        residuals[f'phase_Noether_current_{i}']=sp.diff(lag,b[i])-current[i]
    for i in range(4):
        for j in range(i,4):
            delta=sp.zeros(4); delta[i,j]=1; delta[j,i]=1
            metric=g+eps*delta
            inv=metric.inv(); volume=sp.sqrt(-metric.det())
            density=volume*(-(a.T*inv*a)[0]/2-R*R*(b.T*inv*b)[0]/2-U)
            factor=sp.Rational(1,2) if i==j else 1
            residuals[f'full_Hilbert_variation_{i}{j}']=sp.diff(density,eps).subs(eps,0)-factor*stress_up[i,j]
    amp_stress=g*a*a.T*g-g*(a.T*g*a)[0]/2
    reduced_stress=R*R*g*b*b.T*g+g*(-R*R*(b.T*g*b)[0]/2-U)
    for i in range(4):
        for j in range(i,4):
            residuals[f'discarded_amplitude_gradient_stress_{i}{j}']=stress_up[i,j]-reduced_stress[i,j]-amp_stress[i,j]
    # Derive the principal symbol from the two-real-field kinetic Hessian.
    p=sp.Matrix(sp.symbols('k_0:4',real=True))
    phi=sp.symbols('phi1 phi2',real=True)
    grad=(sp.Matrix(sp.symbols('phi1_0:4',real=True)),
          sp.Matrix(sp.symbols('phi2_0:4',real=True)))
    norm=phi[0]**2+phi[1]**2
    cartlag=-sum((q.T*g*q)[0] for q in grad)/2-m*m*norm/2-lam*norm**2/4
    principal=sp.Matrix(2,2,lambda i,j:sum(sp.diff(cartlag,grad[i][a],grad[j][b])*p[a]*p[b]
                                         for a in range(4) for b in range(4)))
    residuals['Cartesian_metric_null_principal']=principal.det()-(p.T*g*p)[0]**2
    result=audit(residuals)
    result['equations']={'amplitude':'Box R-R (partial theta)^2-m^2 R-lambda R^3=0',
                         'phase':'nabla_a(-R^2 partial^a theta)=0'}
    result['amplitude_gradient_stress']='partial_a R partial_b R-g_ab (partial R)^2/2'
    return result

def symbolic_checks():
    m,lam,x,n,k=sp.symbols('m lambda x n k',positive=True)
    mu=sp.sqrt(m*m+lam*x); h=2*lam*x; B=2*m*m+3*lam*x
    rho=m*m*x+sp.Rational(3,4)*lam*x*x; P=lam*x*x/4; charge=mu*x
    e=n*n/(2*x)+m*m*x/2+lam*x*x/4
    cs=lam*x/B
    X,Q,V=sp.symbols('X Q V',positive=True)
    Leff=(X-m*m)**2/(4*lam)
    res={'fixed_charge_stationarity':sp.diff(e,x).subs(n,charge),
         'fixed_charge_energy':e.subs(n,charge)-rho,
         'fixed_charge_hessian':sp.diff(e,x,2)-n*n/x**3-lam/2,
         'first_law':sp.diff(rho,x)/sp.diff(charge,x)-mu,
         'enthalpy':rho+P-mu*charge,
         'positive_density_derivative':sp.diff(charge,x)-B/(2*mu),
         'thermodynamic_sound':sp.diff(P,x)/sp.diff(rho,x)-cs,
         'volume_work_pressure':(-sp.diff(V*e.subs(n,Q/V),V)).subs(Q/V,charge)-P,
         'amplitude_elimination':(X*x/2-m*m*x/2-lam*x*x/4).subs(x,(X-m*m)/lam)-Leff,
         'effective_current_matching':(2*sp.diff(Leff,X)*sp.sqrt(X)).subs(X,mu*mu)-charge,
         'effective_energy_matching':(2*X*sp.diff(Leff,X)-Leff).subs(X,mu*mu)-rho}
    # The effective Hilbert tensor's coefficient of u_a u_b and of g_ab.
    res['effective_Hilbert_enthalpy']= (2*X*sp.diff(Leff,X)).subs(X,mu*mu)-mu*charge
    res['effective_Hilbert_pressure']=Leff.subs(X,mu*mu)-P
    Kt=(3*mu*mu-m*m)/lam; Ks=(mu*mu-m*m)/lam
    eps,td,pg=sp.symbols('epsilon pi_dot grad_pi',real=True)
    invariant=(mu+eps*td)**2-eps**2*pg**2
    eff2=sp.diff(Leff.subs(X,invariant),eps,2).subs(eps,0)/2
    res['effective_quadratic_action']=eff2-(Kt*td*td-Ks*pg*pg)/2
    res['effective_sound_matching']=Ks/Kt-cs
    # Actual full-action epsilon expansion, before the low-gradient elimination.
    s,sd,sg,pd,pg=sp.symbols('s s_dot grad_s pi_dot grad_pi',real=True)
    radius=sp.sqrt(x)+eps*s
    full=(eps**2*(sd*sd-sg*sg)/2+radius**2*((mu+eps*pd/sp.sqrt(x))**2
          -eps**2*pg*pg/x)/2-m*m*radius**2/2-lam*radius**4/4)
    L2=sp.diff(full,eps,2).subs(eps,0)/2
    target=(sd*sd-sg*sg+pd*pd-pg*pg-h*s*s)/2+2*mu*s*pd
    res['full_quadratic_action']=L2-target
    res['linear_term_is_phase_boundary']=sp.diff(full,eps).subs(eps,0)-mu*sp.sqrt(x)*pd
    sdd,pdd,slap,plap=sp.symbols('s_dd pi_dd Lap_s Lap_pi',real=True)
    eq_s=sp.diff(sp.diff(L2,sd),sd)*sdd-sp.diff(L2,s)-slap
    eq_p=sp.diff(sp.diff(L2,pd),pd)*pdd+sp.diff(sp.diff(L2,pd),s)*sd-plap
    res['amplitude_linear_Euler']=eq_s-(sdd-slap+h*s-2*mu*pd)
    res['phase_linear_Euler']=eq_p-(pdd-plap+2*mu*sd)
    omega=sp.symbols('omega',real=True)
    pencil=sp.Matrix([[k*k+h-omega**2,2*sp.I*mu*omega],[-2*sp.I*mu*omega,k*k-omega**2]])
    determinant=(k*k+h-omega**2)*(k*k-omega**2)-4*mu*mu*omega**2
    res['frequency_pencil']=pencil.det()-determinant
    evolution=sp.Matrix([[0,0,1,0],[0,0,0,1],[-k*k-h,0,0,2*mu],[0,-k*k,-2*mu,0]])
    res['real_time_matrix_spectrum']=(evolution+sp.I*omega*sp.eye(4)).det()-determinant
    S=sp.sqrt(B*B+4*mu*mu*k*k)
    lo=k*k*(k*k+h)/(k*k+B+S); hi=k*k+B+S
    res['root_product']=lo*hi-k*k*(k*k+h)
    res['root_sum']=lo+hi-2*(k*k+B)
    res['Goldstone_zero']=lo.subs(k,0)
    res['gapped_zero_wave_number']=hi.subs(k,0)-2*B
    res['infrared_slope']=sp.limit(lo/(k*k),k,0)-cs
    remainder=8*mu**4*k**4/(B*(S+B)**2)
    res['exact_acoustic_remainder']=lo-cs*k*k-remainder
    res['relative_error_bound_coefficient']=remainder/(cs*k*k)-(k*k/h)*16*mu**4/(S+B)**2
    res['bound_denominator_certificate']=2*B-4*mu*mu-2*lam*x
    res['fixed_k_vacuum_limit']=lo.subs(x,0)-(sp.sqrt(m*m+k*k)-m)**2
    eta=sp.symbols('eta',positive=True)
    ratio=(1+3*eta/4)/sp.sqrt(1+eta)
    res['cold_energy_ratio']=(rho/(m*charge)).subs(x,eta*m*m/lam)-ratio
    # Squared comparisons are equivalent because both sides are positive.
    res['cold_lower_bound_certificate']=(1+3*eta/4)**2-(1+eta)-eta/2-9*eta**2/16
    res['cold_upper_bound_certificate']=(1+eta/4)**2*(1+eta)-(1+3*eta/4)**2-eta**3/16
    res['cold_limit']=sp.limit(ratio,eta,0)-1
    res['cold_pressure_ratio']=(P/rho).subs(x,eta*m*m/lam)-eta/(4+3*eta)
    res['cold_sound_ratio']=cs.subs(x,eta*m*m/lam)-eta/(2+3*eta)
    res['carrier_vacuum_limit']=mu.subs(x,0)-m
    res['pressure_monotonicity']=sp.diff(P,x)-lam*x/2
    res['sound_monotonicity']=sp.diff(cs,x)-2*lam*m*m/B**2
    lapse,C=sp.symbols('N C',positive=True)
    static_pressure=((C/lapse)**2-m*m)**2/(4*lam)
    res['static_pressure_lapse_derivative']=sp.diff(static_pressure,lapse).subs(C,mu*lapse)+mu*mu*x/lapse
    d=charge**(-sp.Rational(1,3))
    res['charge_length_monotonicity']=sp.diff(d,x)+sp.diff(charge,x)/(3*charge**sp.Rational(4,3))
    signs={'energy_positive':bool(e.is_positive),'hessian_positive':bool(sp.diff(e,x,2).is_positive),
           'e_left_endpoint':sp.limit(e,x,0)==sp.oo,'e_right_endpoint':sp.limit(e,x,sp.oo)==sp.oo,
           'eprime_left_endpoint':sp.limit(sp.diff(e,x),x,0)==-sp.oo,
           'eprime_right_endpoint':sp.limit(sp.diff(e,x),x,sp.oo)==sp.oo,
           'positive_temporal_coefficient':bool(sp.simplify(Kt).is_positive),
           'positive_spatial_coefficient':bool(sp.simplify(Ks).is_positive),
           'sound_positive':bool(cs.is_positive),'sound_below_one_third':bool(sp.factor(sp.Rational(1,3)-cs).is_positive),
           'lower_root_positive_k':bool(lo.is_positive),'upper_root_positive_k':bool(hi.is_positive)}
    result=audit(res,signs)
    result['bound_proof']='S>=B, 2B=4mu^2+2lambda*x>4mu^2; hence 16mu^4/(S+B)^2<=1.'
    result['cold_bound_proof']='Positive squared comparison differences eta/2+9eta^2/16 and eta^3/16.'
    result['minimum_proof']='e strictly convex, diverges at both endpoints; eprime runs from -infinity to +infinity.'
    result['EOS']={'parameter':'x>0','n':'x sqrt(m^2+lambda*x)','rho':'m^2*x+3lambda*x^2/4',
                   'P':'lambda*x^2/4','sound_squared':'lambda*x/(2m^2+3lambda*x)'}
    return result

def exact_modes(eta,k):
    x=float(eta); mu=math.sqrt(1+x); h=2*x; B=2+3*x
    S=math.sqrt(B*B+4*mu*mu*k*k)
    low2=k*k*(k*k+h)/(k*k+B+S); high2=k*k+B+S
    return mu,h,B,math.sqrt(low2),math.sqrt(high2),x/B

def hydro_valid(eta,k,shortcut=False):
    _,h,B,_,_,_=exact_modes(eta,k)
    return bool(k*k/(2*B if shortcut else h)<=0.01)

def numerical_checks():
    states=[]; cases=[]
    for eta in (1e-6,1e-3,1.0,100.0):
        x=eta; n=x*math.sqrt(1+x); rho=x+0.75*x*x; pressure=x*x/4
        root=brentq(lambda z:-n*n/(2*z*z)+0.5+z/2,1e-12,1e3,xtol=1e-18,
                    rtol=4*np.finfo(float).eps)
        root_error=abs(root-x)/x; cs=x/(2+3*x); differences=[]
        for epsilon in (1e-3,5e-4):
            xp,xm=x*(1+epsilon),x*(1-epsilon)
            derivative=(xp*xp/4-xm*xm/4)/((xp+0.75*xp*xp)-(xm+0.75*xm*xm))
            differences.append(dict(epsilon=epsilon,derivative=derivative,relative_error=abs(derivative-cs)/cs))
        convergence=differences[1]['relative_error']<=differences[0]['relative_error']+1e-10
        state=dict(eta=eta,x=x,n=n,rho=rho,pressure=pressure,d=n**(-1/3),carrier_mu=math.sqrt(1+x),
                   sound_squared=cs,root_x=root,root_relative_error=root_error,derivatives=differences,
                   derivative_convergence=convergence)
        state['pass']=root_error<1e-8 and convergence and all(t['relative_error']<2e-6 for t in differences)
        states.append(state)
        for fraction in (0.03,0.1):
            k=fraction*math.sqrt(2*x); mu,h,B,low,high,cs=exact_modes(eta,k)
            matrix=np.array([[0,0,1,0],[0,0,0,1],[-k*k-h,0,0,2*mu],[0,-k*k,-2*mu,0]],dtype=float)
            eigen=np.linalg.eigvals(matrix); positive=sorted(float(v.imag) for v in eigen if v.imag>0)
            errors=[abs(a-b)/b for a,b in zip(positive,(low,high))] if len(positive)==2 else [1.0,1.0]
            realmax=float(np.max(np.abs(eigen.real))); relative=low*low/(cs*k*k)-1
            bound=k*k/h
            row=dict(eta=eta,k=k,k_over_sqrt_h=fraction,omega_lower=low,omega_upper=high,
                     real_matrix_frequencies=positive,frequency_relative_errors=errors,
                     max_real_eigenvalue_part=realmax,acoustic_relative_error=relative,error_bound=bound)
            row['pass']=len(positive)==2 and max(errors)<1e-6 and realmax<1e-10*max(1,high) and -1e-10<=relative<=bound+1e-10
            cases.append(row)
    eta,k=1e-8,0.01
    mu,h,B,low,high,cs=exact_modes(eta,k)
    witness=dict(eta=eta,k=k,gap_ratio=k*k/(2*B),healing_ratio=k*k/h,
                 acoustic_relative_error=low*low/(cs*k*k)-1,
                 gap_shortcut_accepts=hydro_valid(eta,k,True),production_accepts=hydro_valid(eta,k))
    witness['pass']=witness['gap_shortcut_accepts'] and not witness['production_accepts'] and witness['acoustic_relative_error']>0.01
    result=dict(units={'m_C':1,'lambda_C':1},states=states,modes=cases,invalid_domain_witness=witness)
    result['all_pass']=len(states)==4 and len(cases)==8 and all(r['pass'] for r in states+cases) and witness['pass']
    return result

def production_validator(config):
    m,lam,x,k,omega=sp.symbols('m lambda x k omega',positive=True)
    mu=sp.sqrt(m*m+lam*x); h=2*lam*x; B=2*m*m+3*lam*x
    rho=m*m*x+3*lam*x*x/4; P=lam*x*x/4; n=mu*x
    exact=(k*k+h-omega*omega)*(k*k-omega*omega)-4*mu*mu*omega*omega
    candidate=(k*k+h-omega*omega)*(k*k-omega*omega)-4*config['mixing']**2*mu*mu*omega*omega
    res={'Noether_density':config['density']*n-n,
         'one_collective_Hilbert_energy':config['stress']*rho-rho,
         'one_collective_Hilbert_pressure':config['stress']*P-P,
         'action_quadratic_dispersion':candidate-exact,
         'action_acoustic_slope':(sp.S.One if config['light_sound'] else lam*x/B)-lam*x/B,
         'fixed_charge_volume_pressure':(sp.S.Zero if config['dust'] else P)-P}
    radius=sp.symbols('R_candidate',positive=True)
    candidate_potential=m*m*radius**2/2+config['quartic']*lam*radius**4/4
    asymptotic_coefficient=sp.limit(candidate_potential/radius**4,radius,sp.oo)
    checks={'quartic_energy_bounded':bool(asymptotic_coefficient>0),
            'sound_domain_counterexample_rejected':not hydro_valid(1e-8,0.01,config['gap_shortcut'])}
    return audit(res,checks)

def negative_controls():
    config=dict(quartic=1,density=1,stress=1,mixing=1,light_sound=False,dust=False,gap_shortcut=False)
    production=production_validator(config); controls={}
    for name,key,value in (('negative_quartic','quartic',-1),('halved_Noether_density','density',sp.Rational(1,2)),
          ('doubled_collective_stress','stress',2),('removed_mixing','mixing',0),
          ('sound_equals_light','light_sound',True),('finite_density_exact_dust','dust',True),
          ('gap_only_sound_condition','gap_shortcut',True)):
        candidate=dict(config); candidate[key]=value; test=production_validator(candidate)
        controls[name]=dict(detected=not test['all_pass'],failed_identities=[k for k,v in test['checks'].items() if not v],
                            failed_validity=[k for k,v in test['sign_checks'].items() if not v],
                            residuals={k:v for k,v in test['residuals'].items() if v!='0'})
    return dict(production=production,controls=controls,all_pass=production['all_pass'] and all(v['detected'] for v in controls.values()))

def main():
    print('W80: pins; full action and all metric variations',file=sys.stderr,flush=True)
    prov=provenance()
    if not prov['all_pass']:
        print(json.dumps(dict(status='FAIL_PROVENANCE',provenance=prov),allow_nan=False)); return 1
    action=action_checks()
    print('W80: fixed-charge EOS; full quadratic spectrum; sound bound',file=sys.stderr,flush=True)
    symbolic=symbolic_checks()
    print('W80: frozen four-density/eight-mode numerical checks and controls',file=sys.stderr,flush=True)
    numerical=numerical_checks(); controls=negative_controls()
    flags=dict(provenance=prov['all_pass'],candidate_action_and_source=action['all_pass'],
               candidate_EOS_spectrum_IR_bound=symbolic['all_pass'],numerical=numerical['all_pass'],mutations=controls['all_pass'])
    passed=all(flags.values()); flags.update({key:False for key in FALSE_FLAGS})
    result=dict(claim_id='W3_80_NEUTRAL_RESONANT_CONDENSATE_CONSTITUTIVE_CANDIDATE',model_version='W3-80-v1.0',
      status='PASS_CLASSICAL_CONSTITUTIVE_CANDIDATE_LOCAL_LINEAR_TEST' if passed else 'FAIL_W80',artifact_valid=passed,
      provenance=prov,action=action,symbolic=symbolic,numerical=numerical,negative_controls=controls,closure_flags=flags,
      source_ledger={'candidate_replaces_effective_T_C':1,'extra_third_stress':0,'active_theory_modified':False},
      interpretation={'rarefaction':'P_C and infrared c_s decrease with charge density; healing window narrows.',
       'carrier':'mu approaches m_C; fixed-k lower mode approaches sqrt(m_C^2+k^2)-m_C.',
       'static_sign':'P_C increases toward lower stationary lapse; P_F mapping remains separate.',
       'gradient_scope':'Amplitude-gradient stress is retained in full action; eliminated only conditionally.',
       'strong_field':'Candidate interface only; no black-hole solution or active W79 replacement.'},output_files_written=[])
    print(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2))
    return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
