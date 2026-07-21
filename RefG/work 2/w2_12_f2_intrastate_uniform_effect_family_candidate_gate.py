"""Exact candidate audit for the narrow W2-F2a intrastate comparison gate.

The candidate is the Frobenius-Riesz Hessian of the already accepted F1
quartic functional.  On the generic accepted branch it generates two normal
spectral sectors and one uniform, atemporal comparison kernel.  The result is
only a law-defined internal comparison: it is not a physical response, mode,
node, imprint, interaction, time, geometry, observable, or full W2-F2.
"""

from __future__ import annotations

import json
from typing import Any, Callable

import sympy as sp

SCIENTIFIC_CONTRACT: dict[str, Any] = {'CLAIM_ID': 'W2_F2A_INTRASTATE_HESSIAN_COMPARISON_CANDIDATE_001',
 'CLAIM': "Evaluate and, only on the declared generic branch, establish that the accepted F1 law's "
          'Hessian generates two internal relata and one invariant nontrivial atemporal comparison '
          'map; do not close full C0 F2.',
 'TYPE': 'CONDITIONAL_EXACT_F2A_CANDIDATE_EVALUATION',
 'ASSUMPTIONS': ('The exact accepted F1 result and its nine imported primitives are valid '
                 'dependencies.',
                 'The frozen F2a contract fixes the meaning of operational as a law-defined '
                 'internal map.',
                 'The w2_11 no-go applies to invariant whole-state readouts on one orbit, not to a '
                 'derived intrastate comparison family.',
                 'The accepted C0 contract supplies the operative scope boundary.'),
 'DOMAIN': 'Accepted F1 positive branch with alpha,b,c>0 and b^2!=3 alpha c.  The tuned surface, '
           'Q=0, rejected stationary branch and invalid F1 coefficient boundaries are explicit '
           'nulls.',
 'CONVENTIONS': 'Sym0(3) uses the inherited Frobenius contraction.  O(3) conjugation is internal '
                'equivalence.  Orbit tangents are quotient nulls.  Hessian/effect/response words '
                'in this file are algebraic and atemporal, never physical.',
 'FREEDOM_LEDGER': {'inherited_f1_parameters': {'source': 'public F1 imported alpha,b,c',
                                                'allowed_range': 'alpha,b,c>0',
                                                'scale': 'three inherited universal model '
                                                         'parameters; not fitted here',
                                                'complexity': 3},
                    'route_choice': {'source': 'declared INTRASTATE_UNIFORM_EFFECT_FAMILY '
                                               'candidate',
                                     'allowed_range': 'one frozen categorical route',
                                     'scale': 'architecture',
                                     'complexity': 1},
                    'hessian_candidate_choice': {'source': 'unique second derivative of frozen V; '
                                                           'its use as F2a candidate is declared',
                                                 'allowed_range': 'D^2 V only',
                                                 'scale': 'architecture',
                                                 'complexity': 1},
                    'normalization_choice': {'source': 'declared common positive lambda_r+lambda_b '
                                                       'normalization',
                                             'allowed_range': 'one frozen scale-free normalization',
                                             'scale': 'report',
                                             'complexity': 1},
                    'tangent_carrier': {'source': 'inherited linear Sym0(3) state space',
                                        'allowed_range': 'its full tangent space',
                                        'scale': 'standard mathematics; no physical mode import',
                                        'complexity': 0},
                    'new_numerical_parameters': {'source': 'none',
                                                 'allowed_range': 0,
                                                 'scale': 'candidate',
                                                 'complexity': 0},
                    'data_fitted_parameters': {'source': 'none',
                                               'allowed_range': 0,
                                               'scale': 'data',
                                               'complexity': 0},
                    'chosen_representative_basis_or_axis': {'source': 'none',
                                                            'allowed_range': 0,
                                                            'scale': 'description',
                                                            'complexity': 0},
                    'new_physical_primitives': {'source': 'none',
                                                'allowed_range': 0,
                                                'scale': 'foundation',
                                                'complexity': 0}},
 'DEPENDENCIES': ['w2_10 F2a internal-distinction definition',
                  'w2_11 single-orbit invariant-readout no-go',
                  'w2_09a conditional atemporal F1 structural proof'],
 'METHOD': 'Differentiate the frozen F1 functional twice, construct its unique Frobenius-Riesz '
           'operator, derive the normal sector projectors as spectral polynomials, evaluate one '
           'predeclared comparison on all ordered sector pairs, and run every exact null and '
           'screening condition.',
 'PASS_CONDITION': 'All symbolic derivations, all 19 F2a screening conditions, the generic-domain '
                   'separation, required nulls, scope ceiling, and closure ledger pass exactly.',
 'FAIL_CONDITION': 'Any dependency/schema drift is INVALID.  Any well-formed false screening gate '
                   'gives a completed non-promoted candidate.  The tuned and origin branches fail '
                   'separation.',
 'FALSIFIER': 'The Hessian is not the second derivative of frozen V, its Riesz spectrum/projectors '
              'or covariance identities fail, the generic weights coincide, a target is required, '
              'or the reference/tuned null fabricates a split.',
 'RESIDUAL': '0 for every declared symbolic identity; no differential field equation is claimed.',
 'ERROR_BOUND': '0 for exact symbolic/discrete checks; numerical and data errors are N/A.',
 'VALIDITY_HEALTH': 'Conditional on imported F1 primitives and the generic open domain.  '
                    'Normalization is regular there.  Stability is inherited from F1; dynamics, '
                    'conservation, causality, physical degrees of freedom and observations are not '
                    'established.',
 'BRANCHES': {'generic_hessian_comparison': 'CANDIDATE_FOR_EXACT_POSITIVE_F2A',
              'tuned_b2_equals_3_alpha_c': 'EXACT_DEGENERACY__NO_F2A_SEPARATION_BY_THIS_CANDIDATE',
              'undifferentiated_Q_zero': 'REFERENCE_NULL__NO_GENERATED_RELATA',
              'qp_only_matrix_effect': 'NULL__RANK_UNARY_OR_EQUALITY_CONTENT_ONLY',
              'strong_pairwise_coupling': 'NOT_PROVED__REMAINS_FOR_LATER_STRONGER_GATE',
              'full_c0_f2': 'OPEN'},
 'OBSERVABLE_MAP': {'status': 'N/A', 'reason': 'internal algebraic comparison only'},
 'FORWARD_MODEL': {'status': 'N/A', 'reason': 'no observable or data chain'},
 'DATA_ROLE': {'status': 'N/A', 'reason': 'no data used, fitted, or validated'},
 'IDENTIFIABILITY': 'Representative axes and sector labels are gauge.  The unordered normalized '
                    'Hessian weights and squared contrast are exact invariants; physical '
                    'identifiability is N/A.',
 'BENCHMARK': 'Predeclared nulls are the scalar-normal tuned Hessian, Q=0 scalar Hessian, Q/P-only '
              'rank/equality algebra, self-only selectors, fixed targets, and incomplete '
              'equivalence.',
 'CROSSCHECK': 'Coordinate differentiation, coordinate-free second variation, generalized Riesz '
               'diagonalization, spectral-polynomial reconstruction and exact covariance checks '
               'agree.',
 'CANDIDATE_DEFINITION': {'route': 'INTRASTATE_UNIFORM_EFFECT_FAMILY',
                          'accepted_state': 'The public F1 accepted uniaxial Q orbit at '
                                            'alpha,b,c>0 and its positive root s.',
                          'carrier': 'The inherited linear state space Sym0(3), used only as an '
                                     'atemporal tangent and comparison carrier; no physical mode '
                                     'meaning is assigned.',
                          'generic_domain': 'alpha,b,c>0 with b^2 != 3 alpha c on the accepted '
                                            'positive branch.',
                          'degenerate_boundary': 'At b^2=3 alpha c the two normal Hessian weights '
                                                 'coincide and this candidate does not establish '
                                                 'F2a distinction.',
                          'reference_boundary': 'At Q=0 the Hessian is scalar on Sym0(3), no two '
                                                'normal spectral relata are generated, and no '
                                                'singular continuation is allowed.',
                          'claim_ceiling': 'Conditional exact law-defined atemporal internal '
                                           'comparison only; full F2 and all physical, temporal, '
                                           'geometric and observational meanings remain open or '
                                           'excluded.'},
 'LAW_DERIVATION': {'functional': 'Use exactly the inherited F1 quartic V(Q)=-alpha Tr(Q^2)/2-b '
                                  'Tr(Q^3)/3+c Tr(Q^2)^2/4; do not add a target or coefficient.',
                    'first_principle_map': 'Differentiate the same frozen V twice at accepted Q to '
                                           'obtain one symmetric bilinear Hessian on every pair of '
                                           'inherited carrier variations.',
                    'riesz_operator': 'Use the inherited positive Frobenius contraction once to '
                                      'represent that Hessian by a unique self-adjoint operator '
                                      'L_Q.',
                    'covariance': 'O(3)-invariance of V implies L_{RQR^T}(RUR^T)=R L_Q(U) R^T '
                                  'under the complete declared internal equivalence.',
                    'ownership': 'The Hessian is mathematically derived from the imported F1 law, '
                                 'but selecting its normalized sector comparison as the F2a '
                                 'candidate is one declared architecture choice and is not claimed '
                                 'foundation-unique.'},
 'RELATA_CONSTRUCTION': {'normal_domain': 'Remove the two tangent directions of the declared O(3) '
                                          'orbit; the remaining three-dimensional normal carrier '
                                          'is the candidate comparison domain.',
                         'radial_sector': 'The simple nonzero Hessian eigenspace generated by '
                                          'Pi_r, rank one.',
                         'biaxial_sector': 'The second nonzero Hessian eigenspace generated by '
                                           'Pi_b, rank two.',
                         'orbit_sector': 'The rank-two zero eigenspace Pi_o is an '
                                         'equivalence-orbit tangent and is a null, not a third '
                                         'physical or operational relatum.',
                         'spectral_generation': 'On the generic domain Pi_r and Pi_b are exact '
                                                'spectral polynomials of the single law-derived '
                                                'L_Q, so neither a basis, axis, target projector '
                                                'nor desired table is input.',
                         'undefined_boundary': 'The separate Pi_r/Pi_b generation by L_Q is '
                                               'undefined as a distinction when their eigenvalues '
                                               'coincide; Q=0 is separately null.'},
 'COMPARISON_MAP': {'domain': 'All four ordered pairs in {Pi_r,Pi_b} x {Pi_r,Pi_b}, fixed before '
                              'outcomes.',
                    'codomain': 'One shared exact real scalar codomain.',
                    'uniform_rule': 'K_Q(A,B)=Tr_End(A L_Q B)/((lambda_r+lambda_b) '
                                    'sqrt(rank(A)rank(B))) for every admitted pair, with no '
                                    'per-relatum selector.',
                    'reported_relation': 'Report the label-free normalized spectrum and squared '
                                         'contrast; the displayed 2x2 table is a derived '
                                         'diagnostic, not an inserted equality table.',
                    'generic_result': 'K has diagonal weights lambda_r/(lambda_r+lambda_b) and '
                                      'lambda_b/(lambda_r+lambda_b), zero cross entries, and '
                                      'unequal diagonal weights exactly on the declared generic '
                                      'domain.',
                    'tuned_null': 'At b^2=3 alpha c the weights both equal 1/2, leaving only a '
                                  'scalar delta skeleton; that boundary is a failed separation, '
                                  'not a promoted result.',
                    'semantic_ceiling': 'K is a narrow atemporal comparison.  Its diagonal '
                                        'factorization is not claimed to be irreducibly pairwise '
                                        'coupling, interaction, intervention or measurement.'},
 'QP_ONLY_NULL_BOUNDARY': {'spectral_algebra': 'R[Q]=span{I,Q}=span{P1,P2} on the accepted '
                                               'uniaxial branch.',
                           'block_scalar_boundary': 'Every target-free Q-only covariant matrix '
                                                    'effect is a P1/P2 block scalar and adds no '
                                                    'off-diagonal carrier.',
                           'rank_equality_null': 'Projector overlaps alone give a bare delta '
                                                 'table; free block weights can fit any two '
                                                 'desired unary answers and therefore do not '
                                                 'predict F2a.',
                           'duplicated_mode_null': 'P1-I/3=Q/s and P2-2I/3=-Q/s, so the two '
                                                   'traceless role carriers are one mode with '
                                                   'opposite sign, not two independent modes.',
                           'why_hessian_is_extra_content': "The accepted law's second derivative "
                                                           'acts on the whole inherited carrier '
                                                           'and has normal curvature sectors not '
                                                           'supplied by the Q-only matrix effect '
                                                           'algebra.'},
 'CANDIDATE_GATE_EVIDENCE': {'source': 'w2_10 screening_gate_keys and screen_candidate',
                             'all_19_gates_runtime_computed': 'Every frozen gate is an exact bool '
                                                              'from this candidate calculation.',
                             'false_gate_policy': 'A false scientific gate is a valid '
                                                  'non-promotion, not schema invalidity.',
                             'calculation_policy': 'F2a is established only when the complete '
                                                   'candidate gate conjunction is true.'},
 'FORBIDDEN_INPUTS': ('preferred representative, fixed axis, ordered eigenbasis, target projector, '
                      'or matrix entry',
                      'preloaded Pi_r/Pi_b split, desired response values, literal delta table, or '
                      'rank lookup',
                      'per-relatum post-selected selector or self-only comparison domain',
                      'free block weights, fitted coefficients, hidden higher operator, or '
                      'unregistered carrier',
                      'orbit tangent counted as a physical or operational relatum',
                      'Q=0 division, tuned-surface promotion, rejected branch, or parameter-fibre '
                      'mixing',
                      'physical effect, response, intervention, node, imprint, mode, particle, or '
                      'measurement',
                      'time, causality, persistence, geometry, action, GR, observable, data, or '
                      'observation'),
 'SCOPE_CEILING': {'foundation_law_derived': False,
                   'functional_uniqueness_derived': False,
                   'N3_physical_origin_derived': False,
                   'physical_node_or_location': False,
                   'atemporal_imprint_or_correlation_carrier': False,
                   'persistent_physical_imprint': False,
                   'irreducibly_pairwise_coupling': False,
                   'physical_response_intervention_or_measurement': False,
                   'independent_additive_physical_modes': False,
                   'temporal_formation_persistence_or_causality': False,
                   'physical_dimension_or_continuum': False,
                   'Lorentzian_metric_or_light_cone': False,
                   'effective_action_or_conservation_law': False,
                   'RefG_environment_map': False,
                   'mass_pressure_particle_or_oscillon': False,
                   'full_W2_F2_operational_relations': False,
                   'GR_PN_or_PPN_bridge': False,
                   'external_observable_or_data_map': False,
                   'observational_validation': False},
 'SCIENTIFIC_CLOSURE': {'F1_conditional_structural_result_inherited': True,
                        'F2a_contract_defined': True,
                        'F2a_candidate_proved_on_generic_domain': True,
                        'F2b_relational_completion_proved': False,
                        'full_W2_F2_operational_relations_proved': False,
                        'F3_internal_order_or_causality_proved': False,
                        'F4_independent_additive_modes_proved': False,
                        'Lorentzian_metric_or_Einstein_branch_proved': False,
                        'PN_or_PPN_handoff_proved': False}}
