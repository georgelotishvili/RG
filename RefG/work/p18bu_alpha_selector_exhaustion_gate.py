from __future__ import annotations

"""PHASE 18bu: target-independent alpha-selector exhaustion gate.

p18bt identifies an operational compact-U(1) coupling from the primitive
electric-flux and transverse-photon spectra.  This gate asks the next and
harder question: does any structure currently derived in RefG select the
dimensionless electric/magnetic shape, identify its primitive flux with the
physical electromagnetic charge, and carry that result to the Thomson limit?

The answer is negative for the current action.  The result is deliberately a
scope-limited no-go, not a universal theorem against future microscopic
completions.  It combines four independent obstructions:

  1. F_min has no compact link Hilbert space, integer electric field, Gauss
     operator or independent ring term, and it is blind to the eigenframe.
  2. A Coulomb Hamiltonian has a continuous U/K shape deformation that keeps
     compactness, Gauss law, topology and photon speed fixed while changing
     alpha.
  3. generalized Maxwell duality fixes a rational coupling only after the
     electric and magnetic one-form gauging orders are independently derived;
     none of the present RefG integers is such an order.
  4. the gravity--gauge fixed-point kernel and the full Thomson matching both
     contain coefficients and spectra not derived by the present theory.

No electromagnetic comparison value is imported or used.  The purpose of
the gate is to close false shortcuts and state the smallest honest completion
that could turn the p18bt spectral observable into a prediction.
"""

import ast
import inspect

import sympy as sp

from p18bp_spin1_frame_electroweak_operator_gate import (
    composite_connection_maxwell_obstruction,
)
from p18bq_photon_rigidity_uv_normalization_matching_gate import (
    neutral_generator_spectrum_rigidity_theorem,
    route_selection_and_closure_contract,
)
from p18br_hs_auxiliary_link_origin_gate import (
    allowed_cp1_ring_operator_theorem,
    continuum_microscopic_completion_nonuniqueness_theorem,
    fmin_eigenframe_blindness_theorem,
    ordered_higgs_vs_coulomb_phase_dichotomy,
)
from p18bs_unified_physical_q_fixed_point_gate import (
    refg_fixed_point_derivability_audit,
    unified_gravity_gauge_prediction_kernel,
)
from p18bt_node_flux_photon_spectral_invariant_gate import (
    common_transposition_and_shape_theorem,
    refg_node_hamiltonian_derivability_audit,
)


def current_action_compact_photon_no_go() -> dict[str, object]:
    """Assemble the exact current-action obstructions proved upstream."""

    fmin = fmin_eigenframe_blindness_theorem()
    ring = allowed_cp1_ring_operator_theorem()
    uv = continuum_microscopic_completion_nonuniqueness_theorem()
    phase = ordered_higgs_vs_coulomb_phase_dichotomy()
    composite = composite_connection_maxwell_obstruction()
    node = refg_node_hamiltonian_derivability_audit()

    return {
        "current_bulk_field_content": (
            "one real phase scalar Phi and three real material scalars phi^A, "
            "with F_min=F(Y,I1,I2,I3)"
        ),
        "Fmin_is_eigenframe_blind": fmin[
            "all_Fmin_invariants_eigenframe_blind"
        ],
        "Fmin_derives_frame_stiffness": fmin[
            "p01_Fmin_derives_nonzero_frame_stiffness"
        ],
        "projective_ring_operator_is_symmetry_allowed": ring[
            "ring_is_local_projective_U1_invariant"
        ],
        "current_symmetry_forces_bare_ring_coefficient_to_zero": ring[
            "p01_or_p18f_symmetry_forces_rho_square_zero"
        ],
        "continuum_EFT_uniquely_selects_microscopic_bond_action": not uv[
            "witnesses_differ"
        ],
        "current_ordered_frame_is_massless_Coulomb_photon": phase[
            "p18f_axis_helicity_pair_can_be_relabelled_as_Coulomb_photon"
        ],
        "composite_frame_curvature_has_quadratic_Maxwell_propagator": composite[
            "composite_F2_has_quadratic_principal_symbol"
        ],
        "compact_link_Hilbert_space_and_Gauss_operator_derived": node[
            "local_node_Hilbert_space_and_Gauss_constraint_derived"
        ],
        "microscopic_compact_Hamiltonian_derived": node[
            "Hamiltonian_derived_from_current_Fmin"
        ],
        "scope_limited_no_go": (
            "the current F_min and ordered-frame branch do not contain a "
            "derived massless compact physical-Q photon sector"
        ),
        "future_microscopic_completion_forbidden": False,
        "reference_value_used": False,
    }


