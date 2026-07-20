# Notation:
# signature (+---); Y=g^mn Phi_m Phi_n;
# B^AB=-g^mn phi^A_m phi^B_n.

"""RefG -> Einstein bridge and layer-separation audit.

The theory-scope contract audited here is:

    RefG explains the physical mechanism that produces curvature;
    it does not replace the Einstein weak-field bridge by an independent
    extra-medium 1PN bridge.

That contract requires three distinct layers:

    U: substrate/mechanism variables and constitutive dynamics;
    M: integrate-out/matching map to the one effective metric and matter;
    E: the effective Einstein equation used for Solar/N-body 1PN and PPN.

Once the E layer is exactly Einstein, the standard GR 1PN/PPN solution is
inherited and must not be independently rebuilt.  Conversely, writing

    S_eff = S_EH + S_matter + S_F/H

and varying S_F/H as an additional nonzero effective stress is GR coupled to
an extra effective medium, with generally different solutions, unless that
sector is action-level stealth.  Calling a nonzero post-variation stress
"structural" does not remove it.

For the currently selected response,

    F_selected/c = Theta^2 - 16 det(E),
    Theta = Yhat + Tr(Bhat) - 4,
    E = I - Bhat,

the exact stationary-zero entrance is

    Theta=0, rank(E)<=1.

This includes a single Kerr-Schild direction exactly.  Two nonparallel
directions make rank(E)=2 and activate the cofactor at quadratic/1PN order in
the downstream-extra-sector reading.  This does not refute an upstream
substrate interpretation; it shows that the current F/H sector has not been
proved to be a universal auxiliary representation of arbitrary GR sources.

The executable outcome is deliberately layered:

* the same-GR-bridge architecture and no-double-count theorem pass;
* the standard GR 1PN handoff is exact under the declared effective-Einstein
  scope;
* the microscopic RefG -> Einstein-Hilbert matching derivation remains open;
* no article or selected-action replacement is authorized by this gate.
"""

from __future__ import annotations

from typing import Any

import sympy as sp

from p03g_source_first_1pn_closure_gate import (
    source_first_1pn_action_decision_gate,
)
from p05r_variational_no_double_count_projector_gate import (
    derive_variational_no_double_count_projector_gate,
)
from p15g_proper_inventory_adm_bridge_gate import (
    proper_inventory_adm_bridge_status,
)


def _all_zero(values) -> bool:
    flattened = []
    for value in values:
        if isinstance(value, sp.MatrixBase):
            flattened.extend(list(value))
        else:
            flattened.append(value)
    return all(sp.simplify(value) == 0 for value in flattened)


def effective_layer_no_double_count_theorem_gate() -> dict[str, Any]:
    """Prove when an extra mechanism sector changes the Einstein equation."""

    E_GR, T_mechanism = sp.symbols(
        "E_GR T_mechanism",
        real=True,
    )
    # E_GR abbreviates M_Pl^2 G_mn - T_mn component by component.
    pure_einstein_residual = E_GR
    downstream_extra_sector_residual = E_GR - T_mechanism
    downstream_on_einstein_solution = sp.simplify(
        downstream_extra_sector_residual.subs(E_GR, 0)
    )
    same_solution_condition = sp.solve(
        sp.Eq(downstream_on_einstein_solution, 0),
        T_mechanism,
    )

    eps, delta_2, delta_3 = sp.symbols(
        "eps delta_2 delta_3",
        real=True,
    )
    nominal_1pn_correction = eps**2 * delta_2
    beyond_nominal_1pn_correction = eps**3 * delta_3
    nominal_1pn_series = sp.series(
        nominal_1pn_correction,
        eps,
        0,
        3,
    ).removeO()
    beyond_1pn_series = sp.series(
        beyond_nominal_1pn_correction,
        eps,
        0,
        3,
    ).removeO()

    passed = (
        downstream_on_einstein_solution == -T_mechanism
        and same_solution_condition == [0]
        and nominal_1pn_series == delta_2 * eps**2
        and beyond_1pn_series == 0
    )

    return {
        "status": (
            "PASS_EFFECTIVE_LAYER_NO_DOUBLE_COUNT_THEOREM"
            if passed
            else "CHECK_EFFECTIVE_LAYER_NO_DOUBLE_COUNT"
        ),
        "Einstein_residual": pure_einstein_residual,
        "EH_plus_independent_mechanism_residual": (
            downstream_extra_sector_residual
        ),
        "extra_sector_residual_on_GR_solution": (
            downstream_on_einstein_solution
        ),
        "same_GR_solution_requires": sp.Eq(
            T_mechanism,
            same_solution_condition[0],
        ),
        "nominal_O_U2_correction_survives_1PN": nominal_1pn_series,
        "O_U3_correction_absent_through_nominal_1PN": beyond_1pn_series,
        "allowed_architectures": [
            "upstream: integrate out/match the mechanism into Gamma_eff and "
            "do not append it again as an independent effective RHS",
            "downstream: the necessary componentwise condition with the same "
            "fixed T_m is zero total extra stress; action-level sectorwise "
            "stationary stealth is one robust sufficient route, not the only "
            "possible cancellation/matching mechanism",
        ],
        "rejected_architecture": (
            "Einstein-Hilbert plus the same curvature mechanism as a second "
            "independently varied nonzero effective stress."
        ),
    }


