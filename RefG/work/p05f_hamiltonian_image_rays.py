# Notation header (see NOTATION.md):
# signature (+---); x=r/r_s; image-plane coordinates are in r_s units.

"""
PHASE 18f: Hamiltonian inclined ray integration

This file continues p05e_inclined_image_rays.py.  The previous gate gave the
first-order image-plane shadow boundary as a shifted circle.  This file writes
and numerically integrates the corresponding first-order Hamiltonian rays.

The metric layer is still the p05d first-order stationary ansatz, not a full
rotating RefG field-equation solution:

    ds^2/r_s^2 = -B d tau^2
                 + A(dx^2 + x^2 d theta^2 + x^2 sin^2(theta)dphi^2)
                 + 2D d tau dphi,

with B=exp(-1/x), A=exp(1/x), and D=-j sin^2(theta)/(2x).  Keeping only terms
through O(j), the null Hamiltonian used here is

    H = 1/2[-A + B p_x^2 + B p_theta^2/x^2
            + B p_phi^2/(x^2 sin^2 theta) + j p_phi/x^3].

The goal is a ray-classification gate: points inside the p05e boundary are
captured and points outside it scatter.
"""

import math

from p05e_inclined_image_rays import (
    _image_boundary_points,
    derive_inclined_image_plane_boundary_gate,
    p05e_central_inclined_image_gate,
)


def _metric_factors(x_value: float):
    return math.exp(-1.0 / x_value), math.exp(1.0 / x_value)


def _hamiltonian(state, p_phi: float, j_value: float) -> float:
    x_value, theta_value, p_x, p_theta = state
    sin_theta = math.sin(theta_value)
    B, A = _metric_factors(x_value)
    angular = p_theta**2 + p_phi**2 / (sin_theta**2)
    return 0.5 * (
        -A
        + B * p_x**2
        + B * angular / x_value**2
        + j_value * p_phi / x_value**3
    )


def _rhs(state, p_phi: float, j_value: float):
    x_value, theta_value, p_x, p_theta = state
    sin_theta = math.sin(theta_value)
    cos_theta = math.cos(theta_value)
    B, A = _metric_factors(x_value)
    angular = p_theta**2 + p_phi**2 / (sin_theta**2)

    dx = B * p_x
    dtheta = B * p_theta / x_value**2

    dA_dx = -A / x_value**2
    dB_dx = B / x_value**2
    d_h_dx = 0.5 * (
        -dA_dx
        + dB_dx * p_x**2
        + (dB_dx / x_value**2 - 2.0 * B / x_value**3) * angular
        - 3.0 * j_value * p_phi / x_value**4
    )
    dp_x = -d_h_dx

    d_h_dtheta = -B * p_phi**2 * cos_theta / (
        x_value**2 * sin_theta**3
    )
    dp_theta = -d_h_dtheta
    return [dx, dtheta, dp_x, dp_theta]


def _rk4_step(state, p_phi: float, j_value: float, step: float):
    def add_scaled(base, delta, scale):
        return [base[index] + scale * delta[index] for index in range(4)]

    k1 = _rhs(state, p_phi, j_value)
    k2 = _rhs(add_scaled(state, k1, step / 2.0), p_phi, j_value)
    k3 = _rhs(add_scaled(state, k2, step / 2.0), p_phi, j_value)
    k4 = _rhs(add_scaled(state, k3, step), p_phi, j_value)
    return [
        state[index]
        + step * (k1[index] + 2.0 * k2[index] + 2.0 * k3[index] + k4[index]) / 6.0
        for index in range(4)
    ]


def _initial_state_from_image_point(
    alpha: float,
    beta_img: float,
    inclination_deg: float,
    j_value: float,
    x_obs: float,
):
    inclination = math.radians(inclination_deg)
    theta = inclination
    sin_i = math.sin(inclination)
    p_phi = alpha * sin_i
    p_theta = beta_img
    B, A = _metric_factors(x_obs)
    angular = p_theta**2 + p_phi**2 / (sin_i**2)
    p_x_sq = (
        A
        - B * angular / x_obs**2
        - j_value * p_phi / x_obs**3
    ) / B
    if p_x_sq <= 0.0:
        raise ValueError("image point has no inward null momentum at x_obs")
    return [x_obs, theta, -math.sqrt(p_x_sq), p_theta], p_phi


