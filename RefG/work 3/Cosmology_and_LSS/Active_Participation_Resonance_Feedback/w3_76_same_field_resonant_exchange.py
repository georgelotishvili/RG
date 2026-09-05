#!/usr/bin/env python3
"""W3-76: no-write action/flux checks and the frozen three-profile witness."""
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
from scipy.integrate import quad_vec, simpson

HERE = Path(__file__).resolve().parent
WORK3 = HERE.parent.parent
CONTRACT = HERE / 'w3_76_same_field_resonant_exchange_contract.md'
VERSION = 'W3-76-v1.0'
CONTRACT_HASH = 'e10781a73470220065c664196efe0c361dbfb1c6c2404864e895d6ad2380bd02'
CORE = WORK3 / 'Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core'
SOLVER = CORE / 'w3_58_one_oscillon_coframe_localized_core.py'
PINS = {
    CONTRACT: CONTRACT_HASH,
    CORE / 'w3_58_one_oscillon_coframe_localized_core_preregistration.md': 'ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db',
    SOLVER: 'b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57',
    HERE / 'w3_50_neutral_collective_phase_density_bridge_contract.md': 'c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635',
    WORK3 / 'Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md': '6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879',
    HERE / 'w3_75_dynamical_relaxation_response_contract.md': '31a1e6bd28b6698e64b790fd4692aba6616af5613c3919f322a790c7296d9f4a',
}
FALSE_FLAGS = ('long_time_synchronization_derived', 'pair_stability_proved',
               'exact_rigid_two_core_solution', 'collective_pressure_feedback_derived',
               'microscopic_node_coupling_derived', 'electromagnetic_alpha_derived',
               'observational_pass', 'intuitive_files_changed')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else 'MISSING'


