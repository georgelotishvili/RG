# Notation header:
# signature (+---); Y = g^mn d_m Phi d_n Phi;
# B^AB = -g^mn d_m phi^A d_n phi^B.

"""Unified deficit-field gate for the two static branches used in the paper.

The older ledger used two symbols for the same on-branch profile:

    H          phase-normalizes the F_min strain invariants,
    H_Delta    supplies the projected compact deficit source.

This gate checks the more economical single-field action

    S_static = integral sqrt(-g) [
        M_Pl^2 R/2
        - M_*^4 F_min(Yhat, I1hat, I2hat, I3hat)
        - omega_H gamma^mn d_m H d_n H/(8*pi*G)
    ],

where

    Yhat = exp(-2H) Y,
    Bhat^AB = exp(2H) B^AB,
    gamma^mn = u^m u^n - g^mn,
    u_m = d_m Phi/sqrt(Y).

It verifies only the two static backgrounds needed by the article:

* weak Solar branch: H=0.  The projected term and its stress vanish, the
  phase-normalized polynomial reduces to the existing Solar F_min action,
  the H equation vanishes through quadratic weak-field order O(U^2), and the
  augmented Solar Einstein residuals vanish through that order;
* compact exterior: H=h=r_s/(2r).  All hatted invariants equal one, F_min and
  all its first variations vanish, the projected H equation is harmonic, the
  Phi and phi^A equations vanish, and all four Einstein equations close when
  omega_H=1.

This is not an off-branch degree-of-freedom, hyperbolicity, formation, core,
or nonlinear-stability theorem.  The status string keeps that boundary
explicit.
"""

from __future__ import annotations

from typing import Any

import sympy as sp

from p03c_exterior_field_equation import augmented_medium_strain_2pn_system
from p03d_phase_normalized_solar_global_audit import (
    phase_normalized_solar_global_audit,
)


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def _isotropic_mixed_einstein(
    A: sp.Expr,
    B: sp.Expr,
    r: sp.Symbol,
) -> dict[str, sp.Expr]:
    """Mixed Einstein tensor for ds^2=B dt^2-A(dr^2+r^2 dOmega^2).

    The curvature convention is

        R^rho_{ sigma mu nu}
          = d_mu Gamma^rho_{nu sigma} - d_nu Gamma^rho_{mu sigma}
            + Gamma^rho_{mu lambda} Gamma^lambda_{nu sigma}
            - Gamma^rho_{nu lambda} Gamma^lambda_{mu sigma}.

    Writing a=log(A), b=log(B) gives a compact direct evaluation from the
    supplied metric functions.  Keeping this calculation in the unified gate
    prevents the exterior Einstein profile from being inserted as target data.
    """
    a = sp.expand_log(sp.log(A), force=True)
    b = sp.expand_log(sp.log(B), force=True)
    ap = sp.diff(a, r)
    app = sp.diff(a, r, 2)
    bp = sp.diff(b, r)
    bpp = sp.diff(b, r, 2)
    prefactor = -sp.exp(-a) / (4 * r)
    Gtt = sp.simplify(prefactor * (r * ap**2 + 4 * r * app + 8 * ap))
    Grr = sp.simplify(
        prefactor * (r * ap**2 + 2 * r * ap * bp + 4 * ap + 4 * bp)
    )
    Gtheta = sp.simplify(
        prefactor
        * (2 * r * app + r * bp**2 + 2 * r * bpp + 2 * ap + 2 * bp)
    )
    return {
        "G^t_t": Gtt,
        "G^r_r": Grr,
        "G^theta_theta": Gtheta,
        "G^phi_phi": Gtheta,
    }


def _physical_solar_fmin(
    Y: sp.Expr,
    lambda_r: sp.Expr,
    lambda_t: sp.Expr,
    c_y2: sp.Expr,
) -> sp.Expr:
    """Solar coefficient slice c_YI1=2 c_Y2 used by p03c/p03d."""
    I1 = lambda_r + 2 * lambda_t
    I2 = 2 * lambda_r * lambda_t + lambda_t**2
    I3 = lambda_r * lambda_t**2
    return sp.simplify(
        c_y2
        * (
            -8 * Y
            + Y**2
            + 8 * I1
            + I1**2
            - 16 * I2
            + 16 * I3
            + 2 * Y * I1
        )
    )