def exact_selected_sector_einstein_entrance_gate() -> dict[str, Any]:
    """Derive the selected F/H sector's exact action-level stealth entrance."""

    Yhat, c = sp.symbols("Yhat c", real=True, nonzero=True)
    b11, b22, b33, b12, b13, b23 = sp.symbols(
        "b11 b22 b33 b12 b13 b23",
        real=True,
    )
    Bhat = sp.Matrix(
        [
            [b11, b12, b13],
            [b12, b22, b23],
            [b13, b23, b33],
        ]
    )
    E = sp.eye(3) - Bhat
    theta = sp.expand(Yhat + sp.trace(Bhat) - 4)
    F_selected = sp.expand(c * (theta**2 - 16 * sp.det(E)))
    F_Y = sp.diff(F_selected, Yhat)
    F_B = sp.Matrix(
        3,
        3,
        lambda i, j: sp.diff(F_selected, Bhat[i, j])
        if i == j
        else sp.diff(F_selected, Bhat[i, j]) / 2,
    )
    # Off-diagonal entries of a symmetric matrix occur twice in the expanded
    # scalar.  Dividing those coordinate derivatives by two recovers the
    # symmetric matrix derivative.
    expected_F_B = sp.simplify(
        c * (2 * theta * sp.eye(3) + 16 * E.cofactor_matrix())
    )
    F_B_residual = (F_B - expected_F_B).applyfunc(sp.simplify)

    lam = sp.Symbol("lambda", real=True)
    v1, v2, v3 = sp.symbols("v1 v2 v3", real=True)
    v = sp.Matrix([v1, v2, v3])
    E_rank_one = lam * v * v.T
    B_rank_one = sp.eye(3) - E_rank_one
    Y_rank_one = sp.simplify(1 + sp.trace(E_rank_one))
    rank_one_subs = {
        Yhat: Y_rank_one,
        **{
            Bhat[i, j]: B_rank_one[i, j]
            for i in range(3)
            for j in range(i, 3)
        },
    }
    rank_one_values = {
        "Theta": sp.simplify(theta.subs(rank_one_subs)),
        "F": sp.simplify(F_selected.subs(rank_one_subs)),
        "F_Y": sp.simplify(F_Y.subs(rank_one_subs)),
        "F_B": sp.simplify(F_B.subs(rank_one_subs)),
        "Cof_E": sp.simplify(E_rank_one.cofactor_matrix()),
        "det_E": sp.simplify(E_rank_one.det()),
    }

    # The projected H sector uses
    # Z_H=(Phi.H)^2/Y-(H.H).  If dH=q*dPhi, every current and metric
    # derivative cancels before the field equation is evaluated.
    q, a_H = sp.symbols("q a_H", real=True, nonzero=True)
    Y = sp.Symbol("Y", positive=True, real=True)
    X = q * Y
    K = q**2 * Y
    Z_H = sp.simplify(X**2 / Y - K)
    H_current_along_Phi = sp.simplify(
        -2 * a_H * X / Y + 2 * a_H * q
    )
    Phi_current_along_Phi = sp.simplify(
        -2 * a_H * X * q / Y + 2 * a_H * X**2 / Y**2
    )
    metric_derivative_along_PhiPhi = sp.simplify(
        2 * X * q / Y - X**2 / Y**2 - q**2
    )

    passed = (
        sp.simplify(F_Y - 2 * c * theta) == 0
        and _all_zero(F_B_residual)
        and _all_zero(rank_one_values.values())
        and Z_H == 0
        and H_current_along_Phi == 0
        and Phi_current_along_Phi == 0
        and metric_derivative_along_PhiPhi == 0
    )

    return {
        "status": (
            "PASS_EXACT_SELECTED_SECTOR_EINSTEIN_ENTRANCE__"
            "THETA_ZERO_RANK_E_AT_MOST_ONE_AND_H_PARALLEL_PHI"
            if passed
            else "CHECK_EXACT_SELECTED_SECTOR_EINSTEIN_ENTRANCE"
        ),
        "F_selected": F_selected,
        "Theta": theta,
        "E": E,
        "F_Yhat": F_Y,
        "F_Bhat": F_B,
        "F_Bhat_expected": expected_F_B,
        "F_Bhat_residual": F_B_residual,
        "stationary_zero_F_conditions_for_c_nonzero": [
            "Theta=0",
            "Cof(E)=0, equivalently rank(E)<=1 for a 3x3 matrix",
        ],
        "rank_one_exact_witness": {
            "E": E_rank_one,
            "Bhat": B_rank_one,
            "Yhat": Y_rank_one,
            "evaluated_density_and_first_variations": rank_one_values,
        },
        "projected_H_exact_stealth_condition": "dH=q*dPhi, i.e. H=H(Phi) locally",
        "projected_H_checks": {
            "Z_H": Z_H,
            "H_current_along_Phi": H_current_along_Phi,
            "Phi_current_along_Phi": Phi_current_along_Phi,
            "metric_derivative_along_PhiPhi": metric_derivative_along_PhiPhi,
        },
        "coordinate_form": {
            "g^00": "exp(2H)*(1+Tr(E))",
            "g^AB": "-exp(-2H)*(delta^AB-E^AB)",
            "g^0A": (
                "cross/readout components C^A not fixed by F, but constrained "
                "by Lorentz signature, nondegeneracy and the physical chart domain"
            ),
            "conditions": "rank(E)<=1 and H=H(X^0)",
            "physical_domain_guard": (
                "Yhat>0, Bhat positive on the material spatial sector, "
                "full-rank scalar chart and nondegenerate Lorentzian metric"
            ),
        },
        "meaning": (
            "On this entrance the F and projected-H densities, metric stresses "
            "and Phi/phi/H currents vanish before variation is evaluated.  The "
            "remaining metric equation is exactly Einstein's.  Existence of "
            "such a full-rank scalar chart for every source is a separate PDE "
            "and matching theorem."
        ),
    }


