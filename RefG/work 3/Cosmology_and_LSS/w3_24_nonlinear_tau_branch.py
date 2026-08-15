import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.integrate import quad
import os
import sys
import json
import hashlib
import urllib.request
from pathlib import Path

# Cosmic Chronometer (OHD) Data Compilation
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
        
    with open(lcparam_file, "rb") as f: lcparam_hash = hashlib.sha256(f.read()).hexdigest()
    with open(sys_file, "rb") as f: sys_hash = hashlib.sha256(f.read()).hexdigest()
        
    return z_sn, mb_sn, cov_tot, lcparam_hash, sys_hash

def main():
    print("=== W3_24: Non-Linear tau-Branch (Resolving Pantheon Tension) ===\n")
    
    # ---------------------------------------------------------
    # 1. Symbolic Derivation of H_tau(z) from dP/dtau
    # ---------------------------------------------------------
    print("--- 1. Symbolic Derivation ---")
    P, P_ref, kappa, beta, rho_m, rho_m0, A = sp.symbols('P P_ref kappa beta rho_m rho_m0 A', positive=True, real=True)
    alpha_vac = sp.symbols('alpha_vac', real=True)
    
    # Fundamental physical postulate in internal time tau
    # dP/dtau = - kappa * P * (P/P_ref)^alpha_vac - beta * P * sqrt(rho_m)
    dP_dtau = - kappa * P * (P/P_ref)**alpha_vac - beta * P * sp.sqrt(rho_m)
    
    # Geometric readout map
    # P_A = P_ref * A^(-6/7)
    P_A = P_ref * A**(-sp.Rational(6, 7))
    dP_dA = sp.diff(P_A, A)
    
    # Since H_tau = 1/A * dA/dtau, and dP/dtau = dP/dA * dA/dtau
    # H_tau = (dP/dtau) / (A * dP/dA)
    H_tau_expr = dP_dtau / (A * dP_dA)
    H_tau_expr = sp.simplify(H_tau_expr)
    
    # Substitute dependencies
    rho_A = rho_m0 * A**(-3)
    H_tau_A = H_tau_expr.subs(P, P_A).subs(rho_m, rho_A)
    H_tau_A = sp.powsimp(H_tau_A, force=True)
    H_tau_A = sp.expand(H_tau_A)
    
    print("Derived H_tau(A) from fundamental postulate:")
    sp.pprint(H_tau_A)
    print("\nSetting alpha = (4/7) * alpha_vac and z = 1/A - 1:")
    print("H_tau(z) = H0 * [ Om_A * (1+z)**(1.5*alpha) + (1-Om_A) * (1+z)**1.5 ]\n")
    
    # ---------------------------------------------------------
    # 2. Joint Observational Fit (CC + Pantheon)
    # ---------------------------------------------------------
    print("--- 2. Joint Observational Fit ---")
    print("Ontological alignment: CC measures differential galactic ages (tau), so it probes H_tau(z).")
    print("Biconformal metric sets D_L proportional to integral(dz/H_tau).")
    
    z_cc, H_cc, err_cc = CC_DATA[:, 0], CC_DATA[:, 1], CC_DATA[:, 2]
    z_sn, mb_sn, cov_tot, lcparam_hash, sys_hash = fetch_pantheon()
    inv_cov = np.linalg.inv(cov_tot)
    
    def H_tau(z, H0, Om_A, alpha):
        return H0 * (Om_A * (1+z)**(1.5*alpha) + (1.0-Om_A) * (1+z)**1.5)
        
    def mu_tau(z_array, H0, Om_A, alpha, M):
        mu = np.zeros(len(z_array))
        for i, zz in enumerate(z_array):
            integ, _ = quad(lambda x: 1.0 / H_tau(x, H0, Om_A, alpha), 0, zz)
            dL = (1.0 + zz) * integ
            mu[i] = 5.0 * np.log10(dL) + M
        return mu
        
    def chi2_joint_refg(params):
        H0, Om_A, alpha, M = params
        if H0 < 50 or H0 > 100 or Om_A < 0 or Om_A > 1: return 1e10
        
        # CC measures H_tau directly!
        H_mod = H_tau(z_cc, H0, Om_A, alpha)
        c2_cc = np.sum(((H_cc - H_mod) / err_cc)**2)
        
        # SN measures D_L via integral of 1/H_tau
        mu_mod = mu_tau(z_sn, H0, Om_A, alpha, M)
        diff = mb_sn - mu_mod
        c2_sn = diff.T @ inv_cov @ diff
        
        return c2_cc + c2_sn

    # LCDM Model for comparison
    def H_lcdm(z, H0, Om):
        return H0 * np.sqrt(Om * (1+z)**3 + (1-Om))
        
    def mu_lcdm(z_array, H0, Om, M):
        mu = np.zeros(len(z_array))
        for i, zz in enumerate(z_array):
            integ, _ = quad(lambda x: 1.0 / H_lcdm(x, H0, Om), 0, zz)
            dL = (1.0 + zz) * integ
            mu[i] = 5.0 * np.log10(dL) + M
        return mu
        
    def chi2_joint_lcdm(params):
        H0, Om, M = params
        if H0 < 50 or H0 > 100 or Om <= 0 or Om >= 1: return 1e10
        
        H_mod = H_lcdm(z_cc, H0, Om)
        c2_cc = np.sum(((H_cc - H_mod) / err_cc)**2)
        
        mu_mod = mu_lcdm(z_sn, H0, Om, M)
        diff = mb_sn - mu_mod
        c2_sn = diff.T @ inv_cov @ diff
        
        return c2_cc + c2_sn

    print("Fitting LCDM...")
    res_lcdm = minimize(chi2_joint_lcdm, [68.0, 0.3, 23.8], method='Nelder-Mead', options={'maxiter': 5000})
    chi2_tot_L = res_lcdm.fun
    H0_L, Om_L, M_L = res_lcdm.x
    
    H_mod_L = H_lcdm(z_cc, H0_L, Om_L)
    chi2_cc_L = np.sum(((H_cc - H_mod_L) / err_cc)**2)
    chi2_sn_L = chi2_tot_L - chi2_cc_L

    print("Fitting Non-Linear RefG (tau branch)...")
    res_refg = minimize(chi2_joint_refg, [68.0, 0.7, -0.05, 23.8], method='Nelder-Mead', options={'maxiter': 5000})
    chi2_tot_R = res_refg.fun
    H0_R, Om_A_R, alpha_R, M_R = res_refg.x
    
    H_mod_R = H_tau(z_cc, H0_R, Om_A_R, alpha_R)
    chi2_cc_R = np.sum(((H_cc - H_mod_R) / err_cc)**2)
    chi2_sn_R = chi2_tot_R - chi2_cc_R
    
    N_tot = len(z_cc) + len(z_sn) # 31 + 40 = 71
    k_L = 3 # H0, Om, M
    k_R = 4 # H0, Om_A, alpha, M
    
    aic_L = chi2_tot_L + 2*k_L
    aic_R = chi2_tot_R + 2*k_R
    bic_L = chi2_tot_L + k_L * np.log(N_tot)
    bic_R = chi2_tot_R + k_R * np.log(N_tot)
    
    print(f"\n--- Joint Fit Results (CC + SN) ---")
    print(f"LCDM Chi2_tot: {chi2_tot_L:.2f} (CC: {chi2_cc_L:.2f}, SN: {chi2_sn_L:.2f})")
    print(f"     AIC = {aic_L:.2f}, BIC = {bic_L:.2f}")
    
    print(f"\nRefG Chi2_tot: {chi2_tot_R:.2f} (CC: {chi2_cc_R:.2f}, SN: {chi2_sn_R:.2f})")
    print(f"     Params: H0 = {H0_R:.2f}, Om_A = {Om_A_R:.4f}, alpha = {alpha_R:.4f}, M = {M_R:.4f}")
    print(f"     AIC = {aic_R:.2f}, BIC = {bic_R:.2f}")
    
    print(f"\nDelta Chi2_tot (RefG - LCDM): {chi2_tot_R - chi2_tot_L:.2f}")
    print(f"Delta AIC (RefG - LCDM): {aic_R - aic_L:.2f}")
    
    # ---------------------------------------------------------
    # 2.5 Kinematic Analysis (q0, q_inf, t0, t_rip)
    # ---------------------------------------------------------
    print("\n--- 2.5 Kinematic Analysis (Late Time limits) ---")
    
    # H_tau(a) = H0 * [ Om_A * a**(-1.5*alpha) + (1-Om_A) * a**(-1.5) ]
    A_R = H0_R * Om_A_R
    B_R = H0_R * (1.0 - Om_A_R)
    
    def q_refg(a):
        H = A_R * a**(-1.5 * alpha_R) + B_R * a**(-1.5)
        dH_da = A_R * (-1.5 * alpha_R) * a**(-1.5 * alpha_R - 1) + B_R * (-1.5) * a**(-2.5)
        return -1.0 - (a / H) * dH_da
        
    q0_R = q_refg(1.0)
    q_inf_R = -1.0 + 1.5 * alpha_R
    
    def dtau_dA(A):
        # H_tau(A) = A_R * A**(-1.5*alpha_R) + B_R * A**(-1.5)
        # dtau/dA = 1 / (A * H_tau)
        return 977.8 / (A * (A_R * A**(-1.5 * alpha_R) + B_R * A**(-1.5)))
        
    def dt_dA(A):
        # dt = Omega^-1 dtau. Omega(A) = A**(-3/7) => Omega^-1 = A**(3/7)
        return A**(3/7) * dtau_dA(A)
        
    tau0_R, _ = quad(dtau_dA, 1e-10, 1.0)
    tau_rip_R, _ = quad(dtau_dA, 1.0, np.inf)
    
    t0_R, _ = quad(dt_dA, 1e-10, 1.0)
    t_rip_R, _ = quad(dt_dA, 1.0, np.inf)
    
    def dt_da_L(a):
        return 977.8 / (a * H_lcdm(1.0/a - 1.0, H0_L, Om_L))
    t0_L, _ = quad(dt_da_L, 1e-10, 1.0)
    
    print(f"LCDM: Age t0 = {t0_L:.2f} Gyr, q0 = {0.5*Om_L - (1-Om_L):.3f}")
    print(f"RefG: Internal Age tau0 = {tau0_R:.2f} Gyr, q0 = {q0_R:.3f}, q(a->oo) = {q_inf_R:.3f}")
    print(f"RefG: Metric Age t0 = {t0_R:.2f} Gyr")
    print(f"RefG: Future to Rip (Internal tau): {tau_rip_R:.2f} Gyr")
    print(f"RefG: Future to Rip (Metric t): {t_rip_R:.2f} Gyr")
    
    # ---------------------------------------------------------
    # 3. Generating Plots
    # ---------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    z_plt = np.linspace(0, 2.5, 100)
    H_L_plt = H_lcdm(z_plt, H0_L, Om_L)
    H_R_plt = H_tau(z_plt, H0_R, Om_A_R, alpha_R)
    
    ax1.errorbar(z_cc, H_cc, yerr=err_cc, fmt='o', color='gray', label='CC Data (31 pts)')
    ax1.plot(z_plt, H_L_plt, 'k--', label=f'$\Lambda$CDM ($\chi^2=${chi2_cc_L:.1f})')
    ax1.plot(z_plt, H_R_plt, 'b-', label=f'RefG ($\chi^2=${chi2_cc_R:.1f})')
    ax1.set_xlabel('Redshift $z$')
    ax1.set_ylabel('$H_\\tau(z)$ [km/s/Mpc]')
    ax1.set_title('Cosmic Chronometers $H(z)$')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    z_plt_sn = np.linspace(0.01, 1.5, 100)
    mu_L_plt = mu_lcdm(z_plt_sn, H0_L, Om_L, M_L)
    mu_R_plt = mu_tau(z_plt_sn, H0_R, Om_A_R, alpha_R, M_R)
    
    ax2.errorbar(z_sn, mb_sn, yerr=cov_tot.diagonal()**0.5, fmt='.', color='gray', alpha=0.5, label='Pantheon (40 bins)')
    ax2.plot(z_plt_sn, mu_L_plt, 'k--', label=f'$\Lambda$CDM ($\chi^2=${chi2_sn_L:.1f})')
    ax2.plot(z_plt_sn, mu_R_plt, 'b-', label=f'RefG ($\chi^2=${chi2_sn_R:.1f})')
    ax2.set_xlabel('Redshift $z$')
    ax2.set_ylabel('Distance Modulus $\mu$')
    ax2.set_title('Pantheon SN Ia $\mu(z)$')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('w3_24_nonlinear_tau_fit.png')
    print("\nSaved plot to 'w3_24_nonlinear_tau_fit.png'")
    
    # ---------------------------------------------------------
    # 4. Save JSON Results
    # ---------------------------------------------------------
    script_path = os.path.abspath(__file__)
    with open(script_path, "rb") as f: file_hash = hashlib.sha256(f.read()).hexdigest()
        
    res_json = {
        "status": "EXPLORATORY FIT_COMPATIBILITY (Phantom Big Rip regime, AIC favors LCDM)",
        "model_version": "RefG_NonLinear_tau_branch",
        "data_provenance": {
            "pantheon_lcparam_hash": lcparam_hash,
            "pantheon_sys_hash": sys_hash,
            "cc_data_pts": len(CC_DATA)
        },
        "results": {
            "RefG": {
                "chi2_tot": round(chi2_tot_R, 2),
                "chi2_CC": round(chi2_cc_R, 2),
                "chi2_SN": round(chi2_sn_R, 2),
                "AIC": round(aic_R, 2),
                "BIC": round(bic_R, 2),
                "params": {
                    "H0": round(H0_R, 3),
                    "Om_A": round(Om_A_R, 4),
                    "alpha": round(alpha_R, 4),
                    "M": round(M_R, 4)
                },
                "kinematics": {
                    "t0_Gyr": round(t0_R, 2),
                    "tau0_Gyr": round(tau0_R, 2),
                    "t_rip_future_Gyr": round(t_rip_R, 2),
                    "tau_rip_future_Gyr": round(tau_rip_R, 2),
                    "q0": round(q0_R, 3),
                    "q_late": round(q_inf_R, 3)
                },
                "future_stability": "FAIL/OPEN (Phantom Big Rip)",
                "jwst_maturity": "OPEN"
            },
            "LCDM": {
                "chi2_tot": round(chi2_tot_L, 2),
                "chi2_CC": round(chi2_cc_L, 2),
                "chi2_SN": round(chi2_sn_L, 2),
                "AIC": round(aic_L, 2),
                "BIC": round(bic_L, 2),
                "kinematics": {
                    "t0_Gyr": round(t0_L, 2),
                    "q0": round(0.5*Om_L - (1-Om_L), 3)
                }
            },
            "delta_AIC": round(aic_R - aic_L, 2),
            "delta_BIC": round(bic_R - bic_L, 2)
        },
        "source_hash": file_hash
    }
    out_path = os.path.join(os.path.dirname(script_path), "w3_24_result.json")
    with open(out_path, "w") as f:
        json.dump(res_json, f, indent=4)
    print(f"Saved results to {out_path}")

if __name__ == "__main__":
    main()
