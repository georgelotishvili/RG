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
    # We adopt a0 as a universal coherence scale constant in this regime. 
    # (While a0 may be derivable from deeper cosmology, here we treat it as an adopted parameter).
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

    # Express g_N in terms of total g
    g_N_sol = g**2 / (g + a0)
    
    # Verify the algebraic closure robustly
    # If g = g_N + g_v, then by substituting g_N = g^2 / (g + a0), 
    # we should recover g_v = a0 * g / (g + a0).
    # Let's check if the original equation dW_dgv = 0 is satisfied for g_N_sol and g_v_sol = g - g_N_sol
    g_v_target = g - g_N_sol
    closure_check = sp.simplify(dW_dgv.subs({g_N: g_N_sol, g_v: g_v_target}))
    assert closure_check == 0, "Algebraic closure failed symbolically."
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

    # 4. Baryonic Tully-Fisher Relation (BTFR) Derivation
    # The asymptotic velocity v for circular orbits is given by v^2 / r = g
    v, M = sp.symbols("v M", positive=True, real=True)
    orbit_eq = sp.Eq(v**2 / r, g_deep_sol)
    
    # Solve for v
    v_sol = sp.solve(orbit_eq, v)[0]
    
    # Compute v^4 symbolically
    v4_expr = sp.simplify(v_sol**4)
    
    # Mathematically prove it exactly equals G * M * a0 (and r drops out completely)
    btfr_target = G * M * a0
    assert sp.simplify(v4_expr - btfr_target) == 0, "BTFR derivation failed! v^4 is not G*M*a0"
    
    btfr_eq = sp.Eq(v**4, v4_expr)
    results["baryonic_tully_fisher_relation"] = str(btfr_eq)

    # Note: BTFR holds EXACTLY in the deep asymptotic regime.
    # We do not use any tuned free parameters (v0 is eliminated). a0 is a universal constant.
    # The mass dependence M is strictly linear with v^4.
    results["btfr_flatness_verified"] = bool(v4_expr.diff(r) == 0)
    results["asymptotic_note"] = "The BTFR v^4 = G*M*a0 is an exact derivation for the deep asymptotic regime (up to the environmental coherence boundary), containing no galaxy-specific free tuning parameters under the universal a0 condition."

    return results

if __name__ == "__main__":
    res = derive_galactic_dynamics()
    with open("w3_10_result.json", "w") as f:
        json.dump(res, f, indent=4)
    print("w3_10 derivation complete.")
    for k, v in res.items():
        print(f"{k}: {v}")
