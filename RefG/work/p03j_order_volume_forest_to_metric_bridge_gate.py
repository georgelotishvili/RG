"""Relational RefG forest -> Lorentzian metric -> Einstein bridge.

This gate supplies the missing *shape* of the road between RefG's
node--imprint--relation language and the full material-response dictionary in
``p03i``.  It keeps three logically different statements separate:

1. A standard Lorentzian reconstruction theorem:

       causal order + spacetime volume element = Lorentzian geometry.

   On a distinguishing continuum spacetime of dimension greater than two,
   causal order fixes the conformal metric.  In four dimensions a volume
   density fixes the one remaining positive conformal factor.

2. RefG's static pressure/carrier-deficit branch has a useful fixed-chart
   compatibility identity.  With

       p=e^(-H),  phi=-2H,  rho_car/rho_0=e^phi=p^2,

   the exponential metric has

       sqrt(-g)/sqrt(-g_0)=p^(-2)=rho_0/rho_car

   in the chosen normalized material chart.  The p05 carrier density is a
   three-dimensional kinetic density, however, whereas causal reconstruction
   needs an independently defined four-dimensional event-count/volume
   measure.  The identity therefore checks compatibility only; it does not
   derive the missing four-volume law.  Scalar pressure alone also does not
   fix a generic metric.

3. The current RefG workspace has not yet derived from the undifferentiated
   foundation (a) a locally finite universal causal order, (b) a four-
   dimensional manifoldlike continuum limit, or (c) its dynamics.  Therefore
   the reconstruction theorem supplies a conditional continuum target *once
   those relational data and an independent four-volume form exist*; it does
   not manufacture those data or prove that a discrete network is
   manifoldlike.

No article or intuitive file is modified by this gate.

Primary theorem references
--------------------------
Hawking, King & McCarthy (1976), doi:10.1063/1.522874.
Malament (1977), doi:10.1063/1.523436.
Bombelli, Lee, Meyer & Sorkin (1987), doi:10.1103/PhysRevLett.59.521.
Lovelock (1972), doi:10.1063/1.1666069.
"""

from __future__ import annotations

from typing import Any

import sympy as sp

from p03i_full_forest_to_einstein_bridge_theorem import (
    einstein_equivalent_response_parent_action_gate,
    full_material_response_metric_dictionary_gate,
    worldtube_adm_and_standard_1pn_handoff_gate,
)


