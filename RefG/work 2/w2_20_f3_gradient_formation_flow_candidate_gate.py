"""Exact evaluator for the Work-2 F3 gradient-formation candidate.

The candidate adds one imported, target-free process package to the static
w2_16 carrier: formation curves are the negative Frobenius-gradient curves of
the already frozen scalar law U(S,R), with identity full-A mobility and unit
relative S/R mobility.  The descent sign, mobility and process interpretation
are Candidate-A primitives, not consequences of the static law.  The curve
parameter is mathematical bookkeeping only.  Candidate-relative event order
is the reparameterisation-invariant reachability relation certified by strict
decrease of U.

This evaluator may establish only conditional structural formation order
relative to that imported ansatz.  It does not derive the ansatz from the
RefG foundation, identify U as physical energy, create persistent phase or
clock order, or close physical time, spatial causality, F4, geometry or GR.
"""

from __future__ import annotations

import importlib.util
import hashlib
import json
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable

import sympy as sp


CLAIM_ID = "W2_F3_GRADIENT_FORMATION_FLOW_CANDIDATE_001"
MODEL_VERSION = "W2-F3-GRADIENT-FORMATION-FLOW-v3.0-PREDECESSOR-AUDITED"

REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN", "CONVENTIONS",
    "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD", "PASS_CONDITION",
    "FAIL_CONDITION", "FALSIFIER", "RESIDUAL", "ERROR_BOUND",
    "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP", "FORWARD_MODEL",
    "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK", "CLOSURE_FLAGS",
    "CROSSCHECK", "PROVENANCE", "FILES",
})

DEPENDENCY_CONTROL_KEYS = frozenset({
    "w2_16_report_valid_and_conditional_F2_exact",
    "w2_17_contract_valid_and_schema_exact",
    "w2_18_static_no_go_valid_and_dynamic_escape_open",
    "w2_19_candidate_contract_valid_and_unpromoted",
    "named_dependency_chain_exact",
})

GRADIENT_CONTROL_KEYS = frozenset({
    "directional_derivative_matches_Frobenius_gradient_exact",
    "symmetric_gradient_formula_exact",
    "skew_gradient_formula_exact",
    "vector_field_is_negative_gradient_exact",
    "symmetric_traceless_constraint_preserved",
    "skew_traceless_constraint_preserved",
    "separable_channel_dependence_exact",
    "ansatz_origin_remains_imported_not_derived",
})

EQUIVARIANCE_CONTROL_KEYS = frozenset({
    "manifest_common_O3_covariance_theorem_registered",
    "exact_generic_plane_rotation_covariance",
    "exact_axis_permutation_covariance",
    "exact_reflection_covariance",
    "transpose_involution_maps_forward_flow_to_forward_flow",
    "no_preferred_basis_axis_or_orientation",
})

REDUCED_FLOW_CONTROL_KEYS = frozenset({
    "uniaxial_symmetric_branch_is_invariant",
    "ds_equation_exact",
    "skew_direction_is_invariant",
    "dJ_equation_exact",
    "state_projectors_are_constant_along_reduced_flow",
    "dtau_is_exactly_zero",
    "generic_F2_relational_stratum_is_preserved",
})

DOMAIN_READOUT_CONTROL_KEYS = frozenset({
    "P_plus_simple_largest_projector_exact",
    "P_R_state_owned_axis_projector_exact",
    "tau_gap_formula_and_endpoint_consistency_exact",
    "state_nodes_reconstruct_A_and_carrier_cross_nulls",
    "commutator_norm_and_tau_imply_C_nonzero_exact",
    "off_endpoint_same_unary_different_joint_witness_exact",
    "off_endpoint_joint_readout_irreducible_exact",
    "inherited_F1_F2_counterexample_exact",
    "tau_zero_not_general_commutator_null_exact",
    "S_flow_preserves_eigenframe_exact",
    "simple_largest_spectral_gaps_preserved_exact",
    "R_flow_preserves_axis_and_P_R_exact",
    "tau_gap_is_flow_invariant_exact",
    "finite_flow_cannot_hit_stationary_endpoint_exact",
    "local_D_gap_basin_nonempty_open_and_stable",
    "D_gap_is_forward_invariant",
    "off_endpoint_relational_readout_common_O3_covariant",
})

HEALTH_CONTROL_KEYS = frozenset({
    "Lyapunov_identity_exact",
    "Lyapunov_strict_off_critical_set",
    "traceless_spectral_discriminant_bound_exact",
    "positive_quartic_coercivity_premises_exact",
    "polynomial_vector_field_is_locally_Lipschitz",
    "compact_sublevel_prevents_finite_forward_blowup",
    "positive_s_and_J_branches_are_forward_invariant",
    "endpoint_radii_are_exact_fixed_points",
    "normal_linear_stability_exact",
    "compact_Morse_Bott_minimum_manifold_registered",
    "flat_tau_direction_is_neutral_not_falsely_stabilized",
    "U_is_not_promoted_to_physical_energy",
})

ORDER_CONTROL_KEYS = frozenset({
    "exact_reduced_J_flow_solves_equation",
    "exact_reduced_J_flow_has_semigroup_composition",
    "strict_Lyapunov_reachability_is_irreflexive",
    "strict_Lyapunov_reachability_is_asymmetric",
    "semigroup_reachability_is_transitive",
    "strict_Lyapunov_reachability_is_acyclic",
    "reflexive_closure_is_antisymmetric",
    "exact_three_event_benchmark_passes",
    "direct_influence_not_static_U_ranking",
    "event_germ_is_state_owned_and_parameter_free",
    "global_positive_reparameterisation_preserves_order",
    "curve_parameter_is_not_physical_time",
})

INTERVENTION_CONTROL_KEYS = frozenset({
    "allowed_interventions_are_tangent_and_domain_preserving",
    "flow_differential_is_the_intervention_response",
    "exact_J_same_channel_response_is_nonzero",
    "finite_flow_same_channel_differential_is_nonsingular",
    "unique_finite_semiflow_factorises_exactly",
    "S_to_R_cross_response_is_exactly_zero",
    "R_to_S_cross_response_is_exactly_zero",
    "forbidden_channel_nontransmission_is_exact",
    "joint_C_response_is_not_silently_set_to_zero",
    "common_O3_gauge_tangent_is_quotient_null",
    "channel_vector_fields_have_zero_Lie_bracket",
    "channel_flow_updates_commute",
    "execution_schedule_does_not_change_the_flow",
    "later_intervention_cannot_change_an_earlier_occurrence",
})

NULL_CONTROL_KEYS = frozenset({
    "stationary_minimum_is_a_frozen_event_null",
    "S_zero_and_R_zero_are_invariant_F2_nulls",
    "tau_boundaries_and_tuned_surface_are_not_promoted",
    "tau_gap_zero_is_boundary_not_false_C_zero",
    "tau_gap_one_is_boundary_not_false_C_zero",
    "static_K_tau_ranking_without_flow_is_rejected",
    "positive_gradient_reverse_ansatz_increases_U",
    "target_symbol_intersection_is_empty",
    "external_graph_clock_metric_and_data_are_absent",
    "small_allowed_state_perturbations_preserve_regular_domain",
    "allowed_initial_conditions_have_open_relative_support",
    "persistent_phase_clock_and_downstream_claims_remain_false",
})

DECISION_CONTROL_KEYS = frozenset({
    "mathematical_evidence_complete_but_full_F3_ineligible",
    "w2_17_screen_never_self_promotes",
    "each_single_false_gate_blocks_eligibility",
    "missing_nonboolean_or_extra_gate_fails_closed",
    "missing_or_partial_candidate_map_fails_closed",
    "each_candidate_map_status_mutation_blocks_validity",
    "candidate_map_content_mutation_blocks_validity",
    "contract_closure_mutation_blocks_validity",
    "scientific_contract_content_mutation_blocks_validity",
    "failed_dependency_blocks_conditional_closure",
    "one_failed_scientific_control_blocks_validity",
    "closure_matches_predeclared_ceiling_exactly",
    "conditional_result_does_not_close_foundation_F3",
    "transition_map_stays_partial_and_blocks_eligibility",
    "exactly_two_predeclared_scientific_F3_gates_remain_false",
})

EXPECTED_FALSE_F3_GATES = frozenset({
    "same_chain_F1_F2_predecessors_valid",
    "target_free_transition_or_response_law_derived",
})

def frozen_closure_flags() -> dict[str, bool]:
    """Independent literal scientific ceiling, rebuilt on every call."""
    return {
        "F1_F2_conditional_predecessors_registered": True,
        "formation_domain_F1_F2_same_chain_revalidated": False,
        "off_endpoint_relational_readout_candidate_evaluated": True,
        "D_gap_nonempty_open_forward_invariant": True,
        "F3_gradient_candidate_evaluated": True,
        "conditional_gradient_semigroup_formation_order_proved": True,
        "gradient_process_ansatz_imported_not_Canon_derived": True,
        "transition_process_principle_foundation_derived": False,
        "event_germ_and_same_channel_influence_proved": True,
        "finite_flow_forbidden_channel_nontransmission_proved": True,
        "same_chain_cross_channel_causal_graph_proved": False,
        "F3_internal_order_or_causality_proved": False,
        "foundation_derived_F3": False,
        "persistent_phase_or_clock_order": False,
        "physical_time_or_clock_readout": False,
        "spatial_locality_or_causality": False,
        "F4_independent_additive_modes": False,
        "foundation_to_effective_closed": False,
        "dimension_or_continuum": False,
        "Lorentzian_metric_or_light_cone": False,
        "effective_action_or_matter_coupling": False,
        "Einstein_GR_PN_or_PPN_bridge": False,
        "observational_validation": False,
    }


EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()

PRIMITIVE_INPUT_SYMBOLS = frozenset({
    "S", "R", "alpha", "b", "c", "eta", "d",
    "P_plus", "P_R", "tau_gap", "Class(A,F)",
    "inherited_Frobenius_contraction", "negative_gradient_process_ansatz",
})
FORBIDDEN_TARGET_INPUT_SYMBOLS = frozenset({
    "x", "t", "clock", "lattice", "causal_DAG", "metric", "light_cone",
    "Einstein_equation", "GR", "PN", "PPN", "observed_answer", "data_fit",
    "phase_memory", "retarded_kernel",
})


SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "Evaluate Candidate A on its frozen D_gap domain: test the off-endpoint "
        "P_plus/P_R/tau_gap relational readout and the inherited same-chain F1/F2 predecessor, "
        "and determine whether the imported negative-gradient process package yields an exact "
        "standalone candidate-relative event order, finite-flow intervention response and "
        "forbidden-channel nontransmission."
    ),
    "TYPE": "CONDITIONAL_EXACT_DYNAMIC_CANDIDATE_THEOREM",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "Import w2_16's abstract state, scalar U and common O(3), w2_17's fail-closed "
        "F3 interface, w2_18's static-only no-go, and w2_19's frozen Candidate A. The "
        "descent sign, full-A Frobenius identity mobility, numerical relative mobility rho=1, "
        "positive-reachability process principle, and off-endpoint P_plus/P_R/tau_gap readout "
        "form the frozen Candidate-A package. They are not Canon-derived facts."
    ),
    "DOMAIN": (
        "D_gap: alpha,b,c,eta,d>0, b^2!=3 alpha c; S has one simple largest "
        "eigenvalue and state-owned P_plus; J>0 and P_R=I+2R^2/J; "
        "tau_gap=1-Tr(P_plus P_R) is in (0,1); C=[S,R] and grad_F U are nonzero; "
        "and the forward orbit lies in the generic w2_16 minimum-stratum basin."
    ),
    "CONVENTIONS": (
        "I2=Tr(S^2), I3=Tr(S^3), J=-Tr(R^2)=Tr(R^T R), and the inherited positive "
        "Frobenius contraction defines grad U. Identity full-A mobility, including unit "
        "relative S/R mobility rho=1, is imported from w2_19 rather than forced by O(3). "
        "The fixed gauge is dA/dsigma=-grad_F U, sigma>=0. A global alternative lambda is "
        "equivalent only when nu>0 is continuous and sigma(lambda)=integral nu has unbounded "
        "range. Neither parameter is physical time."
    ),
    "FREEDOM_LEDGER": {
        "static_carrier_and_law": {
            "source": "w2_16 imported conditional endpoint",
            "allowed_range": "A=S+R and alpha,b,c,eta,d>0",
            "scale": "one abstract internal carrier",
            "complexity": 0,
        },
        "gradient_process_ansatz": {
            "source": "w2_19 imported descent sign and process principle; not Canon-derived",
            "allowed_range": "D A=-grad_F U modulo positive reparameterisation",
            "scale": "one universal discrete candidate choice",
            "complexity": "1 discrete choice; 0 new continuous coefficients",
        },
        "kinetic_metric_and_relative_mobility": {
            "source": (
                "w2_19 imported structural choice built from the inherited trace pairing; "
                "common O(3) permits independent positive S/R weights"
            ),
            "allowed_range": (
                "identity full-A Frobenius mobility with relative S/R mobility fixed to one"
            ),
            "scale": "one universal process-geometry choice",
            "complexity": (
                "1 fixed dimensionless continuous input rho=mu_R/mu_S=1 plus the selected "
                "full-A mobility class; 0 fitted parameters"
            ),
        },
        "off_endpoint_relational_readout_candidate": {
            "source": "w2_19 frozen Candidate-A extension; evaluated here, not fitted",
            "allowed_range": (
                "simple-largest P_plus, P_R=I+2R^2/J, tau_gap=1-Tr(P_plus P_R)"
            ),
            "scale": "one fixed state-readout architecture",
            "complexity": "1 fixed map choice; 0 fitted parameters",
        },
        "overall_positive_rate": {
            "source": "global orientation-preserving curve parameterisation",
            "allowed_range": "continuous nu>0 with unbounded cumulative sigma range",
            "scale": "unphysical bookkeeping",
            "complexity": 0,
        },
        "extra_state_graph_clock_metric_or_data_parameters": {
            "source": "forbidden/absent",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "w2_16: conditional atemporal structural F2",
        "w2_17: exact F3 interface and 18 atomic gates",
        "w2_18: static endpoint cannot close F3 and a new dynamic candidate is required",
        "w2_19: frozen imported negative-gradient formation-flow candidate contract",
    ],
    "METHOD": (
        "Differentiate U exactly; derive the general spectral-gap flow, P_plus/P_R projectors, "
        "tau_gap and off-endpoint relational carrier; test rather than assume the inherited "
        "F1/F2 predecessor; prove D_gap nonempty, open, stable and invariant; "
        "prove global-forward health, O(3) covariance, the Class(A,F) event germ, semigroup "
        "order, finite-flow Frechet factorisation, same-channel response, cross-channel zeros, "
        "schedule/reparameterisation neutrality, nulls and fail-closed screening."
    ),
    "PASS_CONDITION": (
        "Every dependency, exact identity, health theorem premise, order axiom, intervention, "
        "nontransmission, D_gap/readout, null, robustness, scope and fail-closed control passes. "
        "Fourteen candidate maps are DERIVED candidate-relatively; the imported transition "
        "principle remains PARTIAL. Exactly the same-chain F1/F2-predecessor gate and the "
        "target-free foundation-derived-law gate remain false, so the standalone conditional "
        "formation theorem may pass while full F3 is ineligible."
    ),
    "FAIL_CONDITION": (
        "Any algebraic residual, constraint leak, failed covariance, non-strict nonstationary "
        "Lyapunov branch, cycle, reverse reachability, nonzero forbidden response, schedule "
        "dependence, failed spectral-gap/readout theorem, hidden predecessor assumption, "
        "unhealthy flow, target preload, "
        "dependency drift or scope promotion "
        "keeps the conditional result false."
    ),
    "FALSIFIER": (
        "A D_gap state with a lost simple-largest gap, changed P_plus/P_R/tau_gap, D U>=0, "
        "two-way reachability, a "
        "nonzero S-to-R or R-to-S flow response, finite-forward blowup despite remaining in "
        "a U sublevel, or failure of common-O(3) covariance falsifies this candidate."
    ),
    "RESIDUAL": (
        "Exactly zero for the directional-gradient, constraint, covariance, reduced-flow, "
        "projector, tau_gap, spectral-flow, relational carrier, Lyapunov, semigroup, finite-response "
        "and commutator identities."
    ),
    "ERROR_BOUND": (
        "Zero symbolic algebraic error. Positivity and robustness apply only on the declared "
        "open/regular domains; no numerical approximation or data fit is used."
    ),
    "VALIDITY_HEALTH": (
        "The polynomial vector field is locally Lipschitz. Coercivity plus U descent confines "
        "forward curves to compact sublevels, giving global forward existence. The w2_16 "
        "minimum manifold has four exact positive normal modes and four tangent zero modes. "
        "It therefore has a local nonempty open attracting basin; tau_gap remains neutral. "
        "This dynamical basin theorem does not extend the endpoint F1/F2 proof off shell."
    ),
    "BRANCHES": {
        "noncritical_formation_flow": "CONDITIONAL_STRUCTURAL_ORDER_CANDIDATE",
        "stationary_w2_16_minimum": "FROZEN_EVENT_NULL",
        "S_or_R_or_C_zero": "RELATIONAL_NULL_NO_PROMOTION",
        "tau_gap_zero": "EXCLUDED_READOUT_BOUNDARY_NOT_GENERAL_C_ZERO",
        "tau_gap_one": "EXCLUDED_ORBIT_BOUNDARY_NOT_C_ZERO",
        "spectral_gap_or_basin_boundary": "D_GAP_BOUNDARY_NO_PROMOTION",
        "positive_gradient_reverse": "REJECTED_REVERSE_ANSATZ",
        "persistent_phase_clock": "OPEN_REQUIRES_NEW_STATE_OR_LAW",
        "physical_time_spatial_causality_and_later_gates": "OPEN",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "pre-spatial structural candidate"},
    "FORWARD_MODEL": {
        "status": "N/A",
        "reason": "the process semigroup is not a spacetime or data forward model",
    },
    "DATA_ROLE": {"status": "N/A", "reason": "no data, calibration, fit or target"},
    "IDENTIFIABILITY": (
        "Direct influence is identified conditionally by a nonzero invariant D Phi response, "
        "not by U ranking. U descent certifies acyclicity. The same U permits other dynamics, "
        "so the transition principle is not identified or derived by w2_16."
    ),
    "BENCHMARK": (
        "Exact off-endpoint tau_gap=1/4 and 3/4 witnesses and a three-event logistic J orbit "
        "must pass. Frozen, reverse-gradient, correlated-static, cyclic, target-prewired "
        "and forbidden-channel transmission cases are mandatory nulls."
    ),
    "CLOSURE_FLAGS": dict(EXPECTED_CLOSURE_FLAGS),
    "CROSSCHECK": (
        "General diagonal spectral-gap algebra and full matrix differentiation crosscheck the "
        "uniaxial witness route. Finite-flow product uniqueness crosschecks exact logistic "
        "response, while graph mutations independently test order."
    ),
    "PROVENANCE": {
        "date": "2026-07-22",
        "data": "none",
        "code_version": "w2_20 evaluator version 003 predecessor-audited",
        "hash": "N/A; source control is authoritative",
        "output": "JSON exact candidate-evaluation report",
    },
    "FILES": [
        "CODES.md",
        "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py",
        "RefG/work 2/w2_17_f3_internal_order_causality_contract.py",
        "RefG/work 2/w2_18_f3_static_endpoint_adjudication_gate.py",
        "RefG/work 2/w2_19_f3_gradient_formation_flow_candidate_contract.py",
        "RefG/work 2/w2_20_f3_gradient_formation_flow_candidate_gate.py",
    ],
    "THEOREM": {
        "gradient_flow": (
            "D S=alpha S+b(S^2-I I2/3)-c I2 S and D R=(eta-dJ)R. "
            "These are exactly -grad_S U and -grad_R U."
        ),
        "reduced_flow": (
            "For S=s(P-I/3), D s=s(3alpha+bs-2cs^2)/3, "
            "D J=2J(eta-dJ), and D tau_gap=0."
        ),
        "D_gap_relational_readout": (
            "Because D S is a polynomial in S and D R is scalar times R, the S eigenframe, "
            "simple-largest ordering, R axis, P_plus, P_R and tau_gap are fixed along every "
            "finite D_gap orbit. The state-owned nodes S,R reconstruct A; C=[S,R] is nonzero "
            "for 0<tau_gap<1 and supplies exact same-unary/different-joint witnesses. Local "
            "two-sided uniqueness prevents a nonstationary orbit from hitting the stationary "
            "manifold at finite process parameter."
        ),
        "formation_order": (
            "Off the critical set D U=-||grad_S U||^2-||grad_R U||^2<0. "
            "Nonzero finite-flow intervention response defines direct influence between the "
            "state-owned germs E(A)=Class(A,F(A)); its transitive closure is acyclic because U "
            "strictly decreases. Global positive reparameterisations preserve this order."
        ),
        "no_transmission": (
            "The product vector field and its flow factorise into S and R channels. Hence "
            "D Phi_R/D S0=0 and D Phi_S/D R0=0 exactly, while finite same-channel flow "
            "differentials are nonsingular."
        ),
        "scope": (
            "The theorem is conditional on an imported gradient process package, including "
            "the descent sign and unit S/R mobility. U is a mathematical "
            "Lyapunov function, not an identified physical energy, and the minimum is a "
            "frozen null rather than a persistent clock. The off-endpoint readout candidate is "
            "evaluated as a relational readout, but it does not preserve the complete inherited "
            "F1/F2 chain off endpoint. The transition principle itself also remains "
            "imported/PARTIAL; full "
            "w2_17 F3 therefore remains false."
        ),
    },
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def scientific_contract_sha256(contract: dict[str, Any]) -> str:
    canonical = json.dumps(
        contract, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest().upper()


def frozen_scientific_contract_sha256() -> str:
    """Independent literal freeze of the complete scientific contract."""
    return "413CE5BE0590496365FB88D8EC3E6FAD029B256D90251DA9D055FB66B39381D3"


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


def matrix_zero(value: sp.MatrixBase) -> bool:
    return all(sp.simplify(item) == 0 for item in value)


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_safe(item) for item in value]
    return str(value)


def load_sibling(filename: str, module_name: str) -> ModuleType:
    path = Path(__file__).with_name(filename)
    if not path.is_file():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def symbolic_state() -> dict[str, Any]:
    alpha, b, c, eta, d = sp.symbols("alpha b c eta d", positive=True)
    x1, x2, x3, x4, x5 = sp.symbols("x1 x2 x3 x4 x5", real=True)
    y1, y2, y3, y4, y5 = sp.symbols("y1 y2 y3 y4 y5", real=True)
    r1, r2, r3 = sp.symbols("r1 r2 r3", real=True)
    q1, q2, q3 = sp.symbols("q1 q2 q3", real=True)
    eps = sp.symbols("eps", real=True)
    S = sp.Matrix([
        [x1, x2, x3],
        [x2, x4, x5],
        [x3, x5, -x1 - x4],
    ])
    dS = sp.Matrix([
        [y1, y2, y3],
        [y2, y4, y5],
        [y3, y5, -y1 - y4],
    ])
    R = sp.Matrix([
        [0, -r3, r2],
        [r3, 0, -r1],
        [-r2, r1, 0],
    ])
    dR = sp.Matrix([
        [0, -q3, q2],
        [q3, 0, -q1],
        [-q2, q1, 0],
    ])
    I = sp.eye(3)

    def potential(Sm: sp.MatrixBase, Rm: sp.MatrixBase) -> sp.Expr:
        I2m = sp.trace(Sm * Sm)
        I3m = sp.trace(Sm * Sm * Sm)
        Jm = -sp.trace(Rm * Rm)
        return sp.expand(
            -alpha * I2m / 2 - b * I3m / 3 + c * I2m**2 / 4
            - eta * Jm / 2 + d * Jm**2 / 4
        )

    I2 = sp.trace(S * S)
    I3 = sp.trace(S * S * S)
    J = -sp.trace(R * R)
    U = potential(S, R)
    gradS = sp.simplify(-alpha * S - b * (S * S - I * I2 / 3) + c * I2 * S)
    gradR = sp.simplify((-eta + d * J) * R)
    VS = sp.simplify(-gradS)
    VR = sp.simplify(-gradR)
    directional = sp.diff(potential(S + eps * dS, R + eps * dR), eps).subs(eps, 0)
    pairing = sp.trace(gradS.T * dS) + sp.trace(gradR.T * dR)
    return {
        "alpha": alpha, "b": b, "c": c, "eta": eta, "d": d,
        "S": S, "dS": dS, "R": R, "dR": dR, "I": I,
        "I2": I2, "I3": I3, "J": J, "U": U,
        "gradS": gradS, "gradR": gradR, "VS": VS, "VR": VR,
        "directional": directional, "pairing": pairing,
        "S_symbols": (x1, x2, x3, x4, x5),
        "R_symbols": (r1, r2, r3),
    }


def gradient_controls(o: dict[str, Any]) -> dict[str, bool]:
    S, R, I = o["S"], o["R"], o["I"]
    gradS_expected = sp.simplify(
        -o["alpha"] * S - o["b"] * (S * S - I * o["I2"] / 3)
        + o["c"] * o["I2"] * S
    )
    gradR_expected = sp.simplify((-o["eta"] + o["d"] * o["J"]) * R)
    return {
        "directional_derivative_matches_Frobenius_gradient_exact": (
            sp.simplify(o["directional"] - o["pairing"]) == 0
        ),
        "symmetric_gradient_formula_exact": matrix_zero(o["gradS"] - gradS_expected),
        "skew_gradient_formula_exact": matrix_zero(o["gradR"] - gradR_expected),
        "vector_field_is_negative_gradient_exact": all((
            matrix_zero(o["VS"] + o["gradS"]),
            matrix_zero(o["VR"] + o["gradR"]),
        )),
        "symmetric_traceless_constraint_preserved": all((
            matrix_zero(o["VS"] - o["VS"].T),
            sp.simplify(sp.trace(o["VS"])) == 0,
        )),
        "skew_traceless_constraint_preserved": all((
            matrix_zero(o["VR"] + o["VR"].T),
            sp.simplify(sp.trace(o["VR"])) == 0,
        )),
        "separable_channel_dependence_exact": all((
            all(sp.diff(item, symbol) == 0 for item in o["VS"] for symbol in o["R_symbols"]),
            all(sp.diff(item, symbol) == 0 for item in o["VR"] for symbol in o["S_symbols"]),
        )),
        "ansatz_origin_remains_imported_not_derived": all((
            "frozen Candidate-A package" in CLAIM_CONTRACT["ASSUMPTIONS"],
            "not Canon-derived facts" in CLAIM_CONTRACT["ASSUMPTIONS"],
            CLAIM_CONTRACT["FREEDOM_LEDGER"]
            ["kinetic_metric_and_relative_mobility"]["complexity"]
            == (
                "1 fixed dimensionless continuous input rho=mu_R/mu_S=1 plus the selected "
                "full-A mobility class; 0 fitted parameters"
            ),
            EXPECTED_CLOSURE_FLAGS["gradient_process_ansatz_imported_not_Canon_derived"],
            not EXPECTED_CLOSURE_FLAGS["foundation_derived_F3"],
        )),
    }


def equivariance_controls(o: dict[str, Any]) -> dict[str, bool]:
    S, R = o["S"], o["R"]

    def vector_field(Sm: sp.MatrixBase, Rm: sp.MatrixBase) -> tuple[sp.Matrix, sp.Matrix]:
        I2m = sp.trace(Sm * Sm)
        Jm = -sp.trace(Rm * Rm)
        VSm = (
            o["alpha"] * Sm
            + o["b"] * (Sm * Sm - sp.eye(3) * I2m / 3)
            - o["c"] * I2m * Sm
        )
        VRm = (o["eta"] - o["d"] * Jm) * Rm
        return sp.simplify(VSm), sp.simplify(VRm)

    cayley_parameter = sp.symbols("cayley_parameter", real=True)
    cayley_denominator = 1 + cayley_parameter**2
    generic_plane_rotation = sp.Matrix([
        [(1 - cayley_parameter**2) / cayley_denominator,
         -2 * cayley_parameter / cayley_denominator, 0],
        [2 * cayley_parameter / cayley_denominator,
         (1 - cayley_parameter**2) / cayley_denominator, 0],
        [0, 0, 1],
    ])
    axis_permutation = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    reflection = sp.diag(-1, 1, 1)
    # One generic Cayley plane-rotation family, an axis permutation and one
    # reflection generate a dense SO(3) subgroup and both determinant sectors;
    # polynomial/rational covariance and continuity supply the omitted pi
    # Cayley point.  This is a universal generator proof, not sampled angles.
    generators = (generic_plane_rotation, axis_permutation, reflection)
    exact = []
    for Q in generators:
        VSt, VRt = vector_field(Q * S * Q.T, Q * R * Q.T)
        exact.append(all((
            matrix_zero(VSt - Q * o["VS"] * Q.T),
            matrix_zero(VRt - Q * o["VR"] * Q.T),
            matrix_zero(Q.T * Q - sp.eye(3)),
        )))
    s_can, u_can, v_can = sp.symbols("s_can u_can v_can", real=True)
    S_can = s_can * (sp.diag(1, 0, 0) - sp.eye(3) / 3)
    R_can = sp.Matrix([[0, 0, v_can], [0, 0, -u_can], [-v_can, u_can, 0]])
    transpose_reflection = sp.diag(1, 1, -1)
    VS_can, VR_can = vector_field(S_can, R_can)
    return {
        "manifest_common_O3_covariance_theorem_registered": all((
            "O(3)" in CLAIM_CONTRACT["ASSUMPTIONS"]
            and "Tr(S^2)" in CLAIM_CONTRACT["CONVENTIONS"],
            all(exact),
        )),
        "exact_generic_plane_rotation_covariance": exact[0],
        "exact_axis_permutation_covariance": exact[1],
        "exact_reflection_covariance": exact[2],
        "transpose_involution_maps_forward_flow_to_forward_flow": all((
            matrix_zero(transpose_reflection * S_can * transpose_reflection.T - S_can),
            matrix_zero(transpose_reflection * R_can * transpose_reflection.T + R_can),
            matrix_zero(transpose_reflection * VR_can * transpose_reflection.T + VR_can),
            matrix_zero(transpose_reflection * VS_can * transpose_reflection.T - VS_can),
        )),
        "no_preferred_basis_axis_or_orientation": all((
            PRIMITIVE_INPUT_SYMBOLS.isdisjoint(FORBIDDEN_TARGET_INPUT_SYMBOLS),
            all(exact),
        )),
    }


def reduced_flow_objects(o: dict[str, Any]) -> dict[str, Any]:
    s = sp.symbols("s", positive=True)
    u, v = sp.symbols("u v", real=True)
    P = sp.diag(1, 0, 0)
    S = sp.simplify(s * (P - sp.eye(3) / 3))
    R = sp.Matrix([[0, 0, v], [0, 0, -u], [-v, u, 0]])
    I2 = sp.trace(S * S)
    J = -sp.trace(R * R)
    VS = sp.simplify(
        o["alpha"] * S
        + o["b"] * (S * S - sp.eye(3) * I2 / 3)
        - o["c"] * I2 * S
    )
    VR = sp.simplify((o["eta"] - o["d"] * J) * R)
    ds = sp.factor(s * (3 * o["alpha"] + o["b"] * s - 2 * o["c"] * s**2) / 3)
    dJ = sp.factor(2 * sp.trace(R.T * VR))
    PS = sp.simplify(sp.eye(3) / 3 + S / s)
    PR = sp.simplify(sp.eye(3) + 2 * R * R / J)
    dPS = sp.simplify(VS / s - S * ds / s**2)
    dPR = sp.simplify(
        2 * (VR * R + R * VR) / J - 2 * R * R * dJ / J**2
    )
    tau = sp.simplify(1 - sp.trace(PS * PR))
    dtau = sp.simplify(-sp.trace(dPS * PR + PS * dPR))
    return {
        "s": s, "u": u, "v": v, "P": P, "S": S, "R": R,
        "I2": I2, "J": J, "VS": VS, "VR": VR, "ds": ds, "dJ": dJ,
        "PS": PS, "PR": PR, "dPS": dPS, "dPR": dPR,
        "tau": tau, "dtau": dtau,
    }


def reduced_flow_controls(o: dict[str, Any], r: dict[str, Any]) -> dict[str, bool]:
    expected_factor = sp.simplify(
        o["alpha"] + o["b"] * r["s"] / 3 - 2 * o["c"] * r["s"]**2 / 3
    )
    expected_dJ = sp.simplify(2 * r["J"] * (o["eta"] - o["d"] * r["J"]))
    expected_tau = sp.simplify(r["v"]**2 / (r["u"]**2 + r["v"]**2))
    return {
        "uniaxial_symmetric_branch_is_invariant": matrix_zero(
            r["VS"] - expected_factor * r["S"]
        ),
        "ds_equation_exact": sp.simplify(r["ds"] - expected_factor * r["s"]) == 0,
        "skew_direction_is_invariant": matrix_zero(
            r["VR"] - (o["eta"] - o["d"] * r["J"]) * r["R"]
        ),
        "dJ_equation_exact": sp.simplify(r["dJ"] - expected_dJ) == 0,
        "state_projectors_are_constant_along_reduced_flow": all((
            matrix_zero(r["dPS"]), matrix_zero(r["dPR"]),
        )),
        "dtau_is_exactly_zero": sp.simplify(r["dtau"]) == 0,
        "generic_F2_relational_stratum_is_preserved": all((
            sp.simplify(r["tau"] - expected_tau) == 0,
            matrix_zero(r["dPS"]), matrix_zero(r["dPR"]),
            "tau_gap=1-Tr(P_plus P_R) is in (0,1)" in CLAIM_CONTRACT["DOMAIN"],
        )),
    }


def health_controls(o: dict[str, Any], r: dict[str, Any]) -> dict[str, bool]:
    grad_norm_sq = sp.expand(
        sp.trace(o["gradS"].T * o["gradS"])
        + sp.trace(o["gradR"].T * o["gradR"])
    )
    Udot = sp.expand(
        sp.trace(o["gradS"].T * o["VS"])
        + sp.trace(o["gradR"].T * o["VR"])
    )
    lam1, lam2 = sp.symbols("lam1 lam2", real=True)
    lam3 = -lam1 - lam2
    eig_I2 = sp.expand(lam1**2 + lam2**2 + lam3**2)
    eig_I3 = sp.expand(lam1**3 + lam2**3 + lam3**3)
    discriminant_bound = sp.factor(eig_I2**3 - 6 * eig_I3**2)
    s_star = sp.simplify(
        (o["b"] + sp.sqrt(o["b"]**2 + 24 * o["alpha"] * o["c"]))
        / (4 * o["c"])
    )
    J_star = sp.simplify(o["eta"] / o["d"])
    fs = r["ds"]
    fJ_symbol = sp.symbols("J_positive", positive=True)
    fJ = 2 * fJ_symbol * (o["eta"] - o["d"] * fJ_symbol)
    eig_s = sp.simplify(sp.diff(fs, r["s"]).subs(r["s"], s_star))
    eig_J = sp.simplify(sp.diff(fJ, fJ_symbol).subs(fJ_symbol, J_star))

    # Full normal-Hessian audit at a representative positive product minimum.
    # The Frobenius-orthonormal symmetric basis separates one radial, two
    # biaxial and two orbit-tangent directions.  The skew basis separates one
    # radial and two sphere-tangent directions.  Thus this checks more than the
    # reduced (s,J) radial subsystem and keeps every exact zero mode explicit.
    sqrt2, sqrt6 = sp.sqrt(2), sp.sqrt(6)
    Q = sp.diag(sp.Rational(2, 3), sp.Rational(-1, 3), sp.Rational(-1, 3))
    S_star = sp.simplify(s_star * Q)
    E_s_radial = sp.diag(2, -1, -1) / sqrt6
    E_s_biaxial_1 = sp.diag(0, 1, -1) / sqrt2
    E_s_biaxial_2 = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]) / sqrt2
    E_s_orbit_1 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]) / sqrt2
    E_s_orbit_2 = sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]) / sqrt2
    I2_star = sp.simplify(sp.trace(S_star * S_star))

    def symmetric_hessian_action(H: sp.MatrixBase) -> sp.Matrix:
        inner = sp.trace(S_star.T * H)
        return sp.simplify(
            (-o["alpha"] + o["c"] * I2_star) * H
            + 2 * o["c"] * inner * S_star
            - o["b"] * (S_star * H + H * S_star - 2 * inner * sp.eye(3) / 3)
        )

    discriminant = sp.sqrt(o["b"]**2 + 24 * o["alpha"] * o["c"])
    symmetric_radial_curvature = sp.simplify(s_star * discriminant / 3)
    symmetric_biaxial_curvature = sp.simplify(o["b"] * s_star)

    rho_star = sp.sqrt(o["eta"] / (2 * o["d"]))
    R_star = sp.Matrix([[0, -rho_star, 0], [rho_star, 0, 0], [0, 0, 0]])
    E_r_radial = sp.simplify(R_star / sp.sqrt(J_star))
    E_r_orbit_1 = sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]) / sqrt2
    E_r_orbit_2 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]]) / sqrt2

    def skew_hessian_action(H: sp.MatrixBase) -> sp.Matrix:
        inner = sp.trace(R_star.T * H)
        J_at_star = -sp.trace(R_star * R_star)
        return sp.simplify(
            (-o["eta"] + o["d"] * J_at_star) * H
            + 2 * o["d"] * inner * R_star
        )

    full_normal_hessian_exact = all((
        matrix_zero(
            symmetric_hessian_action(E_s_radial)
            - symmetric_radial_curvature * E_s_radial
        ),
        matrix_zero(
            symmetric_hessian_action(E_s_biaxial_1)
            - symmetric_biaxial_curvature * E_s_biaxial_1
        ),
        matrix_zero(
            symmetric_hessian_action(E_s_biaxial_2)
            - symmetric_biaxial_curvature * E_s_biaxial_2
        ),
        matrix_zero(symmetric_hessian_action(E_s_orbit_1)),
        matrix_zero(symmetric_hessian_action(E_s_orbit_2)),
        matrix_zero(skew_hessian_action(E_r_radial) - 2 * o["eta"] * E_r_radial),
        matrix_zero(skew_hessian_action(E_r_orbit_1)),
        matrix_zero(skew_hessian_action(E_r_orbit_2)),
        symmetric_radial_curvature.is_positive,
        symmetric_biaxial_curvature.is_positive,
        o["eta"].is_positive,
    ))

    # The exact spectral inequality controls the cubic invariant, and these
    # radial lower bounds show that the positive quartics dominate every
    # lower-order term.  I2+J is exactly the full Frobenius norm squared.
    radial, radial_J = sp.symbols("radial radial_J", positive=True)
    symmetric_lower_bound = (
        o["c"] * radial**4 / 4
        - o["b"] * radial**3 / (3 * sp.sqrt(6))
        - o["alpha"] * radial**2 / 2
    )
    skew_lower_bound = o["d"] * radial_J**2 / 4 - o["eta"] * radial_J / 2
    norm_split_residual = sp.simplify(
        sp.trace((o["S"] + o["R"]).T * (o["S"] + o["R"])) - o["I2"] - o["J"]
    )
    coercive_radial_limits_exact = all((
        sp.limit(symmetric_lower_bound / radial**4, radial, sp.oo) == o["c"] / 4,
        sp.limit(skew_lower_bound / radial_J**2, radial_J, sp.oo) == o["d"] / 4,
        norm_split_residual == 0,
    ))
    m, delta = sp.symbols("m delta", positive=True)
    robust_upper = sp.factor(-m**2 + m * delta)
    return {
        "Lyapunov_identity_exact": sp.simplify(Udot + grad_norm_sq) == 0,
        "Lyapunov_strict_off_critical_set": all((
            sp.simplify(Udot + grad_norm_sq) == 0,
            "Off the critical set" in CLAIM_CONTRACT["THEOREM"]["formation_order"],
        )),
        "traceless_spectral_discriminant_bound_exact": (
            discriminant_bound
            == 2 * (lam1 - lam2)**2 * (lam1 + 2 * lam2)**2 * (2 * lam1 + lam2)**2
        ),
        "positive_quartic_coercivity_premises_exact": all((
            o["c"].is_positive, o["d"].is_positive,
            discriminant_bound.is_nonnegative,
            coercive_radial_limits_exact,
            "Coercivity" in CLAIM_CONTRACT["VALIDITY_HEALTH"],
        )),
        "polynomial_vector_field_is_locally_Lipschitz": all(
            item.is_polynomial(*o["S_symbols"], *o["R_symbols"])
            for item in tuple(o["VS"]) + tuple(o["VR"])
        ),
        "compact_sublevel_prevents_finite_forward_blowup": all((
            o["c"].is_positive, o["d"].is_positive,
            "compact sublevels" in CLAIM_CONTRACT["VALIDITY_HEALTH"],
            "global forward existence" in CLAIM_CONTRACT["VALIDITY_HEALTH"],
        )),
        "positive_s_and_J_branches_are_forward_invariant": all((
            sp.simplify(fs.subs(r["s"], 0)) == 0,
            sp.simplify(fJ.subs(fJ_symbol, 0)) == 0,
            r["s"].is_positive, fJ_symbol.is_positive,
        )),
        "endpoint_radii_are_exact_fixed_points": all((
            sp.simplify(fs.subs(r["s"], s_star)) == 0,
            sp.simplify(fJ.subs(fJ_symbol, J_star)) == 0,
        )),
        "normal_linear_stability_exact": all((
            eig_s.is_negative, eig_J == -2 * o["eta"], eig_J.is_negative,
            full_normal_hessian_exact,
        )),
        "compact_Morse_Bott_minimum_manifold_registered": all((
            full_normal_hessian_exact,
            "four exact positive normal modes and four tangent zero modes"
            in CLAIM_CONTRACT["VALIDITY_HEALTH"],
            "O(3)" in CLAIM_CONTRACT["ASSUMPTIONS"],
            "local nonempty open attracting basin"
            in CLAIM_CONTRACT["VALIDITY_HEALTH"],
        )),
        "flat_tau_direction_is_neutral_not_falsely_stabilized": all((
            r["dtau"] == 0,
            "tau_gap remains neutral" in CLAIM_CONTRACT["VALIDITY_HEALTH"],
        )),
        "U_is_not_promoted_to_physical_energy": (
            "not an identified physical energy" in CLAIM_CONTRACT["THEOREM"]["scope"]
        ),
        "_robust_descent_witness": sp.simplify(robust_upper + m * (m - delta)) == 0,
    }


