from __future__ import annotations

"""PHASE 18br: auxiliary-link origin and induced-plaquette gate.

This gate asks a narrower and more constructive question than p18bq:

    Can the absence of a bare Maxwell/plaquette coefficient follow from an
    exact rewriting of an existing frame interaction, instead of being added
    as a compositeness boundary condition?

For an O(3) frame field, a *chosen nearest-neighbour Heisenberg regulator*
has an exact CP1/Schwinger-boson rewrite and hence an exact
Hubbard--Stratonovich (HS) bond variable.  Its phase is a compact auxiliary
U(1) link and that factorized one-bond HS action contains no plaquette term.
Integrating out a gapped charged mode then generates a plaquette term.  The
leading strong-coupling coefficient is computed exactly below.

The qualification is essential and is executable here.  The p01/F_min core
depends only on the eigenvalues of B: it is blind to the local O(3)
eigenframe.  A compatible unstrained solid also has no nonconstant local
rotation field.  The p18f axis action therefore introduces an independent
continuum stiffness kappa_n; it does not derive it from F_min.  A Wilson
regulator would conditionally give J_CP1=4*kappa_n*a^2, but next-neighbour,
higher-bond and gauge-invariant ring terms have the same quadratic continuum
limit.  Thus no bare plaquette follows only after declaring the microscopic
factorized bond action; it is not a theorem of the current RefG continuum
action.

The result is useful but not an alpha closure.  The induced stiffness depends
continuously on the hopping-to-gap ratios.  Moreover, the CP1 link gauges a
projective frame redundancy; it is not automatically the physical
generation-blind Q=T3+Y connection.  Before a charged-core determinant can be
predictive, a localized F_min core and its orientational moduli-space/overlap
action must derive the microscopic bond and exclude the allowed ring terms.

No electromagnetic comparison value is imported or used in this file.
"""

import ast
import inspect
from math import comb

import sympy as sp


def cp1_spin1_rewrite_theorem() -> dict[str, object]:
    """Verify the CP1 bond identity and the h=2 spin-one state count."""

    # Generic complex two-spinors written in real components.  The Pauli
    # completeness identity implies
    #   (z^dag sigma z).(w^dag sigma w)
    #     = 2 |z^dag w|^2 - (z^dag z)(w^dag w).
    zr0, zi0, zr1, zi1 = sp.symbols(
        "z_r0 z_i0 z_r1 z_i1", real=True
    )
    wr0, wi0, wr1, wi1 = sp.symbols(
        "w_r0 w_i0 w_r1 w_i1", real=True
    )
    z = sp.Matrix([zr0 + sp.I * zi0, zr1 + sp.I * zi1])
    w = sp.Matrix([wr0 + sp.I * wi0, wr1 + sp.I * wi1])
    sigma = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    )

    n_z = tuple(sp.expand_complex((z.conjugate().T * s * z)[0]) for s in sigma)
    n_w = tuple(sp.expand_complex((w.conjugate().T * s * w)[0]) for s in sigma)
    lhs = sp.expand(sum(n_z[i] * n_w[i] for i in range(3)))
    overlap = sp.expand_complex((z.conjugate().T * w)[0])
    norm_z = sp.expand_complex((z.conjugate().T * z)[0])
    norm_w = sp.expand_complex((w.conjugate().T * w)[0])
    rhs = sp.expand(2 * overlap * sp.conjugate(overlap) - norm_z * norm_w)
    fierz_residual = sp.simplify(sp.expand_complex(lhs - rhs))

    h = 2
    cp1_complex_components = 2
    spin1_dimension = comb(h + 1, 1)
    return {
        "CP1_map": "n=z^dagger sigma z, z^dagger z=1",
        "local_redundancy": "z_x -> exp(i lambda_x) z_x",
        "frame_is_redundancy_invariant": True,
        "exact_fierz_identity": fierz_residual == 0,
        "normalized_bond_identity": (
            "n_x.n_y=2|z_x^dagger z_y|^2-1"
        ),
        "schwinger_boson_occupation_h": h,
        "CP1_complex_component_count": cp1_complex_components,
        "CP1_component_count_is_fixed_by_h": False,
        "symmetric_two_boson_dimension": spin1_dimension,
        "spin1_dimension_equals_C3_dimension": spin1_dimension == 3,
        "CP1_spinor_projective_charges": (+1, +1),
        "spin1_Sym2_common_projective_charge": h,
        "spin1_J3_weights_are_projective_charges": False,
        "p11g_h2_role": (
            "oriented-frame closure label: two half-turns restore the frame"
        ),
        "CP1_two_component_role": "coordinate spinor for S2=CP1",
        "hopping_role": "unit-projective-charge z propagates on a bond",
        "link_phase_role": "continuous auxiliary U(1) bond coordinate",
        "h2_closure_component_hopping_and_phase_roles_are_distinct": True,
        "representation_fact": (
            "h=2 gives the three-dimensional spin-one representation; "
            "this does not identify its projective U(1) with electromagnetism"
        ),
        "reference_value_used": False,
    }


