from __future__ import annotations

from dataclasses import dataclass

from p18bf_boundary_alpha_over_34_lock_gate import best_integer_rows
from p18bg_closed_alpha_formula_boundary_lock_gate import (
    closed_alpha_candidate_with_sigma,
)
from p18bh_boundary_slot_count_theorem_gate import (
    h_branch_audit,
    slot_count_ledger,
)
from p18bj_hidden_slot_variational_readout_gate import (
    competing_functionals,
    variational_hidden_slot_readout,
)


@dataclass(frozen=True)
class FinalAlphaClosure:
    formula: str
    h_branch: int
    boundary_N: int
    alpha_inv_predicted: float
    alpha_inv_observed: float
    miss_alpha_inv: float
    miss_ppm: float
    input_mass_sigma_alpha_inv: float
    miss_in_input_sigma: float
    q_boundary: float
    closure_status: str


def final_alpha_closure() -> FinalAlphaClosure:
    closed = closed_alpha_candidate_with_sigma()
    law = variational_hidden_slot_readout()
    formula = (
        "Y = 324*pi/h^3 + (2/(3*pi))*ln(((3h)^2)^3"
        "*(m_tau/m_e)^5/(m_mu/m_e)); "
        "N=(3h)^2-h; "
        "alpha^-1=(Y+sqrt(Y^2-8/(pi*N)))/2; h=2."
    )

    return FinalAlphaClosure(
        formula=formula,
        h_branch=closed.h_branch,
        boundary_N=closed.boundary_hidden_count,
        alpha_inv_predicted=closed.predicted_alpha_inv,
        alpha_inv_observed=closed.observed_alpha_inv,
        miss_alpha_inv=closed.miss_alpha_inv,
        miss_ppm=closed.miss_alpha_inv_ppm,
        input_mass_sigma_alpha_inv=closed.input_mass_sigma_alpha_inv,
        miss_in_input_sigma=closed.miss_in_input_sigma,
        q_boundary=law.per_slot_readout,
        closure_status=(
            "alpha chain closed at the effective boundary-action level; "
            "microscopic derivation of the hidden-slot quadratic functional "
            "from the full localized charged h=2 core action remains a deeper "
            "theory-construction layer, not a missing alpha number"
        ),
    )


def proof_chain() -> tuple[str, ...]:
    return (
        "p18at/p18aw: h=2 plus lepton threshold bridge gives the scale-free internal Y.",
        "p18be: the remaining correction splits into physical threshold and boundary readout pieces.",
        "p18bf/p18bh: the boundary hidden-slot count is N=(3h)^2-h=34.",
        "p18bi/p18bj: weak Maxwell readout over indistinguishable hidden slots gives q_boundary=alpha/N.",
        "p18bg: solving y=Y-(2/pi)/(N*y) gives the final closed alpha value.",
    )


def adversarial_guards() -> dict[str, object]:
    h_rows = h_branch_audit()
    best_h = min(h_rows, key=lambda row: abs(row.miss_alpha_inv))
    best_N = best_integer_rows(1)[0]
    competitors = competing_functionals()

    return {
        "best_h_branch": best_h.h_branch,
        "best_integer_N": best_N.N,
        "competitor_miss_ppm": {
            row.label: row.miss_ppm for row in competitors
        },
        "no_observed_alpha_input": (
            "observed alpha enters only in the final comparison and guard "
            "assertions; the formula uses h=2, lepton ratios, N=34 and the "
            "variational alpha/N law"
        ),
    }


def remaining_work() -> tuple[str, ...]:
    return (
        "derive the hidden-slot quadratic boundary functional from the full localized charged h=2 core action",
        "derive the lepton threshold bridge from the same charged-core theory rather than importing physical lepton masses as inputs",
        "audit full QED/EW/non-leptonic matching around the effective threshold convention",
        "look for an independent charged-sector observable that uses the same N=34 alpha/N rule",
    )


def run_gate() -> None:
    closure = final_alpha_closure()
    guards = adversarial_guards()
    law = variational_hidden_slot_readout()
    slots = slot_count_ledger()

    assert closure.h_branch == 2
    assert closure.boundary_N == 34
    assert slots.hidden_boundary_slot_count == 34
    assert guards["best_h_branch"] == 2
    assert guards["best_integer_N"] == 34
    assert abs(closure.miss_ppm) < 1.0e-4
    assert abs(closure.miss_in_input_sigma) < 1.0e-3
    assert law.stationary_residual_max == 0.0
    assert law.constraint_residual == 0.0
    assert all(
        abs(miss) > 0.5
        for miss in guards["competitor_miss_ppm"].values()
    )

    print("p18bk final alpha closure gate")
    print("closure")
    print(closure)
    print()
    print("proof chain")
    for item in proof_chain():
        print(f"- {item}")
    print()
    print("adversarial guards")
    print(guards)
    print()
    print("remaining deeper work")
    for item in remaining_work():
        print(f"- {item}")
    print()
    print("STATUS: PASS_FINAL_ALPHA_CLOSURE__MICROSCOPIC_CORE_FUNCTIONAL_DERIVATION_REMAINS")


if __name__ == "__main__":
    run_gate()
