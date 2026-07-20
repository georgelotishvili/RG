# Notation:
# signature (+---); Y=g^mn Phi_m Phi_n;
# B^AB=-g^mn phi^A_m phi^B_n.

"""Source-first 1PN action audit.

Layer scope (superseded at architecture level by p03h):

This file treats F_min/H as an independently varied extra sector appended to
Einstein-Hilbert plus an already supplied minimally coupled matter source.
Its finite-source cofactor result is therefore a downstream-extra-sector
diagnostic.  If F_min/H is instead the upstream microscopic origin of that
same matter/curvature response, the correct task is to integrate and match it
once into the Einstein effective action, not to add its stress again.  The
trace-square form below remains a control replacement, not the selected
RefG-to-GR bridge.

This file does not replace the selected p05z action.  It isolates the exact
reason why the existing static spherical 1PN branch does not automatically
become a general N-body/standard-PPN theorem, and it tests a minimal
replacement candidate.

On the selected Solar coefficient slice,

    F_selected/c = Theta^2 - 16 det(E),
    Theta = Yhat + Tr(Bhat) - 4,
    E = I - Bhat.

The determinant starts at cubic action order.  It is therefore invisible in
the Minkowski quadratic Hessian and on the specially chosen rank-one static
spherical strain, but its cofactor contributes to the field/stress equations
at quadratic perturbative order.  A sum of two differently oriented rank-one
strains is generically rank two.  More decisively, matching even one regular
finite spherical source generates a first-order finite-size solid tail.  That
tail makes the determinant cofactor and the H source nonzero at 1PN.  Hence
the old zero-charge exterior is an allowed branch, not the generic
finite-source continuation.

The comparison candidate is

    F_trace/c = Theta^2.

For F_trace, the solid equation expanded around the full-rank weak branch
fixes each perturbative Theta coefficient to a spatial constant once the lower
orders vanish; localized normalization then sets it to zero order by order.
With minimally coupled matter, no direct H or material-label source, a regular
center and H->0 at infinity, the projected H equation selects H=0 through the
same PN order.  On an assumed global Theta=0 branch, F_trace and all its first
variations vanish exactly, so the metric equation reduces to Einstein's
equation.  This gives a formal source-first quasi-static 1PN stealth
implication; a moving ten-parameter PPN derivation and a nonlinear PDE
existence/uniqueness theorem for arbitrary strong sources are not claimed.

Important boundary: F_trace is only a candidate until the reduced constraint
structure, kinetic sign/strong-coupling scale, radiative stability, cosmology
and particle/core sectors are re-audited.  In particular, deleting the
determinant removes the cubic cofactor source but does not by itself prove that
the rank-one quadratic sector is a healthy dynamical theory.
"""

from __future__ import annotations

from typing import Any

import sympy as sp


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def selected_vs_trace_square_normal_form_gate() -> dict[str, Any]:
    """Compare the current exact slice with the trace-square candidate."""

    eps, c, dy = sp.symbols("eps c delta_Y", real=True)
    b11, b22, b33, b12, b13, b23 = sp.symbols(
        "b11 b22 b33 b12 b13 b23",
        real=True,
    )
    dB = sp.Matrix(
        [
            [b11, b12, b13],
            [b12, b22, b23],
            [b13, b23, b33],
        ]
    )
    B = sp.eye(3) + eps * dB
    Y = 1 + eps * dy
    theta = sp.expand(Y + sp.trace(B) - 4)
    E = sp.eye(3) - B

    f_selected = sp.expand(c * (theta**2 - 16 * sp.det(E)))
    f_trace = sp.expand(c * theta**2)
    difference = sp.factor(f_selected - f_trace)

    selected_o2 = sp.factor(f_selected.coeff(eps, 2))
    trace_o2 = sp.factor(f_trace.coeff(eps, 2))
    selected_o3 = sp.factor(f_selected.coeff(eps, 3))
    trace_o3 = sp.factor(f_trace.coeff(eps, 3))

    variables = (dy, b11, b22, b33, b12, b13, b23)
    selected_hessian = sp.hessian(selected_o2, variables)
    trace_hessian = sp.hessian(trace_o2, variables)

    Yhat, I1hat = sp.symbols("Yhat I1hat", real=True)
    trace_invariant_form = sp.expand((Yhat + I1hat - 4) ** 2)
    trace_coefficient_map = {
        "constant": sp.Integer(16),
        "Yhat": sp.Integer(-8),
        "Yhat^2": sp.Integer(1),
        "I1hat": sp.Integer(-8),
        "I1hat^2": sp.Integer(1),
        "I2hat": sp.Integer(0),
        "I3hat": sp.Integer(0),
        "Yhat*I1hat": sp.Integer(2),
    }
    reconstructed_trace = (
        trace_coefficient_map["constant"]
        + trace_coefficient_map["Yhat"] * Yhat
        + trace_coefficient_map["Yhat^2"] * Yhat**2
        + trace_coefficient_map["I1hat"] * I1hat
        + trace_coefficient_map["I1hat^2"] * I1hat**2
        + trace_coefficient_map["Yhat*I1hat"] * Yhat * I1hat
    )

    passed = (
        sp.simplify(difference + 16 * c * sp.det(E)) == 0
        and sp.simplify(selected_o2 - trace_o2) == 0
        and sp.simplify(selected_o3 - 16 * c * sp.det(dB)) == 0
        and trace_o3 == 0
        and selected_hessian == trace_hessian
        and selected_hessian.rank() == 1
        and sp.expand(reconstructed_trace - trace_invariant_form) == 0
    )

    return {
        "status": (
            "PASS_SELECTED_AND_TRACE_SQUARE_AGREE_THROUGH_QUADRATIC_ACTION__"
            "DIFFER_AT_CUBIC_DETERMINANT"
            if passed
            else "CHECK_SELECTED_VS_TRACE_SQUARE_NORMAL_FORM"
        ),
        "Theta": theta,
        "E": E,
        "F_selected": f_selected,
        "F_trace": f_trace,
        "selected_minus_trace": difference,
        "quadratic_selected": selected_o2,
        "quadratic_trace": trace_o2,
        "cubic_selected": selected_o3,
        "cubic_trace": trace_o3,
        "quadratic_hessian_rank": selected_hessian.rank(),
        "trace_square_invariant_form": trace_invariant_form,
        "trace_square_coefficient_map": trace_coefficient_map,
        "required_constant_term": sp.Integer(16),
        "constant_warning": (
            "The +16*c constant is essential.  It is absent from the old "
            "seven nonconstant monomials because the selected determinant "
            "normal form cancels it."
        ),
        "reading": (
            "The two actions have the same unit-background value, tadpole and "
            "quadratic response.  The current selected action alone carries the "
            "cubic determinant, whose metric/solid variation starts at O(delta^2)."
        ),
    }


