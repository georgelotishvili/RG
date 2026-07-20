# Notation header (see NOTATION.md):
# This gate follows p18n.  It tests the first acceptable route named there:
# a single SO(3)/U(1) orientation-frame action whose expansion fixes the
# fiber/twist and axis/writhe stiffness prefactors.

"""
================================================================================
PHASE 18o: Unified frame stiffness theorem candidate
================================================================================

Purpose
-------
p18n showed that the p18e-h grammar leaves

    rho = k_f/k_a

free.  The first legitimate way to fix rho is not a number fit, but a stronger
action principle.  This gate checks the cleanest candidate:

    the local orientation-frame stiffness is an SO(3)-isotropic quadratic
    norm of the frame angular velocity.

Result
------
The theorem is simple and executable.  Let Omega_i be the infinitesimal
rotation vector of the local oriented frame.  Around the background axis
n=e_3,

    axis motion:   |d n|^2 = Omega_1^2 + Omega_2^2,
    fiber motion:  (D theta)^2 = Omega_3^2.

The SO(3)-isotropic quadratic action

    L_frame = kappa * (Omega_1^2 + Omega_2^2 + Omega_3^2)

therefore fixes

    k_f = k_a = kappa,       rho = 1.

This is a genuine stiffness theorem IF the stronger SO(3)-isotropic frame
action is accepted/derived from the RefG medium.  It is not a convention.

But it still does NOT derive alpha.  With rho=1 the p18m lock expression still
contains the topological/boundary spectral factor.  Therefore the next lock is
not "choose rho"; it is:

    derive the finite boundary/anholonomy factor of the localized
    orientation-frame resonator.

What this gate does NOT claim
-----------------------------
- It does not derive the SO(3)-isotropic action from p01.
- It does not derive N or alpha.
- It does not prove that anisotropic U(1)-only stiffness is impossible.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
N_REQUIRED = ALPHA_INV_CODATA / (4.0 * math.pi)


# ---------------------------------------------------------------------------
# 1. Frame decomposition
# ---------------------------------------------------------------------------

def frame_decomposition() -> dict:
    w1, w2, w3 = sp.symbols("Omega_1 Omega_2 Omega_3", real=True)
    omega = sp.Matrix([w1, w2, w3])
    e3 = sp.Matrix([0, 0, 1])
    dn = omega.cross(e3)
    axis_norm = sp.simplify(dn.dot(dn))
    fiber_norm = w3**2
    full_norm = sp.simplify(axis_norm + fiber_norm)
    return {
        "dn": [str(c) for c in dn],
        "axis_norm": str(axis_norm),
        "fiber_norm": str(fiber_norm),
        "full_norm": str(full_norm),
        "axis_norm_is_Omega1sq_plus_Omega2sq": sp.simplify(
            axis_norm - (w1**2 + w2**2)
        )
        == 0,
        "fiber_norm_is_Omega3sq": sp.simplify(fiber_norm - w3**2) == 0,
    }


# ---------------------------------------------------------------------------
# 2. SO(3)-isotropic stiffness theorem
# ---------------------------------------------------------------------------

def so3_isotropic_stiffness_theorem() -> dict:
    kappa, w1, w2, w3 = sp.symbols(
        "kappa Omega_1 Omega_2 Omega_3", positive=True
    )
    L = kappa * (w1**2 + w2**2 + w3**2)
    k_axis_1 = sp.diff(L, w1, 2) / 2
    k_axis_2 = sp.diff(L, w2, 2) / 2
    k_fiber = sp.diff(L, w3, 2) / 2
    rho = sp.simplify(k_fiber / k_axis_1)
    return {
        "k_axis_1": str(k_axis_1),
        "k_axis_2": str(k_axis_2),
        "k_fiber": str(k_fiber),
        "axis_degenerate": sp.simplify(k_axis_1 - k_axis_2) == 0,
        "fiber_equals_axis": sp.simplify(k_fiber - k_axis_1) == 0,
        "rho": str(rho),
        "rho_fixed_to_one": sp.simplify(rho - 1) == 0,
    }


# ---------------------------------------------------------------------------
# 3. U(1)-only anisotropic counterfactual
# ---------------------------------------------------------------------------

def u1_anisotropic_counterfactual() -> dict:
    kp, kz, w1, w2, w3 = sp.symbols(
        "k_perp k_parallel Omega_1 Omega_2 Omega_3", positive=True
    )
    L = kp * (w1**2 + w2**2) + kz * w3**2
    k_axis = sp.diff(L, w1, 2) / 2
    k_fiber = sp.diff(L, w3, 2) / 2
    rho = sp.simplify(k_fiber / k_axis)
    return {
        "rho": str(rho),
        "rho_free_under_U1_only": rho.has(kz) and rho.has(kp),
        "physical_reading": (
            "U(1)-only symmetry preserves the fiber/axis split and therefore "
            "does not fix the impedance ratio"
        ),
    }


# ---------------------------------------------------------------------------
# 4. Alpha-lock consequence
# ---------------------------------------------------------------------------

def alpha_lock_consequence() -> dict:
    Ctop, S = sp.symbols("C_top S_boundary", positive=True)
    rho = sp.Integer(1)
    N_expr = sp.simplify(Ctop * S * sp.sqrt(rho))
    Nreq = sp.symbols("N_required", positive=True)
    solved_S = sp.solve(sp.Eq(N_expr, Nreq), S)
    return {
        "N_expression_after_rho_1": str(N_expr),
        "still_depends_on_boundary_factor": N_expr.has(Ctop) and N_expr.has(S),
        "matching_N_would_solve_for_boundary_factor": solved_S == [
            Nreq / Ctop
        ],
        "N_required_numeric": N_REQUIRED,
        "conclusion": (
            "SO(3) isotropy can close rho, but alpha still needs the finite "
            "boundary/anholonomy factor; rho=1 alone is not 137"
        ),
    }


# ---------------------------------------------------------------------------
# 5. Required derivation ledger
# ---------------------------------------------------------------------------

def required_derivation_ledger() -> dict:
    return {
        "closed_if_accepted": (
            "SO(3)-isotropic orientation-frame stiffness implies k_f=k_a"
        ),
        "still_open": [
            "derive the SO(3)-isotropic frame action from the RefG medium rather than postulate it",
            "derive the finite boundary/anholonomy factor S_boundary",
            "derive which Lk/h/order sector supplies the physical electric unit",
            "then compute N and alpha",
        ],
        "risk": (
            "if the real medium allows only U(1)-anisotropic stiffness, rho "
            "remains free and p18n's no-go stands"
        ),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_unified_frame_stiffness_gate() -> dict:
    decomp = frame_decomposition()
    so3 = so3_isotropic_stiffness_theorem()
    u1 = u1_anisotropic_counterfactual()
    alpha = alpha_lock_consequence()
    ledger = required_derivation_ledger()

    closed = {
        "frame_decomposition_correct": bool(
            decomp["axis_norm_is_Omega1sq_plus_Omega2sq"]
            and decomp["fiber_norm_is_Omega3sq"]
        ),
        "SO3_isotropic_action_fixes_axis_degeneracy": bool(
            so3["axis_degenerate"]
        ),
        "SO3_isotropic_action_fixes_fiber_axis_equality": bool(
            so3["fiber_equals_axis"]
        ),
        "rho_fixed_to_one_under_SO3_isotropy": bool(so3["rho_fixed_to_one"]),
        "U1_only_counterfactual_leaves_rho_free": bool(
            u1["rho_free_under_U1_only"]
        ),
        "rho_one_still_not_alpha": bool(
            alpha["still_depends_on_boundary_factor"]
            and alpha["matching_N_would_solve_for_boundary_factor"]
        ),
    }

    open_checks = {
        "SO3_isotropic_action_derived_from_RefG_medium": False,
        "finite_boundary_anholonomy_factor_derived": False,
        "electric_unit_sector_derived": False,
        "N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_BOUNDARY_ANHOLONOMY_FACTOR_NEXT__"
            + _pass_status("SO3_FRAME_STIFFNESS_RHO_ONE")
            if all(closed.values())
            else "CHECK_UNIFIED_FRAME_STIFFNESS_GATE"
        ),
        "SCOPE": (
            "candidate stiffness theorem after p18n: a stronger SO(3)-"
            "isotropic orientation-frame action fixes k_f=k_a and therefore "
            "rho=1.  This is the first non-fitting route that can close rho, "
            "but it still leaves the finite boundary/anholonomy factor open. "
            "Alpha is not computed."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "frame_decomposition": decomp,
        "SO3_theorem": so3,
        "U1_counterfactual": u1,
        "alpha_consequence": alpha,
        "required_derivations": ledger,
        "physical_reading": (
            "the stiffness bottleneck has a clean possible resolution: full "
            "SO(3) isotropy of the local orientation-frame stiffness.  If "
            "that action is derived, rho is no longer free.  The remaining "
            "number must then come from the finite boundary/anholonomy sector, "
            "not from a stiffness fit."
        ),
        "missing_derivations": ledger["still_open"],
        "do_not_claim": [
            "Do not claim alpha or N are derived.",
            "Do not claim SO(3) isotropy is derived from p01 in this gate.",
            "Do not set the boundary factor to fit N.",
            "Do not forget the U(1)-anisotropic counterfactual: without the "
            "stronger SO(3) action, rho remains free.",
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
    print("frame_decomposition:", result["frame_decomposition"])
    print("SO3_theorem:", result["SO3_theorem"])
    print("U1_counterfactual:", result["U1_counterfactual"])
    print("alpha_consequence:", result["alpha_consequence"])
    print("required_derivations:", result["required_derivations"])
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
    _print_result(derive_unified_frame_stiffness_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
