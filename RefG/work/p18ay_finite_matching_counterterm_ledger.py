from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_INV_EXACT_C3 = 137.03616654750616
ALPHA_INV_PDG_RATIO = 137.0361358108052

CORE_SCALE_EXACT_C3_TEV = 222.45901084608514
CORE_SCALE_PDG_RATIO_TEV = 222.4452475742128

QED_B1_THREE_LEPTONS = 2.0 * 3.0 / (3.0 * math.pi)


@dataclass(frozen=True)
class MatchingCounterterm:
    label: str
    alpha_inv_candidate: float
    alpha_candidate: float
    alpha_inv_observed: float
    alpha_observed: float
    additive_delta_alpha_inv: float
    relative_delta_alpha_inv_ppm: float
    alpha_ratio_observed_over_candidate: float
    charge_ratio_observed_over_candidate: float
    maxwell_stiffness_ratio_needed: float
    equal_factor_ratio_observed_over_candidate: float
    core_scale_ratio_needed_if_three_lepton_running: float
    core_scale_percent_needed: float
    corrected_core_scale_tev: float


def matching_counterterm(
    label: str,
    alpha_inv_candidate: float,
    core_scale_tev: float,
) -> MatchingCounterterm:
    alpha_candidate = 1.0 / alpha_inv_candidate
    alpha_observed = 1.0 / ALPHA_INV_OBSERVED_LOW

    delta_inv = ALPHA_INV_OBSERVED_LOW - alpha_inv_candidate
    alpha_ratio = alpha_observed / alpha_candidate

    # If alpha = e^2/(4*pi), this is the charge-amplitude normalization.
    charge_ratio = math.sqrt(alpha_ratio)

    # If alpha is inversely proportional to the Maxwell stiffness K_F, then
    # K_F,obs/K_F,cand = alpha_cand/alpha_obs.
    stiffness_ratio = alpha_candidate / alpha_observed

    # In the equal-factor picture alpha=f^4.
    equal_factor_ratio = alpha_ratio ** 0.25

    # If the residual is absorbed only by shifting the high matching scale
    # while all three charged leptons are active:
    #   delta alpha_inv = B_three * delta ln(mu_core).
    log_core_shift = delta_inv / QED_B1_THREE_LEPTONS
    core_ratio = math.exp(log_core_shift)

    return MatchingCounterterm(
        label=label,
        alpha_inv_candidate=alpha_inv_candidate,
        alpha_candidate=alpha_candidate,
        alpha_inv_observed=ALPHA_INV_OBSERVED_LOW,
        alpha_observed=alpha_observed,
        additive_delta_alpha_inv=delta_inv,
        relative_delta_alpha_inv_ppm=1.0e6 * delta_inv / alpha_inv_candidate,
        alpha_ratio_observed_over_candidate=alpha_ratio,
        charge_ratio_observed_over_candidate=charge_ratio,
        maxwell_stiffness_ratio_needed=stiffness_ratio,
        equal_factor_ratio_observed_over_candidate=equal_factor_ratio,
        core_scale_ratio_needed_if_three_lepton_running=core_ratio,
        core_scale_percent_needed=100.0 * (core_ratio - 1.0),
        corrected_core_scale_tev=core_scale_tev * core_ratio,
    )


def all_counterterms() -> tuple[MatchingCounterterm, MatchingCounterterm]:
    return (
        matching_counterterm(
            "exact_C3_ratios",
            ALPHA_INV_EXACT_C3,
            CORE_SCALE_EXACT_C3_TEV,
        ),
        matching_counterterm(
            "PDG_ratio_thresholds",
            ALPHA_INV_PDG_RATIO,
            CORE_SCALE_PDG_RATIO_TEV,
        ),
    )


def interpretation() -> list[str]:
    return [
        "The remaining correction can be represented equivalently as a tiny additive alpha^-1 counterterm, a charge normalization, a Maxwell-stiffness normalization, an equal-factor shift, or a small core-scale shift.",
        "For the exact-C3 version the required charge-amplitude normalization is about +0.61 ppm.",
        "For the equal-factor f language the required shift is about +0.305 ppm.",
        "For the core-scale language the required shift is about -0.026 percent.",
        "These are small enough to be a genuine matching layer, but they are not zero and must not be silently ignored.",
    ]


def open_tasks() -> list[str]:
    return [
        "decide which matching variable is physical in RefG: charge, Maxwell stiffness, boundary level, core scale, or equal readout factor",
        "derive that finite matching term from the charged h=2 core action",
        "separate ordinary QED/EW matching from RefG-specific boundary normalization",
        "keep the leading scale-free formula unchanged unless the action derivation demands otherwise",
    ]


def run_gate() -> None:
    terms = all_counterterms()

    exact, pdg = terms
    assert exact.additive_delta_alpha_inv < 0.0
    assert pdg.additive_delta_alpha_inv < 0.0
    assert abs(exact.relative_delta_alpha_inv_ppm) < 2.0
    assert abs(pdg.relative_delta_alpha_inv_ppm) < 2.0
    assert 0.999 < exact.core_scale_ratio_needed_if_three_lepton_running < 1.0
    assert 1.0 < exact.charge_ratio_observed_over_candidate < 1.00001

    print("p18ay finite matching counterterm ledger")
    for term in terms:
        print()
        print(f"[{term.label}]")
        print(f"candidate alpha^-1 = {term.alpha_inv_candidate:.12f}")
        print(f"observed alpha^-1 = {term.alpha_inv_observed:.12f}")
        print(f"delta alpha^-1 = {term.additive_delta_alpha_inv:.12f}")
        print(f"relative delta alpha^-1 = {term.relative_delta_alpha_inv_ppm:.6f} ppm")
        print(
            "alpha observed/candidate = "
            f"{term.alpha_ratio_observed_over_candidate:.12f}"
        )
        print(
            "charge observed/candidate = "
            f"{term.charge_ratio_observed_over_candidate:.12f}"
        )
        print(
            "Maxwell stiffness observed/candidate = "
            f"{term.maxwell_stiffness_ratio_needed:.12f}"
        )
        print(
            "equal f observed/candidate = "
            f"{term.equal_factor_ratio_observed_over_candidate:.12f}"
        )
        print(
            "core scale ratio if absorbed in three-lepton running = "
            f"{term.core_scale_ratio_needed_if_three_lepton_running:.12f}"
        )
        print(f"core scale shift = {term.core_scale_percent_needed:.9f}%")
        print(f"corrected core scale = {term.corrected_core_scale_tev:.9f} TeV")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_PHYSICAL_MATCHING_VARIABLE_SELECTION__PASS_COUNTERTERM_LEDGER")


if __name__ == "__main__":
    run_gate()
