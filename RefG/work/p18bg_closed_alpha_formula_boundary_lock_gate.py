from __future__ import annotations

import math
from dataclasses import dataclass

from p18ar_c3_h2_alpha_prediction_candidate_gate import (
    LEPTON_MASS_SIGMA_MEV,
    LEPTON_MASSES_MEV,
)
from p18bb_internal_external_em_readout_split_gate import (
    ALPHA_INV_OBSERVED_LOW,
    C3_ORDER,
    H_BRANCH,
    QED_B1_PER_UNIT_CHARGE,
    QED_B1_THREE_LEPTONS,
)
from p18bf_boundary_alpha_over_34_lock_gate import (
    boundary_hidden_count,
    solve_alpha_inv_with_boundary_N,
)


@dataclass(frozen=True)
class ClosedBoundaryAlpha:
    h_branch: int
    core_slot_count: int
    external_helicity_count: int
    boundary_hidden_count: int
    internal_threshold_alpha_inv: float
    predicted_alpha_inv: float
    observed_alpha_inv: float
    miss_alpha_inv: float
    miss_alpha_inv_ppm: float
    predicted_alpha: float
    observed_alpha: float
    relative_alpha_miss_ppm: float
    input_mass_sigma_alpha_inv: float
    miss_in_input_sigma: float
    formula: str


def internal_threshold_alpha_inv_from_masses(
    electron: float,
    muon: float,
    tau: float,
    h: float = H_BRANCH,
) -> float:
    """Scale-free h=2/C3-threshold bridge written with physical lepton ratios."""

    tau_over_e = tau / electron
    muon_over_e = muon / electron
    log_argument = ((C3_ORDER * h) ** 2) ** 3 * tau_over_e**5 / muon_over_e
    return 324.0 * math.pi / (h**3) + QED_B1_PER_UNIT_CHARGE * math.log(
        log_argument
    )


def closed_alpha_inv_from_masses(
    electron: float,
    muon: float,
    tau: float,
) -> float:
    internal = internal_threshold_alpha_inv_from_masses(electron, muon, tau)
    _, _, hidden_count = boundary_hidden_count()
    return solve_alpha_inv_with_boundary_N(internal, hidden_count)


def input_mass_sigma_alpha_inv() -> float:
    central = closed_alpha_inv_from_masses(
        LEPTON_MASSES_MEV["electron"],
        LEPTON_MASSES_MEV["muon"],
        LEPTON_MASSES_MEV["tau"],
    )

    contributions: list[float] = []
    for name, sigma in LEPTON_MASS_SIGMA_MEV.items():
        plus = dict(LEPTON_MASSES_MEV)
        minus = dict(LEPTON_MASSES_MEV)
        plus[name] += sigma
        minus[name] -= sigma
        shifted_plus = closed_alpha_inv_from_masses(
            plus["electron"], plus["muon"], plus["tau"]
        )
        shifted_minus = closed_alpha_inv_from_masses(
            minus["electron"], minus["muon"], minus["tau"]
        )
        contributions.append((shifted_plus - shifted_minus) / 2.0)

    sigma_total = math.sqrt(sum(item * item for item in contributions))

    # Keep the central variable used, so a future refactor cannot accidentally
    # make this function independent of the prediction path.
    assert abs(central - closed_alpha_candidate().predicted_alpha_inv) < 1.0e-12
    return sigma_total


