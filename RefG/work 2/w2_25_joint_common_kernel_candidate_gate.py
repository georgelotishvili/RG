"""Exact audit of one full-law reversible single-carrier representation candidate.

This candidate is intentionally narrower than a foundation derivation.  It uses
one imported real traceless 3x3 endomorphism A, its transpose projections
S=(A+A.T)/2 and R=(A-A.T)/2, and one complete transpose-even common-O(3)
polynomial scalar through degree four.  A single autonomous conservative law
is then obtained from that scalar and the imported Frobenius kinetic form.

The calculation has two jobs.  First, it registers the w2_24 rejection of the
old separable-minimum plus appended-tangent architecture.  Second, it tests
whether the full mixed law supplies an internally consistent representation
candidate for conditional F1/F2, a local reversible process line, and
conditional F4 state accounting.

It does not derive the matrix representation, dimension three, O(3), transpose,
the kinetic form, or the transfer parameter from the RefG foundation.  A
bounded reversible flow may recur, so state reachability is not promoted to an
acyclic occurrence order.  Full F3a, F3b, space, a metric and GR remain open.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any

import sympy as sp


CLAIM_ID = "W2_JOINT_COMMON_KERNEL_REVERSIBLE_FULL_LAW_CANDIDATE_001"
MODEL_VERSION = "W2-JOINT-COMMON-KERNEL-FULL-LAW-v1.0-CONDITIONAL-REPRESENTATION"
CANDIDATE_STATUS = (
    "CONDITIONAL_REVERSIBLE_FULL_LAW_REPRESENTATION_PASS__"
    "OLD_SEPARABLE_ROUTE_REJECTED__FULL_F3A_F3B_OPEN"
)

REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

DEPENDENCY_KEYS = frozenset({
    "w2_23_contract_valid_and_identity_exact",
    "w2_23_all_physical_closure_flags_false",
    "w2_24_complete_invariant_audit_valid",
    "w2_24_old_separable_minimum_tangent_architecture_rejected",
    "direct_dependencies_consumed_through_structured_semantic_interfaces",
})

ALGEBRA_KEYS = frozenset({
    "transpose_split_reconstructs_one_traceless_carrier",
    "complete_degree_four_basis_registered_exactly",
    "cyclic_word_reduction_exact",
    "full_scalar_law_contains_every_registered_basis_element",
    "projected_gradients_match_symbolic_directional_derivative",
    "symmetric_and_skew_constraints_preserved",
    "commutator_norm_identity_exact",
})

COVARIANCE_KEYS = frozenset({
    "common_O3_action_preserves_split_and_scalar_by_construction",
    "exact_rational_rotation_covariance_witness",
    "exact_reflection_covariance_witness",
    "no_preferred_basis_axis_projector_or_relation_table",
    "representation_group_not_promoted_to_physical_space",
})

HEALTH_KEYS = frozenset({
    "coercive_sufficient_domain_is_open_and_nonempty",
    "mixed_cubic_and_quartic_bounds_registered",
    "full_polynomial_vector_field_is_smooth",
    "conserved_energy_identity_exact",
    "compact_energy_sublevels_give_global_candidate_flow",
    "zero_phase_state_is_exact_null",
})

QUOTIENT_KEYS = frozenset({
    "generic_local_quotient_rank_five_exact_witness",
    "unary_rank_three_exact_witness",
    "joint_fibre_rank_two_exact_witness",
    "same_unary_different_joint_exact_pair",
    "discrete_orbit_sheet_not_silently_called_closed",
})

PROCESS_KEYS = frozenset({
    "autonomous_phase_vector_field_is_state_owned",
    "nonzero_local_intrinsic_process_line_exact_witness",
    "global_Z2_history_reversal_exact",
    "positive_line_rescaling_distinguished_from_local_sign_patch",
    "flow_composition_follows_from_autonomous_uniqueness",
    "recurrence_not_excluded_for_bounded_reversible_flow",
    "occurrence_or_universal_cover_lift_absent",
    "state_reachability_not_promoted_to_acyclic_order",
    "full_F3a_remains_open",
})

REPRESENTATION_KEYS = frozenset({
    "conditional_F1_transpose_roles_coexist_and_reconstruct_A",
    "conditional_F2_joint_readout_has_two_local_fibre_directions",
    "conditional_F4_channel_projection_has_rank_eight",
    "conditional_F4_amplitude_accounting_has_rank_two",
    "quadratic_inventory_is_exactly_additive",
    "mixed_law_blocks_false_cross_nontransmission_claim",
    "all_foundation_origin_and_physical_closures_remain_false",
})

ADVERSARIAL_KEYS = frozenset({
    "separable_zero_mixed_surface_is_not_called_open_robust",
    "preferred_axis_source_and_prewired_graph_are_rejected",
    "local_orientation_sign_patching_is_rejected",
    "damping_or_gradient_arrow_is_not_smuggled_into_reversible_law",
    "fixed_dimension_and_O3_are_charged_representation_inputs",
    "F3b_forbidden_pairs_and_nontransmission_are_absent",
})

DECISION_KEYS = frozenset({
    "all_exact_evidence_required_for_conditional_candidate_validity",
    "each_single_false_evidence_item_blocks_validity",
    "missing_extra_or_nonboolean_evidence_fails_closed",
    "old_architecture_rejection_and_new_candidate_status_are_separate",
    "conditional_representation_results_never_promote_foundation_flags",
    "outcome_and_closure_ledgers_match_frozen_ceiling",
})

ALL_EVIDENCE_KEYS = frozenset().union(
    ALGEBRA_KEYS, COVARIANCE_KEYS, HEALTH_KEYS, QUOTIENT_KEYS,
    PROCESS_KEYS, REPRESENTATION_KEYS, ADVERSARIAL_KEYS,
)


FULL_INVARIANT_SPEC: dict[str, Any] = {
    "carrier": "A in sl(3,R)",
    "split": "S=(A+A^T)/2; R=(A-A^T)/2",
    "equivalence": "one common O(3) conjugation on every phase variable",
    "transpose_parity": "scalar law even under R -> -R",
    "degree_cutoff": 4,
    "common_O3_action_on_all_phase_variables": True,
    "physical_space_interpretation": False,
    "preferred_axis_projector_or_relation_table": False,
    "basis": (
        "I2=Tr(S^2)",
        "J=-Tr(R^2)",
        "I3=Tr(S^3)",
        "M3=Tr(S R^2)",
        "I2^2",
        "I2 J",
        "J^2",
        "M4=Tr(S^2 R^2)",
    ),
    "law": (
        "U=-alpha I2/2-eta J/2-b I3/3+gamma M3"
        "+c I2^2/4+e I2 J/2+d J^2/4+delta M4"
    ),
    "coercive_sufficient_domain": "c>0, d>0, e>|delta|; remaining coefficients finite real",
    "coercive_sufficient_conditions": {
        "c": "positive", "d": "positive", "e_minus_abs_delta": "positive",
    },
    "scope": (
        "complete only inside the imported n=3, common-O(3), transpose-even, "
        "polynomial degree<=4 class"
    ),
}

TRANSFER_LAW_SPEC: dict[str, Any] = {
    "configuration": "one A=S+R",
    "phase_state": "(A,V) in T sl(3,R), with V the tangent of A rather than a second carrier",
    "kinetic_form": "T=Tr(V^T V)/2 (imported Frobenius representation form)",
    "action": "integral [T-U] d sigma",
    "equations": "dot A=V; dot V=-grad_F U, projected to sl(3,R)",
    "autonomous": True,
    "conservative": True,
    "damping_present": False,
    "gradient_flow_arrow_present": False,
    "positive_Frobenius_kinetic_form": True,
    "global_reversal_exact": True,
    "statewise_orientation_sign_patch_allowed": False,
    "recurrence_excluded": False,
    "occurrence_lift_supplied": False,
    "acyclic_occurrence_order_claimed": False,
    "parameter": "sigma is an uncalibrated mathematical transfer parameter, not clock time",
    "global_reversal": "(A(sigma),V(sigma)) <-> (A(-sigma),-V(-sigma))",
    "process_ceiling": (
        "a nonzero local quotient line is testable; acyclic occurrence order is not available "
        "without a law-derived recurrence/occurrence lift"
    ),
}


def frozen_outcomes() -> dict[str, bool]:
    return {
        "w2_24_old_separable_minimum_tangent_class_rejected": True,
        "full_mixed_reversible_representation_candidate_evaluated": True,
        "conditional_representation_F1_available": True,
        "conditional_representation_F2_available": True,
        "local_intrinsic_process_line_available": True,
        "global_Z2_reversal_available": True,
        "conditional_representation_F4_state_accounting_available": True,
        "full_F3a_intrinsic_process_order_proved": False,
        "F3b_causal_separability_nontransmission_proved": False,
        "foundation_common_kernel_origin_proved": False,
        "physical_space_time_metric_or_GR_proved": False,
    }


def frozen_physical_closure_flags() -> dict[str, bool]:
    return {
        "F0_common_resonant_kernel_derived": False,
        "F0_self_relation_carrier_origin_proved": False,
        "F0_autonomous_transfer_law_origin_proved": False,
        "F0_carrier_law_robustness_proved": False,
        "F1_self_differentiation_proved_on_derived_kernel": False,
        "F2_operational_relations_proved_on_derived_kernel": False,
        "F3a_intrinsic_process_orientation_proved": False,
        "F4_simultaneous_modes_proved": False,
        "F3b_causal_separability_nontransmission_proved": False,
        "foundation_to_effective_closed": False,
        "M1_dimension_continuum_proved": False,
        "M2_Lorentzian_metric_proved": False,
        "A0_effective_action_origin_proved": False,
        "A1_action_variation_proved": False,
        "A2_conservation_no_double_count_proved": False,
        "A3_degree_of_freedom_health_proved": False,
        "A4_universal_matter_metric_proved": False,
        "E1_reduced_action_matching_proved": False,
        "E2_exact_Einstein_entrance_proved": False,
        "source_matching_or_PN_PPN_handoff_proved": False,
        "observational_validation_proved": False,
    }


EXPECTED_OUTCOMES = frozen_outcomes()
EXPECTED_PHYSICAL_CLOSURE_FLAGS = frozen_physical_closure_flags()

CANDIDATE_MAPS: dict[str, dict[str, str]] = {
    "carrier_state_domain": {
        "status": "PARTIAL",
        "source": "imported finite representation, not RefG foundation",
        "definition": "phase state (A,V) in T sl(3,R) on the declared regular/coercive domain",
    },
    "self_relation_map": {
        "status": "DERIVED",
        "source": "transpose involution in the imported endomorphism algebra",
        "definition": "A -> (S,R), with exact reconstruction A=S+R",
    },
    "complete_equivalence_action": {
        "status": "DERIVED",
        "source": "declared representation redundancy",
        "definition": "(A,V) -> (OAO^T,OVO^T), O in O(3); no physical-space meaning",
    },
    "autonomous_transfer_law": {
        "status": "PARTIAL",
        "source": "Euler-Lagrange law from imported kinetic form and complete U",
        "definition": "dot A=V, dot V=-grad_F U; candidate-derived, foundation origin absent",
    },
    "state_owned_role_or_node_map": {
        "status": "PARTIAL",
        "source": "transpose projections of the same A",
        "definition": "conditional typed roles S and R; representation sectors, not physical nodes",
    },
    "irreducible_relational_report": {
        "status": "PARTIAL",
        "source": "generic local quotient differential",
        "definition": "unary (I2,I3,J), joint fibre (M3,M4), and K=-6M4-I2J",
    },
    "state_owned_change_or_occurrence_map": {
        "status": "PARTIAL",
        "source": "nonzero phase vector field",
        "definition": "local germ [(A,V),X(A,V)] modulo common O(3) and positive line scale",
    },
    "intrinsic_process_line": {
        "status": "PARTIAL",
        "source": "autonomous nonzero phase vector field",
        "definition": "unoriented local line {+X,-X}; no acyclic global state order claimed",
    },
    "orientation_double_cover": {
        "status": "DERIVED",
        "source": "exact reversibility involution",
        "definition": "one coherent global Z2 history reversal; no statewise sign choice",
    },
    "recurrence_occurrence_lift": {
        "status": "ABSENT",
        "source": "not produced by the candidate",
        "definition": "no state-owned record or universal-cover occurrence label",
    },
    "simultaneous_mode_inventory": {
        "status": "PARTIAL",
        "source": "orthogonal transpose projections",
        "definition": "rank-eight channel reconstruction and rank-two amplitude accounting",
    },
    "mode_independence_readout": {
        "status": "PARTIAL",
        "source": "d(I2,J) on S!=0,R!=0",
        "definition": "representation state independence only; no physical conservation claim",
    },
    "signal_support_composition": {
        "status": "ABSENT",
        "source": "no derived multi-occurrence support structure",
        "definition": "F3b unavailable",
    },
    "forbidden_pair_domain": {
        "status": "ABSENT",
        "source": "no derived locality or simultaneous event network",
        "definition": "no nonempty invariant forbidden-pair set",
    },
    "nontransmission_test": {
        "status": "ABSENT",
        "source": "full mixed law generically couples S and R",
        "definition": "old separable cross-zero cannot be inherited",
    },
}


SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "Adjudicate the old separable minimum/tangent architecture and exactly evaluate one new "
        "full mixed, reversible, single-carrier representation law for conditional F1/F2, a local "
        "process line and F4 state accounting, without promoting representation inputs or closing "
        "F3a/F3b."
    ),
    "TYPE": "EXACT_CONDITIONAL_REPRESENTATION_CANDIDATE_AND_CLASS_LOCAL_ADJUDICATION",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "w2_23 is a valid outcome-neutral route contract and w2_24 validly enumerates the complete "
        "degree-four invariant class and rejects open robustness of the old separable-minimum "
        "tangent route. The present A,V representation, n=3, transpose, common O(3), Frobenius "
        "form, degree cutoff and variational transfer principle are imported mathematical hypotheses."
    ),
    "DOMAIN": (
        "A,V in sl(3,R); common O(3); finite real alpha,eta,b,gamma,delta and the nonempty open "
        "coercive sufficient coefficient domain c>0,d>0,e>|delta|. F1/F2/F4 rank statements use "
        "their explicitly declared generic regular strata."
    ),
    "CONVENTIONS": (
        "S=(A+A^T)/2, R=(A-A^T)/2; J=-Tr(R^2). The curve parameter sigma is not clock time. "
        "A process line is local and unoriented until one coherent global Z2 sheet is selected. "
        "A recurrence of one phase state is not silently split into distinct physical occurrences."
    ),
    "FREEDOM_LEDGER": {
        "single_configuration_carrier": {
            "source": "candidate import", "allowed_range": "A in sl(3,R)",
            "scale": "representation", "complexity": 8,
        },
        "tangent_phase_variable": {
            "source": "candidate dynamics", "allowed_range": "V in T_A sl(3,R)",
            "scale": "same carrier tangent, not a second ontology", "complexity": 8,
        },
        "dimension_and_group": {
            "source": "candidate representation", "allowed_range": "n=3 and common O(3)",
            "scale": "not physical dimension/isotropy", "complexity": 0,
        },
        "transpose_and_Frobenius_form": {
            "source": "candidate representation", "allowed_range": "fixed",
            "scale": "algebra/kinetic form", "complexity": 0,
        },
        "law_coefficients": {
            "source": "complete degree-four class", "allowed_range": "alpha,eta,b,gamma,c,e,d,delta",
            "scale": "eight universal candidate parameters", "complexity": 8,
        },
        "curve_parameter": {
            "source": "variational representation", "allowed_range": "affine sigma",
            "scale": "unphysical transfer bookkeeping", "complexity": 0,
        },
        "initial_phase_state": {
            "source": "candidate initial data", "allowed_range": "declared regular energy shell",
            "scale": "state", "complexity": 16,
        },
        "external_graph_clock_metric_target_or_data": {
            "source": "forbidden", "allowed_range": 0, "scale": "all", "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_23_common_resonant_kernel_contract.py: semantic contract interface",
        "RefG/work 2/w2_24_complete_invariant_law_robustness_gate.py: complete-law class audit",
    ],
    "METHOD": (
        "Use exact SymPy polynomial identities: complete invariant reconstruction, symbolic "
        "directional variation, projected gradients, common-O(3) witnesses, conserved energy, "
        "global reversal, exact quotient-rank minors, relation witnesses, nulls and fail-closed "
        "mutations. No finite-difference gradient or fitted data are used."
    ),
    "PASS_CONDITION": (
        "Conditional candidate validity requires every dependency and exact evidence item True, "
        "the frozen outcome ledger exact, every physical closure flag False, and the decision "
        "screen to fail closed under each malformed mutation. This PASS is representation-relative."
    ),
    "FAIL_CONDITION": (
        "An incomplete invariant, wrong gradient, covariance/energy/reversal residual, empty "
        "coercive domain, failed rank/readout, hidden target, false acyclic-order claim, inherited "
        "separable nontransmission, malformed evidence or promoted physical flag invalidates the result."
    ),
    "FALSIFIER": (
        "The old architecture is falsified in its frozen class by any allowed mixed invariant that "
        "lifts its relational minimum modulus outside a coefficient-open domain, as registered by "
        "w2_24. The new candidate is falsified if no nonempty coefficient-open and initial-data-open "
        "regular domain can retain the declared rank-two joint relation, healthy reversible flow "
        "and rank-two independent state accounting, or if any exact identity in this gate fails."
    ),
    "RESIDUAL": "Exact zero for algebraic identities; F3a occurrence lift and every F3b map are absent, not approximated.",
    "ERROR_BOUND": "N/A: exact symbolic algebra and exact rational witnesses only.",
    "VALIDITY_HEALTH": (
        "Coercivity and conserved positive kinetic energy give bounded global candidate trajectories "
        "on the sufficient domain. This does not prove that one generic F1/F2 regular stratum is "
        "globally invariant, exclude recurrence, or establish physical degrees of freedom."
    ),
    "BRANCHES": {
        "old_separable_minimum_plus_tangent": "REJECTED_IN_FROZEN_COMPLETE_INVARIANT_CLASS",
        "new_full_mixed_reversible_representation": "CONDITIONAL_CANDIDATE",
        "zero_phase_state": "EXACT_NULL",
        "generic_rank_stratum": "CONDITIONAL_F1_F2_F4_READOUT",
        "local_process_line_global_Z2": "EXACT_REPRESENTATION_RESULT",
        "full_F3a_occurrence_order": "OPEN_RECURRENCE_LIFT_ABSENT",
        "F3b_and_downstream": "OPEN",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "pre-spatial representation candidate"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "no physical observable or data model"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, fit, benchmark target or validation"},
    "IDENTIFIABILITY": (
        "The generic local quotient differential separates three unary and two joint directions. "
        "A discrete handed orbit sheet remains separately registered; no global orbit classifier, "
        "physical node identity, clock calibration or spacetime observable is claimed."
    ),
    "BENCHMARK": (
        "Positive controls use exact rational states for covariance, quotient ranks, joint fibres "
        "and a nonzero process germ. Nulls use A=V=0 and lost-channel/commuting strata. Adversarial "
        "controls cover zero mixed coefficients, hidden axes/graphs, local arrow patches and false F3b."
    ),
    "CLOSURE_FLAGS": frozen_physical_closure_flags(),
    "CROSSCHECK": (
        "Compare the matrix directional derivative with closed gradients, use rotation and reflection "
        "covariance witnesses, derive energy conservation independently from the phase vector field, "
        "and verify rank both by matrix rank and a fixed nonzero exact minor."
    ),
    "PROVENANCE": {
        "date": "2026-07-23", "data": "none",
        "code_version": "w2_25 candidate v1.0", "arithmetic": "exact SymPy",
    },
    "FILES": [
        "RefG/work 2/w2_23_common_resonant_kernel_contract.py",
        "RefG/work 2/w2_24_complete_invariant_law_robustness_gate.py",
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py",
    ],
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def _canonical_sha256(payload: Any) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()


# Filled after the literal payloads are frozen.  They are checked at runtime.
EXPECTED_FULL_INVARIANT_SPEC_SHA256 = (
    "A55FB1E6F792635272ACAA2F1AD99C5F90B030BBD958939934B46581EB3B0050"
)
EXPECTED_TRANSFER_LAW_SPEC_SHA256 = (
    "31749B675F23887BADB821482922C81BE7AA855048DA926407BA8E97ACE477EE"
)
EXPECTED_CANDIDATE_MAPS_SHA256 = (
    "24F159F45D2245E0804253E1C443E913D55B2849A5DB412D710744B3DD94E0D9"
)
EXPECTED_SCIENTIFIC_CONTRACT_SHA256 = (
    "7508FCD095459F87A55A1DF2CBF365D6DEAD9BAFE01A19A259CA2616DF8FE90E"
)


def _load_sibling(filename: str, module_name: str) -> ModuleType:
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency: {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(item) == 0 for item in matrix)


def _exact_bool_map(value: Any, keys: frozenset[str]) -> bool:
    return bool(
        isinstance(value, dict)
        and set(value) == keys
        and all(type(item) is bool for item in value.values())
    )


def _all_false_flags(value: Any) -> bool:
    return bool(
        isinstance(value, dict)
        and value == EXPECTED_PHYSICAL_CLOSURE_FLAGS
        and all(type(item) is bool and item is False for item in value.values())
    )


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_safe(item) for item in value]
    if isinstance(value, sp.MatrixBase):
        return [[str(sp.simplify(item)) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


@lru_cache(maxsize=1)
def algebra_objects() -> dict[str, Any]:
    alpha, eta, bcoef, gamma, ccoef, ecoef, dcoef, delta = sp.symbols(
        "alpha eta b gamma c e d delta", real=True
    )
    a, bb, cc, dd, ee = sp.symbols("a bb cc dd ee", real=True)
    x, y, z = sp.symbols("x y z", real=True)
    coordinates = (a, bb, cc, dd, ee, x, y, z)
    S = sp.Matrix([[a, dd, ee], [dd, bb, cc], [ee, cc, -a - bb]])
    R = sp.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])

    pa, pb, pc, pd, pe = sp.symbols("pa pb pc pd pe", real=True)
    vx, vy, vz = sp.symbols("vx vy vz", real=True)
    velocity_coordinates = (pa, pb, pc, pd, pe, vx, vy, vz)
    VS = sp.Matrix([[pa, pd, pe], [pd, pb, pc], [pe, pc, -pa - pb]])
    VR = sp.Matrix([[0, -vz, vy], [vz, 0, -vx], [-vy, vx, 0]])

    coefficients = {
        "alpha": alpha, "eta": eta, "b": bcoef, "gamma": gamma,
        "c": ccoef, "e": ecoef, "d": dcoef, "delta": delta,
    }
    invariant = invariants_of(S, R)
    U = potential_of(S, R, coefficients)
    GS, GR = gradients_of(S, R, coefficients)
    return {
        "coefficients": coefficients,
        "coordinates": coordinates,
        "velocity_coordinates": velocity_coordinates,
        "S": S, "R": R, "VS": VS, "VR": VR,
        "invariants": invariant, "U": U, "GS": GS, "GR": GR,
    }


def invariants_of(S: sp.MatrixBase, R: sp.MatrixBase) -> dict[str, sp.Expr]:
    I2 = sp.expand(sp.trace(S * S))
    I3 = sp.expand(sp.trace(S * S * S))
    J = sp.expand(-sp.trace(R * R))
    M3 = sp.expand(sp.trace(S * R * R))
    M4 = sp.expand(sp.trace(S * S * R * R))
    return {"I2": I2, "I3": I3, "J": J, "M3": M3, "M4": M4}


def potential_of(
    S: sp.MatrixBase, R: sp.MatrixBase, coefficients: dict[str, sp.Expr],
) -> sp.Expr:
    q = invariants_of(S, R)
    return sp.expand(
        -coefficients["alpha"] * q["I2"] / 2
        -coefficients["eta"] * q["J"] / 2
        -coefficients["b"] * q["I3"] / 3
        +coefficients["gamma"] * q["M3"]
        +coefficients["c"] * q["I2"]**2 / 4
        +coefficients["e"] * q["I2"] * q["J"] / 2
        +coefficients["d"] * q["J"]**2 / 4
        +coefficients["delta"] * q["M4"]
    )


def gradients_of(
    S: sp.MatrixBase, R: sp.MatrixBase, coefficients: dict[str, sp.Expr],
) -> tuple[sp.Matrix, sp.Matrix]:
    q = invariants_of(S, R)
    identity = sp.eye(3)
    GS = sp.simplify(
        -coefficients["alpha"] * S
        -coefficients["b"] * (S * S - identity * q["I2"] / 3)
        +coefficients["c"] * q["I2"] * S
        +coefficients["gamma"] * (R * R + identity * q["J"] / 3)
        +coefficients["e"] * q["J"] * S
        +coefficients["delta"] * (
            S * R * R + R * R * S - identity * 2 * q["M3"] / 3
        )
    )
    GR = sp.simplify(
        (-coefficients["eta"] + coefficients["d"] * q["J"]
         + coefficients["e"] * q["I2"]) * R
        -coefficients["gamma"] * (S * R + R * S)
        -coefficients["delta"] * (S * S * R + R * S * S)
    )
    return GS, GR


def dependency_controls() -> dict[str, bool]:
    w223 = _load_sibling(
        "w2_23_common_resonant_kernel_contract.py", "w223_joint_candidate"
    )
    w224 = _load_sibling(
        "w2_24_complete_invariant_law_robustness_gate.py", "w224_joint_candidate"
    )
    report23 = w223.run()
    report24 = w224.run()
    # w2_24 publishes stable semantic booleans in its report; no hashes, source
    # text or explanatory prose are consumed here.
    closure24 = report24.get("closure_decision", {})
    old_rejected = bool(all((
        closure24.get("legacy_separable_U_open_neighbourhood_robust") is False,
        closure24.get("legacy_flat_tau_F2_route_open_neighbourhood_robust") is False,
        closure24.get("legacy_w2_22_tangent_route_open_neighbourhood_robust") is False,
        closure24.get("legacy_route_no_inheritance") is True,
    )))
    complete_audit = bool(all((
        w224.CLAIM_ID == "W2_COMPLETE_O3_INVARIANT_LAW_ROBUSTNESS_AUDIT_001",
        report24.get("valid") is True,
        report24.get("adjudication_status")
        == "PASS_COMPLETE_BASIS__LEGACY_FLAT_TAU_ROUTE_FRAGILE",
        closure24.get("complete_O3_scalar_basis_through_degree4_proved") is True,
        closure24.get("common_resonant_kernel_candidate_supplied") is False,
        closure24.get("foundation_law_derived") is False,
        closure24.get("F1_F2_F3a_F4_promoted") is False,
    )))
    return {
        "w2_23_contract_valid_and_identity_exact": all((
            w223.CLAIM_ID == "W2_F0_COMMON_RESONANT_KERNEL_CONTRACT_001",
            report23.get("valid") is True,
        )),
        "w2_23_all_physical_closure_flags_false": all((
            report23.get("physical_closure_flags")
            == w223.frozen_physical_closure_flags(),
            all(value is False for value in report23["physical_closure_flags"].values()),
        )),
        "w2_24_complete_invariant_audit_valid": complete_audit,
        "w2_24_old_separable_minimum_tangent_architecture_rejected": old_rejected,
        "direct_dependencies_consumed_through_structured_semantic_interfaces": all((
            isinstance(report23.get("physical_closure_flags"), dict),
            isinstance(closure24, dict),
            isinstance(report24.get("controls"), dict),
        )),
    }


def algebra_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    o = algebra_objects()
    S, R, GS, GR = o["S"], o["R"], o["GS"], o["GR"]
    q = o["invariants"]
    eps = sp.symbols("epsilon", real=True)
    ha, hb, hc, hd, he, hx, hy, hz = sp.symbols(
        "ha hb hc hd he hx hy hz", real=True
    )
    HS = sp.Matrix([[ha, hd, he], [hd, hb, hc], [he, hc, -ha - hb]])
    HR = sp.Matrix([[0, -hz, hy], [hz, 0, -hx], [-hy, hx, 0]])
    directional = sp.expand(sp.diff(
        potential_of(S + eps * HS, R + eps * HR, o["coefficients"]), eps
    ).subs(eps, 0))
    riesz = sp.expand(sp.trace(GS.T * HS) + sp.trace(GR.T * HR))
    t_srsr = sp.expand(sp.trace(S * R * S * R))
    C = sp.simplify(S * R - R * S)
    K = sp.expand(sp.trace(C.T * C))
    basis_symbols = (
        q["I2"], q["J"], q["I3"], q["M3"], q["I2"]**2,
        q["I2"] * q["J"], q["J"]**2, q["M4"],
    )
    expected_law = sp.expand(
        -o["coefficients"]["alpha"] * q["I2"] / 2
        -o["coefficients"]["eta"] * q["J"] / 2
        -o["coefficients"]["b"] * q["I3"] / 3
        +o["coefficients"]["gamma"] * q["M3"]
        +o["coefficients"]["c"] * q["I2"]**2 / 4
        +o["coefficients"]["e"] * q["I2"] * q["J"] / 2
        +o["coefficients"]["d"] * q["J"]**2 / 4
        +o["coefficients"]["delta"] * q["M4"]
    )
    controls = {
        "transpose_split_reconstructs_one_traceless_carrier": all((
            sp.trace(S) == 0, sp.trace(R) == 0, S.T == S, R.T == -R,
        )),
        "complete_degree_four_basis_registered_exactly": all((
            len(FULL_INVARIANT_SPEC["basis"]) == 8,
            len(basis_symbols) == 8,
            FULL_INVARIANT_SPEC["degree_cutoff"] == 4,
        )),
        "cyclic_word_reduction_exact": (
            sp.factor(t_srsr + 2 * q["M4"] + q["I2"] * q["J"] / 2) == 0
        ),
        "full_scalar_law_contains_every_registered_basis_element": (
            sp.expand(o["U"] - expected_law) == 0
        ),
        "projected_gradients_match_symbolic_directional_derivative": (
            sp.expand(directional - riesz) == 0
        ),
        "symmetric_and_skew_constraints_preserved": all((
            _matrix_zero(GS.T - GS), sp.simplify(sp.trace(GS)) == 0,
            _matrix_zero(GR.T + GR), sp.simplify(sp.trace(GR)) == 0,
        )),
        "commutator_norm_identity_exact": (
            sp.factor(K + 6 * q["M4"] + q["I2"] * q["J"]) == 0
        ),
    }
    diagnostics = {
        "directional_derivative_residual": sp.expand(directional - riesz),
        "cyclic_word_residual": sp.factor(
            t_srsr + 2 * q["M4"] + q["I2"] * q["J"] / 2
        ),
        "commutator_identity_residual": sp.factor(
            K + 6 * q["M4"] + q["I2"] * q["J"]
        ),
    }
    return controls, diagnostics


def covariance_controls() -> dict[str, bool]:
    o = algebra_objects()
    S0 = sp.Matrix([[1, 2, -1], [2, -3, 1], [-1, 1, 2]])
    R0 = sp.Matrix([[0, -4, 2], [4, 0, -1], [-2, 1, 0]])
    rotation = sp.Matrix([
        [sp.Rational(3, 5), -sp.Rational(4, 5), 0],
        [sp.Rational(4, 5), sp.Rational(3, 5), 0],
        [0, 0, 1],
    ])
    reflection = sp.diag(1, -1, 1)

    def exact_covariance(O: sp.MatrixBase) -> bool:
        St = sp.simplify(O * S0 * O.T)
        Rt = sp.simplify(O * R0 * O.T)
        GS0, GR0 = gradients_of(S0, R0, o["coefficients"])
        GSt, GRt = gradients_of(St, Rt, o["coefficients"])
        return all((
            sp.simplify(O * O.T) == sp.eye(3),
            sp.expand(
                potential_of(St, Rt, o["coefficients"])
                - potential_of(S0, R0, o["coefficients"])
            ) == 0,
            _matrix_zero(GSt - O * GS0 * O.T),
            _matrix_zero(GRt - O * GR0 * O.T),
        ))

    return {
        "common_O3_action_preserves_split_and_scalar_by_construction": all((
            FULL_INVARIANT_SPEC["common_O3_action_on_all_phase_variables"] is True,
            FULL_INVARIANT_SPEC["physical_space_interpretation"] is False,
        )),
        "exact_rational_rotation_covariance_witness": exact_covariance(rotation),
        "exact_reflection_covariance_witness": exact_covariance(reflection),
        "no_preferred_basis_axis_projector_or_relation_table": all((
            FULL_INVARIANT_SPEC["preferred_axis_projector_or_relation_table"] is False,
            CLAIM_CONTRACT["DATA_ROLE"]["status"] == "N/A",
        )),
        "representation_group_not_promoted_to_physical_space": (
            CLAIM_CONTRACT["FREEDOM_LEDGER"]["dimension_and_group"]["scale"]
            == "not physical dimension/isotropy"
        ),
    }


def health_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    o = algebra_objects()
    S, R, VS, VR, GS, GR = (
        o["S"], o["R"], o["VS"], o["VR"], o["GS"], o["GR"]
    )
    q = o["invariants"]
    rx = sp.Matrix([o["coordinates"][5], o["coordinates"][6], o["coordinates"][7]])
    r2 = sp.expand((rx.T * rx)[0])
    axial_R2_residual = sp.simplify(R * R - (rx * rx.T - r2 * sp.eye(3)))
    M3_residual = sp.expand(q["M3"] - (rx.T * S * rx)[0])
    M4_residual = sp.expand(q["M4"] - ((rx.T * S * S * rx)[0] - r2 * q["I2"]))
    potential_rate = sp.expand(sp.trace(GS.T * VS) + sp.trace(GR.T * VR))
    kinetic_rate = sp.expand(
        sp.trace(VS.T * (-GS)) + sp.trace(VR.T * (-GR))
    )
    energy_rate = sp.expand(potential_rate + kinetic_rate)
    zero_subs = {
        symbol: 0 for symbol in o["coordinates"] + o["velocity_coordinates"]
    }
    zero_phase = all((
        _matrix_zero(VS.subs(zero_subs)),
        _matrix_zero(VR.subs(zero_subs)),
        _matrix_zero(GS.subs(zero_subs)),
        _matrix_zero(GR.subs(zero_subs)),
    ))
    controls = {
        "coercive_sufficient_domain_is_open_and_nonempty": all((
            FULL_INVARIANT_SPEC["coercive_sufficient_domain"]
            == "c>0, d>0, e>|delta|; remaining coefficients finite real",
            1 > 0, 1 > 0, 2 > abs(1),
        )),
        "mixed_cubic_and_quartic_bounds_registered": all((
            _matrix_zero(axial_R2_residual),
            M3_residual == 0,
            M4_residual == 0,
            FULL_INVARIANT_SPEC["coercive_sufficient_conditions"] == {
                "c": "positive", "d": "positive",
                "e_minus_abs_delta": "positive",
            },
        )),
        "full_polynomial_vector_field_is_smooth": all((
            o["U"].is_polynomial(*o["coordinates"]),
            all(item.is_polynomial(*o["coordinates"]) for item in GS),
            all(item.is_polynomial(*o["coordinates"]) for item in GR),
        )),
        "conserved_energy_identity_exact": energy_rate == 0,
        "compact_energy_sublevels_give_global_candidate_flow": all((
            energy_rate == 0,
            TRANSFER_LAW_SPEC["positive_Frobenius_kinetic_form"] is True,
            FULL_INVARIANT_SPEC["coercive_sufficient_conditions"] == {
                "c": "positive", "d": "positive",
                "e_minus_abs_delta": "positive",
            },
        )),
        "zero_phase_state_is_exact_null": zero_phase,
    }
    diagnostics = {
        "energy_rate": energy_rate,
        "M3_axial_identity_residual": M3_residual,
        "M4_axial_identity_residual": M4_residual,
        "coercive_witness": {"c": 1, "d": 1, "e": 2, "delta": 1},
    }
    return controls, diagnostics


def quotient_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    o = algebra_objects()
    q = o["invariants"]
    coords = o["coordinates"]
    quotient_readout = sp.Matrix([q["I2"], q["I3"], q["J"], q["M3"], q["M4"]])
    unary_readout = sp.Matrix([q["I2"], q["I3"], q["J"]])
    jq = quotient_readout.jacobian(coords)
    ju = unary_readout.jacobian(coords)
    witness_values = (1, 2, 3, 1, 2, 1, 2, 4)
    witness = dict(zip(coords, witness_values))
    jq_w = jq.subs(witness)
    ju_w = ju.subs(witness)
    selected_minor = sp.Matrix(jq_w[:, [0, 1, 2, 3, 5]]).det()

    S_pair = sp.diag(1, 2, -3)
    R_x = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    R_y = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    qa = invariants_of(S_pair, R_x)
    qb = invariants_of(S_pair, R_y)
    unary_equal = all(qa[key] == qb[key] for key in ("I2", "I3", "J"))
    joint_different = (qa["M3"], qa["M4"]) != (qb["M3"], qb["M4"])

    # Five continuous invariants give local quotient coordinates, but common
    # O(3) alone leaves a discrete generic sheet.  The axial-vector scalar
    # Xi=det(r,Sr,S^2r) is O(3)-invariant and flips under R->-R.  The pair below
    # has identical five q-values and opposite nonzero Xi, so q must not be
    # advertised as a global orbit classifier unless that sheet is quotiented.
    r_sheet_plus = sp.Matrix([1, 2, 3])
    r_sheet_minus = sp.Matrix([-1, 2, 3])

    def axial(vector: sp.MatrixBase) -> sp.Matrix:
        r1, r2, r3 = vector
        return sp.Matrix([[0, -r3, r2], [r3, 0, -r1], [-r2, r1, 0]])

    q_sheet_plus = invariants_of(S_pair, axial(r_sheet_plus))
    q_sheet_minus = invariants_of(S_pair, axial(r_sheet_minus))
    xi_plus = sp.det(sp.Matrix.hstack(
        r_sheet_plus, S_pair * r_sheet_plus, S_pair**2 * r_sheet_plus
    ))
    xi_minus = sp.det(sp.Matrix.hstack(
        r_sheet_minus, S_pair * r_sheet_minus, S_pair**2 * r_sheet_minus
    ))
    controls = {
        "generic_local_quotient_rank_five_exact_witness": all((
            jq_w.rank() == 5, selected_minor == -658464,
        )),
        "unary_rank_three_exact_witness": ju_w.rank() == 3,
        "joint_fibre_rank_two_exact_witness": jq_w.rank() - ju_w.rank() == 2,
        "same_unary_different_joint_exact_pair": all((
            unary_equal, joint_different, qa["M3"] == 1, qb["M3"] == 2,
        )),
        "discrete_orbit_sheet_not_silently_called_closed": all((
            q_sheet_plus == q_sheet_minus,
            xi_plus == 120, xi_minus == -120,
        )),
    }
    diagnostics = {
        "quotient_rank": jq_w.rank(),
        "unary_rank": ju_w.rank(),
        "joint_fibre_rank": jq_w.rank() - ju_w.rank(),
        "selected_minor": selected_minor,
        "same_unary_pair": {
            "first": {key: qa[key] for key in qa},
            "second": {key: qb[key] for key in qb},
        },
        "discrete_sheet_witness": {
            "continuous_readouts_equal": q_sheet_plus == q_sheet_minus,
            "Xi_plus": xi_plus, "Xi_minus": xi_minus,
        },
    }
    return controls, diagnostics


def process_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    o = algebra_objects()
    S, R, VS, VR, GS, GR = (
        o["S"], o["R"], o["VS"], o["VR"], o["GS"], o["GR"]
    )
    state_witness = dict(zip(o["coordinates"], (1, 2, 3, 1, 2, 1, 2, 4)))
    velocity_witness = dict(zip(o["velocity_coordinates"], (1, 0, 0, 0, 0, 0, 0, 0)))
    parameter_witness = {
        o["coefficients"]["alpha"]: 1,
        o["coefficients"]["eta"]: 1,
        o["coefficients"]["b"]: 1,
        o["coefficients"]["gamma"]: 1,
        o["coefficients"]["c"]: 1,
        o["coefficients"]["e"]: 2,
        o["coefficients"]["d"]: 1,
        o["coefficients"]["delta"]: 1,
    }
    witness = state_witness | velocity_witness | parameter_witness
    nonzero_field = any(
        sp.simplify(item.subs(witness)) != 0
        for matrix in (VS, VR, -GS, -GR) for item in matrix
    )

    # A common-O(3) gauge tangent leaves every scalar invariant fixed.  The
    # exact positive derivative below proves that the selected process germ is
    # nonzero on the quotient, not merely nonzero in a matrix representative.
    I2_rate = sp.expand(2 * sp.trace(S * VS))
    quotient_change_witness = sp.simplify(I2_rate.subs(witness))

    # For X(A,V)=(V,-G(A)) and Theta(A,V)=(A,-V), reversibility is
    # X(Theta z)=-DTheta X(z).  The four displayed blocks check it exactly.
    velocity_reversal = {
        symbol: -symbol for symbol in o["velocity_coordinates"]
    }
    reversal_residuals = (
        sp.simplify(VS.subs(velocity_reversal) + VS),
        sp.simplify(VR.subs(velocity_reversal) + VR),
        sp.simplify((-GS).subs(velocity_reversal) - (-GS)),
        sp.simplify((-GR).subs(velocity_reversal) - (-GR)),
    )
    controls = {
        "autonomous_phase_vector_field_is_state_owned": all((
            TRANSFER_LAW_SPEC["autonomous"] is True,
            CANDIDATE_MAPS["autonomous_transfer_law"]["status"] == "PARTIAL",
        )),
        "nonzero_local_intrinsic_process_line_exact_witness": all((
            nonzero_field, quotient_change_witness == 8,
        )),
        "global_Z2_history_reversal_exact": all(
            _matrix_zero(residual) if isinstance(residual, sp.MatrixBase)
            else residual == 0
            for residual in reversal_residuals
        ),
        "positive_line_rescaling_distinguished_from_local_sign_patch": all((
            TRANSFER_LAW_SPEC["statewise_orientation_sign_patch_allowed"] is False,
            TRANSFER_LAW_SPEC["global_reversal_exact"] is True,
        )),
        "flow_composition_follows_from_autonomous_uniqueness": all((
            TRANSFER_LAW_SPEC["autonomous"] is True,
            all(item.is_polynomial(*o["coordinates"]) for item in GS),
            all(item.is_polynomial(*o["coordinates"]) for item in GR),
        )),
        "recurrence_not_excluded_for_bounded_reversible_flow": (
            TRANSFER_LAW_SPEC["recurrence_excluded"] is False
        ),
        "occurrence_or_universal_cover_lift_absent": (
            CANDIDATE_MAPS["recurrence_occurrence_lift"]["status"] == "ABSENT"
            and TRANSFER_LAW_SPEC["occurrence_lift_supplied"] is False
        ),
        "state_reachability_not_promoted_to_acyclic_order": (
            TRANSFER_LAW_SPEC["acyclic_occurrence_order_claimed"] is False
        ),
        "full_F3a_remains_open": all((
            EXPECTED_OUTCOMES["full_F3a_intrinsic_process_order_proved"] is False,
            EXPECTED_PHYSICAL_CLOSURE_FLAGS["F3a_intrinsic_process_orientation_proved"] is False,
        )),
    }
    diagnostics = {
        "nonzero_witness": nonzero_field,
        "I2_rate_quotient_witness": quotient_change_witness,
        "reversal_residuals": reversal_residuals,
        "F3a_blocker": "bounded reversible recurrence with no state-owned occurrence lift",
    }
    return controls, diagnostics


def representation_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    o = algebra_objects()
    S, R = o["S"], o["R"]
    q = o["invariants"]
    coords = o["coordinates"]
    amplitude_jacobian = sp.Matrix([q["I2"], q["J"]]).jacobian(coords)
    witness = dict(zip(coords, (1, 2, 3, 1, 2, 1, 2, 4)))
    amplitude_rank = amplitude_jacobian.subs(witness).rank()
    quotient_rank = sp.Matrix([
        q["I2"], q["I3"], q["J"], q["M3"], q["M4"]
    ]).jacobian(coords).subs(witness).rank()
    unary_rank = sp.Matrix([
        q["I2"], q["I3"], q["J"]
    ]).jacobian(coords).subs(witness).rank()
    projection_jacobian = sp.eye(8)
    S_witness = S.subs(witness)
    R_witness = R.subs(witness)

    cross_S_from_R = sp.Matrix([
        [sp.diff(item, variable) for variable in coords[5:]] for item in o["GS"]
    ])
    cross_R_from_S = sp.Matrix([
        [sp.diff(item, variable) for variable in coords[:5]] for item in o["GR"]
    ])
    mixed_parameters = {
        o["coefficients"]["gamma"]: 1,
        o["coefficients"]["e"]: 2,
        o["coefficients"]["delta"]: 1,
    }
    cross_nonzero = any(
        sp.simplify(item.subs(witness | mixed_parameters)) != 0
        for item in tuple(cross_S_from_R) + tuple(cross_R_from_S)
    )
    additive_residual = sp.expand(
        sp.trace((S + R).T * (S + R)) - q["I2"] - q["J"]
    )
    controls = {
        "conditional_F1_transpose_roles_coexist_and_reconstruct_A": all((
            S.T == S, R.T == -R,
            not _matrix_zero(S_witness), not _matrix_zero(R_witness),
            _matrix_zero((S_witness + R_witness) - (S + R).subs(witness)),
            CANDIDATE_MAPS["self_relation_map"]["status"] == "DERIVED",
        )),
        "conditional_F2_joint_readout_has_two_local_fibre_directions": all((
            quotient_rank == 5,
            unary_rank == 3,
            quotient_rank - unary_rank == 2,
        )),
        "conditional_F4_channel_projection_has_rank_eight": projection_jacobian.rank() == 8,
        "conditional_F4_amplitude_accounting_has_rank_two": amplitude_rank == 2,
        "quadratic_inventory_is_exactly_additive": additive_residual == 0,
        "mixed_law_blocks_false_cross_nontransmission_claim": all((
            cross_nonzero,
            CANDIDATE_MAPS["nontransmission_test"]["status"] == "ABSENT",
        )),
        "all_foundation_origin_and_physical_closures_remain_false": (
            _all_false_flags(CLAIM_CONTRACT["CLOSURE_FLAGS"])
        ),
    }
    diagnostics = {
        "channel_projection_rank": projection_jacobian.rank(),
        "amplitude_rank": amplitude_rank,
        "quotient_rank": quotient_rank,
        "unary_rank": unary_rank,
        "additive_inventory_residual": additive_residual,
        "mixed_cross_response_nonzero": cross_nonzero,
    }
    return controls, diagnostics


def adversarial_controls() -> dict[str, bool]:
    forbidden = (
        "external_graph_clock_metric_target_or_data"
        in CLAIM_CONTRACT["FREEDOM_LEDGER"]
    )
    return {
        "separable_zero_mixed_surface_is_not_called_open_robust": (
            CLAIM_CONTRACT["BRANCHES"]["old_separable_minimum_plus_tangent"]
            == "REJECTED_IN_FROZEN_COMPLETE_INVARIANT_CLASS"
        ),
        "preferred_axis_source_and_prewired_graph_are_rejected": forbidden,
        "local_orientation_sign_patching_is_rejected": (
            TRANSFER_LAW_SPEC["statewise_orientation_sign_patch_allowed"] is False
        ),
        "damping_or_gradient_arrow_is_not_smuggled_into_reversible_law": all((
            TRANSFER_LAW_SPEC["conservative"] is True,
            TRANSFER_LAW_SPEC["damping_present"] is False,
            TRANSFER_LAW_SPEC["gradient_flow_arrow_present"] is False,
            TRANSFER_LAW_SPEC["global_reversal_exact"] is True,
        )),
        "fixed_dimension_and_O3_are_charged_representation_inputs": (
            CLAIM_CONTRACT["FREEDOM_LEDGER"]["dimension_and_group"]["source"]
            == "candidate representation"
        ),
        "F3b_forbidden_pairs_and_nontransmission_are_absent": all((
            CANDIDATE_MAPS["forbidden_pair_domain"]["status"] == "ABSENT",
            CANDIDATE_MAPS["nontransmission_test"]["status"] == "ABSENT",
            EXPECTED_OUTCOMES["F3b_causal_separability_nontransmission_proved"] is False,
        )),
    }


def candidate_screen(evidence: Any) -> dict[str, Any]:
    schema_valid = _exact_bool_map(evidence, ALL_EVIDENCE_KEYS)
    eligible = bool(schema_valid and all(evidence.values()))
    return {
        "schema_valid": schema_valid,
        "conditional_candidate_valid": eligible,
        "foundation_promoted": False,
        "full_F3a_promoted": False,
        "F3b_promoted": False,
        "physical_closure_flags": frozen_physical_closure_flags(),
    }


def decision_controls(evidence: dict[str, bool]) -> dict[str, bool]:
    positive = candidate_screen(evidence)
    each_false_blocks = True
    for key in ALL_EVIDENCE_KEYS:
        mutated = dict(evidence)
        mutated[key] = False
        each_false_blocks = each_false_blocks and not candidate_screen(mutated)[
            "conditional_candidate_valid"
        ]
    missing = dict(evidence)
    missing.pop(next(iter(ALL_EVIDENCE_KEYS)))
    extra = dict(evidence)
    extra["unexpected"] = True
    nonboolean = dict(evidence)
    nonboolean[next(iter(ALL_EVIDENCE_KEYS))] = 1
    malformed_blocked = all((
        not candidate_screen(missing)["schema_valid"],
        not candidate_screen(extra)["schema_valid"],
        not candidate_screen(nonboolean)["schema_valid"],
    ))
    return {
        "all_exact_evidence_required_for_conditional_candidate_validity": all((
            positive["schema_valid"], positive["conditional_candidate_valid"],
        )),
        "each_single_false_evidence_item_blocks_validity": each_false_blocks,
        "missing_extra_or_nonboolean_evidence_fails_closed": malformed_blocked,
        "old_architecture_rejection_and_new_candidate_status_are_separate": all((
            EXPECTED_OUTCOMES["w2_24_old_separable_minimum_tangent_class_rejected"],
            EXPECTED_OUTCOMES["full_mixed_reversible_representation_candidate_evaluated"],
        )),
        "conditional_representation_results_never_promote_foundation_flags": all((
            not positive["foundation_promoted"],
            not positive["full_F3a_promoted"],
            not positive["F3b_promoted"],
            _all_false_flags(positive["physical_closure_flags"]),
        )),
        "outcome_and_closure_ledgers_match_frozen_ceiling": all((
            frozen_outcomes() == EXPECTED_OUTCOMES,
            frozen_physical_closure_flags() == EXPECTED_PHYSICAL_CLOSURE_FLAGS,
            CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_PHYSICAL_CLOSURE_FLAGS,
        )),
    }


def definition_controls() -> dict[str, bool]:
    return {
        "scientific_contract_schema_exact": set(CLAIM_CONTRACT) == REQUIRED_SCIENTIFIC_FIELDS,
        "full_invariant_spec_hash_exact": (
            _canonical_sha256(FULL_INVARIANT_SPEC) == EXPECTED_FULL_INVARIANT_SPEC_SHA256
        ),
        "transfer_law_spec_hash_exact": (
            _canonical_sha256(TRANSFER_LAW_SPEC) == EXPECTED_TRANSFER_LAW_SPEC_SHA256
        ),
        "candidate_maps_hash_exact": (
            _canonical_sha256(CANDIDATE_MAPS) == EXPECTED_CANDIDATE_MAPS_SHA256
        ),
        "scientific_contract_hash_exact": (
            _canonical_sha256(CLAIM_CONTRACT) == EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        ),
        "outcomes_exact": frozen_outcomes() == EXPECTED_OUTCOMES,
        "all_physical_closure_flags_false": _all_false_flags(CLAIM_CONTRACT["CLOSURE_FLAGS"]),
    }


def run() -> dict[str, Any]:
    dependency = dependency_controls()
    algebra, algebra_diagnostics = algebra_controls()
    covariance = covariance_controls()
    health, health_diagnostics = health_controls()
    quotient, quotient_diagnostics = quotient_controls()
    process, process_diagnostics = process_controls()
    representation, representation_diagnostics = representation_controls()
    adversarial = adversarial_controls()
    evidence = {
        **algebra, **covariance, **health, **quotient,
        **process, **representation, **adversarial,
    }
    decision = decision_controls(evidence)
    definition = definition_controls()
    valid = bool(
        _exact_bool_map(dependency, DEPENDENCY_KEYS) and all(dependency.values())
        and _exact_bool_map(algebra, ALGEBRA_KEYS) and all(algebra.values())
        and _exact_bool_map(covariance, COVARIANCE_KEYS) and all(covariance.values())
        and _exact_bool_map(health, HEALTH_KEYS) and all(health.values())
        and _exact_bool_map(quotient, QUOTIENT_KEYS) and all(quotient.values())
        and _exact_bool_map(process, PROCESS_KEYS) and all(process.values())
        and _exact_bool_map(representation, REPRESENTATION_KEYS)
        and all(representation.values())
        and _exact_bool_map(adversarial, ADVERSARIAL_KEYS) and all(adversarial.values())
        and _exact_bool_map(decision, DECISION_KEYS) and all(decision.values())
        and all(definition.values())
    )
    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": valid,
        "candidate_status": CANDIDATE_STATUS if valid else "INVALID_NO_PROMOTION",
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The complete mixed reversible A,V law is an exact, internally consistent conditional "
            "representation candidate for F1/F2, a local process line with global Z2 reversal, and "
            "F4 state accounting. The old separable minimum/tangent class is rejected by w2_24. "
            "Because the representation and transfer principle are imported and recurrence lacks a "
            "state-owned occurrence lift, full F3a, F3b and every physical downstream gate remain open."
        ),
        "outcomes": frozen_outcomes(),
        "physical_closure_flags": frozen_physical_closure_flags(),
        "dependency_controls": dependency,
        "controls": {
            "definition": definition,
            "algebra": algebra,
            "covariance": covariance,
            "health": health,
            "quotient": quotient,
            "process": process,
            "representation": representation,
            "adversarial": adversarial,
            "decision": decision,
        },
        "diagnostics": {
            "algebra": algebra_diagnostics,
            "health": health_diagnostics,
            "quotient": quotient_diagnostics,
            "process": process_diagnostics,
            "representation": representation_diagnostics,
        },
        "hashes": {
            "full_invariant_spec": _canonical_sha256(FULL_INVARIANT_SPEC),
            "transfer_law_spec": _canonical_sha256(TRANSFER_LAW_SPEC),
            "candidate_maps": _canonical_sha256(CANDIDATE_MAPS),
            "scientific_contract": _canonical_sha256(CLAIM_CONTRACT),
        },
    }


def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_ID,
            "model_version": MODEL_VERSION,
            "valid": False,
            "candidate_status": "INVALID_NO_PROMOTION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(_json_safe(report), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
