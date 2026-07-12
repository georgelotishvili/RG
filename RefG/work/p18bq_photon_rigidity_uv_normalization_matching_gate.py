from __future__ import annotations

import ast
import inspect
import math

import mpmath as mp
import sympy as sp

from p11b_c3_triplet_inversion import LEPTON_MASSES_MEV
from p18bh_boundary_slot_count_theorem_gate import (
    boundary_rank_nullity_theorem,
)
from p18bl_target_free_alpha_kernel_gate import (
    C3_ORDER,
    H_BRANCH,
    QED_B1_THREE_LEPTONS,
    solve_boundary_relation,
)
from p18bp_spin1_frame_electroweak_operator_gate import (
    composite_connection_maxwell_obstruction,
    gauge_trace_and_ratio_theorem,
    spin1_family_u1_embedding_theorem,
    standard_model_anomaly_theorem,
    standard_model_one_loop_beta_theorem,
)


# Declared external matching inputs.  They are not used to select the
# operator, the C3 branch, or an electromagnetic comparison value.
MZ_GEV = 91.1876
MW_GEV = 80.379
MT_GEV = 173.1
KNT19_HVP_CURRENT_COEFFICIENT = 3.7834269002
KNT19_HVP_CURRENT_SIGMA = 0.0153480319


def neutral_generator_spectrum_rigidity_theorem() -> dict[str, object]:
    """Derive the unique generation-universal unbroken SM generator.

    Work in the unit-potential convention, so a candidate neutral generator is

        Q'=a T3+b Y+c F.

    The centered frame generator has family eigenvalues (-1,0,+1).  Requiring
    all three left-handed neutrinos to be neutral removes F, while primitive
    electron charge fixes the remaining common scale.  The same argument
    removes a projected-line charge P+=(0,0,1).
    """

    a, b, c = sp.symbols("a b c", real=True)
    centered_weights = (-sp.Integer(1), sp.Integer(0), sp.Integer(1))
    projected_weights = (sp.Integer(0), sp.Integer(0), sp.Integer(1))

    def solve_for_weights(weights: tuple[sp.Integer, ...]) -> tuple[object, object]:
        neutrino_charges = tuple(
            sp.simplify((a - b) / 2 + c * weight) for weight in weights
        )
        neutral_solutions = sp.linsolve(neutrino_charges, (a, b, c))
        electron_left_charge = sp.simplify(-a / 2 - b / 2 + c * weights[1])
        primitive_solutions = sp.solve(
            (*neutrino_charges, electron_left_charge + 1),
            (a, b, c),
            dict=True,
        )
        return neutral_solutions, tuple(primitive_solutions)

    centered_neutral, centered_primitive = solve_for_weights(centered_weights)
    projected_neutral, projected_primitive = solve_for_weights(projected_weights)

    return {
        "candidate_generator": "Q'=a T3+b Y+c F",
        "centered_frame_weights": centered_weights,
        "centered_neutrino_charges": tuple(
            sp.simplify((a - b) / 2 + c * weight)
            for weight in centered_weights
        ),
        "centered_neutral_solution": centered_neutral,
        "centered_primitive_solution": centered_primitive,
        "projected_line_weights": projected_weights,
        "projected_neutral_solution": projected_neutral,
        "projected_primitive_solution": projected_primitive,
        "unique_primitive_generator": "Q=T3+Y",
        "frame_component_in_physical_photon": 0,
        "generation_universal_charge_rigidity_proved": centered_primitive
        == ({a: 1, b: 1, c: 0},),
        "projected_line_removed_by_same_rigidity": projected_primitive
        == ({a: 1, b: 1, c: 0},),
        "hypercharges_are_imported_not_derived": True,
        "reference_value_used": False,
    }


def anomaly_pencil_and_projected_line_guard() -> dict[str, object]:
    """Show that anomalies do not select a centered F admixture.

    Every coefficient in the three-generation anomaly polynomial for Y+tF
    vanishes, so anomaly cancellation leaves a continuous pencil.  A P+ charge
    placed on the third SM family is instead anomalous without new spectators.
    """

    t = sp.symbols("t", real=True)
    sm = standard_model_anomaly_theorem()
    family = spin1_family_u1_embedding_theorem()
    per_family = family["per_family_anomaly_ledger"]
    third_family = per_family[-1]

    total_y2f = sp.simplify(sum(row["Y_squared_F"] for row in per_family))
    total_yf2 = sp.simplify(sum(row["Y_F_squared"] for row in per_family))
    total_f3 = sp.simplify(sum(row["F_cubed"] for row in per_family))
    total_grav_f = sp.simplify(sum(row["gravity_F"] for row in per_family))
    total_su2f = sp.simplify(sum(row["SU2_squared_F"] for row in per_family))
    total_su3f = sp.simplify(sum(row["SU3_squared_F"] for row in per_family))

    cubic_pencil = sp.expand(
        sm["U1Y_cubed"]
        + 3 * t * total_y2f
        + 3 * t**2 * total_yf2
        + t**3 * total_f3
    )
    gravity_pencil = sp.expand(sm["mixed_gravity_U1Y"] + t * total_grav_f)
    su2_pencil = sp.expand(sm["SU2_squared_U1Y"] + t * total_su2f)
    su3_pencil = sp.expand(sm["SU3_squared_U1Y"] + t * total_su3f)

    projected_anomalies = {
        "SU3_squared_P": third_family["SU3_squared_F"],
        "SU2_squared_P": third_family["SU2_squared_F"],
        "Y_squared_P": third_family["Y_squared_F"],
        "Y_P_squared": third_family["Y_F_squared"],
        "gravity_P": third_family["gravity_F"],
        "P_cubed": third_family["F_cubed"],
    }

    return {
        "Y_plus_tF_cubic_anomaly": cubic_pencil,
        "Y_plus_tF_gravity_anomaly": gravity_pencil,
        "Y_plus_tF_SU2_squared_anomaly": su2_pencil,
        "Y_plus_tF_SU3_squared_anomaly": su3_pencil,
        "centered_anomaly_pencil_flat_for_all_t": all(
            value == 0
            for value in (
                cubic_pencil,
                gravity_pencil,
                su2_pencil,
                su3_pencil,
            )
        ),
        "anomaly_cancellation_selects_t": False,
        "projected_line_third_family_anomalies": projected_anomalies,
        "projected_line_SM_embedding_anomalous_without_spectators": any(
            value != 0 for value in projected_anomalies.values()
        ),
        "separate_vectorlike_projected_Dirac_line_anomaly_free": True,
        "separate_vectorlike_line_is_SM_photon_embedding": False,
        "reference_value_used": False,
    }


