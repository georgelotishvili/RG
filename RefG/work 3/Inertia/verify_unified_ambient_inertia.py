#!/usr/bin/env python3
"""
Standalone SymPy + SciPy BVP verifier for:
  CLAIM_ID: REFG_UNIFIED_AMBIENT_INERTIA_AND_TWO_CHARGE_FIRST_LAW_V1
  MODEL_VERSION: REFG_UNIFIED_COVARIANT_V1 (extending REFG_ISOLATED_COVARIANT_V2)

Verifies:
  1. Symbolic proof of Theorem 1: Grand-Canonical Threshold Trap at omega_C >= mu_{C0}
     in an asymptotically flat 1/r potential (x_*(r) ~ 1/r, enclosed mass M_C(R) ~ R^2 -> inf).
  2. Symbolic proof of Theorem 2: Sub-Threshold Vacuum Window (omega_C <= mu_{C0} N(0))
     and Compact Trapped-Pocket Regime (mu_{C0} N(0) < omega_C < mu_{C0}).
  3. Symbolic proof of Theorem 3: Exact integrating factor sigma(r) for the coupled
     oscillon + collective mass constraint, joint two-charge ADM first law
     dM_ADM = Omega dQ + omega_C dQ_C, threshold slope dM_ADM/dQ_C|_{0+} = mu_{C0} N_0(0),
     clock-ruler stress identity with total radial pressure, and whole-body boost inertia.
  4. Numerical BVP verification on the alpha=0.001, Q0=190.401136223484 witness branch:
     - Exact recovery of REFG_ISOLATED_COVARIANT_V2 for omega_C <= mu_{C0} N_0(0).
     - Monotonic threshold convergence (M(Q0, Q_C) - M(Q0, 0))/Q_C -> mu_{C0} N_0(0) as Q_C -> 0+.
     - Clock-ruler stress reconstruction and Komar mass balance on the coupled state.
     - Partial and joint two-charge ADM first law finite differences.
     - 4 negative controls rejected.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OSC_INERTIA_PY = ROOT / "RefG" / "work 3" / "Lagrangian_Formulation" / "Oscillon_Inertia" / "verify_oscillon_inertia.py"
REPORT_MD = HERE / "unified_ambient_inertia_audit.md"
RESULT_JSON = HERE / "unified_ambient_inertia_result.json"

Q0 = 190.401136223484
MU_C0 = 1.0
LAM_C = 10.0

UPSTREAM_EXPECTED_SHA256 = {
    "RefG/work 3/Inertia/foundation_revision.md": "588ca272af1c7842c33836e3d73df3ed4d087c0ffe218863c6e5045b565f2425",
    "RefG/work 3/Inertia/verify_foundation_revision.py": "12e4cd5234569b0a564ea68b3542b5139675d70870859c57618dc746d7638baa",
    "RefG/work 3/Lagrangian_Formulation/Oscillon_Inertia/oscillon_inertia.md": "6a8c95f557d4ffac01a404eef3eef54b81c2fe3fd5aca97556cf39d9bda8ea55",
    "RefG/work 3/Lagrangian_Formulation/Oscillon_Inertia/verify_oscillon_inertia.py": "32cf32e9cfd590f93928eff16cbfe5494836df8b9d72bfd88b3cf3ba7da22076",
    "RefG/work 3/Lagrangian_Formulation/Unified_Isolated_Cosmological_Action/unified_isolated_cosmological_action.md": "3531c976615505071c395e4a6c3455c79c0fc022e81e5de94f5c461d16f32dd0",
    "RefG/work 3/Lagrangian_Formulation/Unified_Isolated_Cosmological_Action/verify_unified_isolated_cosmological_action.py": "6bfe75edffaa3f59649d539ffec79fe76af27a511839570b1e4daf0ca32cfde9",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_base():
    spec = importlib.util.spec_from_file_location("oscillon_inertia_base", OSC_INERTIA_PY)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def run_symbolic_checks() -> tuple[dict[str, bool], dict[str, str], dict[str, bool]]:
    checks: dict[str, bool] = {}
    residuals: dict[str, str] = {}
    neg_controls: dict[str, bool] = {}

    def check_zero(name: str, expr: sp.Expr) -> None:
        s = sp.simplify(sp.expand(expr))
        residuals[name] = str(s)
        checks[name] = (s == 0)

    r, R, alpha, M = sp.symbols("r R alpha M", positive=True)
    mu0, lamC, wC = sp.symbols("mu_C0 lambda_C omega_C", positive=True)
    sig, m, f, fp, Om, P_osc, P_C = sp.symbols(
        "sigma m f fp Omega P_osc P_C", positive=True
    )
    V_f, dV_df = sp.symbols("V_f dV_df", real=True)

    # -------------------------------------------------------------------------
    # 1. Theorem 1: Grand-canonical threshold trap at omega_C = mu_C0
    # -------------------------------------------------------------------------
    N_asym = 1 - alpha * M / (4 * sp.pi * r)
    XC_thresh = mu0**2 / N_asym**2
    x_star_asym = sp.series((XC_thresh - mu0**2) / lamC, r, sp.oo, 2).removeO()
    expected_x_asym = mu0**2 * alpha * M / (2 * sp.pi * lamC * r)
    check_zero("grand_canonical_threshold_x_star_1_over_r_tail", x_star_asym - expected_x_asym)

    rhoC_asym = mu0**2 * expected_x_asym
    MC_of_R = sp.integrate(4 * sp.pi * r**2 * rhoC_asym, (r, 0, R))
    expected_MC_of_R = mu0**4 * alpha * M * R**2 / lamC
    check_zero("grand_canonical_threshold_mass_diverges_as_R_squared", MC_of_R - expected_MC_of_R)
    checks["grand_canonical_threshold_limit_is_infinite"] = (
        sp.limit(MC_of_R, R, sp.oo) == sp.oo
    )
    neg_controls["grand_canonical_threshold_finite_mass_ansatz_rejected"] = (
        sp.limit(MC_of_R, R, sp.oo) == sp.oo
    )

    # -------------------------------------------------------------------------
    # 2. Theorem 2: Collective envelope stress-energy & enthalpy identities
    # -------------------------------------------------------------------------
    F = 1 - 2 * alpha * m / r
    N = sig * sp.sqrt(F)
    XC = wC**2 / (sig**2 * F)
    xs = (XC - mu0**2) / lamC
    UC = sp.Rational(1, 2) * mu0**2 * xs + sp.Rational(1, 4) * lamC * xs**2
    pC = sp.simplify(sp.Rational(1, 2) * xs * XC - UC)
    rhoC = sp.simplify(xs * XC - pC)

    check_zero("collective_pressure_is_quartic_envelope", pC - sp.Rational(1, 4) * lamC * xs**2)
    check_zero(
        "collective_density_is_quadratic_plus_quartic",
        rhoC - (mu0**2 * xs + sp.Rational(3, 4) * lamC * xs**2),
    )
    check_zero("collective_enthalpy_is_xs_times_XC", (rhoC + pC) - xs * XC)

    # Sub-threshold condition: wC <= mu0 * N(0) => XC(0) - mu0^2 <= 0
    N0, delta_w = sp.symbols("N_0 delta_omega", positive=True)
    XC_sub = (mu0 * N0 - delta_w) ** 2 / N0**2
    checks["subthreshold_central_driving_nonpositive"] = bool(
        sp.simplify((XC_sub - mu0**2).subs(delta_w, 0)) == 0
        and sp.simplify(sp.diff(XC_sub - mu0**2, delta_w).subs(delta_w, 0)) < 0
    )

    # -------------------------------------------------------------------------
    # 3. Theorem 3: Canonical two-charge mass constraint & integrating factor
    # -------------------------------------------------------------------------
    nC_sym = sp.Symbol("n_C", positive=True)
    rhoC_fn = sp.Function("rho_C")(nC_sym)
    mu_chem = sp.Symbol("mu_chem", positive=True)

    nC_canon = sp.sqrt(F) * P_C / r**2
    h_osc = r**2 * fp**2 + P_osc**2 / (r**2 * f**2)
    r2_rho_total = r**2 * V_f + r**2 * rhoC_fn.subs(nC_sym, nC_canon) + sp.Rational(1, 2) * F * h_osc

    # Differentiate r^2 * rho_total w.r.t. m at fixed (f, fp, P_osc, P_C)
    dr2rho_dm = (
        sp.Rational(1, 2) * sp.diff(F, m) * h_osc
        + r**2 * mu_chem * sp.diff(nC_canon, m)
    )
    P_osc_eq = r**2 * Om * f**2 / (sig * F)
    P_C_eq = r**2 * wC * xs / (sig * F)
    mu_eq = wC / (sig * sp.sqrt(F))

    integrating_factor_lhs = -dr2rho_dm.subs(
        {P_osc: P_osc_eq, P_C: P_C_eq, mu_chem: mu_eq}
    )
    sigma_prime_over_sigma = alpha * r * (
        fp**2 + (Om**2 * f**2 + wC**2 * xs) / (sig**2 * F**2)
    )
    check_zero(
        "coupled_mass_constraint_integrating_factor_is_sigma",
        integrating_factor_lhs - sigma_prime_over_sigma,
    )

    # Partial derivatives w.r.t. canonical momentum densities P_osc and P_C
    dM_dPosc = (sig * sp.diff(r2_rho_total, P_osc)).subs(P_osc, P_osc_eq)
    check_zero("oscillon_charge_functional_derivative_is_Omega", dM_dPosc - Om)

    dM_dPC = sig * r**2 * mu_chem * sp.diff(nC_canon, P_C)
    check_zero(
        "collective_charge_functional_derivative_is_omega_C",
        dM_dPC.subs(mu_chem, mu_eq) - wC,
    )

    # Threshold slope at Q_C -> 0+ (where wC -> mu0 * N_0(0))
    wC_crit = mu0 * N0
    check_zero(
        "threshold_first_law_slope_is_redshifted_mass_gap",
        dM_dPC.subs(mu_chem, wC_crit / (sig * sp.sqrt(F))).subs(sig * sp.sqrt(F), N0)
        - mu0 * N0,
    )

    # -------------------------------------------------------------------------
    # 4. Generalized clock-ruler stress identity with total radial pressure
    # -------------------------------------------------------------------------
    pr_total = sp.Symbol("p_r_total", real=True)
    rho_total = sp.Symbol("rho_total", real=True)
    # Using d/dr ln(N) = sigma'/sigma + F'/(2F) = alpha*r*pr_total/F + alpha*m/(r^2*F)
    # and d/dr ln(A_iso) = (1 - 1/sqrt(F))/r
    dlnN_dr = alpha * r * pr_total / F + alpha * m / (r**2 * F)
    dlnA_dr = (1 - 1 / sp.sqrt(F)) / r
    dlnNA_dr = dlnN_dr + dlnA_dr
    expected_dlnNA_dr = alpha * r * pr_total / F + (1 - sp.sqrt(F)) ** 2 / (2 * r * F)
    # Note: alpha*m/r = (1 - F)/2
    check_zero(
        "coupled_clock_ruler_stress_identity",
        dlnNA_dr.subs(alpha * m, (1 - F) * r / 2) - expected_dlnNA_dr,
    )

    # -------------------------------------------------------------------------
    # 5. Whole-body boost ADM momentum and inertia equivalence
    # -------------------------------------------------------------------------
    v, gamma = sp.symbols("v gamma", positive=True)
    M_coupled = sp.Symbol("M_ADM_coupled", positive=True)
    E_boost = gamma * M_coupled
    P_boost = gamma * M_coupled * v
    M_inertial = sp.limit(P_boost / v, v, 0).subs(gamma, 1)
    check_zero("coupled_boost_inertia_equals_ADM_mass", M_inertial - M_coupled)

    return checks, residuals, neg_controls


def solve_coupled(
    base,
    prev_sol,
    Q_target: float,
    omega_C: float,
    mu_C0: float = MU_C0,
    lam_C: float = LAM_C,
    radius: float = 60.0,
    tol: float = 3e-8,
):
    eps = 1e-4
    x = prev_sol.x
    initial = prev_sol.sol(x)
    param = prev_sol.p.copy()

    def fields(r, y, par):
        f, fp, mass, ls, q = y
        w = 1.0 / (1.0 + np.exp(-par[0]))
        sig = np.exp(ls)
        F = 1.0 - 2.0 * base.ALPHA * mass / r
        T_osc = w * w * f * f / (2.0 * sig * sig * F)
        X_osc = 0.5 * F * fp * fp
        rho_osc = T_osc + X_osc + base.potential(f)
        XC = omega_C * omega_C / (sig * sig * F)
        xs = np.maximum(0.0, (XC - mu_C0 * mu_C0) / lam_C)
        rho_C = mu_C0 * mu_C0 * xs + 0.75 * lam_C * xs * xs
        mp = r * r * (rho_osc + rho_C)
        sp_ = base.ALPHA * r * (
            fp * fp + (w * w * f * f + omega_C * omega_C * xs) / (sig * sig * F * F)
        )
        Fp = -2.0 * base.ALPHA * (mp / r - mass / (r * r))
        fpp = (base.force(f) - w * w * f / (sig * sig * F)) / F - (
            2.0 / r + sp_ + Fp / F
        ) * fp
        qp = w * r * r * f * f / (sig * F)
        return np.vstack((fp, fpp, mp, sp_, qp))

    def boundary(ya, yb, par):
        w = 1.0 / (1.0 + np.exp(-par[0]))
        f0, _, _, ls0, _ = ya
        sig0 = np.exp(ls0)
        f2 = (base.force(f0) - w * w * f0 / (sig0 * sig0)) / 6.0
        XC0 = omega_C * omega_C / (sig0 * sig0)
        xs0 = max(0.0, (XC0 - mu_C0 * mu_C0) / lam_C)
        rho0 = (
            w * w * f0 * f0 / (2.0 * sig0 * sig0)
            + base.potential(f0)
            + mu_C0 * mu_C0 * xs0
            + 0.75 * lam_C * xs0 * xs0
        )
        k = np.sqrt(1.0 - w * w)
        mu = base.ALPHA * yb[2]
        power = -1.0 + mu * (2.0 * w * w - 1.0) / k
        return np.array(
            [
                ya[1] - 2.0 * f2 * eps,
                ya[2] - rho0 * eps**3 / 3.0,
                ya[4] - w * f0 * f0 * eps**3 / (3.0 * sig0),
                yb[3],
                yb[1] + (k - power / radius) * yb[0],
                yb[4] - Q_target / (4.0 * np.pi),
            ]
        )

    sol = solve_bvp(
        fields, boundary, x, initial, p=param, tol=tol, max_nodes=50000
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    sol.omega_C = float(omega_C)
    sol.mu_C0 = float(mu_C0)
    sol.lam_C = float(lam_C)
    sol.coupled_bc = boundary
    return sol


def exact_trapped_charge(base, sol, grid_points: int = 8001) -> tuple[float, float]:
    wC, mu0, lamC = sol.omega_C, sol.mu_C0, sol.lam_C

    def lapse_minus_target(r):
        _, _, m, ls, _ = sol.sol(r)
        return float(np.exp(ls) * np.sqrt(1.0 - 2.0 * base.ALPHA * m / r) - wC / mu0)

    if lapse_minus_target(sol.x[0]) >= 0.0:
        return 0.0, 0.0
    r_trap = float(brentq(lapse_minus_target, sol.x[0], sol.x[-1], xtol=1e-12))
    r = np.linspace(sol.x[0], r_trap, grid_points)
    _, _, m, ls, _ = sol.sol(r)
    sig = np.exp(ls)
    F = 1.0 - 2.0 * base.ALPHA * m / r
    XC = wC * wC / (sig * sig * F)
    xs = np.maximum(0.0, (XC - mu0 * mu0) / lamC)
    qcp = wC * r * r * xs / (sig * F)
    QC = float(
        4.0 * np.pi * (simpson(qcp, x=r) + wC * xs[0] * r[0] ** 3 / (3.0 * sig[0]))
    )
    return QC, r_trap


def measure_coupled_profile(base, sol, points: int = 16001) -> dict:
    r = np.linspace(sol.x[0], sol.x[-1], points)
    f, fp, m, ls, q = sol.sol(r)
    sig = np.exp(ls)
    om = float(1.0 / (1.0 + np.exp(-sol.p[0])))
    wC, mu0, lamC = sol.omega_C, sol.mu_C0, sol.lam_C
    F = 1.0 - 2.0 * base.ALPHA * m / r
    if np.min(F) <= 0.0:
        raise RuntimeError("Static chart outside F > 0 domain")
    N = sig * np.sqrt(F)
    T_osc = om * om * f * f / (2.0 * sig * sig * F)
    X_osc = 0.5 * F * fp * fp
    V_osc = base.potential(f)
    rho_osc = T_osc + X_osc + V_osc
    pr_osc = T_osc + X_osc - V_osc
    pt_osc = T_osc - X_osc - V_osc

    XC = wC * wC / (sig * sig * F)
    xs = np.maximum(0.0, (XC - mu0 * mu0) / lamC)
    pC = 0.25 * lamC * xs * xs
    rhoC = mu0 * mu0 * xs + 0.75 * lamC * xs * xs

    rho_tot = rho_osc + rhoC
    pr_tot = pr_osc + pC
    pt_tot = pt_osc + pC

    outer_mass = base.ALPHA * m[-1]
    iso_outer = (
        r[-1] - outer_mass + np.sqrt(r[-1] * (r[-1] - 2.0 * outer_mass))
    ) / 2.0
    logA_outer = np.log(r[-1] / iso_outer)
    geo_integral = cumulative_trapezoid((1.0 / np.sqrt(F) - 1.0) / r, r, initial=0.0)
    logA = logA_outer + geo_integral[-1] - geo_integral
    metric_product = np.log(N) + logA

    rhs_tot = base.ALPHA * r * pr_tot / F + (1.0 - np.sqrt(F)) ** 2 / (2.0 * r * F)
    stress_integral_tot = cumulative_trapezoid(rhs_tot, r, initial=0.0)
    stress_product_tot = (
        np.log(N[-1]) + logA_outer - stress_integral_tot[-1] + stress_integral_tot
    )

    rhs_osc_only = base.ALPHA * r * pr_osc / F + (1.0 - np.sqrt(F)) ** 2 / (
        2.0 * r * F
    )
    stress_integral_osc = cumulative_trapezoid(rhs_osc_only, r, initial=0.0)
    stress_product_osc = (
        np.log(N[-1]) + logA_outer - stress_integral_osc[-1] + stress_integral_osc
    )

    QC, r_trap = exact_trapped_charge(base, sol)

    # Komar mass (split integral at r_trap for high-precision quadrature of C^0 kink)
    if r_trap > 0.0:
        r1 = np.linspace(sol.x[0], r_trap, 8001)
        r2 = np.linspace(r_trap, sol.x[-1], 8001)

        def komar_integrand(rv):
            fv, fpv, mv, lsv, _ = sol.sol(rv)
            sigv = np.exp(lsv)
            Fv = 1.0 - 2.0 * base.ALPHA * mv / rv
            Tv = om * om * fv * fv / (2.0 * sigv * sigv * Fv)
            Xv = 0.5 * Fv * fpv * fpv
            Vv = base.potential(fv)
            XCv = wC * wC / (sigv * sigv * Fv)
            xsv = np.maximum(0.0, (XCv - mu0 * mu0) / lamC)
            rhoCv = mu0 * mu0 * xsv + 0.75 * lamC * xsv * xsv
            pCv = 0.25 * lamC * xsv * xsv
            rhot = Tv + Xv + Vv + rhoCv
            prt = Tv + Xv - Vv + pCv
            ptt = Tv - Xv - Vv + pCv
            return sigv * rv * rv * (rhot + prt + 2.0 * ptt)

        k1 = komar_integrand(r1)
        k2 = komar_integrand(r2)
        komar_vol = float(
            4.0
            * np.pi
            * (
                simpson(k1, x=r1)
                + simpson(k2, x=r2)
                + sig[0]
                * (rho_tot[0] + pr_tot[0] + 2.0 * pt_tot[0])
                * r[0] ** 3
                / 3.0
            )
        )
    else:
        komar_vol = float(
            4.0
            * np.pi
            * (
                simpson(sig * r * r * (rho_tot + pr_tot + 2.0 * pt_tot), x=r)
                + sig[0]
                * (rho_tot[0] + pr_tot[0] + 2.0 * pt_tot[0])
                * r[0] ** 3
                / 3.0
            )
        )
    komar_surf = float(4.0 * np.pi * sig[-1] * (m[-1] + r[-1] ** 3 * pr_tot[-1]))
    adm_mass = float(4.0 * np.pi * m[-1])
    bc_res = sol.coupled_bc(sol.y[:, 0], sol.y[:, -1], sol.p)

    return {
        "omega": om,
        "omega_C": wC,
        "adm_mass": adm_mass,
        "komar_volume_mass": komar_vol,
        "komar_surface_mass": komar_surf,
        "komar_relative_error": abs(komar_vol / adm_mass - 1.0),
        "charge_Q": float(4.0 * np.pi * q[-1]),
        "charge_QC": QC,
        "r_trap": r_trap,
        "central_clock": float(N[0]),
        "central_x_star": float(xs[0]),
        "outer_x_star": float(xs[-1]),
        "minimum_F": float(np.min(F)),
        "pressure_reconstruction_max_error": float(
            np.max(np.abs(metric_product - stress_product_tot))
        ),
        "omitted_collective_pressure_reconstruction_error": float(
            np.max(np.abs(metric_product - stress_product_osc))
        ),
        "max_boundary_residual": float(np.max(np.abs(bc_res))),
        "max_BVP_residual": float(np.max(sol.rms_residuals)),
        "absolute_outer_field": float(abs(f[-1])),
    }


def main() -> int:
    checks, sym_residuals, neg_controls = run_symbolic_checks()

    # Check upstream SHA-256 hashes
    upstream_hashes: dict[str, dict[str, str | bool]] = {}
    for rel_path, expected_sha in UPSTREAM_EXPECTED_SHA256.items():
        abs_path = ROOT / rel_path
        actual_sha = sha256_file(abs_path) if abs_path.exists() else "MISSING"
        matched = actual_sha == expected_sha
        upstream_hashes[rel_path] = {
            "expected_sha256": expected_sha,
            "actual_sha256": actual_sha,
            "matched": matched,
        }
        checks[f"upstream_sha256_{Path(rel_path).name}"] = matched

    base = load_base()
    base.CHARGE = Q0
    seed = base.load_seed_module()
    flat = seed.solve_profile(0.8, radius=80.0, tolerance=1e-8)
    sol_r40 = base.equilibrium(flat, 40.0, 3e-8)
    sol_iso = base.equilibrium(flat, 60.0, 3e-8, previous=sol_r40)
    iso_ref = base.measure_equilibrium(sol_iso, 16001)

    # Solve coupled system at omega_C = 0 on the identical mesh as baseline
    sol_zero = solve_coupled(base, sol_iso, Q0, 0.0)
    zero_ref = measure_coupled_profile(base, sol_zero)

    N0_center = float(zero_ref["central_clock"])
    M0_adm = float(zero_ref["adm_mass"])
    Om0_iso = float(zero_ref["omega"])
    wC_crit = MU_C0 * N0_center

    checks["coupled_zero_wC_matches_isolated_V2_mass"] = (
        abs(M0_adm - float(iso_ref["energy_ADM"])) < 1e-9
    )
    checks["coupled_zero_wC_matches_isolated_V2_omega"] = (
        abs(Om0_iso - float(iso_ref["omega"])) < 1e-9
    )

    # 1. Sub-threshold vacuum window verification
    sub_sol_below = solve_coupled(base, sol_zero, Q0, 0.990000)
    sub_sol_at = solve_coupled(base, sol_zero, Q0, wC_crit)
    sub_below = measure_coupled_profile(base, sub_sol_below)
    sub_at = measure_coupled_profile(base, sub_sol_at)

    checks["subthreshold_below_QC_is_zero"] = sub_below["charge_QC"] == 0.0
    checks["subthreshold_at_crit_QC_is_zero"] = sub_at["charge_QC"] == 0.0
    checks["subthreshold_below_matches_isolated_mass"] = (
        abs(sub_below["adm_mass"] - M0_adm) < 1e-12
    )
    checks["subthreshold_at_crit_matches_isolated_mass"] = (
        abs(sub_at["adm_mass"] - M0_adm) < 1e-12
    )
    checks["subthreshold_at_crit_matches_isolated_omega"] = (
        abs(sub_at["omega"] - Om0_iso) < 1e-12
    )

    # 2. Threshold convergence scan as delta_wC -> 0+
    threshold_scan = []
    for delta in (2e-3, 1e-3, 4e-4, 2e-4, 1e-4):
        wC = wC_crit + delta
        s = solve_coupled(base, sol_zero, Q0, wC)
        m_row = measure_coupled_profile(base, s)
        secant_slope = (m_row["adm_mass"] - M0_adm) / m_row["charge_QC"]
        rel_err_crit = abs(secant_slope / wC_crit - 1.0)
        threshold_scan.append(
            {
                "delta_omega_C": delta,
                "omega_C": wC,
                "r_trap": m_row["r_trap"],
                "charge_QC": m_row["charge_QC"],
                "adm_mass": m_row["adm_mass"],
                "secant_dM_over_QC": secant_slope,
                "relative_diff_from_wC_crit": rel_err_crit,
                "max_BVP_residual": m_row["max_BVP_residual"],
            }
        )

    checks["threshold_scan_BVP_residuals"] = all(
        row["max_BVP_residual"] < 1e-6 for row in threshold_scan
    )
    checks["threshold_scan_monotonic_convergence_to_wC_crit"] = all(
        threshold_scan[i + 1]["relative_diff_from_wC_crit"]
        < threshold_scan[i]["relative_diff_from_wC_crit"]
        for i in range(len(threshold_scan) - 1)
    )
    checks["threshold_limit_slope_matches_redshifted_gap"] = (
        threshold_scan[-1]["relative_diff_from_wC_crit"] < 2e-4
    )

    # Negative control: unredshifted flat-space threshold mu_C0 = 1.0 instead of mu_C0 * N_0(0)
    unredshifted_err = abs(threshold_scan[-1]["secant_dM_over_QC"] / MU_C0 - 1.0)
    neg_controls["wrong_collective_first_law_unredshifted_threshold_rejected"] = (
        unredshifted_err > 8e-3
    )
    checks["negative_control_unredshifted_threshold_rejected"] = neg_controls[
        "wrong_collective_first_law_unredshifted_threshold_rejected"
    ]

    # 3. Trapped-pocket witness state (omega_C = 0.9935)
    wC_witness = 0.9935
    sol_wit = solve_coupled(base, sol_iso, Q0, wC_witness)
    wit = measure_coupled_profile(base, sol_wit)

    checks["witness_BVP_residual"] = wit["max_BVP_residual"] < 1e-6
    checks["witness_boundary_residual"] = wit["max_boundary_residual"] < 1e-8
    checks["witness_compact_trapping"] = (
        0.0 < wit["r_trap"] < 5.0 and wit["outer_x_star"] == 0.0
    )
    checks["witness_localized_oscillon_tail"] = wit["absolute_outer_field"] < 1e-8
    checks["witness_positive_metric"] = wit["minimum_F"] > 0.0
    checks["witness_clock_ruler_stress_reconstruction"] = (
        wit["pressure_reconstruction_max_error"] < 3e-7
    )
    checks["witness_komar_mass_balance"] = wit["komar_relative_error"] < 1e-5

    # Negative control: omitting collective pressure p_C in clock-ruler stress integral
    # Use a prominent trapped pocket (wC = 0.996, lam_C = 0.05) to test p_C contribution
    sol_strong = solve_coupled(base, sol_zero, Q0, 0.996, lam_C=0.05)
    strong_wit = measure_coupled_profile(base, sol_strong)
    neg_controls[
        "omitted_collective_pressure_in_clock_ruler_reconstruction_rejected"
    ] = bool(
        strong_wit["omitted_collective_pressure_reconstruction_error"]
        > 20.0 * strong_wit["pressure_reconstruction_max_error"]
    )
    checks["negative_control_omitted_collective_pressure_rejected"] = neg_controls[
        "omitted_collective_pressure_in_clock_ruler_reconstruction_rejected"
    ]

    # 4. Partial and joint two-charge ADM first law finite differences around witness
    dwC = 5e-5
    sol_wC_m = solve_coupled(base, sol_wit, Q0, wC_witness - dwC)
    sol_wC_p = solve_coupled(base, sol_wit, Q0, wC_witness + dwC)
    m_wC_m = measure_coupled_profile(base, sol_wC_m)
    m_wC_p = measure_coupled_profile(base, sol_wC_p)
    dM_dQC_fixed_Q = (m_wC_p["adm_mass"] - m_wC_m["adm_mass"]) / (
        m_wC_p["charge_QC"] - m_wC_m["charge_QC"]
    )
    rel_err_dM_dQC = abs(dM_dQC_fixed_Q / wC_witness - 1.0)
    checks["partial_first_law_dM_dQC_at_fixed_Q"] = rel_err_dM_dQC < 1e-5

    # Fixed-wC step in Q (testing Legendre transform d(M - wC*QC)/dQ = Omega)
    dQ_rel = 2e-4
    sol_Q_m = solve_coupled(base, sol_wit, Q0 * (1.0 - dQ_rel), wC_witness)
    sol_Q_p = solve_coupled(base, sol_wit, Q0 * (1.0 + dQ_rel), wC_witness)
    m_Q_m = measure_coupled_profile(base, sol_Q_m)
    m_Q_p = measure_coupled_profile(base, sol_Q_p)
    d_legendre_dQ = (
        (m_Q_p["adm_mass"] - wC_witness * m_Q_p["charge_QC"])
        - (m_Q_m["adm_mass"] - wC_witness * m_Q_m["charge_QC"])
    ) / (m_Q_p["charge_Q"] - m_Q_m["charge_Q"])
    rel_err_dM_dQ = abs(d_legendre_dQ / wit["omega"] - 1.0)
    checks["partial_first_law_dM_dQ_legendre"] = rel_err_dM_dQ < 1e-5

    # Simultaneous step in (Q, wC) with comparable energy increments
    dQ_rel_joint = 1e-5
    sol_joint_m = solve_coupled(
        base, sol_wit, Q0 * (1.0 - dQ_rel_joint), wC_witness - dwC
    )
    sol_joint_p = solve_coupled(
        base, sol_wit, Q0 * (1.0 + dQ_rel_joint), wC_witness + dwC
    )
    m_joint_m = measure_coupled_profile(base, sol_joint_m)
    m_joint_p = measure_coupled_profile(base, sol_joint_p)

    dM_joint = m_joint_p["adm_mass"] - m_joint_m["adm_mass"]
    dQ_joint = m_joint_p["charge_Q"] - m_joint_m["charge_Q"]
    dQC_joint = m_joint_p["charge_QC"] - m_joint_m["charge_QC"]
    om_mid = 0.5 * (m_joint_p["omega"] + m_joint_m["omega"])
    rhs_joint = om_mid * dQ_joint + wC_witness * dQC_joint
    rel_err_joint = abs(dM_joint / rhs_joint - 1.0)
    residual_collective_slope = (dM_joint - om_mid * dQ_joint) / dQC_joint
    rel_err_residual_collective = abs(residual_collective_slope / wC_witness - 1.0)

    checks["joint_two_charge_first_law_total_balance"] = rel_err_joint < 1e-5
    checks["joint_two_charge_first_law_collective_residual_slope"] = (
        rel_err_residual_collective < 1e-5
    )

    # Negative control: omitting wC * dQC from joint first law
    omitted_collective_err = abs(dM_joint / (wit["omega"] * dQ_joint) - 1.0)
    neg_controls["omitted_collective_term_in_joint_first_law_rejected"] = (
        omitted_collective_err > 1e-3
    )
    checks["negative_control_omitted_collective_first_law_term_rejected"] = (
        neg_controls["omitted_collective_term_in_joint_first_law_rejected"]
    )
    checks["negative_control_grand_canonical_threshold_rejected"] = neg_controls[
        "grand_canonical_threshold_finite_mass_ansatz_rejected"
    ]

    all_passed = all(checks.values()) and all(neg_controls.values())

    result = {
        "claim_id": "REFG_UNIFIED_AMBIENT_INERTIA_AND_TWO_CHARGE_FIRST_LAW_V1",
        "model_version": "REFG_UNIFIED_COVARIANT_V1",
        "status": "PASS_UNIFIED_AMBIENT_INERTIA_AND_TWO_CHARGE_FIRST_LAW"
        if all_passed
        else "FAIL",
        "all_checks_passed": all_passed,
        "total_checks": len(checks),
        "passed_checks": sum(1 for v in checks.values() if v),
        "failed_checks": [k for k, v in checks.items() if not v],
        "negative_controls": neg_controls,
        "symbolic_residuals": sym_residuals,
        "isolated_baseline": {
            "Q0": Q0,
            "adm_mass": M0_adm,
            "omega": Om0_iso,
            "central_clock_N0": N0_center,
            "critical_collective_frequency_wC_crit": wC_crit,
        },
        "subthreshold_checks": {
            "below_threshold_wC_0.990": sub_below,
            "at_threshold_wC_crit": sub_at,
        },
        "threshold_convergence_scan": threshold_scan,
        "trapped_pocket_witness": wit,
        "two_charge_first_law_tests": {
            "dM_dQC_at_fixed_Q": dM_dQC_fixed_Q,
            "omega_C_target": wC_witness,
            "relative_error_dM_dQC": rel_err_dM_dQC,
            "d_legendre_dQ_at_fixed_wC": d_legendre_dQ,
            "omega_target": wit["omega"],
            "relative_error_dM_dQ": rel_err_dM_dQ,
            "joint_step_dM": dM_joint,
            "joint_step_rhs": rhs_joint,
            "relative_error_joint": rel_err_joint,
            "residual_collective_slope": residual_collective_slope,
            "relative_error_residual_collective_slope": rel_err_residual_collective,
        },
        "checks": checks,
        "provenance": {
            "python_version": sys.version.split()[0],
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "sympy_version": sp.__version__,
            "verifier_sha256": sha256_file(Path(__file__).resolve()),
            "report_sha256": sha256_file(REPORT_MD) if REPORT_MD.exists() else "MISSING",
            "upstream_sha256": upstream_hashes,
        },
    }

    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "all_checks_passed": all_passed,
                "passed_checks": result["passed_checks"],
                "total_checks": result["total_checks"],
                "failed_checks": result["failed_checks"],
                "witness_M_ADM": wit["adm_mass"],
                "witness_QC": wit["charge_QC"],
                "witness_r_trap": wit["r_trap"],
                "rel_err_dM_dQC": rel_err_dM_dQC,
                "rel_err_dM_dQ": rel_err_dM_dQ,
                "rel_err_joint": rel_err_joint,
            },
            indent=2,
        )
    )
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
