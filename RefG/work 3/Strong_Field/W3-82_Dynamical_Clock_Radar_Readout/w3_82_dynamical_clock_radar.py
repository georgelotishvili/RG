#!/usr/bin/env python3
"""Frozen W3-82 radial observer/ray interface; finite JSON stdout, no writes."""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import hashlib
import importlib.util
import json
import math
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as sp

SOURCE=Path(__file__).resolve(); ROOT=SOURCE.parents[4]
CONTRACT=SOURCE.with_name('w3_82_dynamical_clock_radar_contract.md')
CONTRACT_SHA='3c389016254c2c554bec346e6012857c41daaa01a10e2fbba876be1d971d63d8'
SF='RefG/work 3/Strong_Field/'
W79=SF+'W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction.py'
PINS={
 'CODES.md':'27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41',
 'RefG/work 3/Cosmology_and_LSS/Photon_Atomic_Observable_Bridge/w3_43_photon_atomic_observable_bridge_preregistration.md':
 '20793b696e7fcd64a0a4f9a575b4091eeb2faf651973448b87b2c025b2d258da',
 SF+'W3-71_Horizon_Material_Scale_Separation/w3_71_horizon_material_scale_separation_preregistration.md':
 '1d3f74489f6cc52061253b6e1ea3d7f96e5d423f8b2afb88e79a44a38ae916c3',
 SF+'W3-73_Coupled_Horizon_Regular_Einstein_Complex_Scalar/w3_73_coupled_horizon_regular_einstein_complex_scalar.py':
 '47f2c97b64544f124cc2a5cb8d04825188664493cb5d770b6c3faf4ce2d5d7ca',
 SF+'W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction_contract.md':
 '7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa',
 W79:'4efe86c593db5ad9f5dfb7a1efe1aa0f4d5f2ea0af410d25ba1c7743534c5672',
 SF+'W3-81_Dynamical_Scale_Integrability/w3_81_dynamical_scale_integrability_contract.md':
 '43b5bc7586afc323dbb64129bcb74f154b990c54dd82e33603a394f59c1aff88',
 SF+'W3-81_Dynamical_Scale_Integrability/w3_81_dynamical_scale_integrability.py':
 'dca645b2037141a55dd163fc570fdd69b7797220bea098e1eff99a9574d5ac12'}
FALSE_FLAGS=('universal_scale_potential_derived','foundation_pressure_law_derived',
 'microscopic_clock_derived','resolved_optical_image_derived','full_W80_collapse_solved',
 'singularity_resolved','observational_pass','active_theory_changed','intuitive_files_changed')

def clean(x):
    return sp.factor(sp.simplify(x))

def audit(values):
    residuals={key:clean(value) for key,value in values.items()}
    return dict(all_pass=all(value==0 for value in residuals.values()),
       checks={key:bool(value==0) for key,value in residuals.items()},
       residuals={key:sp.sstr(value) for key,value in residuals.items()})

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def provenance():
    pins={p:dict(expected=h,actual=sha(ROOT/p)) for p,h in PINS.items()}
    files=sorted(p.name for p in SOURCE.parent.iterdir())
    good=all(row['actual']==row['expected'] for row in pins.values())
    return dict(all_pass=good and sha(CONTRACT)==CONTRACT_SHA and sys.dont_write_bytecode
                and files==sorted([SOURCE.name,CONTRACT.name]),dependencies=pins,
       contract_sha256=sha(CONTRACT),expected_contract_sha256=CONTRACT_SHA,
       source_sha256=sha(SOURCE),package_files=files,bytecode_disabled=sys.dont_write_bytecode,
       versions=dict(python=platform.python_version(),sympy=sp.__version__,scipy=scipy.__version__,numpy=np.__version__))

def christoffels(metric,coords):
    inv=metric.inv()
    return [[[clean(sum(inv[i,l]*(sp.diff(metric[l,k],coords[j])+sp.diff(metric[l,j],coords[k])
                    -sp.diff(metric[j,k],coords[l]))/2 for l in range(2)))
               for k in range(2)] for j in range(2)] for i in range(2)]

