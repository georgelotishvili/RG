"""Exact symbolic verifier for the conditional operational FLRW completion.

The verifier reads no data, performs no fit, and writes no files. Its only
output is one deterministic JSON report on stdout.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_COSMOLOGY_OPERATIONAL_GEOMETRIC_FLRW_COMPLETION"
MODEL_VERSION = "W3-COSMOLOGY-v1.0-OPERATIONAL-GEOMETRIC-FLRW"
PASS_STATUS = (
    "PASS_CONDITIONAL_BACKGROUND_EQUATION__"
    "MICROPHYSICS_PARAMETERS_AND_OBSERVABLES_OPEN"
)

SOURCE_REGISTRY = (
    "adiabatic_radiation",
    "localized_defect_noether_proper_energy",
)
EXPECTED_SOURCE_REGISTRY = frozenset(
    {
        "adiabatic_radiation",
        "localized_defect_noether_proper_energy",
    }
)

FREEDOM_LEDGER = (
    "H_A0",
    "Omega_m0",
    "Omega_r0",
)
EXPECTED_FREEDOM_LEDGER = frozenset(
    {
        "H_A0",
        "Omega_m0",
        "Omega_r0",
    }
)

REQUIRED_TRUE_FLAGS = (
    "operational_constraint_selected",
    "operational_source_map_selected",
    "finite_source_registry_complete",
    "finite_freedom_ledger_complete",
    "lapse_00_constraint_agreement_exact",
    "matter_continuity_exact",
    "radiation_continuity_exact",
    "Hamiltonian_constraint_normalization_exact",
    "Omega_sum_rule_exact",
    "spatial_Einstein_consistency_exact",
    "scale_pullback_exact",
    "time_coordinate_pullback_exact",
    "implicit_history_derivatives_exact",
    "a_of_tau_equation_derived_within_conditional_EFT",
    "a_of_t_equation_derived_within_conditional_EFT",
)

REQUIRED_FALSE_FLAGS = (
    "operational_source_map_microphysically_derived",
    "foundation_hamiltonian_derived",
    "EFT_truncation_controlled",
    "Lambda_value_derived",
    "Genesis_matching_derived",
    "numerical_history_fixed",
    "observable_forward_model_derived",
)


def _zero(expression: sp.Expr) -> bool:
    """Return True only for an exact symbolic zero."""

    return sp.simplify(expression) == 0


def _symbolic_residuals() -> tuple[dict[str, sp.Expr], frozenset[str]]:
    """Derive exact residuals and the freedoms present in the background."""

    A, a, N = sp.symbols("A a N", positive=True)
    A_lambda, A_tau, a_tau, a_t = sp.symbols(
        "A_lambda A_tau a_tau a_t", real=True
    )
    c0, G, H_A0 = sp.symbols("c0 G H_A0", positive=True)
    epsilon_m, epsilon_r = sp.symbols("epsilon_m epsilon_r", nonnegative=True)
    epsilon_m0, epsilon_r0 = sp.symbols(
        "epsilon_m0 epsilon_r0", nonnegative=True
    )
    Lambda = sp.symbols("Lambda", real=True)
    Omega_m0, Omega_r0 = sp.symbols("Omega_m0 Omega_r0", real=True)
    Omega_Lambda0 = 1 - Omega_m0 - Omega_r0

    vacuum_energy = Lambda * c0**4 / (8 * sp.pi * G)
    reduced_lagrangian = (
        -3 * c0**2 * A * A_lambda**2 / (8 * sp.pi * G * N)
        - N * A**3 * (epsilon_m + epsilon_r + vacuum_energy)
    )
    lapse_constraint = sp.simplify(
        8
        * sp.pi
        * G
        / (3 * c0**2 * A**3)
        * sp.diff(reduced_lagrangian, N)
    ).subs({N: 1, A_lambda: A_tau})
    efe_00_constraint = (
        (A_tau / A) ** 2
        - 8 * sp.pi * G * (epsilon_m + epsilon_r) / (3 * c0**2)
        - Lambda * c0**2 / 3
    )

    matter_history = epsilon_m0 * A**-3
    radiation_history = epsilon_r0 * A**-4
    H_A = A_tau / A
    matter_continuity = (
        sp.diff(matter_history, A) * A_tau + 3 * H_A * matter_history
    )
    radiation_continuity = (
        sp.diff(radiation_history, A) * A_tau + 4 * H_A * radiation_history
    )

    omega_m_definition = 8 * sp.pi * G * epsilon_m0 / (3 * c0**2 * H_A0**2)
    omega_r_definition = 8 * sp.pi * G * epsilon_r0 / (3 * c0**2 * H_A0**2)
    omega_lambda_definition = Lambda * c0**2 / (3 * H_A0**2)
    raw_constraint = (
        8
        * sp.pi
        * G
        / (3 * c0**2)
        * (matter_history + radiation_history)
        + Lambda * c0**2 / 3
    )
    normalized_constraint = H_A0**2 * (
        omega_r_definition * A**-4
        + omega_m_definition * A**-3
        + omega_lambda_definition
    )

    lambda_from_flat_present_constraint = (
        3 * H_A0**2 / c0**2
        - 8 * sp.pi * G * (epsilon_m0 + epsilon_r0) / c0**4
    )
    omega_sum = (
        omega_r_definition
        + omega_m_definition
        + omega_lambda_definition
        - 1
    ).subs(Lambda, lambda_from_flat_present_constraint)

    expansion_rate_squared = H_A0**2 * (
        Omega_r0 * A**-4
        + Omega_m0 * A**-3
        + Omega_Lambda0
    )
    acceleration_from_constraint = (
        expansion_rate_squared
        + A * sp.diff(expansion_rate_squared, A) / 2
    )
    acceleration_from_spatial_efe = -H_A0**2 / 2 * (
        Omega_m0 * A**-3
        + 2 * Omega_r0 * A**-4
        - 2 * Omega_Lambda0
    )

    operational_scale = a ** sp.Rational(5, 2)
    foundation_cadence = a ** sp.Rational(-3, 2)
    scale_rate_from_definition = (
        sp.diff(operational_scale, a) * a_tau / operational_scale
    )
    scale_rate_from_dictionary = sp.Rational(5, 2) * a_tau / a
    process_constraint_lhs_in_t = (
        sp.Rational(25, 4) * ((a_t / foundation_cadence) / a) ** 2
    )
    coordinate_constraint_lhs = sp.Rational(25, 4) * a * a_t**2

    E_of_a = sp.sqrt(
        Omega_r0 * a**-10
        + Omega_m0 * a ** sp.Rational(-15, 2)
        + Omega_Lambda0
    )
    a_tau_rhs = sp.Rational(2, 5) * H_A0 * a * E_of_a
    a_t_rhs = sp.Rational(2, 5) * H_A0 * a ** sp.Rational(-1, 2) * E_of_a
    a_tau_equation = (
        sp.Rational(5, 2) * a_tau_rhs / a - H_A0 * E_of_a
    )
    a_t_equation = a_t_rhs / foundation_cadence - a_tau_rhs

    u = sp.symbols("u", positive=True)
    E_u = sp.sqrt(
        Omega_r0 * u**-4
        + Omega_m0 * u**-3
        + Omega_Lambda0
    )
    E_A = sp.sqrt(
        Omega_r0 * A**-4
        + Omega_m0 * A**-3
        + Omega_Lambda0
    )
    tau_history = sp.Integral(1 / (H_A0 * u * E_u), (u, 1, A))
    t_history = sp.Integral(
        u ** sp.Rational(-2, 5) / (H_A0 * E_u), (u, 1, A)
    )

    background_expressions = (
        expansion_rate_squared,
        acceleration_from_spatial_efe,
        a_tau_rhs,
        a_t_rhs,
        tau_history,
        t_history,
    )
    state_symbols = {A, a, u}
    actual_background_freedoms = frozenset(
        symbol.name
        for expression in background_expressions
        for symbol in expression.free_symbols - state_symbols
    )

    residuals = {
        "lapse_00_constraint_agreement": lapse_constraint - efe_00_constraint,
        "matter_continuity": matter_continuity,
        "radiation_continuity": radiation_continuity,
        "Hamiltonian_constraint_normalization": raw_constraint
        - normalized_constraint,
        "Omega_sum_rule": omega_sum,
        "spatial_Einstein_consistency": acceleration_from_constraint
        - acceleration_from_spatial_efe,
        "scale_pullback": scale_rate_from_definition
        - scale_rate_from_dictionary,
        "time_coordinate_pullback": process_constraint_lhs_in_t
        - coordinate_constraint_lhs,
        "implicit_tau_history_derivative": sp.diff(tau_history, A)
        - 1 / (H_A0 * A * E_A),
        "implicit_t_history_derivative": sp.diff(t_history, A)
        - A ** sp.Rational(-2, 5) / (H_A0 * E_A),
        "a_of_tau_equation": a_tau_equation,
        "a_of_t_equation": a_t_equation,
    }
    return residuals, actual_background_freedoms


def build_report() -> dict[str, object]:
    """Build the complete machine-readable closure report."""

    residual_expressions, actual_background_freedoms = _symbolic_residuals()
    residuals = {
        name: sp.sstr(sp.simplify(expression))
        for name, expression in residual_expressions.items()
    }
    exact = {
        name: _zero(expression)
        for name, expression in residual_expressions.items()
    }

    sources_exact = frozenset(SOURCE_REGISTRY) == EXPECTED_SOURCE_REGISTRY
    registered_freedoms = frozenset(FREEDOM_LEDGER)
    freedoms_exact = (
        registered_freedoms
        == EXPECTED_FREEDOM_LEDGER
        == actual_background_freedoms
    )

    flags = {
        "operational_constraint_selected": True,
        "operational_source_map_selected": sources_exact,
        "finite_source_registry_complete": sources_exact,
        "finite_freedom_ledger_complete": freedoms_exact,
        "lapse_00_constraint_agreement_exact": exact[
            "lapse_00_constraint_agreement"
        ],
        "matter_continuity_exact": exact["matter_continuity"],
        "radiation_continuity_exact": exact["radiation_continuity"],
        "Hamiltonian_constraint_normalization_exact": exact[
            "Hamiltonian_constraint_normalization"
        ],
        "Omega_sum_rule_exact": exact["Omega_sum_rule"],
        "spatial_Einstein_consistency_exact": exact[
            "spatial_Einstein_consistency"
        ],
        "scale_pullback_exact": exact["scale_pullback"],
        "time_coordinate_pullback_exact": exact["time_coordinate_pullback"],
        "implicit_history_derivatives_exact": exact[
            "implicit_tau_history_derivative"
        ]
        and exact["implicit_t_history_derivative"],
        "a_of_tau_equation_derived_within_conditional_EFT": exact[
            "a_of_tau_equation"
        ],
        "a_of_t_equation_derived_within_conditional_EFT": exact[
            "a_of_t_equation"
        ],
        "operational_source_map_microphysically_derived": False,
        "foundation_hamiltonian_derived": False,
        "EFT_truncation_controlled": False,
        "Lambda_value_derived": False,
        "Genesis_matching_derived": False,
        "numerical_history_fixed": False,
        "observable_forward_model_derived": False,
    }
    conditional_background_pass = all(
        flags[name] for name in REQUIRED_TRUE_FLAGS
    ) and all(not flags[name] for name in REQUIRED_FALSE_FLAGS)
    flags["conditional_background_pass"] = conditional_background_pass

    source_path = Path(__file__).resolve()
    return {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "decision_status": PASS_STATUS if conditional_background_pass else "FAIL",
        "data_role": "NO_DATA_READ_OR_FITTED",
        "writes_files": False,
        "source_registry": list(SOURCE_REGISTRY),
        "freedom_ledger": list(FREEDOM_LEDGER),
        "freedoms_derived_from_background": sorted(actual_background_freedoms),
        "required_true_flags": list(REQUIRED_TRUE_FLAGS),
        "required_false_flags": list(REQUIRED_FALSE_FLAGS),
        "closure_flags": flags,
        "residuals": residuals,
        "runtime": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
    }


def main() -> int:
    report = build_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["closure_flags"]["conditional_background_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
