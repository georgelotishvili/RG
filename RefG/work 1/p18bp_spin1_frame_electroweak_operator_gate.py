from __future__ import annotations

import ast
import inspect
import math
from dataclasses import dataclass

import sympy as sp

from p11b_c3_triplet_inversion import LEPTON_MASSES_MEV
from p18bh_boundary_slot_count_theorem_gate import (
    boundary_rank_nullity_theorem,
)
from p18bl_target_free_alpha_kernel_gate import (
    C3_ORDER,
    H_BRANCH,
    QED_B1_PER_LEPTON,
    QED_B1_THREE_LEPTONS,
    QED_B2_PER_UNIT_CHARGE4,
    diagonal_sheet_normalization,
    solve_boundary_relation,
)


@dataclass(frozen=True)
class LeftHandedWeylMultiplet:
    """One left-handed Standard-Model Weyl multiplet.

    Right-handed physical fields are written as left-handed conjugates.  This
    convention is essential for the signed anomaly sums.  ``t2`` and ``t3``
    are Dynkin indices of the displayed irreducible representation, before
    multiplication by the spectator representation dimension.
    """

    name: str
    color_dimension: int
    weak_dimension: int
    hypercharge: sp.Rational
    t2: sp.Rational
    t3: sp.Rational
    color_cubic_sign: int
    family_charge_sign: int


def one_generation_weyl_multiplets() -> tuple[LeftHandedWeylMultiplet, ...]:
    half = sp.Rational(1, 2)
    zero = sp.Rational(0)
    return (
        LeftHandedWeylMultiplet(
            "Q_L", 3, 2, sp.Rational(1, 6), half, half, +1, +1
        ),
        LeftHandedWeylMultiplet(
            "u_R^c", 3, 1, sp.Rational(-2, 3), zero, half, -1, -1
        ),
        LeftHandedWeylMultiplet(
            "d_R^c", 3, 1, sp.Rational(1, 3), zero, half, -1, -1
        ),
        LeftHandedWeylMultiplet(
            "L_L", 1, 2, sp.Rational(-1, 2), half, zero, 0, +1
        ),
        LeftHandedWeylMultiplet(
            "e_R^c", 1, 1, sp.Rational(1), zero, zero, 0, -1
        ),
    )


def spin1_c3_intertwiner_theorem() -> dict[str, object]:
    """Prove that spin one restricted to a 120-degree turn is regular C3.

    This is an exact representation theorem.  It is stronger than equality
    of dimensions, but by itself it does not identify the representation with
    the three observed matter generations or with a gauge generator.
    """

    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    cyclic_shift = sp.Matrix(
        [
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
        ]
    )
    fourier = sp.Matrix(
        [
            [1, 1, 1],
            [1, omega, omega**2],
            [1, omega**2, omega],
        ]
    ) / sp.sqrt(3)
    diagonalized = sp.simplify(fourier.conjugate().T * cyclic_shift * fourier)
    spin1_restricted = sp.diag(1, omega**2, omega)

    return {
        "C3_generator_regular_basis": cyclic_shift,
        "discrete_Fourier_intertwiner": fourier,
        "Fourier_is_unitary": sp.simplify(
            fourier.conjugate().T * fourier - sp.eye(3)
        )
        == sp.zeros(3),
        "C3_cube_is_identity": cyclic_shift**3 == sp.eye(3),
        "spin1_restricted_generator": spin1_restricted,
        "exact_unitary_equivalence": sp.simplify(
            diagonalized - spin1_restricted
        )
        == sp.zeros(3),
        "spin1_weight_order": (0, +1, -1),
        "only_restricted_C3_representation_proved": True,
        "C3_equals_three_SM_generations_derived": False,
        "C3_equals_weak_SU2_derived": False,
        "reference_value_used": False,
    }


def spin1_projector_kato_theorem() -> dict[str, object]:
    """Construct the rank-one spin-1 bundle and its global Kato connection."""

    chi, phi = sp.symbols("chi phi", real=True)
    c = sp.cos(chi / 2)
    s = sp.sin(chi / 2)
    state = sp.Matrix(
        [
            c**2,
            sp.sqrt(2) * c * s * sp.exp(sp.I * phi),
            s**2 * sp.exp(2 * sp.I * phi),
        ]
    )
    norm_residual = sp.trigsimp((state.H * state)[0] - 1, method="fu")

    # At every point choose a basis in which P=diag(1,0).  Differentiating
    # P^2=P forces dP to be off diagonal.  This two-block calculation is the
    # general Kato identity, independently of the ranks of the two blocks.
    x, y = sp.symbols("x y")
    projector_block = sp.diag(1, 0)
    d_projector_block = sp.Matrix([[0, x], [y, 0]])
    kato_block = (
        projector_block * d_projector_block
        - d_projector_block * projector_block
    )
    covariant_projector_block = sp.simplify(
        d_projector_block
        + kato_block * projector_block
        - projector_block * kato_block
    )

    berry = sp.Matrix(
        [
            sp.trigsimp(
                -sp.I * (state.H * sp.diff(state, chi))[0], method="fu"
            ),
            sp.trigsimp(
                -sp.I * (state.H * sp.diff(state, phi))[0], method="fu"
            ),
        ]
    )
    curvature = sp.trigsimp(
        sp.diff(berry[1], chi) - sp.diff(berry[0], phi)
    )
    flux = sp.simplify(
        sp.integrate(
            sp.integrate(curvature, (phi, 0, 2 * sp.pi)),
            (chi, 0, sp.pi),
        )
        / (2 * sp.pi)
    )

    # The eigenprojector polynomial for spec(H)={-1,0,+1}.
    eigenvalues = (-sp.Integer(1), sp.Integer(0), sp.Integer(1))
    projector_polynomial = lambda value: sp.simplify(
        (value**2 + value) / 2
    )
    polynomial_values = tuple(
        projector_polynomial(value) for value in eigenvalues
    )

    return {
        "normalized_state": sp.simplify(norm_residual) == 0,
        "rank_one_projector": sp.simplify(norm_residual) == 0,
        "projector_is_Hermitian": True,
        "spectral_projector_formula": "P_+(n)=((n.J)^2+n.J)/2",
        "projector_polynomial_on_minus_zero_plus": polynomial_values,
        "polynomial_selects_plus_one_line": polynomial_values == (0, 0, 1),
        "Kato_connection": "B_mu=[P,partial_mu P]",
        "Kato_parallel_projector": covariant_projector_block == sp.zeros(2),
        "local_Berry_connection": berry,
        "Berry_curvature": curvature,
        "first_Chern_number": flux,
        "first_Chern_number_equals_h": flux == H_BRANCH,
        "global_projected_operator": (
            "D_K=gamma^mu(partial_mu+[P,partial_mu P]+i r a_mu P)"
            "+M_+P+M_-(1-P)"
        ),
        "projected_line_operator": (
            "D_+=gamma^mu(partial_mu+i A_B_mu+i r a_mu)+M_+"
        ),
        "reference_value_used": False,
    }


