from __future__ import annotations

import math
from dataclasses import dataclass

from p18bb_internal_external_em_readout_split_gate import (
    ALPHA_INV_OBSERVED_LOW,
    THETA_TOPOLOGICAL,
    alpha_inv_from_c3,
    c3_distortion_guard,
    required_em_readout_split,
)
from p18bc_em_readout_deficit_factor_gate import (
    em_readout_deficit_translation,
)


@dataclass(frozen=True)
class AlphaRoute:
    label: str
    alpha_inv: float | None
    miss_vs_observed: float | None
    miss_ppm: float | None
    uses_observed_alpha_as_input: bool
    preserves_c3_lepton_map: bool
    route_status: str


def _miss(alpha_inv: float) -> tuple[float, float]:
    miss = alpha_inv - ALPHA_INV_OBSERVED_LOW
    ppm = 1.0e6 * miss / ALPHA_INV_OBSERVED_LOW
    return miss, ppm


def route_table() -> tuple[AlphaRoute, ...]:
    q_geom = THETA_TOPOLOGICAL
    direct_unit_impedance = 1.0 / (q_geom**2 / (4.0 * math.pi))
    direct_miss, direct_ppm = _miss(direct_unit_impedance)

    internal = alpha_inv_from_c3()
    internal_miss, internal_ppm = _miss(internal)

    split = required_em_readout_split()
    corrected_miss, corrected_ppm = _miss(split.corrected_alpha_inv)

    exact, theta_fit, a_fit, readout_corrected = c3_distortion_guard()

    return (
        AlphaRoute(
            label="old_direct_q_geom_with_unit_impedance",
            alpha_inv=direct_unit_impedance,
            miss_vs_observed=direct_miss,
            miss_ppm=direct_ppm,
            uses_observed_alpha_as_input=False,
            preserves_c3_lepton_map=True,
            route_status=(
                "REJECT_AS_LEADING_ROUTE: q_geom=2/9 with unit impedance lands "
                "near 254, not 137"
            ),
        ),
        AlphaRoute(
            label="old_eta_core_or_impedance_target",
            alpha_inv=None,
            miss_vs_observed=None,
            miss_ppm=None,
            uses_observed_alpha_as_input=True,
            preserves_c3_lepton_map=True,
            route_status=(
                "TARGET_ONLY: eta_core translated the observed alpha into a "
                "needed partition; it was never a derivation"
            ),
        ),
        AlphaRoute(
            label="new_h2_C3_lepton_threshold_internal_readout",
            alpha_inv=internal,
            miss_vs_observed=internal_miss,
            miss_ppm=internal_ppm,
            uses_observed_alpha_as_input=False,
            preserves_c3_lepton_map=True,
            route_status=(
                "PRIMARY_LEADING_ROUTE: h=2 boundary plus exact C3 lepton "
                "thresholds lands within about 1.22 ppm"
            ),
        ),
        AlphaRoute(
            label="fit_alpha_by_changing_C3_theta",
            alpha_inv=theta_fit.alpha_inv,
            miss_vs_observed=theta_fit.alpha_miss,
            miss_ppm=1.0e6 * theta_fit.alpha_miss / ALPHA_INV_OBSERVED_LOW,
            uses_observed_alpha_as_input=True,
            preserves_c3_lepton_map=False,
            route_status=(
                "REJECT: fits alpha by moving theta, but p18bb shows it "
                "damages the independent lepton mass map"
            ),
        ),
        AlphaRoute(
            label="fit_alpha_by_changing_C3_A",
            alpha_inv=a_fit.alpha_inv,
            miss_vs_observed=a_fit.alpha_miss,
            miss_ppm=1.0e6 * a_fit.alpha_miss / ALPHA_INV_OBSERVED_LOW,
            uses_observed_alpha_as_input=True,
            preserves_c3_lepton_map=False,
            route_status=(
                "REJECT: fits alpha by moving A, but p18bb shows it damages "
                "the independent lepton mass map"
            ),
        ),
        AlphaRoute(
            label="new_h2_C3_plus_internal_external_EM_readout",
            alpha_inv=split.corrected_alpha_inv,
            miss_vs_observed=corrected_miss,
            miss_ppm=corrected_ppm,
            uses_observed_alpha_as_input=True,
            preserves_c3_lepton_map=True,
            route_status=(
                "CONDITIONAL_COMPLETION: exact if q_EM is supplied; final "
                "theorem must derive q_EM without alpha"
            ),
        ),
    )


def consolidation_statement() -> dict[str, object]:
    deficit = em_readout_deficit_translation()
    return {
        "leading_formula": (
            "alpha_inv_internal = 324*pi/h^3 + (2/(3*pi))*ln(((3h)^2)^3 "
            "*(m_tau/m_e)^5/(m_mu/m_e)), h=2, exact C3 ratios"
        ),
        "new_final_object": "q_EM",
        "readout_identity": "alpha_inv_observed = alpha_inv_internal - (2/pi)*q_EM",
        "q_EM_target_for_future_derivation": deficit.q_em_deficit,
        "eta_core_status": (
            "old eta_core/impedance files remain useful as boundary-to-Maxwell "
            "normalization audits, but not as the leading alpha-number search"
        ),
        "protected_objects": (
            "h=2 branch",
            "q_geom=2/9 register",
            "C3 A=sqrt(2)",
            "C3 theta=2/9",
            "charged-lepton mass map",
        ),
        "next_real_theorem": (
            "derive q_EM from the charged h=2 core's internal inventory to "
            "external Maxwell readout map"
        ),
    }


def run_gate() -> None:
    rows = route_table()
    direct, eta_target, internal, theta_fit, a_fit, corrected = rows

    assert direct.alpha_inv is not None
    assert internal.alpha_inv is not None
    assert corrected.alpha_inv is not None
    assert direct.alpha_inv > 200.0
    assert abs(internal.miss_ppm or 0.0) < 2.0
    assert abs(corrected.miss_vs_observed or 0.0) < 1.0e-12
    assert eta_target.uses_observed_alpha_as_input
    assert not theta_fit.preserves_c3_lepton_map
    assert not a_fit.preserves_c3_lepton_map

    print("p18bd alpha route consolidation gate")
    print("routes")
    for row in rows:
        print(f"- {row}")
    print()
    print("consolidation")
    print(consolidation_statement())
    print()
    print("STATUS: OPEN_Q_EM_MICROPHYSICS_REQUIRED__PASS_ALPHA_ROUTE_CONSOLIDATION")


if __name__ == "__main__":
    run_gate()
