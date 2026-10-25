# Strong-Field Horizonless EHT Shadow (Sgr A* and M87*), Quasinormal Modes, and Gravitational-Wave Echo Bridge (`W3-92`)

2026-10-25. Research contract, exact derivation, and symbolic/numerical verification supplement.
MODEL_VERSION=`REFG_STRONG_FIELD_COVARIANT_MEDIUM_C2_INTERIOR_V1`.

## Decision and scope

Building on the action-derived $C^2$-matched horizonless interior closure ([`action_derived_c2_interior_closure.md`](action_derived_c2_interior_closure.md)), where the static spherically symmetric line element
$$ds^2 = -\mathcal{B}(r)\,c_0^2 dt^2 + \mathcal{A}(r)\left(dr^2 + r^2 d\Omega^2\right)$$
smoothly joins the exact exponential exterior
$$\mathcal{B}_+(r) = e^{-2m/r}, \qquad \mathcal{A}_+(r) = e^{2m/r} \qquad (r \ge r_c)$$
to the unlocked degree-6 $C^2$ regular core ($x = r/r_c \in [0, 1]$, compactness $q \equiv 2m/r_c \in (1, q_*)$ with $q_* \approx 1.990069$):
$$\ln\mathcal{A}_-(x) = \ell_A(x) = q\left(\frac{35}{8}x^2 - \frac{21}{4}x^4 + \frac{15}{8}x^6\right), \qquad \ln\mathcal{B}_-(x) = \ell_B(x) = -q + q\left(-\frac{11}{8}x^2 + \frac{9}{4}x^4 - \frac{7}{8}x^6\right),$$
this package derives and verifies the three observational strong-field signatures required by §3.1, Falsification Criterion 2.4 (§6.4.2.4), and Status Item 8 of the Refractive Gravity monograph:

1. **Exact Photon Sphere ($r_{\rm ph}^+ = 2m$), Shadow Radius ($b_c^{\rm RefG} = 2 e m$), and Quantitative Event Horizon Telescope (EHT) Benchmarks for Sgr A* and M87*:**
   - Proves symbolically that the exterior null optical potential $V_+(r) = e^{-4m/r}/r^2$ has its unique global maximum at $r_{\rm ph}^+ = 2m = r_s$ ($V_+''(2m) = -\frac{e^{-2}}{8 m^4} < 0$) with critical shadow impact parameter $b_c^{\rm RefG} = 2 e m \approx 5.43656366\,m$ and fractional deviation relative to Schwarzschild ($b_c^{\rm GR} = 3\sqrt{3}\,m \approx 5.19615242\,m$):
     $$\delta_{\rm sh}^{\rm RefG} \equiv \frac{b_c^{\rm RefG}}{b_c^{\rm GR}} - 1 = \frac{2e}{3\sqrt{3}} - 1 \approx +0.04626716 \quad (+4.626716\%).$$
   - Evaluates the parameter-free angular shadow diameter $d_{\rm sh}^{\rm RefG} = 4 e\,\theta_g \approx 10.873127\,\theta_g$ ($\theta_g \equiv G M/(c_0^2 D)$) for **Sgr A*** ($\theta_g = 5.028\,\mu\text{as}$: $d_{\rm sh}^{\rm RefG} = 54.6701\,\mu\text{as}$ vs. EHT $48.7 \pm 7.0\,\mu\text{as}$, tension $0.85\sigma < 1\sigma$; Keck/VLTI fractional deviation bound $\delta_{\rm Sgr A^*} = -0.04^{+0.09}_{-0.10} \in [-0.14, +0.05]$, tension $0.96\sigma < 1\sigma$) and **M87*** ($\theta_g = 3.8\,\mu\text{as}$: $d_{\rm sh}^{\rm RefG} = 41.3179\,\mu\text{as}$ vs. EHT $42.0 \pm 3.0\,\mu\text{as}$, tension $0.23\sigma < 1\sigma$; $|\delta_{\rm M87^*}| \le 0.17$, tension $0.27\sigma < 1\sigma$).

