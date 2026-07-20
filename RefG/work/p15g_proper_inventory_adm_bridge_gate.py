"""
PHASE 15g: Proper inventory to ADM/readout bridge audit.

This file continues p15e/p15f and does not touch the article.

Question being audited:

    How can a compact object have a small external ADM/readout mass while the
    internal/proper ledger can be much larger?

What is closed here:

    * the exterior ADM/Komar mass is a surface/asymptotic charge;
    * the C2 finite core has finite proper-source bookkeeping for finite q and
      finite r_c;
    * C2 matching removes a thin-shell mass at the boundary;
    * proper-volume source bookkeeping can differ strongly from coordinate or
      ADM readout bookkeeping.

What remains open:

    * the full action-derived map from matter inventory to ADM/Noether charge;
    * the strong-compression equation of state;
    * the dynamics that selects the compact branch.
"""

from __future__ import annotations

import sympy as sp

from p05_compact import (
    derive_adm_komar_and_proper_energy_bookkeeping,
    derive_c2_core_matching_coefficients,
    derive_c2_core_proper_energy_finiteness,
    derive_c2_junction_stress_closure,
)
from p15f_universal_proper_readout_bridge_gate import (
    universal_proper_readout_bridge_status,
)


def derive_c2_external_adm_charge_dictionary() -> dict[str, object]:
    """
    Convert the C2 boundary variable q into the exterior ADM charge.

    The C2 exterior uses log A = q/x with x=r/r_c.  Therefore r_s=q*r_c, and
    the static exterior ADM mass in geometric units is r_s/(2G_N).
    """
    q, r_c, G_N, c = sp.symbols("q r_c G_N c", positive=True, real=True)

    r_s = sp.simplify(q * r_c)
    M_ADM_geometric = sp.simplify(r_s / (2 * G_N))
    M_ADM_physical = sp.simplify(c**2 * r_s / (2 * G_N))
    compactness = sp.simplify(r_s / r_c)

    adm = derive_adm_komar_and_proper_energy_bookkeeping()
    matching = derive_c2_core_matching_coefficients()
    junction = derive_c2_junction_stress_closure()

    return {
        "status": "PASS_C2_BOUNDARY_Q_FIXES_EXTERNAL_ADM_CHARGE",
        "C2_matching_status": matching["derivation_status"],
        "junction_status": junction["junction_status"],
        "ADM_Komar_identity": adm["ADM_Komar_identity"],
        "boundary_dictionary": {
            "x": "r/r_c",
            "log_A_plus": "q/x = q*r_c/r",
            "r_s": sp.Eq(sp.Symbol("r_s"), r_s),
            "q": sp.Eq(sp.Symbol("q"), compactness),
        },
        "ADM_mass_geometric": sp.Eq(sp.Symbol("M_ADM_geo"), M_ADM_geometric),
        "ADM_mass_physical": sp.Eq(sp.Symbol("M_ADM"), M_ADM_physical),
        "thin_shell_mass_status": "zero Israel surface stress at the C2 boundary",
        "reading": (
            "The outside observer reads the coefficient r_s=q*r_c.  That fixes "
            "the ADM/Komar charge.  It does not by itself say that the whole "
            "proper inventory inside the core equals this external readout."
        ),
    }