def selected_entrance_singular_variety_gate() -> dict[str, Any]:
    """Explain why the missing entrance conditions first appear at 1PN."""

    e11, e22, e33, e12, e13, e23 = sp.symbols(
        "e11 e22 e33 e12 e13 e23",
        real=True,
    )
    variables = (e11, e22, e33, e12, e13, e23)
    E = sp.Matrix(
        [
            [e11, e12, e13],
            [e12, e22, e23],
            [e13, e23, e33],
        ]
    )
    cofactor = E.cofactor_matrix()
    independent_cofactors = sp.Matrix(
        [
            cofactor[0, 0],
            cofactor[1, 1],
            cofactor[2, 2],
            cofactor[0, 1],
            cofactor[0, 2],
            cofactor[1, 2],
        ]
    )
    jacobian = independent_cofactors.jacobian(variables)
    unit_point = {value: 0 for value in variables}
    lam = sp.Symbol("lambda", real=True, nonzero=True)
    rank_one_point = {
        e11: lam,
        e22: 0,
        e33: 0,
        e12: 0,
        e13: 0,
        e23: 0,
    }
    unit_rank = jacobian.subs(unit_point).rank()
    rank_one_rank = jacobian.subs(rank_one_point).rank()
    cofactor_degree = min(
        sp.Poly(value, variables).total_degree()
        for value in independent_cofactors
        if value != 0
    )

    passed = (
        unit_rank == 0
        and rank_one_rank == 3
        and cofactor_degree == 2
    )

    return {
        "status": (
            "PASS_SELECTED_ENTRANCE_SINGULAR_AT_MINKOWSKI__"
            "THREE_MISSING_CONDITIONS_ACTIVATE_QUADRATICALLY"
            if passed
            else "CHECK_SELECTED_ENTRANCE_SINGULAR_VARIETY"
        ),
        "E": E,
        "independent_Cof_E_components": independent_cofactors,
        "Cof_E_Jacobian": jacobian,
        "Jacobian_rank_at_E_zero": unit_rank,
        "Jacobian_rank_at_nonzero_rank_one_E": rank_one_rank,
        "cofactor_polynomial_degree": cofactor_degree,
        "meaning": (
            "At Minkowski the cofactor conditions have zero linearization.  "
            "The linear audit therefore sees only Theta=0; three additional "
            "label/coordinate conditions become visible first at quadratic "
            "field-equation order, i.e. the audited 1PN level.  An ordinary "
            "implicit-function theorem cannot be invoked at E=0."
        ),
    }