def neutral_mass_matrix_rank_and_locking_theorem() -> dict[str, object]:
    """Derive all massless neutral directions with a Higgs and one link.

    In the basis (T3,Y,F), the neutral Higgs and link charge covectors are

        h=(-1/2,1/2,f_H),  s=(0,y_S,f_S).

    One Higgs leaves two U(1)s massless.  An independent link raises the mass
    rank to two.  Charge rigidity then forces its hypercharge to vanish if F
    acts on the SM family triplet, so the surviving photon contains no F.
    """

    f_h, y_s, f_s = sp.symbols("f_H y_S f_S", real=True)
    h = sp.Matrix([-sp.Rational(1, 2), sp.Rational(1, 2), f_h])
    s = sp.Matrix([0, y_s, f_s])
    twice_cross = sp.simplify(2 * h.cross(s))
    expected_cross = sp.Matrix([f_s - 2 * f_h * y_s, f_s, -y_s])
    r = sp.symbols("r", real=True)
    normalized_null = sp.Matrix([1 - 2 * f_h * r, 1, -r])

    # Substitute y_S=r f_S to verify the normalized null vector exactly.
    null_h = sp.simplify(h.dot(normalized_null))
    null_s = sp.simplify(s.dot(normalized_null).subs(y_s, r * f_s))

    return {
        "Higgs_charge_covector": h,
        "link_charge_covector": s,
        "mass_matrix": "M^2=v^2 h h^T+w^2 s s^T",
        "Higgs_only_rank": 1,
        "Higgs_only_nullity": 2,
        "independent_Higgs_and_link_rank": 2,
        "independent_Higgs_and_link_nullity": 1,
        "twice_null_cross_product": twice_cross,
        "cross_product_exact": twice_cross == expected_cross,
        "normalized_null_generator": normalized_null,
        "normalized_null_is_Higgs_neutral": null_h == 0,
        "normalized_null_is_link_neutral_for_r_yOverf": null_s == 0,
        "unbroken_generator": "Q_r=(1-2 f_H r)T3+Y-rF",
        "charge_rigidity_requires_r": 0,
        "physical_link_must_be_hypercharge_neutral": True,
        "physical_unbroken_generator": "Q=T3+Y",
        "invertible_kinetic_mixing_changes_mass_nullity": False,
        "reference_value_used": False,
    }


def photon_kinetic_projection_and_counterterm_theorem() -> dict[str, object]:
    """Project the most general neutral stiffness onto the massless mode."""

    K_2, K_y, K_f, chi, f_h, r = sp.symbols(
        "K_2 K_Y K_F chi f_H r", real=True
    )
    kinetic = sp.Matrix(
        [
            [K_2, 0, 0],
            [0, K_y, chi],
            [0, chi, K_f],
        ]
    )
    null = sp.Matrix([1 - 2 * f_h * r, 1, -r])
    projected = sp.expand((null.T * kinetic * null)[0])
    expected = sp.expand(
        K_2 * (1 - 2 * f_h * r) ** 2 + K_y - 2 * r * chi + r**2 * K_f
    )
    physical = sp.simplify(projected.subs(r, 0))

    delta_2, delta_y = sp.symbols("delta_2 delta_Y", real=True)
    inverse_alpha_shift = sp.simplify(4 * sp.pi * (delta_2 + delta_y))
    visible_schur = sp.simplify(K_y - chi**2 / K_f)

    return {
        "neutral_kinetic_matrix": kinetic,
        "positive_definite_conditions": (
            "K_2>0, K_Y>0, K_F>0, K_Y*K_F-chi^2>0"
        ),
        "general_massless_stiffness": projected,
        "projection_formula_exact": sp.simplify(projected - expected) == 0,
        "physical_charge_rigid_stiffness": physical,
        "physical_stiffness_equals_K2_plus_KY": physical == K_2 + K_y,
        "frame_stiffness_and_mixing_drop_from_physical_photon": True,
        "physical_inverse_alpha": 4 * sp.pi * physical,
        "two_massless_U1_visible_Schur_stiffness": visible_schur,
        "two_massless_U1_has_extra_long_range_mode": True,
        "allowed_counterterm_shift_inverse_alpha": inverse_alpha_shift,
        "counterterms_preserve_generator_anomalies_C3_c1_and_mass_rank": True,
        "counterterm_shift_nonzero_generically": inverse_alpha_shift != 0,
        "neutral_frame_link_can_transfer_stiffness_conditionally": True,
        "neutral_frame_link_free_inputs": (K_y, K_f, chi, r),
        "locking_predicts_absolute_normalization": False,
        "reference_value_used": False,
    }


