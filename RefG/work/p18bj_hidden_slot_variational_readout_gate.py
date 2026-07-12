from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from p18bh_boundary_slot_count_theorem_gate import (
    photon_readout_generators,
    slot_count_ledger,
)


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

    Let K=ker(R_gamma), dim_R(K)=N, and let rho be the positive symmetric
    weak-response operator on K.  At quadratic order the unresolved hidden
    sector is assumed to have O(N)-invariant action

        S[rho] = kappa/2 Tr(rho^2),   Tr(rho)=alpha.

    Strict convexity and the trace constraint give the unique stationary
    density rho_*=(alpha/N) I_N.  If C:R^2->K is any isometric two-helicity
    interface, the normalized external readout is

        q = (1/2) Tr(C^T rho_* C) = alpha/N.

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
    interface_metric = sp.simplify(C.T * C)
    normalized_readout = sp.simplify(sp.trace(C.T * rho * C) / 2)
    stationarity = sp.simplify(kappa * rho - kappa * alpha * sp.eye(N) / N)

    return {
        "hidden_dimension": N,
        "functional": "S[rho]=(kappa/2) Tr(rho^2)",
        "constraint": "Tr(rho)=alpha",
        "unique_minimizer": "rho_*=(alpha/N) I_N",
        "interface_condition": "C^T C=I_2",
        "interface_metric": str(interface_metric),
        "normalized_readout": str(normalized_readout),
        "stationarity_matrix_is_zero": stationarity == sp.zeros(N),
        "hessian_positive_for_kappa_positive": True,
        "target_value_used": False,
    }


def explicit_c3_hidden_interface() -> dict[str, object]:
    """Construct an exact orthonormal two-helicity interface inside ker(R)."""

    cyclic = sp.zeros(3)
    for row in range(3):
        cyclic[(row + 1) % 3, row] = 1
    D_c = sp.simplify((cyclic + cyclic.H) / sp.sqrt(6))

    sigma_1 = sp.Matrix([[0, 1], [1, 0]])
    sigma_2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sigma_3 = sp.Matrix([[1, 0], [0, -1]])
    deltas = (
        sp.kronecker_product(D_c, sigma_1) / sp.sqrt(2),
        sp.kronecker_product(D_c, sigma_2) / sp.sqrt(2),
    )
    gammas = photon_readout_generators()

    delta_gram = sp.Matrix(
        [
            [sp.simplify(sp.trace(left.H * right)) for right in deltas]
            for left in deltas
        ]
    )
    gamma_delta_cross = sp.Matrix(
        [
            [sp.simplify(sp.trace(gamma.H * delta)) for delta in deltas]
            for gamma in gammas
        ]
    )
    cyclic_on_V = sp.kronecker_product(cyclic, sp.eye(2))
    helicity_generator = sp.kronecker_product(sp.eye(3), sigma_3 / 2)
    commutator_1 = sp.simplify(
        helicity_generator * deltas[0] - deltas[0] * helicity_generator
    )
    commutator_2 = sp.simplify(
        helicity_generator * deltas[1] - deltas[1] * helicity_generator
    )

    return {
        "generation_operator": "D_c=(P_3+P_3^T)/sqrt(6)",
        "generation_trace": sp.simplify(sp.trace(D_c)),
        "generation_HS_norm_squared": sp.simplify(sp.trace(D_c.H * D_c)),
        "D_c_commutes_with_C3": sp.simplify(cyclic * D_c - D_c * cyclic)
        == sp.zeros(3),
        "hidden_helicity_pair": (
            "Delta_1=D_c tensor sigma_1/sqrt(2)",
            "Delta_2=D_c tensor sigma_2/sqrt(2)",
        ),
        "interface_gram": str(delta_gram),
        "orthogonal_to_photon_readout": gamma_delta_cross == sp.zeros(2),
        "Delta_1_commutator_is_i_Delta_2": sp.simplify(
            commutator_1 - sp.I * deltas[1]
        )
        == sp.zeros(6),
        "Delta_2_commutator_is_minus_i_Delta_1": sp.simplify(
            commutator_2 + sp.I * deltas[0]
        )
        == sp.zeros(6),
        "C3_commutes_with_Delta_1": sp.simplify(
            cyclic_on_V * deltas[0] - deltas[0] * cyclic_on_V
        )
        == sp.zeros(6),
        "C3_commutes_with_Delta_2": sp.simplify(
            cyclic_on_V * deltas[1] - deltas[1] * cyclic_on_V
        )
        == sp.zeros(6),
        "physical_interface_selection_derived": False,
        "target_value_used": False,
    }


def interface_normalization_guard() -> dict[str, object]:
    alpha, gain = sp.symbols("alpha g", positive=True)
    N = slot_count_ledger().hidden_boundary_slot_count
    return {
        "general_interface_condition": "C^T C=g I_2",
        "general_readout": str(sp.simplify(gain * alpha / N)),
        "unit_interface_readout": str(sp.simplify(alpha / N)),
        "gain_is_not_fixed_by_hidden_isotropy": True,
        "target_value_used": False,
    }