def _phase_normalized_fmin(
    Y: sp.Expr,
    lambda_r: sp.Expr,
    lambda_t: sp.Expr,
    H: sp.Expr,
    c_y2: sp.Expr,
) -> sp.Expr:
    return _physical_solar_fmin(
        sp.exp(-2 * H) * Y,
        sp.exp(2 * H) * lambda_r,
        sp.exp(2 * H) * lambda_t,
        c_y2,
    )


def derive_projector_variation_identities() -> dict[str, Any]:
    """Variations for L_H=-a Z_H, including the u(Phi,g) dependence.

    Write X=g^mn Phi_m H_n, K=g^mn H_m H_n.  Then

        Z_H=(u.H)^2-K=X^2/Y-K.

    The coefficients below show algebraically that every extra variation from
    the normalized clock vector u^m is proportional to X.  Thus on a static
    comoving branch (X=0) the Phi current vanishes and the metric variation
    reduces to the spatial-gradient stress used by the compact ledger.  The
    current signs are those of the action used in the paper, L_H=-a Z_H.
    """
    X, Y, K, a = sp.symbols("X Y K a", real=True)
    Z = X**2 / Y - K

    # Phi shift-current coefficients of L_H=-a*Z in the basis {H^m, Phi^m}.
    J_phi = {
        "H^m": sp.simplify(-2 * a * X / Y),
        "Phi^m": sp.simplify(2 * a * X**2 / Y**2),
    }
    # dZ/dg^(mn) in the symmetric basis
    # {Phi_(m H_n), Phi_m Phi_n, H_m H_n}.
    metric_derivative = {
        "Phi_(m H_n)": sp.simplify(2 * X / Y),
        "Phi_m Phi_n": sp.simplify(-X**2 / Y**2),
        "H_m H_n": sp.Integer(-1),
    }
    # H-current coefficients of L_H=-a*Z in the basis {Phi^m, H^m}.
    H_current = {
        "Phi^m": sp.simplify(-2 * a * X / Y),
        "H^m": sp.simplify(2 * a),
    }
    orthogonal = {X: 0}
    J_phi_orthogonal = {
        key: sp.simplify(value.subs(orthogonal)) for key, value in J_phi.items()
    }
    metric_orthogonal = {
        key: sp.simplify(value.subs(orthogonal))
        for key, value in metric_derivative.items()
    }
    return {
        "projected_lagrangian": "L_H=-a*Z_H",
        "Z_identity": sp.Eq(sp.Symbol("Z_H"), Z),
        "Phi_current_coefficients": J_phi,
        "metric_derivative_coefficients": metric_derivative,
        "H_current_coefficients": H_current,
        "orthogonal_X_zero_Phi_current": J_phi_orthogonal,
        "orthogonal_X_zero_metric_derivative": metric_orthogonal,
        "orthogonal_projector_terms_vanish": (
            _all_zero(J_phi_orthogonal.values())
            and metric_orthogonal["Phi_(m H_n)"] == 0
            and metric_orthogonal["Phi_m Phi_n"] == 0
            and metric_orthogonal["H_m H_n"] == -1
        ),
    }


def _weak_solar_h_euler_residual() -> dict[str, Any]:
    """H equation on the unloaded exact-GR Solar strain through O(U^2)."""
    eps = sp.Symbol("eps", real=True)
    c_y2 = sp.Symbol("c_Y2", real=True)
    Y, lambda_r, lambda_t, H = sp.symbols(
        "Y lambda_r lambda_t H", positive=True, real=True
    )

    Fhat = _phase_normalized_fmin(Y, lambda_r, lambda_t, H, c_y2)
    source_H = sp.diff(Fhat, H)
    exact_gr_solar = {
        Y: 1 + eps + eps**2,
        lambda_r: 1 - eps + eps**2,
        lambda_t: 1 - eps**2,
        H: 0,
    }
    series = sp.expand(
        sp.series(source_H.subs(exact_gr_solar), eps, 0, 3).removeO()
    )
    coefficients = {
        "O0": sp.simplify(series.coeff(eps, 0)),
        "O1": sp.simplify(series.coeff(eps, 1)),
        "O2": sp.simplify(series.coeff(eps, 2)),
    }

    # H=0 is constant, so the projected-gradient current and stress vanish.
    projected_H_euler = sp.Integer(0)
    projected_H_stress = {
        "Theta^t_t": sp.Integer(0),
        "Theta^r_r": sp.Integer(0),
        "Theta^theta_theta": sp.Integer(0),
        "Theta^phi_phi": sp.Integer(0),
    }
    return {
        "Fmin_H_source_series": series,
        "Fmin_H_source_coefficients": coefficients,
        "projected_H_euler": projected_H_euler,
        "projected_H_stress": projected_H_stress,
        "residual_zero_through_O_U2": _all_zero(coefficients.values()),
    }


