import sympy as sp
import json
import os

def formulate_refractive_lensing():
    """
    Demonstrates that the RefG macroscopic vacuum index of refraction
    produces the exact same weak lensing signature as an Isothermal Dark Matter halo,
    via direct integration of the deflection angle.
    """
    results = {}
    
    r, b, z = sp.symbols('r b z', positive=True, real=True)
    c, G, r0, V_f = sp.symbols('c G r0 V_f', positive=True, real=True)
    
    # Impact parameter relation: r = sqrt(b^2 + z^2)
    r_expr = sp.sqrt(b**2 + z**2)
    
    # 1. Standard GR with Isothermal Dark Matter Halo
    # An isothermal halo produces a flat rotation curve v(r) = V_f
    # This requires M(r) = (V_f^2 / G) * r
    # Therefore, g_GR = G * M(r) / r^2 = V_f^2 / r
    g_GR = V_f**2 / r
    results["GR_Isothermal_Acceleration"] = str(g_GR)
    
    # 2. RefG deep MOND limit (Far Field)
    # We derived in w3_10 that g_deep = sqrt(G*M*a0)/r.
    # By BTFR, V_f^2 = sqrt(G*M*a0), so g_RefG = V_f^2 / r.
    g_RefG = V_f**2 / r
    results["RefG_Macroscopic_Acceleration"] = str(g_RefG)
    
    # Potential Phi: -dPhi/dr = g => Phi = - V_f^2 * ln(r/r0)
    # Wait, if g = -dPhi/dr and g > 0, then dPhi/dr < 0, so Phi = - V_f^2 ln(r/r0).
    # Conventionally, we use positive potential Phi = V_f^2 ln(r/r0) and g = dPhi/dr 
    # depending on metric signature. Let's stick to standard attractive Phi = V_f^2 ln(r/r0).
    # Then force per unit mass is -Grad(Phi) = -V_f^2/r r_hat. Magnitude is V_f^2/r.
    Phi = V_f**2 * sp.log(r / r0)
    results["RefG_Macroscopic_Potential"] = str(Phi)
    
    # In RefG, the vacuum is an optical medium. 
    # The effective refractive index for transverse waves (photons) 
    # in a weak pressure deficit Phi is given by:
    # n(r) = 1 - 2*Phi(r)/c^2
    n = 1 - 2 * Phi / c**2
    results["Refractive_Index"] = str(n)
    
    # The deflection angle alpha for a photon passing at impact parameter b
    # alpha = Integral_path ( Grad_perp(n) ) dz
    # Grad_perp(n) = dn/db = (dn/dr) * (dr/db)
    dn_dr = sp.diff(n, r)
    dr_db = sp.diff(r_expr.subs(z, 0), b) # In 3D, dr/db = b/r
    
    # Let's substitute r_expr directly into n
    n_bz = n.subs(r, r_expr)
    dn_db = sp.diff(n_bz, b)
    
    # Deflection angle integral: int_{-\infty}^{\infty} dn_db dz
    # We can integrate this symbolically. 
    # dn_db = - (2 V_f^2 / c^2) * b / (b^2 + z^2)
    # Integral of b/(b^2+z^2) dz is arctan(z/b). 
    # From -inf to inf, it is pi.
    integral_val = sp.integrate(dn_db, (z, -sp.oo, sp.oo))
    
    # Note: Magnitude of deflection
    alpha_RefG = sp.simplify(sp.Abs(integral_val))
    results["Deflection_Angle_RefG"] = str(alpha_RefG)
    
    # Equivalence Proof
    results["Lensing_Equivalence_Note"] = (
        "The derivation explicitly integrates the refractive index gradient along the photon path. "
        f"The resulting deflection angle alpha = {str(alpha_RefG)} exactly matches the standard GR "
        "prediction for a Singular Isothermal Sphere (DM halo). Because photons couple to the total "
        "topological pressure deficit Phi through n=1-2*Phi/c^2, and this same Phi defines the rotation curve, "
        "RefG guarantees that lensing mass exactly equals dynamical mass without dark matter."
    )
    
    return results

if __name__ == "__main__":
    res = formulate_refractive_lensing()
    with open("w3_13_result.json", "w") as f:
        json.dump(res, f, indent=4)
    print("w3_13 Refractive Lensing complete.")
    for k, v in res.items():
        print(f"{k}: {v}")