2. **Global $C^2$ Tortoise Refractive Index, Eikonal Quasinormal Modes (QNM), and Quality-Factor Invariance Theorem:**
   - Proves that the radial optical refractive index $n_{\rm opt}(r) \equiv \frac{dr_*}{dr} = \sqrt{\mathcal{A}(r)/\mathcal{B}(r)}$ is globally $C^2$-smooth across the core boundary $r = r_c$ ($x = 1$), making the tortoise coordinate $r_*(r) = \int_0^r n_{\rm opt}(\tilde{r})\,d\tilde{r}$ globally $C^3$-smooth and strictly finite at the regular center ($n_{\rm opt}(0) = e^{q/2} < \infty$).
   - Proves the **Eikonal QNM Quality-Factor Invariance Theorem**: at the outer photon sphere $r_{\rm ph}^+ = 2m$, the circular null orbital angular velocity $\Omega_{\rm ph}^{\rm RefG}$ and the principal Lyapunov instability exponent $\lambda_{\rm L}^{\rm RefG}$ are identically equal:
     $$\Omega_{\rm ph}^{\rm RefG} = \lambda_{\rm L}^{\rm RefG} = \frac{c_0}{2 e m} \approx 0.18393972\,\frac{c_0}{m}, \qquad \frac{\lambda_{\rm L}^{\rm RefG}}{\Omega_{\rm ph}^{\rm RefG}} \equiv 1.$$
     Consequently, while both the real oscillation frequency $\omega_R^{(\ell)} = \Omega_{\rm ph}(\ell + 1/2)$ and the damping rate $\omega_I^{(n)} = \lambda_{\rm L}(n + 1/2)$ shift coherently by $\frac{3\sqrt{3}}{2e} - 1 \approx -4.422118\%$ at fixed ADM mass relative to Schwarzschild, the dimensionless ringdown quality factor is **100% identical to General Relativity**:
     $$Q_{\ell n}^{\rm RefG} \equiv \frac{\omega_R^{(\ell n)}}{2\,\omega_I^{(\ell n)}} = \frac{\ell + 1/2}{2(n + 1/2)} \equiv Q_{\ell n}^{\rm GR}.$$

3. **Finite Tortoise Cavity Depth, Exact Exterior Exponential-Integral Identity, and Quantitative Gravitational-Wave Echo Delay $\Delta t_{\rm echo}(q, M)$:**
   - Proves that, unlike a classical Schwarzschild black hole where $\int_{2m+\epsilon}^{3m}(1-2m/r)^{-1}dr \to +\infty$, the RefG horizonless $C^2$ core has a strictly finite tortoise depth from $r = 0$ to $r_{\rm ph}^+ = 2m$, with exact closed-form exterior integral
     $$\frac{L_{*,\rm ext}(q)}{m} = \frac{2}{q}\int_1^q e^{q/x}\,dx = 2\left[e - \frac{e^q}{q} + \operatorname{Ei}(q) - \operatorname{Ei}(1)\right]$$
     (verified against adaptive Gauss–Kronrod quadrature to $2.66\times 10^{-15}$).
   - Evaluates the dimensionless round-trip echo delay factor $\mathcal{I}_{\rm echo}(q) \equiv \frac{c_0\,\Delta t_{\rm echo}}{G M / c_0^2} = \frac{2 L_*(q)}{m}$ and inner-light-ring cavity factor $\mathcal{I}_{\rm cav}(q)$ across $q \in \{1.2, 1.5, 1.8\}$, predicting at the canonical benchmark $q = 3/2$ ($\mathcal{I}_{\rm echo}(1.5) = 15.555312$, effective compactness $\epsilon_{\rm eff} = e^{-\mathcal{I}_{\rm echo}/4} = 0.020469$) concrete, falsifiable post-merger echo delay times $\Delta t_{\rm echo} = 0.7662\text{ ms}$ ($10\,M_\odot$), $2.2985\text{ ms}$ ($30\,M_\odot$), $4.7503\text{ ms}$ (GW150914 remnant $M_f = 62\,M_\odot$), and $318.27\text{ s}$ (Sgr A*).

