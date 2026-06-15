"""
PHASE 15f: Universal proper inventory versus external readout bridge.

This file continues p15e without touching the article.

The aim is not to declare that the full compact-object dynamics are solved.
The aim is to keep the intuition honest in equations:

    1. internal/proper inventory is additive;
    2. external mass/size/clock readout is a filtered channel;
    3. the filter is weak for weak objects and large for compact objects;
    4. ADM/Komar/asymptotic mass is an exterior charge, not automatically the
       same object as the full internal inventory until the action bridge is
       derived;
    5. mass-volume balance and local light-speed invariance impose precise
       scaling relations that can be audited algebraically.
"""

from __future__ import annotations

import sympy as sp

from p05_compact import derive_adm_komar_and_proper_energy_bookkeeping
from p06_inertia import dressed_mass_no_double_counting
from p13_refractive_force import p10_asymptotic_charge_normalization
from p15e_internal_external_readout_split_gate import (
    internal_external_readout_split_status,
)


def derive_two_mass_ledger_identities() -> dict[str, object]:
    """
    Separate the two mass ledgers without double counting.

    The first identity is the inside/outside split:

        M_proper = M_external_readout + M_hidden_gap.

    The second identity is the outside-sector split:

        M_external_readout = M_active_readout + M_external_dressing.

    These are not one sum with the same term counted twice.  They are two
    different decompositions of two different readings.
    """
    eta_m, zeta, M_proper = sp.symbols(
        "eta_m zeta M_proper",
        positive=True,
        real=True,
    )

    M_external_readout = sp.simplify(eta_m * M_proper)
    M_hidden_gap = sp.simplify(M_proper - M_external_readout)
    M_active_readout = sp.simplify(zeta * M_external_readout)
    M_external_dressing = sp.simplify(M_external_readout - M_active_readout)

    proper_identity = sp.simplify(
        M_external_readout + M_hidden_gap - M_proper
    )
    external_identity = sp.simplify(
        M_active_readout + M_external_dressing - M_external_readout
    )

    return {
        "status": "PASS_TWO_MASS_LEDGERS_SEPARATED_WITHOUT_DOUBLE_COUNTING",
        "conditions": {
            "mass_filter": "0 < eta_m <= 1",
            "active_fraction": "0 <= zeta <= 1",
        },
        "proper_inventory": sp.Eq(sp.Symbol("M_proper"), M_proper),
        "external_mass_readout": sp.Eq(
            sp.Symbol("M_external_readout"),
            M_external_readout,
        ),
        "hidden_readout_gap": sp.Eq(sp.Symbol("M_hidden_gap"), M_hidden_gap),
        "active_readout": sp.Eq(
            sp.Symbol("M_active_readout"),
            M_active_readout,
        ),
        "external_dressing": sp.Eq(
            sp.Symbol("M_external_dressing"),
            M_external_dressing,
        ),
        "proper_ledger_identity_residual": proper_identity,
        "external_ledger_identity_residual": external_identity,
        "reading": (
            "Internal/proper mass is not destroyed.  External readout may be "
            "smaller, and the external readout itself may be partitioned into "
            "active readout plus exterior dressing without adding the same "
            "energy twice."
        ),
    }


