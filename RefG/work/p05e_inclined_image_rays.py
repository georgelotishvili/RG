# Notation header (see NOTATION.md):
# signature (+---); image-plane coordinates are alpha,beta_img in units of r_s.

"""
PHASE 18e: Inclined image-plane shadow boundary

This file continues p05d_rotating_rays.py.  The previous gate derived the
static shadow edge and the first-order equatorial spin split.  This file turns
that result into an image-plane boundary for a distant observer at inclination
i relative to the spin axis.

The gate is first-order in the dimensionless spin parameter j.  It is a
geometric shadow-boundary layer, not a plasma image, not an EHT fit, and not a
full rotating solution of the RefG field equations.
"""

import math

import sympy as sp

from p05d_rotating_rays import (
    derive_first_order_rotating_edge_gate,
    derive_static_exponential_ray_baseline_gate,
    p05d_central_rotating_ray_gate,
)


def derive_inclined_image_plane_boundary_gate():
    """
    First-order inclined image-plane boundary.

    Let i be the observer inclination.  The p05d equatorial edge fixes the
    horizontal displacement.  Projection onto the observer image plane gives

        Delta_alpha = -(e/2) j sin(i),

    while the first-order diameter remains 2e.  The boundary is therefore the
    shifted circle

        (alpha-Delta_alpha)^2 + beta_img^2 = e^2

    through O(j).  At i=pi/2 the right and left edges match p05d.  At i=0 the
    first-order horizontal split vanishes.
    """
    p05d = p05d_central_rotating_ray_gate()
    static_baseline = derive_static_exponential_ray_baseline_gate()
    rotating_edge = derive_first_order_rotating_edge_gate()

    theta, j, inc = sp.symbols("theta j i", real=True)
    alpha, beta_img = sp.symbols("alpha beta_img", real=True)
    beta_c = sp.E
    center_shift = sp.simplify(-beta_c * j * sp.sin(inc) / 2)
    alpha_boundary = sp.simplify(center_shift + beta_c * sp.cos(theta))
    beta_boundary = sp.simplify(beta_c * sp.sin(theta))
    circle_equation = sp.Eq(
        (alpha - center_shift) ** 2 + beta_img**2,
        beta_c**2,
    )

    right_edge = sp.simplify(alpha_boundary.subs(theta, 0))
    left_edge = sp.simplify(alpha_boundary.subs(theta, sp.pi))
    top_edge = sp.simplify(beta_boundary.subs(theta, sp.pi / 2))
    bottom_edge = sp.simplify(beta_boundary.subs(theta, -sp.pi / 2))
    horizontal_diameter = sp.simplify(right_edge - left_edge)
    vertical_diameter = sp.simplify(top_edge - bottom_edge)
    area_first_order = sp.pi * beta_c**2

    p05d_solution = rotating_edge["first_order_solution"]
    p05d_beta_plus = p05d_solution["beta_plus"]
    p05d_beta_minus = p05d_solution["beta_minus"]
    equatorial_right = sp.simplify(right_edge.subs(inc, sp.pi / 2))
    equatorial_left = sp.simplify(left_edge.subs(inc, sp.pi / 2))
    face_on_shift = sp.simplify(center_shift.subs(inc, 0))

    boundary_residual = sp.simplify(
        (
            alpha_boundary - center_shift
        ) ** 2 + beta_boundary**2 - beta_c**2
    )
    diameter_linear_change = sp.simplify(
        sp.diff(horizontal_diameter / (2 * beta_c), j)
    )

    checks = {
        "p05d_central_pass": (
            p05d["p05d_status"]
            == "PASS_P05D_STATIC_RAYS_AND_FIRST_ORDER_ROTATION_LAYER"
        ),
        "static_baseline_pass": (
            static_baseline["static_ray_baseline_status"]
            == "PASS_STATIC_EXPONENTIAL_RAY_BASELINE"
        ),
        "rotating_edge_pass": (
            rotating_edge["first_order_rotating_edge_status"]
            == "PASS_FIRST_ORDER_ROTATING_EQUATORIAL_RAY_EDGE"
        ),
        "circle_residual_zero": boundary_residual == 0,
        "horizontal_diameter_static_to_first_order": (
            sp.simplify(horizontal_diameter - 2 * beta_c) == 0
        ),
        "vertical_diameter_static_to_first_order": (
            sp.simplify(vertical_diameter - 2 * beta_c) == 0
        ),
        "linear_diameter_change_zero": diameter_linear_change == 0,
        "face_on_shift_zero": face_on_shift == 0,
        "equatorial_right_matches_p05d": (
            sp.simplify(equatorial_right - p05d_beta_plus) == 0
        ),
        "equatorial_left_matches_p05d": (
            sp.simplify(equatorial_left - p05d_beta_minus) == 0
        ),
    }

    return {
        "inclined_image_boundary_status": (
            "PASS_INCLINED_IMAGE_PLANE_FIRST_ORDER_SHADOW_BOUNDARY"
            if all(checks.values())
            else "CHECK_INCLINED_IMAGE_PLANE_FIRST_ORDER_SHADOW_BOUNDARY"
        ),
        "scope": (
            "first-order geometric image-plane boundary inherited from the "
            "p05d equatorial spin edge; not a full rotating geodesic solver, "
            "plasma image, or EHT likelihood model"
        ),
        "checks": checks,
        "image_plane_coordinates": "alpha horizontal, beta_img vertical, both in r_s units",
        "center_shift": sp.Eq(sp.Symbol("Delta_alpha"), center_shift),
        "boundary_parametric": {
            "alpha(theta)": sp.Eq(sp.Symbol("alpha(theta)"), alpha_boundary),
            "beta_img(theta)": sp.Eq(sp.Symbol("beta_img(theta)"), beta_boundary),
        },
        "boundary_implicit": circle_equation,
        "right_edge": sp.Eq(sp.Symbol("alpha_R"), right_edge),
        "left_edge": sp.Eq(sp.Symbol("alpha_L"), left_edge),
        "top_edge": sp.Eq(sp.Symbol("beta_top"), top_edge),
        "bottom_edge": sp.Eq(sp.Symbol("beta_bottom"), bottom_edge),
        "horizontal_diameter": sp.Eq(sp.Symbol("D_alpha"), horizontal_diameter),
        "vertical_diameter": sp.Eq(sp.Symbol("D_beta"), vertical_diameter),
        "area_first_order": sp.Eq(sp.Symbol("A_shadow"), area_first_order),
        "equatorial_match_to_p05d": {
            "right": sp.Eq(equatorial_right, p05d_beta_plus),
            "left": sp.Eq(equatorial_left, p05d_beta_minus),
        },
        "reading": (
            "the first-order spin effect moves the static e-radius shadow on "
            "the image plane by a projected horizontal shift.  The e-radius "
            "diameter and area are unchanged at this order."
        ),
    }


