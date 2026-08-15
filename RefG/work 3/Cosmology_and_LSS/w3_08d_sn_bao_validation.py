import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize
import json
import os
import hashlib
import urllib.request
import sys

# Speed of light in km/s
c = 299792.458

def fetch_pantheon():
    # URLs for Pantheon Binned Data
    url_lcparam = "https://raw.githubusercontent.com/dscolnic/Pantheon/master/Binned_data/lcparam_DS17f.txt"
    url_sys = "https://raw.githubusercontent.com/dscolnic/Pantheon/master/Binned_data/sys_DS17f.txt"
    
    print("Downloading Pantheon data...")
    lcparam_file = "lcparam_DS17f.txt"
    sys_file = "sys_DS17f.txt"
    
    if not os.path.exists(lcparam_file):
        urllib.request.urlretrieve(url_lcparam, lcparam_file)
    if not os.path.exists(sys_file):
        urllib.request.urlretrieve(url_sys, sys_file)
        
    # Read lcparam
    # Columns: name zcmb zhel dz mb dmb ...
    z_sn = []
    mb_sn = []
    dmb_sn = []
    with open(lcparam_file, "r") as f:
        lines = f.readlines()
        for line in lines[1:]: # skip header
            parts = line.strip().split()
            if len(parts) > 5:
                z_sn.append(float(parts[1]))
                mb_sn.append(float(parts[4]))
                dmb_sn.append(float(parts[5]))
                
    z_sn = np.array(z_sn)
    mb_sn = np.array(mb_sn)
    dmb_sn = np.array(dmb_sn)
    N = len(z_sn)
    
    # Read systematic covariance
    with open(sys_file, "r") as f:
        lines = f.readlines()
        # First line is usually dimension
        dim = int(lines[0].strip())
        cov_sys = np.zeros((dim, dim))
        idx = 0
        for line in lines[1:]:
            val = float(line.strip())
            row = idx // dim
            col = idx % dim
            cov_sys[row, col] = val
            idx += 1
            
    # Total covariance matrix C = C_stat + C_sys
    cov_tot = cov_sys.copy()
    for i in range(N):
        cov_tot[i, i] += dmb_sn[i]**2
        
    return z_sn, mb_sn, cov_tot

def E_lcdm(z, Om):
    Ol = 1.0 - Om
    return np.sqrt(Ol + Om * (1+z)**3)

def E_refg(z, A, B):
    H0 = A + B
    return (A + B * (1+z)**1.5) / H0

def lum_dist(z, model_func, *args):
    integral, _ = quad(lambda x: 1.0 / model_func(x, *args), 0, z)
    return (1+z) * integral

def mu_model(M, z_array, model_func, *args):
    mu = np.zeros(len(z_array))
    for i, z in enumerate(z_array):
        d_l_free = lum_dist(z, model_func, *args)
        mu[i] = 5.0 * np.log10(d_l_free) + M
    return mu

def chi2_sn_cov(M, z_array, mu_obs, inv_cov, model_func, *args):
    mu_mod = mu_model(M, z_array, model_func, *args)
    delta = mu_obs - mu_mod
    return delta.T @ inv_cov @ delta
    
def d_v(z, model_func, *args):
    # D_V(z) = [ c z D_M^2(z) / H(z) ]^{1/3}
    # Since we are taking ratios, we drop constant c and H0 scaling, 
    # but we must evaluate H(z) proportional correctly.
    d_m = lum_dist(z, model_func, *args) / (1+z)
    E_z = model_func(z, *args)
    return (z * d_m**2 / E_z)**(1/3)

