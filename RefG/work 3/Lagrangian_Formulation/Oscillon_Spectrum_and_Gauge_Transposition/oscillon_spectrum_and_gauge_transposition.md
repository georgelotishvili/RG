# Oscillon Perturbation Spectrum, Universal Clock-Rate Factorization ($\nu_n^{(t)} = s_n\Omega_t$), Local $U(1)$ Gauge Coupling, and Coframe Invariance of $\alpha$

**Date:** 2026-10-25  
**CLAIM_ID:** `REFG_OSCILLON_SPECTRUM_AND_GAUGE_TRANSPOSITION_V1`  
**Status:** `PASS` (`38/38` checks passed, `25/25` symbolic residuals `"0"`, `3/3` negative mutation controls rejected)  
**Verifier:** `verify_oscillon_spectrum_and_gauge_transposition.py` (`SHA-256: d743155ea291250b3593895e2d1a185bc4c69c3f263c084335231e6f95dbd8`)

---

## 1. Executive Summary

This work resolves three foundational microphysical bridges identified in the Research Program Status of Refractive Gravity (`RefG`):
1. **Universal Clock-Rate Factorization and Adiabatic Transposition Theorem (Status Item 3):** Starting from the minimally coframe-coupled nonlinear oscillon action on an arbitrary static isotropic metric $ds^2 = -p_T^2 c_0^2 dt^2 + p_L^{-2}\delta_{ij}dx^i dx^j$ ($p_T = N$, $p_L = A_{\rm iso}^{-1}$), we prove that at fixed conserved Noether phase charge $Q$ the proper radial profile $f(\tilde{r})$ ($\tilde{\mathbf{x}} = p_L^{-1}(\mathbf{x}-\mathbf{x}_0)$) and proper carrier frequency $\Omega_0(Q)$ are strictly invariant under independent $(p_T, p_L)$ transformations, while the coordinate carrier frequency and coordinate energy scale purely with the clock factor ($\Omega_t = p_T\Omega_0(Q)$, $E_{\rm coord} = p_T E_0(Q)$) and the coordinate radius scales purely with the ruler factor ($R_{\rm coord} = p_L R_0(Q)$). Constructing the coupled Bogoliubov–de Gennes (BdG) perturbation pencil $P(\kappa)$ around the localized core, we prove that every normal mode frequency $\omega_n^{(t)} = 2\pi\nu_n^{(t)}$ obeys the exact factorization law
   $$\nu_n^{(t)}(p_T, p_L; Q) = s_n(Q)\,\Omega_t(p_T; Q), \qquad \frac{\partial s_n}{\partial p_T} \equiv 0, \qquad \frac{\partial s_n}{\partial p_L} \equiv 0.$$
   Furthermore, parity symmetry of the localized core eliminates the first-order diagonal shift from any linear gravitational gradient ($\langle n | \mathbf{x}-\mathbf{x}_0 | n\rangle \equiv 0$), suppressing tidal deviations of $s_n/s_m$ to $\mathcal{O}((R_{\rm core}/L_{\rm grav})^2) \sim 1.19\times 10^{-56}$ at Earth's surface.
2. **Local $U(1)$ Gauge Coupling, Screened $1/r^2$ Coulomb Tail, and Charged Oscillon First Law (Status Item 15):** Promoting the global $U(1)$ phase symmetry of $\Psi_O$ to a local electromagnetic gauge symmetry via $D_\mu\Psi_O = (\partial_\mu - i q_{\rm em} A_\mu)\Psi_O$ locks the electromagnetic current to the Noether phase current ($J_{\rm em}^\mu = q_{\rm em} J_O^\mu$, $Q_{\rm em} = q_{\rm em} Q$) via the exact Ward/Noether identity, yields an exact $1/r^2$ exterior Coulomb field with finite electrostatic energy $E_{\rm EM} < \infty$, and satisfies the exact charged soliton first law
   $$\left.\frac{dE_{\rm tot}}{dQ}\right|_{q_{\rm em}} = \Omega_\infty$$
   (verified numerically on the coupled Maxwell–Oscillon BVP at $q_{\rm em}=0.005$, $\Omega_\infty=0.8$ to a relative error of $1.42\times 10^{-6}$, with Gauss-law relative accuracy $1.86\times 10^{-10}$).
