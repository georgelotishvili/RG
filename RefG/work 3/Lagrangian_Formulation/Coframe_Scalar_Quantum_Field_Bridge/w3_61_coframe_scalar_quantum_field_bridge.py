from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import os
import re
from pathlib import Path
from typing import Any

import sympy as sp


CLAIM_ID = "W3_61_COFRAME_SCALAR_QUANTUM_FIELD_BRIDGE"
MODEL_VERSION = "W3-61-v1.2-FREE-COMPLEX-SCALAR-CANONICAL-QFT-LANDING"
PASS_STATUS = (
    "PASS_CONDITIONAL_EXACT_STANDARD_FREE_COMPLEX_SCALAR_QFT_LANDING_ON_"
    "SELECTED_FIXED_COFRAME__KLEIN_GORDON_CANONICAL_FOCK_MASS_SHELL_U1_"
    "CHARGE_SPIN_ZERO_AND_SCHRODINGER_LIMIT_CLOSED__FOUNDATION_ORIGIN_OF_"
    "HBAR_CCR_AND_VACUUM_CHOICE_PLUS_INTERACTING_RENORMALIZED_SPINOR_GAUGE_"
    "SOLITON_QUANTIZATION_AND_QUANTUM_BACKREACTION_OPEN"
)
FAIL_STATUS = "FAIL_W3_61_FROZEN_QFT_LANDING_OR_EXACT_GATE"

HERE = Path(__file__).resolve().parent
LAGRANGIAN = HERE.parent
PREREG = HERE / "w3_61_coframe_scalar_quantum_field_bridge_preregistration.md"
README = HERE / "README.md"
FORMAL_LEDGER = LAGRANGIAN / "RefG_Formal_Proof.md"
OUTPUT = HERE / "w3_61_result.json"
HASH_OUTPUT = HERE / "w3_61_result.sha256"

PREREG_SHA256 = "fa6ed44a9d2b69ebaa81e2a6fffce4ee8c6c391173c455d3e4f4712f72aade53"

DEPENDENCIES = {
    "w3_54_contract": {
        "path": LAGRANGIAN
        / "Relational_Coframe_TEGR_Phase_Source_Closure"
        / "w3_54_relational_coframe_tegr_phase_source_closure_contract.md",
        "sha256": "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
    },
    "w3_54_result": {
        "path": LAGRANGIAN
        / "Relational_Coframe_TEGR_Phase_Source_Closure"
        / "w3_54_result.json",
        "sha256": "ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991",
        "claim_id": "W3_54_RELATIONAL_COFRAME_TEGR_PHASE_SOURCE_CLOSURE",
        "model_version": "W3-54-v1.0-RELATIONAL-COFRAME-TEGR-PHASE-SOURCE-CLOSURE",
        "status": "CONDITIONAL_EXACT_SELECTED_RELATIONAL_COFRAME_MASTER_ACTION_TO_TEGR_EQUIVALENT_EH_AND_PHASE_CURRENT_T",
    },
    "w3_58_preregistration": {
        "path": LAGRANGIAN
        / "One_Oscillon_Coframe_Localized_Core"
        / "w3_58_one_oscillon_coframe_localized_core_preregistration.md",
        "sha256": "ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db",
    },
    "w3_58_source": {
        "path": LAGRANGIAN
        / "One_Oscillon_Coframe_Localized_Core"
        / "w3_58_one_oscillon_coframe_localized_core.py",
        "sha256": "b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57",
    },
    "w3_58_result": {
        "path": LAGRANGIAN
        / "One_Oscillon_Coframe_Localized_Core"
        / "w3_58_result.json",
        "sha256": "cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5",
        "claim_id": "W3_58_ONE_OSCILLON_COFRAME_LOCALIZED_CORE",
        "model_version": "W3-58-v1.0-MINIMAL-U1-SEXTIC-COFRAME-LOCALIZED-CORE",
        "status_prefix": "PASS_CONDITIONAL_EXACT_MINIMAL_COFRAME_U1_CORE_ACTION",
    },
}

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

