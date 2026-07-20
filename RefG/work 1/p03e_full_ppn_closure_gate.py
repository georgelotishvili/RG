# Notation header:
# signature (+---); Y = g^mn d_m Phi d_n Phi;
# B^AB = -g^mn d_m phi^A d_n phi^B.

"""p03e: objective-wide 1PN / standard-PPN closure gate.

This file separates four statements which had become mixed in p03:

1. The selected static spherical Solar branch is an action-level solution
   through O(U^2).  This is supported by p03c/p03d/p05z and gives the standard
   isotropic readings beta=gamma=1.
2. The minimal seven-term F_min polynomial has an unreduced rank-deficient
   quadratic form on the exact-GR coupling slice.  K_pi=0 is not, by itself, a
   ghost theorem or a proof that an ESS term is required; an ADM/Dirac and
   strong-coupling audit must decide whether it is a constraint, a missing
   mode, or a genuine pathology.
3. The selected p05z static action contains EH, phase-normalized F_min and the
   projected H sector.  It does not contain the separate p02c S6/ESS
   completion.  Those operators are alternative completion scenarios.
4. A diffeomorphism boost of the *entire* static solution keeps
   C_A=u.d(phi^A)=0 exactly.  A U*w term appears only if one instead freezes a
   source-rest Newtonian metric while rigidly boosting the asymptotic medium.
   That is a useful off-shell residual, not an unavoidable preferred-frame
   source.

The positive result is therefore a closed static 1PN exterior/EOM certificate
and a useful arbitrary-shape linear decoupling theorem for minimal F_min.  The
full standard PPN problem and the reduced degree-of-freedom problem remain open
until one dynamical action is selected and its inhomogeneous PN equations for
g_00=O(v^4), g_0i=O(v^3), g_ij=O(v^2), Phi, phi^A and H (plus any explicitly
selected completion) are solved and matched to the ten standard PPN
parameters.
"""

from __future__ import annotations

from typing import Any

import sympy as sp


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def solar_fmin_normal_form_theorem() -> dict[str, Any]:
    """Exact normal form of the physical Solar coefficient slice.

    On c_YI1=2*c_Y2, write c=c_Y2.  The seven-term polynomial becomes

        F_min/c = (Y + I1 - 4)^2 - 16 det(I-B).

    Around Y=1 and B=I its unreduced quadratic Hessian has rank one: only the
    combined clock-plus-volume trace is displayed before constraints are
    reduced.  The determinant starts at cubic order.
    """

    Y, c, eps = sp.symbols("Y c eps", real=True)
    entries = sp.symbols("B_00:03 B_10:13 B_20:23", real=True)
    B = sp.Matrix(3, 3, entries)
    I1 = sp.trace(B)
    I2 = sp.simplify((I1**2 - sp.trace(B * B)) / 2)
    I3 = sp.det(B)

    f_slice = sp.expand(
        -8 * Y
        + Y**2
        + 8 * I1
        + I1**2
        - 16 * I2
        + 16 * I3
        + 2 * Y * I1
    )
    trace_constraint = sp.expand(Y + I1 - 4)
    normal_form = sp.expand(
        trace_constraint**2 - 16 * sp.det(sp.eye(3) - B)
    )
    normal_form_residual = sp.simplify(f_slice - normal_form)

    y = sp.Symbol("delta_Y", real=True)
    b11, b22, b33, b12, b13, b23 = sp.symbols(
        "b_11 b_22 b_33 b_12 b_13 b_23",
        real=True,
    )
    dB = sp.Matrix(
        [
            [b11, b12, b13],
            [b12, b22, b23],
            [b13, b23, b33],
        ]
    )
    B_pert = sp.eye(3) + eps * dB
    Y_pert = 1 + eps * y
    pert_subs = {
        Y: Y_pert,
        **{
            B[i, j]: B_pert[i, j]
            for i in range(3)
            for j in range(3)
        },
    }
    perturbation = sp.expand(f_slice.subs(pert_subs))
    quadratic = sp.factor(perturbation.coeff(eps, 2))
    cubic = sp.factor(perturbation.coeff(eps, 3))
    variables = (y, b11, b22, b33, b12, b13, b23)
    hessian = sp.hessian(quadratic, variables)

    E = sp.eye(3) - B
    gradient_B = sp.Matrix(
        3,
        3,
        lambda i, j: sp.diff(f_slice, B[i, j]),
    )
    expected_gradient_B = (
        2 * trace_constraint * sp.eye(3) + 16 * E.cofactor_matrix()
    )
    gradient_residuals = list(gradient_B - expected_gradient_B)

    passed = (
        normal_form_residual == 0
        and sp.simplify(
            quadratic - (y + b11 + b22 + b33) ** 2
        )
        == 0
        and sp.simplify(cubic - 16 * sp.det(dB)) == 0
        and hessian.rank() == 1
        and _all_zero(gradient_residuals)
    )

    return {
        "status": (
            "PASS_SOLAR_FMIN_EXACT_NORMAL_FORM_AND_RANK_ONE_QUADRATIC_HESSIAN"
            if passed
            else "CHECK_SOLAR_FMIN_NORMAL_FORM"
        ),
        "coupling_slice": "c_YI1=2*c_Y2; c=c_Y2",
        "F_min_over_c": f_slice,
        "normal_form": normal_form,
        "normal_form_residual": normal_form_residual,
        "matrix_derivative": gradient_B,
        "matrix_derivative_expected": expected_gradient_B,
        "matrix_derivative_residuals": gradient_residuals,
        "quadratic_perturbation": quadratic,
        "cubic_perturbation": cubic,
        "quadratic_hessian": hessian,
        "quadratic_hessian_rank": hessian.rank(),
        "quadratic_nullity": len(variables) - hessian.rank(),
        "reading": (
            "At the exact-GR Solar slice the minimal polynomial controls only "
            "deltaY+Tr(deltaB) in the unreduced quadratic action.  The displayed "
            "shear/vector entries vanish, but the physical degree-of-freedom "
            "and strong-coupling interpretation requires ADM/Dirac reduction. "
            "The cofactor force begins at quadratic order in deltaB because "
            "det(I-B) begins at cubic action order."
        ),
    }


def general_branch_quadratic_motion_theorem() -> dict[str, Any]:
    """Moving homogeneous quadratic block on the p03 1PN coefficient family.

    Let c=c_Y2, d=c_YI1, and K_pi=2c-d.  For

        Phi=t-a_i x^i,
        phi^A=x^A-b^A t,
        g^{0i}=h_i,

    the seven-term polynomial has

        L_F^(2)=K_pi*(a^2+b^2+2 h.(a-b)).

    Hence the exact-GR slice d=2c removes the whole quadratic moving block.
    """

    c, d = sp.symbols("c d", real=True)
    K_pi = sp.simplify(2 * c - d)
    h = sp.Matrix(sp.symbols("h_1:4", real=True))
    a = sp.Matrix(sp.symbols("a_1:4", real=True))
    b = sp.Matrix(sp.symbols("b_1:4", real=True))
    variables = tuple(h) + tuple(a) + tuple(b)

    l2 = sp.expand(
        K_pi
        * (
            (a.dot(a))
            + (b.dot(b))
            + 2 * h.dot(a - b)
        )
    )
    source_h = sp.Matrix([sp.diff(l2, item) for item in h])
    hessian = sp.hessian(l2, variables)
    exact_gr_subs = {d: 2 * c}
    exact_gr_l2 = sp.simplify(l2.subs(exact_gr_subs))
    exact_gr_hessian = hessian.subs(exact_gr_subs).applyfunc(sp.simplify)

    passed = exact_gr_l2 == 0 and _all_zero(list(exact_gr_hessian))
    return {
        "status": (
            "PASS_GENERAL_BRANCH_MOVING_BLOCK_AND_EXACT_GR_KPI_ZERO_"
            "UNREDUCED_DEGENERACY"
            if passed
            else "CHECK_GENERAL_BRANCH_MOVING_BLOCK"
        ),
        "K_pi": K_pi,
        "quadratic_moving_lagrangian": l2,
        "metric_vector_source": source_h,
        "quadratic_hessian": hessian,
        "exact_GR_slice": sp.Eq(d, 2 * c),
        "quadratic_lagrangian_on_exact_GR_slice": exact_gr_l2,
        "hessian_on_exact_GR_slice": exact_gr_hessian,
        "Kpi_zero_interpretation": (
            "UNREDUCED_QUADRATIC_DEGENERACY__NOT_A_GHOST_THEOREM"
        ),
        "required_reduction_audit": [
            "ADM lapse/shift constraint analysis",
            "Dirac primary/secondary constraint and degree-of-freedom count",
            "reduced kinetic matrix after nondynamical fields are eliminated",
            "strong-coupling scale around the selected Solar background",
        ],
        "reading": (
            "The minimal p03 alpha_i smoke test is zero on the exact-GR slice "
            "because K_pi=0 removes the displayed unreduced quadratic moving "
            "block.  This does not prove a ghost and does not require ESS by "
            "itself; its constraint and strong-coupling content remain open."
        ),
    }


