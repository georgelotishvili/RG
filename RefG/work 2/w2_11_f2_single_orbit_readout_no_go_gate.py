"""Exact no-go for invariant whole-state readouts on one accepted F1 orbit.

The theorem rejects only a narrow route: a complete-equivalence-invariant
whole-state readout cannot distinguish representatives of one transitive
orbit.  Covariant F1 roles, law-derived internal effect families, derived
joint-state relations, and multiple-orbit routes remain open.
"""

from __future__ import annotations

import itertools
import json
from typing import Any, Callable

import sympy as sp

SCIENTIFIC_CONTRACT: dict[str, Any] = {'CLAIM_ID': 'W2_F2_SINGLE_ORBIT_WHOLE_STATE_READOUT_NO_GO_001',
 'CLAIM': 'At one fixed parameter point, every complete-equivalence-invariant whole-state report '
          'is constant on one transitive accepted orbit; this rejects only that route.',
 'TYPE': 'CONDITIONAL_EXACT_ROUTE_CLASS_NO_GO_WITH_SYMBOLIC_AND_EXHAUSTIVE_CONTROLS',
 'ASSUMPTIONS': ('The frozen F2a contract and accepted conditional F1 result are valid '
                 'dependencies.',
                 'One model parameter point is fixed and the accepted F1 minima form one full '
                 'orbit.',
                 'The declared O(3) conjugation is internal equivalence, not physical spatial '
                 'rotation.',
                 'The whole-state report is invariant under the complete declared equivalence.'),
 'DOMAIN': 'One fixed-parameter transitive accepted orbit.  Multiple orbits, joint states, '
           'intrastate effect families, time, geometry, observables and data are outside the '
           'no-go.',
 'CONVENTIONS': 'Orbit representatives are descriptions of one quotient class.  Invariant means a '
                'trivial output action; covariant means an explicitly declared output action.',
 'FREEDOM_LEDGER': {'inherited_f1_parameters': {'source': 'imported F1 open domain alpha,b,c>0; '
                                                          'fixed during each orbit theorem',
                                                'allowed_range': 'positive open domain, one fixed '
                                                                 'fibre at a time',
                                                'scale': 'three inherited model parameters; not '
                                                         'fitted here',
                                                'complexity': 3},
                    'new_parameters': {'source': 'none',
                                       'allowed_range': 0,
                                       'scale': 'theorem',
                                       'complexity': 0},
                    'data_fitted_parameters': {'source': 'none',
                                               'allowed_range': 0,
                                               'scale': 'data',
                                               'complexity': 0},
                    'chosen_representative': {'source': 'for algebraic crosscheck only; no '
                                                        'representative is an output',
                                              'allowed_range': 'any point on the same declared '
                                                               'orbit',
                                              'scale': 'description',
                                              'complexity': 0},
                    'extra_physical_primitives': {'source': 'none',
                                                  'allowed_range': 0,
                                                  'scale': 'foundation',
                                                  'complexity': 0}},
 'DEPENDENCIES': ['w2_10 F2a internal-distinction definition',
                  'w2_09a conditional atemporal F1 orbit structure'],
 'METHOD': 'Prove the transitive-orbit theorem directly; exhaust a finite S3 action as an '
           'independent control; specialize exactly to the symbolic accepted F1 O(3) orbit.',
 'PASS_CONDITION': 'The exact theorem, named scientific dependencies, exhaustive finite-group '
                   'control, symbolic F1 specialization, escape routes, scope ceiling, and closure '
                   'ledger agree.',
 'FAIL_CONDITION': 'Any incomplete equivalence, parameter/state conflation, preferred '
                   'representative, F1-role erasure, escape-route rejection, or scope overclaim.',
 'FALSIFIER': 'Two points of one transitive orbit and a genuinely complete-equivalence-invariant '
              'single-state report with unequal outputs.',
 'RESIDUAL': '0 for the exact group-action identity and symbolic matrix identities.',
 'ERROR_BOUND': '0; no floating-point or observational calculation is used.',
 'VALIDITY_HEALTH': 'Exact only for one transitive orbit at fixed parameters and the complete '
                    'declared equivalence.  It is not a no-go for all operational or relational '
                    'constructions.',
 'BRANCHES': {'one_orbit_invariant_whole_state': 'REJECTED_IF_EXACT_CONTROLS_PASS',
              'covariant_representative_output': 'VALID_BUT_NOT_AN_INVARIANT_REPORT',
              'intrastate_uniform_effect_family': 'OPEN_UNEVALUATED',
              'derived_joint_common_action': 'OPEN_UNEVALUATED',
              'multiple_accepted_orbits': 'OPEN_UNEVALUATED'},
 'OBSERVABLE_MAP': {'status': 'N/A', 'reason': 'internal theorem only'},
 'FORWARD_MODEL': {'status': 'N/A', 'reason': 'no measurement or data chain'},
 'DATA_ROLE': {'status': 'N/A', 'reason': 'no data used'},
 'IDENTIFIABILITY': 'A single quotient class is identifiable only as that class.  Representative '
                    'entries and axes are description-dependent; different classes and internal '
                    'relational structures require separate derived maps.',
 'BENCHMARK': 'Finite complete versus incomplete group actions, one versus multiple orbits, common '
              'versus independent pair actions, and the exact F1 symbolic orbit are fixed '
              'controls.',
 'CROSSCHECK': 'Direct analytic proof, exhaustive finite-group enumeration and an independent '
               'SymPy specialization share only the declared group-action assumptions.',
 'THEOREM': {'fixed_parameter_domain': 'Fix one accepted model parameter point; parameter changes '
                                       'are not state motion.',
             'accepted_orbit': 'For a group G acting on X, the accepted set A is exactly one '
                               'transitive orbit G.x, so A/G contains one class.',
             'invariant_readout': 'A whole-state report r:A->Z is invariant only if r(g.q)=r(q) '
                                  'for every declared equivalence g and every q in A.',
             'covariant_output': 'A representative output F:A->Y may obey F(g.q)=rho(g).F(q); its '
                                 'representative can vary, while its quotient class pi_Y(F(q)) is '
                                 'invariant.',
             'exact_statement': 'Every complete-equivalence-invariant whole-state report on one '
                                'transitive orbit is constant, and every equivariant output has '
                                'constant quotient class there.',
             'proof': 'For q1=g1.x and q2=g2.x, let k=g2 g1^{-1}; then q2=k.q1 and invariance '
                      'gives r(q2)=r(k.q1)=r(q1).  Equivariance puts F(q1),F(q2) in one '
                      'rho(G)-orbit.',
             'f1_corollary': 'On the fixed-parameter accepted F1 O(3)-orbit, invariant whole-state '
                             'reports cannot select an orientation or distinguish accepted '
                             'representatives.',
             'claim_ceiling': 'Constancy does not erase covariant intrastate roles, does not make '
                              'a constant structured table entrywise trivial, and does not reject '
                              'derived relational routes.'},
 'REJECTED_ROUTE': {'route': 'ONE_ORBIT_INVARIANT_WHOLE_STATE_READOUT',
                    'class_definition': 'one fixed-parameter transitive accepted orbit plus one '
                                        'single-state report that is invariant under the complete '
                                        'declared equivalence',
                    'rejection_reason': 'the report is exactly constant by transitivity and '
                                        'invariance',
                    'status': 'REJECTED_BY_EXACT_NO_GO_ONLY_IN_THIS_DECLARED_CLASS'},
 'PRESERVED_ROUTES': {'intrastate_uniform_effect_family': 'OPEN: generated relata plus an '
                                                          'independently law-derived uniform '
                                                          'comparison/effect family may have '
                                                          'invariant internal structure, including '
                                                          'a derived delta response.',
                      'derived_joint_common_action': 'OPEN: a derived joint domain and common '
                                                     'diagonal action may support relational '
                                                     'invariants; independent relabelling remains '
                                                     'the null.',
                      'multiple_accepted_orbits': 'OPEN: an invariant report may distinguish '
                                                  'different accepted quotient classes.',
                      'endogenous_atemporal_response': 'OPEN: an atemporal law-derived response '
                                                       'carrier may be tested separately; '
                                                       'persistence and directed influence remain '
                                                       'behind F3.'},
 'FORBIDDEN_INPUTS': ('preferred representative, fixed axis, ordered eigenbasis, target projector, '
                      'or Q11 readout',
                      'parameter variation, the origin, the rejected stationary branch, or minus-Q '
                      'added to one orbit',
                      'preloaded response/equality table, self-selector, external label, '
                      'apparatus, or observable',
                      'unregistered pair state, composition rule, common action, or restricted '
                      'equivalence subgroup',
                      'sampled rotations, random points, tolerance, floating-point constancy, or '
                      'numerical promotion',
                      'physical space, time, causality, mode, metric, action, GR, node, record, or '
                      'measurement semantics'),
 'SCOPE_CEILING': {'foundation_law_derived': False,
                   'functional_uniqueness_derived': False,
                   'N3_physical_origin_derived': False,
                   'F2a_internal_operational_distinction_proved': False,
                   'full_W2_F2_operational_relations': False,
                   'physical_node_or_location': False,
                   'persistent_physical_imprint': False,
                   'temporal_formation_or_persistence': False,
                   'internal_order_or_causality': False,
                   'independent_additive_modes': False,
                   'physical_dimension_or_continuum': False,
                   'Lorentzian_metric_or_light_cone': False,
                   'effective_action_or_conservation_law': False,
                   'RefG_environment_map': False,
                   'mass_pressure_particle_or_oscillon': False,
                   'GR_PN_or_PPN_bridge': False,
                   'external_observable_or_data_map': False,
                   'observational_validation': False},
 'SCIENTIFIC_CLOSURE': {'F1_conditional_structural_result_inherited': True,
                        'F2a_contract_defined': True,
                        'single_orbit_invariant_readout_route_rejected': True,
                        'F2a_candidate_proved': False,
                        'F2b_candidate_proved': False,
                        'full_W2_F2_operational_relations_proved': False,
                        'F3_internal_order_or_causality_proved': False,
                        'Lorentzian_metric_or_Einstein_branch_proved': False,
                        'PN_or_PPN_handoff_proved': False}}
