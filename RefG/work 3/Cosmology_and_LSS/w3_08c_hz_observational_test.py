import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import json
import os
import hashlib

# Cosmic Chronometer (OHD) Data Compilation
# Format: [z, H(z), sigma_H]
CC_DATA = np.array([
    [0.07, 69, 19.6], [0.09, 69, 12], [0.12, 68.6, 26.2],
    [0.17, 83, 8], [0.179, 75, 4], [0.199, 75, 5],
    [0.2, 72.9, 29.6], [0.27, 77, 14], [0.28, 88.8, 36.6],
    [0.352, 83, 14], [0.3802, 83, 13.5], [0.4, 95, 17],
    [0.4004, 77, 10.2], [0.4247, 87.1, 11.2], [0.4497, 92.8, 12.9],
    [0.47, 89, 50], [0.4783, 80.9, 9], [0.48, 97, 62],
    [0.593, 104, 13], [0.68, 92, 8], [0.781, 105, 12],
    [0.875, 125, 17], [0.88, 90, 40], [0.9, 117, 23],
    [1.037, 154, 20], [1.3, 168, 17], [1.363, 160, 33.6],
    [1.43, 177, 18], [1.53, 140, 14], [1.75, 202, 40],
    [1.965, 186.5, 50.4]
])

def h_lcdm(params, z):
    H0, Om = params
    Ol = 1.0 - Om # Flat universe
    return H0 * np.sqrt(Ol + Om * (1+z)**3)

def h_refg(params, z):
    # H(a) = A + B * a^{-1.5}
    # a = 1 / (1+z)  =>  a^{-1.5} = (1+z)^{1.5}
    A, B = params
    return A + B * (1+z)**1.5

def chi2(params, model_func, z, H, err):
    H_model = model_func(params, z)
    return np.sum(((H - H_model) / err)**2)

def main():
    z = CC_DATA[:, 0]
    H = CC_DATA[:, 1]
    err = CC_DATA[:, 2]
    
    # Fit LCDM
    res_lcdm = minimize(chi2, [70.0, 0.3], args=(h_lcdm, z, H, err), bounds=[(50, 100), (0, 1)])
    H0_fit, Om_fit = res_lcdm.x
    chi2_lcdm = res_lcdm.fun
    
    # Fit RefG
    res_refg = minimize(chi2, [30.0, 40.0], args=(h_refg, z, H, err), bounds=[(0, 100), (0, 100)])
    A_fit, B_fit = res_refg.x
    chi2_refg = res_refg.fun
    
    # Statistics (AIC = chi2 + 2k, BIC = chi2 + k*ln(N))
    N = len(z)
    k = 2 # Both models have 2 parameters
    
    aic_lcdm = chi2_lcdm + 2*k
    aic_refg = chi2_refg + 2*k
    
    print("=== Observational H(z) Cosmic Chronometers Fit ===")
    print(f"Number of data points: {N}")
    print(f"LambdaCDM Fit: H0 = {H0_fit:.2f}, Omega_m = {Om_fit:.3f}")
    print(f"LambdaCDM Chi2: {chi2_lcdm:.2f}, AIC: {aic_lcdm:.2f}\n")
    
    print(f"RefG Fit (n=2/3): A = {A_fit:.2f}, B = {B_fit:.2f}")
    print(f"RefG Chi2: {chi2_refg:.2f}, AIC: {aic_refg:.2f}\n")
    
    # Plotting
    z_plot = np.linspace(0, 2, 100)
    H_lcdm_plot = h_lcdm([H0_fit, Om_fit], z_plot)
    H_refg_plot = h_refg([A_fit, B_fit], z_plot)
    
    plt.figure(figsize=(10, 6))
    plt.errorbar(z, H, yerr=err, fmt='o', color='gray', alpha=0.6, label='CC Data (OHD)')
    plt.plot(z_plot, H_lcdm_plot, label='$\Lambda$CDM Fit', linestyle='--', color='black')
    plt.plot(z_plot, H_refg_plot, label='RefG Fit', color='blue', linewidth=2)
    plt.xlabel('Redshift (z)')
    plt.ylabel('H(z) [km/s/Mpc]')
    plt.title('H(z) Observational Test: RefG vs $\Lambda$CDM')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('hz_observational_fit.png')
    
    # Parameter errors (approximate from inverse Hessian if available)
    def get_errors(res):
        try:
            return np.sqrt(np.diag(res.hess_inv)).tolist()
        except:
            return [None, None]
            
    err_lcdm = get_errors(res_lcdm)
    err_refg = get_errors(res_refg)
    
    # Save Metadata JSON
    script_path = os.path.abspath(__file__)
    with open(script_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
        
    res_json = {
        "model_version": "RefG_Observational_v1.0",
        "status": "FIT_COMPATIBILITY",
        "dataset": {
            "name": "Cosmic Chronometers (OHD)",
            "points": N,
            "sources": "Compilation (Moresco 2016, Stern 2010, etc.)",
            "systematics": "Not included in this baseline fit"
        },
        "models_compared": ["LCDM", "RefG"],
        "results_lcdm": {
            "optimization_success": res_lcdm.success,
            "H0": {"value": H0_fit, "error": err_lcdm[0]},
            "Omega_m": {"value": Om_fit, "error": err_lcdm[1]},
            "chi2": chi2_lcdm,
            "reduced_chi2": chi2_lcdm / (N - k),
            "AIC": aic_lcdm
        },
        "results_refg": {
            "optimization_success": res_refg.success,
            "A": {"value": A_fit, "error": err_refg[0]},
            "B": {"value": B_fit, "error": err_refg[1]},
            "derived_H0": A_fit + B_fit,
            "chi2": chi2_refg,
            "reduced_chi2": chi2_refg / (N - k),
            "AIC": aic_refg
        },
        "source_hash": file_hash
    }
    
    out_path = os.path.join(os.path.dirname(script_path), "w3_08c_results.json")
    with open(out_path, "w") as f:
        json.dump(res_json, f, indent=4)
    print("Saved plot to 'hz_observational_fit.png' and JSON to 'w3_08c_results.json'")

if __name__ == "__main__":
    main()
