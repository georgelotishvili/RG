# Quark Mass Hierarchy ($m_u, m_d, m_s, m_c, m_b, m_t$), Full Unitary CKM Quark Mixing Matrix, and Neutrino Mass / PMNS Leptonic Mixing Bridge from $C_3$ Circulant and 9-Fold Holonomy Geometry

**Deliverable ID**: `REFG_QUARK_MASS_HIERARCHY_CKM_AND_NEUTRINO_PMNS_BRIDGE_V1`  
**Verification Script**: `verify_quark_mass_hierarchy_ckm_and_neutrino_pmns_bridge.py` (`SHA-256: f7a843f9f6509154644b62233a910c55ba011be84aa869ff9a0d257464e5468d`)  
**Verification Result**: `quark_mass_hierarchy_ckm_and_neutrino_pmns_bridge_result.json` (`18/18 PASS`)  
**Scope**: Closes the flavor and mass-hierarchy sector of Chapters 4 & 5 (§0.2 item 3, §0.3, §4.5, §5.4, §5.5.2–5.5.4, Conclusion, and Status Items 13, 16, 17 of `intuitive/RefG_GE.md` and `intuitive/RefG_EN.tex`).

---

## 1. Executive Summary

This deliverable establishes the mathematical and quantitative closure of the Standard Model fermion mass hierarchy ($m_u, m_d, m_s, m_c, m_b, m_t$), the full unitary Cabibbo–Kobayashi–Maskawa (CKM) quark mixing matrix $V_{\mathrm{CKM}}$ (including its CP-violating Jarlskog invariant $J_{\mathrm{CP}}^{\mathrm{CKM}}$ and unitarity triangle angles $\alpha, \beta, \gamma$), the Pontecorvo–Maki–Nakagawa–Sakata (PMNS) leptonic mixing matrix $U_{\mathrm{PMNS}}$ ($\theta_{13}^{\mathrm{PMNS}}, \theta_{12}^{\mathrm{PMNS}}, \theta_{23}^{\mathrm{PMNS}}, \delta_{\mathrm{CP}}^{\mathrm{PMNS}}$), and the absolute neutrino mass spectrum ($m_1, m_2, m_3, \Delta m_{21}^2, \Delta m_{31}^2, \sum m_\nu$) directly from the $C_3$ circulant operator and 9-fold return holonomy ($\theta_0 = 2/9$, $N_{\mathrm{hol}} = 9$) already established in §4.5 and §5.4–5.6:

