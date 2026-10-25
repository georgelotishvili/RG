# First-Principles Primordial Nucleosynthesis (BBN) Coframe Clock Invariance and Quantitative JWST Early Massive Galaxy Process-Time Assembly Closure

**Package ID:** `REFG_COSMOLOGICAL_BBN_AND_JWST_PROCESS_MATURITY_V1`  
**Status:** `PASS` (`18/18` automated symbolic and numerical verification checks passed)  
**Verification Script:** `RefG/work 3/Cosmology_and_LSS/BBN_and_JWST_Process_Maturity/verify_cosmological_bbn_and_jwst_process_maturity.py` (`SHA-256: 57ea24dddf23acbcb28c78f8ddbf7c741fd652610c62282546da8f821c18b5ee`)  
**Result Artifact:** `RefG/work 3/Cosmology_and_LSS/BBN_and_JWST_Process_Maturity/cosmological_bbn_and_jwst_process_maturity_result.json` (`SHA-256: 0c682b8f0663dc3a070e9db53b9319d4faafa29a0e040782d2c1071a220619eb`)

---

## 1. Executive Summary

A foundational question for any theory in which the physical clock rate varies with cosmological epoch—specifically, where the early-Universe foundation pressure ratio $\eta_F(A) = P_F/P_{F,0} = A^{-6/5} = (1+z)^{6/5} > 1$ drives a faster foundation clock cadence $p(A) = \sqrt{\eta_F(A)} = A^{-3/5} = (1+z)^{3/5} > 1$—is how the theory simultaneously achieves two seemingly opposite observational requirements:

1. **Primordial Nucleosynthesis (BBN) Preservation at $z \sim 10^9$:** At $T_\gamma \in [0.078, 0.80]\text{ MeV}$ ($z \in [3.0\times 10^8,\, 3.4\times 10^9]$), the foundation clock factor reaches $p(A) \in [1.30\times 10^5,\, 5.24\times 10^5]$ and the foundation pressure ratio reaches $\eta_F(A) \in [1.68\times 10^{10},\, 2.75\times 10^{11}]$. Why does a $5\times 10^5$-fold faster coordinate clock rate not alter the neutron-to-proton weak freeze-out temperature $T_{\rm freeze} \approx 0.8\text{ MeV}$ or spoil the primordial Helium-4 ($Y_p$) and Deuterium ($(\text{D/H})_p$) abundances?
2. **JWST Early Massive Galaxy Maturity at $z \in [8, 15]$:** Conversely, in the post-recombination matter-dominated era ($z \in [8, 20]$), why *does* the faster foundation clock $p(z) = (1+z)^{3/5} \in [3.74, 6.21]$ resolve the James Webb Space Telescope (JWST) early maturity anomaly—providing $2.42\text{–}3.93\text{ Gyr}$ of accumulated physical process time $\tau(z)$ (and $0.61\text{–}2.12\text{ Gyr}$ of post-$z=20$ assembly time) where constant-clock $\Lambda$CDM allows only $286\text{–}636\text{ Myr}$ of total age (and $108\text{–}458\text{ Myr}$ after $z=20$)?

This package establishes the exact mathematical and numerical closure of both questions from the single operational coframe law $A = a/p = a^{5/2}$ and local proper process differential $d\tau = p(t)\,dt$:

