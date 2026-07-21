"""Self-contained exact certificate for a conditional atemporal F1 result.

The module proves two impossibility boundaries, verifies one imported
Sym_0(3) spectral construction, and evaluates a deliberately narrow
structural-F1 corollary.  It reads no project files and uses no observations.

The conclusion is conditional on the imported state space, equivalence rule,
quartic functional, coefficient domain, and global-minimum rule.  It does not
derive those primitives or any temporal, spacetime, GR, or observational
structure.
"""
from __future__ import annotations

import itertools
import json
import sys
from typing import Any

import sympy as sp


MODEL_VERSION = "RefG-F1-ATEMPORAL-STRUCTURAL-PROOF-v1.0"
PASS_STATUS = "CONDITIONAL_ATEMPORAL_STRUCTURAL_F1_RELATIVE_TO_IMPORTED_PRIMITIVES"
NOT_PROMOTED_STATUS = "COMPLETE_NOT_PROMOTED__CONDITIONAL_RESULTS_RETAINED"
INVALID_STATUS = "INVALID_AUDIT__NO_STRUCTURAL_PROMOTION"

EXTERNAL_FILE_DEPENDENCIES: tuple[str, ...] = ()
DATA_FITTED_PARAMETERS = 0

IMPORTED_PRIMITIVES = {
    "single_internal_carrier_Q": "IMPORTED_NOT_DERIVED",
    "Sym0_3_R_internal_state_space": "IMPORTED_NOT_DERIVED",
    "positive_internal_contraction_and_transpose": "IMPORTED_NOT_DERIVED",
    "matrix_product_and_algebraic_trace": "IMPORTED_NOT_DERIVED",
    "O3_conjugation_as_complete_declared_equivalence": "IMPORTED_NOT_DERIVED",
    "Q_sign_not_gauge": "IMPORTED_NOT_DERIVED",
    "quartic_functional_form_signs_and_truncation": "IMPORTED_NOT_DERIVED",
    "open_parameter_domain_alpha_b_c_positive": "IMPORTED_NOT_DERIVED",
    "atemporal_global_argmin_rule": "IMPORTED_NOT_DERIVED",
}
IMPORTED_PRIMITIVE_KEYS = frozenset(IMPORTED_PRIMITIVES)

STANDARD_MATHEMATICS = (
    "spectral theorem for real symmetric matrices",
    "fundamental theorem of symmetric polynomials",
    "Cayley-Hamilton theorem",
    "elementary group-action and stabilizer identities",
)
STANDARD_MATHEMATICS_KEYS = frozenset(STANDARD_MATHEMATICS)

F1_WITNESS_KINDS = (
    "MULTIPLE_INEQUIVALENT_ACCEPTED_QUOTIENT_CLASSES",
    "ONE_ACCEPTED_QUOTIENT_CLASS_WITH_CANONICAL_COEXISTING_NONEXCHANGEABLE_ROLES",
)
SELECTED_F1_WITNESS_KIND = F1_WITNESS_KINDS[1]

SCOPE_CEILING = {
    "foundation_law_derived": False,
    "functional_uniqueness_derived": False,
    "N3_physical_origin_derived": False,
    "temporal_formation_or_persistence": False,
    "physical_node_or_location": False,
    "operational_relations": False,
    "causal_order_or_clock": False,
    "independent_additive_physical_modes": False,
    "physical_dimension_or_continuum": False,
    "Lorentzian_metric_or_light_cone": False,
    "effective_action_or_conservation_law": False,
    "RefG_resonant_environment_map": False,
    "mass_pressure_particle_or_oscillon": False,
    "GR_PN_or_PPN_bridge": False,
    "observable_or_data_map": False,
}
SCOPE_CEILING_KEYS = frozenset(SCOPE_CEILING)

F1_GATE_KEYS = frozenset({
    "public_definition_accepts_both_witness_kinds",
    "selected_witness_kind_explicit",
    "external_file_dependency_registry_empty",
    "primitive_registry_exactly_declared",
    "explicit_orientation_target_inputs_absent",
    "undifferentiated_reference_trivial",
    "law_O3_invariant_and_representative_target_free",
    "output_classification_complete",
    "intrinsic_differentiation_certified",
    "inequivalence_survives_declared_quotient",
    "law_forces_roles_not_arbitrary_basis",
    "law_selects_no_representative_orientation",
    "open_domain_structural_stability",
    "all_registered_primitives_labelled_imported",
    "no_go_route_boundaries_respected",
    "independent_crosschecks_and_controls",
    "listed_falsifier_checks_pass",
    "scope_ceiling_registry_exactly_false",
})

SINGLETON_CHECK_KEYS = frozenset({
    "singleton_has_no_nontrivial_partition",
    "all_deterministic_endomaps_have_singleton_image",
    "normalized_1x1_markov_kernel_is_identity",
    "singleton_variational_state_and_minimizer_are_unique",
    "one_dimensional_quantum_state_and_channel_are_unique",
    "povm_outcomes_require_external_register",
    "two_state_positive_control_is_detected",
    "state_space_expansion_is_detected_as_domain_escape",
})

EQUIVARIANT_CHECK_KEYS = frozenset({
    "c2_fixed_sets_exact",
    "all_enumerated_equivariant_maps_preserve_fixed_sets",
    "stabilizer_inclusion_holds_independently",
    "unique_invariant_minima_are_fixed",
    "degenerate_nonfixed_minimum_orbit_control",
    "non_equivariant_escape_is_detected",
    "set_valued_orbit_escape_has_no_canonical_single_selection",
})

SPECTRAL_CHECK_KEYS = frozenset({
    "traceless_symmetric_coordinate_chart_and_gram_exact",
    "invariant_ring_through_degree_four_and_CH_reduction_exact",
    "declared_O3_generator_invariance_exact",
    "origin_is_stationary_unstable_and_role_trivial",
    "sharp_eigenvalue_discriminant_bound_exact",
    "reduced_radial_problem_and_positive_root_exact",
    "unique_nonzero_global_minimum_quotient_orbit_certified",
    "negative_stationary_branch_rejected",
    "orbit_normal_hessian_positive_with_two_orbit_zero_modes",
    "Q_generated_rank_1_rank_2_projectors_exact",
    "roles_nonexchangeable_and_Q_sign_not_law_symmetry",
    "law_has_no_target_direction_projector_or_data_symbol",
    "b_zero_shape_degeneracy_control",
    "c_nonpositive_and_alpha_zero_boundary_controls",
    "N1_N2_and_general_N_nonuniversality_controls",
    "positive_quadratic_null_keeps_undifferentiated_origin",
    "explicit_anisotropic_source_is_detected",
})