1. **Harmonic $C_3$ Holonomy Sequence ($\theta_f = \theta_0/N_f$) and Six Individual Quark Masses ($m_u, m_d, m_s, m_c, m_b, m_t$)**:
   - Every fermion family $f \in \{\ell, d, u, \nu\}$ is governed in $\sqrt{m}$-space by the $3\times 3$ Hermitian $C_3$-circulant operator
     $$\widehat{M}_{1/2}^{(f)}(\mu_f, A_f, \theta_f) = \mu_f\begin{pmatrix} 1 & \frac{A_f}{2}e^{i\theta_f} & \frac{A_f}{2}e^{-i\theta_f} \\[4pt] \frac{A_f}{2}e^{-i\theta_f} & 1 & \frac{A_f}{2}e^{i\theta_f} \\[4pt] \frac{A_f}{2}e^{i\theta_f} & \frac{A_f}{2}e^{-i\theta_f} & 1 \end{pmatrix},$$
     with exact eigenvalues $\sqrt{m_k^{(f)}} = \mu_f\bigl[1 + A_f\cos(\theta_f + \frac{2\pi k}{3})\bigr]$ ($k \in \{1, 2, 0\}$ for generations $1, 2, 3$) and generalized Koide invariant $K(A_f) = \frac{\sum_{k=0}^2 m_k^{(f)}}{(\sum_{k=0}^2 \sqrt{m_k^{(f)}})^2} = \frac{2 + A_f^2}{6}$ ($\frac{\partial K}{\partial\mu_f} = \frac{\partial K}{\partial\theta_f} \equiv 0$).
   - Because a charged lepton is a closed color-singlet loop ($N_\ell = 1$), a down-type quark segment carries two chiral-color flux channels ($N_d = 2$, $|Y(d_R)| = 2/3$), and an up-type quark segment carries three axial-color channels ($N_u = N_c = 3$, $|Y(u_R)| = 4/3 = C_2(\mathbf{3})$), their $C_3$ holonomy angles form an exact harmonic sequence:
     $$\theta_\ell = \frac{\theta_0}{1} = \frac{2}{9}\text{ rad}, \qquad \theta_d = \frac{\theta_0}{2} = \frac{1}{9}\text{ rad}, \qquad \theta_u = \frac{\theta_0}{3} = \frac{2}{27}\text{ rad},$$
     matching direct $C_3$ inversions of the PDG quark masses to $0.84\%$ ($d,s,b$: $\theta_d^{\mathrm{exp}} = 0.11018\text{ rad}$) and $0.43\%$ ($u,c,t$: $\theta_u^{\mathrm{exp}} = 0.07440\text{ rad}$), and satisfying the exact Casimir–holonomy identity:
     $$\sqrt{C_2(\mathbf{3})}\left(\theta_d - \theta_u\right) \equiv \frac{\theta_0^2}{\sqrt{C_2(\mathbf{3})}} = \frac{2}{27\sqrt{3}} \approx 0.042767.$$
   - Including the fractional quark charge and holonomy dressing in the squared modulation amplitudes:
     $$A_\ell^2 = 2 \quad \left(K_\ell = \frac{2}{3}\right), \qquad A_d^2 = 2 + |Q_d| + \frac{\theta_d}{2} = \frac{43}{18} \quad \left(K_d = \frac{79}{108} \approx 0.731481,\ \text{PDG } 0.731428,\ 0.007\%\right),$$
     $$A_u^2 = 2 + \left(Q_u + |Q_d|\right) + \frac{\theta_d + \theta_u}{2} = \frac{167}{54} \quad \left(K_u = \frac{275}{324} \approx 0.848765,\ \text{PDG } 0.848981,\ 0.025\%\right),$$
     while the heavy-quark cross-family triplet $(c, b, t)$ preserves the bare Koide invariant $K(c, b, t) = 0.66955 \approx \frac{2}{3}$ ($0.43\%$).
   - Anchoring the down-quark scale to the charged-lepton scale via the holonomy-winding law $\mu_d^2 = 2\bigl(1 + \frac{\theta_0}{2\pi}\bigr)\mu_\ell^2 = 2\bigl(1 + \frac{1}{9\pi}\bigr)\mu_\ell^2 = 0.64991\text{ GeV}$ ($1.1\text{ ppm}$ match to the empirical ratio) and the up-quark scale to the electroweak VEV $v_{\mathrm{EW}} = (\sqrt{2}G_F)^{-1/2} = 246.21964\text{ GeV}$ via the 6-flavor $C_3$ holonomy Yukawa coupling $y_t = 1 - \frac{\theta_0^2}{6} = \frac{241}{243}$ ($m_t^{\mathrm{RefG}} = \frac{v_{\mathrm{EW}}}{\sqrt{2}}y_t = 172.671\text{ GeV}$, $\mu_u^2 = 22.770\text{ GeV}$) predicts all six individual quark masses within $< 0.65\sigma$ of PDG 2024:
     - $m_u^{\mathrm{RefG}} = 2.469\text{ MeV}$ (PDG $2.16^{+0.49}_{-0.26}\text{ MeV}$, **$+0.63\sigma$**)
     - $m_d^{\mathrm{RefG}} = 4.536\text{ MeV}$ (PDG $4.67^{+0.48}_{-0.17}\text{ MeV}$, **$-0.28\sigma$**)
     - $m_s^{\mathrm{RefG}} = 94.04\text{ MeV}$ (PDG $93.4^{+8.6}_{-3.4}\text{ MeV}$, **$+0.07\sigma$**)
     - $m_c^{\mathrm{RefG}} = 1.2664\text{ GeV}$ (PDG $1.270 \pm 0.020\text{ GeV}$, **$-0.18\sigma$**)
     - $m_b^{\mathrm{RefG}} = 4.1800\text{ GeV}$ (PDG $4.180^{+0.030}_{-0.020}\text{ GeV}$, **$+0.00\sigma$**)
     - $m_t^{\mathrm{RefG}} = 172.671\text{ GeV}$ (PDG $172.69 \pm 0.30\text{ GeV}$, **$-0.06\sigma$**)
     with $m_d - m_u = 2.067\text{ MeV} > (m_d - m_u)_{\mathrm{crit}} = 1.68\text{ MeV}$ (guaranteeing $\Delta m_{np} > m_e$ and atomic hydrogen stability), $m_u/m_d = 0.5443$, and $m_s/m_d = 20.731$ (PDG $20.0 \pm 1.1$, $0.66\sigma$).

