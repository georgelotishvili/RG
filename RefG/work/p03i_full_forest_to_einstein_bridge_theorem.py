# Notation:
# signature (+---);
# Y=g^mn Phi_m Phi_n;
# u^m=g^mn Phi_n/sqrt(Y);
# C^A=u^m phi^A_m;
# B^AB=-g^mn phi^A_m phi^B_n.

"""RefG material-response -> Einstein target construction and axiom audit.

Purpose
-------
The user's scope statement is that RefG refines GR by supplying a physical
mechanism for curvature; it does not replace the Einstein equation by a
parallel weak-field theory.  This file constructs the strongest exact
kinematic dictionary and parametrized-GR target available under that
definition, and separates them from the still absent physical matching and
pre-spacetime microscopic derivation.

The exact local material-chart dictionary uses the four operational labels

    q^I=(Phi, phi^A),                  I=0,1,2,3,

and their full symmetric response/Gram matrix

    K^{IJ}=g^{mn} q^I_m q^J_n
          = [[Y, sqrt(Y) C^B],
             [sqrt(Y) C^A, -B^{AB}]].

If the material chart is full rank, K contains all ten components of one
Lorentzian metric in that chart.  This is a local kinematic dictionary, not
yet a derivation of K from the RefG substrate.  It is not merely a scalar
refractive index:

    g_mn = q^I_m (K^{-1})_IJ q^J_n.

In material coordinates q^I themselves, K^{IJ}=g^{IJ}.  The exact ADM
dictionary is

    N=Y^{-1/2},
    N^A=-C^A/sqrt(Y),
    h^{AB}=B^{AB}+C^A C^B.

Thus the local response components sufficient to represent a generic metric
in a regular material chart are:

    one clock/lapse response + three flow/shift responses
    + six spatial strain/shear responses.

The scalar pressure-deficit H is the isotropic, comoving specialization.  On
the branch Y=e^(2H), C^A=0, B^AB=e^(-2H) delta^AB one obtains exactly

    ds^2=e^(-2H)dt^2-e^(2H)d x^2,
    phi=-2H, p=e^(-H).

An Einstein-equivalent parametrized continuum action can then be defined as
the Einstein-Hilbert action written as a functional of K and q through the
metric above.  At fixed full-rank q, the map K <-> g is invertible.  If q is
kept as a pure relational coordinate/Stueckelberg variable and the action
depends only on the reconstructed metric, the accompanying relabeling
redundancy makes this defined parent action exactly GR.  This is an exact
representation construction; it is not evidence that the current F_min/H
action generated Einstein-Hilbert.

Within that defined parametrized-GR completion, the no-double-count rule is
exact: H/pressure/strain are metric readouts or already-integrated upstream
variables.  They are not appended once more as a separately varied nonzero
stress after the Einstein response has already been written.  This statement
does not by itself establish that the independently varied current F_min/H
action has already reached that completion.

Current formal boundary
-----------------------
The current RefG formalism assigns no spacetime-local x, t, fields, pressure,
metric or spacetime action to the operationally undifferentiated foundation.
A pre-geometric relational state space and its self-distinction dynamics have
not yet been formulated.  Consequently the current variables do not yet
supply a transition law from the foundation to a first stable operational
distinction, then to a node--imprint--relation network, and finally to a
full-rank Lorentzian response matrix K.  Covariance and the scalar p/p^2
readout alone also do not select Einstein-Hilbert over, for example,
EH+alpha R^2.

Accordingly this file proves:

* the full-rank material-chart response -> metric dictionary exactly;
* an exact parametrized-GR parent-action construction and its GR 1PN handoff;
* the one-factor redshifted static Killing-energy readout from minimal coupling;
* the non-injectivity of the selected Y/I_k invariant subset for recovering
  all fixed-chart metric components;
* the logical underdetermination of the pre-spacetime -> universal-K step.

The physical links remain separate from the construction: foundation to first
stable distinction; first distinction to the manifested nodal network;
oscillon dynamics to the pressure-deficit profile; pressure deficit to the
full K response; current F_min/H dynamics to the Einstein parent without
extra long-range modes or duplicate stress; and the compact-worldtube map
from RefG source inventory to the ADM/worldline coefficients used by the
standard 1PN EFT.  No article file is modified or authorized by this gate.
"""

from __future__ import annotations

from typing import Any

import sympy as sp

from p03h_einstein_bridge_layer_separation_gate import (
    effective_layer_no_double_count_theorem_gate,
    standard_gr_1pn_handoff_gate,
    worldtube_source_replacement_handoff_gate,
)


def _all_zero(values) -> bool:
    flattened: list[sp.Expr] = []
    for value in values:
        if isinstance(value, sp.MatrixBase):
            flattened.extend(list(value))
        else:
            flattened.append(value)
    return all(sp.simplify(value) == 0 for value in flattened)