def closed_alpha_candidate() -> ClosedBoundaryAlpha:
    core_slots, external_helicity, hidden_count = boundary_hidden_count()
    internal = internal_threshold_alpha_inv_from_masses(
        LEPTON_MASSES_MEV["electron"],
        LEPTON_MASSES_MEV["muon"],
        LEPTON_MASSES_MEV["tau"],
    )
    predicted = solve_alpha_inv_with_boundary_N(internal, hidden_count)
    alpha_pred = 1.0 / predicted
    alpha_obs = 1.0 / ALPHA_INV_OBSERVED_LOW
    miss = predicted - ALPHA_INV_OBSERVED_LOW

    formula = (
        "Let Y = 324*pi/h^3 + (2/(3*pi))*ln(((3h)^2)^3 "
        "*(m_tau/m_e)^5/(m_mu/m_e)); "
        "N=(3h)^2-h; alpha^-1 = (Y + sqrt(Y^2 - 8/(pi*N)))/2, with h=2."
    )

    # Avoid recursive call from input_mass_sigma_alpha_inv while building the
    # central candidate.
    return ClosedBoundaryAlpha(
        h_branch=int(H_BRANCH),
        core_slot_count=core_slots,
        external_helicity_count=external_helicity,
        boundary_hidden_count=hidden_count,
        internal_threshold_alpha_inv=internal,
        predicted_alpha_inv=predicted,
        observed_alpha_inv=ALPHA_INV_OBSERVED_LOW,
        miss_alpha_inv=miss,
        miss_alpha_inv_ppm=1.0e6 * miss / ALPHA_INV_OBSERVED_LOW,
        predicted_alpha=alpha_pred,
        observed_alpha=alpha_obs,
        relative_alpha_miss_ppm=1.0e6 * (alpha_pred - alpha_obs) / alpha_obs,
        input_mass_sigma_alpha_inv=float("nan"),
        miss_in_input_sigma=float("nan"),
        formula=formula,
    )


def closed_alpha_candidate_with_sigma() -> ClosedBoundaryAlpha:
    base = closed_alpha_candidate()
    sigma = input_mass_sigma_alpha_inv()
    return ClosedBoundaryAlpha(
        h_branch=base.h_branch,
        core_slot_count=base.core_slot_count,
        external_helicity_count=base.external_helicity_count,
        boundary_hidden_count=base.boundary_hidden_count,
        internal_threshold_alpha_inv=base.internal_threshold_alpha_inv,
        predicted_alpha_inv=base.predicted_alpha_inv,
        observed_alpha_inv=base.observed_alpha_inv,
        miss_alpha_inv=base.miss_alpha_inv,
        miss_alpha_inv_ppm=base.miss_alpha_inv_ppm,
        predicted_alpha=base.predicted_alpha,
        observed_alpha=base.observed_alpha,
        relative_alpha_miss_ppm=base.relative_alpha_miss_ppm,
        input_mass_sigma_alpha_inv=sigma,
        miss_in_input_sigma=base.miss_alpha_inv / sigma,
        formula=base.formula,
    )


def derivation_chain() -> list[str]:
    return [
        "Use the h=2 bare boundary term alpha_bare^-1=324*pi/h^3.",
        "Use the C3/h lepton threshold bridge through the scale-free log argument ((3h)^2)^3*(m_tau/m_e)^5/(m_mu/m_e).",
        "Use the h=2 boundary hidden count N=(3h)^2-h=34.",
        "Postulate the remaining external Maxwell readout deficit q_boundary=alpha/N.",
        "Solve alpha self-consistently instead of inserting observed alpha.",
    ]


def open_tasks() -> list[str]:
    return [
        "derive N=(3h)^2-h from the charged orientation-frame core action",
        "derive q_boundary=alpha/N rather than treating it as a lock hypothesis",
        "derive the lepton mass ratios or justify the use of physical pole masses in this bridge",
        "complete the QED/EW matching audit around the physical threshold convention",
    ]


def run_gate() -> None:
    result = closed_alpha_candidate_with_sigma()

    assert result.h_branch == 2
    assert result.core_slot_count == 36
    assert result.external_helicity_count == 2
    assert result.boundary_hidden_count == 34
    assert abs(result.miss_alpha_inv_ppm) < 1.0e-4
    assert abs(result.miss_in_input_sigma) < 1.0e-3
    assert result.input_mass_sigma_alpha_inv > 1.0e-5

    print("p18bg closed alpha formula with boundary lock gate")
    print("candidate")
    print(result)
    print()
    print("derivation chain")
    for item in derivation_chain():
        print(f"- {item}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_ACTION_DERIVATION_OF_BOUNDARY_LOCK_REQUIRED__PASS_CLOSED_ALPHA_FORMULA")


if __name__ == "__main__":
    run_gate()