def generic_multisource_cofactor_gate() -> dict[str, Any]:
    """Show why the determinant is silent for one radial strain but not generically."""

    a, b, c = sp.symbols("a b c", real=True)
    rank_one = sp.diag(a, 0, 0)
    two_direction = sp.diag(a, b, 0)

    cofactor_rank_one = rank_one.cofactor_matrix()
    cofactor_two_direction = two_direction.cofactor_matrix()
    selected_B_force_rank_one = 16 * c * cofactor_rank_one
    selected_B_force_two_direction = 16 * c * cofactor_two_direction

    passed = (
        _all_zero(cofactor_rank_one)
        and cofactor_two_direction[2, 2] == a * b
        and selected_B_force_two_direction[2, 2] == 16 * a * b * c
    )

    return {
        "status": (
            "PASS_STATIC_RANK_ONE_SILENCE__GENERIC_TWO_DIRECTION_1PN_"
            "COFACTOR_SOURCE_NONZERO"
            if passed
            else "CHECK_GENERIC_COFACTOR_SOURCE"
        ),
        "rank_one_E": rank_one,
        "rank_one_cofactor": cofactor_rank_one,
        "two_direction_E": two_direction,
        "two_direction_cofactor": cofactor_two_direction,
        "selected_B_force_at_Theta_zero_rank_one": selected_B_force_rank_one,
        "selected_B_force_at_Theta_zero_two_direction": (
            selected_B_force_two_direction
        ),
        "cross_source": sp.Eq(
            sp.Symbol("S_cross"),
            selected_B_force_two_direction[2, 2],
        ),
        "meaning": (
            "The specially chosen zero-C_phi spherical exterior has a rank-one "
            "first-order strain and kills the cofactor.  Two nonparallel source "
            "strains generically produce an O(a*b) cofactor, exactly at the "
            "nonlinear 1PN level."
        ),
    }


def uniform_density_source_matching_promotion_gate() -> dict[str, Any]:
    """Expose the finite-source solid mode hidden by coefficient-wise counting.

    At linear order in areal gauge write

        g_tt=1-y(r),  g_rr=-(1+a(r)),
        phi^A=(r+p(r)) n^A,  H=0.

    The trace constraint is

        Theta_1 = y-a+2 p'+4p/r = 0.

    Regularity gives

        p(r)=r^-2 int_0^r (a-y)s^2 ds/2.

    A uniform-density GR source has a != y in its interior even though a=y in
    the exterior.  Matching therefore produces p=C_phi/r^2 outside.  C_phi is
    proportional to r_s, so this mode is first PN order.  Representing it as
    the old p03c homogeneous coefficient C_s*r_s^2/r^2 makes
    C_s=C_phi/r_s^2 proportional to 1/r_s; treating C_s as O(1) is not a
    uniform finite-source expansion.
    """

    r, x, r_s, R = sp.symbols(
        "r x r_s R",
        positive=True,
        real=True,
    )
    a_int_x = r_s * x**2 / R**3
    y_int_x = r_s * (3 * R**2 - x**2) / (2 * R**3)
    p_int = sp.simplify(
        sp.integrate((a_int_x - y_int_x) * x**2 / 2, (x, 0, r))
        / r**2
    )
    C_phi = sp.simplify(
        sp.integrate((a_int_x - y_int_x) * x**2 / 2, (x, 0, R))
    )

    u = r_s / r
    q = sp.simplify(C_phi / r**3)
    delta_B = sp.diag(-u - 4 * q, 2 * q, 2 * q)
    theta_1 = sp.simplify(u + sp.trace(delta_B))
    cofactor = sp.simplify(delta_B.cofactor_matrix())
    q_over_u = sp.simplify(q / u)

    C_s_old = sp.simplify(C_phi / r_s**2)
    old_homogeneous_displacement = sp.simplify(C_s_old * r_s**2 / r**2)
    matched_displacement = sp.simplify(C_phi / r**2)
    value_matching = sp.simplify(
        p_int.subs(r, R) - matched_displacement.subs(r, R)
    )
    derivative_matching = sp.simplify(
        sp.diff(p_int, r).subs(r, R)
        - sp.diff(matched_displacement, r).subs(r, R)
    )

    passed = (
        C_phi == -r_s * R**2 / 10
        and p_int == r_s * r * (3 * r**2 - 5 * R**2) / (20 * R**3)
        and value_matching == 0
        and derivative_matching == 0
        and theta_1 == 0
        and q_over_u == -R**2 / (10 * r**2)
        and sp.simplify(q_over_u.subs(r, R)) == -sp.Rational(1, 10)
        and cofactor[1, 1] != 0
        and cofactor[2, 2] != 0
        and sp.simplify(
            old_homogeneous_displacement - matched_displacement
        )
        == 0
        and C_s_old == -R**2 / (10 * r_s)
    )

    return {
        "status": (
            "PASS_UNIFORM_DENSITY_CORE_PROMOTES_SOLID_TAIL_TO_FIRST_ORDER__"
            "OLD_C_S_POWER_COUNTING_NONUNIFORM"
            if passed
            else "CHECK_FINITE_SOURCE_SOLID_MODE_PROMOTION"
        ),
        "interior_metric_first_order": {
            "a(r)": r_s * r**2 / R**3,
            "y(r)": r_s * (3 * R**2 - r**2) / (2 * R**3),
        },
        "regular_linear_constraint": (
            "p(r)=r^-2*Integral_0^r[(a-y)s^2/2 ds]"
        ),
        "regular_interior_displacement": sp.Eq(sp.Symbol("p_in"), p_int),
        "matched_C_phi": sp.Eq(sp.Symbol("C_phi"), C_phi),
        "exterior_displacement": sp.Eq(
            sp.Symbol("p_ext"),
            matched_displacement,
        ),
        "surface_value_matching_residual": value_matching,
        "surface_derivative_matching_residual": derivative_matching,
        "exterior_delta_B_eigenvalues": delta_B,
        "Theta_1": theta_1,
        "determinant_cofactor": cofactor,
        "finite_size_strain_ratio_q_over_u": q_over_u,
        "finite_size_ratio_at_surface": q_over_u.subs(r, R),
        "old_C_s_required_by_matching": sp.Eq(sp.Symbol("C_s"), C_s_old),
        "power_counting_warning": (
            "C_s scales as 1/r_s for a regular finite source.  Terms discarded "
            "as higher order when C_s is held O(1) can be promoted into 1PN. "
            "The current determinant cofactor is then active and the H/solid/"
            "metric equations must be re-solved with this matched mode."
        ),
    }


