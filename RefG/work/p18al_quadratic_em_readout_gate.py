from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_CODATA_LOW = 137.035999177
ALPHA_LOW = 1.0 / ALPHA_INV_CODATA_LOW

Q_GEOM_H2 = 2.0 / 9.0
Q0_H2_INTEGER_BRANCH = math.sqrt(2.0)


@dataclass(frozen=True)
class QuadraticReadout:
    alpha: float
    alpha_inv: float
    total_amplitude_transfer: float
    inverse_total_amplitude_transfer: float
    equal_connection_factor: float
    inverse_equal_connection_factor: float
    equal_size_factor: float
    inverse_equal_size_factor: float
    canonical_charge_e: float


@dataclass(frozen=True)
class H2RegisterComparison:
    q_geom: float
    q0_required_from_observed_alpha: float
    q0_h2_integer_branch: float
    q0_relative_gap: float
    alpha_inv_h2_bare: float
    total_amplitude_h2_bare: float
    amplitude_relative_gap: float


def quadratic_readout_from_alpha(alpha: float = ALPHA_LOW) -> QuadraticReadout:
    """Audit the interpretation alpha = T_EM^2.

    T_EM is the amplitude-level transfer from the localized charged oscillon
    register into the externally read Maxwell channel. If the same transfer is
    itself the product of two equal operational effects,

        T_EM = connection_factor * size_factor,

    then alpha = factor^4.
    """

    total_amplitude_transfer = math.sqrt(alpha)
    equal_factor = math.sqrt(total_amplitude_transfer)
    canonical_charge_e = math.sqrt(4.0 * math.pi * alpha)

    return QuadraticReadout(
        alpha=alpha,
        alpha_inv=1.0 / alpha,
        total_amplitude_transfer=total_amplitude_transfer,
        inverse_total_amplitude_transfer=1.0 / total_amplitude_transfer,
        equal_connection_factor=equal_factor,
        inverse_equal_connection_factor=1.0 / equal_factor,
        equal_size_factor=equal_factor,
        inverse_equal_size_factor=1.0 / equal_factor,
        canonical_charge_e=canonical_charge_e,
    )


def h2_register_comparison(alpha: float = ALPHA_LOW) -> H2RegisterComparison:
    """Compare the two-factor readout target to the existing h=2 branch.

    Earlier gates isolated q_geom = 2/9 and the integer-action candidate
    q0 = sqrt(2). That branch gives alpha_bare^-1 = 81*pi/2. This is not the
    observed low-energy value, but it is close enough to be a meaningful bare
    target if a later dressing theorem supplies the remaining shift.
    """

    canonical_e = math.sqrt(4.0 * math.pi * alpha)
    q0_required = canonical_e / Q_GEOM_H2
    q0_gap = (Q0_H2_INTEGER_BRANCH - q0_required) / q0_required

    alpha_h2_bare = (Q0_H2_INTEGER_BRANCH * Q_GEOM_H2) ** 2 / (4.0 * math.pi)
    alpha_inv_h2_bare = 1.0 / alpha_h2_bare

    amp_observed = math.sqrt(alpha)
    amp_h2_bare = math.sqrt(alpha_h2_bare)
    amp_gap = (amp_h2_bare - amp_observed) / amp_observed

    return H2RegisterComparison(
        q_geom=Q_GEOM_H2,
        q0_required_from_observed_alpha=q0_required,
        q0_h2_integer_branch=Q0_H2_INTEGER_BRANCH,
        q0_relative_gap=q0_gap,
        alpha_inv_h2_bare=alpha_inv_h2_bare,
        total_amplitude_h2_bare=amp_h2_bare,
        amplitude_relative_gap=amp_gap,
    )


def theorem_requirements() -> list[str]:
    return [
        "derive an amplitude-level foundation-to-EM transfer T_EM, not alpha directly",
        "show that the EM strength readout is quadratic: alpha = T_EM^2",
        "derive whether T_EM splits into connection_factor * size_factor",
        "if the split is symmetric, derive factor = alpha^(1/4) instead of fitting it",
        "connect the h=2 register q_geom=2/9 to the same transfer convention",
        "derive or reject the remaining bare-to-low-energy dressing gap",
    ]


def run_gate() -> None:
    q = quadratic_readout_from_alpha()
    h2 = h2_register_comparison()

    assert math.isclose(q.alpha * q.alpha_inv, 1.0, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(q.total_amplitude_transfer**2, q.alpha, rel_tol=1e-14)
    assert math.isclose(q.equal_connection_factor * q.equal_size_factor, q.total_amplitude_transfer, rel_tol=1e-14)
    assert math.isclose(q.equal_connection_factor**4, q.alpha, rel_tol=1e-14)

    assert h2.q0_required_from_observed_alpha > 0.0
    assert h2.q0_h2_integer_branch > h2.q0_required_from_observed_alpha
    assert 0.03 < h2.q0_relative_gap < 0.05
    assert 126.0 < h2.alpha_inv_h2_bare < 128.0

    print("p18al quadratic EM readout gate")
    print(f"observed alpha^-1 = {q.alpha_inv:.9f}")
    print(f"alpha = {q.alpha:.12f}")
    print(f"total amplitude transfer sqrt(alpha) = {q.total_amplitude_transfer:.12f}")
    print(f"inverse total amplitude transfer = {q.inverse_total_amplitude_transfer:.9f}")
    print(f"equal two-factor subreadout alpha^(1/4) = {q.equal_connection_factor:.12f}")
    print(f"inverse equal subreadout = {q.inverse_equal_connection_factor:.9f}")
    print(f"canonical charge e = sqrt(4*pi*alpha) = {q.canonical_charge_e:.12f}")
    print()
    print("h=2 register comparison")
    print(f"q_geom = {h2.q_geom:.12f}")
    print(f"q0 required from observed alpha = {h2.q0_required_from_observed_alpha:.12f}")
    print(f"q0 h=2 integer branch = {h2.q0_h2_integer_branch:.12f}")
    print(f"q0 relative gap = {100.0 * h2.q0_relative_gap:.6f}%")
    print(f"h=2 bare alpha^-1 = {h2.alpha_inv_h2_bare:.9f}")
    print(f"h=2 bare total amplitude = {h2.total_amplitude_h2_bare:.12f}")
    print(f"amplitude relative gap = {100.0 * h2.amplitude_relative_gap:.6f}%")
    print()
    print("requirements")
    for item in theorem_requirements():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_TWO_FACTOR_EM_READOUT_THEOREM_REQUIRED__PASS_QUADRATIC_EM_READOUT_REFRAMING")


if __name__ == "__main__":
    run_gate()
