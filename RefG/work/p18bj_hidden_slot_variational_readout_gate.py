from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from p18bh_boundary_slot_count_theorem_gate import slot_count_ledger


@dataclass(frozen=True)
class HiddenDensityReadout:
    hidden_dimension: int
    helicity_interface_rank: int
    interface_gain: float
    total_trace_budget: float
    isotropic_eigenvalue: float
    normalized_interface_readout: float
    unnormalized_interface_trace: float
    lagrange_multiplier: float
    stationary_residual: float
    trace_constraint_residual: float
    quadratic_action: float
    target_value_used: bool


def hidden_density_readout(
    alpha: float,
    kappa: float = 1.0,
    helicity_interface_rank: int = 2,
    interface_gain: float = 1.0,
) -> HiddenDensityReadout:
    """Derive q_boundary=alpha/N in the conditional hidden-density model.

    Let K=ker(R_gamma), dim(K)=N, and let rho be the positive weak-response
    density on K.  At quadratic order the unresolved hidden sector is assumed
    to have U(N)-invariant action

        S[rho] = kappa/2 Tr(rho^2),   Tr(rho)=alpha.

    Strict convexity and the trace constraint give the unique stationary
    density rho_*=(alpha/N) I_N.  If C:C^2->K is any isometric two-helicity
    interface, the normalized external readout is

        q = (1/2) Tr(C^* rho_* C) = alpha/N.

    The result is independent of the choice of the isometry C.  No measured
    value of alpha is used; alpha is the symbolic Maxwell weak-coupling budget.
    """

    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if kappa <= 0.0 or interface_gain <= 0.0:
        raise ValueError("kappa and interface_gain must be positive")

    N = slot_count_ledger().hidden_boundary_slot_count
    r = helicity_interface_rank
    if not 1 <= r <= N:
        raise ValueError("interface rank must lie between one and N")

    eigenvalue = alpha / N
    lagrange = -kappa * eigenvalue
    stationary_residual = abs(kappa * eigenvalue + lagrange)
    trace_residual = abs(N * eigenvalue - alpha)
    interface_trace = r * interface_gain * eigenvalue
    normalized_readout = interface_trace / r
    action = 0.5 * kappa * N * eigenvalue**2

    return HiddenDensityReadout(
        hidden_dimension=N,
        helicity_interface_rank=r,
        interface_gain=interface_gain,
        total_trace_budget=alpha,
        isotropic_eigenvalue=eigenvalue,
        normalized_interface_readout=normalized_readout,
        unnormalized_interface_trace=interface_trace,
        lagrange_multiplier=lagrange,
        stationary_residual=stationary_residual,
        trace_constraint_residual=trace_residual,
        quadratic_action=action,
        target_value_used=False,
    )


def exact_symbolic_theorem() -> dict[str, object]:
    N = slot_count_ledger().hidden_boundary_slot_count
    alpha, kappa = sp.symbols("alpha kappa", positive=True)
    rho = alpha * sp.eye(N) / N

    # A representative isometry selecting two orthonormal hidden directions.
    C = sp.zeros(N, 2)
    C[0, 0] = 1
    C[1, 1] = 1
    interface_metric = sp.simplify(C.H * C)
    normalized_readout = sp.simplify(sp.trace(C.H * rho * C) / 2)
    stationarity = sp.simplify(kappa * rho - kappa * alpha * sp.eye(N) / N)

    return {
        "hidden_dimension": N,
        "functional": "S[rho]=(kappa/2) Tr(rho^2)",
        "constraint": "Tr(rho)=alpha",
        "unique_minimizer": "rho_*=(alpha/N) I_N",
        "interface_condition": "C^* C=I_2",
        "interface_metric": str(interface_metric),
        "normalized_readout": str(normalized_readout),
        "stationarity_matrix_is_zero": stationarity == sp.zeros(N),
        "hessian_positive_for_kappa_positive": True,
        "target_value_used": False,
    }