def kato_photon_dichotomy() -> dict[str, object]:
    """Combine p18bp's composite obstruction with an independent-field branch."""

    composite = composite_connection_maxwell_obstruction()
    return {
        "composite_Berry_F2_has_quadratic_principal_symbol": composite[
            "composite_F2_has_quadratic_principal_symbol"
        ],
        "composite_Berry_spans_generic_Maxwell": composite[
            "generic_four_dimensional_Maxwell_sector_spanned"
        ],
        "composite_Berry_can_supply_photon_stiffness": False,
        "independent_connection_supplies_quadratic_Maxwell": True,
        "independent_connection_reintroduces_K_F": True,
        "projected_line_as_SM_charge_is_anomalous_or_nonuniversal": True,
        "current_Kato_or_F_operator_closes_photon_normalization": False,
        "reference_value_used": False,
    }


def auxiliary_link_compositeness_route() -> dict[str, object]:
    """Record the finite auxiliary-link route and its representation gap.

    The centered (-1,0,+1) values are spin-one/family weights.  They define a
    useful compact-link toy ledger, but the charge-rigidity theorem above
    proves that they are not physical electromagnetic charges.  A physical
    determinant must instead use the complete generation-blind Q=T3+Y
    representation.  p18br audits whether a no-bare-plaquette link can arise
    from an exact CP1/Hubbard--Stratonovich rewrite.
    """

    frame_weights = (-1, 0, 1)
    primitive_gcd = math.gcd(*(abs(weight) for weight in frame_weights))
    weight_square_sum = sum(weight**2 for weight in frame_weights)
    lambda_x, lambda_y, charge = sp.symbols(
        "lambda_x lambda_y q", real=True
    )
    hopping_phase = sp.simplify(
        -charge * lambda_x
        + charge * (lambda_x - lambda_y)
        + charge * lambda_y
    )

    return {
        "compact_link": "U_xy=exp(i a_xy), a_xy equivalent modulo 2*pi",
        "microscopic_action": (
            "S_micro=sum_x Phi_x^dag M Phi_x"
            "-sum_<xy>,a t_a[Phi_ax^dag U_xy^(q_a) Phi_ay+h.c.]"
            "+S_frame+S_lock"
        ),
        "gauge_transformation": (
            "Phi_ax->exp(i q_a lambda_x)Phi_ax; "
            "U_xy->exp(i(lambda_x-lambda_y))U_xy"
        ),
        "hopping_phase_residual": hopping_phase,
        "hopping_is_exactly_gauge_invariant": hopping_phase == 0,
        "centered_C3_frame_weights": frame_weights,
        # Backward-compatible key retained for the historical assertion
        # below.  It must not be interpreted as the physical Q charge set.
        "centered_C3_charge_lattice": frame_weights,
        "primitive_charge_gcd": primitive_gcd,
        "primitive_frame_weight_normalization_fixed": primitive_gcd == 1,
        "primitive_charge_normalization_fixed": primitive_gcd == 1,
        "sum_centered_weights_squared": weight_square_sum,
        "sum_centered_charges_squared": weight_square_sum,
        "sum_charges_squared_equals_h": weight_square_sum == H_BRANCH,
        "centered_weights_are_physical_photon_charges": False,
        "auxiliary_link_is_physical_Q_connection": False,
        "physical_photon_generator_required": "Q=T3+Y",
        "complete_physical_Q_charged_spectrum_present": False,
        "bare_plaquette_term": 0,
        "no_bare_plaquette_is_imposed_microscopic_condition": True,
        "gauge_symmetry_forbids_bare_plaquette": False,
        "induced_effective_action": (
            "exp[-Gamma(U)]=integral D Phi exp[-S_micro(Phi,U)]"
        ),
        "polarization_definition": (
            "Pi_mn^AB=delta^2 Gamma/(delta a_A^m delta a_B^n)|_0"
        ),
        "stiffness_projection": (
            "K_AB=lim_(p2->0) P_T^mn Pi_mn^AB/(3 p^2)"
        ),
        "complete_gapped_spectrum_present_in_current_action": False,
        "microscopic_hopping_and_gap_values_derived": False,
        "regulator_refinement_limit_derived": False,
        "determinant_boundary_double_count_excluded": False,
        "route_is_complete_prediction": False,
        "superseding_origin_and_phase_audit": (
            "p18br_hs_auxiliary_link_origin_gate.py"
        ),
        "reference_value_used": False,
    }


