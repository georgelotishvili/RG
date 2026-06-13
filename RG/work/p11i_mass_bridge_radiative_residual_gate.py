# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: charged-lepton pole-mass audit; no new fit.

"""PHASE 51 (p11i): mass bridge, radiative protection, and residual budget.

The C3 charged-lepton operator is a frequency-ratio statement.  To become a
mass theorem it needs two additional results:

1. an oscillon energy theorem showing that the dressed pole mass scales as
   the square of the C3 normal frequency, m ~ nu^2;
2. a pole/radiative theorem showing that the observed charged-lepton pole
   masses are protected C3 eigenvalues, or that the required residual dressing
   is derived by the same field equations.

This file does not solve either theorem.  It quantifies the budget.
Exact (sqrt(2), theta=2/9) plus the electron anchor misses the muon by only
about 1e-5 relative mass, but by hundreds of PDG sigma.  Therefore the muon
residual must either be derived as a real dressed-pole correction or the
claim must stay at relative-compression level.
"""

from __future__ import annotations

import math
from typing import Sequence


THETA_TOPOLOGICAL = 2.0 / 9.0
A_KOIDE = math.sqrt(2.0)
ALPHA_EM = 1.0 / 137.035999084

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}

LEPTON_MASS_UNCERTAINTY_MEV = {
    "electron": 1.6e-10,
    "muon": 2.3e-06,
    "tau": 0.09,
}

ORDER = ("electron", "muon", "tau")


def c3_raw_frequencies(theta: float = THETA_TOPOLOGICAL) -> list[float]:
    return [
        1.0 + A_KOIDE * math.cos(theta + 2.0 * math.pi * k / 3.0)
        for k in range(3)
    ]


def c3_frequency_ratios(theta: float = THETA_TOPOLOGICAL) -> dict[str, float]:
    raw = sorted(c3_raw_frequencies(theta))
    base = raw[0]
    return {name: value / base for name, value in zip(ORDER, raw)}


def c3_mass_predictions(theta: float = THETA_TOPOLOGICAL) -> dict[str, float]:
    ratios = c3_frequency_ratios(theta)
    m_e = LEPTON_MASSES_MEV["electron"]
    return {name: m_e * ratios[name] ** 2 for name in ORDER}


def koide_ratio_from_frequencies(nu: Sequence[float]) -> float:
    return sum(value * value for value in nu) / (sum(nu) ** 2)


def residual_budget() -> list[dict[str, object]]:
    predicted = c3_mass_predictions()
    rows = []
    for name in ORDER:
        observed = LEPTON_MASSES_MEV[name]
        pred = predicted[name]
        sigma = LEPTON_MASS_UNCERTAINTY_MEV[name]
        mass_fractional_shift_needed = observed / pred - 1.0
        freq_fractional_shift_needed = math.sqrt(observed / pred) - 1.0
        rows.append(
            {
                "particle": name,
                "role": "anchor" if name == "electron" else "non_anchor_test",
                "predicted_MeV": pred,
                "observed_MeV": observed,
                "residual_MeV": pred - observed,
                "residual_relative_to_observed": (pred - observed) / observed,
                "residual_pdg_sigma": (pred - observed) / sigma,
                "required_mass_dressing_observed_over_pred_minus_1": mass_fractional_shift_needed,
                "required_frequency_dressing_sqrt_observed_over_pred_minus_1": freq_fractional_shift_needed,
            }
        )
    return rows


def required_dressing_vector() -> dict[str, object]:
    rows = residual_budget()
    eps = [
        row["required_frequency_dressing_sqrt_observed_over_pred_minus_1"]
        for row in rows
    ]
    raw = c3_frequency_ratios()
    nu = [raw[name] for name in ORDER]
    shifted = [value * (1.0 + eps_i) for value, eps_i in zip(nu, eps)]
    return {
        "frequency_fractional_shifts": {
            row["particle"]: row[
                "required_frequency_dressing_sqrt_observed_over_pred_minus_1"
            ]
            for row in rows
        },
        "koide_before": koide_ratio_from_frequencies(nu),
        "koide_after_required_dressing": koide_ratio_from_frequencies(shifted),
        "koide_drift_required_dressing": koide_ratio_from_frequencies(shifted) - 2.0 / 3.0,
        "meaning": (
            "these are the exact fractional pole-frequency dressings needed "
            "to map the electron-anchored C3 masses to the observed pole masses"
        ),
    }