All 18 symbolic and numerical checks pass (`18/18 PASS`) via [`verify_strong_field_eht_shadow_qnm_and_echo_bridge.py`](verify_strong_field_eht_shadow_qnm_and_echo_bridge.py) and are recorded in [`strong_field_eht_shadow_qnm_and_echo_bridge_result.json`](strong_field_eht_shadow_qnm_and_echo_bridge_result.json).

---

## Frozen claims and verification contract

| Field | Contract |
|---|---|
| CLAIM_ID | `REFG_STRONG_FIELD_EHT_SHADOW_QNM_AND_ECHO_BRIDGE_V1` |
| CLAIM | On the action-derived $C^2$-matched horizonless compact-object geometry, (i) the outer photon sphere at $r_{\rm ph}^+ = 2m$ produces the exact critical shadow impact parameter $b_c^{\rm RefG} = 2 e m$ ($\delta_{\rm sh} = \frac{2e}{3\sqrt{3}} - 1 = +4.6267\%$), which lies strictly within the $1\sigma$ EHT bounds for both Sgr A* ($d_{\rm sh} = 54.67\,\mu\text{as}$, $0.85\sigma$; $\delta = +0.0463 \in [-0.14, +0.05]$, $0.96\sigma$) and M87* ($d_{\rm sh} = 41.32\,\mu\text{as}$, $0.23\sigma$; $|\delta| \le 0.17$, $0.27\sigma$); (ii) the radial optical index $n_{\rm opt}(r) = \sqrt{\mathcal{A}(r)/\mathcal{B}(r)}$ is globally $C^2$-smooth across $r = r_c$, and the eikonal QNM spectrum at $r_{\rm ph}^+ = 2m$ obeys the exact identity $\Omega_{\rm ph}^{\rm RefG} = \lambda_{\rm L}^{\rm RefG} = \frac{c_0}{2em}$, preserving the GR ringdown quality factor $Q_{\ell n}^{\rm RefG} \equiv Q_{\ell n}^{\rm GR}$; (iii) the tortoise cavity depth from $r=0$ to $r_{\rm ph}^+ = 2m$ is strictly finite, with closed-form exterior integral $L_{*,\rm ext}(q)/m = 2[e - e^q/q + \operatorname{Ei}(q) - \operatorname{Ei}(1)]$ and benchmark echo delay $\mathcal{I}_{\rm echo}(3/2) = 15.555312$ ($\Delta t_{\rm echo} = 4.7503\text{ ms}$ for GW150914 remnant $M_f = 62\,M_\odot$). |
| TYPE | Exact symbolic theorems (photon-sphere derivatives, $C^2$ tortoise junction, eikonal QNM Lyapunov/frequency equality, exterior exponential-integral identity) and high-precision numerical quadrature/observational benchmark verification. |
| MODEL_VERSION | `REFG_STRONG_FIELD_COVARIANT_MEDIUM_C2_INTERIOR_V1` ([`action_derived_c2_interior_closure.md`](action_derived_c2_interior_closure.md)). |
| ASSUMPTIONS | Static spherically symmetric isotropic coordinates $ds^2 = -\mathcal{B}(r)c_0^2 dt^2 + \mathcal{A}(r)(dr^2 + r^2 d\Omega^2)$; exponential exterior $\mathcal{B}_+(r)=e^{-2m/r}, \mathcal{A}_+(r)=e^{2m/r}$ on $r \ge r_c$; unlocked degree-6 $C^2$ core on $x = r/r_c \in [0, 1]$ with compactness $q = 2m/r_c \in (1, q_*)$. |
| DOMAIN | Symbolic identities hold for all $m > 0$ and $q \in (1, 2)$; numerical echo quadratures evaluated across $q \in \{1.2, 1.5, 1.8\}$ with primary witness $q = 3/2$. |
| CONVENTIONS | $m = G M / c_0^2$; $\theta_g = G M / (c_0^2 D)$; $n_{\rm opt}(r) = \frac{dr_*}{dr} = \sqrt{\mathcal{A}(r)/\mathcal{B}(r)}$; $\delta_{\rm sh} = \frac{d_{\rm sh}}{6\sqrt{3}\theta_g} - 1$; $\mathcal{I}_{\rm echo}(q) = \frac{2 L_*(q)}{m} = \frac{c_0 \Delta t_{\rm echo}}{m}$. |
| FREEDOM_LEDGER | Exterior shadow radius $b_c^{\rm RefG} = 2em$ and eikonal QNM spectrum $\Omega_{\rm ph} = \lambda_{\rm L} = \frac{c_0}{2em}$ have **zero** free parameters beyond ADM mass $M$. Interior echo delay factor $\mathcal{I}_{\rm echo}(q)$ depends solely on the dimensionless core compactness $q = 2m/r_c \in (1, q_*)$. |
| DEPENDENCIES | [`FORMAL_COVARIANT_MEDIUM_INTEGRATION.md`](FORMAL_COVARIANT_MEDIUM_INTEGRATION.md), [`action_derived_c2_interior_closure.md`](action_derived_c2_interior_closure.md), [`verify_action_derived_c2_interior_closure.py`](verify_action_derived_c2_interior_closure.py), pinned by SHA-256. |
| METHOD | SymPy exact symbolic proof of $V_+'(r)$, $V_+''(2m)$, $b_c^{\rm RefG}$, $C^0/C^1/C^2$ tortoise matching at $x=1$, and $\lambda_{\rm L}^{\rm RefG} = \Omega_{\rm ph}^{\rm RefG}$; SciPy `quad` (`epsabs=1e-13, epsrel=1e-13`), `brentq`, and `expi` for $\mathcal{I}_{\rm echo}(q)$ and $\mathcal{I}_{\rm cav}(q)$. |
| PASS_CONDITION | `18/18` checks pass: all symbolic residuals identically `0`; EHT Sgr A* and M87* shadow diameters and $\delta_{\rm sh}$ within $1\sigma$; exterior tortoise integral matches closed-form $\operatorname{Ei}$ identity to $< 10^{-13}$; $\mathcal{I}_{\rm echo}(q)$ finite and strictly increasing with $q$; 3 negative controls rejected. |
| FAIL_CONDITION | Any nonzero symbolic residual, violation of EHT $1\sigma$ bounds, tortoise discontinuity at $r=r_c$, or divergence of $L_*(q)$. |
| FALSIFIER | EHT shadow diameter measurements excluding $\delta_{\rm sh}^{\rm RefG} = +4.63\%$, LVK ringdown quality-factor measurements excluding $Q_{\ell n}^{\rm RefG} = Q_{\ell n}^{\rm GR}$, or post-merger echo searches ruling out the finite cavity delay $\Delta t_{\rm echo}(q, M)$ together with the barrier greybody factor. |
| RESIDUAL | Stored in [`strong_field_eht_shadow_qnm_and_echo_bridge_result.json`](strong_field_eht_shadow_qnm_and_echo_bridge_result.json). |
| ERROR_BOUND | Exact (`0`) for symbolic theorems; $2.66\times 10^{-15}$ for exterior tortoise quadrature vs. closed-form $\operatorname{Ei}$ formula. |
| VALIDITY_HEALTH | Everywhere positive metric components $\mathcal{A}, \mathcal{B} > 0$; smooth $C^2$ optical index $n_{\rm opt}(r) \ge e^{q/2} > 1$; strictly unstable outer light ring ($V_+''(2m) < 0$) and strictly stable inner light ring ($V_-''(r_{\rm lr}^-) > 0$). |
| BRANCHES | Horizonless exponential exterior ($r \ge r_c$) + action-derived degree-6 $C^2$ regular core ($r \le r_c$). |
| OBSERVABLE_MAP | Shadow angular diameter $d_{\rm sh} = 4e\,\theta_g$, fractional shadow deviation $\delta_{\rm sh} = \frac{2e}{3\sqrt{3}} - 1$, eikonal QNM frequencies $\omega_{\ell n} = \frac{c_0}{2em}[(\ell+\frac{1}{2}) - i(n+\frac{1}{2})]$, and echo delay time $\Delta t_{\rm echo}(q, M) = \mathcal{I}_{\rm echo}(q)\frac{GM}{c_0^3}$. |
| FORWARD_MODEL | Null geodesic ray-tracing potential $V_{\rm opt}(r) = \mathcal{B}(r)/[\mathcal{A}(r)r^2]$, eikonal WKB master wave equation in tortoise coordinate $r_*(r)$, and two-barrier optical cavity round-trip travel time. |
| DATA_ROLE | Quantitative benchmark comparison against EHT Collaboration Sgr A* (2022 ApJL 930, L12 & L17) and M87* (2019 ApJL 875, L1 & L6; 2021 PRD 103, 104047) $1\sigma$ bounds, and LVK GW150914 remnant mass scale ($M_f = 62\,M_\odot$). |
| IDENTIFIABILITY | Exterior observables ($b_c^{\rm RefG}, \delta_{\rm sh}^{\rm RefG}, \Omega_{\rm ph}^{\rm RefG}, \lambda_{\rm L}^{\rm RefG}, Q_{\ell n}^{\rm RefG}$) are parameter-free predictions of the exponential exterior alone; the echo delay factor $\mathcal{I}_{\rm echo}(q)$ directly measures the core compactness $q = 2m/r_c$. |
| BENCHMARK | Exact agreement with [`action_derived_c2_interior_closure.md`](action_derived_c2_interior_closure.md) §2.2 and EHT/LVK published benchmarks. |
| CLOSURE_FLAGS | Closes the analytical and numerical EHT shadow, eikonal QNM, and tortoise echo-delay bridge for §3.1, §6.4.2.4, and Status Item 8. Full spin-$a_*$ Kerr-like rotational generalization and time-dependent nonlinear collapse waveform templates remain subsequent tasks. |
| CROSSCHECK | Symbolic SymPy derivatives vs. numerical root-finding (`brentq`); numerical Gauss–Kronrod quadrature of $L_{*,\rm ext}(q)$ vs. analytical exponential-integral formula $2[e - e^q/q + \operatorname{Ei}(q) - \operatorname{Ei}(1)]$. |
| PROVENANCE | Script SHA-256 `3e193be569ac68b7fa110182c32a7f3dc3145beb63afa5db36a692987e2c1089`; Result JSON SHA-256 `8fa72519c555432f847912a4f4953fad96d602e6810f97edf078cf9f097d0f25`. |
| FILES | `RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/strong_field_eht_shadow_qnm_and_echo_bridge.md`, `RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_strong_field_eht_shadow_qnm_and_echo_bridge.py`, `RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/strong_field_eht_shadow_qnm_and_echo_bridge_result.json`. |

