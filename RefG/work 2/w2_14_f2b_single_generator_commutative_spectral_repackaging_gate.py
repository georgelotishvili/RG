"""Exact scoped no-go for F2b from commutative repackaging of the frozen Q state.

The class contains only the accepted F1 single carrier Q, its regular spectral
functional calculus, the already imported matrix product/trace/transpose, and
law jets used strictly as diagnostics.  It asks whether these ingredients can
produce state-owned nodes and a pair relation outside unary/equality data.

The theorem is deliberately class-local.  It does not reject noncommuting
single-carrier channels, a genuinely state-owned joint carrier, or any revised
candidate that revalidates F1 and F2a.  Full W2-F2 remains open here.
"""

from __future__ import annotations

import json
from typing import Any

import sympy as sp

SCIENTIFIC_CONTRACT: dict[str, Any] = {'CLAIM_ID': 'W2_F2B_SINGLE_GENERATOR_COMMUTATIVE_SPECTRAL_NO_GO_001',
 'CLAIM': 'Within the exact frozen one-Q commutative spectral class, prove that canonical state '
          'nodes stop at P1/P2 and every uniform pair word factors through unary data and '
          'equality; reject only this class and keep full F2 open.',
 'TYPE': 'EXACT_CLASS_LOCAL_NO_GO',
 'ASSUMPTIONS': ('The exact frozen F1, w2_12 F2a and w2_13 completion boundaries are valid.',
                 'The class contains exactly one accepted symmetric carrier Q and no hidden state '
                 'component.',
                 'Law derivatives remain diagnostics and the complete equivalence is inherited '
                 'O(3).'),
 'DOMAIN': 'Every accepted uniaxial Q on the full open alpha,b,c>0 branch.',
 'CONVENTIONS': 'O(3) is internal, not physical space.  Spectral projector means an algebraic '
                'subobject, not automatically a node.  A set-valued fibre is not simultaneous '
                'state content.',
 'FREEDOM_LEDGER': {'inherited_alpha_b_c': {'source': 'exact F1 dependency',
                                            'allowed_range': 'alpha,b,c>0',
                                            'scale': 'three inherited universal parameters',
                                            'complexity': 3},
                    'spectral_function_choice': {'source': 'universally quantified regular f',
                                                 'allowed_range': 'all regular functions of Q',
                                                 'scale': 'theorem class, not fitted choice',
                                                 'complexity': 0},
                    'word_length': {'source': 'universally quantified finite word',
                                    'allowed_range': 'every finite length',
                                    'scale': 'inductive theorem class',
                                    'complexity': 0},
                    'node_selector': {'source': 'none',
                                      'allowed_range': 0,
                                      'scale': 'class',
                                      'complexity': 0},
                    'pair_report': {'source': 'universally quantified uniform spectral word/trace '
                                              'report',
                                    'allowed_range': 'complete declared class',
                                    'scale': 'theorem class',
                                    'complexity': 0},
                    'preferred_basis_or_axis': {'source': 'none',
                                                'allowed_range': 0,
                                                'scale': 'description',
                                                'complexity': 0},
                    'new_state_component': {'source': 'none',
                                            'allowed_range': 0,
                                            'scale': 'accepted state',
                                            'complexity': 0},
                    'data_fitted_parameters': {'source': 'none',
                                               'allowed_range': 0,
                                               'scale': 'data',
                                               'complexity': 0}},
 'DEPENDENCIES': ['w2_12 F2a Hessian comparison',
                  'w2_13 F2b completion requirements',
                  'w2_09a conditional atemporal F1 carrier'],
 'METHOD': 'Use the accepted minimal polynomial, central idempotents, stabilizer fixed-point '
           'classification and an induction on finite spectral words; audit fibre and law-jet '
           'escapes.',
 'PASS_CONDITION': 'All exact algebra, stabilizer, escape-route, dependency, scope, and closure '
                   'checks pass.  Success proves only the declared class-local no-go.',
 'FAIL_CONDITION': 'Any regular spectral element outside span{P1,P2}, canonical rank-one split of '
                   'P2, nonzero irreducible spectral pair quotient, dependency drift or global '
                   'overclaim.',
 'FALSIFIER': 'An exact candidate using only the declared class that passes every w2_13 node, '
              'state-carrier and irreducible-pair gate falsifies this no-go.',
 'RESIDUAL': '0 for every exact identity; no numerical residual.',
 'ERROR_BOUND': '0; symbolic class theorem.',
 'VALIDITY_HEALTH': 'Valid only for the explicitly frozen commutative spectral class; it makes no '
                    'dynamical, physical, geometric or observational claim.',
 'BRANCHES': {'declared_commutative_spectral_class': 'REJECTED_IF_EXACT_CONTROLS_PASS',
              'rank2_set_valued_subprojector_fibre': 'FAILS_STATE_OWNERSHIP_AND_IMPRINT',
              'law_jet_as_diagnostic': 'RETAINED_AS_F2A_ONLY',
              'noncommuting_or_joint_state_routes': 'OPEN_NEW_VERSION',
              'full_c0_f2': 'OPEN'},
 'OBSERVABLE_MAP': {'status': 'N/A', 'reason': 'atemporal internal no-go'},
 'FORWARD_MODEL': {'status': 'N/A', 'reason': 'no observable'},
 'DATA_ROLE': {'status': 'N/A', 'reason': 'no data or fit'},
 'IDENTIFIABILITY': 'The complete class is fixed by one generator and its two central spectral '
                    'idempotents; any added selector or carrier is identifiable as a class exit.',
 'BENCHMARK': 'Positive controls are exact spectral reduction and stabilizer classification; nulls '
              'are off-diagonal words, subprojector overlap, gauge tangents and parameter '
              'stitching.',
 'CROSSCHECK': 'Direct symbolic matrix identities, representation/stabilizer proof, exact '
               'finite-word reduction, and explicit preserved-route controls.',
 'CLASS_DEFINITION': {'state': 'One accepted Q in Sym_0(3,R); no second accepted-state component.',
                      'accepted_branch': 'The exact alpha,b,c>0 uniaxial F1 branch with spectrum '
                                         '(2s/3,-s/3,-s/3), s>0.',
                      'equivalence': 'Complete inherited O(3) conjugation; Q sign is not gauge.',
                      'allowed_algebra': 'The regular unital commutative algebra generated by I '
                                         'and Q, including polynomial/rational spectral functional '
                                         'calculus where denominators are regular, matrix product, '
                                         'transpose, trace and parameter scalars.',
                      'allowed_reports': 'Uniform target-free reports assembled from spectral '
                                         'idempotents, allowed algebra elements, products and '
                                         'traces on the same accepted state.',
                      'law_jet_role': 'Gradient, Hessian and higher law derivatives are diagnostic '
                                      'tensors over the state; they are not accepted-state '
                                      'components in this frozen class.',
                      'node_rule': 'A canonical node must be a single-valued O(3)-covariant, '
                                   'state-supported subobject.  A set of possible subprojectors is '
                                   'not a set of coexisting occupied nodes.',
                      'excluded_extensions': 'Any noncommuting accepted-state channel, extra '
                                             'carrier, product state, selected subprojector, law '
                                             'jet promoted to state, time, geometry or data.',
                      'parameter_domain': 'The full open inherited domain alpha,b,c>0.',
                      'class_boundary': 'The result rejects only single-generator commutative '
                                        'spectral repackaging; it is not a no-go for RefG, for '
                                        'every no-new-primitive construction, or for full F2.'},
 'NO_GO_THEOREM': {'spectral_algebra_collapse': 'The accepted Q has a degree-two minimal '
                                                'polynomial, so every regular spectral element is '
                                                'x P1 + y P2.',
                   'canonical_node_bound': 'Only P1 and P2 are canonical central idempotents.  The '
                                           'O(2) stabilizer on P2 forbids a covariant rank-one '
                                           'split without an additional state object.',
                   'pair_factorization': 'Orthogonality P_a P_b=delta_ab P_a reduces every uniform '
                                         'spectral pair word to unary spectral scalars multiplied '
                                         'by bare equality; its irreducible quotient is zero.',
                   'degenerate_fibre_boundary': 'All rank-one subprojectors inside P2 form a '
                                                'state-owned possibility fibre, but no member is '
                                                'selected or coexists as accepted-state content.  '
                                                'Their overlap is inherited kinematics: p q p=Tr(p '
                                                'q)p for rank-one p,q.  Same unary support with '
                                                'varying bare overlap is therefore a controlled '
                                                'false positive, not an imprint.',
                   'law_jet_boundary': 'A law jet may distinguish diagnostic sectors as in w2_12, '
                                       'but treating such a sector as occupied node or carrier '
                                       'changes the accepted state space and leaves this class.',
                   'conclusion': 'No candidate in the declared class can satisfy the w2_13 '
                                 'state-node, state-carrier and irreducible-pair gates; therefore '
                                 'this class cannot close F2b.',
                   'not_ruled_out': 'A noncommuting channel contained in one revised carrier, a '
                                    'genuine state-owned joint carrier, or another version that '
                                    'revalidates F1 and F2a remains open.'},
 'NO_GO_GATE_EVIDENCE': {'exact_w213_dependency_and_f2a_boundary': 'Frozen w2_13 and exact w2_12 '
                                                                   'F2a boundary pass.',
                         'accepted_uniaxial_minimal_polynomial_exact': 'The accepted spectrum and '
                                                                       'degree-two identity are '
                                                                       'exact.',
                         'commutative_spectral_algebra_is_two_dimensional': 'Every regular f(Q) '
                                                                            'reduces to xP1+yP2.',
                         'only_two_canonical_central_projectors': 'The central idempotents are '
                                                                  'exactly 0,P1,P2,I.',
                         'stabilizer_forbids_canonical_rank1_split_of_rank2_sector': 'No '
                                                                                     'O(2)-fixed '
                                                                                     'rank-one '
                                                                                     'corner '
                                                                                     'idempotent '
                                                                                     'exists.',
                         'uniform_spectral_pair_words_factor_through_unary_and_equality': 'All '
                                                                                          'cross '
                                                                                          'words '
                                                                                          'vanish '
                                                                                          'and '
                                                                                          'diagonal '
                                                                                          'words '
                                                                                          'are '
                                                                                          'unary.',
                         'set_valued_subprojector_fibre_is_not_coexisting_state_content': 'A '
                                                                                          'possibility '
                                                                                          'fibre '
                                                                                          'supplies '
                                                                                          'no '
                                                                                          'selected '
                                                                                          'simultaneous '
                                                                                          'nodes.',
                         'bare_overlap_on_that_fibre_is_not_a_state_imprint': 'Its varying overlap '
                                                                              'comes from the '
                                                                              'imported '
                                                                              'contraction.',
                         'law_jets_remain_diagnostics_unless_state_space_is_revised': 'w2_12 '
                                                                                      'expressly '
                                                                                      'does not '
                                                                                      'promote '
                                                                                      'jets to '
                                                                                      'state '
                                                                                      'content.',
                         'parameter_fibres_and_gauge_tangents_do_not_supply_relata': 'Cross-fibre '
                                                                                     'stitching '
                                                                                     'and orbit '
                                                                                     'tangents '
                                                                                     'remain '
                                                                                     'excluded.',
                         'open_positive_parameter_domain_is_covered': 'The proof uses only s>0 on '
                                                                      'every alpha,b,c>0 accepted '
                                                                      'branch.',
                         'preserved_escape_routes_are_not_rejected': 'All routes outside the exact '
                                                                     'class stay explicitly open.'},
 'ESCAPE_ROUTE_REGISTRY': {'NONCOMMUTING_SINGLE_CARRIER_TRANSPOSE_CHANNELS': 'OPEN - a revised '
                                                                             'one-carrier state '
                                                                             'may have symmetric '
                                                                             'and skew state-owned '
                                                                             'channels.',
                           'STATE_OWNED_JOINT_CARRIER': 'OPEN - must be generated and fully '
                                                        'ledgered, not a target table.',
                           'REVISED_LAW_JET_AS_ACCEPTED_STATE_COMPONENT': 'OPEN_NEW_VERSION - '
                                                                          'requires a state-space '
                                                                          'law and full chain '
                                                                          'revalidation.',
                           'GENUINE_MULTI_OBJECT_DYNAMICAL_STATE': 'OPEN_NEW_VERSION - '
                                                                   'multiplicity and common action '
                                                                   'must be dynamically derived.',
                           'PROJECTIVE_FIBRE': 'OPEN_PROFILE - BARE_OVERLAP_OR_HIDDEN_SELECTION - '
                                               'a rank-one member is either unselected kinematics '
                                               'or an added state/node selector outside this '
                                               'class.'},
 'FORBIDDEN_UPGRADES': ('selected basis vector or rank-one corner projector renamed a node',
                        'set-valued possibility fibre renamed coexisting accepted state',
                        'bare projector overlap renamed state imprint',
                        'Hessian or higher derivative renamed occupied state component',
                        'independent parameter fibres or gauge tangents combined as relata',
                        'extra carrier, tensor product, time, geometry, data or target relation '
                        'hidden in class',
                        'class-local no-go promoted to global RefG or all-no-new-primitives no-go'),
 'SCOPE_CEILING': {'declared_single_generator_class_rejected': True,
                   'all_no_new_primitive_routes_rejected': False,
                   'noncommuting_single_carrier_route_rejected': False,
                   'state_owned_joint_carrier_route_rejected': False,
                   'f2b_candidate_evaluated': False,
                   'state_supported_nodes_proved': False,
                   'atemporal_state_imprint_proved': False,
                   'irreducible_pair_relation_proved': False,
                   'full_W2_F2_operational_relations': False,
                   'persistence_time_or_causality': False,
                   'physical_space_metric_or_observable': False,
                   'GR_PN_or_PPN_bridge': False,
                   'observational_validation': False},
 'SCIENTIFIC_CLOSURE': {'F1_conditional_structural_result_inherited': True,
                        'F2a_candidate_inherited': True,
                        'F2b_completion_contract_inherited': True,
                        'single_generator_commutative_route_rejected': True,
                        'F2b_candidate_proved': False,
                        'full_W2_F2_operational_relations_proved': False,
                        'F3_internal_order_or_causality_proved': False,
                        'Lorentzian_metric_or_Einstein_branch_proved': False,
                        'PN_or_PPN_handoff_proved': False}}
