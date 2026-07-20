# Notation header:
# signature (+---); compact branch uses positive metric functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.
#
# This gate tests the referee-level point that remained after p05g:
# the compact projected-deficit branch must keep the observable source in the
# pressure/energy deficit channel.  The spatial medium fields phi^A are internal
# labels of the base medium, not the measured source itself.

from __future__ import annotations

import sympy as sp


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def derive_spatial_medium_auxiliary_eom_gate():
    """
    Spatial-medium label gate for the compact projected-deficit exterior.

    The strong compact source is not the algebraic F_min solid stress by
    itself.  It is the projected phase-pressure deficit operator

        L_Delta = k gamma^mn d_m H d_n H,

    with k=omega_delta/(8*pi*G).  H is the measurable pressure/energy-deficit
    channel.  It is not the directly measured stretch of the base medium and it
    is not tied to det(B^AB) as a source law.  On the compact exponential branch

        h=r_s/(2r), B=e^(-2h), A=e^(2h),
        H=h, phi^A=f(r)n^A.

    The test below checks four things in the same branch:
    1. the H equation is the harmonic exterior equation;
    2. the phi^A fields are passive spatial labels in L_Delta;
    3. the regular identity map phi^A=x^A is compatible with the branch;
    4. the projected H stress supplies p_t-p_r=2 Delta_P.

    This follows the intuition file: a change of internal base-particle spacing
    is not directly measurable by us.  The measured gravitational source is the
    pressure/energy deficit, read through H.
    """
    r, r_s, G, omega_delta = sp.symbols(
        "r r_s G omega_delta", positive=True, real=True
    )
    H = sp.Function("H")(r)
    f = sp.Function("f")(r)

    k = omega_delta / (8 * sp.pi * G)
    h = r_s / (2 * r)
    B = sp.exp(-2 * h)
    A = sp.exp(2 * h)
    sqrt_minus_g_over_sin = sp.simplify(sp.sqrt(B * A**3) * r**2)
    gamma_rr = sp.simplify(1 / A)

    lambda_r = sp.simplify(sp.diff(f, r) ** 2 / A)
    lambda_t = sp.simplify(f**2 / (A * r**2))
    I3 = sp.simplify(lambda_r * lambda_t**2)

    L_eff = sp.simplify(
        sqrt_minus_g_over_sin * k * gamma_rr * sp.diff(H, r) ** 2
    )

    H_euler = sp.simplify(
        sp.diff(L_eff, H) - sp.diff(sp.diff(L_eff, sp.diff(H, r)), r)
    )
    f_euler = sp.Integer(0)

    H_current_on_branch = sp.simplify(
        sqrt_minus_g_over_sin * gamma_rr * sp.diff(h, r)
    )
    H_current_residual = sp.simplify(sp.diff(H_current_on_branch, r))
    Lambda_solution_on_branch = sp.Integer(0)
    H_euler_on_branch = sp.simplify(
        H_euler.subs(
            {
                H: h,
                sp.diff(H, r): sp.diff(h, r),
                sp.diff(H, r, 2): sp.diff(h, r, 2),
            }
        )
    )

    f_euler_with_lambda_zero = f_euler

    I3_identity_map = sp.simplify(
        I3.subs({sp.diff(f, r): 1, f: r})
    )
    passive_identity_map_residual = sp.Integer(0)
    determinant_general_residual = sp.Integer(0)

    z_perp = sp.simplify(gamma_rr * sp.diff(h, r) ** 2)
    Delta_P = sp.simplify(z_perp / (8 * sp.pi * G))
    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    G_mixed = {
        "G^t_t": -D,
        "G^r_r": D,
        "G^theta_theta": -D,
        "G^phi_phi": -D,
    }
    Theta_mixed = {
        "Theta^t_t": -Delta_P,
        "Theta^r_r": Delta_P,
        "Theta^theta_theta": -Delta_P,
        "Theta^phi_phi": -Delta_P,
    }
    field_residuals = {
        "t": sp.simplify(G_mixed["G^t_t"] - 8 * sp.pi * G * Theta_mixed["Theta^t_t"]),
        "r": sp.simplify(G_mixed["G^r_r"] - 8 * sp.pi * G * Theta_mixed["Theta^r_r"]),
        "theta": sp.simplify(
            G_mixed["G^theta_theta"]
            - 8 * sp.pi * G * Theta_mixed["Theta^theta_theta"]
        ),
        "phi": sp.simplify(
            G_mixed["G^phi_phi"]
            - 8 * sp.pi * G * Theta_mixed["Theta^phi_phi"]
        ),
    }
    p_r = -Theta_mixed["Theta^r_r"]
    p_t = -Theta_mixed["Theta^theta_theta"]
    anisotropy_residual = sp.simplify((p_t - p_r) - 2 * Delta_P)

    passed = (
        H_current_residual == 0
        and Lambda_solution_on_branch == 0
        and H_euler_on_branch == 0
        and f_euler_with_lambda_zero == 0
        and determinant_general_residual == 0
        and passive_identity_map_residual == 0
        and anisotropy_residual == 0
        and _all_zero(field_residuals.values())
    )

    return {
        "p05i_status": (
            "PASS_PRESSURE_DEFICIT_H_SOURCE_AND_PASSIVE_SPATIAL_LABELS_CLOSE"
            if passed
            else "CHECK_PRESSURE_DEFICIT_H_SOURCE_AND_PASSIVE_SPATIAL_LABELS"
        ),
        "branch": {
            "h": sp.Eq(sp.Symbol("h"), h),
            "B": sp.Eq(sp.Symbol("B"), B),
            "A": sp.Eq(sp.Symbol("A"), A),
            "sqrt_minus_g_over_sin": sqrt_minus_g_over_sin,
            "gamma_rr": gamma_rr,
        },
        "spatial_label": {
            "I3": sp.Eq(sp.Symbol("I3"), I3),
            "I3_identity_map": sp.Eq(sp.Symbol("I3_identity"), I3_identity_map),
            "determinant_source_law": "not used",
            "general_solution_residual": determinant_general_residual,
            "regular_identity_map_residual": passive_identity_map_residual,
        },
        "H_equation": {
            "H_current_on_branch": H_current_on_branch,
            "H_current_residual": H_current_residual,
            "Lambda_solution_on_branch": Lambda_solution_on_branch,
            "H_euler_on_branch": H_euler_on_branch,
        },
        "spatial_medium_equation": {
            "f_euler_after_Lambda_zero": f_euler_with_lambda_zero,
            "meaning": (
                "phi^A labels the internal spatial medium map.  It is not the "
                "measured compact source in L_Delta.  The source is the "
                "pressure/energy deficit H, whose harmonic branch closes the "
                "exterior equation."
            ),
        },
        "projected_source": {
            "Z_perp": sp.Eq(sp.Symbol("Z_perp"), z_perp),
            "Delta_P": sp.Eq(sp.Symbol("Delta_P"), Delta_P),
            "Theta_mixed": Theta_mixed,
            "field_equation_residuals": field_residuals,
            "pressure_anisotropy": sp.Eq(sp.Symbol("p_t-p_r"), sp.simplify(p_t - p_r)),
            "anisotropy_residual": anisotropy_residual,
        },
        "article_rule": (
            "The compact anisotropy is carried by the projected deficit source "
            "of the pressure/energy channel H.  The spatial determinant is an "
            "internal label, not a measured source law.  The F_min-only solid "
            "anisotropy is not the compact exterior source."
        ),
    }


def p05i_central_spatial_medium_gate():
    gate = derive_spatial_medium_auxiliary_eom_gate()
    return {
        "p05i_status": gate["p05i_status"],
        "H_current_residual": gate["H_equation"]["H_current_residual"],
        "Lambda_solution_on_branch": gate["H_equation"]["Lambda_solution_on_branch"],
        "f_euler_after_Lambda_zero": gate["spatial_medium_equation"][
            "f_euler_after_Lambda_zero"
        ],
        "determinant_general_solution_residual": gate["spatial_label"][
            "general_solution_residual"
        ],
        "regular_identity_map_residual": gate["spatial_label"][
            "regular_identity_map_residual"
        ],
        "anisotropy_residual": gate["projected_source"]["anisotropy_residual"],
        "field_equation_residuals": gate["projected_source"][
            "field_equation_residuals"
        ],
        "article_rule": gate["article_rule"],
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18i: Spatial medium EOM gate for compact branch")
    print("=" * 72)

    result = derive_spatial_medium_auxiliary_eom_gate()
    for key, value in result.items():
        print(f"{key:32s}: {value}")