def compositeness_sign_and_gap_theorem() -> dict[str, object]:
    """Test the naive continuum K(Lambda)=0 flow against SM beta signs.

    This sign test applies to extrapolating the already-dynamical continuum SM
    RGE from a zero-stiffness boundary.  It is not a no-go against the separate
    finite auxiliary-link determinant, where the gauge field is microscopic
    and non-propagating before matter is integrated out.
    """

    beta = standard_model_one_loop_beta_theorem()
    b_y, b_2, b_3 = beta["b_Y_b_2_b_3"]
    log_ratio = sp.symbols("L", positive=True)
    induced = tuple(
        sp.simplify(coefficient * log_ratio / (8 * sp.pi**2))
        for coefficient in (b_y, b_2, b_3)
    )

    # Proper-time E1 requirements from the p18bp heat-kernel normalization.
    # One unit Dirac line requires I_R=6*pi^2 for q0^2=2.  The centered
    # (-1,0,+1) pair has sum(q^2)=2 and therefore requires I_R=3*pi^2.
    def proper_time_ratio(required_moment: mp.mpf) -> tuple[float, float]:
        initial = -(required_moment + mp.euler)
        log_x = mp.findroot(
            lambda value: mp.e1(mp.e**value) - required_moment,
            initial,
        )
        x = mp.e**log_x
        return float(x), float(1 / mp.sqrt(x))

    one_line_x, one_line_ratio = proper_time_ratio(6 * mp.pi**2)
    c3_pair_x, c3_pair_ratio = proper_time_ratio(3 * mp.pi**2)

    masses = LEPTON_MASSES_MEV
    core_scale_mev = (
        (C3_ORDER * H_BRANCH) ** 2
        * masses["tau"] ** 2
        / masses["electron"]
    )
    core_to_electron = core_scale_mev / masses["electron"]
    core_electron_x = (masses["electron"] / core_scale_mev) ** 2
    core_electron_moment = float(mp.e1(core_electron_x))
    c3_pair_q0_squared = float(
        6 * mp.pi**2 / core_electron_moment
    )

    return {
        "naive_continuum_compositeness_boundary": "K_i(Lambda)=0",
        "one_loop_induced_stiffnesses_at_lower_scale": induced,
        "SM_beta_coefficients": (b_y, b_2, b_3),
        "U1Y_induced_stiffness_positive": bool(b_y > 0),
        "SU2_induced_stiffness_positive": bool(b_2 > 0),
        "SU3_induced_stiffness_positive": bool(b_3 > 0),
        "naive_continuum_SM_zero_boundary_positive": all(
            coefficient > 0 for coefficient in (b_y, b_2, b_3)
        ),
        "one_Dirac_line_required_I_R_for_q0sq2": 6 * sp.pi**2,
        "one_Dirac_line_required_x_M2OverLambda2": one_line_x,
        "one_Dirac_line_required_Lambda_over_M": one_line_ratio,
        "centered_C3_pair_required_I_R_for_q0sq2": 3 * sp.pi**2,
        "centered_C3_pair_required_x_M2OverLambda2": c3_pair_x,
        "centered_C3_pair_required_Lambda_over_M": c3_pair_ratio,
        "candidate_core_over_electron_ratio": core_to_electron,
        "candidate_core_electron_I_R": core_electron_moment,
        "centered_pair_q0_squared_if_gap_is_electron": c3_pair_q0_squared,
        "electron_is_derived_frame_gap": False,
        "gap_requirement_is_prediction_without_mass_theorem": False,
        "naive_continuum_EW_zero_boundary_needs_new_UV_content_or_flow": True,
        "finite_auxiliary_link_determinant_ruled_out_by_this_sign_test": False,
        "reference_value_used": False,
    }


def minimal_vectorlike_sign_repair_audit() -> dict[str, object]:
    """Find the smallest simple vectorlike matter additions that flip signs.

    This is a diagnostic, not a proposed particle spectrum.  A Dirac weak
    triplet contributes (4/3)T(3)=8/3 to b2; a Dirac color adjoint contributes
    (4/3)T(8)=4 to b3.
    """

    b2_base = sp.Rational(-19, 6)
    b3_base = sp.Integer(-7)

    weak_triplets = next(
        count
        for count in range(1, 20)
        if b2_base + count * sp.Rational(8, 3) > 0
    )
    color_adjoints = next(
        count
        for count in range(1, 20)
        if b3_base + count * 4 > 0
    )
    repaired_b2 = sp.simplify(
        b2_base + weak_triplets * sp.Rational(8, 3)
    )
    repaired_b3 = sp.simplify(b3_base + color_adjoints * 4)

    core_scale = (
        (C3_ORDER * H_BRANCH) ** 2
        * LEPTON_MASSES_MEV["tau"] ** 2
        / LEPTON_MASSES_MEV["electron"]
        / 1000.0
    )
    log_core_to_mz = math.log(core_scale / MZ_GEV)
    b_y = sp.Rational(41, 6)
    induced_inverse_alpha_mz = float(
        (b_y + repaired_b2) / (2 * sp.pi) * log_core_to_mz
    )

    return {
        "minimal_Dirac_weak_triplets_for_positive_b2": weak_triplets,
        "minimal_Dirac_color_adjoints_for_positive_b3": color_adjoints,
        "repaired_b2": repaired_b2,
        "repaired_b3": repaired_b3,
        "minimal_counts_equal_h_numerically": weak_triplets
        == color_adjoints
        == H_BRANCH,
        "h_is_vectorlike_matter_multiplicity_derived": False,
        "new_vectorlike_matter_present_in_current_action": False,
        "pure_induced_inverse_alpha_at_MZ_for_repaired_EW_sign": induced_inverse_alpha_mz,
        "pure_induced_branch_matches_existing_QGT_bare_normalization": False,
        "sign_repair_closes_absolute_stiffness": False,
        "reference_value_used": False,
    }


