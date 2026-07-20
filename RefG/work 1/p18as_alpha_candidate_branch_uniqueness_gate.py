from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)

C3_ORDER = 3.0

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}


@dataclass(frozen=True)
class BranchRow:
    h: int
    alpha_inv_bare: float
    core_scale_tev: float
    alpha_inv_predicted: float
    miss: float


@dataclass(frozen=True)
class PairScanRow:
    h: int
    numerator: str
    denominator: str
    core_scale_tev: float
    alpha_inv_bare: float
    alpha_inv_predicted: float
    miss: float
    abs_miss: float


def bare_alpha_inv_for_h(h: int) -> float:
    """Coherent branch rule from q_geom=h/9 and q0^2=h.

    alpha_bare = q0^2*q_geom^2/(4*pi) = h*(h/9)^2/(4*pi)
    alpha_bare^-1 = 324*pi/h^3.
    """

    return 324.0 * math.pi / float(h**3)


def threshold_shift(mu_core_mev: float) -> float:
    if mu_core_mev <= max(LEPTON_MASSES_MEV.values()):
        raise ValueError("mu_core must be above the tau threshold for this ledger")
    return QED_ONE_LOOP_B * sum(
        math.log(mu_core_mev / mass) for mass in LEPTON_MASSES_MEV.values()
    )


def c3_h_core_scale(h: int, numerator: str = "tau", denominator: str = "electron") -> float:
    """mu_core=(3h)^2*m_numerator^2/m_denominator."""

    return (
        (C3_ORDER * float(h)) ** 2
        * LEPTON_MASSES_MEV[numerator] ** 2
        / LEPTON_MASSES_MEV[denominator]
    )


def coherent_h_branch_scan(h_max: int = 5) -> list[BranchRow]:
    rows: list[BranchRow] = []
    for h in range(1, h_max + 1):
        core = c3_h_core_scale(h)
        ainv = bare_alpha_inv_for_h(h) + threshold_shift(core)
        rows.append(
            BranchRow(
                h=h,
                alpha_inv_bare=bare_alpha_inv_for_h(h),
                core_scale_tev=core / 1.0e6,
                alpha_inv_predicted=ainv,
                miss=ainv - ALPHA_INV_OBSERVED_LOW,
            )
        )
    return rows


def restricted_pair_scan(h_max: int = 5) -> list[PairScanRow]:
    """Restricted look-elsewhere audit.

    The allowed form is kept narrow:
        mu_core=(3h)^2*m_i^2/m_j,
        alpha_bare^-1=324*pi/h^3,
        h=1..h_max,
        i,j in charged leptons,
        mu_core above tau threshold.

    This does not prove uniqueness in all possible numerology. It checks the
    actual structural family used by the candidate.
    """

    rows: list[PairScanRow] = []
    names = tuple(LEPTON_MASSES_MEV)
    for h in range(1, h_max + 1):
        bare = bare_alpha_inv_for_h(h)
        for numerator in names:
            for denominator in names:
                core = c3_h_core_scale(h, numerator, denominator)
                if core <= LEPTON_MASSES_MEV["tau"]:
                    continue
                predicted = bare + threshold_shift(core)
                miss = predicted - ALPHA_INV_OBSERVED_LOW
                rows.append(
                    PairScanRow(
                        h=h,
                        numerator=numerator,
                        denominator=denominator,
                        core_scale_tev=core / 1.0e6,
                        alpha_inv_bare=bare,
                        alpha_inv_predicted=predicted,
                        miss=miss,
                        abs_miss=abs(miss),
                    )
                )
    return sorted(rows, key=lambda row: row.abs_miss)


def branch_uniqueness_summary() -> dict[str, object]:
    h_rows = coherent_h_branch_scan()
    pair_rows = restricted_pair_scan()
    best = pair_rows[0]
    second = pair_rows[1]

    return {
        "best_candidate": best,
        "second_best_candidate": second,
        "best_is_h2_tau_over_electron": (
            best.h == 2
            and best.numerator == "tau"
            and best.denominator == "electron"
        ),
        "second_best_abs_miss": second.abs_miss,
        "nearest_wrong_branch_gap": second.abs_miss / best.abs_miss,
        "h_branch_rows": h_rows,
        "top_pair_rows": pair_rows[:8],
    }


def interpretation() -> list[str]:
    return [
        "Within the coherent h-branch rule, h=2 is the only small branch that lands near alpha.",
        "Within the restricted C3/h lepton-pair family, tau^2/electron at h=2 is the unique near hit.",
        "The nearest wrong candidate is off by more than three inverse-alpha units, while the h=2 tau/e candidate misses by about 1.37e-4.",
        "This does not prove the formula from the action; it makes the candidate sharply non-generic inside the actual structural family.",
    ]


def next_tasks() -> list[str]:
    return [
        "derive the h-dependent bare rule q_geom=h/9 and q0^2=h inside one boundary action",
        "derive why the tau/electron second-extrapolation core scale is selected",
        "derive the charged-lepton thresholds internally rather than using PDG inputs",
        "replace the lepton-only threshold bridge by the completed RefG/QED/EW matching calculation",
    ]


def run_gate() -> None:
    summary = branch_uniqueness_summary()
    best: PairScanRow = summary["best_candidate"]  # type: ignore[assignment]
    second: PairScanRow = summary["second_best_candidate"]  # type: ignore[assignment]

    assert summary["best_is_h2_tau_over_electron"] is True
    assert abs(best.miss) < 2.0e-4
    assert second.abs_miss > 3.0
    assert summary["nearest_wrong_branch_gap"] > 10000.0

    print("p18as alpha candidate branch-uniqueness gate")
    print("coherent h-branch scan: mu_core=(3h)^2*m_tau^2/m_e and alpha_bare^-1=324*pi/h^3")
    for row in summary["h_branch_rows"]:  # type: ignore[index]
        print(
            f"- h={row.h}: bare={row.alpha_inv_bare:.9f}, "
            f"mu={row.core_scale_tev:.9f} TeV, "
            f"alpha^-1={row.alpha_inv_predicted:.12f}, miss={row.miss:.12f}"
        )
    print()
    print("restricted pair scan top rows")
    for row in summary["top_pair_rows"]:  # type: ignore[index]
        print(
            f"- h={row.h}, {row.numerator}^2/{row.denominator}: "
            f"mu={row.core_scale_tev:.9f} TeV, "
            f"alpha^-1={row.alpha_inv_predicted:.12f}, miss={row.miss:.12f}"
        )
    print()
    print("best candidate")
    print(best)
    print("second best candidate")
    print(second)
    print(f"nearest wrong branch gap = {summary['nearest_wrong_branch_gap']:.3f}x")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("next tasks")
    for item in next_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_ACTION_DERIVATION_REQUIRED__PASS_RESTRICTED_BRANCH_UNIQUENESS_AUDIT")


if __name__ == "__main__":
    run_gate()