def kerr_schild_single_vs_multidirection_entrance_gate() -> dict[str, Any]:
    """Show the exact single-direction entrance and the two-direction source."""

    V, V1, V2, c = sp.symbols(
        "V V1 V2 c",
        real=True,
        nonzero=True,
    )

    E_single = sp.diag(V, 0, 0)
    B_single = sp.eye(3) - E_single
    Y_single = 1 + V
    theta_single = sp.simplify(Y_single + sp.trace(B_single) - 4)
    F_single_over_c = sp.simplify(
        theta_single**2 - 16 * E_single.det()
    )
    single_cofactor = E_single.cofactor_matrix()

    E_two = sp.diag(V1, V2, 0)
    B_two = sp.eye(3) - E_two
    Y_two = 1 + V1 + V2
    theta_two = sp.simplify(Y_two + sp.trace(B_two) - 4)
    F_two_over_c = sp.simplify(theta_two**2 - 16 * E_two.det())
    two_cofactor = E_two.cofactor_matrix()
    F_B_two = sp.simplify(16 * c * two_cofactor)
    H_algebraic_source_two = sp.simplify(32 * c * sp.trace(two_cofactor))

    passed = (
        theta_single == 0
        and F_single_over_c == 0
        and _all_zero(single_cofactor)
        and theta_two == 0
        and F_two_over_c == 0
        and two_cofactor[2, 2] == V1 * V2
        and F_B_two[2, 2] == 16 * c * V1 * V2
        and H_algebraic_source_two == 32 * c * V1 * V2
    )

    return {
        "status": (
            "PASS_SINGLE_KERR_SCHILD_DIRECTION_EXACT_ENTRANCE__"
            "TWO_DIRECTION_DOWNSTREAM_COFACTOR_ACTIVE"
            if passed
            else "CHECK_KERR_SCHILD_ENTRANCE"
        ),
        "single_direction": {
            "inverse_metric_form": "g^mn=eta^mn+V*l^m*l^n, l=(1,n), |n|=1",
            "E": E_single,
            "Yhat": Y_single,
            "Theta": theta_single,
            "F_over_c": F_single_over_c,
            "Cof_E": single_cofactor,
            "physical_single_direction_domain": (
                "Yhat=1+V>0 and Bhat=diag(1-V,1,1) positive definite, "
                "hence -1<V<1 in this normalized weak-solid chart"
            ),
            "reading": (
                "A single Kerr-Schild direction, including the usual "
                "Schwarzschild/Kerr class in an adapted H=constant chart, lies "
                "pointwise on the selected stationary-zero F entrance wherever "
                "the clock is timelike, Bhat is positive definite, the material "
                "chart is full-rank and the Lorentzian metric is nondegenerate."
            ),
        },
        "two_nonparallel_directions": {
            "E_in_adapted_basis": E_two,
            "Yhat": Y_two,
            "Theta": theta_two,
            "F_over_c": F_two_over_c,
            "Cof_E": two_cofactor,
            "F_Bhat": F_B_two,
            "H_algebraic_source": H_algebraic_source_two,
        },
        "scope": (
            "This is an exact downstream-extra-sector diagnostic in the "
            "displayed label chart.  It does not prove that no alternative "
            "full-rank label/clock embedding exists, and it is not an "
            "objection to an upstream mechanism that is integrated into the "
            "Einstein effective action."
        ),
    }


