"""Exact adjudication of one state-derived order at the w2_16 endpoint.

The inherited state is A=S+R on the generic w2_16 minimum branch.  From that
state one can derive a target-free three-step Krylov filtration.  This file
proves the filtration exactly and then tests, separately, whether it is a
causal order.  It is not: the current law has no transition, intervention or
signal map, and A is equivalent to its algebraic transpose A.T under the accepted common
O(3) action.

Accordingly the executable result is positive for an atemporal algebraic
order and a scoped no-go for causal promotion from the current static inputs.
It does not reject future RefG dynamics and it does not close W2_F3.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable

import sympy as sp


SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F3_STATIC_ENDPOINT_ADJUDICATION_001",
    "CLAIM": (
        "Evaluate a target-free invariant Krylov filtration supplied by the frozen w2_16 static "
        "A=S+R endpoint, and admit W2_F3 only if a candidate also carries law-derived directed "
        "intervention response and forbidden-signal nontransmission."
    ),
    "TYPE": "EXACT_IDENTITY_PLUS_SCOPED_CAUSAL_NO_GO",
    "MODEL_VERSION": (
        "W2-C0, w2_16 conditional F2 endpoint, and w2_17 F3 contract. The evaluated candidate "
        "class adds no state primitive, transition law, clock, history, graph, orientation, "
        "metric, physical semantics, or fitted freedom."
    ),
    "ASSUMPTIONS": (
        "Import the abstract w2_16 minimum branch S=s(P_n-I/3), R=[r]_x, A=S+R, common O(3), "
        "J=-Tr(R^2)>0 and tau=K/(s^2 J). The carrier and polynomial law remain imported "
        "mathematical hypotheses rather than foundation-derived RefG facts."
    ),
    "DOMAIN": (
        "Exact generic filtration domain s>0, J>0 and 0<tau<1, equivalently nonzero parallel "
        "and perpendicular components of r relative to the unoriented S support line. tau=0, "
        "tau=1, J=0, s=0, and every inherited F2 null are excluded and tested separately."
    ),
    "CONVENTIONS": (
        "P0=I/3+S/s is the state-derived rank-one projector. G_k=sum_{j=0}^k "
        "A^j P0 (A^T)^j and V_k=Im(G_k), for k=0,1,2. The index k is algebraic Krylov depth, "
        "not time. Common O(3), including reflections, is the complete inherited equivalence."
    ),
    "FREEDOM_LEDGER": {
        "A_S_R_and_law": {
            "source": "imported unchanged from w2_16",
            "allowed_range": "w2_16 accepted generic F2 branch",
            "scale": "one atemporal state and five universal law coefficients",
            "complexity": 0,
        },
        "P0": {
            "source": "unique simple-eigenspace projector of S on the positive uniaxial branch",
            "allowed_range": "P0=I/3+S/s",
            "scale": "state-derived map",
            "complexity": 0,
        },
        "Krylov_filtration": {
            "source": "fixed inherited multiplication and transpose",
            "allowed_range": "V0 subset V1 subset V2",
            "scale": "state-derived construction",
            "complexity": 0,
        },
        "candidate_transition_intervention_signal_law": {
            "source": "absent by candidate definition",
            "allowed_range": 0,
            "scale": "dynamics",
            "complexity": 0,
        },
        "preferred_arrow_seed_graph_clock_metric": {
            "source": "forbidden",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
        "parameters_added_or_fitted_here": {
            "source": "none",
            "allowed_range": 0,
            "scale": "theory and data",
            "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py: valid "
        "conditional atemporal F1/F2 endpoint",
        "RefG/work 2/w2_17_f3_internal_order_causality_contract.py: valid fail-closed F3 schema",
    ],
    "METHOD": (
        "Use the complete w2_16 O(3) quotient to reduce exactly to n=e1 and "
        "r=(u,v,0); prove the Krylov ranks by Gram invariants and independently by a Krylov "
        "determinant/projector construction; then test transpose-involution equivalence, scalar-law "
        "reciprocity, graph axioms, nulls, target leaks, and every w2_17 causal gate."
    ),
    "PASS_CONDITION": (
        "The adjudication is valid only if both predecessor reports pass, every exact identity, "
        "null, equivariance, independent derivation, graph control, scoped no-go, schema and "
        "closure test passes. Atemporal order may close independently; W2_F3 requires every "
        "w2_17 causal gate and therefore must remain false if dynamics or no-transmission is absent."
    ),
    "FAIL_CONDITION": (
        "Any rank identity error, non-equivariant seed, hidden orientation, failed null, "
        "dependency drift, malformed gate report, unjustified causal upgrade, or false downstream "
        "closure invalidates this adjudication."
    ),
    "FALSIFIER": (
        "For the frozen CURRENT_F2_STATIC_ENDPOINT_ONLY causal candidate, the predeclared "
        "falsifier is met if A and A^T are in one accepted O(3) orbit while no inherited "
        "transition, intervention, signal, or no-transmission law exists. This rejects only "
        "causal promotion from this static candidate class."
    ),
    "RESIDUAL": (
        "Exactly zero for matrix, rank-certificate, equivariance, transpose-involution and mixed-derivative "
        "identities on the declared algebraic domain."
    ),
    "ERROR_BOUND": (
        "Zero: all evidence is symbolic exact algebra. Positivity statements apply only on the "
        "declared open domain; singular normalizations are not assigned values."
    ),
    "VALIDITY_HEALTH": (
        "The rank pattern is stable inside s>0,J>0,0<tau<1 and changes at its predeclared "
        "boundaries. The causal no-go is exact for the static state-only/common-O(3) class and "
        "for a same-state channel DAG inferred solely from reciprocal scalar-potential "
        "cross-response. It does not constrain event-level causal order from a new "
        "foundation-derived transition or response law, which may have reciprocal couplings."
    ),
    "BRANCHES": {
        "generic_Krylov_branch": "ATEMPORAL_INTERNAL_FILTRATION_PASS",
        "alternative_static_equivariant_flag": "EXISTS__NO_UNIQUENESS_OR_MAXIMALITY_CLAIM",
        "tau_zero": "RANK_PATTERN_1_1_1_NULL",
        "tau_one": "RANK_PATTERN_1_2_2_BOUNDARY_NULL",
        "J_zero": "RANK_PATTERN_1_1_1_NULL",
        "s_zero": "P0_UNDEFINED_NO_PROMOTION",
        "ordered_trace_antisymmetry": "EXACT_TERNARY_ALGEBRA_NOT_BINARY_CAUSAL_ARROW",
        "static_state_only_causal_promotion": "REJECTED_BY_FROZEN_FALSIFIER",
        "new_foundation_derived_dynamic_candidate": "OPEN_NEW_VERSION_REQUIRED",
        "physical_time_metric_and_later_gates": "OPEN",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "atemporal internal algebra only"},
    "FORWARD_MODEL": {
        "status": "N/A",
        "reason": "the evaluated candidate deliberately contains no physical dynamics or data map",
    },
    "DATA_ROLE": {"status": "N/A", "reason": "no data, fit, calibration, or target"},
    "IDENTIFIABILITY": (
        "The declared Krylov filtration is fixed by the state-derived P0 and inherited A, but "
        "it is not claimed unique among all equivariant static flags. Its generic rank stratum "
        "is identified by J>0 and 0<tau<1. No invariant transpose/skew-sign-odd scalar "
        "arrow is identifiable from the static orbit because A and A^T are equivalence-related."
    ),
    "BENCHMARK": (
        "Exact generic representative s=5,u=2,v=3 must have ranks (1,2,3). Exact tau=0, "
        "tau=1 and J=0 representatives must give (1,1,1), (1,2,2), and (1,1,1). A logical "
        "three-event DAG is the positive causal-screen control; two-way same-event and cyclic graphs "
        "must fail."
    ),
    "CLOSURE_FLAGS": {
        "F1_F2_conditional_predecessors_revalidated": True,
        "F3_candidate_class_evaluated": True,
        "atemporal_Krylov_filtration_proved": True,
        "ordered_trace_antisymmetry_identity_proved": True,
        "static_F2_only_route_rejected_as_F3_realization": True,
        "new_dynamic_candidate_required": True,
        "F3_internal_order_or_causality_proved": False,
        "physical_time_or_clock_readout_proved": False,
        "persistence_memory_or_signal_propagation_proved": False,
        "F4_independent_additive_modes_proved": False,
        "foundation_to_effective_closed": False,
        "W2_M1_dimension_or_continuum_proved": False,
        "W2_M2_Lorentzian_metric_proved": False,
        "effective_action_or_matter_coupling_proved": False,
        "Einstein_GR_PN_or_PPN_bridge_proved": False,
        "observational_validation_proved": False,
    },
    "CROSSCHECK": (
        "Gram-matrix elementary symmetric polynomials, direct Krylov-column determinant, "
        "orthogonal-projector reconstruction, exact reflection orbit, generic mixed-partial "
        "symmetry, graph transitive closure, and sibling-gate regression are evaluated "
        "independently."
    ),
    "PROVENANCE": {
        "date": "2026-07-22",
        "data": "none",
        "code_version": "w2_18 evaluator version 001",
        "hash": "N/A; source-control commit is the provenance record and no self-hash is embedded",
        "output": "JSON exact-adjudication report",
    },
    "FILES": [
        "CODES.md",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py",
        "RefG/work 2/w2_17_f3_internal_order_causality_contract.py",
        "RefG/work 2/w2_18_f3_static_endpoint_adjudication_gate.py",
    ],
    "THEOREM": {
        "atemporal_filtration": (
            "Let P0=I/3+S/s, G_k=sum_{j=0}^k A^j P0(A^T)^j and V_k=Im(G_k). "
            "On J>0 and 0<tau<1, e2(G1)=J tau/2 and det(G2)=J^3 tau^2(1-tau)/8, "
            "so dim(V0,V1,V2)=(1,2,3) and V0 is a strict subset of V1, which is a strict "
            "subset of V2. This is one invariant atemporal subspace inclusion, not evolution "
            "and not an exhaustiveness or uniqueness theorem."
        ),
        "nonuniqueness_boundary": (
            "The same static state also derives a distinct flag from the perpendicular "
            "component of the axial line of R: line(n) inside span(n,r) inside R^3. Therefore "
            "only the declared Krylov construction, not the strongest possible static order, "
            "is proved."
        ),
        "full_O3_equivariance": (
            "For every orthogonal Q, A'=QAQ^T and P0'=QP0Q^T imply term by term "
            "(A')^j P0' ((A')^T)^j = Q A^j P0 (A^T)^j Q^T. Hence Gk'=QGkQ^T "
            "and Vk'=QVk. Exact one-parameter Givens generators and a reflection are checked "
            "below; these generate O(3)."
        ),
        "projector_path": (
            "The state derives orthogonal rank-one P0,P1,P2 with reciprocal nonzero blocks "
            "P0<->P1 and P1<->P2 and zero P0<->P2 block. This is an undirected weighted "
            "algebraic path; a zero matrix block is not a no-signalling theorem."
        ),
        "ternary_orientation": (
            "For C=[S,R], Tr(S[R,C])=Tr(C^T C)=K>0 and Tr(SRC)=-Tr(RSC)=K/2. "
            "This exact ordered-triple identity is cyclic algebraic orientation, not a binary "
            "acyclic influence relation."
        ),
        "transpose_involution_no_go": (
            "Reflection through span(n,r) fixes S and sends R to -R, hence sends A to A^T. "
            "Any common-O(3)-invariant scalar report that is odd under this algebraic involution "
            "must therefore vanish. This is not a physical time-reversal theorem; the absence of "
            "a transition/intervention law is what prevents general F3 promotion."
        ),
        "reciprocal_response_no_go": (
            "The current scalar law is S/R separable, so its mixed Hessian is zero. More "
            "generally, an instantaneous Euclidean gradient response derived only from a C2 "
            "scalar potential has transpose-paired mixed blocks. At node-support level these "
            "are either absent or reciprocal and cannot alone define a same-state channel DAG. "
            "This does not forbid event-level causality in reciprocal dynamical theories."
        ),
        "required_escape": (
            "A future version must derive a genuinely directed transition, intervention or "
            "signal-response structure from the foundation, with a law-selected event arrow, "
            "open-domain stability and forbidden-signal controls. Couplings need not be "
            "nonreciprocal. It may not rename Krylov depth "
            "or an algorithmic step as time."
        ),
    },
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT
EXPECTED_CLOSURE_FLAGS = dict(CLAIM_CONTRACT["CLOSURE_FLAGS"])
STATIC_ROUTE_F3_PROMOTION_AUTHORIZED = False
STATIC_CANDIDATE_MAPS: dict[str, dict[str, str]] = {
    "state_space": {
        "status": "DERIVED",
        "source": "w2_16 accepted generic static state",
        "definition": "A=S+R modulo the inherited common O(3) action",
    },
    "event_or_change_map": {
        "status": "ABSENT",
        "source": "no event primitive in w2_16",
        "definition": "Krylov subspaces are static state functions, not event occurrences",
    },
    "complete_equivalence_action": {
        "status": "DERIVED",
        "source": "w2_16 common O(3) star-algebra equivalence",
        "definition": "simultaneous orthogonal conjugation including reflections",
    },
    "transition_or_response_law": {
        "status": "ABSENT",
        "source": "w2_16 supplies a static scalar law only",
        "definition": "no transition or response operator is imported",
    },
    "signal_support_or_update_composition": {
        "status": "ABSENT",
        "source": "no signal or update primitive in w2_16",
        "definition": "matrix multiplication is not renamed signal propagation",
    },
    "allowed_interventions": {
        "status": "ABSENT",
        "source": "no intervention class in w2_16",
        "definition": "none",
    },
    "intervention_to_response_map": {
        "status": "ABSENT",
        "source": "requires interventions and dynamics",
        "definition": "none",
    },
    "direct_influence_relation": {
        "status": "ABSENT",
        "source": "static block support is not influence",
        "definition": "none",
    },
    "transitive_effective_order": {
        "status": "ABSENT",
        "source": "no event-level direct influence relation",
        "definition": "none",
    },
    "forbidden_pairs": {
        "status": "ABSENT",
        "source": "no signal-support law",
        "definition": "none",
    },
    "no_transmission_test": {
        "status": "ABSENT",
        "source": "no signal response",
        "definition": "a zero static matrix block is not a no-transmission test",
    },
    "open_domain": {
        "status": "DERIVED",
        "source": "exact rank certificates",
        "definition": "s>0, J>0 and 0<tau<1",
    },
    "null_branches": {
        "status": "DERIVED",
        "source": "exact rank calculations and inherited F2 exclusions",
        "definition": "tau=0, tau=1, J=0, s=0 and all inherited F2 nulls",
    },
    "perturbation_class": {
        "status": "PARTIAL",
        "source": "rank stratum only",
        "definition": "static ranks are open-domain stable; dynamical initial-condition stability absent",
    },
    "independent_crosscheck": {
        "status": "DERIVED",
        "source": "Gram, Krylov determinant, projector and involution routes",
        "definition": "independent exact checks of the adjudication, not positive causal evidence",
    },
}
EXPECTED_STATIC_CANDIDATE_STATUSES = {
    "state_space": "DERIVED",
    "event_or_change_map": "ABSENT",
    "complete_equivalence_action": "DERIVED",
    "transition_or_response_law": "ABSENT",
    "signal_support_or_update_composition": "ABSENT",
    "allowed_interventions": "ABSENT",
    "intervention_to_response_map": "ABSENT",
    "direct_influence_relation": "ABSENT",
    "transitive_effective_order": "ABSENT",
    "forbidden_pairs": "ABSENT",
    "no_transmission_test": "ABSENT",
    "open_domain": "DERIVED",
    "null_branches": "DERIVED",
    "perturbation_class": "PARTIAL",
    "independent_crosscheck": "DERIVED",
}

DEPENDENCY_CONTROL_KEYS = frozenset({
    "w2_16_claim_identity_frozen",
    "w2_16_report_valid",
    "w2_16_full_structural_F2_proved",
    "w2_16_domain_law_and_complete_common_O3_frozen",
    "w2_16_inherited_null_registry_exact_and_all_true",
    "w2_16_has_no_dynamic_maps_and_kept_F3_false",
    "w2_17_claim_identity_frozen",
    "w2_17_contract_report_valid",
    "w2_17_candidate_class_identity_matches",
    "w2_17_F3_gate_schema_available",
    "static_candidate_map_schema_and_status_ledger_exact",
})
INHERITED_F2_NULL_KEYS = frozenset({
    "commuting_branch_null",
    "factorized_same_unary_null_detected",
    "independent_action_false_gauge_detected",
    "no_temporal_or_physical_semantics",
    "normalization_undefined_not_assigned",
    "self_pair_commutators_zero",
    "tuned_and_parameter_boundaries_not_promoted",
    "w2_12_diagonal_remains_unary_equality",
    "w2_14_unselected_fibre_not_reused",
    "zero_and_single_channel_nulls",
})
FILTRATION_CONTROL_KEYS = frozenset({
    "canonical_state_has_required_split_and_invariants",
    "P0_is_state_derived_rank_one_projector",
    "first_Gram_rank_certificate_exact",
    "first_certificate_equals_J_tau_over_two",
    "full_Gram_rank_certificate_exact",
    "full_certificate_equals_J3_tau2_one_minus_tau_over_eight",
    "Gram_factorizations_and_rank_upper_bounds_exact",
    "independent_Krylov_determinant_certificate_exact",
    "generic_rank_pattern_is_one_two_three",
    "generic_strict_filtration_follows_on_open_domain",
    "projector_route_is_exact_complete_orthogonal_triple",
    "distinct_alternative_equivariant_static_flag_exists",
    "projector_path_weights_are_reciprocal",
    "projector_weights_match_invariant_certificates",
    "ordered_trace_antisymmetry_identity_exact",
    "algebraic_depth_explicitly_not_time_or_causality",
})
EQUIVARIANCE_CONTROL_KEYS = frozenset({
    "independent_exact_O3_sample_crosschecks_pass",
    "arbitrary_Givens_generators_and_reflection_prove_full_O3_covariance",
    "alternative_static_flag_covariant_under_full_O3_generators",
    "no_external_seed_basis_or_orientation_in_freedom_ledger",
})
NULL_CONTROL_KEYS = frozenset({
    "generic_positive_benchmark",
    "tau_zero_collapses_to_one_one_one",
    "tau_one_stops_at_one_two_two",
    "J_zero_collapses_to_one_one_one",
    "s_zero_state_has_no_unique_normalized_support_projector",
    "raw_relation_nulls_S_zero_R_zero_and_tau_zero",
    "external_seed_mutation_changes_the_filtration",
})
GRAPH_CONTROL_KEYS = frozenset({
    "directed_DAG_positive_control_passes",
    "empty_relation_fails_only_required_nontriviality",
    "two_way_same_event_relation_fails_order_axioms",
    "directed_cycle_fails_acyclicity",
    "self_loop_fails_irreflexivity_asymmetry_and_acyclicity",
    "out_of_domain_edges_are_rejected_not_counted",
    "label_permutation_preserves_diagnostics",
    "edge_processing_schedule_does_not_change_closure",
    "prewired_DAG_is_only_a_logic_control_not_candidate_evidence",
})
TRANSPOSE_CONTROL_KEYS = frozenset({
    "reflection_is_accepted_orthogonal_transformation",
    "reflection_fixes_S_and_state_seed",
    "reflection_implements_R_C_sign_and_A_transpose_involution",
    "K_and_tau_are_transpose_involution_even",
    "invariant_and_transpose_odd_scalar_must_vanish",
    "static_scalar_arrow_no_go_is_scoped_not_general_causality_rejection",
})
GRADIENT_CONTROL_KEYS = frozenset({
    "imported_matrix_law_has_exact_zero_five_by_three_mixed_Hessian",
    "generic_C2_Schwarz_identity_gives_transpose_paired_cross_blocks",
    "zero_mixed_response_supplies_no_nontrivial_edge",
    "nonzero_reciprocal_same_state_support_fails_channel_DAG",
    "one_way_logical_control_would_pass_but_is_not_derived_here",
    "reciprocal_channel_no_go_scope_does_not_forbid_event_causality",
})
DECISION_CONTROL_KEYS = frozenset({
    "actual_F3_gate_map_valid_but_ineligible",
    "all_true_synthetic_map_still_not_self_promoted",
    "malformed_actual_map_fails_closed",
    "synthetic_eligibility_cannot_authorize_this_static_route",
    "frozen_static_causal_falsifier_met",
    "closure_matches_predeclared_result_exactly",
    "positive_algebraic_result_and_negative_causal_result_separated",
    "candidate_rejection_does_not_reject_new_dynamics",
})
CONTROL_GROUP_KEYS = frozenset({
    "dependency",
    "filtration",
    "equivariance",
    "nulls",
    "graph_controls",
    "transpose_involution_no_go",
    "reciprocal_gradient_no_go",
})


def _all_true(value: Any) -> bool:
    if isinstance(value, dict):
        return bool(value) and all(_all_true(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return bool(value) and all(_all_true(item) for item in value)
    return value is True


def exact_true_map(value: Any, expected_keys: frozenset[str]) -> bool:
    return bool(
        isinstance(value, dict)
        and set(value) == expected_keys
        and all(item is True for item in value.values())
    )


def frozen_static_candidate_statuses() -> dict[str, str]:
    return {
        "state_space": "DERIVED",
        "event_or_change_map": "ABSENT",
        "complete_equivalence_action": "DERIVED",
        "transition_or_response_law": "ABSENT",
        "signal_support_or_update_composition": "ABSENT",
        "allowed_interventions": "ABSENT",
        "intervention_to_response_map": "ABSENT",
        "direct_influence_relation": "ABSENT",
        "transitive_effective_order": "ABSENT",
        "forbidden_pairs": "ABSENT",
        "no_transmission_test": "ABSENT",
        "open_domain": "DERIVED",
        "null_branches": "DERIVED",
        "perturbation_class": "PARTIAL",
        "independent_crosscheck": "DERIVED",
    }


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_safe(item) for item in value]
    return str(value)


def matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def load_sibling(filename: str, module_name: str) -> ModuleType:
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_objects() -> dict[str, Any]:
    s = sp.symbols("s", positive=True)
    u, v = sp.symbols("u v", real=True)
    identity = sp.eye(3)
    p0 = sp.diag(1, 0, 0)
    symmetric = s * (p0 - identity / 3)
    skew = sp.Matrix([[0, 0, v], [0, 0, -u], [-v, u, 0]])
    carrier = symmetric * skew - skew * symmetric
    a_matrix = symmetric + skew
    j_invariant = sp.simplify(-sp.trace(skew**2))
    k_invariant = sp.simplify(sp.trace(carrier.T * carrier))
    tau = sp.factor(k_invariant / (s**2 * j_invariant))

    gram = []
    running = sp.zeros(3)
    for power in range(3):
        running = sp.simplify(
            running + (a_matrix**power) * p0 * (a_matrix.T**power)
        )
        gram.append(running)

    return {
        "s": s,
        "u": u,
        "v": v,
        "I": identity,
        "P0": p0,
        "S": symmetric,
        "R": skew,
        "A": a_matrix,
        "C": carrier,
        "J": j_invariant,
        "K": k_invariant,
        "tau": tau,
        "G0": gram[0],
        "G1": gram[1],
        "G2": gram[2],
    }


def frobenius_square(matrix: sp.MatrixBase) -> sp.Expr:
    return sp.simplify(sp.trace(matrix.T * matrix))


def rank_pattern(objects: dict[str, Any], substitutions: dict[sp.Symbol, Any]) -> tuple[int, ...]:
    return tuple(int(objects[key].subs(substitutions).rank()) for key in ("G0", "G1", "G2"))


def filtration_controls() -> dict[str, bool]:
    o = canonical_objects()
    s, u, v = o["s"], o["u"], o["v"]
    p0, a_matrix = o["P0"], o["A"]
    e2_g1 = sp.factor((sp.trace(o["G1"])**2 - sp.trace(o["G1"]**2)) / 2)
    det_g2 = sp.factor(o["G2"].det())

    krylov_two = sp.Matrix.hstack(p0[:, 0], a_matrix * p0[:, 0])
    krylov = sp.Matrix.hstack(krylov_two, a_matrix**2 * p0[:, 0])
    det_krylov = sp.factor(krylov.det())

    x1 = sp.simplify((o["I"] - p0) * a_matrix * p0 * a_matrix.T * (o["I"] - p0))
    p1 = sp.simplify(x1 / sp.trace(x1))
    p2 = sp.simplify(o["I"] - p0 - p1)
    projectors = (p0, p1, p2)

    axial_line = sp.simplify(o["I"] + 2 * o["R"]**2 / o["J"])
    alt_raw = sp.simplify((o["I"] - p0) * axial_line * (o["I"] - p0))
    p1_alt = sp.simplify(alt_raw / sp.trace(alt_raw))
    p2_alt = sp.simplify(o["I"] - p0 - p1_alt)

    blocks = {
        "10": frobenius_square(p1 * a_matrix * p0),
        "01": frobenius_square(p0 * a_matrix * p1),
        "21": frobenius_square(p2 * a_matrix * p1),
        "12": frobenius_square(p1 * a_matrix * p2),
        "20": frobenius_square(p2 * a_matrix * p0),
        "02": frobenius_square(p0 * a_matrix * p2),
    }

    omega = sp.factor(sp.trace(o["S"] * (o["R"] * o["C"] - o["C"] * o["R"])))
    src = sp.factor(sp.trace(o["S"] * o["R"] * o["C"]))
    rsc = sp.factor(sp.trace(o["R"] * o["S"] * o["C"]))

    return {
        "canonical_state_has_required_split_and_invariants": all((
            matrix_zero(o["S"].T - o["S"]),
            matrix_zero(o["R"].T + o["R"]),
            sp.trace(o["S"]) == 0,
            matrix_zero(o["A"] - o["S"] - o["R"]),
            o["J"] == 2 * (u**2 + v**2),
            o["K"] == 2 * s**2 * v**2,
            o["tau"] == v**2 / (u**2 + v**2),
        )),
        "P0_is_state_derived_rank_one_projector": all((
            matrix_zero(p0 - (o["I"] / 3 + o["S"] / s)),
            matrix_zero(p0**2 - p0),
            sp.trace(p0) == 1,
        )),
        "first_Gram_rank_certificate_exact": e2_g1 == v**2,
        "first_certificate_equals_J_tau_over_two": (
            sp.simplify(e2_g1 - o["J"] * o["tau"] / 2) == 0
        ),
        "full_Gram_rank_certificate_exact": det_g2 == u**2 * v**4,
        "full_certificate_equals_J3_tau2_one_minus_tau_over_eight": (
            sp.simplify(det_g2 - o["J"]**3 * o["tau"]**2 * (1 - o["tau"]) / 8) == 0
        ),
        "Gram_factorizations_and_rank_upper_bounds_exact": all((
            matrix_zero(o["G0"] - p0[:, 0] * p0[:, 0].T),
            matrix_zero(o["G1"] - krylov_two * krylov_two.T),
            matrix_zero(o["G2"] - krylov * krylov.T),
            krylov_two.shape == (3, 2),
            krylov.shape == (3, 3),
        )),
        "independent_Krylov_determinant_certificate_exact": all((
            det_krylov == u * v**2,
            sp.simplify(det_krylov**2 - det_g2) == 0,
        )),
        "generic_rank_pattern_is_one_two_three": (
            rank_pattern(o, {s: 5, u: 2, v: 3}) == (1, 2, 3)
        ),
        "generic_strict_filtration_follows_on_open_domain": all((
            e2_g1 == v**2,
            det_g2 == u**2 * v**4,
            "0<tau<1" in CLAIM_CONTRACT["DOMAIN"],
        )),
        "projector_route_is_exact_complete_orthogonal_triple": all((
            all(matrix_zero(pi**2 - pi) for pi in projectors),
            all(
                matrix_zero(projectors[i] * projectors[j])
                for i in range(3) for j in range(3) if i != j
            ),
            matrix_zero(sum(projectors, sp.zeros(3)) - o["I"]),
            all(sp.trace(pi) == 1 for pi in projectors),
        )),
        "distinct_alternative_equivariant_static_flag_exists": all((
            matrix_zero(axial_line**2 - axial_line),
            sp.simplify(sp.trace(axial_line)) == 1,
            matrix_zero(p1_alt**2 - p1_alt),
            matrix_zero(p2_alt**2 - p2_alt),
            sp.simplify(sp.trace(p1_alt)) == 1,
            sp.simplify(sp.trace(p2_alt)) == 1,
            matrix_zero(p0 * p1_alt),
            matrix_zero(p0 + p1_alt + p2_alt - o["I"]),
            not matrix_zero(p1_alt - p1),
            CLAIM_CONTRACT["BRANCHES"]["alternative_static_equivariant_flag"]
            == "EXISTS__NO_UNIQUENESS_OR_MAXIMALITY_CLAIM",
        )),
        "projector_path_weights_are_reciprocal": all((
            blocks["10"] == v**2,
            blocks["01"] == v**2,
            blocks["21"] == u**2,
            blocks["12"] == u**2,
            blocks["20"] == 0,
            blocks["02"] == 0,
        )),
        "projector_weights_match_invariant_certificates": all((
            sp.simplify(blocks["10"] - o["J"] * o["tau"] / 2) == 0,
            sp.simplify(blocks["21"] - o["J"] * (1 - o["tau"]) / 2) == 0,
        )),
        "ordered_trace_antisymmetry_identity_exact": all((
            sp.simplify(omega - o["K"]) == 0,
            sp.simplify(src - o["K"] / 2) == 0,
            sp.simplify(rsc + o["K"] / 2) == 0,
        )),
        "algebraic_depth_explicitly_not_time_or_causality": all((
            "not time" in CLAIM_CONTRACT["CONVENTIONS"],
            CLAIM_CONTRACT["CLOSURE_FLAGS"]["F3_internal_order_or_causality_proved"] is False,
            CLAIM_CONTRACT["BRANCHES"]["ordered_trace_antisymmetry"]
            == "EXACT_TERNARY_ALGEBRA_NOT_BINARY_CAUSAL_ARROW",
        )),
    }


def transformed_gram(
    a_matrix: sp.MatrixBase, p0: sp.MatrixBase, orthogonal: sp.MatrixBase, power: int
) -> sp.Matrix:
    transformed_a = sp.simplify(orthogonal * a_matrix * orthogonal.T)
    transformed_p = sp.simplify(orthogonal * p0 * orthogonal.T)
    terms = [
        transformed_a**index * transformed_p * (transformed_a.T**index)
        for index in range(power + 1)
    ]
    return sp.simplify(sum(terms, sp.zeros(3)))


def equivariance_controls() -> dict[str, bool]:
    o = canonical_objects()
    axial_line = sp.simplify(o["I"] + 2 * o["R"]**2 / o["J"])
    alt_raw = sp.simplify(
        (o["I"] - o["P0"]) * axial_line * (o["I"] - o["P0"])
    )
    alt_projector = sp.simplify(alt_raw / sp.trace(alt_raw))
    parameter = sp.symbols("t", real=True)
    cosine = (1 - parameter**2) / (1 + parameter**2)
    sine = 2 * parameter / (1 + parameter**2)

    rotations = []
    for left, right in ((0, 1), (0, 2), (1, 2)):
        rotation = sp.eye(3)
        rotation[left, left] = cosine
        rotation[right, right] = cosine
        rotation[left, right] = -sine
        rotation[right, left] = sine
        rotations.append(rotation)
    reflection = sp.diag(1, 1, -1)

    rational_orthogonal = sp.Matrix([
        [sp.Rational(3, 5), -sp.Rational(4, 5), 0],
        [sp.Rational(4, 5), sp.Rational(3, 5), 0],
        [0, 0, -1],
    ])
    permutation = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    tests = []
    for orthogonal in (rational_orthogonal, permutation):
        tests.append(matrix_zero(orthogonal.T * orthogonal - sp.eye(3)))
        for power, key in enumerate(("G0", "G1", "G2")):
            tests.append(matrix_zero(
                transformed_gram(o["A"], o["P0"], orthogonal, power)
                - orthogonal * o[key] * orthogonal.T
            ))

    generator_tests = []
    alternative_flag_tests = []
    for orthogonal in (*rotations, reflection):
        generator_tests.append(matrix_zero(
            sp.simplify(orthogonal.T * orthogonal - sp.eye(3))
        ))
        for power, key in enumerate(("G0", "G1", "G2")):
            generator_tests.append(matrix_zero(
                transformed_gram(o["A"], o["P0"], orthogonal, power)
                - orthogonal * o[key] * orthogonal.T
            ))
        transformed_r = sp.simplify(orthogonal * o["R"] * orthogonal.T)
        transformed_p0 = sp.simplify(orthogonal * o["P0"] * orthogonal.T)
        transformed_j = sp.simplify(-sp.trace(transformed_r**2))
        transformed_axial = sp.simplify(
            o["I"] + 2 * transformed_r**2 / transformed_j
        )
        transformed_alt_raw = sp.simplify(
            (o["I"] - transformed_p0) * transformed_axial
            * (o["I"] - transformed_p0)
        )
        transformed_alt_projector = sp.simplify(
            transformed_alt_raw / sp.trace(transformed_alt_raw)
        )
        alternative_flag_tests.extend((
            sp.simplify(transformed_j - o["J"]) == 0,
            matrix_zero(transformed_axial - orthogonal * axial_line * orthogonal.T),
            matrix_zero(transformed_alt_raw - orthogonal * alt_raw * orthogonal.T),
            matrix_zero(
                transformed_alt_projector
                - orthogonal * alt_projector * orthogonal.T
            ),
        ))

    return {
        "independent_exact_O3_sample_crosschecks_pass": all(tests),
        "arbitrary_Givens_generators_and_reflection_prove_full_O3_covariance": all(
            generator_tests
        ),
        "alternative_static_flag_covariant_under_full_O3_generators": all(
            alternative_flag_tests
        ),
        "no_external_seed_basis_or_orientation_in_freedom_ledger": (
            CLAIM_CONTRACT["FREEDOM_LEDGER"]["preferred_arrow_seed_graph_clock_metric"]
            ["allowed_range"] == 0
        ),
    }


def null_controls() -> dict[str, bool]:
    o = canonical_objects()
    s, u, v = o["s"], o["u"], o["v"]
    alternate_seed = sp.diag(0, 1, 0)
    alternate_g1 = sp.simplify(alternate_seed + o["A"] * alternate_seed * o["A"].T)
    zero_from_first_projector = sp.simplify(0 * (sp.diag(1, 0, 0) - sp.eye(3) / 3))
    zero_from_second_projector = sp.simplify(0 * (sp.diag(0, 1, 0) - sp.eye(3) / 3))
    return {
        "generic_positive_benchmark": rank_pattern(o, {s: 5, u: 2, v: 3}) == (1, 2, 3),
        "tau_zero_collapses_to_one_one_one": all((
            sp.simplify(o["tau"].subs({u: 2, v: 0})) == 0,
            rank_pattern(o, {s: 5, u: 2, v: 0}) == (1, 1, 1),
        )),
        "tau_one_stops_at_one_two_two": all((
            sp.simplify(o["tau"].subs({u: 0, v: 3})) == 1,
            rank_pattern(o, {s: 5, u: 0, v: 3}) == (1, 2, 2),
        )),
        "J_zero_collapses_to_one_one_one": all((
            o["J"].subs({u: 0, v: 0}) == 0,
            rank_pattern(o, {s: 5, u: 0, v: 0}) == (1, 1, 1),
        )),
        "s_zero_state_has_no_unique_normalized_support_projector": all((
            matrix_zero(zero_from_first_projector),
            matrix_zero(zero_from_second_projector),
            not matrix_zero(sp.diag(1, 0, 0) - sp.diag(0, 1, 0)),
        )),
        "raw_relation_nulls_S_zero_R_zero_and_tau_zero": all((
            o["K"].subs(s, 0) == 0,
            o["K"].subs({u: 0, v: 0}) == 0,
            o["K"].subs(v, 0) == 0,
        )),
        "external_seed_mutation_changes_the_filtration": not matrix_zero(
            alternate_g1 - o["G1"]
        ),
    }


def transitive_closure(nodes: Iterable[int], edges: Iterable[tuple[int, int]]) -> set[tuple[int, int]]:
    node_set = set(nodes)
    closure = {(left, right) for left, right in edges if left in node_set and right in node_set}
    changed = True
    while changed:
        changed = False
        additions = {
            (left, right2)
            for left, middle in closure
            for middle2, right2 in closure
            if middle == middle2 and (left, right2) not in closure
        }
        if additions:
            closure |= additions
            changed = True
    return closure


def strict_relation_diagnostics(
    nodes: Iterable[int], edges: Iterable[tuple[int, int]]
) -> dict[str, bool]:
    node_set = set(nodes)
    raw_edges = set(edges)
    edge_set = {
        (left, right)
        for left, right in raw_edges
        if left in node_set and right in node_set
    }
    closure = transitive_closure(node_set, edge_set)
    irreflexive = all((node, node) not in closure for node in node_set)
    asymmetric = all((right, left) not in closure for left, right in closure)
    reflexive_closure = closure | {(node, node) for node in node_set}
    antisymmetric = all(
        left == right or (right, left) not in reflexive_closure
        for left, right in reflexive_closure
    )
    return {
        "nontrivial": any(left != right for left, right in edge_set),
        "all_edges_in_domain": raw_edges == edge_set,
        "irreflexive": irreflexive,
        "asymmetric": asymmetric,
        "acyclic": irreflexive,
        "effective_order_transitive": transitive_closure(node_set, closure) == closure,
        "reflexive_closure_antisymmetric": antisymmetric,
    }


def graph_control_tests() -> dict[str, bool]:
    nodes = {0, 1, 2}
    directed = strict_relation_diagnostics(nodes, {(0, 1), (1, 2)})
    empty = strict_relation_diagnostics(nodes, set())
    reciprocal = strict_relation_diagnostics(nodes, {(0, 1), (1, 0)})
    cycle = strict_relation_diagnostics(nodes, {(0, 1), (1, 2), (2, 0)})
    self_loop = strict_relation_diagnostics(nodes, {(0, 0)})
    outside = strict_relation_diagnostics({0, 1}, {(2, 3)})

    relabel = {0: 2, 1: 0, 2: 1}
    relabelled = strict_relation_diagnostics(
        {relabel[node] for node in nodes},
        {(relabel[left], relabel[right]) for left, right in {(0, 1), (1, 2)}},
    )
    schedule_a = transitive_closure(nodes, [(0, 1), (1, 2)])
    schedule_b = transitive_closure(nodes, [(1, 2), (0, 1)])
    return {
        "directed_DAG_positive_control_passes": _all_true(directed),
        "empty_relation_fails_only_required_nontriviality": all((
            not empty["nontrivial"], empty["irreflexive"], empty["acyclic"]
        )),
        "two_way_same_event_relation_fails_order_axioms": all((
            reciprocal["nontrivial"],
            not reciprocal["asymmetric"],
            not reciprocal["acyclic"],
            not reciprocal["reflexive_closure_antisymmetric"],
        )),
        "directed_cycle_fails_acyclicity": cycle["nontrivial"] and not cycle["acyclic"],
        "self_loop_fails_irreflexivity_asymmetry_and_acyclicity": all((
            not self_loop["irreflexive"],
            not self_loop["asymmetric"],
            not self_loop["acyclic"],
        )),
        "out_of_domain_edges_are_rejected_not_counted": all((
            not outside["all_edges_in_domain"],
            not outside["nontrivial"],
        )),
        "label_permutation_preserves_diagnostics": relabelled == directed,
        "edge_processing_schedule_does_not_change_closure": schedule_a == schedule_b,
        "prewired_DAG_is_only_a_logic_control_not_candidate_evidence": (
            CLAIM_CONTRACT["BENCHMARK"].find("logical three-event DAG") >= 0
            and CLAIM_CONTRACT["FREEDOM_LEDGER"]["preferred_arrow_seed_graph_clock_metric"]
            ["allowed_range"] == 0
        ),
    }


def transpose_involution_no_go_controls() -> dict[str, bool]:
    o = canonical_objects()
    reflection = sp.diag(1, 1, -1)
    arrow = sp.symbols("D", real=True)
    arrow_solutions = sp.solve(sp.Eq(arrow, -arrow), arrow)
    return {
        "reflection_is_accepted_orthogonal_transformation": all((
            matrix_zero(reflection.T * reflection - sp.eye(3)),
            reflection.det() == -1,
        )),
        "reflection_fixes_S_and_state_seed": all((
            matrix_zero(reflection * o["S"] * reflection.T - o["S"]),
            matrix_zero(reflection * o["P0"] * reflection.T - o["P0"]),
        )),
        "reflection_implements_R_C_sign_and_A_transpose_involution": all((
            matrix_zero(reflection * o["R"] * reflection.T + o["R"]),
            matrix_zero(reflection * o["C"] * reflection.T + o["C"]),
            matrix_zero(reflection * o["A"] * reflection.T - o["A"].T),
        )),
        "K_and_tau_are_transpose_involution_even": all((
            sp.simplify(sp.trace((-o["C"]).T * (-o["C"])) - o["K"]) == 0,
            sp.simplify(o["tau"].subs({o["u"]: -o["u"], o["v"]: -o["v"]}) - o["tau"]) == 0,
        )),
        "invariant_and_transpose_odd_scalar_must_vanish": arrow_solutions == [0],
        "static_scalar_arrow_no_go_is_scoped_not_general_causality_rejection": (
            CLAIM_CONTRACT["BRANCHES"]["new_foundation_derived_dynamic_candidate"]
            == "OPEN_NEW_VERSION_REQUIRED"
            and "not a physical time-reversal theorem"
            in CLAIM_CONTRACT["THEOREM"]["transpose_involution_no_go"]
        ),
    }


def reciprocal_gradient_controls() -> dict[str, bool]:
    x_variables = sp.symbols("x0:2", real=True)
    y_variables = sp.symbols("y0:2", real=True)
    generic_potential = sp.Function("V")(*x_variables, *y_variables)
    generic_cross_xy = sp.Matrix([
        [sp.diff(-sp.diff(generic_potential, x_var), y_var) for y_var in y_variables]
        for x_var in x_variables
    ])
    generic_cross_yx = sp.Matrix([
        [sp.diff(-sp.diff(generic_potential, y_var), x_var) for x_var in x_variables]
        for y_var in y_variables
    ])

    q1, q2, q4, q5, q6 = sp.symbols("q1 q2 q4 q5 q6", real=True)
    r1, r2, r3 = sp.symbols("r1 r2 r3", real=True)
    q_variables = (q1, q2, q4, q5, q6)
    r_variables = (r1, r2, r3)
    symmetric = sp.Matrix([
        [q1, q4, q5],
        [q4, q2, q6],
        [q5, q6, -q1 - q2],
    ])
    skew = sp.Matrix([[0, -r3, r2], [r3, 0, -r1], [-r2, r1, 0]])
    alpha, beta, gamma, eta, delta = sp.symbols(
        "alpha beta gamma eta delta", real=True
    )
    i2 = sp.trace(symmetric**2)
    i3 = sp.trace(symmetric**3)
    j_invariant = -sp.trace(skew**2)
    imported_law = (
        -alpha * i2 / 2 - beta * i3 / 3 + gamma * i2**2 / 4
        - eta * j_invariant / 2 + delta * j_invariant**2 / 4
    )
    mixed_matrix_hessian = sp.Matrix([
        [sp.diff(imported_law, q_var, r_var) for r_var in r_variables]
        for q_var in q_variables
    ])

    reciprocal = strict_relation_diagnostics({0, 1}, {(0, 1), (1, 0)})
    directed = strict_relation_diagnostics({0, 1}, {(0, 1)})
    return {
        "imported_matrix_law_has_exact_zero_five_by_three_mixed_Hessian": (
            mixed_matrix_hessian.shape == (5, 3) and matrix_zero(mixed_matrix_hessian)
        ),
        "generic_C2_Schwarz_identity_gives_transpose_paired_cross_blocks": (
            matrix_zero(generic_cross_xy - generic_cross_yx.T)
        ),
        "zero_mixed_response_supplies_no_nontrivial_edge": (
            strict_relation_diagnostics({0, 1}, set())["nontrivial"] is False
        ),
        "nonzero_reciprocal_same_state_support_fails_channel_DAG": all((
            reciprocal["nontrivial"],
            not reciprocal["asymmetric"],
            not reciprocal["acyclic"],
        )),
        "one_way_logical_control_would_pass_but_is_not_derived_here": all((
            _all_true(directed),
            CLAIM_CONTRACT["FREEDOM_LEDGER"]
            ["candidate_transition_intervention_signal_law"]["allowed_range"] == 0,
        )),
        "reciprocal_channel_no_go_scope_does_not_forbid_event_causality": (
            "same-state channel DAG inferred solely from reciprocal scalar-potential"
            in CLAIM_CONTRACT["VALIDITY_HEALTH"]
            and "may have reciprocal couplings" in CLAIM_CONTRACT["VALIDITY_HEALTH"]
        ),
    }


def dependency_controls() -> tuple[dict[str, bool], ModuleType, ModuleType]:
    w216 = load_sibling(
        "w2_16_f2b_general_traceless_single_carrier_candidate_gate.py", "w2_16_dependency"
    )
    w217 = load_sibling(
        "w2_17_f3_internal_order_causality_contract.py", "w2_17_dependency"
    )
    report16 = w216.run()
    report17 = w217.run()
    controls = {
        "w2_16_claim_identity_frozen": (
            w216.CLAIM_CONTRACT["CLAIM_ID"]
            == "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CANDIDATE_001"
        ),
        "w2_16_report_valid": report16.get("valid") is True,
        "w2_16_full_structural_F2_proved": (
            report16.get("closure_decision", {})
            .get("full_W2_F2_operational_relations_proved") is True
        ),
        "w2_16_domain_law_and_complete_common_O3_frozen": all((
            w216.CLAIM_CONTRACT["DOMAIN"]
            == "Full accepted minimum set for alpha,b,c,eta,d>0; structural F2 PASS only "
            "on the open subset b^2!=3 alpha c and 0<tau<1, with all listed nulls excluded.",
            w216.CLAIM_CONTRACT["CONVENTIONS"].endswith("common O(3)."),
            report16["controls"]["minimum"]["product_minimum_separability_exact"],
            report16["controls"]["minimum"]["mixed_coefficients_remain_exact_zero"],
            report16["controls"]["quotient"]["same_tau_canonical_representative_complete"],
        )),
        "w2_16_inherited_null_registry_exact_and_all_true": exact_true_map(
            report16["controls"]["nulls"], INHERITED_F2_NULL_KEYS
        ),
        "w2_16_has_no_dynamic_maps_and_kept_F3_false": all((
            w216.CLAIM_CONTRACT["FORWARD_MODEL"]
            == {"status": "N/A", "reason": "no observable or dynamics"},
            report16.get("closure_decision", {})
            .get("F3_internal_order_or_causality_proved") is False,
        )),
        "w2_17_claim_identity_frozen": (
            w217.CLAIM_CONTRACT["CLAIM_ID"] == "W2_F3_INTERNAL_ORDER_CAUSALITY_CONTRACT_001"
        ),
        "w2_17_contract_report_valid": report17.get("valid") is True,
        "w2_17_candidate_class_identity_matches": (
            w217.CLAIM_CONTRACT.get("FIRST_EVALUATION_CLASS")
            == w217.frozen_first_evaluation_class()
        ),
        "w2_17_F3_gate_schema_available": (
            w217.F3_GATE_KEYS == w217.EXPECTED_F3_GATE_KEYS
            == w217.frozen_f3_gate_keys()
            and len(w217.F3_GATE_KEYS) == 18
            and w217.REQUIRED_CANDIDATE_MAPS == w217.EXPECTED_REQUIRED_CANDIDATE_MAPS
            == w217.frozen_required_candidate_maps()
            and len(w217.REQUIRED_CANDIDATE_MAPS) == 15
        ),
        "static_candidate_map_schema_and_status_ledger_exact": all((
            w217.candidate_map_schema_valid(STATIC_CANDIDATE_MAPS),
            {
                key: entry["status"] for key, entry in STATIC_CANDIDATE_MAPS.items()
            } == EXPECTED_STATIC_CANDIDATE_STATUSES
            == frozen_static_candidate_statuses(),
            any(entry["status"] != "DERIVED" for entry in STATIC_CANDIDATE_MAPS.values()),
        )),
    }
    return controls, w216, w217


def causal_gate_map(
    dependency: dict[str, bool], w217: ModuleType, transpose_no_go: dict[str, bool],
    graphs: dict[str, bool], equivariance: dict[str, bool], nulls: dict[str, bool],
) -> dict[str, bool]:
    gates = {
        "same_chain_F1_F2_predecessors_valid": all((
            dependency["w2_16_report_valid"],
            dependency["w2_16_full_structural_F2_proved"],
        )),
        "state_owned_events_or_changes_derived": False,
        "target_free_transition_or_response_law_derived": False,
        "candidate_dynamics_health_and_state_space_closure_proved": False,
        "allowed_interventions_defined": False,
        "directed_intervention_response_proved": False,
        "correlation_and_static_ranking_excluded": all((
            STATIC_CANDIDATE_MAPS["event_or_change_map"]["status"] == "ABSENT",
            STATIC_CANDIDATE_MAPS["direct_influence_relation"]["status"] == "ABSENT",
            CLAIM_CONTRACT["CLOSURE_FLAGS"]["F3_internal_order_or_causality_proved"] is False,
        )),
        "complete_equivalence_invariance_proved": exact_true_map(
            equivariance, EQUIVARIANCE_CONTROL_KEYS
        ),
        "arrow_selected_by_law_not_labels_or_schedule": False,
        "nontrivial_direct_influence_on_predeclared_open_domain": False,
        "strict_relation_irreflexive_asymmetric_and_acyclic": False,
        "effective_order_transitive_and_reflexive_closure_antisymmetric": False,
        "forbidden_signal_nontransmission_proved": False,
        "computational_schedule_neutrality_proved": (
            graphs["edge_processing_schedule_does_not_change_closure"]
        ),
        "null_reverse_and_target_leak_controls_pass": all((
            exact_true_map(nulls, NULL_CONTROL_KEYS),
            exact_true_map(transpose_no_go, TRANSPOSE_CONTROL_KEYS),
            graphs["prewired_DAG_is_only_a_logic_control_not_candidate_evidence"],
        )),
        "perturbation_and_initial_condition_stability_proved": False,
        "independent_second_derivation_passes": False,
        "physical_time_metric_and_downstream_gates_remain_open": all(
            value is False
            for key, value in CLAIM_CONTRACT["CLOSURE_FLAGS"].items()
            if key in {
                "F3_internal_order_or_causality_proved",
                "physical_time_or_clock_readout_proved",
                "F4_independent_additive_modes_proved",
                "foundation_to_effective_closed",
                "W2_M1_dimension_or_continuum_proved",
                "W2_M2_Lorentzian_metric_proved",
                "effective_action_or_matter_coupling_proved",
                "Einstein_GR_PN_or_PPN_bridge_proved",
                "observational_validation_proved",
            }
        ),
    }
    if set(gates) != set(w217.frozen_f3_gate_keys()) or any(
        type(value) is not bool for value in gates.values()
    ):
        return {key: False for key in w217.frozen_f3_gate_keys()}
    return gates


def closure_decision(
    predecessors_valid: bool,
    filtration_valid: bool,
    trace_identity_valid: bool,
    adjudication_valid: bool,
    screen: dict[str, bool],
    falsifier_met: bool,
) -> dict[str, bool]:
    causal = bool(
        adjudication_valid
        and screen["valid"]
        and screen["eligible"]
        and STATIC_ROUTE_F3_PROMOTION_AUTHORIZED
    )
    return {
        "F1_F2_conditional_predecessors_revalidated": predecessors_valid,
        "F3_candidate_class_evaluated": adjudication_valid,
        "atemporal_Krylov_filtration_proved": filtration_valid,
        "ordered_trace_antisymmetry_identity_proved": trace_identity_valid,
        "static_F2_only_route_rejected_as_F3_realization": bool(
            adjudication_valid and falsifier_met
        ),
        "new_dynamic_candidate_required": bool(adjudication_valid and falsifier_met),
        "F3_internal_order_or_causality_proved": causal,
        "physical_time_or_clock_readout_proved": False,
        "persistence_memory_or_signal_propagation_proved": False,
        "F4_independent_additive_modes_proved": False,
        "foundation_to_effective_closed": False,
        "W2_M1_dimension_or_continuum_proved": False,
        "W2_M2_Lorentzian_metric_proved": False,
        "effective_action_or_matter_coupling_proved": False,
        "Einstein_GR_PN_or_PPN_bridge_proved": False,
        "observational_validation_proved": False,
    }


def decision_controls(
    w217: ModuleType, gates: dict[str, bool], screen: dict[str, bool],
    closure: dict[str, bool], falsifier_met: bool,
) -> dict[str, bool]:
    forced_all_true = {key: True for key in w217.frozen_f3_gate_keys()}
    forced_maps = w217.candidate_map_fixture("DERIVED")
    forced_screen = w217.candidate_screen(forced_all_true, forced_maps)
    missing = dict(gates)
    missing.pop(next(iter(missing)))
    return {
        "actual_F3_gate_map_valid_but_ineligible": all((
            screen["valid"], not screen["eligible"], not screen["promoted"]
        )),
        "all_true_synthetic_map_still_not_self_promoted": all((
            forced_screen["valid"], forced_screen["eligible"], not forced_screen["promoted"]
        )),
        "malformed_actual_map_fails_closed": not w217.candidate_screen(
            missing, STATIC_CANDIDATE_MAPS
        )["valid"],
        "synthetic_eligibility_cannot_authorize_this_static_route": all((
            forced_screen["eligible"],
            forced_screen["promoted"] is False,
            STATIC_ROUTE_F3_PROMOTION_AUTHORIZED is False,
            not closure["F3_internal_order_or_causality_proved"],
        )),
        "frozen_static_causal_falsifier_met": falsifier_met,
        "closure_matches_predeclared_result_exactly": closure == EXPECTED_CLOSURE_FLAGS,
        "positive_algebraic_result_and_negative_causal_result_separated": all((
            closure["atemporal_Krylov_filtration_proved"],
            closure["ordered_trace_antisymmetry_identity_proved"],
            not closure["F3_internal_order_or_causality_proved"],
        )),
        "candidate_rejection_does_not_reject_new_dynamics": all((
            closure["static_F2_only_route_rejected_as_F3_realization"],
            closure["new_dynamic_candidate_required"],
            CLAIM_CONTRACT["BRANCHES"]["new_foundation_derived_dynamic_candidate"]
            == "OPEN_NEW_VERSION_REQUIRED",
        )),
    }


def run() -> dict[str, Any]:
    dependency, _w216, w217 = dependency_controls()
    controls = {
        "dependency": dependency,
        "filtration": filtration_controls(),
        "equivariance": equivariance_controls(),
        "nulls": null_controls(),
        "graph_controls": graph_control_tests(),
        "transpose_involution_no_go": transpose_involution_no_go_controls(),
        "reciprocal_gradient_no_go": reciprocal_gradient_controls(),
    }
    group_valid = {
        "dependency": exact_true_map(controls["dependency"], DEPENDENCY_CONTROL_KEYS),
        "filtration": exact_true_map(controls["filtration"], FILTRATION_CONTROL_KEYS),
        "equivariance": exact_true_map(controls["equivariance"], EQUIVARIANCE_CONTROL_KEYS),
        "nulls": exact_true_map(controls["nulls"], NULL_CONTROL_KEYS),
        "graph_controls": exact_true_map(controls["graph_controls"], GRAPH_CONTROL_KEYS),
        "transpose_involution_no_go": exact_true_map(
            controls["transpose_involution_no_go"], TRANSPOSE_CONTROL_KEYS
        ),
        "reciprocal_gradient_no_go": exact_true_map(
            controls["reciprocal_gradient_no_go"], GRADIENT_CONTROL_KEYS
        ),
    }
    evidence_valid = exact_true_map(group_valid, CONTROL_GROUP_KEYS)
    gates = causal_gate_map(
        dependency, w217, controls["transpose_involution_no_go"], controls["graph_controls"],
        controls["equivariance"], controls["nulls"],
    )
    screen = w217.candidate_screen(gates, STATIC_CANDIDATE_MAPS)
    falsifier_met = bool(
        controls["transpose_involution_no_go"]
        ["reflection_implements_R_C_sign_and_A_transpose_involution"]
        and dependency["w2_16_has_no_dynamic_maps_and_kept_F3_false"]
        and all(
            STATIC_CANDIDATE_MAPS[key]["status"] == "ABSENT"
            for key in (
                "event_or_change_map",
                "transition_or_response_law",
                "signal_support_or_update_composition",
                "allowed_interventions",
                "intervention_to_response_map",
                "direct_influence_relation",
                "forbidden_pairs",
                "no_transmission_test",
            )
        )
    )
    predecessors_valid = group_valid["dependency"]
    filtration_valid = all((
        predecessors_valid,
        group_valid["filtration"],
        group_valid["equivariance"],
        group_valid["nulls"],
    ))
    trace_identity_valid = all((
        predecessors_valid,
        group_valid["filtration"],
        controls["filtration"].get("ordered_trace_antisymmetry_identity_exact") is True,
        controls["filtration"].get("canonical_state_has_required_split_and_invariants") is True,
    ))
    closure = closure_decision(
        predecessors_valid,
        filtration_valid,
        trace_identity_valid,
        evidence_valid,
        screen,
        falsifier_met,
    )
    decisions = decision_controls(w217, gates, screen, closure, falsifier_met)
    valid = bool(
        evidence_valid and exact_true_map(decisions, DECISION_CONTROL_KEYS)
    )
    return {
        "artifact": CLAIM_CONTRACT["CLAIM_ID"],
        "valid": valid,
        "claim": CLAIM_CONTRACT["CLAIM"],
        "candidate_status": "REJECTED_STATIC_ROUTE_AS_F3_REALIZATION" if valid else "INVALID",
        "program_status": "W2_F3_OPEN_REQUIRES_NEW_FOUNDATION_DYNAMICS",
        "conclusion": (
            "The current F2 state exactly yields the declared target-free O(3)-equivariant "
            "atemporal Krylov filtration V0<V1<V2 on J>0 and 0<tau<1; another distinct static "
            "equivariant flag also exists, so uniqueness is not claimed. F3 remains open because "
            "the inherited law supplies no events, transition, intervention, signal, or "
            "no-transmission map. A~A^T additionally blocks only a transpose-odd static scalar "
            "arrow; it is not a physical time-reversal theorem."
        ),
        "exact_rank_certificates": {
            "e2_G1": "J*tau/2",
            "det_G2": "J^3*tau^2*(1-tau)/8",
            "rank_pattern": [1, 2, 3],
        },
        "causal_falsifier_met": falsifier_met,
        "candidate_maps": STATIC_CANDIDATE_MAPS,
        "f3_gate_map": gates,
        "f3_screen": screen,
        "closure_decision": closure,
        "controls": controls,
        "control_group_validity": group_valid,
        "decision_controls": decisions,
    }


def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_CONTRACT.get("CLAIM_ID", "unknown"),
            "valid": False,
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(_json_safe(report), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