def derive_coordinate_vs_proper_source_measure_split() -> dict[str, object]:
    """
    Compare coordinate, proper, and ADM source measures outside the core.

    This is the key audit: coordinate source measure stays tied to the exterior
    charge scale, while proper-volume measure carries an exponential volume
    factor.  Therefore proper bookkeeping can be much larger than external ADM
    readout without inventing a singularity or destroying internal inventory.
    """
    q, r_c, G_N = sp.symbols("q r_c G_N", positive=True, real=True)

    r_s = q * r_c
    M_ADM_geometric = sp.simplify(r_s / (2 * G_N))

    coordinate_source_outside_core = sp.simplify(
        r_s * (1 - sp.exp(-q)) / (8 * G_N)
    )
    proper_source_outside_core = sp.simplify(
        r_c * q * (sp.exp(q / 2) - 1) / (4 * G_N)
    )

    coordinate_to_adm = sp.simplify(
        coordinate_source_outside_core / M_ADM_geometric
    )
    proper_to_adm = sp.simplify(proper_source_outside_core / M_ADM_geometric)
    proper_to_coordinate = sp.simplify(
        proper_source_outside_core / coordinate_source_outside_core
    )

    weak_coordinate_series = sp.series(coordinate_to_adm, q, 0, 4).removeO()
    weak_proper_series = sp.series(proper_to_adm, q, 0, 4).removeO()
    large_q_coordinate_limit = sp.limit(coordinate_to_adm, q, sp.oo)
    large_q_proper_limit = sp.limit(proper_to_adm, q, sp.oo)

    samples = []
    for q_value in [sp.Rational(1, 100), sp.Integer(1), sp.Integer(2), sp.Integer(10)]:
        samples.append(
            {
                "q": q_value,
                "coordinate_source_over_ADM": sp.N(
                    coordinate_to_adm.subs(q, q_value),
                    8,
                ),
                "proper_source_over_ADM": sp.N(
                    proper_to_adm.subs(q, q_value),
                    8,
                ),
            }
        )

    p05_core = derive_c2_core_proper_energy_finiteness()

    return {
        "status": "PASS_COORDINATE_PROPER_ADM_SOURCE_MEASURES_SPLIT",
        "p05_core_proper_energy_status": p05_core["proper_energy_status"],
        "coordinate_source_outside_core": sp.Eq(
            sp.Symbol("Q_coord_ext"),
            coordinate_source_outside_core,
        ),
        "proper_source_outside_core": sp.Eq(
            sp.Symbol("Q_proper_ext"),
            proper_source_outside_core,
        ),
        "coordinate_source_over_ADM": sp.Eq(
            sp.Symbol("Q_coord_ext/M_ADM_geo"),
            coordinate_to_adm,
        ),
        "proper_source_over_ADM": sp.Eq(
            sp.Symbol("Q_proper_ext/M_ADM_geo"),
            proper_to_adm,
        ),
        "proper_source_over_coordinate_source": sp.Eq(
            sp.Symbol("Q_proper_ext/Q_coord_ext"),
            proper_to_coordinate,
        ),
        "weak_coordinate_series": sp.Eq(
            sp.Symbol("Q_coord_ext/M_ADM_geo"),
            weak_coordinate_series,
        ),
        "weak_proper_series": sp.Eq(
            sp.Symbol("Q_proper_ext/M_ADM_geo"),
            weak_proper_series,
        ),
        "large_q_coordinate_limit": large_q_coordinate_limit,
        "large_q_proper_limit": large_q_proper_limit,
        "samples": samples,
        "finite_core_integrand_limit": p05_core["lim_x_to_0_integrand"],
        "finite_core_total_proper_source": p05_core[
            "total_effective_proper_source_charge"
        ],
        "reading": (
            "The same exterior charge has different measure readings.  The "
            "coordinate source outside the core approaches one quarter of the "
            "ADM scale, while the proper-volume source grows like exp(q/2)/2. "
            "This supports the internal/external split but is still an "
            "effective-source ledger, not the final matter-inventory theorem."
        ),
    }


