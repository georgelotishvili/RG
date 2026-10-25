# Action-Derived $C^2$-Matched Regular Interior Closure for the Covariant Medium (`W3-92`)

2026-10-25. Research contract, exact derivation, and symbolic/numerical BVP verification supplement.
MODEL_VERSION=`REFG_STRONG_FIELD_COVARIANT_MEDIUM_C2_INTERIOR_V1`.

## Decision and scope

In the strong-field covariant medium formulation ([`FORMAL_COVARIANT_MEDIUM_INTEGRATION.md`](FORMAL_COVARIANT_MEDIUM_INTEGRATION.md)), the silent exponential exterior
$$\mathcal{A}_+(r) = e^{2m/r}, \qquad \mathcal{B}_+(r) = e^{-2m/r}, \qquad H_+(r) = \frac{m}{r}, \qquad \Phi = t, \qquad \phi^A = x^A \qquad (r \ge r_c)$$
is an exact solution of all five medium Euler–Lagrange equations and all ten Einstein equations for any $C^2$ response $F(\widehat{Y}, \widehat{I}_1, \widehat{I}_2, \widehat{I}_3)$ with a silent isotropic point at $(\widehat{Y}, \widehat{B}^{AB}) = (1, \delta^{AB})$ and $\omega_H = 1$. On $x = r/r_c \in [0, 1]$, a horizonless, geodesically complete $C^2$-matched core geometry is constructed, and its action-derived realization requires regular profiles of $H$, $\Phi$, and $\phi^A$ satisfying the flux condition $Q_H(r_c) = m$ together with a minimally coupled interior matter sector $T^{\rm m}_{\mu\nu}$.

Earlier audits in [`common_scale_centre_source.md`](common_scale_centre_source.md) (§§1–11) proved that imposing the locked common-scale ansatz $\mathcal{A}(r)\mathcal{B}(r) = 1$ ($\ell_A + \ell_B = 0$) inside the core prevents a regular join. However, the degree-6 $C^2$ core geometry explicitly releases the clock–ruler lock inside the core:
$$\ln\bigl(\mathcal{A}_-(x)\mathcal{B}_-(x)\bigr) = \ell_A(x) + \ell_B(x) = q(x^2 - 1)^3 < 0 \qquad \forall x \in [0, 1).$$

This package derives the exact interior field equations, boundary vanishing-order theorems, and radial BVP solution on $x \in [0, 1]$ for the unlocked $C^2$ core geometry:
1. **Exact Interior ODEs, Divergence-Free Label-Traction Theorem, and Boundary Order-Lowering Law:**
   - Proves the exact off-shell radial reparameterization Noether identity and proves that the constitutive chain rule $df/dx = d(\ln y)' + a(\ln b_r)' + c(\ln b_t)'$ is identically equivalent to the radial label Euler–Lagrange equation $E_\ell(x) = 0$ whenever the Einstein, $H$, and covariant matter-conservation equations hold.
   - Proves the exact divergence-free universal label-traction theorem on any $C^1$-matched interior (`Theorem 1`), showing that on the degree-6 $C^2$ core geometry the pure-medium geometric integral is strictly positive ($\mathcal{I}_{\rm met}(q) > 0$ for all $q > 0$), thereby proving rigorously why a minimally coupled core matter sector $T^{\rm m}_{\mu\nu}$ is mathematically required (`Theorem 2`).
   - Proves the boundary order-lowering theorem at $x = 1^-$ ($\text{ord}_{x\to 1^-}(a) = \text{ord}_{x\to 1^-}(c) + 1 \ge 2$) and proves that $H(x) = -\frac{1}{2}\ell_B(x)$ simultaneously satisfies regular central parity ($Q_H(0) = 0$), exact $C^2$ exterior matching ($Q_H(r_c) = m$), and the 3rd- and 4th-derivative label-regularity conditions $a'(1^-) = 0$ and $a''(1^-) = c'(1^-)$ (`Theorem 3`).
2. **Exact Radial BVP Solution, Single-Valued Constitutive Closure, and Optical Light-Ring Verification:**
   - Solves the interior radial label BVP with the covariantly conserved, positive-density core matter profile $\rho_{\rm m}(x) = (P/r_c^2)\rho_0^*(1 - x^2)^3$, proving that $a(x) = Q b_r F_r(x) < 0$ on $[0, 1)$ (positive radial label kinetic sign), $Q C_\ell(x) < 0$ on $(0, 1)$, $\ell(x)$ is smooth and strictly monotonic with $\ell(0) = 0, \ell(1) = r_c, \ell'(1) = 1$, and the principal strain invariants $\bigl(\widehat{I}_1(x), \widehat{I}_3(x)\bigr)$ are strictly monotonically decreasing on $[0, 1]$, guaranteeing a single-valued $C^2$ constitutive function $F(\widehat{Y}, \widehat{I}_1, \widehat{I}_2, \widehat{I}_3)$ with zero chain-rule residual.
   - Verifies the global optical potential $V_\pm(r)$, the outer unstable photon sphere at $r_{\rm ph} = 2m = r_s$ with critical impact parameter $b_c = 2e m$ ($\delta_{\rm exp} = \frac{2e}{3\sqrt{3}} - 1 \approx 0.046297$), and the unique radially stable inner light ring inside the core ($x_{\rm lr} = 0.8705805856$ at $q = 3/2$).