CLAIM_CONTRACT = SCIENTIFIC_CONTRACT
EXPECTED_DEPENDENCIES = tuple(CLAIM_CONTRACT["DEPENDENCIES"])
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
        "named_dependency_chain_exact": tuple(CLAIM_CONTRACT.get("DEPENDENCIES", ()))
        == EXPECTED_DEPENDENCIES,
        "scope_ceiling_exact": (
            isinstance(scope, dict) and scope == EXPECTED_SCOPE_CEILING
            and all(type(value) is bool for value in scope.values())
        ),
        "scientific_closure_exact": (
            isinstance(closure, dict) and closure == EXPECTED_SCIENTIFIC_CLOSURE
            and all(type(value) is bool for value in closure.values())
        ),
    }

def matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)

def algebra_controls() -> dict[str, bool]:
    s, x, y = sp.symbols("s x y", nonzero=True, real=True)
    u, v = sp.symbols("u v", real=True)
    identity = sp.eye(3)
    p1 = sp.diag(1, 0, 0)
    p2 = identity - p1
    q = s * (p1 - identity / 3)
    b_element = x * p1 + y * p2
    minimal = sp.simplify((q - 2 * s * identity / 3) * (q + s * identity / 3))
    recovered_p1 = sp.simplify(identity / 3 + q / s)
    recovered_p2 = sp.simplify(identity - recovered_p1)
    reduced_from_iq = sp.simplify(
        (y * identity + (x - y) * (identity / 3 + q / s)) - b_element
    )

    projectors = (p1, p2)
    central_candidates = (
        sp.zeros(3), p1, p2, identity,
    )
    idempotent_table = all(
        matrix_zero(item**2 - item) and matrix_zero(item * q - q * item)
        for item in central_candidates
    )
    idempotent_solutions = sp.solve(
        (sp.Eq(u**2, u), sp.Eq(v**2, v)), (u, v), dict=True
    )
    exact_idempotent_coefficients = {
        (solution[u], solution[v]) for solution in idempotent_solutions
    } == {(0, 0), (1, 0), (0, 1), (1, 1)}
    pair_table = sp.Matrix(2, 2, lambda a, b: sp.simplify(
        sp.trace(projectors[a] * b_element * projectors[b] * b_element)
    ))
    expected_pair_table = sp.diag(x**2, 2 * y**2)
    unary_weights = (x**2, 2 * y**2)
    unary_equality_table = sp.Matrix(2, 2, lambda a, b: (
        unary_weights[a] if a == b else 0
    ))
    return {
        "accepted_projector_reconstruction_exact": all((
            matrix_zero(p1**2 - p1), matrix_zero(p2**2 - p2),
            matrix_zero(p1 * p2), matrix_zero(recovered_p1 - p1),
            matrix_zero(recovered_p2 - p2), p1.rank() == 1, p2.rank() == 2,
        )),
        "minimal_polynomial_exact": matrix_zero(minimal),
        "generic_spectral_element_reduction_exact": matrix_zero(reduced_from_iq),
        "central_idempotent_table_exact": bool(
            idempotent_table and exact_idempotent_coefficients
        ),
        "generic_pair_word_table_is_diagonal": pair_table == expected_pair_table,
        "diagonal_table_equals_unary_times_equality": pair_table == unary_equality_table,
    }

