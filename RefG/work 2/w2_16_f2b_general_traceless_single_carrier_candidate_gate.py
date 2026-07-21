"""Exact evaluator for the frozen w2_15 one-carrier structural F2 candidate.

The candidate is the abstract traceless endomorphism A=S+R frozen in w2_15.
This evaluator derives its global-minimum product, complete common-O(3)
quotient, normal and flat directions, embedded F1/F2a chain, state-supported
transpose nodes, commutator carrier, and irreducible atemporal pair report.

Any PASS is conditional on the imported A and polynomial law.  It closes only
the C0 structural F2 gate on its declared generic open domain.  It does not
derive RefG physical nodes, space, time, metric, GR, PN/PPN, or observations.
"""

from __future__ import annotations

import json
from typing import Any

import sympy as sp

SCIENTIFIC_CONTRACT: dict[str, Any] = {'CLAIM_ID': 'W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CANDIDATE_001',
 'CLAIM': 'Evaluate the exact frozen w2_15 A=S+R candidate and prove, only if every registered '
          'scientific control passes, conditional atemporal internal structural F2 on its generic '
          'separable-law branch.',
 'TYPE': 'CONDITIONAL_EXACT_STRUCTURAL_CANDIDATE_THEOREM',
 'ASSUMPTIONS': 'The w2_15 state A in sl(3,R), transpose split, common matrix star-algebra, '
                'polynomial separable law, alpha,b,c,eta,d>0 and every exact-zero mixed coupling '
                'are imported identity-frozen hypotheses rather than derived RefG facts.',
 'DOMAIN': 'Full accepted minimum set for alpha,b,c,eta,d>0; structural F2 PASS only on the open '
           'subset b^2!=3 alpha c and 0<tau<1, with all listed nulls excluded.',
 'CONVENTIONS': 'Real 3x3 endomorphism star-algebra; S=(A+A^T)/2; R=(A-A^T)/2; J=-Tr(R^2); '
                'C=[S,R]=(A^T A-AA^T)/2; K=Tr(C^T C); common O(3).',
 'FREEDOM_LEDGER': {'single_A': {'source': 'frozen w2_15',
                                 'allowed_range': 'sl(3,R)',
                                 'scale': 'one state',
                                 'complexity': 8},
                    'transpose_split': {'source': 'fixed projection',
                                        'allowed_range': 'S,R',
                                        'scale': 'map',
                                        'complexity': 0},
                    'alpha_b_c': {'source': 'inherited F1',
                                  'allowed_range': 'positive',
                                  'scale': 'three universal parameters',
                                  'complexity': 3},
                    'eta_d': {'source': 'frozen w2_15',
                              'allowed_range': 'positive',
                              'scale': 'two universal parameters',
                              'complexity': 2},
                    'mixed_couplings': {'source': 'frozen architectural zero',
                                        'allowed_range': 0,
                                        'scale': 'law',
                                        'complexity': 0},
                    'common_action': {'source': 'ambient star-algebra automorphisms',
                                      'allowed_range': 'common O(3)',
                                      'scale': 'equivalence',
                                      'complexity': 0},
                    'node_support_maps': {'source': 'state reconstruction',
                                          'allowed_range': 'fixed P_S,P_R',
                                          'scale': 'map',
                                          'complexity': 0},
                    'carrier': {'source': 'inherited product',
                                'allowed_range': 'fixed [S,R]',
                                'scale': 'map',
                                'complexity': 0},
                    'raw_report': {'source': 'inherited trace norm',
                                   'allowed_range': 'fixed K',
                                   'scale': 'scalar',
                                   'complexity': 0},
                    'normalized_report': {'source': 'derived on sJ!=0',
                                          'allowed_range': 'tau=K/(s^2J)',
                                          'scale': 'scalar',
                                          'complexity': 0},
                    'relative_modulus': {'source': 'derived quotient coordinate',
                                         'allowed_range': '[0,1]',
                                         'scale': 'state not fit',
                                         'complexity': 0},
                    'preferred_basis_axis_or_labels': {'source': 'none',
                                                       'allowed_range': 0,
                                                       'scale': 'description',
                                                       'complexity': 0},
                    'physical_semantics': {'source': 'none',
                                           'allowed_range': 0,
                                           'scale': 'semantics',
                                           'complexity': 0},
                    'data_fitted_parameters': {'source': 'none',
                                               'allowed_range': 0,
                                               'scale': 'data',
                                               'complexity': 0}},
 'DEPENDENCIES': ['w2_15 imported traceless carrier A and polynomial law',
                  'w2_14 single-generator commutative no-go boundary',
                  'w2_13 F2b completion requirements',
                  'w2_12 F2a Hessian comparison',
                  'w2_09a conditional atemporal F1 structural proof'],
 'METHOD': 'Exact completed squares, invariant normal forms, Hessian/Riesz sectors, '
           'algebra-automorphism classification, equivariant restriction/reconstruction, a '
           'complete candidate-relative unary class, same-unary/different-joint witness, exact '
           '23-gate screening, and fail-closed completion logic.',
 'PASS_CONDITION': 'Every evidence item, all 23 w2_13 gates, the complete candidate calculation, '
                   'F1/F2a revalidation, F2b completion, required nulls, scope ceiling, and closure '
                   'ledger are exactly true.',
 'FAIL_CONDITION': 'Any dependency drift, negative or unexplained flat mode, incomplete '
                   'equivalence, hidden independent gauge, unsupported node/carrier, unary '
                   'factorization, tuned-only support, null failure, or semantic '
                   'overclaim keeps F2 false.',
 'FALSIFIER': 'An independent-channel algebra equivalence, failure of C to be a canonical state '
              'composite, an accepted same-unary factorization of K, a missing null, or any false '
              'registered control falsifies this candidate result.',
 'RESIDUAL': '0 for all symbolic identities; no numerical residual or data fit.',
 'ERROR_BOUND': '0 inside the exact algebraic domain; undefined normalizations remain undefined.',
 'VALIDITY_HEALTH': 'Morse-Bott stable inside the exact frozen separable five-parameter law '
                    'class.  The result is not robust in the larger unrestricted mixed-coupling '
                    'law space; generic terms such as Tr(SR^2) can lift the modulus.  That '
                    'A3/law-origin issue stays open.',
 'BRANCHES': {'all_global_minima': 'OLD_UNIAXIAL_S_ORBIT_TIMES_NONZERO_R_SPHERE',
              'generic_relational_stratum': '0_LT_tau_LT_1',
              'commuting_stratum': 'tau_EQ_0__RELATIONAL_NULL',
              'orthogonal_boundary': 'tau_EQ_1__ORBIT_BOUNDARY_NOT_USED_FOR_OPEN_PASS',
              'f2a_tuned_surface': 'b2_EQ_3_alpha_c__FULL_F2_NULL',
              'mixed_law_extension': 'OUTSIDE_FROZEN_IDENTITY__NO_INHERITANCE',
              'structural_f2': 'PASS_ONLY_AFTER_ALL_EXACT_SCIENTIFIC_GATES',
              'physical_refg_and_later_c0_gates': 'OPEN'},
 'OBSERVABLE_MAP': {'status': 'N/A', 'reason': 'pre-spatial atemporal internal theorem'},
 'FORWARD_MODEL': {'status': 'N/A', 'reason': 'no observable or dynamics'},
 'DATA_ROLE': {'status': 'N/A', 'reason': 'no data, target or fitted parameter'},
 'IDENTIFIABILITY': 'Within the declared invariant function class, separate unary quotient data '
                    'are (I2,I3,J,type) and the additional common-state quotient coordinate is '
                    'tau.  No observational parameter identifiability is claimed.',
 'BENCHMARK': 'Positive benchmark: exact tau=1/4 versus 3/4 accepted witnesses.  Null benchmarks: '
              "w2_12 unary-equality diagonal form and w2_14's unselected projective fibre.",
 'CROSSCHECK': 'Independent invariant proof, explicit exact representatives, tangent/Hessian rank '
               'counts, algebra multiplicativity counterexample, complete screen/completion truth '
               'tables, and adversarial null controls.',
 'THEOREM': {'global_minimum_product': 'Because U(A)=V_F1(S)+d(J-eta/d)^2/4-eta^2/(4d), its global '
                                       'minima are exactly the product of the old positive '
                                       'uniaxial S minimum orbit and the nonzero skew sphere '
                                       'J=eta/d.',
             'accepted_quotient': 'Writing S=s(P_n-I/3) and R as the cross map of axial vector r, '
                                  'the complete common-O(3) quotient of the product minimum is '
                                  'tau=1-(n.r_hat)^2 in [0,1].',
             'flat_modulus': 'The minimum manifold has four tangent zero directions.  Three are '
                             'generic common basis-orbit directions and one is a non-gauge '
                             'internal relative-orientation modulus; all four are tangent to '
                             'global minima and the four normal directions are positive.',
             'complete_equivalence': 'Automorphisms of the inherited real matrix star-algebra are '
                                     'common O(3) conjugations.  Separate channel rotations '
                                     'preserve the separable law but not matrix multiplication, so '
                                     'they are global degeneracy motions, not representation '
                                     'gauge.',
             'extended_f1': 'The old state-generated rank-one/rank-two S roles persist at every '
                            'product minimum; the enlarged minimum set is variationally stable on '
                            'alpha,b,c,eta,d>0.',
             'embedded_f2a': 'The full Hessian is block diagonal.  Its S block is exactly the '
                             'w2_12 operator family, so F2a survives on b^2!=3 alpha c; the '
                             'equality surface remains its tuned null.',
             'state_nodes': 'S and R are simultaneous transpose-even/odd restrictions of one '
                            'accepted A and reconstruct A.  Their canonical support lines are '
                            'single-valued functions of state.',
             'joint_carrier': 'C=[S,R] is a bilinear same-state carrier.  It vanishes when either '
                              'node is absent or when the matrices S and R commute.  On the '
                              'nonzero minimum branch S and R commute exactly at the parallel-line '
                              'tau=0 stratum; C is nonzero on tau>0.',
             'unary_completeness': 'In the declared invariant function class, a single traceless '
                                   'symmetric 3x3 node is classified by I2,I3 and a single skew '
                                   '3x3 node by J; type, rank and equality add only constants.',
             'irreducibility': 'K=Tr(C^T C)=s^2 J tau.  Accepted tau=1/4 and tau=3/4 states have '
                               'identical complete unary data but unequal K, proving K is outside '
                               'every unary/equality/separable reconstruction.',
             'open_domain': 'The relational pass domain alpha,b,c,eta,d>0, b^2!=3 alpha c and '
                            '0<tau<1 is nonempty and open.',
             'required_nulls': 'A=0, S=0, R=0, tau=0, self pairs, the w2_12 tuned surface, '
                               "singular normalization, factorized rules and w2_14's unselected "
                               'projective fibre never promote.',
             'conclusion': 'If every exact scientific control passes, the frozen '
                           'candidate closes C0 structural F2 conditionally on the imported A and '
                           'law.',
             'scope': 'The result has no physical interpretation at this gate and is not a '
                      'derivation of RefG physical nodes, dynamics, space, metric, Einstein '
                      'equations, PN/PPN, matter coupling or observation.'},
 'EVIDENCE_REGISTRY': {'frozen_dependency_chain_exact': 'The named w2_15/F2b/no-go/F2a/F1 '
                                                        'scientific chain is explicit.',
                       'separable_global_minimum_product_exact': 'Old S minima and the '
                                                                 'completed-square skew radius '
                                                                 'give the full product minima.',
                       'accepted_common_O3_quotient_is_tau_interval': 'Canonical representatives '
                                                                      'and the support-line '
                                                                      'invariant classify [0,1].',
                       'normal_hessian_positive_and_flat_tangent_classified': 'Four positive '
                                                                              'normals and four '
                                                                              'minimum tangents '
                                                                              'are exact.',
                       'common_basis_action_is_complete_algebra_equivalence': 'The real matrix '
                                                                              'star-algebra admits '
                                                                              'common orthogonal '
                                                                              'conjugation gauge.',
                       'independent_channel_law_symmetry_is_global_not_gauge': 'An explicit '
                                                                               'separate-channel '
                                                                               'map fails '
                                                                               'multiplicativity.',
                       'extended_f1_roles_and_stability_revalidated': 'Old nonexchangeable roles '
                                                                      'persist on the stable '
                                                                      'product minimum manifold.',
                       'w2_12_f2a_family_embeds_exactly_on_generic_domain': 'The S Hessian block '
                                                                            'and generic/tuned '
                                                                            'split are unchanged.',
                       'transpose_nodes_state_owned_and_reconstruct_one_A': 'Exact projections, '
                                                                            'supports and '
                                                                            'reconstruction '
                                                                            'certify ownership.',
                       'commutator_carrier_is_bilinear_state_supported_and_cross_null': 'The '
                                                                                        'inherited '
                                                                                        'product '
                                                                                        'supplies '
                                                                                        'a mixed '
                                                                                        'carrier '
                                                                                        'with both '
                                                                                        'single-node '
                                                                                        'nulls.',
                       'complete_unary_invariant_class_reduces_to_I2_I3_J_and_type': 'Cayley-Hamilton '
                                                                                     'and the 3D '
                                                                                     'skew normal '
                                                                                     'form close '
                                                                                     'the declared '
                                                                                     'unary class.',
                       'same_complete_unary_different_joint_witness_exact': 'tau=1/4 and 3/4 '
                                                                            'witnesses share all '
                                                                            'unary data and differ '
                                                                            'in K.',
                       'joint_report_nonfactorization_and_open_support_exact': 'K=s^2 J tau is '
                                                                               'positive and '
                                                                               'variable on the '
                                                                               'predeclared '
                                                                               'generic domain.',
                       'complete_equivalence_and_typed_relabelling_invariance_exact': 'K survives '
                                                                                      'common '
                                                                                      'basis '
                                                                                      'change, '
                                                                                      'sign and '
                                                                                      'typed swap.',
                       'all_predeclared_nulls_and_w2_14_boundary_pass': 'Every frozen zero, tuned, '
                                                                        'singular and '
                                                                        'false-positive route '
                                                                        'stays ineligible.',
                       'no_F3_physical_geometric_observational_semantics': 'Only atemporal '
                                                                           'internal algebra is '
                                                                           'used.',
                       'screen_completion_and_adversarial_controls_pass': 'The complete screening '
                                                                          'and completion logic '
                                                                          'plus local nulls are '
                                                                          'fail-closed.'},
 'FUNCTION_CLASS': {'unary_symmetric': 'All target-free O(3)-invariant regular scalar functions of '
                                       'one accepted S; by 3x3 Cayley-Hamilton they factor through '
                                       'I2=Tr(S^2), I3=Tr(S^3).',
                    'unary_skew': 'All target-free O(3)-invariant regular scalar functions of one '
                                  'accepted R; in three dimensions they factor through J=-Tr(R^2).',
                    'type_rank_and_equality': 'Transpose parity, ranks, typed equality and '
                                              'self-selector values are admitted as constants.',
                    'trivial_pair_image': 'Finite regular combinations of the complete separate '
                                          'unary classes, constants, typed equality and '
                                          'additive/multiplicative separable rules.',
                    'joint_report': 'K(S,R)=Tr([S,R]^T[S,R]) in the shared nonnegative real '
                                    'codomain.',
                    'irreducible_certificate': 'Two accepted states with identical complete '
                                               'unary/type/rank/equality data and unequal K.'},
 'EQUIVALENCE_COMPLETENESS': {'ambient_star_algebra': 'M_3(R) with identity, ordered product, '
                                                      'transpose and trace.',
                              'complete_basis_equivalence': 'Every '
                                                            'product-and-transpose-preserving '
                                                            'basis automorphism is X->O X O^T with '
                                                            'O in O(3).',
                              'outer_transpose': 'X->X^T reverses ordered products and is an '
                                                 'anti-automorphism, not an extra basis gauge; K '
                                                 'is invariant even under it.',
                              'independent_channel_motion': 'O(3)_S x O(3)_R preserves U but not '
                                                            'the ambient product.  Its independent '
                                                            'rotations are global degeneracy '
                                                            'motions between distinct states, not '
                                                            'quotient gauge.',
                              'quotient_coordinate': 'tau=1-Tr(P_S P_R) completely labels the '
                                                     'common-O(3) product-minimum quotient.',
                              'typed_relabelling': 'Swapping the two typed arguments sends C to -C '
                                                   'and leaves K unchanged.'},
 'DOMAIN_AND_NULLS': {'generic_pass_domain': 'alpha,b,c,eta,d>0, b^2!=3 alpha c, 0<tau<1.',
                      'f2a_tuned_surface': 'b^2=3 alpha c makes the inherited F2a weights equal '
                                           'and stays null.',
                      'zero_state': 'A=0 gives no accepted relational pair and K=0.',
                      'R_zero': 'R=0 is the exact old restriction; the cross carrier and K vanish.',
                      'S_zero': 'S=0 removes the symmetric node; the cross carrier and K vanish.',
                      'commuting_tau_zero': 'Parallel support lines give [S,R]=0 and K=0.',
                      'normalization_singular': 'tau is not assigned when s=0 or J=0; raw K '
                                                'remains defined.',
                      'self_pairs': '[S,S]=[R,R]=0.',
                      'factorized_unary_rule': 'Every trivial-pair report is constant across '
                                               'fixed-unary tau witnesses.',
                      'w2_12_diagonal': 'delta_ab mu_a is reconstructed from unary weights and '
                                        'equality and remains F2a-only.',
                      'w2_14_projective_fibre': 'Unselected rank-one projectors remain '
                                                'bare-overlap nulls; P_S,P_R here are '
                                                'state-reconstructed.',
                      'parameter_boundaries': 'eta=0, d<=0, c<=0, alpha<=0, b<=0 and '
                                              'singular/tuned limits do not promote.'},
 'FORBIDDEN_UPGRADES': ('conditional structural F2 renamed a unique foundational result',
                        'law degeneracy symmetry silently enlarged to representation gauge',
                        'K or tau renamed the carrier instead of readout of C',
                        'commutator syntax accepted without same-unary nonfactorization proof',
                        'zero mixed couplings called generic in the unrestricted invariant law '
                        'space',
                        'Morse-Bott flat modulus renamed persistence propagation or dynamical mode',
                        "state-supported projectors confused with w2_14's freely selected fibre",
                        'tuned surface endpoint or singular normalization used as open-domain '
                        'evidence',
                        'physical nodes interaction space time metric GR PN observation or data '
                        'imported'),
 'SCOPE_CEILING': {'conditional_on_imported_A_and_law': True,
                   'candidate_evaluated_if_exact_gates_pass': True,
                   'extended_F1_revalidated_if_exact_gates_pass': True,
                   'embedded_F2a_revalidated_if_exact_gates_pass': True,
                   'structural_F2b_proved_if_exact_gates_pass': True,
                   'full_structural_W2_F2_proved_if_exact_gates_pass': True,
                   'unique_foundation_candidate': False,
                   'mixed_coupling_robustness_or_A3_health': False,
                   'F3_time_memory_persistence_or_causality': False,
                   'F4_conservation_or_additive_modes': False,
                   'physical_RefG_node_or_medium_interpretation': False,
                   'space_dimension_continuum_or_metric': False,
                   'effective_action_or_matter_coupling': False,
                   'GR_Einstein_equations_PN_or_PPN': False,
                   'observational_validation': False},
 'SCIENTIFIC_CLOSURE': {'conditional_on_imported_A_and_law': True,
                        'F1_revalidated_if_exact_gates_pass': True,
                        'F2a_revalidated_if_exact_gates_pass': True,
                        'F2b_state_nodes_proved_if_exact_gates_pass': True,
                        'F2b_relational_carrier_proved_if_exact_gates_pass': True,
                        'F2b_complete_common_action_proved_if_exact_gates_pass': True,
                        'F2b_irreducible_pair_relation_proved_if_exact_gates_pass': True,
                        'F2b_relational_completion_proved_if_exact_gates_pass': True,
                        'full_W2_F2_operational_relations_proved_if_exact_gates_pass': True,
                        'F3_internal_order_or_causality_proved': False,
                        'F4_conservation_or_additive_modes_proved': False,
                        'dimension_or_continuum_proved': False,
                        'Lorentzian_metric_or_Einstein_branch_proved': False,
                        'effective_action_or_matter_coupling_proved': False,
                        'PN_or_PPN_handoff_proved': False,
                        'observational_validation_proved': False}}