def continuous_coulomb_shape_fibre_theorem() -> dict[str, object]:
    """Prove that common tempo, topology and luminality do not select alpha."""

    u, k, lam = sp.symbols("U K lambda", positive=True)
    alpha = sp.sqrt(u / k) / (4 * sp.pi)
    u_deformed = lam * u
    k_deformed = k / lam
    alpha_deformed = sp.simplify(sp.sqrt(u_deformed / k_deformed) / (4 * sp.pi))
    photon_product_residual = sp.simplify(u_deformed * k_deformed - u * k)
    alpha_residual = sp.simplify(alpha_deformed - lam * alpha)

    return {
        "declared_Coulomb_Hamiltonian": (
            "H=(U/2) sum_l E_l^2+(K/2) sum_p B_p^2"
        ),
        "shape_deformation": "U->lambda U, K->K/lambda, lambda>0",
        "photon_speed_product_residual": photon_product_residual,
        "photon_speed_is_unchanged": photon_product_residual == 0,
        "compact_holonomy_period_is_unchanged": True,
        "integer_electric_flux_lattice_is_unchanged": True,
        "Gauss_constraint_is_unchanged": True,
        "winding_helicity_and_C3_labels_are_unchanged": True,
        "alpha_before": alpha,
        "alpha_after": alpha_deformed,
        "alpha_scales_by_lambda": alpha_residual == 0,
        "alpha_changes_continuously": sp.simplify(
            sp.diff(alpha_deformed, lam)
        )
        != 0,
        "same_kinematics_and_topology_fix_alpha": False,
        "shape_modulus_dimension": 1,
        "reference_value_used": False,
    }


def continuum_physical_q_operator_rank_theorem() -> dict[str, object]:
    """Count the marginal photon coefficients after all current symmetries.

    At quadratic order, spatial rotations allow E^2, B^2 and E.B.  P or T
    removes E.B, while emergent Lorentz invariance in fixed physical
    coordinates equates the electric and magnetic coefficients.  The two
    constraints have rank two on a three-dimensional coefficient space, so
    one common Maxwell stiffness remains.  Once the compact primitive charge
    fixes the period of A, that last coefficient cannot be removed by a field
    redefinition and is precisely the gauge coupling.
    """

    k_e, k_b, k_theta, scale = sp.symbols(
        "kappa_E kappa_B kappa_theta s", positive=True
    )
    coefficient_vector = sp.Matrix([k_e, k_b, k_theta])
    constraint_matrix = sp.Matrix([[0, 0, 1], [1, -1, 0]])
    constraint_rank = constraint_matrix.rank()
    nullspace = tuple(constraint_matrix.nullspace())
    kappa = sp.symbols("kappa", positive=True)
    alpha = 1 / (4 * sp.pi * kappa)
    scaled_alpha = sp.simplify(1 / (4 * sp.pi * scale * kappa))

    return {
        "rotation_invariant_quadratic_basis": ("E^2", "B^2", "E.B"),
        "coefficient_vector": coefficient_vector,
        "P_or_T_constraint": "kappa_theta=0",
        "Lorentz_constraint_in_fixed_coordinates": "kappa_E=kappa_B",
        "constraint_matrix": constraint_matrix,
        "constraint_rank": constraint_rank,
        "allowed_coefficient_space_dimension": 3 - constraint_rank,
        "allowed_nullspace": nullspace,
        "remaining_action": "S_gamma=(kappa/4) int F_mu_nu F^mu_nu",
        "primitive_charge_convention": "A modulo 2*pi with unit Wilson line",
        "field_rescaling_after_primitive_period_is_fixed": False,
        "alpha_in_potential_unit_convention": alpha,
        "symmetry_preserving_stiffness_rescaling": "kappa->s*kappa",
        "alpha_after_rescaling": scaled_alpha,
        "alpha_changes_under_allowed_common_stiffness": sp.diff(
            scaled_alpha, scale
        )
        != 0,
        "gauge_Ward_identity_forbids_finite_F2_renormalization": False,
        "C3_h2_c1_or_helicity_acts_on_common_F2_coefficient": False,
        "current_symmetries_leave_one_physical_marginal_modulus": (
            3 - constraint_rank
        )
        == 1,
        "reference_value_used": False,
    }