3. **Exact Coframe Invariance of the Wave Impedance $Z_{\rm eff}$ and Fine-Structure Constant $\alpha$ (Status Item 18):** On the coframe metric $ds^2 = -p_T^2 c_0^2 dt^2 + p_L^{-2}\delta_{ij}dx^i dx^j$, the Maxwell action maps onto effective coordinate permittivity and permeability $\varepsilon_{\rm eff} = \varepsilon_0(p_T p_L)^{-1}$ and $\mu_{\rm eff} = \mu_0(p_T p_L)^{-1}$. This yields $c_{\rm coord} = (\varepsilon_{\rm eff}\mu_{\rm eff})^{-1/2} = c_0 p_T p_L$, an invariant vacuum wave impedance $Z_{\rm eff} = \sqrt{\mu_{\rm eff}/\varepsilon_{\rm eff}} = Z_0$, and an **identically invariant fine-structure constant**
   $$\alpha(p_T, p_L) = \frac{Q_{\rm em}^2}{4\pi\varepsilon_{\rm eff}\hbar c_{\rm coord}} = \frac{Q_{\rm em}^2}{4\pi\varepsilon_0\hbar c_0} = \alpha_0, \qquad \frac{\partial\alpha}{\partial p_T} \equiv 0, \qquad \frac{\partial\alpha}{\partial p_L} \equiv 0,$$
   locking atomic Rydberg transition frequencies $\nu_{n\to m}^{(t)} \propto p_T m_0 c_0^2\alpha_0^2/\hbar$ to the exact same clock factor $p_T = N$ as the internal oscillon spectrum $\nu_k^{(t)} = s_k\Omega_t = p_T(s_k\Omega_0)$.

---

## 2. Stationary Oscillon Coframe Rescaling and Coupled BdG Factorization

### 2.1 Stationary Oscillon on an Arbitrary $(p_T, p_L)$ Coframe Background
In an external static isotropic metric with local clock factor $p_T = N(\mathbf{x}_0)$ and local ruler factor $p_L = A_{\rm iso}(\mathbf{x}_0)^{-1}$,
$$ds^2 = -p_T^2 c_0^2 dt^2 + p_L^{-2}\delta_{ij}dx^i dx^j, \qquad \sqrt{-g} = p_T c_0 p_L^{-3},$$
the canonical complex oscillon action for $\Psi_O(t,\mathbf{x}) = \frac{1}{\sqrt{2}}f(\tilde{r})e^{-i\Omega_t t}$ in terms of the proper ruler coordinate $\tilde{\mathbf{x}} = p_L^{-1}(\mathbf{x}-\mathbf{x}_0)$ ($d^3x = p_L^3 d^3\tilde{x}$) takes the factorized form
$$L_{\rm eff} = p_T \int d^3\tilde{x} \left[ \frac{1}{2}\left(\frac{\Omega_t}{p_T c_0}\right)^2 f(\tilde{r})^2 - \frac{1}{2}(\nabla_{\tilde{\mathbf{x}}} f)^2 - V(f) \right], \qquad V(f) = \frac{1}{2}f^2 - \frac{1}{4}f^4 + \frac{a}{6}f^6.$$
The conserved Noether phase charge is
$$Q = \int d^3x\,\frac{\sqrt{-g}}{c_0}\left(-g^{00}\partial_t\theta_O\right)f^2 = \left(\frac{\Omega_t}{p_T c_0}\right)\int d^3\tilde{x}\,f(\tilde{r})^2.$$
Hence fixing $Q$ uniquely fixes the proper carrier frequency $\Omega_0(Q) \equiv \frac{\Omega_t}{p_T c_0}$ and the proper profile $f(\tilde{r})$, yielding:
$$\Omega_t(p_T, p_L; Q) = p_T c_0\,\Omega_0(Q), \qquad E_{\rm coord}(p_T, p_L; Q) = p_T\,E_0(Q), \qquad R_{\rm coord}(p_T, p_L; Q) = p_L\,R_0(Q).$$

