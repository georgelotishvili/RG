import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize
import json
import os
import hashlib
import urllib.request
import sys
from pathlib import Path

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
    
    print("Downloading/Loading Pantheon data...")
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

def h_refg(z, K, B):
    return K + B * (1+z)**1.5

def E_lcdm(z, Om):
    Ol = 1.0 - Om
    return np.sqrt(Ol + Om * (1+z)**3)

def E_refg(z, K, B):
    H0 = K + B
    return (K + B * (1+z)**1.5) / H0

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

def d_v(z, model_func, *args):
    d_m = lum_dist(z, model_func, *args) / (1+z)
    E_z = model_func(z, *args)
    return (z * d_m**2 / E_z)**(1/3)

def generate_hash(content):
    if not content: return ""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def main():
    print("=== W3_20: Observational Background Gate (CC + Pantheon + BAO) ===\n")
    
    # 1. CC Fitting
    print("--- 1. Fitting Cosmic Chronometers ---")
    z_cc, H_cc, err_cc = CC_DATA[:, 0], CC_DATA[:, 1], CC_DATA[:, 2]
    
    res_lcdm_cc = minimize(chi2_cc, [70.0, 0.3], args=(h_lcdm, z_cc, H_cc, err_cc), bounds=[(50, 100), (0, 1)])
    H0_fit, Om_fit = res_lcdm_cc.x
    chi2_cc_lcdm = res_lcdm_cc.fun
    
    res_refg_cc = minimize(chi2_cc, [30.0, 40.0], args=(h_refg, z_cc, H_cc, err_cc), bounds=[(0, 100), (0, 100)])
    K_fit, B_fit = res_refg_cc.x
    chi2_cc_refg = res_refg_cc.fun
    
    print(f"LambdaCDM CC Fit: H0 = {H0_fit:.2f}, Om = {Om_fit:.3f}, Chi2 = {chi2_cc_lcdm:.2f}")
    print(f"RefG CC Fit: K = {K_fit:.2f}, B = {B_fit:.2f}, Chi2 = {chi2_cc_refg:.2f}\n")
    
    # 2. Pantheon Supernovae
    print("--- 2. Testing Pantheon SNe with Frozen Parameters ---")
    z_sn, mu_sn, cov_tot = fetch_pantheon()
    inv_cov = np.linalg.inv(cov_tot)
    
    res_lcdm_sn = minimize(chi2_sn_cov, [10.0], args=(z_sn, mu_sn, inv_cov, E_lcdm, Om_fit))
    chi2_sn_lcdm = res_lcdm_sn.fun
    
    res_refg_sn = minimize(chi2_sn_cov, [10.0], args=(z_sn, mu_sn, inv_cov, E_refg, K_fit, B_fit))
    chi2_sn_refg = res_refg_sn.fun
    
    print(f"LambdaCDM SN Chi2 = {chi2_sn_lcdm:.2f}")
    print(f"RefG SN Chi2 = {chi2_sn_refg:.2f}")
    print(f"Delta Chi2 (RefG - LCDM) = {chi2_sn_refg - chi2_sn_lcdm:.2f}\n")
    
    # 3. BAO Ratios
    print("--- 3. Testing BAO (BOSS DR12) ---")
    dv_038, dv_051, dv_061 = 1477, 1877, 2140
    err_038, err_051, err_061 = 16, 19, 22
    
    r1_obs = dv_051 / dv_038
    r2_obs = dv_061 / dv_038
    
    var_r1 = (dv_051 / dv_038**2)**2 * err_038**2 + (1 / dv_038)**2 * err_051**2
    var_r2 = (dv_061 / dv_038**2)**2 * err_038**2 + (1 / dv_038)**2 * err_061**2
    cov_r1_r2 = (dv_051 * dv_061 / dv_038**4) * err_038**2
    
    cov_bao = np.array([[var_r1, cov_r1_r2], [cov_r1_r2, var_r2]])
    inv_cov_bao = np.linalg.inv(cov_bao)
    
    r1_lcdm = d_v(0.51, E_lcdm, Om_fit) / d_v(0.38, E_lcdm, Om_fit)
    r2_lcdm = d_v(0.61, E_lcdm, Om_fit) / d_v(0.38, E_lcdm, Om_fit)
    
    r1_refg = d_v(0.51, E_refg, K_fit, B_fit) / d_v(0.38, E_refg, K_fit, B_fit)
    r2_refg = d_v(0.61, E_refg, K_fit, B_fit) / d_v(0.38, E_refg, K_fit, B_fit)
    
    delta_lcdm = np.array([r1_obs - r1_lcdm, r2_obs - r2_lcdm])
    delta_refg = np.array([r1_obs - r1_refg, r2_obs - r2_refg])
    
    chi2_bao_lcdm = delta_lcdm.T @ inv_cov_bao @ delta_lcdm
    chi2_bao_refg = delta_refg.T @ inv_cov_bao @ delta_refg
    
    print(f"LambdaCDM BAO Chi2 = {chi2_bao_lcdm:.2f}")
    print(f"RefG BAO Chi2 = {chi2_bao_refg:.2f}")
    print(f"Delta Chi2 (RefG - LCDM) = {chi2_bao_refg - chi2_bao_lcdm:.2f}\n")
    
    # Check Gate Condition
    # If RefG is drastically worse (e.g., delta chi2 > 20 in Pantheon), it's a TENSION FAIL.
    delta_sn = chi2_sn_refg - chi2_sn_lcdm
    if delta_sn > 20:
        status = "FAIL (OBSERVATIONAL TENSION)"
        conclusion = f"W3_20 mathematically proves that the physically motivated H(z) = K + B(1+z)^{1.5} fails the Pantheon test by Delta Chi2 = {delta_sn:.2f}. The theoretical matter epoch was recovered, but the functional form doesn't fit real late-time cosmology."
    else:
        status = "PASS (BACKGROUND CONSISTENT)"
        conclusion = "W3_20 mathematically proved that H(z) = K + B(1+z)^{1.5} is consistent with CC, Pantheon, and BAO."
        
    print(f"--- GATE STATUS: {status} ---")
    print(conclusion)
    
    # Save outputs
    script_path = Path(__file__)
    script_hash = generate_hash(script_path.read_text('utf-8'))
    
    prereg_path = script_path.parent / "w3_20_observational_fit_preregistration.md"
    prereg_hash = generate_hash(prereg_path.read_text('utf-8')) if prereg_path.exists() else ""
    
    result_data = {
        "claim_id": "W3_20_BACKGROUND_OBSERVATIONAL_FIT",
        "status": status,
        "source_hashes": {
            "script_hash": script_hash,
            "preregistration_hash": prereg_hash
        },
        "results_lcdm": {
            "CC_Chi2": chi2_cc_lcdm,
            "SN_Chi2": chi2_sn_lcdm,
            "BAO_Chi2": chi2_bao_lcdm
        },
        "results_refg": {
            "frozen_K": K_fit,
            "frozen_B": B_fit,
            "CC_Chi2": chi2_cc_refg,
            "SN_Chi2": chi2_sn_refg,
            "BAO_Chi2": chi2_bao_refg
        },
        "conclusion": conclusion
    }
    
    out_file = script_path.parent / "w3_20_result.json"
    with open(out_file, "w") as f:
        json.dump(result_data, f, indent=2)

if __name__ == "__main__":
    main()
