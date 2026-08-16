import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import json
import hashlib

# Model Version and Hashes
MODEL_VERSION = "RefG-Canonical-v1.0"
SOURCE_HASH = "to_be_computed_by_caller"
PREREG_HASH = "to_be_computed_by_caller"

# Canonical Constants
H0_km_s_Mpc = 67.4
H0_yr = H0_km_s_Mpc * 1.02271e-12
Omega_m = 0.315
Omega_r = 5e-5
Omega_L = 1 - Omega_m - Omega_r

def H_t(A):
    """Metric Hubble parameter."""
    return H0_yr * np.sqrt(Omega_m * A**-3 + Omega_r * A**-4 + Omega_L)

def dt_dA(A):
    if A == 0:
        return 0.0
    return 1.0 / (A * H_t(A))

# Gate 1: Metric Age
t0, _ = quad(dt_dA, 0.0, 1.0)
T0_canonical = t0

def t_metric(A):
    val, _ = quad(dt_dA, 0.0, A)
    return val

def Omega_func(A):
    return T0_canonical / t_metric(A)

def processual_time(A):
    return T0_canonical * np.log(t_metric(A) / T0_canonical)

def processual_interval(z1, z2):
    A1 = 1.0 / (1.0 + z1)
    A2 = 1.0 / (1.0 + z2)
    t1 = t_metric(A1)
    t2 = t_metric(A2)
    return T0_canonical * np.log(t2 / t1)

def metric_interval(z1, z2):
    A1 = 1.0 / (1.0 + z1)
    A2 = 1.0 / (1.0 + z2)
    return t_metric(A2) - t_metric(A1)

# Generate data for plotting and Gate 2 Limit
A_decades = np.logspace(-15, -5, 50)
tau_decades = np.array([processual_time(a) for a in A_decades])
lnA_decades = np.log(A_decades)

# Gate 2: True Asymptotic Limit Check
# d(tau)/d(ln A) -> 2T0 at early times (radiation era)
dtau_dlnA = np.gradient(tau_decades, lnA_decades)
limit_ratio = dtau_dlnA / (2 * T0_canonical)
gate2_error = np.abs(limit_ratio[0] - 1.0)

A_vals = np.logspace(-4, 0, 100)
z_vals = 1.0 / A_vals - 1.0
t_vals = np.array([t_metric(a) for a in A_vals])
tau_vals = np.array([processual_time(a) for a in A_vals])
Omega_vals = np.array([Omega_func(a) for a in A_vals])
P_vals = Omega_vals**2  

# Gate 3: Exponential Pressure Relaxation Check (Algebraic)
dP_dtau_num = np.gradient(P_vals, tau_vals)
dP_dtau_analytical = -2.0 * P_vals / T0_canonical
gate3_errors = np.abs((dP_dtau_num - dP_dtau_analytical) / dP_dtau_analytical)
max_error_gate3 = np.max(gate3_errors[1:-1])

# Assertions (Strict Gates)
assert abs(T0_canonical/1e9 - 13.793) < 0.1, f"Gate 1 Failed: T0 = {T0_canonical/1e9}"
gate1_status = "PASS"

assert gate2_error < 0.05, f"Gate 2 Limit Failed: ratio = {limit_ratio[0]}"
gate2_status = "PASS_ANALYTIC_LIMIT"

assert max_error_gate3 < 0.05, f"Gate 3 Failed: max_error = {max_error_gate3}"
gate3_status_exact = "PASS_EXACT_ALGEBRAIC_IDENTITY"
gate3_status_num = "PASS_NUMERICAL_CONSISTENCY_5PCT"

aggregate_status = "CONDITIONAL_ALGEBRAIC_DIAGNOSTIC"

print(f"Gate 1 (Metric Age 13.8 Gyr): {gate1_status} (T0 = {T0_canonical/1e9:.3f})")
print(f"Gate 2 (Infinite Past): {gate2_status} (d(tau)/dlnA approaches 2T0)")
print(f"Gate 3 (Exponential Relaxation): {gate3_status_exact}, {gate3_status_num}")

# JSON Results
results = {
    "Model_Version": MODEL_VERSION,
    "Aggregate_Status": aggregate_status,
    "Gate1_Metric_Age_Gyr": T0_canonical/1e9,
    "Gate1_Status": gate1_status,
    "Gate2_Tau_Early_Gyr": tau_decades[0]/1e9,
    "Gate2_Limit_Error": float(gate2_error),
    "Gate2_Status": gate2_status,
    "Gate3_Max_Derivative_Error": float(max_error_gate3),
    "Gate3_Status_Exact": gate3_status_exact,
    "Gate3_Status_Numerical": gate3_status_num,
    "Open_Physical_Closures": [
        "PHYSICAL_PRESSURE_DERIVATION",
        "RULER_GATE_A_a_p",
        "LIGHT_GATE_p2_CHANNEL",
        "JWST_PHYSICAL_GROWTH_dX_dtau"
    ],
    "JWST_z20_to_10_Metric_Myr_DIAGNOSTIC_ONLY": metric_interval(20, 10)/1e6,
    "JWST_z20_to_10_Processual_Gyr_DIAGNOSTIC_ONLY": processual_interval(20, 10)/1e9,
    "JWST_z50_to_10_Processual_Gyr_DIAGNOSTIC_ONLY": processual_interval(50, 10)/1e9,
    "Hashes": {
        "Source_Hash": SOURCE_HASH,
        "Prereg_Hash": PREREG_HASH
    }
}

with open("w3_28_result.json", "w") as f:
    json.dump(results, f, indent=4)
print("Results saved to w3_28_result.json")

# Plotting
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(z_vals + 1, t_vals/1e9, label='Metric Time $t$ (Gyr)', color='blue')
plt.plot(z_vals + 1, tau_vals/1e9, label='Processual Time $\\tau$ (Gyr)', color='red')
plt.xscale('log')
plt.gca().invert_xaxis()
plt.xlabel('Redshift $z+1$')
plt.ylabel('Time (Gyr)')
plt.title('Canonical Time Bridge: $t$ vs $\\tau$')
plt.axhline(0, color='black', linestyle='--')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(tau_vals/1e9, P_vals, label='$P / P_{ref}$', color='purple')
plt.yscale('log')
plt.xlabel('Processual Time $\\tau$ (Gyr)')
plt.ylabel('Pressure $P / P_{ref}$')
plt.title('Exponential Pressure Relaxation: $dP/d\\tau = -2P/T_0$')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('w3_28_canonical_bridge.png', dpi=300)
print("Plot saved as w3_28_canonical_bridge.png")
