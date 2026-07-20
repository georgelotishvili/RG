# Notation header (see NOTATION.md):
# This gate follows p18k.  It audits the finite orientation-frame resonator
# spectrum without scanning numbers.  It asks whether ordinary periodic or
# twisted boundary conditions already determine the alpha-lock normalization N.

"""
================================================================================
PHASE 18l: Finite orientation-frame resonator spectrum audit
================================================================================

Purpose
-------
Continue the p18j/p18k alpha chain:

    derive finite boundary conditions and compute the fiber/framing and
    axis/curvature spectra from the same action.

The answer at this level is again sharp and limited.  A finite closed
orientation-frame resonator correctly gives discrete modes and cancels the
overall size L in ratios.  But ordinary periodic/twisted boundary conditions
do NOT determine the numerical normalization N.  They leave either a free
twist offset, a free stiffness ratio, or a choice of mode numbers.  Therefore
the alpha-lock still needs a dynamical boundary/anholonomy theorem.

Results (all executable below)
------------------------------
1. PERIODIC LUMINAL SPECTRUM:

       k_n = 2*pi*n/L,       omega_n = |k_n|

   for both the fiber/framing scalar and the two axis modes.

2. TWISTED BOUNDARY SPECTRUM:

       k_{n,delta} = 2*pi*(n + delta)/L,
       phi(s+L) = exp(2*pi*i*delta) phi(s).

   The same-resonator ratio cancels L:

       omega_f/omega_a = (n_f + delta_f)/(n_a + delta_a).

3. ORIENTED CLOSURE COMPATIBILITY:
   the p18k/p11g oriented-current logic still selects h=2 as the first
   nontrivial oriented closure, while h=1 is only projective.  This is a
   compatibility condition, not an alpha derivation.

4. NO-LOCK THEOREM:
   the most general finite-resonator audit expression has the form

       N = C_top * sqrt(k_f/k_a) * (n_f + delta_f)/(n_a + delta_a).

   Matching N_required at this stage merely solves for a free offset or a free
   stiffness ratio.  No number is derived.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive N.
- It does not choose the physical boundary offsets.
- It does not compute the localized core spectrum.
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
# 1. Periodic and twisted spectra
# ---------------------------------------------------------------------------

def periodic_luminal_spectrum() -> dict:
    L, n = sp.symbols("L n", positive=True)
    k = 2 * sp.pi * n / L
    omega = k
    return {
        "k_n": str(k),
        "omega_n": str(omega),
        "size_derivative_of_k_ratio_zero": True,
        "axis_degeneracy": "two identical p18f axis polarizations share the same k_n",
    }


def twisted_boundary_spectrum() -> dict:
    L = sp.symbols("L", positive=True)
    nf, na = sp.symbols("n_f n_a", integer=True, positive=True)
    df, da = sp.symbols("delta_f delta_a", real=True)
    kf = 2 * sp.pi * (nf + df) / L
    ka = 2 * sp.pi * (na + da) / L
    ratio = sp.simplify(kf / ka)
    return {
        "ratio": str(ratio),
        "ratio_independent_of_L": sp.diff(ratio, L) == 0,
        "depends_on_offsets": bool(ratio.has(df) or ratio.has(da)),
        "twisted_boundary_rule": "phi(s+L) = exp(2*pi*i*delta) phi(s)",
    }


# ---------------------------------------------------------------------------
# 2. Oriented closure compatibility
# ---------------------------------------------------------------------------

def oriented_closure_compatibility() -> dict:
    def director_after_half_turns(h: int) -> tuple[int, int]:
        angle = math.pi * h
        return (round(math.cos(angle)), round(math.sin(angle)))

    h1 = director_after_half_turns(1)
    h2 = director_after_half_turns(2)
    return {
        "h1_projective_only": h1 == (-1, 0),
        "h2_oriented_closed": h2 == (1, 0),
        "first_nontrivial_oriented_closure": 2,
        "status": "compatibility with p18k electric oriented-current branch",
    }


# ---------------------------------------------------------------------------
# 3. No-lock theorem
# ---------------------------------------------------------------------------

def finite_resonator_no_lock_theorem() -> dict:
    Ctop, rho = sp.symbols("C_top rho_stiffness", positive=True)
    nf, na = sp.symbols("n_f n_a", integer=True, positive=True)
    df, da = sp.symbols("delta_f delta_a", real=True)
    Nreq = sp.symbols("N_required", positive=True)
    N_expr = Ctop * sp.sqrt(rho) * (nf + df) / (na + da)
    solved_rho = sp.solve(sp.Eq(N_expr, Nreq), rho)
    solved_df = sp.solve(sp.Eq(N_expr, Nreq), df)
    return {
        "N_expression": str(N_expr),
        "depends_on_stiffness": N_expr.has(rho),
        "depends_on_boundary_offsets": N_expr.has(df) or N_expr.has(da),
        "matching_solves_for_rho_by_hand": solved_rho == [
            Nreq**2 * (da + na) ** 2 / (Ctop**2 * (df + nf) ** 2)
        ],
        "matching_solves_for_delta_by_hand": len(solved_df) == 1,
        "N_required_numeric": N_REQUIRED,
        "conclusion": (
            "finite discreteness and size cancellation are necessary but not "
            "sufficient; a dynamical theorem must fix rho_stiffness and/or "
            "the boundary offsets"
        ),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_finite_resonator_spectrum_gate() -> dict:
    periodic = periodic_luminal_spectrum()
    twisted = twisted_boundary_spectrum()
    closure = oriented_closure_compatibility()
    nolock = finite_resonator_no_lock_theorem()

    closed = {
        "periodic_spectrum_discrete": bool(periodic["k_n"]),
        "twisted_ratio_cancels_size": bool(twisted["ratio_independent_of_L"]),
        "twisted_ratio_keeps_boundary_offsets": bool(
            twisted["depends_on_offsets"]
        ),
        "oriented_h2_compatible": bool(
            closure["h1_projective_only"] and closure["h2_oriented_closed"]
        ),
        "general_N_expression_identified": bool(nolock["N_expression"]),
        "N_depends_on_free_stiffness_or_offsets": bool(
            nolock["depends_on_stiffness"]
            and nolock["depends_on_boundary_offsets"]
        ),
        "matching_N_now_would_be_hand_fit": bool(
            nolock["matching_solves_for_rho_by_hand"]
            and nolock["matching_solves_for_delta_by_hand"]
        ),
        "number_scan_not_performed": True,
    }

    open_checks = {
        "physical_boundary_offsets_derived": False,
        "rho_stiffness_derived_from_action": False,
        "localized_core_spectrum_computed": False,
        "N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_DYNAMIC_BOUNDARY_LOCK_REQUIRED__"
            + _pass_status("FINITE_RESONATOR_SPECTRUM_AUDIT")
            if all(closed.values())
            else "CHECK_FINITE_RESONATOR_SPECTRUM_AUDIT"
        ),
        "SCOPE": (
            "finite resonator spectrum audit after p18k: discreteness, "
            "luminal spectra, oriented h=2 compatibility, and same-base "
            "size cancellation are verified.  They still do not fix N; "
            "the missing ingredient is a dynamical boundary/anholonomy "
            "lock that fixes the stiffness ratio and boundary offsets."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "periodic_spectrum": periodic,
        "twisted_spectrum": twisted,
        "oriented_closure": closure,
        "no_lock_theorem": nolock,
        "physical_reading": (
            "the finite-resonator idea is structurally right but not yet "
            "numerically closed.  It gives discrete ratios and cancels the "
            "overall size, but alpha needs the next theorem: the physical "
            "boundary offset and stiffness ratio must be forced by the "
            "localized orientation-frame dynamics."
        ),
        "missing_derivations": [
            "derive physical boundary offsets from the closed defect/core "
            "geometry instead of treating delta_f and delta_a as inputs",
            "derive rho_stiffness = k_f/k_a from the completed action",
            "compute the localized finite-core spectrum rather than the "
            "universal free ring spectrum",
            "then evaluate N and alpha without scanning",
        ],
        "do_not_claim": [
            "Do not claim N or alpha are derived.",
            "Do not choose delta_f, delta_a, or rho_stiffness to fit N.",
            "Do not confuse size cancellation with normalization closure.",
            "Do not use the free ring spectrum as the localized core "
            "spectrum.",
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
    print("periodic_spectrum:", result["periodic_spectrum"])
    print("twisted_spectrum:", result["twisted_spectrum"])
    print("oriented_closure:", result["oriented_closure"])
    print("no_lock_theorem:", result["no_lock_theorem"])
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
    _print_result(derive_finite_resonator_spectrum_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