def linearized_minimal_fmin_decoupling_theorem() -> dict[str, Any]:
    """Arbitrary-shape linear theorem for the minimal F_min slice.

    With inverse-metric perturbations dq^{mn}, Phi=t+chi,
    phi^A=x^A+pi^A, and the phase-normalizing field H, the only quadratic
    minimal-F_min combination is

        Theta = dq00 + 2 chi_dot + 2 div(pi) - Tr(dqij) + 4 H.

    The spatial solid equation gives grad(Theta)=0.  For a localized source
    with asymptotic normalization Theta->0, this sets Theta=0 and removes the
    linear minimal-F_min stress for arbitrary spatial shape.
    """

    c = sp.Symbol("c", positive=True)
    dq00, chi_dot, div_pi, H = sp.symbols(
        "dq00 chi_dot div_pi H",
        real=True,
    )
    dq11, dq22, dq33 = sp.symbols("dq11 dq22 dq33", real=True)
    q01, q02, q03 = sp.symbols("q01 q02 q03", real=True)
    theta = sp.expand(
        dq00
        + 2 * chi_dot
        + 2 * div_pi
        - dq11
        - dq22
        - dq33
        + 4 * H
    )
    l2 = sp.expand(c * theta**2)

    metric_sources = {
        "dq00": sp.diff(l2, dq00),
        "dq11": sp.diff(l2, dq11),
        "dq22": sp.diff(l2, dq22),
        "dq33": sp.diff(l2, dq33),
        "q01": sp.diff(l2, q01),
        "q02": sp.diff(l2, q02),
        "q03": sp.diff(l2, q03),
    }
    theta_zero = {
        dq00: (
            -2 * chi_dot
            - 2 * div_pi
            + dq11
            + dq22
            + dq33
            - 4 * H
        )
    }
    sources_on_constraint = {
        key: sp.simplify(value.subs(theta_zero))
        for key, value in metric_sources.items()
    }

    k1, k2, k3 = sp.symbols("k_1 k_2 k_3", real=True)
    theta_k = sp.Symbol("Theta_k", real=True)
    k_sq = sp.expand(k1**2 + k2**2 + k3**2)
    solid_fourier_equations = [
        sp.expand(4 * sp.I * c * component * theta_k)
        for component in (k1, k2, k3)
    ]
    contracted_equation = sp.simplify(
        sum(
            (-sp.I * component) * equation
            for component, equation in zip(
                (k1, k2, k3),
                solid_fourier_equations,
            )
        )
    )

    passed = (
        _all_zero(sources_on_constraint.values())
        and metric_sources["q01"] == 0
        and metric_sources["q02"] == 0
        and metric_sources["q03"] == 0
        and sp.simplify(contracted_equation - 4 * c * k_sq * theta_k) == 0
    )
    return {
        "status": (
            "PASS_MINIMAL_FMIN_LINEAR_ARBITRARY_SHAPE_DECOUPLING_WITH_LOCALIZED_BOUNDARY"
            if passed
            else "CHECK_MINIMAL_FMIN_LINEAR_DECOUPLING"
        ),
        "Theta": theta,
        "quadratic_lagrangian": l2,
        "linear_metric_sources": metric_sources,
        "sources_after_Theta_zero": sources_on_constraint,
        "solid_equation_fourier_components": solid_fourier_equations,
        "solid_equation_contracted": sp.Eq(
            4 * c * k_sq * theta_k,
            0,
        ),
        "boundary_condition": (
            "localized mode: k^2>0; homogeneous integration mode fixed by "
            "Theta(r->infinity)=0"
        ),
        "closed_here": (
            "minimal F_min adds no linear stress after its localized solid "
            "constraint is imposed, without assuming spherical symmetry"
        ),
        "not_closed_here": (
            "selected-p05z H/metric/field nonlinear response and the "
            "inhomogeneous standard-PPN potential solution; optional ESS "
            "response only if an ESS completion is separately selected"
        ),
    }


def selected_p05z_action_provenance_gate() -> dict[str, Any]:
    """Separate the selected p05z action from optional ESS/S6 completions.

    The static action selected by p05z is

        EH + phase-normalized F_min + projected H.

    The p02c S6 square and phase-solid ESS/Z kinetic operator are separate
    completion proposals.  A diagnostic computed for those proposals must not
    be conjoined with the selected p05z static action or treated as a required
    repair of K_pi=0.
    """

    from p05z_unified_deficit_field_static_branch_gate import (
        unified_deficit_field_static_branch_status,
    )

    selected = unified_deficit_field_static_branch_status()
    action = selected["action"]
    required_tokens = (
        "M_Pl^2 R/2",
        "F_min",
        "gamma^mn d_m H d_n H",
    )
    excluded_tokens = (
        "eta_ESS",
        "c_Z",
        "lambda_S",
        "(S-6)",
    )
    required_present = {
        token: token in action
        for token in required_tokens
    }
    excluded_absent = {
        token: token not in action
        for token in excluded_tokens
    }
    passed = (
        selected["status"]
        == "PASS_UNIFIED_H_STATIC_BRANCHES_EOM__OFF_BRANCH_DYNAMICS_OPEN"
        and all(required_present.values())
        and all(excluded_absent.values())
    )

    return {
        "status": (
            "PASS_SELECTED_P05Z_ACTION_PROVENANCE__ESS_S6_EXCLUDED_"
            "ALTERNATIVE_ONLY"
            if passed
            else "CHECK_SELECTED_P05Z_ACTION_PROVENANCE"
        ),
        "selected_action_source": (
            "p05z_unified_deficit_field_static_branch_gate.py"
        ),
        "selected_action_status": selected["status"],
        "selected_action": action,
        "selected_sectors": [
            "Einstein-Hilbert metric sector",
            "phase-normalized F_min(Yhat,I1hat,I2hat,I3hat)",
            "projected H-gradient sector",
        ],
        "required_token_checks": required_present,
        "excluded_token_checks": excluded_absent,
        "excluded_from_selected_action": [
            "p02c lambda_S*(S-6)^2 completion",
            "p02c/p03c phase-solid ESS operator c_Z*delta_AB*(u.d phi^A)*(u.d phi^B)",
        ],
        "scenario_rule": (
            "ESS/S6 results are optional alternative-completion diagnostics. "
            "They are not premises of the selected p05z static branch."
        ),
    }