def causal_conformal_plus_volume_reconstruction_gate() -> dict[str, Any]:
    """Record the continuum theorem and verify only its 4D scaling algebra.

    The Hawking--King--McCarthy/Malament theorem is an external mathematical
    theorem, not something proved by this SymPy function.  Conditional on its
    smooth-spacetime hypotheses, it supplies a conformal representative
    ``g_bar``.  The executable algebra below checks that one independently
    specified positive four-volume density selects exactly one member
    ``g=Omega^2 g_bar`` of that conformal class.
    """

    a, b, c, d, volume_density = sp.symbols(
        "a b c d volume_density",
        positive=True,
        real=True,
    )
    omega = sp.Symbol("Omega", positive=True, real=True)

    g_bar = sp.diag(a, -b, -c, -d)
    sqrt_minus_det_g_bar = sp.sqrt(-g_bar.det())
    g = sp.simplify(omega**2) * g_bar
    sqrt_minus_det_g = sp.sqrt(-sp.factor(g.det()))

    four_dimensional_scaling_residual = sp.simplify(
        sqrt_minus_det_g - omega**4 * sqrt_minus_det_g_bar
    )

    reconstructed_omega = sp.simplify(
        (volume_density / sqrt_minus_det_g_bar) ** sp.Rational(1, 4)
    )
    reconstructed_g = (reconstructed_omega**2 * g_bar).applyfunc(sp.simplify)
    reconstructed_volume = sp.simplify(
        sp.sqrt(-sp.factor(reconstructed_g.det()))
    )
    volume_reconstruction_residual = sp.simplify(
        reconstructed_volume - volume_density
    )

    # Positive fourth roots are unique.  This algebraic representative of the
    # uniqueness step avoids introducing sign branches forbidden by Omega>0.
    omega_1, omega_2 = sp.symbols(
        "Omega_1 Omega_2",
        positive=True,
        real=True,
    )
    equal_volume_polynomial = sp.factor(omega_1**4 - omega_2**4)
    positive_root = sp.solve(
        sp.Eq(omega_1**4, omega_2**4),
        omega_1,
    )
    positive_uniqueness = positive_root == [omega_2]

    passed = (
        four_dimensional_scaling_residual == 0
        and volume_reconstruction_residual == 0
        and positive_uniqueness
    )

    return {
        "status": (
            "CONDITIONAL_STANDARD_CONTINUUM_RECONSTRUCTION_THEOREM__"
            "PASS_4D_CONFORMAL_VOLUME_SCALING_CHECK"
            if passed
            else "CHECK_CAUSAL_VOLUME_METRIC_RECONSTRUCTION"
        ),
        "standard_theorem_domain": (
            "a past- and future-distinguishing Lorentzian continuum "
            "spacetime, dimension > 2, with the relevant chronological/"
            "causal isomorphism hypotheses"
        ),
        "causal_order_result": (
            "causal order determines topology, differentiable structure and "
            "the conformal metric class [g]"
        ),
        "conformal_representative": g_bar,
        "conformal_metric": g,
        "sqrt_minus_det_g_bar": sqrt_minus_det_g_bar,
        "sqrt_minus_det_conformal_metric": sqrt_minus_det_g,
        "four_dimensional_volume_scaling": "sqrt(-g)=Omega^4 sqrt(-g_bar)",
        "four_dimensional_scaling_residual": (
            four_dimensional_scaling_residual
        ),
        "reconstructed_positive_Omega": reconstructed_omega,
        "reconstructed_metric": reconstructed_g,
        "reconstructed_volume_density": reconstructed_volume,
        "volume_reconstruction_residual": volume_reconstruction_residual,
        "equal_volume_factorization": equal_volume_polynomial,
        "positive_conformal_factor_is_unique": positive_uniqueness,
        "coordinate_component_information_split_in_4D": {
            "causal_conformal_structure": (
                "9 local coordinate-component combinations"
            ),
            "volume_scale": "1 local coordinate-component combination",
            "total": 10,
            "not_a_physical_DOF_count": True,
        },
        "important_limit": (
            "The external theorem reconstructs a metric from already obtained "
            "smooth continuum causal and four-volume data.  This executable "
            "gate checks only the conformal determinant scaling on a diagonal "
            "representative; it does not prove HKMM/Malament, topology or "
            "differentiable reconstruction, nor that an arbitrary microscopic "
            "network has a manifoldlike limit."
        ),
    }