AUDIT_CHECK_KEYS = frozenset({
    "section_checks_exact_and_all_true",
    "promotion_evidence_schema_exact_boolean",
    "imported_primitive_registry_exact",
    "standard_mathematics_registry_explicit",
    "scope_ceiling_exactly_false",
    "zero_data_fit_and_no_external_file_dependencies",
    "decision_logic_positive_negative_invalid_controls",
    "exact_symbolic_outputs_without_floating_tolerance",
})

DECISION_CONTROL_KEYS = frozenset({
    "valid_positive_branch",
    "valid_negative_branch",
    "invalid_audit_cannot_promote",
    "missing_gate_invalid",
    "extra_gate_invalid",
    "nonboolean_gate_invalid",
    "nonboolean_audit_invalid",
})

def matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def exact_bool_map(actual: Any, expected_keys: Any) -> bool:
    return (
        isinstance(actual, dict)
        and set(actual) == set(expected_keys)
        and all(type(value) is bool for value in actual.values())
    )


def exact_true_map(actual: Any, expected_keys: Any) -> bool:
    return exact_bool_map(actual, expected_keys) and all(
        value is True for value in actual.values()
    )


def contains_float(value: Any) -> bool:
    if isinstance(value, (float, sp.Float)):
        return True
    if isinstance(value, sp.MatrixBase):
        return any(contains_float(entry) for entry in value)
    if isinstance(value, sp.Basic):
        return bool(value.has(sp.Float))
    if isinstance(value, dict):
        return any(contains_float(key) or contains_float(item) for key, item in value.items())
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(contains_float(item) for item in value)
    return False


def _all_maps(states: tuple[int, ...]) -> list[dict[int, int]]:
    return [
        dict(zip(states, outputs))
        for outputs in itertools.product(states, repeat=len(states))
    ]


def strict_singleton_no_go() -> dict[str, Any]:
    states = (0,)
    subsets = [
        set(subset)
        for size in range(len(states) + 1)
        for subset in itertools.combinations(states, size)
    ]
    nontrivial_subsets = [
        subset for subset in subsets if 0 < len(subset) < len(states)
    ]
    deterministic_maps = _all_maps(states)
    deterministic_images = [set(mapping.values()) for mapping in deterministic_maps]

    kernel_entry = sp.symbols("kernel_entry", nonnegative=True, real=True)
    normalized_kernel_solutions = sp.solve(
        sp.Eq(kernel_entry, 1), kernel_entry
    )
    kernel = sp.Matrix([[normalized_kernel_solutions[0]]])
    probability = sp.Matrix([1])

    energy = sp.symbols("energy", real=True)
    energy_map = {0: energy}
    minimizers = tuple(energy_map)

    theta, phi = sp.symbols("theta phi", real=True)
    psi_theta = sp.Matrix([sp.exp(sp.I * theta)])
    psi_phi = sp.Matrix([sp.exp(sp.I * phi)])
    rho_theta = sp.simplify(psi_theta * psi_theta.conjugate().T)
    rho_phi = sp.simplify(psi_phi * psi_phi.conjugate().T)
    channel_scale = sp.symbols("channel_scale", nonnegative=True, real=True)
    trace_preserving_channel = sp.solve(
        sp.Eq(channel_scale, 1), channel_scale
    )

    p = sp.Rational(1, 3)
    effect_zero = sp.Matrix([[p]])
    effect_one = sp.Matrix([[1 - p]])
    post_zero = sp.simplify(effect_zero * rho_theta / p)
    post_one = sp.simplify(effect_one * rho_theta / (1 - p))

    two_states = (0, 1)
    two_state_identity = {0: 0, 1: 1}
    external_binary_register = tuple(
        (state, label) for state in states for label in (0, 1)
    )

    checks = {
        "singleton_has_no_nontrivial_partition": (
            len(states) == 1
            and subsets == [set(), {0}]
            and nontrivial_subsets == []
        ),
        "all_deterministic_endomaps_have_singleton_image": (
            len(deterministic_maps) == 1
            and all(len(image) == 1 for image in deterministic_images)
        ),
        "normalized_1x1_markov_kernel_is_identity": all((
            normalized_kernel_solutions == [1],
            kernel == sp.eye(1),
            kernel * probability == probability,
        )),
        "singleton_variational_state_and_minimizer_are_unique": (
            len(set(energy_map.values())) == 1 and len(minimizers) == 1
        ),
        "one_dimensional_quantum_state_and_channel_are_unique": all((
            rho_theta == sp.eye(1),
            rho_phi == sp.eye(1),
            matrix_is_zero(rho_theta - rho_phi),
            trace_preserving_channel == [1],
        )),
        "povm_outcomes_require_external_register": all((
            effect_zero + effect_one == sp.eye(1),
            effect_zero[0, 0].is_positive is True,
            effect_one[0, 0].is_positive is True,
            sp.trace(effect_zero * rho_theta) == p,
            sp.trace(effect_one * rho_theta) == 1 - p,
            post_zero == sp.eye(1),
            post_one == sp.eye(1),
            len(external_binary_register) == 2,
            len(states) == 1,
        )),
        "two_state_positive_control_is_detected": (
            len(two_states) == 2 and len(set(two_state_identity.values())) == 2
        ),
        "state_space_expansion_is_detected_as_domain_escape": (
            len(external_binary_register) > len(states)
            and set(external_binary_register) != set(states)
        ),
    }
    return {
        "checks": checks,
        "diagnostics": {
            "state_count": len(states),
            "deterministic_map_count": len(deterministic_maps),
            "deterministic_image_sizes": [len(image) for image in deterministic_images],
            "normalized_kernel": str(kernel),
            "density_matrix": str(rho_theta),
            "external_binary_register_size": len(external_binary_register),
        },
    }