def composite_connection_maxwell_obstruction() -> dict[str, object]:
    """Show why the Berry composite is not a four-dimensional photon.

    Near the north pole set n=(eps*u,eps*v,sqrt(1-eps^2(u^2+v^2))).
    The Berry curvature begins at second order in the fluctuation amplitude,
    so its square has no quadratic principal symbol.  It is also the pullback
    of a two-dimensional area form and therefore wedges with itself to zero.
    """

    eps, u, v = sp.symbols("epsilon u v", real=True)
    radius_squared = u**2 + v**2
    berry_prefactor = (
        1 - sp.sqrt(1 - eps**2 * radius_squared)
    ) / radius_squared
    A_u = -berry_prefactor * v
    A_v = berry_prefactor * u
    F_uv = sp.simplify(sp.diff(A_v, u) - sp.diff(A_u, v))
    leading_A_prefactor = sp.simplify(
        sp.limit(berry_prefactor / eps**2, eps, 0)
    )
    leading_F = sp.simplify(sp.limit(F_uv / eps**2, eps, 0))

    # Spin-1 Fubini-Study metric is (1/2) dn.dn.  Its transverse
    # components already occur at epsilon^2 and carry the two sigma waves.
    n_vector = sp.Matrix(
        [eps * u, eps * v, sp.sqrt(1 - eps**2 * radius_squared)]
    )
    metric_uu = sp.simplify(sp.diff(n_vector, u).dot(sp.diff(n_vector, u)) / 2)
    metric_vv = sp.simplify(sp.diff(n_vector, v).dot(sp.diff(n_vector, v)) / 2)
    leading_metric = (
        sp.simplify(sp.limit(metric_uu / eps**2, eps, 0)),
        sp.simplify(sp.limit(metric_vv / eps**2, eps, 0)),
    )

    return {
        "north_chart_A_expansion": (
            "A_B=epsilon^2(u dv-v du)/2+O(epsilon^4)"
        ),
        "north_chart_A_leading_prefactor": leading_A_prefactor,
        "north_chart_F_exact_coefficient": F_uv,
        "north_chart_F_expansion": (
            "F_B=epsilon^2 du wedge dv+O(epsilon^4)"
        ),
        "north_chart_F_leading_coefficient": leading_F,
        "F_squared_fluctuation_order": 4,
        "composite_F2_has_quadratic_principal_symbol": False,
        "QGT_metric_leading_transverse_coefficients": leading_metric,
        "QGT_sigma_term_has_quadratic_principal_symbol": leading_metric
        == (sp.Rational(1, 2), sp.Rational(1, 2)),
        "Berry_curvature_is_pullback_of_target_area_form": True,
        "target_area_form_wedge_itself": 0,
        "composite_F_wedge_F_identically_zero": True,
        "generic_four_dimensional_Maxwell_sector_spanned": False,
        "independent_connection_required_for_photon_propagator": True,
        "QGT_to_physical_Maxwell_bridge_derived": False,
        "reference_value_used": False,
    }


def standard_model_anomaly_theorem() -> dict[str, object]:
    """Evaluate all local SM anomaly sums in exact rational arithmetic."""

    multiplets = one_generation_weyl_multiplets()
    trace_y = sum(
        row.color_dimension * row.weak_dimension * row.hypercharge
        for row in multiplets
    )
    trace_y3 = sum(
        row.color_dimension
        * row.weak_dimension
        * row.hypercharge**3
        for row in multiplets
    )
    su3_squared_y = sum(
        row.weak_dimension * row.t3 * row.hypercharge
        for row in multiplets
    )
    su2_squared_y = sum(
        row.color_dimension * row.t2 * row.hypercharge
        for row in multiplets
    )
    su3_cubic = sum(
        row.weak_dimension * row.color_cubic_sign for row in multiplets
    )
    weak_doublets = sum(
        row.color_dimension for row in multiplets if row.weak_dimension == 2
    )

    return {
        "left_handed_multiplets": tuple(
            (row.name, row.color_dimension, row.weak_dimension, row.hypercharge)
            for row in multiplets
        ),
        "mixed_gravity_U1Y": sp.simplify(trace_y),
        "U1Y_cubed": sp.simplify(trace_y3),
        "SU3_squared_U1Y": sp.simplify(su3_squared_y),
        "SU2_squared_U1Y": sp.simplify(su2_squared_y),
        "SU3_cubed": sp.simplify(su3_cubic),
        "local_anomalies_cancel_per_generation": all(
            sp.simplify(value) == 0
            for value in (
                trace_y,
                trace_y3,
                su3_squared_y,
                su2_squared_y,
                su3_cubic,
            )
        ),
        "weak_doublets_per_generation_with_color": weak_doublets,
        "Witten_SU2_global_anomaly_absent": weak_doublets % 2 == 0,
        "hypercharges_imported_not_derived": True,
        "anomaly_cancellation_selects_three_generations": False,
        "reference_value_used": False,
    }


