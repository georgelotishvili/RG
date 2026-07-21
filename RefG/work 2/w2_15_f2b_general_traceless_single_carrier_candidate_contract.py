"""Frozen, outcome-neutral contract for the selected revised W2-F2b candidate.

This file does not claim that F2b or full F2 is proved.  It freezes one abstract
traceless endomorphism A and the two channels derived from A by transpose,

    S=(A+A.T)/2,       R=(A-A.T)/2,

before any candidate outcome is evaluated.  The old F1 state is the exact
R=0 restriction.  The next artifact must revalidate F1 and F2a and then pass
every frozen w2_13 gate in one identity-pinned aggregate candidate.

S and R have no spacetime, material, vortex, pressure or observable meaning
here.  Such interpretations remain later derivation duties.
"""

from __future__ import annotations

import json
from typing import Any

import sympy as sp

SCIENTIFIC_CONTRACT: dict[str, Any] = {'CLAIM_ID': 'W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CONTRACT_001',
 'CLAIM': 'Freeze, without evaluating outcomes, the selected revised one-carrier candidate A=S+R '
          'whose transpose-derived noncommuting channels may supply the state nodes and joint '
          'carrier absent from the exact w2_14 class.',
 'TYPE': 'OUTCOME_NEUTRAL_REVISED_CANDIDATE_CONTRACT',
 'ASSUMPTIONS': 'The exact C0, w2_13 F2b contract and w2_14 scoped no-go are valid.  The new A and '
                'its polynomial law are imported mathematical hypotheses, not derived RefG facts.',
 'DOMAIN': 'A in sl(3,R), S=(A+A^T)/2, R=(A-A^T)/2, alpha,b,c,eta,d>0; the accepted branch and '
           'relational open subset must be derived in w2_16.',
 'CONVENTIONS': 'Real 3x3 endomorphisms, Euclidean internal transpose/trace, common O(3) '
                'conjugation, commutator [S,R]=SR-RS, and no spacetime or physical interpretation.',
 'FREEDOM_LEDGER': {'ambient_dimension': {'source': 'inherited F1 matrix representation',
                                          'allowed_range': 3,
                                          'scale': 'internal representation',
                                          'complexity': 0},
                    'single_carrier_A': {'source': 'new version primitive',
                                         'allowed_range': 'sl(3,R)',
                                         'scale': 'one accepted-state carrier',
                                         'complexity': 8},
                    'transpose_split': {'source': 'derived exact projection',
                                        'allowed_range': 'S plus R',
                                        'scale': 'fixed map',
                                        'complexity': 0},
                    'common_basis_action': {'source': 'inherited internal delta and matrix algebra',
                                            'allowed_range': 'O(3)',
                                            'scale': 'one common action',
                                            'complexity': 0},
                    'inherited_alpha_b_c': {'source': 'exact F1 law',
                                            'allowed_range': 'alpha,b,c>0',
                                            'scale': 'three universal parameters',
                                            'complexity': 3},
                    'new_eta_d': {'source': 'new skew radial law',
                                  'allowed_range': 'eta,d>0',
                                  'scale': 'two universal parameters',
                                  'complexity': 2},
                    'mixed_couplings': {'source': 'candidate architectural zero',
                                        'allowed_range': 0,
                                        'scale': 'all mixed invariant coefficients',
                                        'complexity': 0},
                    'node_maps': {'source': 'transpose projections',
                                  'allowed_range': 'fixed',
                                  'scale': 'S,R',
                                  'complexity': 0},
                    'carrier_map': {'source': 'inherited matrix commutator',
                                    'allowed_range': 'fixed',
                                    'scale': '[S,R]',
                                    'complexity': 0},
                    'joint_report': {'source': 'inherited trace norm',
                                     'allowed_range': 'fixed K and derived tau',
                                     'scale': 'one raw and one normalized scalar',
                                     'complexity': 0},
                    'relative_modulus': {'source': 'accepted-state quotient if proved',
                                         'allowed_range': 'to be derived',
                                         'scale': 'not a fitted parameter',
                                         'complexity': 0},
                    'preferred_basis_axis_or_labels': {'source': 'none',
                                                       'allowed_range': 0,
                                                       'scale': 'description',
                                                       'complexity': 0},
                    'physical_interpretation': {'source': 'none',
                                                'allowed_range': 0,
                                                'scale': 'semantics',
                                                'complexity': 0},
                    'data_fitted_parameters': {'source': 'none',
                                               'allowed_range': 0,
                                               'scale': 'data',
                                               'complexity': 0}},
 'DEPENDENCIES': ['w2_13 F2b completion requirements',
                  'w2_14 single-generator commutative no-go boundary'],
 'METHOD': 'Precommit one candidate identity, complete law, domain, proposed nodes/carrier, '
           'equivalence, nulls, freedom ledger and every downstream proof duty before evaluation.',
 'PASS_CONDITION': 'Named dependencies, definition coherence, outcome neutrality, scope ceiling, '
                   'and closure ledger pass exactly.  This contract cannot pass F2b.',
 'FAIL_CONDITION': 'Any missing freedom, changed law, hidden primitive, physical import, premature '
                   'result flag, dependency drift, or ambiguous common action '
                   'invalidates the freeze.',
 'FALSIFIER': 'A proof that this artifact evaluated a candidate outcome, hid a target, omitted a '
              'candidate freedom or failed to specify a unique downstream object falsifies the '
              'freeze.',
 'RESIDUAL': 'N/A for outcomes; exact zero for contract identities.',
 'ERROR_BOUND': 'N/A; no numerical or observational statement.',
 'VALIDITY_HEALTH': 'Conditional only on the imported abstract A and law.  The separable '
                    'mixed-coupling choice and flat relative modulus are explicit risks that w2_16 '
                    'may reject.',
 'BRANCHES': {'contract': 'DEFINED_IF_EXACT_CONTROLS_PASS',
              'candidate_outcome': 'UNEVALUATED',
              'old_R_zero_restriction': 'DECLARED_REQUIRES_EXACT_CHECK',
              'generic_noncommuting_branch': 'DECLARED_REQUIRES_DERIVATION',
              'commuting_or_zero_branches': 'PREDECLARED_NULLS',
              'flat_relative_modulus': 'OPEN_HEALTH_AND_EQUIVALENCE_GATE',
              'full_c0_f2': 'OPEN'},
 'OBSERVABLE_MAP': {'status': 'N/A', 'reason': 'atemporal internal contract'},
 'FORWARD_MODEL': {'status': 'N/A', 'reason': 'no observable'},
 'DATA_ROLE': {'status': 'N/A', 'reason': 'no data, target or fit'},
 'IDENTIFIABILITY': 'All five law parameters, the exact zero mixed couplings, state algebra, '
                    'common action, node maps, carrier and reports are explicitly enumerated and '
                    'identity-frozen.  No observational or inferential identifiability is claimed.',
 'BENCHMARK': 'w2_14 is the null boundary: deleting R or replacing [S,R] by commutative spectral '
              'repackaging must return the rejected class.',
 'CROSSCHECK': 'Exact transpose decomposition, single-carrier reconstruction, old-law restriction, '
               'outcome neutrality, and a separately evaluated w2_16 candidate.',
 'CANDIDATE_DEFINITION': {'primitive': 'One abstract real traceless endomorphism A in sl(3,R); A '
                                       'is the only new accepted-state primitive in this version.',
                          'derived_channels': 'S=(A+A^T)/2 in Sym_0(3,R) and R=(A-A^T)/2 in so(3); '
                                              'they are exact transpose projections of A, not '
                                              'separately imported fields.',
                          'ambient_algebra': 'The inherited real 3x3 endomorphism algebra with '
                                             'identity, transpose, product and trace; no tensor '
                                             'product, spacetime or external graph is added.',
                          'equivalence': 'One common internal basis change A -> O A O^T for O in '
                                         'O(3), acting simultaneously on S and R.',
                          'old_restriction': 'R=0 and S=Q gives exactly the frozen F1 carrier and '
                                             'law; this is an exact restriction, not automatic '
                                             'proof for the extended accepted branch.',
                          'new_content': 'The skew transpose channel and its two positive law '
                                         'parameters eta,d.  No preferred direction, node labels, '
                                         'pair table or physical interpretation is added.',
                          'semantic_boundary': 'A,S,R are pre-spatial internal algebra objects.  '
                                               'Symmetric and skew do not yet mean pressure, '
                                               'strain, rotation, vortex, matter, geometry or an '
                                               'observable.'},
 'LAW_AND_BRANCH': {'invariants': 'I2=Tr(S^2), I3=Tr(S^3), J=-Tr(R^2)>=0.',
                    'law': 'U(A)=-alpha I2/2-b I3/3+c I2^2/4-eta J/2+d J^2/4.',
                    'parameter_domain': 'alpha,b,c,eta,d>0; no fitted or observed constants.',
                    'accepted_branch': 'Global minima must be derived, not assumed: expected '
                                       'candidate branch has the old uniaxial S amplitude s_+>0, '
                                       'J=eta/d>0, and an unfixed relative orientation.',
                    'relative_modulus': 'The law is separable in S and R, so relative orientation '
                                        'is a candidate flat modulus.  Its legitimacy, stability '
                                        'class and non-gauge status are mandatory w2_16 tests, not '
                                        'conclusions of this contract.',
                    'mixed_coefficients': 'Every mixed invariant coefficient is fixed exactly to '
                                          'zero by this candidate law; this architectural choice '
                                          'is charged and must survive robustness criticism.',
                    'undefined_points': 'U itself is polynomial and defined everywhere.  Only '
                                        'normalized diagnostic relations may be undefined at s=0 '
                                        'or J=0; raw carriers remain defined.'},
 'NODE_AND_CARRIER_ANSATZ': {'symmetric_node': 'Candidate node N_S is the nonzero transpose-even '
                                               'restriction S of the same A.',
                             'skew_node': 'Candidate node N_R is the nonzero transpose-odd '
                                          'restriction R of the same A.',
                             'ownership': 'The proposed ownership certificate is the equivariant '
                                          'projection/reconstruction pair A -> (S,R) and A=S+R; '
                                          'w2_16 must prove that this meets w2_13 rather than '
                                          'merely renaming matrix sectors.',
                             'carrier': 'Candidate joint carrier C=[S,R]=SR-RS, generated by the '
                                        'inherited product from the two coexisting restrictions of '
                                        'one state.',
                             'joint_report': 'Raw report K=Tr(C^T C).  On the proposed nonzero '
                                             'branch the optional normalized report tau=K/(s^2 J) '
                                             'must be derived with its exact domain; no value is '
                                             'preassigned.',
                             'unary_reductions': 'Complete candidate unary data are the separate '
                                                 'O(3)-invariant classes of S and R; on the '
                                                 'accepted branch these reduce to the S spectrum '
                                                 'and J respectively.',
                             'candidate_only_not_result': 'Calling these objects node, carrier and '
                                                          'report is an ansatz.  Every '
                                                          'corresponding proof flag remains false '
                                                          'until the separate exact '
                                                          'evaluation.'},
 'EQUIVALENCE_AND_PAIR_DOMAIN': {'common_action': 'Pairs inherit one diagonal/common O(3) '
                                                  'conjugation from the single endomorphism A.',
                                 'why_not_independent_gauge': 'Independent rotations of S and R do '
                                                              'not preserve their product as '
                                                              'restrictions of one endomorphism '
                                                              'algebra; w2_16 must audit whether '
                                                              'they are global degeneracy motions '
                                                              'or hidden gauge, rather than '
                                                              'deciding this by wording.',
                                 'typed_nodes': 'Transpose parity distinguishes N_S and N_R '
                                                'covariantly; they cannot be exchanged by the '
                                                'declared common O(3) basis action.',
                                 'pair_domain': 'The proposed domain is the two typed same-state '
                                                'nodes and their ordered cross pair; self pairs '
                                                'are reference unary/null controls.',
                                 'relabel_policy': 'No arbitrary labels occur.  Any '
                                                   'representation-level renaming preserving '
                                                   'transpose type and the common action must '
                                                   'leave the reported scalar unchanged.',
                                 'report_invariance_duty': 'w2_16 must prove K and any normalized '
                                                           'quotient invariant under the complete '
                                                           'accepted equivalence, including every '
                                                           'discrete equivalence found in the '
                                                           'audit.'},
 'OPEN_DOMAIN_AND_NULLS': {'predeclared_open_domain': 'alpha,b,c,eta,d>0 and accepted states with '
                                                      'S!=0, R!=0, [S,R]!=0; the generic '
                                                      'relative-orientation interior must be '
                                                      'characterized exactly.',
                           'reference_zero': 'A=0 gives S=R=C=K=0 but need not be an accepted '
                                             'minimum.',
                           'symmetric_only': 'R=0 gives the exact old law restriction and C=K=0.',
                           'skew_only': 'S=0 gives C=K=0.',
                           'commuting_branch': '[S,R]=0 gives C=K=0 and is outside the positive '
                                               'relational domain.',
                           'factorized_pair_rule': 'Any report reconstructed only from separate '
                                                   'unary invariants and typed equality is null.',
                           'projective_bare_overlap': 'A freely selected projector overlap without '
                                                      'state reconstruction remains the w2_14 '
                                                      'null.',
                           'undefined_normalization': 'tau is undefined when s=0 or J=0; no '
                                                      'limiting value may be silently assigned.'},
 'OUTCOME_BLINDNESS': {'candidate_selected_before_outcomes': True,
                       'no_observational_constants': True,
                       'no_target_relation_table': True,
                       'no_spacetime_import': True,
                       'all_result_flags_false': True,
                       'failure_does_not_authorize_patch': True,
                       'new_version_on_revision': True},
 'REVALIDATION_DUTIES': {'exact_old_law_restriction': 'Prove U(S,R=0)=V_F1(S) identically.',
                         'full_extended_f1': 'Derive all global minima, quotient classes, '
                                             'stabilizer and normal/flat Hessian sectors.',
                         'embedded_f2a_operator_family': 'Recompute the extended Hessian and prove '
                                                         'the exact old S-sector F2a family '
                                                         'survives.',
                         'same_aggregate_identity': 'Pin one source identity for the state, law, '
                                                    'nodes, carrier, quotient and all gates.',
                         'new_flat_directions_classified': 'Distinguish common gauge rotations, '
                                                           'independent global degeneracy motions, '
                                                           'physical relative moduli and unstable '
                                                           'directions exactly.',
                         'no_automatic_inheritance': 'The old F1/F2a results are lemmas only; no '
                                                     'extended-state pass is inherited by name.'},
 'F2B_GATE_DUTIES': {'w213_exact_screen_imported': 'Use every exact w2_13 screening key without '
                                                   'deletion.',
                     'state_node_support': 'Prove both proposed nodes coexist and are state/law '
                                           'generated.',
                     'joint_carrier_support': 'Prove [S,R] belongs to the accepted state and links '
                                              'both nodes.',
                     'common_action_and_pair_domain': 'Derive the full action and admissible '
                                                      'pairs.',
                     'same_unary_different_joint': 'Exhibit exact accepted states with equal '
                                                   'complete unary classes and unequal joint '
                                                   'report.',
                     'irreducible_quotient': 'Prove the joint report cannot factor through unary '
                                             'data, typed equality or w2_14 nulls.',
                     'complete_invariance': 'Prove representative and relabelling invariance.',
                     'open_domain_and_nulls': 'Prove nonzero open support and every predeclared '
                                              'null.',
                     'no_f3_semantics': 'Keep formation, persistence, propagation, memory and '
                                        'causality absent.',
                     'candidate_specific_calculation': 'Require the complete exact w2_16 '
                                                       'calculation before any closure.'},
 'FORBIDDEN_UPGRADES': ('candidate contract renamed a proof or full-F2 closure',
                        'S or R imported independently instead of derived from one A',
                        'flat modulus declared physical or stable without exact calculation',
                        'independent channel rotations silently declared gauge or non-gauge',
                        'commutator syntax alone declared irreducible relational content',
                        'normalized tau assigned at s=0 or J=0',
                        'pressure strain vortex matter geometry time memory or observation '
                        'imported',
                        'failed candidate patched in place after seeing outcomes'),
 'SCOPE_CEILING': {'candidate_contract_frozen': True,
                   'candidate_evaluated': False,
                   'new_single_carrier_imported': True,
                   'symmetric_and_skew_channels_derived': True,
                   'old_f1_exact_restriction_declared': True,
                   'f1_revalidated_in_extended_state': False,
                   'f2a_revalidated_in_extended_state': False,
                   'state_supported_nodes_proved': False,
                   'atemporal_state_carrier_proved': False,
                   'irreducible_pair_relation_proved': False,
                   'complete_common_action_proved': False,
                   'flat_relative_modulus_accepted': False,
                   'full_W2_F2_operational_relations': False,
                   'time_memory_or_causality': False,
                   'physical_space_metric_or_observable': False,
                   'GR_PN_or_PPN_bridge': False,
                   'observational_validation': False},
 'SCIENTIFIC_CLOSURE': {'F1_conditional_structural_result_inherited': True,
                        'F2a_candidate_inherited': True,
                        'F2b_completion_contract_inherited': True,
                        'selected_F2b_candidate_contract_defined': True,
                        'F2b_candidate_evaluated': False,
                        'F2b_relational_completion_proved': False,
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

def definition_controls() -> dict[str, bool]:
    entries = sp.symbols("a0:9", real=True)
    a = sp.Matrix(3, 3, entries)
    a = a - sp.trace(a) * sp.eye(3) / 3
    s_matrix = sp.simplify((a + a.T) / 2)
    r_matrix = sp.simplify((a - a.T) / 2)

    alpha, b, c, eta, d = sp.symbols("alpha b c eta d", positive=True)
    q1, q2, q4, q5, q6 = sp.symbols("q1 q2 q4 q5 q6", real=True)
    q = sp.Matrix([
        [q1, q4, q5],
        [q4, q2, q6],
        [q5, q6, -q1 - q2],
    ])
    q_i2 = sp.trace(q**2)
    q_i3 = sp.trace(q**3)
    zero_r = sp.zeros(3)
    q_j = -sp.trace(zero_r**2)
    restricted_law = (
        -alpha * q_i2 / 2 - b * q_i3 / 3 + c * q_i2**2 / 4
        - eta * q_j / 2 + d * q_j**2 / 4
    )
    exact_old_q_law = -alpha * q_i2 / 2 - b * q_i3 / 3 + c * q_i2**2 / 4
    restricted = sp.simplify(restricted_law - exact_old_q_law)

    x, y, z = sp.symbols("x y z", real=True)
    prototype_r = sp.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    prototype_j = sp.simplify(-sp.trace(prototype_r**2))
    prototype_s = sp.diag(2, -1, -1)
    commutator = sp.simplify(prototype_s * prototype_r - prototype_r * prototype_s)

    return {
        "transpose_split_exact": all((
            matrix_zero(a - s_matrix - r_matrix),
            matrix_zero((s_matrix + r_matrix) - a),
        )),
        "channels_have_required_symmetry_and_trace": all((
            matrix_zero(s_matrix.T - s_matrix),
            matrix_zero(r_matrix.T + r_matrix),
            sp.simplify(sp.trace(s_matrix)) == 0,
            sp.simplify(sp.trace(r_matrix)) == 0,
        )),
        "single_carrier_reconstruction_exact": matrix_zero(a - (s_matrix + r_matrix)),
        "old_law_restriction_exact": restricted == 0,
        "skew_invariant_nonnegative_prototype": prototype_j == 2 * (x**2 + y**2 + z**2),
        "candidate_parameter_domain_open": (
            CLAIM_CONTRACT["LAW_AND_BRANCH"]["parameter_domain"]
            == "alpha,b,c,eta,d>0; no fitted or observed constants."
        ),
        "commutator_report_joint_not_unary_syntax": all((
            not matrix_zero(commutator),
            "[S,R]" in CLAIM_CONTRACT["NODE_AND_CARRIER_ANSATZ"]["carrier"],
            "Tr(C^T C)" in CLAIM_CONTRACT["NODE_AND_CARRIER_ANSATZ"]["joint_report"],
        )),
        "all_candidate_outcomes_false": all(
            value is False
            for key, value in CLAIM_CONTRACT["SCOPE_CEILING"].items()
            if key not in {
                "candidate_contract_frozen", "new_single_carrier_imported",
                "symmetric_and_skew_channels_derived", "old_f1_exact_restriction_declared",
            }
        ),
    }

def run() -> dict[str, Any]:
    controls = definition_controls()
    scope_closure = scope_closure_controls()
    return {
        "artifact": CLAIM_CONTRACT["CLAIM_ID"],
        "valid": _all_true(controls) and _all_true(scope_closure),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The traceless carrier A=S+R and its imported polynomial law are defined "
            "without evaluating their F2b outcome. F1/F2a revalidation, nulls, common "
            "action and irreducibility remain explicit duties."
        ),
        "scope_ceiling": CLAIM_CONTRACT["SCOPE_CEILING"],
        "scientific_closure": CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"],
        "controls": controls,
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
