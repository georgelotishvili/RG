from __future__ import annotations

import math
from dataclasses import dataclass

from p18bb_internal_external_em_readout_split_gate import (
    ALPHA_INV_OBSERVED_LOW,
    C3_ORDER,
    H_BRANCH,
)
from p18bf_boundary_alpha_over_34_lock_gate import (
    solve_alpha_inv_with_boundary_N,
)
from p18bg_closed_alpha_formula_boundary_lock_gate import (
    internal_threshold_alpha_inv_from_masses,
)
from p18f_oriented_axis_completion_gate import (
    derive_oriented_axis_completion_gate,
)
from p18h_frame_connection_u1_gate import (
    derive_frame_connection_u1_gate,
)


LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}


@dataclass(frozen=True)
class SlotCountLedger:
    h_branch: int
    c3_order: int
    core_step_count: int
    internal_core_slot_count: int
    external_helicity_count: int
    hidden_boundary_slot_count: int
    slot_formula: str


@dataclass(frozen=True)
class SubtractionAudit:
    subtracted_external_channels: int
    boundary_N: int
    predicted_alpha_inv: float
    miss_alpha_inv: float
    miss_ppm: float
    physical_status: str


@dataclass(frozen=True)
class BranchAudit:
    h_branch: int
    boundary_N: int
    internal_alpha_inv: float
    predicted_alpha_inv: float
    miss_alpha_inv: float
    miss_ppm: float


def slot_count_ledger(h: int = int(H_BRANCH)) -> SlotCountLedger:
    c3 = int(C3_ORDER)
    core_step = c3 * h
    internal_slots = core_step**2
    external_helicity = h
    hidden = internal_slots - external_helicity
    return SlotCountLedger(
        h_branch=h,
        c3_order=c3,
        core_step_count=core_step,
        internal_core_slot_count=internal_slots,
        external_helicity_count=external_helicity,
        hidden_boundary_slot_count=hidden,
        slot_formula="N_boundary=(3h)^2-h",
    )


def _alpha_internal_for_h(h: int) -> float:
    return internal_threshold_alpha_inv_from_masses(
        LEPTON_MASSES_MEV["electron"],
        LEPTON_MASSES_MEV["muon"],
        LEPTON_MASSES_MEV["tau"],
        h=float(h),
    )


def subtraction_audit(max_subtraction: int = 6) -> tuple[SubtractionAudit, ...]:
    ledger = slot_count_ledger()
    alpha_internal = _alpha_internal_for_h(ledger.h_branch)
    rows: list[SubtractionAudit] = []
    for subtracted in range(max_subtraction + 1):
        boundary_N = ledger.internal_core_slot_count - subtracted
        predicted = solve_alpha_inv_with_boundary_N(alpha_internal, boundary_N)
        miss = predicted - ALPHA_INV_OBSERVED_LOW
        if subtracted == 0:
            status = "NO_EXTERNAL_MODE_REMOVAL"
        elif subtracted == 1:
            status = "ONE_MODE_REMOVAL_NOT_PHOTON"
        elif subtracted == 2:
            status = "PHYSICAL_HELICITY_PAIR_REMOVAL"
        elif subtracted == 3:
            status = "REMOVES_GAUGE_COORDINATE_TOO_MUCH"
        else:
            status = "NO_SUPPORTED_MODE_COUNT"
        rows.append(
            SubtractionAudit(
                subtracted_external_channels=subtracted,
                boundary_N=boundary_N,
                predicted_alpha_inv=predicted,
                miss_alpha_inv=miss,
                miss_ppm=1.0e6 * miss / ALPHA_INV_OBSERVED_LOW,
                physical_status=status,
            )
        )
    return tuple(rows)


def h_branch_audit(h_min: int = 1, h_max: int = 6) -> tuple[BranchAudit, ...]:
    rows: list[BranchAudit] = []
    for h in range(h_min, h_max + 1):
        ledger = slot_count_ledger(h)
        internal = _alpha_internal_for_h(h)
        predicted = solve_alpha_inv_with_boundary_N(
            internal,
            ledger.hidden_boundary_slot_count,
        )
        miss = predicted - ALPHA_INV_OBSERVED_LOW
        rows.append(
            BranchAudit(
                h_branch=h,
                boundary_N=ledger.hidden_boundary_slot_count,
                internal_alpha_inv=internal,
                predicted_alpha_inv=predicted,
                miss_alpha_inv=miss,
                miss_ppm=1.0e6 * miss / ALPHA_INV_OBSERVED_LOW,
            )
        )
    return tuple(rows)