def fmin_eigenframe_blindness_theorem() -> dict[str, object]:
    """Prove that p01/F_min contains no independent O(3) eigenframe action.

    Write B=R diag(lambda_i) R^T with a generic three-angle Euler rotation.
    F_min depends on B only through its three elementary spectral invariants,
    so all Euler-angle dependence must cancel.  The physical 2PN polynomial
    slice is also reduced to an eigenvalue-only normal form as a check.
    """

    alpha_e, beta_e, gamma_e = sp.symbols(
        "alpha_E beta_E gamma_E", real=True
    )
    lam1, lam2, lam3, Y = sp.symbols(
        "lambda_1 lambda_2 lambda_3 Y", real=True
    )

    def rz(angle: sp.Expr) -> sp.Matrix:
        return sp.Matrix(
            [
                [sp.cos(angle), -sp.sin(angle), 0],
                [sp.sin(angle), sp.cos(angle), 0],
                [0, 0, 1],
            ]
        )

    def ry(angle: sp.Expr) -> sp.Matrix:
        return sp.Matrix(
            [
                [sp.cos(angle), 0, sp.sin(angle)],
                [0, 1, 0],
                [-sp.sin(angle), 0, sp.cos(angle)],
            ]
        )

    rotation = rz(alpha_e) * ry(beta_e) * rz(gamma_e)
    B = rotation * sp.diag(lam1, lam2, lam3) * rotation.T
    I1 = sp.trigsimp(sp.trace(B))
    I2 = sp.trigsimp((sp.trace(B) ** 2 - sp.trace(B * B)) / 2)
    I3 = sp.trigsimp(B.det())
    expected_I1 = lam1 + lam2 + lam3
    expected_I2 = lam1 * lam2 + lam1 * lam3 + lam2 * lam3
    expected_I3 = lam1 * lam2 * lam3
    invariant_residuals = (
        sp.trigsimp(I1 - expected_I1),
        sp.trigsimp(I2 - expected_I2),
        sp.trigsimp(I3 - expected_I3),
    )

    # p18b/p18d physical polynomial slice c_YI1=2*c_Y2, divided by c_Y2.
    F_slice = sp.expand(
        -8 * Y
        + Y**2
        + 8 * I1
        + I1**2
        - 16 * I2
        + 16 * I3
        + 2 * Y * I1
    )
    eta, e1, e2, e3 = sp.symbols("eta e_1 e_2 e_3", real=True)
    strain_subs = {
        Y: 1 + eta,
        lam1: 1 + e1,
        lam2: 1 + e2,
        lam3: 1 + e3,
    }
    normal_form = (eta + e1 + e2 + e3) ** 2 + 16 * e1 * e2 * e3
    normal_form_residual = sp.factor(
        sp.expand(F_slice.subs(strain_subs) - normal_form)
    )

    return {
        "B_spectral_decomposition": "B=R diag(lambda_1,lambda_2,lambda_3) R^T",
        "I1_residual": invariant_residuals[0],
        "I2_residual": invariant_residuals[1],
        "I3_residual": invariant_residuals[2],
        "all_Fmin_invariants_eigenframe_blind": all(
            residual == 0 for residual in invariant_residuals
        ),
        "physical_slice_strain_normal_form": normal_form,
        "physical_slice_normal_form_residual": normal_form_residual,
        "physical_slice_normal_form_exact": normal_form_residual == 0,
        "p01_Fmin_contains_independent_n_or_R_derivative": False,
        "p01_Fmin_derives_nonzero_frame_stiffness": False,
        "scope": (
            "algebraic spectral blindness; compatibility of an actual solid "
            "map is checked separately below"
        ),
        "reference_value_used": False,
    }


def compatible_unstrained_frame_rigidity_theorem() -> dict[str, object]:
    """Prove that a compatible unstrained local rotation is constant.

    For e_i^A=partial_i phi^A and e_i.e_j=delta_ij, define
    A_ijk=e_i.partial_j e_k.  Mixed-derivative compatibility makes A symmetric
    in (j,k), whereas orthonormality makes it antisymmetric in (i,k).  The
    resulting 27-component homogeneous system has full rank.
    """

    connection = sp.symbols("A_0:27", real=True)

    def component(i: int, j: int, k: int) -> sp.Expr:
        return connection[9 * i + 3 * j + k]

    equations = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                equations.append(component(i, j, k) - component(i, k, j))
                equations.append(component(i, j, k) + component(k, j, i))
    matrix, _ = sp.linear_eq_to_matrix(equations, connection)
    rank = matrix.rank()
    nullity = len(connection) - rank
    return {
        "connection_definition": "A_ijk=e_i dot partial_j e_k",
        "compatibility_constraint": "A_ijk=A_ikj",
        "orthonormality_constraint": "A_ijk=-A_kji",
        "number_of_connection_components": len(connection),
        "constraint_matrix_rank": rank,
        "constraint_nullity": nullity,
        "full_rank_27": rank == 27,
        "only_compatible_unstrained_solution_is_zero_connection": nullity == 0,
        "local_unstrained_rotation_is_constant": nullity == 0,
        "defects_or_strain_require_separate_dynamics": True,
        "reference_value_used": False,
    }