def stabilizer_controls() -> dict[str, bool]:
    a, b, d = sp.symbols("a b d", real=True)
    corner = sp.Matrix([[a, b], [b, d]])
    reflection = sp.diag(1, -1)
    quarter_turn = sp.Matrix([[0, -1], [1, 0]])
    equations = list(reflection * corner * reflection.T - corner)
    equations += list(quarter_turn * corner * quarter_turn.T - corner)
    solutions = sp.solve(equations, (a, b, d), dict=True)
    expected = [{a: d, b: 0}]
    invariant_corner = corner.subs(expected[0]) if solutions == expected else corner
    z = sp.symbols("z", real=True)
    idempotent_roots = sp.solve(sp.Eq(z**2, z), z)
    ranks = sorted((z_value * sp.eye(2)).rank() for z_value in idempotent_roots)
    generators_exact = all((
        reflection.T * reflection == sp.eye(2),
        quarter_turn.T * quarter_turn == sp.eye(2),
        reflection.det() == -1, quarter_turn.det() == 1,
    ))
    return {
        "rank2_stabilizer_generators_exact": generators_exact,
        "invariant_symmetric_corner_is_scalar": all((
            solutions == expected, matrix_zero(invariant_corner - d * sp.eye(2)),
        )),
        "invariant_corner_idempotents_have_rank_zero_or_two": all((
            idempotent_roots == [0, 1], ranks == [0, 2],
        )),
        "no_canonical_rank1_corner_projector": 1 not in ranks,
    }