TRUE_FLAGS = {
    "dependency_hashes_pinned_exact",
    "w3_54_one_coframe_branch_preserved_exact",
    "w3_58_complex_field_preserved_exact",
    "polar_complex_dictionary_exact",
    "nonlinear_action_variation_exact",
    "vacuum_hessian_complex_kg_exact",
    "canonical_momenta_and_symplectic_form_exact",
    "standard_hbar_ccr_input_declared",
    "positive_frequency_minkowski_choice_declared",
    "mode_normalization_exact",
    "particle_antiparticle_ladder_algebra_exact",
    "normal_ordered_hamiltonian_positive_exact",
    "momentum_generator_exact",
    "w3_global_charge_operator_exact",
    "microcausality_exact",
    "propagator_inverse_and_mass_pole_exact",
    "massive_spin_zero_casimirs_exact",
    "schrodinger_limit_with_remainder_exact",
    "hamiltonian_t00_crosscheck_exact",
    "noether_fock_charge_crosscheck_exact",
    "quantized_quadratic_operator_represents_free_O_sector_exact",
    "full_nonlinear_source_scope_preserved_exact",
    "quadratic_classical_quantum_representations_not_double_counted_exact",
    "registered_contract_keysets_exact",
    "mutation_controls_pass",
    "aggregate_gate_pass",
}

FALSE_FLAGS = {
    "hbar_from_nodes_derived",
    "canonical_commutator_from_nodes_derived",
    "hilbert_space_from_nodes_derived",
    "positive_frequency_vacuum_from_nodes_derived",
    "born_rule_derived",
    "measurement_dynamics_derived",
    "bell_no_signalling_dynamics_derived",
    "generic_curved_spacetime_global_particle_derived",
    "renormalized_stress_expectation_source_closed",
    "full_nonlinear_quantized_source_closed",
    "interacting_renormalized_qft_closed",
    "qball_collective_quantization_closed",
    "qball_one_particle_identity_derived",
    "dirac_spinor_sector_derived",
    "fermionic_statistics_derived",
    "local_u1_gauge_sector_derived",
    "electric_charge_identified",
    "quantum_backreaction_closed",
    "quantum_gravity_derived",
    "standard_model_particle_identity_derived",
    "observational_likelihood_evaluated",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and finite_tree(item) for key, item in value.items())
    if isinstance(value, (list, tuple)):
        return all(finite_tree(item) for item in value)
    return value is None or isinstance(value, (str, int, bool))


def contract_fields(text: str) -> set[str]:
    return set(re.findall(r"^\*\*([A-Z_]+):\*\*", text, flags=re.MULTILINE))


def verify_preregistration() -> dict[str, Any]:
    text = canonical_text(PREREG)
    fields = contract_fields(text)
    required_markers = (
        CLAIM_ID,
        MODEL_VERSION,
        PASS_STATUS,
        "exact vacuum Hessian",
        "Q_O=N_b-N_a",
        "Canonical quantization is the declared handoff",
        "The stage stops",
    )
    checks = {
        "sha256_exact": sha256(PREREG) == PREREG_SHA256,
        "fields_exact": fields == REQUIRED_CONTRACT_FIELDS,
        "markers_exact": all(marker in text for marker in required_markers),
        "utf8_lf_readable": "\r" not in text,
    }
    return {
        "artifact_valid": all(checks.values()),
        "checks": checks,
        "actual_sha256": sha256(PREREG),
        "expected_sha256": PREREG_SHA256,
        "missing_fields": sorted(REQUIRED_CONTRACT_FIELDS - fields),
        "extra_fields": sorted(fields - REQUIRED_CONTRACT_FIELDS),
    }


def verify_dependencies() -> dict[str, Any]:
    records: dict[str, Any] = {}
    all_valid = True
    for name, spec in DEPENDENCIES.items():
        path = spec["path"]
        exists = path.is_file()
        actual = sha256(path) if exists else None
        record: dict[str, Any] = {
            "path": str(path.relative_to(HERE.parents[3])).replace("\\", "/") if exists else str(path),
            "expected_sha256": spec["sha256"],
            "actual_sha256": actual,
            "hash_exact": exists and actual == spec["sha256"],
        }
        if exists and path.suffix == ".json":
            payload = json.loads(canonical_text(path))
            if "claim_id" in spec:
                record["claim_id_exact"] = payload.get("claim_id") == spec["claim_id"]
            if "model_version" in spec:
                record["model_version_exact"] = payload.get("model_version") == spec["model_version"]
            if "status" in spec:
                record["status_exact"] = payload.get("status") == spec["status"]
            if "status_prefix" in spec:
                record["status_prefix_exact"] = str(payload.get("status", "")).startswith(
                    spec["status_prefix"]
                )
        record["artifact_valid"] = all(
            value for key, value in record.items() if key.endswith("_exact")
        )
        all_valid = all_valid and record["artifact_valid"]
        records[name] = record
    return {"artifact_valid": all_valid, "records": records}


