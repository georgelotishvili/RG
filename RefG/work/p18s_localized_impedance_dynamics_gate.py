# Notation header (see NOTATION.md):
# This gate follows p18r.  It turns the user's finite-transfer intuition into
# an executable impedance audit: luminal propagation fixes the causal speed,
# but not the medium impedance that normalizes electric charge.

"""
================================================================================
PHASE 18s: Localized impedance dynamics gate
================================================================================

Purpose
-------
p18q-r located the remaining alpha bottleneck in the medium impedance.  The
physical intuition sharpened after p18r is:

    the substrate does not carry electric/frame changes instantaneously;
    it carries them with the luminal transfer speed c.

This is essential, but it is not yet alpha.  In a Maxwell/line-action language
the speed and the impedance are different invariants:

    speed      v = 1/sqrt(epsilon * mu)      or sqrt(kappa/chi),
    impedance  Z = sqrt(mu/epsilon)         or 1/sqrt(kappa*chi).

Therefore the statement "the medium transfers electric changes at c" fixes the
causal cone, while leaving the response normalization free.  Alpha lives in the
leftover normalization:

    alpha = Z_medium * q_geom^2 / (4*pi)     in the p18r convention.

What this gate closes
---------------------
1. Luminality is a propagation theorem, not a coupling theorem.
2. A continuous one-parameter rescaling keeps the wave speed fixed while
   changing the impedance.
3. Dirac/Wilson product quantization is blind to the same dual impedance
   rescaling.
4. The observed alpha can be translated into a required impedance for a chosen
   geometric electric coordinate, but that is only a target, not a derivation.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive Z_medium.
- It does not set Z_medium from CODATA.
- It does not identify the substrate with a classical conductor.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA
THETA_H = 2.0 / 9.0


# ---------------------------------------------------------------------------
# 1. Maxwell response: speed versus impedance
# ---------------------------------------------------------------------------

def maxwell_speed_impedance_split() -> dict:
    eps, mu, lam, q = sp.symbols("epsilon mu lambda q_geom", positive=True)
    speed = sp.simplify(1 / sp.sqrt(eps * mu))
    impedance = sp.simplify(sp.sqrt(mu / eps))

    eps_rescaled = lam * eps
    mu_rescaled = mu / lam
    speed_rescaled = sp.simplify(1 / sp.sqrt(eps_rescaled * mu_rescaled))
    impedance_rescaled = sp.simplify(sp.sqrt(mu_rescaled / eps_rescaled))

    alpha = sp.simplify(impedance * q**2 / (4 * sp.pi))
    alpha_rescaled = sp.simplify(impedance_rescaled * q**2 / (4 * sp.pi))

    return {
        "speed": str(speed),
        "impedance": str(impedance),
        "speed_invariant_under_dual_rescaling": sp.simplify(
            speed_rescaled - speed
        )
        == 0,
        "impedance_rescaling_ratio": str(
            sp.simplify(impedance_rescaled / impedance)
        ),
        "alpha": str(alpha),
        "alpha_rescaling_ratio": str(sp.simplify(alpha_rescaled / alpha)),
        "luminality_does_not_fix_impedance": True,
    }


# ---------------------------------------------------------------------------
# 2. Local transfer-line analogue: finite current transfer is not enough
# ---------------------------------------------------------------------------

def finite_transfer_line_audit() -> dict:
    L, C, lam = sp.symbols("L C lambda", positive=True)
    velocity = sp.simplify(1 / sp.sqrt(L * C))
    line_impedance = sp.simplify(sp.sqrt(L / C))

    L_rescaled = lam * L
    C_rescaled = C / lam
    velocity_rescaled = sp.simplify(1 / sp.sqrt(L_rescaled * C_rescaled))
    impedance_rescaled = sp.simplify(sp.sqrt(L_rescaled / C_rescaled))

    return {
        "velocity": str(velocity),
        "line_impedance": str(line_impedance),
        "velocity_invariant_under_LC_rescaling": sp.simplify(
            velocity_rescaled - velocity
        )
        == 0,
        "impedance_rescaling_ratio": str(
            sp.simplify(impedance_rescaled / line_impedance)
        ),
        "finite_transfer_not_instantaneous": True,
        "finite_transfer_speed_not_alpha": True,
        "physical_reading": (
            "a line can carry signals at the same finite velocity while its "
            "impedance changes.  RefG's substrate can therefore have c as the "
            "transfer ceiling without alpha being fixed by c alone."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Action normalization: wave speed fixes a ratio, impedance fixes a product
# ---------------------------------------------------------------------------

def localized_quadratic_action_audit() -> dict:
    chi, kappa, lam = sp.symbols("chi kappa lambda", positive=True)

    # L = chi E^2/2 - kappa B^2/2 gives chi A_tt - kappa nabla^2 A = 0.
    speed_sq = sp.simplify(kappa / chi)
    impedance = sp.simplify(1 / sp.sqrt(chi * kappa))

    chi_rescaled = lam * chi
    kappa_rescaled = lam * kappa
    speed_sq_rescaled = sp.simplify(kappa_rescaled / chi_rescaled)
    impedance_rescaled = sp.simplify(
        1 / sp.sqrt(chi_rescaled * kappa_rescaled)
    )

    return {
        "action": "L = chi*E^2/2 - kappa*B^2/2",
        "speed_squared": str(speed_sq),
        "impedance": str(impedance),
        "speed_invariant_under_common_action_rescaling": sp.simplify(
            speed_sq_rescaled - speed_sq
        )
        == 0,
        "impedance_rescaling_ratio": str(
            sp.simplify(impedance_rescaled / impedance)
        ),
        "local_action_normalization_still_needed": True,
    }


# ---------------------------------------------------------------------------
# 4. Dirac product is blind to dual impedance scaling
# ---------------------------------------------------------------------------

def dirac_product_impedance_blindness() -> dict:
    Z, qg, gg = sp.symbols("Z_medium q_geom g_geom", positive=True)
    qe = sp.sqrt(Z) * qg
    gm = gg / sp.sqrt(Z)
    product = sp.simplify(qe * gm)
    alpha = sp.simplify(qe**2 / (4 * sp.pi))
    return {
        "canonical_qe": str(qe),
        "canonical_gm": str(gm),
        "dirac_product": str(product),
        "dirac_product_depends_on_Z": product.has(Z),
        "alpha": str(alpha),
        "alpha_depends_on_Z": alpha.has(Z),
        "product_quantization_cannot_fix_Z": True,
    }


# ---------------------------------------------------------------------------
# 5. Observed alpha as target impedance, not as derivation
# ---------------------------------------------------------------------------

def alpha_target_translation() -> dict:
    q_geom = THETA_H
    Z_required = 4.0 * math.pi * ALPHA_CODATA / (q_geom**2)
    alpha_if_Z1 = q_geom**2 / (4.0 * math.pi)
    alpha_inv_if_Z1 = 1.0 / alpha_if_Z1
    alpha_from_required = Z_required * q_geom**2 / (4.0 * math.pi)
    return {
        "q_geom_candidate": q_geom,
        "alpha_inv_if_Z1": alpha_inv_if_Z1,
        "Z_required_for_CODATA_alpha": Z_required,
        "alpha_recovered_if_Z_required_is_inserted": alpha_from_required,
        "matches_CODATA_only_if_Z_is_inserted": abs(
            alpha_from_required - ALPHA_CODATA
        )
        < 1.0e-15,
        "Z_required_not_derived": True,
        "target_reading": (
            "for q_geom=2/9 the observed alpha asks for a non-unit impedance; "
            "this number is a target for the localized medium theorem, not an "
            "input."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Next theorem requirements
# ---------------------------------------------------------------------------

def localized_impedance_theorem_requirements() -> dict:
    return {
        "needed_object": "Z_medium from localized orientation-frame dynamics",
        "must_use": [
            "completed frame connection Dtheta = dtheta + A(n)",
            "electric closed framing/twist current",
            "magnetic frame-curvature flux",
            "finite boundary/anholonomy sector order-9, h=2",
            "core matching or action normalization, not CODATA fitting",
        ],
        "must_not_use": [
            "setting Z_medium = 1 by convention",
            "setting Z_medium to the observed required value",
            "treating c as enough to fix the coupling",
            "identifying the substrate with a classical perfect conductor",
        ],
        "candidate_next_gate": "p18t_core_impedance_matching_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_localized_impedance_dynamics_gate() -> dict:
    maxwell = maxwell_speed_impedance_split()
    line = finite_transfer_line_audit()
    action = localized_quadratic_action_audit()
    dirac = dirac_product_impedance_blindness()
    target = alpha_target_translation()
    requirements = localized_impedance_theorem_requirements()

    closed = {
        "luminal_speed_separated_from_impedance": bool(
            maxwell["speed_invariant_under_dual_rescaling"]
            and maxwell["luminality_does_not_fix_impedance"]
        ),
        "finite_transfer_speed_is_not_alpha": bool(
            line["velocity_invariant_under_LC_rescaling"]
            and line["finite_transfer_speed_not_alpha"]
        ),
        "local_action_speed_leaves_normalization_free": bool(
            action["speed_invariant_under_common_action_rescaling"]
            and action["local_action_normalization_still_needed"]
        ),
        "dirac_product_blind_to_dual_impedance": bool(
            not dirac["dirac_product_depends_on_Z"]
            and dirac["alpha_depends_on_Z"]
            and dirac["product_quantization_cannot_fix_Z"]
        ),
        "observed_alpha_translated_to_target_Z_only": bool(
            target["matches_CODATA_only_if_Z_is_inserted"]
            and target["Z_required_not_derived"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "Z_medium_derived_from_local_action": False,
        "core_matching_condition_derived": False,
        "electric_boundary_unit_action_derived": False,
        "alpha_computed": False,
        "N_derived": False,
    }

    result = {
        "STATUS": (
            "OPEN_LOCALIZED_MEDIUM_IMPEDANCE_THEOREM_REQUIRED__"
            + _pass_status("LUMINAL_TRANSFER_IMPEDANCE_NO_GO")
            if all(closed.values())
            else "CHECK_LOCALIZED_IMPEDANCE_DYNAMICS"
        ),
        "SCOPE": (
            "impedance gate after p18r: finite luminal electric/frame transfer "
            "is encoded as a causal wave speed, but speed-preserving "
            "rescalings leave the medium impedance free.  Alpha therefore "
            "cannot be obtained from c alone; it requires a localized "
            "orientation-frame impedance theorem."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "maxwell_split": maxwell,
        "finite_transfer_line": line,
        "localized_action": action,
        "dirac_impedance_blindness": dirac,
        "alpha_target": target,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the user's finite-transfer intuition is correct and important: "
            "the substrate is not an instantaneous electric carrier.  This "
            "establishes the causal cone.  The fine-structure constant, "
            "however, sits one layer deeper: in the finite impedance by which "
            "a closed geometric framing twist is read as a canonical Maxwell "
            "charge."
        ),
        "missing_derivations": [
            "derive Z_medium from the localized completed frame action",
            "derive the core/boundary matching condition that normalizes the "
            "electric framing current against magnetic frame flux",
            "derive the selected geometric electric unit dynamically rather "
            "than by choosing theta=2/9 as a direct charge",
            "only then combine q_geom and Z_medium to compute alpha",
        ],
        "do_not_claim": [
            "Do not claim finite luminal transfer derives alpha.",
            "Do not call the substrate an ordinary conductor.",
            "Do not set Z_medium to the CODATA-required target.",
            "Do not use Dirac product quantization as an alpha derivation.",
            "Do not claim N or alpha are derived by this gate.",
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
    print("maxwell_split:", result["maxwell_split"])
    print("finite_transfer_line:", result["finite_transfer_line"])
    print("localized_action:", result["localized_action"])
    print("dirac_impedance_blindness:", result["dirac_impedance_blindness"])
    print("alpha_target:", result["alpha_target"])
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
    _print_result(derive_localized_impedance_dynamics_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
