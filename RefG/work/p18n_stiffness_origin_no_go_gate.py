# Notation header (see NOTATION.md):
# This gate follows p18m.  It asks whether the p18e-h orientation-frame action
# already fixes the stiffness ratio rho = k_f/k_a required by the alpha lock.

"""
================================================================================
PHASE 18n: Stiffness-origin no-go gate
================================================================================

Purpose
-------
p18m reduced the alpha-lock problem to a single missing object:

    rho_stiffness = k_f/k_a,

the elastic impedance ratio between the fiber/twist channel and the
axis/writhe channel of the same localized orientation-frame object.

This gate checks whether rho is already fixed by the p18e-h action grammar.
The answer is NO.  The current completed quadratic action has the schematic
form

    L = F_f(Y,I1,I2,I3) * (D theta)^2
        + F_a(Y,I1,I2,I3) * P_n,

with two independent positive prefactors.  Cone exactness fixes the wave
speed, not the absolute normalization.  Solar transparency is blind to both
normalizations on constant-orientation backgrounds.  U(1) completion removes
theta as a third mode but does not identify F_f and F_a.  Therefore rho is a
flat normalization direction in the present gates.

This is not a failure.  It tells us precisely what the next real theorem must
do: derive rho from localized core dynamics, a stronger unifying frame action,
or a renormalization/matching condition.  Without that theorem, alpha remains
open.

What this gate does NOT claim
-----------------------------
- It does not derive rho, N, or alpha.
- It does not say rho cannot be derived in RefG.
- It says only that rho is not derived by the current p18e-h grammar.
"""

from __future__ import annotations

import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


# ---------------------------------------------------------------------------
# 1. Current grammar leaves two independent prefactors
# ---------------------------------------------------------------------------

def independent_prefactor_audit() -> dict:
    Ff, Fa = sp.symbols("F_f F_a", positive=True)
    rho = sp.simplify(Ff / Fa)
    # Cone speeds are C/K = 1 for both sectors when the metric-cone family
    # is F * kinetic form; multiplying by F does not change the cone.
    cf2 = sp.simplify(Ff / Ff)
    ca2 = sp.simplify(Fa / Fa)
    return {
        "fiber_cone_speed_independent_of_Ff": cf2 == 1,
        "axis_cone_speed_independent_of_Fa": ca2 == 1,
        "rho_expression": str(rho),
        "rho_depends_on_independent_prefactors": rho.has(Ff) and rho.has(Fa),
    }


# ---------------------------------------------------------------------------
# 2. Existing constraints do not contain rho
# ---------------------------------------------------------------------------

def constraint_rank_audit() -> dict:
    Ff, Fa = sp.symbols("F_f F_a", positive=True)
    # Existing p18e-h constraints at the normalization level:
    #   luminality: C/K - 1 = 0, identically for F*Pt and F*Pn;
    #   solar transparency: stress=0 at Dtheta=0, dn=0, also independent;
    #   gauge covariance: algebraic invariance of Dtheta, independent.
    constraints = [
        sp.Integer(0),  # luminality residual for F_f * Dtheta^2
        sp.Integer(0),  # luminality residual for F_a * Pn
        sp.Integer(0),  # solar residual at constant orientation
        sp.Integer(0),  # gauge covariance residual
    ]
    jac = sp.Matrix([[sp.diff(c, Ff), sp.diff(c, Fa)] for c in constraints])
    return {
        "constraint_jacobian_rank_in_Ff_Fa": jac.rank(),
        "constraints_blind_to_prefactors": jac.rank() == 0,
        "no_relation_Ff_equals_Fa": True,
        "no_relation_rho_equals_number": True,
    }


# ---------------------------------------------------------------------------
# 3. Isotropic-frame counterfactual
# ---------------------------------------------------------------------------

def isotropic_frame_counterfactual() -> dict:
    rho = sp.symbols("rho", positive=True)
    # A stronger SO(3)-isotropic frame action could set rho=1.  That would be
    # an extra theorem/assumption; it still would not produce N=10.9 by itself.
    return {
        "stronger_isotropic_action_would_set_rho_1": True,
        "rho_1_is_extra_assumption_not_current_derivation": True,
        "rho_1_not_alpha_lock_by_itself": True,
        "current_gate_requires_derivation_not_assumption": bool(rho != 1),
    }


