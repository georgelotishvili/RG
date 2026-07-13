from __future__ import annotations

"""PHASE 18bv: microscopic alpha-selector routes gate.

p18bu proves that the current RefG continuum action and its symmetries leave
one physical Maxwell modulus.  That does not mean that every microscopic
model is unable to select a coupling.  This gate separates two often-confused
claims:

  * a fully specified, single-scale compact node Hamiltonian can select a
    target-independent dimensionless link coupling by its spectrum;
  * merely declaring "no bare F^2" in a continuum effective action does not
    select the coupling without the complete regulator, spectrum and finite
    matching data.

The positive witness is the strict-ice pure-ring quantum-link Hamiltonian.
Published exact-diagonalization data give it a definite emergent link alpha.
It is not a RefG electromagnetic prediction: the Hamiltonian is not derived
from F_min, strict projection removes dynamical charges, and the primitive
spin-ice defect is not the physical Q=T3+Y charge.

The negative witness is exact.  With no bare plaquette and the same primitive
charge spectrum, different hopping/gap ratios induce different plaquette
stiffnesses.  A continuum no-bare statement is also scheme dependent unless a
finite microscopic regulator and measure are declared.  No electromagnetic
comparison value is imported or used anywhere in this gate.
"""

import ast
import inspect
import math

import sympy as sp

from p18bl_target_free_alpha_kernel_gate import (
    C3_ORDER,
    H_BRANCH,
    exact_c3_mass_ratios,
)
from p18bq_photon_rigidity_uv_normalization_matching_gate import (
    neutral_generator_spectrum_rigidity_theorem,
    route_selection_and_closure_contract,
)
from p18br_hs_auxiliary_link_origin_gate import (
    leading_induced_plaquette_theorem,
)


def single_scale_pure_ring_selector_witness() -> dict[str, object]:
    """Use published pure-ring spectral data as a positive existence proof.

    The strict ice manifold has an exact Gauss constraint and one Hamiltonian
    scale g.  Pace et al. report e=0.20(1)*sqrt(a g) and
    c=0.51(6)*a g/hbar at the unperturbed pure-ring point.  Their convention
    is alpha=e^2/(hbar c), so both a and g cancel.
    """

    lattice_a, ring_g, hbar = sp.symbols("a g hbar", positive=True)
    e_coefficient = sp.Float("0.20")
    e_sigma = sp.Float("0.01")
    c_coefficient = sp.Float("0.51")
    c_sigma = sp.Float("0.06")

    electric_charge = e_coefficient * sp.sqrt(lattice_a * ring_g)
    photon_speed = c_coefficient * lattice_a * ring_g / hbar
    alpha_link = sp.simplify(electric_charge**2 / (hbar * photon_speed))
    relative_variance = (2 * e_sigma / e_coefficient) ** 2 + (
        c_sigma / c_coefficient
    ) ** 2
    alpha_sigma = sp.N(alpha_link * sp.sqrt(relative_variance), 12)

    return {
        "microscopic_Hamiltonian": (
            "H0=-g sum_hexagon(W_hexagon+W_hexagon^dagger), with G_x=0"
        ),
        "link_Hilbert_space": "spin-1/2 quantum links in the strict ice manifold",
        "exact_Gauss_constraint": True,
        "independent_Hamiltonian_energy_scales": 1,
        "published_electric_charge": electric_charge,
        "published_photon_speed": photon_speed,
        "published_link_alpha": alpha_link,
        "published_link_alpha_numeric": float(sp.N(alpha_link, 12)),
        "propagated_published_statistical_sigma": float(alpha_sigma),
        "lattice_spacing_cancels": not alpha_link.has(lattice_a),
        "overall_ring_scale_cancels": not alpha_link.has(ring_g),
        "hbar_cancels": not alpha_link.has(hbar),
        "declared_model_selects_link_alpha_without_target": True,
        "result_is_exact_closed_form": False,
        "result_is_external_numerical_spectrum": True,
        "strict_projection_has_finite_energy_dynamical_electric_charges": False,
        "primitive_ice_defect_is_physical_Q": False,
        "Hamiltonian_derived_from_current_RefG_Fmin": False,
        "allowed_diagonal_and_longer_ring_perturbations_are_absent_by_RefG_theorem": False,
        "current_RefG_alpha_EM_prediction": False,
        "reference_value_used": False,
    }


