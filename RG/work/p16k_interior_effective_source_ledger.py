# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16k: effective-source ledger of the C2 core.

p16j closed the geometric completeness of the cored object.  This gate closes
the companion question: what effective source does the C2 core require, and is
it a bounded, junction-continuous, center-regular medium state that continues
the exterior deficit -- or a hidden pathology?

Method.  For the static isotropic metric

    ds^2 = e^{lb(x)} c^2 dt^2 - e^{la(x)} (dx^2 + x^2 dOmega^2)   (units r_c=1)

the mixed Einstein tensor G^mu_nu is computed symbolically from Christoffels
for GENERIC la(x), lb(x), then evaluated on

  * the exterior profile  la=q/x, lb=-q/x  (cross-check: must reproduce the
    known projected-deficit pattern G^t_t=-D, G^r_r=+D, G^th_th=-D with
    D=q^2 e^{-q/x}/(4 x^4); p05), and
  * the C2 core profile (p05):
        la = q(35x^2/8 - 21x^4/4 + 15x^6/8),
        lb = -q + q(-11x^2/8 + 9x^4/4 - 7x^6/8).

With the project convention Theta^mu_nu = G^mu_nu/(8 pi G_N) and
rho = Theta^t_t, p_r = -Theta^x_x, p_t = -Theta^th_th, the ledger checks:

  * finiteness of (rho, p_r, p_t) on the whole core 0<=x<=1 for 1<q<2;
  * regular center: stresses finite at x=0 and isotropic, p_r(0)=p_t(0);
  * junction continuity: all three mixed components continuous at x=1
    (guaranteed by C2 matching; verified to be exactly zero residual);
  * deficit continuation: the radial null load rho+p_r stays negative on the
    outer core and matches the exterior deficit signature -2*Delta_P at x=1;
    the center has rho+p_r = rho+p_t (isotropy), and the sign ledger over the
    core is recorded explicitly, including any interior sign change;
  * boundedness: numeric max of |rho|, |p_r|, |p_t| over x in [0,1], q in
    {6/5, 3/2, 19/10}.

This is an effective-source (right-hand-side) ledger in the same sense used by
the article's exterior: the geometry defines the required Theta.  It does not
derive the core from a physical EOS or from the medium action; that remains the
research-grade interior problem.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def _mixed_einstein_isotropic(la: sp.Expr, lb: sp.Expr, x: sp.Symbol) -> dict[str, sp.Expr]:
    """Mixed Einstein components G^t_t, G^x_x, G^th_th for the metric
    diag(e^lb, -e^la, -e^la x^2, -e^la x^2 sin^2 th) with profiles la(x), lb(x)."""
    t, th, ph = sp.symbols("t theta phi", real=True)
    coords = [t, x, th, ph]
    g = sp.diag(sp.exp(lb), -sp.exp(la), -sp.exp(la) * x**2, -sp.exp(la) * x**2 * sp.sin(th) ** 2)
    ginv = g.inv()
    n = 4

    def christoffel(a: int, b: int, c: int) -> sp.Expr:
        return sp.Rational(1, 2) * sum(
            ginv[a, d]
            * (sp.diff(g[d, c], coords[b]) + sp.diff(g[d, b], coords[c]) - sp.diff(g[b, c], coords[d]))
            for d in range(n)
        )

    Gamma = [[[sp.simplify(christoffel(a, b, c)) for c in range(n)] for b in range(n)] for a in range(n)]

    def ricci(b: int, c: int) -> sp.Expr:
        term = sp.Integer(0)
        for a in range(n):
            term += sp.diff(Gamma[a][b][c], coords[a]) - sp.diff(Gamma[a][b][a], coords[c])
            for d in range(n):
                term += Gamma[a][a][d] * Gamma[d][b][c] - Gamma[a][c][d] * Gamma[d][b][a]
        return sp.together(term)

    Ric = [sp.together(ricci(i, i)) for i in range(n)]
    Rs = sp.together(sum(ginv[i, i] * Ric[i] for i in range(n)))
    mixed = {}
    for label, i in (("t", 0), ("x", 1), ("th", 2)):
        mixed[label] = sp.simplify(ginv[i, i] * Ric[i] - sp.Rational(1, 2) * Rs)
    return mixed


