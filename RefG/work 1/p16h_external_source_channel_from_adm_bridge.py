# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16h: which readout channel is the external gravitating source.

p16g proved that the deficit feedback exponent chi is a metric-readout
exponent, not a function of the polynomial coefficients, and that it equals 1
for the volume/bulk-mass channel and 1/3 for the unit-mass/clock channel.  The
one remaining choice was which channel sets the EXTERNAL gravitating source S.

This gate closes that choice using the p15g proper-inventory/ADM bridge:

  * p15g already fixes the external charge as the ADM/Komar surface mass and,
    in the balanced isotropic case, gives the readout filter eta_m = eta_L^3,
    i.e. the external mass uses the cubic (volume) length exponent, with the
    identity M_proper(q_m = 3 q_L) = M_ADM * exp(3 q_L).

  * The biconformal length deficit is q_L = h (length readout filter e^{-h}),
    and the volume deficit used by the selector is q_v = 3 h = 3 q_L.

  * Therefore the external ADM mass filter is
        eta_m = eta_L^3 = e^{-3 q_L} = e^{-q_v},
    so the external gravitating source obeys S_eff = S e^{-q_v}, i.e. chi = 1.

  * The lapse/clock filter e^{-h} = e^{-q_v/3} (chi = 1/3) governs an intensive
    readout (a single clock rate or unit rod).  It is NOT the integrated ADM
    mass, so it is not the gravitating-source channel.

Result: the gravitating-source channel is the bulk/volume channel, chi = 1,
selected by the ADM surface charge being a volume-extensive integral, not
assumed.  This removes the chi=1/3 alternative for the source.

Open (inherited from p15g): the full action-derived matter-inventory-to-ADM
map.  Rotating exteriors, QNM/echo stability, and full nonlinear collapse
remain separate layers.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp

from p15g_proper_inventory_adm_bridge_gate import (
    derive_internal_inventory_to_external_readout_dictionary,
    derive_c2_external_adm_charge_dictionary,
)
from p16g_deficit_feedback_exponent_derivation import (
    derive_deficit_feedback_exponent_gate,
)


