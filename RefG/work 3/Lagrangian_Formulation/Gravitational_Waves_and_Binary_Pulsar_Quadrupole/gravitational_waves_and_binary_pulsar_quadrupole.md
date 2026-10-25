# Gravitational-Wave Propagation ($v_{\rm gw} \equiv c_0$), Two Transverse-Traceless Polarizations ($h_+, h_\times$), and Relativistic Binary Pulsar Quadrupole Radiation (`PSR B1913+16`, `PSR J0737-3039A/B`, `PSR J1738+0333`)

- **Module ID:** `REFG_GRAVITATIONAL_WAVES_AND_BINARY_PULSAR_QUADRUPOLE_V1`
- **Verification Script:** [verify_gravitational_waves_and_binary_pulsar_quadrupole.py](verify_gravitational_waves_and_binary_pulsar_quadrupole.py) (`77a50d3a0c4882d98470e49bb9d6d53f9bdb5e747daf2c1958faefc060130062`)
- **Result Artifact:** [gravitational_waves_and_binary_pulsar_quadrupole_result.json](gravitational_waves_and_binary_pulsar_quadrupole_result.json) (`af460c06edf73bffb853689bcac777f0ab5dd16a551c5a2c6257b312c89667c7`)
- **Verification Status:** `PASS (18/18 checks passed)`

---

## 1. Coframe TEGR / Einstein–Hilbert Linearization, Exact $v_{\rm gw} \equiv c_0$ (`GW170817`), and Purely Transverse-Traceless ($h_+, h_\times$) Polarizations

1. **Coframe Perturbation and Inertial-Gauge Orientation (`CHK_01`):**
   On the isolated branch ($\Psi_C \equiv 0$, $\Lambda_F = 0$) of the Grand Unified Covariant Action (`REFG_GRAND_UNIFIED_ACTION_V1`), expanding the relational coframe around Minkowski space as
   $$e^A{}_\mu = \delta^A_\mu + \frac{1}{2}\eta^{AB}h_{B\mu} + \frac{1}{2}\eta^{AB}\omega_{B\mu}, \qquad h_{\mu\nu} = h_{\nu\mu},\quad \omega_{\mu\nu} = -\omega_{\nu\mu},$$
   yields the first-order metric perturbation $g_{\mu\nu} = \eta_{AB}e^A{}_\mu e^B{}_\nu = \eta_{\mu\nu} + h_{\mu\nu} + \mathcal{O}(h^2)$ with identically zero dependence on all 6 antisymmetric local Lorentz orientation components ($\partial g^{(1)}_{\mu\nu}/\partial\omega_{\alpha\beta} \equiv 0$).

2. **Linearized Einstein Operator, Bianchi Identity, and Lorenz-Gauge Wave Equation (`CHK_02`, `CHK_03`):**
   In terms of the trace-reversed perturbation $\bar{h}_{\mu\nu} \equiv h_{\mu\nu} - \frac{1}{2}\eta_{\mu\nu}h$, the linearized Einstein tensor
   $$G^{(1)}_{\mu\nu} = -\frac{1}{2}\Box\bar{h}_{\mu\nu} + \frac{1}{2}\bigl(\partial_\mu\partial^\alpha\bar{h}_{\alpha\nu} + \partial_\nu\partial^\alpha\bar{h}_{\alpha\mu} - \eta_{\mu\nu}\partial^\alpha\partial^\beta\bar{h}_{\alpha\beta}\bigr)$$
   satisfies the linearized Bianchi identity $\partial^\mu G^{(1)}_{\mu\nu} \equiv 0$ identically for arbitrary symmetric $h_{\mu\nu}(t,\mathbf{x})$ and reduces in Lorenz gauge ($\partial^\mu\bar{h}_{\mu\nu} = 0$) to
   $$\Box\bar{h}_{\mu\nu} = \left(-\frac{1}{c_0^2}\frac{\partial^2}{\partial t^2} + \nabla^2\right)\bar{h}_{\mu\nu} = -\frac{16\pi G}{c_0^4}T_{\mu\nu}.$$
   A vacuum plane wave $\bar{h}_{\mu\nu} = \epsilon_{\mu\nu}e^{i k_\alpha x^\alpha}$ has exact null dispersion $\omega^2 = c_0^2|\mathbf{k}|^2$, giving
   $$v_{\rm phase} = v_{\rm group} = c_0 \implies \frac{v_{\rm gw}^{\rm RefG} - c_0}{c_0} \equiv 0,$$
   strictly within the GW170817 / GRB 170817A multi-messenger constraint $-3\times 10^{-15} \le (v_{\rm gw} - c_0)/c_0 \le +7\times 10^{-16}$ (Abbott et al. 2017).

