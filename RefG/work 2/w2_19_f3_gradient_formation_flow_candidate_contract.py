"""Frozen, outcome-neutral contract for W2-F3 Candidate A.

Candidate A imports the scalar law ``U`` already frozen and evaluated in
``w2_16`` and adds one new oriented-process ansatz in a fixed autonomous gauge:

    dA/dsigma = -grad_F U(A),     sigma >= 0.

``grad_F`` is the Frobenius gradient on ``sl(3,R)``.  Positive changes of the
auxiliary parameter are gauge.  A global alternative parameter must satisfy
``sigma(lambda)=integral nu dlambda``, with continuous ``nu>0`` and unbounded
cumulative range.  Neither parameter nor its normalization is physical time
or an external clock.  The full-A Frobenius mobility (including
its fixed unit S/R relative mobility), the descent sign, and the assertion that
positive gradient-flow reachability is a physical internal process form a new
candidate process package.  They are imported here, not derived from the
Canon, observations, or the static w2_16 theorem.

This file freezes the candidate and authorizes a separate evaluator.  It does
not evaluate the flow, derive an intervention response, or close W2_F3.  In
particular, the accepted w2_16 product-minimum branch is stationary under this
flow, while nonstationary formation states have not yet inherited the w2_16 F2
proof.  Those facts are explicit eligibility risks, not hidden conclusions.

Audit correction 002 leaves the Candidate-A dynamics and interior D_gap
domain unchanged, but corrects two semantic ceilings discovered by the
separate evaluator: tau_gap=0 is not generally C=0 off the uniaxial endpoint,
and the off-endpoint readout does not automatically inherit the complete
stationary F1/F2 chain.
"""

from __future__ import annotations

import importlib.util
import hashlib
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import sympy as sp


F3_GATE_KEYS = frozenset({
    "same_chain_F1_F2_predecessors_valid",
    "state_owned_events_or_changes_derived",
    "target_free_transition_or_response_law_derived",
    "candidate_dynamics_health_and_state_space_closure_proved",
    "allowed_interventions_defined",
    "directed_intervention_response_proved",
    "correlation_and_static_ranking_excluded",
    "complete_equivalence_invariance_proved",
    "arrow_selected_by_law_not_labels_or_schedule",
    "nontrivial_direct_influence_on_predeclared_open_domain",
    "strict_relation_irreflexive_asymmetric_and_acyclic",
    "effective_order_transitive_and_reflexive_closure_antisymmetric",
    "forbidden_signal_nontransmission_proved",
    "computational_schedule_neutrality_proved",
    "null_reverse_and_target_leak_controls_pass",
    "perturbation_and_initial_condition_stability_proved",
    "independent_second_derivation_passes",
    "physical_time_metric_and_downstream_gates_remain_open",
})

REQUIRED_CANDIDATE_MAPS = (
    "state_space",
    "event_or_change_map",
    "complete_equivalence_action",
    "transition_or_response_law",
    "signal_support_or_update_composition",
    "allowed_interventions",
    "intervention_to_response_map",
    "direct_influence_relation",
    "transitive_effective_order",
    "forbidden_pairs",
    "no_transmission_test",
    "open_domain",
    "null_branches",
    "perturbation_class",
    "independent_crosscheck",
)

FORBIDDEN_PRELOADS = (
    "physical position, physical time, external clock, or 3+1 split",
    "lattice, locality graph, causal DAG, time layers, or event numbering",
    "Lorentzian metric, light cone, GR, Einstein equations, or PN/PPN target",
    "preferred basis, axis, orientation, labels, or state-external seed",
    "history, lag, memory, retarded kernel, or update arrow not derived from the law",
    "correlation, commutator sign, eigenvalue rank, or Krylov depth renamed causality",
    "algorithmic iteration or execution schedule renamed physical process order",
    "post-selection of the branch or convention that gives the desired arrow",
)

MANDATORY_CONTROLS = (
    "known directed acyclic influence positive control",
    "frozen or nonresponsive null",
    "correlated but noninterventional null",
    "two-way reachability between the same event occurrences rejection",
    "directed-cycle rejection",
    "prewired target-DAG rejection",
    "basis, label, reflection, and reversal mutations",
    "execution-schedule permutation",
    "F2 nulls S=0, R=0, tau=0, tau=1, tuned branch, and singular normalization",
    "small-perturbation and allowed-initial-condition stability",
    "independent derivation not trained on the first result",
)

CANDIDATE_MAP_ENTRY_KEYS = frozenset({"status", "source", "definition"})
CANDIDATE_MAP_STATUSES = frozenset({"DERIVED", "PARTIAL", "ABSENT", "NOT_APPLICABLE"})
GRADIENT_ROUTE_CONDITIONAL_FORMATION_ORDER_EVALUATION_AUTHORIZED = True
GRADIENT_ROUTE_FULL_F3_PROMOTION_AUTHORIZED = False
MAXIMUM_AUTHORIZED_EVALUATOR_OUTCOME = (
    "CONDITIONAL_CANDIDATE_RELATIVE_FORMATION_ORDER_THEOREM"
)
CANDIDATE_A_EVALUATION_AUTHORIZED = (
    GRADIENT_ROUTE_CONDITIONAL_FORMATION_ORDER_EVALUATION_AUTHORIZED
)
CANDIDATE_A_F3_PROMOTION_AUTHORIZED = GRADIENT_ROUTE_FULL_F3_PROMOTION_AUTHORIZED


CANDIDATE_A_MAPS: dict[str, dict[str, str]] = {
    "state_space": {
        "status": "DERIVED",
        "source": "w2_16 conditional structural endpoint",
        "definition": (
            "A in sl(3,R), S=(A+A^T)/2 and R=(A-A^T)/2, modulo one common O(3) "
            "conjugation; no extra physical state variable is added"
        ),
    },
    "event_or_change_map": {
        "status": "PARTIAL",
        "source": "new Candidate-A oriented-process ansatz; not Canon-derived",
        "definition": (
            "E(A)=Class(A,F(A)) modulo common O(3) and positive tangent rescaling, where "
            "F=-grad_F U and F(A)!=0; this state-owned oriented tangent germ is a local "
            "candidate change, not a sampled parameter value, next-event rule or record"
        ),
    },
    "complete_equivalence_action": {
        "status": "DERIVED",
        "source": "w2_16 complete matrix-star-algebra equivalence",
        "definition": "A -> O A O^T for every O in O(3), including reflections",
    },
    "transition_or_response_law": {
        "status": "PARTIAL",
        "source": "new imported Candidate-A law; definition frozen but unevaluated",
        "definition": (
            "dA/dsigma=-grad_F U(A), sigma>=0; a global gauge-equivalent lambda obeys "
            "sigma(lambda)=integral_0^lambda nu(l)dl with continuous nu>0 and "
            "sigma(lambda)->infinity; neither parameter is physical time"
        ),
    },
    "signal_support_or_update_composition": {
        "status": "PARTIAL",
        "source": "candidate positive-parameter negative-gradient semiflow",
        "definition": (
            "after gauge fixing nu=1, Phi_{r+s}=Phi_r composed with Phi_s for r,s>=0; "
            "existence, domain closure and physical signal meaning remain evaluator duties"
        ),
    },
    "allowed_interventions": {
        "status": "PARTIAL",
        "source": "candidate tangent-state intervention class",
        "definition": (
            "pure-S deltaA=deltaS in Sym_0(3), pure-R deltaA=deltaR in so(3), and their "
            "finite sums, small enough to stay in the declared domain; quotient infinitesimal "
            "common-O(3) gauge tangents [omega,A], and add no coefficient or target fitting"
        ),
    },
    "intervention_to_response_map": {
        "status": "PARTIAL",
        "source": "linearized candidate semiflow",
        "definition": (
            "for every sigma>0 with both trajectories in-domain, deltaA at E(A) maps to "
            "D Phi_sigma(A)[deltaA]; response support is the O(3)-covariant S/R projection, "
            "whose zero/nonzero Frobenius norm is invariant; no next-event sampling is used"
        ),
    },
    "direct_influence_relation": {
        "status": "PARTIAL",
        "source": "candidate intervention semantics, not U-ranking",
        "definition": (
            "E(A) directly influences the positive-reachable germ E(Phi_sigma(A)) only if "
            "an allowed intervention produces a nonzero invariant projected-response norm "
            "for some declared sigma>0; U ranking alone is not the definition"
        ),
    },
    "transitive_effective_order": {
        "status": "PARTIAL",
        "source": "transitive closure of evaluated direct influence",
        "definition": (
            "positive-semiflow reachability may support composition, but U decrease alone is "
            "only an acyclicity certificate and is not the causal definition"
        ),
    },
    "forbidden_pairs": {
        "status": "PARTIAL",
        "source": "predeclared Candidate-A no-signal targets",
        "definition": (
            "the substantive channel pairs are pure-S intervention to future R projection "
            "and pure-R intervention to future S projection; pure common-O(3) tangents are "
            "gauge nulls. Reverse reachability is tested separately as an order axiom, not "
            "counted as an independent no-transmission theorem; effects on joint C are nonzero"
        ),
    },
    "no_transmission_test": {
        "status": "PARTIAL",
        "source": "future exact variational-semigroup calculation",
        "definition": (
            "prove the finite-semiflow Frechet blocks D_S Phi^R_sigma and D_R Phi^S_sigma "
            "vanish identically for every supported sigma>0; separately prove positive "
            "reachability has no reverse cycle. A zero static Hessian block is insufficient"
        ),
    },
    "open_domain": {
        "status": "PARTIAL",
        "source": "predeclared formation-basin candidate domain",
        "definition": (
            "D_gap: alpha,b,c,eta,d>0 and b^2!=3 alpha c; S has one simple largest "
            "eigenvalue with projector P_plus(S), J>0, P_R=I+2R^2/J, "
            "tau_gap=1-Tr(P_plus P_R) lies in (0,1), C=[S,R]!=0, grad_F U!=0, and the "
            "forward orbit belongs to the basin of the generic w2_16 minimum stratum. The "
            "evaluator must prove this dynamically defined spectral-gap basin nonempty, open "
            "and invariant, and must separately adjudicate whether the complete inherited "
            "F1/F2 chain survives on these off-endpoint maps"
        ),
    },
    "null_branches": {
        "status": "PARTIAL",
        "source": "inherited endpoint nulls plus separately classified flow boundaries",
        "definition": (
            "A=0, S=0, R=0 and C=0 nulls; tau_gap=0 and tau_gap=1 excluded readout "
            "boundaries (tau_gap=0 is not generally C=0 away from the uniaxial endpoint); "
            "tuned and singular branches, spectral-gap/basin boundaries, the stationary "
            "accepted F2 endpoint, and the excluded ascent sign"
        ),
    },
    "perturbation_class": {
        "status": "PARTIAL",
        "source": "candidate initial-state perturbations only",
        "definition": (
            "small traceless perturbations preserving the same open basin and simple-support "
            "branch; coefficient, physical-clock and target perturbations are excluded"
        ),
    },
    "independent_crosscheck": {
        "status": "ABSENT",
        "source": "reserved for the separate evaluator",
        "definition": (
            "requires a second derivation of the flow, invariant basin, intervention response "
            "and forbidden-pair zeros that is not trained on the first calculation"
        ),
    },
}

