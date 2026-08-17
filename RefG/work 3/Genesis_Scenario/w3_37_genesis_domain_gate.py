"""W3-37 exact Genesis domain-separation and closure gate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_37_GENESIS_DOMAIN_SEPARATION"
MODEL_VERSION = "W3-37-v1.1-GENESIS-DOMAINS"
HERE = Path(__file__).resolve().parent
PREREG = HERE / "w3_37_genesis_domain_preregistration.md"
OUTPUT = HERE / "w3_37_result.json"
HASH_OUTPUT = HERE / "w3_37_result.sha256"
PINNED_PREREG_SHA256 = "0e8f8673094e21a48e243a53a108491957e341ec91e3e19c9167163b33eab490"

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
    "finite_process_time_origin_encoded_exact",
    "elapsed_process_time_FTC_exact",
    "bookkeeping_field_has_no_spatial_argument_exact",
    "local_threshold_chain_rule_exact",
    "activated_null_branches_exact",
    "birth_activated_parameter_sets_disjoint_exact",
    "candidate_DAG_acyclic_exact",
    "added_tail_to_relation_edge_creates_cycle_exact",
    "threshold_null_identity_not_forced_exact",
    "registered_top_level_keysets_exact",
    "mutation_controls_pass",
    "aggregate_identity_pass",
}

EXPECTED_PHYSICAL_KEYS = {
    "genesis_action_derived",
    "global_trigger_instability_derived",
    "initial_state_derived",
    "initial_spectrum_topology_derived",
    "order_parameter_defined",
    "phase_transition_potential_derived",
    "activation_threshold_derived",
    "activation_front_eom_derived",
    "global_centerlessness_derived",
    "foundation_energy_balance_derived",
    "energy_partition_transfer_derived",
    "candidate_DAG_edges_derived",
    "tail_propagation_law_derived",
    "mode_selection_operator_derived",
    "stable_oscillon_spectrum_derived",
    "thermal_history_derived",
    "spectroscopic_forward_model_derived",
    "CMB_BBN_structure_validated",
}

EXPECTED_BRANCH_KEYS = {
    "DECLARED_BIRTH_PARAMETER_SET",
    "DECLARED_ALREADY_ACTIVATED_SET",
    "LOCAL_THRESHOLD_CHAIN_RULE",
    "SUPPLIED_ACTIVATED_NULL",
    "RETAINED_CANDIDATE_DAG",
    "ADDED_TAIL_TO_RELATION_EDGE_MUTATION",
}

EXPECTED_NEGATIVE_CONTROL_KEYS = {
    "spatialized_bookkeeping_field",
    "threshold_wrong_sign_not_identity",
    "factor_two_null_speed",
    "threshold_null_expressions_not_identities",
    "merged_parameter_sets_detected",
    "added_edge_cycle_detected",
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
    "genesis_mechanism_status",
    "falsifier_triggered_for_refg",
    "blocking_reasons",
    "contract",
    "closure_flags",
    "physical_closure_flags",
    "identities",
    "branch_classification",
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


def graph_is_acyclic(nodes: tuple[str, ...], edges: tuple[tuple[str, str], ...]) -> bool:
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
    t, s = sp.symbols("t s", nonnegative=True)
    radial_coordinate = sp.symbols("r", real=True)
    cadence = sp.Function("p")
    process_time = sp.Integral(cadence(s), (s, 0, t))
    elapsed_derivative_residual = sp.simplify(
        sp.diff(process_time, t) - cadence(t)
    )
    elapsed_origin_residual = sp.simplify(process_time.subs(t, 0).doit())

    bookkeeping_field = sp.Function("B")(t)
    bookkeeping_gradient_residual = sp.diff(
        bookkeeping_field, radial_coordinate
    )

    R_of_t = sp.Function("R")(t)
    phi_composite = sp.Function("Phi")(R_of_t, t)
    total_threshold_derivative = sp.diff(phi_composite, t)
    R_dot = sp.diff(R_of_t, t)
    phi_r = total_threshold_derivative.coeff(R_dot)
    phi_t = sp.simplify(total_threshold_derivative.subs(R_dot, 0))
    threshold_speed = -phi_t / phi_r
    threshold_residual = sp.simplify(
        total_threshold_derivative.subs(R_dot, threshold_speed)
    )

    c0, p_symbol, a_symbol = sp.symbols("c_0 p a", positive=True)
    null_speed_plus = c0 * p_symbol**2 / a_symbol
    null_speed_minus = -null_speed_plus
    null_residual_plus = sp.simplify(
        p_symbol**2 * c0**2
        - a_symbol**2 / p_symbol**2 * null_speed_plus**2
    )
    null_residual_minus = sp.simplify(
        p_symbol**2 * c0**2
        - a_symbol**2 / p_symbol**2 * null_speed_minus**2
    )
    threshold_null_expression_plus = sp.simplify(
        phi_t + phi_r * null_speed_plus
    )
    threshold_null_expression_minus = sp.simplify(
        phi_t + phi_r * null_speed_minus
    )

    birth_domain = sp.FiniteSet(0)
    activated_domain = sp.Interval.open(0, sp.oo)
    domain_intersection = birth_domain.intersect(activated_domain)
    merged_domain = birth_domain.intersect(sp.Interval(0, sp.oo))

    causal_nodes = ("B", "N", "O", "G", "P")
    causal_edges = (("B", "N"), ("N", "O"), ("O", "G"), ("G", "P"))
    causal_acyclic = graph_is_acyclic(causal_nodes, causal_edges)
    added_edge_graph = causal_edges + (("G", "N"),)
    added_edge_cyclic = not graph_is_acyclic(causal_nodes, added_edge_graph)

    epsilon = sp.symbols("epsilon", nonzero=True)
    spatialized_mutation = sp.diff(
        bookkeeping_field + epsilon * radial_coordinate, radial_coordinate
    )
    wrong_threshold_sign = sp.simplify(
        phi_t + phi_r * (phi_t / phi_r)
    )
    factor_two_speed = 2 * c0 * p_symbol**2 / a_symbol
    factor_two_null_residual = sp.simplify(
        p_symbol**2 * c0**2
        - a_symbol**2 / p_symbol**2 * factor_two_speed**2
    )

    branch_classification = {
        "DECLARED_BIRTH_PARAMETER_SET": "D_B={0}",
        "DECLARED_ALREADY_ACTIVATED_SET": "D_+=(0,infinity)",
        "LOCAL_THRESHOLD_CHAIN_RULE": "Rdot=-Phi_t/Phi_R for Phi_R!=0",
        "SUPPLIED_ACTIVATED_NULL": "dchi/dt=+/-c0*p^2/a",
        "RETAINED_CANDIDATE_DAG": "B->N->O->G->P__POSTULATED",
        "ADDED_TAIL_TO_RELATION_EDGE_MUTATION": "retain base and add G->N",
    }

    physical_flags = {key: False for key in EXPECTED_PHYSICAL_KEYS}
    physical_flip_invalidates = all(
        not all(
            value is False
            for value in (physical_flags | {key: True}).values()
        )
        for key in EXPECTED_PHYSICAL_KEYS
    )
    negative_controls = {
        "spatialized_bookkeeping_field": exact_nonzero(spatialized_mutation),
        "threshold_wrong_sign_not_identity": exact_nonzero(wrong_threshold_sign),
        "factor_two_null_speed": exact_nonzero(factor_two_null_residual),
        "threshold_null_expressions_not_identities": exact_nonzero(
            threshold_null_expression_plus
        ) and exact_nonzero(threshold_null_expression_minus),
        "merged_parameter_sets_detected": merged_domain != sp.EmptySet,
        "added_edge_cycle_detected": added_edge_cyclic,
        "physical_flag_flip_invalidates": physical_flip_invalidates,
    }

    residuals = {
        "elapsed_process_time_derivative": elapsed_derivative_residual,
        "elapsed_process_time_origin": elapsed_origin_residual,
        "bookkeeping_spatial_gradient": bookkeeping_gradient_residual,
        "local_threshold_chain_rule": threshold_residual,
        "activated_metric_null_plus": null_residual_plus,
        "activated_metric_null_minus": null_residual_minus,
        "threshold_null_nonidentity_expression_plus": threshold_null_expression_plus,
        "threshold_null_nonidentity_expression_minus": threshold_null_expression_minus,
    }
    closure_flags = {
        "finite_process_time_origin_encoded_exact": birth_domain == sp.FiniteSet(0),
        "elapsed_process_time_FTC_exact": exact_zero(elapsed_derivative_residual) and exact_zero(elapsed_origin_residual),
        "bookkeeping_field_has_no_spatial_argument_exact": exact_zero(bookkeeping_gradient_residual),
        "local_threshold_chain_rule_exact": exact_zero(threshold_residual),
        "activated_null_branches_exact": exact_zero(null_residual_plus) and exact_zero(null_residual_minus),
        "birth_activated_parameter_sets_disjoint_exact": domain_intersection == sp.EmptySet,
        "candidate_DAG_acyclic_exact": causal_acyclic,
        "added_tail_to_relation_edge_creates_cycle_exact": added_edge_cyclic,
        "threshold_null_identity_not_forced_exact": exact_nonzero(threshold_null_expression_plus) and exact_nonzero(threshold_null_expression_minus),
        "registered_top_level_keysets_exact": False,
        "mutation_controls_pass": all(negative_controls.values()),
        "aggregate_identity_pass": False,
    }

    diagnostics = {
        "residuals": {key: sp.sstr(value) for key, value in residuals.items()},
        "branch_classification": branch_classification,
        "semantic_constraints": {
            "result_class": "ASSUMPTION_CONSISTENCY_ONLY",
            "base_DAG": "POSTULATED_NOT_DERIVED",
            "added_edge_result": "CYCLIC_ONLY_WHILE_BASE_EDGES_ARE_RETAINED",
            "threshold_null_relation": "NOT_AN_IDENTITY__FUTURE_PDE_MAY_IMPOSE",
            "finite_meaning": "FINITE_PARAMETER_ORIGIN_NOT_SPATIAL_SIZE",
            "centerlessness": "FROZEN_POSTULATE_NOT_DERIVED",
        },
        "negative_controls": negative_controls,
    }
    return residuals, closure_flags, physical_flags, diagnostics


def build_contract() -> dict[str, object]:
    return {
        "CLAIM_ID": CLAIM_ID,
        "CLAIM": (
            "Under the frozen branch definitions and retained candidate DAG, "
            "the birth parameter set is disjoint from the already-activated "
            "parameter set, the local threshold is not identically forced to "
            "follow either activated null characteristic, and adding G -> N while "
            "retaining the base edges makes the declared graph cyclic. These "
            "are conditional assumption-consequences only."
        ),
        "TYPE": "EXACT_CONDITIONAL_DEFINITION_AND_GRAPH_CONSISTENCY_GATE",
        "MODEL_VERSION": {
            "id": MODEL_VERSION,
            "change_boundary": (
                "Branch definitions, candidate DAG, activated metric, claim, "
                "semantic constraints, or flag sets."
            ),
        },
        "ASSUMPTIONS": (
            "Declared origin and post-origin sets; positive continuous cadence; "
            "B(t) bookkeeping representation; differentiable threshold with "
            "Phi_R!=0; supplied activated metric; retained candidate DAG."
        ),
        "DOMAIN": (
            "D_B={0}; D_+=(0,infinity); local post-origin threshold; supplied "
            "metric and finite DAG; no spatial-size or physical-tail result."
        ),
        "CONVENTIONS": {
            "birth": "declared parameter origin",
            "global_centerless": "scenario postulate, not output",
            "not_identically_forced": "special solutions or a future PDE may coincide",
            "metric_signature": "+---",
        },
        "FREEDOM_LEDGER": {
            "current_data_fitted_effective_dimension": 0,
            "branch_domain_choice": {
                "source": "Genesis ontology",
                "admissible_class": "ordered measurable parameter sets",
                "scale": "universal",
                "effective_complexity_measure": "set/function choice",
                "status": "FROZEN_FOR_GATE__NOT_DERIVED",
            },
            "candidate_dependency_graph": {
                "source": "Genesis causal hypothesis",
                "admissible_class": "directed graphs on declared event classes",
                "scale": "universal",
                "effective_complexity_measure": "discrete edge set",
                "status": "FROZEN_FOR_GATE__NOT_DERIVED",
            },
            "activated_metric_form": {
                "source": "structural gate choice",
                "admissible_class": "Lorentzian post-origin metric forms",
                "scale": "universal",
                "effective_complexity_measure": "one structural form",
                "status": "FROZEN_FOR_GATE__NOT_DERIVED",
            },
            "background_functions": {
                "source": "foundation action",
                "admissible_class": "positive continuous p(t), positive differentiable a(t)",
                "scale": "universal",
                "effective_complexity_measure": "functional/infinite-dimensional",
                "status": "OPEN_UNINSTANTIATED",
            },
            "activation_tail_field_law": {
                "source": "activation/tail action",
                "admissible_class": "universal differentiable field equations and characteristics",
                "scale": "universal",
                "effective_complexity_measure": "functional/infinite-dimensional",
                "status": "OPEN_UNINSTANTIATED",
            },
            "mode_family_response": {
                "source": "nonlinear field solutions",
                "admissible_class": "response/profile per mode family",
                "scale": "group",
                "effective_complexity_measure": "functional per family",
                "status": "OPEN_UNINSTANTIATED",
            },
            "local_seed_profiles": {
                "source": "local solutions",
                "admissible_class": "finite-energy profile and state",
                "scale": "object",
                "effective_complexity_measure": "functional state per object",
                "status": "OPEN_UNINSTANTIATED",
            },
            "future_observable_nuisance": {
                "source": "future likelihood",
                "admissible_class": "declared finite calibration parameters",
                "scale": "data",
                "effective_complexity_measure": "N_nuisance=0 in W3-37",
                "status": "OPEN_UNINSTANTIATED",
            },
        },
        "DEPENDENCIES": "None; self-contained; no upstream result imported.",
        "METHOD": (
            "Exact FTC, chain rule, set/metric substitutions, both null signs, "
            "pure-Python DAG checks, mutations, top-level keysets, strict JSON."
        ),
        "PASS_CONDITION": (
            "Every registered assumption-consequence and mutation passes; all "
            "physical flags remain false; aggregate AND is true."
        ),
        "FAIL_CONDITION": (
            "Any identity, set, DAG, mutation, or registered keyset fails, or "
            "a physical result is reported as derived."
        ),
        "FALSIFIER": "Failure invalidates this definitional gate only; no RefG or observational falsifier is supplied.",
        "RESIDUAL": "Exact zero/nonidentity residuals, set equality, DAG and keyset predicates.",
        "ERROR_BOUND": "Zero algebraic error; physical/numerical/data error N/A.",
        "VALIDITY_HEALTH": (
            "Exact algebraic health with large disclosed structural freedom; "
            "conservation, stability, thermodynamics, causality, and data N/A."
        ),
        "BRANCHES": sorted(EXPECTED_BRANCH_KEYS),
        "OBSERVABLE_MAP": "N/A: no observable map.",
        "FORWARD_MODEL": "N/A: no physical simulation or likelihood.",
        "DATA_ROLE": "No data read.",
        "IDENTIFIABILITY": (
            "Only consequences of supplied sets, metric, level set, and DAG; "
            "trigger, globality, causal edges, fields, energy, topology open."
        ),
        "BENCHMARK": "N/A as a competing-model benchmark.",
        "CLOSURE_FLAGS": {
            "exact": sorted(EXPECTED_CLOSURE_KEYS),
            "physical_required_false": sorted(EXPECTED_PHYSICAL_KEYS),
        },
        "CROSSCHECK": "FTC, both null signs, set intersection, DAG traversal, factor-two speed, spatial and physical-flag mutations.",
        "PROVENANCE": "Pinned LF prereg, LF source, runtime hashes, UTC, checksum.",
        "FILES": [PREREG.name, Path(__file__).name, OUTPUT.name, HASH_OUTPUT.name],
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
        "source": {"path": Path(__file__).name, "sha256": source_hash},
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
        "evidence_type": "EXACT_ASSUMPTION_CONSEQUENCE",
        "refg_status": "OPEN",
        "genesis_mechanism_status": "OPEN_NOT_DERIVED",
        "falsifier_triggered_for_refg": False,
        "blocking_reasons": [
            "Genesis action and global trigger are not derived.",
            "Branch domains and candidate DAG are supplied, not derived.",
            "Background functions, tail PDE, topology, and energy are open.",
            "No thermal or observational forward model exists."
        ],
        "contract": contract,
        "closure_flags": closure_flags,
        "physical_closure_flags": physical_flags,
        "identities": diagnostics["residuals"],
        "branch_classification": diagnostics["branch_classification"],
        "semantic_constraints": diagnostics["semantic_constraints"],
        "negative_controls": diagnostics["negative_controls"],
        "provenance": provenance,
        "files": {
            "preregistration": PREREG.name,
            "source": Path(__file__).name,
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
        and set(diagnostics["branch_classification"]) == EXPECTED_BRANCH_KEYS
        and set(diagnostics["negative_controls"]) == EXPECTED_NEGATIVE_CONTROL_KEYS
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
        "PASS_CONDITIONAL_DEFINITION_AND_DAG_CONSISTENCY__PHYSICAL_GENESIS_OPEN"
        if artifact_valid
        else "FAIL_EXACT_GATE"
    )
    if not artifact_valid:
        raise RuntimeError("W3-37 aggregate gate failed")
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
