from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)

C3_ORDER = 3.0
H_BRANCH = 2.0
A_KOIDE = math.sqrt(2.0)
THETA_TOPOLOGICAL = 2.0 / 9.0

PDG_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}


@dataclass(frozen=True)
class ExactC3AlphaCandidate:
    nu_tau_over_nu_e: float
    nu_mu_over_nu_e: float
    mass_tau_over_e: float
    mass_mu_over_e: float
    alpha_inv_bare_h2: float
    threshold_shift: float
    alpha_inv_predicted: float
    alpha_inv_observed: float
    alpha_inv_miss: float
    alpha_inv_miss_ppm: float
    electron_anchor_core_scale_tev: float
    pdg_ratio_alpha_inv: float
    exact_minus_pdg_ratio_alpha_inv: float


def c3_frequencies(a: float = A_KOIDE, theta: float = THETA_TOPOLOGICAL) -> tuple[float, float, float]:
    """Return the C3 frequency triplet in the p11 order: tau, electron, muon."""

    tau = 1.0 + a * math.cos(theta)
    electron = 1.0 + a * math.cos(theta + 2.0 * math.pi / 3.0)
    muon = 1.0 + a * math.cos(theta + 4.0 * math.pi / 3.0)
    return tau, electron, muon


def alpha_inv_bare_for_h(h: float = H_BRANCH) -> float:
    # q_geom=h/9 and q0^2=h give alpha_bare^-1=324*pi/h^3.
    return 324.0 * math.pi / (h**3)


def alpha_inv_from_mass_ratios(m_tau_over_e: float, m_mu_over_e: float, h: float = H_BRANCH) -> float:
    """Absolute mass scale cancels from the candidate alpha formula.

    Starting from:
        mu_core = (3h)^2*m_tau^2/m_e
        Delta alpha^-1 = B[3 ln(mu_core/m_tau)
                           +2 ln(m_tau/m_mu)
                           +  ln(m_mu/m_e)]

    one obtains:
        Delta alpha^-1 = B[3 ln((3h)^2*m_tau/m_e)
                           +2 ln((m_tau/m_e)/(m_mu/m_e))
                           +  ln(m_mu/m_e)].
    """

    threshold_shift = QED_ONE_LOOP_B * (
        3.0 * math.log((C3_ORDER * h) ** 2 * m_tau_over_e)
        + 2.0 * math.log(m_tau_over_e / m_mu_over_e)
        + math.log(m_mu_over_e)
    )
    return alpha_inv_bare_for_h(h) + threshold_shift


def exact_c3_alpha_candidate() -> ExactC3AlphaCandidate:
    nu_tau, nu_e, nu_mu = c3_frequencies()

    r_tau = nu_tau / nu_e
    r_mu = nu_mu / nu_e
    mass_tau_over_e = r_tau**2
    mass_mu_over_e = r_mu**2

    predicted = alpha_inv_from_mass_ratios(mass_tau_over_e, mass_mu_over_e)

    pdg_m_tau_over_e = PDG_MASSES_MEV["tau"] / PDG_MASSES_MEV["electron"]
    pdg_m_mu_over_e = PDG_MASSES_MEV["muon"] / PDG_MASSES_MEV["electron"]
    pdg_ratio_predicted = alpha_inv_from_mass_ratios(pdg_m_tau_over_e, pdg_m_mu_over_e)

    electron_anchor_core = (
        (C3_ORDER * H_BRANCH) ** 2
        * (PDG_MASSES_MEV["electron"] * mass_tau_over_e) ** 2
        / PDG_MASSES_MEV["electron"]
    )

    return ExactC3AlphaCandidate(
        nu_tau_over_nu_e=r_tau,
        nu_mu_over_nu_e=r_mu,
        mass_tau_over_e=mass_tau_over_e,
        mass_mu_over_e=mass_mu_over_e,
        alpha_inv_bare_h2=alpha_inv_bare_for_h(),
        threshold_shift=predicted - alpha_inv_bare_for_h(),
        alpha_inv_predicted=predicted,
        alpha_inv_observed=ALPHA_INV_OBSERVED_LOW,
        alpha_inv_miss=predicted - ALPHA_INV_OBSERVED_LOW,
        alpha_inv_miss_ppm=1.0e6 * (predicted - ALPHA_INV_OBSERVED_LOW) / ALPHA_INV_OBSERVED_LOW,
        electron_anchor_core_scale_tev=electron_anchor_core / 1.0e6,
        pdg_ratio_alpha_inv=pdg_ratio_predicted,
        exact_minus_pdg_ratio_alpha_inv=predicted - pdg_ratio_predicted,
    )