def full_material_response_metric_dictionary_gate() -> dict[str, Any]:
    """Prove the local metric dictionary carried by (Y,C^A,B^AB).

    C^A is the normalized convective response u.d(phi^A), so the raw mixed
    Gram entry is C_raw^A=sqrt(Y) C^A.  In the material chart q^I, compare K
    directly with the inverse-ADM metric.  The reconstruction in an arbitrary
    chart follows by the invertible Jacobian J^I_m=d_m q^I.
    """

    Y = sp.Symbol("Y", positive=True)
    c1, c2, c3 = sp.symbols("C_1 C_2 C_3", real=True)
    C = sp.Matrix([c1, c2, c3])
    b11, b22, b33, b12, b13, b23 = sp.symbols(
        "B_11 B_22 B_33 B_12 B_13 B_23",
        real=True,
    )
    B = sp.Matrix(
        [
            [b11, b12, b13],
            [b12, b22, b23],
            [b13, b23, b33],
        ]
    )

    C_raw = sp.sqrt(Y) * C
    K_response = sp.BlockMatrix(
        [
            [sp.Matrix([[Y]]), C_raw.T],
            [C_raw, -B],
        ]
    ).as_explicit()

    lapse = 1 / sp.sqrt(Y)
    shift = -C / sp.sqrt(Y)
    h_inverse = B + C * C.T
    K_from_adm = sp.BlockMatrix(
        [
            [
                sp.Matrix([[1 / lapse**2]]),
                (-shift / lapse**2).T,
            ],
            [
                -shift / lapse**2,
                -h_inverse + shift * shift.T / lapse**2,
            ],
        ]
    ).as_explicit()
    adm_residual = (K_response - K_from_adm).applyfunc(sp.simplify)

    determinant_identity_residual = sp.factor(
        K_response.det() + Y * h_inverse.det()
    )
    congruence_L = sp.BlockMatrix(
        [
            [sp.eye(1), sp.zeros(1, 3)],
            [C / sp.sqrt(Y), sp.eye(3)],
        ]
    ).as_explicit()
    congruence_diagonal = sp.BlockMatrix(
        [
            [sp.Matrix([[Y]]), sp.zeros(1, 3)],
            [sp.zeros(3, 1), -h_inverse],
        ]
    ).as_explicit()
    congruence_residual = (
        K_response
        - congruence_L * congruence_diagonal * congruence_L.T
    ).applyfunc(sp.simplify)

    # Coordinate-independent reconstruction identity:
    # K=J g^{-1} J^T => g^{-1}=J^{-1} K J^{-T}.
    J = sp.MatrixSymbol("J", 4, 4)
    g_inverse = sp.MatrixSymbol("g_inverse", 4, 4)
    abstract_K = J * g_inverse * J.T
    reconstructed_g_inverse = sp.simplify(
        sp.Inverse(J) * abstract_K * sp.Inverse(J.T)
    )

    delta_g_inverse = sp.MatrixSymbol("delta_g_inverse", 4, 4)
    delta_K = J * delta_g_inverse * J.T
    reconstructed_delta_g_inverse = sp.simplify(
        sp.Inverse(J) * delta_K * sp.Inverse(J.T)
    )

    passed = (
        _all_zero([adm_residual])
        and _all_zero([congruence_residual])
        and determinant_identity_residual == 0
        and reconstructed_g_inverse == g_inverse
        and reconstructed_delta_g_inverse == delta_g_inverse
    )

    return {
        "status": (
            "PASS_FULL_MATERIAL_CHART_LOCAL_METRIC_AND_ADM_DICTIONARY"
            if passed
            else "CHECK_FULL_MATERIAL_RESPONSE_METRIC_DICTIONARY"
        ),
        "material_labels": "q^I=(Phi,phi^1,phi^2,phi^3)",
        "full_rank_condition": "det(J^I_mu)!=0",
        "convective_convention": {
            "normalized_C^A": "u^mu d_mu phi^A",
            "raw_Gram_C_raw^A": "sqrt(Y)*C^A",
        },
        "response_Gram_matrix_K": K_response,
        "component_count": {
            "Y_clock_lapse": 1,
            "normalized_C^A_flow_shift": 3,
            "B_AB_spatial_strain": 6,
            "total": 10,
        },
        "ADM_dictionary": {
            "N": lapse,
            "N^A": shift,
            "h_inverse_AB": h_inverse,
        },
        "inverse_ADM_reconstruction": K_from_adm,
        "ADM_reconstruction_residual": adm_residual,
        "ADM_congruence_factorization": (
            "K=L diag(Y,-h^{AB}) L^T, "
            "L=[[1,0],[C^A/sqrt(Y),I_3]]"
        ),
        "ADM_congruence_residual": congruence_residual,
        "determinant_identity": sp.Eq(
            sp.Symbol("det_K"),
            -Y * h_inverse.det(),
        ),
        "determinant_identity_residual": determinant_identity_residual,
        "Lorentz_signature_condition": (
            "Y>0 and h^{AB}=B^{AB}+C^A C^B positive definite imply, by "
            "ADM congruence, exactly one positive and three negative "
            "eigenvalues; det(K)=-Y det(h^{-1})<0."
        ),
        "arbitrary_chart_dictionary": {
            "K": "J g^{-1} J^T",
            "g_inverse": "J^{-1} K J^{-T}",
            "g_covariant": "J^T K^{-1} J",
            "sqrt_minus_g": "|det J|/sqrt(-det K)",
        },
        "abstract_reconstruction_identity": (
            reconstructed_g_inverse == g_inverse
        ),
        "variation_map_is_invertible": (
            reconstructed_delta_g_inverse == delta_g_inverse
        ),
        "variation_scope": (
            "delta K=J delta(g^{-1}) J^T is the variation map at fixed q/J; "
            "simultaneous q variations also contain delta J terms"
        ),
        "physical_reading": (
            "On a full-rank material chart, a generic metric is encoded by a "
            "full response tensor: clock response, medium flow and spatial "
            "strain/shear.  A single scalar pressure deficit is only a "
            "symmetry-reduced specialization.  Because K is currently defined "
            "using g, this identity is not a non-circular origin theorem for g."
        ),
    }