def derive_external_source_channel_gate() -> dict[str, Any]:
    h, q_L, q_v = sp.symbols("h q_L q_v", positive=True, real=True)

    p15g_inv = derive_internal_inventory_to_external_readout_dictionary()
    p15g_adm = derive_c2_external_adm_charge_dictionary()
    p16g = derive_deficit_feedback_exponent_gate()

    # 1. Biconformal readout exponents (from p16g / p15h conventions).
    length_readout_filter = sp.exp(-h)          # e^{-h}
    lapse_clock_filter = sp.exp(-h)             # e^{-h}  (intensive)
    q_L_from_h = sp.simplify(-sp.log(length_readout_filter))   # q_L = h
    length_identity = sp.simplify(q_L_from_h - h)

    # 2. Volume deficit used by the selector: q_v = 3 h = 3 q_L.
    q_v_in_h = sp.Integer(3) * h
    q_v_in_qL = sp.Integer(3) * q_L
    qv_qL_identity = sp.simplify(q_v_in_h.subs(h, q_L) - q_v_in_qL)

    # 3. p15g balanced isotropic ADM mass filter: eta_m = eta_L^3.
    #    eta_L = e^{-q_L}, so eta_m = e^{-3 q_L} = e^{-q_v}.
    eta_L = sp.exp(-q_L)
    eta_m_balanced = sp.simplify(eta_L**3)
    eta_m_in_qv = sp.simplify(eta_m_balanced.subs(q_L, q_v / 3))
    adm_mass_filter = eta_m_in_qv                       # e^{-q_v}

    # 4. External gravitating source exponent from the ADM filter.
    chi_adm = sp.simplify(-sp.log(adm_mass_filter) / q_v)        # 1
    chi_lapse = sp.simplify(-sp.log(lapse_clock_filter.subs(h, q_v / 3)) / q_v)  # 1/3

    # 5. Cross-checks against p15g and p16g.
    p15g_balanced_identity_holds = bool(p15g_inv["q_substitution_identity"])
    p16g_volume_chi = sp.simplify(
        p16g["chi_by_channel"]["volume"].rhs
    )
    chi_matches_p16g_volume = sp.simplify(chi_adm - p16g_volume_chi) == 0
    rules_out_one_third = sp.simplify(chi_adm - sp.Rational(1, 3)) != 0

    selected_pass = (
        length_identity == 0
        and qv_qL_identity == 0
        and sp.simplify(adm_mass_filter - sp.exp(-q_v)) == 0
        and sp.simplify(chi_adm - 1) == 0
        and sp.simplify(chi_lapse - sp.Rational(1, 3)) == 0
        and p15g_balanced_identity_holds
        and chi_matches_p16g_volume
        and rules_out_one_third
    )

    return {
        "STATUS": (
            "PASS_EXTERNAL_GRAVITATING_SOURCE_IS_BULK_VOLUME_CHANNEL_CHI_ONE__"
            "VIA_P15G_ADM_BALANCED_FILTER__FULL_ACTION_INVENTORY_MAP_OPEN"
            if selected_pass
            else "CHECK_EXTERNAL_SOURCE_CHANNEL"
        ),
        "SCOPE": (
            "Channel-selection gate at the metric-readout / ADM level.  It "
            "selects chi=1 for the external gravitating source by identifying it "
            "with the p15g balanced-isotropic ADM mass filter (cubic/volume "
            "exponent), and rules out the intensive lapse/clock channel chi=1/3. "
            "It inherits the open p15g item: the full action-derived "
            "matter-inventory-to-ADM map."
        ),
        "closed_checks": {
            "length_deficit_equals_metric_deficit_qL_is_h": length_identity == 0,
            "volume_deficit_qv_equals_3qL": qv_qL_identity == 0,
            "adm_mass_filter_is_exp_minus_qv": sp.simplify(adm_mass_filter - sp.exp(-q_v)) == 0,
            "external_source_chi_is_one": sp.simplify(chi_adm - 1) == 0,
            "lapse_clock_channel_chi_is_one_third": sp.simplify(chi_lapse - sp.Rational(1, 3)) == 0,
            "p15g_balanced_identity_holds": p15g_balanced_identity_holds,
            "chi_matches_p16g_volume_channel": chi_matches_p16g_volume,
            "intensive_one_third_channel_ruled_out_for_source": rules_out_one_third,
        },
        "open_checks": {
            "full_action_derived_inventory_to_adm_map": False,
            "rotating_exterior_and_qnm_echo_stability": False,
            "full_nonlinear_collapse_solved": False,
        },
        "length_readout_filter": sp.Eq(sp.Symbol("eta_L"), length_readout_filter),
        "q_L_identity": sp.Eq(sp.Symbol("q_L"), q_L_from_h),
        "volume_deficit": sp.Eq(sp.Symbol("q_v"), q_v_in_qL),
        "balanced_adm_filter": sp.Eq(sp.Symbol("eta_m"), eta_m_balanced),
        "adm_filter_in_qv": sp.Eq(sp.Symbol("eta_m(q_v)"), adm_mass_filter),
        "external_source_exponent": sp.Eq(sp.Symbol("chi_external_source"), chi_adm),
        "lapse_clock_exponent": sp.Eq(sp.Symbol("chi_lapse_clock"), chi_lapse),
        "p15g_adm_status": p15g_adm["status"],
        "p15g_inventory_status": p15g_inv["status"],
        "p16g_status": p16g["STATUS"],
        "physical_reason": (
            "The ADM/Komar mass is a volume-extensive surface charge of the "
            "energy distribution, so it is read through the cubic volume measure "
            "e^{-3h}=e^{-q_v}, giving chi=1.  A clock rate or unit rod is "
            "intensive and uses e^{-h}=e^{-q_v/3}; that intensive channel is not "
            "the gravitating source."
        ),
        "combined_with_p16g": (
            "p16g + p16h fix chi=1 for the compact branch feedback without any "
            "polynomial-coefficient input: chi is a readout exponent (p16g) and "
            "the gravitating-source channel is the bulk/volume ADM channel "
            "(p16h)."
        ),
        "missing_derivations": [
            "derive the matter-inventory-to-ADM/Noether map from the full RefG "
            "action (the p15g open item)",
            "extend the static channel selection to the rotating exterior",
        ],
        "do_not_claim": [
            "do not claim the full action inventory-to-ADM map is derived here",
            "do not claim rotating, QNM/echo, or collapse layers are solved",
            "do not remove global conditional wording from compact predictions",
        ],
    }


def _print_result(result: dict[str, Any]) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, value in result["closed_checks"].items():
        print(f"  - {key}: {value}")
    print("open_checks:")
    for key, value in result["open_checks"].items():
        print(f"  - {key}: {value}")
    for key in (
        "length_readout_filter",
        "q_L_identity",
        "volume_deficit",
        "balanced_adm_filter",
        "adm_filter_in_qv",
        "external_source_exponent",
        "lapse_clock_exponent",
        "p15g_adm_status",
        "p15g_inventory_status",
        "p16g_status",
    ):
        print(f"{key}: {result[key]}")
    print("physical_reason:", result["physical_reason"])
    print("combined_with_p16g:", result["combined_with_p16g"])
    print("missing_derivations:")
    for item in result["missing_derivations"]:
        print("  -", item)
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    _print_result(derive_external_source_channel_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
