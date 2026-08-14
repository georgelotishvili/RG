import sympy as sp
import json
import os


def derive_galactic_dynamics():
    """
    Derives the exact galactic rotation dynamics and Baryonic Tully-Fisher Relation (BTFR)
    starting strictly from the Refractive Gravity (RefG) low-energy macroscopic postulate.
    """
    results = {}

    # 1. The Low-Energy Postulate: Vortex Loading Potential
    g_v, g_N, a0 = sp.symbols("g_v g_N a0", positive=True, real=True)

    # The chosen loading potential that dictates the response of the topological
    # defect vacuum to localized baryonic mass (g_N)
    W = g_v**3 / 3 + g_N * g_v**2 / 2 - a0 * g_N * g_v

    # Variation with respect to the vortex response field g_v must be zero
    dW_dgv = sp.diff(W, g_v)
    results["postulate_variation_eq"] = str(sp.Eq(dW_dgv, 0))

    # Solve for g_v
    gv_solutions = sp.solve(sp.Eq(dW_dgv, 0), g_v)
    # g_v is positive, so we take the positive root
    gv_sol = sp.simplify(gv_solutions[0])
    results["vortex_field_solution"] = str(sp.Eq(g_v, gv_sol))

    # The total gravitational acceleration is g = g_N + g_v
    g = sp.symbols("g", positive=True, real=True)
    g_total_expr = g_N + gv_sol

    # We want to express g_N in terms of total g to find the interpolating function
    # Note: gv_sol = (-g_N + sqrt(g_N^2 + 4 a0 g_N))/2
    # So g = (g_N + sqrt(g_N^2 + 4 a0 g_N))/2
    # 2g - g_N = sqrt(g_N^2 + 4 a0 g_N)
    # 4g^2 - 4g g_N + g_N^2 = g_N^2 + 4 a0 g_N
    # 4g^2 = 4 g_N (g + a0) => g_N = g^2 / (g + a0)
    g_N_sol = g**2 / (g + a0)
    
    # Verify the algebraic closure
    closure_expr = (g_total_expr).subs(g_N, g_N_sol)
    # Sympy needs help with square roots of squared positive polynomials
    closure_check = sp.simplify(closure_expr)
    closure_check = closure_check.replace(sp.sqrt(g**2 * (g + 2*a0)**2 / (a0 + g)**2), g * (g + 2*a0) / (a0 + g))
    # To be safe, we can just check it numerically at a random positive point:
    num_check = float(abs(closure_expr.subs({g: 2.5, a0: 1.2}) - 2.5))
    assert num_check < 1e-9, f"Algebraic closure failed numerically. Diff: {num_check}"
    results["effective_newtonian_source"] = str(sp.Eq(g_N, g_N_sol))

    # MOND interpolation function mu(x) where x = g/a0 and g_N = g * mu(x)
    x = sp.symbols("x", positive=True, real=True)
    mu_expr = g_N_sol / g
    mu_x = sp.simplify(mu_expr.subs(g, x * a0))
    results["derived_interpolation_function"] = str(sp.Eq(sp.symbols("mu(x)"), mu_x))

    # 2. Field Equation for Disk Geometry
    # The true localized source follows Poisson's equation: Div(g_N) = 4*pi*G*rho
    # Substituting our derived relation:
    results["AQUAL_field_equation"] = "Div( g^2 / (g + a0) * n_vector ) = 4*pi*G*rho"

    # 3. Deep MOND Limit (Far Field)
    # Far from the galactic center, g << a0
    # Thus mu(x) ~ x
    g_deep = sp.symbols("g_deep", positive=True, real=True)
    g_N_deep = sp.limit(g_N_sol, g, 0, dir="+") # Actually we need Taylor expansion for small g
    # g^2 / (a0 * (1 + g/a0)) ~ g^2 / a0
    g_N_deep = g**2 / a0
    results["deep_mond_limit_gN"] = str(sp.Eq(g_N, g_N_deep))

    # Deep MOND Gauss's law for total mass M enclosed
    # Integral of Div(g_N_deep) dV = 4*pi*G*M
    # Integral of g_N_deep * dA = 4*pi*G*M
    # Assuming the far-field monopole dominates, area is 4*pi*r^2
    r, G, M = sp.symbols("r G M", positive=True, real=True)
    gauss_eq = sp.Eq((g_deep**2 / a0) * 4 * sp.pi * r**2, 4 * sp.pi * G * M)
    g_deep_sol = sp.solve(gauss_eq, g_deep)[0]
    results["far_field_acceleration"] = str(sp.Eq(g_deep, g_deep_sol))

    # 4. Exact BTFR Derivation
    # For circular orbits in the disk plane, centrifugal acceleration is v^2 / r
    v = sp.symbols("v", positive=True, real=True)
    orbit_eq = sp.Eq(v**2 / r, g_deep_sol)
    v_sol = sp.solve(orbit_eq, v)[0]
    v4_sol = sp.simplify(v_sol**4)
    
    # We prove that v^4 is EXACTLY G * M * a0, and the radius r drops out completely,
    # leaving no free parameters and no v0 assumption.
    btfr_eq = sp.Eq(v**4, v4_sol)
    results["baryonic_tully_fisher_relation"] = str(btfr_eq)
    
    # Verifying r is totally eliminated
    assert v4_sol.diff(r) == 0, "Radius 'r' did not cancel out. BTFR is not flat!"
    results["btfr_flatness_verified"] = True

    return results

if __name__ == "__main__":
    res = derive_galactic_dynamics()
    with open("w3_10_result.json", "w") as f:
        json.dump(res, f, indent=4)
    print("w3_10 derivation complete.")
    for k, v in res.items():
        print(f"{k}: {v}")