- **BBN Coframe Clock Invariance & Zero Dark Radiation ($\Delta N_{\rm eff}^{\rm RefG} \equiv 0$):** During the radiation-dominated BBN epoch, the neutron-to-proton conversion balance is governed by the dimensionless ratio of the weak reaction rate to the expansion rate of the operational photon bath ($T_\gamma \propto A^{-1}$). In foundation coordinate time $t$, both the nuclear weak conversion rates $\Gamma_{n\leftrightarrow p}^{(t)}(A) = p(A)\,\Gamma_{n\leftrightarrow p}^{(0)}(T_\gamma)$ and the coordinate rate of change of the operational scale factor $dA/dt = p(A)\,A\,H_{\rm op}(A)$ scale linearly with the exact same local cadence factor $p(A) = A^{-3/5}$. Consequently, $p(A)$ cancels identically from the relativistic Boltzmann equation $dX_n/dA$. Furthermore, because the collective foundation phase source $Q_C$ resides on its cold Thomas–Fermi condensate branch ($\hat{\rho}_{C,\mathrm{op}}(A) = \rho_{C,0}\,A^{-3}$), its energy density relative to radiation during BBN is $\hat{\rho}_{C,\mathrm{op}}/\hat{\rho}_{r,\mathrm{op}} = (\Omega_{C,0}/\Omega_{r,0})\,A = 8.44\times 10^{-7}$ at weak freeze-out ($T = 0.80\text{ MeV}$) and $8.66\times 10^{-6}$ at the deuterium bottleneck ($T_{\rm nuc} = 0.0779\text{ MeV}$), contributing zero dark radiation ($\Delta N_{\rm eff}^{\rm RefG} \equiv 0$). Integrating the relativistic weak Boltzmann equation with the parameter-free RefG Version 4.1 neutron lifetime $\tau_n^{\rm RefG} = 879.903\text{ s}$ yields:
  $$X_n^{\rm freeze} = 0.1559, \qquad T_{\rm nuc} = 0.07792\text{ MeV}\;\;(t_{\rm nuc} = 210.2\text{ s}), \qquad X_n(T_{\rm nuc}) = 0.12278,$$
  $$Y_p^{\rm RefG} = 2 X_n(T_{\rm nuc}) = 0.2456 \quad (\text{vs. PDG 2024 } 0.245 \pm 0.003,\;\; 0.19\sigma),$$
  $$(\text{D/H})_p^{\rm RefG} = 2.512\times 10^{-5} \quad (\text{vs. PDG 2024 } (2.547 \pm 0.025)\times 10^{-5},\;\; 1.38\sigma).$$
- **Quantitative JWST Early Massive Galaxy Process-Time Assembly ($z \in [8, 15]$):** Unlike radiation-locked BBN freeze-out (which depends on the ratio of two rates at a single radiation temperature $T_\gamma$), post-recombination baryonic star formation, stellar main-sequence evolution, supernova chemical enrichment, and Balmer-break buildup inside gravitationally collapsed halos are **cumulative proper-time processes** governed by the integrated number of atomic and nuclear clock cycles $\Delta\tau(z_{\rm form}\to z) = \int_{t(z_{\rm form})}^{t(z)} p(t)\,dt = \int_{A_{\rm form}}^{A(z)} \frac{A^{-8/5}\,dA}{H_0\,E(A)}$. In the matter-dominated era, $\tau(z)/t(z) = \frac{5}{3}\,p(z) = \frac{5}{3}(1+z)^{3/5}$ symbolically. With a standard feedback-regulated gas depletion time $\tau_{\rm dep} = 0.80\text{ Gyr}$ starting at halo collapse onset $z_{\rm form} = 20$, RefG converts $83.9\%$ of convertible gas into stars by $z = 10$ (vs. $30.6\%$ in constant-clock $\Lambda$CDM, a **$2.74\times$** boost in stellar mass at $z = 10$ and **$3.75\times$** at $z = 13$), assembling $M_* = 1.0\times 10^{10}\,M_\odot$ in a $3.5\times 10^{11}\,M_\odot$ halo at $z = 10$ with a normal feedback-regulated baryon conversion efficiency $\epsilon_*^{\rm RefG} = 0.218 < 0.25$ (whereas constant-clock $\Lambda$CDM requires an extreme $\epsilon_*^{\Lambda\text{CDM}} = 0.596 > 0.55$) and providing $1.46\text{ Gyr}$ ($z = 10$) to $2.12\text{ Gyr}$ ($z = 8$) of post-$z=20$ process time for evolved Balmer-break stellar populations and $4.1\times\text{–}5.2\times$ higher metallicity enrichment.

---

## 2. Exact Coframe Clock Invariance of BBN Weak Freeze-Out and $\Delta N_{\rm eff}^{\rm RefG} \equiv 0$

### 2.1 Common-Coframe Cancellation of $p(A)$ in the Relativistic Boltzmann Equation

In RefG, all local nuclear, weak, and electromagnetic interactions share the common foundation coframe metric $\ell_\mu \propto p(x)$ and local process time differential $d\tau = p(A)\,dt$, where $A = a/p = a^{5/2}$ is the operational scale factor and $p(A) = A^{-3/5}$.

