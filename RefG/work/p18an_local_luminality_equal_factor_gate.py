from __future__ import annotations

import math
from dataclasses import dataclass


ALPHA_INV_OBSERVED_LOW = 137.035999177
ALPHA_OBSERVED_LOW = 1.0 / ALPHA_INV_OBSERVED_LOW

Q_GEOM_H2 = 2.0 / 9.0
Q0_H2_INTEGER_BRANCH = math.sqrt(2.0)


@dataclass(frozen=True)
class EqualFactorConsequence:
    observed_factor: float
    observed_factor_inv: float
    observed_alpha_inv: float
    h2_bare_factor: float
    h2_bare_factor_inv: float
    h2_bare_alpha_inv: float
    per_factor_dressing: float
    per_factor_dressing_percent: float


def local_luminality_condition(link_factor: float, size_factor: float) -> float:
    """Minimal local-cone audit.

    link_factor measures the transfer capacity of the foundation connection.
    size_factor measures the operational spacing/readout scale built from the
    same foundation modes.

    In this stripped model the local signal speed is their ratio. If local
    Maxwell propagation remains luminal for observers built from the same
    foundation, this ratio must be one, so link_factor=size_factor.
    """

    if size_factor <= 0.0:
        raise ValueError("size_factor must be positive")
    return link_factor / size_factor


def alpha_from_equal_factor(factor: float) -> float:
    """If T_EM = link*size and link=size=f, then alpha = f^4."""

    return factor**4


def consequence(alpha: float = ALPHA_OBSERVED_LOW) -> EqualFactorConsequence:
    observed_factor = alpha ** 0.25

    h2_total_transfer = (Q0_H2_INTEGER_BRANCH * Q_GEOM_H2) / math.sqrt(4.0 * math.pi)
    h2_bare_alpha = h2_total_transfer**2
    h2_bare_factor = h2_bare_alpha ** 0.25

    per_factor_dressing = observed_factor / h2_bare_factor

    return EqualFactorConsequence(
        observed_factor=observed_factor,
        observed_factor_inv=1.0 / observed_factor,
        observed_alpha_inv=1.0 / alpha,
        h2_bare_factor=h2_bare_factor,
        h2_bare_factor_inv=1.0 / h2_bare_factor,
        h2_bare_alpha_inv=1.0 / h2_bare_alpha,
        per_factor_dressing=per_factor_dressing,
        per_factor_dressing_percent=(per_factor_dressing - 1.0) * 100.0,
    )


def theorem_status() -> list[str]:
    return [
        "conditional theorem: local luminality in foundation-built units sets link_factor=size_factor",
        "then the EM strength appears as alpha=factor^4, not as a primitive 1/137 input",
        "h=2 gives a bare factor within about two percent of the observed factor",
        "the remaining task is to derive the per-factor dressing from the charged core/environment readout",
    ]


def run_gate() -> None:
    c = consequence()

    assert math.isclose(local_luminality_condition(c.observed_factor, c.observed_factor), 1.0, rel_tol=1e-14)
    assert math.isclose(alpha_from_equal_factor(c.observed_factor), ALPHA_OBSERVED_LOW, rel_tol=1e-14)
    assert math.isclose(alpha_from_equal_factor(c.h2_bare_factor), 1.0 / c.h2_bare_alpha_inv, rel_tol=1e-14)
    assert 0.98 < c.per_factor_dressing < 0.99

    print("p18an local luminality equal-factor gate")
    print(f"observed alpha^-1 = {c.observed_alpha_inv:.9f}")
    print(f"observed equal factor f = alpha^(1/4) = {c.observed_factor:.12f}")
    print(f"observed equal factor inverse = {c.observed_factor_inv:.9f}")
    print()
    print("h=2 bare equal-factor target")
    print(f"h=2 bare alpha^-1 = {c.h2_bare_alpha_inv:.9f}")
    print(f"h=2 bare equal factor = {c.h2_bare_factor:.12f}")
    print(f"h=2 bare equal factor inverse = {c.h2_bare_factor_inv:.9f}")
    print()
    print("per-factor dressing")
    print(f"observed/h2 factor ratio = {c.per_factor_dressing:.12f}")
    print(f"per-factor shift = {c.per_factor_dressing_percent:.6f}%")
    print()
    print("status")
    for item in theorem_status():
        print(f"- {item}")
    print()
    print("STATUS: CONDITIONAL_EQUAL_FACTOR_THEOREM__OPEN_PER_FACTOR_DRESSING_DERIVATION")


if __name__ == "__main__":
    run_gate()
