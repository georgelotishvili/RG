# Notation header:
# signature (+---); compact branch uses positive metric functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.
#
# This gate answers the referee's tensor-level objection to p05j:
# a passive phase normalization cannot remove a true metric stress tensor.
# Therefore the compact exponential exterior is tested against the mistaken
# insertion of raw F_min as an ordinary RHS stress plus the projected L_Delta
# stress in one field equation.  The nonzero residual is the double-counting
# diagnostic used by p05p.

from __future__ import annotations

import sympy as sp

from p05j_fmin_compact_exterior_gate import (
    _coefficient_symbols,
    _fmin_polynomial,
    solar_physical_fmin_coefficients,
)


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def _raw_fmin_mixed_stress_over_cY2(w):
    """Raw F_min mixed stress on Y=w, lambda_r=lambda_t=1/w."""
    coeff_symbols = _coefficient_symbols()
    _, c_Y2, _, _, _, _, _ = coeff_symbols
    Y, lambda_r, lambda_t = sp.symbols(
        "Y lambda_r lambda_t", positive=True, real=True
    )

    F = _fmin_polynomial(Y, lambda_r, lambda_t, coeff_symbols)
    F_solar = sp.simplify(F.subs(solar_physical_fmin_coefficients(coeff_symbols)))

    F_Y = sp.diff(F_solar, Y)
    F_lr = sp.diff(F_solar, lambda_r)
    F_lt = sp.diff(F_solar, lambda_t)

    theta_t = sp.simplify(2 * Y * F_Y - F_solar)
    theta_r = sp.simplify(2 * lambda_r * F_lr - F_solar)
    theta_theta = sp.simplify(lambda_t * F_lt - F_solar)

    branch = {Y: w, lambda_r: 1 / w, lambda_t: 1 / w}
    return {
        "ThetaF^t_t/(M4*cY2)": sp.factor(sp.simplify(theta_t.subs(branch) / c_Y2)),
        "ThetaF^r_r/(M4*cY2)": sp.factor(sp.simplify(theta_r.subs(branch) / c_Y2)),
        "ThetaF^theta_theta/(M4*cY2)": sp.factor(
            sp.simplify(theta_theta.subs(branch) / c_Y2)
        ),
        "ThetaF^phi_phi/(M4*cY2)": sp.factor(
            sp.simplify(theta_theta.subs(branch) / c_Y2)
        ),
    }


def derive_full_raw_fmin_plus_ldelta_residual_gate():
    """
    Full mixed tensor residual for the compact exponential branch.

    The compact metric has

        G^t_t=-D, G^r_r=D, G^theta_theta=G^phi_phi=-D,
        D=r_s^2 exp(-r_s/r)/(4 r^4).

    The projected deficit source has

        Theta_Delta^t_t=-Delta_P, Theta_Delta^r_r=Delta_P,
        Theta_Delta^theta_theta=Theta_Delta^phi_phi=-Delta_P,
        Delta_P=D/(8*pi*G).

    The raw F_min contribution is inserted with the physical Solar-family
    coefficient slice as if it were ordinary active compact matter.  This is
    the wrong ledger placement, but it is the necessary diagnostic test.  The
    residual is

        R^mu_mu = G^mu_mu
                 - 8*pi*G*(omega_delta*Theta_Delta^mu_mu
                            + M4*c_Y2*ThetaF_unit^mu_mu).
    """
    r, r_s, G, M4, c_Y2, omega_delta = sp.symbols(
        "r r_s G M4 c_Y2 omega_delta", positive=True, real=True
    )
    kappa_F = sp.symbols("kappa_F", real=True)
    u = sp.symbols("u", positive=True, real=True)
    w = sp.symbols("w", positive=True, real=True)

    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    delta_p = sp.simplify(D / (8 * sp.pi * G))

    G_mixed = {
        "t": -D,
        "r": D,
        "theta": -D,
        "phi": -D,
    }
    theta_delta_mixed = {
        "t": -delta_p,
        "r": delta_p,
        "theta": -delta_p,
        "phi": -delta_p,
    }

    theta_f_w = _raw_fmin_mixed_stress_over_cY2(w)
    theta_f_branch = {
        "t": theta_f_w["ThetaF^t_t/(M4*cY2)"].subs(w, sp.exp(r_s / r)),
        "r": theta_f_w["ThetaF^r_r/(M4*cY2)"].subs(w, sp.exp(r_s / r)),
        "theta": theta_f_w["ThetaF^theta_theta/(M4*cY2)"].subs(w, sp.exp(r_s / r)),
        "phi": theta_f_w["ThetaF^phi_phi/(M4*cY2)"].subs(w, sp.exp(r_s / r)),
    }

    residuals = {
        key: sp.factor(
            sp.simplify(
                G_mixed[key]
                - 8 * sp.pi * G * (
                    omega_delta * theta_delta_mixed[key]
                    + M4 * c_Y2 * theta_f_branch[key]
                )
            )
        )
        for key in G_mixed
    }
    residuals_no_delta_error = {
        key: sp.factor(sp.simplify(value.subs(omega_delta, 1)))
        for key, value in residuals.items()
    }
    residuals_over_D = {
        key: sp.factor(sp.simplify(value / D)) for key, value in residuals.items()
    }
    residuals_over_D_u = {
        key: sp.factor(
            sp.series(value.subs({r: r_s / u, omega_delta: 1}), u, 0, 3).removeO()
        )
        for key, value in residuals_over_D.items()
    }

    # Algebraic no-go independent of the radial profile.  Let kappa_F stand for
    # the whole F_min gravitational load 8*pi*G*M4*c_Y2.  The r and theta
    # residuals have opposite geometry/projected-source signs, while raw F_min
    # gives equal radial and tangential stresses on this identity branch.
    theta_fr = theta_f_w["ThetaF^r_r/(M4*cY2)"]
    theta_ft = theta_f_w["ThetaF^theta_theta/(M4*cY2)"]
    radial_plus_angular_no_go = sp.factor(
        sp.simplify(-kappa_F * (theta_fr + theta_ft))
    )
    theta_fr_at_w2 = sp.simplify(theta_fr.subs(w, 2))
    exact_closure_requires = (
        "kappa_F=0 or ThetaF^r_r=ThetaF^theta_theta=0; "
        "on the physical compact branch ThetaF^r_r(w=2)=19/4, so the raw "
        "F_min load cannot be absorbed by changing omega_delta."
    )

    raw_full_closes = _all_zero(residuals_no_delta_error.values())

    return {
        "full_raw_residual_status": (
            "PASS_RAW_FMIN_PLUS_LDELTA_CLOSES_COMPACT_EXTERIOR"
            if raw_full_closes
            else "FAIL_RAW_FMIN_ADDS_NONZERO_TENSOR_RESIDUAL"
        ),
        "D_profile": sp.Eq(sp.Symbol("D"), D),
        "Delta_P": sp.Eq(sp.Symbol("Delta_P"), delta_p),
        "Einstein_mixed": G_mixed,
        "Theta_Delta_mixed": theta_delta_mixed,
        "ThetaF_raw_mixed_over_M4_cY2_w": theta_f_w,
        "full_residuals": residuals,
        "full_residuals_with_omega_delta_1": residuals_no_delta_error,
        "full_residuals_over_D_with_omega_delta_1_u_series": residuals_over_D_u,
        "radial_plus_angular_no_go": sp.Eq(
            sp.Symbol("R_r+R_theta"), radial_plus_angular_no_go
        ),
        "ThetaF_radial_at_w_equals_2_over_M4_cY2": theta_fr_at_w2,
        "exact_closure_requires": exact_closure_requires,
        "verdict": (
            "The tensor objection is correct for the mistaken ledger where raw "
            "F_min is added as ordinary compact RHS matter: the projected "
            "L_Delta source already matches the compact exponential Einstein "
            "tensor, and raw F_min leaves a nonzero tensor residual.  This is "
            "the double-counting mark.  No constant retuning of the projected "
            "load can absorb it, because the raw F_min radial and tangential "
            "stresses have the same branch value while the compact geometry "
            "requires opposite radial/tangential signs."
        ),
    }