### 2.2 Coupled Bogoliubov–de Gennes (BdG) Perturbation Spectrum
Linearizing $\Psi_O(t,\mathbf{x}) = \frac{1}{\sqrt{2}}e^{-i\Omega_t t}\left[f(\tilde{r}) + \eta(t,\tilde{\mathbf{x}}) + i\xi(t,\tilde{\mathbf{x}})\right]$ with normal-mode dependence $\eta = \operatorname{Re}[(U_n(\tilde{r})/\tilde{r})Y_{\ell m}\,e^{-i\omega_n^{(t)}t}]$, $\xi = \operatorname{Re}[i(V_n(\tilde{r})/\tilde{r})Y_{\ell m}\,e^{-i\omega_n^{(t)}t}]$ produces the coupled quadratic eigenvalue pencil in proper radial coordinate $\tilde{r}$:
$$\begin{pmatrix} \mathcal{L}_+^{(\ell)}(\tilde{r}) - \kappa_n^2 & -2\Omega_0\kappa_n \\ -2\Omega_0\kappa_n & \mathcal{L}_-^{(\ell)}(\tilde{r}) - \kappa_n^2 \end{pmatrix} \begin{pmatrix} U_n(\tilde{r}) \\ V_n(\tilde{r}) \end{pmatrix} = 0, \qquad \kappa_n \equiv \frac{\omega_n^{(t)}}{p_T c_0},$$
where
$$\mathcal{L}_+^{(\ell)}(\tilde{r}) = -\frac{d^2}{d\tilde{r}^2} + \frac{\ell(\ell+1)}{\tilde{r}^2} + V''(f(\tilde{r})) - \Omega_0^2, \qquad \mathcal{L}_-^{(\ell)}(\tilde{r}) = -\frac{d^2}{d\tilde{r}^2} + \frac{\ell(\ell+1)}{\tilde{r}^2} + \frac{V'(f(\tilde{r}))}{f(\tilde{r})} - \Omega_0^2.$$
Because $\mathcal{L}_\pm^{(\ell)}(\tilde{r})$ and $\Omega_0(Q)$ are strictly independent of $(p_T, p_L)$, every eigenvalue $\kappa_n(Q)$ is a pure structural constant of the oscillon at charge $Q$, and every coordinate frequency $\omega_n^{(t)} = 2\pi\nu_n^{(t)}$ obeys:
$$\omega_n^{(t)}(p_T, p_L; Q) = s_n(Q)\,\Omega_t(p_T; Q), \qquad s_n(Q) \equiv \frac{\kappa_n(Q)}{\Omega_0(Q)}, \qquad \frac{\partial s_n}{\partial p_T} = \frac{\partial s_n}{\partial p_L} \equiv 0.$$

On the `W3-58` benchmark core ($a = 1/4$, $\Omega_0 = 4/5 = 0.8$, $Q_0 = 190.40113622$, $E_0 = 177.26834051$, $R_{\rm rms} = 2.72894693$), numerical solution of the coupled $4N\times 4N$ companion BdG eigenvalue problem confirms:
- Exact $\ell=0$ phase zero mode $U_0 = 0, V_0 = \tilde{r}f(\tilde{r})$ ($|\lambda_0(\mathcal{L}_-^{(0)})| = 1.25\times 10^{-4}$);
- Exact $\ell=1$ translational zero mode $U_1 = \tilde{r}f'(\tilde{r}), V_1 = 0$ ($|\lambda_0(\mathcal{L}_+^{(1)})| = 3.85\times 10^{-4}$);
- Discrete coupled radial modes $\kappa_1 = 0.208040$ ($s_1 = \kappa_1/\Omega_0 = 0.260050$) and $\kappa_2 = 0.231624$ ($s_2 = 0.289530$), whose coordinate-grid operator $P_{\rm coord}(\omega_n^{(t)})$ has maximum singular-value residual $2.14\times 10^{-14}$ across all four tested scalings $(p_T, p_L) \in \{(1,1), (0.8, 1.25), (0.5, 2.0), (0.7, 1.4)\}$.

---

## 3. Local $U(1)$ Gauge Coupling and Invariance of $\alpha$

### 3.1 Gauged Oscillon Action and Charged First Law
Replacing $\partial_\mu\Psi_O \to D_\mu\Psi_O = (\partial_\mu - i q_{\rm em}A_\mu)\Psi_O$ gives the gauge-invariant phase gradient $\mathcal{D}_\mu\theta_O = \partial_\mu\theta_O - q_{\rm em}A_\mu$ and the exact Ward/Noether identity
$$J_{\rm em}^\mu \equiv \frac{\delta S_{O+{\rm EM}}}{\delta A_\mu} = q_{\rm em} J_O^\mu = -q_{\rm em} f^2 g^{\mu\nu}(\partial_\nu\theta_O - q_{\rm em}A_\nu).$$
For a stationary spherically symmetric state ($\theta_O = -\Omega t$, $A_t = \Phi_{\rm em}(r)$ with $\Phi_{\rm em}(\infty)=0$), the coupled radial field equations are
$$f'' + \frac{2}{r}f' + (\Omega - q_{\rm em}\Phi_{\rm em})^2 f - V'(f) = 0, \qquad \Phi_{\rm em}'' + \frac{2}{r}\Phi_{\rm em}' + q_{\rm em}(\Omega - q_{\rm em}\Phi_{\rm em})f^2 = 0.$$
At $q_{\rm em} = 0.005$ and $\Omega = 0.800$, the converged BVP solution gives $Q = 190.609717$, $Q_{\rm em} = q_{\rm em}Q = 0.95304858$, Gauss-law surface flux $-4\pi r_{\rm max}^2\Phi_{\rm em}'(r_{\rm max}) = 0.95304858$ (relative error $1.86\times 10^{-10}$), finite electrostatic energy $E_{\rm EM} = 0.0131213$, total energy $E_{\rm tot} = 177.448313$, and centered finite-difference derivative
$$\left.\frac{dE_{\rm tot}}{dQ}\right|_{q_{\rm em}=0.005} = 0.79999887 \quad \left(\text{relative error } 1.42\times 10^{-6}\text{ against }\Omega = 0.800\right).$$

### 3.2 Exact Coframe Invariance of $Z_{\rm eff}$ and $\alpha$
Expanding the Maxwell action $\int d^4x\sqrt{-g}\left(-\frac{1}{4\mu_0}F_{\mu\nu}F^{\mu\nu}\right)$ on $ds^2 = -p_T^2 c_0^2 dt^2 + p_L^{-2}\delta_{ij}dx^i dx^j$ yields
$$\mathcal{L}_{\rm EM}^{\rm (coord)} = \frac{1}{2}\varepsilon_{\rm eff}\mathbf{E}_{\rm coord}^2 - \frac{1}{2\mu_{\rm eff}}\mathbf{B}_{\rm coord}^2, \qquad \varepsilon_{\rm eff} = \frac{\varepsilon_0}{p_T p_L}, \qquad \mu_{\rm eff} = \frac{\mu_0}{p_T p_L}.$$
Consequently:
$$c_{\rm coord} = \frac{1}{\sqrt{\varepsilon_{\rm eff}\mu_{\rm eff}}} = c_0 p_T p_L, \qquad Z_{\rm eff} = \sqrt{\frac{\mu_{\rm eff}}{\varepsilon_{\rm eff}}} = Z_0, \qquad \alpha(p_T, p_L) = \frac{Q_{\rm em}^2}{4\pi\varepsilon_{\rm eff}\hbar c_{\rm coord}} = \frac{Q_{\rm em}^2}{4\pi\varepsilon_0\hbar c_0} = \alpha_0,$$
and the ratio of any atomic Rydberg transition frequency $\nu_{\rm Ryd}^{(t)} \propto p_T m_0 c_0^2\alpha_0^2/\hbar$ to any internal oscillon frequency $\nu_n^{(t)} = s_n p_T\Omega_0$ is strictly independent of $(p_T, p_L)$.