def worldtube_source_replacement_handoff_gate() -> dict[str, Any]:
    """Define the weakest source contract needed before importing GR 1PN.

    Exact auxiliary stealth inside matter is stronger than necessary.  It is
    sufficient, once independently derived, that the full RefG source be
    conserved, counted once, matched to each body's ADM mass/current moments,
    and leave the standard Einstein equation outside the source worldtubes.
    This gate checks only the no-double-count algebra and records the remaining
    physical premises; it does not derive them.
    """

    M_ADM_matched = sp.Symbol(
        "m_A_isolated_ADM_or_Noether",
        real=True,
    )
    M_preinserted_GR = sp.Symbol("M_preinserted_GR", real=True)
    once_counted_charge = M_ADM_matched
    duplicated_charge = sp.expand(M_preinserted_GR + M_ADM_matched)
    duplicate_subs = {M_preinserted_GR: M_ADM_matched}
    duplicated_same_source = sp.simplify(
        duplicated_charge.subs(duplicate_subs)
    )
    duplicate_excess = sp.simplify(
        duplicated_same_source - once_counted_charge
    )

    Delta_T_ext = sp.Symbol("Delta_T_ext_through_1PN", real=True)
    exterior_einstein_residual = sp.Symbol(
        "M_Pl^2*G_ext",
        real=True,
    ) - Delta_T_ext
    vacuum_exterior_residual = sp.simplify(
        exterior_einstein_residual.subs(Delta_T_ext, 0)
    )

    passed = (
        duplicated_same_source == 2 * M_ADM_matched
        and duplicate_excess == M_ADM_matched
        and vacuum_exterior_residual
        == sp.Symbol("M_Pl^2*G_ext", real=True)
    )

    return {
        "status": (
            "PASS_WORLD_TUBE_NO_DOUBLE_COUNT_CONTRACT_ALGEBRA__"
            "PHYSICAL_ADM_MATCHING_AND_EFFACEMENT_OPEN"
            if passed
            else "CHECK_WORLD_TUBE_SOURCE_HANDOFF"
        ),
        "RefG_total_source_charge_counted_once": once_counted_charge,
        "internal_component_warning": (
            "Do not write M_core+M_deficit+M_dressing as an additive identity "
            "until the full action proves that these are disjoint renormalized "
            "contributions rather than different ledgers/readouts of one energy."
        ),
        "rejected_preinserted_matter_plus_same_mechanism_charge": (
            duplicated_charge
        ),
        "same_source_double_count_result": duplicated_same_source,
        "double_count_excess": duplicate_excess,
        "exterior_equation_before_matching": exterior_einstein_residual,
        "required_exterior_condition": sp.Eq(Delta_T_ext, 0),
        "exterior_equation_after_matching": vacuum_exterior_residual,
        "physical_premises_not_derived_by_this_algebra": [
            "inside each worldtube use one conserved total RefG stress ledger",
            "match the isolated-body ADM/Noether mass to the worldline mass "
            "coefficient; N-body ADM mass itself is a global charge",
            "match every source moment required by the claimed PPN matter "
            "class, not only monopole, momentum and spin",
            "do not also insert the same body's pre-existing GR matter source",
            "outside worldtubes leave no independent long-range medium stress "
            "through the claimed 1PN order",
            "leave no direct H/label fifth force or nonminimal preferred-frame "
            "worldline coupling through 1PN",
            "show finite-size and higher-multipole operators enter beyond the "
            "claimed order or match their GR values",
            "then use the standard Einstein/EIH N-body bridge with the matched charges",
        ],
        "important_scope": (
            "This avoids demanding exact F/H stealth at every interior point. "
            "The executable identities above do not derive conservation, "
            "effacement, minimal worldline coupling or PN order of finite-size "
            "operators.  The current files also have not derived the full "
            "action-level internal inventory to ADM/Noether charge equality."
        ),
    }


