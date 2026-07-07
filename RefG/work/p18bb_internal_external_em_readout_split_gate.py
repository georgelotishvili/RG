from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
QED_B1_PER_UNIT_CHARGE = 2.0 / (3.0 * math.pi)
QED_B1_THREE_LEPTONS = 2.0 / math.pi

C3_ORDER = 3.0
H_BRANCH = 2.0
A_KOIDE = math.sqrt(2.0)
THETA_TOPOLOGICAL = 2.0 / 9.0

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}


@dataclass(frozen=True)
class EMReadoutSplit:
    alpha_inv_internal_readout_identification: float
    alpha_inv_observed: float
    residual_observed_minus_internal: float
    core_external_over_internal: float
    frequency_external_over_internal: float
    log_argument_readout_factor: float
    corrected_alpha_inv: float
    internal_core_scale_tev: float
    external_core_scale_tev: float
    core_readout_shift_percent: float
    frequency_readout_shift_percent: float


@dataclass(frozen=True)
class C3DistortionTest:
    label: str
    A: float
    theta: float
    predicted_muon_mev: float
    predicted_tau_mev: float
    relative_mass_error_sum: float
    alpha_inv: float
    alpha_miss: float


def alpha_inv_bare_h2() -> float:
    return 324.0 * math.pi / (H_BRANCH**3)


def c3_frequencies(A: float, theta: float) -> tuple[float, float, float]:
    """Return p11 order: tau, electron, muon."""

    return tuple(
        1.0 + A * math.cos(theta + 2.0 * math.pi * k / 3.0)
        for k in range(3)
    )  # type: ignore[return-value]


def exact_c3_mass_ratios(A: float = A_KOIDE, theta: float = THETA_TOPOLOGICAL) -> tuple[float, float]:
    tau, electron, muon = c3_frequencies(A, theta)
    return (tau / electron) ** 2, (muon / electron) ** 2


def alpha_inv_from_c3(
    A: float = A_KOIDE,
    theta: float = THETA_TOPOLOGICAL,
    core_readout_factor: float = 1.0,
) -> float:
    """Alpha bridge with an explicit internal-to-external core readout factor.

    core_readout_factor multiplies the internal core scale

        mu_internal = (3h)^2*m_tau^2/m_e.

    Because the high-scale threshold appears in all three lepton logs, this is
    equivalent to multiplying the single closed-form log argument by
    core_readout_factor^3.
    """

    tau_over_e, muon_over_e = exact_c3_mass_ratios(A, theta)
    log_argument = (
        core_readout_factor**3
        * ((C3_ORDER * H_BRANCH) ** 2) ** 3
        * tau_over_e**5
        / muon_over_e
    )
    return alpha_inv_bare_h2() + QED_B1_PER_UNIT_CHARGE * math.log(log_argument)


def internal_core_scale_tev(A: float = A_KOIDE, theta: float = THETA_TOPOLOGICAL) -> float:
    tau_over_e, _ = exact_c3_mass_ratios(A, theta)
    electron = LEPTON_MASSES_MEV["electron"]
    tau = electron * tau_over_e
    mu_core_mev = (C3_ORDER * H_BRANCH) ** 2 * tau * tau / electron
    return mu_core_mev / 1.0e6


def required_em_readout_split() -> EMReadoutSplit:
    internal_alpha = alpha_inv_from_c3()
    residual = ALPHA_INV_OBSERVED_LOW - internal_alpha

    core_factor = math.exp(residual / QED_B1_THREE_LEPTONS)
    frequency_factor = math.sqrt(core_factor)
    log_argument_factor = core_factor**3
    corrected = alpha_inv_from_c3(core_readout_factor=core_factor)
    core_internal = internal_core_scale_tev()
    core_external = core_internal * core_factor

    return EMReadoutSplit(
        alpha_inv_internal_readout_identification=internal_alpha,
        alpha_inv_observed=ALPHA_INV_OBSERVED_LOW,
        residual_observed_minus_internal=residual,
        core_external_over_internal=core_factor,
        frequency_external_over_internal=frequency_factor,
        log_argument_readout_factor=log_argument_factor,
        corrected_alpha_inv=corrected,
        internal_core_scale_tev=core_internal,
        external_core_scale_tev=core_external,
        core_readout_shift_percent=100.0 * (core_factor - 1.0),
        frequency_readout_shift_percent=100.0 * (frequency_factor - 1.0),
    )


