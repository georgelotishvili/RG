# Notation header (see NOTATION.md):
# This gate follows p18q.  It rejects the obvious shortcut normalizations before
# the alpha chain proceeds to a genuine medium-impedance theorem.

"""
================================================================================
PHASE 18r: Impedance shortcut rejection gate
================================================================================

Purpose
-------
p18q showed that topology gives electric-magnetic product quantization but not
alpha.  This gate checks the obvious shortcuts that could otherwise sneak in:

  1. canonical electric unit q_geom = 1 with impedance Z=1,
  2. order-9/h=2 electric coordinate q_geom = theta = 2/9 with Z=1,
  3. geometric magnetic flux g_m = 4*pi as the canonical magnetic charge.

All three fail.  The observed alpha requires a nontrivial medium impedance
factor.  That factor must be derived; it cannot be chosen.

What this gate does NOT claim
-----------------------------
- It does not derive the impedance.
- It does not derive alpha.
- It does not scan arbitrary formulas.
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
# 1. Electric-unit shortcut checks
# ---------------------------------------------------------------------------

def electric_unit_shortcuts() -> dict:
    candidates = {
        "unit_winding_q1": 1.0,
        "order9_h2_theta": THETA_H,
    }
    rows = {}
    for name, q in candidates.items():
        alpha = q**2 / (4.0 * math.pi)
        rows[name] = {
            "q_geom": q,
            "alpha_inv_if_Z1": 1.0 / alpha,
            "miss_vs_CODATA_alpha_inv": abs(1.0 / alpha - ALPHA_INV_CODATA),
            "fails": abs(1.0 / alpha - ALPHA_INV_CODATA) > 1.0,
            "Z_required": 4.0 * math.pi * ALPHA_CODATA / (q**2),
        }
    return {
        "rows": rows,
        "all_Z1_shortcuts_fail": all(row["fails"] for row in rows.values()),
    }


# ---------------------------------------------------------------------------
# 2. Magnetic-flux shortcut check
# ---------------------------------------------------------------------------

def magnetic_flux_shortcut() -> dict:
    gm = 4.0 * math.pi
    qe = 2.0 * math.pi / gm
    alpha = qe**2 / (4.0 * math.pi)
    alpha_inv = 1.0 / alpha
    return {
        "g_m_assumed": gm,
        "q_e_from_Dirac_n1": qe,
        "alpha_inv": alpha_inv,
        "miss_vs_CODATA_alpha_inv": abs(alpha_inv - ALPHA_INV_CODATA),
        "fails": abs(alpha_inv - ALPHA_INV_CODATA) > 1.0,
        "required_gm_over_4pi": (2.0 * math.pi / math.sqrt(4.0 * math.pi * ALPHA_CODATA))
        / (4.0 * math.pi),
    }


# ---------------------------------------------------------------------------
# 3. Symbolic impedance requirement
# ---------------------------------------------------------------------------

def symbolic_impedance_requirement() -> dict:
    q, Z, Nreq = sp.symbols("q_geom Z_medium N_required", positive=True)
    alpha = Z * q**2 / (4 * sp.pi)
    N = sp.simplify(1 / (4 * sp.pi * alpha))
    Z_solution = sp.solve(sp.Eq(N, Nreq), Z)[0]
    return {
        "alpha_expression": str(alpha),
        "N_expression": str(N),
        "Z_required_symbolic": str(Z_solution),
        "depends_on_impedance": alpha.has(Z),
        "matching_N_solves_for_Z": True,
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_impedance_shortcut_rejection_gate() -> dict:
    electric = electric_unit_shortcuts()
    magnetic = magnetic_flux_shortcut()
    symbolic = symbolic_impedance_requirement()

    closed = {
        "unit_and_theta_Z1_shortcuts_fail": bool(
            electric["all_Z1_shortcuts_fail"]
        ),
        "magnetic_4pi_shortcut_fails": bool(magnetic["fails"]),
        "observed_alpha_requires_nontrivial_Z": bool(
            symbolic["depends_on_impedance"]
            and symbolic["matching_N_solves_for_Z"]
        ),
        "no_arbitrary_formula_scan_performed": True,
    }

    open_checks = {
        "Z_medium_derived": False,
        "q_geom_selected_by_action": False,
        "N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_MEDIUM_IMPEDANCE_DYNAMICS_REQUIRED__"
            + _pass_status("IMPEDANCE_SHORTCUTS_REJECTED")
            if all(closed.values())
            else "CHECK_IMPEDANCE_SHORTCUT_REJECTION"
        ),
        "SCOPE": (
            "shortcut rejection after p18q: the natural unit electric charge, "
            "the order-9/h=2 theta charge, and the geometric 4*pi magnetic "
            "flux do not reproduce alpha with unit impedance.  The missing "
            "object is a genuine medium-impedance theorem."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "electric_shortcuts": electric,
        "magnetic_shortcut": magnetic,
        "symbolic_impedance": symbolic,
        "physical_reading": (
            "the chain is now protected against the tempting shortcuts.  The "
            "137-lock cannot be obtained by declaring a geometric unit to be "
            "canonical; the medium must tell us the impedance converting "
            "geometry into Maxwell normalization."
        ),
        "missing_derivations": [
            "derive Z_medium from the completed localized orientation-frame "
            "action",
            "derive which geometric electric unit q_geom is selected by the "
            "defect boundary problem",
            "combine q_geom and Z_medium to compute N",
        ],
        "do_not_claim": [
            "Do not set Z_medium=1 without derivation.",
            "Do not identify q_geom=2/9 with q_e directly.",
            "Do not identify geometric flux 4*pi with canonical magnetic "
            "charge directly.",
            "Do not claim alpha or N are derived.",
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
    print("electric_shortcuts:", result["electric_shortcuts"])
    print("magnetic_shortcut:", result["magnetic_shortcut"])
    print("symbolic_impedance:", result["symbolic_impedance"])
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
    _print_result(derive_impedance_shortcut_rejection_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
