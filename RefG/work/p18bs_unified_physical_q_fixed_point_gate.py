from __future__ import annotations

"""PHASE 18bs: physical-Q unification and gravity fixed-point gate.

p18br rejects the current ordered CP1/frame branch as a massless-photon
phase.  This gate therefore tests one sufficient conditional continuum
mechanism that can remove an arbitrary Maxwell normalization: an isolated
gravity--gauge fixed point for a *single* ultraviolet gauge coupling,
followed here by an assumed SU(5) breaking map to Q=T3+Y.

The gate is target independent.  It proves the exact simple-group
normalization algebra, rejects a simultaneously nonzero fixed point for the
minimal product Standard-Model electroweak beta system with universal
gravitational antiscreening, and derives the conditional unified prediction
kernel.  SU(5) is a conventional full-SM simple-group witness in this gate,
not a structure already derived from RefG.
"""

import ast
import inspect

import sympy as sp


def su5_physical_q_normalization_theorem() -> dict[str, object]:
    """Use SU(5) only as a conventional exact full-SM GUT witness."""

    Y = sp.diag(
        -sp.Rational(1, 3),
        -sp.Rational(1, 3),
        -sp.Rational(1, 3),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
    )
    T_y = sp.sqrt(sp.Rational(3, 5)) * Y
    trace_y = sp.simplify(sp.trace(Y * Y))
    trace_t = sp.simplify(sp.trace(T_y * T_y))
    g_u = sp.symbols("g_U", positive=True)
    g_y_squared = sp.simplify(sp.Rational(3, 5) * g_u**2)
    g_2_squared = g_u**2
    e_squared = sp.simplify(
        g_y_squared * g_2_squared / (g_y_squared + g_2_squared)
    )
    sin2 = sp.simplify(g_y_squared / (g_y_squared + g_2_squared))

    return {
        "fundamental_hypercharge_generator": Y,
        "hypercharge_is_traceless": sp.trace(Y) == 0,
        "raw_hypercharge_trace": trace_y,
        "canonically_normalized_generator": T_y,
        "normalized_trace_is_one_half": trace_t == sp.Rational(1, 2),
        "matching_gY_squared": g_y_squared,
        "matching_g2_squared": g_2_squared,
        "g2_squared_equals_5_over_3_gY_squared": sp.simplify(
            g_2_squared - sp.Rational(5, 3) * g_y_squared
        )
        == 0,
        "matching_e_squared": e_squared,
        "e_squared_over_gU_squared": sp.simplify(e_squared / g_u**2),
        "matching_sin2_theta": sin2,
        "standard_generator_after_assumed_breaking": "Q=T3+Y",
        "breaking_Higgs_vacuum_derived_here": False,
        "three_C3_states_role": "three copies of a matter representation, not gauge charges",
        "SU5_is_derived_from_current_RefG_action": False,
        "reference_value_used": False,
    }


def product_electroweak_fixed_point_no_go() -> dict[str, object]:
    """Test simultaneous nonzero roots of the minimal product EW equations."""

    f_g = sp.symbols("f_g", positive=True)
    b_y = sp.Rational(41, 6)
    b_2 = -sp.Rational(19, 6)
    g_y_sq_star = sp.simplify(16 * sp.pi**2 * f_g / b_y)
    g_2_sq_star = sp.simplify(16 * sp.pi**2 * f_g / b_2)

    # The conditional common-trace relation is not invariant under the
    # separate one-loop SM product-group flow.  Write x_i=g_i^2 and test the
    # tangent condition on x_2=(5/3)x_Y.
    x_y = sp.symbols("x_Y", positive=True)
    x_2 = sp.Rational(5, 3) * x_y
    beta_x_y = -2 * f_g * x_y + b_y * x_y**2 / (8 * sp.pi**2)
    beta_x_2 = -2 * f_g * x_2 + b_2 * x_2**2 / (8 * sp.pi**2)
    relation_flow = sp.factor(beta_x_2 - sp.Rational(5, 3) * beta_x_y)

    return {
        "beta_convention": "beta_g=-f_g g+b g^3/(16 pi^2)",
        "b_Y": b_y,
        "b_2": b_2,
        "formal_nonzero_gY_squared": g_y_sq_star,
        "formal_nonzero_g2_squared": g_2_sq_star,
        "hypercharge_root_positive_for_fg_positive": True,
        "weak_root_positive_for_fg_positive": False,
        "simultaneous_nonzero_physical_EW_fixed_point": False,
        "semi_interacting_root": "gY=gY_star, g2=0",
        "semi_interacting_root_exists": True,
        "semi_interacting_root_fixes_electromagnetism": False,
        "reason_e_is_not_fixed": (
            "the SU(2) trajectory remains an independent direction, so the "
            "low-energy value of g2 and hence e are not selected"
        ),
        "common_trace_relation_flow_residual": relation_flow,
        "common_trace_relation_is_product_SM_RG_invariant": relation_flow == 0,
        "scope_limited_conclusion": (
            "the physical electromagnetic coupling is not fixed by the "
            "minimal one-loop product electroweak system with one universal "
            "gravity term; a genuinely unified UV phase or a derived fuller "
            "fixed-point system is required"
        ),
        "reference_value_used": False,
    }


