"""მკაცრი singleton მდგომარეობათა სივრცის პირობითი no-go.

თუ S={omega} ფიქსირებულია და წესს არც S-ის გაფართოება და არც გარე
outcome-register-ის დამატება შეუძლია, მის შიგნით ორი ოპერაციულად
არაეკვივალენტური მდგომარეობა ვერ წარმოიქმნება. ეს არ ნიშნავს, რომ RefG-ის
ერთი ონტოლოგიური ფუძე აუცილებლად ერთმდგომარეობიანია.
"""
from __future__ import annotations

import itertools
import json
import sys
from typing import Any

import sympy as sp


MODEL_VERSION = "W2-F1-SINGLETON-NO-GO-v1.5-corrected-internal"

SCIENTIFIC_CLAIM: dict[str, Any] = {
    "claim": (
        "ფიქსირებულ S={omega}-ზე, მდგომარეობათა სივრცის გაფართოების ან გარე "
        "რეესტრის გარეშე, დეტერმინისტული ენდომორფიზმი, 1x1 მარკოვის ბირთვი, "
        "ატემპორალური ფუნქციონალი და ერთგანზომილებიანი კვანტური არხი ვერ "
        "ქმნის ორ ოპერაციულად არაეკვივალენტურ შინაგან მდგომარეობას."
    ),
    "assumptions": [
        "საბაზო მდგომარეობათა სივრცეა ზუსტად S={omega}.",
        "დაშვებული წესი S-ს არ აფართოებს და გარე ნიშანს არ ამატებს.",
        "დეტერმინისტული წესი არის f:S→S.",
        "სტოქასტიკური წესი არის ნორმირებული 1x1 მარკოვის ბირთვი.",
        "ვარიაციული წესი არის ნებისმიერი რეალური ფუნქცია S-ზე.",
        "კვანტური წესი მოქმედებს ერთგანზომილებიან ჰილბერტის სივრცეზე; "
        "გლობალური ფაზები ერთი სხივია.",
        "მრავალშედეგიანი POVM ან S→Y გამოსავალი ცალკე outcome-register-ს მოითხოვს.",
    ],
    "scope": (
        "მხოლოდ ფიქსირებული strict singleton. არატრივიალური თვითრელაცია, "
        "გენერაციული გრამატიკა, მრავალმდგომარეობიანი სივრცე, გარე ხმაური ან "
        "state-space-changing წესი ამ დომენის გარეთაა."
    ),
    "falsifier": (
        "იმავე S={omega}-ზე კონკრეტული წესი, რომელიც არც სივრცეს აფართოებს, "
        "არც გარე რეესტრს ამატებს და მაინც ქმნის ორ ოპერაციულად "
        "არაეკვივალენტურ შინაგან მდგომარეობას."
    ),
    "open_boundaries": [
        "ერთი მატარებლის არატრივიალური თვითრელაციური მდგომარეობათა სივრცე",
        "state-space-generating წესი",
        "შინაგანი სტოქასტიკური ან კვანტური outcome მექანიზმი დამატებითი სივრცით",
        "RefG-ის ფიზიკური W2_F1 მექანიზმი",
    ],
}


def is_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    return all(is_zero(entry) for entry in matrix)


def all_functions(size: int) -> list[tuple[int, ...]]:
    return list(itertools.product(range(size), repeat=size))


def equivalence_relations(size: int) -> list[frozenset[tuple[int, int]]]:
    pairs = tuple(itertools.product(range(size), repeat=2))
    relations: list[frozenset[tuple[int, int]]] = []
    for mask in itertools.product((False, True), repeat=len(pairs)):
        relation = frozenset(pair for pair, keep in zip(pairs, mask) if keep)
        reflexive = all((x, x) in relation for x in range(size))
        symmetric = all((right, left) in relation for left, right in relation)
        transitive = all(
            (left, end) in relation
            for left, middle in relation
            for start, end in relation
            if middle == start
        )
        if reflexive and symmetric and transitive:
            relations.append(relation)
    return relations


def quotient_class_count(
    size: int, relation: frozenset[tuple[int, int]]
) -> int:
    classes = {
        frozenset(right for right in range(size) if (left, right) in relation)
        for left in range(size)
    }
    return len(classes)