def generalized_maxwell_duality_family_theorem() -> dict[str, object]:
    """Separate a rational-coupling duality theorem from a number selector.

    In the convention

        S=(1/(2 e^2)) int F wedge *F,   alpha=e^2/(4 pi),

    gauging Z_Ne and Z_Nm one-form subgroups and composing with electric-
    magnetic duality can be a self-equivalence when e^2/(2 pi)=Nm/Ne.
    The theorem supplies a family indexed by independently declared coprime
    integers; it selects a number only if the microscopic theory uniquely
    derives those integers and the required line-operator lattice.
    """

    n_e, n_m = sp.symbols("N_e N_m", integer=True, positive=True)
    e_squared = sp.simplify(2 * sp.pi * n_m / n_e)
    alpha = sp.simplify(e_squared / (4 * sp.pi))
    self_dual_alpha = sp.simplify(alpha.subs({n_e: 1, n_m: 1}))
    second_alpha = sp.simplify(alpha.subs({n_e: 2, n_m: 1}))

    return {
        "coupling_convention": "alpha=e^2/(4*pi)",
        "rational_self_equivalence_condition": "e^2/(2*pi)=N_m/N_e",
        "conditional_alpha_family": alpha,
        "ordinary_self_dual_member": self_dual_alpha,
        "distinct_family_member": second_alpha,
        "family_contains_distinct_couplings": self_dual_alpha != second_alpha,
        "N_e_role": "order of a gauged electric one-form subgroup",
        "N_m_role": "order of a gauged magnetic one-form subgroup",
        "C3_is_a_derived_one_form_gauging_order": False,
        "spin1_Berry_c1_is_a_derived_physical_Q_gauging_order": False,
        "order9_or_h2_is_a_derived_physical_Q_gauging_order": False,
        "conditional_hidden_dimension_is_a_derived_gauging_order": False,
        "physical_Q_Wilson_tHooft_lattice_derived_in_RefG": False,
        "exact_electric_magnetic_self_equivalence_derived_in_RefG": False,
        "magnetic_partner_spectrum_derived_in_RefG": False,
        "dynamical_electric_charges_leave_exact_electric_one_form_symmetry": False,
        "low_energy_defect_symmetry_can_be_approximate_after_charges_decouple": True,
        "existence_of_a_noninvertible_duality_alone_selects_alpha": False,
        "using_a_desired_coupling_to_choose_Ne_Nm_is_a_prediction": False,
        "reference_value_used": False,
    }


def compact_u1_criticality_nonuniversality_audit() -> dict[str, object]:
    """Record the allowed deformation behind the critical-coupling no-go."""

    beta, gamma, flux = sp.symbols("beta gamma theta_p", real=True)
    plaquette_action = -beta * sp.cos(flux) - gamma * sp.cos(2 * flux)
    deformation = sp.diff(plaquette_action, gamma)

    return {
        "extended_compact_action_per_plaquette": plaquette_action,
        "symmetry_preserving_deformation": deformation,
        "deformation_is_nonzero": deformation != 0,
        "compact_period_is_preserved": sp.simplify(
            plaquette_action.subs(flux, flux + 2 * sp.pi) - plaquette_action
        )
        == 0,
        "integer_charge_and_flux_lattice_is_preserved": True,
        "deconfinement_transition_exists_for_an_action_family": True,
        "renormalized_critical_coupling_is_universal_across_that_family": False,
        "sitting_at_a_confinement_boundary_selects_unique_alpha": False,
        "evidence_scope": (
            "the extended-action lattice study gives an explicit counterexample "
            "to a conjectured universal renormalized critical coupling"
        ),
        "reference_value_used": False,
    }


def ordinary_abelian_matter_fixed_point_no_go() -> dict[str, object]:
    """Show why ordinary four-dimensional screening does not select a root."""

    alpha, b = sp.symbols("alpha b", positive=True)
    beta_alpha = sp.simplify(b * alpha**2 / (2 * sp.pi))
    nonzero_root = sp.solve(sp.Eq(beta_alpha / alpha, 0), alpha)

    return {
        "one_loop_screening_flow": beta_alpha,
        "positive_matter_coefficient": b,
        "Gaussian_root": 0,
        "positive_interacting_root": tuple(nonzero_root),
        "ordinary_screening_has_nonzero_fixed_point": bool(nonzero_root),
        "Landau_direction_for_positive_alpha": beta_alpha > 0,
        "a_nonzero_selector_requires_new_antiscreening_or_higher_operator_dynamics": True,
        "Pauli_or_other_fixed_point_operator_derived_in_current_RefG": False,
        "future_nonperturbative_fixed_point_forbidden": False,
        "reference_value_used": False,
    }


