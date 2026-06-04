"""
PHASE 15b: Dressing mass conservation gate.

This file follows p15 and p15a without touching the article.

Question:
    If the external active core readout falls with active volume, while the
    internal/proper inventory is a separate quantity, can the compact exterior
    still carry a conserved far-zone mass?

Answer at the current proof level:
    Yes as a surface-charge/Noether ledger, but not yet as a direct full-action
    compact-body integral.

The distinction matters.  The filtered active readout by itself becomes less
compact.  A compact threshold appears only if the remaining external charge is
kept in the exterior medium/dressing and counted once as the same far-zone
ADM/Noether mass.  Existing p05 and p06 files support this bookkeeping:

    p05: the static exterior ADM/Komar mass is an asymptotic surface charge;
    p06: core+dressing is one total Noether energy, not two masses.

What is still open is stronger:
    derive the compact-object dressing energy directly from the RefG action
    and show that the full proper/Noether integral equals the ADM/Komar charge.
"""

from __future__ import annotations

import sympy as sp

from p05_compact import (
    derive_adm_komar_and_proper_energy_bookkeeping,
    derive_c2_core_proper_energy_finiteness,
    derive_c2_core_refg_medium_source_decomposition,
)
from p06_inertia import (
    dressed_mass_no_double_counting,
    inertia_noether_short_path_certificate,
)
from p15a_volume_deficit_compact_threshold_gate import (
    volume_deficit_compact_threshold_status,
)


def derive_depleted_core_plus_dressing_ledger() -> dict[str, object]:
    """External active-readout plus dressing ledger for the volume-deficit picture."""
    q_v, M0, R0, G, c = sp.symbols(
        "q_v M0 R0 G c",
        positive=True,
        real=True,
    )

    v = sp.exp(-q_v)
    active_readout_mass = sp.simplify(M0 * v)
    dressing_mass = sp.simplify(M0 * (1 - v))
    total_mass = sp.simplify(active_readout_mass + dressing_mass)
    radius = sp.simplify(R0 * v ** sp.Rational(1, 3))

    active_readout_compactness = sp.simplify(
        2 * G * active_readout_mass / (c**2 * radius)
    )
    total_compactness = sp.simplify(2 * G * total_mass / (c**2 * radius))
    initial_compactness = sp.simplify(2 * G * M0 / (c**2 * R0))

    return {
        "status": "PASS_FILTERED_ACTIVE_READOUT_PLUS_DRESSING_LEDGER_IDENTITIES",
        "active_volume_factor": sp.Eq(sp.Symbol("v"), v),
        "external_active_mass_readout": sp.Eq(
            sp.Symbol("M_active_readout"),
            active_readout_mass,
        ),
        "core_mass_legacy_name": sp.Eq(
            sp.Symbol("M_core_readout"),
            active_readout_mass,
        ),
        "dressing_mass": sp.Eq(sp.Symbol("M_dress"), dressing_mass),
        "total_mass": sp.Eq(sp.Symbol("M_total"), total_mass),
        "proper_inventory_guard": (
            "M_active_readout is not the internal/proper inventory.  It is the "
            "part of the external charge ledger carried directly by the active "
            "core readout."
        ),
        "mass_conservation_residual": sp.simplify(total_mass - M0),
        "radius": sp.Eq(sp.Symbol("R"), radius),
        "initial_compactness": sp.Eq(sp.Symbol("Q0"), initial_compactness),
        "active_readout_compactness": sp.Eq(
            sp.Symbol("Q_active_readout"),
            active_readout_compactness,
        ),
        "total_compactness": sp.Eq(sp.Symbol("Q_total"), total_compactness),
        "core_compactness_over_initial": sp.simplify(
            active_readout_compactness / initial_compactness
        ),
        "total_compactness_over_initial": sp.simplify(
            total_compactness / initial_compactness
        ),
        "dressing_nonnegative_condition": "q_v>=0 gives M_dress=M0(1-exp(-q_v))>=0",
        "reading": (
            "If the external active readout follows active volume, that readout "
            "alone loses compactness.  A compact threshold requires the far-zone "
            "source to be the conserved active-readout+dressing total mass."
        ),
    }