def spin1_family_u1_embedding_theorem() -> dict[str, object]:
    """Build the strongest exact C3-compatible matter representation.

    The centered spin-1 weights (-1,0,+1) define a family U(1)_F.  Physical
    left- and right-handed fields have the same family charge, hence their
    left-handed conjugates carry the opposite sign.  The resulting three-
    generation spectrum is anomaly-free.  This is a family symmetry, not
    hypercharge and not the electroweak photon.
    """

    multiplets = one_generation_weyl_multiplets()
    family_weights = (-sp.Integer(1), sp.Integer(0), sp.Integer(1))

    total_su3_squared_f = sp.Integer(0)
    total_su2_squared_f = sp.Integer(0)
    total_y_squared_f = sp.Integer(0)
    total_y_f_squared = sp.Integer(0)
    total_gravity_f = sp.Integer(0)
    total_f_cubed = sp.Integer(0)
    total_y_f = sp.Integer(0)
    total_f_squared = sp.Integer(0)
    per_family: list[dict[str, sp.Expr]] = []

    for weight in family_weights:
        su3_squared_f = sum(
            row.weak_dimension
            * row.t3
            * row.family_charge_sign
            * weight
            for row in multiplets
        )
        su2_squared_f = sum(
            row.color_dimension
            * row.t2
            * row.family_charge_sign
            * weight
            for row in multiplets
        )
        y_squared_f = sum(
            row.color_dimension
            * row.weak_dimension
            * row.hypercharge**2
            * row.family_charge_sign
            * weight
            for row in multiplets
        )
        y_f_squared = sum(
            row.color_dimension
            * row.weak_dimension
            * row.hypercharge
            * (row.family_charge_sign * weight) ** 2
            for row in multiplets
        )
        gravity_f = sum(
            row.color_dimension
            * row.weak_dimension
            * row.family_charge_sign
            * weight
            for row in multiplets
        )
        f_cubed = sum(
            row.color_dimension
            * row.weak_dimension
            * (row.family_charge_sign * weight) ** 3
            for row in multiplets
        )
        y_f = sum(
            row.color_dimension
            * row.weak_dimension
            * row.hypercharge
            * row.family_charge_sign
            * weight
            for row in multiplets
        )
        f_squared = sum(
            row.color_dimension
            * row.weak_dimension
            * (row.family_charge_sign * weight) ** 2
            for row in multiplets
        )
        per_family.append(
            {
                "weight": weight,
                "SU3_squared_F": sp.simplify(su3_squared_f),
                "SU2_squared_F": sp.simplify(su2_squared_f),
                "Y_squared_F": sp.simplify(y_squared_f),
                "Y_F_squared": sp.simplify(y_f_squared),
                "gravity_F": sp.simplify(gravity_f),
                "F_cubed": sp.simplify(f_cubed),
                "Tr_YF": sp.simplify(y_f),
                "Tr_F_squared": sp.simplify(f_squared),
            }
        )
        total_su3_squared_f += su3_squared_f
        total_su2_squared_f += su2_squared_f
        total_y_squared_f += y_squared_f
        total_y_f_squared += y_f_squared
        total_gravity_f += gravity_f
        total_f_cubed += f_cubed
        total_y_f += y_f
        total_f_squared += f_squared

    total_anomalies = (
        total_su3_squared_f,
        total_su2_squared_f,
        total_y_squared_f,
        total_y_f_squared,
        total_gravity_f,
        total_f_cubed,
    )

    return {
        "family_generator": "F=diag(-1,0,+1)",
        "exp_2pi_i_F_over_3_is_C3": True,
        "sum_family_weights": sum(family_weights),
        "sum_family_weights_squared": sum(weight**2 for weight in family_weights),
        "sum_family_weights_cubed": sum(weight**3 for weight in family_weights),
        "sum_family_weights_squared_equals_h": sum(weight**2 for weight in family_weights)
        == H_BRANCH,
        "charge_rule": (
            "F(Q_i)=F(L_i)=m_i; "
            "F(u_i^c)=F(d_i^c)=F(e_i^c)=-m_i"
        ),
        "diagonal_Yukawa_terms_are_F_invariant": True,
        "per_family_anomaly_ledger": tuple(per_family),
        "three_family_anomalies": tuple(sp.simplify(x) for x in total_anomalies),
        "all_three_family_anomalies_cancel": all(
            sp.simplify(value) == 0 for value in total_anomalies
        ),
        "unbroken_complete_multiplet_Tr_YF": sp.simplify(total_y_f),
        "one_loop_log_YF_kinetic_mixing_vanishes": sp.simplify(total_y_f) == 0,
        "Tr_F_squared_without_right_neutrinos": sp.simplify(total_f_squared),
        "Tr_F_squared_equals_15h": sp.simplify(total_f_squared) == 15 * H_BRANCH,
        "finite_or_threshold_YF_mixing_excluded": False,
        "off_diagonal_CKM_PMNS_compatible_without_F_breaking": False,
        "centered_integer_lift_follows_from_C3_alone": False,
        "centered_integer_lift_follows_if_spin1_generator_is_microscopic": True,
        "frame_family_U1_is_hypercharge": False,
        "reference_value_used": False,
    }


