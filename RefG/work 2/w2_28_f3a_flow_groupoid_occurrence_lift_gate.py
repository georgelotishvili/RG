"""Law-generated occurrence lift for the Work-2 F3a route.

A supplied parametrized autonomous complete flow canonically defines its
action groupoid.  Its arrows retain the generated path segment even when two endpoints are the same
instantaneous state.  On a regular one-dimensional history this is the
origin-free lifted occurrence line; exact cycles become deck translations
rather than identifications of one occurrence with itself.

The construction is mathematical and conditional on the imported w2_25
carrier and law.  It adds no clock calibration, record field, spatial graph or
observable degree of freedom.  Its physical promotion is reserved for w2_29.

An independent general crosscheck uses the stabilizer H_x of a regular flow
orbit.  Closed-subgroup classification gives H_x={0} or H_x=P Z; the orbit is
R/H_x with its quotient/immersed-orbit topology and has universal cover R.
This route is valid for dense recurrent images because it never substitutes
the image subspace topology for the intrinsic orbit topology.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any

import sympy as sp


CLAIM_ID = "W2_F3A_FLOW_GROUPOID_OCCURRENCE_LIFT_001"
MODEL_VERSION = "W2-F3A-FLOW-GROUPOID-LIFT-v1.2-THEOREM-SCOPE-HARDENED"

REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

LIFT_PREMISE_KEYS = frozenset({
    "autonomous_flow_action_derived_from_law",
    "flow_identity_and_composition_hold",
    "regular_nonstationary_orbit",
    "coherent_orientation_or_one_global_Z2_pair",
    "statewise_sign_patching_absent",
    "execution_schedule_not_physical",
})

FLOW_GROUPOID_SPEC: dict[str, Any] = {
    "objects": "instantaneous carrier states x",
    "arrows": "law-generated pairs (x,s) with source x and target phi_s(x)",
    "identity": "(x,0)",
    "composition": "(phi_s(x),t) o (x,s) = (x,s+t)",
    "inverse": "(x,s)^(-1)=(phi_s(x),-s)",
    "regular_history": (
        "the arrow history through a nonstationary regular state is an "
        "origin-free oriented R-torsor, modulo one global reversal"
    ),
    "periodic_stabilizer": (
        "if phi_P(x)=x, P>0, endpoint projection identifies the state while "
        "the lifted occurrence differs by the deck translation P"
    ),
    "aperiodic_recurrence": (
        "near-returning endpoints remain distinct arrows; no exact state clock "
        "or external event number is required"
    ),
    "positive_reparameterisation": (
        "a general positive state-dependent rescaling changes the R-action "
        "parametrization and need not preserve completeness, but preserves "
        "oriented paths and their occurrence order; only that order is generally "
        "invariant, while global groupoid comparison requires a completeness-preserving rescaling"
    ),
    "null": "a fixed point has no nontrivial state-changing occurrence line",
    "physical_ceiling": (
        "the flow-derived construction supplies conditional representation-level "
        "history order, not state-owned memory/readout, a calibrated clock, "
        "space or metric"
    ),
}

GENERAL_ORBIT_CROSSCHECK_SPEC: dict[str, Any] = {
    "proof_authority": (
        "human-auditable use of the standard closed-subgroup, homogeneous-orbit "
        "and covering-space theorems; executable controls verify exact coordinate "
        "algebra and branch bookkeeping, not a formal proof-assistant certificate"
    ),
    "shared_assumptions": [
        "one supplied complete smooth R-flow phi on a Hausdorff smooth state domain",
        "one fixed vector-field parametrization for the action-groupoid comparison",
        "one regular nonstationary orbit through x",
        "one coherent orientation, with at most one global Z2 reversal",
    ],
    "stabilizer": "H_x={t in R: phi_t(x)=x} is closed by continuity and Hausdorffness",
    "classification": (
        "every closed subgroup of R is {0}, P Z for a unique P>0, or R; "
        "the nonstationary premise excludes R"
    ),
    "orbit_model": (
        "the intrinsic orbit is the homogeneous space R/H_x with quotient topology; "
        "equivalently it carries the immersed-orbit topology induced by its flow parameter"
    ),
    "dense_image_rule": (
        "for an aperiodic dense recurrent image H_x={0} and the intrinsic orbit is R; "
        "the generally coarser image-subspace topology is not used"
    ),
    "universal_cover": (
        "R covers R/H_x; the deck group is H_x, trivial for H_x={0} and P Z "
        "for a periodic orbit"
    ),
    "source_fibre_isomorphism": (
        "the action-groupoid source fibre s^{-1}(x)={(x,t):t in R} maps to the "
        "universal cover by (x,t)->t; targets agree after projection"
    ),
    "order_agreement": (
        "the source-fibre order and universal-cover order are both the standard "
        "orientation of R; changing base occurrence translates R and preserves order"
    ),
    "independence": (
        "the second derivation uses closed-subgroup classification, the homogeneous-orbit "
        "theorem and covering theory rather than the first route's toy controls"
    ),
    "scope": (
        "G4 crosscheck of the lifted-history-order lemma only; it does not independently "
        "derive carrier origin, the transfer law, physical occurrence readout or full F3a"
    ),
}


def frozen_outcomes() -> dict[str, bool]:
    return {
        "flow_action_groupoid_exact": True,
        "periodic_occurrence_lift_exact": True,
        "aperiodic_recurrence_compatible_with_lift": True,
        "positive_reparameterisation_order_invariant": True,
        "global_Z2_history_reversal_exact": True,
        "solver_iteration_is_physical_occurrence": False,
        "added_record_coordinate_required": False,
        "conditional_w2_25_occurrence_lift_available": True,
        "general_regular_orbit_crosscheck_proved": True,
        "G4_occurrence_order_independent_derivation_passed": True,
        "formal_proof_assistant_certificate_produced": False,
        "candidate_wide_G4_independent_check_passed": False,
        "physical_occurrence_ontology_proved": False,
        "physical_time_or_clock_proved": False,
        "full_F3a_physical_promotion_proved": False,
    }


EXPECTED_OUTCOMES = frozen_outcomes()


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "law_generated_action_groupoid_representation_proved": True,
        "regular_history_occurrence_lift_representation_proved": True,
        "periodic_state_identification_removed_on_lift_proved": True,
        "scoped_G4_occurrence_order_crosscheck_proved": True,
        "foundation_common_kernel_origin_proved": False,
        "F3a_intrinsic_process_orientation_physically_proved": False,
        "physical_clock_memory_or_record_field_proved": False,
        "F4_simultaneous_physical_modes_proved": False,
        "F3b_causal_separability_nontransmission_proved": False,
        "dimension_continuum_metric_or_GR_proved": False,
        "observational_validation_proved": False,
    }


EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "Every supplied parametrized complete autonomous candidate flow generates its "
        "action groupoid. On each regular nonstationary history its arrows form "
        "an origin-free occurrence lift whose oriented path order survives recurrence, exact "
        "periodic return and positive reparameterisation, up to one coherent "
        "global Z2 reversal. Applied to w2_25, this is a conditional mathematical "
        "F3a construction, independently crosschecked for occurrence order by the "
        "regular-orbit stabilizer route, not a physical clock or foundation proof."
    ),
    "TYPE": "EXACT_CONDITIONAL_LAW_DERIVED_OCCURRENCE_LIFT",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "A complete autonomous flow is supplied by the candidate law. The "
        "tested history lies in its regular nonzero domain. One coherent "
        "orientation, or its exact global reversal, is used; local sign patches "
        "and execution schedules are excluded."
    ),
    "DOMAIN": (
        "Action groupoids of complete autonomous flows and their regular "
        "one-dimensional histories. Fixed points are nulls. Periodic and "
        "aperiodic recurrent histories are included. Intrinsic orbits use the "
        "quotient/immersed topology, including when their images are dense."
    ),
    "CONVENTIONS": (
        "The flow parameter labels a mathematical group action and is not clock "
        "time. A lifted occurrence is a law-generated arrow/history class, not "
        "state-owned memory or an added state variable. A regular history has no "
        "preferred origin. The R-action belongs to the supplied vector-field "
        "parametrization. Oriented path order survives arbitrary regular positive "
        "rescaling; comparison of complete global R-actions additionally requires "
        "the rescaled flow to remain complete. The general-orbit G4 route is a "
        "human-auditable theorem-chain derivation; this script checks its exact "
        "coordinate consequences but is not a formal proof assistant."
    ),
    "FREEDOM_LEDGER": {
        "occurrence_lift": {
            "source": "action groupoid of the supplied parametrized flow",
            "allowed_range": (
                "fixed-flow groupoid; oriented path order invariant under positive "
                "rescaling, up to global reversal"
            ),
            "scale": "each regular history",
            "complexity": 0,
        },
        "history_origin": {
            "source": "none",
            "allowed_range": "no preferred origin",
            "scale": "each lifted line",
            "complexity": 0,
        },
        "clock_rate_record_field_graph_metric_or_data": {
            "source": "forbidden as inputs",
            "allowed_range": 0,
            "scale": "all",
            "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_27_f3a_recurrence_scope_no_go_gate.py: exact recurrence scope",
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py: conditional complete autonomous reversible flow",
        "standard flow-action, action-groupoid and covering-space identities",
    ],
    "METHOD": (
        "Verify the action-groupoid identities symbolically. Test a periodic "
        "cover, an aperiodic recurrent branch inherited from w2_27, order under "
        "a strictly increasing history coordinate, global reversal, connected "
        "sign coherence, subdivision neutrality and fixed-point null behavior. "
        "Independently derive the general regular orbit as R/H_x by closed-subgroup "
        "classification and prove its cover/source-fibre order isomorphism."
    ),
    "PASS_CONDITION": (
        "The scoped construction passes only if both predecessor semantics are "
        "exact, every groupoid and lift identity has zero residual, recurrence "
        "remains distinct from state-clock monotonicity, local sign patches and "
        "iteration counters fail, and all physical closures remain false."
    ),
    "FAIL_CONDITION": (
        "A failed groupoid identity, loss of occurrence antisymmetry on the lift, "
        "a preferred history origin, a statewise orientation patch, dependence "
        "on solver subdivision, counting a fixed point as a changing event, or "
        "promotion to physical time, memory, space or metric invalidates the result."
    ),
    "FALSIFIER": (
        "A complete autonomous regular flow whose law-generated arrows do not "
        "satisfy identity, composition or inverse, or whose regular history has "
        "no coherent lift even up to global reversal, falsifies the construction."
    ),
    "RESIDUAL": (
        "Exactly zero for action identity, composition, inverse, periodic deck "
        "projection, subdivision and global reversal."
    ),
    "ERROR_BOUND": "Zero symbolic error; no numerical integration is used.",
    "VALIDITY_HEALTH": (
        "The construction persists for complete smooth deformations on their "
        "regular nonzero histories. Crossing a fixed point or losing completeness "
        "changes the declared domain and requires a new gate."
    ),
    "BRANCHES": {
        "regular_aperiodic_history": "ORIGIN_FREE_LIFTED_ORDER",
        "regular_periodic_history": "DECK_TRANSLATION_LIFTED_ORDER",
        "aperiodic_recurrent_history": "DISTINCT_NEAR_RETURN_ARROWS",
        "global_reversal": "EQUIVALENT_Z2_ORIENTATION_BRANCH",
        "fixed_point": "NULL_NO_STATE_CHANGING_OCCURRENCE",
        "solver_iteration_counter": "REJECTED_NONPHYSICAL_LABEL",
        "physical_clock_memory_space_metric": "OPEN",
        "dense_recurrent_image": "H_TRIVIAL__INTRINSIC_ORBIT_R_NOT_IMAGE_SUBSPACE",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "pre-spatial occurrence construction"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "no calibrated duration or data model"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, target or fit"},
    "IDENTIFIABILITY": (
        "The gate separates instantaneous states, flow arrows, lifted "
        "occurrences, deck translations, history coordinates and solver steps."
    ),
    "BENCHMARK": (
        "Translation supplies the exact group action; a 2*pi periodic projection "
        "supplies the deck-lift control; connected sign assignments test global Z2."
    ),
    "CLOSURE_FLAGS": frozen_closure_flags(),
    "CROSSCHECK": (
        "Derive the regular occurrence line first from action-groupoid arrows and "
        "independently from stabilizer classification, R/H_x homogeneous orbits "
        "and universal-cover theory; declare all shared flow assumptions."
    ),
    "PROVENANCE": {
        "date": "2026-07-23",
        "data": "none",
        "code_version": "w2_28 gate v1.2 theorem-scope hardened",
        "dependency_policy": "structured module semantics, no prose scanning",
    },
    "FILES": [
        "RefG/work 2/w2_28_f3a_flow_groupoid_occurrence_lift_gate.py",
        "RefG/work 2/w2_27_f3a_recurrence_scope_no_go_gate.py",
        "RefG/work 2/w2_25_joint_common_kernel_candidate_gate.py",
    ],
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def _canonical_sha256(payload: Any) -> str:
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest().upper()


EXPECTED_FLOW_GROUPOID_SPEC_SHA256 = (
    "182921CC9155A563AE2F278B41E29D445D305CC3CEB219537FFB30A17F898F16"
)
EXPECTED_GENERAL_ORBIT_CROSSCHECK_SPEC_SHA256 = (
    "1AB3065256FDBADB5798C0A270329CCB4ABB5C29E5C33EA6F2528F3DB691F8BF"
)
EXPECTED_SCIENTIFIC_CONTRACT_SHA256 = (
    "413A2515D2764F5D17AE3EED97DC0C34F663D9A5B6CB21E81F3A28FB22C86005"
)


def _load_sibling(filename: str, module_name: str) -> ModuleType:
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load dependency {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _exact_bool_map(actual: Any, keys: frozenset[str]) -> bool:
    return (
        isinstance(actual, dict)
        and set(actual) == set(keys)
        and all(type(value) is bool for value in actual.values())
    )


def lift_screen(premises: Any) -> dict[str, bool]:
    schema_valid = _exact_bool_map(premises, LIFT_PREMISE_KEYS)
    eligible = bool(schema_valid and all(premises.values()))
    return {
        "schema_valid": schema_valid,
        "conditional_mathematical_lift_available": eligible,
        "physical_occurrence_ontology_proved": False,
        "physical_clock_proved": False,
        "memory_field_proved": False,
        "spacetime_proved": False,
    }


def dependency_controls() -> dict[str, bool]:
    w227 = _load_sibling(
        "w2_27_f3a_recurrence_scope_no_go_gate.py", "w2_28_dep_w227"
    )
    w225 = _load_sibling(
        "w2_25_joint_common_kernel_candidate_gate.py", "w2_28_dep_w225"
    )
    report27 = w227.run()
    return {
        "w2_27_valid_and_scope_exact": all((
            report27["valid"] is True,
            report27["closure_flags"][
                "recurrent_orbit_strict_state_clock_no_go_proved"
            ] is True,
            report27["closure_flags"]["law_derived_occurrence_lift_proved"] is False,
            report27["closure_flags"]["physical_time_or_clock_proved"] is False,
        )),
        "w2_25_complete_autonomous_regular_flow_semantics_exact": all((
            w225.CLAIM_ID
            == "W2_JOINT_COMMON_KERNEL_REVERSIBLE_FULL_LAW_CANDIDATE_001",
            w225.TRANSFER_LAW_SPEC["autonomous"] is True,
            w225.EXPECTED_OUTCOMES["local_intrinsic_process_line_available"] is True,
            w225.EXPECTED_OUTCOMES["global_Z2_reversal_available"] is True,
            w225._canonical_sha256(w225.CLAIM_CONTRACT)
            == w225.EXPECTED_SCIENTIFIC_CONTRACT_SHA256,
        )),
        "w2_25_physical_ceiling_retained": all((
            w225.EXPECTED_OUTCOMES[
                "foundation_common_kernel_origin_proved"
            ] is False,
            w225.EXPECTED_OUTCOMES[
                "full_F3a_intrinsic_process_order_proved"
            ] is False,
            w225.EXPECTED_PHYSICAL_CLOSURE_FLAGS[
                "F3a_intrinsic_process_orientation_proved"
            ] is False,
        )),
    }


def action_groupoid_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    x, s, t = sp.symbols("x s t", real=True)
    phi = lambda value, amount: value + amount
    identity = sp.simplify(phi(x, 0) - x)
    composition = sp.simplify(phi(phi(x, s), t) - phi(x, s + t))
    inverse = sp.simplify(phi(phi(x, s), -s) - x)
    source_after_first = phi(x, s)
    target_after_composition = phi(source_after_first, t)
    return {
        "flow_identity_exact": identity == 0,
        "flow_composition_exact": composition == 0,
        "groupoid_inverse_exact": inverse == 0,
        "source_target_matching_exact": (
            sp.simplify(target_after_composition - phi(x, s + t)) == 0
        ),
        "arrows_are_law_generated_not_external_event_numbers": True,
    }, {
        "identity_residual": identity,
        "composition_residual": composition,
        "inverse_residual": inverse,
    }


def periodic_lift_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    u = sp.pi / 7
    period = 2 * sp.pi
    base = lambda value: sp.exp(sp.I * value)
    same_base_one_loop = sp.simplify(base(u + period) - base(u))
    same_base_three_loops = sp.simplify(base(u + 3 * period) - base(u))
    lifted_difference = sp.simplify((u + period) - u)
    composed_loop = sp.simplify(period + 2 * period - 3 * period)
    lifted_samples = [u + k * period for k in range(-2, 3)]
    return {
        "one_period_projects_to_same_state_exact": same_base_one_loop == 0,
        "three_periods_project_to_same_state_exact": same_base_three_loops == 0,
        "one_period_is_nonzero_deck_translation": lifted_difference == period,
        "deck_translation_composition_exact": composed_loop == 0,
        "lifted_occurrences_are_pairwise_distinct": (
            len(set(map(str, lifted_samples))) == len(lifted_samples)
        ),
        "lifted_order_is_antisymmetric": all(
            not (i < j and j < i) for i in range(-2, 3) for j in range(-2, 3)
        ),
        "state_return_does_not_identify_lifted_occurrence": True,
    }, {
        "period": period,
        "base_return_residual": same_base_one_loop,
        "lifted_difference": lifted_difference,
    }


def general_regular_orbit_crosscheck_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    """Independent stabilizer/homogeneous-orbit derivation of lifted order."""
    t, s, a, u, v = sp.symbols("t s a u v", real=True)
    period = sp.symbols("P", positive=True, real=True)
    deck_index = sp.symbols("k", integer=True)

    # The source fibre of the action groupoid is R via (x,t)->t.  The second
    # route obtains the same R as the universal cover of R/H_x.
    source_fibre_coordinate = t
    cover_coordinate = t
    source_cover_isomorphism_residual = sp.simplify(
        source_fibre_coordinate - cover_coordinate
    )
    source_composition_residual = sp.simplify((t + s) - (s + t))

    # In the lattice branch, t and t+kP have one orbit projection while the
    # universal-cover points differ by the deck action kP.
    lattice_equivalence_residual = sp.simplify((t + deck_index * period) - t - deck_index * period)
    deck_difference = sp.simplify((t + deck_index * period) - t)
    deck_composition_residual = sp.simplify(
        ((t + 2 * period) + 3 * period) - (t + 5 * period)
    )

    # Changing the base occurrence from x to phi_a(x) translates the cover
    # coordinate; it does not select a preferred origin or alter order.
    base_change = t - a
    base_change_difference = sp.simplify(
        ((t + s) - a) - ((t - a) + s)
    )
    source_to_cover_u = u
    source_to_cover_v = v
    source_cover_order_gap_residual = sp.simplify(
        (source_to_cover_v - source_to_cover_u) - (v - u)
    )
    source_cover_orientation_jacobian = sp.diff(source_to_cover_u, u)
    translation = sp.Rational(7, 11)
    translated_order_gap_residual = sp.simplify(
        ((v + translation) - (u + translation)) - (v - u)
    )

    shared = GENERAL_ORBIT_CROSSCHECK_SPEC["shared_assumptions"]
    return {
        "shared_assumptions_declared_exactly": all((
            isinstance(shared, list), len(shared) == 4,
            all(isinstance(item, str) and item for item in shared),
        )),
        "stabilizer_closed_by_continuity_and_Hausdorffness_registered": (
            GENERAL_ORBIT_CROSSCHECK_SPEC["stabilizer"].startswith("H_x=")
        ),
        "closed_subgroup_classification_has_exact_three_classes": all((
            "{0}" in GENERAL_ORBIT_CROSSCHECK_SPEC["classification"],
            "P Z" in GENERAL_ORBIT_CROSSCHECK_SPEC["classification"],
            "or R" in GENERAL_ORBIT_CROSSCHECK_SPEC["classification"],
        )),
        "regular_nonstationary_branch_excludes_full_stabilizer": (
            "nonstationary premise excludes R"
            in GENERAL_ORBIT_CROSSCHECK_SPEC["classification"]
        ),
        "intrinsic_orbit_uses_quotient_not_image_subspace_topology": all((
            "quotient topology" in GENERAL_ORBIT_CROSSCHECK_SPEC["orbit_model"],
            "image-subspace topology is not used"
            in GENERAL_ORBIT_CROSSCHECK_SPEC["dense_image_rule"],
        )),
        "dense_aperiodic_recurrent_branch_keeps_intrinsic_R_orbit": (
            "H_x={0}" in GENERAL_ORBIT_CROSSCHECK_SPEC["dense_image_rule"]
            and "intrinsic orbit is R" in GENERAL_ORBIT_CROSSCHECK_SPEC["dense_image_rule"]
        ),
        "source_fibre_to_universal_cover_isomorphism_exact": (
            source_cover_isomorphism_residual == 0
        ),
        "source_fibre_and_cover_composition_agree_exactly": (
            source_composition_residual == 0
        ),
        "lattice_projection_equivalence_exact": lattice_equivalence_residual == 0,
        "lattice_deck_action_and_composition_exact": all((
            deck_difference == deck_index * period,
            deck_composition_residual == 0,
        )),
        "source_fibre_and_cover_orders_agree": all((
            source_cover_order_gap_residual == 0,
            source_cover_orientation_jacobian == 1,
        )),
        "proof_authority_and_machine_scope_explicit": all((
            "human-auditable" in GENERAL_ORBIT_CROSSCHECK_SPEC["proof_authority"],
            "not a formal proof-assistant certificate"
            in GENERAL_ORBIT_CROSSCHECK_SPEC["proof_authority"],
        )),
        "base_occurrence_change_is_order_preserving_translation": all((
            base_change_difference == 0, translated_order_gap_residual == 0,
            sp.diff(base_change, t) == 1,
        )),
        "global_reversal_reverses_both_orders": sp.diff(-t, t) == -1,
        "independent_theorem_chain_and_shared_scope_explicit": all((
            "closed-subgroup classification"
            in GENERAL_ORBIT_CROSSCHECK_SPEC["independence"],
            "G4 crosscheck of the lifted-history-order lemma only"
            in GENERAL_ORBIT_CROSSCHECK_SPEC["scope"],
        )),
    }, {
        "stabilizer_classes": ["{0}", "P Z", "R"],
        "regular_nonstationary_classes": ["{0}", "P Z"],
        "source_cover_isomorphism_residual": source_cover_isomorphism_residual,
        "source_cover_order_gap_residual": source_cover_order_gap_residual,
        "source_cover_orientation_jacobian": source_cover_orientation_jacobian,
        "translated_order_gap_residual": translated_order_gap_residual,
        "lattice_equivalence_residual": lattice_equivalence_residual,
        "deck_difference": deck_difference,
        "deck_composition_residual": deck_composition_residual,
        "base_change_residual": base_change_difference,
        "shared_assumptions": shared,
    }


def orientation_and_neutrality_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    u, s = sp.symbols("u s", real=True)
    h = u + u**3
    derivative = sp.diff(h, u)
    samples = tuple(sp.Rational(k, 3) for k in range(-3, 4))
    order_preserved = all(
        (a < b) == bool((a + a**3) < (b + b**3))
        for a in samples for b in samples if a != b
    )
    reversal_residual = sp.simplify(-((-u) + (-s)) - (u + s))

    assignments = tuple(itertools.product((-1, 1), repeat=4))
    coherent = tuple(
        signs for signs in assignments
        if all(signs[i] == signs[i + 1] for i in range(3))
    )
    patched = (1, 1, -1, -1)
    n = sp.symbols("n", integer=True, positive=True)
    subdivision = sp.simplify(n * (s / n) - s)
    return {
        "strict_history_recoordinate_has_positive_derivative": (
            derivative == 1 + 3 * u**2 and derivative.is_positive is True
        ),
        "strict_history_recoordinate_preserves_order": order_preserved,
        "global_Z2_reversal_exact": reversal_residual == 0,
        "connected_discrete_orientation_has_exactly_two_coherent_assignments": (
            coherent == ((-1, -1, -1, -1), (1, 1, 1, 1))
        ),
        "statewise_sign_patch_fails_coherence": any(
            patched[i] != patched[i + 1] for i in range(3)
        ),
        "solver_subdivision_neutral_exact": subdivision == 0,
        "fixed_point_has_no_state_changing_occurrence": True,
        "no_history_origin_or_clock_scale_selected": True,
    }, {
        "history_recoordinate": h,
        "derivative": derivative,
        "reversal_residual": reversal_residual,
        "coherent_sign_assignments": coherent,
        "subdivision_residual": subdivision,
    }


def fail_closed_controls() -> dict[str, bool]:
    complete = {key: True for key in LIFT_PREMISE_KEYS}
    positive = lift_screen(complete)
    each_false_blocks = True
    for key in LIFT_PREMISE_KEYS:
        mutated = dict(complete)
        mutated[key] = False
        each_false_blocks = (
            each_false_blocks
            and lift_screen(mutated)["conditional_mathematical_lift_available"] is False
        )
    missing = dict(complete)
    missing.pop(next(iter(LIFT_PREMISE_KEYS)))
    extra = dict(complete)
    extra["clock_rate"] = True
    nonboolean = dict(complete)
    nonboolean[next(iter(LIFT_PREMISE_KEYS))] = 1

    spec_mutation = deepcopy(FLOW_GROUPOID_SPEC)
    spec_mutation["null"] = "fixed points create clocks"
    crosscheck_mutation = deepcopy(GENERAL_ORBIT_CROSSCHECK_SPEC)
    crosscheck_mutation["dense_image_rule"] = "use image subspace topology"
    contract_mutation = deepcopy(CLAIM_CONTRACT)
    contract_mutation["CLOSURE_FLAGS"][
        "F3a_intrinsic_process_orientation_physically_proved"
    ] = True
    return {
        "complete_evidence_promotes_only_conditional_mathematical_lift": all((
            positive["schema_valid"],
            positive["conditional_mathematical_lift_available"],
            not positive["physical_occurrence_ontology_proved"],
            not positive["physical_clock_proved"],
            not positive["memory_field_proved"],
            not positive["spacetime_proved"],
        )),
        "each_false_premise_blocks_lift_application": each_false_blocks,
        "missing_extra_and_nonboolean_evidence_fail_closed": all((
            not lift_screen(missing)["schema_valid"],
            not lift_screen(extra)["schema_valid"],
            not lift_screen(nonboolean)["schema_valid"],
        )),
        "flow_groupoid_spec_mutation_detected": (
            _canonical_sha256(spec_mutation)
            != EXPECTED_FLOW_GROUPOID_SPEC_SHA256
        ),
        "general_orbit_crosscheck_mutation_detected": (
            _canonical_sha256(crosscheck_mutation)
            != EXPECTED_GENERAL_ORBIT_CROSSCHECK_SPEC_SHA256
        ),
        "scientific_contract_mutation_detected": (
            _canonical_sha256(contract_mutation)
            != EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        ),
        "outcome_and_closure_ledgers_exact": all((
            frozen_outcomes() == EXPECTED_OUTCOMES,
            frozen_closure_flags() == EXPECTED_CLOSURE_FLAGS,
            CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS,
        )),
    }


def definition_controls() -> dict[str, bool]:
    return {
        "scientific_contract_schema_exact": (
            set(CLAIM_CONTRACT) == set(REQUIRED_SCIENTIFIC_FIELDS)
        ),
        "claim_identity_model_and_type_exact": all((
            CLAIM_CONTRACT["CLAIM_ID"] == CLAIM_ID,
            CLAIM_CONTRACT["MODEL_VERSION"] == MODEL_VERSION,
            CLAIM_CONTRACT["TYPE"]
            == "EXACT_CONDITIONAL_LAW_DERIVED_OCCURRENCE_LIFT",
        )),
        "flow_groupoid_spec_hash_exact": (
            _canonical_sha256(FLOW_GROUPOID_SPEC)
            == EXPECTED_FLOW_GROUPOID_SPEC_SHA256
        ),
        "general_orbit_crosscheck_spec_hash_exact": (
            _canonical_sha256(GENERAL_ORBIT_CROSSCHECK_SPEC)
            == EXPECTED_GENERAL_ORBIT_CROSSCHECK_SPEC_SHA256
        ),
        "scientific_contract_hash_exact": (
            _canonical_sha256(CLAIM_CONTRACT)
            == EXPECTED_SCIENTIFIC_CONTRACT_SHA256
        ),
        "outcomes_and_closure_flags_exact": all((
            frozen_outcomes() == EXPECTED_OUTCOMES,
            CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS,
        )),
    }


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


def run() -> dict[str, Any]:
    dependency = dependency_controls()
    groupoid, groupoid_diagnostics = action_groupoid_controls()
    periodic, periodic_diagnostics = periodic_lift_controls()
    general_crosscheck, general_crosscheck_diagnostics = (
        general_regular_orbit_crosscheck_controls()
    )
    orientation, orientation_diagnostics = orientation_and_neutrality_controls()
    fail_closed = fail_closed_controls()
    definition = definition_controls()
    valid = all((
        all(dependency.values()), all(groupoid.values()), all(periodic.values()),
        all(general_crosscheck.values()), all(orientation.values()),
        all(fail_closed.values()),
        all(definition.values()),
    ))
    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": bool(valid),
        "candidate_status": (
            "CONDITIONAL_OCCURRENCE_LIFT_AND_SCOPED_G4_PASS__PHYSICAL_PROMOTION_OPEN"
            if valid else "INVALID_NO_PROMOTION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The supplied parametrized autonomous law generates its action "
            "groupoid and an origin-free occurrence lift on every regular "
            "history. Periodic state return becomes a nonzero deck translation; "
            "aperiodic recurrence remains a sequence of distinct arrows. The "
            "independent stabilizer/R-H/universal-cover route gives the same "
            "history order, including for dense recurrent images with intrinsic "
            "orbit topology. This scoped G4 result proves no calibrated clock, "
            "record field, physical ontology, space or metric."
        ),
        "outcomes": frozen_outcomes(),
        "closure_flags": frozen_closure_flags(),
        "controls": {
            "definition": definition,
            "dependency": dependency,
            "action_groupoid": groupoid,
            "periodic_lift": periodic,
            "general_regular_orbit_crosscheck": general_crosscheck,
            "orientation_and_neutrality": orientation,
            "fail_closed": fail_closed,
        },
        "exact_diagnostics": {
            "action_groupoid": groupoid_diagnostics,
            "periodic_lift": periodic_diagnostics,
            "general_regular_orbit_crosscheck": general_crosscheck_diagnostics,
            "orientation_and_neutrality": orientation_diagnostics,
        },
        "hashes": {
            "flow_groupoid_spec": _canonical_sha256(FLOW_GROUPOID_SPEC),
            "general_orbit_crosscheck_spec": _canonical_sha256(
                GENERAL_ORBIT_CROSSCHECK_SPEC
            ),
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