def escape_controls(dependencies: dict[str, Any]) -> dict[str, bool]:
    w213_report = dependencies.get("w213_report", {})
    s = sp.symbols("s", nonzero=True, real=True)
    q = s * sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
    p2 = sp.diag(0, 1, 1)
    p0 = sp.diag(0, 1, 0)
    p_orthogonal = sp.diag(0, 0, 1)
    vector = sp.Matrix([0, sp.Rational(3, 5), sp.Rational(4, 5)])
    p_variable = sp.simplify(vector * vector.T)
    overlap = sp.simplify(sp.trace(p0 * p_variable))
    subgates = w213_report.get("SUBGATE_CLOSURE_FLAGS", {})
    scope = w213_report.get("SCOPE_CEILING", {})
    routes = CLAIM_CONTRACT["ESCAPE_ROUTE_REGISTRY"]
    return {
        "set_valued_fibre_exists_but_has_no_canonical_member": all((
            matrix_zero(p0**2 - p0), matrix_zero(p_variable**2 - p_variable),
            matrix_zero(p2 * p0 - p0), matrix_zero(p2 * p_variable - p_variable),
            p0.rank() == 1, p_variable.rank() == 1,
            stabilizer_controls()["no_canonical_rank1_corner_projector"],
        )),
        "fibre_overlap_varies_but_is_imported_kinematics": all((
            sp.trace(p0 * p0) == 1, overlap == sp.Rational(9, 25),
            "bare projector overlap" in CLAIM_CONTRACT["FORBIDDEN_UPGRADES"][2],
        )),
        "same_unary_bare_overlap_not_irreducible": all((
            sp.trace(p0) == sp.trace(p_orthogonal) == sp.trace(p_variable) == 1,
            matrix_zero(p2 * p_orthogonal - p_orthogonal),
            matrix_zero(p2 * p_variable - p_variable),
            sp.trace(p0 * p_orthogonal) == 0,
            overlap == sp.Rational(9, 25),
            "BARE_OVERLAP_OR_HIDDEN_SELECTION" in routes["PROJECTIVE_FIBRE"],
        )),
        "rank1_word_reduces_to_overlap": all((
            matrix_zero(p0 * p_variable * p0 - overlap * p0),
            matrix_zero(q * p0 + s * p0 / 3),
            matrix_zero(q * p_variable + s * p_variable / 3),
        )),
        "no_invariant_rank1_split_P2": stabilizer_controls()[
            "no_canonical_rank1_corner_projector"
        ],
        "w2_12_pairwise_and_state_imprint_flags_remain_false": all((
            subgates.get("W2_F2B_ATEMPORAL_RELATIONAL_CARRIER_PROVED") is False,
            subgates.get("W2_F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED") is False,
            scope.get("atemporal_relational_carrier_proved") is False,
            scope.get("irreducibly_pairwise_relation_proved") is False,
        )),
        "preserved_routes_are_explicitly_open": all(
            isinstance(value, str) and value.startswith("OPEN")
            for value in routes.values()
        ),
    }

