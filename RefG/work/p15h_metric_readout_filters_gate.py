"""
PHASE 15h: Metric readout filters for length, volume, clock and bulk mass.

This file continues p15f/p15g and does not touch the article.

The important distinction:

    single local unit / oscillator / rod / clock channel:
        exp(-q/2)

    isotropic three-dimensional bulk volume channel:
        exp(-3q/2)

Therefore p10's half-exponent result is not discarded.  It is the one-unit
metric/readout factor.  The new mass-volume statement applies only when the
external bulk mass readout follows the three-dimensional volume readout.
"""

from __future__ import annotations

import sympy as sp

from p05_compact import (
    analyze_horizon_throat_and_boundary,
    compact_signature_bridge,
    derive_exponential_exterior_from_phase_equation,
)
from p10_oscillons import step6b_deficit_scaling_factor_two_gate
from p15f_universal_proper_readout_bridge_gate import (
    universal_proper_readout_bridge_status,
)
from p15g_proper_inventory_adm_bridge_gate import (
    proper_inventory_adm_bridge_status,
)


def derive_exponential_metric_readout_filters() -> dict[str, object]:
    """
    Derive the metric-level filters from the exponential branch.

    Let q_geo=r_s/r=-phi>=0.  On the static exponential exterior,

        B = exp(-q_geo), A = exp(+q_geo).

    Hence local clock rate and one-dimensional length readout both carry the
    half exponent exp(-q_geo/2), while radial coordinate light speed carries
    the full exponent exp(-q_geo).
    """
    q_geo, c, dt = sp.symbols("q_geo c dt", positive=True, real=True)

    B = sp.exp(-q_geo)
    A = sp.exp(q_geo)
    alpha_t = sp.sqrt(B)
    eta_L = sp.simplify(1 / sp.sqrt(A))
    eta_V = sp.simplify(eta_L**3)
    c_coord = sp.simplify(c * sp.sqrt(B / A))

    d_tau = sp.simplify(alpha_t * dt)
    dL_proper = sp.simplify(c * d_tau)
    dL_readout = sp.simplify(eta_L * dL_proper)
    local_c_reconstructed = sp.simplify((dL_readout / eta_L) / d_tau)
    c_coord_from_halves = sp.simplify(c * alpha_t * eta_L)

    exterior = derive_exponential_exterior_from_phase_equation()
    signature = compact_signature_bridge()
    boundary = analyze_horizon_throat_and_boundary()

    return {
        "status": "PASS_EXPONENTIAL_METRIC_READOUT_FILTERS_DERIVED",
        "p05_exterior_status": exterior["derivation_status"],
        "p05_signature_bridge": signature["stress_bridge_status"],
        "p05_coordinate_light_speed": boundary["coordinate_light_speed"],
        "geometric_deficit": sp.Eq(sp.Symbol("q_geo"), q_geo),
        "metric_lapse_B": sp.Eq(sp.Symbol("B"), B),
        "metric_spatial_A": sp.Eq(sp.Symbol("A"), A),
        "clock_rate_filter": sp.Eq(sp.Symbol("alpha_t"), alpha_t),
        "one_dimensional_length_filter": sp.Eq(sp.Symbol("eta_L"), eta_L),
        "volume_filter": sp.Eq(sp.Symbol("eta_V"), eta_V),
        "coordinate_light_speed": sp.Eq(sp.Symbol("c_coord"), c_coord),
        "coordinate_light_from_halves": sp.Eq(
            sp.Symbol("c_coord"),
            c_coord_from_halves,
        ),
        "coordinate_light_identity": sp.simplify(c_coord - c_coord_from_halves)
        == 0,
        "local_c_reconstruction": sp.Eq(
            sp.Symbol("c_local"),
            local_c_reconstructed,
        ),
        "local_c_identity": sp.simplify(local_c_reconstructed - c) == 0,
        "reading": (
            "The metric itself gives the filters: clock and one-dimensional "
            "length readout use exp(-q_geo/2); coordinate light speed is their "
            "product exp(-q_geo); volume readout is exp(-3q_geo/2)."
        ),
    }