def static_carrier_deficit_chart_compatibility_gate() -> dict[str, Any]:
    """Check a fixed-chart identity, not a four-event-volume derivation."""

    H = sp.Symbol("H", nonnegative=True, real=True)

    pressure_factor = sp.exp(-H)
    phi = -2 * H
    rho_carrier_ratio = sp.exp(phi)
    metric = sp.diag(
        pressure_factor**2,
        -pressure_factor**-2,
        -pressure_factor**-2,
        -pressure_factor**-2,
    )
    sqrt_minus_g = sp.simplify(sp.sqrt(-metric.det()))

    density_pressure_residual = sp.simplify(
        rho_carrier_ratio - pressure_factor**2
    )
    reciprocal_volume_residual = sp.simplify(
        rho_carrier_ratio * sqrt_minus_g - 1
    )
    lapse_residual = sp.simplify(
        sp.sqrt(metric[0, 0]) - pressure_factor
    )
    spatial_linear_readout = sp.simplify(
        1 / sp.sqrt(-metric[1, 1])
    )
    spatial_readout_residual = sp.simplify(
        spatial_linear_readout - pressure_factor
    )

    passed = (
        density_pressure_residual == 0
        and reciprocal_volume_residual == 0
        and lapse_residual == 0
        and spatial_readout_residual == 0
    )

    return {
        "status": (
            "PASS_STATIC_3D_CARRIER_DEFICIT_AND_METRIC_DETERMINANT_"
            "FIXED_CHART_COMPATIBILITY"
            if passed
            else "CHECK_STATIC_CARRIER_DEFICIT_VOLUME_READOUT"
        ),
        "pressure_factor_p": pressure_factor,
        "geometric_deficit_phi": phi,
        "phenomenological_3D_carrier_density_ratio_rho_car_over_rho0": (
            rho_carrier_ratio
        ),
        "static_exponential_metric": metric,
        "sqrt_minus_g": sqrt_minus_g,
        "density_equals_p_squared_residual": density_pressure_residual,
        "density_times_metric_volume_residual": reciprocal_volume_residual,
        "clock_readout_residual": lapse_residual,
        "one_dimensional_spatial_readout": spatial_linear_readout,
        "spatial_readout_residual": spatial_readout_residual,
        "physical_reading": (
            "On the static isotropic branch and in the normalized material "
            "chart, the chosen p05 three-dimensional carrier-density ansatz is "
            "reciprocal to the determinant density of the already assumed "
            "exponential metric.  This is a compatibility identity, not a "
            "derivation of an invariant four-event-count measure.  The causal "
            "propagation structure is still required to fix the conformal "
            "light-cone/shear/flow information."
        ),
        "scope_guard": (
            "rho_car/rho0=exp(phi) is p05's phenomenological three-dimensional "
            "kinetic carrier-density closure (used for mean spacing and mean "
            "free path).  It is not p13's refractive index n_eff and it is not "
            "the four-dimensional event-count density needed by causal metric "
            "reconstruction.  Both a microscopic derivation and an invariant "
            "four-volume/count law remain open."
        ),
    }