---

## 1. Exact Photon Sphere, Critical Shadow Impact Parameter, and EHT Sgr A* / M87* Benchmarks

### 1.1 Null Geodesics and Unstable Photon Sphere on the Exponential Exterior

On the horizonless exponential exterior ($r \ge r_c$, $q = 2m/r_c > 1$),
$$\mathcal{B}_+(r) = e^{-2m/r}, \qquad \mathcal{A}_+(r) = e^{2m/r}, \qquad \mathcal{A}_+(r)\mathcal{B}_+(r) \equiv 1,$$
equatorial null geodesics ($\theta = \pi/2$, conserved energy $E = \mathcal{B}_+(r)c_0\dot{t}$, angular momentum $L = \mathcal{A}_+(r)r^2\dot{\varphi}$, impact parameter $b \equiv c_0 L / E$) obey the radial equation
$$\left(\frac{dr}{d\lambda}\right)^2 = \frac{E^2}{c_0^2}\left[1 - b^2 V_+(r)\right], \qquad V_+(r) \equiv \frac{\mathcal{B}_+(r)}{\mathcal{A}_+(r)r^2} = \frac{e^{-4m/r}}{r^2}.$$
Differentiating $V_+(r)$ with respect to $r$ gives
$$\frac{d V_+(r)}{dr} = \frac{2(2m - r)}{r^4}\,e^{-4m/r} = 0 \iff r_{\rm ph}^+ = 2m = r_s,$$
with strictly negative second derivative at the peak:
$$\left.\frac{d^2 V_+(r)}{dr^2}\right|_{r = 2m} = -\frac{e^{-2}}{8 m^4} < 0.$$
The critical shadow impact parameter is therefore
$$b_c^{\rm RefG} = \frac{1}{\sqrt{V_+(2m)}} = 2 e m \approx 5.4365636569\,m,$$
which exceeds the classical Schwarzschild value $b_c^{\rm GR} = 3\sqrt{3}\,m \approx 5.1961524227\,m$ by the exact parameter-free fraction
$$\delta_{\rm sh}^{\rm RefG} \equiv \frac{b_c^{\rm RefG}}{b_c^{\rm GR}} - 1 = \frac{2e}{3\sqrt{3}} - 1 \approx +0.0462671636 \quad (+4.626716\%).$$

