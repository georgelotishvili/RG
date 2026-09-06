'''W3-78 frozen common-geometry/core response; finite JSON on stdout, no writes.'''
from __future__ import annotations

import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import math
import platform
import traceback
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp
from scipy.sparse import bmat, diags, eye
from scipy.sparse.linalg import ArpackNoConvergence, eigs, spsolve

HERE = Path(__file__).resolve().parent
WORK3 = HERE.parents[1]
CONTRACT = HERE / 'w3_78_core_frequency_response_contract.md'
CONTRACT_HASH = 'a1b575d97eb678f52a792cafb8ab5954206d961f8a4f2bd6351260394ad845a3'
DEPENDENCIES = {
    'Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_one_oscillon_coframe_localized_core_preregistration.md': 'ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db',
    'Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_one_oscillon_coframe_localized_core.py': 'b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57',
    'Strong_Field/W3-66_Physical_Radial_Mode/w3_66_physical_radial_mode_preregistration.md': '13f16dbb45299af763c3934a6a116b85f0f11085c2e7c5478af9249b41666245',
    'Strong_Field/W3-66_Physical_Radial_Mode/w3_66_physical_radial_mode.py': '381d8fec0e9188536bc75c37ef0159b51a06967612fb73a1463f3b65a5e49e06',
    'Cosmology_and_LSS/Active_Participation_Resonance_Feedback/w3_50_neutral_collective_phase_density_bridge_contract.md': 'c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635',
    'Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md': '6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879',
}
A6, OMEGA = .25, .8
FREQUENCIES = (.04, .08, .12, .16, .19, .24, .32, .48)


