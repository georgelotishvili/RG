#!/usr/bin/env python3
"""Exact no-write verifier for the W3-47 conditional participation kernel."""

from __future__ import annotations

import hashlib
import json
import runpy
import sys
from pathlib import Path
from typing import Any

import sympy as sp

sys.dont_write_bytecode = True


HERE = Path(__file__).resolve().parent
COSMOLOGY = HERE.parent
WORK3 = COSMOLOGY.parent
W3_45_DIR = COSMOLOGY / "Active_Phase_Lambda_Interface"

CLAIM_ID = "W3_47_POST_GENESIS_PARTICIPATION_KERNEL"
MODEL_VERSION = "W3-COSMOLOGY-v1.5-PARTICIPATION-BACKGROUND-MATCHING"
PASS_STATUS = (
    "PASS_EXACT_CONDITIONAL_PARTICIPATION_BACKGROUND_MATCHING__"
    "NO_POSITIVE_FIXED_POINT__MICROSCOPIC_ENERGY_TRANSFER_OPEN"
)

PATHS = {
    "w3_47_preregistration": HERE
    / "w3_47_post_genesis_evolution_pressure_coupling_kernel_preregistration.md",
    "w3_46_contract": HERE
    / "w3_46_active_participation_resonance_feedback_contract.md",
    "w3_39_result": WORK3 / "Genesis_Scenario" / "w3_39_result.json",
    "w3_40_result": COSMOLOGY
    / "Expansion_Relaxation_Causal_Lock"
    / "w3_40_result.json",
    "w3_42_preregistration": COSMOLOGY
    / "Foundation_State_Space_and_Volume_Map"
    / "w3_42_foundation_state_space_volume_map_preregistration.md",
    "w3_42_source": COSMOLOGY
    / "Foundation_State_Space_and_Volume_Map"
    / "w3_42_foundation_state_space_volume_map.py",
    "w3_42_result": COSMOLOGY
    / "Foundation_State_Space_and_Volume_Map"
    / "w3_42_result.json",
    "operational_background_source": COSMOLOGY
    / "w3_cosmology_operational_geometric_flrw.py",
    "w3_45_preregistration": W3_45_DIR
    / "w3_45_active_phase_lambda_interface_preregistration.md",
    "w3_45_source": W3_45_DIR
    / "w3_45_active_phase_lambda_interface.py",
}

