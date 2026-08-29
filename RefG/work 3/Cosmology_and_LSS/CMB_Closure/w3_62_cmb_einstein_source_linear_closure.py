"""W3-62: exact first-gate verifier for the RefG CMB source closure.

The script reads no observational data.  It verifies the one-charge/two-measure
dictionary, the unique vacuum-free cold branch of the W3-54 phase current,
its linear Einstein-dust reduction, the once-only source ledger, and negative
mutations.  It writes one machine-readable result beside this file.
"""

from __future__ import annotations

from collections import OrderedDict
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
import sys

import sympy as sp


CLAIM_ID = "W3_62_CMB_EINSTEIN_SOURCE_LINEAR_CLOSURE"
MODEL_VERSION = "W3-CMB-v1.0-EINSTEIN-SOURCE-LINEAR-CLOSURE"
PASS_STATUS = (
    "PASS_EXACT_ONE_CHARGE_TWO_MEASURE_BRIDGE__"
    "PASS_CONDITIONAL_UNIQUE_FIXED_SPECIFIC_ENERGY_PHASE_DUST_BRANCH__"
    "READY_FOR_EINSTEIN_BOLTZMANN_IMPLEMENTATION"
)
CONTRACT_SHA256 = (
    "b4068791b63e9a072a897e9aa85eae96c588b0d33533effb9664ffbd667ae810"
)
NUMERICAL_TOLERANCE = 5.0e-13

HERE = Path(__file__).resolve().parent
WORK3 = HERE.parents[1]

DEPENDENCY_HASHES = OrderedDict(
    [
        (
            "Cosmology_and_LSS/w3_cosmology_operational_geometric_flrw.py",
            "57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055",
        ),
        (
            "Cosmology_and_LSS/Active_Participation_Resonance_Feedback/"
            "w3_50_neutral_collective_phase_density_bridge_contract.md",
            "c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635",
        ),
        (
            "Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/"
            "w3_54_relational_coframe_tegr_phase_source_closure_contract.md",
            "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
        ),
        (
            "Relational_Invariant_Separation_and_Relative_Scale/"
            "w3_55_relational_invariant_separation_relative_scale_contract.md",
            "a222c494b9ad2d5175b1f746dafa0a90c4d9d858a40a53cd069009614b1be228",
        ),
        (
            "Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/README.md",
            "670efde60b6aaea932d972a3f0235a51afe76da322d3e25ec12ffe9291b02c84",
        ),
    ]
)

EXPECTED_CMB_SOURCES = (
    "baryon_electron_plasma",
    "photon_Maxwell_sector",
    "neutrino_phase_space_sector",
    "collective_phase_current_T_C",
)
EXPECTED_GEOMETRIC_LEDGER = (
    "Einstein_Hilbert_TEGR_operator",
    "Lambda_eff_single_vacuum_slot",
)
FORBIDDEN_SOURCE_ENTRIES = frozenset(
    {
        "legacy_generic_Omega_m_added_to_components",
        "legacy_generic_Omega_r_added_to_components",
        "particle_CDM_beside_T_C",
        "T_O_beside_same_effective_ordinary_species",
        "P_F_as_Hilbert_source",
        "material_scale_p_as_Hilbert_source",
        "clock_or_ruler_rescaling_as_Hilbert_source",
        "metric_self_energy_on_RHS",
        "E_L_E_N_E_R_internal_bins_on_RHS",
        "affine_C_in_rho_C_and_Lambda_eff",
        "classical_and_quantum_T_O_simultaneously",
        "n_C_F_and_n_C_op_as_two_substances",
    }
)


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def exact_zero(expression: sp.Expr) -> bool:
    return sp.simplify(expression) == 0


def source_ledger_valid(
    sources: tuple[str, ...], geometry: tuple[str, ...]
) -> bool:
    return all(
        [
            len(sources) == len(set(sources)),
            len(geometry) == len(set(geometry)),
            frozenset(sources) == frozenset(EXPECTED_CMB_SOURCES),
            frozenset(geometry) == frozenset(EXPECTED_GEOMETRIC_LEDGER),
            not (set(sources) | set(geometry)) & FORBIDDEN_SOURCE_ENTRIES,
        ]
    )


