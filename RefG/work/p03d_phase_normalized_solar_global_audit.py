# Notation header:
# signature (+---); Y = g^mn d_m Phi d_n Phi;
# lambda_r, lambda_t are the radial and repeated tangential eigenvalues of
# B^AB = -g^mn d_m phi^A d_n phi^B.

"""
p03d_phase_normalized_solar_global_audit.py

Audit forced by the compact F_min repair.

p05s closes the compact pure-phase branch by writing F_min in locally
phase-normalized variables

    Yhat=e^(-2H)Y,   lambdahat_i=e^(2H)lambda_i.

The dangerous interpretation is to lock H globally to the spatial determinant,

    H = -1/6 log(I3),   I3=lambda_r*lambda_t**2.

That is not a harmless notation change: if H is a function of I3, it varies
with the metric and changes the weak Solar stress tensor.  This file checks
the Solar branch directly at the orders used by the article.

The result distinguishes three action readings:

1. raw F_min;
2. independent-H phase-normalized F_min, with H held fixed in metric variation;
3. determinant-locked Fhat_min, where H=-1/6 log(I3) is substituted into the
   action before variation.

Only the second reading is the action-level compact repair compatible with the
weak Solar p03c branch: H is the independent pressure/energy-deficit channel.
It is unloaded through 2PN in the weak diffuse Solar branch and loaded as H=h
on the compact pure-phase branch.  The spatial determinant is tested only as a
rejected reading, because the internal spacing of the base medium is not the
observable gravitational source.
"""

from __future__ import annotations

from typing import Callable

import sympy as sp