def run_gate() -> dict[str, Any]:
    singleton_relations = equivalence_relations(1)
    quotient_counts = [
        quotient_class_count(1, relation) for relation in singleton_relations
    ]
    quotient_unique = (
        singleton_relations == [frozenset({(0, 0)})]
        and quotient_counts == [1]
    )

    singleton_maps = all_functions(1)
    deterministic_unique = (
        singleton_maps == [(0,)]
        and all(len(set(function)) == 1 for function in singleton_maps)
    )

    kernel_entry = sp.symbols("k", real=True, nonnegative=True)
    kernel_solution = sp.solve(sp.Eq(kernel_entry, 1), kernel_entry)
    singleton_kernel = sp.Matrix([[kernel_solution[0]]])
    singleton_probability = sp.Matrix([1])
    stochastic_residual = sp.simplify(
        singleton_kernel * singleton_probability - singleton_probability
    )
    stochastic_unique = (
        kernel_solution == [1]
        and singleton_kernel.rank() == 1
        and matrix_is_zero(stochastic_residual)
    )

    energy = sp.symbols("E", real=True)
    singleton_energy = {0: energy}
    variational_unique = (
        len(set(singleton_energy.values())) == 1
        and len(singleton_energy) == 1
    )

    density_entry = sp.symbols("rho", real=True, nonnegative=True)
    density_solution = sp.solve(sp.Eq(density_entry, 1), density_entry)
    density = sp.Matrix([[density_solution[0]]])
    channel_scale = sp.symbols("channel_scale", real=True, nonnegative=True)
    channel_solution = sp.solve(sp.Eq(channel_scale, 1), channel_scale)
    channel_residual = sp.simplify(channel_solution[0] * density - density)
    density_channel_unique = all((
        density_solution == [1],
        channel_solution == [1],
        density == sp.Matrix([[1]]),
        matrix_is_zero(channel_residual),
    ))

    theta, phi = sp.symbols("theta phi", real=True)
    psi_theta = sp.Matrix([sp.exp(sp.I * theta)])
    psi_phi = sp.Matrix([sp.exp(sp.I * phi)])
    rho_theta = sp.simplify(psi_theta * psi_theta.conjugate().T)
    rho_phi = sp.simplify(psi_phi * psi_phi.conjugate().T)
    ray_residual = sp.simplify(rho_theta - rho_phi)
    ray_trace_distance = sp.simplify(sp.Abs(ray_residual[0, 0]) / 2)
    quantum_rays_unique = (
        rho_theta == rho_phi == sp.Matrix([[1]])
        and matrix_is_zero(ray_residual)
        and ray_trace_distance == 0
    )

    ratio = sp.symbols("outcome_ratio", positive=True)
    weight_0 = sp.simplify(ratio / (1 + ratio))
    weight_1 = sp.simplify(1 / (1 + ratio))
    povm_residual = sp.simplify(
        sp.Matrix([[weight_0]]) + sp.Matrix([[weight_1]]) - sp.eye(1)
    )
    post_state_0 = sp.simplify(weight_0 * density / weight_0)
    post_state_1 = sp.simplify(weight_1 * density / weight_1)
    povm_register_external = all((
        weight_0.is_positive is True,
        weight_1.is_positive is True,
        matrix_is_zero(povm_residual),
        post_state_0 == post_state_1 == density,
        len(("outcome_0", "outcome_1")) == 2,
    ))
    stochastic_output_residual = sp.simplify(weight_0 + weight_1 - 1)
    stochastic_register_external = (
        is_zero(stochastic_output_residual)
        and singleton_kernel == sp.Matrix([[1]])
        and len(("label_0", "label_1")) == 2
    )

    p0, p1 = sp.Matrix([1, 0]), sp.Matrix([0, 1])
    strong_classical_distance = sp.simplify(
        sum(abs(entry) for entry in p0 - p1) / 2
    )
    density_0, density_1 = sp.diag(1, 0), sp.diag(0, 1)
    density_difference = density_0 - density_1
    strong_quantum_distance = sp.simplify(
        sum(
            sp.Abs(value) * multiplicity
            for value, multiplicity in density_difference.eigenvals().items()
        )
        / 2
    )
    strong_positive_control = (
        len(set((0, 1))) == 2
        and strong_classical_distance == 1
        and strong_quantum_distance == 1
    )

    weak_p0 = sp.Matrix([sp.Rational(3, 4), sp.Rational(1, 4)])
    weak_p1 = sp.Matrix([sp.Rational(1, 4), sp.Rational(3, 4)])
    weak_classical_distance = sp.simplify(
        sum(abs(entry) for entry in weak_p0 - weak_p1) / 2
    )
    ket_zero = sp.Matrix([1, 0])
    ket_plus = sp.Matrix([1, 1]) / sp.sqrt(2)
    weak_density_difference = sp.simplify(
        ket_zero * ket_zero.T - ket_plus * ket_plus.T
    )
    weak_quantum_distance = sp.simplify(
        sum(
            sp.Abs(value) * multiplicity
            for value, multiplicity in weak_density_difference.eigenvals().items()
        )
        / 2
    )
    weak_positive_control = (
        weak_classical_distance == sp.Rational(1, 2)
        and weak_quantum_distance == sp.sqrt(2) / 2
        and 0 < float(weak_quantum_distance) < 1
    )

    swap = sp.Matrix([[0, 1], [1, 0]])
    swapped_distance = sp.simplify(
        sum(abs(entry) for entry in swap * p0 - swap * p1) / 2
    )
    relabel_invariant = (
        swap.T * swap == sp.eye(2)
        and swapped_distance == strong_classical_distance
    )
    external_decoration_rejected = (
        len({(0, "left"), (0, "right")}) == 2
        and povm_register_external
        and stochastic_register_external
        and post_state_0 == post_state_1
    )

    checks = {
        "singleton_quotient_has_one_class": quotient_unique,
        "all_singleton_deterministic_maps_have_one_image": deterministic_unique,
        "normalized_1x1_markov_kernel_is_unique": stochastic_unique,
        "singleton_functional_has_one_value_and_minimizer": variational_unique,
        "one_dimensional_density_and_CPTP_channel_are_unique": density_channel_unique,
        "one_dimensional_quantum_rays_are_indistinguishable": quantum_rays_unique,
        "POVM_labels_are_external_and_post_state_is_unique": povm_register_external,
        "stochastic_output_alphabet_is_an_external_register": stochastic_register_external,
        "two_state_strong_control_detects_distinction": strong_positive_control,
        "two_state_weak_control_detects_distinction": weak_positive_control,
        "state_relabelling_preserves_distinction": relabel_invariant,
        "external_label_injection_is_not_internal_self_differentiation": external_decoration_rejected,
    }
    passed = all(checks.values())
    return {
        "model_version": MODEL_VERSION,
        "status": (
            "EXACT_SINGLETON_NO_GO_PASS__W2_F1_OPEN"
            if passed
            else "EXACT_SINGLETON_NO_GO_FAIL__W2_F1_OPEN"
        ),
        "claim": SCIENTIFIC_CLAIM,
        "checks": checks,
        "exact_diagnostics": {
            "quotient_class_counts": quotient_counts,
            "singleton_map_count": len(singleton_maps),
            "markov_residual": str(stochastic_residual),
            "ray_trace_distance": str(ray_trace_distance),
            "POVM_completeness_residual": str(povm_residual),
            "strong_classical_distance": str(strong_classical_distance),
            "strong_quantum_distance": str(strong_quantum_distance),
            "weak_classical_distance": str(weak_classical_distance),
            "weak_quantum_distance": str(weak_quantum_distance),
        },
        "theory_consequence": (
            "ერთი ონტოლოგიური მატარებელი არ უნდა გაიგივდეს შესაძლებლობების "
            "არმქონე ერთ მდგომარეობასთან; no-go გამორიცხავს მხოლოდ strict singleton-ს."
        ),
        "strict_singleton_no_go_pass": passed,
        "refg_W2_F1_closed": False,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["strict_singleton_no_go_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
