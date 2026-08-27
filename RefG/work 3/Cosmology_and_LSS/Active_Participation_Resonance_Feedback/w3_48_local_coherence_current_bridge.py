#!/usr/bin/env python3
"""No-write verifier for the W3-48 local coherence-current bridge audit."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_48_MICRO_TO_HOMOGENEOUS_COHERENCE_CURRENT_BRIDGE"
SUBSIDIARY_STATUS = (
    "PASS_EXACT_CONDITIONAL_COHERENCE_BALANCE_TO_W3_47_EQUIVALENCE"
)
OPEN_STATUS = (
    "OPEN_MICRO_TO_W3_47_BRIDGE__"
    "LOCAL_COHERENT_PARTICIPATION_CURRENT_UNDERIVED"
)

HERE = Path(__file__).resolve().parent
WORK3 = HERE.parents[1]
W3_42_DIR = HERE.parent / "Foundation_State_Space_and_Volume_Map"
W3_42_RESULT = W3_42_DIR / "w3_42_result.json"
W3_42_CHECKSUM = W3_42_DIR / "w3_42_result.sha256"

DEPENDENCIES = {
    "w3_39_result": (
        WORK3 / "Genesis_Scenario" / "w3_39_result.json",
        "ff2440311e2c4ceb5fe5a2393b6730d2a3c2a2c49dd5b2ceaf7e32f0a0ab1160",
    ),
    "w3_42_preregistration": (
        W3_42_DIR
        / "w3_42_foundation_state_space_volume_map_preregistration.md",
        "4cc4674775525a3c76cd8cb282461e5e83b651aff3554de21983568ee7e1f9f1",
    ),
    "w3_42_source": (
        W3_42_DIR / "w3_42_foundation_state_space_volume_map.py",
        "0593c452dae764c2b0455d31807a6a81d033bd928db40717a0eec6df5fe04188",
    ),
    "w3_46_contract": (
        HERE / "w3_46_active_participation_resonance_feedback_contract.md",
        "0109ed3d5e8daec55dbd0f01f8b05932e6f653373438455c32a3d26378e0f3b2",
    ),
    "w3_47_preregistration": (
        HERE
        / "w3_47_post_genesis_evolution_pressure_coupling_kernel_preregistration.md",
        "ed1d5b6c2a982cdaafd6739e6a8388219931300b8df92bf015ab2112001049a5",
    ),
    "w3_47_verifier_source": (
        HERE / "w3_47_post_genesis_evolution_pressure_coupling_kernel.py",
        "d65d8644f443d7991fadbf5f808453b4b227fb87bcef789a8e8c8f89860bfc1f",
    ),
    "w3_48_preregistration": (
        HERE / "w3_48_local_coherence_current_bridge_preregistration.md",
        "cd30cdb22d0ad138836afbf1f676b31786c8a9e69cdc42c1baf77603be1fe02b",
    ),
}

REQUIRED_EXACT_FLAGS = (
    "dependency_hashes_exact",
    "w3_42_runtime_checksum_exact",
    "w3_42_runtime_semantics_exact",
    "w3_42_runtime_provenance_exact",
    "sector_transfer_cancellation_exact",
    "candidate_charge_identification_declared",
    "assumed_integrated_balance_solved_exactly",
    "geometry_rate_dictionary_exact",
    "target_residual_exact",
    "zero_source_positive_control_exact",
    "source_mutation_detected",
    "leakage_mutation_detected",
    "selected_energy_transfer_symbols_absent_from_candidate_rate_exact",
    "declared_open_mechanism_markers_exact",
)

MECHANISM_FLAGS = (
    "local_coherence_density_and_flux_from_foundation_derived",
    "eta_coarse_graining_from_foundation_current_derived",
    "Gamma_C_from_foundation_dynamics_and_boundary_derived",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def registered_checksum(path: Path) -> str:
    return path.read_text(encoding="utf-8").split()[0]


def is_zero(expression: sp.Expr) -> bool:
    return sp.simplify(expression) == 0


def compact_plain_text(text: str) -> str:
    return " ".join(text.replace(chr(96), "").split())


def scoped_text(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


def main() -> int:
    dependency_hashes = {
        name: path.is_file() and sha256(path) == expected
        for name, (path, expected) in DEPENDENCIES.items()
    }
    w3_42_result_exists = W3_42_RESULT.is_file()
    w3_42_checksum_exists = W3_42_CHECKSUM.is_file()
    w3_42_actual_sha256 = (
        sha256(W3_42_RESULT) if w3_42_result_exists else None
    )
    w3_42_registered_sha256 = (
        registered_checksum(W3_42_CHECKSUM)
        if w3_42_checksum_exists
        else None
    )
    w3_42_result = (
        json.loads(W3_42_RESULT.read_text(encoding="utf-8"))
        if w3_42_result_exists
        else {}
    )
    w3_42_provenance = w3_42_result.get("provenance", {})
    w3_42_prereg_provenance = w3_42_provenance.get(
        "preregistration", {}
    )
    w3_42_source_provenance = w3_42_provenance.get("source", {})

    w3_46_text = DEPENDENCIES["w3_46_contract"][0].read_text(encoding="utf-8")
    w3_47_text = DEPENDENCIES["w3_47_preregistration"][0].read_text(
        encoding="utf-8"
    )
    w3_48_text = DEPENDENCIES["w3_48_preregistration"][0].read_text(
        encoding="utf-8"
    )
    w3_46_plain = compact_plain_text(w3_46_text)
    w3_47_plain = compact_plain_text(w3_47_text)
    w3_48_plain = compact_plain_text(w3_48_text)
    w3_46_closure = scoped_text(
        w3_46_plain, "- CLOSURE_FLAGS:", "- CROSSCHECK:"
    )
    w3_47_closure = scoped_text(
        w3_47_plain, "- CLOSURE_FLAGS:", "- CROSSCHECK:"
    )
    w3_47_required_false = w3_47_closure[
        w3_47_closure.index("- required false:") :
    ]
    open_markers = {
        "w3_46_names_local_current_as_remaining_target": (
            "The remaining microscopic target is one local continuity/current law"
            in w3_46_plain
        ),
        "w3_46_master_action_or_PDE_false": (
            "master_action_or_resonance_PDE_derived=false" in w3_46_closure
        ),
        "w3_46_energy_transfer_law_false": (
            "energy_transfer_law_derived=false" in w3_46_closure
        ),
        "w3_47_foundation_action_required_false": (
            "foundation_action_derived" in w3_47_required_false
        ),
        "w3_47_resonance_transport_required_false": (
            "I_R_or_J_R_transport_derived" in w3_47_required_false
        ),
        "w3_47_names_microscopic_current_as_open": (
            "The microscopic continuity/current law, sector definitions and"
            in w3_47_plain
        ),
        "w3_47_Q_rel_identity_declared_inherited_not_derived": (
            "This is an inherited identity used to obtain a=eta^(-1/3), "
            "not a newly derived conservation law."
            in w3_47_plain
        ),
    }

    t_ln, t_lr, t_nr = sp.symbols("t_LN t_LR t_NR", real=True)
    q_l = -t_ln - t_lr
    q_n = t_ln - t_nr
    q_r = t_lr + t_nr
    sector_sum = sp.simplify(q_l + q_n + q_r)

    eta_log_rate, h_a, h_A, gamma_c = sp.symbols(
        "eta_log_rate H_a H_A Gamma_C", real=True
    )
    balance_equation = eta_log_rate + 3 * h_a - gamma_c
    geometry_equation = h_A - h_a + eta_log_rate / 2
    solutions = sp.solve(
        (balance_equation, geometry_equation),
        (eta_log_rate, h_a),
        dict=True,
    )

    unique_solution = len(solutions) == 1
    if not unique_solution:
        print(
            json.dumps(
                {
                    "claim_id": CLAIM_ID,
                    "audit_pass": False,
                    "error": "The frozen linear rate system has no unique solution.",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    solution = solutions[0]
    eta_rate_solution = sp.simplify(solution[eta_log_rate])
    h_a_solution = sp.simplify(solution[h_a])
    expected_eta_rate = -sp.Rational(6, 5) * h_A + sp.Rational(2, 5) * gamma_c
    expected_h_a = sp.Rational(2, 5) * h_A + sp.Rational(1, 5) * gamma_c
    target_residual = sp.simplify(
        eta_rate_solution + sp.Rational(6, 5) * h_A
    )

    def rate_residual(candidate_gamma: sp.Expr) -> sp.Expr:
        return sp.simplify(target_residual.subs(gamma_c, candidate_gamma))

    def validate_rate(candidate_gamma: sp.Expr) -> dict[str, object]:
        residual = rate_residual(candidate_gamma)
        return {
            "gamma": str(candidate_gamma),
            "target_residual": str(residual),
            "target_matches": is_zero(residual),
        }

    source_rate, outward_leak_rate = sp.symbols(
        "source_rate outward_leak_rate", positive=True
    )
    canonical_residual = rate_residual(sp.Integer(0))
    source_residual = rate_residual(source_rate)
    leakage_residual = rate_residual(-outward_leak_rate)
    canonical = validate_rate(sp.Integer(0))
    source_mutation = validate_rate(source_rate)
    leakage_mutation = validate_rate(-outward_leak_rate)

    energy_symbols = {t_ln, t_lr, t_nr}
    participation_symbols = (
        eta_rate_solution.free_symbols
        | h_a_solution.free_symbols
        | target_residual.free_symbols
    )

    checks = {
        "dependency_hashes_exact": all(dependency_hashes.values()),
        "w3_42_runtime_checksum_exact": bool(
            w3_42_result_exists
            and w3_42_checksum_exists
            and w3_42_actual_sha256 == w3_42_registered_sha256
        ),
        "w3_42_runtime_semantics_exact": bool(
            w3_42_result.get("status") == "PASS"
            and w3_42_result.get("closure_flags", {}).get(
                "aggregate_identity_pass"
            )
            is True
            and w3_42_result.get("closure_flags", {}).get(
                "d3_geometric_branch_matches_cubic_map_exact"
            )
            is True
            and w3_42_result.get("closure_flags", {}).get(
                "one_coordinate_completeness_nonselection_exact"
            )
            is True
            and w3_42_result.get("physical_closure_flags", {}).get(
                "three_spatial_dimensions_derived"
            )
            is False
        ),
        "w3_42_runtime_provenance_exact": bool(
            w3_42_prereg_provenance.get("sha256")
            == DEPENDENCIES["w3_42_preregistration"][1]
            and w3_42_prereg_provenance.get("expected_sha256")
            == DEPENDENCIES["w3_42_preregistration"][1]
            and w3_42_prereg_provenance.get("valid") is True
            and w3_42_source_provenance.get("sha256")
            == DEPENDENCIES["w3_42_source"][1]
        ),
        "sector_transfer_cancellation_exact": is_zero(sector_sum),
        "candidate_charge_identification_declared": (
            "diagnostic candidate identification is Q_C/Q_C0=eta a^3"
            in w3_48_plain
            and "not derived from Phi_F" in w3_48_plain
        ),
        "assumed_integrated_balance_solved_exactly": is_zero(
            balance_equation.subs(solution)
        ),
        "geometry_rate_dictionary_exact": is_zero(
            geometry_equation.subs(solution)
        ),
        "target_residual_exact": (
            is_zero(eta_rate_solution - expected_eta_rate)
            and is_zero(h_a_solution - expected_h_a)
            and is_zero(target_residual - sp.Rational(2, 5) * gamma_c)
        ),
        "zero_source_positive_control_exact": is_zero(canonical_residual),
        "source_mutation_detected": (
            not source_mutation["target_matches"]
            and is_zero(
                source_residual - sp.Rational(2, 5) * source_rate
            )
        ),
        "leakage_mutation_detected": (
            not leakage_mutation["target_matches"]
            and is_zero(
                leakage_residual + sp.Rational(2, 5) * outward_leak_rate
            )
        ),
        "selected_energy_transfer_symbols_absent_from_candidate_rate_exact": (
            energy_symbols.isdisjoint(participation_symbols)
        ),
        "declared_open_mechanism_markers_exact": all(open_markers.values()),
    }
    exact_audit_pass = all(checks[name] for name in REQUIRED_EXACT_FLAGS)

    mechanism_flags = {
        "local_coherence_density_and_flux_from_foundation_derived": (
            False
            if (
                open_markers["w3_46_names_local_current_as_remaining_target"]
                and open_markers["w3_46_master_action_or_PDE_false"]
            )
            else None
        ),
        "eta_coarse_graining_from_foundation_current_derived": (
            False
            if open_markers[
                "w3_47_Q_rel_identity_declared_inherited_not_derived"
            ]
            else None
        ),
        "Gamma_C_from_foundation_dynamics_and_boundary_derived": (
            False
            if (
                open_markers["w3_46_names_local_current_as_remaining_target"]
                and open_markers["w3_47_resonance_transport_required_false"]
            )
            else None
        ),
    }
    mechanism_open = all(open_markers.values()) and all(
        mechanism_flags[name] is False for name in MECHANISM_FLAGS
    )
    mechanism_closed = False if mechanism_open else None
    status = OPEN_STATUS if exact_audit_pass and mechanism_open else (
        "INVALID_W3_48_AUDIT"
    )

    result = {
        "claim_id": CLAIM_ID,
        "status": status,
        "subsidiary_status": SUBSIDIARY_STATUS if exact_audit_pass else None,
        "audit_pass": exact_audit_pass,
        "mechanism_closed": mechanism_closed,
        "checks": checks,
        "dependency_hashes": dependency_hashes,
        "w3_42_runtime_artifact": {
            "actual_sha256": w3_42_actual_sha256,
            "registered_sha256": w3_42_registered_sha256,
        },
        "declared_open_mechanism_markers": open_markers,
        "closure_flags": mechanism_flags,
        "derived_exactly": {
            "eta_log_rate": str(eta_rate_solution),
            "H_a": str(h_a_solution),
            "target_residual": str(target_residual),
            "sector_transfer_sum": str(sector_sum),
        },
        "controls": {
            "canonical_zero_net_rate": canonical,
            "nonzero_source": source_mutation,
            "outward_leakage": leakage_mutation,
        },
        "conditional_identification": (
            "Q_C/Q_C0=eta_F*a^3 is selected for this diagnostic identity; "
            "it is not derived from Phi_F."
        ),
        "immediate_missing_physical_input": (
            "A foundation rule must construct n_C[Phi_F], j_C[Phi_F], "
            "and their coarse-graining map to eta_F. The resulting dynamics "
            "and boundary conditions must then determine Gamma_C."
        ),
        "writes_files": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if exact_audit_pass and status == OPEN_STATUS else 1


if __name__ == "__main__":
    sys.exit(main())