def symbolic_gate():
    r, b, k, C, D = sp.symbols('r b k C D', positive=True)
    f, fp, c, s, rho, omega, a = sp.symbols('f fp c s rho Omega a', real=True)
    q = sp.Rational

    def reduce(expr):
        expr = sp.rem(sp.expand(expr), s**2 + c**2 - 1, s)
        return sp.simplify(expr.subs(rho**2, r**2 - b**2).subs(omega**2, 1 - k**2))

    def potential(modulus_squared):
        return modulus_squared / 2 - modulus_squared**2 / 4 + a * modulus_squared**3 / 6

    u = f * (1 + c + sp.I * s)
    ux = b * fp * (1 - c - sp.I * s) / r
    ur = rho * fp * (1 + c + sp.I * s) / r
    ut = sp.I * omega * u
    square = lambda z: sp.expand(z * sp.conjugate(z))
    jx = reduce(-sp.im(sp.conjugate(u) * ux))
    energy = reduce(-sp.re(sp.conjugate(ut) * ux))
    full = reduce((square(ut) + square(ux) - square(ur)) / 2 - potential(square(u)))
    self_stress = reduce((omega**2 * f**2 + (b**2 - rho**2) * fp**2 / r**2) / 2 - potential(f**2))
    reals = (f * (1 + c), f * s)
    real_x = (b * fp * (1 - c) / r, -b * fp * s / r)
    real_t = (-omega * reals[1], omega * reals[0])
    real_r = (rho * fp * (1 + c) / r, rho * fp * s / r)
    real_current = -(reals[0] * real_x[1] - reals[1] * real_x[0])
    real_energy = -sum(v * w for v, w in zip(real_t, real_x))
    real_stress = (sum(v*v for v in real_t) + sum(v*v for v in real_x) - sum(v*v for v in real_r)) / 2 - potential(sum(v*v for v in reals))
    quadratic = -c * (fp**2 + k**2 * f**2)
    quartic = f**4 * ((1 + c)**2 - q(1, 2))
    sextic = -a * f**6 * (q(4, 3) * (1 + c)**3 - q(1, 3))
    expected_stress = quadratic + quartic + sextic
    pr = fp**2 / 2 - k**2 * f**2 / 2 + f**4 / 4 - a * f**6 / 6
    fpp = k**2 * f - f**3 + a * f**5 - 2 * fp / r
    radial_d = lambda e: sp.diff(e, r) + sp.diff(e, f) * fp + sp.diff(e, fp) * fpp
    fy = C * sp.exp(-k*r) / r
    primitive = C**2 * sp.exp(-2*k*r) * (k/r + 1/(2*r**2))
    kernel = 4 * sp.pi * C**2 * sp.exp(-k*D) / D
    left, right = sp.symbols('theta_L theta_R', real=True)
    generator = -kernel * sp.cos(right-left)
    I, J, source = sp.symbols('I J source')
    green = (sp.exp(-k*r)*I + sp.sinh(k*r)*J) / k
    green_d = lambda e: sp.diff(e, r) + sp.diff(e, I)*r*sp.sinh(k*r)*source - sp.diff(e, J)*r*sp.exp(-k*r)*source
    base = {
        'complex_real_current': jx-real_current,
        'complex_real_energy_flux': energy-real_energy,
        'complex_real_full_stress': full-real_stress,
        'instantaneous_energy_charge_flux': energy-omega*jx,
        'current_radial_antiderivative': radial_d(2*sp.pi*b*f**2*s)-2*sp.pi*r*jx,
        'radial_pressure_balance': radial_d(pr)+2*fp**2/r,
        'isolated_plane_stress_boundary': radial_d((r**2-b**2)*pr/2)-r*self_stress,
        'Yukawa_force_antiderivative': sp.diff(primitive,r)+r*(sp.diff(fy,r)**2+k**2*fy**2),
        'Yukawa_kernel_boundary': 2*sp.pi*b*fy.subs(r,b)**2-kernel.subs(D,2*b),
        'Yukawa_force_kernel': 2*sp.pi*primitive.subs(r,D/2)+sp.diff(kernel,D),
        'generator_force': sp.diff(generator,D)+sp.diff(kernel,D)*sp.cos(right-left),
        'generator_charge': -sp.diff(generator,left)-kernel*sp.sin(right-left),
        'radial_Green_source_equation': -green_d(sp.simplify(green_d(green)))+k**2*green-r*source,
    }
    canonical = {'current': 2*b*f*fp*s/r, 'energy': omega*2*b*f*fp*s/r,
                 'stress': expected_stress, 'orientation': -1, 'exponent': k}

    def validate(candidate):
        exterior = C*sp.exp(-candidate['exponent']*r)/r
        residuals = dict(base)
        residuals.update({'action_current': candidate['current']-jx,
                          'raised_energy_flux': candidate['energy']-energy,
                          'full_sextic_cross_stress': candidate['stress']-(full-2*self_stress),
                          'left_boundary_orientation': candidate['orientation']*(-2*sp.pi*b*f**2*s)-2*sp.pi*b*f**2*s,
                          'exterior_vacuum_equation': sp.diff(exterior,r,2)+2*sp.diff(exterior,r)/r-k**2*exterior})
        return {name: reduce(value) for name,value in residuals.items()}

    exact = validate(canonical)
    mutations = {'reversed_current_sign': {'current': -canonical['current']},
                 'missing_factor_two': {'current': canonical['current']/2},
                 'two_independent_fields': {'current': sp.Integer(0)},
                 'reversed_raised_energy_sign': {'energy': -canonical['energy']},
                 'removed_quartic_cross': {'stress': expected_stress-quartic},
                 'removed_sextic_cross': {'stress': expected_stress-sextic},
                 'reversed_left_orientation': {'orientation': 1},
                 'wrong_Yukawa_exponent': {'exponent': 2*k}}
    controls = {}
    for name, change in mutations.items():
        bad = {key:sp.sstr(value) for key,value in validate({**canonical, **change}).items() if value != 0}
        controls[name] = {'detected': bool(bad), 'nonzero_production_residuals': bad}
    # Endpoint extrema on -1<=cos(Delta)<=1; both coefficients are monotone.
    coeff4, coeff6 = quartic/f**4, -sextic/(a*f**6)
    bounds = {'quartic_maximum_exact': max(abs(coeff4.subs(c,z)) for z in (-1,1)) == q(7,2),
              'sextic_maximum_exact': max(abs(coeff6.subs(c,z)) for z in (-1,1)) == q(31,3)}
    return {'residuals': {key:sp.sstr(value) for key,value in exact.items()},
            'checks': {key:value == 0 for key,value in exact.items()}, 'nonlinear_bound_checks': bounds,
            'negative_controls': controls}


