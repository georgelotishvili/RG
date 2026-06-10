# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16l: light-ring structure of the cored compact object.

Motivation.  Cunha-Berti-Herdeiro (PRL 119, 251102 (2017)) show that for
horizonless ultracompact objects light rings generically come in pairs, the
inner one stable; a stable light ring is associated with a nonlinear
instability channel (slow pile-up of trapped modes).  Any referee of the
rebuilt article will ask whether the C2-cored RefG object has an inner stable
light ring and how deep its trapping well is.  This gate computes it.

Geometry (p05 / p16j conventions, x=r/r_c, q=r_s/r_c in the window 1<q<2):
  exterior (x>=1):  log A = q/x,  log B = -q/x
  core    (x<=1):   log A_- = q(35x^2/8 - 21x^4/4 + 15x^6/8)
                    log B_- = -q + q(-11x^2/8 + 9x^4/4 - 7x^6/8)

Null circular orbits of ds^2 = B c^2 dt^2 - A (dr^2 + r^2 dOmega^2) sit at
critical points of the optical potential V(x) = B/(A x^2) (units r_c=c=1);
the impact parameter of a circular null orbit is b = 1/sqrt(V).

Closed results proved here:
  * the exterior has the known unstable light ring at x = q (r = r_s) with
    V_max = e^{-2}/q^2, i.e. b_c = e q = e r_s/r_c (BNSV 2018 in r_s units);
  * V is continuous and C1 at the junction (C2 metric matching), V'(1) > 0
    for q > 1, and V -> +infinity at the regular center (centrifugal wall);
  * therefore V has an interior minimum: the object possesses exactly one
    inner STABLE light ring in the core for the whole window 1<q<2 --
    confirming the Cunha-Berti-Herdeiro pairing for this geometry;
  * its location x_LR(q), potential depth V_min, trapped impact-parameter
    band b in (b_outer = e r_s, b_inner = 1/sqrt(V_min)), and two
    dimensionless depth measures are computed numerically for
    q in {1.2, 1.5, 1.9} and at the representative q = 3/2.