def spectral_topology_and_duality_route_audit() -> dict[str, object]:
    """Reject three routes that cannot fix the parity-even coefficient."""

    traces = gauge_trace_and_ratio_theorem()
    hidden_level = boundary_rank_nullity_theorem().kernel_dimension

    S = sp.Matrix([[0, -1], [1, 0]])
    T_level = sp.Matrix([[1, hidden_level], [0, 1]])
    modular = S * T_level
    modular_trace = sp.trace(modular)
    modular_discriminant = sp.simplify(modular_trace**2 - 4)
    tau = sp.symbols("tau")
    fixed_polynomial = sp.expand(tau**2 + hidden_level * tau + 1)
    fixed_roots = sp.solve(sp.Eq(fixed_polynomial, 0), tau)

    q_geom_squared = sp.Rational(H_BRANCH, 9) ** 2
    q0_squared_candidate = sp.Integer(H_BRANCH)
    self_dual_inverse_alpha = sp.simplify(
        1 / (q0_squared_candidate * q_geom_squared)
    )

    return {
        "spectral_common_trace_inverse_alpha": traces[
            "conditional_inverse_alpha_EM"
        ],
        "spectral_trace_fixes_ratios": True,
        "spectral_common_moment_fixed_by_operator": False,
        "spectral_rescaling_preserves_all_ratios": True,
        "topology_quantizes": ("c1 flux", "theta periodicity", "CS level"),
        "topology_quantizes_parity_even_F2_stiffness": False,
        "allowed_delta_K_preserves_topology": True,
        "S_duality_matrix": S,
        "S_self_dual_upper_half_fixed_point": sp.I,
        "S_self_dual_normalized_g_squared": 4 * sp.pi,
        "conditional_self_dual_inverse_alpha_with_q0_hOver9": self_dual_inverse_alpha,
        "exact_S_duality_present_in_current_matter_spectrum": False,
        "level34_ST_matrix": modular,
        "level34_ST_trace": modular_trace,
        "level34_ST_discriminant": modular_discriminant,
        "level34_ST_fixed_polynomial": fixed_polynomial,
        "level34_ST_fixed_roots": tuple(fixed_roots),
        "level34_ST_is_hyperbolic": abs(int(modular_trace)) > 2,
        "level34_ST_has_upper_half_plane_fixed_point": False,
        "duality_or_level34_closes_stiffness": False,
        "reference_value_used": False,
    }


def isolated_uv_fixed_point_criterion() -> dict[str, object]:
    """State the only continuum mechanism that removes a coupling fibre."""

    g_y, f_g = sp.symbols("g_Y f_g", positive=True)
    b_y = sp.Rational(41, 6)
    beta_y = sp.factor(-f_g * g_y + b_y * g_y**3 / (16 * sp.pi**2))
    nonzero_fixed_squared = sp.simplify(16 * sp.pi**2 * f_g / b_y)

    g_2, f_2 = sp.symbols("g_2 f_2", positive=True)
    b_2 = sp.Rational(-19, 6)
    beta_2 = sp.factor(-f_2 * g_2 + b_2 * g_2**3 / (16 * sp.pi**2))
    nonzero_weak_squared = sp.simplify(16 * sp.pi**2 * f_2 / b_2)

    return {
        "gravity_dressed_Abelian_beta": beta_y,
        "Abelian_nonzero_fixed_g_squared": nonzero_fixed_squared,
        "Abelian_fixed_point_positive_if_f_g_positive": bool(
            nonzero_fixed_squared > 0
        ),
        "gravity_dressed_weak_beta": beta_2,
        "weak_nonzero_fixed_g_squared_in_same_sign_truncation": nonzero_weak_squared,
        "weak_nonzero_fixed_point_positive_if_f_2_positive": bool(
            nonzero_weak_squared > 0
        ),
        "one_loop_SM_without_gravity_has_nonzero_Abelian_fixed_point": False,
        "isolated_full_system_fixed_point_sufficient_condition": (
            "beta_A(x_*)=0 and every free relevant or marginal eigenvector "
            "v_I obeys grad(K_gamma).v_I=0"
        ),
        "current_RefG_quantum_gravity_gauge_beta_system_present": False,
        "current_operator_has_isolated_full_product_fixed_point": False,
        "fixed_point_route_is_current_prediction": False,
        "reference_value_used": False,
    }


def common_trace_one_loop_running_to_mz() -> dict[str, object]:
    """Run the conditional common-trace branch through the unbroken SM."""

    inverse_alpha_star_exact = sp.Rational(81, 2) * sp.pi
    inverse_alpha_star = float(inverse_alpha_star_exact)
    core_scale_gev = (
        (C3_ORDER * H_BRANCH) ** 2
        * LEPTON_MASSES_MEV["tau"] ** 2
        / LEPTON_MASSES_MEV["electron"]
        / 1000.0
    )
    log_ratio = math.log(core_scale_gev / MZ_GEV)

    A_y = (
        5.0 * inverse_alpha_star / 8.0
        + 41.0 / (12.0 * math.pi) * log_ratio
    )
    A_2 = (
        3.0 * inverse_alpha_star / 8.0
        - 19.0 / (12.0 * math.pi) * log_ratio
    )
    A_3 = (
        3.0 * inverse_alpha_star / 8.0
        - 7.0 / (2.0 * math.pi) * log_ratio
    )
    inverse_alpha_mz = A_y + A_2

    return {
        "conditional_boundary_inverse_alpha_exact": inverse_alpha_star_exact,
        "conditional_boundary_inverse_alpha": inverse_alpha_star,
        "candidate_core_scale_GeV": core_scale_gev,
        "MZ_GeV": MZ_GEV,
        "log_core_over_MZ": log_ratio,
        "A_Y_4pi_over_gY2_at_MZ": A_y,
        "A_2_4pi_over_g2sq_at_MZ": A_2,
        "A_3_4pi_over_g3sq_at_MZ": A_3,
        "MSbar_inverse_alpha_at_MZ": inverse_alpha_mz,
        "MSbar_sin2_theta_W_at_MZ": A_2 / inverse_alpha_mz,
        "conditional_alpha_s_at_MZ": 1.0 / A_3,
        "running_order": 1,
        "comparison_value_used": False,
        "reference_value_used": False,
    }