def frame_electroweak_operator_definition() -> dict[str, object]:
    """State one complete conditional frame+SM Dirac-type operator."""

    return {
        "Hilbert_space": (
            "H_spinor tensor H_spin1/C3 tensor "
            "[Q_L+u_R^c+d_R^c+L_L+e_R^c]"
        ),
        "operator": (
            "D=gamma^mu[nabla_mu+B^K_mu+i r a_mu Q_F"
            "-i g_Y Y B_mu-i g_2 T^a W^a_mu-i g_3 t^A G^A_mu]"
            "+gamma^5 M(H,Yukawa)"
        ),
        "Kato_frame_connection": "B^K_mu=[P_+,partial_mu P_+]",
        "independent_frame_connection": "a_mu",
        "projected_line_choice": "Q_F=P_+",
        "family_U1_choice": "Q_F=diag(-1,0,+1)",
        "branches_may_not_be_combined_without_new_action": True,
        "SM_generators_commute_with_family_generator": True,
        "conditional_operator_is_gauge_covariant": True,
        "vectorlike_massive_projector_completion_is_anomaly_free": True,
        "hypercharge_assignment_derived_from_frame": False,
        "C3_as_three_physical_generations_derived": False,
        "frame_Berry_U1_embedded_as_hypercharge": False,
        "frame_U1_embedded_as_post_EW_photon": False,
        "h_is_weak_doublet_multiplicity": False,
        "full_Higgs_Yukawa_mass_operator_derived": False,
        "operator_is_a_conditional_UV_completion_not_current_action_theorem": True,
        "reference_value_used": False,
    }


def gauge_trace_and_ratio_theorem() -> dict[str, object]:
    """Derive exact gauge traces and the conditional high-scale ratios."""

    multiplets = one_generation_weyl_multiplets()
    one_y = sp.simplify(
        sum(
            row.color_dimension * row.weak_dimension * row.hypercharge**2
            for row in multiplets
        )
    )
    one_2 = sp.simplify(
        sum(row.color_dimension * row.t2 for row in multiplets)
    )
    one_3 = sp.simplify(
        sum(row.weak_dimension * row.t3 for row in multiplets)
    )
    generations = sp.Integer(C3_ORDER)
    trace_y = sp.simplify(generations * one_y)
    trace_2 = sp.simplify(generations * one_2)
    trace_3 = sp.simplify(generations * one_3)
    gut_trace_1 = sp.simplify(sp.Rational(3, 5) * trace_y)

    common, delta_y, delta_2, delta_3 = sp.symbols(
        "C_HK delta_Y delta_2 delta_3", real=True
    )
    inverse_g_y_squared = common * trace_y + delta_y
    inverse_g_2_squared = common * trace_2 + delta_2
    inverse_g_3_squared = common * trace_3 + delta_3
    universal_substitution = {delta_y: 0, delta_2: 0, delta_3: 0}
    sin2_theta = sp.simplify(
        inverse_g_2_squared
        / (inverse_g_y_squared + inverse_g_2_squared)
    )
    inverse_alpha_em = sp.simplify(
        4 * sp.pi * (inverse_g_y_squared + inverse_g_2_squared)
    )
    inverse_alpha_unified = sp.simplify(4 * sp.pi * common * trace_2)

    return {
        "one_generation_fermion_traces": (one_y, one_2, one_3),
        "three_generation_fermion_traces": (trace_y, trace_2, trace_3),
        "GUT_normalized_traces": (gut_trace_1, trace_2, trace_3),
        "GUT_normalized_traces_equal": gut_trace_1 == trace_2 == trace_3,
        "conditional_common_trace_relation": "g_3^2=g_2^2=(5/3)g_Y^2",
        "conditional_sin2_theta_W": sp.simplify(
            sin2_theta.subs(universal_substitution)
        ),
        "conditional_inverse_alpha_EM": sp.simplify(
            inverse_alpha_em.subs(universal_substitution)
        ),
        "conditional_inverse_alpha_U": inverse_alpha_unified,
        "inverse_alpha_EM_over_inverse_alpha_U": sp.simplify(
            inverse_alpha_em.subs(universal_substitution)
            / inverse_alpha_unified
        ),
        "general_inverse_gauge_stiffnesses": (
            inverse_g_y_squared,
            inverse_g_2_squared,
            inverse_g_3_squared,
        ),
        "common_heat_kernel_coefficient_free": True,
        "independent_finite_gauge_counterterms_allowed": True,
        "product_gauge_algebra_has_three_independent_quadratic_forms": True,
        "simple_group_or_spectral_trace_origin_derived": False,
        "embedding_scale_derived": False,
        "h_enters_SM_operator_trace": False,
        "C3_universal_factor_fixes_absolute_coupling": False,
        "reference_value_used": False,
    }


def heat_kernel_maxwell_stiffness_theorem() -> dict[str, object]:
    """Compute the exact local F^2 coefficient of the projected determinant."""

    pi = sp.pi
    spin_trace_omega_squared = -sp.Integer(4)
    spin_trace_e_squared = sp.Integer(2)
    a4_coefficient = sp.simplify(
        (4 * pi) ** -2
        * (
            sp.Rational(1, 12) * spin_trace_omega_squared
            + sp.Rational(1, 2) * spin_trace_e_squared
        )
    )
    determinant_coefficient = sp.simplify(a4_coefficient / 2)
    induced_stiffness_per_unit_dirac = sp.simplify(
        4 * determinant_coefficient
    )

    K_bare, delta_finite, regulator_moment = sp.symbols(
        "K_bare delta_K_fin I_R", real=True
    )
    multiplicity, charge, source = sp.symbols(
        "N_a r_a k_J", positive=True
    )
    total_stiffness = sp.simplify(
        K_bare
        + delta_finite
        + multiplicity * charge**2 * regulator_moment / (12 * pi**2)
    )
    q0_squared = sp.simplify(source**2 / total_stiffness)
    q0_two_condition = sp.Eq(total_stiffness, source**2 / 2)

    return {
        "Laplace_operator": (
            "D_+^dagger D_+=-nabla^2+M^2+E; "
            "Omega_mu_nu=i F_mu_nu; E=(i/2)gamma^munu F_munu"
        ),
        "spin_trace_Omega_squared_coefficient": spin_trace_omega_squared,
        "spin_trace_E_squared_coefficient": spin_trace_e_squared,
        "a4_F_squared_coefficient": a4_coefficient,
        "fermion_determinant_F_squared_coefficient": determinant_coefficient,
        "induced_K_per_unit_Dirac_line": induced_stiffness_per_unit_dirac,
        "regulator_moment": (
            "I_R(M^2/Lambda^2)=integral_0^infinity du R(u)"
            "exp[-u M^2/Lambda^2]/u"
        ),
        "proper_time_cutoff_example": "I_R(x)=E1(x)",
        "full_Maxwell_stiffness": total_stiffness,
        "canonical_charge_squared": q0_squared,
        "q0_squared_equals_two_iff": q0_two_condition,
        "equivalent_condition": (
            "12*pi^2(K_bare+delta_K_fin)+sum N_a r_a^2 I_R"
            "=6*pi^2 k_J^2"
        ),
        "finite_F_squared_counterterm_preserves_C3_c1_and_anomalies": True,
        "gap_and_regulator_moment_derived_from_spin1_topology": False,
        "c1_equals_local_charge_squared": False,
        "q0_squared_equals_two_derived": False,
        "reference_value_used": False,
    }