def static_pressure_deficit_and_mass_readout_gate() -> dict[str, Any]:
    """Recover the static metric and audit its one-factor energy readout."""

    H = sp.Symbol("H", real=True)
    m0 = sp.Symbol("m_0", positive=True)

    Y = sp.exp(2 * H)
    C = sp.zeros(3, 1)
    B = sp.exp(-2 * H) * sp.eye(3)
    K = sp.BlockMatrix(
        [
            [sp.Matrix([[Y]]), sp.sqrt(Y) * C.T],
            [sp.sqrt(Y) * C, -B],
        ]
    ).as_explicit()
    g_covariant = K.inv().applyfunc(sp.simplify)
    expected_metric = sp.diag(
        sp.exp(-2 * H),
        -sp.exp(2 * H),
        -sp.exp(2 * H),
        -sp.exp(2 * H),
    )
    metric_residual = (g_covariant - expected_metric).applyfunc(sp.simplify)

    phi = -2 * H
    pressure_factor = sp.exp(-H)
    lapse = pressure_factor
    article_mass_readout = sp.simplify(m0 * sp.exp(phi / 2))

    # A constant worldline coefficient in the one physical metric has the
    # redshifted static Killing-energy readout m0*sqrt(g_tt)=m0*N relative to
    # the asymptotic time normalization.  A local comoving observer instead
    # measures the rest energy m0.  This is not, by itself, a derivation of the
    # source body's global ADM mass.
    metric_only_killing_energy_over_c2 = sp.simplify(m0 * lapse)
    one_factor_residual = sp.simplify(
        metric_only_killing_energy_over_c2 - article_mass_readout
    )

    # Inside the defined pure one-metric completion, inserting the same factor
    # in the worldline coefficient adds a second, nonminimal H sensitivity.
    variable_worldline_mass = sp.simplify(m0 * pressure_factor)
    double_counted_external_energy_over_c2 = sp.simplify(
        variable_worldline_mass * lapse
    )
    double_count_residual = sp.simplify(
        double_counted_external_energy_over_c2
        - metric_only_killing_energy_over_c2
    )
    scalar_sensitivity = sp.simplify(
        sp.diff(variable_worldline_mass, H)
    )
    constant_mass_sensitivity = sp.diff(m0, H)

    H_from_clock = sp.expand_log(sp.log(Y) / 2, force=True)
    H_from_volume = sp.expand_log(-sp.log(B.det()) / 6, force=True)

    passed = (
        _all_zero([metric_residual])
        and one_factor_residual == 0
        and double_count_residual != 0
        and scalar_sensitivity != 0
        and constant_mass_sensitivity == 0
        and sp.simplify(H_from_clock - H) == 0
        and sp.simplify(H_from_volume - H) == 0
    )

    return {
        "status": (
            "PASS_STATIC_PRESSURE_METRIC_AND_SINGLE_FACTOR_KILLING_ENERGY_READOUT"
            if passed
            else "CHECK_STATIC_PRESSURE_METRIC_READOUT"
        ),
        "branch": {
            "Y": Y,
            "normalized_C^A": C,
            "B_AB": B,
            "phi": phi,
            "p": pressure_factor,
        },
        "metric_from_response": g_covariant,
        "expected_RefG_metric": expected_metric,
        "metric_residual": metric_residual,
        "H_from_clock_response": H_from_clock,
        "H_from_spatial_volume_response": H_from_volume,
        "constant_matched_worldline_coefficient": m0,
        "redshifted_static_Killing_energy_over_c2": (
            metric_only_killing_energy_over_c2
        ),
        "article_m_eff": article_mass_readout,
        "single_factor_identity_residual": one_factor_residual,
        "nonminimal_variable_worldline_mass_in_pure_metric_completion": (
            variable_worldline_mass
        ),
        "double_counted_external_energy_over_c2": (
            double_counted_external_energy_over_c2
        ),
        "double_count_error": double_count_residual,
        "variable_mass_H_sensitivity": scalar_sensitivity,
        "constant_mass_H_sensitivity": constant_mass_sensitivity,
        "source_rule": (
            "Use one constant matched worldline coefficient (rest mass for a "
            "test body, isolated ADM mass after compact-body matching).  The "
            "factor exp(-H)=sqrt(g_tt) is its redshifted static Killing-energy "
            "readout relative to asymptotic time; a local comoving observer "
            "measures m0.  It is not a second H-dependent matter mass in the "
            "pure one-metric completion."
        ),
        "global_charge_boundary": (
            "The local factor m0*sqrt(g_tt) is not the source body's ADM/Komar "
            "surface charge and does not replace the worldtube-to-ADM matching "
            "theorem."
        ),
        "compact_H_branch_boundary": (
            "For H=H(r), the selected p05z projected-H term is an active "
            "spatial source, not the p03h stealth case H=H(Phi).  Treating H "
            "as a pure metric readout belongs to the separately defined "
            "parametrized-GR completion, not to generic off-branch p05z."
        ),
    }


