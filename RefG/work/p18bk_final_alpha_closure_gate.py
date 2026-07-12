from __future__ import annotations

from dataclasses import dataclass

from p18bh_boundary_slot_count_theorem_gate import (
    boundary_rank_nullity_theorem,
)
from p18bj_hidden_slot_variational_readout_gate import hidden_density_readout
from p18bl_target_free_alpha_kernel_gate import (
    PredictionRecord,
    derivation_hypotheses,
    predict_empirical_mass_branch,
    predict_exact_c3_branch,
    prediction_digest,
    source_firewall,
)
from p18bm_alpha_observation_comparison_gate import (
    ObservationComparison,
    compare_with_reference,
    observation_perturbation_firewall,
)


@dataclass(frozen=True)
class ConditionalAlphaRelation:
    formula: str
    exact_c3_branch: PredictionRecord
    empirical_mass_branch: PredictionRecord
    runtime_target_free: bool
    historically_target_exposed: bool
    retrospectively_blind: bool
    independent_validation_completed: bool
    relation_status: str


def evaluate_conditional_relation() -> ConditionalAlphaRelation:
    exact = predict_exact_c3_branch()
    empirical = predict_empirical_mass_branch()
    firewall = source_firewall()
    perturbation = observation_perturbation_firewall()
    formula = (
        "Y=4*pi*9^2/(n*eta_*h^2)"
        "+(2/(3*pi))*ln(((3h)^2)^3*(m_tau/m_e)^5/(m_mu/m_e)); "
        "N=dim ker(R_gamma); q=(1/2)Tr(C^*rho C)=alpha/N; "
        "alpha^-1=(Y+sqrt(Y^2-8/(pi*N)))/2. "
        "Working conditional branch: h=2, n=h, eta_*=1, N=34."
    )

    return ConditionalAlphaRelation(
        formula=formula,
        exact_c3_branch=exact,
        empirical_mass_branch=empirical,
        runtime_target_free=bool(firewall["runtime_target_free"]),
        historically_target_exposed=bool(
            firewall["historically_target_exposed"]
        ),
        retrospectively_blind=bool(perturbation["retrospectively_blind"]),
        independent_validation_completed=bool(
            firewall["independent_validation_completed"]
        ),
        relation_status=(
            "The formula is now evaluated through a target-isolated kernel, "
            "with exact-C3 and empirical-mass branches kept separate.  It is "
            "a conditional relation until the listed action, matching and "
            "interface hypotheses are derived independently."
        ),
    )


def comparison_ledger() -> tuple[ObservationComparison, ObservationComparison]:
    relation = evaluate_conditional_relation()
    return (
        compare_with_reference(relation.exact_c3_branch),
        compare_with_reference(relation.empirical_mass_branch),
    )


def proof_chain() -> tuple[str, ...]:
    return (
        "The diagonal-sheet reduction gives q0^2=n*eta_* and exposes n=h, eta_*=1 as separate working hypotheses.",
        "The lepton threshold identity reduces to the scale-free logarithm in the displayed Y once the core-scale and lepton-only matching prescription are supplied.",
        "p18bh proves N=34 by rank-nullity inside B=Herm(C^3 tensor C^2) with a rank-two generation-blind photon map.",
        "p18bj proves q_boundary=alpha/N from the unique U(N)-isotropic trace-constrained density and a unit-isometric two-helicity interface.",
        "The boundary equation y=Y-(2/pi)/(N*y) has the displayed unique large positive quadratic root.",
        "p18bl computes both mass-ratio branches before p18bm introduces the reference value.",
    )


def unclosed_derivations() -> tuple[str, ...]:
    return (
        "derive an additive gauge-sheet level n equal to the oriented return index h",
        "derive the unit-sheet Maxwell/source normalization eta_*=k_*^2/K_*=1 from a completed action",
        "derive B=Herm(C^3 tensor C^2), its generation-blind photon projection and the U(34) hidden kernel from the localized core",
        "derive the trace budget and unit-isometric photon interface, including symmetry-breaking error bounds",
        "derive the core matching scale and justify the lepton-only threshold register in a full QED/EW/nonleptonic scheme",
        "obtain an independent charged-sector observable without reselecting h, N or the readout law",
    )


def run_gate() -> None:
    relation = evaluate_conditional_relation()
    exact_comparison, empirical_comparison = comparison_ledger()
    boundary = boundary_rank_nullity_theorem()
    readout = hidden_density_readout(relation.empirical_mass_branch.alpha)

    assert relation.exact_c3_branch.h_branch == 2
    assert relation.empirical_mass_branch.h_branch == 2
    assert boundary.kernel_dimension == 34
    assert relation.exact_c3_branch.hidden_dimension == 34
    assert relation.empirical_mass_branch.hidden_dimension == 34
    assert abs(relation.exact_c3_branch.equation_residual) < 1.0e-14
    assert abs(relation.empirical_mass_branch.equation_residual) < 1.0e-14
    assert readout.target_value_used is False
    assert relation.runtime_target_free is True
    assert relation.historically_target_exposed is True
    assert relation.retrospectively_blind is False
    assert relation.independent_validation_completed is False
    assert prediction_digest(relation.exact_c3_branch) == prediction_digest(
        predict_exact_c3_branch()
    )
    assert prediction_digest(
        relation.empirical_mass_branch
    ) == prediction_digest(predict_empirical_mass_branch())
    assert exact_comparison.observational_pass_claimed is False
    assert empirical_comparison.observational_pass_claimed is False

    print("p18bk conditional alpha relation gate")
    print("relation")
    print(relation)
    print()
    print("proof chain")
    for item in proof_chain():
        print(f"- {item}")
    print()
    print("observation comparison ledger")
    print(f"- {exact_comparison}")
    print(f"- {empirical_comparison}")
    print()
    print("explicit hypotheses")
    for item in derivation_hypotheses():
        print(f"- {item}")
    print()
    print("unclosed derivations")
    for item in unclosed_derivations():
        print(f"- {item}")
    print()
    print(
        "STATUS: OPEN_ACTION_DERIVATION_AND_INDEPENDENT_VALIDATION__"
        "PASS_TARGET_FREE_CONDITIONAL_ALPHA_RELATION"
    )


if __name__ == "__main__":
    run_gate()
