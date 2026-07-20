from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)

C3_ORDER = 3.0
H_BRANCH = 2.0
A_KOIDE = math.sqrt(2.0)
THETA_TOPOLOGICAL = 2.0 / 9.0

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}

LEPTON_MASS_SIGMA_MEV = {
    "electron": 0.00000000016,
    "muon": 0.0000023,
    "tau": 0.09,
}


@dataclass(frozen=True)
class C3Inversion:
    A: float
    theta: float
    A_delta_from_exact: float
    theta_delta_from_exact: float


@dataclass(frozen=True)
class SensitivityResult:
    exact_alpha_inv: float
    exact_residual: float
    d_alpha_inv_d_A: float
    d_alpha_inv_d_theta: float
    required_A_at_exact_theta: float
    required_A_delta_at_exact_theta: float
    required_theta_at_exact_A: float
    required_theta_delta_at_exact_A: float
    measured_A: float
    measured_theta: float
    measured_A_delta: float
    measured_theta_delta: float
    measured_alpha_inv: float
    measured_residual: float
    required_A_at_measured_theta: float
    required_A_delta_from_measured: float
    required_theta_at_measured_A: float
    required_theta_delta_from_measured: float
    A_sigma_linear: float
    theta_sigma_linear: float


def alpha_inv_bare_h2() -> float:
    return 324.0 * math.pi / (H_BRANCH**3)


def alpha_inv_from_c3(A: float, theta: float) -> float:
    tau, electron, muon = (
        1.0 + A * math.cos(theta + 2.0 * math.pi * k / 3.0)
        for k in range(3)
    )
    m_tau_over_e = (tau / electron) ** 2
    m_mu_over_e = (muon / electron) ** 2

    shift = QED_ONE_LOOP_B * (
        3.0 * math.log((C3_ORDER * H_BRANCH) ** 2 * m_tau_over_e)
        + 2.0 * math.log(m_tau_over_e / m_mu_over_e)
        + math.log(m_mu_over_e)
    )
    return alpha_inv_bare_h2() + shift


def invert_c3_from_masses(
    electron: float = LEPTON_MASSES_MEV["electron"],
    muon: float = LEPTON_MASSES_MEV["muon"],
    tau: float = LEPTON_MASSES_MEV["tau"],
) -> C3Inversion:
    triplet = (math.sqrt(tau), math.sqrt(electron), math.sqrt(muon))
    mean = sum(triplet) / 3.0
    c1 = sum(
        nu
        * complex(
            math.cos(-2.0 * math.pi * k / 3.0),
            math.sin(-2.0 * math.pi * k / 3.0),
        )
        for k, nu in enumerate(triplet)
    ) / 3.0
    A = 2.0 * abs(c1) / mean
    theta = math.atan2(c1.imag, c1.real)
    while theta > math.pi / 3.0:
        theta -= 2.0 * math.pi / 3.0
    while theta < -math.pi / 3.0:
        theta += 2.0 * math.pi / 3.0

    return C3Inversion(
        A=A,
        theta=theta,
        A_delta_from_exact=A - A_KOIDE,
        theta_delta_from_exact=theta - THETA_TOPOLOGICAL,
    )


def _root_for_A(theta: float, center: float) -> float:
    lo = center - 1.0e-4
    hi = center + 1.0e-4
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if (
            alpha_inv_from_c3(lo, theta) - ALPHA_INV_OBSERVED_LOW
        ) * (
            alpha_inv_from_c3(mid, theta) - ALPHA_INV_OBSERVED_LOW
        ) <= 0.0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def _root_for_theta(A: float, center: float) -> float:
    lo = center - 1.0e-4
    hi = center + 1.0e-4
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if (
            alpha_inv_from_c3(A, lo) - ALPHA_INV_OBSERVED_LOW
        ) * (
            alpha_inv_from_c3(A, mid) - ALPHA_INV_OBSERVED_LOW
        ) <= 0.0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def _linear_c3_parameter_sigmas() -> tuple[float, float]:
    contributions_A: list[float] = []
    contributions_theta: list[float] = []

    for name, sigma in LEPTON_MASS_SIGMA_MEV.items():
        plus = dict(LEPTON_MASSES_MEV)
        minus = dict(LEPTON_MASSES_MEV)
        plus[name] += sigma
        minus[name] -= sigma

        inv_plus = invert_c3_from_masses(
            plus["electron"], plus["muon"], plus["tau"]
        )
        inv_minus = invert_c3_from_masses(
            minus["electron"], minus["muon"], minus["tau"]
        )
        contributions_A.append((inv_plus.A - inv_minus.A) / 2.0)
        contributions_theta.append((inv_plus.theta - inv_minus.theta) / 2.0)

    sigma_A = math.sqrt(sum(x * x for x in contributions_A))
    sigma_theta = math.sqrt(sum(x * x for x in contributions_theta))
    return sigma_A, sigma_theta