def selected_scalar_grammar_noninjectivity_gate() -> dict[str, Any]:
    """Prove that F(Y,I1,I2,I3) cannot be the full metric dictionary."""

    eps, c_f = sp.symbols("eps c_F", real=True, nonzero=True)
    Y = sp.Integer(1)
    B = sp.eye(3)
    C_zero_normalized = sp.zeros(3, 1)
    C_flow_normalized = sp.Matrix([eps, 0, 0])

    def response(C_normalized: sp.Matrix) -> sp.Matrix:
        C_raw = sp.sqrt(Y) * C_normalized
        return sp.BlockMatrix(
            [
                [sp.Matrix([[Y]]), C_raw.T],
                [C_raw, -B],
            ]
        ).as_explicit()

    K_zero = response(C_zero_normalized)
    K_flow = response(C_flow_normalized)
    g_zero = K_zero.inv()
    g_flow = K_flow.inv().applyfunc(sp.simplify)

    I1 = sp.trace(B)
    I2 = sp.simplify((I1**2 - sp.trace(B * B)) / 2)
    I3 = B.det()
    theta = sp.simplify(Y + I1 - 4)
    E = sp.eye(3) - B
    F_selected = sp.simplify(c_f * (theta**2 - 16 * E.det()))

    same_selected_invariants = {
        "Y": Y,
        "I1": I1,
        "I2": I2,
        "I3": I3,
        "F_selected": F_selected,
    }
    metric_difference = (g_flow - g_zero).applyfunc(sp.simplify)
    det_zero = sp.factor(K_zero.det())
    det_flow = sp.factor(K_flow.det())

    passed = (
        theta == 0
        and F_selected == 0
        and not _all_zero([K_flow - K_zero])
        and not _all_zero([metric_difference])
        and det_zero == -1
        and det_flow == -(eps**2 + 1)
    )

    return {
        "status": (
            "PASS_SELECTED_INVARIANTS_NONINJECTIVE_FOR_FIXED_CHART_"
            "COMPONENT_RECONSTRUCTION"
            if passed
            else "CHECK_SELECTED_SCALAR_GRAMMAR_NONINJECTIVITY"
        ),
        "selected_grammar_component_count": 4,
        "full_metric_component_count": 10,
        "missing_information": [
            "three convective/shift components C^A",
            "three relative spatial eigenframe/orientation components in a "
            "chosen material chart, unless an additional local relabeling "
            "symmetry makes them gauge",
        ],
        "convention_note": (
            "The witness has Y=1, so normalized C^A and the raw Gram entry "
            "sqrt(Y) C^A coincide; the response() definition nevertheless "
            "keeps the conversion explicit."
        ),
        "same_selected_invariants": same_selected_invariants,
        "zero_flow_response": K_zero,
        "nonzero_flow_response": K_flow,
        "zero_flow_metric": g_zero,
        "nonzero_flow_metric": g_flow,
        "metric_difference": metric_difference,
        "Lorentz_determinants": {
            "det_K_zero": det_zero,
            "det_K_flow": det_flow,
        },
        "decisive_result": (
            "Two different fixed-chart Lorentzian component matrices have "
            "exactly the same (Y,I1,I2,I3) and F_min value.  Therefore this "
            "selected invariant subset cannot algebraically reconstruct every "
            "generic metric component or determine tensor dynamics by itself. "
            "The displayed constant-coefficient witness is flat on both "
            "sides; it does not by itself prove non-injectivity between "
            "physically inequivalent curved geometries."
        ),
    }


