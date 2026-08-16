import numpy as np
import matplotlib.pyplot as plt
import json

# Model Version and Constants
MODEL_VERSION = "RefG-Stationary-v1.0"
T0_Gyr = 13.793
c0_km_s = 299792.458
Mpc_to_km = 3.085677581e19
Gyr_to_s = 3.1536e16
T0_s = T0_Gyr * Gyr_to_s
T0_Mpc = T0_s * c0_km_s / Mpc_to_km  # c0 * T0 in Mpc

# Theoretical derivations from Stationary Branch Axioms
# 1. A = t/T0
# 2. p = 1/A = 1+z
# 3. c_coord = c0 * p^2 = c0 * (1+z)^2
# 4. dt = -T0 / (1+z)^2 dz

def D_M_theory(z):
    # Integral of c_coord dt
    # c_coord dt = c0 (1+z)^2 * [T0 / (1+z)^2] dz = c0 T0 dz
    # D_M = c0 T0 z
    return T0_Mpc * z

def D_L_theory(z):
    # D_L = D_M * (1+z)
    return D_M_theory(z) * (1.0 + z)

def H_CC_theory(z):
    # Standard: dt = -dz / ((1+z) H(z))
    # RefG: dt = -T0 / (1+z)^2 dz
    # Therefore: H(z) = (1+z) / T0
    # Let's return in km/s/Mpc
    # H = (1+z) / T0_s
    return (1.0 + z) / T0_s * Mpc_to_km

def F_AP_theory(z):
    # F_AP = D_A * H / c0 = (D_M / (1+z)) * H / c0
    # F_AP = (c0 T0 z / (1+z)) * ((1+z) / T0) / c0 = z
    return z

# Calculate values over redshift range
z_vals = np.linspace(0, 5, 100)
DM_vals = D_M_theory(z_vals)
DL_vals = D_L_theory(z_vals)
H_vals = H_CC_theory(z_vals)
FAP_vals = F_AP_theory(z_vals)

# Present Day Values (z=0)
H0 = H_CC_theory(0.0)

# Check assertions
assert abs(H0 - 70.9) < 0.2, f"H0 prediction failed: {H0}"
assert abs(D_M_theory(1.0) - T0_Mpc) < 0.1, "D_M linear relation failed"
assert abs(F_AP_theory(2.0) - 2.0) < 1e-5, "F_AP identity failed"

# Create JSON output
results = {
    "Model_Version": MODEL_VERSION,
    "H0_Prediction_km_s_Mpc": float(H0),
    "D_M_Relation": "c0 * T0 * z",
    "H_CC_Relation": "(1+z) / T0",
    "F_AP_Relation": "z",
    "Time_Dilation": "dt_obs / dt_emit = 1+z"
}

with open("w3_30_observables.json", "w") as f:
    json.dump(results, f, indent=4)
print("Results saved to w3_30_observables.json")
print(f"H0 Prediction: {H0:.2f} km/s/Mpc")

# Plotting against LambdaCDM for comparison
# LambdaCDM for plotting
Omega_m = 0.315
Omega_L = 1 - Omega_m
H0_lcdm = 67.4
def H_lcdm(z):
    return H0_lcdm * np.sqrt(Omega_m * (1+z)**3 + Omega_L)

from scipy.integrate import quad
def DM_lcdm(z):
    def integrand(x):
        return 1.0 / np.sqrt(Omega_m * (1+x)**3 + Omega_L)
    val, _ = quad(integrand, 0, z)
    return (c0_km_s / H0_lcdm) * val

DM_lcdm_vals = np.array([DM_lcdm(z) for z in z_vals])
DL_lcdm_vals = DM_lcdm_vals * (1+z_vals)
H_lcdm_vals = np.array([H_lcdm(z) for z in z_vals])

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(z_vals, DM_vals, 'r-', label='RefG Stationary ($D_M = cT_0z$)')
plt.plot(z_vals, DM_lcdm_vals, 'k--', label='$\Lambda$CDM')
plt.xlabel('Redshift $z$')
plt.ylabel('Comoving Distance $D_M$ (Mpc)')
plt.title('Comoving Distance')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(z_vals, H_vals, 'r-', label='RefG Stationary ($H \propto 1+z$)')
plt.plot(z_vals, H_lcdm_vals, 'k--', label='$\Lambda$CDM')
plt.xlabel('Redshift $z$')
plt.ylabel('Hubble Parameter $H(z)$ (km/s/Mpc)')
plt.title('Cosmic Chronometers')
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(z_vals, DL_vals, 'r-', label='RefG Stationary')
plt.plot(z_vals, DL_lcdm_vals, 'k--', label='$\Lambda$CDM')
plt.xlabel('Redshift $z$')
plt.ylabel('Luminosity Distance $D_L$ (Mpc)')
plt.title('Luminosity Distance (Supernovae)')
plt.legend()

plt.tight_layout()
plt.savefig('w3_30_observables.png', dpi=300)
print("Plot saved as w3_30_observables.png")