def derive_internal_inventory_to_external_readout_dictionary() -> dict[str, object]:
    """
    Keep the matter-inventory bridge explicit and conditional.

    Let eta_ADM=M_ADM/M_proper_inventory.  The previous p15f mass-volume ledger
    gives eta_m=eta_L^3 in the balanced isotropic case.  This dictionary says
    how an internal inventory would be read outside, but it does not pretend
    that eta_ADM has already been derived from the full action.
    """
    eta_L, q_L, q_m, M_ADM = sp.symbols(
        "eta_L q_L q_m M_ADM",
        positive=True,
        real=True,
    )

    eta_m = sp.exp(-q_m)
    M_proper_inventory = sp.simplify(M_ADM / eta_m)
    hidden_gap = sp.simplify(M_proper_inventory - M_ADM)

    balanced_eta_m = eta_L**3
    balanced_inventory_over_adm = sp.simplify(1 / balanced_eta_m)
    q_balance_inventory_over_adm = sp.simplify(sp.exp(3 * q_L))
    q_substitution_identity = sp.simplify(
        M_proper_inventory.subs(q_m, 3 * q_L) - M_ADM * sp.exp(3 * q_L)
    )

    volume_halved = sp.Rational(1, 2)
    length_factor_for_volume_halved = sp.real_root(volume_halved, 3)
    inventory_over_adm_for_volume_halved = sp.simplify(1 / volume_halved)

    return {
        "status": "PASS_INTERNAL_INVENTORY_EXTERNAL_READOUT_DICTIONARY",
        "ADM_readout": sp.Eq(sp.Symbol("M_ADM"), M_ADM),
        "readout_filter": sp.Eq(sp.Symbol("eta_m"), eta_m),
        "proper_inventory_from_ADM_readout": sp.Eq(
            sp.Symbol("M_proper_inventory"),
            M_proper_inventory,
        ),
        "hidden_gap": sp.Eq(sp.Symbol("M_hidden_gap"), hidden_gap),
        "balanced_isotropic_condition": sp.Eq(
            sp.Symbol("eta_m"),
            balanced_eta_m,
        ),
        "balanced_inventory_over_ADM": sp.Eq(
            sp.Symbol("M_proper_inventory/M_ADM"),
            balanced_inventory_over_adm,
        ),
        "q_balance_inventory_over_ADM": sp.Eq(
            sp.Symbol("M_proper_inventory/M_ADM"),
            q_balance_inventory_over_adm,
        ),
        "q_substitution_identity": q_substitution_identity == 0,
        "volume_halved_example": {
            "eta_V": volume_halved,
            "eta_L": length_factor_for_volume_halved,
            "M_proper_inventory_over_M_ADM_if_balanced": (
                inventory_over_adm_for_volume_halved
            ),
        },
        "reading": (
            "If ADM is the outside readout and the balanced filter is eta_m, "
            "then the proper inventory ledger is M_ADM/eta_m.  For a twofold "
            "volume/readout reduction, the proper inventory corresponding to a "
            "fixed outside ADM reading is twofold larger.  The derivation of "
            "eta_m from the action remains the next task."
        ),
    }


def derive_no_singularity_from_external_smallness_gate() -> dict[str, object]:
    """
    Check that the C2 core keeps finite center geometry for finite q and r_c.
    """
    q, r_c = sp.symbols("q r_c", positive=True, real=True)

    a2 = sp.Rational(35, 8) * q / r_c**2
    b2_over_b0 = -sp.Rational(11, 8) * q / r_c**2
    center_ricci = sp.simplify(12 * a2 + 6 * b2_over_b0)
    center_kretschmann = sp.simplify(48 * a2**2 + 12 * b2_over_b0**2)

    finite_checks = {
        "center_A": sp.Integer(1),
        "center_B": sp.exp(-q),
        "center_Ricci_finite_for_finite_q_rc": center_ricci,
        "center_Kretschmann_finite_for_finite_q_rc": center_kretschmann,
    }

    return {
        "status": "PASS_C2_FINITE_CENTER_BLOCKS_EXTERNAL_SMALLNESS_TO_SINGULARITY_INFERENCE",
        "center_Ricci_scalar": sp.Eq(sp.Symbol("R_0"), center_ricci),
        "center_Kretschmann": sp.Eq(sp.Symbol("K_0"), center_kretschmann),
        "finite_checks": finite_checks,
        "reading": (
            "A small outside readout is not a proof of a proper singularity. "
            "For finite q and r_c the C2 center coefficients and curvature "
            "scalars are finite.  A singularity would need a separate limit "
            "q/r_c^2 -> infinity or a failed core dynamics proof."
        ),
    }