def p18f_continuum_to_cp1_bond_scope_theorem() -> dict[str, object]:
    """Derive the conditional Wilson bond and exhibit regulator freedom."""

    kn_P, kn_PY, kn_PI1, kn_PI2, kn_PI3 = sp.symbols(
        "kn_P kn_PY kn_PI1 kn_PI2 kn_PI3", real=True
    )
    kappa_n = kn_P + kn_PY + 3 * kn_PI1 + 3 * kn_PI2 + kn_PI3
    scale = sp.symbols("s", positive=True)
    scaled_kappa = sp.expand(
        kappa_n.subs(
            {
                kn_P: scale * kn_P,
                kn_PY: scale * kn_PY,
                kn_PI1: scale * kn_PI1,
                kn_PI2: scale * kn_PI2,
                kn_PI3: scale * kn_PI3,
            }
        )
    )
    witness_one = {kn_P: 1, kn_PY: 0, kn_PI1: 0, kn_PI2: 0, kn_PI3: 0}
    witness_two = {kn_P: 2, kn_PY: 0, kn_PI1: 0, kn_PI2: 0, kn_PI3: 0}

    lattice_a = sp.symbols("a", positive=True)
    dot, overlap_sq = sp.symbols("n_x_dot_n_y overlap_squared", real=True)
    difference_squared = 2 - 2 * dot
    wilson_link_action = sp.expand(kappa_n * lattice_a**2 * difference_squared)
    cp1_link_action = sp.expand(
        wilson_link_action.subs(dot, 2 * overlap_sq - 1)
    )
    J_cp1 = sp.simplify(-cp1_link_action.coeff(overlap_sq))

    regulator_delta = sp.symbols("delta_reg", real=True)
    beta_nearest = (2 - 4 * regulator_delta) * kappa_n * lattice_a**2
    beta_next = regulator_delta * kappa_n * lattice_a**2
    second_moment = sp.simplify(beta_nearest + 4 * beta_next)
    fourth_moment = sp.simplify(beta_nearest + 16 * beta_next)

    return {
        "p18f_normalized_background_stiffness": kappa_n,
        "p18f_continuum_action": "S_E=int d4x kappa_n (partial n)^2",
        "scaled_stiffness": scaled_kappa,
        "scale_direction_is_free": sp.simplify(scaled_kappa - scale * kappa_n)
        == 0,
        "two_positive_free_stiffness_witnesses": (
            kappa_n.subs(witness_one),
            kappa_n.subs(witness_two),
        ),
        "p18f_fixes_absolute_kappa_n": False,
        "unit_vector_difference_identity": "(n_y-n_x)^2=2(1-n_x.n_y)",
        "conditional_Wilson_link_action": wilson_link_action,
        "conditional_CP1_link_action": cp1_link_action,
        "conditional_J_CP1": J_cp1,
        "conditional_J_CP1_equals_4_kappa_n_a2": sp.simplify(
            J_cp1 - 4 * kappa_n * lattice_a**2
        )
        == 0,
        "regulator_family_nearest_coefficient": beta_nearest,
        "regulator_family_next_neighbor_coefficient": beta_next,
        "regulator_second_moment": second_moment,
        "same_two_derivative_continuum_for_all_delta": sp.simplify(
            second_moment - 2 * kappa_n * lattice_a**2
        )
        == 0,
        "regulator_fourth_moment": fourth_moment,
        "higher_moment_depends_on_delta": sp.diff(
            fourth_moment, regulator_delta
        )
        != 0,
        "nearest_neighbor_CP1_bond_uniquely_implied_by_continuum": False,
        "reference_value_used": False,
    }


def allowed_cp1_ring_operator_theorem() -> dict[str, object]:
    """Show that a real four-bond Bargmann/Wilson ring is symmetry allowed."""

    lam1, lam2, lam3, lam4 = sp.symbols(
        "lambda_1 lambda_2 lambda_3 lambda_4", real=True
    )
    overlap_phase_shifts = (
        -lam1 + lam2,
        -lam2 + lam3,
        -lam3 + lam4,
        -lam4 + lam1,
    )
    total_phase_shift = sp.simplify(sum(overlap_phase_shifts))
    return {
        "ring_operator": (
            "W_square=(z1^dag z2)(z2^dag z3)(z3^dag z4)(z4^dag z1)"
        ),
        "projector_form": "W_square=Tr(P1 P2 P3 P4), P_i=(1+n_i.sigma)/2",
        "local_phase_shifts": overlap_phase_shifts,
        "total_local_U1_phase_shift": total_phase_shift,
        "ring_is_local_projective_U1_invariant": total_phase_shift == 0,
        "real_ring_is_O3_even": True,
        "allowed_bare_term": "-rho_square Re(W_square)",
        "ring_is_direct_plaquette_like_operator": True,
        "p01_or_p18f_symmetry_forces_rho_square_zero": False,
        "quadratic_p18f_gate_detects_ring_coefficient": False,
        "reference_value_used": False,
    }


