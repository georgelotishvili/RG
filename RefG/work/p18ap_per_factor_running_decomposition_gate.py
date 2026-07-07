from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_INV_BARE_H2 = 81.0 * math.pi / 2.0

QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}


@dataclass(frozen=True)
class RunningInterval:
    label: str
    high_mev: float
    low_mev: float
    active_charge_sum: float
    log_ratio: float
    delta_alpha_inv: float
    alpha_inv_before: float
    alpha_inv_after: float
    per_factor_ratio: float
    per_factor_attenuation_percent: float


@dataclass(frozen=True)
class DecompositionResult:
    target_mu_mev: float
    target_mu_tev: float
    alpha_inv_bare: float
    alpha_inv_low: float
    total_delta_alpha_inv: float
    total_per_factor_ratio: float
    total_per_factor_attenuation_percent: float
    intervals: tuple[RunningInterval, ...]


def required_mu_from_low_alpha() -> float:
    delta = ALPHA_INV_OBSERVED_LOW - ALPHA_INV_BARE_H2
    required_sum_log = delta / QED_ONE_LOOP_B
    mass_log_mean = sum(math.log(m) for m in LEPTON_MASSES_MEV.values()) / 3.0
    return math.exp(mass_log_mean + required_sum_log / 3.0)


def _interval_step(
    label: str,
    high_mev: float,
    low_mev: float,
    active_charge_sum: float,
    alpha_inv_before: float,
) -> RunningInterval:
    log_ratio = math.log(high_mev / low_mev)
    delta = QED_ONE_LOOP_B * active_charge_sum * log_ratio
    alpha_inv_after = alpha_inv_before + delta

    # Since alpha=f^4 and alpha=1/alpha_inv, the equal readout factor runs as
    # f_after/f_before = (alpha_inv_before/alpha_inv_after)^(1/4).
    per_factor_ratio = (alpha_inv_before / alpha_inv_after) ** 0.25

    return RunningInterval(
        label=label,
        high_mev=high_mev,
        low_mev=low_mev,
        active_charge_sum=active_charge_sum,
        log_ratio=log_ratio,
        delta_alpha_inv=delta,
        alpha_inv_before=alpha_inv_before,
        alpha_inv_after=alpha_inv_after,
        per_factor_ratio=per_factor_ratio,
        per_factor_attenuation_percent=(1.0 - per_factor_ratio) * 100.0,
    )


def decompose_running(mu_high_mev: float | None = None) -> DecompositionResult:
    mu_high_mev = required_mu_from_low_alpha() if mu_high_mev is None else mu_high_mev

    alpha_inv = ALPHA_INV_BARE_H2
    intervals: list[RunningInterval] = []

    # Running from the high matching scale downward:
    # above tau: electron, muon and tau are active;
    # between tau and muon: electron and muon are active;
    # between muon and electron: only electron is active.
    threshold_plan = [
        ("mu_core_to_tau", mu_high_mev, LEPTON_MASSES_MEV["tau"], 3.0),
        ("tau_to_muon", LEPTON_MASSES_MEV["tau"], LEPTON_MASSES_MEV["muon"], 2.0),
        ("muon_to_electron", LEPTON_MASSES_MEV["muon"], LEPTON_MASSES_MEV["electron"], 1.0),
    ]

    for label, high, low, active_sum in threshold_plan:
        step = _interval_step(label, high, low, active_sum, alpha_inv)
        intervals.append(step)
        alpha_inv = step.alpha_inv_after

    total_ratio = 1.0
    for step in intervals:
        total_ratio *= step.per_factor_ratio

    return DecompositionResult(
        target_mu_mev=mu_high_mev,
        target_mu_tev=mu_high_mev / 1.0e6,
        alpha_inv_bare=ALPHA_INV_BARE_H2,
        alpha_inv_low=alpha_inv,
        total_delta_alpha_inv=alpha_inv - ALPHA_INV_BARE_H2,
        total_per_factor_ratio=total_ratio,
        total_per_factor_attenuation_percent=(1.0 - total_ratio) * 100.0,
        intervals=tuple(intervals),
    )


def predict_alpha_inv_from_core_scale(mu_core_tev: float) -> float:
    return decompose_running(mu_core_tev * 1.0e6).alpha_inv_low


def benchmark_predictions() -> dict[str, dict[str, float]]:
    rows: dict[str, dict[str, float]] = {}
    for mu_tev in (10.0, 100.0, 222.397510635, 1000.0):
        result = decompose_running(mu_tev * 1.0e6)
        rows[f"{mu_tev:g}_TeV"] = {
            "alpha_inv": result.alpha_inv_low,
            "miss_vs_observed_alpha_inv": result.alpha_inv_low - ALPHA_INV_OBSERVED_LOW,
            "per_factor_ratio": result.total_per_factor_ratio,
            "per_factor_attenuation_percent": result.total_per_factor_attenuation_percent,
        }
    return rows


def interpretation() -> list[str]:
    return [
        "If alpha=f^4, inverse-alpha running becomes a multiplicative running of f with one-quarter logarithmic weight.",
        "The 1.838190% per-factor dressing is not a new free parameter once the matching scale and active thresholds are known.",
        "The target 222 TeV scale is still not derived here; this gate only gives the exact dressing calculator for any future RefG core scale.",
        "A future core-scale prediction can be inserted into predict_alpha_inv_from_core_scale(mu_core_tev) without using the observed alpha as input.",
    ]


def run_gate() -> None:
    result = decompose_running()
    observed_ratio = (ALPHA_INV_BARE_H2 / ALPHA_INV_OBSERVED_LOW) ** 0.25

    assert math.isclose(result.alpha_inv_low, ALPHA_INV_OBSERVED_LOW, rel_tol=1e-12)
    assert math.isclose(result.total_per_factor_ratio, observed_ratio, rel_tol=1e-12)
    assert math.isclose(
        sum(step.delta_alpha_inv for step in result.intervals),
        result.total_delta_alpha_inv,
        rel_tol=1e-14,
    )
    assert 200.0 < result.target_mu_tev < 250.0
    assert 0.98 < result.total_per_factor_ratio < 0.99

    print("p18ap per-factor running decomposition gate")
    print(f"bare alpha^-1 = {result.alpha_inv_bare:.9f}")
    print(f"low alpha^-1 reconstructed = {result.alpha_inv_low:.9f}")
    print(f"target mu = {result.target_mu_tev:.6f} TeV")
    print(f"total delta alpha^-1 = {result.total_delta_alpha_inv:.9f}")
    print(f"total per-factor ratio = {result.total_per_factor_ratio:.12f}")
    print(f"total per-factor attenuation = {result.total_per_factor_attenuation_percent:.6f}%")
    print()
    print("threshold decomposition")
    for step in result.intervals:
        print(
            f"- {step.label}: S={step.active_charge_sum:.0f}, "
            f"log={step.log_ratio:.9f}, delta_inv={step.delta_alpha_inv:.9f}, "
            f"f_ratio={step.per_factor_ratio:.12f}, "
            f"attenuation={step.per_factor_attenuation_percent:.6f}%"
        )
    print()
    print("benchmark predictions")
    for label, row in benchmark_predictions().items():
        print(f"- {label}: {row}")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_REFG_CORE_SCALE_INPUT_REQUIRED__PASS_PER_FACTOR_RUNNING_DECOMPOSITION")


if __name__ == "__main__":
    run_gate()