def fixed_point_and_thomson_underdetermination_audit() -> dict[str, object]:
    """Test the remaining continuum route and the low-energy bridge."""

    kernel = unified_gravity_gauge_prediction_kernel()
    fixed = refg_fixed_point_derivability_audit()
    q_rigidity = neutral_generator_spectrum_rigidity_theorem()
    matching = route_selection_and_closure_contract()

    return {
        "conditional_unified_inverse_alpha": kernel[
            "electromagnetic_inverse_alpha_if_breaking_at_fixed_point_scale"
        ],
        "conditional_fixed_point_inputs": kernel["absolute_prediction_inputs"],
        "gravity_gauge_coefficient_derived": fixed[
            "gravity_gauge_coefficient_f_g_derived"
        ],
        "unified_matter_coefficient_derived": fixed[
            "unified_matter_coefficient_b_U_derived"
        ],
        "unified_group_and_breaking_derived": fixed[
            "unified_group_and_breaking_derived"
        ],
        "photon_stiffness_has_no_relevant_or_marginal_direction_proved": fixed[
            "no_relevant_direction_projects_onto_photon_stiffness_proved"
        ],
        "physical_generator_direction": q_rigidity["unique_primitive_generator"],
        "hypercharges_are_imported": q_rigidity[
            "hypercharges_are_imported_not_derived"
        ],
        "primitive_electron_normalization_is_used_to_fix_Q_scale": True,
        "complete_global_charge_lattice_is_derived": False,
        "all_microscopic_and_matching_requirements_satisfied": matching[
            "current_requirements_satisfied"
        ],
        "current_Thomson_alpha_closed": matching["current_alpha_closed"],
        "reference_value_used": False,
    }


def current_selector_exhaustion_theorem() -> dict[str, object]:
    """Rank every current route without upgrading a conditional relation."""

    action = current_action_compact_photon_no_go()
    shape = continuous_coulomb_shape_fibre_theorem()
    operator_rank = continuum_physical_q_operator_rank_theorem()
    duality = generalized_maxwell_duality_family_theorem()
    critical = compact_u1_criticality_nonuniversality_audit()
    ordinary_rg = ordinary_abelian_matter_fixed_point_no_go()
    fixed = fixed_point_and_thomson_underdetermination_audit()
    upstream_shape = common_transposition_and_shape_theorem()

    routes = (
        ("current F_min/frame photon", False),
        ("common node-connection weakening", False),
        ("compactness/winding/C3/helicity alone", False),
        ("confinement boundary", False),
        ("generalized duality without derived one-form indices", False),
        ("ordinary four-dimensional Abelian matter flow", False),
        ("current symbolic gravity-gauge fixed point", False),
        ("current full Thomson matching", False),
    )

    exact_guards_pass = (
        action["Fmin_is_eigenframe_blind"]
        and not action["microscopic_compact_Hamiltonian_derived"]
        and shape["photon_speed_is_unchanged"]
        and shape["alpha_changes_continuously"]
        and operator_rank[
            "current_symmetries_leave_one_physical_marginal_modulus"
        ]
        and upstream_shape["alpha_changes_with_internal_shape"]
        and duality["family_contains_distinct_couplings"]
        and not critical[
            "renormalized_critical_coupling_is_universal_across_that_family"
        ]
        and not ordinary_rg["ordinary_screening_has_nonzero_fixed_point"]
        and not fixed["gravity_gauge_coefficient_derived"]
        and not fixed["current_Thomson_alpha_closed"]
    )

    return {
        "route_table": routes,
        "number_of_current_routes_audited": len(routes),
        "any_current_route_derives_unique_physical_alpha": any(
            passed for _, passed in routes
        ),
        "exact_guards_pass": exact_guards_pass,
        "strongest_closed_result": (
            "alpha at a declared compact-Coulomb scale is operationally the "
            "primitive flux/photon spectral ratio"
        ),
        "strongest_no_go": (
            "all presently derived RefG symmetries and integers survive a "
            "continuous physical stiffness deformation that changes alpha"
        ),
        "new_microscopic_information_is_required": True,
        "no_go_scope": "current RefG action and the candidate selectors listed here",
        "universal_future_alpha_prediction_is_impossible": False,
        "reference_value_used": False,
    }


