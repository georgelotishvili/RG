# Preregistration: Non-Linear tau-Branch (W3_24)

## 1. Theoretical Motivation
In RefG, the internal process time $\tau$ is tied to the evolution of the global vacuum pressure. The linear mapping $d\tau/dt = \Omega^{-1}$ (where $\Omega$ is the lapse factor $\sqrt{P/P_{\rm ref}}$) provides the bridge between standard metric time $t$ and internal cyclic time $\tau$. To resolve the Pantheon tension and accurately model the late-time acceleration, we evaluate the non-linear "tau-branch" where the universe's expansion is driven by the relaxation of the vacuum. 

The previous test (W3_08c/d) indicated that the RefG parameter $\alpha$ (which governs the relaxation rate) is unconstrained on the purely algebraic/linear branch. This test introduces the exact dynamical formulation:
$$ H_\tau(z) = H_0 [\Omega_A (1+z)^{1.5\alpha} + (1-\Omega_A)(1+z)^{1.5}] $$
Since the cosmic chronometers (CC) measure differential galactic ages (which inherently track $\tau$), the CC data natively probes $H_\tau(z)$. Supernova data (Pantheon) measures metric distance, which in the biconformal framework is proportional to the conformal integral of $dz/H_\tau$.

## 2. Methodology
1.  **Observational Datasets**: We use 31 Cosmic Chronometer data points and 40 binned Supernova (Pantheon) moduli.
2.  **Model Variables**: $H_0$, $\Omega_A$, $\alpha$ (the phantom tendency parameter), and $M$ (the absolute magnitude calibration).
3.  **Optimization**: Joint $\chi^2$ minimization using `scipy.optimize`.
4.  **Kinematics & Saturation Law**: Instead of calculating a standard "Big Rip" (which implies infinite metric tearing), the phantom-like limit $q_\infty < -1$ indicates a trajectory toward thermodynamic equilibrium. We calculate the finite time to reach complete vacuum saturation (soliton dissipation), representing the point where the universe transitions back to a uniform, unexcited background state.

## 3. Expected Outcomes
-   Determine whether the non-linear tau-branch resolves the $H(z)$ vs SN tension seen in the linear analysis.
-   Calculate the specific values for Metric Age ($t_0$) and Internal Age ($\tau_0$).
-   Evaluate the finite time remaining until absolute equilibrium (saturation).
-   Compare AIC/BIC metrics directly against the $\Lambda$CDM baseline.