def one_loop_thomson_matching(
    hadronic_current_coefficient: float = 0.0,
    hadronic_current_sigma: float = 0.0,
) -> dict[str, object]:
    """Match the conditional MSbar branch to the Thomson limit.

    The perturbative one-loop term contains W, top and the three charged
    leptons.  Five-light-quark HVP is a separate current-correlator input.  It
    is zero by default, keeping the construction internally target-free.
    """

    if hadronic_current_coefficient < 0.0 or hadronic_current_sigma < 0.0:
        raise ValueError("HVP coefficient and uncertainty must be non-negative")

    running = common_trace_one_loop_running_to_mz()
    lepton_masses_gev = tuple(
        LEPTON_MASSES_MEV[name] / 1000.0
        for name in ("electron", "muon", "tau")
    )
    perturbative_numerator = (
        202.0 / 27.0
        + 14.0 * math.log(MW_GEV / MZ_GEV)
        - 32.0 / 9.0 * math.log(MT_GEV / MZ_GEV)
        - 8.0
        / 3.0
        * sum(math.log(mass / MZ_GEV) for mass in lepton_masses_gev)
    )
    perturbative_threshold = perturbative_numerator / (4.0 * math.pi)
    pre_boundary = (
        running["MSbar_inverse_alpha_at_MZ"]
        + perturbative_threshold
        + hadronic_current_coefficient
    )
    hidden_dimension = boundary_rank_nullity_theorem().kernel_dimension
    root = solve_boundary_relation(
        pre_boundary,
        hidden_dimension,
        boundary_matching_coefficient=QED_B1_THREE_LEPTONS,
    )
    lower_pre_boundary = pre_boundary - hadronic_current_sigma
    upper_pre_boundary = pre_boundary + hadronic_current_sigma
    lower_root = solve_boundary_relation(
        lower_pre_boundary,
        hidden_dimension,
        boundary_matching_coefficient=QED_B1_THREE_LEPTONS,
    )
    upper_root = solve_boundary_relation(
        upper_pre_boundary,
        hidden_dimension,
        boundary_matching_coefficient=QED_B1_THREE_LEPTONS,
    )

    return {
        "running": running,
        "MW_GeV_external": MW_GEV,
        "Mt_GeV_external": MT_GEV,
        "lepton_masses_GeV": lepton_masses_gev,
        "one_loop_threshold_numerator": perturbative_numerator,
        "one_loop_perturbative_Thomson_threshold": perturbative_threshold,
        "five_light_quark_HVP_current_coefficient": hadronic_current_coefficient,
        "five_light_quark_HVP_current_sigma": hadronic_current_sigma,
        "pre_boundary_Thomson_inverse_alpha": pre_boundary,
        "conditional_boundary_large_root": root,
        "HVP_only_root_interval": (lower_root, upper_root),
        "HVP_is_external_nonperturbative_input": hadronic_current_coefficient > 0.0,
        "HVP_external_normalization_is_self_contained_RefG_prediction": False,
        "MW_Mt_and_lepton_masses_are_imported_inputs": True,
        "Higgs_Yukawa_VEV_and_threshold_spectrum_derived_by_RefG": False,
        "full_two_loop_SM_and_thresholds_included": False,
        "conditional_branch_own_QCD_HVP_computed": False,
        "result_is_full_prediction": False,
        "comparison_value_used": False,
        "reference_value_used": False,
    }


def external_knt19_hvp_ledger() -> dict[str, object]:
    """Evaluate a declared external HVP correlator input, not a RefG output."""

    result = one_loop_thomson_matching(
        hadronic_current_coefficient=KNT19_HVP_CURRENT_COEFFICIENT,
        hadronic_current_sigma=KNT19_HVP_CURRENT_SIGMA,
    )
    return {
        "source": "Keshavarzi-Nomura-Teubner, arXiv:1911.00367",
        "published_Delta_alpha_had5": 276.09e-4,
        "published_Delta_alpha_had5_sigma": 1.12e-4,
        "current_correlator_coefficient": KNT19_HVP_CURRENT_COEFFICIENT,
        "current_correlator_sigma": KNT19_HVP_CURRENT_SIGMA,
        "conversion_uses_external_electromagnetic_normalization": True,
        "conditional_matching": result,
        "input_is_independent_RefG_QCD_calculation": False,
        "result_is_self_contained_prediction": False,
        "comparison_value_used": False,
        "reference_value_used_in_input_provenance": True,
        "direct_alpha_comparison_used": False,
    }