def exact_interface():
    t,r=sp.symbols('T r',real=True); E=sp.symbols('E',positive=True)
    sig=sp.Function('sigma',positive=True)(t,r); z=sp.Function('zeta')(t,r)
    metric=sp.Matrix([[sig**2*(z*z-1),sig*z],[sig*z,1]])
    inv=metric.inv(); gamma=christoffels(metric,(t,r))
    kt,kr=sp.symbols('k_T k_r',real=True); p=sp.Matrix([kt,kr])
    H4=(p.T*inv*p)[0]/2
    null={}; frequency={}; endpoints={}; rulers={}; limits={}; contexts={}
    for s in (-1,1):
        f=sig*(s-z); HT=f*kr
        roots=sp.solve(H4,kt)
        # Branch selection is by the declared future coframe vector, not k_T sign.
        candidate=-sig*E*(1-s*z)
        null[f'Hamiltonian_root_{s}']=sp.prod(root.subs(kr,s*E)-candidate for root in roots)
        null[f'null_constraint_{s}']=H4.subs({kt:candidate,kr:s*E})
        K=inv*sp.Matrix([candidate,s*E])
        null[f'future_time_component_{s}']=K[0]-E/sig
        null[f'radial_component_{s}']=K[1]-E*(s-z)
        null[f'Hamilton_reduced_velocity_{s}']=sp.diff(HT,kr)-f
        Edot=-sp.diff(HT,r).subs(kr,s*E)/s
        frequency[f'Hamilton_frequency_{s}']=Edot+E*sp.diff(f,r)
        for a in range(2):
            derivative=K[0]*(sp.diff(K[a],t)+f*sp.diff(K[a],r)+Edot*sp.diff(K[a],E))
            frequency[f'affine_geodesic_{s}_{a}']=derivative+sum(gamma[a][b][c]*K[b]*K[c] for b in range(2) for c in range(2))
        energy=HT.subs(kr,s*E)
        energy_dot=sp.diff(energy,t)+f*sp.diff(energy,r)+Edot*sp.diff(energy,E)
        frequency[f'nonstatic_coordinate_energy_{s}']=energy_dot-sp.diff(f,t)*s*E
        J=sp.symbols('J',positive=True)
        frequency[f'frequency_flow_Jacobian_invariant_{s}']=Edot*J+E*sp.diff(f,r)*J
        v=sp.symbols('v',real=True); gam=1/sp.sqrt(1-v*v)
        u=sp.Matrix([gam/sig,gam*(v-z)]); projection=-(u.T*metric*K)[0]
        endpoints[f'observer_normalization_{s}']=(u.T*metric*u)[0]+1
        endpoints[f'proper_clock_rate_{s}']=1/u[0]-sig/gam
        endpoints[f'observer_coordinate_velocity_{s}']=u[1]/u[0]-sig*(v-z)
        endpoints[f'observer_frequency_projection_{s}']=projection-gam*(1-s*v)*E
        se,so=sp.symbols('sigma_e sigma_o',positive=True)
        ze,zo,ve,vo=sp.symbols('zeta_e zeta_o v_e v_o',real=True)
        ge,go=1/sp.sqrt(1-ve*ve),1/sp.sqrt(1-vo*vo)
        fe,fo=se*(s-ze),so*(s-zo); we,wo=se*(ve-ze),so*(vo-zo)
        de,arrival=sp.symbols('initial_endpoint_change arrival_time_derivative')
        # Differentiate the initial condition along the moving launch event:
        initial_variation=sp.solve(de+fe-we,de)[0]
        To=sp.solve(J*initial_variation+(fo-wo)*arrival,arrival)[0]
        pulse=(so/go)/(se/ge)*To
        factor_e=clean(projection.subs({v:ve,E:1,sig:se,z:ze}))
        factor_o=clean(projection.subs({v:vo,E:1,sig:so,z:zo}))
        ratio=factor_o/(J*factor_e)
        endpoints[f'launch_time_boundary_{s}']=initial_variation-(we-fe)
        endpoints[f'moving_arrival_boundary_{s}']=To-J*(we-fe)/(wo-fo)
        endpoints[f'proper_pulse_frequency_reciprocity_{s}']=pulse*ratio-1
        endpoints[f'transverse_receiver_{s}']=wo-fo-so*(vo-s)
        dl,dT,dr=sp.symbols('dell dT dr',real=True)
        rest_time=gam*(sig*dT-v*(dr+sig*z*dT))
        rest_length=gam*(dr+sig*z*dT-v*sig*dT)
        displacement=sp.solve((rest_time,rest_length-dl),(dT,dr),dict=True)[0]
        rulers[f'rest_simultaneous_time_{s}']=displacement[dT]-gam*v*dl/sig
        rulers[f'rest_simultaneous_radial_{s}']=displacement[dr]-gam*(1-z*v)*dl
        delta=sp.Matrix([displacement[dT],displacement[dr]])
        rulers[f'proper_length_metric_{s}']=(delta.T*metric*delta)[0]-dl*dl
        after=sp.symbols('E_after',real=True)
        outgoing=projection.subs(E,after).subs(v,-v)
        reflected=sp.solve(projection-outgoing,after)[0]/E
        rulers[f'elastic_reflection_{s}']=reflected-(1-s*v)/(1+s*v)
        limits[f'Minkowski_ray_{s}']=f.subs({sig:1,z:0})-s
        limits[f'Minkowski_frequency_{s}']=Edot.subs({sig:1,z:0}).doit()
        limits[f'Minkowski_Doppler_{s}']=ratio-(go*(1-s*vo))/(J*ge*(1-s*ve))
        static_energy=energy_dot.subs({sp.diff(sig,t):0,sp.diff(z,t):0})
        limits[f'stationary_coordinate_energy_{s}']=static_energy
        N=sig*sp.sqrt(1-z*z)
        limits[f'normalized_Killing_frequency_{s}']=projection.subs(v,z)-energy/N
        Ne,No=se*sp.sqrt(1-ze*ze),so*sp.sqrt(1-zo*zo)
        static_ratio=(go*(1-s*vo)/(ge*(1-s*ve))*se*(1-s*ze)/(so*(1-s*zo))).subs({ve:ze,vo:zo})
        limits[f'static_Killing_endpoint_ratio_{s}']=static_ratio-Ne/No
        limits[f'marginal_ray_finite_{s}']=f.subs(z,1)-sig*(s-1)
        # Take the point value z=1 after differentiation; do not erase z_r.
        zR,sR=sp.symbols('zeta_r sigma_r',real=True)
        marginal=Edot.subs({sp.diff(z,r):zR,sp.diff(sig,r):sR},simultaneous=True).subs(z,1)
        limits[f'marginal_energy_finite_{s}']=marginal-E*(sig*zR-(s-1)*sR)
        contexts[s]=dict(E=E,Edot=Edot,fr=sp.diff(f,r),projection=projection,v=v,
          factor_o=factor_o,ratio=ratio,J=J,fe=fe,fo=fo,we=we,wo=wo,se=se,so=so,ge=ge,go=go,ve=ve,vo=vo)
    # Independent comoving affine geodesic, also used to derive the LTB route.
    a=sp.symbols('a',real=True); B=sp.Function('B',positive=True)(t,a)
    gm=sp.diag(-1,B*B); cg=christoffels(gm,(t,a))
    comoving={}
    for s in (-1,1):
        K=sp.Matrix([E,s*E/B]); ad=s/B; ed=-E*sp.diff(B,t)/B
        for i in range(2):
            comoving[f'comoving_affine_geodesic_{s}_{i}']=E*(sp.diff(K[i],t)+ad*sp.diff(K[i],a)+ed*sp.diff(K[i],E))+sum(cg[i][j][k]*K[j]*K[k] for j in range(2) for k in range(2))
        comoving[f'LTB_time_against_shell_{s}']=1/ad-s*B
        comoving[f'LTB_frequency_against_shell_{s}']=(ed/E)/ad+s*sp.diff(B,t)
        A=sp.Function('A',positive=True)(t)
        limits[f'FLRW_frequency_invariant_{s}']=(E*sp.diff(A,t)+A*ed.subs(B,A).doit())
    ae,ao=sp.symbols('A_e A_o',positive=True); dTo=sp.symbols('dT_o')
    limits['FLRW_adjacent_fronts']=sp.solve(1/ae-dTo/ao,dTo)[0]-ao/ae
    limits['FLRW_frequency_pulse_reciprocity']=(ae/ao)*(ao/ae)-1
    L,send=sp.symbols('L T_send',positive=True); mirror=send+L; returned=mirror+L
    rulers['Minkowski_outgoing_event']=mirror-send-L
    rulers['Minkowski_return_event']=returned-mirror-L
    rulers['Minkowski_radar_distance']=(returned-send)/2-L
    rulers['Minkowski_radar_time']=(returned+send)/2-mirror
    groups={key:audit(value) for key,value in dict(null=null,frequency=frequency,endpoints=endpoints,rulers=rulers,limits=limits,comoving=comoving).items()}
    return groups,contexts