def node_imprint_relation_to_metric_chain_gate() -> dict[str, Any]:
    """State the exact chain and expose every non-theorem premise."""

    causal_volume = causal_conformal_plus_volume_reconstruction_gate()
    deficit = static_carrier_deficit_chart_compatibility_gate()
    material_dictionary = full_material_response_metric_dictionary_gate()

    conditional_target_chain_consistent = (
        causal_volume["status"].startswith(
            "CONDITIONAL_STANDARD_CONTINUUM_RECONSTRUCTION_THEOREM"
        )
        and deficit["status"].startswith("PASS_")
        and material_dictionary["status"].startswith(
            "PASS_FULL_MATERIAL_CHART_LOCAL_METRIC"
        )
    )

    return {
        "status": (
            "CONDITIONAL_ORDER_AND_INDEPENDENT_4VOLUME_TO_MATERIAL_METRIC_"
            "TARGET_CONSISTENT__DISCRETE_NETWORK_ORIGIN_OPEN"
            if conditional_target_chain_consistent
            else "CHECK_RELATIONAL_ORDER_VOLUME_TO_METRIC_CHAIN"
        ),
        "conditional_target_chain_consistent": (
            conditional_target_chain_consistent
        ),
        "actual_RefG_forest_to_metric_bridge_closed": False,
        "forest_stages": [
            {
                "stage": "0_undifferentiated_foundation",
                "content": (
                    "one ontological foundation; no prior x, clock time, "
                    "local pressure field or metric is assigned"
                ),
                "current_status": "ONTOLOGICAL_POSTULATE",
            },
            {
                "stage": "1_self_distinction",
                "content": (
                    "stable node, imprint and relation; repeated relations "
                    "supply a pre-clock process order"
                ),
                "current_status": (
                    "CONCEPTUAL_REFG_RULE__NO_MICROSCOPIC_TRANSITION_KERNEL"
                ),
            },
            {
                "stage": "2_relational_causal_network",
                "content": (
                    "x precedes y when an allowed manifested/self-distinguished "
                    "medium imprint can propagate from x to y; local finiteness "
                    "makes bounded "
                    "order intervals finite but does not by itself turn counts "
                    "into continuum four-volume"
                ),
                "current_status": (
                    "REQUIRED_PREMISE__PARTIAL_ORDER_UNIVERSALITY_AND_"
                    "COUNT_TO_4VOLUME_LAW_NOT_YET_DERIVED"
                ),
            },
            {
                "stage": "3_manifoldlike_3_plus_1_limit",
                "content": (
                    "the coarse network must admit a faithful manifoldlike "
                    "embedding/approximation by a distinguishing 3+1 "
                    "Lorentzian continuum, with controlled discreteness "
                    "fluctuations and E[N(A)]=rho_4 Vol_g(A), or the "
                    "corresponding coarse-grained approximate law"
                ),
                "current_status": (
                    "REQUIRED_PREMISE__DIMENSION_AND_CONTINUUM_LIMIT_OPEN"
                ),
            },
            {
                "stage": "4_metric_reconstruction",
                "content": (
                    "for an already smooth distinguishing continuum, causal "
                    "order fixes [g]; an independently supplied positive "
                    "four-volume form fixes the conformal factor"
                ),
                "current_status": causal_volume["status"],
            },
            {
                "stage": "5_material_response_dictionary",
                "content": (
                    "four operational labels q=(Phi,phi^A) encode g in the "
                    "full response K=(Y,C^A,B^AB)"
                ),
                "current_status": material_dictionary["status"],
            },
        ],
        "scalar_deficit_role": (
            "The pressure/carrier deficit supplies the static scalar clock/"
            "length readout and has a determinant compatibility identity in "
            "the selected chart.  It neither supplies the missing generic "
            "causal/conformal response nor derives the invariant four-volume "
            "measure."
        ),
        "conditional_local_result": (
            "Once a universal smooth manifoldlike causal structure and an "
            "independently established four-volume form exist, the standard "
            "continuum theorem fixes the Lorentzian metric and p03i gives its "
            "full local material-response encoding without a second metric."
        ),
        "remaining_origin_problem": (
            "Derive the universal locally finite order, a faithful 3+1 "
            "manifoldlike continuum limit, the four-event-count/volume law and "
            "its normalization from explicit self-distinction dynamics."
        ),
        "causal_volume_gate": causal_volume,
        "static_deficit_gate": deficit,
        "material_dictionary_gate": material_dictionary,
    }