def selected_action_finite_source_residual_gate() -> dict[str, Any]:
    """Solve the selected O(2) solid equation and test its H/stress residual.

    The first-order exterior strain of the matched uniform sphere is

        D_1=diag(-u-4q, 2q, 2q),
        u=r_s/r, q=C_phi/r^3, Theta_1=0.

    For F_selected/c=Theta^2+16 det(D), its matrix response at O(2) is

        P_2=2 Theta_2 I+16 Cof(D_1).

    The radial solid equation fixes the decaying Theta_2.  This gate then
    evaluates the algebraic H bracket and medium stress rather than assuming
    H=0.
    """

    r, r_s = sp.symbols("r r_s", positive=True, real=True)
    C_phi = sp.Symbol("C_phi", real=True)
    k_uq, k_q2 = sp.symbols("k_uq k_q2", real=True)
    u = r_s / r
    q = C_phi / r**3
    D_1 = sp.diag(-u - 4 * q, 2 * q, 2 * q)
    cofactor = sp.simplify(D_1.cofactor_matrix())

    theta_2_trial = k_uq * u * q + k_q2 * q**2
    P_r = sp.simplify(2 * theta_2_trial + 16 * cofactor[0, 0])
    P_t = sp.simplify(2 * theta_2_trial + 16 * cofactor[1, 1])
    radial_solid_residual = sp.factor(
        sp.diff(r**2 * P_r, r) - 2 * r * P_t
    )
    solved_coefficients = sp.solve(
        sp.Poly(
            sp.together(radial_solid_residual * r**5),
            r,
        ).coeffs(),
        (k_uq, k_q2),
        dict=True,
    )
    coefficient_solution = solved_coefficients[0]
    theta_2 = sp.simplify(theta_2_trial.subs(coefficient_solution))
    solved_solid_residual = sp.simplify(
        radial_solid_residual.subs(coefficient_solution)
    )

    trace_cofactor = sp.simplify(sp.trace(cofactor))
    # This is the p05z convention
    # S_H/c=Yhat*F_Y/c-Bhat:F_B/c=-F_H/(2c).
    H_bracket = sp.factor(-4 * theta_2 - 16 * trace_cofactor)
    direct_F_H_over_c = sp.factor(-2 * H_bracket)
    H_bracket_numerator = sp.Poly(
        sp.cancel(H_bracket * r**6 / 32),
        r,
    )
    all_r_zero_solution = sp.solve(
        H_bracket_numerator.all_coeffs(),
        C_phi,
        dict=True,
    )

    stress_t = sp.simplify(4 * theta_2)
    stress_spatial = sp.simplify(
        4 * theta_2 * sp.eye(3) + 32 * cofactor
    )

    matched_C_phi = -r_s * sp.Symbol("R", positive=True, real=True) ** 2 / 10
    matched_H_bracket = sp.factor(H_bracket.subs(C_phi, matched_C_phi))

    passed = (
        coefficient_solution == {k_q2: 0, k_uq: 8}
        and solved_solid_residual == 0
        and theta_2 == 8 * r_s * C_phi / r**4
        and H_bracket
        == 32 * C_phi * (r_s * r**2 + 6 * C_phi) / r**6
        and all_r_zero_solution == [{C_phi: 0}]
        and stress_t == 32 * r_s * C_phi / r**4
        and any(value != 0 for value in stress_spatial)
        and matched_H_bracket != 0
    )

    return {
        "status": (
            "FAIL_CURRENT_DETERMINANT_ZERO_H_SOURCE_SELECTION__"
            "UNIFORM_SPHERE_COUNTEREXAMPLE_CONFIRMED"
            if passed
            else "CHECK_SELECTED_FINITE_SOURCE_COUNTEREXAMPLE"
        ),
        "audit_pass": passed,
        "counterexample_confirmed": passed,
        "current_action_zero_H_GR_continuation_pass": (
            False if passed else None
        ),
        "first_order_strain_D_1": D_1,
        "Theta_1": sp.simplify(u + sp.trace(D_1)),
        "Cof_D_1": cofactor,
        "Tr_Cof_D_1": trace_cofactor,
        "O2_matrix_response_P": sp.simplify(
            2 * theta_2 * sp.eye(3) + 16 * cofactor
        ),
        "radial_solid_equation_residual_before_solving": (
            radial_solid_residual
        ),
        "solved_coefficients": coefficient_solution,
        "Theta_2_selected": theta_2,
        "radial_solid_equation_residual_after_solving": (
            solved_solid_residual
        ),
        "p05z_H_algebraic_bracket_over_c": H_bracket,
        "direct_F_H_over_c": direct_F_H_over_c,
        "H_bracket_zero_for_all_r_only_if": all_r_zero_solution,
        "matched_uniform_sphere_H_bracket": matched_H_bracket,
        "medium_stress_over_M4_c": {
            "Theta^t_t": stress_t,
            "spatial_diagonal": stress_spatial,
        },
        "meaning": (
            "The selected determinant action cannot keep H=0 and zero medium "
            "stress for the regular matched uniform sphere.  The old exterior "
            "zero-charge Schwarzschild algebra remains an allowed special "
            "branch, but it is not generically selected by a finite source."
        ),
    }


