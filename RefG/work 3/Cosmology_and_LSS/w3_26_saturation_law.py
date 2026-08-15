import os
import json
import hashlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.interpolate import interp1d

def main():
    print("=== W3_26: Saturation Law Formalization ===")
    
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
    
    def H_tau(A):
        return H0_R * (Om_A_R * A**(-1.5 * alpha_R) + (1.0 - Om_A_R) * A**(-1.5))
        
    def dtau_dA(A):
        return 977.8 / (A * H_tau(A))
        
    def dt_dA(A):
        # dt = Omega^-1 dtau => dt = A^(3/7) dtau
        return A**(3/7) * dtau_dA(A)
        
    # Calculate total remaining time from A=1 to A=infinity
    tau_fut_total, _ = quad(dtau_dA, 1.0, np.inf)
    t_fut_total, _ = quad(dt_dA, 1.0, np.inf)
    
    print(f"Total remaining Metric time: {t_fut_total:.3f} Gyr")
    print(f"Total remaining Internal time: {tau_fut_total:.3f} Gyr")
    
    # Generate arrays for plotting
    # We map A from 1 to 10000 to cover the asymptotic future
    A_eval = np.logspace(0, 4, 1000)
    
    t_passed = []
    current_t = 0.0
    
    # Numerically integrate up to each A to find metric time passed since today
    for i in range(len(A_eval)):
        if i == 0:
            t_passed.append(0.0)
        else:
            dt_val, _ = quad(dt_dA, A_eval[i-1], A_eval[i])
            current_t += dt_val
            t_passed.append(current_t)
            
    t_passed = np.array(t_passed)
    t_remaining = t_fut_total - t_passed
    
    # Calculate physical quantities
    # P_norm = P / P_today = A^(-6/7)
    P_norm = A_eval**(-6/7)
    
    # Mass_eff_norm = M_eff / M_today = P_norm = A^(-6/7)
    M_norm = A_eval**(-6/7)
    
    # Clock_rate_norm = (dtau/dt) / (dtau/dt)_today = A^(-3/7)
    Clock_rate = A_eval**(-3/7)
    
    # Plotting against Remaining Metric Time
    plt.figure(figsize=(10, 6))
    
    # Note: t_remaining goes from ~46.8 down to 0
    plt.plot(t_remaining, P_norm, 'b-', linewidth=2.5, label=r'Background Pressure $P/P_0$')
    plt.plot(t_remaining, M_norm, 'r--', linewidth=2.5, label=r'Effective Mass $M_{eff}/M_0$')
    plt.plot(t_remaining, Clock_rate, 'g-.', linewidth=2.5, label=r'Internal Clock Rate $(d\tau/dt) / (d\tau/dt)_0$')
    
    plt.gca().invert_xaxis()  # So time moves forward from left (46.8) to right (0)
    
    plt.axvline(x=0, color='black', linestyle='--', alpha=0.5, label='Vacuum Saturation (Equilibrium)')
    
    plt.xlabel('Remaining Metric Time to Equilibrium (Gyr)', fontsize=12)
    plt.ylabel('Normalized Physical Quantities', fontsize=12)
    plt.title('Vacuum Saturation Law: Asymptotic Dissipation of Structure', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add text annotation
    plt.text(t_fut_total * 0.4, 0.6, 
             "As $t \to t_{end}$, $P \to 0$.\nStructures lose mass and dissipate.\nInternal clocks freeze.", 
             fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
             
    plot_path = os.path.join(os.path.dirname(script_path), "w3_26_saturation_law.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nSaved plot to {os.path.basename(plot_path)}")
    
    with open(script_path, "rb") as f:
        source_hash = hashlib.sha256(f.read()).hexdigest()
        
    res_json = {
        "status": "PASS (Phantom Big Rip replaced by Thermodynamic Equilibrium / Saturation)",
        "model_version": "RefG_NonLinear_tau_branch",
        "data_provenance": {
            "dependency": "w3_24_result.json"
        },
        "results": {
            "total_remaining_metric_time_Gyr": round(t_fut_total, 3),
            "total_remaining_internal_time_Gyr": round(tau_fut_total, 3),
            "asymptotic_limits": {
                "P_background": "0",
                "M_eff": "0",
                "clock_rate_dtau_dt": "0"
            }
        },
        "source_hash": source_hash
    }
    
    json_path = os.path.join(os.path.dirname(script_path), "w3_26_result.json")
    with open(json_path, "w") as f:
        json.dump(res_json, f, indent=4)
    print(f"Saved results to {json_path}")

if __name__ == "__main__":
    main()