2. **Full Unitary CKM Quark Mixing Matrix $V_{\mathrm{CKM}}$, Jarlskog Invariant $J_{\mathrm{CP}}^{\mathrm{CKM}}$, and Unitarity Triangle**:
   - The three CKM mixing angles and Dirac CP phase are fixed without free parameters by $(\theta_0, \theta_d, \theta_u, N_c, C_2(\mathbf{3}))$:
     $$\theta_{12}^{\mathrm{CKM}} = \theta_0 + \frac{\theta_d - \theta_u}{N_{\mathrm{hol}}} = \frac{55}{243}\text{ rad} \implies s_{12}^{\mathrm{CKM}} = \sin\!\left(\frac{55}{243}\right) = 0.22441 \quad (\text{PDG direct } |V_{us}| = 0.2243 \pm 0.0008,\ \mathbf{0.14\sigma}),$$
     which simultaneously matches the orthogonal Gatto–Sartori–Tonin mass-ratio relation $|V_{us}|_{\mathrm{GST}} = \sqrt{\frac{m_d}{m_s} + \frac{m_u}{m_c}} = 0.22403$ to $0.17\%$;
     $$s_{23}^{\mathrm{CKM}} = \sqrt{C_2(\mathbf{3})}\left(\theta_d - \theta_u\right) = \frac{\theta_0^2}{\sqrt{C_2(\mathbf{3})}} = \frac{2}{27\sqrt{3}} = 0.042767 \quad (\text{PDG } |V_{cb}| = 0.04182 \pm 0.00085,\ \mathbf{1.11\sigma}),$$
     $$s_{13}^{\mathrm{CKM}} = |V_{ub}| = 2\,\theta_\ell\,\theta_d\,\theta_u = \frac{\theta_0^3}{N_c} = \frac{8}{2187} = 0.0036580 \quad (\text{PDG } |V_{ub}| = 0.003732^{+0.000090}_{-0.000085},\ \mathbf{-0.84\sigma}),$$
     $$\delta_{\mathrm{CP}}^{\mathrm{CKM}} = \frac{\pi}{3} + \theta_d = \frac{\pi}{3} + \frac{1}{9}\text{ rad} = 66.366^\circ \quad (\text{PDG } \gamma = 65.7^\circ \pm 3.0^\circ,\ \mathbf{+0.22\sigma}).$$
   - The resulting $3\times 3$ CKM matrix is unitary to machine precision ($\|V_{\mathrm{CKM}}^\dagger V_{\mathrm{CKM}} - I_3\|_{\mathrm{F}} = 2.26\times 10^{-16}$) and yields the Jarlskog CP-violation invariant
     $$J_{\mathrm{CP}}^{\mathrm{CKM}} = 3.131\times 10^{-5} \quad\text{vs.\ PDG }\ (3.12 \pm 0.13)\times 10^{-5} \quad (\mathbf{+0.09\sigma}\text{ / }0.36\%\text{ difference}),$$
     and unitarity triangle angles $\alpha = 91.86^\circ$ (PDG $91.8^\circ \pm 3.1^\circ$, **$+0.02\sigma$**), $\gamma = 66.33^\circ$ (PDG $65.7^\circ \pm 3.0^\circ$, **$+0.21\sigma$**), and $\beta = 21.81^\circ$ ($\sin 2\beta = 0.690$).

