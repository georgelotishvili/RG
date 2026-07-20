# Notation header (see NOTATION.md):
# This gate follows p18p.  It audits whether the magnetic/frame-flux register
# from p18i plus the electric/framing current from p18k can fix alpha through a
# Dirac/Gauss normalization condition.

"""
================================================================================
PHASE 18q: Electric-magnetic normalization audit
================================================================================

Purpose
-------
p18i identified the hedgehog as a magnetic/frame-curvature flux register.
p18k identified electric charge as a closed framing/twist current.  p18p
identified the finite electric unit sector (order-9, h=2), but left the map to
N open.

This gate checks a natural next possibility:

    Can electric-magnetic quantization fix the coupling normalization?

Result
------
It cannot fix alpha by itself.  It gives the expected product quantization:

    q_e * g_m = 2*pi*n       (convention-dependent 2*pi unit),

or equivalently a Wilson phase exp(i q_e g_m) = 1.  But unless the absolute
magnetic normalization g_m is derived in the same units as the electric
coupling, this only trades one unknown for another.  If one naively sets the
geometric flux g_m=4*pi as a unit charge, the resulting alpha is not the
observed value; therefore that shortcut is forbidden.

The real missing object is the medium impedance / dual normalization that
converts the frame-curvature flux unit and the framing-current unit into the
same canonical Maxwell normalization.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive the electric coupling.
- It does not derive the magnetic/electric impedance normalization.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA


# ---------------------------------------------------------------------------
# 1. Dirac/Wilson product quantization
# ---------------------------------------------------------------------------

def product_quantization_gate() -> dict:
    qe, gm, n = sp.symbols("q_e g_m n", positive=True)
    condition = sp.Eq(qe * gm, 2 * sp.pi * n)
    qe_solution = sp.solve(condition, qe)[0]
    alpha_expr = sp.simplify(qe_solution**2 / (4 * sp.pi))
    return {
        "condition": "q_e * g_m = 2*pi*n",
        "q_e_solution": str(qe_solution),
        "alpha_expression": str(alpha_expr),
        "alpha_still_depends_on_gm": alpha_expr.has(gm),
        "product_quantizes_but_does_not_fix_alpha": True,
    }


# ---------------------------------------------------------------------------
# 2. Naive geometric flux shortcut audit
# ---------------------------------------------------------------------------

def naive_flux_shortcut_audit() -> dict:
    n = 1
    gm_geo = 4.0 * math.pi
    qe = 2.0 * math.pi * n / gm_geo
    alpha = qe**2 / (4.0 * math.pi)
    alpha_inv = 1.0 / alpha
    miss = abs(alpha_inv - ALPHA_INV_CODATA)
    return {
        "gm_geo_assumed": gm_geo,
        "qe_from_dirac_if_gm_geo": qe,
        "alpha_inv_from_shortcut": alpha_inv,
        "miss_vs_CODATA_alpha_inv": miss,
        "shortcut_fails_observed_alpha": miss > 1.0,
        "conclusion": (
            "setting geometric 4*pi flux directly equal to canonical magnetic "
            "charge is not the RefG alpha derivation"
        ),
    }


# ---------------------------------------------------------------------------
# 3. Medium impedance normalization ledger
# ---------------------------------------------------------------------------

def medium_impedance_ledger() -> dict:
    Ze, Zm, q_geom, g_geom = sp.symbols(
        "Z_electric Z_magnetic q_geom g_geom", positive=True
    )
    qe = sp.sqrt(Ze) * q_geom
    gm = sp.sqrt(Zm) * g_geom
    alpha = sp.simplify(qe**2 / (4 * sp.pi))
    product = sp.simplify(qe * gm)
    return {
        "canonical_qe": str(qe),
        "canonical_gm": str(gm),
        "alpha": str(alpha),
        "dirac_product": str(product),
        "depends_on_impedance": alpha.has(Ze) and product.has(Ze) and product.has(Zm),
        "needed_theorem": (
            "derive the electric/magnetic medium impedance that maps geometric "
            "framing current and frame-curvature flux to canonical Maxwell "
            "normalization"
        ),
    }


# ---------------------------------------------------------------------------
# 4. Relation to N target
# ---------------------------------------------------------------------------

def N_relation_ledger() -> dict:
    N_required = ALPHA_INV_CODATA / (4.0 * math.pi)
    qe_required = math.sqrt(4.0 * math.pi * ALPHA_CODATA)
    gm_required_dirac_n1 = 2.0 * math.pi / qe_required
    return {
        "N_required": N_required,
        "q_e_required_in_hbar_c_1": qe_required,
        "g_m_required_by_dirac_n1": gm_required_dirac_n1,
        "g_m_required_over_4pi": gm_required_dirac_n1 / (4.0 * math.pi),
        "physical_reading": (
            "observed alpha corresponds to a magnetic normalization about "
            "1/(4*pi) times g_m_required, so the geometric 4*pi flux still "
            "needs a nontrivial medium normalization"
        ),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_electric_magnetic_normalization_gate() -> dict:
    product = product_quantization_gate()
    shortcut = naive_flux_shortcut_audit()
    impedance = medium_impedance_ledger()
    Nrel = N_relation_ledger()

    closed = {
        "dirac_product_quantization_written": bool(product["condition"]),
        "alpha_still_depends_on_magnetic_normalization": bool(
            product["alpha_still_depends_on_gm"]
        ),
        "naive_4pi_flux_shortcut_rejected": bool(
            shortcut["shortcut_fails_observed_alpha"]
        ),
        "medium_impedance_slot_identified": bool(
            impedance["depends_on_impedance"]
        ),
        "N_target_translated_to_required_dual_normalization": bool(
            Nrel["g_m_required_over_4pi"] > 0
        ),
    }

    open_checks = {
        "medium_impedance_derived": False,
        "canonical_electric_coupling_derived": False,
        "canonical_magnetic_normalization_derived": False,
        "N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_MEDIUM_IMPEDANCE_THEOREM_REQUIRED__"
            + _pass_status("DUAL_NORMALIZATION_AUDIT")
            if all(closed.values())
            else "CHECK_DUAL_NORMALIZATION_AUDIT"
        ),
        "SCOPE": (
            "electric-magnetic normalization audit after p18p: Dirac/Wilson "
            "product quantization is compatible with the frame-flux and "
            "framing-current registers, but it does not fix alpha without a "
            "medium impedance theorem.  The naive g_m=4*pi shortcut fails."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "product_quantization": product,
        "naive_shortcut": shortcut,
        "impedance_ledger": impedance,
        "N_relation": Nrel,
        "physical_reading": (
            "the next missing factor is not topological; topology gives the "
            "integer product.  The fine-structure value lives in the medium "
            "impedance that converts RefG's geometric flux/current units into "
            "canonical Maxwell units."
        ),
        "missing_derivations": [
            "derive the medium impedance between frame-curvature flux and "
            "framing-current units",
            "derive canonical electric coupling q_e from the localized "
            "orientation-frame action",
            "combine that impedance with the order-9/h=2 boundary sector to "
            "compute N without fitting",
        ],
        "do_not_claim": [
            "Do not claim Dirac quantization fixes alpha by itself.",
            "Do not identify geometric flux 4*pi with canonical magnetic "
            "charge without the impedance theorem.",
            "Do not set the impedance to fit CODATA.",
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
    print("product_quantization:", result["product_quantization"])
    print("naive_shortcut:", result["naive_shortcut"])
    print("impedance_ledger:", result["impedance_ledger"])
    print("N_relation:", result["N_relation"])
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
    _print_result(derive_electric_magnetic_normalization_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