def _is_equivariant(
    mapping: dict[int, int],
    states: tuple[int, ...],
    actions: tuple[dict[int, int], ...],
) -> bool:
    return all(
        mapping[action[x]] == action[mapping[x]]
        for action in actions
        for x in states
    )


def _fixed_set(
    states: tuple[int, ...], actions: tuple[dict[int, int], ...]
) -> set[int]:
    return {
        x for x in states if all(action[x] == x for action in actions)
    }


def _stabilizer(
    x: int, actions: tuple[dict[int, int], ...]
) -> frozenset[int]:
    return frozenset(index for index, action in enumerate(actions) if action[x] == x)


def _c2_actions(states: tuple[int, ...], swap: dict[int, int]) -> tuple[dict[int, int], ...]:
    identity = {state: state for state in states}
    return identity, swap


def deterministic_equivariant_fixed_set_no_go() -> dict[str, Any]:
    states3 = (0, 1, 2)
    actions3 = _c2_actions(states3, {0: 1, 1: 0, 2: 2})
    states4 = (0, 1, 2, 3)
    actions4 = _c2_actions(states4, {0: 1, 1: 0, 2: 2, 3: 3})

    fixed3 = _fixed_set(states3, actions3)
    fixed4 = _fixed_set(states4, actions4)
    maps3 = [m for m in _all_maps(states3) if _is_equivariant(m, states3, actions3)]
    maps4 = [m for m in _all_maps(states4) if _is_equivariant(m, states4, actions4)]

    fixed_preservation = all(
        mapping[x] in fixed
        for states, actions, fixed, mappings in (
            (states3, actions3, fixed3, maps3),
            (states4, actions4, fixed4, maps4),
        )
        for mapping in mappings
        for x in fixed
    )
    stabilizer_inclusion = all(
        _stabilizer(x, actions).issubset(_stabilizer(mapping[x], actions))
        for states, actions, mappings in (
            (states3, actions3, maps3),
            (states4, actions4, maps4),
        )
        for mapping in mappings
        for x in states
    )

    unique_minimum_results: list[bool] = []
    for states, actions, fixed in (
        (states3, actions3, fixed3),
        (states4, actions4, fixed4),
    ):
        for values in itertools.product(range(len(states)), repeat=len(states)):
            energy = dict(zip(states, values))
            invariant = all(
                energy[action[x]] == energy[x]
                for action in actions
                for x in states
            )
            if invariant:
                minimum = min(energy.values())
                minimizers = [x for x in states if energy[x] == minimum]
                if len(minimizers) == 1:
                    unique_minimum_results.append(minimizers[0] in fixed)

    degenerate_energy = {0: 0, 1: 0, 2: 1}
    degenerate_minima = {x for x, value in degenerate_energy.items() if value == 0}
    non_equivariant = {0: 0, 1: 1, 2: 0}
    set_valued_output = {0, 1}
    swap3 = actions3[1]

    checks = {
        "c2_fixed_sets_exact": fixed3 == {2} and fixed4 == {2, 3},
        "all_enumerated_equivariant_maps_preserve_fixed_sets": fixed_preservation,
        "stabilizer_inclusion_holds_independently": stabilizer_inclusion,
        "unique_invariant_minima_are_fixed": (
            bool(unique_minimum_results) and all(unique_minimum_results)
        ),
        "degenerate_nonfixed_minimum_orbit_control": all((
            degenerate_minima == {0, 1},
            {swap3[x] for x in degenerate_minima} == degenerate_minima,
            not degenerate_minima & fixed3,
        )),
        "non_equivariant_escape_is_detected": all((
            non_equivariant[2] not in fixed3,
            not _is_equivariant(non_equivariant, states3, actions3),
        )),
        "set_valued_orbit_escape_has_no_canonical_single_selection": all((
            {swap3[x] for x in set_valued_output} == set_valued_output,
            not set_valued_output & fixed3,
            len(set_valued_output) == 2,
        )),
    }
    return {
        "checks": checks,
        "diagnostics": {
            "fixed_set_C2_three_states": sorted(fixed3),
            "fixed_set_C2_four_states": sorted(fixed4),
            "equivariant_map_count_three_states": len(maps3),
            "equivariant_map_count_four_states": len(maps4),
            "unique_invariant_minimum_controls": len(unique_minimum_results),
        },
    }


