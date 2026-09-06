#!/usr/bin/env python3
"""W3-79: no-write exact local scalar/current/Einstein source audit.

Run with python -B. Finite JSON goes to stdout; progress goes to stderr.
The cold LTB annulus is an exact regression, not a selected physical EOS.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as sp

VERSION = 'W3-79-v1.0'
SOURCE = Path(__file__).resolve()
ROOT = SOURCE.parents[4]
CONTRACT = SOURCE.with_name('w3_79_collective_current_backreaction_contract.md')
CONTRACT_SHA = '7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa'
W73_REL = ('RefG/work 3/Strong_Field/'
           'W3-73_Coupled_Horizon_Regular_Einstein_Complex_Scalar/')
PINS = {
    'CODES.md': '27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41',
    'RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/'
    'w3_54_relational_coframe_tegr_phase_source_closure_contract.md':
        '6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879',
    'RefG/work 3/Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/'
    'w3_58_one_oscillon_coframe_localized_core_preregistration.md':
        'ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db',
    W73_REL + 'w3_73_coupled_horizon_regular_einstein_complex_scalar_preregistration.md':
        '8a3c3887fc0a28edc8fced67da0bc66ccaff39ade1f6e5b7e339f579fc02c49e',
    W73_REL + 'w3_73_coupled_horizon_regular_einstein_complex_scalar.py':
        '47f2c97b64544f124cc2a5cb8d04825188664493cb5d770b6c3faf4ce2d5d7ca',
    'RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/'
    'w3_75_dynamical_relaxation_response_contract.md':
        '31a1e6bd28b6698e64b790fd4692aba6616af5613c3919f322a790c7296d9f4a',
}
FALSE_FLAGS = (
    'high_density_EOS_selected', 'foundation_pressure_feedback_derived',
    'full_nonstatic_material_scale_map', 'collective_origin_from_ordinary_modes',
    'nonlinear_oscillon_collapse_solved', 'regular_centre_derived',
    'singularity_resolution', 'observational_pass', 'intuitive_files_changed',
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(expr):
    return sp.factor(sp.simplify(expr))


def audit(residuals):
    normalized = {name: clean(value) for name, value in residuals.items()}
    return {
        'all_exact': all(value == 0 for value in normalized.values()),
        'residuals': {name: sp.sstr(value) for name, value in normalized.items()},
        'checks': {name: bool(value == 0) for name, value in normalized.items()},
    }


def progress(message):
    print(message, file=sys.stderr, flush=True)


def provenance():
    items = {name: {'expected': expected, 'actual': sha(ROOT / name)}
             for name, expected in PINS.items()}
    package = sorted(p.name for p in SOURCE.parent.iterdir())
    expected_package = sorted([SOURCE.name, CONTRACT.name])
    result = {
        'dependencies': items, 'contract_sha256': sha(CONTRACT),
        'expected_contract_sha256': CONTRACT_SHA, 'source_sha256': sha(SOURCE),
        'package_files': package, 'exact_two_file_package': package == expected_package,
        'python': platform.python_version(), 'sympy': sp.__version__,
        'numpy': np.__version__, 'scipy': scipy.__version__,
        'bytecode_disabled': sys.dont_write_bytecode,
    }
    result['all_pass'] = (all(x['expected'] == x['actual'] for x in items.values())
                          and result['contract_sha256'] == CONTRACT_SHA
                          and result['exact_two_file_package']
                          and result['bytecode_disabled'])
    return result


def load_geometry():
    path = ROOT / (W73_REL + 'w3_73_coupled_horizon_regular_einstein_complex_scalar.py')
    spec = importlib.util.spec_from_file_location('w79_w73_geometry', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    # Only this pure symbolic function is called, never the old main/report writer.
    return module, module.geometry_base()


def action_variation():
    """Actual pointwise metric/current differentiation before any PG ansatz.

    A local Lorentz frame suffices for the tensor variation. All ten independent
    metric components are varied; the flow/ordinary gradients are spherical.
    """
    eps = sp.symbols('epsilon', real=True)
    n = sp.symbols('n', positive=True)
    v = sp.symbols('v', real=True)
    gam = 1 / sp.sqrt(1-v*v)
    jt, jr = sp.symbols('J0 J1', real=True)
    q0, q1 = sp.symbols('theta0 theta1', real=True)
    eta = sp.diag(-1, 1, 1, 1)
    rho = sp.Function('rho')
    mu = sp.diff(rho(n), n)
    pressure = n*mu-rho(n)
    density = sp.sqrt(jt*jt-jr*jr)
    lag_current = jt*q0+jr*q1-rho(density)
    substitution = {jt: n*gam, jr: n*gam*v}
    residuals = {}
    for index, (j, target) in enumerate(((jt, q0-mu*gam),
                                        (jr, q1+mu*gam*v))):
        derivative = sp.diff(lag_current, j).subs(substitution)
        residuals['current_variation_' + str(index)] = derivative-target
    p0, p1, f0, f1, potential = sp.symbols('Pi1 Pi2 Phi1 Phi2 V', real=True)
    grads = (sp.Matrix([p0, f0, 0, 0]), sp.Matrix([p1, f1, 0, 0]))
    flow = sp.Matrix([gam, gam*v, 0, 0])
    collective_up = n*mu*flow*flow.T+pressure*eta
    kinetic = sum((a.T*eta*a)[0] for a in grads)
    scalar_up = sum((eta*a*a.T*eta for a in grads), sp.zeros(4))
    scalar_up -= eta*(kinetic/2+potential)
    jvector = n*flow
    for a in range(4):
        for b in range(a, 4):
            delta = sp.zeros(4)
            delta[a,b] = 1
            delta[b,a] = 1
            metric = eta+eps*delta
            inv = metric.inv()
            vol = sp.sqrt(-metric.det())
            nd = sp.sqrt(-(jvector.T*metric*jvector)[0])/vol
            lag_c = -vol*rho(nd)
            lag_o = -vol*(sum((x.T*inv*x)[0] for x in grads)/2+potential)
            weight = sp.Rational(1,2) if a == b else 1
            residuals[f'Hilbert_collective_{a}{b}'] = (
                sp.diff(lag_c, eps).subs(eps,0)-weight*collective_up[a,b])
            residuals[f'Hilbert_ordinary_{a}{b}'] = (
                sp.diff(lag_o, eps).subs(eps,0)-weight*scalar_up[a,b])
    # The density-valued J theta term has identically no metric dependence.
    residuals['phase_term_metric_independent'] = sp.diff(jt*q0+jr*q1, eps)
    residuals['enthalpy_identity'] = rho(n)+pressure-n*mu
    residuals['thermodynamic_pressure_derivative'] = sp.diff(pressure,n)-n*sp.diff(mu,n)
    result = audit(residuals)
    result['variation_domain'] = 'Local orthonormal frame; n>0, |v|<1; arbitrary rho(n).'
    return result


def warped_geometry(w, full):
    """Independent two-dimensional warped-product Einstein calculation."""
    t, r, sig, z = w.T, w.R, w.SIGMA, w.ZETA
    coords = (t,r)
    h = sp.Matrix([[-sig**2*(1-z*z),sig*z],[sig*z,1]])
    inv = h.inv()
    gamma = [[[clean(sum(inv[i,l]*(sp.diff(h[l,k],coords[j])
                          +sp.diff(h[l,j],coords[k])-sp.diff(h[j,k],coords[l]))/2
                          for l in range(2))) for k in range(2)]
                          for j in range(2)] for i in range(2)]
    ric = sp.zeros(2)
    for a in range(2):
        for b in range(2):
            ric[a,b] = clean(sum(sp.diff(gamma[c][a][b],coords[c])
                  -sp.diff(gamma[c][a][c],coords[b])
                  +sum(gamma[c][c][d]*gamma[d][a][b]
                      -gamma[c][b][d]*gamma[d][a][c] for d in range(2))
                  for c in range(2)))
    r2 = clean(sum(inv[a,b]*ric[a,b] for a in range(2) for b in range(2)))
    hess_r = sp.Matrix(2,2,lambda a,b: -gamma[1][a][b])
    boxr = clean(sum(inv[a,b]*hess_r[a,b] for a in range(2) for b in range(2)))
    gab = -2*hess_r/r+(2*boxr/r+(inv[1,1]-1)/r**2)*h
    gtheta = r*boxr-r*r*r2/2
    residuals = {f'warped_vs_full_G_{a}{b}': gab[a,b]-full['einstein'][a,b]
                 for a in range(2) for b in range(2)}
    residuals['warped_vs_full_G_angular'] = gtheta-full['einstein'][2,2]
    residuals.update({f'full_Bianchi_{i}': expr for i,expr in enumerate(full['bianchi'])})
    return audit(residuals)


def divergence_mixed(tensor_cov, w, geom):
    coords = (w.T,w.R,w.THETA,w.AZIMUTH)
    mixed = geom['inverse']*tensor_cov
    gamma = geom['gamma']
    return [sp.diff(mixed[0,nu],coords[0])+sp.diff(mixed[1,nu],coords[1])
            +sum(gamma[m][m][l]*mixed[l,nu]-gamma[l][m][nu]*mixed[m,l]
                 for m in range(4) for l in range(4)) for nu in (0,1)]


def current_and_ward(w, geom):
    t,r,sig,z = w.T,w.R,w.SIGMA,w.ZETA
    n = sp.Function('n')(t,r)
    v = sp.Function('v')(t,r)
    mu = sp.Function('mu')(n)
    rho = sp.Function('rho')(n)
    gam = 1/sp.sqrt(1-v*v)
    D,B,W = n*gam,mu*gam*v,mu*gam
    u = sp.Matrix([gam/sig,gam*(v-z),0,0])
    ucov = geom['metric']*u
    P = n*mu-rho
    tc = n*mu*ucov*ucov.T+P*geom['metric']
    C = (sp.diff(r*r*D,t)+sp.diff(sig*r*r*D*(v-z),r))/(sig*r*r)
    EB = sp.diff(B,t)+sp.diff(sig*(W-z*B),r)
    div = divergence_mixed(tc,w,geom)
    residuals = {
        'four_velocity_normalization': (ucov.T*u)[0]+1,
        'phase_T_projection': -mu*ucov[0]-sig*(W-z*B),
        'phase_r_projection': -mu*ucov[1]+B,
        'current_coordinate_T': n*u[0]-D/sig,
        'current_coordinate_r': n*u[1]-D*(v-z),
        'densitized_current_divergence':
            sp.diff(sig*r*r*n*u[0],t)+sp.diff(sig*r*r*n*u[1],r)-sig*r*r*C,
        'phase_integrability': sp.diff(B,t)+sp.diff(sig*(W-z*B),r)-EB,
        'collective_Ward_T': div[0]-mu*ucov[0]*C+n*u[1]*EB,
        'collective_Ward_r': div[1]-mu*ucov[1]*C-n*u[0]*EB,
    }
    residuals = {key: value.subs(sp.diff(rho,n),mu) for key,value in residuals.items()}
    # Ordinary Cartesian fields and their action-derived Euler equations.
    phi = (w.PHI1,w.PHI2)
    pi = (w.PI1,w.PI2)
    rad = (w.RAD1,w.RAD2)
    matter = w.matter_quantities()
    grads = [sp.Matrix([sig*(pi[i]+z*rad[i]),rad[i],0,0]) for i in range(2)]
    kin = sum((g.T*geom['inverse']*g)[0] for g in grads)
    to = sum((g*g.T for g in grads),sp.zeros(4))
    to -= geom['metric']*(kin/2+matter['potential'])
    phit = [sig*(pi[i]+z*rad[i]) for i in range(2)]
    pit = [sp.diff(sig*r*r*(rad[i]+z*pi[i]),r)/(r*r)-sig*matter['gradients'][i]
           for i in range(2)]
    replacements = {sp.diff(phi[i],t):phit[i] for i in range(2)}
    replacements.update({sp.diff(pi[i],t):pit[i] for i in range(2)})
    replacements.update({sp.diff(rad[i],t):sp.diff(phit[i],r) for i in range(2)})
    radial_map = {sp.diff(phi[i],r):rad[i] for i in range(2)}
    for index,expr in enumerate(divergence_mixed(to,w,geom)):
        residuals['ordinary_covariant_conservation_'+str(index)] = (
            expr.subs(replacements,simultaneous=True).subs(radial_map))
    for i in range(2):
        # 1/e partial_mu(e g^munu partial_nu phi) - V_,phi.
        vector = geom['inverse']*grads[i]
        wave = (sp.diff(sig*r*r*vector[0],t)+sp.diff(sig*r*r*vector[1],r))/(sig*r*r)
        residuals['ordinary_action_Euler_'+str(i)] = (
            (wave-matter['gradients'][i]).subs(replacements,simultaneous=True).subs(radial_map))
    qo,so = matter['q'],matter['s_o']
    residuals['ordinary_U1_Noether'] = (
        (sp.diff(r*r*qo,t)-sp.diff(sig*r*r*(z*qo+so),r))
        .subs(replacements,simultaneous=True).subs(radial_map))
    ntime,scale = sp.Function('nh')(t),sp.Function('A')(t)
    residuals['homogeneous_current_dilution'] = (
        sp.diff(scale**3*ntime,t)/scale**3-sp.diff(ntime,t)-3*sp.diff(scale,t)*ntime/scale)
    return audit(residuals)


def primitive_checks():
    n, mu = sp.symbols('n mu',positive=True)
    v = sp.symbols('v',real=True)
    c = sp.symbols('c_s',nonnegative=True)
    x = sp.symbols('speed',real=True)
    gamma = 1/sp.sqrt(1-v*v)
    D,B,W = n*gamma,mu*gamma*v,mu*gamma
    def dn(expression):
        return sp.diff(expression,n)+sp.diff(expression,mu)*mu*c*c/n
    jac = sp.Matrix([[dn(D),sp.diff(D,v)],[dn(B),sp.diff(B,v)]])
    fluxjac = sp.Matrix([[dn(D*v),sp.diff(D*v,v)],[dn(W),sp.diff(W,v)]])*jac.inv()
    den = 1-c*c*v*v
    expected = sp.Matrix([[v*(1-c*c)/den,n/(mu*gamma**2*den)],
                          [mu*c*c/(n*gamma**2*den),v*(1-c*c)/den]])
    A0 = sp.Matrix([[c*c,c*c*v],[c*c*v,1]])
    A1 = sp.Matrix([[c*c*v,c*c],[c*c,v]])
    # Actual variable transformation from conservative equations to ln n,rapidity.
    transform = sp.diag(n,1-v*v)
    raw0,raw1 = jac*transform,fluxjac*jac*transform
    sym = sp.diag(c*c/D,1/W)
    res = {'primitive_Jacobian':jac.det()-mu*gamma**4*den,
           'symmetrizer_positive_minor':A0[0,0]-c*c,
           'symmetrizer_positive_determinant':A0.det()-c*c*den,
           'acoustic_characteristic_polynomial':
               (A1-x*A0).det()-c*c*((v-x)**2-c*c*(1-v*x)**2)}
    for i in range(2):
        for j in range(2):
            res[f'flux_Jacobian_{i}{j}'] = fluxjac[i,j]-expected[i,j]
            res[f'principal_symmetrization_time_{i}{j}'] = (sym*raw0-A0)[i,j]
            res[f'principal_symmetrization_space_{i}{j}'] = (sym*raw1-A1)[i,j]
    for sign in (-1,1):
        speed = (v+sign*c)/(1+sign*v*c)
        res[f'sound_eigenvalue_{sign}'] = (fluxjac-speed*sp.eye(2)).det()
        res[f'sound_metric_cone_{sign}'] = 1-speed**2-(1-v*v)*(1-c*c)/(1+sign*v*c)**2
        res[f'stiff_metric_null_{sign}'] = speed.subs(c,1)-sign
        res[f'horizon_speed_{sign}'] = speed-1+(1-v)*(1-sign*c)/(1+sign*v*c)
    dust = fluxjac.subs(c,0)
    res['dust_Jordan_diagonal_0'] = dust[0,0]-v
    res['dust_Jordan_diagonal_1'] = dust[1,1]-v
    res['dust_Jordan_lower'] = dust[1,0]
    res['dust_Jordan_nonzero_upper'] = dust[0,1]-n*(1-v*v)/mu
    sig,z = sp.symbols('sigma zeta',positive=True)
    # The unchanged scalar first-order equations have this coordinate principal
    # block when written as y_T+A y_r=lower-order terms.
    scalar_block=-sig*sp.Matrix([[z,1],[1,z]])
    for sign in (-1,1):
        res[f'ordinary_scalar_metric_null_{sign}'] = (
            scalar_block-sig*(sign-z)*sp.eye(2)).det()
    result = audit(res)
    result['positive_branch'] = 'n,mu>0; |v|<1; 0<c_s^2<=1; A0 positive definite.'
    result['primitive_recovery'] = 'Locally invertible on physical image only.'
    result['dust_branch'] = 'c_s=0: repeated eigenvalue; strictly positive Jordan upper entry; defective Eulerian block.'
    result['dust_symmetric_hyperbolicity_claimed'] = False
    result['trapped_annulus'] = 'zeta>1 subtracts a strictly larger shift than every causal sound speed.'
    return result


def source_geometry_balances(w, geom):
    t,r,sig,z,G = w.T,w.R,w.SIGMA,w.ZETA,w.GNEWTON
    rho,S,pr,pT = [sp.Function(name)(t,r) for name in ('rho','S','pr','pT')]
    sig_r = -4*sp.pi*G*r*sig*S/z
    z_r = 4*sp.pi*G*r*(rho/z+S)-z/(2*r)
    z_t = sig*z*sp.diff(z,r)-sp.diff(sig,r)+sig*z*z/(2*r)+4*sp.pi*G*sig*r*pr
    def on_geometry(expr):
        expr = expr.subs(sp.diff(z,t),z_t)
        return clean(expr.subs({sp.diff(sig,r):sig_r,sp.diff(z,r):z_r},simultaneous=True))
    mr = 4*sp.pi*r*r*(rho+z*S)
    mt = 4*sp.pi*sig*r*r*(z*(rho+pr)+(1+z*z)*S)
    mass = r*z*z/(2*G)
    res = {'Einstein_00':on_geometry(geom['g00']-8*sp.pi*G*rho),
           'Einstein_01':on_geometry(geom['g01']-8*sp.pi*G*S),
           'Einstein_11':on_geometry(geom['g11']-8*sp.pi*G*pr),
           'mass_radial':on_geometry(sp.diff(mass,r)-mr),
           'mass_temporal':on_geometry(sp.diff(mass,t)-mt)}
    res['marginal_metric_nondegeneracy'] = (
        geom['metric'].det().subs(z,1)+sig**2*r**4*sp.sin(w.THETA)**2)
    tetrad = sp.Matrix([[sig,0,0,0],[sig*z,1,0,0],
                       [0,0,r,0],[0,0,0,r*sp.sin(w.THETA)]])
    frameT = sp.Matrix([[rho,S,0,0],[S,pr,0,0],[0,0,pT,0],[0,0,0,pT]])
    tcov = tetrad.T*frameT*tetrad
    divT = divergence_mixed(tcov,w,geom)
    # The Kodama current -T^mu_T/sigma yields the two mass source formulas.
    mixed = geom['inverse']*tcov
    res['Kodama_mass_density'] = mixed[0,0]+rho+z*S
    res['Kodama_mass_flux'] = mixed[1,0]-mt/(4*sp.pi*r*r)
    integrability = sp.diff(mr,t)-sp.diff(mt,r)
    # After radial/evolution Einstein constraints, the source curl is -4pi r² divT_T.
    res['total_mass_integrability_Ward'] = on_geometry(integrability+4*sp.pi*r*r*divT[0])
    # Vanishing base Einstein residuals and covariant Ward identities force angular
    # residual via the radial contracted Bianchi identity (r>0).
    angular_error = sp.Function('angular_error')(t,r)
    angular_tensor = sp.diag(0,0,r*r*angular_error,
                            r*r*sp.sin(w.THETA)**2*angular_error)
    residual_div = divergence_mixed(angular_tensor,w,geom)
    res['angular_equation_from_Bianchi'] = residual_div[1]+2*angular_error/r
    v,n,mu = sp.symbols('v n mu',real=True)
    gamma2=1/(1-v*v)
    P=sp.symbols('P_C',real=True)
    fluid=(n*mu*gamma2-P,-n*mu*gamma2*v,n*mu*gamma2*v*v+P)
    res['collective_mass_flux_factorization'] = (
        z*(fluid[0]+fluid[2])+(1+z*z)*fluid[1]-n*mu*gamma2*(z-v)*(1-z*v))
    a,b,c,d,V = sp.symbols('Pi1 Pi2 Phi1 Phi2 V',real=True)
    ordinary=((a*a+b*b+c*c+d*d)/2+V,a*c+b*d,(a*a+b*b+c*c+d*d)/2-V)
    fluxH = ordinary[0]+ordinary[2]+2*ordinary[1]+fluid[0]+fluid[2]+2*fluid[1]
    res['outer_horizon_positive_flux'] = fluxH-(a+c)**2-(b+d)**2-n*mu*gamma2*(1-v)**2
    mrH,mtH,Rdot = sp.symbols('m_rH m_TH Rdot',real=True)
    DH=1-2*G*mrH
    res['implicit_outer_horizon_derivative'] = (Rdot-2*G*(mtH+mrH*Rdot)).subs(Rdot,2*G*mtH/DH)
    area=4*sp.pi*r*r
    res['horizon_area_derivative'] = sp.diff(area,r)*Rdot-8*sp.pi*r*Rdot
    result = audit(res)
    result['horizon_domain'] = 'zeta=1, D_H=1-2Gm_r>0; n,mu,D,sigma>0, |v|<1.'
    result['horizon_sign_certificate'] = 'm_TH>=0, Rdot>=0; D[(v-1)-Rdot/sigma]<0.'
    return result


def production_validator(configuration):
    """All eight mutations use the same action/conservation identities."""
    n,mu,r,sig,z = sp.symbols('n mu r sigma zeta',positive=True)
    v,c = sp.symbols('v c',real=True)
    rho,PF = sp.symbols('rho_C P_F',real=True)
    D,Dt,Dr,vr,zr,sr = sp.symbols('D D_T D_r v_r zeta_r sigma_r',real=True)
    B,Bt,Br,W,Wr = sp.symbols('B B_T B_r W W_r',real=True)
    Rdot,q,j = sp.symbols('Rdot q j_r',real=True)
    gamma2=1/(1-v*v)
    P=n*mu-rho
    expected = sp.Matrix([n*mu*gamma2-P,-n*mu*gamma2*v,n*mu*gamma2*v*v+P,P])
    candidate = configuration['TC_count']*expected
    candidate[1] *= configuration['momentum_sign']
    candidate += configuration['extra_PF']*sp.Matrix([0,0,PF,PF])
    residuals = {f'action_source_{i}':candidate[i]-expected[i] for i in range(4)}
    phase_gradient=sr*(W-z*B)+sig*(Wr-zr*B-z*Br)
    residuals['phase_action_integrability'] = (
        Bt+configuration['phase_flux_sign']*phase_gradient-(Bt+phase_gradient))
    current_exact=Dt+sr*D*(v-z)+sig*(Dr*(v-z)+D*(vr-zr))+2*sig*D*(v-z)/r
    current_candidate=current_exact+(configuration['radial_measure_power']-2)*sig*D*(v-z)/r
    residuals['densitized_action_current'] = current_candidate-current_exact
    for sign in (-1,1):
        physical=(v+sign*c)/(1+sign*v*c)
        candidate_speed = v+sign*c if configuration['newtonian_sound'] else physical
        residuals[f'acoustic_characteristic_{sign}'] = (
            (v-candidate_speed)**2-c*c*(1-v*candidate_speed)**2)
    expected_boundary=4*sp.pi*r*r*(sig*j-q*Rdot)
    candidate_boundary=4*sp.pi*r*r*(sig*j-configuration['moving_boundary']*q*Rdot)
    residuals['Leibniz_moving_charge_balance'] = candidate_boundary-expected_boundary
    return audit(residuals)


def mutations():
    baseline={'TC_count':1,'momentum_sign':1,'phase_flux_sign':1,
              'radial_measure_power':2,'newtonian_sound':False,'extra_PF':0,'moving_boundary':1}
    variations=(('omitted_collective_stress','TC_count',0),
                ('doubled_collective_stress','TC_count',2),
                ('reversed_collective_momentum','momentum_sign',-1),
                ('reversed_phase_flux','phase_flux_sign',-1),
                ('omitted_spherical_measure','radial_measure_power',0),
                ('Newtonian_sound_speeds','newtonian_sound',True),
                ('extra_foundation_Hilbert_pressure','extra_PF',1),
                ('omitted_moving_surface_term','moving_boundary',0))
    controls={}
    for name,key,value in variations:
        config=dict(baseline)
        config[key]=value
        validation=production_validator(config)
        controls[name]={'detected':not validation['all_exact'],
                        'failed_identities':[k for k,v in validation['checks'].items() if not v],
                        'residuals':{k:v for k,v in validation['residuals'].items() if v != '0'}}
    production=production_validator(baseline)
    return {'production':production,'controls':controls,
            'all_pass':production['all_exact'] and all(c['detected'] for c in controls.values())}


def ltb_regression(w, geom):
    t,a = sp.symbols('T a',real=True,positive=True)
    G,mu0 = sp.symbols('G mu0',positive=True)
    RR=sp.Function('R')(t,a)
    M=sp.Function('M')(a)
    Ra=sp.diff(RR,a)
    zz=sp.sqrt(2*G*M/RR)
    rho=sp.diff(M,a)/(4*sp.pi*RR**2*Ra)
    density=rho/mu0
    evolution={sp.diff(RR,t):-zz,sp.diff(RR,t,2):-G*M/RR**2,
               sp.diff(RR,t,a):-sp.diff(zz,a),
               sp.diff(RR,t,a,2):-sp.diff(zz,a,2),
               sp.diff(RR,t,2,a):sp.diff(-G*M/RR**2,a)}
    def shell_reduce(expr):
        return clean(expr.subs(evolution,simultaneous=True))
    def dr(expr):
        return sp.diff(expr,a)/Ra
    def dt(expr):
        return shell_reduce(sp.diff(expr,t)+zz*sp.diff(expr,a)/Ra)
    zr,zt=dr(zz),dt(zz)
    zrr,ztr,ztt=dr(zr),dt(zr),dt(zt)
    substitution={w.R:RR,w.SIGMA:1,w.ZETA:zz,
                  sp.diff(w.SIGMA,w.R):0,sp.diff(w.SIGMA,w.T):0,
                  sp.diff(w.SIGMA,w.R,2):0,sp.diff(w.SIGMA,w.T,w.R):0,
                  sp.diff(w.ZETA,w.R):zr,sp.diff(w.ZETA,w.T):zt,
                  sp.diff(w.ZETA,w.R,2):zrr,sp.diff(w.ZETA,w.T,w.R):ztr,
                  sp.diff(w.ZETA,w.T,2):ztt,w.GNEWTON:G}
    res={'LTB_PG_Einstein_00':geom['g00'].subs(substitution,simultaneous=True)-8*sp.pi*G*rho,
         'LTB_PG_Einstein_01':geom['g01'].subs(substitution,simultaneous=True),
         'LTB_PG_Einstein_11':geom['g11'].subs(substitution,simultaneous=True),
         'LTB_PG_Einstein_angular':geom['g22'].subs(substitution,simultaneous=True),
         'LTB_collective_current':dt(density)-dr(RR*RR*density*zz)/(RR*RR),
         'LTB_collective_phase':sp.diff(mu0,t)+sp.diff(mu0,a),
         'LTB_mass_radial':dr(M)-4*sp.pi*RR*RR*rho,
         'LTB_mass_temporal':dt(M)-4*sp.pi*RR*RR*zz*rho,
         'LTB_comoving_current':sp.diff(RR*RR*Ra*density,t)}
    # dR=-zeta dT+R_a da: pull back the comoving two-metric into (T,R).
    jacobian=sp.Matrix([[1,0],[zz/Ra,1/Ra]])
    transformed=jacobian.T*sp.diag(-1,Ra**2)*jacobian
    expected_pg=sp.Matrix([[-1+zz**2,zz],[zz,1]])
    for i in range(2):
        for j in range(2):
            res[f'LTB_comoving_to_PG_metric_{i}{j}']=transformed[i,j]-expected_pg[i,j]
    # Direct independent 4D comoving metric, not the W73 metric/projection formula.
    angle,az=sp.symbols('theta varphi',real=True)
    coords=(t,a,angle,az)
    metric=sp.diag(-1,Ra**2,RR**2,RR**2*sp.sin(angle)**2)
    inv=metric.inv()
    gamma=[[[clean(sum(inv[i,l]*(sp.diff(metric[l,k],coords[j])+sp.diff(metric[l,j],coords[k])
                               -sp.diff(metric[j,k],coords[l]))/2 for l in range(4)))
              for k in range(4)] for j in range(4)] for i in range(4)]
    ric=sp.zeros(4)
    for i in range(4):
        for j in range(i,4):
            value=sum(sp.diff(gamma[k][i][j],coords[k])-sp.diff(gamma[k][i][k],coords[j])
                      +sum(gamma[k][k][l]*gamma[l][i][j]-gamma[k][j][l]*gamma[l][i][k]
                           for l in range(4)) for k in range(4))
            ric[i,j]=clean(value)
            ric[j,i]=ric[i,j]
    scalar=clean(sum(inv[i,j]*ric[i,j] for i in range(4) for j in range(4)))
    einstein=ric-metric*scalar/2
    for i,j in ((0,0),(0,1),(1,1),(2,2),(3,3)):
        target=8*sp.pi*G*rho if (i,j)==(0,0) else 0
        res[f'LTB_independent_comoving_Einstein_{i}{j}']=shell_reduce(einstein[i,j]-target)
    # Explicit shell solution and future-outer implicit root identity.
    Mb,b=sp.symbols('M_b b',positive=True)
    Mlinear=Mb+b*a
    F=sp.symbols('F',positive=True)
    Rsol=(a**sp.Rational(3,2)-sp.Rational(3,2)*sp.sqrt(2*G*Mlinear)*t)**sp.Rational(2,3)
    # Real positive shell branch: verify R^(3/2) equation before fractional powers.
    X=a**sp.Rational(3,2)-sp.Rational(3,2)*sp.sqrt(2*G*Mlinear)*t
    res['LTB_explicit_shell_first_integral']=sp.diff(X,t)+sp.Rational(3,2)*sp.sqrt(2*G*Mlinear)
    res['LTB_initial_R']=Rsol.subs(t,0)-a
    aH=2*G*Mb/(1-2*G*b)
    res['LTB_initial_outer_root']= (a-2*G*Mlinear).subs(a,aH)
    res['LTB_initial_outer_denominator']=(1-2*G*sp.diff(Mlinear,a))-(1-2*G*b)
    adot=zz/(Ra-2*G*sp.diff(M,a))
    implicit_radius_dot=-zz+Ra*adot
    mass_dot=zz*sp.diff(M,a)/Ra
    res['LTB_implicit_horizon_vs_mass_balance']=implicit_radius_dot-2*G*mass_dot/(1-2*G*sp.diff(M,a)/Ra)
    for i in range(2):
        res[f'LTB_scalar_zero_equation_{i}']=w.matter_quantities()['gradients'][i].subs({w.PHI1:0,w.PHI2:0})
    exact=audit({key:shell_reduce(value) for key,value in res.items()})
    numerical=ltb_numerical()
    return {'exact':exact,'numerical':numerical,
            'all_pass':exact['all_exact'] and numerical['all_pass'],
            'physical_EOS_selected':False}


def ltb_numerical():
    G=mu0=1.0
    Mb,b=0.5,0.05
    times=(0.0,0.05,0.1)
    shells=(0.75,1.0,1.25,1.5,2.0)
    def state(t,a):
        M=Mb+b*a
        root=math.sqrt(2*G*M)
        X=a**1.5-1.5*root*t
        R=X**(2.0/3.0)
        Ra=(math.sqrt(a)-G*b*t/root)/math.sqrt(R)
        z=math.sqrt(2*G*M/R)
        n=b/(4*math.pi*mu0*R*R*Ra)
        mr=b/Ra
        mt=z*mr
        return dict(T=t,a=a,R=R,R_a=Ra,M=M,zeta=z,n=n,m_r=mr,m_T=mt,D_H=1-2*G*mr)
    states=[state(t,a) for t in times for a in shells]
    horizons=[]
    for t in times:
        def function(a):
            s=state(t,a)
            return s['R']-2*G*s['M']
        aH=brentq(function,0.75,2.0,xtol=1e-12,rtol=4*np.finfo(float).eps)
        s=state(t,aH)
        normalized=abs(function(aH))/max(s['R'],2*G*s['M'])
        adot=s['zeta']/(s['R_a']-2*G*b)
        implicit=-s['zeta']+s['R_a']*adot
        flux=2*G*s['m_T']/s['D_H']
        error=abs(implicit-flux)/max(abs(implicit),abs(flux))
        s.update(horizon_normalized_residual=normalized,radius_dot_implicit=implicit,
                 radius_dot_mass_flux=flux,radius_dot_relative_error=error,
                 area_dot=8*math.pi*s['R']*flux)
        horizons.append(s)
    finite=all(math.isfinite(float(value)) for row in states+horizons for value in row.values())
    positive=all(row['R']>0 and row['R_a']>0 and row['n']>0 for row in states)
    roots_ok=all(row['horizon_normalized_residual']<1e-10 and row['D_H']>0
                 and row['radius_dot_relative_error']<1e-9 for row in horizons)
    return {'inputs':{'G':G,'mu0':mu0,'M_b':Mb,'b':b,'times':times,'shells':shells},
            'states':states,'horizons':horizons,'finite':finite,'positive_states':positive,
            'root_xtol':1e-12,'horizon_residual_budget':1e-10,'derivative_relative_budget':1e-9,
            'all_pass':finite and positive and roots_ok and len(states)==15 and len(horizons)==3,
            'time_evolution_solver_used':False}


def zero_collective_regression(w, geom):
    matter=w.matter_quantities()
    production=w.production_evolution()
    t,r,sig,z,G=w.T,w.R,w.SIGMA,w.ZETA,w.GNEWTON
    res={
        'W73_lapse_constraint':production['sigma_r']+4*sp.pi*G*r*sig*matter['S']/z,
        'W73_shift_constraint':production['zeta_r']-4*sp.pi*G*r*(matter['rho']/z+matter['S'])+z/(2*r),
        'W73_shift_evolution':production['zeta_t']-(sig*z*sp.diff(z,r)-sp.diff(sig,r)
                              +sig*z*z/(2*r)+4*sp.pi*G*sig*r*matter['p_r']),
    }
    for index in range(2):
        res[f'W73_scalar_evolution_{index}']=production['pi_t'][index]-(
            sp.diff(sig*r*r*((w.RAD1,w.RAD2)[index]+z*(w.PI1,w.PI2)[index]),r)/(r*r)
            -sig*matter['gradients'][index])
    return audit(res)


def main():
    progress('W79: dependency pins and current/scalar action variation')
    prov=provenance()
    if not prov['all_pass']:
        print(json.dumps({'status':'FAIL_PROVENANCE','provenance':prov},allow_nan=False))
        return 1
    action=action_variation()
    progress('W79: recomputing full PG geometry and independent warped geometry')
    w,geom=load_geometry()
    geometry=warped_geometry(w,geom)
    progress('W79: covariant Ward identities, sound block and joint mass balances')
    ward=current_and_ward(w,geom)
    primitive=primitive_checks()
    balances=source_geometry_balances(w,geom)
    controls=mutations()
    zero=zero_collective_regression(w,geom)
    progress('W79: exact PG/comoving LTB regression and fixed 15-state/3-root crosscheck')
    ltb=ltb_regression(w,geom)
    groups={'action':action,'geometry':geometry,'current_and_source_conservation':ward,
            'primitive_characteristics':primitive,'source_geometry_balances':balances,
            'zero_collective_W73':zero}
    closure={key:value['all_exact'] for key,value in groups.items()}
    closure.update(dependency_pins=prov['all_pass'],mutations=controls['all_pass'],
                   exact_nonvacuum_regression=ltb['exact']['all_exact'],
                   numerical_nonvacuum_regression=ltb['numerical']['all_pass'])
    passed=all(closure.values())
    closure.update({name:False for name in FALSE_FLAGS})
    result={'claim_id':'W3_79_COLLECTIVE_CURRENT_BACKREACTION','model_version':VERSION,
            'status':'PASS_CONDITIONAL_EXACT_LOCAL_COUPLED_SYSTEM' if passed else 'FAIL_W79',
            'artifact_valid':passed,'provenance':prov,'closure_flags':closure,
            'exact_groups':groups,'mutation_controls':controls,'LTB_regression':ltb,
            'source_ledger':{'Einstein_operator':1,'ordinary_Hilbert_stress':1,
                            'collective_Hilbert_stress':1,'extra_P_F_stress':0,
                            'extra_passive_scale_stress':0,'extra_phase_current_stress':0},
            'scope':'Local supplied-EOS smooth annulus; no central endpoint or high-density EOS selection.',
            'output_files_written':[]}
    print(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