def second_order_selected_stress_gate() -> dict[str, Any]:
    """Show that one scalar Theta_2 cannot cancel a generic cofactor stress."""

    a, b = sp.symbols("a b", nonzero=True, real=True)
    theta_2 = sp.Symbol("Theta_2", real=True)
    D_1 = sp.diag(a, b, 0)
    cofactor = D_1.cofactor_matrix()
    stress_t = 4 * theta_2
    stress_spatial = 4 * theta_2 * sp.eye(3) + 32 * cofactor
    theta_from_time = sp.solve(sp.Eq(stress_t, 0), theta_2)[0]
    spatial_after_time = sp.simplify(
        stress_spatial.subs(theta_2, theta_from_time)
    )

    passed = (
        theta_from_time == 0
        and spatial_after_time[2, 2] == 32 * a * b
        and spatial_after_time[2, 2] != 0
    )

    return {
        "status": (
            "PASS_GENERIC_COFACTOR_STRESS_CANNOT_BE_CANCELLED_BY_THETA_2_ALONE"
            if passed
            else "CHECK_SECOND_ORDER_SELECTED_STRESS"
        ),
        "two_direction_D_1": D_1,
        "Cof_D_1": cofactor,
        "time_stress": stress_t,
        "spatial_stress": stress_spatial,
        "Theta_2_for_zero_time_stress": theta_from_time,
        "spatial_stress_after_time_cancellation": spatial_after_time,
        "scope": (
            "This disproves automatic GR stealth at fixed first-order strain. "
            "It does not prove that the full coupled second-order system has no "
            "non-GR solution."
        ),
    }


def finite_source_1pn_metric_scale_boundary_gate() -> dict[str, Any]:
    """Separate coefficient-wise 1PN order from observational amplitude."""

    U, R, M_star, M_Pl = sp.symbols(
        "U R M_star M_Pl",
        positive=True,
        real=True,
    )
    c = sp.Symbol("c", real=True)
    medium_stress_scale = M_star**4 * c * U**2
    metric_response_scale = sp.simplify(
        R**2 * medium_stress_scale / M_Pl**2
    )
    response_over_U2 = sp.simplify(metric_response_scale / U**2)
    expected_ratio = c * M_star**4 * R**2 / M_Pl**2
    response_magnitude_over_U2 = sp.Abs(c) * M_star**4 * R**2 / M_Pl**2
    passed = sp.simplify(response_over_U2 - expected_ratio) == 0

    return {
        "status": (
            "PASS_COEFFICIENTWISE_1PN_VS_OBSERVATIONAL_SCALE_BOUNDARY"
            if passed
            else "CHECK_FINITE_SOURCE_1PN_METRIC_SCALE"
        ),
        "nominal_medium_stress_scale": medium_stress_scale,
        "nominal_metric_response_scale": metric_response_scale,
        "metric_response_over_U2": response_over_U2,
        "signed_dimensionless_response_coefficient": expected_ratio,
        "magnitude_requiring_uniform_domain_bound": (
            response_magnitude_over_U2
        ),
        "meaning": (
            "The counterexample is an exact nonzero O(U^2) coefficient and "
            "therefore breaks exact GR inheritance.  Its physical metric size "
            "is additionally weighted by |c|*M_star^4*R^2/M_Pl^2; without a "
            "source-domain bound on that ratio it must not be called an "
            "observationally unsuppressed 1PN deviation."
        ),
    }


def phase_normalized_trace_square_stealth_gate() -> dict[str, Any]:
    """Prove that Theta=0 kills the candidate density and every first variation."""

    Y, l1, l2, l3 = sp.symbols(
        "Y lambda_1 lambda_2 lambda_3",
        positive=True,
        real=True,
    )
    H, c = sp.symbols("H c", real=True)
    yhat = sp.exp(-2 * H) * Y
    lambdas_hat = [sp.exp(2 * H) * value for value in (l1, l2, l3)]
    theta = sp.simplify(yhat + sum(lambdas_hat) - 4)
    f_trace = sp.expand(c * theta**2)

    derivatives = {
        "F": f_trace,
        "F_Y": sp.diff(f_trace, Y),
        "F_lambda_1": sp.diff(f_trace, l1),
        "F_lambda_2": sp.diff(f_trace, l2),
        "F_lambda_3": sp.diff(f_trace, l3),
        "F_H": sp.diff(f_trace, H),
    }
    mixed_responses = {
        "Theta^t_t": sp.simplify(2 * Y * derivatives["F_Y"] - f_trace),
        "Theta^1_1": sp.simplify(
            2 * l1 * derivatives["F_lambda_1"] - f_trace
        ),
        "Theta^2_2": sp.simplify(
            2 * l2 * derivatives["F_lambda_2"] - f_trace
        ),
        "Theta^3_3": sp.simplify(
            2 * l3 * derivatives["F_lambda_3"] - f_trace
        ),
    }

    # Solve Theta=0 for Y and use it as an exact symbolic substitution.
    theta_zero_subs = {
        Y: sp.exp(2 * H)
        * (4 - sp.exp(2 * H) * (l1 + l2 + l3))
    }
    derivatives_on_constraint = {
        key: sp.simplify(value.subs(theta_zero_subs))
        for key, value in derivatives.items()
    }
    responses_on_constraint = {
        key: sp.simplify(value.subs(theta_zero_subs))
        for key, value in mixed_responses.items()
    }

    h = sp.Symbol("h", real=True)
    compact_subs = {
        H: h,
        Y: sp.exp(2 * h),
        l1: sp.exp(-2 * h),
        l2: sp.exp(-2 * h),
        l3: sp.exp(-2 * h),
    }
    compact_theta = sp.simplify(theta.subs(compact_subs))

    passed = (
        _all_zero(derivatives_on_constraint.values())
        and _all_zero(responses_on_constraint.values())
        and compact_theta == 0
    )

    return {
        "status": (
            "PASS_TRACE_SQUARE_THETA_ZERO_EXACT_STEALTH__"
            "WEAK_AND_COMPACT_ENDPOINTS_RETAINED"
            if passed
            else "CHECK_TRACE_SQUARE_STEALTH"
        ),
        "Yhat": yhat,
        "lambda_hat": lambdas_hat,
        "Theta": theta,
        "F_trace": f_trace,
        "first_variations": derivatives,
        "metric_responses": mixed_responses,
        "Theta_zero_substitution": theta_zero_subs,
        "first_variations_on_Theta_zero": derivatives_on_constraint,
        "metric_responses_on_Theta_zero": responses_on_constraint,
        "weak_endpoint": "H=0 and Y+lambda_1+lambda_2+lambda_3=4",
        "compact_endpoint_Theta": compact_theta,
        "meaning": (
            "On the Theta=0 branch the trace-square sector has zero density, "
            "zero metric stress and zero Phi/phi^A/H source exactly.  The "
            "algebra is shape-independent; source selection of that branch is "
            "proved here only perturbatively under the explicit boundary assumptions."
        ),
    }