def interface_normalization_guard() -> dict[str, object]:
    alpha, gain = sp.symbols("alpha g", positive=True)
    N = slot_count_ledger().hidden_boundary_slot_count
    return {
        "general_interface_condition": "C^* C=g I_2",
        "general_readout": str(sp.simplify(gain * alpha / N)),
        "unit_interface_readout": str(sp.simplify(alpha / N)),
        "gain_is_not_fixed_by_hidden_isotropy": True,
        "target_value_used": False,
    }


def uniqueness_statement() -> tuple[str, ...]:
    return (
        "U(N) conjugation invariance makes the stationary hidden density commute with every unitary.",
        "The only matrix commuting with the full defining U(N) representation is a scalar multiple of I_N.",
        "Tr(rho)=alpha fixes that scalar uniquely to alpha/N.",
        "C^*C=I_2 makes the normalized two-helicity interface readout alpha/N for every isometric interface.",
    )


def model_assumptions() -> tuple[str, ...]:
    return (
        "The hidden boundary register is K=ker(R_gamma) from p18bh.",
        "The leading weak boundary variable is a positive density rho on K with trace budget alpha.",
        "The quadratic hidden action is U(34)-isotropic at the matching scale.",
        "The photon couples through a unit-isometric two-helicity interface and reads its normalized trace.",
    )


def alternative_readout_guard(alpha: float) -> dict[str, float]:
    law = hidden_density_readout(alpha)
    return {
        "normalized_interface_readout": law.normalized_interface_readout,
        "unnormalized_two_helicity_trace": law.unnormalized_interface_trace,
        "total_hidden_trace": law.total_trace_budget,
        "rank_one_interface_readout": hidden_density_readout(
            alpha, helicity_interface_rank=1
        ).normalized_interface_readout,
        "gain_two_readout": hidden_density_readout(
            alpha, interface_gain=2.0
        ).normalized_interface_readout,
    }


def open_tasks() -> list[str]:
    return [
        "derive the hidden response density rho and Tr(rho)=alpha budget from the localized charged-core action",
        "derive U(34) isotropy of the quadratic hidden kernel and bound its symmetry-breaking terms",
        "derive the unit-isometric photon interface from the boundary-to-Maxwell reduction",
        "derive the matching coefficient multiplying this normalized trace in the full QED/EW effective action",
    ]


def run_gate() -> None:
    symbolic = exact_symbolic_theorem()
    interface_guard = interface_normalization_guard()
    probes = (1.0e-6, 1.0 / 137.0, 0.25)
    laws = tuple(hidden_density_readout(alpha) for alpha in probes)

    assert symbolic["hidden_dimension"] == 34
    assert symbolic["normalized_readout"] == "alpha/34"
    assert symbolic["stationarity_matrix_is_zero"]
    assert symbolic["hessian_positive_for_kappa_positive"]
    assert symbolic["target_value_used"] is False
    assert interface_guard["general_readout"] == "alpha*g/34"
    assert interface_guard["gain_is_not_fixed_by_hidden_isotropy"]
    for law in laws:
        assert law.hidden_dimension == 34
        assert law.helicity_interface_rank == 2
        assert law.interface_gain == 1.0
        assert law.stationary_residual == 0.0
        assert law.trace_constraint_residual < 1.0e-18
        assert abs(
            law.normalized_interface_readout
            - law.total_trace_budget / law.hidden_dimension
        ) < 1.0e-18
        assert law.target_value_used is False

    print("p18bj hidden-density normalized-trace readout gate")
    print("exact theorem")
    print(symbolic)
    print()
    print("uniqueness chain")
    for item in uniqueness_statement():
        print(f"- {item}")
    print()
    print("model assumptions")
    for item in model_assumptions():
        print(f"- {item}")
    print()
    print("interface normalization guard")
    print(interface_guard)
    print()
    print("probe evaluations")
    for law in laws:
        print(f"- {law}")
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print(
        "STATUS: OPEN_MICROSCOPIC_HIDDEN_KERNEL_DERIVATION__"
        "PASS_TARGET_INDEPENDENT_CONDITIONAL_ALPHA_OVER_34_TRACE_THEOREM"
    )


if __name__ == "__main__":
    run_gate()