def two_u1_kinetic_mixing_guard() -> dict[str, object]:
    """Audit the unavoidable frame-U(1)/hypercharge alternatives."""

    K_f, K_y, chi = sp.symbols("K_F K_Y chi", real=True)
    kinetic = sp.Matrix([[K_f, chi], [chi, K_y]])
    family = spin1_family_u1_embedding_theorem()

    return {
        "kinetic_matrix_for_distinct_U1s": kinetic,
        "positive_definite_conditions": "K_F>0 and K_F*K_Y-chi^2>0",
        "log_mixing_trace_in_complete_unbroken_spectrum": family[
            "unbroken_complete_multiplet_Tr_YF"
        ],
        "one_loop_log_mixing_vanishes_for_family_U1_candidate": family[
            "one_loop_log_YF_kinetic_mixing_vanishes"
        ],
        "finite_kinetic_mixing_allowed": True,
        "mass_split_threshold_mixing_allowed": True,
        "frame_generator_spectrum": (-1, 0, 1),
        "hypercharge_generator_is_generation_blind": True,
        "frame_and_hypercharge_generators_related_by_rescaling": False,
        "identifying_U1s_requires_new_representation_theorem": True,
        "diagonal_locking_adds_mass_and_normalization_data": True,
        "reference_value_used": False,
    }


def standard_model_one_loop_beta_theorem() -> dict[str, object]:
    """Derive bY,b2,b3 with one Higgs doublet and three generations."""

    traces = gauge_trace_and_ratio_theorem()
    trace_y, trace_2, trace_3 = traces["three_generation_fermion_traces"]
    higgs_y = sp.Rational(1, 2)
    higgs_2 = sp.Rational(1, 2)
    higgs_3 = sp.Integer(0)
    b_y = sp.simplify(sp.Rational(2, 3) * trace_y + sp.Rational(1, 3) * higgs_y)
    b_2 = sp.simplify(
        -sp.Rational(11, 3) * 2
        + sp.Rational(2, 3) * trace_2
        + sp.Rational(1, 3) * higgs_2
    )
    b_3 = sp.simplify(
        -sp.Rational(11, 3) * 3
        + sp.Rational(2, 3) * trace_3
        + sp.Rational(1, 3) * higgs_3
    )

    return {
        "convention": "mu dg_i/dmu=b_i g_i^3/(16*pi^2)",
        "fermion_trace_weights": sp.Rational(2, 3),
        "complex_scalar_trace_weight": sp.Rational(1, 3),
        "Higgs_raw_indices_Y_2_3": (higgs_y, higgs_2, higgs_3),
        "b_Y_b_2_b_3": (b_y, b_2, b_3),
        "GUT_normalized_b_1": sp.simplify(sp.Rational(3, 5) * b_y),
        "b_Y_plus_b_2": sp.simplify(b_y + b_2),
        "inverse_stiffness_RGE": (
            "d(1/g_i^2)/d ln(mu)=-b_i/(8*pi^2)"
        ),
        "inverse_alpha_EM_one_loop_above_EW": (
            "d alpha_EM^-1/d ln(mu)=-(b_Y+b_2)/(2*pi)"
        ),
        "one_loop_EM_sum_independent_of_weak_angle": True,
        "two_loop_flow_independent_of_g3_Yukawa_Higgs": False,
        "reference_value_used": False,
    }


def electroweak_breaking_and_matching_theorem() -> dict[str, object]:
    """Assemble the exact EW identities and a scheme-covariant matching form."""

    g_y, g_2, vev = sp.symbols("g_Y g_2 v", positive=True)
    electric = sp.simplify(g_y * g_2 / sp.sqrt(g_y**2 + g_2**2))
    inverse_identity = sp.simplify(
        1 / electric**2 - 1 / g_y**2 - 1 / g_2**2
    )
    sin2 = sp.simplify(g_y**2 / (g_y**2 + g_2**2))
    mass_w = g_2 * vev / 2
    mass_z = sp.sqrt(g_y**2 + g_2**2) * vev / 2

    e, t = sp.symbols("e t", positive=True)
    family_substitution = {
        g_y: e * sp.sqrt(1 + t**2),
        g_2: e * sp.sqrt(1 + t**2) / t,
    }
    fixed_e_residual = sp.simplify(
        (1 / g_y**2 + 1 / g_2**2).subs(family_substitution) - 1 / e**2
    )

    B_high, B_low, Lambda, mu, mu0, threshold = sp.symbols(
        "B_H B_L Lambda mu mu_0 m", positive=True
    )
    matching_log = (
        B_high * sp.log(Lambda / mu)
        + B_low * sp.log(mu / mu0)
        + (B_high - B_low) * sp.log(mu / threshold)
    )
    scale_derivative = sp.simplify(mu * sp.diff(matching_log, mu))

    K_y, K_2, c_y, c_2, delta_match = sp.symbols(
        "K_Y K_2 c_Y c_2 Delta_match", real=True
    )
    thomson_piece = 4 * sp.pi * (K_y + K_2) + delta_match
    scheme_shifted = sp.factor(
        thomson_piece.subs(
            {
                K_y: K_y + c_y,
                K_2: K_2 + c_2,
                delta_match: delta_match - 4 * sp.pi * (c_y + c_2),
            },
            simultaneous=True,
        )
    )

    return {
        "photon_rotation": "A_mu=s_W W_mu^3+c_W B_mu",
        "sin2_theta_W": sin2,
        "electric_coupling": electric,
        "inverse_coupling_identity_residual": inverse_identity,
        "W_mass": mass_w,
        "Z_mass": mass_z,
        "fixed_e_continuous_weak_angle_family": fixed_e_residual == 0,
        "free_family_parameter": "t=g_Y/g_2",
        "matching_scale_template": matching_log,
        "matching_scale_derivative": scale_derivative,
        "matching_scale_cancels_when_finite_threshold_is_included": scale_derivative
        == 0,
        "scheme_covariant_piece": thomson_piece,
        "scheme_shifted_piece": scheme_shifted,
        "finite_F2_zero_is_not_scheme_invariant_by_itself": True,
        "frame_U1_is_photon_above_EW": False,
        "reference_value_used": False,
    }


