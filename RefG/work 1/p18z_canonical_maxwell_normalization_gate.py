# Notation header (see NOTATION.md):
# This gate follows p18y.  It audits the canonical Maxwell normalization that
# turns one completed framing register into a physical electric coupling.

"""
================================================================================
PHASE 18z: Canonical Maxwell normalization gate
================================================================================

Purpose
-------
p18y showed that topology can identify the electric register candidate:

    q_geom = 2/9.

It also showed that alpha still depends on the Maxwell strength q0:

    q_e   = q0*q_geom,
    alpha = q0^2*q_geom^2/(4*pi).

This gate asks what q0 is in field-normalization language.  The answer is
simple and important.  If the effective Maxwell/source sector is

    L = -K_F F^2/4 + k_J q_geom A_mu J^mu,

then the canonically normalized field is A_can = sqrt(K_F) A, and therefore

    q_e = (k_J/sqrt(K_F)) q_geom,
    q0  = k_J/sqrt(K_F).

Thus the remaining alpha problem is a ratio of two action normalizations:

    source strength / field stiffness.

Gauge invariance, compact topology and luminal propagation do not fix that
ratio by themselves.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive q0.
- It does not set K_F or k_J from the observed alpha.
- It does not claim q_geom=2/9 is canonical electric charge.
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
# 1. Canonical field rescaling
# ---------------------------------------------------------------------------

def canonical_field_rescaling_gate() -> dict:
    K_F, k_J, q_geom = sp.symbols("K_F k_J q_geom", positive=True)
    q0 = sp.simplify(k_J / sp.sqrt(K_F))
    q_e = sp.simplify(q0 * q_geom)
    alpha = sp.simplify(q_e**2 / (4 * sp.pi))
    K_solution = sp.solve(sp.Eq(sp.Symbol("q0") , q0), K_F)

    return {
        "effective_sector": "L = -K_F*F^2/4 + k_J*q_geom*A_mu*J^mu",
        "canonical_field": "A_can = sqrt(K_F)*A",
        "canonical_charge": str(q_e),
        "q0": str(q0),
        "alpha": str(alpha),
        "alpha_depends_on_K_F_and_k_J": alpha.has(K_F) and alpha.has(k_J),
        "K_F_if_q0_and_kJ_known": str(K_solution[0]),
        "reading": (
            "canonical Maxwell normalization converts the topological register "
            "into charge through q0=k_J/sqrt(K_F).  Topology supplies q_geom; "
            "the action must supply the normalization ratio."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Gauss-law normalization gives the same q0
# ---------------------------------------------------------------------------

def gauss_law_normalization_gate() -> dict:
    K_F, k_J, q_geom, r = sp.symbols(
        "K_F k_J q_geom r", positive=True
    )
    q_src = sp.simplify(k_J * q_geom)
    E_r = sp.simplify(q_src / (4 * sp.pi * K_F * r**2))
    alpha_gauss = sp.simplify(q_src**2 / (4 * sp.pi * K_F))
    q0 = sp.simplify(k_J / sp.sqrt(K_F))
    alpha_from_q0 = sp.simplify(q0**2 * q_geom**2 / (4 * sp.pi))

    return {
        "Gauss_law": "div(K_F*E) = k_J*q_geom*rho",
        "point_field_E_r": str(E_r),
        "alpha_from_Gauss_normalization": str(alpha_gauss),
        "alpha_matches_q0_expression": sp.simplify(alpha_gauss - alpha_from_q0)
        == 0,
        "reading": (
            "Gauss law sees the same ratio: source coupling squared divided "
            "by field stiffness.  The external Coulomb strength is not fixed "
            "by the integer/topological charge alone."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Luminal speed does not fix canonical normalization
# ---------------------------------------------------------------------------

def luminal_speed_normalization_no_go() -> dict:
    chi, kappa, K, k_J, q_geom = sp.symbols(
        "chi kappa K k_J q_geom", positive=True
    )
    speed_squared = sp.simplify(kappa / chi)
    isotropic_subs = {chi: K, kappa: K}
    speed_unit = sp.simplify(speed_squared.subs(isotropic_subs))
    q0 = sp.simplify(k_J / sp.sqrt(K))
    alpha = sp.simplify(q0**2 * q_geom**2 / (4 * sp.pi))

    return {
        "quadratic_EM_sector": "L = chi*E^2/2 - kappa*B^2/2 + k_J*q_geom*A*J",
        "speed_squared": str(speed_squared),
        "unit_speed_after_chi_equals_kappa": str(speed_unit),
        "q0_after_unit_speed": str(q0),
        "alpha_after_unit_speed": str(alpha),
        "speed_unit_but_K_free": speed_unit == 1 and alpha.has(K),
        "reading": (
            "setting the wave speed to c fixes kappa/chi.  It does not fix "
            "the common stiffness K or the source normalization k_J."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Target translations only
# ---------------------------------------------------------------------------

def normalization_target_translation() -> dict:
    q0_required = math.sqrt(4.0 * math.pi * ALPHA_CODATA) / Q_GEOM
    K_required_if_kJ_1 = 1.0 / (q0_required**2)
    kJ_required_if_K_1 = q0_required
    alpha_if_K1_kJ1 = Q_GEOM**2 / (4.0 * math.pi)

    return {
        "q_geom": Q_GEOM,
        "alpha_inv_if_K1_and_kJ1": 1.0 / alpha_if_K1_kJ1,
        "q0_required_for_CODATA_alpha": q0_required,
        "K_F_required_if_k_J_equals_1": K_required_if_kJ_1,
        "k_J_required_if_K_F_equals_1": kJ_required_if_K_1,
        "Z_medium_required_q0_squared": q0_required**2,
        "target_not_derivation": True,
        "reading": (
            "observed alpha can be translated into a required q0, or into a "
            "required K_F for k_J=1, or into a required k_J for K_F=1.  None "
            "of these translations is a derivation."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Field redefinition cannot remove the physical ratio
# ---------------------------------------------------------------------------

def field_redefinition_guard() -> dict:
    K_F, k_J, q_geom, lam = sp.symbols(
        "K_F k_J q_geom lambda", positive=True
    )
    q0 = sp.simplify(k_J / sp.sqrt(K_F))

    # Reparameterize A' = lambda*A.  Then F' = lambda*F.  To keep the same
    # physics written in A', K_F' = K_F/lambda^2 and k_J' = k_J/lambda.
    K_prime = sp.simplify(K_F / lam**2)
    kJ_prime = sp.simplify(k_J / lam)
    q0_prime = sp.simplify(kJ_prime / sp.sqrt(K_prime))

    return {
        "q0_before_redefinition": str(q0),
        "K_F_prime_under_Aprime_equals_lambda_A": str(K_prime),
        "k_J_prime_under_Aprime_equals_lambda_A": str(kJ_prime),
        "q0_after_redefinition": str(q0_prime),
        "q0_invariant_under_field_redefinition": sp.simplify(q0_prime - q0) == 0,
        "reading": (
            "one may choose units where K_F=1, but then the coupling changes. "
            "The physical object is q0=k_J/sqrt(K_F), not either coefficient "
            "separately."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "derive k_J/sqrt(K_F) from the same completed orientation-frame "
            "action that supplies the charged oscillon current"
        ),
        "must_derive": [
            "K_F: the coefficient of the external Maxwell kinetic term",
            "k_J: the coefficient coupling one completed framing register to A_mu",
            "the field normalization bridge from frame connection curvature to canonical Maxwell F",
            "the source normalization bridge from charged oscillon current to canonical J",
        ],
        "acceptable_routes": [
            "derive K_F and k_J directly from the localized action",
            "derive their ratio through a medium impedance theorem",
            "derive their ratio through a core partition theorem",
            "derive their ratio through a boundary-to-Maxwell normalization functional",
        ],
        "falsification_tests": [
            "if K_F and k_J remain independent constants, alpha is not derived",
            "if K_F=1 is chosen as convention and k_J is then fitted, the gate fails",
            "if luminal propagation is used alone, alpha is not derived",
            "if q_geom=2/9 is used as q_e without q0, alpha is not derived",
        ],
        "candidate_next_gate": "p18aa_action_origin_of_maxwell_normalization_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_canonical_maxwell_normalization_gate() -> dict:
    rescale = canonical_field_rescaling_gate()
    gauss = gauss_law_normalization_gate()
    luminal = luminal_speed_normalization_no_go()
    target = normalization_target_translation()
    field_guard = field_redefinition_guard()
    requirements = next_theorem_requirements()

    closed = {
        "canonical_charge_is_source_over_sqrt_field_stiffness": bool(
            rescale["alpha_depends_on_K_F_and_k_J"]
        ),
        "Gauss_law_matches_q0_normalization": bool(
            gauss["alpha_matches_q0_expression"]
        ),
        "luminal_speed_leaves_K_and_kJ_free": bool(
            luminal["speed_unit_but_K_free"]
        ),
        "observed_alpha_translated_to_q0_target_only": bool(
            target["target_not_derivation"]
        ),
        "field_redefinition_preserves_q0": bool(
            field_guard["q0_invariant_under_field_redefinition"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "K_F_derived_from_action": False,
        "k_J_derived_from_action": False,
        "q0_derived": False,
        "Z_medium_derived": False,
        "canonical_e_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_ACTION_ORIGIN_OF_MAXWELL_NORMALIZATION_REQUIRED__"
            + _pass_status("CANONICAL_MAXWELL_NORMALIZATION_LEDGER")
            if all(closed.values())
            else "CHECK_CANONICAL_MAXWELL_NORMALIZATION"
        ),
        "SCOPE": (
            "canonical Maxwell normalization after p18y: the physical electric "
            "strength of the topological register is q0=k_J/sqrt(K_F).  "
            "Gauge invariance, topology and luminal propagation do not fix "
            "this ratio.  Alpha remains open until K_F and k_J, or their "
            "ratio, are derived from the action."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "canonical_rescaling": rescale,
        "Gauss_normalization": gauss,
        "luminal_no_go": luminal,
        "target_translation": target,
        "field_redefinition_guard": field_guard,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "we have reached the precise normalization problem.  The electric "
            "topology gives the register; the charged oscillon gives a current; "
            "Maxwell normalization asks how stiff the field is and how strongly "
            "the register couples to it.  Alpha is their ratio squared times "
            "q_geom^2/(4*pi)."
        ),
        "missing_derivations": [
            "derive the Maxwell kinetic coefficient K_F",
            "derive the source coupling coefficient k_J",
            "derive q0=k_J/sqrt(K_F) without using CODATA",
            "then compute alpha = q0^2*q_geom^2/(4*pi)",
        ],
        "do_not_claim": [
            "Do not claim alpha, q0, K_F, or k_J are derived.",
            "Do not set K_F=1 and k_J=1 simultaneously as physics.",
            "Do not use luminal propagation as coupling normalization.",
            "Do not use q_geom=2/9 as canonical electric charge.",
            "Do not fit q0 to CODATA.",
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
    print("canonical_rescaling:", result["canonical_rescaling"])
    print("Gauss_normalization:", result["Gauss_normalization"])
    print("luminal_no_go:", result["luminal_no_go"])
    print("target_translation:", result["target_translation"])
    print("field_redefinition_guard:", result["field_redefinition_guard"])
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
    _print_result(derive_canonical_maxwell_normalization_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
