import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import sys
import json

def main():
    print("=== RefG Cosmology: Matter-Vacuum Transition ===")
    
    # Symbols
    a = sp.Symbol('a', real=True, positive=True)
    n = sp.Symbol('n', real=True, positive=True)
    kappa = sp.Symbol('kappa', real=True, positive=True)
    C = sp.Symbol('C', real=True, positive=True) # C = kappa_m * rho_m0 / P_i
    
    # H(a) derivation
    # P = P_i * a^{-1/n}
    # dot_P = - kappa * P - C * P_i * a^{-3}
    # H = -n * dot_P / P
    H_a = n * (kappa + C * a**(1/n - 3))
    
    # q(a) derivation
    # q = -1 - a/H * dH/da
    dH_da = sp.diff(H_a, a)
    q_a = sp.simplify(-1 - (a / H_a) * dH_da)
    
    print(f"General H(a) = {H_a}")
    print(f"General q(a) = {q_a}")
    
    # We must substitute n = 2/3 before limit because 1-3n sign is ambiguous to SymPy
    print("\n--- Substituting n = 2/3 ---")
    H_a_23 = sp.simplify(H_a.subs(n, sp.Rational(2, 3)))
    q_a_23 = sp.simplify(q_a.subs(n, sp.Rational(2, 3)))
    
    print(f"H(a) [n=2/3] = {H_a_23}")
    print(f"q(a) [n=2/3] = {q_a_23}")
    
    # Asymptotic limits for n=2/3
    q_early = sp.limit(q_a_23, a, 0)
    q_late = sp.limit(q_a_23, a, sp.oo)
    
    print(f"\nLimit a->0 (Early Matter Era): q = {q_early}")
    print(f"Limit a->oo (Late Vacuum Era): q = {q_late}")
    
    # Transition scale factor (where q=0)
    a_trans = sp.solve(q_a_23, a)
    print(f"Transition Scale Factor a_trans = {a_trans}")
    
    # Lambda CDM for comparison
    O_L = sp.Symbol('Omega_Lambda', real=True, positive=True)
    O_m = sp.Symbol('Omega_m', real=True, positive=True)
    H0 = sp.Symbol('H0', real=True, positive=True)
    
    H_LCDM = H0 * sp.sqrt(O_L + O_m * a**-3)
    q_LCDM = sp.simplify(-1 - (a / H_LCDM) * sp.diff(H_LCDM, a))
    print(f"\nLCDM H(a) = {H_LCDM}")
    print(f"LCDM q(a) = {q_LCDM}")
    
    # Plotting
    # We will normalize so that H(a=1) = 1 for both models.
    # For LCDM: O_m = 0.3, O_L = 0.7, H0 = 1
    # For RefG: H(1) = 2/3 kappa + 2/3 C = 1.
    # We want to match the transition point.
    # LCDM a_trans = (O_m / (2 O_L))^(1/3) = (0.3 / 1.4)^(1/3) ~ 0.598
    # RefG a_trans = (C / (2 kappa))^(2/3)
    # Let's set kappa and C to match H(1)=1 and a_trans=0.598
    
    a_vals = np.logspace(-1, 1, 500)
    
    def q_lcdm_num(a_val):
        return -1 + 1.5 * (0.3 * a_val**-3) / (0.7 + 0.3 * a_val**-3)
        
    def q_refg_num(a_val, k, c):
        # q = -1 + 1.5 * c * a^(-3/2) / (k + c * a^(-3/2))
        return -1 + 1.5 * c * a_val**-1.5 / (k + c * a_val**-1.5)
        
    # Find matching parameters for RefG
    # k + c = 1.5 (since H(1) = 2/3(k+c) = 1)
    # (c / 2k)^(2/3) = 0.598 => c / 2k = 0.598^(1.5) = 0.462 => c = 0.924 k
    # k + 0.924 k = 1.5 => k = 0.779, c = 0.721
    k_val = 0.779
    c_val = 0.721
    
    q_l_vals = [q_lcdm_num(x) for x in a_vals]
    q_r_vals = [q_refg_num(x, k_val, c_val) for x in a_vals]
    
    plt.figure(figsize=(10, 6))
    plt.plot(a_vals, q_l_vals, label='$\Lambda$CDM ($O_m=0.3$)', linestyle='--', color='black')
    plt.plot(a_vals, q_r_vals, label='RefG ($n=2/3$)', color='blue', linewidth=2)
    plt.axhline(0, color='gray', linestyle=':', alpha=0.5)
    plt.axvline(0.598, color='red', linestyle=':', alpha=0.5, label='Transition ($a \\approx 0.6$)')
    plt.xscale('log')
    plt.xlabel('Scale Factor (a)')
    plt.ylabel('Deceleration Parameter q(a)')
    plt.title('Deceleration Parameter: RefG vs $\Lambda$CDM')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.savefig('q_transition.png')
    print("Saved plot to 'q_transition.png'")
    
    import os
    import hashlib
    script_path = os.path.abspath(__file__)
    
    with open(script_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
        
    res = {
        "model_version": "RefG_Cosmology_v1.0",
        "status": "CONDITIONAL EXACT BACKGROUND SOLUTION",
        "assumptions": [
            "P_i > P_0 = 0 (Total vacuum relaxation)",
            "a = (P_i / P)^n (Readout law)",
            "n = 2/3 (3D geometric projection factor)",
            "dot_P = -kappa*P - kappa_m*rho_m (Matter + Relaxation dynamics)"
        ],
        "parameters": {
            "n": "2/3",
            "kappa": k_val,
            "C": c_val
        },
        "results": {
            "H_a": str(H_a_23),
            "q_a": str(q_a_23),
            "transition_a": str(a_trans),
            "q_early_limit": str(q_early),
            "q_late_limit": str(q_late)
        },
        "source_hash": file_hash
    }
    
    out_path = os.path.join(os.path.dirname(script_path), "w3_08b_results.json")
    with open(out_path, "w") as f:
        json.dump(res, f, indent=4)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    main()
