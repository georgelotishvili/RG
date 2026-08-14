import numpy as np
import json
import os
import urllib.request
import zipfile
import glob

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

def download_and_extract_sparc(data_dir="SPARC_data"):
    """
    Downloads the official SPARC database containing 175 galaxies.
    """
    url = "http://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip"
    zip_path = "Rotmod_LTG.zip"
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    if not glob.glob(os.path.join(data_dir, "*.dat")):
        print(f"Attempting to download SPARC dataset from {url}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response, open(zip_path, 'wb') as out_file:
                out_file.write(response.read())
            print("Extracting...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(data_dir)
            os.remove(zip_path)
            return True
        except Exception as e:
            print(f"Failed to download SPARC data automatically: {e}")
            print(f"ACTION REQUIRED: Please download {url} manually and extract its .dat files into {data_dir}/")
            return False
    return True

def parse_sparc_data(data_dir="SPARC_data"):
    """
    Parses SPARC .dat files, applying standard Lelli et al. (2016) quality filters.
    Computes true g_obs and g_bar in m/s^2.
    """
    # 1 pc = 3.086e16 m. 1 km/s = 1000 m/s
    kpc_to_m = 3.086e19
    kms_to_ms = 1e3
    
    g_obs_list = []
    g_bar_list = []
    
    files = glob.glob(os.path.join(data_dir, "*.dat"))
    for f in files:
        try:
            data = np.loadtxt(f, comments='#')
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
                
            R = data[:, 0] * kpc_to_m
            V_obs = data[:, 1] * kms_to_ms
            errV = data[:, 2] * kms_to_ms
            V_gas = data[:, 3] * kms_to_ms
            V_disk = data[:, 4] * kms_to_ms
            V_bulge = data[:, 5] * kms_to_ms
            
            # Quality Filters (Lelli 2016 standard cuts for empirical RAR)
            # 1. Filter out highly uncertain points (delta V / V > 10%)
            # 2. Exclude non-circular inner points (V < 20 km/s)
            rel_err = errV / np.abs(V_obs)
            quality_mask = (rel_err < 0.10) & (V_obs > 20 * kms_to_ms)
            
            data = data[quality_mask]
            if len(data) == 0:
                continue
                
            R = R[quality_mask]
            V_obs = V_obs[quality_mask]
            V_gas = V_gas[quality_mask]
            V_disk = V_disk[quality_mask]
            V_bulge = V_bulge[quality_mask]
            
            # g = V^2 / R
            g_obs = V_obs**2 / R
            
            # Baryonic Newtonian acceleration
            # Ups_disk = 0.5, Ups_bulge = 0.7
            V_bar_sq = V_gas * np.abs(V_gas) + 0.5 * V_disk * np.abs(V_disk) + 0.7 * V_bulge * np.abs(V_bulge)
            
            valid = (V_bar_sq > 0) & (R > 0) & (g_obs > 0)
            
            g_bar = V_bar_sq[valid] / R[valid]
            g_obs = g_obs[valid]
            
            g_bar_list.extend(g_bar)
            g_obs_list.extend(g_obs)
            
        except Exception:
            continue
            
    return np.array(g_bar_list), np.array(g_obs_list)

def predict_g_obs(g_bar, a0=1.2e-10):
    """RefG/MOND predictive equation derived from W(g_v, g_N)"""
    return (g_bar + np.sqrt(g_bar**2 + 4 * g_bar * a0)) / 2

def compute_residuals(g_bar, g_obs, a0=1.2e-10):
    g_obs_pred = predict_g_obs(g_bar, a0)
    return np.log10(g_obs) - np.log10(g_obs_pred)

def validate_rar():
    a0_universal = 1.2e-10 
    
    if download_and_extract_sparc():
        g_bar, g_obs = parse_sparc_data()
        print(f"Successfully loaded {len(g_bar)} quality-filtered observational points from SPARC.")
    else:
        results = {
            "dataset": "Official SPARC Database",
            "validation_status": "WAITING_FOR_DATA",
            "message": "CWRU server refused connection. Please download Rotmod_LTG.zip manually and extract to SPARC_data/"
        }
        with open("w3_11_result.json", "w") as f:
            json.dump(results, f, indent=4)
        print("w3_11 validation paused: Waiting for manual SPARC data.")
        return
        
    residuals = compute_residuals(g_bar, g_obs, a0_universal)
    rms_scatter = np.sqrt(np.mean(residuals**2))
    
    results = {
        "dataset": "Filtered SPARC Database (Lelli 2016 Cuts)",
        "n_points_analyzed": len(g_bar),
        "a0_used_m_s2": a0_universal,
        "rms_log_scatter_dex": float(rms_scatter),
        "mean_log_residual_dex": float(np.mean(residuals)),
        "validation_status": "PASS" if rms_scatter < 0.15 else "FAIL",
    }
    
    if HAS_MATPLOTLIB:
        plt.figure(figsize=(8, 6))
        plt.scatter(np.log10(g_bar), np.log10(g_obs), alpha=0.1, s=10, color='blue', label='SPARC (Quality Filtered)')
        
        g_bar_line = np.logspace(-13, -8, 100)
        g_obs_line = predict_g_obs(g_bar_line, a0_universal)
        plt.plot(np.log10(g_bar_line), np.log10(g_obs_line), 'r-', lw=2, label='RefG Derived Prediction')
        plt.plot(np.log10(g_bar_line), np.log10(g_bar_line), 'k--', lw=1, label='Newtonian Expectation')
        
        plt.xlabel(r'$\log_{10}(g_{\rm bar}) \ [\rm m/s^2]$')
        plt.ylabel(r'$\log_{10}(g_{\rm obs}) \ [\rm m/s^2]$')
        plt.title('Radial Acceleration Relation - Quality Filtered SPARC Data')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('sparc_rar_real_validation.png', dpi=150)
        print("Saved validation plot to sparc_rar_real_validation.png")
    
    with open("w3_11_result.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("w3_11 quality-filtered data validation complete.")
    for k, v in results.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    validate_rar()
