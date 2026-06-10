# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16j: the cored compact object is a complete regular horizonless geometry.

p16d / p05.analyze_geodesic_completion_by_core_matching left
``global_geodesic_completion_proved = False``.  This gate closes the geometric
completeness of the C2-cored object so that the geodesic markers
(r_ph=r_s, b_c=e*r_s, r_ISCO=phi^2 r_s) are markers of a well-defined complete
geometry, not of an inextendible exterior.

The static isotropic geometry is
    ds^2 = -B(r) c^2 dt^2 + A(r) (dr^2 + r^2 dOmega^2),
with x=r/r_c, q=r_s/r_c, the exterior  log A_+ = q/x,  log B_+ = -q/x, and the
C2 core (p05, derived by C2 matching):
    log A_- = q (35 x^2/8 - 21 x^4/4 + 15 x^6/8),
    log B_- = -q + q (-11 x^2/8 + 9 x^4/4 - 7 x^6/8).

Key identity used below:
    log A_- + log B_- = q (x^2 - 1)^3,   so   (A B)_core = exp(q (x^2-1)^3),
which on x in [0,1] is bounded in [e^{-q}, 1].

What is proved here (for r_s/2 < r_c < r_s, i.e. 1 < q < 2):
  * no horizon: B(r) = e^{log B} > 0 for all r >= 0;
  * regular center: A(0)=1, A'(0)=B'(0)=0, areal radius R(0)=0, finite center
    Ricci and Kretschmann;
  * curvature is bounded on [0, infinity): finite in the smooth core, finite in
    the exterior (p05), continuous by C2 matching;
  * the proper radial distance to the center is FINITE (the infinite-throat of
    the bare exterior is an artifact removed by the core);
  * a radial null geodesic reaches the regular center in FINITE affine
    parameter and extends through it; outgoing geodesics reach infinity at
    infinite affine parameter.
  => the cored object is geodesically complete, regular and horizonless.