def current_workspace_layer_boundary_gate() -> dict[str, Any]:
    """Bind the new layer reading to existing executable open-status gates."""

    p03g = source_first_1pn_action_decision_gate()
    p05r = derive_variational_no_double_count_projector_gate()
    p15g = proper_inventory_adm_bridge_status()

    p03g_formal = p03g["formal_stealth_implication_gate"]
    checks = {
        "p03g_downstream_generic_Nbody_not_closed": not p03g_formal[
            "current_selected_p05z_full_N_body_1PN_closed"
        ],
        "p03g_article_export_blocked": not p03g["article_export_allowed"],
        "p05r_postvariation_deletion_rejected": p05r[
            "variational_projector_status"
        ]
        == "REJECTED_POST_VARIATION_PROJECTOR_NOT_ACTION_MECHANISM__USE_P05S",
        "p15g_full_action_map_open": p15g["status"]
        == "PASS_PROPER_INVENTORY_ADM_BRIDGE_AUDIT__FULL_ACTION_MAP_OPEN",
    }
    passed = all(checks.values())

    return {
        "status": (
            "PASS_EXISTING_GATES_COMPATIBLE_WITH_DECLARED_LAYER_SEPARATION"
            if passed
            else "CHECK_WORKSPACE_LAYER_BOUNDARY"
        ),
        "checks": checks,
        "p03g_status": p03g["status"],
        "p05r_status": p05r["variational_projector_status"],
        "p15g_status": p15g["status"],
        "p03g_reclassification": (
            "Its finite-source/cofactor result is a failure of the current "
            "downstream independent-extra-sector GR continuation.  It is not "
            "a reason to replace an upstream substrate action before the "
            "substrate-to-Einstein matching map is defined.  This reading is "
            "introduced by the newly declared layer architecture; the older "
            "gates are compatible with it but did not derive it."
        ),
    }


def standard_gr_1pn_handoff_gate() -> dict[str, Any]:
    """Record the GR consequence of the full effective-Einstein postulate."""

    Delta_E = sp.Symbol("Delta_E_effective", real=True)
    effective_residual = sp.Symbol("M_Pl^2*G_mn-T_mn", real=True) + Delta_E
    exact_einstein_subs = {Delta_E: 0}
    handoff_residual = sp.simplify(
        effective_residual.subs(exact_einstein_subs)
    )
    ppn_gr_targets = {
        "gamma": 1,
        "beta": 1,
        "xi": 0,
        "alpha_1": 0,
        "alpha_2": 0,
        "alpha_3": 0,
        "zeta_1": 0,
        "zeta_2": 0,
        "zeta_3": 0,
        "zeta_4": 0,
    }
    passed = handoff_residual == sp.Symbol(
        "M_Pl^2*G_mn-T_mn",
        real=True,
    )

    return {
        "status": (
            "PASS_LOGICAL_HANDOFF_FROM_POSTULATED_MINIMAL_EINSTEIN_EFFECTIVE_"
            "ACTION_TO_STANDARD_GR_1PN__REFG_MATCHING_DERIVATION_OPEN"
            if passed
            else "CHECK_STANDARD_GR_1PN_HANDOFF"
        ),
        "effective_equation_contract": (
            "Postulate/target: Gamma_eff[g,matter]=S_EH[g]+"
            "S_matter^minimal[g,matter] at the audited weak-field orders, "
            "with conserved total stress, standard compact-body worldline "
            "coupling, no extra long-range charge/nonminimal preferred-frame "
            "operator, and no separately appended duplicate mechanism stress"
        ),
        "premises_derived_from_current_RefG_action": False,
        "effective_residual_before_matching": effective_residual,
        "exact_Einstein_matching": sp.Eq(Delta_E, 0),
        "residual_after_matching": handoff_residual,
        "standard_GR_PPN_values_if_all_effective_premises_hold": ppn_gr_targets,
        "scientific_use": (
            "The RefG calculation ends at the equality of effective field "
            "equations.  The EIH/standard-PPN calculation belongs to GR and is "
            "then cited and reused rather than rebuilt with a parallel ansatz. "
            "The current gate proves this logical implication, not that RefG "
            "has already derived every premise of the effective action."
        ),
    }