def rk_projector_relativistic_no_go() -> dict[str, object]:
    """Show why the exactly soluble RK point is not a nonzero Maxwell selector."""

    epsilon, a_e, a_c = sp.symbols("epsilon A_e A_c", positive=True)
    electric_charge = a_e * sp.sqrt(epsilon)
    photon_speed = a_c * sp.sqrt(epsilon)
    alpha = sp.simplify(electric_charge**2 / photon_speed)

    return {
        "distance_to_RK_point": "epsilon=1-mu -> 0+",
        "electric_charge_scaling": electric_charge,
        "linear_photon_speed_scaling": photon_speed,
        "alpha_scaling": alpha,
        "alpha_RK_limit": sp.limit(alpha, epsilon, 0, dir="+"),
        "linear_photon_speed_RK_limit": sp.limit(
            photon_speed, epsilon, 0, dir="+"
        ),
        "RK_dynamic_exponent": 2,
        "RK_has_relativistic_linear_photon": False,
        "RK_selects_nonzero_Maxwell_alpha": False,
        "equal_projector_or_frustration_free_alone_closes_physical_alpha": False,
        "reference_value_used": False,
    }


def continuum_no_bare_scheme_theorem() -> dict[str, object]:
    """Distinguish a microscopic no-plaquette action from a scheme choice."""

    k_bare, delta_fin, loop, shift = sp.symbols(
        "K_bare delta_K_fin K_loop c", real=True
    )
    total = sp.simplify(k_bare + delta_fin + loop)
    shifted_total = sp.simplify(
        (k_bare + shift) + (delta_fin - shift) + loop
    )

    return {
        "total_stiffness": total,
        "finite_scheme_change": (
            "K_bare->K_bare+c, delta_K_fin->delta_K_fin-c"
        ),
        "total_stiffness_is_scheme_invariant": sp.simplify(
            shifted_total - total
        )
        == 0,
        "K_bare_equals_zero_is_continuum_scheme_invariant": False,
        "microscopic_lattice_no_plaquette_is_a_valid_boundary_condition": True,
        "microscopic_prediction_requires_declared_regulator_measure_and_all_couplings": True,
        "continuum_no_bare_statement_alone_predicts_alpha": False,
        "reference_value_used": False,
    }


def same_spectrum_different_induced_stiffness_theorem() -> dict[str, object]:
    """Give an exact no-bare, same-charge, different-coupling witness."""

    upstream = leading_induced_plaquette_theorem()
    kappa = sp.symbols("kappa", positive=True)
    species = sp.Integer(3)
    primitive_charge = sp.Integer(1)
    beta = sp.simplify(2 * species * kappa**4 * primitive_charge**2)
    kappa_one = sp.Rational(1, 4)
    kappa_two = sp.Rational(1, 3)
    beta_one = sp.simplify(beta.subs(kappa, kappa_one))
    beta_two = sp.simplify(beta.subs(kappa, kappa_two))

    return {
        "single_mode_exact_flux_coefficient": upstream[
            "induced_Wilson_beta_per_mode"
        ],
        "primitive_charge_spectrum": (1, 1, 1),
        "bare_plaquette_coefficient": 0,
        "common_hopping_gap_ratio": kappa,
        "three_mode_induced_beta": beta,
        "first_hopping_gap_ratio": kappa_one,
        "second_hopping_gap_ratio": kappa_two,
        "first_induced_beta": beta_one,
        "second_induced_beta": beta_two,
        "first_expected_value": sp.Rational(3, 128),
        "second_expected_value": sp.Rational(2, 27),
        "same_spectrum_and_no_bare_term": True,
        "different_induced_stiffnesses": beta_one != beta_two,
        "no_bare_plus_charge_spectrum_fixes_stiffness": False,
        "hopping_gap_ratios_must_be_derived": True,
        "reference_value_used": False,
    }


def pure_induced_exact_c3_leading_log_ledger() -> dict[str, object]:
    """Evaluate the strongest old C3 lepton-only induced conditional branch.

    This is intentionally not a prediction.  It grants the exact-C3 mass
    ratios, the historical core-scale rule and primitive unit lepton charge,
    while removing the old bare Maxwell contribution completely.  The output
    shows what pure induction alone supplies before finite and full-spectrum
    completion.
    """

    tau_over_e, muon_over_e = exact_c3_mass_ratios()
    core_factor = (C3_ORDER * H_BRANCH) ** 2
    log_argument = (
        core_factor**3 * tau_over_e**5 / muon_over_e
    )
    stiffness = math.log(log_argument) / (6.0 * math.pi**2)
    inverse_alpha = 4.0 * math.pi * stiffness

    return {
        "granted_exact_C3_tau_over_e": tau_over_e,
        "granted_exact_C3_muon_over_e": muon_over_e,
        "historical_core_scale_rule": "Lambda=(3h)^2 m_tau^2/m_e",
        "primitive_lepton_charge_assumption": 1,
        "pure_induced_log_argument": log_argument,
        "pure_induced_stiffness": stiffness,
        "pure_induced_inverse_alpha": inverse_alpha,
        "old_bare_Maxwell_contribution_included": False,
        "exact_C3_spectrum_derived_from_localized_RefG_action": False,
        "core_scale_rule_derived_from_localized_RefG_action": False,
        "finite_regulator_part_included": False,
        "complete_physical_Q_spectrum_included": False,
        "self_contained_prediction": False,
        "reference_value_used": False,
    }


