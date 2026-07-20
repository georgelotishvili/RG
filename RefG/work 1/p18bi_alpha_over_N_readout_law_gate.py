from __future__ import annotations

import math
from dataclasses import dataclass

from p18bb_internal_external_em_readout_split_gate import (
    ALPHA_INV_OBSERVED_LOW,
    QED_B1_THREE_LEPTONS,
)
from p18be_q_em_source_budget_gate import q_em_source_budget
from p18bg_closed_alpha_formula_boundary_lock_gate import (
    closed_alpha_candidate_with_sigma,
)
from p18bh_boundary_slot_count_theorem_gate import (
    existing_gate_support,
    slot_count_ledger,
)
from p18z_canonical_maxwell_normalization_gate import (
    derive_canonical_maxwell_normalization_gate,
)


@dataclass(frozen=True)
class ReadoutLawCandidate:
    label: str
    q_boundary: float
    alpha_inv_predicted: float
    miss_alpha_inv: float
    miss_ppm: float
    weak_coupling_limit_ok: bool
    hidden_slot_symmetry_ok: bool
    self_consistent: bool
    verdict: str


@dataclass(frozen=True)
class UniquenessLedger:
    coupling_variable: str
    hidden_slot_count: int
    law: str
    assumptions: tuple[str, ...]
    rejected_readings: tuple[str, ...]
    predicted_alpha_inv: float
    observed_alpha_inv: float
    miss_ppm: float


def solve_with_q_law(
    internal_alpha_inv: float,
    hidden_slots: int,
    law: str,
) -> tuple[float, float]:
    """Return (alpha_inv, q_boundary) for a self-consistent q law.

    law values:
      alpha_over_N: q = alpha/N = 1/(N*y)
      sqrt_alpha_over_N: q = sqrt(alpha)/N = 1/(N*sqrt(y))
      alpha: q = alpha = 1/y
      alpha_over_N2: q = alpha/N^2 = 1/(N^2*y)
      constant_over_N: q = 1/N
    """

    if law == "alpha_over_N":
        predicted = _solve_quadratic_alpha_over_N(internal_alpha_inv, hidden_slots)
    elif law == "alpha_over_N2":
        predicted = _solve_quadratic_alpha_over_N(
            internal_alpha_inv,
            hidden_slots * hidden_slots,
        )
    elif law == "alpha":
        predicted = _solve_quadratic_alpha_over_N(internal_alpha_inv, 1)
    elif law == "sqrt_alpha_over_N":
        predicted = _solve_by_bisection(
            internal_alpha_inv,
            lambda y: 1.0 / (hidden_slots * math.sqrt(y)),
        )
    elif law == "constant_over_N":
        predicted = internal_alpha_inv - QED_B1_THREE_LEPTONS / hidden_slots
    else:
        raise ValueError(f"unknown law: {law}")

    if law == "alpha_over_N":
        q = 1.0 / (hidden_slots * predicted)
    elif law == "alpha_over_N2":
        q = 1.0 / (hidden_slots * hidden_slots * predicted)
    elif law == "alpha":
        q = 1.0 / predicted
    elif law == "sqrt_alpha_over_N":
        q = 1.0 / (hidden_slots * math.sqrt(predicted))
    else:
        q = 1.0 / hidden_slots

    return predicted, q


def _solve_quadratic_alpha_over_N(internal_alpha_inv: float, denominator: int) -> float:
    discriminant = (
        internal_alpha_inv**2 - 4.0 * QED_B1_THREE_LEPTONS / denominator
    )
    if discriminant <= 0.0:
        raise ValueError("no positive large root")
    return (internal_alpha_inv + math.sqrt(discriminant)) / 2.0


def _solve_by_bisection(
    internal_alpha_inv: float,
    q_of_y,
) -> float:
    def residual(y: float) -> float:
        return y - internal_alpha_inv + QED_B1_THREE_LEPTONS * q_of_y(y)

    lo = 1.0
    hi = internal_alpha_inv
    for _ in range(140):
        mid = (lo + hi) / 2.0
        if residual(lo) * residual(mid) <= 0.0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def readout_law_candidates() -> tuple[ReadoutLawCandidate, ...]:
    closed = closed_alpha_candidate_with_sigma()
    internal = closed.internal_threshold_alpha_inv
    N = closed.boundary_hidden_count

    definitions = (
        (
            "alpha_over_N",
            True,
            True,
            "PASS: weak Maxwell probability alpha averaged over N hidden boundary slots",
        ),
        (
            "sqrt_alpha_over_N",
            True,
            True,
            "REJECT: amplitude-level law uses sqrt(alpha), not a probability/energy readout",
        ),
        (
            "alpha",
            True,
            False,
            "REJECT: ignores hidden-slot dilution by N",
        ),
        (
            "alpha_over_N2",
            True,
            True,
            "REJECT: double-divides by the hidden-slot count",
        ),
        (
            "constant_over_N",
            False,
            True,
            "REJECT: does not vanish when Maxwell coupling alpha goes to zero",
        ),
    )

    rows: list[ReadoutLawCandidate] = []
    for law, weak_ok, symmetry_ok, verdict in definitions:
        predicted, q = solve_with_q_law(internal, N, law)
        miss = predicted - ALPHA_INV_OBSERVED_LOW
        rows.append(
            ReadoutLawCandidate(
                label=law,
                q_boundary=q,
                alpha_inv_predicted=predicted,
                miss_alpha_inv=miss,
                miss_ppm=1.0e6 * miss / ALPHA_INV_OBSERVED_LOW,
                weak_coupling_limit_ok=weak_ok,
                hidden_slot_symmetry_ok=symmetry_ok,
                self_consistent=abs(
                    predicted - internal + QED_B1_THREE_LEPTONS * q
                )
                < 1.0e-12,
                verdict=verdict,
            )
        )
    return tuple(rows)


