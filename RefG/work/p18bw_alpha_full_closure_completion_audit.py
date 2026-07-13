from __future__ import annotations

"""PHASE 18bw: objective-wide alpha closure completion audit.

This gate asks only whether the complete RefG electromagnetic problem is
closed.  It does not confuse a conditional Maxwell identity, a coupling of an
imported microscopic model, or a matching template with a RefG prediction.

The audit follows the required causal order:

  microscopic RefG action -> compact physical-Q Coulomb sector -> primitive
  normalization -> renormalized U_R/K_R -> charged spectrum and running ->
  Thomson prediction record -> comparison.

Every verdict below is assembled from earlier target-isolated gates.  No
electromagnetic comparison value is read or used.
"""

import ast
import inspect
from dataclasses import asdict, dataclass

from p18bp_spin1_frame_electroweak_operator_gate import (
    full_thomson_functional_and_counterterm_no_go,
)
from p18bq_photon_rigidity_uv_normalization_matching_gate import (
    neutral_generator_spectrum_rigidity_theorem,
    route_selection_and_closure_contract,
)
from p18br_hs_auxiliary_link_origin_gate import (
    constructive_route_contract,
    fmin_eigenframe_blindness_theorem,
    ordered_higgs_vs_coulomb_phase_dichotomy,
)
from p18bs_unified_physical_q_fixed_point_gate import (
    refg_fixed_point_derivability_audit,
)
from p18bt_node_flux_photon_spectral_invariant_gate import (
    flux_photon_spectral_alpha_theorem,
    refg_node_hamiltonian_derivability_audit,
)
from p18bu_alpha_selector_exhaustion_gate import (
    current_selector_exhaustion_theorem,
    minimal_predictive_completion_contract,
    source_firewall as selector_source_firewall,
)
from p18bv_microscopic_alpha_selector_routes_gate import (
    physical_q_bridge_and_success_contract,
    single_scale_pure_ring_selector_witness,
    source_firewall as microscopic_routes_source_firewall,
)


@dataclass(frozen=True)
class RequirementEvidence:
    requirement: str
    status: str
    satisfied: bool
    evidence: tuple[str, ...]