All symbolic and numerical claims are verified by [`verify_action_derived_c2_interior_closure.py`](verify_action_derived_c2_interior_closure.py) and recorded in [`action_derived_c2_interior_closure_result.json`](action_derived_c2_interior_closure_result.json).

---

## Frozen claims and verification contract

| Field | Contract |
|---|---|
| CLAIM_ID | `REFG_ACTION_DERIVED_C2_INTERIOR_CLOSURE_V1` |
| CLAIM | On the $C^2$-matched horizonless core geometry, (i) the universal divergence-free label-traction identity proves that a pure-medium realization ($T^{\rm m}_{\mu\nu}=0$) has $Q C_\ell(r_c) > 0$ for all $H(x)$ and $q>0$, requiring a minimally coupled core matter sector; (ii) the regular deficit profile $H(x) = -\frac{1}{2}\ell_B(x)$ and covariantly conserved core matter $\rho_{\rm m}(x) = (P/r_c^2)\rho_0^*(1-x^2)^3$ satisfy all 5 medium Euler–Lagrange equations, all 3 Einstein equations, $\nabla_\mu T^{\rm m\,\mu}{}_\nu = 0$, $Q_H(0)=0, Q_H(r_c)=m$, $a(x)<0$ on $[0,1)$, strict monotonicity of $\ell(x)$, $\widehat{I}_1(x)$, and $\widehat{I}_3(x)$ on $[0,1]$, and zero constitutive chain-rule residual; (iii) the matched geometry possesses the exact outer unstable light ring at $r_{\rm ph}=2m$ ($b_c=2em$) and unique radially stable inner light ring on $1<q<2$. |
| TYPE | Action-derived exact theorems (radial Noether/chain-rule equivalence, divergence-free label-traction identity, boundary order-lowering theorem) and symbolic/high-precision numerical BVP verification. |
| MODEL_VERSION | `REFG_STRONG_FIELD_COVARIANT_MEDIUM_C2_INTERIOR_V1` (compatible with [`FORMAL_COVARIANT_MEDIUM_INTEGRATION.md`](FORMAL_COVARIANT_MEDIUM_INTEGRATION.md) at $\omega_H = 1$). |
| ASSUMPTIONS | Static spherically symmetric isotropic coordinates $ds^2 = -\mathcal{B}(r)dt^2 + \mathcal{A}(r)(dr^2 + r^2 d\Omega^2)$ in positive-spatial signature $(-,+,+,+)$; $\Phi = t$, $\phi^A = \ell(r)n^A$, $H = H(r)$; $\omega_H = 1$; $P = M_{\rm Pl}^2 = (8\pi G)^{-1} > 0$, $Q = M_*^4 > 0$; $1 < q = 2m/r_c \le q_* \approx 1.990069$. |
| DOMAIN | Symbolic identities hold on all static regular spherically symmetric configurations on $x = r/r_c \in [0, 1]$ matched $C^2$ to the exponential exterior on $x \ge 1$. Numerical BVP and quadrature checks evaluated across $q \in \{1.2, 1.5, 1.8\}$ with primary witness $q = 3/2$. |
| CONVENTIONS | $x = r/r_c \in [0, 1]$; $\ell_A(x) = \ln\mathcal{A}_-(x)$, $\ell_B(x) = \ln\mathcal{B}_-(x)$; $N = e^{\ell_B/2}$, $A = e^{\ell_A/2}$, $S = r_c x e^{\ell_A/2}$; $\sqrt{-g}/\sin\theta = r_c^2 x^2 e^{(3\ell_A+\ell_B)/2}$; $y = e^{-2H-\ell_B}$, $b_r = e^{2H-\ell_A}(\ell')^2$, $b_t = e^{2H-\ell_A}(\ell/r)^2$. |
| FREEDOM_LEDGER | Core metric profiles $\ell_A(x), \ell_B(x)$ fixed to the degree-6 $C^2$ core ansatz. Deficit profile $H(x) = -\frac{1}{2}\ell_B(x)$ uniquely selected by the 5 boundary conditions at $x=1$. Core matter eigenvalue $\rho_0^*(q)$ uniquely fixed by the integral constraint $Q C_\ell(r_c) = 0$. No free fitting parameters. |
| DEPENDENCIES | [`FORMAL_COVARIANT_MEDIUM_INTEGRATION.md`](FORMAL_COVARIANT_MEDIUM_INTEGRATION.md), [`common_scale_centre_source.md`](common_scale_centre_source.md), [`verify_common_scale_centre_source.py`](verify_common_scale_centre_source.py), pinned by SHA-256. |
| METHOD | SymPy exact symbolic proof of off-shell radial Noether identity, chain-rule equivalence, divergence-free label-traction identity, boundary order-lowering law, central curvature/stress formulas, and light-ring cubic; SciPy `quad` (tolerance $10^{-14}$) and dense-grid BVP integration for $\rho_0^*(q)$, $\ell(x)$, $(b_r(x), b_t(x))$, and ODE/chain-rule residuals. |
| PASS_CONDITION | All symbolic residuals identically `0`; pure-medium traction integral $\mathcal{I}_{\rm met}(q) > 0$ verified for $q \in \{1.2, 1.5, 1.8\}$; boundary traction residual $|Q C_\ell(r_c)| < 10^{-14}$; $a(x) < 0$ on $[0, 1)$ and $Q C_\ell(x) < 0$ on $(0, 1)$; $\ell'(x) > 0$ on $[0, 1]$ with $|\ell(1)/r_c - 1| < 10^{-12}$ and $|\ell'(1) - 1| < 10^{-6}$; strict monotonicity of $\widehat{I}_1(x)$ and $\widehat{I}_3(x)$ on $[0, 1]$; numerical chain-rule and label ODE residual $< 10^{-9}$; 5 negative controls rejected. |
| FAIL_CONDITION | Any nonzero symbolic residual, sign flip of $a(x)$ or $Q C_\ell(x)$ inside $(0, 1)$, non-monotonicity of $\ell(x)$ or $(\widehat{I}_1, \widehat{I}_3)$, or upstream SHA-256 mismatch. |
| FALSIFIER | Any failure of the constitutive chain rule along $\gamma(x)$ or failure of $Q C_\ell(r_c) = 0$ at the eigenvalue $\rho_0^*(q)$. |
| RESIDUAL | Symbolic residuals and numerical quadrature/ODE residuals stored separately in [`action_derived_c2_interior_closure_result.json`](action_derived_c2_interior_closure_result.json). |
| ERROR_BOUND | Adaptive Gauss–Kronrod quadrature (`scipy.integrate.quad`, `epsabs=1e-14, epsrel=1e-14`) and $L^\infty$ ODE residual checks on $N = 4001$ interior nodes. |
| VALIDITY_HEALTH | Everywhere positive metric functions $\mathcal{A}_-, \mathcal{B}_- > 0$; strictly monotonic areal radius $R_{\rm ar}'(x) > 0$ for $1 < q \le q_*$; negative radial strain derivative $F_r(x) < 0$ on $[0, 1)$ (positive radial label kinetic energy); positive core matter density $\rho_{\rm m}(x) > 0$ on $[0, 1)$; elliptic $H$–$H$ principal symbol $\mathcal{P}_{HH}(k) = M_{\rm Pl}^2 \gamma^{\mu\nu}k_\mu k_\nu > 0$. |
| BRANCHES | Unlocked $C^2$ core branch ($\mathcal{A}_-\mathcal{B}_- = e^{q(x^2-1)^3} < 1$ on $[0,1)$) smoothly joining the exact common-scale exponential exterior ($\mathcal{A}_+\mathcal{B}_+ = 1$) at $x = 1$. |
| OBSERVABLE_MAP | ADM mass $M_{\rm ADM} = m/G$, outer photon sphere $r_{\rm ph} = 2m$, critical impact parameter $b_c = 2e m$ ($\delta_{\rm exp} \approx +4.63\%$), inner stable light ring $r_{\rm lr,-} = r_c x_{\rm lr}$, central redshift $\sqrt{\mathcal{B}(0)} = e^{-q/2}$. |
| FORWARD_MODEL | Ray-geometric optical potential $V_\pm(r) = \mathcal{B}_\pm(r)/[\mathcal{A}_\pm(r)r^2]$ and critical impact parameter $b_c = 1/\sqrt{V_+(r_{\rm ph})}$. |
| DATA_ROLE | Purely theoretical/mathematical verification; EHT Sgr A* bounds are orientation benchmarks only. |
| IDENTIFIABILITY | Separates the exterior metric/optical predictions (which depend only on the silent point of $F$ and $\omega_H = 1$) from the interior core profiles $(H(x), \ell(x), \rho_{\rm m}(x))$. |
| BENCHMARK | Exact agreement with all analytical formulas in [`FORMAL_COVARIANT_MEDIUM_INTEGRATION.md`](FORMAL_COVARIANT_MEDIUM_INTEGRATION.md) and [`common_scale_centre_source.md`](common_scale_centre_source.md) §§8–11. |
| CLOSURE_FLAGS | Closes exact interior ODEs, $r \to 0$ Taylor germ, $C^2$ exterior matching, single-valued constitutive closure on $r \in [0, r_c]$, and optical potential verification. Full non-radial coupled perturbation stability remains a separate task. |
| CROSSCHECK | Symbolic chain-rule identity vs numerical finite-difference verification along solved $\ell(x)$; divergence-free integral formula vs direct quadrature of $r_c\sqrt{-g}(a+c)$; analytical L'Hôpital limit $\ell'(1) = a''(1^-)/c'(1^-) = 1$ vs numerical BVP boundary slope. |
| PROVENANCE | SHA-256 hashes of all upstream files and generated outputs recorded in [`action_derived_c2_interior_closure_result.json`](action_derived_c2_interior_closure_result.json). |
| FILES | `RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/action_derived_c2_interior_closure.md`, `RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_action_derived_c2_interior_closure.py`, `RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/action_derived_c2_interior_closure_result.json`. |

---

## 1. Exact Interior Field Equations and Analytical Theorems

### 1.1 Reduced 1D Radial Action and Algebraic Source Inversion

In static spherically symmetric coordinates with line element
$$ds^2 = -N(r)^2\,dt^2 + A(r)^2\,dr^2 + S(r)^2\,d\Omega^2,$$
clock $\Phi = t$, radial material labels $\phi^A = \ell(r)n^A$ ($n^A = x^A/r$), and deficit scalar $H = H(r)$, the normalized invariants of [`FORMAL_COVARIANT_MEDIUM_INTEGRATION.md`](FORMAL_COVARIANT_MEDIUM_INTEGRATION.md) are
$$y(r) = \widehat{Y}(r) = \frac{e^{-2H(r)}}{N(r)^2}, \qquad b_r(r) = \frac{e^{2H(r)}(\ell'(r))^2}{A(r)^2}, \qquad b_t(r) = \frac{e^{2H(r)}\ell(r)^2}{S(r)^2}.$$
Writing $\bar{F}(y, b_r, b_t) \equiv F(\widehat{Y}, \widehat{I}_1, \widehat{I}_2, \widehat{I}_3)$ on the axisymmetric strain spectrum $(b_r, b_t, b_t)$ (so that $F_t \equiv \partial\bar{F}/\partial b_t$ sums over both tangential eigenvalues), the reduced 1D radial Lagrangian for the gravitational + medium sector ($P = M_{\rm Pl}^2 = (8\pi G)^{-1}, Q = M_*^4, \omega_H = 1$) is
$$L_{\rm rad}(N, A, S, H, \ell) = P\left[N A + \frac{N(S')^2 + 2 N' S S'}{A}\right] + N A S^2\left[Q\bar{F}(y, b_r, b_t) + P\frac{(H')^2}{A^2}\right].$$
Varying $N, A, S, H, \ell$ independently before specializes to isotropic coordinates $N = e^{\ell_B/2}, A = e^{\ell_A/2}, S = r e^{\ell_A/2}$ ($\mathcal{A} = e^{\ell_A}, \mathcal{B} = e^{\ell_B}, \sqrt{-g}/\sin\theta = N A S^2 = r^2 e^{(3\ell_A+\ell_B)/2}$) and including a covariantly conserved, minimally coupled core matter stress–energy tensor $T^{\rm m\,\mu}{}_\nu = \mathrm{diag}(\rho_{\rm m}, -p_{r,\rm m}, -p_{t,\rm m}, -p_{t,\rm m})$ yields the exact algebraic inversion for the four medium constitutive quantities
$$f(r) \equiv Q\bar{F}(r), \qquad d(r) \equiv Q y(r) F_y(r), \qquad a(r) \equiv Q b_r(r) F_r(r), \qquad c(r) \equiv Q b_t(r) F_t(r):$$
$$\begin{aligned}
f(r) &= \frac{S_\rho(r) + S_r(r) + 2 S_t(r)}{2} - J_g(r), \\
d(r) &= \frac{3 S_\rho(r) + S_r(r) + 2 S_t(r)}{4} - \frac{1}{2}J_g(r), \\
a(r) &= \frac{S_\rho(r) - S_r(r) + 2 S_t(r)}{4} - \frac{1}{2}J_g(r), \\
c(r) &= \frac{S_\rho(r) + S_r(r)}{2} - J_g(r),
\end{aligned}$$
where $S_\rho \equiv \rho_{\rm geom} + P e^{-\ell_A}(H')^2 - \rho_{\rm m}$, $S_r \equiv p_{r,\rm geom} + P e^{-\ell_A}(H')^2 - p_{r,\rm m}$, $S_t \equiv p_{t,\rm geom} - P e^{-\ell_A}(H')^2 - p_{t,\rm m}$, and
$$J_g(r) \equiv -\frac{P}{\sqrt{-g}}\frac{d}{dr}\!\left(r^2 e^{(\ell_A+\ell_B)/2} H'(r)\right) = \frac{P}{\sqrt{-g}}\frac{d Q_H(r)}{dr} = d(r) - a(r) - c(r).$$

---

### 1.2 Three Exact Structural Theorems

#### Theorem 1 (Off-Shell Radial Reparameterization Identity and Chain-Rule Equivalence)

> **Statement.**
> 1. The reduced radial Lagrangian $L_{\rm rad}(N, A, S, H, \ell)$ satisfies the exact off-shell radial diffeomorphism Noether identity
>    $$E_N N' + E_A A' + E_S S' + E_H H' + E_\ell \ell' - \frac{d}{dr}\bigl(A E_A\bigr) \equiv 0.$$
> 2. Separating $L_{\rm rad} = L_{\rm grav+H}(N, A, S, H) + N A S^2 Q\bar{F}(y, b_r, b_t)$, the medium sector satisfies the exact algebraic identity
>    $$E_N^{(F)} N' + E_A^{(F)} A' + E_S^{(F)} S' + E_H^{(F)} H' + E_\ell^{(F)} \ell' - \frac{d}{dr}\bigl(A E_A^{(F)}\bigr) \equiv -N A S^2\left[f'(r) - \left(d(r)\frac{y'(r)}{y(r)} + a(r)\frac{b_r'(r)}{b_r(r)} + c(r)\frac{b_t'(r)}{b_t(r)}\right)\right].$$
> 3. Consequently, whenever $(f, d, a, c)$ are defined by the Einstein and $H$ equations and the core matter stress tensor is covariantly conserved ($\nabla_\mu T^{\rm m\,\mu}{}_r = 0$), the constitutive chain rule along $(y(r), b_r(r), b_t(r))$ is **identically equivalent** to the radial label Euler–Lagrange equation $E_\ell(r) = 0$:
>    $$f'(r) - \left(d(r)\frac{y'(r)}{y(r)} + a(r)\frac{b_r'(r)}{b_r(r)} + c(r)\frac{b_t'(r)}{b_t(r)}\right) \equiv \frac{\ell'(r)}{N(r)A(r)S(r)^2}\,E_\ell^{(F)}(r) = 0.$$

---

#### Theorem 2 (Universal Divergence-Free Label-Traction Identity and Necessity of Core Matter on the Degree-6 $C^2$ Core)

> **Statement.** Define the radial label current $Q C_\ell(r) \equiv \sqrt{-g}(r)\,a(r)\,\frac{\ell(r)}{\ell'(r)}$, whose radial Euler–Lagrange equation $E_\ell = 0$ is $\frac{d}{dr}(Q C_\ell) = \sqrt{-g}\,(a + c)$.
> 1. In dimensionless radius $x = r/r_c \in [0, 1]$, the medium contribution to $r_c\sqrt{-g}\,(a + c)$ obeys the exact differential identity:
>    $$r_c\sqrt{-g}(x)\bigl(a_{\rm med}(x) + c_{\rm med}(x)\bigr) \equiv \frac{P r_c}{8}\frac{d}{dx}\!\left[x^2 e^{(\ell_A+\ell_B)/2}\bigl(12 H' - 4\ell_A' + 2\ell_B'\bigr)\right] + \frac{P r_c}{8} x^2 e^{(\ell_A+\ell_B)/2}\left[\ell_A'\bigl(\ell_A' + 2\ell_B'\bigr) + 4(H')^2\right].$$
> 2. On **any** regular interior $(\ell_A(x), \ell_B(x), H(x))$ that matches $C^1$ to the exponential exterior at $x = 1$ ($\ell_A(1) = q, \ell_B(1) = -q, \ell_A'(1) = -q, \ell_B'(1) = q, H'(1) = -q/2$), the boundary combination $12 H'(1) - 4\ell_A'(1) + 2\ell_B'(1) = -6q + 4q + 2q = 0$ vanishes identically at $x = 1$ (and as $O(x^3)$ at $x = 0$). Integrating over $x \in [0, 1]$ yields the **exact boundary-term-free global traction theorem**:
>    $$\frac{Q C_\ell(r_c)}{P r_c} = \frac{1}{8}\int_0^1 x^2 e^{(\ell_A+\ell_B)/2}\left[\ell_A'(x)\bigl(\ell_A'(x) + 2\ell_B'(x)\bigr) + 4(H'(x))^2\right]dx - \frac{r_c^2}{4P}\int_0^1 x^2 e^{(3\ell_A+\ell_B)/2}\bigl(3\rho_{\rm m} + p_{r,\rm m} + 2 p_{t,\rm m}\bigr)\,dx.$$
> 3. For the target degree-6 $C^2$ core geometry,
>    $$\ell_A'(x) + 2\ell_B'(x) = \frac{q x}{4}\bigl(13 - 12 x^2 + 3 x^4\bigr) = \frac{q x}{4}\left[3(x^2 - 2)^2 + 1\right] > 0 \qquad \forall x \in (0, 1],$$
>    and the pure-metric integral $\mathcal{I}_{\rm met}(q) \equiv \frac{1}{8}\int_0^1 x^2 e^{(\ell_A+\ell_B)/2}\ell_A'(\ell_A' + 2\ell_B')\,dx$ is strictly positive for all $q > 0$ ($\mathcal{I}_{\rm met}(3/2) = 0.019037742879 > 0$). Since $4(H'(x))^2 \ge 0$ pointwise for every real function $H(x)$, any pure-medium configuration ($T^{\rm m}_{\mu\nu} = 0$) on the degree-6 $C^2$ core has $Q C_\ell(r_c) / (P r_c) \ge \mathcal{I}_{\rm met}(q) > 0$ and cannot satisfy the zero-traction boundary condition $C_\ell(r_c) = 0$. Realizing the $C^2$ core with zero boundary traction therefore **strictly requires** a non-zero minimally coupled core matter sector $T^{\rm m}_{\mu\nu}$.

---

#### Theorem 3 (Boundary Order-Lowering Law and Exact Selection of $H(x) = -\frac{1}{2}\ell_B(x)$)

> **Statement.**
> 1. Because $Q C_\ell(r) = \sqrt{-g}(r)\frac{\ell(r)}{\ell'(r)}a(r)$ and $\frac{d}{dr}(Q C_\ell) = \sqrt{-g}(a + c)$, any interior solution with smooth invertible label profile $\ell(r_c) = r_c > 0, 0 < \ell'(r_c) < \infty$ and continuous stresses at $r = r_c$ ($a(r_c^-) = c(r_c^-) = 0$) must obey the **boundary order-lowering law**:
>    $$\operatorname{ord}_{x \to 1^-}\bigl(a(x)\bigr) = \operatorname{ord}_{x \to 1^-}\bigl(c(x)\bigr) + 1 \ge 2 \implies a(1^-) = 0, \quad a'(1^-) = 0, \quad c(1^-) = 0,$$
>    with boundary slope ratio
>    $$\lim_{x \to 1^-}\frac{x\,\ell'(x)}{\ell(x)} = \frac{a''(1^-)}{c'(1^-)}.$$
> 2. On any $C^2$-matched interior metric $(\ell_A(x), \ell_B(x))$ with core matter vanishing as $O((1-x)^3)$ at $x = 1$, the first derivatives of $a(x)$ and $c(x)$ at $x = 1^-$ are
>    $$a'(1^-) = \frac{P e^{-q}}{4 r_c^2}\bigl(2\,\Delta H''' + \Delta\ell_B'''\bigr), \qquad c'(1^-) = \frac{P e^{-q}}{2 r_c^2}\bigl(2\,\Delta H''' - \Delta\ell_A'''\bigr),$$
>    where $\Delta f''' \equiv f'''(1^-) - f_{\rm ext}'''(1)$. Thus $a'(1^-) = 0$ holds if and only if $H'''(1^-) = -\frac{1}{2}\ell_B'''(1^-) = \frac{51}{2}q$, and $\ell'(1^-) = 1$ ($a''(1^-) = c'(1^-)$) holds if and only if $H^{(4)}(1^-) = -\frac{1}{2}\ell_B^{(4)}(1^-) = \frac{261}{2}q$.
> 3. The unique degree-6 even polynomial in $x$ satisfying all five boundary conditions at $x = 1$ ($H(1) = q/2, H'(1) = -q/2, H''(1) = q, H'''(1) = \frac{51}{2}q, H^{(4)}(1) = \frac{261}{2}q$) is
>    $$H(x) = -\frac{1}{2}\ell_B(x) = \frac{q}{2} + \frac{q}{16}\bigl(11 x^2 - 18 x^4 + 7 x^6\bigr) = q\left[\frac{1}{2} + \frac{1}{4}(1-x^2) + \frac{3}{16}(1-x^2)^2 - \frac{7}{16}(1-x^2)^3\right].$$
>    On this profile:
>    - $\widehat{Y}(x) = e^{-2H(x)-\ell_B(x)} \equiv 1$ throughout the core,
>    - $Q_H(0) = 0$ and $Q_H(r_c) = -r_c e^{(\ell_A(1)+\ell_B(1))/2} H'(1) = \frac{q r_c}{2} = m$,
>    - the medium active combination satisfies $f_{\rm med}(x) \equiv 0$,
>    - the medium radial strain derivative factors exactly as
>      $$a_{\rm med}(x) = -\frac{3 P q}{2 r_c^2} e^{-\ell_A(x)}(1 - x^2)^2\left[2 + 3 q x^2(1 - x^2)^2\right] < 0 \qquad \forall x \in [0, 1).$$

---

## 2. Exact Radial BVP Solution, Constitutive Closure, and Optical Verification

### 2.1 Covariantly Conserved Core Matter and Exact Solution of the Radial Label BVP

We equip the core $x \in [0, 1]$ with the smooth, compactly supported, positive-energy core matter profile
$$\rho_{\rm m}(x) = \frac{P}{r_c^2}\rho_0^*(q)\,(1 - x^2)^3, \qquad p_{r,\rm m}(x) = 0, \qquad p_{t,\rm m}(x) = \frac{x\,\ell_B'(x)}{2\bigl(2 + x\,\ell_A'(x)\bigr)}\,\rho_{\rm m}(x).$$
1. **Exact Covariant Conservation ($\nabla_\mu T^{\rm m\,\mu}{}_\nu = 0$):** By construction, $p_{r,\rm m}' + \frac{1}{2}\ell_B'(\rho_{\rm m} + p_{r,\rm m}) + \frac{2 + x\ell_A'}{x}(p_{r,\rm m} - p_{t,\rm m}) \equiv 0$ identically on $[0, 1]$. At the center $x \to 0$, $p_{t,\rm m}(x) = O(x^2) \to 0 = p_{r,\rm m}(0)$, so the matter stress is regular and isotropic at the origin. At the core boundary $x \to 1^-$, both $\rho_{\rm m}(x)$ and $p_{t,\rm m}(x)$ vanish as $O((1-x)^3)$, preserving all $C^2$ junction conditions and the 3rd- and 4th-derivative label-regularity conditions of Theorem 3.
2. **Unique Eigenvalue $\rho_0^*(q) > 0$:** The global label-traction condition $Q C_\ell(r_c) = 0$ (`Theorem 2`) uniquely fixes $\rho_0^*(q)$ by the linear ratio of two positive integrals:
   $$\rho_0^*(q) = \frac{\frac{1}{8}\int_0^1 x^2 e^{(\ell_A+\ell_B)/2}\bigl(\ell_A'(x) + \ell_B'(x)\bigr)^2\,dx}{\int_0^1 x^2 e^{(3\ell_A+\ell_B)/2}(1 - x^2)^3\left[\frac{3}{4} + \frac{x\,\ell_B'(x)}{4(2 + x\,\ell_A'(x))}\right]dx} > 0.$$
   For the representative compactness values $q \in \{1.2, 1.5, 1.8\}$:
   - $q = 1.2$: $\rho_0^*(1.2) = 0.562802798863$, $\ell'(0) = 0.674410673977$, $b_r(0) = b_t(0) = 1.505025797876$.
   - $q = 1.5$: $\rho_0^*(1.5) = 0.663639933233$, $\ell'(0) = 0.607531066802$, $b_r(0) = b_t(0) = 1.654164532986$.
   - $q = 1.8$: $\rho_0^*(1.8) = 0.722457025335$, $\ell'(0) = 0.548469271055$, $b_r(0) = b_t(0) = 1.819967252024$.
3. **Sign Definiteness and Smooth Monotonicity of $\ell(x)$:**
   Across the entire core $x \in [0, 1)$, $a(x) = Q b_r F_r(x) < 0$ is strictly negative (ensuring positive radial label kinetic energy $-Q F_r > 0$), and $Q C_\ell(x) < 0$ is strictly negative on $(0, 1)$. Consequently,
   $$\frac{d\ln\ell}{dx} = \frac{r_c\sqrt{-g}(x)\,a(x)}{Q C_\ell(x)} > 1 \qquad \forall x \in (0, 1),$$
   with $\lim_{x\to 0^+} x\frac{d\ln\ell}{dx} = 1$ and $\lim_{x\to 1^-} \frac{d\ln\ell}{dx} = 1$. Integrating $\frac{d}{dx}\ln(\ell(x)/(r_c x)) = \frac{d\ln\ell}{dx} - \frac{1}{x}$ backward from $\ell(1) = r_c$ yields the unique smooth, strictly increasing radial label profile $\ell(x)$ on $[0, 1]$.
4. **Strict Monotonicity of Principal Strain Invariants and Single-Valued Constitutive Closure:**
   On the solved profile $\ell(x)$, both $\widehat{I}_1(x) = b_r(x) + 2 b_t(x)$ and $\widehat{I}_3(x) = b_r(x)\,b_t(x)^2$ decrease strictly monotonically from $(3 b_c, b_c^3)$ at $x = 0$ to the silent isotropic point $(3, 1)$ at $x = 1$, and the constitutive chain rule $f'(x) = a(x)(\ln b_r)' + c(x)(\ln b_t)'$ holds with symbolic residual `0` and numerical grid residual $< 10^{-10}$.

---

### 2.2 Verification of Central Invariants and Optical Light-Ring Structure

[`verify_action_derived_c2_interior_closure.py`](verify_action_derived_c2_interior_closure.py) also verifies all geometric and optical theorems of the $C^2$ core geometry:
1. **Areal Radius Monotonicity Window:**
   $$\frac{x}{R_{\rm ar}}\frac{d R_{\rm ar}}{dx} = 1 + \frac{q}{8}\bigl(35 x^2 - 84 x^4 + 45 x^6\bigr) > 0 \quad \forall x \in [0, 1] \iff q < q_* = \frac{8}{175} + \frac{148\sqrt{259}}{1225} \approx 1.9900690546.$$
2. **Central Curvature and Effective Stress:**
   $$R(0) = \frac{177 q}{4 r_c^2}, \qquad R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}\big|_0 = \frac{15063 q^2}{16 r_c^4}, \qquad 8\pi G r_c^2 \rho_{\rm eff}(0) = -\frac{105 q}{4}, \qquad 8\pi G r_c^2 p_{\rm eff}(0) = 6q.$$
3. **Global Minimum of the Lapse:**
   $\mathcal{B}_-(x)$ achieves its unique interior minimum at $x_{\min} = \sqrt{(18 - \sqrt{93})/21} \approx 0.63098878$, where $\mathcal{B}_{\min} = e^{-\alpha_B q} > 0$ with $\alpha_B = \frac{211}{196} + \frac{31\sqrt{93}}{1764} \approx 1.24600531$.
4. **Outer Unstable Photon Sphere and Inner Stable Light Ring:**
   - Exterior optical potential $V_+(r) = e^{-4m/r}/r^2$ has its unique global maximum at $r_{\rm ph} = 2m = r_s$ with critical impact parameter $b_c = 2e m = e r_s$ and relative shift vs. Schwarzschild $\delta_{\rm exp} = \frac{2e}{3\sqrt{3}} - 1 \approx 0.046297067$.
   - Interior optical potential $r_c^2 V_-(x) = x^{-2} e^{-q P(x)}$ with $P(x) = 1 + \frac{23}{4}x^2 - \frac{15}{2}x^4 + \frac{11}{4}x^6$ satisfies $\frac{2x}{V_-}\frac{dV_-}{dx} = q(-23 x^2 + 60 x^4 - 33 x^6) - 4 = 0$, which for every $1 < q < 2$ has a unique root $y_{\rm lr} = x_{\rm lr}^2 \in (y_-, y_+)$ ($y_\pm = (20 \pm 7\sqrt{3})/33$) where $d^2 V_- / dx^2 > 0$ (radially stable inner light ring). At $q = 3/2$, $x_{\rm lr} = 0.8705805856$ and $V_{+,\max}/V_{-,\min} = 1.3263051946$.
5. **Negative Controls Rejected (`5/5`):**
   - `pure_medium_zero_matter_on_deg6_metric`: setting $\rho_{\rm m} = p_{r,\rm m} = p_{t,\rm m} = 0$ on the degree-6 $C^2$ core leaves $Q C_\ell(r_c)/(P r_c) \ge 0.01903774 > 0$, failing the zero-traction boundary gate — **rejected**.
   - `locked_common_scale_interior_ansatz`: imposing $\ell_A(x) + \ell_B(x) = 0$ inside $x \in [0, 1)$ violates the $C^2$ regular center/boundary balance — **rejected**.
   - `unmatched_third_derivative_H_at_boundary`: setting $H'''(1^-) = H_{\rm ext}'''(1) = -3q$ instead of $-\frac{1}{2}\ell_B'''(1^-) = \frac{51}{2}q$ produces $a'(1^-) \neq 0$ and a singular $1/(1-x)$ pole in $\ell'(x)/\ell(x)$ — **rejected**.
   - `non_conserved_isotropic_zero_pressure_core_matter`: setting $p_{t,\rm m} = 0$ alongside $p_{r,\rm m} = 0$ violates $\nabla_\mu T^{\rm m\,\mu}{}_r = 0$ and breaks the constitutive chain rule $df/dx = a(\ln b_r)' + c(\ln b_t)'$ — **rejected**.
   - `wrong_sign_core_matter_density`: setting $\rho_0 < 0$ drives $Q C_\ell(r_c) > 0$ further away from zero — **rejected**.