def derive_adm_source_measure_separation_gate() -> dict[str, object]:
    """
    Check that p05 treats ADM mass and volume-source integrals separately.

    This prevents a common false step: identifying the Bernoulli coordinate
    source integral with the total far-zone mass.  p05 shows the exterior mass
    is an ADM/Komar surface charge, while proper source bookkeeping belongs to
    the finite-core completion.
    """
    adm = derive_adm_komar_and_proper_energy_bookkeeping()
    ratio = sp.simplify(adm["coordinate_source_to_ADM_ratio"])

    return {
        "status": (
            "PASS_ADM_SURFACE_CHARGE_SEPARATED_FROM_RAW_VOLUME_SOURCE"
            if adm["ADM_Komar_identity"] and ratio == sp.Rational(1, 4)
            else "CHECK_ADM_SOURCE_MEASURE_SEPARATION"
        ),
        "p05_energy_status": adm["energy_status"],
        "ADM_mass_physical": adm["ADM_mass_physical"],
        "ADM_Komar_identity": adm["ADM_Komar_identity"],
        "coordinate_Bernoulli_source_total": adm[
            "coordinate_Bernoulli_source_total"
        ],
        "coordinate_source_to_ADM_ratio": ratio,
        "coordinate_source_is_not_total_mass": ratio != 1,
        "proper_exterior_source_outside_core": adm[
            "proper_Bernoulli_source_outside_core"
        ],
        "proper_source_zero_core_limit": adm[
            "lim_rc_to_0_proper_source_outside_core"
        ],
        "reading": (
            "The exterior 1/r mass is the surface charge.  The Bernoulli "
            "volume-source integral is a different measure and cannot by "
            "itself be used as the total compact-body mass."
        ),
    }


def derive_c2_core_dressing_integral_open_gate() -> dict[str, object]:
    """Finite C2 source support is closed; equality to ADM mass is still open."""
    proper = derive_c2_core_proper_energy_finiteness()
    medium = derive_c2_core_refg_medium_source_decomposition()

    finite_core = (
        proper["proper_energy_status"]
        == "C2_CORE_EFFECTIVE_PROPER_SOURCE_FINITE_FOR_FINITE_R_C"
    )
    medium_basis = (
        medium["realization_status"]
        == "PASS_C2_CORE_SOURCE_DECOMPOSED_IN_REFG_PROJECTED_PHASE_PLUS_FINITE_MEDIUM_STRESS_BASIS"
        and medium["boundary_residuals_zero"]
    )

    return {
        "status": (
            "PASS_C2_CORE_SOURCE_FINITE_AND_MEDIUM_DECOMPOSED__ADM_EQUALITY_OPEN"
            if finite_core and medium_basis
            else "CHECK_C2_CORE_DRESSING_INTEGRAL_GATE"
        ),
        "proper_energy_status": proper["proper_energy_status"],
        "medium_realization_status": medium["realization_status"],
        "boundary_residuals_zero": medium["boundary_residuals_zero"],
        "total_effective_proper_source_charge": proper[
            "total_effective_proper_source_charge"
        ],
        "open_equality_needed": sp.Eq(
            sp.Symbol("Q_total_proper_or_Noether"),
            sp.Symbol("M_ADM_or_E0_over_c2"),
        ),
        "reading": (
            "The finite core can carry the required tensor source in the RefG "
            "medium basis.  What is not yet derived is the full compact-body "
            "Noether/proper integral equaling the ADM/Komar surface charge."
        ),
    }


def derive_noether_dressing_bridge_gate() -> dict[str, object]:
    """Use p06 only at its stated leading localized-body theorem level."""
    noether = inertia_noether_short_path_certificate()
    no_double = dressed_mass_no_double_counting()

    return {
        "status": (
            "PASS_LEADING_NOETHER_DRESSING_BRIDGE__COMPACT_BODY_EXPORT_OPEN"
            if noether["status"] == "PASS_INERTIA_NOETHER_SHORT_PATH"
            and noether["same_mass_identity"]
            else "CHECK_LEADING_NOETHER_DRESSING_BRIDGE"
        ),
        "p06_status": noether["status"],
        "same_mass_identity": noether["same_mass_identity"],
        "total_rest_energy": no_double["total_rest_energy"],
        "inertial_mass": no_double["inertial_mass"],
        "gravitational_mass": no_double["gravitational_mass"],
        "no_double_counting_rule": no_double["no_double_counting_rule"],
        "far_zone_charge_rule": no_double["far_zone_charge"],
        "reading": (
            "For a localized dressed object, p06 already uses one total energy "
            "E0 for inertia and far-zone gravitational charge.  Exporting that "
            "to nonlinear compact bodies remains the explicit ADM/Noether task."
        ),
    }


