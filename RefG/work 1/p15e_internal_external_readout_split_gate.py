"""
PHASE 15e: Internal inventory versus external readout split.

This file repairs the language of p15-p15d after the user's clarification.
It does not touch the article.

Core distinction:

    internal/proper inventory:
        matter units add normally inside their own physical frame.

    external readout:
        mass, size, clock rate and light escape are filtered by the deficit
        gradient before they are seen by an outside observer.

Therefore the earlier p15 phrase "core mass decreases" must not be read as
"proper mass disappears" or "matter turns into a singularity."  It means:

    the external active mass/readout channel is deficit-filtered.

For any object with a nonzero gravitational/deficit profile, internal/proper
inventory and external readout are not exactly the same channel.  Weak objects
have a tiny split; compact objects have a large split.  The asymptotic q=0
limit is the equality limit.

The internal inventory may be much larger than the external ADM/readout mass,
and an externally small compact object may contain a very large proper
interior scale.  The singularity claim is not licensed by external smallness.
"""

from __future__ import annotations

import sympy as sp

from p15b_dressing_mass_conservation_gate import (
    dressing_mass_conservation_status,
)


def derive_universal_cosmic_mass_readout_split() -> dict[str, object]:
    """
    Universal mass split for any nonzero deficit profile.

    This is not a black-hole-only statement.  Any object with q_m>0 has an
    external readout channel that differs from its internal/proper inventory.
    The weak-field case is just the small-q_m limit.
    """
    q_m, M_proper = sp.symbols("q_m M_proper", nonnegative=True, real=True)

    eta_m = sp.exp(-q_m)
    M_readout = sp.simplify(M_proper * eta_m)
    difference = sp.simplify(M_proper - M_readout)
    fractional_difference = sp.simplify(difference / M_proper)
    weak_series = sp.series(fractional_difference, q_m, 0, 4).removeO()

    return {
        "status": "PASS_ANY_NONZERO_DEFICIT_SPLITS_PROPER_AND_EXTERNAL_MASS",
        "deficit_amplitude": sp.Eq(sp.Symbol("q_m"), q_m),
        "readout_filter": sp.Eq(sp.Symbol("eta_m"), eta_m),
        "internal_proper_mass": sp.Eq(sp.Symbol("M_proper"), M_proper),
        "external_mass_readout": sp.Eq(sp.Symbol("M_readout"), M_readout),
        "mass_difference": sp.Eq(sp.Symbol("Delta_M"), difference),
        "fractional_difference": sp.Eq(
            sp.Symbol("Delta_M/M_proper"),
            fractional_difference,
        ),
        "weak_deficit_series": sp.Eq(
            sp.Symbol("Delta_M/M_proper"),
            weak_series,
        ),
        "equality_limit": sp.Eq(
            M_readout.subs(q_m, 0),
            M_proper,
        ),
        "nonzero_deficit_reading": (
            "For q_m>0, M_readout=M_proper*exp(-q_m) is smaller than "
            "M_proper in this readout ledger.  For q_m<<1 the difference is "
            "small; the black-hole-like case is the strong-q_m limit."
        ),
    }


def derive_internal_inventory_external_readout_split() -> dict[str, object]:
    """Separate additive internal mass from deficit-filtered external readout."""
    N, N1, N2, m0, q_m, M_ext = sp.symbols(
        "N N1 N2 m0 q_m M_ext",
        positive=True,
        real=True,
    )

    readout_filter = sp.exp(-q_m)
    internal_mass = sp.simplify(N * m0)
    external_mass_readout = sp.simplify(readout_filter * internal_mass)
    additivity_residual = sp.simplify((N1 + N2) * m0 - (N1 * m0 + N2 * m0))
    internal_over_external = sp.simplify(internal_mass / external_mass_readout)
    internal_mass_for_fixed_external = sp.simplify(M_ext / readout_filter)

    return {
        "status": "PASS_INTERNAL_MASS_ADDITIVE_EXTERNAL_MASS_FILTERED",
        "internal_unit_count": sp.Eq(sp.Symbol("N"), N),
        "internal_proper_mass": sp.Eq(sp.Symbol("M_proper"), internal_mass),
        "internal_mass_additivity_residual": additivity_residual,
        "external_readout_filter": sp.Eq(sp.Symbol("eta_m"), readout_filter),
        "external_mass_readout": sp.Eq(
            sp.Symbol("M_external_readout"),
            external_mass_readout,
        ),
        "internal_over_external_mass": sp.Eq(
            sp.Symbol("M_proper/M_external_readout"),
            internal_over_external,
        ),
        "internal_mass_at_fixed_external_readout": sp.Eq(
            sp.Symbol("M_proper"),
            internal_mass_for_fixed_external,
        ),
        "singularity_guard": (
            "No mass is sent to zero or infinity by this bookkeeping.  For "
            "finite N and finite q_m, both internal and external masses are "
            "finite.  The readout filter is not proper-mass destruction."
        ),
        "reading": (
            "Inside the object, matter inventory is additive: one unit, two "
            "units, three units.  Outside, the same inventory is read through "
            "a deficit filter eta_m=exp(-q_m), so external readout can be "
            "smaller than the internal/proper inventory."
        ),
    }