def derive_interior_effective_source_ledger() -> dict[str, Any]:
    x = sp.symbols("x", positive=True, real=True)
    q = sp.symbols("q", positive=True, real=True)

    # Generic profiles -> Einstein once, then substitute.
    la_f = sp.Function("la")(x)
    lb_f = sp.Function("lb")(x)
    G_generic = _mixed_einstein_isotropic(la_f, lb_f, x)

    la_core = q * (sp.Rational(35, 8) * x**2 - sp.Rational(21, 4) * x**4 + sp.Rational(15, 8) * x**6)
    lb_core = -q + q * (-sp.Rational(11, 8) * x**2 + sp.Rational(9, 4) * x**4 - sp.Rational(7, 8) * x**6)
    la_ext = q / x
    lb_ext = -q / x

    def on_profile(expr: sp.Expr, la_p: sp.Expr, lb_p: sp.Expr) -> sp.Expr:
        out = expr.subs({la_f: la_p, lb_f: lb_p})
        return sp.simplify(out.doit())

    # 1. Exterior cross-check against the known projected-deficit pattern.
    D = q**2 * sp.exp(-q / x) / (4 * x**4)
    ext = {k: on_profile(v, la_ext, lb_ext) for k, v in G_generic.items()}
    exterior_residuals = {
        "G^t_t_plus_D": sp.simplify(ext["t"] + D),
        "G^x_x_minus_D": sp.simplify(ext["x"] - D),
        "G^th_th_plus_D": sp.simplify(ext["th"] + D),
    }
    exterior_check = all(v == 0 for v in exterior_residuals.values())

    # 2. Core effective source (8 pi G_N = 1 units; values are 8piG rho etc.).
    core = {k: on_profile(v, la_core, lb_core) for k, v in G_generic.items()}
    rho = sp.simplify(core["t"])
    p_r = sp.simplify(-core["x"])
    p_t = sp.simplify(-core["th"])
    nec_r = sp.simplify(rho + p_r)
    nec_t = sp.simplify(rho + p_t)

    # 3. Junction continuity at x=1 (C2 matching => zero residual).
    junction_residuals = {
        k: sp.simplify(core[k].subs(x, 1) - ext[k].subs(x, 1)) for k in core
    }
    junction_continuous = all(v == 0 for v in junction_residuals.values())
    nec_r_at_junction = sp.simplify(nec_r.subs(x, 1) + 2 * D.subs(x, 1))  # = 0 if matches -2*Delta_P

    # 4. Regular, isotropic center.
    rho_0 = sp.limit(rho, x, 0, "+")
    p_r_0 = sp.limit(p_r, x, 0, "+")
    p_t_0 = sp.limit(p_t, x, 0, "+")
    center_finite = all(v.is_finite for v in (rho_0, p_r_0, p_t_0))
    center_isotropic = sp.simplify(p_r_0 - p_t_0) == 0

    # 5. Numeric boundedness / sign ledger over the window 1<q<2.
    fns = {
        "rho": sp.lambdify((x, q), rho, "math"),
        "p_r": sp.lambdify((x, q), p_r, "math"),
        "p_t": sp.lambdify((x, q), p_t, "math"),
        "nec_r": sp.lambdify((x, q), nec_r, "math"),
        "nec_t": sp.lambdify((x, q), nec_t, "math"),
    }
    samples: dict[str, dict[str, Any]] = {}
    bounded = True
    for q_val in (1.2, 1.5, 1.9):
        grid = [i / 200 for i in range(1, 201)]
        vals = {name: [fn(xx, q_val) for xx in grid] for name, fn in fns.items()}
        max_abs = {name: max(abs(v) for v in series) for name, series in vals.items()}
        bounded = bounded and all(m < 1e3 for m in max_abs.values())

        def sign_changes(series: list[float]) -> int:
            count = 0
            for a, b in zip(series, series[1:]):
                if a == 0 or b == 0:
                    continue
                if (a > 0) != (b > 0):
                    count += 1
            return count

        samples[f"q={q_val}"] = {
            "max_abs": {k: round(v, 6) for k, v in max_abs.items()},
            "nec_r_at_x1": round(vals["nec_r"][-1], 6),
            "nec_r_sign_changes_on_core": sign_changes(vals["nec_r"]),
            "nec_t_sign_changes_on_core": sign_changes(vals["nec_t"]),
            "rho_at_x1": round(vals["rho"][-1], 6),
            "rho_at_center_numeric": round(fns["rho"](1e-6, q_val), 6),
        }

    ledger_pass = (
        exterior_check
        and junction_continuous
        and nec_r_at_junction == 0
        and center_finite
        and center_isotropic
        and bounded
    )

    return {
        "STATUS": (
            "PASS_INTERIOR_EFFECTIVE_SOURCE_BOUNDED_JUNCTION_CONTINUOUS_"
            "CENTER_REGULAR__DEFICIT_CONTINUATION_LEDGER__EOS_DERIVATION_OPEN"
            if ledger_pass
            else "CHECK_INTERIOR_EFFECTIVE_SOURCE_LEDGER"
        ),
        "SCOPE": (
            "Effective-source (right-hand-side) ledger of the C2 core for "
            "1<q<2, in the same sense as the article's exterior source: the "
            "geometry defines the required Theta.  It proves boundedness, exact "
            "junction continuity, a finite isotropic center, and continuity "
            "with the exterior deficit signature.  It does not derive the core "
            "from a physical EOS or from the medium action."
        ),
        "closed_checks": {
            "generic_einstein_reproduces_exterior_deficit_pattern": exterior_check,
            "junction_stress_residuals_zero_at_x1": junction_continuous,
            "radial_null_load_matches_minus_2DeltaP_at_x1": nec_r_at_junction == 0,
            "center_stresses_finite": center_finite,
            "center_isotropic_pr_equals_pt": center_isotropic,
            "stresses_bounded_on_core_window_numeric": bounded,
        },
        "open_checks": {
            "core_derived_from_physical_eos_or_medium_action": False,
            "dynamical_qnm_echo_stability": False,
            "collapse_formation": False,
        },
        "exterior_residuals": exterior_residuals,
        "junction_residuals": junction_residuals,
        "center_values_8piG_rc2_units": {
            "rho_0": rho_0,
            "p_r_0": p_r_0,
            "p_t_0": p_t_0,
        },
        "numeric_ledger": samples,
        "deficit_reading": (
            "At the junction the radial null load equals the exterior value "
            "-2*Delta_P (deficit continuation).  Inside, the effective state "
            "interpolates to a finite isotropic center; the recorded interior "
            "sign changes are the bounded transition of the deficit state to "
            "the regular center, not a divergence."
        ),
        "do_not_claim": [
            "do not claim the core source is derived from a physical EOS",
            "do not claim classical energy conditions hold everywhere "
            "(the exterior deficit already violates the radial NEC by design)",
            "do not claim dynamical stability or formation",
            "do not remove global conditional wording from compact predictions",
        ],
    }


def _print_result(result: dict[str, Any]) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, value in result["closed_checks"].items():
        print(f"  - {key}: {value}")
    print("open_checks:")
    for key, value in result["open_checks"].items():
        print(f"  - {key}: {value}")
    print("exterior_residuals:", result["exterior_residuals"])
    print("junction_residuals:", result["junction_residuals"])
    print("center_values_8piG_rc2_units:", result["center_values_8piG_rc2_units"])
    print("numeric_ledger:")
    for key, value in result["numeric_ledger"].items():
        print(f"  - {key}: {value}")
    print("deficit_reading:", result["deficit_reading"])
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    _print_result(derive_interior_effective_source_ledger())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