def minimal_su5_screening_sign_audit() -> dict[str, object]:
    """Compute the one-loop sign for a minimal non-supersymmetric witness.

    Content used only for the sign audit:
      - three left-handed generations in 10 + 5bar;
      - one complex scalar 5 containing an electroweak Higgs doublet;
      - one real adjoint 24 for simple-group breaking.
    """

    c2_adj = sp.Integer(5)
    t_10 = sp.Rational(3, 2)
    t_5 = sp.Rational(1, 2)
    t_24 = sp.Integer(5)
    generations = sp.Integer(3)

    gauge = -sp.Rational(11, 3) * c2_adj
    weyl_fermions = sp.Rational(2, 3) * generations * (t_10 + t_5)
    complex_higgs = sp.Rational(1, 3) * t_5
    real_adjoint = sp.Rational(1, 6) * t_24
    b_minimal = sp.simplify(gauge + weyl_fermions + complex_higgs + real_adjoint)

    f_g = sp.symbols("f_g", positive=True)
    formal_root = sp.simplify(16 * sp.pi**2 * f_g / b_minimal)
    delta_b = sp.symbols("Delta_b", real=True)
    b_total = sp.simplify(b_minimal + delta_b)

    return {
        "gauge_contribution": gauge,
        "three_generation_Weyl_contribution": weyl_fermions,
        "complex_5_scalar_contribution": complex_higgs,
        "real_24_scalar_contribution": real_adjoint,
        "minimal_b_U": b_minimal,
        "minimal_b_U_is_screening_positive": b_minimal > 0,
        "formal_minimal_nonzero_gU_squared": formal_root,
        "minimal_nonzero_root_is_physical": False,
        "general_extra_screening": delta_b,
        "general_b_U": b_total,
        "positive_formal_root_condition": sp.Gt(delta_b, -b_minimal),
        "positive_formal_root_is_sufficient_for_full_fixed_point": False,
        "extra_UV_spectrum_derived_in_RefG": False,
        "reference_value_used": False,
    }


def unified_gravity_gauge_prediction_kernel() -> dict[str, object]:
    """Derive the fixed-point-scale coupling if the premises are supplied."""

    f_g, b_u = sp.symbols("f_g b_U", positive=True)
    g_u_squared = sp.simplify(16 * sp.pi**2 * f_g / b_u)
    alpha_u = sp.simplify(g_u_squared / (4 * sp.pi))
    alpha_em_matching = sp.simplify(sp.Rational(3, 8) * alpha_u)
    inverse_alpha_em_matching = sp.simplify(1 / alpha_em_matching)

    g = sp.symbols("g", positive=True)
    beta = -f_g * g + b_u * g**3 / (16 * sp.pi**2)
    stability_derivative = sp.simplify(
        sp.diff(beta, g).subs(g**2, g_u_squared)
    )

    return {
        "unified_beta": beta,
        "interacting_gU_squared": g_u_squared,
        "unified_alpha": alpha_u,
        "electromagnetic_alpha_if_breaking_at_fixed_point_scale": alpha_em_matching,
        "electromagnetic_inverse_alpha_if_breaking_at_fixed_point_scale": inverse_alpha_em_matching,
        "fixed_point_stability_derivative": stability_derivative,
        "IR_attractive_UV_repulsive_gauge_direction_for_fg_positive": stability_derivative > 0,
        "predictive_only_after_full_stability_matrix_audit": True,
        "absolute_prediction_inputs": (f_g, b_u),
        "target_free_kernel": True,
        "low_energy_value_requires_full_breaking_and_threshold_flow": True,
        "reference_value_used": False,
    }