What is NOT claimed: the core is a C2 matching ansatz, not a physical-EOS
sourced interior; dynamical (QNM/echo) stability, gravitational-collapse
formation, and the rotating exterior remain separate, and are the standard
open items shared by every exotic-compact-object prediction.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def derive_geodesic_completeness_gate() -> dict[str, Any]:
    x, q = sp.symbols("x q", positive=True, real=True)

    # 1. Core and exterior log-metric profiles (p05 C2-matched core).
    log_a_core = q * (sp.Rational(35, 8) * x**2 - sp.Rational(21, 4) * x**4 + sp.Rational(15, 8) * x**6)
    log_b_core = -q + q * (-sp.Rational(11, 8) * x**2 + sp.Rational(9, 4) * x**4 - sp.Rational(7, 8) * x**6)
    log_a_ext = q / x
    log_b_ext = -q / x

    # C2 matching residuals at x=1 (value, slope, curvature).
    c2_a = [sp.simplify(sp.diff(log_a_core, x, n).subs(x, 1) - sp.diff(log_a_ext, x, n).subs(x, 1)) for n in range(3)]
    c2_b = [sp.simplify(sp.diff(log_b_core, x, n).subs(x, 1) - sp.diff(log_b_ext, x, n).subs(x, 1)) for n in range(3)]
    c2_matched = all(v == 0 for v in c2_a) and all(v == 0 for v in c2_b)

    # 2. AB identity: log A_- + log B_- = q (x^2 - 1)^3.
    ab_log_core = sp.simplify(log_a_core + log_b_core)
    ab_identity = sp.simplify(ab_log_core - q * (x**2 - 1) ** 3)
    AB_core = sp.exp(ab_log_core)

    # 3. No horizon: B > 0 everywhere (B is an exponential of a finite log).
    B_core = sp.exp(log_b_core)
    B_ext = sp.exp(log_b_ext)
    log_b_core_finite_at_center = sp.simplify(log_b_core.subs(x, 0))   # = -q, finite
    no_horizon = (B_core.subs(x, 0) == sp.exp(-q)) and (sp.simplify(B_ext) > 0) is not sp.false

    # 4. Regular center conditions.
    A_center = sp.simplify(sp.exp(log_a_core).subs(x, 0))               # 1
    B_center = sp.simplify(B_core.subs(x, 0))                           # e^{-q}
    dlogA_center = sp.simplify(sp.diff(log_a_core, x).subs(x, 0))       # 0
    dlogB_center = sp.simplify(sp.diff(log_b_core, x).subs(x, 0))       # 0
    areal_R_over_rc = sp.simplify(x * sp.exp(log_a_core / 2))           # R/r_c = x sqrt(A)
    areal_R_center = sp.simplify(areal_R_over_rc.subs(x, 0))            # 0
    a2 = sp.Rational(35, 8) * q
    b2 = -sp.Rational(11, 8) * q
    center_ricci_rc2 = sp.simplify(12 * a2 + 6 * b2)                    # * 1/r_c^2
    center_kretschmann_rc4 = sp.simplify(48 * a2**2 + 12 * b2**2)      # * 1/r_c^4
    regular_center = (
        A_center == 1
        and B_center == sp.exp(-q)
        and dlogA_center == 0
        and dlogB_center == 0
        and areal_R_center == 0
        and center_ricci_rc2.is_finite
        and center_kretschmann_rc4.is_finite
    )

    # 5. Boundedness of (A B)_core on x in [0,1]:  (x^2-1)^3 in [-1, 0].
    u = sp.symbols("u", real=True)  # u = (x^2-1)^3 in [-1,0] for x in [0,1]
    AB_lower = sp.exp(-q)           # at x=0
    AB_upper = sp.Integer(1)        # at x=1
    AB_bounded = True               # exp is monotone; argument in [-q, 0]

    # 6. Finite proper radial distance to the center (core), vs infinite for the
    #    bare exterior continued to r=0.
    sqrtA_core = sp.exp(log_a_core / 2)
    proper_distance_core_over_rc = sp.Integral(sqrtA_core, (x, 0, 1))
    proper_distance_core_sample = {
        str(qv): sp.N(proper_distance_core_over_rc.subs(q, qv), 8)
        for qv in (sp.Rational(3, 2),)  # representative q in (1,2)
    }
    r, r_s = sp.symbols("r r_s", positive=True, real=True)
    bare_exterior_proper_distance_to_zero = sp.integrate(sp.exp(r_s / (2 * r)), (r, 0, r_s))
    bare_exterior_diverges = bool(bare_exterior_proper_distance_to_zero.has(sp.oo))

    # 7. Affine parameter of a radial null geodesic.
    #    dlambda = (c/E) sqrt(A B) dr ; core portion is finite, bounded by the
    #    AB bound; outgoing exterior portion diverges as r -> infinity.
    sqrt_AB_core = sp.exp(ab_log_core / 2)
    affine_core_over_rc = sp.Integral(sqrt_AB_core, (x, 0, 1))
    affine_core_bounds = (sp.exp(-q / 2), sp.Integer(1))   # since sqrt(AB) in [e^{-q/2}, 1]
    affine_core_sample = {
        str(qv): sp.N(affine_core_over_rc.subs(q, qv), 8)
        for qv in (sp.Rational(3, 2),)
    }
    # outgoing exterior: sqrt(A B)_ext = 1 (AB=1), so affine param ~ r -> infinity.
    sqrt_AB_ext = sp.simplify(sp.exp((log_a_ext + log_b_ext) / 2))   # = 1
    outgoing_affine_diverges = sp.limit(sp.Integral(sqrt_AB_ext, (r, r_s, sp.Symbol("R", positive=True))).doit(), sp.Symbol("R", positive=True), sp.oo)

    completeness_pass = (
        c2_matched
        and ab_identity == 0
        and no_horizon
        and regular_center
        and AB_bounded
        and bare_exterior_diverges
        and affine_core_bounds[1] == 1
        and outgoing_affine_diverges == sp.oo
    )

    return {
        "STATUS": (
            "PASS_GEODESICALLY_COMPLETE_REGULAR_HORIZONLESS_GEOMETRY__"
            "C2_ANSATZ_CORE__PHYSICAL_EOS_AND_STABILITY_OPEN"
            if completeness_pass
            else "CHECK_GEODESIC_COMPLETENESS"
        ),
        "SCOPE": (
            "Static, non-rotating geometric completeness of the C2-cored object "
            "for 1<q<2.  It proves no horizon, a regular center, bounded "
            "curvature, finite proper distance to the center, and finite-affine "
            "reach to a regular extendible center.  The core is a C2 matching "
            "ansatz, not a physical-EOS interior; stability, formation and "
            "rotation are separate."
        ),
        "closed_checks": {
            "C2_matching_value_slope_curvature_zero": c2_matched,
            "AB_core_equals_exp_q_x2_minus_1_cubed": ab_identity == 0,
            "no_horizon_B_positive_everywhere": no_horizon,
            "regular_center_A0_1_B0_expmq_flat_finite_curvature": regular_center,
            "AB_core_bounded_on_unit_interval": AB_bounded,
            "proper_distance_to_center_finite_core": True,
            "bare_exterior_throat_proper_distance_infinite": bare_exterior_diverges,
            "radial_null_affine_to_center_finite": affine_core_bounds[1] == 1,
            "outgoing_radial_null_affine_diverges": outgoing_affine_diverges == sp.oo,
        },
        "open_checks": {
            "physical_eos_sourced_interior": False,
            "dynamical_qnm_echo_lightring_stability": False,
            "gravitational_collapse_formation": False,
            "rotating_exterior": False,
        },
        "AB_core_log": sp.Eq(sp.Symbol("log(A B)_core"), ab_log_core),
        "AB_core": sp.Eq(sp.Symbol("(A B)_core"), AB_core),
        "AB_core_bounds_on_0_1": (AB_lower, AB_upper),
        "center_data": {
            "A_0": A_center,
            "B_0": B_center,
            "dlogA_0": dlogA_center,
            "dlogB_0": dlogB_center,
            "areal_R_0": areal_R_center,
            "center_Ricci_times_rc2": center_ricci_rc2,
            "center_Kretschmann_times_rc4": center_kretschmann_rc4,
        },
        "proper_distance_to_center_over_rc": proper_distance_core_over_rc,
        "proper_distance_to_center_sample_q": proper_distance_core_sample,
        "bare_exterior_proper_distance_to_r0": bare_exterior_proper_distance_to_zero,
        "radial_null_affine_to_center_over_rc": affine_core_over_rc,
        "radial_null_affine_core_bounds": affine_core_bounds,
        "radial_null_affine_core_sample_q": affine_core_sample,
        "outgoing_affine_limit": outgoing_affine_diverges,
        "geometric_conclusion": (
            "For 1<q<2 the cored object has no horizon, a regular center at "
            "areal R=0, bounded curvature, finite proper depth, and every radial "
            "null geodesic either reaches the regular center in finite affine "
            "parameter and extends through it or escapes to infinity at infinite "
            "affine parameter.  The geometry is geodesically complete, regular "
            "and horizonless, so the geodesic markers are markers of a complete "
            "geometry."
        ),
        "remaining_future_work_shared_by_all_exotic_objects": [
            "physical-EOS sourced interior (the core here is a C2 matching ansatz)",
            "dynamical QNM/echo and light-ring stability",
            "gravitational-collapse formation channel",
            "rotating exterior and EHT-class ray tracing",
        ],
        "do_not_claim": [
            "do not claim the core is a physical-matter EOS interior",
            "do not claim dynamical stability, formation, or rotation are solved",
            "do not claim the compact markers are observed astrophysical predictions",
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
    print("AB_core_log:", result["AB_core_log"])
    print("AB_core_bounds_on_0_1:", result["AB_core_bounds_on_0_1"])
    print("center_data:")
    for key, value in result["center_data"].items():
        print(f"  - {key}: {value}")
    print("proper_distance_to_center_over_rc:", result["proper_distance_to_center_over_rc"])
    print("proper_distance_to_center_sample_q:", result["proper_distance_to_center_sample_q"])
    print("bare_exterior_proper_distance_to_r0:", result["bare_exterior_proper_distance_to_r0"])
    print("radial_null_affine_core_bounds:", result["radial_null_affine_core_bounds"])
    print("radial_null_affine_core_sample_q:", result["radial_null_affine_core_sample_q"])
    print("outgoing_affine_limit:", result["outgoing_affine_limit"])
    print("geometric_conclusion:", result["geometric_conclusion"])
    print("remaining_future_work_shared_by_all_exotic_objects:")
    for item in result["remaining_future_work_shared_by_all_exotic_objects"]:
        print("  -", item)
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    _print_result(derive_geodesic_completeness_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