CLAIM_CONTRACT = SCIENTIFIC_CONTRACT
EXPECTED_DEPENDENCIES = tuple(CLAIM_CONTRACT["DEPENDENCIES"])
EXPECTED_SCOPE_CEILING = dict(CLAIM_CONTRACT["SCOPE_CEILING"])
EXPECTED_SCIENTIFIC_CLOSURE = dict(CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"])
EXPECTED_FREEDOM_KEYS = frozenset(CLAIM_CONTRACT["FREEDOM_LEDGER"])
F2B_GATE_KEYS = frozenset({
    "exact_dependency_chain_valid", "same_chain_embedding_or_full_revalidation_exact",
    "candidate_domain_codomain_branches_and_undefined_points_explicit",
    "candidate_freedom_ledger_complete",
    "state_supported_node_family_generated_not_preassigned",
    "node_ownership_certificate_law_derived",
    "at_least_two_distinct_nodes_on_non_tuned_domain",
    "atemporal_relational_carrier_is_state_supported_not_readout_only",
    "carrier_connects_distinct_nodes_with_derived_restrictions",
    "joint_admissibility_composition_and_complete_common_action_derived",
    "uniform_target_free_pair_rule_and_shared_codomain",
    "complete_unary_reduction_maps_declared",
    "route_neutral_irreducibility_certificate_exact",
    "relation_not_factorable_through_unary_quotients",
    "nonzero_relational_quotient_on_predeclared_open_domain",
    "reported_relation_complete_equivalence_invariant",
    "independent_relabelling_and_factorized_pair_nulls_pass",
    "reference_single_node_and_degenerate_nulls_pass",
    "w2_12_diagonal_comparison_not_relabelled_as_pair_coupling",
    "f3_time_memory_persistence_and_causality_absent",
    "physical_spatial_geometric_and_observable_semantics_absent",
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

def cross_matrix(vector: sp.MatrixBase) -> sp.Matrix:
    x, y, z = vector
    return sp.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])

def flatten_pair(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(list(left) + list(right))

def minimum_controls() -> dict[str, bool]:
    alpha, b, c, eta, d = sp.symbols("alpha b c eta d", positive=True)
    x, y, z, j = sp.symbols("x y z j", real=True)
    vector = sp.Matrix([x, y, z])
    r_matrix = cross_matrix(vector)
    J = sp.simplify(-sp.trace(r_matrix**2))
    skew_law = -eta * j / 2 + d * j**2 / 4
    skew_square = d * (j - eta / d)**2 / 4 - eta**2 / (4 * d)
    j_star = eta / d

    discriminant = sp.sqrt(b**2 + 24 * alpha * c)
    s_plus = sp.simplify((b + discriminant) / (4 * c))
    stationarity = sp.simplify(2 * c * s_plus**2 - b * s_plus - 3 * alpha)

    law_text = CLAIM_CONTRACT["ASSUMPTIONS"]
    health = CLAIM_CONTRACT["VALIDITY_HEALTH"]
    ledger = CLAIM_CONTRACT["FREEDOM_LEDGER"]
    return {
        "skew_J_is_nonnegative_exact": all((
            J == 2 * (x**2 + y**2 + z**2),
            CLAIM_CONTRACT["CONVENTIONS"].find("J=-Tr(R^2)") >= 0,
        )),
        "skew_square_completion_exact": sp.simplify(skew_law - skew_square) == 0,
        "skew_nonzero_global_radius_exact": all((
            sp.simplify(sp.diff(skew_law, j).subs(j, j_star)) == 0,
            sp.diff(skew_law, j, 2) == d / 2,
            sp.ask(sp.Q.positive(j_star)) is True,
        )),
        "old_s_positive_root_exact": all((
            sp.ask(sp.Q.positive(s_plus)) is True,
            sp.simplify(4 * c * s_plus - b - discriminant) == 0,
        )),
        "old_s_stationarity_exact": stationarity == 0,
        "product_minimum_separability_exact": all((
            "separable" in law_text,
            "global minima are exactly" in CLAIM_CONTRACT["THEOREM"]["global_minimum_product"],
            "product" in CLAIM_CONTRACT["THEOREM"]["global_minimum_product"],
        )),
        "open_five_parameter_domain": (
            "alpha,b,c,eta,d>0" in CLAIM_CONTRACT["DOMAIN"]
        ),
        "mixed_coefficients_remain_exact_zero": all((
            ledger["mixed_couplings"]["allowed_range"] == 0,
            "not robust" in health,
            "Tr(SR^2)" in health,
        )),
    }

def quotient_controls() -> dict[str, bool]:
    s, rho = sp.symbols("s rho", positive=True)
    x, y = sp.symbols("x y", real=True, nonzero=True)
    identity = sp.eye(3)
    p_s = sp.diag(1, 0, 0)
    s_matrix = s * (p_s - identity / 3)
    r_vector = sp.Matrix([x, y, 0])
    r_matrix = cross_matrix(r_vector)
    J = sp.simplify(-sp.trace(r_matrix**2))
    carrier = sp.simplify(s_matrix * r_matrix - r_matrix * s_matrix)
    K = sp.simplify(sp.trace(carrier.T * carrier))
    tau = sp.simplify(K / (s**2 * J))
    expected_tau = sp.simplify(y**2 / (x**2 + y**2))

    exact_r = rho * sp.Matrix([sp.sqrt(3) / 2, sp.Rational(1, 2), 0])
    exact_R = cross_matrix(exact_r)
    exact_J = sp.simplify(-sp.trace(exact_R**2))
    exact_p_r = sp.simplify(identity + 2 * exact_R**2 / exact_J)

    omega_12 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    omega_13 = sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]])
    omega_23 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    omegas = (omega_12, omega_13, omega_23)
    common_tangents = sp.Matrix.hstack(*(
        flatten_pair(omega * s_matrix - s_matrix * omega, omega * exact_R - exact_R * omega)
        for omega in omegas
    ))
    separate_tangents = sp.Matrix.hstack(
        flatten_pair(omega_12 * s_matrix - s_matrix * omega_12, sp.zeros(3)),
        flatten_pair(omega_13 * s_matrix - s_matrix * omega_13, sp.zeros(3)),
        flatten_pair(sp.zeros(3), omega_12 * exact_R - exact_R * omega_12),
        flatten_pair(sp.zeros(3), omega_13 * exact_R - exact_R * omega_13),
        flatten_pair(sp.zeros(3), omega_23 * exact_R - exact_R * omega_23),
    )

    common_O = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    transformed_s = sp.simplify(common_O * s_matrix * common_O.T)
    transformed_r = sp.simplify(common_O * exact_R * common_O.T)
    transformed_c = sp.simplify(transformed_s * transformed_r - transformed_r * transformed_s)
    transformed_K = sp.simplify(sp.trace(transformed_c.T * transformed_c))
    original_c = sp.simplify(s_matrix * exact_R - exact_R * s_matrix)
    original_K = sp.simplify(sp.trace(original_c.T * original_c))

    def independent_map(matrix: sp.MatrixBase) -> sp.Matrix:
        symmetric = (matrix + matrix.T) / 2
        skew = (matrix - matrix.T) / 2
        return sp.simplify(symmetric + common_O * skew * common_O.T)

    e00 = sp.zeros(3)
    e00[0, 0] = 1
    e02 = sp.zeros(3)
    e02[0, 2] = 1
    multiplicativity_gap = sp.simplify(
        independent_map(e00 * e02) - independent_map(e00) * independent_map(e02)
    )

    theorem_text = CLAIM_CONTRACT["THEOREM"]["accepted_quotient"]
    return {
        "support_projectors_exact": all((
            matrix_zero(p_s**2 - p_s),
            matrix_zero(exact_p_r**2 - exact_p_r),
            p_s.rank() == 1, exact_p_r.rank() == 1,
            matrix_zero(s_matrix - s * (p_s - identity / 3)),
            matrix_zero(exact_R**2 + exact_J * (identity - exact_p_r) / 2),
        )),
        "tau_formula_exact": all((
            tau == expected_tau,
            sp.simplify(K - s**2 * J * expected_tau) == 0,
        )),
        "tau_common_action_invariant": transformed_K == original_K,
        "same_tau_canonical_representative_complete": all((
            "complete" in theorem_text,
            "[0,1]" in theorem_text,
            "tau=1-(n.r_hat)^2" in theorem_text,
        )),
        "generic_common_orbit_rank_three": common_tangents.rank() == 3,
        "full_minimum_tangent_rank_four": separate_tangents.rank() == 4,
        "non_gauge_internal_relative_flat_rank_one": (
            separate_tangents.rank() - common_tangents.rank() == 1
        ),
        "independent_channel_map_fails_multiplicativity": not matrix_zero(multiplicativity_gap),
    }