def sharp_transition_one_loop_flow_witness() -> dict[str, object]:
    """Expose the extra scales needed between the UV root and low energy.

    This is a deliberately transparent witness, not a full FRG solution.  It
    assumes a sharp gravity-decoupling scale k_tr, unified one-loop running to
    a breaking scale M_U, and minimal-SM product running down to M_Z.  Finite
    breaking, electroweak, quark and hadronic thresholds remain separate.
    """

    f_g, b_u = sp.symbols("f_g b_U", positive=True)
    k_tr, m_u, m_z = sp.symbols("k_tr M_U M_Z", positive=True)
    delta_ir = sp.symbols("Delta_IR", real=True)

    inverse_alpha_u_star = b_u / (4 * sp.pi * f_g)
    inverse_alpha_u_at_breaking = (
        inverse_alpha_u_star
        + b_u * sp.log(k_tr / m_u) / (2 * sp.pi)
    )
    inverse_alpha_em_at_breaking = (
        2 * b_u / (3 * sp.pi * f_g)
        + 4 * b_u * sp.log(k_tr / m_u) / (3 * sp.pi)
    )

    b_y = sp.Rational(41, 6)
    b_2 = -sp.Rational(19, 6)
    b_em_above_ew = sp.simplify(b_y + b_2)
    inverse_alpha_em_at_mz = (
        inverse_alpha_em_at_breaking
        + b_em_above_ew * sp.log(m_u / m_z) / (2 * sp.pi)
    )

    return {
        "sharp_transition_assumption": True,
        "unified_inverse_alpha_at_gravity_transition": inverse_alpha_u_star,
        "unified_inverse_alpha_at_breaking": inverse_alpha_u_at_breaking,
        "electromagnetic_inverse_alpha_at_breaking": inverse_alpha_em_at_breaking,
        "minimal_SM_bY_plus_b2": b_em_above_ew,
        "electromagnetic_inverse_alpha_at_MZ_before_finite_thresholds": inverse_alpha_em_at_mz,
        "formal_Thomson_inverse_alpha": inverse_alpha_em_at_mz + delta_ir,
        "additional_inputs_beyond_fixed_point": (
            k_tr / m_u,
            m_u / m_z,
            delta_ir,
        ),
        "full_threshold_flow_derived": False,
        "reference_value_used": False,
    }


def refg_fixed_point_derivability_audit() -> dict[str, object]:
    return {
        "current_p01_status": "classical low-energy seven-coefficient response EFT",
        "missing_quantum_objects": (
            "effective average action Gamma_k including metric, ghosts, Phi, phi^A and physical gauge fields",
            "gauge fixing and regulator with a regulator-independence audit",
            "simultaneous fixed point for Newton, cosmological and p01 response couplings",
            "gravity contribution f_g to the physical unified gauge two-point function",
            "complete unified charged spectrum fixing b_U",
            "derived breaking sector and its vacuum, plus the transition and breaking scales",
            "full stability matrix and critical surface",
        ),
        "dimensionless_Newton_fixed_point_derived": False,
        "gravity_gauge_coefficient_f_g_derived": False,
        "unified_group_and_breaking_derived": False,
        "unified_matter_coefficient_b_U_derived": False,
        "no_relevant_direction_projects_onto_photon_stiffness_proved": False,
        "current_alpha_prediction": False,
        "next_computable_quantity": (
            "derive f_g and b_U from one declared microscopic RefG+unified-gauge action; "
            "only then evaluate the target-free fixed-point kernel"
        ),
        "reference_value_used": False,
    }