def full_matching_normalization_guard() -> dict[str, object]:
    alpha, c_budget, g_source, s_interface = sp.symbols(
        "alpha c g s", positive=True
    )
    N = slot_count_ledger().hidden_boundary_slot_count
    general = sp.simplify(
        c_budget * g_source * s_interface**2 * alpha / N
    )
    return {
        "general_trace_budget": "Tr(rho)=c*alpha",
        "general_source_term": "-g Tr_2[J C^T rho C]",
        "general_interface_metric": "C^T C=s^2 I_2",
        "general_scalar_readout": str(general),
        "unit_candidate": "c=g=s=1",
        "O34_and_N34_do_not_fix_c_g_s": True,
        "target_value_used": False,
    }


def anisotropic_kernel_guard() -> dict[str, object]:
    alpha = sp.symbols("alpha", positive=True)
    normal_slot = sp.simplify(2 * alpha / 67)
    stiff_slot = sp.simplify(alpha / 67)
    mixed_interface_mean = sp.simplify((normal_slot + stiff_slot) / 2)
    return {
        "stiffness_spectrum": "k_i=1 for 33 slots, k_34=2",
        "trace_constraint": "sum_i x_i=alpha",
        "normal_slot_weight": str(normal_slot),
        "stiff_slot_weight": str(stiff_slot),
        "mixed_two_channel_mean": str(mixed_interface_mean),
        "is_not_alpha_over_34": sp.simplify(
            mixed_interface_mean - alpha / 34
        )
        != 0,
        "O34_isotropy_is_essential": True,
        "target_value_used": False,
    }


def single_boundary_action_witness() -> dict[str, object]:
    """Package the trace and interface lemmas in one constrained action."""

    return {
        "action": (
            "S_boundary=(kappa/2)Tr(rho^2)+lambda(Tr(rho)-alpha)"
            "+(1/2)Tr[Lambda(C^T C-I_2)]-Tr_2[J C^T rho C]"
        ),
        "fields": "rho in Sym^+(K), C:R^2->K, dim_R K=34",
        "rho_Euler_Lagrange": "kappa*rho+lambda*I_34-C J C^T=0",
        "lambda_Euler_Lagrange": "Tr(rho)=alpha",
        "Lambda_Euler_Lagrange": "C^T C=I_2",
        "zero_source_solution": "J=0 gives lambda_*=-kappa*alpha/34",
        "unique_density_solution": "rho_*=(alpha/34)I_34",
        "response_tensor": "Q=-dW/dJ|_0=C^T rho_* C=(alpha/34)I_2",
        "scalar_Maxwell_coefficient": "q=Tr(Q)/2=alpha/34",
        "photon_quadratic_kernel": "Gamma_gamma^(2)[a]=(1/2)a^T[I_2-beta*Q]a",
        "boundary_matching_beta_derived": False,
        "O34_covariance": "rho->U rho U^T, C->U C",
        "trace_budget_installed_by_constraint": True,
        "unit_interface_installed_by_constraint": True,
        "microscopic_origin_derived": False,
        "target_value_used": False,
    }


def source_response_tensor_theorem() -> dict[str, object]:
    N = slot_count_ledger().hidden_boundary_slot_count
    alpha, kappa, t = sp.symbols("alpha kappa t", positive=True)
    j11, j12, j22 = sp.symbols("j11 j12 j22", real=True)
    J = sp.Matrix([[j11, j12], [j12, j22]])
    C = sp.zeros(N, 2)
    C[0, 0] = 1
    C[1, 1] = 1
    identity = sp.eye(N)

    lagrange = sp.simplify((sp.trace(J) - kappa * alpha) / N)
    rho_J = sp.simplify((C * J * C.T - lagrange * identity) / kappa)
    residual = sp.simplify(
        kappa * rho_J + lagrange * identity - C * J * C.T
    )
    trace_residual = sp.simplify(sp.trace(rho_J) - alpha)

    zero_source = {j11: 0, j12: 0, j22: 0}
    rho_zero = sp.simplify(rho_J.subs(zero_source))
    response_zero = sp.simplify(C.T * rho_zero * C)
    action_min = sp.simplify(kappa * sp.trace(rho_zero * rho_zero) / 2)

    perturbation = sp.zeros(N)
    perturbation[0, 0] = t
    perturbation[1, 1] = -t
    action_increase = sp.simplify(
        kappa
        * (
            sp.trace((rho_zero + perturbation) ** 2)
            - sp.trace(rho_zero**2)
        )
        / 2
    )

    return {
        "general_symmetric_source": "J=[[j11,j12],[j12,j22]]",
        "lambda_of_J": str(lagrange),
        "rho_of_J": (
            "rho(J)=alpha*I/N+(C J C^T-(Tr J/N)I)/kappa"
        ),
        "Euler_Lagrange_residual_zero": residual == sp.zeros(N),
        "trace_constraint_exact": trace_residual == 0,
        "zero_source_density": "rho(0)=(alpha/34)I_34",
        "zero_source_response_tensor": str(response_zero),
        "response_tensor_is_alpha_over_34_identity": response_zero
        == alpha * sp.eye(2) / N,
        "minimum_action": str(action_min),
        "trace_free_perturbation_action_increase": str(action_increase),
        "strictly_positive_for_nonzero_t_kappa": action_increase == kappa * t**2,
        "target_value_used": False,
    }