Consider the neutron fraction $X_n \equiv n_n / (n_n + n_p)$ during the BBN epoch ($0.05\text{ MeV} \le T_\gamma \le 10\text{ MeV}$). In local operational process units (where $m_e$, $Q_{np} = m_n - m_p = 1.29333\text{ MeV}$, and $G_F$ are coframe invariants), the weak conversion rates $\Gamma_{n\to p}^{(0)}(T_\gamma)$ and $\Gamma_{p\to n}^{(0)}(T_\gamma)$ are fixed functions of the operational photon and neutrino temperatures $T_\gamma(A) = T_{\gamma,0}/A$ and $T_\nu(A)$.

When written in foundation coordinate time $t$:
1. Every microscopic weak reaction rate scales linearly with the foundation clock cadence $p(A)$:
   $$\Gamma_{n\to p}^{(t)}(A) = p(A)\,\Gamma_{n\to p}^{(0)}(T_\gamma(A)), \qquad \Gamma_{p\to n}^{(t)}(A) = p(A)\,\Gamma_{p\to n}^{(0)}(T_\gamma(A)).$$
2. Simultaneously, the coordinate rate of change of the operational scale factor $A$ is related to the operational Hubble rate $H_{\rm op}(A) \equiv \frac{1}{A}\frac{dA}{d\tau_{\rm op}}$ by the exact same clock factor $p(A)$:
   $$\frac{dA}{dt} = p(A)\,\frac{dA}{d\tau_{\rm op}} = p(A)\,A\,H_{\rm op}(A).$$

Transforming the coordinate-time Boltzmann equation $\frac{dX_n}{dt} = -\Gamma_{n\to p}^{(t)}(A)\,X_n + \Gamma_{p\to n}^{(t)}(A)\,(1 - X_n)$ to the operational scale factor $A$ via the chain rule yields:
$$\frac{dX_n}{dA} = \frac{dX_n/dt}{dA/dt} = \frac{-p(A)\,\Gamma_{n\to p}^{(0)}(A)\,X_n + p(A)\,\Gamma_{p\to n}^{(0)}(A)\,(1 - X_n)}{p(A)\,A\,H_{\rm op}(A)} = \frac{-\Gamma_{n\to p}^{(0)}(A)\,X_n + \Gamma_{p\to n}^{(0)}(A)\,(1 - X_n)}{A\,H_{\rm op}(A)}.$$

Thus $p(A) = A^{-3/5}$ cancels identically:
$$\frac{\partial}{\partial p(A)}\left(\frac{dX_n}{dA}\right) \equiv 0.$$

### 2.2 Absence of Dark Radiation ($\Delta N_{\rm eff}^{\rm RefG} \equiv 0$) at BBN

Because the collective foundation phase source $Q_C$ obeys exact Noether conservation on its cold Thomas–Fermi condensate branch ($w_C = 0$, $c_{s,C}^2 = 0$), its operational energy density scales as $\hat{\rho}_{C,\mathrm{op}}(A) = \rho_{C,0}\,A^{-3}$, whereas the radiation bath scales as $\hat{\rho}_{r,\mathrm{op}}(A) = \rho_{r,0}\,A^{-4}$. The ratio of the collective foundation condensate density to the radiation density at BBN is therefore suppressed by $A \sim 3\times 10^{-10}\text{–}3\times 10^{-9}$:

| BBN Epoch Milestone | $T_\gamma$ [MeV] | Redshift $z$ | Operational Scale $A$ | Clock Factor $p(A) = A^{-3/5}$ | Pressure Ratio $\eta_F(A) = A^{-6/5}$ | $\hat{\rho}_{C,\mathrm{op}} / \hat{\rho}_{r,\mathrm{op}}$ | $\Delta N_{\rm eff}^{\rm RefG}$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Weak Freeze-Out | $0.8000$ | $3.406\times 10^9$ | $2.936\times 10^{-10}$ | $5.240\times 10^5$ | $2.746\times 10^{11}$ | $8.437\times 10^{-7}$ | $0$ |
| Deuterium Bottleneck | $0.07792$ | $3.316\times 10^8$ | $3.014\times 10^{-9}$ | $1.298\times 10^5$ | $1.685\times 10^{10}$ | $8.662\times 10^{-6}$ | $0$ |

### 2.3 Numerical Relativistic Weak Freeze-Out and Primordial Element Abundances ($Y_p$, $(\text{D/H})_p$)

