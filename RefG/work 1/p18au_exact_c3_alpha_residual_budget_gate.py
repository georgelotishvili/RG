from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_INV_EXACT_C3_CANDIDATE = 137.03616654750616
QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)

CORE_SCALE_EXACT_C3_TEV = 222.45901084608514


@dataclass(frozen=True)
class ResidualBudget:
    alpha_inv_candidate: float
    alpha_inv_observed: float
    alpha_inv_residual_observed_minus_candidate: float
    alpha_inv_residual_ppm: float
    equivalent_log_core_shift: float
    equivalent_core_scale_ratio: float
    equivalent_core_scale_percent: float
    equivalent_core_scale_tev: float
    equal_readout_factor_ratio: float
    equal_readout_factor_percent: float
    alpha_relative_ppm: float


def residual_budget() -> ResidualBudget:
    residual = ALPHA_INV_OBSERVED_LOW - ALPHA_INV_EXACT_C3_CANDIDATE

    # In the lepton-threshold bridge, alpha_inv depends on the core scale as
    # d alpha_inv / d ln(mu_core) = 3*B while all three leptons are active.
    equivalent_log_core_shift = residual / (3.0 * QED_ONE_LOOP_B)
    core_ratio = math.exp(equivalent_log_core_shift)

    alpha_candidate = 1.0 / ALPHA_INV_EXACT_C3_CANDIDATE
    alpha_observed = 1.0 / ALPHA_INV_OBSERVED_LOW
    equal_factor_ratio = (alpha_observed / alpha_candidate) ** 0.25

    return ResidualBudget(
        alpha_inv_candidate=ALPHA_INV_EXACT_C3_CANDIDATE,
        alpha_inv_observed=ALPHA_INV_OBSERVED_LOW,
        alpha_inv_residual_observed_minus_candidate=residual,
        alpha_inv_residual_ppm=1.0e6 * residual / ALPHA_INV_EXACT_C3_CANDIDATE,
        equivalent_log_core_shift=equivalent_log_core_shift,
        equivalent_core_scale_ratio=core_ratio,
        equivalent_core_scale_percent=100.0 * (core_ratio - 1.0),
        equivalent_core_scale_tev=CORE_SCALE_EXACT_C3_TEV * core_ratio,
        equal_readout_factor_ratio=equal_factor_ratio,
        equal_readout_factor_percent=100.0 * (equal_factor_ratio - 1.0),
        alpha_relative_ppm=1.0e6 * (alpha_observed - alpha_candidate) / alpha_candidate,
    )


def interpretation() -> list[str]:
    return [
        "After the exact-C3 alpha candidate, the remaining inverse-alpha residual is about -1.22 ppm.",
        "Equivalently, the exact-C3 core scale would need a -0.0263 percent matching correction.",
        "In the equal readout-factor language, the remaining correction is only about +0.0000305 percent per factor.",
        "This residual is small enough to be plausibly assigned to the not-yet-completed matching layer, but it must still be derived.",
        "The next task is therefore not to search for a new 137 formula; it is to derive this tiny completion term.",
    ]


def completion_candidates() -> list[str]:
    return [
        "full QED threshold treatment beyond the lepton-only one-loop ledger",
        "electroweak U(1)/SU(2) matching if the core scale is above the EW regime",
        "RefG-specific boundary-to-Maxwell normalization correction",
        "small residual between exact C3 ratios and physical pole thresholds",
        "charged-core finite-size/profile matching correction",
    ]


def run_gate() -> None:
    r = residual_budget()

    assert abs(r.alpha_inv_residual_ppm) < 2.0
    assert -0.05 < r.equivalent_core_scale_percent < 0.0
    assert abs(r.equal_readout_factor_percent) < 0.0001
    assert 222.3 < r.equivalent_core_scale_tev < 222.5

    print("p18au exact-C3 alpha residual-budget gate")
    print(f"candidate alpha^-1 = {r.alpha_inv_candidate:.12f}")
    print(f"observed alpha^-1 = {r.alpha_inv_observed:.12f}")
    print(f"observed - candidate = {r.alpha_inv_residual_observed_minus_candidate:.12f}")
    print(f"residual ppm in alpha^-1 = {r.alpha_inv_residual_ppm:.6f}")
    print()
    print("equivalent core-scale correction")
    print(f"log core shift = {r.equivalent_log_core_shift:.12f}")
    print(f"core scale ratio = {r.equivalent_core_scale_ratio:.12f}")
    print(f"core scale percent = {r.equivalent_core_scale_percent:.9f}%")
    print(f"equivalent core scale = {r.equivalent_core_scale_tev:.9f} TeV")
    print()
    print("equal readout-factor correction")
    print(f"factor ratio = {r.equal_readout_factor_ratio:.12f}")
    print(f"factor percent = {r.equal_readout_factor_percent:.9f}%")
    print(f"alpha relative ppm = {r.alpha_relative_ppm:.6f}")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("completion candidates")
    for item in completion_candidates():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_TINY_MATCHING_COMPLETION_REQUIRED__PASS_EXACT_C3_RESIDUAL_BUDGET")


if __name__ == "__main__":
    run_gate()
