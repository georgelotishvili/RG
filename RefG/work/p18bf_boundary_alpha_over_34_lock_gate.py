from __future__ import annotations

import math
from dataclasses import dataclass

from p18at_exact_c3_ratio_alpha_candidate_gate import (
    PDG_MASSES_MEV,
    alpha_inv_from_mass_ratios,
)
from p18bb_internal_external_em_readout_split_gate import (
    ALPHA_INV_OBSERVED_LOW,
    C3_ORDER,
    H_BRANCH,
    QED_B1_THREE_LEPTONS,
)
from p18be_q_em_source_budget_gate import q_em_source_budget


@dataclass(frozen=True)
class BoundaryLock:
    internal_threshold_alpha_inv: float
    observed_alpha_inv: float
    core_slot_count: int
    external_helicity_count: int
    boundary_hidden_count: int
    predicted_alpha_inv: float
    predicted_alpha: float
    miss_alpha_inv: float
    miss_alpha_inv_ppm: float
    q_boundary_predicted: float
    q_boundary_needed: float
    q_boundary_difference: float
    effective_real_N_needed: float
    self_consistency_residual: float


@dataclass(frozen=True)
class IntegerScanRow:
    N: int
    predicted_alpha_inv: float
    miss_alpha_inv: float
    miss_ppm: float


def internal_threshold_alpha_inv() -> float:
    tau_over_e = PDG_MASSES_MEV["tau"] / PDG_MASSES_MEV["electron"]
    muon_over_e = PDG_MASSES_MEV["muon"] / PDG_MASSES_MEV["electron"]
    return alpha_inv_from_mass_ratios(tau_over_e, muon_over_e)


def solve_alpha_inv_with_boundary_N(alpha_inv_internal: float, N_boundary: int) -> float:
    """Solve y = y_internal - (2/pi)/(N*y), with y=alpha^-1."""

    discriminant = alpha_inv_internal**2 - 4.0 * QED_B1_THREE_LEPTONS / N_boundary
    if discriminant <= 0.0:
        raise ValueError("boundary self-consistency has no positive large root")
    return (alpha_inv_internal + math.sqrt(discriminant)) / 2.0


def boundary_hidden_count() -> tuple[int, int, int]:
    core_slots = int((C3_ORDER * H_BRANCH) ** 2)
    external_helicity = int(H_BRANCH)
    return core_slots, external_helicity, core_slots - external_helicity


def boundary_alpha_over_34_lock() -> BoundaryLock:
    alpha_internal = internal_threshold_alpha_inv()
    core_slots, external_helicity, hidden_count = boundary_hidden_count()
    predicted = solve_alpha_inv_with_boundary_N(alpha_internal, hidden_count)
    alpha_pred = 1.0 / predicted
    q_pred = alpha_pred / hidden_count

    budget = q_em_source_budget()
    q_needed = budget.q_pdg_to_observed_readout

    miss = predicted - ALPHA_INV_OBSERVED_LOW
    effective_N = (1.0 / ALPHA_INV_OBSERVED_LOW) / q_needed
    residual = predicted - alpha_internal + QED_B1_THREE_LEPTONS / (
        hidden_count * predicted
    )

    return BoundaryLock(
        internal_threshold_alpha_inv=alpha_internal,
        observed_alpha_inv=ALPHA_INV_OBSERVED_LOW,
        core_slot_count=core_slots,
        external_helicity_count=external_helicity,
        boundary_hidden_count=hidden_count,
        predicted_alpha_inv=predicted,
        predicted_alpha=alpha_pred,
        miss_alpha_inv=miss,
        miss_alpha_inv_ppm=1.0e6 * miss / ALPHA_INV_OBSERVED_LOW,
        q_boundary_predicted=q_pred,
        q_boundary_needed=q_needed,
        q_boundary_difference=q_pred - q_needed,
        effective_real_N_needed=effective_N,
        self_consistency_residual=residual,
    )


def integer_N_scan(N_min: int = 2, N_max: int = 96) -> tuple[IntegerScanRow, ...]:
    alpha_internal = internal_threshold_alpha_inv()
    rows: list[IntegerScanRow] = []
    for N in range(N_min, N_max + 1):
        predicted = solve_alpha_inv_with_boundary_N(alpha_internal, N)
        miss = predicted - ALPHA_INV_OBSERVED_LOW
        rows.append(
            IntegerScanRow(
                N=N,
                predicted_alpha_inv=predicted,
                miss_alpha_inv=miss,
                miss_ppm=1.0e6 * miss / ALPHA_INV_OBSERVED_LOW,
            )
        )
    return tuple(rows)


def best_integer_rows(count: int = 7) -> tuple[IntegerScanRow, ...]:
    rows = integer_N_scan()
    return tuple(sorted(rows, key=lambda row: abs(row.miss_alpha_inv))[:count])


def interpretation() -> list[str]:
    return [
        "After the physical lepton-threshold step, the remaining boundary readout is almost exactly alpha/34.",
        "The integer 34 is not imported from alpha; it is the h=2 C3 core count (3h)^2=36 minus the two external helicity/readout channels.",
        "The equation is self-consistent: q_boundary is proportional to the final alpha, so alpha is solved as a quadratic rather than inserted.",
        "This converts the open q_boundary target into a concrete integer-lock hypothesis.",
        "It is still a hypothesis until the charged-core action derives why the hidden boundary count is (3h)^2-h and why each hidden slot carries alpha/N.",
    ]


def open_tasks() -> list[str]:
    return [
        "derive the boundary slot count N_boundary=(3h)^2-h from the h=2 charged core geometry",
        "derive why the external Maxwell readout deficit per hidden slot is alpha/N_boundary",
        "show that the two subtracted channels are exactly the two luminal helicity/readout modes",
        "combine this with the exact-C3 to physical-threshold bridge without using observed alpha",
        "audit whether the same N_boundary rule predicts anything else in the charged sector",
    ]


def run_gate() -> None:
    lock = boundary_alpha_over_34_lock()
    best = best_integer_rows()
    best_N = best[0].N
    neighbors = {
        row.N: row
        for row in integer_N_scan(
            lock.boundary_hidden_count - 2,
            lock.boundary_hidden_count + 2,
        )
    }

    assert lock.core_slot_count == 36
    assert lock.external_helicity_count == 2
    assert lock.boundary_hidden_count == 34
    assert best_N == lock.boundary_hidden_count
    assert abs(lock.self_consistency_residual) < 1.0e-14
    assert abs(lock.miss_alpha_inv_ppm) < 1.0e-4
    assert abs(lock.effective_real_N_needed - lock.boundary_hidden_count) < 1.0e-3
    assert abs(neighbors[33].miss_ppm) > 1000.0 * abs(lock.miss_alpha_inv_ppm)
    assert abs(neighbors[35].miss_ppm) > 1000.0 * abs(lock.miss_alpha_inv_ppm)

    print("p18bf boundary alpha-over-34 lock gate")
    print("lock")
    print(lock)
    print()
    print("best integer N rows")
    for row in best:
        print(f"- {row}")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_BOUNDARY_SLOT_DERIVATION_REQUIRED__PASS_ALPHA_OVER_34_LOCK")


if __name__ == "__main__":
    run_gate()