def minimal_predictive_completion_contract() -> dict[str, object]:
    """State the smallest new block that would make the problem well posed."""

    requirements = (
        "derive compact links a_l modulo 2*pi and conjugate integer E_l from the substrate nodes",
        "derive the local Gauss operator and physical Hilbert space",
        "derive the complete primitive physical-Q charge lattice and global gauge-group quotient",
        "derive electric and magnetic defect spectra and any exact duality rather than assigning their integers",
        "derive one microscopic electric inertia and ring amplitude with no free dimensionless shape, or an isolated UV fixed point",
        "prove a deconfined 3+1D Coulomb phase with a massless transverse photon",
        "compute renormalized U_R/K_R by convergent finite-volume flux and photon spectra",
        "derive the complete charged spectrum, electroweak breaking, QCD and hadronic polarization",
        "run and match in one declared scheme to the Thomson limit",
        "freeze the prediction before any electromagnetic comparison",
    )
    return {
        "minimal_node_Hamiltonian": (
            "H_node=(U0/2) sum E_l^2+K0 sum_p(1-cos B_p)+"
            "H_charged_hopping+H_core"
        ),
        "canonical_link_algebra": "[a_l,E_l']=i delta_ll', a_l modulo 2*pi, E_l in Z",
        "Gauss_operator": "G_x=div E_x-rho_Q(x); physical states obey G_x|psi>=0",
        "adding_this_structure_alone_selects_U0_over_K0": False,
        "predictive_alternative_A": (
            "derive every coefficient from one microscopic substrate action "
            "and show no symmetry-allowed finite F^2 counterterm remains"
        ),
        "predictive_alternative_B": (
            "derive an isolated full UV fixed point whose critical surface has "
            "no free direction projected onto the physical photon stiffness"
        ),
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
                "an emergent compact photon and Gauss law do not make alpha "
                "universal; local microscopic deformations tune the coupling"
            ),
        },
        {
            "source": "https://arxiv.org/abs/hep-lat/0311006",
            "result": (
                "the helicity modulus measures the renormalized compact-U(1) "
                "coupling and supplies a counterexample to universal critical coupling"
            ),
        },
        {
            "source": "https://arxiv.org/abs/2307.12927",
            "result": (
                "generalized electric-magnetic self-equivalences exist at a "
                "family of rational couplings indexed by one-form gauging orders"
            ),
        },
        {
            "source": "https://arxiv.org/abs/2501.14419",
            "result": (
                "continuous gauging can realize non-invertible Maxwell self-duality "
                "at any coupling, so existence alone is not a number selector"
            ),
        },
        {
            "source": "https://arxiv.org/abs/1412.5148",
            "result": (
                "one-form symmetries act on line operators and are explicitly "
                "broken by dynamical objects carrying the corresponding charge"
            ),
        },
        {
            "source": "https://arxiv.org/abs/1705.01853",
            "result": (
                "the global form of the Standard-Model gauge group changes its "
                "allowed line operators and is not fixed by the local Lie algebra"
            ),
        },
        {
            "source": "https://arxiv.org/abs/1711.02949",
            "result": (
                "a gravity-gauge fixed point can conditionally predict a coupling, "
                "but its value depends on matter and gravitational fluctuations"
            ),
        },
        {
            "source": "https://arxiv.org/abs/1201.5868",
            "result": (
                "ordinary four-dimensional Abelian matter fluctuations give "
                "screening rather than an isolated nonzero perturbative root"
            ),
        },
        {
            "source": "https://arxiv.org/abs/2201.11402",
            "result": (
                "quantitative gravity contributions to gauge flows require a "
                "full fixed-point and truncation analysis rather than one imported coefficient"
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
        "p18bp_spin1_frame_electroweak_operator_gate",
        "p18bq_photon_rigidity_uv_normalization_matching_gate",
        "p18br_hs_auxiliary_link_origin_gate",
        "p18bs_unified_physical_q_fixed_point_gate",
        "p18bt_node_flux_photon_spectral_invariant_gate",
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
    action = current_action_compact_photon_no_go()
    shape = continuous_coulomb_shape_fibre_theorem()
    operator_rank = continuum_physical_q_operator_rank_theorem()
    duality = generalized_maxwell_duality_family_theorem()
    critical = compact_u1_criticality_nonuniversality_audit()
    ordinary_rg = ordinary_abelian_matter_fixed_point_no_go()
    fixed = fixed_point_and_thomson_underdetermination_audit()
    exhaustion = current_selector_exhaustion_theorem()
    completion = minimal_predictive_completion_contract()
    firewall = source_firewall()

    assert action["Fmin_is_eigenframe_blind"]
    assert action["Fmin_derives_frame_stiffness"] is False
    assert action["projective_ring_operator_is_symmetry_allowed"]
    assert action[
        "current_symmetry_forces_bare_ring_coefficient_to_zero"
    ] is False
    assert action[
        "current_ordered_frame_is_massless_Coulomb_photon"
    ] is False
    assert action[
        "composite_frame_curvature_has_quadratic_Maxwell_propagator"
    ] is False
    assert action["microscopic_compact_Hamiltonian_derived"] is False
    assert shape["photon_speed_is_unchanged"]
    assert shape["alpha_scales_by_lambda"]
    assert shape["alpha_changes_continuously"]
    assert shape["same_kinematics_and_topology_fix_alpha"] is False
    assert operator_rank["constraint_rank"] == 2
    assert operator_rank["allowed_coefficient_space_dimension"] == 1
    assert operator_rank[
        "current_symmetries_leave_one_physical_marginal_modulus"
    ]
    assert operator_rank[
        "alpha_changes_under_allowed_common_stiffness"
    ]
    assert duality["conditional_alpha_family"] == (
        sp.symbols("N_m", integer=True, positive=True)
        / (2 * sp.symbols("N_e", integer=True, positive=True))
    )
    assert duality["family_contains_distinct_couplings"]
    assert duality["physical_Q_Wilson_tHooft_lattice_derived_in_RefG"] is False
    assert duality[
        "existence_of_a_noninvertible_duality_alone_selects_alpha"
    ] is False
    assert critical["compact_period_is_preserved"]
    assert critical[
        "renormalized_critical_coupling_is_universal_across_that_family"
    ] is False
    assert ordinary_rg["ordinary_screening_has_nonzero_fixed_point"] is False
    assert ordinary_rg[
        "a_nonzero_selector_requires_new_antiscreening_or_higher_operator_dynamics"
    ]
    assert fixed["gravity_gauge_coefficient_derived"] is False
    assert fixed["unified_matter_coefficient_derived"] is False
    assert fixed["all_microscopic_and_matching_requirements_satisfied"] is False
    assert fixed["current_Thomson_alpha_closed"] is False
    assert exhaustion["exact_guards_pass"]
    assert exhaustion["any_current_route_derives_unique_physical_alpha"] is False
    assert exhaustion["universal_future_alpha_prediction_is_impossible"] is False
    assert completion["adding_this_structure_alone_selects_U0_over_K0"] is False
    assert completion["current_contract_satisfied"] is False
    assert firewall["target_isolation_pass"]

    for title, payload in (
        ("current-action compact-photon no-go", action),
        ("continuous Coulomb shape fibre", shape),
        ("continuum physical-Q operator rank", operator_rank),
        ("generalized Maxwell duality family", duality),
        ("compact-U(1) criticality nonuniversality", critical),
        ("ordinary Abelian matter fixed-point no-go", ordinary_rg),
        ("fixed-point and Thomson underdetermination", fixed),
        ("current selector exhaustion", exhaustion),
        ("minimal predictive completion", completion),
        ("source firewall", firewall),
    ):
        print(f"\n{title}")
        for key, value in payload.items():
            print(f"  {key}: {value}")

    print("\nprimary references")
    for row in primary_reference_ledger():
        print(f"  {row['source']}: {row['result']}")

    print(
        "\nSTATUS: OPEN_DERIVED_COMPACT_PHYSICAL_Q_NODE_ACTION_UNIQUE_"
        "STIFFNESS_OR_ISOLATED_FIXED_POINT_AND_COMPLETE_THOMSON_MATCHING__"
        "PASS_TARGET_INDEPENDENT_CURRENT_REFG_ALPHA_SELECTOR_EXHAUSTION_"
        "CONTINUOUS_SHAPE_FIBRE_GENERALIZED_DUALITY_FAMILY_CRITICAL_"
        "NONUNIVERSALITY_AND_MINIMAL_PREDICTIVE_COMPLETION_THEOREM"
    )


if __name__ == "__main__":
    run_gate()