def order_volume_to_einstein_and_1pn_status() -> dict[str, Any]:
    """Join relational reconstruction to the exact GR/1PN handoff."""

    relational = node_imprint_relation_to_metric_chain_gate()
    parent = einstein_equivalent_response_parent_action_gate()
    pn = worldtube_adm_and_standard_1pn_handoff_gate()

    conditional_target_chain_consistent = (
        relational["conditional_target_chain_consistent"]
        and parent["status"].startswith(
            "PASS_EXACT_PARAMETRIZED_EINSTEIN_PARENT_ACTION_IDENTITY"
        )
        and pn["status"].startswith(
            "PASS_DEFINED_GR_1PN_FORM_FOR_PARAMETRIZED_EINSTEIN_COMPLETION"
        )
    )

    current_micro_premises = {
        "universal_causal_partial_order_derived": False,
        "local_finiteness_and_count_measure_derived": False,
        "four_event_count_to_invariant_4volume_law_derived": False,
        "faithful_manifoldlike_embedding_and_fluctuation_control_derived": False,
        "three_plus_one_manifoldlike_limit_derived": False,
        "all_matter_modes_share_one_characteristic_cone_derived": False,
        "universal_minimal_matter_coupling_and_Ward_conservation_derived": False,
        "absence_of_nonminimal_curvature_or_composition_couplings_derived": False,
        "only_metric_gravity_mode_gapless_in_IR_derived": False,
        "two_derivative_Einstein_IR_dynamics_derived": False,
        "Newton_constant_from_foundation_parameters_derived": False,
        "no_extra_worldtube_charge_or_preferred_frame_operator_derived": False,
        "RefG_worldtube_to_ADM_EFT_matching_derived": False,
    }

    return {
        "status": (
            "OPEN_FOUNDATION_TO_CAUSAL_4VOLUME_MANIFOLD_AND_EINSTEIN_"
            "MATCHING__CONDITIONAL_CONTINUUM_TARGET_CHAIN_CONSISTENT"
            if conditional_target_chain_consistent
            else "CHECK_ORDER_VOLUME_TO_EINSTEIN_1PN_BRIDGE"
        ),
        "conditional_target_chain_consistent": (
            conditional_target_chain_consistent
        ),
        "standard_continuum_metric_reconstruction_exact_given_premises": True,
        "defined_parametrized_GR_target_exact_given_definition": True,
        "full_foundation_derivation_closed": False,
        "current_RefG_to_Einstein_and_1PN_bridge_closed": False,
        "current_micro_premises": current_micro_premises,
        "dynamics_theorem": (
            "If the reconstructed universal metric is the only gapless "
            "gravitational variable and the leading four-dimensional IR "
            "dynamics is metric-only, natural/local, diffeomorphism-covariant, "
            "symmetric, divergence-free and at most second order, the "
            "Lovelock/consistent-deformation result selects Einstein plus "
            "cosmological/boundary/topological terms.  Universal minimal "
            "matter coupling and its Ward identity are additional premises. "
            "These hypotheses, not the determinant algebra, are the remaining "
            "dynamics obligation."
        ),
        "one_premise_package_needed_to_finish": (
            "An explicit self-distinction/network action or a clearly named "
            "IR emergence axiom must produce: a universal locally finite "
            "causal order; a normalized four-event-count/volume law; a "
            "faithful 3+1 manifoldlike limit; one metric cone; universal "
            "minimal coupling and Ward conservation; no extra long-range, "
            "composition-dependent or preferred-frame charge; and the RefG "
            "worldtube-to-ADM matching."
        ),
        "why_1PN_then_needs_no_second_bridge": (
            "Only after that package fixes the same Einstein metric with "
            "minimal matter coupling do the standard compact-body worldline "
            "action and EIH 1PN equations follow from GR.  Pressure deficit "
            "may then be the upstream physical meaning of the matched metric "
            "response; it must be integrated/matched once, neither omitted "
            "while active nor counted again as a duplicate stress."
        ),
        "relational_reconstruction": relational,
        "Einstein_parent_action": parent,
        "standard_1PN_handoff": pn,
        "article_files_modified": False,
    }


def main() -> int:
    result = order_volume_to_einstein_and_1pn_status()
    print("status:", result["status"])
    print(
        "conditional target chain consistent:",
        result["conditional_target_chain_consistent"],
    )
    print(
        "full foundation derivation closed:",
        result["full_foundation_derivation_closed"],
    )
    print(
        "order+volume:",
        result["relational_reconstruction"]["causal_volume_gate"]["status"],
    )
    print(
        "static deficit:",
        result["relational_reconstruction"]["static_deficit_gate"]["status"],
    )
    print(
        "material metric:",
        result["relational_reconstruction"]["material_dictionary_gate"][
            "status"
        ],
    )
    print("Einstein action:", result["Einstein_parent_action"]["status"])
    print("1PN:", result["standard_1PN_handoff"]["status"])
    # Exit success certifies completion of the compatibility/obligation audit,
    # not closure of the physical RefG bridge (which remains explicitly False).
    return 0 if result["conditional_target_chain_consistent"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