def numerical_gate(module):
    omega, a = 0.8, 0.25
    k = math.sqrt(1-omega**2)
    runs, checks = [], {}
    phases = (('0',0.0), ('pi/2',math.pi/2), ('pi',math.pi))
    for index, (X,tol) in enumerate(((60.,1e-7),(80.,1e-7),(80.,3e-8))):
        solution = module.solve_profile(omega, radius=X, tolerance=tol)
        obs = module.profile_observables(solution, omega, X, points=8001)
        checks[f'run{index}_shape'] = bool(obs['minimum_amplitude']>0 and obs['central_amplitude']>0 and obs['maximum_positive_derivative']<=0)
        checks[f'run{index}_profile_residual'] = obs['equation_normalized_weighted_l2_residual'] < 2e-5
        green_values = []
        for points in (4001,8001):
            rr=np.linspace(0,X,points); ff=solution.sol(rr)[0]
            green_values.append(float(simpson(rr*np.sinh(k*rr)*(ff**3-a*ff**5),x=rr)/k))
        C=green_values[-1]
        C16=float(16*solution.sol(16)[0]*math.exp(16*k))
        green_error=abs(C-C16)/abs(C)
        green_refinement=abs(green_values[0]-C)/abs(C)
        checks[f'run{index}_Green_exterior'] = green_error < 2e-3
        checks[f'run{index}_Green_quadrature'] = green_refinement < 2e-4
        records, kernels = [], []
        for D in (20.,24.,28.):
            b=D/2; fb,fX=float(solution.sol(b)[0]),float(solution.sol(X)[0])
            Kexact=math.pi*D*fb**2; Kcut=math.pi*D*(fb**2-fX**2)
            Klead=4*math.pi*C**2*math.exp(-k*D)/D
            force_scale=Klead*(k+1/D)
            kernels.append(Kexact)
            checks[f'run{index}_D{D:g}_kernel'] = abs(Kexact-Klead)/Klead < 5e-3
            for phase_name, phase in phases:
                cosine,sine=math.cos(phase),math.sin(phase)
                radial=[]
                for points in (4001,8001):
                    rr=np.linspace(b,X,points); ff,gg=solution.sol(rr)
                    excess=-cosine*(gg**2+k**2*ff**2)+ff**4*((1+cosine)**2-.5)-a*ff**6*((4/3)*(1+cosine)**3-1/3)
                    self_t=(b*b/rr**2-.5)*gg**2-.5*k*k*ff**2+.25*ff**4-a*ff**6/6
                    qleft=float(-4*math.pi*b*sine*simpson(ff*gg,x=rr))
                    self_integral=float(2*math.pi*simpson(rr*self_t,x=rr))
                    fex=float(-2*math.pi*simpson(rr*excess,x=rr))
                    radial.append(np.array([qleft,omega*qleft,fex-2*self_integral,fex,self_integral]))
                def cylindrical(sigma):
                    radius=math.hypot(b,sigma); ff,gg=solution.sol(radius)
                    phase_factor=complex(cosine,sine)
                    u=ff*(1+phase_factor); ux=(b/radius)*gg*(1-phase_factor)
                    ur=(sigma/radius)*gg*(1+phase_factor); ut=1j*omega*u
                    mod2=abs(u)**2; v=mod2/2-mod2**2/4+a*mod2**3/6
                    txx=(abs(ut)**2+abs(ux)**2-abs(ur)**2)/2-v
                    self_t=(omega**2*ff**2+(b*b-sigma*sigma)*gg**2/radius**2)/2-(ff**2/2-ff**4/4+a*ff**6/6)
                    jx=-(u.conjugate()*ux).imag
                    t0x=-(ut.conjugate()*ux).real
                    return -2*math.pi*sigma*np.array([jx,t0x,txx,txx-2*self_t])
                cylindrical_value,quad_error=quad_vec(cylindrical,0,math.sqrt(X*X-b*b),epsabs=1e-14,epsrel=3e-10,limit=2000)
                high=radial[-1]; scales=np.array([Kcut,omega*Kcut,force_scale,force_scale])
                integration_error=float(np.max(np.abs(cylindrical_value-high[:4])/scales))
                refinement=float(np.max(np.abs(radial[0][:4]-high[:4])/scales))
                boundary_error=abs(high[0]-Kcut*sine)/Kcut
                lead_error=abs(high[3]-force_scale*cosine)/force_scale
                self_normalized=abs(high[4])/force_scale
                prX=float(solution.sol(X)[1]**2/2-k*k*fX*fX/2+fX**4/4-a*fX**6/6)
                self_boundary_error=abs(high[4]-math.pi*(X*X-b*b)*prX)/force_scale
                key=f'run{index}_D{D:g}_{phase_name}'
                for label,error,budget in (('independent_surface',integration_error,2e-4),('refinement',refinement,2e-4),('current_boundary',boundary_error,2e-4),('leading_force',lead_error,5e-3),('self_stress',self_normalized,2e-4),('self_boundary',self_boundary_error,2e-4)):
                    checks[f'{key}_{label}']=error<budget
                if phase_name=='pi/2':
                    checks[f'{key}_nonzero_transfer']=bool(high[0]>0 and high[1]>0)
                records.append({'D':D,'phase':phase_name,'K_exact':Kexact,'K_leading':Klead,
                                'charge_into_left':float(high[0]),'energy_into_left':float(high[1]),
                                'force_excess':float(high[3]),'force_leading':force_scale*cosine,
                                'surface_discrepancy':integration_error,'quadrature_change':refinement,
                                'current_boundary_error':boundary_error,'leading_force_error':lead_error,
                                'self_stress_normalized':self_normalized,'self_boundary_error':self_boundary_error,
                                'quad_absolute_error_estimate':float(quad_error)})
        runs.append({'X':X,'tolerance':tol,'C_Green':C,'C_exterior_r16':C16,'Green_exterior_error':green_error,
                     'Green_refinement':green_refinement,'observables':{key:obs[key] for key in ('central_amplitude','energy_dimensionless','charge_dimensionless','charge_rms_radius_dimensionless','equation_normalized_weighted_l2_residual')},
                     'kernels':kernels,'surface_witnesses':records})
    reference=runs[-1]
    for index,run in enumerate(runs[:-1]):
        for key in ('energy_dimensionless','charge_dimensionless','charge_rms_radius_dimensionless'):
            error=abs(run['observables'][key]-reference['observables'][key])/abs(reference['observables'][key])
            checks[f'run{index}_{key}_convergence']=error<2e-4
        for j,(value,ref) in enumerate(zip(run['kernels'],reference['kernels'])):
            checks[f'run{index}_kernel{j}_convergence']=abs(value-ref)/abs(ref)<2e-4
    return {'checks':{name:bool(value) for name,value in checks.items()},'runs':runs,'normalization':'Charge by K_exact; energy by Omega*K_exact; every force/self-stress by positive -K_leading_prime, including pi/2.'}