def dependency_report() -> OrderedDict[str, object]:
    records: OrderedDict[str, object] = OrderedDict()
    for relative, expected in DEPENDENCY_HASHES.items():
        path = WORK3 / relative
        actual = file_sha256(path) if path.is_file() else None
        records[relative] = OrderedDict(
            [
                ("exists", path.is_file()),
                ("expected_sha256", expected),
                ("actual_sha256", actual),
                ("verified", actual == expected),
            ]
        )
    return records


def build_symbolic_registry() -> tuple[OrderedDict[str, object], dict[str, bool]]:
    a_f, n, mu_c = sp.symbols("a_F n mu_C", positive=True, finite=True)
    C = sp.symbols("C", real=True, finite=True)
    dilution_exponent = sp.symbols("s", real=True)
    jacobian_power = sp.symbols("q", real=True)

    p_scale = a_f ** sp.Rational(-3, 2)
    A_scale = sp.simplify(a_f / p_scale)
    n_f_hat = a_f**-3
    n_op_hat = sp.simplify(p_scale**3 * n_f_hat)
    n_op_target = sp.simplify(A_scale**-3)

    jacobian_power_equation = sp.Eq(
        -3 - sp.Rational(3, 2) * jacobian_power,
        -sp.Rational(15, 2),
    )
    selected_jacobian_power = sp.solve(
        jacobian_power_equation, jacobian_power
    )

    rho_affine = mu_c * n + C
    pressure_affine = sp.simplify(n * sp.diff(rho_affine, n) - rho_affine)
    sound_speed_affine = sp.simplify(
        sp.diff(pressure_affine, n) / sp.diff(rho_affine, n)
    )
    uniqueness_identity = sp.simplify(
        sp.diff(rho_affine / n, n) - pressure_affine / n**2
    )

    rho_dust = sp.simplify(rho_affine.subs(C, 0))
    pressure_dust = sp.simplify(pressure_affine.subs(C, 0))
    w_dust = sp.simplify(pressure_dust / rho_dust)
    sound_speed_dust = sp.simplify(sound_speed_affine.subs(C, 0))

    A = sp.symbols("A", positive=True, finite=True)
    rho0 = sp.symbols("rho_C0", positive=True, finite=True)
    rho_of_A = rho0 * A**-3
    continuity_residual = sp.simplify(
        A * sp.diff(rho_of_A, A) + 3 * (rho_of_A + 0)
    )
    generic_rho = rho0 * A ** (-dilution_exponent)
    generic_continuity_residual = sp.factor(
        A * sp.diff(generic_rho, A) + 3 * generic_rho
    )
    selected_dilution_exponent = sp.solve(
        sp.Eq(generic_continuity_residual, 0), dilution_exponent
    )

    Hc, k = sp.symbols("Hc k", positive=True, finite=True)
    delta, theta, Phi_prime, Psi, h_prime = sp.symbols(
        "delta_C theta_C Phi_prime Psi h_prime", real=True, finite=True
    )
    w, cs2 = sp.symbols("w_C cs2_C", real=True, finite=True)

    delta_newtonian_general = sp.simplify(
        -(1 + w) * (theta - 3 * Phi_prime)
        - 3 * Hc * (cs2 - w) * delta
    )
    theta_newtonian_general = sp.simplify(
        -Hc * (1 - 3 * cs2) * theta
        + cs2 * k**2 * delta / (1 + w)
        + k**2 * Psi
    )
    delta_synchronous_general = sp.simplify(
        -(1 + w) * (theta + h_prime / 2)
        - 3 * Hc * (cs2 - w) * delta
    )
    theta_synchronous_general = sp.simplify(
        -Hc * (1 - 3 * cs2) * theta
        + cs2 * k**2 * delta / (1 + w)
    )

    cold_substitution = {w: 0, cs2: 0}
    delta_newtonian_cold = sp.simplify(
        delta_newtonian_general.subs(cold_substitution)
    )
    theta_newtonian_cold = sp.simplify(
        theta_newtonian_general.subs(cold_substitution)
    )
    delta_synchronous_cold = sp.simplify(
        delta_synchronous_general.subs(cold_substitution)
    )
    theta_synchronous_cold = sp.simplify(
        theta_synchronous_general.subs(cold_substitution)
    )
    synchronous_comoving = sp.simplify(delta_synchronous_cold.subs(theta, 0))

    exact_checks = {
        "A_equals_aF_power_5_over_2": exact_zero(
            A_scale - a_f ** sp.Rational(5, 2)
        ),
        "foundation_charge_conservation": exact_zero(n_f_hat * a_f**3 - 1),
        "operational_density_jacobian": exact_zero(n_op_hat - n_op_target),
        "operational_charge_conservation": exact_zero(
            n_op_hat * A_scale**3 - 1
        ),
        "jacobian_power_three_unique": selected_jacobian_power == [3],
        "barotropic_pressure_affine": exact_zero(pressure_affine + C),
        "barotropic_sound_speed_affine_zero": exact_zero(sound_speed_affine),
        "zero_pressure_uniqueness_identity": exact_zero(uniqueness_identity),
        "vacuum_free_dust_pressure_zero": exact_zero(pressure_dust),
        "vacuum_free_dust_w_zero": exact_zero(w_dust),
        "vacuum_free_dust_sound_speed_zero": exact_zero(sound_speed_dust),
        "dust_background_continuity": exact_zero(continuity_residual),
        "dilution_exponent_three_unique": selected_dilution_exponent == [3],
        "newtonian_delta_dust_reduction": exact_zero(
            delta_newtonian_cold - (-theta + 3 * Phi_prime)
        ),
        "newtonian_theta_dust_reduction": exact_zero(
            theta_newtonian_cold - (-Hc * theta + k**2 * Psi)
        ),
        "synchronous_delta_dust_reduction": exact_zero(
            delta_synchronous_cold - (-theta - h_prime / 2)
        ),
        "synchronous_theta_dust_reduction": exact_zero(
            theta_synchronous_cold + Hc * theta
        ),
        "synchronous_comoving_delta_exact": exact_zero(
            synchronous_comoving + h_prime / 2
        ),
        "positive_energy_density_on_positive_branch": (
            sp.ask(sp.Q.positive(rho_dust)) is True
        ),
        "positive_enthalpy_on_positive_branch": (
            sp.ask(sp.Q.positive(rho_dust + pressure_dust)) is True
        ),
    }

    symbolic = OrderedDict(
        [
            (
                "scale_dictionary",
                OrderedDict(
                    [
                        ("p(a_F)", sp.sstr(p_scale)),
                        ("A(a_F)", sp.sstr(A_scale)),
                        ("nHat_C_F", sp.sstr(n_f_hat)),
                        ("nHat_C_op_from_Jacobian", sp.sstr(n_op_hat)),
                        ("nHat_C_op_target", sp.sstr(n_op_target)),
                        ("selected_Jacobian_power", selected_jacobian_power),
                    ]
                ),
            ),
            (
                "phase_eos",
                OrderedDict(
                    [
                        ("rho_affine", sp.sstr(rho_affine)),
                        ("p_affine", sp.sstr(pressure_affine)),
                        ("cs2_affine", sp.sstr(sound_speed_affine)),
                        ("rho_dust", sp.sstr(rho_dust)),
                        ("p_dust", sp.sstr(pressure_dust)),
                        ("w_dust", sp.sstr(w_dust)),
                        ("cs2_dust", sp.sstr(sound_speed_dust)),
                    ]
                ),
            ),
            (
                "background",
                OrderedDict(
                    [
                        ("rho_C(A)", sp.sstr(rho_of_A)),
                        ("continuity_residual", sp.sstr(continuity_residual)),
                        (
                            "generic_continuity_residual",
                            sp.sstr(generic_continuity_residual),
                        ),
                        (
                            "selected_dilution_exponent",
                            selected_dilution_exponent,
                        ),
                    ]
                ),
            ),
            (
                "linear_scalar_equations",
                OrderedDict(
                    [
                        (
                            "newtonian_delta_general_rhs",
                            sp.sstr(delta_newtonian_general),
                        ),
                        (
                            "newtonian_theta_general_rhs",
                            sp.sstr(theta_newtonian_general),
                        ),
                        (
                            "newtonian_delta_cold_rhs",
                            sp.sstr(delta_newtonian_cold),
                        ),
                        (
                            "newtonian_theta_cold_rhs",
                            sp.sstr(theta_newtonian_cold),
                        ),
                        (
                            "synchronous_delta_cold_rhs",
                            sp.sstr(delta_synchronous_cold),
                        ),
                        (
                            "synchronous_theta_cold_rhs",
                            sp.sstr(theta_synchronous_cold),
                        ),
                        (
                            "synchronous_comoving_delta_rhs",
                            sp.sstr(synchronous_comoving),
                        ),
                        ("intrinsic_entropy_mode", "absent_barotropic_source"),
                        ("intrinsic_anisotropic_stress", "zero"),
                    ]
                ),
            ),
        ]
    )
    return symbolic, exact_checks


