import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize
import os
import urllib.request
import json

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

def h_t_refg(z, K, B):
    return (1+z)**(3/7) * h_tau_refg(z, K, B)

def E_t_refg(z, K, B):
    # E(z) = H_t(z) / H_t(0)
    # H_t(0) = 1 * (K + B)
    return h_t_refg(z, K, B) / (K + B)

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
    print("=== W3_22: CORRECTED Observational Background Gate (CC + Pantheon) ===\n")
    
    # 1. CC Fitting
    print("--- 1. Fitting Cosmic Chronometers ---")
    z_cc, H_cc, err_cc = CC_DATA[:, 0], CC_DATA[:, 1], CC_DATA[:, 2]
    
    res_lcdm_cc = minimize(chi2_cc, [70.0, 0.3], args=(h_lcdm, z_cc, H_cc, err_cc), bounds=[(50, 100), (0, 1)])
    H0_fit, Om_fit = res_lcdm_cc.x
    chi2_cc_lcdm = res_lcdm_cc.fun
    
    # Fit RefG to CC data using H_tau!
    res_refg_cc = minimize(chi2_cc, [30.0, 40.0], args=(h_tau_refg, z_cc, H_cc, err_cc), bounds=[(0, 100), (0, 100)])
    K_fit, B_fit = res_refg_cc.x
    chi2_cc_refg = res_refg_cc.fun
    
    print(f"LambdaCDM CC Fit: H0 = {H0_fit:.2f}, Om = {Om_fit:.3f}, Chi2 = {chi2_cc_lcdm:.2f}")
    print(f"RefG CC Fit (H_tau): K = {K_fit:.2f}, B = {B_fit:.2f}, Chi2 = {chi2_cc_refg:.2f}\n")
    
    # 2. Pantheon Supernovae
    print("--- 2. Testing Pantheon SNe with Frozen Parameters ---")
    z_sn, mu_sn, cov_tot = fetch_pantheon()
    inv_cov = np.linalg.inv(cov_tot)
    
    res_lcdm_sn = minimize(chi2_sn_cov, [10.0], args=(z_sn, mu_sn, inv_cov, E_lcdm, Om_fit))
    chi2_sn_lcdm = res_lcdm_sn.fun
    M_lcdm = res_lcdm_sn.x[0]
    
    # Test RefG SN using E_t!
    res_refg_sn = minimize(chi2_sn_cov, [10.0], args=(z_sn, mu_sn, inv_cov, E_t_refg, K_fit, B_fit))
    chi2_sn_refg = res_refg_sn.fun
    M_refg = res_refg_sn.x[0]
    
    print(f"LambdaCDM SN Chi2 = {chi2_sn_lcdm:.2f}")
    print(f"RefG SN Chi2 (E_t) = {chi2_sn_refg:.2f}")
    print(f"Delta Chi2 (RefG - LCDM) = {chi2_sn_refg - chi2_sn_lcdm:.2f}\n")
    
    # 3. JWST time calculations
    print("--- 3. JWST Time availability (z=10 to z=5) ---")
    z_f = 10.0
    z_e = 5.0
    
    def dtau_dz(z):
        # dtau = dz / ((1+z)*H_tau)
        H_tau_Gyr = h_tau_refg(z, K_fit, B_fit) * 1.022e-3
        return 1.0 / ((1+z)*H_tau_Gyr)

    def dt_dz(z):
        # dt = dz / ((1+z)*H_t)
        H_t_Gyr = h_t_refg(z, K_fit, B_fit) * 1.022e-3
        return 1.0 / ((1+z)*H_t_Gyr)

    delta_tau, _ = quad(dtau_dz, z_e, z_f)
    delta_t, _ = quad(dt_dz, z_e, z_f)
    
    print(f"Metric time elapsed: {delta_t:.3f} Gyr")
    print(f"Structural time elapsed: {delta_tau:.3f} Gyr")
    print(f"Ratio (tau/t): {delta_tau/delta_t:.2f}\n")
    
    # Plotting Hubble Parameters
    z_plot = np.linspace(0, 2.5, 100)
    plt.figure(figsize=(10, 6))
    plt.plot(z_plot, h_lcdm(z_plot, H0_fit, Om_fit), label=r'$\Lambda$CDM', color='black', linestyle=':')
    plt.plot(z_plot, h_tau_refg(z_plot, K_fit, B_fit), label=r'RefG $H_\tau(z)$ (CC)', color='red', linewidth=2)
    plt.plot(z_plot, h_t_refg(z_plot, K_fit, B_fit), label=r'RefG $H_t(z)$ (Metric)', color='blue', linestyle='--')
    plt.errorbar(z_cc, H_cc, yerr=err_cc, fmt='o', color='gray', alpha=0.5, label='Cosmic Chronometers')
    
    plt.xlabel('Redshift $z$', fontsize=14)
    plt.ylabel(r'$H(z)$ [km/s/Mpc]', fontsize=14)
    plt.title('RefG W3_22: Corrected Observational Fits', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('w3_22_hubble_rates.png', dpi=300)
    
    # Plot SN residuals
    plt.figure(figsize=(10, 6))
    mu_lcdm = mu_model(M_lcdm, z_sn, E_lcdm, Om_fit)
    mu_refg = mu_model(M_refg, z_sn, E_t_refg, K_fit, B_fit)
    
    # Plot residuals relative to LCDM
    plt.errorbar(z_sn, mu_sn - mu_lcdm, yerr=np.sqrt(np.diag(cov_tot)), fmt='o', color='gray', alpha=0.3, markersize=3)
    plt.plot(z_sn, mu_refg - mu_lcdm, 'ro', markersize=2, label='RefG Model (Metric)')
    plt.axhline(0, color='black', linestyle='--')
    plt.xscale('log')
    plt.xlabel('Redshift $z$')
    plt.ylabel(r'$\Delta \mu$ (Data - $\Lambda$CDM)')
    plt.title('SN Ia Hubble Diagram Residuals')
    plt.legend()
    plt.savefig('w3_22_sn_residuals.png', dpi=300)

if __name__ == "__main__":
    main()
