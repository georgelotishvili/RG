# Notation header:
# signature (+---); compact branch uses positive metric functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.
#
# This gate answers the referee's remaining point after p05i:
# if the structural F_min sector is inserted again as an ordinary compact RHS
# source on the same geometry, it produces a tensor residual.  That residual is
# a double-counting diagnostic.  The compact source ledger is repaired in p05p.

from __future__ import annotations

import sympy as sp


def _coefficient_symbols():
    return sp.symbols(
        "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1",
        real=True,
    )


def solar_physical_fmin_coefficients(coeff_symbols=None):
    """p03/p01 physical Solar-family coefficient slice used in the article."""
    if coeff_symbols is None:
        coeff_symbols = _coefficient_symbols()
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = coeff_symbols
    return {
        c_Y: -8 * c_Y2,
        c_I1: 8 * c_Y2,
        c_I1sq: c_Y2,
        c_I2: -16 * c_Y2,
        c_I3: 16 * c_Y2,
        c_YI1: 2 * c_Y2,
    }


def _fmin_polynomial(Y, lambda_r, lambda_t, coeff_symbols):
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = coeff_symbols
    I1 = lambda_r + 2 * lambda_t
    I2 = 2 * lambda_r * lambda_t + lambda_t**2
    I3 = lambda_r * lambda_t**2
    F = (
        c_Y * Y
        + c_Y2 * Y**2
        + c_I1 * I1
        + c_I1sq * I1**2
        + c_I2 * I2
        + c_I3 * I3
        + c_YI1 * Y * I1
    )
    return sp.simplify(F)


