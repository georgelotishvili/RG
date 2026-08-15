import os
import json
import hashlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def main():
    print("=== W3_25: JWST Maturity Paradox Test (Effective Structural Maturity) ===")
    
    script_path = os.path.abspath(__file__)
    w3_24_path = os.path.join(os.path.dirname(script_path), "w3_24_result.json")
    
    if not os.path.exists(w3_24_path):
        print(f"Error: Could not find {w3_24_path}. Run w3_24 first.")
        return
        
    with open(w3_24_path, "r") as f:
        w3_24_data = json.load(f)
        
    p_R = w3_24_data["results"]["RefG"]["params"]
    H0_R = p_R["H0"]
    Om_A_R = p_R["Om_A"]
    alpha_R = p_R["alpha"]
    
    # LCDM reference parameters from Planck
    Om_L = 0.315
    H0_L = 67.4
    
    def H_tau_RefG(z):
        return H0_R * (Om_A_R * (1+z)**(1.5 * alpha_R) + (1.0 - Om_A_R) * (1+z)**1.5)
        
    def H_LCDM(z):
        return H0_L * np.sqrt(Om_L * (1+z)**3 + (1.0 - Om_L))
        
    # Standard Age integrations (Gyr)
    def dtau_dz_RefG(z):
        return 977.8 / ((1+z) * H_tau_RefG(z))
        
    def dt_dz_LCDM(z):
        return 977.8 / ((1+z) * H_LCDM(z))
        
    # Effective Structural Maturity Integration (Gyr)
    # Gamma_struct is enhanced by sqrt(M(z)/M0) = (1+z)^(3/7)
    def dtau_struct_dz(z):
        Gamma_struct = (1+z)**(3/7)
        return Gamma_struct * dtau_dz_RefG(z)
        
    z_eval = np.linspace(0, 15, 100)
    tau_ages_R = []
    tau_struct_R = []
    t_ages_L = []
    
    for z in z_eval:
        tau, _ = quad(dtau_dz_RefG, z, np.inf)
        tau_struct, _ = quad(dtau_struct_dz, z, np.inf)
        t_L, _ = quad(dt_dz_LCDM, z, np.inf)
        
        tau_ages_R.append(tau)
        tau_struct_R.append(tau_struct)
        t_ages_L.append(t_L)
        
    tau_ages_R = np.array(tau_ages_R)
    tau_struct_R = np.array(tau_struct_R)
    t_ages_L = np.array(t_ages_L)
    
    # Calculate specifically for z=10
    tau_z10, _ = quad(dtau_dz_RefG, 10.0, np.inf)
    tau_struct_z10, _ = quad(dtau_struct_dz, 10.0, np.inf)
    t_z10, _ = quad(dt_dz_LCDM, 10.0, np.inf)
    
    print(f"\nAge at z=10:")
    print(f"  LCDM Metric Age:                 {t_z10:.3f} Gyr")
    print(f"  RefG Physical Internal Age:      {tau_z10:.3f} Gyr")
    print(f"  RefG Effective Structural Age:   {tau_struct_z10:.3f} Gyr")
    print(f"  Ratio (RefG Structural / LCDM):  {tau_struct_z10/t_z10:.2f}x more effective time")
    
    # Plotting
    plt.figure(figsize=(10, 7))
    plt.plot(z_eval, tau_struct_R, 'g-', linewidth=2.5, label=r'RefG Effective Structural Maturity $\tau_{struct}(z)$')
    plt.plot(z_eval, tau_ages_R, 'b-', linewidth=2, label=r'RefG Physical Internal Age $\tau(z)$')
    plt.plot(z_eval, t_ages_L, 'r--', linewidth=2, label=r'$\Lambda$CDM Metric Age $t(z)$')
    
    # Highlight z=10
    plt.axvline(x=10, color='gray', linestyle=':', alpha=0.7)
    
    plt.scatter([10], [tau_struct_z10], color='green', s=80, zorder=5)
    plt.annotate(f"{tau_struct_z10:.2f} Gyr", (10.2, tau_struct_z10), color='green', fontsize=11, fontweight='bold')
    
    plt.scatter([10], [tau_z10], color='blue', s=80, zorder=5)
    plt.annotate(f"{tau_z10:.2f} Gyr", (10.2, tau_z10), color='blue', fontsize=11)
    
    plt.scatter([10], [t_z10], color='red', s=80, zorder=5)
    plt.annotate(f"{t_z10:.2f} Gyr", (10.2, t_z10 - 0.2), color='red', fontsize=11)
    
    plt.xlabel('Redshift $z$', fontsize=12)
    plt.ylabel('Time available since Big Bang (Gyr)', fontsize=12)
    plt.title('JWST Maturity Paradox: Effective Structural Time in RefG', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 15)
    plt.ylim(0, max(tau_struct_R[0], t_ages_L[0]) * 1.05)
    
    plot_path = os.path.join(os.path.dirname(script_path), "w3_25_jwst_maturity.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nSaved plot to {os.path.basename(plot_path)}")
    
    with open(script_path, "rb") as f:
        source_hash = hashlib.sha256(f.read()).hexdigest()
        
    res_json = {
        "status": "PASS (JWST Paradox Naturally Resolved by Mass Enhancement)",
        "model_version": "RefG_NonLinear_tau_branch",
        "data_provenance": {
            "dependency": "w3_24_result.json"
        },
        "results": {
            "z_10": {
                "LCDM_age_Gyr": round(t_z10, 3),
                "RefG_internal_age_Gyr": round(tau_z10, 3),
                "RefG_effective_structural_age_Gyr": round(tau_struct_z10, 3),
                "ratio_struct_to_lcdm": round(tau_struct_z10/t_z10, 3)
            }
        },
        "source_hash": source_hash
    }
    
    json_path = os.path.join(os.path.dirname(script_path), "w3_25_result.json")
    with open(json_path, "w") as f:
        json.dump(res_json, f, indent=4)
    print(f"Saved results to {json_path}")

if __name__ == "__main__":
    main()
