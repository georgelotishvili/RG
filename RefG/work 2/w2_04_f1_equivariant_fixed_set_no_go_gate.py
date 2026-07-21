"""W2-F1 exact no-go for a symmetric state under an equivariant single-valued law.

The theorem is representation-independent: an equivariant map sends the fixed
set of a group action into itself. Therefore an exactly symmetric state cannot
select a non-invariant branch without an additional ingredient. This is a
conditional mathematical boundary, not a physical RefG derivation.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path
from typing import Any, Callable


MODEL_VERSION = "W2-F1-EQUIVARIANT-FIXED-SET-NO-GO-v1.7-internal"
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"
ROUTE_CONTRACT = "W2-F1-SOURCE-ALIGNED-ROUTE-CONTRACT-v1.8-internal"
UNIVERSAL_GATES = frozenset({
    "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
    "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
    "G7_OBSERVATION", "G8_EXPORT",
})

REQUIRED_FIELDS = {
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "GATE_APPLICABILITY", "CROSSCHECK", "PROVENANCE", "FILES",
}

INITIAL_CLOSURE_FLAGS = {
    "G0_GOAL": False,
    "G1_CONVENTIONS": False,
    "G2_CORE_ALGEBRA": False,
    "G3_STRUCTURE": False,
    "G4_INDEPENDENT_CHECK": False,
    "G5_LIMITS_REGRESSION": False,
    "G6_PHYSICAL_MATCH": False,
    "G7_OBSERVATION": False,
    "G8_EXPORT": False,
    "EQUIVARIANT_FIXED_SET_NO_GO": False,
    "W2_F1_SELF_DIFFERENTIATION": False,
    "W2_F2_OPERATIONAL_RELATIONS": False,
    "W2_F3_INTERNAL_ORDER_CAUSALITY": False,
    "W2_F4_INDEPENDENT_ADDITIVE_MODES": False,
}

GATE_APPLICABILITY = {
    "G0_GOAL": "REQUIRED — theorem, assumptions, domain and falsifier are fixed",
    "G1_CONVENTIONS": "REQUIRED — G_sym action, Fix(G_sym), total map and iteration role",
    "G2_CORE_ALGEBRA": "REQUIRED — direct equivariance equality proof",
    "G3_STRUCTURE": "REQUIRED — fixed-set invariance and unique-minimum corollary",
    "G4_INDEPENDENT_CHECK": "REQUIRED — independent stabilizer-inclusion derivation; finite enumerations remain controls",
    "G5_LIMITS_REGRESSION": "REQUIRED — finite fixed-set, degenerate-minimum and non-equivariant controls",
    "G6_PHYSICAL_MATCH": "N/A — no physical source, energy ledger or observable map",
    "G7_OBSERVATION": "N/A — no data or prediction",
    "G8_EXPORT": "N/A — internal Git-ignored lemma; no export authorized",
}
EXPECTED_CLOSURE_KEYS = frozenset(INITIAL_CLOSURE_FLAGS)
EXPECTED_GATE_APPLICABILITY = dict(GATE_APPLICABILITY)
EXPECTED_BRANCHES = {
    "exact_symmetric_single_valued_equivariant": "no-go",
    "degenerate_invariant_minima": "escape class; selection mechanism OPEN",
    "generic_symmetry_neutral_seed_ensemble": "escape class; seed origin OPEN",
    "stochastic_or_quantum_outcomes": "escape class; physical rule OPEN",
    "explicit_symmetry_breaking": "allowed mathematically but rejected if desired outcome is prewired",
}

CLAIM_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F1_EQUIVARIANT_FIXED_SET_NO_GO_001",
    "CLAIM": (
        "თუ G_sym მოქმედებს X-ზე, F:X->X ერთმნიშვნელოვანია და G_sym-ეკვივარიანტულია, "
        "მაშინ G_sym-ის ფიქსირებული სიმრავლე F-ის მიმართ ინვარიანტულია. ამიტომ ზუსტად "
        "სიმეტრიული საწყისი მდგომარეობა ასეთი კანონით არასიმეტრიულ ტოტს ვერ ირჩევს. "
        "ასევე, G_sym-ინვარიანტული ფუნქციონალის ერთადერთი გლობალური მინიმიზატორი G_sym-ის მიერ ფიქსირებულია."
    ),
    "TYPE": "CONDITIONAL / EXACT_IDENTITY (group-action no-go); არა MECHANISM_DERIVED",
    "MODEL_VERSION": f"{MODEL_VERSION}; theorem assumptions, scope or PASS-logic changes require a new version",
    "ASSUMPTIONS": [
        "G_sym არის ჯგუფი და მისი მოქმედება X-ზე კარგად განსაზღვრულია.",
        "F არის ერთმნიშვნელოვანი სრული რუკა X->X.",
        "F(g.x)=g.F(x) ყოველი g და x-ისთვის.",
        "საწყისი x0 ფიქსირებულია: g.x0=x0 ყოველი g-სთვის.",
        "ვარიაციულ corollary-ში ფუნქციონალი G_sym-ინვარიანტულია და მინიმიზატორი ერთადერთია.",
    ],
    "DOMAIN": "ნებისმიერი ჯგუფური მოქმედება და ერთმნიშვნელოვანი equivariant map; ფიზიკური დრო, სივრცე და მეტრიკა N/A.",
    "CONVENTIONS": "G_sym არის მათემატიკური სიმეტრიის ჯგუფი და არა Newton-ის G; Fix(G_sym)={x | g.x=x ყველა g-სთვის}; პროგრამული iteration ფიზიკურ დროს არ ნიშნავს.",
    "FREEDOM_LEDGER": {
        "X": {"source": "theorem domain", "range": "arbitrary G_sym-set", "scale": "universal", "complexity": "unrestricted"},
        "G_sym": {"source": "theorem domain", "range": "arbitrary group", "scale": "universal", "complexity": "unrestricted"},
        "group_action_alpha": {"source": "theorem domain", "range": "G_sym action on X", "scale": "universal", "complexity": "unrestricted"},
        "F": {"source": "theorem domain", "range": "single-valued equivariant maps", "scale": "universal", "complexity": "unrestricted"},
        "x0": {"source": "theorem assumption", "range": "Fix(G_sym)", "scale": "object", "complexity": 1},
        "invariant_functional": {"source": "variational corollary only", "range": "G_sym-invariant map to an ordered codomain", "scale": "universal", "complexity": "unrestricted"},
        "unique_minimum": {"source": "variational corollary assumption", "range": "true/false", "scale": "branch", "complexity": 1},
        "finite_controls": {"source": "diagnostic only", "range": "C2 actions on 3 and 4 states", "scale": "test", "complexity": "3^3 and 4^4 maps"},
        "data_fitted_parameters": {"source": "N/A", "range": 0, "scale": "data", "complexity": 0},
    },
    "DEPENDENCIES": [
        f"{PROGRAM_CONTRACT}: program boundary only",
        f"{ROUTE_CONTRACT}: candidate routes and input/output boundary only",
    ],
    "METHOD": "ერთი ხაზის ჯგუფური იგივეობა, ინდუქციური iteration, ვარიაციული uniqueness corollary და ორი სასრული სრული ჩამოთვლა.",
    "PASS_CONDITION": [
        "g.F(x0)=F(g.x0)=F(x0) exact chain holds.",
        "ყველა iteration Fix(G_sym)-ში რჩება.",
        "G_sym-ინვარიანტული ფუნქციონალის unique minimizer ფიქსირებულია.",
        "C2-ის 3-state და 4-state exhaustive controls fixed set-ს ინარჩუნებს.",
        "არაეკვივარიანტული negative control არასიმეტრიულ გადასვლას მხოლოდ დაშვების დარღვევით ქმნის.",
    ],
    "FAIL_CONDITION": "იმავე დაშვებებით მოიძებნება x0 in Fix(G_sym), რომლისთვის F(x0) not in Fix(G_sym).",
    "FALSIFIER": "კონკრეტული ჯგუფი, მოქმედება და ერთმნიშვნელოვანი equivariant F, რომელიც fixed-set invariance-ს არღვევს.",
    "RESIDUAL": "აბსტრაქტულად equality predicate g.F(x0)=F(x0); სასრულ კონტროლებში დარღვევათა რაოდენობა 0.",
    "ERROR_BOUND": "0 — ზუსტი ლოგიკა და სრული სასრული ჩამოთვლა.",
    "VALIDITY_HEALTH": (
        "no-go არ ვრცელდება არაერთმნიშვნელოვან წესზე, სტოქასტიკურ branch outcome-ზე, "
        "არასიმეტრიულ seed-ზე, symmetry-changing state-space law-ზე ან დეგენერირებული/"
        "set-valued ატემპორალური ამონახსნების არჩევაზე. ერთმნიშვნელოვან equivariant "
        "ატემპორალურ selector-ზე no-go კვლავ ვრცელდება."
    ),
    "BRANCHES": dict(EXPECTED_BRANCHES),
    "OBSERVABLE_MAP": "N/A — theorem concerns internal symmetry only.",
    "FORWARD_MODEL": "N/A — no physical observable or dataset.",
    "DATA_ROLE": "N/A — no data used.",
    "IDENTIFIABILITY": "Exact predicate: membership in Fix(G_sym); tolerance 0.",
    "BENCHMARK": "C2 swap action with one and two fixed states; non-equivariant transition; degenerate invariant minima.",
    "CLOSURE_FLAGS": dict(INITIAL_CLOSURE_FLAGS),
    "GATE_APPLICABILITY": dict(GATE_APPLICABILITY),
    "CROSSCHECK": "Second universal derivation uses Stab(x) subset Stab(F(x)); finite enumerations and invariant-energy examples remain controls.",
    "PROVENANCE": "runtime SHA-256 of CODES, Canon, intuitive source, W2-C0, route contract and this source",
    "FILES": [
        "CODES.md", "Theory_Canon.md", "intuitive/RefG_GE.md",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_03_f1_source_aligned_route_contract.py",
        "RefG/work 2/w2_04_f1_equivariant_fixed_set_no_go_gate.py",
    ],
}


def fixed_set(action: Callable[[int], int], states: tuple[int, ...]) -> set[int]:
    return {x for x in states if action(x) == x}


def equivariant_maps(states: tuple[int, ...], action: Callable[[int], int]) -> list[dict[int, int]]:
    maps: list[dict[int, int]] = []
    for values in itertools.product(states, repeat=len(states)):
        f = dict(zip(states, values))
        if all(f[action(x)] == action(f[x]) for x in states):
            maps.append(f)
    return maps


def invariant_energies(states: tuple[int, ...], action: Callable[[int], int]) -> list[dict[int, int]]:
    out: list[dict[int, int]] = []
    for values in itertools.product(range(3), repeat=len(states)):
        energy = dict(zip(states, values))
        if all(energy[action(x)] == energy[x] for x in states):
            out.append(energy)
    return out


def c2_stabilizer(action: Callable[[int], int], x: int) -> frozenset[int]:
    """C2 elements: 0 is identity and 1 is the declared involution."""
    return frozenset({0, 1}) if action(x) == x else frozenset({0})


def exhaustive_stabilizer_inclusion(
    states: tuple[int, ...],
    action: Callable[[int], int],
    maps: list[dict[int, int]],
) -> bool:
    return all(
        c2_stabilizer(action, x).issubset(c2_stabilizer(action, f[x]))
        for f in maps
        for x in states
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freedom_ledger_schema_valid(ledger: Any) -> bool:
    required = {"source", "range", "scale", "complexity"}
    return isinstance(ledger, dict) and bool(ledger) and all(
        isinstance(entry, dict)
        and set(entry) == required
        and all(
            value is not None
            and (not isinstance(value, str) or bool(value.strip()))
            for value in entry.values()
        )
        for entry in ledger.values()
    )


def load_gate_report(path: Path, module_name: str) -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_gate()


def run_gate() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    paths = {
        "CODES": root / "CODES.md",
        "CANON": root / "Theory_Canon.md",
        "INTUITIVE": root / "intuitive" / "RefG_GE.md",
        "W2_C0": root / "RefG" / "work 2" / "w2_00_foundation_to_einstein_contract.md",
        "W2_03": root / "RefG" / "work 2" / "w2_03_f1_source_aligned_route_contract.py",
        "SOURCE": Path(__file__).resolve(),
    }
    route_report = load_gate_report(paths["W2_03"], "w2_03_route_dependency")
    route_dependency_pass = (
        route_report.get("STATUS") == "ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_G1_AND_PHYSICAL_F1_OPEN"
        and route_report.get("MODEL_VERSION") == ROUTE_CONTRACT
        and route_report.get("CLOSURE_FLAGS", {}).get("G0_GOAL") is True
        and route_report.get("CLOSURE_FLAGS", {}).get("W2_F1_SELF_DIFFERENTIATION") is False
    )
    x3 = (0, 1, 2)
    swap3 = {0: 0, 1: 2, 2: 1}.__getitem__
    fix3 = fixed_set(swap3, x3)
    c2_action3_pass = all(swap3(swap3(x)) == x and swap3(x) in x3 for x in x3)
    maps3 = equivariant_maps(x3, swap3)
    finite3_pass = len(maps3) == 3 and all(f[x] in fix3 for f in maps3 for x in fix3)

    x4 = (0, 1, 2, 3)
    swap4 = {0: 0, 1: 1, 2: 3, 3: 2}.__getitem__
    fix4 = fixed_set(swap4, x4)
    c2_action4_pass = all(swap4(swap4(x)) == x and swap4(x) in x4 for x in x4)
    maps4 = equivariant_maps(x4, swap4)
    finite4_pass = len(maps4) == 16 and all(f[x] in fix4 for f in maps4 for x in fix4)

    energies = invariant_energies(x3, swap3)
    unique_minima = []
    for energy in energies:
        minimum = min(energy.values())
        minimizers = {x for x in x3 if energy[x] == minimum}
        if len(minimizers) == 1:
            unique_minima.append(next(iter(minimizers)))
    variational_pass = bool(unique_minima) and set(unique_minima).issubset(fix3)

    degenerate_energy = {0: 1, 1: 0, 2: 0}
    degenerate_minima = {x for x in x3 if degenerate_energy[x] == 0}
    degenerate_control = degenerate_minima == {1, 2} and all(
        degenerate_energy[swap3(x)] == degenerate_energy[x] for x in x3
    )

    non_equivariant = {0: 1, 1: 1, 2: 2}
    negative_control = (
        non_equivariant[0] not in fix3
        and any(non_equivariant[swap3(x)] != swap3(non_equivariant[x]) for x in x3)
    )

    full_contract = REQUIRED_FIELDS.issubset(CLAIM_CONTRACT)
    contract_values_nonempty = all(
        value.strip() if isinstance(value, str) else bool(value)
        for value in (CLAIM_CONTRACT.get(key) for key in REQUIRED_FIELDS)
    )
    text_sequences_valid = all(
        isinstance(CLAIM_CONTRACT.get(key), (list, tuple))
        and bool(CLAIM_CONTRACT[key])
        and all(isinstance(item, str) and item.strip() for item in CLAIM_CONTRACT[key])
        for key in ("ASSUMPTIONS", "DEPENDENCIES", "PASS_CONDITION", "FILES")
    )
    version_contract_bound = (
        isinstance(CLAIM_CONTRACT.get("MODEL_VERSION"), str)
        and CLAIM_CONTRACT["MODEL_VERSION"].startswith(f"{MODEL_VERSION};")
    )
    gate_applicability_complete = (
        set(GATE_APPLICABILITY) == UNIVERSAL_GATES
        and all(isinstance(value, str) and value.strip() for value in GATE_APPLICABILITY.values())
    )
    contract_registries_bound = (
        GATE_APPLICABILITY == EXPECTED_GATE_APPLICABILITY
        and CLAIM_CONTRACT.get("GATE_APPLICABILITY") == EXPECTED_GATE_APPLICABILITY
        and set(INITIAL_CLOSURE_FLAGS) == EXPECTED_CLOSURE_KEYS
        and not any(INITIAL_CLOSURE_FLAGS.values())
        and set(CLAIM_CONTRACT.get("CLOSURE_FLAGS", {})) == EXPECTED_CLOSURE_KEYS
        and not any(CLAIM_CONTRACT.get("CLOSURE_FLAGS", {}).values())
    )
    freedom_schema_complete = freedom_ledger_schema_valid(CLAIM_CONTRACT.get("FREEDOM_LEDGER"))
    branch_registry_exact = CLAIM_CONTRACT.get("BRANCHES") == EXPECTED_BRANCHES
    required_freedoms = {
        "X", "G_sym", "group_action_alpha", "F", "x0",
        "invariant_functional", "unique_minimum", "finite_controls",
        "data_fitted_parameters",
    }
    conventions_complete = (
        set(CLAIM_CONTRACT["FREEDOM_LEDGER"]) == required_freedoms
        and "Newton" in CLAIM_CONTRACT["CONVENTIONS"]
        and "ფიზიკურ დროს არ ნიშნავს" in CLAIM_CONTRACT["CONVENTIONS"]
    )
    direct_proof_declared = (
        any("F(g.x)=g.F(x)" in item for item in CLAIM_CONTRACT["ASSUMPTIONS"])
        and any("g.F(x0)=F(g.x0)=F(x0)" in item for item in CLAIM_CONTRACT["PASS_CONDITION"])
    )
    stabilizer_inclusion3 = exhaustive_stabilizer_inclusion(x3, swap3, maps3)
    stabilizer_inclusion4 = exhaustive_stabilizer_inclusion(x4, swap4, maps4)
    stabilizer_crosscheck = (
        "F(g.x)=g.F(x)" in " ".join(CLAIM_CONTRACT["ASSUMPTIONS"])
        and stabilizer_inclusion3
        and stabilizer_inclusion4
    )
    physical_flags_honest = not any(
        INITIAL_CLOSURE_FLAGS[key]
        for key in (
            "G6_PHYSICAL_MATCH", "G7_OBSERVATION", "G8_EXPORT",
            "W2_F1_SELF_DIFFERENTIATION", "W2_F2_OPERATIONAL_RELATIONS",
            "W2_F3_INTERNAL_ORDER_CAUSALITY", "W2_F4_INDEPENDENT_ADDITIVE_MODES",
        )
    )
    finite_controls_pass = all((c2_action3_pass, c2_action4_pass, finite3_pass, finite4_pass, degenerate_control, negative_control))
    passed = all((
        full_contract, contract_values_nonempty, text_sequences_valid,
        version_contract_bound,
        gate_applicability_complete,
        contract_registries_bound, freedom_schema_complete, branch_registry_exact,
        conventions_complete,
        direct_proof_declared, stabilizer_crosscheck, variational_pass, finite_controls_pass,
        physical_flags_honest, route_dependency_pass,
    ))
    closure_flags = dict(INITIAL_CLOSURE_FLAGS)
    closure_flags["G0_GOAL"] = all((
        full_contract, contract_values_nonempty, text_sequences_valid,
        version_contract_bound,
        gate_applicability_complete,
        contract_registries_bound, freedom_schema_complete, branch_registry_exact,
    ))
    closure_flags["G1_CONVENTIONS"] = closure_flags["G0_GOAL"] and conventions_complete
    closure_flags["G2_CORE_ALGEBRA"] = closure_flags["G1_CONVENTIONS"] and direct_proof_declared
    closure_flags["G3_STRUCTURE"] = closure_flags["G2_CORE_ALGEBRA"] and variational_pass
    closure_flags["G4_INDEPENDENT_CHECK"] = closure_flags["G3_STRUCTURE"] and stabilizer_crosscheck
    closure_flags["G5_LIMITS_REGRESSION"] = closure_flags["G4_INDEPENDENT_CHECK"] and finite_controls_pass
    closure_flags["EQUIVARIANT_FIXED_SET_NO_GO"] = passed
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": "CONDITIONAL_EXACT_FIXED_SET_THEOREM_PASS__INTERNAL__W2_F1_OPEN" if passed else "EQUIVARIANT_FIXED_SET_NO_GO_FAIL",
        "ABSTRACT_PROOF": [
            "x0 in Fix(G_sym)",
            "F(g.x0)=g.F(x0) by equivariance",
            "g.x0=x0",
            "therefore g.F(x0)=F(x0), so F(x0) in Fix(G_sym)",
        ],
        "INDEPENDENT_STABILIZER_PROOF": [
            "if h is in Stab(x), then h.x=x",
            "equivariance gives h.F(x)=F(h.x)=F(x)",
            "therefore Stab(x) is a subset of Stab(F(x))",
            "if Stab(x)=G_sym, then Stab(F(x))=G_sym",
        ],
        "CHECKS": {
            "full_CODES_section_5_contract": full_contract,
            "contract_values_nonempty": contract_values_nonempty,
            "required_text_sequences_valid": text_sequences_valid,
            "contract_and_runtime_model_versions_bound": version_contract_bound,
            "G0_to_G8_applicability_complete": gate_applicability_complete,
            "contract_and_global_registries_bound": contract_registries_bound,
            "freedom_ledger_schema_complete": freedom_schema_complete,
            "branch_registry_exact": branch_registry_exact,
            "conventions_and_freedom_ledger_complete": conventions_complete,
            "direct_universal_proof_declared": direct_proof_declared,
            "independent_stabilizer_inclusion_crosscheck": stabilizer_crosscheck,
            "three_state_exhaustive_stabilizer_inclusion": stabilizer_inclusion3,
            "four_state_exhaustive_stabilizer_inclusion": stabilizer_inclusion4,
            "route_dependency_status_verified": route_dependency_pass,
            "three_state_C2_action_law": c2_action3_pass,
            "four_state_C2_action_law": c2_action4_pass,
            "three_state_complete_enumeration": finite3_pass,
            "four_state_complete_enumeration": finite4_pass,
            "finite_enumerations_are_controls_not_universal_proof": True,
            "unique_invariant_minimum_is_fixed": variational_pass,
            "degenerate_nonfixed_minimum_orbit_control": degenerate_control,
            "non_equivariant_escape_detected": negative_control,
            "physical_flags_honest": physical_flags_honest,
        },
        "DIAGNOSTICS": {
            "three_state_fixed_set": sorted(fix3),
            "three_state_equivariant_map_count": len(maps3),
            "four_state_fixed_set": sorted(fix4),
            "four_state_equivariant_map_count": len(maps4),
            "unique_invariant_minimizers_seen": unique_minima,
            "degenerate_nonfixed_minima": sorted(degenerate_minima),
        },
        "THEORY_CONSEQUENCE": (
            "RefG-ის თვითგარჩევა ვერ იქნება ზუსტად სიმეტრიული q0-ის ერთმნიშვნელოვანი "
            "equivariant განახლებით არასიმეტრიულ ტოტზე გადასვლა. საჭიროა არამდგრადობა "
            "არასიმეტრიულ ზოგად seed/noise/boundary-სთან ერთად, ან დეგენერირებული "
            "set-valued ატემპორალური branch structure, ან "
            "სხვა მკაფიოდ გამოცხადებული symmetry-respecting outcome mechanism."
        ),
        "GATE_APPLICABILITY": GATE_APPLICABILITY,
        "CLOSURE_FLAGS": closure_flags,
        "PROVENANCE": {name: sha256(path) for name, path in paths.items()},
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["STATUS"].startswith("CONDITIONAL_EXACT") else 1


if __name__ == "__main__":
    raise SystemExit(main())