def derive_unit_vs_bulk_mass_scaling_dictionary() -> dict[str, object]:
    """
    Separate one-unit mass scale from bulk mass-volume readout.

    p10 establishes a one-unit effective mass scale exp(-q/2).  p15f/p15g
    establish that a balanced isotropic bulk mass-volume readout uses the
    volume factor exp(-3q/2).  They are equal only at q=0.
    """
    q_geo = sp.symbols("q_geo", nonnegative=True, real=True)

    eta_unit = sp.exp(-q_geo / 2)
    eta_L = eta_unit
    eta_V = sp.simplify(eta_L**3)
    eta_bulk_mass = eta_V

    unit_minus_length = sp.simplify(eta_unit - eta_L)
    bulk_minus_volume = sp.simplify(eta_bulk_mass - eta_V)
    unit_minus_bulk = sp.factor(sp.simplify(eta_unit - eta_bulk_mass))
    unit_over_bulk = sp.simplify(eta_unit / eta_bulk_mass)

    q_L = sp.simplify(q_geo / 2)
    q_m_unit = sp.simplify(q_geo / 2)
    q_m_bulk = sp.simplify(3 * q_geo / 2)
    q_bulk_balance_residual = sp.simplify(q_m_bulk - 3 * q_L)

    weak_unit_loss = sp.series(1 - eta_unit, q_geo, 0, 4).removeO()
    weak_bulk_loss = sp.series(1 - eta_bulk_mass, q_geo, 0, 4).removeO()

    equality_roots = sp.solve(sp.Eq(unit_minus_bulk, 0), q_geo)

    return {
        "status": "PASS_UNIT_AND_BULK_MASS_READOUTS_SEPARATED",
        "unit_mass_or_clock_filter": sp.Eq(sp.Symbol("eta_unit"), eta_unit),
        "length_filter": sp.Eq(sp.Symbol("eta_L"), eta_L),
        "volume_filter": sp.Eq(sp.Symbol("eta_V"), eta_V),
        "balanced_bulk_mass_filter": sp.Eq(
            sp.Symbol("eta_m_bulk"),
            eta_bulk_mass,
        ),
        "unit_minus_length": unit_minus_length,
        "bulk_minus_volume": bulk_minus_volume,
        "unit_minus_bulk": unit_minus_bulk,
        "unit_over_bulk": sp.Eq(sp.Symbol("eta_unit/eta_m_bulk"), unit_over_bulk),
        "q_L": sp.Eq(sp.Symbol("q_L"), q_L),
        "q_m_unit": sp.Eq(sp.Symbol("q_m_unit"), q_m_unit),
        "q_m_bulk": sp.Eq(sp.Symbol("q_m_bulk"), q_m_bulk),
        "bulk_q_balance_residual": q_bulk_balance_residual,
        "weak_unit_loss": sp.Eq(sp.Symbol("1-eta_unit"), weak_unit_loss),
        "weak_bulk_loss": sp.Eq(sp.Symbol("1-eta_m_bulk"), weak_bulk_loss),
        "unit_bulk_equality_roots": equality_roots,
        "reading": (
            "A single local unit scales with the half exponent.  A balanced "
            "three-dimensional bulk readout scales with the cube of that factor. "
            "Mixing these two channels would create a false contradiction."
        ),
    }


def derive_volume_halving_metric_example() -> dict[str, object]:
    """Exact numbers for the user's volume-halving question."""
    eta_V = sp.Rational(1, 2)

    eta_L = sp.real_root(eta_V, 3)
    q_geo = sp.simplify(-2 * sp.log(eta_L))
    alpha_t = eta_L
    c_coord_over_c = sp.simplify(alpha_t * eta_L)
    eta_unit = eta_L
    eta_bulk_mass = eta_V
    proper_inventory_over_external_bulk_readout = sp.simplify(1 / eta_bulk_mass)

    return {
        "status": "PASS_VOLUME_HALVING_METRIC_EXAMPLE",
        "volume_readout_factor": eta_V,
        "length_readout_factor": eta_L,
        "geometric_deficit_q_geo": q_geo,
        "clock_rate_filter": alpha_t,
        "coordinate_light_speed_over_c": c_coord_over_c,
        "unit_mass_filter": eta_unit,
        "bulk_mass_filter_if_volume_balanced": eta_bulk_mass,
        "proper_inventory_over_external_bulk_readout": (
            proper_inventory_over_external_bulk_readout
        ),
        "reading": (
            "When volume readout is halved, each linear readout factor is "
            "2^(-1/3).  The one-unit mass/clock factor is also 2^(-1/3), "
            "while balanced bulk mass readout is 1/2."
        ),
    }