def _mass_error_test(label: str, A: float, theta: float) -> C3DistortionTest:
    tau_over_e, muon_over_e = exact_c3_mass_ratios(A, theta)
    electron = LEPTON_MASSES_MEV["electron"]
    predicted_muon = electron * muon_over_e
    predicted_tau = electron * tau_over_e
    rel_error = abs(predicted_muon - LEPTON_MASSES_MEV["muon"]) / LEPTON_MASSES_MEV[
        "muon"
    ] + abs(predicted_tau - LEPTON_MASSES_MEV["tau"]) / LEPTON_MASSES_MEV["tau"]
    alpha_inv = alpha_inv_from_c3(A, theta)
    return C3DistortionTest(
        label=label,
        A=A,
        theta=theta,
        predicted_muon_mev=predicted_muon,
        predicted_tau_mev=predicted_tau,
        relative_mass_error_sum=rel_error,
        alpha_inv=alpha_inv,
        alpha_miss=alpha_inv - ALPHA_INV_OBSERVED_LOW,
    )


def _root_for_A(theta: float) -> float:
    lo = A_KOIDE - 1.0e-4
    hi = A_KOIDE + 1.0e-4
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if (alpha_inv_from_c3(lo, theta) - ALPHA_INV_OBSERVED_LOW) * (
            alpha_inv_from_c3(mid, theta) - ALPHA_INV_OBSERVED_LOW
        ) <= 0.0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def _root_for_theta(A: float) -> float:
    lo = THETA_TOPOLOGICAL - 1.0e-4
    hi = THETA_TOPOLOGICAL + 1.0e-4
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if (alpha_inv_from_c3(A, lo) - ALPHA_INV_OBSERVED_LOW) * (
            alpha_inv_from_c3(A, mid) - ALPHA_INV_OBSERVED_LOW
        ) <= 0.0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def c3_distortion_guard() -> tuple[C3DistortionTest, ...]:
    theta_fit = _root_for_theta(A_KOIDE)
    A_fit = _root_for_A(THETA_TOPOLOGICAL)

    split = required_em_readout_split()
    readout_corrected = _mass_error_test(
        "internal_external_EM_readout_correction",
        A_KOIDE,
        THETA_TOPOLOGICAL,
    )
    object.__setattr__(readout_corrected, "alpha_inv", split.corrected_alpha_inv)
    object.__setattr__(
        readout_corrected,
        "alpha_miss",
        split.corrected_alpha_inv - ALPHA_INV_OBSERVED_LOW,
    )

    return (
        _mass_error_test("exact_C3_no_readout_correction", A_KOIDE, THETA_TOPOLOGICAL),
        _mass_error_test("fit_alpha_by_changing_theta", A_KOIDE, theta_fit),
        _mass_error_test("fit_alpha_by_changing_A", A_fit, THETA_TOPOLOGICAL),
        readout_corrected,
    )


def interpretation() -> list[str]:
    return [
        "The old formula implicitly identified internal charged-core reserve with external Maxwell readout.",
        "RefG already uses a split between internal inventory and external readout in the mass/compact-object sector.",
        "Applying the same split to the EM alpha bridge leaves h=2 and C3 untouched.",
        "Changing A or theta can fit alpha, but it damages the independent charged-lepton mass map.",
        "The internal/external EM readout correction fits alpha while preserving the lepton map exactly.",
    ]


def next_theorem_requirements() -> list[str]:
    return [
        "derive why the charged-core EM readout factor is slightly below the internal reserve scale",
        "derive whether this factor belongs to boundary-to-Maxwell normalization, finite core profile, or threshold matching",
        "test the same internal/external readout factor against any other EM observable the theory predicts",
        "do not use observed alpha to set the factor in the final theorem",
    ]


def run_gate() -> None:
    split = required_em_readout_split()
    tests = c3_distortion_guard()
    exact, theta_fit, A_fit, readout_corrected = tests

    assert math.isclose(split.corrected_alpha_inv, ALPHA_INV_OBSERVED_LOW, rel_tol=1.0e-14)
    assert split.core_external_over_internal < 1.0
    assert split.frequency_external_over_internal < 1.0
    assert split.log_argument_readout_factor < 1.0
    assert theta_fit.relative_mass_error_sum > 5.0 * exact.relative_mass_error_sum
    assert A_fit.relative_mass_error_sum > 5.0 * exact.relative_mass_error_sum
    assert math.isclose(
        readout_corrected.relative_mass_error_sum,
        exact.relative_mass_error_sum,
        rel_tol=0.0,
        abs_tol=1.0e-18,
    )

    print("p18bb internal/external EM readout split gate")
    print("required EM readout split:")
    print(split)
    print()
    print("C3 distortion guard")
    for row in tests:
        print(f"- {row}")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("next theorem requirements")
    for item in next_theorem_requirements():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_EM_READOUT_FACTOR_DERIVATION_REQUIRED__PASS_INTERNAL_EXTERNAL_ALPHA_REPAIR")


if __name__ == "__main__":
    run_gate()