def derive_mass_volume_balance_condition() -> dict[str, object]:
    """
    Put the user's volume intuition into exact algebra.

    If each measured length direction is filtered by eta_L, then volume is
    filtered by eta_L^3.  If mass and volume filtering are balanced, then

        eta_m = eta_V = eta_L^3.

    In q variables this is q_m = 3*q_L for isotropic length filtering.
    """
    eta_L, eta_m, L_proper, V_proper, M_proper = sp.symbols(
        "eta_L eta_m L_proper V_proper M_proper",
        positive=True,
        real=True,
    )
    q_L, q_m = sp.symbols("q_L q_m", nonnegative=True, real=True)

    L_readout = sp.simplify(eta_L * L_proper)
    V_readout = sp.simplify(eta_L**3 * V_proper)
    M_readout = sp.simplify(eta_m * M_proper)
    rho_proper = sp.simplify(M_proper / V_proper)
    rho_readout = sp.simplify(M_readout / V_readout)
    density_ratio = sp.simplify(rho_readout / rho_proper)

    balanced_density_ratio = sp.simplify(density_ratio.subs(eta_m, eta_L**3))
    q_balance_residual = sp.simplify(
        sp.exp(-q_m).subs(q_m, 3 * q_L) - sp.exp(-q_L) ** 3
    )

    length_halving_volume_factor = sp.simplify((sp.Rational(1, 2)) ** 3)
    length_halving_mass_factor_if_balanced = length_halving_volume_factor

    return {
        "status": "PASS_MASS_VOLUME_BALANCE_CONDITION_DERIVED",
        "length_readout": sp.Eq(sp.Symbol("L_readout"), L_readout),
        "volume_readout": sp.Eq(sp.Symbol("V_readout"), V_readout),
        "mass_readout": sp.Eq(sp.Symbol("M_readout"), M_readout),
        "density_readout_ratio": sp.Eq(
            sp.Symbol("rho_readout/rho_proper"),
            density_ratio,
        ),
        "balanced_condition": sp.Eq(sp.Symbol("eta_m"), eta_L**3),
        "balanced_density_ratio": sp.Eq(
            sp.Symbol("rho_readout/rho_proper"),
            balanced_density_ratio,
        ),
        "q_balance": sp.Eq(sp.Symbol("q_m"), 3 * q_L),
        "q_balance_residual": q_balance_residual,
        "if_length_readout_halves": {
            "volume_readout_factor": length_halving_volume_factor,
            "mass_readout_factor_if_balanced": (
                length_halving_mass_factor_if_balanced
            ),
        },
        "reading": (
            "If the outside readout sees each length direction reduced by two, "
            "the readout volume is reduced by eight.  Mass-volume balance then "
            "requires the external mass readout to be reduced by the same "
            "factor eight; this preserves the readout density ratio instead of "
            "silently changing it."
        ),
    }


def derive_clock_length_light_consistency_gate() -> dict[str, object]:
    """
    Check that length filtering and clock slowing do not change local c.

    Let alpha_t=d_tau/dt be the lapse/readout clock factor and eta_L the length
    readout factor.  A local light ray satisfies dL_proper=c*d_tau.  The outside
    coordinate/readout speed is then eta_L*alpha_t*c.  Reconstructing with the
    local rods and local clock returns c exactly.
    """
    eta_L, alpha_t, c, dt = sp.symbols(
        "eta_L alpha_t c dt",
        positive=True,
        real=True,
    )

    d_tau = sp.simplify(alpha_t * dt)
    dL_proper = sp.simplify(c * d_tau)
    dL_readout = sp.simplify(eta_L * dL_proper)
    c_coordinate_readout = sp.simplify(dL_readout / dt)
    c_reconstructed_local = sp.simplify((dL_readout / eta_L) / d_tau)

    equal_filter_coordinate_speed = sp.simplify(
        c_coordinate_readout.subs(alpha_t, eta_L)
    )
    collision_rate_readout = sp.simplify(alpha_t * sp.Symbol("Gamma_0"))

    return {
        "status": "PASS_CLOCK_LENGTH_LIGHT_SPEED_LEDGER_CONSISTENT",
        "clock_factor": sp.Eq(sp.Symbol("d_tau/dt"), alpha_t),
        "length_factor": sp.Eq(sp.Symbol("dL_readout/dL_proper"), eta_L),
        "proper_light_path": sp.Eq(sp.Symbol("dL_proper"), dL_proper),
        "readout_light_path": sp.Eq(sp.Symbol("dL_readout"), dL_readout),
        "coordinate_light_speed": sp.Eq(
            sp.Symbol("c_coordinate_readout"),
            c_coordinate_readout,
        ),
        "local_c_reconstruction": sp.Eq(
            sp.Symbol("c_local"),
            c_reconstructed_local,
        ),
        "local_c_identity": sp.simplify(c_reconstructed_local - c) == 0,
        "equal_length_clock_filter_coordinate_speed": sp.Eq(
            sp.Symbol("c_coordinate_readout"),
            equal_filter_coordinate_speed,
        ),
        "collision_rate_readout_ansatz": sp.Eq(
            sp.Symbol("Gamma_readout"),
            collision_rate_readout,
        ),
        "open_microphysics": (
            "alpha_t and eta_L must be derived from the medium dynamics; this "
            "gate only checks that any proposed factors preserve local c when "
            "the same local rods and clocks are used."
        ),
    }