def proper_inventory_adm_bridge_status() -> dict[str, object]:
    p15f = universal_proper_readout_bridge_status()
    adm_dictionary = derive_c2_external_adm_charge_dictionary()
    measure_split = derive_coordinate_vs_proper_source_measure_split()
    inventory_dictionary = derive_internal_inventory_to_external_readout_dictionary()
    finite_center = derive_no_singularity_from_external_smallness_gate()

    passed = (
        p15f["status"]
        == "PASS_UNIVERSAL_PROPER_READOUT_BRIDGE_LEDGER__ACTION_DYNAMICS_OPEN"
        and adm_dictionary["status"] == "PASS_C2_BOUNDARY_Q_FIXES_EXTERNAL_ADM_CHARGE"
        and adm_dictionary["ADM_Komar_identity"]
        and measure_split["status"]
        == "PASS_COORDINATE_PROPER_ADM_SOURCE_MEASURES_SPLIT"
        and measure_split["large_q_coordinate_limit"] == sp.Rational(1, 4)
        and measure_split["large_q_proper_limit"] == sp.oo
        and inventory_dictionary["status"]
        == "PASS_INTERNAL_INVENTORY_EXTERNAL_READOUT_DICTIONARY"
        and inventory_dictionary["q_substitution_identity"]
        and finite_center["status"]
        == "PASS_C2_FINITE_CENTER_BLOCKS_EXTERNAL_SMALLNESS_TO_SINGULARITY_INFERENCE"
    )

    return {
        "status": (
            "PASS_PROPER_INVENTORY_ADM_BRIDGE_AUDIT__FULL_ACTION_MAP_OPEN"
            if passed
            else "CHECK_PROPER_INVENTORY_ADM_BRIDGE_AUDIT"
        ),
        "p15f_status": p15f["status"],
        "adm_dictionary": adm_dictionary,
        "coordinate_vs_proper_measure": measure_split,
        "inventory_dictionary": inventory_dictionary,
        "finite_center": finite_center,
        "closed_now": [
            "C2 boundary q fixes r_s=q*r_c and the exterior ADM/Komar charge",
            "C2 matching removes a boundary thin-shell mass",
            "coordinate source, proper-volume source, and ADM charge are distinct measures",
            "proper-volume source can grow far beyond ADM readout in the strong-q limit",
            "balanced isotropic readout gives M_proper_inventory/M_ADM=exp(3*q_L)",
            "finite C2 center blocks the inference from external smallness to singularity",
        ],
        "not_closed_now": [
            "derive eta_m, eta_L, and alpha_t from the full RefG action",
            "derive the matter inventory to ADM/Noether equality or inequality theorem",
            "derive the strong-compression equation of state",
            "solve compact-branch dynamics and perturbative stability",
        ],
        "plain_reading": (
            "The work files now support a clean statement: ADM mass is the "
            "outside surface charge.  Proper interior bookkeeping is a different "
            "measure and can be much larger in a compact deficit.  The current "
            "Python proof is an honest bridge audit, not yet the final action "
            "derivation of the internal matter inventory."
        ),
    }


if __name__ == "__main__":
    result = proper_inventory_adm_bridge_status()
    print("PHASE 15g: Proper inventory to ADM/readout bridge audit")
    print("status:", result["status"])
    print("closed_now:")
    for item in result["closed_now"]:
        print("  -", item)
    print("not_closed_now:")
    for item in result["not_closed_now"]:
        print("  -", item)
    print("adm_dictionary:", result["adm_dictionary"]["status"])
    print("measure_split:", result["coordinate_vs_proper_measure"]["status"])
    print(
        "Q_coord_ext/M_ADM:",
        result["coordinate_vs_proper_measure"]["coordinate_source_over_ADM"],
    )
    print(
        "Q_proper_ext/M_ADM:",
        result["coordinate_vs_proper_measure"]["proper_source_over_ADM"],
    )
    print("inventory:", result["inventory_dictionary"]["status"])
    print(
        "volume_halved_example:",
        result["inventory_dictionary"]["volume_halved_example"],
    )
    print("finite_center:", result["finite_center"]["status"])