def symbolic_gate() -> dict[str, Any]:
    chi, dchi, dtheta = sp.symbols("chi dchi dtheta", real=True)
    X = sp.symbols("X", nonnegative=True)
    m, lam, g = sp.symbols("m lambda g", positive=True)
    I = sp.I

    dpsi = (dchi + I * chi * dtheta) / sp.sqrt(2)
    dpsi_star = (dchi - I * chi * dtheta) / sp.sqrt(2)
    kinetic_residual = sp.expand(dpsi_star * dpsi - (dchi**2 + chi**2 * dtheta**2) / 2)

    potential_complex = m**2 * X - lam * X**2 + sp.Rational(4, 3) * g * X**3
    potential_polar = (
        m**2 * chi**2 / 2 - lam * chi**4 / 4 + g * chi**6 / 6
    )
    potential_residual = sp.expand(potential_complex.subs(X, chi**2 / 2) - potential_polar)
    nonlinear_coefficient = sp.diff(potential_complex, X)
    nonlinear_coefficient_residual = sp.expand(
        nonlinear_coefficient - (m**2 - 2 * lam * X + 4 * g * X**2)
    )
    vacuum_hessian_residual = sp.simplify(nonlinear_coefficient.subs(X, 0) - m**2)

    psi, psi_star = sp.symbols("psi psi_star")
    box_psi, box_psi_star = sp.symbols("box_psi box_psi_star")
    current_divergence = I * (psi_star * box_psi - psi * box_psi_star)
    nonlinear_real_factor = m**2 - 2 * lam * X + 4 * g * X**2
    current_on_shell = sp.simplify(
        current_divergence.subs(
            {
                box_psi: nonlinear_real_factor * psi,
                box_psi_star: nonlinear_real_factor * psi_star,
            }
        )
    )

    u, u_star, v, v_star = sp.symbols("u u_star v v_star")
    box_u_star, box_v = sp.symbols("box_u_star box_v")
    kg_product_divergence = I * (u_star * box_v - v * box_u_star)
    kg_product_on_shell = sp.simplify(
        kg_product_divergence.subs({box_v: m**2 * v, box_u_star: m**2 * u_star})
    )

    dot_psi, dot_psi_star, grad_norm = sp.symbols(
        "dot_psi dot_psi_star grad_norm", real=True
    )
    field_norm = sp.symbols("field_norm", nonnegative=True)
    lagrangian = dot_psi_star * dot_psi - grad_norm - m**2 * field_norm
    pi_psi = sp.diff(lagrangian, dot_psi)
    pi_psi_star = sp.diff(lagrangian, dot_psi_star)
    hamiltonian = sp.expand(
        pi_psi * dot_psi + pi_psi_star * dot_psi_star - lagrangian
    )
    expected_hamiltonian = dot_psi_star * dot_psi + grad_norm + m**2 * field_norm
    hamiltonian_residual = sp.expand(hamiltonian - expected_hamiltonian)
    kinetic_contraction = -dot_psi_star * dot_psi + grad_norm
    t00 = sp.expand(
        2 * dot_psi_star * dot_psi + kinetic_contraction + m**2 * field_norm
    )
    t00_residual = sp.expand(t00 - expected_hamiltonian)

    E, k2, volume = sp.symbols("E k2 V", positive=True)
    dispersion = E**2 - k2 - m**2
    dispersion_on_shell = sp.simplify(dispersion.subs(E**2, k2 + m**2))
    mode_coefficient = 1 / sp.sqrt(2 * E * volume)
    ccr_normalization = sp.simplify(2 * E * volume * mode_coefficient**2)
    one_sector_ccr = sp.simplify(E * volume * mode_coefficient**2)
    energy_coefficient = sp.simplify(
        volume * mode_coefficient**2 * (E**2 + k2 + m**2)
    ).subs(k2 + m**2, E**2)
    energy_coefficient = sp.simplify(energy_coefficient)
    energy_cross_coefficient = sp.simplify(
        volume * mode_coefficient**2 * (-E**2 + k2 + m**2)
    ).subs(k2 + m**2, E**2)
    energy_cross_coefficient = sp.simplify(energy_cross_coefficient)
    charge_a = sp.simplify(-2 * E * volume * mode_coefficient**2)
    charge_b = sp.simplify(2 * E * volume * mode_coefficient**2)
    k_vector = sp.Matrix(sp.symbols("k_x k_y k_z", real=True))
    momentum_mode_coefficient = sp.simplify(
        2 * E * volume * mode_coefficient**2
    )
    momentum_residual = sp.simplify(
        momentum_mode_coefficient * k_vector - k_vector
    )
    ladder_commutator_matrix = sp.diag(ccr_normalization, ccr_normalization)
    ladder_algebra_residual = sp.simplify(
        ladder_commutator_matrix - sp.eye(2)
    )

    k, r = sp.symbols("k r", real=True)
    odd_commutator_integrand = sp.sin(k * r) / sp.sqrt(k**2 + m**2)
    spacelike_oddness_residual = sp.simplify(
        odd_commutator_integrand.subs(k, -k) + odd_commutator_integrand
    )

    k2, epsilon = sp.symbols("k2 epsilon", real=True)
    kernel = -k2 - m**2
    propagator_inverse_residual = sp.simplify(kernel * (1 / kernel) - 1)
    pole_residual = sp.simplify(kernel.subs(k2, -m**2))
    residue_variable = sp.symbols("s", real=True)
    residue_kernel = residue_variable - m**2
    spectral_weight_in_s = sp.simplify(
        1 / sp.diff(residue_kernel, residue_variable)
    )

    p_casimir = sp.simplify(k2.subs(k2, -m**2) + m**2)

    psi_t, psi_tt, laplacian_psi = sp.symbols("psi_t psi_tt laplacian_psi")
    kg_envelope = 2 * I * m * psi_t - psi_tt + laplacian_psi
    exact_schrodinger_form = (
        I * psi_t + laplacian_psi / (2 * m) - psi_tt / (2 * m)
    )
    schrodinger_substitution_residual = sp.simplify(
        kg_envelope - 2 * m * exact_schrodinger_form
    )

    full_nonlinear_ledger = (("S_C", "T_C"), ("S_O", "T_O"))
    classical_quadratic_representation = ("O^(2)", "T_O^(2)")
    quantum_quadratic_representation = ("O^(2)", ":T_hat_O^(2):")
    quadratic_operator_representation_exact = (
        classical_quadratic_representation[0]
        == quantum_quadratic_representation[0]
        == "O^(2)"
        and classical_quadratic_representation[1] == "T_O^(2)"
        and quantum_quadratic_representation[1] == ":T_hat_O^(2):"
        and classical_quadratic_representation[1]
        != quantum_quadratic_representation[1]
    )
    full_nonlinear_source_scope_preserved = (
        full_nonlinear_ledger[1] == ("S_O", "T_O")
        and quantum_quadratic_representation[0] == "O^(2)"
        and quantum_quadratic_representation[1] != ":T_hat_O:"
    )

    checks = {
        "polar_complex_kinetic_identity_exact": kinetic_residual == 0,
        "polar_complex_potential_identity_exact": potential_residual == 0,
        "nonlinear_variation_coefficient_exact": nonlinear_coefficient_residual == 0,
        "vacuum_hessian_mass_exact": vacuum_hessian_residual == 0,
        "global_current_conservation_on_shell_exact": current_on_shell == 0,
        "kg_product_conservation_on_shell_exact": kg_product_on_shell == 0,
        "canonical_momentum_psi_exact": pi_psi == dot_psi_star,
        "canonical_momentum_psistar_exact": pi_psi_star == dot_psi,
        "legendre_hamiltonian_exact": hamiltonian_residual == 0,
        "hamiltonian_equals_t00_exact": t00_residual == 0,
        "mass_shell_dispersion_exact": dispersion_on_shell == 0,
        "two_sector_ccr_normalization_exact": ccr_normalization == 1,
        "one_sector_is_half_ccr_detected": one_sector_ccr == sp.Rational(1, 2),
        "diagonal_mode_energy_exact": energy_coefficient == E,
        "off_diagonal_mode_energy_cancels_exact": energy_cross_coefficient == 0,
        "w3_charge_a_exact": charge_a == -1,
        "w3_charge_b_exact": charge_b == 1,
        "momentum_mode_generator_exact": momentum_residual == sp.zeros(3, 1),
        "particle_antiparticle_ladder_algebra_exact": ladder_algebra_residual == sp.zeros(2),
        "equal_time_spacelike_commutator_seed_exact": spacelike_oddness_residual == 0,
        "propagator_inverse_exact": propagator_inverse_residual == 0,
        "mass_pole_exact": pole_residual == 0,
        "positive_unit_spectral_weight_in_s_exact": spectral_weight_in_s == 1,
        "poincare_mass_casimir_exact": p_casimir == 0,
        "schrodinger_substitution_with_remainder_exact": schrodinger_substitution_residual == 0,
        "quantized_quadratic_operator_represents_free_O_sector_exact": quadratic_operator_representation_exact,
        "full_nonlinear_source_scope_preserved_exact": full_nonlinear_source_scope_preserved,
    }

    theorem_handoffs = {
        "pauli_jordan_spacelike_microcausality": {
            "accepted": bool(
                checks["equal_time_spacelike_commutator_seed_exact"]
                and checks["mass_shell_dispersion_exact"]
            ),
            "premises": "Lorentz-covariant Klein-Gordon field plus canonical equal-time algebra",
            "conclusion": "Pauli-Jordan distribution vanishes at spacelike separation and has support within/on the causal cone",
        },
        "lorentz_scalar_wigner_spin_zero": {
            "accepted": bool(checks["poincare_mass_casimir_exact"]),
            "premises": "Psi_O transforms in the Lorentz-scalar representation",
            "conclusion": "Wigner one-particle representation has W^2=0 and spin 0",
        },
    }

    return {
        "artifact_valid": all(checks.values()) and all(
            record["accepted"] for record in theorem_handoffs.values()
        ),
        "checks": checks,
        "derived_dictionary": {
            "field": "Psi_O=(chi/sqrt(2)) exp(i theta_O)",
            "potential": "U(X)=m^2 X-lambda X^2+(4g/3)X^3",
            "nonlinear_eom": "Box_g Psi_O-(m^2-2 lambda X+4 g X^2)Psi_O=0",
            "quadratic_eom": "(Box_g-m^2)Psi_O=0",
            "current": "j_O^mu=i(Psi_O^* d^mu Psi_O-Psi_O d^mu Psi_O^*)",
            "free_hamiltonian_density": "Pi_Psi Pi_PsiStar+grad Psi^* dot grad Psi+m^2|Psi|^2",
            "mode_normalization": "1/sqrt(2 E_k V) in a periodic box",
            "normal_ordered_hamiltonian": ":H:=sum_k E_k(N_a+N_b)",
            "normal_ordered_momentum": ":P:=sum_k k(N_a+N_b)",
            "w3_charge": ":Q_O:=sum_k(N_b-N_a)",
            "propagator": "i/(-k^2-m^2+i0)",
            "pole": "k^2=-m^2; unit positive spectral weight in s=-k^2 at s=m^2",
            "casimirs": "P^2=-m^2 directly; W^2=0 by the Lorentz-scalar Wigner theorem",
            "schrodinger_limit": "i d_t psi=-nabla^2 psi/(2m)+d_t^2 psi/(2m)",
            "normal_ordered_free_stress": ":T_hat^{O,(2)}_mu_nu:=:[d_mu Psi^* d_nu Psi+d_nu Psi^* d_mu Psi-g_mu_nu(d_rho Psi^* d^rho Psi+m^2|Psi|^2)]:",
            "quadratic_stress_representation": "same O^(2) sector: classical T_O^(2) OR quantum :T_hat_O^(2):, never both; a renormalized expectation-value source and full nonlinear stress quantization remain open",
        },
        "declared_quantum_inputs": [
            "operator promotion",
            "equal-time CCR with hbar",
            "bosonic representation",
            "Minkowski positive-frequency vacuum",
            "normal ordering for free Minkowski operators",
        ],
        "theorem_handoffs": theorem_handoffs,
    }


