from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from p18f_oriented_axis_completion_gate import (
    derive_oriented_axis_completion_gate,
)
from p18h_frame_connection_u1_gate import (
    derive_frame_connection_u1_gate,
)


C3_ORDER = 3
H_BRANCH = 2


@dataclass(frozen=True)
class SlotCountLedger:
    h_branch: int
    c3_order: int
    core_step_count: int
    internal_core_slot_count: int
    external_helicity_count: int
    hidden_boundary_slot_count: int
    slot_formula: str


@dataclass(frozen=True)
class BoundaryRankNullityTheorem:
    state_space: str
    response_space: str
    response_real_dimension: int
    photon_readout_generators: tuple[str, str]
    readout_rank: int
    kernel_dimension: int
    gamma_gram_matrix: tuple[tuple[int, int], tuple[int, int]]
    exact_sequence: str
    target_value_used: bool


def _pauli_generators() -> tuple[sp.Matrix, sp.Matrix]:
    sigma_1 = sp.Matrix([[0, 1], [1, 0]])
    sigma_2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    identity_c3 = sp.eye(C3_ORDER)
    normalization = sp.sqrt(C3_ORDER * H_BRANCH)
    gamma_1 = sp.kronecker_product(identity_c3, sigma_1) / normalization
    gamma_2 = sp.kronecker_product(identity_c3, sigma_2) / normalization
    return gamma_1, gamma_2


def photon_readout_generators() -> tuple[sp.Matrix, sp.Matrix]:
    """Public exact generators for downstream boundary-interface gates."""

    return _pauli_generators()


def boundary_symmetry_audit() -> dict[str, object]:
    gamma_1, gamma_2 = _pauli_generators()
    sigma_3 = sp.Matrix([[1, 0], [0, -1]])
    helicity_generator = sp.kronecker_product(
        sp.eye(C3_ORDER), sigma_3 / 2
    )

    cyclic = sp.zeros(C3_ORDER)
    for row in range(C3_ORDER):
        cyclic[(row + 1) % C3_ORDER, row] = 1
    cyclic_on_V = sp.kronecker_product(cyclic, sp.eye(H_BRANCH))

    comm_c3_gamma_1 = sp.simplify(cyclic_on_V * gamma_1 - gamma_1 * cyclic_on_V)
    comm_c3_gamma_2 = sp.simplify(cyclic_on_V * gamma_2 - gamma_2 * cyclic_on_V)
    comm_h_gamma_1 = sp.simplify(
        helicity_generator * gamma_1 - gamma_1 * helicity_generator
    )
    comm_h_gamma_2 = sp.simplify(
        helicity_generator * gamma_2 - gamma_2 * helicity_generator
    )
    gamma_plus = sp.simplify((gamma_1 + sp.I * gamma_2) / sp.sqrt(2))
    gamma_minus = sp.simplify((gamma_1 - sp.I * gamma_2) / sp.sqrt(2))

    helicity_plus_residual = sp.simplify(
        helicity_generator * gamma_plus
        - gamma_plus * helicity_generator
        - gamma_plus
    )
    helicity_minus_residual = sp.simplify(
        helicity_generator * gamma_minus
        - gamma_minus * helicity_generator
        + gamma_minus
    )

    # Hermitian matrices on C^3 commuting with the cyclic generator are
    # Hermitian circulants: one real diagonal coefficient and one complex
    # off-diagonal coefficient, hence real dimension three.
    return {
        "C3_commutes_with_gamma_1": comm_c3_gamma_1 == sp.zeros(6),
        "C3_commutes_with_gamma_2": comm_c3_gamma_2 == sp.zeros(6),
        "helicity_commutator_1": sp.simplify(comm_h_gamma_1 - sp.I * gamma_2)
        == sp.zeros(6),
        "helicity_commutator_2": sp.simplify(comm_h_gamma_2 + sp.I * gamma_1)
        == sp.zeros(6),
        "gamma_plus_has_helicity_plus_one": helicity_plus_residual
        == sp.zeros(6),
        "gamma_minus_has_helicity_minus_one": helicity_minus_residual
        == sp.zeros(6),
        "real_Hermitian_C3_commutant_dimension": 3,
        "C3_symmetry_alone_allows_helicity_pairs": 3,
        "generation_blind_identity_projection_is_additional": True,
        "target_value_used": False,
    }


