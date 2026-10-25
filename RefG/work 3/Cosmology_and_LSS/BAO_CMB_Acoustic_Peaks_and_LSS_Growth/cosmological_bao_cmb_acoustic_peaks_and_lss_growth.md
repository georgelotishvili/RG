# Cosmological Sound Horizon ($r_s, r_d$), BAO $100\,h^{-1}\text{ Mpc}$ Standard Ruler, CMB Acoustic Peaks ($\theta_*, \ell_A, \ell_1, \ell_2, \ell_3$), and Linear Perturbation Growth ($D_+(A), \gamma = 6/11, f\sigma_8(z)$) on the $A = a/p = a^{5/2}$ Operational Geometry

- **Gate ID:** `REFG_COSMOLOGICAL_BAO_CMB_ACOUSTIC_PEAKS_AND_LSS_GROWTH_V1`
- **Status:** `PASS` (`19/19` verification checks passed)
- **Verifier Script:** `verify_cosmological_bao_cmb_acoustic_peaks_and_lss_growth.py` (`SHA-256: ed5b07996a4240823d8e9ffd5c75fda31f0380dfa6cd8074cd12aeae980d2c5a`)
- **Result Artifact:** `cosmological_bao_cmb_acoustic_peaks_and_lss_growth_result.json` (`SHA-256: 44e77ffa2a1ffed3a412bbee3090a7a710270bc1d7cfed612fe6712d0af0cdc0`)
- **Monograph Sections Closed:** §3.3 (Cosmological Scale: Foundation Expansion and Internal Readout), §6.4.2.3 (Falsification Criterion 2.3: CMB Anisotropy, BAO $100\,h^{-1}\text{ Mpc}$ Standard Ruler, and LSS Growth), and Research Program Status Item 10.

---

## 1. Operational Scale Reconstruction, Exact Volume Jacobian $\widehat{n}_{C,\rm op} = p^3\widehat{n}_{C,F} = A^{-3}$, and the Cold Collective Phase-Source Background