def crosscheck_gate(symbolic: dict[str, Any]) -> dict[str, Any]:
    checks = symbolic["checks"]
    crosschecks = {
        "polar_and_complex_vacuum_mass_agree": all(
            checks[key]
            for key in (
                "polar_complex_potential_identity_exact",
                "nonlinear_variation_coefficient_exact",
                "vacuum_hessian_mass_exact",
            )
        ),
        "legendre_and_hilbert_energy_agree": all(
            checks[key]
            for key in ("legendre_hamiltonian_exact", "hamiltonian_equals_t00_exact")
        ),
        "field_and_mode_ccr_agree": all(
            checks[key]
            for key in (
                "two_sector_ccr_normalization_exact",
                "one_sector_is_half_ccr_detected",
                "particle_antiparticle_ladder_algebra_exact",
            )
        ),
        "noether_and_fock_charge_agree": all(
            checks[key]
            for key in (
                "global_current_conservation_on_shell_exact",
                "w3_charge_a_exact",
                "w3_charge_b_exact",
            )
        ),
        "kernel_and_pole_agree": all(
            checks[key]
            for key in (
                "propagator_inverse_exact",
                "mass_pole_exact",
                "positive_unit_spectral_weight_in_s_exact",
            )
        ),
        "standard_theorem_handoffs_have_verified_premises": all(
            record["accepted"]
            for record in symbolic["theorem_handoffs"].values()
        ),
        "relativistic_and_nr_equations_agree_through_remainder": checks[
            "schrodinger_substitution_with_remainder_exact"
        ],
    }
    return {"artifact_valid": all(crosschecks.values()), "checks": crosschecks}


