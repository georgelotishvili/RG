from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_OBSERVED_LOW = 1.0 / ALPHA_INV_OBSERVED_LOW

ALPHA_INV_BARE_H2 = 81.0 * math.pi / 2.0
ALPHA_BARE_H2 = 1.0 / ALPHA_INV_BARE_H2

QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}


@dataclass(frozen=True)
class PerFactorDressing:
    alpha_inv_bare: float
    alpha_inv_observed: float
    delta_alpha_inv: float
    alpha_ratio_observed_over_bare: float
    amplitude_ratio_observed_over_bare: float
    per_factor_ratio_observed_over_bare: float
    per_factor_log_attenuation: float
    bare_equal_factor: float
    observed_equal_factor: float


@dataclass(frozen=True)
class LeptonThresholdTarget:
    required_sum_log: float
    required_mu_mev: float
    required_mu_gev: float
    required_mu_tev: float
    lepton_geometric_mean_mev: float
    required_mu_over_lepton_geometric_mean: float
    reconstructed_alpha_inv: float
    per_factor_ratio_from_running: float


def per_factor_dressing() -> PerFactorDressing:
    alpha_ratio = ALPHA_OBSERVED_LOW / ALPHA_BARE_H2
    amplitude_ratio = math.sqrt(alpha_ratio)
    per_factor_ratio = alpha_ratio ** 0.25

    bare_equal_factor = ALPHA_BARE_H2 ** 0.25
    observed_equal_factor = ALPHA_OBSERVED_LOW ** 0.25

    return PerFactorDressing(
        alpha_inv_bare=ALPHA_INV_BARE_H2,
        alpha_inv_observed=ALPHA_INV_OBSERVED_LOW,
        delta_alpha_inv=ALPHA_INV_OBSERVED_LOW - ALPHA_INV_BARE_H2,
        alpha_ratio_observed_over_bare=alpha_ratio,
        amplitude_ratio_observed_over_bare=amplitude_ratio,
        per_factor_ratio_observed_over_bare=per_factor_ratio,
        per_factor_log_attenuation=-math.log(per_factor_ratio),
        bare_equal_factor=bare_equal_factor,
        observed_equal_factor=observed_equal_factor,
    )


def _lepton_shift(alpha_scale_mev: float) -> float:
    total = 0.0
    for mass_mev in LEPTON_MASSES_MEV.values():
        if alpha_scale_mev > mass_mev:
            total += math.log(alpha_scale_mev / mass_mev)
    return QED_ONE_LOOP_B * total


def lepton_threshold_target() -> LeptonThresholdTarget:
    d = per_factor_dressing()
    required_sum_log = d.delta_alpha_inv / QED_ONE_LOOP_B

    mass_log_mean = sum(math.log(m) for m in LEPTON_MASSES_MEV.values()) / len(LEPTON_MASSES_MEV)
    lepton_geometric_mean = math.exp(mass_log_mean)

    # With all three charged leptons active:
    #   B * sum_i ln(mu/m_i) = delta_alpha_inv
    #   mu = (m_e*m_mu*m_tau)^(1/3) * exp(delta/(3B)).
    required_mu_mev = lepton_geometric_mean * math.exp(required_sum_log / len(LEPTON_MASSES_MEV))

    reconstructed_alpha_inv = ALPHA_INV_BARE_H2 + _lepton_shift(required_mu_mev)
    alpha_from_running = 1.0 / reconstructed_alpha_inv
    per_factor_ratio_from_running = (alpha_from_running / ALPHA_BARE_H2) ** 0.25

    return LeptonThresholdTarget(
        required_sum_log=required_sum_log,
        required_mu_mev=required_mu_mev,
        required_mu_gev=required_mu_mev / 1000.0,
        required_mu_tev=required_mu_mev / 1.0e6,
        lepton_geometric_mean_mev=lepton_geometric_mean,
        required_mu_over_lepton_geometric_mean=required_mu_mev / lepton_geometric_mean,
        reconstructed_alpha_inv=reconstructed_alpha_inv,
        per_factor_ratio_from_running=per_factor_ratio_from_running,
    )


def predict_alpha_inv_from_core_scale(mu_gev: float) -> float:
    return ALPHA_INV_BARE_H2 + _lepton_shift(mu_gev * 1000.0)