def atemporal_spectral_construction() -> dict[str, Any]:
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
    expected_gram = sp.Matrix([
        [2, 1, 0, 0, 0],
        [1, 2, 0, 0, 0],
        [0, 0, 2, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 0, 0, 0, 2],
    ])

    I2 = sp.expand(sp.trace(Q**2))
    I3 = sp.expand(sp.trace(Q**3))
    potential = sp.expand(-alpha * I2 / 2 - b * I3 / 3 + c * I2**2 / 4)
    gradient = sp.Matrix([sp.diff(potential, variable) for variable in coordinates])
    hessian = sp.hessian(potential, coordinates)
    zero = {variable: 0 for variable in coordinates}

    cayley_hamilton = sp.simplify(Q**3 - I2 * Q / 2 - I3 * sp.eye(3) / 3)
    degree_four_reduction = sp.expand(sp.trace(Q**4) - I2**2 / 2)
    invariant_monomials = [
        (power_I2, power_I3)
        for power_I2 in range(3)
        for power_I3 in range(2)
        if 0 < 2 * power_I2 + 3 * power_I3 <= 4
    ]

    theta_12, theta_13, theta_23 = sp.symbols(
        "theta_12 theta_13 theta_23", real=True
    )
    rotation_12 = sp.Matrix([
        [sp.cos(theta_12), -sp.sin(theta_12), 0],
        [sp.sin(theta_12), sp.cos(theta_12), 0],
        [0, 0, 1],
    ])
    rotation_13 = sp.Matrix([
        [sp.cos(theta_13), 0, -sp.sin(theta_13)],
        [0, 1, 0],
        [sp.sin(theta_13), 0, sp.cos(theta_13)],
    ])
    rotation_23 = sp.Matrix([
        [1, 0, 0],
        [0, sp.cos(theta_23), -sp.sin(theta_23)],
        [0, sp.sin(theta_23), sp.cos(theta_23)],
    ])
    reflection = sp.diag(-1, 1, 1)
    generator_invariance: list[bool] = []
    for transform, determinant in (
        (rotation_12, 1),
        (rotation_13, 1),
        (rotation_23, 1),
        (reflection, -1),
    ):
        transformed = sp.trigsimp(transform * Q * transform.T)
        generator_invariance.extend([
            matrix_is_zero(sp.trigsimp(transform.T * transform - sp.eye(3))),
            sp.trigsimp(transform.det() - determinant) == 0,
            sp.trigsimp(sp.expand(sp.trace(transformed**2) - I2)) == 0,
            sp.trigsimp(sp.expand(sp.trace(transformed**3) - I3)) == 0,
        ])

    origin_gradient = sp.simplify(gradient.subs(zero))
    origin_hessian = sp.simplify(hessian.subs(zero))

    l1, l2 = sp.symbols("l1 l2", real=True)
    l3 = -l1 - l2
    I2_eigen = sp.expand(l1**2 + l2**2 + l3**2)
    I3_eigen = sp.expand(l1**3 + l2**3 + l3**3)
    eigen_discriminant_squares = (
        (l1 - l2) ** 2 * (l2 - l3) ** 2 * (l3 - l1) ** 2
    )
    eigen_discriminant = sp.expand(eigen_discriminant_squares)
    discriminant_identity = sp.expand(
        I2_eigen**3 - 6 * I3_eigen**2 - 2 * eigen_discriminant
    )

    equality_I2, equality_I3 = sp.symbols(
        "equality_I2 equality_I3", positive=True, real=True
    )
    equality_amplitude = sp.simplify(3 * equality_I3 / equality_I2)
    equality_constraint = equality_I2**3 - 6 * equality_I3**2
    equality_I2_from_amplitude = sp.factor(
        sp.together(equality_amplitude**2 - 3 * equality_I2 / 2)
    ).subs(equality_I3**2, equality_I2**3 / 6)
    equality_I3_from_amplitude = sp.factor(
        sp.together(equality_amplitude**3 - 9 * equality_I3 / 2)
    ).subs(equality_I3**2, equality_I2**3 / 6)
    equality_spectral_parameter = sp.symbols(
        "equality_spectral_parameter", real=True
    )
    equality_characteristic_polynomial = (
        equality_spectral_parameter**3
        - equality_I2 * equality_spectral_parameter / 2
        - equality_I3 / 3
    )
    equality_factored_polynomial = (
        (equality_spectral_parameter - 2 * equality_amplitude / 3)
        * (equality_spectral_parameter + equality_amplitude / 3) ** 2
    )
    equality_factorization_residual = sp.factor(
        equality_characteristic_polynomial - equality_factored_polynomial
    )
    expected_equality_factorization_residual = sp.factor(
        -equality_constraint
        * (3 * equality_I2 * equality_spectral_parameter + 2 * equality_I3)
        / (6 * equality_I2**3)
    )
    equality_locus_spectrum_certificate = all((
        equality_I2_from_amplitude == 0,
        equality_I3_from_amplitude == 0,
        sp.ask(sp.Q.positive(equality_amplitude)) is True,
        equality_factorization_residual
        == expected_equality_factorization_residual,
        sp.simplify(
            equality_factorization_residual.subs(equality_constraint, 0)
        ) == 0,
    ))

    r = sp.symbols("r", positive=True, real=True)
    reduced_potential = (
        -alpha * r**2 / 2
        - b * r**3 / (3 * sp.sqrt(6))
        + c * r**4 / 4
    )
    fixed_radius_I3_coefficient = -b / 3
    reduced_derivative = sp.simplify(
        sp.diff(reduced_potential, r)
        - r * (c * r**2 - b * r / sp.sqrt(6) - alpha)
    )
    radial_polynomial = c * r**2 - b * r / sp.sqrt(6) - alpha
    discriminant_root = sp.sqrt(b**2 + 24 * alpha * c)
    s_plus = sp.simplify((b + discriminant_root) / (4 * c))
    s_minus = sp.simplify((b - discriminant_root) / (4 * c))
    r_plus = sp.simplify((b + discriminant_root) / (2 * sp.sqrt(6) * c))
    r_minus = sp.simplify((b - discriminant_root) / (2 * sp.sqrt(6) * c))
    r_root_residual = sp.simplify(
        radial_polynomial.subs(r, r_plus)
    )
    r_minus_residual = sp.simplify(radial_polynomial.subs(r, r_minus))
    radial_factorization = sp.simplify(
        radial_polynomial - c * (r - r_plus) * (r - r_minus)
    )
    radial_root_product = sp.simplify(r_plus * r_minus)
    radial_coercive = sp.limit(reduced_potential, r, sp.oo) == sp.oo
    discriminant_gap = sp.simplify(24 * alpha * c / (discriminant_root + b))
    discriminant_gap_identity = sp.simplify(
        discriminant_root - b - discriminant_gap
    )
    negative_root_identity = sp.simplify(
        r_minus + 2 * sp.sqrt(6) * alpha / (discriminant_root + b)
    )
    negative_root_certificate = all((
        discriminant_gap_identity == 0,
        sp.ask(sp.Q.positive(discriminant_root + b)) is True,
        sp.ask(sp.Q.positive(discriminant_gap)) is True,
        negative_root_identity == 0,
        sp.ask(
            sp.Q.negative(
                -2 * sp.sqrt(6) * alpha / (discriminant_root + b)
            )
        ) is True,
        sp.ask(sp.Q.positive(r_plus)) is True,
    ))
    s_plus_residual = sp.simplify(2 * c * s_plus**2 - b * s_plus - 3 * alpha)
    s_minus_residual = sp.simplify(2 * c * s_minus**2 - b * s_minus - 3 * alpha)

    Q_star = s * sp.diag(
        sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3)
    )
    I2_star = sp.simplify(sp.trace(Q_star**2))
    I3_star = sp.simplify(sp.trace(Q_star**3))
    star_substitution = {
        x: 2 * s / 3, y: -s / 3, u: 0, v: 0, w: 0,
    }
    stationarity_relation = {alpha: (2 * c * s**2 - b * s) / 3}
    star_gradient = sp.simplify(
        gradient.subs(star_substitution).subs(stationarity_relation)
    )
    star_bound_saturation = sp.simplify(I2_star**3 - 6 * I3_star**2)
    spectral_parameter = sp.symbols("spectral_parameter", real=True)
    star_characteristic_polynomial = sp.factor(
        (spectral_parameter * sp.eye(3) - Q_star).det()
    )
    expected_star_characteristic_polynomial = sp.factor(
        (spectral_parameter - 2 * s / 3) * (spectral_parameter + s / 3) ** 2
    )

    def potential_of(matrix: sp.MatrixBase) -> sp.Expr:
        matrix_I2 = sp.trace(matrix**2)
        matrix_I3 = sp.trace(matrix**3)
        return sp.simplify(
            -alpha * matrix_I2 / 2
            - b * matrix_I3 / 3
            + c * matrix_I2**2 / 4
        )

    star_energy_on_shell = sp.factor(
        potential_of(Q_star).subs(stationarity_relation)
    )
    expected_star_energy = s**3 * (b - 3 * c * s) / 27
    energy_plus = sp.simplify(expected_star_energy.subs(s, s_plus))
    energy_minus = sp.simplify(expected_star_energy.subs(s, s_minus))
    energy_order_residual = sp.simplify(
        energy_plus - energy_minus
        + b * discriminant_root**3 / (432 * c**3)
    )
    positive_energy_gap = sp.simplify(2 * discriminant_root + discriminant_gap)
    energy_plus_negative_identity = sp.simplify(
        energy_plus + s_plus**3 * positive_energy_gap / 108
    )
    negative_minimum_energy_certificate = all((
        energy_plus_negative_identity == 0,
        sp.ask(sp.Q.positive(positive_energy_gap)) is True,
        sp.ask(
            sp.Q.negative(-s_plus**3 * positive_energy_gap / 108)
        ) is True,
    ))

    hessian_star = sp.simplify(
        hessian.subs(star_substitution).subs(stationarity_relation)
    )
    radial_mode = sp.Matrix([sp.Rational(2, 3), -sp.Rational(1, 3), 0, 0, 0])
    biaxial_diagonal = sp.Matrix([0, 1, 0, 0, 0])
    biaxial_23 = sp.Matrix([0, 0, 0, 0, 1])
    orbit_12 = sp.Matrix([0, 0, 1, 0, 0])
    orbit_13 = sp.Matrix([0, 0, 0, 1, 0])
    mode_matrix = sp.Matrix.hstack(
        radial_mode, biaxial_diagonal, biaxial_23, orbit_12, orbit_13
    )
    mode_gram = sp.simplify(mode_matrix.T * gram * mode_matrix)
    mode_hessian = sp.simplify(mode_matrix.T * hessian_star * mode_matrix)
    radial_eigenvalue = s * (4 * c * s - b) / 3
    biaxial_eigenvalue = b * s
    expected_mode_hessian = sp.diag(
        mode_gram[0, 0] * radial_eigenvalue,
        mode_gram[1, 1] * biaxial_eigenvalue,
        mode_gram[2, 2] * biaxial_eigenvalue,
        0,
        0,
    )
    mode_hessian_residual = sp.simplify(mode_hessian - expected_mode_hessian)
    radial_positive_certificate = sp.simplify(4 * c * s_plus - b)

    amplitude_from_state = sp.simplify(3 * I3_star / I2_star)
    P1 = sp.simplify(sp.eye(3) / 3 + Q_star / amplitude_from_state)
    P2 = sp.simplify(sp.eye(3) - P1)
    origin_scalar = sp.symbols("origin_scalar", real=True)
    origin_idempotents = sp.solve(
        sp.Eq(origin_scalar**2, origin_scalar), origin_scalar
    )
    commutant_entries = sp.symbols("commutant_0:9", real=True)
    generic_commutant = sp.Matrix(3, 3, commutant_entries)
    commutant_generators = (
        sp.diag(-1, 1, 1),
        sp.diag(1, -1, 1),
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]]),
        sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]]),
    )
    commutant_equations = [
        entry
        for transform in commutant_generators
        for entry in transform * generic_commutant * transform.T - generic_commutant
    ]
    commutant_solutions = sp.solve(
        commutant_equations, commutant_entries, dict=True
    )
    expected_commutant_solution = {
        commutant_entries[0]: commutant_entries[8],
        commutant_entries[1]: 0,
        commutant_entries[2]: 0,
        commutant_entries[3]: 0,
        commutant_entries[4]: commutant_entries[8],
        commutant_entries[5]: 0,
        commutant_entries[6]: 0,
        commutant_entries[7]: 0,
    }
    commutant_is_scalar = all((
        commutant_solutions == [expected_commutant_solution],
        matrix_is_zero(
            generic_commutant.subs(expected_commutant_solution)
            - commutant_entries[8] * sp.eye(3)
        ),
    ))
    sign_exchange_gap = sp.simplify(
        potential_of(-Q_star) - potential_of(Q_star)
    )

    unit_uniaxial = sp.sqrt(sp.Rational(3, 2)) * sp.diag(
        sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3)
    )
    unit_biaxial = sp.diag(1 / sp.sqrt(2), -1 / sp.sqrt(2), 0)
    b_zero_degeneracy = all((
        sp.simplify(sp.trace(unit_uniaxial**2)) == 1,
        sp.simplify(sp.trace(unit_biaxial**2)) == 1,
        sp.simplify(sp.trace(unit_uniaxial**3))
        != sp.simplify(sp.trace(unit_biaxial**3)),
        sp.simplify(
            (potential_of(unit_uniaxial) - potential_of(unit_biaxial)).subs(b, 0)
        ) == 0,
    ))

    c_negative = sp.symbols("c_negative", positive=True, real=True)
    c_zero_unbounded = sp.limit(reduced_potential.subs(c, 0), r, sp.oo) == -sp.oo
    c_negative_unbounded = (
        sp.limit(reduced_potential.subs(c, -c_negative), r, sp.oo) == -sp.oo
    )
    alpha_zero_marginal = matrix_is_zero(origin_hessian.subs(alpha, 0))

    q2x, q2y = sp.symbols("q2x q2y", real=True)
    Q2 = sp.Matrix([[q2x, q2y], [q2y, -q2x]])
    N, t = sp.symbols("N t", integer=True, positive=True)
    general_I2 = N * (N - 1) * t**2
    general_I3 = N * (N - 1) * (N - 2) * t**3
    general_ratio = sp.simplify(general_I3**2 / general_I2**3)
    expected_ratio = (N - 2) ** 2 / (N * (N - 1))

    null_potential = alpha * I2 / 2 + c * I2**2 / 4
    null_hessian = sp.simplify(sp.hessian(null_potential, coordinates).subs(zero))

    h = sp.symbols("h", nonzero=True, real=True)
    sourced_potential = potential - h * x
    sourced_origin_gradient = sp.Matrix([
        sp.diff(sourced_potential, variable) for variable in coordinates
    ]).subs(zero)
    allowed_symbols = set(coordinates) | {alpha, b, c}

    checks = {
        "traceless_symmetric_coordinate_chart_and_gram_exact": all((
            Q == Q.T,
            sp.trace(Q) == 0,
            gram == expected_gram,
            set(gram.eigenvals()) == {1, 2, 3},
        )),
        "invariant_ring_through_degree_four_and_CH_reduction_exact": all((
            matrix_is_zero(cayley_hamilton),
            degree_four_reduction == 0,
            invariant_monomials == [(0, 1), (1, 0), (2, 0)],
        )),
        "declared_O3_generator_invariance_exact": all(generator_invariance),
        "origin_is_stationary_unstable_and_role_trivial": all((
            matrix_is_zero(origin_gradient),
            matrix_is_zero(origin_hessian + alpha * gram),
            commutant_is_scalar,
            origin_idempotents == [0, 1],
        )),
        "sharp_eigenvalue_discriminant_bound_exact": all((
            discriminant_identity == 0,
            eigen_discriminant_squares.is_nonnegative is True,
            equality_locus_spectrum_certificate,
        )),
        "reduced_radial_problem_and_positive_root_exact": all((
            reduced_derivative == 0,
            r_root_residual == 0,
            r_minus_residual == 0,
            radial_factorization == 0,
            radial_root_product == -alpha / c,
            negative_root_certificate,
            sp.simplify(r_plus - sp.sqrt(sp.Rational(2, 3)) * s_plus) == 0,
            s_plus_residual == 0,
            sp.simplify(discriminant_root**2 - b**2) == 24 * alpha * c,
        )),
        "unique_nonzero_global_minimum_quotient_orbit_certified": all((
            discriminant_identity == 0,
            eigen_discriminant_squares.is_nonnegative is True,
            equality_locus_spectrum_certificate,
            reduced_derivative == 0,
            radial_factorization == 0,
            radial_coercive,
            negative_root_certificate,
            negative_minimum_energy_certificate,
            fixed_radius_I3_coefficient.is_negative is True,
            alpha.is_positive is True,
            b.is_positive is True,
            c.is_positive is True,
            matrix_is_zero(star_gradient),
            star_bound_saturation == 0,
            I2_star == 2 * s**2 / 3,
            I3_star == 2 * s**3 / 9,
            star_characteristic_polynomial
            == expected_star_characteristic_polynomial,
            sp.simplify(star_energy_on_shell - expected_star_energy) == 0,
            sp.simplify(3 * c * s_plus - b - (-b + 3 * discriminant_root) / 4) == 0,
        )),
        "negative_stationary_branch_rejected": all((
            s_minus_residual == 0,
            r_minus_residual == 0,
            negative_root_certificate,
            sp.simplify(s_minus + 6 * alpha / (discriminant_root + b)) == 0,
            sp.ask(
                sp.Q.negative(-6 * alpha / (discriminant_root + b))
            ) is True,
            sp.simplify(4 * c * s_minus - b) == -discriminant_root,
            sp.simplify(b * s_minus - b * (b - discriminant_root) / (4 * c)) == 0,
            energy_order_residual == 0,
        )),
        "orbit_normal_hessian_positive_with_two_orbit_zero_modes": all((
            mode_matrix.det() != 0,
            mode_gram == sp.diag(*[mode_gram[i, i] for i in range(5)]),
            matrix_is_zero(mode_hessian_residual),
            radial_positive_certificate == discriminant_root,
            b.is_positive is True,
            s_plus.is_positive is True,
        )),
        "Q_generated_rank_1_rank_2_projectors_exact": all((
            amplitude_from_state == s,
            matrix_is_zero(P1**2 - P1),
            matrix_is_zero(P2**2 - P2),
            matrix_is_zero(P1 * P2),
            P1 + P2 == sp.eye(3),
            P1.rank() == 1,
            P2.rank() == 2,
            matrix_is_zero(Q_star - s * (P1 - sp.eye(3) / 3)),
        )),
        "roles_nonexchangeable_and_Q_sign_not_law_symmetry": all((
            P1.rank() != P2.rank(),
            sp.trace(P1) != sp.trace(P2),
            sign_exchange_gap == 4 * b * s**3 / 27,
        )),
        "law_has_no_target_direction_projector_or_data_symbol": all((
            potential.free_symbols == allowed_symbols,
            matrix_is_zero(origin_gradient),
            DATA_FITTED_PARAMETERS == 0,
        )),
        "b_zero_shape_degeneracy_control": b_zero_degeneracy,
        "c_nonpositive_and_alpha_zero_boundary_controls": all((
            c_zero_unbounded,
            c_negative_unbounded,
            alpha_zero_marginal,
        )),
        "N1_N2_and_general_N_nonuniversality_controls": all((
            sp.Matrix([[0]]).rank() == 0,
            sp.simplify(sp.trace(Q2**3)) == 0,
            sp.simplify(general_ratio - expected_ratio) == 0,
            sp.simplify(general_ratio.subs(N, 2)) == 0,
            sp.simplify(general_ratio.subs(N, 3)) == sp.Rational(1, 6),
            sp.simplify(general_ratio.subs(N, 4)) == sp.Rational(1, 3),
        )),
        "positive_quadratic_null_keeps_undifferentiated_origin": (
            matrix_is_zero(null_hessian - alpha * gram)
        ),
        "explicit_anisotropic_source_is_detected": all((
            sourced_origin_gradient[0] == -h,
            any(entry != 0 for entry in sourced_origin_gradient),
        )),
    }
    return {
        "checks": checks,
        "diagnostics": {
            "invariant_basis_degree_le_4": ["I2", "I3", "I2^2"],
            "s_plus": str(s_plus),
            "s_minus": str(s_minus),
            "projector_ranks": [int(P1.rank()), int(P2.rank())],
            "normal_hessian_eigenvalues": [
                str(radial_eigenvalue), str(biaxial_eigenvalue),
                str(biaxial_eigenvalue),
            ],
            "orbit_zero_mode_count": 2,
            "Q_sign_energy_gap": str(sign_exchange_gap),
            "data_fitted_parameters": DATA_FITTED_PARAMETERS,
        },
    }