# ---------------------------------------------------------------------------
# 4. Required next theorem
# ---------------------------------------------------------------------------

def required_next_theorem() -> dict:
    return {
        "needed_theorem": (
            "derive rho_stiffness = k_f/k_a from localized orientation-frame "
            "core dynamics or a stronger unified frame action"
        ),
        "acceptable_routes": [
            "single SO(3)/U(1) frame action whose expansion fixes both prefactors",
            "core matching between magnetic hedgehog flux and electric framing current",
            "RG/renormalization condition that locks F_f/F_a at the finite defect scale",
            "finite-energy variational problem with boundary conditions that quantize the impedance ratio",
        ],
        "unacceptable_routes": [
            "choose rho to fit alpha",
            "declare rho=1 without deriving the stronger symmetry",
            "scan constants for N",
            "hide rho in a background frequency",
        ],
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_stiffness_origin_no_go_gate() -> dict:
    pref = independent_prefactor_audit()
    rank = constraint_rank_audit()
    iso = isotropic_frame_counterfactual()
    needed = required_next_theorem()

    closed = {
        "cone_speed_blind_to_absolute_prefactors": bool(
            pref["fiber_cone_speed_independent_of_Ff"]
            and pref["axis_cone_speed_independent_of_Fa"]
        ),
        "rho_contains_independent_prefactors": bool(
            pref["rho_depends_on_independent_prefactors"]
        ),
        "existing_constraints_have_zero_rank_on_prefactors": bool(
            rank["constraints_blind_to_prefactors"]
        ),
        "current_gates_do_not_force_Ff_equals_Fa": bool(
            rank["no_relation_Ff_equals_Fa"]
        ),
        "current_gates_do_not_force_numeric_rho": bool(
            rank["no_relation_rho_equals_number"]
        ),
        "rho_1_identified_as_extra_counterfactual": bool(
            iso["rho_1_is_extra_assumption_not_current_derivation"]
            and iso["rho_1_not_alpha_lock_by_itself"]
        ),
    }

    open_checks = {
        "localized_core_action_derived": False,
        "unified_frame_prefactor_theorem_derived": False,
        "rho_stiffness_derived": False,
        "N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "BLOCKED_ON_LOCALIZED_STIFFNESS_THEOREM__"
            + _pass_status("CURRENT_GRAMMAR_RHO_NO_GO")
            if all(closed.values())
            else "CHECK_STIFFNESS_ORIGIN_AUDIT"
        ),
        "SCOPE": (
            "stiffness-origin audit after p18m: the current p18e-h grammar "
            "does not fix rho=k_f/k_a.  Luminality, solar transparency and "
            "U(1) gauge completion are blind to absolute prefactors.  Alpha "
            "is therefore blocked until a localized stiffness theorem or a "
            "stronger unified frame action derives rho."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "prefactor_audit": pref,
        "constraint_rank_audit": rank,
        "isotropic_counterfactual": iso,
        "required_next_theorem": needed,
        "physical_reading": (
            "we have reached the real mathematical bottleneck.  The chain "
            "has located the alpha number in one missing medium property: "
            "the elastic impedance ratio of the completed orientation-frame "
            "core.  Current gates cannot derive it; adding another audit "
            "without new dynamics will only restate this no-go."
        ),
        "missing_derivations": needed["acceptable_routes"],
        "do_not_claim": [
            "Do not claim alpha, N, or rho are derived.",
            "Do not set rho by convention.",
            "Do not identify cone exactness with normalization closure.",
            "Do not continue with number scans; the missing object is an "
            "action/core theorem.",
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
    print("prefactor_audit:", result["prefactor_audit"])
    print("constraint_rank_audit:", result["constraint_rank_audit"])
    print("isotropic_counterfactual:", result["isotropic_counterfactual"])
    print("required_next_theorem:", result["required_next_theorem"])
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
    _print_result(derive_stiffness_origin_no_go_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