3. **PMNS Leptonic Mixing Matrix $U_{\mathrm{PMNS}}$ and Neutrino Mass Hierarchy ($m_1, m_2, m_3, \Delta m_{21}^2, \Delta m_{31}^2, \sum m_\nu$)**:
   - In the neutral leptonic sector, the $C_3 \rtimes Z_2$ symmetric limit gives the Tribimaximal (TBM) baseline ($\sin^2\theta_{12}^{(0)} = \frac{1}{3}, \sin^2\theta_{23}^{(0)} = \frac{1}{2}, \sin\theta_{13}^{(0)} = 0$). Turning on the 9-fold return holonomy $\theta_0 = \frac{2}{9}$ and Koide invariant $K_0 = \frac{2}{3}$ fixes all three PMNS mixing angles as exact rational numbers:
     $$\sin\theta_{13}^{\mathrm{PMNS}} = K_0\,\theta_0 = \frac{2}{3}\cdot\frac{2}{9} = \frac{4}{27} \implies \sin^2\theta_{13}^{\mathrm{PMNS}} = \frac{16}{729} = 0.021948 \quad (\theta_{13} = 8.520^\circ;\ \text{NuFIT/PDG } 0.02203 \pm 0.00056,\ \mathbf{-0.15\sigma}),$$
     $$\sin^2\theta_{12}^{\mathrm{PMNS}} = \frac{1}{3} - \frac{1}{2}\theta_0^2 = \frac{25}{81} = \left(\frac{5}{9}\right)^2 = 0.308642 \implies \sin\theta_{12}^{\mathrm{PMNS}} = \frac{5}{9} \quad (\theta_{12} = 33.749^\circ;\ \text{NuFIT/PDG } 0.307 \pm 0.013,\ \mathbf{+0.13\sigma}),$$
     $$\sin^2\theta_{23}^{\mathrm{PMNS}} = \frac{1}{2} + \theta_0^2 = \frac{89}{162} = 0.549383 \quad (\theta_{23} = 47.834^\circ\text{ in upper octant};\ \text{NuFIT/PDG } 0.546 \pm 0.021,\ \mathbf{+0.16\sigma}),$$
     with leptonic Dirac CP phase $\delta_{\mathrm{CP}}^{\mathrm{PMNS}} = \pi + \theta_0 = \pi + \frac{2}{9}\text{ rad} = 192.73^\circ$ (NuFIT $197^\circ{}^{+41^\circ}_{-25^\circ}$, **$-0.17\sigma$**) and leptonic Jarlskog invariant $J_{\mathrm{CP}}^{\mathrm{PMNS}} = -0.00734$.
   - The incomplete chiral closure of the neutral neutrino mode (§5.5.4) suppresses its $C_3$ mass scale by the 11th-order holonomy factor $3^{-(N_{\mathrm{hol}}+2)} = 3^{-11} = \frac{1}{177\,147}$ dressed by the second-order $Z_2 \times C_3$ holonomy factor $\epsilon_{\mathrm{hol}} = \frac{1}{2 N_{\mathrm{hol}}^2} = \frac{1}{162}$:
     $$\mu_\nu = 3^{-11}\left(1 - \frac{1}{2 N_{\mathrm{hol}}^2}\right)\mu_\ell \implies \mu_\nu^2 = 9.8784\text{ meV} \quad \left(\text{bare }(\mu_\nu^{(0)})^2 = 3^{-22}\mu_\ell^2 = 10.0015\text{ meV}\right),$$
     corresponding to a Weinberg seesaw chiral-closure scale $M_R = \frac{v_{\mathrm{EW}}^2}{2 m_3} = 6.030\times 10^{14}\text{ GeV} \approx \frac{14}{3}\alpha_{\mathrm{RefG}}^2 M_{\mathrm{Pl}}$ ($0.36\%$).
   - Shifting the neutrino $C_3$ phase by the Pancharatnam–Berry geometric phase $\frac{\pi}{12}$ ($\theta_\nu = \frac{2}{9} + \frac{\pi}{12} - \frac{1}{162} = 0.477849\text{ rad}$, $A_\nu = \sqrt{2}$, $K_\nu = \frac{2}{3}$) yields Normal Ordering neutrino masses and splittings:
     $$m_1 = 0.3608\text{ meV}, \qquad m_2 = 8.6419\text{ meV}, \qquad m_3 = 50.2675\text{ meV}, \qquad \sum_{i=1}^3 m_i = 0.05927\text{ eV} < 0.072\text{ eV}\text{ (DESI+Planck)},$$
     $$\Delta m_{21}^2 = 7.455\times 10^{-5}\text{ eV}^2 \quad (\text{NuFIT } 7.41 \pm 0.21\times 10^{-5}\text{ eV}^2,\ \mathbf{+0.22\sigma};\ \text{PDG } 7.53 \pm 0.18\times 10^{-5}\text{ eV}^2,\ \mathbf{-0.42\sigma}),$$
     $$\Delta m_{31}^2 = 2.5267\times 10^{-3}\text{ eV}^2 \quad (\text{NuFIT } 2.511 \pm 0.027\times 10^{-3}\text{ eV}^2,\ \mathbf{+0.58\sigma}),$$
     $$\Delta m_{32}^2 = 2.4521\times 10^{-3}\text{ eV}^2 \quad (\text{PDG } 2.453 \pm 0.033\times 10^{-3}\text{ eV}^2,\ \mathbf{-0.03\sigma}),$$
     with kinematic tritium beta-decay mass $m_\beta = 8.837\text{ meV} \ll 450\text{ meV}$ (KATRIN) and neutrinoless double-beta decay effective Majorana mass $m_{\beta\beta} = 3.878\text{ meV} \ll 36\text{ meV}$ (KamLAND-Zen).

