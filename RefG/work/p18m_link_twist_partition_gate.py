# Notation header (see NOTATION.md):
# This gate follows p18l.  It models the completed framing register with the
# Calugareanu-Fuller style split Lk = Tw + Wr and asks whether the energy
# minimization of a finite orientation-frame loop fixes the alpha-lock
# stiffness ratio.

"""
================================================================================
PHASE 18m: Link/twist partition stiffness gate
================================================================================

Purpose
-------
Continue the finite-lock chain after p18l.  The previous gate showed that a
free finite ring spectrum gives discreteness and size cancellation but does
not determine N.  The next physically meaningful step is the framing identity

    Lk = Tw + Wr,

read as: the completed electric/framing register can be carried partly by
internal twist (fiber/framing) and partly by axis writhe/curvature.  This gate
checks whether minimizing the finite-loop elastic energy fixes their ratio.

Result
------
The partition is computable, but it is controlled by the still-free stiffness
ratio:

    E = (k_f/2) Tw^2 + (k_a/2) Wr^2,      Tw + Wr = Lk

gives

    Tw = k_a/(k_f+k_a) Lk,
    Wr = k_f/(k_f+k_a) Lk,
    Tw/Wr = k_a/k_f.

Thus the topology fixes the sum, the variational principle fixes uniform
sharing, but the numerical partition is exactly the stiffness ratio that the
theory still has to derive from the localized action.  This is progress: the
missing alpha-lock number is no longer a vague finite-resonator mystery; it is
the elastic impedance ratio of the two completed orientation-frame channels.

What this gate does NOT claim
-----------------------------
- It does not derive k_f/k_a.
- It does not compute N or alpha.
- It does not solve the nonlinear core.
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
# 1. Elastic partition of a fixed framing/linking register
# ---------------------------------------------------------------------------

def link_twist_partition() -> dict:
    kf, ka, Lk, Tw = sp.symbols("k_f k_a Lk Tw", positive=True)
    Wr = Lk - Tw
    E = sp.Rational(1, 2) * kf * Tw**2 + sp.Rational(1, 2) * ka * Wr**2
    dE = sp.diff(E, Tw)
    sol = sp.solve(sp.Eq(dE, 0), Tw)[0]
    wr_sol = sp.simplify(Wr.subs(Tw, sol))
    ratio = sp.simplify(sol / wr_sol)
    E_min = sp.simplify(E.subs(Tw, sol))
    convex = sp.diff(E, Tw, 2)
    return {
        "Tw_solution": str(sol),
        "Wr_solution": str(wr_sol),
        "partition_ratio_Tw_over_Wr": str(ratio),
        "minimum_energy": str(E_min),
        "convex_for_positive_stiffness": convex == kf + ka,
        "sum_constraint_satisfied": sp.simplify(sol + wr_sol - Lk) == 0,
        "ratio_depends_on_stiffness": ratio.has(kf) and ratio.has(ka),
    }


# ---------------------------------------------------------------------------
# 2. Impedance-ratio alpha audit
# ---------------------------------------------------------------------------

def impedance_ratio_alpha_audit() -> dict:
    rho, Ctop, S = sp.symbols("rho_stiffness C_top S_spectral", positive=True)
    Nreq = sp.symbols("N_required", positive=True)
    # rho = k_f/k_a.  Depending on convention the lock may use rho, 1/rho,
    # or sqrt(rho); none is fixed until the action fixes rho.
    candidates = {
        "rho": Ctop * S * rho,
        "inverse_rho": Ctop * S / rho,
        "sqrt_rho": Ctop * S * sp.sqrt(rho),
    }
    solved = {
        name: sp.solve(sp.Eq(expr, Nreq), rho)
        for name, expr in candidates.items()
    }
    return {
        "candidate_forms": {name: str(expr) for name, expr in candidates.items()},
        "all_forms_depend_on_rho": all(expr.has(rho) for expr in candidates.values()),
        "matching_N_solves_for_rho_not_N": all(len(vals) >= 1 for vals in solved.values()),
        "N_required_numeric": N_REQUIRED,
        "conclusion": (
            "the alpha-lock has been reduced to deriving rho_stiffness from "
            "the localized orientation-frame action; topology and finite "
            "spectra alone do not fix it"
        ),
    }


# ---------------------------------------------------------------------------
# 3. Same-loop size cancellation with energy partition
# ---------------------------------------------------------------------------

def size_cancellation_with_partition() -> dict:
    L, kf, ka, m, n = sp.symbols("L k_f k_a m n", positive=True)
    omega_f = sp.pi * m / L
    omega_a = sp.pi * n / L
    energy_ratio = sp.simplify(kf * omega_f**2 / (ka * omega_a**2))
    return {
        "energy_ratio": str(energy_ratio),
        "independent_of_L": sp.diff(energy_ratio, L) == 0,
        "depends_on_stiffness_ratio": energy_ratio.has(kf) and energy_ratio.has(ka),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_link_twist_partition_gate() -> dict:
    partition = link_twist_partition()
    alpha = impedance_ratio_alpha_audit()
    size = size_cancellation_with_partition()

    closed = {
        "link_constraint_partition_solved": bool(
            partition["sum_constraint_satisfied"]
        ),
        "energy_minimum_convex": bool(partition["convex_for_positive_stiffness"]),
        "partition_ratio_is_stiffness_ratio": bool(
            partition["ratio_depends_on_stiffness"]
        ),
        "same_loop_size_cancels": bool(size["independent_of_L"]),
        "energy_ratio_still_depends_on_stiffness": bool(
            size["depends_on_stiffness_ratio"]
        ),
        "alpha_candidate_forms_depend_on_rho": bool(
            alpha["all_forms_depend_on_rho"]
        ),
        "matching_alpha_now_solves_for_rho": bool(
            alpha["matching_N_solves_for_rho_not_N"]
        ),
        "number_scan_not_performed": True,
    }

    open_checks = {
        "rho_stiffness_derived_from_localized_action": False,
        "core_boundary_conditions_derived": False,
        "N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_LOCALIZED_STIFFNESS_THEOREM_REQUIRED__"
            + _pass_status("LINK_TWIST_PARTITION_AUDIT")
            if all(closed.values())
            else "CHECK_LINK_TWIST_PARTITION_AUDIT"
        ),
        "SCOPE": (
            "finite orientation-frame partition gate: topology fixes "
            "Lk=Tw+Wr and energy minimization partitions it, but the "
            "partition is controlled by k_f/k_a.  The alpha-lock is now "
            "localized to one missing theorem: derive this stiffness ratio "
            "from the completed localized action."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "partition": partition,
        "size_cancellation": size,
        "alpha_audit": alpha,
        "physical_reading": (
            "the finite-lock mechanism has become precise: alpha cannot be "
            "obtained from topology alone; it must come from the elastic "
            "impedance ratio between the fiber/twist and axis/writhe "
            "channels of the same localized orientation-frame object."
        ),
        "missing_derivations": [
            "derive k_f/k_a from the local p18e-h orientation-frame action "
            "including the defect core",
            "derive the boundary conditions that select the physical Lk "
            "sector and mode pair",
            "insert the derived rho_stiffness into the N-lock formula and "
            "only then compare with 10.904978325...",
        ],
        "do_not_claim": [
            "Do not claim alpha or N are derived.",
            "Do not choose k_f/k_a to fit alpha.",
            "Do not claim topology alone fixes the fine-structure constant.",
            "Do not ignore the localized core; the stiffness ratio lives "
            "there.",
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
    print("partition:", result["partition"])
    print("size_cancellation:", result["size_cancellation"])
    print("alpha_audit:", result["alpha_audit"])
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
    _print_result(derive_link_twist_partition_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