def ess_whole_solution_covariant_boost_gate() -> dict[str, Any]:
    """Exact covariance audit for a boost of the entire static solution.

    Work in the boost direction of an isotropic static metric

        q_bar^{ab}=diag(1/B,-1/D),  a,b in {T,X},

    with Phi_bar=T, phi_bar=X and H_bar=H(X).  Pull back the metric and every
    scalar by the same Lorentz/diffeomorphism boost.  Because
    C=u.d(phi) and X_H=u.d(H) are spacetime scalars which vanish before the
    boost, they must remain zero.  The explicit matrix calculation below also
    shows the cancellation.

    In inverse-metric PN notation

        q^{00}=1+p,  q^{ij}=-delta^{ij}+k^{ij},

    the whole-solution boost generates

        h_i=q^{0i}=(p delta_ij+k_ij) w_j.

    This is precisely the term needed to cancel the apparent rigid-seed
    C_i=h_i-(p delta_ij+k_ij)w_j.
    """

    B_metric, D_metric = sp.symbols(
        "B_metric D_metric",
        positive=True,
        real=True,
    )
    w = sp.Symbol("w", real=True)
    gamma_w = 1 / sp.sqrt(1 - w**2)

    # Old/static coordinates y=(T,X) and new coordinates x=(t,x):
    # y=Lambda*x with T=Gamma(t-wx), X=Gamma(x-wt).
    boost = sp.Matrix(
        [
            [gamma_w, -gamma_w * w],
            [-gamma_w * w, gamma_w],
        ]
    )
    inverse_boost = sp.Matrix(
        [
            [gamma_w, gamma_w * w],
            [gamma_w * w, gamma_w],
        ]
    )
    q_static = sp.diag(1 / B_metric, -1 / D_metric)
    q_boosted = (
        inverse_boost * q_static * inverse_boost.T
    ).applyfunc(sp.simplify)

    d_phi_clock = boost.row(0).T
    d_phi_solid = boost.row(1).T
    Y_boosted = sp.factor(
        (d_phi_clock.T * q_boosted * d_phi_clock)[0]
    )
    numerator_C = sp.factor(
        (d_phi_solid.T * q_boosted * d_phi_clock)[0]
    )
    C_exact = sp.simplify(numerator_C / sp.sqrt(Y_boosted))

    H_x = sp.Symbol("H_x", real=True)
    d_H = H_x * d_phi_solid
    phase_H_contraction = sp.factor(
        (d_H.T * q_boosted * d_phi_clock)[0]
        / sp.sqrt(Y_boosted)
    )

    expected_q01 = sp.simplify(
        gamma_w**2
        * w
        * (1 / B_metric - 1 / D_metric)
    )
    exact_q01_residual = sp.simplify(
        q_boosted[0, 1] - expected_q01
    )

    p, k, U, gamma_ppn = sp.symbols(
        "p k U gamma_PPN",
        real=True,
    )
    q_static_pk = sp.diag(1 + p, -1 + k)
    q_boosted_pk = (
        inverse_boost * q_static_pk * inverse_boost.T
    ).applyfunc(sp.simplify)
    h_linear = sp.simplify(
        sp.diff(q_boosted_pk[0, 1], w).subs(w, 0) * w
    )
    expected_h_linear = sp.expand((p + k) * w)
    C_linear_on_whole_boost = sp.simplify(
        h_linear - (p + k) * w
    )
    h_linear_newtonian = sp.simplify(
        h_linear.subs(
            {
                p: 2 * U,
                k: 2 * gamma_ppn * U,
            }
        )
    )

    # p05z uses Yhat=e^(-2H)Y but u_m=d_m Phi/sqrt(Y).  Even if
    # the normalized one-form e^(-H)dPhi is used, normalization cancels H.
    H, sqrt_Y = sp.symbols("H sqrt_Y", positive=True, real=True)
    u_hat_scale = sp.simplify(
        sp.exp(-H) / (sp.exp(-H) * sqrt_Y)
    )
    u_scale = 1 / sqrt_Y
    H_normalization_residual = sp.simplify(u_hat_scale - u_scale)

    passed = (
        sp.simplify(Y_boosted - 1 / B_metric) == 0
        and numerator_C == 0
        and C_exact == 0
        and phase_H_contraction == 0
        and exact_q01_residual == 0
        and sp.simplify(h_linear - expected_h_linear) == 0
        and C_linear_on_whole_boost == 0
        and sp.simplify(
            h_linear_newtonian
            - 2 * (1 + gamma_ppn) * U * w
        )
        == 0
        and H_normalization_residual == 0
    )

    return {
        "status": (
            "PASS_WHOLE_SOLUTION_COVARIANT_BOOST__C_A_ZERO__"
            "H_EQUALS_P_PLUS_K_TIMES_W"
            if passed
            else "CHECK_WHOLE_SOLUTION_COVARIANT_BOOST"
        ),
        "signature": "(+---)",
        "boost_convention": (
            "T=Gamma*(t-w*x), X=Gamma*(x-w*t); reversing the convention "
            "reverses both h and w and leaves the cancellation unchanged"
        ),
        "static_inverse_metric": q_static,
        "boosted_inverse_metric": q_boosted,
        "boosted_clock_gradient": d_phi_clock,
        "boosted_solid_gradient": d_phi_solid,
        "Y_after_whole_solution_boost": Y_boosted,
        "C_numerator_after_whole_solution_boost": numerator_C,
        "C_A_after_whole_solution_boost": C_exact,
        "u_dot_dH_after_whole_solution_boost": phase_H_contraction,
        "boosted_q0i_exact_representative": q_boosted[0, 1],
        "boosted_q0i_exact_expected": expected_q01,
        "boosted_q0i_exact_residual": exact_q01_residual,
        "boosted_q0i_linear": h_linear,
        "boosted_q0i_linear_expected": expected_h_linear,
        "boosted_q0i_on_Newtonian_branch": h_linear_newtonian,
        "C_A_linear_on_whole_solution_boost": C_linear_on_whole_boost,
        "H_normalization_residual_in_u": H_normalization_residual,
        "all_internal_components": (
            "The displayed exact block is the boost direction.  Transverse "
            "solid labels have zero contraction, and internal O(3) covariance "
            "extends C_A=0 to A=1,2,3."
        ),
        "covariant_reason": (
            "C_A and u.dH are spacetime scalars.  A common pullback of metric, "
            "Phi, phi^A and H cannot turn their static zero into a source."
        ),
    }