def exact_hubbard_stratonovich_link_theorem() -> dict[str, object]:
    """Complete the HS square and identify the compact bond phase."""

    q_r, q_i, b_r, b_i = sp.symbols(
        "Q_r Q_i b_r b_i", real=True
    )
    J = sp.symbols("J", positive=True)
    q_abs2 = q_r**2 + q_i**2
    b_abs2 = b_r**2 + b_i**2
    re_qstar_b = q_r * b_r + q_i * b_i
    completed_square = (
        (q_r - J * b_r) ** 2 + (q_i - J * b_i) ** 2
    ) / J
    expanded_form = q_abs2 / J - 2 * re_qstar_b + J * b_abs2
    square_residual = sp.simplify(completed_square - expanded_form)

    lam_x, lam_y = sp.symbols("lambda_x lambda_y", real=True)
    phase_b = lam_y - lam_x
    phase_u = lam_x - lam_y
    hopping_phase = sp.simplify(-lam_x + phase_u + lam_y)

    return {
        "original_bond": "J |z_x^dagger z_y|^2",
        "gaussian_identity": (
            "exp[J|b|^2] proportional to integral dQ "
            "exp[-|Q|^2/J+Q*b^star+Q^star*b]"
        ),
        "completed_square_residual": square_residual,
        "HS_identity_exact": square_residual == 0,
        "overlap_phase_under_local_redundancy": phase_b,
        "compact_link_definition": "U_xy=Q_xy^star/|Q_xy|",
        "compact_link_phase_rule": phase_u,
        "link_hopping_phase_residual": hopping_phase,
        "link_hopping_is_gauge_invariant": hopping_phase == 0,
        "HS_bond_terms": ("|Q_xy|^2/J", "z_x^dagger U_xy z_y+h.c."),
        "bare_plaquette_in_exact_one_bond_rewrite": 0,
        "no_bare_plaquette_is_exact_if_original_quartic_bond_is_microscopic": True,
        "no_bare_plaquette_scope": (
            "exact only for a declared factorized one-bond microscopic action; "
            "not implied by p01/F_min or by the p18f continuum limit"
        ),
        "unconditional_no_bare_plaquette_theorem_for_current_RefG": False,
        "link_amplitude_must_also_be_integrated": True,
        "freezing_link_amplitude_is_extra_saddle_assumption": True,
        "current_RefG_microscopic_bond_action_derived": False,
        "reference_value_used": False,
    }


def exact_fixed_amplitude_link_phase_audit() -> dict[str, object]:
    """Integrate a factorized compact link phase when the plaquette term is zero.

    With c2=0, every link phase is independent and

        int da/(2*pi) exp[x cos(a)] = I0(x).

    The all-order Taylor coefficient is verified for symbolic m.  Since
    |z_x^dag z_y|^2=(1+n_x.n_y)/2, the result is a bond-local O(3) action;
    there is no independent flux stiffness left after exact link integration.
    """

    m = sp.symbols("m", integer=True, nonnegative=True)
    c1, overlap_abs, overlap_sq = sp.symbols(
        "c_1 overlap_abs overlap_squared",
        nonnegative=True,
        real=True,
    )
    spin_dot = sp.symbols("n_x_dot_n_y", real=True)
    angular_even_moment = sp.binomial(2 * m, m) / 4**m
    integrated_exponential_coefficient = sp.simplify(
        angular_even_moment / sp.factorial(2 * m)
    )
    bessel_I0_coefficient = 1 / (
        4**m * sp.factorial(m) ** 2
    )
    coefficient_residual = sp.simplify(
        integrated_exponential_coefficient - bessel_I0_coefficient
    )
    bessel_argument = c1 * overlap_abs
    overlap_to_spin_residual = sp.simplify(
        (2 * overlap_sq - 1 - spin_dot).subs(
            overlap_sq, (1 + spin_dot) / 2
        )
    )

    return {
        "bare_plaquette_coefficient_c2": 0,
        "one_link_phase_integral": "I0(c1*|b_xy|)",
        "symbolic_even_moment": angular_even_moment,
        "integrated_series_coefficient": integrated_exponential_coefficient,
        "Bessel_I0_series_coefficient": bessel_I0_coefficient,
        "all_order_coefficient_residual": coefficient_residual,
        "all_order_I0_identity_verified": coefficient_residual == 0,
        "Bessel_argument": bessel_argument,
        "CP1_overlap_spin_identity_residual": overlap_to_spin_residual,
        "CP1_overlap_spin_identity_exact": overlap_to_spin_residual == 0,
        "bond_local_spin_action": (
            "-log I0(c1*sqrt((1+n_x.n_y)/2)) per nearest-neighbour bond"
        ),
        "exact_phase_integration_generates_only_bond_local_O3_interaction": True,
        "independent_flux_stiffness_after_exact_phase_integration": False,
        "exact_full_HS_integration_returns_original_spin_bond": True,
        "holding_U_fixed_then_integrating_matter_is_a_conditional_reordering": True,
        "leading_induced_plaquette_alone_proves_deconfinement": False,
        "deconfinement_requires_full_compact_loop_tower_and_phase_analysis": True,
        "reference_value_used": False,
    }