def _image_boundary_points(j_value: float, inclination_deg: float, samples: int = 16):
    inclination = math.radians(inclination_deg)
    center_shift = -math.e * j_value * math.sin(inclination) / 2.0
    points = []
    for index in range(samples):
        theta = 2.0 * math.pi * index / samples
        alpha = center_shift + math.e * math.cos(theta)
        beta_img = math.e * math.sin(theta)
        radius_residual = math.hypot(alpha - center_shift, beta_img) - math.e
        points.append({
            "theta": theta,
            "alpha": alpha,
            "beta_img": beta_img,
            "radius_residual": radius_residual,
        })
    return points


def run_inclined_image_plane_numeric_gate():
    """
    Numeric sample of the first-order image-plane boundary.

    The test samples inclinations from face-on to edge-on.  It checks that the
    sampled boundary remains an e-radius shifted circle, and that the edge-on
    j=0.1 sample matches the p05d equatorial edge values.
    """
    boundary = derive_inclined_image_plane_boundary_gate()
    inclinations = (0.0, 30.0, 60.0, 90.0)
    j_values = (0.0, 0.1)
    rows = []

    for j_value in j_values:
        for inclination_deg in inclinations:
            points = _image_boundary_points(j_value, inclination_deg)
            alpha_values = [point["alpha"] for point in points]
            beta_values = [point["beta_img"] for point in points]
            center_shift = -math.e * j_value * math.sin(math.radians(inclination_deg)) / 2.0
            rows.append({
                "j": j_value,
                "inclination_deg": inclination_deg,
                "center_shift": center_shift,
                "alpha_min": min(alpha_values),
                "alpha_max": max(alpha_values),
                "horizontal_diameter": max(alpha_values) - min(alpha_values),
                "vertical_diameter": max(beta_values) - min(beta_values),
                "max_radius_residual_abs": max(
                    abs(point["radius_residual"])
                    for point in points
                ),
            })

    edge_on = next(
        row for row in rows
        if abs(row["j"] - 0.1) < 1.0e-12
        and abs(row["inclination_deg"] - 90.0) < 1.0e-12
    )
    face_on = next(
        row for row in rows
        if abs(row["j"] - 0.1) < 1.0e-12
        and abs(row["inclination_deg"] - 0.0) < 1.0e-12
    )

    p05d_sample = derive_first_order_rotating_edge_gate()["sample_j_0p1"]
    all_diameters_ok = all(
        abs(row["horizontal_diameter"] - 2.0 * math.e) < 1.0e-12
        and abs(row["vertical_diameter"] - 2.0 * math.e) < 1.0e-12
        for row in rows
    )
    all_radii_ok = all(row["max_radius_residual_abs"] < 1.0e-12 for row in rows)
    edge_on_matches_p05d = (
        abs(edge_on["alpha_max"] - p05d_sample["beta_plus"]) < 1.0e-12
        and abs(edge_on["alpha_min"] - p05d_sample["beta_minus"]) < 1.0e-12
    )
    face_on_shift_ok = abs(face_on["center_shift"]) < 1.0e-15

    return {
        "inclined_image_numeric_status": (
            "PASS_INCLINED_IMAGE_PLANE_NUMERIC_BOUNDARY"
            if boundary["inclined_image_boundary_status"]
            == "PASS_INCLINED_IMAGE_PLANE_FIRST_ORDER_SHADOW_BOUNDARY"
            and all_diameters_ok
            and all_radii_ok
            and edge_on_matches_p05d
            and face_on_shift_ok
            else "CHECK_INCLINED_IMAGE_PLANE_NUMERIC_BOUNDARY"
        ),
        "sample_rows": rows,
        "edge_on_j_0p1_matches_p05d": edge_on_matches_p05d,
        "face_on_j_0p1_shift_zero": face_on_shift_ok,
        "reading": (
            "the sampled image-plane boundary is an e-radius circle whose "
            "center shift scales as j*sin(i), and the edge-on sample reproduces "
            "the p05d equatorial first-order split."
        ),
    }


