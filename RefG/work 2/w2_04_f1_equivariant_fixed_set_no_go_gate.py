"""Equivariant ერთმნიშვნელოვანი კანონის fixed-set no-go.

თუ F:X→X არის G-ეკვივარიანტული, მაშინ G-ის მიერ ფიქსირებული მდგომარეობა
კვლავ ფიქსირებულ სიმრავლეში გადადის. ეს არის პირობითი მათემატიკური საზღვარი
და არა RefG-ის ფიზიკური თვითგარჩევის გამოყვანა.
"""
from __future__ import annotations

import itertools
import json
import sys
from typing import Any, Callable


MODEL_VERSION = "W2-F1-EQUIVARIANT-FIXED-SET-NO-GO-v1.7-internal"

SCIENTIFIC_CLAIM: dict[str, Any] = {
    "theorem": (
        "თუ G მოქმედებს X-ზე, F:X→X ერთმნიშვნელოვანია და F(g·x)=g·F(x), "
        "მაშინ F(Fix(G))⊆Fix(G). ამიტომ ზუსტად სიმეტრიული x0 ასეთი კანონით "
        "არასიმეტრიულ ტოტს ვერ ირჩევს."
    ),
    "variational_corollary": (
        "G-ინვარიანტული ფუნქციონალის ერთადერთი გლობალური მინიმიზატორი "
        "G-ის მიერ ფიქსირებულია."
    ),
    "assumptions": [
        "G არის ჯგუფი და მისი მოქმედება X-ზე კარგადაა განსაზღვრული.",
        "F არის სრული, ერთმნიშვნელოვანი რუკა X→X.",
        "F(g·x)=g·F(x) ყოველი g და x-ისთვის.",
        "საწყისი x0 ეკუთვნის Fix(G)-ს.",
        "ვარიაციულ corollary-ში ფუნქციონალი G-ინვარიანტულია და მინიმიზატორი ერთადერთია.",
    ],
    "proof": [
        "x0∈Fix(G), ამიტომ g·x0=x0.",
        "ეკვივარიანტობით g·F(x0)=F(g·x0).",
        "აქედან g·F(x0)=F(x0), ამიტომ F(x0)∈Fix(G).",
        "ინდუქციით ყველა iteration Fix(G)-ში რჩება.",
    ],
    "independent_stabilizer_proof": [
        "h∈Stab(x) ⇒ h·x=x.",
        "ეკვივარიანტობით h·F(x)=F(h·x)=F(x).",
        "ამიტომ Stab(x)⊆Stab(F(x)); Stab(x)=G-ისას F(x) ფიქსირებულია.",
    ],
    "scope": (
        "ნებისმიერი ჯგუფური მოქმედება და ერთმნიშვნელოვანი equivariant map. "
        "ფიზიკური სივრცე, დრო, მეტრიკა და კონკრეტული RefG კანონი აქ არ განისაზღვრება."
    ),
    "falsifier": (
        "კონკრეტული G, მოქმედება, x0∈Fix(G) და ერთმნიშვნელოვანი equivariant F, "
        "რომლისთვის F(x0)∉Fix(G)."
    ),
    "open_boundaries": [
        "არაერთმნიშვნელოვანი ან set-valued წესი",
        "სტოქასტიკური ან კვანტური branch outcome",
        "არასიმეტრიული seed ან boundary",
        "state-space-changing კანონი",
        "დეგენერირებული ინვარიანტული მინიმუმების არჩევის მექანიზმი",
        "ფიზიკური W2_F1 realization",
    ],
}


def fixed_set(
    action: Callable[[int], int], states: tuple[int, ...]
) -> set[int]:
    return {state for state in states if action(state) == state}


def equivariant_maps(
    states: tuple[int, ...], action: Callable[[int], int]
) -> list[dict[int, int]]:
    maps: list[dict[int, int]] = []
    for values in itertools.product(states, repeat=len(states)):
        candidate = dict(zip(states, values))
        if all(
            candidate[action(state)] == action(candidate[state])
            for state in states
        ):
            maps.append(candidate)
    return maps


def invariant_energies(
    states: tuple[int, ...], action: Callable[[int], int]
) -> list[dict[int, int]]:
    energies: list[dict[int, int]] = []
    for values in itertools.product(range(3), repeat=len(states)):
        energy = dict(zip(states, values))
        if all(energy[action(state)] == energy[state] for state in states):
            energies.append(energy)
    return energies


def c2_stabilizer(
    action: Callable[[int], int], state: int
) -> frozenset[int]:
    return frozenset({0, 1}) if action(state) == state else frozenset({0})