EXPECTED_HASHES = {
    "w3_47_preregistration":
        "ed1d5b6c2a982cdaafd6739e6a8388219931300b8df92bf015ab2112001049a5",
    "w3_46_contract":
        "0109ed3d5e8daec55dbd0f01f8b05932e6f653373438455c32a3d26378e0f3b2",
    "w3_39_result":
        "ff2440311e2c4ceb5fe5a2393b6730d2a3c2a2c49dd5b2ceaf7e32f0a0ab1160",
    "w3_40_result":
        "e8104a664484ea0735387446c94367cca1035877ee6a26413eeddaf158b5be64",
    "w3_42_preregistration":
        "4cc4674775525a3c76cd8cb282461e5e83b651aff3554de21983568ee7e1f9f1",
    "w3_42_source":
        "0593c452dae764c2b0455d31807a6a81d033bd928db40717a0eec6df5fe04188",
    "operational_background_source":
        "57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055",
    "w3_45_preregistration":
        "a312202a239eb25c24e66920ef400241528639345ce26967e64b96dba6757e79",
    "w3_45_source":
        "4de9c939e25c5176190493232b50dc313d5cc165ca0e11a5a89019dbe33dd3e3",
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

REQUIRED_TRUE_FLAGS = {
    "dependency_hashes_exact",
    "pressure_participation_map_selected",
    "locked_coupling_rule_selected",
    "flatness_constraint_exact",
    "homogeneous_dictionary_exact",
    "state_evolution_pullback_exact",
    "Q_rel_identity_consistency_exact",
    "eta_monotone_on_expanding_branch_exact",
    "no_positive_fixed_point_exact",
    "zero_boundary_stability_classified_exact",
    "late_boundary_powers_derived_exact",
    "sector_transfer_cancellation_exact",
    "stationary_zero_radiative_flux_selected",
    "operational_source_registry_inherited_unchanged_exact",
    "mutation_controls_pass",
    "schema_keysets_exact",
}

REQUIRED_FALSE_FLAGS = {
    "foundation_action_derived",
    "microscopic_energy_density_derived",
    "microscopic_energy_transfer_rate_derived",
    "I_R_or_J_R_transport_derived",
    "foundation_to_operational_source_map_derived",
    "positive_fixed_point_derived",
    "Lambda_value_derived",
    "new_observation_tested",
}

EXPECTED_MUTATIONS = {
    "extra_independent_decay_coefficient",
    "pressure_floor",
    "second_p_factor",
    "positive_participation_fixed_point",
    "noncancelling_internal_transfer",
    "stationary_radiative_leakage",
    "Q_rel_promoted_to_total_energy",
    "P_F_promoted_to_mechanical_work_pressure",
    "duplicate_operational_mass_factor",
    "duplicate_Lambda_source",
    "flipped_relaxation_sign",
}

EXPECTED_DICTIONARY_KEYS = {
    "normalized_foundation_pressure_of_eta",
    "material_scale_p_of_eta",
    "locked_coupling_c_lock_of_eta",
    "foundation_scale_a_of_eta",
    "operational_scale_A_of_eta",
    "participation_eta_of_operational_A",
    "flatness_Omega_Lambda0",
    "operational_E_of_A",
    "operational_E_of_eta",
    "participation_eta_prime_of_eta",
}

EXPECTED_RESIDUAL_KEYS = {
    "flatness_sum",
    "pressure_participation_map",
    "cadence_pressure_bridge",
    "locked_coupling_map",
    "cubic_volume_identity",
    "operational_scale_definition",
    "inverse_participation_map",
    "background_substitution",
    "state_law_pullback",
    "feedback_readout",
    "Q_rel_identity",
    "sector_internal_transfer_sum",
}

EXPECTED_FIXED_POINT_KEYS = {
    "eta_monotone_for_eta_positive_H_A_positive",
    "positive_fixed_point_exists",
    "eta_zero_is_boundary",
    "positive_Lambda_linear_coefficient",
    "positive_Lambda_one_sided_exponential_attractor",
    "zero_Lambda_boundary_nonhyperbolic",
    "late_rate_powers",
    "boundary_reached_at_finite_regular_time",
}

EXPECTED_LATE_POWER_KEYS = {
    "Lambda_dominated",
    "matter_dominated",
    "radiation_dominated",
}

EXPECTED_ENERGY_LEDGER_KEYS = {
    "registry_kind",
    "sector_registry",
    "energy_sum",
    "internal_sources",
    "moving_boundary_template",
    "regular_center_rule",
    "stationary_radiative_flux_rule",
    "Q_rel_role",
    "microscopic_functionals_status",
}

EXPECTED_SECTOR_REGISTRY_KEYS = {"E_L", "E_N", "E_R"}
EXPECTED_INTERNAL_SOURCE_KEYS = {"q_L", "q_N", "q_R", "sum"}

EXPECTED_OPERATIONAL_SOURCE_KEYS = {
    "registry_kind",
    "matter_source",
    "radiation_source",
    "Lambda_source",
    "representation_rule",
    "foundation_to_operational_map_status",
    "source_counts",
}

EXPECTED_SOURCE_COUNT_KEYS = {
    "operational_mass_factor_count",
    "Lambda_source_count",
}

EXPECTED_CANDIDATE_KEYS = {
    "pressure_ratio",
    "locked_coupling",
    "eta_rhs",
    "internal_sources",
    "stationary_radiative_flux_rule",
    "Q_rel_role",
    "P_F_role",
    "operational_mass_factor_count",
    "Lambda_source_count",
}

EXPECTED_VALIDATOR_CHECK_KEYS = {
    "pressure_map_exact",
    "locked_coupling_exact",
    "state_law_exact",
    "internal_transfer_sum_exact",
    "stationary_radiative_flux_rule_selected",
    "Q_rel_role_not_energy",
    "P_F_role_not_mechanical_work_pressure",
    "one_operational_mass_factor",
    "one_Lambda_source",
    "aggregate",
}

EXPECTED_FREEDOM_LEDGER_KEYS = {
    "new_continuous_parameters",
    "new_instantiated_or_fitted_homogeneous_functions",
    "new_fitted_exponents",
    "fixed_structural_choices",
    "open_uninstantiated_microphysical_functionals",
    "inherited_inputs",
}

EXPECTED_REPORT_KEYS = {
    "schema_version",
    "claim_id",
    "model_version",
    "claim_contract",
    "closure_flags",
    "required_true_flags",
    "required_false_flags",
    "dependency_hashes",
    "dependency_checks",
    "dictionary",
    "residuals",
    "fixed_point",
    "energy_ledger",
    "operational_source_registry",
    "canonical_candidate",
    "canonical_validation",
    "negative_controls",
    "negative_control_validations",
    "data_role",
    "decision_status",
    "aggregate_pass",
    "source_sha256",
    "runtime",
    "writes_files",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def registered_checksum(path: Path) -> str:
    return path.read_text(encoding="utf-8").split()[0]


def verify_dependencies() -> tuple[dict[str, str], dict[str, bool], bool]:
    actual = {name: sha256(path) for name, path in PATHS.items()}
    checks = {
        f"{name}_hash": actual[name] == expected
        for name, expected in EXPECTED_HASHES.items()
    }

    checksum_paths = {
        "w3_39_checksum": WORK3
        / "Genesis_Scenario"
        / "w3_39_result.sha256",
        "w3_40_checksum": COSMOLOGY
        / "Expansion_Relaxation_Causal_Lock"
        / "w3_40_result.sha256",
        "w3_42_checksum": COSMOLOGY
        / "Foundation_State_Space_and_Volume_Map"
        / "w3_42_result.sha256",
    }
    for name, checksum_path in checksum_paths.items():
        result_name = name.replace("_checksum", "_result")
        checks[name] = (
            registered_checksum(checksum_path) == actual[result_name]
        )

    w3_39 = load_json(PATHS["w3_39_result"])
    w3_40 = load_json(PATHS["w3_40_result"])
    w3_42 = load_json(PATHS["w3_42_result"])
    w3_42_provenance = w3_42.get("provenance", {})
    w3_42_prereg_provenance = w3_42_provenance.get(
        "preregistration", {}
    )
    w3_42_source_provenance = w3_42_provenance.get("source", {})
    w3_45_namespace = runpy.run_path(
        str(PATHS["w3_45_source"]),
        run_name="w3_45_dependency",
    )
    w3_45 = w3_45_namespace["build_report"]()
    checks.update(
        {
            "w3_39_semantics": bool(
                w3_39.get("status") == "PASS"
                and w3_39["closure_flags"][
                    "antisymmetric_transfer_sum_exact"
                ]
                and w3_39["closure_flags"][
                    "boundary_sweep_and_center_terms_required_exact"
                ]
                and w3_39["closure_flags"]["total_sector_continuity_exact"]
            ),
            "w3_40_semantics": bool(
                w3_40.get("status") == "PASS"
                and w3_40["closure_flags"]["cadence_pressure_bridge_exact"]
                and w3_40["closure_flags"]["operational_scale_identity_exact"]
                and w3_40["closure_flags"]["A_only_nonidentifiability_exact"]
            ),
            "w3_42_semantics": bool(
                w3_42.get("status") == "PASS"
                and w3_42["closure_flags"]["aggregate_identity_pass"]
                and w3_42["closure_flags"][
                    "d3_geometric_branch_matches_cubic_map_exact"
                ]
                and w3_42["closure_flags"][
                    "one_coordinate_completeness_nonselection_exact"
                ]
                and not w3_42["physical_closure_flags"][
                    "three_spatial_dimensions_derived"
                ]
            ),
            "w3_42_provenance": bool(
                w3_42_prereg_provenance.get("sha256")
                == actual["w3_42_preregistration"]
                and w3_42_prereg_provenance.get("expected_sha256")
                == EXPECTED_HASHES["w3_42_preregistration"]
                and w3_42_prereg_provenance.get("valid") is True
                and w3_42_source_provenance.get("sha256")
                == actual["w3_42_source"]
            ),
            "w3_45_semantics": bool(
                w3_45.get("decision_status")
                == (
                    "PASS_EXACT_CONDITIONAL_ACTIVE_PHASE_LAMBDA_INTERFACE__"
                    "ABSOLUTE_ENERGY_NORMALIZATION_AND_LAMBDA_VALUE_OPEN"
                )
                and w3_45["closure_flags"][
                    "active_phase_lambda_interface_pass"
                ]
                and w3_45["closure_flags"][
                    "single_driver_semantics_preserved"
                ]
                and w3_45["closure_flags"][
                    "single_representation_no_double_counting"
                ]
                and not w3_45["closure_flags"]["Lambda_value_derived"]
                and not w3_45["closure_flags"][
                    "foundation_to_operational_matching_derived"
                ]
                and not w3_45["closure_flags"]["new_parameter_fitted"]
                and w3_45["dependency_hashes"]["preregistration"]
                == actual["w3_45_preregistration"]
                and w3_45["source_sha256"] == actual["w3_45_source"]
                and not w3_45["writes_files"]
            ),
        }
    )
    return actual, checks, all(checks.values())


def validate_candidate(
    candidate: dict[str, Any],
    canonical: dict[str, Any],
) -> dict[str, bool]:
    sources = candidate["internal_sources"]
    checks = {
        "pressure_map_exact": bool(
            sp.simplify(
                candidate["pressure_ratio"] - canonical["pressure_ratio"]
            )
            == 0
        ),
        "locked_coupling_exact": bool(
            sp.simplify(
                candidate["locked_coupling"]
                - canonical["locked_coupling"]
            )
            == 0
        ),
        "state_law_exact": bool(
            sp.simplify(candidate["eta_rhs"] - canonical["eta_rhs"]) == 0
        ),
        "internal_transfer_sum_exact": bool(
            sp.simplify(
                sources["q_L"] + sources["q_N"] + sources["q_R"]
            )
            == 0
        ),
        "stationary_radiative_flux_rule_selected": bool(
            candidate["stationary_radiative_flux_rule"]
            == "cycle_average(F_b_rad)=0"
        ),
        "Q_rel_role_not_energy": bool(
            candidate["Q_rel_role"]
            == "inherited_coherence_identity_not_energy"
        ),
        "P_F_role_not_mechanical_work_pressure": bool(
            candidate["P_F_role"]
            == "cadence_controlling_foundation_scalar"
        ),
        "one_operational_mass_factor": bool(
            candidate["operational_mass_factor_count"] == 1
        ),
        "one_Lambda_source": bool(candidate["Lambda_source_count"] == 1),
    }
    checks["aggregate"] = all(checks.values())
    return checks


def serialize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "pressure_ratio": sp.sstr(candidate["pressure_ratio"]),
        "locked_coupling": sp.sstr(candidate["locked_coupling"]),
        "eta_rhs": sp.sstr(candidate["eta_rhs"]),
        "internal_sources": {
            name: sp.sstr(value)
            for name, value in candidate["internal_sources"].items()
        },
        "stationary_radiative_flux_rule":
            candidate["stationary_radiative_flux_rule"],
        "Q_rel_role": candidate["Q_rel_role"],
        "P_F_role": candidate["P_F_role"],
        "operational_mass_factor_count":
            candidate["operational_mass_factor_count"],
        "Lambda_source_count": candidate["Lambda_source_count"],
    }


def derive_kernel() -> dict[str, Any]:
    eta, H_A0 = sp.symbols("eta H_A0", positive=True)
    A_symbol = sp.symbols("A_operational", positive=True)
    Omega_r0, Omega_m0 = sp.symbols(
        "Omega_r0 Omega_m0", nonnegative=True
    )
    Omega_Lambda0 = 1 - Omega_m0 - Omega_r0

    pressure_ratio = eta
    p = sp.sqrt(eta)
    c_lock = p
    a = eta ** sp.Rational(-1, 3)
    A = sp.simplify(a / p)
    eta_inverse = A_symbol ** sp.Rational(-6, 5)

    E_A = sp.sqrt(
        Omega_r0 * A_symbol ** -4
        + Omega_m0 * A_symbol ** -3
        + Omega_Lambda0
    )
    E_eta = sp.sqrt(
        Omega_r0 * eta ** sp.Rational(10, 3)
        + Omega_m0 * eta ** sp.Rational(5, 2)
        + Omega_Lambda0
    )
    eta_rhs = -sp.Rational(6, 5) * H_A0 * eta * E_eta

    T_LN, T_LR, T_NR = sp.symbols("T_LN T_LR T_NR", real=True)
    q_L = -T_LN - T_LR
    q_N = T_LN - T_NR
    q_R = T_LR + T_NR
    internal_sources = {"q_L": q_L, "q_N": q_N, "q_R": q_R}
    transfer_sum = sp.simplify(q_L + q_N + q_R)

    residuals = {
        "flatness_sum": sp.simplify(
            Omega_m0 + Omega_r0 + Omega_Lambda0 - 1
        ),
        "pressure_participation_map": sp.simplify(
            pressure_ratio - eta
        ),
        "cadence_pressure_bridge": sp.simplify(p**2 - pressure_ratio),
        "locked_coupling_map": sp.simplify(c_lock - p),
        "cubic_volume_identity": sp.simplify(eta * a**3 - 1),
        "operational_scale_definition": sp.simplify(A - a / p),
        "inverse_participation_map": sp.simplify(
            eta_inverse.subs(A_symbol, A) - eta
        ),
        "background_substitution": sp.simplify(
            E_A.subs(A_symbol, A) - E_eta
        ),
        "state_law_pullback": sp.simplify(
            sp.diff(sp.log(A), eta) * eta_rhs - H_A0 * E_eta
        ),
        "feedback_readout": sp.simplify(
            eta_rhs
            + sp.Rational(6, 5) * H_A0 * E_eta * c_lock**2
        ),
        "Q_rel_identity": sp.simplify(pressure_ratio * a**3 - 1),
        "sector_internal_transfer_sum": transfer_sum,
    }

    H_A_positive = sp.symbols("H_A_positive", positive=True)
    abstract_rhs = -sp.Rational(6, 5) * H_A_positive * eta
    monotone = abstract_rhs.is_negative is True
    no_positive_fixed_point = bool(
        monotone
        and sp.simplify(
            abstract_rhs / (H_A_positive * eta)
        )
        == -sp.Rational(6, 5)
    )

    branch_rhs = {
        "Lambda_dominated": sp.simplify(
            eta_rhs.subs({Omega_m0: 0, Omega_r0: 0})
        ),
        "matter_dominated": sp.simplify(
            eta_rhs.subs({Omega_m0: 1, Omega_r0: 0})
        ),
        "radiation_dominated": sp.simplify(
            eta_rhs.subs({Omega_m0: 0, Omega_r0: 1})
        ),
    }

    def log_rate_power(rhs: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sp.limit(
                eta * sp.diff(sp.log(-rhs), eta),
                eta,
                0,
                dir="+",
            )
        )

    late_rate_powers = {
        name: log_rate_power(rhs) for name, rhs in branch_rhs.items()
    }
    expected_late_rate_powers = {
        "Lambda_dominated": sp.Integer(1),
        "matter_dominated": sp.Rational(9, 4),
        "radiation_dominated": sp.Rational(8, 3),
    }
    late_powers_exact = all(
        sp.simplify(late_rate_powers[name] - expected) == 0
        for name, expected in expected_late_rate_powers.items()
    )
    boundary_infinite_time = all(
        bool(power >= 1) for power in late_rate_powers.values()
    )

    stability_coefficient = sp.simplify(
        sp.limit(sp.diff(eta_rhs, eta), eta, 0, dir="+")
    )
    expected_stability_coefficient = (
        -sp.Rational(6, 5)
        * H_A0
        * sp.sqrt(Omega_Lambda0)
    )
    lambda_boundary_attractor = bool(
        sp.simplify(
            stability_coefficient - expected_stability_coefficient
        )
        == 0
        and late_rate_powers["Lambda_dominated"] == 1
    )
    zero_lambda_nonhyperbolic = bool(
        sp.limit(
            sp.diff(branch_rhs["matter_dominated"], eta),
            eta,
            0,
            dir="+",
        )
        == 0
        and sp.limit(
            sp.diff(branch_rhs["radiation_dominated"], eta),
            eta,
            0,
            dir="+",
        )
        == 0
        and late_rate_powers["matter_dominated"] > 1
        and late_rate_powers["radiation_dominated"] > 1
    )

    energy_ledger = {
        "registry_kind":
            "declared_conditional_nonoverlapping_bookkeeping_partition",
        "sector_registry": {
            "E_L": "localized_phase_locked_core_content",
            "E_N": "remaining_nonradiative_foundation_response",
            "E_R": "freely_propagating_radiative_content",
        },
        "energy_sum": "E_total=E_L+E_N+E_R",
        "internal_sources": {
            "q_L": sp.sstr(q_L),
            "q_N": sp.sstr(q_N),
            "q_R": sp.sstr(q_R),
            "sum": sp.sstr(transfer_sum),
        },
        "moving_boundary_template":
            "dE_total/dtau=4*pi*(Q_V-F_b+F_0+R^2*rho_b*Rprime)",
        "regular_center_rule": "F_0=0",
        "stationary_radiative_flux_rule":
            "cycle_average(F_b_rad)=0",
        "Q_rel_role": "inherited_coherence_identity_not_energy",
        "microscopic_functionals_status":
            "open_uninstantiated_and_not_derived",
    }

    operational_source_registry = {
        "registry_kind": "inherited_operational_slots_not_foundation_map",
        "matter_source": "one_existing_operational_matter_slot",
        "radiation_source": "one_existing_operational_radiation_slot",
        "Lambda_source": "one_W3_45_Lambda_effective_slot",
        "representation_rule":
            "no_foundation_sector_is_added_again_to_operational_T_mn",
        "foundation_to_operational_map_status": "not_derived",
        "source_counts": {
            "operational_mass_factor_count": 1,
            "Lambda_source_count": 1,
        },
    }

    canonical_candidate = {
        "pressure_ratio": pressure_ratio,
        "locked_coupling": c_lock,
        "eta_rhs": eta_rhs,
        "internal_sources": internal_sources,
        "stationary_radiative_flux_rule":
            energy_ledger["stationary_radiative_flux_rule"],
        "Q_rel_role": energy_ledger["Q_rel_role"],
        "P_F_role": "cadence_controlling_foundation_scalar",
        "operational_mass_factor_count": 1,
        "Lambda_source_count": 1,
    }
    frozen_target = {
        "pressure_ratio": eta,
        "locked_coupling": sp.sqrt(eta),
        "eta_rhs": (
            -sp.Rational(6, 5) * H_A0 * eta * E_eta
        ),
        "internal_sources": {
            "q_L": -T_LN - T_LR,
            "q_N": T_LN - T_NR,
            "q_R": T_LR + T_NR,
        },
        "stationary_radiative_flux_rule":
            "cycle_average(F_b_rad)=0",
        "Q_rel_role": "inherited_coherence_identity_not_energy",
        "P_F_role": "cadence_controlling_foundation_scalar",
        "operational_mass_factor_count": 1,
        "Lambda_source_count": 1,
    }
    canonical_validation = validate_candidate(
        canonical_candidate,
        frozen_target,
    )

    gamma, floor, eta_star = sp.symbols(
        "gamma floor eta_star", positive=True
    )

    def mutate(**changes: Any) -> dict[str, Any]:
        candidate = {
            **canonical_candidate,
            "internal_sources": dict(
                canonical_candidate["internal_sources"]
            ),
        }
        candidate.update(changes)
        return candidate

    noncancelling_sources = dict(internal_sources)
    noncancelling_sources["q_R"] = q_R + T_NR

    mutated_candidates = {
        "extra_independent_decay_coefficient": mutate(
            eta_rhs=gamma * eta_rhs
        ),
        "pressure_floor": mutate(
            pressure_ratio=(eta + floor) / (1 + floor)
        ),
        "second_p_factor": mutate(eta_rhs=eta_rhs * p),
        "positive_participation_fixed_point": mutate(
            eta_rhs=eta_rhs * (eta - eta_star)
        ),
        "noncancelling_internal_transfer": mutate(
            internal_sources=noncancelling_sources
        ),
        "stationary_radiative_leakage": mutate(
            stationary_radiative_flux_rule=
                "cycle_average(F_b_rad)=F_leak_nonzero"
        ),
        "Q_rel_promoted_to_total_energy": mutate(
            Q_rel_role="foundation_total_energy"
        ),
        "P_F_promoted_to_mechanical_work_pressure": mutate(
            P_F_role="mechanical_generalized_work_pressure"
        ),
        "duplicate_operational_mass_factor": mutate(
            operational_mass_factor_count=2
        ),
        "duplicate_Lambda_source": mutate(Lambda_source_count=2),
        "flipped_relaxation_sign": mutate(eta_rhs=-eta_rhs),
    }
    mutation_validations = {
        name: validate_candidate(candidate, frozen_target)
        for name, candidate in mutated_candidates.items()
    }
    mutations = {
        name: not validation["aggregate"]
        for name, validation in mutation_validations.items()
    }

    return {
        "dictionary": {
            "normalized_foundation_pressure_of_eta":
                sp.sstr(pressure_ratio),
            "material_scale_p_of_eta": sp.sstr(p),
            "locked_coupling_c_lock_of_eta": sp.sstr(c_lock),
            "foundation_scale_a_of_eta": sp.sstr(a),
            "operational_scale_A_of_eta": sp.sstr(A),
            "participation_eta_of_operational_A":
                sp.sstr(eta_inverse),
            "flatness_Omega_Lambda0": sp.sstr(Omega_Lambda0),
            "operational_E_of_A": sp.sstr(E_A),
            "operational_E_of_eta": sp.sstr(E_eta),
            "participation_eta_prime_of_eta": sp.sstr(eta_rhs),
        },
        "residuals": {
            name: sp.sstr(value) for name, value in residuals.items()
        },
        "all_residuals_zero": all(
            value == 0 for value in residuals.values()
        ),
        "fixed_point": {
            "eta_monotone_for_eta_positive_H_A_positive": monotone,
            "positive_fixed_point_exists": not no_positive_fixed_point,
            "eta_zero_is_boundary": True,
            "positive_Lambda_linear_coefficient":
                sp.sstr(stability_coefficient),
            "positive_Lambda_one_sided_exponential_attractor":
                lambda_boundary_attractor,
            "zero_Lambda_boundary_nonhyperbolic":
                zero_lambda_nonhyperbolic,
            "late_rate_powers": {
                name: sp.sstr(power)
                for name, power in late_rate_powers.items()
            },
            "boundary_reached_at_finite_regular_time":
                not boundary_infinite_time,
        },
        "late_powers_exact": late_powers_exact,
        "energy_ledger": energy_ledger,
        "operational_source_registry": operational_source_registry,
        "canonical_candidate": serialize_candidate(canonical_candidate),
        "canonical_validation": canonical_validation,
        "mutations": mutations,
        "mutation_validations": mutation_validations,
        "mutation_keys_exact": set(mutations) == EXPECTED_MUTATIONS,
        "mutation_controls_pass": all(mutations.values()),
    }


def build_contract() -> dict[str, Any]:
    return {
        "CLAIM_ID": CLAIM_ID,
        "CLAIM": (
            "The selected normalized pressure and locked-coupling maps pull "
            "the cubic relaxation dictionary and flat expanding operational "
            "background back to one exact eta state law, remain consistent "
            "with the inherited Q_rel identity, exclude a positive fixed "
            "point, and preserve one declared transfer-cancelling "
            "energy-role ledger."
        ),
        "TYPE":
            "EXACT_CONDITIONAL_HOMOGENEOUS_MATCHING_AND_ENERGY_ROLE_LEDGER",
        "MODEL_VERSION": MODEL_VERSION,
        "ASSUMPTIONS": (
            "Positive post-Genesis eta; P_F/P_F0=eta; c_lock=p; inherited "
            "cubic Q_rel closure; flat expanding leading-EH background; "
            "three nonoverlapping energy roles with antisymmetric transfers; "
            "zero cycle-averaged stationary radiative flux."
        ),
        "DOMAIN": (
            "Homogeneous connected expanding post-Genesis eta>0 branch with "
            "Omega_m0>=0, Omega_r0>=0, Omega_m0+Omega_r0<=1, and "
            "Omega_Lambda0=1-Omega_m0-Omega_r0; not Genesis, local strong "
            "field, thermal, PDE, or data domain."
        ),
        "CONVENTIONS": (
            "Prime=d/dtau; H_A=A'/A; positive normalized scales; outward "
            "radiative flux positive; eta_0=a_0=p_0=A_0=c_lock,0=1."
        ),
        "FREEDOM_LEDGER": {
            "new_continuous_parameters": 0,
            "new_instantiated_or_fitted_homogeneous_functions": 0,
            "new_fitted_exponents": 0,
            "fixed_structural_choices": [
                "P_F/P_F0=eta",
                "c_lock=p",
            ],
            "open_uninstantiated_microphysical_functionals": [
                "E_L[Phi_F]",
                "E_N[Phi_F]",
                "E_R[Phi_F]",
                "T_LN(tau), T_LR(tau), T_NR(tau)",
                "boundary flux/stress map",
                "I_R/J_R transport",
            ],
            "inherited_inputs": [
                "H_A0",
                "Omega_m0",
                "Omega_r0",
                "flatness-fixed Omega_Lambda0",
                "reference normalizations",
                "additive time origin",
            ],
        },
        "DEPENDENCIES": sorted(EXPECTED_HASHES),
        "METHOD": (
            "Exact substitution, logarithmic differentiation, sector "
            "summation, sign classification, frozen dependency hashes, "
            "production-RHS rate-power limits, and exact negative mutations "
            "through one candidate validator in a no-write SymPy verifier."
        ),
        "PASS_CONDITION": (
            "Dependencies, flatness, identities, monotonicity, fixed-point "
            "class, Q_rel identity consistency, sector cancellation, the "
            "selected stationary-flux rule, schemas, and every mutation "
            "pass while microscopic flags remain false."
        ),
        "FAIL_CONDITION": (
            "Any required exact check fails or an extra rate, floor, p "
            "factor, positive fixed point, leakage, or duplicate source is "
            "inserted."
        ),
        "FALSIFIER": (
            "Failure of a selected map, a nonzero identity residual, an "
            "interior fixed point on H_A>0, non-cancelling transfer, or "
            "compulsory stationary radiative leakage rejects this kernel."
        ),
        "RESIDUAL": (
            "Exact zero for flatness and every registered symbolic identity; "
            "stationary zero radiative flux is a selected rule, not a "
            "tautological residual."
        ),
        "ERROR_BOUND": (
            "Zero algebraic error; microscopic coarse-graining and "
            "leading-EH truncation errors unquantified; data error N/A."
        ),
        "VALIDITY_HEALTH": (
            "Positive branch, H_A>0, exact dependencies, monotone eta, "
            "declared conditional registry, and explicit boundary/flux terms."
        ),
        "BRANCHES": (
            "Flat expanding branch; eta=0 is a one-sided exponentially "
            "attracting boundary for positive Lambda and a one-sided "
            "nonhyperbolic asymptotic boundary on the pure matter/radiation "
            "limits; positive floors and independent decay timescales are "
            "excluded."
        ),
        "OBSERVABLE_MAP":
            "eta->(P_F,p,a,A), then the existing W3-43 ideal A map.",
        "FORWARD_MODEL": "N/A: no new data model or likelihood.",
        "DATA_ROLE": "NO_DATA_READ_OR_FITTED",
        "IDENTIFIABILITY": (
            "A fixes eta within this selected dictionary; microscopic "
            "participation, node geometry, sector energy functionals, "
            "normalizations, transfer histories, and resonance transport "
            "remain unresolved separately."
        ),
        "BENCHMARK":
            "Zero residual against the cubic relaxation and flat-EH branch.",
        "CLOSURE_FLAGS": {
            "required_true": sorted(REQUIRED_TRUE_FLAGS),
            "required_false": sorted(REQUIRED_FALSE_FLAGS),
        },
        "CROSSCHECK": (
            "Direct and logarithmic-rate pullbacks, independent sector sum, "
            "production-RHS late-power limits, and one-validator mutations."
        ),
        "PROVENANCE": (
            "Frozen local W3-39/40, W3-42 preregistration/source, W3-45/46 "
            "and operational-background SHA-256 dependencies; the generated "
            "W3-42 result is validated at runtime by adjacent checksum, "
            "semantics, and embedded provenance."
        ),
        "FILES": [
            (
                "Cosmology_and_LSS/"
                "Active_Participation_Resonance_Feedback/"
                "w3_47_post_genesis_evolution_pressure_coupling_kernel_"
                "preregistration.md"
            ),
            (
                "Cosmology_and_LSS/"
                "Active_Participation_Resonance_Feedback/"
                "w3_47_post_genesis_evolution_pressure_coupling_kernel.py"
            ),
            (
                "Cosmology_and_LSS/"
                "Active_Participation_Resonance_Feedback/"
                "w3_46_active_participation_resonance_feedback_contract.md"
            ),
            "Cosmology_and_LSS/README.md",
            "Lagrangian_Formulation/RefG_Formal_Proof.md",
        ],
    }


def schema_keysets_exact(report: dict[str, Any]) -> bool:
    expected_dependency_checks = {
        f"{name}_hash" for name in EXPECTED_HASHES
    } | {
        "w3_39_checksum",
        "w3_40_checksum",
        "w3_42_checksum",
        "w3_39_semantics",
        "w3_40_semantics",
        "w3_42_semantics",
        "w3_42_provenance",
        "w3_45_semantics",
    }
    expected_files = {
        (
            "Cosmology_and_LSS/"
            "Active_Participation_Resonance_Feedback/"
            "w3_47_post_genesis_evolution_pressure_coupling_kernel_"
            "preregistration.md"
        ),
        (
            "Cosmology_and_LSS/"
            "Active_Participation_Resonance_Feedback/"
            "w3_47_post_genesis_evolution_pressure_coupling_kernel.py"
        ),
        (
            "Cosmology_and_LSS/"
            "Active_Participation_Resonance_Feedback/"
            "w3_46_active_participation_resonance_feedback_contract.md"
        ),
        "Cosmology_and_LSS/README.md",
        "Lagrangian_Formulation/RefG_Formal_Proof.md",
    }
    energy_ledger = report["energy_ledger"]
    source_registry = report["operational_source_registry"]
    candidate = report["canonical_candidate"]
    checks = [
        set(report) == EXPECTED_REPORT_KEYS,
        set(report["claim_contract"]) == REQUIRED_CONTRACT_FIELDS,
        set(report["claim_contract"]["FREEDOM_LEDGER"])
        == EXPECTED_FREEDOM_LEDGER_KEYS,
        set(report["claim_contract"]["FILES"]) == expected_files,
        set(report["closure_flags"])
        == REQUIRED_TRUE_FLAGS | REQUIRED_FALSE_FLAGS,
        set(report["required_true_flags"]) == REQUIRED_TRUE_FLAGS,
        len(report["required_true_flags"]) == len(REQUIRED_TRUE_FLAGS),
        set(report["required_false_flags"]) == REQUIRED_FALSE_FLAGS,
        len(report["required_false_flags"]) == len(REQUIRED_FALSE_FLAGS),
        set(report["dependency_hashes"]) == set(PATHS),
        set(PATHS) == set(EXPECTED_HASHES) | {"w3_42_result"},
        set(report["dependency_checks"]) == expected_dependency_checks,
        set(report["dictionary"]) == EXPECTED_DICTIONARY_KEYS,
        set(report["residuals"]) == EXPECTED_RESIDUAL_KEYS,
        set(report["fixed_point"]) == EXPECTED_FIXED_POINT_KEYS,
        set(report["fixed_point"]["late_rate_powers"])
        == EXPECTED_LATE_POWER_KEYS,
        set(energy_ledger) == EXPECTED_ENERGY_LEDGER_KEYS,
        set(energy_ledger["sector_registry"])
        == EXPECTED_SECTOR_REGISTRY_KEYS,
        set(energy_ledger["internal_sources"])
        == EXPECTED_INTERNAL_SOURCE_KEYS,
        set(source_registry) == EXPECTED_OPERATIONAL_SOURCE_KEYS,
        set(source_registry["source_counts"])
        == EXPECTED_SOURCE_COUNT_KEYS,
        set(candidate) == EXPECTED_CANDIDATE_KEYS,
        set(candidate["internal_sources"])
        == {"q_L", "q_N", "q_R"},
        set(report["canonical_validation"])
        == EXPECTED_VALIDATOR_CHECK_KEYS,
        set(report["negative_controls"]) == EXPECTED_MUTATIONS,
        set(report["negative_control_validations"])
        == EXPECTED_MUTATIONS,
        all(
            set(validation) == EXPECTED_VALIDATOR_CHECK_KEYS
            for validation in report[
                "negative_control_validations"
            ].values()
        ),
        set(report["runtime"]) == {"python", "sympy"},
    ]
    return all(checks)


def build_report() -> dict[str, Any]:
    dependency_hashes, dependency_checks, dependencies_exact = (
        verify_dependencies()
    )
    derivation = derive_kernel()
    contract = build_contract()

    residuals = derivation["residuals"]
    fixed_point = derivation["fixed_point"]
    mutations = derivation["mutations"]
    canonical_validation = derivation["canonical_validation"]
    source_registry = derivation["operational_source_registry"]

    closure_flags = {
        "dependency_hashes_exact": dependencies_exact,
        "pressure_participation_map_selected":
            canonical_validation["pressure_map_exact"],
        "locked_coupling_rule_selected":
            canonical_validation["locked_coupling_exact"],
        "flatness_constraint_exact":
            residuals["flatness_sum"] == "0",
        "homogeneous_dictionary_exact": bool(
            residuals["pressure_participation_map"] == "0"
            and residuals["cadence_pressure_bridge"] == "0"
            and residuals["locked_coupling_map"] == "0"
            and residuals["cubic_volume_identity"] == "0"
            and residuals["operational_scale_definition"] == "0"
            and residuals["inverse_participation_map"] == "0"
        ),
        "state_evolution_pullback_exact": bool(
            residuals["background_substitution"] == "0"
            and residuals["state_law_pullback"] == "0"
            and residuals["feedback_readout"] == "0"
            and canonical_validation["state_law_exact"]
        ),
        "Q_rel_identity_consistency_exact": bool(
            residuals["Q_rel_identity"] == "0"
            and canonical_validation["Q_rel_role_not_energy"]
        ),
        "eta_monotone_on_expanding_branch_exact": fixed_point[
            "eta_monotone_for_eta_positive_H_A_positive"
        ],
        "no_positive_fixed_point_exact":
            not fixed_point["positive_fixed_point_exists"],
        "zero_boundary_stability_classified_exact": bool(
            fixed_point[
                "positive_Lambda_one_sided_exponential_attractor"
            ]
            and fixed_point["zero_Lambda_boundary_nonhyperbolic"]
            and not fixed_point["boundary_reached_at_finite_regular_time"]
        ),
        "late_boundary_powers_derived_exact": bool(
            derivation["late_powers_exact"]
            and set(fixed_point["late_rate_powers"])
            == EXPECTED_LATE_POWER_KEYS
        ),
        "sector_transfer_cancellation_exact":
            bool(
                residuals["sector_internal_transfer_sum"] == "0"
                and canonical_validation[
                    "internal_transfer_sum_exact"
                ]
            ),
        "stationary_zero_radiative_flux_selected":
            canonical_validation[
                "stationary_radiative_flux_rule_selected"
            ],
        "operational_source_registry_inherited_unchanged_exact": bool(
            source_registry["registry_kind"]
            == "inherited_operational_slots_not_foundation_map"
            and source_registry["Lambda_source"]
            == "one_W3_45_Lambda_effective_slot"
            and source_registry["representation_rule"]
            == (
                "no_foundation_sector_is_added_again_to_operational_T_mn"
            )
            and source_registry["foundation_to_operational_map_status"]
            == "not_derived"
            and canonical_validation["one_operational_mass_factor"]
            and canonical_validation["one_Lambda_source"]
            and dependency_checks["w3_45_semantics"]
        ),
        "mutation_controls_pass": bool(
            derivation["mutation_controls_pass"]
            and derivation["mutation_keys_exact"]
        ),
        "schema_keysets_exact": False,
        **{name: False for name in REQUIRED_FALSE_FLAGS},
    }
    report = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "claim_contract": contract,
        "closure_flags": closure_flags,
        "required_true_flags": sorted(REQUIRED_TRUE_FLAGS),
        "required_false_flags": sorted(REQUIRED_FALSE_FLAGS),
        "dependency_hashes": dependency_hashes,
        "dependency_checks": dependency_checks,
        "dictionary": derivation["dictionary"],
        "residuals": residuals,
        "fixed_point": fixed_point,
        "energy_ledger": derivation["energy_ledger"],
        "operational_source_registry": source_registry,
        "canonical_candidate": derivation["canonical_candidate"],
        "canonical_validation": canonical_validation,
        "negative_controls": mutations,
        "negative_control_validations":
            derivation["mutation_validations"],
        "data_role": "NO_DATA_READ_OR_FITTED",
        "decision_status": "FAIL_W3_47",
        "aggregate_pass": False,
        "source_sha256": sha256(Path(__file__).resolve()),
        "runtime": {
            "python": sys.version.split()[0],
            "sympy": sp.__version__,
        },
        "writes_files": False,
    }
    closure_flags["schema_keysets_exact"] = schema_keysets_exact(report)
    aggregate_pass = bool(
        all(closure_flags[name] for name in REQUIRED_TRUE_FLAGS)
        and all(not closure_flags[name] for name in REQUIRED_FALSE_FLAGS)
        and derivation["all_residuals_zero"]
        and canonical_validation["aggregate"]
    )
    report["aggregate_pass"] = aggregate_pass
    report["decision_status"] = (
        PASS_STATUS if aggregate_pass else "FAIL_W3_47"
    )
    return report


def main() -> None:
    report = build_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["aggregate_pass"] else 1)


if __name__ == "__main__":
    main()