def einstein_equivalent_response_parent_action_gate() -> dict[str, Any]:
    """Construct an exactly GR-equivalent parametrized continuum action.

    This is an exact representation by definition.  It is not a claim that
    the current p01 polynomial generated Einstein-Hilbert microscopically.
    """

    J = sp.MatrixSymbol("J", 4, 4)
    F = sp.MatrixSymbol("F", 4, 4)
    g_inverse = sp.MatrixSymbol("g_inverse", 4, 4)
    delta_g_inverse = sp.MatrixSymbol("delta_g_inverse", 4, 4)

    K = J * g_inverse * J.T
    delta_K = J * delta_g_inverse * J.T
    reconstructed_g_inverse = sp.simplify(
        sp.Inverse(J) * K * sp.Inverse(J.T)
    )
    reconstructed_delta = sp.simplify(
        sp.Inverse(J) * delta_K * sp.Inverse(J.T)
    )

    # Linear representative of the local material relabeling law
    # q'=f(q), J'=F J, K'=F K F^T.  The second line uses
    # (F K F^T)^-1=F^-T K^-1 F^-1 and verifies that g is invariant.
    metric_covariant_from_qK = J.T * sp.Inverse(K) * J
    relabeled_metric_covariant = sp.simplify(
        J.T
        * F.T
        * sp.Inverse(F.T)
        * sp.Inverse(K)
        * sp.Inverse(F)
        * F
        * J
    )
    relabeling_invariance = (
        relabeled_metric_covariant == metric_covariant_from_qK
    )

    passed = (
        reconstructed_g_inverse == g_inverse
        and reconstructed_delta == delta_g_inverse
        and relabeling_invariance
    )

    return {
        "status": (
            "PASS_EXACT_PARAMETRIZED_EINSTEIN_PARENT_ACTION_IDENTITY"
            if passed
            else "CHECK_EINSTEIN_EQUIVALENT_RESPONSE_PARENT_ACTION"
        ),
        "candidate_IR_gravitational_response_variable": (
            "one symmetric Lorentzian response K^{IJ} in a regular local "
            "operational material chart q^I"
        ),
        "metric_definition": (
            "g_mn[q,K]=q^I_m (K^{-1})_IJ q^J_n"
        ),
        "measure_definition": (
            "sqrt(-g)=|det(dq/dx)|/sqrt(-det K)"
        ),
        "exact_parent_action": (
            "S_bridge[q,K,psi]=(M_Pl^2/2) Integral sqrt(-g[q,K]) "
            "(R[g[q,K]]-2 Lambda)+S_matter^minimal[g[q,K],psi]"
        ),
        "covariant_Dirichlet_action": (
            "S_covariant,Dirichlet=S_EH+S_GHY with the chosen outward-normal "
            "and curvature conventions"
        ),
        "matter_stress_convention": (
            "T_mn=-(2/sqrt(-g)) delta S_matter/delta g^{mn}; this convention "
            "gives G_mn+Lambda g_mn=M_Pl^{-2}T_mn"
        ),
        "material_ADM_action_for_project_curvature_convention": (
            "S_EH=(M_Pl^2/2) Integral dPhi d^3phi N sqrt(h) "
            "[-R^(3)+Kcal^2-Kcal_AB Kcal^AB]"
            "+S_spatial-boundary+S_corner+S_asymptotic"
        ),
        "curvature_and_boundary_scope": (
            "The ADM sign uses the (+---) and p05z Riemann convention.  "
            "The covariant Dirichlet action contains S_GHY.  After the "
            "Gauss-Codazzi split, its cancelling normal divergence is already "
            "accounted for; the displayed ADM bulk is therefore supplemented "
            "by the appropriate spatial-boundary/corner/asymptotic terms, not "
            "by a second copy of the full GHY term.  Falloff conditions are "
            "required when ADM charges are used."
        ),
        "material_ADM_variables": (
            "N=Y^(-1/2), N^A=-C_normalized^A/sqrt(Y), "
            "h^{AB}=B^{AB}+C_normalized^A C_normalized^B"
        ),
        "extrinsic_curvature_convention": (
            "Kcal_AB=(2N)^(-1)[partial_Phi h_AB-D_A N_B-D_B N_A]; "
            "reversing the overall sign of Kcal does not change the displayed "
            "quadratic combination"
        ),
        "variation_dictionary": (
            "At fixed q/J, delta K=J delta(g^{-1}) J^T; because det J!=0, "
            "delta K is arbitrary iff delta(g^{-1}) is arbitrary"
        ),
        "metric_reconstruction_identity": (
            reconstructed_g_inverse == g_inverse
        ),
        "variation_reconstruction_identity": (
            reconstructed_delta == delta_g_inverse
        ),
        "joint_parameter_count": {
            "q_labels": 4,
            "symmetric_K_components": 10,
            "metric_components": 10,
            "local_relabeling_redundancies": 4,
        },
        "local_material_relabeling_rule": (
            "q'^I=f^I(q), F^I_J=d f^I/d q^J, "
            "J'=F J, K'=F K F^T"
        ),
        "linear_relabeling_metric_invariance": relabeling_invariance,
        "equation_equivalence": (
            "delta S_bridge/delta K=0 iff "
            "G_mn+Lambda g_mn=M_Pl^{-2} T_mn"
        ),
        "label_equations": (
            "In this defined completion q^I are postulated to be pure "
            "relational coordinates and the action depends only on g[q,K].  "
            "Define E_g^{mn}:=(1/sqrt(-g)) delta S/delta g_mn.  At fixed K, "
            "the chain rule gives E_qI=-2 partial_m[sqrt(-g) E_g^{mn} "
            "(K^{-1})_IJ J_n^J], so the q equations follow when the metric/K "
            "equations hold.  This redundancy is part of the newly defined "
            "parametrized completion; it has not been derived for the physical "
            "p01 scalar/solid fields."
        ),
        "physical_DOF": (
            "After quotienting the explicit four-function material relabeling "
            "redundancy, this parametrized parent has exactly the GR metric "
            "degrees of freedom after the usual constraints: two tensor "
            "helicities in the weak vacuum.  This statement does not apply to "
            "the independently varied current F_min/H medium action."
        ),
        "global_chart_guard": (
            "det J!=0 proves only a local dictionary.  Generic GR spacetimes "
            "may require several material-chart patches; one global q chart "
            "is neither assumed nor proved."
        ),
        "scientific_scope": (
            "This is an exact parametrized-GR target/representation.  It may "
            "serve as the continuum completion when RefG is defined as the "
            "mechanism/interpretation of GR curvature, but the current files "
            "have not derived this parent action, K or M_Pl from either the "
            "effective F_min/H medium or the undifferentiated foundation."
        ),
    }