3. **Two Transverse-Traceless Polarizations and Interferometer Differential Readout (`CHK_04`, `CHK_05`, `CHK_06`):**
   Starting from $10$ independent components of symmetric $\bar{h}_{\mu\nu}$, the $4$ Lorenz constraints $k^\mu\epsilon_{\mu\nu} = 0$ and $4$ residual harmonic gauge transformations $\epsilon_{\mu\nu} \to \epsilon_{\mu\nu} + i(k_\mu\xi_\nu + k_\nu\xi_\mu - \eta_{\mu\nu}k\cdot\xi)$ ($k^2 = 0$) leave exactly **$10 - 4 - 4 = 2$** transverse-traceless radiative polarizations ($h_+, h_\times$) with $\eta^{\mu\nu}e^{+,\times}_{\mu\nu} = 0$, $k^\mu e^{+,\times}_{\mu\nu} = 0$, $e^+_{\mu\nu}e^{+\mu\nu} = e^\times_{\mu\nu}e^{\times\mu\nu} = 2$, and $e^+_{\mu\nu}e^{\times\mu\nu} = 0$ (and zero scalar breathing or vector modes).
   While an isotropic scalar clock-ruler shift ($\delta p_T = \delta p_L = \delta p$) affects both orthogonal Michelson interferometer arms identically ($\Delta\tau_x - \Delta\tau_y \equiv 0$, common-mode self-calibration), a TT gravitational wave stretches one arm and compresses the orthogonal arm, producing the differential strain readout $(\Delta L_x - \Delta L_y)/L_0 = h_+\cos(2\psi) + h_\times\sin(2\psi)$. Solid-angle integration of the Isaacson stress-energy tensor $t^{\rm GW}_{\mu\nu} = \frac{c_0^4}{32\pi G}\langle\partial_\mu h^{\rm TT}_{ij}\partial_\nu h^{\rm TT\,ij}\rangle$ over $S^2$ ($\langle\Lambda_{ij,kl}Q_{ij}Q_{kl}\rangle_{S^2} = \frac{2}{5}Q_{ij}Q^{ij}$) yields Einstein's quadrupole power formula:
   $$P_{\rm GW} = \frac{G}{5 c_0^5}\bigl\langle \dddot{Q}_{ij}\dddot{Q}^{ij}\bigr\rangle.$$

---

## 2. Exact Symbolic Derivation of Peters–Mathews Factors $f(e), g(e)$ and Secular Decay Laws

For a Keplerian binary of masses $m_1, m_2$ ($M = m_1+m_2$, $\mu = m_1 m_2/M$, $\mathcal{M}_c = \mu^{3/5}M^{2/5}$), symbolic differentiation and orbit-averaging over $\theta \in [0, 2\pi]$ (`CHK_07`–`CHK_11`) establish:
$$\langle P_{\rm GW}\rangle = \frac{32}{5}\frac{G^4}{c_0^5}\frac{\mu^2 M^3}{a^5}\,f(e), \qquad f(e) = \frac{1 + \frac{73}{24}e^2 + \frac{37}{96}e^4}{(1 - e^2)^{7/2}},$$
$$\left\langle\frac{dJ_z}{dt}\right\rangle = -\frac{32}{5}\frac{G^{7/2}}{c_0^5}\frac{\mu^2 M^{5/2}}{a^{7/2}}\,g(e), \qquad g(e) = \frac{1 + \frac{7}{8}e^2}{(1 - e^2)^2},$$
and the secular orbital period decay rate:
$$\dot{P}_b^{\rm RefG} = -\frac{192\pi}{5}\left(\frac{2\pi G\mathcal{M}_c}{c_0^3 P_b}\right)^{5/3} f(e) = -\frac{192\pi}{5}\left(\frac{2\pi T_\odot}{P_b}\right)^{5/3}\frac{m_1 m_2}{(m_1+m_2)^{1/3}}\left(\frac{M_\odot^5}{M_\odot^3}\right) f(e),$$
together with the exact Peters (1964) orbital invariant $c_0(a,e) = a(1-e^2)e^{-12/19}[1 + \frac{121}{304}e^2]^{-870/2299}$ ($\frac{d}{dt}\ln c_0(a,e) \equiv 0$). Because $M_I = M_A = M_P = M_{\rm ADM}$ holds for all isolated bodies, the scalar sensitivity difference vanishes identically ($\Delta s_{12} = 0$), so monopole and dipole gravitational radiation are identically zero ($\dot{P}_b^{\rm dipole} \equiv 0$).