def leading_induced_plaquette_theorem() -> dict[str, object]:
    """Derive the first flux-sensitive term of a finite matter determinant.

    Use one four-site square, gauge three links to one, and put the plaquette
    holonomy exp(i f) on the fourth link.  For a gapped complex mode with
    kernel M^2 I-t H, kappa=t/M^2, the flux part of Tr log begins at length
    four.  Backtracking walks are flux independent; the two oriented square
    loops give the exact coefficient below.
    """

    f, kappa, q = sp.symbols("f kappa q", real=True)
    phase = sp.exp(sp.I * q * f)
    H = sp.zeros(4)
    for left, right in ((0, 1), (1, 2), (2, 3)):
        H[left, right] = 1
        H[right, left] = 1
    # Oriented edge 3 -> 0 carries exp(i q f).
    H[3, 0] = phase
    H[0, 3] = sp.conjugate(phase)

    trace_h4 = sp.simplify(sp.expand_complex(sp.trace(H**4)))
    expected_trace = 24 + 8 * sp.cos(q * f)
    flux_trace = sp.simplify(trace_h4 - trace_h4.subs(f, 0))
    logdet_flux_order4 = sp.simplify(-kappa**4 * flux_trace / 4)
    expected_logdet_flux = sp.simplify(
        -2 * kappa**4 * (sp.cos(q * f) - 1)
    )
    wilson_beta = sp.simplify(2 * kappa**4 * q**2)
    quadratic_flux_coefficient = sp.simplify(
        sp.diff(logdet_flux_order4, f, 2).subs(f, 0) / 2
    )

    kappa_a, q_a = sp.symbols("kappa_a q_a", real=True)
    return {
        "four_site_hopping_matrix": H,
        "trace_H4": trace_h4,
        "trace_H4_identity": sp.simplify(trace_h4 - expected_trace) == 0,
        "flux_sensitive_logdet_at_order4": logdet_flux_order4,
        "logdet_flux_identity": sp.simplify(
            logdet_flux_order4 - expected_logdet_flux
        )
        == 0,
        "induced_Wilson_beta_per_mode": wilson_beta,
        "quadratic_flux_coefficient": quadratic_flux_coefficient,
        "many_mode_leading_beta": "2 sum_a kappa_a^4 q_a^2",
        "many_mode_symbols": (kappa_a, q_a),
        "higher_closed_loops_begin_at": "O(kappa^6) on a hypercubic lattice",
        "absolute_stiffness_requires_full_determinant": True,
        "reference_value_used": False,
    }


def continuous_hopping_gap_witness() -> dict[str, object]:
    """Show that fixed topology and charges do not fix the stiffness."""

    kappa = sp.symbols("kappa", positive=True)
    projective_unit_charge = sp.Integer(1)
    beta_projective = sp.simplify(
        2 * kappa**4 * projective_unit_charge**2
    )
    witness_values = (sp.Rational(1, 4), sp.Rational(1, 3))
    witness_betas = tuple(
        sp.simplify(beta_projective.subs(kappa, value))
        for value in witness_values
    )

    return {
        "projective_link_charge": projective_unit_charge,
        "centered_spin1_weights_are_not_link_charges": True,
        "leading_projective_link_beta": beta_projective,
        "same_charge_lattice_hopping_gap_witnesses": witness_values,
        "different_induced_betas": witness_betas,
        "witnesses_are_distinct": witness_betas[0] != witness_betas[1],
        "d_beta_d_kappa": sp.diff(beta_projective, kappa),
        "fixed_C3_and_compactness_determine_stiffness": False,
        "reference_value_used": False,
    }


def ordered_frame_stueckelberg_mass_audit() -> dict[str, object]:
    """Check whether an independent frame link is massless on the p18h branch.

    The current ordered-frame action contains kappa_f (d theta+a)^2.  If a is
    an independent connection and an induced Maxwell term is added, unitary
    gauge theta=0 leaves a Proca mass.  A massless emergent photon therefore
    requires a distinct Coulomb phase rather than the ordered north-pole
    expansion itself.
    """

    K, kappa_f = sp.symbols("K_F kappa_f", positive=True)
    canonical_mass_squared = sp.simplify(2 * kappa_f / K)
    return {
        "ordered_frame_term": "kappa_f (partial theta+a)^2",
        "unitary_gauge_term": "kappa_f a_mu a^mu",
        "induced_kinetic_term": "-K_F f_mu_nu f^mu_nu/4",
        "canonical_vector_mass_squared": canonical_mass_squared,
        "positive_ordered_frame_stiffness_gives_mass": True,
        "composite_connection_branch": (
            "no quadratic Maxwell propagator, as proved in p18bp"
        ),
        "independent_connection_on_ordered_branch": "Stueckelberg/Higgs massive",
        "massless_route": (
            "derive a separate 3+1D Coulomb phase with an uncondensed charged "
            "field and a deconfined compact link"
        ),
        "current_ordered_frame_branch_is_massless_photon_phase": False,
        "reference_value_used": False,
    }


def p18f_axis_cp1_higgs_mass_theorem() -> dict[str, object]:
    """Rewrite the actual p18f axis kinetic term and canonically normalize it.

    In a CP1 chart

        z=(cos(chi/2), exp(i phi) sin(chi/2)),
        n=z^dagger sigma z,

    the exact identity is (d n)^2=4|D z|^2.  Promoting the projective
    connection to an independent field on the ordered p18f background gives
    a positive Higgs mass.  This is separate from the p18h fiber mass audited
    above and already suffices to exclude a massless link on that branch.
    """

    chi = sp.symbols("chi", real=True)
    dchi, dphi = sp.symbols("dchi dphi", real=True)
    z = sp.Matrix(
        [
            sp.cos(chi / 2),
            sp.exp(sp.I * sp.symbols("phi", real=True)) * sp.sin(chi / 2),
        ]
    )
    dz = sp.Matrix(
        [
            sp.diff(z[0], chi) * dchi,
            sp.diff(z[1], chi) * dchi
            + sp.diff(z[1], sp.symbols("phi", real=True)) * dphi,
        ]
    )
    berry = sp.simplify(-sp.I * (z.conjugate().T * dz)[0])
    Dz = sp.simplify(dz - z * (z.conjugate().T * dz)[0])
    cp1_norm = sp.trigsimp(
        sp.expand_complex((Dz.conjugate().T * Dz)[0]), method="fu"
    )
    sphere_norm = sp.simplify(dchi**2 + sp.sin(chi) ** 2 * dphi**2)
    identity_residual = sp.trigsimp(sphere_norm - 4 * cp1_norm, method="fu")

    K_F, kappa_n, condensate = sp.symbols(
        "K_F kappa_n v", positive=True
    )
    mass_squared = sp.simplify(8 * kappa_n * condensate**2 / K_F)
    ordered_mass_squared = sp.simplify(mass_squared.subs(condensate, 1))

    return {
        "CP1_chart": z,
        "Berry_one_form": berry,
        "CP1_covariant_norm": cp1_norm,
        "sphere_metric_norm": sphere_norm,
        "exact_dn_squared_equals_4_Dz_squared": identity_residual == 0,
        "p18f_background_stiffness": (
            "kappa_n=kn_P+kn_PY+3 kn_PI1+3 kn_PI2+kn_PI3"
        ),
        "p18f_axis_action_in_CP1": "L_axis=4 kappa_n |(partial-i a)z|^2",
        "canonical_vector_mass_squared": mass_squared,
        "ordered_unit_norm_mass_squared": ordered_mass_squared,
        "positive_stability_stiffness_implies_positive_mass": True,
        "massless_if_and_only_if_in_this_tree_sector": "v=0 or kappa_n=0",
        "kappa_n_zero_keeps_p18f_axis_waves_healthy": False,
        "ordered_p18f_axis_is_massless_projective_photon": False,
        "reference_value_used": False,
    }