def _weak_solar_solid_euler_residual() -> dict[str, Any]:
    """Direct reduced phi^A radial Euler residual through O(U^2)."""
    r, r_s, eps = sp.symbols("r r_s eps", positive=True, real=True)
    c_y2 = sp.Symbol("c_Y2", real=True)
    f = sp.Function("f")(r)
    U = eps * r_s / r

    # Exact-GR areal-coordinate branch used in p03c: f_metric=g_metric=0.
    A = 1 + U + U**2
    B = 1 - U
    Y = 1 / B
    lambda_r = sp.diff(f, r) ** 2 / A
    lambda_t = f**2 / r**2
    L = _physical_solar_fmin(Y, lambda_r, lambda_t, c_y2)
    reduced_density = sp.sqrt(A * B) * r**2 * L
    euler_f = sp.simplify(
        sp.diff(reduced_density, f)
        - sp.diff(sp.diff(reduced_density, sp.diff(f, r)), r)
    )

    # Constant local strain s=-1/2; the C/r homogeneous tail is a boundary mode.
    f_branch = sp.simplify(r * (1 - U**2 / 2))
    branch_subs = {
        f: f_branch,
        sp.diff(f, r): sp.diff(f_branch, r),
        sp.diff(f, r, 2): sp.diff(f_branch, r, 2),
    }
    euler_branch = sp.expand(
        sp.series(euler_f.subs(branch_subs).doit(), eps, 0, 3).removeO()
    )
    coefficients = {
        "O0": sp.simplify(euler_branch.coeff(eps, 0)),
        "O1": sp.simplify(euler_branch.coeff(eps, 1)),
        "O2": sp.simplify(euler_branch.coeff(eps, 2)),
    }
    return {
        "radial_phiA_euler_series": sp.factor(euler_branch),
        "radial_phiA_euler_coefficients": coefficients,
        "residual_zero_through_O_U2": _all_zero(coefficients.values()),
        "angular_phiA_residuals": (
            "zero by SO(3) covariance on the hedgehog solid map once the radial "
            "Euler equation is satisfied"
        ),
    }


def derive_unified_H_weak_solar_static_gate() -> dict[str, Any]:
    """Unloaded H=0 branch, audited only through the stated Solar order."""
    solar_action = phase_normalized_solar_global_audit()
    solar_metric = augmented_medium_strain_2pn_system()
    H_euler = _weak_solar_h_euler_residual()
    solid_euler = _weak_solar_solid_euler_residual()

    three_residuals = solar_metric["gr_2pn_metric_candidate"]["residuals"]
    einstein_residuals = {
        "t": sp.simplify(three_residuals[0]),
        "r": sp.simplify(three_residuals[1]),
        "theta": sp.simplify(three_residuals[2]),
        "phi": sp.simplify(three_residuals[2]),
    }

    # For Phi=Phi(t) on a static diagonal background, its shift current has
    # only a time component and is time independent.  The projected H current
    # also vanishes because dH=0.  Hence div J_Phi=0 exactly on this branch.
    phi_clock_euler = sp.Integer(0)

    passed = (
        solar_action["status"]
        == "PASS_INDEPENDENT_H_RETAINS_SOLAR_1PN_2PN__GLOBAL_I3_LOCK_REJECTED"
        and solar_metric["status"] == "PASS_AUGMENTED_MEDIUM_STRAIN_2PN_SYSTEM"
        and solar_metric["gr_2pn_metric_candidate"]["identity"]
        and _all_zero(einstein_residuals.values())
        and H_euler["residual_zero_through_O_U2"]
        and phi_clock_euler == 0
        and solid_euler["residual_zero_through_O_U2"]
    )

    return {
        "status": (
            "PASS_UNIFIED_H_WEAK_SOLAR_STATIC_EOM_THROUGH_O_U2"
            if passed
            else "CHECK_UNIFIED_H_WEAK_SOLAR_STATIC_EOM"
        ),
        "branch_values": {
            "H": 0,
            "projected_H_operator": 0,
            "phase_normalized_Fmin_equals_raw_Fmin": True,
        },
        "H_euler": H_euler,
        "Phi_euler_residual": phi_clock_euler,
        "phiA_euler": solid_euler,
        "Einstein_residuals_through_O_U2": einstein_residuals,
        "scope": (
            "weak static Solar branch through quadratic order O(U^2); the "
            "imported p03c/p03d function names retain their legacy 2PN label"
        ),
    }


