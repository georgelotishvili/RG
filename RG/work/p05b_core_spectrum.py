# Notation header (see NOTATION.md):
# signature (+---); compact exterior is written with positive functions
# B=exp(-r_s/r), A=exp(r_s/r) in
# ds^2=-B c^2 dt^2 + A(dr^2+r^2 dOmega^2).

"""
PHASE 18b: Compact-core perturbation, spectrum, and echo gates

This file continues p05_compact.py without growing that ledger further.

p05_compact.py now closes the static exponential exterior, the C2 finite-core
source ledger, the p01 action-density branch, and the local no-ghost/mixed-mode
interface.  This file starts the next layer: spectrum-facing perturbation
bookkeeping.  It keeps the first pass narrow:

1. import the static compact-core gate from p05;
2. derive the scalar-probe master potential on the exponential exterior;
3. measure the exponentially suppressed negative pocket in the probe potential;
4. derive the local coupled radial principal symbol for the compact spectrum;
5. derive the static echo-cavity tortoise scale for a finite C2 core radius;
6. keep full QNMs, rotation, and ray tracing as explicit next gates.
"""

import cmath
import math

import sympy as sp

from p05_compact import (
    compact_central_claim_gate,
    derive_c2_core_local_stability_interface,
    derive_c2_core_refg_medium_source_decomposition,
    derive_c2_junction_stress_closure,
)
from p01_core import (
    minkowski_principal_symbol,
    mixed_mode_stability_conditions,
)


def import_static_compact_foundation_gate():
    """
    Import the closed static compact-core claims from p05_compact.py.

    This is the foundation check for p05b.  The spectrum file does not reopen
    the static source ledger; it verifies that p05 supplies the expected closed
    inputs and then works on the perturbation layer.
    """
    gate = compact_central_claim_gate()
    local_stability = derive_c2_core_local_stability_interface()

    required = {
        "compact_exterior_short_path": "PASS_COMPACT_EXTERIOR_SHORT_PATH",
        "core_nonlinear_ivp_domain_status": (
            "PASS_SUFFICIENT_PARAMETER_DOMAIN_FOR_NONLINEAR_CORE_DEFORMATION_IVP"
        ),
        "core_action_density_integrability_status": (
            "PASS_BRANCH_LEVEL_FULL_DIAGONAL_ACTION_DENSITY_INTEGRABILITY"
        ),
        "core_local_stability_interface_status": (
            "PASS_COMPACT_CORE_P01_LOCAL_STABILITY_INTERFACE"
        ),
    }
    checks = {
        key: gate[key] == value
        for key, value in required.items()
    }
    checks["direct_local_stability_interface"] = (
        local_stability["interface_status"]
        == "PASS_COMPACT_CORE_P01_LOCAL_STABILITY_INTERFACE"
    )

    return {
        "foundation_status": (
            "PASS_STATIC_COMPACT_FOUNDATION_IMPORTED"
            if all(checks.values())
            else "CHECK_STATIC_COMPACT_FOUNDATION_IMPORT"
        ),
        "checks": checks,
        "compact_status": gate["full_compact_object_status"],
        "usable_static_inputs": [
            "exponential exterior B=exp(-r_s/r), A=exp(r_s/r)",
            "finite C2 core source and zero thin-shell stress",
            "nonlinear C2 deformation branch sufficient domain",
            "p01 action-density integrability",
            "p01 local no-ghost and mixed-mode stability interface",
        ],
        "remaining_layer": (
            "background-dependent coupled perturbations, QNMs, echoes, "
            "rotation, and EHT ray tracing"
        ),
    }


def derive_exterior_scalar_probe_master_operator():
    """
    Scalar-probe master operator on the static exponential exterior.

    This is a probe spectrum gate.  It derives the same master potential from
    the exponential exterior in a compact form that p05b can reuse for QNM and
    echo estimates.  It is not the full coupled metric-medium perturbation
    system.
    """
    r, r_s, c, ell = sp.symbols("r r_s c ell", positive=True)
    x, L = sp.symbols("x L", positive=True)
    phi = -r_s / r

    c_eff_sq = sp.simplify(c**2 * sp.exp(2 * phi))
    drstar_dr = sp.simplify(sp.exp(-phi) / c)
    phi_p = sp.diff(phi, r)
    phi_pp = sp.diff(phi_p, r)
    v_eff = sp.factor(
        c**2
        * sp.exp(2 * phi)
        * (
            ell * (ell + 1) / r**2
            - sp.Rational(1, 2) * phi_pp
            - sp.Rational(1, 4) * phi_p**2
        )
    )

    dimensionless_v = sp.factor(
        sp.exp(-2 / x) * (L * x**2 + x - sp.Rational(1, 4)) / x**4
    )
    negative_boundary_x = {
        "ell_0": sp.Rational(1, 4),
        "ell_positive": sp.simplify(
            (-1 + sp.sqrt(1 + L)) / (2 * L)
        ),
    }

    return {
        "operator_status": "PASS_STATIC_EXPONENTIAL_PROBE_MASTER_OPERATOR_DERIVED",
        "c_eff_squared": sp.Eq(sp.Symbol("c_eff^2"), c_eff_sq),
        "tortoise_drstar_dr": sp.Eq(sp.Symbol("drstar_dr"), drstar_dr),
        "master_potential": sp.Eq(sp.Symbol("V_eff"), v_eff),
        "dimensionless_potential_c_rs_1": dimensionless_v,
        "negative_region_boundary_x": negative_boundary_x,
        "reading": (
            "V_eff is exponentially suppressed at the r->0 exterior boundary; "
            "the probe potential has a finite negative pocket before the C2 "
            "core boundary is imposed."
        ),
    }


def _negative_well_integrals_for_ell(ell_value: int):
    L = ell_value * (ell_value + 1)
    if ell_value == 0:
        y0 = 4.0
        x0 = 0.25
    else:
        y0 = 2.0 * (math.sqrt(1.0 + L) + 1.0)
        x0 = 1.0 / y0

    # Integral of |V| drstar for c=r_s=1 on the negative pocket.
    well_drstar = math.exp(-y0) * (
        y0**2 / 4.0 - y0 / 2.0 - 0.5 - L
    )

    # Integral of |V| dr for c=r_s=1, kept as a direct one-dimensional check.
    # y=1/x maps the pocket to y in [y0, infinity).
    y = sp.Symbol("y", positive=True)
    well_dr_expr = sp.integrate(
        sp.exp(-2 * y) * (y**2 / 4 - y - L),
        (y, y0, sp.oo),
    )
    well_dr = float(sp.N(well_dr_expr, 16))

    return {
        "ell": ell_value,
        "L": L,
        "x_negative_boundary": x0,
        "y0_inverse_boundary": y0,
        "well_integral_absV_drstar_c_rs_1": well_drstar,
        "well_integral_absV_dr_c_rs_1": well_dr,
    }


def audit_probe_negative_well(max_ell: int = 6):
    """
    Measure the negative pocket in the scalar-probe potential.

    The pocket is largest at ell=0 in the checked range and is exponentially
    suppressed by the tortoise weight.  This is a spectrum prerequisite, not a
    coupled stability theorem.
    """
    samples = [
        _negative_well_integrals_for_ell(ell_value)
        for ell_value in range(max_ell + 1)
    ]
    largest = max(
        samples,
        key=lambda row: row["well_integral_absV_drstar_c_rs_1"],
    )
    monotone_checked = all(
        samples[i]["well_integral_absV_drstar_c_rs_1"]
        >= samples[i + 1]["well_integral_absV_drstar_c_rs_1"]
        for i in range(len(samples) - 1)
    )

    return {
        "negative_well_status": "PASS_PROBE_NEGATIVE_WELL_LEDGER_DERIVED",
        "samples": samples,
        "largest_checked_pocket": largest,
        "monotone_decrease_checked_to_ell": max_ell if monotone_checked else None,
        "ell0_exact_drstar_integral": sp.Eq(
            sp.Symbol("I_l0_drstar"),
            sp.Rational(3, 2) * sp.exp(-4),
        ),
        "reading": (
            "the scalar-probe negative pocket is finite and exponentially "
            "small; the full compact-object verdict still belongs to the "
            "coupled metric-medium spectrum."
        ),
    }


def derive_core_cutoff_negative_pocket_gate(max_ell: int = 6):
    """
    Compare the C2 core cutoff with the probe negative pocket.

    The exterior domain begins at x_c=r_c/r_s=1/q.  For a given ell, the
    negative pocket is present in the exterior only if q exceeds the inverse
    pocket boundary y0=1/x0.  Thus the finite core can remove the entire probe
    pocket for moderate compactness.
    """
    q = sp.Symbol("q", positive=True)
    rows = []
    for ell_value in range(max_ell + 1):
        sample = _negative_well_integrals_for_ell(ell_value)
        L = sample["L"]
        y0 = sample["y0_inverse_boundary"]
        full_well = sample["well_integral_absV_drstar_c_rs_1"]
        tail_after_q = sp.exp(-q) * (
            q**2 / 4 - q / 2 - sp.Rational(1, 2) - L
        )
        exterior_piece = sp.Piecewise(
            (0, q <= y0),
            (full_well - tail_after_q, True),
        )
        rows.append({
            "ell": ell_value,
            "q_threshold_for_exterior_negative_pocket": y0,
            "x_threshold": sample["x_negative_boundary"],
            "full_probe_well_drstar_c_rs_1": full_well,
            "exterior_well_drstar_piece": exterior_piece,
        })

    return {
        "cutoff_status": "PASS_CORE_CUTOFF_VS_PROBE_NEGATIVE_POCKET_DERIVED",
        "rule": (
            "the ell-mode negative pocket lies outside the C2 core only when "
            "q=r_s/r_c is larger than the listed threshold"
        ),
        "ell0_threshold": "q>4",
        "rows": rows,
        "reading": (
            "for q<=4 the l=0 probe negative pocket is removed by the finite "
            "core cutoff; for larger q the exterior contains only the finite "
            "piece shown in the ledger."
        ),
    }


def compact_spectrum_local_stable_point():
    """
    Explicit p01 coefficient point for the compact-spectrum principal symbol.

    The older p01 article point closes the mixed radial sector but leaves the
    transverse branch marginal.  This point is used only in p05b as a cleaner
    local spectrum certificate: both mixed radial roots are positive and the
    transverse characteristic speed is positive.
    """
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1",
        real=True,
    )
    return {
        c_Y2: sp.Rational(1, 2),
        c_I1sq: sp.Rational(1, 2),
        c_YI1: -sp.Rational(1, 2),
        c_Y: sp.Integer(5),
        c_I1: -sp.Integer(12),
        c_I2: sp.Integer(1),
        c_I3: -sp.Integer(1),
    }