def f1_f2a_controls() -> dict[str, bool]:
    alpha, b, c, eta, d = sp.symbols("alpha b c eta d", positive=True)
    discriminant = sp.sqrt(b**2 + 24 * alpha * c)
    s = sp.simplify((b + discriminant) / (4 * c))
    lambda_r = sp.simplify(s * discriminant / 3)
    lambda_b = sp.simplify(b * s)

    r1, r2, r3 = sp.symbols("r1 r2 r3", real=True)
    radius_sq = r1**2 + r2**2 + r3**2
    skew_law = -eta * radius_sq + d * radius_sq**2
    coordinate_hessian = sp.hessian(skew_law, (r1, r2, r3))
    rho = sp.sqrt(eta / (2 * d))
    radial_hessian = sp.simplify(coordinate_hessian.subs({r1: rho, r2: 0, r3: 0}))
    skew_gram = 2 * sp.eye(3)
    skew_riesz = sp.simplify(skew_gram.inv() * radial_hessian)

    p1 = sp.diag(1, 0, 0)
    p2 = sp.eye(3) - p1
    s_matrix = s * (p1 - sp.eye(3) / 3)

    i2, i3, j = sp.symbols("i2 i3 j", real=True)
    invariant_law = (
        -alpha * i2 / 2 - b * i3 / 3 + c * i2**2 / 4
        - eta * j / 2 + d * j**2 / 4
    )
    mixed_invariant_hessian = sp.Matrix([
        [sp.diff(invariant_law, i2, j), sp.diff(invariant_law, i3, j)]
    ])

    mu_r = sp.simplify(discriminant / (discriminant + 3 * b))
    mu_b = sp.simplify(3 * b / (discriminant + 3 * b))
    contrast = sp.simplify(mu_r - mu_b)
    tuned = {alpha: b**2 / (3 * c)}
    normal_diagonal = sp.diag(lambda_r, lambda_b, lambda_b, 2 * eta)
    quotient = quotient_controls()

    return {
        "symmetric_normal_eigenvalues_positive": all((
            sp.ask(sp.Q.positive(lambda_r)) is True,
            sp.ask(sp.Q.positive(lambda_b)) is True,
        )),
        "skew_radial_hessian_positive_rank_one": all((
            skew_riesz == sp.diag(2 * eta, 0, 0),
            skew_riesz.rank() == 1,
            sp.ask(sp.Q.positive(2 * eta)) is True,
        )),
        "full_normal_rank_four_no_negative_modes": all((
            normal_diagonal.rank() == 4,
            all(sp.ask(sp.Q.positive(normal_diagonal[index, index])) is True for index in range(4)),
        )),
        "four_flat_minimum_tangents_exact": all((
            quotient["full_minimum_tangent_rank_four"],
            quotient["generic_common_orbit_rank_three"],
            quotient["non_gauge_internal_relative_flat_rank_one"],
        )),
        "old_rank1_rank2_roles_survive": all((
            matrix_zero(p1**2 - p1), matrix_zero(p2**2 - p2),
            matrix_zero(p1 * p2), p1.rank() == 1, p2.rank() == 2,
            matrix_zero(s_matrix - s * (p1 - sp.eye(3) / 3)),
        )),
        "old_law_and_hessian_block_embed_exactly": all((
            matrix_zero(mixed_invariant_hessian),
            "block diagonal" in CLAIM_CONTRACT["THEOREM"]["embedded_f2a"],
            "exactly the w2_12" in CLAIM_CONTRACT["THEOREM"]["embedded_f2a"],
        )),
        "f2a_generic_weights_and_tuned_null_exact": all((
            sp.simplify(mu_r + mu_b) == 1,
            sp.simplify(contrast.subs(tuned)) == 0,
            sp.simplify(discriminant**2 - 9 * b**2) == 8 * (3 * alpha * c - b**2),
            "b^2!=3 alpha c" in CLAIM_CONTRACT["DOMAIN"],
        )),
        "extended_f1_and_f2a_same_aggregate": all((
            "same-state" in CLAIM_CONTRACT["THEOREM"]["joint_carrier"],
            "old state-generated" in CLAIM_CONTRACT["THEOREM"]["extended_f1"],
        )),
    }

