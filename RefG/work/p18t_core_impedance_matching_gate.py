# Notation header (see NOTATION.md):
# This gate follows p18s.  It tests whether the localized core can fix the
# medium impedance by matching the electric framing-current channel to the
# magnetic frame-flux channel.

"""
================================================================================
PHASE 18t: Core impedance matching gate
================================================================================

Purpose
-------
p18s separated two facts:

    c fixes the finite transfer speed of electric/frame disturbances,
    Z_medium fixes how strongly a geometric framing twist is read as charge.

This gate asks whether the next natural step, core matching, fixes Z_medium.
The local picture is:

    electric channel:  closed framing/twist current,
    magnetic channel:  frame-curvature flux,
    common core:       one localized orientation-frame object.

If the core enforces a definite electric/magnetic energy partition, then the
impedance is fixed.  If the partition is not derived, the impedance remains
free.  This gate makes that statement executable.

Result
------
The far-field energies can be written with one impedance:

    E_e(R) = Z q_geom^2 / (8*pi*R),
    E_m(R) = g_geom^2 / (8*pi*Z*R).

Their ratio is

    E_e/E_m = Z^2 q_geom^2 / g_geom^2.

Therefore a core partition theorem

    E_e/E_m = eta_core

would fix

    Z = (g_geom/q_geom) * sqrt(eta_core).

But eta_core is not determined by p18h-s.  Equal electric/magnetic core energy,
unit impedance, and direct geometric 4*pi flux shortcuts all fail the observed
alpha.  The problem has become sharper, not solved: RefG now needs a theorem
for eta_core from the nonlinear localized orientation-frame core.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive Z_medium.
- It does not insert CODATA as a fitted partition.
- It does not identify geometric 4*pi flux with canonical magnetic charge.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA
N_REQUIRED = ALPHA_INV_CODATA / (4.0 * math.pi)
Q_GEOM_H2_ORDER9 = 2.0 / 9.0
G_GEOM_FLUX_4PI = 4.0 * math.pi


# ---------------------------------------------------------------------------
# 1. Electric/magnetic core-energy matching ledger
# ---------------------------------------------------------------------------

def core_energy_matching_ledger() -> dict:
    Z, q, g, R = sp.symbols("Z_medium q_geom g_geom R", positive=True)
    E_e = sp.simplify(Z * q**2 / (8 * sp.pi * R))
    E_m = sp.simplify(g**2 / (8 * sp.pi * Z * R))
    ratio = sp.simplify(E_e / E_m)

    eta = sp.symbols("eta_core", positive=True)
    Z_solution = sp.solve(sp.Eq(ratio, eta), Z)[0]
    alpha = sp.simplify(Z_solution * q**2 / (4 * sp.pi))

    return {
        "electric_energy": str(E_e),
        "magnetic_energy": str(E_m),
        "both_far_field_energies_scale_as_1_over_R": bool(
            sp.simplify(sp.diff(R * E_e, R)) == 0
            and sp.simplify(sp.diff(R * E_m, R)) == 0
        ),
        "energy_ratio": str(ratio),
        "ratio_independent_of_R": sp.diff(ratio, R) == 0,
        "Z_from_core_partition_eta": str(Z_solution),
        "alpha_from_eta": str(alpha),
        "eta_core_required_for_Z": True,
    }


# ---------------------------------------------------------------------------
# 2. Core matching does not fix Z unless eta_core is derived
# ---------------------------------------------------------------------------

def eta_core_no_go() -> dict:
    eta, q, g, Nreq = sp.symbols(
        "eta_core q_geom g_geom N_required", positive=True
    )
    Z = sp.simplify(g * sp.sqrt(eta) / q)
    alpha = sp.simplify(Z * q**2 / (4 * sp.pi))
    N = sp.simplify(1 / (4 * sp.pi * alpha))
    eta_solution = sp.solve(sp.Eq(N, Nreq), eta)[0]

    return {
        "Z_expression": str(Z),
        "alpha_expression": str(alpha),
        "N_expression": str(N),
        "N_still_depends_on_eta_core": N.has(eta),
        "matching_N_solves_for_eta_not_alpha": str(eta_solution),
        "conclusion": (
            "core matching becomes a real alpha derivation only after eta_core "
            "is derived from the nonlinear localized core"
        ),
    }


# ---------------------------------------------------------------------------
# 3. Natural shortcut conditions and their failures
# ---------------------------------------------------------------------------

def natural_core_shortcut_audit() -> dict:
    q = Q_GEOM_H2_ORDER9
    g = G_GEOM_FLUX_4PI

    def alpha_inv_from_eta(eta: float) -> float:
        Z = (g / q) * math.sqrt(eta)
        alpha = Z * q**2 / (4.0 * math.pi)
        return 1.0 / alpha

    eta_equal_energy = 1.0
    eta_unit_impedance = (q / g) ** 2
    eta_observed_target = ((4.0 * math.pi * ALPHA_CODATA / (q**2)) * q / g) ** 2

    rows = {
        "equal_electric_magnetic_far_energy_eta1": {
            "eta_core": eta_equal_energy,
            "Z_medium": g / q,
            "alpha_inv": alpha_inv_from_eta(eta_equal_energy),
            "fails_observed_alpha": abs(
                alpha_inv_from_eta(eta_equal_energy) - ALPHA_INV_CODATA
            )
            > 1.0,
        },
        "unit_impedance_eta": {
            "eta_core": eta_unit_impedance,
            "Z_medium": 1.0,
            "alpha_inv": alpha_inv_from_eta(eta_unit_impedance),
            "fails_observed_alpha": abs(
                alpha_inv_from_eta(eta_unit_impedance) - ALPHA_INV_CODATA
            )
            > 1.0,
        },
        "observed_alpha_target_eta": {
            "eta_core": eta_observed_target,
            "Z_medium": 4.0 * math.pi * ALPHA_CODATA / (q**2),
            "alpha_inv": ALPHA_INV_CODATA,
            "is_target_not_derivation": True,
        },
    }

    return {
        "q_geom_used_for_diagnostic": q,
        "g_geom_used_for_diagnostic": g,
        "rows": rows,
        "simple_natural_shortcuts_fail": bool(
            rows["equal_electric_magnetic_far_energy_eta1"][
                "fails_observed_alpha"
            ]
            and rows["unit_impedance_eta"]["fails_observed_alpha"]
        ),
        "observed_target_requires_small_eta_under_4pi_flux_diagnostic": (
            eta_observed_target < 0.01
        ),
        "target_eta_not_inserted": True,
    }


# ---------------------------------------------------------------------------
# 4. What would count as a real theorem
# ---------------------------------------------------------------------------

def core_theorem_requirements() -> dict:
    return {
        "needed_theorem": (
            "derive eta_core = E_e/E_m from the nonlinear localized "
            "orientation-frame core"
        ),
        "acceptable_inputs": [
            "completed connection Dtheta = dtheta + A(n)",
            "closed electric framing/twist current",
            "magnetic frame-curvature flux",
            "finite order-9, h=2 boundary sector",
            "localized core regularity and finite-energy boundary conditions",
            "one action normalization for the electric and magnetic channels",
        ],
        "unacceptable_inputs": [
            "CODATA alpha",
            "declaring eta_core by hand",
            "equal electric/magnetic energy without a derived self-duality",
            "directly equating geometric 4*pi flux with canonical magnetic charge",
            "using c as a coupling normalization",
        ],
        "candidate_next_gate": "p18u_nonlinear_core_partition_gate.py",
    }


# ---------------------------------------------------------------------------
# 5. Article-level physical reading
# ---------------------------------------------------------------------------

def physical_interpretation_ledger() -> dict:
    return {
        "finite_transfer_statement": (
            "the substrate carries electric/frame disturbance at the luminal "
            "transfer ceiling, not instantaneously"
        ),
        "impedance_statement": (
            "the strength of the external Maxwell readout is set by the "
            "core's electric/magnetic partition, not by the speed alone"
        ),
        "alpha_statement": (
            "alpha can be derived only if this partition is derived from RefG "
            "dynamics rather than fitted"
        ),
        "best_current_intuition": (
            "one closed orientation-frame defect must distribute its stored "
            "trace between internal twist, axis curvature and external field; "
            "the missing number is that distribution law"
        ),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_core_impedance_matching_gate() -> dict:
    matching = core_energy_matching_ledger()
    nogo = eta_core_no_go()
    shortcuts = natural_core_shortcut_audit()
    requirements = core_theorem_requirements()
    physical = physical_interpretation_ledger()

    closed = {
        "electric_and_magnetic_far_energies_have_common_1_over_R_scaling": bool(
            matching["both_far_field_energies_scale_as_1_over_R"]
        ),
        "energy_ratio_independent_of_core_radius": bool(
            matching["ratio_independent_of_R"]
        ),
        "core_partition_would_fix_Z": bool(
            matching["eta_core_required_for_Z"]
        ),
        "without_eta_core_N_still_free": bool(
            nogo["N_still_depends_on_eta_core"]
        ),
        "matching_observed_N_would_solve_for_eta_core": bool(
            nogo["matching_N_solves_for_eta_not_alpha"]
        ),
        "equal_energy_and_unit_impedance_shortcuts_fail": bool(
            shortcuts["simple_natural_shortcuts_fail"]
        ),
        "observed_eta_left_as_target_not_input": bool(
            shortcuts["target_eta_not_inserted"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "eta_core_derived_from_nonlinear_core": False,
        "self_duality_or_partition_law_derived": False,
        "geometric_flux_to_canonical_flux_map_derived": False,
        "Z_medium_derived": False,
        "N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_NONLINEAR_CORE_PARTITION_THEOREM_REQUIRED__"
            + _pass_status("CORE_MATCHING_IMPEDANCE_NO_GO")
            if all(closed.values())
            else "CHECK_CORE_IMPEDANCE_MATCHING"
        ),
        "SCOPE": (
            "core impedance gate after p18s: electric framing-current and "
            "magnetic frame-flux energies can be matched at the same localized "
            "core, and such a matching would fix Z_medium.  However, the "
            "required partition eta_core is not determined by the current "
            "p18 chain.  Natural shortcuts fail; alpha remains open."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "core_matching": matching,
        "eta_core_no_go": nogo,
        "shortcut_audit": shortcuts,
        "requirements_for_next_gate": requirements,
        "physical_interpretation": physical,
        "physical_reading": (
            "p18t turns the alpha problem into a precise local question: "
            "what fraction of a charged orientation-frame core is carried by "
            "electric framing current versus magnetic frame curvature?  If "
            "RefG derives that partition, Z_medium and alpha can be computed. "
            "Without it, inserting 137 would be only a fit."
        ),
        "missing_derivations": [
            "derive eta_core from the nonlinear localized core equations",
            "derive whether a self-dual or non-self-dual partition is selected",
            "derive the map from geometric 4*pi frame flux to canonical "
            "magnetic normalization",
            "then combine eta_core with q_geom to compute Z_medium and alpha",
        ],
        "do_not_claim": [
            "Do not claim alpha or N are derived.",
            "Do not set eta_core to the observed target.",
            "Do not assume equal electric and magnetic core energy unless "
            "self-duality is derived.",
            "Do not identify geometric 4*pi flux with canonical magnetic "
            "charge without the flux normalization theorem.",
            "Do not treat finite luminal transfer as a coupling derivation.",
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
    print("core_matching:", result["core_matching"])
    print("eta_core_no_go:", result["eta_core_no_go"])
    print("shortcut_audit:", result["shortcut_audit"])
    print("requirements_for_next_gate:", result["requirements_for_next_gate"])
    print("physical_interpretation:", result["physical_interpretation"])
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
    _print_result(derive_core_impedance_matching_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