def objective_requirement_evidence_map() -> dict[str, object]:
    """Map every full-closure requirement to direct executable evidence."""

    frame = fmin_eigenframe_blindness_theorem()
    phase = ordered_higgs_vs_coulomb_phase_dichotomy()
    microscopic_route = constructive_route_contract()
    generator = neutral_generator_spectrum_rigidity_theorem()
    matching_contract = route_selection_and_closure_contract()
    thomson = full_thomson_functional_and_counterterm_no_go()
    fixed_point = refg_fixed_point_derivability_audit()
    spectral = flux_photon_spectral_alpha_theorem()
    node = refg_node_hamiltonian_derivability_audit()
    selectors = current_selector_exhaustion_theorem()
    completion = minimal_predictive_completion_contract()
    pure_ring = single_scale_pure_ring_selector_witness()
    physical_q = physical_q_bridge_and_success_contract()

    microscopic_action_closed = bool(
        microscopic_route["current_Fmin_microscopic_bond_derived"]
        and node["Hamiltonian_derived_from_current_Fmin"]
        and node["local_node_Hilbert_space_and_Gauss_constraint_derived"]
    )
    physical_q_photon_closed = bool(
        phase["current_RefG_action_selects_coulomb_branch"]
        and node["deconfined_3plus1D_Coulomb_phase_derived"]
        and node["primitive_flux_to_physical_Q_bridge_derived"]
    )
    primitive_normalization_closed = bool(
        generator["generation_universal_charge_rigidity_proved"]
        and not generator["hypercharges_are_imported_not_derived"]
        and not physical_q["hypercharges_are_imported"]
        and physical_q[
            "pure_ring_primitive_defect_is_derived_as_electron_charge"
        ]
        and physical_q[
            "fractional_quark_charge_and_global_quotient_derived"
        ]
    )
    renormalized_shape_closed = bool(
        spectral["spectral_ratio_equals_alpha_at_declared_scale"]
        and node[
            "renormalized_Coulomb_stiffness_from_microscopic_nodes_derived"
        ]
        and node["dimensionless_shape_U_over_K_derived"]
    )
    charged_sector_closed = bool(
        node["charged_core_spectrum_and_vacuum_polarization_derived"]
        and not physical_q["hypercharges_are_imported"]
        and fixed_point["unified_group_and_breaking_derived"]
        and fixed_point["unified_matter_coefficient_b_U_derived"]
    )
    thomson_closed = bool(
        node["running_to_Thomson_limit_derived"]
        and thomson["HVP_present_in_workspace"]
        and thomson["full_matching_is_prediction_without_independent_HVP"]
        and matching_contract["current_requirements_satisfied"]
    )
    frozen_prediction_closed = bool(
        microscopic_action_closed
        and physical_q_photon_closed
        and primitive_normalization_closed
        and renormalized_shape_closed
        and charged_sector_closed
        and thomson_closed
        and selectors["any_current_route_derives_unique_physical_alpha"]
        and fixed_point["current_alpha_prediction"]
        and pure_ring["current_RefG_alpha_EM_prediction"]
    )
    comparison_stage_reached = frozen_prediction_closed

    requirements = (
        RequirementEvidence(
            requirement="RefG-derived microscopic compact node action",
            status="MISSING",
            satisfied=microscopic_action_closed,
            evidence=(
                "F_min is exactly eigenframe-blind",
                "the microscopic bond, compact link Hilbert space and Gauss law are not derived",
                "a bare ring coefficient is not fixed by the present action",
            ),
        ),
        RequirementEvidence(
            requirement="massless deconfined physical-Q photon sector",
            status="MISSING",
            satisfied=physical_q_photon_closed,
            evidence=(
                "the present ordered frame is a Higgs/Stueckelberg branch rather than a Coulomb photon",
                "a deconfined three-dimensional Coulomb phase is not derived",
                "primitive node flux is not derived as Q=T3+Y",
            ),
        ),
        RequirementEvidence(
            requirement="primitive electric-charge and coupling normalization",
            status="CONDITIONAL_ONLY",
            satisfied=primitive_normalization_closed,
            evidence=(
                "Q=T3+Y is rigid only after the Standard-Model charge representation is supplied",
                "the hypercharges and global charge lattice are imported rather than derived",
                "the pure-ring defect is not identified with the electron charge",
            ),
        ),
        RequirementEvidence(
            requirement="unique target-free renormalized U_R/K_R",
            status="MEASUREMENT_IDENTITY_CLOSED_SELECTOR_MISSING",
            satisfied=renormalized_shape_closed,
            evidence=(
                "the primitive-flux/photon spectral ratio exactly measures alpha for a declared compact Coulomb model",
                "the current RefG action does not derive the renormalized stiffness ratio",
                "an allowed continuous stiffness deformation changes alpha while preserving the derived kinematics and topology",
            ),
        ),
        RequirementEvidence(
            requirement="complete charged spectrum, electroweak breaking and QCD sector",
            status="MISSING",
            satisfied=charged_sector_closed,
            evidence=(
                "finite-energy charged cores, hopping, masses and multiplicities are not derived",
                "the electroweak representation and breaking sector are not produced by the current substrate action",
                "fractional quark charges and the global gauge-group quotient are not derived",
            ),
        ),
        RequirementEvidence(
            requirement="complete running and matching to the Thomson limit",
            status="MISSING",
            satisfied=thomson_closed,
            evidence=(
                "the target-free Thomson functional is known but retains finite local stiffness directions",
                "hadronic vacuum polarization is not derived in the workspace",
                "the complete single-scheme threshold flow is not closed",
            ),
        ),
        RequirementEvidence(
            requirement="frozen target-independent RefG alpha_EM prediction",
            status="NOT_AVAILABLE",
            satisfied=frozen_prediction_closed,
            evidence=(
                "none of the currently audited selectors gives a unique physical coupling",
                "the external pure-ring model selects its own link coupling but is not derived from RefG",
                "no RefG prediction record exists to freeze",
            ),
        ),
        RequirementEvidence(
            requirement="comparison only after the prediction is frozen",
            status="NOT_REACHED_BY_DESIGN",
            satisfied=comparison_stage_reached,
            evidence=(
                "the construction audit contains no electromagnetic comparison value",
                "comparison is withheld because the preceding prediction record does not exist",
            ),
        ),
    )

    upstream_payloads = (
        frame,
        phase,
        microscopic_route,
        generator,
        matching_contract,
        thomson,
        fixed_point,
        spectral,
        node,
        selectors,
        completion,
        pure_ring,
        physical_q,
    )
    upstream_reference_firewall_pass = all(
        payload.get("reference_value_used") is False
        for payload in upstream_payloads
    )
    upstream_source_firewall_pass = bool(
        selector_source_firewall()["target_isolation_pass"]
        and microscopic_routes_source_firewall()["target_isolation_pass"]
    )

    return {
        "requirements": tuple(asdict(row) for row in requirements),
        "requirement_count": len(requirements),
        "requirements_satisfied": sum(row.satisfied for row in requirements),
        "all_requirements_satisfied": all(
            row.satisfied for row in requirements
        ),
        "upstream_reference_firewall_pass": upstream_reference_firewall_pass,
        "upstream_source_firewall_pass": upstream_source_firewall_pass,
        "spectral_alpha_measure_closed": spectral[
            "spectral_ratio_equals_alpha_at_declared_scale"
        ],
        "fully_specified_microscopic_model_can_select_a_link_coupling": pure_ring[
            "declared_model_selects_link_alpha_without_target"
        ],
        "that_external_model_is_a_RefG_alpha_EM_prediction": pure_ring[
            "current_RefG_alpha_EM_prediction"
        ],
        "current_selector_exhaustion_guards_pass": selectors[
            "exact_guards_pass"
        ],
        "current_route_derives_unique_physical_alpha": selectors[
            "any_current_route_derives_unique_physical_alpha"
        ],
        "future_microscopic_prediction_is_proved_impossible": selectors[
            "universal_future_alpha_prediction_is_impossible"
        ],
        "completion_contract_currently_satisfied": completion[
            "current_contract_satisfied"
        ],
        "current_RefG_alpha_EM_mathematically_closed": frozen_prediction_closed,
        "comparison_stage_reached": comparison_stage_reached,
        "exact_blocker": (
            "the current RefG EFT neither contains nor uniquely selects a microscopic compact physical-Q node action; "
            "the allowed completion class therefore retains a continuous physical Maxwell-stiffness direction"
        ),
        "new_theory_premise_required": (
            "derive one compact physical-Q microscopic action from the substrate, or declare a new dynamical selection principle that uniquely fixes that action and its full charged sector"
        ),
        "choosing_a_convenient_microscopic_model_now_would_be_a_derivation": False,
        "reference_value_used": False,
    }