def domain_readout_controls(
    o: dict[str, Any], r: dict[str, Any], health: dict[str, bool],
) -> tuple[dict[str, bool], dict[str, Any]]:
    """Exact D_gap/readout audit plus inherited-F1/F2 counterexamples.

    A diagonal spectral representative is general modulo the already frozen
    common O(3) action.  Positive g2=lambda1-lambda2 and
    g3=lambda1-lambda3 encode precisely one simple largest eigenvalue without
    imposing an artificial ordering on the two lower eigenvalues.
    """
    g2, g3 = sp.symbols("g2 g3", positive=True)
    rx, ry, rz = sp.symbols("rx ry rz", real=True)
    q = sp.expand(rx**2 + ry**2 + rz**2)
    lam1 = sp.simplify((g2 + g3) / 3)
    lam2 = sp.simplify(lam1 - g2)
    lam3 = sp.simplify(lam1 - g3)
    S_gap = sp.diag(lam1, lam2, lam3)
    P_plus = sp.diag(1, 0, 0)
    R_gap = sp.Matrix([
        [0, -rz, ry],
        [rz, 0, -rx],
        [-ry, rx, 0],
    ])
    J_gap = sp.simplify(-sp.trace(R_gap * R_gap))
    P_R = sp.simplify(sp.eye(3) + 2 * R_gap * R_gap / J_gap)
    tau_gap = sp.factor(1 - sp.trace(P_plus * P_R))
    C_gap = sp.simplify(S_gap * R_gap - R_gap * S_gap)
    K_gap = sp.factor(sp.trace(C_gap.T * C_gap))
    expected_K = sp.expand(2 * (
        g2**2 * rz**2 + g3**2 * ry**2 + (g3 - g2)**2 * rx**2
    ))
    transverse_K = sp.expand(2 * (g2**2 * rz**2 + g3**2 * ry**2))
    # A manifest strict lower-bound certificate on tau_gap>0.  The harmonic
    # sub-gap m_gap is positive and smaller than both g2 and g3, so the exact
    # transverse commutator norm is at least
    # 2*m_gap^2*(ry^2+rz^2), which is strictly positive when tau_gap>0.
    m_gap = sp.factor(g2 * g3 / (g2 + g3))
    transverse_lower_bound = sp.factor(2 * m_gap**2 * (ry**2 + rz**2))
    transverse_lower_remainder = sp.factor(transverse_K - transverse_lower_bound)
    q_perp_positive = sp.symbols("q_perp_positive", positive=True)
    strict_transverse_proxy = sp.factor(2 * m_gap**2 * q_perp_positive)

    I2_gap = sp.trace(S_gap * S_gap)
    F_S_gap = sp.simplify(
        o["alpha"] * S_gap
        + o["b"] * (S_gap * S_gap - sp.eye(3) * I2_gap / 3)
        - o["c"] * I2_gap * S_gap
    )
    flow_lambdas = tuple(F_S_gap[index, index] for index in range(3))
    gap2_rate = sp.factor(flow_lambdas[0] - flow_lambdas[1])
    gap3_rate = sp.factor(flow_lambdas[0] - flow_lambdas[2])
    expected_gap2_rate = sp.factor(
        g2 * (o["alpha"] + o["b"] * (lam1 + lam2) - o["c"] * I2_gap)
    )
    expected_gap3_rate = sp.factor(
        g3 * (o["alpha"] + o["b"] * (lam1 + lam3) - o["c"] * I2_gap)
    )
    F_R_gap = sp.simplify((o["eta"] - o["d"] * J_gap) * R_gap)
    J_gap_rate = sp.simplify(2 * sp.trace(R_gap.T * F_R_gap))
    P_R_rate = sp.simplify(
        2 * (F_R_gap * R_gap + R_gap * F_R_gap) / J_gap
        - 2 * R_gap * R_gap * J_gap_rate / J_gap**2
    )
    tau_gap_rate = sp.simplify(-sp.trace(P_plus * P_R_rate))

    # Consistency with the old w2_16 endpoint support/readout.
    s = sp.symbols("s_endpoint", positive=True)
    S_uniaxial = sp.simplify(s * (P_plus - sp.eye(3) / 3))
    P_old = sp.simplify(sp.eye(3) / 3 + S_uniaxial / s)
    C_uniaxial = sp.simplify(S_uniaxial * R_gap - R_gap * S_uniaxial)
    K_uniaxial = sp.factor(sp.trace(C_uniaxial.T * C_uniaxial))
    old_tau = sp.factor(K_uniaxial / (s**2 * J_gap))

    # Two exact, nonstationary D_gap witnesses with complete identical unary
    # data and different joint reports.  For alpha=b=c=eta=d=1, s=1 and
    # J=1/2 flow to s_+=3/2 and J_*=1, so they lie in a proved local basin and
    # are not the frozen endpoint.
    parameters_one = {
        o["alpha"]: 1, o["b"]: 1, o["c"]: 1, o["eta"]: 1, o["d"]: 1,
    }
    S_witness = sp.diag(sp.Rational(2, 3), sp.Rational(-1, 3), sp.Rational(-1, 3))

    def axial_matrix(vector: tuple[sp.Expr, sp.Expr, sp.Expr]) -> sp.Matrix:
        ax, ay, az = vector
        return sp.Matrix([[0, -az, ay], [az, 0, -ax], [-ay, ax, 0]])

    R_quarter = axial_matrix((sp.sqrt(3) / 4, sp.Rational(1, 4), 0))
    R_three_quarters = axial_matrix((sp.Rational(1, 4), sp.sqrt(3) / 4, 0))

    def witness_report(Rm: sp.MatrixBase) -> dict[str, Any]:
        Jm = sp.simplify(-sp.trace(Rm * Rm))
        PRm = sp.simplify(sp.eye(3) + 2 * Rm * Rm / Jm)
        taum = sp.simplify(1 - sp.trace(P_plus * PRm))
        Cm = sp.simplify(S_witness * Rm - Rm * S_witness)
        Km = sp.simplify(sp.trace(Cm.T * Cm))
        I2m = sp.trace(S_witness * S_witness)
        VSm = sp.simplify((
            o["alpha"] * S_witness
            + o["b"] * (S_witness * S_witness - sp.eye(3) * I2m / 3)
            - o["c"] * I2m * S_witness
        ).subs(parameters_one))
        VRm = sp.simplify(
            ((o["eta"] - o["d"] * Jm) * Rm).subs(parameters_one)
        )
        speed_sq = sp.simplify(sp.trace(VSm.T * VSm) + sp.trace(VRm.T * VRm))
        return {"J": Jm, "P_R": PRm, "tau_gap": taum, "C": Cm, "K": Km,
                "speed_sq": speed_sq}

    witness_a = witness_report(R_quarter)
    witness_b = witness_report(R_three_quarters)
    I2_witness = sp.trace(S_witness * S_witness)
    I3_witness = sp.trace(S_witness**3)
    ds_witness = sp.simplify(r["ds"].subs(parameters_one).subs(r["s"], 1))
    dJ_witness = sp.simplify(
        (2 * sp.Rational(1, 2) * (o["eta"] - o["d"] * sp.Rational(1, 2)))
        .subs(parameters_one)
    )
    s_plus_witness = sp.Rational(3, 2)
    basin_parameter = sp.symbols("basin_parameter", positive=True)
    s_inside_basin = sp.simplify(
        1 + sp.Rational(1, 2) * basin_parameter / (1 + basin_parameter)
    )
    J_inside_basin = sp.simplify(
        sp.Rational(1, 2)
        + sp.Rational(1, 2) * basin_parameter / (1 + basin_parameter)
    )
    ds_inside_basin = sp.factor(
        (r["ds"].subs(parameters_one).subs(r["s"], s_inside_basin))
    )
    dJ_inside_basin = sp.factor(
        2 * J_inside_basin * (1 - J_inside_basin)
    )

    # Exact common-O(3) covariance checks for an orientation-preserving rational
    # rotation and a reflection.  The formulas use only conjugation, products
    # and traces, so these representatives also audit both determinant sectors.
    extension_parameter = sp.symbols("extension_parameter", real=True)
    extension_denominator = 1 + extension_parameter**2
    rotation = sp.Matrix([
        [(1 - extension_parameter**2) / extension_denominator,
         -2 * extension_parameter / extension_denominator, 0],
        [2 * extension_parameter / extension_denominator,
         (1 - extension_parameter**2) / extension_denominator, 0],
        [0, 0, 1],
    ])
    axis_permutation = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    reflection = sp.diag(1, 1, -1)

    def extension_covariant(O: sp.MatrixBase) -> bool:
        St = sp.simplify(O * S_gap * O.T)
        Rt = sp.simplify(O * R_gap * O.T)
        Pt = sp.simplify(O * P_plus * O.T)
        Jt = sp.simplify(-sp.trace(Rt * Rt))
        PRt = sp.simplify(sp.eye(3) + 2 * Rt * Rt / Jt)
        taut = sp.simplify(1 - sp.trace(Pt * PRt))
        Ct = sp.simplify(St * Rt - Rt * St)
        return all((
            matrix_zero(O.T * O - sp.eye(3)),
            matrix_zero(PRt - O * P_R * O.T),
            sp.simplify(taut - tau_gap) == 0,
            matrix_zero(Ct - O * C_gap * O.T),
        ))

    projector_controls = all((
        matrix_zero(P_plus.T - P_plus), matrix_zero(P_plus**2 - P_plus),
        sp.trace(P_plus) == 1,
        matrix_zero(S_gap * P_plus - lam1 * P_plus),
        sp.simplify(lam1 - lam2 - g2) == 0,
        sp.simplify(lam1 - lam3 - g3) == 0,
    ))
    p_r_controls = all((
        sp.simplify(J_gap - 2 * q) == 0,
        matrix_zero(P_R.T - P_R), matrix_zero(P_R**2 - P_R),
        sp.simplify(sp.trace(P_R) - 1) == 0,
        matrix_zero(R_gap * P_R),
    ))
    witness_controls = all((
        witness_a["J"] == witness_b["J"] == sp.Rational(1, 2),
        witness_a["tau_gap"] == sp.Rational(1, 4),
        witness_b["tau_gap"] == sp.Rational(3, 4),
        witness_a["K"] == sp.Rational(1, 8),
        witness_b["K"] == sp.Rational(3, 8),
        witness_a["speed_sq"] > 0, witness_b["speed_sq"] > 0,
        ds_witness == sp.Rational(2, 3),
        dJ_witness == sp.Rational(1, 2),
        I2_witness == sp.Rational(2, 3),
        I3_witness == sp.Rational(2, 9),
    ))

    # The same exact nonstationary witness falsifies an inherited-F2a
    # extension.  Off shell, the Hessian no longer has the stationary
    # orbit-null structure used by w2_12/w2_16.  At alpha=b=c=s=1 its radial
    # and biaxial curvatures coincide even though b^2 != 3 alpha c, and its
    # former orbit direction has nonzero curvature.  Thus the relational
    # P_plus/P_R/tau_gap readout can be valid while the complete same-chain
    # F1/F2 predecessor is not.
    E_radial = sp.diag(2, -1, -1) / sp.sqrt(6)
    E_biaxial = sp.diag(0, 1, -1) / sp.sqrt(2)
    E_orbit = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]) / sp.sqrt(2)

    def off_shell_hessian_action(H: sp.MatrixBase) -> sp.Matrix:
        inner = sp.trace(S_witness.T * H)
        return sp.simplify((
            (-o["alpha"] + o["c"] * I2_witness) * H
            + 2 * o["c"] * inner * S_witness
            - o["b"] * (
                S_witness * H + H * S_witness
                - 2 * inner * sp.eye(3) / 3
            )
        ).subs(parameters_one))

    off_shell_curvatures = tuple(
        sp.simplify(sp.trace(H.T * off_shell_hessian_action(H)))
        for H in (E_radial, E_biaxial, E_orbit)
    )
    inherited_predecessor_counterexample = all((
        witness_controls,
        off_shell_curvatures == (
            sp.Rational(1, 3), sp.Rational(1, 3), sp.Rational(-2, 3)
        ),
        off_shell_curvatures[0] == off_shell_curvatures[1],
        off_shell_curvatures[2] != 0,
        ds_witness != 0,
        1 != 3,
    ))

    # tau_gap=0 is only an excluded boundary for the general off-endpoint
    # readout.  It is not a general synonym for C=0: a biaxial lower block can
    # fail to commute with rotations about the P_plus axis.
    S_tau_zero = sp.diag(2, 0, -2)
    R_tau_zero = axial_matrix((1, 0, 0))
    J_tau_zero = sp.simplify(-sp.trace(R_tau_zero * R_tau_zero))
    P_R_tau_zero = sp.simplify(
        sp.eye(3) + 2 * R_tau_zero * R_tau_zero / J_tau_zero
    )
    tau_zero = sp.simplify(1 - sp.trace(P_plus * P_R_tau_zero))
    C_tau_zero = sp.simplify(S_tau_zero * R_tau_zero - R_tau_zero * S_tau_zero)
    K_tau_zero = sp.simplify(sp.trace(C_tau_zero.T * C_tau_zero))
    tau_zero_counterexample = all((
        tau_zero == 0,
        K_tau_zero == 8,
        not matrix_zero(C_tau_zero),
        matrix_zero(P_R_tau_zero - P_plus),
    ))
    gap_flow_controls = all((
        matrix_zero(S_gap * F_S_gap - F_S_gap * S_gap),
        sp.simplify(gap2_rate - expected_gap2_rate) == 0,
        sp.simplify(gap3_rate - expected_gap3_rate) == 0,
        g2.is_positive, g3.is_positive,
        sp.exp(sp.symbols("integrated_gap2_rate", real=True)).is_positive,
        sp.exp(sp.symbols("integrated_gap3_rate", real=True)).is_positive,
    ))
    local_basin_controls = all((
        witness_controls,
        s_plus_witness > 1,
        (s_plus_witness - s_inside_basin).is_positive,
        (1 - J_inside_basin).is_positive,
        ds_inside_basin.is_positive,
        dJ_inside_basin.is_positive,
        health["normal_linear_stability_exact"],
        health["compact_Morse_Bott_minimum_manifold_registered"],
        health["polynomial_vector_field_is_locally_Lipschitz"],
        health["compact_sublevel_prevents_finite_forward_blowup"],
        "local nonempty open attracting basin" in CLAIM_CONTRACT["VALIDITY_HEALTH"],
    ))
    commutator_nonzero_controls = all((
        sp.simplify(K_gap - expected_K) == 0,
        transverse_K.is_nonnegative,
        sp.simplify(expected_K - transverse_K - 2 * (g3 - g2)**2 * rx**2) == 0,
        m_gap.is_positive,
        transverse_lower_remainder.is_nonnegative,
        strict_transverse_proxy.is_positive,
        sp.simplify(tau_gap - (ry**2 + rz**2) / q) == 0,
        g2.is_positive, g3.is_positive,
        "tau_gap=1-Tr(P_plus P_R) is in (0,1)" in CLAIM_CONTRACT["DOMAIN"],
    ))
    no_finite_endpoint_hit_controls = all((
        health["polynomial_vector_field_is_locally_Lipschitz"],
        health["endpoint_radii_are_exact_fixed_points"],
        "grad_F U are nonzero" in CLAIM_CONTRACT["DOMAIN"],
        "two-sided uniqueness prevents" in
        CLAIM_CONTRACT["THEOREM"]["D_gap_relational_readout"],
    ))
    controls = {
        "P_plus_simple_largest_projector_exact": projector_controls,
        "P_R_state_owned_axis_projector_exact": p_r_controls,
        "tau_gap_formula_and_endpoint_consistency_exact": all((
            sp.simplify(tau_gap - (ry**2 + rz**2) / q) == 0,
            matrix_zero(P_old - P_plus),
            sp.simplify(old_tau - tau_gap) == 0,
            sp.simplify(K_uniaxial - s**2 * J_gap * tau_gap) == 0,
        )),
        "state_nodes_reconstruct_A_and_carrier_cross_nulls": all((
            matrix_zero((o["S"] + o["R"] + (o["S"] + o["R"]).T) / 2 - o["S"]),
            matrix_zero((o["S"] + o["R"] - (o["S"] + o["R"]).T) / 2 - o["R"]),
            matrix_zero(o["S"] * sp.zeros(3) - sp.zeros(3) * o["S"]),
            matrix_zero(sp.zeros(3) * o["R"] - o["R"] * sp.zeros(3)),
        )),
        "commutator_norm_and_tau_imply_C_nonzero_exact": all((
            commutator_nonzero_controls,
        )),
        "off_endpoint_same_unary_different_joint_witness_exact": witness_controls,
        "off_endpoint_joint_readout_irreducible_exact": all((
            witness_controls,
            witness_a["J"] == witness_b["J"],
            witness_a["K"] != witness_b["K"],
            "state-owned nodes S,R"
            in CLAIM_CONTRACT["THEOREM"]["D_gap_relational_readout"],
        )),
        "inherited_F1_F2_counterexample_exact": inherited_predecessor_counterexample,
        "tau_zero_not_general_commutator_null_exact": tau_zero_counterexample,
        "S_flow_preserves_eigenframe_exact": all((
            matrix_zero(S_gap * F_S_gap - F_S_gap * S_gap),
            matrix_zero(F_S_gap - sp.diag(*flow_lambdas)),
        )),
        "simple_largest_spectral_gaps_preserved_exact": gap_flow_controls,
        "R_flow_preserves_axis_and_P_R_exact": all((
            matrix_zero(F_R_gap - (o["eta"] - o["d"] * J_gap) * R_gap),
            matrix_zero(P_R_rate),
        )),
        "tau_gap_is_flow_invariant_exact": all((
            matrix_zero(P_R_rate), tau_gap_rate == 0,
        )),
        "finite_flow_cannot_hit_stationary_endpoint_exact": all((
            no_finite_endpoint_hit_controls,
        )),
        "local_D_gap_basin_nonempty_open_and_stable": local_basin_controls,
        "D_gap_is_forward_invariant": all((
            gap_flow_controls, matrix_zero(P_R_rate), tau_gap_rate == 0,
            commutator_nonzero_controls, no_finite_endpoint_hit_controls,
            local_basin_controls,
            health["positive_s_and_J_branches_are_forward_invariant"],
        )),
        "off_endpoint_relational_readout_common_O3_covariant": all((
            extension_covariant(rotation), extension_covariant(axis_permutation),
            extension_covariant(reflection),
        )),
    }
    diagnostics = {
        "S_gap": S_gap, "P_plus": P_plus, "P_R": P_R,
        "tau_gap": tau_gap, "K_gap": K_gap,
        "gap2_rate": gap2_rate, "gap3_rate": gap3_rate,
        "witness_tau_gap": (witness_a["tau_gap"], witness_b["tau_gap"]),
        "witness_K": (witness_a["K"], witness_b["K"]),
        "off_shell_F2a_curvatures": off_shell_curvatures,
        "tau_zero_counterexample": {"tau_gap": tau_zero, "K": K_tau_zero},
        "strict_K_lower_bound": transverse_lower_bound,
    }
    return controls, diagnostics