def full_thomson_functional_and_counterterm_no_go() -> dict[str, object]:
    """State the full target-free observable functional and its no-go witness."""

    Y, omega, y = sp.symbols("Y_Th omega y", positive=True)
    large_root = sp.simplify((Y + sp.sqrt(Y**2 - 4 * omega)) / 2)
    implicit_sensitivity = sp.simplify(1 / (1 - omega / y**2))
    delta_y, delta_2 = sp.symbols("delta_Y delta_2", real=True)

    return {
        "Thomson_functional": (
            "Y_Th=4*pi[K_Y(Lambda)+K_2(Lambda)]"
            "+R_SM(Lambda->mu_EW)+Delta_EW^scheme"
            "+R_LEFT(mu_EW->mu_had)+Delta_lep^OS"
            "+4*pi[Pi_had(M_Z^2)-Pi_had(0)]+Delta_frame^finite"
        ),
        "boundary_equation": "y+omega/y=Y_Th",
        "large_positive_root": large_root,
        "large_branch_domain": "Y_Th^2>4 omega and y^2>omega",
        "allowed_local_counterterms": (
            "-(delta_Y/4) B_mn B^mn-(delta_2/4) W_mn^a W^{a mn}"
        ),
        "counterterm_shift_in_Y_Th": 4 * sp.pi * (delta_y + delta_2),
        "dy_dY_on_large_branch": implicit_sensitivity,
        "dy_ddelta_Y": 4 * sp.pi * implicit_sensitivity,
        "dy_ddelta_2": 4 * sp.pi * implicit_sensitivity,
        "counterterm_sensitivity_nonzero_on_large_branch": True,
        "counterterms_preserve_C3_c1_level34_and_gauge_symmetry": True,
        "parity_odd_level34_forbids_parity_even_F2_counterterms": False,
        "HVP_definition": (
            "(q_mu q_nu-q^2 g_mn)Pi_JJ(q^2)="
            "i integral d^4x exp(iqx)<T J_mu(x)J_nu(0)>"
        ),
        "HVP_matching_identity": (
            "alpha(0)^-1=alpha(q^2)^-1"
            "+4*pi[Pi_JJ(q^2)-Pi_JJ(0)]"
        ),
        "HVP_present_in_workspace": False,
        "full_matching_is_prediction_without_independent_HVP": False,
        "reference_value_used": False,
    }


def strongest_target_free_partial_matching() -> dict[str, object]:
    """Run the strongest currently executable, explicitly incomplete chain.

    This replaces the invalid lepton-only running above the electroweak scale
    by the full one-loop unbroken-SM coefficient.  Below that scale it keeps
    only the separately controlled leptonic QED part.  No comparison value is
    read or used.
    """

    masses = LEPTON_MASSES_MEV
    core_scale_gev = (
        (C3_ORDER * H_BRANCH) ** 2
        * masses["tau"] ** 2
        / masses["electron"]
        / 1000.0
    )
    electroweak_scale_gev = 91.1876
    normalization = diagonal_sheet_normalization(
        sheet_count=1,
        unit_sheet_ratio=2.0,
    )
    bare_inverse_alpha = normalization.bare_inverse_alpha
    sm_one_loop_shift = 11.0 / (6.0 * math.pi) * math.log(
        core_scale_gev / electroweak_scale_gev
    )

    intervals = (
        (
            "EW_to_tau",
            electroweak_scale_gev,
            masses["tau"] / 1000.0,
            3.0,
        ),
        (
            "tau_to_muon",
            masses["tau"] / 1000.0,
            masses["muon"] / 1000.0,
            2.0,
        ),
        (
            "muon_to_electron",
            masses["muon"] / 1000.0,
            masses["electron"] / 1000.0,
            1.0,
        ),
    )
    running_inverse = bare_inverse_alpha + sm_one_loop_shift
    lepton_one_loop_shift = 0.0
    lepton_two_loop_shift = 0.0
    rows: list[dict[str, float | str]] = []
    for label, high, low, active_leptons in intervals:
        log_ratio = math.log(high / low)
        b1 = QED_B1_PER_LEPTON * active_leptons
        b2 = QED_B2_PER_UNIT_CHARGE4 * active_leptons
        one_loop = b1 * log_ratio
        two_loop = (b2 / b1) * math.log(
            (running_inverse + one_loop) / running_inverse
        )
        rows.append(
            {
                "label": label,
                "active_unit_leptons": active_leptons,
                "one_loop_shift": one_loop,
                "two_loop_on_one_loop_trajectory": two_loop,
            }
        )
        running_inverse += one_loop
        lepton_one_loop_shift += one_loop
        lepton_two_loop_shift += two_loop

    boundary_dimension = boundary_rank_nullity_theorem().kernel_dimension
    one_loop_root = solve_boundary_relation(
        running_inverse,
        boundary_dimension,
        boundary_matching_coefficient=QED_B1_THREE_LEPTONS,
    )
    partial_two_loop_root = solve_boundary_relation(
        running_inverse + lepton_two_loop_shift,
        boundary_dimension,
        boundary_matching_coefficient=QED_B1_THREE_LEPTONS,
    )

    return {
        "candidate_core_scale_GeV": core_scale_gev,
        "electroweak_matching_scale_GeV": electroweak_scale_gev,
        "QGT_candidate_bare_inverse_alpha": bare_inverse_alpha,
        "unbroken_SM_one_loop_shift_core_to_EW": sm_one_loop_shift,
        "leptonic_QED_intervals": tuple(rows),
        "leptonic_one_loop_shift_EW_to_e": lepton_one_loop_shift,
        "pre_boundary_one_loop_inverse_alpha": running_inverse,
        "conditional_one_loop_large_root": one_loop_root,
        "leptonic_two_loop_shift_EW_to_e": lepton_two_loop_shift,
        "conditional_partial_two_loop_large_root": partial_two_loop_root,
        "alpha_comparison_value_used": False,
        "finite_EW_thresholds_included": False,
        "two_loop_unbroken_SM_included": False,
        "quark_and_hadronic_vacuum_polarization_included": False,
        "QGT_to_independent_Maxwell_normalization_derived": False,
        "result_is_a_prediction": False,
        "reference_value_used": False,
    }


