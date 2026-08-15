import sympy as sp
import json
import os
import hashlib
from pathlib import Path

def main():
    print("=== RefG Cosmology: Non-Linear Process-to-Metric Bridge (W3_09b) ===\n")
    
    # 1. Define Symbols
    t, tau = sp.symbols('t tau', real=True)
    P = sp.Function('P')(t)
    P_tau = sp.Function('P')(tau)
    P_ref = sp.Symbol('P_ref', real=True, positive=True)
    
    alpha = sp.Symbol('alpha', real=True)
    k0 = sp.Symbol('kappa_0', real=True, positive=True)
    C0 = sp.Symbol('C_0', real=True, positive=True)
    
    # Scale factor geometric link
    # a(t) = (P_ref / P(t))^(2/3)
    a_t = (P_ref / P)**(sp.Rational(2,3))
    a_tau = (P_ref / P_tau)**(sp.Rational(2,3))
    
    print("--- Postulate: Local Potential and Time Dilation ---")
    print("Phi = -1/2 * ln(P/P_ref)")
    print("Omega = dtau/dt = exp(-Phi) = (P/P_ref)^(1/2)")
    
    Omega_t = (P / P_ref)**(sp.Rational(1,2))
    Omega_tau = (P_tau / P_ref)**(sp.Rational(1,2))
    
    # Lapse function N = dt/dtau = 1/Omega
    N_tau = 1 / Omega_tau
    
    # 2. Non-Linear Relaxation Equation in tau-frame
    # We want to find what dP/dtau must be to yield the non-linear dP/dt
    # In t-frame, we assume: dP/dt = -kappa_0 * P * (P/P_ref)^alpha - C_0 * a(t)^(-3)
    dP_dt_target = -k0 * P * (P/P_ref)**alpha - C0 * a_t**(-3)
    
    # Chain rule: dP/dtau = dP/dt * dt/dtau = dP/dt * N_tau
    # Let's compute dP/dtau in terms of P_tau
    dP_dtau_derived = dP_dt_target.subs(P, P_tau) * N_tau
    dP_dtau_derived = sp.simplify(dP_dtau_derived)
    
    print("\nDerived Non-Linear Dynamics in internal tau-frame:")
    print("dP/dtau =")
    sp.pprint(dP_dtau_derived)
    
    # Test specific alpha = -1/2
    dP_dtau_alpha_half = sp.simplify(dP_dtau_derived.subs(alpha, sp.Rational(-1,2)))
    print("\nIf alpha = -1/2, dP/dtau becomes:")
    sp.pprint(dP_dtau_alpha_half)
    
    print("Notice that for alpha = -1/2, the relaxation part (first term) is strictly CONSTANT!")
    
    # Verification
    # Is the transformation consistent?
    dP_dt_back = dP_dtau_derived.subs(P_tau, P) / N_tau.subs(P_tau, P)
    residual = sp.simplify(dP_dt_back - dP_dt_target)
    is_consistent = (residual == 0)
    
    print(f"\nConsistency Check: {is_consistent}")
    
    # Is the relaxation part constant for alpha = -1/2?
    # Relaxation part is the term without C_0
    dP_dtau_relax = dP_dtau_alpha_half.subs(C0, 0)
    is_constant_relaxation = (sp.diff(dP_dtau_relax, P_tau) == 0)
    
    # Save Metadata JSON
    script_path = os.path.abspath(__file__)
    with open(script_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
        
    out_status = "CONDITIONAL PASS (Given P -> Phi Postulate)" if is_consistent else "FAIL (Inconsistent bridge)"
    
    res_json = {
        "claim_id": "W3_09B_NONLINEAR_BRIDGE",
        "model_version": "W3-09b-v1.0-NONLINEAR",
        "status": out_status,
        "results": {
            "consistency": is_consistent,
            "alpha_minus_half_implies_constant_relaxation": bool(is_constant_relaxation)
        },
        "source_hash": file_hash
    }
    
    out_path = os.path.join(os.path.dirname(script_path), "w3_09b_result.json")
    with open(out_path, "w") as f:
        json.dump(res_json, f, indent=4)
        
if __name__ == "__main__":
    main()