def spherical_source_first_embedding_gate() -> dict[str, Any]:
    """Recover the p03c radial response from Theta=0 rather than insert it."""

    r, r_s, eps = sp.symbols("r r_s eps", positive=True, real=True)
    s0, C_s = sp.symbols("s0 C_s", real=True)
    profile = sp.Function("profile")(r)
    u = eps * r_s / r

    A = 1 + u + u**2
    B = 1 - u
    radial_constraint = sp.simplify(
        1 / B
        + sp.diff(profile, r) ** 2 / A
        + 2 * profile**2 / r**2
        - 4
    )
    source_first_ode = sp.Eq(
        sp.diff(profile, r) ** 2,
        sp.simplify(A * (4 - 1 / B - 2 * profile**2 / r**2)),
    )

    strain = s0 + C_s / r
    weak_profile = r * (1 + strain * u**2)
    weak_constraint = sp.factor(
        sp.series(
            radial_constraint.subs(
                {
                    profile: weak_profile,
                    sp.diff(profile, r): sp.diff(weak_profile, r),
                }
            ).doit(),
            eps,
            0,
            3,
        ).removeO()
    )
    weak_o2 = sp.expand(weak_constraint).coeff(eps, 2)
    s0_solution = sp.solve(sp.Eq(weak_o2, 0), s0)
    selected_constraint = sp.simplify(
        weak_constraint.subs(s0, -sp.Rational(1, 2))
    )

    passed = (
        s0_solution == [-sp.Rational(1, 2)]
        and selected_constraint == 0
        and C_s not in weak_o2.free_symbols
    )

    return {
        "status": (
            "PASS_ZERO_CHARGE_EXTERIOR_THETA_CONSTRAINT_DERIVES_P03C_RADIAL_STRAIN"
            if passed
            else "CHECK_SOURCE_FIRST_SPHERICAL_EMBEDDING"
        ),
        "metric": {"A": A, "B": B},
        "Theta_spherical": radial_constraint,
        "source_first_profile_ODE": source_first_ode,
        "weak_profile": weak_profile,
        "weak_Theta_series": weak_constraint,
        "derived_constant_strain": sp.Eq(s0, s0_solution[0]),
        "solid_C_over_r_charge_drops_out_through_1PN": C_s not in weak_o2.free_symbols,
        "reading": (
            "This exterior embedding check derives the displayed zero-charge "
            "weak radial response from Theta=0 rather than freezing the solid "
            "profile.  It does not solve the finite-source interior and does "
            "not include the first-order C_phi/r^2 tail generated by regular "
            "matching.  The old C_s/r coefficient drops out only inside that "
            "restricted bookkeeping ansatz."
        ),
    }


def finite_source_zero_H_charge_gate() -> dict[str, Any]:
    """Check conditional radial and arbitrary-shape zero-H weak-branch selection."""

    r = sp.Symbol("r", positive=True, real=True)
    C0, Q_H = sp.symbols("C0 Q_H", real=True)
    H_ext = C0 + Q_H / r
    radial_laplacian = sp.simplify(
        sp.diff(r**2 * sp.diff(H_ext, r), r) / r**2
    )
    flux = sp.simplify(4 * sp.pi * r**2 * sp.diff(H_ext, r))

    # H->0 removes C0.  With no direct H source and Theta=0 globally, Gauss'
    # law gives zero flux.  A regular center/no inner boundary excludes a
    # hidden delta-function charge, hence Q_H=0.
    asymptotic_subs = {C0: 0}
    zero_flux_solution = sp.solve(
        sp.Eq(flux.subs(asymptotic_subs), 0),
        Q_H,
    )
    selected_H = sp.simplify(
        H_ext.subs({C0: 0, Q_H: zero_flux_solution[0]})
    )

    k_squared = sp.Symbol("k_squared", positive=True, real=True)
    H_localized_mode = sp.Symbol("H_n_of_k", real=True)
    arbitrary_shape_fourier_equation = sp.Eq(
        k_squared * H_localized_mode,
        0,
    )
    arbitrary_shape_mode_solution = sp.solve(
        arbitrary_shape_fourier_equation,
        H_localized_mode,
    )

    passed = (
        radial_laplacian == 0
        and zero_flux_solution == [0]
        and selected_H == 0
        and arbitrary_shape_mode_solution == [0]
    )

    return {
        "status": (
            "PASS_CONDITIONAL_THETA_ZERO_BRANCH_SELECTS_ZERO_H__"
            "RADIAL_AND_ARBITRARY_SHAPE_LOCALIZED_PN_MODES"
            if passed
            else "CHECK_FINITE_SOURCE_ZERO_H_SELECTION"
        ),
        "exterior_harmonic_solution": sp.Eq(sp.Symbol("H_ext"), H_ext),
        "radial_laplacian": radial_laplacian,
        "Gauss_flux": flux,
        "asymptotic_constant": sp.Eq(C0, 0),
        "zero_flux_solution": sp.Eq(Q_H, zero_flux_solution[0]),
        "selected_H": selected_H,
        "arbitrary_shape_fourier_equation": arbitrary_shape_fourier_equation,
        "arbitrary_shape_localized_mode_solution": sp.Eq(
            H_localized_mode,
            arbitrary_shape_mode_solution[0],
        ),
        "arbitrary_shape_uniqueness_reading": (
            "At each audited PN order, the source-free H equation has "
            "k^2 H_n(k)=0.  Every localized nonzero mode vanishes; regularity "
            "and H->0 remove harmonic defects and the remaining constant."
        ),
        "assumptions": [
            "matter is minimally coupled to the one physical metric",
            "no direct matter-H coupling or H surface current",
            "the solid map is full-rank and single-valued on the weak branch",
            "the solid EOM selects Theta_n=0 order by order through the source",
            "regular center and no inner boundary/defect carrying H charge",
            "connected domain, H->0 at infinity and omega_H>0",
        ],
        "failure_modes": [
            "an oscillon/core action with explicit H charge",
            "a material-label shell current",
            "nontrivial topology or an excised inner boundary",
            "using the current determinant action without solving its O(delta^2) cofactor source",
        ],
    }