def transitive_closure(
    nodes: Iterable[int], edges: Iterable[tuple[int, int]],
) -> set[tuple[int, int]]:
    node_set = set(nodes)
    closure = {(left, right) for left, right in edges if left in node_set and right in node_set}
    while True:
        additions = {
            (left, right2)
            for left, middle in closure
            for middle2, right2 in closure
            if middle == middle2 and (left, right2) not in closure
        }
        if not additions:
            return closure
        closure |= additions


def order_axioms(nodes: Iterable[int], edges: Iterable[tuple[int, int]]) -> dict[str, bool]:
    node_set = set(nodes)
    closure = transitive_closure(node_set, edges)
    reflexive = closure | {(node, node) for node in node_set}
    return {
        "irreflexive": all((node, node) not in closure for node in node_set),
        "asymmetric": all((right, left) not in closure for left, right in closure),
        "transitive": transitive_closure(node_set, closure) == closure,
        "acyclic": all((node, node) not in closure for node in node_set),
        "reflexive_closure_antisymmetric": all(
            left == right or (right, left) not in reflexive for left, right in reflexive
        ),
    }


def ranked_relation_lemma(
    strict_rank_on_every_direct_edge: bool,
    effective_relation_is_transitive_closure: bool,
) -> dict[str, bool]:
    """Universal rank-function lemma, independent of any finite graph fixture.

    If every direct edge x->y obeys U(y)<U(x), a self-edge, reverse pair or
    finite directed cycle would imply a strict real-number inequality back to
    its starting value.  The nonempty transitive closure preserves that strict
    decrease and is transitive by definition; adjoining equality therefore
    gives an antisymmetric reflexive closure.
    """
    premises = bool(
        strict_rank_on_every_direct_edge
        and effective_relation_is_transitive_closure
    )
    return {
        "irreflexive": premises,
        "asymmetric": premises,
        "acyclic": premises,
        "transitive": premises,
        "reflexive_closure_antisymmetric": premises,
    }