def build_report():
    pins={str(path.relative_to(WORK3)):{'actual':digest(path),'expected':expected} for path,expected in PINS.items()}
    hash_checks={name:entry['actual']==entry['expected'] for name,entry in pins.items()}
    symbolic=symbolic_gate()
    exact_pass=all(symbolic['checks'].values()) and all(symbolic['nonlinear_bound_checks'].values())
    mutation_pass=all(v['detected'] for v in symbolic['negative_controls'].values())
    numeric={'checks':{},'runs':[]}; error=None
    if all(hash_checks.values()) and exact_pass and mutation_pass:
        try:
            spec=importlib.util.spec_from_file_location('w3_76_retained_w58',SOLVER)
            module=importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # Import functions only; never invoke W3-58.main().
            numeric=numerical_gate(module)
        except Exception as exc:
            error=f'{type(exc).__name__}: {exc}'
    numeric_pass=bool(numeric['checks']) and all(numeric['checks'].values()) and error is None
    flags={'exact_current_energy_stress_and_kernel':exact_pass,'production_mutation_controls_pass':mutation_pass,
           'dependency_hashes_exact':all(hash_checks.values()),'numerical_pair_flux_witness_pass':numeric_pass}
    flags.update({name:False for name in FALSE_FLAGS})
    passed=all(flags[name] for name in flags if name not in FALSE_FLAGS) and all(not flags[name] for name in FALSE_FLAGS)
    status='PASS_EXACT_INITIAL_PAIR_EXCHANGE_AND_ASYMPTOTIC_KERNEL__NUMERICAL_WITNESS' if passed else ('NUMERICALLY_INCONCLUSIVE_W3_76' if error else 'FAIL_W3_76_REGISTERED_GATE')
    failures=[name for name,value in hash_checks.items() if not value]+[name for name,value in symbolic['checks'].items() if not value]+[name for name,value in symbolic['nonlinear_bound_checks'].items() if not value]+[name for name,value in symbolic['negative_controls'].items() if not value['detected']]+[name for name,value in numeric['checks'].items() if not value]
    if error: failures.append(error)
    return {'claim_id':'W3_76_SAME_FIELD_RESONANT_EXCHANGE','model_version':VERSION,'status':status,
            'aggregate_pass':passed,'failures':failures,'closure_flags':flags,'dependencies':pins,'dependency_checks':hash_checks,
            'symbolic':symbolic,'numerical':numeric,'scope':'Exact flux of specified one-field initial data; large-D kernel and floating-point witness. No rigid two-core solution, phase-locking attractor, or collective pressure feedback is claimed.',
            'provenance':{'source_sha256':digest(Path(__file__)),'contract_sha256':digest(CONTRACT),'python':sys.version.split()[0],'sympy':sp.__version__,'numpy':np.__version__,'scipy':scipy.__version__},'writes_files':False}


def main():
    try:
        report=build_report()
        encoded=json.dumps(report,indent=2,sort_keys=True,allow_nan=False)
    except Exception as exc:
        report={'aggregate_pass':False,'status':'FAIL_W3_76_EXECUTION','failures':[f'{type(exc).__name__}: {exc}'],'writes_files':False}
        encoded=json.dumps(report,indent=2,sort_keys=True,allow_nan=False)
    print(encoded)
    raise SystemExit(0 if report['aggregate_pass'] else 1)


if __name__=='__main__':
    main()