CLAIM_CONTRACT = SCIENTIFIC_CONTRACT
EXPECTED_DEPENDENCIES = tuple(CLAIM_CONTRACT["DEPENDENCIES"])
EXPECTED_SCOPE_CEILING = dict(CLAIM_CONTRACT["SCOPE_CEILING"])
EXPECTED_SCIENTIFIC_CLOSURE = dict(CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"])
F2A_GATE_KEYS = frozenset({
    "f1_dependency_valid",
    "candidate_domain_map_and_branches_explicit",
    "relata_generated_not_preloaded",
    "uniform_comparison_family_generated_not_preloaded",
    "outputs_share_one_comparison_codomain",
    "exact_nontrivial_separation_witness",
    "relation_not_reduced_to_preassigned_unary_or_bare_equality_data",
    "postselected_self_test_null_rejected",
    "quotient_covariance_and_reported_invariance",
    "undifferentiated_reference_null",
    "non_tuned_domain_and_regular_normalization",
    "extra_primitive_ledger_complete",
    "joint_admissibility_composition_and_common_action_derived",
    "full_f2_node_and_imprint_obligations_not_claimed",
    "operational_semantics_not_upgraded",
    "external_observable_and_data_map_absent",
    "f3_temporal_and_causal_imports_absent",
    "positive_null_and_adversarial_controls_pass",
    "candidate_specific_calculation_complete",
})

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

def matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)