### 1.2 Quantitative Comparison with EHT Observations of Sgr A* and M87*

For an observer at distance $D \gg m$ viewing a compact object of angular gravitational radius $\theta_g \equiv \frac{G M}{c_0^2 D}$, the predicted shadow angular diameter is $d_{\rm sh}^{\rm RefG} = 2(b_c^{\rm RefG}/m)\theta_g = 4e\,\theta_g \approx 10.873127\,\theta_g$ (vs. $d_{\rm sh}^{\rm GR} = 6\sqrt{3}\,\theta_g \approx 10.392305\,\theta_g$):

| Target | $\theta_g$ ($\mu\text{as}$) | $d_{\rm sh}^{\rm GR}$ ($\mu\text{as}$) | $d_{\rm sh}^{\rm RefG}$ ($\mu\text{as}$) | EHT Measured $d_{\rm sh}$ ($\mu\text{as}$) | Direct Tension | EHT $1\sigma$ Bound on $\delta_{\rm sh}$ | $\delta_{\rm sh}^{\rm RefG}$ Tension | Status |
|---|---:|---:|---:|---:|---:|---|---:|---|
| **Sgr A*** (EHT 2022) | $5.028$ | $52.25$ | **$54.67$** | $48.7 \pm 7.0$ | **$0.85\sigma$** | $[-0.14,\,+0.05]$ (Keck+VLTI) | **$0.96\sigma$** | **PASS ($<1\sigma$)** |
| **M87*** (EHT 2019/2021) | $3.800$ | $39.49$ | **$41.32$** | $42.0 \pm 3.0$ | **$0.23\sigma$** | $[-0.17,\,+0.17]$ | **$0.27\sigma$** | **PASS ($<1\sigma$)** |

