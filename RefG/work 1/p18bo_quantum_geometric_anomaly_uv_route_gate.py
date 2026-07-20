from __future__ import annotations

import ast
import inspect
import math

import sympy as sp

from p18h_frame_connection_u1_gate import (
    connection_curvature_and_holonomy,
)
from p18bh_boundary_slot_count_theorem_gate import (
    boundary_rank_nullity_theorem,
)
from p18bl_target_free_alpha_kernel_gate import (
    H_BRANCH,
    ORDER_NINE,
    QED_B1_THREE_LEPTONS,
    diagonal_sheet_normalization,
    exact_c3_mass_ratios,
    internal_inverse_alpha,
    lepton_only_matching_scope_guard,
    solve_boundary_relation,
    two_loop_lepton_precision_guard,
)


def spin1_coherent_state_qgt_theorem() -> dict[str, object]:
    """Derive the exact spin-1 QGT behind the p18h frame connection.

    The normalized state is the symmetric square of a spinor.  Its three
    components match the spin-1 representation dimension, its Berry bundle
    has first Chern number two, and its Berry connection is exactly the p18h
    tangent-frame connection.
    """

    def canonical_trig(expression: sp.Expr) -> sp.Expr:
        reduced = sp.trigsimp(expression, method="fu")
        return sp.trigsimp(sp.simplify(sp.expand_trig(reduced)), method="fu")

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
    norm = sp.trigsimp((state.H * state)[0])
    derivatives = (sp.diff(state, chi), sp.diff(state, phi))

    berry = sp.Matrix(
        [
            canonical_trig(-sp.I * (state.H * derivative)[0])
            for derivative in derivatives
        ]
    )

    qgt = sp.Matrix(
        2,
        2,
        lambda i, j: sp.trigsimp(
            (derivatives[i].H * derivatives[j])[0]
            - (derivatives[i].H * state)[0]
            * (state.H * derivatives[j])[0]
        ),
    )
    metric = sp.Matrix(
        2,
        2,
        lambda i, j: canonical_trig(
            sp.expand_complex(qgt[i, j]).as_real_imag()[0]
        ),
    )
    curvature = sp.trigsimp(
        sp.diff(berry[1], chi) - sp.diff(berry[0], phi)
    )
    chern_number = sp.simplify(
        sp.integrate(
            sp.integrate(curvature, (phi, 0, 2 * sp.pi)),
            (chi, 0, sp.pi),
        )
        / (2 * sp.pi)
    )

    expected_berry = sp.Matrix([0, 1 - sp.cos(chi)])
    expected_metric = sp.diag(sp.Rational(1, 2), sp.sin(chi) ** 2 / 2)
    metric_matches = all(
        canonical_trig(metric[i, j] - expected_metric[i, j]) == 0
        for i in range(2)
        for j in range(2)
    )
    berry_coefficient = sp.simplify(curvature / sp.sin(chi))
    metric_coefficient = metric[0, 0]
    qgt_ratio = sp.simplify(berry_coefficient**2 / metric_coefficient)
    p18h = connection_curvature_and_holonomy()

    return {
        "state": (
            "|n;1>=(cos^2(chi/2),sqrt(2)e^(i phi)sin(chi/2)"
            "cos(chi/2),e^(2i phi)sin^2(chi/2))"
        ),
        "state_dimension": state.rows,
        "state_normalized": sp.simplify(norm - 1) == 0,
        "berry_connection": berry,
        "berry_matches_p18h": all(
            canonical_trig(berry[i] - expected_berry[i]) == 0
            for i in range(2)
        )
        and p18h["curvature_is_area_form"],
        "quantum_metric": expected_metric if metric_matches else metric,
        "metric_is_spin1_Fubini_Study": metric_matches,
        "berry_curvature": curvature,
        "first_chern_number": chern_number,
        "C3_dimension_equals_2j_plus_1": state.rows == 3,
        "h_equals_first_chern_number": chern_number == H_BRANCH,
        "C3_cycle_derived_as_spin1_weight_action": False,
        "oriented_return_index_derived_as_Chern_class": False,
        "QGT_ratio_kBerry2_over_Kmetric": qgt_ratio,
        "QGT_ratio_equals_two": qgt_ratio == 2,
        "reference_value_used": False,
    }


