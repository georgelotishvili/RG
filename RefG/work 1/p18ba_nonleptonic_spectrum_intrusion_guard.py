from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_INV_BARE_H2 = 81.0 * math.pi / 2.0
CORE_SCALE_TEV = 222.4452475742128

QED_B1_PER_UNIT_CHARGE = 2.0 / (3.0 * math.pi)

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}


@dataclass(frozen=True)
class ExtraSpectrumScenario:
    label: str
    extra_charge_sum: float
    activation_scale_gev: float
    extra_shift_alpha_inv: float
    alpha_inv_with_extra: float
    miss_vs_observed: float
    destroys_ppm_candidate: bool


def lepton_only_alpha_inv(mu_core_tev: float = CORE_SCALE_TEV) -> float:
    mu_core_mev = mu_core_tev * 1.0e6
    shift = QED_B1_PER_UNIT_CHARGE * (
        3.0 * math.log(mu_core_mev / LEPTON_MASSES_MEV["tau"])
        + 2.0 * math.log(LEPTON_MASSES_MEV["tau"] / LEPTON_MASSES_MEV["muon"])
        + math.log(LEPTON_MASSES_MEV["muon"] / LEPTON_MASSES_MEV["electron"])
    )
    return ALPHA_INV_BARE_H2 + shift


def extra_spectrum_shift(
    extra_charge_sum: float,
    activation_scale_gev: float,
    mu_core_tev: float = CORE_SCALE_TEV,
) -> float:
    high_gev = mu_core_tev * 1000.0
    if not high_gev > activation_scale_gev:
        return 0.0
    return QED_B1_PER_UNIT_CHARGE * extra_charge_sum * math.log(
        high_gev / activation_scale_gev
    )


def scenarios() -> tuple[ExtraSpectrumScenario, ...]:
    base = lepton_only_alpha_inv()

    # Charge sums are deliberately schematic guards:
    # - five light quarks up to b: 3 colors*(4/9+1/9+1/9+4/9+1/9)=11/3
    # - all six quarks: 5
    # - W+- is not treated by QED beta here; it is listed as EW matching needed,
    #   not included as a naive QED fermion term.
    definitions = (
        ("five_quarks_from_5GeV_schematic", 11.0 / 3.0, 5.0),
        ("all_quarks_from_173GeV_schematic", 5.0, 173.0),
        ("generic_extra_unit_charge_from_EW", 1.0, 100.0),
        ("generic_extra_charge_sum_5_from_EW", 5.0, 100.0),
    )

    rows = []
    for label, charge_sum, scale in definitions:
        shift = extra_spectrum_shift(charge_sum, scale)
        predicted = base + shift
        miss = predicted - ALPHA_INV_OBSERVED_LOW
        rows.append(
            ExtraSpectrumScenario(
                label=label,
                extra_charge_sum=charge_sum,
                activation_scale_gev=scale,
                extra_shift_alpha_inv=shift,
                alpha_inv_with_extra=predicted,
                miss_vs_observed=miss,
                destroys_ppm_candidate=abs(miss) > 0.01,
            )
        )
    return tuple(rows)


def interpretation() -> list[str]:
    return [
        "The ppm alpha candidate is not compatible with naively adding ordinary non-leptonic charged running over the whole 222 TeV interval.",
        "Therefore the lepton-only bridge must be interpreted as an effective charged-lepton threshold bridge, or it must be replaced by a completed EW/U1 matching theorem.",
        "This is not a weakness of the leading C3/h=2 formula; it identifies the exact place where Standard-Model matching must be handled.",
        "A final alpha claim must say what happens to quark, W and electroweak-sector contributions before the observed alpha(0) comparison.",
    ]


def allowed_completions() -> list[str]:
    return [
        "RefG derives an effective lepton-only Maxwell readout sector for this boundary register",
        "RefG derives a U(1)/EW matching counterterm that cancels or reshapes non-leptonic contributions",
        "RefG shows the bare h=2 alpha is defined below the non-leptonic activation scale in the relevant effective theory",
        "RefG includes the full charged spectrum and moves the leading formula accordingly",
    ]


def run_gate() -> None:
    base = lepton_only_alpha_inv()
    rows = scenarios()

    assert abs(base - ALPHA_INV_OBSERVED_LOW) < 2.0e-4
    assert all(row.destroys_ppm_candidate for row in rows)
    assert any(row.extra_shift_alpha_inv > 1.0 for row in rows)

    print("p18ba non-leptonic spectrum intrusion guard")
    print(f"lepton-only candidate alpha^-1 = {base:.12f}")
    print(f"observed alpha^-1 = {ALPHA_INV_OBSERVED_LOW:.12f}")
    print(f"lepton-only miss = {base - ALPHA_INV_OBSERVED_LOW:.12f}")
    print()
    print("extra-spectrum scenarios")
    for row in rows:
        print(f"- {row}")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("allowed completions")
    for item in allowed_completions():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_EW_U1_MATCHING_OR_LEPTON_ONLY_EFFECTIVE_THEOREM_REQUIRED__PASS_NONLEPTONIC_INTRUSION_GUARD")


if __name__ == "__main__":
    run_gate()