def main():
    print("=== RefG Cosmology: SN Ia & BAO Full Covariance VALIDATION ===")
    
    # Load parameters from previous fit
    json_path = "w3_08c_results.json"
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Run w3_08c first.")
        return
        
    with open(json_path, "r") as f:
        res_c = json.load(f)
        
    Om_frozen = res_c["results_lcdm"]["Omega_m"]["value"]
    A_frozen = res_c["results_refg"]["A"]["value"]
    B_frozen = res_c["results_refg"]["B"]["value"]
    
    print(f"Loaded frozen parameters:")
    print(f"  LCDM: Omega_m = {Om_frozen}")
    print(f"  RefG: A = {A_frozen}, B = {B_frozen}")
    
    # Load Pantheon
    z_sn, mu_sn, cov_tot = fetch_pantheon()
    inv_cov = np.linalg.inv(cov_tot)
    N_sn = len(z_sn)
    
    # Fit only M
    res_lcdm = minimize(chi2_sn_cov, [10.0], args=(z_sn, mu_sn, inv_cov, E_lcdm, Om_frozen))
    M_lcdm = res_lcdm.x[0]
    chi2_lcdm = res_lcdm.fun
    
    res_refg = minimize(chi2_sn_cov, [10.0], args=(z_sn, mu_sn, inv_cov, E_refg, A_frozen, B_frozen))
    M_refg = res_refg.x[0]
    chi2_refg = res_refg.fun
    
    print(f"\n--- Supernova Ia (Pantheon 40 Bins) ---")
    print(f"LCDM Chi2 = {chi2_lcdm:.2f} / {N_sn-1} (M = {M_lcdm:.3f})")
    print(f"RefG Chi2 = {chi2_refg:.2f} / {N_sn-1} (M = {M_refg:.3f})")
    print(f"Delta Chi2 (RefG - LCDM) = {chi2_refg - chi2_lcdm:.2f}")
    
    # BAO Analysis (Relative D_V ratios to cancel r_d)
    # BOSS DR12 Data (Alam et al. 2016, Eq 21-23):
    # D_V(0.38) = 1477+-16, D_V(0.51) = 1877+-19, D_V(0.61) = 2140+-22
    print("\n--- BAO Relative Volume Distance (BOSS DR12) ---")
    dv_038 = 1477
    dv_051 = 1877
    dv_061 = 2140
    
    err_038 = 16
    err_051 = 19
    err_061 = 22
    
    # Empirical Ratios
    r1_obs = dv_051 / dv_038
    r2_obs = dv_061 / dv_038
    
    # Analytical Covariance Matrix for the ratios (due to shared denominator dv_038)
    var_r1 = (dv_051 / dv_038**2)**2 * err_038**2 + (1 / dv_038)**2 * err_051**2
    var_r2 = (dv_061 / dv_038**2)**2 * err_038**2 + (1 / dv_038)**2 * err_061**2
    cov_r1_r2 = (dv_051 * dv_061 / dv_038**4) * err_038**2
    
    cov_bao = np.array([
        [var_r1, cov_r1_r2],
        [cov_r1_r2, var_r2]
    ])
    inv_cov_bao = np.linalg.inv(cov_bao)
    
    print(f"Observed D_V(0.51)/D_V(0.38) = {r1_obs:.4f} +- {np.sqrt(var_r1):.4f}")
    print(f"Observed D_V(0.61)/D_V(0.38) = {r2_obs:.4f} +- {np.sqrt(var_r2):.4f}")
    print(f"Correlation: {cov_r1_r2 / np.sqrt(var_r1 * var_r2):.4f}")
    
    # LCDM Ratios
    dv_038_lcdm = d_v(0.38, E_lcdm, Om_frozen)
    dv_051_lcdm = d_v(0.51, E_lcdm, Om_frozen)
    dv_061_lcdm = d_v(0.61, E_lcdm, Om_frozen)
    r1_lcdm = dv_051_lcdm / dv_038_lcdm
    r2_lcdm = dv_061_lcdm / dv_038_lcdm
    
    # RefG Ratios
    dv_038_refg = d_v(0.38, E_refg, A_frozen, B_frozen)
    dv_051_refg = d_v(0.51, E_refg, A_frozen, B_frozen)
    dv_061_refg = d_v(0.61, E_refg, A_frozen, B_frozen)
    r1_refg = dv_051_refg / dv_038_refg
    r2_refg = dv_061_refg / dv_038_refg
    
    delta_lcdm = np.array([r1_obs - r1_lcdm, r2_obs - r2_lcdm])
    delta_refg = np.array([r1_obs - r1_refg, r2_obs - r2_refg])
    
    chi2_bao_lcdm = delta_lcdm.T @ inv_cov_bao @ delta_lcdm
    chi2_bao_refg = delta_refg.T @ inv_cov_bao @ delta_refg
    
    print(f"\nLCDM BAO Predictions: r1 = {r1_lcdm:.4f}, r2 = {r2_lcdm:.4f} -> Chi2 = {chi2_bao_lcdm:.2f}")
    print(f"RefG BAO Predictions: r1 = {r1_refg:.4f}, r2 = {r2_refg:.4f} -> Chi2 = {chi2_bao_refg:.2f}")
    
    # Plotting Hubble Diagram & Residuals
    z_plot = np.linspace(0.01, 1.5, 100)
    mu_lcdm_plot = mu_model(M_lcdm, z_plot, E_lcdm, Om_frozen)
    mu_refg_plot = mu_model(M_refg, z_plot, E_refg, A_frozen, B_frozen)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    
    # We use diagonal errors for visual plotting of residuals
    err_diag = np.sqrt(np.diag(cov_tot))
    
    ax1.errorbar(z_sn, mu_sn, yerr=err_diag, fmt='o', color='gray', alpha=0.6, label='Pantheon Binned SNe (DS17)')
    ax1.plot(z_plot, mu_lcdm_plot, label=f'$\Lambda$CDM ($\chi^2={chi2_lcdm:.1f}$)', linestyle='--', color='black')
    ax1.plot(z_plot, mu_refg_plot, label=f'RefG ($\chi^2={chi2_refg:.1f}$)', color='blue', linewidth=2)
    ax1.set_ylabel(r'Distance Modulus $\mu(z)$')
    ax1.set_title('Supernova Validation (Full Covariance Matrix)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    mu_mod_lcdm = mu_model(M_lcdm, z_sn, E_lcdm, Om_frozen)
    res_obs = mu_sn - mu_mod_lcdm
    mu_refg_plot_resid = mu_model(M_refg, z_plot, E_refg, A_frozen, B_frozen) - mu_lcdm_plot
    
    ax2.errorbar(z_sn, res_obs, yerr=err_diag, fmt='o', color='gray', alpha=0.6)
    ax2.plot(z_plot, np.zeros_like(z_plot), linestyle='--', color='black')
    ax2.plot(z_plot, mu_refg_plot_resid, color='blue', linewidth=2)
    ax2.set_xlabel('Redshift (z)')
    ax2.set_ylabel(r'$\Delta \mu$ (vs $\Lambda$CDM)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sn_bao_validation_fit.png')
    
    # JSON Metadata
    script_path = os.path.abspath(__file__)
    with open(script_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
        
    with open("w3_08c_results.json", "rb") as f:
        upstream_hash = hashlib.sha256(f.read()).hexdigest()
        
    res_json = {
        "model_version": "RefG_Validation_v2.0",
        "status_sn": "VALIDATION TENSION",
        "status_bao": "DIAGNOSTIC_COMPATIBILITY",
        "dataset_sn": "Pantheon Binned SN Ia (40 bins, full covariance)",
        "dataset_bao": "BOSS DR12 D_V(z) relative ratios with cov",
        "upstream_data_hash": upstream_hash,
        "models_compared": ["LCDM", "RefG"],
        "frozen_parameters": {
            "LCDM": {"Omega_m": Om_frozen},
            "RefG": {"A": A_frozen, "B": B_frozen}
        },
        "results_lcdm": {
            "optimization_success": res_lcdm.success,
            "M_offset": M_lcdm,
            "chi2_sn": chi2_lcdm,
            "chi2_bao": chi2_bao_lcdm
        },
        "results_refg": {
            "optimization_success": res_refg.success,
            "M_offset": M_refg,
            "chi2_sn": chi2_refg,
            "chi2_bao": chi2_bao_refg
        },
        "source_hash": file_hash
    }
    
    out_path = os.path.join(os.path.dirname(script_path), "w3_08d_results.json")
    with open(out_path, "w") as f:
        json.dump(res_json, f, indent=4)
        
    print("\nSaved plot to 'sn_bao_validation_fit.png' and JSON to 'w3_08d_results.json'")

if __name__ == "__main__":
    main()
