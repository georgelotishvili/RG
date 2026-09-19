"""Stdout-only verifier for frozen SINGLE_STATE_RESONANCE_RESPONSE_V1.

Run with python -B. This verifies an explicitly new finite-mode constitutive
law, not a reduction of the earlier scalar PDE or homogeneous tension EOS.
All benchmarks and decision thresholds are frozen in the adjacent ledger.
"""

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.special import lambertw

VERSION = 'SINGLE_STATE_RESONANCE_RESPONSE_V1'
TOLS = ((1e-8, 1e-11), (1e-10, 1e-13))
LIMITS = dict(equilibrium=1e-11, energy=2e-8, refinement=2e-6,
              clocks=2e-6, interval=2e-9, terminal=1e-7, inertia_ratio=0.8)
CHECKS = {}
MAX_STEP = 0.1


def check(name, passed, **metrics):
    CHECKS[name] = dict(pass_=bool(passed), **metrics)


def zero(name, expression):
    residual = sp.simplify(expression)
    check(name, residual == 0, residual=str(residual))


def symbolic_checks():
    u, v, a, w, b = sp.symbols('u v a w b', real=True)
    I, K, z, M, p, s = sp.symbols('I K z M p s', positive=True)
    P = sp.exp(-u)
    V = K*u**2/2 + M*P
    L = I*v**2/(2*P) - V
    momentum = sp.diff(L, v)
    el = sp.diff(momentum, u)*v + sp.diff(momentum, v)*a
    el += -sp.diff(L, u) + z*v
    expected = a + v**2/2 + z*P*v/I + K*P*u/I - M*P**2/I
    zero('exact_variation', el*P/I - expected)
    acceleration = sp.solve(el, a)[0]
    E = v*momentum - L
    zero('exact_energy_definition', E - (I*v**2/(2*P)+V))
    zero('exact_energy_balance', sp.diff(E, u)*v
         + sp.diff(E, v)*acceleration + z*v**2)
    tau_eq = b-w**2/2+z*w/I+K*u/(I*P)-M/I
    zero('exact_clock_transform', expected.subs(
        {v: P*w, a: P**2*(b-w**2)}, simultaneous=True)/P**2-tau_eq)
    zero('exact_double_factor_loss', (z*v**2).subs(v, P*w)-z*P**2*w**2)
    pd, pdd = sp.symbols('pd pdd', real=True)
    transformed = expected.subs({u: -sp.log(p), v: -pd/p,
        a: -pdd/p+pd**2/p**2}, simultaneous=True)*(-p)
    p_eq = pdd-3*pd**2/(2*p)+z*p*pd/I+K*p**2*sp.log(p)/I+M*p**3/I
    zero('exact_pressure_transform', transformed-p_eq)
    velocity = sp.solve((el*P).subs(I, 0), v)[0]
    first_p = (-P*velocity).subs(u, -sp.log(p))
    zero('exact_first_order_rate', first_p-(-K*p*sp.log(p)-M*p**2)/z)
    zero('exact_first_order_source_p2', sp.diff(first_p, M)+p**2/z)
    zero('exact_first_order_energy', sp.diff(V, u)*velocity+z*velocity**2)
    zero('exact_stationary_root', sp.diff(V, u).subs({u: s, M: K*s*sp.exp(s)}))
    zero('exact_stationary_curvature', sp.diff(V, u, 2).subs(
        {u: s, M: K*s*sp.exp(s)})-K*(1+s))
    zero('exact_global_convexity', sp.diff(V, u, 2)-(K+M*P))
    zero('exact_coercive_remainder', E-K*u**2/2-(I*v**2/(2*P)+M*P))
    zero('exact_zero_content_branch', sp.diff(V, u).subs({M: 0, u: 0}))
    # Wrong candidates are substituted into the same independently varied action.
    for label, power in [('missing', 1), ('extra', 3)]:
        bad_a = acceleration-M*P**2/I+M*P**power/I
        residual = sp.simplify(el.subs(a, bad_a))
        witness = float(residual.subs({u: sp.log(2), I: 1, K: 1, M: 1, z: 1, v: 0}))
        check('negative_'+label+'_clock', residual != 0 and witness != 0,
              residual=str(residual), witness=witness)
    wrong_exchange = sp.simplify(sp.diff(E, u)*v+sp.diff(E, v)*acceleration-z*v**2)
    check('negative_wrong_exchange_sign', wrong_exchange != 0,
          residual=str(wrong_exchange))
    # M>0 branch; M=0 at rest is separately static, without a finite endpoint.
    t, tau, p0 = sp.symbols('t tau p0', positive=True)
    q = p0/(1+M*p0**2*t**2/(2*I))
    zero('exact_unrestored_ode', sp.diff(q, t, 2)
         -3*sp.diff(q, t)**2/(2*q)+M*q**3/I)
    zero('exact_unrestored_energy', I*sp.diff(q, t)**2/(2*q**3)+M*q-M*p0)
    local_time = sp.sqrt(2*I/M)*sp.atan(p0*sp.sqrt(M/(2*I))*t)
    zero('exact_unrestored_clock', sp.diff(local_time, t)-q)
    angle = sp.sqrt(M/(2*I))*tau
    qt = p0*sp.cos(angle)**2
    zero('exact_unrestored_local_ode', sp.diff(qt, tau, 2)
         -sp.diff(qt, tau)**2/(2*qt)+M*qt/I)
    zero('exact_unrestored_finite_tau', sp.limit(local_time, t, sp.oo)
         -sp.pi*sp.sqrt(I/(2*M)))
    zero('exact_unrestored_external_zero_limit', sp.limit(q, t, sp.oo))
    return dict(coercivity='E >= K*u^2/2; p >= exp(-sqrt(2*E_initial/K))',
                clocks='tau(t) >= exp(-sqrt(2*E_initial/K))*t',
                stability='V_second=K+M*exp(-u)>0; zeta>0 gives dissipation',
                equilibrium='u_star=LambertW(M/K); M=0 gives u_star=0',
                local_endpoint='pi*sqrt(I/(2*M)), K=zeta=0, M>0, initially at rest')