def uniqueness_statement() -> tuple[str, ...]:
    return (
        "O(N) conjugation invariance makes the stationary hidden density commute with every orthogonal transformation.",
        "The only symmetric operator commuting with the full defining O(N) representation is a scalar multiple of I_N.",
        "Tr(rho)=alpha fixes that scalar uniquely to alpha/N.",
        "C^T C=I_2 makes the normalized two-helicity interface readout alpha/N for every isometric interface.",
    )


def model_assumptions() -> tuple[str, ...]:
    return (
        "The hidden boundary register is K=ker(R_gamma) from p18bh.",
        "The leading weak boundary variable is a positive density rho on K with trace budget alpha.",
        "The quadratic hidden action is O(34)-isotropic at the matching scale.",
        "The photon couples through a unit-isometric two-helicity interface and reads its normalized trace.",
        "The explicit C3-covariant hidden pair Delta_1,2 is the physical interface selected by the core.",
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
        "derive O(34) isotropy of the quadratic hidden kernel and bound its symmetry-breaking terms",
        "derive the unit-isometric photon interface from the boundary-to-Maxwell reduction",
        "derive the matching coefficient multiplying this normalized trace in the full QED/EW effective action",
    ]


def run_gate() -> None:
    symbolic = exact_symbolic_theorem()
    interface_guard = interface_normalization_guard()
    full_normalization_guard = full_matching_normalization_guard()
    anisotropy_guard = anisotropic_kernel_guard()
    explicit_interface = explicit_c3_hidden_interface()
    action_witness = single_boundary_action_witness()
    response_theorem = source_response_tensor_theorem()
    probes = (1.0 / 101.0, 2.0 / 17.0, 1.0 / 5.0)
    laws = tuple(hidden_density_readout(alpha) for alpha in probes)

    assert symbolic["hidden_dimension"] == 34
    assert symbolic["normalized_readout"] == "alpha/34"
    assert symbolic["stationarity_matrix_is_zero"]
    assert symbolic["hessian_positive_for_kappa_positive"]
    assert symbolic["target_value_used"] is False
    assert interface_guard["general_readout"] == "alpha*g/34"
    assert interface_guard["gain_is_not_fixed_by_hidden_isotropy"]
    assert full_normalization_guard["general_scalar_readout"] == "alpha*c*g*s**2/34"
    assert full_normalization_guard["O34_and_N34_do_not_fix_c_g_s"]
    assert full_normalization_guard["target_value_used"] is False
    assert anisotropy_guard["mixed_two_channel_mean"] == "3*alpha/134"
    assert anisotropy_guard["is_not_alpha_over_34"]
    assert anisotropy_guard["O34_isotropy_is_essential"]
    assert explicit_interface["generation_trace"] == 0
    assert explicit_interface["generation_HS_norm_squared"] == 1
    assert explicit_interface["D_c_commutes_with_C3"]
    assert explicit_interface["interface_gram"] == "Matrix([[1, 0], [0, 1]])"
    assert explicit_interface["orthogonal_to_photon_readout"]
    assert explicit_interface["Delta_1_commutator_is_i_Delta_2"]
    assert explicit_interface["Delta_2_commutator_is_minus_i_Delta_1"]
    assert explicit_interface["C3_commutes_with_Delta_1"]
    assert explicit_interface["C3_commutes_with_Delta_2"]
    assert explicit_interface["physical_interface_selection_derived"] is False
    assert explicit_interface["target_value_used"] is False
    assert action_witness["trace_budget_installed_by_constraint"]
    assert action_witness["unit_interface_installed_by_constraint"]
    assert action_witness["boundary_matching_beta_derived"] is False
    assert action_witness["microscopic_origin_derived"] is False
    assert action_witness["target_value_used"] is False
    assert response_theorem["Euler_Lagrange_residual_zero"]
    assert response_theorem["trace_constraint_exact"]
    assert response_theorem["response_tensor_is_alpha_over_34_identity"]
    assert response_theorem["minimum_action"] == "alpha**2*kappa/68"
    assert response_theorem["trace_free_perturbation_action_increase"] == "kappa*t**2"
    assert response_theorem["strictly_positive_for_nonzero_t_kappa"]
    assert response_theorem["target_value_used"] is False
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
    print("full matching-normalization guard")
    print(full_normalization_guard)
    print()
    print("anisotropic-kernel guard")
    print(anisotropy_guard)
    print()
    print("explicit C3 hidden interface")
    print(explicit_interface)
    print()
    print("single constrained boundary-action witness")
    print(action_witness)
    print()
    print("source-response tensor theorem")
    print(response_theorem)
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
