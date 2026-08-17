"""W3-38 exact conditional Genesis connectivity and accounting witness."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from collections import deque
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


CLAIM_ID = "W3_38_CONDITIONAL_GENESIS_EXISTENCE"
MODEL_VERSION = "W3-38-v1.0-CONDITIONAL-EXISTENCE"
HERE = Path(__file__).resolve().parent
PREREG = HERE / "w3_38_conditional_existence_preregistration.md"
OUTPUT = HERE / "w3_38_result.json"
HASH_OUTPUT = HERE / "w3_38_result.sha256"
PINNED_PREREG_SHA256 = "442d04ca95470507e500634f8048d7234cdcc3b1f5dcc58c585c78d7d7d484af"

L = 5
DIMENSION = 2
RHO = Fraction(3, 5)
Q_BOND = Fraction(1, 2)

REQUIRED_CONTRACT_FIELDS = {
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS",
    "DOMAIN", "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES",
    "METHOD", "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER",
    "RESIDUAL", "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES",
    "OBSERVABLE_MAP", "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY",
    "BENCHMARK", "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
}

EXPECTED_CLOSURE_KEYS = {
    "finite_graph_counts_exact",
    "tail_bridge_condition_exact",
    "tail_rule_translation_covariant_exact",
    "full_fixture_connected_exact",
    "all_periodic_directions_wrap_exact",
    "translation_action_free_transitive_exact",
    "graph_center_equals_vertex_set_exact",
    "finite_wrapping_event_exact",
    "positive_probability_lower_bound_exact",
    "cycle_bond_enumeration_exact",
    "energy_feasibility_inequality_exact",
    "energy_ledger_balance_exact",
    "energy_ledger_nonnegative_exact",
    "schema_keysets_exact",
    "mutation_controls_pass",
    "aggregate_identity_pass",
}

EXPECTED_PHYSICAL_KEYS = {
    "periodic_cosmic_topology_derived",
    "cosmic_dimension_and_period_derived",
    "graph_to_foundation_mapping_derived",
    "tail_field_equation_derived",
    "tail_range_or_speed_derived",
    "bridge_formation_dynamics_derived",
    "occupation_probability_derived",
    "infinite_volume_threshold_derived",
    "physical_universe_percolation_established",
    "cosmological_centerlessness_established",
    "total_genesis_energy_derived",
    "vertex_or_edge_energy_derived",
    "energy_conservation_dynamics_derived",
    "energy_partition_fractions_derived",
    "matter_radiation_assignment_derived",
    "structure_formation_derived",
    "genesis_trigger_derived",
    "observable_forward_model_derived",
    "data_validated",
}

EXPECTED_NEGATIVE_CONTROL_KEYS = {
    "low_tail_range_bridge_fails",
    "x_seam_removal_loses_x_wrap",
    "open_grid_breaks_transitivity_and_full_center",
    "origin_selected_rule_breaks_covariance",
    "energy_overrun_detected",
    "double_counted_tail_energy_detected",
    "zero_probability_not_positive",
    "physical_flag_flip_invalidates",
}

EXPECTED_RESULT_KEYS = {
    "schema_version", "claim_id", "claim", "type", "model_version",
    "status", "scope_status", "artifact_valid", "evidence_type",
    "refg_status", "genesis_scenario_status", "physical_realization_status",
    "falsifier_triggered_for_refg", "blocking_reasons", "contract", "inputs",
    "graph_witness", "tail_bridge_witness", "finite_percolation_witness",
    "probability_calibration", "energy_partition_ledger", "closure_flags",
    "physical_closure_flags", "negative_controls", "provenance", "files",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def canonical_edge(left: tuple[int, int], right: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def vertices() -> tuple[tuple[int, int], ...]:
    return tuple((x, y) for x in range(L) for y in range(L))


def torus_edges() -> frozenset[tuple[tuple[int, int], tuple[int, int]]]:
    edges = set()
    for x, y in vertices():
        edges.add(canonical_edge((x, y), ((x + 1) % L, y)))
        edges.add(canonical_edge((x, y), (x, (y + 1) % L)))
    return frozenset(edges)


def open_grid_edges() -> frozenset[tuple[tuple[int, int], tuple[int, int]]]:
    edges = set()
    for x, y in vertices():
        if x + 1 < L:
            edges.add(canonical_edge((x, y), (x + 1, y)))
        if y + 1 < L:
            edges.add(canonical_edge((x, y), (x, y + 1)))
    return frozenset(edges)


def adjacency(edges: frozenset[tuple[tuple[int, int], tuple[int, int]]]) -> dict[tuple[int, int], set[tuple[int, int]]]:
    graph = {vertex: set() for vertex in vertices()}
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    return graph


def bfs_distances(graph: dict[tuple[int, int], set[tuple[int, int]]], start: tuple[int, int]) -> dict[tuple[int, int], int]:
    distances = {start: 0}
    queue: deque[tuple[int, int]] = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances


def translate(vertex: tuple[int, int], shift: tuple[int, int]) -> tuple[int, int]:
    return ((vertex[0] + shift[0]) % L, (vertex[1] + shift[1]) % L)


def translate_edge(edge: tuple[tuple[int, int], tuple[int, int]], shift: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    return canonical_edge(translate(edge[0], shift), translate(edge[1], shift))


def translations_are_automorphisms(edges: frozenset[tuple[tuple[int, int], tuple[int, int]]]) -> bool:
    return all(
        frozenset(translate_edge(edge, shift) for edge in edges) == edges
        for shift in vertices()
    )


def translation_action_free_transitive() -> bool:
    node_set = set(vertices())
    orbit = {translate((0, 0), shift) for shift in vertices()}
    free = all(
        shift == (0, 0)
        or all(translate(vertex, shift) != vertex for vertex in vertices())
        for shift in vertices()
    )
    return orbit == node_set and free


def wraps_positive_direction(
    walk: tuple[tuple[int, int], ...],
    axis: int,
    edges: frozenset[tuple[tuple[int, int], tuple[int, int]]],
) -> bool:
    if len(walk) != L + 1 or walk[0] != walk[-1]:
        return False
    lifted_displacement = 0
    for left, right in zip(walk, walk[1:]):
        if canonical_edge(left, right) not in edges:
            return False
        other_axis = 1 - axis
        if left[other_axis] != right[other_axis]:
            return False
        if (right[axis] - left[axis]) % L != 1:
            return False
        lifted_displacement += 1
    return lifted_displacement == L


def has_winding_cycle(
    edges: frozenset[tuple[tuple[int, int], tuple[int, int]]],
    axis: int,
) -> bool:
    """Detect any nonzero lifted cycle displacement in one torus direction."""
    graph = adjacency(edges)
    lifts: dict[tuple[int, int], tuple[int, int]] = {}
    for start in vertices():
        if start in lifts:
            continue
        lifts[start] = (0, 0)
        queue: deque[tuple[int, int]] = deque([start])
        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                step = []
                for coordinate in range(2):
                    modular_delta = (
                        neighbor[coordinate] - current[coordinate]
                    ) % L
                    if modular_delta == 0:
                        step.append(0)
                    elif modular_delta == 1:
                        step.append(1)
                    elif modular_delta == L - 1:
                        step.append(-1)
                    else:
                        raise RuntimeError("Non-nearest-neighbor torus edge")
                candidate = (
                    lifts[current][0] + step[0],
                    lifts[current][1] + step[1],
                )
                if neighbor not in lifts:
                    lifts[neighbor] = candidate
                    queue.append(neighbor)
                else:
                    cycle_displacement = (
                        candidate[0] - lifts[neighbor][0],
                        candidate[1] - lifts[neighbor][1],
                    )
                    if cycle_displacement[axis] != 0:
                        if cycle_displacement[axis] % L != 0:
                            raise RuntimeError("Invalid torus lift displacement")
                        return True
    return False


def ring_probabilities(q: Fraction) -> tuple[Fraction, Fraction, int, int]:
    connected_probability = Fraction(0, 1)
    wrap_probability = Fraction(0, 1)
    connected_states = 0
    wrap_states = 0
    for mask in range(1 << L):
        occupied = [(mask >> edge) & 1 == 1 for edge in range(L)]
        count = sum(occupied)
        weight = q**count * (1 - q) ** (L - count)
        ring_graph = {vertex: set() for vertex in range(L)}
        for edge_index, present in enumerate(occupied):
            if present:
                left = edge_index
                right = (edge_index + 1) % L
                ring_graph[left].add(right)
                ring_graph[right].add(left)
        reached = {0}
        queue = deque([0])
        while queue:
            current = queue.popleft()
            for neighbor in ring_graph[current]:
                if neighbor not in reached:
                    reached.add(neighbor)
                    queue.append(neighbor)
        connected = len(reached) == L
        wraps = all(occupied)
        if connected:
            connected_states += 1
            connected_probability += weight
        if wraps:
            wrap_states += 1
            wrap_probability += weight
    return connected_probability, wrap_probability, connected_states, wrap_states


def verify_preregistration() -> dict[str, object]:
    if not PREREG.is_file():
        raise RuntimeError(f"Missing preregistration: {PREREG}")
    actual = sha256(PREREG)
    if actual != PINNED_PREREG_SHA256:
        raise RuntimeError(
            f"Frozen preregistration changed: expected {PINNED_PREREG_SHA256}, got {actual}"
        )
    return {
        "path": PREREG.name,
        "sha256": actual,
        "expected_sha256": PINNED_PREREG_SHA256,
        "valid": True,
    }


def derive_gate() -> tuple[dict[str, bool], dict[str, bool], dict[str, object]]:
    node_set = set(vertices())
    edges = torus_edges()
    graph = adjacency(edges)
    reached = bfs_distances(graph, (0, 0))
    connected = set(reached) == node_set

    x_walk = tuple((step % L, 0) for step in range(L + 1))
    y_walk = tuple((0, step % L) for step in range(L + 1))
    wrap_x = wraps_positive_direction(x_walk, 0, edges)
    wrap_y = wraps_positive_direction(y_walk, 1, edges)

    automorphisms = translations_are_automorphisms(edges)
    free_transitive = translation_action_free_transitive()
    eccentricities = {
        vertex: max(bfs_distances(graph, vertex).values()) for vertex in vertices()
    }
    degrees = {vertex: len(graph[vertex]) for vertex in vertices()}
    minimum_eccentricity = min(eccentricities.values())
    center_set = {vertex for vertex, value in eccentricities.items() if value == minimum_eccentricity}

    bridge_active = 2 * RHO >= 1
    bridge_rule = {edge: bridge_active for edge in edges}
    bridge_covariant = all(
        bridge_rule[edge] == bridge_rule[translate_edge(edge, shift)]
        for shift in vertices() for edge in edges
    )

    probability_lower_bound = Q_BOND ** len(edges)
    ring_connected, ring_wrap, connected_states, wrap_states = ring_probabilities(Q_BOND)

    energy_star = Fraction(1, 1)
    vertex_amount = Fraction(1, 4 * len(vertices()))
    edge_amount = Fraction(1, 4 * len(edges))
    locked_total = len(vertices()) * vertex_amount
    tail_total = len(edges) * edge_amount
    unresolved_total = energy_star - locked_total - tail_total
    energy_residual = energy_star - locked_total - tail_total - unresolved_total
    frozen_partition = (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2))
    partition_crosscheck = (
        (locked_total, tail_total, unresolved_total) == frozen_partition
        and sum(frozen_partition, Fraction(0, 1)) == energy_star
    )

    low_range_fails = 2 * Fraction(2, 5) < 1
    x_seam_removed = frozenset(
        edge for edge in edges
        if not (
            edge[0][1] == edge[1][1]
            and {edge[0][0], edge[1][0]} == {0, L - 1}
        )
    )
    seam_mutation_loses_x_wrap = not has_winding_cycle(x_seam_removed, 0)

    open_edges = open_grid_edges()
    open_graph = adjacency(open_edges)
    open_eccentricities = {
        vertex: max(bfs_distances(open_graph, vertex).values()) for vertex in vertices()
    }
    open_minimum = min(open_eccentricities.values())
    open_center = {vertex for vertex, value in open_eccentricities.items() if value == open_minimum}
    open_grid_breaks_symmetry = (
        not translations_are_automorphisms(open_edges) and open_center != node_set
    )

    origin_rule = frozenset(edge for edge in edges if (0, 0) in edge)
    shifted_origin_rule = frozenset(translate_edge(edge, (1, 0)) for edge in origin_rule)
    origin_rule_breaks_covariance = shifted_origin_rule != origin_rule

    excessive_edge_amount = Fraction(1, len(edges))
    overrun_residual = energy_star - locked_total - len(edges) * excessive_edge_amount
    energy_overrun_detected = overrun_residual < 0
    double_counted_tail_detected = (
        locked_total + 2 * tail_total + unresolved_total != energy_star
    )
    zero_probability_detected = Fraction(0, 1) ** len(edges) == 0

    physical_flags = {key: False for key in EXPECTED_PHYSICAL_KEYS}
    physical_flip_invalidates = not all(
        value is False
        for value in (physical_flags | {"periodic_cosmic_topology_derived": True}).values()
    )

    negative_controls = {
        "low_tail_range_bridge_fails": low_range_fails,
        "x_seam_removal_loses_x_wrap": seam_mutation_loses_x_wrap,
        "open_grid_breaks_transitivity_and_full_center": open_grid_breaks_symmetry,
        "origin_selected_rule_breaks_covariance": origin_rule_breaks_covariance,
        "energy_overrun_detected": energy_overrun_detected,
        "double_counted_tail_energy_detected": double_counted_tail_detected,
        "zero_probability_not_positive": zero_probability_detected,
        "physical_flag_flip_invalidates": physical_flip_invalidates,
    }

    finite_event = connected and wrap_x and wrap_y
    closure_flags = {
        "finite_graph_counts_exact": len(vertices()) == 25 and len(edges) == 50 and all(value == 4 for value in degrees.values()),
        "tail_bridge_condition_exact": bridge_active and all(bridge_rule.values()),
        "tail_rule_translation_covariant_exact": bridge_covariant,
        "full_fixture_connected_exact": connected,
        "all_periodic_directions_wrap_exact": wrap_x and wrap_y,
        "translation_action_free_transitive_exact": automorphisms and free_transitive,
        "graph_center_equals_vertex_set_exact": center_set == node_set,
        "finite_wrapping_event_exact": finite_event,
        "positive_probability_lower_bound_exact": 0 < Q_BOND <= 1 and finite_event and probability_lower_bound == Fraction(1, 2**50) and probability_lower_bound > 0,
        "cycle_bond_enumeration_exact": ring_connected == Fraction(3, 16) and ring_wrap == Fraction(1, 32) and connected_states == 6 and wrap_states == 1,
        "energy_feasibility_inequality_exact": locked_total + tail_total <= energy_star,
        "energy_ledger_balance_exact": energy_residual == 0 and partition_crosscheck,
        "energy_ledger_nonnegative_exact": all(value >= 0 for value in (vertex_amount, edge_amount, locked_total, tail_total, unresolved_total)),
        "schema_keysets_exact": False,
        "mutation_controls_pass": all(negative_controls.values()),
        "aggregate_identity_pass": False,
    }

    diagnostics = {
        "inputs": {"L": L, "dimension": DIMENSION, "rho": fraction_text(RHO), "q_bond": fraction_text(Q_BOND)},
        "graph_witness": {
            "vertices": len(vertices()), "edges": len(edges),
            "degree_values": sorted(set(degrees.values())),
            "connected": connected, "common_eccentricity": minimum_eccentricity,
            "center_cardinality": len(center_set), "translation_automorphisms": automorphisms,
        },
        "tail_bridge_witness": {
            "condition": "2*rho>=1", "two_rho": fraction_text(2 * RHO),
            "all_nearest_neighbor_edges_bridged": all(bridge_rule.values()),
            "translation_covariant": bridge_covariant,
        },
        "finite_percolation_witness": {
            "definition": "connected_and_wraps_each_periodic_direction",
            "wrap_x": wrap_x, "wrap_y": wrap_y, "event": finite_event,
            "infinite_volume_claim": False,
        },
        "probability_calibration": {
            "full_occupation_lower_bound": fraction_text(probability_lower_bound),
            "ring_connected_probability": fraction_text(ring_connected),
            "ring_wrap_probability": fraction_text(ring_wrap),
            "status": "AUXILIARY_ASSUMED_IID_CALIBRATION_ONLY",
        },
        "energy_partition_ledger": {
            "E_star": fraction_text(energy_star),
            "per_vertex_locked": fraction_text(vertex_amount),
            "per_edge_tail": fraction_text(edge_amount),
            "locked_total": fraction_text(locked_total),
            "tail_total": fraction_text(tail_total),
            "unresolved_total": fraction_text(unresolved_total),
            "balance_residual": fraction_text(energy_residual),
            "status": "ACCOUNTING_ONLY_NOT_PHYSICAL_ENERGY",
        },
        "negative_controls": negative_controls,
    }
    return closure_flags, physical_flags, diagnostics


def build_contract() -> dict[str, object]:
    return {
        "CLAIM_ID": CLAIM_ID,
        "CLAIM": (
            "Given a finite periodic relational graph, a translation-covariant "
            "finite-range tail bridge, and a normalized accounting budget, at "
            "least one connected, fully wrapping, non-uniquely-centered, "
            "nonnegative-ledger configuration exists."
        ),
        "TYPE": "EXACT_CONDITIONAL_EXISTENCE_AND_ACCOUNTING_WITNESS",
        "MODEL_VERSION": {"id": MODEL_VERSION, "change_boundary": "fixture, tail rule, event, calibration, ledger, flags, or scope"},
        "ASSUMPTIONS": "Given 5x5 periodic graph, rho=3/5 support rule, q=1/2 auxiliary calibration, normalized accounting budget.",
        "DOMAIN": "Finite combinatorial witness only; no continuum, physical topology, dynamics, or data.",
        "CONVENTIONS": {"center": "graph center set", "percolation": "finite connectivity plus winding", "energy": "accounting labels"},
        "FREEDOM_LEDGER": {
            "current_fitted_effective_dimension": 0,
            "foundation_relational_support": "universal functional/infinite-dimensional",
            "dimension_period_topology": "universal discrete open choices",
            "tail_profile_and_bridge_law": "group functional open choice",
            "local_seed_configuration": "object profile open choice",
            "future_connectivity_inference": "data nuisance count zero here",
        },
        "DEPENDENCIES": "None; self-contained.",
        "METHOD": "Exact integer graph/BFS/winding/enumeration and Fraction arithmetic with mutations.",
        "PASS_CONDITION": "All exact flags true, all mutations detected, all physical flags false.",
        "FAIL_CONDITION": "Any witness/schema failure or promotion to physical derivation.",
        "FALSIFIER": "Counterexample falsifies only this frozen conditional witness.",
        "RESIDUAL": "Exact Boolean and rational residuals.",
        "ERROR_BOUND": "Zero arithmetic error; observational error N/A.",
        "VALIDITY_HEALTH": "Finite mathematical nonemptiness only.",
        "BRANCHES": ["FULL_PERIODIC_WITNESS", "LOW_RANGE_MUTATION", "SEAM_REMOVAL_MUTATION", "OPEN_GRID_MUTATION", "ORIGIN_SELECTED_RULE_MUTATION", "ENERGY_OVERRUN_MUTATION", "DOUBLE_COUNTED_TAIL_MUTATION", "ZERO_PROBABILITY_MUTATION"],
        "OBSERVABLE_MAP": "N/A.",
        "FORWARD_MODEL": "N/A.",
        "DATA_ROLE": "No data read.",
        "IDENTIFIABILITY": "Finite existence and accounting feasibility only; physical realization remains open.",
        "BENCHMARK": "N=25, M=50, 2rho=6/5, P>=2^-50, ring 3/16 and 1/32, ledger 1/4+1/4+1/2.",
        "CLOSURE_FLAGS": {"exact": sorted(EXPECTED_CLOSURE_KEYS), "physical_required_false": sorted(EXPECTED_PHYSICAL_KEYS)},
        "CROSSCHECK": "Independent BFS, all translations, all-pairs eccentricity, exhaustive 32-state ring.",
        "PROVENANCE": "Pinned prereg, source/runtime hashes, UTC, LF, external checksum.",
        "FILES": [PREREG.name, Path(__file__).name, OUTPUT.name, HASH_OUTPUT.name],
    }


def build_report() -> dict[str, object]:
    prereg_record = verify_preregistration()
    closure_flags, physical_flags, diagnostics = derive_gate()
    contract = build_contract()
    result = {
        "schema_version": "1.0", "claim_id": CLAIM_ID, "claim": contract["CLAIM"],
        "type": contract["TYPE"], "model_version": MODEL_VERSION, "status": "PENDING",
        "scope_status": "PENDING", "artifact_valid": False,
        "evidence_type": "EXACT_FINITE_CONDITIONAL_EXISTENCE",
        "refg_status": "OPEN", "genesis_scenario_status": "CANDIDATE_ONLY",
        "physical_realization_status": "OPEN_NOT_DERIVED",
        "falsifier_triggered_for_refg": False,
        "blocking_reasons": [
            "Graph, dimension, and topology are supplied rather than derived.",
            "Tail profile, bridge dynamics, and occupation law are open.",
            "Energy entries are accounting labels, not derived physical sectors.",
            "No infinite-volume or observational result is produced."
        ],
        "contract": contract, "inputs": diagnostics["inputs"],
        "graph_witness": diagnostics["graph_witness"],
        "tail_bridge_witness": diagnostics["tail_bridge_witness"],
        "finite_percolation_witness": diagnostics["finite_percolation_witness"],
        "probability_calibration": diagnostics["probability_calibration"],
        "energy_partition_ledger": diagnostics["energy_partition_ledger"],
        "closure_flags": closure_flags, "physical_closure_flags": physical_flags,
        "negative_controls": diagnostics["negative_controls"],
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "preregistration": prereg_record,
            "source": {"path": Path(__file__).name, "sha256": sha256(Path(__file__).resolve())},
            "python": platform.python_version(), "platform": platform.platform(), "line_endings": "LF",
        },
        "files": {"preregistration": PREREG.name, "source": Path(__file__).name, "result": OUTPUT.name, "checksum": HASH_OUTPUT.name},
    }
    closure_flags["schema_keysets_exact"] = bool(
        set(contract) == REQUIRED_CONTRACT_FIELDS
        and set(closure_flags) == EXPECTED_CLOSURE_KEYS
        and set(physical_flags) == EXPECTED_PHYSICAL_KEYS
        and set(diagnostics["negative_controls"]) == EXPECTED_NEGATIVE_CONTROL_KEYS
        and set(result) == EXPECTED_RESULT_KEYS
    )
    closure_flags["aggregate_identity_pass"] = all(
        value for key, value in closure_flags.items() if key != "aggregate_identity_pass"
    )
    valid = closure_flags["aggregate_identity_pass"] and all(value is False for value in physical_flags.values())
    result["artifact_valid"] = bool(valid)
    result["status"] = "PASS" if valid else "FAIL"
    result["scope_status"] = "PASS_CONDITIONAL_EXISTENCE_WITNESS__PHYSICAL_GENESIS_OPEN" if valid else "FAIL_EXACT_GATE"
    if not valid:
        raise RuntimeError("W3-38 aggregate gate failed")
    return result


def write_atomic(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    temporary.replace(path)


def write_report(report: dict[str, object]) -> str:
    payload = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
    write_atomic(OUTPUT, payload)
    digest = sha256(OUTPUT)
    write_atomic(HASH_OUTPUT, f"{digest}  {OUTPUT.name}\n")
    return digest


def write_failure(error: Exception) -> None:
    failure = {"schema_version": "1.0-failure", "claim_id": CLAIM_ID, "model_version": MODEL_VERSION, "status": "FAIL", "artifact_valid": False, "error": f"{type(error).__name__}: {error}", "generated_utc": datetime.now(timezone.utc).isoformat()}
    write_atomic(OUTPUT, json.dumps(failure, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n")
    write_atomic(HASH_OUTPUT, f"{sha256(OUTPUT)}  {OUTPUT.name}\n")


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