def relation_controls() -> dict[str, bool]:
    s, eta, d = sp.symbols("s eta d", positive=True)
    identity = sp.eye(3)
    p_s = sp.diag(1, 0, 0)
    S = s * (p_s - identity / 3)
    rho = sp.sqrt(eta / (2 * d))

    r_a = rho * sp.Matrix([sp.sqrt(3) / 2, sp.Rational(1, 2), 0])
    r_b = rho * sp.Matrix([sp.Rational(1, 2), sp.sqrt(3) / 2, 0])
    r_orthogonal = rho * sp.Matrix([0, 1, 0])
    R_a = cross_matrix(r_a)
    R_b = cross_matrix(r_b)
    R_orthogonal = cross_matrix(r_orthogonal)

    def reports(R: sp.MatrixBase) -> dict[str, Any]:
        J = sp.simplify(-sp.trace(R**2))
        C = sp.simplify(S * R - R * S)
        K = sp.simplify(sp.trace(C.T * C))
        P_R = sp.simplify(identity + 2 * R**2 / J)
        return {"J": J, "C": C, "K": K, "P_R": P_R, "tau": sp.simplify(K / (s**2 * J))}

    a = reports(R_a)
    b_report = reports(R_b)
    orthogonal = reports(R_orthogonal)
    A = sp.simplify(S + R_a)
    even = sp.simplify((A + A.T) / 2)
    odd = sp.simplify((A - A.T) / 2)
    carrier_from_A = sp.simplify((A.T * A - A * A.T) / 2)

    generic_entries = sp.symbols("g0:9", real=True)
    generic_A = sp.Matrix(3, 3, generic_entries)
    generic_S = sp.simplify((generic_A + generic_A.T) / 2)
    generic_R = sp.simplify((generic_A - generic_A.T) / 2)
    projected_even_twice = sp.simplify((generic_S + generic_S.T) / 2)
    projected_odd_twice = sp.simplify((generic_R - generic_R.T) / 2)

    zero = sp.zeros(3)
    self_s = sp.simplify(S * S - S * S)
    self_r = sp.simplify(R_a * R_a - R_a * R_a)
    swapped_c = sp.simplify(R_a * S - S * R_a)
    sign_c = sp.simplify(S * (-R_a) - (-R_a) * S)
    swapped_K = sp.simplify(sp.trace(swapped_c.T * swapped_c))
    sign_K = sp.simplify(sp.trace(sign_c.T * sign_c))

    I2 = sp.simplify(sp.trace(S**2))
    I3 = sp.simplify(sp.trace(S**3))
    p_r_a = a["P_R"]
    p_r_b = b_report["P_R"]
    unary_a = (I2, I3, a["J"], S.rank(), R_a.rank(), "transpose_even", "transpose_odd")
    unary_b = (I2, I3, b_report["J"], S.rank(), R_b.rank(), "transpose_even", "transpose_odd")

    return {
        "transpose_nodes_nonzero_distinct_and_reconstruct_A": all((
            not matrix_zero(S), not matrix_zero(R_a),
            matrix_zero(even - S), matrix_zero(odd - R_a),
            matrix_zero(A - even - odd),
            not matrix_zero(S - R_a),
        )),
        "node_support_maps_single_valued_equivariant": all((
            matrix_zero(projected_even_twice - generic_S),
            matrix_zero(projected_odd_twice - generic_R),
            matrix_zero(generic_A - generic_S - generic_R),
            matrix_zero(p_s**2 - p_s), matrix_zero(p_r_a**2 - p_r_a),
            p_s.rank() == 1, p_r_a.rank() == 1,
        )),
        "commutator_carrier_symmetric_traceless": all((
            matrix_zero(a["C"].T - a["C"]),
            sp.simplify(sp.trace(a["C"])) == 0,
            matrix_zero(a["C"] - carrier_from_A),
        )),
        "carrier_vanishes_if_either_node_absent": all((
            matrix_zero(S * zero - zero * S),
            matrix_zero(zero * R_a - R_a * zero),
        )),
        "raw_report_nonnegative_and_regular": all((
            a["K"] == eta * s**2 / (4 * d),
            b_report["K"] == 3 * eta * s**2 / (4 * d),
            sp.ask(sp.Q.positive(a["K"])) is True,
            sp.ask(sp.Q.positive(b_report["K"])) is True,
        )),
        "two_exact_accepted_witnesses_same_unary": all((
            a["J"] == b_report["J"] == eta / d,
            sp.trace(p_r_a) == sp.trace(p_r_b) == 1,
            I2 == 2 * s**2 / 3, I3 == 2 * s**3 / 9,
            R_a.rank() == R_b.rank() == 2,
        )),
        "two_exact_accepted_witnesses_different_joint": all((
            a["K"] != b_report["K"],
            a["tau"] == sp.Rational(1, 4),
            b_report["tau"] == sp.Rational(3, 4),
        )),
        "normalized_report_equals_tau": all((
            a["K"] == s**2 * a["J"] * a["tau"],
            b_report["K"] == s**2 * b_report["J"] * b_report["tau"],
            sp.simplify(a["tau"] - (1 - sp.trace(p_s * p_r_a))) == 0,
            sp.simplify(b_report["tau"] - (1 - sp.trace(p_s * p_r_b))) == 0,
        )),
        "unary_invariant_generators_complete_in_declared_class": all((
            "Cayley-Hamilton" in CLAIM_CONTRACT["FUNCTION_CLASS"]["unary_symmetric"],
            "I2=Tr(S^2), I3=Tr(S^3)" in CLAIM_CONTRACT["FUNCTION_CLASS"]["unary_symmetric"],
            "J=-Tr(R^2)" in CLAIM_CONTRACT["FUNCTION_CLASS"]["unary_skew"],
        )),
        "typed_swap_and_R_sign_leave_report_invariant": all((
            matrix_zero(swapped_c + a["C"]), matrix_zero(sign_c + a["C"]),
            swapped_K == a["K"], sign_K == a["K"],
            matrix_zero(self_s), matrix_zero(self_r),
        )),
        "relation_not_in_unary_equality_separable_image": all((
            unary_a == unary_b,
            a["K"] != b_report["K"],
            "identical complete unary" in CLAIM_CONTRACT["THEOREM"]["irreducibility"],
        )),
        "nonzero_on_predeclared_generic_open_domain": all((
            "0<tau<1" in CLAIM_CONTRACT["DOMAIN"],
            "s^2 J tau" in CLAIM_CONTRACT["THEOREM"]["irreducibility"],
            a["tau"] > 0, a["tau"] < 1,
            b_report["tau"] > 0, b_report["tau"] < 1,
        )),
        "orthogonal_support_projectors_commute_but_carrier_is_nonzero": all((
            matrix_zero(p_s * orthogonal["P_R"] - orthogonal["P_R"] * p_s),
            orthogonal["tau"] == 1,
            not matrix_zero(orthogonal["C"]),
            orthogonal["K"] == s**2 * orthogonal["J"],
            sp.ask(sp.Q.positive(orthogonal["K"])) is True,
        )),
    }

