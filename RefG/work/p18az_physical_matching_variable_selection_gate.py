from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_INV_EXACT_C3 = 137.03616654750616
ALPHA_INV_PDG_RATIO = 137.0361358108052

CORE_SCALE_EXACT_C3_TEV = 222.45901084608514
QED_B1_THREE_LEPTONS = 2.0 / math.pi


@dataclass(frozen=True)
class MatchingTranslation:
    delta_alpha_inv: float
    charge_ratio: float
    maxwell_stiffness_ratio: float
    equal_factor_ratio: float
    core_scale_ratio: float
    core_scale_shift_percent: float


@dataclass(frozen=True)
class VariableScore:
    variable: str
    preserves_topology: bool
    preserves_exact_c3_block: bool
    existing_open_slot: bool
    localized_to_final_readout: bool
    does_not_redefine_bare_alpha: bool
    score: int
    verdict: str


def translate_residual(alpha_inv_candidate: float) -> MatchingTranslation:
    alpha_candidate = 1.0 / alpha_inv_candidate
    alpha_observed = 1.0 / ALPHA_INV_OBSERVED_LOW

    delta_inv = ALPHA_INV_OBSERVED_LOW - alpha_inv_candidate
    alpha_ratio = alpha_observed / alpha_candidate

    charge_ratio = math.sqrt(alpha_ratio)
    stiffness_ratio = alpha_candidate / alpha_observed
    equal_factor_ratio = alpha_ratio**0.25

    log_core_shift = delta_inv / QED_B1_THREE_LEPTONS
    core_ratio = math.exp(log_core_shift)

    return MatchingTranslation(
        delta_alpha_inv=delta_inv,
        charge_ratio=charge_ratio,
        maxwell_stiffness_ratio=stiffness_ratio,
        equal_factor_ratio=equal_factor_ratio,
        core_scale_ratio=core_ratio,
        core_scale_shift_percent=100.0 * (core_ratio - 1.0),
    )


def _score(
    variable: str,
    preserves_topology: bool,
    preserves_exact_c3_block: bool,
    existing_open_slot: bool,
    localized_to_final_readout: bool,
    does_not_redefine_bare_alpha: bool,
    verdict: str,
) -> VariableScore:
    flags = (
        preserves_topology,
        preserves_exact_c3_block,
        existing_open_slot,
        localized_to_final_readout,
        does_not_redefine_bare_alpha,
    )
    return VariableScore(
        variable=variable,
        preserves_topology=preserves_topology,
        preserves_exact_c3_block=preserves_exact_c3_block,
        existing_open_slot=existing_open_slot,
        localized_to_final_readout=localized_to_final_readout,
        does_not_redefine_bare_alpha=does_not_redefine_bare_alpha,
        score=sum(1 for flag in flags if flag),
        verdict=verdict,
    )