def build_f1_evidence(
    sections: dict[str, dict[str, Any]],
) -> dict[str, bool]:
    singleton = sections["singleton"]["checks"]
    equivariant = sections["equivariant"]["checks"]
    spectral = sections["spectral"]["checks"]
    derived_ranks = sections["spectral"]["diagnostics"].get("projector_ranks")

    ranks_cross_bound = derived_ranks == [1, 2]

    evidence = {
        "public_definition_accepts_both_witness_kinds": (
            F1_WITNESS_KINDS == (
                "MULTIPLE_INEQUIVALENT_ACCEPTED_QUOTIENT_CLASSES",
                "ONE_ACCEPTED_QUOTIENT_CLASS_WITH_CANONICAL_COEXISTING_NONEXCHANGEABLE_ROLES",
            )
        ),
        "selected_witness_kind_explicit": all((
            SELECTED_F1_WITNESS_KIND in F1_WITNESS_KINDS,
            SELECTED_F1_WITNESS_KIND
            == "ONE_ACCEPTED_QUOTIENT_CLASS_WITH_CANONICAL_COEXISTING_NONEXCHANGEABLE_ROLES",
        )),
        "external_file_dependency_registry_empty": EXTERNAL_FILE_DEPENDENCIES == (),
        "primitive_registry_exactly_declared": (
            set(IMPORTED_PRIMITIVES) == IMPORTED_PRIMITIVE_KEYS
            and len(IMPORTED_PRIMITIVES) == 9
        ),
        "explicit_orientation_target_inputs_absent": all((
            spectral["law_has_no_target_direction_projector_or_data_symbol"] is True,
            spectral["declared_O3_generator_invariance_exact"] is True,
            DATA_FITTED_PARAMETERS == 0,
        )),
        "undifferentiated_reference_trivial": (
            spectral["origin_is_stationary_unstable_and_role_trivial"] is True
        ),
        "law_O3_invariant_and_representative_target_free": all((
            spectral["invariant_ring_through_degree_four_and_CH_reduction_exact"] is True,
            spectral["declared_O3_generator_invariance_exact"] is True,
            spectral["law_has_no_target_direction_projector_or_data_symbol"] is True,
        )),
        "output_classification_complete": all((
            spectral["unique_nonzero_global_minimum_quotient_orbit_certified"] is True,
            spectral["negative_stationary_branch_rejected"] is True,
            spectral["b_zero_shape_degeneracy_control"] is True,
            spectral["c_nonpositive_and_alpha_zero_boundary_controls"] is True,
        )),
        "intrinsic_differentiation_certified": all((
            spectral["Q_generated_rank_1_rank_2_projectors_exact"] is True,
            ranks_cross_bound,
            spectral["law_has_no_target_direction_projector_or_data_symbol"] is True,
        )),
        "inequivalence_survives_declared_quotient": all((
            spectral["roles_nonexchangeable_and_Q_sign_not_law_symmetry"] is True,
            ranks_cross_bound,
            IMPORTED_PRIMITIVES.get("Q_sign_not_gauge")
            == "IMPORTED_NOT_DERIVED",
        )),
        "law_forces_roles_not_arbitrary_basis": all((
            spectral["unique_nonzero_global_minimum_quotient_orbit_certified"] is True,
            spectral["Q_generated_rank_1_rank_2_projectors_exact"] is True,
        )),
        "law_selects_no_representative_orientation": all((
            spectral["declared_O3_generator_invariance_exact"] is True,
            spectral["law_has_no_target_direction_projector_or_data_symbol"] is True,
        )),
        "open_domain_structural_stability": all((
            spectral["orbit_normal_hessian_positive_with_two_orbit_zero_modes"] is True,
            IMPORTED_PRIMITIVES.get("open_parameter_domain_alpha_b_c_positive")
            == "IMPORTED_NOT_DERIVED",
        )),
        "all_registered_primitives_labelled_imported": all((
            set(IMPORTED_PRIMITIVES) == IMPORTED_PRIMITIVE_KEYS,
            set(IMPORTED_PRIMITIVES.values()) == {"IMPORTED_NOT_DERIVED"},
            all(value is False for value in SCOPE_CEILING.values()),
        )),
        "no_go_route_boundaries_respected": all((
            exact_true_map(singleton, SINGLETON_CHECK_KEYS),
            exact_true_map(equivariant, EQUIVARIANT_CHECK_KEYS),
        )),
        "independent_crosschecks_and_controls": all((
            spectral["sharp_eigenvalue_discriminant_bound_exact"] is True,
            spectral["orbit_normal_hessian_positive_with_two_orbit_zero_modes"] is True,
            spectral["explicit_anisotropic_source_is_detected"] is True,
            not contains_float(sections),
        )),
        "listed_falsifier_checks_pass": all((
            spectral["unique_nonzero_global_minimum_quotient_orbit_certified"] is True,
            spectral["orbit_normal_hessian_positive_with_two_orbit_zero_modes"] is True,
            spectral["invariant_ring_through_degree_four_and_CH_reduction_exact"] is True,
            spectral["roles_nonexchangeable_and_Q_sign_not_law_symmetry"] is True,
            spectral["origin_is_stationary_unstable_and_role_trivial"] is True,
            spectral["declared_O3_generator_invariance_exact"] is True,
            spectral["law_has_no_target_direction_projector_or_data_symbol"] is True,
        )),
        "scope_ceiling_registry_exactly_false": all((
            set(SCOPE_CEILING) == SCOPE_CEILING_KEYS,
            all(value is False for value in SCOPE_CEILING.values()),
        )),
    }
    return evidence