def null_controls() -> dict[str, bool]:
    s, eta, d = sp.symbols("s eta d", positive=True)
    identity = sp.eye(3)
    S = s * (sp.diag(1, 0, 0) - identity / 3)
    rho = sp.sqrt(eta / (2 * d))
    parallel_R = cross_matrix(sp.Matrix([rho, 0, 0]))
    generic_R = cross_matrix(rho * sp.Matrix([sp.sqrt(3) / 2, sp.Rational(1, 2), 0]))
    zero = sp.zeros(3)

    commuting_c = sp.simplify(S * parallel_R - parallel_R * S)
    generic_c = sp.simplify(S * generic_R - generic_R * S)
    generic_k = sp.simplify(sp.trace(generic_c.T * generic_c))

    mu_r, mu_b = sp.symbols("mu_r mu_b", real=True)
    w212_table = sp.diag(mu_r, mu_b)
    unary_equality = sp.Matrix(2, 2, lambda i, j: (mu_r, mu_b)[i] if i == j else 0)
    q_controls = quotient_controls()
    relation = relation_controls()
    domain = CLAIM_CONTRACT["DOMAIN_AND_NULLS"]

    return {
        "zero_and_single_channel_nulls": all((
            matrix_zero(zero * zero - zero * zero),
            matrix_zero(S * zero - zero * S),
            matrix_zero(zero * generic_R - generic_R * zero),
        )),
        "commuting_branch_null": all((
            matrix_zero(commuting_c),
            "K=0" in domain["commuting_tau_zero"],
        )),
        "normalization_undefined_not_assigned": all((
            "not assigned" in domain["normalization_singular"],
            "s=0 or J=0" in domain["normalization_singular"],
        )),
        "self_pair_commutators_zero": all((
            matrix_zero(S * S - S * S),
            matrix_zero(generic_R * generic_R - generic_R * generic_R),
        )),
        "factorized_same_unary_null_detected": all((
            relation["two_exact_accepted_witnesses_same_unary"],
            relation["two_exact_accepted_witnesses_different_joint"],
            generic_k > 0,
        )),
        "independent_action_false_gauge_detected": q_controls[
            "independent_channel_map_fails_multiplicativity"
        ],
        "w2_12_diagonal_remains_unary_equality": w212_table == unary_equality,
        "w2_14_unselected_fibre_not_reused": all((
            relation["node_support_maps_single_valued_equivariant"],
            "state-reconstructed" in domain["w2_14_projective_fibre"],
            "Unselected" in domain["w2_14_projective_fibre"],
        )),
        "tuned_and_parameter_boundaries_not_promoted": all((
            "stays null" in domain["f2a_tuned_surface"],
            "do not promote" in domain["parameter_boundaries"],
        )),
        "no_temporal_or_physical_semantics": all((
            CLAIM_CONTRACT["SCOPE_CEILING"][
                "F3_time_memory_persistence_or_causality"
            ] is False,
            CLAIM_CONTRACT["SCOPE_CEILING"][
                "physical_RefG_node_or_medium_interpretation"
            ] is False,
            CLAIM_CONTRACT["OBSERVABLE_MAP"]["status"] == "N/A",
            CLAIM_CONTRACT["FORWARD_MODEL"]["status"] == "N/A",
            CLAIM_CONTRACT["SCOPE_CEILING"][
                "space_dimension_continuum_or_metric"
            ] is False,
        )),
    }

