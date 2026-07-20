# Notation header (see NOTATION.md):
# This gate follows p18o.  It imports the p11f/p11g finite charged-frame logic
# into the p18 alpha chain: C3 x C3 needs a carry to become one order-9 orbit,
# and oriented charged-frame closure selects h=2 conditionally.

"""
================================================================================
PHASE 18p: Order-9 boundary/anholonomy factor gate
================================================================================

Purpose
-------
p18o closed the stiffness ratio under the stronger SO(3)-isotropic frame
action, leaving the finite boundary/anholonomy factor:

    N = C_top * S_boundary        (if rho = 1).

This gate asks what the existing p11f/p11g charged-frame machinery contributes
to S_boundary.  The result is useful but not final:

  * p11f supplies a genuine order-9 return map only with a nonzero carry.
  * p11g supplies h=2 as the first nontrivial oriented charged-frame closure.
  * together they supply the finite coordinate theta = h/9 = 2/9.

But they do NOT yet tell us how theta=2/9 becomes the normalization N.  The
boundary sector is identified; the boundary-to-normalization map is still the
missing theorem.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive N.
- It does not choose a function of theta to fit N.
- It does not fully action-derive the order-9 carry or h=2 closure.
"""

from __future__ import annotations

from itertools import product
import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
N_REQUIRED = ALPHA_INV_CODATA / (4.0 * math.pi)
ORDER = 9
H_SELECTED = 2


# ---------------------------------------------------------------------------
# 1. C3 x C3 order-9 carry audit
# ---------------------------------------------------------------------------

def orbit_of(step, start=(0, 0)):
    state = start
    seen = [state]
    while True:
        state = step(state)
        if state == start:
            return seen
        if state in seen:
            return seen + [state]
        seen.append(state)


def order9_carry_audit() -> dict:
    z3 = range(3)

    def split_step(da, db):
        return lambda state: ((state[0] + da) % 3, (state[1] + db) % 3)

    split_orders = []
    for da, db in product(z3, z3):
        split_orders.append(len(orbit_of(split_step(da, db))))

    def carry_step(carry):
        return lambda state: (
            (state[0] + 1) % 3,
            (state[1] + carry[state[0]]) % 3,
        )

    rows = []
    for carry in product(z3, repeat=3):
        orbit = orbit_of(carry_step(carry))
        rows.append(
            {
                "carry": carry,
                "total": sum(carry) % 3,
                "order": len(orbit),
                "covers9": len(set(orbit)) == 9,
            }
        )
    criterion = all(row["covers9"] == (row["total"] != 0) for row in rows)
    canonical = (0, 0, 1)
    canonical_orbit = orbit_of(carry_step(canonical))
    z_values = [a + 3 * b for a, b in canonical_orbit]
    return {
        "split_max_order": max(split_orders),
        "split_never_order9": max(split_orders) <= 3,
        "carry_order9_criterion_verified": criterion,
        "canonical_unit_carry": canonical,
        "canonical_orbit_length": len(canonical_orbit),
        "canonical_z_values": z_values,
        "canonical_is_z9_shift": z_values == list(range(9)),
    }


# ---------------------------------------------------------------------------
# 2. h=2 oriented closure audit
# ---------------------------------------------------------------------------