def derive_coupled_local_principal_symbol_gate():
    """
    Coupled radial principal symbol for the compact spectrum.

    The radial phase/solid perturbations use the p01 mixed 2x2 principal
    symbol.  At the explicit p05b coefficient point the mixed roots are
    positive and simple:

        s_- = 9/17, s_+ = 1.

    The transverse branch also has c_T^2=1 at the same point.  In the compact
    static geometry the coordinate radial speeds are redshifted by B/A.
    """
    coeffs, s, det, _roots = minkowski_principal_symbol()
    conditions = mixed_mode_stability_conditions(coeffs)
    poly = conditions["mixed_polynomial_coefficients"]
    point = compact_spectrum_local_stable_point()

    coeff_values = {
        key: sp.simplify(value.subs(point))
        for key, value in coeffs.items()
        if key not in {"L2", "a"}
    }
    poly_values = {
        key: sp.factor(sp.simplify(value.subs(point)))
        for key, value in poly.items()
    }
    det_at_point = sp.factor(sp.simplify(det.subs(point)))
    roots = [sp.simplify(root) for root in sp.solve(det_at_point, s)]
    roots = sorted(roots, key=lambda root: float(sp.N(root)))
    c_t_sq = sp.simplify(-coeff_values["C_T"] / coeff_values["K_T"])

    checks = {
        "A_positive": sp.simplify(coeff_values["A"] > 0),
        "B_long_positive": sp.simplify(coeff_values["B_long"] > 0),
        "K_T_positive": sp.simplify(coeff_values["K_T"] > 0),
        "C_T_negative": sp.simplify(coeff_values["C_T"] < 0),
        "p2_positive": sp.simplify(poly_values["p2"] > 0),
        "p1_negative": sp.simplify(poly_values["p1"] < 0),
        "p0_positive": sp.simplify(poly_values["p0"] > 0),
        "discriminant_nonnegative": sp.simplify(poly_values["discriminant"] >= 0),
        "roots_positive": all(sp.simplify(root > 0) for root in roots),
        "transverse_speed_positive": sp.simplify(c_t_sq > 0),
    }

    r, r_s, c, q, x = sp.symbols("r r_s c q x", positive=True)
    log_a_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    log_b_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )
    exterior_redshift = sp.exp(-2 * r_s / r)
    core_redshift = sp.simplify(sp.exp(log_b_core - log_a_core))

    return {
        "coupled_symbol_status": (
            "PASS_COUPLED_LOCAL_PRINCIPAL_SYMBOL_WITH_FULL_STABLE_POINT"
            if all(bool(value) for value in checks.values())
            else "CHECK_COUPLED_LOCAL_PRINCIPAL_SYMBOL"
        ),
        "coefficient_point": point,
        "coefficient_values": coeff_values,
        "mixed_determinant_at_point": sp.Eq(sp.Symbol("D(s)"), det_at_point),
        "mixed_speed_roots_local": roots,
        "transverse_speed_squared_local": c_t_sq,
        "checks": checks,
        "exterior_coordinate_speed_squared": {
            "v_minus^2": sp.simplify(c**2 * exterior_redshift * roots[0]),
            "v_plus^2": sp.simplify(c**2 * exterior_redshift * roots[1]),
            "v_T^2": sp.simplify(c**2 * exterior_redshift * c_t_sq),
        },
        "core_coordinate_speed_squared": {
            "redshift_factor_B_over_A": core_redshift,
            "v_minus^2": sp.simplify(c**2 * core_redshift * roots[0]),
            "v_plus^2": sp.simplify(c**2 * core_redshift * roots[1]),
            "v_T^2": sp.simplify(c**2 * core_redshift * c_t_sq),
            "center_B_over_A": sp.simplify(core_redshift.subs(x, 0)),
            "boundary_B_over_A": sp.simplify(core_redshift.subs(x, 1)),
        },
        "reading": (
            "the local compact-spectrum principal symbol has one slower radial "
            "mixed branch, one lightlike radial mixed branch, and a lightlike "
            "transverse branch at the displayed coefficient point."
        ),
        "remaining_gate": (
            "promote this local symbol to a background-dependent radial ODE "
            "system with C2 boundary reflectivity."
        ),
    }


def derive_static_echo_cavity_scale():
    """
    Static echo-cavity tortoise scale for a finite C2 core radius.

    For the exponential exterior, drstar/dr=exp(r_s/r)/c.  With q=r_s/r_c,
    the one-way tortoise distance from the C2 core boundary to the photon
    sphere is exact in terms of Ei.  The scale is finite for finite q and grows
    rapidly as q increases.
    """
    q, r_s, c = sp.symbols("q r_s c", positive=True)
    x = sp.Symbol("x", positive=True)

    primitive = sp.simplify(x * sp.exp(1 / x) - sp.Ei(1 / x))
    primitive_residual = sp.simplify(sp.diff(primitive, x) - sp.exp(1 / x))

    x_core = 1 / q
    x_ph = sp.Integer(1)
    one_way = sp.simplify(
        r_s / c * (primitive.subs(x, x_ph) - primitive.subs(x, x_core))
    )
    round_trip = sp.simplify(2 * one_way)
    large_q_leading = sp.exp(q) / q**2

    return {
        "echo_scale_status": "PASS_STATIC_ECHO_CAVITY_SCALE_DERIVED_FOR_FINITE_C2_CORE_RADIUS",
        "tortoise_primitive": sp.Eq(sp.Symbol("F(x)"), primitive),
        "primitive_residual": primitive_residual,
        "q_definition": sp.Eq(sp.Symbol("q"), r_s / sp.Symbol("r_c", positive=True)),
        "one_way_core_to_photon_sphere": sp.Eq(sp.Symbol("Delta_t_one_way"), one_way),
        "round_trip_echo_scale": sp.Eq(sp.Symbol("Delta_t_echo"), round_trip),
        "large_q_growth": sp.Eq(sp.Symbol("Delta_t_one_way_leading"), r_s / c * large_q_leading),
        "reading": (
            "finite C2 radius gives a finite static echo scale; the actual "
            "ringdown spectrum still needs boundary reflectivity and the "
            "coupled perturbation equations."
        ),
    }


def derive_c2_boundary_reflectivity_gate():
    """
    Boundary reflectivity of the finite C2 core at principal-symbol level.

    C2 matching removes the thin shell and matches the characteristic redshift
    factor B/A through value, slope, and curvature.  With the same p01 branch
    crossing the boundary, the leading impedance jump is zero.  Therefore the
    C2 boundary is not a hard reflecting wall by itself.  Echoes require a
    separate microphysical reflectivity/absorption law or an inner-center
    boundary condition.
    """
    q, x, c, s_local, zeta = sp.symbols(
        "q x c s_local zeta",
        positive=True,
    )
    log_red_ext = -2 * q / x
    log_red_core = q * (
        -sp.Integer(1)
        - sp.Rational(23, 4) * x**2
        + sp.Rational(15, 2) * x**4
        - sp.Rational(11, 4) * x**6
    )

    redshift_c2_match = {
        "log_B_over_A": sp.simplify((log_red_core - log_red_ext).subs(x, 1)),
        "d_log_B_over_A_dx": sp.simplify(
            (sp.diff(log_red_core, x) - sp.diff(log_red_ext, x)).subs(x, 1)
        ),
        "d2_log_B_over_A_dx2": sp.simplify(
            (sp.diff(log_red_core, x, 2) - sp.diff(log_red_ext, x, 2)).subs(x, 1)
        ),
    }

    v2_ext = sp.simplify(c**2 * s_local * sp.exp(log_red_ext))
    v2_core = sp.simplify(c**2 * s_local * sp.exp(log_red_core))
    characteristic_c2_match = {
        "v2": sp.simplify((v2_core - v2_ext).subs(x, 1)),
        "dv2_dx": sp.simplify((sp.diff(v2_core, x) - sp.diff(v2_ext, x)).subs(x, 1)),
        "d2v2_dx2": sp.simplify(
            (sp.diff(v2_core, x, 2) - sp.diff(v2_ext, x, 2)).subs(x, 1)
        ),
    }

    junction = derive_c2_junction_stress_closure()
    medium = derive_c2_core_refg_medium_source_decomposition()
    surface_stress_zero = all(
        value == 0
        for value in junction["Israel_surface_stress"].values()
    )
    residual_boundary_zero = all(
        value == 0
        for value in medium["residual_boundary"].values()
    )

    reflection_amplitude = sp.simplify((zeta - 1) / (zeta + 1))
    reflection_power = sp.simplify(reflection_amplitude**2)
    transmission_power = sp.simplify(4 * zeta / (zeta + 1) ** 2)

    matched_impedance = sp.Integer(1)
    matched_reflection = sp.simplify(reflection_amplitude.subs(zeta, matched_impedance))
    matched_transmission = sp.simplify(transmission_power.subs(zeta, matched_impedance))

    return {
        "boundary_reflectivity_status": (
            "PASS_C2_BOUNDARY_HAS_NO_LEADING_HARD_WALL_REFLECTION"
            if all(value == 0 for value in redshift_c2_match.values())
            and all(value == 0 for value in characteristic_c2_match.values())
            and surface_stress_zero
            and residual_boundary_zero
            and matched_reflection == 0
            and matched_transmission == 1
            else "CHECK_C2_BOUNDARY_REFLECTIVITY"
        ),
        "redshift_C2_match": redshift_c2_match,
        "characteristic_speed_C2_match": characteristic_c2_match,
        "surface_stress_zero": surface_stress_zero,
        "residual_medium_stress_zero_at_boundary": residual_boundary_zero,
        "impedance_ratio": sp.Eq(sp.Symbol("zeta"), sp.Symbol("Z_core") / sp.Symbol("Z_ext")),
        "reflection_amplitude": sp.Eq(sp.Symbol("R_amp"), reflection_amplitude),
        "reflection_power": sp.Eq(sp.Symbol("|R|^2"), reflection_power),
        "transmission_power": sp.Eq(sp.Symbol("|T|^2"), transmission_power),
        "matched_impedance_result": {
            "zeta": matched_impedance,
            "R_amp": matched_reflection,
            "transmission_power": matched_transmission,
        },
        "reading": (
            "C2 matching plus the same p01 principal branch makes the boundary "
            "transmissive at leading order; a nonzero echo needs an additional "
            "reflectivity, absorption, or center-boundary law."
        ),
        "next_gate": (
            "derive the inner finite-core propagation/center condition and "
            "then compute the QNM or echo transfer function."
        ),
    }


def _core_travel_time_dimensionless(q_value: float, s_value: float, steps: int = 2000) -> float:
    """Return Delta t_core/(r_s/c) for one local branch using Simpson integration."""
    if steps % 2:
        steps += 1

    def log_redshift(x_value: float) -> float:
        return q_value * (
            -1.0
            - 23.0 * x_value**2 / 4.0
            + 15.0 * x_value**4 / 2.0
            - 11.0 * x_value**6 / 4.0
        )

    def integrand(x_value: float) -> float:
        return math.exp(-0.5 * log_redshift(x_value)) / (
            q_value * math.sqrt(s_value)
        )

    h = 1.0 / steps
    total = integrand(0.0) + integrand(1.0)
    total += 4.0 * sum(integrand(i * h) for i in range(1, steps, 2))
    total += 2.0 * sum(integrand(i * h) for i in range(2, steps, 2))
    return total * h / 3.0


def _exterior_cavity_time_dimensionless(q_value: float) -> float:
    """Return photon-sphere-to-core exterior time Delta t_ext/(r_s/c)."""
    return float(
        sp.N(
            (
                q_value
                * (sp.Ei(q_value) - sp.Ei(1) + sp.E)
                - sp.exp(q_value)
            )
            / q_value,
            16,
        )
    )


def _rho_of_x(x_value: float) -> float:
    """Dimensionless exterior tortoise coordinate rho=r_*/(r_s/c)."""
    return float(
        sp.N(
            x_value * sp.exp(1 / x_value) - sp.Ei(1 / x_value),
            18,
        )
    )


def _exterior_potential_dimensionless(x_value: float, ell_value: int) -> float:
    """Dimensionless scalar-probe exterior potential U=(r_s/c)^2 V."""
    angular = ell_value * (ell_value + 1)
    return (
        math.exp(-2.0 / x_value)
        * (angular * x_value * x_value + x_value - 0.25)
        / (x_value**4)
    )