Integrating the relativistic three-channel weak conversion rates ($n + \nu_e \leftrightarrow p + e^-$, $n + e^+ \leftrightarrow p + \bar{\nu}_e$, and $n \leftrightarrow p + e^- + \bar{\nu}_e$) normalized at $T \to 0$ to the RefG Version 4.1 derived neutron lifetime $\tau_n^{\rm RefG} = 879.903\text{ s}$ across $T_\gamma \in [10.0, 0.05]\text{ MeV}$ with exact $e^+e^-$ annihilation entropy transfer $T_\nu / T_\gamma = [(4 + 7 f_{ee}(T_\gamma))/11]^{1/3}$ and Planck baryon-to-photon ratio $\eta_{10} = 273.715\,\Omega_b h^2 = 6.1230$ gives:

| Observable / Parameter | Symbol | RefG Prediction | Observational Benchmark (PDG 2024) | Tension / Status |
| :--- | :---: | :---: | :---: | :---: |
| Neutron $\beta$-decay lifetime (V4.1) | $\tau_n^{\rm RefG}$ | $879.903\text{ s}$ | $878.4 \pm 0.5\text{ s}$ (UCN bottle) / $888.0 \pm 2.0\text{ s}$ (beam) | Input from V4.1 |
| Baryon-to-photon ratio ($10^{10}\eta_b$) | $\eta_{10}$ | $6.1230$ | $6.123 \pm 0.038$ (Planck 2018) | $0.00\sigma$ |
| Effective neutrino species | $N_{\rm eff}^{\rm RefG}$ | $3.044$ ($\Delta N_{\rm eff}=0$) | $2.99 \pm 0.17$ (Planck + BBN) | $0.32\sigma$ |
| Asymptotic weak freeze-out fraction | $X_n^{\rm freeze}$ | $0.15590$ | $0.151\text{–}0.158$ | **PASS** |
| Kinetic deuterium bottleneck temperature | $T_{\rm nuc}$ | $0.07792\text{ MeV}$ | $0.075\text{–}0.080\text{ MeV}$ | **PASS** |
| Operational time at $T_{\rm nuc}$ | $t_{\rm nuc}$ | $210.15\text{ s}$ | $200\text{–}250\text{ s}$ | **PASS** |
| Surviving neutron fraction at $T_{\rm nuc}$ | $X_n(T_{\rm nuc})$ | $0.12278$ | $0.1225 \pm 0.0015$ | **PASS** |
| **Primordial Helium-4 mass fraction** | $Y_p^{\rm RefG}$ | **$0.24556$** | **$0.2450 \pm 0.0030$** | **$0.19\sigma$ (PASS)** |
| **Primordial Deuterium abundance** | $(\text{D/H})_p^{\rm RefG}$ | **$2.512\times 10^{-5}$** | **$(2.547 \pm 0.025)\times 10^{-5}$** | **$1.38\sigma$ (PASS)** |

---

## 3. Quantitative JWST High-Redshift ($z \in [8, 20]$) Process-Time Galaxy Assembly and Maturity

### 3.1 Exact Symbolic and Numerical Comparison of Coordinate Age $t(z)$ vs. Process Age $\tau(z)$

While BBN depends on an instantaneous rate ratio at $T_\gamma \sim 0.8\text{ MeV}$, post-recombination galaxy evolution depends on the **accumulated physical process time** $\tau(z)$ elapsed since the Big Bang (and specifically $\Delta\tau(z_{\rm form}\to z)$ elapsed since the onset of first-generation halo collapse at $z_{\rm form} = 20$):
$$t(z) = \frac{1}{H_0}\int_0^{(1+z)^{-1}} \frac{dA}{A\,E(A)}, \qquad \tau(z) = \int_0^{t(z)} p(t)\,dt = \frac{1}{H_0}\int_0^{(1+z)^{-1}} \frac{A^{-8/5}\,dA}{E(A)}.$$

In the matter-dominated regime ($E(A) \simeq \sqrt{\Omega_{m,0}}\,A^{-3/2}$), symbolic integration yields:
$$t_{\rm mat}(A) = \frac{2}{3 H_0 \sqrt{\Omega_{m,0}}}\,A^{3/2}, \qquad \tau_{\rm mat}(A) = \frac{10}{9 H_0 \sqrt{\Omega_{m,0}}}\,A^{9/10} \implies \frac{\tau_{\rm mat}(z)}{t_{\rm mat}(z)} = \frac{5}{3}\,p(z) = \frac{5}{3}(1+z)^{3/5}.$$