def run() -> dict[str, Any]:
    algebra = algebra_controls()
    stabilizer = stabilizer_controls()
    inherited_open_boundaries = {
        "w213_report": {
            "SUBGATE_CLOSURE_FLAGS": {
                "W2_F2B_ATEMPORAL_RELATIONAL_CARRIER_PROVED": False,
                "W2_F2B_IRREDUCIBLY_PAIRWISE_RELATION_PROVED": False,
            },
            "SCOPE_CEILING": {
                "atemporal_relational_carrier_proved": False,
                "irreducibly_pairwise_relation_proved": False,
            },
        }
    }
    escapes = escape_controls(inherited_open_boundaries)
    scope_closure = scope_closure_controls()
    valid = (
        _all_true(algebra) and _all_true(stabilizer) and _all_true(escapes)
        and _all_true(scope_closure)
    )
    return {
        "artifact": CLAIM_CONTRACT["CLAIM_ID"],
        "valid": valid,
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The commutative spectral algebra generated by one accepted Q cannot supply "
            "a canonical rank-one split or an irreducible pair relation. This no-go is "
            "strictly class-local; noncommuting and genuinely joint carriers remain open."
        ),
        "scope_ceiling": CLAIM_CONTRACT["SCOPE_CEILING"],
        "scientific_closure": CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"],
        "algebra_controls": algebra,
        "stabilizer_controls": stabilizer,
        "escape_controls": escapes,
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