def pn_solid_constraint_recursion_gate() -> dict[str, Any]:
    """Encode the formal weak-branch Theta recursion for F_trace.

    Write the solid current schematically as

        J_A^i=M_A^i(eps) (eps*Theta_1+eps^2*Theta_2+...),

    with full-rank M_A^i(0)=delta_A^i.  In coordinate space the O(eps^2)
    equation contains d_i(M1_A^i*Theta_1), including derivatives of the
    inhomogeneous response matrix.  Once the lower equation and localized
    boundary data set Theta_1 identically to zero, that entire product
    divergence drops out and leaves d_A Theta_2=0.  Only then is the remaining
    gradient transformed to k_A Theta_2 in Fourier space.
    """

    x1, x2, x3 = sp.symbols("x_1 x_2 x_3", real=True)
    coordinates = (x1, x2, x3)
    theta_1_field = sp.Function("Theta_1")(*coordinates)
    theta_2_field = sp.Function("Theta_2")(*coordinates)
    m_field = sp.Matrix(
        3,
        3,
        lambda A, i: sp.Function(f"M1_{A + 1}{i + 1}")(*coordinates),
    )
    coordinate_order_1 = sp.Matrix(
        [sp.diff(theta_1_field, coordinates[A]) for A in range(3)]
    )
    coordinate_order_2_before = sp.Matrix(
        [
            sp.diff(theta_2_field, coordinates[A])
            + sum(
                sp.diff(
                    m_field[A, i] * theta_1_field,
                    coordinates[i],
                )
                for i in range(3)
            )
            for A in range(3)
        ]
    )
    coordinate_order_2_after = sp.simplify(
        coordinate_order_2_before.subs(theta_1_field, 0).doit()
    )
    expected_coordinate_order_2 = sp.Matrix(
        [sp.diff(theta_2_field, coordinates[A]) for A in range(3)]
    )

    k1, k2, k3 = sp.symbols("k_1 k_2 k_3", real=True)
    theta_1, theta_2 = sp.symbols("Theta_1 Theta_2", real=True)
    k = sp.Matrix([k1, k2, k3])
    k_sq = sp.expand(k.dot(k))

    fourier_order_1 = theta_1 * k
    fourier_order_2_after = theta_2 * k
    contracted_1 = sp.expand(k.dot(fourier_order_1))
    contracted_2 = sp.expand(k.dot(fourier_order_2_after))

    passed = (
        coordinate_order_2_after == expected_coordinate_order_2
        and sp.simplify(contracted_1 - k_sq * theta_1) == 0
        and sp.simplify(contracted_2 - k_sq * theta_2) == 0
    )

    return {
        "status": (
            "PASS_TRACE_SQUARE_FORMAL_1PN_STEALTH_INDUCTION__"
            "LABEL_NULL_MODES_AND_REDUCED_DYNAMICS_OPEN"
            if passed
            else "CHECK_TRACE_SQUARE_PN_SOLID_RECURSION"
        ),
        "coordinate_space_O1_solid_equation": coordinate_order_1,
        "coordinate_space_O2_before_Theta_1_constraint": (
            coordinate_order_2_before
        ),
        "coordinate_space_O2_after_Theta_1_constraint": (
            coordinate_order_2_after
        ),
        "wave_vector": k,
        "k_squared": k_sq,
        "O1_fourier_equation": fourier_order_1,
        "O1_contracted_equation": contracted_1,
        "O2_fourier_equation_after_Theta_1_constraint": (
            fourier_order_2_after
        ),
        "O2_contracted_equation": contracted_2,
        "boundary_selection": (
            "For k^2>0 the localized modes have Theta_1=Theta_2=0.  The "
            "spatial constant is fixed to zero by asymptotic normalization."
        ),
        "assumptions": [
            "full-rank weak material map",
            "localized quasi-static PN source",
            "time-current divergence is of higher PN order in this recursion",
            "lower Theta orders vanish before solving the next order",
            "no direct material-label source",
        ],
        "scope": (
            "This is an order-by-order weak-field statement, not an exact "
            "global nonlinear uniqueness theorem."
        ),
    }


def adm_medium_potential_auxiliary_hessian_diagnostic_gate() -> dict[str, Any]:
    """Evaluate the H=0 medium-potential lapse/shift Hessian at field-space points.

    The non-Minkowski witnesses are not asserted to solve the field equations.
    This is a pointwise H=0 unitary-gauge diagnostic of N*F, not a completed
    ADM/Dirac constraint-rank calculation.  Away from H=0 the hatted
    invariants also carry their exp(-2H) and exp(2H) factors.
    """

    N, n1, n2, n3 = sp.symbols("N n_1 n_2 n_3", real=True)
    g1, g2, g3 = sp.symbols("gamma_1 gamma_2 gamma_3", real=True)
    shift = sp.Matrix([n1, n2, n3])
    gamma_inverse = sp.diag(g1, g2, g3)
    Bhat = gamma_inverse - shift * shift.T / N**2
    Yhat = 1 / N**2
    theta = sp.simplify(Yhat + sp.trace(Bhat) - 4)
    auxiliary_variables = (N, n1, n2, n3)

    selected_density = sp.simplify(
        N * (theta**2 - 16 * sp.det(sp.eye(3) - Bhat))
    )
    trace_density = sp.simplify(N * theta**2)
    selected_hessian = sp.hessian(selected_density, auxiliary_variables)
    trace_hessian = sp.hessian(trace_density, auxiliary_variables)
    t = sp.Symbol("t", real=True)
    near_minkowski_path = {
        N: 1,
        n1: t,
        n2: 2 * t,
        n3: 3 * t,
        g1: 1 - t,
        g2: 1 - 2 * t,
        g3: 1 - 3 * t,
    }
    selected_path_determinant = sp.factor(
        selected_hessian.subs(near_minkowski_path).det()
    )
    trace_path_determinant = sp.factor(
        trace_hessian.subs(near_minkowski_path).det()
    )
    selected_path_leading_t3 = sp.simplify(
        sp.limit(selected_path_determinant / t**3, t, 0)
    )
    trace_path_leading_t3 = sp.simplify(
        sp.limit(trace_path_determinant / t**3, t, 0)
    )

    minkowski = {
        N: 1,
        n1: 0,
        n2: 0,
        n3: 0,
        g1: 1,
        g2: 1,
        g3: 1,
    }
    theta_zero_two_direction = {
        N: sp.sqrt(sp.Rational(10, 13)),
        n1: 0,
        n2: 0,
        n3: 0,
        g1: sp.Rational(9, 10),
        g2: sp.Rational(4, 5),
        g3: 1,
    }
    arbitrarily_close_off_shell = {
        N: 1,
        n1: sp.Rational(1, 100),
        n2: sp.Rational(1, 50),
        n3: sp.Rational(3, 100),
        g1: sp.Rational(99, 100),
        g2: sp.Rational(49, 50),
        g3: sp.Rational(97, 100),
    }
    points = {
        "Minkowski": minkowski,
        "Theta_zero_two_direction_off_shell": theta_zero_two_direction,
        "near_Minkowski_off_shell": arbitrarily_close_off_shell,
    }
    selected_ranks = {
        key: selected_hessian.subs(point).rank()
        for key, point in points.items()
    }
    trace_ranks = {
        key: trace_hessian.subs(point).rank()
        for key, point in points.items()
    }
    theta_values = {
        key: sp.simplify(theta.subs(point))
        for key, point in points.items()
    }

    passed = (
        theta_values["Minkowski"] == 0
        and theta_values["Theta_zero_two_direction_off_shell"] == 0
        and selected_ranks
        == {
            "Minkowski": 1,
            "Theta_zero_two_direction_off_shell": 2,
            "near_Minkowski_off_shell": 4,
        }
        and trace_ranks
        == {
            "Minkowski": 1,
            "Theta_zero_two_direction_off_shell": 1,
            "near_Minkowski_off_shell": 4,
        }
        and selected_path_leading_t3 != 0
        and trace_path_leading_t3 != 0
    )

    return {
        "status": (
            "PASS_UNITARY_GAUGE_MEDIUM_POTENTIAL_AUXILIARY_HESSIAN_"
            "FIELD_POINT_RANK_CHANGE_DIAGNOSTIC"
            if passed
            else "CHECK_ADM_AUXILIARY_HESSIAN_RANKS"
        ),
        "H_zero_unitary_gauge_Yhat": Yhat,
        "H_zero_unitary_gauge_Bhat": Bhat,
        "Theta": theta,
        "field_point_Theta_values": theta_values,
        "selected_density_NF_over_c": selected_density,
        "trace_density_NF_over_c": trace_density,
        "selected_lapse_shift_hessian_ranks": selected_ranks,
        "trace_square_lapse_shift_hessian_ranks": trace_ranks,
        "near_Minkowski_field_path": near_minkowski_path,
        "selected_path_Hessian_determinant": selected_path_determinant,
        "trace_square_path_Hessian_determinant": trace_path_determinant,
        "selected_path_det_over_t3_limit": selected_path_leading_t3,
        "trace_square_path_det_over_t3_limit": trace_path_leading_t3,
        "punctured_neighborhood_reading": (
            "Both determinants are t^3 times a factor nonzero at t=0.  Thus "
            "both pointwise medium-potential Hessians have rank four for all "
            "sufficiently small nonzero t on this off-shell path."
        ),
        "warning": (
            "The pointwise N*F auxiliary Hessian rank is field-point-dependent, "
            "including arbitrarily close to Minkowski.  This is a "
            "strong-coupling/constraint warning, not a physical constraint-rank "
            "or ghost theorem.  Off-shell Hessian rank can also depend on the "
            "auxiliary-variable parametrization.  A full on-shell ADM/Dirac "
            "reduction and reduced kinetic-sign calculation remain mandatory."
        ),
    }