Exact numerical quadrature including radiation, matter, and $\Lambda_{\rm eff}$ across key JWST redshifts yields:

| Redshift $z$ | Benchmark / Survey Epoch | Clock Rate $p(z)=(1+z)^{3/5}$ | Pressure Ratio $\eta_F(z)=(1+z)^{6/5}$ | $\Lambda$CDM Age $t(z)$ [Myr] | RefG Process Age $\tau(z)$ [Gyr] | Total Ratio $\tau(z)/t(z)$ | Post-$z=20$ $\Delta t$ [Myr] | Post-$z=20$ $\Delta\tau$ [Myr] | Assembly Window Boost $\Delta\tau/\Delta t$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $20.0$ | Halo collapse / Cosmic Dawn onset | $6.213$ | $38.61$ | $177.6$ | $1.8159$ | $10.22\times$ | $0.0$ | $0.0$ | $6.21\times$ |
| $14.32$ | **JADES-GS-z14-0** (Carniani et al. 2024) | $5.142$ | $26.44$ | $285.7$ | $2.4230$ | $8.48\times$ | $108.0$ | $607.1$ | **$5.62\times$** |
| $14.0$ | JWST $z=14$ benchmark | $5.078$ | $25.78$ | $294.9$ | $2.4701$ | $8.38\times$ | $117.3$ | $654.2$ | **$5.58\times$** |
| $13.0$ | **JADES-GS-z13-0** (Robertson et al. 2023) | $4.872$ | $23.73$ | $327.2$ | $2.6306$ | $8.04\times$ | $149.5$ | $814.7$ | **$5.45\times$** |
| $12.0$ | GLASS-z12 /Maisie's Galaxy epoch | $4.660$ | $21.71$ | $365.8$ | $2.8144$ | $7.69\times$ | $188.1$ | $998.5$ | **$5.31\times$** |
| $10.0$ | **JWST $z=10$** (GN-z11 / CEERS / UNCOVER) | $4.215$ | $17.77$ | $470.2$ | $3.2767$ | $6.97\times$ | $292.6$ | $1460.8$ | **$4.99\times$** |
| $9.0$ | Labbé et al. (2023) upper redshift | $3.981$ | $15.85$ | $542.7$ | $3.5732$ | $6.58\times$ | $365.0$ | $1757.4$ | **$4.81\times$** |
| $8.0$ | **Labbé et al. (2023)** massive red candidates | $3.737$ | $13.97$ | $635.8$ | $3.9320$ | $6.18\times$ | $458.1$ | $2116.1$ | **$4.62\times$** |
| $6.0$ | End of Reionization | $3.214$ | $10.33$ | $927.1$ | $4.9379$ | $5.33\times$ | $749.4$ | $3122.0$ | **$4.17\times$** |
| $0.0$ | Present-day Universe ($A_0 = 1$) | $1.000$ | $1.00$ | $13796.6$ | $24.5799$ | $1.78\times$ | $13619.0$ | $22764.0$ | $1.67\times$ |

### 3.2 Resolution of the JWST Baryonic Efficiency, Balmer-Break, and Metallicity Tensions

In a collapsed halo of baryon mass $M_b = (\Omega_{b,0}/\Omega_{m,0})\,M_{\rm halo} = 0.1571\,M_{\rm halo}$, star formation regulated by radiative and supernova feedback converts gas into stars on a characteristic proper depletion timescale $\tau_{\rm dep} \approx 0.80\text{ Gyr}$:
$$M_*(z) = \epsilon_{\max}\,M_b\,\big[1 - \exp\!\big(-\Delta\tau(z_{\rm form}\to z)/\tau_{\rm dep}\big)\big], \qquad f_{\rm conv}(\Delta\tau) \equiv 1 - \exp(-\Delta\tau/\tau_{\rm dep}).$$

Comparing constant-clock $\Lambda$CDM ($\Delta t(20\to z)$) against RefG process-time evolution ($\Delta\tau(20\to z)$):