def ir_uniqueness_and_pregeometric_underdetermination_gate() -> dict[str, Any]:
    """Separate the standard IR uniqueness theorem from missing micro premises."""

    M2, alpha = sp.symbols("M_Pl_sq alpha_R2", nonzero=True, real=True)
    R, box_R = sp.symbols("R Box_R", real=True)

    gr_trace = -M2 * R
    r2_trace = -M2 * R + 6 * alpha * box_R
    countermodel_difference = sp.simplify(r2_trace - gr_trace)

    current_workspace = {
        "pregeometric_relational_state_space_and_self_distinction_law": False,
        "foundation_to_first_stable_distinction_derived": False,
        "first_distinction_to_manifested_nodal_network_derived": False,
        "manifested_network_to_local_qK_response_derived": False,
        "oscillon_to_pressure_deficit_profile_derived": False,
        "pressure_deficit_to_full_response_K_derived": False,
        "one_universal_response_K_for_every_mode_derived": False,
        "only_one_positive_residue_massless_helicity_2_pair_derived": False,
        "nonlinear_diffeomorphism_Ward_constraint_algebra_derived": False,
        "universal_minimal_matter_coupling_derived_from_microphysics": False,
        "all_extra_Phi_phiA_H_modes_constrained_or_gapped": False,
        "Einstein_Hilbert_and_M_Pl_generated_from_substrate": False,
        "effective_spacetime_covariance_once_g_is_assumed": True,
        "local_GR_like_TT_subsector_from_inserted_EH_backbone": True,
    }

    countermodel_pass = (
        countermodel_difference == 6 * alpha * box_R
        and countermodel_difference != 0
    )

    return {
        "status": (
            "PASS_IR_EINSTEIN_UNIQUENESS_CONTRACT_RECORDED__"
            "PREGEOMETRIC_UNDERDETERMINATION_SHOWN"
            if countermodel_pass
            else "CHECK_IR_UNIQUENESS_AND_UNDERDETERMINATION"
        ),
        "standard_IR_theorem_premises": [
            "four-dimensional local continuum",
            "one universal Lorentzian metric/response tensor",
            "exact diffeomorphism gauge redundancy and conserved total stress",
            "local leading dynamics with at most two metric derivatives",
            "only one healthy massless helicity +/-2 pair in the gravity sector",
            "universal matter coupling",
        ],
        "standard_IR_theorem_conclusion": (
            "The leading action is Einstein-Hilbert plus cosmological, "
            "boundary and four-dimensional topological terms.  Standard "
            "massless-spin-2 self-coupling/consistent-deformation and "
            "Lovelock routes establish this implication."
        ),
        "current_workspace_derivation": current_workspace,
        "countermodel": {
            "action_1": "EH",
            "action_2": "EH+alpha R^2",
            "shared_properties": (
                "one covariant metric and the same normalized flat/readout "
                "branch can be admitted by both"
            ),
            "GR_trace": gr_trace,
            "R2_trace": r2_trace,
            "difference": countermodel_difference,
        },
        "underdetermination_result": (
            "The current ontology, covariance and p/p^2 readout do not entail "
            "Einstein-Hilbert uniquely.  A two-derivative/no-extra-gapless-mode "
            "IR premise or an explicit microscopic calculation is necessary."
        ),
        "minimal_IR_emergence_axiom_after_nodal_network": (
            "After the first stable node-imprint-relation structure develops "
            "and coarse grains to a 3+1 continuum, the manifested phase has "
            "local full-rank four-label charts and one universal Lorentzian "
            "response K^{IJ}; label changes are gauge relabelings, K is the "
            "only gapless gravitational collective variable, and higher-"
            "derivative/nonlocal corrections lie beyond the audited 1PN scale."
        ),
        "primary_theorem_sources": [
            "Deser, Self-Interaction and Gauge Invariance, "
            "https://arxiv.org/abs/gr-qc/0411023",
            "Boulanger-Damour-Gualtieri-Henneaux, consistent massless spin-2 "
            "deformations, https://arxiv.org/abs/hep-th/0009109",
            "Lovelock, The Four-Dimensionality of Space and the Einstein Tensor",
            "Donoghue, GR as an EFT, https://arxiv.org/abs/gr-qc/9405057",
        ],
    }


def selected_fh_role_in_exact_refinement_gate() -> dict[str, Any]:
    """Classify the admissible roles of the current F_min/H sector."""

    no_double = effective_layer_no_double_count_theorem_gate()
    noninjective = selected_scalar_grammar_noninjectivity_gate()

    passed = (
        no_double["status"] == "PASS_EFFECTIVE_LAYER_NO_DOUBLE_COUNT_THEOREM"
        and noninjective["status"]
        == (
            "PASS_SELECTED_INVARIANTS_NONINJECTIVE_FOR_FIXED_CHART_"
            "COMPONENT_RECONSTRUCTION"
        )
    )

    return {
        "status": (
            "PASS_FH_ROLE_OPTIONS_AND_NO_DOUBLE_COUNT_CONSTRAINT_CLASSIFIED__"
            "CURRENT_MATCHING_UNDECIDED"
            if passed
            else "CHECK_FH_ROLE_IN_EXACT_REFINEMENT"
        ),
        "no_double_count_status": no_double["status"],
        "metric_noninjectivity_status": noninjective["status"],
        "defined_parametrized_completion_action": (
            "S_EH[g(K)]+S_matter^minimal[g(K),psi]"
        ),
        "allowed_FH_roles": [
            "an upstream microscopic/internal constitutive sector already "
            "integrated into the response K and its matched coefficients",
            "a symmetry-reduced readout/parameterization of K in the newly "
            "defined parametrized-GR completion",
            "a genuine matter sector included once in the total T_mn, in "
            "which case its nonzero stress is physical and the theory is no "
            "longer exactly vacuum GR in that domain",
        ],
        "rejected_role": (
            "Counting one and the same physical F_min/H contribution both as "
            "already integrated into the matched EH response and again as an "
            "independently varied nonzero effective stress.  Conversely, "
            "dropping an active sector before an integrate-out/matching proof "
            "would undercount it."
        ),
        "current_p05z_as_generic_final_GR_equivalent_action": False,
        "current_p05z_value": (
            "p05z remains the selected static effective-action gate and "
            "establishes its stated weak and compact on-shell branches.  The "
            "present parametrized-GR construction neither replaces p05z nor "
            "derives its matching to the Einstein parent; that matching is "
            "open."
        ),
        "compact_H_clarification": (
            "On the compact H=H(r) branch F_min is quiet at the hatted unit "
            "point, while the projected H-gradient term is active and sources "
            "the exponential metric.  It is not action-level stealth and "
            "cannot be relabeled a pure metric coordinate inside current p05z."
        ),
        "existing_selected_action_file_rewritten": False,
        "article_export_allowed": False,
    }


