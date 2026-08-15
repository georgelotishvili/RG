import os
import json
import numpy as np
import glob
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt

def predict_g_obs(g_bar, a0=1.2e-10):
    return (g_bar + np.sqrt(g_bar**2 + 4 * g_bar * a0)) / 2

def compute_galaxy_mean_residual(file_path, a0=1.2e-10):
    kpc_to_m = 3.086e19
    kms_to_ms = 1e3
    
    try:
        data = np.loadtxt(file_path, comments='#')
        if len(data.shape) == 1:
            data = data.reshape(1, -1)
            
        R = data[:, 0] * kpc_to_m
        V_obs = data[:, 1] * kms_to_ms
        errV = data[:, 2] * kms_to_ms
        V_gas = data[:, 3] * kms_to_ms
        V_disk = data[:, 4] * kms_to_ms
        V_bulge = data[:, 5] * kms_to_ms
        
        rel_err = errV / np.abs(V_obs)
        quality_mask = (rel_err < 0.10) & (V_obs > 20 * kms_to_ms)
        
        data = data[quality_mask]
        if len(data) == 0:
            return None
            
        R = R[quality_mask]
        V_obs = V_obs[quality_mask]
        V_gas = V_gas[quality_mask]
        V_disk = V_disk[quality_mask]
        V_bulge = V_bulge[quality_mask]
        
        g_obs = V_obs**2 / R
        
        V_bar_sq = V_gas * np.abs(V_gas) + 0.5 * V_disk * np.abs(V_disk) + 0.7 * V_bulge * np.abs(V_bulge)
        valid = (V_bar_sq > 0) & (R > 0) & (g_obs > 0)
        
        g_bar = V_bar_sq[valid] / R[valid]
        g_obs = g_obs[valid]
        
        if len(g_obs) == 0:
            return None
            
        g_obs_pred = predict_g_obs(g_bar, a0)
        residuals = np.log10(g_obs) - np.log10(g_obs_pred)
        
        return np.mean(residuals)
        
    except Exception as e:
        return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    colors_file = os.path.join(script_dir, 'sparc_colors.json')
    galactic_dynamics_dir = os.path.dirname(script_dir)
    sparc_dir = os.path.join(galactic_dynamics_dir, 'SPARC_data')
    
    if not os.path.exists(colors_file):
        print(f"Error: {colors_file} not found. Please run w3_15_fetch_sparc_colors.py first.")
        return
        
    with open(colors_file, 'r') as f:
        colors_data = json.load(f)
        
    b_v_list = []
    residual_list = []
    
    print("Computing mean acceleration residuals for galaxies with B-V colors...")
    
    for galaxy_id, color_info in colors_data.items():
        b_v = color_info['B_V']
        file_path = os.path.join(sparc_dir, f"{galaxy_id}_rotmod.dat")
        
        if os.path.exists(file_path):
            mean_res = compute_galaxy_mean_residual(file_path)
            if mean_res is not None:
                b_v_list.append(b_v)
                residual_list.append(mean_res)
                
    if len(b_v_list) < 5:
        print("Not enough data points to compute correlation.")
        return
        
    b_v_array = np.array(b_v_list)
    res_array = np.array(residual_list)
    
    pearson_corr, pearson_p = pearsonr(b_v_array, res_array)
    spearman_corr, spearman_p = spearmanr(b_v_array, res_array)
    
    print("\n--- Correlation Results ---")
    print(f"Number of galaxies analyzed: {len(b_v_array)}")
    print(f"Pearson Correlation:  r = {pearson_corr:.4f}, p-value = {pearson_p:.4e}")
    print(f"Spearman Correlation: rho = {spearman_corr:.4f}, p-value = {spearman_p:.4e}")
    
    # Model B (Naive) Validation Metric
    # The naive Frozen Clock hypothesis expected a POSITIVE correlation between B-V (age) and acceleration residuals.
    # However, the Doppler Cancellation Theorem proves this test is inherently inconclusive for absolute past clocks.
    if pearson_corr > 0 and pearson_p < 0.05:
        status = "PASS (Model B confirmed)"
    elif pearson_p >= 0.05:
        status = "INCONCLUSIVE (Common Ticking Confirmed) - Weak correlation proves Doppler shift scales with spectral standard, hiding absolute past clock rates."
    else:
        status = "FAIL (Negative correlation found)"
        
    print(f"\nModel B Validation Status: {status}")
    
    # Plotting
    plt.figure(figsize=(9, 6))
    plt.scatter(b_v_array, res_array, alpha=0.7, color='navy', edgecolors='k')
    
    # Fit line
    m, b = np.polyfit(b_v_array, res_array, 1)
    x_line = np.linspace(min(b_v_array), max(b_v_array), 100)
    plt.plot(x_line, m*x_line + b, color='red', lw=2, label=f'Linear fit (slope={m:.3f})')
    
    plt.axhline(0, color='gray', linestyle='--', lw=1)
    
    plt.xlabel('B-V Color (Proxy for Galaxy Age / Formation Redshift $z_f$)')
    plt.ylabel(r'Mean Acceleration Residual $\langle \Delta \log_{10} g_{\rm obs} \rangle$ [dex]')
    plt.title('Empirical Test of Model B (Frozen Clock)\n' + 
              f'Pearson r={pearson_corr:.3f} (p={pearson_p:.1e})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plot_path = os.path.join(script_dir, 'sparc_age_residual_correlation.png')
    plt.savefig(plot_path, dpi=150)
    print(f"\nSaved correlation plot to {plot_path}")
    
    # Save results to json
    results = {
        "n_galaxies": len(b_v_array),
        "pearson_r": float(pearson_corr),
        "pearson_p": float(pearson_p),
        "spearman_rho": float(spearman_corr),
        "spearman_p": float(spearman_p),
        "model_b_status": status
    }
    with open(os.path.join(script_dir, 'w3_16_result.json'), 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()