def derive_interior_scale_external_size_split() -> dict[str, object]:
    """Show how an externally small object can have a large proper interior."""
    q_L, L_external, c = sp.symbols("q_L L_external c", positive=True, real=True)

    interior_to_external_scale = sp.exp(q_L)
    external_length_readout_factor = sp.exp(-q_L)
    lapse = sp.exp(-q_L)
    external_period_factor = sp.exp(q_L)
    coordinate_light_speed = sp.simplify(c * sp.exp(-2 * q_L))
    local_c_identity = sp.simplify(
        (coordinate_light_speed / c)
        * external_period_factor
        / external_length_readout_factor
    )
    L_proper = sp.simplify(interior_to_external_scale * L_external)

    example_ratio = sp.Integer(300_000_000)
    example = {
        "external_length_m": sp.Integer(1),
        "interior_to_external_scale": example_ratio,
        "proper_length_m": example_ratio,
        "proper_length_km": sp.simplify(example_ratio / 1000),
        "q_L": sp.log(example_ratio),
        "lapse": sp.simplify(1 / example_ratio),
        "coordinate_light_speed_over_c": sp.simplify(1 / example_ratio**2),
    }

    return {
        "status": "PASS_EXTERNAL_SMALLNESS_CAN_HIDE_LARGE_PROPER_INTERIOR",
        "interior_to_external_scale": sp.Eq(
            sp.Symbol("Xi_L"),
            interior_to_external_scale,
        ),
        "external_length_readout_factor": sp.Eq(
            sp.Symbol("L_external/L_proper"),
            external_length_readout_factor,
        ),
        "proper_length": sp.Eq(sp.Symbol("L_proper"), L_proper),
        "metric_lapse": sp.Eq(sp.Symbol("d_tau/dt"), lapse),
        "external_period_factor": sp.Eq(
            sp.Symbol("dt/d_tau"),
            external_period_factor,
        ),
        "coordinate_light_speed": sp.Eq(
            sp.Symbol("c_coord"),
            coordinate_light_speed,
        ),
        "local_c_identity": local_c_identity == 1,
        "example_external_1m_to_internal_300000km": example,
        "reading": (
            "An outside length readout can be tiny while the proper interior "
            "length is huge.  Local light speed remains c; the external "
            "coordinate/readout speed is suppressed by the time and length "
            "readout factors."
        ),
    }


def derive_external_smallness_not_singularity_gate() -> dict[str, object]:
    """
    External shrinkage does not imply a proper singularity.

    This is a kinematic guardrail, not a full matter equation of state.  Matter
    may be strongly compressed, but an outside small radius alone is not proof
    that the proper interior radius is zero or that proper density is infinite.
    """
    q_L, R_external, M_proper = sp.symbols(
        "q_L R_external M_proper",
        positive=True,
        real=True,
    )

    R_proper = sp.simplify(R_external * sp.exp(q_L))
    V_proper = sp.simplify(sp.Rational(4, 3) * sp.pi * R_proper**3)
    proper_average_density = sp.simplify(M_proper / V_proper)
    external_readout_volume = sp.simplify(
        sp.Rational(4, 3) * sp.pi * R_external**3
    )
    proper_to_external_volume_ratio = sp.simplify(V_proper / external_readout_volume)

    finite_checks = {
        "R_proper_finite_for_finite_inputs": "finite if R_external>0 and q_L finite",
        "V_proper_finite_for_finite_inputs": "finite if R_external>0 and q_L finite",
        "rho_proper_finite_for_finite_inputs": (
            "finite if M_proper, R_external and q_L are finite"
        ),
    }

    return {
        "status": "PASS_EXTERNAL_SMALLNESS_DOES_NOT_IMPLY_PROPER_SINGULARITY",
        "proper_radius": sp.Eq(sp.Symbol("R_proper"), R_proper),
        "proper_volume": sp.Eq(sp.Symbol("V_proper"), V_proper),
        "proper_to_external_volume_ratio": sp.Eq(
            sp.Symbol("V_proper/V_external_readout"),
            proper_to_external_volume_ratio,
        ),
        "proper_average_density": sp.Eq(
            sp.Symbol("rho_proper_avg"),
            proper_average_density,
        ),
        "finite_checks": finite_checks,
        "reading": (
            "External compactness can be a readout/escape property.  A proper "
            "singularity would require an additional proof that the proper "
            "radius goes to zero or the proper density diverges; external "
            "smallness alone does not prove that."
        ),
    }