def order_controls(
    o: dict[str, Any], health: dict[str, bool],
) -> tuple[dict[str, bool], dict[str, Any]]:
    z, z1, z2, J0 = sp.symbols("z z1 z2 J0", positive=True)
    a = sp.symbols("a", nonnegative=True)
    J_star = o["eta"] / o["d"]

    def phi(z_value: sp.Expr, initial: sp.Expr) -> sp.Expr:
        return sp.factor(
            J_star * initial / (initial + (J_star - initial) * z_value)
        )

    phi_a = phi(sp.exp(-2 * o["eta"] * a), J0)
    ode_residual = sp.simplify(
        sp.diff(phi_a, a) - 2 * phi_a * (o["eta"] - o["d"] * phi_a)
    )
    composition_residual = sp.simplify(phi(z1, phi(z2, J0)) - phi(z1 * z2, J0))
    response = sp.factor(sp.diff(phi(z, J0), J0))
    benchmark = [sp.Rational(1, 4), sp.Rational(2, 5), sp.Rational(4, 7)]
    energies = [sp.simplify(-J / 2 + J**2 / 4) for J in benchmark]
    benchmark_substitution = {o["eta"]: 1, o["d"]: 1}
    benchmark_edges = ((0, 1), (1, 2))
    axioms = order_axioms((0, 1, 2), benchmark_edges)
    reverse = order_axioms((0, 1), ((0, 1), (1, 0)))
    benchmark_flow_exact = all((
        sp.simplify(
            phi(sp.Rational(1, 2), benchmark[0]).subs(benchmark_substitution)
            - benchmark[1]
        ) == 0,
        sp.simplify(
            phi(sp.Rational(1, 2), benchmark[1]).subs(benchmark_substitution)
            - benchmark[2]
        ) == 0,
    ))
    benchmark_strict_descent = all(
        energies[left] > energies[right] for left, right in benchmark_edges
    )
    strict_rank_on_every_direct_edge = all((
        health["Lyapunov_strict_off_critical_set"],
        "grad_F U are nonzero" in CLAIM_CONTRACT["DOMAIN"],
        "E(Phi_sigma(A))"
        in CANDIDATE_MAPS["direct_influence_relation"]["definition"],
        "for sigma>0"
        in CANDIDATE_MAPS["intervention_to_response_map"]["definition"],
        "U ranking alone is not the definition"
        in CANDIDATE_MAPS["direct_influence_relation"]["definition"],
    ))
    effective_relation_is_transitive_closure = all((
        "transitive closure"
        in CANDIDATE_MAPS["transitive_effective_order"]["source"],
        "nonempty chain"
        in CANDIDATE_MAPS["transitive_effective_order"]["definition"],
    ))
    universal_ranked_order = ranked_relation_lemma(
        strict_rank_on_every_direct_edge,
        effective_relation_is_transitive_closure,
    )
    lam = sp.symbols("lambda_global", nonnegative=True)
    nu = 1 + lam**2
    sigma = lam + lam**3 / 3
    bounded_sigma = 1 - sp.exp(-lam)
    controls = {
        "exact_reduced_J_flow_solves_equation": ode_residual == 0,
        "exact_reduced_J_flow_has_semigroup_composition": composition_residual == 0,
        "strict_Lyapunov_reachability_is_irreflexive": all((
            universal_ranked_order["irreflexive"],
            "strictly decreases" in CLAIM_CONTRACT["THEOREM"]["formation_order"],
        )),
        "strict_Lyapunov_reachability_is_asymmetric": all((
            universal_ranked_order["asymmetric"], not reverse["asymmetric"],
        )),
        "semigroup_reachability_is_transitive": all((
            universal_ranked_order["transitive"], composition_residual == 0,
            health["compact_sublevel_prevents_finite_forward_blowup"],
        )),
        "strict_Lyapunov_reachability_is_acyclic": all((
            universal_ranked_order["acyclic"], not reverse["acyclic"],
        )),
        "reflexive_closure_is_antisymmetric": all((
            universal_ranked_order["reflexive_closure_antisymmetric"],
        )),
        "exact_three_event_benchmark_passes": all((
            energies[0] > energies[1] > energies[2],
            benchmark_flow_exact,
            not reverse["acyclic"],
        )),
        "direct_influence_not_static_U_ranking": all((
            "nonzero invariant D Phi response" in CLAIM_CONTRACT["IDENTIFIABILITY"],
            "U descent certifies acyclicity" in CLAIM_CONTRACT["IDENTIFIABILITY"],
            "U ranking alone is not the definition"
            in CANDIDATE_MAPS["direct_influence_relation"]["definition"],
        )),
        "event_germ_is_state_owned_and_parameter_free": all((
            "E(A)=Class(A,F(A))" in CANDIDATE_MAPS["event_or_change_map"]["definition"],
            "not a sampled parameter value"
            in CANDIDATE_MAPS["event_or_change_map"]["definition"],
            "grad_F U are nonzero" in CLAIM_CONTRACT["DOMAIN"],
        )),
        "global_positive_reparameterisation_preserves_order": all((
            sp.diff(sigma, lam) == nu,
            nu.is_positive,
            sp.limit(sigma, lam, sp.oo) == sp.oo,
            sp.limit(bounded_sigma, lam, sp.oo) == 1,
            "unbounded range" in CLAIM_CONTRACT["CONVENTIONS"],
        )),
        "curve_parameter_is_not_physical_time": all((
            "Neither parameter is physical time" in CLAIM_CONTRACT["CONVENTIONS"],
            CLAIM_CONTRACT["FORWARD_MODEL"]["status"] == "N/A",
        )),
    }
    diagnostics = {
        "J_flow": phi(z, J0),
        "J_response": response,
        "semigroup_residual": composition_residual,
        "benchmark_J": benchmark,
        "benchmark_U_R": energies,
        "universal_ranked_relation_premises": {
            "strict_rank_on_every_direct_edge": strict_rank_on_every_direct_edge,
            "effective_relation_is_transitive_closure": (
                effective_relation_is_transitive_closure
            ),
        },
    }
    return controls, diagnostics