def rhs_external(params):
    inertia, stiffness, load, damping, first = params

    def rhs(t, y):
        u = y[0]
        p = np.exp(-u)
        if first:
            v = (load*p-stiffness*u)/damping
            return [v, damping*v*v, p]
        v = y[1]
        acceleration = -.5*v*v-damping*p*v/inertia
        acceleration += p*(load*p-stiffness*u)/inertia
        return [v, acceleration, damping*v*v, p]
    return rhs


def rhs_local(params):
    inertia, stiffness, load, damping, first = params

    def rhs(tau, y):
        u = y[0]
        inverse_p = np.exp(u)
        if first:
            w = (load-stiffness*u*inverse_p)/damping
            return [w, damping*w*w/inverse_p, inverse_p]
        w = y[1]
        acceleration = .5*w*w-damping*w/inertia
        acceleration += (load-stiffness*u*inverse_p)/inertia
        return [w, acceleration, damping*w*w/inverse_p, inverse_p]
    return rhs


def energy(y, params, local=False):
    inertia, stiffness, load, damping, first = params
    p = np.exp(-y[0])
    result = .5*stiffness*y[0]**2+load*p
    if not first:
        result += .5*inertia*y[1]**2*(p if local else 1/p)
    return result


def constitutive_sensitivity():
    """Post-contract analytic diagnostic; not a registered numerical gate."""
    u = sp.symbols('u', positive=True)
    bounded_response = u**2/(2*(1+u**2))
    available = 1-sp.exp(-u)-bounded_response
    lower = u*(u**2-u+2)/(2*(1+u)*(1+u**2))
    residuals = dict(
        same_weak_stiffness=sp.diff(bounded_response, u, 2).subs(u, 0)-1,
        rational_lower_bound=sp.simplify(1-1/(1+u)-bounded_response-lower),
        positive_quadratic=sp.expand(u**2-u+2-((u-sp.Rational(1, 2))**2+sp.Rational(7, 4))),
        origin_available_energy=sp.limit(available/u, u, 0)-1,
        infinity_available_energy=sp.limit(available, u, sp.oo)-sp.Rational(1, 2))
    return dict(role='POST_CONTRACT_ANALYTIC_SENSITIVITY_NOT_REGISTERED_GATE',
                residuals={k: str(v) for k, v in residuals.items()},
                identities_verified=all(v == 0 for v in residuals.values()),
                assumptions='I=K=M=1, zeta=0, initially u=u_t=0; alternate bounded response',
                comparison='exp(-u)<1/(1+u), u>0, gives D>positive rational lower bound',
                endpoint='d_tau/du=exp(-u/2)/sqrt(2*D): integrable at 0 and infinity',
                interpretation='Weak quadratic stiffness alone does not imply the global energy barrier')