def uniqueness_ledger() -> UniquenessLedger:
    closed = closed_alpha_candidate_with_sigma()
    support = existing_gate_support()
    maxwell = derive_canonical_maxwell_normalization_gate()

    assumptions = (
        "p18bh supplies N_boundary=34 hidden boundary slots.",
        "p18f/p18h leave exactly two physical external helicity readout channels; theta is not a third external channel.",
        "p18z identifies alpha as the squared canonical Maxwell coupling, so leading weak readout probability/energy is proportional to alpha.",
        "The hidden slots are indistinguishable at the boundary-readout level, so the unresolved readout is the symmetric average over N slots.",
        "The correction must vanish as alpha -> 0 and must be first order in the weak Maxwell readout.",
    )
    rejected = (
        "q=1/N: leaves a deficit even with zero Maxwell coupling.",
        "q=sqrt(alpha)/N: amplitude-level, too large, and not an energy/probability readout.",
        "q=alpha: ignores the hidden-slot dilution.",
        "q=alpha/N^2: averages twice over the same hidden slots.",
        "N*(alpha/N): this is the additive total over slots and equals alpha; it is not the unresolved per-readout mean.",
    )

    assert support["supported_external_physical_channels"] == 2
    assert maxwell["closed_checks"]["canonical_charge_is_source_over_sqrt_field_stiffness"]

    return UniquenessLedger(
        coupling_variable="alpha = e^2/(4*pi), the squared canonical Maxwell coupling",
        hidden_slot_count=closed.boundary_hidden_count,
        law="q_boundary = alpha / N_boundary",
        assumptions=assumptions,
        rejected_readings=rejected,
        predicted_alpha_inv=closed.predicted_alpha_inv,
        observed_alpha_inv=closed.observed_alpha_inv,
        miss_ppm=closed.miss_alpha_inv_ppm,
    )


def q_boundary_budget_check() -> dict[str, float | str]:
    budget = q_em_source_budget()
    closed = closed_alpha_candidate_with_sigma()
    q_pred = 1.0 / (closed.boundary_hidden_count * closed.predicted_alpha_inv)
    return {
        "q_boundary_from_budget_needed": budget.q_pdg_to_observed_readout,
        "q_boundary_from_alpha_over_N": q_pred,
        "difference": q_pred - budget.q_pdg_to_observed_readout,
        "relative_difference": (
            q_pred - budget.q_pdg_to_observed_readout
        )
        / budget.q_pdg_to_observed_readout,
        "reading": (
            "the small remaining discrepancy is exactly the closed-form "
            "alpha prediction residual, not a new adjustable coefficient"
        ),
    }


def open_tasks() -> list[str]:
    return [
        "derive the symmetric hidden-slot readout average from the boundary-to-Maxwell functional, not just from weak-coupling axioms",
        "derive the weak-readout expansion directly from the charged h=2 core action",
        "check whether the same alpha/N hidden-slot rule appears in any independent charged observable",
        "fold the p18bi law back into the article only after the action-level derivation is written clearly",
    ]


def run_gate() -> None:
    rows = readout_law_candidates()
    ledger = uniqueness_ledger()
    budget = q_boundary_budget_check()

    alpha_over_N = next(row for row in rows if row.label == "alpha_over_N")
    best = min(rows, key=lambda row: abs(row.miss_alpha_inv))

    assert best.label == "alpha_over_N"
    assert alpha_over_N.self_consistent
    assert alpha_over_N.weak_coupling_limit_ok
    assert alpha_over_N.hidden_slot_symmetry_ok
    assert abs(alpha_over_N.miss_ppm) < 1.0e-4
    assert all(row.self_consistent for row in rows)
    assert abs(
        next(row for row in rows if row.label == "sqrt_alpha_over_N").miss_ppm
    ) > 1.0
    assert abs(next(row for row in rows if row.label == "alpha").miss_ppm) > 1.0
    assert abs(next(row for row in rows if row.label == "alpha_over_N2").miss_ppm) > 0.02
    assert next(row for row in rows if row.label == "constant_over_N").weak_coupling_limit_ok is False

    print("p18bi alpha-over-N boundary readout law gate")
    print("candidate laws")
    for row in rows:
        print(f"- {row}")
    print()
    print("uniqueness ledger")
    print(ledger)
    print()
    print("q-boundary budget check")
    print(budget)
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_ACTION_LEVEL_DERIVATION_REQUIRED__PASS_ALPHA_OVER_N_READOUT_LAW")


if __name__ == "__main__":
    run_gate()