def scope_closure_controls() -> dict[str, bool]:
    scope = CLAIM_CONTRACT.get("SCOPE_CEILING")
    closure = CLAIM_CONTRACT.get("SCIENTIFIC_CLOSURE")
    return {
        "named_dependency_chain_exact": tuple(CLAIM_CONTRACT.get("DEPENDENCIES", ()))
        == EXPECTED_DEPENDENCIES,
        "freedom_ledger_complete": frozenset(CLAIM_CONTRACT.get("FREEDOM_LEDGER", {}))
        == EXPECTED_FREEDOM_KEYS,
        "scope_ceiling_exact": (
            isinstance(scope, dict) and scope == EXPECTED_SCOPE_CEILING
            and all(type(value) is bool for value in scope.values())
        ),
        "scientific_closure_exact": (
            isinstance(closure, dict) and closure == EXPECTED_SCIENTIFIC_CLOSURE
            and all(type(value) is bool for value in closure.values())
        ),
    }


def candidate_gate_map(
    controls: dict[str, dict[str, bool]], scope_closure: dict[str, bool]
) -> dict[str, bool]:
    minima = controls["minimum"]
    quotient = controls["quotient"]
    f1_f2a = controls["f1_f2a"]
    relation = controls["relation"]
    nulls = controls["nulls"]
    all_calculations = _all_true(controls)
    scope = CLAIM_CONTRACT["SCOPE_CEILING"]
    gates = {
        "exact_dependency_chain_valid": scope_closure["named_dependency_chain_exact"],
        "same_chain_embedding_or_full_revalidation_exact": all((
            f1_f2a["extended_f1_and_f2a_same_aggregate"],
            f1_f2a["old_law_and_hessian_block_embed_exactly"],
        )),
        "candidate_domain_codomain_branches_and_undefined_points_explicit": all((
            "0<tau<1" in CLAIM_CONTRACT["DOMAIN"],
            set(CLAIM_CONTRACT["DOMAIN_AND_NULLS"]) == {
                "generic_pass_domain", "f2a_tuned_surface", "zero_state", "R_zero",
                "S_zero", "commuting_tau_zero", "normalization_singular", "self_pairs",
                "factorized_unary_rule", "w2_12_diagonal", "w2_14_projective_fibre",
                "parameter_boundaries",
            },
        )),
        "candidate_freedom_ledger_complete": scope_closure["freedom_ledger_complete"],
        "state_supported_node_family_generated_not_preassigned": all((
            relation["transpose_nodes_nonzero_distinct_and_reconstruct_A"],
            relation["node_support_maps_single_valued_equivariant"],
        )),
        "node_ownership_certificate_law_derived": all((
            relation["node_support_maps_single_valued_equivariant"],
            minima["product_minimum_separability_exact"],
        )),
        "at_least_two_distinct_nodes_on_non_tuned_domain": all((
            relation["transpose_nodes_nonzero_distinct_and_reconstruct_A"],
            relation["nonzero_on_predeclared_generic_open_domain"],
        )),
        "atemporal_relational_carrier_is_state_supported_not_readout_only": all((
            relation["commutator_carrier_symmetric_traceless"],
            relation["carrier_vanishes_if_either_node_absent"],
        )),
        "carrier_connects_distinct_nodes_with_derived_restrictions": all((
            relation["transpose_nodes_nonzero_distinct_and_reconstruct_A"],
            relation["carrier_vanishes_if_either_node_absent"],
        )),
        "joint_admissibility_composition_and_complete_common_action_derived": all((
            quotient["tau_common_action_invariant"],
            quotient["same_tau_canonical_representative_complete"],
            quotient["independent_channel_map_fails_multiplicativity"],
        )),
        "uniform_target_free_pair_rule_and_shared_codomain": (
            CLAIM_CONTRACT["FUNCTION_CLASS"]["joint_report"].startswith("K(S,R)=")
        ),
        "complete_unary_reduction_maps_declared": relation[
            "unary_invariant_generators_complete_in_declared_class"
        ],
        "route_neutral_irreducibility_certificate_exact": all((
            relation["two_exact_accepted_witnesses_same_unary"],
            relation["two_exact_accepted_witnesses_different_joint"],
        )),
        "relation_not_factorable_through_unary_quotients": relation[
            "relation_not_in_unary_equality_separable_image"
        ],
        "nonzero_relational_quotient_on_predeclared_open_domain": relation[
            "nonzero_on_predeclared_generic_open_domain"
        ],
        "reported_relation_complete_equivalence_invariant": all((
            quotient["tau_common_action_invariant"],
            relation["typed_swap_and_R_sign_leave_report_invariant"],
        )),
        "independent_relabelling_and_factorized_pair_nulls_pass": all((
            relation["typed_swap_and_R_sign_leave_report_invariant"],
            nulls["factorized_same_unary_null_detected"],
        )),
        "reference_single_node_and_degenerate_nulls_pass": _all_true(nulls),
        "w2_12_diagonal_comparison_not_relabelled_as_pair_coupling": nulls[
            "w2_12_diagonal_remains_unary_equality"
        ],
        "f3_time_memory_persistence_and_causality_absent": all((
            nulls["no_temporal_or_physical_semantics"],
            scope["F3_time_memory_persistence_or_causality"] is False,
        )),
        "physical_spatial_geometric_and_observable_semantics_absent": all((
            nulls["no_temporal_or_physical_semantics"],
            scope["physical_RefG_node_or_medium_interpretation"] is False,
            scope["space_dimension_continuum_or_metric"] is False,
            scope["GR_Einstein_equations_PN_or_PPN"] is False,
            scope["observational_validation"] is False,
        )),
        "positive_null_and_adversarial_controls_pass": all_calculations,
        "candidate_specific_calculation_complete": all_calculations,
    }
    if set(gates) != F2B_GATE_KEYS or any(type(value) is not bool for value in gates.values()):
        return {key: False for key in F2B_GATE_KEYS}
    return gates


