"""W3-84: one NEW finite rotor/link hypothesis; finite JSON stdout, no writes."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from scipy.optimize import brentq

HERE = Path(__file__).resolve()
ROOT = HERE.parents[4]
CONTRACT_SHA = 'ff1b94280a533e6aba4109465de7afcd2b5c7019c5292cb78c1040982c47d1dd'
PINS = {
    'CODES.md':'27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41',
    'RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/w3_50_neutral_collective_phase_density_bridge_contract.md':'c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635',
    'RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/w3_76_same_field_resonant_exchange_contract.md':'e10781a73470220065c664196efe0c361dbfb1c6c2404864e895d6ad2380bd02',
}
C = I = B = K0 = D0 = KAPPA = NBAR = 1
N = 48
EPSILON = 1e-3
TIMES = np.arange(801,dtype=float)/5


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coupling(q, exp=np.exp):
    x = KAPPA*D0*exp(q)
    K = K0*exp(-q-KAPPA*D0*(exp(q)-1))
    return K, -(1+x)*K, (1+x+x*x)*K


def bond_forces(q, delta, current_sign=1, backreaction=1, exp=np.exp, sin=np.sin, cos=np.cos):
    K,Kp,_ = coupling(q,exp)
    return current_sign*K*sin(delta), -B*q-backreaction*Kp*(1-cos(delta))


def stiffness(q,delta,mixed=1,exp=np.exp,sin=np.sin,cos=np.cos):
    K,Kp,Kpp = coupling(q,exp)
    return K*cos(delta),mixed*Kp*sin(delta),B+Kpp*(1-cos(delta))


def speed_squared(q,delta,include_length=True,exp=np.exp,sin=np.sin,cos=np.cos):
    A,b,D = stiffness(q,delta,exp=exp,sin=sin,cos=cos)
    label = (A-b*b/D)/C
    return label*(D0*exp(q))**2 if include_length else label


def forces(position,current_sign=1,backreaction=1):
    theta,q = position
    delta = np.roll(theta,-1)-theta
    current,link = bond_forces(q,delta,current_sign,backreaction)
    return np.array([current-np.roll(current,1),link])


def velocities(momentum):
    return np.array([(momentum[0]-NBAR)/C,momentum[1]/I])


def energy_terms(position,momentum):
    theta,q = position
    K,_,_ = coupling(q)
    delta = np.roll(theta,-1)-theta
    return np.array([(momentum[0]-NBAR)**2/(2*C),momentum[1]**2/(2*I),
                     B*q*q/2,K*(1-np.cos(delta))])


def energy(position,momentum):
    return math.fsum(energy_terms(position,momentum).ravel())


def exact_checks():
    q,delta = sp.symbols('q delta',real=True)
    K,Kp,Kpp = coupling(q,sp.exp)
    V = B*q*q/2+K*(1-sp.cos(delta))
    hessian = sp.hessian(V,(delta,q))
    dK = sp.diff(K,q)
    identities = {'K_prime':sp.simplify(Kp-dK),
                  'K_second':sp.simplify(Kpp-sp.diff(K,q,2))}
    # Off-shell local continuity uses two actual adjacent link energies and forces.
    qm,qp,dm,dp,pm,pp,vl,vc,vr = sp.symbols('qm qp dm dp pm pp vl vc vr',real=True)

    def validate(current_sign=1,backreaction=1,mixed=1,include_length=True):
        J,Fq = bond_forces(q,delta,current_sign,backreaction,sp.exp,sp.sin,sp.cos)
        A,b,D = stiffness(q,delta,mixed,sp.exp,sp.sin,sp.cos)
        rows = {'phase_force':sp.simplify(J-sp.diff(V,delta)),
                'link_force':sp.simplify(Fq+sp.diff(V,q)),
                'mixed_hessian':sp.simplify(b-hessian[0,1]),
                'phase_hessian':sp.simplify(A-hessian[0,0]),
                'link_hessian':sp.simplify(D-hessian[1,1])}
        # A physical wave number k_phys means label k=d*k_phys.
        kp = sp.symbols('k_phys',real=True)
        omega_low = (hessian[0,0]-hessian[0,1]**2/hessian[1,1])*(D0*sp.exp(q)*kp)**2/C
        physical_target = sp.diff(omega_low,kp,2)/2
        candidate_speed = speed_squared(q,delta,include_length,sp.exp,sp.sin,sp.cos)
        rows['physical_length_readout'] = sp.simplify(candidate_speed-physical_target)
        currents,link_rates = [],[]
        for dilation,angle,P,deltadot in ((qm,dm,pm,vc-vl),(qp,dp,pp,vr-vc)):
            vb = V.subs({q:dilation,delta:angle})
            jj,ff = bond_forces(dilation,angle,current_sign,backreaction,sp.exp,sp.sin,sp.cos)
            # d(P^2/2I+V)/dt, including the actual reciprocal link force.
            link_rates.append(sp.diff(vb,dilation)*P/I+P*ff/I+sp.diff(vb,angle)*deltadot)
            currents.append(jj)
        jl,jr = currents
        ndot = jr-jl
        flux_left,flux_right = -jl*(vl+vc)/2,-jr*(vc+vr)/2
        rows['local_energy_continuity'] = sp.simplify(vc*ndot+sum(link_rates)/2+flux_right-flux_left)
        rows['local_charge_continuity'] = sp.simplify(ndot-jr+jl)
        return {'accepted':all(v==0 for v in rows.values()),'residuals':{k:str(v) for k,v in rows.items()}}

    baseline = validate()
    controls = {name:validate(**kwargs) for name,kwargs in (
        ('reverse_phase_current',{'current_sign':-1}),
        ('omit_link_backreaction',{'backreaction':0}),
        ('omit_mixed_hessian',{'mixed':0}),
        ('omit_physical_bond_length',{'include_length':False}))}
    # The local identities telescope on the periodic graph, giving both global laws.
    j0,j1,j2 = sp.symbols('j0 j1 j2')
    identities['periodic_divergence_sum'] = sp.expand((j1-j0)+(j2-j1)+(j0-j2))
    gap = sp.exp(q)-1-q
    identities['slowing_gap_value_zero'] = gap.subs(q,0)
    identities['slowing_gap_slope_zero'] = sp.diff(gap,q).subs(q,0)
    identities['slowing_gap_second_derivative'] = sp.diff(gap,q,2)-sp.exp(q)
    positive = {'K':bool(K.is_positive),'K_second':bool(Kpp.is_positive),
                'slowing_gap_second_derivative':bool(sp.exp(q).is_positive)}
    return {'passed':all(v==0 for v in identities.values()) and all(positive.values()) and baseline['accepted'] and all(not x['accepted'] for x in controls.values()),
            'identities':{k:str(v) for k,v in identities.items()},'positive_certificates':positive,
            'baseline':baseline,'mutations':controls,
            'energy_certificate':'Every summand is nonnegative: kinetic squares, Bq^2/2, and K(1-cos Delta). Thus |q_i|<=sqrt(2H/B).',
            'ground_state':'n=nbar, P=q=0, all theta equal modulo 2pi; global phase is the sole zero mode.',
            'slowing_certificate':'exp(q)-1-q has value and slope zero at 0 and positive second derivative. On the stable admitted q>=0 branch, c_long^2<=d^2 K cos Q/C<=d0^2 K0/C.'}


def bloch(q,Q,k):
    A,b,D = stiffness(q,Q)
    z = np.exp(1j*k)-1
    return np.array([[A*abs(z)**2/C,b*np.conj(z)/np.sqrt(C*I)],
                     [b*z/np.sqrt(C*I),D/I]],dtype=complex)


def equilibrium(Q):
    q0 = 0. if Q==0 else brentq(lambda q:-bond_forces(q,Q)[1],0.,4.,xtol=1e-14,rtol=1e-14)
    pos = np.array([Q*np.arange(N),np.full(N,q0)])
    mom = np.array([np.full(N,NBAR,dtype=float),np.zeros(N)])
    A,b,D = stiffness(q0,Q)
    schur = A-b*b/D
    stable = bool(D>0 and schur>0)
    incidence = np.zeros((N,N))
    incidence[np.arange(N),np.arange(N)] = -1
    incidence[np.arange(N),(np.arange(N)+1)%N] = 1
    analytic = np.block([[A*incidence.T@incidence,b*incidence.T],[b*incidence,D*np.eye(N)]])
    invmass = 1/np.sqrt(np.r_[np.full(N,C),np.full(N,I)])
    weighted = invmass[:,None]*analytic*invmass[None,:]
    blocks = [np.linalg.eigvalsh(bloch(q0,Q,2*np.pi*j/N)) for j in range(N)]
    union = np.sort(np.concatenate(blocks))
    # Remove only j=0's exact phase eigenvalue, never a low/negative physical mode.
    physical_eigenvalues = np.r_[blocks[0][1],np.concatenate(blocks[1:])]
    fd_records = []
    for step in (1e-5,5e-6):
        fd = np.empty((2*N,2*N))
        for j in range(2*N):
            plus,minus = pos.copy(),pos.copy()
            plus.flat[j] += step
            minus.flat[j] -= step
            fd[:,j] = -(forces(plus)-forces(minus)).ravel()/(2*step)
        entry_error = float(np.max(np.abs(fd-analytic))/max(1.,np.max(np.abs(analytic))))
        wfd = invmass[:,None]*fd*invmass[None,:]
        spectrum = np.linalg.eigvalsh((wfd+wfd.T)/2)
        spectrum_error = float(np.max(np.abs(spectrum-union))/max(1.,np.max(np.abs(union))))
        fd_records.append({'step':step,'raw_entry_relative_error':entry_error,
                           'raw_asymmetry_max':float(np.max(np.abs(fd-fd.T))),
                           'spectrum_relative_error':spectrum_error,
                           'passed':entry_error<1e-8 and spectrum_error<1e-7})
    residual = float(np.max(np.abs(forces(pos))))
    direct_spectrum_error = float(np.max(np.abs(np.linalg.eigvalsh(weighted)-union)))
    c2 = float(speed_squared(q0,Q))
    return {'Q':Q,'winding':int(round(Q*N/(2*np.pi))),'q0':q0,'bond_length':float(D0*np.exp(q0)),
            'K':float(coupling(q0)[0]),'A':float(A),'b':float(b),'D':float(D),'mixed_stiffness':float(schur),
            'stable':stable,'classification':'stable modulo global phase' if stable else 'mixed phase-link instability',
            'label_long_speed':float(np.sqrt(schur/C)) if stable else None,
            'physical_long_speed':float(np.sqrt(c2)) if stable else None,
            'physical_long_speed_squared':c2,'equilibrium_force_residual':residual,
            'minimum_physical_eigenvalue':float(np.min(physical_eigenvalues)),
            'negative_physical_mode_count':int(np.sum(physical_eigenvalues<0)),
            'spectrum':union.tolist(),'fd_jacobian_checks':fd_records,
            'real_space_bloch_eigenvalue_error':direct_spectrum_error,
            'passed':residual<1e-12 and all(v['passed'] for v in fd_records) and direct_spectrum_error<1e-7}


def evolve(primary,dt):
    print('W84 Verlet dt=%.3g: starting' % dt,file=sys.stderr,flush=True)
    Q,q0 = primary['Q'],primary['q0']
    k = 2*np.pi/N
    w2 = float(np.linalg.eigvalsh(bloch(q0,Q,k))[0])
    omega = np.sqrt(w2)
    ratio = -primary['b']*(np.exp(1j*k)-1)/(primary['D']-I*w2)
    carrier = np.exp(1j*k*np.arange(N))
    background = np.array([Q*np.arange(N),np.full(N,q0)])
    background_mom = np.array([np.full(N,NBAR,dtype=float),np.zeros(N)])
    position = background+EPSILON*np.array([carrier.real,(ratio*carrier).real])
    momentum = background_mom+EPSILON*np.array([C*(-1j*omega*carrier).real,I*(-1j*omega*ratio*carrier).real])
    initial_energy = energy(position,momentum)
    background_energy = energy(background,background_mom)
    perturbation_energy = initial_energy-background_energy
    initial_charge = float(np.sum(momentum[0]))
    if perturbation_energy<=0:
        raise RuntimeError('Initial perturbation energy is not positive')
    states = np.empty((len(TIMES),4,N))
    energies,charges,coefficients = [],[],[]
    max_energy_drift,max_charge_drift,min_n,min_d,min_stiff = 0.,0.,1e100,1e100,1e100
    max_q_bound_ratio = 0.

    def health_and_conservation():
        nonlocal max_energy_drift,max_charge_drift,min_n,min_d,min_stiff,max_q_bound_ratio
        if not np.isfinite(position).all() or not np.isfinite(momentum).all():
            raise RuntimeError('Nonfinite canonical trajectory')
        hh = energy(position,momentum)
        qq = float(np.sum(momentum[0]))
        delta = np.roll(position[0],-1)-position[0]
        aa,bb,dd = stiffness(position[1],delta)
        lengths = D0*np.exp(position[1])
        max_energy_drift = max(max_energy_drift,abs(hh-initial_energy))
        max_charge_drift = max(max_charge_drift,abs(qq-initial_charge))
        min_n = min(min_n,float(momentum[0].min()))
        min_d = min(min_d,float(lengths.min()))
        min_stiff = min(min_stiff,float(np.min(aa-bb*bb/dd)))
        max_q_bound_ratio = max(max_q_bound_ratio,float(np.max(np.abs(position[1]))/np.sqrt(2*hh/B)))
        if min_n<=0 or min_d<=0 or not np.isfinite(lengths).all():
            raise RuntimeError('Selected positive-action/finite-length domain failed')
        return hh,qq

    def store(j):
        hh,qq = health_and_conservation()
        states[j] = np.concatenate((position,momentum))
        energies.append(hh)
        charges.append(qq)
        coefficients.append(2*np.dot(position[0]-background[0],np.conj(carrier))/N)

    store(0)
    for j in range(1,len(TIMES)):
        t = TIMES[j-1]
        while t<TIMES[j]-1e-12:
            step = min(dt,TIMES[j]-t)
            momentum += step*forces(position)/2
            position += step*velocities(momentum)
            momentum += step*forces(position)/2
            health_and_conservation()
            t += step
        store(j)
        if j%200==0:
            print('W84 dt=%.3g: t=%.1f' % (dt,TIMES[j]),file=sys.stderr,flush=True)
    coefficients = np.asarray(coefficients)
    phase = np.unwrap(np.angle(coefficients))
    slope,intercept = np.polyfit(TIMES,phase,1)
    fitted_omega = -slope
    phase_residual = float(np.max(np.abs(phase-(slope*TIMES+intercept))))
    amplitude_drift = float(np.max(np.abs(np.abs(coefficients)/abs(coefficients[0])-1)))
    return {'dt':dt,'states':states,'omega_linear':float(omega),'omega_measured':float(fitted_omega),
            'omega_relative_error':float(abs(fitted_omega-omega)/omega),
            'phase_fit_max_residual':phase_residual,'relative_amplitude_change':amplitude_drift,
            'initial_energy':initial_energy,'equilibrium_energy':background_energy,
            'positive_initial_perturbation_energy':perturbation_energy,
            'subtraction_float_spacing_scale':float(np.spacing(initial_energy)+np.spacing(background_energy)),
            'subtraction_spacing_relative_to_perturbation':float((np.spacing(initial_energy)+np.spacing(background_energy))/perturbation_energy),
            'max_energy_drift':max_energy_drift,'energy_drift_over_perturbation':max_energy_drift/perturbation_energy,
            'energy_drift_over_total':max_energy_drift/initial_energy,
            'initial_total_charge':initial_charge,'max_charge_drift':max_charge_drift,
            'min_phase_action':min_n,'min_length':min_d,'min_local_mixed_stiffness':min_stiff,
            'max_energy_length_bound_ratio':max_q_bound_ratio,
            'link_mode_ratio':[float(ratio.real),float(ratio.imag)],
            'phase_history':phase.tolist(),'amplitude_history':np.abs(coefficients).tolist(),
            'energy_history':energies,'total_charge_history':charges,
            'final_theta_mode':[float(coefficients[-1].real),float(coefficients[-1].imag)]}


def main():
    contract = HERE.with_name('w3_84_node_link_contract.md')
    pin_records = {name:{'actual':sha(ROOT/name),'expected':value} for name,value in PINS.items()}
    pin_ok = all(v['actual']==v['expected'] for v in pin_records.values()) and sha(contract)==CONTRACT_SHA
    package_ok = sorted(p.name for p in HERE.parent.iterdir()) == sorted([HERE.name,contract.name])
    result = {'stage':'W3-84-v1.0','claim':'W3_84_MINIMAL_DYNAMICAL_NODE_LINK',
              'type':'NEW_CLASSICAL_FINITE_GRAPH_HYPOTHESIS',
              'provenance':{'source_sha256':sha(HERE),'contract_sha256':sha(contract),'pins':pin_records,
                            'exact_two_files':package_ok,'versions':{'Python':platform.python_version(),'NumPy':np.__version__,'SciPy':scipy.__version__,'SymPy':sp.__version__}},
              'scope':{name:False for name in ('microscopic_law_derived','physical_node_identity','oscillon_solution',
                   'foundation_pressure_map','relativistic_covariance','Einstein_source_derived','weak_field_inheritance',
                   'singularity_resolution','observational_pass','active_theory_changed','intuitive_files_changed')}}
    if not pin_ok or not package_ok:
        result.update(status='UNRESOLVED',failure='Frozen provenance or exact-two-file package mismatch')
        return result
    exact = exact_checks()
    result['exact_and_mutation_checks'] = exact
    if not exact['passed']:
        result.update(status='UNRESOLVED',failure='Exact production or mutation evaluator failed')
        return result
    equilibria = [equilibrium(float(Q)) for Q in (0,np.pi/12,np.pi/6,np.pi/4)]
    result['equilibria'] = equilibria
    primary = equilibria[2]
    if not primary['stable'] or not all(row['passed'] for row in equilibria):
        result.update(status='UNRESOLVED',failure='Equilibrium/Jacobian gate or primary stability failed')
        return result
    runs = [evolve(primary,dt) for dt in (.04,.02,.01)]
    errors = []
    per_variable = []
    for a,b in zip(runs,runs[1:]):
        difference = (a['states']-b['states'])/(EPSILON*np.sqrt(N))
        errors.append(float(np.max(np.linalg.norm(difference.reshape(len(TIMES),-1),axis=1))))
        per_variable.append(np.max(np.linalg.norm(difference,axis=2),axis=0).tolist())
    for run in runs:
        del run['states']
    fine = runs[-1]
    flags = {
        'joint_energy_defined':exact['passed'],
        'reciprocal_forces':exact['baseline']['accepted'],
        'conservation_identities':exact['baseline']['accepted'],
        'equilibrium':all(row['equilibrium_force_residual']<1e-12 for row in equilibria),
        'mixed_spectrum':all(row['passed'] for row in equilibria),
        'nonlinear_mode':fine['omega_relative_error']<1e-3 and fine['phase_fit_max_residual']<.01 and fine['relative_amplitude_change']<.01 and fine['min_local_mixed_stiffness']>0,
        'energy_balance':fine['energy_drift_over_perturbation']<5e-4,
        'charge_balance':fine['max_charge_drift']<1e-10*max(1,abs(fine['initial_total_charge'])) and fine['min_phase_action']>0 and fine['min_length']>0,
        'refinement':errors[1]<1e-3 and (errors[1]<1e-7 or errors[1]<=.5*errors[0]),
        'mutation_controls':all(not v['accepted'] for v in exact['mutations'].values()),
    }
    result.update(closure_flags=flags,runs=runs,times=TIMES.tolist(),
                  refinement={'combined_canonical_errors':errors,'per_variable_order':['theta','q','n','P'],
                              'per_variable_errors':per_variable,'normalizer':'epsilon*sqrt(N); all common outputs'},
                  status='PASS' if all(flags.values()) else 'UNRESOLVED',
                  failed_gates=[k for k,v in flags.items() if not v])
    result['physical_outcome'] = {
        'state_classifications':[row['classification'] for row in equilibria],
        'primary_speed_ratio_to_ground':primary['physical_long_speed']/equilibria[0]['physical_long_speed'],
        'primary_slower_than_ground':primary['physical_long_speed']<equilibria[0]['physical_long_speed'],
        'scope':'Reciprocal link-opening and phase-transfer response of the NEW finite Hamiltonian hypothesis. No damping, asymptotic locking, RefG pressure identification, relativistic front or Einstein continuation is inferred.'}
    return result


if __name__ == '__main__':
    try:
        with np.errstate(over='raise',invalid='raise',divide='raise'):
            report = main()
        print(json.dumps(report,allow_nan=False,separators=(',',':')))
        sys.exit(0 if report.get('status')=='PASS' else 1)
    except Exception as exc:
        print(json.dumps({'stage':'W3-84-v1.0','status':'UNRESOLVED','failure_type':type(exc).__name__,'failure':str(exc)},allow_nan=False))
        raise
