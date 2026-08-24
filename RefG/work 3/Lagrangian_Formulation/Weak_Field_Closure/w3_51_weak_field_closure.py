"""W3-51: bounded RefG static weak-field closure.

The gate derives the operational metric from the frozen common material
response, varies one explicitly declared leading static pressure functional,
extracts the static PPN beta/gamma coefficients, and performs an independent
Einstein--Hilbert overlap check. It does not claim a microscopic derivation of
the pressure functional or a nonlinear/all-PPN completion.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_51_REFG_STATIC_WEAK_FIELD_CLOSURE"
MODEL_VERSION = "W3-51-v1.1-STATIC-WEAK-FIELD"


def zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    # ------------------------------------------------------------------
    # 1. Frozen common response -> coordinate speed and metric dictionary
    # ------------------------------------------------------------------
    length_exponent = sp.Integer(1)   # L_oper/L0 = p
    cadence_exponent = sp.Integer(1)  # Omega_t/Omega_0 = p
    period_exponent = -cadence_exponent
    coordinate_speed_exponent = sp.simplify(
        length_exponent - period_exponent
    )

    p, c0 = sp.symbols("p c0", positive=True)
    g00_p = p ** (2 * cadence_exponent)
    spatial_scale_p = p ** (-2 * length_exponent)
    null_speed_ratio = sp.simplify(sp.sqrt(g00_p / spatial_scale_p))
    local_null_speed_ratio = sp.simplify(
        sp.sqrt(spatial_scale_p / g00_p) * null_speed_ratio
    )

    common_response_ok = coordinate_speed_exponent == 2
    metric_dictionary_ok = zero(null_speed_ratio - p**2)
    local_c_ok = zero(local_null_speed_ratio - 1)

    # ---------------------------------------------------------------
    # 2. Leading static pressure functional -> sourced field equation
    # ---------------------------------------------------------------
    x, y, z = sp.symbols("x y z", real=True)
    G = sp.symbols("G", positive=True)
    rho = sp.Function("rho")(x, y, z)
    u_xyz = sp.Function("u")(x, y, z)

    grad_components = [sp.diff(u_xyz, q) for q in (x, y, z)]
    lag_density = (
        c0**4 / (8 * sp.pi * G) * sum(q**2 for q in grad_components)
        - rho * c0**2 * u_xyz
    )
    euler_lagrange = sp.diff(lag_density, u_xyz)
    for q, du_q in zip((x, y, z), grad_components):
        euler_lagrange -= sp.diff(sp.diff(lag_density, du_q), q)

    laplacian_u = sum(sp.diff(u_xyz, q, 2) for q in (x, y, z))
    expected_el = -c0**4 / (4 * sp.pi * G) * (
        laplacian_u + 4 * sp.pi * G * rho / c0**2
    )
    source_variation_residual = sp.simplify(euler_lagrange - expected_el)
    source_variation_ok = zero(source_variation_residual)

    # ------------------------------------------------------
    # 3. Spherical exterior and Gauss-normalized source charge
    # ------------------------------------------------------
    r, M = sp.symbols("r M", positive=True)
    mu = G * M / c0**2
    u_radial = sp.Function("u_radial")(r)
    radial_ode = sp.Eq(
        sp.diff(r**2 * sp.diff(u_radial, r), r), sp.Integer(0)
    )
    C_offset, C_flux = sp.symbols("C_offset C_flux", real=True)
    radial_first_integral = sp.Eq(
        r**2 * sp.diff(u_radial, r), C_flux
    )
    radial_family = sp.simplify(
        C_offset + sp.integrate(C_flux / r**2, r)
    )
    radial_ode_residual = sp.simplify(
        sp.diff(r**2 * sp.diff(radial_family, r), r)
    )
    asymptotic_solution = {C_offset: sp.Integer(0)}
    radial_asymptotic = sp.simplify(
        radial_family.subs(asymptotic_solution)
    )
    generic_gauss_flux = sp.simplify(
        4 * sp.pi * r**2 * sp.diff(radial_asymptotic, r)
    )
    expected_flux = -4 * sp.pi * G * M / c0**2
    charge_solution = sp.solve(
        sp.Eq(generic_gauss_flux, expected_flux), C_flux, dict=True
    )[0]
    u_ext = sp.simplify(radial_asymptotic.subs(charge_solution))
    exterior_laplacian = sp.simplify(
        sp.diff(u_ext, r, 2) + 2 * sp.diff(u_ext, r) / r
    )
    gauss_flux = sp.simplify(4 * sp.pi * r**2 * sp.diff(u_ext, r))
    exterior_profile_ok = (
        zero(radial_ode_residual)
        and zero(sp.limit(u_ext, r, sp.oo))
        and zero(exterior_laplacian)
        and zero(gauss_flux - expected_flux)
        and zero(u_ext - mu / r)
    )

    # ---------------------------------------------
    # 4. RefG metric expansion and PPN coefficients
    # ---------------------------------------------
    eps = sp.symbols("eps", real=True)
    u = sp.symbols("u", real=True)
    p_of_u = sp.exp(-eps * u)
    g00_refg = p_of_u**2
    spatial_refg = p_of_u**-2  # positive magnitude of -g_ii

    g00_series = sp.series(g00_refg, eps, 0, 3).removeO().expand()
    spatial_series = sp.series(spatial_refg, eps, 0, 3).removeO().expand()

    beta, gamma = sp.symbols("beta gamma", real=True)
    ppn_g00 = 1 - 2 * eps * u + 2 * beta * eps**2 * u**2
    ppn_spatial = 1 + 2 * gamma * eps * u

    beta_solution = sp.solve(
        sp.Eq(g00_series.coeff(eps, 2), ppn_g00.coeff(eps, 2)), beta
    )[0]
    gamma_solution = sp.solve(
        sp.Eq(spatial_series.coeff(eps, 1), ppn_spatial.coeff(eps, 1)), gamma
    )[0]

    beta_residual = sp.simplify(beta_solution - 1)
    gamma_residual = sp.simplify(gamma_solution - 1)
    beta_ok = zero(beta_residual)
    gamma_ok = zero(gamma_residual)

    # The common biconformal dictionary fixes gamma, while beta also probes
    # the second-order constitutive relation between p and the sourced field.
    constitutive_a = sp.symbols("a", real=True)
    p_mutated = sp.exp(-eps * u + constitutive_a * eps**2 * u**2)
    g00_mutated = sp.series(p_mutated**2, eps, 0, 3).removeO().expand()
    beta_mutated = sp.solve(
        sp.Eq(g00_mutated.coeff(eps, 2), ppn_g00.coeff(eps, 2)), beta
    )[0]
    beta_mutation_ok = zero(beta_mutated - (1 + constitutive_a))

    # Newtonian acceleration from g00: a_i = -(c0^2/2) d_i g00 at O(u).
    # With U>0 and u=U/c0^2 this gives a=grad(U), inward for U=GM/r.
    dg00_du_linear = sp.diff(g00_series.coeff(eps, 1), u)
    acceleration_coefficient = sp.simplify(-sp.Rational(1, 2) * dg00_du_linear)
    newtonian_limit_ok = acceleration_coefficient == 1

    # -------------------------------------------------------
    # 5. Independent isotropic-Schwarzschild overlap by order
    # -------------------------------------------------------
    schwarzschild_g00 = ((1 - eps * u / 2) / (1 + eps * u / 2)) ** 2
    schwarzschild_spatial = (1 + eps * u / 2) ** 4
    schwarzschild_g00_series = sp.series(
        schwarzschild_g00, eps, 0, 3
    ).removeO().expand()
    schwarzschild_spatial_series = sp.series(
        schwarzschild_spatial, eps, 0, 3
    ).removeO().expand()

    g00_eh_residual = sp.simplify(g00_series - schwarzschild_g00_series)
    spatial_eh_1pn_residual = sp.simplify(
        spatial_series.coeff(eps, 1)
        - schwarzschild_spatial_series.coeff(eps, 1)
    )
    spatial_first_out_of_scope_remainder = sp.simplify(
        (spatial_series.coeff(eps, 2)
         - schwarzschild_spatial_series.coeff(eps, 2))
        * eps**2
    )
    eh_metric_overlap_ok = zero(g00_eh_residual) and zero(
        spatial_eh_1pn_residual
    )

    # Linearized Einstein G00 for the frozen beta=gamma=1 metric.
    # In (+---), G00^(1)=-2 nabla^2 u. Substituting the sourced RefG equation
    # gives +8 pi G rho/c0^2, the Einstein 00 source normalization.
    laplacian_symbol = sp.Symbol("laplacian_u", real=True)
    einstein_g00_linear = -2 * laplacian_symbol
    einstein_g00_sourced = sp.simplify(
        einstein_g00_linear.subs(
            laplacian_symbol, -4 * sp.pi * G * rho / c0**2
        )
    )
    expected_einstein_source = 8 * sp.pi * G * rho / c0**2
    einstein_source_residual = sp.simplify(
        einstein_g00_sourced - expected_einstein_source
    )
    eh_source_overlap_ok = zero(einstein_source_residual)
    eh_overlap_ok = eh_metric_overlap_ok and eh_source_overlap_ok

    # --------------------
    # 6. Negative controls
    # --------------------
    # A: clock response only, no spatial-ruler response -> extractor gamma=0.
    clock_only_spatial = sp.Integer(1)
    gamma_clock_only = sp.solve(
        sp.Eq(
            clock_only_spatial.coeff(eps, 1),
            ppn_spatial.coeff(eps, 1),
        ),
        gamma,
    )[0]
    # B: pure conformal metric g00=p^2, |gii|=p^2 -> gamma=-1.
    pure_conformal_spatial = sp.series(p_of_u**2, eps, 0, 2).removeO()
    gamma_pure_conformal = sp.solve(
        sp.Eq(
            pure_conformal_spatial.coeff(eps, 1),
            ppn_spatial.coeff(eps, 1),
        ),
        gamma,
    )[0]
    # C: make p itself the canonical harmonic field. With p=1-u, the same
    # biconformal metric gives beta=1/2 even though gamma remains one.
    p_harmonic = 1 - eps * u
    harmonic_g00 = sp.series(p_harmonic**2, eps, 0, 3).removeO().expand()
    harmonic_spatial = sp.series(
        p_harmonic**-2, eps, 0, 2
    ).removeO().expand()
    beta_harmonic_p = sp.solve(
        sp.Eq(harmonic_g00.coeff(eps, 2), ppn_g00.coeff(eps, 2)), beta
    )[0]
    gamma_harmonic_p = sp.solve(
        sp.Eq(
            harmonic_spatial.coeff(eps, 1),
            ppn_spatial.coeff(eps, 1),
        ),
        gamma,
    )[0]
    negative_controls_ok = (
        gamma_clock_only != 1
        and gamma_pure_conformal != 1
        and beta_harmonic_p != 1
        and gamma_harmonic_p == 1
    )

    flags = {
        "COMMON_RESPONSE_TO_CCOORD": bool(common_response_ok),
        "OPERATIONAL_METRIC_DICTIONARY": bool(metric_dictionary_ok),
        "LOCAL_C_INVARIANCE": bool(local_c_ok),
        "STATIC_SOURCE_VARIATION": bool(source_variation_ok),
        "SPHERICAL_EXTERIOR_PROFILE": bool(exterior_profile_ok),
        "PPN_BETA": bool(beta_ok),
        "PPN_GAMMA": bool(gamma_ok),
        "EH_OVERLAP": bool(eh_overlap_ok),
        "NEGATIVE_CONTROLS": bool(negative_controls_ok),
        "BETA_CONSTITUTIVE_MUTATION_CONTROL": bool(beta_mutation_ok),
        "MICRO_SOURCE_DERIVATION": False,
        "FULL_PPN": False,
        "NONLINEAR_EH_COMPLETION": False,
    }
    tested_flags = [
        "COMMON_RESPONSE_TO_CCOORD",
        "OPERATIONAL_METRIC_DICTIONARY",
        "LOCAL_C_INVARIANCE",
        "STATIC_SOURCE_VARIATION",
        "SPHERICAL_EXTERIOR_PROFILE",
        "PPN_BETA",
        "PPN_GAMMA",
        "EH_OVERLAP",
        "NEGATIVE_CONTROLS",
        "BETA_CONSTITUTIVE_MUTATION_CONTROL",
    ]
    gate_pass = all(flags[name] for name in tested_flags) and newtonian_limit_ok
    aggregate_status = (
        "CONDITIONAL_MATCHED_THROUGH_STATIC_SPHERICAL_PPN_BETA_GAMMA"
        if gate_pass
        else "FAIL"
    )

    script_path = Path(__file__).resolve()
    contract_path = script_path.with_name(
        "w3_51_weak_field_closure_contract.md"
    )
    result_path = script_path.with_name("w3_51_result.json")

    result = {
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "gate_status": "PASS" if gate_pass else "FAIL",
        "aggregate_status": aggregate_status,
        "domain": "static spherical weak field; g00 O(u^2), gij O(u)",
        "conditional_premise": (
            "canonical additive log-response u=-ln(p), its static gradient "
            "functional and linear effective active-source coupling through "
            "1PN amplitude; microscopic derivation remains open"
        ),
        "derived": {
            "coordinate_speed_exponent": str(coordinate_speed_exponent),
            "null_speed_ratio": str(null_speed_ratio),
            "local_null_speed_ratio": str(local_null_speed_ratio),
            "metric": "ds^2=p^2*c0^2*dt^2-p^(-2)*dX^2",
            "euler_lagrange_equation": "laplacian(u)=-4*pi*G*rho/c0^2",
            "radial_vacuum_ode": str(radial_ode),
            "radial_first_integral": str(radial_first_integral),
            "radial_integrated_family": str(radial_family),
            "asymptotically_flat_family": str(radial_asymptotic),
            "gauss_charge_solution": {
                str(k): str(v) for k, v in charge_solution.items()
            },
            "exterior_solution": str(u_ext),
            "gauss_flux": str(gauss_flux),
            "g00_series": str(g00_series),
            "spatial_series": str(spatial_series),
            "PPN_beta": str(beta_solution),
            "PPN_gamma": str(gamma_solution),
            "beta_under_ln_p_mutation": str(beta_mutated),
            "newtonian_acceleration_coefficient": str(
                acceleration_coefficient
            ),
        },
        "residuals": {
            "source_variation": str(source_variation_residual),
            "radial_ode": str(radial_ode_residual),
            "exterior_laplacian": str(exterior_laplacian),
            "gauss_flux": str(sp.simplify(gauss_flux - expected_flux)),
            "beta_minus_one": str(beta_residual),
            "gamma_minus_one": str(gamma_residual),
            "EH_g00_declared_order": str(g00_eh_residual),
            "EH_spatial_declared_order": str(spatial_eh_1pn_residual),
            "EH_linear_G00_source": str(einstein_source_residual),
            "first_out_of_scope_spatial_remainder": str(
                spatial_first_out_of_scope_remainder
            ),
        },
        "negative_controls": {
            "clock_only_gamma": str(gamma_clock_only),
            "pure_conformal_gamma": str(gamma_pure_conformal),
            "harmonic_p_beta": str(beta_harmonic_p),
            "harmonic_p_gamma": str(gamma_harmonic_p),
        },
        "closure_flags": flags,
        "scope_boundary": {
            "micro_source_derivation": "OPEN",
            "full_PPN": "NOT_TESTED",
            "2PN_spatial_completion": "NOT_TESTED",
            "strong_field": "NOT_TESTED",
        },
        "provenance": {
            "sympy_version": sp.__version__,
            "script_sha256": sha256(script_path),
            "contract_sha256": sha256(contract_path),
        },
    }
    result_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