def integrate_image_ray(
    alpha: float,
    beta_img: float,
    inclination_deg: float,
    j_value: float,
    x_obs: float = 80.0,
    step: float = 0.02,
    max_steps: int = 12000,
):
    """
    Integrate one ray from a distant image-plane point.

    Classification:
    * captured: x reaches the photon-edge/core side x<=1;
    * scattered: p_x turns positive outside x>1.
    """
    state, p_phi = _initial_state_from_image_point(
        alpha,
        beta_img,
        inclination_deg,
        j_value,
        x_obs,
    )
    initial_h = _hamiltonian(state, p_phi, j_value)
    min_x = state[0]
    max_h_abs = abs(initial_h)
    previous_p_x = state[2]

    classification = "open"
    steps_used = 0
    for step_index in range(max_steps):
        state = _rk4_step(state, p_phi, j_value, step)
        steps_used = step_index + 1
        x_value, theta_value, p_x, _ = state
        min_x = min(min_x, x_value)
        max_h_abs = max(max_h_abs, abs(_hamiltonian(state, p_phi, j_value)))

        if x_value <= 1.0:
            classification = "captured"
            break
        if previous_p_x < 0.0 <= p_x and x_value > 1.0 + 1.0e-4:
            classification = "scattered"
            break
        if theta_value <= 1.0e-5 or theta_value >= math.pi - 1.0e-5:
            classification = "coordinate_pole"
            break
        previous_p_x = p_x

    return {
        "classification": classification,
        "alpha": alpha,
        "beta_img": beta_img,
        "inclination_deg": inclination_deg,
        "j": j_value,
        "x_obs": x_obs,
        "steps_used": steps_used,
        "min_x": min_x,
        "final_x": state[0],
        "final_theta": state[1],
        "p_phi": p_phi,
        "initial_H_abs": abs(initial_h),
        "max_H_abs": max_h_abs,
    }


def derive_first_order_hamiltonian_gate():
    """
    Symbolic/numeric ledger for the first-order Hamiltonian used by the rays.
    """
    p05e = p05e_central_inclined_image_gate()
    boundary = derive_inclined_image_plane_boundary_gate()
    inside_radius = math.e - 0.08
    outside_radius = math.e + 0.08
    static_inside = integrate_image_ray(
        inside_radius / math.sqrt(2.0),
        inside_radius / math.sqrt(2.0),
        inclination_deg=60.0,
        j_value=0.0,
    )
    static_outside = integrate_image_ray(
        outside_radius / math.sqrt(2.0),
        outside_radius / math.sqrt(2.0),
        inclination_deg=60.0,
        j_value=0.0,
    )

    return {
        "hamiltonian_ray_status": (
            "PASS_FIRST_ORDER_HAMILTONIAN_RAY_SYSTEM"
            if p05e["p05e_status"]
            == "PASS_P05E_INCLINED_IMAGE_PLANE_FIRST_ORDER_LAYER"
            and boundary["inclined_image_boundary_status"]
            == "PASS_INCLINED_IMAGE_PLANE_FIRST_ORDER_SHADOW_BOUNDARY"
            and static_inside["classification"] == "captured"
            and static_outside["classification"] == "scattered"
            and static_inside["max_H_abs"] < 5.0e-6
            and static_outside["max_H_abs"] < 5.0e-6
            else "CHECK_FIRST_ORDER_HAMILTONIAN_RAY_SYSTEM"
        ),
        "hamiltonian": (
            "H=1/2[-A+B*p_x^2+B*p_theta^2/x^2+"
            "B*p_phi^2/(x^2*sin(theta)^2)+j*p_phi/x^3]"
        ),
        "metric_layer": (
            "B=exp(-1/x), A=exp(1/x), D=-j*sin(theta)^2/(2x), "
            "kept through O(j)"
        ),
        "static_smoke_tests": {
            "inside": static_inside,
            "outside": static_outside,
        },
        "scope": (
            "Hamiltonian ray integration in the p05d first-order stationary "
            "metric layer; this is still not a derived full rotating RefG "
            "solution and has no plasma/emission model"
        ),
        "chart_note": (
            "this spherical-coordinate integrator samples generic image rays; "
            "exact polar-axis crossings require a rotated or Cartesian chart"
        ),
    }


