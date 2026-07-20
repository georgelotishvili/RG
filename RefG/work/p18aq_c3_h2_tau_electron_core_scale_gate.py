from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_INV_BARE_H2 = 81.0 * math.pi / 2.0
QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)

H_BRANCH = 2.0
C3_ORDER = 3.0

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}

# Minimal PDG-style uncertainties used only to size the coincidence. They are
# not used as fitted parameters.
LEPTON_MASS_SIGMA_MEV = {
    "electron": 0.00000000016,
    "muon": 0.0000023,
    "tau": 0.09,
}


@dataclass(frozen=True)
class CoreScaleCandidate:
    target_mu_mev: float
    target_mu_tev: float
    candidate_mu_mev: float
    candidate_mu_tev: float
    candidate_over_target: float
    candidate_miss_percent: float
    candidate_sigma_percent: float
    candidate_miss_in_sigma: float
    predicted_alpha_inv: float
    predicted_alpha_inv_miss: float
    predicted_alpha_inv_sigma: float
    predicted_alpha_inv_miss_in_sigma: float
    frequency_multiplier: float


def target_mu_from_observed_alpha() -> float:
    delta = ALPHA_INV_OBSERVED_LOW - ALPHA_INV_BARE_H2
    required_sum_log = delta / QED_ONE_LOOP_B
    mass_log_mean = sum(math.log(m) for m in LEPTON_MASSES_MEV.values()) / 3.0
    return math.exp(mass_log_mean + required_sum_log / 3.0)


def c3_h2_tau_electron_core_scale() -> float:
    """C3/h=2 core-frequency extrapolation.

    If the charged lepton mass readout follows m ~ nu^2, then m_tau^2/m_e is
    the mass-scale obtained by extending the tau/electron frequency hierarchy
    one more step. The C3/h=2 finite-frame multiplier is 3*h=6 in frequency,
    hence (3*h)^2=36 in mass:

        mu_core = (3*h)^2 * m_tau^2 / m_e.
    """

    me = LEPTON_MASSES_MEV["electron"]
    mtau = LEPTON_MASSES_MEV["tau"]
    return (C3_ORDER * H_BRANCH) ** 2 * mtau * mtau / me


def alpha_inv_from_core_scale(mu_core_mev: float) -> float:
    me = LEPTON_MASSES_MEV["electron"]
    mmu = LEPTON_MASSES_MEV["muon"]
    mtau = LEPTON_MASSES_MEV["tau"]
    if not (mu_core_mev > mtau > mmu > me):
        raise ValueError("this threshold ledger assumes mu_core > tau > muon > electron")

    shift = QED_ONE_LOOP_B * (
        3.0 * math.log(mu_core_mev / mtau)
        + 2.0 * math.log(mtau / mmu)
        + math.log(mmu / me)
    )
    return ALPHA_INV_BARE_H2 + shift


def _candidate_relative_sigma() -> float:
    # mu = 36*m_tau^2/m_e, so dmu/mu = 2 dmtau/mtau - dme/me.
    me = LEPTON_MASSES_MEV["electron"]
    mtau = LEPTON_MASSES_MEV["tau"]
    se = LEPTON_MASS_SIGMA_MEV["electron"]
    stau = LEPTON_MASS_SIGMA_MEV["tau"]
    return math.sqrt((2.0 * stau / mtau) ** 2 + (se / me) ** 2)


def _alpha_inv_sigma_from_candidate() -> float:
    # alpha_inv contains 3*ln(mu_core/tau). Since mu_core ~ tau^2/e,
    # the tau and electron uncertainties enter the substituted expression as
    # 3*ln(36) + 5*ln(tau) - ln(muon) - 4*ln(electron).
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