def qgt_to_maxwell_bridge_guard() -> dict[str, object]:
    """Separate the exact state-space QGT ratio from the Maxwell invariant."""

    j, bridge_scale, counterterm = sp.symbols(
        "j lambda delta_F", positive=True
    )
    berry_coefficient = j
    qgt_metric_coefficient = j / 2
    maxwell_stiffness = bridge_scale * qgt_metric_coefficient
    source_coefficient = berry_coefficient
    q0_squared = sp.simplify(source_coefficient**2 / maxwell_stiffness)
    shifted_q0_squared = sp.simplify(
        source_coefficient**2 / (maxwell_stiffness + counterterm)
    )

    return {
        "exact_QGT_ratio": sp.simplify(
            berry_coefficient**2 / qgt_metric_coefficient
        ),
        "candidate_identification": (
            "k_J=k_Berry and K_F=K_QGT, with no extra F^2 term"
        ),
        "general_Maxwell_stiffness": maxwell_stiffness,
        "general_q0_squared": q0_squared,
        "spin1_candidate_q0_squared": sp.simplify(
            q0_squared.subs({j: 1, bridge_scale: 1})
        ),
        "same_topology_counterterm_q0_squared": shifted_q0_squared,
        "counterterm_changes_q0": sp.simplify(
            shifted_q0_squared - q0_squared
        )
        != 0,
        "QGT_metric_operator_order": "two derivatives: g_Q(dn,dn)",
        "composite_Maxwell_operator_order": (
            "four derivatives: F_B(n)_{mu nu} F_B(n)^{mu nu}"
        ),
        "Chern_number_unchanged_by_Maxwell_counterterm": True,
        "QGT_to_Maxwell_source_bridge_derived": False,
        "required_theorem": (
            "derive the frame effective action and prove lambda=1 and "
            "delta_F=0 in a fixed renormalization prescription"
        ),
        "reference_value_used": False,
    }


def one_u1_qgt_normalization_branch() -> dict[str, object]:
    """Compare the new one-U(1) candidate with the old two-sheet product."""

    two_sheet = diagonal_sheet_normalization(
        sheet_count=2,
        unit_sheet_ratio=1.0,
    )
    qgt_frame = diagonal_sheet_normalization(
        sheet_count=1,
        unit_sheet_ratio=2.0,
    )
    tau_over_e, muon_over_e = exact_c3_mass_ratios()
    Y_two_sheet = internal_inverse_alpha(
        tau_over_e,
        muon_over_e,
        two_sheet,
    )
    Y_qgt = internal_inverse_alpha(
        tau_over_e,
        muon_over_e,
        qgt_frame,
    )
    N = boundary_rank_nullity_theorem().kernel_dimension
    y_two_sheet = solve_boundary_relation(
        Y_two_sheet,
        N,
        boundary_matching_coefficient=QED_B1_THREE_LEPTONS,
    )
    y_qgt = solve_boundary_relation(
        Y_qgt,
        N,
        boundary_matching_coefficient=QED_B1_THREE_LEPTONS,
    )

    return {
        "old_interpretation": "n=2 additive sheets, eta_*=1",
        "QGT_interpretation": "one frame U(1), eta_QGT=|c1|=2",
        "old_q0_squared": two_sheet.q0_squared,
        "QGT_q0_squared": qgt_frame.q0_squared,
        "same_bare_inverse_alpha": math.isclose(
            two_sheet.bare_inverse_alpha,
            qgt_frame.bare_inverse_alpha,
            rel_tol=1.0e-15,
        ),
        "same_conditional_exact_C3_inverse_alpha": math.isclose(
            y_two_sheet,
            y_qgt,
            rel_tol=1.0e-15,
        ),
        "conditional_inverse_alpha": y_qgt,
        "avoids_helicity_as_sheet_count": True,
        "QGT_Maxwell_bridge_still_open": True,
        "reference_value_used": False,
    }