def existing_gate_support() -> dict[str, object]:
    axis = derive_oriented_axis_completion_gate()
    frame = derive_frame_connection_u1_gate()
    axis_closed = axis["closed_checks"]
    frame_closed = frame["closed_checks"]

    return {
        "p18f_status": axis["STATUS"],
        "p18h_status": frame["STATUS"],
        "p18f_two_luminal_modes": axis_closed["two_identical_luminal_modes"],
        "p18f_helicity_pair": axis_closed["helicity_pair_identified"],
        "p18h_u1_redundancy": frame_closed["Dtheta_is_U1_gauge_invariant"],
        "p18h_no_third_quadratic_mode": frame_closed[
            "gauge_fixed_fiber_has_no_quadratic_mode"
        ],
        "p18h_axis_pair_double_luminal": frame_closed[
            "axis_pair_remains_double_luminal"
        ],
        "supported_external_physical_channels": 2,
        "reading": (
            "p18f supplies the two helicity modes; p18h promotes theta to a "
            "local frame-section coordinate and leaves only the two helicity "
            "modes as physical quadratic EM readout channels"
        ),
    }


def theorem_statement() -> dict[str, object]:
    ledger = slot_count_ledger()
    return {
        "claim": (
            "For the h=2 charged orientation-frame core, the boundary count "
            "used by the alpha/34 lock is N_boundary=(3h)^2-h."
        ),
        "internal_count": (
            "(3h)^2 counts the squared C3-by-h finite core step structure "
            "already present in the h=2 threshold bridge."
        ),
        "external_subtraction": (
            "h=2 supplies exactly two physical external helicity/readout "
            "channels after the U(1) redundancy removes theta as a third mode."
        ),
        "result": ledger,
        "status": (
            "This is now a supported slot-count theorem inside the current "
            "work-file ledger; the deeper action derivation of why every "
            "hidden slot carries alpha/N remains open."
        ),
    }


def open_tasks() -> list[str]:
    return [
        "derive the squared core slot count (3h)^2 from the localized charged-core action, not only from the threshold bridge",
        "derive the h external-channel subtraction as the general rule, with h=2 giving the photon helicity pair",
        "derive q_boundary=alpha/N_boundary from the boundary-to-Maxwell readout functional",
        "check whether any independent charged observable uses the same N_boundary=34",
    ]


def run_gate() -> None:
    support = existing_gate_support()
    ledger = slot_count_ledger()
    subtractions = subtraction_audit()
    branches = h_branch_audit()

    physical_row = next(
        row
        for row in subtractions
        if row.subtracted_external_channels == ledger.external_helicity_count
    )
    best_subtraction = min(subtractions, key=lambda row: abs(row.miss_alpha_inv))
    best_branch = min(branches, key=lambda row: abs(row.miss_alpha_inv))

    assert support["p18f_two_luminal_modes"]
    assert support["p18f_helicity_pair"]
    assert support["p18h_u1_redundancy"]
    assert support["p18h_no_third_quadratic_mode"]
    assert support["p18h_axis_pair_double_luminal"]
    assert ledger.internal_core_slot_count == 36
    assert ledger.external_helicity_count == 2
    assert ledger.hidden_boundary_slot_count == 34
    assert best_subtraction.subtracted_external_channels == 2
    assert best_branch.h_branch == 2
    assert abs(physical_row.miss_ppm) < 1.0e-4
    assert abs(
        subtractions[1].miss_ppm
    ) > 1000.0 * abs(physical_row.miss_ppm)
    assert abs(
        subtractions[3].miss_ppm
    ) > 1000.0 * abs(physical_row.miss_ppm)

    print("p18bh boundary slot-count theorem gate")
    print("support")
    print(support)
    print()
    print("theorem")
    print(theorem_statement())
    print()
    print("subtraction audit")
    for row in subtractions:
        print(f"- {row}")
    print()
    print("h-branch audit")
    for row in branches:
        print(f"- {row}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_ALPHA_OVER_N_READOUT_LAW_REQUIRED__PASS_BOUNDARY_SLOT_COUNT_THEOREM")


if __name__ == "__main__":
    run_gate()