def worldtube_adm_and_standard_1pn_handoff_gate() -> dict[str, Any]:
    """Define the GR 1PN form of the parametrized-Einstein completion."""

    parent = einstein_equivalent_response_parent_action_gate()
    readout = static_pressure_deficit_and_mass_readout_gate()
    worldtube = worldtube_source_replacement_handoff_gate()
    handoff = standard_gr_1pn_handoff_gate()

    passed = (
        parent["status"]
        == "PASS_EXACT_PARAMETRIZED_EINSTEIN_PARENT_ACTION_IDENTITY"
        and readout["status"]
        == "PASS_STATIC_PRESSURE_METRIC_AND_SINGLE_FACTOR_KILLING_ENERGY_READOUT"
        and worldtube["status"].startswith(
            "PASS_WORLD_TUBE_NO_DOUBLE_COUNT_CONTRACT_ALGEBRA"
        )
        and handoff["status"].startswith(
            "PASS_LOGICAL_HANDOFF_FROM_POSTULATED_MINIMAL_EINSTEIN_EFFECTIVE_ACTION"
        )
    )

    return {
        "status": (
            "PASS_DEFINED_GR_1PN_FORM_FOR_PARAMETRIZED_EINSTEIN_COMPLETION__"
            "REFG_WORLDTUBE_MATCHING_AND_MICROSCOPIC_MASSES_OPEN"
            if passed
            else "CHECK_WORLD_TUBE_ADM_AND_STANDARD_1PN_HANDOFF"
        ),
        "effective_action_through_1PN": (
            "For Lambda=0 with asymptotically flat boundary conditions, "
            "S_eff=S_EH[g(K)]-sum_A m_A^(isolated ADM) Integral ds_A"
        ),
        "worldline_mass_rule": (
            "m_A^(isolated ADM) is one constant matched coefficient.  Local "
            "exp(-H) redshifting of its static Killing energy is already "
            "sqrt(g_tt), not m_A(H)."
        ),
        "extra_charge_rule": (
            "By definition of this parametrized-GR completion, H is only a "
            "metric-response parameter and q^I are relational labels, so "
            "neither supplies an independent long-range worldline charge.  "
            "The current p05z medium requires a separate matching proof before "
            "this rule can be applied to it."
        ),
        "effacement_scope": (
            "The defined GR parent action has the standard GR compact-body "
            "effacement/finite-size hierarchy once each RefG body has actually "
            "been matched to that worldline EFT.  Spin or retained multipoles "
            "then use the usual GR worldline operators."
        ),
        "standard_1PN_conclusion": (
            "For the defined parametrized-Einstein completion with Lambda=0, "
            "asymptotically flat boundary conditions, minimal universal "
            "matter coupling and no extra long-range field, the N-body "
            "equations through 1PN are the standard EIH equations and the ten "
            "standard PPN parameters take their GR values.  Applying that "
            "conclusion to current RefG bodies still requires the stated "
            "worldtube/source matching."
        ),
        "what_is_not_needed_for_the_1PN_form": (
            "A microscopic prediction of each particle mass is not required "
            "to determine the universal EIH form; measured isolated ADM masses "
            "serve as EFT matching coefficients."
        ),
        "what_remains_open_for_predictivity": [
            "derive the full RefG source inventory to isolated ADM/Noether "
            "mass, current moments and worldline coefficients",
            "show that no independent H/label charge or preferred-frame "
            "operator survives that matching through 1PN",
            "derive finite-energy RefG oscillon/compact-body solutions",
            "compute their isolated ADM/Noether masses rather than treating "
            "those masses as matched data",
            "derive the particle spectrum and strong-field internal structure",
        ],
        "parent_action_status": parent["status"],
        "mass_readout_status": readout["status"],
        "worldtube_contract_status": worldtube["status"],
        "GR_handoff_status": handoff["status"],
    }


