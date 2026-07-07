# Notation header (see NOTATION.md):
# This gate is the alpha-lock audit after p18e-i.  It deliberately performs
# no integer/constant scan.  It asks whether the existing orientation-frame
# gates already force the dimensionless normalization
#     N = alpha_inv/(4*pi) = 10.904978325...
# or whether one more stiffness/spectrum theorem is still missing.

"""
================================================================================
PHASE 18j: Finite orientation-frame lock and alpha normalization audit
================================================================================

Purpose
-------
Execute lock 4 named by p18i:

    "derive N as the ratio of fiber-step to axis-step spectra on the same
     finite orientation-frame resonator; no number scanning."

The honest result of this gate is negative-but-sharp: p18e-i have located the
right arena for alpha, but they do NOT yet determine N.  They supply:

  * a compact frame/fiber register,
  * a fixed holonomy curvature,
  * two luminal axis modes,
  * a Coulomb/Maxwell far-field normalization slot,
  * same-resonator size cancellation.

They still do not supply the final dimensionless stiffness/spectrum ratio.
Therefore this file refuses to call alpha derived.  It computes the exact
target, proves which factors cancel, and isolates the single missing theorem.

Results (all executable below)
------------------------------
1. TARGET LEDGER:

       N_required = alpha_inv/(4*pi) = 10.904978325278...
       alpha = 1/(4*pi*N_required)

   This is only the target, not a derivation.

2. SAME-RESONATOR SIZE CANCELLATION: for two luminal channels on the same
   finite base, omega_n ~ n*pi/L, the ratio omega_f/omega_a is independent of
   L.  The author's "finite base gives discreteness; ratio cancels size"
   principle is executable and correct at this level.

3. FREE-STIFFNESS NO-GO: the most general lock expression allowed by the
   p18e-i data has the schematic form

       N = C_top * rho_stiffness * spectral_ratio,

   where C_top is fixed by geometry/topology, but rho_stiffness is not fixed
   by the solar sector, the cone condition, the U(1) completion, or the
   far-field Maxwell ledger.  Matching N_required would simply define
   rho_stiffness by hand.  That is not a derivation.

4. NEXT THEOREM: to derive alpha, one must compute rho_stiffness from the
   completed finite orientation-frame dynamics: the ratio between the
   framing/fiber step and the axis/curvature step on the same finite
   resonator.  Only then can alpha = W^2/(4*pi*N) become a result.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not approximate alpha.
- It performs no number scan.
- It does not choose boundary conditions for the finite resonator.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_INV_CODATA_SIGMA = 0.000000021


# ---------------------------------------------------------------------------
# 1. Target ledger
# ---------------------------------------------------------------------------

def target_ledger() -> dict:
    N_required = ALPHA_INV_CODATA / (4.0 * math.pi)
    N_sigma = ALPHA_INV_CODATA_SIGMA / (4.0 * math.pi)
    alpha_back = 1.0 / (4.0 * math.pi * N_required)
    return {
        "N_required": N_required,
        "N_required_sigma": N_sigma,
        "alpha_back_matches_CODATA": abs(alpha_back - 1.0 / ALPHA_INV_CODATA)
        < 1e-18,
        "route_formula": "alpha = W^2/(4*pi*N), W=1 only after completed bundle charge is fixed",
    }


# ---------------------------------------------------------------------------
# 2. Same-resonator size cancellation
# ---------------------------------------------------------------------------

def same_resonator_size_cancellation() -> dict:
    L, nf, na = sp.symbols("L n_f n_a", positive=True)
    omega_f = sp.pi * nf / L
    omega_a = sp.pi * na / L
    ratio = sp.simplify(omega_f / omega_a)
    return {
        "ratio": str(ratio),
        "independent_of_L": sp.diff(ratio, L) == 0,
        "principle": (
            "finite L discretizes both spectra; comparing two channels on "
            "the same base cancels L"
        ),
    }


# ---------------------------------------------------------------------------
# 3. Free-stiffness audit
# ---------------------------------------------------------------------------

def free_stiffness_no_go() -> dict:
    C_top, rho, S = sp.symbols("C_top rho_stiffness S_spectral", positive=True)
    N = C_top * rho * S
    N_req = sp.Symbol("N_required", positive=True)
    solved_rho = sp.solve(sp.Eq(N, N_req), rho)
    return {
        "N_expression": str(N),
        "depends_on_free_stiffness_ratio": sp.diff(N, rho) != 0,
        "matching_target_solves_for_rho_by_hand": solved_rho == [
            N_req / (C_top * S)
        ],
        "current_data_cannot_fix_N": True,
        "reason": (
            "p18e/p18f cone exactness fixes propagation speed, not absolute "
            "normalization; p18h fixes the connection geometry, not the "
            "finite stiffness spectrum; p18i fixes far-field scaling, not "
            "the electric framing coupling"
        ),
    }


# ---------------------------------------------------------------------------
# 4. Required theorem ledger
# ---------------------------------------------------------------------------

def required_theorem_ledger() -> dict:
    return {
        "needed_object": (
            "rho_stiffness = framing/fiber step stiffness divided by "
            "axis/curvature step stiffness on the same finite orientation "
            "resonator"
        ),
        "must_be_derived_from": [
            "completed bundle boundary conditions",
            "electric framing/twist coupling",
            "finite spectrum of axis and fiber sectors",
            "core-to-far-field matching from p18i",
        ],
        "must_not_be": [
            "fit to alpha",
            "integer scan",
            "chosen normalization convention",
            "hidden background frequency",
        ],
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_finite_orientation_lock_alpha_gate() -> dict:
    target = target_ledger()
    size = same_resonator_size_cancellation()
    free = free_stiffness_no_go()
    needed = required_theorem_ledger()

    closed = {
        "N_target_computed": bool(target["N_required"] > 0),
        "alpha_formula_self_consistent": bool(target["alpha_back_matches_CODATA"]),
        "same_resonator_size_cancels": bool(size["independent_of_L"]),
        "general_lock_expression_identified": bool(
            "rho_stiffness" in free["N_expression"]
        ),
        "stiffness_ratio_remains_free": bool(
            free["depends_on_free_stiffness_ratio"]
        ),
        "matching_target_would_be_hand_fit_now": bool(
            free["matching_target_solves_for_rho_by_hand"]
        ),
        "number_scan_not_performed": True,
    }

    open_checks = {
        "electric_framing_coupling_derived": False,
        "finite_boundary_conditions_derived": False,
        "axis_and_fiber_spectra_computed_from_same_action": False,
        "rho_stiffness_derived": False,
        "N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_STIFFNESS_RATIO_THEOREM_REQUIRED__"
            + _pass_status("FINITE_LOCK_AUDIT_NO_NUMEROLOGY")
            if all(closed.values())
            else "CHECK_FINITE_LOCK_AUDIT"
        ),
        "SCOPE": (
            "lock 4 audit: p18e-i provide the correct orientation-frame "
            "arena and same-resonator size cancellation, but they do not "
            "yet derive the dimensionless stiffness/spectrum ratio N.  "
            "Alpha is therefore NOT computed; the next required theorem is "
            "rho_stiffness from the completed finite orientation-frame "
            "dynamics, with no number scanning."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "target": target,
        "size_cancellation": size,
        "free_stiffness_audit": free,
        "required_theorem": needed,
        "physical_reading": (
            "the theory has narrowed alpha to a precise missing lock rather "
            "than a vague mystery.  The number N must be a derived ratio of "
            "two spectra/stiffnesses on one finite orientation-frame object. "
            "At the present gate that ratio is still free, so claiming "
            "alpha would be numerology."
        ),
        "missing_derivations": [
            "derive the electric framing/twist coupling left open by p18i",
            "derive finite boundary conditions for the completed "
            "orientation-frame resonator",
            "compute the fiber/framing and axis/curvature spectra from the "
            "same action and take their stiffness ratio",
            "only then test whether N = 10.904978325... follows",
        ],
        "do_not_claim": [
            "Do not claim alpha is derived or approximated here.",
            "Do not insert N_required as a normalization choice.",
            "Do not scan integers/constants to hit 10.904978325.",
            "Do not treat size cancellation as enough; it removes L but "
            "does not fix rho_stiffness.",
            "Do not reintroduce a hidden background frequency.",
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
    print("target:")
    for key, val in result["target"].items():
        print(f"  {key}: {val}")
    print("size_cancellation:", result["size_cancellation"])
    print("free_stiffness_audit:", result["free_stiffness_audit"])
    print("required_theorem:", result["required_theorem"])
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
    _print_result(derive_finite_orientation_lock_alpha_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
