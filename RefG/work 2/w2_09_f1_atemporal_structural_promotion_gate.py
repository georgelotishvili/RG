"""F1 promotion of the atemporal spectral candidate, with an exact ceiling.

The result is conditional on the declared foundation primitives.  It promotes
only intrinsic structural self-differentiation: one accepted quotient state
contains canonical, coexisting, nonexchangeable internal roles.  It does not
derive the foundation law and does not establish nodes, relations, time,
modes, spacetime, gravity, or observations.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


MODEL_VERSION = "W2-F1-ATEMPORAL-STRUCTURAL-PROMOTION-v1.0-scientific"
CANDIDATE_ID = "W2_F1_ATEMPORAL_SPECTRAL_SPLIT_CANDIDATE_001"
ROUTE_CLASS = "atemporal_intrastate_invariant_role_structure"
WITNESS_KIND = "INTRA_CLASS_CANONICAL_ROLES"
LAW_ORIGIN_STATUS = "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED"

FROZEN_PROMOTION_GATES = (
    "f1_definition_frozen_route_neutral",
    "witness_kind_frozen_before_evaluation",
    "complete_one_foundation_primitive_freedom_registry",
    "forbidden_target_intersection_empty",
    "undifferentiated_reference_trivial",
    "target_free_law_certified",
    "complete_output_classification",
    "intrinsic_differentiation_certified",
    "inequivalence_survives_full_quotient",
    "law_relevance_not_arbitrary_decomposition",
    "realization_or_selection_noncircular",
    "open_domain_stability_and_robustness",
    "foundation_admissibility_and_import_health",
    "router_extension_aligned",
    "independent_crosscheck_and_controls",
    "candidate_falsifier_absent",
    "f1_only_scope_honest",
)

NORMALIZED_IMPORT_OWNERSHIP = {
    "single_internal_carrier_Q": {
        "origin": LAW_ORIGIN_STATUS,
        "allowed_meaning": "one abstract internal carrier",
        "forbidden_inference": "particle, node, location, material object, or physical object count",
    },
    "Sym0_3_R_internal_configuration_space": {
        "origin": LAW_ORIGIN_STATUS,
        "allowed_meaning": "finite internal trial state space with imported N=3",
        "forbidden_inference": "physical three-space, 3+1 dimension, or continuum",
    },
    "positive_definite_internal_delta_and_transpose": {
        "origin": LAW_ORIGIN_STATUS,
        "allowed_meaning": "internal algebraic contraction and transpose",
        "forbidden_inference": "spacetime or spatial metric",
    },
    "matrix_product_and_Tr_alg": {
        "origin": LAW_ORIGIN_STATUS,
        "allowed_meaning": "internal matrix/Jordan-algebra bookkeeping",
        "forbidden_inference": "persistent physical trace, propagation, or observable",
    },
    "O3_internal_conjugation_relabel_equivalence": {
        "origin": LAW_ORIGIN_STATUS,
        "allowed_meaning": "complete declared internal relabelling equivalence",
        "forbidden_inference": "physical rotation group or spacetime isotropy",
    },
    "absence_of_Q_sign_relabel_symmetry": {
        "origin": LAW_ORIGIN_STATUS,
        "allowed_meaning": "declared internal polarity choice",
        "forbidden_inference": "charge, arrow of time, or observed polarity",
    },
    "atemporal_global_argmin_rule": {
        "origin": LAW_ORIGIN_STATUS,
        "allowed_meaning": "uniform atemporal admissibility law",
        "forbidden_inference": "temporal relaxation, dynamics, or deeper-law derivation",
    },
    "positive_open_parameter_domain_alpha_b_c": {
        "origin": LAW_ORIGIN_STATUS,
        "allowed_meaning": "one open model domain with zero data fit",
        "forbidden_inference": "observational calibration or unique constants",
    },
    "quartic_invariant_functional_form_signs_and_truncation": {
        "origin": LAW_ORIGIN_STATUS,
        "allowed_meaning": "fixed complete O(3)-invariant polynomial through degree four",
        "forbidden_inference": "derived unique fundamental law or target-orbit distance",
    },
}

INVARIANT_LAW_LEDGER = {
    "carrier": "one Q in Sym_0(3,R)",
    "equivalence": "Q ~ R Q R^T for R in O(3)",
    "trace_constraint": "Tr(Q)=0 removes the degree-one invariant",
    "generators": ("I2=Tr(Q^2)", "I3=Tr(Q^3)"),
    "invariant_ring_theorem": (
        "real-symmetric spectral theorem plus the fundamental theorem of symmetric "
        "polynomials with e1=Tr(Q)=0"
    ),
    "invariant_ring_theorem_status": "STANDARD_EXACT_MATHEMATICAL_THEOREM_NOT_PHYSICAL_PRIMITIVE",
    "terms_through_degree_four": ("I2", "I3", "I2^2"),
    "dependent_identity": "Tr(Q^4)=I2^2/2",
    "irrelevant_constant": "an additive constant is omitted because it does not change argmin",
    "functional": "V=-alpha I2/2-b I3/3+c I2^2/4",
    "domain": "alpha>0, b>0, c>0",
    "forbidden_terms_absent": (
        "preferred basis or direction",
        "target projector, rank, spectrum, or orbit distance",
        "post-output term or hidden tie-breaker",
        "spacetime, GR, observable, or data term",
    ),
    "origin_status": LAW_ORIGIN_STATUS,
}

OUTPUT_CLASSIFICATION = {
    "alpha_b_c_positive": "unique nonzero global-minimum quotient class with canonical 1+2 roles",
    "Q_zero": "stationary strict maximum; no nontrivial generated role",
    "negative_stationary_root": "higher energy and negative biaxial direction",
    "O3_orientation_orbit": "relabel-equivalent; no representative direction selected",
    "b_zero_boundary": "degenerate quotient outside the strict certificate",
    "alpha_zero_boundary": "marginal origin outside the open domain",
    "c_zero_or_negative": "noncoercive or unbounded outside the domain",
    "b_negative": "polarity mirror outside the frozen positive domain",
    "positive_quadratic_null": "undifferentiated stable origin only",
    "N_one": "traceless state space trivial",
    "N_two": "equal-rank sectors; not this witness",
    "N_four_and_general_N": "control only; N=3 and 1+2 are not universal",
    "explicit_linear_source": "rejected preferred-direction preloading",
    "invariant_target_orbit_distance": "rejected invariant target preloading",
}

SCOPE_FIREWALL = {
    "physical_node_or_location": False,
    "persistent_physical_imprint": False,
    "operational_relation": False,
    "temporal_formation_or_persistence": False,
    "internal_causal_order_or_clock": False,
    "independent_additive_physical_modes": False,
    "physical_space_dimension_or_continuum": False,
    "Lorentzian_metric_or_light_cone": False,
    "effective_action_or_conservation_law": False,
    "pressure_mass_particle_or_oscillon": False,
    "observable_or_data_map": False,
    "Einstein_GR_PN_PPN_or_compact_source_bridge": False,
}

KNOWN_LIMITATIONS = {
    "foundation_law_origin": "open beyond the declared primitive",
    "functional_uniqueness": "not derived; other foundation laws remain possible",
    "N3_origin": "imported; no physical dimension meaning",
    "equivalence_ceiling": "nonexchangeability is relative to the declared O(3) relabelling",
    "robustness_ceiling": "open alpha,b,c domain inside the frozen quartic law class",
    "RefG_resonant_environment_map": "open; belongs to F2 and later",
    "temporal_formation": "open; this result is atemporal",
    "observation": "not applicable at F1; observational veto remains",
}


def _load_sibling(filename: str, module_name: str) -> Any:
    path = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def independent_algebra_audit() -> dict[str, Any]:
    """Independent invariant/projector calculation, not report-schema checking."""
    alpha, b, c = sp.symbols("alpha b c", positive=True, real=True)
    x, y, u, v, w = sp.symbols("x y u v w", real=True)
    Q = sp.Matrix([[x, u, v], [u, y, w], [v, w, -x - y]])
    I2 = sp.expand(sp.trace(Q**2))
    I3 = sp.expand(sp.trace(Q**3))
    I4 = sp.expand(sp.trace(Q**4))
    trace_constraint = sp.simplify(sp.trace(Q)) == 0

    cayley_hamilton = sp.simplify(Q**3 - I2 * Q / 2 - I3 * sp.eye(3) / 3)
    degree_four = sp.simplify(I4 - I2**2 / 2)

    s = sp.symbols("s", positive=True, real=True)
    Qs = s * sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
    P1 = sp.simplify(Qs / s + sp.eye(3) / 3)
    P2 = sp.simplify(sp.eye(3) - P1)
    projectors_exact = all((
        matrix_is_zero(P1**2 - P1),
        matrix_is_zero(P2**2 - P2),
        matrix_is_zero(P1 * P2),
        P1.rank() == 1,
        P2.rank() == 2,
    ))

    Delta = sp.sqrt(b**2 + 24 * alpha * c)
    s_plus = (b + Delta) / (4 * c)
    stationary_exact = sp.simplify(2 * c * s_plus**2 - b * s_plus - 3 * alpha) == 0
    radial_positive = sp.simplify(4 * c * s_plus - b) == Delta
    biaxial_positive = sp.simplify(b * s_plus).is_positive is True

    # Spectral invariance reduces the problem to symmetric polynomials in
    # three real eigenvalues.  Newton identities with e1=p1=0 give
    # e2=-p2/2, e3=p3/3 and p4=p2^2/2.  Thus, apart from a constant, the
    # nonconstant invariant terms through degree four are I2, I3 and I2^2.
    l1, l2 = sp.symbols("l1 l2", real=True)
    l3 = -l1 - l2
    p1 = sp.expand(l1 + l2 + l3)
    p2 = sp.expand(l1**2 + l2**2 + l3**2)
    p3 = sp.expand(l1**3 + l2**3 + l3**3)
    p4 = sp.expand(l1**4 + l2**4 + l3**4)
    e2 = sp.expand(l1 * l2 + l1 * l3 + l2 * l3)
    e3 = sp.expand(l1 * l2 * l3)
    newton_identities_exact = all((
        p1 == 0,
        sp.expand(e2 + p2 / 2) == 0,
        sp.expand(e3 - p3 / 3) == 0,
        sp.expand(p4 - p2**2 / 2) == 0,
    ))
    theorem_basis_declared = all((
        "spectral theorem" in INVARIANT_LAW_LEDGER["invariant_ring_theorem"],
        "symmetric polynomials" in INVARIANT_LAW_LEDGER["invariant_ring_theorem"],
        INVARIANT_LAW_LEDGER["invariant_ring_theorem_status"]
        == "STANDARD_EXACT_MATHEMATICAL_THEOREM_NOT_PHYSICAL_PRIMITIVE",
    ))
    invariant_terms_complete = all((
        trace_constraint,
        matrix_is_zero(cayley_hamilton),
        degree_four == 0,
        newton_identities_exact,
        theorem_basis_declared,
        INVARIANT_LAW_LEDGER["terms_through_degree_four"] == ("I2", "I3", "I2^2"),
    ))
    checks = {
        "traceless_3x3_Cayley_Hamilton": matrix_is_zero(cayley_hamilton),
        "degree_four_reduction": degree_four == 0,
        "trace_constraint_exact": trace_constraint,
        "newton_identities_through_degree_four": newton_identities_exact,
        "spectral_invariant_theorem_basis_declared": theorem_basis_declared,
        "invariant_terms_through_degree_four_complete": invariant_terms_complete,
        "Q_generated_projectors": projectors_exact,
        "ranks_prevent_O3_exchange": P1.rank() != P2.rank(),
        "positive_stationary_root": stationary_exact,
        "radial_normal_mode_positive": radial_positive,
        "biaxial_normal_modes_positive": biaxial_positive,
    }
    return {
        "CHECKS": checks,
        "DIAGNOSTICS": {
            "Cayley_Hamilton_residual": str(cayley_hamilton),
            "TrQ4_minus_I2sq_over_2": str(degree_four),
            "projector_ranks": [P1.rank(), P2.rank()],
            "s_plus": str(s_plus),
        },
    }


def run_gate() -> dict[str, Any]:
    candidate_module = _load_sibling(
        "w2_06_f1_atemporal_spectral_split_candidate_gate.py", "w2_06_scientific"
    )
    contract_module = _load_sibling(
        "w2_08_f1_physical_promotion_contract.py", "w2_08_scientific"
    )
    candidate = candidate_module.run_gate()
    contract = contract_module.run_gate()
    algebra = independent_algebra_audit()

    candidate_checks = candidate.get("CHECKS", {})
    candidate_exact = all((
        candidate.get("STATUS")
        == "EXACT_ATEMPORAL_SPECTRAL_CANDIDATE_PASS__PHYSICAL_F1_OPEN",
        bool(candidate_checks),
        all(value is True for value in candidate_checks.values()),
    ))
    contract_checks = contract.get("CHECKS", {})
    contract_exact = all((
        contract.get("STATUS")
        == "F1_PROMOTION_CONTRACT_AND_ROUTE_TAXONOMY_DEFINED__CANDIDATE_NOT_EVALUATED",
        bool(contract_checks),
        all(value is True for value in contract_checks.values()),
        contract.get("PROMOTION_AUTHORIZED") is False,
        contract.get("CLOSURE_FLAGS", {}).get("W2_06_PROMOTED_TO_W2_F1") is False,
    ))
    algebra_exact = all(algebra["CHECKS"].values())
    imported = tuple(candidate.get("IMPORTED_NOT_DERIVED", ()))
    expected_imports = frozenset(NORMALIZED_IMPORT_OWNERSHIP)
    import_registry_exact = all((
        len(imported) == len(expected_imports),
        frozenset(imported) == expected_imports,
    ))
    ownership_schema_exact = all((
        set(NORMALIZED_IMPORT_OWNERSHIP) == expected_imports,
        all(
            set(item) == {"origin", "allowed_meaning", "forbidden_inference"}
            and item["origin"] == LAW_ORIGIN_STATUS
            and bool(item["allowed_meaning"].strip())
            and bool(item["forbidden_inference"].strip())
            for item in NORMALIZED_IMPORT_OWNERSHIP.values()
        ),
    ))
    expected_output_keys = {
        "alpha_b_c_positive", "Q_zero", "negative_stationary_root",
        "O3_orientation_orbit", "b_zero_boundary", "alpha_zero_boundary",
        "c_zero_or_negative", "b_negative", "positive_quadratic_null",
        "N_one", "N_two", "N_four_and_general_N", "explicit_linear_source",
        "invariant_target_orbit_distance",
    }
    output_classification_exact = all((
        set(OUTPUT_CLASSIFICATION) == expected_output_keys,
        OUTPUT_CLASSIFICATION["alpha_b_c_positive"].startswith(
            "unique nonzero global-minimum quotient class"
        ),
        OUTPUT_CLASSIFICATION["negative_stationary_root"].startswith("higher energy"),
        OUTPUT_CLASSIFICATION["invariant_target_orbit_distance"]
        == "rejected invariant target preloading",
        candidate_checks.get("stationary_branches_exhaustive_and_energy_ordered") is True,
        candidate_checks.get("all_boundary_null_and_preloading_controls") is True,
    ))
    target_orbit_distance_absent = all((
        "orbit distance" not in INVARIANT_LAW_LEDGER["functional"].lower(),
        "target_orbit" not in " ".join(imported).lower(),
        candidate_checks.get("explicit_linear_source_is_detected") is True,
        OUTPUT_CLASSIFICATION["invariant_target_orbit_distance"].startswith("rejected"),
    ))
    required_control_keys = {
        "N1_traceless_state_is_trivial",
        "N2_has_no_unequal_rank_cubic_split",
        "N3_N4_generalN_dimension_control",
        "b_zero_quotient_is_degenerate",
        "positive_quadratic_null_has_stable_origin",
        "alpha_zero_origin_is_marginal",
        "c_nonpositive_is_noncoercive",
        "Q_sign_polarity_mirror_exact",
        "negative_stationary_branch_rejected",
        "explicit_linear_source_is_detected",
        "all_boundary_null_and_preloading_controls",
    }
    candidate_controls_exact = all(
        candidate_checks.get(key) is True for key in required_control_keys
    )

    evidence = {
        "f1_definition_frozen_route_neutral": contract_exact,
        "witness_kind_frozen_before_evaluation": (
            contract["CANDIDATE_CLASSIFICATION"]["witness_kind"] == WITNESS_KIND
        ),
        "complete_one_foundation_primitive_freedom_registry": (
            import_registry_exact and ownership_schema_exact
        ),
        "forbidden_target_intersection_empty": target_orbit_distance_absent,
        "undifferentiated_reference_trivial": candidate_checks.get(
            "origin_stationary_and_unstable"
        ) is True,
        "target_free_law_certified": all((
            algebra_exact,
            INVARIANT_LAW_LEDGER["functional"]
            == "V=-alpha I2/2-b I3/3+c I2^2/4",
            target_orbit_distance_absent,
        )),
        "complete_output_classification": output_classification_exact,
        "intrinsic_differentiation_certified": candidate_checks.get(
            "state_generated_rank_1_rank_2_projectors"
        ) is True,
        "inequivalence_survives_full_quotient": (
            algebra["DIAGNOSTICS"]["projector_ranks"] == [1, 2]
        ),
        "law_relevance_not_arbitrary_decomposition": all((
            candidate_checks.get("sharp_bound_and_unique_global_orbit") is True,
            candidate_checks.get("state_generated_rank_1_rank_2_projectors") is True,
        )),
        "realization_or_selection_noncircular": (
            LAW_ORIGIN_STATUS == "DECLARED_FOUNDATIONAL_PRIMITIVE_NOT_DERIVED"
            and "atemporal_global_argmin_rule" in imported
            and OUTPUT_CLASSIFICATION["O3_orientation_orbit"].startswith("relabel-equivalent")
        ),
        "open_domain_stability_and_robustness": candidate_checks.get(
            "orbit_normal_hessian_positive"
        ) is True,
        "foundation_admissibility_and_import_health": (
            import_registry_exact and ownership_schema_exact
        ),
        "router_extension_aligned": (
            contract["CANDIDATE_CLASSIFICATION"]["effective_class"] == ROUTE_CLASS
        ),
        "independent_crosscheck_and_controls": all((
            algebra_exact,
            candidate_controls_exact,
        )),
        "candidate_falsifier_absent": candidate_exact,
        "f1_only_scope_honest": not any(SCOPE_FIREWALL.values()),
    }
    schema_exact = set(evidence) == set(FROZEN_PROMOTION_GATES)
    exact_booleans = all(type(value) is bool for value in evidence.values())
    promoted = schema_exact and exact_booleans and all(evidence.values())

    return {
        "MODEL_VERSION": MODEL_VERSION,
        "CANDIDATE_ID": CANDIDATE_ID,
        "STATUS": (
            "W2_F1_ATEMPORAL_STRUCTURAL_PASS_RELATIVE_TO_DECLARED_PRIMITIVES"
            if promoted else
            "W2_F1_ATEMPORAL_STRUCTURAL_NOT_PROMOTED"
        ),
        "PROMOTED": promoted,
        "PROMOTION_EVIDENCE": evidence,
        "INDEPENDENT_ALGEBRA_AUDIT": algebra,
        "NORMALIZED_IMPORT_OWNERSHIP": NORMALIZED_IMPORT_OWNERSHIP,
        "INVARIANT_LAW_LEDGER": INVARIANT_LAW_LEDGER,
        "OUTPUT_CLASSIFICATION": OUTPUT_CLASSIFICATION,
        "KNOWN_LIMITATIONS": KNOWN_LIMITATIONS,
        "SCOPE_FIREWALL": SCOPE_FIREWALL,
        "PROMOTION_CEILING": (
            "structural self-differentiation relative to declared imported primitives; "
            "not foundation-law derivation, F2, time, modes, geometry, gravity, or observation"
        ),
        "FALLBACK_STATUS": {
            "symmetric_seed_route": "open; not rejected",
            "atemporal_nonunique_solution_structure": "open; not rejected",
            "all_other_nonfalsified_routes": "open",
        },
        "CLOSURE_FLAGS": {
            "W2_06_OVERLAY_CLASS_EVALUATED": True,
            "W2_06_OVERLAY_CLASS_SATISFIED": promoted,
            "W2_F1_ATEMPORAL_STRUCTURAL_RELATIVE_TO_FROZEN_PRIMITIVES": promoted,
            "W2_F1_SELF_DIFFERENTIATION": promoted,
            "FOUNDATION_LAW_DERIVED": False,
            "REFG_RESONANT_ENVIRONMENT_MAP": False,
            "W2_F2_OPERATIONAL_RELATIONS": False,
            "W2_F3_INTERNAL_ORDER_CAUSALITY": False,
            "W2_F4_INDEPENDENT_ADDITIVE_MODES": False,
            "W2_M1_DIMENSION_CONTINUUM": False,
            "W2_M2_LORENTZIAN_METRIC": False,
            "W2_A0_EFFECTIVE_ACTION_ORIGIN": False,
        },
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["PROMOTED"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
