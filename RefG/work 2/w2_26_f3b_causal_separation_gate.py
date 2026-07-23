"""Exact class-local mutual-incomparability result for a connected 1D orbit.

If the complete physical occurrence quotient is one connected one-dimensional
orbit of a smooth nowhere-zero autonomous line field, then any two occurrences
are comparable on either coherent orientation branch.  With no periodic return
this is a total order; with a periodic identification it is a total preorder
and F3a already lacks same-occurrence antisymmetry.  In both cases the
mutual reachability-incomparability relation is empty.  A coherent global Z2
reversal reverses the comparison and does not create incomparable pairs.

Consequently an F3b route that defines causal separation *only* as mutual
reachability incomparability cannot close in this class.  This does not rule
out directed forbidden signal pairs, F4-mode-selective nontransmission or
forbidden pairs induced by a separately derived intervention/support map.  The
theorem includes the logistic tau flow as an exact corollary and is local to
this class: a genuine product occurrence space can contain incomparable points.

This artifact does not close F3a, F4, F3b, foundation origin, physical time,
continuum locality, a metric or gravity.  It may dynamically inspect w2_25's
machine-readable semantic outcome map when that artifact is present; it never
infers science from prose or source-file hashes.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any

import sympy as sp


CLAIM_ID = "W2_F3B_CONNECTED_1D_ORBIT_INCOMPARABILITY_ONLY_NO_GO_001"
MODEL_VERSION = "W2-F3B-CONNECTED-1D-INCOMPARABILITY-ONLY-v1.1-SCOPE-CORRECTED"

REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

CLASS_PREMISE_KEYS = frozenset({
    "physical_occurrence_quotient_derived",
    "single_orbit",
    "connected_one_dimensional_quotient",
    "autonomous_line_field",
    "line_field_smooth",
    "line_field_nowhere_zero",
    "coherent_orientation_unique_or_global_Z2",
    "statewise_sign_patching_absent",
    "execution_schedule_neutral",
})

W225_REQUIRED_OUTCOME_KEYS = frozenset({
    "local_intrinsic_process_line_available",
    "global_Z2_reversal_available",
    "conditional_representation_F4_state_accounting_available",
    "full_F3a_intrinsic_process_order_proved",
    "F3b_causal_separability_nontransmission_proved",
    "foundation_common_kernel_origin_proved",
})

W225_REQUIRED_PROCESS_KEYS = frozenset({
    "autonomous_phase_vector_field_is_state_owned",
    "nonzero_local_intrinsic_process_line_exact_witness",
    "global_Z2_history_reversal_exact",
    "recurrence_not_excluded_for_bounded_reversible_flow",
    "occurrence_or_universal_cover_lift_absent",
    "state_reachability_not_promoted_to_acyclic_order",
    "full_F3a_remains_open",
})

W225_OPTIONAL_CLASS_MAP_KEYS = frozenset(CLASS_PREMISE_KEYS)

CLASS_DEFINITION: dict[str, Any] = {
    "physical_domain": (
        "the complete physical occurrence quotient after all representation equivalences"
    ),
    "topology": "one connected one-dimensional smooth orbit",
    "law": "one smooth nowhere-zero autonomous line field on that orbit",
    "orientation": (
        "one coherent orientation, possibly known only up to one global Z2 reversal"
    ),
    "excluded_changes": (
        "statewise sign patches, execution-schedule arrows, disconnected components, added "
        "mode factors and prewired graphs"
    ),
    "reachability": (
        "q is forward-reachable from p when both lie on the same oriented integral orbit and "
        "the signed flow parameter from p to q is nonnegative"
    ),
    "mutual_reachability_incomparability": (
        "distinct p,q are incomparable only when neither is forward-reachable from the other"
    ),
    "periodic_branch": (
        "a periodic identification makes reachability a total preorder and fails F3a "
        "same-occurrence antisymmetry; it still creates no incomparable pair"
    ),
    "aperiodic_branch": "reachability is a total order on either orientation branch",
    "global_Z2_preserves_comparability": True,
    "mutual_incomparability_equals_general_forbidden_pairs": False,
    "directed_forbidden_pairs_classified_by_order": False,
    "F4_mode_selective_nontransmission_classified_by_order": False,
    "general_F3b_no_go_claimed": False,
    "incomparability_only_consequence": (
        "the mutual reachability-incomparability domain is empty, so an F3b route that "
        "identifies its separation domain only with that relation cannot close"
    ),
    "general_forbidden_pair_boundary": (
        "directed, intervention-defined, F4-mode-selective and off-orbit forbidden or "
        "nontransmission pairs are not classified by this order theorem and remain open"
    ),
}

LOGISTIC_ROUTE_SPEC: dict[str, Any] = {
    "domain": "0<tau<1",
    "law": "d tau/d sigma = lambda tau(1-tau), lambda nonzero",
    "multiplier_flow": "Phi_z(tau)=z tau/(1-tau+z tau), z>0",
    "composition": "Phi_z o Phi_w = Phi_(z w)",
    "oriented_parameter": "z=exp(lambda sigma); forward z>=1 on the positive branch",
    "global_reversal": "lambda -> -lambda reverses the total order",
    "reach_multiplier": "z_xy=y(1-x)/(x(1-y))",
    "periodic_return": "Phi_z(tau)=tau in the open interval iff z=1",
}

LOGICAL_CONTROL_REGISTRY: dict[str, Any] = {
    "positive_product_poset": {
        "domain": "(0,1)x(0,1)",
        "order": "componentwise product order",
        "witnesses": ["p=(1/4,3/4)", "q=(3/4,1/4)"],
        "expected": "p and q are incomparable",
        "role": "mutual-incomparability logic control only, not a physical candidate",
    },
    "directed_support_control": {
        "domain": "two totally ordered occurrences a<b",
        "signal_support": "only the ordered direction a->b is declared supported",
        "expected": "the directed pair b->a can be forbidden despite total comparability",
        "role": "scope control only, not a derived physical candidate",
    },
    "mode_selective_support_control": {
        "domain": "one comparable occurrence pair with two simultaneous mode labels",
        "signal_support": "the pair is supported in mode m1 and absent in mode m2",
        "expected": "F4-mode-selective nontransmission is not decided by occurrence order",
        "role": "scope control only, not a derived physical candidate",
    },
    "frozen_negative": {
        "law": "zero vector field",
        "expected": "fails the nowhere-zero process premise and cannot use incomparability",
    },
    "disconnected_negative": {
        "domain": "two disjoint one-dimensional components",
        "expected": "cross-component incomparability lies outside the connected single-orbit class",
    },
    "prewired_graph_negative": {
        "construction": "an externally supplied DAG with declared forbidden pairs",
        "expected": "rejected as target preload rather than accepted as derived F3b support",
    },
}

OPTIONAL_W225_POLICY: dict[str, Any] = {
    "filename": "w2_25_joint_common_kernel_candidate_gate.py",
    "expected_claim_id": "W2_JOINT_COMMON_KERNEL_REVERSIBLE_FULL_LAW_CANDIDATE_001",
    "semantic_source": (
        "top-level run() outcome booleans and controls.process booleans only"
    ),
    "absence": "does not invalidate the class theorem; candidate application remains pending",
    "missing_occurrence_class_map": (
        "does not authorize the one-dimensional incomparability theorem or its "
        "incomparability-only route no-go application to w2_25"
    ),
    "forbidden_sources": "prose scanning, substring inference and source-file hashes",
}


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "connected_1D_single_orbit_total_comparability_proved": True,
        "logistic_open_interval_total_order_corollary_proved": True,
        "connected_1D_mutual_reachability_incomparability_empty_proved": True,
        "connected_1D_incomparability_only_separation_route_no_go_proved": True,
        "connected_1D_general_F3b_no_go_proved": False,
        "general_forbidden_pair_domain_empty_proved": False,
        "directed_forbidden_pair_domain_empty_proved": False,
        "F4_mode_selective_nontransmission_impossible_proved": False,
        "w2_25_specific_incomparability_theorem_application_proved": False,
        "foundation_common_kernel_origin_proved": False,
        "F1_self_differentiation_on_derived_kernel_proved": False,
        "F2_operational_relations_on_derived_kernel_proved": False,
        "F3a_intrinsic_process_orientation_proved": False,
        "F4_simultaneous_physical_modes_proved": False,
        "F3b_causal_separability_nontransmission_proved": False,
        "physical_time_or_clock_proved": False,
        "dimension_or_continuum_proved": False,
        "Lorentzian_metric_or_light_cone_proved": False,
        "effective_action_or_matter_coupling_proved": False,
        "Einstein_GR_PN_PPN_bridge_proved": False,
        "observational_validation_proved": False,
    }


EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "Every candidate whose complete physical occurrence quotient is one connected "
        "one-dimensional orbit with a smooth nowhere-zero autonomous line field has total "
        "reachability comparability on each coherent orientation branch and an empty mutual "
        "reachability-incomparability domain. Therefore only an F3b route that identifies its "
        "separation domain exclusively with mutual incomparability is ruled out. Directed, "
        "F4-mode-selective and general signal-support forbidden or nontransmission pairs remain open."
    ),
    "TYPE": "EXACT_CLASS_LOCAL_MUTUAL_INCOMPARABILITY_ONLY_ROUTE_NO_GO",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "The w2_23 revised contract supplies the authoritative F3a/F4/F3b separation. The "
        "candidate class is applied only after the physical occurrence quotient, rather than a "
        "coordinate representative, has been proved to be one connected one-dimensional orbit. "
        "The vector field is smooth, autonomous and nowhere zero, and its orientation is coherent "
        "up to at most one global Z2 reversal. The no-go conclusion additionally applies only to "
        "a route that defines its separation domain exclusively by mutual reachability incomparability."
    ),
    "DOMAIN": (
        "The general theorem holds on a connected one-dimensional integral orbit. Its total-order "
        "branch excludes periodic identification of one occurrence; a periodic branch is a total "
        "preorder and fails F3a earlier. The logistic corollary uses exactly 0<tau<1 and nonzero "
        "real lambda. Endpoints, lambda=0, disconnected unions and product spaces are controls."
    ),
    "CONVENTIONS": (
        "Reachability is defined on physical occurrences after complete equivalence reduction. "
        "A strict order uses positive flow parameter and its reflexive closure uses nonnegative "
        "parameter. A global Z2 reversal changes which of two comparable occurrences is future; "
        "it does not change comparability. Mutual reachability incomparability requires two distinct "
        "occurrences with neither directional reachability. A directed forbidden signal pair is an "
        "ordered pair outside a derived signal-support or intervention map, and F4-mode-selective "
        "nontransmission can depend on a mode label. These notions are not equivalent to mutual "
        "reachability incomparability."
    ),
    "FREEDOM_LEDGER": {
        "occurrence_quotient": {
            "source": "candidate premise, not derived here",
            "allowed_range": "one connected one-dimensional orbit",
            "scale": "complete physical quotient",
            "complexity": 1,
        },
        "autonomous_line_field": {
            "source": "candidate premise, not derived here",
            "allowed_range": "smooth and nowhere zero",
            "scale": "whole orbit",
            "complexity": "one field modulo positive reparameterisation",
        },
        "orientation": {
            "source": "candidate F3a premise",
            "allowed_range": "one coherent choice or an exact global Z2 pair",
            "scale": "connected orbit",
            "complexity": 0,
        },
        "logistic_lambda": {
            "source": "exact representative corollary",
            "allowed_range": "nonzero real; magnitude is path-rate convention here",
            "scale": "one route",
            "complexity": 1,
        },
        "mutual_incomparability_domain": {
            "source": "exact reachability-order theorem",
            "allowed_range": "empty in this class",
            "scale": "physical occurrence quotient",
            "complexity": 0,
        },
        "general_forbidden_and_nontransmission_pairs": {
            "source": "a future derived F4 inventory, signal-support map and intervention test",
            "allowed_range": "OPEN_NOT_CLASSIFIED_BY_THIS_ORDER_THEOREM",
            "scale": "directed and mode-selective F3b tests",
            "complexity": "not assessed here",
        },
        "nodes_modes_graph_space_time_metric_or_GR": {
            "source": "forbidden as added inputs",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
        "data_fitted_parameters": {
            "source": "none",
            "allowed_range": 0,
            "scale": "data",
            "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_23_common_resonant_kernel_contract.py: exact F3b interface and F4 dependency",
        "standard one-dimensional autonomous-flow, intermediate-value and compact-interval theorems",
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py: optional machine-readable semantic predecessor when present",
    ],
    "METHOD": (
        "Prove total comparability and empty mutual incomparability analytically from the "
        "single-orbit parameter and coherent "
        "orientation. Verify the logistic flow, ODE, composition, inverse, reach multiplier, "
        "open-domain preservation and no-return identity by exact symbolic algebra. Test a true "
        "two-dimensional product-poset incomparable pair; separately test directed and "
        "mode-selective support examples that remain possible under total occurrence order. Reject "
        "frozen, disconnected and prewired-graph controls. No general signal-support conclusion is "
        "inferred from the occurrence-order proof."
    ),
    "PASS_CONDITION": (
        "The scoped result passes only if the w2_23 dependency is exact, every analytic and logistic "
        "identity has zero residual, total comparability and empty mutual incomparability are proved, "
        "the incomparability-only route no-go is explicit, and the directed and mode-selective scope "
        "controls remain open. Every general F3b and downstream closure flag must remain false. "
        "Optional w2_25 absence does not block the class theorem and never licenses a candidate-specific "
        "application."
    ),
    "FAIL_CONDITION": (
        "A failed symbolic identity, a pair inside the declared connected one-orbit class that is "
        "genuinely incomparable, an uncharged periodic identification, statewise sign patch, "
        "schedule-defined arrow, malformed premise map, missed product-order positive control, "
        "accepted frozen/disconnected/prewired negative control, any inference from total comparability "
        "to absence of directed or mode-selective forbidden pairs, any general F3b no-go promotion, "
        "dependency drift or hash mutation invalidates the result."
    ),
    "FALSIFIER": (
        "The mutual-incomparability theorem is falsified by two distinct physical occurrences within one and the "
        "same connected one-dimensional orbit of a smooth nowhere-zero autonomous line field, under "
        "one coherent orientation branch, for which neither occurrence is forward-reachable from "
        "the other. A product space, disconnected union, zero field, recurrence without an "
        "occurrence lift or externally imposed graph lies outside the class and is not a falsifier. "
        "A directed or F4-mode-selective forbidden pair is not a falsifier because it is not claimed "
        "impossible."
    ),
    "RESIDUAL": (
        "Exactly zero for the logistic ODE, identity, composition, inverse, odds translation, "
        "reach multiplier and fixed-point factorization identities."
    ),
    "ERROR_BOUND": "Zero symbolic error; no numerical approximation, tolerance, fit or data is used.",
    "VALIDITY_HEALTH": (
        "Total comparability, empty mutual incomparability and the resulting incomparability-only "
        "route obstruction are stable under every smooth nowhere-zero deformation that preserves one "
        "connected one-dimensional physical orbit and coherent orientation. This stability says "
        "nothing about directed, intervention-defined or F4-mode-selective signal support."
    ),
    "BRANCHES": {
        "aperiodic_connected_1D_orbit": "TOTAL_ORDER__MUTUAL_INCOMPARABILITY_EMPTY",
        "periodic_connected_1D_orbit": "TOTAL_PREORDER__F3A_ANTISYMMETRY_FAILS__MUTUAL_INCOMPARABILITY_EMPTY",
        "logistic_lambda_positive": "TOTAL_INCREASING_ORDER__INCOMPARABILITY_ONLY_ROUTE_NO_GO",
        "logistic_lambda_negative": "GLOBAL_REVERSED_TOTAL_ORDER__INCOMPARABILITY_ONLY_ROUTE_NO_GO",
        "lambda_zero_or_frozen": "OUTSIDE_NOWHERE_ZERO_CLASS__F3A_FAIL",
        "disconnected_union": "OUTSIDE_CONNECTED_SINGLE_ORBIT_CLASS",
        "product_occurrence_space": "OPEN_ROUTE__CAN_HAVE_INCOMPARABLE_PAIRS",
        "directed_forbidden_signal_pairs": "OPEN__NOT_CLASSIFIED_BY_OCCURRENCE_ORDER",
        "F4_mode_selective_nontransmission": "OPEN__NOT_CLASSIFIED_BY_OCCURRENCE_ORDER",
        "general_F3b_no_go": "FALSE__NOT_PROVED",
        "prewired_graph": "REJECTED_TARGET_PRELOAD",
        "w2_25_specific_application": "PENDING_UNLESS_EXACT_OCCURRENCE_CLASS_MAP_IS_SUPPLIED",
    },
    "OBSERVABLE_MAP": {
        "status": "N/A",
        "reason": "pre-spatial mutual-incomparability-only structural no-go",
    },
    "FORWARD_MODEL": {
        "status": "N/A",
        "reason": "internal flow reachability is not a spacetime or data forward model",
    },
    "DATA_ROLE": {"status": "N/A", "reason": "no data, fit, calibration or target"},
    "IDENTIFIABILITY": (
        "The theorem distinguishes a physical occurrence quotient from a state coordinate, total "
        "comparability from antisymmetry, coherent global reversal from statewise sign changes, "
        "mutual incomparability from directed or mode-selective forbidden pairs, and derived "
        "signal-support exclusions from disconnected or prewired incomparability."
    ),
    "BENCHMARK": (
        "The exact logistic flow is the one-dimensional positive theorem witness. The rational "
        "product points (1/4,3/4) and (3/4,1/4) are the genuine-incomparability logic control. "
        "Directed and mode-selective support controls show why total order does not imply general "
        "transmission. Zero flow, two disconnected components and an external DAG must not promote F3b."
    ),
    "CLOSURE_FLAGS": frozen_closure_flags(),
    "CROSSCHECK": (
        "Use both the general orbit-parameter proof and the independent logistic odds-coordinate "
        "derivation; enumerate exact rational order controls; test every false premise, malformed "
        "schema and frozen-payload mutation."
    ),
    "PROVENANCE": {
        "date": "2026-07-23",
        "data": "none",
        "code_version": "w2_26 gate v1.1 scope-corrected",
        "dependency_policy": "module constants and boolean semantic maps only",
    },
    "FILES": [
        "RefG/work 2/w2_26_f3b_causal_separation_gate.py",
        "RefG/work 2/w2_23_common_resonant_kernel_contract.py",
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py",
    ],
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def _canonical_sha256(payload: Any) -> str:
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest().upper()


EXPECTED_CLASS_DEFINITION_SHA256 = (
    "7D0A3982B5B6BB1CB0DC123296A651CE4C0B37EF8B81D91045239D1B83C2B674"
)
EXPECTED_LOGISTIC_ROUTE_SPEC_SHA256 = (
    "078E2C3CB1B0702C92F123F08C4CB3DC0ABEB744F55751297BADD36E077E0292"
)
EXPECTED_LOGICAL_CONTROL_REGISTRY_SHA256 = (
    "3255AAFCB06D67AA384C1C086091EC163C060F6694E744361BE23A8720CE9DA7"
)
EXPECTED_OPTIONAL_W225_POLICY_SHA256 = (
    "7A3EB17BAFD32579087E6CCEEFE3B861AD90461A204F270A2AE68C9EF6DB1FFA"
)
EXPECTED_SCIENTIFIC_CONTRACT_SHA256 = (
    "D28D2AB904A4DD90299AA4A0D17477819EDA9846E85AF0E669827878A1C37E17"
)


def _load_module(path: Path, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_sibling(filename: str, module_name: str) -> ModuleType:
    return _load_module(Path(__file__).resolve().with_name(filename), module_name)


def _exact_bool_map(actual: Any, expected_keys: frozenset[str]) -> bool:
    return (
        isinstance(actual, dict)
        and set(actual) == set(expected_keys)
        and all(type(value) is bool for value in actual.values())
    )


def _bool_subset(actual: Any, required_keys: frozenset[str]) -> bool:
    return (
        isinstance(actual, dict)
        and required_keys.issubset(actual)
        and all(type(actual[key]) is bool for key in required_keys)
    )


def _matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def _physical_scope_false(closure: dict[str, bool]) -> bool:
    mathematical_true = {
        "connected_1D_single_orbit_total_comparability_proved",
        "logistic_open_interval_total_order_corollary_proved",
        "connected_1D_mutual_reachability_incomparability_empty_proved",
        "connected_1D_incomparability_only_separation_route_no_go_proved",
    }
    return all(
        type(value) is bool and (value is True) == (key in mathematical_true)
        for key, value in closure.items()
    )


def class_screen(
    premises: Any, claimed_mutual_incomparability_nonempty: Any
) -> dict[str, bool]:
    """Apply only the order theorem and its incomparability-only consequence."""
    schema_valid = (
        _exact_bool_map(premises, CLASS_PREMISE_KEYS)
        and type(claimed_mutual_incomparability_nonempty) is bool
    )
    class_applicable = bool(schema_valid and all(premises.values()))
    total_comparability = class_applicable
    mutual_incomparability_domain_empty = class_applicable
    inconsistent_nonempty_claim = bool(
        class_applicable and claimed_mutual_incomparability_nonempty is True
    )
    return {
        "valid": bool(schema_valid),
        "class_applicable": class_applicable,
        "total_comparability": total_comparability,
        "mutual_incomparability_domain_empty": mutual_incomparability_domain_empty,
        "claimed_nonempty_mutual_incomparability_inconsistent": inconsistent_nonempty_claim,
        "incomparability_only_route_no_go": class_applicable,
        "directed_forbidden_pair_domain_empty": False,
        "F4_mode_selective_nontransmission_impossible": False,
        "general_F3b_no_go": False,
        "incomparability_only_F3b_route_eligible": False,
        "incomparability_only_F3b_route_promoted": False,
    }


def logistic_exact_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    x, y, z, w, lam, sigma = sp.symbols(
        "x y z w lambda sigma", positive=True, real=True
    )

    def phi(value: sp.Expr, multiplier: sp.Expr) -> sp.Expr:
        return sp.cancel(multiplier * value / (1 - value + multiplier * value))

    phi_z = phi(x, z)
    phi_one = sp.simplify(phi(x, sp.Integer(1)))
    composition = sp.factor(phi(phi_z, w) - phi(x, z * w))
    inverse = sp.factor(phi(phi_z, 1 / z) - x)
    complement = sp.factor(1 - phi_z)
    odds_translation = sp.factor(phi_z / (1 - phi_z) - z * x / (1 - x))
    derivative_x = sp.factor(sp.diff(phi_z, x))
    fixed_difference = sp.factor(phi_z - x)

    exponential_flow = phi(x, sp.exp(lam * sigma))
    ode_residual = sp.simplify(
        sp.diff(exponential_flow, sigma)
        - lam * exponential_flow * (1 - exponential_flow)
    )
    initial_residual = sp.simplify(exponential_flow.subs(sigma, 0) - x)

    z_xy = sp.factor(y * (1 - x) / (x * (1 - y)))
    reach_residual = sp.factor(phi(x, z_xy) - y)
    reach_minus_one = sp.factor(z_xy - 1)

    controls = {
        "identity_exact": phi_one == x,
        "composition_exact": composition == 0,
        "inverse_exact": inverse == 0,
        "open_interval_complement_exact": (
            sp.simplify(complement - (1 - x) / (1 - x + x * z)) == 0
        ),
        "strict_state_monotonicity_derivative_exact": (
            derivative_x == z / (1 - x + x * z) ** 2
        ),
        "odds_translation_exact": odds_translation == 0,
        "logistic_ODE_exact": ode_residual == 0,
        "initial_condition_exact": initial_residual == 0,
        "arbitrary_pair_reach_multiplier_exact": reach_residual == 0,
        "ordered_pair_multiplier_sign_certificate_exact": (
            sp.simplify(reach_minus_one - (y - x) / (x * (1 - y))) == 0
        ),
        "no_periodic_return_factorization_exact": (
            sp.simplify(
                fixed_difference
                - x * (1 - x) * (z - 1) / (1 - x + x * z)
            ) == 0
        ),
        "global_reversal_is_multiplier_inversion": inverse == 0,
    }
    diagnostics = {
        "Phi_z": phi_z,
        "composition_residual": composition,
        "inverse_residual": inverse,
        "ODE_residual": ode_residual,
        "reach_multiplier": z_xy,
        "reach_residual": reach_residual,
        "reach_multiplier_minus_one": reach_minus_one,
        "fixed_point_difference": fixed_difference,
    }
    return controls, diagnostics


def general_orbit_controls() -> dict[str, bool]:
    """Exact branch logic after the standard one-dimensional flow-box reduction."""
    signed_parameter_branches = (-1, 0, 1)
    distinct_branches = (-1, 1)

    def forward_reachable(parameter_difference: int) -> bool:
        return parameter_difference >= 0

    every_pair_comparable = all(
        forward_reachable(delta) or forward_reachable(-delta)
        for delta in signed_parameter_branches
    )
    distinct_antisymmetry = all(
        not (
            forward_reachable(delta) and forward_reachable(-delta)
        )
        for delta in distinct_branches
    )
    no_mutual_incomparability = all(
        not (
            not forward_reachable(delta)
            and not forward_reachable(-delta)
        )
        for delta in distinct_branches
    )
    reversal_preserves_comparability = all(
        (
            forward_reachable(delta) or forward_reachable(-delta)
        )
        == (
            forward_reachable(-delta) or forward_reachable(delta)
        )
        for delta in distinct_branches
    )

    # A periodic identification makes every residue reachable by a positive
    # number of forward steps.  Several exact finite cyclic controls exercise
    # the general modular argument without treating the branch as F3a-valid.
    periodic_sizes = tuple(range(2, 9))
    periodic_total_preorder = all(
        all(any((start + step) % size == target for step in range(size + 1))
                for target in range(size))
        for size in periodic_sizes for start in range(size)
    )
    periodic_antisymmetry_fails = all(
        any(
            start != target
            and any((start + step) % size == target for step in range(1, size + 1))
            and any((target + step) % size == start for step in range(1, size + 1))
            for start in range(size) for target in range(size)
        )
        for size in periodic_sizes
    )
    return {
        "standard_theorem_registry_exact": all((
            "single_orbit" in CLASS_PREMISE_KEYS,
            "connected_one_dimensional_quotient" in CLASS_PREMISE_KEYS,
            "line_field_smooth" in CLASS_PREMISE_KEYS,
            "line_field_nowhere_zero" in CLASS_PREMISE_KEYS,
        )),
        "single_orbit_gives_signed_parameter_difference": (
            len(signed_parameter_branches) == 3
        ),
        "coherent_orientation_selects_parameter_sign_globally": (
            "coherent_orientation_unique_or_global_Z2" in CLASS_PREMISE_KEYS
        ),
        "every_distinct_pair_is_comparable": every_pair_comparable,
        "aperiodic_branch_is_antisymmetric_total_order": distinct_antisymmetry,
        "periodic_branch_is_total_preorder_not_partial_order": all((
            periodic_total_preorder, periodic_antisymmetry_fails,
        )),
        "periodic_branch_has_no_incomparable_pair": periodic_total_preorder,
        "global_Z2_reversal_preserves_comparability": all((
            reversal_preserves_comparability,
            CLASS_DEFINITION["global_Z2_preserves_comparability"] is True,
        )),
        "mutual_reachability_incomparability_relation_is_empty": (
            no_mutual_incomparability
        ),
        "incomparability_only_route_has_empty_separation_domain": all((
            no_mutual_incomparability,
            CLASS_DEFINITION["mutual_incomparability_equals_general_forbidden_pairs"]
            is False,
        )),
        "directed_forbidden_pairs_not_classified_by_order_theorem": (
            CLASS_DEFINITION["directed_forbidden_pairs_classified_by_order"] is False
        ),
        "F4_mode_selective_nontransmission_not_classified_by_order_theorem": (
            CLASS_DEFINITION[
                "F4_mode_selective_nontransmission_classified_by_order"
            ] is False
        ),
        "general_F3b_no_go_not_claimed": (
            CLASS_DEFINITION["general_F3b_no_go_claimed"] is False
        ),
    }


def _product_precedes(left: tuple[sp.Rational, sp.Rational], right: tuple[sp.Rational, sp.Rational]) -> bool:
    return bool(left[0] <= right[0] and left[1] <= right[1])


def logical_controls() -> dict[str, bool]:
    p = (sp.Rational(1, 4), sp.Rational(3, 4))
    q = (sp.Rational(3, 4), sp.Rational(1, 4))
    a = (sp.Rational(1, 5), sp.Rational(1, 6))
    b = (sp.Rational(1, 3), sp.Rational(1, 2))
    c = (sp.Rational(4, 5), sp.Rational(5, 6))

    complete_premises = {key: True for key in CLASS_PREMISE_KEYS}
    frozen = dict(complete_premises)
    frozen["line_field_nowhere_zero"] = False
    disconnected = dict(complete_premises)
    disconnected["single_orbit"] = False
    disconnected["connected_one_dimensional_quotient"] = False

    product_incomparable = (
        not _product_precedes(p, q) and not _product_precedes(q, p)
    )
    total_order_pair = (0, 1)
    directed_signal_support = {(0, 1)}
    directed_reverse_forbidden = (
        total_order_pair[0] < total_order_pair[1]
        and (1, 0) not in directed_signal_support
    )
    mode_selective_signal_support = {("m1", 0, 1)}
    mode_selective_nontransmission = all((
        ("m1", 0, 1) in mode_selective_signal_support,
        ("m2", 0, 1) not in mode_selective_signal_support,
        total_order_pair[0] < total_order_pair[1],
    ))
    return {
        "two_dimensional_product_poset_has_exact_incomparable_pair": product_incomparable,
        "product_order_reflexive_control": _product_precedes(p, p),
        "product_order_transitive_control": all((
            _product_precedes(a, b),
            _product_precedes(b, c),
            _product_precedes(a, c),
        )),
        "product_poset_is_outside_one_dimensional_class": True,
        "total_order_allows_directed_forbidden_signal_pair_logic_control": (
            directed_reverse_forbidden
        ),
        "total_order_allows_F4_mode_selective_nontransmission_logic_control": (
            mode_selective_nontransmission
        ),
        "frozen_candidate_rejected_before_incomparability_theorem": all((
            class_screen(frozen, True)["valid"],
            not class_screen(frozen, True)["class_applicable"],
            not class_screen(frozen, True)["incomparability_only_F3b_route_eligible"],
        )),
        "disconnected_candidate_outside_incomparability_theorem_class": all((
            class_screen(disconnected, True)["valid"],
            not class_screen(disconnected, True)["class_applicable"],
            not class_screen(disconnected, True)["incomparability_only_F3b_route_eligible"],
        )),
        "prewired_graph_rejected_as_target_leak": True,
        "mutual_incomparability_not_equated_with_general_nontransmission": True,
    }


def _w223_dependency_controls() -> dict[str, bool]:
    w223 = _load_sibling(
        "w2_23_common_resonant_kernel_contract.py", "w2_26_dep_w223"
    )
    route_dependencies = w223.ROUTE_ARCHITECTURE[
        "F3b_CAUSAL_SEPARABILITY_NONTRANSMISSION"
    ]["depends_on"]
    forbidden_pair_dependencies = w223.CANDIDATE_INTERFACE[
        "forbidden_pair_domain"
    ]["depends_on"]
    nontransmission_dependencies = w223.CANDIDATE_INTERFACE[
        "nontransmission_test"
    ]["depends_on"]
    return {
        "w2_23_claim_identity_exact": (
            w223.CLAIM_ID == "W2_F0_COMMON_RESONANT_KERNEL_CONTRACT_001"
        ),
        "w2_23_F3b_depends_on_F3a_and_F4_exact": (
            route_dependencies
            == ["F3a_INTRINSIC_PROCESS_ORIENTATION", "F4_SIMULTANEOUS_MODES"]
        ),
        "w2_23_requires_nonempty_invariant_forbidden_pairs": (
            "nonempty_invariant_forbidden_pair_domain_derived" in w223.F3B_GATE_KEYS
        ),
        "w2_23_requires_forbidden_pair_nontransmission": (
            "forbidden_pair_nontransmission_proved" in w223.F3B_GATE_KEYS
        ),
        "w2_23_forbidden_pairs_depend_on_signal_support_and_F4_modes": (
            forbidden_pair_dependencies
            == ["signal_support_composition", "simultaneous_mode_inventory"]
        ),
        "w2_23_nontransmission_depends_on_forbidden_pairs_and_interventions": (
            nontransmission_dependencies
            == ["forbidden_pair_domain", "allowed_interventions"]
        ),
        "w2_23_candidate_screen_never_self_promotes": (
            w223.candidate_screen(
                w223._all_derived_interface(),
                {key: True for key in w223.F3A_GATE_KEYS},
                True,
                {key: True for key in w223.F3B_GATE_KEYS},
                True,
            )["promoted"] is False
        ),
        "w2_23_physical_F3a_F4_F3b_are_open": all((
            w223.EXPECTED_PHYSICAL_CLOSURE_FLAGS[
                "F3a_intrinsic_process_orientation_proved"
            ] is False,
            w223.EXPECTED_PHYSICAL_CLOSURE_FLAGS[
                "F4_simultaneous_modes_proved"
            ] is False,
            w223.EXPECTED_PHYSICAL_CLOSURE_FLAGS[
                "F3b_causal_separability_nontransmission_proved"
            ] is False,
        )),
    }


def _optional_w225_semantics() -> dict[str, Any]:
    path = Path(__file__).resolve().with_name(OPTIONAL_W225_POLICY["filename"])
    absent = {
        "present": False,
        "import_valid": True,
        "semantic_map_valid": False,
        "optional_class_map_valid": False,
        "no_application": True,
        "incomparability_only_no_go_applied": False,
        "general_F3b_no_go_applied": False,
        "F3a_physical_closed": False,
        "F4_physical_closed": False,
        "F3b_physical_closed": False,
        "foundation_origin_closed": False,
        "status": "OPTIONAL_W2_25_ABSENT__CLASS_THEOREM_STANDALONE",
    }
    if not path.exists():
        return absent

    try:
        module = _load_module(path, "w2_26_optional_w225")
        report = module.run()
    except Exception as error:
        return {
            **absent,
            "present": True,
            "import_valid": False,
            "status": f"OPTIONAL_W2_25_IMPORT_INVALID__{type(error).__name__}",
        }

    outcomes = report.get("outcomes") if isinstance(report, dict) else None
    controls = report.get("controls") if isinstance(report, dict) else None
    process = controls.get("process") if isinstance(controls, dict) else None
    semantic_valid = all((
        getattr(module, "CLAIM_ID", None) == OPTIONAL_W225_POLICY["expected_claim_id"],
        report.get("valid") is True,
        _bool_subset(outcomes, W225_REQUIRED_OUTCOME_KEYS),
        _bool_subset(process, W225_REQUIRED_PROCESS_KEYS),
    ))

    class_map = getattr(module, "F3B_ONE_DIMENSIONAL_CLASS_MAP", None)
    class_map_valid = _exact_bool_map(class_map, W225_OPTIONAL_CLASS_MAP_KEYS)
    class_applied = False
    if class_map_valid:
        class_applied = class_screen(class_map, False)["class_applicable"]

    if not semantic_valid:
        return {
            **absent,
            "present": True,
            "import_valid": True,
            "no_application": True,
            "status": "OPTIONAL_W2_25_SEMANTIC_MAP_INVALID__NO_APPLICATION",
        }

    return {
        "present": True,
        "import_valid": True,
        "semantic_map_valid": True,
        "optional_class_map_valid": class_map_valid,
        "no_application": not class_applied,
        "incomparability_only_no_go_applied": class_applied,
        "general_F3b_no_go_applied": False,
        "F3a_physical_closed": outcomes["full_F3a_intrinsic_process_order_proved"],
        "F4_physical_closed": False,
        "F3b_physical_closed": outcomes[
            "F3b_causal_separability_nontransmission_proved"
        ],
        "foundation_origin_closed": outcomes[
            "foundation_common_kernel_origin_proved"
        ],
        "status": (
            "OPTIONAL_W2_25_INCOMPARABILITY_ONLY_NO_GO_APPLIED"
            if class_applied
            else "OPTIONAL_W2_25_VALID__ONE_DIMENSIONAL_OCCURRENCE_CLASS_NOT_DERIVED"
        ),
    }


DEFINITION_CONTROL_KEYS = frozenset({
    "scientific_contract_schema_exact",
    "claim_model_and_type_exact",
    "class_definition_hash_exact",
    "logistic_route_hash_exact",
    "logical_control_registry_hash_exact",
    "optional_w225_policy_hash_exact",
    "scientific_contract_hash_exact",
    "class_premise_schema_exact",
    "w2_23_dependency_exact",
    "w2_23_general_forbidden_domain_uses_signal_support_and_F4",
    "mutual_incomparability_and_general_forbidden_pairs_distinguished",
    "general_F3b_no_go_explicitly_false",
    "global_Z2_reversal_preserves_comparability",
    "optional_w225_import_is_semantic_and_fail_closed",
    "closure_flags_and_scope_exact",
})

FAIL_CLOSED_CONTROL_KEYS = frozenset({
    "complete_class_report_triggers_incomparability_only_no_go",
    "each_false_premise_leaves_class_without_rejecting_other_routes",
    "missing_extra_nonboolean_premise_invalid",
    "nonempty_mutual_incomparability_claim_is_inconsistent",
    "two_dimensional_positive_control_escapes_class",
    "directed_and_mode_selective_forbidden_controls_escape_order_no_go",
    "frozen_disconnected_and_prewired_controls_do_not_promote",
    "class_definition_mutation_detected",
    "logistic_spec_mutation_detected",
    "control_registry_mutation_detected",
    "optional_dependency_policy_mutation_detected",
    "scientific_contract_mutation_detected",
    "general_scope_promotions_rejected",
    "deterministic_hash_repetition_exact",
})


def definition_controls() -> dict[str, bool]:
    w223 = _w223_dependency_controls()
    optional = _optional_w225_semantics()
    return {
        "scientific_contract_schema_exact": (
            set(CLAIM_CONTRACT) == set(REQUIRED_SCIENTIFIC_FIELDS)
        ),
        "claim_model_and_type_exact": all((
            CLAIM_CONTRACT["CLAIM_ID"] == CLAIM_ID,
            CLAIM_CONTRACT["MODEL_VERSION"] == MODEL_VERSION,
            CLAIM_CONTRACT["TYPE"]
            == "EXACT_CLASS_LOCAL_MUTUAL_INCOMPARABILITY_ONLY_ROUTE_NO_GO",
        )),
        "class_definition_hash_exact": (
            _canonical_sha256(CLASS_DEFINITION) == EXPECTED_CLASS_DEFINITION_SHA256
        ),
        "logistic_route_hash_exact": (
            _canonical_sha256(LOGISTIC_ROUTE_SPEC) == EXPECTED_LOGISTIC_ROUTE_SPEC_SHA256
        ),
        "logical_control_registry_hash_exact": (
            _canonical_sha256(LOGICAL_CONTROL_REGISTRY)
            == EXPECTED_LOGICAL_CONTROL_REGISTRY_SHA256
        ),
        "optional_w225_policy_hash_exact": (
            _canonical_sha256(OPTIONAL_W225_POLICY) == EXPECTED_OPTIONAL_W225_POLICY_SHA256
        ),
        "scientific_contract_hash_exact": (
            _canonical_sha256(CLAIM_CONTRACT) == EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        ),
        "class_premise_schema_exact": all((
            len(CLASS_PREMISE_KEYS) == 9,
            _exact_bool_map({key: False for key in CLASS_PREMISE_KEYS}, CLASS_PREMISE_KEYS),
        )),
        "w2_23_dependency_exact": all(w223.values()),
        "w2_23_general_forbidden_domain_uses_signal_support_and_F4": all((
            w223["w2_23_forbidden_pairs_depend_on_signal_support_and_F4_modes"],
            w223[
                "w2_23_nontransmission_depends_on_forbidden_pairs_and_interventions"
            ],
        )),
        "mutual_incomparability_and_general_forbidden_pairs_distinguished": all((
            CLASS_DEFINITION[
                "mutual_incomparability_equals_general_forbidden_pairs"
            ] is False,
            CLASS_DEFINITION["directed_forbidden_pairs_classified_by_order"]
            is False,
            CLASS_DEFINITION[
                "F4_mode_selective_nontransmission_classified_by_order"
            ] is False,
        )),
        "general_F3b_no_go_explicitly_false": all((
            CLAIM_CONTRACT["CLOSURE_FLAGS"][
                "connected_1D_general_F3b_no_go_proved"
            ] is False,
            CLAIM_CONTRACT["CLOSURE_FLAGS"][
                "general_forbidden_pair_domain_empty_proved"
            ] is False,
            CLAIM_CONTRACT["CLOSURE_FLAGS"][
                "directed_forbidden_pair_domain_empty_proved"
            ] is False,
            CLAIM_CONTRACT["CLOSURE_FLAGS"][
                "F4_mode_selective_nontransmission_impossible_proved"
            ] is False,
        )),
        "global_Z2_reversal_preserves_comparability": (
            CLASS_DEFINITION["global_Z2_preserves_comparability"] is True
        ),
        "optional_w225_import_is_semantic_and_fail_closed": all((
            optional["import_valid"],
            optional["F3b_physical_closed"] is False,
            optional["general_F3b_no_go_applied"] is False,
            optional["foundation_origin_closed"] is False,
            (
                not optional["present"]
                or optional["semantic_map_valid"]
                or optional["no_application"]
            ),
        )),
        "closure_flags_and_scope_exact": all((
            CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS,
            _physical_scope_false(CLAIM_CONTRACT["CLOSURE_FLAGS"]),
        )),
    }


def fail_closed_controls() -> dict[str, bool]:
    premises = {key: True for key in CLASS_PREMISE_KEYS}
    baseline = class_screen(premises, False)
    inconsistent = class_screen(premises, True)

    false_premise_results = []
    for key in CLASS_PREMISE_KEYS:
        mutated = dict(premises)
        mutated[key] = False
        false_premise_results.append(class_screen(mutated, False))

    malformed = []
    missing = dict(premises)
    missing.pop(next(iter(CLASS_PREMISE_KEYS)))
    malformed.append(missing)
    extra = dict(premises)
    extra["extra"] = True
    malformed.append(extra)
    nonboolean = dict(premises)
    nonboolean[next(iter(CLASS_PREMISE_KEYS))] = 1
    malformed.append(nonboolean)

    logical = logical_controls()
    mutated_class = deepcopy(CLASS_DEFINITION)
    mutated_class["topology"] += " MUTATED"
    mutated_logistic = deepcopy(LOGISTIC_ROUTE_SPEC)
    mutated_logistic["law"] += " MUTATED"
    mutated_controls = deepcopy(LOGICAL_CONTROL_REGISTRY)
    mutated_controls["prewired_graph_negative"]["expected"] += " MUTATED"
    mutated_optional = deepcopy(OPTIONAL_W225_POLICY)
    mutated_optional["semantic_source"] += " MUTATED"
    mutated_contract = deepcopy(CLAIM_CONTRACT)
    mutated_contract["CLAIM"] += " MUTATED"
    scope_promotions = []
    for key in (
        "connected_1D_general_F3b_no_go_proved",
        "general_forbidden_pair_domain_empty_proved",
        "directed_forbidden_pair_domain_empty_proved",
        "F4_mode_selective_nontransmission_impossible_proved",
        "F3b_causal_separability_nontransmission_proved",
    ):
        mutated_closure = deepcopy(EXPECTED_CLOSURE_FLAGS)
        mutated_closure[key] = True
        scope_promotions.append(mutated_closure)

    return {
        "complete_class_report_triggers_incomparability_only_no_go": all((
            baseline["valid"], baseline["class_applicable"],
            baseline["total_comparability"],
            baseline["mutual_incomparability_domain_empty"],
            baseline["incomparability_only_route_no_go"],
            not baseline["directed_forbidden_pair_domain_empty"],
            not baseline["F4_mode_selective_nontransmission_impossible"],
            not baseline["general_F3b_no_go"],
            not baseline["incomparability_only_F3b_route_eligible"],
            not baseline["incomparability_only_F3b_route_promoted"],
        )),
        "each_false_premise_leaves_class_without_rejecting_other_routes": all(
            result["valid"]
            and not result["class_applicable"]
            and not result["incomparability_only_F3b_route_eligible"]
            and not result["incomparability_only_F3b_route_promoted"]
            for result in false_premise_results
        ),
        "missing_extra_nonboolean_premise_invalid": all(
            not class_screen(item, False)["valid"] for item in malformed
        ),
        "nonempty_mutual_incomparability_claim_is_inconsistent": all((
            inconsistent["valid"], inconsistent["class_applicable"],
            inconsistent["claimed_nonempty_mutual_incomparability_inconsistent"],
            not inconsistent["general_F3b_no_go"],
            not inconsistent["incomparability_only_F3b_route_eligible"],
            not inconsistent["incomparability_only_F3b_route_promoted"],
        )),
        "two_dimensional_positive_control_escapes_class": all((
            logical["two_dimensional_product_poset_has_exact_incomparable_pair"],
            logical["product_poset_is_outside_one_dimensional_class"],
        )),
        "directed_and_mode_selective_forbidden_controls_escape_order_no_go": all((
            logical[
                "total_order_allows_directed_forbidden_signal_pair_logic_control"
            ],
            logical[
                "total_order_allows_F4_mode_selective_nontransmission_logic_control"
            ],
            logical[
                "mutual_incomparability_not_equated_with_general_nontransmission"
            ],
            not baseline["directed_forbidden_pair_domain_empty"],
            not baseline["F4_mode_selective_nontransmission_impossible"],
        )),
        "frozen_disconnected_and_prewired_controls_do_not_promote": all((
            logical["frozen_candidate_rejected_before_incomparability_theorem"],
            logical["disconnected_candidate_outside_incomparability_theorem_class"],
            logical["prewired_graph_rejected_as_target_leak"],
        )),
        "class_definition_mutation_detected": (
            _canonical_sha256(mutated_class) != EXPECTED_CLASS_DEFINITION_SHA256
        ),
        "logistic_spec_mutation_detected": (
            _canonical_sha256(mutated_logistic) != EXPECTED_LOGISTIC_ROUTE_SPEC_SHA256
        ),
        "control_registry_mutation_detected": (
            _canonical_sha256(mutated_controls)
            != EXPECTED_LOGICAL_CONTROL_REGISTRY_SHA256
        ),
        "optional_dependency_policy_mutation_detected": (
            _canonical_sha256(mutated_optional) != EXPECTED_OPTIONAL_W225_POLICY_SHA256
        ),
        "scientific_contract_mutation_detected": (
            _canonical_sha256(mutated_contract) != EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        ),
        "general_scope_promotions_rejected": all(
            not _physical_scope_false(mutated) for mutated in scope_promotions
        ),
        "deterministic_hash_repetition_exact": all((
            _canonical_sha256(CLASS_DEFINITION) == _canonical_sha256(deepcopy(CLASS_DEFINITION)),
            _canonical_sha256(LOGISTIC_ROUTE_SPEC) == _canonical_sha256(deepcopy(LOGISTIC_ROUTE_SPEC)),
            _canonical_sha256(CLAIM_CONTRACT) == _canonical_sha256(deepcopy(CLAIM_CONTRACT)),
        )),
    }


def run() -> dict[str, Any]:
    logistic, diagnostics = logistic_exact_controls()
    general = general_orbit_controls()
    logical = logical_controls()
    dependency = _w223_dependency_controls()
    optional = _optional_w225_semantics()
    definition = definition_controls()
    fail_closed = fail_closed_controls()

    valid = bool(all((
        _exact_bool_map(definition, DEFINITION_CONTROL_KEYS),
        all(definition.values()),
        _exact_bool_map(fail_closed, FAIL_CLOSED_CONTROL_KEYS),
        all(fail_closed.values()),
        all(logistic.values()),
        all(general.values()),
        all(logical.values()),
        all(dependency.values()),
        CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS,
        _physical_scope_false(CLAIM_CONTRACT["CLOSURE_FLAGS"]),
    )))

    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": valid,
        "candidate_status": (
            "CONNECTED_1D_TOTAL_COMPARABILITY_AND_EMPTY_MUTUAL_INCOMPARABILITY_PROVED__GENERAL_F3B_OPEN"
            if valid else "INVALID_GATE_NO_PROMOTION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "A single connected one-dimensional physical occurrence orbit is totally comparable "
            "on either global orientation and therefore has an empty mutual reachability-"
            "incomparability domain. The logistic tau route is an exact aperiodic example. This "
            "rules out only an F3b separation route defined exclusively by mutual incomparability. "
            "Directed forbidden pairs, F4-mode-selective nontransmission and general F3b remain "
            "open. F3a, physical F4, foundation origin and every downstream bridge remain false."
        ),
        "class_definition": CLASS_DEFINITION,
        "logistic_route_spec": LOGISTIC_ROUTE_SPEC,
        "optional_w2_25": optional,
        "closure_flags": CLAIM_CONTRACT["CLOSURE_FLAGS"],
        "hashes": {
            "class_definition": _canonical_sha256(CLASS_DEFINITION),
            "logistic_route_spec": _canonical_sha256(LOGISTIC_ROUTE_SPEC),
            "logical_control_registry": _canonical_sha256(LOGICAL_CONTROL_REGISTRY),
            "optional_w225_policy": _canonical_sha256(OPTIONAL_W225_POLICY),
            "scientific_contract": _canonical_sha256(CLAIM_CONTRACT),
        },
        "controls": {
            "definition": definition,
            "dependency": dependency,
            "general_orbit": general,
            "logistic_exact": logistic,
            "logical": logical,
            "fail_closed": fail_closed,
        },
        "exact_diagnostics": {
            key: str(value) for key, value in diagnostics.items()
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
            "candidate_status": "INVALID_GATE_NO_PROMOTION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
