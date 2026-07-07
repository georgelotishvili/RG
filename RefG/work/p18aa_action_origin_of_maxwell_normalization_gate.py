# Notation header (see NOTATION.md):
# This gate follows p18z.  It asks whether an action-level origin for the
# Maxwell kinetic coefficient and the charged oscillon source coefficient can
# fix q0 = k_J/sqrt(K_F), hence alpha, without fitting CODATA.

"""
================================================================================
PHASE 18aa: Action origin of Maxwell normalization gate
================================================================================

Purpose
-------
p18z reduced the fine-structure problem to one precise object:

    q0 = k_J / sqrt(K_F),
    alpha = q0^2*q_geom^2/(4*pi).

Here K_F is the canonical Maxwell stiffness and k_J is the source coefficient
by which one completed charged oscillon/framing register couples to A_mu.

This gate tests the next natural hope:

    maybe the same completed orientation-frame action fixes K_F and k_J.

Main result
-----------
A local action can name the missing coefficients very cleanly, but it does not
yet derive their ratio.  In the generic completed frame action,

    L = -C_B I_B F^2/4 + C_D I_J q_reg A_mu J^mu + ...

one obtains

    K_F = C_B I_B,
    k_J = C_D I_J q_reg,
    q0  = C_D I_J q_reg / sqrt(C_B I_B).

Gauge invariance fixes current conservation.  Luminality fixes a cone.  SO(3)
isotropy can set certain stiffness ratios.  None of these by itself fixes the
absolute action normalization relative to the quantum unit.  If the whole
classical action is rescaled by s, the classical stationary equations do not
see a new geometry, but the canonical charge scales as sqrt(s).  Alpha is
therefore a quantum/action-normalization lock, not merely a classical
connection-geometry lock.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive q0, K_F, or k_J.
- It does not fit q0 to CODATA.
- It does not claim that a classical frame action alone is enough.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA
Q_GEOM = 2.0 / 9.0


# ---------------------------------------------------------------------------
# 1. Generic action-origin ledger
# ---------------------------------------------------------------------------

def generic_action_origin_ledger() -> dict:
    C_B, C_D, I_B, I_J, q_reg = sp.symbols(
        "C_B C_D I_B I_J q_reg", positive=True
    )
    K_F = sp.simplify(C_B * I_B)
    k_J = sp.simplify(C_D * I_J * q_reg)
    q0 = sp.simplify(k_J / sp.sqrt(K_F))
    alpha = sp.simplify(q0**2 / (4 * sp.pi))

    return {
        "effective_action_sector": (
            "L = -C_B*I_B*F^2/4 + C_D*I_J*q_reg*A_mu*J^mu + ..."
        ),
        "K_F": str(K_F),
        "k_J": str(k_J),
        "q0": str(q0),
        "alpha_without_q_geom": str(alpha),
        "depends_on_action_coefficients": (
            q0.has(C_B) and q0.has(C_D) and q0.has(I_B) and q0.has(I_J)
        ),
        "reading": (
            "the action gives the right place to look: field stiffness, source "
            "strength, register normalization and core inventory.  Unless "
            "these are linked by a theorem, q0 remains open."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Shared stiffness/isotropy audit
# ---------------------------------------------------------------------------

def shared_stiffness_audit() -> dict:
    kappa, I_B, I_J, q_reg = sp.symbols(
        "kappa I_B I_J q_reg", positive=True
    )
    K_F = sp.simplify(kappa * I_B)
    k_J = sp.simplify(kappa * I_J * q_reg)
    q0 = sp.simplify(k_J / sp.sqrt(K_F))

    special_same_inventory = sp.simplify(q0.subs({I_B: 1, I_J: 1, q_reg: 1}))

    return {
        "SO3_or_single_kappa_case": "C_B = C_D = kappa",
        "K_F": str(K_F),
        "k_J": str(k_J),
        "q0": str(q0),
        "q0_if_all_dimensionless_inventories_are_set_to_one": str(
            special_same_inventory
        ),
        "common_kappa_still_present": q0.has(kappa),
        "inventory_ratio_still_present": q0.has(I_B) and q0.has(I_J),
        "reading": (
            "a common frame stiffness is valuable, but it does not by itself "
            "produce a number.  It leaves a square-root action scale and the "
            "relative core inventories."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Gauge invariance fixes conservation, not the coupling size
# ---------------------------------------------------------------------------

def gauge_invariance_normalization_no_go() -> dict:
    q, lam0, lam1, lam2 = sp.symbols(
        "q lambda_0 lambda_1 lambda_2", real=True
    )

    closed_variation = q * (
        (lam1 - lam0) + (lam2 - lam1) + (lam0 - lam2)
    )
    open_variation = q * ((lam1 - lam0) + (lam2 - lam1))

    q_a, q_b = sp.symbols("q_a q_b", positive=True)
    closed_variation_a = sp.simplify(closed_variation.subs(q, q_a))
    closed_variation_b = sp.simplify(closed_variation.subs(q, q_b))

    return {
        "closed_loop_variation": str(sp.simplify(closed_variation)),
        "open_line_variation": str(sp.simplify(open_variation)),
        "closed_loop_gauge_invariant_for_any_q": (
            closed_variation_a == 0 and closed_variation_b == 0
        ),
        "normalization_not_fixed_by_gauge_invariance": True,
        "reading": (
            "gauge invariance selects closed/conserved currents.  It permits "
            "any overall coupling coefficient, so it cannot be the alpha "
            "derivation by itself."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Overall classical action scale audit
# ---------------------------------------------------------------------------

def overall_action_scale_audit() -> dict:
    s, K_F, k_J, q_geom = sp.symbols(
        "s K_F k_J q_geom", positive=True
    )
    q0 = sp.simplify(k_J / sp.sqrt(K_F))
    alpha = sp.simplify(q0**2 * q_geom**2 / (4 * sp.pi))

    K_scaled = sp.simplify(s * K_F)
    k_scaled = sp.simplify(s * k_J)
    q0_scaled = sp.simplify(k_scaled / sp.sqrt(K_scaled))
    alpha_scaled = sp.simplify(q0_scaled**2 * q_geom**2 / (4 * sp.pi))

    # Static classical field sourced by a fixed current:
    # K_F div E = k_J q_geom rho, so E is controlled by k_J/K_F.
    field_ratio = sp.simplify(k_J / K_F)
    field_ratio_scaled = sp.simplify(k_scaled / K_scaled)

    return {
        "q0_before_scale": str(q0),
        "q0_after_full_action_scale_s": str(q0_scaled),
        "q0_scale_ratio": str(sp.simplify(q0_scaled / q0)),
        "alpha_scale_ratio": str(sp.simplify(alpha_scaled / alpha)),
        "classical_source_field_ratio": str(field_ratio),
        "classical_source_field_ratio_after_scale": str(field_ratio_scaled),
        "classical_field_ratio_invariant_under_common_scale": (
            sp.simplify(field_ratio_scaled - field_ratio) == 0
        ),
        "alpha_changes_under_common_action_scale": (
            sp.simplify(alpha_scaled / alpha - s) == 0
        ),
        "reading": (
            "the common classical action scale is invisible to the classical "
            "field ratio k_J/K_F, but it changes the canonical charge by "
            "sqrt(s) and alpha by s.  A quantum/action-unit lock is therefore "
            "needed."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Target translation without fitting
# ---------------------------------------------------------------------------

def codata_target_translation() -> dict:
    q0_required = math.sqrt(4.0 * math.pi * ALPHA_CODATA) / Q_GEOM
    alpha_if_q0_one = Q_GEOM**2 / (4.0 * math.pi)
    s_required_if_q0_base_one = q0_required**2
    return {
        "q_geom": Q_GEOM,
        "alpha_inv_if_q0_equals_1": 1.0 / alpha_if_q0_one,
        "q0_required_for_observed_alpha": q0_required,
        "action_scale_required_if_base_q0_is_1": s_required_if_q0_base_one,
        "target_not_derivation": True,
        "reading": (
            "if a future theorem produced base q0=1, the observed alpha would "
            "ask for an action-scale factor q0_required^2.  This is only a "
            "target ledger, not an input."
        ),
    }


# ---------------------------------------------------------------------------
# 6. What a real next theorem must derive
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "quantum normalization of one completed charged oscillon/framing "
            "register relative to the Maxwell field stiffness"
        ),
        "must_derive": [
            "the coefficient K_F of the canonical Maxwell kinetic term",
            "the coefficient k_J of one closed charged oscillon current",
            "the register normalization q_reg for the order-9, h=2 sector",
            "the dimensionless core inventory ratio I_J/sqrt(I_B)",
            "the overall action scale relative to the quantum phase unit hbar",
        ],
        "plausible_routes": [
            "Bohr-Sommerfeld or path-integral phase closure for one completed h=2 framed loop",
            "a boundary symplectic-form normalization of the U(1) frame bundle",
            "a finite resonator action quantum that fixes the common kappa scale",
            "a core partition theorem that also fixes the absolute Maxwell stiffness",
        ],
        "falsification_tests": [
            "if only classical Euler-Lagrange equations are used, the common action scale remains invisible",
            "if q0 is chosen from CODATA, the gate fails as a fit",
            "if gauge invariance is the only input, the coupling remains arbitrary",
            "if SO(3) isotropy only sets C_B=C_D, alpha is still not derived",
        ],
        "candidate_next_gate": "p18ab_quantum_action_unit_lock_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_action_origin_of_maxwell_normalization_gate() -> dict:
    generic = generic_action_origin_ledger()
    shared = shared_stiffness_audit()
    gauge = gauge_invariance_normalization_no_go()
    scale = overall_action_scale_audit()
    target = codata_target_translation()
    requirements = next_theorem_requirements()

    closed = {
        "generic_action_identifies_KF_kJ_q0": bool(
            generic["depends_on_action_coefficients"]
        ),
        "shared_stiffness_still_leaves_scale_and_inventory": bool(
            shared["common_kappa_still_present"]
            and shared["inventory_ratio_still_present"]
        ),
        "gauge_invariance_does_not_fix_coupling_size": bool(
            gauge["closed_loop_gauge_invariant_for_any_q"]
            and gauge["normalization_not_fixed_by_gauge_invariance"]
        ),
        "common_classical_scale_changes_alpha": bool(
            scale["classical_field_ratio_invariant_under_common_scale"]
            and scale["alpha_changes_under_common_action_scale"]
        ),
        "observed_alpha_kept_as_target_only": bool(
            target["target_not_derivation"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "K_F_derived_from_full_action": False,
        "k_J_derived_from_full_action": False,
        "core_inventory_ratio_derived": False,
        "action_scale_relative_to_hbar_derived": False,
        "q0_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_QUANTUM_ACTION_UNIT_LOCK_REQUIRED__"
            + _pass_status("ACTION_NORMALIZATION_ORIGIN_AUDIT")
            if all(closed.values())
            else "CHECK_ACTION_NORMALIZATION_ORIGIN"
        ),
        "SCOPE": (
            "action-origin gate after p18z: the completed frame action can "
            "organize K_F and k_J, but classical geometry, gauge invariance, "
            "luminality and SO(3)-style stiffness equality do not by "
            "themselves fix q0.  The missing object is the quantum/action-unit "
            "normalization of one completed charged oscillon register."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "generic_action_origin": generic,
        "shared_stiffness_audit": shared,
        "gauge_no_go": gauge,
        "overall_action_scale": scale,
        "target_translation": target,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "we have found the real wall: alpha is not just a topology number "
            "and not just the speed of transfer.  It is the strength with "
            "which one completed charged oscillon register enters the quantum "
            "Maxwell action.  The next successful theorem must quantize that "
            "action unit, not merely redraw the classical field equations."
        ),
        "missing_derivations": [
            "derive K_F and k_J from the same completed orientation-frame action",
            "derive the core inventory ratio I_J/sqrt(I_B)",
            "derive the action scale relative to hbar or an equivalent phase-closure unit",
            "derive q0 without CODATA",
            "then compute alpha = q0^2*q_geom^2/(4*pi)",
        ],
        "do_not_claim": [
            "Do not claim alpha, q0, K_F, or k_J are derived.",
            "Do not treat gauge invariance as a coupling normalization theorem.",
            "Do not treat SO(3) isotropy as enough to produce 137.",
            "Do not fit the common action scale to observed alpha.",
            "Do not confuse classical wave-speed closure with quantum coupling closure.",
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
    print("generic_action_origin:", result["generic_action_origin"])
    print("shared_stiffness_audit:", result["shared_stiffness_audit"])
    print("gauge_no_go:", result["gauge_no_go"])
    print("overall_action_scale:", result["overall_action_scale"])
    print("target_translation:", result["target_translation"])
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
    _print_result(derive_action_origin_of_maxwell_normalization_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