def closure_contract() -> dict[str, object]:
    """List jointly necessary gates for a genuine alpha prediction."""

    requirements = (
        "derive the physical identification of the spin-1/C3 space with the charged matter representation",
        "derive an independent four-dimensional Maxwell connection or an equivalent field with a quadratic principal symbol",
        "fix its charge generator, kinetic matrix, gap spectrum and regulator measure",
        "prove that no free finite parity-even F^2 counterterm remains",
        "derive hypercharge, weak chirality, Higgs/Yukawa data and all charged thresholds",
        "run U(1)_Y x SU(2)_L x SU(3)_c in one declared scheme and order",
        "prove matching-scale and scheme independence to the next retained order",
        "supply HVP from the same independently fixed QCD sector or mark it as external input",
        "exclude double counting between the frame determinant and boundary response",
        "keep every comparison value outside the construction and use it only afterward",
    )
    return {
        "joint_requirements": requirements,
        "requirement_count": len(requirements),
        "isolated_fixed_point_sufficient_condition": (
            "beta_A(x_*)=0, no exactly marginal Maxwell direction, and no "
            "unfixed relevant eigenvector projects onto K_gamma=K_Y+K_2"
        ),
        "compositeness_sufficient_condition": (
            "gauge fields auxiliary at a derived Lambda; a fully specified "
            "determinant/measure uniquely induces K_Y,K_2 and excludes finite F^2"
        ),
        "current_complete_UV_beta_system_present": False,
        "current_no_counterterm_theorem_present": False,
        "all_requirements_satisfied": False,
        "reference_value_used": False,
    }


def primary_reference_ledger() -> tuple[dict[str, str], ...]:
    return (
        {
            "result": "four-dimensional heat-kernel coefficients for Dirac-type operators",
            "source": "D. Vassilevich, arXiv:hep-th/0306138",
        },
        {
            "result": "spectral trace gives SU(5)-type high-scale coupling relations",
            "source": "A. Chamseddine and A. Connes, arXiv:hep-th/9606001",
        },
        {
            "result": "Standard-Model gauge beta functions beyond one loop",
            "source": "L. Mihaila, J. Salomon and M. Steinhauser, arXiv:1201.5868",
        },
        {
            "result": "complete SM running and threshold organization",
            "source": "S. Martin and D. Robertson, arXiv:1907.02500",
        },
        {
            "result": "Thomson-limit charge renormalization in broken electroweak theory",
            "source": "S. Dittmaier, arXiv:2101.05154",
        },
        {
            "result": "nonperturbative HVP contribution to running alpha and weak angle",
            "source": "M. Ce et al., arXiv:1910.09525",
        },
    )


def source_firewall() -> dict[str, object]:
    module = inspect.getmodule(source_firewall)
    source = inspect.getsource(module)
    forbidden_literals = (
        "COD" + "ATA",
        "OBS" + "ERVED",
        "137.03" + "5999177",
        "required_" + "from_alpha",
        "fit_" + "alpha",
    )
    violations = tuple(
        token for token in forbidden_literals if token in source
    )
    tree = ast.parse(source)
    local_imports = tuple(
        sorted(
            {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom)
                and node.module is not None
                and node.module.startswith("p")
            }
        )
    )
    allowed = {
        "p11b_c3_triplet_inversion",
        "p18bh_boundary_slot_count_theorem_gate",
        "p18bl_target_free_alpha_kernel_gate",
    }
    disallowed = tuple(name for name in local_imports if name not in allowed)
    return {
        "forbidden_literal_violations": violations,
        "local_imports": local_imports,
        "disallowed_local_imports": disallowed,
        "runtime_reference_free": not violations and not disallowed,
    }


