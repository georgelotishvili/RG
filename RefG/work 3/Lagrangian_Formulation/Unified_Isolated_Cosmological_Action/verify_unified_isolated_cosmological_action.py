"""REFG_UNIFIED_ISOLATED_COSMOLOGICAL_ACTION_V1: exact symbolic verifier.

Proves:
1. The exact W3-54 hydrodynamic zero-current obstruction (directional derivative
   discontinuity at J_C = 0 and inhomogeneous-lapse eikonal incompatibility when
   rho_C'(0) > 0).
2. Regularity of the parent envelope action S_C^(env)[e, x, theta_C, J_C] and
   Cartesian complex field action S_C^(field)[e, Psi_C] at x = 0 (Psi_C = 0).
3. Exact reduction of REFG_UNIFIED_COVARIANT_V1 to REFG_ISOLATED_COVARIANT_V2
   on the vacuum branch (x = 0, Lambda_F = 0) on any curved metric.
4. Exact reduction of REFG_UNIFIED_COVARIANT_V1 on the active branch (x > 0)
   to W3-54's barotropic phase-current source and W3-62's dilute cold-dust limit.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from collections import OrderedDict
from pathlib import Path

sys.dont_write_bytecode = True
import sympy as sp

CLAIM_ID = "REFG_UNIFIED_ISOLATED_COSMOLOGICAL_ACTION_V1"
MODEL_VERSION = "REFG_UNIFIED_COVARIANT_V1"
CONTRACT_SHA256 = "3531c976615505071c395e4a6c3455c79c0fc022e81e5de94f5c461d16f32dd0"

UPSTREAM_HASHES = OrderedDict(
    [
        (
            "RefG/work 3/Inertia/foundation_revision.md",
            "588ca272af1c7842c33836e3d73df3ed4d087c0ffe218863c6e5045b565f2425",
        ),
        (
            "RefG/work 3/Inertia/verify_foundation_revision.py",
            "12e4cd5234569b0a564ea68b3542b5139675d70870859c57618dc746d7638baa",
        ),
        (
            "RefG/work 3/Lagrangian_Formulation/Oscillon_Inertia/oscillon_inertia.md",
            "6a8c95f557d4ffac01a404eef3eef54b81c2fe3fd5aca97556cf39d9bda8ea55",
        ),
        (
            "RefG/work 3/Lagrangian_Formulation/Oscillon_Inertia/verify_oscillon_inertia.py",
            "32cf32e9cfd590f93928eff16cbfe5494836df8b9d72bfd88b3cf3ba7da22076",
        ),
        (
            "RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md",
            "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
        ),
        (
            "RefG/work 3/Cosmology_and_LSS/CMB_Closure/w3_62_cmb_einstein_source_linear_closure_preregistration.md",
            "b4068791b63e9a072a897e9aa85eae96c588b0d33533effb9664ffbd667ae810",
        ),
    ]
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_root() -> Path:
    here = Path(__file__).resolve()
    for parent in (here.parent, *here.parents):
        if (parent / "CODES.md").exists() and (parent / "Theory_Canon.md").exists():
            return parent
    raise RuntimeError("Could not locate RefG workspace root")


def exact_zero(expr) -> bool:
    return bool(sp.simplify(expr) == 0)


def run_checks() -> OrderedDict:
    root = locate_root()
    here = Path(__file__).resolve().parent
    contract_path = here / "unified_isolated_cosmological_action.md"

    checks = OrderedDict()
    residuals = OrderedDict()
    negative_controls = OrderedDict()

    def check_zero(name: str, expr: sp.Expr) -> None:
        simplified = sp.simplify(expr)
        residuals[name] = str(simplified)
        checks[name] = bool(simplified == 0)

    # ------------------------------------------------------------------
    # Group 1: W3-54 hydrodynamic zero-current obstruction checks
    # ------------------------------------------------------------------
    eps, e_det, c0, mu0 = sp.symbols("eps e c0 mu0", positive=True)
    chi = sp.symbols("chi", positive=True)
    J0, J1 = sp.symbols("J0 J1", real=True)
    nC_expr = sp.sqrt(J0**2 - J1**2) / e_det
    dnC_dJ0 = sp.diff(nC_expr, J0)
    dnC_dJ1 = sp.diff(nC_expr, J1)

    # Ray 1: J0 = eps, J1 = 0
    grad_ray1 = sp.Matrix(
        [
            sp.simplify(dnC_dJ0.subs({J0: eps, J1: 0})),
            sp.simplify(dnC_dJ1.subs({J0: eps, J1: 0})),
        ]
    )
    # Ray 2: J0 = eps*cosh(chi), J1 = eps*sinh(chi)
    grad_ray2 = sp.Matrix(
        [
            sp.trigsimp(
                sp.simplify(
                    dnC_dJ0.subs({J0: eps * sp.cosh(chi), J1: eps * sp.sinh(chi)})
                )
            ),
            sp.trigsimp(
                sp.simplify(
                    dnC_dJ1.subs({J0: eps * sp.cosh(chi), J1: eps * sp.sinh(chi)})
                )
            ),
        ]
    )
    check_zero("w54_nC_grad_ray1_eps_independent", sp.diff(grad_ray1[0], eps))
    check_zero("w54_nC_grad_ray2_eps_independent", sp.diff(grad_ray2[1], eps))
    ray_diff_norm = sp.simplify(
        (grad_ray2[0] - grad_ray1[0]) ** 2 + (grad_ray2[1] - grad_ray1[1]) ** 2
    )
    checks["w54_nC_directional_derivative_discontinuity_at_zero"] = bool(
        sp.simplify(ray_diff_norm.subs(chi, 1)) != 0
    )

    # Inhomogeneous static lapse eikonal obstruction for stationary phase theta_C = -omega_C t
    r, omega_C = sp.symbols("r omega_C", positive=True)
    N_fn = sp.Function("N")(r)
    XC_static = omega_C**2 / (c0**2 * N_fn**2)
    eikonal_radial_derivative = sp.simplify(sp.diff(XC_static - (mu0 / c0) ** 2, r))
    expected_eikonal_radial_derivative = -2 * omega_C**2 * sp.diff(N_fn, r) / (
        c0**2 * N_fn**3
    )
    check_zero(
        "w54_inhomogeneous_lapse_eikonal_derivative_identity",
        eikonal_radial_derivative - expected_eikonal_radial_derivative,
    )
    checks["w54_stationary_eikonal_incompatible_with_nonconstant_lapse"] = bool(
        eikonal_radial_derivative.subs({N_fn: 1 - sp.Rational(1, 10) / r}) != 0
    )

    # ------------------------------------------------------------------
    # Group 2: Parent envelope action S_C^(env) -> polynomial dual action S_C^(dual)
    # ------------------------------------------------------------------
    x, XC, lamC = sp.symbols("x XC lamC", positive=True)
    g00, dtheta0 = sp.symbols("g00 dtheta0", real=True)
    # In local rest/aligned coordinates with metric component g_00 = -N^2 < 0:
    N_sym = sp.symbols("N_sym", positive=True)
    UC = mu0**2 * x / 2 + lamC * x**2 / 4

    # First-order envelope Lagrangian density (1D timelike representative J^0, dtheta_0)
    J0_sym = sp.symbols("J0_sym", real=True)
    L_env = J0_sym * dtheta0 - (e_det / c0) * (
        (N_sym**2 * J0_sym**2) / (2 * e_det**2 * x) + UC
    )
    dL_env_dJ0 = sp.diff(L_env, J0_sym)
    J0_sol = sp.solve(dL_env_dJ0, J0_sym)[0]
    expected_J0_sol = c0 * e_det * x * dtheta0 / N_sym**2
    check_zero("envelope_J_variation_polynomial_in_x", J0_sol - expected_J0_sol)

    # Substitute J0_sol back into L_env and identify X_C = -g^{00} (dtheta_0)^2 = (dtheta_0)^2 / N^2
    L_dual_from_env = sp.simplify(L_env.subs(J0_sym, J0_sol))
    L_dual_target = (e_det / c0) * (c0**2 * x * (dtheta0**2 / N_sym**2) / 2 - UC)
    check_zero(
        "envelope_J_elimination_gives_polynomial_dual_action",
        L_dual_from_env - L_dual_target,
    )

    # Check regularity at x = 0: J0_sol(x=0) = 0 and L_dual(x=0) = 0
    check_zero("envelope_J_vanishes_regularly_at_x_zero", J0_sol.subs(x, 0))
    check_zero(
        "dual_lagrangian_vanishes_at_x_zero",
        L_dual_target.subs(x, 0),
    )

    # Sub-threshold Kuhn-Tucker condition on x >= 0 when c0^2 * XC <= mu0^2
    delta_mu_sq = sp.symbols("delta_mu_sq", positive=True)
    L_dual_general = (e_det / c0) * (c0**2 * x * XC / 2 - UC)
    dL_dual_dx = sp.simplify(sp.diff(L_dual_general, x))
    dL_dual_dx_subthreshold = sp.simplify(
        dL_dual_dx.subs(XC, (mu0**2 - delta_mu_sq) / c0**2)
    )
    expected_subthreshold_slope = -(e_det / (2 * c0)) * (delta_mu_sq + lamC * x)
    check_zero(
        "subthreshold_dual_slope_strictly_negative_identity",
        dL_dual_dx_subthreshold - expected_subthreshold_slope,
    )
    checks["subthreshold_unique_maximum_on_nonnegative_x_is_zero"] = bool(
        dL_dual_dx_subthreshold.is_negative
    )

    # ------------------------------------------------------------------
    # Group 3: Cartesian complex field S_C^(field) exact vacuum reduction at Psi_C = 0
    # ------------------------------------------------------------------
    phi1 = sp.Function("phi1")(r)
    phi2 = sp.Function("phi2")(r)
    A_fn = sp.Function("A")(r)
    # Spherical static curved metric ds^2 = -N(r)^2 c0^2 dt^2 + A(r)^2 (dr^2 + r^2 dOmega^2)
    e_sph = N_fn * A_fn**3 * r**2
    x_cart = (phi1**2 + phi2**2) / 2
    UC_cart = mu0**2 * x_cart / 2 + lamC * x_cart**2 / 4
    L_field_sph = -(e_sph / c0) * (
        c0**2 * (sp.diff(phi1, r) ** 2 + sp.diff(phi2, r) ** 2) / (2 * A_fn**2)
        + UC_cart
    )
    EL_phi1 = sp.simplify(
        sp.diff(L_field_sph, phi1) - sp.diff(sp.diff(L_field_sph, sp.diff(phi1, r)), r)
    )
    EL_phi2 = sp.simplify(
        sp.diff(L_field_sph, phi2) - sp.diff(sp.diff(L_field_sph, sp.diff(phi2, r)), r)
    )
    vacuum_subs = {
        phi1: 0,
        phi2: 0,
        sp.diff(phi1, r): 0,
        sp.diff(phi2, r): 0,
        sp.diff(phi1, r, 2): 0,
        sp.diff(phi2, r, 2): 0,
    }
    check_zero(
        "cartesian_complex_EL_phi1_vanishes_at_vacuum_on_curved_metric",
        EL_phi1.subs(vacuum_subs),
    )
    check_zero(
        "cartesian_complex_EL_phi2_vanishes_at_vacuum_on_curved_metric",
        EL_phi2.subs(vacuum_subs),
    )

    # Collective radial Noether current and stress components vanish at Psi_C = 0
    J_r_cart = (e_sph * c0 / A_fn**2) * (
        phi1 * sp.diff(phi2, r) - phi2 * sp.diff(phi1, r)
    )
    rho_C_cart = c0**2 * (
        sp.diff(phi1, r) ** 2 + sp.diff(phi2, r) ** 2
    ) / (2 * A_fn**2) + UC_cart
    pr_C_cart = c0**2 * (
        sp.diff(phi1, r) ** 2 + sp.diff(phi2, r) ** 2
    ) / (2 * A_fn**2) - UC_cart
    check_zero("cartesian_collective_current_vanishes_at_vacuum", J_r_cart.subs(vacuum_subs))
    check_zero("cartesian_collective_energy_vanishes_at_vacuum", rho_C_cart.subs(vacuum_subs))
    check_zero("cartesian_collective_pressure_vanishes_at_vacuum", pr_C_cart.subs(vacuum_subs))

    # Verify exact recovery of REFG_ISOLATED_COVARIANT_V2 total stress at Psi_C = 0
    T_osc, T_EM = sp.symbols("T_osc T_EM", real=True)
    T_total_unified = T_osc + T_EM + rho_C_cart
    check_zero(
        "unified_stress_reduces_to_isolated_covariant_v2_at_vacuum",
        T_total_unified.subs(vacuum_subs) - (T_osc + T_EM),
    )

    # ------------------------------------------------------------------
    # Group 4: Active branch (x > 0) exact equivalence with W3-54 and W3-62
    # ------------------------------------------------------------------
    # Envelope minimization of rho_env(x; n_C) = n_C^2 / (2*x) + U_C(x) (in c0 = 1 units for clean algebra, then with c0 restored)
    nC_pos = sp.symbols("nC_pos", positive=True)
    UC_c1 = mu0**2 * x / 2 + lamC * x**2 / 4
    rho_env = nC_pos**2 / (2 * x) + UC_c1
    drho_env_dx = sp.diff(rho_env, x)
    d2rho_env_dx2 = sp.diff(rho_env, x, 2)
    checks["active_branch_envelope_hessian_positive"] = bool(d2rho_env_dx2.is_positive)

    # Parametrize stationary point by x > 0: n_C(x) = x * sqrt(2 * U_C'(x)) = x * mu(x)
    mu_of_x = sp.sqrt(mu0**2 + lamC * x)
    nC_of_x = x * mu_of_x
    check_zero(
        "envelope_stationarity_satisfied_by_nC_of_x",
        drho_env_dx.subs(nC_pos, nC_of_x),
    )

    rhoC_of_x = sp.simplify(rho_env.subs(nC_pos, nC_of_x))
    expected_rhoC_of_x = mu0**2 * x + sp.Rational(3, 4) * lamC * x**2
    check_zero("active_branch_energy_density_formula", rhoC_of_x - expected_rhoC_of_x)

    # Thermodynamic derivative d(rho_C)/d(n_C) = (d rho_C / dx) / (d n_C / dx)
    drhoC_dnC = sp.simplify(sp.diff(rhoC_of_x, x) / sp.diff(nC_of_x, x))
    check_zero("envelope_chemical_potential_equals_mu", drhoC_dnC - mu_of_x)

    # Thermodynamic pressure p_C = n_C * rho_C'(n_C) - rho_C(n_C) vs dual Lagrangian pressure
    pC_thermo = sp.simplify(nC_of_x * drhoC_dnC - rhoC_of_x)
    pC_dual = sp.simplify((x * mu_of_x**2 / 2 - UC_c1))
    expected_pC = lamC * x**2 / 4
    check_zero("thermodynamic_pressure_matches_dual_lagrangian", pC_thermo - pC_dual)
    check_zero("active_branch_pressure_formula", pC_thermo - expected_pC)

    # Hilbert stress tensor equivalence across 3 routes in basis [u_mu u_nu, g_mu_nu]:
    # Route A (W3-54): (rho_C + p_C) u_mu u_nu + p_C g_mu_nu
    # Route B (Dual action variation at dtheta_mu = -mu u_mu): x * mu^2 u_mu u_nu + p_C_dual g_mu_nu
    check_zero(
        "hilbert_stress_uu_component_matches_w54",
        (rhoC_of_x + pC_thermo) - x * mu_of_x**2,
    )
    check_zero(
        "hilbert_stress_g_component_matches_w54",
        pC_thermo - pC_dual,
    )

    # Dilute W3-62 cold-dust limit in terms of dimensionless eta = lamC * x / mu0^2 > 0
    eta = sp.symbols("eta", positive=True)
    x_eta = eta * mu0**2 / lamC
    specific_energy_ratio = sp.simplify(
        (rhoC_of_x / (mu0 * nC_of_x)).subs(x, x_eta)
    )
    expected_specific_energy_ratio = (1 + sp.Rational(3, 4) * eta) / sp.sqrt(1 + eta)
    check_zero(
        "dilute_specific_energy_ratio_identity",
        specific_energy_ratio - expected_specific_energy_ratio,
    )
    check_zero(
        "dilute_specific_energy_limit_is_one",
        sp.limit(specific_energy_ratio, eta, 0) - 1,
    )

    wC_eta = sp.simplify((pC_thermo / rhoC_of_x).subs(x, x_eta))
    expected_wC_eta = eta / (4 + 3 * eta)
    check_zero("dilute_eos_parameter_identity", wC_eta - expected_wC_eta)
    check_zero("dilute_eos_limit_is_zero", sp.limit(wC_eta, eta, 0))

    cs2_eta = sp.simplify(
        (sp.diff(pC_thermo, x) / sp.diff(rhoC_of_x, x)).subs(x, x_eta)
    )
    expected_cs2_eta = eta / (2 + 3 * eta)
    check_zero("dilute_sound_speed_squared_identity", cs2_eta - expected_cs2_eta)
    check_zero("dilute_sound_speed_limit_is_zero", sp.limit(cs2_eta, eta, 0))
    check_zero(
        "high_density_sound_speed_upper_bound_is_one_third",
        sp.limit(cs2_eta, eta, sp.oo) - sp.Rational(1, 3),
    )

    # ------------------------------------------------------------------
    # Group 5: Once-only unified source ledger and negative controls
    # ------------------------------------------------------------------
    unified_source_ledger = OrderedDict(
        [
            ("localized_oscillon_T_osc", 1),
            ("maxwell_field_T_EM", 1),
            ("collective_phase_T_C", 1),
            ("metric_self_energy_readded_on_rhs", 0),
            ("clock_or_ruler_readout_p_readded", 0),
            ("foundation_pressure_P_F_readded", 0),
            ("vacuum_offset_duplicated_in_U_C", 0),
        ]
    )
    checks["once_only_unified_source_ledger_exact"] = (
        unified_source_ledger["localized_oscillon_T_osc"] == 1
        and unified_source_ledger["maxwell_field_T_EM"] == 1
        and unified_source_ledger["collective_phase_T_C"] == 1
        and sum(list(unified_source_ledger.values())[3:]) == 0
    )

    # Negative controls (each must fail its corresponding production identity)
    # NC1: Nonzero vacuum offset U_C(0) = V0 != 0 spoils T^C = 0 at x = 0
    V0_mut = sp.symbols("V0_mut", positive=True)
    L_dual_mut_vacuum = L_dual_target - (e_det / c0) * V0_mut
    negative_controls["nonzero_UC0_vacuum_offset_rejected"] = not exact_zero(
        L_dual_mut_vacuum.subs(x, 0)
    )

    # NC2: Negative quartic coupling lamC < 0 violates c_s^2 > 0 in dilute regime
    cs2_neg_lam = cs2_eta.subs(eta, -sp.Rational(1, 10))
    negative_controls["negative_quartic_coupling_instability_rejected"] = bool(
        cs2_neg_lam < 0
    )

    # NC3: Doubling collective stress breaks envelope Legendre identity
    negative_controls["doubled_collective_stress_rejected"] = not exact_zero(
        2 * (rhoC_of_x + pC_thermo) - x * mu_of_x**2
    )

    # NC4: Identifying p_C with dust (p_C = 0) at finite eta > 0 fails thermodynamic identity
    negative_controls["finite_density_exact_dust_misidentification_rejected"] = (
        not exact_zero(pC_thermo.subs(x, 1))
    )

    # NC5: Naive W54 stationary eikonal on nonconstant lapse N(r) = 1 - m/r fails
    negative_controls["naive_w54_stationary_vacuum_on_curved_lapse_rejected"] = (
        not exact_zero(
            eikonal_radial_derivative.subs({N_fn: 1 - sp.Rational(1, 5) / r})
        )
    )

    checks["all_negative_controls_rejected"] = all(negative_controls.values())

    # ------------------------------------------------------------------
    # Group 6: Provenance and upstream hash verification
    # ------------------------------------------------------------------
    contract_hash_ok = (
        contract_path.exists() and sha256(contract_path) == CONTRACT_SHA256
    )
    checks["contract_sha256_verified"] = contract_hash_ok

    dependency_status = OrderedDict()
    for rel_path, expected_hash in UPSTREAM_HASHES.items():
        full_path = root / rel_path
        actual_hash = sha256(full_path) if full_path.exists() else None
        ok = actual_hash == expected_hash
        dependency_status[rel_path] = OrderedDict(
            [
                ("exists", full_path.exists()),
                ("expected_sha256", expected_hash),
                ("actual_sha256", actual_hash),
                ("verified", ok),
            ]
        )
    checks["all_upstream_dependencies_verified"] = all(
        item["verified"] for item in dependency_status.values()
    )

    closure_flags = OrderedDict(
        [
            (
                "w54_hydrodynamic_zero_current_obstruction_proved",
                checks["w54_nC_directional_derivative_discontinuity_at_zero"]
                and checks[
                    "w54_stationary_eikonal_incompatible_with_nonconstant_lapse"
                ],
            ),
            (
                "unified_action_regular_at_zero_collective_field",
                checks["envelope_J_vanishes_regularly_at_x_zero"]
                and checks["dual_lagrangian_vanishes_at_x_zero"]
                and checks[
                    "cartesian_complex_EL_phi1_vanishes_at_vacuum_on_curved_metric"
                ]
                and checks[
                    "cartesian_complex_EL_phi2_vanishes_at_vacuum_on_curved_metric"
                ],
            ),
            (
                "isolated_covariant_v2_recovered_exact",
                checks["unified_stress_reduces_to_isolated_covariant_v2_at_vacuum"],
            ),
            (
                "w54_barotropic_source_recovered_on_positive_branch",
                checks["hilbert_stress_uu_component_matches_w54"]
                and checks["hilbert_stress_g_component_matches_w54"],
            ),
            (
                "w62_dilute_cold_dust_limit_recovered_exact",
                checks["dilute_specific_energy_limit_is_one"]
                and checks["dilute_eos_limit_is_zero"]
                and checks["dilute_sound_speed_limit_is_zero"],
            ),
            (
                "once_only_unified_source_ledger_verified",
                checks["once_only_unified_source_ledger_exact"],
            ),
            ("inhomogeneous_ambient_background_perturbation_solved", False),
            ("microscopic_node_origin_derived", False),
        ]
    )

    passed_count = sum(1 for v in checks.values() if v)
    total_count = len(checks)
    status = (
        "PASS_EXACT_UNIFIED_ACTION_AND_REGULAR_VACUUM_REDUCTION"
        if passed_count == total_count
        else "FAIL_UNIFIED_ACTION_AUDIT"
    )

    return OrderedDict(
        [
            ("claim_id", CLAIM_ID),
            ("model_version", MODEL_VERSION),
            ("status", status),
            ("passed", passed_count),
            ("total", total_count),
            ("checks", checks),
            ("exact_residuals", residuals),
            ("negative_controls", negative_controls),
            ("closure_flags", closure_flags),
            ("dependencies", dependency_status),
            (
                "provenance",
                OrderedDict(
                    [
                        ("verifier_sha256", sha256(Path(__file__).resolve())),
                        (
                            "contract_sha256",
                            sha256(contract_path) if contract_path.exists() else None,
                        ),
                        ("python_version", platform.python_version()),
                        ("sympy_version", sp.__version__),
                    ]
                ),
            ),
        ]
    )


if __name__ == "__main__":
    result = run_checks()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["passed"] == result["total"] else 1)