def ess_moving_vector_operator_gate() -> dict[str, Any]:
    """Unreduced quadratic Hessian of the optional ESS completion.

    At linear order

        C_A = u^m d_m phi^A
            = q^{0A} + dot(pi_A) - d_A chi,

        L_ESS^(2) = eta C_A C_A.

    It has no vector tadpole at the background, but its q^{0i} Hessian is
    2*eta*delta_ij before constraints are reduced.  This is a valid optional
    completion diagnostic.  It is not part of the selected p05z action, and an
    h-only Hessian is not yet a physical vector Green operator: Phi/phi/H,
    lapse and shift constraints must first be eliminated.
    """

    eta = sp.Symbol("eta_ESS", positive=True)
    h = sp.Matrix(sp.symbols("h_1:4", real=True))
    pi_dot = sp.Matrix(sp.symbols("piDot_1:4", real=True))
    grad_chi = sp.Matrix(sp.symbols("gradChi_1:4", real=True))
    C = sp.simplify(h + pi_dot - grad_chi)
    l2 = sp.expand(eta * C.dot(C))

    variables = tuple(h) + tuple(pi_dot) + tuple(grad_chi)
    source_h = sp.Matrix([sp.diff(l2, item) for item in h])
    h_hessian = sp.Matrix(
        3,
        3,
        lambda i, j: sp.diff(source_h[i], h[j]),
    )
    full_hessian = sp.hessian(l2, variables)
    background = {
        **{item: 0 for item in h},
        **{item: 0 for item in pi_dot},
        **{item: 0 for item in grad_chi},
    }
    tadpole = source_h.subs(background).applyfunc(sp.simplify)
    lock_subs = {
        pi_dot[i]: -h[i] + grad_chi[i]
        for i in range(3)
    }
    source_on_convective_lock = source_h.subs(lock_subs).applyfunc(sp.simplify)

    # The co-boost used in the old p03 smoke test has grad(chi)=pi_dot=v.
    v = sp.Matrix(sp.symbols("v_1:4", real=True))
    co_boost_subs = {
        **{pi_dot[i]: v[i] for i in range(3)},
        **{grad_chi[i]: v[i] for i in range(3)},
    }
    co_boost_l2 = sp.simplify(l2.subs(co_boost_subs))
    co_boost_source = source_h.subs(co_boost_subs).applyfunc(sp.simplify)

    expected_hessian = 2 * eta * sp.eye(3)
    passed = (
        _all_zero(list(tadpole))
        and h_hessian == expected_hessian
        and full_hessian.rank() == 3
        and _all_zero(list(source_on_convective_lock))
        and sp.simplify(co_boost_l2 - eta * h.dot(h)) == 0
        and _all_zero(list(co_boost_source - 2 * eta * h))
    )

    return {
        "status": (
            "PASS_OPTIONAL_ESS_UNREDUCED_QUADRATIC_HESSIAN__"
            "REDUCED_VECTOR_EFFECT_OPEN"
            if passed
            else "CHECK_ESS_MOVING_VECTOR_OPERATOR"
        ),
        "action_scope": "OPTIONAL_COMPLETION_NOT_IN_SELECTED_P05Z_ACTION",
        "linear_convective_strain_C_A": C,
        "quadratic_ESS_lagrangian": l2,
        "q0i_variation": source_h,
        "background_vector_tadpole": tadpole,
        "q0i_operator_hessian": h_hessian,
        "expected_q0i_operator_hessian": expected_hessian,
        "full_hessian_rank": full_hessian.rank(),
        "co_boost_lagrangian": co_boost_l2,
        "co_boost_q0i_variation": co_boost_source,
        "convective_lock_condition": "C_A=0, i.e. dot(pi_A)=-q0A+d_A chi",
        "q0i_variation_on_convective_lock": source_on_convective_lock,
        "decisive_distinction": (
            "The background tadpole is zero while the unreduced coupled Hessian "
            "is nonzero.  Whether a physical vector operator remains after "
            "constraints and convective lock are imposed is not derived here."
        ),
        "required_closure": (
            "If ESS is selected in a future action, perform the ADM/Dirac "
            "reduction, derive C_A from the full inhomogeneous equations and "
            "boundary conditions, and only then match alpha_1, alpha_2 and "
            "frame dragging."
        ),
        "legacy_status_replaced": (
            "OPEN_FULL_ACTION_VECTOR_PPN__ESS_HAS_ZERO_TADPOLE_BUT_"
            "NONZERO_OPERATOR_HESSIAN"
        ),
    }


def first_derivative_static_silent_operator_classification_gate() -> dict[str, Any]:
    """Classify analytic O(3) static-silent first-derivative cross operators.

    For the same supersolid fields, every O(3)-scalar cross invariant can be
    generated locally by

        y_n = C^T B^n C,  n=0,1,2,
        C^A = u.d phi^A.

    Around C=0, B=I+eps*E, all y_n have the same quadratic term.  Therefore a
    new analytic first-derivative operator made only from these fields can only
    rescale ESS/Z at quadratic order; it cannot independently repair the
    kinetic/mixing entries while remaining exactly static-silent.
    """

    eps = sp.Symbol("eps", real=True)
    e11, e22, e33, e12, e13, e23 = sp.symbols(
        "E_11 E_22 E_33 E_12 E_13 E_23",
        real=True,
    )
    E = sp.Matrix(
        [
            [e11, e12, e13],
            [e12, e22, e23],
            [e13, e23, e33],
        ]
    )
    c1, c2, c3 = sp.symbols("c_1 c_2 c_3", real=True)
    c_vec = sp.Matrix([c1, c2, c3])
    C = eps * c_vec
    B = sp.eye(3) + eps * E
    invariants = {
        f"y_{n}": sp.expand((C.T * (B**n) * C)[0])
        for n in range(3)
    }
    quadratic = {
        name: sp.factor(expr.coeff(eps, 2))
        for name, expr in invariants.items()
    }
    cubic = {
        name: sp.factor(expr.coeff(eps, 3))
        for name, expr in invariants.items()
    }
    common_quadratic = sp.expand(c_vec.dot(c_vec))
    quadratic_residuals = {
        name: sp.simplify(value - common_quadratic)
        for name, value in quadratic.items()
    }

    a0, a1, a2 = sp.symbols("a_0 a_1 a_2", real=True)
    analytic_linear_combination = sp.expand(
        a0 * invariants["y_0"]
        + a1 * invariants["y_1"]
        + a2 * invariants["y_2"]
    )
    combined_quadratic = sp.factor(
        analytic_linear_combination.coeff(eps, 2)
    )
    expected_combined = sp.expand((a0 + a1 + a2) * common_quadratic)
    passed = (
        _all_zero(quadratic_residuals.values())
        and sp.simplify(combined_quadratic - expected_combined) == 0
        and sp.simplify(cubic["y_1"] - (c_vec.T * E * c_vec)[0]) == 0
        and sp.simplify(cubic["y_2"] - 2 * (c_vec.T * E * c_vec)[0]) == 0
    )

    return {
        "status": (
            "PASS_ONE_DERIVATIVE_O3_STATIC_SILENT_OPERATOR_CLASSIFICATION__"
            "INDEPENDENT_QUADRATIC_REPAIR_NO_GO"
            if passed
            else "CHECK_STATIC_SILENT_OPERATOR_CLASSIFICATION"
        ),
        "action_scope": (
            "OPTIONAL_COMPLETION_CLASSIFICATION__"
            "NOT_A_SELECTED_P05Z_ACTION_REQUIREMENT"
        ),
        "invariants": invariants,
        "quadratic_terms": quadratic,
        "cubic_terms": cubic,
        "common_quadratic_term": common_quadratic,
        "quadratic_residuals": quadratic_residuals,
        "general_analytic_combination_quadratic": combined_quadratic,
        "classification_scope": (
            "analytic, first-derivative, internal-O(3)-invariant operators made "
            "from the existing Phi, phi^A and metric fields near C^A=0"
        ),
        "no_go": (
            "Within this class, another exactly static-silent cross operator is "
            "ESS/Z again at quadratic order.  It cannot supply independent "
            "principal-matrix shifts."
        ),
        "escape_routes": [
            "allow a controlled nonzero static shear operator and bound its Solar effect",
            "use a degenerate higher-derivative projected operator with a full ghost/constraint audit",
            "add a genuinely new field or response channel",
            "derive a nontrivial H constraint that changes the reduced principal symbol",
        ],
    }