def microscopic_to_einstein_matching_contract_gate() -> dict[str, Any]:
    """State exactly what must be derived for RefG to explain curvature."""

    requirements = {
        "emergent_metric_dictionary_from_substrate": False,
        "diffeomorphism_Ward_identity_and_Bianchi_consistency": False,
        "Einstein_Hilbert_two_derivative_term_and_M_Pl_normalization": False,
        "universal_minimal_matter_coupling_or_equivalence_principle": False,
        "extra_scalar_solid_H_modes_gauge_constrained_or_gapped": False,
        "bound_state_worldtubes_integrated_to_ADM_mass_and_spin": False,
        "no_independent_H_or_label_charge_through_1PN": False,
        "no_preferred_frame_worldline_operator_through_1PN": False,
        "higher_derivative_and_nonlocal_corrections_bounded_beyond_1PN": False,
        "matter_inventory_pressure_deficit_and_ADM_charge_counted_once": False,
    }
    matching_closed = all(requirements.values())

    return {
        "status": (
            "PASS_MICROSCOPIC_TO_EINSTEIN_MATCHING"
            if matching_closed
            else "OPEN_MICROSCOPIC_TO_EINSTEIN_MATCHING__"
            "SAME_GR_BRIDGE_CONTRACT_DEFINED"
        ),
        "declared_theory_scope": (
            "RefG is a mechanism/refinement of GR curvature, not an "
            "independent extra-medium weak-field equation."
        ),
        "required_derivations": requirements,
        "matching_closed": matching_closed,
        "effective_action_target": (
            "Gamma_eff = integral sqrt(-g)[M_Pl^2 R/2 + L_matter] "
            "+ corrections proven irrelevant at the claimed scale"
        ),
        "minimal_compact_body_1PN_target": (
            "S_eff^(through 1PN)=S_EH-sum_A m_A^ADM*Integral(ds_A), "
            "with spin terms when retained, no long-range H/label charge and "
            "no preferred-frame worldline operator; finite-size operators "
            "start beyond the claimed order"
        ),
        "uniqueness_route_under_standard_assumptions": [
            "one universal Lorentzian metric",
            "diffeomorphism invariance and local stress conservation",
            "local two-derivative metric dynamics",
            "only the two massless tensor helicities in the weak domain",
            "universal matter coupling",
            "then the leading metric action is Einstein-Hilbert plus "
            "cosmological/boundary terms",
        ],
        "important_boundary": (
            "This gate defines the target and prevents double counting.  It "
            "does not pretend that the present effective-medium Python family "
            "has already derived the metric, M_Pl or Einstein-Hilbert action "
            "from the pre-spacetime substrate."
        ),
    }