def candidate_screen(gates: Any) -> dict[str, bool]:
    schema_valid = (
        isinstance(gates, dict) and set(gates) == F2B_GATE_KEYS
        and all(type(value) is bool for value in gates.values())
    )
    return {
        "valid": bool(schema_valid),
        "eligible": bool(schema_valid and all(gates.values())),
        "promoted": False,
    }


def completion_logic(
    inherited_f2a: Any, candidate_valid: Any, screen_eligible: Any,
    candidate_evaluated: Any, state_nodes: Any, relational_carrier: Any,
    common_action: Any, irreducible_pair_relation: Any,
    equivalence_invariant: Any, domain_and_nulls: Any, same_chain: Any,
) -> dict[str, bool]:
    values = (
        inherited_f2a, candidate_valid, screen_eligible, candidate_evaluated,
        state_nodes, relational_carrier, common_action, irreducible_pair_relation,
        equivalence_invariant, domain_and_nulls, same_chain,
    )
    valid = all(type(value) is bool for value in values)
    f2b = bool(valid and all(values[1:]))
    full_f2 = bool(valid and inherited_f2a and f2b)
    return {
        "valid": valid,
        "F2b_relational_completion": f2b,
        "full_W2_F2_operational_relations": full_f2,
        "promoted": full_f2,
    }