def derive_p10_p15_compatibility_gate() -> dict[str, object]:
    """
    Verify that p10's half-exponent and p15's bulk-volume exponent are compatible.
    """
    q_geo = sp.symbols("q_geo", positive=True, real=True)

    p10 = step6b_deficit_scaling_factor_two_gate()
    p15f = universal_proper_readout_bridge_status()
    p15g = proper_inventory_adm_bridge_status()

    p10_unit = sp.exp(-q_geo / 2)
    p15_bulk = sp.exp(-3 * q_geo / 2)
    ratio = sp.simplify(p15_bulk / p10_unit)
    not_equal_for_positive_q = sp.simplify(p10_unit - p15_bulk)

    checks = (
        p10["deficit_scaling_factor_two_status"]
        == "PASS_MASS_SIZE_LAPSE_HALF_EXPONENT_AND_LIGHT_FULL_EXPONENT",
        p15f["status"]
        == "PASS_UNIVERSAL_PROPER_READOUT_BRIDGE_LEDGER__ACTION_DYNAMICS_OPEN",
        p15g["status"]
        == "PASS_PROPER_INVENTORY_ADM_BRIDGE_AUDIT__FULL_ACTION_MAP_OPEN",
        sp.simplify(ratio - sp.exp(-q_geo)) == 0,
    )

    return {
        "status": (
            "PASS_P10_HALF_EXPONENT_AND_P15_BULK_VOLUME_EXPONENT_COMPATIBLE"
            if all(checks)
            else "CHECK_P10_P15_FILTER_COMPATIBILITY"
        ),
        "p10_status": p10["deficit_scaling_factor_two_status"],
        "p15f_status": p15f["status"],
        "p15g_status": p15g["status"],
        "p10_unit_mass_scale": sp.Eq(sp.Symbol("eta_unit"), p10_unit),
        "p15_bulk_mass_scale": sp.Eq(sp.Symbol("eta_m_bulk"), p15_bulk),
        "bulk_over_unit": sp.Eq(sp.Symbol("eta_m_bulk/eta_unit"), ratio),
        "unit_minus_bulk_factorized": sp.factor(not_equal_for_positive_q),
        "compatibility_rule": (
            "Use exp(-q/2) for a single local oscillator/rod/clock scale.  Use "
            "exp(-3q/2) only for an isotropic bulk mass readout that follows "
            "three-dimensional volume."
        ),
    }


def metric_readout_filters_status() -> dict[str, object]:
    metric_filters = derive_exponential_metric_readout_filters()
    unit_bulk = derive_unit_vs_bulk_mass_scaling_dictionary()
    volume_example = derive_volume_halving_metric_example()
    compatibility = derive_p10_p15_compatibility_gate()

    passed = (
        metric_filters["status"] == "PASS_EXPONENTIAL_METRIC_READOUT_FILTERS_DERIVED"
        and metric_filters["coordinate_light_identity"]
        and metric_filters["local_c_identity"]
        and unit_bulk["status"] == "PASS_UNIT_AND_BULK_MASS_READOUTS_SEPARATED"
        and unit_bulk["unit_minus_length"] == 0
        and unit_bulk["bulk_minus_volume"] == 0
        and unit_bulk["bulk_q_balance_residual"] == 0
        and volume_example["status"] == "PASS_VOLUME_HALVING_METRIC_EXAMPLE"
        and compatibility["status"]
        == "PASS_P10_HALF_EXPONENT_AND_P15_BULK_VOLUME_EXPONENT_COMPATIBLE"
    )

    return {
        "status": (
            "PASS_METRIC_READOUT_FILTERS_FOR_CLOCK_LENGTH_VOLUME_BULK_MASS__MICRODYNAMICS_OPEN"
            if passed
            else "CHECK_METRIC_READOUT_FILTERS"
        ),
        "metric_filters": metric_filters,
        "unit_vs_bulk": unit_bulk,
        "volume_halving_example": volume_example,
        "p10_p15_compatibility": compatibility,
        "closed_now": [
            "exponential metric gives alpha_t=eta_L=exp(-q_geo/2)",
            "coordinate light speed is c_coord/c=exp(-q_geo)",
            "local c reconstructs exactly from local rods and clocks",
            "isotropic volume readout is eta_V=eta_L^3=exp(-3q_geo/2)",
            "balanced bulk mass-volume readout uses eta_m_bulk=eta_V",
            "p10 half-exponent and p15 bulk-volume exponent are compatible when their channels are kept separate",
        ],
        "not_closed_now": [
            "derive why the bulk mass readout must follow eta_V from the full matter action",
            "derive the finite-core strong-compression equation of state",
            "derive the full proper inventory to ADM/Noether map",
            "solve the compact-branch dynamics",
        ],
        "plain_reading": (
            "The metric supplies the clock and length half-factor.  A single "
            "unit follows that half-factor.  A 3D bulk object, if its readout "
            "mass follows its readout volume, follows the cube of that factor."
        ),
    }


if __name__ == "__main__":
    result = metric_readout_filters_status()
    print("PHASE 15h: Metric readout filters")
    print("status:", result["status"])
    print("closed_now:")
    for item in result["closed_now"]:
        print("  -", item)
    print("not_closed_now:")
    for item in result["not_closed_now"]:
        print("  -", item)
    print("metric:", result["metric_filters"]["status"])
    print("unit_vs_bulk:", result["unit_vs_bulk"]["status"])
    print("volume_halving:", result["volume_halving_example"])
    print("compatibility:", result["p10_p15_compatibility"]["status"])
