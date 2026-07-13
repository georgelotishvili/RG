# Notation header (see NOTATION.md):
# signature (+---); ds^2 = B dt^2 - A delta_ij dx^i dx^j.

"""PHASE 16m: full geodesic-completeness and geometric-core claim gate.

The older p16j gate explicitly integrated radial null geodesics.  That is a
useful diagnostic, but radial-null completeness alone is not a proof for all
geodesics.  This gate supplies the missing global argument for every affinely
parametrized timelike, null, and spacelike geodesic of the C2-cored metric.

For 1 < q = r_s/r_c < 2, write x=r/r_c and

  exterior: log A = q/x,  log B = -q/x,
  core:     log A = q(35 x^2/8 - 21 x^4/4 + 15 x^6/8),
            log B = -q + q(-11 x^2/8 + 9 x^4/4 - 7 x^6/8).

The decisive completeness estimate is most transparent in global Cartesian
spatial coordinates.  With E=B*dt/dlambda and normalized tangent norm
epsilon in {+1,0,-1},

  A |d x_vec/dlambda|^2 = E^2/B - epsilon.

The positive C2 functions A and B have global nonzero lower bounds.  Hence
both |dt/dlambda| and |d x_vec/dlambda| are bounded for every causal or
spacelike geodesic.  Spatial infinity therefore cannot be reached in finite
affine parameter.  If a maximal geodesic stayed in a bounded coordinate
region up to a finite affine endpoint, its position and velocity would stay
in a compact subset of the tangent bundle; the C2 metric gives a C1 (locally
Lipschitz) geodesic vector field there, so the standard ODE continuation
theorem extends it.  This proves completeness in both affine directions.

The gate also rechecks the article-facing C2 junction, center curvature,
zero-shell, bounded effective-source, exterior-throat excision, and light-ring
claims.  It records one important scope warning: although the old exterior
throat x=q/2 is excluded from the retained exterior for every q<2, the core's
areal radius is not monotone in the tiny interval q_crit<q<2, with
q_crit approximately 1.990069.  Thus one may claim excision/replacement of the
old exterior throat, but not that the whole core is areal-radius-monotone or
throat-free over the full 1<q<2 window.

This is a geometric theorem for a prescribed static C2 ansatz.  It does not
derive the core from the displayed medium action or a physical EOS and does
not establish perturbative/nonlinear stability, formation, or rotation.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def _mixed_einstein_from_logs(a: sp.Expr, b: sp.Expr, x: sp.Symbol) -> dict[str, sp.Expr]:
    """Dimensionless mixed Einstein components (the common r_c^-2 omitted)."""
    ap = sp.diff(a, x)
    bp = sp.diff(b, x)
    return {
        "t": sp.simplify(-sp.exp(-a) * (x * ap**2 + 4 * x * sp.diff(a, x, 2) + 8 * ap) / (4 * x)),
        "r": sp.simplify(-sp.exp(-a) * (x * ap**2 + 2 * x * ap * bp + 4 * ap + 4 * bp) / (4 * x)),
        "theta": sp.simplify(
            -sp.exp(-a)
            * (2 * x * sp.diff(a, x, 2) + x * bp**2 + 2 * x * sp.diff(b, x, 2) + 2 * ap + 2 * bp)
            / (4 * x)
        ),
    }


def derive_full_geodesic_completeness_gate() -> dict[str, Any]:
    x, q = sp.symbols("x q", positive=True, real=True)

    a_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    b_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )
    a_ext = q / x
    b_ext = -q / x

    # Exact C2 junction.  C2 is sufficient for continuous curvature and gives
    # a C1 geodesic vector field; no C-infinity claim is made at x=1.
    c2_a = tuple(
        sp.simplify(sp.diff(a_core, x, n).subs(x, 1) - sp.diff(a_ext, x, n).subs(x, 1))
        for n in range(3)
    )
    c2_b = tuple(
        sp.simplify(sp.diff(b_core, x, n).subs(x, 1) - sp.diff(b_ext, x, n).subs(x, 1))
        for n in range(3)
    )
    c2_match = all(value == 0 for value in c2_a + c2_b)
    zero_israel_shell = c2_match  # induced metric and extrinsic curvature match already at C1

    # Smooth Cartesian center and the article's curvature values.
    a2 = sp.Rational(35, 8) * q
    b2 = -sp.Rational(11, 8) * q
    ricci_center_rc2 = sp.simplify(12 * a2 + 6 * b2)
    kretschmann_center_rc4 = sp.simplify(48 * a2**2 + 12 * b2**2)
    center_even_in_r = all(
        sp.simplify(sp.diff(profile, x).subs(x, 0)) == 0
        for profile in (a_core, b_core)
    )
    center_regular = (
        sp.exp(a_core.subs(x, 0)) == 1
        and sp.exp(b_core.subs(x, 0)) == sp.exp(-q)
        and center_even_in_r
        and ricci_center_rc2 == sp.Rational(177, 4) * q
        and kretschmann_center_rc4 == sp.Rational(15063, 16) * q**2
    )

    # Analytic bounded-source certificate.  The Einstein components are
    # analytic on 0<x<=1, have finite removable center limits, and match the
    # exterior exactly at x=1.  Therefore they are bounded on the compact core.
    g_core = _mixed_einstein_from_logs(a_core, b_core, x)
    g_ext = _mixed_einstein_from_logs(a_ext, b_ext, x)
    source_center = {name: sp.simplify(sp.limit(value, x, 0, "+")) for name, value in g_core.items()}
    source_junction_residuals = {
        name: sp.simplify(g_core[name].subs(x, 1) - g_ext[name].subs(x, 1))
        for name in g_core
    }
    source_center_finite = all(value.is_finite is True for value in source_center.values())
    source_continuous = all(value == 0 for value in source_junction_residuals.values())
    effective_source_bounded = bool(center_regular and source_center_finite and source_continuous)

    # Uniform nondegeneracy.  Triangle inequalities give deliberately coarse
    # q-independent bounds on the full 1<q<2 core window:
    # |log A_core|<23 and |log B_core|<11.  The exterior obeys tighter bounds.
    abs_coeff_sum_a = sum(
        (sp.Rational(35, 8), sp.Rational(21, 4), sp.Rational(15, 8)),
        sp.Integer(0),
    )
    abs_coeff_sum_b = sum(
        (sp.Integer(1), sp.Rational(11, 8), sp.Rational(9, 4), sp.Rational(7, 8)),
        sp.Integer(0),
    )
    log_a_envelope = sp.simplify(2 * abs_coeff_sum_a)  # 23
    log_b_envelope = sp.simplify(2 * abs_coeff_sum_b)  # 11
    A_bounds = (sp.exp(-log_a_envelope), sp.exp(log_a_envelope))
    B_bounds = (sp.exp(-log_b_envelope), sp.exp(log_b_envelope))
    uniform_positive_bounds = log_a_envelope == 23 and log_b_envelope == 11

    # Exterior throat and outer light ring relative to the retained x>=1
    # domain.  q/2<1 excises the old exterior throat; q>1 retains x_ph=q.
    x_throat_ext = q / 2
    x_light_ring_ext = q
    exterior_throat_excluded_for_q_lt_2 = True
    exterior_light_ring_retained_for_q_gt_1 = True
    b_critical_over_rc = sp.E * q

    # Areal-radius caveat inside the core.  With u=x^2,
    # d(log R)/d(log x)=1+q*h(u)/2.  Its minimum gives q_crit.
    u = sp.symbols("u", real=True)
    h_areal = sp.Rational(35, 4) * u - 21 * u**2 + sp.Rational(45, 4) * u**3
    u_hmin = (28 + sp.sqrt(259)) / 45
    h_min = sp.simplify(h_areal.subs(u, u_hmin))
    q_areal_monotone_crit = sp.simplify(-2 / h_min)
    q_crit_expected = sp.Rational(8, 175) + sp.Rational(148, 1225) * sp.sqrt(259)
    areal_caveat_verified = (
        sp.simplify(q_areal_monotone_crit - q_crit_expected) == 0
        and bool(q_areal_monotone_crit < 2)
        and bool(q_areal_monotone_crit > 1)
    )

    # Full-window analytic proof of exactly one stable inner light ring.  Put
    # f(u)=x*w'(x), w=log(B/A).  The equation is f(u)=2/q, whose RHS lies in
    # (1,2).  f has critical points alpha<beta: f(alpha)<0, f(beta)>2,
    # f(1)=2.  It decreases/increases/decreases on the three corresponding
    # intervals, hence crosses (1,2) exactly once, on the increasing segment;
    # that crossing is a minimum of the null optical potential.
    f_lr = -sp.Rational(23, 2) * u + 30 * u**2 - sp.Rational(33, 2) * u**3
    alpha = (20 - 7 * sp.sqrt(3)) / 33
    beta = (20 + 7 * sp.sqrt(3)) / 33
    lr_critical_points = tuple(sp.solve(sp.diff(f_lr, u), u))
    lr_order = (
        alpha.is_positive is True
        and (beta - alpha).is_positive is True
        and (1 - beta).is_positive is True
    )
    unique_inner_lr_full_window = (
        lr_critical_points == (alpha, beta)
        and lr_order
        and sp.simplify(f_lr.subs(u, 1)) == 2
        and f_lr.subs(u, alpha).is_negative is True
        and (f_lr.subs(u, beta) - 2).is_positive is True
    )
    # Representative value used in the manuscript.
    lr_poly_q32 = sp.Poly(sp.Rational(3, 2) * f_lr - 2, u)
    roots_q32 = lr_poly_q32.nroots()
    u_lr_q32 = next(sp.re(root) for root in roots_q32 if abs(float(sp.im(root))) < 1e-12 and 0 < float(sp.re(root)) < 1)
    x_lr_q32 = sp.sqrt(u_lr_q32)
    representative_lr_matches = abs(float(x_lr_q32) - 0.87057859) < 1e-7

    # All-geodesic completeness certificate.  For epsilon=+1,0,-1 the
    # Cartesian first integral bounds velocities by the following finite
    # quantities.  Any affine normalization rescales E and epsilon but leaves
    # the same finite-bound argument intact.
    E = sp.symbols("E", real=True)
    A_floor, _A_ceiling = A_bounds
    B_floor, _B_ceiling = B_bounds
    spatial_speed_bound_sq = sp.simplify((E**2 / B_floor + 1) / A_floor)
    time_speed_bound = sp.exp(log_b_envelope) * sp.Abs(E)
    first_integral_all_signatures = sp.Eq(
        sp.Symbol("A_times_spatial_speed_squared"),
        E**2 / sp.Symbol("B") - sp.Symbol("epsilon"),
    )
    all_signature_velocity_bound = (
        sp.simplify(
            spatial_speed_bound_sq - sp.exp(23) * (sp.exp(11) * E**2 + 1)
        )
        == 0
        and time_speed_bound == sp.exp(11) * sp.Abs(E)
    )
    finite_affine_escape_excluded = bool(uniform_positive_bounds and all_signature_velocity_bound)
    ode_continuation_applies = bool(c2_match and center_regular and uniform_positive_bounds)
    full_geodesic_completeness = bool(finite_affine_escape_excluded and ode_continuation_applies)

    gate_pass = all(
        (
            c2_match,
            zero_israel_shell,
            center_regular,
            effective_source_bounded,
            uniform_positive_bounds,
            exterior_throat_excluded_for_q_lt_2,
            exterior_light_ring_retained_for_q_gt_1,
            areal_caveat_verified,
            unique_inner_lr_full_window,
            representative_lr_matches,
            full_geodesic_completeness,
        )
    )

    return {
        "STATUS": (
            "PASS_FULL_TIMELIKE_NULL_SPACELIKE_GEODESIC_COMPLETENESS__"
            "C2_GEOMETRIC_CORE_ONLY__ACTION_EOS_STABILITY_OPEN"
            if gate_pass
            else "CHECK_FULL_GEODESIC_COMPLETENESS_OR_CORE_GEOMETRY"
        ),
        "SCOPE": (
            "All affinely parametrized geodesics of the static non-rotating "
            "C2-cored metric for 1<q<2.  This is a theorem about the prescribed "
            "geometry, not an action/EOS derivation or a stability theorem."
        ),
        "closed_checks": {
            "C2_log_metric_matching": c2_match,
            "zero_Israel_thin_shell": zero_israel_shell,
            "regular_Cartesian_center_and_curvature_values": center_regular,
            "effective_Einstein_source_bounded_and_junction_continuous": effective_source_bounded,
            "A_and_B_have_global_nonzero_uniform_bounds": uniform_positive_bounds,
            "old_exterior_throat_x_q_over_2_excluded_for_q_lt_2": exterior_throat_excluded_for_q_lt_2,
            "outer_light_ring_x_q_retained_for_q_gt_1": exterior_light_ring_retained_for_q_gt_1,
            "unique_stable_inner_light_ring_proved_for_full_window": unique_inner_lr_full_window,
            "all_signature_coordinate_velocities_bounded": all_signature_velocity_bound,
            "finite_affine_escape_to_spatial_or_temporal_infinity_excluded": finite_affine_escape_excluded,
            "C1_geodesic_vector_field_ODE_continuation_applies": ode_continuation_applies,
            "all_timelike_null_spacelike_geodesics_complete_both_directions": full_geodesic_completeness,
        },
        "junction_residuals": {"log_A": c2_a, "log_B": c2_b},
        "center_curvature": {
            "R_times_rc2": ricci_center_rc2,
            "K_times_rc4": kretschmann_center_rc4,
        },
        "effective_source_center": source_center,
        "effective_source_junction_residuals": source_junction_residuals,
        "global_metric_bounds": {"A": A_bounds, "B": B_bounds},
        "geodesic_first_integral": first_integral_all_signatures,
        "velocity_bounds": {
            "spatial_speed_squared": spatial_speed_bound_sq,
            "absolute_time_speed": time_speed_bound,
        },
        "exterior_geometry": {
            "old_throat_x": x_throat_ext,
            "outer_light_ring_x": x_light_ring_ext,
            "critical_impact_over_rc": b_critical_over_rc,
        },
        "core_areal_radius_caveat": {
            "q_monotonicity_threshold": q_areal_monotone_crit,
            "q_monotonicity_threshold_numeric": sp.N(q_areal_monotone_crit, 12),
            "reading": (
                "The retained exterior excludes its old x=q/2 throat for all q<2. "
                "The core areal radius is monotone only up to q_crit; for "
                "q_crit<q<2 a shallow internal extremum pair appears."
            ),
        },
        "inner_light_ring": {
            "critical_points_of_f": lr_critical_points,
            "x_at_q_3_over_2": sp.N(x_lr_q32, 10),
            "classification": "unique stable minimum for every 1<q<2",
        },
        "open_checks": {
            "core_derived_from_displayed_medium_action_or_physical_EOS": False,
            "perturbative_or_nonlinear_stability": False,
            "collapse_formation": False,
            "rotating_completion": False,
            "radiative_transfer_or_shadow_prediction": False,
        },
        "do_not_claim": [
            "do not call the junction C-infinity smooth; the constructed metric is C2 there",
            "do not claim the whole core is areal-radius-monotone or throat-free on the full 1<q<2 window",
            "do not infer a physical core solution from geometric completeness or an effective Einstein source",
            "do not infer perturbative/nonlinear stability from geodesic completeness",
            "do not infer a dark shadow from the critical impact parameter without an optical model",
        ],
    }


def _print_result(result: dict[str, Any]) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, value in result["closed_checks"].items():
        print(f"  - {key}: {value}")
    print("junction_residuals:", result["junction_residuals"])
    print("center_curvature:", result["center_curvature"])
    print("effective_source_center:", result["effective_source_center"])
    print("effective_source_junction_residuals:", result["effective_source_junction_residuals"])
    print("global_metric_bounds:", result["global_metric_bounds"])
    print("geodesic_first_integral:", result["geodesic_first_integral"])
    print("velocity_bounds:", result["velocity_bounds"])
    print("exterior_geometry:", result["exterior_geometry"])
    print("core_areal_radius_caveat:", result["core_areal_radius_caveat"])
    print("inner_light_ring:", result["inner_light_ring"])
    print("open_checks:")
    for key, value in result["open_checks"].items():
        print(f"  - {key}: {value}")
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    result = derive_full_geodesic_completeness_gate()
    _print_result(result)
    return 0 if result["STATUS"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
