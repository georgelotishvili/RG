# Notation:
# signature (+---); Y=g^mn Phi_m Phi_n;
# B^AB=-g^mn phi^A_m phi^B_n.

"""Independent completeness audit for the selected p05z weak-field branch.

The purpose of this file is to keep three logically different statements
separate:

1. A zero-H-charge, static spherical branch solves every selected-action
   Euler equation through the metric orders used to read beta and gamma.
2. That branch is the unique exterior selected by a finite Solar source.
3. The complete inhomogeneous first-post-Newtonian/standard-PPN problem is
   solved.

Only the first statement is currently proved.  The second still needs
finite-source/core matching and branch selection.  The third additionally
needs the moving, nonlinear, standard-gauge solution and the ADM/Dirac-reduced
field system.

This audit deliberately rebuilds the static algebra directly from the
selected exact-GR coefficient slice rather than trusting the status tokens in
p03c, p03e or p05z.
"""

from __future__ import annotations

from typing import Any

import sympy as sp


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def _fmin_exact_slice(
    Y: sp.Expr,
    lambda_r: sp.Expr,
    lambda_t: sp.Expr,
    H: sp.Expr,
    c: sp.Expr,
) -> sp.Expr:
    """Phase-normalized exact-GR density on c_YI1=2*c_Y2."""
    Yhat = sp.exp(-2 * H) * Y
    lr_hat = sp.exp(2 * H) * lambda_r
    lt_hat = sp.exp(2 * H) * lambda_t
    I1 = lr_hat + 2 * lt_hat
    I2 = 2 * lr_hat * lt_hat + lt_hat**2
    I3 = lr_hat * lt_hat**2
    return sp.expand(
        c
        * (
            -8 * Yhat
            + Yhat**2
            + 8 * I1
            + I1**2
            - 16 * I2
            + 16 * I3
            + 2 * Yhat * I1
        )
    )