def run_shifted_boundary_ray_classification_gate():
    """
    Classify rays just inside and just outside the p05e shifted boundary.

    For each sample angle, the boundary center is taken from p05e.  The ray is
    launched at R=e-delta and R=e+delta around that center.  The gate passes
    when inner samples are captured and outer samples scatter.
    """
    hamiltonian = derive_first_order_hamiltonian_gate()
    inclinations = (30.0, 60.0, 90.0)
    j_values = (0.0, 0.1)
    theta_values = (
        math.pi / 6.0,
        5.0 * math.pi / 6.0,
        7.0 * math.pi / 6.0,
        11.0 * math.pi / 6.0,
    )
    delta = 0.08
    rows = []

    for j_value in j_values:
        for inclination_deg in inclinations:
            inclination = math.radians(inclination_deg)
            center_shift = -math.e * j_value * math.sin(inclination) / 2.0
            for theta_value in theta_values:
                for side, radius in (("inside", math.e - delta), ("outside", math.e + delta)):
                    alpha = center_shift + radius * math.cos(theta_value)
                    beta_img = radius * math.sin(theta_value)
                    result = integrate_image_ray(
                        alpha,
                        beta_img,
                        inclination_deg,
                        j_value,
                    )
                    result.update({
                        "side": side,
                        "theta_image": theta_value,
                        "boundary_center_shift": center_shift,
                        "radius_from_shifted_center": radius,
                    })
                    rows.append(result)

    inside_rows = [row for row in rows if row["side"] == "inside"]
    outside_rows = [row for row in rows if row["side"] == "outside"]
    inside_ok = all(row["classification"] == "captured" for row in inside_rows)
    outside_ok = all(row["classification"] == "scattered" for row in outside_rows)
    max_h_abs = max(row["max_H_abs"] for row in rows)

    p05e_points = _image_boundary_points(0.1, 90.0, samples=4)
    edge_on_boundary = {
        "alpha_max": max(point["alpha"] for point in p05e_points),
        "alpha_min": min(point["alpha"] for point in p05e_points),
    }

    return {
        "ray_classification_status": (
            "PASS_SHIFTED_BOUNDARY_HAMILTONIAN_RAY_CLASSIFICATION"
            if hamiltonian["hamiltonian_ray_status"]
            == "PASS_FIRST_ORDER_HAMILTONIAN_RAY_SYSTEM"
            and inside_ok
            and outside_ok
            and max_h_abs < 5.0e-6
            else "CHECK_SHIFTED_BOUNDARY_HAMILTONIAN_RAY_CLASSIFICATION"
        ),
        "delta_from_boundary": delta,
        "rows": rows,
        "inside_all_captured": inside_ok,
        "outside_all_scattered": outside_ok,
        "max_H_abs": max_h_abs,
        "edge_on_boundary_from_p05e": edge_on_boundary,
        "chart_note": (
            "classification uses generic image-plane angles away from the "
            "spherical-coordinate polar axis"
        ),
        "reading": (
            "direct Hamiltonian rays classify the p05e shifted circle as the "
            "first-order capture boundary: samples inside it fall through the "
            "x=1 edge, and samples outside it turn around."
        ),
    }


def p05f_central_hamiltonian_image_ray_gate():
    hamiltonian = derive_first_order_hamiltonian_gate()
    classification = run_shifted_boundary_ray_classification_gate()

    return {
        "p05f_status": (
            "PASS_P05F_HAMILTONIAN_IMAGE_RAY_LAYER"
            if hamiltonian["hamiltonian_ray_status"]
            == "PASS_FIRST_ORDER_HAMILTONIAN_RAY_SYSTEM"
            and classification["ray_classification_status"]
            == "PASS_SHIFTED_BOUNDARY_HAMILTONIAN_RAY_CLASSIFICATION"
            else "CHECK_P05F_HAMILTONIAN_IMAGE_RAY_LAYER"
        ),
        "hamiltonian_ray_system": hamiltonian["hamiltonian_ray_status"],
        "shifted_boundary_classification": classification["ray_classification_status"],
        "max_H_abs": classification["max_H_abs"],
        "next_gates": [
            "derive the rotating RefG exterior from the action/source equations",
            "add a plasma/emission model before any EHT likelihood claim",
        ],
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18f: Hamiltonian inclined image rays")
    print("=" * 72)

    sections = [
        ("1. Hamiltonian ray system", derive_first_order_hamiltonian_gate()),
        ("2. Shifted-boundary ray classification", run_shifted_boundary_ray_classification_gate()),
        ("3. Central p05f gate", p05f_central_hamiltonian_image_ray_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:42s}: {value}")