def derive_weak_to_strong_readout_filter_gate() -> dict[str, object]:
    """
    Audit the weak and strong limits of a monotone exponential readout filter.

    The exponential parameterization is used as a clean ledger ansatz.  The
    action must still derive which physical deficit variable supplies q_m.
    """
    q_m, M_proper = sp.symbols("q_m M_proper", nonnegative=True, real=True)

    eta_m = sp.exp(-q_m)
    M_readout = sp.simplify(eta_m * M_proper)
    hidden_gap = sp.simplify(M_proper - M_readout)
    hidden_gap_fraction = sp.simplify(hidden_gap / M_proper)
    weak_series = sp.series(hidden_gap_fraction, q_m, 0, 5).removeO()

    strong_readout_limit = sp.limit(eta_m, q_m, sp.oo)
    strong_gap_limit = sp.limit(hidden_gap_fraction, q_m, sp.oo)

    sample_q_values = [
        sp.Integer(0),
        sp.Rational(1, 1000),
        sp.log(2),
        sp.Integer(1),
        sp.log(300_000_000),
    ]
    samples = [
        {
            "q_m": q_value,
            "M_readout_over_M_proper": sp.simplify(eta_m.subs(q_m, q_value)),
            "hidden_gap_over_M_proper": sp.simplify(
                hidden_gap_fraction.subs(q_m, q_value)
            ),
        }
        for q_value in sample_q_values
    ]

    return {
        "status": "PASS_WEAK_TO_STRONG_READOUT_FILTER_LIMITS",
        "filter_ansatz": sp.Eq(sp.Symbol("eta_m(q_m)"), eta_m),
        "external_mass_readout": sp.Eq(
            sp.Symbol("M_readout"),
            M_readout,
        ),
        "hidden_gap": sp.Eq(sp.Symbol("M_hidden_gap"), hidden_gap),
        "hidden_gap_fraction": sp.Eq(
            sp.Symbol("M_hidden_gap/M_proper"),
            hidden_gap_fraction,
        ),
        "weak_gap_series": sp.Eq(
            sp.Symbol("M_hidden_gap/M_proper"),
            weak_series,
        ),
        "zero_deficit_equality": sp.Eq(
            M_readout.subs(q_m, 0),
            M_proper,
        ),
        "strong_readout_limit": strong_readout_limit,
        "strong_gap_limit": strong_gap_limit,
        "samples": samples,
        "reading": (
            "The same algebra covers weak and compact objects.  At q_m=0 the "
            "two readings coincide.  At small q_m they differ only by the weak "
            "series.  At large q_m the outside readout can become tiny while "
            "the proper inventory remains the independent internal ledger."
        ),
    }


def derive_external_charge_interface_gate() -> dict[str, object]:
    """
    Connect p15e/p15f language to existing ADM/Komar and asymptotic-charge work.
    """
    p15e = internal_external_readout_split_status()
    adm = derive_adm_komar_and_proper_energy_bookkeeping()
    charge = p10_asymptotic_charge_normalization()
    no_double = dressed_mass_no_double_counting()

    checks = (
        p15e["status"]
        == "PASS_INTERNAL_EXTERNAL_SPLIT_REPAIRS_VOLUME_DEFICIT_LANGUAGE__DYNAMICS_OPEN",
        adm["ADM_Komar_identity"],
        adm["coordinate_source_to_ADM_ratio"] == sp.Rational(1, 4),
        charge["status"] == "PASS_P10_ASYMPTOTIC_CHARGE_NORMALIZATION",
        charge["charge_identity"],
        charge["newton_identity"],
        "no_double_counting_rule" in no_double,
    )

    return {
        "status": (
            "PASS_EXTERNAL_CHARGE_INTERFACE_READY__PROPER_INVENTORY_BRIDGE_OPEN"
            if all(checks)
            else "CHECK_EXTERNAL_CHARGE_INTERFACE"
        ),
        "p15e_status": p15e["status"],
        "ADM_mass_physical": adm["ADM_mass_physical"],
        "ADM_Komar_identity": adm["ADM_Komar_identity"],
        "coordinate_source_to_ADM_ratio": adm["coordinate_source_to_ADM_ratio"],
        "p10_charge_status": charge["status"],
        "p10_asymptotic_charge": charge["asymptotic_charge"],
        "p10_mu_from_charge": charge["mu_from_charge"],
        "p10_charge_identity": charge["charge_identity"],
        "p10_newton_identity": charge["newton_identity"],
        "no_double_counting_rule": no_double["no_double_counting_rule"],
        "closed_now": (
            "external mass is fixed as an ADM/Komar/asymptotic surface charge",
            "the weak exterior 1/r charge normalization is closed",
            "core+dressing is counted once in the far-zone charge ledger",
        ),
        "still_open": (
            "derive the full finite-core proper inventory to ADM/Noether bridge",
            "derive eta_m, eta_L, and alpha_t from the full medium dynamics",
            "derive the strong-compression matter equation of state",
        ),
    }