def comparison_only_required_finite_stiffness(
    construction_pre_boundary: float,
    required_inverse_alpha: float,
) -> dict[str, float]:
    """Post-construction diagnostic; never called by the target-free gate."""

    if construction_pre_boundary <= 0.0 or required_inverse_alpha <= 0.0:
        raise ValueError("inverse couplings must be positive")
    hidden_dimension = boundary_rank_nullity_theorem().kernel_dimension
    omega = QED_B1_THREE_LEPTONS / hidden_dimension
    required_pre_boundary = (
        required_inverse_alpha + omega / required_inverse_alpha
    )
    delta_y = required_pre_boundary - construction_pre_boundary
    return {
        "required_pre_boundary": required_pre_boundary,
        "delta_inverse_alpha_functional": delta_y,
        "delta_K_gamma_finite": delta_y / (4.0 * math.pi),
    }


def route_selection_and_closure_contract() -> dict[str, object]:
    requirements = (
        "derive the generation-blind physical Q=T3+Y representation on the complete Hilbert space",
        "derive a finite microscopic auxiliary-link action with no independent bare plaquette parameter, as audited next in p18br",
        "derive every charged gap, hopping coefficient and multiplicity",
        "derive a deconfined massless Coulomb phase rather than the current ordered Higgs branch",
        "prove the polarization Ward identity and a positive symmetric stiffness matrix",
        "prove regulator/refinement convergence and exclude a free finite F^2 counterterm",
        "derive the Higgs/link mass matrix while preserving Q=T3+Y",
        "derive QCD/HVP from the same gauge and quark sector",
        "include full declared-order RG and threshold matching in one scheme",
        "exclude determinant/boundary-response double counting",
        "keep electromagnetic comparison data outside the construction",
    )
    return {
        "selected_finite_route": (
            "conditional exact-origin auxiliary link plus complete physical-Q "
            "finite determinant; action-origin and phase audit deferred to p18br"
        ),
        "continuum_sufficient_route": (
            "isolated full UV fixed point with no free relevant or marginal "
            "direction projecting onto K_gamma"
        ),
        "joint_requirements": requirements,
        "requirement_count": len(requirements),
        "current_requirements_satisfied": False,
        "topology_duality_or_spectral_ratio_selected_as_absolute_route": False,
        "current_alpha_closed": False,
        "reference_value_used": False,
    }