def standard_model_compositeness_sign_no_go() -> dict[str, object]:
    """Test a zero-stiffness UV boundary with the imported SM coefficients."""

    log_ratio = sp.symbols("L", positive=True)
    b_y = sp.Rational(41, 6)
    b_2 = -sp.Rational(19, 6)
    b_3 = -sp.Integer(7)
    stiffnesses = tuple(
        sp.simplify(b * log_ratio / (8 * sp.pi**2))
        for b in (b_y, b_2, b_3)
    )

    return {
        "boundary_condition": "K_Y(Lambda)=K_2(Lambda)=K_3(Lambda)=0",
        "one_loop_coefficients": (b_y, b_2, b_3),
        "infrared_stiffnesses_for_log_Lambda_over_mu_positive": stiffnesses,
        "hypercharge_stiffness_positive": bool(b_y > 0),
        "weak_stiffness_positive": bool(b_2 > 0),
        "color_stiffness_positive": bool(b_3 > 0),
        "minimal_imported_SM_supports_all_group_compositeness": False,
        "matter_rich_non_asymptotically_free_completion_required": True,
        "such_extra_spectrum_derived_in_RefG": False,
        "physical_SM_spectrum_derived_in_RefG": False,
        "reference_value_used": False,
    }


def physical_q_bridge_and_success_contract() -> dict[str, object]:
    q = neutral_generator_spectrum_rigidity_theorem()
    closure = route_selection_and_closure_contract()
    requirements = (
        "derive a finite node/link Hilbert space and exact Gauss operator from F_min or its declared UV completion",
        "derive one complete microscopic Hamiltonian and every symmetry-allowed diagonal and loop coefficient",
        "prove a deconfined 3+1D Coulomb phase",
        "compute the thermodynamic primitive-flux and photon spectra",
        "derive the primitive defect as the complete physical Q=T3+Y charge lattice",
        "derive finite-energy charged cores, hopping, masses and multiplicities",
        "derive electroweak breaking, QCD and HVP from the same microscopic theory",
        "run and match the frozen high-scale prediction to the Thomson limit",
    )
    return {
        "conditional_physical_generator": q["unique_primitive_generator"],
        "frame_generator_component_in_photon": q[
            "frame_component_in_physical_photon"
        ],
        "hypercharges_are_imported": q[
            "hypercharges_are_imported_not_derived"
        ],
        "pure_ring_primitive_defect_is_derived_as_electron_charge": False,
        "fractional_quark_charge_and_global_quotient_derived": False,
        "existing_joint_closure_requirements_satisfied": closure[
            "current_requirements_satisfied"
        ],
        "requirements": requirements,
        "requirement_count": len(requirements),
        "current_contract_satisfied": False,
        "reference_value_used": False,
    }