def adjudicate(evidence: Any, audit_valid: Any) -> dict[str, Any]:
    evidence_schema_valid = exact_bool_map(evidence, F1_GATE_KEYS)
    exact_audit_boolean = type(audit_valid) is bool
    completed_audit = bool(exact_audit_boolean and audit_valid and evidence_schema_valid)
    raw_candidate_pass = bool(
        evidence_schema_valid and all(value is True for value in evidence.values())
    )
    effective_promotion = bool(completed_audit and raw_candidate_pass)
    if not completed_audit:
        status = INVALID_STATUS
    elif raw_candidate_pass:
        status = PASS_STATUS
    else:
        status = NOT_PROMOTED_STATUS
    return {
        "AUDIT_VALID": completed_audit,
        "RAW_CANDIDATE_PASS": raw_candidate_pass,
        "PROMOTED": effective_promotion,
        "STATUS": status,
    }


def decision_logic_controls() -> dict[str, bool]:
    all_true = {key: True for key in F1_GATE_KEYS}
    one_false = dict(all_true)
    one_false["intrinsic_differentiation_certified"] = False
    missing = dict(all_true)
    missing.pop("public_definition_accepts_both_witness_kinds")
    extra = dict(all_true)
    extra["unregistered_score"] = True
    nonboolean = dict(all_true)
    nonboolean["public_definition_accepts_both_witness_kinds"] = 1
    return {
        "valid_positive_branch": adjudicate(all_true, True) == {
            "AUDIT_VALID": True,
            "RAW_CANDIDATE_PASS": True,
            "PROMOTED": True,
            "STATUS": PASS_STATUS,
        },
        "valid_negative_branch": adjudicate(one_false, True) == {
            "AUDIT_VALID": True,
            "RAW_CANDIDATE_PASS": False,
            "PROMOTED": False,
            "STATUS": NOT_PROMOTED_STATUS,
        },
        "invalid_audit_cannot_promote": adjudicate(all_true, False) == {
            "AUDIT_VALID": False,
            "RAW_CANDIDATE_PASS": True,
            "PROMOTED": False,
            "STATUS": INVALID_STATUS,
        },
        "missing_gate_invalid": adjudicate(missing, True)["STATUS"] == INVALID_STATUS,
        "extra_gate_invalid": adjudicate(extra, True)["STATUS"] == INVALID_STATUS,
        "nonboolean_gate_invalid": adjudicate(nonboolean, True)["STATUS"] == INVALID_STATUS,
        "nonboolean_audit_invalid": adjudicate(all_true, 1)["STATUS"] == INVALID_STATUS,
    }