def _areal_einstein_tensor(
    A: sp.Expr,
    B: sp.Expr,
    r: sp.Symbol,
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Mixed Einstein components for ds^2=B dt^2-A dr^2-r^2 dOmega^2."""
    Ap = sp.diff(A, r)
    Bp = sp.diff(B, r)
    Bpp = sp.diff(B, r, 2)
    Gtt = -Ap / (r * A**2) + (1 / A - 1) / r**2
    Grr = Bp / (r * A * B) + (1 / A - 1) / r**2
    Gtheta = (
        Bpp / (2 * A * B)
        - Bp**2 / (4 * A * B**2)
        - Ap * Bp / (4 * A**2 * B)
        + Bp / (2 * r * A * B)
        - Ap / (2 * r * A**2)
    )
    return tuple(sp.simplify(value) for value in (Gtt, Grr, Gtheta))


def independent_static_euler_residual_gate() -> dict[str, Any]:
    """Rebuild all static selected-action residuals through O((r_s/r)^2)."""
    r, r_s, eps, c, kappa = sp.symbols(
        "r r_s eps c_Y2 kappa",
        positive=True,
        real=True,
    )
    Y_s, lr_s, lt_s, H_s = sp.symbols(
        "Y lambda_r lambda_t H",
        positive=True,
        real=True,
    )
    u = eps * r_s / r

    # Schwarzschild areal metric through the required order and the radial
    # solid response derived by the p03c equations.
    A = 1 + u + u**2
    B = 1 - u
    solid_radius = r * (1 - u**2 / 2)
    Y = 1 / B
    lambda_r = sp.diff(solid_radius, r) ** 2 / A
    lambda_t = solid_radius**2 / r**2
    H = sp.Integer(0)

    F = _fmin_exact_slice(Y_s, lr_s, lt_s, H_s, c)
    on_branch = {
        Y_s: Y,
        lr_s: lambda_r,
        lt_s: lambda_t,
        H_s: H,
    }
    F_value = F.subs(on_branch)
    F_Y = sp.diff(F, Y_s).subs(on_branch)
    F_lr = sp.diff(F, lr_s).subs(on_branch)
    F_lt = sp.diff(F, lt_s).subs(on_branch)

    # F is the positive dimensionless density in the physical action -M_*^4 F.
    # With the repository convention this gives the following dimensionless
    # mixed source, with the common M_*^4 absorbed into kappa.
    Ttt = sp.simplify(2 * Y * F_Y - F_value)
    Trr = sp.simplify(2 * lambda_r * F_lr - F_value)
    Ttheta = sp.simplify(lambda_t * F_lt - F_value)
    Gtt, Grr, Gtheta = _areal_einstein_tensor(A, B, r)

    def through_two(expr: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.series(sp.expand(expr * r**2), eps, 0, 3).removeO()
        )

    metric_residuals = {
        "t": through_two(Gtt - kappa * Ttt),
        "r": through_two(Grr - kappa * Trr),
        "theta": through_two(Gtheta - kappa * Ttheta),
    }
    metric_coefficients = {
        name: {
            "O0": sp.simplify(expr.coeff(eps, 0)),
            "O1": sp.simplify(expr.coeff(eps, 1)),
            "O2": sp.simplify(expr.coeff(eps, 2)),
        }
        for name, expr in metric_residuals.items()
    }

    # The reduced hedgehog Euler equation is sufficient because the full
    # internal-vector Euler residual must be radial by diagonal SO(3).
    profile = sp.Function("profile")(r)
    lr_profile = sp.diff(profile, r) ** 2 / A
    lt_profile = profile**2 / r**2
    F_profile = _fmin_exact_slice(Y, lr_profile, lt_profile, 0, c)
    reduced_density = sp.sqrt(A * B) * r**2 * F_profile
    solid_euler = sp.simplify(
        sp.diff(reduced_density, profile)
        - sp.diff(
            sp.diff(reduced_density, sp.diff(profile, r)),
            r,
        )
    )
    profile_subs = {
        profile: solid_radius,
        sp.diff(profile, r): sp.diff(solid_radius, r),
        sp.diff(profile, r, 2): sp.diff(solid_radius, r, 2),
    }
    solid_series = sp.expand(
        sp.series(solid_euler.subs(profile_subs).doit(), eps, 0, 3).removeO()
    )
    solid_coefficients = {
        f"O{order}": sp.simplify(solid_series.coeff(eps, order))
        for order in range(3)
    }

    H_source = sp.diff(F, H_s).subs(on_branch)
    H_source_series = sp.expand(
        sp.series(H_source, eps, 0, 3).removeO()
    )
    H_source_coefficients = {
        f"O{order}": sp.simplify(H_source_series.coeff(eps, order))
        for order in range(3)
    }

    # Phi=t on a static diagonal background.  Its shift current has only a
    # time component; all coefficients are time independent, so div J_Phi=0.
    phi_clock_euler = sp.Integer(0)
    projected_H_euler = sp.Integer(0)
    projected_H_stress = sp.Integer(0)

    passed = (
        _all_zero(
            value
            for rows in metric_coefficients.values()
            for value in rows.values()
        )
        and _all_zero(solid_coefficients.values())
        and _all_zero(H_source_coefficients.values())
        and phi_clock_euler == 0
        and projected_H_euler == 0
        and projected_H_stress == 0
    )

    return {
        "status": (
            "PASS_INDEPENDENT_ZERO_H_STATIC_SPHERICAL_EULER_RESIDUALS_"
            "THROUGH_U2"
            if passed
            else "CHECK_INDEPENDENT_STATIC_EULER_RESIDUALS"
        ),
        "selected_exact_GR_slice": "c_YI1=2*c_Y2",
        "metric": {"A": A, "B": B},
        "solid_radius": solid_radius,
        "H": H,
        "metric_residual_series_times_r2": metric_residuals,
        "metric_residual_coefficients": metric_coefficients,
        "solid_euler_series": sp.factor(solid_series),
        "solid_euler_coefficients": solid_coefficients,
        "H_source_series": sp.factor(H_source_series),
        "H_source_coefficients": H_source_coefficients,
        "Phi_euler_residual": phi_clock_euler,
        "projected_H_euler_and_stress": {
            "euler": projected_H_euler,
            "stress": projected_H_stress,
        },
        "scope": (
            "existence of the unloaded H=0 static spherical branch; this does "
            "not prove that a finite source selects it uniquely"
        ),
    }


def independent_areal_to_standard_ppn_gate() -> dict[str, Any]:
    """Exact Schwarzschild areal-to-isotropic expansion and beta/gamma readout."""
    x = sp.Symbol("U_N", real=True)
    # x=GM/rho.  Exact Schwarzschild has
    # R/rho=(1+x/2)^2 and r_s/R=2*x/(R/rho).
    radius_ratio = (1 + x / 2) ** 2
    r_s_over_R = sp.simplify(2 * x / radius_ratio)
    g00 = sp.series(1 - r_s_over_R, x, 0, 3).removeO().expand()
    spatial_factor = sp.series(radius_ratio**2, x, 0, 3).removeO().expand()
    beta = sp.simplify(g00.coeff(x, 2) / 2)
    gamma = sp.simplify(spatial_factor.coeff(x, 1) / 2)
    passed = (
        g00 == 1 - 2 * x + 2 * x**2
        and spatial_factor == 1 + 2 * x + sp.Rational(3, 2) * x**2
        and beta == 1
        and gamma == 1
    )
    return {
        "status": (
            "PASS_INDEPENDENT_AREAL_TO_STANDARD_PPN_BETA_GAMMA_ONE"
            if passed
            else "CHECK_INDEPENDENT_PPN_COORDINATE_BRIDGE"
        ),
        "R_over_rho": radius_ratio,
        "g00_isotropic_series": g00,
        "spatial_conformal_factor_series": spatial_factor,
        "beta_PPN": beta,
        "gamma_PPN": gamma,
    }


def radial_metric_mode_and_branch_selection_audit() -> dict[str, Any]:
    """Solve the static U^2 radial modes far enough to expose branch assumptions."""
    r, r_s, eps, c, kappa = sp.symbols(
        "r r_s eps c_Y2 kappa",
        positive=True,
        real=True,
    )
    f = sp.Function("f")(r)
    g = sp.Function("g")(r)
    s = sp.Function("s")(r)
    u = eps * r_s / r

    A = 1 + u + (1 + f) * u**2
    B = 1 - u + g * u**2
    solid_radius = r * (1 + s * u**2)
    Y = 1 / B
    lr = sp.diff(solid_radius, r) ** 2 / A
    lt = solid_radius**2 / r**2

    Y_s, lr_s, lt_s, H_s = sp.symbols(
        "Y lambda_r lambda_t H",
        positive=True,
        real=True,
    )
    F = _fmin_exact_slice(Y_s, lr_s, lt_s, H_s, c)
    substitutions = {Y_s: Y, lr_s: lr, lt_s: lt, H_s: 0}
    F_value = F.subs(substitutions)
    Ttt = sp.simplify(2 * Y * sp.diff(F, Y_s).subs(substitutions) - F_value)
    Trr = sp.simplify(2 * lr * sp.diff(F, lr_s).subs(substitutions) - F_value)
    Ttheta = sp.simplify(lt * sp.diff(F, lt_s).subs(substitutions) - F_value)
    Gtt, Grr, Gtheta = _areal_einstein_tensor(A, B, r)

    def order_two(expr: sp.Expr) -> sp.Expr:
        return sp.factor(
            sp.series(sp.expand(expr * r**2), eps, 0, 3)
            .removeO()
            .expand()
            .coeff(eps, 2)
        )

    equations = [
        order_two(Gtt - kappa * Ttt),
        order_two(Grr - kappa * Trr),
        order_two(Gtheta - kappa * Ttheta),
    ]
    q1 = sp.factor(-equations[0] * r**2 / r_s**2)
    q2 = sp.factor(-equations[1] * r**2 / r_s**2)
    q3 = sp.factor(-2 * equations[2] * r**2 / r_s**2)

    # Keep the check in the original f,g variables.  A direct SymPy
    # substitution f+g -> h is representation-dependent because expanded
    # Add nodes need not contain f+g as a literal subexpression.
    sum_mode_equation = sp.factor(q2 - q1)
    expected_sum_mode = (
        2 * (f + g)
        - r * (sp.diff(f, r) + sp.diff(g, r))
    )

    g_minus_f = {
        g: -f,
        sp.diff(g, r): -sp.diff(f, r),
        sp.diff(g, r, 2): -sp.diff(f, r, 2),
    }
    metric_mode_equation = sp.factor((q3 - 2 * q1).subs(g_minus_f))
    expected_metric_mode = (
        r**2 * sp.diff(f, r, 2)
        - 4 * r * sp.diff(f, r)
        + 4 * f
    )
    m = sp.Symbol("m", real=True)
    indicial = sp.factor(m * (m - 1) - 4 * m + 4)
    indicial_roots = sp.solve(sp.Eq(indicial, 0), m)

    C_s = sp.Symbol("C_s", real=True)
    static_candidate = {
        f: 0,
        g: 0,
        s: -sp.Rational(1, 2) + C_s / r,
        sp.diff(f, r): 0,
        sp.diff(g, r): 0,
        sp.diff(g, r, 2): 0,
        sp.diff(s, r): -C_s / r**2,
    }
    candidate_residuals = [
        sp.simplify(equation.subs(static_candidate))
        for equation in equations
    ]
    passed = (
        sp.simplify(sum_mode_equation - expected_sum_mode) == 0
        and sp.simplify(metric_mode_equation - expected_metric_mode) == 0
        and indicial_roots == [1, 4]
        and _all_zero(candidate_residuals)
    )

    return {
        "status": (
            "PASS_STATIC_RADIAL_METRIC_UNIQUENESS_WITHIN_ZERO_H_ANSATZ__"
            "SOURCE_BRANCH_SELECTION_OPEN"
            if passed
            else "CHECK_STATIC_RADIAL_MODE_AUDIT"
        ),
        "raw_O_U2_equations": equations,
        "sum_mode_equation": sp.Eq(sum_mode_equation, 0),
        "sum_mode_solution": "f+g=C_norm*r^2; asymptotic metric normalization sets C_norm=0",
        "remaining_metric_mode_equation": sp.Eq(metric_mode_equation, 0),
        "metric_mode_indicial_polynomial": indicial,
        "metric_mode_powers": indicial_roots,
        "mode_reading": {
            "r^4": "excluded by asymptotic flatness",
            "r": "renormalizes the 1/r mass coefficient and is removed once ADM/Newton mass is fixed",
            "remaining_metric": "f=g=0",
        },
        "solid_solution": "s=-1/2+C_s/r",
        "candidate_residuals": candidate_residuals,
        "limitation": (
            "uniqueness is only within the unloaded H=0 radial ansatz after "
            "asymptotic normalization and mass fixing; the same action also "
            "admits other H-loaded branches"
        ),
    }


def unreduced_null_direction_audit() -> dict[str, Any]:
    """Record why rank-one quadratic algebra cannot certify predictive dynamics."""
    dy, b11, b22, b33, b12, b13, b23, H = sp.symbols(
        "dY b11 b22 b33 b12 b13 b23 H",
        real=True,
    )

    # In hatted invariant variables F^(2)/c=(dYhat+Tr dBhat)^2.
    # The three off-diagonal entries are included because B is symmetric.
    hatted_variables = (dy, b11, b22, b33, b12, b13, b23)
    theta_hatted = dy + b11 + b22 + b33
    quadratic_hatted = sp.expand(theta_hatted**2)
    hessian_hatted = sp.hessian(quadratic_hatted, hatted_variables)
    rank_hatted = hessian_hatted.rank()
    nullity_hatted = len(hatted_variables) - rank_hatted

    # In the unhatted field variables the phase normalization adds 4H to the
    # same trace combination.  This is still an unreduced response Hessian;
    # the projected H-gradient term, metric constraints and gauge reduction
    # must be included before counting physical modes.
    unhatted_variables = hatted_variables + (H,)
    theta_unhatted = theta_hatted + 4 * H
    quadratic_unhatted = sp.expand(theta_unhatted**2)
    hessian_unhatted = sp.hessian(quadratic_unhatted, unhatted_variables)
    rank_unhatted = hessian_unhatted.rank()
    nullity_unhatted = len(unhatted_variables) - rank_unhatted

    epsilon = sp.Symbol("epsilon", real=True)
    cubic_witness_matrix = sp.diag(epsilon, epsilon, -2 * epsilon)
    witness_trace = sp.trace(cubic_witness_matrix)
    witness_determinant = sp.det(cubic_witness_matrix)
    witness_response_over_c = sp.simplify(
        witness_trace**2 + 16 * witness_determinant
    )
    passed = (
        rank_hatted == 1
        and nullity_hatted == 6
        and rank_unhatted == 1
        and nullity_unhatted == 7
        and witness_trace == 0
        and witness_determinant == -2 * epsilon**3
        and witness_response_over_c == -32 * epsilon**3
    )
    return {
        "status": (
            "OPEN_REDUCED_DYNAMICS__RANK_ONE_QUADRATIC_AND_"
            "SIGN_INDEFINITE_CUBIC_SADDLE"
            if passed
            else "CHECK_UNREDUCED_NULL_DIRECTION_AUDIT"
        ),
        "hatted_quadratic_combination": theta_hatted,
        "hatted_quadratic_density_up_to_scale": quadratic_hatted,
        "hatted_hessian": hessian_hatted,
        "hatted_rank": rank_hatted,
        "hatted_nullity": nullity_hatted,
        "unhatted_phase_normalized_combination": theta_unhatted,
        "unhatted_F_hessian": hessian_unhatted,
        "unhatted_F_rank": rank_unhatted,
        "unhatted_F_nullity": nullity_unhatted,
        "cubic_interaction": (
            "+16*det(delta Bhat), nonzero along generic quadratic-null directions"
        ),
        "exact_cubic_saddle_witness": {
            "delta_Yhat": 0,
            "delta_Bhat": cubic_witness_matrix,
            "trace": witness_trace,
            "determinant": witness_determinant,
            "Fmin_over_c": witness_response_over_c,
            "positive_definite_Bhat_domain": "-1 < epsilon < 1/2",
            "sign_reverses_under_epsilon_to_minus_epsilon": True,
        },
        "logical_boundary": (
            "the null directions may be removed by constraints, or may signal "
            "a low strong-coupling scale; the unreduced Hessian alone cannot decide"
        ),
    }


def selected_action_sign_convention_audit() -> dict[str, Any]:
    """Separate the response Hessian of F from the selected action Hessian."""
    velocity, c, M4 = sp.symbols(
        "dot_chi c_Y2 Mstar4",
        real=True,
    )
    Y = (1 + velocity) ** 2
    # At Bhat=I and H=0, F/c=(Y-1)^2 exactly.
    F_clock = sp.expand(c * (Y - 1) ** 2)
    F_clock_quadratic = sp.expand(
        sp.series(F_clock, velocity, 0, 3).removeO()
    )
    selected_L_clock_quadratic = sp.expand(-M4 * F_clock_quadratic)
    response_hessian_entry = sp.simplify(
        sp.diff(F_clock_quadratic, velocity, 2) / 2
    )
    action_hessian_entry = sp.simplify(
        sp.diff(selected_L_clock_quadratic, velocity, 2) / 2
    )
    passed = (
        response_hessian_entry == 4 * c
        and action_hessian_entry == -4 * M4 * c
    )
    return {
        "status": (
            "OPEN_SELECTED_ACTION_REDUCED_KINETIC_SIGN__"
            "RESPONSE_F_AND_LAGRANGIAN_MINUS_F_SEPARATED"
            if passed
            else "CHECK_SELECTED_ACTION_SIGN_CONVENTION"
        ),
        "selected_medium_lagrangian": "-Mstar4*Fmin",
        "clock_only_F_quadratic": F_clock_quadratic,
        "response_F_hessian_entry": response_hessian_entry,
        "selected_action_hessian_entry": action_hessian_entry,
        "warning": (
            "the historical p01 K_Phi=4*c_Y2 is a Hessian entry of F; "
            "the selected p05z Lagrangian carries the opposite overall sign. "
            "Neither fixed-metric entry is a physical ghost theorem before "
            "lapse, shift, solid, H and gauge constraints are reduced"
        ),
    }


def uniform_static_power_counting_audit() -> dict[str, Any]:
    """Make the dimensionful hierarchy missing from coefficient-wise U counting explicit."""
    Mstar, Mpl, r = sp.symbols(
        "Mstar M_Pl r",
        positive=True,
        real=True,
    )
    hierarchy = sp.simplify(Mstar**4 * r**2 / Mpl**2)
    return {
        "status": (
            "OPEN_UNIFORM_STATIC_PN_HIERARCHY__"
            "COEFFICIENT_WISE_U2_CANCELLATION_ONLY"
        ),
        "dimensionless_medium_to_Einstein_prefactor": hierarchy,
        "required_domain_condition": (
            "specify and bound Mstar^4*r^2/M_Pl^2 over the complete "
            "source-matching and PPN domain"
        ),
        "logical_boundary": (
            "tau=O(U^3) does not by itself make "
            "(Mstar^4*r^2/M_Pl^2)*tau uniformly higher order"
        ),
    }


def full_standard_1pn_completeness_gate() -> dict[str, Any]:
    """Final independent verdict: branch existence is not full standard 1PN."""
    static = independent_static_euler_residual_gate()
    coordinate = independent_areal_to_standard_ppn_gate()
    radial = radial_metric_mode_and_branch_selection_audit()
    null_audit = unreduced_null_direction_audit()
    sign_audit = selected_action_sign_convention_audit()
    power_counting = uniform_static_power_counting_audit()

    gamma, beta, xi, alpha1, alpha2, alpha3 = sp.symbols(
        "gamma beta xi alpha_1 alpha_2 alpha_3",
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
    static_rows = sp.Matrix([2 * gamma, 2 * beta])
    static_rank = static_rows.jacobian(parameters).rank()
    static_nullity = len(parameters) - static_rank

    branch_eom_pass = (
        static["status"]
        == "PASS_INDEPENDENT_ZERO_H_STATIC_SPHERICAL_EULER_RESIDUALS_THROUGH_U2"
        and coordinate["status"]
        == "PASS_INDEPENDENT_AREAL_TO_STANDARD_PPN_BETA_GAMMA_ONE"
        and radial["status"].startswith("PASS_")
    )
    full_standard_1pn_closed = False
    finite_source_selects_zero_H_branch = False
    reduced_dynamics_closed = False

    return {
        "status": (
            "PASS_CONDITIONAL_ZERO_H_STATIC_SPHERICAL_1PN_BRANCH__"
            "FULL_STANDARD_1PN_NOT_CLOSED"
            if branch_eom_pass
            and static_rank == 2
            and static_nullity == 8
            and not full_standard_1pn_closed
            else "CHECK_INDEPENDENT_1PN_COMPLETENESS"
        ),
        "static_branch_EOM_exists": branch_eom_pass,
        "static_branch_values": {
            "beta": coordinate["beta_PPN"],
            "gamma": coordinate["gamma_PPN"],
        },
        "static_PPN_information_rank": static_rank,
        "static_PPN_information_nullity": static_nullity,
        "independent_static_EOM_audit": static,
        "independent_coordinate_bridge": coordinate,
        "radial_mode_audit": radial,
        "unreduced_null_direction_audit": null_audit,
        "selected_action_sign_convention_audit": sign_audit,
        "uniform_static_power_counting_audit": power_counting,
        "finite_source_selects_zero_H_branch": (
            finite_source_selects_zero_H_branch
        ),
        "reduced_dynamics_closed": reduced_dynamics_closed,
        "full_standard_1PN_closed": full_standard_1pn_closed,
        "missing_for_predictive_static_1PN": [
            "match a finite Solar source/core to the exterior fields",
            "show that the source selects the unloaded H=0 branch and excludes independent medium charges",
            "classify the rank-one quadratic null directions by ADM/Dirac reduction",
            "freeze the overall -Mstar^4*F sign and test the reduced kinetic signature",
            "bound the reduced strong-coupling scale above the Solar 1PN regime",
            "bound Mstar^4*r^2/M_Pl^2 uniformly over the matching and PPN domain",
        ],
        "missing_for_full_standard_1PN": [
            "derive g_ij through O(v^2) for an arbitrary inhomogeneous source",
            "derive g_0i through O(v^3), including physical source-medium relative motion",
            "derive g_00 through O(v^4) with Phi_1,Phi_2,Phi_3,Phi_4,Phi_W,A and preferred-frame potentials",
            "solve the coupled Phi, phi^A and H equations with matter boundary data",
            "map the result to standard PPN gauge and read all ten coefficients without inserting GR targets",
        ],
        "verdict": (
            "The selected action has a machine-checked beta=gamma=1 unloaded "
            "static spherical solution through the required weak-field order. "
            "It is not yet a unique source-selected Solar prediction and it is "
            "not a complete first-post-Newtonian/ten-parameter PPN solution."
        ),
    }


def main() -> int:
    result = full_standard_1pn_completeness_gate()
    print("status:", result["status"])
    print("static branch EOM:", result["static_branch_EOM_exists"])
    print("beta, gamma:", result["static_branch_values"])
    print(
        "static rank/nullity:",
        result["static_PPN_information_rank"],
        result["static_PPN_information_nullity"],
    )
    print("full standard 1PN:", result["full_standard_1PN_closed"])
    print("reduced dynamics:", result["reduced_dynamics_closed"])
    print(
        "action sign:",
        result["selected_action_sign_convention_audit"]["status"],
    )
    print(
        "nonlinear null directions:",
        result["unreduced_null_direction_audit"]["status"],
    )
    print(
        "uniform power counting:",
        result["uniform_static_power_counting_audit"]["status"],
    )
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