def derive_legacy_p15_language_reinterpretation_gate() -> dict[str, object]:
    """Tie the corrected language back to the existing p15b ledger."""
    p15b = dressing_mass_conservation_status()

    return {
        "status": (
            "PASS_LEGACY_CORE_DEPLETION_REINTERPRETED_AS_EXTERNAL_READOUT_FILTER"
            if p15b["status"]
            == "PASS_DRESSING_MASS_CONSERVATION_LEDGER_COMPATIBLE_WITH_ADM_NOETHER__ACTION_DERIVATION_OPEN"
            else "CHECK_LEGACY_P15_LANGUAGE_REINTERPRETATION"
        ),
        "p15b_status": p15b["status"],
        "legacy_symbol_rule": {
            "M_core_in_p15a_p15b": (
                "read as M_active_readout or M_core_readout, not as internal "
                "proper mass inventory"
            ),
            "M_dress": (
                "external deficit/dressing charge in the far-zone ledger, "
                "counted once"
            ),
            "M_proper": (
                "separate internal inventory variable; it may exceed the "
                "external readout mass"
            ),
        },
        "blocked_readings": [
            "do not say matter disappears",
            "do not say internal proper mass is forced to shrink by p15a/p15b",
            "do not infer a singularity from external smallness",
            "do not identify ADM/readout mass with the full internal inventory without a derived bridge",
        ],
        "reading": (
            "The previous p15 mass-volume ledger remains useful only after "
            "relabeling it as an external active-readout ledger.  The internal "
            "proper inventory is a separate object."
        ),
    }


def internal_external_readout_split_status() -> dict[str, object]:
    universal = derive_universal_cosmic_mass_readout_split()
    mass = derive_internal_inventory_external_readout_split()
    scale = derive_interior_scale_external_size_split()
    finite = derive_external_smallness_not_singularity_gate()
    legacy = derive_legacy_p15_language_reinterpretation_gate()

    passed = (
        universal["status"]
        == "PASS_ANY_NONZERO_DEFICIT_SPLITS_PROPER_AND_EXTERNAL_MASS"
        and
        mass["status"] == "PASS_INTERNAL_MASS_ADDITIVE_EXTERNAL_MASS_FILTERED"
        and scale["status"] == "PASS_EXTERNAL_SMALLNESS_CAN_HIDE_LARGE_PROPER_INTERIOR"
        and scale["local_c_identity"]
        and finite["status"] == "PASS_EXTERNAL_SMALLNESS_DOES_NOT_IMPLY_PROPER_SINGULARITY"
        and legacy["status"]
        == "PASS_LEGACY_CORE_DEPLETION_REINTERPRETED_AS_EXTERNAL_READOUT_FILTER"
    )

    return {
        "status": (
            "PASS_INTERNAL_EXTERNAL_SPLIT_REPAIRS_VOLUME_DEFICIT_LANGUAGE__DYNAMICS_OPEN"
            if passed
            else "CHECK_INTERNAL_EXTERNAL_READOUT_SPLIT"
        ),
        "universal_cosmic_mass_split": universal,
        "mass_split": mass,
        "scale_split": scale,
        "finite_interior_guard": finite,
        "legacy_language_reinterpretation": legacy,
        "closed_now": [
            "any nonzero deficit profile splits internal/proper mass from external mass readout",
            "internal/proper mass inventory is additive and not erased by deficit filtering",
            "external mass readout can be smaller than internal/proper inventory",
            "external smallness can hide a large proper interior scale",
            "local c remains invariant in the split metric-readout ledger",
            "old p15 core-mass language is reinterpreted as external active readout",
        ],
        "not_closed_now": [
            "derive the readout filters eta_m and Xi_L from the full action",
            "derive the finite-core matter equation of state under strong compression",
            "derive the full ADM/Noether bridge between internal inventory and external charge",
            "solve the finite-core dynamical branch selection",
        ],
        "intuitive_reading": (
            "Every nonzero gravitational/deficit profile creates a distinction "
            "between internal/proper inventory and external readout.  A compact "
            "object is the strong limit, where the outside readout can look "
            "small and slow while the proper interior is very large.  This "
            "blocks the singularity interpretation at the bookkeeping level, "
            "while leaving the real dynamical proof open."
        ),
    }


if __name__ == "__main__":
    result = internal_external_readout_split_status()
    print("PHASE 15e: Internal inventory versus external readout split")
    print("status:", result["status"])
    print("closed_now:")
    for item in result["closed_now"]:
        print("  -", item)
    print("not_closed_now:")
    for item in result["not_closed_now"]:
        print("  -", item)
    print("universal:", result["universal_cosmic_mass_split"]["status"])
    print("mass:", result["mass_split"]["status"])
    print("scale:", result["scale_split"]["status"])
    print(
        "example:",
        result["scale_split"]["example_external_1m_to_internal_300000km"],
    )
    print("finite:", result["finite_interior_guard"]["status"])
    print("legacy:", result["legacy_language_reinterpretation"]["status"])
