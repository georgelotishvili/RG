from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_INV_BARE_H2 = 81.0 * math.pi / 2.0
QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)

C3_ORDER = 3.0
H_BRANCH = 2.0

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}

LEPTON_MASS_SIGMA_MEV = {
    "electron": 0.00000000016,
    "muon": 0.0000023,
    "tau": 0.09,
}


@dataclass(frozen=True)
class AlphaPredictionCandidate:
    core_scale_mev: float
    core_scale_tev: float
    alpha_inv_predicted: float
    alpha_predicted: float
    alpha_inv_observed: float
    alpha_inv_miss: float
    alpha_inv_relative_miss_ppm: float
    alpha_relative_miss_ppm: float
    theory_input_sigma_alpha_inv: float
    miss_in_input_sigma: float
    bare_alpha_inv: float
    dressing_shift: float


def c3_h2_core_scale_from_lepton_hierarchy() -> float:
    me = LEPTON_MASSES_MEV["electron"]
    mtau = LEPTON_MASSES_MEV["tau"]
    return (C3_ORDER * H_BRANCH) ** 2 * mtau * mtau / me


def lepton_threshold_shift(mu_core_mev: float) -> float:
    me = LEPTON_MASSES_MEV["electron"]
    mmu = LEPTON_MASSES_MEV["muon"]
    mtau = LEPTON_MASSES_MEV["tau"]
    return QED_ONE_LOOP_B * (
        3.0 * math.log(mu_core_mev / mtau)
        + 2.0 * math.log(mtau / mmu)
        + math.log(mmu / me)
    )


def predicted_alpha_inv() -> float:
    return ALPHA_INV_BARE_H2 + lepton_threshold_shift(
        c3_h2_core_scale_from_lepton_hierarchy()
    )


def input_sigma_alpha_inv() -> float:
    # After substituting mu_core=36*tau^2/e, the log shift is:
    # B * [3 ln 36 + 5 ln tau - ln muon - 4 ln electron].
    me = LEPTON_MASSES_MEV["electron"]
    mmu = LEPTON_MASSES_MEV["muon"]
    mtau = LEPTON_MASSES_MEV["tau"]
    se = LEPTON_MASS_SIGMA_MEV["electron"]
    smu = LEPTON_MASS_SIGMA_MEV["muon"]
    stau = LEPTON_MASS_SIGMA_MEV["tau"]
    log_sigma = math.sqrt(
        (5.0 * stau / mtau) ** 2
        + (smu / mmu) ** 2
        + (4.0 * se / me) ** 2
    )
    return QED_ONE_LOOP_B * log_sigma


def evaluate_prediction_candidate() -> AlphaPredictionCandidate:
    mu_core = c3_h2_core_scale_from_lepton_hierarchy()
    shift = lepton_threshold_shift(mu_core)
    ainv = ALPHA_INV_BARE_H2 + shift
    alpha = 1.0 / ainv
    alpha_obs = 1.0 / ALPHA_INV_OBSERVED_LOW
    miss_inv = ainv - ALPHA_INV_OBSERVED_LOW
    sigma = input_sigma_alpha_inv()

    return AlphaPredictionCandidate(
        core_scale_mev=mu_core,
        core_scale_tev=mu_core / 1.0e6,
        alpha_inv_predicted=ainv,
        alpha_predicted=alpha,
        alpha_inv_observed=ALPHA_INV_OBSERVED_LOW,
        alpha_inv_miss=miss_inv,
        alpha_inv_relative_miss_ppm=1.0e6 * miss_inv / ALPHA_INV_OBSERVED_LOW,
        alpha_relative_miss_ppm=1.0e6 * (alpha - alpha_obs) / alpha_obs,
        theory_input_sigma_alpha_inv=sigma,
        miss_in_input_sigma=miss_inv / sigma,
        bare_alpha_inv=ALPHA_INV_BARE_H2,
        dressing_shift=shift,
    )


def derivation_chain() -> list[str]:
    return [
        "bare h=2 boundary value: alpha_bare^-1 = 81*pi/2",
        "C3/h=2 core frequency multiplier: 3*h = 6",
        "charged-lepton hierarchy extrapolation: mu_core = (3*h)^2*m_tau^2/m_e",
        "lepton-only threshold bridge: Delta alpha^-1 = (2/(3*pi))*[3 ln(mu_core/m_tau)+2 ln(m_tau/m_mu)+ln(m_mu/m_e)]",
        "candidate prediction: alpha_pred^-1 = alpha_bare^-1 + Delta alpha^-1",
    ]


def do_not_claim() -> list[str]:
    return [
        "Do not claim this is final alpha until the lepton thresholds and m~nu^2 law are derived inside RefG.",
        "Do not claim lepton-only running is the full electroweak/vacuum-polarization calculation.",
        "Do not hide the residual miss; it is about one ppm in alpha^-1 and about 2.5 tau-mass-input sigma with the adopted errors.",
        "Do not use the observed alpha to set mu_core in this prediction candidate.",
    ]


def run_gate() -> None:
    p = evaluate_prediction_candidate()

    assert 200.0 < p.core_scale_tev < 250.0
    assert abs(p.alpha_inv_miss) < 2.0e-4
    assert abs(p.alpha_inv_relative_miss_ppm) < 2.0
    assert 2.0 < abs(p.miss_in_input_sigma) < 3.0

    print("p18ar C3/h=2 alpha prediction-candidate gate")
    print("inputs used for prediction: alpha_bare=81*pi/2, C3=3, h=2, e/mu/tau masses")
    print(f"core scale mu_core = {p.core_scale_tev:.9f} TeV")
    print(f"dressing shift = {p.dressing_shift:.12f}")
    print(f"predicted alpha^-1 = {p.alpha_inv_predicted:.12f}")
    print(f"observed alpha^-1 = {p.alpha_inv_observed:.12f}")
    print(f"miss in alpha^-1 = {p.alpha_inv_miss:.12f}")
    print(f"relative miss in alpha^-1 = {p.alpha_inv_relative_miss_ppm:.6f} ppm")
    print(f"relative miss in alpha = {p.alpha_relative_miss_ppm:.6f} ppm")
    print(f"input sigma on alpha^-1 = {p.theory_input_sigma_alpha_inv:.12f}")
    print(f"miss/input sigma = {p.miss_in_input_sigma:.6f}")
    print()
    print("derivation chain")
    for item in derivation_chain():
        print(f"- {item}")
    print()
    print("do not claim")
    for item in do_not_claim():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_INTERNAL_THRESHOLD_AND_EW_COMPLETION__PASS_ALPHA_PREDICTION_CANDIDATE")


if __name__ == "__main__":
    run_gate()
