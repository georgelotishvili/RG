"""ზუსტი დადებითი კონტროლი ატემპორალური თვითგარჩევის კანდიდატისთვის.

ეს ფაილი ამტკიცებს მხოლოდ O(2)-სიმეტრიული Landau-ს სათამაშო მოდელის
ალგებრულ თვისებებს. იგი არ გამოჰყავს ეს მოდელი RefG-ის ფუძიდან და არ ხურავს
ფიზიკურ W2_F1-ს.
"""
from __future__ import annotations

import json
import sys
from typing import Any

import sympy as sp


MODEL_VERSION = "W2-F1-RADIAL-LANDAU-v1.2-frozen"

SCIENTIFIC_CLAIM: dict[str, Any] = {
    "claim": (
        "q=(q1,q2)-ზე V=(a/2)(q·q)+(lambda/4)(q·q)^2 პოტენციალს "
        "lambda>0-ისას a>0-ზე სტაბილური ნულოვანი ტოტი აქვს, ხოლო a<0-ზე "
        "არანულოვანი გლობალური მინიმუმების O(2)-ორბიტა."
    ),
    "assumptions": [
        "q არის გარედან მოცემული ორკომპონენტიანი რეალური შიდა პარამეტრი.",
        "lambda>0; გატეხილ ტოტზე a<0; ნულოვან კონტროლში a>0.",
        "მდგომარეობა განისაზღვრება ატემპორალური პირობით grad(V)=0.",
        "R^2, O(2), კვარტიკული ფორმა და a-ს ნიშანი ფუძიდან გამოყვანილი არაა.",
    ],
    "scope": (
        "სტატიკური სასრულგანზომილებიანი სათამაშო მოდელი; q არ არის სივრცე, დრო, "
        "მეტრიკა, ფუძის წნევა ან დაკვირვებადი ველი; a=0 გამორიცხულია."
    ),
    "falsifier": (
        "იმავე დაშვებებით არანულოვანი გრადიენტული/ჰესიანური ნაშთი, a<0-ზე "
        "არანულოვანი მინიმუმის არყოფნა, a>0-ზე რეალური არანულოვანი მინიმუმი "
        "ან O(2)-გარდაქმნისას V-ის ცვლილება."
    ),
    "open_boundaries": [
        "კანდიდატის ფუძიდან წარმოშობა",
        "q-ს ფიზიკური მნიშვნელობა და დაკვირვებადი რუკა",
        "მიზეზობრიობა, გავრცელება და ფიზიკური თავისუფლების ხარისხები",
        "სრული W2_F1 თვითგარჩევა",
    ],
}


def is_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    return all(is_zero(entry) for entry in matrix)