def continuum_microscopic_completion_nonuniqueness_theorem() -> dict[str, object]:
    """Exhibit two UV bond actions with the same p18f quadratic continuum.

    The p18f continuum EFT determines the coefficient of (d n)^2.  It does
    not determine higher powers of the bond angle or ring exchange.  Those
    operators are invisible in the quadratic continuum gate but change the
    HS measure and the induced plaquette action.
    """

    delta, J, lam = sp.symbols("delta J lambda_4", real=True)
    nearest = J * (1 - sp.cos(delta))
    extended = nearest + lam * (1 - sp.cos(delta)) ** 2
    nearest_series = sp.series(nearest, delta, 0, 6).removeO().expand()
    extended_series = sp.series(extended, delta, 0, 6).removeO().expand()
    quadratic_nearest = sp.expand(nearest_series).coeff(delta, 2)
    quadratic_extended = sp.expand(extended_series).coeff(delta, 2)
    quartic_difference = sp.simplify(
        sp.expand(extended_series - nearest_series).coeff(delta, 4)
    )
    witnesses = tuple(
        sp.expand(extended_series.subs(lam, value))
        for value in (sp.Integer(0), sp.Integer(1))
    )

    return {
        "nearest_neighbor_bond": nearest,
        "higher_response_bond": extended,
        "nearest_series": nearest_series,
        "extended_series": extended_series,
        "same_quadratic_continuum_coefficient": sp.simplify(
            quadratic_nearest - quadratic_extended
        )
        == 0,
        "quartic_difference": quartic_difference,
        "same_IR_different_UV_witnesses": witnesses,
        "witnesses_differ": sp.simplify(witnesses[0] - witnesses[1]) != 0,
        "ring_exchange_coefficient_visible_in_p18f_quadratic_gate": False,
        "p18f_continuum_uniquely_selects_nearest_neighbor_action": False,
        "no_bare_plaquette_follows_from_current_continuum_EFT": False,
        "physical_reading": (
            "minimal power counting selects an IR truncation, not a unique "
            "microscopic regulator or zero ring-exchange coefficient"
        ),
        "reference_value_used": False,
    }


def ordered_higgs_vs_coulomb_phase_dichotomy() -> dict[str, object]:
    """Separate the p18f Goldstone phase from an emergent-photon phase."""

    return {
        "ordered_branch": {
            "order_parameter": "<z> nonzero, equivalently a chosen n=e3 background",
            "low_energy_axis_modes": "two O(3)->O(2) Goldstone/magnon modes",
            "projective_link": "Higgs/Stueckelberg massive",
            "massless_emergent_photon": False,
        },
        "coulomb_branch": {
            "order_parameter": "<z>=0 with gapped projective charges",
            "low_energy_axis_modes": "no p18f north-pole Goldstone pair",
            "projective_link": "deconfined massless U(1) gauge mode if monopoles are suppressed",
            "massless_emergent_photon": True,
        },
        "same_two_modes_in_both_branches": False,
        "p18f_axis_helicity_pair_can_be_relabelled_as_Coulomb_photon": False,
        "current_RefG_action_selects_coulomb_branch": False,
        "required_decision": (
            "either retain the ordered frame and stop identifying its axis "
            "waves with photons, or derive a distinct quantum-disordered "
            "Coulomb sector whose gauge mode is the photon"
        ),
        "reference_value_used": False,
    }


def physical_photon_generator_separation_theorem() -> dict[str, object]:
    """Keep family/frame weights separate from the physical photon."""

    a, b, c = sp.symbols("a b c", real=True)
    family_weights = (-1, 0, 1)
    neutrino_charges = tuple(
        sp.simplify((a - b) / 2 + c * weight)
        for weight in family_weights
    )
    neutral_solution = sp.linsolve(neutrino_charges, (a, b, c))
    electron_charge = sp.simplify(-a / 2 - b / 2)
    primitive_solution = sp.linsolve(
        (*neutrino_charges, electron_charge + 1), (a, b, c)
    )

    return {
        "general_neutral_generator": "Q'=a T3+b Y+c F",
        "neutrino_charges": neutrino_charges,
        "neutral_solution": neutral_solution,
        "primitive_electron_solution": primitive_solution,
        "physical_generator_is_Q_T3_plus_Y": primitive_solution
        == sp.FiniteSet((1, 1, 0)),
        "family_frame_coefficient_in_photon": 0,
        "C3_role_if_retained": "generation multiplicity/representation, not electric charge",
        "CP1_auxiliary_link_is_automatically_physical_photon": False,
        "required_bridge": (
            "derive a generation-blind electroweak representation on the "
            "complete charged-core Hilbert space"
        ),
        "reference_value_used": False,
    }