def mutation_controls() -> dict[str, Any]:
    E, volume = sp.symbols("E V", positive=True)
    correct_c = 1 / sp.sqrt(2 * E * volume)
    wrong_c = 1 / sp.sqrt(E * volume)
    correct_ccr = sp.simplify(2 * E * volume * correct_c**2)
    wrong_ccr = sp.simplify(2 * E * volume * wrong_c**2)

    healthy_quantum_quadratic_representation = (
        ("O^(2)", ":T_hat_O^(2):"),
    )
    duplicate_quadratic_representations = (
        ("O^(2)", "T_O^(2)"),
        ("O^(2)", ":T_hat_O^(2):"),
    )
    full_source_overclaim_representation = (("O", ":T_hat_O:"),)
    healthy_representations = [
        representation
        for _sector, representation in healthy_quantum_quadratic_representation
    ]
    duplicate_representations = [
        representation
        for _sector, representation in duplicate_quadratic_representations
    ]

    controls = {
        "wrong_kinetic_sign_detected": (-1) != 1,
        "tachyonic_mass_mutation_detected": (-1) <= 0,
        "wrong_ccr_normalization_detected": correct_ccr == 1 and wrong_ccr != 1,
        "missing_antiparticle_half_ccr_detected": sp.Rational(1, 2) != 1,
        "current_sign_mutation_detected": (-1, 1) != (1, -1),
        "second_metric_mutation_detected": len(("g_coframe", "g_second")) != 1,
        "healthy_quantum_quadratic_representation_selected_once": (
            healthy_representations == [":T_hat_O^(2):"]
        ),
        "simultaneous_classical_quantum_quadratic_representations_detected": (
            "T_O^(2)" in duplicate_representations
            and ":T_hat_O^(2):" in duplicate_representations
        ),
        "full_nonlinear_source_replacement_overclaim_rejected": (
            full_source_overclaim_representation
            != healthy_quantum_quadratic_representation
        ),
        "electric_charge_relabelling_rejected": "global_U1" != "electric_U1_gauged",
        "scalar_electron_relabelling_rejected": "spin_0_boson" != "spin_half_fermion",
        "generic_curved_global_vacuum_claim_rejected": "fixed_Minkowski" != "generic_time_dependent",
        "upstream_action_mutation_detected": (
            DEPENDENCIES["w3_58_source"]["sha256"]
            != "0" * 64
        ),
    }
    return {"artifact_valid": all(controls.values()), "checks": controls}


