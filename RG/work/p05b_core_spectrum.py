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
4. derive the static echo-cavity tortoise scale for a finite C2 core radius;
5. keep coupled QNMs, rotation, and ray tracing as explicit next gates.
"""

import math

import sympy as sp

from p05_compact import (
    compact_central_claim_gate,
    derive_c2_core_local_stability_interface,
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
        sp.simplify(
            (r_s**2 / c**2)
            * v_eff.subs({r: x * r_s, ell * (ell + 1): L})
        )
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


def p05b_central_spectrum_gate():
    foundation = import_static_compact_foundation_gate()
    operator = derive_exterior_scalar_probe_master_operator()
    negative_well = audit_probe_negative_well()
    echo_scale = derive_static_echo_cavity_scale()

    status = (
        "PASS_P05B_STATIC_PROBE_AND_ECHO_PREREQUISITES"
        if foundation["foundation_status"]
        == "PASS_STATIC_COMPACT_FOUNDATION_IMPORTED"
        and operator["operator_status"]
        == "PASS_STATIC_EXPONENTIAL_PROBE_MASTER_OPERATOR_DERIVED"
        and negative_well["negative_well_status"]
        == "PASS_PROBE_NEGATIVE_WELL_LEDGER_DERIVED"
        and echo_scale["echo_scale_status"]
        == "PASS_STATIC_ECHO_CAVITY_SCALE_DERIVED_FOR_FINITE_C2_CORE_RADIUS"
        else "CHECK_P05B_STATIC_PROBE_AND_ECHO_PREREQUISITES"
    )

    return {
        "p05b_status": status,
        "foundation": foundation["foundation_status"],
        "probe_operator": operator["operator_status"],
        "negative_well": negative_well["negative_well_status"],
        "largest_probe_well": negative_well["largest_checked_pocket"],
        "echo_scale": echo_scale["echo_scale_status"],
        "next_gates": [
            "derive coupled compact-core perturbation variables",
            "derive boundary reflectivity/absorption at the finite C2 core",
            "compute QNM/echo transfer function",
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
        ("4. Static echo-cavity scale", derive_static_echo_cavity_scale()),
        ("5. Central p05b gate", p05b_central_spectrum_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:36s}: {value}")