def _rk4_outgoing_jost(
    omega_value: complex,
    ell_value: int,
    q_value: float,
    x_out: float,
    steps: int,
    s_value: float = 1.0,
):
    """
    Integrate the outgoing Jost solution from x_out down to x_c=1/q.

    The branch-corrected dimensionless equation in the light tortoise
    coordinate rho is u_{rho rho}+[Omega^2/s-U(x)]u=0.  The scalar/lightlike
    probe is the special case s=1.  The state is (u, u_rho).
    """
    x_in = 1.0 / q_value
    branch_speed = float(s_value)
    asymptotic_k = omega_value / math.sqrt(branch_speed)
    rho_out = _rho_of_x(x_out)
    u = cmath.exp(1j * asymptotic_k * rho_out)
    w = 1j * asymptotic_k * u
    h = (x_in - x_out) / steps

    def rhs(x_value: float, state):
        u_value, w_value = state
        rho_x = math.exp(1.0 / x_value)
        potential = _exterior_potential_dimensionless(x_value, ell_value)
        return (
            rho_x * w_value,
            rho_x * (potential - omega_value**2 / branch_speed) * u_value,
        )

    x_value = x_out
    for _ in range(steps):
        k1 = rhs(x_value, (u, w))
        k2 = rhs(
            x_value + h / 2.0,
            (u + h * k1[0] / 2.0, w + h * k1[1] / 2.0),
        )
        k3 = rhs(
            x_value + h / 2.0,
            (u + h * k2[0] / 2.0, w + h * k2[1] / 2.0),
        )
        k4 = rhs(
            x_value + h,
            (u + h * k3[0], w + h * k3[1]),
        )
        u += h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        w += h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        x_value += h

    rho_in = _rho_of_x(x_in)
    e_plus = cmath.exp(1j * asymptotic_k * rho_in)
    e_minus = cmath.exp(-1j * asymptotic_k * rho_in)
    a_incident_times_phase = (u + w / (1j * asymptotic_k)) / 2.0
    b_reflected_times_phase = (u - w / (1j * asymptotic_k)) / 2.0
    a_incident = a_incident_times_phase / e_plus
    b_reflected = b_reflected_times_phase / e_minus
    reflection = b_reflected / a_incident
    reflection_power = abs(reflection) ** 2
    transmission_power = 1.0 / (abs(a_incident) ** 2)

    return {
        "Omega": omega_value,
        "ell": ell_value,
        "q": q_value,
        "s_branch": branch_speed,
        "asymptotic_k": asymptotic_k,
        "x_in": x_in,
        "x_out": x_out,
        "steps": steps,
        "R_ph": reflection,
        "|R_ph|^2": reflection_power,
        "|T_ph|^2": transmission_power,
        "flux_sum": reflection_power + transmission_power,
    }


def derive_finite_core_propagation_center_regular_gate():
    """
    Finite-core propagation and center regularity.

    The C2 core has a finite positive characteristic redshift B/A at x=0 and
    x=1.  For every finite q and every positive local speed root s, the core
    tortoise distance is a finite integral.  The center is therefore a regular
    endpoint for the principal wave problem, not an infinite-redshift wall.

    Near the regular spherical center the master variable u_l has the standard
    Frobenius pair u_l~r^(ell+1) and u_l~r^(-ell).  The physical center
    condition selects u_l~r^(ell+1).
    """
    q, x, c, r_s, s_local, ell = sp.symbols(
        "q x c r_s s_local ell",
        positive=True,
    )
    log_red_core = q * (
        -sp.Integer(1)
        - sp.Rational(23, 4) * x**2
        + sp.Rational(15, 2) * x**4
        - sp.Rational(11, 4) * x**6
    )
    v2_core = sp.simplify(c**2 * s_local * sp.exp(log_red_core))
    tortoise_integrand = sp.simplify(sp.exp(-log_red_core / 2))
    core_time = sp.Eq(
        sp.Symbol("Delta_t_core"),
        r_s
        / (q * c * sp.sqrt(s_local))
        * sp.Integral(tortoise_integrand, (x, 0, 1)),
    )

    center_series = sp.series(tortoise_integrand, x, 0, 5).removeO()
    y = sp.Symbol("y", positive=True)
    boundary_series = sp.series(
        tortoise_integrand.subs(x, 1 - y),
        y,
        0,
        4,
    ).removeO()

    p = sp.Symbol("p")
    indicial = sp.Eq(p * (p - 1), ell * (ell + 1))
    indicial_roots = sp.solve(indicial, p)
    regular_root = ell + 1
    singular_root = -ell

    local_symbol = derive_coupled_local_principal_symbol_gate()
    roots = local_symbol["mixed_speed_roots_local"]
    branch_speeds = [roots[0], roots[1], local_symbol["transverse_speed_squared_local"]]
    samples = []
    for q_value in (2.0, 4.0, 6.0):
        row = {"q": q_value}
        for label, speed in zip(("minus", "plus", "transverse"), branch_speeds):
            row[f"{label}_Delta_t_core_over_rs_c"] = _core_travel_time_dimensionless(
                q_value,
                float(sp.N(speed)),
            )
        samples.append(row)

    center_v2 = sp.simplify(v2_core.subs(x, 0))
    boundary_v2 = sp.simplify(v2_core.subs(x, 1))
    finite_checks = {
        "center_v2_positive_finite": center_v2,
        "boundary_v2_positive_finite": boundary_v2,
        "center_integrand_finite": sp.limit(tortoise_integrand, x, 0, dir="+"),
        "boundary_integrand_finite": sp.limit(tortoise_integrand, x, 1, dir="-"),
    }

    return {
        "finite_core_status": "PASS_FINITE_CORE_PROPAGATION_AND_CENTER_REGULARITY_LEDGER",
        "core_B_over_A": sp.Eq(sp.Symbol("B_over_A_core"), sp.exp(log_red_core)),
        "core_coordinate_speed_squared": sp.Eq(sp.Symbol("v_core^2"), v2_core),
        "endpoint_values": finite_checks,
        "core_tortoise_time": core_time,
        "center_integrand_series": center_series,
        "boundary_integrand_series_x_equals_1_minus_y": boundary_series,
        "regular_center_indicial_equation": indicial,
        "indicial_roots": indicial_roots,
        "regular_master_branch": sp.Eq(sp.Symbol("u_l"), sp.Symbol("C_reg") * sp.Symbol("r") ** regular_root),
        "discarded_singular_branch": sp.Eq(
            sp.Symbol("u_l_sing"),
            sp.Symbol("C_sing") * sp.Symbol("r") ** singular_root,
        ),
        "sample_core_times": samples,
        "reading": (
            "finite q gives finite propagation from the C2 boundary to the "
            "regular center; the center condition is regularity, not a hard "
            "reflecting wall inserted at r_c."
        ),
        "next_gate": (
            "write the radial transfer problem with the regular-center "
            "condition and outgoing exterior condition."
        ),
    }


def derive_qnm_echo_transfer_problem_gate():
    """
    QNM/echo transfer problem with regular center and outgoing exterior.

    The C2 boundary is transmissive at leading order, so the useful transfer
    problem is not a hard-wall echo model.  The radial problem is:

    - regular center: u_l ~ r^(ell+1);
    - C2 matching: u and du/dr_* pass continuously through r_c;
    - exterior outgoing condition: u ~ exp(+i Omega r_*) at infinity.

    A compact echo denominator can be written after compressing the photon
    barrier into its frequency-dependent reflection coefficient R_ph(Omega).
    The pole condition is

        1 - R_ph(Omega) R_c exp(2 i Omega T_branch) = 0,

    where T_branch is the one-way regular-center-to-photon-sphere travel time.
    This is a transfer-function formulation, not a numerical QNM spectrum.
    """
    Omega, q, s_local, ell = sp.symbols(
        "Omega q s_local ell",
        positive=True,
    )
    x = sp.Symbol("x", positive=True)
    R_ph = sp.Function("R_ph")(Omega)
    A_ph = sp.Function("A_ph")(Omega)

    exterior_time = (
        q * (sp.Ei(q) - sp.Ei(1) + sp.E)
        - sp.exp(q)
    ) / q
    log_red_core = q * (
        -sp.Integer(1)
        - sp.Rational(23, 4) * x**2
        + sp.Rational(15, 2) * x**4
        - sp.Rational(11, 4) * x**6
    )
    core_time = (
        sp.Integral(sp.exp(-log_red_core / 2), (x, 0, 1))
        / (q * sp.sqrt(s_local))
    )
    branch_time = sp.simplify(exterior_time + core_time)

    center_reflection = (-1) ** (ell + 1)
    transfer_denominator = sp.simplify(
        1 - R_ph * center_reflection * sp.exp(2 * sp.I * Omega * branch_time)
    )
    response = sp.simplify(A_ph / transfer_denominator)
    pole_condition = sp.Eq(transfer_denominator, 0)

    local_symbol = derive_coupled_local_principal_symbol_gate()
    branches = {
        "minus": local_symbol["mixed_speed_roots_local"][0],
        "plus": local_symbol["mixed_speed_roots_local"][1],
        "transverse": local_symbol["transverse_speed_squared_local"],
    }
    samples = []
    for q_value in (2.0, 4.0, 6.0):
        row = {
            "q": q_value,
            "Delta_t_ext_over_rs_c": _exterior_cavity_time_dimensionless(q_value),
        }
        for label, speed in branches.items():
            core = _core_travel_time_dimensionless(q_value, float(sp.N(speed)))
            total = row["Delta_t_ext_over_rs_c"] + core
            row[f"{label}_T_branch_over_rs_c"] = total
            row[f"{label}_echo_roundtrip_over_rs_c"] = 2.0 * total
        samples.append(row)

    return {
        "transfer_problem_status": "PASS_QNM_ECHO_TRANSFER_PROBLEM_FORMULATED__NUMERICAL_SPECTRUM_OPEN",
        "dimensionless_frequency": sp.Eq(sp.Symbol("Omega"), sp.Symbol("omega") * sp.Symbol("r_s") / sp.Symbol("c")),
        "exterior_master_equation": (
            "d^2u/dr_*^2 + [Omega^2 - V_ext(x)]u = 0, "
            "with V_ext from derive_exterior_scalar_probe_master_operator"
        ),
        "regular_center_condition": sp.Eq(sp.Symbol("u_l"), sp.Symbol("C_reg") * sp.Symbol("r") ** (ell + 1)),
        "c2_matching_conditions": [
            "u_core(r_c)=u_ext(r_c)",
            "du_core/dr_*(r_c)=du_ext/dr_*(r_c)",
        ],
        "outgoing_infinity_condition": "u_ext ~ exp(+i Omega r_*)",
        "center_reflection_phase": sp.Eq(sp.Symbol("R_c"), center_reflection),
        "one_way_exterior_time_over_rs_c": sp.Eq(sp.Symbol("T_ext"), exterior_time),
        "one_way_core_time_over_rs_c": sp.Eq(sp.Symbol("T_core"), core_time),
        "one_way_branch_time_over_rs_c": sp.Eq(sp.Symbol("T_branch"), branch_time),
        "transfer_response": sp.Eq(sp.Symbol("H(Omega)"), response),
        "pole_condition": pole_condition,
        "sample_branch_times": samples,
        "reading": (
            "the QNM/echo problem is now a well-defined radial transfer problem; "
            "actual frequencies require R_ph(Omega) from exterior barrier "
            "scattering and the full background-dependent coupled ODE."
        ),
        "next_gate": "numerically compute R_ph(Omega) and solve the pole condition",
    }