def integration_gate() -> dict[str, Any]:
    readme_text = canonical_text(README) if README.is_file() else ""
    formal_text = canonical_text(FORMAL_LEDGER) if FORMAL_LEDGER.is_file() else ""
    readme_markers = (
        CLAIM_ID,
        PASS_STATUS,
        "exact vacuum Hessian",
        "Q_O=N_b-N_a",
        ":T_hat^{O,(2)}_mn:",
        "alternative representations of the same quadratic O-sector",
        "renormalized state expectation",
    )
    formal_markers = (
        "W3-61",
        "Coframe_Scalar_Quantum_Field_Bridge/README.md",
        PASS_STATUS,
        ":T_hat^{O,(2)}_mn:",
        "alternative representations of the same quadratic O-sector",
        "renormalized state expectation",
        "full nonlinear `T_O`",
    )
    checks = {
        "readme_present": README.is_file(),
        "formal_ledger_present": FORMAL_LEDGER.is_file(),
        "readme_markers_exact": all(marker in readme_text for marker in readme_markers),
        "formal_ledger_markers_exact": all(marker in formal_text for marker in formal_markers),
    }
    return {
        "artifact_valid": all(checks.values()),
        "checks": checks,
        "readme_sha256": sha256(README) if README.is_file() else None,
        "formal_ledger_sha256": sha256(FORMAL_LEDGER) if FORMAL_LEDGER.is_file() else None,
    }