def p05e_central_inclined_image_gate():
    boundary = derive_inclined_image_plane_boundary_gate()
    numeric = run_inclined_image_plane_numeric_gate()

    return {
        "p05e_status": (
            "PASS_P05E_INCLINED_IMAGE_PLANE_FIRST_ORDER_LAYER"
            if boundary["inclined_image_boundary_status"]
            == "PASS_INCLINED_IMAGE_PLANE_FIRST_ORDER_SHADOW_BOUNDARY"
            and numeric["inclined_image_numeric_status"]
            == "PASS_INCLINED_IMAGE_PLANE_NUMERIC_BOUNDARY"
            else "CHECK_P05E_INCLINED_IMAGE_PLANE_FIRST_ORDER_LAYER"
        ),
        "inclined_image_boundary": boundary["inclined_image_boundary_status"],
        "inclined_image_numeric": numeric["inclined_image_numeric_status"],
        "center_shift_formula": boundary["center_shift"],
        "boundary_implicit": boundary["boundary_implicit"],
        "next_gates": [
            "derive the rotating RefG exterior from the action/source equations",
            (
                "p05f_hamiltonian_image_rays.py replaces the shifted-circle "
                "boundary with first-order Hamiltonian inclined ray integration"
            ),
            "add plasma/emission model before any EHT likelihood claim",
        ],
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18e: Inclined image-plane shadow boundary")
    print("=" * 72)

    sections = [
        ("1. Inclined image-plane boundary", derive_inclined_image_plane_boundary_gate()),
        ("2. Numeric image-plane samples", run_inclined_image_plane_numeric_gate()),
        ("3. Central p05e gate", p05e_central_inclined_image_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:40s}: {value}")