def sensitivity_result() -> SensitivityResult:
    exact = alpha_inv_from_c3(A_KOIDE, THETA_TOPOLOGICAL)
    eps_A = 1.0e-6
    eps_theta = 1.0e-6
    dA = (
        alpha_inv_from_c3(A_KOIDE + eps_A, THETA_TOPOLOGICAL)
        - alpha_inv_from_c3(A_KOIDE - eps_A, THETA_TOPOLOGICAL)
    ) / (2.0 * eps_A)
    dtheta = (
        alpha_inv_from_c3(A_KOIDE, THETA_TOPOLOGICAL + eps_theta)
        - alpha_inv_from_c3(A_KOIDE, THETA_TOPOLOGICAL - eps_theta)
    ) / (2.0 * eps_theta)

    measured = invert_c3_from_masses()
    measured_alpha = alpha_inv_from_c3(measured.A, measured.theta)

    required_A_exact_theta = _root_for_A(THETA_TOPOLOGICAL, A_KOIDE)
    required_theta_exact_A = _root_for_theta(A_KOIDE, THETA_TOPOLOGICAL)
    required_A_measured_theta = _root_for_A(measured.theta, measured.A)
    required_theta_measured_A = _root_for_theta(measured.A, measured.theta)

    sigma_A, sigma_theta = _linear_c3_parameter_sigmas()

    return SensitivityResult(
        exact_alpha_inv=exact,
        exact_residual=exact - ALPHA_INV_OBSERVED_LOW,
        d_alpha_inv_d_A=dA,
        d_alpha_inv_d_theta=dtheta,
        required_A_at_exact_theta=required_A_exact_theta,
        required_A_delta_at_exact_theta=required_A_exact_theta - A_KOIDE,
        required_theta_at_exact_A=required_theta_exact_A,
        required_theta_delta_at_exact_A=required_theta_exact_A
        - THETA_TOPOLOGICAL,
        measured_A=measured.A,
        measured_theta=measured.theta,
        measured_A_delta=measured.A_delta_from_exact,
        measured_theta_delta=measured.theta_delta_from_exact,
        measured_alpha_inv=measured_alpha,
        measured_residual=measured_alpha - ALPHA_INV_OBSERVED_LOW,
        required_A_at_measured_theta=required_A_measured_theta,
        required_A_delta_from_measured=required_A_measured_theta - measured.A,
        required_theta_at_measured_A=required_theta_measured_A,
        required_theta_delta_from_measured=required_theta_measured_A
        - measured.theta,
        A_sigma_linear=sigma_A,
        theta_sigma_linear=sigma_theta,
    )


def interpretation() -> list[str]:
    return [
        "The exact-C3 residual can be removed by a sub-sigma shift in A or theta.",
        "The measured A shift already points in the alpha-correcting direction.",
        "The measured theta shift points in the opposite direction, so the two measured deviations partially cancel.",
        "The residual is therefore a tiny matching/scheme problem, not a failure of the C3/h=2 chain.",
        "A final derivation must explain which combination of C3 pole thresholds, running thresholds and boundary matching is physical.",
    ]


def open_tasks() -> list[str]:
    return [
        "derive whether exact C3 parameters or physical pole-threshold parameters enter the alpha bridge",
        "derive the residual C3-to-threshold dressing instead of fitting A or theta to alpha",
        "compute the completed QED/EW/RefG matching correction at the 1 ppm level",
        "keep alpha out of the parameter extraction until the final comparison step",
    ]


def run_gate() -> None:
    s = sensitivity_result()

    assert abs(s.exact_residual) < 2.0e-4
    assert abs(s.measured_residual) < 2.0e-4
    assert abs(s.required_A_delta_at_exact_theta / s.A_sigma_linear) < 1.0
    assert abs(s.required_theta_delta_at_exact_A / s.theta_sigma_linear) < 1.0
    assert s.measured_A_delta * s.required_A_delta_at_exact_theta > 0.0
    assert s.measured_theta_delta * s.required_theta_delta_at_exact_A < 0.0

    print("p18av C3 residual sensitivity gate")
    print(f"exact C3 alpha^-1 = {s.exact_alpha_inv:.12f}")
    print(f"exact residual = {s.exact_residual:.12f}")
    print(f"d(alpha^-1)/dA = {s.d_alpha_inv_d_A:.9f}")
    print(f"d(alpha^-1)/dtheta = {s.d_alpha_inv_d_theta:.9f}")
    print()
    print("required one-parameter shifts from exact C3")
    print(
        f"A required at theta=2/9 = {s.required_A_at_exact_theta:.12f}, "
        f"delta = {s.required_A_delta_at_exact_theta:.12e}, "
        f"sigma = {s.required_A_delta_at_exact_theta / s.A_sigma_linear:.6f}"
    )
    print(
        f"theta required at A=sqrt(2) = {s.required_theta_at_exact_A:.12f}, "
        f"delta = {s.required_theta_delta_at_exact_A:.12e}, "
        f"sigma = {s.required_theta_delta_at_exact_A / s.theta_sigma_linear:.6f}"
    )
    print()
    print("measured lepton C3 parameters")
    print(
        f"A_measured = {s.measured_A:.12f}, "
        f"delta = {s.measured_A_delta:.12e}, "
        f"sigma = {s.measured_A_delta / s.A_sigma_linear:.6f}"
    )
    print(
        f"theta_measured = {s.measured_theta:.12f}, "
        f"delta = {s.measured_theta_delta:.12e}, "
        f"sigma = {s.measured_theta_delta / s.theta_sigma_linear:.6f}"
    )
    print(f"measured-ratio alpha^-1 = {s.measured_alpha_inv:.12f}")
    print(f"measured residual = {s.measured_residual:.12f}")
    print()
    print("remaining one-parameter shifts from measured C3")
    print(
        f"A shift needed at measured theta = {s.required_A_delta_from_measured:.12e}, "
        f"sigma = {s.required_A_delta_from_measured / s.A_sigma_linear:.6f}"
    )
    print(
        f"theta shift needed at measured A = {s.required_theta_delta_from_measured:.12e}, "
        f"sigma = {s.required_theta_delta_from_measured / s.theta_sigma_linear:.6f}"
    )
    print()
    print("linear sigmas")
    print(f"A_sigma = {s.A_sigma_linear:.12e}")
    print(f"theta_sigma = {s.theta_sigma_linear:.12e}")
    print()
    print("interpretation")
    for item in interpretation():
        print(f"- {item}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_THRESHOLD_MATCHING_DERIVATION__PASS_C3_RESIDUAL_SENSITIVITY")


if __name__ == "__main__":
    run_gate()
