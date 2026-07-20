# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: population normal-form ledger; no new p01 signs.

"""PHASE 50 (p11h): F_min population first-set programme.

This file is a guardrail for the "first set" problem.

p11c shows that a stable oscillon population can supply its own local tempo:
dimensionless ratios survive a common transposition, and integer/rational
locks are robust attractors in toy normal forms.  That is not yet a derivation
of the particle spectrum.

The real problem is sharper:

    Which mutually compatible oscillon sets are admitted by the F_min
    nonlinearity inside the p01 stability window?

This gate closes only the scaffolding:

* all resonance constraints must live in ratio space, not in an external
  substrate clock;
* low-order integer locks are toy attractors and can be searched;
* the charged-lepton C3 chord is not derived by a simple low-order integer
  harmonic relation;
* the actual first-set calculation requires the localized oscillon profiles,
  F_min mode-coupling tensors, amplitude/frequency fixed points, and decay
  closure.
"""

from __future__ import annotations

from itertools import product
from math import cos, gcd, pi, sqrt
from typing import Iterable, Sequence

import sympy as sp


THETA_C3 = 2.0 / 9.0
SQRT2 = sqrt(2.0)


def c3_frequency_ratios(theta: float = THETA_C3) -> list[float]:
    values = sorted(
        1.0 + SQRT2 * cos(theta + 2.0 * pi * k / 3.0)
        for k in range(3)
    )
    base = values[0]
    return [value / base for value in values]


def relation_gcd(coeffs: Sequence[int]) -> int:
    g = 0
    for coeff in coeffs:
        g = gcd(g, abs(coeff))
    return g


def integer_relation_search(
    values: Sequence[float],
    max_coeff: int = 12,
    tolerance: float = 1.0e-8,
) -> list[dict[str, object]]:
    """Search primitive integer relations sum_i n_i values_i ~= 0."""
    relations = []
    for coeffs in product(range(-max_coeff, max_coeff + 1), repeat=len(values)):
        if all(coeff == 0 for coeff in coeffs):
            continue
        if relation_gcd(coeffs) != 1:
            continue
        # Avoid reporting the same relation twice with opposite sign.
        first_nonzero = next(coeff for coeff in coeffs if coeff != 0)
        if first_nonzero < 0:
            continue
        residual = sum(coeff * value for coeff, value in zip(coeffs, values))
        if abs(residual) <= tolerance:
            relations.append(
                {
                    "coeffs": coeffs,
                    "residual": residual,
                    "weight": sum(abs(coeff) for coeff in coeffs),
                }
            )
    return sorted(relations, key=lambda row: (row["weight"], row["coeffs"]))


def symbolic_transposition_of_resonance_constraints() -> dict[str, object]:
    """A resonance equation R=sum n_i omega_i=0 is scale-covariant."""
    s = sp.symbols("s", positive=True)
    n1, n2, n3 = sp.symbols("n1 n2 n3", integer=True)
    w1, w2, w3 = sp.symbols("omega1 omega2 omega3", positive=True)
    residual = n1 * w1 + n2 * w2 + n3 * w3
    scaled_residual = n1 * s * w1 + n2 * s * w2 + n3 * s * w3
    return {
        "constraint": sp.Eq(sp.Symbol("R"), residual),
        "scaled_constraint": sp.Eq(sp.Symbol("R_scaled"), scaled_residual),
        "scale_covariance_residual": sp.simplify(scaled_residual - s * residual),
        "meaning": (
            "population compatibility is a relation among ratios; gravity or "
            "pressure may transpose the local tempo without changing the lock"
        ),
    }


def candidate_population_sets() -> list[dict[str, object]]:
    return [
        {
            "name": "single_population_tempo",
            "frequency_ratios": [1.0],
            "role": "trivial seed; no mutual relation is required",
        },
        {
            "name": "integer_1_to_2_lock_toy",
            "frequency_ratios": [1.0, 2.0],
            "role": "toy Arnold-tongue relation, not a particle spectrum",
        },
        {
            "name": "c3_charged_lepton_chord",
            "frequency_ratios": c3_frequency_ratios(),
            "role": "structural C3/order-9 candidate; not a simple low-order harmonic lock",
        },
    ]


