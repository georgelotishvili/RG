"""W3-39 exact Genesis energy, phase-sign, and causality gate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_39_GENESIS_ENERGY_PHASE_CAUSALITY"
MODEL_VERSION = "W3-39-v1.0-ENERGY-PHASE-CAUSALITY"
HERE = Path(__file__).resolve().parent
PREREG = HERE / "w3_39_energy_phase_causality_preregistration.md"
OUTPUT = HERE / "w3_39_result.json"
HASH_OUTPUT = HERE / "w3_39_result.sha256"
PINNED_PREREG_SHA256 = "3e73c6d8b09f20d0eda02001cdddcbb03ec08788c4239a9e69436f114be6b45f"

REQUIRED_CONTRACT_FIELDS = {
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS",
    "DOMAIN", "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES",
    "METHOD", "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER",
    "RESIDUAL", "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES",
    "OBSERVABLE_MAP", "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY",
    "BENCHMARK", "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
}

EXPECTED_CLOSURE_KEYS = {
    "antisymmetric_transfer_sum_exact",
    "total_sector_continuity_exact",
    "moving_boundary_leibniz_FTC_exact",
    "regular_center_spherical_ledger_exact",
    "boundary_sweep_and_center_terms_required_exact",
    "rankine_hugoniot_balance_exact",
    "latent_transfer_cancellation_exact",
    "latent_sign_classifier_exact",
    "centered_explosion_breaks_transitive_invariance_exact",
    "branch_keysets_exact",
    "schema_keysets_exact",
    "mutation_controls_pass",
    "aggregate_identity_pass",
}

EXPECTED_PHYSICAL_KEYS = {
    "pregeometric_state_space_derived",
    "genesis_action_or_Hamiltonian_derived",
    "origin_trigger_or_boundary_condition_derived",
    "initial_energy_charge_derived",
    "sector_stress_tensors_derived",
    "sector_transfer_matrix_derived",
    "foundation_volume_measure_derived",
    "foundation_energy_balance_derived",
    "phase_free_energy_EOS_derived",
    "latent_heat_sign_derived",
    "surface_tension_interface_terms_derived",
    "entropy_current_time_arrow_derived",
    "activation_field_and_front_eom_derived",
    "global_centerlessness_derived",
    "physical_cosmic_topology_derived",
    "proto_oscillon_solution_derived",
    "tail_energy_flux_derived",
    "percolation_dynamics_derived",
    "stable_oscillon_spectrum_derived",
    "background_expansion_derived",
    "cadence_history_derived",
    "thermal_history_derived",
    "CMB_BBN_structure_validated",
    "observable_forward_model_derived",
    "data_validated",
}

EXPECTED_NEGATIVE_CONTROL_KEYS = {
    "net_sector_source_detected",
    "omitted_boundary_sweep_detected",
    "omitted_nonregular_center_flux_detected",
    "flipped_outward_flux_sign_detected",
    "omitted_boundary_flux_detected",
    "flipped_interface_jump_sign_detected",
    "double_counted_latent_transfer_detected",
    "center_selected_by_radial_profile_detected",
    "physical_flag_flip_invalidates",
}

EXPECTED_BRANCH_KEYS = {
    "ANTISYMMETRIC_SECTOR_LEDGER",
    "LOCAL_MOVING_BOUNDARY",
    "REGULAR_CENTER",
    "SHARP_INTERFACE_NO_SURFACE_SOURCE",
    "EXOTHERMIC_CONVERSION",
    "NEUTRAL_CONVERSION",
    "ENDOTHERMIC_CONVERSION",
    "CENTERED_RADIAL_FRONT_MUTATION",
    "GLOBAL_CENTERLESS_POSTULATE",
}

EXPECTED_RESULT_KEYS = {
    "schema_version", "claim_id", "claim", "type", "model_version",
    "status", "scope_status", "artifact_valid", "evidence_type",
    "refg_status", "genesis_mechanism_status", "phase_mechanism_status",
    "falsifier_triggered_for_refg", "blocking_reasons", "contract",
    "identities", "sector_transfer_ledger", "moving_boundary_ledger",
    "phase_conversion_ledger", "centered_explosion_witness",
    "branch_classification", "closure_flags", "physical_closure_flags",
    "negative_controls", "provenance", "files",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_zero(value: object) -> bool:
    return sp.simplify(value) == 0


def exact_nonzero(value: object) -> bool:
    return sp.simplify(value) != 0


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
    H = sp.symbols("H_tau", real=True)
    rho_F, rho_C, rho_R = sp.symbols("rho_F rho_C rho_R", real=True)
    P_F, P_C, P_R = sp.symbols("P_F P_C P_R", real=True)
    q_FC, q_FR, q_CR = sp.symbols("q_FC q_FR q_CR", real=True)
    q_F = -q_FC - q_FR
    q_C = q_FC - q_CR
    q_R = q_FR + q_CR
    transfer_sum_residual = sp.simplify(q_F + q_C + q_R)

    drho_F = q_F - 3 * H * (rho_F + P_F)
    drho_C = q_C - 3 * H * (rho_C + P_C)
    drho_R = q_R - 3 * H * (rho_R + P_R)
    total_continuity_residual = sp.simplify(
        drho_F + drho_C + drho_R
        + 3 * H * (rho_F + rho_C + rho_R + P_F + P_C + P_R)
    )

    tau = sp.symbols("tau", real=True)
    r = sp.symbols("r", nonnegative=True)
    R_tau = sp.Function("R")(tau)
    rho_rt = sp.Function("rho")(r, tau)
    flux_primitive = sp.Function("F")(r, tau)
    source_rt = sp.Function("S")(r, tau)
    energy = 4 * sp.pi * sp.Integral(r**2 * rho_rt, (r, 0, R_tau))
    leibniz = sp.diff(energy, tau)
    local_continuity = source_rt - sp.Derivative(flux_primitive, r) / r**2
    after_continuity = leibniz.xreplace(
        {sp.Derivative(rho_rt, tau): local_continuity}
    )
    q_integral = sp.Integral(r**2 * source_rt, (r, 0, R_tau))
    flux_boundary = flux_primitive.subs(r, R_tau)
    flux_center = flux_primitive.subs(r, 0)
    rho_boundary = rho_rt.subs(r, R_tau)
    general_target = 4 * sp.pi * (
        q_integral - flux_boundary + flux_center
        + R_tau**2 * rho_boundary * sp.diff(R_tau, tau)
    )
    moving_boundary_residual = sp.simplify(after_continuity.doit() - general_target)

    R, rho_b = sp.symbols("R rho_b", positive=True)
    J_b, R_dot, Q_V, F_0 = sp.symbols("J_b R_dot Q_V F_0", real=True)
    regular_derived = general_target.xreplace({
        q_integral: Q_V,
        R_tau: R,
        sp.diff(R_tau, tau): R_dot,
        rho_boundary: rho_b,
        flux_boundary: R**2 * J_b,
        flux_center: 0,
    })
    regular_target = 4 * sp.pi * (Q_V - R**2 * J_b + R**2 * rho_b * R_dot)
    regular_center_residual = sp.simplify(regular_derived - regular_target)
    omitted_sweep_residual = sp.simplify(
        regular_target - 4 * sp.pi * (Q_V - R**2 * J_b)
    )
    omitted_center_residual = sp.simplify(
        4 * sp.pi * (Q_V - R**2 * J_b + F_0 + R**2 * rho_b * R_dot)
        - regular_target
    )
    flipped_flux_residual = sp.simplify(
        regular_target - 4 * sp.pi * (Q_V + R**2 * J_b + R**2 * rho_b * R_dot)
    )
    omitted_boundary_flux_residual = sp.simplify(
        regular_target - 4 * sp.pi * (Q_V + R**2 * rho_b * R_dot)
    )

    rho_in, J_in = sp.symbols("rho_in J_in", real=True)
    density_jump, interface_speed = sp.symbols("Delta_rho v_n", real=True)
    rho_out = rho_in + density_jump
    J_out = J_in + interface_speed * density_jump
    actual_density_jump = sp.simplify(rho_out - rho_in)
    actual_flux_jump = sp.simplify(J_out - J_in)
    rankine_hugoniot_residual = sp.simplify(
        interface_speed * actual_density_jump - actual_flux_jump
    )
    jump_definition_residual = sp.simplify(
        actual_density_jump - density_jump
        + actual_flux_jump - interface_speed * density_jump
    )
    flipped_interface_sign_residual = sp.simplify(
        interface_speed * actual_density_jump + actual_flux_jump
    )

    X = sp.Function("X")(tau)
    rho_U = sp.Function("rho_U")(tau)
    rho_A = sp.Function("rho_A")(tau)
    latent = rho_U - rho_A
    rho_phase = (1 - X) * rho_U + X * rho_A
    conversion_rate = sp.diff(X, tau)
    recipient_source = latent * conversion_rate
    background_phase_rate = (
        (1 - X) * sp.diff(rho_U, tau) + X * sp.diff(rho_A, tau)
    )
    conversion_only_rate = sp.simplify(
        sp.diff(rho_phase, tau) - background_phase_rate
    )
    latent_cancellation_residual = sp.simplify(
        conversion_only_rate + recipient_source
    )
    double_count_latent_residual = sp.simplify(
        conversion_only_rate + 2 * recipient_source
    )
    L_positive, X_positive = sp.symbols("L_positive X_positive", positive=True)
    exothermic_positive = (L_positive * X_positive).is_positive is True
    neutral_zero = exact_zero(sp.Integer(0) * X_positive)
    endothermic_negative = (-L_positive * X_positive).is_negative is True

    cycle_vertices = tuple(range(5))
    cycle_edges = {
        tuple(sorted((vertex, (vertex + 1) % 5))) for vertex in cycle_vertices
    }
    translated_edges = {
        tuple(sorted(((left + 1) % 5, (right + 1) % 5)))
        for left, right in cycle_edges
    }
    cycle_translation_automorphism = translated_edges == cycle_edges
    activation_times = tuple(min(vertex, 5 - vertex) for vertex in cycle_vertices)
    translated_times = tuple(activation_times[(vertex - 1) % 5] for vertex in cycle_vertices)
    centered_profile_breaks_invariance = activation_times != translated_times
    unique_selected_center = {
        vertex for vertex, value in enumerate(activation_times)
        if value == min(activation_times)
    } == {0}

    branch_classification = {
        "ANTISYMMETRIC_SECTOR_LEDGER": "EXACT_ASSUMPTION_CONSEQUENCE",
        "LOCAL_MOVING_BOUNDARY": "EXACT_LOCAL_LEDGER",
        "REGULAR_CENTER": "CONDITIONAL_F0_EQUALS_ZERO",
        "SHARP_INTERFACE_NO_SURFACE_SOURCE": "CONDITIONAL_BALANCE",
        "EXOTHERMIC_CONVERSION": "L>0_FOR_XDOT>0__SIGN_ONLY",
        "NEUTRAL_CONVERSION": "L=0_FOR_XDOT>0__SIGN_ONLY",
        "ENDOTHERMIC_CONVERSION": "L<0_FOR_XDOT>0__SIGN_ONLY",
        "CENTERED_RADIAL_FRONT_MUTATION": "INCOMPATIBLE_WITH_TRANSITIVE_INVARIANCE",
        "GLOBAL_CENTERLESS_POSTULATE": "FROZEN_NOT_DERIVED",
    }

    physical_flags = {key: False for key in EXPECTED_PHYSICAL_KEYS}
    physical_flip_invalidates = all(
        not all(
            value is False
            for value in (physical_flags | {key: True}).values()
        )
        for key in EXPECTED_PHYSICAL_KEYS
    )
    nonzero_source_sum = sp.symbols("epsilon_source", nonzero=True)
    negative_controls = {
        "net_sector_source_detected": exact_nonzero(transfer_sum_residual + nonzero_source_sum),
        "omitted_boundary_sweep_detected": exact_nonzero(omitted_sweep_residual),
        "omitted_nonregular_center_flux_detected": exact_nonzero(omitted_center_residual),
        "flipped_outward_flux_sign_detected": exact_nonzero(flipped_flux_residual),
        "omitted_boundary_flux_detected": exact_nonzero(omitted_boundary_flux_residual),
        "flipped_interface_jump_sign_detected": exact_nonzero(flipped_interface_sign_residual),
        "double_counted_latent_transfer_detected": exact_nonzero(double_count_latent_residual),
        "center_selected_by_radial_profile_detected": unique_selected_center and centered_profile_breaks_invariance,
        "physical_flag_flip_invalidates": physical_flip_invalidates,
    }

    closure_flags = {
        "antisymmetric_transfer_sum_exact": exact_zero(transfer_sum_residual),
        "total_sector_continuity_exact": exact_zero(total_continuity_residual),
        "moving_boundary_leibniz_FTC_exact": exact_zero(moving_boundary_residual),
        "regular_center_spherical_ledger_exact": exact_zero(regular_center_residual),
        "boundary_sweep_and_center_terms_required_exact": exact_nonzero(omitted_sweep_residual) and exact_nonzero(omitted_center_residual),
        "rankine_hugoniot_balance_exact": exact_zero(rankine_hugoniot_residual) and exact_zero(jump_definition_residual),
        "latent_transfer_cancellation_exact": exact_zero(latent_cancellation_residual),
        "latent_sign_classifier_exact": exothermic_positive and neutral_zero and endothermic_negative,
        "centered_explosion_breaks_transitive_invariance_exact": cycle_translation_automorphism and centered_profile_breaks_invariance and unique_selected_center,
        "branch_keysets_exact": set(branch_classification) == EXPECTED_BRANCH_KEYS,
        "schema_keysets_exact": False,
        "mutation_controls_pass": all(negative_controls.values()),
        "aggregate_identity_pass": False,
    }

    diagnostics = {
        "identities": {
            "antisymmetric_transfer_sum": sp.sstr(transfer_sum_residual),
            "total_sector_continuity": sp.sstr(total_continuity_residual),
            "moving_boundary_leibniz_FTC": sp.sstr(moving_boundary_residual),
            "regular_center_ledger": sp.sstr(regular_center_residual),
            "rankine_hugoniot": sp.sstr(rankine_hugoniot_residual),
            "latent_transfer": sp.sstr(latent_cancellation_residual),
        },
        "sector_transfer_ledger": {
            "q_F": sp.sstr(q_F), "q_C": sp.sstr(q_C), "q_R": sp.sstr(q_R),
            "sum": sp.sstr(transfer_sum_residual),
            "pair_signs": "q_FC>0:F_to_C; q_FR>0:F_to_R; q_CR>0:C_to_R",
            "status": "POST_ORIGIN_CONDITIONAL_LEDGER_NOT_DERIVED_SECTORS",
        },
        "moving_boundary_ledger": {
            "general": "dE/dtau=4*pi*(Q_V-F_b+F_0+R^2*rho_b*Rdot)",
            "regular_center": "dE/dtau=4*pi*(Q_V-R^2*J_b+R^2*rho_b*Rdot)",
            "constant_energy_condition": "Q_V=R^2*(J_b-rho_b*Rdot) when F_0=0",
            "normalization": "F=r^2*J_r and Q_V=int_0^R r^2*S dr are per unit solid angle",
            "scope": "LOCAL_FLAT_SPHERICAL_PATCH_ONLY",
        },
        "phase_conversion_ledger": {
            "identity": "conversion_only_rate + (rho_U-rho_A)*X_prime = 0",
            "background_terms": "(1-X)*rho_U_prime + X*rho_A_prime retained separately",
            "L_positive": "release_to_recipient__condensation_like",
            "L_zero": "no_latent_transfer",
            "L_negative": "input_required__melting_like",
            "physical_sign": "OPEN_NOT_DERIVED",
        },
        "centered_explosion_witness": {
            "graph": "vertex_transitive_cycle_C5",
            "activation_times": list(activation_times),
            "one_step_translated_times": list(translated_times),
            "translation_is_automorphism": cycle_translation_automorphism,
            "activation_record_is_invariant": not centered_profile_breaks_invariance,
            "selected_center": 0,
            "scope": "CONDITIONAL_FINITE_SYMMETRY_WITNESS_NOT_COSMIC_TOPOLOGY",
        },
        "branch_classification": branch_classification,
        "negative_controls": negative_controls,
    }
    return closure_flags, physical_flags, diagnostics


def build_contract() -> dict[str, object]:
    return {
        "CLAIM_ID": CLAIM_ID,
        "CLAIM": (
            "Post-origin antisymmetric transfers, local continuity, and regular "
            "moving boundaries obey exact energy and phase-sign ledgers; a "
            "single distance-graded centered explosion conflicts with the frozen "
            "global-centerless birth postulate on a transitive witness."
        ),
        "TYPE": "EXACT_CONSERVATION_SIGN_LEDGER_AND_CENTERED_BIRTH_SYMMETRY_NO_GO",
        "MODEL_VERSION": {"id": MODEL_VERSION, "change_boundary": "transfer, boundary, phase, centered-front witness, flags, or scope"},
        "ASSUMPTIONS": "Post-origin sectors, local continuity, regular-center branch, no-surface-source interface, supplied global-centerless postulate.",
        "DOMAIN": "Exact post-origin algebra, local spherical patch, phase sign, finite transitive witness; no pre-birth or observational domain.",
        "CONVENTIONS": {"q_positive": "sector injection", "J_outward_positive": "leaves domain", "Rdot_positive": "boundary expansion", "latent_positive": "release for Xdot>0"},
        "FREEDOM_LEDGER": {
            "current_fitted_effective_dimension": 0,
            "genesis_action_initial_charge": "universal functional/infinite-dimensional",
            "sector_stress_transfer_matrix": "group functional per sector pair",
            "phase_free_energy_interface": "group EOS/free-energy/interface functional",
            "local_seed_boundary_history": "object boundary/flux history",
            "future_thermal_observable_calibration": "data nuisance count zero here",
        },
        "DEPENDENCIES": "None; self-contained.",
        "METHOD": "Exact SymPy transfer, Leibniz/FTC, interface, phase, graph-invariance checks and mutations.",
        "PASS_CONDITION": "All exact flags true, mutations detected, physical flags false.",
        "FAIL_CONDITION": "Ledger/sign/symmetry/schema failure or physical promotion.",
        "FALSIFIER": "Counterexample falsifies this frozen exact gate only.",
        "RESIDUAL": "Exact symbolic zero and invariance predicates.",
        "ERROR_BOUND": "Zero algebraic error; data error N/A.",
        "VALIDITY_HEALTH": "Bookkeeping and one centered-birth symmetry incompatibility only; later local centered fronts remain allowed.",
        "BRANCHES": sorted(EXPECTED_BRANCH_KEYS),
        "OBSERVABLE_MAP": "N/A.",
        "FORWARD_MODEL": "N/A.",
        "DATA_ROLE": "No data read.",
        "IDENTIFIABILITY": "Transfer/boundary/sign identities and one symmetry conflict only.",
        "BENCHMARK": "Source sum 0; Reynolds residual 0; v[rho]=[J]; phase residual 0; C5 radial record noninvariant.",
        "CLOSURE_FLAGS": {"exact": sorted(EXPECTED_CLOSURE_KEYS), "physical_required_false": sorted(EXPECTED_PHYSICAL_KEYS)},
        "CROSSCHECK": "Independent sector sum, general/regular boundary routes, sign branches, explicit translation.",
        "PROVENANCE": "Pinned prereg, source/runtime hashes, UTC, LF, checksum.",
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
        "evidence_type": "EXACT_CONSERVATION_SIGN_AND_CENTERED_BIRTH_SYMMETRY_NO_GO",
        "refg_status": "OPEN", "genesis_mechanism_status": "OPEN_NOT_DERIVED",
        "phase_mechanism_status": "OPEN_SIGN_NOT_SELECTED",
        "falsifier_triggered_for_refg": False,
        "blocking_reasons": [
            "Genesis action, initial charge, and sector stress tensors are not derived.",
            "Phase free energy, latent sign, transfers, and surface terms are open.",
            "The centered-explosion result is a conditional symmetry witness only.",
            "No thermal, cosmological, or observational forward model exists."
        ],
        "contract": contract, "identities": diagnostics["identities"],
        "sector_transfer_ledger": diagnostics["sector_transfer_ledger"],
        "moving_boundary_ledger": diagnostics["moving_boundary_ledger"],
        "phase_conversion_ledger": diagnostics["phase_conversion_ledger"],
        "centered_explosion_witness": diagnostics["centered_explosion_witness"],
        "branch_classification": diagnostics["branch_classification"],
        "closure_flags": closure_flags, "physical_closure_flags": physical_flags,
        "negative_controls": diagnostics["negative_controls"],
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "preregistration": prereg_record,
            "source": {"path": Path(__file__).name, "sha256": sha256(Path(__file__).resolve())},
            "python": platform.python_version(), "sympy": importlib.metadata.version("sympy"),
            "platform": platform.platform(), "line_endings": "LF",
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
    result["scope_status"] = "PASS_EXACT_CONSERVATION_SIGN_AND_CENTERED_BIRTH_SYMMETRY_NO_GO__GENESIS_MECHANISM_OPEN" if valid else "FAIL_EXACT_GATE"
    if not valid:
        raise RuntimeError("W3-39 aggregate gate failed")
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