def source_firewall() -> dict[str, object]:
    """Reject target leakage and imports from comparison-stage modules."""

    source = inspect.getsource(inspect.getmodule(source_firewall))
    tree = ast.parse(source)
    numeric_literals = tuple(
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    )
    forbidden_modules = ("p18" + "bm", "p18" + "bk")
    forbidden_text = (
        "CO" + "DATA",
        "observed " + "inverse",
        "13" + "7.",
    )
    comparison_float = any(
        isinstance(value, float) and 100 < abs(value) < 200
        for value in numeric_literals
    )
    local_imports = tuple(
        sorted(
            {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom)
                and node.module is not None
                and node.module.startswith("p")
            }
        )
    )
    allowed_local_imports = {
        "p18bp_spin1_frame_electroweak_operator_gate",
        "p18bq_photon_rigidity_uv_normalization_matching_gate",
        "p18br_hs_auxiliary_link_origin_gate",
        "p18bs_unified_physical_q_fixed_point_gate",
        "p18bt_node_flux_photon_spectral_invariant_gate",
        "p18bu_alpha_selector_exhaustion_gate",
        "p18bv_microscopic_alpha_selector_routes_gate",
    }
    violations = tuple(text for text in forbidden_text if text in source)
    disallowed_imports = tuple(
        name for name in local_imports if name not in allowed_local_imports
    )
    comparison_module = any(name in source for name in forbidden_modules)
    return {
        "contains_comparison_numeric_literal": comparison_float,
        "forbidden_text_violations": violations,
        "local_imports": local_imports,
        "disallowed_local_imports": disallowed_imports,
        "imports_comparison_module": comparison_module,
        "target_isolation_pass": not (
            comparison_float
            or violations
            or disallowed_imports
            or comparison_module
        ),
    }


def run_gate() -> None:
    audit = objective_requirement_evidence_map()
    firewall = source_firewall()

    assert audit["requirement_count"] == 8
    assert audit["requirements_satisfied"] == 0
    assert audit["all_requirements_satisfied"] is False
    assert audit["upstream_reference_firewall_pass"]
    assert audit["upstream_source_firewall_pass"]
    assert audit["spectral_alpha_measure_closed"]
    assert audit[
        "fully_specified_microscopic_model_can_select_a_link_coupling"
    ]
    assert audit[
        "that_external_model_is_a_RefG_alpha_EM_prediction"
    ] is False
    assert audit["current_selector_exhaustion_guards_pass"]
    assert audit["current_route_derives_unique_physical_alpha"] is False
    assert audit[
        "future_microscopic_prediction_is_proved_impossible"
    ] is False
    assert audit["completion_contract_currently_satisfied"] is False
    assert audit["current_RefG_alpha_EM_mathematically_closed"] is False
    assert audit["comparison_stage_reached"] is False
    assert audit[
        "choosing_a_convenient_microscopic_model_now_would_be_a_derivation"
    ] is False
    assert firewall["target_isolation_pass"]

    print("\nobjective-wide requirement evidence")
    for row in audit["requirements"]:
        print(
            f"  [{row['status']}] {row['requirement']}: "
            f"satisfied={row['satisfied']}"
        )
        for evidence in row["evidence"]:
            print(f"    - {evidence}")

    print("\ncompletion verdict")
    for key, value in audit.items():
        if key != "requirements":
            print(f"  {key}: {value}")

    print("\nsource firewall")
    for key, value in firewall.items():
        print(f"  {key}: {value}")

    print(
        "\nSTATUS: BLOCKED_CURRENT_REFG_LACKS_DERIVED_MICROSCOPIC_"
        "COMPACT_PHYSICAL_Q_ACTION__PASS_OBJECTIVE_WIDE_ALPHA_CLOSURE_"
        "COMPLETION_AUDIT_AND_TARGET_FIREWALL"
    )


if __name__ == "__main__":
    run_gate()