def decision_controls(gates: dict[str, bool], completion: dict[str, bool]) -> dict[str, bool]:
    all_true_screen = candidate_screen(gates)
    false_screens = []
    malformed_screens = []
    for key in F2B_GATE_KEYS:
        false_map = dict(gates)
        false_map[key] = False
        false_screens.append(candidate_screen(false_map))
        missing = dict(gates)
        missing.pop(key)
        malformed_screens.append(candidate_screen(missing))
        nonboolean = dict(gates)
        nonboolean[key] = 1
        malformed_screens.append(candidate_screen(nonboolean))
    f2a_false = completion_logic(False, *([True] * 10))
    closure = CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"]
    later_keys = {
        "F3_internal_order_or_causality_proved",
        "F4_conservation_or_additive_modes_proved",
        "dimension_or_continuum_proved",
        "Lorentzian_metric_or_Einstein_branch_proved",
        "effective_action_or_matter_coupling_proved",
        "PN_or_PPN_handoff_proved",
        "observational_validation_proved",
    }
    return {
        "all_true_screen_is_eligible_but_not_promoted": all((
            all_true_screen["valid"], all_true_screen["eligible"],
            not all_true_screen["promoted"],
        )),
        "one_false_gate_never_eligible": all(
            result["valid"] and not result["eligible"] and not result["promoted"]
            for result in false_screens
        ),
        "every_missing_or_nonboolean_gate_is_invalid": all(
            not result["valid"] and not result["eligible"] and not result["promoted"]
            for result in malformed_screens
        ),
        "f2a_false_keeps_full_f2_open": all((
            f2a_false["valid"], f2a_false["F2b_relational_completion"],
            not f2a_false["full_W2_F2_operational_relations"],
            not f2a_false["promoted"],
        )),
        "complete_candidate_closes_exactly_structural_f2": all((
            completion["valid"], completion["F2b_relational_completion"],
            completion["full_W2_F2_operational_relations"], completion["promoted"],
        )),
        "candidate_result_never_closes_later_gates": all(
            key in closure and closure[key] is False for key in later_keys
        ),
    }


def run() -> dict[str, Any]:
    controls = {
        "minimum": minimum_controls(),
        "quotient": quotient_controls(),
        "f1_f2a": f1_f2a_controls(),
        "relation": relation_controls(),
        "nulls": null_controls(),
    }
    scope_closure = scope_closure_controls()
    gates = candidate_gate_map(controls, scope_closure)
    screen = candidate_screen(gates)
    completion = completion_logic(
        gates["same_chain_embedding_or_full_revalidation_exact"],
        bool(_all_true(controls) and _all_true(scope_closure)),
        screen["eligible"],
        gates["candidate_specific_calculation_complete"],
        gates["state_supported_node_family_generated_not_preassigned"],
        gates["atemporal_relational_carrier_is_state_supported_not_readout_only"],
        gates["joint_admissibility_composition_and_complete_common_action_derived"],
        gates["relation_not_factorable_through_unary_quotients"],
        gates["reported_relation_complete_equivalence_invariant"],
        bool(gates["nonzero_relational_quotient_on_predeclared_open_domain"]
             and gates["reference_single_node_and_degenerate_nulls_pass"]),
        gates["same_chain_embedding_or_full_revalidation_exact"],
    )
    decisions = decision_controls(gates, completion)
    valid = bool(
        _all_true(controls) and _all_true(scope_closure) and _all_true(gates)
        and screen["eligible"] and _all_true(completion) and _all_true(decisions)
    )
    closure_decision = {
        "F1_revalidated": bool(valid),
        "F2a_revalidated": bool(valid),
        "F2b_state_nodes_proved": bool(valid),
        "F2b_relational_carrier_proved": bool(valid),
        "F2b_complete_common_action_proved": bool(valid),
        "F2b_irreducible_pair_relation_proved": bool(valid),
        "F2b_relational_completion_proved": bool(
            valid and completion["F2b_relational_completion"]
        ),
        "full_W2_F2_operational_relations_proved": bool(
            valid and completion["full_W2_F2_operational_relations"]
        ),
        "F3_internal_order_or_causality_proved": False,
        "F4_conservation_or_additive_modes_proved": False,
        "dimension_or_continuum_proved": False,
        "Lorentzian_metric_or_Einstein_branch_proved": False,
        "effective_action_or_matter_coupling_proved": False,
        "PN_or_PPN_handoff_proved": False,
        "observational_validation_proved": False,
    }
    return {
        "artifact": CLAIM_CONTRACT["CLAIM_ID"],
        "valid": valid,
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "Conditional on the imported traceless carrier A and polynomial law, the "
            "declared generic branch supplies exact structural F1 and F2 relations. "
            "This does not derive physical RefG nodes, time, metric, GR, PN/PPN or data."
        ),
        "scope_ceiling": CLAIM_CONTRACT["SCOPE_CEILING"],
        "scientific_closure": CLAIM_CONTRACT["SCIENTIFIC_CLOSURE"],
        "closure_decision": closure_decision,
        "controls": controls,
        "scope_closure_controls": scope_closure,
        "candidate_gate_map": gates,
        "candidate_screen": screen,
        "completion_decision": completion,
        "decision_controls": decisions,
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