def controls(contexts):
    def validator(config):
        res={}
        for s,c in contexts.items():
            candidate_ed=config['energy_sign']*c['Edot']
            candidate_factor=c['go'] if config['drop_receiver'] else c['factor_o']
            candidate_launch=-c['fe'] if config['drop_emitter_motion'] else c['we']-c['fe']
            candidate_pulse=(c['so']/c['go'])/(c['se']/c['ge'])*c['J']*candidate_launch/(c['wo']-c['fo'])
            res[f'Hamiltonian_frequency_{s}']=candidate_ed-c['Edot']
            res[f'receiver_momentum_projection_{s}']=candidate_factor-c['factor_o']
            res[f'moving_proper_pulse_reciprocity_{s}']=candidate_pulse*c['ratio']-1
        L=sp.symbols('L',positive=True)
        res['stationary_mirror_radar']=config['radar_factor']*2*L-L
        return audit(res)
    base=dict(energy_sign=1,drop_receiver=False,drop_emitter_motion=False,radar_factor=sp.Rational(1,2))
    production=validator(base); mutants={}
    for name,key,value in [('reversed_energy_gradient','energy_sign',-1),('omitted_receiver_Doppler','drop_receiver',True),('omitted_emitter_motion','drop_emitter_motion',True),('full_roundtrip_as_distance','radar_factor',1)]:
        config=dict(base); config[key]=value; test=validator(config)
        mutants[name]=dict(detected=not test['all_pass'],failed_identities=[k for k,v in test['checks'].items() if not v],residuals={k:v for k,v in test['residuals'].items() if v!='0'})
    return dict(all_pass=production['all_pass'] and all(row['detected'] for row in mutants.values()),production=production,mutations=mutants)