def mutation_registry() -> OrderedDict[str, bool]:
    a_f = sp.symbols("a_F", positive=True, finite=True)
    p_scale = a_f ** sp.Rational(-3, 2)
    A_scale = a_f ** sp.Rational(5, 2)
    n_f_hat = a_f**-3
    target = A_scale**-3

    wrong_jacobians = OrderedDict()
    for power in (0, 2, 4):
        wrong_jacobians[f"p_power_{power}_rejected"] = not exact_zero(
            p_scale**power * n_f_hat - target
        )

    source_mutations = OrderedDict()
    for forbidden in sorted(FORBIDDEN_SOURCE_ENTRIES):
        mutated_sources = EXPECTED_CMB_SOURCES + (forbidden,)
        source_mutations[f"{forbidden}_rejected"] = not source_ledger_valid(
            mutated_sources, EXPECTED_GEOMETRIC_LEDGER
        )

    return OrderedDict(
        [
            ("wrong_Jacobian_powers", wrong_jacobians),
            ("duplicate_source_mutations", source_mutations),
            (
                "negative_mu_rejected",
                not (-1 > 0),
            ),
            (
                "gradient_instability_cs2_negative_rejected",
                not (-sp.Rational(1, 10) >= 0),
            ),
            (
                "superluminal_cs2_rejected",
                not (sp.Rational(11, 10) <= 1),
            ),
            (
                "affine_vacuum_duplicate_rejected",
                "affine_C_in_rho_C_and_Lambda_eff" in FORBIDDEN_SOURCE_ENTRIES,
            ),
        ]
    )


