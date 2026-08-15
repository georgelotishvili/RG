import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import minimize
from scipy.integrate import quad
import sys
import os
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

def main():
    print("=== RefG Cosmology: Non-Linear Vacuum Relaxation (Joint Fit) ===\n")
    
    # Check upstream gate W3_09b
    gate_script = Path(__file__).parent / "w3_09b_nonlinear_bridge_gate.py"
    gate_path = Path(__file__).parent / "w3_09b_result.json"
    
    if gate_path.exists() and gate_script.exists():
        with open(gate_path, "r") as f:
            gate_data = json.load(f)
        script_content = gate_script.read_text('utf-8')
        computed_hash = hashlib.sha256(script_content.encode('utf-8')).hexdigest()
        
        # Strict validation checks
        is_hash_match = (gate_data.get("source_hash") == computed_hash)
        is_claim_match = (gate_data.get("claim_id") == "W3_09B_NONLINEAR_BRIDGE")
        is_status_pass = ("CONDITIONAL PASS" in gate_data.get("status", ""))
        is_consistent = gate_data.get("results", {}).get("consistency", False)
        
        if not (is_hash_match and is_claim_match and is_status_pass and is_consistent):
            print("ERROR: Upstream validation gate W3_09b FAILED (Hash, Claim, Status, or Consistency mismatch). Stopping pipeline.")
            sys.exit(1)
            
        print(f"[PRE-CHECK] Upstream Gate W3_09b (Nonlinear Bridge) verified (PASS).")
        print(f"[PRE-CHECK] True Source Hash Match: {computed_hash[:8]}...\n")
    else:
        print("ERROR: W3_09b gate not fully executed or missing. Stopping pipeline.")
        sys.exit(1)
    
    # 1. SYMBOLIC DERIVATION OF H(a, alpha)
    print("--- 1. Symbolic Derivation of Non-Linear Kinematics ---")
    P, P_ref, k0, C0, a = sp.symbols('P P_ref kappa_0 C_0 a', positive=True, real=True)
    alpha = sp.symbols('alpha', real=True) # Alpha can be negative
    
    dP_dt = -k0 * P * (P/P_ref)**alpha - C0 * a**-3
    H_expr = - (2 / (3 * P)) * dP_dt
    H_expr = sp.simplify(H_expr)
    
    P_a = P_ref * a**(-1.5)
    H_a = H_expr.subs(P, P_a)
    H_a = sp.powsimp(H_a, force=True)
    H_a = sp.expand(H_a)
    
    print("Derived H_t(a) with alpha non-linearity:")
    sp.pprint(H_a)
    print("\nNote: The coefficient of the relaxation term simplifies to A = 2/3 * kappa_0.")
    print("H_t(a) = A * a**(-1.5 * alpha) + B * a**(-1.5)\n")
    
    # 2. JOINT OBSERVATIONAL FIT (CC + SN Ia)
    print("--- 2. Joint Observational Fit (CC + Pantheon 40 Bins) ---")
    
    # Load Pantheon SN Ia
    data_url = "https://raw.githubusercontent.com/dscolnic/Pantheon/master/Binned_data/lcparam_DS17f.txt"
    local_file = "lcparam_DS17f.txt"
    if not os.path.exists(local_file):
        urllib.request.urlretrieve(data_url, local_file)
        
    z_sn = []
    mb_sn = []
    dmb_sn = []
    with open(local_file, "r") as f:
        lines = f.readlines()
        for line in lines[1:]: 
            parts = line.strip().split()
            if len(parts) > 5:
                z_sn.append(float(parts[1]))
                mb_sn.append(float(parts[4]))
                dmb_sn.append(float(parts[5]))
                
    # Data hashes for provenance
    with open(local_file, "rb") as f:
        lcparam_hash = hashlib.sha256(f.read()).hexdigest()
        
    z_sn = np.array(z_sn)
    mb_sn = np.array(mb_sn)
    err_sn = np.array(dmb_sn)
    
    sys_file = "sys_DS17f.txt"
    if not os.path.exists(sys_file):
        sys_url = "https://raw.githubusercontent.com/dscolnic/Pantheon/master/Binned_data/sys_DS17f.txt"
        urllib.request.urlretrieve(sys_url, sys_file)
        
    with open(sys_file, "r") as f:
        lines = f.readlines()
        dim = int(lines[0].strip())
        cov_sys = np.zeros((dim, dim))
        idx = 0
        for line in lines[1:]:
            cov_sys[idx//dim, idx%dim] = float(line.strip())
            idx += 1
            
    with open(sys_file, "rb") as f:
        sys_hash = hashlib.sha256(f.read()).hexdigest()
            
    cov_tot = np.diag(err_sn**2) + cov_sys
    inv_cov = np.linalg.inv(cov_tot)
    
    # CC Data
    z_cc = CC_DATA[:, 0]
    H_cc = CC_DATA[:, 1]
    err_cc = CC_DATA[:, 2]
    
    # RefG Non-Linear Model
    def H_refg_nl(z, H0, Om_A, alpha):
        a = 1.0 / (1.0 + z)
        A = H0 * Om_A
        B = H0 * (1.0 - Om_A)
        return A * a**(-1.5 * alpha) + B * a**(-1.5)
        
    def mu_refg_nl(z, H0, Om_A, alpha, M):
        integral = np.array([quad(lambda x: H0/H_refg_nl(x, H0, Om_A, alpha), 0, zz)[0] for zz in z])
        dL = (1.0 + z) * integral
        return 5.0 * np.log10(dL) + M
        
    def chi2_joint_refg(params):
        H0, Om_A, alpha, M = params
        if H0 < 50 or H0 > 100 or Om_A < 0 or Om_A > 1: return 1e10
        
        # CC Chi2
        H_mod = H_refg_nl(z_cc, H0, Om_A, alpha)
        c2_cc = np.sum(((H_cc - H_mod) / err_cc)**2)
        
        # SN Chi2
        mu_mod = mu_refg_nl(z_sn, H0, Om_A, alpha, M)
        diff = mb_sn - mu_mod
        c2_sn = diff.T @ inv_cov @ diff
        
        return c2_cc + c2_sn
        
    # LCDM Model
    def H_lcdm(z, H0, Om):
        return H0 * np.sqrt(Om * (1+z)**3 + (1-Om))
        
    def mu_lcdm(z, H0, Om, M):
        integral = np.array([quad(lambda x: H0/H_lcdm(x, H0, Om), 0, zz)[0] for zz in z])
        dL = (1.0 + z) * integral
        return 5.0 * np.log10(dL) + M
        
    def chi2_joint_lcdm(params):
        H0, Om, M = params
        if H0 < 50 or H0 > 100 or Om <= 0 or Om >= 1: return 1e10
        
        H_mod = H_lcdm(z_cc, H0, Om)
        c2_cc = np.sum(((H_cc - H_mod) / err_cc)**2)
        
        mu_mod = mu_lcdm(z_sn, H0, Om, M)
        diff = mb_sn - mu_mod
        c2_sn = diff.T @ inv_cov @ diff
        
        return c2_cc + c2_sn

    print("Fitting LCDM (Joint CC + SN)...")
    res_lcdm = minimize(chi2_joint_lcdm, [68.0, 0.3, 23.8], method='Nelder-Mead', options={'maxiter': 5000})
    chi2_tot_L = res_lcdm.fun
    H0_L, Om_L, M_L = res_lcdm.x
    
    H_mod_L = H_lcdm(z_cc, H0_L, Om_L)
    chi2_cc_L = np.sum(((H_cc - H_mod_L) / err_cc)**2)
    chi2_sn_L = chi2_tot_L - chi2_cc_L

    print("Fitting Non-Linear RefG (Joint CC + SN)...")
    res_refg = minimize(chi2_joint_refg, [68.0, 0.7, -0.05, 23.8], method='Nelder-Mead', options={'maxiter': 5000})
    chi2_tot_R = res_refg.fun
    H0_R, Om_A_R, alpha_R, M_R = res_refg.x
    
    H_mod_R = H_refg_nl(z_cc, H0_R, Om_A_R, alpha_R)
    chi2_cc_R = np.sum(((H_cc - H_mod_R) / err_cc)**2)
    chi2_sn_R = chi2_tot_R - chi2_cc_R
    
    # N total = 31 (CC) + 40 (SN) = 71
    N_tot = 71
    k_L = 3 # H0, Om, M
    k_R = 4 # H0, Om_A, alpha, M
    
    aic_L = chi2_tot_L + 2*k_L
    aic_R = chi2_tot_R + 2*k_R
    bic_L = chi2_tot_L + k_L * np.log(N_tot)
    bic_R = chi2_tot_R + k_R * np.log(N_tot)
    
    print(f"\n--- Joint Fit Results (CC + SN) ---")
    print(f"LCDM Chi2_tot: {chi2_tot_L:.2f} (CC: {chi2_cc_L:.2f}, SN: {chi2_sn_L:.2f})")
    print(f"     Params: H0 = {H0_L:.2f}, Om = {Om_L:.4f}, M = {M_L:.4f}")
    print(f"     AIC = {aic_L:.2f}, BIC = {bic_L:.2f}")
    
    print(f"\nRefG Chi2_tot: {chi2_tot_R:.2f} (CC: {chi2_cc_R:.2f}, SN: {chi2_sn_R:.2f})")
    print(f"     Params: H0 = {H0_R:.2f}, Om_A = {Om_A_R:.4f}, alpha = {alpha_R:.4f}, M = {M_R:.4f}")
    print(f"     AIC = {aic_R:.2f}, BIC = {bic_R:.2f}")
    
    print(f"\nDelta Chi2_tot (RefG - LCDM): {chi2_tot_R - chi2_tot_L:.2f}")
    print(f"Delta AIC (RefG - LCDM): {aic_R - aic_L:.2f}")
    print(f"Delta BIC (RefG - LCDM): {bic_R - bic_L:.2f}")
    
    # 3. KINEMATIC ANALYSIS (Age and q0)
    print("\n--- 3. Kinematic Analysis (Late Time limits) ---")
    # q(z=0) = -1 + (1+z)/H * dH/dz|_0
    # For RefG: H(a) = A a^{-1.5 alpha} + B a^{-1.5}
    # q(a) = -1 - (a/H) dH/da
    A_R = H0_R * Om_A_R
    B_R = H0_R * (1.0 - Om_A_R)
    
    def q_refg(a):
        H = A_R * a**(-1.5 * alpha_R) + B_R * a**(-1.5)
        dH_da = A_R * (-1.5 * alpha_R) * a**(-1.5 * alpha_R - 1) + B_R * (-1.5) * a**(-2.5)
        return -1.0 - (a / H) * dH_da
        
    q0_R = q_refg(1.0)
    
    # As a -> oo, the A_R * a^(-1.5*alpha) term dominates (since alpha < 0)
    # q -> -1 - (-1.5 * alpha_R) = -1 + 1.5 * alpha_R
    q_inf_R = -1.0 + 1.5 * alpha_R
    
    # Age of Universe in metric time (t) and internal time (tau)
    # Note: Convert H0 to Gyr^-1. 100 km/s/Mpc = 1 / 9.778 Gyr
    # t0 [Gyr] = 977.8 * integral da / (a H)
    def dt_da(a):
        return 977.8 / (a * (A_R * a**(-1.5 * alpha_R) + B_R * a**(-1.5)))
        
    def dtau_da(a):
        # dtau = Omega dt = (P/P_ref)^0.5 dt = a^-0.75 dt
        return a**(-0.75) * dt_da(a)
        
    t0_R, _ = quad(dt_da, 1e-10, 1.0)
    tau0_R, _ = quad(dtau_da, 1e-10, 1.0)
    
    t_rip_R, _ = quad(dt_da, 1.0, np.inf)
    tau_rip_R, _ = quad(dtau_da, 1.0, np.inf)
    
    def age_integrand_L(a):
        return 977.8 / (a * H_lcdm(1.0/a - 1.0, H0_L, Om_L))
    t0_L, _ = quad(age_integrand_L, 1e-10, 1.0)
    
    print(f"LCDM: Age t0 = {t0_L:.2f} Gyr, q0 = {0.5*Om_L - (1-Om_L):.3f}")
    print(f"RefG: Age t0 = {t0_R:.2f} Gyr, q0 = {q0_R:.3f}, q(a->oo) = {q_inf_R:.3f}")
    
    print("\n--- Internal vs Metric Time to Big Rip (RefG) ---")
    print(f"Past Age (Metric t): {t0_R:.2f} Gyr")
    print(f"Past Age (Internal tau): {tau0_R:.2f} Gyr")
    print(f"Future to Rip (Metric t): {t_rip_R:.2f} Gyr")
    print(f"Future to Rip (Internal tau): {tau_rip_R:.2f} Gyr")
    print(f"=> In internal time, the universe has lived ~{tau0_R/(tau0_R+tau_rip_R)*100:.1f}% of its total lifespan.")
    
    print("\nNote on Future Kinematics:")
    print("q(a->oo) < -1 indicates a Phantom Expansion regime.")
    print("This structurally predicts a 'Big Rip' at finite future time unless a late-time saturation postulate is introduced.")
    
    # 4. PLOTTING
    print("\nGenerating Joint Fit Plot...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot CC H(z)
    z_plt_cc = np.linspace(0, 2.5, 100)
    H_L_plt = H_lcdm(z_plt_cc, H0_L, Om_L)
    H_R_plt = H_refg_nl(z_plt_cc, H0_R, Om_A_R, alpha_R)
    
    ax1.errorbar(z_cc, H_cc, yerr=err_cc, fmt='o', color='gray', label='CC Data (31 pts)')
    ax1.plot(z_plt_cc, H_L_plt, 'k--', label=f'$\Lambda$CDM ($\chi^2=${chi2_cc_L:.1f})')
    ax1.plot(z_plt_cc, H_R_plt, 'b-', label=f'RefG ($\chi^2=${chi2_cc_R:.1f})')
    ax1.set_xlabel('Redshift $z$')
    ax1.set_ylabel('$H(z)$ [km/s/Mpc]')
    ax1.set_title('Cosmic Chronometers $H(z)$')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Plot SN Ia mu(z)
    z_plt_sn = np.linspace(0.01, 1.5, 100)
    mu_L_plt = mu_lcdm(z_plt_sn, H0_L, Om_L, M_L)
    mu_R_plt = mu_refg_nl(z_plt_sn, H0_R, Om_A_R, alpha_R, M_R)
    
    ax2.errorbar(z_sn, mb_sn, yerr=err_sn, fmt='.', color='gray', alpha=0.5, label='Pantheon (40 bins)')
    ax2.plot(z_plt_sn, mu_L_plt, 'k--', label=f'$\Lambda$CDM ($\chi^2=${chi2_sn_L:.1f})')
    ax2.plot(z_plt_sn, mu_R_plt, 'b-', label=f'RefG ($\chi^2=${chi2_sn_R:.1f})')
    ax2.set_xlabel('Redshift $z$')
    ax2.set_ylabel('Distance Modulus $\mu$')
    ax2.set_title('Pantheon SN Ia $\mu(z)$')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('nonlinear_joint_fit.png')
    print("Saved plot to 'nonlinear_joint_fit.png'")
    
    # Remove old outdated plot if exists
    if os.path.exists('nonlinear_sn_fit.png'):
        os.remove('nonlinear_sn_fit.png')
        
    if not res_lcdm.success or not res_refg.success:
        print("\nERROR: Optimizer failed to converge. Stopping pipeline.")
        sys.exit(1)
    
    # Save Metadata JSON
    script_path = os.path.abspath(__file__)
    with open(script_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
        
    res_json = {
        "model_version": "RefG_NonLinear_v1.0",
        "status": "JOINT_FIT_COMPLETE",
        "upstream_provenance": {
            "w3_09b_hash": computed_hash
        },
        "data_provenance": {
            "pantheon_lcparam_hash": lcparam_hash,
            "pantheon_sys_hash": sys_hash,
            "cc_data_pts": len(CC_DATA)
        },
        "results": {
            "RefG": {
                "chi2_tot": chi2_tot_R,
                "chi2_CC": chi2_cc_R,
                "chi2_SN": chi2_sn_R,
                "AIC": aic_R,
                "BIC": bic_R,
                "params": {
                    "H0": H0_R,
                    "Om_A": Om_A_R,
                    "alpha": alpha_R,
                    "M": M_R
                },
                "kinematics": {
                    "t0_Gyr": t0_R,
                    "tau0_Gyr": tau0_R,
                    "t_rip_future_Gyr": t_rip_R,
                    "tau_rip_future_Gyr": tau_rip_R,
                    "q0": q0_R,
                    "q_late": q_inf_R
                },
                "optimizer_success": res_refg.success
            },
            "LCDM": {
                "chi2_tot": chi2_tot_L,
                "chi2_CC": chi2_cc_L,
                "chi2_SN": chi2_sn_L,
                "AIC": aic_L,
                "BIC": bic_L,
                "params": {
                    "H0": H0_L,
                    "Om_m": Om_L,
                    "M": M_L
                },
                "kinematics": {
                    "t0_Gyr": t0_L,
                    "q0": 0.5*Om_L - (1-Om_L)
                },
                "optimizer_success": res_lcdm.success
            },
            "delta_AIC": aic_R - aic_L,
            "delta_BIC": bic_R - bic_L
        },
        "source_hash": file_hash
    }
    out_path = os.path.join(os.path.dirname(script_path), "w3_10_results.json")
    with open(out_path, "w") as f:
        json.dump(res_json, f, indent=4)

if __name__ == "__main__":
    main()