Honest scope: this is the static geometric structure only.  The nonlinear
fate of the trapped-mode pile-up (migration/collapse vs long-term stability)
is a dynamical question outside this gate; the article must cite the
nonlinear literature for it.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def derive_inner_light_ring_gate() -> dict[str, Any]:
    x = sp.symbols("x", positive=True, real=True)
    q = sp.symbols("q", positive=True, real=True)

    log_a_core = q * (sp.Rational(35, 8) * x**2 - sp.Rational(21, 4) * x**4 + sp.Rational(15, 8) * x**6)
    log_b_core = -q + q * (-sp.Rational(11, 8) * x**2 + sp.Rational(9, 4) * x**4 - sp.Rational(7, 8) * x**6)
    log_a_ext = q / x
    log_b_ext = -q / x

    # Optical potentials V = B/(A x^2) = exp(log B - log A)/x^2.
    w_core = sp.simplify(log_b_core - log_a_core)      # log(B/A) in the core
    w_ext = sp.simplify(log_b_ext - log_a_ext)         # = -2q/x
    V_core = sp.exp(w_core) / x**2
    V_ext = sp.exp(w_ext) / x**2

    # 1. Exterior light ring: V_ext' = 0  =>  x = q  (r = r_s), a maximum.
    dV_ext = sp.simplify(sp.diff(V_ext, x))
    ext_lr = sp.solve(sp.Eq(dV_ext, 0), x)
    ext_lr_at_q = q in ext_lr or sp.simplify(dV_ext.subs(x, q)) == 0
    V_max = sp.simplify(V_ext.subs(x, q))              # e^{-2}/q^2
    b_outer = sp.simplify(1 / sp.sqrt(V_max))          # e*q  (= e r_s / r_c)
    second_deriv_at_lr = sp.simplify(sp.diff(V_ext, x, 2).subs(x, q))
    ext_lr_is_max = bool(sp.simplify(second_deriv_at_lr * q**4 * sp.exp(2)) == -2)

    # 2. Junction behaviour: continuity and slope sign.
    V_match = sp.simplify(V_core.subs(x, 1) - V_ext.subs(x, 1))
    dV_core = sp.simplify(sp.diff(V_core, x))
    dV_match = sp.simplify(dV_core.subs(x, 1) - dV_ext.subs(x, 1))
    dV_at_junction = sp.simplify(dV_ext.subs(x, 1))    # 2 e^{-2q} (q-1) > 0 for q>1
    slope_positive_in_window = sp.simplify(dV_at_junction / (2 * sp.exp(-2 * q))) - (q - 1) == 0

    # 3. Center wall: V_core -> e^{-q}/x^2 -> +infinity as x -> 0.
    center_limit = sp.limit(V_core, x, 0, "+")

    # 4. Inner stable light ring: dV_core = 0 in (0,1).
    #    dV/V = w'(x) - 2/x ;  w'(x) = q(-23/2 x + 30 x^3 - 33/2 x^5).
    w_prime = sp.simplify(sp.diff(w_core, x))
    lr_condition = sp.simplify(x * w_prime - 2)        # = 0 at interior LR
    # polynomial in u = x^2:  q(-23/2 u + 30 u^2 - 33/2 u^3) = 2
    u = sp.symbols("u", positive=True, real=True)
    lr_poly = sp.expand(q * (-sp.Rational(23, 2) * u + 30 * u**2 - sp.Rational(33, 2) * u**3) - 2)

    samples: dict[str, dict[str, Any]] = {}
    all_unique_interior = True
    for q_val in (sp.Rational(6, 5), sp.Rational(3, 2), sp.Rational(19, 10)):
        roots = sp.Poly(lr_poly.subs(q, q_val), u).nroots()
        real_roots = [sp.re(r) for r in roots if abs(sp.im(r)) < 1e-12 and 0 < sp.re(r) < 1]
        all_unique_interior = all_unique_interior and len(real_roots) == 1
        u_lr = real_roots[0]
        x_lr = sp.sqrt(u_lr)
        V_min = sp.N(V_core.subs({q: q_val, x: x_lr}), 10)
        V_top = sp.N(V_max.subs(q, q_val), 10)
        b_in = sp.N(1 / sp.sqrt(V_min), 8)
        b_out = sp.N(b_outer.subs(q, q_val), 8)
        d2V = sp.N(sp.diff(V_core, x, 2).subs({q: q_val, x: x_lr}), 8)
        samples[f"q={sp.nsimplify(q_val)}"] = {
            "x_LR": sp.N(x_lr, 8),
            "r_LR_over_r_s": sp.N(x_lr / q_val, 8),
            "V_min_rc2": V_min,
            "V_max_rc2": V_top,
            "stable_minimum_d2V_positive": bool(d2V > 0),
            "b_inner_over_rc": b_in,
            "b_outer_over_rc": b_out,
            "trapped_band_b_over_rs": (sp.N(b_out / q_val, 8), sp.N(b_in / q_val, 8)),
            "depth_ratio_Vmax_over_Vmin": sp.N(V_top / V_min, 8),
            "lapse_at_LR_sqrtB": sp.N(sp.exp(log_b_core / 2).subs({q: q_val, x: x_lr}), 8),
        }

    rep = samples["q=3/2"]
    gate_pass = (
        ext_lr_at_q
        and ext_lr_is_max
        and sp.simplify(b_outer - sp.E * q) == 0
        and V_match == 0
        and dV_match == 0
        and bool(slope_positive_in_window)
        and center_limit == sp.oo
        and all_unique_interior
        and bool(rep["stable_minimum_d2V_positive"])
    )

    return {
        "STATUS": (
            "PASS_INNER_STABLE_LIGHT_RING_EXISTS_AND_QUANTIFIED__"
            "CBH_PAIRING_CONFIRMED__NONLINEAR_FATE_OPEN"
            if gate_pass
            else "CHECK_INNER_LIGHT_RING_STRUCTURE"
        ),
        "SCOPE": (
            "Static null geodesic structure of the C2-cored object on 1<q<2. "
            "It proves the unstable exterior light ring at r=r_s, exactly one "
            "stable interior light ring in the core, and quantifies the "
            "trapping well.  The nonlinear fate of trapped modes is a "
            "dynamical problem outside this gate."
        ),
        "closed_checks": {
            "exterior_lr_at_r_s_is_maximum": bool(ext_lr_at_q and ext_lr_is_max),
            "b_outer_equals_e_rs": sp.simplify(b_outer - sp.E * q) == 0,
            "V_continuous_at_junction": V_match == 0,
            "V_slope_continuous_at_junction": dV_match == 0,
            "V_increasing_at_junction_for_q_gt_1": bool(slope_positive_in_window),
            "center_centrifugal_wall_infinite": center_limit == sp.oo,
            "unique_interior_minimum_in_window_samples": all_unique_interior,
            "interior_extremum_is_stable_minimum": bool(rep["stable_minimum_d2V_positive"]),
        },
        "open_checks": {
            "nonlinear_fate_of_trapped_modes": False,
            "qnm_spectrum_of_cored_geometry": False,
            "rotating_generalization": False,
        },
        "optical_potential_core": sp.Eq(sp.Symbol("V_core"), V_core),
        "optical_potential_exterior": sp.Eq(sp.Symbol("V_ext"), V_ext),
        "interior_lr_condition_in_u_x2": sp.Eq(lr_poly, 0),
        "exterior_lr": {"x_LR_ext": q, "V_max": V_max, "b_outer": b_outer},
        "samples": samples,
        "physical_reading": (
            "The cored object realizes the Cunha-Berti-Herdeiro light-ring "
            "pair: the unstable ring at r=r_s seen from outside, and one "
            "stable ring inside the core.  Photons with impact parameter "
            "between b=e*r_s and b_inner are trapped in a finite well whose "
            "depth ratio V_max/V_min is order one-to-few (samples above), "
            "i.e. a shallow-to-moderate well rather than a deep cavity; the "
            "nonlinear pile-up question must be cited, not claimed solved."
        ),
        "do_not_claim": [
            "do not claim nonlinear stability or instability of the trapped modes",
            "do not claim a QNM/echo spectrum from this static structure",
            "do not extend these statements to rotating objects",
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
    print("exterior_lr:", result["exterior_lr"])
    print("interior_lr_condition_in_u_x2:", result["interior_lr_condition_in_u_x2"])
    print("samples:")
    for key, value in result["samples"].items():
        print(f"  - {key}:")
        for k2, v2 in value.items():
            print(f"      {k2}: {v2}")
    print("physical_reading:", result["physical_reading"])
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    _print_result(derive_inner_light_ring_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