def run_gate() -> dict[str, Any]:
    q1, q2, a = sp.symbols("q1 q2 a", real=True)
    lam, r, mu, alpha = sp.symbols("lambda r mu alpha", positive=True)
    h = sp.symbols("h", real=True, nonzero=True)
    theta = sp.symbols("theta", real=True)

    q = sp.Matrix([q1, q2])
    norm_sq = sp.expand(q.dot(q))
    potential = a * norm_sq / 2 + lam * norm_sq**2 / 4
    gradient = sp.Matrix([sp.diff(potential, variable) for variable in q])
    hessian = sp.hessian(potential, (q1, q2))
    expected_gradient = (a + lam * norm_sq) * q
    expected_hessian = (
        (a + lam * norm_sq) * sp.eye(2) + 2 * lam * q * q.T
    )
    gradient_residual = sp.simplify(gradient - expected_gradient)
    hessian_residual = sp.simplify(hessian - expected_hessian)

    null_substitution = {q1: 0, q2: 0, a: mu**2}
    null_gradient = sp.simplify(gradient.subs(null_substitution))
    null_hessian = sp.simplify(hessian.subs(null_substitution))
    null_required_norm_sq = -mu**2 / lam
    null_control = all((
        matrix_is_zero(null_gradient),
        null_hessian == mu**2 * sp.eye(2),
        null_required_norm_sq.is_negative is True,
    ))

    broken_substitution = {q1: r, q2: 0, a: -lam * r**2}
    broken_gradient = sp.simplify(gradient.subs(broken_substitution))
    broken_hessian = sp.simplify(hessian.subs(broken_substitution))
    broken_energy_gap = sp.simplify(
        potential.subs(broken_substitution)
        - potential.subs({q1: 0, q2: 0})
    )
    completed_square = (
        lam * (norm_sq + a / lam) ** 2 / 4 - a**2 / (4 * lam)
    )
    completed_square_residual = sp.simplify(potential - completed_square)
    nonnegative_square = lam * (norm_sq + a / lam) ** 2 / 4

    broken_origin_hessian = sp.simplify(
        hessian.subs({q1: 0, q2: 0, a: -mu**2})
    )
    origin_unstable = broken_origin_hessian == -mu**2 * sp.eye(2)
    radial_vector = sp.Matrix([r, 0])
    tangent_vector = sp.Matrix([0, r])
    radial_residual = sp.simplify(
        broken_hessian * radial_vector - 2 * lam * r**2 * radial_vector
    )
    tangent_residual = sp.simplify(broken_hessian * tangent_vector)
    broken_branch = all((
        matrix_is_zero(broken_gradient),
        broken_hessian == sp.diag(2 * lam * r**2, 0),
        broken_energy_gap == -lam * r**4 / 4,
        is_zero(completed_square_residual),
        nonnegative_square.is_nonnegative is True,
        is_zero(nonnegative_square.subs(broken_substitution)),
        origin_unstable,
        matrix_is_zero(radial_residual),
        matrix_is_zero(tangent_residual),
    ))

    rotation = sp.Matrix([
        [sp.cos(theta), -sp.sin(theta)],
        [sp.sin(theta), sp.cos(theta)],
    ])
    improper = sp.diag(1, -1) * rotation
    transformed_residuals: list[sp.Expr] = []
    for transform, determinant in ((rotation, 1), (improper, -1)):
        transformed_q = transform * q
        transformed_norm = sp.trigsimp(sp.expand(transformed_q.dot(transformed_q)))
        transformed_potential = (
            a * transformed_norm / 2 + lam * transformed_norm**2 / 4
        )
        transformed_residuals.extend([
            *(transform.T * transform - sp.eye(2)).applyfunc(sp.trigsimp),
            sp.trigsimp(transform.det() - determinant),
            sp.trigsimp(transformed_norm - norm_sq),
            sp.trigsimp(sp.expand(transformed_potential - potential)),
        ])
    o2_invariance = all(is_zero(value) for value in transformed_residuals)

    open_a = -alpha
    open_norm_sq = alpha / lam
    open_map_determinant = sp.simplify(
        sp.Matrix([open_a, lam]).jacobian((alpha, lam)).det()
    )
    open_region = all((
        open_a.is_negative is True,
        open_norm_sq.is_positive is True,
        is_zero(open_a + lam * open_norm_sq),
        open_map_determinant == -1,
    ))

    rho = sp.symbols("rho", real=True)
    radial_potential = a * rho**2 / 2 + lam * rho**4 / 4
    radial_first = sp.diff(radial_potential, rho)
    radial_second = sp.diff(radial_potential, rho, 2)
    independent_radial_check = all((
        is_zero(radial_first.subs({rho: r, a: -lam * r**2})),
        is_zero(
            radial_second.subs({rho: r, a: -lam * r**2})
            - 2 * lam * r**2
        ),
    ))

    prewired_potential = potential - h * q1
    prewired_gradient = sp.Matrix([
        sp.diff(prewired_potential, variable) for variable in q
    ])
    prewired_at_origin = sp.simplify(
        prewired_gradient.subs({q1: 0, q2: 0})
    )
    prewired_rejected = prewired_at_origin == sp.Matrix([-h, 0])

    checks = {
        "declared_symbol_inventory_exact": (
            potential.free_symbols == {q1, q2, a, lam}
        ),
        "gradient_hessian_exact": (
            matrix_is_zero(gradient_residual)
            and matrix_is_zero(hessian_residual)
        ),
        "stable_null_branch_for_a_positive": null_control,
        "unstable_origin_and_global_nonzero_branch_for_a_negative": broken_branch,
        "O2_invariance_exact": o2_invariance,
        "broken_branch_exists_on_open_parameter_region": open_region,
        "independent_radial_derivation": independent_radial_check,
        "prewired_direction_rejected": prewired_rejected,
    }
    passed = all(checks.values())
    return {
        "model_version": MODEL_VERSION,
        "status": (
            "EXACT_IDENTITY_PASS__TOY_POSITIVE_CONTROL__W2_F1_OPEN"
            if passed
            else "EXACT_IDENTITY_FAIL__TOY_POSITIVE_CONTROL__W2_F1_OPEN"
        ),
        "claim": SCIENTIFIC_CLAIM,
        "checks": checks,
        "exact_residuals": {
            "gradient": str(gradient_residual),
            "hessian": str(hessian_residual),
            "completed_square": str(completed_square_residual),
            "open_region_stationarity": str(open_a + lam * open_norm_sq),
            "prewired_origin_gradient": str(prewired_at_origin),
        },
        "toy_positive_control_pass": passed,
        "refg_W2_F1_closed": False,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["toy_positive_control_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
