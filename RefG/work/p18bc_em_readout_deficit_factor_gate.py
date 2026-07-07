from __future__ import annotations

import math
from dataclasses import dataclass

from p15f_universal_proper_readout_bridge_gate import (
    universal_proper_readout_bridge_status,
)
from p18bb_internal_external_em_readout_split_gate import (
    ALPHA_INV_OBSERVED_LOW,
    QED_B1_THREE_LEPTONS,
    alpha_inv_from_c3,
    c3_distortion_guard,
    required_em_readout_split,
)


@dataclass(frozen=True)
class EMReadoutDeficit:
    alpha_inv_internal: float
    alpha_inv_observed: float
    alpha_inv_residual: float
    core_readout_filter: float
    q_em_deficit: float
    alpha_inv_shift_from_q_em: float
    balanced_length_filter: float
    balanced_volume_filter: float
    two_channel_equal_factor: float
    hidden_external_gap_fraction: float
    q_em_ppm: float
    core_gap_ppm: float


@dataclass(frozen=True)
class CarrierVerdict:
    carrier: str
    uses_observed_alpha_as_input: bool
    preserves_h2_branch: bool
    preserves_exact_c3_lepton_map: bool
    has_existing_refg_slot: bool
    final_status: str


def em_readout_deficit_translation() -> EMReadoutDeficit:
    """Translate the p18bb residual into the p15-style readout filter.

    This is a target translation, not a derivation.  The important object is

        eta_EM = exp(-q_EM),

    which is exactly the same mathematical type as the p15 external readout
    filters.  The future theorem must derive q_EM without using alpha.
    """

    split = required_em_readout_split()
    q_em = -math.log(split.core_external_over_internal)
    shift_from_q = -QED_B1_THREE_LEPTONS * q_em

    # Balanced isotropic p15 language: if the external energy/core readout is
    # carried as a volume-like filter, eta_core = eta_L^3.
    length_filter = math.exp(-q_em / 3.0)

    return EMReadoutDeficit(
        alpha_inv_internal=split.alpha_inv_internal_readout_identification,
        alpha_inv_observed=split.alpha_inv_observed,
        alpha_inv_residual=split.residual_observed_minus_internal,
        core_readout_filter=split.core_external_over_internal,
        q_em_deficit=q_em,
        alpha_inv_shift_from_q_em=shift_from_q,
        balanced_length_filter=length_filter,
        balanced_volume_filter=length_filter**3,
        two_channel_equal_factor=split.frequency_external_over_internal,
        hidden_external_gap_fraction=1.0 - split.core_external_over_internal,
        q_em_ppm=1.0e6 * q_em,
        core_gap_ppm=1.0e6 * (1.0 - split.core_external_over_internal),
    )


def carrier_table() -> tuple[CarrierVerdict, ...]:
    return (
        CarrierVerdict(
            carrier="change_h_or_topological_charge",
            uses_observed_alpha_as_input=False,
            preserves_h2_branch=False,
            preserves_exact_c3_lepton_map=True,
            has_existing_refg_slot=False,
            final_status="REJECT: this would move the discrete skeleton, not the ppm readout layer",
        ),
        CarrierVerdict(
            carrier="change_exact_C3_A_or_theta",
            uses_observed_alpha_as_input=True,
            preserves_h2_branch=True,
            preserves_exact_c3_lepton_map=False,
            has_existing_refg_slot=False,
            final_status="REJECT: p18bb shows this can fit alpha only by damaging the lepton map",
        ),
        CarrierVerdict(
            carrier="ordinary_QED_EW_threshold_matching",
            uses_observed_alpha_as_input=False,
            preserves_h2_branch=True,
            preserves_exact_c3_lepton_map=True,
            has_existing_refg_slot=True,
            final_status="OPEN: allowed, but p18ba says non-leptonic matching must be handled explicitly",
        ),
        CarrierVerdict(
            carrier="RefG_boundary_to_Maxwell_normalization",
            uses_observed_alpha_as_input=False,
            preserves_h2_branch=True,
            preserves_exact_c3_lepton_map=True,
            has_existing_refg_slot=True,
            final_status="PRIMARY: derive the EM readout filter from the charged h=2 core action",
        ),
        CarrierVerdict(
            carrier="p15_style_internal_external_readout_filter",
            uses_observed_alpha_as_input=False,
            preserves_h2_branch=True,
            preserves_exact_c3_lepton_map=True,
            has_existing_refg_slot=True,
            final_status="PRIMARY LANGUAGE: eta_EM=exp(-q_EM) is the correct ledger form",
        ),
    )


def derivation_contract() -> dict[str, object]:
    return {
        "object_to_derive": "q_EM in eta_EM=exp(-q_EM)",
        "must_not_use": (
            "observed alpha, changed C3 angle, changed h branch, or fitted "
            "Maxwell stiffness"
        ),
        "acceptable_inputs": (
            "charged h=2 core action, boundary-to-Maxwell projection, finite "
            "core profile, exact C3 charged-lepton register, and independently "
            "specified QED/EW threshold convention"
        ),
        "required_identity_after_derivation": (
            "alpha_inv = alpha_inv_internal - (2/pi)*q_EM"
        ),
        "falsification": (
            "if the derived q_EM has the wrong sign, is order-one, or requires "
            "moving C3/h=2, then this alpha completion fails"
        ),
    }


def interpretation() -> list[str]:
    return [
        "The residual is naturally written as a tiny external-readout deficit q_EM.",
        "This is the same algebraic kind of split already used in p15: internal inventory and external readout are separate ledgers.",
        "The number is small: the external EM core readout is lower than the internal core scale by about 263 ppm.",
        "This does not derive alpha yet; it isolates the exact object that must be derived.",
        "The C3 lepton map stays protected, so the next theorem should target q_EM, not the C3 block.",
    ]


def run_gate() -> None:
    p15f = universal_proper_readout_bridge_status()
    deficit = em_readout_deficit_translation()
    carriers = carrier_table()
    tests = c3_distortion_guard()
    exact, theta_fit, a_fit, readout_corrected = tests

    corrected = alpha_inv_from_c3(core_readout_factor=deficit.core_readout_filter)

    assert (
        p15f["status"]
        == "PASS_UNIVERSAL_PROPER_READOUT_BRIDGE_LEDGER__ACTION_DYNAMICS_OPEN"
    )
    assert math.isclose(corrected, ALPHA_INV_OBSERVED_LOW, rel_tol=1.0e-14)
    assert math.isclose(
        deficit.alpha_inv_shift_from_q_em,
        deficit.alpha_inv_residual,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    assert math.isclose(
        deficit.balanced_volume_filter,
        deficit.core_readout_filter,
        rel_tol=1.0e-15,
    )
    assert 0.0 < deficit.q_em_deficit < 1.0e-3
    assert theta_fit.relative_mass_error_sum > 5.0 * exact.relative_mass_error_sum
    assert a_fit.relative_mass_error_sum > 5.0 * exact.relative_mass_error_sum
    assert math.isclose(
        readout_corrected.relative_mass_error_sum,
        exact.relative_mass_error_sum,
        rel_tol=0.0,
        abs_tol=1.0e-18,
    )

    print("p18bc EM readout deficit factor gate")
    print("p15f status:", p15f["status"])
    print()
    print("EM readout deficit translation:")
    print(deficit)
    print()
    print("carrier table")
    for row in carriers:
        print(f"- {row}")
    print()
    print("derivation contract")
    print(derivation_contract())
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_Q_EM_DERIVATION_REQUIRED__PASS_EM_READOUT_DEFICIT_FACTOR_LEDGER")


if __name__ == "__main__":
    run_gate()
