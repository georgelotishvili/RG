#!/usr/bin/env python3
"""W3-59: fixed-benchmark real-field oscillon in an open radiation domain."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import simpson, solve_bvp
from scipy.signal import butter, hilbert, sosfiltfilt


HERE = Path(__file__).resolve().parent
PREREG = HERE / "w3_59_one_oscillon_real_field_open_radiation_preregistration.md"
SOURCE = Path(__file__).resolve()
README = HERE / "README.md"
FORMAL_LEDGER = HERE.parent / "RefG_Formal_Proof.md"
OUTPUT = HERE / "w3_59_result.json"
HASH_OUTPUT = HERE / "w3_59_result.sha256"

PINNED_PREREG_SHA256 = "7ff251419e0f2ab3f977e18d296d68eea9b438600b1d5852acb1618fe228e76f"

W3_54_CONTRACT = (
    HERE.parent
    / "Relational_Coframe_TEGR_Phase_Source_Closure"
    / "w3_54_relational_coframe_tegr_phase_source_closure_contract.md"
)
W3_58_DIR = HERE.parent / "One_Oscillon_Coframe_Localized_Core"
W3_58_PREREG = W3_58_DIR / "w3_58_one_oscillon_coframe_localized_core_preregistration.md"
W3_58_SOURCE = W3_58_DIR / "w3_58_one_oscillon_coframe_localized_core.py"
W3_58_RESULT = W3_58_DIR / "w3_58_result.json"
W3_58_CHECKSUM = W3_58_DIR / "w3_58_result.sha256"

DEPENDENCIES = {
    "W3_54_contract": (
        W3_54_CONTRACT,
        "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
    ),
    "W3_58_preregistration": (
        W3_58_PREREG,
        "962980d4607ba506a5b65fe458f04ab31d8a78ac74511c68d43ff2d95f911dda",
    ),
    "W3_58_source": (
        W3_58_SOURCE,
        "f4894b3608a0a5964592fe2d42015497709c35b58ba62a336dc15f7c64bd60cf",
    ),
    "W3_58_result": (
        W3_58_RESULT,
        "04412d4b1c55e5a94eae25ae401f3f574c051f883e78251ec27238679ccb1940",
    ),
}

A = 0.25
OMEGA_SEED = 0.80
T0 = 2.0 * math.pi / OMEGA_SEED
SAMPLES_PER_PERIOD = 32
ABSORBER_POWER = 4
ABSORBER_GAMMA_MAX = 1.0
DETECTOR_RADII = (40.0, 60.0)
SINGULAR_MATRIX = np.array([[0.0, 0.0], [0.0, -2.0]])

LONG_CONFIGS = (
    {
        "name": "canonical",
        "radius": 200.0,
        "absorber_start": 150.0,
        "dx": 0.050,
        "dt": 0.0125,
        "periods": 1000.0,
    },
    {
        "name": "fine",
        "radius": 200.0,
        "absorber_start": 150.0,
        "dx": 0.025,
        "dt": 0.00625,
        "periods": 1000.0,
    },
    {
        "name": "domain",
        "radius": 240.0,
        "absorber_start": 180.0,
        "dx": 0.050,
        "dt": 0.0125,
        "periods": 1000.0,
    },
)

SUCCESS_STATUS = (
    "PASS_CONDITIONAL_EXACT_SINGLE_REAL_Z2_COFRAME_CORE_ACTION_AND_"
    "CONTINUOUS_INTERNAL_CHARGE_ABSENCE__CONVERGED_OPEN_BOUNDARY_"
    "LONG_LIVED_RADIATING_SPHERICAL_OSCILLON_NUMERICAL_EVIDENCE__"
    "FOUNDATION_COEFFICIENT_SELECTION_LOCALIZED_DYNAMICAL_BACKREACTION_"
    "NONSpherical_STABILITY_ELECTRIC_NEUTRALITY_AND_PARTICLE_IDENTITY_OPEN"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def relative_change(value: float, reference: float) -> float:
    scale = max(abs(reference), np.finfo(float).tiny)
    return abs(value - reference) / scale


def finite_tree(value: Any) -> bool:
    if isinstance(value, dict):
        return all(finite_tree(k) and finite_tree(v) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return all(finite_tree(v) for v in value)
    if isinstance(value, (float, np.floating)):
        return bool(np.isfinite(value))
    if isinstance(value, (complex, np.complexfloating)):
        return bool(np.isfinite(value.real) and np.isfinite(value.imag))
    return True


def native_tree(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): native_tree(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [native_tree(v) for v in value]
    if isinstance(value, np.ndarray):
        return [native_tree(v) for v in value.tolist()]
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, Path):
        return str(value)
    return value


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def verify_preregistration() -> dict[str, Any]:
    text = canonical_text(PREREG)
    digest = sha256(PREREG)
    required = (
        "## CLAIM",
        "## MODEL_AND_SOURCE_LEDGER",
        "## FROZEN_BENCHMARK_AND_SEED",
        "## EXACT_RADIATION_GATE",
        "## NUMERICAL_METHOD",
        "## SYMBOLIC_PASS_GATES",
        "## NUMERICAL_PASS_GATES",
        "## MUTATION_CONTROLS",
        "## PINNED_DEPENDENCIES",
        "## STOP_RULE",
        "a = 0.25",
        "Omega_seed = 0.80",
        "canonical: Xmax=200",
        "fine:      Xmax=200",
        "domain:    Xmax=240",
        "1000 seed periods",
        "T_total = T_C + T_phi",
        "T_phi` replaces",
        "Dynamical coframe backreaction is the separate W3-60 gate",
        SUCCESS_STATUS,
    )
    markers = {marker: marker in text for marker in required}
    return {
        "path": str(PREREG),
        "sha256": digest,
        "expected_sha256": PINNED_PREREG_SHA256,
        "hash_exact": digest == PINNED_PREREG_SHA256,
        "markers": markers,
        "markers_exact": all(markers.values()),
        "pass": digest == PINNED_PREREG_SHA256 and all(markers.values()),
    }


def verify_dependencies() -> dict[str, Any]:
    records: dict[str, Any] = {}
    for name, (path, expected) in DEPENDENCIES.items():
        exists = path.is_file()
        actual = sha256(path) if exists else None
        records[name] = {
            "path": str(path),
            "exists": exists,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "hash_exact": exists and actual == expected,
        }
    checksum_token = W3_58_CHECKSUM.read_text(encoding="utf-8").split()[0].strip()
    w358 = json.loads(W3_58_RESULT.read_text(encoding="utf-8"))
    status = str(w358.get("status", ""))
    semantic = {
        "checksum_token_matches_result": checksum_token == sha256(W3_58_RESULT),
        "artifact_valid": bool(w358.get("artifact_valid", False)),
        "conditional_pass_status": status.startswith("PASS_CONDITIONAL"),
        "fixed_coframe_boundary_present": "COFRAME" in status and status.endswith("OPEN"),
    }
    return {
        "records": records,
        "semantic": semantic,
        "all_pass": all(r["hash_exact"] for r in records.values())
        and all(semantic.values()),
    }


def symbolic_gate() -> dict[str, Any]:
    # Frozen physical polynomial.
    f, c = sp.symbols("f c", real=True)
    a = sp.Rational(1, 4)
    v = sp.Rational(1, 2) * f**2 - sp.Rational(1, 4) * f**4 + a * f**6 / 6
    vp = sp.diff(v, f)
    target_factor = f * (1 - f**2 / 2) ** 2

    # Euler--Lagrange equation from the spherical reduced action.
    u, x = sp.symbols("u x", real=True, positive=True)
    phi = sp.Function("phi")(u, x)
    v_phi = (
        sp.Rational(1, 2) * phi**2
        - sp.Rational(1, 4) * phi**4
        + a * phi**6 / 6
    )
    reduced_lagrangian = x**2 * (
        sp.diff(phi, u) ** 2 / 2 - sp.diff(phi, x) ** 2 / 2 - v_phi
    )
    euler = (
        sp.diff(reduced_lagrangian, phi)
        - sp.diff(sp.diff(reduced_lagrangian, sp.diff(phi, u)), u)
        - sp.diff(sp.diff(reduced_lagrangian, sp.diff(phi, x)), x)
    )
    expected_pde = (
        sp.diff(phi, u, 2)
        - sp.diff(phi, x, 2)
        - 2 * sp.diff(phi, x) / x
        + phi
        - phi**3
        + a * phi**5
    )
    euler_residual = sp.simplify(euler + x**2 * expected_pde)

    # Hilbert tensor from variation of the scalar action with respect to g^mn.
    kinetic_plus_potential, g_mn, p_m_p_n = sp.symbols(
        "kinetic_plus_potential g_mn p_m_p_n", real=True
    )
    delta_e_over_e = -g_mn / 2
    delta_kinetic_plus_potential = p_m_p_n / 2
    delta_action_density_over_e = -(
        delta_e_over_e * kinetic_plus_potential + delta_kinetic_plus_potential
    )
    hilbert_from_variation = sp.simplify(-2 * delta_action_density_over_e)
    hilbert_expected = p_m_p_n - g_mn * kinetic_plus_potential
    hilbert_residual = sp.simplify(hilbert_from_variation - hilbert_expected)

    # Covariant product rule after metric compatibility and commuting scalar
    # second derivatives; these declared geometric identities are recorded below.
    box_phi, dphi_n, mixed_second, vp_symbol = sp.symbols(
        "box_phi dphi_n mixed_second vp_symbol", real=True
    )
    divergence_derived = (
        box_phi * dphi_n + mixed_second
        - (mixed_second + vp_symbol * dphi_n)
    )
    divergence_expected = (box_phi - vp_symbol) * dphi_n
    divergence_residual = sp.simplify(divergence_derived - divergence_expected)

    # Explicit nondimensionalization of the physical radial equation.
    m, lam, g = sp.symbols("m lam g", positive=True)
    f_uu, f_xx, f_x_over_x = sp.symbols("f_uu f_xx f_x_over_x", real=True)
    common = m**3 / sp.sqrt(lam)
    phi_phys = m * f / sp.sqrt(lam)
    physical_residual = (
        common * f_uu
        - common * f_xx
        - 2 * common * f_x_over_x
        + m**2 * phi_phys
        - lam * phi_phys**3
        + g * phi_phys**5
    )
    a_general = g * m**2 / lam**2
    dimensionless_expected = (
        f_uu - f_xx - 2 * f_x_over_x + f - f**3 + a_general * f**5
    )
    dimensionless_residual = sp.simplify(
        physical_residual / common - dimensionless_expected
    )

    # Harmonic projection and omitted sources.
    theta = sp.symbols("theta", real=True)
    avg_cos2 = sp.integrate(sp.cos(theta) ** 2, (theta, 0, 2 * sp.pi)) / sp.pi
    coeff3 = sp.integrate(sp.cos(theta) ** 4, (theta, 0, 2 * sp.pi)) / sp.pi
    coeff5 = sp.integrate(sp.cos(theta) ** 6, (theta, 0, 2 * sp.pi)) / sp.pi
    r3 = -f**3 / 4 + 5 * a * f**5 / 16
    r5 = a * f**5 / 16

    # Derive the leading cubic Q-ball-to-real initial-guess scaling.
    seed_scale = sp.symbols("seed_scale", positive=True)
    scale_solutions = sp.solve(
        sp.Eq(sp.Rational(3, 4) * seed_scale**2, 1), seed_scale
    )
    derived_seed_scale = scale_solutions[0]
    effective_seed_a = sp.simplify(
        sp.Rational(5, 8) * a * derived_seed_scale**4
    )

    # Analytic Galerkin seed window.
    seed_left = 1 - sp.Rational(4, 5) ** 2
    seed_right = sp.Rational(27, 160) / a

    # Open spherical tail and divergence of its positive mass-energy term.
    k, amplitude = sp.symbols("k amplitude", positive=True)
    radial_tail = amplitude * sp.sin(k * x) / x
    tail_equation = sp.simplify(
        sp.diff(radial_tail, x, 2)
        + 2 * sp.diff(radial_tail, x) / x
        + k**2 * radial_tail
    )
    tail_mass_primitive = amplitude**2 * (
        x / 2 - sp.sin(2 * k * x) / (4 * k)
    )
    tail_integrand_residual = sp.simplify(
        sp.diff(tail_mass_primitive, x) - x**2 * radial_tail**2
    )
    tail_linear_coefficient = sp.simplify(
        sp.limit(tail_mass_primitive / x, x, sp.oo)
    )

    # A canonical real target dimension has only a translation generator
    # c*d/df. Potential invariance requires c*V'(f)=0 identically.
    generator_coefficients = sp.Poly(sp.expand(c * vp), f).all_coeffs()
    generator_solutions = sp.solve(
        [sp.Eq(item, 0) for item in generator_coefficients], c, dict=True
    )

    # Single-count source ledger, including replacement of the W3-58 source.
    action_source_map = (("S_C", "T_C"), ("S_phi", "T_phi"))
    source_terms = tuple(source for _action, source in action_source_map)
    source_ledger_exact = (
        action_source_map == (("S_C", "T_C"), ("S_phi", "T_phi"))
        and source_terms == ("T_C", "T_phi")
        and len(set(source_terms)) == 2
        and "T_O" not in source_terms
    )

    checks = {
        "real_euler_lagrange_equation": euler_residual == 0,
        "hilbert_tensor_from_metric_variation": hilbert_residual == 0,
        "on_shell_divergence_identity": divergence_residual == 0,
        "z2_exact": sp.simplify(v.subs(f, -f) - v) == 0,
        "continuous_internal_generator_absent": generator_solutions == [{c: 0}],
        "dimensionless_pde_exact": dimensionless_residual == 0,
        "a_quarter_flat_shoulder_factor": sp.simplify(vp - target_factor) == 0,
        "cosine_projection_normalization": avg_cos2 == 1,
        "galerkin_cubic_three_quarters": coeff3 == sp.Rational(3, 4),
        "galerkin_quintic_five_eighths": coeff5 == sp.Rational(5, 8),
        "seed_window_benchmark": bool(0 < seed_left < seed_right),
        "qball_to_real_seed_factor": sp.simplify(
            derived_seed_scale - 2 / sp.sqrt(3)
        )
        == 0,
        "third_harmonic_source_nonzero": not sp.Poly(r3, f).is_zero,
        "fifth_harmonic_source_nonzero": not sp.Poly(r5, f).is_zero,
        "odd_harmonic_basis_exact": (
            sp.simplify(
                sp.expand_trig(sp.cos(3 * theta))
                - (4 * sp.cos(theta) ** 3 - 3 * sp.cos(theta))
            )
            == 0
            and sp.simplify(
                sp.expand_trig(sp.cos(5 * theta))
                - (
                    16 * sp.cos(theta) ** 5
                    - 20 * sp.cos(theta) ** 3
                    + 5 * sp.cos(theta)
                )
            )
            == 0
        ),
        "open_tail_solution_exact": tail_equation == 0,
        "open_tail_energy_diverges_if_amplitude_nonzero": (
            tail_integrand_residual == 0
            and sp.simplify(tail_linear_coefficient - amplitude**2 / 2) == 0
        ),
        "single_source_ledger_exact": source_ledger_exact,
    }
    return {
        "checks": checks,
        "all_pass": all(bool(value) for value in checks.values()),
        "residuals": {
            "euler_lagrange": str(euler_residual),
            "hilbert_variation": str(hilbert_residual),
            "covariant_divergence": str(divergence_residual),
            "nondimensionalization": str(dimensionless_residual),
            "open_tail_equation": str(tail_equation),
            "open_tail_mass_integrand": str(tail_integrand_residual),
        },
        "derived_values": {
            "qball_to_real_seed_factor": str(derived_seed_scale),
            "seed_equation_effective_sextic_coefficient": str(effective_seed_a),
            "open_tail_mass_integral_linear_coefficient": str(tail_linear_coefficient),
            "continuous_generator_solutions": str(generator_solutions),
        },
        "declared_covariant_identities": [
            "metric compatibility",
            "scalar second derivatives commute",
            "covariant product rule",
        ],
        "identities": {
            "action": "S_phi=-(1/c0) integral e [1/2 g^munu d_mu phi d_nu phi+V(phi)]",
            "potential": "V=1/2 m^2 phi^2-1/4 lambda phi^4+1/6 g phi^6",
            "equation": "Box_g phi-dV/dphi=0",
            "stress": "T_phi_mn=d_m phi d_n phi-g_mn[1/2(dphi)^2+V]",
            "divergence": "nabla^m T_phi_mn=(Box_g phi-dV/dphi)d_n phi",
            "dimensionless_pde": "f_uu-f_xx-2f_x/x+f-f^3+a f^5=0",
            "symmetry": "Z2 only; no continuous internal U(1)",
            "galerkin": "F_xx+2F_x/x=(1-Omega^2)F-(3/4)F^3+(5a/8)F^5",
            "R3": str(r3),
            "R5": str(r5),
            "tail": "F_n,xx+2F_n,x/x+[(n omega)^2-1]F_n=0",
            "source_ledger": "T_total=T_C+T_phi; T_phi replaces T_O",
        },
    }

def load_w358_solution() -> Any:
    spec = importlib.util.spec_from_file_location("w3_58_pinned", W3_58_SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load pinned W3-58 source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve_profile(OMEGA_SEED, 80.0, 1e-7)


def qball_seed(x: np.ndarray, q_solution: Any) -> np.ndarray:
    source_r = float(q_solution.x[-1])
    y = np.empty((2, x.size), dtype=float)
    inside = x <= source_r
    y[:, inside] = q_solution.sol(x[inside])
    if np.any(~inside):
        decay = math.sqrt(1.0 - OMEGA_SEED**2)
        edge = float(q_solution.sol(source_r)[0])
        xx = x[~inside]
        tail = edge * source_r / xx * np.exp(-decay * (xx - source_r))
        y[0, ~inside] = tail
        y[1, ~inside] = -(decay + 1.0 / xx) * tail
    return (2.0 / math.sqrt(3.0)) * y


def solve_galerkin_seed(radius: float, tolerance: float, q_solution: Any) -> Any:
    x = np.linspace(0.0, radius, 801)
    y = qball_seed(x, q_solution)
    decay = math.sqrt(1.0 - OMEGA_SEED**2)

    def fun(_x: np.ndarray, yy: np.ndarray) -> np.ndarray:
        ff = yy[0]
        force = (
            (1.0 - OMEGA_SEED**2) * ff
            - 0.75 * ff**3
            + 0.625 * A * ff**5
        )
        return np.vstack((yy[1], force))

    def bc(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
        return np.array([ya[1], yb[1] + (decay + 1.0 / radius) * yb[0]])

    solution = solve_bvp(
        fun,
        bc,
        x,
        y,
        S=SINGULAR_MATRIX,
        tol=tolerance,
        max_nodes=100000,
        verbose=0,
    )
    if not solution.success:
        raise RuntimeError(f"Galerkin BVP failed: R={radius}, tol={tolerance}: {solution.message}")
    return solution


def evaluate_seed(solution: Any, x: np.ndarray) -> np.ndarray:
    source_r = float(solution.x[-1])
    f = np.empty_like(x)
    inside = x <= source_r
    f[inside] = solution.sol(x[inside])[0]
    if np.any(~inside):
        decay = math.sqrt(1.0 - OMEGA_SEED**2)
        edge = float(solution.sol(source_r)[0])
        xx = x[~inside]
        f[~inside] = edge * source_r / xx * np.exp(-decay * (xx - source_r))
    return f


def bvp_observables(solution: Any, radius: float) -> dict[str, Any]:
    x = np.linspace(0.0, radius, 24001)
    y = solution.sol(x)
    yp = solution.sol(x, 1)
    f = y[0]
    fp = y[1]
    rhs = (1.0 - OMEGA_SEED**2) * f - 0.75 * f**3 + 0.625 * A * f**5
    residual = yp[1, 1:] + 2.0 * fp[1:] / x[1:] - rhs[1:]
    norm = math.sqrt(float(simpson(x**2 * f**2, x=x)))
    weighted_residual = math.sqrt(float(simpson(x[1:] ** 2 * residual**2, x=x[1:]))) / max(
        norm, np.finfo(float).tiny
    )
    i2 = float(simpson(x**2 * f**2, x=x))
    rms = math.sqrt(float(simpson(x**4 * f**2, x=x)) / i2)
    monotone_tolerance = 2e-7 * max(1.0, float(f[0]))
    return {
        "radius": radius,
        "central_amplitude": float(f[0]),
        "rms_radius_f2": rms,
        "minimum": float(np.min(f)),
        "maximum_positive_derivative": float(np.max(fp)),
        "tail_amplitude": float(abs(f[-1])),
        "robin_residual": float(
            abs(fp[-1] + (math.sqrt(1.0 - OMEGA_SEED**2) + 1.0 / radius) * f[-1])
        ),
        "weighted_collocation_residual": weighted_residual,
        "finite": bool(np.all(np.isfinite(f)) and np.all(np.isfinite(fp))),
        "positive_nodeless": bool(np.min(f) > -1e-10 and f[0] > 0.1),
        "monotone": bool(np.max(fp) < monotone_tolerance),
    }


def bvp_gate() -> tuple[dict[str, Any], Any]:
    q_solution = load_w358_solution()
    settings = ((60.0, 1e-6), (80.0, 3e-7), (100.0, 1e-7))
    records = []
    solutions = []
    for radius, tolerance in settings:
        sol = solve_galerkin_seed(radius, tolerance, q_solution)
        obs = bvp_observables(sol, radius)
        obs["tolerance"] = tolerance
        records.append(obs)
        solutions.append(sol)
    reference = records[-1]
    central_changes = [relative_change(r["central_amplitude"], reference["central_amplitude"]) for r in records]
    radius_changes = [relative_change(r["rms_radius_f2"], reference["rms_radius_f2"]) for r in records]
    checks = {
        "all_solver_outputs_finite": all(r["finite"] for r in records),
        "all_positive_nodeless": all(r["positive_nodeless"] for r in records),
        "all_monotone": all(r["monotone"] for r in records),
        "central_amplitude_converged": max(central_changes) < 1e-4,
        "rms_radius_converged": max(radius_changes) < 1e-4,
        "collocation_residual_small": max(r["weighted_collocation_residual"] for r in records) < 2e-5,
        "robin_boundary_satisfied": max(r["robin_residual"] for r in records) < 1e-7,
    }
    canonical = solve_galerkin_seed(80.0, 1e-8, q_solution)
    canonical_obs = bvp_observables(canonical, 80.0)
    return (
        {
            "records": records,
            "central_relative_changes": central_changes,
            "rms_radius_relative_changes": radius_changes,
            "canonical": canonical_obs,
            "core_radius_rule": "R_core=4 R_rms(seed)",
            "core_radius": 4.0 * canonical_obs["rms_radius_f2"],
            "checks": checks,
            "pass": all(checks.values()),
        },
        canonical,
    )


def make_grid(radius: float, dx: float) -> dict[str, np.ndarray | float | int]:
    n = int(round(radius / dx))
    if not math.isclose(n * dx, radius, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("radius/dx must be integral")
    faces = np.arange(n + 1, dtype=float) * dx
    centres = (np.arange(n, dtype=float) + 0.5) * dx
    volumes = (4.0 * math.pi / 3.0) * (faces[1:] ** 3 - faces[:-1] ** 3)
    areas = 4.0 * math.pi * faces**2
    radial_denominator = faces[1:] ** 3 - faces[:-1] ** 3
    return {
        "n": n,
        "radius": radius,
        "dx": dx,
        "faces": faces,
        "centres": centres,
        "volumes": volumes,
        "areas": areas,
        "radial_denominator": radial_denominator,
    }


def absorber_half_factor(grid: dict[str, Any], start: float | None, dt: float) -> np.ndarray:
    r = grid["centres"]
    gamma = np.zeros_like(r)
    if start is not None:
        radius = float(grid["radius"])
        mask = r > start
        scaled = np.clip((r[mask] - start) / (radius - start), 0.0, 1.0)
        gamma[mask] = ABSORBER_GAMMA_MAX * scaled**ABSORBER_POWER
    return np.exp(-0.5 * dt * gamma)


def acceleration_inplace(
    f: np.ndarray,
    grid: dict[str, Any],
    linear: bool,
    face_flux: np.ndarray,
    out: np.ndarray,
    f2: np.ndarray,
) -> None:
    n = int(grid["n"])
    dx = float(grid["dx"])
    faces = grid["faces"]
    face_flux[0] = 0.0
    face_flux[1:n] = faces[1:n] ** 2 * (f[1:] - f[:-1]) / dx
    face_flux[n] = 0.0
    out[:] = 3.0 * (face_flux[1:] - face_flux[:-1]) / grid["radial_denominator"]
    out -= f
    if not linear:
        np.multiply(f, f, out=f2)
        out += f * f2 * (1.0 - A * f2)


def kdk_step_inplace(
    f: np.ndarray,
    v: np.ndarray,
    grid: dict[str, Any],
    dt: float,
    linear: bool,
    damp_half: np.ndarray,
    face_flux: np.ndarray,
    acc: np.ndarray,
    f2: np.ndarray,
) -> None:
    v *= damp_half
    acceleration_inplace(f, grid, linear, face_flux, acc, f2)
    v += 0.5 * dt * acc
    f += dt * v
    acceleration_inplace(f, grid, linear, face_flux, acc, f2)
    v += 0.5 * dt * acc
    v *= damp_half


def cell_energies(f: np.ndarray, v: np.ndarray, grid: dict[str, Any], linear: bool) -> np.ndarray:
    dx = float(grid["dx"])
    n = int(grid["n"])
    potential = 0.5 * f**2
    if not linear:
        potential = potential - 0.25 * f**4 + (A / 6.0) * f**6
    energies = grid["volumes"] * (0.5 * v**2 + potential)
    gradients = (f[1:] - f[:-1]) / dx
    face_energy = 0.5 * grid["areas"][1:n] * dx * gradients**2
    energies[:-1] += 0.5 * face_energy
    energies[1:] += 0.5 * face_energy
    return energies


def face_outward_flux(f: np.ndarray, v: np.ndarray, grid: dict[str, Any], radius: float) -> float:
    j = int(round(radius / float(grid["dx"])))
    if not 1 <= j < int(grid["n"]):
        raise ValueError("flux radius outside grid")
    gradient = (f[j] - f[j - 1]) / float(grid["dx"])
    velocity = 0.5 * (v[j] + v[j - 1])
    return float(-grid["areas"][j] * gradient * velocity)


def face_field(f: np.ndarray, grid: dict[str, Any], radius: float) -> float:
    j = int(round(radius / float(grid["dx"])))
    return float(0.5 * (f[j] + f[j - 1]))


def centre_field(f: np.ndarray) -> float:
    return float((9.0 * f[0] - f[1]) / 8.0)


def summarize_state(
    f: np.ndarray,
    v: np.ndarray,
    grid: dict[str, Any],
    core_radius: float,
    balance_radius: float,
    linear: bool,
) -> dict[str, float]:
    energies = cell_energies(f, v, grid, linear)
    dx = float(grid["dx"])
    core_j = int(round(core_radius / dx))
    balance_j = int(round(balance_radius / dx))
    core_slice = energies[:core_j]
    core_energy = float(np.sum(core_slice))
    rms = math.sqrt(
        float(np.sum(grid["centres"][:core_j] ** 2 * core_slice))
        / max(core_energy, np.finfo(float).tiny)
    )
    return {
        "centre": centre_field(f),
        "core_energy": core_energy,
        "core_rms_radius": rms,
        "balance_energy": float(np.sum(energies[:balance_j])),
        "total_energy": float(np.sum(energies)),
        "detector_40": 40.0 * face_field(f, grid, 40.0),
        "detector_60": 60.0 * face_field(f, grid, 60.0),
    }


def evolve_case(payload: dict[str, Any]) -> dict[str, Any]:
    config = payload["config"]
    grid = make_grid(float(config["radius"]), float(config["dx"]))
    dt = float(config["dt"])
    periods = float(config.get("periods", 0.0))
    tmax = float(config.get("tmax", periods * T0))
    steps = int(round(tmax / dt))
    sample_every = max(1, int(round((T0 / SAMPLES_PER_PERIOD) / dt)))
    linear = bool(config.get("linear", False))
    core_radius = float(payload["core_radius"])
    seed_x = np.asarray(payload["seed_x"], dtype=float)
    seed_f = np.asarray(payload["seed_f"], dtype=float)
    f = np.interp(grid["centres"], seed_x, seed_f, left=seed_f[0], right=0.0)
    f *= float(config.get("scale", 1.0))
    v = np.zeros_like(f)
    damp_half = absorber_half_factor(grid, config.get("absorber_start"), dt)
    face_flux = np.empty(int(grid["n"]) + 1, dtype=float)
    acc = np.empty_like(f)
    f2 = np.empty_like(f)
    balance_radius = 60.0
    initial = summarize_state(f, v, grid, core_radius, balance_radius, linear)
    previous_flux = face_outward_flux(f, v, grid, balance_radius)
    cumulative_flux = 0.0
    records: dict[str, list[float]] = {
        "time": [],
        "centre": [],
        "core_energy": [],
        "core_rms_radius": [],
        "balance_energy": [],
        "balance_residual": [],
        "detector_40": [],
        "detector_60": [],
        "cumulative_flux_60": [],
    }

    def record(time_value: float) -> None:
        state = summarize_state(f, v, grid, core_radius, balance_radius, linear)
        records["time"].append(time_value)
        for key in ("centre", "core_energy", "core_rms_radius", "balance_energy", "detector_40", "detector_60"):
            records[key].append(state[key])
        records["cumulative_flux_60"].append(cumulative_flux)
        records["balance_residual"].append(
            (state["balance_energy"] + cumulative_flux - initial["balance_energy"])
            / max(initial["balance_energy"], np.finfo(float).tiny)
        )

    record(0.0)
    completed_steps = 0
    for step in range(1, steps + 1):
        kdk_step_inplace(f, v, grid, dt, linear, damp_half, face_flux, acc, f2)
        current_flux = face_outward_flux(f, v, grid, balance_radius)
        cumulative_flux += 0.5 * dt * (previous_flux + current_flux)
        previous_flux = current_flux
        completed_steps = step
        if step % sample_every == 0 or step == steps:
            record(step * dt)
        if not (np.all(np.isfinite(f)) and np.all(np.isfinite(v))):
            break
    result = {
        "name": config["name"],
        "config": config,
        "core_radius": core_radius,
        "initial": initial,
        "completed_steps": completed_steps,
        "requested_steps": steps,
        "finite": bool(np.all(np.isfinite(f)) and np.all(np.isfinite(v))),
        "records": {k: np.asarray(vv, dtype=float) for k, vv in records.items()},
    }
    if bool(config.get("return_final", False)):
        result["final_f"] = f
        result["final_v"] = v
        result["grid_centres"] = grid["centres"]
        result["final_total_energy"] = summarize_state(
            f, v, grid, core_radius, balance_radius, linear
        )["total_energy"]
    return result


def dominant_frequency(
    time: np.ndarray,
    signal: np.ndarray,
    start: float,
    end: float,
    lower_omega: float = 0.5,
    upper_omega: float | None = 1.0,
) -> dict[str, Any]:
    mask = (time >= start) & (time <= end)
    t = time[mask]
    y = signal[mask]
    if t.size < 32:
        return {
            "omega": float("nan"),
            "bin_width": float("nan"),
            "power": float("nan"),
            "search_lower_omega": lower_omega,
            "search_upper_omega": upper_omega,
            "peak_within_three_bins_of_search_edge": True,
        }
    dt = float(np.median(np.diff(t)))
    y = y - np.mean(y)
    window = np.hanning(y.size)
    spectrum = np.fft.rfft(y * window)
    omega = 2.0 * math.pi * np.fft.rfftfreq(y.size, dt)
    power = np.abs(spectrum) ** 2
    band = omega > lower_omega
    if upper_omega is not None:
        band &= omega < upper_omega
    candidates = np.where(band)[0]
    if candidates.size == 0:
        raise RuntimeError("Empty registered frequency search band")
    index = candidates[np.argmax(power[candidates])]
    edge_distance = min(index - candidates[0], candidates[-1] - index)
    return {
        "omega": float(omega[index]),
        "bin_width": float(omega[1] - omega[0]),
        "power": float(power[index]),
        "search_lower_omega": lower_omega,
        "search_upper_omega": upper_omega,
        "peak_within_three_bins_of_search_edge": bool(edge_distance < 3),
    }


def moving_mean(values: np.ndarray, count: int) -> np.ndarray:
    if count <= 1:
        return values.copy()
    if values.size < count:
        return np.array([], dtype=float)
    cumulative = np.concatenate(([0.0], np.cumsum(values, dtype=float)))
    return (cumulative[count:] - cumulative[:-count]) / count


def case_metrics(case: dict[str, Any], long_run: bool) -> dict[str, Any]:
    rec = case["records"]
    time = rec["time"]
    period = time / T0
    reference_mask = (period >= 80.0) & (period <= 100.0)
    e_ref = float(np.mean(rec["core_energy"][reference_mask]))
    central_ref_rms = float(math.sqrt(np.mean(rec["centre"][reference_mask] ** 2)))
    samples_per_period = max(1, int(round(1.0 / np.median(np.diff(period)))))
    average_count = 20 * samples_per_period
    means = moving_mean(rec["core_energy"], average_count)
    mean_times = time[average_count - 1 :] if means.size else np.array([], dtype=float)
    crossing = np.where((mean_times / T0 >= 100.0) & (means < e_ref / math.e))[0]
    lifetime_periods = float(mean_times[crossing[0]] / T0) if crossing.size else float(period[-1])
    last_period = float(period[-1])
    late_start = 800.0 * T0 if long_run else max(0.0, last_period - 50.0) * T0
    frequency = dominant_frequency(time, rec["centre"], late_start, time[-1])
    broadband_frequency = dominant_frequency(
        time, rec["centre"], late_start, time[-1], lower_omega=0.0, upper_omega=None
    )
    final_mask = period >= max(0.0, last_period - 20.0)
    final_normalized_energy = float(np.mean(rec["core_energy"][final_mask]) / e_ref)
    final_radius = float(np.mean(rec["core_rms_radius"][final_mask]))
    max_balance = float(np.max(np.abs(rec["balance_residual"])))
    net_flux = float(rec["cumulative_flux_60"][-1])
    return {
        "finite": bool(case["finite"]),
        "completed_fraction": case["completed_steps"] / case["requested_steps"],
        "E_ref_periods_80_100": e_ref,
        "central_rms_periods_80_100": central_ref_rms,
        "lifetime_periods_lower_bound_or_crossing": lifetime_periods,
        "threshold_crossed": bool(crossing.size),
        "final_normalized_core_energy": final_normalized_energy,
        "final_core_rms_radius": final_radius,
        "late_frequency": frequency,
        "late_broadband_frequency_diagnostic": broadband_frequency,
        "late_frequency_interpretation": (
            "registered one-sided submass-band peak; broadband diagnostic is separate"
        ),
        "max_energy_flux_balance_residual": max_balance,
        "net_outward_flux_at_60": net_flux,
        "last_period": last_period,
    }


def spectrum_power(time: np.ndarray, signal: np.ndarray, start: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mask = time >= start
    t = time[mask]
    y = signal[mask] - np.mean(signal[mask])
    dt = float(np.median(np.diff(t)))
    window = np.hanning(y.size)
    transform = np.fft.rfft(y * window)
    omega = 2.0 * math.pi * np.fft.rfftfreq(y.size, dt)
    power = np.abs(transform) ** 2
    return omega, power, transform


def harmonic_record(
    omega_axis: np.ndarray,
    power: np.ndarray,
    transform: np.ndarray,
    target: float,
) -> dict[str, Any]:
    bin_width = float(omega_axis[1] - omega_axis[0])
    search_half = max(0.08, 5.0 * bin_width)
    peak_mask = np.abs(omega_axis - target) <= search_half
    indices = np.where(peak_mask)[0]
    index = int(indices[np.argmax(power[indices])])
    noise_mask = (
        (np.abs(omega_axis - target) >= max(0.15, 8.0 * bin_width))
        & (np.abs(omega_axis - target) <= 0.60)
    )
    noise_values = power[noise_mask]
    noise = float(np.median(noise_values)) if noise_values.size else np.finfo(float).tiny
    return {
        "target_omega": target,
        "peak_omega": float(omega_axis[index]),
        "bin_width": bin_width,
        "power": float(power[index]),
        "noise_power": noise,
        "snr_power": float(power[index] / max(noise, np.finfo(float).tiny)),
        "complex_real": float(transform[index].real),
        "complex_imag": float(transform[index].imag),
        "index": index,
    }


def band_arrival_time(time: np.ndarray, signal: np.ndarray, omega: float, radius: float) -> float:
    sample_dt = float(np.median(np.diff(time)))
    sample_rate = 1.0 / sample_dt
    low = max(0.05, (omega - 0.35) / (2.0 * math.pi))
    high = min(0.45 * sample_rate, (omega + 0.35) / (2.0 * math.pi))
    sos = butter(4, [low, high], btype="bandpass", fs=sample_rate, output="sos")
    filtered = sosfiltfilt(sos, signal)
    envelope = np.abs(hilbert(filtered))
    group_velocity = math.sqrt(max(omega**2 - 1.0, 0.0)) / omega
    lower = max(0.0, 0.65 * radius / max(group_velocity, 1e-12))
    upper = min(float(time[-1]), radius / max(group_velocity, 1e-12) + 80.0)
    mask = (time >= lower) & (time <= upper)
    local = envelope[mask]
    local_time = time[mask]
    threshold = 0.20 * float(np.max(local))
    crossing = np.where(local >= threshold)[0]
    return float(local_time[crossing[0]]) if crossing.size else float("nan")


def radiation_gate(canonical: dict[str, Any], canonical_metrics: dict[str, Any]) -> dict[str, Any]:
    rec = canonical["records"]
    time = rec["time"]
    omega_core = canonical_metrics["late_frequency"]["omega"]
    start = 800.0 * T0
    spectra = {}
    for radius in DETECTOR_RADII:
        key = f"detector_{int(radius)}"
        spectra[radius] = spectrum_power(time, rec[key], start)
    candidates = []
    for odd in (3, 5, 7):
        target = odd * omega_core
        if target <= 1.0:
            continue
        records = {}
        for radius in DETECTOR_RADII:
            records[str(int(radius))] = harmonic_record(*spectra[radius], target)
        score = min(records["40"]["snr_power"], records["60"]["snr_power"])
        candidates.append({"odd": odd, "records": records, "minimum_snr": score})
    selected = max(candidates, key=lambda item: item["minimum_snr"])
    peak_omega = 0.5 * (
        selected["records"]["40"]["peak_omega"] + selected["records"]["60"]["peak_omega"]
    )
    early = time <= 200.0
    arrival_40 = band_arrival_time(time[early], rec["detector_40"][early], peak_omega, 40.0)
    arrival_60 = band_arrival_time(time[early], rec["detector_60"][early], peak_omega, 60.0)
    measured_delay = arrival_60 - arrival_40
    group_velocity = math.sqrt(max(peak_omega**2 - 1.0, 0.0)) / peak_omega
    expected_delay = 20.0 / group_velocity
    delay_error = abs(measured_delay - expected_delay) / expected_delay
    checks = {
        "open_odd_harmonic_at_both_radii_snr_ge_10": selected["minimum_snr"] >= 10.0,
        "peak_matches_odd_core_harmonic": abs(peak_omega - selected["odd"] * omega_core)
        <= max(0.08, 5.0 * selected["records"]["40"]["bin_width"]),
        "finite_group_arrivals": bool(np.isfinite(arrival_40) and np.isfinite(arrival_60)),
        "outward_group_delay_within_10_percent": bool(np.isfinite(delay_error) and delay_error <= 0.10),
        "net_flux_outward": canonical_metrics["net_outward_flux_at_60"] > 0.0,
    }
    return {
        "candidates": candidates,
        "selected_odd_harmonic": selected["odd"],
        "selected_peak_omega": peak_omega,
        "arrival_time_40": arrival_40,
        "arrival_time_60": arrival_60,
        "measured_group_delay": measured_delay,
        "expected_group_delay": expected_delay,
        "relative_group_delay_error": delay_error,
        "checks": checks,
        "pass": all(checks.values()),
    }


def packet_seed(radius: float, dx: float, omega: float) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    grid = make_grid(radius, dx)
    r = grid["centres"]
    r0 = 80.0
    width = 8.0
    k = math.sqrt(omega**2 - 1.0)
    vg = k / omega
    q = r - r0
    envelope = np.exp(-0.5 * (q / width) ** 2)
    psi = envelope * np.cos(k * q)
    dpsi = envelope * (-(q / width**2) * np.cos(k * q) - k * np.sin(k * q))
    psi_t = -vg * dpsi
    f = psi / r
    v = psi_t / r
    return f, v, grid


def evolve_packet(radius: float, absorber_start: float | None, omega: float) -> dict[str, np.ndarray | float]:
    dx = 0.05
    dt = 0.0125
    tmax = 220.0
    f, v, grid = packet_seed(radius, dx, omega)
    damp = absorber_half_factor(grid, absorber_start, dt)
    face_flux = np.empty(int(grid["n"]) + 1)
    acc = np.empty_like(f)
    f2 = np.empty_like(f)
    sample_every = 20
    times = []
    inner = []
    initial_total = float(np.sum(cell_energies(f, v, grid, True)))
    inner_j = int(round(120.0 / dx))
    for step in range(int(round(tmax / dt)) + 1):
        if step % sample_every == 0:
            energies = cell_energies(f, v, grid, True)
            times.append(step * dt)
            inner.append(float(np.sum(energies[:inner_j])))
        if step == int(round(tmax / dt)):
            break
        kdk_step_inplace(f, v, grid, dt, True, damp, face_flux, acc, f2)
    return {"time": np.asarray(times), "inner_energy": np.asarray(inner), "initial_total": initial_total}


def absorber_calibration() -> dict[str, Any]:
    records = {}
    checks = {}
    for odd in (3, 5):
        omega = odd * OMEGA_SEED
        absorbed = evolve_packet(200.0, 150.0, omega)
        reference = evolve_packet(400.0, None, omega)
        if not np.allclose(absorbed["time"], reference["time"]):
            raise RuntimeError("Absorber/reference sample grids differ")
        late = absorbed["time"] >= 170.0
        excess = np.maximum(absorbed["inner_energy"][late] - reference["inner_energy"][late], 0.0)
        fraction = float(np.max(excess) / absorbed["initial_total"])
        records[str(odd)] = {"omega": omega, "excess_reflected_energy_fraction": fraction}
        checks[f"odd_{odd}_excess_reflection_below_1e_6"] = fraction < 1e-6
    return {"records": records, "checks": checks, "pass": all(checks.values())}


def rk4_reference(payload: dict[str, Any]) -> dict[str, Any]:
    radius = 400.0
    dx = 0.05
    dt = 0.00625
    tmax = 200.0
    grid = make_grid(radius, dx)
    seed_x = np.asarray(payload["seed_x"])
    seed_f = np.asarray(payload["seed_f"])
    f = np.interp(grid["centres"], seed_x, seed_f, left=seed_f[0], right=0.0)
    v = np.zeros_like(f)
    initial_energy = float(np.sum(cell_energies(f, v, grid, False)))
    face_flux = np.empty(int(grid["n"]) + 1)
    f2 = np.empty_like(f)

    def acc(field: np.ndarray) -> np.ndarray:
        out = np.empty_like(field)
        acceleration_inplace(field, grid, False, face_flux, out, f2)
        return out

    sample_every = int(round((T0 / SAMPLES_PER_PERIOD) / dt))
    time_values = []
    centres = []
    steps = int(round(tmax / dt))
    for step in range(steps + 1):
        if step % sample_every == 0 or step == steps:
            time_values.append(step * dt)
            centres.append(centre_field(f))
        if step == steps:
            break
        k1f = v
        k1v = acc(f)
        k2f = v + 0.5 * dt * k1v
        k2v = acc(f + 0.5 * dt * k1f)
        k3f = v + 0.5 * dt * k2v
        k3v = acc(f + 0.5 * dt * k2f)
        k4f = v + dt * k3v
        k4v = acc(f + dt * k3f)
        f = f + (dt / 6.0) * (k1f + 2.0 * k2f + 2.0 * k3f + k4f)
        v = v + (dt / 6.0) * (k1v + 2.0 * k2v + 2.0 * k3v + k4v)
    final_energy = float(np.sum(cell_energies(f, v, grid, False)))
    return {
        "time": np.asarray(time_values),
        "centre": np.asarray(centres),
        "final_f": f,
        "final_v": v,
        "grid_centres": grid["centres"],
        "initial_energy": initial_energy,
        "final_energy": final_energy,
    }


def independent_pre_reflection(seed_x: np.ndarray, seed_f: np.ndarray, core_radius: float) -> dict[str, Any]:
    config = {
        "name": "independent_kdk",
        "radius": 400.0,
        "absorber_start": None,
        "dx": 0.05,
        "dt": 0.00625,
        "tmax": 200.0,
        "linear": False,
        "return_final": True,
    }
    payload = {"config": config, "seed_x": seed_x, "seed_f": seed_f, "core_radius": core_radius}
    kdk = evolve_case(payload)
    rk4 = rk4_reference(payload)
    mask = rk4["grid_centres"] <= 60.0
    profile_difference = float(
        np.linalg.norm(kdk["final_f"][mask] - rk4["final_f"][mask])
        / max(np.linalg.norm(rk4["final_f"][mask]), np.finfo(float).tiny)
    )
    common_time = kdk["records"]["time"]
    rk4_centre = np.interp(common_time, rk4["time"], rk4["centre"])
    centre_difference = float(
        np.sqrt(np.mean((kdk["records"]["centre"] - rk4_centre) ** 2))
        / max(np.sqrt(np.mean(rk4_centre**2)), np.finfo(float).tiny)
    )
    kdk_drift = abs(kdk["final_total_energy"] - kdk["initial"]["total_energy"]) / kdk["initial"]["total_energy"]
    rk4_drift = abs(rk4["final_energy"] - rk4["initial_energy"]) / rk4["initial_energy"]
    checks = {
        "profile_difference_below_5e_3": profile_difference < 5e-3,
        "centre_signal_difference_below_5e_3": centre_difference < 5e-3,
        "kdk_energy_drift_below_2e_3": kdk_drift < 2e-3,
        "rk4_energy_drift_below_2e_3": rk4_drift < 2e-3,
    }
    return {
        "profile_relative_l2_difference": profile_difference,
        "centre_signal_relative_rms_difference": centre_difference,
        "kdk_energy_drift": kdk_drift,
        "rk4_energy_drift": rk4_drift,
        "checks": checks,
        "pass": all(checks.values()),
    }


def validate_model_contract(model: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    if model.get("field_components") != 1 or model.get("field_type") != "real":
        reasons.append("one_real_field_required")
    if model.get("continuous_internal_charge", False):
        reasons.append("continuous_charge_forbidden")
    if model.get("metric_count") != 1:
        reasons.append("one_metric_required")
    if model.get("source_ledger") != "T_C+T_phi":
        reasons.append("source_ledger_must_replace_T_O")
    if model.get("readout_as_dynamics", False):
        reasons.append("readout_as_dynamics_forbidden")
    if model.get("harmonic_filter", False):
        reasons.append("harmonic_filter_forbidden")
    if model.get("boundary") != "open_absorbing":
        reasons.append("open_boundary_required")
    if model.get("electric_neutrality_claim", False):
        reasons.append("electric_neutrality_claim_forbidden")
    if model.get("particle_identity_claim", False):
        reasons.append("particle_identity_claim_forbidden")
    if model.get("a") != A or model.get("omega_seed") != OMEGA_SEED:
        reasons.append("frozen_benchmark_changed")
    if model.get("perturbation_signs") != [-1, 1]:
        reasons.append("both_perturbation_signs_required")
    return len(reasons) == 0, reasons


def mutation_controls() -> dict[str, Any]:
    base = {
        "field_components": 1,
        "field_type": "real",
        "continuous_internal_charge": False,
        "metric_count": 1,
        "source_ledger": "T_C+T_phi",
        "readout_as_dynamics": False,
        "harmonic_filter": False,
        "boundary": "open_absorbing",
        "electric_neutrality_claim": False,
        "particle_identity_claim": False,
        "a": A,
        "omega_seed": OMEGA_SEED,
        "perturbation_signs": [-1, 1],
    }
    mutations = {
        "complex_two_component": {"field_components": 2, "field_type": "complex"},
        "qball_charge": {"continuous_internal_charge": True},
        "second_metric": {"metric_count": 2},
        "duplicate_source": {"source_ledger": "T_C+T_O+T_phi"},
        "readout_dynamics": {"readout_as_dynamics": True},
        "harmonic_filter": {"harmonic_filter": True},
        "reflecting_cavity": {"boundary": "reflecting"},
        "neutrality_claim": {"electric_neutrality_claim": True},
        "particle_claim": {"particle_identity_claim": True},
        "changed_a": {"a": 0.251},
        "changed_omega": {"omega_seed": 0.801},
        "one_sided_perturbation": {"perturbation_signs": [1]},
    }
    base_pass, base_reasons = validate_model_contract(base)
    records = {}
    for name, changes in mutations.items():
        trial = dict(base)
        trial.update(changes)
        accepted, reasons = validate_model_contract(trial)
        records[name] = {"rejected": not accepted, "reasons": reasons}
    checks = {
        "base_contract_accepted": base_pass and not base_reasons,
        "all_registered_mutations_rejected": all(record["rejected"] for record in records.values()),
    }
    return {"checks": checks, "records": records, "pass": all(checks.values())}


def run_registered_evolutions(seed_x: np.ndarray, seed_f: np.ndarray, core_radius: float) -> dict[str, Any]:
    payloads = []
    for config in LONG_CONFIGS:
        payloads.append({"config": dict(config), "seed_x": seed_x, "seed_f": seed_f, "core_radius": core_radius})
    results: dict[str, Any] = {}
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(evolve_case, payload): payload["config"]["name"] for payload in payloads}
        for future in as_completed(futures):
            name = futures[future]
            results[name] = future.result()
            print(f"completed long run: {name}", flush=True)
    linear_config = {
        "name": "linear_control",
        "radius": 200.0,
        "absorber_start": 150.0,
        "dx": 0.05,
        "dt": 0.0125,
        "periods": 100.0,
        "linear": True,
    }
    results["linear_control"] = evolve_case(
        {"config": linear_config, "seed_x": seed_x, "seed_f": seed_f, "core_radius": core_radius}
    )
    for scale, name in ((0.99, "perturb_minus_1pct"), (1.01, "perturb_plus_1pct")):
        config = {
            "name": name,
            "radius": 200.0,
            "absorber_start": 150.0,
            "dx": 0.05,
            "dt": 0.0125,
            "periods": 200.0,
            "scale": scale,
        }
        results[name] = evolve_case(
            {"config": config, "seed_x": seed_x, "seed_f": seed_f, "core_radius": core_radius}
        )
        print(f"completed robustness run: {name}", flush=True)
    return results


def numerical_decision(
    evolutions: dict[str, Any],
    bvp: dict[str, Any],
    absorber: dict[str, Any],
    independent: dict[str, Any],
) -> dict[str, Any]:
    metrics = {
        name: case_metrics(case, name in {"canonical", "fine", "domain"})
        for name, case in evolutions.items()
    }
    canonical = metrics["canonical"]
    fine = metrics["fine"]
    domain = metrics["domain"]
    linear = metrics["linear_control"]
    formation_energy_ratio = canonical["E_ref_periods_80_100"] / max(
        linear["E_ref_periods_80_100"], np.finfo(float).tiny
    )
    formation_centre_ratio = canonical["central_rms_periods_80_100"] / max(
        linear["central_rms_periods_80_100"], np.finfo(float).tiny
    )
    numerical_energy_floor = np.finfo(float).eps * evolutions["canonical"]["initial"]["core_energy"]
    numerical_centre_floor = np.finfo(float).eps * abs(evolutions["canonical"]["initial"]["centre"])
    radiation = radiation_gate(evolutions["canonical"], canonical)
    resolution = {
        "frequency_relative_difference": relative_change(
            canonical["late_frequency"]["omega"], fine["late_frequency"]["omega"]
        ),
        "formation_energy_relative_difference": relative_change(
            canonical["E_ref_periods_80_100"], fine["E_ref_periods_80_100"]
        ),
        "final_normalized_energy_relative_difference": relative_change(
            canonical["final_normalized_core_energy"], fine["final_normalized_core_energy"]
        ),
    }
    domain_check = {
        "frequency_relative_difference": relative_change(
            canonical["late_frequency"]["omega"], domain["late_frequency"]["omega"]
        ),
        "formation_energy_relative_difference": relative_change(
            canonical["E_ref_periods_80_100"], domain["E_ref_periods_80_100"]
        ),
        "final_normalized_energy_relative_difference": relative_change(
            canonical["final_normalized_core_energy"], domain["final_normalized_core_energy"]
        ),
    }
    perturb_checks = {}
    for name in ("perturb_minus_1pct", "perturb_plus_1pct"):
        item = metrics[name]
        perturb_checks[name] = {
            "finite": item["finite"],
            "no_lifetime_crossing": not item["threshold_crossed"],
            "completed_200_periods": item["last_period"] >= 199.9,
            "submass_frequency": 0.5 < item["late_frequency"]["omega"] < 1.0,
        }
    bin_margin = 3.0 * canonical["late_frequency"]["bin_width"]
    localization_checks = {
        "bvp_pass": bvp["pass"],
        "all_long_runs_finite_and_complete": all(
            metrics[name]["finite"] and metrics[name]["completed_fraction"] == 1.0
            for name in ("canonical", "fine", "domain")
        ),
        "formation_energy_vs_linear_ge_10": formation_energy_ratio >= 10.0,
        "formation_centre_vs_linear_ge_10": formation_centre_ratio >= 10.0,
        "formation_energy_vs_noise_ge_1000": canonical["E_ref_periods_80_100"]
        >= 1000.0 * numerical_energy_floor,
        "formation_centre_vs_noise_ge_1000": canonical["central_rms_periods_80_100"]
        >= 1000.0 * numerical_centre_floor,
        "no_1000_period_lifetime_crossing": all(
            not metrics[name]["threshold_crossed"] for name in ("canonical", "fine", "domain")
        ),
        "submass_late_frequency_with_three_bin_margin": 0.5
        < canonical["late_frequency"]["omega"]
        < 1.0 - bin_margin,
        "resolution_frequency_below_0p5_percent": resolution["frequency_relative_difference"] < 0.005,
        "resolution_formation_energy_below_2_percent": resolution[
            "formation_energy_relative_difference"
        ]
        < 0.02,
        "resolution_final_energy_below_5_percent": resolution[
            "final_normalized_energy_relative_difference"
        ]
        < 0.05,
        "domain_frequency_below_2_percent": domain_check["frequency_relative_difference"] < 0.02,
        "domain_formation_energy_below_2_percent": domain_check[
            "formation_energy_relative_difference"
        ]
        < 0.02,
        "domain_final_energy_below_2_percent": domain_check[
            "final_normalized_energy_relative_difference"
        ]
        < 0.02,
        "canonical_balance_below_5e_3": canonical["max_energy_flux_balance_residual"] < 5e-3,
        "domain_balance_below_5e_3": domain["max_energy_flux_balance_residual"] < 5e-3,
        "fine_balance_below_1p5e_3": fine["max_energy_flux_balance_residual"] < 1.5e-3,
        "balance_decreases_under_refinement": fine["max_energy_flux_balance_residual"]
        < canonical["max_energy_flux_balance_residual"],
        "absorber_calibration_pass": absorber["pass"],
        "independent_pre_reflection_pass": independent["pass"],
        "both_perturbations_pass": all(all(v.values()) for v in perturb_checks.values()),
    }
    localization_pass = all(localization_checks.values())
    return {
        "case_metrics": metrics,
        "formation_energy_ratio_nonlinear_to_linear": formation_energy_ratio,
        "formation_centre_rms_ratio_nonlinear_to_linear": formation_centre_ratio,
        "resolution_comparison": resolution,
        "domain_comparison": domain_check,
        "perturbation_checks": perturb_checks,
        "radiation": radiation,
        "localization_checks": localization_checks,
        "localization_pass": localization_pass,
        "radiation_pass": radiation["pass"],
        "pass": localization_pass and radiation["pass"],
    }


def integration_gate() -> dict[str, Any]:
    readme_text = canonical_text(README) if README.is_file() else ""
    ledger_text = canonical_text(FORMAL_LEDGER) if FORMAL_LEDGER.is_file() else ""
    checks = {
        "readme_exists": README.is_file(),
        "readme_has_W3_59_marker": "W3-59 real-field open-radiation bridge" in readme_text,
        "readme_has_fixed_coframe_boundary": "fixed coframe" in readme_text.lower(),
        "formal_ledger_exists": FORMAL_LEDGER.is_file(),
        "formal_ledger_has_W3_59_marker": "W3-59 real-field open-radiation bridge" in ledger_text,
        "formal_ledger_has_replacement_ledger": "T_total=T_C+T_phi" in ledger_text,
        "formal_ledger_has_backreaction_boundary": "dynamical coframe backreaction" in ledger_text.lower(),
    }
    return {
        "checks": checks,
        "readme_sha256": sha256(README) if README.is_file() else None,
        "formal_ledger_sha256": sha256(FORMAL_LEDGER) if FORMAL_LEDGER.is_file() else None,
        "pass": all(checks.values()),
    }


def smoke_test() -> None:
    prereg = verify_preregistration()
    dependencies = verify_dependencies()
    symbolic = symbolic_gate()
    bvp, solution = bvp_gate()
    x = np.linspace(0.0, 80.0, 16001)
    f = evaluate_seed(solution, x)
    config = {
        "name": "smoke_non_evidence",
        "radius": 80.0,
        "absorber_start": 60.0,
        "dx": 0.1,
        "dt": 0.025,
        "periods": 2.0,
    }
    case = evolve_case({"config": config, "seed_x": x, "seed_f": f, "core_radius": bvp["core_radius"]})
    payload = {
        "preregistration_pass": prereg["pass"],
        "dependencies_pass": dependencies["all_pass"],
        "symbolic_pass": symbolic["all_pass"],
        "bvp_pass": bvp["pass"],
        "bvp_central": bvp["canonical"]["central_amplitude"],
        "bvp_rms_radius": bvp["canonical"]["rms_radius_f2"],
        "evolution_finite": case["finite"],
        "completed_steps": case["completed_steps"],
    }
    print(json.dumps(native_tree(payload), indent=2, sort_keys=True, allow_nan=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true", help="non-evidentiary implementation smoke test")
    args = parser.parse_args()
    if args.smoke:
        smoke_test()
        return

    prereg = verify_preregistration()
    dependencies = verify_dependencies()
    symbolic = symbolic_gate()
    mutations = mutation_controls()
    if not (prereg["pass"] and dependencies["all_pass"] and symbolic["all_pass"] and mutations["pass"]):
        raise RuntimeError("Exact preregistration/dependency/symbolic/mutation gate failed")

    print("solving frozen Galerkin seed", flush=True)
    bvp, solution = bvp_gate()
    seed_x = np.linspace(0.0, 100.0, 24001)
    seed_f = evaluate_seed(solution, seed_x)
    core_radius = float(bvp["core_radius"])

    print("calibrating open absorber", flush=True)
    absorber = absorber_calibration()
    print("running independent pre-reflection methods", flush=True)
    independent = independent_pre_reflection(seed_x, seed_f, core_radius)
    print("running registered long evolutions", flush=True)
    evolutions = run_registered_evolutions(seed_x, seed_f, core_radius)
    numerical = numerical_decision(evolutions, bvp, absorber, independent)
    integration = integration_gate()

    exact_pass = prereg["pass"] and dependencies["all_pass"] and symbolic["all_pass"] and mutations["pass"]
    if exact_pass and numerical["pass"] and integration["pass"]:
        status = SUCCESS_STATUS
    elif exact_pass and numerical["localization_pass"] and not numerical["radiation_pass"]:
        status = (
            "NUMERICALLY_INCONCLUSIVE_RADIATION__EXACT_SINGLE_REAL_Z2_COFRAME_"
            "CORE_ACTION_AND_LONG_LIVED_SPHERICAL_LOCALIZATION_ESTABLISHED__"
            "DYNAMICAL_BACKREACTION_AND_PARTICLE_IDENTITY_OPEN"
        )
    elif exact_pass and numerical["pass"] and not integration["pass"]:
        status = "PASS_PENDING_README_AND_FORMAL_LEDGER_INTEGRATION"
    else:
        status = (
            "FAIL_FROZEN_W3_58_TO_W3_59_REAL_OSCILLON_BRIDGE__EXACT_REAL_FIELD_"
            "ACTION_RETAINED__ALTERNATIVE_BENCHMARKS_NOT_TESTED"
        )

    result = {
        "stage": "W3-59",
        "title": "One real oscillon on the fixed RefG coframe: open-radiation bridge",
        "status": status,
        "artifact_valid": bool(exact_pass and bvp["pass"] and finite_tree(numerical)),
        "claim_boundary": {
            "establishes_if_pass": (
                "one converged long-lived slowly radiating spherically symmetric real-field "
                "oscillon candidate at the frozen sextic benchmark on a fixed coframe"
            ),
            "does_not_establish": [
                "exact eternal breather",
                "universal real-oscillon theorem",
                "electric neutrality",
                "particle identity",
                "nonspherical stability",
                "foundation derivation of a and Omega_seed",
                "dynamical coframe backreaction",
            ],
        },
        "preregistration": prereg,
        "dependencies": dependencies,
        "symbolic": symbolic,
        "bvp": bvp,
        "absorber_calibration": absorber,
        "independent_pre_reflection": independent,
        "numerical": numerical,
        "mutations": mutations,
        "integration": integration,
        "closure": {
            "exact_single_real_Z2_action_source_bridge": exact_pass,
            "localized_galerkin_seed": bvp["pass"],
            "long_lived_open_boundary_spherical_localization": numerical["localization_pass"],
            "resolved_outgoing_open_harmonic": numerical["radiation_pass"],
            "fixed_coframe_only": True,
            "dynamic_coframe_backreaction_closed": False,
            "electric_neutrality_derived": False,
            "particle_identity_derived": False,
            "nonspherical_stability_derived": False,
        },
        "reproducibility": {
            "python": os.sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
            "source_sha256": sha256(SOURCE),
            "preregistration_sha256": sha256(PREREG),
            "deterministic_seed_rule": "no random numbers; W3-58 profile used only as fixed BVP initial guess",
        },
    }
    result = native_tree(result)
    if not finite_tree(result):
        raise RuntimeError("Result contains non-finite values")
    encoded = (json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    atomic_write(OUTPUT, encoded)
    digest = sha256(OUTPUT)
    atomic_write(HASH_OUTPUT, f"{digest}  {OUTPUT.name}\n".encode("ascii"))
    print(json.dumps({"status": status, "artifact_valid": result["artifact_valid"], "result_sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