def variable_selection_table() -> tuple[VariableScore, ...]:
    return (
        _score(
            "topological_h_or_q_geom",
            preserves_topology=False,
            preserves_exact_c3_block=True,
            existing_open_slot=False,
            localized_to_final_readout=False,
            does_not_redefine_bare_alpha=False,
            verdict=(
                "reject as residual carrier: h and q_geom are the discrete "
                "branch skeleton, not a ppm matching dial"
            ),
        ),
        _score(
            "bare_q0_or_h2_boundary_level",
            preserves_topology=False,
            preserves_exact_c3_block=True,
            existing_open_slot=True,
            localized_to_final_readout=False,
            does_not_redefine_bare_alpha=False,
            verdict=(
                "avoid for final residual: q0=sqrt(2) is part of the bare "
                "h=2 candidate; shifting it would blur the leading theorem"
            ),
        ),
        _score(
            "exact_C3_A_theta_ratios",
            preserves_topology=True,
            preserves_exact_c3_block=False,
            existing_open_slot=True,
            localized_to_final_readout=False,
            does_not_redefine_bare_alpha=True,
            verdict=(
                "avoid as a fit variable: C3 deviations are diagnostics of "
                "threshold/pole dressing, not alpha knobs"
            ),
        ),
        _score(
            "core_scale_shift",
            preserves_topology=True,
            preserves_exact_c3_block=True,
            existing_open_slot=True,
            localized_to_final_readout=True,
            does_not_redefine_bare_alpha=True,
            verdict=(
                "acceptable representation: a -0.026 percent scale shift is "
                "equivalent to the residual, but the scale-free formula shows "
                "this is not the most primitive variable"
            ),
        ),
        _score(
            "ordinary_QED_EW_threshold_scheme",
            preserves_topology=True,
            preserves_exact_c3_block=True,
            existing_open_slot=True,
            localized_to_final_readout=True,
            does_not_redefine_bare_alpha=True,
            verdict=(
                "primary external completion: pole thresholds, running masses "
                "and EW/U1 matching naturally live at the final bridge"
            ),
        ),
        _score(
            "RefG_boundary_to_Maxwell_readout_normalization",
            preserves_topology=True,
            preserves_exact_c3_block=True,
            existing_open_slot=True,
            localized_to_final_readout=True,
            does_not_redefine_bare_alpha=True,
            verdict=(
                "primary internal completion: p18z/p18aa leave exactly this "
                "normalization slot, K_F/k_J or boundary-to-Maxwell matching"
            ),
        ),
        _score(
            "equal_readout_factor_f",
            preserves_topology=True,
            preserves_exact_c3_block=True,
            existing_open_slot=True,
            localized_to_final_readout=True,
            does_not_redefine_bare_alpha=True,
            verdict=(
                "useful phenomenological language: f needs only a 0.305 ppm "
                "shift, but the action must say whether this is K_F, k_J, or "
                "threshold matching"
            ),
        ),
    )


def selected_bucket() -> dict[str, object]:
    table = variable_selection_table()
    primary = [
        row
        for row in table
        if row.variable
        in (
            "ordinary_QED_EW_threshold_scheme",
            "RefG_boundary_to_Maxwell_readout_normalization",
        )
    ]
    protected = [
        "h=2 branch",
        "q_geom=2/9",
        "q0^2=h bare boundary rule",
        "exact C3 A=sqrt(2), theta=2/9 leading block",
        "scale-free closed alpha formula",
    ]
    return {
        "primary_bucket": "finite external/internal matching layer",
        "primary_variables": tuple(row.variable for row in primary),
        "protected_leading_objects": tuple(protected),
        "selection_rule": (
            "do not absorb ppm residual into quantized topology or exact C3 "
            "leading data; absorb it only in a derived final matching map"
        ),
    }


def next_theorem_requirements() -> list[str]:
    return [
        "derive the boundary-to-Maxwell finite normalization from the charged h=2 core action",
        "derive the threshold convention that maps exact C3 ratios to physical lepton pole/running thresholds",
        "derive the EW/U1 matching status of the 222 TeV scale",
        "combine those terms into one finite counterterm without using observed alpha",
        "verify the completed formula lands on alpha(0) rather than only alpha at an intermediate scheme scale",
    ]


def run_gate() -> None:
    exact = translate_residual(ALPHA_INV_EXACT_C3)
    pdg = translate_residual(ALPHA_INV_PDG_RATIO)
    table = variable_selection_table()
    bucket = selected_bucket()

    best_score = max(row.score for row in table)
    best_variables = [row.variable for row in table if row.score == best_score]

    assert exact.delta_alpha_inv < 0.0
    assert pdg.delta_alpha_inv < 0.0
    assert "RefG_boundary_to_Maxwell_readout_normalization" in best_variables
    assert "ordinary_QED_EW_threshold_scheme" in best_variables
    assert all(
        row.score < best_score
        for row in table
        if row.variable in ("topological_h_or_q_geom", "bare_q0_or_h2_boundary_level")
    )

    print("p18az physical matching variable selection gate")
    print("exact-C3 residual translation:")
    print(exact)
    print()
    print("PDG-ratio residual translation:")
    print(pdg)
    print()
    print("selection table")
    for row in table:
        print(f"- {row}")
    print()
    print("selected bucket")
    print(bucket)
    print()
    print("next theorem requirements")
    for item in next_theorem_requirements():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_FINITE_MATCHING_THEOREM_REQUIRED__PASS_PHYSICAL_VARIABLE_SELECTION")


if __name__ == "__main__":
    run_gate()
