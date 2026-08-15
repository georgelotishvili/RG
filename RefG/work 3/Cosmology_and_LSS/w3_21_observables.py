import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import json

def H_t(z, H0=70.0, Om_m=0.3, Om_L=0.7):
    """
    W3_19b background derived metric Hubble parameter.
    H_phys(A) ~ K + B * A^{-3/2}  =>  H_t(z) = H0 * (Om_L + Om_m * (1+z)^{1.5})
    """
    return H0 * (Om_L + Om_m * (1+z)**1.5)

def Omega(z):
    """
    Local operational time rate factor.
    Omega(A) = A^{-3/7} = (1+z)^{3/7}
    """
    return (1+z)**(3/7)

def H_tau(z, H0=70.0, Om_m=0.3, Om_L=0.7):
    """
    Structural Hubble parameter (what CC measures).
    H_tau = H_t / Omega
    """
    return H_t(z, H0, Om_m, Om_L) / Omega(z)

def dt_dz(z, H0=70.0, Om_m=0.3, Om_L=0.7):
    # 1 km/s/Mpc = 1.022e-3 1/Gyr
    H_Gyr = H_t(z, H0, Om_m, Om_L) * 1.022e-3
    return 1.0 / ((1+z) * H_Gyr)

def dtau_dz(z, H0=70.0, Om_m=0.3, Om_L=0.7):
    return Omega(z) * dt_dz(z, H0, Om_m, Om_L)

def main():
    # 1. JWST Time availability
    # From formation z=10 to emission z=5 (example)
    z_f = 10.0
    z_e = 5.0
    
    delta_t, _ = quad(dt_dz, z_e, z_f)
    delta_tau, _ = quad(dtau_dz, z_e, z_f)
    
    print(f"--- JWST Interval (z={z_f} -> z={z_e}) ---")
    print(f"Metric time elapsed: {delta_t:.3f} Gyr")
    print(f"Structural time elapsed: {delta_tau:.3f} Gyr")
    print(f"Ratio (tau/t): {delta_tau/delta_t:.2f}")
    print("------------------------------------------")
    
    # 2. Plotting H_t vs H_tau vs LCDM
    z_range = np.linspace(0, 2.5, 100)
    Ht_vals = H_t(z_range)
    Htau_vals = H_tau(z_range)
    
    def H_LCDM(z, H0=70.0, Om_m=0.3):
        return H0 * np.sqrt(1 - Om_m + Om_m * (1+z)**3)
        
    H_LCDM_vals = H_LCDM(z_range)
    
    plt.figure(figsize=(10, 6))
    plt.plot(z_range, Ht_vals, label=r'RefG $H_t(z)$ (Metric)', color='blue', linestyle='--')
    plt.plot(z_range, Htau_vals, label=r'RefG $H_\tau(z) = H_t(z)/\Omega(z)$ (CC Observable)', color='red', linewidth=2)
    plt.plot(z_range, H_LCDM_vals, label=r'$\Lambda$CDM', color='black', linestyle=':', alpha=0.7)
    
    plt.xlabel('Redshift $z$', fontsize=14)
    plt.ylabel(r'$H(z)$ [km/s/Mpc]', fontsize=14)
    plt.title('RefG W3_21: Metric vs Structural Hubble Parameter', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    out_img = 'C:/Users/george/.gemini/antigravity-ide/brain/f3800565-f13c-42d8-ae6a-b22d401e8359/w3_21_hubble_rates.png'
    plt.savefig(out_img, dpi=300)
    print(f"Saved plot to {out_img}")
    
    # Save results to json in artifact dir
    out_json = 'C:/Users/george/.gemini/antigravity-ide/brain/f3800565-f13c-42d8-ae6a-b22d401e8359/w3_21_results.json'
    res = {
        "jwst_interval": {
            "z_start": z_f,
            "z_end": z_e,
            "delta_t_Gyr": round(delta_t, 3),
            "delta_tau_Gyr": round(delta_tau, 3),
            "ratio": round(delta_tau/delta_t, 3)
        }
    }
    with open(out_json, "w") as f:
        json.dump(res, f, indent=4)
    print(f"Saved results to {out_json}")

if __name__ == "__main__":
    main()