def trace_square_open_dynamics_boundary_gate() -> dict[str, Any]:
    """Record exact flat directions and the radiative-stability boundary."""

    invariant_dimension = 7  # deltaY plus six symmetric deltaB components
    theta_zero_dimension = invariant_dimension - 1
    fixed_Y_shear_dimension = 6 - 1
    passed = (
        theta_zero_dimension == 6
        and fixed_Y_shear_dimension == 5
    )

    return {
        "status": (
            "PASS_TRACE_SQUARE_OPEN_DYNAMICS_BOUNDARY_RECORDED"
            if passed
            else "CHECK_TRACE_SQUARE_DYNAMICS_BOUNDARY"
        ),
        "invariant_perturbation_dimension": invariant_dimension,
        "exact_Theta_zero_hypersurface_dimension": theta_zero_dimension,
        "fixed_Y_shear_flat_directions": fixed_Y_shear_dimension,
        "quadratic_hessian_rank": 1,
        "technical_naturalness": (
            "The currently declared symmetries do not protect the determinant "
            "coefficient from radiative regeneration; setting it to zero is a "
            "tuning until an additional symmetry or constraint mechanism is supplied."
        ),
        "dynamics_warning": (
            "F_trace is a penalty square, not a genuine Lagrange-multiplier "
            "constraint.  Its transverse label directions have no quadratic "
            "propagator, so the reduced dynamics and strong-coupling scale are open."
        ),
    }