---

## 2. Global $C^2$ Tortoise Coordinate and Eikonal Quasinormal Modes (QNM)

### 2.1 Global $C^2$ Smoothness of the Radial Optical Index $n_{\rm opt}(r)$

Along radial null rays ($ds^2 = 0, d\Omega = 0$), $c_0 dt = \pm n_{\rm opt}(r)\,dr \equiv \pm dr_*$, where the effective radial optical refractive index is
$$n_{\rm opt}(r) \equiv \frac{dr_*}{dr} = \sqrt{\frac{\mathcal{A}(r)}{\mathcal{B}(r)}} = \begin{cases} \exp\!\left[\dfrac{q}{2}\left(1 + \dfrac{23}{4}x^2 - \dfrac{15}{2}x^4 + \dfrac{11}{4}x^6\right)\right], & 0 \le x = \dfrac{r}{r_c} \le 1, \\[10pt] e^{2m/r} = e^{q/x}, & x = \dfrac{r}{r_c} \ge 1. \end{cases}$$
At the core boundary $x = 1$ ($r = r_c$), the interior and exterior optical indices and their first two radial derivatives match identically:
$$n_{\rm opt}^-(1) = n_{\rm opt}^+(1) = e^q, \qquad \left.\frac{d n_{\rm opt}^-}{dx}\right|_1 = \left.\frac{d n_{\rm opt}^+}{dx}\right|_1 = -q e^q, \qquad \left.\frac{d^2 n_{\rm opt}^-}{dx^2}\right|_1 = \left.\frac{d^2 n_{\rm opt}^+}{dx^2}\right|_1 = q(q+2)e^q.$$
Thus $n_{\rm opt}(r)$ is globally $C^2$-smooth (free of artificial junction reflection steps), and the tortoise coordinate $r_*(r) = \int_0^r n_{\rm opt}(\tilde{r})\,d\tilde{r}$ is globally $C^3$-smooth and finite at the origin ($n_{\rm opt}(0) = e^{q/2} < \infty$).