### Theorem 1.1 (Unique Scale Inversion and Volume Jacobian on the Homogeneous Post-Genesis Branch)
On the post-Genesis homogeneous, isotropic, network-comoving $d=3$ branch of Refractive Gravity, the neutral collective phase state $\Psi_C = \sqrt{n_{C,F}}\,e^{i\theta_C}$ conserves the total Noether phase charge $Q_C$ inside any fixed comoving foundation domain ($\mathcal{V}/\mathcal{V}_0 = a^3$):
$$
\frac{Q_C}{Q_{C,0}} = \eta_F(a)\,a^3 = 1 \quad\Longrightarrow\quad \eta_F(a) \equiv \frac{\langle n_{C,F}\rangle}{\langle n_{C,F}\rangle_0} = a^{-3}.
$$
Combined with the constitutive pressure-cadence relations $P_F/P_{F,0} = \eta_F = a^{-3}$ and $p = \sqrt{P_F/P_{F,0}} = a^{-3/2}$, the internal operational scale factor $A \equiv a/p$ and its inverse reconstruction are uniquely fixed without free exponents:
$$
A(a) = \frac{a}{p} = a^{5/2}, \qquad a(A) = A^{2/5}, \qquad p(A) = A^{-3/5}, \qquad \frac{P_F(A)}{P_{F,0}} = \eta_F(A) = A^{-6/5}.
$$
The exact volume Jacobian between the operational number density $\widehat{n}_{C,\rm op} \equiv n_{C,\rm op}/n_{C,\rm op,0}$ and the foundation number density $\widehat{n}_{C,F} \equiv n_{C,F}/n_{C,F,0} = \eta_F$ of the **same** conserved Noether charge $Q_C$ is:
$$
\widehat{n}_{C,\rm op}(A) = p(A)^3\,\widehat{n}_{C,F}(A) = \bigl(A^{-3/5}\bigr)^3 A^{-6/5} = A^{-9/5 - 6/5} = A^{-3}.
$$
On the cold Thomas–Fermi branch ($\rho_C(n_{C,\rm op}) = \mu_{C0}\,n_{C,\rm op}$), the thermodynamic pressure, adiabatic sound speed squared, and anisotropic stress vanish identically:
$$
p_C = n_{C,\rm op}\rho_C'(n_{C,\rm op}) - \rho_C(n_{C,\rm op}) \equiv 0, \qquad c_{s,C}^2 = \frac{p_C'}{\rho_C'} \equiv 0, \qquad \sigma_C \equiv 0,
$$
so $T^C_{\mu\nu} = \rho_{C0} A^{-3} u_\mu u_\nu$ acts in both the background Friedmann equations and linear scalar perturbation equations as an exact pressureless, irrotational cold Einstein source without introducing a separate dark-matter particle species.

### Theorem 1.2 (Matter–Radiation Equality, Process-Time vs. Coordinate-Time Age, and Cosmological–Galactic Acceleration Lock)
With $1 + z = A^{-1}$, $d\tau = p(A)\,dt = A^{-3/5}dt$, CODATA 2022 fundamental constants, $T_{\rm CMB,0} = 2.7255\text{ K}$, $N_{\rm eff} = 3.044$, and Planck 2018 fiducial parameters ($\omega_b = 0.02237$, $\omega_c \equiv \Omega_{C0}h^2 = 0.1200$, $\omega_\nu = 0.0006442$, $h = 0.6736$):
1. **Radiation and Matter Density Parameters:**
   $$
   \omega_\gamma = 2.4730\times 10^{-5}, \qquad \omega_r = \omega_\gamma\!\left[1 + \frac{7}{8}\!\left(\frac{4}{11}\right)^{4/3}\!N_{\rm eff}\right] = 4.1826\times 10^{-5}, \qquad \Omega_{r0} = 9.2181\times 10^{-5},
   $$
   $$
   \Omega_{b0} = 0.04930, \qquad \Omega_{C0} = 0.26447, \qquad \Omega_{m0,\rm early} = 0.31377, \qquad \Omega_{m0,\rm late} = 0.31519, \qquad \Omega_{\Lambda 0} = 0.68472.
   $$
2. **Matter–Radiation Equality ($z_{\rm eq}$):**
   $$
   A_{\rm eq} = \frac{\omega_r}{\omega_b + \omega_c} = 2.9378\times 10^{-4} \quad\Longrightarrow\quad z_{\rm eq}^{\rm RefG} = A_{\rm eq}^{-1} - 1 = 3402.88,
   $$
   matching the Planck 2018 determination $z_{\rm eq} = 3402 \pm 26$ to **$0.034\sigma$**, with hidden foundation scale $a_F(z_{\rm eq}) = A_{\rm eq}^{2/5} = 0.03866$ and material cadence factor $p(z_{\rm eq}) = A_{\rm eq}^{-3/5} = 131.58$.
3. **Foundation Coordinate Expansion Age ($t_0$) vs. Accumulated Process-Time Age ($\tau_0$) and JWST Early Maturity:**
   Extrapolating today's constant clock rate ($p_0 = 1$, $dt = \frac{dA}{A H_0 E(A)}$) gives the standard coordinate/expansion age $t_0$, whereas multiplying each expansion interval by the higher early-epoch cadence factor $p(A) = A^{-3/5} = (1+z)^{3/5} > 1$ ($d\tau = p(A)\,dt = A^{-3/5}dt$, where $p(t) \propto t^{-2/5}$ in the matter era is strictly integrable as $t \to 0$) yields the significantly larger accumulated material process history $\tau(z) > t(z)$:
   $$
   t_0 = \frac{1}{H_0}\int_0^1 \frac{dA}{A\,E(A)} = 13.7965\text{ Gyr} \quad (\text{Planck 2018: } 13.787 \pm 0.020\text{ Gyr}),
   $$
   $$
   \tau_0 = \int_0^{t_0} p(t)\,dt = \frac{1}{H_0}\int_0^1 \frac{p(A)\,dA}{A\,E(A)} = \frac{1}{H_0}\int_0^1 \frac{A^{-8/5}\,dA}{E(A)} = 24.5795\text{ Gyr} \quad (\tau_0 / t_0 = 1.7816).
   $$
   At high redshifts observed by JWST, the higher early foundation pressure $P_F/P_{F,0} = (1+z)^{6/5}$ accelerates internal material cycles ($p(z) = (1+z)^{3/5}$), providing several billion years of accumulated process time for stellar and chemical maturation within a short coordinate expansion interval:
   - At **$z = 10$** ($A = 1/11$, $p(10) = 4.215$): $t(10) = 470.2\text{ Myr}$, whereas **$\tau(10) = 3.2766\text{ Gyr}$** ($\tau/t = 6.97\times$);
   - At **$z = 13$** ($A = 1/14$, $p(13) = 4.872$): $t(13) = 327.2\text{ Myr}$, whereas **$\tau(13) = 2.6305\text{ Gyr}$** ($\tau/t = 8.04\times$).
4. **Cosmological–Galactic Acceleration Scale Lock:**
   The present-epoch foundation pressure relaxation rate $\Gamma_{P,0} = -\left.\frac{1}{P_F}\frac{dP_F}{d\tau}\right|_0 = \frac{6}{5}H_0$ fixes the galactic transition acceleration without free parameters:
   $$
   a_0^{\rm (RefG)} = \frac{\Gamma_{P,0} c_0}{2\pi} = \frac{3}{5\pi}c_0 H_0 = 1.2499\times 10^{-10}\text{ m s}^{-2},
   $$
   within $+4.16\%$ of the empirical SPARC calibration $a_0 = 1.20\times 10^{-10}\text{ m s}^{-2}$.

---

## 2. Exact Comoving Sound Horizon $r_s(z_*)$, Drag-Epoch BAO Standard Ruler $r_d \approx 100\,h^{-1}\text{ Mpc}$, and CMB Acoustic Peaks

### Theorem 2.1 (Exact Analytical Logarithmic Law for the Comoving Sound Horizon $r_s(z)$)
Prior to recombination, the tightly coupled baryon–photon plasma on the operational metric $g_{\rm op}$ has momentum density ratio and adiabatic sound speed:
$$
R_b(A) \equiv \frac{3\rho_b(A)}{4\rho_\gamma(A)} = \frac{3\omega_b}{4\omega_\gamma}\,A \equiv R_{b0}\,A \quad (R_{b0} = 678.434), \qquad c_s(A) = \frac{c_0}{\sqrt{3\bigl(1 + R_b(A)\bigr)}}.
$$
The comoving sound horizon at operational scale $A = (1+z)^{-1}$ is given by the quadrature integral
$$
r_s(z) = \int_0^{(1+z)^{-1}} \frac{c_s(A)}{A^2 H_A(A)}\,dA = \frac{c_0}{H_0\sqrt{3}}\int_0^{(1+z)^{-1}} \frac{dA}{\sqrt{(1 + R_{b0} A)\bigl(\Omega_{r0} + \Omega_{m0} A + \Omega_{\Lambda 0} A^4\bigr)}}.
$$
Because $\Omega_{\Lambda 0} A^4 < 10^{-9}$ for $z > 1000$, omitting $\Omega_{\Lambda 0} A^4$ in the pre-recombination era yields the **exact closed-form logarithmic sound horizon law**:
$$
r_s^{\rm (analyt)}(z) = \frac{2 c_0}{H_0\sqrt{3\,\Omega_{m0}\,R_{b0}}}\,\ln\!\left(\frac{\sqrt{1 + R_b(A)} + \sqrt{R_b(A) + R_b(A_{\rm eq})}}{1 + \sqrt{R_b(A_{\rm eq})}}\right), \qquad A = (1+z)^{-1}, \quad A_{\rm eq} = \frac{\Omega_{r0}}{\Omega_{m0}}.
$$
Numerical evaluation confirms that $r_s^{\rm (analyt)}(z)$ agrees with the full numerical quadrature including $\Omega_{\Lambda 0} A^4$ to **$1.10\times 10^{-10}$** relative accuracy at recombination ($z_* = 1089.92$) and **$1.20\times 10^{-10}$** at the baryon drag epoch ($z_d = 1059.94$):

| Quantity | RefG Numerical Quadrature | RefG Exact Analytical Formula | Planck 2018 / Observational Benchmark | Relative Error |
| :--- | :---: | :---: | :---: | :---: |
| Recombination redshift $z_*$ | $1089.92$ (HS96: $1091.91$) | $1089.92$ | $1089.92 \pm 0.25$ | $0.00\%$ ($0.18\%$) |
| Foundation & cadence at $z_*$ | $a_F(z_*) = 0.06094$, $p(z_*) = 66.48$ | $\eta_F(z_*) = 4419.28$ | — | Exact inversion |
| Sound speed $c_s(z_*)/c_0$ | $0.45334$ ($R_b(z_*) = 0.6219$) | $0.45334$ | $0.4533$ | $<0.01\%$ |
| Recombination sound horizon $r_s(z_*)$ | **$144.29\text{ Mpc}$** | **$144.29\text{ Mpc}$** | $144.43 \pm 0.26\text{ Mpc}$ | **$0.099\%$** |
| Drag-epoch redshift $z_d$ | $1059.94$ (HS96: $1063.41$) | $1059.94$ | $1059.94 \pm 0.30$ | $0.00\%$ ($0.33\%$) |
| Drag-epoch BAO ruler $r_d \equiv r_s(z_d)$ | **$146.94\text{ Mpc}$** ($146.63\text{ Mpc}$) | **$146.94\text{ Mpc}$** | $147.09 \pm 0.26\text{ Mpc}$ | **$0.100\%$** |
| BAO ruler in $h^{-1}\text{ Mpc}$ | **$98.98\,h^{-1}\text{ Mpc} \approx 100\,h^{-1}\text{ Mpc}$** | **$98.98\,h^{-1}\text{ Mpc}$** | $\simeq 100\,h^{-1}\text{ Mpc}$ (SDSS/BOSS/DESI) | **$0.10\%$** |

### Theorem 2.2 (CMB Acoustic Scale $\theta_*$, Fundamental Multipole $\ell_A$, and First Three Acoustic Peaks)
The comoving angular diameter distance to the recombination surface on the operational $A$-geometry is:
$$
D_M(z_*) = \frac{c_0}{H_0}\int_{(1+z_*)^{-1}}^1 \frac{dA}{A^2 E(A)} = 13869.09\text{ Mpc},
$$
which determines the acoustic angular scale $\theta_*$ and fundamental multipole spacing $\ell_A$:
$$
100\theta_* \equiv 100\,\frac{r_s(z_*)}{D_M(z_*)} = 1.04035 \quad (\text{Planck 2018: } 1.04110 \pm 0.00031, \text{ diff } 0.072\%),
$$
$$
\ell_A \equiv \frac{\pi}{\theta_*} = 301.97 \quad (\text{Planck 2018: } 301.76 \pm 0.09, \text{ diff } 0.071\%).
$$
With the radiation-driving acoustic phase shifts $\ell_m = \ell_A(m - \phi_m)$ ($\phi_1 = 0.267(r_*/0.30)^{0.1} = 0.26865$ where $r_* \equiv \rho_r(z_*)/\rho_m(z_*) = 0.31905$, $\phi_2 = 0.2185$, $\phi_3 = 0.3125$; Hu et al. 2001; Doran & Lilley 2002), the locations of the first three CMB temperature acoustic peaks are:
- **1st Peak ( fundamental compression):** $\ell_1^{\rm RefG} = 220.85$ vs. Planck observed $\ell_1^{\rm obs} = 220.0 \pm 0.5$ (**$0.39\%$** error);
- **2nd Peak (1st rarefaction):** $\ell_2^{\rm RefG} = 537.97$ vs. Planck observed $\ell_2^{\rm obs} = 537.5 \pm 0.7$ (**$0.087\%$** error);
- **3rd Peak (2nd compression):** $\ell_3^{\rm RefG} = 811.55$ vs. Planck observed $\ell_3^{\rm obs} = 810.8 \pm 0.7$ (**$0.093\%$** error).

### Late-Time BAO Standard Ruler Distance Ratios ($D_M/r_d, D_H/r_d, D_V/r_d$)
Across the benchmark BOSS DR12, eBOSS DR16, and DESI DR2 effective redshifts, the RefG operational $A$-geometry predicts the parameter-free BAO distance ratios:

| Redshift $z$ | Operational $A = (1+z)^{-1}$ | Foundation $a_F = A^{2/5}$ | Cadence $p = A^{-3/5}$ | $D_M(z)/r_d$ | $D_H(z)/r_d$ | $D_V(z)/r_d$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $0.38$ | $0.72464$ | $0.87912$ | $1.21319$ | $10.436$ | $24.620$ | $10.063$ |
| $0.51$ | $0.66225$ | $0.84803$ | $1.28052$ | $13.515$ | $22.763$ | $12.847$ |
| $0.61$ | $0.62112$ | $0.82655$ | $1.33075$ | $15.723$ | $21.413$ | $14.780$ |
| $0.85$ | $0.54054$ | $0.78186$ | $1.44645$ | $20.502$ | $18.496$ | $18.766$ |
| $1.48$ | $0.40323$ | $0.69538$ | $1.72453$ | $30.255$ | $12.920$ | $25.964$ |
| $2.33$ | $0.30030$ | $0.61805$ | $2.05810$ | $39.222$ | $8.624$ | $31.384$ |

---

## 3. Sub-Horizon Linear Perturbation Growth $D_+(A)$, Gauss Hypergeometric Solution, Growth Index $\gamma = 6/11$, and $f\sigma_8(z)$ RSD Benchmark

### Theorem 3.1 (Equivalence of Linear Growth ODE, Gauss Hypergeometric Solution, and Heath Integral on the $A$-Geometry)
After the baryon drag epoch ($A > A_d$), baryons and the cold collective phase-current perturbation $\delta_C = \delta n_{C,\rm op}/n_{C,\rm op}$ co-evolve on sub-horizon scales ($k \gg A H_A/c_0$) as a single pressureless matter density contrast $\delta_m(A)$ governed in operational scale $A$ by:
$$
\frac{d^2 D_+}{dA^2} + \left(\frac{3}{A} + \frac{d\ln E(A)}{dA}\right)\frac{d D_+}{dA} - \frac{3\,\Omega_{m0}}{2\,A^5\,E(A)^2}\,D_+(A) = 0.
$$
On the late-time matter+$\Lambda$ branch ($E_m(A)^2 = \Omega_{m0} A^{-3} + \Omega_{\Lambda 0}$), the growing mode normalized to $D_+(A) \simeq A$ at $A \ll 1$ has the **exact closed-form Gauss hypergeometric representation**:
$$
D_+^{\rm (exact)}(A) = A\,{}_2F_1\!\left(\frac{1}{3},\,1;\,\frac{11}{6};\,-\frac{\Omega_{\Lambda 0}}{\Omega_{m0}}\,A^3\right) = \frac{5\,\Omega_{m0}}{2}\,E_m(A)\int_0^A \frac{du}{\bigl[u\,E_m(u)\bigr]^3}.
$$
At $A = 1$ ($z = 0$), high-precision `DOP853` numerical integration of the ODE, the closed-form hypergeometric function, and the Heath integral yield:
$$
D_+(1)_{\rm ODE} = 0.78792299616365, \qquad D_+(1)_{{}_2F_1} = 0.78792299616369, \qquad D_+(1)_{\rm Heath} = 0.78792299616369,
$$
agreeing to **$4.73\times 10^{-14}$** (ODE vs. ${}_2F_1$) and **$2.82\times 10^{-16}$** (Heath vs. ${}_2F_1$).

### Theorem 3.2 (Analytical Derivation of the Growth Index $\gamma(\Omega_m) = \frac{6}{11} + \frac{15}{2057}(1 - \Omega_m)$)
Expanding $D_+^{\rm (exact)}(A)$ in powers of $x \equiv -\frac{\Omega_{\Lambda 0}}{\Omega_{m0}}A^3 = -\frac{\epsilon}{1 - \epsilon}$ where $\epsilon \equiv 1 - \Omega_m(A)$:
$$
{}_2F_1\!\left(\frac{1}{3},\,1;\,\frac{11}{6};\,x\right) = 1 + \frac{2}{11}x + \frac{16}{187}x^2 + \mathcal{O}(x^3),
$$
the logarithmic growth rate $f(A) \equiv \frac{d\ln D_+}{d\ln A} = 1 + 3x\frac{{}_2F_1'(x)}{{}_2F_1(x)}$ has the exact asymptotic expansion around $\Omega_m \to 1$:
$$
f(\Omega_m) = \bigl[\Omega_m(A)\bigr]^{\gamma(\Omega_m)}, \qquad \gamma(\Omega_m) = \frac{6}{11} + \frac{15}{2057}\bigl(1 - \Omega_m(A)\bigr) + \mathcal{O}\bigl((1 - \Omega_m)^2\bigr),
$$
with zero symbolic residuals for both $\gamma_0 = \frac{6}{11} \approx 0.54545$ and $\gamma_1 = \frac{15}{2057} \approx 0.007292$. At $z = 0$ ($\Omega_{m0} = 0.31519$), $\gamma(\Omega_{m0}) = 0.55045$, giving $f_{\rm exact}(0) = 0.52728$ and $f\sigma_8(0) = f_{\rm exact}(0)\,\sigma_{8,0} = 0.42768$.

### Redshift-Space Distortion (RSD) $f\sigma_8(z)$ Benchmark Comparison
Across the 6 benchmark SDSS MGS, BOSS DR12, and eBOSS DR16 measurements, the RefG trajectory $f\sigma_8(z) = f(z)\,\sigma_{8,0}\,D_+(z)/D_+(0)$ achieves $\chi^2/\text{dof} = 7.074/6 = 1.179$:

| Survey | Redshift $z$ | Operational $A$ | $\widehat{D}_+(z) = D_+(z)/D_+(0)$ | Growth Rate $f(z)$ | $f\sigma_8^{\rm RefG}(z)$ | Observed $f\sigma_8^{\rm obs}(z)$ | Tension ($\sigma$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| SDSS MGS | $0.15$ | $0.86957$ | $0.92342$ | $0.61264$ | $0.4589$ | $0.530 \pm 0.160$ | $0.44\sigma$ |
| BOSS DR12 | $0.38$ | $0.72464$ | $0.81780$ | $0.71794$ | $0.4762$ | $0.497 \pm 0.045$ | $0.46\sigma$ |
| BOSS DR12 | $0.51$ | $0.66225$ | $0.76498$ | $0.76442$ | $0.4743$ | $0.459 \pm 0.038$ | $0.40\sigma$ |
| BOSS DR12 | $0.61$ | $0.62112$ | $0.72767$ | $0.79460$ | $0.4690$ | $0.436 \pm 0.034$ | $0.97\sigma$ |
| eBOSS ELG | $0.85$ | $0.54054$ | $0.64897$ | $0.85081$ | $0.4479$ | $0.315 \pm 0.095$ | $1.40\sigma$ |
| eBOSS QSO | $1.48$ | $0.40323$ | $0.49932$ | $0.92982$ | $0.3766$ | $0.462 \pm 0.045$ | $1.90\sigma$ |

---

## 4. Explicit Negative Mutation and Falsification Controls

1. **Mutation 1 — Broken Volume Jacobian ($\widehat{n}_{C,\rm op} = p^2\widehat{n}_{C,F}$ instead of $p^3\widehat{n}_{C,F}$, Falsification Criterion 2.5):**
   Replacing $p^3$ by $p^2$ yields $\widehat{n}_{C,\rm op}^{\rm mut}(A) = (A^{-3/5})^2 A^{-6/5} = A^{-12/5} = A^{-2.4} \neq A^{-3}$, suppressing the cold phase density at recombination by $A_*^{0.6} \approx 0.0150$ and shifting the drag-epoch BAO ruler from $146.94\text{ Mpc}$ to $198.52\text{ Mpc}$ (**$+35.10\%$ shift**), which is immediately detected and rejected.
2. **Mutation 2 — Non-Zero Collective Phase Sound Speed ($c_{s,C}^2 = 0.10 > 0$, Falsification Criterion 2.3):**
   Introducing an unsuppressed linear sound speed $c_{s,C}^2 = 0.10$ at $k = 0.1\,h\text{ Mpc}^{-1}$ replaces gravitational instability with rapid Jeans acoustic oscillations, collapsing the present-epoch growth factor from $D_+(1) = 0.78792$ to $|D_+^{\rm mut}(1)| = 2.76\times 10^{-5}$ (a **$3.50\times 10^{-5}$ suppression ratio**), which is detected and rejected.
3. **Mutation 3 — Uncoupled Atomic $p(A)$ Drift in $\alpha(z)$ (Falsification Criterion 1.4):**
   Allowing $p(A) = (1+z)^{3/5}$ to leak into $\alpha(z) = \alpha_0(1+z)^{3/5}$ produces $\Delta\alpha/\alpha = +0.9332$ at $z = 2$ (violating quasar absorption bounds $|\Delta\alpha/\alpha| < 10^{-6}$ by nearly 6 orders of magnitude) and boosts the Rydberg binding energy at $z_*$ by $(1+z_*)^{6/5} = 4419.3\times$, which is detected and rejected.