def _physical_solar_fmin(
    Y: sp.Expr,
    lambda_r: sp.Expr,
    lambda_t: sp.Expr,
    cY2: sp.Expr,
) -> sp.Expr:
    I1 = lambda_r + 2 * lambda_t
    I2 = 2 * lambda_r * lambda_t + lambda_t**2
    I3 = lambda_r * lambda_t**2
    return sp.simplify(
        cY2
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


def _stress_series(
    action_builder: Callable[[sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol], sp.Expr],
) -> dict[str, dict[str, sp.Expr]]:
    eps = sp.Symbol("eps")
    cY2 = sp.Symbol("cY2", real=True)
    Y, lr, lt, H = sp.symbols("Y lambda_r lambda_t H", positive=True, real=True)
    y1, y2, r1, r2, t1, t2, h1, h2 = sp.symbols(
        "y1 y2 r1 r2 t1 t2 h1 h2", real=True
    )

    L = action_builder(Y, lr, lt, H, cY2)
    Tt = sp.simplify(2 * Y * sp.diff(L, Y) - L)
    Tr = sp.simplify(2 * lr * sp.diff(L, lr) - L)
    Tth = sp.simplify(lt * sp.diff(L, lt) - L)

    series_subs = {
        Y: 1 + y1 * eps + y2 * eps**2,
        lr: 1 + r1 * eps + r2 * eps**2,
        lt: 1 + t1 * eps + t2 * eps**2,
        H: h1 * eps + h2 * eps**2,
    }

    def coeff(expr: sp.Expr, order: int) -> sp.Expr:
        return sp.factor(
            sp.simplify(
                sp.series(expr.subs(series_subs), eps, 0, order + 1)
                .removeO()
                .coeff(eps, order)
            )
        )

    return {
        "T^t_t": {"O1": coeff(Tt, 1), "O2": coeff(Tt, 2)},
        "T^r_r": {"O1": coeff(Tr, 1), "O2": coeff(Tr, 2)},
        "T^theta_theta": {"O1": coeff(Tth, 1), "O2": coeff(Tth, 2)},
    }


def _raw_action(
    Y: sp.Symbol,
    lr: sp.Symbol,
    lt: sp.Symbol,
    _H: sp.Symbol,
    cY2: sp.Symbol,
) -> sp.Expr:
    return _physical_solar_fmin(Y, lr, lt, cY2)


def _independent_h_action(
    Y: sp.Symbol,
    lr: sp.Symbol,
    lt: sp.Symbol,
    H: sp.Symbol,
    cY2: sp.Symbol,
) -> sp.Expr:
    return _physical_solar_fmin(
        sp.exp(-2 * H) * Y,
        sp.exp(2 * H) * lr,
        sp.exp(2 * H) * lt,
        cY2,
    )


def _determinant_locked_action(
    Y: sp.Symbol,
    lr: sp.Symbol,
    lt: sp.Symbol,
    _H: sp.Symbol,
    cY2: sp.Symbol,
) -> sp.Expr:
    I3 = lr * lt**2
    volume = I3 ** sp.Rational(1, 3)
    return _physical_solar_fmin(
        sp.simplify(Y * volume),
        sp.simplify(lr / volume),
        sp.simplify(lt / volume),
        cY2,
    )


def _solar_series_subs() -> dict[sp.Symbol, sp.Expr]:
    r, rs = sp.symbols("r rs", positive=True)
    f = sp.Function("f")(r)
    g = sp.Function("g")(r)
    sigma = sp.Function("sigma")(r)
    y1, y2, r1, r2, t1, t2, h1, h2 = sp.symbols(
        "y1 y2 r1 r2 t1 t2 h1 h2", real=True
    )
    u1 = rs / r
    return {
        y1: u1,
        y2: (1 - g) * u1**2,
        r1: -u1,
        r2: rs**2 * (-f / r**2 + 2 * sp.diff(sigma, r) / r - 2 * sigma / r**2),
        t1: 0,
        t2: 2 * sigma * u1**2,
        h1: 0,
        h2: 0,
    }


def _determinant_locked_h_series_subs() -> dict[sp.Symbol, sp.Expr]:
    base = _solar_series_subs()
    r, rs = sp.symbols("r rs", positive=True)
    f = sp.Function("f")(r)
    sigma = sp.Function("sigma")(r)
    h1, h2 = sp.symbols("h1 h2", real=True)
    # H=-1/6 log(lambda_r lambda_t^2) on the same Solar ansatz.
    base[h1] = rs / (6 * r)
    base[h2] = -sp.Rational(1, 6) * (
        rs**2 * (-f / r**2 + 2 * sp.diff(sigma, r) / r - 2 * sigma / r**2)
        + 4 * sigma * rs**2 / r**2
        - rs**2 / (2 * r**2)
    )
    return base


def _einstein_2pn_coefficients() -> dict[str, sp.Expr]:
    r, rs, eps = sp.symbols("r rs eps", positive=True)
    f = sp.Function("f")(r)
    g = sp.Function("g")(r)
    U = eps * rs / r
    A = 1 + U + (1 + f) * U**2
    B = 1 - U + g * U**2
    Ap, Bp, Bpp = sp.diff(A, r), sp.diff(B, r), sp.diff(B, r, 2)

    Gt = -Ap / (r * A**2) + (1 / A - 1) / r**2
    Gr = Bp / (r * A * B) + (1 / A - 1) / r**2
    Gth = (
        Bpp / (2 * A * B)
        - Bp**2 / (4 * A * B**2)
        - Ap * Bp / (4 * A**2 * B)
        + Bp / (2 * r * A * B)
        - Ap / (2 * r * A**2)
    )

    def coeff(expr: sp.Expr) -> sp.Expr:
        return sp.factor(
            sp.simplify(
                sp.series(sp.expand(expr * r**2), eps, 0, 3)
                .removeO()
                .coeff(eps, 2)
            )
        )

    return {
        "T^t_t": coeff(Gt),
        "T^r_r": coeff(Gr),
        "T^theta_theta": coeff(Gth),
    }


def _solar_field_equations(
    stress: dict[str, dict[str, sp.Expr]],
    substitutions: dict[sp.Symbol, sp.Expr],
) -> dict[str, sp.Expr]:
    kappa = sp.Symbol("kappa", real=True)
    geometry = _einstein_2pn_coefficients()
    return {
        comp: sp.factor(
            sp.simplify(geometry[comp] - kappa * stress[comp]["O2"].subs(substitutions))
        )
        for comp in geometry
    }


def _exact_gr_constant_strain_solutions(equations: dict[str, sp.Expr]) -> list[dict]:
    r = sp.Symbol("r", positive=True)
    cY2 = sp.Symbol("cY2", real=True)
    f = sp.Function("f")(r)
    g = sp.Function("g")(r)
    sigma = sp.Function("sigma")(r)
    sigma0 = sp.Symbol("sigma0", real=True)
    subs = {
        f: 0,
        g: 0,
        sigma: sigma0,
        sp.diff(f, r): 0,
        sp.diff(g, r): 0,
        sp.diff(g, r, 2): 0,
        sp.diff(sigma, r): 0,
    }
    residuals = [sp.factor(sp.simplify(expr.subs(subs))) for expr in equations.values()]
    return sp.solve(residuals, [sigma0], dict=True, simplify=True)


def phase_normalized_solar_global_audit() -> dict[str, object]:
    raw = _stress_series(_raw_action)
    independent_h = _stress_series(_independent_h_action)
    determinant_locked = _stress_series(_determinant_locked_action)

    weak_subs = _solar_series_subs()
    determinant_h_subs = _determinant_locked_h_series_subs()

    raw_o1 = {comp: sp.factor(sp.simplify(rows["O1"].subs(weak_subs))) for comp, rows in raw.items()}
    independent_h_unloaded_o1 = {
        comp: sp.factor(sp.simplify(rows["O1"].subs(weak_subs)))
        for comp, rows in independent_h.items()
    }
    determinant_locked_o1 = {
        comp: sp.factor(sp.simplify(rows["O1"].subs(weak_subs)))
        for comp, rows in determinant_locked.items()
    }
    independent_h_if_forced_to_determinant_o1 = {
        comp: sp.factor(sp.simplify(rows["O1"].subs(determinant_h_subs)))
        for comp, rows in independent_h.items()
    }

    raw_eqs = _solar_field_equations(raw, weak_subs)
    independent_h_eqs = _solar_field_equations(independent_h, weak_subs)
    determinant_locked_eqs = _solar_field_equations(determinant_locked, weak_subs)

    raw_solutions = _exact_gr_constant_strain_solutions(raw_eqs)
    independent_h_solutions = _exact_gr_constant_strain_solutions(independent_h_eqs)
    determinant_locked_solutions = _exact_gr_constant_strain_solutions(determinant_locked_eqs)

    weak_o1_pass = all(value == 0 for value in raw_o1.values()) and all(
        value == 0 for value in independent_h_unloaded_o1.values()
    )
    determinant_lock_breaks_1pn = any(value != 0 for value in determinant_locked_o1.values())
    independent_h_exact_gr_pass = independent_h_solutions == [
        {sp.Symbol("sigma0", real=True): -sp.Rational(1, 2)}
    ]
    raw_exact_gr_pass = raw_solutions == [
        {sp.Symbol("sigma0", real=True): -sp.Rational(1, 2)}
    ]

    status = (
        "PASS_INDEPENDENT_H_RETAINS_SOLAR_1PN_2PN__GLOBAL_I3_LOCK_REJECTED"
        if weak_o1_pass
        and raw_exact_gr_pass
        and independent_h_exact_gr_pass
        and determinant_lock_breaks_1pn
        else "CHECK_PHASE_NORMALIZED_SOLAR_AUDIT"
    )

    return {
        "status": status,
        "weak_Solar_O1_stress": {
            "raw_Fmin": raw_o1,
            "independent_H_unloaded": independent_h_unloaded_o1,
            "determinant_locked_Fhat": determinant_locked_o1,
            "independent_H_forced_to_H_equals_minus_logI3_over_6": (
                independent_h_if_forced_to_determinant_o1
            ),
        },
        "Solar_2PN_exact_GR_constant_strain_solutions": {
            "raw_Fmin": raw_solutions,
            "independent_H_unloaded": independent_h_solutions,
            "determinant_locked_Fhat": determinant_locked_solutions,
        },
        "field_equations_2PN": {
            "raw_Fmin": raw_eqs,
            "independent_H_unloaded": independent_h_eqs,
            "determinant_locked_Fhat": determinant_locked_eqs,
        },
        "action_level_verdict": (
            "The compact repair is not a global substitution H=-log(I3)/6. "
            "That determinant lock changes the metric variation and gives a "
            "nonzero weak-Solar O(U) stress.  The consistent action reading is "
            "an independent pressure/energy-deficit H: unloaded H=0 through Solar 2PN gives "
            "the raw p03c weak branch and keeps the exact-GR strain "
            "sigma=-1/2; loaded H=h gives the compact pure-phase branch."
        ),
    }


if __name__ == "__main__":
    result = phase_normalized_solar_global_audit()
    print("=" * 72)
    print("PHASE 03d: Phase-normalized F_min Solar global audit")
    print("=" * 72)
    for key, value in result.items():
        print(f"{key}: {value}")