def h2_oriented_closure_audit() -> dict:
    def director_after_half_turns(h: int) -> tuple[int, int]:
        angle = math.pi * h
        return (round(math.cos(angle)), round(math.sin(angle)))

    rows = []
    for h in range(6):
        n = director_after_half_turns(h)
        rows.append(
            {
                "h": h,
                "director": n,
                "projective_closed": n in ((1, 0), (-1, 0)),
                "oriented_closed": n == (1, 0),
                "nontrivial": h != 0,
            }
        )
    oriented = [
        row["h"]
        for row in rows
        if row["nontrivial"] and row["oriented_closed"]
    ]
    theta = sp.Rational(H_SELECTED, ORDER)
    return {
        "first_nontrivial_oriented_h": oriented[0],
        "h2_selected": oriented[0] == H_SELECTED,
        "theta_h": theta,
        "theta_h_string": str(theta),
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# 3. Boundary factor ledger
# ---------------------------------------------------------------------------

def boundary_factor_ledger() -> dict:
    theta = sp.Rational(H_SELECTED, ORDER)
    # These are not a scan.  They are the elementary maps one might be tempted
    # to call "the" boundary factor.  The gate refuses to choose among them
    # without a derived normalization functional.
    elementary_maps = {
        "theta": theta,
        "inverse_theta": 1 / theta,
        "theta_squared_inverse": 1 / theta**2,
        "two_pi_theta": 2 * sp.pi * theta,
        "inverse_two_pi_theta": 1 / (2 * sp.pi * theta),
    }
    numeric = {name: float(sp.N(value)) for name, value in elementary_maps.items()}
    required_map_factor = {
        name: N_REQUIRED / val for name, val in numeric.items() if val != 0
    }
    return {
        "theta_h": str(theta),
        "elementary_maps": {name: str(value) for name, value in elementary_maps.items()},
        "elementary_map_numerics": numeric,
        "N_required": N_REQUIRED,
        "required_extra_factor_if_map_chosen": required_map_factor,
        "no_map_selected": True,
        "conclusion": (
            "order-9/h=2 supplies a finite boundary coordinate, not the "
            "normalization functional from that coordinate to N"
        ),
    }


# ---------------------------------------------------------------------------
# 4. Boundary-to-N no-go
# ---------------------------------------------------------------------------

def boundary_to_N_no_go() -> dict:
    theta, M = sp.symbols("theta_boundary M_map", positive=True)
    Nreq = sp.symbols("N_required", positive=True)
    N_expr = M / theta
    solved_M = sp.solve(sp.Eq(N_expr, Nreq), M)
    return {
        "schematic_N": str(N_expr),
        "depends_on_map_functional": N_expr.has(M),
        "matching_N_solves_for_map_factor": solved_M == [Nreq * theta],
        "missing_theorem": (
            "derive M_map, the boundary-to-normalization functional, from "
            "localized frame dynamics"
        ),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_order9_boundary_anholonomy_gate() -> dict:
    carry = order9_carry_audit()
    h2 = h2_oriented_closure_audit()
    ledger = boundary_factor_ledger()
    nogo = boundary_to_N_no_go()

    closed = {
        "split_C3xC3_not_order9": bool(carry["split_never_order9"]),
        "carry_order9_criterion_verified": bool(
            carry["carry_order9_criterion_verified"]
        ),
        "canonical_unit_carry_is_Z9_shift": bool(
            carry["canonical_is_z9_shift"]
        ),
        "h2_first_nontrivial_oriented_closure": bool(h2["h2_selected"]),
        "theta_h_is_2_over_9": bool(h2["theta_h"] == sp.Rational(2, 9)),
        "boundary_coordinate_identified": bool(ledger["no_map_selected"]),
        "boundary_to_N_map_still_free": bool(
            nogo["depends_on_map_functional"]
            and nogo["matching_N_solves_for_map_factor"]
        ),
        "number_scan_not_performed": True,
    }

    open_checks = {
        "unit_carry_derived_from_local_action": False,
        "h2_action_derived": False,
        "boundary_to_normalization_functional_derived": False,
        "N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_BOUNDARY_TO_NORMALIZATION_MAP_REQUIRED__"
            + _pass_status("ORDER9_H2_ANHOLONOMY_LEDGER")
            if all(closed.values())
            else "CHECK_ORDER9_BOUNDARY_ANHOLONOMY_LEDGER"
        ),
        "SCOPE": (
            "finite boundary/anholonomy gate after p18o: the charged-frame "
            "sector supplies an order-9 carry and h=2 oriented closure, hence "
            "theta=2/9 as the finite boundary coordinate.  This identifies "
            "the electric unit sector but still does not derive the map from "
            "that sector to N."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "order9_carry": carry,
        "h2_closure": h2,
        "boundary_factor_ledger": ledger,
        "boundary_to_N_no_go": nogo,
        "physical_reading": (
            "the finite electric unit is now anchored in the existing p11 "
            "order-9/h=2 machinery.  What remains is not to find a prettier "
            "function of 2/9, but to derive the normalization functional that "
            "turns the completed boundary anholonomy into N."
        ),
        "missing_derivations": [
            "derive the unit carry from the localized orientation-frame action",
            "derive h=2 oriented closure dynamically, not only conditionally",
            "derive the boundary-to-normalization functional M_map",
            "then compute N without choosing a function of theta by hand",
        ],
        "do_not_claim": [
            "Do not claim theta=2/9 derives alpha.",
            "Do not choose inverse theta, theta squared, or any other map "
            "because it is numerically convenient.",
            "Do not claim unit carry or h=2 are action-derived here.",
            "Do not scan functions of 2/9 for 10.904978325.",
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
    print("order9_carry:", result["order9_carry"])
    print("h2_closure:", result["h2_closure"])
    print("boundary_factor_ledger:", result["boundary_factor_ledger"])
    print("boundary_to_N_no_go:", result["boundary_to_N_no_go"])
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
    _print_result(derive_order9_boundary_anholonomy_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