CLAIM_CONTRACT = SCIENTIFIC_CONTRACT
EXPECTED_SCOPE_CEILING = dict(CLAIM_CONTRACT["SCOPE_CEILING"])
EXPECTED_SCIENTIFIC_CLOSURE = dict(CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"])

def _all_true(value: Any) -> bool:
    if isinstance(value, dict):
        return all(_all_true(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return all(_all_true(item) for item in value)
    return value is True


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return str(value)


def scope_closure_controls() -> dict[str, bool]:
    scope = CLAIM_CONTRACT.get("SCOPE_CEILING")
    closure = CLAIM_CONTRACT.get("SCIENTIFIC_CLOSURE")
    return {
        "scope_ceiling_exact": (
            isinstance(scope, dict)
            and scope == EXPECTED_SCOPE_CEILING
            and all(type(value) is bool for value in scope.values())
        ),
        "scientific_closure_exact": (
            isinstance(closure, dict)
            and closure == EXPECTED_SCIENTIFIC_CLOSURE
            and all(type(value) is bool for value in closure.values())
        ),
    }

Permutation = tuple[int, ...]
State = tuple[int, ...]

def act(permutation: Permutation, state: State) -> State:
    return tuple(state[index] for index in permutation)

def compose(left: Permutation, right: Permutation) -> Permutation:
    """Composition compatible with act(left, act(right, state))."""
    return tuple(right[index] for index in left)

def inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for index, image in enumerate(permutation):
        result[image] = index
    return tuple(result)

def parity(permutation: Permutation) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1

def is_invariant(
    group: tuple[Permutation, ...], orbit: tuple[State, ...],
    readout: Callable[[State], Any],
) -> bool:
    return all(readout(act(g, state)) == readout(state) for g in group for state in orbit)

def finite_group_controls() -> dict[str, bool]:
    group = tuple(itertools.permutations(range(3)))
    identity = (0, 1, 2)
    seed = (0, 1, 2)
    orbit = tuple(sorted({act(g, seed) for g in group}))
    transitive = all(any(act(g, left) == right for g in group) for left in orbit for right in orbit)
    sorted_readout = lambda state: tuple(sorted(state))
    sum_readout = sum
    representative_readout = lambda state: state[0]
    covariant_output = lambda state: state
    quotient_output = lambda state: tuple(sorted(covariant_output(state)))

    even_group = tuple(g for g in group if parity(g) == 1)
    even_sample = tuple(sorted({act(g, seed) for g in even_group}))
    orientation = parity

    second_seed = (0, 1, 3)
    two_orbits = orbit + tuple(sorted({act(g, second_seed) for g in group}))
    orbit_labels = {tuple(sorted(state)) for state in two_orbits}

    e1, e2 = (1, 0, 0), (0, 1, 0)
    dot = lambda left, right: sum(a * b for a, b in zip(left, right))
    common_invariant = all(
        dot(act(g, left), act(g, right)) == dot(left, right)
        for g in group for left in (e1, e2) for right in (e1, e2)
    )
    independent_null = any(
        dot(act(g, e1), act(h, e1)) != dot(e1, e1)
        for g in group for h in group
    )

    structured = lambda _state: ((1, 0), (0, 1))
    structured_outputs = {structured(state) for state in orbit}
    return {
        "complete_group_and_transitive_orbit_exact": all((
            len(group) == 6, len(orbit) == 6, transitive,
            identity in group,
            all(compose(left, right) in group for left in group for right in group),
            all(
                compose(compose(first, second), third)
                == compose(first, compose(second, third))
                for first in group for second in group for third in group
            ),
            all(
                compose(g, inverse(g)) == identity
                and compose(inverse(g), g) == identity
                for g in group
            ),
            all(
                act(left, act(right, state)) == act(compose(left, right), state)
                for left in group for right in group for state in orbit
            ),
            all(act(g, state) in orbit for g in group for state in orbit),
        )),
        "invariant_whole_state_readouts_constant": all((
            is_invariant(group, orbit, sorted_readout),
            is_invariant(group, orbit, sum_readout),
            len({sorted_readout(state) for state in orbit}) == 1,
            len({sum_readout(state) for state in orbit}) == 1,
        )),
        "covariant_representative_varies_but_quotient_constant": all((
            all(covariant_output(act(g, state)) == act(g, covariant_output(state))
                for g in group for state in orbit),
            len({representative_readout(state) for state in orbit}) > 1,
            not is_invariant(group, orbit, representative_readout),
            len({quotient_output(state) for state in orbit}) == 1,
        )),
        "incomplete_equivalence_sampling_trap_rejected": all((
            len(even_sample) == 3,
            len({orientation(state) for state in even_sample}) == 1,
            is_invariant(even_group, orbit, orientation),
            len({orientation(state) for state in orbit}) == 2,
            not is_invariant(group, orbit, orientation),
        )),
        "multiple_orbit_escape_preserved": all((
            len(orbit_labels) == 2,
            is_invariant(group, tuple(two_orbits), sorted_readout),
        )),
        "common_action_pair_invariant_and_independent_action_null": all((
            common_invariant, independent_null, dot(e1, e1) == 1, dot(e1, e2) == 0,
        )),
        "constant_structured_output_not_entrywise_trivial": all((
            len(structured_outputs) == 1,
            {entry for row in structured(seed) for entry in row} == {0, 1},
        )),
    }

def matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.trigsimp(sp.simplify(entry)) == 0 for entry in matrix)

def f1_symbolic_controls() -> dict[str, bool]:
    theta = sp.symbols("theta", real=True)
    s = sp.symbols("s", nonzero=True, real=True)
    rotation = sp.Matrix([
        [sp.cos(theta), -sp.sin(theta), 0],
        [sp.sin(theta), sp.cos(theta), 0],
        [0, 0, 1],
    ])
    identity = sp.eye(3)
    q0 = s * sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
    qt = sp.trigsimp(rotation * q0 * rotation.T)
    i2_0, i3_0 = sp.trace(q0**2), sp.trace(q0**3)
    i2_t, i3_t = sp.trigsimp(sp.trace(qt**2)), sp.trigsimp(sp.trace(qt**3))

    p1_0 = sp.simplify(identity / 3 + q0 / s)
    p2_0 = sp.simplify(identity - p1_0)
    p1_t = sp.trigsimp(identity / 3 + qt / s)
    p2_t = sp.trigsimp(identity - p1_t)
    p1_covariance = sp.trigsimp(p1_t - rotation * p1_0 * rotation.T)
    p2_covariance = sp.trigsimp(p2_t - rotation * p2_0 * rotation.T)
    at_zero = sp.simplify(p1_t.subs(theta, 0))
    at_quarter = sp.simplify(p1_t.subs(theta, sp.pi / 2))

    n = sp.Matrix([1, 0, 0])
    minus_n = -n
    q_of_n = s * (n * n.T - identity / 3)
    q_of_minus_n = s * (minus_n * minus_n.T - identity / 3)
    central = -identity

    q_scale_1 = q0.subs(s, 1)
    q_scale_2 = q0.subs(s, 2)
    return {
        "symbolic_orbit_invariants_constant": all((
            matrix_zero(rotation.T * rotation - identity),
            sp.simplify(rotation.det()) == 1,
            sp.trigsimp(i2_t - i2_0) == 0,
            sp.trigsimp(i3_t - i3_0) == 0,
            sp.simplify(i2_0 - 2 * s**2 / 3) == 0,
            sp.simplify(i3_0 - 2 * s**3 / 9) == 0,
        )),
        "projectors_covariant_and_internal_roles_preserved": all((
            matrix_zero(p1_covariance), matrix_zero(p2_covariance),
            matrix_zero(p1_t**2 - p1_t), matrix_zero(p2_t**2 - p2_t),
            matrix_zero(p1_t * p2_t), matrix_zero(p1_t + p2_t - identity),
            sp.trigsimp(sp.trace(p1_t)) == 1,
            sp.trigsimp(sp.trace(p2_t)) == 2,
            p1_0.rank() == 1, p2_0.rank() == 2,
        )),
        "representative_entries_vary_and_are_not_invariant_reports": all((
            at_zero != at_quarter,
            at_zero[0, 0] == 1, at_quarter[0, 0] == 0,
            sp.trace(at_zero) == sp.trace(at_quarter) == 1,
        )),
        "preferred_axis_is_not_a_single_valued_state_readout": all((
            q_of_n == q_of_minus_n, n != minus_n,
            central * q_of_n * central.T == q_of_n,
            central * n == minus_n,
        )),
        "parameter_variation_is_not_same_fixed_parameter_orbit": all((
            sp.trace(q_scale_1**2) == sp.Rational(2, 3),
            sp.trace(q_scale_2**2) == sp.Rational(8, 3),
            sp.trace(q_scale_1**2) != sp.trace(q_scale_2**2),
        )),
    }

def run() -> dict[str, Any]:
    finite = finite_group_controls()
    symbolic = f1_symbolic_controls()
    scope_closure = scope_closure_controls()
    valid = _all_true(finite) and _all_true(symbolic) and _all_true(scope_closure)
    return {
        "artifact": CLAIM_CONTRACT["CLAIM_ID"],
        "valid": valid,
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "Within one complete transitive quotient orbit, every invariant whole-state "
            "readout is constant. Covariant representatives and multi-orbit or relational "
            "routes remain open; this is not a global F2 no-go."
        ),
        "scope_ceiling": CLAIM_CONTRACT["SCOPE_CEILING"],
        "scientific_closure": CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"],
        "finite_group_controls": finite,
        "f1_symbolic_controls": symbolic,
        "scope_closure_controls": scope_closure,
    }

def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_CONTRACT.get("CLAIM_ID", "unknown"),
            "valid": False,
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(_json_safe(report), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