def mass_bridge_theorem_contract() -> list[dict[str, str]]:
    return [
        {
            "stage": "finite-energy oscillon solution",
            "status": "OPEN",
            "required_result": "construct a localized, regular, spectrally stable charged oscillon profile",
        },
        {
            "stage": "Noether/pole mass identity",
            "status": "PARTIAL_UPSTREAM",
            "required_result": "use p06: M=E0/c^2 once the localized dressed stress tensor and Laue condition are verified",
        },
        {
            "stage": "frequency-energy scaling",
            "status": "OPEN",
            "required_result": "show that the dressed pole energy scales as E0 proportional to nu_C3^2 for the charged C3 branch",
        },
        {
            "stage": "absolute scale",
            "status": "OPEN",
            "required_result": "derive the electron scale; current tables insert m_e as an anchor",
        },
    ]


def leading_qed_log_stress(cutoff_mev: float) -> dict[str, object]:
    prefactor_mass = 3.0 * ALPHA_EM / (4.0 * math.pi)
    freq_shifts = {}
    for name in ORDER:
        mass = LEPTON_MASSES_MEV[name]
        dm_over_m = prefactor_mass * math.log((cutoff_mev / mass) ** 2)
        freq_shifts[name] = 0.5 * dm_over_m
    mean_shift = sum(freq_shifts.values()) / len(freq_shifts)
    generation_dependent = {
        name: shift - mean_shift for name, shift in freq_shifts.items()
    }
    return {
        "cutoff_MeV": cutoff_mev,
        "freq_shifts": freq_shifts,
        "generation_dependent_part": generation_dependent,
        "max_generation_dependent_abs": max(abs(v) for v in generation_dependent.values()),
        "meaning": (
            "ordinary generation-dependent logs are much larger than the "
            "required 1e-5-level residual budget unless protected or absorbed"
        ),
    }


def radiative_protection_contract() -> list[dict[str, str]]:
    return [
        {
            "route": "A. dressed pole-frequency theorem",
            "needed": "derive the charged normal-mode equation with EM/self-field backreaction already included",
            "status": "BEST_RG_ONTOLOGY_MATCH__OPEN",
        },
        {
            "route": "B. Ward/Sumino-like cancellation",
            "needed": "identify an RG current/loop sector that cancels generation-dependent QED logs",
            "status": "OPEN",
        },
        {
            "route": "C. matching-scale theorem",
            "needed": "derive RG running from the C3 matching scale to pole masses",
            "status": "OPEN",
        },
    ]


def mass_radiative_residual_gate() -> dict[str, object]:
    rows = residual_budget()
    required = required_dressing_vector()
    muon = next(row for row in rows if row["particle"] == "muon")
    tau = next(row for row in rows if row["particle"] == "tau")
    stress = leading_qed_log_stress(1.0e6)

    pdg_precision_pass = (
        abs(muon["residual_pdg_sigma"]) <= 1.0
        and abs(tau["residual_pdg_sigma"]) <= 1.0
    )
    relative_compression = all(
        abs(row["residual_relative_to_observed"]) < 1.0e-4
        for row in rows
        if row["role"] != "anchor"
    )

    return {
        "status": "OPEN_MASS_BRIDGE_AND_RADIATIVE_PROTECTION__RESIDUAL_BUDGET_QUANTIFIED",
        "relative_compression_pass": relative_compression,
        "pdg_precision_pass": pdg_precision_pass,
        "residual_budget": rows,
        "required_dressing_vector": required,
        "qed_log_stress_test_1e6_MeV": stress,
        "mass_bridge_contract": mass_bridge_theorem_contract(),
        "radiative_protection_contract": radiative_protection_contract(),
        "strongest_allowed_claim": (
            "C3 gives a strong charged-lepton relative-compression candidate. "
            "It is not a pole-mass prediction until m~nu^2, absolute scale, "
            "and radiative/dressed-pole protection are derived."
        ),
        "do_not_claim": [
            "Do not claim m~nu^2 is derived from the oscillon energy functional.",
            "Do not claim the electron mass is derived; it is still the anchor.",
            "Do not claim charged-lepton pole masses are predicted within PDG uncertainty.",
            "Do not patch the muon residual with an ad hoc correction after seeing the masses.",
            "Do not claim radiative protection before route A, B, or C is derived.",
        ],
    }


def main() -> None:
    gate = mass_radiative_residual_gate()
    print("PHASE 51: mass bridge / radiative / residual gate")
    print(f"status: {gate['status']}")
    print(f"relative_compression_pass: {gate['relative_compression_pass']}")
    print(f"pdg_precision_pass: {gate['pdg_precision_pass']}")
    for row in gate["residual_budget"]:
        if row["role"] == "anchor":
            continue
        print(
            f"{row['particle']}: rel={row['residual_relative_to_observed']:.3e}, "
            f"sigma={row['residual_pdg_sigma']:.3f}, "
            f"freq_shift_needed={row['required_frequency_dressing_sqrt_observed_over_pred_minus_1']:.3e}"
        )


if __name__ == "__main__":
    main()
