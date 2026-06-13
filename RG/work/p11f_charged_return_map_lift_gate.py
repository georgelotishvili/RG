# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: particle-sector finite return maps only.

"""PHASE 48 (p11f): charged return-map gate for the order-9 lift.

Purpose
-------
The charged-lepton route uses a 9-slot lattice

    C3(axis) x C3(phase/braid).

But C3 x C3 is not Z9.  A true order-9 reduced coordinate needs a
charged-defect return map that visits all nine slots as one orbit.

This file closes the finite combinatorial part:

1. Any split product return map on C3 x C3 has order at most 3.
2. A skew/carry return map

       (a, b) -> (a + 1, b + c(a))   mod 3

   visits all nine slots iff the total carry c(0)+c(1)+c(2) is nonzero
   mod 3.
3. A unit carry, for example c=(0,0,1), is exactly the odometer lift:

       z = a + 3 b,     z -> z + 1 mod 9.

What remains open is the physical theorem: derive this nonzero unit braid
anholonomy per full oriented axis cycle from the charged defect field
equations.  Until that is done, RG may say "conditional order-9 lift
candidate", not "derived Z9 holonomy".
"""

from __future__ import annotations

from itertools import product
from typing import Callable, Iterable, Sequence


State = tuple[int, int]

Z3 = range(3)
LATTICE_SIZE = 9
CANONICAL_UNIT_CARRY = (0, 0, 1)


def orbit_of(step: Callable[[State], State], start: State = (0, 0)) -> list[State]:
    """Return the closed orbit of start under a finite return map."""
    state = start
    seen = [state]
    while True:
        state = step(state)
        if state == start:
            return seen
        if state in seen:
            # A non-start repeat should not occur for bijective maps here, but
            # keeping it explicit makes the diagnostic robust.
            return seen + [state]
        seen.append(state)


def orbit_order(step: Callable[[State], State], start: State = (0, 0)) -> int:
    return len(orbit_of(step, start))


def covers_all_slots(orbit: Iterable[State]) -> bool:
    return len(set(orbit)) == LATTICE_SIZE


def split_step(delta_axis: int, delta_phase: int) -> Callable[[State], State]:
    """Independent C3 rotations: no carry between the two factors."""
    return lambda state: (
        (state[0] + delta_axis) % 3,
        (state[1] + delta_phase) % 3,
    )


def split_return_map_audit() -> dict[str, object]:
    rows = []
    for delta_axis, delta_phase in product(Z3, Z3):
        step = split_step(delta_axis, delta_phase)
        orbit = orbit_of(step)
        rows.append(
            {
                "delta_axis": delta_axis,
                "delta_phase": delta_phase,
                "order": len(orbit),
                "covers_all_slots": covers_all_slots(orbit),
            }
        )
    return {
        "maps_checked": len(rows),
        "max_order": max(row["order"] for row in rows),
        "any_single_9_orbit": any(row["covers_all_slots"] for row in rows),
        "rows": rows,
        "conclusion": (
            "split C3 x C3 return maps never produce one order-9 orbit; "
            "the direct product is only a 9-slot dictionary"
        ),
    }


def carry_step(carry: Sequence[int]) -> Callable[[State], State]:
    """Skew return map with phase/braid carry tied to the old axis slot."""
    if len(carry) != 3:
        raise ValueError("carry must contain exactly three Z3 entries")
    return lambda state: (
        (state[0] + 1) % 3,
        (state[1] + carry[state[0]]) % 3,
    )


def total_carry_mod3(carry: Sequence[int]) -> int:
    return sum(carry) % 3


def carry_return_map_audit() -> dict[str, object]:
    rows = []
    for carry in product(Z3, repeat=3):
        orbit = orbit_of(carry_step(carry))
        total = total_carry_mod3(carry)
        rows.append(
            {
                "carry": carry,
                "total_carry_mod3": total,
                "order": len(orbit),
                "covers_all_slots": covers_all_slots(orbit),
            }
        )
    criterion_ok = all(
        row["covers_all_slots"] == (row["total_carry_mod3"] != 0)
        for row in rows
    )
    return {
        "maps_checked": len(rows),
        "criterion": "single order-9 orbit iff total_carry_mod3 != 0",
        "criterion_verified": criterion_ok,
        "orders_by_total_carry": {
            total: sorted(
                {row["order"] for row in rows if row["total_carry_mod3"] == total}
            )
            for total in Z3
        },
        "single_9_orbit_count": sum(row["covers_all_slots"] for row in rows),
        "rows": rows,
        "physical_reading": (
            "a nonzero total carry is the finite-map signature of braid "
            "anholonomy accumulated during one oriented axis cycle"
        ),
    }


def canonical_unit_carry_lift() -> dict[str, object]:
    """Canonical unit-carry lift, conjugate to z -> z+1 on Z9."""
    orbit = orbit_of(carry_step(CANONICAL_UNIT_CARRY))
    z_values = [axis + 3 * phase for axis, phase in orbit]
    expected = list(range(9))
    return {
        "carry": CANONICAL_UNIT_CARRY,
        "orbit": orbit,
        "z_coordinate": "z = axis + 3*phase",
        "z_values": z_values,
        "z_plus_one_residuals_mod9": [
            (z_values[(i + 1) % len(z_values)] - z_values[i] - 1) % 9
            for i in range(len(z_values))
        ],
        "is_exact_z9_shift": z_values == expected,
        "orientation_reversed_unit": "total_carry_mod3=2 gives the inverse orientation class",
    }


def charged_return_map_lift_gate() -> dict[str, object]:
    split = split_return_map_audit()
    carry = carry_return_map_audit()
    canonical = canonical_unit_carry_lift()

    math_closed = (
        split["max_order"] == 3
        and not split["any_single_9_orbit"]
        and carry["criterion_verified"]
        and canonical["is_exact_z9_shift"]
    )

    return {
        "status": (
            "PASS_MATH_ORDER9_LIFT_CRITERION__PHYSICAL_ANHOLONOMY_OPEN"
            if math_closed
            else "CHECK_RETURN_MAP_LIFT"
        ),
        "slot_lattice": "C3(axis) x C3(phase/braid)",
        "split_product_result": split["conclusion"],
        "carry_lift_result": carry["criterion"],
        "canonical_unit_lift": "c=(0,0,1) gives z=a+3b -> z+1 mod 9",
        "math_result_closed": math_closed,
        "physical_theorem_open": (
            "derive nonzero unit braid anholonomy per full oriented axis cycle "
            "from the charged defect field equations"
        ),
        "allowed_language": "conditional non-split order-9 lift candidate",
        "forbidden_language": "derived Z9 holonomy before the field-equation anholonomy theorem",
        "do_not_claim": [
            "Do not call C3 x C3 itself Z9.",
            "Do not claim theta=2/9 is derived until the unit-anholonomy theorem is derived.",
            "Do not treat the carry function as a fitted mass parameter; it must come from charged defect transport.",
            "Do not identify the inverse carry orientation with antiparticles without a charge-current theorem.",
        ],
    }


def main() -> None:
    gate = charged_return_map_lift_gate()
    print("PHASE 48: charged return-map order-9 lift gate")
    print(f"status: {gate['status']}")
    print(f"split: {gate['split_product_result']}")
    print(f"carry: {gate['carry_lift_result']}")
    print(f"canonical: {gate['canonical_unit_lift']}")
    print(f"open: {gate['physical_theorem_open']}")


if __name__ == "__main__":
    main()