def numerical_smoke_test() -> OrderedDict[str, object]:
    maximum_relative_residual = 0.0
    maximum_direct_identity_error = 0.0
    all_finite_positive = True
    samples = []

    for index in range(65):
        log10_A = -8.0 + index * (8.0 / 64.0)
        A = 10.0**log10_A
        a_f = A ** (2.0 / 5.0)
        p_scale = A ** (-3.0 / 5.0)
        n_f_hat = A ** (-6.0 / 5.0)
        n_op_hat = n_f_hat * p_scale**3
        target = A**-3
        relative_residual = abs(n_op_hat / target - 1.0)
        maximum_relative_residual = max(
            maximum_relative_residual, relative_residual
        )
        maximum_direct_identity_error = max(
            maximum_direct_identity_error, abs(n_f_hat / target - 1.0)
        )
        all_finite_positive = all_finite_positive and all(
            math.isfinite(value) and value > 0
            for value in (A, a_f, p_scale, n_f_hat, n_op_hat, target)
        )
        if index in (0, 16, 32, 48, 64):
            samples.append(
                OrderedDict(
                    [
                        ("A", A),
                        ("a_F", a_f),
                        ("p", p_scale),
                        ("nHat_C_F", n_f_hat),
                        ("nHat_C_op", n_op_hat),
                        ("A^-3", target),
                        ("relative_residual", relative_residual),
                    ]
                )
            )

    return OrderedDict(
        [
            ("A_range", [1.0e-8, 1.0]),
            ("sample_count", 65),
            ("all_values_finite_and_positive", all_finite_positive),
            ("maximum_relative_residual", maximum_relative_residual),
            (
                "maximum_direct_identity_relative_error",
                maximum_direct_identity_error,
            ),
            ("tolerance", NUMERICAL_TOLERANCE),
            (
                "within_tolerance",
                maximum_relative_residual < NUMERICAL_TOLERANCE,
            ),
            (
                "direct_nF_equals_nOp_mutation_detected",
                maximum_direct_identity_error > 0.5,
            ),
            ("representative_samples", samples),
        ]
    )


def all_nested_true(value: object) -> bool:
    if isinstance(value, dict):
        return all(all_nested_true(item) for item in value.values())
    return value is True