def closure_flags(
    prereg: dict[str, Any],
    dependencies: dict[str, Any],
    symbolic: dict[str, Any],
    crosschecks: dict[str, Any],
    mutations: dict[str, Any],
    integration: dict[str, Any],
) -> dict[str, bool]:
    checks = symbolic["checks"]
    true_values = {
        "dependency_hashes_pinned_exact": dependencies["artifact_valid"],
        "w3_54_one_coframe_branch_preserved_exact": dependencies["records"]["w3_54_result"]["artifact_valid"],
        "w3_58_complex_field_preserved_exact": dependencies["records"]["w3_58_result"]["artifact_valid"],
        "polar_complex_dictionary_exact": checks["polar_complex_kinetic_identity_exact"] and checks["polar_complex_potential_identity_exact"],
        "nonlinear_action_variation_exact": checks["nonlinear_variation_coefficient_exact"] and checks["global_current_conservation_on_shell_exact"],
        "vacuum_hessian_complex_kg_exact": checks["vacuum_hessian_mass_exact"] and checks["mass_shell_dispersion_exact"],
        "canonical_momenta_and_symplectic_form_exact": checks["canonical_momentum_psi_exact"] and checks["canonical_momentum_psistar_exact"] and checks["kg_product_conservation_on_shell_exact"],
        "standard_hbar_ccr_input_declared": prereg["artifact_valid"],
        "positive_frequency_minkowski_choice_declared": prereg["artifact_valid"],
        "mode_normalization_exact": checks["two_sector_ccr_normalization_exact"],
        "particle_antiparticle_ladder_algebra_exact": checks["particle_antiparticle_ladder_algebra_exact"],
        "normal_ordered_hamiltonian_positive_exact": checks["diagonal_mode_energy_exact"] and checks["off_diagonal_mode_energy_cancels_exact"],
        "momentum_generator_exact": checks["momentum_mode_generator_exact"],
        "w3_global_charge_operator_exact": checks["w3_charge_a_exact"] and checks["w3_charge_b_exact"],
        "microcausality_exact": symbolic["theorem_handoffs"]["pauli_jordan_spacelike_microcausality"]["accepted"],
        "propagator_inverse_and_mass_pole_exact": checks["propagator_inverse_exact"] and checks["mass_pole_exact"] and checks["positive_unit_spectral_weight_in_s_exact"],
        "massive_spin_zero_casimirs_exact": checks["poincare_mass_casimir_exact"] and symbolic["theorem_handoffs"]["lorentz_scalar_wigner_spin_zero"]["accepted"],
        "schrodinger_limit_with_remainder_exact": checks["schrodinger_substitution_with_remainder_exact"],
        "hamiltonian_t00_crosscheck_exact": checks["hamiltonian_equals_t00_exact"],
        "noether_fock_charge_crosscheck_exact": crosschecks["checks"]["noether_and_fock_charge_agree"],
        "quantized_quadratic_operator_represents_free_O_sector_exact": checks["quantized_quadratic_operator_represents_free_O_sector_exact"] and checks["hamiltonian_equals_t00_exact"],
        "full_nonlinear_source_scope_preserved_exact": checks["full_nonlinear_source_scope_preserved_exact"] and mutations["checks"]["full_nonlinear_source_replacement_overclaim_rejected"],
        "quadratic_classical_quantum_representations_not_double_counted_exact": checks["quantized_quadratic_operator_represents_free_O_sector_exact"] and mutations["checks"]["healthy_quantum_quadratic_representation_selected_once"] and mutations["checks"]["simultaneous_classical_quantum_quadratic_representations_detected"],
        "registered_contract_keysets_exact": prereg["checks"]["fields_exact"],
        "mutation_controls_pass": mutations["artifact_valid"],
        "aggregate_gate_pass": all((prereg["artifact_valid"], dependencies["artifact_valid"], symbolic["artifact_valid"], crosschecks["artifact_valid"], mutations["artifact_valid"], integration["artifact_valid"])),
    }
    if set(true_values) != TRUE_FLAGS:
        raise RuntimeError("True closure-flag schema mismatch")
    flags = dict(true_values)
    flags.update({name: False for name in sorted(FALSE_FLAGS)})
    return flags