def candidate_set_relation_audit(max_coeff: int = 12) -> list[dict[str, object]]:
    rows = []
    for candidate in candidate_population_sets():
        ratios = candidate["frequency_ratios"]
        relations = []
        if len(ratios) > 1:
            relations = integer_relation_search(ratios, max_coeff=max_coeff)
        rows.append(
            {
                **candidate,
                "max_coeff": max_coeff,
                "low_order_integer_relations": relations[:5],
                "relation_count": len(relations),
                "simple_integer_lock": bool(relations),
            }
        )
    return rows


def first_set_solver_contract() -> list[dict[str, str]]:
    return [
        {
            "stage": "p01 stability window",
            "status": "UPSTREAM_AVAILABLE",
            "required_work": "choose coefficient points inside the p01 no-ghost/hyperbolicity window",
        },
        {
            "stage": "phase-normalized F_min action",
            "status": "UPSTREAM_AVAILABLE",
            "required_work": "use the p05s/p05t branch-consistent F_min action, not raw wrong-branch stress",
        },
        {
            "stage": "localized oscillon basis",
            "status": "OPEN",
            "required_work": "construct finite-energy profiles and their tail/dispersion data",
        },
        {
            "stage": "F_min mode-coupling tensor",
            "status": "OPEN",
            "required_work": "project the F_min nonlinearities onto the localized mode basis",
        },
        {
            "stage": "population fixed-point equations",
            "status": "OPEN",
            "required_work": "solve amplitude and phase-lock equations modulo common tempo scaling",
        },
        {
            "stage": "decay and exclusion closure",
            "status": "OPEN",
            "required_work": "remove modes with allowed decay channels into the already locked set",
        },
        {
            "stage": "spectral stability",
            "status": "OPEN",
            "required_work": "check the fluctuation/Floquet spectrum of the full population state",
        },
    ]


def fmin_population_first_set_gate() -> dict[str, object]:
    transposition = symbolic_transposition_of_resonance_constraints()
    relation_rows = candidate_set_relation_audit()
    c3_row = next(row for row in relation_rows if row["name"] == "c3_charged_lepton_chord")
    toy_row = next(row for row in relation_rows if row["name"] == "integer_1_to_2_lock_toy")

    scaffold_closed = (
        transposition["scale_covariance_residual"] == 0
        and toy_row["simple_integer_lock"]
        and not c3_row["simple_integer_lock"]
    )

    return {
        "status": (
            "PASS_FIRST_SET_PROGRAMME_SCAFFOLD__FMIN_ATTRACTOR_SOLVER_OPEN"
            if scaffold_closed
            else "CHECK_FIRST_SET_PROGRAMME_SCAFFOLD"
        ),
        "closed_now": [
            "population constraints are scale-covariant ratio constraints",
            "simple integer locks can be represented as toy attractor relations",
            "the C3 charged-lepton chord is not explained by a low-order integer harmonic lock",
            "the first-set problem is reduced to an F_min projected mode-coupling/fixed-point calculation",
        ],
        "relation_audit": relation_rows,
        "solver_contract": first_set_solver_contract(),
        "physical_problem_open": (
            "compute the mutually compatible F_min oscillon attractor sets "
            "inside the p01 stability window"
        ),
        "allowed_language": "population-lock programme scaffold; first-set solver open",
        "forbidden_language": "F_min has selected the particle spectrum",
        "do_not_claim": [
            "Do not claim Kuramoto/Adler toys derive the particle spectrum.",
            "Do not claim the C3 lepton chord is a simple integer harmonic lock.",
            "Do not claim the first population set is known before the F_min mode-coupling tensors are computed.",
            "Do not introduce an external substrate frequency as the selection clock.",
        ],
    }


def main() -> None:
    gate = fmin_population_first_set_gate()
    print("PHASE 50: F_min population first-set gate")
    print(f"status: {gate['status']}")
    for row in gate["relation_audit"]:
        print(
            f"{row['name']}: relations={row['relation_count']} "
            f"simple_lock={row['simple_integer_lock']}"
        )
    print(f"open: {gate['physical_problem_open']}")


if __name__ == "__main__":
    main()