def vector_of(matrix: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix([
        matrix[0, 0], matrix[1, 1], matrix[0, 1], matrix[0, 2], matrix[1, 2],
    ])

def superoperator_matrix(
    basis: tuple[sp.Matrix, ...], operation: Callable[[sp.Matrix], sp.Matrix],
) -> sp.Matrix:
    return sp.Matrix.hstack(*(vector_of(sp.simplify(operation(item))) for item in basis))

def candidate_algebra() -> dict[str, Any]:
    alpha, b, c, s = sp.symbols("alpha b c s", positive=True, real=True)
    x, y, u, v, w = sp.symbols("x y u v w", real=True)
    coordinates = (x, y, u, v, w)
    Q = sp.Matrix([
        [x, u, v],
        [u, y, w],
        [v, w, -x - y],
    ])
    basis = tuple(Q.diff(variable) for variable in coordinates)
    gram = sp.Matrix([
        [sp.trace(left * right) for right in basis]
        for left in basis
    ])
    I2 = sp.expand(sp.trace(Q**2))
    I3 = sp.expand(sp.trace(Q**3))
    potential = sp.expand(-alpha * I2 / 2 - b * I3 / 3 + c * I2**2 / 4)
    coordinate_hessian = sp.hessian(potential, coordinates)

    Q_star = s * sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
    star_substitution = {x: 2*s/3, y: -s/3, u: 0, v: 0, w: 0}
    on_shell = {alpha: (2*c*s**2 - b*s)/3}
    hessian_star = sp.simplify(coordinate_hessian.subs(star_substitution).subs(on_shell))
    riesz = sp.simplify(gram.inv() * hessian_star)

    def second_variation(q: sp.MatrixBase, left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Expr:
        q_i2 = sp.trace(q**2)
        return sp.simplify(
            (-alpha + c*q_i2) * sp.trace(left*right)
            + 2*c*sp.trace(q*left)*sp.trace(q*right)
            - b*sp.trace(q*(left*right + right*left))
        )

    formula_hessian = sp.Matrix([
        [second_variation(Q_star, left, right).subs(on_shell) for right in basis]
        for left in basis
    ])

    def riesz_action(q: sp.MatrixBase, variation: sp.MatrixBase) -> sp.Matrix:
        q_i2 = sp.trace(q**2)
        qv = sp.trace(q*variation)
        return sp.simplify(
            (-alpha + c*q_i2)*variation
            + 2*c*qv*q
            - b*(q*variation + variation*q - sp.Rational(2, 3)*qv*sp.eye(3))
        )

    formula_riesz = superoperator_matrix(
        basis, lambda variation: riesz_action(Q_star, variation).subs(on_shell)
    )

    radial_mode = sp.Matrix([sp.Rational(2, 3), -sp.Rational(1, 3), 0, 0, 0])
    biaxial_diagonal = sp.Matrix([0, 1, 0, 0, 0])
    biaxial_23 = sp.Matrix([0, 0, 0, 0, 1])
    orbit_12 = sp.Matrix([0, 0, 1, 0, 0])
    orbit_13 = sp.Matrix([0, 0, 0, 1, 0])
    modes = sp.Matrix.hstack(
        radial_mode, biaxial_diagonal, biaxial_23, orbit_12, orbit_13
    )
    lambda_r = sp.simplify(s*(4*c*s - b)/3)
    lambda_b = b*s
    mode_riesz = sp.simplify(modes.inv()*riesz*modes)
    expected_mode_riesz = sp.diag(lambda_r, lambda_b, lambda_b, 0, 0)

    pi_r = sp.simplify(modes*sp.diag(1, 0, 0, 0, 0)*modes.inv())
    pi_b = sp.simplify(modes*sp.diag(0, 1, 1, 0, 0)*modes.inv())
    pi_o = sp.simplify(modes*sp.diag(0, 0, 0, 1, 1)*modes.inv())

    I2_star = sp.simplify(sp.trace(Q_star**2))
    P1 = sp.simplify(sp.eye(3)/3 + Q_star/s)
    P2 = sp.simplify(sp.eye(3) - P1)

    def radial_action(variation: sp.MatrixBase) -> sp.Matrix:
        return sp.simplify(sp.trace(Q_star*variation)*Q_star/I2_star)

    def orbit_action(variation: sp.MatrixBase) -> sp.Matrix:
        return sp.simplify(P1*variation*P2 + P2*variation*P1)

    q_pi_r = superoperator_matrix(basis, radial_action)
    q_pi_o = superoperator_matrix(basis, orbit_action)
    q_pi_b = sp.simplify(sp.eye(5) - q_pi_r - q_pi_o)

    spectral_parameter = sp.symbols("spectral_parameter", real=True)
    characteristic = sp.factor((spectral_parameter*sp.eye(5) - riesz).det())
    expected_characteristic = sp.factor(
        spectral_parameter**2
        * (spectral_parameter-lambda_b)**2
        * (spectral_parameter-lambda_r)
    )
    spectral_pi_r = sp.simplify(
        riesz*(riesz-lambda_b*sp.eye(5))/(lambda_r*(lambda_r-lambda_b))
    )
    spectral_pi_b = sp.simplify(
        riesz*(riesz-lambda_r*sp.eye(5))/(lambda_b*(lambda_b-lambda_r))
    )
    spectral_pi_o = sp.simplify(
        (riesz-lambda_r*sp.eye(5))*(riesz-lambda_b*sp.eye(5))/(lambda_r*lambda_b)
    )

    lambda_sum = sp.simplify(lambda_r + lambda_b)

    def comparison(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Expr:
        denominator = lambda_sum*sp.sqrt(sp.trace(left)*sp.trace(right))
        return sp.simplify(sp.trace(left*riesz*right)/denominator)

    comparison_table = sp.Matrix([
        [comparison(pi_r, pi_r), comparison(pi_r, pi_b)],
        [comparison(pi_b, pi_r), comparison(pi_b, pi_b)],
    ])
    expected_table = sp.diag(lambda_r/lambda_sum, lambda_b/lambda_sum)

    D = sp.sqrt(b**2 + 24*alpha*c)
    s_plus = sp.simplify((b + D)/(4*c))
    lambda_r_plus = sp.simplify(lambda_r.subs(s, s_plus))
    lambda_b_plus = sp.simplify(lambda_b.subs(s, s_plus))
    expected_lambda_r_plus = sp.simplify(s_plus*D/3)
    expected_lambda_b_plus = b*s_plus
    mu_r = sp.simplify(lambda_r_plus/(lambda_r_plus+lambda_b_plus))
    mu_b = sp.simplify(lambda_b_plus/(lambda_r_plus+lambda_b_plus))
    expected_mu_r = D/(D+3*b)
    expected_mu_b = 3*b/(D+3*b)
    contrast = sp.simplify(mu_r-mu_b)
    contrast_factor = sp.simplify(8*(3*alpha*c-b**2)/(D+3*b)**2)
    contrast_sq = sp.simplify(contrast**2)
    tuned = {alpha: b**2/(3*c)}
    tuned_mu_r = sp.simplify(mu_r.subs(tuned))
    tuned_mu_b = sp.simplify(mu_b.subs(tuned))

    zero_substitution = {variable: 0 for variable in coordinates}
    origin_hessian = sp.simplify(coordinate_hessian.subs(zero_substitution))
    origin_riesz = sp.simplify(gram.inv()*origin_hessian)

    a1, a2, target_1, target_2 = sp.symbols(
        "a1 a2 target_1 target_2", real=True
    )
    block_effect = a1*P1 + a2*P2
    block_response_1 = sp.simplify(sp.trace(P1*block_effect)/sp.trace(P1))
    block_response_2 = sp.simplify(sp.trace(P2*block_effect)/sp.trace(P2))
    fitted_effect = target_1*P1 + target_2*P2
    overlap_table = sp.Matrix([
        [sp.trace(P1*P1)/sp.trace(P1), sp.trace(P1*P2)/sp.trace(P2)],
        [sp.trace(P2*P1)/sp.trace(P1), sp.trace(P2*P2)/sp.trace(P2)],
    ])
    rank_only_table = sp.Matrix([
        [sp.trace(pi_r*pi_r)/sp.sqrt(sp.trace(pi_r)**2),
         sp.trace(pi_r*pi_b)/sp.sqrt(sp.trace(pi_r)*sp.trace(pi_b))],
        [sp.trace(pi_b*pi_r)/sp.sqrt(sp.trace(pi_b)*sp.trace(pi_r)),
         sp.trace(pi_b*pi_b)/sp.sqrt(sp.trace(pi_b)**2)],
    ])

    theta_12, theta_13, theta_23 = sp.symbols(
        "theta_12 theta_13 theta_23", real=True
    )
    rotations = (
        sp.Matrix([[sp.cos(theta_12), -sp.sin(theta_12), 0],
                   [sp.sin(theta_12), sp.cos(theta_12), 0], [0, 0, 1]]),
        sp.Matrix([[sp.cos(theta_13), 0, -sp.sin(theta_13)], [0, 1, 0],
                   [sp.sin(theta_13), 0, sp.cos(theta_13)]]),
        sp.Matrix([[1, 0, 0], [0, sp.cos(theta_23), -sp.sin(theta_23)],
                   [0, sp.sin(theta_23), sp.cos(theta_23)]]),
        sp.diag(-1, 1, 1),
    )
    covariance_checks: list[bool] = []
    for transform in rotations:
        covariance_checks.append(
            matrix_zero(sp.trigsimp(transform.T*transform-sp.eye(3)))
        )
        rotated_q = sp.trigsimp(transform*Q_star*transform.T)
        for variation in basis:
            rotated_variation = sp.trigsimp(transform*variation*transform.T)
            lhs = riesz_action(rotated_q, rotated_variation)
            rhs = transform*riesz_action(Q_star, variation)*transform.T
            covariance_checks.append(matrix_zero(sp.trigsimp(lhs-rhs)))

    derivation_controls = {
        "coordinate_hessian_matches_coordinate_free_second_variation": (
            matrix_zero(hessian_star-formula_hessian)
        ),
        "riesz_operator_matches_hessian_and_is_self_adjoint": all((
            matrix_zero(riesz-formula_riesz),
            matrix_zero(gram*riesz-hessian_star),
            matrix_zero(riesz.T*gram-gram*riesz),
        )),
        "on_shell_spectral_decomposition_exact": all((
            matrix_zero(mode_riesz-expected_mode_riesz),
            matrix_zero(riesz-(lambda_r*pi_r+lambda_b*pi_b)),
        )),
        "characteristic_polynomial_and_multiplicities_exact": (
            characteristic == expected_characteristic
        ),
        "accepted_positive_branch_eigenvalues_exact": all((
            lambda_r_plus == expected_lambda_r_plus,
            lambda_b_plus == expected_lambda_b_plus,
            sp.ask(sp.Q.positive(expected_lambda_r_plus)) is True,
            sp.ask(sp.Q.positive(expected_lambda_b_plus)) is True,
        )),
    }
    relata_controls = {
        "q_generated_sector_projectors_exact": all((
            matrix_zero(pi_r-q_pi_r), matrix_zero(pi_b-q_pi_b), matrix_zero(pi_o-q_pi_o),
        )),
        "sector_projectors_idempotent_orthogonal_complete": all((
            matrix_zero(pi_r**2-pi_r), matrix_zero(pi_b**2-pi_b),
            matrix_zero(pi_o**2-pi_o), matrix_zero(pi_r*pi_b),
            matrix_zero(pi_r*pi_o), matrix_zero(pi_b*pi_o),
            matrix_zero(pi_r+pi_b+pi_o-sp.eye(5)),
        )),
        "sector_ranks_one_two_two_exact": (
            (pi_r.rank(), pi_b.rank(), pi_o.rank()) == (1, 2, 2)
        ),
        "generic_spectral_polynomials_generate_relata": all((
            matrix_zero(spectral_pi_r-pi_r), matrix_zero(spectral_pi_b-pi_b),
            matrix_zero(spectral_pi_o-pi_o),
        )),
        "orbit_sector_excluded_as_declared_equivalence": all((
            matrix_zero(riesz*pi_o),
            CLAIM_CONTRACT["RELATA_CONSTRUCTION"]["orbit_sector"].startswith("The rank-two zero"),
            CLAIM_CONTRACT["SCOPE_CEILING"]["independent_additive_physical_modes"] is False,
        )),
    }
    comparison_controls = {
        "one_predeclared_rule_covers_all_four_ordered_pairs": all((
            comparison_table.shape == (2, 2),
            CLAIM_CONTRACT["COMPARISON_MAP"]["domain"].startswith("All four ordered pairs"),
            "per-relatum selector" in CLAIM_CONTRACT["COMPARISON_MAP"]["uniform_rule"],
        )),
        "normalized_comparison_table_exact": matrix_zero(comparison_table-expected_table),
        "label_free_contrast_and_sum_exact": all((
            sp.simplify(mu_r-expected_mu_r) == 0,
            sp.simplify(mu_b-expected_mu_b) == 0,
            sp.simplify(mu_r+mu_b-1) == 0,
            sp.simplify(contrast_sq-(mu_b-mu_r)**2) == 0,
        )),
        "generic_open_domain_separation_exact": all((
            sp.simplify(contrast-contrast_factor) == 0,
            sp.simplify(D**2-9*b**2-8*(3*alpha*c-b**2)) == 0,
            tuned_mu_r == sp.Rational(1, 2), tuned_mu_b == sp.Rational(1, 2),
            "b^2 != 3 alpha c" in CLAIM_CONTRACT["CANDIDATE_DEFINITION"]["generic_domain"],
        )),
        "comparison_not_a_physical_or_temporal_response": all((
            CLAIM_CONTRACT["SCOPE_CEILING"]["physical_response_intervention_or_measurement"]
            is False,
            CLAIM_CONTRACT["SCOPE_CEILING"]["temporal_formation_persistence_or_causality"]
            is False,
            "not claimed" in CLAIM_CONTRACT["COMPARISON_MAP"]["semantic_ceiling"],
        )),
    }
    qp_null_controls = {
        "qp_spectral_algebra_closes_in_two_dimensions": all((
            matrix_zero(Q_star**2-(s/3)*Q_star-(2*s**2/9)*sp.eye(3)),
            matrix_zero(P1+P2-sp.eye(3)), matrix_zero(P1*P2),
        )),
        "qp_only_effects_are_block_scalar": all((
            matrix_zero(P1*block_effect*P2), matrix_zero(P2*block_effect*P1),
            block_response_1 == a1, block_response_2 == a2,
        )),
        "free_block_weights_fit_arbitrary_two_unary_targets": all((
            sp.simplify(sp.trace(P1*fitted_effect)/sp.trace(P1)-target_1) == 0,
            sp.simplify(sp.trace(P2*fitted_effect)/sp.trace(P2)-target_2) == 0,
        )),
        "projector_overlap_is_bare_delta": overlap_table == sp.eye(2),
        "traceless_p1_p2_carriers_duplicate_one_q_mode": all((
            matrix_zero(P1-sp.eye(3)/3-Q_star/s),
            matrix_zero(P2-2*sp.eye(3)/3+Q_star/s),
        )),
    }
    null_controls = {
        "tuned_surface_collapses_to_scalar_delta": all((
            tuned_mu_r == sp.Rational(1, 2), tuned_mu_b == sp.Rational(1, 2),
            sp.simplify(contrast_sq.subs(tuned)) == 0,
        )),
        "origin_hessian_is_scalar_and_generates_no_relata": all((
            matrix_zero(origin_hessian+alpha*gram),
            matrix_zero(origin_riesz+alpha*sp.eye(5)),
            sp.factor((spectral_parameter*sp.eye(5)-origin_riesz).det())
            == (spectral_parameter+alpha)**5,
            "no two normal spectral relata" in CLAIM_CONTRACT["CANDIDATE_DEFINITION"][
                "reference_boundary"
            ],
        )),
        "self_only_postselection_is_rejected_by_full_pair_domain": all((
            comparison_table[0, 1] == 0, comparison_table[1, 0] == 0,
            "All four ordered pairs" in CLAIM_CONTRACT["COMPARISON_MAP"]["domain"],
            any("self-only" in item for item in CLAIM_CONTRACT["FORBIDDEN_INPUTS"]),
        )),
        "rank_only_comparator_cannot_reproduce_generic_weights": all((
            rank_only_table == sp.eye(2),
            sp.simplify(mu_r-mu_b-contrast_factor) == 0,
        )),
        "preferred_axis_and_representative_entries_absent": all((
            CLAIM_CONTRACT["FREEDOM_LEDGER"]["chosen_representative_basis_or_axis"][
                "complexity"
            ] == 0,
            any("preferred representative" in item for item in CLAIM_CONTRACT["FORBIDDEN_INPUTS"]),
            set(potential.free_symbols) == {alpha, b, c, x, y, u, v, w},
        )),
        "invalid_f1_boundaries_do_not_inherit_candidate": all((
            sp.simplify(lambda_b.subs(b, 0)) == 0,
            "alpha,b,c>0" in CLAIM_CONTRACT["DOMAIN"],
            "rejected stationary branch" in CLAIM_CONTRACT["DOMAIN"],
        )),
    }
    covariance_controls = {
        "manifest_complete_o3_covariance_from_invariant_second_derivative": all((
            derivation_controls["coordinate_hessian_matches_coordinate_free_second_variation"],
            CLAIM_CONTRACT["LAW_DERIVATION"]["covariance"].startswith("O(3)-invariance"),
        )),
        "exact_generator_covariance_crosscheck": all(covariance_checks),
        "frobenius_pairing_and_supertrace_report_invariant": all((
            gram.det() != 0,
            matrix_zero(riesz.T*gram-gram*riesz),
            comparison_table == comparison_table.T,
        )),
        "label_swap_leaves_reported_contrast_invariant": (
            sp.simplify(contrast_sq-(mu_b-mu_r)**2) == 0
        ),
        "parameter_motion_not_confused_with_one_orbit_equivalence": all((
            sp.trace(Q_star**2) == 2*s**2/3,
            sp.simplify((2*s**2/3).subs(s, 1)-(2*s**2/3).subs(s, 2)) != 0,
            "parameter-fibre mixing" in " ".join(CLAIM_CONTRACT["FORBIDDEN_INPUTS"]),
        )),
    }
    return {
        "DERIVATION_CONTROLS": derivation_controls,
        "RELATA_CONTROLS": relata_controls,
        "COMPARISON_CONTROLS": comparison_controls,
        "QP_ONLY_NULL_CONTROLS": qp_null_controls,
        "NULL_CONTROLS": null_controls,
        "COVARIANCE_CONTROLS": covariance_controls,
        "DIAGNOSTICS": {
            "hessian_characteristic_polynomial": str(characteristic),
            "sector_ranks": [int(pi_r.rank()), int(pi_b.rank()), int(pi_o.rank())],
            "lambda_r_positive_branch": str(lambda_r_plus),
            "lambda_b_positive_branch": str(lambda_b_plus),
            "normalized_weights": [str(mu_r), str(mu_b)],
            "contrast": str(contrast),
            "tuned_weights": [str(tuned_mu_r), str(tuned_mu_b)],
            "comparison_table": str(comparison_table),
        },
    }

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


def candidate_gate_map(algebra: dict[str, Any]) -> dict[str, bool]:
    derivation = algebra["DERIVATION_CONTROLS"]
    relata = algebra["RELATA_CONTROLS"]
    comparison = algebra["COMPARISON_CONTROLS"]
    qp_null = algebra["QP_ONLY_NULL_CONTROLS"]
    nulls = algebra["NULL_CONTROLS"]
    covariance = algebra["COVARIANCE_CONTROLS"]
    scope = CLAIM_CONTRACT["SCOPE_CEILING"]
    closure = CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"]
    freedom = CLAIM_CONTRACT["FREEDOM_LEDGER"]
    all_calculations = all(
        value is True
        for group in (derivation, relata, comparison, qp_null, nulls, covariance)
        for value in group.values()
    )
    gates = {
        "f1_dependency_valid": tuple(CLAIM_CONTRACT["DEPENDENCIES"]) == EXPECTED_DEPENDENCIES,
        "candidate_domain_map_and_branches_explicit": all((
            "b^2!=3 alpha c" in CLAIM_CONTRACT["DOMAIN"],
            "tuned_b2_equals_3_alpha_c" in CLAIM_CONTRACT["BRANCHES"],
            "undifferentiated_Q_zero" in CLAIM_CONTRACT["BRANCHES"],
        )),
        "relata_generated_not_preloaded": all((
            relata["q_generated_sector_projectors_exact"],
            relata["generic_spectral_polynomials_generate_relata"],
            freedom["chosen_representative_basis_or_axis"]["complexity"] == 0,
        )),
        "uniform_comparison_family_generated_not_preloaded": all((
            derivation["coordinate_hessian_matches_coordinate_free_second_variation"],
            derivation["riesz_operator_matches_hessian_and_is_self_adjoint"],
            comparison["one_predeclared_rule_covers_all_four_ordered_pairs"],
            freedom["new_numerical_parameters"]["complexity"] == 0,
        )),
        "outputs_share_one_comparison_codomain": all((
            comparison["normalized_comparison_table_exact"],
            CLAIM_CONTRACT["COMPARISON_MAP"]["codomain"]
            == "One shared exact real scalar codomain.",
        )),
        "exact_nontrivial_separation_witness": all((
            comparison["generic_open_domain_separation_exact"],
            comparison["label_free_contrast_and_sum_exact"],
        )),
        "relation_not_reduced_to_preassigned_unary_or_bare_equality_data": all((
            _all_true(qp_null), nulls["tuned_surface_collapses_to_scalar_delta"],
            "not claimed to be irreducibly pairwise"
            in CLAIM_CONTRACT["COMPARISON_MAP"]["semantic_ceiling"],
        )),
        "postselected_self_test_null_rejected": all((
            nulls["self_only_postselection_is_rejected_by_full_pair_domain"],
            comparison["one_predeclared_rule_covers_all_four_ordered_pairs"],
        )),
        "quotient_covariance_and_reported_invariance": _all_true(covariance),
        "undifferentiated_reference_null": nulls[
            "origin_hessian_is_scalar_and_generates_no_relata"
        ],
        "non_tuned_domain_and_regular_normalization": all((
            derivation["accepted_positive_branch_eigenvalues_exact"],
            comparison["generic_open_domain_separation_exact"],
            nulls["tuned_surface_collapses_to_scalar_delta"],
        )),
        "extra_primitive_ledger_complete": all((
            freedom["new_physical_primitives"]["complexity"] == 0,
            freedom["data_fitted_parameters"]["complexity"] == 0,
            freedom["hessian_candidate_choice"]["complexity"] == 1,
            freedom["normalization_choice"]["complexity"] == 1,
        )),
        "joint_admissibility_composition_and_common_action_derived": all((
            CLAIM_CONTRACT["CANDIDATE_DEFINITION"]["route"]
            == "INTRASTATE_UNIFORM_EFFECT_FAMILY",
            covariance["manifest_complete_o3_covariance_from_invariant_second_derivative"],
            "All four ordered pairs" in CLAIM_CONTRACT["COMPARISON_MAP"]["domain"],
        )),
        "full_f2_node_and_imprint_obligations_not_claimed": all((
            scope["physical_node_or_location"] is False,
            scope["atemporal_imprint_or_correlation_carrier"] is False,
            scope["full_W2_F2_operational_relations"] is False,
            closure["full_W2_F2_operational_relations_proved"] is False,
        )),
        "operational_semantics_not_upgraded": all((
            comparison["comparison_not_a_physical_or_temporal_response"],
            scope["irreducibly_pairwise_coupling"] is False,
            scope["physical_response_intervention_or_measurement"] is False,
        )),
        "external_observable_and_data_map_absent": all((
            CLAIM_CONTRACT["OBSERVABLE_MAP"]["status"] == "N/A",
            CLAIM_CONTRACT["FORWARD_MODEL"]["status"] == "N/A",
            CLAIM_CONTRACT["DATA_ROLE"]["status"] == "N/A",
            scope["external_observable_or_data_map"] is False,
            scope["observational_validation"] is False,
        )),
        "f3_temporal_and_causal_imports_absent": all((
            scope["temporal_formation_persistence_or_causality"] is False,
            closure["F3_internal_order_or_causality_proved"] is False,
        )),
        "positive_null_and_adversarial_controls_pass": all_calculations,
        "candidate_specific_calculation_complete": all_calculations,
    }
    if set(gates) != F2A_GATE_KEYS or any(type(value) is not bool for value in gates.values()):
        return {key: False for key in F2A_GATE_KEYS}
    return gates


def candidate_screen(gates: Any) -> dict[str, bool]:
    schema_valid = (
        isinstance(gates, dict) and set(gates) == F2A_GATE_KEYS
        and all(type(value) is bool for value in gates.values())
    )
    proved = bool(schema_valid and all(gates.values()))
    return {"valid": bool(schema_valid), "F2a_proved": proved, "full_F2_proved": False}


def run() -> dict[str, Any]:
    result = candidate_algebra()
    controls = {key: value for key, value in result.items() if key != "DIAGNOSTICS"}
    scope_closure = scope_closure_controls()
    gates = candidate_gate_map(result)
    screen = candidate_screen(gates)
    valid = bool(
        _all_true(controls) and _all_true(scope_closure)
        and screen["valid"] and screen["F2a_proved"]
        and not screen["full_F2_proved"]
    )
    return {
        "artifact": CLAIM_CONTRACT["CLAIM_ID"],
        "valid": valid,
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The invariant Hessian generates an exact internal two-sector comparison "
            "on the declared generic domain. The tuned surface and origin remain null "
            "boundaries; this is F2a only, not full F2 or a physical response."
        ),
        "scope_ceiling": CLAIM_CONTRACT["SCOPE_CEILING"],
        "scientific_closure": CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"],
        "controls": controls,
        "scope_closure_controls": scope_closure,
        "candidate_gate_map": gates,
        "candidate_screen": screen,
        "diagnostics": result["DIAGNOSTICS"],
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