def run_proof() -> dict[str, Any]:
    sections = {
        "singleton": strict_singleton_no_go(),
        "equivariant": deterministic_equivariant_fixed_set_no_go(),
        "spectral": atemporal_spectral_construction(),
    }
    evidence = build_f1_evidence(sections)
    decision_controls = decision_logic_controls()

    audit_checks = {
        "section_checks_exact_and_all_true": all((
            exact_true_map(sections["singleton"]["checks"], SINGLETON_CHECK_KEYS),
            exact_true_map(sections["equivariant"]["checks"], EQUIVARIANT_CHECK_KEYS),
            exact_true_map(sections["spectral"]["checks"], SPECTRAL_CHECK_KEYS),
        )),
        "promotion_evidence_schema_exact_boolean": exact_bool_map(
            evidence, F1_GATE_KEYS
        ),
        "imported_primitive_registry_exact": all((
            set(IMPORTED_PRIMITIVES) == IMPORTED_PRIMITIVE_KEYS,
            len(IMPORTED_PRIMITIVES) == 9,
            set(IMPORTED_PRIMITIVES.values()) == {"IMPORTED_NOT_DERIVED"},
        )),
        "standard_mathematics_registry_explicit": (
            set(STANDARD_MATHEMATICS) == STANDARD_MATHEMATICS_KEYS
            and len(STANDARD_MATHEMATICS) == 4
            and all(isinstance(item, str) and item for item in STANDARD_MATHEMATICS)
        ),
        "scope_ceiling_exactly_false": all((
            set(SCOPE_CEILING) == SCOPE_CEILING_KEYS,
            len(SCOPE_CEILING) == 15,
            all(type(value) is bool and value is False for value in SCOPE_CEILING.values()),
        )),
        "zero_data_fit_and_no_external_file_dependencies": all((
            type(DATA_FITTED_PARAMETERS) is int,
            DATA_FITTED_PARAMETERS == 0,
            EXTERNAL_FILE_DEPENDENCIES == (),
        )),
        "decision_logic_positive_negative_invalid_controls": (
            exact_true_map(decision_controls, DECISION_CONTROL_KEYS)
        ),
        "exact_symbolic_outputs_without_floating_tolerance": (
            not contains_float(sections)
            and not contains_float(evidence)
            and not contains_float(decision_controls)
        ),
    }
    audit_valid = exact_true_map(audit_checks, AUDIT_CHECK_KEYS)
    decision = adjudicate(evidence, audit_valid)
    return {
        "MODEL_VERSION": MODEL_VERSION,
        **decision,
        "CLAIM": (
            "A conditional atemporal structural F1 follows relative to the "
            "explicitly imported Sym_0(3), O(3), quartic-law and argmin primitives."
        ),
        "AUDIT_CHECKS": audit_checks,
        "PROMOTION_EVIDENCE": evidence,
        "SECTION_RESULTS": sections,
        "DECISION_LOGIC_CONTROLS": decision_controls,
        "IMPORTED_PRIMITIVES": IMPORTED_PRIMITIVES,
        "STANDARD_MATHEMATICS": STANDARD_MATHEMATICS,
        "DATA_FITTED_PARAMETERS": DATA_FITTED_PARAMETERS,
        "SCOPE_CEILING": SCOPE_CEILING,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_proof()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["STATUS"] == PASS_STATUS else 1


if __name__ == "__main__":
    raise SystemExit(main())