def constructive_route_contract() -> dict[str, object]:
    """State why the minimal nearest-bond route is not a current closure."""

    return {
        "selected_mechanism": (
            "conditional exact auxiliary link from a separately derived "
            "microscopic quartic bond, followed by the complete finite "
            "charged-core determinant"
        ),
        "why_selected": (
            "an exact HS rewrite can remove the independent bare plaquette "
            "parameter rather than merely setting it to zero by hand"
        ),
        "next_mathematical_object": (
            "a localized phase-normalized F_min core, its orientational "
            "moduli-space inertia and its inter-core overlap/ring action"
        ),
        "must_derive_in_order": (
            "derive the microscopic frame/charged-core bond from p01/F_min",
            "perform the HS rewrite while retaining the link amplitude",
            "derive the saddle/gap equations and every kappa_a=t_a/M_a^2",
            "show that the microscopic parameters lie in a deconfined 3+1D Coulomb phase rather than the ordered Higgs or confined phase",
            "prove that the surviving compact link acts as Q=T3+Y, with C3 only as a generation index",
            "compute the full transverse polarization/determinant and its continuum limit",
            "derive the electroweak breaking, QCD vacuum polarization and Thomson matching from the same spectrum",
        ),
        "success_condition": (
            "all hopping/gap ratios are isolated solutions of target-free "
            "core equations, the link has a massless transverse pole, and no "
            "independent plaquette/counterterm direction remains"
        ),
        "failure_condition": (
            "if the core equations leave any continuous kappa or finite F^2 "
            "direction, this induced route does not predict the coupling"
        ),
        "current_Fmin_microscopic_bond_derived": False,
        "current_ring_coefficient_forced_zero": False,
        "exact_link_integration_leaves_independent_flux_stiffness": False,
        "leading_induced_plaquette_proves_deconfinement": False,
        "minimal_nearest_bond_route_verdict": (
            "negative for the current RefG action: F_min is eigenframe-blind, "
            "p18f leaves kappa_n free, the regulator is nonunique, and exact "
            "c2=0 link integration returns a bond-local spin action"
        ),
        "current_ordered_branch_verdict": (
            "rejected as a massless-photon phase; its two axis modes are "
            "ordered-frame Goldstones and its independent link is Higgsed"
        ),
        "fallback_if_failure": (
            "compute the full RefG gravity-gauge beta system and seek an "
            "isolated UV fixed point with no relevant direction projecting "
            "onto the physical photon stiffness"
        ),
        "reference_value_used": False,
    }


def primary_reference_ledger() -> tuple[dict[str, str], ...]:
    return (
        {
            "source": "https://arxiv.org/abs/0711.0818",
            "result": (
                "3+1D compact CP1+U1 has distinct Higgs, Coulomb and "
                "confinement phases; a massless gauge mode is phase-dependent "
                "and the plaquette coupling is an independent phase control"
            ),
        },
        {
            "source": "https://arxiv.org/abs/hep-lat/0311006",
            "result": (
                "in four-dimensional compact U1 theory the helicity modulus "
                "is a phase diagnostic and the renormalized transition "
                "coupling is not universal"
            ),
        },
        {
            "source": "https://arxiv.org/abs/1102.5035",
            "result": (
                "a Maxwell term can be generated dynamically in gauge models "
                "without a microscopic Maxwell term"
            ),
        },
        {
            "source": "https://arxiv.org/abs/1511.08374",
            "result": (
                "finite auxiliary bosons can induce a lattice gauge action "
                "and its continuum coupling requires an explicit matching"
            ),
        },
    )


def source_firewall() -> dict[str, object]:
    source = inspect.getsource(inspect.getmodule(source_firewall))
    tree = ast.parse(source)
    numeric_literals = tuple(
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    )
    forbidden_modules = ("p18" + "bm", "p18" + "bk")
    forbidden_text = ("CO" + "DATA", "observed " + "inverse")
    return {
        "contains_comparison_numeric_literal": any(
            isinstance(value, float) and 100 < abs(value) < 200
            for value in numeric_literals
        ),
        "imports_comparison_module": any(name in source for name in forbidden_modules),
        "contains_comparison_text": any(text in source for text in forbidden_text),
        "target_isolation_pass": not any(
            (
                any(
                    isinstance(value, float) and 100 < abs(value) < 200
                    for value in numeric_literals
                ),
                any(name in source for name in forbidden_modules),
                any(text in source for text in forbidden_text),
            )
        ),
    }