def dressing_mass_conservation_status() -> dict[str, object]:
    p15a = volume_deficit_compact_threshold_status()
    ledger = derive_depleted_core_plus_dressing_ledger()
    adm = derive_adm_source_measure_separation_gate()
    c2 = derive_c2_core_dressing_integral_open_gate()
    noether = derive_noether_dressing_bridge_gate()

    passed = (
        p15a["status"]
        == "PASS_VOLUME_DEFICIT_CAN_SELECT_COMPACT_GATE_CONDITIONALLY__DRESSING_DYNAMICS_OPEN"
        and ledger["mass_conservation_residual"] == 0
        and adm["status"]
        == "PASS_ADM_SURFACE_CHARGE_SEPARATED_FROM_RAW_VOLUME_SOURCE"
        and c2["status"]
        == "PASS_C2_CORE_SOURCE_FINITE_AND_MEDIUM_DECOMPOSED__ADM_EQUALITY_OPEN"
        and noether["status"]
        == "PASS_LEADING_NOETHER_DRESSING_BRIDGE__COMPACT_BODY_EXPORT_OPEN"
    )

    return {
        "status": (
            "PASS_DRESSING_MASS_CONSERVATION_LEDGER_COMPATIBLE_WITH_ADM_NOETHER__ACTION_DERIVATION_OPEN"
            if passed
            else "CHECK_DRESSING_MASS_CONSERVATION_GATE"
        ),
        "p15a_status": p15a["status"],
        "ledger": ledger,
        "adm_source_separation": adm,
        "c2_integral_gate": c2,
        "noether_bridge": noether,
        "closed_now": [
            "volume-mass equality is compatible with the p15 metric guardrail",
            "active-readout compactness falls, so it cannot be the compact threshold alone",
            "conserved active-readout+dressing far mass raises total compactness as R shrinks",
            "p05 fixes the exterior mass as ADM/Komar surface charge",
            "p06 supplies the leading one-energy Noether no-double-counting rule",
        ],
        "not_closed_now": [
            "derive M_dress(q_v) from the full compact RefG action",
            "prove the full compact-body proper/Noether integral equals the ADM/Komar charge",
            "derive the finite-core time evolution that selects and reaches the gate",
        ],
        "intuitive_reading": (
            "The external active readout can be filtered without losing the "
            "far-zone mass, but only if the remaining external charge is stored "
            "in the dressing/deficit field and counted once.  This helps the "
            "compact-threshold mechanism; it does not yet replace the missing "
            "action-level proof."
        ),
    }


if __name__ == "__main__":
    result = dressing_mass_conservation_status()
    print("PHASE 15b: Dressing mass conservation gate")
    print("status:", result["status"])
    print("closed_now:")
    for item in result["closed_now"]:
        print("  -", item)
    print("not_closed_now:")
    for item in result["not_closed_now"]:
        print("  -", item)
    print("ledger:", result["ledger"]["status"])
    print("mass residual:", result["ledger"]["mass_conservation_residual"])
    print(
        "active-readout compactness / initial:",
        result["ledger"]["core_compactness_over_initial"],
    )
    print(
        "total compactness / initial:",
        result["ledger"]["total_compactness_over_initial"],
    )
    print("ADM/source:", result["adm_source_separation"]["status"])
    print(
        "coordinate source / ADM:",
        result["adm_source_separation"]["coordinate_source_to_ADM_ratio"],
    )
    print("C2:", result["c2_integral_gate"]["status"])
    print("Noether:", result["noether_bridge"]["status"])
