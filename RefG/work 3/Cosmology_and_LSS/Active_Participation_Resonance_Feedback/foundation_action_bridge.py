'''FULL_ACTION_ENERGY_BRIDGE_V1: stdout-only exact action/source audit.

Frozen contract: foundation_oscillon_minimum_closure.md, same claim ID.
Run: python -B foundation_action_bridge.py. No numerical evolution or fit.
EOS examples witness underdetermination; neither is an adopted new law.
EH/ADM boundary comparison assumes smooth fields and matched boundary terms.
Packet scaling assumes an admissible finite packet/cell and proper boundary
accounting, not an unspecified infinite background or ADM-constrained data.
'''

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import sys
import argparse

sys.dont_write_bytecode = True
import sympy as sp

HERE = Path(__file__).resolve().parent
WORK3 = HERE.parents[1]
LEDGER = HERE / 'foundation_oscillon_minimum_closure.md'
CLAIM_ID = 'FULL_ACTION_ENERGY_BRIDGE_V1'
PINS = {
    'w54_contract': (
        WORK3 / 'Lagrangian_Formulation'
        / 'Relational_Coframe_TEGR_Phase_Source_Closure'
        / 'w3_54_relational_coframe_tegr_phase_source_closure_contract.md',
        '6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879'),
    'scalar_candidate': (HERE / 'common_scale_finite_source_candidate.py',
        '6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8'),
    'profile_verifier': (HERE / 'profile_relaxed_response.py',
        '7d8059fb2123778f890c1e679f374820c9f9010e54ec4d34a1e5efc10458a7ba'),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    checks, controls = {}, {}

    def exact(name, expression):
        residual = sp.simplify(expression)
        checks[name] = {'passed': residual == 0, 'residual': str(residual)}

    def positive(name, expression):
        factored = sp.factor(expression)
        checks[name] = {'passed': factored.is_positive is True,
                        'positive_factorization': str(factored)}

    def control(name, expression, explanation):
        residual = sp.simplify(expression)
        controls[name] = {'passed': residual != 0, 'nonzero_difference': str(residual),
                          'meaning': explanation}

    u = sp.symbols('u', real=True)
    n, q, p, alpha = sp.symbols('n q p alpha', positive=True)
    rho = sp.Function('rho')
    mu = sp.diff(rho(n), n)
    pressure = n*mu-rho(n)
    volume4 = sp.exp(2*u)
    metric = sp.diag(-sp.exp(-2*u), *([sp.exp(2*u)]*3))
    n_fixed = sp.sqrt(-metric[0, 0]*q*q)/sp.sqrt(-metric.det())
    exact('rest_current_density_from_metric', n_fixed-q*sp.exp(-3*u))
    lagrangian = -volume4*rho(n_fixed)
    source = volume4*(rho(n)+3*pressure)
    exact('fixed_current_action_source', sp.diff(lagrangian, u)
          -source.subs(n, n_fixed))
    stress_upper = sp.diag(rho(n)*sp.exp(2*u),
                           *([pressure*sp.exp(-2*u)]*3))
    hilbert = volume4*sum(stress_upper[i, i]*sp.diff(metric[i, i], u)
                          for i in range(4))/2
    exact('independent_hilbert_source', hilbert-source)
    energy = -lagrangian
    exact('conserved_count_energy_derivative', sp.diff(energy, q)
          -sp.exp(-u)*mu.subs(n, n_fixed))
    exact('fluid_first_law', sp.diff(rho(n)/n, n)-pressure/n**2)
    exact('pressure_derivative', sp.diff(pressure, n)-n*sp.diff(mu, n))
    nx, px = sp.symbols('n_x p_x', real=True)
    hydro = sp.diff(pressure, n)*nx+(rho(n)+pressure)*px/p
    chemical_gradient = px*mu+p*sp.diff(mu, n)*nx
    exact('independent_static_euler', hydro-n*chemical_gradient/p)
    nt, pt = sp.symbols('n_t p_t', real=True)
    exact('rest_continuity_at_fixed_coordinate_cell',
          sp.diff(n/p**3, n)*nt+sp.diff(n/p**3, p)*pt
          -(nt-3*n*pt/p)/p**3)
    C = sp.symbols('C', real=True)
    shifted = rho(n)+C*n
    shifted_pressure = n*sp.diff(shifted, n)-shifted
    exact('add_Cn_preserves_pressure', shifted_pressure-pressure)
    exact('add_Cn_changes_source', shifted+3*shifted_pressure
          -(rho(n)+3*pressure)-C*n)
    R, M, P = sp.symbols('rho mu Pi', positive=True)
    control('omitted_3Pi', sp.exp(2*u)*3*P,
            'Fails for positive pressure; the dust special case is not generic.')
    control('wrong_local_p5_current_response',
            sp.exp(2*u)*((5*n*M-2*R)-(3*n*M-2*R)),
            'Using n=q p^5 changes the fixed-current source by 2 n mu exp(2u).')

    # The unaltered scalar action supplies the u equation. Apply its exact
    # differential chain rule to p=exp(-u), including the new rest-fluid term.
    ptt, lap, grad2, psi_t2, V = sp.symbols(
        'p_tt laplacian_p grad_p_squared psi_t_squared V', real=True)
    ut = -pt/p
    utt = pt**2/p**2-ptt/p
    lapu = grad2/p**2-lap/p
    u_equation = ((utt+2*ut**2)/p**4-lapu-2*alpha*psi_t2/p**4
                  +2*alpha*V/p**2-alpha*(R+3*P)/p**2)
    p_rhs = (3*pt**2/p-p**3*grad2-2*alpha*p*psi_t2
             +2*alpha*p**3*V-alpha*p**3*(R+3*P))
    exact('rest_fluid_scalar_p_equation_chain_rule',
          -p**5*u_equation-(ptt-p**4*lap-p_rhs))

    # Full ADM lapse variation is performed with A and J0 independent of N.
    N, A = sp.symbols('N A', positive=True)
    Adot, Lambda, R3 = sp.symbols('A_dot Lambda R3', real=True)
    K = sp.eye(3)*A*Adot/N
    inverse_h = sp.eye(3)/A**2
    K_mixed = inverse_h*K
    K_combo = sp.trace(K_mixed*K_mixed)-sp.trace(K_mixed)**2
    exact('ADM_extrinsic_contraction', K_combo+6*(Adot/(N*A))**2)
    ADM = N*A**3*(R3+K_combo-2*Lambda)/(4*alpha)
    matter_ADM = -N*A**3*rho(q/A**3)
    lapse_equation = 4*alpha/A**3*sp.diff(ADM+matter_ADM, N)
    exact('independent_lapse_constraint_before_restriction', lapse_equation
          -(R3+6*(Adot/(N*A))**2-2*Lambda-4*alpha*rho(q/A**3)))
    exact('independent_lapse_matter_source',
          sp.diff(matter_ADM, N)+A**3*rho(q/A**3))

    # Independent geometric route: Christoffels and Ricci contraction of
    # g=diag(-exp(-2u),exp(2u),exp(2u),exp(2u)), using exact derivative jets.
    first = sp.symbols('u_t u_x u_y u_z', real=True)
    second = {(i, j): sp.symbols('u_%s%s' % (i, j), real=True)
              for i in range(4) for j in range(i, 4)}

    def derivative(expression, coordinate):
        return (sp.diff(expression, u)*first[coordinate]
                +sum(sp.diff(expression, first[i])
                     *second[tuple(sorted((i, coordinate)))] for i in range(4)))

    def ricci_scalar(diagonal, indices):
        gamma = {}
        for a in indices:
            for b in indices:
                for c in indices:
                    gamma[a, b, c] = sp.simplify(
                        ((derivative(diagonal[a], b) if a == c else 0)
                         +(derivative(diagonal[a], c) if a == b else 0)
                         -(derivative(diagonal[b], a) if b == c else 0))
                        /(2*diagonal[a]))
        result = 0
        for a in indices:
            ricci = sum(derivative(gamma[k, a, a], k)
                        -derivative(gamma[k, a, k], a)
                        +sum(gamma[k, a, a]*gamma[l, k, l]
                             -gamma[k, a, l]*gamma[l, a, k] for l in indices)
                        for k in indices)
            result += sp.simplify(ricci)/diagonal[a]
        return sp.simplify(result)

    diagonal = {i: metric[i, i] for i in range(4)}
    grad_u2 = sum(first[i]**2 for i in range(1, 4))
    lap_u = sum(second[i, i] for i in range(1, 4))
    R3_direct = ricci_scalar(diagonal, range(1, 4))
    R3_formula = sp.exp(-2*u)*(-4*lap_u-2*grad_u2)
    exact('three_curvature_from_Christoffels', R3_direct-R3_formula)
    restricted = ADM.subs({N: sp.exp(-u), A: sp.exp(u),
                          Adot: sp.exp(u)*first[0], R3: R3_formula}, simultaneous=True)
    target = -lap_u/alpha-(grad_u2+3*sp.exp(4*u)*first[0]**2
                           +Lambda*sp.exp(2*u))/(2*alpha)
    exact('ADM_common_scale_restriction', restricted-target)
    R4_direct = ricci_scalar(diagonal, range(4))
    EH_direct = volume4*(R4_direct-2*Lambda)/(4*alpha)
    boundary = lap_u/(2*alpha)+3*derivative(sp.exp(4*u)*first[0], 0)/(2*alpha)
    exact('independent_four_curvature_boundary_crosscheck',
          EH_direct-restricted-boundary)
    candidate = (sp.exp(4*u)*first[0]**2-grad_u2)/(2*alpha)
    EH_bulk = (restricted+lap_u/alpha).subs(Lambda, 0)
    exact('candidate_minus_EH_kinetic_difference',
          candidate-EH_bulk-2*sp.exp(4*u)*first[0]**2/alpha)
    control('candidate_plus_one_is_not_EH_minus_three',
            sp.diff(candidate, first[0], 2)/ (sp.exp(4*u)/alpha)
            -sp.diff(EH_bulk, first[0], 2)/(sp.exp(4*u)/alpha),
            'Normalized kinetic coefficients differ by 4, even at Lambda=0.')

    # All positivity statements use exact factors, or zero boundary value
    # plus a strictly positive derivative on x>0. No sampled inequalities.
    x, m, ns = sp.symbols('x m n_s', positive=True)
    eos = [m*n+m*n**2/(2*ns), 2*m*n-m*ns*sp.log(1+n/ns)]
    witnesses = []
    for i, energy_n in enumerate(eos, 1):
        tag = 'eos%s_' % i
        mu_n = sp.diff(energy_n, n)
        Pi_n = n*mu_n-energy_n
        cs_n = n*sp.diff(mu_n, n)/mu_n
        expressions = [sp.simplify(expr.subs(n, ns*x))
                       for expr in (energy_n, mu_n, Pi_n, cs_n)]
        energy_x, mu_x, Pi_x, cs_x = expressions
        expected_cs = x/(1+x) if i == 1 else x/((1+x)*(1+2*x))
        expected_mu = m*(1+x) if i == 1 else m*(1+2*x)/(1+x)
        expected_Pi = m*ns*x**2/2 if i == 1 else m*ns*(sp.log(1+x)-x/(1+x))
        exact(tag+'chemical_potential', mu_x-expected_mu)
        exact(tag+'pressure', Pi_x-expected_Pi)
        exact(tag+'sound_speed', cs_x-expected_cs)
        exact(tag+'zero_density_energy_limit', sp.limit(energy_x, x, 0, dir='+'))
        exact(tag+'zero_density_pressure_limit', sp.limit(Pi_x, x, 0, dir='+'))
        positive(tag+'rho_positive_by_increase_from_zero', sp.diff(energy_x, x))
        positive(tag+'Pi_positive_by_increase_from_zero', sp.diff(Pi_x, x))
        positive(tag+'chemical_potential_positive', mu_x)
        positive(tag+'compressibility_positive', sp.diff(mu_x, x))
        positive(tag+'sound_speed_positive', cs_x)
        positive(tag+'sound_speed_below_one', 1-cs_x)
        lapse = sp.factor(mu_x.subs(x, 1)/mu_x)
        expected_p = 2/(1+x) if i == 1 else sp.Rational(3, 2)*(1+x)/(1+2*x)
        endpoint = sp.S.Zero if i == 1 else sp.Rational(3, 4)
        exact(tag+'normalized_static_lapse', lapse-expected_p)
        exact(tag+'Euler_first_integral', lapse*mu_x-mu_x.subs(x, 1))
        exact(tag+'reference_lapse_one', lapse.subs(x, 1)-1)
        exact(tag+'static_lapse_endpoint', sp.limit(lapse, x, sp.oo)-endpoint)
        witnesses.append({'rho': str(energy_x), 'mu': str(mu_x), 'Pi': str(Pi_x),
                          'cs_squared': str(cs_x), 'static_p': str(lapse),
                          'static_p_limit': str(endpoint), 'adopted': False})
    inverse_x2 = (3-2*p)/(4*p-3)
    exact('eos2_density_inverse',
          (sp.Rational(3, 2)*(1+x)/(1+2*x)).subs(x, inverse_x2)-p)
    density_limit = sp.limit(ns*inverse_x2, p, sp.Rational(3, 4), dir='+')
    controls['positive_lapse_does_not_bound_density'] = {
        'passed': density_limit == sp.oo, 'lapse_endpoint': '3/4',
        'density_limit': str(density_limit), 'scope': 'static first integral only'}
    for label, expression in (
            ('rho', eos[1]), ('Pi', n*sp.diff(eos[1], n)-eos[1])):
        endpoint_limit = sp.limit(expression, n, sp.oo)
        checks['eos2_'+label+'_diverges_at_density_endpoint'] = {
            'passed': endpoint_limit == sp.oo, 'limit': str(endpoint_limit),
            'expected_limit': 'oo'}

    U, B, Cg, proper_energy, proper_volume = sp.symbols(
        'U B C_grad E_proper V_proper', positive=True)
    exact('correlated_shrink_proper_volume', p**(-3)*p**3*proper_volume-proper_volume)
    exact('correlated_shrink_conserved_number',
          n*p**(-3)*p**3*proper_volume-n*proper_volume)
    exact('correlated_shrink_material_energy', p**(-2)*p**3*proper_energy-p*proper_energy)
    total_family = sp.exp(-U)*(B+Cg*U**2+proper_energy)
    exact('finite_packet_extends_existing_family_limit', sp.limit(total_family, U, sp.oo))
    return checks, controls, witnesses


def static_compatibility():
    """Independent necessary-equilibrium gate; no new constitutive law."""
    claim = 'STATIC_COMMON_SCALE_COMPATIBILITY_V1'
    if claim not in LEDGER.read_text(encoding='utf-8-sig'):
        raise ValueError('Missing compatibility contract: '+claim)
    sources = dict(PINS)
    sources.update({
        'existing_common_scale_source': (
            WORK3 / 'Strong_Field' / 'W3-92_Covariant_Medium_Integration'
            / 'common_scale_centre_source.md',
            '8d1bb86883989c425c601682d22f49f7c6aec9820999514e2d53cf924e4a65b9'),
        'canonical_oscillon': (
            WORK3 / 'Lagrangian_Formulation' / 'One_Oscillon_Coframe_Localized_Core'
            / 'w3_58_one_oscillon_coframe_localized_core.py',
            'b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57'),
    })
    provenance = {key: {'path': str(path), 'sha256': digest(path),
                        'expected_sha256': expected, 'passed': digest(path) == expected}
                  for key, (path, expected) in sources.items()}
    if not all(row['passed'] for row in provenance.values()):
        raise RuntimeError('Compatibility source changed; review contract.')
    checks, controls = {}, {}

    def exact(name, expression):
        residual = sp.simplify(expression)
        checks[name] = {'passed': residual == 0, 'residual': str(residual)}

    t, r, theta, phi = sp.symbols('t r theta phi', real=True)
    alpha, mass = sp.symbols('alpha mass', positive=True)
    u, slip = sp.Function('u')(r), sp.Function('slip')(r)
    coords = (t, r, theta, phi)
    diagonal = (-sp.exp(-2*u+2*slip), sp.exp(2*u),
                r**2*sp.exp(2*u), r**2*sp.exp(2*u)*sp.sin(theta)**2)
    gamma = {}
    for a in range(4):
        for b in range(4):
            for c in range(4):
                gamma[a, b, c] = sp.simplify(
                    ((sp.diff(diagonal[a], coords[b]) if a == c else 0)
                     +(sp.diff(diagonal[a], coords[c]) if a == b else 0)
                     -(sp.diff(diagonal[b], coords[a]) if b == c else 0))
                    /(2*diagonal[a]))
    ricci = []
    for a in range(4):
        ricci.append(sp.simplify(sum(
            sp.diff(gamma[k, a, a], coords[k])
            -sp.diff(gamma[k, a, k], coords[a])
            +sum(gamma[k, a, a]*gamma[l, k, l]
                 -gamma[k, a, l]*gamma[l, a, k] for l in range(4))
            for k in range(4))))
    scalar = sp.simplify(sum(ricci[i]/diagonal[i] for i in range(4)))
    einstein = [sp.simplify(ricci[i]-diagonal[i]*scalar/2) for i in range(4)]
    eps = sp.simplify(-einstein[0]/diagonal[0]/(2*alpha))
    radial = sp.simplify(einstein[1]/diagonal[1]/(2*alpha))
    tangential = sp.simplify(einstein[2]/diagonal[2]/(2*alpha))
    exact('angular_pressures_equal', tangential-einstein[3]/diagonal[3]/(2*alpha))

    def replace(expression, rules):
        return sp.simplify(expression.subs(rules).doit())

    common = [replace(expr, {slip: 0}) for expr in (eps, radial, tangential)]
    ur, urr = sp.diff(u, r), sp.diff(u, r, 2)
    exact('common_energy', common[0]+sp.exp(-2*u)*(2*(urr+2*ur/r)+ur**2)/(2*alpha))
    exact('common_radial_pressure', common[1]+sp.exp(-2*u)*ur**2/(2*alpha))
    exact('common_tangential_pressure', common[2]-sp.exp(-2*u)*ur**2/(2*alpha))
    exact('common_anisotropy', common[1]-common[2]+sp.exp(-2*u)*ur**2/alpha)
    exact('general_slip_equation', 2*alpha*sp.exp(2*u)*(radial-tangential)
          -(-sp.diff(slip, r, 2)+sp.diff(slip, r)/r-2*ur**2
            +4*ur*sp.diff(slip, r)-sp.diff(slip, r)**2))

    # Vary sqrt(-g)*L with separate radial and tangential logarithmic
    # ruler coefficients, holding coordinate field derivatives fixed.
    a, b, lapse = sp.symbols('a b lapse', real=True)
    ft2, fr, potential, current_pressure = sp.symbols(
        'field_time_derivative_squared field_radial_derivative V Pi_C', real=True)
    volume = sp.exp(lapse+a+2*b)
    scalar_lag = (sp.exp(-2*lapse)*ft2-sp.exp(-2*a)*fr**2)/2-potential
    matter_radial = sp.diff(volume*scalar_lag, a)/volume+current_pressure
    matter_tangent = sp.diff(volume*scalar_lag, b)/(2*volume)+current_pressure
    source_difference = sp.simplify(matter_radial-matter_tangent)
    exact('scalar_anisotropy_from_independent_variation',
          source_difference-sp.exp(-2*a)*fr**2)
    exact('isotropic_EOS_cancels', sp.diff(source_difference, current_pressure))
    fprime, uprime = sp.symbols('f_prime u_prime', real=True)
    mismatch = (common[1]-common[2]-source_difference.subs(a, u)).subs(
        {ur: uprime, fr: fprime})
    squares = uprime**2+alpha*fprime**2
    exact('constraint_is_sum_of_nonnegative_squares',
          mismatch+sp.exp(-2*u)*squares/alpha)
    checks['sum_squares_nonnegative_for_real_profiles'] = {
        'passed': squares.is_nonnegative is True,
        'expression': str(squares), 'domain': 'real derivatives, alpha>0'}
    checks['both_square_coefficients_strictly_positive'] = {
        'passed': alpha.is_positive is True, 'coefficients': ['1', str(alpha)]}
    controls['nonuniform_empty_scalar_profile_still_fails'] = {
        'passed': sp.simplify(mismatch.subs({uprime: 1, fprime: 0})) != 0,
        'residual': str(sp.simplify(mismatch.subs({uprime: 1, fprime: 0})))}

    # Exact empty-exterior witness with INDEPENDENT metric potentials.
    # This is not a new adopted background or a finite-body solution.
    N = (1-mass/(2*r))/(1+mass/(2*r))
    A = (1+mass/(2*r))**2
    rules = {u: sp.log(A), slip: sp.log(N*A)}
    for name, expression in zip(('energy', 'radial', 'tangential'),
                                (eps, radial, tangential)):
        exact('independent_potentials_vacuum_'+name, replace(expression, rules))
    exact('vacuum_product', N*A-(1-mass**2/(4*r**2)))
    exact('vacuum_ruler_clock_relation', 1/A-(1+N)**2/4)
    exact('vacuum_ruler_departure', 1/A-N-(1-N)**2/4)
    exact('vacuum_coordinate_light_departure', N/A-N**2-N*(1-N)**2/4)
    controls['forcing_common_scale_changes_the_vacuum_witness'] = {
        'passed': sp.simplify(N*A-1) != 0, 'difference': str(sp.simplify(N*A-1))}

    passed = all(row['passed'] for row in [*checks.values(), *controls.values()])
    output = {
        'claim_id': claim, 'status': 'PASS_EXACT_COMPATIBILITY_AUDIT' if passed else 'FAIL',
        'checks': checks, 'negative_controls': controls,
        'source_provenance': provenance, 'ledger_sha256_at_run': digest(LEDGER),
        'self_sha256': digest(Path(__file__)),
        'software': {'python': platform.python_version(), 'sympy': sp.__version__},
        'decision': ('REJECTED_NONUNIFORM_STATIC_COMMON_SCALE_EH_CURRENT_CANONICAL_SCALAR'
                     if passed else 'NO_VERIFIED_DECISION'),
        'scope': ['Static smooth r>0; real radial scalar profile; positive G.',
                  'Arbitrary rest-current barotropic EOS and canonical scalar potential.',
                  'No additional anisotropic source or modified gravitational action.',
                  'Vacuum witness: Lambda=0, r>mass/2, mass>0; not a completed material body.',
                  'No no-go claim for all RefG completions or dynamic oscillons.'],
        'closure_flags': {key: False for key in (
            'replacement_action_adopted', 'EOS_selected', 'nonlinear_equilibrium_closed',
            'two_clock_nozero_closed', 'singularity_resolution_closed')},
        'next_required_choice': 'Change the gravitational/medium response or relax exact common scaling.',
        'error_bound': 'Exact symbolic identities; no numerical fitting or tolerance.',
        'side_effects': 'stdout only',
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    if not passed:
        raise AssertionError('Static compatibility audit failed.')


def main():
    if not LEDGER.is_file():
        raise FileNotFoundError('Frozen contract ledger is missing: '+str(LEDGER))
    marker_present = CLAIM_ID in LEDGER.read_text(encoding='utf-8-sig')
    if not marker_present:
        raise ValueError('Frozen contract marker is missing: '+CLAIM_ID)
    contract_provenance = {
        'path': str(LEDGER), 'sha256_at_run': digest(LEDGER),
        'required_marker': CLAIM_ID, 'marker_present': marker_present}
    provenance = {}
    for label, (path, expected) in PINS.items():
        actual = digest(path)
        provenance[label] = {'path': str(path), 'expected_sha256': expected,
                             'actual_sha256': actual, 'passed': actual == expected}
    if not all(item['passed'] for item in provenance.values()):
        print(json.dumps({'status': 'FAIL_SOURCE_PIN', 'sources': provenance}, indent=2))
        raise RuntimeError('Inherited source hash changed; review the frozen contract.')
    checks, controls, witnesses = verify()
    passed = all(item['passed'] for item in [*checks.values(), *controls.values()])
    current_keys = (
        'rest_current_density_from_metric', 'fixed_current_action_source',
        'independent_hilbert_source', 'conserved_count_energy_derivative',
        'fluid_first_law', 'pressure_derivative', 'independent_static_euler',
        'rest_continuity_at_fixed_coordinate_cell',
        'rest_fluid_scalar_p_equation_chain_rule')
    adm_keys = (
        'ADM_extrinsic_contraction', 'independent_lapse_constraint_before_restriction',
        'independent_lapse_matter_source', 'three_curvature_from_Christoffels',
        'ADM_common_scale_restriction', 'independent_four_curvature_boundary_crosscheck',
        'candidate_minus_EH_kinetic_difference')
    witness_keys = [key for key in checks if key.startswith('eos')]
    witness_keys += ['add_Cn_preserves_pressure', 'add_Cn_changes_source']
    verified_flags = {
        'current_source_derived': all(checks[key]['passed'] for key in current_keys),
        'ADM_comparison_verified': all(checks[key]['passed'] for key in adm_keys)
            and controls['candidate_plus_one_is_not_EH_minus_three']['passed'],
        'constitutive_witnesses_verified': all(checks[key]['passed'] for key in witness_keys)
            and controls['positive_lapse_does_not_bound_density']['passed']}
    output = {
        'claim_id': CLAIM_ID, 'contract_provenance': contract_provenance,
        'status': 'PASS_DECLARED_EXACT_AUDIT' if passed else 'FAIL_EXACT_AUDIT',
        'checks': checks, 'negative_controls': controls, 'unselected_EOS_witnesses': witnesses,
        'sources': provenance, 'self_sha256': digest(Path(__file__)),
        'software': {'python': platform.python_version(), 'sympy': sp.__version__},
        'assumptions': [
            'c0=1, signature -+++, alpha=4 pi G>0; independent N,A before restriction.',
            'rho is smooth at n>0; conserved densitized current is held fixed in metric variation.',
            'EOS witness m, n_s, x positive; zero-density limits are witness extensions only.',
            'ADM and direct EH expressions are compared with explicit matched boundary divergence.',
            'Finite-packet scaling requires its vacuum/boundary prescription; no infinite-background claim.',
            'The correlated-shrink trial family is not assumed to satisfy the full ADM constraints.'],
        'time_scope': 'Static Euler fixes no trajectory or endpoint times; motion also requires continuity, Euler dynamics and the complete field equations.',
        'verified_flags': verified_flags,
        'closure_flags': {key: False for key in (
            'EOS_selected', 'full_action_identified_with_scalar_candidate',
            'nonlinear_equilibrium_closed', 'two_clock_nozero_closed',
            'singularity_resolution_closed')},
        'error_bound': 'Exact symbolic algebra; no numerical tolerance or fitted threshold.',
        'side_effects': 'stdout only; no result files or bytecode written',
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    if not passed:
        failed = [key for key, item in {**checks, **controls}.items() if not item['passed']]
        raise AssertionError('Exact audit failures: '+', '.join(failed))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--static-compatibility', action='store_true',
                        help='Check the necessary static source compatibility, without rerunning V1.')
    args = parser.parse_args()
    if args.static_compatibility:
        static_compatibility()
    else:
        main()