def ess_boosted_newtonian_preferred_frame_gate() -> dict[str, Any]:
    """Off-shell rigid-relative ESS residual in a source-rest Newtonian seed.

    Keep a diagonal source-rest Newtonian metric while rigidly tilting the
    asymptotic phase/solid coframe by w.  With

        dq00 = p = 2U,
        dqij = k_ij = 2 gamma U delta_ij.

    The ESS convective strain contains

        C_i = h_i - (p delta_ij + k_ij) w_j
            = h_i - 2(1+gamma) U w_i.

    At h_i=0 this seed has an O(U w_i) Euler residual.  It is not a boost of the
    whole solution: the common metric/field boost generates

        h_i=(p delta_ij+k_ij)w_j,

    and then C_i and the ESS first variation vanish.  The h=0 residual is useful
    input to a coupled physical-relative boundary-value problem, but it is not
    an unavoidable preferred-frame source and it does not determine alpha_i.
    """

    eta = sp.Symbol("eta_ESS", positive=True)
    U, gamma = sp.symbols("U gamma", real=True)
    h = sp.Matrix(sp.symbols("h_1:4", real=True))
    w = sp.Matrix(sp.symbols("w_1:4", real=True))
    p = 2 * U
    k = 2 * gamma * U * sp.eye(3)
    C = sp.simplify(h - (p * sp.eye(3) + k) * w)
    l2 = sp.expand(eta * C.dot(C))
    source_h = sp.Matrix([sp.diff(l2, item) for item in h])
    source_at_h_zero = source_h.subs(
        {item: 0 for item in h}
    ).applyfunc(sp.simplify)
    expected_C = sp.simplify(h - 2 * (1 + gamma) * U * w)
    expected_source = sp.simplify(-4 * eta * (1 + gamma) * U * w)
    source_gamma_one = source_at_h_zero.subs(gamma, 1).applyfunc(sp.simplify)
    h_whole_boost = sp.simplify((p * sp.eye(3) + k) * w)
    whole_boost_subs = {
        h[i]: h_whole_boost[i]
        for i in range(3)
    }
    C_on_whole_boost = C.subs(whole_boost_subs).applyfunc(sp.simplify)
    source_on_whole_boost = source_h.subs(
        whole_boost_subs
    ).applyfunc(sp.simplify)
    l2_on_whole_boost = sp.simplify(l2.subs(whole_boost_subs))
    covariance = ess_whole_solution_covariant_boost_gate()
    passed = (
        _all_zero(list(C - expected_C))
        and _all_zero(list(source_at_h_zero - expected_source))
        and _all_zero(list(source_gamma_one + 8 * eta * U * w))
        and _all_zero(list(C_on_whole_boost))
        and _all_zero(list(source_on_whole_boost))
        and l2_on_whole_boost == 0
        and covariance["status"]
        == (
            "PASS_WHOLE_SOLUTION_COVARIANT_BOOST__C_A_ZERO__"
            "H_EQUALS_P_PLUS_K_TIMES_W"
        )
    )

    return {
        "status": (
            "PASS_ESS_RIGID_RELATIVE_SEED_UW_OFFSHELL_RESIDUAL__"
            "WHOLE_SOLUTION_BOOST_CANCELS"
            if passed
            else "CHECK_ESS_RIGID_RELATIVE_SEED"
        ),
        "action_scope": "OPTIONAL_COMPLETION_NOT_IN_SELECTED_P05Z_ACTION",
        "Newtonian_inverse_metric": {
            "dq00": p,
            "dqij": k,
        },
        "convective_strain": C,
        "quadratic_ESS_lagrangian": l2,
        "q0i_variation": source_h,
        "q0i_variation_at_h_zero": source_at_h_zero,
        "q0i_variation_at_gamma_one": source_gamma_one,
        "h_on_whole_solution_boost": h_whole_boost,
        "convective_strain_on_whole_solution_boost": C_on_whole_boost,
        "q0i_variation_on_whole_solution_boost": source_on_whole_boost,
        "ESS_lagrangian_on_whole_solution_boost": l2_on_whole_boost,
        "whole_solution_covariance_gate": covariance["status"],
        "meaning": (
            "Freezing h=0 and the rigidly boosted coframe produces a bare U*w "
            "residual.  A common diffeomorphism boost of metric, Phi, phi^A and "
            "H instead has h=(p+k)w and C_A=0.  The residual is therefore an "
            "off-shell seed for a physical-relative solve, not a coordinate-"
            "boost source."
        ),
        "not_an_alpha_value": (
            "The induced Phi/phi/H response and reduced metric constraints may "
            "cancel the seed residual.  Only the complete physical-relative "
            "solution can fix alpha_1 or alpha_2."
        ),
        "legacy_status_replaced": (
            "PASS_ESS_BOOSTED_NEWTONIAN_UW_SOURCE_DERIVED__"
            "GLOBAL_PPN_SOLUTION_OPEN"
        ),
    }


def ess_stationary_vector_scale_gate() -> dict[str, Any]:
    """Conditional scale estimate for an optional unreduced ESS scenario.

    In a stationary transverse unitary-gauge reduction the operator has the
    schematic form

        (nabla^2 - mu_Z^2) h_i = matter source,
        mu_Z^2 = 4 eta_ESS / M_Pl^2,

    up to the sign convention of the full action.  This unitary-gauge schematic
    operator has not been obtained after the Phi/phi/H and ADM constraints are
    reduced.  Moreover ESS is absent from the selected p05z action.  The scale
    estimate is retained only for an explicitly selected future ESS scenario.
    """

    H0_s = 67.4 * 1000.0 / 3.085677581491367e22
    c_m_s = 299_792_458.0
    au_m = 149_597_870_700.0
    r_sun_m = 6.957e8
    au_suppression = (H0_s * au_m / c_m_s) ** 2
    solar_radius_suppression = (H0_s * r_sun_m / c_m_s) ** 2

    eta, M_Pl = sp.symbols("eta_ESS M_Pl", positive=True)
    mu_sq = sp.simplify(4 * eta / M_Pl**2)
    return {
        "status": (
            "CONDITIONAL_OPTIONAL_ESS_UNITARY_GAUGE_SCALE_ESTIMATE__"
            "REDUCED_OPERATOR_AND_ETA_NORMALIZATION_NOT_DERIVED"
        ),
        "action_scope": "OPTIONAL_COMPLETION_NOT_IN_SELECTED_P05Z_ACTION",
        "stationary_vector_operator": "(nabla^2-mu_Z^2) h_i = source_i",
        "mu_Z_squared": mu_sq,
        "conditional_scale_identification": "eta_ESS/M_Pl^2 = O(H0^2)",
        "H0_per_second_used": H0_s,
        "suppression_at_1_AU": au_suppression,
        "suppression_at_solar_radius": solar_radius_suppression,
        "reading": (
            "If a future reduced ESS action retained this operator and derived "
            "eta at the dark-energy scale, its local correction would be tiny. "
            "Neither premise is established by the selected action."
        ),
    }


