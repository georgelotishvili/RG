import numpy as np
import json

def evaluate_qumond_curl_correction(M, a, b, a0, G, grid_size=300):
    """
    Numerically evaluates the QUMOND curl correction for one Miyamoto-Nagai disk.

    It builds the algebraic field on a finite axisymmetric grid, computes its
    azimuthal curl, and reconstructs the radial correction with a Biot-Savart kernel.

    QUMOND and AQUAL are distinct field formulations; this benchmark evaluates QUMOND.
    """
    from scipy.special import ellipk, ellipe
    
    # Grid setup for curl integration (concentrated on the disk)
    r_max, z_max = 20000.0, 5000.0
    r_arr = np.linspace(10.0, r_max, grid_size)
    z_arr = np.linspace(10.0, z_max, grid_size)
    dr = r_arr[1] - r_arr[0]
    dz = z_arr[1] - z_arr[0]
    
    R, Z = np.meshgrid(r_arr, z_arr, indexing='ij')
    
    # Miyamoto-Nagai Newtonian field
    sqrt_z = np.sqrt(Z**2 + b**2)
    R_MN = np.sqrt(R**2 + (a + sqrt_z)**2)
    
    gNr = - (G * M * R) / R_MN**3
    gNz = - (G * M * Z * (a + sqrt_z)) / (R_MN**3 * sqrt_z)
    gN_mag = np.sqrt(gNr**2 + gNz**2)
    
    # nu function
    nu_val = 0.5 + np.sqrt(1.0 + 4.0 * a0 / (gN_mag + 1e-15)) / 2.0
    
    gAlg_r = nu_val * gNr
    gAlg_z = nu_val * gNz
    
    # Compute Phantom Curl S_theta = d(gAlg_r)/dz - d(gAlg_z)/dr
    S_theta = np.zeros_like(gAlg_r)
    
    dgAlg_r_dz = np.zeros_like(gAlg_r)
    dgAlg_r_dz[:, 1:-1] = (gAlg_r[:, 2:] - gAlg_r[:, :-2]) / (2*dz)
    
    dgAlg_z_dr = np.zeros_like(gAlg_z)
    dgAlg_z_dr[1:-1, :] = (gAlg_z[2:, :] - gAlg_z[:-2, :]) / (2*dr)
    
    S_theta = dgAlg_r_dz - dgAlg_z_dr
    
    # We will evaluate the correction field Delta g_r at a set of observer radii
    # using the Biot-Savart Law for the "current" S_theta.
    obs_radii = np.linspace(a, 5.0 * a, 20)
    delta_g_r_obs = np.zeros_like(obs_radii)
    alg_g_r_obs = np.zeros_like(obs_radii)
    
    # S_theta exists for z > 0 and z < 0. By symmetry, the radial magnetic field B_r 
    # from a pair of current loops at +z and -z adds constructively at z=0.
    # Actually, S_theta is antisymmetric in z?
    # gNr is symmetric in z, nu is symmetric. d(gNr)/dz is antisymmetric.
    # Thus gAlg_r is symmetric, d(gAlg_r)/dz is antisymmetric.
    # gAlg_z is antisymmetric, d(gAlg_z)/dr is antisymmetric.
    # Therefore S_theta is ANTISYMMETRIC in z.
    # A current loop at +z has current +I. A loop at -z has current -I.
    # The radial magnetic field of a current loop at +z points in +r direction (if I>0, z>0).
    # The loop at -z with -I points in +r direction. They ADD constructively.
    # We just integrate over z > 0 and multiply by 2.
    
    current_I = S_theta * dr * dz
    
    for k, R_obs in enumerate(obs_radii):
        # Radial magnetic field of a current loop I at (r, z) evaluated at (R_obs, 0)
        d_sq = (R_obs + R)**2 + Z**2
        d = np.sqrt(d_sq)
        
        k_sq = 4 * R_obs * R / d_sq
        k_sq = np.clip(k_sq, 0, 0.99999) 
        
        K_ellip = ellipk(k_sq)
        E_ellip = ellipe(k_sq)
        
        # B_r = I / (2*pi) * z / (R_obs * d) * [ -K + (R_obs^2 + r^2 + z^2)/((R_obs-r)^2 + z^2) * E ]
        numerator = R_obs**2 + R**2 + Z**2
        denominator = (R_obs - R)**2 + Z**2
        factor = numerator / denominator
        
        # B_r kernel
        B_r_kernel = (1.0 / (2 * np.pi)) * (Z / (R_obs * d)) * (-K_ellip + factor * E_ellip)
        
        # Integral of S_theta * B_r_kernel over the upper half-plane, multiplied by 2 for the lower half.
        # Note: B_r kernel here acts as the Green's function for the curl correction.
        # Delta g_r = 2 * sum(I * B_r_kernel)
        delta_g_r = np.sum(current_I * B_r_kernel) * 2.0
        delta_g_r_obs[k] = delta_g_r
        
        # Exact algebraic field
        R_MN_obs = np.sqrt(R_obs**2 + (a + b)**2)
        gNr_obs = - (G * M * R_obs) / R_MN_obs**3
        gN_mag_obs = np.abs(gNr_obs)
        nu_obs = 0.5 + np.sqrt(1.0 + 4.0 * a0 / (gN_mag_obs + 1e-15)) / 2.0
        alg_g_r_obs[k] = nu_obs * gNr_obs

    # Maximum radial-acceleration correction relative to the algebraic field.
    deviation = np.abs(delta_g_r_obs) / (np.abs(alg_g_r_obs) + 1e-15)
    max_dev = np.max(deviation)
        
    return max_dev, grid_size

def formulate_qumond_disk_benchmark():
    results = {}

    # Typical parameters for a Miyamoto-Nagai disk
    G_val = 4.3009e-3 # pc (km/s)^2 / M_sun
    M_val = 1e10 # M_sun
    a_val = 3000.0 # pc (disk scale length)
    b_val = 300.0 # pc (disk scale height)
    a0_val = 1.2e-10 * 3.086e16 / 1e6 # ~3.70 (km/s)^2 / pc
    grid_size = 300
    
    print("Starting QUMOND numerical curl integration for specific MN disk...")
    max_dev, evaluated_grid_size = evaluate_qumond_curl_correction(
        M_val, a_val, b_val, a0_val, G_val, grid_size=grid_size
    )
    max_error_percent = max_dev * 100.0
    
    results["Model"] = "QUMOND curl correction for a Miyamoto-Nagai disk"
    results["Numerical_Grid"] = f"{evaluated_grid_size}x{evaluated_grid_size}"
    results["Radial_Interval"] = "a to 5a"
    results["Maximum_Radial_Acceleration_Correction_Percent"] = f"{max_error_percent:.2f}%"
    
    results["Disk_Correction_Note"] = (
        "For the stated Miyamoto-Nagai disk, the QUMOND curl correction was reconstructed "
        "from the gridded algebraic field with the axisymmetric Biot-Savart kernel. Across "
        "the radial interval a to 5a, its maximum radial-acceleration "
        f"correction is {max_error_percent:.2f}%. This is the QUMOND disk benchmark for the "
        "stated parameters."
    )

    return results

if __name__ == "__main__":
    res = formulate_qumond_disk_benchmark()
    for k,v in res.items():
        print(f"{k}: {v}")
    with open("w3_12_result.json", "w") as f:
        json.dump(res, f, indent=4)
    print("w3_12 QUMOND disk test complete.")
    for k, v in res.items():
        print(f"{k}: {v}")