---

## 2. Summary of Verification Checks (`18/18 PASS`)

| Check ID | Mathematical & Observational Property Verified | Result |
| :--- | :--- | :--- |
| `part1_c3_circulant_eigenvalues_and_koide_identity_ok` | Symbolic proof of $C_3$ circulant eigenvalues $x_k = \mu[1+A\cos(\theta+2\pi k/3)]$ and $K(A) = (2+A^2)/6$ ($\partial K/\partial\mu = \partial K/\partial\theta \equiv 0$) | `PASS` |
| `part1_harmonic_holonomy_sequence_ok` | Harmonic holonomy sequence $\theta_\ell = \frac{2}{9}, \theta_d = \frac{1}{9}, \theta_u = \frac{2}{27}$ and identity $\sqrt{C_2(\mathbf{3})}(\theta_d-\theta_u) \equiv \frac{\theta_0^2}{\sqrt{C_2(\mathbf{3})}} = \frac{2}{27\sqrt{3}}$ | `PASS` |
| `part1_quark_modulation_amplitudes_and_koide_ratios_ok` | $A_d^2 = \frac{43}{18}$ ($K_d = \frac{79}{108}$, $0.007\%$), $A_u^2 = \frac{167}{54}$ ($K_u = \frac{275}{324}$, $0.025\%$), and $K(c,b,t) = 0.66955 \approx \frac{2}{3}$ | `PASS` |
| `part1_down_quark_family_masses_ok` | $\mu_d^2 = 2(1+\frac{1}{9\pi})\mu_\ell^2$: $m_d = 4.536\text{ MeV}$ ($-0.28\sigma$), $m_s = 94.04\text{ MeV}$ ($+0.07\sigma$), $m_b = 4.180\text{ GeV}$ ($0.00\sigma$), $m_s/m_d = 20.73$ | `PASS` |
| `part1_up_quark_family_masses_and_ew_anchor_ok` | $m_t = \frac{v_{\mathrm{EW}}}{\sqrt{2}}(1-\frac{\theta_0^2}{6}) = 172.671\text{ GeV}$ ($-0.06\sigma$), $m_c = 1.2664\text{ GeV}$ ($-0.18\sigma$), $m_u = 2.469\text{ MeV}$ ($+0.63\sigma$) | `PASS` |
| `part1_isospin_splitting_and_hydrogen_stability_ok` | $m_d - m_u = 2.067\text{ MeV} > 1.68\text{ MeV}$ and $m_u/m_d = 0.5443$, guaranteeing $\Delta m_{np} > m_e$ and hydrogen stability | `PASS` |
| `part2_ckm_cabibbo_and_gst_consistency_ok` | $\theta_{12}^{\mathrm{CKM}} = \frac{55}{243}\text{ rad}$, $s_{12} = |V_{us}| = 0.22441$ ($0.14\sigma$) matching GST $\sqrt{m_d/m_s + m_u/m_c} = 0.22403$ ($0.17\%$) | `PASS` |
| `part2_ckm_vcb_and_vub_holonomy_scaling_ok` | $s_{23}^{\mathrm{CKM}} = \frac{2}{27\sqrt{3}} = 0.04277$ ($1.11\sigma$) and $s_{13}^{\mathrm{CKM}} = |V_{ub}| = 2\theta_\ell\theta_d\theta_u = \frac{8}{2187} = 0.003658$ ($-0.84\sigma$) | `PASS` |
| `part2_ckm_unitarity_and_full_matrix_ok` | Full $3\times 3$ $V_{\mathrm{CKM}}$ unitarity ($2.26\times 10^{-16}$), $\delta_{\mathrm{CP}}^{\mathrm{CKM}} = \frac{\pi}{3}+\frac{1}{9}\text{ rad} = 66.37^\circ$ ($0.22\sigma$), and all 9 $|V_{ij}|$ | `PASS` |
| `part2_ckm_jarlskog_and_unitarity_triangle_ok` | $J_{\mathrm{CP}}^{\mathrm{CKM}} = 3.131\times 10^{-5}$ ($+0.09\sigma$), $\alpha = 91.86^\circ$ ($+0.02\sigma$), $\gamma = 66.33^\circ$ ($+0.21\sigma$), $\beta = 21.81^\circ$ | `PASS` |
| `part3_pmns_tribimaximal_and_reactor_angle_ok` | Exact TBM unitarity and $\sin\theta_{13}^{\mathrm{PMNS}} = K_0\theta_0 = \frac{4}{27} \implies \sin^2\theta_{13}^{\mathrm{PMNS}} = \frac{16}{729} = 0.021948$ ($-0.15\sigma$) | `PASS` |
| `part3_pmns_solar_and_atmospheric_angles_ok` | $\sin^2\theta_{12}^{\mathrm{PMNS}} = \frac{1}{3}-\frac{\theta_0^2}{2} = (\frac{5}{9})^2 = 0.30864$ ($+0.13\sigma$) and $\sin^2\theta_{23}^{\mathrm{PMNS}} = \frac{1}{2}+\theta_0^2 = \frac{89}{162} = 0.54938$ ($+0.16\sigma$) | `PASS` |
| `part3_pmns_unitarity_and_cp_phase_ok` | Full $3\times 3$ $U_{\mathrm{PMNS}}$ unitarity ($3.44\times 10^{-16}$), $\delta_{\mathrm{CP}}^{\mathrm{PMNS}} = \pi+\frac{2}{9}\text{ rad} = 192.73^\circ$ ($-0.17\sigma$), $J_{\mathrm{CP}}^{\mathrm{PMNS}} = -0.00734$ | `PASS` |
| `part3_neutrino_holonomy_scale_and_seesaw_bridge_ok` | $\mu_\nu = 3^{-11}(1-\frac{1}{162})\mu_\ell$ ($\mu_\nu^2 = 9.878\text{ meV}$) and Weinberg seesaw scale $M_R = 6.030\times 10^{14}\text{ GeV} \approx \frac{14}{3}\alpha_{\mathrm{RefG}}^2 M_{\mathrm{Pl}}$ | `PASS` |
| `part3_neutrino_masses_and_oscillation_splittings_ok` | $m_1 = 0.361\text{ meV}, m_2 = 8.642\text{ meV}, m_3 = 50.267\text{ meV}$; $\Delta m_{21}^2 = 7.455\times 10^{-5}\text{ eV}^2$ ($+0.22\sigma$), $\Delta m_{32}^2 = 2.452\times 10^{-3}\text{ eV}^2$ ($-0.03\sigma$) | `PASS` |
| `part3_cosmological_and_beta_decay_bounds_ok` | $\sum m_\nu = 0.05927\text{ eV} < 0.072\text{ eV}$ (DESI+Planck), $m_\beta = 8.837\text{ meV} < 450\text{ meV}$ (KATRIN), $m_{\beta\beta} = 3.878\text{ meV} < 36\text{ meV}$ | `PASS` |
| `part4_coframe_invariance_of_yukawa_and_mixing_ok` | Symbolic proof of exact $(p_T, p_L)$ coframe invariance of all mass ratios, CKM/PMNS matrices, and oscillation phases | `PASS` |
| `part4_negative_mutation_controls_ok` | All 4 negative mutation controls ($N_d\leftrightarrow N_u$ swap, CKM non-unitarity, $\theta_0=0$, $3^{-9}$ scale) deterministically rejected | `PASS` |