def source_regression():
    spec=importlib.util.spec_from_file_location('w82_w79_pure_regression',ROOT/W79)
    module=importlib.util.module_from_spec(spec); sys.modules[spec.name]=module; spec.loader.exec_module(module)
    w,geometry=module.load_geometry()
    return module.ltb_regression(w,geometry)  # Pure recomputation; no main or result reader.

def background_functions():
    t=sp.symbols('T',real=True); a=sp.symbols('a',positive=True)
    M=sp.Rational(1,2)+a/20
    X=a**sp.Rational(3,2)-sp.Rational(3,2)*sp.sqrt(2*M)*t
    R=X**sp.Rational(2,3); Ra=sp.diff(R,a); RTa=sp.diff(R,t,a)
    # On the frozen real shell branch X>0, the positive metric root is
    # sqrt(2M/R)=sqrt(2M)*X^(-1/3); no unrestricted complex-power rewrite.
    z=sp.sqrt(2*M)*X**(-sp.Rational(1,3)); rho=sp.diff(M,a)/(4*sp.pi*R*R*Ra)
    fn=sp.lambdify((t,a),(R,Ra,RTa,z,rho,X),'math')
    exact=audit({'positive_metric_root':z*z*R-2*M,
                 'shell_evolution':sp.diff(R,t)+z,'PG_comoving_frequency':sp.diff(z,a)+RTa})
    return fn,exact