def derive_fmin_compact_identity_branch_residual_gate():
    """
    Raw F_min residual on the compact exponential identity medium branch.

    Compact branch:
        h=r_s/(2r), B=e^(-2h), A=e^(2h), Y=1/B=e^(2h).

    Spatial medium identity branch:
        phi^A=f(r)n^A, f=r,
        lambda_r=lambda_t=1/A=e^(-2h).

    The gate computes:
    - F_min on this branch;
    - mixed stress components from F_min;
    - the F_min contribution to the radial phi^A Euler equation;
    - the asymptotic scaling against the projected deficit source.

    The result is not used as a physical compact RHS source.  It is the audit
    showing what goes wrong if the structural medium modulus is counted twice:
    first as the mechanism that forms the geometry, then again as matter on
    the same geometry.
    """
    r, r_s, G, M4 = sp.symbols("r r_s G M4", positive=True, real=True)
    u = sp.symbols("u", positive=True, real=True)
    w = sp.symbols("w", positive=True, real=True)
    coeff_symbols = _coefficient_symbols()
    _, c_Y2, _, _, _, _, _ = coeff_symbols

    Y, lambda_r, lambda_t = sp.symbols(
        "Y lambda_r lambda_t", positive=True, real=True
    )
    F = _fmin_polynomial(Y, lambda_r, lambda_t, coeff_symbols)
    coeff_subs = solar_physical_fmin_coefficients(coeff_symbols)

    F_solar = sp.simplify(F.subs(coeff_subs))
    F_w = sp.factor(
        sp.simplify(F_solar.subs({Y: w, lambda_r: 1 / w, lambda_t: 1 / w}))
    )
    F_w_over_c = sp.factor(sp.simplify(F_w / c_Y2))
    F_u_over_c = sp.factor(sp.simplify(F_w_over_c.subs(w, sp.exp(u))))
    F_u_series = sp.factor(sp.series(F_u_over_c, u, 0, 5).removeO())

    F_Y = sp.diff(F_solar, Y)
    F_lr = sp.diff(F_solar, lambda_r)
    F_lt = sp.diff(F_solar, lambda_t)
    T_t = sp.simplify(2 * Y * F_Y - F_solar)
    T_r = sp.simplify(2 * lambda_r * F_lr - F_solar)
    T_theta = sp.simplify(lambda_t * F_lt - F_solar)
    branch = {Y: w, lambda_r: 1 / w, lambda_t: 1 / w}
    T_w = {
        "ThetaF^t_t/M4": sp.factor(sp.simplify(T_t.subs(branch))),
        "ThetaF^r_r/M4": sp.factor(sp.simplify(T_r.subs(branch))),
        "ThetaF^theta_theta/M4": sp.factor(sp.simplify(T_theta.subs(branch))),
    }
    T_w_over_c = {
        key: sp.factor(sp.simplify(value / c_Y2)) for key, value in T_w.items()
    }
    T_u_over_c = {
        key: sp.factor(sp.simplify(value.subs(w, sp.exp(u))))
        for key, value in T_w_over_c.items()
    }
    T_u_series = {
        key: sp.factor(sp.series(value, u, 0, 5).removeO())
        for key, value in T_u_over_c.items()
    }

    # Radial phi^A Euler equation from F_min.
    h = r_s / (2 * r)
    A = sp.exp(2 * h)
    Y_ext = sp.exp(2 * h)
    f = sp.Function("f")(r)
    lambda_r_ext = sp.diff(f, r) ** 2 / A
    lambda_t_ext = f**2 / (A * r**2)
    F_ext = sp.simplify(
        F_solar.subs({Y: Y_ext, lambda_r: lambda_r_ext, lambda_t: lambda_t_ext})
    )
    sqrt_minus_g_over_sin = sp.simplify(r**2 * sp.exp(2 * h))
    L_radial = sp.simplify(sqrt_minus_g_over_sin * F_ext)
    E_f = sp.simplify(
        sp.diff(L_radial, f) - sp.diff(sp.diff(L_radial, sp.diff(f, r)), r)
    )
    E_f_identity = sp.factor(
        sp.simplify(
            E_f.subs(
                {
                    f: r,
                    sp.diff(f, r): 1,
                    sp.diff(f, r, 2): 0,
                }
            )
        )
    )
    E_f_identity_over_c = sp.factor(sp.simplify(E_f_identity / c_Y2))
    E_f_u_over_c = sp.factor(
        sp.simplify(E_f_identity_over_c.subs(r, r_s / u))
    )
    E_f_u_series = sp.factor(sp.series(E_f_u_over_c / r_s, u, 0, 5).removeO())

    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    Tt_ext_over_c = sp.simplify(T_w_over_c["ThetaF^t_t/M4"].subs(w, sp.exp(r_s / r)))
    metric_residual_from_fmin = sp.simplify(-8 * sp.pi * G * M4 * c_Y2 * Tt_ext_over_c)
    ratio_to_D = sp.factor(sp.simplify(metric_residual_from_fmin / D))
    ratio_u = sp.factor(sp.simplify(ratio_to_D.subs(r, r_s / u)))
    ratio_u_series = sp.factor(sp.series(ratio_u, u, 0, 3).removeO())

    nonzero_checks = {
        "Fmin_not_zero": sp.simplify(F_w_over_c) != 0,
        "Tt_not_zero": sp.simplify(T_w_over_c["ThetaF^t_t/M4"]) != 0,
        "Tr_not_zero": sp.simplify(T_w_over_c["ThetaF^r_r/M4"]) != 0,
        "Ttheta_not_zero": sp.simplify(T_w_over_c["ThetaF^theta_theta/M4"]) != 0,
        "Ef_not_zero": sp.simplify(E_f_identity_over_c) != 0,
    }
    passed = not any(nonzero_checks.values())

    return {
        "p05j_status": (
            "PASS_FMIN_VANISHES_ON_COMPACT_IDENTITY_BRANCH"
            if passed
            else "FAIL_FMIN_HAS_NONZERO_COMPACT_EXTERIOR_RESIDUAL"
        ),
        "coefficient_slice": {
            str(key): value for key, value in coeff_subs.items()
        },
        "compact_identity_branch": {
            "w": sp.Eq(w, sp.exp(r_s / r)),
            "Y": sp.Eq(sp.Symbol("Y"), w),
            "lambda_r": sp.Eq(sp.Symbol("lambda_r"), 1 / w),
            "lambda_t": sp.Eq(sp.Symbol("lambda_t"), 1 / w),
        },
        "Fmin_on_branch_over_cY2": sp.Eq(sp.Symbol("F_min/c_Y2"), F_w_over_c),
        "Fmin_at_w_equals_2_over_cY2": sp.simplify(F_w_over_c.subs(w, 2)),
        "Fmin_u_series_over_cY2": F_u_series,
        "Fmin_mixed_stress_over_M4_cY2": T_w_over_c,
        "Fmin_stress_u_series_over_M4_cY2": T_u_series,
        "Fmin_phiA_Euler_identity_over_cY2": E_f_identity_over_c,
        "Fmin_phiA_Euler_u_series_over_cY2_rs": E_f_u_series,
        "metric_residual_from_Fmin_t_component": metric_residual_from_fmin,
        "metric_residual_over_projected_D": ratio_to_D,
        "metric_residual_over_projected_D_u_series": ratio_u_series,
        "nonzero_checks": nonzero_checks,
        "verdict": (
            "On the physical Solar F_min slice, inserting the structural "
            "F_min sector again as an ordinary compact RHS source gives "
            "nonzero stress and a nonzero phi^A Euler residual.  This is the "
            "double-counting diagnostic: the compact projected deficit source "
            "already closes the geometry, while F_min is the compact "
            "structural medium sector, not an extra compact matter load."
        ),
        "next_options": [
            "use p05p as the compact no-double-count source ledger",
            "keep raw F_min explicitly marked as a rejected compact RHS insertion",
            "write the no-double-count rule as a variational projector or branch decomposition",
        ],
    }


