#!/usr/bin/env python3
"""W3-44 bounded numerical RefG--flat-LCDM degeneracy regression."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import platform
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable

import scipy
from scipy.integrate import quad
import sympy as sp


sys.dont_write_bytecode = True


CLAIM_ID = "W3_44_REFG_FLAT_LCDM_IDEAL_OBSERVABLE_DEGENERACY"
MODEL_VERSION = (
    "W3-COSMOLOGY-v1.2-REFG-FLAT-LCDM-IDEAL-OBSERVABLE-DEGENERACY"
)
PASS_STATUS = (
    "PASS_BOUNDED_NUMERICAL_IDEAL_OBSERVABLE_DEGENERACY__"
    "NO_DATA_FIT_OR_EMPIRICAL_PREFERENCE"
)
UPSTREAM_PASS_STATUS = (
    "PASS_CONDITIONAL_IDEAL_OBSERVABLE_MAP__"
    "ASTROPHYSICAL_FORWARD_MODEL_AND_DATA_TEST_OPEN"
)

EXPECTED_PREREG_SHA256 = (
    "21dcb67e990d91b8ff1ce7d1e80eab202ee38099a207eebdddf0a622e3ed3521"
)
EXPECTED_W3_43_PREREG_SHA256 = (
    "20793b696e7fcd64a0a4f9a575b4091eeb2faf651973448b87b2c025b2d258da"
)
EXPECTED_W3_43_SOURCE_SHA256 = (
    "b9cf8550edc0b0db83bd2f0278e6e082bb8c18ea09433e20f71ca5f14622cf2e"
)
EXPECTED_BACKGROUND_SHA256 = (
    "57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055"
)

C0_KM_S = 299_792.458
ABS_TOL = 1.0e-9
REL_TOL = 1.0e-9
QUAD_ABS_TOL = 1.0e-12
QUAD_REL_TOL = 1.0e-12
SIMPSON_FINE_N = 32_768
SIMPSON_COARSE_N = 16_384
MUTATION_MIN_ERROR = 1.0e-4

PARAMETER_REGISTRY = (
    ("reference", 70.0, 0.30000, 0.00009),
    ("component_stress", 67.0, 0.25000, 0.05000),
)
EXPECTED_PARAMETER_REGISTRY = (
    ("reference", 70.0, 0.30000, 0.00009),
    ("component_stress", 67.0, 0.25000, 0.05000),
)
REDSHIFT_GRID = (
    1.0e-4,
    1.0e-3,
    1.0e-2,
    0.03,
    0.1,
    0.25,
    0.5,
    0.8,
    1.0,
    1.5,
    2.0,
    2.3,
    3.0,
)
EXPECTED_REDSHIFT_GRID = (
    1.0e-4,
    1.0e-3,
    1.0e-2,
    0.03,
    0.1,
    0.25,
    0.5,
    0.8,
    1.0,
    1.5,
    2.0,
    2.3,
    3.0,
)

OBSERVABLE_KEYS = frozenset(
    {
        "redshift",
        "signal_dilation",
        "H",
        "chi",
        "D_A",
        "D_L",
        "mu",
    }
)
EXPECTED_OBSERVABLE_KEYS = frozenset(
    {
        "redshift",
        "signal_dilation",
        "H",
        "chi",
        "D_A",
        "D_L",
        "mu",
    }
)
MUTATION_KEYS = frozenset(
    {
        "extra_endpoint_p_factor",
        "wrong_A_redshift_power",
        "omitted_radiation_component",
        "wrong_single_factor_distance_duality",
        "wrong_signal_dilation_sqrt",
        "wrong_supernova_intercept_sign",
    }
)
EXPECTED_MUTATION_KEYS = frozenset(
    {
        "extra_endpoint_p_factor",
        "wrong_A_redshift_power",
        "omitted_radiation_component",
        "wrong_single_factor_distance_duality",
        "wrong_signal_dilation_sqrt",
        "wrong_supernova_intercept_sign",
    }
)

REQUIRED_TRUE_FLAGS = (
    "upstream_w3_43_pass_verified",
    "dependency_hashes_exact",
    "canonical_dependency_text",
    "frozen_parameter_registry_exact",
    "frozen_redshift_grid_exact",
    "independent_coordinate_routes_used",
    "quadrature_convergence_pass",
    "redshift_map_match",
    "signal_dilation_match",
    "expansion_rate_match",
    "comoving_distance_match",
    "angular_diameter_distance_match",
    "luminosity_distance_match",
    "distance_modulus_match",
    "supernova_intercept_symmetry_exact",
    "mutation_controls_pass",
    "schema_keysets_exact",
)
REQUIRED_FALSE_FLAGS = (
    "observational_data_read",
    "observational_fit_performed",
    "observational_pass",
    "empirical_preference_established",
    "measured_H0_identified",
    "new_physical_freedom_introduced",
)
EXPECTED_REQUIRED_TRUE_FLAGS = (
    "upstream_w3_43_pass_verified",
    "dependency_hashes_exact",
    "canonical_dependency_text",
    "frozen_parameter_registry_exact",
    "frozen_redshift_grid_exact",
    "independent_coordinate_routes_used",
    "quadrature_convergence_pass",
    "redshift_map_match",
    "signal_dilation_match",
    "expansion_rate_match",
    "comoving_distance_match",
    "angular_diameter_distance_match",
    "luminosity_distance_match",
    "distance_modulus_match",
    "supernova_intercept_symmetry_exact",
    "mutation_controls_pass",
    "schema_keysets_exact",
)
EXPECTED_REQUIRED_FALSE_FLAGS = (
    "observational_data_read",
    "observational_fit_performed",
    "observational_pass",
    "empirical_preference_established",
    "measured_H0_identified",
    "new_physical_freedom_introduced",
)
EXPECTED_CLOSURE_FLAG_KEYS = frozenset(
    {
        "upstream_w3_43_pass_verified",
        "dependency_hashes_exact",
        "canonical_dependency_text",
        "frozen_parameter_registry_exact",
        "frozen_redshift_grid_exact",
        "independent_coordinate_routes_used",
        "quadrature_convergence_pass",
        "redshift_map_match",
        "signal_dilation_match",
        "expansion_rate_match",
        "comoving_distance_match",
        "angular_diameter_distance_match",
        "luminosity_distance_match",
        "distance_modulus_match",
        "supernova_intercept_symmetry_exact",
        "mutation_controls_pass",
        "schema_keysets_exact",
        "observational_data_read",
        "observational_fit_performed",
        "observational_pass",
        "empirical_preference_established",
        "measured_H0_identified",
        "new_physical_freedom_introduced",
        "ideal_observable_degeneracy_regression_pass",
    }
)
EXPECTED_DEPENDENCY_HASH_KEYS = frozenset(
    {
        "preregistration",
        "w3_43_preregistration",
        "w3_43_source",
        "operational_background_source",
    }
)
EXPECTED_REPORT_KEYS = frozenset(
    {
        "schema_version",
        "claim_id",
        "model_version",
        "decision_status",
        "scope",
        "data_role",
        "parameter_registry",
        "redshift_grid",
        "tolerances",
        "integration",
        "observable_keys",
        "dependency_hashes",
        "dependency_hashes_exact",
        "upstream_status",
        "closure_flags",
        "required_true_flags",
        "required_false_flags",
        "max_absolute_residuals",
        "max_tolerance_ratios",
        "max_simpson_convergence_tolerance_ratios",
        "max_quad_error_tolerance_ratio",
        "mutation_errors",
        "mutation_detection",
        "supernova_intercept_identity",
        "runtime",
        "direct_files_read",
        "writes_files",
        "source_sha256",
    }
)

HERE = Path(__file__).resolve().parent
COSMOLOGY_DIR = HERE.parent
W3_43_DIR = COSMOLOGY_DIR / "Photon_Atomic_Observable_Bridge"
PREREG_PATH = (
    HERE
    / "w3_44_refg_flat_lcdm_ideal_observable_degeneracy_preregistration.md"
)
W3_43_PREREG_PATH = (
    W3_43_DIR / "w3_43_photon_atomic_observable_bridge_preregistration.md"
)
W3_43_SOURCE_PATH = (
    W3_43_DIR / "w3_43_photon_atomic_observable_bridge.py"
)
BACKGROUND_SOURCE_PATH = (
    COSMOLOGY_DIR / "w3_cosmology_operational_geometric_flrw.py"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_lf(path: Path) -> bool:
    raw = path.read_bytes()
    return (
        not raw.startswith(b"\xef\xbb\xbf")
        and b"\r\n" not in raw
        and b"\r" not in raw
    )


def _load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _bound(left: float, right: float) -> float:
    return ABS_TOL + REL_TOL * max(abs(left), abs(right))


def _tolerance_ratio(left: float, right: float) -> float:
    return abs(left - right) / _bound(left, right)


def _scale_normalized_error(left: float, right: float) -> float:
    return abs(left - right) / max(1.0, abs(left), abs(right))


def _simpson(
    function: Callable[[float], float],
    left: float,
    right: float,
    intervals: int,
) -> float:
    if intervals <= 0 or intervals % 2:
        raise ValueError("Composite Simpson intervals must be positive and even")
    if left == right:
        return 0.0
    step = (right - left) / intervals
    odd_sum = 0.0
    even_sum = 0.0
    for index in range(1, intervals, 2):
        odd_sum += function(left + index * step)
    for index in range(2, intervals, 2):
        even_sum += function(left + index * step)
    return (
        step
        / 3.0
        * (
            function(left)
            + function(right)
            + 4.0 * odd_sum
            + 2.0 * even_sum
        )
    )


def _refg_route(
    h_a0: float,
    omega_m0: float,
    omega_r0: float,
    redshift: float,
) -> tuple[dict[str, float], float]:
    omega_lambda0 = 1.0 - omega_m0 - omega_r0
    a_emit = 1.0 / (1.0 + redshift)

    def e_a(scale: float) -> float:
        square = (
            omega_r0 * scale ** (-4)
            + omega_m0 * scale ** (-3)
            + omega_lambda0
        )
        if square <= 0.0:
            raise ValueError("RefG E_A^2 left the positive branch")
        return math.sqrt(square)

    chi_dimensionless, quad_error = quad(
        lambda scale: 1.0 / (scale * scale * e_a(scale)),
        a_emit,
        1.0,
        epsabs=QUAD_ABS_TOL,
        epsrel=QUAD_REL_TOL,
        limit=200,
    )
    chi = C0_KM_S / h_a0 * chi_dimensionless
    d_a = a_emit * chi
    d_l = chi / a_emit
    values = {
        "redshift": 1.0 / a_emit - 1.0,
        "signal_dilation": 1.0 / a_emit,
        "H": h_a0 * e_a(a_emit),
        "chi": chi,
        "D_A": d_a,
        "D_L": d_l,
        "mu": 5.0 * math.log10(d_l) + 25.0,
    }
    return values, float(quad_error)


def _benchmark_route(
    h_0: float,
    omega_m0: float,
    omega_r0: float,
    redshift: float,
    intervals: int,
) -> dict[str, float]:
    omega_lambda0 = 1.0 - omega_m0 - omega_r0

    def e_z(value: float) -> float:
        square = (
            omega_r0 * (1.0 + value) ** 4
            + omega_m0 * (1.0 + value) ** 3
            + omega_lambda0
        )
        if square <= 0.0:
            raise ValueError("Benchmark E_z^2 left the positive branch")
        return math.sqrt(square)

    chi_dimensionless = _simpson(
        lambda value: 1.0 / e_z(value),
        0.0,
        redshift,
        intervals,
    )
    chi = C0_KM_S / h_0 * chi_dimensionless
    d_a = chi / (1.0 + redshift)
    d_l = (1.0 + redshift) * chi
    return {
        "redshift": redshift,
        "signal_dilation": 1.0 + redshift,
        "H": h_0 * e_z(redshift),
        "chi": chi,
        "D_A": d_a,
        "D_L": d_l,
        "mu": 5.0 * math.log10(d_l * 1_000_000.0 / 10.0),
    }


def _intercept_identity() -> tuple[sp.Expr, sp.Expr, sp.Symbol]:
    h_ratio, lambda_scale, distance_scale, distance_shape = sp.symbols(
        "h_ratio lambda_scale distance_scale distance_shape",
        positive=True,
    )
    mass_b = sp.Symbol("mass_b", real=True)
    coefficient = sp.Integer(5) / sp.log(10)

    # Source equations: D_L/Mpc=(c0/[H_ref Mpc]) d(z;Omega)/(H0/H_ref),
    # mu=5 log10(D_L/Mpc)+25, and m_B^model=M_B+mu.
    d_l_over_mpc = distance_scale * distance_shape / h_ratio
    distance_modulus = coefficient * sp.log(d_l_over_mpc) + 25
    apparent_magnitude = mass_b + distance_modulus

    correct_transform = apparent_magnitude.subs(
        {
            h_ratio: lambda_scale * h_ratio,
            mass_b: mass_b + coefficient * sp.log(lambda_scale),
        },
        simultaneous=True,
    )
    wrong_transform = apparent_magnitude.subs(
        {
            h_ratio: lambda_scale * h_ratio,
            mass_b: mass_b - coefficient * sp.log(lambda_scale),
        },
        simultaneous=True,
    )
    return (
        sp.simplify(correct_transform - apparent_magnitude),
        sp.simplify(wrong_transform - apparent_magnitude),
        lambda_scale,
    )


def build_report() -> dict[str, object]:
    source_path = Path(__file__).resolve()
    dependency_hashes = {
        "preregistration": _sha256(PREREG_PATH),
        "w3_43_preregistration": _sha256(W3_43_PREREG_PATH),
        "w3_43_source": _sha256(W3_43_SOURCE_PATH),
        "operational_background_source": _sha256(BACKGROUND_SOURCE_PATH),
    }
    expected_dependency_hashes = {
        "preregistration": EXPECTED_PREREG_SHA256,
        "w3_43_preregistration": EXPECTED_W3_43_PREREG_SHA256,
        "w3_43_source": EXPECTED_W3_43_SOURCE_SHA256,
        "operational_background_source": EXPECTED_BACKGROUND_SHA256,
    }
    dependency_hashes_exact = {
        key: dependency_hashes[key] == expected_dependency_hashes[key]
        for key in expected_dependency_hashes
    }

    w3_43_module = _load_module(
        W3_43_SOURCE_PATH,
        "w3_43_dependency_for_w3_44",
    )
    w3_43_report = w3_43_module.build_report()
    upstream_pass = bool(
        w3_43_report["decision_status"] == UPSTREAM_PASS_STATUS
        and w3_43_report["closure_flags"][
            "conditional_ideal_observable_map_pass"
        ]
        and not w3_43_report["closure_flags"]["observational_pass"]
    )

    canonical_dependencies = all(
        _canonical_lf(path)
        for path in (
            PREREG_PATH,
            W3_43_PREREG_PATH,
            W3_43_SOURCE_PATH,
            BACKGROUND_SOURCE_PATH,
            source_path,
        )
    )

    max_absolute_residuals = {
        key: 0.0 for key in sorted(OBSERVABLE_KEYS)
    }
    max_tolerance_ratios = {
        key: 0.0 for key in sorted(OBSERVABLE_KEYS)
    }
    max_simpson_convergence_tolerance_ratios = {
        key: 0.0 for key in sorted(OBSERVABLE_KEYS)
    }
    max_quad_error_tolerance_ratio = 0.0
    mutation_errors = {
        key: 0.0 for key in sorted(MUTATION_KEYS)
    }
    all_values_finite_positive = True
    route_keysets_exact = True

    for _, h_0, omega_m0, omega_r0 in PARAMETER_REGISTRY:
        omega_lambda0 = 1.0 - omega_m0 - omega_r0
        if not (
            h_0 > 0.0
            and omega_m0 >= 0.0
            and omega_r0 >= 0.0
            and omega_lambda0 >= 0.0
        ):
            all_values_finite_positive = False
        for redshift in REDSHIFT_GRID:
            refg, quad_error = _refg_route(
                h_0,
                omega_m0,
                omega_r0,
                redshift,
            )
            benchmark_fine = _benchmark_route(
                h_0,
                omega_m0,
                omega_r0,
                redshift,
                SIMPSON_FINE_N,
            )
            benchmark_coarse = _benchmark_route(
                h_0,
                omega_m0,
                omega_r0,
                redshift,
                SIMPSON_COARSE_N,
            )
            route_keysets_exact = bool(
                route_keysets_exact
                and frozenset(refg) == EXPECTED_OBSERVABLE_KEYS
                and frozenset(benchmark_fine) == EXPECTED_OBSERVABLE_KEYS
                and frozenset(benchmark_coarse)
                == EXPECTED_OBSERVABLE_KEYS
            )
            for key in OBSERVABLE_KEYS:
                left = refg[key]
                right = benchmark_fine[key]
                coarse = benchmark_coarse[key]
                max_absolute_residuals[key] = max(
                    max_absolute_residuals[key],
                    abs(left - right),
                )
                max_tolerance_ratios[key] = max(
                    max_tolerance_ratios[key],
                    _tolerance_ratio(left, right),
                )
                max_simpson_convergence_tolerance_ratios[key] = max(
                    max_simpson_convergence_tolerance_ratios[key],
                    _tolerance_ratio(right, coarse),
                )
            chi_dimensionless = (
                refg["chi"] * h_0 / C0_KM_S
            )
            quad_inputs_valid = bool(
                math.isfinite(chi_dimensionless)
                and math.isfinite(quad_error)
                and quad_error >= 0.0
            )
            quad_bound = max(
                QUAD_ABS_TOL,
                QUAD_REL_TOL * abs(chi_dimensionless),
            )
            quad_error_tolerance_ratio = (
                quad_error / quad_bound
                if quad_inputs_valid
                else math.inf
            )
            max_quad_error_tolerance_ratio = max(
                max_quad_error_tolerance_ratio,
                quad_error_tolerance_ratio,
            )
            all_values_finite_positive = bool(
                all_values_finite_positive
                and quad_inputs_valid
                and all(math.isfinite(value) for value in refg.values())
                and all(
                    math.isfinite(value)
                    for value in benchmark_fine.values()
                )
                and all(
                    math.isfinite(value)
                    for value in benchmark_coarse.values()
                )
                and all(
                    refg[key] > 0.0
                    for key in ("H", "chi", "D_A", "D_L")
                )
                and all(
                    benchmark_fine[key] > 0.0
                    for key in ("H", "chi", "D_A", "D_L")
                )
                and all(
                    benchmark_coarse[key] > 0.0
                    for key in ("H", "chi", "D_A", "D_L")
                )
            )

            a_emit = 1.0 / (1.0 + redshift)
            extra_p_d_l = refg["D_L"] * a_emit ** (3.0 / 5.0)
            mutation_errors["extra_endpoint_p_factor"] = max(
                mutation_errors["extra_endpoint_p_factor"],
                _scale_normalized_error(
                    extra_p_d_l,
                    benchmark_fine["D_L"],
                ),
            )

            wrong_a_emit = (1.0 + redshift) ** (-0.5)
            wrong_a_redshift = 1.0 / wrong_a_emit - 1.0
            mutation_errors["wrong_A_redshift_power"] = max(
                mutation_errors["wrong_A_redshift_power"],
                _scale_normalized_error(
                    wrong_a_redshift,
                    benchmark_fine["redshift"],
                ),
            )

            omitted_radiation_h = h_0 * math.sqrt(
                omega_m0 * a_emit ** (-3) + omega_lambda0
            )
            mutation_errors["omitted_radiation_component"] = max(
                mutation_errors["omitted_radiation_component"],
                _scale_normalized_error(
                    omitted_radiation_h,
                    benchmark_fine["H"],
                ),
            )

            wrong_single_factor_d_l = (
                (1.0 + redshift) * refg["D_A"]
            )
            mutation_errors[
                "wrong_single_factor_distance_duality"
            ] = max(
                mutation_errors[
                    "wrong_single_factor_distance_duality"
                ],
                _scale_normalized_error(
                    wrong_single_factor_d_l,
                    benchmark_fine["D_L"],
                ),
            )

            wrong_signal_dilation = math.sqrt(1.0 + redshift)
            mutation_errors["wrong_signal_dilation_sqrt"] = max(
                mutation_errors["wrong_signal_dilation_sqrt"],
                _scale_normalized_error(
                    wrong_signal_dilation,
                    benchmark_fine["signal_dilation"],
                ),
            )

    (
        intercept_residual,
        wrong_intercept_residual,
        intercept_lambda,
    ) = _intercept_identity()
    wrong_intercept_value = abs(
        float(
            wrong_intercept_residual.subs(
                {intercept_lambda: 2}
            )
        )
    )
    mutation_errors["wrong_supernova_intercept_sign"] = (
        wrong_intercept_value / max(1.0, wrong_intercept_value)
    )
    mutation_detection = {
        key: value > MUTATION_MIN_ERROR
        for key, value in mutation_errors.items()
    }

    flags = {
        "upstream_w3_43_pass_verified": upstream_pass,
        "dependency_hashes_exact": all(dependency_hashes_exact.values()),
        "canonical_dependency_text": canonical_dependencies,
        "frozen_parameter_registry_exact": (
            PARAMETER_REGISTRY == EXPECTED_PARAMETER_REGISTRY
        ),
        "frozen_redshift_grid_exact": (
            REDSHIFT_GRID == EXPECTED_REDSHIFT_GRID
        ),
        "independent_coordinate_routes_used": True,
        "quadrature_convergence_pass": bool(
            all_values_finite_positive
            and max_quad_error_tolerance_ratio <= 1.0
            and all(
                value <= 1.0
                for value in (
                    max_simpson_convergence_tolerance_ratios.values()
                )
            )
        ),
        "redshift_map_match": (
            max_tolerance_ratios["redshift"] <= 1.0
        ),
        "signal_dilation_match": (
            max_tolerance_ratios["signal_dilation"] <= 1.0
        ),
        "expansion_rate_match": max_tolerance_ratios["H"] <= 1.0,
        "comoving_distance_match": (
            max_tolerance_ratios["chi"] <= 1.0
        ),
        "angular_diameter_distance_match": (
            max_tolerance_ratios["D_A"] <= 1.0
        ),
        "luminosity_distance_match": (
            max_tolerance_ratios["D_L"] <= 1.0
        ),
        "distance_modulus_match": (
            max_tolerance_ratios["mu"] <= 1.0
        ),
        "supernova_intercept_symmetry_exact": intercept_residual == 0,
        "mutation_controls_pass": all(mutation_detection.values()),
        "schema_keysets_exact": False,
        "observational_data_read": False,
        "observational_fit_performed": False,
        "observational_pass": False,
        "empirical_preference_established": False,
        "measured_H0_identified": False,
        "new_physical_freedom_introduced": False,
        "ideal_observable_degeneracy_regression_pass": False,
    }

    report: dict[str, object] = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "decision_status": "PENDING_SCHEMA_CHECK",
        "scope": (
            "BOUNDED_NUMERICAL_IMPLEMENTATION_AND_IDENTIFIABILITY_"
            "REGRESSION_ONLY"
        ),
        "data_role": "NO_OBSERVATIONAL_DATA_READ_OR_FITTED",
        "parameter_registry": [
            {
                "name": name,
                "H_A0_km_s_Mpc": h_0,
                "Omega_m0": omega_m0,
                "Omega_r0": omega_r0,
                "Omega_Lambda0": 1.0 - omega_m0 - omega_r0,
            }
            for name, h_0, omega_m0, omega_r0 in PARAMETER_REGISTRY
        ],
        "redshift_grid": list(REDSHIFT_GRID),
        "tolerances": {
            "absolute": ABS_TOL,
            "relative": REL_TOL,
            "quad_absolute_target": QUAD_ABS_TOL,
            "quad_relative_target": QUAD_REL_TOL,
            "mutation_minimum_scale_normalized_error": (
                MUTATION_MIN_ERROR
            ),
        },
        "integration": {
            "refg_route": "scipy.integrate.quad in A",
            "benchmark_route": "composite Simpson in z",
            "simpson_fine_intervals": SIMPSON_FINE_N,
            "simpson_coarse_intervals": SIMPSON_COARSE_N,
        },
        "observable_keys": sorted(OBSERVABLE_KEYS),
        "dependency_hashes": dependency_hashes,
        "dependency_hashes_exact": dependency_hashes_exact,
        "upstream_status": w3_43_report["decision_status"],
        "closure_flags": flags,
        "required_true_flags": list(REQUIRED_TRUE_FLAGS),
        "required_false_flags": list(REQUIRED_FALSE_FLAGS),
        "max_absolute_residuals": max_absolute_residuals,
        "max_tolerance_ratios": max_tolerance_ratios,
        "max_simpson_convergence_tolerance_ratios": (
            max_simpson_convergence_tolerance_ratios
        ),
        "max_quad_error_tolerance_ratio": (
            max_quad_error_tolerance_ratio
        ),
        "mutation_errors": mutation_errors,
        "mutation_detection": mutation_detection,
        "supernova_intercept_identity": {
            "residual": str(intercept_residual),
            "wrong_sign_residual": str(wrong_intercept_residual),
            "derived_from": (
                "D_L=(c0/H0)d(z;Omega), "
                "mu=5 log10(D_L/Mpc)+25, m_B_model=M_B+mu"
            ),
            "symmetry": (
                "H0->lambda H0, "
                "M_B->M_B+5 log10(lambda)"
            ),
            "consequence": (
                "SN magnitudes alone do not identify absolute H0 "
                "without external absolute calibration"
            ),
        },
        "runtime": {
            "python": platform.python_version(),
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
        },
        "direct_files_read": [
            str(PREREG_PATH.relative_to(COSMOLOGY_DIR)),
            str(W3_43_PREREG_PATH.relative_to(COSMOLOGY_DIR)),
            str(W3_43_SOURCE_PATH.relative_to(COSMOLOGY_DIR)),
            str(BACKGROUND_SOURCE_PATH.relative_to(COSMOLOGY_DIR)),
        ],
        "writes_files": False,
        "source_sha256": _sha256(source_path),
    }

    schema_keysets_exact = bool(
        frozenset(dependency_hashes)
        == EXPECTED_DEPENDENCY_HASH_KEYS
        and frozenset(dependency_hashes_exact)
        == EXPECTED_DEPENDENCY_HASH_KEYS
        and frozenset(OBSERVABLE_KEYS) == EXPECTED_OBSERVABLE_KEYS
        and route_keysets_exact
        and frozenset(max_absolute_residuals)
        == EXPECTED_OBSERVABLE_KEYS
        and frozenset(max_tolerance_ratios)
        == EXPECTED_OBSERVABLE_KEYS
        and frozenset(max_simpson_convergence_tolerance_ratios)
        == EXPECTED_OBSERVABLE_KEYS
        and frozenset(MUTATION_KEYS) == EXPECTED_MUTATION_KEYS
        and frozenset(mutation_errors) == EXPECTED_MUTATION_KEYS
        and frozenset(mutation_detection) == EXPECTED_MUTATION_KEYS
        and frozenset(flags) == EXPECTED_CLOSURE_FLAG_KEYS
        and frozenset(report) == EXPECTED_REPORT_KEYS
        and REQUIRED_TRUE_FLAGS == EXPECTED_REQUIRED_TRUE_FLAGS
        and REQUIRED_FALSE_FLAGS == EXPECTED_REQUIRED_FALSE_FLAGS
        and set(REQUIRED_TRUE_FLAGS).isdisjoint(REQUIRED_FALSE_FLAGS)
        and "ideal_observable_degeneracy_regression_pass"
        not in REQUIRED_TRUE_FLAGS
    )
    flags["schema_keysets_exact"] = schema_keysets_exact
    aggregate_pass = all(
        flags[name] for name in REQUIRED_TRUE_FLAGS
    ) and all(not flags[name] for name in REQUIRED_FALSE_FLAGS)
    flags["ideal_observable_degeneracy_regression_pass"] = aggregate_pass
    report["decision_status"] = PASS_STATUS if aggregate_pass else "FAIL"
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    return (
        0
        if report["closure_flags"][
            "ideal_observable_degeneracy_regression_pass"
        ]
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