AE=1.5; AM=1.55; TE=.02; TMAX=.2
SETTINGS={'coarse':dict(rtol=1e-9,atol=1e-11,max_step=1e-2),'fine':dict(rtol=1e-11,atol=1e-13,max_step=5e-3)}

def numerical():
    bg,bg_exact=background_functions()
    def invert(T,r):
        return brentq(lambda a:bg(T,a)[0]-r,1.25,1.75,xtol=2e-13,rtol=1e-13)
    def health(sol,chart):
        coordinates=np.unique(np.r_[sol.t,np.linspace(sol.t[0],sol.t[-1],21)])
        rows=[]
        for coordinate in coordinates:
            y=sol.sol(coordinate)
            if chart=='comoving':
                a=float(coordinate); T=float(y[0]); r=bg(T,a)[0]
            else:
                T=float(coordinate); r=float(y[0]); a=invert(T,r)
            R,Ra,RTa,z,rho,X=bg(T,a); recovered=invert(T,r); E=math.exp(float(y[1]))
            row=[T,a,R,Ra,rho,X,E,abs(recovered-a)]
            if not all(math.isfinite(v) for v in row) or not (0<=T<=TMAX and R>0 and Ra>0 and rho>0 and X>0 and E>0):
                raise RuntimeError('Ray left the frozen sampled health domain.')
            rows.append(row)
        data=np.asarray(rows)
        return dict(sample_count=len(rows),T_range=[float(data[:,0].min()),float(data[:,0].max())],
            min_R=float(data[:,2].min()),min_R_a=float(data[:,3].min()),min_rho=float(data[:,4].min()),min_E=float(data[:,6].min()),
            max_shell_inversion_error=float(data[:,7].max()),passed=bool(data[:,7].max()<2e-7))
    def roundtrip(chart,label,emission=TE):
        settings=SETTINGS[label]; times=[]; logs=[]; checks=[]; time=emission; logE=0.
        for s,start,target in ((1,AE,AM),(-1,AM,AE)):
            if chart=='comoving':
                def rhs(a,y):
                    R,Ra,RTa,z,rho,X=bg(float(y[0]),a)
                    return [s*Ra,-s*RTa]
                sol=solve_ivp(rhs,(start,target),[time,logE],method='DOP853',dense_output=True,**settings)
                if not sol.success: raise RuntimeError(sol.message)
                arrival=float(sol.y[0,-1]); lastlog=float(sol.y[1,-1])
            else:
                def rhs(T,y):
                    a=invert(T,float(y[0])); R,Ra,RTa,z,rho,X=bg(T,a)
                    return [s-z,-RTa/Ra]
                def endpoint(T,y): return float(y[0])-bg(T,target)[0]
                endpoint.terminal=True; endpoint.direction=s
                sol=solve_ivp(rhs,(time,TMAX),[bg(time,start)[0],logE],events=endpoint,method='DOP853',dense_output=True,**settings)
                if not sol.success or len(sol.t_events[0])!=1: raise RuntimeError('Frozen PG return/arrival event failed: '+sol.message)
                arrival=float(sol.t_events[0][0]); lastlog=float(sol.y_events[0][0,1])
            checks.append(health(sol,chart)); times.append(arrival); logs.append(lastlog)
            time=arrival; logE=lastlog  # v_m=0: exact local elastic reflection.
        out=math.exp(logs[0]); total=math.exp(logs[1])
        return dict(chart=chart,tolerance=label,send=emission,reflection_time=times[0],return_time=times[1],
          outward_frequency_ratio=out,inward_frequency_ratio=total/out,total_frequency_ratio=total,
          radar_distance=(times[1]-emission)/2,radar_time=(times[1]+emission)/2,
          reflection_local_frequency_jump=0.,health=checks,
          passed=all(row['passed'] for row in checks) and emission<times[0]<times[1]<=TMAX and total>0)
    runs={(chart,label):roundtrip(chart,label) for chart in ('comoving','PG') for label in SETTINGS}
    metrics=('reflection_time','return_time','outward_frequency_ratio','inward_frequency_ratio','total_frequency_ratio','radar_distance')
    relative=lambda x,y:abs(x-y)/max(abs(x),abs(y),1e-12)
    comparisons=[]
    pairs=[(('comoving',label),('PG',label)) for label in SETTINGS]+[((chart,'coarse'),(chart,'fine')) for chart in ('comoving','PG')]
    for left,right in pairs:
        errors={key:relative(runs[left][key],runs[right][key]) for key in metrics}
        comparisons.append(dict(left=list(left),right=list(right),relative_errors=errors,passed=max(errors.values())<2e-7))
    base=runs[('comoving','fine')]; pulses=[]
    for epsilon in (1e-4,5e-5):
        minus=roundtrip('comoving','fine',TE-epsilon); plus=roundtrip('comoving','fine',TE+epsilon)
        derivatives={key:(plus[key]-minus[key])/(2*epsilon) for key in ('reflection_time','return_time')}
        expected={'reflection_time':1/base['outward_frequency_ratio'],'return_time':1/base['total_frequency_ratio']}
        errors={key:relative(derivatives[key],expected[key]) for key in derivatives}
        pulses.append(dict(epsilon=epsilon,derivatives=derivatives,reciprocal_frequency_targets=expected,relative_errors=errors,
                          independently_retraced_arrivals={'minus':[minus['reflection_time'],minus['return_time']],'plus':[plus['reflection_time'],plus['return_time']]},
                          health_passed=minus['passed'] and plus['passed'],passed=minus['passed'] and plus['passed'] and max(errors.values())<2e-6))
    convergence={key:pulses[1]['relative_errors'][key]<=.5*pulses[0]['relative_errors'][key]+1e-8 for key in ('reflection_time','return_time')}
    return dict(exact_background=bg_exact,runs=list(runs.values()),comparisons=comparisons,neighboring_pulses=pulses,
       pulse_offset_convergence=convergence,two_chart_passed=all(row['passed'] for row in runs.values()) and all(row['passed'] for row in comparisons),
       pulse_passed=all(row['passed'] for row in pulses) and all(convergence.values()),
       health_scope='Accepted solver nodes plus 21 dense points per leg; sampled evidence, not interval certification.')

