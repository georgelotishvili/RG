import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize
import os
import urllib.request
import json
import hashlib

# Speed of light in km/s
c = 299792.458

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

def fetch_pantheon():
    url_lcparam = "https://raw.githubusercontent.com/dscolnic/Pantheon/master/Binned_data/lcparam_DS17f.txt"
    url_sys = "https://raw.githubusercontent.com/dscolnic/Pantheon/master/Binned_data/sys_DS17f.txt"
    
    lcparam_file = "lcparam_DS17f.txt"
    sys_file = "sys_DS17f.txt"
    
    if not os.path.exists(lcparam_file): urllib.request.urlretrieve(url_lcparam, lcparam_file)
    if not os.path.exists(sys_file): urllib.request.urlretrieve(url_sys, sys_file)
        
    z_sn, mb_sn, dmb_sn = [], [], []
    with open(lcparam_file, "r") as f:
        lines = f.readlines()
        for line in lines[1:]: 
            parts = line.strip().split()
            if len(parts) > 5:
                z_sn.append(float(parts[1]))
                mb_sn.append(float(parts[4]))
                dmb_sn.append(float(parts[5]))
                
    z_sn = np.array(z_sn)
    mb_sn = np.array(mb_sn)
    dmb_sn = np.array(dmb_sn)
    N = len(z_sn)
    
    with open(sys_file, "r") as f:
        lines = f.readlines()
        dim = int(lines[0].strip())
        cov_sys = np.zeros((dim, dim))
        idx = 0
        for line in lines[1:]:
            val = float(line.strip())
            cov_sys[idx // dim, idx % dim] = val
            idx += 1
            
    cov_tot = cov_sys.copy()
    for i in range(N):
        cov_tot[i, i] += dmb_sn[i]**2
        
    return z_sn, mb_sn, cov_tot

def h_lcdm(z, H0, Om):
    Ol = 1.0 - Om
    return H0 * np.sqrt(Ol + Om * (1+z)**3)

def E_lcdm(z, Om):
    Ol = 1.0 - Om
    return np.sqrt(Ol + Om * (1+z)**3)

def h_tau_refg(z, K, B):
    return K + B * (1+z)**1.5

def E_tau_refg(z, K, B):
    # E_tau is what integrates distance in the biconformal metric
    # H_tau(0) = K + B
    return h_tau_refg(z, K, B) / (K + B)

def chi2_cc(params, model_func, z, H, err):
    H_model = model_func(z, *params)
    return np.sum(((H - H_model) / err)**2)

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

def main():
    print("=== W3_23: Biconformal Distance Correction (CC + Pantheon) ===\n")
    
    # 1. CC Fitting
    z_cc, H_cc, err_cc = CC_DATA[:, 0], CC_DATA[:, 1], CC_DATA[:, 2]
    
    res_lcdm_cc = minimize(chi2_cc, [70.0, 0.3], args=(h_lcdm, z_cc, H_cc, err_cc), bounds=[(50, 100), (0, 1)])
    H0_fit, Om_fit = res_lcdm_cc.x
    chi2_cc_lcdm = res_lcdm_cc.fun
    
    res_refg_cc = minimize(chi2_cc, [30.0, 40.0], args=(h_tau_refg, z_cc, H_cc, err_cc), bounds=[(0, 100), (0, 100)])
    K_fit, B_fit = res_refg_cc.x
    chi2_cc_refg = res_refg_cc.fun
    
    print(f"LambdaCDM CC Fit: H0 = {H0_fit:.2f}, Om = {Om_fit:.3f}, Chi2 = {chi2_cc_lcdm:.2f}")
    print(f"RefG CC Fit (H_tau): K = {K_fit:.2f}, B = {B_fit:.2f}, Chi2 = {chi2_cc_refg:.2f}\n")
    
    # 2. Pantheon Supernovae
    z_sn, mu_sn, cov_tot = fetch_pantheon()
    inv_cov = np.linalg.inv(cov_tot)
    
    res_lcdm_sn = minimize(chi2_sn_cov, [10.0], args=(z_sn, mu_sn, inv_cov, E_lcdm, Om_fit))
    chi2_sn_lcdm = res_lcdm_sn.fun
    
    res_refg_sn = minimize(chi2_sn_cov, [10.0], args=(z_sn, mu_sn, inv_cov, E_tau_refg, K_fit, B_fit))
    chi2_sn_refg = res_refg_sn.fun
    
    print(f"LambdaCDM SN Chi2 = {chi2_sn_lcdm:.2f}")
    print(f"RefG SN Chi2 (E_tau) = {chi2_sn_refg:.2f}")
    print(f"Delta Chi2 (RefG - LCDM) = {chi2_sn_refg - chi2_sn_lcdm:.2f}\n")
    
    # 3. JWST Time availability (Theoretical Demo)
    z_f = 10.0
    z_e = 5.0
    
    def dtau_dz(z):
        H_tau_Gyr = h_tau_refg(z, K_fit, B_fit) * 1.022e-3
        return 1.0 / ((1+z)*H_tau_Gyr)

    def dt_dz(z):
        H_t_Gyr = ((1+z)**(3/7) * h_tau_refg(z, K_fit, B_fit)) * 1.022e-3
        return 1.0 / ((1+z)*H_t_Gyr)

    delta_tau, _ = quad(dtau_dz, z_e, z_f)
    delta_t, _ = quad(dt_dz, z_e, z_f)
    
    print(f"Metric time elapsed: {delta_t:.3f} Gyr")
    print(f"Structural time elapsed: {delta_tau:.3f} Gyr")
    print(f"Ratio (tau/t): {delta_tau/delta_t:.2f}\n")
    
    # Hashing data for provenance
    cc_data_bytes = CC_DATA.tobytes()
    cc_hash = hashlib.sha256(cc_data_bytes).hexdigest()
    sn_hash = hashlib.sha256(np.concatenate([z_sn, mu_sn]).tobytes()).hexdigest()
    
    # Save JSON results
    result_dict = {
        "status": "FAIL (Pantheon test failed. This specific K+B(1+z)^1.5 branch is rejected.)",
        "hypothesis": "W3_23: Biconformal Distance Integral uses H_tau",
        "provenance": {
            "cc_data_hash": cc_hash,
            "pantheon_data_hash": sn_hash
        },
        "cc_fit": {
            "lcdm_chi2": round(chi2_cc_lcdm, 2),
            "refg_chi2": round(chi2_cc_refg, 2),
            "refg_params": {"K": round(K_fit, 2), "B": round(B_fit, 2)}
        },
        "sn_pantheon_test": {
            "lcdm_chi2": round(chi2_sn_lcdm, 2),
            "refg_chi2": round(chi2_sn_refg, 2),
            "delta_chi2": round(chi2_sn_refg - chi2_sn_lcdm, 2),
            "verdict": "FAIL"
        },
        "jwst_demo": {
            "z_start": z_f,
            "z_end": z_e,
            "metric_time_gyr": round(delta_t, 3),
            "structural_time_gyr": round(delta_tau, 3),
            "ratio_tau_to_t": round(delta_tau/delta_t, 3),
            "status": "OPEN (Ratio is time-scales only; requires empirical Gamma_struct test for maturity)"
        }
    }
    
    with open('w3_23_result.json', 'w') as f:
        json.dump(result_dict, f, indent=4)
    print("Saved w3_23_result.json")

if __name__ == "__main__":
    main()
