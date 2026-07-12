from __future__ import annotations

import math
from dataclasses import dataclass

from p18bl_target_free_alpha_kernel_gate import (
    PredictionRecord,
    predict_empirical_mass_branch,
    predict_exact_c3_branch,
    prediction_digest,
    source_firewall,
)


ALPHA_INV_REFERENCE = 137.035999177
ALPHA_INV_REFERENCE_SIGMA = 0.000000021


@dataclass(frozen=True)
class ObservationComparison:
    branch: str
    predicted_inverse_alpha: float
    reference_inverse_alpha: float
    difference: float
    difference_ppm: float
    reference_sigma: float
    mass_input_sigma: float | None
    combined_input_sigma: float
    difference_in_combined_input_sigma: float
    theory_systematic_sigma: float | None
    observational_pass_claimed: bool


def compare_with_reference(
    prediction: PredictionRecord,
    reference: float = ALPHA_INV_REFERENCE,
    reference_sigma: float = ALPHA_INV_REFERENCE_SIGMA,
) -> ObservationComparison:
    if reference <= 0.0 or reference_sigma <= 0.0:
        raise ValueError("reference and reference_sigma must be positive")
    difference = prediction.inverse_alpha - reference
    mass_sigma = prediction.mass_input_sigma_inverse_alpha
    combined = math.sqrt(reference_sigma**2 + (mass_sigma or 0.0) ** 2)
    return ObservationComparison(
        branch=prediction.branch,
        predicted_inverse_alpha=prediction.inverse_alpha,
        reference_inverse_alpha=reference,
        difference=difference,
        difference_ppm=1.0e6 * difference / reference,
        reference_sigma=reference_sigma,
        mass_input_sigma=mass_sigma,
        combined_input_sigma=combined,
        difference_in_combined_input_sigma=difference / combined,
        theory_systematic_sigma=prediction.theory_systematic_sigma,
        observational_pass_claimed=False,
    )


def observation_perturbation_firewall() -> dict[str, object]:
    exact = predict_exact_c3_branch()
    empirical = predict_empirical_mass_branch()
    exact_digest = prediction_digest(exact)
    empirical_digest = prediction_digest(empirical)

    references = (100.0, 137.0, 200.0)
    comparisons = tuple(
        (
            compare_with_reference(exact, value, 1.0e-6),
            compare_with_reference(empirical, value, 1.0e-6),
        )
        for value in references
    )

    return {
        "reference_values_tested": references,
        "exact_prediction_digest": exact_digest,
        "empirical_prediction_digest": empirical_digest,
        "exact_digest_unchanged": all(
            prediction_digest(exact) == exact_digest for _ in comparisons
        ),
        "empirical_digest_unchanged": all(
            prediction_digest(empirical) == empirical_digest
            for _ in comparisons
        ),
        "comparison_values_change": len(
            {pair[0].difference for pair in comparisons}
        )
        == len(references),
        "runtime_target_free": source_firewall()["runtime_target_free"],
        "historically_target_exposed": True,
        "retrospectively_blind": False,
    }


def interpretation() -> tuple[str, ...]:
    return (
        "The exact-C3 and empirical-pole-mass branches are distinct predictions and are never merged.",
        "The reference value is introduced only after each prediction record and digest already exist.",
        "The empirical branch carries a propagated pole-mass input uncertainty; its unquantified matching uncertainty remains open.",
        "Historical target exposure of h=2, N=34 and the readout-law search is retained in provenance, so this run is target-free but not retrospectively blind.",
        "No numerical closeness threshold is used as a gate-pass condition.",
    )


def run_gate() -> None:
    exact_prediction = predict_exact_c3_branch()
    empirical_prediction = predict_empirical_mass_branch()
    exact = compare_with_reference(exact_prediction)
    empirical = compare_with_reference(empirical_prediction)
    firewall = observation_perturbation_firewall()

    assert exact.predicted_inverse_alpha == exact_prediction.inverse_alpha
    assert empirical.predicted_inverse_alpha == empirical_prediction.inverse_alpha
    assert math.isclose(
        exact.difference,
        exact.predicted_inverse_alpha - exact.reference_inverse_alpha,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    assert math.isclose(
        empirical.difference,
        empirical.predicted_inverse_alpha - empirical.reference_inverse_alpha,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    assert exact.observational_pass_claimed is False
    assert empirical.observational_pass_claimed is False
    assert exact.theory_systematic_sigma is None
    assert empirical.theory_systematic_sigma is None
    assert firewall["exact_digest_unchanged"]
    assert firewall["empirical_digest_unchanged"]
    assert firewall["comparison_values_change"]
    assert firewall["runtime_target_free"]
    assert firewall["historically_target_exposed"]
    assert firewall["retrospectively_blind"] is False

    print("p18bm alpha observation comparison gate")
    print("exact-C3 comparison")
    print(exact)
    print()
    print("empirical-mass comparison")
    print(empirical)
    print()
    print("observation perturbation firewall")
    print(firewall)
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print(
        "STATUS: OPEN_ACTION_DERIVATION_AND_INDEPENDENT_VALIDATION__"
        "PASS_RUNTIME_TARGET_FIREWALL_AND_COMPARISON_LEDGER"
    )


if __name__ == "__main__":
    run_gate()
