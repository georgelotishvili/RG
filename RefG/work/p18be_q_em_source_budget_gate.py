from __future__ import annotations

import math
from dataclasses import dataclass

from p18ax_next_order_matching_guard_gate import next_order_guard
from p18bb_internal_external_em_readout_split_gate import (
    ALPHA_INV_OBSERVED_LOW,
    QED_B1_THREE_LEPTONS,
    alpha_inv_from_c3,
)
from p18at_exact_c3_ratio_alpha_candidate_gate import (
    PDG_MASSES_MEV,
    alpha_inv_from_mass_ratios,
)


@dataclass(frozen=True)
class QEMBudget:
    exact_c3_alpha_inv: float
    pdg_threshold_alpha_inv: float
    observed_alpha_inv: float
    q_total_exact_c3_to_observed: float
    q_c3_to_pdg_thresholds: float
    q_pdg_to_observed_readout: float
    threshold_fraction_of_total: float
    boundary_fraction_of_total: float
    eta_total: float
    eta_c3_to_pdg_thresholds: float
    eta_pdg_to_observed_readout: float
    eta_product: float
    naive_next_order_q_equivalent: float
    naive_next_order_abs_over_total: float


@dataclass(frozen=True)
class SourceVerdict:
    source: str
    q_value: float | None
    independent_of_observed_alpha: bool
    sign_correct: bool | None
    size_reasonable: bool | None
    verdict: str


def q_needed_from_alpha_candidate(alpha_inv_candidate: float) -> float:
    """q in alpha_obs = alpha_candidate - (2/pi)*q."""

    return (alpha_inv_candidate - ALPHA_INV_OBSERVED_LOW) / QED_B1_THREE_LEPTONS


def pdg_threshold_alpha_inv() -> float:
    tau_over_e = PDG_MASSES_MEV["tau"] / PDG_MASSES_MEV["electron"]
    muon_over_e = PDG_MASSES_MEV["muon"] / PDG_MASSES_MEV["electron"]
    return alpha_inv_from_mass_ratios(tau_over_e, muon_over_e)


def q_em_source_budget() -> QEMBudget:
    exact = alpha_inv_from_c3()
    pdg = pdg_threshold_alpha_inv()

    q_total = q_needed_from_alpha_candidate(exact)
    q_pdg = q_needed_from_alpha_candidate(pdg)
    q_threshold = q_total - q_pdg

    eta_total = math.exp(-q_total)
    eta_threshold = math.exp(-q_threshold)
    eta_boundary = math.exp(-q_pdg)

    # A schematic positive next-order beta shift moves alpha^-1 upward.  In
    # readout-filter language that is a negative q, so it has the wrong sign
    # for the residual.
    next_guard = next_order_guard()
    q_next = -next_guard.schematic_next_order_shift / QED_B1_THREE_LEPTONS

    return QEMBudget(
        exact_c3_alpha_inv=exact,
        pdg_threshold_alpha_inv=pdg,
        observed_alpha_inv=ALPHA_INV_OBSERVED_LOW,
        q_total_exact_c3_to_observed=q_total,
        q_c3_to_pdg_thresholds=q_threshold,
        q_pdg_to_observed_readout=q_pdg,
        threshold_fraction_of_total=q_threshold / q_total,
        boundary_fraction_of_total=q_pdg / q_total,
        eta_total=eta_total,
        eta_c3_to_pdg_thresholds=eta_threshold,
        eta_pdg_to_observed_readout=eta_boundary,
        eta_product=eta_threshold * eta_boundary,
        naive_next_order_q_equivalent=q_next,
        naive_next_order_abs_over_total=abs(q_next / q_total),
    )


def source_verdicts() -> tuple[SourceVerdict, ...]:
    b = q_em_source_budget()
    return (
        SourceVerdict(
            source="exact_C3_to_physical_pole_threshold_shift",
            q_value=b.q_c3_to_pdg_thresholds,
            independent_of_observed_alpha=True,
            sign_correct=True,
            size_reasonable=True,
            verdict=(
                "VALID_PARTIAL_SOURCE: physical lepton thresholds explain "
                "about 18 percent of q_EM without touching alpha"
            ),
        ),
        SourceVerdict(
            source="remaining_boundary_to_Maxwell_readout",
            q_value=b.q_pdg_to_observed_readout,
            independent_of_observed_alpha=False,
            sign_correct=True,
            size_reasonable=True,
            verdict=(
                "PRIMARY_OPEN_SOURCE: about 82 percent remains; derive this "
                "from the charged h=2 core readout map"
            ),
        ),
        SourceVerdict(
            source="naive_positive_next_order_QED_beta_term",
            q_value=b.naive_next_order_q_equivalent,
            independent_of_observed_alpha=True,
            sign_correct=False,
            size_reasonable=False,
            verdict=(
                "REJECT_AS_STANDALONE_SOURCE: wrong sign and far too large; "
                "only a completed matching theorem may use higher-order pieces"
            ),
        ),
        SourceVerdict(
            source="change_C3_parameters_to_fit_alpha",
            q_value=None,
            independent_of_observed_alpha=False,
            sign_correct=None,
            size_reasonable=None,
            verdict=(
                "REJECT: this consumes the lepton map and is already guarded "
                "against by p18bb"
            ),
        ),
    )


def next_step_contract() -> dict[str, object]:
    return {
        "decomposition": "q_EM = q_threshold + q_boundary",
        "q_threshold_status": (
            "computable from exact C3 ratios versus physical lepton pole "
            "thresholds; this is a partial source"
        ),
        "q_boundary_status": (
            "still open; must come from RefG boundary-to-Maxwell readout or "
            "from a fully specified QED/EW matching convention"
        ),
        "do_not_do": (
            "do not tune C3, do not add a naive two-loop term, and do not "
            "declare q_boundary derived just because its target value is known"
        ),
        "next_gate": (
            "derive or constrain q_boundary from a finite charged-core "
            "readout functional"
        ),
    }


def run_gate() -> None:
    budget = q_em_source_budget()
    verdicts = source_verdicts()

    assert math.isclose(
        budget.q_total_exact_c3_to_observed,
        budget.q_c3_to_pdg_thresholds + budget.q_pdg_to_observed_readout,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    assert math.isclose(
        budget.eta_total,
        budget.eta_product,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    assert 0.10 < budget.threshold_fraction_of_total < 0.25
    assert 0.75 < budget.boundary_fraction_of_total < 0.90
    assert budget.naive_next_order_q_equivalent < 0.0
    assert budget.naive_next_order_abs_over_total > 30.0

    print("p18be q_EM source budget gate")
    print("budget")
    print(budget)
    print()
    print("source verdicts")
    for row in verdicts:
        print(f"- {row}")
    print()
    print("next step contract")
    print(next_step_contract())
    print()
    print("STATUS: OPEN_Q_BOUNDARY_DERIVATION_REQUIRED__PASS_Q_EM_SOURCE_BUDGET")


if __name__ == "__main__":
    run_gate()