### 2.2 Eikonal QNM Quality-Factor Invariance Theorem

In the eikonal/WKB regime ($\ell \gg 1$), scalar, electromagnetic, and axial gravitational perturbations trapped at the unstable photon sphere $r_{\rm ph}^+ = 2m$ obey the master wave equation $\frac{d^2\Psi_\ell}{dr_*^2} + \left[\frac{\omega^2}{c_0^2} - \ell(\ell+1)V_{\rm opt}(r)\right]\Psi_\ell = 0$, yielding the complex quasinormal-mode frequencies
$$\omega_{\ell n}^{\rm RefG} = \Omega_{\rm ph}^{\rm RefG}\left(\ell + \frac{1}{2}\right) - i\left(n + \frac{1}{2}\right)\lambda_{\rm L}^{\rm RefG} + \mathcal{O}(\ell^{-1}), \qquad n = 0, 1, 2, \dots$$
Evaluating the circular null angular velocity $\Omega_{\rm ph}^{\rm RefG} = c_0\sqrt{V_+(2m)}$ and the principal Lyapunov instability exponent $\lambda_{\rm L}^{\rm RefG} = \frac{c_0}{n_{\rm opt}^+(2m)}\sqrt{-\frac{V_+''(2m)}{2 V_+(2m)}}$ at $r_{\rm ph}^+ = 2m$ ($V_+(2m) = \frac{e^{-2}}{4m^2}$, $V_+''(2m) = -\frac{e^{-2}}{8 m^4}$, $n_{\rm opt}^+(2m) = e$) yields the exact identity:
$$\Omega_{\rm ph}^{\rm RefG} = \frac{c_0}{2 e m}, \qquad \lambda_{\rm L}^{\rm RefG} = \frac{c_0}{e}\sqrt{\frac{e^{-2}/(8m^4)}{2(e^{-2}/(4m^2))}} = \frac{c_0}{2 e m} \implies \frac{\lambda_{\rm L}^{\rm RefG}}{\Omega_{\rm ph}^{\rm RefG}} \equiv 1.$$
Comparing with Schwarzschild GR ($\Omega_{\rm ph}^{\rm GR} = \lambda_{\rm L}^{\rm GR} = \frac{c_0}{3\sqrt{3}\,m}$) establishes two exact consequences:
1. At fixed ADM mass $M$, both the real oscillation frequency and the damping rate shift coherently by $\frac{\Omega_{\rm ph}^{\rm RefG}}{\Omega_{\rm ph}^{\rm GR}} - 1 = \frac{3\sqrt{3}}{2e} - 1 \approx -4.422118\%$ (for the GW150914 remnant mass $M_f = 62\,M_\odot$, the $\ell=2, n=0$ eikonal benchmark gives $f_{20}^{\rm RefG} = 239.66\text{ Hz}$, $\tau_{20}^{\rm RefG} = 3.320\text{ ms}$ vs. $f_{20}^{\rm GR} = 250.75\text{ Hz}$, $\tau_{20}^{\rm GR} = 3.174\text{ ms}$).
2. Because $\lambda_{\rm L}/\Omega_{\rm ph} \equiv 1$ in both geometries, the dimensionless **ringdown quality factor** is identically preserved:
   $$Q_{\ell n}^{\rm RefG} \equiv \frac{\omega_R^{(\ell n)}}{2\,\omega_I^{(\ell n)}} = \frac{\ell + 1/2}{2(n + 1/2)} \equiv Q_{\ell n}^{\rm GR}.$$

---

## 3. Finite Tortoise Cavity Depth and Quantitative Gravitational-Wave Echo Delay $\Delta t_{\rm echo}(q, M)$

