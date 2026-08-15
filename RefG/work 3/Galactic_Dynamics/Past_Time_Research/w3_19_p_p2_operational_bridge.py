import sympy as sp
import json
import hashlib
from pathlib import Path

def generate_hash(content):
    if not content:
        return ""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def main():
    print("Running W3_19: Complete p/p^2 Physical Bridge & Matter Epoch Gate...")
    
    # Define symbols
    A, a_e, t, r, c = sp.symbols('A a_e t r c', real=True, positive=True)
    kappa_tau, kappa_m, rho_m0, P_ref = sp.symbols('kappa_tau kappa_m rho_m0 P_ref', real=True, positive=True)
    
    # ---------------------------------------------------------
    # 1. Coordinate and Kinematic Bridge (from W3_09 map)
    # ---------------------------------------------------------
    # Geometric readout map defines a from P.
    # W3_09 assumed P = P_ref a^(-1.5), which means p = a^(-3/4).
    # Thus physical scale factor A = a/p = a^(7/4) => a = A^(4/7).
    # This locks P(A):
    P_A = P_ref * (A**(sp.Rational(4, 7)))**(-sp.Rational(3, 2))
    
    # Verify P(A) scales as A^(-6/7)
    P_A_simplified = sp.simplify(P_A)
    print(f"Foundation Pressure P(A) based on W3_09 bridge: {P_A_simplified}")
    
    # ---------------------------------------------------------
    # Kinematic Bridge and Clock Cancellation
    # ---------------------------------------------------------
    p_e = a_e**(-sp.Rational(3, 4))
    p_o = 1
    
    # Biconformal metric: ds^2 = -c^2 p^2 dt^2 + p^-2 a^2 dr^2
    # Coordinate time stretch for photon propagation:
    dt_stretch = (1 * p_o**(-2)) / (a_e * p_e**(-2))
    dtau_stretch = dt_stretch * (p_o / p_e)
    dtau_stretch = sp.simplify(dtau_stretch)
    
    # Physical scale factor A = a/p
    A_e = a_e / p_e
    Z_geom = 1 / A_e - 1
    
    sn_kinematic_cancellation = bool(sp.simplify(dtau_stretch - (Z_geom + 1)) == 0)
    
    # ---------------------------------------------------------
    # 2. Physical Closure & H_phys Derivation
    # ---------------------------------------------------------
    # Postulate 1: Physical dust matter conservation
    rho_m = rho_m0 * A**(-3)
    
    # Postulate 2: RefG evolutionary dynamics
    # dP/dtau = - kappa_tau * P - kappa_m * rho_m
    
    # Chain rule: dP/dtau = (dP/dA) * A * H_phys
    dP_dA = sp.diff(P_A_simplified, A)
    chain_rule_LHS = dP_dA * A 
    
    # H_phys = (dP/dtau) / (A * dP/dA)
    dP_dtau_RHS = - kappa_tau * P_A_simplified - kappa_m * rho_m
    H_phys = sp.simplify(dP_dtau_RHS / chain_rule_LHS)
    
    print(f"Derived H_phys(A) = {H_phys}")
    
    # ---------------------------------------------------------
    # 3. Matter Epoch Recovery Gate (q_early)
    # ---------------------------------------------------------
    # Deceleration parameter q = -1 - (A/H) * (dH/dA)
    dH_dA = sp.diff(H_phys, A)
    q_A = sp.simplify(-1 - (A / H_phys) * dH_dA)
    
    # Evaluate early limit (A -> 0)
    # Since H_phys = C1 + C2 A^(-15/7), the A^(-15/7) term dominates.
    q_early = sp.limit(q_A, A, 0)
    print(f"Deceleration parameter in early limit q_early = {q_early}")
    
    # The gate passes ONLY if q_early == 1/2 (standard matter era)
    matter_epoch_recovered = bool(sp.simplify(q_early - sp.Rational(1, 2)) == 0)
    print(f"Matter epoch (q=1/2) recovered: {matter_epoch_recovered}")
    
    # Evaluate late limit (A -> oo)
    # The constant term dominates, so H_phys -> constant.
    q_late = sp.limit(q_A, A, sp.oo)
    print(f"Deceleration parameter in late limit q_late = {q_late}")
    
    # ---------------------------------------------------------
    # 4. Structural Growth Integral Formulation
    # ---------------------------------------------------------
    A_e, A_f = sp.symbols('A_e A_f', real=True, positive=True)
    Gamma_tau = sp.Function('Gamma_tau')(A)
    
    # Number of available physical proper-time interval cycles
    dN_dlnA = Gamma_tau / H_phys
    N_RefG = sp.Integral(dN_dlnA / A, (A, A_f, A_e))
    
    print(f"Formulated Structural Integral N_RefG(A_e, A_f) = {N_RefG}")
    
    # ---------------------------------------------------------
    # 5. Save State and Hashes
    # ---------------------------------------------------------
    script_path = Path(__file__)
    script_hash = generate_hash(script_path.read_text('utf-8'))
    
    prereg_path = Path(__file__).parent / "w3_19_p_p2_operational_bridge_preregistration.md"
    prereg_content = prereg_path.read_text('utf-8') if prereg_path.exists() else ""
    prereg_hash = generate_hash(prereg_content)
    
    if not matter_epoch_recovered:
        status = "FAIL (PHYSICAL CLOSURE CONFLICT: q_early != 1/2)"
        conclusion = (
            "W3_19 successfully formulated the physical closure by retaining the W3_09 bridge (p=a^{-3/4}) "
            "and applying physical dust conservation rho_m = rho_m0 A^{-3}. "
            "This objectively derives H_phys(A) = 7*kappa_tau/6 + 7*kappa_m*rho_m0*A^{-15/7} / (6*P_ref). "
            "However, this produces q_early = 8/7, mathematically failing to recover the required matter-dominated epoch (q=1/2). "
            "The physical parameters P and rho_m were kept strictly separate as required by Codex. "
            "Because the matter epoch is lost, the pipeline stops here. The fundamental geometric readout map p(a) "
            "in RefG must be re-evaluated to restore q=1/2 before JWST and SN/BAO observations can be fitted."
        )
    else:
        status = "PIPELINE READY"
        conclusion = "Matter epoch recovered."

    print(f"\n--- GATE STATUS: {status} ---")
    print(conclusion)
    
    result_data = {
        "claim_id": "W3_19_P_P2_PHYSICAL_BRIDGE",
        "status": status,
        "source_hashes": {
            "script_hash": script_hash,
            "preregistration_hash": prereg_hash
        },
        "checks": {
            "biconformal_kinematics_cancel": sn_kinematic_cancellation,
            "matter_epoch_recovered": matter_epoch_recovered,
            "JWST_decoupling_observationally_proven": False,
            "SN_BAO_re_evaluated_in_A_tau": False
        },
        "equations": {
            "P_A_closure": str(P_A_simplified),
            "H_phys_A": str(H_phys),
            "q_early_limit": str(q_early),
            "q_late_limit": str(q_late),
            "N_RefG_integral": str(N_RefG)
        },
        "conclusion": conclusion
    }
    
    out_file = Path(__file__).parent / "w3_19_result.json"
    with open(out_file, "w") as f:
        json.dump(result_data, f, indent=2)

if __name__ == "__main__":
    main()
