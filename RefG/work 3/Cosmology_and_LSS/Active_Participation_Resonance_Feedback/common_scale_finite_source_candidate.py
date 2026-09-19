"""Bounded finite-source test of a NEW scalar composite-metric candidate.

This is not an Einstein-Hilbert reduction or a replacement of the retained
RefG gravitational architecture. Results and provenance go to stdout only.
Run with python -B; the unchanged W58 solver supplies the zero-coupling core.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import platform
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp
from scipy.sparse import bmat, coo_matrix
from scipy.sparse.linalg import LinearOperator, eigsh, factorized

HERE = Path(__file__).resolve().parent
WORK3 = HERE.parents[1]
SOURCE = Path(__file__).resolve()
CONTRACT = HERE / "common_scale_finite_source_candidate.md"
W58 = (
    WORK3 / "Lagrangian_Formulation"
    / "One_Oscillon_Coframe_Localized_Core"
    / "w3_58_one_oscillon_coframe_localized_core.py"
)
W58_SHA256 = "b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57"
ALPHAS = (0.001, 0.003)
RESOLUTIONS = ((40.0, 1e-6, 8001), (60.0, 3e-8, 16001))
HESSIAN_GRIDS = {40.0: (240, 480), 60.0: (360, 720)}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def potential(f):
    return f**2 / 2 - f**4 / 4 + f**6 / 24


def potential_prime(f):
    return f - f**3 + f**5 / 4


def potential_second(f):
    return 1 - 3 * f**2 + 5 * f**4 / 4


def relative(value, reference):
    return abs(float(value) - float(reference)) / max(abs(float(reference)), 1e-30)


def symbolic_checks():
    a, u, f, w, r = sp.symbols("alpha u f omega r", positive=True)
    v = f**2 / 2 - f**4 / 4 + f**6 / 24
    phase = w**2 * sp.exp(4 * u) * f**2 / 2
    vbar = sp.exp(2 * u) * v
    density = phase - vbar
    checks = {}
    checks["source_is_same_action_derivative"] = sp.simplify(
        sp.diff(density, u) - (4 * phase - 2 * vbar)
    ) == 0
    checks["amplitude_same_action_derivative"] = sp.simplify(
        -sp.diff(density, f)
        - (sp.exp(2 * u) * sp.diff(v, f) - w**2 * sp.exp(4 * u) * f)
    ) == 0
    gu, gf, t, vv = sp.symbols("G_u G_f T Vbar", real=True)
    checks["energy_minus_source_equals_virial"] = sp.expand(
        (gu + gf + t + vv) - (4 * t - 2 * vv)
        - (gu + gf + 3 * vv - 3 * t)
    ) == 0
    p = sp.exp(-u)
    checks["common_clock_rod_and_light_readout"] = (
        sp.simplify(sp.sqrt(p**2 / p**-2) - p**2) == 0
    )
    checks["static_ppn_beta_gamma_only"] = (
        sp.series(-sp.exp(-2 * u), u, 0, 3).removeO() == -1 + 2 * u - 2 * u**2
        and sp.series(sp.exp(2 * u), u, 0, 2).removeO() == 1 + 2 * u
    )
    checks["radial_hessian_local_entries"] = all(
        sp.simplify(x - y) == 0
        for x, y in (
            (-sp.diff(density, f, 2), sp.exp(2*u)*sp.diff(v, f, 2) - w**2*sp.exp(4*u)),
            (-sp.diff(density, f, u), 2*sp.exp(2*u)*sp.diff(v, f) - 4*w**2*sp.exp(4*u)*f),
            (-sp.diff(density, u, 2), 4*sp.exp(2*u)*v - 8*w**2*sp.exp(4*u)*f**2),
        )
    )
    charge, inertia = sp.symbols("Q I", positive=True)
    checks["fixed_charge_rank_one_coefficient"] = (
        sp.simplify(sp.diff(charge**2 / (2*inertia), inertia, 2)
                    - charge**2 / inertia**3) == 0
    )
    checks["both_principal_speeds_equal_p_squared"] = (
        sp.simplify(sp.sqrt((1/a)/(sp.exp(4*u)/a)) - p**2) == 0
        and sp.simplify(sp.sqrt(1/sp.exp(4*u)) - p**2) == 0
    )
    tt, xx = sp.symbols("t x", real=True)
    uu, aa, bb = [sp.Function(name)(tt, xx) for name in ("u", "a", "b")]
    s = aa**2 + bb**2
    vv_dynamic = s/2 - s**2/4 + s**3/24
    fields = (uu, aa, bb)
    speeds = [sp.diff(field, tt) for field in fields]
    gradients = [sp.diff(field, xx) for field in fields]
    lagrangian = (
        (sp.exp(4*uu)*speeds[0]**2 - gradients[0]**2)/(2*a)
        + sp.exp(4*uu)*(speeds[1]**2+speeds[2]**2)/2
        - (gradients[1]**2+gradients[2]**2)/2
        - sp.exp(2*uu)*vv_dynamic
    )
    momenta = [sp.diff(lagrangian, speed) for speed in speeds]
    flux_derivatives = [sp.diff(lagrangian, gradient) for gradient in gradients]
    el = [
        sp.diff(momentum, tt) + sp.diff(flux_derivative, xx)
        - sp.diff(lagrangian, field)
        for field, momentum, flux_derivative in zip(fields, momenta, flux_derivatives)
    ]
    energy = sum(speed*momentum for speed, momentum in zip(speeds, momenta)) - lagrangian
    energy_flux = sum(speed*flux for speed, flux in zip(speeds, flux_derivatives))
    checks["dynamic_same_action_local_energy_balance"] = sp.simplify(
        sp.diff(energy, tt) + sp.diff(energy_flux, xx)
        - sum(speed*equation for speed, equation in zip(speeds, el))
    ) == 0
    checks["dynamic_foundation_equation"] = sp.simplify(
        el[0] - (
            (sp.exp(4*uu)*(sp.diff(uu, tt, 2)+2*speeds[0]**2)
             - sp.diff(uu, xx, 2))/a
            - 2*sp.exp(4*uu)*(speeds[1]**2+speeds[2]**2)
            + 2*sp.exp(2*uu)*vv_dynamic
        )
    ) == 0
    return checks


def coupled_profile(reference, charge, alpha, radius, tolerance, previous=None):
    x = np.linspace(0.0, radius, 1001)
    if previous is None:
        f, fp = reference.sol(x)
        omega = 0.8
        source = 2 * omega**2 * f**2 - 2 * potential(f)
        inside = cumulative_trapezoid(x**2 * source, x, initial=0)
        outer = cumulative_trapezoid(x * source, x, initial=0)
        u = alpha * (outer[-1] - outer)
        u[1:] += alpha * inside[1:] / x[1:]
        up = np.zeros_like(x)
        up[1:] = -alpha * inside[1:] / x[1:]**2
        qacc = cumulative_trapezoid(omega*np.exp(4*u)*x**2*f**2, x, initial=0)
        seed = np.vstack((f, fp, u, up, qacc))
    else:
        seed = previous.sol(x)
        omega = float(previous.p[0])
    singular = np.zeros((5, 5))
    singular[1, 1] = singular[3, 3] = -2

    def rhs(xx, yy, parameters):
        ff, ff_prime, uu, uu_prime = yy[:4]
        om = parameters[0]
        e2 = np.exp(2 * uu)
        e4 = e2**2
        return np.vstack((
            ff_prime,
            e2 * potential_prime(ff) - e4 * om**2 * ff,
            uu_prime,
            -alpha * (2*e4*om**2*ff**2 - 2*e2*potential(ff)),
            om * e4 * xx**2 * ff**2,
        ))

    def boundary(ya, yb, parameters):
        om = parameters[0]
        # Iterative proposals may leave the localization interval; acceptance
        # independently enforces 0<Omega<1 on the converged solution.
        k = math.sqrt(max(1 - om**2, 1e-12))
        return np.array((
            ya[1], ya[3], ya[4],
            yb[1] + (k + 1/radius)*yb[0],
            yb[3] + yb[2]/radius,
            yb[4] - charge/(4*np.pi),
        ))

    solution = solve_bvp(
        rhs, boundary, x, seed, p=np.array([omega]), S=singular,
        tol=tolerance, max_nodes=20000, verbose=0,
    )
    if not solution.success:
        raise RuntimeError(
            f"Frozen BVP failed alpha={alpha}, R={radius}: {solution.message}"
        )
    return solution


def observables(solution, alpha, radius, points, charge):
    r = np.linspace(0.0, radius, points)
    f, fp, u, up, qacc = solution.sol(r)
    omega = float(solution.p[0])
    e2 = np.exp(2*u)
    e4 = e2**2

    def integrate(value):
        return float(4*np.pi*simpson(r**2*value, x=r))

    phase = integrate(e4*omega**2*f**2/2)
    gradient_f = integrate(fp**2/2)
    vbar = integrate(e2*potential(f))
    tail = float(2*np.pi*radius*u[-1]**2/alpha)
    gradient_u = integrate(up**2/(2*alpha)) + tail
    energy = phase + gradient_f + vbar + gradient_u
    source = integrate(2*e4*omega**2*f**2 - 2*e2*potential(f))
    gauss_mass = float(-4*np.pi*radius**2*up[-1]/alpha)
    q_integral = integrate(omega*e4*f**2)
    rms = math.sqrt(integrate(r**2*omega*e4*f**2)/q_integral)
    virial = gradient_u + gradient_f + 3*vbar - 3*phase
    return {
        "alpha": alpha, "radius": radius, "quadrature_points": points,
        "omega": omega, "charge_integral": q_integral,
        "charge_relative_residual": relative(q_integral, charge),
        "central_amplitude": float(f[0]), "central_p": float(np.exp(-u[0])),
        "maximum_abs_u": float(np.max(np.abs(u))),
        "minimum_f": float(np.min(f)),
        "energy": energy, "mass_gauss": gauss_mass, "mass_source": source,
        "mass_energy_relative": relative(gauss_mass, energy),
        "mass_source_relative": relative(gauss_mass, source),
        "virial": virial,
        "virial_relative": abs(virial)/max(energy, 1e-30),
        "phase_energy": phase, "amplitude_gradient_energy": gradient_f,
        "potential_energy": vbar, "foundation_gradient_energy": gradient_u,
        "foundation_exterior_tail_energy": tail,
        "charge_rms_radius": rms,
        "collocation_max_rms_residual": float(np.max(solution.rms_residuals)),
        "adaptive_nodes": int(solution.x.size),
        "endpoint_amplitude": float(f[-1]),
        "exterior_u_coefficient": float(radius*u[-1]),
        "qacc_endpoint_relative": relative(4*np.pi*qacc[-1], charge),
    }


def radial_hessian(solution, alpha, radius, cells, charge):
    """Consistent P1 finite elements, three-point Gaussian coefficient rule.

    h=r delta f, k=r delta u/sqrt(alpha); both vanish at 0, h(R)=0.
    The analytically integrated exterior u-tail gives the natural k'(R)=0.
    The rank-one term retains the fixed-total-charge constraint.
    """
    step = radius/cells
    rows, cols = [], []
    data_mass, data_stiffness = [], []
    data_hh, data_hk, data_kk = [], [], []
    vector_h, vector_k = np.zeros(cells+1), np.zeros(cells+1)
    gauss_x, gauss_w = np.polynomial.legendre.leggauss(3)
    omega = float(solution.p[0])
    for cell in range(cells):
        xx = step*(cell + (gauss_x+1)/2)
        f, _, u, _, _ = solution.sol(xx)
        e2, e4 = np.exp(2*u), np.exp(4*u)
        uff = e2*potential_second(f)-omega**2*e4
        ufu = np.sqrt(alpha)*(2*e2*potential_prime(f)-4*omega**2*e4*f)
        uuu = alpha*(4*e2*potential(f)-8*omega**2*e4*f**2)
        shape = np.vstack(((1-gauss_x)/2, (1+gauss_x)/2))
        weights = gauss_w*step/2
        wh = xx*e4*2*f
        wk = xx*e4*4*np.sqrt(alpha)*f**2
        for i in range(2):
            ni = cell+i
            vector_h[ni] += np.sum(weights*shape[i]*wh)
            vector_k[ni] += np.sum(weights*shape[i]*wk)
            for j in range(2):
                rows.append(ni)
                cols.append(cell+j)
                weight = weights*shape[i]*shape[j]
                data_mass.append(float(np.sum(weight)))
                data_stiffness.append((1 if i == j else -1)/step)
                data_hh.append(float(np.sum(weight*uff)))
                data_hk.append(float(np.sum(weight*ufu)))
                data_kk.append(float(np.sum(weight*uuu)))
    shape = (cells+1, cells+1)

    def sparse(values):
        return coo_matrix((values, (rows, cols)), shape=shape).tocsr()

    m, stiffness = sparse(data_mass), sparse(data_stiffness)
    hh, hk, kk = sparse(data_hh), sparse(data_hk), sparse(data_kk)
    ih, ik = np.arange(1, cells), np.arange(1, cells+1)
    mass = bmat([[m[ih][:, ih], None], [None, m[ik][:, ik]]], format="csc")
    local = bmat([
        [(stiffness+hh)[ih][:, ih], hk[ih][:, ik]],
        [hk[ik][:, ih], (stiffness+kk)[ik][:, ik]],
    ], format="csr")
    vector = np.concatenate((vector_h[ih], vector_k[ik]))
    inertia = charge/omega
    coefficient = 4*np.pi*omega**2/inertia

    def apply(value):
        return local @ value + coefficient*vector*np.dot(vector, value)

    operator = LinearOperator(local.shape, matvec=apply, dtype=float)
    inverse_mass = factorized(mass)
    minv = LinearOperator(mass.shape, matvec=inverse_mass, dtype=float)
    seed = np.sin(np.arange(1, mass.shape[0]+1)*0.12345)
    values, vectors = eigsh(
        operator, k=2, M=mass, Minv=minv, which="SA", tol=1e-10,
        maxiter=20000, v0=seed,
    )
    order = np.argsort(values)
    values, vectors = values[order], vectors[:, order]
    residuals = []
    for eigenvalue, vector_e in zip(values, vectors.T):
        residuals.append(float(np.linalg.norm(
            apply(vector_e)-eigenvalue*(mass@vector_e)
        ) / max(np.linalg.norm(mass@vector_e), 1e-30)))
    return {
        "radius": radius, "cells": cells, "spacing": step,
        "smallest_two_eigenvalues": values.tolist(),
        "eigen_equation_absolute_residuals": residuals,
        "positive_sampled_fixed_charge_hessian": bool(np.all(values > 0)),
        "boundary": "h(0)=k(0)=h(R)=0; natural k_prime(R)=0 with u exterior tail",
        "meaning": "finite-domain fixed-Q radial energy Hessian, not a dynamical frequency or uniform infinite-domain gap",
    }


def run():
    if digest(W58) != W58_SHA256:
        raise RuntimeError("W58 source hash changed; frozen dependency mismatch")
    spec = importlib.util.spec_from_file_location("w58_reference_no_write", W58)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    reference = module.solve_profile(0.8, radius=80.0, tolerance=1e-8)
    x = np.linspace(0, 80, 24001)
    f, fp = reference.sol(x)
    charge = float(4*np.pi*0.8*simpson(x**2*f**2, x=x))
    energy0 = float(4*np.pi*simpson(
        x**2*(0.5*fp**2+0.5*0.8**2*f**2+potential(f)), x=x
    ))
    radius0 = math.sqrt(float(
        4*np.pi*0.8*simpson(x**4*f**2, x=x)/charge
    ))
    exact = symbolic_checks()
    records, solutions, numerical_checks = [], {}, {}
    for radius, tolerance, points in RESOLUTIONS:
        previous = None
        for alpha in ALPHAS:
            solution = coupled_profile(reference, charge, alpha, radius, tolerance, previous)
            previous = solution
            solutions[(radius, alpha)] = solution
            row = observables(solution, alpha, radius, points, charge)
            alternate_points = 16001 if points == 8001 else 8001
            alternate = observables(
                solution, alpha, radius, alternate_points, charge
            )
            row["same_profile_quadrature_changes"] = {
                key: relative(row[key], alternate[key])
                for key in ("energy", "mass_source", "charge_integral", "charge_rms_radius")
            }
            row["tolerance"] = tolerance
            row["energy_relative_to_zero_coupling"] = row["energy"]/energy0
            row["radius_relative_to_zero_coupling"] = row["charge_rms_radius"]/radius0
            records.append(row)
            prefix = f"R{radius:g}_alpha{alpha:g}"
            numerical_checks[prefix+"_source_energy_virial"] = all(
                row[key] < 2e-5
                for key in ("mass_energy_relative", "mass_source_relative", "virial_relative")
            )
            numerical_checks[prefix+"_charge"] = row["charge_relative_residual"] < 1e-7
            numerical_checks[prefix+"_collocation"] = (
                row["collocation_max_rms_residual"] <= 2*tolerance
            )
            numerical_checks[prefix+"_localized_weak_core"] = (
                row["minimum_f"] >= -1e-9 and row["central_amplitude"] > 0.1
                and 0 < row["omega"] < 1 and row["maximum_abs_u"] < 0.1
            )
            numerical_checks[prefix+"_quadrature"] = (
                max(row["same_profile_quadrature_changes"].values()) < 3e-4
            )
            numerical_checks[prefix+"_missing_exterior_energy_rejected"] = (
                relative(row["mass_gauss"],
                         row["energy"]-row["foundation_exterior_tail_energy"])
                > 2e-5
            )
    convergence = {}
    for alpha in ALPHAS:
        low, high = [row for row in records if row["alpha"] == alpha]
        changes = {
            key: relative(low[key], high[key])
            for key in ("energy", "mass_gauss", "omega", "central_p", "charge_rms_radius")
        }
        convergence[str(alpha)] = changes
        numerical_checks[f"refinement_alpha{alpha:g}"] = max(changes.values()) < 3e-4
    hessians = []
    for radius, grids in HESSIAN_GRIDS.items():
        for cells in grids:
            row = radial_hessian(
                solutions[(radius, ALPHAS[-1])], ALPHAS[-1], radius, cells, charge
            )
            hessians.append(row)
            numerical_checks[f"radial_hessian_R{radius:g}_N{cells}"] = (
                row["positive_sampled_fixed_charge_hessian"]
                and max(row["eigen_equation_absolute_residuals"]) < 1e-7
            )
    numerical_checks["protected_W58_unchanged"] = digest(W58) == W58_SHA256
    passed = all(exact.values()) and all(numerical_checks.values())
    stationary_passed = all(exact.values()) and all(
        result for name, result in numerical_checks.items()
        if not name.startswith("radial_hessian_")
    )
    radial_passed = all(
        result for name, result in numerical_checks.items()
        if name.startswith("radial_hessian_")
    )
    return {
        "claim": "NEW_SCALAR_COMPOSITE_METRIC_FINITE_SOURCE_CANDIDATE_V1",
        "passed": passed,
        "status": "FINITE_SOURCE_CANDIDATE_GATE_PASS" if passed else "FROZEN_CANDIDATE_GATE_FAILED",
        "stationary_source_gate_pass": stationary_passed,
        "radial_energy_test_pass": radial_passed,
        "reference": {"omega": 0.8, "radius": 80, "tolerance": 1e-8,
                      "charge": charge, "energy": energy0,
                      "charge_rms_radius": radius0},
        "symbolic_checks": exact, "numerical_checks": numerical_checks,
        "finite_source_records": records, "refinement_changes": convergence,
        "fixed_charge_radial_hessian": hessians,
        "scope": {
            "new_gravitational_response_candidate": True,
            "retained_EH_architecture_replaced": False,
            "EH_equivalence_derived": False,
            "full_PPN_or_tensor_sector_validated": False,
            "nonlinear_stability_proved": False,
            "no_zero_pressure_theorem": False,
            "strong_field_or_singularity_test": False,
            "observational_pass": False,
            "writes_files": False,
        },
        "provenance": {
            "script_sha256": digest(SOURCE),
            "contract_sha256": digest(CONTRACT) if CONTRACT.exists() else None,
            "W58_sha256": digest(W58),
            "python": platform.python_version(), "numpy": np.__version__,
            "scipy": scipy.__version__, "sympy": sp.__version__,
        },
    }


if __name__ == "__main__":
    try:
        report = run()
    except Exception as error:
        report = {"passed": False, "status": "EXECUTION_FAILED",
                  "error_type": type(error).__name__, "error": str(error),
                  "writes_files": False}
    print(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False))
    raise SystemExit(0 if report["passed"] else 1)