def derive_phase_normalized_fmin_compact_gate():
    """
    Test the phase-normalized branch-action candidate.

    This is not a passive field redefinition of the raw F_min action.  A true
    metric stress tensor is not removed by renaming variables.  The calculation
    below only shows what happens if the compact branch defines the quiet
    F_min channel through local phase-normalized invariants, or equivalently
    through a compact-branch projector.

    Define normalized invariants

        Y_hat = e^(-2H) Y,
        lambda_hat_i = e^(2H) lambda_i.

    On the pure compact phase branch H=h, Y=e^(2h), lambda_i=e^(-2h), so
    Y_hat=lambda_hat_i=1.  The candidate branch channel is then quiet on the
    compact pure-phase exterior.  The raw tensor residual is tested separately
    in p05k.
    """
    r, r_s, M4 = sp.symbols("r r_s M4", positive=True, real=True)
    c_Y2 = sp.Symbol("c_Y2", real=True)
    Y, lambda_r, lambda_t, H = sp.symbols(
        "Y lambda_r lambda_t H", positive=True, real=True
    )
    coeff_symbols = _coefficient_symbols()
    _, c_Y2_coeff, _, _, _, _, _ = coeff_symbols
    F = _fmin_polynomial(Y, lambda_r, lambda_t, coeff_symbols)
    F_solar = sp.simplify(F.subs(solar_physical_fmin_coefficients(coeff_symbols)))
    F_solar = F_solar.subs(c_Y2_coeff, c_Y2)

    Y_hat = sp.exp(-2 * H) * Y
    lambda_r_hat = sp.exp(2 * H) * lambda_r
    lambda_t_hat = sp.exp(2 * H) * lambda_t
    F_hat = sp.simplify(
        F_solar.subs(
            {
                Y: Y_hat,
                lambda_r: lambda_r_hat,
                lambda_t: lambda_t_hat,
            }
        )
    )

    F_Y = sp.diff(F_hat, Y)
    F_lr = sp.diff(F_hat, lambda_r)
    F_lt = sp.diff(F_hat, lambda_t)
    T_t = sp.simplify(2 * Y * F_Y - F_hat)
    T_r = sp.simplify(2 * lambda_r * F_lr - F_hat)
    T_theta = sp.simplify(lambda_t * F_lt - F_hat)

    h = r_s / (2 * r)
    branch = {H: h, Y: sp.exp(2 * h), lambda_r: sp.exp(-2 * h), lambda_t: sp.exp(-2 * h)}
    stress_branch = {
        "ThetaFhat^t_t/M4": sp.factor(sp.simplify(T_t.subs(branch))),
        "ThetaFhat^r_r/M4": sp.factor(sp.simplify(T_r.subs(branch))),
        "ThetaFhat^theta_theta/M4": sp.factor(sp.simplify(T_theta.subs(branch))),
    }

    f = sp.Function("f")(r)
    A = sp.exp(2 * h)
    Y_ext = sp.exp(2 * h)
    H_ext = h
    lambda_r_ext = sp.diff(f, r) ** 2 / A
    lambda_t_ext = f**2 / (A * r**2)
    F_hat_ext = sp.simplify(
        F_hat.subs({H: H_ext, Y: Y_ext, lambda_r: lambda_r_ext, lambda_t: lambda_t_ext})
    )
    sqrt_minus_g_over_sin = sp.simplify(r**2 * sp.exp(2 * h))
    L_radial = sp.simplify(sqrt_minus_g_over_sin * F_hat_ext)
    E_f = sp.simplify(
        sp.diff(L_radial, f) - sp.diff(sp.diff(L_radial, sp.diff(f, r)), r)
    )
    E_f_identity = sp.factor(
        sp.simplify(
            E_f.subs({f: r, sp.diff(f, r): 1, sp.diff(f, r, 2): 0})
        )
    )
    u = sp.Symbol("u", positive=True, real=True)
    E_f_u_series = sp.factor(
        sp.series((E_f_identity / (c_Y2 * r_s)).subs(r, r_s / u), u, 0, 5).removeO()
    )

    stress_quiet = all(sp.simplify(value) == 0 for value in stress_branch.values())
    eom_quiet = sp.simplify(E_f_identity) == 0

    return {
        "phase_normalized_status": (
            "PASS_IF_FMIN_IS_DEFINED_WITH_PHASE_NORMALIZED_BRANCH_INVARIANTS"
            if stress_quiet and eom_quiet
            else "PARTIAL_PHASE_NORMALIZED_BRANCH_FMIN_STRESS_QUIET_BUT_SPATIAL_EOM_ACTIVE"
            if stress_quiet
            else "FAIL_PHASE_NORMALIZED_BRANCH_FMIN_STILL_ACTIVE"
        ),
        "normalized_invariants": {
            "Y_hat": sp.Eq(sp.Symbol("Y_hat"), Y_hat),
            "lambda_r_hat": sp.Eq(sp.Symbol("lambda_r_hat"), lambda_r_hat),
            "lambda_t_hat": sp.Eq(sp.Symbol("lambda_t_hat"), lambda_t_hat),
        },
        "Fhat_on_compact_identity": sp.simplify(F_hat.subs(branch)),
        "Fhat_stress_on_compact_identity": stress_branch,
        "Fhat_phiA_Euler_identity": E_f_identity,
        "Fhat_phiA_Euler_u_series_over_cY2_rs": E_f_u_series,
        "meaning": (
            "If the compact branch defines the quiet F_min channel with local "
            "phase-normalized invariants, both the branch F_min stress and the "
            "branch spatial Euler residual vanish on the pure-phase exterior. "
            "This is a branch-action/projector statement, not a passive "
            "normalization of the raw F_min tensor."
        ),
    }