def main():
    prov=provenance()
    if not prov['all_pass']:
        print(json.dumps(dict(status='FAIL_PROVENANCE',provenance=prov),allow_nan=False)); return 1
    print('W82: exact Hamiltonian, observers, ruler and independent geometry',file=sys.stderr,flush=True)
    groups,contexts=exact_interface(); mutation=controls(contexts); source=source_regression()
    print('W82: frozen two-chart LTB rays and independent neighboring pulses',file=sys.stderr,flush=True)
    nums=numerical()
    flags=dict(null_transport_checked=groups['null']['all_pass'],frequency_transport_checked=groups['frequency']['all_pass'],
       endpoint_pulse_reciprocity_checked=groups['endpoints']['all_pass'],local_ruler_checked=groups['rulers']['all_pass'],
       reflection_and_radar_checked=groups['rulers']['all_pass'],known_limits_checked=groups['limits']['all_pass'],
       source_metric_regression_checked=source['all_pass'] and groups['comoving']['all_pass'] and nums['exact_background']['all_pass'],
       dynamic_two_chart_test_passed=nums['two_chart_passed'],independent_pulse_test_passed=nums['pulse_passed'],mutation_controls_passed=mutation['all_pass'])
    passed=prov['all_pass'] and all(flags.values()); flags.update({key:False for key in FALSE_FLAGS})
    result=dict(claim_id='W3_82_DYNAMICAL_RADIAL_CLOCK_AND_RADAR_READOUT',model_version='W3-82-v1.0',
       status='PASS_CONDITIONAL_RADIAL_OPERATIONAL_INTERFACE_AND_DYNAMIC_REGRESSION' if passed else 'FAIL_W82_OPERATIONAL_INTERFACE',
       artifact_valid=bool(passed),provenance=prov,closure_flags=flags,exact_groups=groups,source_metric_regression=source,
       negative_controls=mutation,numerical=nums,output_files_written=[],
       scope='Inherited minimal Maxwell, ideal proper clocks, one metric; protocol-dependent radial measurements. LTB is an exact dust regression, not a W80 collapse solution.')
    print(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2)); return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