| Redshift $z$ | $\Lambda$CDM Gas Conversion $f_{\rm conv}^{\Lambda\text{CDM}}$ | RefG Gas Conversion $f_{\rm conv}^{\rm RefG}$ | Assembled Stellar Mass Boost $M_*^{\rm RefG}/M_*^{\Lambda\text{CDM}}$ | $\Lambda$CDM Metallicity $Z/y_Z$ | RefG Metallicity $Z/y_Z$ | Chemical Enrichment Boost $Z^{\rm RefG}/Z^{\Lambda\text{CDM}}$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $14.0$ | $13.63\%$ | $55.86\%$ | **$4.10\times$** | $0.123$ | $0.644$ | **$5.23\times$** |
| $13.0$ | $17.05\%$ | $63.88\%$ | **$3.75\times$** | $0.157$ | $0.783$ | **$5.00\times$** |
| $10.0$ | $30.63\%$ | $83.89\%$ | **$2.74\times$** | $0.302$ | $1.249$ | **$4.14\times$** |
| $8.0$ | $43.60\%$ | $92.90\%$ | **$2.13\times$** | $0.463$ | $1.559$ | **$3.37\times$** |

1. **Resolution of the "Impossible Early Galaxy" Baryon Efficiency Crisis:** For a benchmark halo of $M_{\rm halo} = 3.5\times 10^{11}\,M_\odot$ ($M_b = 5.50\times 10^{10}\,M_\odot$) at $z = 10$, assembling a massive galaxy of $M_* = 1.0\times 10^{10}\,M_\odot$ within $\tau_{\rm dep} = 0.80\text{ Gyr}$ requires an intrinsic baryon conversion cap of $\epsilon_{\rm req}^{\Lambda\text{CDM}} = 0.596$ in constant-clock $\Lambda$CDM—Nearly $3\times$ above the maximum feedback-regulated efficiency $\epsilon_{\max} \approx 0.20\text{–}0.25$ observed in local and intermediate-redshift starbursts. In RefG, because $\Delta\tau(20\to 10) = 1.461\text{ Gyr}$, $83.9\%$ of the convertible reservoir has already been processed, requiring only a completely normal $\epsilon_{\rm req}^{\rm RefG} = 0.218 < 0.25$ (giving $M_*^{\rm RefG}(z=10) = 1.01\times 10^{10}\,M_\odot$ at $\epsilon_{\max} = 0.22$, vs. $3.69\times 10^9}\,M_\odot$ in $\Lambda$CDM).
2. **Resolution of Evolved Balmer Breaks at $z = 8\text{–}10$:** Strong $3646\text{ \AA}$ Balmer breaks observed in JWST candidates at $z = 8\text{–}10$ require A/F-type main-sequence turnoff stars with stellar population ages $\Delta\tau_* \gtrsim 400\text{–}800\text{ Myr}$. In $\Lambda$CDM at $z = 10$, the entire post-$z=20$ window is only $292.6\text{ Myr}$ ($< 400\text{ Myr}$). In RefG, the post-$z=20$ process window is **$1,460.8\text{ Myr}$ at $z = 10$** and **$2,116.1\text{ Myr}$ at $z = 8$**, easily accommodating mature post-starburst Balmer breaks and dust/metal enrichment across multiple AGB and core-collapse supernova cycles.

---

## 4. Verification Summary and Negative Falsification Controls

All `18/18` checks in `verify_cosmological_bbn_and_jwst_process_maturity.py` pass:
- **Control 1 (Inverted Clock Law Rejected):** Replacing $d\tau = p(A)\,dt$ with the inverted law $d\tau_{\rm wrong} = dt/p(A) = A^{+3/5}\,dt$ yields $\tau_{\rm wrong}(z=10) = 79.8\text{ Myr} < t(10) = 470.2\text{ Myr}$, making the JWST early maturity problem $5.9\times$ *worse* instead of solving it.
- **Control 2 (Uncompensated BBN Clock Scaling Rejected):** Allowing $p(A)$ to scale nuclear weak rates $\Gamma_{n\leftrightarrow p}^{(t)}$ without scaling the coordinate expansion rate $dA/dt$ (violating common-coframe transposition) shifts freeze-out to $T_{\rm freeze} \sim 0.015\text{ MeV}$ and destroys primordial Helium-4 ($Y_p \sim 7\times 10^{-38} \approx 0$).
- **Control 3 (Constant-Clock Extreme Efficiency Rejected):** Constant-clock $\Lambda$CDM requires $2.74\times$ higher baryon conversion efficiency ($\epsilon_* = 0.596$) than RefG ($\epsilon_* = 0.218$) to assemble $10^{10}\,M_\odot$ by $z = 10$.