def derive_compact_projected_full_residual_gate():
    """
    Exact compact-branch closure when F_min is structural, not active RHS.

    This is the tensor statement used by the no-double-count source ledger:
    on the compact pure-phase exterior the active gravitational source is the
    projected deficit channel, and the structural F_min sector is not added
    again as an ordinary compact RHS stress.
    """
    r, r_s, G = sp.symbols("r r_s G", positive=True, real=True)
    Omega_F, omega_delta = sp.symbols("Omega_F omega_delta", real=True)
    M4, c_Y2 = sp.symbols("M4 c_Y2", real=True)

    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    delta_p = sp.simplify(D / (8 * sp.pi * G))
    w = sp.Symbol("w", positive=True, real=True)
    w_expr = sp.exp(r_s / r)
    theta_f = _raw_fmin_mixed_stress_over_cY2(w)
    theta_f_branch = {
        "t": theta_f["ThetaF^t_t/(M4*cY2)"].subs(w, w_expr),
        "r": theta_f["ThetaF^r_r/(M4*cY2)"].subs(w, w_expr),
        "theta": theta_f["ThetaF^theta_theta/(M4*cY2)"].subs(w, w_expr),
        "phi": theta_f["ThetaF^phi_phi/(M4*cY2)"].subs(w, w_expr),
    }

    G_mixed = {"t": -D, "r": D, "theta": -D, "phi": -D}
    theta_delta = {"t": -delta_p, "r": delta_p, "theta": -delta_p, "phi": -delta_p}

    residuals = {
        key: sp.factor(
            sp.simplify(
                G_mixed[key]
                - 8 * sp.pi * G * (
                    omega_delta * theta_delta[key]
                    + Omega_F * M4 * c_Y2 * theta_f_branch[key]
                )
            )
        )
        for key in G_mixed
    }
    compact_rule = {omega_delta: 1, Omega_F: 0}
    compact_residuals = {
        key: sp.factor(sp.simplify(value.subs(compact_rule)))
        for key, value in residuals.items()
    }

    return {
        "projected_compact_residual_status": (
            "PASS_COMPACT_BRANCH_CLOSES_WHEN_ACTIVE_FMIN_WEIGHT_IS_ZERO"
            if _all_zero(compact_residuals.values())
            else "CHECK_COMPACT_BRANCH_PROJECTED_RESIDUAL"
        ),
        "branch_weights": {
            "omega_delta": sp.Eq(omega_delta, 1),
            "Omega_F_compact": sp.Eq(Omega_F, 0),
        },
        "full_weighted_residuals": residuals,
        "compact_projected_residuals": compact_residuals,
        "article_safe_statement": (
            "The compact exponential exterior is a solution of the projected "
            "compact branch, where the active source is L_Delta^perp.  F_min "
            "is the structural medium sector and is not added again as an "
            "ordinary compact RHS stress.  This is a no-double-count source "
            "ledger statement, not a passive change of variables."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18k: Full compact source residual gate")
    print("=" * 72)
    sections = [
        (
            "1. Full raw F_min + L_Delta residual",
            derive_full_raw_fmin_plus_ldelta_residual_gate(),
        ),
        (
            "2. Compact projected full residual",
            derive_compact_projected_full_residual_gate(),
        ),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:54s}: {value}")