def primary_reference_ledger() -> tuple[dict[str, str], ...]:
    return (
        {
            "result": "compositeness condition for induced gauge bosons",
            "source": "K. Akama and T. Hattori, arXiv:hep-ph/9607331",
        },
        {
            "result": "four-dimensional Abelian S-duality",
            "source": "E. Witten, arXiv:hep-th/9505186",
        },
        {
            "result": "spectral-action high-scale coupling relations",
            "source": "A. Chamseddine and A. Connes, arXiv:hep-th/9606001",
        },
        {
            "result": "Standard-Model gauge beta functions",
            "source": "L. Mihaila et al., arXiv:1201.5868",
        },
        {
            "result": "SMbar-to-Thomson matching and HVP input structure",
            "source": "S. Martin and D. Robertson, arXiv:1907.02500",
        },
        {
            "result": "Thomson-limit charge renormalization",
            "source": "S. Dittmaier, arXiv:2101.05154",
        },
        {
            "result": "five-flavor hadronic vacuum polarization input",
            "source": "A. Keshavarzi et al., arXiv:1911.00367",
        },
        {
            "result": "gravity-induced interacting Abelian fixed-point route",
            "source": "A. Eichhorn and A. Held, arXiv:1803.04027",
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
        "p18bp_spin1_frame_electroweak_operator_gate",
    }
    disallowed = tuple(name for name in local_imports if name not in allowed)
    comparison_called = "comparison_only_required_finite_stiffness(" in inspect.getsource(
        run_gate
    )
    return {
        "forbidden_literal_violations": violations,
        "local_imports": local_imports,
        "disallowed_local_imports": disallowed,
        "comparison_function_called_by_gate": comparison_called,
        "runtime_direct_alpha_target_free": not violations
        and not disallowed
        and not comparison_called,
    }


def run_gate() -> None:
    rigidity = neutral_generator_spectrum_rigidity_theorem()
    anomalies = anomaly_pencil_and_projected_line_guard()
    mass_rank = neutral_mass_matrix_rank_and_locking_theorem()
    projection = photon_kinetic_projection_and_counterterm_theorem()
    kato = kato_photon_dichotomy()
    auxiliary = auxiliary_link_compositeness_route()
    compositeness = compositeness_sign_and_gap_theorem()
    sign_repair = minimal_vectorlike_sign_repair_audit()
    other_routes = spectral_topology_and_duality_route_audit()
    fixed_point = isolated_uv_fixed_point_criterion()
    running = common_trace_one_loop_running_to_mz()
    perturbative_matching = one_loop_thomson_matching()
    external_hvp = external_knt19_hvp_ledger()
    selection = route_selection_and_closure_contract()
    firewall = source_firewall()

    assert rigidity["generation_universal_charge_rigidity_proved"]
    assert rigidity["projected_line_removed_by_same_rigidity"]
    assert rigidity["frame_component_in_physical_photon"] == 0
    assert anomalies["centered_anomaly_pencil_flat_for_all_t"]
    assert anomalies["anomaly_cancellation_selects_t"] is False
    assert anomalies["projected_line_SM_embedding_anomalous_without_spectators"]
    assert mass_rank["cross_product_exact"]
    assert mass_rank["normalized_null_is_Higgs_neutral"]
    assert mass_rank["normalized_null_is_link_neutral_for_r_yOverf"]
    assert mass_rank["charge_rigidity_requires_r"] == 0
    assert projection["projection_formula_exact"]
    assert projection["physical_stiffness_equals_K2_plus_KY"]
    assert projection["frame_stiffness_and_mixing_drop_from_physical_photon"]
    assert projection["locking_predicts_absolute_normalization"] is False
    assert kato["composite_Berry_F2_has_quadratic_principal_symbol"] is False
    assert kato["composite_Berry_spans_generic_Maxwell"] is False
    assert kato["current_Kato_or_F_operator_closes_photon_normalization"] is False
    assert auxiliary["hopping_is_exactly_gauge_invariant"]
    assert auxiliary["primitive_charge_gcd"] == 1
    assert auxiliary["sum_charges_squared_equals_h"]
    assert auxiliary["centered_weights_are_physical_photon_charges"] is False
    assert auxiliary["auxiliary_link_is_physical_Q_connection"] is False
    assert auxiliary["complete_physical_Q_charged_spectrum_present"] is False
    assert auxiliary["gauge_symmetry_forbids_bare_plaquette"] is False
    assert auxiliary["route_is_complete_prediction"] is False
    assert compositeness["SM_beta_coefficients"] == (
        sp.Rational(41, 6),
        sp.Rational(-19, 6),
        -7,
    )
    assert compositeness["U1Y_induced_stiffness_positive"]
    assert compositeness["SU2_induced_stiffness_positive"] is False
    assert compositeness["SU3_induced_stiffness_positive"] is False
    assert compositeness["naive_continuum_SM_zero_boundary_positive"] is False
    assert compositeness[
        "finite_auxiliary_link_determinant_ruled_out_by_this_sign_test"
    ] is False
    assert math.isclose(
        compositeness["one_Dirac_line_required_Lambda_over_M"],
        9.644616844868e12,
        rel_tol=2.0e-13,
    )
    assert math.isclose(
        compositeness["centered_C3_pair_required_Lambda_over_M"],
        3.587673262621e6,
        rel_tol=2.0e-13,
    )
    assert sign_repair["minimal_Dirac_weak_triplets_for_positive_b2"] == 2
    assert sign_repair["minimal_Dirac_color_adjoints_for_positive_b3"] == 2
    assert sign_repair["h_is_vectorlike_matter_multiplicity_derived"] is False
    assert other_routes["spectral_trace_fixes_ratios"]
    assert other_routes["spectral_common_moment_fixed_by_operator"] is False
    assert other_routes["topology_quantizes_parity_even_F2_stiffness"] is False
    assert other_routes["level34_ST_trace"] == 34
    assert other_routes["level34_ST_is_hyperbolic"]
    assert other_routes["level34_ST_has_upper_half_plane_fixed_point"] is False
    assert fixed_point["one_loop_SM_without_gravity_has_nonzero_Abelian_fixed_point"] is False
    assert fixed_point["current_RefG_quantum_gravity_gauge_beta_system_present"] is False
    assert math.isclose(
        running["MSbar_inverse_alpha_at_MZ"],
        131.7860521831133,
        rel_tol=2.0e-13,
    )
    assert math.isclose(
        running["MSbar_sin2_theta_W_at_MZ"],
        0.3322207005848506,
        rel_tol=2.0e-13,
    )
    assert math.isclose(
        running["conditional_alpha_s_at_MZ"],
        0.025625508247526962,
        rel_tol=2.0e-13,
    )
    assert math.isclose(
        perturbative_matching["conditional_boundary_large_root"],
        136.89566769246392,
        rel_tol=2.0e-13,
    )
    hvp_matching = external_hvp["conditional_matching"]
    assert math.isclose(
        hvp_matching["conditional_boundary_large_root"],
        140.67909827113797,
        rel_tol=2.0e-13,
    )
    assert external_hvp["result_is_self_contained_prediction"] is False
    assert selection["current_alpha_closed"] is False
    assert firewall["runtime_direct_alpha_target_free"]

    sections = (
        ("neutral-generator spectrum rigidity theorem", rigidity),
        ("anomaly pencil and projected-line guard", anomalies),
        ("neutral mass-matrix rank and locking theorem", mass_rank),
        ("photon kinetic projection and counterterm theorem", projection),
        ("Kato photon dichotomy", kato),
        ("auxiliary-link compositeness route", auxiliary),
        ("compositeness sign and gap theorem", compositeness),
        ("minimal vectorlike sign-repair audit", sign_repair),
        ("spectral/topology/duality route audit", other_routes),
        ("isolated UV fixed-point criterion", fixed_point),
        ("conditional common-trace running to MZ", running),
        ("one-loop perturbative Thomson matching", perturbative_matching),
        ("external KNT19 HVP ledger", external_hvp),
        ("route selection and closure contract", selection),
        ("source firewall", firewall),
    )
    print("p18bq photon-rigidity/UV-normalization/full-matching gate")
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
        "STATUS: OPEN_AUXILIARY_LINK_ACTION_COMPLETE_SPECTRUM_FINITE_"
        "STIFFNESS_AND_SELF_CONTAINED_HVP__PASS_PHOTON_RIGIDITY_TARGET_"
        "ISOLATED_UV_ROUTE_AND_FULL_ONE_LOOP_CONDITIONAL_MATCHING_AUDIT"
    )


if __name__ == "__main__":
    run_gate()
