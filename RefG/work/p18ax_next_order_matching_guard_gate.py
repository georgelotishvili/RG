from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_INV_BARE_H2 = 81.0 * math.pi / 2.0

QED_B1_PER_UNIT_CHARGE = 2.0 / (3.0 * math.pi)

# Schematic mass-independent QED-like next beta coefficient per unit charged
# lepton. This is used only as a size/sign guard, not as a final threshold
# theorem.
QED_B2_PER_UNIT_CHARGE_SCHEMATIC = 1.0 / (4.0 * math.pi**2)

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}


@dataclass(frozen=True)
class IntervalCorrection:
    label: str
    active_charge_sum: float
    log_ratio: float
    one_loop_shift: float
    next_order_shift: float
    alpha_inv_before: float
    alpha_inv_after_one_loop: float


@dataclass(frozen=True)
class NextOrderGuard:
    one_loop_alpha_inv: float
    observed_alpha_inv: float
    one_loop_residual_observed_minus_candidate: float
    schematic_next_order_shift: float
    next_order_over_residual_abs: float
    alpha_inv_with_schematic_next_order: float
    miss_with_schematic_next_order: float
    effective_b2_scale_needed: float
    intervals: tuple[IntervalCorrection, ...]


def c3_h2_core_scale_from_pdg_ratios() -> float:
    return (
        (3.0 * 2.0) ** 2
        * LEPTON_MASSES_MEV["tau"] ** 2
        / LEPTON_MASSES_MEV["electron"]
    )


def one_loop_intervals(mu_core_mev: float | None = None) -> list[tuple[str, float, float, float]]:
    mu_core_mev = c3_h2_core_scale_from_pdg_ratios() if mu_core_mev is None else mu_core_mev
    return [
        ("core_to_tau", mu_core_mev, LEPTON_MASSES_MEV["tau"], 3.0),
        ("tau_to_muon", LEPTON_MASSES_MEV["tau"], LEPTON_MASSES_MEV["muon"], 2.0),
        ("muon_to_electron", LEPTON_MASSES_MEV["muon"], LEPTON_MASSES_MEV["electron"], 1.0),
    ]


def next_order_guard() -> NextOrderGuard:
    y = ALPHA_INV_BARE_H2
    intervals: list[IntervalCorrection] = []
    next_order_total = 0.0

    for label, high, low, charge_sum in one_loop_intervals():
        log_ratio = math.log(high / low)
        b1 = QED_B1_PER_UNIT_CHARGE * charge_sum
        b2 = QED_B2_PER_UNIT_CHARGE_SCHEMATIC * charge_sum

        one_loop_shift = b1 * log_ratio

        # With y=alpha^-1, a schematic next order beta term gives
        # d y / dL = b1 + b2/y while running downward across L.
        # Evaluate it on the one-loop y(L)=y0+b1*L trajectory.
        next_order_shift = (b2 / b1) * math.log((y + one_loop_shift) / y)

        intervals.append(
            IntervalCorrection(
                label=label,
                active_charge_sum=charge_sum,
                log_ratio=log_ratio,
                one_loop_shift=one_loop_shift,
                next_order_shift=next_order_shift,
                alpha_inv_before=y,
                alpha_inv_after_one_loop=y + one_loop_shift,
            )
        )

        y += one_loop_shift
        next_order_total += next_order_shift

    one_loop_alpha_inv = y
    residual = ALPHA_INV_OBSERVED_LOW - one_loop_alpha_inv
    alpha_inv_with_next = one_loop_alpha_inv + next_order_total

    effective_b2_scale_needed = (
        residual / next_order_total if next_order_total != 0.0 else float("nan")
    )

    return NextOrderGuard(
        one_loop_alpha_inv=one_loop_alpha_inv,
        observed_alpha_inv=ALPHA_INV_OBSERVED_LOW,
        one_loop_residual_observed_minus_candidate=residual,
        schematic_next_order_shift=next_order_total,
        next_order_over_residual_abs=abs(next_order_total / residual),
        alpha_inv_with_schematic_next_order=alpha_inv_with_next,
        miss_with_schematic_next_order=alpha_inv_with_next
        - ALPHA_INV_OBSERVED_LOW,
        effective_b2_scale_needed=effective_b2_scale_needed,
        intervals=tuple(intervals),
    )


def interpretation() -> list[str]:
    return [
        "The leading one-loop/C3/h=2 candidate is already within about one ppm.",
        "A naive positive next-order beta contribution is much larger than the residual and moves in the wrong direction.",
        "Therefore the last ppm should not be treated as simply adding a bare two-loop term.",
        "The completion must be a full matching calculation: scheme constants, finite thresholds, EW/U1 matching and RefG boundary normalization may cancel or reshape the naive term.",
        "This gate protects the alpha chain from overclaiming a residual closure before the real matching theorem exists.",
    ]


def open_tasks() -> list[str]:
    return [
        "derive the correct RefG-to-Maxwell matching scheme",
        "derive the threshold convention for pole masses versus running masses",
        "compute the full QED/EW bridge rather than adding a schematic next-order term",
        "derive whether RefG boundary normalization supplies a finite counterterm at the matching scale",
    ]


def run_gate() -> None:
    guard = next_order_guard()

    assert guard.one_loop_alpha_inv > ALPHA_INV_OBSERVED_LOW
    assert guard.schematic_next_order_shift > 0.0
    assert guard.next_order_over_residual_abs > 50.0
    assert guard.effective_b2_scale_needed < 0.0

    print("p18ax next-order matching guard gate")
    print(f"one-loop candidate alpha^-1 = {guard.one_loop_alpha_inv:.12f}")
    print(f"observed alpha^-1 = {guard.observed_alpha_inv:.12f}")
    print(
        "observed - one-loop candidate = "
        f"{guard.one_loop_residual_observed_minus_candidate:.12f}"
    )
    print()
    print("schematic next-order audit")
    print(f"schematic next-order shift = {guard.schematic_next_order_shift:.12f}")
    print(
        "next-order / residual magnitude = "
        f"{guard.next_order_over_residual_abs:.6f}"
    )
    print(
        "alpha^-1 with schematic next order = "
        f"{guard.alpha_inv_with_schematic_next_order:.12f}"
    )
    print(
        "miss with schematic next order = "
        f"{guard.miss_with_schematic_next_order:.12f}"
    )
    print(
        "effective b2 scale needed to close residual = "
        f"{guard.effective_b2_scale_needed:.12f}"
    )
    print()
    print("intervals")
    for item in guard.intervals:
        print(f"- {item}")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_FULL_MATCHING_THEOREM_REQUIRED__PASS_NEXT_ORDER_OVERCLAIM_GUARD")


if __name__ == "__main__":
    run_gate()