EXPECTED_CANDIDATE_A_STATUSES = {
    "state_space": "DERIVED",
    "event_or_change_map": "PARTIAL",
    "complete_equivalence_action": "DERIVED",
    "transition_or_response_law": "PARTIAL",
    "signal_support_or_update_composition": "PARTIAL",
    "allowed_interventions": "PARTIAL",
    "intervention_to_response_map": "PARTIAL",
    "direct_influence_relation": "PARTIAL",
    "transitive_effective_order": "PARTIAL",
    "forbidden_pairs": "PARTIAL",
    "no_transmission_test": "PARTIAL",
    "open_domain": "PARTIAL",
    "null_branches": "PARTIAL",
    "perturbation_class": "PARTIAL",
    "independent_crosscheck": "ABSENT",
}


SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F3_GRADIENT_FORMATION_FLOW_CANDIDATE_CONTRACT_001",
    "CLAIM": (
        "Freeze, without evaluating any F3 outcome, Candidate A: the negative Frobenius-gradient "
        "semigroup of the inherited w2_16 scalar law U, with an imported Frobenius-mobility "
        "descent process package, positive-reparameterization gauge, and no physical time."
    ),
    "TYPE": "OUTCOME_NEUTRAL_DYNAMIC_CANDIDATE_CONTRACT",
    "MODEL_VERSION": (
        "W2-C0 through w2_18 plus Candidate-A dynamics version 001 and contract audit "
        "correction 002. Changing U, the descent sign, the "
        "process interpretation, the intervention class, the domain, or the gauge policy creates "
        "a new candidate version and reopens every dependent gate."
    ),
    "ASSUMPTIONS": (
        "The conditional w2_16 F1/F2 result and the w2_17 fail-closed F3 interface are valid. "
        "The law U, trace pairing and common O(3) are inherited. Promoting the full-A Frobenius "
        "pairing to an identity mobility, fixing the relative S/R mobility to one, choosing "
        "-grad_F U, and reading its positive reachability as an oriented internal process form "
        "a new imported process ansatz. The simple-largest-eigenspace projector and tau_gap "
        "below are a new off-endpoint relational-readout candidate whose compatibility with "
        "the complete inherited F1/F2 chain must be tested. None of these "
        "choices is a Theory_Canon-derived fact or observational evidence."
    ),
    "DOMAIN": (
        "The polynomial vector field is defined on sl(3,R) for alpha,b,c,eta,d>0. Candidate F3 "
        "evaluation is restricted to the precisely defined D_gap spectral-gap basin recorded "
        "in CANDIDATE_A_MAPS. Its nonemptiness, openness, invariance and candidate-specific "
        "relational "
        "readout and same-chain predecessor status are evaluator duties; inherited endpoint "
        "nulls, stationary points, undefined "
        "projectors, basin boundaries and the ascent sign are separate nonpromoting branches."
    ),
    "CONVENTIONS": (
        "S=(A+A^T)/2, R=(A-A^T)/2, I2=Tr(S^2), I3=Tr(S^3), J=-Tr(R^2), "
        "<X,Y>_F=Tr(X^T Y), and U=-alpha I2/2-b I3/3+c I2^2/4-eta J/2+d J^2/4. "
        "The fixed-gauge law is dA/dsigma=-grad_F U for sigma>=0. A global alternative "
        "parameter lambda is gauge only when sigma(lambda)=integral_0^lambda nu(l)dl has "
        "continuous nu>0 and unbounded cumulative range. Neither sigma nor lambda is physical "
        "time or an external clock."
    ),
    "FREEDOM_LEDGER": {
        "inherited_state_and_split": {
            "source": "w2_16",
            "allowed_range": "A in sl(3,R), with fixed transpose projections S,R",
            "scale": "one internal state",
            "complexity": 8,
        },
        "inherited_law_coefficients": {
            "source": "w2_16; no value changed here",
            "allowed_range": "alpha,b,c,eta,d>0",
            "scale": "five universal theory coefficients",
            "complexity": 5,
        },
        "descent_sign_and_process_principle": {
            "source": "new Candidate-A primitive; not Canon-derived",
            "allowed_range": "negative Frobenius gradient and positive reachability only",
            "scale": "one universal discrete theory choice",
            "complexity": "1 discrete choice; 0 new continuous coefficients",
        },
        "kinetic_metric_and_relative_mobility": {
            "source": (
                "new Candidate-A structural choice built from the inherited trace pairing; "
                "common O(3) alone permits independent positive S/R weights"
            ),
            "allowed_range": (
                "identity mobility for the full-A Frobenius metric, fixing the S/R relative "
                "mobility to one"
            ),
            "scale": "one universal process-geometry choice",
            "complexity": (
                "1 fixed dimensionless continuous input rho=mu_R/mu_S=1 plus the selected "
                "full-A mobility class; 0 fitted parameters"
            ),
        },
        "off_endpoint_relational_readout_candidate": {
            "source": "new Candidate-A continuous extension of the w2_16 positive support line",
            "allowed_range": (
                "P_plus is the simple-largest-eigenvalue projector, P_R=I+2R^2/J, and "
                "tau_gap=1-Tr(P_plus P_R); undefined outside the spectral-gap/J>0 domain"
            ),
            "scale": "one fixed state-readout architecture",
            "complexity": "1 fixed map choice; 0 fitted parameters",
        },
        "positive_reparameterization": {
            "source": "candidate gauge redundancy",
            "allowed_range": (
                "continuous nu(lambda)>0 with sigma(lambda)=integral nu, sigma(0)=0, "
                "and sigma(lambda)->infinity for global semigroup equivalence"
            ),
            "scale": "unphysical orbit parameterization",
            "complexity": 0,
        },
        "initial_state": {
            "source": "allowed formation-domain state, not a fitted coefficient",
            "allowed_range": "predeclared open basin modulo common O(3)",
            "scale": "state/initial condition",
            "complexity": "state dimension only; not theory-parameter complexity",
        },
        "intervention_class": {
            "source": "fixed candidate tangent class",
            "allowed_range": "traceless in-domain deltaA modulo common-O(3) gauge",
            "scale": "diagnostic map",
            "complexity": "1 fixed diagnostic class; 0 fitted parameters",
        },
        "new_continuous_or_fitted_coefficients": {
            "source": "none left free or fitted; fixed rho=1 is charged separately above",
            "allowed_range": 0,
            "scale": "theory and data",
            "complexity": 0,
        },
        "physical_time_clock_rate_or_schedule": {
            "source": "forbidden",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
        "position_lattice_graph_metric_or_GR_target": {
            "source": "forbidden",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py: conditional "
        "static F1/F2 state and U",
        "RefG/work 2/w2_17_f3_internal_order_causality_contract.py: exact F3 schema",
        "RefG/work 2/w2_18_f3_static_endpoint_adjudication_gate.py: static-only F3 route rejected "
        "and a genuinely dynamic candidate required",
    ],
    "METHOD": (
        "Freeze the exact gradient direction, global gauge conditions, spectral-gap state/readout "
        "domain, oriented-tangent event map, event/intervention interface, "
        "forbidden pairs, nulls, freedoms and all w2_17 gates before evaluation. A separate "
        "artifact may derive the candidate-relative semigroup, basin and formation order by exact "
        "algebra and an independent route. Because the generator is imported, the inherited F2 "
        "minimum is stationary, and no persistent internal phase or record has been supplied, its "
        "strongest authorized result is a conditional candidate-relative formation-order theorem."
    ),
    "PASS_CONDITION": (
        "This file passes only as an outcome-neutral candidate definition when its complete CODES "
        "schema, dependency identities, exact candidate maps, freedom ledger, registries, false "
        "outcome ledger and fail-closed mutations all pass. A separate evaluator may test a "
        "conditional formation-order statement, but this candidate cannot authorize full w2_17 "
        "F3 promotion even if a synthetic screen has all 15 maps DERIVED and all 18 gates True."
    ),
    "FAIL_CONDITION": (
        "Any hidden mobility, rate, coefficient or off-endpoint readout, physical-time "
        "interpretation, nonpositive reparameterization, sign post-selection, target preload, "
        "missing map/control/null, premature "
        "DERIVED status, or true scientific outcome invalidates this contract. The standalone "
        "dynamic evaluation fails if the formation domain is not state-space closed, its declared "
        "relational readout is ill-defined, it has no directed intervention response, or it violates "
        "a forbidden-pair zero. Failure of the complete same-chain F1/F2 predecessor blocks F3 "
        "eligibility but does not erase an otherwise valid standalone dynamics theorem."
    ),
    "FALSIFIER": (
        "Candidate A is falsified as an F3 realization if D_gap lacks the complete same-chain "
        "F1/F2 predecessor or if the imported transition principle remains not derived from the "
        "foundation. "
        "Its standalone dynamic theorem is falsified if D_gap is not a nonempty invariant open "
        "domain carrying the declared relational readout and a nontrivial directed intervention "
        "response with exact forbidden-signal nontransmission. The contract freeze is "
        "falsified if it calls the process Canon-derived, hides the mobility or sign choice, introduces "
        "physical time, invents a persistent phase or record, or allows any unevaluated map, "
        "closure flag, or candidate-relative order result to promote the full w2_17 F3 claim."
    ),
    "RESIDUAL": (
        "N/A for F3 outcomes. Definition-level identities require zero residual for the frozen U, "
        "its Frobenius gradient, traceless tangent and dU/dsigma=-||grad_F U||_F^2."
    ),
    "ERROR_BOUND": (
        "Zero for definition-level symbolic identities. No numerical integration, approximation, "
        "data likelihood or observational error is used; basin and stability bounds remain open."
    ),
    "VALIDITY_HEALTH": (
        "Severe open issues are explicit. U is separable, so S and R have no cross-channel "
        "dynamical response. Every accepted w2_16 product minimum has grad_F U=0, hence the "
        "proved generic F2 endpoint is event-frozen. Nonstationary formation states use the new "
        "P_plus/P_R/tau_gap extension and lie outside the already proved minimum-set F2 theorem "
        "until that extension is revalidated. Descent orientation is an "
        "imported dissipative process postulate, not a Canon derivation. Therefore Lyapunov descent "
        "or semigroup reachability alone cannot close causality or no-transmission. No persistent "
        "internal phase or record is present. Common O(3) does not uniquely force equal S/R "
        "mobilities, so the full-A Frobenius mobility is an explicit architectural choice. A "
        "candidate-relative formation order therefore cannot be promoted to full F3 internal causality."
    ),
    "BRANCHES": {
        "nonstationary_positive_descent_basin": "FROZEN_FOR_EVALUATION_NOT_PROVED",
        "accepted_w2_16_F2_minimum": "STATIONARY_EVENT_NULL",
        "S_or_R_or_C_zero": "INHERITED_RELATIONAL_NULL",
        "tau_gap_zero": "EXCLUDED_READOUT_BOUNDARY__NOT_GENERAL_C_ZERO",
        "tau_gap_one": "EXCLUDED_ORBIT_BOUNDARY_CONTROL_NOT_RELATIONAL_ZERO",
        "tuned_or_singular_branch": "NO_PROMOTION",
        "ascent_or_parameter_reversal": "EXCLUDED_NEW_VERSION_REQUIRED",
        "physical_time_clock_metric_or_graph": "FORBIDDEN_TARGET_LEAK",
        "conditional_candidate_relative_formation_order": "EVALUATION_AUTHORIZED_NOT_PROVED",
        "full_w2_17_F3_promotion": "UNAUTHORIZED_FOR_THIS_CANDIDATE",
        "F3_result": "UNEVALUATED_FALSE",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "pre-spatial internal candidate contract"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "no data or physical-time dynamics"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, target, calibration or fit"},
    "IDENTIFIABILITY": (
        "The five law coefficients are inherited. Candidate A adds one explicit discrete "
        "descent/process choice, the fixed numerical mobility ratio rho=1, the full-A mobility "
        "class and one off-endpoint spectral readout map, but no fitted coefficient. Positive parameter speed is gauge and "
        "has no identifiable physical rate. The evaluator must distinguish intervention response "
        "from U ranking, static C dependence, common-O(3) representatives and the excluded reversed "
        "orientation."
    ),
    "BENCHMARK": (
        "The positive logical control is a three-event directed intervention chain. Candidate "
        "formation witnesses must start off the stationary minimum with S,R,C nonzero and "
        "0<tau_gap<1. The accepted w2_16 minimum, frozen/nonresponsive states, correlation-only pairs, "
        "two-way reachability, cycles, prewired DAGs, inherited endpoint F2 nulls, separately "
        "classified readout boundaries and the reversed sign are mandatory "
        "negative controls. None is candidate evidence in this contract."
    ),
    "CLOSURE_FLAGS": {
        "F1_F2_conditional_predecessors_registered": True,
        "w2_17_F3_contract_registered": True,
        "Candidate_A_contract_defined": True,
        "Candidate_A_evaluation_authorized": True,
        "Candidate_A_evaluated": False,
        "Candidate_A_flow_or_basin_proved": False,
        "Candidate_A_intervention_response_proved": False,
        "Candidate_A_forbidden_nontransmission_proved": False,
        "atemporal_internal_order_proved": False,
        "F3_internal_order_or_causality_proved": False,
        "physical_time_or_clock_readout_proved": False,
        "persistence_or_memory_proved": False,
        "persistent_internal_phase_or_record_proved": False,
        "conditional_candidate_relative_formation_order_proved": False,
        "F4_independent_additive_modes_proved": False,
        "foundation_to_effective_closed": False,
        "W2_M1_dimension_or_continuum_proved": False,
        "W2_M2_Lorentzian_metric_proved": False,
        "effective_action_or_matter_coupling_proved": False,
        "Einstein_GR_PN_or_PPN_bridge_proved": False,
        "observational_validation_proved": False,
    },
    "CROSSCHECK": (
        "Definition coherence is checked by an independent coordinate directional derivative of U, "
        "the closed-form Frobenius gradient, exact endpoint stationarity, sibling-contract registry "
        "comparison, and adversarial schema/map/gate mutations. Scientific flow and causality "
        "crosschecks remain reserved for the evaluator."
    ),
    "PROVENANCE": {
        "date": "2026-07-22",
        "data": "none",
        "code_version": (
            "w2_19 Candidate-A contract audit correction 002; dynamics and interior domain "
            "unchanged, predecessor and tau-gap-zero ceilings corrected"
        ),
        "hash": (
            "complete contract content is internally SHA-256 frozen; the source-control commit "
            "remains the artifact provenance record"
        ),
        "output": "JSON contract-validation report",
    },
    "FILES": [
        "CODES.md",
        "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py",
        "RefG/work 2/w2_17_f3_internal_order_causality_contract.py",
        "RefG/work 2/w2_18_f3_static_endpoint_adjudication_gate.py",
        "RefG/work 2/w2_19_f3_gradient_formation_flow_candidate_contract.py",
    ],
    "CANDIDATE_DEFINITION": {
        "law": "U=-alpha I2/2-b I3/3+c I2^2/4-eta J/2+d J^2/4",
        "gradient": (
            "grad_F U=(-alpha+c I2)S-b(S^2-I2 I/3)+(d J-eta)R"
        ),
        "mobility": (
            "identity mobility induced by the full-A Frobenius pairing; relative S/R mobility "
            "rho=mu_R/mu_S fixed numerically to one as an imported structural choice"
        ),
        "off_endpoint_support_map": (
            "on the simple-largest-eigenvalue/J>0 domain, P_plus(S) is the spectral "
            "projector, P_R=I+2R^2/J, and tau_gap=1-Tr(P_plus P_R); this equals the old "
            "tau on the w2_16 uniaxial endpoint; away from that endpoint it is only a "
            "relational-readout candidate and does not by itself revalidate the full F1/F2 chain"
        ),
        "oriented_flow": "dA/dsigma=-grad_F U, sigma>=0",
        "gauge": (
            "global orientation-preserving reparameterization with continuous nu>0, "
            "sigma(lambda)=integral_0^lambda nu(l)dl, and unbounded cumulative range"
        ),
        "semantic_limit": "oriented pre-clock process ansatz; no physical duration or clock",
        "origin_status": "NEW_IMPORTED_PROCESS_PACKAGE_NOT_CANON_DERIVED",
        "maximum_authorized_evaluator_outcome": MAXIMUM_AUTHORIZED_EVALUATOR_OUTCOME,
    },
    "DOMAIN_AND_NULLS": {
        "mathematical_domain": "sl(3,R), alpha,b,c,eta,d>0",
        "evaluation_domain": CANDIDATE_A_MAPS["open_domain"]["definition"],
        "accepted_F2_endpoint": (
            "the w2_16 global-minimum product has grad_F U=0 and is a required event null"
        ),
        "formation_gap": (
            "nonstationary D_gap states must independently test P_plus, P_R, tau_gap and C, "
            "and separately test the complete inherited F1/F2 predecessor chain"
        ),
        "inherited_nulls": CANDIDATE_A_MAPS["null_branches"]["definition"],
        "undefined_tau": (
            "tau_gap is not assigned when the largest eigenspace is not simple or J=0"
        ),
        "reverse_branch": "ascent or sigma reversal is not gauge and requires a new candidate version",
    },
    "F3_EVALUATION_DUTIES": {key: "UNEVALUATED_REQUIRED" for key in sorted(F3_GATE_KEYS)},
    "REQUIRED_CANDIDATE_MAPS": REQUIRED_CANDIDATE_MAPS,
    "FORBIDDEN_PRELOADS": FORBIDDEN_PRELOADS,
    "MANDATORY_CONTROLS": MANDATORY_CONTROLS,
    "AUTHORIZATION": {
        "candidate_identity_frozen": True,
        "separate_evaluator_authorized": True,
        "conditional_candidate_relative_formation_order_evaluation_authorized": True,
        "full_w2_17_F3_promotion_authorized": False,
        "in_place_patch_after_outcomes_authorized": False,
        "scientific_promotion_authorized": False,
        "Canon_or_article_export_authorized": False,
    },
    "SCOPE_CEILING": {
        "Candidate_A_contract_valid_if_definition_controls_pass": True,
        "Candidate_A_identity_frozen": True,
        "Candidate_A_separate_evaluation_authorized": True,
        "Candidate_A_conditional_formation_order_theorem_authorized": True,
        "Candidate_A_full_w2_17_F3_promotion_authorized": False,
        "Candidate_A_mathematical_or_physical_origin_proved": False,
        "Candidate_A_dynamic_health_proved": False,
        "Candidate_A_F2_relation_preserved_on_open_flow_domain": False,
        "Candidate_A_forbidden_pair_nontransmission_proved": False,
        "Candidate_A_persistent_internal_phase_or_record_proved": False,
        "Candidate_A_conditional_formation_order_proved": False,
        "Candidate_A_full_w2_17_eligibility_proved": False,
        "F3_internal_order_or_causality_proved": False,
        "physical_time_metric_GR_or_observation_proved": False,
    },
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def scientific_contract_sha256(contract: dict[str, Any]) -> str:
    canonical = json.dumps(
        contract, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest().upper()


def frozen_scientific_contract_sha256() -> str:
    """Independent literal freeze of the complete corrected contract."""
    return "7D2CE65CD6FCA7B3007FE6B9EA60CDC4F0AA93595DA828745DC7FE2FB9842F98"


def frozen_closure_flags() -> dict[str, bool]:
    """Independent outcome ledger, deliberately not copied from the contract."""
    return {
        "F1_F2_conditional_predecessors_registered": True,
        "w2_17_F3_contract_registered": True,
        "Candidate_A_contract_defined": True,
        "Candidate_A_evaluation_authorized": True,
        "Candidate_A_evaluated": False,
        "Candidate_A_flow_or_basin_proved": False,
        "Candidate_A_intervention_response_proved": False,
        "Candidate_A_forbidden_nontransmission_proved": False,
        "atemporal_internal_order_proved": False,
        "F3_internal_order_or_causality_proved": False,
        "physical_time_or_clock_readout_proved": False,
        "persistence_or_memory_proved": False,
        "persistent_internal_phase_or_record_proved": False,
        "conditional_candidate_relative_formation_order_proved": False,
        "F4_independent_additive_modes_proved": False,
        "foundation_to_effective_closed": False,
        "W2_M1_dimension_or_continuum_proved": False,
        "W2_M2_Lorentzian_metric_proved": False,
        "effective_action_or_matter_coupling_proved": False,
        "Einstein_GR_PN_or_PPN_bridge_proved": False,
        "observational_validation_proved": False,
    }


def frozen_authorization() -> dict[str, bool]:
    return {
        "candidate_identity_frozen": True,
        "separate_evaluator_authorized": True,
        "conditional_candidate_relative_formation_order_evaluation_authorized": True,
        "full_w2_17_F3_promotion_authorized": False,
        "in_place_patch_after_outcomes_authorized": False,
        "scientific_promotion_authorized": False,
        "Canon_or_article_export_authorized": False,
    }


def frozen_scope_ceiling() -> dict[str, bool]:
    return {
        "Candidate_A_contract_valid_if_definition_controls_pass": True,
        "Candidate_A_identity_frozen": True,
        "Candidate_A_separate_evaluation_authorized": True,
        "Candidate_A_conditional_formation_order_theorem_authorized": True,
        "Candidate_A_full_w2_17_F3_promotion_authorized": False,
        "Candidate_A_mathematical_or_physical_origin_proved": False,
        "Candidate_A_dynamic_health_proved": False,
        "Candidate_A_F2_relation_preserved_on_open_flow_domain": False,
        "Candidate_A_forbidden_pair_nontransmission_proved": False,
        "Candidate_A_persistent_internal_phase_or_record_proved": False,
        "Candidate_A_conditional_formation_order_proved": False,
        "Candidate_A_full_w2_17_eligibility_proved": False,
        "F3_internal_order_or_causality_proved": False,
        "physical_time_metric_GR_or_observation_proved": False,
    }


def frozen_freedom_ledger() -> dict[str, dict[str, Any]]:
    return {
        "inherited_state_and_split": {
            "source": "w2_16",
            "allowed_range": "A in sl(3,R), with fixed transpose projections S,R",
            "scale": "one internal state",
            "complexity": 8,
        },
        "inherited_law_coefficients": {
            "source": "w2_16; no value changed here",
            "allowed_range": "alpha,b,c,eta,d>0",
            "scale": "five universal theory coefficients",
            "complexity": 5,
        },
        "descent_sign_and_process_principle": {
            "source": "new Candidate-A primitive; not Canon-derived",
            "allowed_range": "negative Frobenius gradient and positive reachability only",
            "scale": "one universal discrete theory choice",
            "complexity": "1 discrete choice; 0 new continuous coefficients",
        },
        "kinetic_metric_and_relative_mobility": {
            "source": (
                "new Candidate-A structural choice built from the inherited trace pairing; "
                "common O(3) alone permits independent positive S/R weights"
            ),
            "allowed_range": (
                "identity mobility for the full-A Frobenius metric, fixing the S/R relative "
                "mobility to one"
            ),
            "scale": "one universal process-geometry choice",
            "complexity": (
                "1 fixed dimensionless continuous input rho=mu_R/mu_S=1 plus the selected "
                "full-A mobility class; 0 fitted parameters"
            ),
        },
        "off_endpoint_relational_readout_candidate": {
            "source": "new Candidate-A continuous extension of the w2_16 positive support line",
            "allowed_range": (
                "P_plus is the simple-largest-eigenvalue projector, P_R=I+2R^2/J, and "
                "tau_gap=1-Tr(P_plus P_R); undefined outside the spectral-gap/J>0 domain"
            ),
            "scale": "one fixed state-readout architecture",
            "complexity": "1 fixed map choice; 0 fitted parameters",
        },
        "positive_reparameterization": {
            "source": "candidate gauge redundancy",
            "allowed_range": (
                "continuous nu(lambda)>0 with sigma(lambda)=integral nu, sigma(0)=0, "
                "and sigma(lambda)->infinity for global semigroup equivalence"
            ),
            "scale": "unphysical orbit parameterization",
            "complexity": 0,
        },
        "initial_state": {
            "source": "allowed formation-domain state, not a fitted coefficient",
            "allowed_range": "predeclared open basin modulo common O(3)",
            "scale": "state/initial condition",
            "complexity": "state dimension only; not theory-parameter complexity",
        },
        "intervention_class": {
            "source": "fixed candidate tangent class",
            "allowed_range": "traceless in-domain deltaA modulo common-O(3) gauge",
            "scale": "diagnostic map",
            "complexity": "1 fixed diagnostic class; 0 fitted parameters",
        },
        "new_continuous_or_fitted_coefficients": {
            "source": "none left free or fitted; fixed rho=1 is charged separately above",
            "allowed_range": 0,
            "scale": "theory and data",
            "complexity": 0,
        },
        "physical_time_clock_rate_or_schedule": {
            "source": "forbidden",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
        "position_lattice_graph_metric_or_GR_target": {
            "source": "forbidden",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
    }


def frozen_candidate_definition() -> dict[str, str]:
    return {
        "law": "U=-alpha I2/2-b I3/3+c I2^2/4-eta J/2+d J^2/4",
        "gradient": "grad_F U=(-alpha+c I2)S-b(S^2-I2 I/3)+(d J-eta)R",
        "mobility": (
            "identity mobility induced by the full-A Frobenius pairing; relative S/R mobility "
            "rho=mu_R/mu_S fixed numerically to one as an imported structural choice"
        ),
        "off_endpoint_support_map": (
            "on the simple-largest-eigenvalue/J>0 domain, P_plus(S) is the spectral "
            "projector, P_R=I+2R^2/J, and tau_gap=1-Tr(P_plus P_R); this equals the old "
            "tau on the w2_16 uniaxial endpoint; away from that endpoint it is only a "
            "relational-readout candidate and does not by itself revalidate the full F1/F2 chain"
        ),
        "oriented_flow": "dA/dsigma=-grad_F U, sigma>=0",
        "gauge": (
            "global orientation-preserving reparameterization with continuous nu>0, "
            "sigma(lambda)=integral_0^lambda nu(l)dl, and unbounded cumulative range"
        ),
        "semantic_limit": "oriented pre-clock process ansatz; no physical duration or clock",
        "origin_status": "NEW_IMPORTED_PROCESS_PACKAGE_NOT_CANON_DERIVED",
        "maximum_authorized_evaluator_outcome": (
            "CONDITIONAL_CANDIDATE_RELATIVE_FORMATION_ORDER_THEOREM"
        ),
    }


def frozen_domain_and_nulls() -> dict[str, str]:
    return {
        "mathematical_domain": "sl(3,R), alpha,b,c,eta,d>0",
        "evaluation_domain": (
            "D_gap: alpha,b,c,eta,d>0 and b^2!=3 alpha c; S has one simple largest "
            "eigenvalue with projector P_plus(S), J>0, P_R=I+2R^2/J, "
            "tau_gap=1-Tr(P_plus P_R) lies in (0,1), C=[S,R]!=0, grad_F U!=0, and the "
            "forward orbit belongs to the basin of the generic w2_16 minimum stratum. The "
            "evaluator must prove this dynamically defined spectral-gap basin nonempty, open "
            "and invariant, and must separately adjudicate whether the complete inherited "
            "F1/F2 chain survives on these off-endpoint maps"
        ),
        "accepted_F2_endpoint": (
            "the w2_16 global-minimum product has grad_F U=0 and is a required event null"
        ),
        "formation_gap": (
            "nonstationary D_gap states must independently test P_plus, P_R, tau_gap and C, "
            "and separately test the complete inherited F1/F2 predecessor chain"
        ),
        "inherited_nulls": (
            "A=0, S=0, R=0 and C=0 nulls; tau_gap=0 and tau_gap=1 excluded readout "
            "boundaries (tau_gap=0 is not generally C=0 away from the uniaxial endpoint); "
            "tuned and singular branches, spectral-gap/basin boundaries, the stationary "
            "accepted F2 endpoint, and the excluded ascent sign"
        ),
        "undefined_tau": (
            "tau_gap is not assigned when the largest eigenspace is not simple or J=0"
        ),
        "reverse_branch": (
            "ascent or sigma reversal is not gauge and requires a new candidate version"
        ),
    }


EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()
EXPECTED_AUTHORIZATION = frozen_authorization()
EXPECTED_SCOPE_CEILING = frozen_scope_ceiling()
EXPECTED_FREEDOM_LEDGER = frozen_freedom_ledger()
EXPECTED_CANDIDATE_DEFINITION = frozen_candidate_definition()
EXPECTED_DOMAIN_AND_NULLS = frozen_domain_and_nulls()
EXPECTED_FREEDOM_KEYS = frozenset({
    "inherited_state_and_split",
    "inherited_law_coefficients",
    "descent_sign_and_process_principle",
    "kinetic_metric_and_relative_mobility",
    "off_endpoint_relational_readout_candidate",
    "positive_reparameterization",
    "initial_state",
    "intervention_class",
    "new_continuous_or_fitted_coefficients",
    "physical_time_clock_rate_or_schedule",
    "position_lattice_graph_metric_or_GR_target",
})
EXPECTED_F3_EVALUATION_DUTIES = {
    key: "UNEVALUATED_REQUIRED" for key in F3_GATE_KEYS
}
EXPECTED_CRITICAL_FREEDOM_ENTRIES: dict[str, dict[str, Any]] = {
    "new_continuous_or_fitted_coefficients": {
        "source": "none left free or fitted; fixed rho=1 is charged separately above",
        "allowed_range": 0,
        "scale": "theory and data",
        "complexity": 0,
    },
    "physical_time_clock_rate_or_schedule": {
        "source": "forbidden",
        "allowed_range": 0,
        "scale": "all",
        "complexity": 0,
    },
    "position_lattice_graph_metric_or_GR_target": {
        "source": "forbidden",
        "allowed_range": 0,
        "scale": "all",
        "complexity": 0,
    },
}

CODES_SCHEMA_KEYS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD", "PASS_CONDITION",
    "FAIL_CONDITION", "FALSIFIER", "RESIDUAL", "ERROR_BOUND", "VALIDITY_HEALTH",
    "BRANCHES", "OBSERVABLE_MAP", "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY",
    "BENCHMARK", "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})
REQUIRED_CONTRACT_KEYS = CODES_SCHEMA_KEYS | frozenset({
    "CANDIDATE_DEFINITION", "DOMAIN_AND_NULLS", "F3_EVALUATION_DUTIES",
    "REQUIRED_CANDIDATE_MAPS", "FORBIDDEN_PRELOADS", "MANDATORY_CONTROLS",
    "AUTHORIZATION", "SCOPE_CEILING",
})

DEFINITION_CONTROL_KEYS = frozenset({
    "full_CODES_scientific_schema_exact",
    "candidate_identity_and_origin_boundary_frozen",
    "freedom_ledger_complete_and_no_new_fitted_coefficient",
    "positive_reparameterization_is_gauge_not_physical_time",
    "candidate_maps_complete_exact_and_unevaluated",
    "all_w2_17_registries_frozen_exactly",
    "all_F3_evaluation_outcomes_false",
    "authorization_freezes_evaluation_not_promotion",
    "gradient_formula_directional_derivative_exact",
    "negative_gradient_descent_identity_exact",
    "accepted_w2_16_endpoint_is_stationary_exact",
    "formation_F2_gap_and_separable_no_cross_response_explicit",
    "closure_and_scope_ledgers_exact_boolean",
})
DEPENDENCY_CONTROL_KEYS = frozenset({
    "w2_16_identity_and_report_valid",
    "w2_16_U_law_and_F2_endpoint_frozen",
    "w2_17_identity_and_report_valid",
    "w2_17_gate_map_control_and_preload_registries_match",
    "w2_17_accepts_candidate_map_schema_but_not_eligibility",
    "w2_18_static_no_go_requires_new_dynamic_candidate",
})
FAIL_CLOSED_CONTROL_KEYS = frozenset({
    "baseline_contract_schema_valid",
    "every_missing_contract_key_invalid",
    "extra_contract_key_invalid",
    "nonboolean_or_promoted_closure_invalid",
    "actual_false_gate_map_valid_ineligible_and_unpromoted",
    "synthetic_all_true_complete_maps_eligible_but_never_self_promoted",
    "each_single_false_gate_blocks_eligibility",
    "missing_extra_or_nonboolean_gate_invalid",
    "missing_extra_malformed_or_partial_map_fails_closed",
    "nested_duties_maps_and_forbidden_freedoms_fail_closed",
    "complete_contract_content_mutation_invalid",
    "coordinated_candidate_status_mutation_invalid",
    "coordinated_closure_mutation_invalid",
    "authorization_bit_cannot_promote_science",
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


def matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def transpose_split(matrix: sp.MatrixBase) -> tuple[sp.Matrix, sp.Matrix]:
    return (
        sp.simplify((matrix + matrix.T) / 2),
        sp.simplify((matrix - matrix.T) / 2),
    )


def invariant_law(
    matrix: sp.MatrixBase,
    alpha: sp.Expr,
    b: sp.Expr,
    c: sp.Expr,
    eta: sp.Expr,
    d: sp.Expr,
) -> sp.Expr:
    symmetric, skew = transpose_split(matrix)
    i2 = sp.trace(symmetric**2)
    i3 = sp.trace(symmetric**3)
    j = -sp.trace(skew**2)
    return sp.expand(-alpha * i2 / 2 - b * i3 / 3 + c * i2**2 / 4 - eta * j / 2 + d * j**2 / 4)


def frobenius_gradient(
    matrix: sp.MatrixBase,
    alpha: sp.Expr,
    b: sp.Expr,
    c: sp.Expr,
    eta: sp.Expr,
    d: sp.Expr,
) -> sp.Matrix:
    symmetric, skew = transpose_split(matrix)
    i2 = sp.trace(symmetric**2)
    j = -sp.trace(skew**2)
    identity = sp.eye(matrix.rows)
    symmetric_gradient = (
        (-alpha + c * i2) * symmetric
        - b * (symmetric**2 - i2 * identity / matrix.rows)
    )
    skew_gradient = (d * j - eta) * skew
    return sp.simplify(symmetric_gradient + skew_gradient)


def negative_gradient_vector_field(
    matrix: sp.MatrixBase,
    alpha: sp.Expr,
    b: sp.Expr,
    c: sp.Expr,
    eta: sp.Expr,
    d: sp.Expr,
) -> sp.Matrix:
    return sp.simplify(-frobenius_gradient(matrix, alpha, b, c, eta, d))


def frozen_f3_gate_keys() -> frozenset[str]:
    """Independent literal registry; do not derive this from mutable contract state."""
    return frozenset({
        "same_chain_F1_F2_predecessors_valid",
        "state_owned_events_or_changes_derived",
        "target_free_transition_or_response_law_derived",
        "candidate_dynamics_health_and_state_space_closure_proved",
        "allowed_interventions_defined",
        "directed_intervention_response_proved",
        "correlation_and_static_ranking_excluded",
        "complete_equivalence_invariance_proved",
        "arrow_selected_by_law_not_labels_or_schedule",
        "nontrivial_direct_influence_on_predeclared_open_domain",
        "strict_relation_irreflexive_asymmetric_and_acyclic",
        "effective_order_transitive_and_reflexive_closure_antisymmetric",
        "forbidden_signal_nontransmission_proved",
        "computational_schedule_neutrality_proved",
        "null_reverse_and_target_leak_controls_pass",
        "perturbation_and_initial_condition_stability_proved",
        "independent_second_derivation_passes",
        "physical_time_metric_and_downstream_gates_remain_open",
    })


def frozen_required_candidate_maps() -> tuple[str, ...]:
    return (
        "state_space",
        "event_or_change_map",
        "complete_equivalence_action",
        "transition_or_response_law",
        "signal_support_or_update_composition",
        "allowed_interventions",
        "intervention_to_response_map",
        "direct_influence_relation",
        "transitive_effective_order",
        "forbidden_pairs",
        "no_transmission_test",
        "open_domain",
        "null_branches",
        "perturbation_class",
        "independent_crosscheck",
    )


def frozen_forbidden_preloads() -> tuple[str, ...]:
    return (
        "physical position, physical time, external clock, or 3+1 split",
        "lattice, locality graph, causal DAG, time layers, or event numbering",
        "Lorentzian metric, light cone, GR, Einstein equations, or PN/PPN target",
        "preferred basis, axis, orientation, labels, or state-external seed",
        "history, lag, memory, retarded kernel, or update arrow not derived from the law",
        "correlation, commutator sign, eigenvalue rank, or Krylov depth renamed causality",
        "algorithmic iteration or execution schedule renamed physical process order",
        "post-selection of the branch or convention that gives the desired arrow",
    )


def frozen_mandatory_controls() -> tuple[str, ...]:
    return (
        "known directed acyclic influence positive control",
        "frozen or nonresponsive null",
        "correlated but noninterventional null",
        "two-way reachability between the same event occurrences rejection",
        "directed-cycle rejection",
        "prewired target-DAG rejection",
        "basis, label, reflection, and reversal mutations",
        "execution-schedule permutation",
        "F2 nulls S=0, R=0, tau=0, tau=1, tuned branch, and singular normalization",
        "small-perturbation and allowed-initial-condition stability",
        "independent derivation not trained on the first result",
    )


def frozen_candidate_a_statuses() -> dict[str, str]:
    return {
        "state_space": "DERIVED",
        "event_or_change_map": "PARTIAL",
        "complete_equivalence_action": "DERIVED",
        "transition_or_response_law": "PARTIAL",
        "signal_support_or_update_composition": "PARTIAL",
        "allowed_interventions": "PARTIAL",
        "intervention_to_response_map": "PARTIAL",
        "direct_influence_relation": "PARTIAL",
        "transitive_effective_order": "PARTIAL",
        "forbidden_pairs": "PARTIAL",
        "no_transmission_test": "PARTIAL",
        "open_domain": "PARTIAL",
        "null_branches": "PARTIAL",
        "perturbation_class": "PARTIAL",
        "independent_crosscheck": "ABSENT",
    }


def frozen_candidate_a_map_text() -> dict[str, tuple[str, str]]:
    """Independent exact source/definition registry for every candidate map."""
    return {
        "state_space": (
            "w2_16 conditional structural endpoint",
            "A in sl(3,R), S=(A+A^T)/2 and R=(A-A^T)/2, modulo one common O(3) "
            "conjugation; no extra physical state variable is added",
        ),
        "event_or_change_map": (
            "new Candidate-A oriented-process ansatz; not Canon-derived",
            "E(A)=Class(A,F(A)) modulo common O(3) and positive tangent rescaling, where "
            "F=-grad_F U and F(A)!=0; this state-owned oriented tangent germ is a local "
            "candidate change, not a sampled parameter value, next-event rule or record",
        ),
        "complete_equivalence_action": (
            "w2_16 complete matrix-star-algebra equivalence",
            "A -> O A O^T for every O in O(3), including reflections",
        ),
        "transition_or_response_law": (
            "new imported Candidate-A law; definition frozen but unevaluated",
            "dA/dsigma=-grad_F U(A), sigma>=0; a global gauge-equivalent lambda obeys "
            "sigma(lambda)=integral_0^lambda nu(l)dl with continuous nu>0 and "
            "sigma(lambda)->infinity; neither parameter is physical time",
        ),
        "signal_support_or_update_composition": (
            "candidate positive-parameter negative-gradient semiflow",
            "after gauge fixing nu=1, Phi_{r+s}=Phi_r composed with Phi_s for r,s>=0; "
            "existence, domain closure and physical signal meaning remain evaluator duties",
        ),
        "allowed_interventions": (
            "candidate tangent-state intervention class",
            "pure-S deltaA=deltaS in Sym_0(3), pure-R deltaA=deltaR in so(3), and their "
            "finite sums, small enough to stay in the declared domain; quotient infinitesimal "
            "common-O(3) gauge tangents [omega,A], and add no coefficient or target fitting",
        ),
        "intervention_to_response_map": (
            "linearized candidate semiflow",
            "for every sigma>0 with both trajectories in-domain, deltaA at E(A) maps to "
            "D Phi_sigma(A)[deltaA]; response support is the O(3)-covariant S/R projection, "
            "whose zero/nonzero Frobenius norm is invariant; no next-event sampling is used",
        ),
        "direct_influence_relation": (
            "candidate intervention semantics, not U-ranking",
            "E(A) directly influences the positive-reachable germ E(Phi_sigma(A)) only if "
            "an allowed intervention produces a nonzero invariant projected-response norm "
            "for some declared sigma>0; U ranking alone is not the definition",
        ),
        "transitive_effective_order": (
            "transitive closure of evaluated direct influence",
            "positive-semiflow reachability may support composition, but U decrease alone is "
            "only an acyclicity certificate and is not the causal definition",
        ),
        "forbidden_pairs": (
            "predeclared Candidate-A no-signal targets",
            "the substantive channel pairs are pure-S intervention to future R projection "
            "and pure-R intervention to future S projection; pure common-O(3) tangents are "
            "gauge nulls. Reverse reachability is tested separately as an order axiom, not "
            "counted as an independent no-transmission theorem; effects on joint C are nonzero",
        ),
        "no_transmission_test": (
            "future exact variational-semigroup calculation",
            "prove the finite-semiflow Frechet blocks D_S Phi^R_sigma and D_R Phi^S_sigma "
            "vanish identically for every supported sigma>0; separately prove positive "
            "reachability has no reverse cycle. A zero static Hessian block is insufficient",
        ),
        "open_domain": (
            "predeclared formation-basin candidate domain",
            "D_gap: alpha,b,c,eta,d>0 and b^2!=3 alpha c; S has one simple largest "
            "eigenvalue with projector P_plus(S), J>0, P_R=I+2R^2/J, "
            "tau_gap=1-Tr(P_plus P_R) lies in (0,1), C=[S,R]!=0, grad_F U!=0, and the "
            "forward orbit belongs to the basin of the generic w2_16 minimum stratum. The "
            "evaluator must prove this dynamically defined spectral-gap basin nonempty, open "
            "and invariant, and must separately adjudicate whether the complete inherited "
            "F1/F2 chain survives on these off-endpoint maps",
        ),
        "null_branches": (
            "inherited endpoint nulls plus separately classified flow boundaries",
            "A=0, S=0, R=0 and C=0 nulls; tau_gap=0 and tau_gap=1 excluded readout "
            "boundaries (tau_gap=0 is not generally C=0 away from the uniaxial endpoint); "
            "tuned and singular branches, spectral-gap/basin boundaries, the stationary "
            "accepted F2 endpoint, and the excluded ascent sign",
        ),
        "perturbation_class": (
            "candidate initial-state perturbations only",
            "small traceless perturbations preserving the same open basin and simple-support "
            "branch; coefficient, physical-clock and target perturbations are excluded",
        ),
        "independent_crosscheck": (
            "reserved for the separate evaluator",
            "requires a second derivation of the flow, invariant basin, intervention response "
            "and forbidden-pair zeros that is not trained on the first calculation",
        ),
    }


def candidate_a_gate_map() -> dict[str, bool]:
    """Outcome-neutral contract: every scientific F3 evaluator gate is false."""
    return {key: False for key in frozen_f3_gate_keys()}


def candidate_map_fixture(status: str = "DERIVED") -> dict[str, dict[str, str]]:
    if status not in CANDIDATE_MAP_STATUSES:
        raise ValueError(f"unsupported candidate-map status: {status}")
    return {
        key: {
            "status": status,
            "source": "LOGIC_TEST_FIXTURE_NOT_SCIENTIFIC_EVIDENCE",
            "definition": f"schema fixture for {key}",
        }
        for key in frozen_required_candidate_maps()
    }


def candidate_map_schema_valid(candidate_maps: Any) -> bool:
    if not isinstance(candidate_maps, dict) or set(candidate_maps) != set(
        frozen_required_candidate_maps()
    ):
        return False
    for entry in candidate_maps.values():
        if not isinstance(entry, dict) or set(entry) != CANDIDATE_MAP_ENTRY_KEYS:
            return False
        if entry["status"] not in CANDIDATE_MAP_STATUSES:
            return False
        if not isinstance(entry["source"], str) or not entry["source"].strip():
            return False
        if not isinstance(entry["definition"], str) or not entry["definition"].strip():
            return False
    return True


def candidate_map_content_frozen(candidate_maps: Any) -> bool:
    return bool(
        candidate_map_schema_valid(candidate_maps)
        and {key: entry["status"] for key, entry in candidate_maps.items()}
        == EXPECTED_CANDIDATE_A_STATUSES
        == frozen_candidate_a_statuses()
        and {
            key: (entry["source"], entry["definition"])
            for key, entry in candidate_maps.items()
        } == frozen_candidate_a_map_text()
    )


def candidate_screen(gates: Any, candidate_maps: Any) -> dict[str, bool]:
    gate_schema_valid = bool(
        isinstance(gates, dict)
        and set(gates) == frozen_f3_gate_keys()
        and all(type(value) is bool for value in gates.values())
    )
    map_schema_valid = candidate_map_schema_valid(candidate_maps)
    maps_complete = bool(
        map_schema_valid
        and all(entry["status"] == "DERIVED" for entry in candidate_maps.values())
    )
    valid = bool(gate_schema_valid and map_schema_valid)
    return {
        "valid": valid,
        "eligible": bool(valid and maps_complete and all(gates.values())),
        "promoted": False,
    }


def contract_schema_valid(contract: Any) -> bool:
    if not isinstance(contract, dict) or set(contract) != REQUIRED_CONTRACT_KEYS:
        return False
    closure = contract.get("CLOSURE_FLAGS")
    scope = contract.get("SCOPE_CEILING")
    authorization = contract.get("AUTHORIZATION")
    ledger = contract.get("FREEDOM_LEDGER")
    return bool(
        scientific_contract_sha256(contract) == frozen_scientific_contract_sha256()
        and isinstance(closure, dict)
        and closure == EXPECTED_CLOSURE_FLAGS == frozen_closure_flags()
        and all(type(value) is bool for value in closure.values())
        and isinstance(scope, dict)
        and scope == EXPECTED_SCOPE_CEILING == frozen_scope_ceiling()
        and all(type(value) is bool for value in scope.values())
        and isinstance(authorization, dict)
        and authorization == EXPECTED_AUTHORIZATION == frozen_authorization()
        and all(type(value) is bool for value in authorization.values())
        and contract.get("F3_EVALUATION_DUTIES")
        == EXPECTED_F3_EVALUATION_DUTIES
        == {key: "UNEVALUATED_REQUIRED" for key in frozen_f3_gate_keys()}
        and isinstance(ledger, dict)
        and ledger == EXPECTED_FREEDOM_LEDGER == frozen_freedom_ledger()
        and contract.get("CANDIDATE_DEFINITION")
        == EXPECTED_CANDIDATE_DEFINITION
        == frozen_candidate_definition()
        and contract.get("DOMAIN_AND_NULLS")
        == EXPECTED_DOMAIN_AND_NULLS
        == frozen_domain_and_nulls()
        and all(
            ledger.get(key) == expected
            for key, expected in EXPECTED_CRITICAL_FREEDOM_ENTRIES.items()
        )
        and tuple(contract.get("REQUIRED_CANDIDATE_MAPS", ()))
        == frozen_required_candidate_maps()
        and tuple(contract.get("FORBIDDEN_PRELOADS", ())) == frozen_forbidden_preloads()
        and tuple(contract.get("MANDATORY_CONTROLS", ())) == frozen_mandatory_controls()
    )


def load_sibling(filename: str, module_name: str) -> ModuleType:
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def symbolic_definition_controls() -> dict[str, bool]:
    alpha, b, c, eta, d = sp.symbols("alpha b c eta d", positive=True)
    q = sp.symbols("q0:8", real=True)
    matrix = sp.Matrix([
        [q[0], q[1], q[2]],
        [q[3], q[4], q[5]],
        [q[6], q[7], -q[0] - q[4]],
    ])
    gradient = frobenius_gradient(matrix, alpha, b, c, eta, d)
    law = invariant_law(matrix, alpha, b, c, eta, d)
    directional_residuals = []
    for coordinate in q:
        tangent = matrix.diff(coordinate)
        directional_residuals.append(
            sp.simplify(sp.diff(law, coordinate) - sp.trace(gradient.T * tangent))
        )

    flow = -gradient
    descent_residual = sp.simplify(
        sp.trace(gradient.T * flow) + sp.trace(gradient.T * gradient)
    )
    gradient_norm = sp.expand(sp.trace(gradient.T * gradient))
    manifest_sum_of_squares = sp.expand(sum(entry**2 for entry in gradient))

    discriminant = sp.sqrt(b**2 + 24 * alpha * c)
    s_plus = (b + discriminant) / (4 * c)
    projector = sp.diag(1, 0, 0)
    symmetric_endpoint = sp.simplify(s_plus * (projector - sp.eye(3) / 3))
    radius = sp.sqrt(eta / (4 * d))
    skew_endpoint = sp.Matrix([
        [0, 0, radius],
        [0, 0, -radius],
        [-radius, radius, 0],
    ])
    endpoint = symmetric_endpoint + skew_endpoint
    endpoint_gradient = frobenius_gradient(endpoint, alpha, b, c, eta, d)

    definition = CLAIM_CONTRACT["CANDIDATE_DEFINITION"]
    ledger = CLAIM_CONTRACT["FREEDOM_LEDGER"]
    validity = CLAIM_CONTRACT["VALIDITY_HEALTH"]
    return {
        "full_CODES_scientific_schema_exact": contract_schema_valid(CLAIM_CONTRACT),
        "candidate_identity_and_origin_boundary_frozen": all((
            definition["origin_status"]
            == "NEW_IMPORTED_PROCESS_PACKAGE_NOT_CANON_DERIVED",
            "None of these choices is a Theory_Canon-derived fact"
            in CLAIM_CONTRACT["ASSUMPTIONS"],
            CLAIM_CONTRACT["TYPE"] == "OUTCOME_NEUTRAL_DYNAMIC_CANDIDATE_CONTRACT",
        )),
        "freedom_ledger_complete_and_no_new_fitted_coefficient": all((
            frozenset(ledger) == EXPECTED_FREEDOM_KEYS,
            ledger["descent_sign_and_process_principle"]["complexity"]
            == "1 discrete choice; 0 new continuous coefficients",
            ledger["kinetic_metric_and_relative_mobility"]["complexity"]
            == (
                "1 fixed dimensionless continuous input rho=mu_R/mu_S=1 plus the selected "
                "full-A mobility class; 0 fitted parameters"
            ),
            "independent positive S/R weights"
            in ledger["kinetic_metric_and_relative_mobility"]["source"],
            ledger["off_endpoint_relational_readout_candidate"]["complexity"]
            == "1 fixed map choice; 0 fitted parameters",
            ledger["intervention_class"]["complexity"]
            == "1 fixed diagnostic class; 0 fitted parameters",
            ledger["new_continuous_or_fitted_coefficients"]["allowed_range"] == 0,
        )),
        "positive_reparameterization_is_gauge_not_physical_time": all((
            definition["oriented_flow"] == "dA/dsigma=-grad_F U, sigma>=0",
            "continuous nu>0" in definition["gauge"],
            "unbounded cumulative range" in definition["gauge"],
            "no physical duration or clock" in definition["semantic_limit"],
            ledger["physical_time_clock_rate_or_schedule"]["allowed_range"] == 0,
        )),
        "candidate_maps_complete_exact_and_unevaluated": all((
            candidate_map_content_frozen(CANDIDATE_A_MAPS),
            any(entry["status"] != "DERIVED" for entry in CANDIDATE_A_MAPS.values()),
        )),
        "all_w2_17_registries_frozen_exactly": all((
            F3_GATE_KEYS == frozen_f3_gate_keys(),
            REQUIRED_CANDIDATE_MAPS == frozen_required_candidate_maps(),
            FORBIDDEN_PRELOADS == frozen_forbidden_preloads(),
            MANDATORY_CONTROLS == frozen_mandatory_controls(),
            len(F3_GATE_KEYS) == 18,
            len(REQUIRED_CANDIDATE_MAPS) == 15,
            len(FORBIDDEN_PRELOADS) == 8,
            len(MANDATORY_CONTROLS) == 11,
        )),
        "all_F3_evaluation_outcomes_false": all(
            value is False for value in candidate_a_gate_map().values()
        ),
        "authorization_freezes_evaluation_not_promotion": all((
            CANDIDATE_A_EVALUATION_AUTHORIZED is True,
            CANDIDATE_A_F3_PROMOTION_AUTHORIZED is False,
            GRADIENT_ROUTE_CONDITIONAL_FORMATION_ORDER_EVALUATION_AUTHORIZED is True,
            GRADIENT_ROUTE_FULL_F3_PROMOTION_AUTHORIZED is False,
            definition["maximum_authorized_evaluator_outcome"]
            == "CONDITIONAL_CANDIDATE_RELATIVE_FORMATION_ORDER_THEOREM",
            CLAIM_CONTRACT["AUTHORIZATION"]["separate_evaluator_authorized"] is True,
            CLAIM_CONTRACT["AUTHORIZATION"][
                "conditional_candidate_relative_formation_order_evaluation_authorized"
            ] is True,
            CLAIM_CONTRACT["AUTHORIZATION"]["full_w2_17_F3_promotion_authorized"]
            is False,
            CLAIM_CONTRACT["AUTHORIZATION"]["scientific_promotion_authorized"] is False,
        )),
        "gradient_formula_directional_derivative_exact": all((
            all(residual == 0 for residual in directional_residuals),
            sp.simplify(sp.trace(gradient)) == 0,
        )),
        "negative_gradient_descent_identity_exact": all((
            descent_residual == 0,
            sp.simplify(gradient_norm - manifest_sum_of_squares) == 0,
            all(entry.is_real is True for entry in gradient),
        )),
        "accepted_w2_16_endpoint_is_stationary_exact": all((
            matrix_zero(endpoint_gradient),
            sp.simplify(2 * c * s_plus**2 - b * s_plus - 3 * alpha) == 0,
            sp.simplify(d * (eta / d) - eta) == 0,
        )),
        "formation_F2_gap_and_separable_no_cross_response_explicit": all(
            token in validity for token in (
                "separable", "no cross-channel", "event-frozen", "outside",
                "imported dissipative process postulate",
            )
        ),
        "closure_and_scope_ledgers_exact_boolean": all((
            scientific_contract_sha256(CLAIM_CONTRACT)
            == frozen_scientific_contract_sha256(),
            CLAIM_CONTRACT["CLOSURE_FLAGS"]
            == EXPECTED_CLOSURE_FLAGS
            == frozen_closure_flags(),
            CLAIM_CONTRACT["SCOPE_CEILING"]
            == EXPECTED_SCOPE_CEILING
            == frozen_scope_ceiling(),
            all(type(value) is bool for value in EXPECTED_CLOSURE_FLAGS.values()),
            all(type(value) is bool for value in EXPECTED_SCOPE_CEILING.values()),
        )),
    }


def dependency_controls() -> dict[str, bool]:
    w216 = load_sibling(
        "w2_16_f2b_general_traceless_single_carrier_candidate_gate.py", "w2_16_w219_dependency"
    )
    w217 = load_sibling(
        "w2_17_f3_internal_order_causality_contract.py", "w2_17_w219_dependency"
    )
    w218 = load_sibling(
        "w2_18_f3_static_endpoint_adjudication_gate.py", "w2_18_w219_dependency"
    )
    report16 = w216.run()
    report17 = w217.run()
    report18 = w218.run()
    actual_screen = w217.candidate_screen(candidate_a_gate_map(), CANDIDATE_A_MAPS)
    return {
        "w2_16_identity_and_report_valid": all((
            w216.CLAIM_CONTRACT["CLAIM_ID"]
            == "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CANDIDATE_001",
            report16.get("valid") is True,
            report16.get("closure_decision", {}).get(
                "full_W2_F2_operational_relations_proved"
            ) is True,
        )),
        "w2_16_U_law_and_F2_endpoint_frozen": all((
            "U(A)=V_F1(S)" in w216.CLAIM_CONTRACT["THEOREM"]["global_minimum_product"],
            w216.CLAIM_CONTRACT["CONVENTIONS"].find("C=[S,R]") >= 0,
            w216.CLAIM_CONTRACT["DOMAIN_AND_NULLS"]["generic_pass_domain"]
            == "alpha,b,c,eta,d>0, b^2!=3 alpha c, 0<tau<1.",
            exact_true_map(report16["controls"]["minimum"], frozenset({
                "skew_J_is_nonnegative_exact",
                "skew_square_completion_exact",
                "skew_nonzero_global_radius_exact",
                "old_s_positive_root_exact",
                "old_s_stationarity_exact",
                "product_minimum_separability_exact",
                "open_five_parameter_domain",
                "mixed_coefficients_remain_exact_zero",
            })),
        )),
        "w2_17_identity_and_report_valid": all((
            w217.CLAIM_CONTRACT["CLAIM_ID"] == "W2_F3_INTERNAL_ORDER_CAUSALITY_CONTRACT_001",
            report17.get("valid") is True,
        )),
        "w2_17_gate_map_control_and_preload_registries_match": all((
            w217.frozen_f3_gate_keys() == frozen_f3_gate_keys(),
            w217.frozen_required_candidate_maps() == frozen_required_candidate_maps(),
            w217.frozen_forbidden_preloads() == frozen_forbidden_preloads(),
            w217.frozen_mandatory_controls() == frozen_mandatory_controls(),
        )),
        "w2_17_accepts_candidate_map_schema_but_not_eligibility": all((
            w217.candidate_map_schema_valid(CANDIDATE_A_MAPS),
            actual_screen["valid"],
            not actual_screen["eligible"],
            not actual_screen["promoted"],
        )),
        "w2_18_static_no_go_requires_new_dynamic_candidate": all((
            w218.CLAIM_CONTRACT["CLAIM_ID"] == "W2_F3_STATIC_ENDPOINT_ADJUDICATION_001",
            report18.get("valid") is True,
            w218.CLAIM_CONTRACT["CLOSURE_FLAGS"]["static_F2_only_route_rejected_as_F3_realization"],
            w218.CLAIM_CONTRACT["CLOSURE_FLAGS"]["new_dynamic_candidate_required"],
            not w218.CLAIM_CONTRACT["CLOSURE_FLAGS"]["F3_internal_order_or_causality_proved"],
        )),
    }


def fail_closed_controls() -> dict[str, bool]:
    all_true = {key: True for key in frozen_f3_gate_keys()}
    complete_maps = candidate_map_fixture("DERIVED")
    synthetic = candidate_screen(all_true, complete_maps)
    actual = candidate_screen(candidate_a_gate_map(), CANDIDATE_A_MAPS)

    missing_contract_results = []
    for key in REQUIRED_CONTRACT_KEYS:
        mutated = dict(CLAIM_CONTRACT)
        mutated.pop(key)
        missing_contract_results.append(not contract_schema_valid(mutated))
    extra_contract = dict(CLAIM_CONTRACT)
    extra_contract["SELF_ATTESTED_PASS"] = True
    promoted_closure = dict(CLAIM_CONTRACT)
    promoted_closure["CLOSURE_FLAGS"] = dict(CLAIM_CONTRACT["CLOSURE_FLAGS"])
    promoted_closure["CLOSURE_FLAGS"]["F3_internal_order_or_causality_proved"] = True
    nonboolean_closure = dict(CLAIM_CONTRACT)
    nonboolean_closure["CLOSURE_FLAGS"] = dict(CLAIM_CONTRACT["CLOSURE_FLAGS"])
    nonboolean_closure["CLOSURE_FLAGS"]["Candidate_A_evaluated"] = 0
    mutated_claim_contract = dict(CLAIM_CONTRACT)
    mutated_claim_contract["CLAIM"] = "FOUNDATION F3 PROVED"

    coordinated_status_maps = {
        key: dict(value) for key, value in CANDIDATE_A_MAPS.items()
    }
    coordinated_status_maps["independent_crosscheck"]["status"] = "PARTIAL"
    coordinated_status_expected = dict(EXPECTED_CANDIDATE_A_STATUSES)
    coordinated_status_expected["independent_crosscheck"] = "PARTIAL"
    coordinated_status_values = {
        key: value["status"] for key, value in coordinated_status_maps.items()
    }

    coordinated_closure_contract = dict(CLAIM_CONTRACT)
    coordinated_closure_contract["CLOSURE_FLAGS"] = dict(
        CLAIM_CONTRACT["CLOSURE_FLAGS"]
    )
    coordinated_closure_contract["CLOSURE_FLAGS"][
        "Candidate_A_flow_or_basin_proved"
    ] = True
    coordinated_closure_expected = dict(EXPECTED_CLOSURE_FLAGS)
    coordinated_closure_expected["Candidate_A_flow_or_basin_proved"] = True

    single_false_results = []
    malformed_gate_results = []
    for key in frozen_f3_gate_keys():
        one_false = dict(all_true)
        one_false[key] = False
        single_false_results.append(candidate_screen(one_false, complete_maps))
        missing = dict(all_true)
        missing.pop(key)
        malformed_gate_results.append(candidate_screen(missing, complete_maps))
        nonboolean = dict(all_true)
        nonboolean[key] = 1
        malformed_gate_results.append(candidate_screen(nonboolean, complete_maps))
    extra_gate = dict(all_true)
    extra_gate["SELF_ATTESTED_PASS"] = True
    malformed_gate_results.append(candidate_screen(extra_gate, complete_maps))

    missing_map = {key: dict(value) for key, value in complete_maps.items()}
    missing_map.pop(next(iter(missing_map)))
    extra_map = {key: dict(value) for key, value in complete_maps.items()}
    extra_map["SELF_ATTESTED_MAP"] = {
        "status": "DERIVED", "source": "invalid", "definition": "invalid"
    }
    malformed_map = {key: dict(value) for key, value in complete_maps.items()}
    malformed_map[next(iter(malformed_map))]["status"] = "SELF_ATTESTED_PASS"
    partial_maps = candidate_map_fixture("PARTIAL")

    altered_domain_map = {key: dict(value) for key, value in CANDIDATE_A_MAPS.items()}
    altered_domain_map["open_domain"]["definition"] = "UNDEFINED DOMAIN"
    altered_duty = dict(CLAIM_CONTRACT)
    altered_duty["F3_EVALUATION_DUTIES"] = dict(
        CLAIM_CONTRACT["F3_EVALUATION_DUTIES"]
    )
    altered_duty["F3_EVALUATION_DUTIES"][next(iter(frozen_f3_gate_keys()))] = "PROVED"
    altered_target_freedom = dict(CLAIM_CONTRACT)
    altered_target_freedom["FREEDOM_LEDGER"] = {
        key: dict(value) for key, value in CLAIM_CONTRACT["FREEDOM_LEDGER"].items()
    }
    altered_target_freedom["FREEDOM_LEDGER"][
        "position_lattice_graph_metric_or_GR_target"
    ]["allowed_range"] = 1
    altered_mobility = dict(CLAIM_CONTRACT)
    altered_mobility["FREEDOM_LEDGER"] = {
        key: dict(value) for key, value in CLAIM_CONTRACT["FREEDOM_LEDGER"].items()
    }
    altered_mobility["FREEDOM_LEDGER"][
        "kinetic_metric_and_relative_mobility"
    ]["allowed_range"] = "rho arbitrary"
    altered_definition = dict(CLAIM_CONTRACT)
    altered_definition["CANDIDATE_DEFINITION"] = dict(
        CLAIM_CONTRACT["CANDIDATE_DEFINITION"]
    )
    altered_definition["CANDIDATE_DEFINITION"]["gradient"] = "WRONG"
    altered_domain_contract = dict(CLAIM_CONTRACT)
    altered_domain_contract["DOMAIN_AND_NULLS"] = dict(
        CLAIM_CONTRACT["DOMAIN_AND_NULLS"]
    )
    altered_domain_contract["DOMAIN_AND_NULLS"]["evaluation_domain"] = "UNDEFINED DOMAIN"

    return {
        "baseline_contract_schema_valid": contract_schema_valid(CLAIM_CONTRACT),
        "every_missing_contract_key_invalid": all(missing_contract_results),
        "extra_contract_key_invalid": not contract_schema_valid(extra_contract),
        "nonboolean_or_promoted_closure_invalid": all((
            not contract_schema_valid(promoted_closure),
            not contract_schema_valid(nonboolean_closure),
        )),
        "actual_false_gate_map_valid_ineligible_and_unpromoted": all((
            actual["valid"], not actual["eligible"], not actual["promoted"]
        )),
        "synthetic_all_true_complete_maps_eligible_but_never_self_promoted": all((
            synthetic["valid"], synthetic["eligible"], not synthetic["promoted"]
        )),
        "each_single_false_gate_blocks_eligibility": all(
            result["valid"] and not result["eligible"] and not result["promoted"]
            for result in single_false_results
        ),
        "missing_extra_or_nonboolean_gate_invalid": all(
            not result["valid"] and not result["eligible"] and not result["promoted"]
            for result in malformed_gate_results
        ),
        "missing_extra_malformed_or_partial_map_fails_closed": all((
            not candidate_screen(all_true, missing_map)["valid"],
            not candidate_screen(all_true, extra_map)["valid"],
            not candidate_screen(all_true, malformed_map)["valid"],
            candidate_screen(all_true, partial_maps)["valid"],
            not candidate_screen(all_true, partial_maps)["eligible"],
            not candidate_screen(all_true, partial_maps)["promoted"],
        )),
        "nested_duties_maps_and_forbidden_freedoms_fail_closed": all((
            not candidate_map_content_frozen(altered_domain_map),
            not contract_schema_valid(altered_duty),
            not contract_schema_valid(altered_target_freedom),
            not contract_schema_valid(altered_mobility),
            not contract_schema_valid(altered_definition),
            not contract_schema_valid(altered_domain_contract),
        )),
        "complete_contract_content_mutation_invalid": all((
            not contract_schema_valid(mutated_claim_contract),
            scientific_contract_sha256(mutated_claim_contract)
            != frozen_scientific_contract_sha256(),
        )),
        "coordinated_candidate_status_mutation_invalid": all((
            coordinated_status_values == coordinated_status_expected,
            coordinated_status_values != frozen_candidate_a_statuses(),
            not candidate_map_content_frozen(coordinated_status_maps),
        )),
        "coordinated_closure_mutation_invalid": all((
            coordinated_closure_contract["CLOSURE_FLAGS"]
            == coordinated_closure_expected,
            coordinated_closure_expected != frozen_closure_flags(),
            not contract_schema_valid(coordinated_closure_contract),
        )),
        "authorization_bit_cannot_promote_science": all((
            CANDIDATE_A_EVALUATION_AUTHORIZED,
            not CANDIDATE_A_F3_PROMOTION_AUTHORIZED,
            GRADIENT_ROUTE_CONDITIONAL_FORMATION_ORDER_EVALUATION_AUTHORIZED,
            not GRADIENT_ROUTE_FULL_F3_PROMOTION_AUTHORIZED,
            not actual["promoted"],
            CLAIM_CONTRACT["CLOSURE_FLAGS"]["Candidate_A_evaluated"] is False,
            CLAIM_CONTRACT["CLOSURE_FLAGS"][
                "conditional_candidate_relative_formation_order_proved"
            ] is False,
            CLAIM_CONTRACT["CLOSURE_FLAGS"][
                "persistent_internal_phase_or_record_proved"
            ] is False,
            CLAIM_CONTRACT["CLOSURE_FLAGS"]["F3_internal_order_or_causality_proved"] is False,
        )),
    }


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_safe(item) for item in value]
    return str(value)


def run() -> dict[str, Any]:
    controls = {
        "definition": symbolic_definition_controls(),
        "dependency": dependency_controls(),
        "fail_closed": fail_closed_controls(),
    }
    group_valid = {
        "definition": exact_true_map(controls["definition"], DEFINITION_CONTROL_KEYS),
        "dependency": exact_true_map(controls["dependency"], DEPENDENCY_CONTROL_KEYS),
        "fail_closed": exact_true_map(controls["fail_closed"], FAIL_CLOSED_CONTROL_KEYS),
    }
    valid = _all_true(group_valid)
    actual_screen = candidate_screen(candidate_a_gate_map(), CANDIDATE_A_MAPS)
    return {
        "artifact": CLAIM_CONTRACT["CLAIM_ID"],
        "valid": valid,
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "Candidate A is identity-frozen. A separate evaluator may at most prove a conditional "
            "candidate-relative formation order. Full w2_17 F3 promotion is unauthorized because "
            "the generator is imported, the accepted F2 minimum is stationary, and no persistent "
            "internal phase or record is supplied. No candidate dynamics, F2-preserving formation "
            "domain, intervention response, forbidden-signal theorem, internal causal order, "
            "physical time, metric or later gate is proved."
        ),
        "evaluation_authorized": CANDIDATE_A_EVALUATION_AUTHORIZED,
        "conditional_formation_order_evaluation_authorized": (
            GRADIENT_ROUTE_CONDITIONAL_FORMATION_ORDER_EVALUATION_AUTHORIZED
        ),
        "maximum_authorized_evaluator_outcome": MAXIMUM_AUTHORIZED_EVALUATOR_OUTCOME,
        "full_w2_17_f3_promotion_authorized": (
            GRADIENT_ROUTE_FULL_F3_PROMOTION_AUTHORIZED
        ),
        "scientific_promotion_authorized": CANDIDATE_A_F3_PROMOTION_AUTHORIZED,
        "candidate_map_statuses": frozen_candidate_a_statuses(),
        "f3_gate_outcomes": candidate_a_gate_map(),
        "candidate_screen": actual_screen,
        "closure_flags": CLAIM_CONTRACT["CLOSURE_FLAGS"],
        "scope_ceiling": CLAIM_CONTRACT["SCOPE_CEILING"],
        "group_valid": group_valid,
        "controls": controls,
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