def formal_standard_ppn_stealth_implication_gate() -> dict[str, Any]:
    """Record the conditional GR implication, not a moving ten-PPN derivation."""

    normal = selected_vs_trace_square_normal_form_gate()
    cofactor = generic_multisource_cofactor_gate()
    source_promotion = uniform_density_source_matching_promotion_gate()
    selected_counterexample = selected_action_finite_source_residual_gate()
    stress_obstruction = second_order_selected_stress_gate()
    response_scale = finite_source_1pn_metric_scale_boundary_gate()
    stealth = phase_normalized_trace_square_stealth_gate()
    spherical = spherical_source_first_embedding_gate()
    source = finite_source_zero_H_charge_gate()
    recursion = pn_solid_constraint_recursion_gate()
    adm = adm_medium_potential_auxiliary_hessian_diagnostic_gate()
    dynamics_boundary = trace_square_open_dynamics_boundary_gate()

    candidate_algebra_pass = (
        normal["status"].startswith("PASS_")
        and cofactor["status"].startswith("PASS_")
        and source_promotion["status"].startswith("PASS_")
        and selected_counterexample["counterexample_confirmed"]
        and stress_obstruction["status"].startswith("PASS_")
        and response_scale["status"].startswith("PASS_")
        and stealth["status"].startswith("PASS_")
        and spherical["status"].startswith("PASS_")
        and source["status"].startswith("PASS_")
        and recursion["status"].startswith("PASS_")
        and adm["status"].startswith("PASS_")
        and dynamics_boundary["status"].startswith("PASS_")
    )
    ppn_gr = {
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

    return {
        "status": (
            "PASS_FORMAL_TRACE_SQUARE_STEALTH_IMPLICATION__"
            "FULL_MOVING_STANDARD_PPN_OPEN"
            if candidate_algebra_pass
            else "CHECK_SOURCE_FIRST_TRACE_SQUARE_ROUTE"
        ),
        "candidate_algebra_pass": candidate_algebra_pass,
        "current_selected_p05z_full_N_body_1PN_closed": False,
        "current_selected_finite_source_H_zero_selected": False,
        "current_selected_reason": selected_counterexample["status"],
        "finite_source_power_counting_audit": source_promotion,
        "finite_source_selected_action_counterexample": selected_counterexample,
        "generic_selected_stress_obstruction": stress_obstruction,
        "finite_source_metric_response_scale_boundary": response_scale,
        "trace_square_candidate_exact_medium_stress_on_Theta_zero": 0,
        "trace_square_candidate_selected_H": source["selected_H"],
        "trace_square_formal_PN_recursion": recursion,
        "ADM_medium_potential_auxiliary_hessian_diagnostic": adm,
        "trace_square_open_dynamics_boundary": dynamics_boundary,
        "remaining_metric_equation": "M_Pl^2 G_mn = T_mn^(minimal matter)",
        "conditional_GR_PPN_targets_if_full_branch_exists": ppn_gr,
        "PPN_implication_not_derivation": (
            "If the full moving N-body solution is proved to remain on "
            "Theta=H=0 through 1PN, the medium vanishes and GR fixes all ten "
            "targets below.  This gate has not independently solved the "
            "time-current, vector, matter-potential and standard-gauge system."
        ),
        "logical_chain": [
            "minimal matter sources the Einstein equation",
            "the weak full-rank solid equation plus localized boundary data "
            "formally selects Theta_n=0 order by order through 1PN",
            "conditional on that recursion, the regular no-direct-source H "
            "equation selects H_n=0 through the same order",
            "wherever Theta=0, the F_trace density and first variations vanish "
            "as an exact algebraic identity, hence they vanish through the "
            "recursively audited quasi-static 1PN orders",
            "the remaining audited metric/matter equations reduce to Einstein's",
            "a full moving Theta=0 branch would therefore inherit all ten GR "
            "PPN values, but that moving/gauge derivation remains open",
        ],
        "not_yet_proved": [
            "that F_trace is the selected RefG action rather than a replacement candidate",
            "persistent ADM/Dirac constraints and a healthy reduced kinetic sign",
            "a strong-coupling scale above the domain of use",
            "compatibility with cosmology, oscillons, particles and the compact-core formation problem",
            "absence of direct H/material-label charge in the microscopic oscillon core",
            "nonlinear PDE existence and uniqueness beyond the perturbative weak branch",
            "explicit existence of the full moving N-body Theta=0 branch, "
            "including time-current terms and standard-PPN gauge matching",
            "the pointwise unitary-gauge N*F lapse/shift Hessian changes rank "
            "off shell; its implication for the on-shell ADM/Dirac constraints",
            "the selected -M_*^4*c*Theta^2 clock/trace kinetic sign after full "
            "constraint reduction",
            "technical naturalness of setting the determinant coefficient to "
            "zero under radiative corrections",
            "a uniform source-domain bound on |c|*M_star^4*R^2/M_Pl^2 before "
            "assigning an observational amplitude to the nominal O(U^2) residual",
            "whether an actual gauge symmetry or auxiliary multiplier is "
            "needed to make Theta=0 a genuine constraint rather than a penalty minimum",
        ],
    }


def source_first_1pn_action_decision_gate() -> dict[str, Any]:
    """Top-level decision ledger; it deliberately does not auto-select an action."""

    inheritance = formal_standard_ppn_stealth_implication_gate()
    audit_pass = inheritance["candidate_algebra_pass"]

    return {
        "status": (
            "CURRENT_P05Z_STATIC_ZERO_CHARGE_BRANCH_EXISTS_BUT_IS_NOT_"
            "UNIVERSALLY_SOURCE_SELECTED__TRACE_SQUARE_REPLACEMENT_CANDIDATE_"
            "ALGEBRA_PASS__FULL_MOVING_PPN_OPEN"
            if audit_pass
            else "CHECK_SOURCE_FIRST_1PN_ACTION_DECISION"
        ),
        "safe_conclusion": (
            "In the downstream reading that appends F_min/H to an already "
            "supplied GR matter source, the existing p03f/p05z beta=gamma=1 "
            "exterior algebra is valid for its specially selected C_phi=0 and "
            "H=0 branch.  A regular uniform-density source instead generates "
            "C_phi!=0, for which the selected determinant produces nonzero H "
            "source and medium stress at coefficient-wise O(U^2).  Every such "
            "spherical source with a nonzero matching moment C_phi has the same "
            "exact-GR obstruction; a re-solved branch is not excluded, and its "
            "observational amplitude still depends on "
            "|c|*M_star^4*R^2/M_Pl^2."
        ),
        "candidate_conclusion": (
            "Replacing the response normal form by F_trace=c*Theta^2 gives a "
            "formal quasi-static source-first 1PN stealth branch under explicit "
            "minimal-coupling/no-defect and perturbative-regularity assumptions, "
            "while retaining the weak and compact zero-F endpoints.  Full "
            "moving N-body standard-PPN matching is still open.  Under the "
            "p03h layer separation this is a downstream control replacement, "
            "not the preferred microscopic-to-Einstein matching route."
        ),
        "decision_required_before_action_change": [
            "apply p03h layer separation before interpreting this downstream diagnostic",
            "select or reject removal of -16*det(I-Bhat)",
            "decide whether the trace/label sector is a genuine constrained system",
            "run ADM/Dirac and strong-coupling checks",
            "derive the moving N-body time-current/vector equations and standard PPN gauge",
            "supply symmetry protection or accept determinant-zero tuning",
            "re-run cosmology/oscillon/compact-core gates on the candidate",
        ],
        "audit_completed": audit_pass,
        "interpretation_scope": (
            "DOWNSTREAM_EXTRA_SECTOR_DIAGNOSTIC__UPSTREAM_MATCHING_HANDLED_BY_P03H"
        ),
        "selected_action_replacement_authorized": False,
        "article_export_allowed": False,
        "formal_stealth_implication_gate": inheritance,
    }


def main() -> int:
    result = source_first_1pn_action_decision_gate()
    inheritance = result["formal_stealth_implication_gate"]
    print("status:", result["status"])
    print("safe conclusion:", result["safe_conclusion"])
    print("candidate conclusion:", result["candidate_conclusion"])
    print("formal stealth implication:", inheritance["status"])
    print(
        "current p05z generic N-body 1PN closed:",
        inheritance["current_selected_p05z_full_N_body_1PN_closed"],
    )
    print(
        "conditional GR PPN targets (full moving derivation open):",
        inheritance["conditional_GR_PPN_targets_if_full_branch_exists"],
    )
    print("article export allowed:", result["article_export_allowed"])
    return 0 if result["audit_completed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