def stabilizer_inclusion_holds(
    states: tuple[int, ...],
    action: Callable[[int], int],
    maps: list[dict[int, int]],
) -> bool:
    return all(
        c2_stabilizer(action, state).issubset(
            c2_stabilizer(action, candidate[state])
        )
        for candidate in maps
        for state in states
    )


def run_gate() -> dict[str, Any]:
    states_3 = (0, 1, 2)
    swap_3 = {0: 0, 1: 2, 2: 1}.__getitem__
    fix_3 = fixed_set(swap_3, states_3)
    maps_3 = equivariant_maps(states_3, swap_3)
    action_3_valid = all(
        swap_3(swap_3(state)) == state and swap_3(state) in states_3
        for state in states_3
    )
    finite_3 = (
        len(maps_3) == 3
        and all(
            candidate[state] in fix_3
            for candidate in maps_3
            for state in fix_3
        )
    )

    states_4 = (0, 1, 2, 3)
    swap_4 = {0: 0, 1: 1, 2: 3, 3: 2}.__getitem__
    fix_4 = fixed_set(swap_4, states_4)
    maps_4 = equivariant_maps(states_4, swap_4)
    action_4_valid = all(
        swap_4(swap_4(state)) == state and swap_4(state) in states_4
        for state in states_4
    )
    finite_4 = (
        len(maps_4) == 16
        and all(
            candidate[state] in fix_4
            for candidate in maps_4
            for state in fix_4
        )
    )

    stabilizer_crosscheck = all((
        stabilizer_inclusion_holds(states_3, swap_3, maps_3),
        stabilizer_inclusion_holds(states_4, swap_4, maps_4),
    ))

    unique_minimizers: list[int] = []
    for energy in invariant_energies(states_3, swap_3):
        minimum = min(energy.values())
        minimizers = {
            state for state in states_3 if energy[state] == minimum
        }
        if len(minimizers) == 1:
            unique_minimizers.append(next(iter(minimizers)))
    unique_invariant_minimum_fixed = (
        bool(unique_minimizers) and set(unique_minimizers).issubset(fix_3)
    )

    degenerate_energy = {0: 1, 1: 0, 2: 0}
    degenerate_minima = {
        state for state in states_3 if degenerate_energy[state] == 0
    }
    degenerate_escape_remains_open = (
        degenerate_minima == {1, 2}
        and all(
            degenerate_energy[swap_3(state)] == degenerate_energy[state]
            for state in states_3
        )
    )

    non_equivariant = {0: 1, 1: 1, 2: 2}
    non_equivariant_escape_detected = (
        non_equivariant[0] not in fix_3
        and any(
            non_equivariant[swap_3(state)]
            != swap_3(non_equivariant[state])
            for state in states_3
        )
    )

    checks = {
        "C2_three_state_action_valid": action_3_valid,
        "C2_four_state_action_valid": action_4_valid,
        "three_state_equivariant_maps_preserve_fixed_set": finite_3,
        "four_state_equivariant_maps_preserve_fixed_set": finite_4,
        "independent_stabilizer_inclusion_crosscheck": stabilizer_crosscheck,
        "unique_invariant_minimum_is_fixed": unique_invariant_minimum_fixed,
        "degenerate_nonfixed_minimum_orbit_is_an_open_escape": degenerate_escape_remains_open,
        "non_equivariant_escape_violates_the_assumption": non_equivariant_escape_detected,
    }
    passed = all(checks.values())
    return {
        "model_version": MODEL_VERSION,
        "status": (
            "CONDITIONAL_EXACT_FIXED_SET_THEOREM_PASS__INTERNAL__W2_F1_OPEN"
            if passed
            else "EQUIVARIANT_FIXED_SET_NO_GO_FAIL"
        ),
        "claim": SCIENTIFIC_CLAIM,
        "checks": checks,
        "diagnostics": {
            "three_state_fixed_set": sorted(fix_3),
            "three_state_equivariant_map_count": len(maps_3),
            "four_state_fixed_set": sorted(fix_4),
            "four_state_equivariant_map_count": len(maps_4),
            "unique_invariant_minimizers_seen": unique_minimizers,
            "degenerate_nonfixed_minima": sorted(degenerate_minima),
        },
        "theory_consequence": (
            "ზუსტად სიმეტრიული x0-ის ერთმნიშვნელოვანი equivariant განახლება "
            "არასიმეტრიულ ტოტს ვერ ირჩევს; საჭიროა ერთ-ერთი ღიად გამოცხადებული "
            "escape ინგრედიენტი."
        ),
        "equivariant_fixed_set_no_go_pass": passed,
        "refg_W2_F1_closed": False,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["equivariant_fixed_set_no_go_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