def primary_reference_ledger() -> tuple[dict[str, str], ...]:
    return (
        {
            "source": "https://arxiv.org/abs/2009.04499",
            "result": (
                "finite-volume spectra determine a definite coupling for a "
                "fully specified pure-ring model and show that allowed local "
                "perturbations tune it"
            ),
        },
        {
            "source": "https://arxiv.org/abs/cond-mat/0307592",
            "result": (
                "the exactly soluble Rokhsar--Kivelson point has quadratic, "
                "rather than relativistic linear, photon dynamics"
            ),
        },
        {
            "source": "https://arxiv.org/abs/hep-th/0507118",
            "result": (
                "an explicit string-net photon-plus-charge Hamiltonian contains "
                "independent charge, electric, ring and hopping coefficients"
            ),
        },
        {
            "source": "https://arxiv.org/abs/hep-ph/9607331",
            "result": "gauge-boson compositeness is a UV boundary condition, not charge topology alone",
        },
        {
            "source": "https://arxiv.org/abs/hep-th/0010147",
            "result": (
                "non-Abelian compositeness requires a matter-rich regime that "
                "is complementary to asymptotic freedom"
            ),
        },
        {
            "source": "https://arxiv.org/abs/1102.5035",
            "result": "a Maxwell term may be dynamically induced from a complete microscopic matter theory",
        },
        {
            "source": "https://arxiv.org/abs/hep-th/0306138",
            "result": "heat-kernel coefficients determine the local induced F-squared term once the operator and regulator are declared",
        },
        {
            "source": "https://arxiv.org/abs/1511.08374",
            "result": (
                "induced lattice gauge actions require explicit matching of "
                "microscopic parameters to the continuum gauge coupling"
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
    forbidden_text = (
        "CO" + "DATA",
        "observed " + "inverse",
        "13" + "7.",
    )
    comparison_float = any(
        isinstance(value, float) and 100 < abs(value) < 200
        for value in numeric_literals
    )
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
    allowed_local_imports = {
        "p18bl_target_free_alpha_kernel_gate",
        "p18bq_photon_rigidity_uv_normalization_matching_gate",
        "p18br_hs_auxiliary_link_origin_gate",
    }
    violations = tuple(text for text in forbidden_text if text in source)
    disallowed_imports = tuple(
        name for name in local_imports if name not in allowed_local_imports
    )
    comparison_module = any(name in source for name in forbidden_modules)
    return {
        "contains_comparison_numeric_literal": comparison_float,
        "forbidden_text_violations": violations,
        "local_imports": local_imports,
        "disallowed_local_imports": disallowed_imports,
        "imports_comparison_module": comparison_module,
        "target_isolation_pass": not (
            comparison_float
            or violations
            or disallowed_imports
            or comparison_module
        ),
    }


def run_gate() -> None:
    pure_ring = single_scale_pure_ring_selector_witness()
    rk = rk_projector_relativistic_no_go()
    scheme = continuum_no_bare_scheme_theorem()
    induced = same_spectrum_different_induced_stiffness_theorem()
    c3 = pure_induced_exact_c3_leading_log_ledger()
    sm = standard_model_compositeness_sign_no_go()
    bridge = physical_q_bridge_and_success_contract()
    firewall = source_firewall()

    assert pure_ring["exact_Gauss_constraint"]
    assert pure_ring["independent_Hamiltonian_energy_scales"] == 1
    assert pure_ring["lattice_spacing_cancels"]
    assert pure_ring["overall_ring_scale_cancels"]
    assert pure_ring["hbar_cancels"]
    assert pure_ring["declared_model_selects_link_alpha_without_target"]
    assert pure_ring["result_is_exact_closed_form"] is False
    assert pure_ring[
        "strict_projection_has_finite_energy_dynamical_electric_charges"
    ] is False
    assert pure_ring["primitive_ice_defect_is_physical_Q"] is False
    assert pure_ring["Hamiltonian_derived_from_current_RefG_Fmin"] is False
    assert rk["alpha_RK_limit"] == 0
    assert rk["linear_photon_speed_RK_limit"] == 0
    assert rk["RK_dynamic_exponent"] == 2
    assert rk["RK_selects_nonzero_Maxwell_alpha"] is False
    assert scheme["total_stiffness_is_scheme_invariant"]
    assert scheme["K_bare_equals_zero_is_continuum_scheme_invariant"] is False
    assert scheme["continuum_no_bare_statement_alone_predicts_alpha"] is False
    assert induced["first_induced_beta"] == sp.Rational(3, 128)
    assert induced["second_induced_beta"] == sp.Rational(2, 27)
    assert induced["different_induced_stiffnesses"]
    assert induced["no_bare_plus_charge_spectrum_fixes_stiffness"] is False
    assert c3["old_bare_Maxwell_contribution_included"] is False
    assert c3["self_contained_prediction"] is False
    assert sm["hypercharge_stiffness_positive"]
    assert sm["weak_stiffness_positive"] is False
    assert sm["color_stiffness_positive"] is False
    assert sm["minimal_imported_SM_supports_all_group_compositeness"] is False
    assert bridge["frame_generator_component_in_photon"] == 0
    assert bridge["current_contract_satisfied"] is False
    assert firewall["target_isolation_pass"]

    for title, payload in (
        ("single-scale pure-ring selector witness", pure_ring),
        ("RK projector relativistic no-go", rk),
        ("continuum no-bare scheme theorem", scheme),
        ("same-spectrum induced-stiffness theorem", induced),
        ("pure-induced exact-C3 leading-log ledger", c3),
        ("Standard-Model compositeness sign no-go", sm),
        ("physical-Q bridge and success contract", bridge),
        ("source firewall", firewall),
    ):
        print(f"\n{title}")
        for key, value in payload.items():
            print(f"  {key}: {value}")

    print("\nprimary references")
    for row in primary_reference_ledger():
        print(f"  {row['source']}: {row['result']}")

    print(
        "\nSTATUS: OPEN_REFG_DERIVED_SINGLE_SCALE_PHYSICAL_Q_NODE_"
        "HAMILTONIAN_DYNAMICAL_CHARGED_SPECTRUM_AND_COMPLETE_THOMSON_"
        "MATCHING__PASS_TARGET_INDEPENDENT_PURE_RING_MICROSCOPIC_SELECTOR_"
        "EXISTENCE_RK_ZERO_AND_NO_BARE_INDUCED_MAXWELL_INSUFFICIENCY_"
        "THEOREM"
    )


if __name__ == "__main__":
    run_gate()
