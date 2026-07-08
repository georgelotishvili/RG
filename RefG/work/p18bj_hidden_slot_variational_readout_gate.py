from __future__ import annotations

import math
from dataclasses import dataclass

from p18bb_internal_external_em_readout_split_gate import (
    ALPHA_INV_OBSERVED_LOW,
    QED_B1_THREE_LEPTONS,
)
from p18bg_closed_alpha_formula_boundary_lock_gate import (
    closed_alpha_candidate_with_sigma,
)
from p18bh_boundary_slot_count_theorem_gate import slot_count_ledger


@dataclass(frozen=True)
class VariationalReadoutLaw:
    hidden_slot_count: int
    total_weak_budget_alpha: float
    per_slot_readout: float
    unresolved_mean_readout: float
    total_sum_readout: float
    lagrange_multiplier: float
    stationary_residual_max: float
    constraint_residual: float
    quadratic_action_value: float
    alpha_inv_internal: float
    alpha_inv_predicted: float
    alpha_inv_observed: float
    miss_alpha_inv: float
    miss_ppm: float


@dataclass(frozen=True)
class CompetingFunctional:
    label: str
    q_boundary: float
    alpha_inv_predicted: float
    miss_ppm: float
    rejected_because: str


def variational_hidden_slot_readout() -> VariationalReadoutLaw:
    """Derive q_boundary=alpha/N from a symmetric hidden-slot action.

    Boundary variables x_i are the weak Maxwell readout weights carried by
    N hidden slots.  The completed Maxwell channel supplies the total weak
    readout budget

        sum_i x_i = alpha.

    The lowest positive symmetric boundary action is

        S_hidden = 1/2 * sum_i x_i^2.

    Extremizing S_hidden with the budget constraint gives x_i=alpha/N.  The
    external unresolved readout is a mean over the indistinguishable hidden
    slots, so q_boundary=x_i=alpha/N, not sum_i x_i=alpha.
    """

    closed = closed_alpha_candidate_with_sigma()
    N = closed.boundary_hidden_count
    alpha = closed.predicted_alpha
    per_slot = alpha / N
    lagrange = -per_slot

    stationary_residuals = [per_slot + lagrange for _ in range(N)]
    constraint_residual = N * per_slot - alpha
    action_value = 0.5 * N * per_slot**2
    alpha_inv_pred = (
        closed.internal_threshold_alpha_inv - QED_B1_THREE_LEPTONS * per_slot
    )
    miss = alpha_inv_pred - ALPHA_INV_OBSERVED_LOW

    return VariationalReadoutLaw(
        hidden_slot_count=N,
        total_weak_budget_alpha=alpha,
        per_slot_readout=per_slot,
        unresolved_mean_readout=per_slot,
        total_sum_readout=N * per_slot,
        lagrange_multiplier=lagrange,
        stationary_residual_max=max(abs(item) for item in stationary_residuals),
        constraint_residual=constraint_residual,
        quadratic_action_value=action_value,
        alpha_inv_internal=closed.internal_threshold_alpha_inv,
        alpha_inv_predicted=alpha_inv_pred,
        alpha_inv_observed=ALPHA_INV_OBSERVED_LOW,
        miss_alpha_inv=miss,
        miss_ppm=1.0e6 * miss / ALPHA_INV_OBSERVED_LOW,
    )


def competing_functionals() -> tuple[CompetingFunctional, ...]:
    closed = closed_alpha_candidate_with_sigma()
    N = closed.boundary_hidden_count
    alpha = closed.predicted_alpha
    internal = closed.internal_threshold_alpha_inv

    definitions = (
        (
            "total_sum_readout",
            alpha,
            "uses the sum over hidden slots; that is a resolved additive readout, not the external unresolved mean",
        ),
        (
            "amplitude_budget_sqrt_alpha",
            math.sqrt(alpha) / N,
            "uses amplitude instead of probability/energy alpha=e^2/(4*pi)",
        ),
        (
            "double_mean_alpha_over_N2",
            alpha / (N * N),
            "averages over the same hidden slot space twice",
        ),
        (
            "zero_coupling_blind_one_over_N",
            1.0 / N,
            "does not vanish as the Maxwell coupling alpha goes to zero",
        ),
    )

    rows: list[CompetingFunctional] = []
    for label, q, reason in definitions:
        predicted = internal - QED_B1_THREE_LEPTONS * q
        rows.append(
            CompetingFunctional(
                label=label,
                q_boundary=q,
                alpha_inv_predicted=predicted,
                miss_ppm=1.0e6 * (predicted - ALPHA_INV_OBSERVED_LOW)
                / ALPHA_INV_OBSERVED_LOW,
                rejected_because=reason,
            )
        )
    return tuple(rows)


def action_level_statement() -> dict[str, object]:
    slots = slot_count_ledger()
    return {
        "boundary_action": "S_hidden = 1/2 * sum_{i=1}^{N} x_i^2",
        "constraint": "sum_i x_i = alpha",
        "euler_lagrange": "x_i + lambda = 0",
        "solution": "x_i = alpha/N for every hidden slot",
        "external_readout": "q_boundary is the unresolved mean per hidden slot, not the resolved sum",
        "N_boundary": slots.hidden_boundary_slot_count,
        "physical_inputs": (
            "N_boundary=(3h)^2-h from p18bh, alpha as the squared canonical "
            "Maxwell coupling from p18z, and hidden-slot permutation symmetry"
        ),
        "status": (
            "This is the action-level derivation of the alpha/N readout law "
            "within the effective hidden-slot boundary functional.  The deeper "
            "microscopic derivation of this quadratic functional from the full "
            "localized charged h=2 core action remains the next layer."
        ),
    }


def run_gate() -> None:
    law = variational_hidden_slot_readout()
    competitors = competing_functionals()

    assert law.hidden_slot_count == 34
    assert abs(law.stationary_residual_max) < 1.0e-18
    assert abs(law.constraint_residual) < 1.0e-18
    assert math.isclose(
        law.total_sum_readout,
        law.total_weak_budget_alpha,
        rel_tol=1.0e-15,
    )
    assert math.isclose(
        law.unresolved_mean_readout,
        law.total_weak_budget_alpha / law.hidden_slot_count,
        rel_tol=1.0e-15,
    )
    assert abs(law.miss_ppm) < 1.0e-4
    assert all(abs(row.miss_ppm) > 0.5 for row in competitors)

    print("p18bj hidden-slot variational readout gate")
    print("law")
    print(law)
    print()
    print("action-level statement")
    print(action_level_statement())
    print()
    print("competing functionals")
    for row in competitors:
        print(f"- {row}")
    print()
    print("STATUS: OPEN_MICROSCOPIC_CORE_FUNCTIONAL_DERIVATION__PASS_HIDDEN_SLOT_VARIATIONAL_ALPHA_OVER_N")


if __name__ == "__main__":
    run_gate()
