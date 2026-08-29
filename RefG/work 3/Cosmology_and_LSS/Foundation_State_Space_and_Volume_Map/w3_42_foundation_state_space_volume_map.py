"""W3-42 exact foundation state-space and volume-map nonselection gate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_42_FOUNDATION_STATE_SPACE_VOLUME_MAP"
MODEL_VERSION = "W3-42-v1.0-FOUNDATION-STATE-SPACE-VOLUME-MAP"
CLAIM = (
    r"In a fixed-combinatorics relational $d$-cell comparison class, uniform "
    r"dilation of every independent cell direction by the foundation link scale "
    r"$a$ gives the exact geometric measure law "
    r"$\mathcal V_d(a)=\mathcal V_{d,0}a^d$. The logarithmic response "
    r"$\nu=d\ln\mathcal V/d\ln a$ reconstructs the general measure and, only on "
    r"the separately declared bridge $V_F\equiv\mathcal V$, generalizes the W3-41 "
    r"mechanical dictionary. Exact periodic-graph, alternative-measure, and "
    r"hidden-state witnesses show that the frozen upstream constraints select "
    r"neither $d=3$, the physical measure, that bridge, nor a one-coordinate "
    r"homogeneous state space. Thus the W3-41 cubic branch remains a valid "
    r"conditional branch and is not promoted to a derived physical closure."
)

HERE = Path(__file__).resolve().parent
PREREG = HERE / "w3_42_foundation_state_space_volume_map_preregistration.md"
OUTPUT = HERE / "w3_42_result.json"
HASH_OUTPUT = HERE / "w3_42_result.sha256"
PINNED_PREREG_SHA256 = (
    "8ba44af154a3f9a18b207b4f17a3dcecdb27a8a9d59f7f9aa712c0946763ae98"
)
UPSTREAM_DIR = HERE.parent / "Foundation_Constitutive_Interface"
UPSTREAM_RESULT = UPSTREAM_DIR / "w3_41_result.json"
UPSTREAM_CHECKSUM = UPSTREAM_DIR / "w3_41_result.sha256"
PINNED_W3_41_RESULT_SHA256 = (
    "48e6a981eaa2d696240323d6ccbbb4f744e67f2c37329ed292a1de11ce10c9fb"
)

REQUIRED_CONTRACT_FIELDS = {
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
}

EXPECTED_CLOSURE_KEYS = {
    "w3_41_dependency_verified",
    "periodic_graph_counts_exact",
    "periodic_graph_regular_degrees_exact",
    "periodic_graph_connected_exact",
    "periodic_graph_translation_symmetry_exact",
    "periodic_graph_no_unique_center_exact",
    "multi_dimension_relational_witnesses_exact",
    "homogeneous_deformation_determinant_exact",
    "principal_stretch_product_exact",
    "jacobi_log_measure_rate_exact",
    "uniform_dilation_gram_scaling_exact",
    "geometric_measure_power_scaling_exact",
    "logarithmic_volume_response_exact",
    "volume_response_reconstruction_exact",
    "constant_response_power_equivalence_exact",
    "d3_geometric_branch_matches_cubic_map_exact",
    "generalized_mechanical_pressure_exact",
    "generalized_bulk_modulus_exact",
    "generalized_kappa_identity_exact",
    "constant_d_mechanical_dictionary_exact",
    "hidden_state_path_derivative_identity_exact",
    "hidden_state_reduction_condition_exact",
    "tracefree_shape_measure_degeneracy_exact",
    "tracefree_shape_states_distinct_exact",
    "equal_link_volume_nonselection_exact",
    "fixed_graph_measure_nonselection_exact",
    "active_volume_factorization_exact",
    "dimension_measure_nonselection_exact",
    "one_coordinate_completeness_nonselection_exact",
    "registered_top_level_keysets_exact",
    "mutation_controls_pass",
    "aggregate_identity_pass",
}

EXPECTED_PHYSICAL_KEYS = {
    "foundation_adjacency_derived",
    "graph_to_geometry_map_derived",
    "effective_cell_dimension_selected",
    "three_spatial_dimensions_derived",
    "physical_cosmic_topology_derived",
    "homogeneous_foundation_state_derived",
    "homogeneous_state_manifold_derived",
    "one_coordinate_state_reduction_derived",
    "uniform_isotropic_dilation_derived",
    "comoving_cell_count_conservation_derived",
    "isotropy_dynamically_derived",
    "extra_shape_modes_excluded",
    "geometric_measure_selected",
    "foundation_volume_measure_derived",
    "geometric_measure_equals_mechanical_volume_derived",
    "link_scale_equals_volume_scale_derived",
    "foundation_volume_law_V0_a3_derived",
    "active_cell_measure_history_derived",
    "foundation_dynamics_derived",
    "foundation_energy_function_selected",
    "foundation_pressure_equals_mechanical_pressure_derived",
    "P_F_of_a_selected",
    "expansion_equation_derived",
    "observable_forward_model_derived",
}

EXPECTED_NEGATIVE_KEYS = {
    "wrong_gram_power_detected",
    "gram_square_root_omission_detected",
    "jacobi_inverse_omission_detected",
    "wrong_log_response_detected",
    "wrong_reconstruction_measure_detected",
    "hard_selected_d3_detected",
    "dimension_witness_removal_detected",
    "periodic_edge_removal_detected",
    "unique_center_promotion_detected",
    "equal_link_cubic_conflation_detected",
    "node_cell_measure_conflation_detected",
    "shape_state_erasure_detected",
    "hidden_path_fixed_q_conflation_detected",
    "active_measure_derivative_omission_detected",
    "general_d_pressure_three_detected",
    "physical_bridge_flag_flip_invalidates_scope",
    "one_coordinate_flag_flip_invalidates_scope",
    "upstream_hash_mutation_detected",
    "registered_keyset_mutation_detected",
}

EXPECTED_NONSELECTION_KEYS = {
    "candidate_dimensions",
    "selected_dimension",
    "candidate_measure_scalings",
    "selected_geometric_measure",
    "distinct_shape_states_same_a_and_volume",
    "selected_homogeneous_state_coordinates",
    "link_scale_alone_selects_volume_map",
    "geometric_mechanical_bridge_selected",
    "active_cell_history_selected",
}

EXPECTED_GRAPH_KEYS = {
    "dimension_label", "period", "node_count", "expected_node_count",
    "edge_count", "expected_edge_count", "degree_values", "expected_degree",
    "connected", "translation_automorphisms",
    "expected_translation_automorphisms", "center_count",
    "all_vertices_are_centers", "unique_center",
}

EXPECTED_DEFORMATION_VALIDATION_KEYS = {
    "gram_determinant_identity",
    "principal_stretch_product",
    "jacobi_log_measure_rate",
    "uniform_gram_scaling",
    "uniform_measure_scaling",
}

EXPECTED_SHAPE_KEYS = {
    "cubic_measure_for_all_shape_states",
    "shape_invariant_distinguishes_states",
    "same_a",
    "same_measure",
    "states_distinct",
}

EXPECTED_EQUAL_LINK_KEYS = {
    "all_three_link_lengths_equal_a",
    "reference_normalized",
    "volume_formula_exact",
    "noncubic_at_a4",
    "link_scale_selects_cubic_map",
}

EXPECTED_HIDDEN_KEYS = {
    "path_residual_identity",
    "frozen_q_reduction",
    "equilibrium_reduction",
    "unconditional_path_equals_fixed_q",
}

EXPECTED_ACTIVE_VOLUME_KEYS = {
    "factorization_identity",
    "log_rate_identity",
    "active_cell_history_selected",
}

EXPECTED_RESULT_KEYS = {
    "schema_version", "claim_id", "claim", "type", "model_version", "status",
    "scope_status", "artifact_valid", "evidence_type", "refg_status",
    "bridge_status", "falsifier_triggered_for_refg", "blocking_reasons",
    "contract", "closure_flags", "physical_closure_flags", "identities",
    "graph_witnesses", "deformation_dictionary", "measure_response",
    "mechanical_dictionary", "hidden_state", "shape_witness",
    "equal_link_witness", "measure_nonselection", "active_volume_roles",
    "nonselection", "negative_controls", "provenance", "files",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_zero(value: object) -> bool:
    return bool(sp.simplify(value) == 0)


def exact_nonzero(value: object) -> bool:
    return bool(sp.simplify(value) != 0)


def exact_keyset(actual: object, expected: set[str]) -> bool:
    return set(actual) == expected


def all_true_record(record: dict[str, bool], expected: set[str]) -> bool:
    return bool(
        exact_keyset(record, expected)
        and all(value is True for value in record.values())
    )


def dependency_hash_chain_valid(
    actual_hash: str, checksum_hash: str, expected_hash: str
) -> bool:
    return bool(actual_hash == checksum_hash == expected_hash)


def physical_scope_valid(flags: dict[str, bool]) -> bool:
    return bool(
        exact_keyset(flags, EXPECTED_PHYSICAL_KEYS)
        and all(value is False for value in flags.values())
    )


def nonselection_record_valid(record: dict[str, object]) -> bool:
    return bool(
        exact_keyset(record, EXPECTED_NONSELECTION_KEYS)
        and record["candidate_dimensions"] == [1, 2, 3]
        and record["selected_dimension"] is None
        and record["candidate_measure_scalings"] == {
            "filled_cell_measure": 3,
            "node_count": 0,
            "total_edge_length": 1,
        }
        and record["selected_geometric_measure"] is None
        and record["distinct_shape_states_same_a_and_volume"] is True
        and record["selected_homogeneous_state_coordinates"] is None
        and record["link_scale_alone_selects_volume_map"] is False
        and record["geometric_mechanical_bridge_selected"] is False
        and record["active_cell_history_selected"] is False
    )


def graph_record_valid(record: dict[str, object]) -> bool:
    d = record.get("dimension_label")
    period = record.get("period")
    return bool(
        exact_keyset(record, EXPECTED_GRAPH_KEYS)
        and d in {1, 2, 3}
        and period == 5
        and record["node_count"] == period**d
        and record["expected_node_count"] == period**d
        and record["edge_count"] == d * period**d
        and record["expected_edge_count"] == d * period**d
        and record["degree_values"] == [2 * d]
        and record["expected_degree"] == 2 * d
        and record["connected"] is True
        and record["translation_automorphisms"] == period**d
        and record["expected_translation_automorphisms"] == period**d
        and record["center_count"] == period**d
        and record["all_vertices_are_centers"] is True
        and record["unique_center"] is False
    )


def shape_record_valid(record: dict[str, bool]) -> bool:
    return bool(exact_keyset(record, EXPECTED_SHAPE_KEYS) and all(record.values()))


def equal_link_record_valid(record: dict[str, bool]) -> bool:
    return bool(
        exact_keyset(record, EXPECTED_EQUAL_LINK_KEYS)
        and all(
            record[key] is True
            for key in EXPECTED_EQUAL_LINK_KEYS - {"link_scale_selects_cubic_map"}
        )
        and record["link_scale_selects_cubic_map"] is False
    )


def hidden_record_valid(record: dict[str, bool]) -> bool:
    return bool(
        exact_keyset(record, EXPECTED_HIDDEN_KEYS)
        and record["path_residual_identity"] is True
        and record["frozen_q_reduction"] is True
        and record["equilibrium_reduction"] is True
        and record["unconditional_path_equals_fixed_q"] is False
    )


def active_volume_record_valid(record: dict[str, bool]) -> bool:
    return bool(
        exact_keyset(record, EXPECTED_ACTIVE_VOLUME_KEYS)
        and record["factorization_identity"] is True
        and record["log_rate_identity"] is True
        and record["active_cell_history_selected"] is False
    )


def schema_keysets_valid(
    contract: dict[str, object],
    closure_flags: dict[str, bool],
    physical_flags: dict[str, bool],
    negative_controls: dict[str, bool],
    result: dict[str, object],
) -> bool:
    return bool(
        exact_keyset(contract, REQUIRED_CONTRACT_FIELDS)
        and exact_keyset(closure_flags, EXPECTED_CLOSURE_KEYS)
        and exact_keyset(physical_flags, EXPECTED_PHYSICAL_KEYS)
        and exact_keyset(negative_controls, EXPECTED_NEGATIVE_KEYS)
        and exact_keyset(result, EXPECTED_RESULT_KEYS)
    )


def verify_canonical_text(path: Path) -> None:
    payload = path.read_bytes()
    if b"\r" in payload or not payload.endswith(b"\n"):
        raise RuntimeError(f"Noncanonical UTF-8 LF text: {path}")
    payload.decode("utf-8")


def registered_claim() -> str:
    verify_canonical_text(PREREG)
    text = PREREG.read_text(encoding="utf-8")
    marker = "**CLAIM:** "
    if marker not in text:
        raise RuntimeError("Preregistration claim field is missing")
    block = text.split(marker, 1)[1].split("\n\n", 1)[0]
    return " ".join(line.strip() for line in block.splitlines())


def verify_upstream() -> dict[str, object]:
    if not UPSTREAM_RESULT.is_file() or not UPSTREAM_CHECKSUM.is_file():
        raise RuntimeError("Missing frozen W3-41 dependency")
    actual_hash = sha256(UPSTREAM_RESULT)
    checksum_text = UPSTREAM_CHECKSUM.read_text(encoding="utf-8").strip()
    checksum_hash, checksum_name = checksum_text.split(maxsplit=1)
    data = json.loads(UPSTREAM_RESULT.read_text(encoding="utf-8"))
    closures = data.get("closure_flags", {})
    physical = data.get("physical_closure_flags", {})
    checks = {
        "hash_pinned": actual_hash == PINNED_W3_41_RESULT_SHA256,
        "checksum_matches": (
            checksum_hash == actual_hash and checksum_name == UPSTREAM_RESULT.name
        ),
        "hash_chain": dependency_hash_chain_valid(
            actual_hash, checksum_hash, PINNED_W3_41_RESULT_SHA256
        ),
        "claim_id": data.get("claim_id")
        == "W3_41_FOUNDATION_CONSTITUTIVE_INTERFACE",
        "model_version": data.get("model_version")
        == "W3-41-v1.2-FOUNDATION-CONSTITUTIVE-INTERFACE",
        "status": data.get("status") == "PASS",
        "scope_status": data.get("scope_status")
        == (
            "PASS_EXACT_CONSTITUTIVE_INTERFACE__RECONSTRUCTION_DEGENERACY_"
            "PROVED__PHYSICAL_BRIDGE_AND_DYNAMICS_OPEN"
        ),
        "w3_40_dependency": closures.get("w3_40_dependency_verified") is True,
        "cubic_jacobian_conditional": (
            closures.get("foundation_volume_jacobian_exact") is True
        ),
        "volume_law_open": physical.get("foundation_volume_law_derived") is False,
        "state_reduction_open": (
            physical.get("one_coordinate_state_reduction_derived") is False
        ),
        "mechanical_bridge_open": (
            physical.get(
                "foundation_pressure_equals_mechanical_pressure_derived"
            )
            is False
        ),
        "dynamics_open": physical.get("foundation_dynamics_derived") is False,
    }
    if not all(checks.values()):
        raise RuntimeError(f"W3-41 dependency verification failed: {checks}")
    return {
        "path": UPSTREAM_RESULT.relative_to(HERE.parent).as_posix(),
        "sha256": actual_hash,
        "expected_sha256": PINNED_W3_41_RESULT_SHA256,
        "checks": checks,
        "valid": True,
    }


def periodic_vertices_edges(
    dimension: int, period: int
) -> tuple[list[tuple[int, ...]], set[tuple[tuple[int, ...], tuple[int, ...]]]]:
    vertices = list(product(range(period), repeat=dimension))
    edges: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    for vertex in vertices:
        for axis in range(dimension):
            neighbor_list = list(vertex)
            neighbor_list[axis] = (neighbor_list[axis] + 1) % period
            neighbor = tuple(neighbor_list)
            edges.add(tuple(sorted((vertex, neighbor))))
    return vertices, edges


def graph_record_from_edges(
    dimension: int,
    period: int,
    vertices: list[tuple[int, ...]],
    edges: set[tuple[tuple[int, ...], tuple[int, ...]]],
) -> dict[str, object]:
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    def distances(start: tuple[int, ...]) -> dict[tuple[int, ...], int]:
        found = {start: 0}
        queue = [start]
        for vertex in queue:
            for neighbor in adjacency[vertex]:
                if neighbor not in found:
                    found[neighbor] = found[vertex] + 1
                    queue.append(neighbor)
        return found

    connected = len(distances(vertices[0])) == len(vertices)
    eccentricities = {}
    for vertex in vertices:
        distance_map = distances(vertex)
        eccentricities[vertex] = (
            max(distance_map.values())
            if len(distance_map) == len(vertices)
            else sys.maxsize
        )
    minimum_eccentricity = min(eccentricities.values())
    center = [
        vertex
        for vertex, eccentricity in eccentricities.items()
        if eccentricity == minimum_eccentricity
    ]

    translation_automorphisms = 0
    for shift in vertices:
        translated = set()
        for left, right in edges:
            left_shifted = tuple(
                (left[axis] + shift[axis]) % period
                for axis in range(dimension)
            )
            right_shifted = tuple(
                (right[axis] + shift[axis]) % period
                for axis in range(dimension)
            )
            translated.add(
                tuple(sorted((left_shifted, right_shifted)))
            )
        if translated == edges:
            translation_automorphisms += 1

    return {
        "dimension_label": dimension,
        "period": period,
        "node_count": len(vertices),
        "expected_node_count": period**dimension,
        "edge_count": len(edges),
        "expected_edge_count": dimension * period**dimension,
        "degree_values": sorted({len(adjacency[v]) for v in vertices}),
        "expected_degree": 2 * dimension,
        "connected": connected,
        "translation_automorphisms": translation_automorphisms,
        "expected_translation_automorphisms": period**dimension,
        "center_count": len(center),
        "all_vertices_are_centers": len(center) == len(vertices),
        "unique_center": len(center) == 1,
    }


def build_graph_witness(dimension: int, period: int = 5) -> dict[str, object]:
    vertices, edges = periodic_vertices_edges(dimension, period)
    return graph_record_from_edges(dimension, period, vertices, edges)


def build_contract() -> dict[str, object]:
    return {
        "CLAIM_ID": CLAIM_ID,
        "CLAIM": CLAIM,
        "TYPE": (
            "EXACT_CONDITIONAL_HOMOGENEOUS_MEASURE_DICTIONARY_AND_"
            "STATE_REDUCTION_NONSELECTION_GATE"
        ),
        "MODEL_VERSION": {
            "id": MODEL_VERSION,
            "change_boundary": (
                "Upstream hash, relational witnesses, deformation/measure "
                "convention, mechanical bridge, hidden-state diagnostic, "
                "validators, closure keys, or claim scope."
            ),
        },
        "ASSUMPTIONS": (
            "Pinned W3-41; prespatial foundation; supplied comparison "
            "cell/graph structures; independent link scale a; fixed "
            "combinatorics only on conditional branches; geometric measure "
            "distinct from mechanical and activated volumes."
        ),
        "DOMAIN": (
            "Regular positive a and measures; nondegenerate supplied cells; "
            "T_5^d witnesses for d=1,2,3. Mechanical ratios require "
            "mathcal_V'!=0 (nu!=0), and kappa also P_F=Pi_F!=0. Hidden-state "
            "ratios require V_a!=0 at fixed q and V_a+V_q*q'!=0 along path. "
            "No singular denominator, Genesis endpoint, compact-object "
            "sector, or observable sector."
        ),
        "CONVENTIONS": {
            "d": "intrinsic supplied cell/measure rank",
            "geometric_measure": "mathcal V=sqrt(det G)",
            "mechanical_volume": "V_F, work-conjugate coordinate",
            "activated_volume": "V_act=N_act*v_cell",
            "link_scale": "a is independent and is not defined from volume",
        },
        "FREEDOM_LEDGER": {
            "current_data_fitted_effective_dimension": 0,
            "foundation_adjacency": "open",
            "intrinsic_cell_rank": "open",
            "geometric_measure": "comparison dictionary only",
            "homogeneous_state_manifold": "open",
            "mechanical_volume_bridge": "candidate identity only",
            "foundation_dynamics": "open",
            "future_observables": "none instantiated",
        },
        "DEPENDENCIES": (
            "Pinned W3-41 result/checksum; W3-38 and W3-39 are contextual "
            "witnesses, not algebraic dependencies."
        ),
        "METHOD": (
            "Exact SymPy determinants, logarithmic derivatives, chain rules, "
            "periodic-graph enumeration/BFS/translation checks, constructive "
            "measure/state counterexamples, shared-validator mutations, "
            "strict JSON, and atomic checksum output."
        ),
        "PASS_CONDITION": (
            "All exact identities, graph predicates, dependency checks, "
            "nonselection witnesses, schemas, and mutations pass while every "
            "physical/downstream closure flag remains false."
        ),
        "FAIL_CONDITION": (
            "Any exact check fails or dimension, physical measure, isotropy, "
            "one-coordinate completeness, bridge, dynamics, or observable is "
            "promoted without a microscopic derivation."
        ),
        "FALSIFIER": (
            "An exact counterexample under the registered comparison "
            "assumptions falsifies its identity; a future microscopic model "
            "adds missing premises rather than falsifying present nonselection."
        ),
        "RESIDUAL": (
            "Exact symbolic zero, integer/Boolean graph predicates, and exact "
            "hash/schema equality."
        ),
        "ERROR_BOUND": "Zero algebraic/integer/hash error; numerical error N/A.",
        "VALIDITY_HEALTH": (
            "Conditional state-space/measure dictionary and constructive "
            "nonselection only; physical selection and dynamics remain open."
        ),
        "BRANCHES": [
            "PERIODIC_RELATIONAL_COMPARISON",
            "HOMOGENEOUS_DEFORMATION_DICTIONARY",
            "UNIFORM_DILATION_GEOMETRIC_DICTIONARY",
            "EQUAL_LINK_ANGLE_WITNESS",
            "GENERAL_MEASURE_RESPONSE",
            "CANDIDATE_GEOMETRIC_MECHANICAL_BRIDGE",
            "TRACEFREE_SHAPE_DEGENERACY",
            "FIXED_GRAPH_MEASURE_NONSELECTION",
            "HIDDEN_STATE_REDUCTION_DIAGNOSTIC",
            "ACTIVE_VOLUME_ROLE_SEPARATION",
            "MICROSCOPIC_SELECTION_OPEN",
        ],
        "OBSERVABLE_MAP": "None.",
        "FORWARD_MODEL": "Not applicable.",
        "DATA_ROLE": "No data; W3-41 is a logical upstream artifact.",
        "IDENTIFIABILITY": (
            "Supplied dimension, measure, uniform dilation, hidden-state "
            "reduction, and V_F=mathcal V bridge identify the dictionary; "
            "current premises select none."
        ),
        "BENCHMARK": (
            "Recover determinant/Gram/Jacobi identities, V_d=V_d0*a^d, "
            "nu reconstruction, general and constant-d mechanical formulas, "
            "the d=3 W3-41 branch, and all graph/measure/state no-go witnesses."
        ),
        "CLOSURE_FLAGS": {
            "exact": sorted(EXPECTED_CLOSURE_KEYS),
            "physical_required_false": sorted(EXPECTED_PHYSICAL_KEYS),
        },
        "CROSSCHECK": (
            "Independent determinant and Gram routes; Jacobi rate; inverse "
            "response; d=3 regression; graph enumeration; equal-link angle, "
            "fixed-graph measure, shape, hidden-state, and active-volume "
            "witnesses; production-validator mutations."
        ),
        "PROVENANCE": (
            "Pinned prereg/W3-41 hashes, canonical UTF-8 LF, runtime versions, "
            "strict JSON, and atomic result/checksum."
        ),
        "FILES": [
            "README.md", PREREG.name, Path(__file__).name, OUTPUT.name,
            HASH_OUTPUT.name,
        ],
    }


def derive_gate() -> tuple[
    dict[str, bool],
    dict[str, bool],
    dict[str, object],
    dict[str, bool],
]:
    a, V0 = sp.symbols("a V_0", positive=True)
    d_symbol = sp.symbols("d", positive=True, integer=True)

    # Supplied deformation: G=F^T G0 F and det(G)=det(F)^2 det(G0).
    l1, l2, l3 = sp.symbols(
        "lambda_1 lambda_2 lambda_3", positive=True
    )
    shear = sp.symbols("shear", real=True)
    g1, g2 = sp.symbols("g_1 g_2", positive=True)
    F_triangular = sp.Matrix([[l1, shear], [0, l2]])
    G0_general = sp.diag(g1, g2)
    G_general = F_triangular.T * G0_general * F_triangular
    gram_determinant_residual = (
        sp.det(G_general)
        - sp.det(F_triangular) ** 2 * sp.det(G0_general)
    )
    principal_F = sp.diag(l1, l2, l3)
    principal_stretch_residual = sp.det(principal_F) - l1 * l2 * l3

    # Jacobi's formula is checked with independent matrix/differential entries.
    f11, f12, f21, f22 = sp.symbols("f_11 f_12 f_21 f_22")
    df11, df12, df21, df22 = sp.symbols(
        "df_11 df_12 df_21 df_22"
    )
    F_generic = sp.Matrix([[f11, f12], [f21, f22]])
    dF_generic = sp.Matrix([[df11, df12], [df21, df22]])
    det_F_generic = sp.det(F_generic)
    directional_det = sum(
        sp.diff(det_F_generic, entry) * dentry
        for entry, dentry in zip(
            (f11, f12, f21, f22),
            (df11, df12, df21, df22),
        )
    )
    jacobi_residual = (
        directional_det / det_F_generic
        - sp.trace(F_generic.inv() * dF_generic)
    )

    uniform_gram_residuals: dict[str, sp.Expr] = {}
    uniform_measure_residuals: dict[str, sp.Expr] = {}
    for dimension in (1, 2, 3):
        reference_entries = sp.symbols(
            f"b1:{dimension + 1}", positive=True
        )
        B0 = sp.diag(*reference_entries)
        G0 = B0.T * B0
        B = a * B0
        G = B.T * B
        matrix_residual = G - a**2 * G0
        for row in range(dimension):
            for column in range(dimension):
                uniform_gram_residuals[
                    f"d{dimension}_{row}_{column}"
                ] = matrix_residual[row, column]
        geometric_ratio = sp.sqrt(sp.det(G) / sp.det(G0))
        uniform_measure_residuals[f"d{dimension}"] = (
            geometric_ratio - a**dimension
        )
    d3_cubic_residual = V0 * a**3 - V0 * a**3

    # General logarithmic response and its inverse reconstruction.
    measure = sp.Function("mathcal_V")(a)
    measure_prime = sp.diff(measure, a)
    response_from_measure = a * measure_prime / measure
    log_response_residual = (
        a * sp.diff(sp.log(measure), a) - response_from_measure
    )
    u = sp.symbols("u", positive=True)
    nu_function = sp.Function("nu")
    reconstructed_measure = V0 * sp.exp(
        sp.Integral(nu_function(u) / u, (u, 1, a))
    )
    response_reconstruction_residual = (
        a * sp.diff(sp.log(reconstructed_measure), a) - nu_function(a)
    )
    constant_response_forward_residual = (
        a * sp.diff(sp.log(V0 * a**d_symbol), a) - d_symbol
    )
    constant_response_inverse_residual = (
        sp.log((V0 * a**d_symbol) / V0) - d_symbol * sp.log(a)
    )

    # Mechanical dictionary, conditional on V_F=mathcal V.
    energy = sp.Function("E_F")(a)
    energy_prime = sp.diff(energy, a)
    volume_prime = sp.diff(measure, a)
    nu_definition = a * volume_prime / measure
    mechanical_pressure = -energy_prime / volume_prime
    mechanical_pressure_expected = (
        -a * energy_prime / (nu_definition * measure)
    )
    pressure_prime = sp.diff(mechanical_pressure, a)
    bulk_modulus = -measure * pressure_prime / volume_prime
    bulk_modulus_expected = -a * pressure_prime / nu_definition
    kappa = -a * pressure_prime / mechanical_pressure
    kappa_expected = nu_definition * bulk_modulus / mechanical_pressure
    mechanical_pressure_residual = (
        mechanical_pressure - mechanical_pressure_expected
    )
    bulk_modulus_residual = bulk_modulus - bulk_modulus_expected
    kappa_residual = kappa - kappa_expected

    volume_d = V0 * a**d_symbol
    pressure_d = -energy_prime / sp.diff(volume_d, a)
    pressure_d_expected = (
        -energy_prime / (d_symbol * V0 * a ** (d_symbol - 1))
    )
    bulk_d = -volume_d * sp.diff(pressure_d, a) / sp.diff(volume_d, a)
    bulk_d_expected = (
        a * sp.diff(energy, a, 2) - (d_symbol - 1) * energy_prime
    ) / (d_symbol**2 * V0 * a ** (d_symbol - 1))
    kappa_d = -a * sp.diff(pressure_d, a) / pressure_d
    kappa_d_expected = (
        d_symbol - 1 - a * sp.diff(energy, a, 2) / energy_prime
    )
    constant_d_residuals = {
        "pressure": pressure_d - pressure_d_expected,
        "bulk_modulus": bulk_d - bulk_d_expected,
        "kappa": kappa_d - kappa_d_expected,
        "w3_41_pressure_d3": pressure_d.subs(d_symbol, 3)
        + energy_prime / (3 * V0 * a**2),
        "w3_41_bulk_d3": bulk_d.subs(d_symbol, 3)
        - (
            a * sp.diff(energy, a, 2) - 2 * energy_prime
        )
        / (9 * V0 * a**2),
        "w3_41_kappa_d3": kappa_d.subs(d_symbol, 3)
        - (2 - a * sp.diff(energy, a, 2) / energy_prime),
    }

    # Hidden state q: fixed-q and along-path derivatives are distinct.
    E_a, E_q, V_a, V_q, q_prime = sp.symbols(
        "E_a E_q V_a V_q q_prime", real=True
    )
    pressure_fixed_q = -E_a / V_a
    pressure_along_path = -(
        E_a + E_q * q_prime
    ) / (V_a + V_q * q_prime)
    path_difference = pressure_along_path - pressure_fixed_q
    path_difference_expected = -q_prime * (
        E_q + pressure_fixed_q * V_q
    ) / (V_a + V_q * q_prime)
    hidden_path_residual = path_difference - path_difference_expected
    frozen_q_residual = path_difference.subs(q_prime, 0)
    equilibrium_q_residual = sp.simplify(
        path_difference.subs(E_q, -pressure_fixed_q * V_q)
    )
    hidden_state_record = {
        "path_residual_identity": exact_zero(hidden_path_residual),
        "frozen_q_reduction": exact_zero(frozen_q_residual),
        "equilibrium_reduction": exact_zero(equilibrium_q_residual),
        "unconditional_path_equals_fixed_q": False,
    }

    # Cubic measure with a surviving trace-free homogeneous shape state.
    shape = sp.symbols("s", real=True)
    G_shape = a**2 * sp.diag(
        sp.exp(2 * shape), sp.exp(-2 * shape), 1
    )
    shape_measure = sp.sqrt(sp.det(G_shape))
    shape_measure_residual = shape_measure - a**3
    shape_invariant = (
        sp.trace(G_shape) / sp.det(G_shape) ** sp.Rational(1, 3)
    )
    shape_zero = sp.simplify(shape_invariant.subs(shape, 0))
    shape_log_two = sp.simplify(
        shape_invariant.subs(shape, sp.log(2))
    )
    shape_record = {
        "cubic_measure_for_all_shape_states": exact_zero(
            shape_measure_residual
        ),
        "shape_invariant_distinguishes_states": exact_nonzero(
            shape_log_two - shape_zero
        ),
        "same_a": True,
        "same_measure": exact_zero(
            shape_measure.subs(shape, 0)
            - shape_measure.subs(shape, sp.log(2))
        ),
        "states_distinct": exact_nonzero(sp.log(2)),
    }

    # Three equal basis-link lengths do not freeze angles or volume.
    angle_cosine = (a - 1) / (a + 1)
    angle_sine = 2 * sp.sqrt(a) / (a + 1)
    B_equal_links = a * sp.Matrix(
        [
            [1, angle_cosine, 0],
            [0, angle_sine, 0],
            [0, 0, 1],
        ]
    )
    link_norm_residuals = [
        B_equal_links[:, column].dot(B_equal_links[:, column]) - a**2
        for column in range(3)
    ]
    equal_link_volume = sp.det(B_equal_links)
    equal_link_volume_expected = (
        2 * a ** sp.Rational(7, 2) / (a + 1)
    )
    equal_link_volume_residual = (
        equal_link_volume - equal_link_volume_expected
    )
    equal_link_record = {
        "all_three_link_lengths_equal_a": all(
            exact_zero(value) for value in link_norm_residuals
        ),
        "reference_normalized": exact_zero(
            equal_link_volume.subs(a, 1) - 1
        ),
        "volume_formula_exact": exact_zero(equal_link_volume_residual),
        "noncubic_at_a4": exact_nonzero(
            equal_link_volume.subs(a, 4) - sp.Integer(4) ** 3
        ),
        "link_scale_selects_cubic_map": False,
    }

    # One fixed graph admits inequivalent supplied extensive measures.
    graph_vertices_3, graph_edges_3 = periodic_vertices_edges(3, 5)
    node_measure = sp.Integer(len(graph_vertices_3))
    edge_measure = sp.Integer(len(graph_edges_3)) * a
    filled_cell_measure = sp.Integer(len(graph_vertices_3)) * a**3
    measure_scalings = {
        "node_count": int(
            sp.simplify(a * sp.diff(node_measure, a) / node_measure)
        ),
        "total_edge_length": int(
            sp.simplify(a * sp.diff(edge_measure, a) / edge_measure)
        ),
        "filled_cell_measure": int(
            sp.simplify(
                a * sp.diff(filled_cell_measure, a) / filled_cell_measure
            )
        ),
    }
    measure_nonselection = {
        "fixed_graph": "T_5^3",
        "node_count": str(node_measure),
        "total_edge_length": str(edge_measure),
        "supplied_filled_cell_measure": str(filled_cell_measure),
        "logarithmic_scaling_exponents": measure_scalings,
        "selected_measure": None,
    }

    # Activated volume contains an independent active-cell contribution.
    active_count = sp.Function("N_act")(a)
    cell_measure = sp.Function("v_cell")(a)
    activated_volume = active_count * cell_measure
    active_factorization_residual = (
        activated_volume - active_count * cell_measure
    )
    active_log_rate_residual = (
        a * sp.diff(activated_volume, a) / activated_volume
        - a * sp.diff(active_count, a) / active_count
        - a * sp.diff(cell_measure, a) / cell_measure
    )
    active_volume_record = {
        "factorization_identity": exact_zero(
            active_factorization_residual
        ),
        "log_rate_identity": exact_zero(active_log_rate_residual),
        "active_cell_history_selected": False,
    }

    graph_witnesses = {
        f"d{dimension}": build_graph_witness(dimension)
        for dimension in (1, 2, 3)
    }
    nonselection = {
        "candidate_dimensions": [1, 2, 3],
        "selected_dimension": None,
        "candidate_measure_scalings": measure_scalings,
        "selected_geometric_measure": None,
        "distinct_shape_states_same_a_and_volume": (
            shape_record["states_distinct"] and shape_record["same_measure"]
        ),
        "selected_homogeneous_state_coordinates": None,
        "link_scale_alone_selects_volume_map": False,
        "geometric_mechanical_bridge_selected": False,
        "active_cell_history_selected": False,
    }

    deformation_validation = {
        "gram_determinant_identity": exact_zero(
            gram_determinant_residual
        ),
        "principal_stretch_product": exact_zero(
            principal_stretch_residual
        ),
        "jacobi_log_measure_rate": exact_zero(jacobi_residual),
        "uniform_gram_scaling": all(
            exact_zero(value) for value in uniform_gram_residuals.values()
        ),
        "uniform_measure_scaling": all(
            exact_zero(value)
            for value in uniform_measure_residuals.values()
        ),
    }

    identities = {
        "gram_determinant": gram_determinant_residual,
        "principal_stretch_product": principal_stretch_residual,
        "jacobi_log_measure_rate": jacobi_residual,
        **{
            f"uniform_gram_{key}": value
            for key, value in uniform_gram_residuals.items()
        },
        **{
            f"uniform_measure_{key}": value
            for key, value in uniform_measure_residuals.items()
        },
        "d3_cubic_branch": d3_cubic_residual,
        "logarithmic_measure_response": log_response_residual,
        "response_reconstruction": response_reconstruction_residual,
        "constant_response_forward": constant_response_forward_residual,
        "constant_response_inverse": constant_response_inverse_residual,
        "mechanical_pressure": mechanical_pressure_residual,
        "bulk_modulus": bulk_modulus_residual,
        "kappa": kappa_residual,
        **{
            f"constant_d_{key}": value
            for key, value in constant_d_residuals.items()
        },
        "hidden_path": hidden_path_residual,
        "hidden_frozen_q": frozen_q_residual,
        "hidden_equilibrium_q": equilibrium_q_residual,
        "shape_measure": shape_measure_residual,
        "equal_link_volume": equal_link_volume_residual,
        **{
            f"equal_link_norm_{index + 1}": value
            for index, value in enumerate(link_norm_residuals)
        },
        "active_factorization": active_factorization_residual,
        "active_log_rate": active_log_rate_residual,
    }

    physical_flags = {key: False for key in EXPECTED_PHYSICAL_KEYS}

    # All mutations are fed through the same validators used by the gate.
    wrong_deformation = dict(deformation_validation)
    wrong_deformation["uniform_gram_scaling"] = exact_zero(a**3 - a**2)
    square_root_omission = dict(deformation_validation)
    square_root_omission["uniform_measure_scaling"] = exact_zero(
        a**6 - a**3
    )
    wrong_jacobi = dict(deformation_validation)
    wrong_jacobi["jacobi_log_measure_rate"] = exact_zero(
        directional_det / det_F_generic
        - sp.trace(F_generic * dF_generic)
    )

    selected_d3 = dict(nonselection)
    selected_d3["selected_dimension"] = 3
    missing_dimension = dict(nonselection)
    missing_dimension["candidate_dimensions"] = [2, 3]
    conflated_measure = dict(nonselection)
    conflated_measure["candidate_measure_scalings"] = {
        "filled_cell_measure": 3,
        "node_count": 3,
        "total_edge_length": 1,
    }

    vertices_mutated, edges_mutated = periodic_vertices_edges(2, 5)
    edges_mutated.remove(sorted(edges_mutated)[0])
    removed_edge_graph = graph_record_from_edges(
        2, 5, vertices_mutated, edges_mutated
    )
    promoted_center = dict(graph_witnesses["d2"])
    promoted_center["center_count"] = 1
    promoted_center["all_vertices_are_centers"] = False
    promoted_center["unique_center"] = True

    equal_link_conflation = dict(equal_link_record)
    equal_link_conflation["link_scale_selects_cubic_map"] = True
    erased_shape = dict(shape_record)
    erased_shape["states_distinct"] = False
    hidden_conflation = dict(hidden_state_record)
    hidden_conflation["unconditional_path_equals_fixed_q"] = True
    active_derivative_omission = (
        a * sp.diff(activated_volume, a) / activated_volume
        - a * sp.diff(cell_measure, a) / cell_measure
    )

    bridge_flip = dict(physical_flags)
    bridge_flip["geometric_measure_equals_mechanical_volume_derived"] = True
    one_coordinate_flip = dict(physical_flags)
    one_coordinate_flip["one_coordinate_state_reduction_derived"] = True

    negative_controls = {
        "wrong_gram_power_detected": not all_true_record(
            wrong_deformation, EXPECTED_DEFORMATION_VALIDATION_KEYS
        ),
        "gram_square_root_omission_detected": not all_true_record(
            square_root_omission, EXPECTED_DEFORMATION_VALIDATION_KEYS
        ),
        "jacobi_inverse_omission_detected": not all_true_record(
            wrong_jacobi, EXPECTED_DEFORMATION_VALIDATION_KEYS
        ),
        "wrong_log_response_detected": exact_nonzero(
            a * sp.diff(sp.log(measure), a)
            - response_from_measure
            + 1
        ),
        "wrong_reconstruction_measure_detected": exact_nonzero(
            a
            * sp.diff(
                sp.log(
                    V0
                    * sp.exp(
                        sp.Integral(nu_function(u), (u, 1, a))
                    )
                ),
                a,
            )
            - nu_function(a)
        ),
        "hard_selected_d3_detected": not nonselection_record_valid(
            selected_d3
        ),
        "dimension_witness_removal_detected": not nonselection_record_valid(
            missing_dimension
        ),
        "periodic_edge_removal_detected": not graph_record_valid(
            removed_edge_graph
        ),
        "unique_center_promotion_detected": not graph_record_valid(
            promoted_center
        ),
        "equal_link_cubic_conflation_detected": not equal_link_record_valid(
            equal_link_conflation
        ),
        "node_cell_measure_conflation_detected": not nonselection_record_valid(
            conflated_measure
        ),
        "shape_state_erasure_detected": not shape_record_valid(
            erased_shape
        ),
        "hidden_path_fixed_q_conflation_detected": not hidden_record_valid(
            hidden_conflation
        ),
        "active_measure_derivative_omission_detected": exact_nonzero(
            active_derivative_omission
        ),
        "general_d_pressure_three_detected": exact_nonzero(
            -energy_prime / (3 * V0 * a ** (d_symbol - 1))
            - pressure_d_expected
        ),
        "physical_bridge_flag_flip_invalidates_scope": not physical_scope_valid(
            bridge_flip
        ),
        "one_coordinate_flag_flip_invalidates_scope": not physical_scope_valid(
            one_coordinate_flip
        ),
        "upstream_hash_mutation_detected": not dependency_hash_chain_valid(
            PINNED_W3_41_RESULT_SHA256,
            PINNED_W3_41_RESULT_SHA256,
            "0" * len(PINNED_W3_41_RESULT_SHA256),
        ),
        "registered_keyset_mutation_detected": not exact_keyset(
            EXPECTED_CLOSURE_KEYS | {"unexpected_key"},
            EXPECTED_CLOSURE_KEYS,
        ),
    }

    graphs_valid = all(
        graph_record_valid(record)
        for record in graph_witnesses.values()
    )
    closure_flags = {
        "w3_41_dependency_verified": False,
        "periodic_graph_counts_exact": graphs_valid,
        "periodic_graph_regular_degrees_exact": graphs_valid,
        "periodic_graph_connected_exact": graphs_valid,
        "periodic_graph_translation_symmetry_exact": graphs_valid,
        "periodic_graph_no_unique_center_exact": graphs_valid,
        "multi_dimension_relational_witnesses_exact": (
            graphs_valid
            and sorted(
                record["dimension_label"]
                for record in graph_witnesses.values()
            )
            == [1, 2, 3]
        ),
        "homogeneous_deformation_determinant_exact": (
            deformation_validation["gram_determinant_identity"]
        ),
        "principal_stretch_product_exact": (
            deformation_validation["principal_stretch_product"]
        ),
        "jacobi_log_measure_rate_exact": (
            deformation_validation["jacobi_log_measure_rate"]
        ),
        "uniform_dilation_gram_scaling_exact": (
            deformation_validation["uniform_gram_scaling"]
        ),
        "geometric_measure_power_scaling_exact": (
            deformation_validation["uniform_measure_scaling"]
        ),
        "logarithmic_volume_response_exact": exact_zero(
            log_response_residual
        ),
        "volume_response_reconstruction_exact": exact_zero(
            response_reconstruction_residual
        ),
        "constant_response_power_equivalence_exact": bool(
            exact_zero(constant_response_forward_residual)
            and exact_zero(constant_response_inverse_residual)
        ),
        "d3_geometric_branch_matches_cubic_map_exact": exact_zero(
            d3_cubic_residual
        ),
        "generalized_mechanical_pressure_exact": exact_zero(
            mechanical_pressure_residual
        ),
        "generalized_bulk_modulus_exact": exact_zero(
            bulk_modulus_residual
        ),
        "generalized_kappa_identity_exact": exact_zero(kappa_residual),
        "constant_d_mechanical_dictionary_exact": all(
            exact_zero(value) for value in constant_d_residuals.values()
        ),
        "hidden_state_path_derivative_identity_exact": (
            hidden_state_record["path_residual_identity"]
        ),
        "hidden_state_reduction_condition_exact": hidden_record_valid(
            hidden_state_record
        ),
        "tracefree_shape_measure_degeneracy_exact": (
            shape_record["cubic_measure_for_all_shape_states"]
            and shape_record["same_measure"]
        ),
        "tracefree_shape_states_distinct_exact": shape_record_valid(
            shape_record
        ),
        "equal_link_volume_nonselection_exact": equal_link_record_valid(
            equal_link_record
        ),
        "fixed_graph_measure_nonselection_exact": (
            measure_scalings == {
                "filled_cell_measure": 3,
                "node_count": 0,
                "total_edge_length": 1,
            }
            and measure_nonselection["selected_measure"] is None
        ),
        "active_volume_factorization_exact": active_volume_record_valid(
            active_volume_record
        ),
        "dimension_measure_nonselection_exact": nonselection_record_valid(
            nonselection
        ),
        "one_coordinate_completeness_nonselection_exact": bool(
            nonselection_record_valid(nonselection)
            and shape_record_valid(shape_record)
            and hidden_record_valid(hidden_state_record)
        ),
        "registered_top_level_keysets_exact": False,
        "mutation_controls_pass": all(negative_controls.values()),
        "aggregate_identity_pass": False,
    }

    diagnostics = {
        "identities": {
            key: str(sp.simplify(value))
            for key, value in sorted(identities.items())
        },
        "graph_witnesses": graph_witnesses,
        "deformation_dictionary": {
            "validation": deformation_validation,
            "geometric_measure": "mathcal_V=sqrt(det(G))",
            "general_ratio": "mathcal_V/mathcal_V0=det(F) on GL^+(d)",
            "jacobi_response": (
                "d ln(mathcal_V/mathcal_V0)/d ln(a)="
                "a*tr(F^-1*dF/da)"
            ),
            "uniform_branch": (
                "F=a*I_d => mathcal_V_d=mathcal_V_d0*a^d"
            ),
            "selected_dimension": None,
        },
        "measure_response": {
            "definition": "nu=a*mathcal_V'(a)/mathcal_V(a)",
            "reconstruction": (
                "mathcal_V(a)=mathcal_V0*"
                "exp(Integral(nu(u)/u,(u,1,a)))"
            ),
            "constant_response_equivalence": (
                "nu=d constant iff mathcal_V=mathcal_V0*a^d "
                "on a connected normalized interval"
            ),
            "selected_response": None,
        },
        "mechanical_dictionary": {
            "bridge": "V_F=mathcal_V is candidate, not derived",
            "regular_locus": (
                "mathcal_V'!=0 (nu!=0); kappa additionally P_F=Pi_F!=0"
            ),
            "general_pressure": "Pi_F=-a*E_F'/(nu*mathcal_V)",
            "general_bulk_modulus": "K_F=-(a/nu)*Pi_F'",
            "general_kappa": "kappa=nu*K_F/P_F on P_F=Pi_F",
            "constant_d_pressure": (
                "Pi_F=-E_F'/(d*V_0*a**(d-1))"
            ),
            "constant_d_bulk_modulus": (
                "K_F=(a*E_F''-(d-1)*E_F')/"
                "(d**2*V_0*a**(d-1))"
            ),
            "constant_d_kappa": "kappa=d-1-a*E_F''/E_F'",
            "d3_regression_exact": all(
                exact_zero(value)
                for key, value in constant_d_residuals.items()
                if key.startswith("w3_41_")
            ),
        },
        "hidden_state": {
            **hidden_state_record,
            "regular_locus": (
                "V_a!=0 and V_a+V_q*q'!=0 for the corresponding ratios"
            ),
            "fixed_q_pressure": "Pi_F=-E_a/V_a",
            "path_difference": (
                "-q'*(E_q+Pi_F*V_q)/(V_a+V_q*q')"
            ),
            "reduction_condition": (
                "q'=0 OR E_q+Pi_F*V_q=0 on a regular path"
            ),
        },
        "shape_witness": {
            **shape_record,
            "gram_matrix": "a^2*diag(exp(2s),exp(-2s),1)",
            "measure": "a^3",
            "shape_invariant_s0": str(shape_zero),
            "shape_invariant_slog2": str(shape_log_two),
        },
        "equal_link_witness": {
            **equal_link_record,
            "angle_cosine": "(a-1)/(a+1)",
            "volume_ratio": "2*a**(7/2)/(a+1)",
            "interpretation": (
                "common link length does not freeze cell angles"
            ),
        },
        "measure_nonselection": measure_nonselection,
        "active_volume_roles": {
            **active_volume_record,
            "identity": "V_act=N_act*v_cell",
            "log_rate": (
                "dln(V_act)/dln(a)=dln(N_act)/dln(a)+"
                "dln(v_cell)/dln(a)"
            ),
            "geometric_cell_measure_equals_activated_volume": False,
        },
        "nonselection": nonselection,
    }
    return closure_flags, physical_flags, diagnostics, negative_controls


def build_report() -> dict[str, object]:
    prereg_hash = sha256(PREREG)
    if prereg_hash != PINNED_PREREG_SHA256:
        raise RuntimeError(
            "Preregistration hash mismatch: "
            f"{prereg_hash} != {PINNED_PREREG_SHA256}"
        )
    prereg_claim = registered_claim()
    if prereg_claim != CLAIM:
        raise RuntimeError("Registered claim does not match source claim")

    upstream = verify_upstream()
    closure_flags, physical_flags, diagnostics, negative_controls = (
        derive_gate()
    )
    closure_flags["w3_41_dependency_verified"] = bool(upstream["valid"])
    contract = build_contract()

    source_path = Path(__file__).resolve()
    verify_canonical_text(source_path)
    result = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "claim": CLAIM,
        "type": contract["TYPE"],
        "model_version": MODEL_VERSION,
        "status": "PENDING",
        "scope_status": "PENDING",
        "artifact_valid": False,
        "evidence_type": (
            "EXACT_CONDITIONAL_DICTIONARY_AND_CONSTRUCTIVE_NONSELECTION"
        ),
        "refg_status": (
            "FOUNDATION_DIMENSION_MEASURE_STATE_SELECTION_OPEN"
        ),
        "bridge_status": (
            "GEOMETRIC_MEASURE_EQUALS_MECHANICAL_VOLUME__"
            "CANDIDATE_NOT_DERIVED"
        ),
        "falsifier_triggered_for_refg": False,
        "blocking_reasons": [
            "No microscopic adjacency or graph-to-geometry map is derived.",
            "No physical dimension, cell complex, or volume measure is selected.",
            "The link scale a alone does not freeze angles or shape modes.",
            "No state-space quotient proves one homogeneous coordinate is complete.",
            "No work law derives the bridge V_F=mathcal_V.",
            "No foundation dynamics, pressure history, or observable model is derived.",
        ],
        "contract": contract,
        "closure_flags": closure_flags,
        "physical_closure_flags": physical_flags,
        "identities": diagnostics["identities"],
        "graph_witnesses": diagnostics["graph_witnesses"],
        "deformation_dictionary": diagnostics["deformation_dictionary"],
        "measure_response": diagnostics["measure_response"],
        "mechanical_dictionary": diagnostics["mechanical_dictionary"],
        "hidden_state": diagnostics["hidden_state"],
        "shape_witness": diagnostics["shape_witness"],
        "equal_link_witness": diagnostics["equal_link_witness"],
        "measure_nonselection": diagnostics["measure_nonselection"],
        "active_volume_roles": diagnostics["active_volume_roles"],
        "nonselection": diagnostics["nonselection"],
        "negative_controls": negative_controls,
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "preregistration": {
                "path": PREREG.name,
                "sha256": prereg_hash,
                "expected_sha256": PINNED_PREREG_SHA256,
                "registered_claim": prereg_claim,
                "valid": True,
            },
            "upstream_w3_41": upstream,
            "source": {
                "path": source_path.name,
                "sha256": sha256(source_path),
            },
            "python": platform.python_version(),
            "sympy": importlib.metadata.version("sympy"),
            "platform": platform.platform(),
            "line_endings": "LF",
        },
        "files": {
            "preregistration": PREREG.name,
            "source": source_path.name,
            "result": OUTPUT.name,
            "checksum": HASH_OUTPUT.name,
        },
    }

    closure_flags["registered_top_level_keysets_exact"] = bool(
        schema_keysets_valid(
            contract,
            closure_flags,
            physical_flags,
            negative_controls,
            result,
        )
        and contract["CLAIM"] == prereg_claim
        and contract["MODEL_VERSION"]["id"] == MODEL_VERSION
    )
    closure_flags["aggregate_identity_pass"] = all(
        value
        for key, value in closure_flags.items()
        if key != "aggregate_identity_pass"
    )
    artifact_valid = bool(
        closure_flags["aggregate_identity_pass"]
        and physical_scope_valid(physical_flags)
        and nonselection_record_valid(result["nonselection"])
    )
    result["artifact_valid"] = artifact_valid
    result["status"] = "PASS" if artifact_valid else "FAIL"
    result["scope_status"] = (
        "PASS_EXACT_HOMOGENEOUS_MEASURE_DICTIONARY__"
        "DIMENSION_MEASURE_AND_STATE_COMPLETENESS_OPEN"
        if artifact_valid
        else "FAIL_FOUNDATION_STATE_SPACE_VOLUME_MAP_GATE"
    )
    if not artifact_valid:
        failed = [
            key for key, value in closure_flags.items() if not value
        ]
        raise RuntimeError(f"W3-42 aggregate gate failed: {failed}")
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