def benchmark_scales() -> dict[str, dict[str, float]]:
    scales_gev = {
        "10_TeV": 1.0e4,
        "100_TeV": 1.0e5,
        "target_222_TeV": lepton_threshold_target().required_mu_gev,
        "1_PeV": 1.0e6,
    }

    rows = {}
    for label, mu_gev in scales_gev.items():
        alpha_inv = predict_alpha_inv_from_core_scale(mu_gev)
        alpha = 1.0 / alpha_inv
        rows[label] = {
            "mu_GeV": mu_gev,
            "alpha_inv": alpha_inv,
            "miss_vs_observed_alpha_inv": alpha_inv - ALPHA_INV_OBSERVED_LOW,
            "per_factor_ratio_vs_bare": (alpha / ALPHA_BARE_H2) ** 0.25,
        }
    return rows


def interpretation() -> list[str]:
    return [
        "The h=2 branch gives the bare value alpha_bare^-1 = 81*pi/2.",
        "The observed value is reached by reducing each equal readout factor by 1.838190%.",
        "In a lepton-only one-loop threshold ledger this same correction corresponds to a core scale near 222 TeV.",
        "Therefore the next decisive target is not 137 itself, but an independent RefG derivation of either the 222 TeV scale or the 0.981618 per-factor dressing.",
        "If that scale or dressing is derived without CODATA input, the h=2 alpha route becomes predictive.",
    ]


def open_tasks() -> list[str]:
    return [
        "derive the charged-oscillon core scale independently",
        "derive the charged-lepton thresholds or explain why the C3 triplet is the active dressing sector",
        "derive whether QED-like one-loop dressing is the correct effective bridge in this RefG regime",
        "derive or reject the 0.981618 per-factor contraction from foundation readout",
    ]


def run_gate() -> None:
    d = per_factor_dressing()
    target = lepton_threshold_target()
    rows = benchmark_scales()

    assert math.isclose(d.per_factor_ratio_observed_over_bare**4, d.alpha_ratio_observed_over_bare, rel_tol=1e-14)
    assert math.isclose(d.observed_equal_factor / d.bare_equal_factor, d.per_factor_ratio_observed_over_bare, rel_tol=1e-14)
    assert math.isclose(target.reconstructed_alpha_inv, ALPHA_INV_OBSERVED_LOW, rel_tol=1e-12)
    assert math.isclose(target.per_factor_ratio_from_running, d.per_factor_ratio_observed_over_bare, rel_tol=1e-12)
    assert 200.0 < target.required_mu_tev < 250.0
    assert 0.98 < d.per_factor_ratio_observed_over_bare < 0.99

    print("p18ao bare-to-observed per-factor dressing gate")
    print(f"bare alpha^-1 h=2 = {d.alpha_inv_bare:.9f}")
    print(f"observed alpha^-1 = {d.alpha_inv_observed:.9f}")
    print(f"delta alpha^-1 = {d.delta_alpha_inv:.9f}")
    print()
    print("two-factor readout dressing")
    print(f"bare equal factor = {d.bare_equal_factor:.12f}")
    print(f"observed equal factor = {d.observed_equal_factor:.12f}")
    print(f"alpha ratio observed/bare = {d.alpha_ratio_observed_over_bare:.12f}")
    print(f"amplitude ratio observed/bare = {d.amplitude_ratio_observed_over_bare:.12f}")
    print(f"per-factor ratio observed/bare = {d.per_factor_ratio_observed_over_bare:.12f}")
    print(f"per-factor attenuation = {-100.0 * (d.per_factor_ratio_observed_over_bare - 1.0):.6f}%")
    print(f"per-factor log attenuation = {d.per_factor_log_attenuation:.12f}")
    print()
    print("lepton-threshold target equivalent")
    print(f"required sum log = {target.required_sum_log:.12f}")
    print(f"lepton geometric mean = {target.lepton_geometric_mean_mev:.12f} MeV")
    print(f"required mu = {target.required_mu_gev:.6f} GeV = {target.required_mu_tev:.6f} TeV")
    print(f"mu / lepton geometric mean = {target.required_mu_over_lepton_geometric_mean:.12e}")
    print(f"reconstructed alpha^-1 = {target.reconstructed_alpha_inv:.9f}")
    print(f"per-factor ratio from running = {target.per_factor_ratio_from_running:.12f}")
    print()
    print("benchmark scales")
    for label, row in rows.items():
        print(f"- {label}: {row}")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_CORE_SCALE_OR_PER_FACTOR_DRESSING_DERIVATION__PASS_BARE_TO_OBSERVED_REDUCTION")


if __name__ == "__main__":
    run_gate()