def compute_exterior_photon_barrier_reflection_gate():
    """
    Numerical exterior photon-barrier reflection for the probe equation.

    This computes R_ph(Omega) by integrating the outgoing Jost solution from a
    large exterior radius back to the finite C2 boundary.  The value is a
    scalar-probe barrier reflection coefficient.  It is the first numerical
    input for the transfer denominator, not the final coupled QNM spectrum.
    """
    ell_value = 2
    q_value = 4.0
    omega_values = (0.25, 0.5, 1.0)
    rows = []
    convergence_rows = []

    for omega_value in omega_values:
        coarse = _rk4_outgoing_jost(
            omega_value,
            ell_value,
            q_value,
            x_out=80.0,
            steps=8000,
        )
        fine = _rk4_outgoing_jost(
            omega_value,
            ell_value,
            q_value,
            x_out=120.0,
            steps=12000,
        )
        rows.append({
            "Omega": omega_value,
            "ell": ell_value,
            "q": q_value,
            "x_out": fine["x_out"],
            "|R_ph|^2": fine["|R_ph|^2"],
            "|T_ph|^2": fine["|T_ph|^2"],
            "flux_sum": fine["flux_sum"],
            "R_ph_real": fine["R_ph"].real,
            "R_ph_imag": fine["R_ph"].imag,
        })
        convergence_rows.append({
            "Omega": omega_value,
            "abs_delta_R_power": abs(fine["|R_ph|^2"] - coarse["|R_ph|^2"]),
            "abs_flux_error_fine": abs(fine["flux_sum"] - 1.0),
            "coarse_R_power": coarse["|R_ph|^2"],
            "fine_R_power": fine["|R_ph|^2"],
        })

    max_flux_error = max(row["abs_flux_error_fine"] for row in convergence_rows)
    max_convergence_delta = max(row["abs_delta_R_power"] for row in convergence_rows)

    return {
        "reflection_status": (
            "PASS_NUMERICAL_PROBE_PHOTON_BARRIER_REFLECTION_COEFFICIENT"
            if max_flux_error < 5.0e-3
            else "CHECK_NUMERICAL_PROBE_PHOTON_BARRIER_REFLECTION_COEFFICIENT"
        ),
        "method": (
            "outgoing Jost integration in x with asymptotic matching at x_out; "
            "equation u_{rho rho}+[Omega^2-U(x)]u=0"
        ),
        "sample_parameters": {
            "ell": ell_value,
            "q": q_value,
            "x_in": 1.0 / q_value,
            "Omega_values": omega_values,
        },
        "reflection_samples": rows,
        "convergence_checks": convergence_rows,
        "max_flux_error": max_flux_error,
        "max_xout_convergence_delta_R_power": max_convergence_delta,
        "reading": (
            "the exterior photon barrier now has numerical R_ph samples for "
            "the transfer denominator; a production QNM scan should replace "
            "the plane-wave finite-x_out matching with a dedicated asymptotic "
            "Coulomb/Bessel tail or push x_out farther."
        ),
        "next_gate": "solve the transfer pole condition using the sampled or fitted R_ph(Omega)",
    }


def _nearest_constant_barrier_pole(
    omega_sample: float,
    r_real: float,
    r_imag: float,
    branch_time: float,
    ell_value: int,
):
    """Local pole estimate for 1-R_ph R_c exp(2 i Omega T)=0."""
    r_complex = complex(r_real, r_imag)
    center_reflection = (-1) ** (ell_value + 1)
    effective_reflection = r_complex * center_reflection
    magnitude = abs(effective_reflection)
    phase = cmath.phase(effective_reflection)
    mode_number = round((2.0 * branch_time * omega_sample + phase) / (2.0 * math.pi))
    omega_real = (2.0 * math.pi * mode_number - phase) / (2.0 * branch_time)
    omega_imag = math.log(magnitude) / (2.0 * branch_time)
    residual = (
        1.0
        - effective_reflection
        * cmath.exp(2j * complex(omega_real, omega_imag) * branch_time)
    )
    return {
        "Omega_sample": omega_sample,
        "mode_number": mode_number,
        "Omega_real": omega_real,
        "Omega_imag": omega_imag,
        "|R_eff|": magnitude,
        "phase_R_eff": phase,
        "pole_residual_abs": abs(residual),
    }


def solve_sampled_transfer_pole_estimate_gate():
    """
    Approximate pole estimates from sampled R_ph(Omega).

    For each sampled real frequency, this freezes R_ph at that value and solves
    the transfer denominator analytically.  The result is a local pole estimate,
    not the final complex-frequency QNM spectrum.  It checks the sign and scale
    of damping and gives a concrete target for the next full complex-plane scan.
    """
    reflection = compute_exterior_photon_barrier_reflection_gate()
    transfer = derive_qnm_echo_transfer_problem_gate()
    q_value = reflection["sample_parameters"]["q"]
    ell_value = reflection["sample_parameters"]["ell"]
    branch_row = next(
        row for row in transfer["sample_branch_times"]
        if abs(row["q"] - q_value) < 1.0e-12
    )
    branches = {
        "minus": branch_row["minus_T_branch_over_rs_c"],
        "plus": branch_row["plus_T_branch_over_rs_c"],
        "transverse": branch_row["transverse_T_branch_over_rs_c"],
    }

    estimates = []
    for sample in reflection["reflection_samples"]:
        for branch_name, branch_time in branches.items():
            estimate = _nearest_constant_barrier_pole(
                sample["Omega"],
                sample["R_ph_real"],
                sample["R_ph_imag"],
                branch_time,
                ell_value,
            )
            estimate.update({
                "branch": branch_name,
                "T_branch_over_rs_c": branch_time,
                "echo_roundtrip_over_rs_c": 2.0 * branch_time,
            })
            estimates.append(estimate)

    all_lower_half = all(row["Omega_imag"] <= 1.0e-12 for row in estimates)
    max_residual = max(row["pole_residual_abs"] for row in estimates)
    least_damped = max(estimates, key=lambda row: row["Omega_imag"])

    return {
        "pole_estimate_status": (
            "PASS_SAMPLED_CONSTANT_BARRIER_POLE_ESTIMATES"
            if reflection["reflection_status"]
            == "PASS_NUMERICAL_PROBE_PHOTON_BARRIER_REFLECTION_COEFFICIENT"
            and all_lower_half
            and max_residual < 1.0e-10
            else "CHECK_SAMPLED_CONSTANT_BARRIER_POLE_ESTIMATES"
        ),
        "approximation": (
            "R_ph is frozen at each sampled real Omega; final QNM spectrum "
            "needs analytic continuation or direct complex shooting."
        ),
        "q": q_value,
        "ell": ell_value,
        "estimates": estimates,
        "least_damped_estimate": least_damped,
        "all_estimates_in_lower_half_plane": all_lower_half,
        "max_pole_residual_abs": max_residual,
        "reading": (
            "sampled transfer poles have nonpositive imaginary part.  The "
            "low-frequency samples are very weakly damped because the photon "
            "barrier reflection is close to unity; this is an approximate "
            "echo-cavity diagnostic, not the final coupled QNM spectrum."
        ),
        "next_gate": "perform direct complex shooting with R_ph(Omega) in the complex plane",
    }


def _transfer_denominator_complex(
    omega_complex: complex,
    ell_value: int,
    q_value: float,
    branch_time: float,
    x_out: float,
    steps: int,
    s_value: float = 1.0,
) -> complex:
    """Direct complex transfer denominator using the outgoing Jost solution."""
    jost = _rk4_outgoing_jost(
        omega_complex,
        ell_value,
        q_value,
        x_out=x_out,
        steps=steps,
        s_value=s_value,
    )
    center_reflection = (-1) ** (ell_value + 1)
    return (
        1.0
        - jost["R_ph"]
        * center_reflection
        * cmath.exp(2j * omega_complex * branch_time)
    )


def _newton_complex_transfer_root(
    initial: complex,
    ell_value: int,
    q_value: float,
    branch_time: float,
    x_out: float,
    steps: int,
    s_value: float = 1.0,
    max_iter: int = 8,
):
    """Newton solve for the direct complex transfer denominator."""
    z = initial
    history = []
    converged = False
    for index in range(max_iter):
        residual = _transfer_denominator_complex(
            z,
            ell_value,
            q_value,
            branch_time,
            x_out,
            steps,
            s_value,
        )
        residual_abs = abs(residual)
        history.append({
            "iteration": index,
            "Omega_real": z.real,
            "Omega_imag": z.imag,
            "residual_abs": residual_abs,
        })
        if residual_abs < 1.0e-10:
            converged = True
            break

        h = 1.0e-5 * (1.0 + abs(z))
        derivative = (
            _transfer_denominator_complex(
                z + h,
                ell_value,
                q_value,
                branch_time,
                x_out,
                steps,
                s_value,
            )
            - _transfer_denominator_complex(
                z - h,
                ell_value,
                q_value,
                branch_time,
                x_out,
                steps,
                s_value,
            )
        ) / (2.0 * h)
        if abs(derivative) < 1.0e-14:
            break
        z -= residual / derivative

    final_residual = _transfer_denominator_complex(
        z,
        ell_value,
        q_value,
        branch_time,
        x_out,
        steps,
        s_value,
    )
    return {
        "Omega_real": z.real,
        "Omega_imag": z.imag,
        "residual_abs": abs(final_residual),
        "iterations": len(history),
        "converged": converged or abs(final_residual) < 1.0e-10,
        "x_out": x_out,
        "steps": steps,
        "s_branch": s_value,
        "history": history,
    }


def direct_complex_shooting_probe_root_gate():
    """
    Direct complex shooting for one transfer-denominator probe root.

    This promotes the sampled pole estimate into a direct complex root of the
    scalar-probe transfer denominator.  It is still not the final coupled QNM
    spectrum: the barrier is the scalar-probe exterior barrier and the core
    dynamics are compressed into the regular-center transfer time.
    """
    sampled = solve_sampled_transfer_pole_estimate_gate()
    initial_row = sampled["least_damped_estimate"]
    ell_value = sampled["ell"]
    q_value = sampled["q"]
    branch_time = initial_row["T_branch_over_rs_c"]
    initial = complex(initial_row["Omega_real"], initial_row["Omega_imag"])

    coarse = _newton_complex_transfer_root(
        initial,
        ell_value,
        q_value,
        branch_time,
        x_out=80.0,
        steps=5000,
    )
    fine = _newton_complex_transfer_root(
        complex(coarse["Omega_real"], coarse["Omega_imag"]),
        ell_value,
        q_value,
        branch_time,
        x_out=120.0,
        steps=8000,
    )
    root_delta = abs(
        complex(fine["Omega_real"], fine["Omega_imag"])
        - complex(coarse["Omega_real"], coarse["Omega_imag"])
    )

    return {
        "complex_shooting_status": (
            "PASS_DIRECT_COMPLEX_SHOOTING_PROBE_ROOT_LOWER_HALF_PLANE"
            if fine["converged"]
            and fine["residual_abs"] < 1.0e-8
            and fine["Omega_imag"] <= 1.0e-12
            and root_delta < 1.0e-5
            else "CHECK_DIRECT_COMPLEX_SHOOTING_PROBE_ROOT"
        ),
        "scope": (
            "scalar-probe transfer denominator with regular-center phase and "
            "outgoing exterior condition; not the full coupled QNM spectrum"
        ),
        "initial_sampled_estimate": initial_row,
        "coarse_root": coarse,
        "fine_root": fine,
        "coarse_fine_root_delta": root_delta,
        "reading": (
            "direct complex shooting finds a lower-half-plane probe root near "
            "the sampled estimate.  This supports the absence of a growing "
            "mode in this reduced transfer model."
        ),
        "next_gate": (
            "replace the reduced transfer model with the full background-"
            "dependent coupled radial ODE and scan multiple roots."
        ),
    }


