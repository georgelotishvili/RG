"""REFG_ISOLATED_COVARIANT_V2: new source/dictionary and ADM first-law checks.

Reuses the existing equilibrium solver; does not rerun its 69-test campaign.
Thresholds frozen in foundation_revision.md. Optional output stays in this
research package. No observational or global-stability pass is produced.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import scipy
import sympy as sp
from scipy.integrate import cumulative_trapezoid

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "Lagrangian_Formulation" / "Oscillon_Inertia" / "verify_oscillon_inertia.py"
BASE_HASH = "32cf32e9cfd590f93928eff16cbfe5494836df8b9d72bfd88b3cf3ba7da22076"
Q0 = 190.401136223484


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_base():
    if digest(BASE) != BASE_HASH:
        raise RuntimeError("Existing covariant inertia dependency changed")
    spec = importlib.util.spec_from_file_location("revision_covariant_inertia", BASE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def symbolic_checks():
    checks = {}

    def zero(key, expr):
        checks[key] = bool(sp.simplify(expr) == 0)

    r, alpha, z, pr = sp.symbols("r alpha z pr", positive=True)
    mass = (1-z*z)*r/(2*alpha)
    dn = alpha*(mass+r**3*pr)/(r*r*z*z)
    da = (1-1/z)/r
    target = alpha*r*pr/(z*z)+(1-z)**2/(2*r*z*z)
    zero("independent_stress_clock_ruler_identity", dn+da-target)
    zero("vacuum_positive_lock_defect", target.subs(pr, 0)-(1-z)**2/(2*r*z*z))
    checks["nonzero_mass_exact_lock_control_rejected"] = target.subs({pr: 0, z: sp.Rational(9, 10)}) != 0

    N, A, c, v, w, k, mu = sp.symbols("N A c v omega k mu", positive=True)
    null_symbol = -w*w/(c*c*N*N)+k*k/(A*A)
    zero("scalar_metric_null_cone", null_symbol.subs(w, c*N*k/A))
    # Derive Maxwell principal symbol directly from k_mu F^{mu,nu}.
    kx, ky, kz = sp.symbols("kx ky kz", real=True)
    avec = sp.Matrix(sp.symbols("a0 a1 a2 a3", real=True))
    inverse_metric = sp.diag(-1/(c*c*N*N), 1/(A*A), 1/(A*A), 1/(A*A))
    kcov = sp.Matrix([-w, kx, ky, kz])
    kup = inverse_metric*kcov
    ksq = (kcov.T*kup)[0]
    field_strength = kup*avec.T-avec*kup.T
    divergence = (kcov.T*field_strength).T
    symbol_matrix = ksq*sp.eye(4)-kup*kcov.T
    zero("Maxwell_symbol_from_field_strength", sum(x*x for x in divergence-symbol_matrix*avec))
    zero("Maxwell_gauge_direction", sum(x*x for x in symbol_matrix*kup))
    zero("Maxwell_Lorenz_reduction", sum(x*x for x in divergence-ksq*avec+kup*(kcov.T*avec)[0]))
    null_maxwell = symbol_matrix.subs({kx: k, ky: 0, kz: 0, w: c*N*k/A})
    for index in (2, 3):
        polarization = sp.eye(4)[:, index]
        zero(f"Maxwell_null_transverse_polarization_{index}", sum(x*x for x in null_maxwell*polarization))
    checks["Maxwell_null_kernel_includes_gauge_and_two_polarizations"] = null_maxwell.rank() == 1
    local_speed = A*(c*N/A)/N
    zero("proper_clock_ruler_give_local_light_speed", local_speed-c)
    point_lag = -mu*c*c*N*sp.sqrt(1-A*A*v*v/(N*N*c*c))
    zero("redshifted_rest_energy", -point_lag.subs(v, 0)-mu*c*c*N)
    zero("coordinate_inertia_is_not_redshifted_rest_mass", sp.diff(point_lag, v, 2).subs(v, 0)-mu*A*A/N)
    checks["redshift_as_coordinate_inertia_control_rejected"] = sp.simplify(mu*A*A/N-mu*N) != 0
    zz = sp.symbols("zeta", real=True)
    zero("schwarzschild_isotropic_dictionary", (1-zz)/(1+zz)*(1+zz)**2-(1-zz*zz))

    f, fp, P, m, sig, Om, pot, dpot = sp.symbols("f fp P m sigma Omega V Vprime", positive=True)
    F = 1-2*alpha*m/r
    h = r*r*fp*fp+P*P/(r*r*f*f)
    density = F*h/(2*r*r)+pot
    zero("linear_mass_constraint", r*r*density-(r*r*pot+h/2-alpha*h*m/r))
    P_eq = Om*r*r*f*f/(sig*F)
    zero("constraint_integrating_factor_is_lapse", (alpha*h/r).subs(P, P_eq)-alpha*r*(fp*fp+Om*Om*f*f/(sig*sig*F*F)))
    zero("energy_charge_functional_derivative", (sig*F*sp.diff(h, P)/2).subs(P, P_eq)-Om)
    # Functional f derivative, at fixed P and after radial integration by parts.
    local_f_term = sig*(r*r*dpot+F*sp.diff(h, f)/2)
    zero("energy_amplitude_variation_is_KG_source", local_f_term.subs(P, P_eq)-sig*r*r*(dpot-Om*Om*f/(sig*sig*F)))
    zero("energy_gradient_variation_is_KG_flux", sig*F*sp.diff(h, fp)/2-sig*r*r*F*fp)
    return checks


def profile(base, sol, points):
    r = np.linspace(sol.x[0], sol.x[-1], points)
    f, fp, m, ls, q = sol.sol(r)
    sig = np.exp(ls)
    om = float(1/(1+np.exp(-sol.p[0])))
    F = 1-2*base.ALPHA*m/r
    if np.min(F) <= 0:
        raise RuntimeError("Static chart outside frozen F>0 domain")
    N = sig*np.sqrt(F)
    radial_pressure = om*om*f*f/(2*sig*sig*F)+F*fp*fp/2-base.potential(f)
    outer_mass = base.ALPHA*m[-1]
    iso_outer = (r[-1]-outer_mass+np.sqrt(r[-1]*(r[-1]-2*outer_mass)))/2
    logA_outer = np.log(r[-1]/iso_outer)
    geo_integral = cumulative_trapezoid((1/np.sqrt(F)-1)/r, r, initial=0)
    logA = logA_outer+geo_integral[-1]-geo_integral
    metric_product = np.log(N)+logA
    rhs = base.ALPHA*r*radial_pressure/F+(1-np.sqrt(F))**2/(2*r*F)
    stress_integral = cumulative_trapezoid(rhs, r, initial=0)
    stress_product = np.log(N[-1])+logA_outer-stress_integral[-1]+stress_integral
    bc = sol.inertia_bc(sol.y[:, 0], sol.y[:, -1], sol.p)
    return {
        "points": points, "radius": float(r[-1]), "omega": om,
        "adm_mass": float(4*np.pi*m[-1]), "charge": float(4*np.pi*q[-1]),
        "minimum_F": float(np.min(F)), "central_clock": float(N[0]),
        "central_ruler_factor": float(np.exp(-logA[0])),
        "central_clock_times_A": float(np.exp(metric_product[0])),
        "central_coordinate_light_speed": float(N[0]*np.exp(-logA[0])),
        "central_pressure": float(radial_pressure[0]),
        "pressure_reconstruction_max_error": float(np.max(np.abs(metric_product-stress_product))),
        "max_boundary_residual": float(np.max(np.abs(bc))),
        "max_BVP_residual": float(np.max(sol.rms_residuals)),
        "absolute_outer_field": float(abs(f[-1])),
    }


def run():
    base = load_base()
    base.CHARGE = Q0
    seed = base.load_seed_module()
    flat = seed.solve_profile(.8, radius=80., tolerance=1e-8)
    a = base.equilibrium(flat, 40., 3e-8)
    b = base.equilibrium(flat, 60., 3e-8, previous=a)
    coarse = profile(base, a, 8001)
    fine_grid = profile(base, b, 16001)
    coarse_grid = profile(base, b, 8001)
    checks = symbolic_checks()
    for tag, row in (("R40", coarse), ("R60", fine_grid)):
        checks[f"{tag}_source_stress_reconstruction"] = row["pressure_reconstruction_max_error"] < 3e-7
        checks[f"{tag}_boundary_residual"] = row["max_boundary_residual"] < 1e-8
        checks[f"{tag}_BVP_residual"] = row["max_BVP_residual"] < 1e-6
        checks[f"{tag}_localized_tail"] = row["absolute_outer_field"] < 1e-8
        checks[f"{tag}_positive_metric"] = row["minimum_F"] > 0
        checks[f"{tag}_exact_common_scale_lock_rejected"] = abs(row["central_clock_times_A"]-1) > 1e-4
    mass_domain_error = abs(coarse["adm_mass"]-fine_grid["adm_mass"])/fine_grid["adm_mass"]
    product_domain_error = abs(coarse["central_clock_times_A"]-coarse_grid["central_clock_times_A"])
    product_grid_error = abs(coarse_grid["central_clock_times_A"]-fine_grid["central_clock_times_A"])
    checks["mass_domain_agreement"] = mass_domain_error < 1e-7
    checks["product_domain_agreement"] = product_domain_error < 2e-7
    checks["product_grid_agreement"] = product_grid_error < 2e-7
    rows = []
    try:
        for step in (.002, .001):
            neighbors = []
            for sign in (-1, 1):
                base.CHARGE = Q0*(1+sign*step)
                sol = base.equilibrium(flat, 60., 3e-8, previous=b)
                neighbors.append(profile(base, sol, 8001))
            low, high = neighbors
            slope = (high["adm_mass"]-low["adm_mass"])/(high["charge"]-low["charge"])
            rows.append({"relative_charge_step": step, "low": low, "high": high,
                         "dM_dQ": slope, "omega_center": fine_grid["omega"],
                         "relative_first_law_error": abs(slope/fine_grid["omega"]-1),
                         "dOmega_dQ": (high["omega"]-low["omega"])/(high["charge"]-low["charge"])})
            checks[f"charge_step_{step}_neighbor_BVPs"] = all(x["max_BVP_residual"] < 1e-6 and x["max_boundary_residual"] < 1e-8 for x in neighbors)
    finally:
        base.CHARGE = Q0
    checks["independent_ADM_first_law"] = rows[-1]["relative_first_law_error"] < 1e-5
    checks["first_law_charge_step_refinement"] = abs(rows[0]["dM_dQ"]-rows[1]["dM_dQ"]) < 2e-5
    flags = {
        "same_action_source_dictionary": all(checks.values()),
        "ADM_first_law_numerical": checks["independent_ADM_first_law"],
        "existing_ADM_inertia_proof_reused": digest(BASE) == BASE_HASH,
        "radial_hessian": "separate radial_adm_hessian.py artifact; not inferred here",
        "original_collective_current_vacuum_reduction_derived": False,
        "microscopic_foundation_derivation": False,
        "cosmological_completion": False,
        "observational_validation": False,
        "singularity_removal": False,
    }
    return {
        "model_version": "REFG_ISOLATED_COVARIANT_V2",
        "status": "PASS_DECLARED_REVISION_CHECKS" if all(checks.values()) else "FAIL_DECLARED_REVISION_CHECKS",
        "checks": checks, "passed": sum(checks.values()), "total": len(checks),
        "reference_state": fine_grid, "radius40": coarse,
        "errors": {"mass_domain_relative": mass_domain_error,
                   "central_product_domain": product_domain_error, "central_product_grid": product_grid_error},
        "charge_neighbors": rows, "closure_flags": flags,
        "provenance": {"script_sha256": digest(Path(__file__)),
                       "contract_sha256": digest(HERE / "foundation_revision.md"),
                       "existing_inertia_solver_sha256": digest(BASE),
                       "W58_sha256": digest(base.W58), "python": platform.python_version(),
                       "numpy": np.__version__, "scipy": scipy.__version__, "sympy": sp.__version__},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output is not None:
        target = args.output.resolve()
        if target.parent != HERE:
            raise ValueError("Output must remain in the Inertia research package")
        target.write_text(output+"\n", encoding="utf-8")
    print(output)
    raise SystemExit(0 if result["passed"] == result["total"] else 1)