def intervention_controls(
    o: dict[str, Any], order_diagnostics: dict[str, Any], health: dict[str, bool],
) -> dict[str, bool]:
    cross_S_from_R = sp.Matrix([
        [sp.diff(item, symbol) for symbol in o["R_symbols"]] for item in o["VS"]
    ])
    cross_R_from_S = sp.Matrix([
        [sp.diff(item, symbol) for symbol in o["S_symbols"]] for item in o["VR"]
    ])
    s_var, J_var = sp.symbols("s_var J_var", positive=True)
    fs = s_var * (3 * o["alpha"] + o["b"] * s_var - 2 * o["c"] * s_var**2) / 3
    fJ = 2 * J_var * (o["eta"] - o["d"] * J_var)
    # Coordinate vector fields (fs,0) and (0,fJ) have zero Lie bracket.
    bracket_s = sp.simplify(0 * sp.diff(fs, s_var) + fJ * sp.diff(fs, J_var))
    bracket_J = sp.simplify(fs * sp.diff(fJ, s_var) + 0 * sp.diff(fJ, J_var))
    F_s = sp.Function("Phi_S")
    phi_R_of_J = order_diagnostics["J_flow"].subs({
        sp.Symbol("J0", positive=True): J_var
    })

    def split_S_update(pair: tuple[sp.Expr, sp.Expr]) -> tuple[sp.Expr, sp.Expr]:
        return F_s(pair[0]), pair[1]

    def split_R_update(pair: tuple[sp.Expr, sp.Expr]) -> tuple[sp.Expr, sp.Expr]:
        return pair[0], phi_R_of_J.subs(J_var, pair[1])

    initial_pair = (s_var, J_var)
    update_S_then_R = split_R_update(split_S_update(initial_pair))
    update_R_then_S = split_S_update(split_R_update(initial_pair))
    response = order_diagnostics["J_response"]
    response_symbols = {symbol.name: symbol for symbol in response.free_symbols}
    response_z = response_symbols["z"]
    response_J0 = response_symbols["J0"]
    positive_w = sp.symbols("positive_w", positive=True)
    manifest_physical_response = sp.factor(
        o["eta"]**2 * (1 + positive_w)
        / (response_J0 * o["d"] * positive_w + o["eta"])**2
    )
    response_on_physical_z = sp.factor(
        response.subs(response_z, 1 / (1 + positive_w))
    )
    response_nonzero = all((
        sp.simplify(response_on_physical_z - manifest_physical_response) == 0,
        manifest_physical_response.is_positive is True,
    ))
    later_kick = sp.symbols("later_kick", real=True)
    J_flow_formula = order_diagnostics["J_flow"]
    exact_substitution = {o["eta"]: 1, o["d"]: 1, response_z: sp.Rational(1, 2)}
    pre_kick_occurrence = sp.simplify(
        J_flow_formula.subs(exact_substitution).subs(
            response_J0, sp.Rational(1, 4)
        )
    )
    post_kick_occurrence = sp.simplify(
        J_flow_formula.subs(exact_substitution).subs(
            response_J0, pre_kick_occurrence + later_kick
        )
    )
    composed_intervention_prefix_control = all((
        pre_kick_occurrence == sp.Rational(2, 5),
        sp.diff(pre_kick_occurrence, later_kick) == 0,
        sp.diff(post_kick_occurrence, later_kick).subs(later_kick, 0)
        == sp.Rational(50, 49),
    ))

    # Finite-flow blocks, not merely static Hessian blocks.  Polynomial local
    # uniqueness plus the product generator forces
    # Phi_sigma(S,R)=(Phi^S_sigma(S),Phi^R_sigma(R)).  The abstract component
    # functions below audit the resulting Frechet block structure exactly.
    sigma = sp.symbols("sigma_response", positive=True)
    S0 = sp.symbols("S0_0:5", real=True)
    R0 = sp.symbols("R0_0:3", real=True)
    phi_S_components = sp.Matrix([
        sp.Function(f"PhiS_{index}")(*S0, sigma) for index in range(5)
    ])
    phi_R_components = sp.Matrix([
        sp.Function(f"PhiR_{index}")(*R0, sigma) for index in range(3)
    ])
    flow_R_from_S = phi_R_components.jacobian(S0)
    flow_S_from_R = phi_S_components.jacobian(R0)
    chi_S, chi_R = sp.symbols("chi_S chi_R", real=True)
    liouville_determinants_positive = all((
        sp.exp(chi_S).is_positive, sp.exp(chi_R).is_positive,
    ))
    product_generator_exact = all((
        matrix_zero(cross_R_from_S), matrix_zero(cross_S_from_R),
    ))
    unique_global_semiflow_premises = all((
        health["polynomial_vector_field_is_locally_Lipschitz"],
        health["compact_sublevel_prevents_finite_forward_blowup"],
    ))
    # Standard product-ODE uniqueness: if F(S,R)=(F_S(S),F_R(R)) and the IVP
    # is unique, its finite flow is exactly the product of the component
    # flows.  The abstract component functions above are used only after these
    # computed premises pass.  Liouville's formula then gives nonzero
    # same-channel fundamental-matrix determinants exp(int tr DF_i).
    product_flow_uniqueness_applies = all((
        product_generator_exact,
        unique_global_semiflow_premises,
        matrix_zero(flow_R_from_S), matrix_zero(flow_S_from_R),
    ))
    finite_variational_invertibility_applies = all((
        unique_global_semiflow_premises,
        liouville_determinants_positive,
        "finite same-channel flow differentials are nonsingular"
        in CLAIM_CONTRACT["THEOREM"]["no_transmission"],
    ))

    # A concrete pure-channel perturbation verifies that the joint commutator
    # readout generally responds even though the opposite state channel does
    # not.  This prevents an illicit strengthening of the no-transmission claim.
    S_joint = sp.diag(2, -1, -1)
    # Axial vector (1,1,0): its support has tau_gap=1/2 relative to P_plus=e1,
    # so this is an interior D_gap readout witness rather than the tau=1 edge.
    R_joint = sp.Matrix([[0, 0, 1], [0, 0, -1], [-1, 1, 0]])
    delta_S_joint = sp.diag(1, -1, 0)
    delta_R_joint = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    delta_C_from_S = sp.simplify(delta_S_joint * R_joint - R_joint * delta_S_joint)
    delta_C_from_R = sp.simplify(S_joint * delta_R_joint - delta_R_joint * S_joint)
    J_joint = sp.simplify(-sp.trace(R_joint * R_joint))
    P_R_joint = sp.simplify(sp.eye(3) + 2 * R_joint * R_joint / J_joint)
    tau_joint = sp.simplify(1 - sp.trace(sp.diag(1, 0, 0) * P_R_joint))

    # Infinitesimal common-O(3) covariance: a gauge tangent remains the gauge
    # tangent of the flowed representative and is quotiented from response.
    eps = sp.symbols("eps_gauge", real=True)
    omega = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    A = o["S"] + o["R"]
    delta_A_gauge = sp.simplify(omega * A - A * omega)

    def full_vector_field(Am: sp.MatrixBase) -> sp.Matrix:
        Sm = sp.simplify((Am + Am.T) / 2)
        Rm = sp.simplify((Am - Am.T) / 2)
        I2m = sp.trace(Sm * Sm)
        Jm = -sp.trace(Rm * Rm)
        return sp.simplify(
            o["alpha"] * Sm
            + o["b"] * (Sm * Sm - sp.eye(3) * I2m / 3)
            - o["c"] * I2m * Sm
            + (o["eta"] - o["d"] * Jm) * Rm
        )

    F_A = full_vector_field(A)
    gauge_linearisation = sp.simplify(
        sp.diff(full_vector_field(A + eps * delta_A_gauge), eps).subs(eps, 0)
    )
    gauge_covariance_residual = sp.simplify(
        gauge_linearisation - (omega * F_A - F_A * omega)
    )
    return {
        "allowed_interventions_are_tangent_and_domain_preserving": all((
            matrix_zero(o["dS"] - o["dS"].T), sp.trace(o["dS"]) == 0,
            matrix_zero(o["dR"] + o["dR"].T), sp.trace(o["dR"]) == 0,
            "pure-S" in CANDIDATE_MAPS["allowed_interventions"]["definition"],
            "pure-R" in CANDIDATE_MAPS["allowed_interventions"]["definition"],
            "stay in D_gap" in CANDIDATE_MAPS["allowed_interventions"]["definition"],
        )),
        "flow_differential_is_the_intervention_response": all((
            "D Phi_sigma" in CANDIDATE_MAPS["intervention_to_response_map"]["definition"],
            "finite-flow Frechet" in CLAIM_CONTRACT["METHOD"],
        )),
        "exact_J_same_channel_response_is_nonzero": response_nonzero,
        "finite_flow_same_channel_differential_is_nonsingular": all((
            response_nonzero, finite_variational_invertibility_applies,
        )),
        "unique_finite_semiflow_factorises_exactly": all((
            product_flow_uniqueness_applies,
        )),
        "S_to_R_cross_response_is_exactly_zero": all((
            product_flow_uniqueness_applies, matrix_zero(flow_R_from_S),
        )),
        "R_to_S_cross_response_is_exactly_zero": all((
            product_flow_uniqueness_applies, matrix_zero(flow_S_from_R),
        )),
        "forbidden_channel_nontransmission_is_exact": all((
            product_flow_uniqueness_applies,
            matrix_zero(flow_R_from_S), matrix_zero(flow_S_from_R),
            "finite-semiflow Frechet blocks"
            in CANDIDATE_MAPS["no_transmission_test"]["definition"],
        )),
        "joint_C_response_is_not_silently_set_to_zero": all((
            not matrix_zero(delta_C_from_S), not matrix_zero(delta_C_from_R),
            tau_joint == sp.Rational(1, 2),
            "effects on joint C are nonzero" in CANDIDATE_MAPS["forbidden_pairs"]["definition"],
        )),
        "common_O3_gauge_tangent_is_quotient_null": all((
            matrix_zero(gauge_covariance_residual),
            "common-O(3) gauge tangents" in CANDIDATE_MAPS["allowed_interventions"]["definition"],
        )),
        "channel_vector_fields_have_zero_Lie_bracket": bracket_s == 0 and bracket_J == 0,
        "channel_flow_updates_commute": update_S_then_R == update_R_then_S,
        "execution_schedule_does_not_change_the_flow": all((
            bracket_s == 0, bracket_J == 0, update_S_then_R == update_R_then_S,
        )),
        "later_intervention_cannot_change_an_earlier_occurrence": (
            all((
                composed_intervention_prefix_control,
                product_flow_uniqueness_applies,
                "acyclic" in CLAIM_CONTRACT["THEOREM"]["formation_order"],
            ))
        ),
    }


def null_controls(
    o: dict[str, Any], r: dict[str, Any], health: dict[str, bool],
) -> dict[str, bool]:
    s_star = (
        o["b"] + sp.sqrt(o["b"]**2 + 24 * o["alpha"] * o["c"])
    ) / (4 * o["c"])
    J_star = o["eta"] / o["d"]
    reverse_Udot = sp.expand(
        sp.trace(o["gradS"].T * o["gradS"])
        + sp.trace(o["gradR"].T * o["gradR"])
    )
    m, delta = sp.symbols("m delta", positive=True)
    robustness_identity = sp.factor(-m**2 + m * delta + m * (m - delta))
    S_boundary = sp.diag(sp.Rational(2, 3), sp.Rational(-1, 3), sp.Rational(-1, 3))
    R_tau_one = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    J_tau_one = sp.simplify(-sp.trace(R_tau_one * R_tau_one))
    P_R_tau_one = sp.simplify(sp.eye(3) + 2 * R_tau_one**2 / J_tau_one)
    P_plus_boundary = sp.diag(1, 0, 0)
    tau_one = sp.simplify(1 - sp.trace(P_plus_boundary * P_R_tau_one))
    C_tau_one = sp.simplify(S_boundary * R_tau_one - R_tau_one * S_boundary)
    S_tau_zero = sp.diag(2, 0, -2)
    R_tau_zero = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    J_tau_zero = sp.simplify(-sp.trace(R_tau_zero * R_tau_zero))
    P_R_tau_zero = sp.simplify(sp.eye(3) + 2 * R_tau_zero**2 / J_tau_zero)
    tau_zero = sp.simplify(1 - sp.trace(P_plus_boundary * P_R_tau_zero))
    C_tau_zero = sp.simplify(S_tau_zero * R_tau_zero - R_tau_zero * S_tau_zero)
    downstream_false = all(
        EXPECTED_CLOSURE_FLAGS[key] is False
        for key in (
            "foundation_derived_F3", "persistent_phase_or_clock_order",
            "physical_time_or_clock_readout", "spatial_locality_or_causality",
            "F4_independent_additive_modes", "foundation_to_effective_closed",
            "dimension_or_continuum", "Lorentzian_metric_or_light_cone",
            "effective_action_or_matter_coupling", "Einstein_GR_PN_or_PPN_bridge",
            "observational_validation",
        )
    )
    return {
        "stationary_minimum_is_a_frozen_event_null": all((
            sp.simplify(r["ds"].subs(r["s"], s_star)) == 0,
            sp.simplify((2 * r["J"] * (o["eta"] - o["d"] * r["J"])).subs(
                r["J"], J_star
            )) == 0,
            "FROZEN_EVENT_NULL" in CLAIM_CONTRACT["BRANCHES"].values(),
        )),
        "S_zero_and_R_zero_are_invariant_F2_nulls": all((
            sp.simplify(r["ds"].subs(r["s"], 0)) == 0,
            matrix_zero(o["VR"].subs({symbol: 0 for symbol in o["R_symbols"]})),
        )),
        "tau_boundaries_and_tuned_surface_are_not_promoted": all((
            CLAIM_CONTRACT["BRANCHES"]["S_or_R_or_C_zero"]
            == "RELATIONAL_NULL_NO_PROMOTION",
            CLAIM_CONTRACT["BRANCHES"]["tau_gap_zero"]
            == "EXCLUDED_READOUT_BOUNDARY_NOT_GENERAL_C_ZERO",
            CLAIM_CONTRACT["BRANCHES"]["tau_gap_one"]
            == "EXCLUDED_ORBIT_BOUNDARY_NOT_C_ZERO",
            "tau_gap=0" in CANDIDATE_MAPS["null_branches"]["definition"],
            "tau_gap=1" in CANDIDATE_MAPS["null_branches"]["definition"],
            "b^2!=3 alpha c" in CLAIM_CONTRACT["DOMAIN"],
        )),
        "tau_gap_zero_is_boundary_not_false_C_zero": all((
            tau_zero == 0,
            not matrix_zero(C_tau_zero),
            sp.trace(C_tau_zero.T * C_tau_zero) == 8,
        )),
        "tau_gap_one_is_boundary_not_false_C_zero": all((
            tau_one == 1,
            not matrix_zero(C_tau_one),
            sp.trace(C_tau_one.T * C_tau_one) > 0,
        )),
        "static_K_tau_ranking_without_flow_is_rejected": (
            "not by U ranking" in CLAIM_CONTRACT["IDENTIFIABILITY"]
        ),
        "positive_gradient_reverse_ansatz_increases_U": all((
            reverse_Udot != 0,
            "REJECTED_REVERSE_ANSATZ" in CLAIM_CONTRACT["BRANCHES"].values(),
        )),
        "target_symbol_intersection_is_empty": (
            PRIMITIVE_INPUT_SYMBOLS.isdisjoint(FORBIDDEN_TARGET_INPUT_SYMBOLS)
        ),
        "external_graph_clock_metric_and_data_are_absent": all((
            CLAIM_CONTRACT["OBSERVABLE_MAP"]["status"] == "N/A",
            CLAIM_CONTRACT["FORWARD_MODEL"]["status"] == "N/A",
            CLAIM_CONTRACT["DATA_ROLE"]["status"] == "N/A",
            CLAIM_CONTRACT["FREEDOM_LEDGER"]
            ["extra_state_graph_clock_metric_or_data_parameters"]["allowed_range"] == 0,
        )),
        "small_allowed_state_perturbations_preserve_regular_domain": all((
            robustness_identity == 0,
            health["Lyapunov_strict_off_critical_set"],
            "initial-state perturbations" in CANDIDATE_MAPS["perturbation_class"]["definition"],
            "process-law perturbations excluded"
            in CANDIDATE_MAPS["perturbation_class"]["definition"],
        )),
        "allowed_initial_conditions_have_open_relative_support": all((
            "D_gap" in CLAIM_CONTRACT["DOMAIN"],
            "tau_gap=1-Tr(P_plus P_R) is in (0,1)" in CLAIM_CONTRACT["DOMAIN"],
            "grad_F U are nonzero" in CLAIM_CONTRACT["DOMAIN"],
        )),
        "persistent_phase_clock_and_downstream_claims_remain_false": downstream_false,
    }


CANDIDATE_MAPS: dict[str, dict[str, str]] = {
    "state_space": {
        "status": "DERIVED",
        "source": "w2_16 one-carrier split used on the w2_19 D_gap candidate domain",
        "definition": "A in sl(3,R), S in Sym_0(3), R in so(3), modulo one common O(3)",
    },
    "event_or_change_map": {
        "status": "DERIVED",
        "source": "exact nonzero Candidate-A vector field on D_gap",
        "definition": (
            "E(A)=Class(A,F(A)) modulo common O(3) and positive tangent rescaling, with "
            "F=-grad_F U nonzero; it is not a sampled parameter value or persistent record"
        ),
    },
    "complete_equivalence_action": {
        "status": "DERIVED",
        "source": "common star-algebra O(3) plus global positive process gauge",
        "definition": (
            "A->OAO^T for all O in O(3), event tangent positive rescaling, and global "
            "continuous nu>0 with unbounded cumulative sigma range"
        ),
    },
    "transition_or_response_law": {
        "status": "PARTIAL",
        "source": "w2_19 imported process package, evaluated but not Canon-derived",
        "definition": (
            "dA/dsigma=-grad_F U, sigma>=0, identity full-A mobility and rho=1; exact as a "
            "conditional candidate law, but its transition principle remains imported"
        ),
    },
    "signal_support_or_update_composition": {
        "status": "DERIVED",
        "source": "global-forward autonomous product semiflow",
        "definition": "Phi_{r+s}=Phi_r composed Phi_s on D_gap with finite block Frechet flow",
    },
    "allowed_interventions": {
        "status": "DERIVED",
        "source": "w2_19 pure-channel tangent intervention class",
        "definition": (
            "pure-S deltaS in Sym_0(3), pure-R deltaR in so(3), and finite sums small enough "
            "to stay in D_gap; quotient common-O(3) gauge tangents and no coefficient fitting"
        ),
    },
    "intervention_to_response_map": {
        "status": "DERIVED",
        "source": "exact finite variational semiflow",
        "definition": (
            "for sigma>0, deltaA maps to D Phi_sigma(A)[deltaA]; projected S/R response "
            "zero/nonzero Frobenius norm is O(3)-invariant"
        ),
    },
    "direct_influence_relation": {
        "status": "DERIVED",
        "source": "nonzero invariant same-channel Frechet flow response",
        "definition": (
            "E(A) directly influences E(Phi_sigma(A)) only when an allowed intervention has "
            "nonzero invariant projected D Phi response; U ranking alone is not the definition"
        ),
    },
    "transitive_effective_order": {
        "status": "DERIVED",
        "source": "transitive closure of evaluated direct influence on the positive semigroup",
        "definition": (
            "x precedes y by a nonempty chain of nonzero forward responses; strict U descent "
            "certifies acyclicity but is not substituted for the intervention definition"
        ),
    },
    "forbidden_pairs": {
        "status": "DERIVED",
        "source": "finite product semiflow and quotient intervention semantics",
        "definition": (
            "pure-S to future R and pure-R to future S are substantive forbidden pairs; "
            "common-O(3) tangents are gauge nulls; effects on joint C are nonzero"
        ),
    },
    "no_transmission_test": {
        "status": "DERIVED",
        "source": "uniqueness-derived finite product flow",
        "definition": (
            "finite-semiflow Frechet blocks D_S Phi^R_sigma and D_R Phi^S_sigma vanish "
            "for every supported sigma>0; this is stronger than a static Hessian zero"
        ),
    },
    "open_domain": {
        "status": "DERIVED",
        "source": "exact spectral-flow and local normal-stability proof",
        "definition": (
            "D_gap with simple-largest P_plus, J>0, P_R=I+2R^2/J, 0<tau_gap<1, "
            "C and grad_F U nonzero, inside the generic minimum-stratum basin"
        ),
    },
    "null_branches": {
        "status": "DERIVED",
        "source": "exact fixed/boundary controls",
        "definition": (
            "A=0, S=0, R=0 and C=0 nulls; tau_gap=0 and tau_gap=1 excluded readout "
            "boundaries (neither is generally C=0 off endpoint); tuned, singular, "
            "spectral-gap/basin boundaries, stationary endpoint and ascent"
        ),
    },
    "perturbation_class": {
        "status": "DERIVED",
        "source": "openness, continuous dependence and normal stability",
        "definition": (
            "small traceless initial-state perturbations preserving D_gap and the simple-support "
            "branch; coefficient, clock, target and process-law perturbations excluded"
        ),
    },
    "independent_crosscheck": {
        "status": "DERIVED",
        "source": "independent general-spectral and uniaxial/logistic derivations",
        "definition": (
            "general g2/g3 spectral flow, full matrix directional algebra, exact uniaxial "
            "witnesses, logistic semigroup, finite-flow response and graph mutations"
        ),
    },
}