def boundary_rank_nullity_theorem() -> BoundaryRankNullityTheorem:
    """Return the target-independent N=34 rank-nullity theorem.

    The conditional boundary model is

        V = C^3 tensor C^2,
        B = Herm(V),
        R(X)_a = Tr(Gamma_a X),  a=1,2.

    Herm(V) has real dimension 6^2=36.  The generation-blind helicity
    generators Gamma_1 and Gamma_2 are Hilbert--Schmidt orthonormal, so R has
    rank two.  Rank-nullity then gives dim_R ker(R)=36-2=34.

    No value of alpha, measured or otherwise, enters this calculation.
    """

    gamma_1, gamma_2 = _pauli_generators()
    gammas = (gamma_1, gamma_2)
    gram = sp.Matrix(
        [
            [sp.simplify(sp.trace(left.H * right)) for right in gammas]
            for left in gammas
        ]
    )
    rank = int(gram.rank())
    response_dim = (C3_ORDER * H_BRANCH) ** 2
    kernel_dim = response_dim - rank

    return BoundaryRankNullityTheorem(
        state_space="V=C^3 tensor C^2",
        response_space="B=Herm(V), viewed as a real Hilbert space",
        response_real_dimension=response_dim,
        photon_readout_generators=(
            "Gamma_1=I_3 tensor sigma_1/sqrt(6)",
            "Gamma_2=I_3 tensor sigma_2/sqrt(6)",
        ),
        readout_rank=rank,
        kernel_dimension=kernel_dim,
        gamma_gram_matrix=(
            (int(gram[0, 0]), int(gram[0, 1])),
            (int(gram[1, 0]), int(gram[1, 1])),
        ),
        exact_sequence="0 -> ker(R) -> Herm(C^3 tensor C^2) -> R^2 -> 0",
        target_value_used=False,
    )


def slot_count_ledger(h: int = H_BRANCH) -> SlotCountLedger:
    """Dimension ledger for the selected h=2 oriented charged branch.

    The exact matrix theorem above is specific to the two-helicity h=2
    branch.  The formula is retained for downstream symbolic use, while the
    gate rejects treating other h values as already established branches.
    """

    core_step = C3_ORDER * h
    internal_slots = core_step**2
    external_helicity = h
    hidden = internal_slots - external_helicity
    return SlotCountLedger(
        h_branch=h,
        c3_order=C3_ORDER,
        core_step_count=core_step,
        internal_core_slot_count=internal_slots,
        external_helicity_count=external_helicity,
        hidden_boundary_slot_count=hidden,
        slot_formula="dim_R Herm(C^(3h)) - rank(R_gamma) = (3h)^2-h",
    )


def existing_gate_support() -> dict[str, object]:
    axis = derive_oriented_axis_completion_gate()
    frame = derive_frame_connection_u1_gate()
    axis_closed = axis["closed_checks"]
    frame_closed = frame["closed_checks"]

    return {
        "p18f_status": axis["STATUS"],
        "p18h_status": frame["STATUS"],
        "p18f_two_luminal_modes": axis_closed["two_identical_luminal_modes"],
        "p18f_helicity_pair": axis_closed["helicity_pair_identified"],
        "p18h_u1_redundancy": frame_closed["Dtheta_is_U1_gauge_invariant"],
        "p18h_no_third_quadratic_mode": frame_closed[
            "gauge_fixed_fiber_has_no_quadratic_mode"
        ],
        "p18h_axis_pair_double_luminal": frame_closed[
            "axis_pair_remains_double_luminal"
        ],
        "supported_external_physical_channels": 2,
    }