def scale_cancellation_audit() -> dict[str, float | bool]:
    """Check that alpha does not depend on the absolute electron anchor."""

    candidate = exact_c3_alpha_candidate()
    predicted = candidate.alpha_inv_predicted

    # Build fake absolute mass scales from the same exact C3 ratios.
    anchors = (0.001, 0.51099895069, 1000.0, 1.0e9)
    values = []
    for me in anchors:
        mtau = me * candidate.mass_tau_over_e
        mmu = me * candidate.mass_mu_over_e
        mu_core = (C3_ORDER * H_BRANCH) ** 2 * mtau * mtau / me
        shift = QED_ONE_LOOP_B * (
            3.0 * math.log(mu_core / mtau)
            + 2.0 * math.log(mtau / mmu)
            + math.log(mmu / me)
        )
        values.append(alpha_inv_bare_for_h() + shift)

    max_spread = max(values) - min(values)
    return {
        "anchor_count": float(len(anchors)),
        "first_value": values[0],
        "last_value": values[-1],
        "max_spread": max_spread,
        "scale_cancels": max_spread < 1.0e-12 and abs(values[0] - predicted) < 1.0e-12,
    }


def interpretation() -> list[str]:
    return [
        "The alpha candidate can be written using only exact C3 mass ratios, not an absolute electron mass.",
        "The electron mass is needed only if the same formula is expressed as a TeV core scale.",
        "With exact A=sqrt(2) and theta=2/9, the candidate gives alpha^-1 within about 1.22 ppm.",
        "With measured PDG ratios, the same formula gives the earlier about 1 ppm result.",
        "Thus the alpha route is now tied to the C3 ratio theorem and the h=2 branch, not to an arbitrary mass-scale fit.",
    ]


def open_tasks() -> list[str]:
    return [
        "derive A=sqrt(2), theta=2/9 and m~nu^2 from the RefG charged-core action",
        "derive the h=2 bare rule alpha_bare^-1=81*pi/2 from the same boundary action",
        "derive the C3/h core extrapolation mu_core=(3h)^2*m_tau^2/m_e",
        "replace the lepton-only threshold bridge by the completed RefG/QED/EW bridge",
    ]


def run_gate() -> None:
    c = exact_c3_alpha_candidate()
    scale = scale_cancellation_audit()

    assert scale["scale_cancels"] is True
    assert abs(c.alpha_inv_miss_ppm) < 2.0
    assert 200.0 < c.electron_anchor_core_scale_tev < 250.0
    assert abs(c.exact_minus_pdg_ratio_alpha_inv) < 5.0e-5

    print("p18at exact-C3 ratio alpha candidate gate")
    print(f"nu_tau/nu_e = {c.nu_tau_over_nu_e:.12f}")
    print(f"nu_mu/nu_e = {c.nu_mu_over_nu_e:.12f}")
    print(f"m_tau/m_e from exact C3 = {c.mass_tau_over_e:.12f}")
    print(f"m_mu/m_e from exact C3 = {c.mass_mu_over_e:.12f}")
    print()
    print(f"alpha_bare^-1 h=2 = {c.alpha_inv_bare_h2:.12f}")
    print(f"threshold shift from exact C3 ratios = {c.threshold_shift:.12f}")
    print(f"predicted alpha^-1 = {c.alpha_inv_predicted:.12f}")
    print(f"observed alpha^-1 = {c.alpha_inv_observed:.12f}")
    print(f"miss = {c.alpha_inv_miss:.12f}")
    print(f"miss ppm = {c.alpha_inv_miss_ppm:.6f}")
    print()
    print(f"electron-anchored core scale = {c.electron_anchor_core_scale_tev:.9f} TeV")
    print(f"PDG-ratio version alpha^-1 = {c.pdg_ratio_alpha_inv:.12f}")
    print(f"exact C3 minus PDG-ratio version = {c.exact_minus_pdg_ratio_alpha_inv:.12f}")
    print()
    print("scale cancellation audit")
    print(scale)
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_C3_ACTION_DERIVATION_AND_EW_COMPLETION__PASS_SCALE_FREE_ALPHA_CANDIDATE")


if __name__ == "__main__":
    run_gate()