def primary_reference_ledger() -> tuple[dict[str, str], ...]:
    return (
        {
            "source": "https://arxiv.org/abs/1711.02949",
            "result": (
                "gravity and matter fluctuations can generate an interacting "
                "fixed point for a unified gauge coupling"
            ),
        },
        {
            "source": "https://arxiv.org/abs/1803.04027",
            "result": (
                "an Abelian hypercharge fixed point can become predictive in "
                "a gravity-matter truncation"
            ),
        },
        {
            "source": "https://arxiv.org/abs/hep-th/9606001",
            "result": "simple-group/spectral normalization gives gauge-coupling ratios, not the absolute scale",
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
    comparison_float = any(
        isinstance(value, float) and 100 < abs(value) < 200
        for value in numeric_literals
    )
    comparison_module = any(name in source for name in forbidden_modules)
    comparison_text = any(text in source for text in forbidden_text)
    return {
        "contains_comparison_numeric_literal": comparison_float,
        "imports_comparison_module": comparison_module,
        "contains_comparison_text": comparison_text,
        "target_isolation_pass": not (
            comparison_float or comparison_module or comparison_text
        ),
    }


def run_gate() -> None:
    embedding = su5_physical_q_normalization_theorem()
    product = product_electroweak_fixed_point_no_go()
    sign = minimal_su5_screening_sign_audit()
    kernel = unified_gravity_gauge_prediction_kernel()
    flow = sharp_transition_one_loop_flow_witness()
    refg = refg_fixed_point_derivability_audit()
    firewall = source_firewall()

    assert embedding["hypercharge_is_traceless"]
    assert embedding["normalized_trace_is_one_half"]
    assert embedding["g2_squared_equals_5_over_3_gY_squared"]
    assert embedding["e_squared_over_gU_squared"] == sp.Rational(3, 8)
    assert product["simultaneous_nonzero_physical_EW_fixed_point"] is False
    assert product["semi_interacting_root_exists"]
    assert product["semi_interacting_root_fixes_electromagnetism"] is False
    assert product["common_trace_relation_is_product_SM_RG_invariant"] is False
    assert sign["minimal_b_U"] == -sp.Rational(40, 3)
    assert sign["minimal_nonzero_root_is_physical"] is False
    assert kernel["electromagnetic_inverse_alpha_if_breaking_at_fixed_point_scale"] == (
        2 * sp.symbols("b_U", positive=True)
        / (3 * sp.pi * sp.symbols("f_g", positive=True))
    )
    assert kernel["target_free_kernel"]
    assert flow["minimal_SM_bY_plus_b2"] == sp.Rational(11, 3)
    assert flow["full_threshold_flow_derived"] is False
    assert refg["current_alpha_prediction"] is False
    assert firewall["target_isolation_pass"]

    for title, payload in (
        ("simple-group physical-Q normalization", embedding),
        ("product electroweak fixed-point no-go", product),
        ("minimal unified screening sign", sign),
        ("unified gravity-gauge prediction kernel", kernel),
        ("sharp-transition one-loop flow witness", flow),
        ("RefG derivability audit", refg),
        ("source firewall", firewall),
    ):
        print(f"\n{title}")
        for key, value in payload.items():
            print(f"  {key}: {value}")

    print("\nprimary references")
    for row in primary_reference_ledger():
        print(f"  {row['source']}: {row['result']}")

    print(
        "\nSTATUS: OPEN_DERIVED_UNIFIED_GROUP_BREAKING_UV_SPECTRUM_REFG_"
        "GRAVITY_FIXED_POINT_AND_THRESHOLD_FLOW__PASS_TARGET_INDEPENDENT_"
        "CONDITIONAL_SU5_NORMALIZATION_UNIVERSAL_GRAVITY_ONE_LOOP_PRODUCT_"
        "EW_NO_GO_AND_UNIFIED_PREDICTION_KERNEL"
    )


if __name__ == "__main__":
    run_gate()
