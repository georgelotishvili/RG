"""W2-F1 atemporal spectral-split candidate on one internal carrier.

The candidate is deliberately pre-spatial and pre-clock.  Its state is one
abstract real symmetric traceless 3x3 operator Q.  Matrix indices are internal
representation labels, O(3) conjugation is relabel equivalence, and ``Tr_alg``
is an algebraic contraction rather than RefG's persistent physical imprint.

The exact result proved here is conditional: an O(3)-invariant bounded
functional has one nonzero global-minimum orbit in the quotient and that orbit
contains two Q-generated spectral sectors of unequal ranks 1 and 2.  This is
an atemporal variational construction, not a temporal formation history and
not yet a promotion of the physical programme-wide W2_F1 flag.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


MODEL_VERSION = "W2-F1-ATEMPORAL-SPECTRAL-SPLIT-v1.0-internal"
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"

UNIVERSAL_GATES = frozenset({
    "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
    "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
    "G7_OBSERVATION", "G8_EXPORT",
})

REQUIRED_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "GATE_APPLICABILITY", "CROSSCHECK", "PROVENANCE", "FILES",
})

REQUIRED_CUSTOM_FIELDS = frozenset({
    "PRIMITIVE_REGISTRY", "IMPORTED_NOT_DERIVED", "DEFERRED_OUTPUTS",
    "SELECTION_RULE", "COMPUTATIONAL_INDEX_ROLE", "METRIC_ROUTE",
})

EXPECTED_FREEDOM_SLOTS = frozenset({
    "ontological_carrier_count", "internal_state_space", "internal_matrix_size_N",
    "internal_index_metric", "relabel_equivalence", "algebraic_invariants",
    "polarity_symmetry_choice", "variational_rule", "alpha", "b", "c", "seed_or_randomness",
    "computational_index", "data_fitted_parameters",
})

EXPECTED_PRIMITIVE_REGISTRY = {
    "1_objects_and_state_space": (
        "ერთი აბსტრაქტული მატარებლის მდგომარეობაა Q in Sym_0(3,R); "
        "მატრიცის კომპონენტები მხოლოდ შიდა წარმოდგენაა."
    ),
    "2_primitive_relations": (
        "მატრიცული ნამრავლი, ტრანსპონირება, შიდა delta და ალგებრული Tr_alg; "
        "ფიზიკური კვანძი, ადგილი ან მდგრადი კვალი არაა შეტანილი."
    ),
    "3_symmetry_and_equivalence": (
        "Q ~ R Q R^T ყველა R in O(3)-სთვის; O(3) არის შიდა გადაიარლიყება "
        "და არა ფიზიკური სივრცის ბრუნვა. Q->-Q ამ კანდიდატში გადაიარლიყება არაა."
    ),
    "4_rule": (
        "ატემპორალური წესი: ფიზიკურად დასაშვები კანდიდატური მდგომარეობაა "
        "V(Q)-ის გლობალური argmin modulo O(3)."
    ),
    "5_free_parameters": "alpha>0, b>0, c>0 ღია არე; მონაცემზე მორგებული პარამეტრი 0.",
    "6_initial_and_boundary_conditions": (
        "N/A — არ გამოიყენება სივრცითი საზღვარი, საწყისი დრო ან წინასწარ არჩეული მიმართულება."
    ),
    "7_randomness": (
        "N/A — seed/noise არ გამოიყენება; მინიმუმთა ორიენტაციული ორბიტა მთლიანად გადაიარლიყებაა."
    ),
    "8_computational_index": (
        "მხოლოდ სიმბოლური კომპონენტებისა და საკონტროლო ჩამოთვლის ინდექსი; ფიზიკური დრო არაა."
    ),
    "9_validity_and_limits": (
        "სასრული შიდა Sym_0(3,R), alpha,b,c>0 და ატემპორალური გლობალური მინიმიზაცია."
    ),
    "10_imported_not_derived": (
        "Sym_0(3,R), N=3, დადებითი შიდა delta, O(3), მატრიცული ალგებრა, "
        "კვარტიკულამდე ფუნქციონალი და argmin-პრინციპი კანდიდატში შეტანილია."
    ),
}

EXPECTED_IMPORTED_NOT_DERIVED = (
    "single_internal_carrier_Q",
    "Sym0_3_R_internal_configuration_space",
    "positive_definite_internal_delta_and_transpose",
    "matrix_product_and_Tr_alg",
    "O3_internal_conjugation_relabel_equivalence",
    "absence_of_Q_sign_relabel_symmetry",
    "atemporal_global_argmin_rule",
    "positive_open_parameter_domain_alpha_b_c",
)

EXPECTED_DEFERRED_OUTPUTS = (
    "physical_node_or_location",
    "persistent_physical_imprint",
    "operational_relation",
    "internal_causal_order_or_clock",
    "additive_physical_modes",
    "spacetime_dimension_or_metric",
    "pressure_mass_particle_oscillon_or_GR_bridge",
)

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
    "ATEMPORAL_SPECTRAL_SPLIT_EXACT": False,
    "QUOTIENT_STABILITY_EXACT": False,
    "W2_F1_CONDITIONAL_CANDIDATE": False,
    "W2_F1_SELF_DIFFERENTIATION": False,
    "W2_F2_OPERATIONAL_RELATIONS": False,
    "W2_F3_INTERNAL_ORDER_CAUSALITY": False,
    "W2_F4_INDEPENDENT_ADDITIVE_MODES": False,
    "W2_M1_DIMENSION_CONTINUUM": False,
    "W2_M2_LORENTZIAN_METRIC": False,
    "W2_A0_EFFECTIVE_ACTION_ORIGIN": False,
}

GATE_APPLICABILITY = {
    "G0_GOAL": "REQUIRED — conditional candidate claim, scope, imports and PASS/FAIL are frozen",
    "G1_CONVENTIONS": "REQUIRED — internal indices, Tr_alg, O(3) relabel quotient and atemporal rule",
    "G2_CORE_ALGEBRA": "REQUIRED — invariant bound, stationary equations, projectors and exact residuals",
    "G3_STRUCTURE": "REQUIRED — complete global-minimum orbit and positive Hessian on the orbit-normal slice",
    "G4_INDEPENDENT_CHECK": "REQUIRED — eigenvalue-discriminant proof vs direct five-coordinate Hessian",
    "G5_LIMITS_REGRESSION": "REQUIRED — N=1/N=2/N=4/general-N, b=0, polarity, coercivity and source controls",
    "G6_PHYSICAL_MATCH": "N/A — no physical source, energy ledger or observable map",
    "G7_OBSERVATION": "N/A — no physical prediction or dataset at F1 candidate level",
    "G8_EXPORT": "N/A — internal Git-ignored candidate; no Canon/article export authorized",
}

EXPECTED_BRANCHES = {
    "alpha_b_c_positive_atemporal_uniaxial_orbit": "EXACT_CONDITIONAL_CANDIDATE_PASS",
    "Q_zero": "STATIONARY_BUT_STRICT_VARIATIONAL_MAXIMUM",
    "O3_orientation_orbit": "RELABEL_EQUIVALENT__NO_PHYSICAL_DIRECTION_SELECTED",
    "b_zero_boundary": "DEGENERATE_QUOTIENT__DOES_NOT_CLOSE_THIS_UNIQUE_ORBIT_CLAIM",
    "positive_quadratic_null_control": "UNDIFFERENTIATED_ORIGIN_ONLY",
    "N_one_control": "TRACLESS_STATE_SPACE_TRIVIAL",
    "N_two_control": "NO_UNEQUAL_RANK_TWO_SECTOR_SPLIT",
    "explicit_linear_source": "REJECTED_TARGET_PREWIRING",
}

EXPECTED_CLOSURE_KEYS = frozenset(INITIAL_CLOSURE_FLAGS)
EXPECTED_GATE_APPLICABILITY = dict(GATE_APPLICABILITY)


CLAIM_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F1_ATEMPORAL_SPECTRAL_SPLIT_CANDIDATE_001",
    "CLAIM": (
        "ერთ აბსტრაქტულ შიდა მატარებელზე X=Sym_0(3,R) და Q~RQR^T გადაიარლიყების "
        "პირობებში, V(Q)=-alpha Tr_alg(Q^2)/2-b Tr_alg(Q^3)/3+"
        "c[Tr_alg(Q^2)]^2/4 ფუნქციონალს alpha,b,c>0 ღია არეში აქვს ზუსტად ერთი "
        "არანულოვანი გლობალური მინიმუმის O(3)-ორბიტა. quotient-ში ეს ორბიტა "
        "მდგრადია და Q-სგან პოლინომურად მიიღება ურთიერთორთოგონალური rank-1 და rank-2 "
        "სპექტრული სექტორები; Q=0 ასეთ არატრივიალურ კანონიკურ სექტორს არ შეიცავს."
    ),
    "TYPE": (
        "EXACT_IDENTITY + EXACT_VARIATIONAL_CONSTRUCTION; CONDITIONAL_CANDIDATE; "
        "არა MECHANISM_DERIVED და ჯერ არა programme-wide W2_F1 closure"
    ),
    "MODEL_VERSION": (
        f"{MODEL_VERSION}; state space, quotient, functional, parameter domain, "
        "selection rule, role criterion or PASS logic changes require a new version"
    ),
    "ASSUMPTIONS": [
        "ერთი ონტოლოგიური მატარებელი შეიძლება ჰქონდეს არატრივიალური შიდა მდგომარეობათა სივრცე; იგი strict singleton არაა.",
        "Q არის ერთი რეალური სიმეტრიული traceless 3x3 შიდა ოპერატორი და არა Q(x,t) ველი.",
        "O(3)-conjugation მხოლოდ შიდა ბაზის გადაიარლიყებაა; ფიზიკური მდგომარეობაა quotient class [Q].",
        "Q->-Q არ შედის გადაიარლიყების ჯგუფში; ამიტომ კუბური invariant დაშვებულია, ხოლო b-ს ნიშნის სარკული ტოტი ცალკე კონტროლდება.",
        "Tr_alg არის მატრიცული შეკუმშვა და არა RefG-ის მდგრადი ფიზიკური კვალი/imprint.",
        "ატემპორალური კანდიდატური კანონი ირჩევს global argmin-set-ს modulo O(3), არა დროში ტრაექტორიას.",
        "alpha>0, b>0 და c>0; ეს არის ღია კანდიდატური არე და არცერთი კოეფიციენტი მონაცემზე არაა მორგებული.",
        "კანონიკური შიდა როლი ითვლება მხოლოდ Q-ს მიერ გენერირებული სპექტრული ალგებრის არატრივიალურ projector-ად; წინასწარ არჩეული ბაზის projector არ ითვლება.",
    ],
    "DOMAIN": (
        "სასრული წინასივრცითი შიდა Sym_0(3,R), O(3)-quotient და alpha,b,c>0. "
        "არ მოიცავს ფიზიკურ სივრცეს, საათურ დროს, კვანძს, გავრცელებას, ენერგიას, "
        "მეტრიკას ან დაკვირვებადს. N=3 შიდა trial dimension-ია და არა 3-space."
    ),
    "CONVENTIONS": (
        "Q^T=Q, Tr_alg(Q)=0, I2=Tr_alg(Q^2), I3=Tr_alg(Q^3). შიდა delta "
        "დადებითად განსაზღვრულია. O(3) არის gauge/relabel; n და Q*=s(nn^T-I/3) "
        "მხოლოდ ორბიტის წარმომადგენელია. Hessian-ის ნულოვანი orbit modes gauge-ია, "
        "არა ნაწილაკი. faithful მოქმედებაა O(3)/{+I,-I}, არა O(3)/SO(3). "
        "განივი 1+2 დადებითი modes არ ცხადდება სამ დამოუკიდებელ გლუვ quotient-"
        "კოორდინატად. Q->-Q gauge არაა; Tr_alg არ ნიშნავს persistent trace-ს."
    ),
    "FREEDOM_LEDGER": {
        "ontological_carrier_count": {"source": "Canon candidate constraint", "range": 1, "scale": "universal", "complexity": 0},
        "internal_state_space": {"source": "imported candidate", "range": "Sym_0(3,R)", "scale": "model", "complexity": 5},
        "internal_matrix_size_N": {"source": "candidate choice with within-class rank control", "range": 3, "scale": "model", "complexity": 1},
        "internal_index_metric": {"source": "imported candidate", "range": "positive delta_ab", "scale": "model", "complexity": 0},
        "relabel_equivalence": {"source": "imported candidate", "range": "O(3) conjugation", "scale": "universal", "complexity": 3},
        "algebraic_invariants": {"source": "imported candidate algebra", "range": "I2 and I3", "scale": "model", "complexity": 2},
        "polarity_symmetry_choice": {"source": "imported candidate", "range": "Q->-Q is not gauge", "scale": "model", "complexity": 1},
        "variational_rule": {"source": "imported candidate law", "range": "global argmin modulo O(3)", "scale": "universal", "complexity": 1},
        "alpha": {"source": "free theory parameter", "range": "(0,infinity)", "scale": "model", "complexity": 1},
        "b": {"source": "free theory parameter", "range": "(0,infinity)", "scale": "model", "complexity": 1},
        "c": {"source": "free theory parameter", "range": "(0,infinity)", "scale": "model", "complexity": 1},
        "seed_or_randomness": {"source": "N/A — atemporal quotient rule", "range": 0, "scale": "realization", "complexity": 0},
        "computational_index": {"source": "symbolic bookkeeping only", "range": "finite coordinates", "scale": "calculation", "complexity": 0},
        "data_fitted_parameters": {"source": "N/A — no data", "range": 0, "scale": "data", "complexity": 0},
    },
    "DEPENDENCIES": [
        f"{PROGRAM_CONTRACT}: pre-spatial target-leakage and W2_F1 boundary",
        "w2_01 v1.2: radial Landau toy positive control only",
        "w2_02 v1.5: strict-singleton conditional no-go",
        "w2_03 v1.8: source-aligned route and forbidden-input contract",
        "w2_04 v1.7: equivariant fixed-set no-go and set-valued escape boundary",
        "w2_05 v1.7: primary route remains provisional; atemporal class remains OPEN",
    ],
    "METHOD": (
        "First derive the sharp traceless-3x3 invariant inequality from the eigenvalue "
        "discriminant and reduce the global problem to one radius. Independently compute "
        "the full five-coordinate gradient/Hessian and decompose it into radial, biaxial "
        "and O(3)-orbit modes. Derive spectral projectors directly from Q."
    ),
    "PASS_CONDITION": [
        "the complete primitive/freedom registry contains no forbidden spacetime, RefG-effective or observed target input.",
        "V is exactly O(3)-invariant and bounded below for c>0.",
        "Q=0 has no nontrivial Q-generated projector and is strictly variationally unstable for alpha>0.",
        "I2^3-6 I3^2 equals twice the nonnegative eigenvalue discriminant and gives the sharp global bound.",
        "the global argmin-set is exactly one O(3) orbit with s*=(b+sqrt(b^2+24 alpha c))/(4c).",
        "the orbit-normal Hessian has one positive radial and two positive biaxial modes; its only two zero modes are relabel-orbit tangents, not three asserted smooth quotient coordinates.",
        "Q-generated P1 and P2 are orthogonal projectors of unequal ranks 1 and 2 and reconstruct Q exactly.",
        "N=1 and N=2 controls do not realize this specific unequal-rank two-sector certificate; no claim of general SSB minimality is made.",
        "general-N and N=4 controls expose that N=3 is an imported choice selecting the specific 1+2 count.",
        "the negative stationary amplitude, c<=0 branches, Q-sign-gauge alternative and explicit anisotropy source are rejected or kept outside the frozen domain.",
        "all physical W2_F1/F2/F3/F4 and later programme flags remain False pending a separate promotion audit.",
    ],
    "FAIL_CONDITION": (
        "A lower-energy state exists outside the declared orbit, a non-gauge negative/zero "
        "Hessian direction remains, the two projectors are not Q-generated or rank-inequivalent, "
        "or a preferred direction/physical geometry is hidden in the inputs."
    ),
    "FALSIFIER": (
        "An explicit Q in Sym_0(3,R) and alpha,b,c>0 with V(Q)<V(Q*), or an exact "
        "non-orbit perturbation with nonpositive second variation at Q*, falsifies the claim."
    ),
    "RESIDUAL": (
        "Zero for the stationary equation, sharp-discriminant identity, projector algebra, "
        "mode-resolved Hessian identities and invariance controls."
    ),
    "ERROR_BOUND": "0 — symbolic exact algebra in the declared finite-dimensional domain.",
    "VALIDITY_HEALTH": (
        "The quartic c>0 term bounds V. Quotient stability, not temporal stability, is proved. "
        "The three positive transverse modes form a normal-slice Hessian certificate; the "
        "stratified quotient is not asserted to have three independent smooth coordinates. "
        "The construction imports N=3, a positive internal metric, O(3), matrix algebra, the "
        "functional and global-minimum law. It does not derive their ontology, a physical "
        "formation history, an operational F2 map, spacetime or observations."
    ),
    "BRANCHES": dict(EXPECTED_BRANCHES),
    "OBSERVABLE_MAP": "N/A — spectral ranks are internal mathematical certificates, not physical observables.",
    "FORWARD_MODEL": "N/A — no bridge from the internal candidate to data.",
    "DATA_ROLE": "N/A — no data used for construction, fitting, validation or prediction.",
    "IDENTIFIABILITY": (
        "Within the internal quotient, the unordered spectrum and projector ranks are exact "
        "invariants; O(3)-orientation is unidentifiable gauge. Physical identifiability is N/A."
    ),
    "BENCHMARK": (
        "Positive control alpha=b=c=1 gives s*=3/2. Null controls: stable positive-quadratic "
        "origin, b=0 quotient degeneracy, negative stationary root, c<=0, polarity mirror, "
        "N=1/N=2/N=4/general-N rank structure and a forbidden linear source."
    ),
    "CLOSURE_FLAGS": dict(INITIAL_CLOSURE_FLAGS),
    "GATE_APPLICABILITY": dict(GATE_APPLICABILITY),
    "CROSSCHECK": (
        "Eigenvalue-discriminant global proof is independent of the component-coordinate "
        "gradient/Hessian proof; both share only the declared state space and functional."
    ),
    "PROVENANCE": "runtime SHA-256 of sources, Work2 dependencies and this source; stdout JSON artifact",
    "FILES": [
        "CODES.md", "Theory_Canon.md", "intuitive/RefG_GE.md",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_01_self_differentiation_candidate_gate.py",
        "RefG/work 2/w2_02_f1_singleton_no_go_gate.py",
        "RefG/work 2/w2_03_f1_source_aligned_route_contract.py",
        "RefG/work 2/w2_04_f1_equivariant_fixed_set_no_go_gate.py",
        "RefG/work 2/w2_05_f1_primary_route_specification.py",
        "RefG/work 2/w2_06_f1_atemporal_spectral_split_candidate_gate.py",
    ],
    "PRIMITIVE_REGISTRY": dict(EXPECTED_PRIMITIVE_REGISTRY),
    "IMPORTED_NOT_DERIVED": list(EXPECTED_IMPORTED_NOT_DERIVED),
    "DEFERRED_OUTPUTS": list(EXPECTED_DEFERRED_OUTPUTS),
    "SELECTION_RULE": (
        "Atemporal set-valued global argmin followed by O(3) quotient. The quotient minimum "
        "is unique; no representative direction n, seed, noise or boundary is selected."
    ),
    "COMPUTATIONAL_INDEX_ROLE": "Finite symbolic coordinate index only; no physical time, order or causality.",
    "METRIC_ROUTE": "N/A — internal positive delta is not a spacetime metric and cannot close W2_M1/W2_M2.",
}

# Independent snapshots prevent the checked contract and its certification
# registry from drifting apart during a run.
EXPECTED_FREEDOM_LEDGER = {
    key: dict(value) for key, value in CLAIM_CONTRACT["FREEDOM_LEDGER"].items()
}
_SEPARATELY_BOUND_FIELDS = {
    "MODEL_VERSION", "FREEDOM_LEDGER", "BRANCHES", "CLOSURE_FLAGS",
    "GATE_APPLICABILITY", "PRIMITIVE_REGISTRY", "IMPORTED_NOT_DERIVED",
    "DEFERRED_OUTPUTS",
}
EXPECTED_SEMANTIC_FIELDS = {
    key: copy.deepcopy(value)
    for key, value in CLAIM_CONTRACT.items()
    if key not in _SEPARATELY_BOUND_FIELDS
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def value_present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    return bool(value)


def text_sequence_valid(value: Any) -> bool:
    return (
        isinstance(value, (list, tuple))
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def freedom_ledger_valid(ledger: Any) -> bool:
    required = {"source", "range", "scale", "complexity"}
    return (
        isinstance(ledger, dict)
        and set(ledger) == EXPECTED_FREEDOM_SLOTS
        and ledger == EXPECTED_FREEDOM_LEDGER
        and all(
            isinstance(entry, dict)
            and set(entry) == required
            and all(
                item is not None
                and (not isinstance(item, str) or bool(item.strip()))
                for item in entry.values()
            )
            for entry in ledger.values()
        )
    )


def load_gate_report(path: Path, module_name: str) -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_gate()


def report_value(report: dict[str, Any], upper: str, lower: str) -> Any:
    return report.get(upper, report.get(lower))


def run_gate() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    work2 = root / "RefG" / "work 2"
    paths = {
        "CODES": root / "CODES.md",
        "CANON": root / "Theory_Canon.md",
        "INTUITIVE": root / "intuitive" / "RefG_GE.md",
        "W2_C0": work2 / "w2_00_foundation_to_einstein_contract.md",
        "W2_01": work2 / "w2_01_self_differentiation_candidate_gate.py",
        "W2_02": work2 / "w2_02_f1_singleton_no_go_gate.py",
        "W2_03": work2 / "w2_03_f1_source_aligned_route_contract.py",
        "W2_04": work2 / "w2_04_f1_equivariant_fixed_set_no_go_gate.py",
        "W2_05": work2 / "w2_05_f1_primary_route_specification.py",
        "SOURCE": Path(__file__).resolve(),
    }

    dependency_reports = {
        name: load_gate_report(paths[name], f"{name.lower()}_w2_06_dependency")
        for name in ("W2_01", "W2_02", "W2_03", "W2_04", "W2_05")
    }
    expected_statuses = {
        "W2_01": "EXACT_IDENTITY_PASS__TOY_POSITIVE_CONTROL__W2_F1_OPEN",
        "W2_02": "EXACT_SINGLETON_NO_GO_PASS__W2_F1_OPEN",
        "W2_03": "ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_G1_AND_PHYSICAL_F1_OPEN",
        "W2_04": "CONDITIONAL_EXACT_FIXED_SET_THEOREM_PASS__INTERNAL__W2_F1_OPEN",
        "W2_05": "PRIMARY_ROUTE_SCHEMA_VALIDATED_INTERNAL__CONCRETE_MODEL_AND_W2_F1_OPEN",
    }
    expected_versions = {
        "W2_01": "W2-F1-RADIAL-LANDAU-v1.2-frozen",
        "W2_02": "W2-F1-SINGLETON-NO-GO-v1.5-corrected-internal",
        "W2_03": "W2-F1-SOURCE-ALIGNED-ROUTE-CONTRACT-v1.8-internal",
        "W2_04": "W2-F1-EQUIVARIANT-FIXED-SET-NO-GO-v1.7-internal",
        "W2_05": "W2-F1-PRIMARY-ROUTE-SPEC-v1.7-internal",
    }
    dependency_statuses = {
        name: report_value(report, "STATUS", "status")
        for name, report in dependency_reports.items()
    }
    dependency_versions = {
        name: report_value(report, "MODEL_VERSION", "model_version")
        for name, report in dependency_reports.items()
    }
    dependency_chain_valid = all(
        dependency_statuses[name] == expected_statuses[name]
        and dependency_versions[name] == expected_versions[name]
        for name in expected_statuses
    )
    dependency_f1_open = all(
        report_value(report, "CLOSURE_FLAGS", "closure_flags").get(
            "W2_F1_SELF_DIFFERENTIATION"
        ) is False
        for report in dependency_reports.values()
    )
    route_registration_valid = (
        "atemporal_nonunique_solution_structure"
        in dependency_reports["W2_03"].get("CANDIDATE_CLASSES", {})
        and "atemporal_nonunique_solution_structure"
        in dependency_reports["W2_05"].get("ALTERNATIVE_CLASSES_REMAIN_OPEN", [])
    )

    all_required_fields = REQUIRED_FIELDS | REQUIRED_CUSTOM_FIELDS
    required_fields_present = all_required_fields.issubset(CLAIM_CONTRACT)
    contract_values_nonempty = all(
        value_present(CLAIM_CONTRACT.get(key)) for key in all_required_fields
    )
    text_sequences_valid = all(
        text_sequence_valid(CLAIM_CONTRACT.get(key))
        for key in ("ASSUMPTIONS", "DEPENDENCIES", "PASS_CONDITION", "FILES")
    )
    version_bound = (
        isinstance(CLAIM_CONTRACT.get("MODEL_VERSION"), str)
        and CLAIM_CONTRACT["MODEL_VERSION"].startswith(f"{MODEL_VERSION};")
    )
    semantic_contract_bound = all(
        CLAIM_CONTRACT.get(key) == value
        for key, value in EXPECTED_SEMANTIC_FIELDS.items()
    )
    registries_bound = (
        CLAIM_CONTRACT.get("BRANCHES") == EXPECTED_BRANCHES
        and CLAIM_CONTRACT.get("PRIMITIVE_REGISTRY") == EXPECTED_PRIMITIVE_REGISTRY
        and tuple(CLAIM_CONTRACT.get("IMPORTED_NOT_DERIVED", ())) == EXPECTED_IMPORTED_NOT_DERIVED
        and tuple(CLAIM_CONTRACT.get("DEFERRED_OUTPUTS", ())) == EXPECTED_DEFERRED_OUTPUTS
        and CLAIM_CONTRACT.get("GATE_APPLICABILITY") == EXPECTED_GATE_APPLICABILITY
        and GATE_APPLICABILITY == EXPECTED_GATE_APPLICABILITY
        and set(CLAIM_CONTRACT.get("CLOSURE_FLAGS", {})) == EXPECTED_CLOSURE_KEYS
        and not any(CLAIM_CONTRACT.get("CLOSURE_FLAGS", {}).values())
        and set(INITIAL_CLOSURE_FLAGS) == EXPECTED_CLOSURE_KEYS
        and not any(INITIAL_CLOSURE_FLAGS.values())
    )
    primitive_values_nonblank = all(
        isinstance(value, str) and value.strip()
        for value in CLAIM_CONTRACT.get("PRIMITIVE_REGISTRY", {}).values()
    )
    freedom_ledger_complete = freedom_ledger_valid(CLAIM_CONTRACT.get("FREEDOM_LEDGER"))
    gate_applicability_complete = (
        set(GATE_APPLICABILITY) == UNIVERSAL_GATES
        and all(isinstance(value, str) and value.strip() for value in GATE_APPLICABILITY.values())
    )

    forbidden_inputs = set(dependency_reports["W2_03"].get("FORBIDDEN_PREWIRED_INPUTS", []))
    deferred_inputs = set(dependency_reports["W2_03"].get("DEFERRED_OUTPUTS", []))
    declared_imports = set(EXPECTED_IMPORTED_NOT_DERIVED)
    exact_forbidden_intersection = declared_imports & (forbidden_inputs | deferred_inputs)
    source_boundary_declared = all((
        "N=3 შიდა trial dimension-ია და არა 3-space" in CLAIM_CONTRACT["DOMAIN"],
        "Tr_alg არ ნიშნავს persistent trace-ს" in CLAIM_CONTRACT["CONVENTIONS"],
        "no physical time" in CLAIM_CONTRACT["COMPUTATIONAL_INDEX_ROLE"],
        CLAIM_CONTRACT["METRIC_ROUTE"].startswith("N/A"),
        "no representative direction" in CLAIM_CONTRACT["SELECTION_RULE"],
    ))
    target_leakage_absent = not exact_forbidden_intersection and source_boundary_declared

    # General internal traceless-symmetric coordinate chart.
    alpha, b, c, s = sp.symbols("alpha b c s", positive=True, real=True)
    x, y, u, v, w = sp.symbols("x y u v w", real=True)
    coordinates = (x, y, u, v, w)
    Q = sp.Matrix([
        [x, u, v],
        [u, y, w],
        [v, w, -x - y],
    ])
    basis = tuple(Q.diff(variable) for variable in coordinates)
    gram = sp.Matrix([
        [sp.trace(left * right) for right in basis]
        for left in basis
    ])
    expected_gram = sp.diag(1, 1, 2, 2, 2)
    expected_gram[0, 0] = 2
    expected_gram[1, 1] = 2
    expected_gram[0, 1] = expected_gram[1, 0] = 1
    gram_pass = gram == expected_gram and set(gram.eigenvals()) == {1, 2, 3}

    I2 = sp.expand(sp.trace(Q * Q))
    I3 = sp.expand(sp.trace(Q * Q * Q))
    potential = sp.expand(-alpha * I2 / 2 - b * I3 / 3 + c * I2**2 / 4)
    gradient = sp.Matrix([sp.diff(potential, variable) for variable in coordinates])
    hessian = sp.hessian(potential, coordinates)
    zero_substitution = {variable: 0 for variable in coordinates}
    origin_gradient = sp.simplify(gradient.subs(zero_substitution))
    origin_hessian = sp.simplify(hessian.subs(zero_substitution))
    origin_residual = sp.simplify(origin_hessian + alpha * gram)
    origin_pass = (
        matrix_is_zero(origin_gradient)
        and matrix_is_zero(origin_residual)
        and gram_pass
    )

    # Sharp invariant bound from the exact real-eigenvalue discriminant.
    l1, l2 = sp.symbols("l1 l2", real=True)
    l3 = -l1 - l2
    I2_eig = sp.expand(l1**2 + l2**2 + l3**2)
    I3_eig = sp.expand(l1**3 + l2**3 + l3**3)
    eigen_discriminant = sp.expand(
        (l1 - l2) ** 2 * (l2 - l3) ** 2 * (l3 - l1) ** 2
    )
    sharp_bound_residual = sp.expand(I2_eig**3 - 6 * I3_eig**2 - 2 * eigen_discriminant)

    r = sp.symbols("r", positive=True, real=True)
    reduced_potential = -alpha * r**2 / 2 - b * r**3 / (3 * sp.sqrt(6)) + c * r**4 / 4
    reduced_derivative_residual = sp.simplify(
        sp.diff(reduced_potential, r)
        - r * (c * r**2 - b * r / sp.sqrt(6) - alpha)
    )
    r_star = sp.simplify(
        (b / sp.sqrt(6) + sp.sqrt(b**2 / 6 + 4 * alpha * c)) / (2 * c)
    )
    r_minus = sp.simplify(
        (b / sp.sqrt(6) - sp.sqrt(b**2 / 6 + 4 * alpha * c)) / (2 * c)
    )
    radial_root_residual = sp.simplify(c * r_star**2 - b * r_star / sp.sqrt(6) - alpha)

    s_star = sp.simplify((b + sp.sqrt(b**2 + 24 * alpha * c)) / (4 * c))
    discriminant_root = sp.sqrt(b**2 + 24 * alpha * c)
    s_minus = sp.simplify((b - discriminant_root) / (4 * c))
    s_stationary_residual = sp.simplify(2 * c * s_star**2 - b * s_star - 3 * alpha)
    s_minus_stationary_residual = sp.simplify(2 * c * s_minus**2 - b * s_minus - 3 * alpha)
    radius_relation_residual = sp.simplify(r_star - sp.sqrt(sp.Rational(2, 3)) * s_star)
    radical_gap = sp.simplify((b**2 / 6 + 4 * alpha * c) - b**2 / 6)
    discriminant_gap = sp.simplify(discriminant_root**2 - b**2)
    minimum_energy_sign_certificate = sp.simplify(3 * c * s_star - b)
    negative_root_biaxial_eigenvalue = sp.simplify(b * s_minus)
    negative_stationary_branch_rejected = all((
        s_minus_stationary_residual == 0,
        discriminant_gap == 24 * alpha * c,
        sp.simplify(4 * c * s_minus - b) == -discriminant_root,
        sp.simplify(negative_root_biaxial_eigenvalue - b * (b - discriminant_root) / (4 * c)) == 0,
        alpha.is_positive is True,
        b.is_positive is True,
        c.is_positive is True,
    ))
    positive_root_structure_pass = all((
        reduced_derivative_residual == 0,
        radial_root_residual == 0,
        s_stationary_residual == 0,
        radius_relation_residual == 0,
        radical_gap == 4 * alpha * c,
        discriminant_gap == 24 * alpha * c,
        sp.simplify(minimum_energy_sign_certificate - (-b + 3 * discriminant_root) / 4) == 0,
        negative_stationary_branch_rejected,
        alpha.is_positive is True,
        b.is_positive is True,
        c.is_positive is True,
    ))

    star_substitution = {
        x: 2 * s / 3,
        y: -s / 3,
        u: 0,
        v: 0,
        w: 0,
    }
    stationarity_relation = {alpha: (2 * c * s**2 - b * s) / 3}
    Q_star = sp.simplify(Q.subs(star_substitution))
    I2_star = sp.simplify(I2.subs(star_substitution))
    I3_star = sp.simplify(I3.subs(star_substitution))
    star_gradient_residual = sp.simplify(
        gradient.subs(star_substitution).subs(stationarity_relation)
    )
    star_bound_saturation = sp.simplify(I2_star**3 - 6 * I3_star**2)
    star_energy_on_shell = sp.factor(
        potential.subs(star_substitution).subs(stationarity_relation)
    )
    expected_star_energy = s**3 * (b - 3 * c * s) / 27
    global_classification_pass = all((
        sharp_bound_residual == 0,
        reduced_derivative_residual == 0,
        positive_root_structure_pass,
        matrix_is_zero(star_gradient_residual),
        star_bound_saturation == 0,
        sp.simplify(star_energy_on_shell - expected_star_energy) == 0,
        I2_star == 2 * s**2 / 3,
        I3_star == 2 * s**3 / 9,
    ))

    # Independent stationary-equation classification.  Every eigenvalue of a
    # critical Q obeys one common quadratic, so a nonzero traceless 3x3
    # critical point has multiplicities 1+2 and is one of s_plus/s_minus.
    eom_matrix = sp.simplify(
        -alpha * Q
        - b * (Q * Q - sp.eye(3) * I2 / 3)
        + c * I2 * Q
    )
    eom_coordinate_pairing = sp.Matrix([
        sp.expand(sp.trace(eom_matrix * direction)) for direction in basis
    ])
    eom_gradient_residual = sp.simplify(eom_coordinate_pairing - gradient)
    stationary_energy = sp.expand(
        -alpha * s**2 / 3 - 2 * b * s**3 / 27 + c * s**4 / 9
    )
    energy_plus = sp.simplify(stationary_energy.subs(s, s_star))
    energy_minus = sp.simplify(stationary_energy.subs(s, s_minus))
    energy_order_residual = sp.simplify(
        energy_plus - energy_minus + b * discriminant_root**3 / (432 * c**3)
    )
    stationary_classification_pass = all((
        matrix_is_zero(eom_gradient_residual),
        s_stationary_residual == 0,
        s_minus_stationary_residual == 0,
        energy_order_residual == 0,
        negative_stationary_branch_rejected,
        origin_pass,
    ))

    # Exact full Hessian decomposition at the nonzero orbit representative.
    hessian_star = sp.simplify(
        hessian.subs(star_substitution).subs(stationarity_relation)
    )
    radial_mode = sp.Matrix([sp.Rational(2, 3), -sp.Rational(1, 3), 0, 0, 0])
    biaxial_diag_mode = sp.Matrix([0, 1, 0, 0, 0])
    orbit_12_mode = sp.Matrix([0, 0, 1, 0, 0])
    orbit_13_mode = sp.Matrix([0, 0, 0, 1, 0])
    biaxial_23_mode = sp.Matrix([0, 0, 0, 0, 1])
    mode_matrix = sp.Matrix.hstack(
        radial_mode, biaxial_diag_mode, biaxial_23_mode,
        orbit_12_mode, orbit_13_mode,
    )
    mode_gram = sp.simplify(mode_matrix.T * gram * mode_matrix)
    mode_hessian = sp.simplify(mode_matrix.T * hessian_star * mode_matrix)
    radial_eigenvalue = s * (4 * c * s - b) / 3
    biaxial_eigenvalue = b * s
    expected_mode_hessian = sp.diag(
        mode_gram[0, 0] * radial_eigenvalue,
        mode_gram[1, 1] * biaxial_eigenvalue,
        mode_gram[2, 2] * biaxial_eigenvalue,
        0,
        0,
    )
    mode_hessian_residual = sp.simplify(mode_hessian - expected_mode_hessian)
    radial_positive_certificate = sp.simplify(4 * c * s_star - b)
    quotient_stability_pass = all((
        mode_matrix.det() != 0,
        mode_gram == sp.diag(*[mode_gram[i, i] for i in range(5)]),
        matrix_is_zero(mode_hessian_residual),
        radial_positive_certificate == sp.sqrt(b**2 + 24 * alpha * c),
        b.is_positive is True,
        s_star.is_positive is True,
    ))

    # Q-generated canonical projectors: no basis vector or direction is an input.
    identity3 = sp.eye(3)
    P1 = sp.simplify(Q_star / s + identity3 / 3)
    P2 = sp.simplify(identity3 - P1)
    projector_pass = all((
        matrix_is_zero(sp.simplify(P1 * P1 - P1)),
        matrix_is_zero(sp.simplify(P2 * P2 - P2)),
        matrix_is_zero(sp.simplify(P1 * P2)),
        sp.trace(P1) == 1,
        sp.trace(P2) == 2,
        P1.rank() == 1,
        P2.rank() == 2,
        matrix_is_zero(sp.simplify(Q_star - s * (P1 - identity3 / 3))),
    ))
    polynomial_constant = sp.symbols("polynomial_constant", real=True)
    origin_projector_solutions = sp.solve(
        sp.Eq(polynomial_constant**2, polynomial_constant),
        polynomial_constant,
    )
    origin_no_nontrivial_generated_role = origin_projector_solutions == [0, 1]
    unequal_rank_quotient_certificate = projector_pass and {P1.rank(), P2.rank()} == {1, 2}

    # Continuous and improper O(3) generator controls.
    theta = sp.symbols("theta", real=True)
    rotation_12 = sp.Matrix([
        [sp.cos(theta), -sp.sin(theta), 0],
        [sp.sin(theta), sp.cos(theta), 0],
        [0, 0, 1],
    ])
    rotation_13 = sp.Matrix([
        [sp.cos(theta), 0, -sp.sin(theta)],
        [0, 1, 0],
        [sp.sin(theta), 0, sp.cos(theta)],
    ])
    rotation_23 = sp.Matrix([
        [1, 0, 0],
        [0, sp.cos(theta), -sp.sin(theta)],
        [0, sp.sin(theta), sp.cos(theta)],
    ])
    reflection = sp.diag(-1, 1, 1)
    Q_reflected = sp.simplify(reflection * Q * reflection.T)
    invariance_residuals: dict[str, sp.Expr] = {
        "reflection_I2": sp.simplify(sp.trace(Q_reflected**2) - I2),
        "reflection_I3": sp.simplify(sp.trace(Q_reflected**3) - I3),
    }
    for label, rotation in {
        "rotation_12": rotation_12,
        "rotation_13": rotation_13,
        "rotation_23": rotation_23,
    }.items():
        Q_rotated = sp.simplify(rotation * Q * rotation.T)
        invariance_residuals[f"{label}_I2"] = sp.trigsimp(sp.trace(Q_rotated**2) - I2)
        invariance_residuals[f"{label}_I3"] = sp.trigsimp(sp.trace(Q_rotated**3) - I3)
    invariance_pass = all(sp.simplify(value) == 0 for value in invariance_residuals.values())

    # O(3) has a central kernel {+I,-I}; the faithful relabel action is
    # O(3)/{+I,-I}, isomorphic to SO(3).  This is not the ill-defined O(3)/SO(3).
    proper_partner = -reflection
    faithful_group_control = all((
        reflection.det() == -1,
        proper_partner.det() == 1,
        matrix_is_zero(
            sp.simplify(
                proper_partner * Q * proper_partner.T
                - reflection * Q * reflection.T
            )
        ),
    ))

    # Controls for class boundary and target leakage.
    q2x, q2y = sp.symbols("q2x q2y", real=True)
    Q2 = sp.Matrix([[q2x, q2y], [q2y, -q2x]])
    n2_cubic_zero = sp.simplify(sp.trace(Q2**3)) == 0
    n2_characteristic = sp.factor(Q2.charpoly().as_expr())
    n2_expected_characteristic = sp.Symbol("lambda")**2 - q2x**2 - q2y**2
    n2_equal_rank_control = (
        n2_cubic_zero
        and sp.expand(n2_characteristic - n2_expected_characteristic) == 0
    )
    n1_traceless_control = sp.Matrix([[0]]).rank() == 0
    N, t_general = sp.symbols("N t_general", integer=True, positive=True)
    general_n_I2 = N * (N - 1) * t_general**2
    general_n_I3 = N * (N - 1) * (N - 2) * t_general**3
    general_n_ratio_squared = sp.simplify(general_n_I3**2 / general_n_I2**3)
    expected_general_n_ratio_squared = (N - 2) ** 2 / (N * (N - 1))
    general_n_control = all((
        sp.simplify(general_n_ratio_squared - expected_general_n_ratio_squared) == 0,
        sp.simplify(general_n_ratio_squared.subs(N, 2)) == 0,
        sp.simplify(general_n_ratio_squared.subs(N, 3)) == sp.Rational(1, 6),
        sp.simplify(general_n_ratio_squared.subs(N, 4)) == sp.Rational(1, 3),
    ))
    n3_claim_narrowly_minimal = (
        n1_traceless_control
        and n2_cubic_zero
        and I3_star != 0
        and general_n_control
    )
    within_class_minimal_control = (
        n1_traceless_control
        and n2_equal_rank_control
        and n3_claim_narrowly_minimal
        and projector_pass
    )

    unit_uniaxial = sp.sqrt(sp.Rational(3, 2)) * sp.diag(
        sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3)
    )
    unit_biaxial = sp.diag(1 / sp.sqrt(2), -1 / sp.sqrt(2), 0)
    b_zero_degeneracy_control = all((
        sp.simplify(sp.trace(unit_uniaxial**2)) == 1,
        sp.simplify(sp.trace(unit_biaxial**2)) == 1,
        sp.simplify(sp.trace(unit_uniaxial**3)) != sp.simplify(sp.trace(unit_biaxial**3)),
    ))
    stable_origin_null_potential = alpha * I2 / 2 + c * I2**2 / 4
    stable_origin_null_hessian = sp.simplify(
        sp.hessian(stable_origin_null_potential, coordinates).subs(zero_substitution)
    )
    stable_origin_control = matrix_is_zero(stable_origin_null_hessian - alpha * gram)

    c_negative_magnitude = sp.symbols("c_negative_magnitude", positive=True, real=True)
    c_zero_unbounded_control = sp.limit(reduced_potential.subs(c, 0), r, sp.oo) == -sp.oo
    c_negative_unbounded_control = (
        sp.limit(reduced_potential.subs(c, -c_negative_magnitude), r, sp.oo) == -sp.oo
    )
    alpha_zero_marginal_control = matrix_is_zero(origin_hessian.subs(alpha, 0))
    coercivity_boundary_control = all((
        c_zero_unbounded_control,
        c_negative_unbounded_control,
        alpha_zero_marginal_control,
    ))

    sign_flip_substitution = {variable: -variable for variable in coordinates}
    potential_at_minus_Q = sp.expand(potential.subs(sign_flip_substitution, simultaneous=True))
    polarity_mirror_residual = sp.simplify(potential_at_minus_Q - potential.subs(b, -b))
    polarity_control = polarity_mirror_residual == 0

    h = sp.symbols("h", nonzero=True, real=True)
    prewired_potential = potential - h * x
    prewired_origin_gradient = sp.simplify(
        sp.Matrix([
            sp.diff(prewired_potential, variable) for variable in coordinates
        ]).subs(zero_substitution)
    )
    prewired_source_rejected = prewired_origin_gradient[0] == -h and any(
        entry != 0 for entry in prewired_origin_gradient
    )
    rank_swap_is_not_gauge = P1.rank() != P2.rank()
    controls_pass = all((
        within_class_minimal_control,
        b_zero_degeneracy_control,
        stable_origin_control,
        coercivity_boundary_control,
        polarity_control,
        negative_stationary_branch_rejected,
        faithful_group_control,
        rank_swap_is_not_gauge,
        prewired_source_rejected,
    ))

    source_phrases_present = all((
        "დროის არმქონე კანდიდატში თვითგარჩევა შეიძლება იყოს ამონახსნთა სტრუქტურული არჩევა" in paths["W2_C0"].read_text(encoding="utf-8"),
        "ერთი წინასივრცითი და წინასაათური ფუძის" in paths["INTUITIVE"].read_text(encoding="utf-8"),
        "ყველაფერი სხვა გადასინჯვადია" in paths["CODES"].read_text(encoding="utf-8"),
    ))

    candidate_exact_pass = all((
        required_fields_present,
        contract_values_nonempty,
        text_sequences_valid,
        version_bound,
        semantic_contract_bound,
        registries_bound,
        primitive_values_nonblank,
        freedom_ledger_complete,
        gate_applicability_complete,
        dependency_chain_valid,
        dependency_f1_open,
        route_registration_valid,
        target_leakage_absent,
        source_phrases_present,
        origin_pass,
        global_classification_pass,
        stationary_classification_pass,
        quotient_stability_pass,
        unequal_rank_quotient_certificate,
        origin_no_nontrivial_generated_role,
        invariance_pass,
        controls_pass,
    ))

    closure_flags = dict(INITIAL_CLOSURE_FLAGS)
    closure_flags["G0_GOAL"] = all((
        required_fields_present, contract_values_nonempty, text_sequences_valid,
        version_bound, semantic_contract_bound, registries_bound, primitive_values_nonblank,
        freedom_ledger_complete, gate_applicability_complete,
    ))
    closure_flags["G1_CONVENTIONS"] = closure_flags["G0_GOAL"] and all((
        dependency_chain_valid, dependency_f1_open, route_registration_valid,
        target_leakage_absent, source_phrases_present,
    ))
    closure_flags["G2_CORE_ALGEBRA"] = closure_flags["G1_CONVENTIONS"] and all((
        origin_pass, global_classification_pass, projector_pass, invariance_pass,
    ))
    closure_flags["G3_STRUCTURE"] = closure_flags["G2_CORE_ALGEBRA"] and all((
        quotient_stability_pass, unequal_rank_quotient_certificate,
        origin_no_nontrivial_generated_role,
    ))
    closure_flags["G4_INDEPENDENT_CHECK"] = closure_flags["G3_STRUCTURE"] and all((
        sharp_bound_residual == 0,
        stationary_classification_pass,
        matrix_is_zero(mode_hessian_residual),
    ))
    closure_flags["G5_LIMITS_REGRESSION"] = closure_flags["G4_INDEPENDENT_CHECK"] and controls_pass
    closure_flags["ATEMPORAL_SPECTRAL_SPLIT_EXACT"] = candidate_exact_pass
    closure_flags["QUOTIENT_STABILITY_EXACT"] = candidate_exact_pass and quotient_stability_pass
    closure_flags["W2_F1_CONDITIONAL_CANDIDATE"] = candidate_exact_pass
    # Programme-wide physical promotion is deliberately a separate future audit.
    closure_flags["W2_F1_SELF_DIFFERENTIATION"] = False
    physical_flags_honest = not any(
        closure_flags[key]
        for key in (
            "W2_F1_SELF_DIFFERENTIATION", "W2_F2_OPERATIONAL_RELATIONS",
            "W2_F3_INTERNAL_ORDER_CAUSALITY", "W2_F4_INDEPENDENT_ADDITIVE_MODES",
            "W2_M1_DIMENSION_CONTINUUM", "W2_M2_LORENTZIAN_METRIC",
            "W2_A0_EFFECTIVE_ACTION_ORIGIN", "G6_PHYSICAL_MATCH",
            "G7_OBSERVATION", "G8_EXPORT",
        )
    )
    certified_pass = candidate_exact_pass and physical_flags_honest

    return {
        "MODEL_VERSION": MODEL_VERSION,
        "STATUS": (
            "EXACT_ATEMPORAL_SPECTRAL_CANDIDATE_PASS__W2_F1_PROMOTION_OPEN"
            if certified_pass
            else "ATEMPORAL_SPECTRAL_CANDIDATE_FAIL__W2_F1_OPEN"
        ),
        "CHECKS": {
            "required_contract_and_custom_fields_present": required_fields_present,
            "contract_values_nonempty": contract_values_nonempty,
            "required_text_sequences_valid": text_sequences_valid,
            "contract_and_runtime_model_versions_bound": version_bound,
            "semantic_contract_fields_exactly_bound": semantic_contract_bound,
            "registries_exactly_bound": registries_bound,
            "primitive_registry_values_nonblank": primitive_values_nonblank,
            "freedom_ledger_exact_and_complete": freedom_ledger_complete,
            "G0_to_G8_applicability_complete": gate_applicability_complete,
            "dependencies_reexecuted_status_version_exact": dependency_chain_valid,
            "dependency_physical_F1_flags_open": dependency_f1_open,
            "atemporal_route_registered_and_open": route_registration_valid,
            "target_leakage_absent": target_leakage_absent,
            "source_boundary_phrases_present": source_phrases_present,
            "internal_coordinate_gram_positive": gram_pass,
            "origin_stationary_and_strictly_unstable": origin_pass,
            "sharp_discriminant_bound_and_global_orbit": global_classification_pass,
            "independent_stationary_branches_and_energy_order": stationary_classification_pass,
            "O3_invariance_exact": invariance_pass,
            "faithful_O3_mod_center_action_not_O3_mod_SO3": faithful_group_control,
            "orbit_normal_hessian_positive_with_only_orbit_zero_modes": quotient_stability_pass,
            "Q_generated_rank_1_rank_2_projectors": unequal_rank_quotient_certificate,
            "origin_has_no_nontrivial_Q_generated_projector": origin_no_nontrivial_generated_role,
            "N1_N2_N4_generalN_b0_polarity_coercivity_and_source_controls": controls_pass,
            "all_physical_and_export_flags_honestly_open": physical_flags_honest,
        },
        "EXACT_DIAGNOSTICS": {
            "I2": str(I2),
            "I3": str(I3),
            "sharp_bound_residual": str(sharp_bound_residual),
            "reduced_derivative_residual": str(reduced_derivative_residual),
            "s_star": str(s_star),
            "s_minus": str(s_minus),
            "negative_root_biaxial_eigenvalue": str(negative_root_biaxial_eigenvalue),
            "s_stationary_residual": str(s_stationary_residual),
            "r_star": str(r_star),
            "r_minus": str(r_minus),
            "radius_relation_residual": str(radius_relation_residual),
            "Q_star_representative": str(Q_star),
            "star_gradient_residual": str(star_gradient_residual),
            "star_energy_on_shell": str(star_energy_on_shell),
            "stationary_E_plus_minus_E_minus": str(sp.simplify(energy_plus - energy_minus)),
            "stationary_energy_order_residual": str(energy_order_residual),
            "eom_gradient_pairing_residual": str(eom_gradient_residual),
            "mode_gram": str(mode_gram),
            "mode_hessian": str(mode_hessian),
            "mode_hessian_residual": str(mode_hessian_residual),
            "orbit_normal_transverse_eigenvalues": {
                "radial": str(radial_eigenvalue.subs({s: s_star})),
                "biaxial_multiplicity_2": str(biaxial_eigenvalue.subs({s: s_star})),
                "orbit_gauge_multiplicity_2": "0",
            },
            "P1": str(P1),
            "P2": str(P2),
            "projector_ranks": [P1.rank(), P2.rank()],
            "origin_projector_constants": [str(value) for value in origin_projector_solutions],
            "N2_characteristic": str(n2_characteristic),
            "general_N_cubic_ratio_squared": str(general_n_ratio_squared),
            "polarity_mirror_residual": str(polarity_mirror_residual),
            "prewired_origin_gradient": str(prewired_origin_gradient),
        },
        "SCOPE_CEILING": (
            "CONDITIONAL_EXACT_ATEMPORAL_F1_CANDIDATE; imported internal algebra and "
            "variational law; no F2, spacetime, RefG effective physics or observation"
        ),
        "IMPORTED_NOT_DERIVED": list(EXPECTED_IMPORTED_NOT_DERIVED),
        "DEFERRED_OUTPUTS": list(EXPECTED_DEFERRED_OUTPUTS),
        "DEPENDENCY_STATUSES": dependency_statuses,
        "DEPENDENCY_VERSIONS": dependency_versions,
        "NEXT_ATOMIC_TASK": (
            "Audit whether the imported Sym_0(3,R) algebra and atemporal argmin law are an "
            "acceptable RefG F1 realization rather than only a conditional mathematical "
            "construction; compare it against the seed route and either promote exactly this "
            "frozen candidate or keep programme-wide W2_F1 open."
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
    return 0 if report["STATUS"].startswith("EXACT_ATEMPORAL") else 1


if __name__ == "__main__":
    raise SystemExit(main())
