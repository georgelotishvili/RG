# Preregistration: W3-28 Canonical Time Bridge

## 1. Hypothesis / Goal
To formally validate the canonical cosmological time bridge of RefG Theory, demonstrating that the universe has a finite metric age ($T_0 \approx 13.8$ Gyr) but an infinite processual past ($\tau \to -\infty$). 
The test enforces the canonical foundation: $t(\tau) = T_0 e^{\tau/T_0}$ and $\Omega = T_0 / t$.

## 2. Mathematical Formalism
- **Coordinate Metric Time ($t$):** Derived from standard observational scale factor $A$.
- **Processual Time ($\tau$):** Defined via $\tau = T_0 \ln(t / T_0)$.
- **Cadence / Pressure Map:** $\Omega = T_0 / t$ and $P = P_{\rm ref} \Omega^2$.
- **New Exponential Relaxation Law (Candidate):** $\frac{dP}{d\tau} = -\frac{2}{T_0}P$.

## 3. Strict Pass/Fail Criteria (The Gates)
1. **Gate 1 (Metric Age):** The integrated metric time $T_0$ must equal $13.8 \pm 0.1$ Gyr. [PASS/FAIL]
2. **Gate 2 (Infinite Past):** As $A \to 0$ (or $z \to \infty$), the processual time $\tau$ must diverge to $-\infty$. This is checked by verifying the analytical limit $\frac{\Delta\tau}{\Delta\ln A} \to 2T_0$ over several decades of $A$. [PASS_ANALYTIC_LIMIT]
3. **Gate 3 (Exponential Pressure Relaxation):** Numerical differentiation of $P(\tau)$ confirms the algebraic identity $dP/d\tau = -2P/T_0$ within 5% tolerance. [PASS_EXACT_ALGEBRAIC_IDENTITY, PASS_NUMERICAL_CONSISTENCY_5PCT]

## 4. Execution Plan
1. Run `w3_28_canonical_cosmology.py` with rigorous assertions.
2. Save numerical results and test statuses to `w3_28_result.json`.
3. Generate updated plots with correct labels ($P \propto \Omega^2$, handling $z=0$ logs).