def refg_same_gr_bridge_decision_gate() -> dict[str, Any]:
    """Top-level ledger for the user's GR-refinement definition."""

    no_double = effective_layer_no_double_count_theorem_gate()
    exact_entrance = exact_selected_sector_einstein_entrance_gate()
    singular_entrance = selected_entrance_singular_variety_gate()
    kerr_schild = kerr_schild_single_vs_multidirection_entrance_gate()
    worldtube = worldtube_source_replacement_handoff_gate()
    workspace = current_workspace_layer_boundary_gate()
    handoff = standard_gr_1pn_handoff_gate()
    matching = microscopic_to_einstein_matching_contract_gate()

    matching_status_valid = matching["status"].startswith(
        ("OPEN_", "PASS_")
    )
    audit_pass = (
        no_double["status"].startswith("PASS_")
        and exact_entrance["status"].startswith("PASS_")
        and singular_entrance["status"].startswith("PASS_")
        and kerr_schild["status"].startswith("PASS_")
        and worldtube["status"].startswith("PASS_")
        and workspace["status"].startswith("PASS_")
        and handoff["status"].startswith("PASS_")
        and matching_status_valid
    )
    if audit_pass and matching["matching_closed"]:
        top_status = (
            "PASS_REFG_AS_GR_CURVATURE_MECHANISM_ARCHITECTURE_AUDIT__"
            "STANDARD_GR_1PN_HANDOFF__MICRO_TO_EH_BRIDGE_CLOSED"
        )
    elif audit_pass:
        top_status = (
            "PASS_REFG_AS_GR_CURVATURE_MECHANISM_ARCHITECTURE_AUDIT__"
            "USE_STANDARD_GR_1PN_AFTER_MATCHING__MICRO_TO_EH_BRIDGE_OPEN"
        )
    else:
        top_status = "CHECK_REFG_SAME_GR_BRIDGE_ARCHITECTURE"

    return {
        "status": top_status,
        "effective_1PN_status": (
            "CONDITIONAL_STANDARD_GR_1PN_TARGET_FROM_DECLARED_MINIMAL_"
            "EINSTEIN_EFFECTIVE_SCOPE__REFG_MATCHING_NOT_YET_DERIVED"
        ),
        "current_mechanism_derivation_status": matching["status"],
        "core_decision": (
            "Treat F_min/H/pressure-deficit dynamics as upstream mechanism or "
            "as an exactly auxiliary representation.  Do not add their "
            "nonzero stress to an Einstein equation that already represents "
            "the same curvature response."
        ),
        "what_is_established_by_this_architecture_audit": [
            "the no-double-count variational logic",
            "the exact stationary-zero entrance of the selected F/H sector",
            "why three entrance conditions are invisible linearly and activate at 1PN",
            "the single Kerr-Schild exact witness and multidirection cofactor diagnostic",
            "the once-counted worldtube/ADM-charge handoff contract and its "
            "still-open physical premises",
            "the logical handoff rule to standard GR 1PN once every effective "
            "action and source premise is independently matched",
        ],
        "what_remains_open": [
            "derive the substrate-to-effective-metric map",
            "derive Einstein-Hilbert normalization and universal coupling",
            "eliminate, constrain or gap every extra weak-field mode",
            "prove arbitrary-source matching or integrate the mechanism out",
            "derive the one-time core/deficit/dressing to ADM/Noether charge map",
            "reclassify non-vacuum/extra-effective-source strong-field branches "
            "as internal matching ansatzes or separately declared physical sectors",
        ],
        "selected_action_replacement_authorized": False,
        "article_export_allowed": False,
        "no_double_count_gate": no_double,
        "exact_selected_entrance_gate": exact_entrance,
        "singular_entrance_variety_gate": singular_entrance,
        "kerr_schild_gate": kerr_schild,
        "worldtube_source_handoff_gate": worldtube,
        "workspace_boundary_gate": workspace,
        "standard_GR_handoff_gate": handoff,
        "microscopic_matching_gate": matching,
        "audit_completed": audit_pass,
    }


def main() -> int:
    result = refg_same_gr_bridge_decision_gate()
    print("status:", result["status"])
    print("effective 1PN:", result["effective_1PN_status"])
    print("mechanism derivation:", result["current_mechanism_derivation_status"])
    print("core decision:", result["core_decision"])
    print(
        "selected action replacement authorized:",
        result["selected_action_replacement_authorized"],
    )
    print("article export allowed:", result["article_export_allowed"])
    return 0 if result["audit_completed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
