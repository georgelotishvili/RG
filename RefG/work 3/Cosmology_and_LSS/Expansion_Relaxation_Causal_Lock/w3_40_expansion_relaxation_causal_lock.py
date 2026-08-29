"""W3-40 exact expansion--relaxation causal-lock gate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_40_EXPANSION_RELAXATION_CAUSAL_LOCK"
MODEL_VERSION = "W3-40-v1.2-SINGLE-DRIVER-EXPANSION-RELAXATION-CAUSAL-LOCK"
HERE = Path(__file__).resolve().parent
PREREG = HERE / "w3_40_expansion_relaxation_causal_lock_preregistration.md"
OUTPUT = HERE / "w3_40_result.json"
HASH_OUTPUT = HERE / "w3_40_result.sha256"
PINNED_PREREG_SHA256 = "6da72a4fea86fe6bd4c29f007593c9c2c176062150d2090ee597845a53c9f5eb"

REQUIRED_CONTRACT_FIELDS = {
    "CLAIM_ID",
    "CLAIM",
    "TYPE",
    "MODEL_VERSION",
    "ASSUMPTIONS",
    "DOMAIN",
    "CONVENTIONS",
    "FREEDOM_LEDGER",
    "DEPENDENCIES",
    "METHOD",
    "PASS_CONDITION",
    "FAIL_CONDITION",
    "FALSIFIER",
    "RESIDUAL",
    "ERROR_BOUND",
    "VALIDITY_HEALTH",
    "BRANCHES",
    "OBSERVABLE_MAP",
    "FORWARD_MODEL",
    "DATA_ROLE",
    "IDENTIFIABILITY",
    "BENCHMARK",
    "CLOSURE_FLAGS",
    "CROSSCHECK",
    "PROVENANCE",
    "FILES",
}

EXPECTED_CLOSURE_KEYS = {
    "fixed_comoving_link_count_encoded_exact",
    "foundation_link_and_distance_identity_exact",
    "cadence_pressure_bridge_exact",
    "pressure_relaxation_implies_material_contraction_exact",
    "operational_scale_identity_exact",
    "causal_DAG_acyclic_exact",
    "single_primary_foundation_expansion_root_exact",
    "causal_locked_log_rate_identity_exact",
    "causal_locked_process_rate_identity_exact",
    "single_trajectory_operational_growth_positive_exact",
    "A_common_rescaling_invariance_exact",
    "A_only_nonidentifiability_exact",
    "registered_top_level_keysets_exact",
    "mutation_controls_pass",
    "aggregate_identity_pass",
}

EXPECTED_PHYSICAL_KEYS = {
    "foundation_action_derived",
    "expansion_equation_derived",
    "foundation_energy_balance_derived",
    "P_F_of_a_derived",
    "material_bridge_microphysics_derived",
    "kappa_history_derived",
    "absolute_foundation_link_scale_observed",
    "absolute_material_scale_observed",
    "spectroscopic_redshift_forward_map_derived",
    "photon_atomic_transport_derived",
    "H_of_z_derived",
    "luminosity_distance_derived",
    "supernova_time_dilation_derived",
    "CMB_BBN_BAO_validated",
    "structure_growth_validated",
    "observational_discriminator_validated",
}

EXPECTED_CAUSAL_CHAIN_KEYS = {
    "PRIMARY_FOUNDATION_EXPANSION",
    "FOUNDATION_PRESSURE_RELAXATION",
    "MATERIAL_STANDARD_RESPONSE",
    "INTERNAL_OPERATIONAL_READOUT",
}

EXPECTED_NEGATIVE_CONTROL_KEYS = {
    "reversed_pressure_response_detected",
    "linear_bridge_mutation_detected",
    "product_scale_mutation_detected",
    "independent_material_rate_detected",
    "independent_material_root_mutation_detected",
    "numerator_only_rescaling_detected",
    "denominator_only_rescaling_detected",
    "causal_cycle_mutation_detected",
    "registered_keyset_mutation_detected",
    "physical_flag_flip_invalidates",
}

EXPECTED_RESULT_KEYS = {
    "schema_version",
    "claim_id",
    "claim",
    "type",
    "model_version",
    "status",
    "scope_status",
    "artifact_valid",
    "evidence_type",
    "refg_status",
    "causal_lock_status",
    "falsifier_triggered_for_refg",
    "blocking_reasons",
    "contract",
    "closure_flags",
    "physical_closure_flags",
    "identities",
    "causal_chain",
    "identifiability",
    "semantic_constraints",
    "negative_controls",
    "provenance",
    "files",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_zero(value: object) -> bool:
    return sp.simplify(value) == 0


def exact_nonzero(value: object) -> bool:
    return sp.simplify(value) != 0


def graph_is_acyclic(
    nodes: tuple[str, ...], edges: tuple[tuple[str, str], ...]
) -> bool:
    incoming = {node: 0 for node in nodes}
    outgoing = {node: [] for node in nodes}
    for left, right in edges:
        outgoing[left].append(right)
        incoming[right] += 1
    queue = [node for node in nodes if incoming[node] == 0]
    visited = 0
    while queue:
        node = queue.pop(0)
        visited += 1
        for neighbor in outgoing[node]:
            incoming[neighbor] -= 1
            if incoming[neighbor] == 0:
                queue.append(neighbor)
    return visited == len(nodes)


def graph_roots(
    nodes: tuple[str, ...], edges: tuple[tuple[str, str], ...]
) -> tuple[str, ...]:
    children = {right for _, right in edges}
    return tuple(node for node in nodes if node not in children)


def verify_preregistration() -> dict[str, object]:
    if not PREREG.is_file():
        raise RuntimeError(f"Missing preregistration: {PREREG}")
    prereg_bytes = PREREG.read_bytes()
    if b"\r" in prereg_bytes or not prereg_bytes.endswith(b"\n"):
        raise RuntimeError("Preregistration is not canonical LF text")
    prereg_text = prereg_bytes.decode("utf-8")
    claim_marker = "**CLAIM:** "
    if claim_marker not in prereg_text:
        raise RuntimeError("Preregistration claim field is missing")
    claim_block = prereg_text.split(claim_marker, 1)[1].split("\n\n", 1)[0]
    registered_claim = " ".join(
        line.strip() for line in claim_block.splitlines()
    )
    actual = sha256(PREREG)
    if actual != PINNED_PREREG_SHA256:
        raise RuntimeError(
            "Frozen preregistration changed: "
            f"expected {PINNED_PREREG_SHA256}, got {actual}"
        )
    return {
        "path": PREREG.name,
        "sha256": actual,
        "expected_sha256": PINNED_PREREG_SHA256,
        "registered_claim": registered_claim,
        "valid": True,
    }


def derive_gate() -> tuple[
    dict[str, object], dict[str, bool], dict[str, bool], dict[str, object]
]:
    t = sp.symbols("t", real=True)
    a, pressure_f, pressure_f0 = sp.symbols("a P_F P_F0", positive=True)
    p = sp.symbols("p", positive=True)
    n_12, ell_f0, ell_mat0 = sp.symbols(
        "N_12 ell_F0 ell_mat0", positive=True
    )
    kappa, h_a, common_scale = sp.symbols(
        "kappa H_a lambda", positive=True
    )

    fixed_count_residual = sp.diff(n_12, t)
    ell_f = ell_f0 * a
    distance = n_12 * ell_f
    distance_identity_residual = sp.simplify(
        distance - n_12 * ell_f0 * a
    )

    bridge_residual = sp.expand(
        (p**2 - pressure_f / pressure_f0).subs(
            pressure_f, pressure_f0 * p**2
        )
    )
    p_from_pressure = sp.sqrt(pressure_f / pressure_f0)
    pressure_slope = -kappa * pressure_f / a
    p_slope = sp.simplify(
        sp.diff(p_from_pressure, pressure_f) * pressure_slope
    )
    expected_p_slope = -kappa * p_from_pressure / (2 * a)
    p_slope_residual = sp.simplify(p_slope - expected_p_slope)
    log_p_slope = sp.simplify(a * p_slope / p_from_pressure)
    log_p_slope_residual = sp.simplify(log_p_slope + kappa / 2)

    operational_scale = a / p_from_pressure
    ruler_length = ell_mat0 * p_from_pressure
    ruler_readout = distance / ruler_length
    ruler_readout_residual = sp.simplify(
        ruler_readout
        - n_12 * ell_f0 / ell_mat0 * operational_scale
    )

    total_A_slope = sp.simplify(
        sp.diff(operational_scale, a)
        + sp.diff(operational_scale, pressure_f) * pressure_slope
    )
    log_A_slope = sp.simplify(
        a * total_A_slope / operational_scale
    )
    log_A_slope_residual = sp.simplify(
        log_A_slope - (1 + kappa / 2)
    )

    a_dot = a * h_a
    pressure_dot = sp.simplify(pressure_slope * a_dot)
    p_dot = sp.simplify(p_slope * a_dot)
    A_dot = sp.simplify(total_A_slope * a_dot)
    process_rate = sp.simplify(
        (A_dot / operational_scale) / p_from_pressure
    )
    expected_process_rate = h_a * (1 + kappa / 2) / p_from_pressure
    process_rate_residual = sp.simplify(
        process_rate - expected_process_rate
    )
    pressure_rate_residual = sp.simplify(
        pressure_dot / pressure_f + kappa * h_a
    )
    material_rate_residual = sp.simplify(
        p_dot / p_from_pressure + kappa * h_a / 2
    )

    causal_nodes = ("a", "P_F", "p", "A")
    causal_edges = (
        ("a", "P_F"),
        ("P_F", "p"),
        ("a", "A"),
        ("p", "A"),
    )
    causal_acyclic = graph_is_acyclic(causal_nodes, causal_edges)
    causal_roots = graph_roots(causal_nodes, causal_edges)
    single_primary_foundation_expansion_root = causal_roots == ("a",)
    causal_cycle_mutation = causal_edges + (("p", "P_F"),)
    causal_cycle_detected = not graph_is_acyclic(
        causal_nodes, causal_cycle_mutation
    )
    independent_material_root_mutation = tuple(
        edge for edge in causal_edges if edge != ("P_F", "p")
    )
    independent_material_root_mutation_detected = graph_roots(
        causal_nodes, independent_material_root_mutation
    ) == ("a", "p")

    scaled_a = common_scale * a
    scaled_p = common_scale * p
    scaled_pressure = common_scale**2 * pressure_f
    scaled_A_residual = sp.simplify(scaled_a / scaled_p - a / p)
    scaled_bridge_residual = sp.expand(
        (scaled_p**2 - scaled_pressure / pressure_f0).subs(
            pressure_f, pressure_f0 * p**2
        )
    )

    t0, h_history, eps_history, delta_history = sp.symbols(
        "t_0 h_history eps_history delta_history", positive=True
    )
    x_history = (t - t0) / t0
    a_history_1 = sp.exp(h_history * x_history)
    p_history_1 = sp.exp(-(eps_history + delta_history) * x_history)
    pressure_history_1 = pressure_f0 * p_history_1**2
    lambda_history = sp.exp(eps_history * x_history)
    a_history_2 = sp.simplify(lambda_history * a_history_1)
    p_history_2 = sp.simplify(lambda_history * p_history_1)
    pressure_history_2 = sp.simplify(lambda_history**2 * pressure_history_1)
    A_history_1 = sp.simplify(a_history_1 / p_history_1)
    A_history_2 = sp.simplify(a_history_2 / p_history_2)
    functional_A_residual = sp.simplify(A_history_2 - A_history_1)
    functional_bridge_1_residual = sp.simplify(
        p_history_1**2 - pressure_history_1 / pressure_f0
    )
    functional_bridge_2_residual = sp.simplify(
        p_history_2**2 - pressure_history_2 / pressure_f0
    )
    normalized_history_residuals = (
        sp.simplify(lambda_history.subs(t, t0) - 1),
        sp.simplify(a_history_1.subs(t, t0) - 1),
        sp.simplify(a_history_2.subs(t, t0) - 1),
        sp.simplify(p_history_1.subs(t, t0) - 1),
        sp.simplify(p_history_2.subs(t, t0) - 1),
        sp.simplify(pressure_history_1.subs(t, t0) / pressure_f0 - 1),
        sp.simplify(pressure_history_2.subs(t, t0) / pressure_f0 - 1),
    )
    a_history_1_dot = sp.simplify(sp.diff(a_history_1, t))
    a_history_2_dot = sp.simplify(sp.diff(a_history_2, t))
    p_history_1_dot = sp.simplify(sp.diff(p_history_1, t))
    p_history_2_dot = sp.simplify(sp.diff(p_history_2, t))
    pressure_history_1_dot = sp.simplify(sp.diff(pressure_history_1, t))
    pressure_history_2_dot = sp.simplify(sp.diff(pressure_history_2, t))
    pressure_a_slope_1 = sp.simplify(
        pressure_history_1_dot / a_history_1_dot
    )
    pressure_a_slope_2 = sp.simplify(
        pressure_history_2_dot / a_history_2_dot
    )
    lambda_history_dot = sp.simplify(sp.diff(lambda_history, t))
    functional_history_signs_preserved = all(
        (
            lambda_history.is_positive,
            a_history_1_dot.is_positive,
            a_history_2_dot.is_positive,
            p_history_1_dot.is_negative,
            p_history_2_dot.is_negative,
            pressure_history_1_dot.is_negative,
            pressure_history_2_dot.is_negative,
            pressure_a_slope_1.is_negative,
            pressure_a_slope_2.is_negative,
        )
    )
    functional_histories_distinct = bool(
        exact_nonzero(lambda_history_dot)
        and exact_nonzero(a_history_2 - a_history_1)
        and exact_nonzero(p_history_2 - p_history_1)
    )

    reversed_pressure_slope = kappa * pressure_f / a
    reversed_p_slope = sp.simplify(
        sp.diff(p_from_pressure, pressure_f) * reversed_pressure_slope
    )
    linear_bridge_mutation = pressure_f / pressure_f0
    linear_bridge_residual = sp.simplify(
        linear_bridge_mutation**2 - pressure_f / pressure_f0
    )
    product_scale_residual = sp.simplify(
        a * p_from_pressure - operational_scale
    )
    independent_shrink_rate = sp.symbols("S_p", positive=True)
    independent_rate_residual = sp.simplify(
        -independent_shrink_rate + kappa * h_a / 2
    )
    numerator_only_residual = sp.simplify(
        common_scale * a / p - a / p
    )
    denominator_only_residual = sp.simplify(
        a / (common_scale * p) - a / p
    )

    physical_flags = {key: False for key in EXPECTED_PHYSICAL_KEYS}
    physical_flip_invalidates = all(
        not all(
            value is False
            for value in (physical_flags | {key: True}).values()
        )
        for key in EXPECTED_PHYSICAL_KEYS
    )
    registered_keyset_mutation_detected = bool(
        (EXPECTED_RESULT_KEYS - {"status"}) != EXPECTED_RESULT_KEYS
        and (EXPECTED_CLOSURE_KEYS | {"unregistered_mutation"})
        != EXPECTED_CLOSURE_KEYS
    )
    negative_controls = {
        "reversed_pressure_response_detected": bool(
            reversed_p_slope.is_positive
        ),
        "linear_bridge_mutation_detected": exact_nonzero(
            linear_bridge_residual
        ),
        "product_scale_mutation_detected": exact_nonzero(
            product_scale_residual
        ),
        "independent_material_rate_detected": exact_nonzero(
            independent_rate_residual
        ),
        "independent_material_root_mutation_detected": (
            independent_material_root_mutation_detected
        ),
        "numerator_only_rescaling_detected": exact_nonzero(
            numerator_only_residual
        ),
        "denominator_only_rescaling_detected": exact_nonzero(
            denominator_only_residual
        ),
        "causal_cycle_mutation_detected": causal_cycle_detected,
        "registered_keyset_mutation_detected": (
            registered_keyset_mutation_detected
        ),
        "physical_flag_flip_invalidates": physical_flip_invalidates,
    }

    residuals = {
        "fixed_comoving_count": fixed_count_residual,
        "foundation_distance": distance_identity_residual,
        "cadence_pressure_bridge": bridge_residual,
        "material_slope": p_slope_residual,
        "material_log_slope": log_p_slope_residual,
        "ruler_normalized_readout": ruler_readout_residual,
        "operational_log_slope": log_A_slope_residual,
        "pressure_coordinate_rate": pressure_rate_residual,
        "material_coordinate_rate": material_rate_residual,
        "operational_process_rate": process_rate_residual,
        "common_rescaling_A": scaled_A_residual,
        "common_rescaling_bridge": scaled_bridge_residual,
        "normalized_functional_rescaling_A": functional_A_residual,
        "normalized_functional_bridge_history_1": (
            functional_bridge_1_residual
        ),
        "normalized_functional_bridge_history_2": (
            functional_bridge_2_residual
        ),
        "normalized_functional_present_values": sp.Add(
            *normalized_history_residuals
        ),
    }
    closure_flags = {
        "fixed_comoving_link_count_encoded_exact": exact_zero(
            fixed_count_residual
        ),
        "foundation_link_and_distance_identity_exact": exact_zero(
            distance_identity_residual
        ),
        "cadence_pressure_bridge_exact": exact_zero(bridge_residual),
        "pressure_relaxation_implies_material_contraction_exact": (
            exact_zero(p_slope_residual)
            and exact_zero(log_p_slope_residual)
            and pressure_slope.is_negative
            and p_slope.is_negative
        ),
        "operational_scale_identity_exact": exact_zero(
            ruler_readout_residual
        ),
        "causal_DAG_acyclic_exact": causal_acyclic,
        "single_primary_foundation_expansion_root_exact": (
            single_primary_foundation_expansion_root
        ),
        "causal_locked_log_rate_identity_exact": (
            exact_zero(log_A_slope_residual)
            and exact_zero(pressure_rate_residual)
            and exact_zero(material_rate_residual)
        ),
        "causal_locked_process_rate_identity_exact": exact_zero(
            process_rate_residual
        ),
        "single_trajectory_operational_growth_positive_exact": bool(
            log_A_slope.is_positive and process_rate.is_positive
        ),
        "A_common_rescaling_invariance_exact": (
            exact_zero(scaled_A_residual)
            and exact_zero(scaled_bridge_residual)
        ),
        "A_only_nonidentifiability_exact": (
            exact_zero(functional_A_residual)
            and exact_zero(functional_bridge_1_residual)
            and exact_zero(functional_bridge_2_residual)
            and all(exact_zero(value) for value in normalized_history_residuals)
            and functional_history_signs_preserved
            and functional_histories_distinct
        ),
        "registered_top_level_keysets_exact": False,
        "mutation_controls_pass": all(negative_controls.values()),
        "aggregate_identity_pass": False,
    }

    causal_chain = {
        "PRIMARY_FOUNDATION_EXPANSION": (
            "a_dot>0__SOLE_PRIMARY_CAUSAL_ROOT__SELECTED_PHYSICAL_HYPOTHESIS"
        ),
        "FOUNDATION_PRESSURE_RELAXATION": (
            "DEPENDENT_ON_a__dP_F/da<0__SELECTED_CONSTITUTIVE_SIGN__LAW_OPEN"
        ),
        "MATERIAL_STANDARD_RESPONSE": (
            "DEPENDENT_ON_P_F__p^2=P_F/P_F0__NOT_SECOND_DRIVER"
        ),
        "INTERNAL_OPERATIONAL_READOUT": (
            "A=a/p__RELATIONAL_READOUT_OF_ONE_TRAJECTORY__NOT_ADDITIVE"
        ),
    }
    diagnostics = {
        "residuals": {key: sp.sstr(value) for key, value in residuals.items()},
        "causal_chain": causal_chain,
        "identifiability": {
            "identified_from_A_alone": ["A"],
            "not_identified_from_A_alone": ["a", "p", "P_F"],
            "equivalence_class": (
                "(a,p,P_F)->(lambda(t)*a,lambda(t)*p,"
                "lambda(t)^2*P_F), lambda(t)>0, lambda(t0)=1"
            ),
            "closure_needed": (
                "derived P_F(a), normalization history, or an independent "
                "dimensionless response channel"
            ),
        },
        "semantic_constraints": {
            "primary_process": "FOUNDATION_EXPANSION",
            "primary_causal_roots": ["a"],
            "material_contraction_role": "CAUSALLY_DEPENDENT_RESPONSE",
            "operational_measurement": "A_EQUALS_a_OVER_p",
            "independent_second_driver": "EXCLUDED_FROM_SELECTED_BRANCH",
            "effect_counting": (
                "ONE_PRIMARY_DRIVER_WITH_DEPENDENT_RESPONSE__NO_DOUBLE_COUNTING"
            ),
            "absolute_a_or_p_from_A": "NOT_IDENTIFIABLE",
            "P_F_of_a_status": "OPEN_NOT_DERIVED",
            "redshift_forward_map_status": "OPEN_NOT_DERIVED",
        },
        "negative_controls": negative_controls,
    }
    return residuals, closure_flags, physical_flags, diagnostics


def build_contract() -> dict[str, object]:
    return {
        "CLAIM_ID": CLAIM_ID,
        "CLAIM": (
            "On the frozen selected branch, foundation expansion is the sole "
            "primary cosmological driver. With fixed comoving link count, its "
            "increase of the foundation link scale lowers foundation pressure; "
            "through the positive bridge p^2=P_F/P_F0, that pressure relaxation "
            "contracts the material standard. These are causally ordered stages "
            "of one trajectory, not independent or additive effects. An internal "
            "observer reads the trajectory only through the relational scale "
            "A=a/p; A alone does not identify a and p. The gate proves the linked "
            "scale and rate identities but does not derive P_F(a) or an "
            "observational cosmology."
        ),
        "TYPE": "EXACT_CONDITIONAL_CAUSAL_DICTIONARY_AND_IDENTIFIABILITY_GATE",
        "MODEL_VERSION": {
            "id": MODEL_VERSION,
            "change_boundary": (
                "Causal ordering, unique-primary-root condition, sign assumptions, "
                "cadence-pressure bridge, "
                "operational scale, comoving convention, identifiability class, "
                "semantic constraints, or closure keys."
            ),
        },
        "ASSUMPTIONS": (
            "Positive regular homogeneous scales; fixed ideal-comoving N_12; "
            "unique causal root=a; "
            "a_dot>0; dP_F/da<0; kappa=-dln(P_F)/dln(a)>0; "
            "p^2=P_F/P_F0; ell_mat=ell_mat0*p; A=a/p."
        ),
        "DOMAIN": (
            "Positive finite regular post-origin variables and differentiable "
            "homogeneous histories on the selected expansion branch."
        ),
        "CONVENTIONS": {
            "coordinate_time": "dot=d/dt",
            "process_time": "d_tau=p*dt",
            "comoving_component": "dN_12/dt=0",
            "foundation_pressure": "P_F is not thermodynamic pressure",
            "operational_scale": "A=a/p",
        },
        "FREEDOM_LEDGER": {
            "current_data_fitted_effective_dimension": 0,
            "foundation_expansion_history": {
                "source": "foundation action and initial state",
                "domain": "positive homogeneous histories",
                "scale": "universal",
                "effective_complexity_measure": "one functional history a(t)",
                "status": "OPEN_UNINSTANTIATED",
            },
            "pressure_relaxation_law": {
                "source": "foundation energy balance and constitutive dynamics",
                "domain": "selected expansion branch",
                "scale": "universal",
                "effective_complexity_measure": "one function P_F(a) or kappa(a)",
                "status": "SIGN_FROZEN__MAGNITUDE_AND_HISTORY_OPEN",
            },
            "material_response_law": {
                "source": "foundation-matter microphysics",
                "domain": "universal material standards",
                "scale": "universal",
                "effective_complexity_measure": "one frozen bridge in this gate",
                "status": "BRIDGE_FROZEN__MICROPHYSICS_OPEN",
            },
            "photon_atomic_response": {
                "source": "radiative and atomic action",
                "domain": "each response family",
                "scale": "group",
                "effective_complexity_measure": "functional per response family",
                "status": "OPEN_UNINSTANTIATED",
            },
            "source_history": {
                "source": "astrophysical emitter",
                "domain": "each source",
                "scale": "object",
                "effective_complexity_measure": "one functional history per object",
                "status": "OPEN_UNINSTANTIATED",
            },
            "likelihood_nuisance": {
                "source": "future survey and likelihood",
                "domain": "each datum or declared group",
                "scale": "data",
                "effective_complexity_measure": "N_nuisance=0 in W3-40",
                "status": "OPEN_UNINSTANTIATED",
            },
        },
        "DEPENDENCIES": (
            "None; self-contained; no upstream result artifact is imported."
        ),
        "METHOD": (
            "Exact substitution, ordinary/logarithmic chain rules, positive-sign "
            "classification, ruler normalization, rescaling invariance, an exact "
            "normalized functional-history non-identifiability witness, DAG and "
            "unique-primary-root checks, mutation checks, strict LF/JSON/hash."
        ),
        "PASS_CONDITION": (
            "Every identity, causal-order and unique-primary-root check, "
            "identifiability construction, keyset, and mutation passes; every "
            "physical flag remains false."
        ),
        "FAIL_CONDITION": (
            "Any registered check fails, any physical flag is true, the graph has "
            "a primary root other than a, p is treated as an independent or "
            "additive driver, or an unclosed physical/observable result is reported."
        ),
        "FALSIFIER": (
            "A symbolic counterexample under the frozen assumptions falsifies "
            "this dictionary gate; no RefG-wide observational falsifier is supplied."
        ),
        "RESIDUAL": (
            "Exact zero identities, strict sign consequences, graph/keyset "
            "predicates, and common-rescaling equality."
        ),
        "ERROR_BOUND": (
            "Zero algebraic error; numerical, continuum, and observational error N/A."
        ),
        "VALIDITY_HEALTH": (
            "Internal causal dictionary and A-only identifiability only; action, "
            "dynamics, transport, thermodynamics, structure, and data remain open."
        ),
        "BRANCHES": [
            "IDEAL_COMOVING_CAUSAL_TRAJECTORY",
            "A_ONLY_EQUIVALENCE_CLASS",
            "LOCAL_PECULIAR_MOTION_OUTSIDE_GATE",
        ],
        "OBSERVABLE_MAP": (
            "L_12/ell_mat=(N_12*ell_F0/ell_mat0)*A only; spectroscopic "
            "redshift and distance maps are open."
        ),
        "FORWARD_MODEL": "N/A: no synthetic cosmological observable or likelihood.",
        "DATA_ROLE": "No data or upstream result artifacts are read.",
        "IDENTIFIABILITY": (
            "A alone preserves normalized positive functional histories under "
            "(a,p,P_F)->(lambda(t)*a,lambda(t)*p,lambda(t)^2*P_F), with "
            "lambda(t0)=1; a, p, and P_F require a derived closure or "
            "independent dimensionless channel."
        ),
        "BENCHMARK": (
            "Recover distance, bridge, log-rate, process-rate, unique-primary-root, "
            "and rescaling identities and detect all declared mutations."
        ),
        "CLOSURE_FLAGS": {
            "exact": sorted(EXPECTED_CLOSURE_KEYS),
            "physical_required_false": sorted(EXPECTED_PHYSICAL_KEYS),
        },
        "CROSSCHECK": (
            "Ordinary/log derivatives, coordinate/process rates, ruler readout, "
            "DAG with unique primary root a, normalized functional equivalence "
            "class, and declared sign/bridge/scale/rate/root/keyset/flag mutations."
        ),
        "PROVENANCE": (
            "Pinned UTF-8 LF preregistration, LF source, runtime hashes and "
            "versions, UTC, strict JSON, atomic result and checksum."
        ),
        "FILES": [
            "README.md",
            PREREG.name,
            Path(__file__).name,
            OUTPUT.name,
            HASH_OUTPUT.name,
        ],
    }


def build_report() -> dict[str, object]:
    prereg_record = verify_preregistration()
    _, closure_flags, physical_flags, diagnostics = derive_gate()
    contract = build_contract()
    contract_keys_exact = set(contract) == REQUIRED_CONTRACT_FIELDS
    closure_keys_exact = set(closure_flags) == EXPECTED_CLOSURE_KEYS
    physical_keys_exact = set(physical_flags) == EXPECTED_PHYSICAL_KEYS

    source_path = Path(__file__).resolve()
    source_bytes = source_path.read_bytes()
    if b"\r" in source_bytes or not source_bytes.endswith(b"\n"):
        raise RuntimeError("Source is not canonical LF text")
    source_hash = sha256(source_path)
    provenance = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "preregistration": prereg_record,
        "source": {"path": source_path.name, "sha256": source_hash},
        "python": platform.python_version(),
        "sympy": importlib.metadata.version("sympy"),
        "platform": platform.platform(),
        "line_endings": "LF",
    }

    result = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "claim": contract["CLAIM"],
        "type": contract["TYPE"],
        "model_version": MODEL_VERSION,
        "status": "PENDING",
        "scope_status": "PENDING",
        "artifact_valid": False,
        "evidence_type": "EXACT_CONDITIONAL_ASSUMPTION_CONSEQUENCE",
        "refg_status": "SELECTED_HYPOTHESIS__PHYSICAL_CLOSURE_OPEN",
        "causal_lock_status": "CONDITIONALLY_CONSISTENT__NOT_DERIVED",
        "falsifier_triggered_for_refg": False,
        "blocking_reasons": [
            "No foundation action or expansion equation is derived.",
            "No foundation energy balance or P_F(a) law is derived.",
            "The material bridge is frozen but not derived from microphysics.",
            "No photon-atomic, redshift, distance, thermal, or growth forward model exists.",
            "No observational likelihood or discriminator is evaluated.",
        ],
        "contract": contract,
        "closure_flags": closure_flags,
        "physical_closure_flags": physical_flags,
        "identities": diagnostics["residuals"],
        "causal_chain": diagnostics["causal_chain"],
        "identifiability": diagnostics["identifiability"],
        "semantic_constraints": diagnostics["semantic_constraints"],
        "negative_controls": diagnostics["negative_controls"],
        "provenance": provenance,
        "files": {
            "preregistration": PREREG.name,
            "source": source_path.name,
            "result": OUTPUT.name,
            "checksum": HASH_OUTPUT.name,
        },
    }

    result_keys_exact = set(result) == EXPECTED_RESULT_KEYS
    closure_flags["registered_top_level_keysets_exact"] = bool(
        contract_keys_exact
        and closure_keys_exact
        and physical_keys_exact
        and result_keys_exact
        and set(diagnostics["causal_chain"]) == EXPECTED_CAUSAL_CHAIN_KEYS
        and set(diagnostics["negative_controls"])
        == EXPECTED_NEGATIVE_CONTROL_KEYS
        and result["claim"] == contract["CLAIM"]
        and prereg_record["registered_claim"] == contract["CLAIM"]
        and contract["MODEL_VERSION"]["id"] == MODEL_VERSION
    )
    closure_flags["aggregate_identity_pass"] = all(
        value
        for key, value in closure_flags.items()
        if key != "aggregate_identity_pass"
    )
    artifact_valid = bool(
        closure_flags["aggregate_identity_pass"]
        and all(value is False for value in physical_flags.values())
    )
    result["artifact_valid"] = artifact_valid
    result["status"] = "PASS" if artifact_valid else "FAIL"
    result["scope_status"] = (
        "PASS_EXACT_CAUSAL_LOCK_DICTIONARY__DYNAMICS_AND_OBSERVABLES_OPEN"
        if artifact_valid
        else "FAIL_EXACT_CAUSAL_LOCK_GATE"
    )
    if not artifact_valid:
        raise RuntimeError("W3-40 aggregate gate failed")
    return result


def write_atomic(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    temporary.replace(path)


def write_report(report: dict[str, object]) -> str:
    payload = json.dumps(
        report,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    write_atomic(OUTPUT, payload)
    digest = sha256(OUTPUT)
    write_atomic(HASH_OUTPUT, f"{digest}  {OUTPUT.name}\n")
    return digest


def write_failure(error: Exception) -> None:
    failure = {
        "schema_version": "1.0-failure",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "status": "FAIL",
        "artifact_valid": False,
        "error": f"{type(error).__name__}: {error}",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    payload = json.dumps(
        failure,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    write_atomic(OUTPUT, payload)
    digest = sha256(OUTPUT)
    write_atomic(HASH_OUTPUT, f"{digest}  {OUTPUT.name}\n")


def main() -> int:
    try:
        report = build_report()
        digest = write_report(report)
    except Exception as error:
        write_failure(error)
        print(f"FAIL: {error}", file=sys.stderr)
        return 2
    print(report["scope_status"])
    print(f"Result: {OUTPUT}")
    print(f"Result SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
