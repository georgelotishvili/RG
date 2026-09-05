#!/usr/bin/env python3
"""W3-77: no-write leading pair-response and scope diagnostics."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
sys.dont_write_bytecode = True
import numpy as np
import scipy
import sympy as sp
from scipy.integrate import simpson

HERE = Path(__file__).resolve().parent
WORK3 = HERE.parent.parent
CORE = WORK3 / 'Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core'
CONTRACT = HERE / 'w3_77_pair_phase_susceptibility_contract.md'
SOLVER = CORE / 'w3_58_one_oscillon_coframe_localized_core.py'
VERSION = 'W3-77-v1.0'
PINS = {
    CONTRACT: 'a69aa554ba09472176e04996a4f17d1057f18e4fb802a2533aebf47a432abb26',
    CORE / 'w3_58_one_oscillon_coframe_localized_core_preregistration.md': 'ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db',
    SOLVER: 'b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57',
    HERE / 'w3_76_same_field_resonant_exchange_contract.md': 'e10781a73470220065c664196efe0c361dbfb1c6c2404864e895d6ad2380bd02',
    HERE / 'w3_76_same_field_resonant_exchange.py': 'c3ad4b140c7b89a3e6d587b6b46480db1da0bb94b6b5307a32237df876285a6f',
    WORK3 / 'Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md': '6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879',
    HERE / 'w3_75_dynamical_relaxation_response_contract.md': '31a1e6bd28b6698e64b790fd4692aba6616af5613c3919f322a790c7296d9f4a',
}
FALSE_FLAGS = ('Full_PDE_pair_stability_proved', 'asymptotically_attracting_lock_derived',
               'collective_P_F_feedback_derived', 'damping_kernel_derived',
               'electromagnetic_alpha_derived', 'observational_pass', 'intuitive_files_changed')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else 'MISSING'


def native(value):
    if isinstance(value, dict): return {key:native(item) for key,item in value.items()}
    if isinstance(value, (list, tuple)): return [native(item) for item in value]
    return value.item() if isinstance(value, np.generic) else value


def symbolic_gate():
    z, delta, s, theta, dd, td = sp.symbols('z Delta s theta_mean dDelta dtheta_mean', real=True)
    K, D, k, C, V, E0, Omega, S, gamma = sp.symbols('K D k C V E0 Omega S gamma', positive=True)
    qt, q0, ql, qr, tl, tr, lam = sp.symbols('q_total q0 qL qR theta_L theta_R eigenvalue', real=True)
    qprime, radial_prime = sp.symbols('q_prime radial_q_prime', negative=True)
    kernel = 4*sp.pi*C**2*sp.exp(-k*D)/D
    H = s*z**2-K*sp.cos(delta)
    Horiginal = Omega*(ql+qr)+s*((ql-q0)**2+(qr-q0)**2)/2-K*sp.cos(tr-tl)
    substitution = {ql:q0+z, qr:q0-z, tl:theta-delta/2, tr:theta+delta/2}
    original_zdot = ((-sp.diff(Horiginal,tl)+sp.diff(Horiginal,tr))/2).subs(substitution)
    original_ddot = (sp.diff(Horiginal,qr)-sp.diff(Horiginal,ql)).subs(substitution)
    original_form = (qt/2+z)*(td-dd/2)+(qt/2-z)*(td+dd/2)
    crossq = 2*Omega*S*sp.cos(delta)
    crossE = Omega*crossq-K*sp.cos(delta)
    Hint = -kernel*sp.cos(delta)
    acceleration = -2*sp.diff(kernel,D)/E0
    sigma2 = -2*kernel/qprime
    recoil = -qprime*(k+1/D)/(2*E0)
    canonical = {'symplectic':-1, 'response_factor':2, 'solid_angle':4*sp.pi,
                 'force_sign':1, 'friction':0, 'charge_adjustment':-crossq}

    def validate(candidate):
        zdot = -sp.diff(H,delta)/candidate['symplectic']-candidate['friction']*z
        deltadot = candidate['response_factor']*s*z/candidate['symplectic']
        J = sp.Matrix([zdot,deltadot]).jacobian([z,delta])
        force_left = -candidate['force_sign']*sp.diff(kernel,D)*sp.cos(delta)
        pressure = candidate['force_sign']*D*sp.diff(kernel,D)*sp.cos(delta)/(3*V)
        residuals = {
            'relative_one_form':original_form-(qt*td+candidate['symplectic']*z*dd),
            'original_pairs_charge_equation':zdot-original_zdot,
            'original_pairs_phase_equation':deltadot-original_ddot,
            'relative_phase_Euler_Lagrange':candidate['symplectic']*deltadot-sp.diff(H,z),
            'relative_charge_Euler_Lagrange':candidate['symplectic']*zdot+sp.diff(H,delta),
            'linear_characteristic_polynomial':(lam*sp.eye(2)-J).det()-(lam**2+2*s*K*sp.cos(delta)),
            'closed_flow_divergence':sp.diff(zdot,z)+sp.diff(deltadot,delta),
            'full_angle_susceptibility':1/(candidate['solid_angle']*radial_prime)-1/(4*sp.pi*radial_prime),
            'fixed_charge_Legendre_cancellation':crossE+Omega*candidate['charge_adjustment']+K*sp.cos(delta),
            'force_from_interaction':force_left-sp.diff(Hint,D),
            'pressure_from_dilation':pressure+sp.diff(Hint,D)*D/(3*V),
            'pressure_from_once_counted_virial':pressure+D*force_left/(3*V),
            'recoil_Taylor_identity':acceleration/(2*sigma2)-recoil,
            'recoil_large_D_limit':sp.limit(k*recoil,D,sp.oo)+qprime*k**2/(2*E0),
        }
        return {name:sp.simplify(value) for name,value in residuals.items()}

    exact = validate(canonical)
    variants = {'reversed_relative_symplectic_sign':{'symplectic':1},
                'missing_imbalance_factor_two':{'response_factor':1},
                'omitted_solid_angle':{'solid_angle':1},
                'reversed_force_and_pressure':{'force_sign':-1},
                'inserted_closed_flow_friction':{'friction':gamma},
                'unadjusted_overlap_energy':{'charge_adjustment':0}}
    mutations = {}
    for name, change in variants.items():
        failed = {key:sp.sstr(value) for key,value in validate({**canonical, **change}).items() if value != 0}
        mutations[name] = {'detected':bool(failed), 'nonzero_production_residuals':failed}
    A = sp.Symbol('A',positive=True)
    eigen_squared = -2*s*K*sp.cos(delta)
    signs = {'negative_s_inphase':int(sp.sign(eigen_squared.subs({s:-A,delta:0}))),
             'negative_s_antiphase':int(sp.sign(eigen_squared.subs({s:-A,delta:sp.pi}))),
             'positive_s_inphase':int(sp.sign(eigen_squared.subs({s:A,delta:0}))),
             'positive_s_antiphase':int(sp.sign(eigen_squared.subs({s:A,delta:sp.pi}))),
             'decoupled_eigenvalue_squared':int(eigen_squared.subs(K,0))}
    return {'residuals':{key:sp.sstr(value) for key,value in exact.items()},
            'checks':{key:value == 0 for key,value in exact.items()}, 'negative_controls':mutations,
            'classification_signs':signs, 'classification_check':list(signs.values()) == [1,-1,-1,1,0]}


def numerical_gate(module):
    omega, k = .8, .6
    runs, checks = [], {}
    for i,tolerance in enumerate((1e-7,3e-8)):
        profile = module.solve_profile(omega,radius=80.,tolerance=tolerance)
        obs = module.profile_observables(profile,omega,80.,points=16001)
        sensitivity = module.solve_sensitivity(profile)
        x=np.linspace(0.,80.,16001); f=profile.sol(x)[0]
        C=float(simpson(x*np.sinh(k*x)*(f**3-.25*f**5),x=x)/k)
        runs.append({'tolerance':tolerance,'q_Omega':4*math.pi*sensitivity['dQ_dOmega'],
                     'radial_q_Omega':sensitivity['dQ_dOmega'],'E':4*math.pi*obs['energy_dimensionless'],
                     'C':C,'sensitivity':sensitivity})
        checks[f'run{i}_negative_sensitivity'] = sensitivity['dQ_dOmega'] < 0
    branch = module.branch_and_slope(profile)
    by_omega = {row['Omega']:row['observables'] for row in branch['branch']}
    stencils=[]
    for h,frequencies in ((.01,(.78,.79,.81,.82)),(.005,(.79,.795,.805,.81))):
        derivative=lambda key:4*math.pi*sum(w*by_omega[o][key] for w,o in zip((1,-8,8,-1),frequencies))/(12*h)
        qdot,edot=derivative('charge_dimensionless'),derivative('energy_dimensionless')
        firstlaw=abs(edot-omega*qdot)/abs(omega*qdot)
        checks[f'h{h}_negative_slope']=qdot<0
        checks[f'h{h}_first_law']=firstlaw<2e-3
        discrepancies=[]
        for i,run in enumerate(runs):
            error=abs(qdot-run['q_Omega'])/abs(run['q_Omega']); discrepancies.append(error)
            checks[f'run{i}_h{h}_sensitivity_stencil']=error<2e-2
        stencils.append({'h':h,'q_Omega':qdot,'E_Omega':edot,'relative_first_law_residual':firstlaw,
                         'relative_sensitivity_discrepancies':discrepancies})
    convergence={key:abs(runs[0][key]-runs[1][key])/abs(runs[1][key]) for key in ('q_Omega','E','C')}
    checks.update({f'profile_convergence_{key}':value<2e-4 for key,value in convergence.items()})
    ref=runs[-1]; diagnostics=[]
    for D in (20.,24.,28.):
        K=4*math.pi*ref['C']**2*math.exp(-k*D)/D
        sigma=math.sqrt(-2*K/ref['q_Omega'])
        recoil=abs(ref['q_Omega'])*(k+1/D)/(2*ref['E'])
        plus,minus=(omega+sigma)**2-1,(omega-sigma)**2-1
        diagnostics.append({'D':D,'K':K,'sigma_instantaneous':sigma,'inverse_sigma':1/sigma,
                            'sideband_plus_wave_number_squared':plus,'sideband_minus_wave_number_squared':minus,
                            'both_frozen_linear_sidebands_closed':plus<0 and minus<0,
                            'L_recoil_Taylor_diagnostic':recoil,'recoil_index':k*recoil,
                            'frozen_separation_valid_on_phase_time':k*recoil<=.1})
    return native({'checks':checks,'profile_runs':runs,'slope_stencils':stencils,'profile_convergence':convergence,
                   'diagnostics':diagnostics,'recoil_large_D_index':abs(ref['q_Omega'])*k*k/(2*ref['E'])})


def build_report():
    pins={str(path.relative_to(WORK3)):{'actual':digest(path),'expected':expected} for path,expected in PINS.items()}
    dependency_checks={key:value['actual']==value['expected'] for key,value in pins.items()}
    symbolic=symbolic_gate()
    exact_pass=all(symbolic['checks'].values()) and symbolic['classification_check']
    mutation_pass=all(row['detected'] for row in symbolic['negative_controls'].values())
    numerical={'checks':{},'diagnostics':[]}; error=None
    if all(dependency_checks.values()) and exact_pass and mutation_pass:
        try:
            spec=importlib.util.spec_from_file_location('w3_77_retained_w58',SOLVER)
            module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
            numerical=numerical_gate(module)  # Functions only; never W3-58.main().
        except Exception as exc: error=f'{type(exc).__name__}: {exc}'
    numerical_pass=bool(numerical['checks']) and all(numerical['checks'].values()) and error is None
    flags={'leading_exact_response_and_stress':exact_pass,'mutation_controls_pass':mutation_pass,
           'dependencies_pinned_exact':all(dependency_checks.values()),'numerical_crosschecks_pass':numerical_pass}
    aggregate=all(flags.values())
    flags.update({name:False for name in FALSE_FLAGS})
    flags['Frozen_separation_valid_on_phase_time']=bool(numerical['diagnostics']) and all(row['frozen_separation_valid_on_phase_time'] for row in numerical['diagnostics'])
    failures=[key for key,value in dependency_checks.items() if not value]+[key for key,value in symbolic['checks'].items() if not value]
    failures += [key for key,value in symbolic['negative_controls'].items() if not value['detected']]
    failures += [key for key,value in numerical['checks'].items() if not value]
    if not symbolic['classification_check']: failures.append('classification_signs')
    if error: failures.append(error)
    return native({'claim_id':'W3_77_PAIR_PHASE_SUSCEPTIBILITY_PRESSURE_PROJECTION','model_version':VERSION,
                   'status':'PASS_CONDITIONAL_LEADING_PAIR_RESPONSE_AND_SCOPE_DIAGNOSTICS' if aggregate else 'FAIL_W3_77_REGISTERED_GATE',
                   'aggregate_pass':aggregate,'failures':failures,'closure_flags':flags,'dependencies':pins,
                   'dependency_checks':dependency_checks,'symbolic':symbolic,'numerical':numerical,
                   'scope':'Leading instantaneous modulation; finite-D overlap corrections unbounded here. Recoil and sideband outcomes are diagnostics, not required positive claims.',
                   'provenance':{'source_sha256':digest(Path(__file__)),'contract_sha256':digest(CONTRACT),
                                 'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},'writes_files':False})


def main():
    try:
        report=build_report(); encoded=json.dumps(report,indent=2,sort_keys=True,allow_nan=False)
    except Exception as exc:
        report={'aggregate_pass':False,'status':'FAIL_W3_77_EXECUTION','failures':[f'{type(exc).__name__}: {exc}'],'writes_files':False}
        encoded=json.dumps(report,indent=2,allow_nan=False)
    print(encoded)
    raise SystemExit(0 if report['aggregate_pass'] else 1)


if __name__=='__main__':
    main()