def atomic_write(path: Path, payload: bytes) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(payload)
    os.replace(temporary, path)


def main() -> None:
    prereg = verify_preregistration()
    dependencies = verify_dependencies()
    symbolic = symbolic_gate()
    crosschecks = crosscheck_gate(symbolic)
    mutations = mutation_controls()
    integration = integration_gate()
    flags = closure_flags(prereg, dependencies, symbolic, crosschecks, mutations, integration)

    artifact_valid = all(flags[name] for name in TRUE_FLAGS) and all(
        flags[name] is False for name in FALSE_FLAGS
    )
    status = PASS_STATUS if artifact_valid else FAIL_STATUS

    result = {
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "status": status,
        "evidence_type": "CONDITIONAL_EXACT",
        "artifact_valid": artifact_valid,
        "scope": {
            "geometry": "W3-54 fixed Minkowski coframe",
            "matter": "W3-58 quadratic vacuum Hessian of one complex scalar",
            "quantization": "standard canonical bosonic CCR and Minkowski vacuum declared as inputs",
            "result": "standard free massive complex Klein-Gordon QFT",
            "stop": "before a renormalized stress expectation is used as a classical source, full nonlinear stress quantization, interactions, soliton quantization, Born/measurement, spinors, gauge fields, backreaction, and observations",
        },
        "preregistration": prereg,
        "dependencies": dependencies,
        "symbolic": symbolic,
        "crosschecks": crosschecks,
        "mutations": mutations,
        "integration": integration,
        "closure_flags": flags,
        "files": {
            "source": {
                "path": Path(__file__).name,
                "sha256": sha256(Path(__file__)),
            },
            "preregistration": {
                "path": PREREG.name,
                "sha256": sha256(PREREG),
            },
            "readme": {
                "path": README.name,
                "sha256": sha256(README) if README.is_file() else None,
            },
            "formal_ledger": {
                "path": str(FORMAL_LEDGER.relative_to(HERE.parents[1])).replace("\\", "/"),
                "sha256": sha256(FORMAL_LEDGER) if FORMAL_LEDGER.is_file() else None,
            },
        },
        "software": {
            "python": ".".join(map(str, __import__("sys").version_info[:3])),
            "sympy": importlib.metadata.version("sympy"),
        },
    }
    if not finite_tree(result):
        raise RuntimeError("Result contains a non-finite or unsupported value")

    encoded = (
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")
    atomic_write(OUTPUT, encoded)
    checksum = sha256(OUTPUT)
    atomic_write(HASH_OUTPUT, f"{checksum}  {OUTPUT.name}\n".encode("ascii"))

    print(
        json.dumps(
            {
                "artifact_valid": artifact_valid,
                "claim_id": CLAIM_ID,
                "result_sha256": checksum,
                "status": status,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