Unlike a classical Schwarzschild black hole where $\int_{2m+\epsilon}^{3m}(1-2m/r)^{-1}dr \to +\infty$ as $\epsilon \to 0^+$, the optical tortoise distance from the regular center $r = 0$ to the outer photon-sphere barrier $r_{\rm ph}^+ = 2m$ is strictly finite:
$$L_*(q) = \int_0^{2m} n_{\rm opt}(r)\,dr = L_{*,\rm core}(q) + L_{*,\rm ext}(q) < \infty,$$
where the exterior integral ($r \in [r_c, 2m]$, $x \in [1, q]$) has the exact closed-form exponential-integral expression
$$\frac{L_{*,\rm ext}(q)}{m} = \frac{2}{q}\int_1^q e^{q/x}\,dx = 2\left[e - \frac{e^q}{q} + \operatorname{Ei}(q) - \operatorname{Ei}(1)\right].$$
Consequently, waves partially transmitted inward through the $r_{\rm ph}^+ = 2m$ barrier reflect off the regular core center $r = 0$ (and traverse the inner stable light ring $r_{\rm lr}^- = r_c x_{\rm lr}(q)$), producing delayed post-merger gravitational-wave **echoes** with round-trip delay time
$$\Delta t_{\rm echo}(q, M) = \frac{2 L_*(q)}{c_0} = \mathcal{I}_{\rm echo}(q)\,\frac{G M}{c_0^3}, \qquad \mathcal{I}_{\rm echo}(q) \equiv \frac{2 L_*(q)}{m}.$$

| Compactness $q = 2m/r_c$ | $r_c / m$ | $r_{\rm lr}^- / m$ | $L_{*,\rm core}/m$ | $L_{*,\rm ext}/m$ | $\mathcal{I}_{\rm echo}(q) = 2L_*/m$ | $\mathcal{I}_{\rm cav}(q)$ ($r_{\rm lr}^-\leftrightarrow 2m$) | $\epsilon_{\rm eff} = e^{-\mathcal{I}_{\rm echo}/4}$ | $\Delta t_{\rm echo}$ ($10\,M_\odot$) | $\Delta t_{\rm echo}$ ($30\,M_\odot$) | $\Delta t_{\rm echo}$ (GW150914 $62\,M_\odot$) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **$1.2$** | $1.6667$ | $1.5139$ | $5.134692$ | $0.996984$ | **$12.263353$** | $3.066961$ | $0.046615$ | $0.604\text{ ms}$ | $1.812\text{ ms}$ | **$3.745\text{ ms}$** |
| **$1.5$** | $1.3333$ | $1.1608$ | $5.504342$ | $2.273313$ | **$15.555312$** | $6.252789$ | $0.020469$ | $0.766\text{ ms}$ | $2.299\text{ ms}$ | **$4.750\text{ ms}$** |
| **$1.8$** | $1.1111$ | $0.9426$ | $6.171263$ | $3.424233$ | **$19.190990$** | $9.185948$ | $0.008248$ | $0.945\text{ ms}$ | $2.836\text{ ms}$ | **$5.861\text{ ms}$** |

---

## 4. Negative Controls Rejected (`3/3`)

1. `negative_control_schwarzschild_horizon_divergent_tortoise_rejected`: replacing the horizonless $C^2$ core with the classical Schwarzschild factor $f(r) = 1 - 2m/r$ causes $\lim_{\epsilon\to 0^+}\int_{2m+\epsilon}^{3m}(1-2m/r)^{-1}dr = +\infty$, eliminating finite-time echo reflection — **rejected**.
2. `negative_control_c0_only_core_tortoise_c2_jump_rejected`: replacing the degree-6 $C^2$ core with a naive constant-index core $n_{\rm opt}^{\rm naive}(x) \equiv e^q$ on $x \in [0, 1]$ creates large $C^1$ and $C^2$ derivative jumps at $x = 1$ ($|\Delta n_{\rm opt}'(1)| = 6.7225$ and $|\Delta n_{\rm opt}''(1)| = 23.5289$ at $q = 1.5$) — **rejected**.
3. `negative_control_oversized_shadow_violating_eht_1sigma_rejected`: mutating the shadow radius to $b_c^{\rm mut} = 7.0\,m$ ($\delta_{\rm mut} = +0.3472$) violates both the EHT Sgr A* ($+0.05$) and M87* ($+0.17$) $1\sigma$ bounds — **rejected**.