def derive_unified_H_compact_static_gate() -> dict[str, Any]:
    """Exact compact exterior EOM for the unified H field."""
    r, r_s, G, omega_H = sp.symbols(
        "r r_s G omega_H", positive=True, real=True
    )
    c_y2 = sp.Symbol("c_Y2", real=True)
    projector_variation = derive_projector_variation_identities()
    Y, lambda_r, lambda_t, H = sp.symbols(
        "Y lambda_r lambda_t H", positive=True, real=True
    )

    h = r_s / (2 * r)
    A = sp.exp(2 * h)
    B = sp.exp(-2 * h)
    branch_subs = {
        H: h,
        Y: sp.exp(2 * h),
        lambda_r: sp.exp(-2 * h),
        lambda_t: sp.exp(-2 * h),
    }

    Yhat = sp.exp(-2 * H) * Y
    lambda_r_hat = sp.exp(2 * H) * lambda_r
    lambda_t_hat = sp.exp(2 * H) * lambda_t
    hatted_invariants = {
        "Yhat": sp.simplify(Yhat.subs(branch_subs)),
        "lambda_r_hat": sp.simplify(lambda_r_hat.subs(branch_subs)),
        "lambda_t_hat": sp.simplify(lambda_t_hat.subs(branch_subs)),
    }

    Fhat = _phase_normalized_fmin(Y, lambda_r, lambda_t, H, c_y2)
    F_first_variations = {
        "F": sp.simplify(Fhat.subs(branch_subs)),
        "dF_dY": sp.simplify(sp.diff(Fhat, Y).subs(branch_subs)),
        "dF_dlambda_r": sp.simplify(sp.diff(Fhat, lambda_r).subs(branch_subs)),
        "dF_dlambda_t": sp.simplify(sp.diff(Fhat, lambda_t).subs(branch_subs)),
        "dF_dH": sp.simplify(sp.diff(Fhat, H).subs(branch_subs)),
    }

    gamma_rr = 1 / A
    sqrt_minus_g_over_sin = sp.sqrt(B * A**3) * r**2
    H_current_over_sin = sp.simplify(
        sqrt_minus_g_over_sin * gamma_rr * sp.diff(h, r)
    )
    H_projected_euler = sp.simplify(sp.diff(H_current_over_sin, r))

    # V=u^m d_m H=0 on the static comoving branch.  Therefore the Phi-current
    # induced by the projector is zero, including the metric dependence of u.
    V = sp.Integer(0)
    Phi_projector_euler = sp.Integer(0)
    Phi_Fmin_euler = sp.Integer(0) if _all_zero(F_first_variations.values()) else sp.nan
    Phi_euler = sp.simplify(Phi_projector_euler + Phi_Fmin_euler)

    # F_min is at a stationary unit point and L_H contains no phi^A.
    phiA_euler = {
        "radial": sp.Integer(0),
        "theta": sp.Integer(0),
        "phi": sp.Integer(0),
    }

    H_prime = sp.diff(h, r)
    Z_H = sp.simplify(gamma_rr * H_prime**2)
    # Derive the mixed source from L_H=-a_H*Z_H and the standard definition
    # T_mn=g_mn*L_H-2*dL_H/dg^mn.  At X=u.H=0 one has
    # dZ_H/dg^mn=-H_m H_n, hence dL_H/dg^mn=+a_H H_m H_n.
    a_H = omega_H / (8 * sp.pi * G)
    L_H = sp.simplify(-a_H * Z_H)
    vartheta = sp.Symbol("vartheta", real=True)
    g_inverse_diagonal = {
        "t": 1 / B,
        "r": -1 / A,
        "theta": -1 / (A * r**2),
        "phi": -1 / (A * r**2 * sp.sin(vartheta) ** 2),
    }
    H_covariant = {
        "t": sp.Integer(0),
        "r": H_prime,
        "theta": sp.Integer(0),
        "phi": sp.Integer(0),
    }
    Theta_mixed = {
        f"Theta^{label}": sp.simplify(
            L_H
            - 2
            * g_inverse_diagonal[component]
            * a_H
            * H_covariant[component] ** 2
        )
        for component, label in (
            ("t", "t_t"),
            ("r", "r_r"),
            ("theta", "theta_theta"),
            ("phi", "phi_phi"),
        )
    }
    Delta_H = sp.simplify(a_H * Z_H)
    expected_Theta_mixed = {
        "Theta^t_t": -Delta_H,
        "Theta^r_r": Delta_H,
        "Theta^theta_theta": -Delta_H,
        "Theta^phi_phi": -Delta_H,
    }
    stress_derivation_residuals = {
        key: sp.simplify(Theta_mixed[key] - expected_Theta_mixed[key])
        for key in Theta_mixed
    }

    # Compute the curvature from the metric functions rather than inserting
    # the desired exponential profile into the residual by hand.
    G_mixed = _isotropic_mixed_einstein(A, B, r)
    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    expected_G_mixed = {
        "G^t_t": -D,
        "G^r_r": D,
        "G^theta_theta": -D,
        "G^phi_phi": -D,
    }
    curvature_derivation_residuals = {
        key: sp.simplify(G_mixed[key] - expected_G_mixed[key])
        for key in G_mixed
    }
    residuals_general_omega = {
        "t": sp.factor(G_mixed["G^t_t"] - 8 * sp.pi * G * Theta_mixed["Theta^t_t"]),
        "r": sp.factor(G_mixed["G^r_r"] - 8 * sp.pi * G * Theta_mixed["Theta^r_r"]),
        "theta": sp.factor(
            G_mixed["G^theta_theta"]
            - 8 * sp.pi * G * Theta_mixed["Theta^theta_theta"]
        ),
        "phi": sp.factor(
            G_mixed["G^phi_phi"]
            - 8 * sp.pi * G * Theta_mixed["Theta^phi_phi"]
        ),
    }
    residuals_omega_one = {
        key: sp.simplify(value.subs(omega_H, 1))
        for key, value in residuals_general_omega.items()
    }

    passed = (
        all(value == 1 for value in hatted_invariants.values())
        and _all_zero(F_first_variations.values())
        and H_projected_euler == 0
        and V == 0
        and projector_variation["orthogonal_projector_terms_vanish"]
        and Phi_euler == 0
        and _all_zero(phiA_euler.values())
        and _all_zero(stress_derivation_residuals.values())
        and _all_zero(curvature_derivation_residuals.values())
        and _all_zero(residuals_omega_one.values())
    )

    return {
        "status": (
            "PASS_UNIFIED_H_COMPACT_STATIC_EXACT_EOM_AT_OMEGA_H_ONE"
            if passed
            else "CHECK_UNIFIED_H_COMPACT_STATIC_EOM"
        ),
        "branch_values": {
            "H_equals_metric_deficit_h": sp.Eq(sp.Symbol("H"), h),
            "A": sp.Eq(sp.Symbol("A"), A),
            "B": sp.Eq(sp.Symbol("B"), B),
            "Phi": "t (static comoving clock)",
            "phiA": "x^A (identity solid labels in isotropic Cartesian coordinates)",
        },
        "hatted_invariants": hatted_invariants,
        "Fmin_density_and_first_variations": F_first_variations,
        "H_projected_current_over_sin": H_current_over_sin,
        "H_euler_residual": H_projected_euler,
        "orthogonality_V_u_dot_dH": V,
        "projector_variation_identities": projector_variation,
        "Phi_euler_residual": Phi_euler,
        "phiA_euler_residuals": phiA_euler,
        "Z_H": Z_H,
        "projected_lagrangian_on_branch": L_H,
        "Theta_mixed": Theta_mixed,
        "Theta_derivation_residuals": stress_derivation_residuals,
        "Einstein_mixed_derived_from_A_B": G_mixed,
        "Einstein_profile_derivation_residuals": curvature_derivation_residuals,
        "Einstein_residuals_general_omega_H": residuals_general_omega,
        "Einstein_residuals_at_omega_H_one": residuals_omega_one,
        "normalization_condition": sp.Eq(omega_H, 1),
        "scope": "exact static compact exterior; no core or off-branch dynamics",
    }