def healthy_near_gr_cosmological_suppression_route_gate() -> dict[str, Any]:
    """Alternative raw-coefficient scenario away from the exact-GR slice.

    On the p03 static 1PN family

        K_Phi = 2c+d,
        K_pi  = 2c-d,

    where c=c_Y2 and d=c_YI1.  Put d=2c-kappa_pi.  Then

        K_pi=kappa_pi,
        K_Phi=4c-kappa_pi,

    so 0<kappa_pi<4c is a nonempty window in the displayed unreduced kinetic
    coefficients.  This is not yet a no-ghost theorem: the constrained ADM/
    Dirac reduction is still required.  The exact p03c GR slice is the distinct
    kappa_pi=0 scenario.  Moving inside the raw window relaxes exact static
    silence; if every coefficient scale is action-derived to be O(H0^2), the
    resulting local response may be organized by H0^2 L^2.

    This is a development route, not a PPN solution: core matching must exclude
    unsuppressed homogeneous 1/r scalar/vector charges, and the full principal
    symbol must still be checked.
    """

    c, kappa_pi = sp.symbols("c_Y2 kappa_pi", positive=True)
    d = sp.simplify(2 * c - kappa_pi)
    K_phi = sp.simplify(2 * c + d)
    K_pi = sp.simplify(2 * c - d)
    exact_gr_boundary = sp.simplify(
        d.subs(kappa_pi, 0) - 2 * c
    )

    witness = {
        c: sp.Integer(1),
        kappa_pi: sp.Rational(1, 2),
    }
    witness_values = {
        "c_YI1": sp.simplify(d.subs(witness)),
        "K_Phi": sp.simplify(K_phi.subs(witness)),
        "K_pi": sp.simplify(K_pi.subs(witness)),
    }
    witness_healthy = (
        witness_values["K_Phi"] > 0
        and witness_values["K_pi"] > 0
    )

    H0_s = 67.4 * 1000.0 / 3.085677581491367e22
    c_m_s = 299_792_458.0
    au_m = 149_597_870_700.0
    r_sun_m = 6.957e8
    suppression = {
        "solar_radius": (H0_s * r_sun_m / c_m_s) ** 2,
        "one_AU": (H0_s * au_m / c_m_s) ** 2,
    }
    passed = (
        K_pi == kappa_pi
        and K_phi == 4 * c - kappa_pi
        and exact_gr_boundary == 0
        and bool(witness_healthy)
        and suppression["one_AU"] < 1.0e-28
    )

    return {
        "status": (
            "PASS_NONEMPTY_NEAR_GR_RAW_KINETIC_SCENARIO__"
            "ALTERNATIVE_NOT_CONJOINED__REDUCED_DYNAMICS_AND_PPN_OPEN"
            if passed
            else "CHECK_NEAR_GR_KPI_POSITIVE_ROUTE"
        ),
        "scenario_role": (
            "ALTERNATIVE_TO_EXACT_GR_SLICE__NOT_A_MASTER_PASS_REQUIREMENT"
        ),
        "parameterization": {
            "c": c,
            "d_equals_c_YI1": d,
            "kappa_pi": kappa_pi,
        },
        "kinetic_coefficients": {
            "K_Phi": K_phi,
            "K_pi": K_pi,
        },
        "algebraic_window": sp.And(kappa_pi > 0, kappa_pi < 4 * c),
        "exact_GR_slice": sp.Eq(kappa_pi, 0),
        "explicit_window_witness": witness_values,
        "witness_positive_raw_coefficients": bool(witness_healthy),
        "witness_healthy": bool(witness_healthy),
        "conditional_scale_lock": (
            "c/M_Pl^2, kappa_pi/M_Pl^2 and every active completion scale "
            "must be derived as O(H0^2), not fitted independently"
        ),
        "H0_squared_L_squared": suppression,
        "why_promising": (
            "As a separate scenario, this route gives positive displayed raw "
            "coefficients and permits a small non-static-silent response.  It "
            "does not certify the exact-GR branch or the reduced spectrum."
        ),
        "still_required": [
            "derive the coefficient scale lock from one cosmological/local action",
            "solve the near-slice static exterior and quantify beta,gamma shifts",
            "prove a nondefective coupled principal symbol without the old ESS-only shortcut",
            "match a regular finite source and eliminate unsuppressed homogeneous charges",
            "solve and gauge-match the complete ten-parameter PPN system",
        ],
    }


def standard_ppn_metric_contract() -> dict[str, Any]:
    """Ten-parameter standard PPN coefficient contract.

    Coefficients are written in the conventional Will-Nordtvedt (-+++) PPN
    metric.  RefG uses (+---); the overall signature conversion changes metric
    signs but not the parameter solution.
    """

    gamma, beta, xi = sp.symbols("gamma beta xi", real=True)
    alpha1, alpha2, alpha3 = sp.symbols(
        "alpha_1 alpha_2 alpha_3",
        real=True,
    )
    zeta1, zeta2, zeta3, zeta4 = sp.symbols(
        "zeta_1 zeta_2 zeta_3 zeta_4",
        real=True,
    )
    parameters = (
        gamma,
        beta,
        xi,
        alpha1,
        alpha2,
        alpha3,
        zeta1,
        zeta2,
        zeta3,
        zeta4,
    )

    coefficients = {
        "gij_U": 2 * gamma,
        "g00_U2": -2 * beta,
        "g00_PhiW": -2 * xi,
        "g00_Phi1": 2 * gamma + 2 + alpha3 + zeta1 - 2 * xi,
        "g00_Phi2": 2 * (3 * gamma - 2 * beta + 1 + zeta2 + xi),
        "g00_Phi3": 2 * (1 + zeta3),
        "g00_Phi4": 2 * (3 * gamma + 3 * zeta4 - 2 * xi),
        "g00_A": -(zeta1 - 2 * xi),
        "g0i_Vi": -sp.Rational(1, 2)
        * (4 * gamma + 3 + alpha1 - alpha2 + zeta1 - 2 * xi),
        "g0i_Wi": -sp.Rational(1, 2)
        * (1 + alpha2 - zeta1 + 2 * xi),
        "g0i_wiU": -sp.Rational(1, 2) * (alpha1 - 2 * alpha2),
        "g0i_wjUij": -alpha2,
        "g00_w2U": -(alpha1 - alpha2 - alpha3),
        "g00_wiwjUij": -alpha2,
        "g00_wiVi": 2 * alpha3 - alpha1,
    }
    gr_targets = {
        "gij_U": sp.Integer(2),
        "g00_U2": sp.Integer(-2),
        "g00_PhiW": sp.Integer(0),
        "g00_Phi1": sp.Integer(4),
        "g00_Phi2": sp.Integer(4),
        "g00_Phi3": sp.Integer(2),
        "g00_Phi4": sp.Integer(6),
        "g00_A": sp.Integer(0),
        "g0i_Vi": -sp.Rational(7, 2),
        "g0i_Wi": -sp.Rational(1, 2),
        "g0i_wiU": sp.Integer(0),
        "g0i_wjUij": sp.Integer(0),
        "g00_w2U": sp.Integer(0),
        "g00_wiwjUij": sp.Integer(0),
        "g00_wiVi": sp.Integer(0),
    }
    equations = [
        sp.Eq(coefficients[name], target)
        for name, target in gr_targets.items()
    ]
    solution = sp.solve(equations, parameters, dict=True)
    first_solution = solution[0] if solution else {}
    residuals = [
        sp.simplify((equation.lhs - equation.rhs).subs(first_solution))
        for equation in equations
    ]
    expected_solution = {
        gamma: 1,
        beta: 1,
        xi: 0,
        alpha1: 0,
        alpha2: 0,
        alpha3: 0,
        zeta1: 0,
        zeta2: 0,
        zeta3: 0,
        zeta4: 0,
    }
    passed = (
        first_solution == expected_solution
        and _all_zero(residuals)
    )

    return {
        "status": (
            "PASS_STANDARD_PPN_TEN_PARAMETER_MATCHING_CONTRACT"
            if passed
            else "CHECK_STANDARD_PPN_MATCHING_CONTRACT"
        ),
        "signature_convention": (
            "coefficients displayed in standard (-+++) PPN convention; "
            "RefG (+---) uses the signature-reversed metric"
        ),
        "required_metric_orders": {
            "gij": "O(v^2)",
            "g0i": "O(v^3)",
            "g00": "O(v^4)",
        },
        "parameters": parameters,
        "coefficients": coefficients,
        "GR_targets": gr_targets,
        "matching_equations": equations,
        "solution": solution,
        "residuals": residuals,
        "meaning": (
            "A full PPN claim requires deriving every coefficient in this table "
            "from the same inhomogeneous action solution.  Inserting GR vector "
            "coefficients into this algebra only proves a conditional matcher."
        ),
    }


def static_spherical_ppn_rank_theorem() -> dict[str, Any]:
    """Static point-mass exterior sees only beta and gamma out of ten PPN rows."""

    gamma, beta, xi = sp.symbols("gamma beta xi", real=True)
    alpha1, alpha2, alpha3 = sp.symbols(
        "alpha_1 alpha_2 alpha_3",
        real=True,
    )
    zeta1, zeta2, zeta3, zeta4 = sp.symbols(
        "zeta_1 zeta_2 zeta_3 zeta_4",
        real=True,
    )
    parameters = (
        gamma,
        beta,
        xi,
        alpha1,
        alpha2,
        alpha3,
        zeta1,
        zeta2,
        zeta3,
        zeta4,
    )
    static_coefficients = sp.Matrix([2 * gamma, 2 * beta])
    jacobian = static_coefficients.jacobian(parameters)
    rank = jacobian.rank()
    nullity = len(parameters) - rank
    passed = rank == 2 and nullity == 8

    return {
        "status": (
            "PASS_STATIC_SPHERICAL_PPN_INFORMATION_RANK_2_OF_10"
            if passed
            else "CHECK_STATIC_SPHERICAL_PPN_RANK"
        ),
        "static_exterior_coefficients": {
            "spatial_U": 2 * gamma,
            "time_U_squared": 2 * beta,
        },
        "jacobian": jacobian,
        "rank": rank,
        "nullity": nullity,
        "identified_by_static_exterior": ["gamma", "beta"],
        "not_identified_by_static_exterior": [
            "xi",
            "alpha_1",
            "alpha_2",
            "alpha_3",
            "zeta_1",
            "zeta_2",
            "zeta_3",
            "zeta_4",
        ],
        "reading": (
            "No amount of rechecking a single static spherical metric can close "
            "the missing eight standard-PPN directions."
        ),
    }