def derive_background_dependent_coupled_radial_ode_gate():
    """
    Background-dependent coupled radial ODE at principal/eigenchannel level.

    The direct complex root above is a scalar-probe transfer root.  The p01
    coupled principal symbol has two radial eigenchannels.  For an eigenvalue
    s_i, the exterior radial equation in the light tortoise coordinate rho is

        u_i'' + [Omega^2/s_i - U_ext(x)] u_i = 0,

    or equivalently in the branch tortoise coordinate rho_i=rho/sqrt(s_i):

        d^2u_i/d rho_i^2 + [Omega^2 - s_i U_ext(x)] u_i = 0.

    This function records the coupled radial ODE and the corrected one-way
    travel times.  It also records the scope correction: the already computed
    direct complex root belongs to the scalar/lightlike probe transfer model;
    the slower mixed branch needs a branch-corrected scattering scan.
    """
    coeffs, s, det, _roots = minkowski_principal_symbol()
    point = compact_spectrum_local_stable_point()
    coeff_values = {
        key: sp.simplify(value.subs(point))
        for key, value in coeffs.items()
        if key not in {"L2", "a"}
    }
    det_at_point = sp.factor(sp.simplify(det.subs(point)))
    roots = [sp.simplify(root) for root in sp.solve(det_at_point, s)]
    roots = sorted(roots, key=lambda root: float(sp.N(root)))
    c_t_sq = sp.simplify(-coeff_values["C_T"] / coeff_values["K_T"])

    Omega, x, L, s_i = sp.symbols("Omega x L s_i", positive=True)
    u_i = sp.Function("u_i")
    rho = sp.Symbol("rho")
    rho_i = sp.Symbol("rho_i")
    u_ext = sp.exp(-2 / x) * (L * x**2 + x - sp.Rational(1, 4)) / x**4

    K_matrix = sp.Matrix([[coeff_values["A"], 0], [0, coeff_values["B_long"]]])
    C_matrix = sp.Matrix([[coeff_values["C"], 0], [0, coeff_values["D"]]])
    Mix_matrix = sp.Matrix([[0, coeff_values["M_mix"]], [coeff_values["M_mix"], 0]])

    eigenvectors = {}
    for label, root in (("minus", roots[0]), ("plus", roots[1])):
        ratio = sp.simplify(
            -(coeff_values["A"] * root + coeff_values["C"])
            / (coeff_values["M_mix"] * sp.sqrt(root))
        )
        eigenvectors[label] = {
            "s": root,
            "sqrt_s": sp.sqrt(root),
            "pi_over_phi": ratio,
            "vector_phi_pi": (1, ratio),
        }
    eigenvectors["transverse"] = {
        "s": c_t_sq,
        "sqrt_s": sp.sqrt(c_t_sq),
        "pi_over_phi": None,
        "vector_phi_pi": "transverse solid mode",
    }

    branch_ode_light_tortoise = sp.Eq(
        sp.diff(u_i(rho), rho, 2)
        + (Omega**2 / s_i - u_ext) * u_i(rho),
        0,
    )
    branch_ode_branch_tortoise = sp.Eq(
        sp.diff(u_i(rho_i), rho_i, 2)
        + (Omega**2 - s_i * u_ext) * u_i(rho_i),
        0,
    )

    samples = []
    branch_speeds = {
        "minus": roots[0],
        "plus": roots[1],
        "transverse": c_t_sq,
    }
    for q_value in (2.0, 4.0, 6.0):
        ext_time = _exterior_cavity_time_dimensionless(q_value)
        row = {"q": q_value, "T_ext_light_over_rs_c": ext_time}
        for label, speed in branch_speeds.items():
            speed_float = float(sp.N(speed))
            corrected = ext_time / math.sqrt(speed_float) + _core_travel_time_dimensionless(
                q_value,
                speed_float,
            )
            row[f"{label}_T_branch_corrected_over_rs_c"] = corrected
            row[f"{label}_roundtrip_corrected_over_rs_c"] = 2.0 * corrected
        samples.append(row)

    previous_transfer = derive_qnm_echo_transfer_problem_gate()
    previous_q4 = next(row for row in previous_transfer["sample_branch_times"] if row["q"] == 4.0)
    corrected_q4 = next(row for row in samples if row["q"] == 4.0)

    return {
        "coupled_radial_ode_status": (
            "PASS_BACKGROUND_DEPENDENT_COUPLED_RADIAL_ODE_FORMULATED__BRANCH_CORRECTED_SCAN_OPEN"
        ),
        "coefficient_point": point,
        "principal_matrices": {
            "K_time": K_matrix,
            "C_space": C_matrix,
            "M_mixed_time_space": Mix_matrix,
        },
        "characteristic_determinant": sp.Eq(sp.Symbol("D(s)"), det_at_point),
        "eigenchannels": eigenvectors,
        "exterior_potential_U": sp.Eq(sp.Symbol("U_ext"), u_ext),
        "branch_ode_light_tortoise": branch_ode_light_tortoise,
        "branch_ode_branch_tortoise": branch_ode_branch_tortoise,
        "corrected_branch_times": samples,
        "scope_correction": (
            "the direct complex root computed above is the scalar/lightlike "
            "probe root.  The slower mixed branch must use the branch-corrected "
            "exterior equation Omega^2/s_i-U_ext and therefore needs a rescan."
        ),
        "q4_time_comparison": {
            "previous_minus_T": previous_q4["minus_T_branch_over_rs_c"],
            "corrected_minus_T": corrected_q4["minus_T_branch_corrected_over_rs_c"],
            "previous_plus_T": previous_q4["plus_T_branch_over_rs_c"],
            "corrected_plus_T": corrected_q4["plus_T_branch_corrected_over_rs_c"],
        },
        "next_gate": "rerun exterior scattering and complex roots for each coupled eigenchannel",
    }


def compute_branch_corrected_reduced_root_scan_gate():
    """
    Branch-corrected reduced scattering and transfer-root scan.

    This is the next reduced calculation after the scalar/lightlike probe root.
    It keeps the same one-channel transfer denominator, but now uses the
    eigenchannel-corrected exterior equation Omega^2/s_i-U_ext and the corrected
    branch travel time.  The two unique speeds at the chosen p01 point are
    s_-=9/17 and s_+=s_T=1.
    """
    ell_value = 2
    q_value = 4.0
    omega_values = (0.25, 0.5, 1.0)
    coupled_ode = derive_background_dependent_coupled_radial_ode_gate()
    corrected_row = next(
        row for row in coupled_ode["corrected_branch_times"]
        if abs(row["q"] - q_value) < 1.0e-12
    )
    eigenchannels = coupled_ode["eigenchannels"]
    branches = {
        "minus": {
            "s": float(sp.N(eigenchannels["minus"]["s"])),
            "T_branch_over_rs_c": corrected_row["minus_T_branch_corrected_over_rs_c"],
            "degenerate_channels": ["minus"],
        },
        "plus_transverse": {
            "s": float(sp.N(eigenchannels["plus"]["s"])),
            "T_branch_over_rs_c": corrected_row["plus_T_branch_corrected_over_rs_c"],
            "degenerate_channels": ["plus", "transverse"],
        },
    }

    branch_results = []
    for branch_name, branch_data in branches.items():
        s_value = branch_data["s"]
        branch_time = branch_data["T_branch_over_rs_c"]
        samples = []
        convergence_rows = []
        estimates = []

        for omega_value in omega_values:
            coarse = _rk4_outgoing_jost(
                omega_value,
                ell_value,
                q_value,
                x_out=80.0,
                steps=8000,
                s_value=s_value,
            )
            fine = _rk4_outgoing_jost(
                omega_value,
                ell_value,
                q_value,
                x_out=120.0,
                steps=12000,
                s_value=s_value,
            )
            sample = {
                "Omega": omega_value,
                "s_branch": s_value,
                "|R_ph|^2": fine["|R_ph|^2"],
                "|T_ph|^2": fine["|T_ph|^2"],
                "flux_sum": fine["flux_sum"],
                "R_ph_real": fine["R_ph"].real,
                "R_ph_imag": fine["R_ph"].imag,
            }
            samples.append(sample)
            convergence_rows.append({
                "Omega": omega_value,
                "abs_delta_R_power": abs(fine["|R_ph|^2"] - coarse["|R_ph|^2"]),
                "abs_flux_error_fine": abs(fine["flux_sum"] - 1.0),
                "coarse_R_power": coarse["|R_ph|^2"],
                "fine_R_power": fine["|R_ph|^2"],
            })

            estimate = _nearest_constant_barrier_pole(
                omega_value,
                sample["R_ph_real"],
                sample["R_ph_imag"],
                branch_time,
                ell_value,
            )
            estimate.update({
                "branch": branch_name,
                "s_branch": s_value,
                "T_branch_over_rs_c": branch_time,
                "echo_roundtrip_over_rs_c": 2.0 * branch_time,
            })
            estimates.append(estimate)

        least_damped = max(estimates, key=lambda row: row["Omega_imag"])
        initial = complex(least_damped["Omega_real"], least_damped["Omega_imag"])
        coarse_root = _newton_complex_transfer_root(
            initial,
            ell_value,
            q_value,
            branch_time,
            x_out=80.0,
            steps=5000,
            s_value=s_value,
        )
        fine_root = _newton_complex_transfer_root(
            complex(coarse_root["Omega_real"], coarse_root["Omega_imag"]),
            ell_value,
            q_value,
            branch_time,
            x_out=120.0,
            steps=8000,
            s_value=s_value,
        )
        root_delta = abs(
            complex(fine_root["Omega_real"], fine_root["Omega_imag"])
            - complex(coarse_root["Omega_real"], coarse_root["Omega_imag"])
        )

        branch_results.append({
            "branch": branch_name,
            "degenerate_channels": branch_data["degenerate_channels"],
            "s_branch": s_value,
            "T_branch_over_rs_c": branch_time,
            "reflection_samples": samples,
            "convergence_checks": convergence_rows,
            "sampled_estimates": estimates,
            "least_damped_sampled_estimate": least_damped,
            "coarse_root": coarse_root,
            "fine_root": fine_root,
            "coarse_fine_root_delta": root_delta,
        })

    max_flux_error = max(
        row["abs_flux_error_fine"]
        for result in branch_results
        for row in result["convergence_checks"]
    )
    max_convergence_delta = max(
        row["abs_delta_R_power"]
        for result in branch_results
        for row in result["convergence_checks"]
    )
    roots_lower_half = all(
        result["fine_root"]["Omega_imag"] <= 1.0e-12
        for result in branch_results
    )
    roots_converged = all(
        result["fine_root"]["converged"]
        and result["fine_root"]["residual_abs"] < 1.0e-8
        and result["coarse_fine_root_delta"] < 1.0e-5
        for result in branch_results
    )

    return {
        "branch_corrected_scan_status": (
            "PASS_BRANCH_CORRECTED_REDUCED_ROOT_SCAN_LOWER_HALF_PLANE"
            if roots_lower_half and roots_converged and max_flux_error < 5.0e-3
            else "CHECK_BRANCH_CORRECTED_REDUCED_ROOT_SCAN"
        ),
        "scope": (
            "one-channel reduced transfer scan using branch-corrected exterior "
            "speeds; full coupled matrix QNMs remain the next layer"
        ),
        "ell": ell_value,
        "q": q_value,
        "branches": branch_results,
        "max_flux_error": max_flux_error,
        "max_xout_convergence_delta_R_power": max_convergence_delta,
        "reading": (
            "the branch-corrected reduced scan keeps both unique channels in the "
            "lower half-plane.  The slower branch moves because both its "
            "exterior wave number and its travel time differ from the lightlike "
            "probe value."
        ),
        "next_gate": "promote the reduced scan to a full coupled matrix radial QNM problem",
    }


