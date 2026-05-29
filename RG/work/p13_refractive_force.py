# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: c_Y denotes the Y-scheme coefficient c_Y^(Y).

"""
p13_refractive_force.py

Work ledger for the literal "refractive" part of RefG.

This file does not claim the final proof. It separates three layers:

1. closed geometric/mechanical identities:
   if a static metric or an effective matter index is already given,
   motion can be written as motion in an index gradient;
2. action-level weak-field lemma:
   if matter is minimally coupled to one physical static metric, the
   point-particle action gives a universal weak scalar potential;
3. conditional Newton/MOND identities:
   if the index profile has the Newton or deep-MOND form, the standard
   force laws follow;
4. the primary open theorem:
   derive that effective index from the active RefG stress/pressure sector.

Only layer 4 can make the name "Refractive Gravity" fully literal inside
the RG theory. Until that bridge is proved, Newton/MOND recovery is still
conditional on an index profile or closure.
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
            "Derive this index profile and its source normalization from the RG action/"
            "stress sector, consistently with p10."
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
            "Derive the logarithmic index and a0 normalization from the RG vortex/"
            "pressure closure, consistently with p07."
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

    This does not yet derive F(Pi_eff) from the RG action. It closes only the
    mechanical step from a universal scalar coupling to a refractive index.
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
            "The refractive force is mechanically proved once the RG action "
            "produces a universal scalar potential F(Pi_eff)."
        ),
        "still_open": (
            "derive the universal matter coupling from the RG action",
            "derive Pi_eff and F from the active stress variables",
            "prove that the coupling is composition-independent",
            "prove that the same coupling gives the Newton and MOND profiles",
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

    return {
        "status": "PASS_BICONFORMAL_BRANCH_TO_REFRACTIVE_NEWTON_IF_BRANCH_AND_NORMALIZATION_GIVEN",
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
        "still_open": (
            "derive the bi-conformal branch from the full p01 static equations",
            "derive phi=-2GM/(c^2 r) and the source normalization",
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
        "status": "PASS_MOND_STRESS_TO_H_DIFFERENTIAL_FORM_IF_P07_BRIDGE_ASSUMED",
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
            "The p07 plateau stress gives the logarithmic refractive h_eff if "
            "the p07 acceleration bridge is derived."
        ),
        "still_open": (
            "derive g_h=2*Delta_p/(r*rho_solid) from the RG action",
            "derive the constant plateau amplitude and finite-radius cutoff",
            "derive a0 normalization",
        ),
    }


def pressure_variable_unification_audit() -> dict[str, Any]:
    """
    Do not silently identify p10 Bernoulli pressure with p07 vortex Delta_p.

    The local-source branch uses a Bernoulli pressure deficit tied to h_eff'^2.
    The galactic branch uses an anisotropic/vortex stress tied linearly to
    h_eff'.  They may be two limits of one active stress tensor, but that is
    not proved here.
    """

    return {
        "status": "OPEN_SINGLE_PI_EFF_UNIFICATION",
        "bernoulli_tov_eos": bernoulli_tov_eos_source_closure()["status"],
        "weak_stress_projection": weak_anisotropic_stress_projection_to_h()["status"],
        "single_scalar_no_go": local_algebraic_scalar_no_go()["status"],
        "two_channel_working_ledger": two_channel_refractive_stress_ledger()["status"],
        "local_source_pressure": (
            "p10 Delta_P_Bernoulli controls h_eff'^2 and supports the Newton 1/r profile"
        ),
        "galactic_vortex_stress": (
            "p07 Delta_p controls h_eff' through the assumed acceleration bridge "
            "and supports the MOND logarithmic profile"
        ),
        "no_go_for_simple_algebraic_map": (
            "A single pointwise algebraic Pi_eff -> h_eff is not supported by "
            "the current p10 Bernoulli structure; the bridge is differential."
        ),
        "required_for_unification": (
            "derive both Delta_P_Bernoulli and Delta_p_vortex from one active RG stress tensor",
            "derive the Bernoulli response density from the p01/p10 action",
            "show their regime limits and transition law",
            "prove the same h_eff sources the one physical metric",
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
        "status": "PASS_WEAK_ANISOTROPIC_STRESS_PROJECTION_TO_H_WITH_CAVEATS",
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
        "still_open": (
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
    Working unification ledger: one refractive h_eff with two stress channels.

    This is not the final stress-tensor theorem.  It records the minimal form
    that can hold both active limits without falsifying either:

        h_eff = h_Newton + h_vortex

    with h_Newton supported by the p10 Bernoulli/localized-source branch and
    h_vortex supported by the p07 vortex/Delta_p branch.
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
        "status": "PASS_TWO_CHANNEL_REFRACTIVE_LEDGER_IF_STRESS_CHANNELS_DERIVED",
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
        "meaning": (
            "A single refractive h_eff can carry both Newton and MOND behavior "
            "if the local Bernoulli channel and the vortex anisotropic channel "
            "are both derived from the active RG stress tensor."
        ),
        "still_open": (
            "derive the two stress channels from one RG action",
            "derive the regime selector/transition between local source and vortex response",
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


def pressure_to_index_bridge_requirements() -> dict[str, Any]:
    """Central open theorem: map the active RG pressure sector to an index."""

    r, c = sp.symbols("r c", positive=True)
    Pi = sp.Function("Pi_eff")(r)
    F = sp.Function("F")
    log_n = F(Pi)
    radial_acceleration = sp.diff(c**2 * log_n, r)

    return {
        "status": "OPEN_PRIMARY_REFRACTIVE_BRIDGE",
        "algebraic_ansatz_status": "NOT_CLOSED_AND_DISFAVORED_AS_A_SINGLE_LOCAL_MAP",
        "differential_bridge_status": "CURRENT_WORKING_FORM",
        "index_definition": "n_eff = exp(h_eff)",
        "radial_acceleration": radial_acceleration,
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
        "required_closures": (
            "derive Pi_eff from T^RefG_mn or the active RG stress variables",
            "derive a differential h_eff equation, not a hand-chosen local F",
            "derive the Bernoulli response density from the active medium action",
            "derive the universal test-matter potential V_eff/m = -c^2 F(Pi_eff)",
            "derive g_tt=exp(-2F(Pi_eff)) as the one physical metric branch",
            "fix sign and normalization without using a phantom sign",
            "recover the Newton 1/r index in the local source regime",
            "recover the logarithmic deep-MOND index in the galaxy regime",
            "show compatibility with the Solar GR branch from p03b",
        ),
        "meaning": (
            "This is the theorem that must be closed before the word "
            "'refractive' is fully proved inside RG."
        ),
    }


def refractive_force_claim_gate() -> dict[str, ClaimGate]:
    return {
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
            status="CONDITIONAL_IDENTITY",
            verified_here=(
                "n_matter = exp(GM/(c^2 r)) gives radial acceleration -GM/r^2",
            ),
            open_requirements=(
                "derive n_matter = exp(GM/(c^2 r)) from the RG source/stress sector",
                "match normalization to the p10 Newton branch",
            ),
            do_not_claim=(
                "Do not claim Newton gravity mechanism is derived from RG action yet.",
            ),
        ),
        "mond_from_index": ClaimGate(
            claim="Deep-MOND force and BTFR follow from a logarithmic refractive index.",
            status="CONDITIONAL_IDENTITY",
            verified_here=(
                "logarithmic index gives acceleration -sqrt(GMa0)/r",
                "circular motion then gives v^4 = GMa0",
            ),
            open_requirements=(
                "derive the logarithmic index from the RG vortex/pressure closure",
                "derive a0 normalization, not merely postulate it",
            ),
            do_not_claim=(
                "Do not claim p07 MOND closure is derived by this file.",
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
                "derive V_eff/m = -c^2 F(Pi_eff) from the RG action",
                "prove universality and composition independence",
            ),
            do_not_claim=(
                "Do not claim active RG pressure already produces that potential.",
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
                "derive h_eff from the active RG metric/stress equations",
                "derive the static branch rather than imposing g_tt=exp(-2h_eff)",
            ),
            do_not_claim=(
                "Do not claim pressure directly pushes matter; p01/p10 use one-metric geodesic motion.",
            ),
        ),
        "p10_biconformal_to_index": ClaimGate(
            claim="The p10 bi-conformal Newton bridge is a refractive-index bridge.",
            status="CONDITIONAL_ON_P10_BRANCH_AND_NORMALIZATION",
            verified_here=(
                "for ds^2=exp(phi)c^2dt^2-exp(-phi)dSigma^2, h_eff=-phi/2",
                "phi=-2GM/(c^2r) gives n_eff=exp(GM/(c^2r)) and Newton acceleration",
            ),
            open_requirements=(
                "derive the bi-conformal branch from p01",
                "derive the source-to-G normalization from finite-energy sources",
            ),
            do_not_claim=(
                "Do not claim p10 already proves the full RG action-to-Newton theorem.",
            ),
        ),
        "weak_anisotropic_stress_projection": ClaimGate(
            claim="The p07 halo acceleration bridge follows from weak anisotropic stress projection under clear assumptions.",
            status="CLOSED_TO_P07_LIMIT_WITH_CAVEATS",
            verified_here=(
                "p_rad' + rho_inert Phi_N' - 2*Delta_p/r = 0 with Phi_N=-c^2 h_eff",
                "p_rad'=0 and rho_inert=rho_solid give h_eff'=-2*Delta_p/(c^2*r*rho_solid)",
            ),
            open_requirements=(
                "derive the projection from p01, not only from weak TOV bookkeeping",
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
            status="CONDITIONAL_LEDGER",
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
                "derive source normalization and boundary conditions",
            ),
            do_not_claim=(
                "Do not claim a pointwise Pi_eff -> h_eff algebraic theorem from p10.",
            ),
        ),
        "mond_stress_to_h": ClaimGate(
            claim="p07 Delta_p stress gives a logarithmic h_eff when the acceleration bridge is assumed.",
            status="CONDITIONAL_DIFFERENTIAL_BRIDGE",
            verified_here=(
                "h_eff'=-2*Delta_p/(c^2*r*rho_solid) reproduces the p07 halo acceleration",
                "constant deep plateau Delta_p gives the MOND logarithmic h_eff and BTFR",
            ),
            open_requirements=(
                "derive the p07 acceleration bridge from RG",
                "derive the finite vortex plateau and a0 normalization",
            ),
            do_not_claim=(
                "Do not identify p07 Delta_p with p10 Delta_P_Bernoulli until the stress tensor unification is proved.",
            ),
        ),
        "pressure_variable_unification": ClaimGate(
            claim="One active RG stress variable unifies the local Newton and galactic MOND pressure bridges.",
            status="OPEN_CORE_UNIFICATION_THEOREM",
            verified_here=(
                "the local and galactic target bridge forms are isolated",
            ),
            open_requirements=(
                "derive both pressure/stress variables from one RG stress tensor",
                "derive their regime split and transition law",
            ),
            do_not_claim=(
                "Do not write Pi_eff as a single finished scalar unless this theorem is closed.",
            ),
        ),
        "pressure_to_index": ClaimGate(
            claim="Active RefG pressure/stress produces the effective refractive index.",
            status="PRIMARY_OPEN_THEOREM",
            verified_here=(
                "requirements and algebraic form of the bridge are isolated",
                "universal potential-to-index sublemma is closed",
                "minimal matter action gives the needed weak potential once h_eff is supplied",
                "p10 bi-conformal Newton bridge translates to h_eff=-phi/2",
                "p10 pressure bridge is differential and closed as a target form",
                "p10 quadratic pressure and TOV linear source are compatible through response EoS",
                "p07 stress bridge is differential and conditional on the MOND acceleration bridge",
            ),
            open_requirements=(
                "derive Pi_eff from the active RG variables",
                "derive the map Pi_eff -> n_eff",
                "prove Newton and MOND limits from the same bridge",
            ),
            do_not_claim=(
                "Do not claim the refractive force is fully proved until this bridge closes.",
            ),
        ),
    }


def refractive_do_not_claim() -> tuple[str, ...]:
    return (
        "Do not claim the title 'Refractive Gravity' is mathematically secured yet.",
        "Do not claim Newton's mechanism is derived from RG until the pressure-to-index bridge is closed.",
        "Do not claim MOND is proved until the logarithmic index and a0 emerge from RG dynamics.",
        "Do not import GR's metric as the final explanation; use it only as a compatibility identity.",
        "Do not claim literal pressure-gradient pushing on matter; the active rule is one-metric geodesic motion.",
        "Do not claim a single algebraic Pi_eff -> h_eff map; current work supports a differential bridge.",
        "Do not identify p10 Bernoulli pressure with p07 vortex Delta_p until the stress unification theorem is proved.",
        "Do not claim the Bernoulli response EoS is microderived; p13 closes only the exterior compatibility relation.",
    )


def p13_refractive_force_status() -> dict[str, Any]:
    static_identity = static_metric_refractive_indices()
    newton_identity = newton_refractive_index_identity()
    mond_identity = mond_refractive_btfr_identity()
    potential_lemma = universal_potential_to_index_lemma()
    action_lemma = minimal_point_particle_action_bridge()
    biconformal_bridge = biconformal_branch_refractive_bridge()
    bernoulli_bridge = bernoulli_pressure_to_h_ode()
    mond_stress_bridge = mond_stress_to_h_ode()
    weak_stress_projection = weak_anisotropic_stress_projection_to_h()
    bernoulli_eos = bernoulli_tov_eos_source_closure()
    scalar_no_go = local_algebraic_scalar_no_go()
    two_channel = two_channel_refractive_stress_ledger()
    pressure_unification = pressure_variable_unification_audit()
    target_profiles = required_enthalpy_profiles_for_newton_mond()
    bridge = pressure_to_index_bridge_requirements()

    closed_checks = (
        static_identity["acceleration_identity"],
        newton_identity["newton_identity"],
        mond_identity["deep_mond_identity"],
        mond_identity["btfr_identity"],
        potential_lemma["identity"],
        action_lemma["weak_identity"],
        action_lemma["exact_residual_starts_after_first_order"],
        biconformal_bridge["branch_identity"],
        biconformal_bridge["newton_identity"],
        bernoulli_bridge["newton_pressure_identity"],
        mond_stress_bridge["acceleration_identity"],
        mond_stress_bridge["deep_mond_identity"],
        mond_stress_bridge["btfr_identity"],
        weak_stress_projection["p07_bridge_identity"],
        bernoulli_eos["rho_formula_identity"],
        bernoulli_eos["tov_identity"],
        scalar_no_go["no_go_check"],
        two_channel["vortex_h_prime_identity"],
        two_channel["total_acceleration_identity"],
        two_channel["far_btfr_identity"],
        target_profiles["newton_target_identity"],
        target_profiles["deep_mond_target_identity"],
        target_profiles["deep_mond_btfr_identity"],
    )

    return {
        "file": "p13_refractive_force.py",
        "export_status": "WORK_LEDGER_ONLY_NOT_READY_FOR_ARTICLE_EXPORT",
        "closed_identity_status": "PASS" if all(closed_checks) else "FAIL",
        "central_open_problem": bridge["status"],
        "static_metric_identity": static_identity,
        "newton_index_identity": newton_identity,
        "mond_index_identity": mond_identity,
        "universal_potential_to_index": potential_lemma,
        "minimal_action_to_index": action_lemma,
        "p10_biconformal_to_index": biconformal_bridge,
        "p10_bernoulli_pressure_to_h": bernoulli_bridge,
        "p07_mond_stress_to_h": mond_stress_bridge,
        "weak_anisotropic_stress_projection": weak_stress_projection,
        "bernoulli_tov_eos_source": bernoulli_eos,
        "local_algebraic_scalar_no_go": scalar_no_go,
        "two_channel_refractive_stress": two_channel,
        "pressure_variable_unification": pressure_unification,
        "required_enthalpy_profiles": target_profiles,
        "pressure_to_index_bridge": bridge,
        "claim_gate": refractive_force_claim_gate(),
        "do_not_claim": refractive_do_not_claim(),
    }


if __name__ == "__main__":
    status = p13_refractive_force_status()
    print("p13_refractive_force")
    print("closed_identity_status:", status["closed_identity_status"])
    print("export_status:", status["export_status"])
    print("central_open_problem:", status["central_open_problem"])
    print("static_metric:", status["static_metric_identity"]["status"])
    print("newton_index:", status["newton_index_identity"]["status"])
    print("mond_index:", status["mond_index_identity"]["status"])
    print("universal_potential_to_index:", status["universal_potential_to_index"]["status"])
    print("minimal_action_to_index:", status["minimal_action_to_index"]["status"])
    print("p10_biconformal_to_index:", status["p10_biconformal_to_index"]["status"])
    print("p10_bernoulli_pressure_to_h:", status["p10_bernoulli_pressure_to_h"]["status"])
    print("p07_mond_stress_to_h:", status["p07_mond_stress_to_h"]["status"])
    print("weak_anisotropic_stress_projection:", status["weak_anisotropic_stress_projection"]["status"])
    print("bernoulli_tov_eos_source:", status["bernoulli_tov_eos_source"]["status"])
    print("local_algebraic_scalar_no_go:", status["local_algebraic_scalar_no_go"]["status"])
    print("two_channel_refractive_stress:", status["two_channel_refractive_stress"]["status"])
    print("pressure_variable_unification:", status["pressure_variable_unification"]["status"])
    print("target_profiles:", status["required_enthalpy_profiles"]["status"])
    print("bridge:", status["pressure_to_index_bridge"]["status"])