def full_1pn_ppn_closure_status() -> dict[str, Any]:
    """Objective-wide status assembled from the active Solar/action gates."""

    from p03_solar import (
        ppn_time_coefficient_convention_bridge,
        solar_1pn_branch_derivation_theorem,
    )
    from p03c_exterior_field_equation import (
        augmented_medium_strain_2pn_system,
        static_silent_ess_kinetic_lift_theorem,
    )
    from p05z_unified_deficit_field_static_branch_gate import (
        derive_unified_H_weak_solar_static_gate,
    )
    from p13_refractive_force import (
        minimal_point_particle_action_bridge,
        p10_asymptotic_charge_normalization,
    )
    from p03f_independent_1pn_completeness_audit import (
        selected_action_sign_convention_audit,
        uniform_static_power_counting_audit,
        unreduced_null_direction_audit,
    )

    normal = solar_fmin_normal_form_theorem()
    general_motion = general_branch_quadratic_motion_theorem()
    linear = linearized_minimal_fmin_decoupling_theorem()
    action_provenance = selected_p05z_action_provenance_gate()
    whole_boost = ess_whole_solution_covariant_boost_gate()
    ess = ess_moving_vector_operator_gate()
    operator_classification = (
        first_derivative_static_silent_operator_classification_gate()
    )
    rigid_relative_seed = ess_boosted_newtonian_preferred_frame_gate()
    ess_scale = ess_stationary_vector_scale_gate()
    near_gr_route = healthy_near_gr_cosmological_suppression_route_gate()
    contract = standard_ppn_metric_contract()
    rank = static_spherical_ppn_rank_theorem()

    beta_bridge = ppn_time_coefficient_convention_bridge()
    old_static_derivation = solar_1pn_branch_derivation_theorem()
    augmented_static = augmented_medium_strain_2pn_system()
    weak_static = derive_unified_H_weak_solar_static_gate()
    ess_lift = static_silent_ess_kinetic_lift_theorem()
    matter = minimal_point_particle_action_bridge()
    charge = p10_asymptotic_charge_normalization()
    sign_convention = selected_action_sign_convention_audit()
    nonlinear_null_directions = unreduced_null_direction_audit()
    uniform_power_counting = uniform_static_power_counting_audit()

    conditional_static_branch_pass = (
        normal["status"]
        == "PASS_SOLAR_FMIN_EXACT_NORMAL_FORM_AND_RANK_ONE_QUADRATIC_HESSIAN"
        and general_motion["status"]
        == (
            "PASS_GENERAL_BRANCH_MOVING_BLOCK_AND_EXACT_GR_KPI_ZERO_"
            "UNREDUCED_DEGENERACY"
        )
        and linear["status"]
        == "PASS_MINIMAL_FMIN_LINEAR_ARBITRARY_SHAPE_DECOUPLING_WITH_LOCALIZED_BOUNDARY"
        and action_provenance["status"]
        == (
            "PASS_SELECTED_P05Z_ACTION_PROVENANCE__ESS_S6_EXCLUDED_"
            "ALTERNATIVE_ONLY"
        )
        and beta_bridge["status"]
        == "PASS_AREAL_TO_STANDARD_PPN_BETA_BRIDGE"
        and old_static_derivation["status"] == "PASS"
        and augmented_static["status"]
        == "PASS_AUGMENTED_MEDIUM_STRAIN_2PN_SYSTEM"
        and weak_static["status"]
        == "PASS_UNIFIED_H_WEAK_SOLAR_STATIC_EOM_THROUGH_O_U2"
        and matter["status"]
        == "PASS_MINIMAL_POINT_PARTICLE_ACTION_TO_WEAK_REFRACTIVE_POTENTIAL"
        and charge["status"] == "PASS_P10_ASYMPTOTIC_CHARGE_NORMALIZATION"
        and contract["status"]
        == "PASS_STANDARD_PPN_TEN_PARAMETER_MATCHING_CONTRACT"
        and rank["status"]
        == "PASS_STATIC_SPHERICAL_PPN_INFORMATION_RANK_2_OF_10"
    )
    # These two checks concern the optional ESS/S6 scenario.  They are useful
    # diagnostics, but ESS and S6 are absent from the selected p05z action and
    # therefore must not be premises of the selected-action closure status.
    optional_ess_boost_diagnostics_pass = (
        whole_boost["status"]
        == (
            "PASS_WHOLE_SOLUTION_COVARIANT_BOOST__C_A_ZERO__"
            "H_EQUALS_P_PLUS_K_TIMES_W"
        )
        and rigid_relative_seed["status"]
        == (
            "PASS_ESS_RIGID_RELATIVE_SEED_UW_OFFSHELL_RESIDUAL__"
            "WHOLE_SOLUTION_BOOST_CANCELS"
        )
    )
    selected_action_contains_ess_or_s6 = False
    identified_ess_obstruction = False
    full_ppn_closed = False
    reduced_dynamics_closed = False

    status = (
        "PASS_ZERO_H_STATIC_SPHERICAL_1PN_EOM_BRANCH__"
        "NO_SELECTED_ACTION_ESS_OBSTRUCTION__"
        "SOURCE_MATCHING_FULL_STANDARD_PPN_AND_REDUCED_DYNAMICS_OPEN"
        if (
            conditional_static_branch_pass
            and not selected_action_contains_ess_or_s6
            and not identified_ess_obstruction
            and not full_ppn_closed
            and not reduced_dynamics_closed
        )
        else "CHECK_FULL_1PN_PPN_CLOSURE"
    )

    return {
        "status": status,
        "static_1PN_result": {
            "status": (
                "PASS_ZERO_H_STATIC_EXTERIOR_EOM_BRANCH_THROUGH_O_U2__"
                "FINITE_SOURCE_BRANCH_SELECTION_OPEN"
            ),
            "beta_PPN": sp.Integer(1),
            "gamma_PPN": sp.Integer(1),
            "is_unique_source_selected_prediction": False,
            "H_zero_means_unloaded_zero_exterior_charge": True,
            "finite_source_fixes_H_and_solid_charges": False,
            "uniform_dimensionful_PN_hierarchy_closed": False,
            "unified_H_weak_static_gate": weak_static["status"],
            "areal_to_isotropic_beta_bridge": beta_bridge["status"],
            "minimal_matter_coupling": matter["status"],
            "asymptotic_Newton_charge": charge["status"],
        },
        "selected_action_provenance": action_provenance,
        "new_derivations": {
            "F_min_normal_form": normal,
            "general_branch_moving_block": general_motion,
            "linear_arbitrary_shape_decoupling": linear,
            "whole_solution_covariant_boost": whole_boost,
            "static_silent_operator_classification": operator_classification,
            # Backward-compatible key: the payload is now explicitly
            # reclassified as an off-shell rigid-relative seed.
            "ESS_boosted_Newtonian_preferred_frame_source": (
                rigid_relative_seed
            ),
            "ESS_rigid_relative_seed_offshell_residual": rigid_relative_seed,
            "alternative_near_GR_scenario": near_gr_route,
            "healthy_near_GR_development_route": near_gr_route,
            "static_PPN_information_rank": rank,
            "standard_PPN_contract": contract,
        },
        "completion_conflict": {
            "exact_GR_slice_minimal_Kpi": sp.Integer(0),
            "exact_GR_slice_Kpi_interpretation": (
                "UNREDUCED_DEGENERACY__ADM_DIRAC_STRONG_COUPLING_AUDIT_REQUIRED"
            ),
            "Kpi_zero_is_not_a_ghost_theorem": True,
            "Kpi_zero_does_not_require_ESS_by_itself": True,
            "selected_action_sign_convention": sign_convention,
            "rank_one_and_cubic_saddle_audit": nonlinear_null_directions,
            "uniform_static_power_counting": uniform_power_counting,
            "selected_action_contains_ESS_or_S6": (
                selected_action_contains_ess_or_s6
            ),
            "static_silent_ESS_lift": ess_lift["status"],
            "static_silent_ESS_lift_scope": (
                "OPTIONAL_ISOLATED_DIAGNOSTIC_NOT_IN_SELECTED_P05Z_ACTION"
            ),
            "ESS_moving_vector_operator": ess,
            "ESS_boosted_Newtonian_source": rigid_relative_seed,
            "whole_solution_covariant_boost": whole_boost,
            "optional_ESS_boost_diagnostics_pass": (
                optional_ess_boost_diagnostics_pass
            ),
            "same_field_static_silent_repair_classification": (
                operator_classification["status"]
            ),
            "conditional_cosmological_scale_route": ess_scale,
            "identified_ESS_obstruction": identified_ess_obstruction,
            "verdict": (
                "No ESS obstruction is identified in the selected p05z action "
                "because that action contains neither ESS nor S6.  A common "
                "boost of an optional ESS configuration keeps C_A=0; the U*w "
                "term is only a rigid-relative off-shell seed.  If ESS is added "
                "in a different action, its reduced constraint dynamics must "
                "be solved before drawing a PPN conclusion."
            ),
        },
        "development_scenarios": {
            "selected_exact_static_scenario": {
                "action": action_provenance["selected_action"],
                "Kpi_status": (
                    "ZERO_UNREDUCED__CONSTRAINT_OR_STRONG_COUPLING_AUDIT_OPEN"
                ),
                "next_priority": (
                    "freeze the action sign/scales and matter sector, perform "
                    "ADM/Dirac reduction, match finite-source exterior charges, "
                    "and solve the physical-relative PPN system"
                ),
            },
            "optional_ESS_S6_scenario": {
                "selected": False,
                "unreduced_hessian": ess["status"],
                "whole_boost": whole_boost["status"],
                "rigid_relative_seed": rigid_relative_seed["status"],
            },
            "alternative_near_GR_scenario": near_gr_route,
            "mutual_conjunction_forbidden": True,
        },
        "standard_PPN_parameter_ledger": {
            "gamma": "DERIVED_STATIC_EXTERIOR_VALUE_1",
            "beta": "DERIVED_STATIC_EXTERIOR_VALUE_1",
            "alpha_1": "OPEN_SELECTED_ACTION_PHYSICAL_RELATIVE_SOLUTION",
            "alpha_2": "OPEN_SELECTED_ACTION_PHYSICAL_RELATIVE_SOLUTION",
            "alpha_3": "OPEN_FULL_PPN_EXPORT__NOETHER_ZERO_IS_A_TARGET",
            "xi": "OPEN_PREFERRED_LOCATION_POTENTIAL_MATCH",
            "zeta_1": "OPEN_FULL_MATTER_POTENTIAL_MATCH__CONSERVATION_ZERO_TARGET",
            "zeta_2": "OPEN_FULL_MATTER_POTENTIAL_MATCH__CONSERVATION_ZERO_TARGET",
            "zeta_3": "OPEN_FULL_MATTER_POTENTIAL_MATCH__CONSERVATION_ZERO_TARGET",
            "zeta_4": "OPEN_FULL_MATTER_POTENTIAL_MATCH__CONSERVATION_ZERO_TARGET",
        },
        "full_PPN_closed": full_ppn_closed,
        "reduced_dynamics_closed": reduced_dynamics_closed,
        "identified_ESS_obstruction": identified_ess_obstruction,
        "recommended_development_route": {
            "status": (
                "SELECTED_P05Z_REDUCED_DYNAMICS_FIRST__"
                "NEAR_GR_AND_ESS_S6_ARE_ALTERNATIVE_SCENARIOS"
            ),
            "selected_action_first": [
                "perform ADM/Dirac constraint and degree-of-freedom reduction",
                "determine whether K_pi=0 removes a mode or lowers the strong-coupling scale",
                "solve the physical source-medium relative boundary-value problem",
                "derive the ten standard PPN coefficients",
            ],
            "alternative_near_GR_scenario": near_gr_route,
        },
        "next_decisive_calculation": [
            "promote the selected p05z static action to a frozen dynamical action, or explicitly choose a different completion without mixing scenarios",
            "perform its ADM/Dirac reduction and strong-coupling audit before interpreting K_pi=0",
            "freeze the overall -M_*^4 F_min sign and determine the reduced kinetic signature",
            "bound M_*^4*r^2/M_Pl^2 over the complete source-matching and PPN domain",
            "expand arbitrary conserved matter and all selected fields to gij=O(v^2), g0i=O(v^3), g00=O(v^4)",
            "solve the physical-relative scalar/solid/H constraints with asymptotically normalized boundary data",
            "derive, rather than insert, the V_i, W_i, w_i U, U_ij and nonlinear Phi_A coefficients",
            "map the result to the standard PPN gauge and solve the ten-parameter coefficient contract",
            "only then run Solar ephemeris/LLR/Cassini likelihoods with nuisance parameters",
        ],
        "falsification_branch": (
            "The exact static scenario fails if its reduced selected-action "
            "dynamics has an unacceptable strong-coupling scale or its physical-"
            "relative solution violates preferred-frame/frame-dragging bounds. "
            "An optional ESS scenario is judged only after it is explicitly "
            "selected and reduced; the off-shell U*w seed is not such a verdict."
        ),
        "do_not_claim": [
            "do not call alpha_1=alpha_2=alpha_3=0 derived from the current full action",
            "do not call the rigid-relative h=0 U*w residual an unavoidable preferred-frame source",
            "do not call K_pi=0 a ghost or infer that ESS is required before an ADM/Dirac reduction",
            "do not import the historical +F_min response-Hessian sign as the selected -M_*^4 F_min kinetic sign",
            "do not treat coefficient-wise O(U^2) cancellation as a uniform PN estimate without the M_*^4*r^2/M_Pl^2 hierarchy",
            "do not conjoin the exact-GR and near-GR scenarios as simultaneous premises",
            "do not insert ESS/S6 into the selected p05z action without declaring a new action scenario",
            "do not infer eight missing PPN parameters from the rank-two static spherical exterior",
            "do not call the unloaded H=0 exterior a unique source-selected prediction before finite-core matching",
            "do not turn the conditional dark-energy-scale eta estimate into a derived normalization",
            "do not call a symbolic PPN coefficient matcher an observational likelihood",
        ],
    }


def main() -> int:
    status = full_1pn_ppn_closure_status()
    print("status:", status["status"])
    print("static:", status["static_1PN_result"]["status"])
    print(
        "F_min normal form:",
        status["new_derivations"]["F_min_normal_form"]["status"],
    )
    print(
        "static PPN rank:",
        status["new_derivations"]["static_PPN_information_rank"]["rank"],
        "/ 10",
    )
    print(
        "whole-solution boost:",
        status["new_derivations"]["whole_solution_covariant_boost"]["status"],
    )
    print(
        "selected action provenance:",
        status["selected_action_provenance"]["status"],
    )
    print(
        "optional ESS unreduced sector:",
        status["completion_conflict"]["ESS_moving_vector_operator"]["status"],
    )
    print("full PPN closed:", status["full_PPN_closed"])
    print("reduced dynamics closed:", status["reduced_dynamics_closed"])
    return 0 if status["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