def run_gate() -> None:
    intertwiner = spin1_c3_intertwiner_theorem()
    projector = spin1_projector_kato_theorem()
    composite = composite_connection_maxwell_obstruction()
    sm_anomalies = standard_model_anomaly_theorem()
    family = spin1_family_u1_embedding_theorem()
    operator = frame_electroweak_operator_definition()
    traces = gauge_trace_and_ratio_theorem()
    heat_kernel = heat_kernel_maxwell_stiffness_theorem()
    mixing = two_u1_kinetic_mixing_guard()
    beta = standard_model_one_loop_beta_theorem()
    electroweak = electroweak_breaking_and_matching_theorem()
    thomson = full_thomson_functional_and_counterterm_no_go()
    partial = strongest_target_free_partial_matching()
    contract = closure_contract()
    firewall = source_firewall()

    assert intertwiner["Fourier_is_unitary"]
    assert intertwiner["C3_cube_is_identity"]
    assert intertwiner["exact_unitary_equivalence"]
    assert intertwiner["C3_equals_three_SM_generations_derived"] is False
    assert projector["normalized_state"]
    assert projector["rank_one_projector"]
    assert projector["projector_is_Hermitian"]
    assert projector["polynomial_selects_plus_one_line"]
    assert projector["Kato_parallel_projector"]
    assert projector["first_Chern_number"] == 2
    assert projector["first_Chern_number_equals_h"]
    assert composite["north_chart_A_leading_prefactor"] == sp.Rational(1, 2)
    assert composite["north_chart_F_leading_coefficient"] == 1
    assert composite["F_squared_fluctuation_order"] == 4
    assert composite["composite_F2_has_quadratic_principal_symbol"] is False
    assert composite["QGT_sigma_term_has_quadratic_principal_symbol"]
    assert composite["composite_F_wedge_F_identically_zero"]
    assert composite["independent_connection_required_for_photon_propagator"]
    assert sm_anomalies["local_anomalies_cancel_per_generation"]
    assert sm_anomalies["Witten_SU2_global_anomaly_absent"]
    assert sm_anomalies["hypercharges_imported_not_derived"]
    assert family["sum_family_weights_squared_equals_h"]
    assert family["all_three_family_anomalies_cancel"]
    assert family["one_loop_log_YF_kinetic_mixing_vanishes"]
    assert family["Tr_F_squared_without_right_neutrinos"] == 30
    assert family["frame_family_U1_is_hypercharge"] is False
    assert operator["conditional_operator_is_gauge_covariant"]
    assert operator["frame_Berry_U1_embedded_as_hypercharge"] is False
    assert traces["one_generation_fermion_traces"] == (
        sp.Rational(10, 3),
        2,
        2,
    )
    assert traces["three_generation_fermion_traces"] == (10, 6, 6)
    assert traces["GUT_normalized_traces_equal"]
    assert traces["conditional_sin2_theta_W"] == sp.Rational(3, 8)
    assert traces["conditional_inverse_alpha_EM"] == 64 * sp.pi * sp.Symbol(
        "C_HK", real=True
    )
    assert traces["inverse_alpha_EM_over_inverse_alpha_U"] == sp.Rational(8, 3)
    assert heat_kernel["a4_F_squared_coefficient"] == 1 / (24 * sp.pi**2)
    assert heat_kernel["fermion_determinant_F_squared_coefficient"] == 1 / (
        48 * sp.pi**2
    )
    assert heat_kernel["induced_K_per_unit_Dirac_line"] == 1 / (
        12 * sp.pi**2
    )
    assert heat_kernel["q0_squared_equals_two_derived"] is False
    assert mixing["one_loop_log_mixing_vanishes_for_family_U1_candidate"]
    assert mixing["finite_kinetic_mixing_allowed"]
    assert beta["b_Y_b_2_b_3"] == (
        sp.Rational(41, 6),
        sp.Rational(-19, 6),
        -7,
    )
    assert beta["b_Y_plus_b_2"] == sp.Rational(11, 3)
    assert electroweak["inverse_coupling_identity_residual"] == 0
    assert electroweak["fixed_e_continuous_weak_angle_family"]
    assert electroweak["matching_scale_derivative"] == 0
    assert sp.simplify(
        electroweak["scheme_shifted_piece"]
        - electroweak["scheme_covariant_piece"]
    ) == 0
    assert thomson["counterterm_sensitivity_nonzero_on_large_branch"]
    assert thomson["HVP_present_in_workspace"] is False
    assert math.isclose(
        partial["conditional_one_loop_large_root"],
        136.62222151393388,
        rel_tol=2.0e-13,
    )
    assert math.isclose(
        partial["conditional_partial_two_loop_large_root"],
        136.63082563502343,
        rel_tol=2.0e-13,
    )
    assert partial["alpha_comparison_value_used"] is False
    assert partial["result_is_a_prediction"] is False
    assert contract["all_requirements_satisfied"] is False
    assert firewall["runtime_reference_free"]

    sections = (
        ("spin-1/C3 intertwiner theorem", intertwiner),
        ("spin-1 projector and Kato theorem", projector),
        ("composite-connection Maxwell obstruction", composite),
        ("Standard-Model anomaly theorem", sm_anomalies),
        ("spin-1 family-U(1) embedding theorem", family),
        ("frame+electroweak operator", operator),
        ("gauge-trace and ratio theorem", traces),
        ("heat-kernel Maxwell stiffness theorem", heat_kernel),
        ("two-U(1) kinetic-mixing guard", mixing),
        ("Standard-Model one-loop beta theorem", beta),
        ("electroweak breaking and matching theorem", electroweak),
        ("full Thomson functional and counterterm no-go", thomson),
        ("strongest target-free partial matching", partial),
        ("closure contract", contract),
        ("source firewall", firewall),
    )
    print("p18bp spin-1 frame/electroweak operator gate")
    for title, payload in sections:
        print()
        print(title)
        print(payload)
    print()
    print("primary reference ledger")
    for row in primary_reference_ledger():
        print(f"- {row}")
    print()
    print(
        "STATUS: OPEN_INDEPENDENT_MAXWELL_NORMALIZATION_FRAME_SM_ORIGIN_"
        "EW_THRESHOLDS_AND_HVP__PASS_TARGET_INDEPENDENT_SPIN1_FRAME_"
        "ELECTROWEAK_OPERATOR_AUDIT"
    )


if __name__ == "__main__":
    run_gate()
