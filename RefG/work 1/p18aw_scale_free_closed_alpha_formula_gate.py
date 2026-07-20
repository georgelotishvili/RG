from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)

A_KOIDE = math.sqrt(2.0)
THETA_TOPOLOGICAL = 2.0 / 9.0
C3_ORDER = 3.0
H_BRANCH = 2.0

PDG_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}


@dataclass(frozen=True)
class ClosedFormulaResult:
    alpha_inv_bare: float
    tau_over_e_ratio: float
    muon_over_e_ratio: float
    log_argument: float
    log_argument_ln: float
    threshold_shift: float
    alpha_inv_predicted: float
    alpha_inv_observed: float
    miss: float
    miss_ppm: float
    pdg_ratio_predicted: float
    exact_minus_pdg_ratio: float


def alpha_inv_bare(h: float = H_BRANCH) -> float:
    return 324.0 * math.pi / (h**3)


def exact_c3_mass_ratios() -> tuple[float, float]:
    tau, electron, muon = (
        1.0 + A_KOIDE * math.cos(THETA_TOPOLOGICAL + 2.0 * math.pi * k / 3.0)
        for k in range(3)
    )
    return (tau / electron) ** 2, (muon / electron) ** 2


def closed_alpha_formula(
    tau_over_e: float,
    muon_over_e: float,
    h: float = H_BRANCH,
) -> float:
    """Scale-free alpha candidate.

    Start from
        alpha_bare^-1 = 324*pi/h^3,
        mu_core = (3h)^2*m_tau^2/m_e,
        Delta = B[3 ln(mu_core/m_tau)
                  +2 ln(m_tau/m_mu)
                  +  ln(m_mu/m_e)].

    With x=m_tau/m_e and y=m_mu/m_e, the absolute mass cancels:
        Delta = B ln(((3h)^2)^3 * x^5 / y).
    """

    log_argument = ((C3_ORDER * h) ** 2) ** 3 * tau_over_e**5 / muon_over_e
    return alpha_inv_bare(h) + QED_ONE_LOOP_B * math.log(log_argument)


def evaluate_closed_formula() -> ClosedFormulaResult:
    tau_over_e, muon_over_e = exact_c3_mass_ratios()
    log_argument = ((C3_ORDER * H_BRANCH) ** 2) ** 3 * tau_over_e**5 / muon_over_e
    shift = QED_ONE_LOOP_B * math.log(log_argument)
    predicted = alpha_inv_bare() + shift

    pdg_tau_over_e = PDG_MASSES_MEV["tau"] / PDG_MASSES_MEV["electron"]
    pdg_muon_over_e = PDG_MASSES_MEV["muon"] / PDG_MASSES_MEV["electron"]
    pdg_predicted = closed_alpha_formula(pdg_tau_over_e, pdg_muon_over_e)

    return ClosedFormulaResult(
        alpha_inv_bare=alpha_inv_bare(),
        tau_over_e_ratio=tau_over_e,
        muon_over_e_ratio=muon_over_e,
        log_argument=log_argument,
        log_argument_ln=math.log(log_argument),
        threshold_shift=shift,
        alpha_inv_predicted=predicted,
        alpha_inv_observed=ALPHA_INV_OBSERVED_LOW,
        miss=predicted - ALPHA_INV_OBSERVED_LOW,
        miss_ppm=1.0e6 * (predicted - ALPHA_INV_OBSERVED_LOW)
        / ALPHA_INV_OBSERVED_LOW,
        pdg_ratio_predicted=pdg_predicted,
        exact_minus_pdg_ratio=predicted - pdg_predicted,
    )


def formula_statement() -> str:
    return (
        "alpha^-1 = 324*pi/h^3 + (2/(3*pi))*ln(((3h)^2)^3 "
        "*(m_tau/m_e)^5/(m_mu/m_e)), with h=2 and C3 exact ratios"
    )


def interpretation() -> list[str]:
    return [
        "The alpha candidate is scale-free: absolute lepton mass cancels.",
        "The TeV core scale is one equivalent reading, not the most compact formula.",
        "The formula uses only the h=2 bare boundary value and C3 charged-lepton ratios.",
        "The remaining 1.22 ppm is a matching-completion target, not a search for a new leading formula.",
    ]


def open_tasks() -> list[str]:
    return [
        "derive the h-dependent bare boundary term alpha_bare^-1=324*pi/h^3",
        "derive exact C3 mass ratios from the charged RefG action",
        "derive the threshold bridge and its full QED/EW/RefG completion",
        "derive the residual 1 ppm matching term without using observed alpha",
    ]


def run_gate() -> None:
    result = evaluate_closed_formula()

    assert math.isclose(
        result.alpha_inv_predicted,
        closed_alpha_formula(result.tau_over_e_ratio, result.muon_over_e_ratio),
        rel_tol=1.0e-15,
    )
    assert abs(result.miss_ppm) < 2.0
    assert abs(result.exact_minus_pdg_ratio) < 5.0e-5
    assert result.log_argument_ln > 40.0

    print("p18aw scale-free closed alpha formula gate")
    print("formula:")
    print(formula_statement())
    print()
    print(f"alpha_bare^-1 = {result.alpha_inv_bare:.12f}")
    print(f"m_tau/m_e exact C3 = {result.tau_over_e_ratio:.12f}")
    print(f"m_mu/m_e exact C3 = {result.muon_over_e_ratio:.12f}")
    print(f"ln argument = {result.log_argument_ln:.12f}")
    print(f"threshold shift = {result.threshold_shift:.12f}")
    print(f"alpha_pred^-1 = {result.alpha_inv_predicted:.12f}")
    print(f"alpha_obs^-1 = {result.alpha_inv_observed:.12f}")
    print(f"miss = {result.miss:.12f}")
    print(f"miss ppm = {result.miss_ppm:.6f}")
    print()
    print(f"PDG-ratio formula alpha^-1 = {result.pdg_ratio_predicted:.12f}")
    print(f"exact minus PDG-ratio formula = {result.exact_minus_pdg_ratio:.12f}")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_MATCHING_COMPLETION_REQUIRED__PASS_SCALE_FREE_CLOSED_ALPHA_FORMULA")


if __name__ == "__main__":
    run_gate()