def integrate(rhs, end, initial, tolerance, method):
    solution = solve_ivp(rhs, (0, end), initial, method=method,
                         rtol=tolerance[0], atol=tolerance[1], dense_output=True,
                         max_step=MAX_STEP)
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution


def numerical_case(name, params, u0, v0, end, method='DOP853'):
    inertia, stiffness, load, damping, first = params
    initial = [u0, 0., 0.] if first else [u0, v0, 0., 0.]
    initial_local = [u0, 0., 0.] if first else [u0, v0*np.exp(u0), 0., 0.]
    grid = np.linspace(0, end, 801)
    external = [integrate(rhs_external(params), end, initial, tol, method) for tol in TOLS]
    states = [sol.sol(grid) for sol in external]
    tau_end = float(states[1][-1, -1])
    local = [integrate(rhs_local(params), tau_end, initial_local, tol, method) for tol in TOLS]
    local_grid = np.linspace(0, tau_end, 801)
    local_states = [sol.sol(local_grid) for sol in local]
    e0 = float(energy(np.asarray(initial), params))
    budgets = [float(np.max(np.abs(energy(y, params)+y[-2]-e0))/abs(e0)) for y in states]
    local_budgets = [float(np.max(np.abs(energy(y, params, True)+y[-2]-e0))/abs(e0))
                     for y in local_states]
    refinement = float(np.max(np.abs(states[0]-states[1])))
    local_refinement = float(np.max(np.abs(local_states[0]-local_states[1])))
    endpoint = local_states[1][:, -1].copy()
    reference = states[1][:, -1].copy()
    if not first:
        endpoint[1] *= np.exp(-endpoint[0])
    reference[-1] = end
    clock_error = float(np.max(np.abs(endpoint-reference)))
    check(name+'_energy', max(budgets[1], local_budgets[1]) < LIMITS['energy'],
          external=budgets, local=local_budgets)
    check(name+'_refinement', max(refinement, local_refinement) < LIMITS['refinement'],
          external=refinement, local=local_refinement)
    check(name+'_clocks', clock_error < LIMITS['clocks'],
          endpoint_error=clock_error, external_end=end, local_end=tau_end)
    observed_min = float(np.min(np.exp(-states[1][0])))
    analytic_bound = float(np.exp(-np.sqrt(2*e0/stiffness)))
    if first:
        star = float(lambertw(load/stiffness).real)
        lower, upper = min(u0, star), max(u0, star)
        violation = max(0., lower-float(np.min(states[1][0])), float(np.max(states[1][0]))-upper)
        local_violation = max(0., lower-float(np.min(local_states[1][0])),
                              float(np.max(local_states[1][0]))-upper)
        final_error = abs(float(states[1][0, -1])-star)
        check(name+'_interval', max(violation, local_violation) <= LIMITS['interval'],
              external_violation=violation, local_violation=local_violation)
        check(name+'_terminal', final_error < LIMITS['terminal'], error=final_error)
    return dict(parameters=dict(I=inertia, K=stiffness, M=load, zeta=damping),
                first_order=first, method=method, initial=initial, external_end=end,
                p_min_sampled=observed_min, analytic_p_bound=analytic_bound,
                energy_initial=e0, external_nfev=[s.nfev for s in external],
                local_nfev=[s.nfev for s in local]), external[1], grid