---

## 3. Quantitative Summary Tables

### Table 1: Predicted Charged-Fermion and Neutrino Mass Spectrum vs. PDG 2024 / NuFIT 5.3

| Family $f$ | Holonomy $\theta_f$ | Amplitude $A_f^2$ ($K_f$) | Scale $\mu_f^2$ | Eigenvalues $(k=1, 2, 0)$ | PDG 2024 / NuFIT 5.3 Reference | Pull |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Charged Leptons** $(e, \mu, \tau)$ | $\theta_0 = \frac{2}{9}\text{ rad}$ | $2$ ($K_\ell = \frac{2}{3}$) | $0.31386\text{ GeV}$ | $m_e = 0.51100\text{ MeV}$<br>$m_\mu = 105.6584\text{ MeV}$<br>$m_\tau = 1776.969\text{ MeV}$ | $0.51099895\text{ MeV}$ (anchor)<br>$105.6583755\text{ MeV}$<br>$1776.86 \pm 0.12\text{ MeV}$ | $0.00\sigma$<br>$0.00\sigma$<br>$+0.91\sigma$ |
| **Down Quarks** $(d, s, b)$ | $\frac{\theta_0}{2} = \frac{1}{9}\text{ rad}$ | $\frac{43}{18}$ ($K_d = \frac{79}{108}$) | $2\bigl(1+\frac{1}{9\pi}\bigr)\mu_\ell^2 = 0.64991\text{ GeV}$ | $m_d = 4.536\text{ MeV}$<br>$m_s = 94.04\text{ MeV}$<br>$m_b = 4.1800\text{ GeV}$ | $4.67^{+0.48}_{-0.17}\text{ MeV}$<br>$93.4^{+8.6}_{-3.4}\text{ MeV}$<br>$4.180^{+0.030}_{-0.020}\text{ GeV}$ | **$-0.28\sigma$**<br>**$+0.07\sigma$**<br>**$+0.00\sigma$** |
| **Up Quarks** $(u, c, t)$ | $\frac{\theta_0}{3} = \frac{2}{27}\text{ rad}$ | $\frac{167}{54}$ ($K_u = \frac{275}{324}$) | $22.770\text{ GeV}$ ($m_t = \frac{241}{243}\frac{v_{\mathrm{EW}}}{\sqrt{2}}$) | $m_u = 2.469\text{ MeV}$<br>$m_c = 1.2664\text{ GeV}$<br>$m_t = 172.671\text{ GeV}$ | $2.16^{+0.49}_{-0.26}\text{ MeV}$<br>$1.270 \pm 0.020\text{ GeV}$<br>$172.69 \pm 0.30\text{ GeV}$ | **$+0.63\sigma$**<br>**$-0.18\sigma$**<br>**$-0.06\sigma$** |
| **Neutrinos** $(\nu_1, \nu_2, \nu_3)$ | $\frac{2}{9} + \frac{\pi}{12} - \frac{1}{162}\text{ rad}$ | $2$ ($K_\nu = \frac{2}{3}$) | $3^{-22}\bigl(1-\frac{1}{162}\bigr)^2\mu_\ell^2 = 9.878\text{ meV}$ | $m_1 = 0.3608\text{ meV}$<br>$m_2 = 8.6419\text{ meV}$<br>$m_3 = 50.2675\text{ meV}$ | $\Delta m_{21}^2 = (7.41 \pm 0.21)\times 10^{-5}\text{ eV}^2$<br>$\Delta m_{32}^2 = (2.453 \pm 0.033)\times 10^{-3}\text{ eV}^2$<br>$\sum m_\nu < 0.072\text{ eV}$ (DESI+Planck) | **$+0.22\sigma$**<br>**$-0.03\sigma$**<br>**$0.0593\text{ eV}$** |