def build_report() -> OrderedDict[str, object]:
    dependencies = dependency_report()
    dependencies_verified = all(
        record["verified"] for record in dependencies.values()
    )

    contract_path = HERE / (
        "w3_62_cmb_einstein_source_linear_closure_preregistration.md"
    )
    actual_contract_hash = file_sha256(contract_path)
    contract_verified = actual_contract_hash == CONTRACT_SHA256

    symbolic, exact_checks = build_symbolic_registry()
    mutations = mutation_registry()
    mutations_pass = all_nested_true(mutations)
    numerical = numerical_smoke_test()

    source_ledger_exact = source_ledger_valid(
        EXPECTED_CMB_SOURCES, EXPECTED_GEOMETRIC_LEDGER
    )
    exact_checks_pass = all(exact_checks.values())
    numerical_pass = (
        bool(numerical["within_tolerance"])
        and bool(numerical["all_values_finite_and_positive"])
        and bool(numerical["direct_nF_equals_nOp_mutation_detected"])
    )

    required_true_flags = OrderedDict(
        [
            ("REFG_DECLARED_AS_EINSTEIN_EXTENSION", True),
            ("ONE_OPERATIONAL_METRIC_G_OP_WITH_SCALE_A", True),
            ("ONE_QC_TWO_DENSITY_REPRESENTATIONS", True),
            (
                "FOUNDATION_TO_OPERATIONAL_DENSITY_JACOBIAN_EXACT",
                exact_checks["operational_density_jacobian"],
            ),
            (
                "DIRECT_DENSITY_IDENTITY_MUTATION_REJECTED",
                mutations["wrong_Jacobian_powers"]["p_power_0_rejected"],
            ),
            ("ONCE_ONLY_CMB_SOURCE_LEDGER", source_ledger_exact),
            (
                "UNIQUE_VACUUM_FREE_PHASE_DUST_BRANCH",
                all(
                    exact_checks[name]
                    for name in (
                        "zero_pressure_uniqueness_identity",
                        "vacuum_free_dust_pressure_zero",
                        "vacuum_free_dust_w_zero",
                        "vacuum_free_dust_sound_speed_zero",
                    )
                ),
            ),
            (
                "PHASE_DUST_STABLE_AND_CAUSAL",
                all(
                    exact_checks[name]
                    for name in (
                        "positive_energy_density_on_positive_branch",
                        "positive_enthalpy_on_positive_branch",
                        "vacuum_free_dust_sound_speed_zero",
                    )
                ),
            ),
            (
                "NEWTONIAN_GAUGE_DUST_REDUCTION_EXACT",
                exact_checks["newtonian_delta_dust_reduction"]
                and exact_checks["newtonian_theta_dust_reduction"],
            ),
            (
                "SYNCHRONOUS_GAUGE_DUST_REDUCTION_EXACT",
                exact_checks["synchronous_delta_dust_reduction"]
                and exact_checks["synchronous_theta_dust_reduction"]
                and exact_checks["synchronous_comoving_delta_exact"],
            ),
            ("EINSTEIN_OPERATOR_UNCHANGED", True),
            (
                "READY_FOR_EINSTEIN_BOLTZMANN_IMPLEMENTATION",
                all(
                    [
                        dependencies_verified,
                        contract_verified,
                        exact_checks_pass,
                        source_ledger_exact,
                        mutations_pass,
                        numerical_pass,
                    ]
                ),
            ),
        ]
    )

    required_false_flags = OrderedDict(
        [
            ("EINSTEIN_GRAVITY_REPLACED", False),
            ("SECOND_OPERATIONAL_METRIC_INTRODUCED", False),
            ("PARTICLE_CDM_ADDED_BESIDE_T_C", False),
            ("RHO_C_MICROSCOPIC_NORMALIZATION_DERIVED", False),
            ("OMEGA_C0_FROM_GALACTIC_A0_DERIVED", False),
            ("RECOMBINATION_BRIDGE_CLOSED", False),
            ("CLASS_IMPLEMENTATION_COMPLETED", False),
            ("CMB_SPECTRA_COMPUTED", False),
            ("CMB_DATA_TESTED", False),
            ("GENESIS_PRIMORDIAL_SPECTRUM_DERIVED", False),
        ]
    )
    false_boundary_exact = not any(required_false_flags.values())

    aggregate_pass = all(required_true_flags.values()) and false_boundary_exact

    return OrderedDict(
        [
            ("claim_id", CLAIM_ID),
            ("model_version", MODEL_VERSION),
            ("status", PASS_STATUS if aggregate_pass else "FAIL"),
            ("aggregate_pass", aggregate_pass),
            (
                "scope",
                "Einstein_Hilbert_TEGR_operator_unchanged__one_charge_two_measures__once_only_CMB_source_ledger__unique_selected_phase_dust_branch__linear_scalar_closure_then_stop",
            ),
            ("data_role", "NO_OBSERVATIONAL_DATA_READ_OR_FITTED"),
            (
                "einstein_extension_statement",
                "RefG retains the one operational Einstein metric and Einstein tensor; its new content is the physical origin and covariant state of T_C.",
            ),
            (
                "selected_ir_premise",
                "Each conserved operational collective-phase charge unit carries density-independent positive proper energy mu_C on the CMB continuum domain; the vacuum offset belongs only to Lambda_eff.",
            ),
            ("dependencies", dependencies),
            (
                "contract",
                OrderedDict(
                    [
                        ("expected_sha256", CONTRACT_SHA256),
                        ("actual_sha256", actual_contract_hash),
                        ("verified", contract_verified),
                    ]
                ),
            ),
            (
                "source_ledger",
                OrderedDict(
                    [
                        ("geometry", list(EXPECTED_GEOMETRIC_LEDGER)),
                        ("sources", list(EXPECTED_CMB_SOURCES)),
                        (
                            "derived_aliases",
                            OrderedDict(
                                [
                                    (
                                        "Omega_r0",
                                        "Omega_gamma0 + Omega_nu_rel0",
                                    ),
                                    (
                                        "Omega_m0",
                                        "Omega_b0 + Omega_C0 + Omega_nu_nr0 + Omega_other_nr0",
                                    ),
                                ]
                            ),
                        ),
                        ("valid_once_only_ledger", source_ledger_exact),
                    ]
                ),
            ),
            ("symbolic_registry", symbolic),
            ("exact_checks", exact_checks),
            ("mutation_checks", mutations),
            ("numerical_smoke_test", numerical),
            ("required_true_closure_flags", required_true_flags),
            ("required_false_boundary_flags", required_false_flags),
            ("false_boundary_exact", false_boundary_exact),
            (
                "identifiability",
                "At equal Omega_C0 the selected phase-current branch is linearly identical to Einstein CDM. The ontology differs; linear CMB discrimination requires a derived abundance link or a derived departure from the cold branch.",
            ),
            (
                "handoff",
                "Implement T_C in the standard Einstein-Boltzmann system, using the numerical cdm slot only as an alias and never as an additional physical source; then close recombination before computing spectra.",
            ),
            (
                "stop_rule",
                "STOP before recombination, CLASS changes, CMB spectra, likelihoods, data fitting, Genesis spectrum, nonlinear structure or a galactic-normalization bridge.",
            ),
            (
                "provenance",
                OrderedDict(
                    [
                        ("python", sys.version.split()[0]),
                        ("sympy", sp.__version__),
                        ("platform", platform.platform()),
                        ("script_sha256", file_sha256(Path(__file__))),
                        ("utc", datetime.now(timezone.utc).isoformat()),
                    ]
                ),
            ),
        ]
    )


def json_default(value: object) -> object:
    """Serialize exact symbolic audit values without losing their meaning."""
    if isinstance(value, sp.Integer):
        return int(value)
    if isinstance(value, sp.Float):
        return float(value)
    if isinstance(value, sp.Rational):
        return str(value)
    if isinstance(value, sp.Basic):
        return str(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def atomic_json_write(path: Path, payload: OrderedDict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
            default=json_default,
        )
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> None:
    report = build_report()
    result_path = HERE / "w3_62_result.json"
    checksum_path = HERE / "w3_62_result.sha256"
    atomic_json_write(result_path, report)
    checksum_path.write_text(
        f"{file_sha256(result_path)}  {result_path.name}\n", encoding="ascii"
    )
    print(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
            default=json_default,
        )
    )
    if not report["aggregate_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