def derive_compact_branch_fmin_screening_gate():
    """
    Compact branch source-ledger gate.

    The intuitive branch rule is:
      - weak/diffuse exterior: F_min supplies the diffuse medium response used
        by the Solar branch;
      - compact pure-phase exterior: F_min is the structural medium sector and
        the active RHS source is L_Delta^perp.

    Omega_F is kept only as an algebraic ledger marker.  It is not derived
    from exterior residual matching.  The physical statement is the p05p
    no-double-count rule: structural F_min is not added again as compact
    matter on the same geometry.
    """
    Omega_F, F_raw, E_raw = sp.symbols("Omega_F F_raw E_raw", real=True)
    compact_rule = {Omega_F: 0}
    weak_rule = {Omega_F: 1}
    compact_active_stress = sp.simplify(Omega_F * F_raw).subs(compact_rule)
    compact_active_eom = sp.simplify(Omega_F * E_raw).subs(compact_rule)
    weak_active_stress = sp.simplify(Omega_F * F_raw).subs(weak_rule)

    return {
        "screening_gate_status": (
            "PASS_IF_COMPACT_BRANCH_PROJECTOR_SETS_DIFFUSE_FMIN_WEIGHT_TO_ZERO"
            if compact_active_stress == 0 and compact_active_eom == 0
            else "CHECK_COMPACT_BRANCH_PROJECTOR"
        ),
        "branch_weight": "Omega_F",
        "weak_diffuse_branch": sp.Eq(sp.Symbol("Omega_F"), 1),
        "compact_phase_branch": sp.Eq(sp.Symbol("Omega_F"), 0),
        "compact_active_Fmin_stress": compact_active_stress,
        "compact_active_Fmin_phiA_EOM": compact_active_eom,
        "weak_active_Fmin_stress": weak_active_stress,
        "remaining_derivation": (
            "p05p supplies the source ledger: the compact active RHS is "
            "L_Delta^perp, while F_min remains structural.  The remaining "
            "formal work is to write this as an explicit variational projector "
            "or branch decomposition, not to infer Omega_F from a residual."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18j: F_min residual on compact exponential exterior")
    print("=" * 72)
    sections = [
        ("1. Raw F_min on compact identity branch", derive_fmin_compact_identity_branch_residual_gate()),
        ("2. Phase-normalized F_min", derive_phase_normalized_fmin_compact_gate()),
        ("3. Compact branch F_min screening rule", derive_compact_branch_fmin_screening_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:44s}: {value}")