def boundary_inverse_level_candidate() -> dict[str, object]:
    """Audit the exact U(1)_34 anomaly response and its channel mismatch."""

    N = sp.Integer(boundary_rank_nullity_theorem().kernel_dimension)
    level = N
    primitive_mixed_charge = sp.Integer(1)
    inverse_level = sp.simplify(primitive_mixed_charge**2 / level)

    # Central-charge check for the conformal embedding
    # so(68)_1 contains so(34)_2 plus so(2)_34.
    dim_so68 = sp.Integer(68 * 67 // 2)
    dim_so34 = sp.Integer(34 * 33 // 2)
    c_so68_1 = sp.simplify(dim_so68 / (1 + 66))
    c_so34_2 = sp.simplify(2 * dim_so34 / (2 + 32))
    c_so2_34 = sp.Integer(1)

    return {
        "candidate_edge_content": "68 same-chirality Majoranas psi_(i,a)",
        "candidate_current": "J=i sum_(i=1)^34 psi_(i,1) psi_(i,2)",
        "current_algebra": "so(68)_1 contains so(34)_2 plus so(2)_34",
        "parent_central_charge": c_so68_1,
        "subalgebra_central_charges": (c_so34_2, c_so2_34),
        "central_charge_embedding_exact": (
            c_so68_1 == c_so34_2 + c_so2_34
        ),
        "topological_action": (
            "S=34/(4*pi) integral a da + 1/(2*pi) integral A_EM da"
        ),
        "K_matrix_level": level,
        "primitive_mixed_charge": primitive_mixed_charge,
        "integrated_response_tKinvT": inverse_level,
        "inverse_level_equals_one_over_34": inverse_level == sp.Rational(1, 34),
        "response_channel": "2+1D parity-odd Chern-Simons/anomaly response",
        "needed_channel": "3+1D parity-even Maxwell/vacuum-polarization matching",
        "K_kernel_is_not_a_34_state_chiral_Hilbert_space": True,
        "ordinary_34_species_loop_scales_as_34_not_one_over_34": True,
        "parity_doubling_can_cancel_Chern_Simons_response": True,
        "level34_microscopic_edge_content_present_in_current_action": False,
        "topological_to_Maxwell_matching_bridge_derived": False,
        "reference_value_used": False,
    }


def normalized_hidden_weight_guard() -> dict[str, object]:
    """Record why trace-one averaging is algebra, not yet a loop theorem."""

    N = sp.Integer(boundary_rank_nullity_theorem().kernel_dimension)
    sigma = sp.eye(int(N)) / N
    C = sp.zeros(int(N), 2)
    C[0, 0] = 1
    C[1, 1] = 1
    scalar_share = sp.simplify(sp.trace(C.T * sigma * C) / 2)

    return {
        "normalized_isotropic_weight": "sigma=I_N/N, Tr(sigma)=1",
        "unit_isometric_interface_share": scalar_share,
        "share_equals_one_over_34": scalar_share == sp.Rational(1, 34),
        "algebraic_alpha_share": "alpha*Tr(C^T sigma C)/2=alpha/34",
        "K_is_response_operator_space_not_state_Hilbert_space": True,
        "Ward_identity_fixes_vertex_conservation_not_spectral_residue": True,
        "conserved_current_spectral_weight_has_no_universal_unit_sum": True,
        "trace_one_response_measure_derived_from_current_action": False,
        "normalized_average_is_not_a_vacuum_loop_multiplicity": True,
        "reference_value_used": False,
    }


def full_electroweak_matching_obstruction() -> dict[str, object]:
    matching = lepton_only_matching_scope_guard()
    two_loop = two_loop_lepton_precision_guard()

    gY, g2, t = sp.symbols("g_Y g_2 t", positive=True)
    electromagnetic_inverse_square = sp.simplify(1 / gY**2 + 1 / g2**2)
    e = sp.symbols("e", positive=True)
    one_parameter_family = {
        gY: e * sp.sqrt(1 + t**2),
        g2: e * sp.sqrt(1 + t**2) / t,
    }
    family_residual = sp.simplify(
        electromagnetic_inverse_square.subs(one_parameter_family) - 1 / e**2
    )

    return {
        "above_EW_identity": "1/e^2=1/g_Y^2+1/g_2^2",
        "single_e_leaves_weak_angle_family": family_residual == 0,
        "free_family_parameter": "t=g_Y/g_2",
        "h2_is_not_weak_SU2": True,
        "C3_is_not_hypercharge_or_color_embedding": True,
        "SM_minus_lepton_shift_from_MZ_to_core": matching[
            "SM_minus_lepton_shift_from_MZ_to_core"
        ],
        "SM_shift_over_conditional_boundary": matching[
            "SM_minus_lepton_abs_over_boundary"
        ],
        "lepton_two_loop_shift": two_loop["two_loop_running_shift"],
        "two_loop_over_conditional_boundary": two_loop[
            "two_loop_over_boundary_shift"
        ],
        "complete_matching_requires": (
            "g_Y, g_2, g_3, Higgs/Yukawa data, W/Z/H/top thresholds, "
            "quark thresholds and nonperturbative hadronic vacuum polarization"
        ),
        "single_frame_U1_sufficient_above_EW": False,
        "precision_ready": False,
        "reference_value_used": False,
    }


def unified_uv_fixed_point_criterion() -> dict[str, object]:
    """State the only non-fitting way to remove the remaining coupling fibre."""

    C, B, y, omega = sp.symbols("C B y omega", positive=True)
    u, log_scale, finite = sp.symbols("u L Delta", real=True)
    D = sp.symbols("D", positive=True)
    sensitivity = sp.Matrix(
        [[C / D, B / D, 1 / D, -1 / (y * D)]]
    )

    counterterm = sp.symbols("delta_F", real=True)
    induced_stiffness = sp.symbols("K_induced", positive=True)
    total_stiffness = induced_stiffness + counterterm

    return {
        "reduced_relation": "y+omega/y=C*u+B*ln(Lambda)+Delta",
        "coefficient_order": (
            "u=1/g_U^2",
            "ln(Lambda)",
            "Delta_finite",
            "omega_boundary",
        ),
        "output_sensitivity_rank": sensitivity.rank(),
        "fixed_output_fibre_dimension": 4 - sensitivity.rank(),
        "induced_operator_candidate": (
            "Gamma[A,W,B]=k Gamma_WZ + (1/2) STr log(D^dagger D/Lambda^2)"
        ),
        "induced_plus_counterterm_stiffness": total_stiffness,
        "determinant_predictive_if_counterterm_free": False,
        "required_counterterm_theorem": (
            "derive a UV measure/renormalization condition that fixes the "
            "finite F^2 term rather than choosing it from alpha"
        ),
        "isolated_fixed_point_alternative": (
            "beta_i(g_*)=0 and no free relevant direction may project onto "
            "1/g_Y^2+1/g_2^2"
        ),
        "current_frame_EW_beta_system_present": False,
        "reference_value_used": False,
    }


def primary_reference_ledger() -> tuple[dict[str, str], ...]:
    return (
        {
            "result": "four-dimensional Abelian duality inverts the coupling",
            "source": "E. Witten, arXiv:hep-th/9505186",
        },
        {
            "result": "three-dimensional SL(2,Z) action and CS shift",
            "source": "E. Witten, arXiv:hep-th/0307041",
        },
        {
            "result": "spectral action gives high-scale gauge-coupling relations",
            "source": "A. Chamseddine and A. Connes, arXiv:hep-th/9606001",
        },
        {
            "result": "boundary response coefficients can vary with marginal couplings",
            "source": "C. Herzog and K.-W. Huang, arXiv:1707.06224",
        },
    )


def source_firewall() -> dict[str, object]:
    module = inspect.getmodule(source_firewall)
    source = inspect.getsource(module)
    forbidden_literals = (
        "COD" + "ATA",
        "OBS" + "ERVED",
        "137.03" + "5999177",
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
        "p18h_frame_connection_u1_gate",
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


def selected_research_route() -> tuple[str, ...]:
    return (
        "Use the exact spin-1 coherent-state bundle as the microscopic C3/h=2 frame object; it replaces the fictitious two-sheet interpretation by one U(1) with a candidate q0^2=|c1|=2.",
        "Derive, rather than postulate, the QGT-to-Maxwell bridge by integrating the complete gapped frame/core operator and proving that no independent finite F^2 counterterm remains.",
        "Test a genuine 2+1D core-surface anomaly sector for the inverse level 1/34; reject it unless its chirality, parity completion and parity-even Maxwell matching are derived.",
        "Embed the frame connection into a complete U(1)_Y x SU(2)_L charged spectrum and compute all thresholds in one scheme, without double-counting the boundary term.",
        "Introduce the comparison value only after the UV action, RG trajectory and matching coefficients are fixed.",
    )


def run_gate() -> None:
    qgt = spin1_coherent_state_qgt_theorem()
    bridge = qgt_to_maxwell_bridge_guard()
    branch = one_u1_qgt_normalization_branch()
    inverse_level = boundary_inverse_level_candidate()
    normalized_weight = normalized_hidden_weight_guard()
    electroweak = full_electroweak_matching_obstruction()
    fixed_point = unified_uv_fixed_point_criterion()
    firewall = source_firewall()

    assert qgt["state_dimension"] == 3
    assert qgt["state_normalized"]
    assert qgt["berry_matches_p18h"]
    assert qgt["metric_is_spin1_Fubini_Study"]
    assert qgt["first_chern_number"] == 2
    assert qgt["h_equals_first_chern_number"]
    assert qgt["C3_cycle_derived_as_spin1_weight_action"] is False
    assert qgt["oriented_return_index_derived_as_Chern_class"] is False
    assert qgt["QGT_ratio_equals_two"]
    assert bridge["spin1_candidate_q0_squared"] == 2
    assert bridge["counterterm_changes_q0"]
    assert bridge["Chern_number_unchanged_by_Maxwell_counterterm"]
    assert bridge["QGT_to_Maxwell_source_bridge_derived"] is False
    assert branch["old_q0_squared"] == 2.0
    assert branch["QGT_q0_squared"] == 2.0
    assert branch["same_bare_inverse_alpha"]
    assert branch["same_conditional_exact_C3_inverse_alpha"]
    assert branch["avoids_helicity_as_sheet_count"]
    assert inverse_level["central_charge_embedding_exact"]
    assert inverse_level["inverse_level_equals_one_over_34"]
    assert inverse_level[
        "level34_microscopic_edge_content_present_in_current_action"
    ] is False
    assert inverse_level["topological_to_Maxwell_matching_bridge_derived"] is False
    assert normalized_weight["share_equals_one_over_34"]
    assert normalized_weight[
        "trace_one_response_measure_derived_from_current_action"
    ] is False
    assert normalized_weight["normalized_average_is_not_a_vacuum_loop_multiplicity"]
    assert electroweak["single_e_leaves_weak_angle_family"]
    assert electroweak["single_frame_U1_sufficient_above_EW"] is False
    assert electroweak["SM_shift_over_conditional_boundary"] > 3000.0
    assert electroweak["two_loop_over_conditional_boundary"] > 100.0
    assert electroweak["precision_ready"] is False
    assert fixed_point["output_sensitivity_rank"] == 1
    assert fixed_point["fixed_output_fibre_dimension"] == 3
    assert fixed_point["current_frame_EW_beta_system_present"] is False
    assert firewall["runtime_reference_free"]

    print("p18bo quantum-geometric/anomaly UV route gate")
    print("spin-1 coherent-state QGT theorem")
    print(qgt)
    print()
    print("QGT-to-Maxwell bridge guard")
    print(bridge)
    print()
    print("one-U(1) QGT normalization branch")
    print(branch)
    print()
    print("boundary inverse-level candidate")
    print(inverse_level)
    print()
    print("normalized hidden-weight guard")
    print(normalized_weight)
    print()
    print("full electroweak matching obstruction")
    print(electroweak)
    print()
    print("unified UV/fixed-point criterion")
    print(fixed_point)
    print()
    print("primary reference ledger")
    for row in primary_reference_ledger():
        print(f"- {row}")
    print()
    print("selected research route")
    for item in selected_research_route():
        print(f"- {item}")
    print()
    print("source firewall")
    print(firewall)
    print()
    print(
        "STATUS: OPEN_QGT_MAXWELL_ANOMALY_PARITY_AND_FULL_EW_BRIDGES__"
        "PASS_TARGET_INDEPENDENT_MICROSCOPIC_ALPHA_ROUTE_SELECTION"
    )


if __name__ == "__main__":
    run_gate()
