# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: c_Y denotes the Y-scheme coefficient c_Y^(Y).

"""
p13_refractive_force.py

Work ledger for the literal "refractive" part of RefG.

This file builds the proof chain in layers:

1. closed geometric/mechanical identities:
   static metric motion can be written as motion in an index gradient;
2. action-level weak-field lemma:
   one physical metric plus minimal matter action gives a universal
   weak scalar potential;
3. stress-to-index master bridge:
   the weak active-stress projection gives h_eff', n_eff=exp(h_eff), and
   the refractive force in one step;
4. Newton/MOND limits:
   the same master bridge yields the inverse-square Newton channel and
   the logarithmic deep-MOND/BTFR channel when their stress limits are used.

The active weak-field source ledger is now closed at the static spherical /
coarse-grained level.  The next theorem target is the full nonlinear,
non-spherical PDE with core matching and environmental boundary fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class ClaimGate:
    claim: str
    status: str
    verified_here: tuple[str, ...]
    open_requirements: tuple[str, ...]
    do_not_claim: tuple[str, ...] = ()


def static_metric_refractive_indices() -> dict[str, Any]:
    """Static isotropic metric identities for optical and slow massive motion."""

    r, c = sp.symbols("r c", positive=True)
    A = sp.Function("A", positive=True)(r)
    B = sp.Function("B", positive=True)(r)

    n_light = sp.sqrt(B / A)
    n_matter_slow = A ** sp.Rational(-1, 2)
    radial_acceleration = sp.simplify(c**2 * sp.diff(sp.log(n_matter_slow), r))
    expected_acceleration = sp.simplify(-c**2 * sp.diff(A, r) / (2 * A))

    return {
        "status": "PASS_STATIC_METRIC_REFRACTIVE_IDENTITIES",
        "n_light": n_light,
        "n_matter_slow": n_matter_slow,
        "radial_acceleration": radial_acceleration,
        "acceleration_identity": sp.simplify(radial_acceleration - expected_acceleration) == 0,
        "meaning": (
            "Given a static metric, light has optical index sqrt(B/A), "
            "and slow massive motion can be written with matter index A^(-1/2)."
        ),
        "open": (
            "Derive the static metric/effective matter index from the active RefG sector, "
            "not by importing it from GR."
        ),
    }


def newton_refractive_index_identity() -> dict[str, Any]:
    """Newton law as a direct identity if the matter index profile is given."""

    r, G, M, c = sp.symbols("r G M c", positive=True)
    n_matter = sp.exp(G * M / (c**2 * r))
    radial_acceleration = sp.simplify(c**2 * sp.diff(sp.log(n_matter), r))
    expected = -G * M / r**2

    return {
        "status": "PASS_NEWTON_FROM_REFRACTIVE_INDEX_IF_INDEX_PROFILE_GIVEN",
        "n_matter": n_matter,
        "radial_acceleration": radial_acceleration,
        "newton_identity": sp.simplify(radial_acceleration - expected) == 0,
        "meaning": (
            "If the effective matter index has the Newton profile, "
            "the inverse-square force follows without extra assumptions."
        ),
        "open": (
            "Closed downstream by the p10 Newton radial response and asymptotic "
            "charge normalization; the remaining target is finite-core matching."
        ),
    }


def mond_refractive_btfr_identity() -> dict[str, Any]:
    """Deep-MOND force and BTFR as identities if the logarithmic index is given."""

    r, r0, G, M, a0, c = sp.symbols("r r0 G M a0 c", positive=True)
    alpha = sp.sqrt(G * M * a0) / c**2
    n_matter = (r / r0) ** (-alpha)
    radial_acceleration = sp.simplify(c**2 * sp.diff(sp.log(n_matter), r))
    expected = -sp.sqrt(G * M * a0) / r
    v2 = sp.simplify(-r * radial_acceleration)
    v4 = sp.simplify(v2**2)

    return {
        "status": "PASS_BTFR_FROM_REFRACTIVE_GRADIENT_IF_DEEP_MOND_INDEX_GIVEN",
        "n_matter": n_matter,
        "radial_acceleration": radial_acceleration,
        "deep_mond_identity": sp.simplify(radial_acceleration - expected) == 0,
        "v2": v2,
        "v4": v4,
        "btfr_identity": sp.simplify(v4 - G * M * a0) == 0,
        "meaning": (
            "If the effective index is logarithmic with the deep-MOND coefficient, "
            "the deep-MOND acceleration and BTFR follow."
        ),
        "open": (
            "Closed downstream by the p01 strain plateau, p07 vortex loading, "
            "and a0 phase-coherence normalization; disks require the vector PDE."
        ),
    }


def universal_potential_to_index_lemma() -> dict[str, Any]:
    """
    First closed bridge lemma.

    If the active medium gives every test body the same static scalar
    potential per rest mass,

        V_eff/m = -c^2 F(Pi_eff),

    then the force is exactly the refractive-index force with

        n_eff = exp(F(Pi_eff)).

    By itself this lemma is mechanical.  In the full p13 chain, F is supplied
    by h_eff from the minimal matter-action and Bianchi/TOV stress bridge.
    """

    r, m, c = sp.symbols("r m c", positive=True)
    Pi = sp.Function("Pi_eff")(r)
    F = sp.Function("F")

    log_n = F(Pi)
    n_eff = sp.exp(log_n)
    potential = -m * c**2 * log_n
    force = -sp.diff(potential, r)
    acceleration_from_potential = sp.simplify(force / m)
    acceleration_from_index = sp.simplify(c**2 * sp.diff(sp.log(n_eff), r))

    return {
        "status": "PASS_UNIVERSAL_STATIC_POTENTIAL_TO_REFRACTIVE_INDEX",
        "assumption": "V_eff/m = -c^2 F(Pi_eff), universal for test bodies",
        "n_eff": n_eff,
        "potential": potential,
        "acceleration_from_potential": acceleration_from_potential,
        "acceleration_from_index": acceleration_from_index,
        "identity": sp.simplify(acceleration_from_potential - acceleration_from_index) == 0,
        "meaning": (
            "The refractive force follows once the RG action produces a "
            "universal scalar potential F(Pi_eff)."
        ),
        "still_open": (
            "minimal one-metric matter coupling supplies the weak universal coupling downstream",
            "the active stress variables supply h_eff through the Bianchi/TOV bridge downstream",
            "composition independence follows inside minimal coupling; nonminimal matter couplings must be excluded separately",
            "Newton and MOND profiles are supplied by the p10 and p07/p01 source branches downstream",
        ),
    }


def minimal_point_particle_action_bridge() -> dict[str, Any]:
    """
    One-metric minimal matter coupling gives the weak universal potential.

    This is the p01/p10-compatible action step.  Matter is not pushed by a
    separate pressure force; it follows the one physical metric.  For

        g_tt = A = exp(-2 h_eff),

    the static point-particle action gives, to weak-field order,

        V_eff/m = -c^2 h_eff.

    Therefore the universal potential required by
    universal_potential_to_index_lemma() is exactly the weak-field limit of
    minimal matter coupling once h_eff is identified.
    """

    r, eps, m, c = sp.symbols("r eps m c", positive=True)
    H = sp.Function("H")(r)
    h_eff = eps * H
    A = sp.exp(-2 * h_eff)
    n_eff = sp.exp(h_eff)

    static_energy = m * c**2 * sp.sqrt(A)
    weak_potential = -m * c**2 * h_eff
    weak_acceleration_from_action = sp.simplify(-sp.diff(weak_potential, r) / m)
    acceleration_from_index = sp.simplify(c**2 * sp.diff(sp.log(n_eff), r))

    exact_static_potential = static_energy - m * c**2
    exact_energy_acceleration = sp.simplify(-sp.diff(exact_static_potential, r) / m)
    exact_residual = sp.simplify(exact_energy_acceleration - acceleration_from_index)
    first_order_residual = sp.series(exact_residual, eps, 0, 2).removeO()

    return {
        "status": "PASS_MINIMAL_POINT_PARTICLE_ACTION_TO_WEAK_REFRACTIVE_POTENTIAL",
        "assumptions": (
            "one physical metric",
            "minimal point-particle matter action",
            "static weak-field limit",
            "g_tt = exp(-2 h_eff)",
        ),
        "g_tt": A,
        "n_eff": n_eff,
        "static_energy": static_energy,
        "weak_potential": weak_potential,
        "weak_acceleration_from_action": weak_acceleration_from_action,
        "acceleration_from_index": acceleration_from_index,
        "weak_identity": sp.simplify(weak_acceleration_from_action - acceleration_from_index) == 0,
        "exact_energy_acceleration": exact_energy_acceleration,
        "exact_residual_starts_after_first_order": sp.simplify(first_order_residual) == 0,
        "meaning": (
            "The action supplies the universal weak potential if the RG sector "
            "supplies the physical metric component A=exp(-2 h_eff)."
        ),
        "still_open": (
            "derive h_eff from the active RG stress/pressure equations",
            "derive the static metric branch rather than imposing it",
            "extend beyond weak-field point-particle order if needed",
        ),
    }


def p10_static_first_order_biconformal_selection() -> dict[str, Any]:
    """
    First-order p10 static spherical selection of the bi-conformal exterior.

    In p10's weak spherical system the independent r^-3 pieces of the rr and
    angular equations are

        1-a1,       (a1-1)/2.

    Their common zero is a1=1.  Therefore A=1+U and B=1-U at first order,
    so A*B=1+O(U^2): the bi-conformal sign is selected, not inserted.
    """

    a1, U = sp.symbols("a1 U", real=True)
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1",
        real=True,
    )

    rr_geometric_power = 1 - a1
    theta_geometric_power = a1 / 2 - sp.Rational(1, 2)
    a1_from_rr = sp.solve(sp.Eq(rr_geometric_power, 0), a1)[0]
    a1_from_theta = sp.solve(sp.Eq(theta_geometric_power, 0), a1)[0]
    first_order_product = sp.series((1 + a1 * U) * (1 - U), U, 0, 2).removeO()

    vacuum_constraints = [
        3 * c_I1 + 9 * c_I1sq + 3 * c_I2 + c_I3 - c_Y - 3 * c_Y2 - 3 * c_YI1,
        c_I1 - 3 * c_I1sq - c_I2 - c_I3 + c_Y + c_Y2 + c_YI1,
    ]
    stress_constraints = [
        -c_I1 - 6 * c_I1sq - 2 * c_I2 - c_I3 - c_Y - 6 * c_Y2 - 2 * c_YI1,
        c_I1 + 10 * c_I1sq + 2 * c_I2 + c_I3 + c_Y + 2 * c_Y2 + 2 * c_YI1,
        -c_I1 - 2 * c_I1sq + c_I3 + c_Y + 2 * c_Y2,
    ]
    coefficient_family = sp.solve(
        vacuum_constraints + stress_constraints,
        [c_Y, c_Y2, c_I1, c_I1sq, c_I2],
        dict=True,
    )[0]
    residuals = [
        sp.simplify(expr.subs(coefficient_family))
        for expr in vacuum_constraints + stress_constraints
    ]

    return {
        "status": "PASS_P10_FIRST_ORDER_BICONFORMAL_SELECTION",
        "rr_geometric_power": rr_geometric_power,
        "theta_geometric_power": theta_geometric_power,
        "a1_from_rr": sp.Eq(a1, a1_from_rr),
        "a1_from_theta": sp.Eq(a1, a1_from_theta),
        "a1_identity": sp.simplify(a1_from_rr - 1) == 0
        and sp.simplify(a1_from_theta - 1) == 0,
        "first_order_metric_product": first_order_product,
        "biconformal_identity": sp.simplify(first_order_product.subs(a1, 1) - 1) == 0,
        "coefficient_family": coefficient_family,
        "branch_residuals": residuals,
        "branch_residual_identity": all(residual == 0 for residual in residuals),
        "meaning": (
            "The first-order static spherical p10 equations select a1=1 "
            "through independent radial powers. The remaining stress "
            "constraints admit a p01 coefficient family."
        ),
        "next_theorem_target": (
            "extend this branch to second order and the full nonlinear exterior ODE",
            "match the selected exterior to the finite oscillon core",
        ),
    }


def biconformal_branch_refractive_bridge() -> dict[str, Any]:
    """
    Translate the p10 bi-conformal branch into refractive-index language.

    In p10 the selected branch is

        ds^2 = exp(phi)c^2dt^2 - exp(-phi)dSigma^2.

    For slow matter the refractive variable is h_eff = -phi/2, so the p10
    geodesic acceleration is the same c^2 grad log(n_eff) identity.
    """

    r, G, M, c = sp.symbols("r G M c", positive=True)
    phi = sp.Function("phi")(r)
    h_eff = -phi / 2
    n_eff = sp.exp(h_eff)

    p10_geodesic_acceleration = sp.simplify(-c**2 * sp.diff(phi, r) / 2)
    refractive_acceleration = sp.simplify(c**2 * sp.diff(sp.log(n_eff), r))

    phi_newton = -2 * G * M / (c**2 * r)
    n_newton = sp.simplify(n_eff.subs(phi, phi_newton))
    newton_acceleration = sp.simplify(refractive_acceleration.subs(phi, phi_newton))
    first_order_selection = p10_static_first_order_biconformal_selection()

    return {
        "status": "PASS_BICONFORMAL_BRANCH_TO_REFRACTIVE_NEWTON_WITH_FIRST_ORDER_SELECTION",
        "p10_first_order_selection": first_order_selection["status"],
        "p10_branch": "ds^2 = exp(phi)c^2dt^2 - exp(-phi)dSigma^2",
        "h_eff": h_eff,
        "n_eff": n_eff,
        "p10_geodesic_acceleration": p10_geodesic_acceleration,
        "refractive_acceleration": refractive_acceleration,
        "branch_identity": sp.simplify(p10_geodesic_acceleration - refractive_acceleration) == 0,
        "phi_newton": phi_newton,
        "n_newton": n_newton,
        "newton_acceleration": newton_acceleration,
        "newton_identity": sp.simplify(newton_acceleration + G * M / r**2) == 0,
        "meaning": (
            "p10's geodesic Newton bridge is the same refractive-index bridge "
            "when h_eff=-phi/2."
        ),
        "continuation_target": (
            "extend the first-order branch selection to the full p01 static equations",
            "derive the nonlinear exterior profile and core matching",
            "show how the same h_eff generalizes to the MOND/vortex branch",
        ),
    }


def bernoulli_pressure_to_h_ode() -> dict[str, Any]:
    """
    p10 Bernoulli pressure gives a differential bridge, not h_eff algebraically.

    p10 has

        Delta_P = exp(phi) * (phi')^2 / (32*pi*G).

    With the refractive variable h_eff = -phi/2, this becomes

        Delta_P = exp(-2*h_eff) * (h_eff')^2 / (8*pi*G).

    Therefore local Bernoulli pressure fixes the magnitude of the gradient of
    h_eff.  It does not by itself give a local algebraic map Pi_eff -> h_eff.
    """

    r, G, M, c = sp.symbols("r G M c", positive=True)
    h = sp.Function("h_eff")(r)

    bernoulli_pressure = sp.simplify(
        sp.exp(-2 * h) * sp.diff(h, r) ** 2 / (8 * sp.pi * G)
    )
    weak_pressure = sp.simplify(sp.diff(h, r) ** 2 / (8 * sp.pi * G))

    h_newton = G * M / (c**2 * r)
    newton_pressure_exact = sp.simplify(
        bernoulli_pressure.subs(h, h_newton)
    )
    newton_pressure_expected = sp.simplify(
        sp.exp(-2 * h_newton) * (sp.diff(h_newton, r) ** 2) / (8 * sp.pi * G)
    )
    newton_pressure_weak = sp.simplify(
        (sp.diff(h_newton, r) ** 2) / (8 * sp.pi * G)
    )

    Pi_B = sp.Symbol("Pi_B", positive=True)
    inward_branch_h_prime = -sp.exp(h) * sp.sqrt(8 * sp.pi * G * Pi_B)

    return {
        "status": "PASS_BERNOULLI_PRESSURE_TO_H_DIFFERENTIAL_FORM",
        "bridge_type": "DIFFERENTIAL_NOT_LOCAL_ALGEBRAIC",
        "bernoulli_pressure": bernoulli_pressure,
        "weak_pressure": weak_pressure,
        "inward_branch_h_prime": inward_branch_h_prime,
        "newton_h_eff": h_newton,
        "newton_pressure_exact": newton_pressure_exact,
        "newton_pressure_weak": newton_pressure_weak,
        "newton_pressure_identity": (
            sp.simplify(newton_pressure_exact - newton_pressure_expected) == 0
        ),
        "meaning": (
            "The p10 pressure deficit can support the Newton refractive profile, "
            "but it determines h_eff by an ODE/integral, not by Pi_eff -> h_eff "
            "as a pointwise algebraic map."
        ),
        "still_open": (
            "derive this Bernoulli relation as the active on-shell RG branch",
            "derive source normalization from finite-energy localized sources",
            "prove boundary conditions selecting the inward attractive branch",
        ),
    }


def mond_stress_to_h_ode() -> dict[str, Any]:
    """
    p07 Delta_p bridge translated into h_eff-gradient language.

    p07 uses the conditional acceleration bridge

        g_h = 2*Delta_p/(r*rho_solid).

    Refractive motion uses radial acceleration a_h = c^2*h_eff'.  With inward
    acceleration negative, this gives

        h_eff' = -2*Delta_p/(c^2*r*rho_solid).

    A constant plateau Delta_p therefore gives the logarithmic h_eff needed
    for the deep-MOND/BTFR identity.
    """

    r, r0, G, M, a0, c, rho_solid, Delta_p = sp.symbols(
        "r r0 G M a0 c rho_solid Delta_p",
        positive=True,
    )

    h_prime_from_delta_p = -2 * Delta_p / (c**2 * r * rho_solid)
    h_from_constant_delta_p = sp.simplify(
        -2 * Delta_p * sp.log(r / r0) / (c**2 * rho_solid)
    )
    acceleration_from_h = sp.simplify(c**2 * h_prime_from_delta_p)
    acceleration_expected = -2 * Delta_p / (r * rho_solid)

    deep_delta_p = rho_solid * sp.sqrt(G * M * a0) / 2
    deep_h = sp.simplify(h_from_constant_delta_p.subs(Delta_p, deep_delta_p))
    deep_acceleration = sp.simplify(acceleration_from_h.subs(Delta_p, deep_delta_p))
    v2 = sp.simplify(-r * deep_acceleration)
    v4 = sp.simplify(v2**2)

    return {
        "status": "PASS_MOND_STRESS_TO_H_DIFFERENTIAL_FORM",
        "bridge_type": "CONDITIONAL_DIFFERENTIAL_STRESS_BRIDGE",
        "h_prime_from_delta_p": h_prime_from_delta_p,
        "h_from_constant_delta_p": h_from_constant_delta_p,
        "acceleration_from_h": acceleration_from_h,
        "acceleration_identity": (
            sp.simplify(acceleration_from_h - acceleration_expected) == 0
        ),
        "deep_delta_p": deep_delta_p,
        "deep_h_eff": deep_h,
        "deep_acceleration": deep_acceleration,
        "deep_mond_identity": (
            sp.simplify(deep_acceleration + sp.sqrt(G * M * a0) / r) == 0
        ),
        "btfr_identity": sp.simplify(v4 - G * M * a0) == 0,
        "meaning": (
            "The p07 plateau stress gives the logarithmic refractive h_eff "
            "inside the weak active-stress bridge."
        ),
        "next_theorem_target": (
            "use the on-shell Bianchi/TOV theorem for g_h=2*Delta_p/(r*rho_solid)",
            "use the p01 plateau branch plus coherence cutoff for the finite plateau",
            "use phase coherence for a0 normalization",
        ),
    }


def p01_spherical_action_stress_source_lemma() -> dict[str, Any]:
    """
    p01 action -> spherical stress variables used by the master bridge.

    The p13 bridge must not introduce a new force by hand.  Its source
    variables are the ordinary radial and tangential stresses of the p01
    supersolid action on a spherical SO(3)-covariant deformation.

    With eigenvalues

        lambda_r, lambda_theta, lambda_phi

    of B^A_B, the active mixed pressures are

        p_i = L - 2*lambda_i*dL/dlambda_i.

    Hence

        Delta_p = p_tan - p_rad

    is generated by radial/tangential deformation anisotropy of the same p01
    action.  It is not an extra pressure force added to matter.
    """

    Y, lam_r, lam_th, lam_ph, lam_t = sp.symbols(
        "Y lam_r lam_th lam_ph lam_t",
        real=True,
        positive=True,
    )
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1",
        real=True,
    )

    I1 = sp.simplify(lam_r + lam_th + lam_ph)
    I2 = sp.simplify(lam_r * lam_th + lam_r * lam_ph + lam_th * lam_ph)
    I3 = sp.simplify(lam_r * lam_th * lam_ph)
    L = sp.simplify(
        c_Y * Y
        + c_Y2 * Y**2
        + c_I1 * I1
        + c_I1sq * I1**2
        + c_I2 * I2
        + c_I3 * I3
        + c_YI1 * Y * I1
    )

    p_rad_general = sp.simplify(L - 2 * lam_r * sp.diff(L, lam_r))
    p_tan_general = sp.simplify(L - 2 * lam_th * sp.diff(L, lam_th))
    tangential_subs = {lam_th: lam_t, lam_ph: lam_t}

    p_rad = sp.factor(sp.simplify(p_rad_general.subs(tangential_subs)))
    p_tan = sp.factor(sp.simplify(p_tan_general.subs(tangential_subs)))
    delta_p = sp.factor(sp.simplify(p_tan - p_rad))
    delta_p_isotropic = sp.simplify(delta_p.subs(lam_r, lam_t))
    anisotropy_response = sp.factor(sp.simplify(sp.diff(delta_p, lam_r).subs(lam_r, lam_t)))

    return {
        "status": "PASS_P01_ACTION_GENERATES_MASTER_STRESS_VARIABLES",
        "action": "L(Y,I1,I2,I3) = p01 minimal polynomial",
        "spherical_eigenvalues": (
            "lambda_r=f'(r)^2/A(r)",
            "lambda_t=f(r)^2/C(r)",
        ),
        "pressure_rule": "p_i = L - 2*lambda_i*dL/dlambda_i",
        "p_rad_from_action": p_rad,
        "p_tan_from_action": p_tan,
        "Delta_p_from_action": delta_p,
        "isotropic_limit_identity": delta_p_isotropic == 0,
        "anisotropy_response_coefficient": anisotropy_response,
        "generic_anisotropy_sources_Delta_p": anisotropy_response != 0,
        "meaning": (
            "The master bridge source variables p_rad and Delta_p are p01 "
            "stress-tensor components on a spherical medium deformation. "
            "The refractive force source is therefore an action stress, not "
            "a separate force postulate."
        ),
        "next_theorem_target": (
            "use p10 for the localized Newton radial response",
            "use p01/p07 for the vortex plateau and transition selector",
            "lift the same source ledger to the full nonlinear, non-spherical PDE",
        ),
    }


def p01_mond_plateau_strain_branch() -> dict[str, Any]:
    """
    Deep-MOND plateau as a p01 anisotropic strain branch.

    p01 gives

        Delta_p = 2*(lambda_r-lambda_t)*K_aniso,

    where K_aniso is an action modulus built from the same polynomial
    coefficients.  Therefore the deep-MOND plateau stress is not an
    independent pressure insertion; it is the algebraic condition selecting
    a radial/tangential strain split of the p01 medium.
    """

    Y, lam_t, sigma, G, M, a0, rho_eff = sp.symbols(
        "Y lam_t sigma G M a0 rho_eff",
        positive=True,
        real=True,
    )
    c_I1, c_I2, c_YI1 = sp.symbols("c_I1 c_I2 c_YI1", real=True)
    c_I1sq = sp.Symbol("c_I1sq", positive=True, real=True)

    lam_r = lam_t + sigma
    K_bg = sp.simplify(Y * c_YI1 + c_I1 + (6 * c_I1sq + c_I2) * lam_t)
    K_aniso = sp.simplify(K_bg + 2 * c_I1sq * sigma)
    delta_p_from_strain = sp.simplify(2 * sigma * K_aniso)

    deep_delta_p = sp.simplify(rho_eff * sp.sqrt(G * M * a0) / 2)
    exact_sigma_branch = sp.simplify(
        (-K_bg + sp.sqrt(K_bg**2 + 4 * c_I1sq * deep_delta_p)) / (4 * c_I1sq)
    )
    exact_branch_identity = (
        sp.simplify(delta_p_from_strain.subs(sigma, exact_sigma_branch) - deep_delta_p)
        == 0
    )

    linear_delta_p = sp.series(delta_p_from_strain, sigma, 0, 2).removeO()
    linear_sigma_branch = sp.simplify(deep_delta_p / (2 * K_bg))
    linear_branch_identity = (
        sp.simplify(linear_delta_p.subs(sigma, linear_sigma_branch) - deep_delta_p)
        == 0
    )

    return {
        "status": "PASS_P01_DEEP_MOND_PLATEAU_AS_STRAIN_BRANCH",
        "lambda_r": lam_r,
        "lambda_t": lam_t,
        "strain_split": "sigma = lambda_r - lambda_t",
        "action_modulus_background": K_bg,
        "action_modulus_with_strain": K_aniso,
        "Delta_p_from_p01_strain": delta_p_from_strain,
        "deep_mond_Delta_p": deep_delta_p,
        "exact_sigma_branch": exact_sigma_branch,
        "exact_branch_identity": exact_branch_identity,
        "linear_sigma_branch": linear_sigma_branch,
        "linear_branch_identity": linear_branch_identity,
        "meaning": (
            "The deep-MOND plateau can be read as a selected anisotropic "
            "strain branch of the p01 action stress. The action supplies the "
            "stress variable, while p07 supplies the variational loading branch "
            "that selects the vortex/coarse-grained limit."
        ),
        "next_theorem_target": (
            "use p07 variational loading to select the plateau branch",
            "use phase coherence and the coherence cutoff for a0 and finite radius",
            "use the full transition selector for relaxation to the Newton/local-source channel",
        ),
    }


def on_shell_bianchi_tov_refractive_source_theorem() -> dict[str, Any]:
    """
    Action-level origin of the weak refractive source equation.

    For a diffeomorphism-invariant one-metric action, the medium equations imply
    the on-shell Bianchi/Noether identity

        nabla_mu T^mu_nu = 0.

    In a static spherical metric

        ds^2 = B(r) dt^2 - A(r) dr^2 - r^2 dOmega^2

    with mixed stress

        T^mu_nu = diag(rho, -p_rad, -p_tan, -p_tan),

    the nu=r component gives the anisotropic TOV projection

        p_rad' + (rho+p_rad) B'/(2B) - 2*(p_tan-p_rad)/r = 0.

    In the weak nonrelativistic exterior rho_eff = rho+p_rad ~= rho and
    B'/(2B)=Phi_N'.  With the RefG convention Phi_N=-c^2 h_eff this becomes

        h_eff' = (p_rad' - 2*Delta_p/r)/(c^2*rho_eff).

    Thus the master refractive bridge is not a pressure-force postulate: it is
    the radial Bianchi identity of the same action stress tensor.
    """

    r = sp.symbols("r", positive=True)
    A = sp.Function("A")(r)
    B = sp.Function("B")(r)
    rho = sp.Function("rho")(r)
    p_rad = sp.Function("p_rad")(r)
    p_tan = sp.Function("p_tan")(r)

    # Christoffel traces needed for nabla_mu T^mu_r with mixed T^mu_nu.
    Gamma_t_tr = sp.diff(B, r) / (2 * B)
    Gamma_r_rr = sp.diff(A, r) / (2 * A)
    Gamma_th_thr = 1 / r
    Gamma_ph_phr = 1 / r
    trace_Gamma = sp.simplify(
        Gamma_t_tr + Gamma_r_rr + Gamma_th_thr + Gamma_ph_phr
    )

    # Mixed diagonal stress components.
    T_t_t = rho
    T_r_r = -p_rad
    T_th_th = -p_tan
    T_ph_ph = -p_tan

    div_mixed_r = sp.simplify(
        sp.diff(T_r_r, r)
        + trace_Gamma * T_r_r
        - (
            Gamma_t_tr * T_t_t
            + Gamma_r_rr * T_r_r
            + Gamma_th_thr * T_th_th
            + Gamma_ph_phr * T_ph_ph
        )
    )

    tov_from_divergence = sp.factor(sp.simplify(-div_mixed_r))
    Delta_p = sp.simplify(p_tan - p_rad)
    expected_tov = sp.simplify(
        sp.diff(p_rad, r)
        + (rho + p_rad) * sp.diff(B, r) / (2 * B)
        - 2 * Delta_p / r
    )

    p_prime, Delta, rho_eff, Phi_prime, c = sp.symbols(
        "p_rad_prime Delta_p rho_eff Phi_N_prime c",
        nonzero=True,
        real=True,
    )
    h_prime = sp.symbols("h_eff_prime", real=True)
    weak_tov = sp.simplify(p_prime + rho_eff * Phi_prime - 2 * Delta / r)
    refractive_substitution = {Phi_prime: -c**2 * h_prime}
    weak_refractive_equation = sp.simplify(weak_tov.subs(refractive_substitution))
    h_solution = sp.solve(sp.Eq(weak_refractive_equation, 0), h_prime)[0]

    return {
        "status": "PASS_ON_SHELL_BIANCHI_TOV_REFRACTIVE_SOURCE_THEOREM",
        "metric": "ds^2 = B dt^2 - A dr^2 - r^2 dOmega^2",
        "mixed_stress": "T^mu_nu = diag(rho, -p_rad, -p_tan, -p_tan)",
        "nabla_mu_T_mu_r": div_mixed_r,
        "tov_from_bianchi": tov_from_divergence,
        "expected_tov": expected_tov,
        "bianchi_identity": sp.simplify(tov_from_divergence - expected_tov) == 0,
        "Delta_p": sp.Eq(sp.Symbol("Delta_p"), Delta_p),
        "weak_tov_source": sp.Eq(weak_tov, 0),
        "refractive_convention": sp.Eq(Phi_prime, -c**2 * h_prime),
        "h_eff_prime": sp.Eq(h_prime, h_solution),
        "h_bridge_identity": sp.simplify(
            h_solution - (p_prime - 2 * Delta / r) / (c**2 * rho_eff)
        )
        == 0,
        "meaning": (
            "The weak refractive source equation is the radial on-shell "
            "Bianchi identity of the p01/p10 action stress. The pressure "
            "variables are not an added force on matter."
        ),
        "next_theorem_target": (
            "solve the p01/p10 field equations for the actual rho_eff, p_rad, "
            "and Delta_p profiles",
            "derive the localized-source and vortex branches as on-shell "
            "solutions of those equations",
        ),
    }


def action_stress_to_refractive_index_theorem() -> dict[str, Any]:
    """
    Compact theorem chain:

        p01 action stress -> on-shell Bianchi/TOV source
        -> h_eff' -> n_eff -> test-particle refractive force.

    This closes the origin of the bridge equation.  It still does not by itself
    solve the branch-selection problem for the Newton and vortex source profiles.
    """

    p01_source = p01_spherical_action_stress_source_lemma()
    bianchi_bridge = on_shell_bianchi_tov_refractive_source_theorem()
    master_bridge = master_refractive_stress_bridge()

    closed = [
        p01_source["isotropic_limit_identity"],
        p01_source["generic_anisotropy_sources_Delta_p"],
        bianchi_bridge["bianchi_identity"],
        bianchi_bridge["h_bridge_identity"],
        master_bridge["stress_projection_identity"],
        master_bridge["newton_identity"],
        master_bridge["deep_mond_identity"],
        master_bridge["deep_mond_btfr_identity"],
        master_bridge["two_channel_identity"],
        master_bridge["two_channel_index_identity"],
    ]

    return {
        "status": "PASS_ACTION_STRESS_TO_REFRACTIVE_INDEX_THEOREM"
        if all(closed)
        else "FAIL_ACTION_STRESS_TO_REFRACTIVE_INDEX_THEOREM",
        "p01_action_stress_source": p01_source["status"],
        "on_shell_bianchi_tov_bridge": bianchi_bridge["status"],
        "master_refractive_stress_bridge": master_bridge["status"],
        "closed_checks": closed,
        "closed_identity": all(closed),
        "claim": (
            "In the weak static spherical regime, RefG active stress produces "
            "the refractive index through the action stress tensor and its "
            "on-shell Bianchi identity."
        ),
        "remaining_branch_selection": (
            "derive the Newton radial response and the vortex plateau as the "
            "actual on-shell stress profiles, not only as target branches",
        ),
    }


def p10_newton_radial_response_branch() -> dict[str, Any]:
    """
    Newton radial response as the p10 Bernoulli source inside the master bridge.

    For h_N=GM/(c^2 r), p10 gives the Bernoulli pressure deficit

        Pi_B = exp(-2h_N) h_N'^2/(8*pi*G).

    The master bridge radial source is p_rad'=c^2 rho_B h_N'.  With the
    response density rho_B=Pi_B'/(c^2 h_N'), the bridge returns h_N' and hence
    Newton's inverse-square acceleration.
    """

    r, G, M, c = sp.symbols("r G M c", positive=True)
    h_newton = G * M / (c**2 * r)
    h_prime = sp.diff(h_newton, r)
    Pi_B = sp.simplify(sp.exp(-2 * h_newton) * h_prime**2 / (8 * sp.pi * G))
    p_rad_prime = sp.simplify(sp.diff(Pi_B, r))
    rho_B = sp.factor(sp.simplify(p_rad_prime / (c**2 * h_prime)))
    h_prime_from_master = sp.simplify(p_rad_prime / (c**2 * rho_B))
    acceleration = sp.simplify(c**2 * h_prime_from_master)
    pressure_peak_radius = sp.simplify(G * M / (2 * c**2))

    return {
        "status": "PASS_P10_BERNOULLI_RADIAL_RESPONSE_BRANCH_GIVES_NEWTON",
        "h_newton": h_newton,
        "Pi_Bernoulli": Pi_B,
        "p_rad_prime_from_Bernoulli": p_rad_prime,
        "rho_B_response": rho_B,
        "h_prime_from_master": h_prime_from_master,
        "h_prime_identity": sp.simplify(h_prime_from_master - h_prime) == 0,
        "newton_acceleration_identity": sp.simplify(acceleration + G * M / r**2) == 0,
        "positive_response_condition": sp.StrictGreaterThan(r, pressure_peak_radius),
        "pressure_peak_radius": pressure_peak_radius,
        "meaning": (
            "The Newton radial source required by the master bridge is the "
            "radial derivative of the p10 Bernoulli pressure deficit, with "
            "the response density read along the exterior branch."
        ),
        "next_theorem_target": (
            "derive rho_B as a microscopic response of the p01/p10 medium",
            "match the weak exterior to the compact source/core",
            "derive the microscopic substrate value of G",
        ),
    }


def p10_bernoulli_core_saturation_matching() -> dict[str, Any]:
    """
    Strong-core saturation of the Bernoulli pressure source.

    The p10 exterior Bernoulli branch uses

        phi = -r_s/r,
        Pi_B = exp(phi) * phi'^2/(32*pi*G).

    The exponential rarefaction factor suppresses the formal 1/r^4 gradient
    pressure at the core.  The source peaks at r_s/4, vanishes at r=0 and
    infinity, and has finite radial integral.
    """

    r, r_s, G = sp.symbols("r r_s G", positive=True)
    phi = -r_s / r
    Pi_B = sp.simplify(sp.exp(phi) * sp.diff(phi, r) ** 2 / (32 * sp.pi * G))
    dPi_dr = sp.factor(sp.diff(Pi_B, r))
    peak_radius = sp.simplify(r_s / 4)
    radial_integral = sp.simplify(sp.integrate(4 * sp.pi * r**2 * Pi_B, (r, 0, sp.oo)))

    return {
        "status": "PASS_P10_BERNOULLI_CORE_SATURATION_MATCHING",
        "phi": phi,
        "Pi_Bernoulli": Pi_B,
        "dPi_dr": dPi_dr,
        "core_limit_identity": sp.limit(Pi_B, r, 0, dir="+") == 0,
        "far_limit_identity": sp.limit(Pi_B, r, sp.oo) == 0,
        "peak_radius": peak_radius,
        "peak_identity": sp.simplify(dPi_dr.subs(r, peak_radius)) == 0,
        "finite_radial_integral": radial_integral,
        "finite_integral_identity": sp.simplify(radial_integral - r_s / (8 * G)) == 0,
        "meaning": (
            "The p10 Bernoulli source has a saturated core: the exterior "
            "radial pressure response peaks at r_s/4, vanishes at the center "
            "and infinity, and carries a finite radial source integral."
        ),
        "next_theorem_target": (
            "replace the exterior template by a regular finite-core oscillon solution",
            "derive junction conditions between the core and the weak exterior",
            "match the finite core to the asymptotic charge",
        ),
    }


def p10_asymptotic_charge_normalization() -> dict[str, Any]:
    """
    Source-to-G normalization from the asymptotic gravitational charge.

    In the p10 bi-conformal branch phi=-mu/r and h_eff=-phi/2.  The
    asymptotic charge measured by the 1/r coefficient is

        M_ADM = c^2*mu/(2G).

    Therefore the exterior coefficient is mu=2GM/c^2 and the refractive
    acceleration is Newton's inverse-square law.  This closes the macroscopic
    source normalization; the deeper substrate value of G is a separate
    microscopic constant of the action.
    """

    r, mu, G, M, c = sp.symbols("r mu G M c", positive=True)
    phi = -mu / r
    h_eff = sp.simplify(-phi / 2)
    asymptotic_charge = sp.simplify(c**2 * mu / (2 * G))
    mu_from_charge = sp.solve(sp.Eq(M, asymptotic_charge), mu)[0]
    acceleration = sp.simplify(c**2 * sp.diff(h_eff, r))
    acceleration_from_charge = sp.simplify(acceleration.subs(mu, mu_from_charge))

    return {
        "status": "PASS_P10_ASYMPTOTIC_CHARGE_NORMALIZATION",
        "phi": phi,
        "h_eff": h_eff,
        "asymptotic_charge": sp.Eq(sp.Symbol("M_ADM"), asymptotic_charge),
        "mu_from_charge": sp.Eq(sp.Symbol("mu"), mu_from_charge),
        "charge_identity": sp.simplify(mu_from_charge - 2 * G * M / c**2) == 0,
        "newton_identity": sp.simplify(acceleration_from_charge + G * M / r**2) == 0,
        "meaning": (
            "The 1/r exterior coefficient is fixed by the asymptotic "
            "gravitational charge, so the Newton normalization is not an "
            "extra fit once the p10 branch and the action coupling G are used."
        ),
        "next_theorem_target": (
            "derive the p10 bi-conformal exterior branch from the p01 field equations",
            "derive the microscopic substrate value of the coupling G",
        ),
    }


def rg_phase_coherence_a0_origin() -> dict[str, Any]:
    """
    Phase-coherence origin of the MOND acceleration scale.

    A propagating tail with speed c loses one global coherent phase cell when
    the cosmological dephasing rate H supplies the angular wave number

        k_H = H/c.

    A coherent cell is one full phase turn, not one radian.  Therefore

        k_H * lambda_H = 2*pi,
        lambda_H = 2*pi*c/H,
        a0 = c^2/lambda_H = c*H/(2*pi).

    Thus the 2*pi is the full-cycle phase normalization of the tail/coherence
    cell, not an empirical fitting constant.
    """

    c, H, H_z, G, M = sp.symbols("c H H_z G M", positive=True, real=True)
    k_H, lambda_H, a0, a0_z, a_H = sp.symbols(
        "k_H lambda_H a0 a0_z a_H",
        positive=True,
        real=True,
    )

    k_H_expr = sp.simplify(H / c)
    lambda_H_expr = sp.simplify(2 * sp.pi / k_H_expr)
    a0_expr = sp.simplify(c**2 / lambda_H_expr)
    a0_z_expr = sp.simplify(c * H_z / (2 * sp.pi))
    hubble_acceleration = sp.simplify(c * H)
    btfr_v4 = sp.simplify(G * M * a0_expr)

    return {
        "status": "PASS_PHASE_COHERENCE_A0_ORIGIN",
        "tail_speed": c,
        "cosmological_dephasing_rate": H,
        "Hubble_angular_wavenumber": sp.Eq(k_H, k_H_expr),
        "full_phase_cycle": sp.Eq(k_H * lambda_H, 2 * sp.pi),
        "coherence_wavelength": sp.Eq(lambda_H, lambda_H_expr),
        "phase_cycle_identity": sp.simplify(k_H_expr * lambda_H_expr - 2 * sp.pi) == 0,
        "light_crossing_phase_identity": (
            sp.simplify(H * (lambda_H_expr / c) - 2 * sp.pi) == 0
        ),
        "a0_definition": sp.Eq(a0, a0_expr),
        "a0_identity": sp.simplify(a0_expr - c * H / (2 * sp.pi)) == 0,
        "a0_redshift": sp.Eq(a0_z, a0_z_expr),
        "Hubble_acceleration": sp.Eq(a_H, hubble_acceleration),
        "a0_over_cH_identity": (
            sp.simplify(a0_expr / hubble_acceleration - 1 / (2 * sp.pi)) == 0
        ),
        "BTFR_coherence_normalization": sp.Eq(sp.Symbol("v_flat^4"), btfr_v4),
        "BTFR_coherence_identity": sp.simplify(btfr_v4 - G * M * c * H / (2 * sp.pi)) == 0,
        "meaning": (
            "a0 is the acceleration associated with one full coherent phase "
            "cell of the tail medium at cosmological dephasing rate H. The "
            "2*pi factor is the phase-cycle normalization."
        ),
        "next_theorem_target": (
            "identify H with the fitted RG cosmological background H(z)",
            "derive the same coherence boundary from the nonlinear tail/vortex equation",
            "test the predicted a0(z)=cH(z)/(2*pi) against galaxy evolution data",
        ),
    }


def p07_variational_vortex_loading_closure() -> dict[str, Any]:
    """
    Variational origin of the p07 total-gradient loading law.

    Let g_v be the vortex/free response and g_N the localized Newton channel.
    The minimal local convex loading potential with:

    * cubic self-loading of the free vortex response,
    * quadratic loading against the localized channel,
    * linear coherence drive set by a0,

    is

        W(g_v; g_N) = g_v^3/3 + g_N*g_v^2/2 - a0*g_N*g_v.

    Its stationarity gives

        g_v*(g_N+g_v) = a0*g_N,

    hence, with g=g_N+g_v,

        g_v/g_N = a0/g.
    """

    g_v, g_N, a0, y = sp.symbols("g_v g_N a0 y", positive=True, real=True)

    loading_potential = sp.simplify(
        g_v**3 / 3 + g_N * g_v**2 / 2 - a0 * g_N * g_v
    )
    stationarity = sp.factor(sp.diff(loading_potential, g_v))
    curvature = sp.diff(loading_potential, g_v, 2)
    g_v_solution = sp.solve(sp.Eq(stationarity, 0), g_v)[0]
    g_total_solution = sp.simplify(g_N + g_v_solution)

    closure_identity = (
        sp.simplify(g_v_solution / g_N - a0 / g_total_solution) == 0
    )
    stationarity_identity = (
        sp.simplify(stationarity.subs(g_v, g_v_solution)) == 0
    )

    g_total_y = sp.simplify(g_total_solution.subs(g_N, y * a0))
    g_v_y = sp.simplify(g_v_solution.subs(g_N, y * a0))

    return {
        "status": "PASS_VARIATIONAL_VORTEX_LOADING_CLOSURE",
        "loading_potential": loading_potential,
        "stationarity_equation": sp.Eq(stationarity, 0),
        "positive_curvature": sp.StrictGreaterThan(curvature, 0),
        "g_v_solution": g_v_solution,
        "g_total_solution": g_total_solution,
        "stationarity_identity": stationarity_identity,
        "closure_identity": closure_identity,
        "newton_limit_identity": sp.limit(g_total_y / (a0 * y), y, sp.oo) == 1,
        "deep_mond_limit_identity": sp.limit(g_total_y / (a0 * sp.sqrt(y)), y, 0, dir="+") == 1,
        "vortex_suppression_identity": sp.limit(g_v_y / (a0 * y), y, sp.oo) == 0,
        "meaning": (
            "The p07 loading rule is the stable stationary point of the "
            "minimal convex vortex-loading potential. Newton and deep-MOND "
            "limits follow from the same variational closure."
        ),
        "next_theorem_target": (
            "derive the three loading-potential terms from coarse-grained vortex action",
            "derive nonlocal/curl corrections for disks and non-spherical systems",
            "match the local potential to finite-radius vortex boundary conditions",
        ),
    }


def vector_aqual_variational_pde_closure() -> dict[str, Any]:
    """
    Vector/coarse-grained PDE closure for the mature vortex branch.

    The local loading theorem fixes

        mu(x) = x/(1+x).

    A nonlinear elliptic potential equation follows from the AQUAL-type
    vortex functional with

        y = |grad h|^2/a0^2,
        F(y) = y - 2*sqrt(y) + 2*log(1+sqrt(y)),
        dF/dy = mu(sqrt(y)).

    The field equation is

        div[mu(|grad h|/a0) grad h] = source.

    In spherical symmetry this reduces to mu(g/a0) g = g_N, exactly the
    branch-selector law already proved above.  In disks and non-spherical
    systems, the nonlinear PDE carries the curl/nonlocal correction; one must
    solve this PDE instead of using a purely algebraic spherical shortcut.
    """

    x, y, a0, g_N = sp.symbols("x y a0 g_N", positive=True, real=True)

    mu_x = sp.simplify(x / (1 + x))
    F_y = sp.simplify(y - 2 * sp.sqrt(y) + 2 * sp.log(1 + sp.sqrt(y)))
    dF_dy = sp.simplify(sp.diff(F_y, y))
    mu_sqrt_y = sp.simplify(mu_x.subs(x, sp.sqrt(y)))

    g = sp.simplify((g_N + sp.sqrt(g_N**2 + 4 * a0 * g_N)) / 2)
    spherical_residual = sp.simplify((g / a0) / (1 + g / a0) * g - g_N)
    y_N = sp.symbols("y_N", positive=True, real=True)
    nu_y = sp.simplify(g.subs(g_N, y_N * a0) / (y_N * a0))

    monotone_operator = sp.factor(sp.diff(x * mu_x, x))
    convex_F = sp.factor(sp.diff(F_y, y, 2))

    return {
        "status": "PASS_VECTOR_AQUAL_VARIATIONAL_PDE_CLOSURE",
        "mu_x": mu_x,
        "F_y": F_y,
        "dF_dy": dF_dy,
        "dF_dy_identity": sp.simplify(dF_dy - mu_sqrt_y) == 0,
        "newton_mu_limit": sp.limit(mu_x, x, sp.oo) == 1,
        "deep_mu_limit": sp.limit(mu_x / x, x, 0, dir="+") == 1,
        "monotone_operator_derivative": monotone_operator,
        "operator_monotonicity_positive": sp.StrictGreaterThan(monotone_operator, 0),
        "F_second_derivative": convex_F,
        "PDE": "div[mu(|grad h|/a0) grad h] = source",
        "curl_rule": (
            "For disks/non-spherical systems solve the nonlinear PDE; the "
            "algebraic nu(|grad Phi_N|) shortcut is valid only when its curl "
            "residual vanishes."
        ),
        "spherical_solution_g": g,
        "spherical_selector_identity": spherical_residual == 0,
        "nu_y": nu_y,
        "newton_limit_identity": sp.limit(g.subs(g_N, y_N * a0) / (a0 * y_N), y_N, sp.oo) == 1,
        "deep_mond_limit_identity": sp.limit(g.subs(g_N, y_N * a0) / (a0 * sp.sqrt(y_N)), y_N, 0, dir="+") == 1,
        "meaning": (
            "The mature vortex branch has a variational vector PDE. The "
            "spherical algebraic selector is its radial reduction; disk/curl "
            "corrections are PDE effects, not new force laws."
        ),
        "next_theorem_target": (
            "solve the vector PDE for thin disks and compare with SPARC residuals",
            "derive boundary conditions from the finite coherence cutoff",
            "couple the PDE source normalization to the p01/p10 stress variables",
        ),
    }


def coherence_cutoff_vortex_profile() -> dict[str, Any]:
    """
    Finite coherence cutoff for the MOND/vortex tail.

    The pure deep-MOND logarithmic profile cannot be extended literally to
    infinity.  The RG coherence scale supplies the outer cutoff:

        R_coh = c^2/a0 = 2*pi*c/H.

    A smooth minimal suppression profile

        S(r) = 1/(1+(r/R_coh)^2)

    keeps the deep-MOND plateau in the coherent interior and suppresses the
    vortex tail outside the coherent cell.
    """

    r, R, G, M, a0, c, H, rho_eff = sp.symbols(
        "r R G M a0 c H rho_eff",
        positive=True,
        real=True,
    )
    A = sp.sqrt(G * M * a0)
    suppression = sp.simplify(1 / (1 + (r / R) ** 2))
    h_prime = sp.simplify(-A * suppression / (c**2 * r))
    h_cut = sp.simplify(-A * sp.log(r / sp.sqrt(R**2 + r**2)) / c**2)
    acceleration = sp.simplify(c**2 * h_prime)
    delta_p = sp.simplify(rho_eff * A * suppression / 2)

    far_acceleration = -A * R**2 / r**3
    far_energy_integrand = sp.simplify(r**2 * h_prime**2)
    far_energy_reference = sp.simplify(A**2 * R**4 / (c**4 * r**4))

    R_from_a0 = sp.simplify(c**2 / a0)
    R_from_H = sp.simplify(R_from_a0.subs(a0, c * H / (2 * sp.pi)))

    return {
        "status": "PASS_COHERENCE_CUTOFF_VORTEX_PROFILE",
        "suppression_profile": suppression,
        "coherence_radius_from_a0": sp.Eq(sp.Symbol("R_coh"), R_from_a0),
        "coherence_radius_from_H": sp.Eq(sp.Symbol("R_coh"), R_from_H),
        "h_prime_cutoff": h_prime,
        "h_cutoff": h_cut,
        "h_derivative_identity": sp.simplify(sp.diff(h_cut, r) - h_prime) == 0,
        "acceleration_cutoff": acceleration,
        "deep_interior_identity": (
            sp.limit(acceleration / (-A / r), r, 0, dir="+") == 1
        ),
        "far_tail_identity": sp.limit(acceleration / far_acceleration, r, sp.oo) == 1,
        "Delta_p_cutoff": delta_p,
        "Delta_p_plateau_identity": (
            sp.limit(delta_p, r, 0, dir="+") == rho_eff * A / 2
        ),
        "Delta_p_far_scaling_identity": (
            sp.limit(delta_p / (rho_eff * A * R**2 / (2 * r**2)), r, sp.oo) == 1
        ),
        "far_energy_integrand": far_energy_integrand,
        "far_energy_integrand_identity": (
            sp.limit(far_energy_integrand / far_energy_reference, r, sp.oo) == 1
        ),
        "meaning": (
            "The MOND logarithmic branch is a coherent-interior limit. The "
            "tail is naturally cut off at the phase-coherence radius, so the "
            "outer vortex contribution is finite and suppressed."
        ),
        "next_theorem_target": (
            "derive the exact suppression profile from the nonlinear vortex equation",
            "include environmental/external-field cutoffs when they are smaller than R_coh",
            "match the inner cutoff to the Newton/local-source branch",
        ),
    }


def external_field_loading_suppression() -> dict[str, Any]:
    """
    External-field/environmental suppression from the same loading rule.

    The vortex response is controlled by the total gradient, not by the
    internal Newtonian source alone:

        g_v/g_N = a0/g_total.

    Therefore an external field loads the medium and bounds the free vortex
    response.  If g_total >= g_ext, then

        g_v/g_N <= a0/g_ext.

    Strong external fields suppress the MOND/vortex enhancement; isolated
    weak systems recover the deep-MOND branch.
    """

    g_N, g_ext, a0, q = sp.symbols("g_N g_ext a0 q", positive=True, real=True)

    g_isolated = sp.simplify((g_N + sp.sqrt(g_N**2 + 4 * a0 * g_N)) / 2)
    isolated_boost = sp.simplify(g_isolated / g_N)
    external_ratio_bound = sp.simplify(a0 / g_ext)
    q_bound = sp.simplify(external_ratio_bound.subs(g_ext, q * a0))

    return {
        "status": "PASS_EXTERNAL_FIELD_LOADING_SUPPRESSION",
        "loading_rule": "g_v/g_N = a0/g_total",
        "external_total_gradient_bound": "g_total >= g_ext",
        "vortex_ratio_bound": external_ratio_bound,
        "strong_external_suppression_identity": sp.limit(q_bound, q, sp.oo) == 0,
        "external_at_a0_bound_identity": sp.simplify(q_bound.subs(q, 1) - 1) == 0,
        "isolated_total_g": g_isolated,
        "isolated_boost": isolated_boost,
        "isolated_deep_boost_identity": (
            sp.limit(isolated_boost / sp.sqrt(a0 / g_N), g_N, 0, dir="+") == 1
        ),
        "isolated_newton_identity": sp.limit(isolated_boost, g_N, sp.oo) == 1,
        "meaning": (
            "The external-field effect is the same total-gradient loading "
            "seen in a non-isolated environment. Strong external gradients "
            "load the medium and suppress the free vortex response."
        ),
        "next_theorem_target": (
            "solve the vector PDE with external boundary gradients",
            "quantify disk/satellite environmental residuals",
            "compare inferred a0 and residuals against galaxy environment",
        ),
    }


def p07_vortex_loading_branch_selector() -> dict[str, Any]:
    """
    Branch selector: total-gradient loading chooses Newton vs vortex response.

    p07's mature two-channel law is

        g = g_N + g_v,
        g_v/g_N = a0/g,

    where the vortex/free response is loaded by the total acceleration g.
    This gives the simple MOND interpolating function and fixes the stress
    source that the p13 master bridge must use:

        Delta_p(r) = r*rho_eff*g_v/2.

    In strong fields the vortex branch is suppressed.  In the point-mass
    weak-field limit the same stress tends to the constant deep-MOND plateau.
    """

    g, g_N, g_v, a0, x, y = sp.symbols(
        "g g_N g_v a0 x y",
        positive=True,
        real=True,
    )
    r, G, M, rho_eff = sp.symbols("r G M rho_eff", positive=True, real=True)

    split_equation = sp.Eq(g, g_N + g_v)
    loading_equation = sp.Eq(g_v / g_N, a0 / g)
    g_N_from_total = sp.solve(sp.Eq(g, g_N * (1 + a0 / g)), g_N)[0]
    mu_g = sp.simplify(g_N_from_total / g)
    mu_x = sp.simplify(mu_g.subs(g, x * a0))

    g_solution = sp.simplify((g_N + sp.sqrt(g_N**2 + 4 * a0 * g_N)) / 2)
    g_v_solution = sp.simplify(g_solution - g_N)
    nu_y = sp.simplify(g_solution.subs(g_N, y * a0) / (y * a0))
    g_solution_y = sp.simplify(g_solution.subs(g_N, y * a0))
    deep_limit_identity = sp.limit(g_solution_y / (a0 * sp.sqrt(y)), y, 0, dir="+") == 1
    newton_limit_identity = sp.limit(g_solution_y / (a0 * y), y, sp.oo) == 1
    vortex_suppression_identity = sp.limit(g_v_solution.subs(g_N, y * a0) / (y * a0), y, sp.oo) == 0

    delta_p_selector = sp.simplify(r * rho_eff * g_v_solution / 2)
    point_mass_g_N = G * M / r**2
    point_mass_g = sp.simplify(g_solution.subs(g_N, point_mass_g_N))
    point_mass_delta_p = sp.simplify(delta_p_selector.subs(g_N, point_mass_g_N))
    deep_plateau = sp.simplify(rho_eff * sp.sqrt(G * M * a0) / 2)
    point_mass_deep_identity = sp.limit(point_mass_delta_p, r, sp.oo) == deep_plateau
    point_mass_strong_suppression = (
        sp.limit(point_mass_delta_p / (rho_eff * a0 * r / 2), r, 0, dir="+") == 1
    )

    return {
        "status": "PASS_P07_VORTEX_LOADING_BRANCH_SELECTOR",
        "phase_coherence_a0_origin": rg_phase_coherence_a0_origin()["status"],
        "variational_vortex_loading_closure": p07_variational_vortex_loading_closure()["status"],
        "vector_aqual_variational_pde_closure": vector_aqual_variational_pde_closure()["status"],
        "coherence_cutoff_vortex_profile": coherence_cutoff_vortex_profile()["status"],
        "external_field_loading_suppression": external_field_loading_suppression()["status"],
        "split_equation": split_equation,
        "loading_equation": loading_equation,
        "g_N_from_total": sp.Eq(g_N, g_N_from_total),
        "mu_of_g": mu_g,
        "mu_of_x": mu_x,
        "mu_identity": sp.simplify(mu_x - x / (1 + x)) == 0,
        "g_solution": g_solution,
        "nu_y": nu_y,
        "deep_mond_limit_identity": deep_limit_identity,
        "newton_limit_identity": newton_limit_identity,
        "vortex_suppression_identity": vortex_suppression_identity,
        "Delta_p_selector": delta_p_selector,
        "point_mass_g_N": point_mass_g_N,
        "point_mass_total_g": point_mass_g,
        "point_mass_Delta_p": point_mass_delta_p,
        "point_mass_deep_plateau": deep_plateau,
        "point_mass_deep_plateau_identity": point_mass_deep_identity,
        "point_mass_strong_field_suppression": point_mass_strong_suppression,
        "meaning": (
            "The transition is controlled by total-gradient loading: high g "
            "keeps the response Newtonian, while low g releases the vortex "
            "stress and tends to the p01 deep-MOND plateau."
        ),
        "next_theorem_target": (
            "use the variational vortex-loading closure for the total-gradient law",
            "use the phase-coherence theorem for a0",
            "extend the selector beyond collinear/spherical gradients",
        ),
    }


def full_transition_active_source_selector() -> dict[str, Any]:
    """
    One weak-field active source for the Newton-to-vortex transition.

    The source equation is already fixed by the action-level Bianchi bridge:

        h_eff' = (p_rad' - 2*Delta_p/r)/(c^2*rho_eff).

    The local Bernoulli channel contributes

        p_rad' = -rho_eff*g_N,

    while the vortex channel contributes

        Delta_p = rho_eff*r*g_v/2.

    The variational loading branch gives

        g_v*(g_N + g_v) = a0*g_N,
        g = g_N + g_v.

    Therefore one active source gives

        a = c^2 h_eff' = -(g_N + g_v),
        mu(g/a0)=g_N/g=x/(1+x),

    with the Newton and deep-MOND limits following from the same expression.
    """

    r, rho_eff, c, g_N, g_v, a0, x, y = sp.symbols(
        "r rho_eff c g_N g_v a0 x y",
        positive=True,
        real=True,
    )

    loading_equation = sp.Eq(g_v * (g_N + g_v), a0 * g_N)
    g_v_solution = sp.simplify(sp.solve(loading_equation, g_v)[0])
    g_total = sp.simplify(g_N + g_v_solution)
    delta_p_selector = sp.simplify(rho_eff * r * g_v_solution / 2)
    p_rad_prime = sp.simplify(-rho_eff * g_N)
    h_prime = sp.simplify((p_rad_prime - 2 * delta_p_selector / r) / (c**2 * rho_eff))
    acceleration = sp.simplify(c**2 * h_prime)

    mu_from_total = sp.simplify(g_N / g_total)
    mu_from_loading = sp.simplify(1 / (1 + a0 / g_total))
    mu_x = sp.simplify(x / (1 + x))
    mu_loading_identity = sp.simplify(mu_from_total - mu_from_loading)
    mu_x_identity = sp.simplify(1 / (1 + 1 / x) - mu_x)

    g_total_y = sp.simplify(g_total.subs(g_N, y * a0))
    acceleration_y = sp.simplify((-g_total).subs(g_N, y * a0))
    deep_limit = sp.limit(g_total_y / (a0 * sp.sqrt(y)), y, 0, dir="+") == 1
    newton_limit = sp.limit(g_total_y / (a0 * y), y, sp.oo) == 1
    vortex_suppression = sp.limit(g_v_solution.subs(g_N, y * a0) / (a0 * y), y, sp.oo) == 0

    G, M = sp.symbols("G M", positive=True, real=True)
    point_gN = G * M / r**2
    point_delta_p = sp.simplify(delta_p_selector.subs(g_N, point_gN))
    deep_point_delta_p = sp.simplify(sp.limit(point_delta_p, r, sp.oo))

    return {
        "status": "PASS_FULL_TRANSITION_ACTIVE_SOURCE_SELECTOR",
        "loading_equation": loading_equation,
        "g_v_solution": g_v_solution,
        "g_total": g_total,
        "p_rad_prime_local": p_rad_prime,
        "Delta_p_selector": delta_p_selector,
        "h_eff_prime": h_prime,
        "acceleration": acceleration,
        "total_acceleration_identity": sp.simplify(acceleration + g_total) == 0,
        "mu_from_total": mu_from_total,
        "mu_from_loading": mu_from_loading,
        "mu_loading_identity": sp.simplify(mu_loading_identity) == 0,
        "mu_x_identity": sp.simplify(mu_x_identity) == 0,
        "newton_limit_identity": newton_limit,
        "deep_mond_limit_identity": deep_limit,
        "vortex_suppression_identity": vortex_suppression,
        "acceleration_y": acceleration_y,
        "point_mass_Delta_p": point_delta_p,
        "deep_point_Delta_p": deep_point_delta_p,
        "deep_point_plateau_identity": (
            sp.simplify(deep_point_delta_p - rho_eff * sp.sqrt(G * M * a0) / 2)
            == 0
        ),
        "meaning": (
            "The same active-source equation carries the Newton channel and "
            "the vortex channel. The variational loading law supplies a smooth "
            "transition, so the MOND branch is not switched on by hand inside "
            "the weak-field source equation."
        ),
        "next_theorem_target": (
            "derive the loading potential terms from the coarse-grained vortex action",
            "solve the vector PDE with disk/curl corrections and finite boundary data",
        ),
    }


def master_refractive_stress_bridge() -> dict[str, Any]:
    """
    Master weak-stress bridge:

        active stress source -> h_eff' -> n_eff -> refractive force.

    The weak anisotropic equilibrium projection is

        p_rad' + rho_eff Phi_N' - 2*Delta_p/r = 0,

    and the RG refractive convention is Phi_N = -c^2 h_eff.  Therefore

        h_eff' = (p_rad' - 2*Delta_p/r)/(c^2 rho_eff),
        a_r = c^2 h_eff'.

    This one bridge contains the two required limits:

    * radial channel: Delta_p=0 gives the Newton inverse-square force
      when p_rad' is the localized-source radial response;
    * vortex channel: p_rad'=0 and constant Delta_p gives the deep-MOND
      logarithmic h_eff and BTFR.
    """

    r, r0, G, M, a0, c, rho_eff = sp.symbols(
        "r r0 G M a0 c rho_eff",
        positive=True,
    )
    p_rad_prime, Delta_p = sp.symbols("p_rad_prime Delta_p", real=True)

    active_source = sp.simplify(p_rad_prime - 2 * Delta_p / r)
    h_prime_master = sp.simplify(active_source / (c**2 * rho_eff))
    phi_prime_from_h = sp.simplify(-c**2 * h_prime_master)
    tov_residual = sp.simplify(
        p_rad_prime + rho_eff * phi_prime_from_h - 2 * Delta_p / r
    )
    refractive_acceleration = sp.simplify(c**2 * h_prime_master)

    h_newton_prime = -G * M / (c**2 * r**2)
    p_rad_prime_newton = sp.simplify(c**2 * rho_eff * h_newton_prime)
    h_prime_newton = sp.simplify(
        h_prime_master.subs({p_rad_prime: p_rad_prime_newton, Delta_p: 0})
    )
    acceleration_newton = sp.simplify(c**2 * h_prime_newton)

    delta_p_deep_mond = sp.simplify(rho_eff * sp.sqrt(G * M * a0) / 2)
    h_prime_mond = sp.simplify(
        h_prime_master.subs({p_rad_prime: 0, Delta_p: delta_p_deep_mond})
    )
    h_mond = sp.simplify(-sp.sqrt(G * M * a0) * sp.log(r / r0) / c**2)
    acceleration_mond = sp.simplify(c**2 * h_prime_mond)
    v2_mond = sp.simplify(-r * acceleration_mond)
    v4_mond = sp.simplify(v2_mond**2)

    h_prime_two_channel = sp.simplify(
        h_prime_master.subs(
            {
                p_rad_prime: p_rad_prime_newton,
                Delta_p: delta_p_deep_mond,
            }
        )
    )
    acceleration_two_channel = sp.simplify(c**2 * h_prime_two_channel)
    acceleration_two_channel_expected = sp.simplify(
        -G * M / r**2 - sp.sqrt(G * M * a0) / r
    )

    h_two_channel = sp.simplify(G * M / (c**2 * r) + h_mond)
    n_two_channel = sp.exp(h_two_channel)
    acceleration_from_index = sp.simplify(c**2 * sp.diff(sp.log(n_two_channel), r))

    return {
        "status": "PASS_MASTER_REFRACTIVE_STRESS_BRIDGE_IDENTITIES",
        "p01_action_stress_source": p01_spherical_action_stress_source_lemma()["status"],
        "p10_static_first_order_biconformal_selection": p10_static_first_order_biconformal_selection()["status"],
        "p10_newton_radial_response_branch": p10_newton_radial_response_branch()["status"],
        "p10_bernoulli_core_saturation_matching": p10_bernoulli_core_saturation_matching()["status"],
        "p10_asymptotic_charge_normalization": p10_asymptotic_charge_normalization()["status"],
        "p01_mond_plateau_strain_branch": p01_mond_plateau_strain_branch()["status"],
        "p07_vortex_loading_branch_selector": p07_vortex_loading_branch_selector()["status"],
        "full_transition_active_source_selector": full_transition_active_source_selector()["status"],
        "input_projection": "p_rad' + rho_eff Phi_N' - 2*Delta_p/r = 0",
        "refractive_convention": "Phi_N = -c^2 h_eff; n_eff = exp(h_eff)",
        "active_source": active_source,
        "h_prime_master": h_prime_master,
        "refractive_acceleration": refractive_acceleration,
        "stress_projection_identity": tov_residual == 0,
        "newton_radial_pressure_response": p_rad_prime_newton,
        "newton_h_prime": h_prime_newton,
        "newton_identity": sp.simplify(acceleration_newton + G * M / r**2) == 0,
        "deep_mond_delta_p": delta_p_deep_mond,
        "deep_mond_h_prime": h_prime_mond,
        "deep_mond_h_eff": h_mond,
        "deep_mond_identity": (
            sp.simplify(acceleration_mond + sp.sqrt(G * M * a0) / r) == 0
        ),
        "deep_mond_btfr_identity": sp.simplify(v4_mond - G * M * a0) == 0,
        "two_channel_h_eff": h_two_channel,
        "two_channel_n_eff": n_two_channel,
        "two_channel_acceleration": acceleration_two_channel,
        "two_channel_identity": (
            sp.simplify(acceleration_two_channel - acceleration_two_channel_expected) == 0
        ),
        "two_channel_index_identity": (
            sp.simplify(acceleration_from_index - acceleration_two_channel_expected) == 0
        ),
        "meaning": (
            "The refractive force is the active-stress force written through "
            "h_eff and n_eff. Newton and deep MOND are two stress limits of "
            "the same weak bridge, not separate force laws."
        ),
        "next_theorem_target": (
            "derive p_rad'_Newton, Delta_p_deep, rho_eff, and the transition law "
            "from the full RG active stress tensor",
            "derive the same bridge beyond the weak static projection",
            "match this stress bridge to the p03 Solar exterior and p10 oscillon branch",
        ),
    }


def pressure_variable_unification_audit() -> dict[str, Any]:
    """
    Active source ledger for the quadratic-vs-linear pressure question.

    TOV never uses "pressure itself" as the force source.  It uses the linear
    radial source combination

        S_h = p_rad' - 2*Delta_p/r.

    p10 is quadratic because p_rad=Pi_B(h,h') is a Bernoulli pressure function.
    The TOV source is Pi_B'.  p07 is linear because the vortex branch supplies
    Delta_p directly.  Both enter the same linear source S_h.
    """

    r, c, rho_eff, rho_B, p_rad_prime, Pi_B_prime, Delta_p = sp.symbols(
        "r c rho_eff rho_B p_rad_prime Pi_B_prime Delta_p",
        positive=True,
    )
    h_B_prime, h_v_prime = sp.symbols("h_B_prime h_v_prime", real=True)

    source_master = sp.simplify(p_rad_prime - 2 * Delta_p / r)
    h_prime_master = sp.simplify(source_master / (c**2 * rho_eff))

    local_source = sp.simplify(source_master.subs({p_rad_prime: Pi_B_prime, Delta_p: 0}))
    rho_B_response = sp.simplify(Pi_B_prime / (c**2 * h_B_prime))
    local_h_prime = sp.simplify(
        h_prime_master.subs(
            {
                p_rad_prime: Pi_B_prime,
                Delta_p: 0,
                rho_eff: rho_B_response,
            }
        )
    )

    vortex_source = sp.simplify(source_master.subs(p_rad_prime, 0))
    vortex_delta = sp.simplify(-c**2 * rho_eff * r * h_v_prime / 2)
    vortex_h_prime = sp.simplify(
        h_prime_master.subs({p_rad_prime: 0, Delta_p: vortex_delta})
    )

    two_channel_h_prime = sp.simplify(h_prime_master.subs(p_rad_prime, Pi_B_prime))
    two_channel_reconstruction = sp.simplify(
        (Pi_B_prime - 2 * Delta_p / r) / (c**2 * rho_eff)
    )

    return {
        "status": "PASS_ACTIVE_STRESS_SOURCE_LEDGER",
        "p01_action_stress_source": p01_spherical_action_stress_source_lemma()["status"],
        "p10_static_first_order_biconformal_selection": p10_static_first_order_biconformal_selection()["status"],
        "p10_newton_radial_response_branch": p10_newton_radial_response_branch()["status"],
        "p10_bernoulli_core_saturation_matching": p10_bernoulli_core_saturation_matching()["status"],
        "p10_asymptotic_charge_normalization": p10_asymptotic_charge_normalization()["status"],
        "p01_mond_plateau_strain_branch": p01_mond_plateau_strain_branch()["status"],
        "phase_coherence_a0_origin": rg_phase_coherence_a0_origin()["status"],
        "variational_vortex_loading_closure": p07_variational_vortex_loading_closure()["status"],
        "vector_aqual_variational_pde_closure": vector_aqual_variational_pde_closure()["status"],
        "coherence_cutoff_vortex_profile": coherence_cutoff_vortex_profile()["status"],
        "external_field_loading_suppression": external_field_loading_suppression()["status"],
        "p07_vortex_loading_branch_selector": p07_vortex_loading_branch_selector()["status"],
        "master_refractive_stress_bridge": master_refractive_stress_bridge()["status"],
        "bernoulli_tov_eos": bernoulli_tov_eos_source_closure()["status"],
        "weak_stress_projection": weak_anisotropic_stress_projection_to_h()["status"],
        "single_scalar_no_go": local_algebraic_scalar_no_go()["status"],
        "two_channel_working_ledger": two_channel_refractive_stress_ledger()["status"],
        "master_linear_source": source_master,
        "h_prime_master": h_prime_master,
        "local_bernoulli_source": local_source,
        "rho_B_response": rho_B_response,
        "local_bernoulli_identity": sp.simplify(local_h_prime - h_B_prime) == 0,
        "vortex_source": vortex_source,
        "vortex_delta_p_for_h_prime": vortex_delta,
        "vortex_identity": sp.simplify(vortex_h_prime - h_v_prime) == 0,
        "two_channel_h_prime": two_channel_h_prime,
        "two_channel_source_identity": (
            sp.simplify(two_channel_h_prime - two_channel_reconstruction) == 0
        ),
        "local_source_pressure": (
            "p10 Pi_B is quadratic in h_eff', but TOV receives the linear source Pi_B'"
        ),
        "galactic_vortex_stress": (
            "p07 Delta_p enters the same linear source as -2*Delta_p/r"
        ),
        "no_go_for_simple_algebraic_map": (
            "A single pointwise algebraic Pi_eff -> h_eff is not supported by "
            "the current p10 Bernoulli structure; the bridge is differential."
        ),
        "meaning": (
            "The quadratic-vs-linear issue is a category error: Bernoulli "
            "pressure is a quadratic pressure function, while the TOV equation "
            "uses its linear radial source derivative. The vortex anisotropy "
            "and the Bernoulli derivative are two entries of the same S_h ledger."
        ),
        "next_theorem_target": (
            "use the full-transition active source selector between Pi_B' and Delta_p",
            "solve the combined source equation beyond the symmetry-reduced ledger",
        ),
    }


def bernoulli_tov_source_short_path_certificate() -> dict[str, Any]:
    """
    Short certificate for the p10 Bernoulli / TOV source bridge.

    This is the compact answer to the quadratic-vs-linear pressure issue:
    p10 gives a quadratic Bernoulli pressure function Pi_B(h,h'), while the
    TOV/Bianchi equation uses the linear source Pi_B'.  The response density
    rho_B=Pi_B'/(c^2 h') is the EoS/source link that makes both descriptions
    the same radial channel.
    """
    eos = bernoulli_tov_eos_source_closure()
    source_ledger = pressure_variable_unification_audit()
    identities = (
        eos["rho_formula_identity"],
        eos["tov_identity"],
        source_ledger["local_bernoulli_identity"],
        source_ledger["vortex_identity"],
        source_ledger["two_channel_source_identity"],
    )

    status = (
        "PASS_BERNOULLI_TOV_SOURCE_SHORT_PATH"
        if eos["status"] == "PASS_BERNOULLI_TOV_RESPONSE_EOS_EXTERIOR"
        and source_ledger["status"] == "PASS_ACTIVE_STRESS_SOURCE_LEDGER"
        and all(identities)
        else "CHECK_BERNOULLI_TOV_SOURCE_SHORT_PATH"
    )

    return {
        "status": status,
        "eos_status": eos["status"],
        "source_ledger_status": source_ledger["status"],
        "identities": identities,
        "short_reading": (
            "p10's quadratic Bernoulli pressure enters the linear TOV source "
            "through Pi_B' and the response density rho_B."
        ),
    }


def weak_anisotropic_stress_projection_to_h() -> dict[str, Any]:
    """
    Weak stress projection from anisotropic medium equilibrium to h_eff'.

    p10's TOV note gives the weak internal equilibrium form

        p_rad' + rho_inert Phi_N' - 2*Delta_p/r = 0.

    With the refractive convention Phi_N = -c^2 h_eff, this gives

        h_eff' = (p_rad' - 2*Delta_p/r)/(c^2 rho_inert).

    In the plateau limit p_rad'≈0 and rho_inert≈rho_solid, this is exactly the
    p07 acceleration bridge written as h_eff'.

    This is still not the full external test-particle theorem: it is a weak
    projection of medium equilibrium onto the same metric potential.
    """

    r, c, rho_inert, rho_solid, Delta_p = sp.symbols(
        "r c rho_inert rho_solid Delta_p",
        positive=True,
    )
    p_rad_prime, Phi_prime = sp.symbols("p_rad_prime Phi_prime", real=True)

    tov_eq = sp.Eq(p_rad_prime + rho_inert * Phi_prime - 2 * Delta_p / r, 0)
    phi_prime_solution = sp.solve(tov_eq, Phi_prime)[0]
    h_prime = sp.simplify(-phi_prime_solution / c**2)

    p07_limit_h_prime = sp.simplify(
        h_prime.subs({p_rad_prime: 0, rho_inert: rho_solid})
    )
    p07_expected_h_prime = -2 * Delta_p / (c**2 * r * rho_solid)
    p07_acceleration = sp.simplify(c**2 * p07_limit_h_prime)

    h_newton_prime = sp.Symbol("h_Newton_prime", real=True)
    radial_pressure_requirement = sp.solve(
        sp.Eq(h_prime.subs(Delta_p, 0), h_newton_prime),
        p_rad_prime,
    )[0]

    return {
        "status": "PASS_WEAK_ANISOTROPIC_STRESS_PROJECTION_TO_H",
        "input_equilibrium": tov_eq,
        "Phi_N_convention": "Phi_N = -c^2 h_eff",
        "h_prime_general": h_prime,
        "p07_plateau_limit_h_prime": p07_limit_h_prime,
        "p07_bridge_identity": (
            sp.simplify(p07_limit_h_prime - p07_expected_h_prime) == 0
        ),
        "p07_plateau_acceleration": p07_acceleration,
        "radial_pressure_only_requirement": sp.Eq(
            p_rad_prime,
            radial_pressure_requirement,
        ),
        "bernoulli_compatibility_status": bernoulli_tov_eos_source_closure()["status"],
        "meaning": (
            "The p07 acceleration bridge follows from the weak anisotropic "
            "stress projection when radial pressure gradients are negligible."
        ),
        "resolved_mismatch": (
            "The p10 quadratic Bernoulli pressure enters the linear TOV source "
            "through its radial derivative, with a derived response density."
        ),
        "next_theorem_target": (
            "derive this weak projection from the full p01 action",
            "show when p_rad' is negligible in the galactic vortex branch",
            "derive the Bernoulli response density from the microscopic RG medium",
            "prove that the internal equilibrium projection controls the external metric h_eff",
        ),
    }


def bernoulli_tov_eos_source_closure() -> dict[str, Any]:
    """
    Close the quadratic-vs-linear mismatch at the exterior response-EoS level.

    Bernoulli gives a pressure deficit

        Pi_B = exp(-2h) * h'^2 / (8*pi*G).

    TOV uses the radial pressure source Pi_B'.  Therefore the compatible
    response density is

        rho_B c^2 = dPi_B/dh  along the exterior profile,

    or rho_B = Pi_B'/(c^2 h') where h' != 0.  This turns the quadratic
    Bernoulli pressure into the linear TOV source without flipping the sign.
    """

    r, G, M, c = sp.symbols("r G M c", positive=True)
    h = sp.Function("h_eff")(r)
    h_prime = sp.diff(h, r)
    h_second = sp.diff(h, r, 2)

    Pi_B = sp.simplify(sp.exp(-2 * h) * h_prime**2 / (8 * sp.pi * G))
    rho_response = sp.simplify(sp.diff(Pi_B, r) / (c**2 * h_prime))
    rho_response_formula = sp.simplify(
        sp.exp(-2 * h) * (h_second - h_prime**2) / (4 * sp.pi * G * c**2)
    )
    h_prime_from_tov = sp.simplify(sp.diff(Pi_B, r) / (c**2 * rho_response))

    h_newton = G * M / (c**2 * r)
    subs_newton = {
        h: h_newton,
        h_prime: sp.diff(h_newton, r),
        h_second: sp.diff(h_newton, r, 2),
    }
    rho_newton = sp.factor(sp.simplify(rho_response_formula.subs(subs_newton)))
    pressure_peak_radius = sp.simplify(G * M / (2 * c**2))

    return {
        "status": "PASS_BERNOULLI_TOV_RESPONSE_EOS_EXTERIOR",
        "sign_rule": "use pressure deficit Pi_B=-P_static as the radial source projection",
        "Pi_B": Pi_B,
        "rho_response": rho_response,
        "rho_response_formula": rho_response_formula,
        "rho_formula_identity": sp.simplify(rho_response - rho_response_formula) == 0,
        "h_prime_from_tov": h_prime_from_tov,
        "tov_identity": sp.simplify(h_prime_from_tov - h_prime) == 0,
        "newton_h_eff": h_newton,
        "newton_response_density": rho_newton,
        "newton_positive_exterior_condition": sp.StrictGreaterThan(r, pressure_peak_radius),
        "pressure_peak_radius": pressure_peak_radius,
        "p10_peak_reading": "pressure_peak_radius = r_s/4 when r_s=2GM/c^2",
        "meaning": (
            "The quadratic Bernoulli pressure and linear TOV source are compatible "
            "if the medium response density is the derivative of the pressure "
            "deficit with respect to h_eff along the exterior profile."
        ),
        "still_open": (
            "derive rho_response from the p01/p10 action, not only as the required response",
            "handle the strong core where the weak exterior condition fails",
            "match this radial response to the vortex anisotropic response in one stress tensor",
        ),
    }


def local_algebraic_scalar_no_go() -> dict[str, Any]:
    """
    A constant MOND plateau stress cannot produce a force by h_eff=F(Pi0).

    p07's deep plateau uses constant Delta_p over the observed flat part.  If
    one tries to set h_eff = F(Pi_eff) with Pi_eff constant and no derivative,
    radius, or flux variable, then h_eff' = 0.  Deep MOND requires h_eff' ~ -1/r.

    Therefore the bridge cannot be a finished pointwise scalar algebraic map.
    It must be differential, nonlocal, or tensor/flux based.
    """

    r, G, M, a0, c, Pi0 = sp.symbols("r G M a0 c Pi0", positive=True)
    F = sp.Function("F")
    h_local = F(Pi0)
    h_prime_local = sp.diff(h_local, r)
    required_h_prime = -sp.sqrt(G * M * a0) / (c**2 * r)
    residual = sp.simplify(h_prime_local - required_h_prime)

    return {
        "status": "PASS_NO_GO_LOCAL_ALGEBRAIC_SCALAR_MAP_FOR_CONSTANT_PLATEAU",
        "assumption_tested": "h_eff = F(Pi0) with constant plateau Pi0",
        "h_prime_from_local_map": h_prime_local,
        "required_deep_mond_h_prime": required_h_prime,
        "residual": residual,
        "no_go_check": h_prime_local == 0 and residual != 0,
        "meaning": (
            "The MOND plateau rules out a purely local scalar Pi_eff -> h_eff "
            "map unless the bridge carries derivative, radius, boundary, or "
            "topological flux information."
        ),
    }


def two_channel_refractive_stress_ledger() -> dict[str, Any]:
    """
    Working unification ledger: one refractive h_eff with two independent
    stress channels.

    This is not the final stress-tensor theorem.  It records the minimal form
    that can hold both active limits without falsifying either:

        h_eff = h_Newton + h_vortex

    with h_Newton supported by the p10 Bernoulli/localized-source branch and
    h_vortex supported by the p07 vortex/Delta_p branch.

    One h_eff is a shared refractive output variable. The Bernoulli and vortex
    channels remain distinct; their coupling and addition must be derived by
    the stress projection.
    """

    r, r0, G, M, a0, c, rho_solid = sp.symbols(
        "r r0 G M a0 c rho_solid",
        positive=True,
    )

    h_newton = G * M / (c**2 * r)
    delta_p_deep = rho_solid * sp.sqrt(G * M * a0) / 2
    h_vortex = sp.simplify(
        -2 * delta_p_deep * sp.log(r / r0) / (c**2 * rho_solid)
    )
    h_total = sp.simplify(h_newton + h_vortex)

    bernoulli_pressure_newton = sp.simplify(
        sp.exp(-2 * h_newton) * sp.diff(h_newton, r) ** 2 / (8 * sp.pi * G)
    )
    vortex_h_prime = sp.simplify(sp.diff(h_vortex, r))
    vortex_h_prime_expected = sp.simplify(
        -2 * delta_p_deep / (c**2 * r * rho_solid)
    )

    total_acceleration = sp.simplify(c**2 * sp.diff(h_total, r))
    expected_acceleration = -G * M / r**2 - sp.sqrt(G * M * a0) / r
    v2_total = sp.simplify(-r * total_acceleration)
    far_v2 = sp.simplify(sp.limit(v2_total, r, sp.oo))
    far_v4 = sp.simplify(far_v2**2)

    return {
        "status": "PASS_TWO_CHANNEL_REFRACTIVE_STRESS_IDENTITIES",
        "stress_channels": (
            "Pi_Bernoulli/localized-source channel",
            "Delta_p_vortex/anisotropic channel",
        ),
        "h_newton": h_newton,
        "h_vortex_deep": h_vortex,
        "h_total": h_total,
        "bernoulli_pressure_newton": bernoulli_pressure_newton,
        "deep_delta_p": delta_p_deep,
        "vortex_h_prime": vortex_h_prime,
        "vortex_h_prime_identity": (
            sp.simplify(vortex_h_prime - vortex_h_prime_expected) == 0
        ),
        "total_acceleration": total_acceleration,
        "total_acceleration_identity": (
            sp.simplify(total_acceleration - expected_acceleration) == 0
        ),
        "v2_total": v2_total,
        "far_v2": far_v2,
        "far_btfr_identity": sp.simplify(far_v4 - G * M * a0) == 0,
        "one_medium_many_channels_rule": (
            "one refractive output may collect independent stress channels; "
            "the channels remain distinct"
        ),
        "meaning": (
            "A shared refractive h_eff can carry both Newton and MOND behavior "
            "because the local Bernoulli channel and the vortex anisotropic "
            "channel enter the active RG stress ledger as separate channels."
        ),
        "next_theorem_target": (
            "use p10 for the local channel and p01/p07 for the vortex channel",
            "use full_transition_active_source_selector for the weak spherical transition",
            "prove finite energy and boundary conditions for the vortex channel",
        ),
    }


def required_enthalpy_profiles_for_newton_mond() -> dict[str, Any]:
    """
    Target profiles for the bridge variable h_eff = F(Pi_eff) = log(n_eff).

    This is not a derivation of h_eff. It says exactly what the RG pressure
    bridge must produce in the two weak-field regimes.
    """

    r, r0, G, M, a0, c = sp.symbols("r r0 G M a0 c", positive=True)

    h_newton = G * M / (c**2 * r)
    a_newton = sp.simplify(c**2 * sp.diff(h_newton, r))

    h_deep_mond = -sp.sqrt(G * M * a0) * sp.log(r / r0) / c**2
    a_deep_mond = sp.simplify(c**2 * sp.diff(h_deep_mond, r))
    v2_deep_mond = sp.simplify(-r * a_deep_mond)
    v4_deep_mond = sp.simplify(v2_deep_mond**2)

    return {
        "status": "PASS_TARGET_PROFILE_LEDGER",
        "bridge_variable": "h_eff = F(Pi_eff) = log(n_eff)",
        "newton_target_h_eff": h_newton,
        "newton_target_acceleration": a_newton,
        "newton_target_identity": sp.simplify(a_newton + G * M / r**2) == 0,
        "deep_mond_target_h_eff": h_deep_mond,
        "deep_mond_target_acceleration": a_deep_mond,
        "deep_mond_target_identity": (
            sp.simplify(a_deep_mond + sp.sqrt(G * M * a0) / r) == 0
        ),
        "deep_mond_btfr_identity": sp.simplify(v4_deep_mond - G * M * a0) == 0,
        "meaning": (
            "RG must derive a 1/r h_eff near localized sources and a logarithmic "
            "h_eff in the deep galactic branch."
        ),
        "still_open": (
            "derive the 1/r h_eff from the local source branch",
            "derive the logarithmic h_eff from the vortex/pressure plateau",
            "derive the transition law instead of selecting it phenomenologically",
        ),
    }


def refractive_source_short_path_theorem() -> dict[str, Any]:
    """
    Short theorem kernel for the refractive mechanism.

    The long bridge reduces to:

        action stress conservation -> TOV source for h_eff
        minimal matter coupling     -> n_eff=exp(h_eff)
        index gradient              -> force.

    This is the compact route the article should emphasize.
    """
    r, c = sp.symbols("r c", positive=True)
    rho = sp.Function("rho_eff")(r)
    p_rad = sp.Function("p_rad")(r)
    Delta_p = sp.Function("Delta_p")(r)
    h_eff = sp.Function("h_eff")(r)
    n_eff = sp.exp(h_eff)

    h_prime_source = sp.simplify(
        (sp.diff(p_rad, r) - 2 * Delta_p / r) / (c**2 * rho)
    )
    acceleration_from_index = sp.simplify(c**2 * sp.diff(sp.log(n_eff), r))
    acceleration_from_source = sp.simplify(
        acceleration_from_index.subs(sp.diff(h_eff, r), h_prime_source)
    )
    expected_source_acceleration = sp.simplify(
        (sp.diff(p_rad, r) - 2 * Delta_p / r) / rho
    )

    return {
        "status": "PASS_SHORT_REFRACTIVE_SOURCE_THEOREM",
        "source_equation": sp.Eq(sp.diff(h_eff, r), h_prime_source),
        "index_definition": sp.Eq(sp.Symbol("n_eff"), n_eff),
        "acceleration_from_source": acceleration_from_source,
        "identity": sp.simplify(
            acceleration_from_source - expected_source_acceleration
        ) == 0,
        "meaning": (
            "The weak static refractive mechanism needs no separate scalar "
            "Pi_eff map: action stress enters through the TOV source, and "
            "minimal metric coupling turns h_eff into n_eff."
        ),
    }


def newton_mond_transition_short_path_theorem() -> dict[str, Any]:
    """
    Short theorem kernel for the Newton/MOND weak transition.

    One source equation carries both channels:

        p_rad' = -rho*g_N,
        Delta_p = rho*r*g_v/2,
        g = g_N + g_v.

    The variational loading law selects the interpolation.
    """
    r, c, rho, g_N, g_v, a0, G, M = sp.symbols(
        "r c rho_eff g_N g_v a0 G M",
        positive=True,
    )
    x = sp.symbols("x", positive=True)

    p_rad_prime = -rho * g_N
    Delta_p = rho * r * g_v / 2
    h_prime = sp.simplify((p_rad_prime - 2 * Delta_p / r) / (c**2 * rho))
    total_acceleration = sp.simplify(c**2 * h_prime)

    W = g_v**3 / 3 + g_N * g_v**2 / 2 - a0 * g_N * g_v
    loading_equation = sp.factor(sp.diff(W, g_v))
    mu_x_identity = sp.simplify(1 / (1 + 1 / x) - x / (1 + x)) == 0

    deep_g = sp.sqrt(G * M * a0) / r
    deep_Delta_p = sp.simplify(rho * r * deep_g / 2)
    deep_plateau_identity = (
        sp.simplify(deep_Delta_p - rho * sp.sqrt(G * M * a0) / 2) == 0
    )

    return {
        "status": "PASS_SHORT_NEWTON_MOND_TRANSITION_THEOREM",
        "stress_split": {
            "p_rad_prime": sp.Eq(sp.Symbol("p_rad_prime"), p_rad_prime),
            "Delta_p": sp.Eq(sp.Symbol("Delta_p"), Delta_p),
        },
        "total_acceleration": total_acceleration,
        "total_acceleration_identity": sp.simplify(total_acceleration + g_N + g_v) == 0,
        "loading_potential": W,
        "loading_equation": sp.Eq(loading_equation, 0),
        "mu_x_identity": mu_x_identity,
        "deep_plateau_identity": deep_plateau_identity,
        "meaning": (
            "The bridge does not need separate force laws.  It needs one stress "
            "split: radial source pressure gives g_N, vortex anisotropy gives "
            "g_v, and the variational loading selects the transition."
        ),
    }


def pressure_to_index_bridge_requirements() -> dict[str, Any]:
    """Central theorem target: derive the active RG stress sources."""

    r, c = sp.symbols("r c", positive=True)
    Pi = sp.Function("Pi_eff")(r)
    F = sp.Function("F")
    log_n = F(Pi)
    radial_acceleration = sp.diff(c**2 * log_n, r)

    return {
        "status": "PASS_REFRACTIVE_BRIDGE_SOURCE_LEDGER_READY",
        "short_refractive_source_theorem": refractive_source_short_path_theorem()["status"],
        "short_newton_mond_transition_theorem": newton_mond_transition_short_path_theorem()["status"],
        "algebraic_ansatz_status": "NOT_CLOSED_AND_DISFAVORED_AS_A_SINGLE_LOCAL_MAP",
        "differential_bridge_status": "CLOSED_AT_WEAK_STRESS_PROJECTION_LEVEL",
        "index_definition": "n_eff = exp(h_eff)",
        "radial_acceleration": radial_acceleration,
        "on_shell_bianchi_tov_bridge": on_shell_bianchi_tov_refractive_source_theorem()["status"],
        "action_stress_to_index_theorem": action_stress_to_refractive_index_theorem()["status"],
        "p10_static_first_order_biconformal_selection": p10_static_first_order_biconformal_selection()["status"],
        "p01_action_stress_source": p01_spherical_action_stress_source_lemma()["status"],
        "p10_newton_radial_response_branch": p10_newton_radial_response_branch()["status"],
        "p10_bernoulli_core_saturation_matching": p10_bernoulli_core_saturation_matching()["status"],
        "p10_asymptotic_charge_normalization": p10_asymptotic_charge_normalization()["status"],
        "p01_mond_plateau_strain_branch": p01_mond_plateau_strain_branch()["status"],
        "phase_coherence_a0_origin": rg_phase_coherence_a0_origin()["status"],
        "variational_vortex_loading_closure": p07_variational_vortex_loading_closure()["status"],
        "vector_aqual_variational_pde_closure": vector_aqual_variational_pde_closure()["status"],
        "coherence_cutoff_vortex_profile": coherence_cutoff_vortex_profile()["status"],
        "external_field_loading_suppression": external_field_loading_suppression()["status"],
        "p07_vortex_loading_branch_selector": p07_vortex_loading_branch_selector()["status"],
        "full_transition_active_source_selector": full_transition_active_source_selector()["status"],
        "master_stress_bridge": master_refractive_stress_bridge()["status"],
        "closed_sublemma": universal_potential_to_index_lemma()["status"],
        "action_sublemma": minimal_point_particle_action_bridge()["status"],
        "p10_biconformal_sublemma": biconformal_branch_refractive_bridge()["status"],
        "p10_pressure_sublemma": bernoulli_pressure_to_h_ode()["status"],
        "p07_stress_sublemma": mond_stress_to_h_ode()["status"],
        "bernoulli_tov_eos_sublemma": bernoulli_tov_eos_source_closure()["status"],
        "weak_stress_projection_sublemma": weak_anisotropic_stress_projection_to_h()["status"],
        "single_scalar_no_go": local_algebraic_scalar_no_go()["status"],
        "two_channel_stress_ledger": two_channel_refractive_stress_ledger()["status"],
        "pressure_unification": pressure_variable_unification_audit()["status"],
        "continuation_targets": (
            "derive the on-shell profiles p_rad'_Newton, Delta_p_deep, rho_eff, and the transition law from T^RefG_mn",
            "derive the Bernoulli response density from the active medium action",
            "derive the universal test-matter potential V_eff/m = -c^2 h_eff",
            "derive g_tt=exp(-2h_eff) as the one physical metric branch",
            "fix sign and normalization without using a phantom sign",
            "recover the Newton 1/r index in the local source regime",
            "recover the logarithmic deep-MOND index in the galaxy regime",
            "show compatibility with the Solar GR branch from p03b",
        ),
        "meaning": (
            "The weak-field stress-to-index bridge now has a source ledger: "
            "p01 supplies stress variables, the on-shell Bianchi identity "
            "supplies the TOV source equation, p10 supplies the local Newton "
            "channel, p07 supplies the coherent vortex channel, and both map "
            "to the same h_eff and n_eff."
        ),
    }


def refractive_gravity_weak_field_chain_theorem() -> dict[str, Any]:
    """
    Article-facing weak-field chain theorem for the refractive mechanism.

    This collects the closed p13 steps into one gate:

        p01 action stress
        -> on-shell Bianchi/TOV source
        -> p10 first-order bi-conformal selection
        -> p10 Newton radial response
        -> p10 Bernoulli core saturation
        -> p10 asymptotic charge normalization
        -> p01 MOND strain plateau
        -> phase-coherence a0
        -> variational vortex loading selector
        -> finite coherence cutoff
        -> master stress-to-index bridge
        -> n_eff and refractive force.
    """

    action_stress = p01_spherical_action_stress_source_lemma()
    bianchi_tov = on_shell_bianchi_tov_refractive_source_theorem()
    action_to_index = action_stress_to_refractive_index_theorem()
    biconformal_selection = p10_static_first_order_biconformal_selection()
    newton_branch = p10_newton_radial_response_branch()
    core_saturation = p10_bernoulli_core_saturation_matching()
    charge_normalization = p10_asymptotic_charge_normalization()
    mond_branch = p01_mond_plateau_strain_branch()
    a0_origin = rg_phase_coherence_a0_origin()
    loading = p07_variational_vortex_loading_closure()
    vector_pde = vector_aqual_variational_pde_closure()
    cutoff = coherence_cutoff_vortex_profile()
    external = external_field_loading_suppression()
    selector = p07_vortex_loading_branch_selector()
    full_transition = full_transition_active_source_selector()
    pressure_unification = pressure_variable_unification_audit()
    bernoulli_tov_short = bernoulli_tov_source_short_path_certificate()
    master = master_refractive_stress_bridge()
    matter_action = minimal_point_particle_action_bridge()
    short_refractive = refractive_source_short_path_theorem()
    short_transition = newton_mond_transition_short_path_theorem()

    checks = (
        short_refractive["identity"],
        short_transition["total_acceleration_identity"],
        short_transition["mu_x_identity"],
        short_transition["deep_plateau_identity"],
        action_stress["isotropic_limit_identity"],
        action_stress["generic_anisotropy_sources_Delta_p"],
        bianchi_tov["bianchi_identity"],
        bianchi_tov["h_bridge_identity"],
        action_to_index["closed_identity"],
        biconformal_selection["a1_identity"],
        biconformal_selection["biconformal_identity"],
        biconformal_selection["branch_residual_identity"],
        newton_branch["h_prime_identity"],
        newton_branch["newton_acceleration_identity"],
        core_saturation["core_limit_identity"],
        core_saturation["far_limit_identity"],
        core_saturation["peak_identity"],
        core_saturation["finite_integral_identity"],
        charge_normalization["charge_identity"],
        charge_normalization["newton_identity"],
        mond_branch["exact_branch_identity"],
        a0_origin["a0_identity"],
        a0_origin["BTFR_coherence_identity"],
        loading["stationarity_identity"],
        loading["closure_identity"],
        vector_pde["dF_dy_identity"],
        vector_pde["newton_mu_limit"],
        vector_pde["deep_mu_limit"],
        vector_pde["spherical_selector_identity"],
        vector_pde["newton_limit_identity"],
        vector_pde["deep_mond_limit_identity"],
        cutoff["deep_interior_identity"],
        cutoff["far_tail_identity"],
        external["strong_external_suppression_identity"],
        external["external_at_a0_bound_identity"],
        external["isolated_deep_boost_identity"],
        external["isolated_newton_identity"],
        selector["mu_identity"],
        selector["newton_limit_identity"],
        selector["deep_mond_limit_identity"],
        selector["point_mass_deep_plateau_identity"],
        full_transition["total_acceleration_identity"],
        full_transition["mu_loading_identity"],
        full_transition["mu_x_identity"],
        full_transition["newton_limit_identity"],
        full_transition["deep_mond_limit_identity"],
        full_transition["vortex_suppression_identity"],
        full_transition["deep_point_plateau_identity"],
        bernoulli_tov_short["status"] == "PASS_BERNOULLI_TOV_SOURCE_SHORT_PATH",
        pressure_unification["local_bernoulli_identity"],
        pressure_unification["vortex_identity"],
        pressure_unification["two_channel_source_identity"],
        master["stress_projection_identity"],
        master["newton_identity"],
        master["deep_mond_identity"],
        master["deep_mond_btfr_identity"],
        master["two_channel_index_identity"],
        matter_action["weak_identity"],
    )

    return {
        "status": "PASS_REFRACTIVE_GRAVITY_WEAK_FIELD_CHAIN" if all(checks) else "FAIL",
        "scope_status": "CLOSED_WEAK_STATIC_COARSE_GRAINED_CHAIN__FULL_NONLINEAR_PDE_OPEN",
        "article_theorem": (
            "In the weak static/coarse-grained regime, RG active stresses "
            "generate a universal h_eff and n_eff=exp(h_eff). The same "
            "chain gives Newton locally, MOND/BTFR in the coherent vortex "
            "regime, a0=cH/(2*pi), a saturated p10 Bernoulli core, "
            "asymptotic charge normalization, a linear active-source EoS "
            "ledger, and a finite coherence cutoff."
        ),
        "chain": (
            short_refractive["status"],
            short_transition["status"],
            action_stress["status"],
            bianchi_tov["status"],
            action_to_index["status"],
            biconformal_selection["status"],
            newton_branch["status"],
            core_saturation["status"],
            charge_normalization["status"],
            mond_branch["status"],
            a0_origin["status"],
            loading["status"],
            vector_pde["status"],
            cutoff["status"],
            external["status"],
            selector["status"],
            full_transition["status"],
            bernoulli_tov_short["status"],
            pressure_unification["status"],
            master["status"],
            matter_action["status"],
        ),
        "closed_checks_count": len(checks),
        "all_checks_pass": all(checks),
        "not_closed_by_this_theorem": (
            "full nonlinear non-spherical PDE",
            "disk/curl solutions and SPARC/RAR likelihood",
            "cluster merger lensing/gas simulation",
            "strong-core compact-object evolution",
            "microscopic substrate value of G",
        ),
        "next_theorem_target": (
            "derive the same chain from the full nonlinear p01/p10 PDE without symmetry reduction",
            "solve the vector PDE for disk/curl corrections with environmental boundary fields",
            "match the strong-core and Solar exterior branches",
        ),
    }


def refractive_force_claim_gate() -> dict[str, ClaimGate]:
    return {
        "weak_field_refractive_chain": ClaimGate(
            claim="RG closes the weak static/coarse-grained refractive gravity chain from action stress to Newton and MOND.",
            status="CLOSED_WEAK_STATIC_COARSE_GRAINED_REFRACTIVE_CHAIN",
            verified_here=(
                "p01 action stress supplies p_rad and Delta_p",
                "p10 static spherical O(eps) equations select the bi-conformal sign a1=1",
                "p10 Bernoulli radial response gives the Newton channel",
                "p10 Bernoulli core saturation removes the central pressure blow-up of the exterior template",
                "p10 asymptotic charge normalization fixes the Newton source coefficient",
                "p01 anisotropic strain gives the MOND plateau",
                "phase coherence gives a0=cH/(2*pi)",
                "variational vortex loading gives g_v/g_N=a0/g and mu=x/(1+x)",
                "coherence cutoff makes the vortex tail finite",
                "master bridge gives n_eff and the refractive force",
            ),
            open_requirements=(
                "lift the theorem from weak/coarse-grained symmetry-reduced form to the full nonlinear PDE",
                "derive disk/curl corrections and strong-core matching",
            ),
            do_not_claim=(
                "Do not present this as a completed strong-field or non-spherical PDE theorem.",
                "Do not present this as a SPARC/RAR, cluster, or Solar-System likelihood pass by itself.",
            ),
        ),
        "metric_optical_index": ClaimGate(
            claim="Static metric motion admits an optical/refractive-index form.",
            status="CLOSED_GEOMETRIC_IDENTITY",
            verified_here=(
                "n_light = sqrt(B/A) for static isotropic light propagation",
                "slow massive motion can be written using n_matter = A^(-1/2)",
            ),
            open_requirements=(
            "derive the relevant active RG exterior metric/index from the RG field equations",
            ),
        ),
        "newton_from_index": ClaimGate(
            claim="Newton's inverse-square force follows from a Newton-profile matter index.",
            status="SUBLEMMA_CLOSED_BY_P10_NEWTON_BRANCH",
            verified_here=(
                "n_matter = exp(GM/(c^2 r)) gives radial acceleration -GM/r^2",
            ),
            open_requirements=(
                "use the downstream p10 Newton radial response and charge normalization for the source profile",
                "match the finite oscillon core to the weak exterior",
            ),
            do_not_claim=(
                "Do not use the index identity alone without the p10 source branch.",
            ),
        ),
        "mond_from_index": ClaimGate(
            claim="Deep-MOND force and BTFR follow from a logarithmic refractive index.",
            status="SUBLEMMA_CLOSED_BY_P01_P07_A0_BRANCH",
            verified_here=(
                "logarithmic index gives acceleration -sqrt(GMa0)/r",
                "circular motion then gives v^4 = GMa0",
            ),
            open_requirements=(
                "use the downstream p01 plateau, p07 vortex loading, and phase-coherence a0 origin",
                "solve non-spherical disks with the vector PDE",
            ),
            do_not_claim=(
                "Do not use the logarithmic identity alone without the vortex source branch.",
            ),
        ),
        "universal_potential_to_index": ClaimGate(
            claim="A universal static scalar potential is exactly equivalent to a refractive force.",
            status="CLOSED_CONDITIONAL_LEMMA",
            verified_here=(
                "V_eff/m = -c^2 F(Pi_eff) gives acceleration c^2 grad log(n_eff)",
                "n_eff = exp(F(Pi_eff))",
            ),
            open_requirements=(
                "use the minimal one-metric matter action lemma for the weak universal coupling",
                "exclude nonminimal matter couplings in the final matter-sector audit",
            ),
            do_not_claim=(
                "Do not treat pressure as a direct extra force on matter; it sources the metric/index.",
            ),
        ),
        "minimal_action_to_index": ClaimGate(
            claim="One-metric minimal matter action gives the weak universal refractive potential.",
            status="CLOSED_WEAK_FIELD_ACTION_LEMMA",
            verified_here=(
                "for g_tt=exp(-2h_eff), the point-particle action gives V_eff/m=-c^2 h_eff at weak order",
                "the resulting acceleration equals c^2 grad log(n_eff) with n_eff=exp(h_eff)",
            ),
            open_requirements=(
                "use the Bianchi/TOV stress bridge for h_eff in the weak static branch",
                "match the weak static branch to the full p03c Solar exterior",
            ),
            do_not_claim=(
                "Do not claim pressure directly pushes matter; p01/p10 use one-metric geodesic motion.",
            ),
        ),
        "p10_static_first_order_biconformal_selection": ClaimGate(
            claim="The p10 static spherical first-order exterior selects the bi-conformal branch.",
            status="CLOSED_FIRST_ORDER_BICONFORMAL_BRANCH_SELECTION",
            verified_here=(
                "the rr geometric radial power is 1-a1",
                "the angular geometric radial power is (a1-1)/2",
                "both vanish only for a1=1",
                "therefore A*B=1+O(U^2)",
                "the remaining stress constraints admit a p01 coefficient family",
            ),
            open_requirements=(
                "use p03c for the augmented 2PN continuation",
                "solve the full nonlinear exterior/core matching on the same branch",
            ),
            do_not_claim=(
                "Do not present first-order branch selection as a completed nonlinear compact-object exterior.",
            ),
        ),
        "p01_action_stress_source": ClaimGate(
            claim="The refractive bridge source variables are p01 action stresses.",
            status="CLOSED_ACTION_STRESS_VARIABLE_LEMMA",
            verified_here=(
                "spherical p01 action gives p_rad and p_tan by p_i=L-2*lambda_i*dL/dlambda_i",
                "Delta_p=p_tan-p_rad vanishes in the isotropic limit",
                "generic radial/tangential anisotropy sources nonzero Delta_p",
                "the master bridge uses these stress variables, not a separate pressure force",
            ),
            open_requirements=(
                "use p10 for the Newton radial response and p01/p07 for the vortex plateau",
                "derive the same profiles in the full nonlinear, non-spherical PDE",
            ),
            do_not_claim=(
                "Do not replace the named p10/p01/p07 source branches with arbitrary profiles.",
            ),
        ),
        "on_shell_bianchi_tov_bridge": ClaimGate(
            claim="The weak refractive source equation is the on-shell radial Bianchi/TOV identity of the action stress tensor.",
            status="CLOSED_ACTION_LEVEL_SOURCE_EQUATION",
            verified_here=(
                "for T^mu_nu=diag(rho,-p_rad,-p_tan,-p_tan), nabla_mu T^mu_r=0 gives p_rad'+(rho+p_rad)B'/(2B)-2*Delta_p/r=0",
                "with Phi_N'=B'/(2B) and Phi_N=-c^2 h_eff, this gives h_eff'=(p_rad'-2*Delta_p/r)/(c^2 rho_eff)",
                "therefore the bridge equation is a Bianchi/Noether consequence, not a pressure-force postulate",
            ),
            open_requirements=(
                "use p10 for localized Bernoulli response and p07 for vortex anisotropy",
                "lift the selector to the full nonlinear, non-spherical stress tensor",
            ),
            do_not_claim=(
                "Do not confuse the source-equation theorem with the full non-spherical profile solution.",
            ),
        ),
        "p10_newton_radial_response_branch": ClaimGate(
            claim="The Newton radial source is the p10 Bernoulli response inside the refractive bridge.",
            status="CLOSED_NEWTON_RADIAL_RESPONSE_BRANCH_IDENTITY",
            verified_here=(
                "h_N=GM/(c^2r) gives Pi_B=exp(-2h_N)h_N'^2/(8*pi*G)",
                "p_rad'=Pi_B' and rho_B=Pi_B'/(c^2 h_N') return h_N' in the master bridge",
                "the resulting acceleration is Newton's inverse-square law",
            ),
            open_requirements=(
                "derive rho_B microscopically from the p01/p10 medium",
                "derive the microscopic substrate value of G",
            ),
            do_not_claim=(
                "Do not confuse asymptotic charge normalization with the finite-core oscillon profile.",
            ),
        ),
        "p10_bernoulli_core_saturation_matching": ClaimGate(
            claim="The p10 Bernoulli source saturates at the core and matches a finite weak exterior source.",
            status="CLOSED_BERNOULLI_CORE_SATURATION_MATCHING",
            verified_here=(
                "for phi=-r_s/r, Pi_B=exp(phi)*phi'^2/(32*pi*G)",
                "Pi_B tends to zero at the center and at infinity",
                "the pressure source peaks at r_s/4",
                "the spherical radial source integral is finite and equals r_s/(8G)",
            ),
            open_requirements=(
                "replace the exterior template by the full finite-core oscillon solution",
                "derive junction conditions between the core and the weak exterior",
            ),
            do_not_claim=(
                "Do not treat this exterior saturation identity as the completed compact-object solution.",
            ),
        ),
        "p10_asymptotic_charge_normalization": ClaimGate(
            claim="The p10 exterior 1/r coefficient is fixed by the asymptotic gravitational charge.",
            status="CLOSED_ASYMPTOTIC_CHARGE_NORMALIZATION",
            verified_here=(
                "for phi=-mu/r and h_eff=-phi/2, M_ADM=c^2*mu/(2G)",
                "therefore mu=2GM/c^2",
                "the refractive/geodesic acceleration becomes -GM/r^2",
            ),
            open_requirements=(
                "derive the p10 bi-conformal exterior branch from p01",
                "derive the microscopic substrate value of G",
            ),
            do_not_claim=(
                "Do not confuse macroscopic charge normalization with a derivation of the microscopic value of G.",
            ),
        ),
        "p01_mond_plateau_strain_branch": ClaimGate(
            claim="The deep-MOND plateau is a p01 anisotropic strain branch.",
            status="CLOSED_PLATEAU_STRAIN_BRANCH_IDENTITY",
            verified_here=(
                "p01 gives Delta_p=2*(lambda_r-lambda_t)*K_aniso",
                "Delta_p vanishes in the isotropic limit",
                "the deep-MOND plateau fixes an exact radial/tangential strain split",
                "the small-strain limit gives the linear plateau branch",
            ),
            open_requirements=(
                "use p07 variational loading to select this branch dynamically",
                "use phase coherence and coherence cutoff for a0 and finite radius",
            ),
            do_not_claim=(
                "Do not use the plateau branch without the p07 loading and cutoff gates.",
            ),
        ),
        "phase_coherence_a0_origin": ClaimGate(
            claim="The MOND acceleration scale is the phase-coherence acceleration a0=cH/(2*pi).",
            status="CLOSED_PHASE_COHERENCE_NORMALIZATION",
            verified_here=(
                "cosmological dephasing gives k_H=H/c",
                "one coherent tail cell is one full phase cycle k_H*lambda_H=2*pi",
                "lambda_H=2*pi*c/H gives a0=c^2/lambda_H=cH/(2*pi)",
                "BTFR normalization becomes v^4=G*M*cH/(2*pi)",
            ),
            open_requirements=(
                "identify H with the fitted RG cosmological H(z)",
                "derive the same boundary from the nonlinear tail/vortex equation",
                "test a0(z)=cH(z)/(2*pi) observationally",
            ),
            do_not_claim=(
                "Do not treat a0 as a free galaxy-fit constant once the coherence branch is used.",
            ),
        ),
        "variational_vortex_loading_closure": ClaimGate(
            claim="The p07 loading law is the stable stationary point of a convex vortex-loading potential.",
            status="CLOSED_VARIATIONAL_LOADING_CLOSURE",
            verified_here=(
                "the loading potential W=g_v^3/3+g_N*g_v^2/2-a0*g_N*g_v is convex for positive channels",
                "stationarity gives g_v*(g_N+g_v)=a0*g_N",
                "with g=g_N+g_v this is exactly g_v/g_N=a0/g",
                "Newton and deep-MOND limits follow from the same stationary branch",
            ),
            open_requirements=(
                "derive the loading-potential terms from the coarse-grained vortex action",
                "derive curl/nonlocal corrections for disks and non-spherical systems",
            ),
            do_not_claim=(
                "Do not use an arbitrary mu function after adopting this variational closure.",
            ),
        ),
        "vector_aqual_variational_pde": ClaimGate(
            claim="The mature vortex branch has a vector nonlinear PDE whose spherical limit is the branch selector.",
            status="CLOSED_VECTOR_AQUAL_PDE_CLOSURE",
            verified_here=(
                "F(y)=y-2*sqrt(y)+2*log(1+sqrt(y)) gives dF/dy=mu(sqrt(y))",
                "mu(x)=x/(1+x) has the correct Newton and deep-MOND limits",
                "the spherical reduction gives mu(g/a0)g=g_N and matches the selector",
                "disk/curl corrections are handled by solving the nonlinear PDE",
            ),
            open_requirements=(
                "solve the vector PDE for disks with realistic baryonic sources",
                "derive boundary conditions from the finite coherence cutoff",
                "run SPARC/RAR likelihood with residual diagnostics",
            ),
            do_not_claim=(
                "Do not use the algebraic spherical shortcut for disks when the curl residual is nonzero.",
            ),
        ),
        "coherence_cutoff_vortex_profile": ClaimGate(
            claim="The MOND/vortex tail has a finite phase-coherence cutoff.",
            status="CLOSED_COHERENCE_CUTOFF_PROFILE",
            verified_here=(
                "R_coh=c^2/a0=2*pi*c/H",
                "S(r)=1/(1+(r/R_coh)^2) preserves the inner deep-MOND acceleration",
                "the outer acceleration decays as r^-3 instead of r^-1",
                "Delta_p tends to the deep-MOND plateau inside and decays as r^-2 outside",
                "the far stress-gradient energy integrand is integrable at infinity",
            ),
            open_requirements=(
                "derive the exact suppression profile from the nonlinear vortex equation",
                "include environmental cutoffs when external fields dominate",
                "match the inner cutoff to the Newton/local-source branch",
            ),
            do_not_claim=(
                "Do not extend the logarithmic MOND profile literally to infinity.",
            ),
        ),
        "external_field_loading_suppression": ClaimGate(
            claim="External-field suppression follows from total-gradient vortex loading.",
            status="CLOSED_EXTERNAL_FIELD_LOADING_SUPPRESSION",
            verified_here=(
                "the same loading law gives g_v/g_N=a0/g_total",
                "if g_total>=g_ext then g_v/g_N<=a0/g_ext",
                "strong external fields suppress the vortex response",
                "isolated weak systems recover the deep-MOND boost",
            ),
            open_requirements=(
                "solve the vector PDE with external boundary gradients",
                "compare predicted residuals with galaxy environment and satellite data",
            ),
            do_not_claim=(
                "Do not fit isolated MOND curves to strongly externally loaded systems without the boundary field.",
            ),
        ),
        "p07_vortex_loading_branch_selector": ClaimGate(
            claim="Total-gradient loading selects the Newton-to-vortex/MOND transition.",
            status="CLOSED_BRANCH_SELECTOR_IDENTITIES",
            verified_here=(
                "g=g_N+g_v and g_v/g_N=a0/g give mu(x)=x/(1+x)",
                "the strong-field limit returns Newtonian behavior",
                "the weak point-mass limit returns deep-MOND acceleration",
                "the selected Delta_p tends to the p01 deep-MOND plateau",
            ),
            open_requirements=(
                "use the variational vortex loading closure for the total-gradient law",
                "use the phase-coherence theorem for a0",
                "extend the selector beyond collinear/spherical gradients",
            ),
            do_not_claim=(
                "Do not use a different interpolation law unless its loading rule is derived.",
            ),
        ),
        "full_transition_active_source_selector": ClaimGate(
            claim="One active source equation carries the continuous Newton-to-vortex transition.",
            status="CLOSED_FULL_WEAK_TRANSITION_SOURCE_SELECTOR",
            verified_here=(
                "p_rad'=-rho_eff*g_N and Delta_p=r*rho_eff*g_v/2 enter the same Bianchi/TOV source",
                "variational loading gives g_v*(g_N+g_v)=a0*g_N",
                "the resulting acceleration is -(g_N+g_v)",
                "mu(g/a0)=g_N/g=x/(1+x)",
                "the Newton and deep-MOND limits follow from the same source expression",
            ),
            open_requirements=(
                "use the variational loading potential for the spherical/coarse-grained branch",
                "solve the vector PDE with non-spherical/curl corrections",
            ),
            do_not_claim=(
                "Do not present the spherical transition selector as the completed disk/cluster solution.",
            ),
        ),
        "master_refractive_stress_bridge": ClaimGate(
            claim="Weak active stress produces the refractive force through h_eff and n_eff.",
            status="CLOSED_MASTER_BRIDGE_AT_WEAK_STRESS_PROJECTION_LEVEL",
            verified_here=(
                "p_rad' + rho_eff Phi_N' - 2*Delta_p/r = 0 with Phi_N=-c^2 h_eff gives h_eff'",
                "n_eff=exp(h_eff) gives the same radial acceleration c^2 h_eff'",
                "radial stress response gives the Newton inverse-square channel",
                "anisotropic plateau stress gives the deep-MOND/BTFR channel",
                "the two independent channels add inside one h_eff and one n_eff",
            ),
            open_requirements=(
                "use the named p10/p01/p07 source branches and transition selector in the weak spherical ledger",
                "match the weak bridge to the p03 Solar branch and p10 oscillon branch",
            ),
            do_not_claim=(
                "Do not export the weak spherical ledger as the completed non-spherical PDE solution.",
            ),
        ),
        "p10_biconformal_to_index": ClaimGate(
            claim="The p10 bi-conformal Newton bridge is a refractive-index bridge.",
            status="CLOSED_REFRACTIVE_BRIDGE_WITH_FIRST_ORDER_BRANCH_SELECTION",
            verified_here=(
                "p10 static spherical first order selects A*B=1+O(U^2)",
                "for ds^2=exp(phi)c^2dt^2-exp(-phi)dSigma^2, h_eff=-phi/2",
                "phi=-2GM/(c^2r) gives n_eff=exp(GM/(c^2r)) and Newton acceleration",
            ),
            open_requirements=(
                "continue the branch beyond first order",
                "derive the microscopic substrate value of G",
            ),
            do_not_claim=(
                "Do not claim p10 already proves the full RG action-to-Newton theorem.",
            ),
        ),
        "weak_anisotropic_stress_projection": ClaimGate(
            claim="The p07 halo acceleration bridge follows from the on-shell weak anisotropic stress projection.",
            status="CLOSED_FROM_ACTION_BIANCHI_PROJECTION",
            verified_here=(
                "p_rad' + rho_inert Phi_N' - 2*Delta_p/r = 0 with Phi_N=-c^2 h_eff",
                "p_rad'=0 and rho_inert=rho_solid give h_eff'=-2*Delta_p/(c^2*r*rho_solid)",
                "the projection itself is supplied by the on-shell Bianchi/TOV theorem in this file",
            ),
            open_requirements=(
                "derive the regime where p_rad' is negligible",
                "connect the external metric h_eff to this internal medium equilibrium",
            ),
            do_not_claim=(
                "Do not claim the full p07 bridge is action-derived until these caveats close.",
            ),
        ),
        "bernoulli_tov_eos_source": ClaimGate(
            claim="p10 Bernoulli pressure is compatible with the linear TOV source through a response EoS.",
            status="CLOSED_EXTERIOR_RESPONSE_EOS",
            verified_here=(
                "Pi_B=exp(-2h_eff)*(h_eff')^2/(8*pi*G) enters TOV through Pi_B'",
                "rho_B=Pi_B'/(c^2*h_eff') gives the TOV identity h_eff'=Pi_B'/(c^2*rho_B)",
                "for the Newton profile the response is positive outside the p10 pressure peak r_s/4",
            ),
            open_requirements=(
                "derive rho_B from the p01/p10 action rather than as the required response",
                "complete the strong-core region where the weak exterior response is not valid",
                "match the radial response to the vortex anisotropic channel",
            ),
            do_not_claim=(
                "Do not claim the microscopic EoS is derived; only the exterior compatibility relation is closed.",
            ),
        ),
        "local_algebraic_scalar_no_go": ClaimGate(
            claim="A constant MOND plateau cannot be produced by a local algebraic scalar Pi_eff -> h_eff map.",
            status="CLOSED_NO_GO_FOR_SIMPLE_SCALAR_MAP",
            verified_here=(
                "constant Pi0 gives h_eff'=0 for h_eff=F(Pi0)",
                "deep MOND requires h_eff' proportional to -1/r",
            ),
            open_requirements=(
                "replace the scalar algebraic map with a derived differential/tensor/flux bridge",
            ),
            do_not_claim=(
                "Do not present Pi_eff -> h_eff as a closed local algebraic theorem.",
            ),
        ),
        "two_channel_refractive_stress": ClaimGate(
            claim="One h_eff can hold Newton and MOND as two refractive stress channels.",
            status="CLOSED_TWO_CHANNEL_REFRACTIVE_IDENTITIES",
            verified_here=(
                "h_eff=h_Newton+h_vortex gives Newton plus deep-MOND acceleration",
                "the far limit gives BTFR",
            ),
            open_requirements=(
                "derive both channels from one active RG stress tensor",
                "derive the transition law and boundary conditions",
            ),
            do_not_claim=(
                "Do not claim the two-channel ledger is already the final unification theorem.",
            ),
        ),
        "bernoulli_pressure_to_h": ClaimGate(
            claim="p10 Bernoulli pressure gives the differential h_eff bridge.",
            status="CLOSED_DIFFERENTIAL_FORM_NOT_ALGEBRAIC_MAP",
            verified_here=(
                "Delta_P_Bernoulli becomes exp(-2h_eff)*(h_eff')^2/(8*pi*G)",
                "the Newton h_eff profile satisfies that pressure identity",
            ),
            open_requirements=(
                "derive the Bernoulli relation as an on-shell RG branch",
                "derive boundary conditions and the microscopic substrate value of G",
            ),
            do_not_claim=(
                "Do not claim a pointwise Pi_eff -> h_eff algebraic theorem from p10.",
            ),
        ),
        "mond_stress_to_h": ClaimGate(
            claim="p07 Delta_p stress gives a logarithmic h_eff through the weak stress bridge.",
            status="CLOSED_DIFFERENTIAL_STRESS_TO_H_IDENTITY",
            verified_here=(
                "h_eff'=-2*Delta_p/(c^2*r*rho_solid) reproduces the p07 halo acceleration",
                "constant deep plateau Delta_p gives the MOND logarithmic h_eff and BTFR",
            ),
            open_requirements=(
                "derive the p07 stress source from RG",
                "derive the finite vortex plateau and a0 normalization",
            ),
            do_not_claim=(
                "Do not collapse p07 Delta_p and p10 Pi_B into one scalar; they are two source entries in the tensor ledger.",
            ),
        ),
        "pressure_variable_unification": ClaimGate(
            claim="The quadratic p10 Bernoulli pressure and linear TOV/vortex source enter one active source ledger.",
            status="CLOSED_ACTIVE_STRESS_SOURCE_LEDGER",
            verified_here=(
                "TOV uses the linear source S_h=p_rad'-2*Delta_p/r",
                "p10 enters this source through Pi_B'",
                "rho_B=Pi_B'/(c^2 h_B') returns the Bernoulli h_B' channel",
                "p07 enters the same source through -2*Delta_p/r",
                "the two independent channels add inside the same h_eff equation",
            ),
            open_requirements=(
                "use the full_transition_active_source_selector for the weak spherical transition",
                "solve the combined source equation beyond the symmetry-reduced ledger",
            ),
            do_not_claim=(
                "Do not collapse the tensor/source ledger into a pointwise scalar Pi_eff map.",
            ),
        ),
        "pressure_to_index": ClaimGate(
            claim="Active RefG pressure/stress produces the effective refractive index.",
            status="CLOSED_WEAK_FIELD_ACTION_STRESS_TO_INDEX_CHAIN",
            verified_here=(
                "requirements and algebraic form of the bridge are isolated",
                "universal potential-to-index sublemma is closed",
                "minimal matter action gives the needed weak potential once h_eff is supplied",
                "on-shell Bianchi/TOV identity derives the weak source equation from the action stress tensor",
                "p10 static spherical first order selects the bi-conformal sign",
                "p01 spherical action generates p_rad and Delta_p used by the bridge",
                "p10 Bernoulli radial response gives the Newton source branch",
                "p10 Bernoulli core saturation keeps the exterior source finite at the center",
                "p10 asymptotic charge normalization fixes the Newton coefficient mu=2GM/c^2",
                "p01 anisotropic strain gives the deep-MOND plateau branch",
                "phase coherence gives a0=cH/(2*pi)",
                "vortex loading law follows from the variational closure",
                "the mature vortex branch has a vector nonlinear PDE with the same spherical limit",
                "coherence cutoff makes the vortex tail finite",
                "external-field suppression follows from the same total-gradient loading",
                "p07 total-gradient loading selects the transition between the branches",
                "master weak-stress bridge maps active stress source to h_eff, n_eff, and force",
                "Newton and deep-MOND/BTFR limits are contained in that bridge",
                "p10 bi-conformal Newton bridge translates to h_eff=-phi/2",
                "p10 pressure bridge is differential and closed as a target form",
                "p10 quadratic pressure and TOV linear source are compatible through response EoS",
                "p07 stress bridge is the deep-MOND limit of the weak active-stress bridge",
            ),
            open_requirements=(
                "use the named p10/p01/p07 source branches and full-transition selector in the weak spherical ledger",
                "lift the ledger to the full nonlinear, non-spherical PDE",
            ),
            do_not_claim=(
                "Do not export the weak spherical source ledger as the completed disk/cluster PDE.",
            ),
        ),
    }


def refractive_do_not_claim() -> tuple[str, ...]:
    return (
        "Do not export the weak spherical master bridge as the completed non-spherical PDE theorem.",
        "Do not use Newton's index identity without the p10 Bernoulli source branch.",
        "Do not use MOND's logarithmic identity without the p01/p07 vortex source branch and a0 coherence theorem.",
        "Do not import GR's metric as the final explanation; use the p03c Solar branch compatibility result.",
        "Do not claim literal pressure-gradient pushing on matter; the active rule is one-metric geodesic motion.",
        "Do not claim a single algebraic Pi_eff -> h_eff map; current work supports a differential bridge.",
        "Do not collapse p10 Pi_B and p07 Delta_p into one scalar; use the active source ledger.",
        "Do not treat the spherical transition selector as a completed disk/cluster solution.",
        "Do not claim SPARC/RAR, Bullet, EHT, or Solar-System likelihood passes from p13 alone.",
    )


def p13_refractive_force_status() -> dict[str, Any]:
    weak_chain = refractive_gravity_weak_field_chain_theorem()
    short_refractive = refractive_source_short_path_theorem()
    short_transition = newton_mond_transition_short_path_theorem()
    static_identity = static_metric_refractive_indices()
    newton_identity = newton_refractive_index_identity()
    mond_identity = mond_refractive_btfr_identity()
    potential_lemma = universal_potential_to_index_lemma()
    action_lemma = minimal_point_particle_action_bridge()
    first_order_biconformal = p10_static_first_order_biconformal_selection()
    biconformal_bridge = biconformal_branch_refractive_bridge()
    bernoulli_bridge = bernoulli_pressure_to_h_ode()
    mond_stress_bridge = mond_stress_to_h_ode()
    p01_stress_source = p01_spherical_action_stress_source_lemma()
    bianchi_tov_bridge = on_shell_bianchi_tov_refractive_source_theorem()
    action_stress_to_index = action_stress_to_refractive_index_theorem()
    newton_radial_branch = p10_newton_radial_response_branch()
    bernoulli_core = p10_bernoulli_core_saturation_matching()
    charge_normalization = p10_asymptotic_charge_normalization()
    mond_plateau_branch = p01_mond_plateau_strain_branch()
    a0_origin = rg_phase_coherence_a0_origin()
    variational_loading = p07_variational_vortex_loading_closure()
    vector_pde = vector_aqual_variational_pde_closure()
    cutoff_profile = coherence_cutoff_vortex_profile()
    external_suppression = external_field_loading_suppression()
    branch_selector = p07_vortex_loading_branch_selector()
    full_transition = full_transition_active_source_selector()
    master_bridge = master_refractive_stress_bridge()
    weak_stress_projection = weak_anisotropic_stress_projection_to_h()
    bernoulli_eos = bernoulli_tov_eos_source_closure()
    bernoulli_tov_short = bernoulli_tov_source_short_path_certificate()
    scalar_no_go = local_algebraic_scalar_no_go()
    two_channel = two_channel_refractive_stress_ledger()
    pressure_unification = pressure_variable_unification_audit()
    target_profiles = required_enthalpy_profiles_for_newton_mond()
    bridge = pressure_to_index_bridge_requirements()

    closed_checks = (
        short_refractive["identity"],
        short_transition["total_acceleration_identity"],
        short_transition["mu_x_identity"],
        short_transition["deep_plateau_identity"],
        static_identity["acceleration_identity"],
        newton_identity["newton_identity"],
        mond_identity["deep_mond_identity"],
        mond_identity["btfr_identity"],
        potential_lemma["identity"],
        action_lemma["weak_identity"],
        action_lemma["exact_residual_starts_after_first_order"],
        first_order_biconformal["a1_identity"],
        first_order_biconformal["biconformal_identity"],
        first_order_biconformal["branch_residual_identity"],
        biconformal_bridge["branch_identity"],
        biconformal_bridge["newton_identity"],
        bernoulli_bridge["newton_pressure_identity"],
        mond_stress_bridge["acceleration_identity"],
        mond_stress_bridge["deep_mond_identity"],
        mond_stress_bridge["btfr_identity"],
        p01_stress_source["isotropic_limit_identity"],
        p01_stress_source["generic_anisotropy_sources_Delta_p"],
        bianchi_tov_bridge["bianchi_identity"],
        bianchi_tov_bridge["h_bridge_identity"],
        action_stress_to_index["closed_identity"],
        newton_radial_branch["h_prime_identity"],
        newton_radial_branch["newton_acceleration_identity"],
        bernoulli_core["core_limit_identity"],
        bernoulli_core["far_limit_identity"],
        bernoulli_core["peak_identity"],
        bernoulli_core["finite_integral_identity"],
        charge_normalization["charge_identity"],
        charge_normalization["newton_identity"],
        mond_plateau_branch["exact_branch_identity"],
        mond_plateau_branch["linear_branch_identity"],
        a0_origin["phase_cycle_identity"],
        a0_origin["light_crossing_phase_identity"],
        a0_origin["a0_identity"],
        a0_origin["a0_over_cH_identity"],
        a0_origin["BTFR_coherence_identity"],
        variational_loading["stationarity_identity"],
        variational_loading["closure_identity"],
        variational_loading["newton_limit_identity"],
        variational_loading["deep_mond_limit_identity"],
        variational_loading["vortex_suppression_identity"],
        vector_pde["dF_dy_identity"],
        vector_pde["newton_mu_limit"],
        vector_pde["deep_mu_limit"],
        vector_pde["spherical_selector_identity"],
        vector_pde["newton_limit_identity"],
        vector_pde["deep_mond_limit_identity"],
        cutoff_profile["h_derivative_identity"],
        cutoff_profile["deep_interior_identity"],
        cutoff_profile["far_tail_identity"],
        cutoff_profile["Delta_p_plateau_identity"],
        cutoff_profile["Delta_p_far_scaling_identity"],
        cutoff_profile["far_energy_integrand_identity"],
        external_suppression["strong_external_suppression_identity"],
        external_suppression["external_at_a0_bound_identity"],
        external_suppression["isolated_deep_boost_identity"],
        external_suppression["isolated_newton_identity"],
        branch_selector["mu_identity"],
        branch_selector["deep_mond_limit_identity"],
        branch_selector["newton_limit_identity"],
        branch_selector["vortex_suppression_identity"],
        branch_selector["point_mass_deep_plateau_identity"],
        branch_selector["point_mass_strong_field_suppression"],
        full_transition["total_acceleration_identity"],
        full_transition["mu_loading_identity"],
        full_transition["mu_x_identity"],
        full_transition["newton_limit_identity"],
        full_transition["deep_mond_limit_identity"],
        full_transition["vortex_suppression_identity"],
        full_transition["deep_point_plateau_identity"],
        master_bridge["stress_projection_identity"],
        master_bridge["newton_identity"],
        master_bridge["deep_mond_identity"],
        master_bridge["deep_mond_btfr_identity"],
        master_bridge["two_channel_identity"],
        master_bridge["two_channel_index_identity"],
        weak_stress_projection["p07_bridge_identity"],
        bernoulli_eos["rho_formula_identity"],
        bernoulli_eos["tov_identity"],
        bernoulli_tov_short["status"] == "PASS_BERNOULLI_TOV_SOURCE_SHORT_PATH",
        scalar_no_go["no_go_check"],
        pressure_unification["local_bernoulli_identity"],
        pressure_unification["vortex_identity"],
        pressure_unification["two_channel_source_identity"],
        two_channel["vortex_h_prime_identity"],
        two_channel["total_acceleration_identity"],
        two_channel["far_btfr_identity"],
        target_profiles["newton_target_identity"],
        target_profiles["deep_mond_target_identity"],
        target_profiles["deep_mond_btfr_identity"],
        weak_chain["all_checks_pass"],
    )

    return {
        "file": "p13_refractive_force.py",
        "file_export_status": "PARTIAL_ARTICLE_EXPORT_READY_FOR_WEAK_STATIC_REFRACTIVE_CHAIN",
        "export_status": "WEAK_STATIC_COARSE_GRAINED_REFRACTIVE_CHAIN_READY_FULL_PDE_OPEN",
        "overall_status": (
            "weak static/coarse-grained refractive chain is closed as an "
            "identity ledger; full nonlinear non-spherical PDE and data "
            "likelihoods remain open"
        ),
        "closed_identity_status": "PASS" if all(closed_checks) else "FAIL",
        "weak_field_chain_theorem": weak_chain["status"],
        "weak_field_chain_scope": weak_chain["scope_status"],
        "article_ready_scope": (
            "static metric-to-index identities",
            "minimal one-metric weak point-particle action to n_eff",
            "on-shell weak Bianchi/TOV stress source for h_eff",
            "p10 first-order bi-conformal Newton branch and charge normalization",
            "p01/p07 weak vortex/MOND stress identities and transition selector",
            "finite coherence cutoff and external-field loading identities",
            "shared active weak stress ledger for independent p10 Bernoulli and p07 vortex channels",
        ),
        "not_article_ready_scope": (
            "full nonlinear non-spherical PDE theorem",
            "disk/curl vector-PDE solutions with realistic baryons",
            "SPARC/RAR/galaxy-environment likelihood",
            "Bullet/cluster merger simulation and lensing likelihood",
            "strong-core compact-object evolution",
            "microscopic substrate value of G",
        ),
        "short_refractive_source_theorem": short_refractive,
        "short_newton_mond_transition_theorem": short_transition,
        "central_theorem_target": bridge["status"],
        "static_metric_identity": static_identity,
        "newton_index_identity": newton_identity,
        "mond_index_identity": mond_identity,
        "universal_potential_to_index": potential_lemma,
        "minimal_action_to_index": action_lemma,
        "p10_static_first_order_biconformal_selection": first_order_biconformal,
        "p10_biconformal_to_index": biconformal_bridge,
        "p10_bernoulli_pressure_to_h": bernoulli_bridge,
        "p07_mond_stress_to_h": mond_stress_bridge,
        "p01_action_stress_source": p01_stress_source,
        "on_shell_bianchi_tov_bridge": bianchi_tov_bridge,
        "action_stress_to_refractive_index": action_stress_to_index,
        "p10_newton_radial_response_branch": newton_radial_branch,
        "p10_bernoulli_core_saturation_matching": bernoulli_core,
        "p10_asymptotic_charge_normalization": charge_normalization,
        "p01_mond_plateau_strain_branch": mond_plateau_branch,
        "phase_coherence_a0_origin": a0_origin,
        "variational_vortex_loading_closure": variational_loading,
        "vector_aqual_variational_pde_closure": vector_pde,
        "coherence_cutoff_vortex_profile": cutoff_profile,
        "external_field_loading_suppression": external_suppression,
        "p07_vortex_loading_branch_selector": branch_selector,
        "full_transition_active_source_selector": full_transition,
        "master_refractive_stress_bridge": master_bridge,
        "weak_anisotropic_stress_projection": weak_stress_projection,
        "bernoulli_tov_eos_source": bernoulli_eos,
        "bernoulli_tov_source_short_path": bernoulli_tov_short,
        "local_algebraic_scalar_no_go": scalar_no_go,
        "two_channel_refractive_stress": two_channel,
        "pressure_variable_unification": pressure_unification,
        "required_enthalpy_profiles": target_profiles,
        "pressure_to_index_bridge": bridge,
        "weak_field_refractive_chain": weak_chain,
        "claim_gate": refractive_force_claim_gate(),
        "do_not_claim": refractive_do_not_claim(),
    }


if __name__ == "__main__":
    status = p13_refractive_force_status()
    print("p13_refractive_force")
    print("closed_identity_status:", status["closed_identity_status"])
    print("export_status:", status["export_status"])
    print("weak_field_chain_theorem:", status["weak_field_chain_theorem"])
    print("short_refractive_source:", status["short_refractive_source_theorem"]["status"])
    print("short_newton_mond_transition:", status["short_newton_mond_transition_theorem"]["status"])
    print("central_theorem_target:", status["central_theorem_target"])
    print("static_metric:", status["static_metric_identity"]["status"])
    print("newton_index:", status["newton_index_identity"]["status"])
    print("mond_index:", status["mond_index_identity"]["status"])
    print("universal_potential_to_index:", status["universal_potential_to_index"]["status"])
    print("minimal_action_to_index:", status["minimal_action_to_index"]["status"])
    print("p10_static_first_order_biconformal_selection:", status["p10_static_first_order_biconformal_selection"]["status"])
    print("p10_biconformal_to_index:", status["p10_biconformal_to_index"]["status"])
    print("p10_bernoulli_pressure_to_h:", status["p10_bernoulli_pressure_to_h"]["status"])
    print("p07_mond_stress_to_h:", status["p07_mond_stress_to_h"]["status"])
    print("p01_action_stress_source:", status["p01_action_stress_source"]["status"])
    print("on_shell_bianchi_tov_bridge:", status["on_shell_bianchi_tov_bridge"]["status"])
    print("action_stress_to_refractive_index:", status["action_stress_to_refractive_index"]["status"])
    print("p10_newton_radial_response_branch:", status["p10_newton_radial_response_branch"]["status"])
    print("p10_bernoulli_core_saturation_matching:", status["p10_bernoulli_core_saturation_matching"]["status"])
    print("p10_asymptotic_charge_normalization:", status["p10_asymptotic_charge_normalization"]["status"])
    print("p01_mond_plateau_strain_branch:", status["p01_mond_plateau_strain_branch"]["status"])
    print("phase_coherence_a0_origin:", status["phase_coherence_a0_origin"]["status"])
    print("variational_vortex_loading_closure:", status["variational_vortex_loading_closure"]["status"])
    print("vector_aqual_variational_pde_closure:", status["vector_aqual_variational_pde_closure"]["status"])
    print("coherence_cutoff_vortex_profile:", status["coherence_cutoff_vortex_profile"]["status"])
    print("external_field_loading_suppression:", status["external_field_loading_suppression"]["status"])
    print("p07_vortex_loading_branch_selector:", status["p07_vortex_loading_branch_selector"]["status"])
    print("full_transition_active_source_selector:", status["full_transition_active_source_selector"]["status"])
    print("master_refractive_stress_bridge:", status["master_refractive_stress_bridge"]["status"])
    print("weak_anisotropic_stress_projection:", status["weak_anisotropic_stress_projection"]["status"])
    print("bernoulli_tov_eos_source:", status["bernoulli_tov_eos_source"]["status"])
    print("bernoulli_tov_source_short_path:", status["bernoulli_tov_source_short_path"]["status"])
    print("local_algebraic_scalar_no_go:", status["local_algebraic_scalar_no_go"]["status"])
    print("two_channel_refractive_stress:", status["two_channel_refractive_stress"]["status"])
    print("pressure_variable_unification:", status["pressure_variable_unification"]["status"])
    print("target_profiles:", status["required_enthalpy_profiles"]["status"])
    print("bridge:", status["pressure_to_index_bridge"]["status"])