def main():
    global MAX_STEP
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--unbounded-step', action='store_true',
                        help='Reproduce the initial adaptive-step numerical method, including its failures.')
    args = parser.parse_args()
    MAX_STEP = np.inf if args.unbounded_step else 0.1
    analytic = symbolic_checks()
    cases = {}
    for load in (1., 10.):
        star = float(lambertw(load).real)
        residual = abs(star-load*np.exp(-star))
        check('equilibrium_'+str(load), residual < LIMITS['equilibrium'],
              residual=residual, u_star=star, p_star=float(np.exp(-star)))
        for label, u0 in [('below', 0.), ('above', star+.25)]:
            name = 'first_M'+str(load)+'_'+label
            cases[name], _, _ = numerical_case(name, (0., 1., load, 1., True), u0, 0., 80.)
        for damping in (0., .7):
            name = 'inertial_M'+str(load)+'_z'+str(damping)
            cases[name], _, _ = numerical_case(name, (1., 1., load, damping, False), 0., 0., 60.)
    # Registered well-prepared initial velocity agrees with the I=0 law.
    reference = integrate(rhs_external((0., 1., 1., 1., True)), 8.,
                          [0., 0., 0.], TOLS[1], 'DOP853')
    errors = []
    for inertia in (.01, .005, .0025):
        name = 'limit_I'+str(inertia)
        cases[name], solution, grid = numerical_case(
            name, (inertia, 1., 1., 1., False), 0., 1., 8., 'Radau')
        y = solution.sol(grid)
        r = reference.sol(grid)
        velocity = np.exp(-r[0])-r[0]
        components = [float(np.max(np.abs(y[0]-r[0]))),
                      float(np.max(np.abs(np.exp(-y[0])-np.exp(-r[0])))),
                      float(np.max(np.abs(y[1]-velocity)))]
        errors.append(max(components))
        cases[name]['inertia_errors_u_p_velocity'] = components
    ratios = [errors[j+1]/errors[j] for j in range(2)]
    check('inertia_limit', all(r < LIMITS['inertia_ratio'] for r in ratios),
          max_errors=errors, halving_ratios=ratios)
    failures = [name for name, entry in CHECKS.items() if not entry['pass_']]
    exact = all(entry['pass_'] for name, entry in CHECKS.items() if name.startswith('exact_'))
    numeric = all(entry['pass_'] for name, entry in CHECKS.items()
                  if not name.startswith(('exact_', 'negative_')))
    flags = dict(candidate_response_closed=exact,
                 candidate_energy_balanced=exact and all(v['pass_'] for k, v in CHECKS.items() if k.endswith('_energy')),
                 candidate_equilibrium=exact and all(v['pass_'] for k, v in CHECKS.items() if k.startswith('equilibrium_')),
                 candidate_two_clock_positivity=exact,
                 Original_PDE_reduction_derived=False, homogeneous_tension_EOS_derived=False,
                 spatial_RefG_closure=False, observational_pass=False, singularity_resolution=False)
    path = Path(__file__).resolve()
    ledger = path.with_name('foundation_oscillon_minimum_closure.md')
    text = ledger.read_text(encoding='utf-8')
    marker = '- CLAIM_ID / MODEL_VERSION: '+VERSION+'.'
    ending = 'This finite-mode result does not complete \u00a74\'s full spatial action.'
    start = text.rindex(marker)
    frozen = text[start:text.index(ending, start)+len(ending)]
    environment = dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__,
                       sympy=sp.__version__, platform=platform.platform())
    hashes = dict(source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  contract_section_sha256=hashlib.sha256(frozen.encode('utf-8')).hexdigest(),
                  environment_sha256=hashlib.sha256(json.dumps(environment, sort_keys=True).encode()).hexdigest())
    report = dict(model_version=VERSION, status='PASS' if not failures else 'FAIL',
                  scope='CONDITIONAL_FINITE_MODE_CANDIDATE', thresholds=LIMITS,
                  tolerances=TOLS, sample_points=801, numerical_evidence_pass=numeric,
                  max_step=None if args.unbounded_step else MAX_STEP,
                  step_policy='unbounded_adaptive' if args.unbounded_step else 'controlled_0.1_in_each_clock',
                  analytic=analytic, checks=CHECKS, failed_checks=failures,
                  post_contract_analytic_sensitivity=constitutive_sensitivity(),
                  metric_definitions=dict(refinement='max absolute full-state discrepancy on 801 common samples',
                      external_state='[u,W,tau] or [u,u_t,W,tau]',
                      local_state='[u,W,t] or [u,u_tau,W,t]',
                      clock_endpoint='max absolute error of [u,W,t] or [u,p*u_tau,W,t]',
                      inertia_limit='max absolute error across u, p and u_t on 801 samples',
                      energy='max abs(E+W-E_initial)/abs(E_initial), separately in both clocks',
                      interval='max fine-sample excess outside initial/equilibrium interval in either clock'),
                  closure_flags=flags, cases=cases, environment=environment, hashes=hashes)
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