def universal_proper_readout_bridge_status() -> dict[str, object]:
    two_mass = derive_two_mass_ledger_identities()
    mass_volume = derive_mass_volume_balance_condition()
    clock_light = derive_clock_length_light_consistency_gate()
    filter_limits = derive_weak_to_strong_readout_filter_gate()
    charge_interface = derive_external_charge_interface_gate()

    passed = (
        two_mass["status"]
        == "PASS_TWO_MASS_LEDGERS_SEPARATED_WITHOUT_DOUBLE_COUNTING"
        and two_mass["proper_ledger_identity_residual"] == 0
        and two_mass["external_ledger_identity_residual"] == 0
        and mass_volume["status"] == "PASS_MASS_VOLUME_BALANCE_CONDITION_DERIVED"
        and mass_volume["q_balance_residual"] == 0
        and clock_light["status"]
        == "PASS_CLOCK_LENGTH_LIGHT_SPEED_LEDGER_CONSISTENT"
        and clock_light["local_c_identity"]
        and filter_limits["status"] == "PASS_WEAK_TO_STRONG_READOUT_FILTER_LIMITS"
        and filter_limits["strong_readout_limit"] == 0
        and filter_limits["strong_gap_limit"] == 1
        and charge_interface["status"]
        == "PASS_EXTERNAL_CHARGE_INTERFACE_READY__PROPER_INVENTORY_BRIDGE_OPEN"
    )

    return {
        "status": (
            "PASS_UNIVERSAL_PROPER_READOUT_BRIDGE_LEDGER__ACTION_DYNAMICS_OPEN"
            if passed
            else "CHECK_UNIVERSAL_PROPER_READOUT_BRIDGE"
        ),
        "two_mass_ledger": two_mass,
        "mass_volume_balance": mass_volume,
        "clock_length_light": clock_light,
        "weak_to_strong_filter": filter_limits,
        "external_charge_interface": charge_interface,
        "closed_now": [
            "internal/proper inventory and external readout are separate ledgers",
            "external readout gaps are not proper-mass destruction",
            "mass-volume balance requires eta_m=eta_L^3 for isotropic length filtering",
            "in q variables the balanced isotropic relation is q_m=3*q_L",
            "clock slowing and length filtering can preserve local c exactly",
            "ADM/Komar/asymptotic mass is the exterior charge channel",
        ],
        "not_closed_now": [
            "derive eta_m, eta_L, and alpha_t from the full RefG action",
            "derive the finite-core proper inventory to ADM/Noether map",
            "derive the strong-compression matter equation of state",
            "solve the finite-core dynamical selection of the compact branch",
        ],
        "plain_reading": (
            "The Python ledger now supports the intuition that every nonzero "
            "deficit profile splits inside/proper inventory from outside "
            "readout.  In the balanced isotropic case, a twofold length readout "
            "reduction means an eightfold volume and external mass readout "
            "reduction.  Local c is not changed; outside coordinate/readout "
            "speed changes because both clock and length readings are filtered."
        ),
    }


if __name__ == "__main__":
    result = universal_proper_readout_bridge_status()
    print("PHASE 15f: Universal proper/readout bridge")
    print("status:", result["status"])
    print("closed_now:")
    for item in result["closed_now"]:
        print("  -", item)
    print("not_closed_now:")
    for item in result["not_closed_now"]:
        print("  -", item)
    print("two_mass:", result["two_mass_ledger"]["status"])
    print("mass_volume:", result["mass_volume_balance"]["status"])
    print("q_balance:", result["mass_volume_balance"]["q_balance"])
    print(
        "length_half_mass_factor:",
        result["mass_volume_balance"]["if_length_readout_halves"][
            "mass_readout_factor_if_balanced"
        ],
    )
    print("clock_light:", result["clock_length_light"]["status"])
    print(
        "local_c_identity:",
        result["clock_length_light"]["local_c_identity"],
    )
    print("filter_limits:", result["weak_to_strong_filter"]["status"])
    print("charge_interface:", result["external_charge_interface"]["status"])
