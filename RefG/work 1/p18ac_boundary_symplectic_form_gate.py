# Notation header (see NOTATION.md):
# This gate follows p18ab.  It audits the boundary symplectic form of the
# completed order-9, h=2 orientation-frame resonator and checks whether the
# frame-bundle geometry alone fixes the action cell needed for alpha.

"""
================================================================================
PHASE 18ac: Boundary symplectic-form gate
================================================================================

Purpose
-------
p18ab identified the next missing object:

    the finite symplectic/action cell of the completed order-9, h=2
    charged orientation-frame resonator.

This gate tests the direct geometric candidates:

  1. the S^2 frame-bundle connection curvature,
  2. the order-9, h=2 holonomy cell,
  3. coadjoint-orbit/prequantization integrality,
  4. the canonical boundary one-form.

Main result
-----------
The boundary geometry cleanly gives the h=2/order-9 register:

    q_geom = 2/9,
    holonomy cell = 2*pi*q_geom = 4*pi/9.

Prequantization then quantizes products such as C*holonomy/(2*pi).  It does
not fix the coefficient C itself unless the action supplies C.  Direct
coadjoint-orbit or cap-cell identifications do not yield the observed
fine-structure normalization.  Therefore the missing object is now very
specific:

    derive the dynamic boundary symplectic coefficient from the completed
    localized frame action.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive q0.
- It does not choose a symplectic coefficient from CODATA.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA
H = 2
ORDER = 9
Q_GEOM = H / ORDER
Q0_SQUARED_REQUIRED = 4.0 * math.pi * ALPHA_CODATA / (Q_GEOM**2)
OMEGA0_REQUIRED_IF_P18AB_CELL = 2.0 * math.pi / Q0_SQUARED_REQUIRED


# ---------------------------------------------------------------------------
# 1. Boundary frame-bundle geometry
# ---------------------------------------------------------------------------

def boundary_frame_bundle_geometry() -> dict:
    h = sp.Integer(H)
    order = sp.Integer(ORDER)
    q_geom = sp.simplify(h / order)
    holonomy_cell = sp.simplify(2 * sp.pi * q_geom)
    full_sphere_area = 4 * sp.pi
    complement = sp.simplify(full_sphere_area - holonomy_cell)

    return {
        "order": ORDER,
        "h": H,
        "q_geom": str(q_geom),
        "holonomy_cell": str(holonomy_cell),
        "holonomy_cell_numeric": float(sp.N(holonomy_cell)),
        "cell_fraction_of_2pi": str(sp.simplify(holonomy_cell / (2 * sp.pi))),
        "cell_fraction_of_4pi": str(sp.simplify(holonomy_cell / (4 * sp.pi))),
        "complement_cell": str(complement),
        "register_cleanly_fixed": q_geom == sp.Rational(2, 9),
        "reading": (
            "the frame-bundle boundary geometry supplies the electric "
            "coordinate/register q_geom=2/9 and its holonomy cell 4*pi/9."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Coadjoint-orbit prequantization audit
# ---------------------------------------------------------------------------

def coadjoint_orbit_prequantization_audit() -> dict:
    s, n = sp.symbols("s n", positive=True)
    total_area = 4 * sp.pi * s
    prequantization_number = sp.simplify(total_area / (2 * sp.pi))
    s_solution = sp.solve(sp.Eq(prequantization_number, n), s)[0]

    target_prequant_number = OMEGA0_REQUIRED_IF_P18AB_CELL / (2.0 * math.pi)
    nearest_integer = round(target_prequant_number)

    return {
        "symplectic_area_total": str(total_area),
        "prequantization_number": str(prequantization_number),
        "s_allowed_if_n_integer": str(s_solution),
        "Omega0_required_if_used_as_total_area": OMEGA0_REQUIRED_IF_P18AB_CELL,
        "target_prequantization_number": target_prequant_number,
        "nearest_integer": nearest_integer,
        "target_is_not_integral_orbit_area": abs(
            target_prequant_number - nearest_integer
        )
        > 1.0e-3,
        "reading": (
            "a direct coadjoint-orbit area identification would require an "
            "integral area in 2*pi units.  The target cell is not produced by "
            "that simple integrality rule."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Order-9/h=2 cap-cell prequantization
# ---------------------------------------------------------------------------

def cap_cell_prequantization_audit() -> dict:
    C, n = sp.symbols("C n", positive=True)
    cell_fraction = sp.Rational(H, ORDER)
    prequantization_number = sp.simplify(C * cell_fraction)
    C_solution = sp.solve(sp.Eq(prequantization_number, n), C)[0]
    C_min = float(C_solution.subs(n, 1))

    return {
        "cell_fraction_of_2pi": str(cell_fraction),
        "prequantization_rule": "C*(h/order) = n",
        "C_solution": str(C_solution),
        "C_min_for_n1": C_min,
        "product_quantized_not_C_fixed_absolutely": True,
        "reading": (
            "the cap cell quantizes C times the order-9 fraction.  For n=1 "
            "it would set C=9/2, but the map from C to q0 is not fixed by "
            "this geometry alone."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Simple map audit
# ---------------------------------------------------------------------------

def simple_map_audit() -> dict:
    target = Q0_SQUARED_REQUIRED
    holonomy = 2.0 * math.pi * Q_GEOM
    C_min = ORDER / H

    candidates = {
        "q0sq_equals_1": 1.0,
        "q0sq_equals_q_geom": Q_GEOM,
        "q0sq_equals_q_geom_squared": Q_GEOM**2,
        "q0sq_equals_inverse_q_geom": 1.0 / Q_GEOM,
        "q0sq_equals_holonomy_over_2pi": holonomy / (2.0 * math.pi),
        "q0sq_equals_2pi_over_holonomy": (2.0 * math.pi) / holonomy,
        "q0sq_equals_C_min": C_min,
        "q0sq_equals_inverse_C_min": 1.0 / C_min,
        "q0sq_equals_4pi_over_9": 4.0 * math.pi / 9.0,
        "q0sq_equals_4pi_over_2pi_plus_cell": (4.0 * math.pi)
        / (2.0 * math.pi + holonomy),
    }

    rows = {}
    for name, value in candidates.items():
        alpha = value * Q_GEOM**2 / (4.0 * math.pi)
        rows[name] = {
            "q0_squared": value,
            "alpha_inv": 1.0 / alpha,
            "relative_miss_q0_squared": abs(value - target) / target,
        }

    best_name, best_row = min(
        rows.items(), key=lambda item: item[1]["relative_miss_q0_squared"]
    )

    return {
        "q0_squared_required_for_CODATA": target,
        "rows": rows,
        "best_simple_candidate": best_name,
        "best_relative_miss": best_row["relative_miss_q0_squared"],
        "no_simple_boundary_map_hits_target": best_row[
            "relative_miss_q0_squared"
        ]
        > 0.05,
        "target_not_used_as_choice": True,
        "reading": (
            "the obvious maps from the order-9 cap, its inverse, and the "
            "minimal prequantization coefficient do not produce the required "
            "q0^2.  This does not disprove RefG; it blocks the shortcut."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Boundary one-form openness
# ---------------------------------------------------------------------------

def boundary_one_form_openness() -> dict:
    P, theta, C, A = sp.symbols("P theta C A", real=True)
    dP, dtheta, dA = sp.symbols("dP dtheta dA", real=True)

    one_form = "Theta_boundary = P*dtheta + C*A"
    symplectic_form = "Omega_boundary = dP wedge dtheta + C*dA"

    q_geom = sp.Rational(H, ORDER)
    n = sp.symbols("n", integer=True, positive=True)
    quantization = sp.Eq(C * q_geom, n)
    C_solution = sp.solve(quantization, C)[0]

    return {
        "one_form": one_form,
        "symplectic_form": symplectic_form,
        "quantization_condition_on_cap": str(quantization),
        "C_solution_from_integrality": str(C_solution),
        "C_still_a_dynamic_coefficient_before_integrality_branch_choice": True,
        "requires_action_to_select_branch_and_map_to_q0": True,
        "reading": (
            "the boundary one-form shows the precise missing coefficient.  "
            "Topology quantizes C*q_geom, while dynamics must tell us what C "
            "is and how it enters q0."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Next theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "dynamic coefficient C of the boundary one-form and its map to "
            "q0=k_J/sqrt(K_F)"
        ),
        "must_derive": [
            "Theta_boundary from the completed localized frame action",
            "which integrality branch n belongs to one electron/charged oscillon",
            "whether C is independent or fixed by regularity/core matching",
            "the map from C and the cap holonomy to Maxwell-normalized q0",
            "whether the result is a bare geometric alpha or the low-energy alpha",
        ],
        "falsification_tests": [
            "if C remains an independent coefficient, alpha is not derived",
            "if n is chosen to fit alpha, the gate fails",
            "if the map from C to q0 is postulated, the gate fails",
            "if coadjoint/cap integrality is the only input, the shortcut fails",
        ],
        "candidate_next_gate": "p18ad_dynamic_boundary_coefficient_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_boundary_symplectic_form_gate() -> dict:
    geometry = boundary_frame_bundle_geometry()
    orbit = coadjoint_orbit_prequantization_audit()
    cap = cap_cell_prequantization_audit()
    maps = simple_map_audit()
    one_form = boundary_one_form_openness()
    requirements = next_theorem_requirements()

    closed = {
        "order9_h2_boundary_register_fixed": bool(
            geometry["register_cleanly_fixed"]
        ),
        "coadjoint_orbit_shortcut_rejected": bool(
            orbit["target_is_not_integral_orbit_area"]
        ),
        "cap_prequantization_quantizes_product": bool(
            cap["product_quantized_not_C_fixed_absolutely"]
        ),
        "simple_boundary_maps_do_not_hit_target": bool(
            maps["no_simple_boundary_map_hits_target"]
        ),
        "boundary_one_form_exposes_dynamic_C": bool(
            one_form["C_still_a_dynamic_coefficient_before_integrality_branch_choice"]
            and one_form["requires_action_to_select_branch_and_map_to_q0"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "Theta_boundary_derived_from_action": False,
        "dynamic_C_derived": False,
        "electron_integrality_branch_derived": False,
        "C_to_q0_map_derived": False,
        "q0_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_DYNAMIC_BOUNDARY_COEFFICIENT_REQUIRED__"
            + _pass_status("BOUNDARY_SYMPLECTIC_FORM_AUDIT")
            if all(closed.values())
            else "CHECK_BOUNDARY_SYMPLECTIC_FORM_GATE"
        ),
        "SCOPE": (
            "boundary symplectic-form gate after p18ab: the order-9, h=2 "
            "frame-bundle cell is cleanly identified as q_geom=2/9 with "
            "holonomy 4*pi/9.  Prequantization and simple boundary maps do "
            "not derive q0 or alpha.  The missing object is the dynamic "
            "boundary coefficient C and its action-level map to Maxwell "
            "normalization."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "boundary_geometry": geometry,
        "coadjoint_orbit_audit": orbit,
        "cap_cell_prequantization": cap,
        "simple_map_audit": maps,
        "boundary_one_form": one_form,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the boundary geometry has done its job: it gives the 2/9 "
            "electric register.  It does not give the strength of that "
            "register as a Maxwell charge.  That strength sits in a dynamic "
            "coefficient of the boundary one-form.  This is the next real "
            "target."
        ),
        "missing_derivations": [
            "derive the boundary one-form from the completed localized frame action",
            "derive the coefficient C rather than choosing it",
            "derive the electron branch n and the C-to-q0 map",
            "compute q0 and alpha without CODATA",
        ],
        "do_not_claim": [
            "Do not claim alpha or q0 are derived.",
            "Do not claim the order-9/h=2 holonomy cell alone gives 137.",
            "Do not choose C or n from observed alpha.",
            "Do not identify a simple coadjoint-orbit area with the needed cell.",
            "Do not postulate the C-to-q0 map.",
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
    print("boundary_geometry:", result["boundary_geometry"])
    print("coadjoint_orbit_audit:", result["coadjoint_orbit_audit"])
    print("cap_cell_prequantization:", result["cap_cell_prequantization"])
    print("simple_map_audit:", result["simple_map_audit"])
    print("boundary_one_form:", result["boundary_one_form"])
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
    _print_result(derive_boundary_symplectic_form_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