def run_gate() -> None:
    cp1 = cp1_spin1_rewrite_theorem()
    fmin = fmin_eigenframe_blindness_theorem()
    rigidity = compatible_unstrained_frame_rigidity_theorem()
    bond_scope = p18f_continuum_to_cp1_bond_scope_theorem()
    ring = allowed_cp1_ring_operator_theorem()
    hs = exact_hubbard_stratonovich_link_theorem()
    phase_integral = exact_fixed_amplitude_link_phase_audit()
    plaquette = leading_induced_plaquette_theorem()
    witness = continuous_hopping_gap_witness()
    mass = ordered_frame_stueckelberg_mass_audit()
    axis_mass = p18f_axis_cp1_higgs_mass_theorem()
    uv_nonunique = continuum_microscopic_completion_nonuniqueness_theorem()
    phase = ordered_higgs_vs_coulomb_phase_dichotomy()
    photon = physical_photon_generator_separation_theorem()
    route = constructive_route_contract()
    firewall = source_firewall()

    assert cp1["exact_fierz_identity"]
    assert cp1["spin1_dimension_equals_C3_dimension"]
    assert cp1["h2_closure_component_hopping_and_phase_roles_are_distinct"]
    assert fmin["all_Fmin_invariants_eigenframe_blind"]
    assert fmin["physical_slice_normal_form_exact"]
    assert fmin["p01_Fmin_derives_nonzero_frame_stiffness"] is False
    assert rigidity["full_rank_27"]
    assert rigidity["constraint_nullity"] == 0
    assert rigidity["local_unstrained_rotation_is_constant"]
    assert bond_scope["scale_direction_is_free"]
    assert bond_scope["p18f_fixes_absolute_kappa_n"] is False
    assert bond_scope["conditional_J_CP1_equals_4_kappa_n_a2"]
    assert bond_scope["same_two_derivative_continuum_for_all_delta"]
    assert bond_scope["higher_moment_depends_on_delta"]
    assert bond_scope["nearest_neighbor_CP1_bond_uniquely_implied_by_continuum"] is False
    assert ring["ring_is_local_projective_U1_invariant"]
    assert ring["p01_or_p18f_symmetry_forces_rho_square_zero"] is False
    assert hs["HS_identity_exact"]
    assert hs["link_hopping_is_gauge_invariant"]
    assert hs["bare_plaquette_in_exact_one_bond_rewrite"] == 0
    assert hs["unconditional_no_bare_plaquette_theorem_for_current_RefG"] is False
    assert hs["freezing_link_amplitude_is_extra_saddle_assumption"]
    assert phase_integral["all_order_I0_identity_verified"]
    assert phase_integral["CP1_overlap_spin_identity_exact"]
    assert phase_integral["independent_flux_stiffness_after_exact_phase_integration"] is False
    assert phase_integral["leading_induced_plaquette_alone_proves_deconfinement"] is False
    assert plaquette["trace_H4_identity"]
    assert plaquette["logdet_flux_identity"]
    assert witness["witnesses_are_distinct"]
    assert witness["fixed_C3_and_compactness_determine_stiffness"] is False
    assert mass["current_ordered_frame_branch_is_massless_photon_phase"] is False
    assert axis_mass["exact_dn_squared_equals_4_Dz_squared"]
    assert axis_mass["ordered_p18f_axis_is_massless_projective_photon"] is False
    assert uv_nonunique["same_quadratic_continuum_coefficient"]
    assert uv_nonunique["witnesses_differ"]
    assert uv_nonunique["no_bare_plaquette_follows_from_current_continuum_EFT"] is False
    assert phase["p18f_axis_helicity_pair_can_be_relabelled_as_Coulomb_photon"] is False
    assert photon["physical_generator_is_Q_T3_plus_Y"]
    assert photon["CP1_auxiliary_link_is_automatically_physical_photon"] is False
    assert firewall["target_isolation_pass"]

    for title, payload in (
        ("CP1/spin-one rewrite", cp1),
        ("F_min eigenframe blindness", fmin),
        ("compatible unstrained-frame rigidity", rigidity),
        ("p18f continuum/Wilson bond scope", bond_scope),
        ("allowed CP1 ring operator", ring),
        ("exact HS auxiliary link", hs),
        ("exact c2=0 fixed-amplitude phase integration", phase_integral),
        ("leading induced plaquette", plaquette),
        ("continuous hopping-gap witness", witness),
        ("ordered-frame Stueckelberg mass", mass),
        ("p18f axis CP1 Higgs mass", axis_mass),
        ("continuum/microscopic nonuniqueness", uv_nonunique),
        ("ordered-Higgs versus Coulomb phase", phase),
        ("physical photon separation", photon),
        ("constructive route contract", route),
        ("source firewall", firewall),
    ):
        print(f"\n{title}")
        for key, value in payload.items():
            print(f"  {key}: {value}")

    print("\nprimary references")
    for row in primary_reference_ledger():
        print(f"  {row['source']}: {row['result']}")

    print(
        "\nSTATUS: BLOCKED_MICROSCOPIC_FRAME_BOND_NOT_DERIVED_FROM_FMIN__"
        "REJECT_MINIMAL_NEAREST_BOND_AND_CURRENT_ORDERED_FRAME_AS_"
        "MASSLESS_PHOTON__OPEN_DISTINCT_COULOMB_OR_UV_FIXED_POINT_"
        "PHYSICAL_Q_BRIDGE_AND_FULL_MATCHING__PASS_FMIN_ORIENTATION_"
        "BLINDNESS_REGULATOR_NONUNIQUENESS_CONDITIONAL_CP1_HS_AND_"
        "INDUCED_PLAQUETTE_THEOREMS"
    )


if __name__ == "__main__":
    run_gate()