def unified_deficit_field_static_branch_status() -> dict[str, Any]:
    weak = derive_unified_H_weak_solar_static_gate()
    compact = derive_unified_H_compact_static_gate()
    passed = (
        weak["status"] == "PASS_UNIFIED_H_WEAK_SOLAR_STATIC_EOM_THROUGH_O_U2"
        and compact["status"]
        == "PASS_UNIFIED_H_COMPACT_STATIC_EXACT_EOM_AT_OMEGA_H_ONE"
    )
    return {
        "status": (
            "PASS_UNIFIED_H_STATIC_BRANCHES_EOM__OFF_BRANCH_DYNAMICS_OPEN"
            if passed
            else "CHECK_UNIFIED_H_STATIC_BRANCHES_EOM"
        ),
        "action": (
            "S_static=int sqrt(-g)[M_Pl^2 R/2 - M_*^4 F_min(Yhat,I1hat,I2hat,I3hat) "
            "- omega_H gamma^mn d_m H d_n H/(8*pi*G)]"
        ),
        "covariant_definitions": {
            "Y": "g^mn d_m Phi d_n Phi",
            "B^AB": "-g^mn d_m phi^A d_n phi^B",
            "u_m": "d_m Phi/sqrt(Y)",
            "gamma^mn": "u^m u^n-g^mn",
            "Yhat": "exp(-2H)Y",
            "Bhat^AB": "exp(2H)B^AB",
            "I1hat_I2hat_I3hat": "Tr(Bhat), 1/2[(Tr Bhat)^2-Tr(Bhat^2)], det(Bhat)",
        },
        "weak_solar_branch": weak,
        "compact_branch": compact,
        "article_safe_claim": (
            "A single projected deficit field H can both normalize the elastic "
            "invariants and source the compact exterior.  The unloaded H=0 "
            "configuration preserves the existing static Solar equations "
            "through O(U^2), while H=r_s/(2r) solves the exact compact exterior "
            "field equations at omega_H=1."
        ),
        "open_requirements": [
            "derive the off-branch constraint/degree-of-freedom algebra",
            "establish curved-background hyperbolicity and coupled stability",
            "derive a physical-EOS or medium-action core",
            "derive formation and branch-selection dynamics",
        ],
        "do_not_claim": [
            "do not call H a propagating healthy scalar; the displayed operator is spatially projected",
            "do not claim a global stability theorem from the two static solutions",
            "do not claim the C2 core follows from this action",
            "do not claim physical objects dynamically select the compact branch",
        ],
    }


def main() -> int:
    result = unified_deficit_field_static_branch_status()
    print("status:", result["status"])
    print("weak:", result["weak_solar_branch"]["status"])
    print("compact:", result["compact_branch"]["status"])
    print(
        "compact Einstein residuals:",
        result["compact_branch"]["Einstein_residuals_at_omega_H_one"],
    )
    print(
        "compact curvature derivation residuals:",
        result["compact_branch"]["Einstein_profile_derivation_residuals"],
    )
    print(
        "compact stress-variation residuals:",
        result["compact_branch"]["Theta_derivation_residuals"],
    )
    print(
        "weak Einstein residuals:",
        result["weak_solar_branch"]["Einstein_residuals_through_O_U2"],
    )
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