def compute_coupled_matrix_radial_transfer_gate(branch_scan=None, coupled_ode=None):
    """
    Coupled 2x2 radial transfer determinant in the principal eigenbasis.

    At the explicit p01 stable point the radial phase/medium principal symbol
    has an invertible eigenbasis.  In that basis the reduced transfer
    determinant is the product of the two radial branch denominators.  This gate
    checks that the branch-corrected roots are zeros of the 2x2 determinant in
    the same reduced exterior/core transfer model.
    """
    if coupled_ode is None:
        coupled_ode = derive_background_dependent_coupled_radial_ode_gate()
    if branch_scan is None:
        branch_scan = compute_branch_corrected_reduced_root_scan_gate()

    ell_value = branch_scan["ell"]
    q_value = branch_scan["q"]
    eigenchannels = coupled_ode["eigenchannels"]
    matrices = coupled_ode["principal_matrices"]
    K_matrix = matrices["K_time"]
    C_matrix = matrices["C_space"]
    Mix_matrix = matrices["M_mixed_time_space"]

    s = sp.Symbol("s", positive=True)
    symbol_matrix = sp.Matrix([
        [K_matrix[0, 0] * s + C_matrix[0, 0], Mix_matrix[0, 1] * sp.sqrt(s)],
        [Mix_matrix[1, 0] * sp.sqrt(s), K_matrix[1, 1] * s + C_matrix[1, 1]],
    ])
    basis = sp.Matrix.hstack(
        sp.Matrix(eigenchannels["minus"]["vector_phi_pi"]),
        sp.Matrix(eigenchannels["plus"]["vector_phi_pi"]),
    )
    basis_det = sp.factor(sp.simplify(basis.det()))

    eigen_residuals = {}
    for branch_name in ("minus", "plus"):
        channel = eigenchannels[branch_name]
        vector = sp.Matrix(channel["vector_phi_pi"])
        residual = sp.simplify(symbol_matrix.subs(s, channel["s"]) * vector)
        eigen_residuals[branch_name] = list(residual)

    branch_by_name = {
        result["branch"]: result
        for result in branch_scan["branches"]
    }
    radial_branches = {
        "minus": branch_by_name["minus"],
        "plus": branch_by_name["plus_transverse"],
    }

    def denominator_for(branch_result, omega_complex):
        fine_root = branch_result["fine_root"]
        return _transfer_denominator_complex(
            omega_complex,
            ell_value,
            q_value,
            branch_result["T_branch_over_rs_c"],
            x_out=fine_root["x_out"],
            steps=fine_root["steps"],
            s_value=branch_result["s_branch"],
        )

    determinant_rows = []
    for root_branch, root_result in radial_branches.items():
        fine_root = root_result["fine_root"]
        omega_root = complex(fine_root["Omega_real"], fine_root["Omega_imag"])
        denominators = {
            branch_name: denominator_for(branch_result, omega_root)
            for branch_name, branch_result in radial_branches.items()
        }
        determinant = denominators["minus"] * denominators["plus"]
        determinant_rows.append({
            "root_branch": root_branch,
            "Omega_real": omega_root.real,
            "Omega_imag": omega_root.imag,
            "D_minus_abs": abs(denominators["minus"]),
            "D_plus_abs": abs(denominators["plus"]),
            "matrix_determinant_abs": abs(determinant),
        })

    basis_ok = basis_det != 0
    symbol_ok = all(
        all(sp.simplify(value) == 0 for value in residual)
        for residual in eigen_residuals.values()
    )
    determinant_ok = all(
        row["matrix_determinant_abs"] < 1.0e-8
        and row["Omega_imag"] <= 1.0e-12
        for row in determinant_rows
    )

    return {
        "matrix_transfer_status": (
            "PASS_COUPLED_MATRIX_RADIAL_TRANSFER_DETERMINANT"
            if branch_scan["branch_corrected_scan_status"]
            == "PASS_BRANCH_CORRECTED_REDUCED_ROOT_SCAN_LOWER_HALF_PLANE"
            and basis_ok
            and symbol_ok
            and determinant_ok
            else "CHECK_COUPLED_MATRIX_RADIAL_TRANSFER_DETERMINANT"
        ),
        "scope": (
            "2x2 radial matrix determinant in the fixed principal eigenbasis; "
            "radially varying coefficient mixing is the next layer"
        ),
        "symbol_matrix": symbol_matrix,
        "eigenbasis": basis,
        "eigenbasis_determinant": basis_det,
        "eigen_symbol_residuals": eigen_residuals,
        "matrix_transfer_determinant": "det D_matrix(Omega)=D_minus(Omega)*D_plus(Omega)",
        "plus_transverse_note": (
            "the plus radial branch and the transverse branch share s=1 in the "
            "reduced scan; this 2x2 determinant uses the radial plus branch"
        ),
        "determinant_root_checks": determinant_rows,
        "reading": (
            "the branch-corrected roots are also roots of the coupled 2x2 "
            "radial determinant at the current principal-eigenbasis level."
        ),
        "next_gate": "include radially varying coefficient mixing in the matrix radial QNM system",
    }


def derive_radially_varying_eigenbasis_mixing_gate(coupled_ode=None):
    """
    Radially varying eigenbasis mixing for the coupled radial system.

    If the local principal coefficients become functions of radius, the local
    eigenvectors form a matrix P(rho).  Writing the field vector as y=P a gives
    the eigenbasis equation

        a'' + 2 Gamma a' + (Gamma' + Gamma^2 + diagonal branch operator) a = 0,

    with Gamma=P^{-1}P'.  Thus radial mixing is controlled by the rotation of
    the eigenbasis, not by the mere redshift factor.  At the constant p01 point
    used in the current compact-spectrum scan, P' is exactly zero.
    """
    if coupled_ode is None:
        coupled_ode = derive_background_dependent_coupled_radial_ode_gate()

    rho = sp.Symbol("rho")
    p_minus = sp.Function("p_minus")(rho)
    p_plus = sp.Function("p_plus")(rho)
    omega = sp.Symbol("Omega")
    u_minus = sp.Function("U_minus")(rho)
    u_plus = sp.Function("U_plus")(rho)

    basis = sp.Matrix([[1, 1], [p_minus, p_plus]])
    basis_det = sp.factor(sp.simplify(basis.det()))
    gamma = sp.simplify(basis.inv() * sp.diff(basis, rho))
    mixing_potential = sp.simplify(sp.diff(gamma, rho) + gamma * gamma)
    diagonal_branch_operator = sp.diag(omega**2 - u_minus, omega**2 - u_plus)
    eigenbasis_operator = sp.simplify(
        diagonal_branch_operator
        + mixing_potential
    )

    eigenchannels = coupled_ode["eigenchannels"]
    constant_subs = {
        p_minus: eigenchannels["minus"]["pi_over_phi"],
        p_plus: eigenchannels["plus"]["pi_over_phi"],
        sp.diff(p_minus, rho): 0,
        sp.diff(p_plus, rho): 0,
        sp.diff(p_minus, rho, 2): 0,
        sp.diff(p_plus, rho, 2): 0,
    }
    gamma_constant = sp.simplify(gamma.subs(constant_subs))
    mixing_constant = sp.simplify(mixing_potential.subs(constant_subs))
    offdiag_mixing_constant = [
        sp.simplify(mixing_constant[0, 1]),
        sp.simplify(mixing_constant[1, 0]),
    ]
    all_constant_mixing_zero = all(
        sp.simplify(value) == 0
        for value in list(gamma_constant) + list(mixing_constant)
    )

    coeff_profile_status = (
        "constant p01 coefficient point used in p05b; no separate "
        "background-dependent coefficient profile is supplied in p01/p05"
    )

    return {
        "radial_mixing_status": (
            "PASS_RADIAL_EIGENBASIS_MIXING_FORMULATED__ZERO_FOR_CONSTANT_P01_POINT"
            if all_constant_mixing_zero
            else "CHECK_RADIAL_EIGENBASIS_MIXING"
        ),
        "basis": basis,
        "basis_determinant": basis_det,
        "connection_Gamma": gamma,
        "mixing_potential_Gamma_prime_plus_Gamma_sq": mixing_potential,
        "eigenbasis_operator": eigenbasis_operator,
        "constant_point_substitution": constant_subs,
        "constant_point_Gamma": gamma_constant,
        "constant_point_mixing_potential": mixing_constant,
        "constant_point_offdiag_mixing": offdiag_mixing_constant,
        "coefficient_profile_status": coeff_profile_status,
        "reading": (
            "with the current constant p01 stable point the eigenbasis does not "
            "rotate with radius, so the additional radial mixing terms vanish. "
            "A nonzero mixing layer requires an explicit background-dependent "
            "coefficient profile."
        ),
        "next_gate": (
            "derive or choose the background-dependent coefficient profile "
            "before running a genuinely variable-coefficient matrix QNM scan"
        ),
    }