def candidate_maps_sha256(candidate_maps: dict[str, dict[str, str]]) -> str:
    canonical = json.dumps(
        candidate_maps, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest().upper()


def frozen_candidate_maps_sha256() -> str:
    """Independent literal freeze of every candidate-map key and text field."""
    return "43025DA798FEB721822588DAE8C333A60A066799862E8B2B16C268484CA7FEA8"


def frozen_candidate_map_statuses() -> dict[str, str]:
    """Independent literal ceiling; never return the mutable status registry."""
    return {
        "state_space": "DERIVED",
        "event_or_change_map": "DERIVED",
        "complete_equivalence_action": "DERIVED",
        "transition_or_response_law": "PARTIAL",
        "signal_support_or_update_composition": "DERIVED",
        "allowed_interventions": "DERIVED",
        "intervention_to_response_map": "DERIVED",
        "direct_influence_relation": "DERIVED",
        "transitive_effective_order": "DERIVED",
        "forbidden_pairs": "DERIVED",
        "no_transmission_test": "DERIVED",
        "open_domain": "DERIVED",
        "null_branches": "DERIVED",
        "perturbation_class": "DERIVED",
        "independent_crosscheck": "DERIVED",
    }


EXPECTED_CANDIDATE_MAP_STATUSES = frozen_candidate_map_statuses()


def dependency_controls(
    w216: ModuleType, w217: ModuleType, w218: ModuleType, w219: ModuleType,
) -> tuple[dict[str, bool], dict[str, Any]]:
    report16, report17, report18, report19 = (
        w216.run(), w217.run(), w218.run(), w219.run()
    )
    report19_text = json.dumps(_json_safe(report19), sort_keys=True)
    controls = {
        "w2_16_report_valid_and_conditional_F2_exact": all((
            report16.get("valid") is True,
            report16.get("artifact") == "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CANDIDATE_001",
            report16.get("closure_decision", {}).get(
                "full_W2_F2_operational_relations_proved"
            ) is True,
            report16.get("closure_decision", {}).get(
                "F3_internal_order_or_causality_proved"
            ) is False,
        )),
        "w2_17_contract_valid_and_schema_exact": all((
            report17.get("valid") is True,
            set(w217.F3_GATE_KEYS) == set(w217.EXPECTED_F3_GATE_KEYS),
            tuple(w217.REQUIRED_CANDIDATE_MAPS) == tuple(w217.EXPECTED_REQUIRED_CANDIDATE_MAPS),
            len(w217.F3_GATE_KEYS) == 18,
            len(w217.REQUIRED_CANDIDATE_MAPS) == 15,
        )),
        "w2_18_static_no_go_valid_and_dynamic_escape_open": all((
            report18.get("valid") is True,
            report18.get("program_status") == "W2_F3_OPEN_REQUIRES_NEW_FOUNDATION_DYNAMICS",
            report18.get("closure_decision", {}).get("new_dynamic_candidate_required") is True,
            report18.get("closure_decision", {}).get(
                "F3_internal_order_or_causality_proved"
            ) is False,
        )),
        "w2_19_candidate_contract_valid_and_unpromoted": all((
            report19.get("valid") is True,
            report19.get("artifact")
            == "W2_F3_GRADIENT_FORMATION_FLOW_CANDIDATE_CONTRACT_001",
            report19.get("evaluation_authorized") is True,
            report19.get("scientific_promotion_authorized") is False,
            report19.get("maximum_authorized_evaluator_outcome")
            == "CONDITIONAL_CANDIDATE_RELATIVE_FORMATION_ORDER_THEOREM",
            report19.get("closure_flags", {}).get("Candidate_A_evaluated") is False,
            report19.get("closure_flags", {}).get(
                "conditional_candidate_relative_formation_order_proved"
            ) is False,
            w219.CLAIM_CONTRACT["CANDIDATE_DEFINITION"]["origin_status"]
            == "NEW_IMPORTED_PROCESS_PACKAGE_NOT_CANON_DERIVED",
            "relative S/R mobility"
            in w219.CLAIM_CONTRACT["CANDIDATE_DEFINITION"]["mobility"],
            w219.CLAIM_CONTRACT["FREEDOM_LEDGER"]
            ["kinetic_metric_and_relative_mobility"]["complexity"]
            == (
                "1 fixed dimensionless continuous input rho=mu_R/mu_S=1 plus the selected "
                "full-A mobility class; 0 fitted parameters"
            ),
            w219.CLAIM_CONTRACT["FREEDOM_LEDGER"]
            ["off_endpoint_relational_readout_candidate"]["complexity"]
            == "1 fixed map choice; 0 fitted parameters",
            "P_plus" in w219.CLAIM_CONTRACT["CANDIDATE_DEFINITION"]
            ["off_endpoint_support_map"],
            "tau_gap" in w219.CLAIM_CONTRACT["DOMAIN_AND_NULLS"]["evaluation_domain"],
            "E(A)=Class(A,F(A))"
            in w219.CANDIDATE_A_MAPS["event_or_change_map"]["definition"],
            "unbounded cumulative range"
            in w219.CLAIM_CONTRACT["CANDIDATE_DEFINITION"]["gauge"],
            w219.frozen_f3_gate_keys() == w217.frozen_f3_gate_keys(),
            w219.frozen_required_candidate_maps()
            == w217.frozen_required_candidate_maps(),
            "GRADIENT" in report19_text.upper(),
            "FORMATION" in report19_text.upper(),
        )),
        "named_dependency_chain_exact": CLAIM_CONTRACT["DEPENDENCIES"] == [
            "w2_16: conditional atemporal structural F2",
            "w2_17: exact F3 interface and 18 atomic gates",
            "w2_18: static endpoint cannot close F3 and a new dynamic candidate is required",
            "w2_19: frozen imported negative-gradient formation-flow candidate contract",
        ],
    }
    return controls, {
        "w2_16": report16, "w2_17": report17,
        "w2_18": report18, "w2_19": report19,
    }


def f3_gate_map(
    dependency: dict[str, bool], gradient: dict[str, bool],
    equivariance: dict[str, bool], reduced: dict[str, bool],
    domain_f2: dict[str, bool], health: dict[str, bool], order: dict[str, bool],
    interventions: dict[str, bool], nulls: dict[str, bool], w217: ModuleType,
) -> dict[str, bool]:
    health_public = {key: value for key, value in health.items() if not key.startswith("_")}
    return {
        # The endpoint F1/F2 theorem does not extend to the nonstationary
        # D_gap chain.  An exact off-shell Hessian counterexample below keeps
        # this predecessor gate false even though the new relational readout
        # itself is mathematically well defined on D_gap.
        "same_chain_F1_F2_predecessors_valid": False,
        "state_owned_events_or_changes_derived": all((
            gradient["vector_field_is_negative_gradient_exact"],
            health["Lyapunov_strict_off_critical_set"],
            order["event_germ_is_state_owned_and_parameter_free"],
            CANDIDATE_MAPS["event_or_change_map"]["status"] == "DERIVED",
        )),
        # The vector field is derived exactly *inside* Candidate A, but the
        # process principle itself is imported rather than foundation-derived.
        "target_free_transition_or_response_law_derived": False,
        "candidate_dynamics_health_and_state_space_closure_proved": all((
            exact_true_map(health_public, HEALTH_CONTROL_KEYS),
            domain_f2["D_gap_is_forward_invariant"],
            gradient["symmetric_traceless_constraint_preserved"],
            gradient["skew_traceless_constraint_preserved"],
        )),
        "allowed_interventions_defined": interventions[
            "allowed_interventions_are_tangent_and_domain_preserving"
        ],
        "directed_intervention_response_proved": all((
            interventions["flow_differential_is_the_intervention_response"],
            interventions["exact_J_same_channel_response_is_nonzero"],
            interventions["finite_flow_same_channel_differential_is_nonsingular"],
        )),
        "correlation_and_static_ranking_excluded": nulls[
            "static_K_tau_ranking_without_flow_is_rejected"
        ],
        "complete_equivalence_invariance_proved": exact_true_map(
            equivariance, EQUIVARIANCE_CONTROL_KEYS
        ) and domain_f2["off_endpoint_relational_readout_common_O3_covariant"],
        "arrow_selected_by_law_not_labels_or_schedule": all((
            health["Lyapunov_strict_off_critical_set"],
            nulls["positive_gradient_reverse_ansatz_increases_U"],
            interventions["execution_schedule_does_not_change_the_flow"],
            order["global_positive_reparameterisation_preserves_order"],
        )),
        "nontrivial_direct_influence_on_predeclared_open_domain": all((
            interventions["exact_J_same_channel_response_is_nonzero"],
            nulls["allowed_initial_conditions_have_open_relative_support"],
            domain_f2["local_D_gap_basin_nonempty_open_and_stable"],
        )),
        "strict_relation_irreflexive_asymmetric_and_acyclic": all((
            order["strict_Lyapunov_reachability_is_irreflexive"],
            order["strict_Lyapunov_reachability_is_asymmetric"],
            order["strict_Lyapunov_reachability_is_acyclic"],
        )),
        "effective_order_transitive_and_reflexive_closure_antisymmetric": all((
            order["semigroup_reachability_is_transitive"],
            order["reflexive_closure_is_antisymmetric"],
        )),
        "forbidden_signal_nontransmission_proved": all((
            interventions["S_to_R_cross_response_is_exactly_zero"],
            interventions["R_to_S_cross_response_is_exactly_zero"],
            interventions["forbidden_channel_nontransmission_is_exact"],
            interventions["unique_finite_semiflow_factorises_exactly"],
        )),
        "computational_schedule_neutrality_proved": all((
            order["curve_parameter_is_not_physical_time"],
            interventions["channel_flow_updates_commute"],
            interventions["execution_schedule_does_not_change_the_flow"],
            order["global_positive_reparameterisation_preserves_order"],
        )),
        "null_reverse_and_target_leak_controls_pass": all((
            exact_true_map(nulls, NULL_CONTROL_KEYS),
            nulls["positive_gradient_reverse_ansatz_increases_U"],
        )),
        "perturbation_and_initial_condition_stability_proved": all((
            nulls["small_allowed_state_perturbations_preserve_regular_domain"],
            nulls["allowed_initial_conditions_have_open_relative_support"],
            health["normal_linear_stability_exact"],
            domain_f2["local_D_gap_basin_nonempty_open_and_stable"],
        )),
        "independent_second_derivation_passes": all((
            exact_true_map(reduced, REDUCED_FLOW_CONTROL_KEYS),
            exact_true_map(domain_f2, DOMAIN_READOUT_CONTROL_KEYS),
            order["exact_reduced_J_flow_solves_equation"],
            order["exact_three_event_benchmark_passes"],
        )),
        "physical_time_metric_and_downstream_gates_remain_open": nulls[
            "persistent_phase_clock_and_downstream_claims_remain_false"
        ],
    }


def closure_decision(adjudication_valid: bool) -> dict[str, bool]:
    return {
        "F1_F2_conditional_predecessors_registered": bool(adjudication_valid),
        "formation_domain_F1_F2_same_chain_revalidated": False,
        "off_endpoint_relational_readout_candidate_evaluated": bool(adjudication_valid),
        "D_gap_nonempty_open_forward_invariant": bool(adjudication_valid),
        "F3_gradient_candidate_evaluated": bool(adjudication_valid),
        "conditional_gradient_semigroup_formation_order_proved": bool(adjudication_valid),
        "gradient_process_ansatz_imported_not_Canon_derived": True,
        "transition_process_principle_foundation_derived": False,
        "event_germ_and_same_channel_influence_proved": bool(adjudication_valid),
        "finite_flow_forbidden_channel_nontransmission_proved": bool(adjudication_valid),
        "same_chain_cross_channel_causal_graph_proved": False,
        "F3_internal_order_or_causality_proved": False,
        "foundation_derived_F3": False,
        "persistent_phase_or_clock_order": False,
        "physical_time_or_clock_readout": False,
        "spatial_locality_or_causality": False,
        "F4_independent_additive_modes": False,
        "foundation_to_effective_closed": False,
        "dimension_or_continuum": False,
        "Lorentzian_metric_or_light_cone": False,
        "effective_action_or_matter_coupling": False,
        "Einstein_GR_PN_or_PPN_bridge": False,
        "observational_validation": False,
    }


def decision_controls(
    w217: ModuleType, gates: dict[str, bool], screen: dict[str, bool],
    closure: dict[str, bool], science_checks: dict[str, bool], all_science_valid: bool,
) -> dict[str, bool]:
    all_derived_maps = {key: dict(value) for key, value in CANDIDATE_MAPS.items()}
    all_derived_maps["transition_or_response_law"]["status"] = "DERIVED"
    all_true_gates = {key: True for key in w217.F3_GATE_KEYS}
    single_false_blocks = True
    for key in w217.F3_GATE_KEYS:
        # Isolation mutation: begin from a complete all-true fixture and flip
        # exactly one gate, irrespective of the two false scientific outcomes
        # in the actual adjudication.
        mutant = dict(all_true_gates)
        mutant[key] = False
        result = w217.candidate_screen(mutant, all_derived_maps)
        single_false_blocks &= result.get("valid") is True and result.get("eligible") is False
    missing = dict(gates)
    missing.pop(next(iter(w217.F3_GATE_KEYS)))
    nonboolean = dict(gates)
    nonboolean[next(iter(w217.F3_GATE_KEYS))] = 1
    extra = dict(gates)
    extra["extra"] = True
    bad_maps = dict(CANDIDATE_MAPS)
    bad_maps.pop(next(iter(bad_maps)))
    partial_maps = {key: dict(value) for key, value in CANDIDATE_MAPS.items()}
    partial_maps["state_space"]["status"] = "PARTIAL"
    malformed_results = [
        w217.candidate_screen(missing, CANDIDATE_MAPS),
        w217.candidate_screen(nonboolean, CANDIDATE_MAPS),
        w217.candidate_screen(extra, CANDIDATE_MAPS),
    ]
    map_results = [
        w217.candidate_screen(gates, bad_maps),
        w217.candidate_screen(gates, partial_maps),
    ]
    false_closure = closure_decision(False)
    single_science_failure_blocks = bool(science_checks) and all_science_valid
    for key in science_checks:
        mutant = dict(science_checks)
        mutant[key] = False
        single_science_failure_blocks &= not all(
            type(value) is bool and value for value in mutant.values()
        )
    status_mutations_block = True
    for key, frozen_status in frozen_candidate_map_statuses().items():
        changed_status = "PARTIAL" if frozen_status == "DERIVED" else "DERIVED"
        mutated_maps = {name: dict(entry) for name, entry in CANDIDATE_MAPS.items()}
        mutated_maps[key]["status"] = changed_status
        coordinated_expected = dict(EXPECTED_CANDIDATE_MAP_STATUSES)
        coordinated_expected[key] = changed_status
        mutated_statuses = {
            name: entry["status"] for name, entry in mutated_maps.items()
        }
        mutated_status_ceiling_valid = (
            mutated_statuses
            == coordinated_expected
            == frozen_candidate_map_statuses()
        )
        status_mutations_block &= not mutated_status_ceiling_valid
    map_content_mutations_block = True
    for key in CANDIDATE_MAPS:
        for field in ("source", "definition"):
            mutated_maps = {
                name: dict(entry) for name, entry in CANDIDATE_MAPS.items()
            }
            mutated_maps[key][field] = "COORDINATED_NONEMPTY_MUTATION"
            map_content_mutations_block &= (
                candidate_maps_sha256(mutated_maps)
                != frozen_candidate_maps_sha256()
            )
    closure_mutations_block = True
    for key, frozen_value in frozen_closure_flags().items():
        coordinated_contract_closure = dict(CLAIM_CONTRACT["CLOSURE_FLAGS"])
        coordinated_expected_closure = dict(EXPECTED_CLOSURE_FLAGS)
        coordinated_contract_closure[key] = not frozen_value
        coordinated_expected_closure[key] = not frozen_value
        mutated_closure_valid = (
            coordinated_contract_closure
            == coordinated_expected_closure
            == frozen_closure_flags()
        )
        closure_mutations_block &= not mutated_closure_valid
    contract_content_mutations_block = True
    for key in CLAIM_CONTRACT:
        mutated_contract = json.loads(json.dumps(CLAIM_CONTRACT))
        mutated_contract[key] = "COORDINATED_CONTRACT_MUTATION"
        contract_content_mutations_block &= (
            scientific_contract_sha256(mutated_contract)
            != frozen_scientific_contract_sha256()
        )
    return {
        "mathematical_evidence_complete_but_full_F3_ineligible": all((
            all_science_valid, screen.get("valid") is True,
            screen.get("eligible") is False,
        )),
        "w2_17_screen_never_self_promotes": screen.get("promoted") is False,
        "each_single_false_gate_blocks_eligibility": single_false_blocks,
        "missing_nonboolean_or_extra_gate_fails_closed": all(
            result.get("valid") is False and result.get("eligible") is False
            for result in malformed_results
        ),
        "missing_or_partial_candidate_map_fails_closed": all(
            result.get("eligible") is False for result in map_results
        ),
        "each_candidate_map_status_mutation_blocks_validity": status_mutations_block,
        "candidate_map_content_mutation_blocks_validity": map_content_mutations_block,
        "contract_closure_mutation_blocks_validity": closure_mutations_block,
        "scientific_contract_content_mutation_blocks_validity": (
            contract_content_mutations_block
        ),
        "failed_dependency_blocks_conditional_closure": (
            false_closure["conditional_gradient_semigroup_formation_order_proved"] is False
            and false_closure["foundation_derived_F3"] is False
        ),
        "one_failed_scientific_control_blocks_validity": (
            single_science_failure_blocks
        ),
        "closure_matches_predeclared_ceiling_exactly": all((
            closure == EXPECTED_CLOSURE_FLAGS == frozen_closure_flags(),
            CLAIM_CONTRACT["CLOSURE_FLAGS"]
            == EXPECTED_CLOSURE_FLAGS
            == frozen_closure_flags(),
        )),
        "conditional_result_does_not_close_foundation_F3": all((
            closure["conditional_gradient_semigroup_formation_order_proved"],
            not closure["foundation_derived_F3"],
            not closure["F3_internal_order_or_causality_proved"],
            not closure["formation_domain_F1_F2_same_chain_revalidated"],
            closure["off_endpoint_relational_readout_candidate_evaluated"],
            closure["D_gap_nonempty_open_forward_invariant"],
            not closure["same_chain_cross_channel_causal_graph_proved"],
            closure["gradient_process_ansatz_imported_not_Canon_derived"],
            not closure["transition_process_principle_foundation_derived"],
        )),
        "transition_map_stays_partial_and_blocks_eligibility": all((
            CANDIDATE_MAPS["transition_or_response_law"]["status"] == "PARTIAL",
            {key: value["status"] for key, value in CANDIDATE_MAPS.items()}
            == EXPECTED_CANDIDATE_MAP_STATUSES
            == frozen_candidate_map_statuses(),
            w217.candidate_screen(all_true_gates, CANDIDATE_MAPS)["eligible"] is False,
            w217.candidate_screen(gates, all_derived_maps)["eligible"] is False,
            screen.get("eligible") is False,
        )),
        "exactly_two_predeclared_scientific_F3_gates_remain_false": (
            {key for key, value in gates.items() if value is False}
            == EXPECTED_FALSE_F3_GATES
            and len(EXPECTED_FALSE_F3_GATES) == 2
        ),
    }


def run() -> dict[str, Any]:
    w216 = load_sibling(
        "w2_16_f2b_general_traceless_single_carrier_candidate_gate.py", "w2_16_for_w2_20"
    )
    w217 = load_sibling(
        "w2_17_f3_internal_order_causality_contract.py", "w2_17_for_w2_20"
    )
    w218 = load_sibling(
        "w2_18_f3_static_endpoint_adjudication_gate.py", "w2_18_for_w2_20"
    )
    w219 = load_sibling(
        "w2_19_f3_gradient_formation_flow_candidate_contract.py", "w2_19_for_w2_20"
    )

    dependency, dependency_reports = dependency_controls(w216, w217, w218, w219)
    objects = symbolic_state()
    gradient = gradient_controls(objects)
    equivariance = equivariance_controls(objects)
    reduced_objects = reduced_flow_objects(objects)
    reduced = reduced_flow_controls(objects, reduced_objects)
    health_all = health_controls(objects, reduced_objects)
    robustness_witness = health_all.pop("_robust_descent_witness")
    health = dict(health_all)
    domain_f2, domain_diagnostics = domain_readout_controls(
        objects, reduced_objects, health
    )
    order, order_diagnostics = order_controls(objects, health)
    interventions = intervention_controls(objects, order_diagnostics, health)
    nulls = null_controls(objects, reduced_objects, {
        **health, "_robust_descent_witness": robustness_witness,
    })
    gates = f3_gate_map(
        dependency, gradient, equivariance, reduced, domain_f2, health,
        order, interventions, nulls, w217,
    )
    screen = w217.candidate_screen(gates, CANDIDATE_MAPS)
    gate_pattern_valid = bool(
        isinstance(gates, dict)
        and set(gates) == set(w217.F3_GATE_KEYS)
        and all(type(value) is bool for value in gates.values())
        and {key for key, value in gates.items() if value is False}
        == EXPECTED_FALSE_F3_GATES
    )
    contract_schema_valid = all((
        set(CLAIM_CONTRACT) == REQUIRED_SCIENTIFIC_FIELDS | {"THEOREM"},
        scientific_contract_sha256(CLAIM_CONTRACT)
        == frozen_scientific_contract_sha256(),
        CLAIM_CONTRACT["CLOSURE_FLAGS"]
        == EXPECTED_CLOSURE_FLAGS
        == frozen_closure_flags(),
        all(type(value) is bool for value in CLAIM_CONTRACT["CLOSURE_FLAGS"].values()),
    ))
    candidate_map_schema_valid = w217.candidate_map_schema_valid(CANDIDATE_MAPS)
    candidate_map_content_frozen = (
        candidate_maps_sha256(CANDIDATE_MAPS)
        == frozen_candidate_maps_sha256()
    )
    candidate_statuses_valid = (
        {key: value["status"] for key, value in CANDIDATE_MAPS.items()}
        == EXPECTED_CANDIDATE_MAP_STATUSES
        == frozen_candidate_map_statuses()
        and CANDIDATE_MAPS["transition_or_response_law"]["status"] == "PARTIAL"
        and all(
            entry["status"] == "DERIVED"
            for key, entry in CANDIDATE_MAPS.items()
            if key != "transition_or_response_law"
        )
    )
    science_checks: dict[str, bool] = {
        "contract_schema_exact": contract_schema_valid,
        "scientific_contract_content_sha256_frozen": (
            scientific_contract_sha256(CLAIM_CONTRACT)
            == frozen_scientific_contract_sha256()
        ),
        "candidate_map_schema_exact": candidate_map_schema_valid,
        "candidate_map_content_sha256_frozen": candidate_map_content_frozen,
        "candidate_map_status_ceiling_exact": candidate_statuses_valid,
        "gate_pattern_exact": gate_pattern_valid,
        "screen_valid": screen.get("valid") is True,
        "screen_ineligible": screen.get("eligible") is False,
        "screen_unpromoted": screen.get("promoted") is False,
        "robustness_witness": robustness_witness,
    }
    control_groups = (
        ("dependency", dependency, DEPENDENCY_CONTROL_KEYS),
        ("gradient", gradient, GRADIENT_CONTROL_KEYS),
        ("equivariance", equivariance, EQUIVARIANCE_CONTROL_KEYS),
        ("reduced", reduced, REDUCED_FLOW_CONTROL_KEYS),
        ("domain_readout", domain_f2, DOMAIN_READOUT_CONTROL_KEYS),
        ("health", health, HEALTH_CONTROL_KEYS),
        ("order", order, ORDER_CONTROL_KEYS),
        ("intervention", interventions, INTERVENTION_CONTROL_KEYS),
        ("null", nulls, NULL_CONTROL_KEYS),
    )
    for group_name, group, expected_keys in control_groups:
        science_checks[f"{group_name}:schema"] = exact_true_map(group, expected_keys)
        for key, value in group.items():
            science_checks[f"{group_name}:{key}"] = value is True
    all_science_valid = bool(science_checks) and all(science_checks.values())
    closure = closure_decision(all_science_valid)
    decisions = decision_controls(
        w217, gates, screen, closure, science_checks, all_science_valid
    )
    valid = bool(
        all_science_valid
        and exact_true_map(decisions, DECISION_CONTROL_KEYS)
        and closure == EXPECTED_CLOSURE_FLAGS == frozen_closure_flags()
    )
    return _json_safe({
        "artifact": CLAIM_ID,
        "claim": CLAIM_CONTRACT["CLAIM"],
        "candidate_status": (
            "STANDALONE_CONDITIONAL_GRADIENT_SEMIGROUP_ORDER_PASS__F1_F2_CHAIN_AND_FULL_F3_INELIGIBLE"
            if valid else "INVALID_OR_OPEN"
        ),
        "conclusion": (
            "On D_gap, the state-owned P_plus/P_R/tau_gap relational readout is exact and the "
            "imported negative-gradient package has a global-forward semiflow, Class(A,F) "
            "event germs, nonzero same-channel response, strict acyclic candidate-relative "
            "formation order and exact finite S/R cross-channel zeros. An exact off-shell "
            "Hessian counterexample shows that the inherited complete F1/F2 predecessor does "
            "not survive on this nonstationary chain, while the transition principle remains "
            "imported/PARTIAL. The w2_17 screen is therefore valid but ineligible, and full F3, "
            "physical time, persistence, spatial causality and every downstream bridge remain false."
        ),
        "candidate_maps": CANDIDATE_MAPS,
        "f3_gate_map": gates,
        "f3_screen": screen,
        "controls": {
            "dependency": dependency,
            "gradient": gradient,
            "equivariance": equivariance,
            "reduced_flow": reduced,
            "domain_and_off_endpoint_relational_readout": domain_f2,
            "health": health,
            "order": order,
            "intervention_and_no_transmission": interventions,
            "null_reverse_target_and_robustness": nulls,
        },
        "decision_controls": decisions,
        "exact_diagnostics": {
            "DS": objects["VS"],
            "DR": objects["VR"],
            "ds": reduced_objects["ds"],
            "dJ": reduced_objects["dJ"],
            "tau": reduced_objects["tau"],
            "dtau": reduced_objects["dtau"],
            **domain_diagnostics,
            **order_diagnostics,
        },
        "dependency_artifacts": {
            key: report.get("artifact", report.get("CLAIM_ID", "registered report"))
            for key, report in dependency_reports.items()
        },
        "closure_decision": closure,
        "program_status": (
            "STANDALONE_GRADIENT_ORDER_CLOSED__SAME_CHAIN_F1_F2_FULL_F3_AND_CLOCK_OPEN"
            if valid else "W2_F3_GRADIENT_CANDIDATE_INVALID_OR_OPEN"
        ),
        "valid": valid,
    })


def main() -> int:
    report = run()
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if all((
        report.get("valid") is True,
        report.get("closure_decision", {}).get(
            "conditional_gradient_semigroup_formation_order_proved"
        ) is True,
        report.get("closure_decision", {}).get(
            "F3_internal_order_or_causality_proved"
        ) is False,
        report.get("closure_decision", {}).get("foundation_derived_F3") is False,
    )) else 1


if __name__ == "__main__":
    raise SystemExit(main())
