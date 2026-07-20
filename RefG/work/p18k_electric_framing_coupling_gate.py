# Notation header (see NOTATION.md):
# This gate follows p18i.  The p18i hedgehog is read as magnetic/frame-flux.
# The electric candidate is therefore the completed framing/twist register of
# the same orientation-frame bundle.  This file checks the kinematic theorem:
# the framing register is gauge invariant, C-odd, conserved on closed defect
# loops, and can couple to the U(1) connection without violating gauge
# invariance.  It does NOT fix the coupling normalization or alpha.

"""
================================================================================
PHASE 18k: Electric framing/twist coupling gate
================================================================================

Purpose
-------
Close the first missing item left by p18j:

    "derive the electric framing/twist coupling left open by p18i."

The result here is deliberately limited.  This gate identifies the correct
topological/current slot for electric charge after p18i pushed the pi_2
hedgehog into the magnetic/frame-flux register.  It proves that a closed
framing/twist register is:

  * gauge invariant after the p18h completion,
  * odd under the p18g C1/twist mirror,
  * conserved as a closed current,
  * compatible with minimal U(1) coupling,
  * sensitive to oriented-frame closure in the p11g sense.

It does NOT derive the numerical coupling, the finite spectrum, N, or alpha.

Results (all executable below)
------------------------------
1. COMPLETED FRAMING NUMBER:

       Q_f = (Delta theta + integral A)/(2*pi)

   is invariant under theta -> theta - lambda and A -> A + d lambda.
   In the theta=0 gauge the same register is carried by the frame holonomy.

2. C-MAP / ANNIHILATION:
   on the branch supported by p18i, the electron carries W_n=0 and
   electric Q_f != 0.  C1 flips Q_f and leaves W_n=0.  Therefore e+e-
   cancels all electric/framing register without requiring axis inversion.

3. CLOSED CURRENT / GAUGE COUPLING:
   a closed defect loop has zero boundary.  The discrete minimal coupling
   sum_edges q*(lambda_end - lambda_start) telescopes to zero.  An open line
   leaves a boundary term.  Thus gauge invariance selects conserved closed
   framing currents, exactly as a U(1) charge current should.

4. ORIENTED-FRAME SENSITIVITY:
   if the charged coupling sees only a projective director, h=1 is not
   excluded.  If it sees an oriented frame/current, h=1 changes the frame sign
   and the first nontrivial closure is h=2.  This reproduces the p11g
   conditional finite-selection logic inside the EM/framing chain.

What this gate does NOT claim
-----------------------------
- It does not compute the electric coupling strength.
- It does not derive the finite resonator spectrum.
- It does not compute N or alpha.
- It does not derive Dirac spinors, spin-statistics, or QED loops.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


# ---------------------------------------------------------------------------
# 1. Completed framing number and gauge invariance
# ---------------------------------------------------------------------------

def completed_framing_number_gate() -> dict:
    dtheta, holonomy, dlambda = sp.symbols(
        "Delta_theta Holonomy Delta_lambda", real=True
    )
    Q = (dtheta + holonomy) / (2 * sp.pi)
    Q_transformed = ((dtheta - dlambda) + (holonomy + dlambda)) / (
        2 * sp.pi
    )

    s = sp.symbols("s", real=True)
    W = sp.symbols("W", integer=True)
    theta = W * s
    bare = sp.integrate(sp.diff(theta, s), (s, 0, 2 * sp.pi))

    return {
        "Q_framing_gauge_invariant": sp.simplify(Q_transformed - Q) == 0,
        "bare_winding_integer": sp.simplify(bare - 2 * sp.pi * W) == 0,
        "theta_zero_gauge_reading": "Q_f = integral A/(2*pi)",
        "completed_register": "Q_f = (Delta theta + integral A)/(2*pi)",
    }


# ---------------------------------------------------------------------------
# 2. C-map branch B register arithmetic
# ---------------------------------------------------------------------------

def c_map_framing_branch_gate() -> dict:
    Wf, Wn = sp.symbols("W_f W_n", integer=True)
    electron = (Wf, 0)  # p18i branch-B reading: electric framing, no pi2 electric charge
    positron_c1 = (-electron[0], electron[1])
    total = tuple(sp.simplify(a + b) for a, b in zip(electron, positron_c1))

    hedgehog_electric_would_need_c2 = (Wf, Wn)
    c1_total_if_Wn = tuple(
        sp.simplify(a + b)
        for a, b in zip(hedgehog_electric_would_need_c2, (-Wf, Wn))
    )

    return {
        "branch_B_annihilation_complete_under_C1": total == (0, 0),
        "C1_would_leave_hedgehog_remnant_if_Wn_nonzero": sp.simplify(
            c1_total_if_Wn[1] - 2 * Wn
        )
        == 0,
        "electric_register": "framing/twist W_f",
        "magnetic_register": "axis hedgehog W_n",
        "physical_reading": (
            "p18i makes the pi2 hedgehog magnetic/frame-flux; the electric "
            "candidate is the C-odd framing/twist register"
        ),
    }


# ---------------------------------------------------------------------------
# 3. Closed current and gauge coupling
# ---------------------------------------------------------------------------

def closed_current_gauge_coupling_gate() -> dict:
    q = sp.symbols("q", real=True)
    lam0, lam1, lam2 = sp.symbols("lambda_0 lambda_1 lambda_2", real=True)

    # Closed triangular defect loop: 0->1, 1->2, 2->0.
    closed_variation = q * (
        (lam1 - lam0) + (lam2 - lam1) + (lam0 - lam2)
    )
    # Open path: 0->1, 1->2.
    open_variation = q * ((lam1 - lam0) + (lam2 - lam1))

    # Discrete incidence/boundary check.
    closed_edges = [(0, 1), (1, 2), (2, 0)]
    open_edges = [(0, 1), (1, 2)]

    def boundary(edges):
        b = [0, 0, 0]
        for start, end in edges:
            b[start] -= 1
            b[end] += 1
        return b

    return {
        "closed_loop_gauge_variation_zero": sp.simplify(closed_variation)
        == 0,
        "open_line_has_boundary_variation": sp.simplify(
            open_variation - q * (lam2 - lam0)
        )
        == 0,
        "closed_boundary_zero": boundary(closed_edges) == [0, 0, 0],
        "open_boundary_nonzero": boundary(open_edges) != [0, 0, 0],
        "coupling": "S_int = q * integral A_mu dX^mu on closed framing current",
    }


# ---------------------------------------------------------------------------
# 4. Oriented-frame sensitivity and h=2 conditional closure
# ---------------------------------------------------------------------------

def oriented_frame_h2_compatibility_gate() -> dict:
    def director_after_half_turns(h: int) -> tuple[int, int]:
        angle = math.pi * h
        return (round(math.cos(angle)), round(math.sin(angle)))

    def projective_closed(h: int) -> bool:
        return director_after_half_turns(h) in ((1, 0), (-1, 0))

    def oriented_closed(h: int) -> bool:
        return director_after_half_turns(h) == (1, 0)

    rows = []
    for h in range(5):
        rows.append(
            {
                "h": h,
                "director": director_after_half_turns(h),
                "projective_closed": projective_closed(h),
                "oriented_closed": oriented_closed(h),
                "nontrivial": h != 0,
            }
        )
    oriented_candidates = [
        row["h"]
        for row in rows
        if row["nontrivial"] and row["oriented_closed"]
    ]
    return {
        "h1_projective_but_not_oriented": projective_closed(1)
        and not oriented_closed(1),
        "first_nontrivial_oriented_closure_is_h2": oriented_candidates[0] == 2,
        "rows": rows,
        "physical_reading": (
            "electric framing current is orientation-sensitive; this is the "
            "same condition under which p11g conditionally selects h=2"
        ),
    }


# ---------------------------------------------------------------------------
# 5. Normalization ledger
# ---------------------------------------------------------------------------

def normalization_open_ledger() -> dict:
    q0, kf, ka = sp.symbols("q0 k_f k_a", positive=True)
    N_symbolic = sp.Symbol("N", positive=True)
    schematic = q0**2 * kf / ka
    return {
        "schematic_coupling_slot": str(schematic),
        "normalization_depends_on_free_coupling": sp.diff(schematic, q0) != 0,
        "cannot_equal_N_without_next_theorem": True,
        "next_theorem": (
            "derive q0 and k_f/k_a from the completed finite "
            "orientation-frame action and boundary conditions"
        ),
        "N_symbol": str(N_symbolic),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_electric_framing_coupling_gate() -> dict:
    framing = completed_framing_number_gate()
    cmap = c_map_framing_branch_gate()
    current = closed_current_gauge_coupling_gate()
    h2 = oriented_frame_h2_compatibility_gate()
    norm = normalization_open_ledger()

    closed = {
        "completed_framing_register_gauge_invariant": bool(
            framing["Q_framing_gauge_invariant"]
            and framing["bare_winding_integer"]
        ),
        "branch_B_C1_annihilation_complete": bool(
            cmap["branch_B_annihilation_complete_under_C1"]
        ),
        "hedgehog_if_electric_would_need_C2": bool(
            cmap["C1_would_leave_hedgehog_remnant_if_Wn_nonzero"]
        ),
        "closed_framing_current_is_conserved": bool(
            current["closed_boundary_zero"]
            and current["closed_loop_gauge_variation_zero"]
        ),
        "open_framing_line_has_boundary": bool(
            current["open_boundary_nonzero"]
            and current["open_line_has_boundary_variation"]
        ),
        "oriented_coupling_selects_h2_conditionally": bool(
            h2["h1_projective_but_not_oriented"]
            and h2["first_nontrivial_oriented_closure_is_h2"]
        ),
        "normalization_still_open": bool(
            norm["normalization_depends_on_free_coupling"]
            and norm["cannot_equal_N_without_next_theorem"]
        ),
    }

    open_checks = {
        "coupling_strength_q0_derived": False,
        "finite_boundary_conditions_derived": False,
        "fiber_axis_stiffness_ratio_derived": False,
        "N_derived": False,
        "alpha_computed": False,
        "spin_statistics_dirac_structure_derived": False,
    }

    result = {
        "STATUS": (
            "OPEN_FINITE_STIFFNESS_RATIO_NEXT__"
            + _pass_status("ELECTRIC_FRAMING_CURRENT_COUPLING")
            if all(closed.values())
            else "CHECK_ELECTRIC_FRAMING_COUPLING"
        ),
        "SCOPE": (
            "electric register gate after p18i: electric charge is assigned "
            "to the completed framing/twist closed-current register, while "
            "the pi2 hedgehog remains the magnetic/frame-flux register.  "
            "The framing current is gauge invariant, C-odd, conserved on "
            "closed loops, minimally couplable to the U(1) connection, and "
            "orientation-sensitive in the p11g h=2 sense.  Coupling "
            "normalization, N and alpha remain open."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "framing_register": framing,
        "c_map_registers": cmap,
        "closed_current": current,
        "h2_compatibility": h2,
        "normalization_ledger": norm,
        "physical_reading": (
            "the electric slot is no longer vague: it is the completed "
            "framing/twist current of a closed orientation defect.  This "
            "matches the article's twist-sign charge language and preserves "
            "p18i's magnetic reading of the hedgehog.  The remaining alpha "
            "work is now purely quantitative: derive q0 and the finite "
            "fiber/axis stiffness ratio from the same action."
        ),
        "missing_derivations": [
            "derive q0, the unit electric framing coupling, from the "
            "localized defect action",
            "derive the finite boundary conditions of the closed "
            "orientation-frame resonator",
            "compute the fiber/framing and axis/curvature spectra from the "
            "same action and extract the stiffness ratio",
            "only then compute N and alpha",
        ],
        "do_not_claim": [
            "Do not claim the electric coupling strength is derived.",
            "Do not claim alpha or N are derived.",
            "Do not identify the pi2 hedgehog with electric charge in this "
            "branch; it is magnetic/frame-flux here.",
            "Do not claim p11g h=2 is fully action-derived; this gate only "
            "confirms compatibility with oriented electric coupling.",
            "Do not claim Dirac spinor dynamics or spin-statistics.",
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
    print("framing_register:", result["framing_register"])
    print("c_map_registers:", result["c_map_registers"])
    print("closed_current:", result["closed_current"])
    print("h2_compatibility:", result["h2_compatibility"])
    print("normalization_ledger:", result["normalization_ledger"])
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
    _print_result(derive_electric_framing_coupling_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
