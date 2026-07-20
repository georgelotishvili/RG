from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_OBSERVED_LOW = 1.0 / ALPHA_INV_OBSERVED_LOW

Q_GEOM_H2 = 2.0 / 9.0
Q0_H2_INTEGER_BRANCH = math.sqrt(2.0)


@dataclass(frozen=True)
class TwoFactorReadout:
    observed_alpha: float
    observed_alpha_inv: float
    observed_total_transfer: float
    observed_equal_subfactor: float
    h2_bare_alpha: float
    h2_bare_alpha_inv: float
    h2_bare_total_transfer: float
    h2_bare_equal_subfactor: float
    alpha_dressing_ratio: float
    amplitude_dressing_ratio: float
    subfactor_dressing_ratio: float
    q0_required_observed: float
    q0_h2_bare: float


def factorize(alpha: float = ALPHA_OBSERVED_LOW) -> TwoFactorReadout:
    """Factorize alpha as a quadratic EM readout.

    Convention:
        alpha = T_EM^2
        T_EM = C_link * C_size

    If the two operational effects are the same local medium factor, then
        C_link = C_size = alpha^(1/4).

    This file does not claim the equality theorem. It only records the target
    and compares it to the existing h=2 integer branch.
    """

    observed_total = math.sqrt(alpha)
    observed_subfactor = math.sqrt(observed_total)

    h2_total = (Q0_H2_INTEGER_BRANCH * Q_GEOM_H2) / math.sqrt(4.0 * math.pi)
    h2_alpha = h2_total * h2_total
    h2_subfactor = math.sqrt(h2_total)

    alpha_dressing = alpha / h2_alpha
    amplitude_dressing = math.sqrt(alpha_dressing)
    subfactor_dressing = math.sqrt(amplitude_dressing)

    q0_required = math.sqrt(4.0 * math.pi * alpha) / Q_GEOM_H2

    return TwoFactorReadout(
        observed_alpha=alpha,
        observed_alpha_inv=1.0 / alpha,
        observed_total_transfer=observed_total,
        observed_equal_subfactor=observed_subfactor,
        h2_bare_alpha=h2_alpha,
        h2_bare_alpha_inv=1.0 / h2_alpha,
        h2_bare_total_transfer=h2_total,
        h2_bare_equal_subfactor=h2_subfactor,
        alpha_dressing_ratio=alpha_dressing,
        amplitude_dressing_ratio=amplitude_dressing,
        subfactor_dressing_ratio=subfactor_dressing,
        q0_required_observed=q0_required,
        q0_h2_bare=Q0_H2_INTEGER_BRANCH,
    )


def obstruction_statement() -> list[str]:
    return [
        "The product C_link*C_size is fixed by alpha, but the two factors are not fixed separately.",
        "A symmetry/equality theorem C_link=C_size would close the split and give alpha^(1/4).",
        "The h=2 branch already gives the bare transfer T=(sqrt(2)*2/9)/sqrt(4*pi).",
        "The remaining observed-vs-bare difference is small per subfactor, so the next problem is a dressing theorem, not a new fit.",
    ]


def next_gate_requirements() -> list[str]:
    return [
        "derive C_link from inter-node transfer in the charged oscillon core",
        "derive C_size from operational size/readout of the same core",
        "prove or reject C_link=C_size from local Maxwell/luminal consistency",
        "derive the subfactor dressing ratio from the foundation readout instead of inserting CODATA",
    ]


def run_gate() -> None:
    r = factorize()

    assert math.isclose(r.observed_total_transfer**2, r.observed_alpha, rel_tol=1e-14)
    assert math.isclose(r.observed_equal_subfactor**4, r.observed_alpha, rel_tol=1e-14)
    assert math.isclose(r.h2_bare_total_transfer**2, r.h2_bare_alpha, rel_tol=1e-14)
    assert math.isclose(r.h2_bare_equal_subfactor**4, r.h2_bare_alpha, rel_tol=1e-14)
    assert math.isclose(r.h2_bare_alpha * r.alpha_dressing_ratio, r.observed_alpha, rel_tol=1e-14)

    # The useful discovery of this parametrization: the missing correction is
    # not a factor of 137. It is a few percent in alpha, and below two percent
    # per equal subfactor.
    assert 0.92 < r.alpha_dressing_ratio < 0.94
    assert 0.96 < r.amplitude_dressing_ratio < 0.97
    assert 0.98 < r.subfactor_dressing_ratio < 0.99

    print("p18am two-factor EM readout factorization gate")
    print(f"observed alpha^-1 = {r.observed_alpha_inv:.9f}")
    print(f"observed T_EM = sqrt(alpha) = {r.observed_total_transfer:.12f}")
    print(f"observed equal subfactor = alpha^(1/4) = {r.observed_equal_subfactor:.12f}")
    print()
    print("h=2 bare branch")
    print(f"q_geom = {Q_GEOM_H2:.12f}")
    print(f"q0_h2 = {r.q0_h2_bare:.12f}")
    print(f"h=2 bare alpha^-1 = {r.h2_bare_alpha_inv:.9f}")
    print(f"h=2 bare T_EM = {r.h2_bare_total_transfer:.12f}")
    print(f"h=2 bare equal subfactor = {r.h2_bare_equal_subfactor:.12f}")
    print()
    print("observed-to-bare dressing ratios")
    print(f"alpha dressing ratio = {r.alpha_dressing_ratio:.12f}")
    print(f"amplitude dressing ratio = {r.amplitude_dressing_ratio:.12f}")
    print(f"equal-subfactor dressing ratio = {r.subfactor_dressing_ratio:.12f}")
    print(f"q0 required by observed alpha = {r.q0_required_observed:.12f}")
    print()
    print("obstruction")
    for item in obstruction_statement():
        print(f"- {item}")
    print()
    print("next gate requirements")
    for item in next_gate_requirements():
        print(f"- {item}")
    print()
    print("STATUS: OPEN_EQUAL_SUBFACTOR_AND_DRESSING_THEOREM_REQUIRED__PASS_TWO_FACTOR_REDUCTION")


if __name__ == "__main__":
    run_gate()