def evaluate_candidate() -> CoreScaleCandidate:
    target = target_mu_from_observed_alpha()
    candidate = c3_h2_tau_electron_core_scale()
    ratio = candidate / target

    rel_sigma = _candidate_relative_sigma()
    miss_rel = ratio - 1.0

    alpha_inv_pred = alpha_inv_from_core_scale(candidate)
    alpha_miss = alpha_inv_pred - ALPHA_INV_OBSERVED_LOW
    alpha_sigma = _alpha_inv_sigma_from_candidate()

    return CoreScaleCandidate(
        target_mu_mev=target,
        target_mu_tev=target / 1.0e6,
        candidate_mu_mev=candidate,
        candidate_mu_tev=candidate / 1.0e6,
        candidate_over_target=ratio,
        candidate_miss_percent=100.0 * miss_rel,
        candidate_sigma_percent=100.0 * rel_sigma,
        candidate_miss_in_sigma=miss_rel / rel_sigma,
        predicted_alpha_inv=alpha_inv_pred,
        predicted_alpha_inv_miss=alpha_miss,
        predicted_alpha_inv_sigma=alpha_sigma,
        predicted_alpha_inv_miss_in_sigma=alpha_miss / alpha_sigma,
        frequency_multiplier=C3_ORDER * H_BRANCH,
    )


def interpretation() -> list[str]:
    return [
        "The 222 TeV target is numerically locked to 36*m_tau^2/m_e at the 0.022 percent level.",
        "Because m ~ nu^2 in the RefG lepton map, the same relation is a frequency extrapolation by 3*h=6.",
        "This uses the C3 count and the h=2 branch already present in the alpha chain.",
        "The result is not an alpha derivation until RefG derives the charged-lepton masses/thresholds and the m~nu^2 energy rule.",
        "It gives a concrete next theorem: derive mu_core=(3h)^2*m_tau^2/m_e from the charged h=2 oscillon boundary spectrum.",
    ]


def open_tasks() -> list[str]:
    return [
        "derive m~nu^2 for charged oscillons from the energy functional",
        "derive the C3 lepton thresholds rather than inserting PDG masses",
        "derive why the core scale is the tau/electron second extrapolation",
        "derive why the C3/h=2 multiplier acts on frequency as 3*h",
        "then feed the derived mu_core into the p18ap dressing calculator",
    ]


def run_gate() -> None:
    c = evaluate_candidate()

    assert 200.0 < c.target_mu_tev < 250.0
    assert 200.0 < c.candidate_mu_tev < 250.0
    assert abs(c.candidate_miss_percent) < 0.05
    assert abs(c.predicted_alpha_inv_miss) < 2.0e-4
    assert 1.0 < abs(c.candidate_miss_in_sigma) < 3.0

    print("p18aq C3/h=2 tau-electron core-scale gate")
    print(f"target mu from observed-alpha dressing = {c.target_mu_tev:.9f} TeV")
    print(f"candidate mu = (3*h)^2*m_tau^2/m_e = {c.candidate_mu_tev:.9f} TeV")
    print(f"candidate/target = {c.candidate_over_target:.12f}")
    print(f"candidate miss = {c.candidate_miss_percent:.9f}%")
    print(f"candidate scale sigma = {c.candidate_sigma_percent:.9f}%")
    print(f"candidate miss in sigma = {c.candidate_miss_in_sigma:.6f}")
    print()
    print("alpha prediction if candidate core scale is used")
    print(f"predicted alpha^-1 = {c.predicted_alpha_inv:.12f}")
    print(f"observed alpha^-1 = {ALPHA_INV_OBSERVED_LOW:.12f}")
    print(f"miss = {c.predicted_alpha_inv_miss:.12f}")
    print(f"alpha_inv sigma from lepton mass errors = {c.predicted_alpha_inv_sigma:.12f}")
    print(f"miss in sigma = {c.predicted_alpha_inv_miss_in_sigma:.6f}")
    print()
    print("frequency reading")
    print(f"C3*h frequency multiplier = {c.frequency_multiplier:.0f}")
    print("mu_core = (frequency multiplier)^2 * m_tau^2/m_e")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_C3_H2_CORE_SCALE_THEOREM_REQUIRED__PASS_TAU_ELECTRON_LOCK_AUDIT")


if __name__ == "__main__":
    run_gate()