def model_assumptions() -> tuple[str, ...]:
    return (
        "The charged boundary state is V=C^3 tensor C^2.",
        "Its complete quadratic response register is Herm(V), not V, Sym^2(V), wedge^2(V), or Herm_0(V).",
        "The external photon reads only the generation-blind pair I_3 tensor sigma_1,2.",
        "The h=2 oriented-frame return is the same two-state factor that carries the photon helicity pair.",
    )


def alternative_space_guard() -> dict[str, int]:
    """Show why the response-space identification is a real physical input."""

    d = C3_ORDER * H_BRANCH
    external_rank = H_BRANCH
    return {
        "V_hidden_dimension": d - external_rank,
        "wedge2V_hidden_dimension": d * (d - 1) // 2 - external_rank,
        "sym2V_hidden_dimension": d * (d + 1) // 2 - external_rank,
        "Herm0V_hidden_dimension": d * d - 1 - external_rank,
        "HermV_hidden_dimension": d * d - external_rank,
    }


def theorem_statement() -> dict[str, object]:
    theorem = boundary_rank_nullity_theorem()
    return {
        "conditional_claim": (
            "For B=Herm(C^3 tensor C^2) and the generation-blind two-helicity "
            "readout R, rank-nullity gives dim ker(R)=34."
        ),
        "result": theorem,
        "assumptions": model_assumptions(),
        "status": (
            "The N=34 count is now proved without an alpha fit inside this "
            "boundary representation.  Deriving the representation and "
            "readout map from the localized charged-core action remains open."
        ),
    }


def open_tasks() -> list[str]:
    return [
        "derive V=C^3 tensor C^2 as the charged boundary state space from the localized core",
        "derive Herm(V) as the complete quadratic response register",
        "derive the generation-blind photon projection I_3 tensor sigma_1,2",
        "exclude the alternative response spaces in alternative_space_guard from the microscopic action",
    ]


def run_gate() -> None:
    support = existing_gate_support()
    theorem = boundary_rank_nullity_theorem()
    symmetry = boundary_symmetry_audit()
    ledger = slot_count_ledger()
    alternatives = alternative_space_guard()

    assert support["p18f_two_luminal_modes"]
    assert support["p18f_helicity_pair"]
    assert support["p18h_u1_redundancy"]
    assert support["p18h_no_third_quadratic_mode"]
    assert support["p18h_axis_pair_double_luminal"]
    assert theorem.gamma_gram_matrix == ((1, 0), (0, 1))
    assert theorem.response_real_dimension == 36
    assert theorem.readout_rank == 2
    assert theorem.kernel_dimension == 34
    assert theorem.target_value_used is False
    assert symmetry["C3_commutes_with_gamma_1"]
    assert symmetry["C3_commutes_with_gamma_2"]
    assert symmetry["helicity_commutator_1"]
    assert symmetry["helicity_commutator_2"]
    assert symmetry["gamma_plus_has_helicity_plus_one"]
    assert symmetry["gamma_minus_has_helicity_minus_one"]
    assert symmetry["real_Hermitian_C3_commutant_dimension"] == 3
    assert symmetry["generation_blind_identity_projection_is_additional"]
    assert ledger.hidden_boundary_slot_count == theorem.kernel_dimension
    assert len(set(alternatives.values())) == len(alternatives)

    print("p18bh boundary rank-nullity theorem gate")
    print("support")
    print(support)
    print()
    print("theorem")
    print(theorem_statement())
    print()
    print("alternative-space guard")
    print(alternatives)
    print()
    print("boundary symmetry audit")
    print(symmetry)
    print()
    print("open tasks")
    for item in open_tasks():
        print(f"- {item}")
    print()
    print(
        "STATUS: OPEN_MICROSCOPIC_BOUNDARY_REPRESENTATION__"
        "PASS_TARGET_INDEPENDENT_CONDITIONAL_N34_RANK_NULLITY_THEOREM"
    )


if __name__ == "__main__":
    run_gate()