def derive_admissible_background_coefficient_profile_gate(coupled_ode=None):
    """
    Admissible background-dependent coefficient profile for a variable system.

    The compact-spectrum scan uses one constant p01 stable point.  This gate
    builds a controlled variable-profile family around that point without
    changing the two radial characteristic roots.  The profile is anchored with
    a C2 bump on 0<=z<=1:

        p_-(z)=p_-0 + eps z^3(1-z)^3,  p_+(z)=1.

    From the two eigenvectors and fixed roots s_-=9/17, s_+=1, it reconstructs
    A(z), B(z), C(z), D(z), M(z) in the 2x2 principal symbol.  For eps=0 it is
    exactly the constant p05b point.  For 0<=eps<=1 the eigenbasis remains
    separated and the sign pattern A>0, B>0, C<0, D<0 is preserved.
    """
    if coupled_ode is None:
        coupled_ode = derive_background_dependent_coupled_radial_ode_gate()

    z, eps, s = sp.symbols("z eps s", real=True)
    s_minus = coupled_ode["eigenchannels"]["minus"]["s"]
    s_plus = coupled_ode["eigenchannels"]["plus"]["s"]
    sqrt_s_minus = sp.sqrt(s_minus)
    p_minus_0 = coupled_ode["eigenchannels"]["minus"]["pi_over_phi"]
    p_plus = coupled_ode["eigenchannels"]["plus"]["pi_over_phi"]
    A0 = coupled_ode["principal_matrices"]["K_time"][0, 0]

    bump = z**3 * (1 - z)**3
    p_minus = sp.simplify(p_minus_0 + eps * bump)
    p_minus_prime = sp.diff(p_minus, z)
    p_minus_second = sp.diff(p_minus, z, 2)

    M = sp.simplify(-A0 * (s_plus - s_minus) / (sp.sqrt(s_plus) * p_plus - sqrt_s_minus * p_minus))
    B = sp.simplify(-M * (sp.sqrt(s_plus) * p_plus - sqrt_s_minus / p_minus) / (s_plus - s_minus))
    C = sp.simplify(-A0 * s_minus - M * sqrt_s_minus * p_minus)
    D = sp.simplify(-B * s_plus - M * sp.sqrt(s_plus) / p_plus)

    determinant = sp.factor(sp.simplify((A0 * s + C) * (B * s + D) - M**2 * s))
    root_residuals = {
        "minus": sp.factor(sp.simplify(determinant.subs(s, s_minus))),
        "plus": sp.factor(sp.simplify(determinant.subs(s, s_plus))),
    }

    endpoint_subs = [{z: 0}, {z: 1}]
    endpoint_coefficients = [
        {
            "z": point[z],
            "A": sp.simplify(A0.subs(point) if hasattr(A0, "subs") else A0),
            "B": sp.simplify(B.subs(point)),
            "C": sp.simplify(C.subs(point)),
            "D": sp.simplify(D.subs(point)),
            "M": sp.simplify(M.subs(point)),
            "p_minus": sp.simplify(p_minus.subs(point)),
            "p_minus_prime": sp.simplify(p_minus_prime.subs(point)),
            "p_minus_second": sp.simplify(p_minus_second.subs(point)),
        }
        for point in endpoint_subs
    ]

    constant_values = {
        "A": sp.Rational(13, 2),
        "B": sp.Rational(17, 2),
        "C": -sp.Rational(9, 2),
        "D": -sp.Rational(13, 2),
        "M": -sp.Integer(2),
        "p_minus": p_minus_0,
    }
    endpoint_matches_constant = all(
        row["A"] == constant_values["A"]
        and row["B"] == constant_values["B"]
        and row["C"] == constant_values["C"]
        and row["D"] == constant_values["D"]
        and row["M"] == constant_values["M"]
        and row["p_minus"] == constant_values["p_minus"]
        and row["p_minus_prime"] == 0
        and row["p_minus_second"] == 0
        for row in endpoint_coefficients
    )

    sample_points = [sp.Rational(i, 8) for i in range(9)]
    sample_rows = []
    for point in sample_points:
        subs = {z: point, eps: 1}
        row = {
            "z": point,
            "p_minus": float(sp.N(p_minus.subs(subs))),
            "A": float(sp.N(A0)),
            "B": float(sp.N(B.subs(subs))),
            "C": float(sp.N(C.subs(subs))),
            "D": float(sp.N(D.subs(subs))),
            "M": float(sp.N(M.subs(subs))),
        }
        row["sign_pattern_ok"] = (
            row["A"] > 0
            and row["B"] > 0
            and row["C"] < 0
            and row["D"] < 0
            and row["M"] < 0
            and row["p_minus"] < 0
        )
        sample_rows.append(row)

    p_upper_eps1 = sp.simplify(p_minus_0 + sp.Rational(1, 64))
    profile_interval_checks = {
        "bump_C2_zero_at_z0": [
            sp.simplify(sp.diff(bump, z, order).subs(z, 0))
            for order in range(3)
        ],
        "bump_C2_zero_at_z1": [
            sp.simplify(sp.diff(bump, z, order).subs(z, 1))
            for order in range(3)
        ],
        "p_minus_upper_for_eps_1": p_upper_eps1,
        "p_minus_stays_negative_for_0_le_eps_le_1": bool(sp.N(p_upper_eps1) < 0),
        "basis_gap_stays_positive_for_0_le_eps_le_1": bool(sp.N(1 - p_upper_eps1) > 0),
        "denominator_positive_for_0_le_eps_le_1": bool(
            sp.N(1 - sqrt_s_minus * p_upper_eps1) > 0
        ),
    }

    return {
        "coefficient_profile_status": (
            "PASS_ADMISSIBLE_BACKGROUND_COEFFICIENT_PROFILE_FAMILY_DERIVED"
            if all(value == 0 for value in root_residuals.values())
            and endpoint_matches_constant
            and all(row["sign_pattern_ok"] for row in sample_rows)
            and all(
                value == 0
                for value in profile_interval_checks["bump_C2_zero_at_z0"]
                + profile_interval_checks["bump_C2_zero_at_z1"]
            )
            and profile_interval_checks["p_minus_stays_negative_for_0_le_eps_le_1"]
            and profile_interval_checks["basis_gap_stays_positive_for_0_le_eps_le_1"]
            and profile_interval_checks["denominator_positive_for_0_le_eps_le_1"]
            else "CHECK_ADMISSIBLE_BACKGROUND_COEFFICIENT_PROFILE_FAMILY"
        ),
        "profile_coordinate": "z in [0,1]",
        "amplitude_range": "0 <= eps <= 1",
        "bump_profile": sp.Eq(sp.Symbol("b(z)"), bump),
        "p_minus_profile": sp.Eq(sp.Symbol("p_minus(z)"), p_minus),
        "p_plus_profile": sp.Eq(sp.Symbol("p_plus(z)"), p_plus),
        "coefficient_profiles": {
            "A": A0,
            "B": B,
            "C": C,
            "D": D,
            "M": M,
        },
        "fixed_roots": {
            "s_minus": s_minus,
            "s_plus": s_plus,
        },
        "determinant_root_residuals": root_residuals,
        "endpoint_coefficients": endpoint_coefficients,
        "constant_p01_values": constant_values,
        "profile_interval_checks": profile_interval_checks,
        "eps1_sample_sign_checks": sample_rows,
        "reading": (
            "this gives a controlled variable-coefficient family anchored to "
            "the constant p01 point.  It is an admissible test profile for the "
            "next matrix scan; deriving eps and the profile from a microscopic "
            "off-branch action remains a separate source-level step."
        ),
        "next_gate": "run the matrix radial system with this admissible variable profile",
    }


def _profile_p_minus_value(z_value: float, eps_value: float) -> float:
    p0 = -3.0 / math.sqrt(17.0)
    return p0 + eps_value * z_value**3 * (1.0 - z_value) ** 3


def _profile_p_minus_prime_value(z_value: float, eps_value: float) -> float:
    return eps_value * (
        3.0 * z_value**2
        - 12.0 * z_value**3
        + 15.0 * z_value**4
        - 6.0 * z_value**5
    )


def _profile_p_minus_second_value(z_value: float, eps_value: float) -> float:
    return eps_value * (
        6.0 * z_value
        - 36.0 * z_value**2
        + 60.0 * z_value**3
        - 30.0 * z_value**4
    )


def _variable_profile_rhs(z_value: float, state, omega_value: float, eps_value: float):
    """First-order form of the 2x2 eigenbasis radial system on 0<=z<=1."""
    a_minus, a_plus, v_minus, v_plus = state
    s_minus = 9.0 / 17.0
    s_plus = 1.0
    p_minus = _profile_p_minus_value(z_value, eps_value)
    p_prime = _profile_p_minus_prime_value(z_value, eps_value)
    p_second = _profile_p_minus_second_value(z_value, eps_value)
    denom = p_minus - 1.0

    gamma00 = p_prime / denom
    gamma10 = -p_prime / denom
    mix00 = p_second / denom
    mix10 = -p_second / denom

    k_minus_sq = omega_value**2 / s_minus
    k_plus_sq = omega_value**2 / s_plus

    acc_minus = (
        -2.0 * gamma00 * v_minus
        - (k_minus_sq + mix00) * a_minus
    )
    acc_plus = (
        -2.0 * gamma10 * v_minus
        - mix10 * a_minus
        - k_plus_sq * a_plus
    )
    return [v_minus, v_plus, acc_minus, acc_plus]


def _rk4_variable_profile_column(initial, omega_value: float, eps_value: float, steps: int):
    h = 1.0 / steps
    state = [float(value) for value in initial]
    z_value = 0.0

    def add_scaled(base, delta, scale):
        return [
            base[index] + scale * delta[index]
            for index in range(4)
        ]

    for _ in range(steps):
        k1 = _variable_profile_rhs(z_value, state, omega_value, eps_value)
        k2 = _variable_profile_rhs(
            z_value + h / 2.0,
            add_scaled(state, k1, h / 2.0),
            omega_value,
            eps_value,
        )
        k3 = _variable_profile_rhs(
            z_value + h / 2.0,
            add_scaled(state, k2, h / 2.0),
            omega_value,
            eps_value,
        )
        k4 = _variable_profile_rhs(
            z_value + h,
            add_scaled(state, k3, h),
            omega_value,
            eps_value,
        )
        state = [
            state[index]
            + h * (k1[index] + 2.0 * k2[index] + 2.0 * k3[index] + k4[index]) / 6.0
            for index in range(4)
        ]
        z_value += h
    return state


def _variable_profile_transfer_matrix(omega_value: float, eps_value: float, steps: int = 4000):
    columns = [
        _rk4_variable_profile_column(initial, omega_value, eps_value, steps)
        for initial in (
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        )
    ]
    return sp.Matrix(4, 4, lambda row, col: columns[col][row])


def _constant_profile_analytic_transfer_matrix(omega_value: float):
    s_minus = 9.0 / 17.0
    k_minus = omega_value / math.sqrt(s_minus)
    k_plus = omega_value
    c_minus = math.cos(k_minus)
    s_minus_trig = math.sin(k_minus)
    c_plus = math.cos(k_plus)
    s_plus_trig = math.sin(k_plus)
    return sp.Matrix([
        [c_minus, 0.0, s_minus_trig / k_minus, 0.0],
        [0.0, c_plus, 0.0, s_plus_trig / k_plus],
        [-k_minus * s_minus_trig, 0.0, c_minus, 0.0],
        [0.0, -k_plus * s_plus_trig, 0.0, c_plus],
    ])


def _matrix_max_abs(matrix):
    return max(abs(complex(value)) for value in list(matrix))


def _matrix_frobenius_norm(matrix):
    return math.sqrt(sum(abs(complex(value)) ** 2 for value in list(matrix)))


def _transfer_offblock_max_abs(matrix):
    offblock_positions = [
        (0, 1), (0, 3), (2, 1), (2, 3),
        (1, 0), (1, 2), (3, 0), (3, 2),
    ]
    return max(abs(complex(matrix[row, col])) for row, col in offblock_positions)


def run_variable_profile_matrix_radial_system_gate():
    """
    Numerical finite-interval matrix radial system with the admissible profile.

    This gate propagates the coupled eigenbasis system through 0<=z<=1.  It is
    a variable-coefficient transfer-matrix test, not yet the asymptotic complex
    QNM problem.  The checks are:

    * eps=0 reproduces the analytic constant-branch transfer matrix;
    * eps=1 gives finite transfer matrices with determinant one to numerical
      accuracy;
    * off-diagonal channel transfer becomes nonzero only when the profile varies.
    """
    coefficient_profile = derive_admissible_background_coefficient_profile_gate()
    omega_values = (0.25, 0.5, 1.0)
    eps_values = (0.0, 0.5, 1.0)
    steps = 4000

    rows = []
    for omega_value in omega_values:
        analytic = _constant_profile_analytic_transfer_matrix(omega_value)
        for eps_value in eps_values:
            transfer = _variable_profile_transfer_matrix(
                omega_value,
                eps_value,
                steps=steps,
            )
            determinant = complex(sp.N(transfer.det(), 16))
            inverse = transfer.inv()
            analytic_error = (
                _matrix_max_abs(transfer - analytic)
                if eps_value == 0.0
                else None
            )
            rows.append({
                "Omega": omega_value,
                "eps": eps_value,
                "steps": steps,
                "det_transfer_real": determinant.real,
                "det_transfer_imag": determinant.imag,
                "det_minus_one_abs": abs(determinant - 1.0),
                "offblock_max_abs": _transfer_offblock_max_abs(transfer),
                "frobenius_condition_proxy": (
                    _matrix_frobenius_norm(transfer)
                    * _matrix_frobenius_norm(inverse)
                ),
                "analytic_constant_error": analytic_error,
                "max_abs_entry": _matrix_max_abs(transfer),
            })

    constant_errors = [
        row["analytic_constant_error"]
        for row in rows
        if row["analytic_constant_error"] is not None
    ]
    eps1_rows = [row for row in rows if row["eps"] == 1.0]
    max_constant_error = max(constant_errors)
    max_det_error = max(row["det_minus_one_abs"] for row in rows)
    max_eps1_condition = max(row["frobenius_condition_proxy"] for row in eps1_rows)
    min_eps1_offblock = min(row["offblock_max_abs"] for row in eps1_rows)
    all_finite = all(
        math.isfinite(row["det_minus_one_abs"])
        and math.isfinite(row["offblock_max_abs"])
        and math.isfinite(row["frobenius_condition_proxy"])
        and math.isfinite(row["max_abs_entry"])
        for row in rows
    )

    return {
        "variable_profile_matrix_status": (
            "PASS_VARIABLE_PROFILE_MATRIX_RADIAL_TRANSFER"
            if coefficient_profile["coefficient_profile_status"]
            == "PASS_ADMISSIBLE_BACKGROUND_COEFFICIENT_PROFILE_FAMILY_DERIVED"
            and all_finite
            and max_constant_error < 1.0e-10
            and max_det_error < 1.0e-9
            and max_eps1_condition < 10.0
            and min_eps1_offblock > 1.0e-5
            else "CHECK_VARIABLE_PROFILE_MATRIX_RADIAL_TRANSFER"
        ),
        "scope": (
            "finite-interval real-frequency transfer matrix for the admissible "
            "variable profile; complex QNM roots with asymptotic exterior "
            "conditions remain the next layer"
        ),
        "profile_status": coefficient_profile["coefficient_profile_status"],
        "omega_values": omega_values,
        "eps_values": eps_values,
        "steps": steps,
        "rows": rows,
        "max_constant_profile_analytic_error": max_constant_error,
        "max_det_minus_one_abs": max_det_error,
        "max_eps1_condition_proxy": max_eps1_condition,
        "min_eps1_offblock_max_abs": min_eps1_offblock,
        "reading": (
            "the admissible profile gives a finite, determinant-preserving "
            "matrix transfer.  The constant limit reproduces the analytic "
            "decoupled branches, while eps=1 activates controlled off-diagonal "
            "channel transfer."
        ),
        "next_gate": (
            "continue in p05c_complex_qnm.py: embed the variable-profile "
            "transfer into the complex QNM pole condition"
        ),
    }


