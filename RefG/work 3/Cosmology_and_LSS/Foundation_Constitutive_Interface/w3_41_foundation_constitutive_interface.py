"""W3-41 exact foundation constitutive-interface and nonselection gate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_41_FOUNDATION_CONSTITUTIVE_INTERFACE"
MODEL_VERSION = "W3-41-v1.2-FOUNDATION-CONSTITUTIVE-INTERFACE"
CLAIM = (
    r"For a homogeneous one-coordinate foundation cell with volume $V_F=V_0a^3$, "
    "the mechanical generalized pressure conjugate to volume is fixed exactly "
    r"by its energy $E_F(a)$. On the separately declared candidate bridge "
    r"$P_F\equiv\Pi_F$, this gives exact formulas for the relaxation response $\kappa$, "
    "the bulk modulus, the material scale, and the operational scale. The same "
    r"interface admits every positive decreasing $P_F(a)$ and every positive "
    r"$\kappa(a)$, so it does not select a physical constitutive law or a power-law "
    r"exponent. A microscopic foundation dynamical principle, a derived $P_F$--$\Pi_F$ bridge, "
    "and an expansion equation remain necessary."
)
HERE = Path(__file__).resolve().parent
PREREG = HERE / "w3_41_foundation_constitutive_interface_preregistration.md"
OUTPUT = HERE / "w3_41_result.json"
HASH_OUTPUT = HERE / "w3_41_result.sha256"
PINNED_PREREG_SHA256 = (
    "ab852e070871c707ed46e1ac2edde995931c12bd3a0d117e784c258e9f7ba99b"
)
UPSTREAM_DIR = HERE.parent / "Expansion_Relaxation_Causal_Lock"
UPSTREAM_RESULT = UPSTREAM_DIR / "w3_40_result.json"
UPSTREAM_CHECKSUM = UPSTREAM_DIR / "w3_40_result.sha256"
PINNED_W3_40_RESULT_SHA256 = (
    "e8104a664484ea0735387446c94367cca1035877ee6a26413eeddaf158b5be64"
)

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
    "foundation_volume_jacobian_exact",
    "mechanical_pressure_from_energy_exact",
    "bulk_modulus_from_energy_exact",
    "pressure_slope_bulk_modulus_identity_exact",
    "kappa_bulk_modulus_identity_exact",
    "energy_derivative_branch_conditions_exact",
    "pressure_to_energy_reconstruction_exact",
    "kappa_to_pressure_reconstruction_exact",
    "kappa_to_material_scale_exact",
    "kappa_to_operational_scale_exact",
    "power_law_equivalence_exact",
    "power_law_energy_generic_exact",
    "power_law_energy_n3_exact",
    "power_law_energy_n3_limit_exact",
    "power_law_family_nonselection_exact",
    "foundation_pressure_roles_distinct_exact",
    "w3_40_dependency_verified",
    "registered_top_level_keysets_exact",
    "mutation_controls_pass",
    "aggregate_identity_pass",
}

EXPECTED_PHYSICAL_KEYS = {
    "foundation_volume_law_derived",
    "one_coordinate_state_reduction_derived",
    "foundation_pressure_equals_mechanical_pressure_derived",
    "foundation_dynamics_derived",
    "foundation_energy_function_selected",
    "foundation_energy_balance_derived",
    "P_F_of_a_selected",
    "kappa_history_selected",
    "power_law_exponent_selected",
    "material_bridge_microphysics_derived",
    "expansion_equation_derived",
    "a_of_tau_derived",
    "spectroscopic_redshift_forward_map_derived",
    "H_of_z_derived",
    "luminosity_distance_derived",
    "thermal_history_derived",
    "CMB_BBN_BAO_validated",
    "structure_growth_validated",
    "observational_discriminator_validated",
}

EXPECTED_NEGATIVE_KEYS = {
    "wrong_volume_power_detected",
    "pressure_sign_flip_detected",
    "pressure_factor_three_omission_detected",
    "bulk_modulus_sign_flip_detected",
    "kappa_factor_three_omission_detected",
    "reconstruction_measure_mutation_detected",
    "kappa_reconstruction_sign_flip_detected",
    "product_operational_scale_detected",
    "generic_energy_n3_singularity_detected",
    "thermal_pressure_conflation_detected",
    "upstream_hash_mutation_detected",
    "physical_bridge_flag_flip_invalidates_scope",
    "selected_exponent_mutation_invalidates_nonselection",
    "registered_keyset_mutation_detected",
}

EXPECTED_NONSELECTION_KEYS = {
    "n1_normalized",
    "n2_normalized",
    "n1_positive",
    "n2_positive",
    "n1_decreasing",
    "n2_decreasing",
    "n1_positive_bulk_modulus",
    "n2_positive_bulk_modulus",
    "distinct_at_a2",
    "selected_exponent",
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
    "bridge_status",
    "falsifier_triggered_for_refg",
    "blocking_reasons",
    "contract",
    "closure_flags",
    "physical_closure_flags",
    "identities",
    "branch_conditions",
    "reconstruction",
    "nonselection",
    "pressure_roles",
    "negative_controls",
    "provenance",
    "files",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_zero(value: object) -> bool:
    return bool(sp.simplify(value) == 0)


def exact_nonzero(value: object) -> bool:
    return bool(sp.simplify(value) != 0)


def exact_keyset(actual: object, expected: set[str]) -> bool:
    return set(actual) == expected


def dependency_hash_chain_valid(
    actual_hash: str, checksum_hash: str, expected_hash: str
) -> bool:
    return bool(actual_hash == checksum_hash == expected_hash)


def physical_scope_valid(flags: dict[str, bool]) -> bool:
    return bool(
        exact_keyset(flags, EXPECTED_PHYSICAL_KEYS)
        and all(value is False for value in flags.values())
    )


def pressure_roles_are_distinct(roles: dict[str, sp.Symbol]) -> bool:
    return bool(
        exact_keyset(roles, {"P_F", "Pi_F", "P_th"})
        and len(set(roles.values())) == 3
    )


def nonselection_record_valid(record: dict[str, object]) -> bool:
    return bool(
        exact_keyset(record, EXPECTED_NONSELECTION_KEYS)
        and record["selected_exponent"] is None
        and all(
            record[key] is True
            for key in EXPECTED_NONSELECTION_KEYS - {"selected_exponent"}
        )
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
        raise RuntimeError("Missing frozen W3-40 dependency")
    actual_hash = sha256(UPSTREAM_RESULT)
    checksum_text = UPSTREAM_CHECKSUM.read_text(encoding="utf-8").strip()
    checksum_hash, checksum_name = checksum_text.split(maxsplit=1)
    data = json.loads(UPSTREAM_RESULT.read_text(encoding="utf-8"))
    semantics = data.get("semantic_constraints", {})
    closures = data.get("closure_flags", {})
    physical = data.get("physical_closure_flags", {})
    checks = {
        "hash_pinned": actual_hash == PINNED_W3_40_RESULT_SHA256,
        "checksum_matches": (
            checksum_hash == actual_hash
            and checksum_name == UPSTREAM_RESULT.name
        ),
        "hash_chain": dependency_hash_chain_valid(
            actual_hash,
            checksum_hash,
            PINNED_W3_40_RESULT_SHA256,
        ),
        "claim_id": data.get("claim_id")
        == "W3_40_EXPANSION_RELAXATION_CAUSAL_LOCK",
        "model_version": data.get("model_version")
        == "W3-40-v1.2-SINGLE-DRIVER-EXPANSION-RELAXATION-CAUSAL-LOCK",
        "status": data.get("status") == "PASS",
        "scope_status": data.get("scope_status")
        == "PASS_EXACT_CAUSAL_LOCK_DICTIONARY__DYNAMICS_AND_OBSERVABLES_OPEN",
        "single_root": semantics.get("primary_causal_roots") == ["a"],
        "effect_counting": semantics.get("effect_counting")
        == "ONE_PRIMARY_DRIVER_WITH_DEPENDENT_RESPONSE__NO_DOUBLE_COUNTING",
        "nonidentifiability": bool(
            closures.get("A_only_nonidentifiability_exact")
        ),
        "law_open": physical.get("P_F_of_a_derived") is False,
        "action_open": physical.get("foundation_action_derived") is False,
    }
    if not all(checks.values()):
        raise RuntimeError(f"W3-40 dependency verification failed: {checks}")
    return {
        "path": UPSTREAM_RESULT.relative_to(HERE.parent).as_posix(),
        "sha256": actual_hash,
        "expected_sha256": PINNED_W3_40_RESULT_SHA256,
        "checks": checks,
        "valid": True,
    }


def derive_gate() -> tuple[
    dict[str, bool],
    dict[str, bool],
    dict[str, object],
    dict[str, bool],
]:
    a, V0, P0 = sp.symbols("a V_0 P_F0", positive=True)
    E0 = sp.symbols("E_F1", real=True)
    E = sp.Function("E_F")(a)
    E1 = sp.diff(E, a)
    E2 = sp.diff(E, a, 2)

    volume = V0 * a**3
    volume_jacobian = sp.diff(volume, a)
    mechanical_pressure = -E1 / volume_jacobian
    pressure_expected = -E1 / (3 * V0 * a**2)
    pressure_slope = sp.diff(mechanical_pressure, a)
    bulk_modulus = -volume * pressure_slope / volume_jacobian
    bulk_expected = (a * E2 - 2 * E1) / (9 * V0 * a**2)
    kappa_energy = -a * pressure_slope / mechanical_pressure

    residuals = {
        "volume_jacobian": volume_jacobian - 3 * V0 * a**2,
        "mechanical_pressure": mechanical_pressure - pressure_expected,
        "bulk_modulus": bulk_modulus - bulk_expected,
        "pressure_slope_bulk": pressure_slope + 3 * bulk_modulus / a,
        "kappa_bulk": kappa_energy - 3 * bulk_modulus / mechanical_pressure,
        "kappa_energy": kappa_energy - (2 - a * E2 / E1),
    }

    energy_drop, bulk_numerator = sp.symbols(
        "energy_drop bulk_modulus_numerator", positive=True
    )
    positive_bulk_substitutions = {
        E1: -energy_drop,
        E2: (bulk_numerator - 2 * energy_drop) / a,
    }
    positive_pressure = sp.simplify(
        mechanical_pressure.subs(
            positive_bulk_substitutions, simultaneous=True
        )
    )
    positive_bulk = sp.simplify(
        bulk_modulus.subs(
            positive_bulk_substitutions, simultaneous=True
        )
    )
    negative_pressure_slope = sp.simplify(
        pressure_slope.subs(
            positive_bulk_substitutions, simultaneous=True
        )
    )
    branch_conditions = {
        "E_prime_negative": (-energy_drop).is_negative is True,
        "Pi_F_positive": positive_pressure.is_positive is True,
        "bulk_modulus_numerator_positive": bulk_numerator.is_positive is True,
        "K_Pi_positive": positive_bulk.is_positive is True,
        "Pi_F_prime_negative": negative_pressure_slope.is_negative is True,
        "mechanical_equivalence_residual": exact_zero(
            negative_pressure_slope + 3 * positive_bulk / a
        ),
    }

    u = sp.symbols("u", positive=True)
    pressure_function = sp.Function("P_F")
    kappa_function = sp.Function("kappa")
    reconstructed_energy = E0 - 3 * V0 * sp.Integral(
        u**2 * pressure_function(u), (u, 1, a)
    )
    pressure_from_reconstruction = -sp.diff(
        reconstructed_energy, a
    ) / (3 * V0 * a**2)
    kappa_integral = sp.Integral(kappa_function(u) / u, (u, 1, a))
    pressure_from_kappa = P0 * sp.exp(-kappa_integral)
    material_from_kappa = sp.exp(-kappa_integral / 2)
    operational_from_kappa = a / material_from_kappa

    residuals.update(
        {
            "pressure_reconstruction": (
                pressure_from_reconstruction - pressure_function(a)
            ),
            "kappa_reconstruction": (
                -a * sp.diff(sp.log(pressure_from_kappa), a)
                - kappa_function(a)
            ),
            "material_bridge_reconstruction": (
                material_from_kappa**2 - pressure_from_kappa / P0
            ),
            "operational_kappa_slope": (
                a * sp.diff(sp.log(operational_from_kappa), a)
                - 1
                - kappa_function(a) / 2
            ),
        }
    )

    n = sp.symbols("n", positive=True)
    pressure_power = P0 * a ** (-n)
    bulk_power = -a * sp.diff(pressure_power, a) / 3
    kappa_power = -a * sp.diff(sp.log(pressure_power), a)
    material_power = a ** (-n / 2)
    operational_power = a / material_power
    energy_power = E0 - 3 * V0 * P0 * (a ** (3 - n) - 1) / (3 - n)
    pressure_energy_power = -sp.diff(energy_power, a) / (3 * V0 * a**2)
    energy_power_n3 = E0 - 3 * V0 * P0 * sp.log(a)
    pressure_energy_n3 = -sp.diff(
        energy_power_n3, a
    ) / (3 * V0 * a**2)
    energy_power_limit_n3 = sp.limit(energy_power, n, 3)

    residuals.update(
        {
            "power_kappa": kappa_power - n,
            "power_bulk": bulk_power - n * pressure_power / 3,
            "power_material": material_power**2 - pressure_power / P0,
            "power_operational": operational_power - a ** (1 + n / 2),
            "power_energy_generic": pressure_energy_power - pressure_power,
            "power_energy_n3": pressure_energy_n3 - P0 * a ** (-3),
            "power_energy_n3_limit": energy_power_limit_n3 - energy_power_n3,
        }
    )

    pressure_n1 = pressure_power.subs(n, 1)
    pressure_n2 = pressure_power.subs(n, 2)
    witness_a = sp.Integer(2)
    nonselection = {
        "n1_normalized": exact_zero(pressure_n1.subs(a, 1) - P0),
        "n2_normalized": exact_zero(pressure_n2.subs(a, 1) - P0),
        "n1_positive": pressure_n1.is_positive is True,
        "n2_positive": pressure_n2.is_positive is True,
        "n1_decreasing": sp.diff(pressure_n1, a).is_negative is True,
        "n2_decreasing": sp.diff(pressure_n2, a).is_negative is True,
        "n1_positive_bulk_modulus": (
            -a * sp.diff(pressure_n1, a) / 3
        ).is_positive is True,
        "n2_positive_bulk_modulus": (
            -a * sp.diff(pressure_n2, a) / 3
        ).is_positive is True,
        "distinct_at_a2": exact_nonzero(
            pressure_n1.subs(a, witness_a)
            - pressure_n2.subs(a, witness_a)
        ),
        "selected_exponent": None,
    }

    pressure_symbol, mechanical_symbol, thermal_symbol = sp.symbols(
        "P_F Pi_F P_th", positive=True
    )
    pressure_role_symbols = {
        "P_F": pressure_symbol,
        "Pi_F": mechanical_symbol,
        "P_th": thermal_symbol,
    }
    pressure_roles_distinct = pressure_roles_are_distinct(
        pressure_role_symbols
    )
    conflated_pressure_roles = dict(pressure_role_symbols)
    conflated_pressure_roles["P_th"] = pressure_symbol

    wrong_volume = V0 * a**2
    wrong_pressure = -E1 / sp.diff(wrong_volume, a)
    wrong_reconstructed_energy = E0 - 3 * V0 * sp.Integral(
        u * pressure_function(u), (u, 1, a)
    )
    wrong_reconstructed_pressure = -sp.diff(
        wrong_reconstructed_energy, a
    ) / (3 * V0 * a**2)
    wrong_kappa_pressure = P0 * sp.exp(kappa_integral)
    wrong_operational = a * material_from_kappa
    wrong_generic_n3 = energy_power.subs(n, 3)

    physical_flags = {key: False for key in EXPECTED_PHYSICAL_KEYS}
    bridge_flip = dict(physical_flags)
    bridge_flip["foundation_pressure_equals_mechanical_pressure_derived"] = True
    selected_exponent_mutation = dict(nonselection)
    selected_exponent_mutation["selected_exponent"] = 1
    mutated_closure_keys = EXPECTED_CLOSURE_KEYS | {"unexpected_key"}

    negative_controls = {
        "wrong_volume_power_detected": exact_nonzero(
            wrong_pressure - pressure_expected
        ),
        "pressure_sign_flip_detected": exact_nonzero(
            E1 / volume_jacobian - mechanical_pressure
        ),
        "pressure_factor_three_omission_detected": exact_nonzero(
            -E1 / (V0 * a**2) - mechanical_pressure
        ),
        "bulk_modulus_sign_flip_detected": exact_nonzero(
            volume * pressure_slope / volume_jacobian - bulk_modulus
        ),
        "kappa_factor_three_omission_detected": exact_nonzero(
            bulk_modulus / mechanical_pressure - kappa_energy
        ),
        "reconstruction_measure_mutation_detected": exact_nonzero(
            wrong_reconstructed_pressure - pressure_function(a)
        ),
        "kappa_reconstruction_sign_flip_detected": exact_nonzero(
            -a * sp.diff(sp.log(wrong_kappa_pressure), a)
            - kappa_function(a)
        ),
        "product_operational_scale_detected": exact_nonzero(
            a * sp.diff(sp.log(wrong_operational), a)
            - 1
            - kappa_function(a) / 2
        ),
        "generic_energy_n3_singularity_detected": bool(
            wrong_generic_n3.has(sp.zoo)
            or wrong_generic_n3.has(sp.nan)
            or wrong_generic_n3.has(sp.oo)
        ),
        "thermal_pressure_conflation_detected": not pressure_roles_are_distinct(
            conflated_pressure_roles
        ),
        "upstream_hash_mutation_detected": not dependency_hash_chain_valid(
            PINNED_W3_40_RESULT_SHA256,
            PINNED_W3_40_RESULT_SHA256,
            "0" * len(PINNED_W3_40_RESULT_SHA256),
        ),
        "physical_bridge_flag_flip_invalidates_scope": not physical_scope_valid(
            bridge_flip
        ),
        "selected_exponent_mutation_invalidates_nonselection": (
            not nonselection_record_valid(selected_exponent_mutation)
        ),
        "registered_keyset_mutation_detected": not exact_keyset(
            mutated_closure_keys, EXPECTED_CLOSURE_KEYS
        ),
    }

    closure_flags = {
        "foundation_volume_jacobian_exact": exact_zero(
            residuals["volume_jacobian"]
        ),
        "mechanical_pressure_from_energy_exact": exact_zero(
            residuals["mechanical_pressure"]
        ),
        "bulk_modulus_from_energy_exact": exact_zero(
            residuals["bulk_modulus"]
        ),
        "pressure_slope_bulk_modulus_identity_exact": exact_zero(
            residuals["pressure_slope_bulk"]
        ),
        "kappa_bulk_modulus_identity_exact": bool(
            exact_zero(residuals["kappa_bulk"])
            and exact_zero(residuals["kappa_energy"])
        ),
        "energy_derivative_branch_conditions_exact": all(
            value for key, value in branch_conditions.items()
            if key != "mechanical_equivalence_residual"
        )
        and branch_conditions["mechanical_equivalence_residual"],
        "pressure_to_energy_reconstruction_exact": exact_zero(
            residuals["pressure_reconstruction"]
        ),
        "kappa_to_pressure_reconstruction_exact": exact_zero(
            residuals["kappa_reconstruction"]
        ),
        "kappa_to_material_scale_exact": exact_zero(
            residuals["material_bridge_reconstruction"]
        ),
        "kappa_to_operational_scale_exact": exact_zero(
            residuals["operational_kappa_slope"]
        ),
        "power_law_equivalence_exact": all(
            exact_zero(residuals[key])
            for key in (
                "power_kappa",
                "power_bulk",
                "power_material",
                "power_operational",
            )
        ),
        "power_law_energy_generic_exact": exact_zero(
            residuals["power_energy_generic"]
        ),
        "power_law_energy_n3_exact": exact_zero(
            residuals["power_energy_n3"]
        ),
        "power_law_energy_n3_limit_exact": exact_zero(
            residuals["power_energy_n3_limit"]
        ),
        "power_law_family_nonselection_exact": nonselection_record_valid(
            nonselection
        ),
        "foundation_pressure_roles_distinct_exact": pressure_roles_distinct,
        "w3_40_dependency_verified": False,
        "registered_top_level_keysets_exact": False,
        "mutation_controls_pass": all(negative_controls.values()),
        "aggregate_identity_pass": False,
    }

    diagnostics = {
        "residuals": {
            key: sp.sstr(sp.simplify(value)) for key, value in residuals.items()
        },
        "branch_conditions": branch_conditions,
        "reconstruction": {
            "energy_from_pressure": sp.sstr(reconstructed_energy),
            "pressure_from_kappa": sp.sstr(pressure_from_kappa),
            "material_from_kappa": sp.sstr(material_from_kappa),
            "operational_from_kappa": sp.sstr(operational_from_kappa),
            "power_law_energy_generic": sp.sstr(energy_power),
            "power_law_energy_generic_domain": "n>0 AND n!=3",
            "power_law_energy_n3": sp.sstr(energy_power_n3),
            "power_law_energy_limit_n3": sp.sstr(energy_power_limit_n3),
            "status": "FUNCTIONAL_FAMILY_EXACT__NO_MEMBER_SELECTED",
        },
        "nonselection": nonselection,
        "pressure_roles": {
            "P_F": "cadence-controlling foundation scalar",
            "Pi_F": "mechanical generalized pressure conjugate to V_F",
            "P_th": "matter-radiation thermodynamic pressure",
            "candidate_bridge": "P_F=Pi_F is conditional, not derived",
            "roles_distinct": pressure_roles_distinct,
        },
        "negative_controls": negative_controls,
    }
    return closure_flags, physical_flags, diagnostics, negative_controls


def build_contract() -> dict[str, object]:
    return {
        "CLAIM_ID": CLAIM_ID,
        "CLAIM": CLAIM,
        "TYPE": (
            "EXACT_CONDITIONAL_CONSTITUTIVE_DICTIONARY_AND_"
            "RECONSTRUCTION_NONUNIQUENESS_GATE"
        ),
        "MODEL_VERSION": {
            "id": MODEL_VERSION,
            "change_boundary": (
                "Volume map, derivative convention, pressure roles, bridge, "
                "regularity, reconstruction, power audit, dependency, "
                "validator semantics, closure flags, or claim scope."
            ),
        },
        "ASSUMPTIONS": (
            "Verified W3-40; declared but underived V_F=V0*a^3 and "
            "one-coordinate state reduction; E_F(a) is C2 at fixed charges; "
            "Pi_F=-dE_F/dV_F; P_F=Pi_F only on a labeled candidate branch; "
            "P_th distinct; p^2=P_F/P_F0 and A=a/p after P_F is supplied."
        ),
        "DOMAIN": (
            "Regular post-origin homogeneous a>0 interval containing a=1; "
            "assumed one-coordinate adiabatic fixed-charge cell; hidden state "
            "variables are outside this gate, not proved absent."
        ),
        "CONVENTIONS": {
            "pressure_sign": "positive Pi_F=-dE_F/dV_F is compressive",
            "bulk_modulus": "K=-V_F*dPi_F/dV_F",
            "roles": "P_F, Pi_F, and P_th are distinct",
        },
        "FREEDOM_LEDGER": {
            "current_data_fitted_effective_dimension": 0,
            "foundation_dynamics": (
                "open action, Hamiltonian, or equivalent principle"
            ),
            "homogeneous_energy": "one unselected E_F(a,Q) plus omitted states",
            "pressure_bridge": "one unselected P_F--Pi_F map",
            "background_kinetics": "open kinetic functional and initial state",
            "future_observables": "zero instantiated here",
        },
        "DEPENDENCIES": (
            "Pinned W3-40 result/checksum; W3-36 is not an algebraic dependency."
        ),
        "METHOD": (
            "Exact SymPy derivatives, reconstruction, branch signs, two "
            "power-law witnesses, exact n->3 limit, dependency/hash/schema, "
            "and shared-validator mutation checks."
        ),
        "PASS_CONDITION": (
            "Every exact and dependency check passes, nonselection is "
            "constructive, roles remain distinct, and physical flags stay false."
        ),
        "FAIL_CONDITION": (
            "Any check fails or an underived volume law, state reduction, "
            "bridge, exponent, history, observable, thermal result, or data "
            "claim is promoted."
        ),
        "FALSIFIER": (
            "An exact counterexample under frozen assumptions falsifies this "
            "gate; future microscopic dynamics supplies a missing premise."
        ),
        "RESIDUAL": "Exact symbolic zero plus exact Boolean/hash predicates.",
        "ERROR_BOUND": "Zero algebraic/hash error; numerical errors N/A.",
        "VALIDITY_HEALTH": (
            "Constitutive interface and nonselection only; mechanism open."
        ),
        "BRANCHES": [
            "MECHANICAL_STRESS_DICTIONARY",
            "CANDIDATE_FOUNDATION_MECHANICAL_BRIDGE",
            "POSITIVE_BULK_MODULUS_RELAXATION",
            "GENERAL_PRESSURE_RECONSTRUCTION",
            "GENERAL_KAPPA_RECONSTRUCTION",
            "POWER_LAW_AUDIT",
            "HIDDEN_STATE_VARIABLES_OUTSIDE_GATE",
        ],
        "OBSERVABLE_MAP": "N/A: no time or photon observable.",
        "FORWARD_MODEL": "N/A: no synthetic observable or likelihood.",
        "DATA_ROLE": "No data; W3-40 is a logical upstream artifact.",
        "IDENTIFIABILITY": (
            "A supplied E_F and bridge identify P_F; every admissible P_F "
            "reconstructs an E_F up to a constant, so the interface selects none."
        ),
        "BENCHMARK": (
            "Recover Pi_F, K_F, kappa, both functional reconstructions, generic "
            "n!=3 and n=3 power energies, their exact n->3 limit, and distinct "
            "n=1/n=2 positive-bulk-modulus witnesses."
        ),
        "CLOSURE_FLAGS": {
            "exact": sorted(EXPECTED_CLOSURE_KEYS),
            "physical_required_false": sorted(EXPECTED_PHYSICAL_KEYS),
        },
        "CROSSCHECK": (
            "Independent a/V derivatives, inverse reconstructions, n=3 branch "
            "and limit, two-family witness, and shared-validator mutations."
        ),
        "PROVENANCE": (
            "Pinned prereg/W3-40 hashes, canonical LF, runtime versions, "
            "strict JSON, atomic output/checksum."
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
    if sha256(PREREG) != PINNED_PREREG_SHA256:
        raise RuntimeError("Frozen W3-41 preregistration hash changed")
    prereg_claim = registered_claim()
    if prereg_claim != CLAIM:
        raise RuntimeError("Preregistered claim and source claim differ")
    upstream = verify_upstream()
    closure_flags, physical_flags, diagnostics, negative_controls = derive_gate()
    closure_flags["w3_40_dependency_verified"] = bool(upstream["valid"])
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
        "evidence_type": "EXACT_CONDITIONAL_ASSUMPTION_CONSEQUENCE",
        "refg_status": "PHYSICAL_CONSTITUTIVE_CLOSURE_OPEN",
        "bridge_status": "P_F_EQUALS_Pi_F__CANDIDATE_NOT_DERIVED",
        "falsifier_triggered_for_refg": False,
        "blocking_reasons": [
            "No microscopic foundation dynamics derives V_F=V0*a^3.",
            "No derived state reduction proves one coordinate is complete.",
            "No microscopic foundation dynamics selects E_F(a).",
            "No microphysical bridge derives P_F=Pi_F.",
            "No kinetic equation or initial state derives a(t).",
            "No material-bridge microphysics, photon map, or observable model.",
        ],
        "contract": contract,
        "closure_flags": closure_flags,
        "physical_closure_flags": physical_flags,
        "identities": diagnostics["residuals"],
        "branch_conditions": diagnostics["branch_conditions"],
        "reconstruction": diagnostics["reconstruction"],
        "nonselection": diagnostics["nonselection"],
        "pressure_roles": diagnostics["pressure_roles"],
        "negative_controls": negative_controls,
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "preregistration": {
                "path": PREREG.name,
                "sha256": sha256(PREREG),
                "expected_sha256": PINNED_PREREG_SHA256,
                "registered_claim": prereg_claim,
                "valid": True,
            },
            "upstream_w3_40": upstream,
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
    )
    result["artifact_valid"] = artifact_valid
    result["status"] = "PASS" if artifact_valid else "FAIL"
    result["scope_status"] = (
        "PASS_EXACT_CONSTITUTIVE_INTERFACE__RECONSTRUCTION_DEGENERACY_"
        "PROVED__PHYSICAL_BRIDGE_AND_DYNAMICS_OPEN"
        if artifact_valid
        else "FAIL_FOUNDATION_CONSTITUTIVE_INTERFACE_GATE"
    )
    if not artifact_valid:
        raise RuntimeError("W3-41 aggregate gate failed")
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
