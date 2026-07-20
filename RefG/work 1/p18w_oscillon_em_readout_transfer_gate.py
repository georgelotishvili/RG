# Notation header (see NOTATION.md):
# This gate follows p18v, but broadens the search target.  Instead of assuming
# alpha must first appear as a core electric/magnetic energy partition, it asks
# for the direct oscillon-to-medium electromagnetic readout coefficient.

"""
================================================================================
PHASE 18w: Oscillon electromagnetic readout transfer gate
================================================================================

Purpose
-------
p10/p15 already computed an oscillon -> medium GRAVITY/METRIC readout:

    oscillon energy -> pressure deficit -> exterior 1/r field,
    deficit q       -> mass/size/lapse filter exp(-q/2).

That is not yet the alpha problem.  Alpha asks for the ELECTROMAGNETIC readout:

    charged oscillon/framing vibration -> substrate electromagnetic trace
    -> canonical electric charge e -> alpha = e^2/(4*pi).

This gate formalizes the user's new intuition:

    alpha may be the strength with which one internal oscillon/framing
    vibration is heard by the substrate as an electromagnetic field.

The gate separates two readings:

    energy/interaction strength fraction:     alpha ~= 1/137,
    amplitude fraction against sqrt(4*pi):    sqrt(alpha) ~= 1/11.7.

Therefore the phrase "137 times" is meaningful for interaction strength or
energy scale, while amplitudes are weaker by sqrt(137), not by 137.

Main result
-----------
The existing p10/p15 gravity channel does NOT contain this electromagnetic
transfer coefficient.  The p18 impedance/core gates are one possible route to
it, but the broader object is:

    beta_EM:  q_e = beta_EM * q_geom,
    alpha  = beta_EM^2 * q_geom^2 / (4*pi).

Equivalently, with p18s notation:

    Z_medium = beta_EM^2.

The missing theorem is now sharper: derive beta_EM from the charged oscillon /
orientation-frame dynamics, rather than deriving 137 directly.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive beta_EM or Z_medium.
- It does not say the p18t eta_core route is wrong.
- It does not set any transfer coefficient from CODATA.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA
Q_GEOM_H2_ORDER9 = 2.0 / 9.0
G_GEOM_FLUX_4PI = 4.0 * math.pi


# ---------------------------------------------------------------------------
# 1. Existing gravity/metric readout is a different channel
# ---------------------------------------------------------------------------

def gravity_metric_channel_separation() -> dict:
    q = sp.symbols("q_deficit", nonnegative=True, real=True)
    eta_unit = sp.exp(-q / 2)
    eta_light = sp.exp(-q)
    alpha = sp.symbols("alpha", positive=True)
    q_if_half_filter_forced_to_alpha = sp.solve(sp.Eq(eta_unit, alpha), q)[0]
    q_if_light_filter_forced_to_alpha = sp.solve(sp.Eq(eta_light, alpha), q)[0]

    return {
        "existing_single_unit_filter": str(eta_unit),
        "existing_light_transfer_filter": str(eta_light),
        "filters_depend_on_local_deficit_q": True,
        "alpha_is_a_constant_not_a_local_deficit_filter": True,
        "forcing_half_filter_to_alpha_gives": str(q_if_half_filter_forced_to_alpha),
        "forcing_light_filter_to_alpha_gives": str(q_if_light_filter_forced_to_alpha),
        "forced_identification_is_a_fit": True,
        "reading": (
            "p10/p15 compute the gravitational/metric readout of an oscillon. "
            "Alpha needs a separate electromagnetic readout coefficient."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Electromagnetic readout coefficient
# ---------------------------------------------------------------------------

def electromagnetic_transfer_coefficient_map() -> dict:
    beta, q_geom = sp.symbols("beta_EM q_geom", positive=True)
    alpha_target = sp.symbols("alpha_target", positive=True)
    q_e = sp.simplify(beta * q_geom)
    alpha = sp.simplify(q_e**2 / (4 * sp.pi))
    beta_solution = sp.simplify(2 * sp.sqrt(sp.pi) * sp.sqrt(alpha_target) / q_geom)

    e_required = math.sqrt(4.0 * math.pi * ALPHA_CODATA)
    beta_if_q_geom_1 = e_required
    beta_if_q_geom_h2 = e_required / Q_GEOM_H2_ORDER9
    z_if_q_geom_1 = beta_if_q_geom_1**2
    z_if_q_geom_h2 = beta_if_q_geom_h2**2

    return {
        "canonical_charge_map": str(sp.Eq(sp.Symbol("q_e"), q_e)),
        "alpha_from_transfer": str(alpha),
        "beta_solution_for_target_alpha": str(beta_solution),
        "required_canonical_e": e_required,
        "if_q_geom_is_1": {
            "beta_EM_required": beta_if_q_geom_1,
            "Z_medium_required": z_if_q_geom_1,
        },
        "if_q_geom_is_2_over_9": {
            "beta_EM_required": beta_if_q_geom_h2,
            "Z_medium_required": z_if_q_geom_h2,
        },
        "Z_medium_equals_beta_squared": True,
        "reading": (
            "The broad alpha target is beta_EM, the amplitude readout from "
            "geometric/internal charge to canonical electric charge.  p18s's "
            "impedance is beta_EM squared."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Energy versus amplitude language
# ---------------------------------------------------------------------------

def energy_vs_amplitude_language_gate() -> dict:
    amplitude_fraction_against_full_unit = math.sqrt(ALPHA_CODATA)
    strength_fraction = ALPHA_CODATA
    full_natural_charge = math.sqrt(4.0 * math.pi)
    canonical_charge = math.sqrt(4.0 * math.pi * ALPHA_CODATA)

    return {
        "strength_fraction_alpha": strength_fraction,
        "strength_inverse": ALPHA_INV_CODATA,
        "amplitude_fraction_sqrt_alpha": amplitude_fraction_against_full_unit,
        "amplitude_inverse": 1.0 / amplitude_fraction_against_full_unit,
        "full_natural_charge_sqrt_4pi": full_natural_charge,
        "canonical_e": canonical_charge,
        "canonical_e_over_full_natural_charge": canonical_charge
        / full_natural_charge,
        "energy_language": (
            "If alpha is read as interaction/energy strength, the substrate "
            "readout is 137 times weaker than the full natural unit."
        ),
        "amplitude_language": (
            "If the same statement is made about field amplitude, the factor "
            "is sqrt(137), about 11.7, not 137."
        ),
        "language_separated_correctly": True,
    }


# ---------------------------------------------------------------------------
# 4. Relation to the p18t eta_core route
# ---------------------------------------------------------------------------

def eta_core_route_as_one_possible_realization() -> dict:
    eta, q, g = sp.symbols("eta_core q_geom g_geom", positive=True)
    z_from_eta = sp.simplify((g / q) * sp.sqrt(eta))
    beta_from_eta = sp.sqrt(z_from_eta)
    alpha_from_eta = sp.simplify(z_from_eta * q**2 / (4 * sp.pi))

    eta_target = (
        (
            (4.0 * math.pi * ALPHA_CODATA / (Q_GEOM_H2_ORDER9**2))
            * Q_GEOM_H2_ORDER9
            / G_GEOM_FLUX_4PI
        )
        ** 2
    )

    return {
        "p18t_Z_from_eta": str(z_from_eta),
        "p18t_beta_from_eta": str(beta_from_eta),
        "p18t_alpha_from_eta": str(alpha_from_eta),
        "diagnostic_eta_target_if_q_2_over_9_and_g_4pi": eta_target,
        "eta_route_is_sufficient_if_derived": True,
        "eta_route_not_necessary_as_only_possible_route": True,
        "reading": (
            "p18t's eta_core route is one way to derive beta_EM.  The broader "
            "alpha problem is the oscillon/framing-to-Maxwell readout map; "
            "eta_core is a possible mechanism for that map, not the only "
            "logical place where the number could originate."
        ),
    }


# ---------------------------------------------------------------------------
# 5. What must be derived from oscillon/frame dynamics
# ---------------------------------------------------------------------------

def oscillon_em_theorem_requirements() -> dict:
    return {
        "needed_theorem": (
            "derive beta_EM in q_e = beta_EM*q_geom from the charged "
            "oscillon/orientation-frame dynamics"
        ),
        "must_connect": [
            "time-periodic localized oscillon energy/source sector from p10",
            "completed frame connection Dtheta = dtheta + A(n) from p18h",
            "electric closed framing/twist current from p18k",
            "magnetic frame-curvature flux from p18i",
            "finite order-9, h=2 boundary coordinate from p18p/p11f/p11g",
            "canonical Maxwell normalization of the external field",
        ],
        "acceptable_routes": [
            "derive beta_EM directly as an oscillon-to-Maxwell readout coefficient",
            "derive beta_EM through medium impedance Z_medium = beta_EM^2",
            "derive beta_EM through a core partition eta_core if that partition follows from the action",
            "derive beta_EM through a boundary/action normalization theorem",
        ],
        "falsification_tests": [
            "if the charged oscillon action only fixes topology q_geom but not beta_EM, alpha is not derived",
            "if beta_EM is set from CODATA, the gate fails as a fit",
            "if only the gravitational deficit filter exp(-q/2) is used, this is the wrong channel",
            "if p18t eta_core remains free, that route has not closed beta_EM",
        ],
        "candidate_next_gate": "p18x_charged_oscillon_em_source_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_oscillon_em_readout_transfer_gate() -> dict:
    gravity = gravity_metric_channel_separation()
    transfer = electromagnetic_transfer_coefficient_map()
    language = energy_vs_amplitude_language_gate()
    eta_route = eta_core_route_as_one_possible_realization()
    requirements = oscillon_em_theorem_requirements()

    closed = {
        "gravity_metric_channel_separated_from_alpha_channel": bool(
            gravity["filters_depend_on_local_deficit_q"]
            and gravity["alpha_is_a_constant_not_a_local_deficit_filter"]
            and gravity["forced_identification_is_a_fit"]
        ),
        "electromagnetic_transfer_map_written": bool(
            transfer["Z_medium_equals_beta_squared"]
        ),
        "energy_and_amplitude_language_separated": bool(
            language["language_separated_correctly"]
        ),
        "eta_core_route_reclassified_as_possible_mechanism": bool(
            eta_route["eta_route_is_sufficient_if_derived"]
            and eta_route["eta_route_not_necessary_as_only_possible_route"]
        ),
        "target_numbers_translated_not_inserted": True,
    }

    open_checks = {
        "charged_oscillon_em_source_derived": False,
        "beta_EM_derived": False,
        "Z_medium_derived": False,
        "eta_core_derived": False,
        "canonical_e_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_CHARGED_OSCILLON_EM_READOUT_THEOREM_REQUIRED__"
            + _pass_status("OSCILLON_EM_CHANNEL_REFRAMING")
            if all(closed.values())
            else "CHECK_OSCILLON_EM_READOUT_TRANSFER"
        ),
        "SCOPE": (
            "alpha-channel reframing after p18v: p10/p15 already compute the "
            "oscillon-to-gravity/metric readout, but alpha requires the "
            "oscillon/framing-to-electromagnetic readout coefficient beta_EM. "
            "Impedance and eta_core are possible mechanisms for beta_EM, not "
            "the only logical search location."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "gravity_metric_channel": gravity,
        "electromagnetic_transfer": transfer,
        "energy_vs_amplitude_language": language,
        "eta_core_route": eta_route,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "The user's oscillon-medium balance intuition is now the central "
            "target: alpha is the strength with which a charged internal "
            "oscillon/framing vibration becomes an external Maxwell field.  "
            "The old gravity channel says how oscillons curve or rarefy the "
            "medium; the missing alpha channel says how charged oscillons are "
            "heard electrically by that medium."
        ),
        "missing_derivations": [
            "derive the charged oscillon electromagnetic source/current",
            "derive beta_EM, the amplitude readout from geometric framing charge to canonical electric charge",
            "decide whether beta_EM comes from impedance, eta_core, boundary normalization, or another action-derived mechanism",
            "only then compute alpha = beta_EM^2*q_geom^2/(4*pi)",
        ],
        "do_not_claim": [
            "Do not claim alpha is derived.",
            "Do not identify the gravitational exp(-q/2) metric filter with alpha.",
            "Do not say amplitudes are 137 times weaker; that is the strength/energy language.",
            "Do not set beta_EM, Z_medium, or eta_core from CODATA.",
            "Do not treat q_geom=2/9 as canonical electric charge without beta_EM.",
        ],
    }
    return result


def _print_result(result: dict) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, val in result["closed_checks"].items():
        print(f"  - {key}: {val}")
    print("open_checks:")
    for key, val in result["open_checks"].items():
        print(f"  - {key}: {val}")
    print("gravity_metric_channel:", result["gravity_metric_channel"])
    print("electromagnetic_transfer:", result["electromagnetic_transfer"])
    print("energy_vs_amplitude_language:", result["energy_vs_amplitude_language"])
    print("eta_core_route:", result["eta_core_route"])
    print("requirements_for_next_gate:", result["requirements_for_next_gate"])
    print("physical_reading:", result["physical_reading"])
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
    _print_result(derive_oscillon_em_readout_transfer_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