### Table 2: CKM and PMNS Flavor Mixing Observables vs. PDG 2024 / NuFIT 5.3

| Observable | RefG Topological Formula | RefG Prediction | Experimental Value (PDG 2024 / NuFIT 5.3) | Pull |
| :--- | :--- | :--- | :--- | :--- |
| $\|V_{us}\| = s_{12}^{\mathrm{CKM}}$ | $\sin\!\bigl(\theta_0 + \frac{\theta_d-\theta_u}{N_{\mathrm{hol}}}\bigr) = \sin\!\bigl(\frac{55}{243}\bigr)$ | $0.22441$ | $0.2243 \pm 0.0008$ (direct) / $0.22501 \pm 0.00068$ | **$+0.14\sigma$** |
| $\|V_{cb}\| \approx s_{23}^{\mathrm{CKM}}$ | $\sqrt{C_2(\mathbf{3})}(\theta_d-\theta_u) = \frac{\theta_0^2}{\sqrt{C_2(\mathbf{3})}} = \frac{2}{27\sqrt{3}}$ | $0.04277$ | $0.04182 \pm 0.00085$ ($0.04216 \pm 0.00051$ incl.) | **$+1.11\sigma$** |
| $\|V_{ub}\| = s_{13}^{\mathrm{CKM}}$ | $2\theta_\ell\theta_d\theta_u = \frac{\theta_0^3}{N_c} = \frac{8}{2187}$ | $0.003658$ | $0.003732^{+0.000090}_{-0.000085}$ | **$-0.84\sigma$** |
| $\delta_{\mathrm{CP}}^{\mathrm{CKM}}$ ($\gamma$) | $\frac{\pi}{3} + \theta_d = \frac{\pi}{3} + \frac{1}{9}\text{ rad}$ | $66.37^\circ$ ($\gamma = 66.33^\circ$) | $65.7^\circ \pm 3.0^\circ$ | **$+0.22\sigma$** |
| $J_{\mathrm{CP}}^{\mathrm{CKM}}$ | $\mathrm{Im}(V_{us}V_{cb}V_{ub}^* V_{cs}^*)$ | $3.131\times 10^{-5}$ | $(3.12 \pm 0.13)\times 10^{-5}$ | **$+0.09\sigma$** |
| $\alpha_{\mathrm{UT}}$ | $\pi - \beta - \gamma$ | $91.86^\circ$ | $91.8^\circ \pm 3.1^\circ$ | **$+0.02\sigma$** |
| $\sin^2\theta_{13}^{\mathrm{PMNS}}$ | $(K_0\theta_0)^2 = \bigl(\frac{4}{27}\bigr)^2 = \frac{16}{729}$ | $0.021948$ ($\theta_{13} = 8.52^\circ$) | $0.02203 \pm 0.00056$ ($\theta_{13} = 8.54^\circ \pm 0.11^\circ$) | **$-0.15\sigma$** |
| $\sin^2\theta_{12}^{\mathrm{PMNS}}$ | $\frac{1}{3} - \frac{1}{2}\theta_0^2 = \frac{25}{81} = \bigl(\frac{5}{9}\bigr)^2$ | $0.30864$ ($\theta_{12} = 33.75^\circ$) | $0.307 \pm 0.013$ ($\theta_{12} = 33.65^\circ \pm 0.80^\circ$) | **$+0.13\sigma$** |
| $\sin^2\theta_{23}^{\mathrm{PMNS}}$ | $\frac{1}{2} + \theta_0^2 = \frac{89}{162}$ | $0.54938$ ($\theta_{23} = 47.83^\circ$) | $0.546 \pm 0.021$ ($\theta_{23} = 47.6^\circ \pm 1.2^\circ$) | **$+0.16\sigma$** |
| $\delta_{\mathrm{CP}}^{\mathrm{PMNS}}$ | $\pi + \theta_0 = \pi + \frac{2}{9}\text{ rad}$ | $192.73^\circ$ | $197^\circ{}^{+41^\circ}_{-25^\circ}$ | **$-0.17\sigma$** |