---

## 3. Quantitative Observational Benchmarks (`CHK_12`–`CHK_18`)

| Binary / Event | $P_b\text{ [days]}$ | $e$ | $f(e)$ | $\dot{P}_b^{\rm RefG}\text{ [s/s]}$ | $\dot{P}_b^{\rm int,obs}\text{ [s/s]}$ | Ratio $\text{obs}/\text{RefG}$ | Tension |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PSR B1913+16** (Hulse–Taylor; Weisberg & Huang 2016) | $0.32299745$ | $0.6171340$ | $11.8568$ | $-2.4021\times 10^{-12}$ | $(-2.398 \pm 0.004)\times 10^{-12}$ | $0.9983 \pm 0.0017$ | $1.03\sigma$ |
| **PSR J0737-3039A/B** (Double Pulsar; Kramer et al. 2021) | $0.10225156$ | $0.0877770$ | $1.0515$ | $-1.24781\times 10^{-12}$ | $(-1.24775 \pm 0.00008)\times 10^{-12}$ | $0.999953 \pm 0.000063$ | $0.74\sigma$ ($4.7\times 10^{-5}$) |
| **PSR J1738+0333** (NS–WD Dipole Test; Freire et al. 2012) | $0.35479074$ | $3.4\times 10^{-7}$ | $1.0000$ | $-2.759\times 10^{-14}$ | $(-2.59 \pm 0.32)\times 10^{-14}$ | $0.939 \pm 0.116$ | $0.53\sigma$ |

- **Five-Parameter PK Intersection in PSR J0737-3039A/B (`CHK_15`):** At $(m_A, m_B) = (1.338185, 1.248868)\,M_\odot$, RefG simultaneously reproduces periastron advance $\dot{\omega}^{\rm 1PN} = 16.8994^\circ/\text{yr}$ (obs: $16.89932^\circ/\text{yr}$), Einstein clock delay $\gamma_E^{\rm RefG} = 0.38400\text{ ms}$ (obs: $0.384045 \pm 0.000094\text{ ms}$, $0.51\sigma$), Shapiro range $r_{\rm Sh}^{\rm RefG} = 6.151\,\mu\text{s}$ (obs: $6.162 \pm 0.021\,\mu\text{s}$, $0.51\sigma$), and Shapiro shape $s_{\rm Sh}^{\rm RefG} = \sin i = 0.99992$ (obs: $0.99987_{-0.00048}^{+0.00013}$).
- **Coupled $(a(t), e(t))$ Coalescence Time (`CHK_17`):** Numerical `DOP853` integration of PSR B1913+16 down to coalescence gives $T_{\rm coal} = 300.70\text{ Myr}$, matching the analytical Peters (1964) integral to $3.58\times 10^{-15}$.
- **Cosmological GW Luminosity Distance (`CHK_18`):** On the operational $A = a/p = a^{5/2}$ geometry, the canonical tensor amplitude $\chi_k = A\,h_k$ obeys $\chi_k'' + (k^2 - A''/A)\chi_k = 0$ with $\alpha_M \equiv 0$, so $D_L^{\rm GW}(z) \equiv D_L^{\rm EM}(z) = (1+z)D_M(z)$.
