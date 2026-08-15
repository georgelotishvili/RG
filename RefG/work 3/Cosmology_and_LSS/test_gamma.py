import numpy as np
from scipy.integrate import quad

def main():
    H0 = 69.0
    Om_A = 0.45
    alpha = -0.67
    
    def H_tau(z):
        return H0 * (Om_A * (1+z)**(1.5*alpha) + (1.0-Om_A) * (1+z)**1.5)
        
    def dtau_dz(z):
        return 977.8 / ((1+z) * H_tau(z))
        
    def effective_maturity_time(z):
        # Gamma_struct enhancement relative to tau is sqrt(M) = (1+z)^{3/7}
        return (1+z)**(3/7) * dtau_dz(z)
        
    tau_age, _ = quad(dtau_dz, 10, np.inf)
    eff_age, _ = quad(effective_maturity_time, 10, np.inf)
    
    print(f"tau_age at z=10: {tau_age:.3f} Gyr")
    print(f"Effective maturity age at z=10: {eff_age:.3f} Gyr")

if __name__ == "__main__":
    main()