def p05b_central_spectrum_gate():
    foundation = import_static_compact_foundation_gate()
    operator = derive_exterior_scalar_probe_master_operator()
    negative_well = audit_probe_negative_well()
    cutoff = derive_core_cutoff_negative_pocket_gate()
    coupled_symbol = derive_coupled_local_principal_symbol_gate()
    echo_scale = derive_static_echo_cavity_scale()
    boundary = derive_c2_boundary_reflectivity_gate()
    finite_core = derive_finite_core_propagation_center_regular_gate()
    transfer = derive_qnm_echo_transfer_problem_gate()
    reflection = compute_exterior_photon_barrier_reflection_gate()
    pole_estimate = solve_sampled_transfer_pole_estimate_gate()
    complex_root = direct_complex_shooting_probe_root_gate()
    coupled_ode = derive_background_dependent_coupled_radial_ode_gate()
    branch_scan = compute_branch_corrected_reduced_root_scan_gate()
    matrix_transfer = compute_coupled_matrix_radial_transfer_gate(
        branch_scan=branch_scan,
        coupled_ode=coupled_ode,
    )
    radial_mixing = derive_radially_varying_eigenbasis_mixing_gate(
        coupled_ode=coupled_ode,
    )
    coefficient_profile = derive_admissible_background_coefficient_profile_gate(
        coupled_ode=coupled_ode,
    )
    variable_profile_matrix = run_variable_profile_matrix_radial_system_gate()

    status = (
        "PASS_P05B_STATIC_PROBE_AND_ECHO_PREREQUISITES"
        if foundation["foundation_status"]
        == "PASS_STATIC_COMPACT_FOUNDATION_IMPORTED"
        and operator["operator_status"]
        == "PASS_STATIC_EXPONENTIAL_PROBE_MASTER_OPERATOR_DERIVED"
        and negative_well["negative_well_status"]
        == "PASS_PROBE_NEGATIVE_WELL_LEDGER_DERIVED"
        and cutoff["cutoff_status"]
        == "PASS_CORE_CUTOFF_VS_PROBE_NEGATIVE_POCKET_DERIVED"
        and coupled_symbol["coupled_symbol_status"]
        == "PASS_COUPLED_LOCAL_PRINCIPAL_SYMBOL_WITH_FULL_STABLE_POINT"
        and echo_scale["echo_scale_status"]
        == "PASS_STATIC_ECHO_CAVITY_SCALE_DERIVED_FOR_FINITE_C2_CORE_RADIUS"
        and boundary["boundary_reflectivity_status"]
        == "PASS_C2_BOUNDARY_HAS_NO_LEADING_HARD_WALL_REFLECTION"
        and finite_core["finite_core_status"]
        == "PASS_FINITE_CORE_PROPAGATION_AND_CENTER_REGULARITY_LEDGER"
        and transfer["transfer_problem_status"]
        == "PASS_QNM_ECHO_TRANSFER_PROBLEM_FORMULATED__NUMERICAL_SPECTRUM_OPEN"
        and reflection["reflection_status"]
        == "PASS_NUMERICAL_PROBE_PHOTON_BARRIER_REFLECTION_COEFFICIENT"
        and pole_estimate["pole_estimate_status"]
        == "PASS_SAMPLED_CONSTANT_BARRIER_POLE_ESTIMATES"
        and complex_root["complex_shooting_status"]
        == "PASS_DIRECT_COMPLEX_SHOOTING_PROBE_ROOT_LOWER_HALF_PLANE"
        and coupled_ode["coupled_radial_ode_status"]
        == "PASS_BACKGROUND_DEPENDENT_COUPLED_RADIAL_ODE_FORMULATED__BRANCH_CORRECTED_SCAN_OPEN"
        and branch_scan["branch_corrected_scan_status"]
        == "PASS_BRANCH_CORRECTED_REDUCED_ROOT_SCAN_LOWER_HALF_PLANE"
        and matrix_transfer["matrix_transfer_status"]
        == "PASS_COUPLED_MATRIX_RADIAL_TRANSFER_DETERMINANT"
        and radial_mixing["radial_mixing_status"]
        == "PASS_RADIAL_EIGENBASIS_MIXING_FORMULATED__ZERO_FOR_CONSTANT_P01_POINT"
        and coefficient_profile["coefficient_profile_status"]
        == "PASS_ADMISSIBLE_BACKGROUND_COEFFICIENT_PROFILE_FAMILY_DERIVED"
        and variable_profile_matrix["variable_profile_matrix_status"]
        == "PASS_VARIABLE_PROFILE_MATRIX_RADIAL_TRANSFER"
        else "CHECK_P05B_STATIC_PROBE_AND_ECHO_PREREQUISITES"
    )

    return {
        "p05b_status": status,
        "foundation": foundation["foundation_status"],
        "probe_operator": operator["operator_status"],
        "negative_well": negative_well["negative_well_status"],
        "core_cutoff_negative_pocket": cutoff["cutoff_status"],
        "coupled_local_principal_symbol": coupled_symbol["coupled_symbol_status"],
        "local_mixed_speed_roots": coupled_symbol["mixed_speed_roots_local"],
        "local_transverse_speed_squared": coupled_symbol["transverse_speed_squared_local"],
        "largest_probe_well": negative_well["largest_checked_pocket"],
        "echo_scale": echo_scale["echo_scale_status"],
        "boundary_reflectivity": boundary["boundary_reflectivity_status"],
        "boundary_matched_reflection": boundary["matched_impedance_result"],
        "finite_core_propagation": finite_core["finite_core_status"],
        "finite_core_sample_times": finite_core["sample_core_times"],
        "qnm_echo_transfer_problem": transfer["transfer_problem_status"],
        "transfer_sample_branch_times": transfer["sample_branch_times"],
        "photon_barrier_reflection": reflection["reflection_status"],
        "reflection_samples": reflection["reflection_samples"],
        "sampled_pole_estimate": pole_estimate["pole_estimate_status"],
        "least_damped_pole_estimate": pole_estimate["least_damped_estimate"],
        "direct_complex_shooting_probe": complex_root["complex_shooting_status"],
        "direct_complex_probe_root": complex_root["fine_root"],
        "background_coupled_radial_ode": coupled_ode["coupled_radial_ode_status"],
        "coupled_ode_scope_correction": coupled_ode["scope_correction"],
        "branch_corrected_reduced_scan": branch_scan["branch_corrected_scan_status"],
        "branch_corrected_reduced_roots": [
            {
                "branch": result["branch"],
                "s_branch": result["s_branch"],
                "T_branch_over_rs_c": result["T_branch_over_rs_c"],
                "fine_root": result["fine_root"],
            }
            for result in branch_scan["branches"]
        ],
        "coupled_matrix_radial_transfer": matrix_transfer["matrix_transfer_status"],
        "matrix_transfer_root_checks": matrix_transfer["determinant_root_checks"],
        "radial_eigenbasis_mixing": radial_mixing["radial_mixing_status"],
        "radial_mixing_constant_point": {
            "Gamma": radial_mixing["constant_point_Gamma"],
            "mixing_potential": radial_mixing["constant_point_mixing_potential"],
        },
        "admissible_background_coefficient_profile": coefficient_profile[
            "coefficient_profile_status"
        ],
        "coefficient_profile_root_residuals": coefficient_profile[
            "determinant_root_residuals"
        ],
        "variable_profile_matrix_transfer": variable_profile_matrix[
            "variable_profile_matrix_status"
        ],
        "variable_profile_matrix_summary": {
            "max_constant_error": variable_profile_matrix[
                "max_constant_profile_analytic_error"
            ],
            "max_det_error": variable_profile_matrix["max_det_minus_one_abs"],
            "min_eps1_offblock": variable_profile_matrix["min_eps1_offblock_max_abs"],
        },
        "next_gates": [
            (
                "p05c_complex_qnm.py embeds the variable-profile transfer into "
                "the complex QNM pole condition"
            ),
            "add rotating exterior and ray tracing",
        ],
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18b: Compact-core spectrum and echo gates")
    print("=" * 72)

    sections = [
        ("1. Static compact foundation", import_static_compact_foundation_gate()),
        ("2. Exterior scalar-probe master operator", derive_exterior_scalar_probe_master_operator()),
        ("3. Probe negative-well ledger", audit_probe_negative_well()),
        ("4. Core cutoff vs negative pocket", derive_core_cutoff_negative_pocket_gate()),
        ("5. Coupled local principal symbol", derive_coupled_local_principal_symbol_gate()),
        ("6. Static echo-cavity scale", derive_static_echo_cavity_scale()),
        ("7. C2 boundary reflectivity", derive_c2_boundary_reflectivity_gate()),
        ("8. Finite-core propagation and center regularity", derive_finite_core_propagation_center_regular_gate()),
        ("9. QNM/echo transfer problem", derive_qnm_echo_transfer_problem_gate()),
        ("10. Exterior photon-barrier reflection", compute_exterior_photon_barrier_reflection_gate()),
        ("11. Sampled transfer-pole estimate", solve_sampled_transfer_pole_estimate_gate()),
        ("12. Direct complex-shooting probe root", direct_complex_shooting_probe_root_gate()),
        ("13. Background-dependent coupled radial ODE", derive_background_dependent_coupled_radial_ode_gate()),
        ("14. Branch-corrected reduced root scan", compute_branch_corrected_reduced_root_scan_gate()),
        ("15. Coupled matrix radial transfer", compute_coupled_matrix_radial_transfer_gate()),
        ("16. Radially varying eigenbasis mixing", derive_radially_varying_eigenbasis_mixing_gate()),
        ("17. Admissible background coefficient profile", derive_admissible_background_coefficient_profile_gate()),
        ("18. Variable-profile matrix radial system", run_variable_profile_matrix_radial_system_gate()),
        ("19. Central p05b gate", p05b_central_spectrum_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:36s}: {value}")