def native(value):
    if isinstance(value, dict):
        return {str(k): native(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [native(v) for v in value]
    if isinstance(value, np.ndarray):
        return native(value.tolist())
    if isinstance(value, (complex, np.complexfloating)):
        return {'real': float(value.real), 'imag': float(value.imag)}
    if isinstance(value, np.generic):
        return native(value.item())
    return value


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def progress(message):
    print(message, file=sys.stderr, flush=True)


def exact_gate():
    t, r, a, om, k, eps = sp.symbols('t r a om k eps', real=True, nonzero=True)
    f, s, eta, xi = sp.Function('f')(r), sp.Function('s')(r), sp.Function('eta')(t, r), sp.Function('xi')(t, r)
    F = r*f
    fp, fpp = sp.diff(f, r), sp.diff(f, r, 2)
    background = (1-om**2)*f-f**3+a*f**5-2*fp/r
    wp, wm = 1-om**2-3*f**2+5*a*f**4, 1-om**2-f**2+a*f**4
    U, V = sp.Function('U')(r), sp.Function('V')(r)
    lp = lambda z: -sp.diff(z, r, 2)+wp*z
    lm = lambda z: -sp.diff(z, r, 2)+wm*z
    ju, jv = r*(sp.diff(s, r)*fp-2*om**2*s*f), -om*k*s*F
    zero = lambda z: sp.simplify(sp.expand(z).subs(fpp, background)) == 0
    # Independent Euler variation of both real fields, before any probe substitution.
    q, b, N = sp.Function('q')(t, r), sp.Function('b')(t, r), sp.Function('N')(t, r)
    amp2 = q*q+b*b
    potential = amp2/2-amp2**2/4+a*amp2**3/6
    lag = r*r*((sp.diff(q,t)**2+sp.diff(b,t)**2)/(2*N)-N*((sp.diff(q,r)**2+sp.diff(b,r)**2)/2+potential))
    variations = []; euler_expressions=[]
    for field in (q,b):
        el = (sp.diff(sp.diff(lag,sp.diff(field,t)),t)+sp.diff(sp.diff(lag,sp.diff(field,r)),r)-sp.diff(lag,field))/(r*r*N)
        euler_expressions.append(el)
        expected = sp.diff(field,t,2)/N**2-sp.diff(N,t)*sp.diff(field,t)/N**3-sp.diff(field,r,2)-(2/r+sp.diff(N,r)/N)*sp.diff(field,r)+(1-amp2+a*amp2**2)*field
        variations.append(sp.simplify(el-expected) == 0)
    w = f+eps*(eta+sp.I*xi)
    modulus2 = (f+eps*eta)**2+eps**2*xi**2
    rotated = sp.diff(w,t,2)+2*sp.I*om*sp.diff(w,t)-om**2*w-sp.diff(w,r,2)-2*sp.diff(w,r)/r+(1-modulus2+a*modulus2**2)*w
    linear = sp.diff(rotated,eps).subs(eps,0)
    real_eq = sp.diff(eta,t,2)-2*om*sp.diff(xi,t)-sp.diff(eta,r,2)-2*sp.diff(eta,r)/r+wp*eta
    imag_eq = sp.diff(xi,t,2)+2*om*sp.diff(eta,t)-sp.diff(xi,r,2)-2*sp.diff(xi,r)/r+wm*xi
    replacements = {eta: U/r*sp.cos(k*t), xi: V/r*sp.sin(k*t)}
    phasor = sp.simplify((real_eq+sp.I*imag_eq).subs(replacements).doit()*r)
    pencil = ((lp(U)-k*k*U-2*om*k*V)*sp.cos(k*t)+sp.I*(lm(V)-k*k*V-2*om*k*U)*sp.sin(k*t))
    phi = s*sp.cos(k*t)
    vertex = -2*om**2*phi*f+sp.I*om*sp.diff(phi,t)*f+sp.diff(phi,r)*fp
    # Differentiate the actual action E-L under a lapse variation FIRST.
    # This derivative is linear in q, so its complex extension is exact.
    action_source=-sp.diff(euler_expressions[0].subs(N,1+eps*phi).doit(),eps).subs(eps,0)
    action_vertex=sp.simplify(action_source.subs(q,sp.exp(sp.I*om*t)*f).doit()/sp.exp(sp.I*om*t))
    # Obtain charge from the same action's phase Noether variation.
    noether=-b*sp.diff(lag,sp.diff(q,t))+q*sp.diff(lag,sp.diff(b,t))
    rotate_q=(f+eps*eta)*sp.cos(om*t)-eps*xi*sp.sin(om*t)
    rotate_b=(f+eps*eta)*sp.sin(om*t)+eps*xi*sp.cos(om*t)
    noether_lapse=noether.subs({q:rotate_q,b:rotate_b,N:1+eps*phi}).doit()
    charge_linear=sp.trigsimp(sp.expand(sp.diff(noether_lapse,eps).subs(eps,0)))
    charge_phasor=sp.simplify(charge_linear.subs(replacements).doit())
    charge_density = 2*om*F*U+k*F*V-om*s*F**2
    charge_derivative = sp.diff(V*sp.diff(F,r)-F*sp.diff(V,r),r)
    charge_derivative = charge_derivative.subs(sp.diff(V,r,2),(wm-k*k)*V-2*om*k*U-jv)
    # Independent real/imaginary Green-current identity with production signs.
    ur, ui, vr, vi, dur, dui, dvr, dvi, p, m, j1, j2 = sp.symbols('ur ui vr vi dur dui dvr dvi p m j1 j2',real=True)
    ddur=(p-k*k)*ur-2*om*k*vr-j1
    ddui=(p-k*k)*ui-2*om*k*vi
    ddvr=(m-k*k)*vr-2*om*k*ur-j2
    ddvi=(m-k*k)*vi-2*om*k*ui
    green = ur*ddui-ui*ddur+vr*ddvi-vi*ddvr-j1*ui-j2*vi
    zplus,zminus = sp.symbols('zplus zminus',real=True)
    exterior = sp.Matrix([[1-om**2-k*k,-2*om*k],[-2*om*k,1-om**2-k*k]])
    qout, absw = sp.symbols('qout absw',positive=True)
    fq = sp.pi*qout*absw**2
    energy = (om+k)*fq
    # Canonical lapse-work density from the action, integrated by parts once.
    vp=f-f**3+a*f**5
    work_density=r*r*s*((om**2*f+vp)*U/r+fp*sp.diff(U/r,r)+om*k*f*V/r-om**2*s*f*f)
    work_bulk=work_density-sp.diff(r*s*fp*U,r)
    # Physical plane-wave Noether and Hilbert fluxes, before the subtraction.
    wave_amplitude2=absw**2/(4*r*r)
    radial_log_derivative=-1/r-sp.I*qout
    current_density=-sp.im(radial_log_derivative*wave_amplitude2)
    energy_density=-sp.re((-sp.I*(om+k))*radial_log_derivative*wave_amplitude2)
    gauge_v=om*F/k
    checks = {
        'two_real_component_lapse_action_variations_exact': all(variations),
        'complex_and_real_linearization_exact': sp.simplify(linear-real_eq-sp.I*imag_eq)==0,
        'full_time_domain_to_reduced_pencil_exact': sp.simplify(phasor-pencil)==0,
        'lapse_vertex_time_and_gradient_exact': sp.simplify(r*vertex-ju*sp.cos(k*t)-sp.I*jv*sp.sin(k*t))==0,
        'vertex_from_actual_action_lapse_derivative_exact': sp.simplify(r*action_vertex-ju*sp.cos(k*t)-sp.I*jv*sp.sin(k*t))==0,
        'charge_from_actual_action_noether_variation_exact': sp.simplify(charge_phasor-charge_density*sp.cos(k*t))==0,
        'uniform_lapse_amplitude_equation_exact': zero(-2*om*k*gauge_v-ju.subs({s:1,sp.diff(s,r):0})),
        'uniform_lapse_phase_equation_exact': zero(lm(gauge_v)-k*k*gauge_v-jv.subs(s,1)),
        'phase_zero_mode_exact': zero(lm(F)),
        'local_noether_lapse_charge_identity_exact': zero(charge_derivative-k*charge_density),
        'uniform_lapse_charge_correction_exact': sp.simplify(k*F*gauge_v-om*F**2)==0,
        'green_volume_work_boundary_identity_exact': sp.expand(green)==0,
        'canonical_action_lapse_work_vertex_exact': zero(work_bulk+ju*U+jv*V+om**2*r*r*s*s*f*f),
        'outgoing_charge_from_noether_current_exact': sp.simplify(4*sp.pi*r*r*current_density-fq)==0,
        'outgoing_energy_from_hilbert_flux_exact': sp.simplify(4*sp.pi*r*r*energy_density-energy)==0,
        'upper_sideband_dispersion_exact': sp.simplify(exterior*sp.Matrix([1,1])-(1-(om+k)**2)*sp.Matrix([1,1]))==sp.zeros(2,1),
        'lower_sideband_dispersion_exact': sp.simplify(exterior*sp.Matrix([1,-1])-(1-(om-k)**2)*sp.Matrix([1,-1]))==sp.zeros(2,1),
        'physical_energy_minus_charge_exact': sp.simplify(energy-om*fq-sp.pi*k*qout*absw**2)==0,
        'probe_nonconstant_lapse_hessian': sp.diff(f*f,r,2)!=0,
    }
    # One validator compares production and every mutant to unchanged action
    # variations, Noether charge and a positively outgoing physical wave.
    signature={'mix_real':1,'mix_imag':1,'dynamic':1,'time_vertex':1,'gradient_vertex':1,'charge_lapse':1,'outgoing':1,'subtract_omega_charge':1}
    def validate(candidate):
        cp=((lp(U)-candidate['dynamic']*k*k*U-2*om*k*candidate['mix_real']*V)*sp.cos(k*t)
            +sp.I*(lm(V)-candidate['dynamic']*k*k*V-2*om*k*candidate['mix_imag']*U)*sp.sin(k*t))
        cj1=r*(candidate['gradient_vertex']*sp.diff(s,r)*fp-2*om**2*s*f)
        cj2=-candidate['time_vertex']*om*k*s*F
        cq=2*om*F*U+k*F*V-candidate['charge_lapse']*om*s*F**2
        radial=-1/r-sp.I*candidate['outgoing']*qout
        current=4*sp.pi*r*r*(-sp.im(radial*wave_amplitude2))
        full_energy=4*sp.pi*r*r*(-sp.re((-sp.I*(om+k))*radial*wave_amplitude2))
        residuals={
            'dynamic_equations':sp.simplify(cp-phasor),
            'action_lapse_vertex':sp.simplify(cj1*sp.cos(k*t)+sp.I*cj2*sp.sin(k*t)-r*action_vertex),
            'action_noether_charge':sp.simplify(cq*sp.cos(k*t)-charge_phasor),
            'positive_outgoing_current':sp.simplify(current-fq),
            'rotating_energy_accounting':sp.simplify(full_energy-candidate['subtract_omega_charge']*om*current-sp.pi*k*qout*absw**2),
        }
        return {name:bool(value==0) for name,value in residuals.items()}
    production=validate(signature)
    changes={
        'remove_gyroscopic_mixing':{'mix_real':0,'mix_imag':0},
        'reverse_one_mixing_sign':{'mix_imag':-1},
        'omit_lapse_time_derivative':{'time_vertex':0},
        'omit_spatial_gradient_vertex':{'gradient_vertex':0},
        'remove_lapse_charge_correction':{'charge_lapse':0},
        'reverse_outgoing_sign':{'outgoing':-1},
        'confuse_full_energy_and_work':{'subtract_omega_charge':0},
        'replace_dynamic_pencil_with_static_hessians':{'dynamic':0,'mix_real':0,'mix_imag':0},
    }
    details={name:validate(dict(signature,**change)) for name,change in changes.items()}
    mutations={name:not all(out.values()) for name,out in details.items()}
    return {'checks':checks,'production_signature_validation':production,'mutation_controls':mutations,'mutation_validation_residuals_zero':details,'pass':all(checks.values()) and all(production.values()) and all(mutations.values())}


def background_module():
    spec=importlib.util.spec_from_file_location('w3_58_read_only',HERE/'w3_58_one_oscillon_coframe_localized_core.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def coefficients(profile,x,kappa,uniform=False):
    f,fp=profile.sol(x)
    s=np.ones_like(x) if uniform else f*f/float(profile.sol(0)[0])**2
    ds=np.zeros_like(x) if uniform else 2*f*fp/float(profile.sol(0)[0])**2
    wp=1-OMEGA**2-3*f*f+5*A6*f**4
    wm=1-OMEGA**2-f*f+A6*f**4
    return wp,wm,x*(ds*fp-2*OMEGA**2*s*f),-OMEGA*kappa*x*s*f,s


def exterior(kappa):
    plus=1-(OMEGA+kappa)**2
    dp=-math.sqrt(plus) if plus>=0 else 1j*math.sqrt(-plus)
    dm=-math.sqrt(1-(OMEGA-kappa)**2)
    return complex(dp),complex(dm)


def forced(profile,kappa,radius,tolerance,uniform=False):
    x=np.linspace(0,radius,int(radius*20)+1)
    dp,dm=exterior(kappa)
    shift=np.zeros(2,dtype=complex)
    if uniform:
        f,fp=profile.sol(radius)
        v=OMEGA*radius*f/kappa
        vp=OMEGA*(f+radius*fp)/kappa
        shift=np.array([vp-dp*v,-vp+dm*v])
    def fun(xx,y):
        wp,wm,ju,jv,_=coefficients(profile,xx,kappa,uniform)
        return np.vstack((y[1],(wp-kappa*kappa)*y[0]-2*OMEGA*kappa*y[2]-ju,y[3],(wm-kappa*kappa)*y[2]-2*OMEGA*kappa*y[0]-jv))
    def jac(xx,y):
        wp,wm,_,_,_=coefficients(profile,xx,kappa,uniform)
        out=np.zeros((4,4,len(xx)),dtype=complex)
        out[0,1]=1;out[1,0]=wp-kappa*kappa;out[1,2]=-2*OMEGA*kappa
        out[2,3]=1;out[3,2]=wm-kappa*kappa;out[3,0]=-2*OMEGA*kappa
        return out
    def bc(ya,yb):
        return np.array([ya[0],ya[2],yb[1]+yb[3]-dp*(yb[0]+yb[2])-shift[0],yb[1]-yb[3]-dm*(yb[0]-yb[2])-shift[1]])
    # Exact real representation avoids complex Newton line-search stagnation.
    # Equations, retarded conditions and every frozen tolerance are unchanged.
    def unpack(y):
        return y[:4]+1j*y[4:]
    def real_fun(xx,y):
        out=fun(xx,unpack(y));return np.vstack((out.real,out.imag))
    def real_jac(xx,y):
        j=jac(xx,unpack(y));out=np.zeros((8,8,len(xx)))
        out[:4,:4]=j.real;out[:4,4:]=-j.imag
        out[4:,:4]=j.imag;out[4:,4:]=j.real
        return out
    def real_bc(ya,yb):
        out=bc(unpack(ya),unpack(yb));return np.concatenate((out.real,out.imag))
    left=np.zeros((4,4),dtype=complex);right=left.copy()
    left[0,0]=1;left[1,2]=1
    right[2]=[-dp,1,-dp,1];right[3]=[-dm,1,dm,-1]
    real_left=np.block([[left.real,-left.imag],[left.imag,left.real]])
    real_right=np.block([[right.real,-right.imag],[right.imag,right.real]])
    raw=solve_bvp(real_fun,real_bc,x,np.zeros((8,len(x))),tol=tolerance,max_nodes=50000,fun_jac=real_jac,bc_jac=lambda ya,yb:(real_left,real_right))
    return SimpleNamespace(sol=lambda xx:unpack(raw.sol(xx)),x=raw.x,y=unpack(raw.y),success=raw.success,message=raw.message,rms_residuals=raw.rms_residuals)


def response_error(profile,left,right,radius=30):
    x=np.linspace(0,radius,12001)
    yy=left(x)[[0,2]];zz=right(x)[[0,2]]
    weight=profile.sol(x)[0]**2
    den=simpson(weight*np.sum(np.abs(zz)**2,axis=0),x=x)
    return math.sqrt(float(simpson(weight*np.sum(np.abs(yy-zz)**2,axis=0),x=x)/max(den,1e-300)))


def readout(profile,solution,kappa,radius,uniform=False,include_response=False):
    x=np.linspace(0,radius,int(radius*400)+1)
    y=solution.sol(x);f,fp=profile.sol(x)
    _,_,ju,jv,s=coefficients(profile,x,kappa,uniform)
    qterms=np.vstack((2*OMEGA*x*f*y[0],kappa*x*f*y[2],-OMEGA*x*x*s*f*f))
    qintegral=simpson(qterms.sum(axis=0),x=x)
    qscale=float(simpson(np.abs(qterms).sum(axis=0),x=x))
    qerror=abs(qintegral)/max(qscale,1e-300)
    qboundary=(y[2,-1]*(f[-1]+radius*fp[-1])-radius*f[-1]*y[3,-1])/kappa
    work=2*math.pi*kappa*float(np.imag(simpson(ju*y[0]+jv*y[2],x=x)))
    boundary=2*math.pi*kappa*float(np.imag(np.conj(y[0,-1])*y[1,-1]+np.conj(y[2,-1])*y[3,-1]))
    wp=y[0,-1]+y[2,-1];wm=y[0,-1]-y[2,-1]
    opened=kappa>.2
    qwave=math.sqrt((OMEGA+kappa)**2-1) if opened else 0.
    fq=math.pi*qwave*abs(wp)**2
    fe=(OMEGA+kappa)*fq
    pout=kappa*fq
    scale=max(abs(work),abs(boundary),abs(pout),1e-300)
    fluxerror=max(abs(work-boundary),abs(boundary-pout),abs(pout-(fe-OMEGA*fq)))/scale if opened else 0.
    norm=float(simpson(f*f*(abs(y[0])**2+abs(y[2])**2),x=x))
    closed_scale=max(1.,2*math.pi*kappa*float(simpson(abs(ju*y[0])+abs(jv*y[2]),x=x)))
    closed_error=max(abs(work),abs(boundary))/closed_scale
    amp=simpson(x*f*y[0],x=x)/simpson(x*x*f*f,x=x)
    res=float(np.max(solution.rms_residuals))
    record={'kappa':kappa,'radius':radius,'success':solution.success,'message':solution.message,'collocation_nodes':solution.x.size,'max_collocation_residual':res,'A':amp,'profile_weighted_response_norm':norm,'upper_channel':'OPEN_OUTGOING' if opened else 'CLOSED_DECAYING','lower_channel':'CLOSED_DECAYING','w_plus_endpoint':wp,'w_minus_endpoint':wm,'charge_integral':qintegral,'charge_normalization':qscale,'normalized_charge_error':qerror,'finite_boundary_charge_integral':qboundary,'charge_green_identity_error':abs(qintegral-qboundary)/max(qscale,1e-300),'P_in':work,'P_boundary':boundary,'P_out':pout,'F_q':fq,'F_E':fe,'open_channel_relative_flux_error':fluxerror,'closed_channel_roundoff_error':closed_error,'pass':bool(solution.success and res<2e-6 and qerror<2e-5 and (fluxerror<2e-4 if opened else closed_error<1e-12))}
    if include_response:
        record['full_reduced_response_on_collocation_nodes']={'r':solution.x,'U':solution.y[0],'U_prime':solution.y[1],'V':solution.y[2],'V_prime':solution.y[3]}
    return record


def finite_difference(profile,kappa,h):
    radius=40.;n=int(round(radius/h));x=np.linspace(0,radius,n+1);size=n+1
    wp,wm,ju,jv,_=coefficients(profile,x,kappa)
    d=diags((-np.ones(size-1)/h**2,np.full(size,2/h**2),-np.ones(size-1)/h**2),(-1,0,1),format='csc')
    lp=d+diags(wp-kappa*kappa);lm=d+diags(wm-kappa*kappa)
    mix=-2*OMEGA*kappa*eye(size,format='csc')
    matrix=bmat([[lp,mix],[mix,lm]],format='lil',dtype=complex)
    rhs=np.concatenate((ju,jv)).astype(complex)
    for row in (0,size):
        matrix.rows[row]=[row];matrix.data[row]=[1.];rhs[row]=0
    dp,dm=exterior(kappa)
    for row,dout,sign in ((n,dp,1),(size+n,dm,-1)):
        cols=[n-2,n-1,n,size+n-2,size+n-1,size+n]
        vals=[1/(2*h),-2/h,3/(2*h)-dout,sign/(2*h),-sign*2/h,sign*(3/(2*h)-dout)]
        matrix.rows[row]=cols;matrix.data[row]=vals;rhs[row]=0
    matrix=matrix.tocsc();z=spsolve(matrix,rhs)
    algebra=float(np.linalg.norm(matrix@z-rhs)/max(np.linalg.norm(rhs),1e-300))
    def evaluate(xx):
        u=np.interp(xx,x,z[:size]);v=np.interp(xx,x,z[size:])
        return np.vstack((u,np.zeros_like(u),v,np.zeros_like(v)))
    return evaluate,{'spacing':h,'nodes':size,'linear_system_relative_residual':algebra}


def pencil(profile,h,shifts=(.05,.10,.15)):
    radius=40.;n=int(round(radius/h));x=np.linspace(h,radius-h,n-1);size=x.size
    f=profile.sol(x)[0]
    off=-np.ones(size-1)/h**2
    base=np.full(size,2/h**2+1-OMEGA**2)
    lp=diags((off,base-3*f*f+5*A6*f**4,off),(-1,0,1),format='csc')
    lm=diags((off,base-f*f+A6*f**4,off),(-1,0,1),format='csc')
    L=bmat([[lp,None],[None,lm]],format='csc')
    C=bmat([[None,2*OMEGA*eye(size)],[2*OMEGA*eye(size),None]],format='csc')
    matrix=bmat([[None,eye(2*size)],[L,-C]],format='csc')
    records=[];candidates=[]
    for shift in shifts:
        try:
            vals,vecs=eigs(matrix,k=16,sigma=shift,which='LM',tol=1e-9,maxiter=5000,v0=np.linspace(1.,2.,matrix.shape[0]))
            success=True;error=None
        except ArpackNoConvergence as exc:
            vals,vecs=exc.eigenvalues,exc.eigenvectors;success=False;error=str(exc)
        classified=[]
        for val in vals:
            if abs(val.imag)>=1e-7:
                role='COMPLEX_PENCIL_CANDIDATE_NOT_CLASSIFIED_PHYSICAL'
            elif abs(val.real)<.01:
                role='NEAR_ZERO_PHASE_FAMILY_ARTIFACT_CANDIDATE_EXCLUDED'
            elif abs(val.real)>=.2:
                role='FINITE_BOX_OPEN_CHANNEL_LEVEL_NOT_BOUND_MODE'
            elif .01<=val.real<=.195:
                role='ELIGIBLE_POSITIVE_BOUND_CANDIDATE'
            else:
                role='NEGATIVE_PARTNER_OR_OUTSIDE_FROZEN_SEARCH'
            classified.append({'eigenvalue':val,'classification':role})
        records.append({'shift':shift,'success':success,'error':error,'eigenvalues':vals,'classified_candidates':classified})
        for j,val in enumerate(vals):
            if abs(val.imag)<1e-7 and .01<=val.real<=.195:
                z=vecs[:2*size,j]
                z=z*np.exp(-1j*np.angle(z[np.argmax(abs(z))]))
                if not any(abs(val.real-old['kappa'])<5e-5 for old in candidates):
                    candidates.append({'kappa':float(val.real),'x':x,'u':np.real(z[:size]),'v':np.real(z[size:])})
    candidates.sort(key=lambda row:row['kappa'])
    return candidates,{'spacing':h,'radius':radius,'shift_results':records,'eligible_positive_real_candidates':[c['kappa'] for c in candidates],'all_arpack_solves_succeeded':all(r['success'] for r in records)}


def bound_mode(profile,candidate,radius):
    x=np.linspace(0,radius,int(radius*30)+1)
    xx=np.concatenate(([0.],candidate['x'],[40.]))
    us=np.concatenate(([0.],candidate['u'],[0.]));vs=np.concatenate(([0.],candidate['v'],[0.]))
    u=np.interp(x,xx,us,left=0,right=0);v=np.interp(x,xx,vs,left=0,right=0)
    norm=math.sqrt(float(simpson(u*u+v*v,x=x)));u/=norm;v/=norm
    guess=np.vstack((u,np.gradient(u,x),v,np.gradient(v,x),cumulative_trapezoid(u*u+v*v,x,initial=0)))
    def k_of(z):
        return .2/(1+np.exp(-np.clip(z,-30,30)))
    def fun(xx,y,p):
        k=float(k_of(p[0]));wp,wm,_,_,_=coefficients(profile,xx,k)
        return np.vstack((y[1],(wp-k*k)*y[0]-2*OMEGA*k*y[2],y[3],(wm-k*k)*y[2]-2*OMEGA*k*y[0],y[0]**2+y[2]**2))
    def bc(ya,yb,p):
        k=float(k_of(p[0]));dp,dm=exterior(k)
        return np.array([ya[0],ya[2],ya[4],yb[1]+yb[3]-dp.real*(yb[0]+yb[2]),yb[1]-yb[3]-dm.real*(yb[0]-yb[2]),yb[4]-1])
    k0=candidate['kappa'];par=np.array([math.log(k0/(.2-k0))])
    sol=solve_bvp(fun,bc,x,guess,p=par,tol=1e-7,max_nodes=50000)
    k=float(k_of(sol.p[0]));qx=np.linspace(0,radius,int(radius*400)+1);yy=sol.sol(qx);f=profile.sol(qx)[0]
    terms=np.vstack((2*OMEGA*qx*f*yy[0],k*qx*f*yy[2]));den=float(simpson(abs(terms).sum(axis=0),x=qx))
    charge=float(abs(simpson(terms.sum(axis=0),x=qx))/max(den,1e-300))
    residual=float(np.max(sol.rms_residuals))
    rec={'radius':radius,'initial_candidate':k0,'kappa':k,'success':sol.success,'message':sol.message,'max_collocation_residual':residual,'normalized_charge_error':charge,'normalization':float(simpson(yy[0]**2+yy[2]**2,x=qx)),'within_frozen_search':.01<=k<=.195,'pass':bool(sol.success and residual<2e-6 and charge<2e-5 and .01<=k<=.195)}
    return sol,rec


def bound_search(profile):
    candidates,coarse=pencil(profile,.04)
    progress('W78 bounded pencil candidates: '+str([c['kappa'] for c in candidates]))
    result={'search_interval':[.01,.195],'coarse_pencil':coarse,'candidates':[],'spectral_completeness_claimed':False}
    if not candidates:
        result['outcome']='NO_ELIGIBLE_CANDIDATE_IN_FROZEN_PENCIL_PROBES' if coarse['all_arpack_solves_succeeded'] else 'INCONCLUSIVE_PENCIL_SOLVE'
        result['accepted_pole_found']=False
        return result
    refined=[]
    for h in (.02,.01):
        cc,rr=pencil(profile,h);refined.append((cc,rr))
    result['refined_pencils']=[rr for _,rr in refined]
    for candidate in candidates:
        record={'coarse_kappa':candidate['kappa'],'physical_BVPs':[]}
        for radius in (30.,40.,50.):
            _,rr=bound_mode(profile,candidate,radius);record['physical_BVPs'].append(rr)
        reference=record['physical_BVPs'][1]['kappa']
        variation=max(abs(r['kappa']-reference)/max(abs(reference),1e-300) for r in record['physical_BVPs'])
        errors=[]
        for cc,rr in refined:
            errors.append(min((abs(c['kappa']-reference)/max(abs(reference),1e-300) for c in cc),default=None))
        accepted=all(r['pass'] for r in record['physical_BVPs']) and variation<2e-4 and errors[-1] is not None and errors[-1]<3e-3
        record.update({'relative_domain_frequency_variation':variation,'refined_pencil_relative_frequency_errors':errors,'accepted':accepted,'outcome':'ACCEPTED_NUMERICAL_BOUND_POLE' if accepted else 'INCONCLUSIVE_OR_REJECTED_CANDIDATE_NOT_ABSENCE'})
        result['candidates'].append(record)
    result['accepted_pole_found']=any(r['accepted'] for r in result['candidates'])
    result['outcome']='ACCEPTED_POLE_WITH_SCOPED_SEARCH' if result['accepted_pole_found'] else 'INCONCLUSIVE_BOUND_CANDIDATES'
    return result


def run():
    provenance={'contract_sha256':sha(CONTRACT),'source_sha256':sha(Path(__file__)),'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,'dependencies':{name:{'expected':digest,'actual':sha(WORK3/name)} for name,digest in DEPENDENCIES.items()},'runtime_file_writes':False}
    pins=provenance['contract_sha256']==CONTRACT_HASH and all(row['expected']==row['actual'] for row in provenance['dependencies'].values())
    result={'claim_id':'W3_78_CORE_COMMON_GEOMETRY_FREQUENCY_RESPONSE','model_version':'W3-78-v1.0','provenance':provenance,'dependency_pins_pass':pins,'units':{'amplitudes':'per epsilon','powers':'per epsilon squared','q':'lambda Q, full angular factor 4 pi','Ehat':'lambda E_physical/m','frequency':'kappa in proper mass units, not particle mass'},'profile_weighted_norm_definition':'integral f^2 (|U|^2+|V|^2) dr; common comparison interval [0,30]','collocation_representation':'eight real components exactly representing the four complex equations','implementation_history':'Initial direct-complex Newton implementation failed outgoing samples 0.32 and 0.48; the equivalent real split replaces that numerical representation, without changing any frozen physical input or acceptance budget.'}
    if not pins:
        result['status']='FAIL_DEPENDENCY_PINS';return result
    exact=exact_gate();result['exact_gate']=exact
    if not exact['pass']:
        result['status']='FAIL_EXACT_GATE_BEFORE_NUMERICS';return result
    progress('W78 exact and mutation controls passed; recomputing backgrounds.')
    mod=background_module()
    low=mod.solve_profile(OMEGA,radius=80,tolerance=1e-7)
    high=mod.solve_profile(OMEGA,radius=80,tolerance=3e-8)
    result['backgrounds']=[{'tolerance':tol,'radius':80,'success':p.success,'max_collocation_residual':float(np.max(p.rms_residuals)),'central_f':float(p.sol(0)[0])} for tol,p in ((1e-7,low),(3e-8,high))]
    if not all(row['success'] for row in result['backgrounds']):
        result['status']='NUMERICALLY_INCONCLUSIVE_BACKGROUND';return result
    rows=[]
    for kappa in FREQUENCIES:
        progress('W78 forced frequency '+str(kappa))
        solutions=[];records=[]
        for radius in (30.,40.,50.):
            sol=forced(low,kappa,radius,1e-7);solutions.append(sol)
            records.append(readout(low,sol,kappa,radius))
        fine=forced(high,kappa,40.,3e-8)
        reference=readout(high,fine,kappa,40.,include_response=True)
        variations=[response_error(high,sol.sol,fine.sol) for sol in solutions]
        fd=[]
        for h in (.02,.01,.005):
            evaluate,record=finite_difference(high,kappa,h)
            record['profile_weighted_relative_response_error']=response_error(high,evaluate,fine.sol)
            fd.append(record)
        passed=all(r['pass'] for r in records) and reference['pass'] and max(variations)<2e-4 and fd[-1]['profile_weighted_relative_response_error']<3e-3
        row={'kappa':kappa,'domain_runs':records,'fine_reference':reference,'profile_weighted_domain_and_tolerance_variations':variations,'finite_difference_crosschecks':fd,'pass':passed}
        rows.append(row)
        progress('W78 sample '+str(kappa)+' A='+str(reference['A'])+' fluxerr='+str(reference['open_channel_relative_flux_error'])+' chargeerr='+str(reference['normalized_charge_error'])+' FD='+str(fd[-1]['profile_weighted_relative_response_error'])+' pass='+str(passed))
    result['responses']=rows
    gauge=forced(high,.12,40.,3e-8,uniform=True)
    def target(x):
        f,fp=high.sol(x)
        return np.vstack((np.zeros_like(x),np.zeros_like(x),OMEGA*x*f/.12,OMEGA*(f+x*fp)/.12))
    gauge_error=response_error(high,gauge.sol,target)
    gauge_record=readout(high,gauge,.12,40.,uniform=True)
    result['uniform_lapse_gauge']={'response':gauge_record,'relative_profile_error':gauge_error,'inhomogeneous_tail_boundary_used':True,'pass':bool(gauge.success and float(np.max(gauge.rms_residuals))<2e-6 and gauge_error<2e-5 and gauge_record['normalized_charge_error']<2e-5)}
    response_pass=all(row['pass'] for row in rows) and result['uniform_lapse_gauge']['pass']
    result['forced_response_pass']=response_pass
    result['bound_search']=bound_search(high)
    result['closure_flags']={'exact_dynamic_operator_and_metric_vertex':exact['pass'],'uniform_lapse_gauge_control':result['uniform_lapse_gauge']['pass'],'numerical_forced_response':response_pass,'radiative_channel_energy_charge_balance':all(row['fine_reference']['pass'] for row in rows if row['kappa']>.2),'accepted_numerical_bound_pole':result['bound_search']['accepted_pole_found'],'Full_collective_mode_selection':False,'theta_C_probe_source_derived':False,'particle_mass_spectrum_derived':False,'Koide_derived':False,'nonlinear_core_quantized':False,'alpha_derived':False,'observational_pass':False,'intuitive_files_changed':False}
    result['status']='PASS_CONDITIONAL_ACTION_DERIVED_CORE_FREQUENCY_RESPONSE__BOUNDED_SPECTRAL_OUTCOME_SEPARATE' if response_pass else 'FAIL_REGISTERED_FORCED_RESPONSE_NUMERICAL_BUDGET'
    return result


if __name__=='__main__':
    try:
        output=run()
    except Exception as exc:
        output={'claim_id':'W3_78_CORE_COMMON_GEOMETRY_FREQUENCY_RESPONSE','status':'NUMERICALLY_INCONCLUSIVE_OR_IMPLEMENTATION_ERROR','exception_type':type(exc).__name__,'error':str(exc),'traceback':traceback.format_exc(),'runtime_file_writes':False}
    print(json.dumps(native(output),ensure_ascii=False,sort_keys=True,allow_nan=False))