def full_forest_to_einstein_bridge_status() -> dict[str, Any]:
    """Top-level decision: exact representation, open physical matching."""

    dictionary = full_material_response_metric_dictionary_gate()
    readout = static_pressure_deficit_and_mass_readout_gate()
    noninjective = selected_scalar_grammar_noninjectivity_gate()
    parent = einstein_equivalent_response_parent_action_gate()
    uniqueness = ir_uniqueness_and_pregeometric_underdetermination_gate()
    fh_role = selected_fh_role_in_exact_refinement_gate()
    pn = worldtube_adm_and_standard_1pn_handoff_gate()

    parametrized_gr_construction_closed = (
        dictionary["status"]
        == "PASS_FULL_MATERIAL_CHART_LOCAL_METRIC_AND_ADM_DICTIONARY"
        and readout["status"]
        == "PASS_STATIC_PRESSURE_METRIC_AND_SINGLE_FACTOR_KILLING_ENERGY_READOUT"
        and noninjective["status"]
        == (
            "PASS_SELECTED_INVARIANTS_NONINJECTIVE_FOR_FIXED_CHART_"
            "COMPONENT_RECONSTRUCTION"
        )
        and parent["status"]
        == "PASS_EXACT_PARAMETRIZED_EINSTEIN_PARENT_ACTION_IDENTITY"
        and uniqueness["status"].startswith(
            "PASS_IR_EINSTEIN_UNIQUENESS_CONTRACT"
        )
        and fh_role["status"].startswith(
            "PASS_FH_ROLE_OPTIONS_AND_NO_DOUBLE_COUNT_CONSTRAINT_CLASSIFIED"
        )
        and pn["status"].startswith(
            "PASS_DEFINED_GR_1PN_FORM_FOR_PARAMETRIZED_EINSTEIN_COMPLETION"
        )
    )

    # The construction above starts by defining K as metric components and
    # choosing the EH functional.  It therefore does not close the physical
    # matching links that a RefG emergence and compact-body claim must derive.
    current_refg_continuum_to_einstein_matching_closed = False
    pregeometric_micro_derivation_closed = False

    return {
        "status": (
            "OPEN_CURRENT_REFG_PHYSICAL_BRIDGE__PASS_LOCAL_K_TO_G_"
            "DICTIONARY_AND_POSTULATED_EH_REPARAMETERIZATION__FOUNDATION_TO_"
            "DISTINCTION_DEFICIT_TO_K_REFG_TO_EH_AND_WORLDTUBE_MATCHING_OPEN"
            if parametrized_gr_construction_closed
            else "CHECK_FULL_FOREST_TO_EINSTEIN_BRIDGE"
        ),
        "construction_audit_completed": parametrized_gr_construction_closed,
        "parametrized_GR_construction_closed": (
            parametrized_gr_construction_closed
        ),
        "continuum_bridge_closed": (
            current_refg_continuum_to_einstein_matching_closed
        ),
        "current_RefG_continuum_to_Einstein_matching_closed": (
            current_refg_continuum_to_einstein_matching_closed
        ),
        "pregeometric_micro_derivation_closed": (
            pregeometric_micro_derivation_closed
        ),
        "requested_full_proof_from_current_axioms": (
            "NOT_YET_DERIVED_FROM_CURRENT_FORMAL_VARIABLES"
        ),
        "exact_result_now": [
            "on a full-rank material chart, the defined clock/flow/strain "
            "Gram response is exactly the inverse metric in that chart",
            "the static pressure-deficit ansatz reconstructs the exponential "
            "metric exactly",
            "m0 exp(-H) is the one-factor redshifted static Killing-energy "
            "readout of a constant worldline coefficient, not the locally "
            "measured rest energy and not a global ADM theorem",
            "an Einstein-Hilbert parent action can be defined in response "
            "variables as an exact parametrized representation of GR",
            "that defined parent action has the standard GR/EIH 1PN form once "
            "RefG worldtubes are matched to it",
            "the selected scalar F_min invariant subset does not reconstruct "
            "all generic fixed-chart metric components",
        ],
        "remaining_physical_obligations": [
            "formulate a pregeometric relational state space and derive the "
            "first stable node-imprint-relation structure",
            "derive the manifested causal/nodal network and its local 3+1 "
            "full-rank q,K response rather than defining K with a prior g",
            "derive oscillon internal dynamics -> foundation-medium carrier "
            "deficit -> pressure profile H -> the full tensor response K",
            "derive or match the current F_min/H effective medium to the "
            "parametrized Einstein-Hilbert parent action without duplicate "
            "stress, extra modes or preferred-frame operators",
            "derive the RefG worldtube inventory to ADM/Noether charges and "
            "the minimal worldline EFT through 1PN",
        ],
        "correct_theory_reading": (
            "If RefG is completed as a refinement/mechanism of GR, the "
            "response-tensor parent action is a mathematically exact target "
            "representation.  RefG may then explain what the metric components "
            "mean physically, provided the open substrate, effective-medium "
            "and worldtube matching steps are actually derived; it must not "
            "append the same mechanism as a second gravity source."
        ),
        "selected_action_replacement_performed": False,
        "article_export_allowed": False,
        "metric_dictionary_gate": dictionary,
        "static_pressure_readout_gate": readout,
        "scalar_grammar_noninjectivity_gate": noninjective,
        "Einstein_parent_action_gate": parent,
        "IR_uniqueness_and_axiom_gate": uniqueness,
        "F_H_role_gate": fh_role,
        "worldtube_and_1PN_gate": pn,
    }


def main() -> int:
    result = full_forest_to_einstein_bridge_status()
    print("status:", result["status"])
    print(
        "parametrized GR construction closed:",
        result["parametrized_GR_construction_closed"],
    )
    print(
        "current RefG continuum -> Einstein matching closed:",
        result["current_RefG_continuum_to_Einstein_matching_closed"],
    )
    print(
        "pregeometric micro derivation closed:",
        result["pregeometric_micro_derivation_closed"],
    )
    print(
        "requested full proof:",
        result["requested_full_proof_from_current_axioms"],
    )
    print("metric dictionary:", result["metric_dictionary_gate"]["status"])
    print(
        "pressure/readout:",
        result["static_pressure_readout_gate"]["status"],
    )
    print(
        "Einstein parent action:",
        result["Einstein_parent_action_gate"]["status"],
    )
    print("1PN:", result["worldtube_and_1PN_gate"]["status"])
    print("article export allowed:", result["article_export_allowed"])
    return 0 if result["construction_audit_completed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
