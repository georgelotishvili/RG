# Unified Ambient Collective Phase & Oscillon Inertia Audit

2026-10-25. Research contract, exact derivation, and numerical BVP verification supplement.
MODEL_VERSION=`REFG_UNIFIED_COVARIANT_V1` (extending `REFG_ISOLATED_COVARIANT_V2`).

## Decision and scope

[`unified_isolated_cosmological_action.md`](../Lagrangian_Formulation/Unified_Isolated_Cosmological_Action/unified_isolated_cosmological_action.md) constructed the single covariant action `REFG_UNIFIED_COVARIANT_V1` that contains both the isolated oscillon/Maxwell sector (`REFG_ISOLATED_COVARIANT_V2`) on the exact collective vacuum solution $x = |\Psi_C|^2 = 0$ and the cosmological/weak-field collective phase sector ([W3-54](../Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md) / [W3-62](../Cosmology_and_LSS/CMB_Closure/w3_62_cmb_einstein_source_linear_closure_preregistration.md)) on $x > 0$.

This supplement addresses the next fundamental physical and mathematical question following [`foundation_revision.md`](foundation_revision.md):
1. What happens when a self-gravitating oscillon ($Q > 0$) interacts with the collective phase sector of `REFG_UNIFIED_COVARIANT_V1`?
2. Why does a naive grand-canonical boundary condition at the flat-space threshold frequency ($\omega_C = \mu_{C0}$ at spatial infinity $N(\infty) = 1$) fail in an infinite asymptotically flat volume, and how is a localized equilibrium with finite collective charge $Q_C \ge 0$ properly defined?
3. Does the coupled oscillon + collective-phase equilibrium satisfy an exact two-charge ADM first law, preserve the clock–ruler stress reconstruction identity, maintain exact whole-body ADM boost inertia $M_I = M_{\rm active} = M_{\rm passive} = M_{\rm ADM}(Q, Q_C)$, and converge smoothly to `REFG_ISOLATED_COVARIANT_V2` as $Q_C \to 0^+$?

All symbolic and numerical claims in this document are verified by [`verify_unified_ambient_inertia.py`](verify_unified_ambient_inertia.py) and logged in [`unified_ambient_inertia_result.json`](unified_ambient_inertia_result.json).

---

## Frozen claims and verification contract

Contract fixed before execution of [`verify_unified_ambient_inertia.py`](verify_unified_ambient_inertia.py).

| Field | Contract |
|---|---|
| CLAIM_ID | `REFG_UNIFIED_AMBIENT_INERTIA_AND_TWO_CHARGE_FIRST_LAW_V1` |
| CLAIM | Under `REFG_UNIFIED_COVARIANT_V1`, (i) holding $\omega_C \ge \mu_{C0}$ in an infinite asymptotically flat spacetime triggers a $1/r$ grand-canonical threshold divergence ($\int 4\pi r^2 \rho_C\,dr = \infty$); (ii) for $\omega_C \le \mu_{C0} N(0)$, $x_*(r) \equiv 0$ everywhere (`REFG_ISOLATED_COVARIANT_V2` is unperturbed); (iii) for $\mu_{C0} N(0) < \omega_C < \mu_{C0}$, the collective phase forms a compactly supported gravitating pocket $r \in [0, r_{\rm trap}]$ whose coupled equilibria satisfy the exact two-charge ADM first law $dM_{\rm ADM} = \Omega\,dQ + \omega_C\,dQ_C$, the total radial-stress clock–ruler reconstruction identity, exact whole-body boost inertia $M_I = M_{\rm ADM}(Q, Q_C) = M_{\rm Komar}(Q, Q_C)$, and $O(Q_C)$ convergence to `REFG_ISOLATED_COVARIANT_V2` as $Q_C \to 0^+$ with threshold slope $\partial M_{\rm ADM}/\partial Q_C|_{Q_C=0^+} = \mu_{C0} N_0(0)$. |
| TYPE | Action-derived exact theorems (grand-canonical no-go, compact trapping window, two-charge ADM first law, boost inertia) and numerical BVP verification on the coupled oscillon + collective branch. |
| MODEL_VERSION | `REFG_UNIFIED_COVARIANT_V1` reducing to `REFG_ISOLATED_COVARIANT_V2` on $Q_C = 0$. |
| ASSUMPTIONS | Universal minimal metric coupling; static spherically symmetric metric $ds^2 = -N^2 dt^2 + dr^2/F + r^2 d\Omega^2$ with $N = \sigma\sqrt{F}$, $F = 1 - 2\alpha m/r > 0$; stationary oscillon $\Psi = f(r)e^{i\Omega t}/\sqrt{2}$ and collective phase $\theta_C = -\omega_C t$; quadratic envelope potential $U_C(x) = \frac{1}{2}\mu_{C0}^2 x + \frac{1}{4}\lambda_C x^2$ with $\mu_{C0} > 0, \lambda_C > 0$; neutral background $F^{\rm EM}_{\mu\nu} = 0$. |
| DOMAIN | Symbolic proofs hold on all static regular spherically symmetric configurations with $F, N > 0$. Numerical BVPs evaluated at reference coupling $\alpha = 0.001$, $Q_0 = 190.401136223484$, $\mu_{C0} = 1$, $\lambda_C = 10$, across sub-threshold ($\omega_C \le \mu_{C0} N_0(0)$) and trapped-pocket ($\mu_{C0} N_0(0) < \omega_C < \mu_{C0}$) regimes on $R = 60$. |
| CONVENTIONS | Signature $(-,+,+,+)$; $c_0 = \hbar = 1$ in numerical BVP ($c_0$ retained in symbolic checks); $\alpha = 4\pi G_{\rm eff}$; $M_{\rm ADM} = 4\pi m(\infty)$; $Q = 4\pi q(\infty)$; $Q_C = 4\pi q_C(\infty)$. |
| FREEDOM_LEDGER | Oscillon potential $V(f) = f^2/2 - f^4/4 + f^6/24$ and $\alpha = 0.001, Q_0 = 190.401136223484$ frozen to [`verify_oscillon_inertia.py`](../Lagrangian_Formulation/Oscillon_Inertia/verify_oscillon_inertia.py) and [`verify_foundation_revision.py`](verify_foundation_revision.py). Collective parameters $(\mu_{C0}, \lambda_C) = (1, 10)$ fixed as representative witness; no fitted inertia parameters or switches. |
| DEPENDENCIES | [`unified_isolated_cosmological_action.md`](../Lagrangian_Formulation/Unified_Isolated_Cosmological_Action/unified_isolated_cosmological_action.md), [`foundation_revision.md`](foundation_revision.md), [`oscillon_inertia.md`](../Lagrangian_Formulation/Oscillon_Inertia/oscillon_inertia.md), and their Python verifiers, pinned by SHA-256. |
| METHOD | SymPy exact symbolic proof of asymptotic divergence at $\omega_C = \mu_{C0}$, piecewise compact trapping on $\omega_C \in (\mu_{C0}N(0), \mu_{C0})$, canonical two-charge integrating factor $\sigma(r)$, and boost surface charges; SciPy `solve_bvp` + `brentq` trapping-radius quadrature for coupled equilibria, threshold convergence, clock–ruler reconstruction, Komar balance, and partial/joint first-law finite differences. |
| PASS_CONDITION | All symbolic residuals identically `0`; sub-threshold ($\omega_C \le \mu_{C0}N_0(0)$) mass/frequency difference from pure `REFG_ISOLATED_COVARIANT_V2` $< 10^{-12}$; coupled BVP max residual $< 10^{-6}$ and boundary residual $< 10^{-8}$; total pressure clock–ruler reconstruction error $< 3\times 10^{-7}$; Komar volume vs surface vs ADM mass relative error $< 10^{-5}$; partial derivative $(\partial M/\partial Q_C)_Q / \omega_C - 1$ relative error $< 10^{-5}$; joint two-charge first law $(\Delta M - \Omega\Delta Q - \omega_C\Delta Q_C)/\Delta M$ relative error $< 10^{-5}$; threshold limit $(\Delta M/Q_C)/(\mu_{C0} N_0(0)) - 1$ monotonically approaching `0` ($< 2\times 10^{-4}$ at $\delta\omega_C = 10^{-4}$); 4 negative controls rejected. |
| FAIL_CONDITION | Any nonzero symbolic residual, failure of coupled BVP convergence, violation of two-charge ADM first law or clock–ruler reconstruction, or upstream SHA-256 mismatch. |
| FALSIFIER | Discovery of a regular finite-mass stationary solution at $\omega_C \ge \mu_{C0}$ in infinite asymptotically flat space without compact trapping, or failure of $\sigma(r)$ to serve as integrating factor for the coupled mass constraint. |
| RESIDUAL | Symbolic residuals and numerical BVP/quadrature residuals recorded separately in [`unified_ambient_inertia_result.json`](unified_ambient_inertia_result.json). |
| ERROR_BOUND | Numerical quadrature across $r_{\rm trap}$ split at the exact root $N(r_{\rm trap}) = \omega_C/\mu_{C0}$ (`brentq` tolerance $10^{-12}$) to eliminate $C^0$-kink quadrature error. |
| VALIDITY_HEALTH | Positive metric functions $F, N > 0$; hyperbolic principal parts on $x > 0$ ($c_{s,C}^2 > 0$); compact collective support $r_{\rm trap} < R$; exponentially localized oscillon tail at $r = R$. |
| BRANCHES | Sub-threshold vacuum branch ($Q_C = 0$, identical to `REFG_ISOLATED_COVARIANT_V2`) and compact trapped-pocket branch ($Q_C > 0$, $\mu_{C0} N(0) < \omega_C < \mu_{C0}$), meeting continuously at the nucleation threshold $\omega_{C,\text{crit}} = \mu_{C0} N_0(0)$. |
| OBSERVABLE_MAP | Total ADM mass $M_{\rm ADM}(Q, Q_C)$, Komar mass $M_{\rm Komar}$, boost momentum $P_i = \gamma M_{\rm ADM} v_i$, proper clock $N$, isotropic ruler factor $A_{\rm iso}$, trapping radius $r_{\rm trap}$. |
| FORWARD_MODEL | N/A (exact mathematical and numerical BVP theory audit). |
| DATA_ROLE | Synthetic calculations on the frozen `REFG_ISOLATED_COVARIANT_V2` reference oscillon state. |
| IDENTIFIABILITY | Distinguishes grand-canonical infinite-bath boundary conditions (which suffer Jeans/Bose $1/r$ condensation) from canonical finite-$Q_C$ trapped configurations. |
| BENCHMARK | Exact agreement with `REFG_ISOLATED_COVARIANT_V2` (`M_ADM = 176.77035488`, `Omega = 0.79600884`, `N(0) = 0.99182546`) on $\omega_C \le \mu_{C0} N_0(0)$ and as $Q_C \to 0^+$. |
| CLOSURE_FLAGS | Closes the isolated-in-ambient-collective-phase equilibrium and inertia audit. |
| CROSSCHECK | Symbolic integrating-factor identity vs numerical partial derivatives $(\partial M/\partial Q)_{Q_C}$, $(\partial M/\partial Q_C)_Q$, and simultaneous $(\Delta Q, \Delta Q_C)$ steps; metric $\ln(N A_{\rm iso})$ vs stress integral with $p_r = p_{r,\rm osc} + p_C$; ADM mass vs volume and surface Komar integrals. |
| PROVENANCE | SHA-256 hashes of all upstream dependencies and generated files logged in [`unified_ambient_inertia_result.json`](unified_ambient_inertia_result.json). |
| FILES | `RefG/work 3/Inertia/unified_ambient_inertia_audit.md`, `RefG/work 3/Inertia/verify_unified_ambient_inertia.py`, `RefG/work 3/Inertia/unified_ambient_inertia_result.json`. |

---

## 1. Coupled Spherical Field Equations of `REFG_UNIFIED_COVARIANT_V1`

On the static spherically symmetric line element ($c_0 = \hbar = 1$, $\alpha = 4\pi G_{\rm eff}$)
$$ds^2 = -N(r)^2\,dt^2 + \frac{dr^2}{F(r)} + r^2(d\theta^2 + \sin^2\theta\,d\varphi^2), \qquad N(r) = \sigma(r)\sqrt{F(r)}, \qquad F(r) = 1 - \frac{2\alpha m(r)}{r},$$
consider a stationary complex oscillon $\Psi = \frac{1}{\sqrt{2}}f(r)e^{i\Omega t}$ and a stationary collective phase field $\theta_C = -\omega_C t$ with non-negative squared amplitude $x(r) = |\Psi_C(r)|^2 \ge 0$ and envelope potential
$$U_C(x) = \frac{1}{2}\mu_{C0}^2 x + \frac{1}{4}\lambda_C x^2 \qquad (\mu_{C0} > 0,\;\lambda_C > 0).$$

### 1.1 Collective Envelope Profile and Stress–Energy Components

The collective kinetic invariant is
$$X_C(r) = -g^{\mu\nu}\partial_\mu\theta_C\partial_\nu\theta_C = \frac{\omega_C^2}{N(r)^2} = \frac{\omega_C^2}{\sigma(r)^2 F(r)}.$$
As proved in [`unified_isolated_cosmological_action.md` §2.3](../Lagrangian_Formulation/Unified_Isolated_Cosmological_Action/unified_isolated_cosmological_action.md), maximization of the strictly concave dual Lagrangian $\mathcal{L}_C^{\rm (dual)} = \frac{1}{2}x X_C - U_C(x)$ over the physical domain $x \ge 0$ yields the unique piecewise-smooth envelope profile
$$x_*(r) = \max\!\left(0,\,\frac{X_C(r) - \mu_{C0}^2}{\lambda_C}\right) = \frac{\mu_{C0}^2}{\lambda_C}\max\!\left(0,\,\frac{\omega_C^2}{\mu_{C0}^2 N(r)^2} - 1\right).$$
Substituting $x_*(r)$ into the collective stress–energy tensor $T_{C\,\mu\nu} = x_*\,\partial_\mu\theta_C\partial_\nu\theta_C + g_{\mu\nu}\bigl(\frac{1}{2}x_* X_C - U_C(x_*)\bigr)$ gives the isotropic fluid components in the static frame:
$$\rho_C(r) = \mu_{C0}^2 x_*(r) + \frac{3}{4}\lambda_C x_*(r)^2, \qquad p_{r,C}(r) = p_{t,C}(r) = p_C(r) = \frac{1}{4}\lambda_C x_*(r)^2,$$
with enthalpy density
$$\rho_C(r) + p_C(r) = x_*(r)\bigl(\mu_{C0}^2 + \lambda_C x_*(r)\bigr) = x_*(r) X_C(r) = \frac{\omega_C^2 x_*(r)}{\sigma(r)^2 F(r)}.$$
Equivalently, in terms of the collective invariant number density $n_C(r) = x_*(r)\sqrt{X_C(r)} = \frac{\omega_C x_*(r)}{\sigma(r)\sqrt{F(r)}}$ and chemical potential $\mu(r) = \rho_C'(n_C(r)) = \sqrt{X_C(r)} = \frac{\omega_C}{N(r)}$ on $x_*(r) > 0$, Tolman's law $N(r)\mu(r) = \omega_C$ is identically satisfied and $\rho_C + p_C = \mu n_C$.

### 1.2 Coupled Einstein–Klein–Gordon System and Conserved Charges

Combining the oscillon components
$$T_{\rm osc} = \frac{\Omega^2 f^2}{2\sigma^2 F}, \qquad X_{\rm osc} = \frac{1}{2}F(f')^2, \qquad V_{\rm osc} = V(f),$$
$$\rho_{\rm osc} = T_{\rm osc} + X_{\rm osc} + V_{\rm osc}, \qquad p_{r,\rm osc} = T_{\rm osc} + X_{\rm osc} - V_{\rm osc}, \qquad p_{t,\rm osc} = T_{\rm osc} - X_{\rm osc} - V_{\rm osc},$$
with $(\rho_C, p_C)$, the coupled radial Einstein–matter system is:
$$\begin{aligned}
m'(r) &= r^2\bigl(\rho_{\rm osc}(r) + \rho_C(r)\bigr), \\
\frac{\sigma'(r)}{\sigma(r)} &= \frac{\alpha r}{F(r)}\bigl(\rho_{\rm osc} + p_{r,\rm osc} + \rho_C + p_C\bigr) = \alpha r\left[(f')^2 + \frac{\Omega^2 f^2 + \omega_C^2 x_*(r)}{\sigma(r)^2 F(r)^2}\right], \\
f''(r) &= \frac{V'(f) - \frac{\Omega^2 f}{\sigma^2 F}}{F} - \left(\frac{2}{r} + \frac{\sigma'}{\sigma} + \frac{F'}{F}\right)f'(r).
\end{aligned}$$
The two conserved global $U(1)$ Noether charges are the oscillon charge $Q = 4\pi q(\infty)$ and the collective phase charge $Q_C = 4\pi q_C(\infty)$, where
$$q'(r) = \frac{\Omega r^2 f(r)^2}{\sigma(r) F(r)}, \qquad q_C'(r) = \frac{\omega_C r^2 x_*(r)}{\sigma(r) F(r)} = \frac{r^2 n_C(r)}{\sqrt{F(r)}}.$$
The clock–ruler product $N(r)A_{\rm iso}(r)$ obeys the exact radial stress identity with total radial pressure $p_r(r) = p_{r,\rm osc}(r) + p_C(r)$:
$$\frac{d}{dr}\ln\bigl(N(r)A_{\rm iso}(r)\bigr) = \frac{\alpha r\bigl(p_{r,\rm osc}(r) + p_C(r)\bigr)}{F(r)} + \frac{\bigl(1 - \sqrt{F(r)}\bigr)^2}{2rF(r)}.$$

---

## 2. Three Exact Theorems on Ambient vs. Trapped Collective Equilibria

### Theorem 1 (Grand-Canonical Threshold Trap at $\omega_C \ge \mu_{C0}$)

> **Statement.** Suppose an asymptotically flat static spherically symmetric spacetime has total mass $M = 4\pi m(\infty) > 0$ so that $N(r) = 1 - \frac{\alpha M}{4\pi r} + O(r^{-2})$ as $r \to \infty$. If the collective phase frequency is set at or above the flat-space rest-mass threshold, $\omega_C \ge \mu_{C0}$, then the stationary envelope $x_*(r)$ cannot have finite ADM mass:
> 1. At the exact flat-space threshold $\omega_C = \mu_{C0}$, the Newtonian potential well $N(r) < 1$ forces $X_C(r) = \mu_{C0}^2 / N(r)^2 > \mu_{C0}^2$ throughout the exterior, producing a $1/r$ condensate tail:
>    $$x_*(r) = \frac{\mu_{C0}^2}{\lambda_C}\left(\frac{1}{N(r)^2} - 1\right) = \frac{\mu_{C0}^2 \alpha M}{2\pi \lambda_C r} + O(r^{-2}), \qquad \rho_C(r) = \frac{\mu_{C0}^4 \alpha M}{2\pi \lambda_C r} + O(r^{-2}).$$
>    The enclosed collective mass and charge diverge quadratically with cutoff radius $R$:
>    $$M_C(R) = \int^{R} 4\pi r^2 \rho_C(r)\,dr \sim \frac{\mu_{C0}^4 \alpha M}{\lambda_C} R^2 \to \infty \qquad (R \to \infty).$$
> 2. Above threshold ($\omega_C > \mu_{C0}$), $x_*(\infty) = (\omega_C^2 - \mu_{C0}^2)/\lambda_C > 0$ is a uniform non-zero background density and $M_C(R) \propto R^3 \to \infty$.

**Physical meaning.** A nearly pressureless Bose/dust condensate ($c_{s,C}^2 \to 0$ as $x \to 0$) held at the flat-space threshold chemical potential $\omega_C = \mu_{C0}$ in an infinite volume undergoes unbounded gravitational condensation into the long-range $1/r$ Newtonian potential of any central mass. Therefore, an isolated body in an asymptotically flat chart must be analyzed either in the **sub-threshold vacuum window** ($\omega_C \le \mu_{C0} N(0)$) or in the **canonical ensemble at fixed finite collective charge $Q_C$** ($\mu_{C0} N(0) < \omega_C < \mu_{C0}$). Cosmological backgrounds with $x_{\rm bg} > 0$ require an expanding FRW background (`W3-62`) or finite Jeans/Voronoi cell rather than an infinite static asymptotically flat bath.

---

### Theorem 2 (Sub-Threshold Vacuum Window and Compact Trapped-Pocket Regime)

> **Statement.** On any regular static spherically symmetric equilibrium with $\rho + p_r \ge 0$ and $m(r) \ge 0$, the lapse $N(r) = \sigma(r)\sqrt{F(r)}$ satisfies
> $$\frac{N'(r)}{N(r)} = \frac{\sigma'}{\sigma} + \frac{F'}{2F} = \frac{\alpha}{F(r)}\left[r(\rho + p_r - \rho) + \frac{m(r)}{r^2}\right] = \frac{\alpha}{F(r)}\left[r p_r(r) + \frac{m(r)}{r^2}\right],$$
> and reaches its global minimum at the center $r = 0$, increasing monotonically to $N(\infty) = 1$. Consequently, $\max_{r \ge 0} X_C(r) = \frac{\omega_C^2}{N(0)^2}$, which partitions the frequency space $\omega_C < \mu_{C0}$ into two exact regimes:
> 1. **Sub-Threshold Vacuum Window ($0 \le \omega_C \le \omega_{C,\text{crit}} \equiv \mu_{C0} N_0(0)$):**
>    $$X_C(r) \le \frac{\omega_C^2}{N_0(0)^2} \le \mu_{C0}^2 \quad \forall r \ge 0 \implies x_*(r) \equiv 0, \quad Q_C = 0, \quad T_{C\,\mu\nu}(r) \equiv 0.$$
>    The coupled equilibrium is **identically** the unperturbed `REFG_ISOLATED_COVARIANT_V2` oscillon.
> 2. **Compact Trapped-Pocket Regime ($\mu_{C0} N(0) < \omega_C < \mu_{C0}$):**
>    There exists a unique finite trapping radius $r_{\rm trap}(\omega_C) \in (0, \infty)$ defined by
>    $$N\bigl(r_{\rm trap}(\omega_C)\bigr) = \frac{\omega_C}{\mu_{C0}} < 1,$$
>    such that $x_*(r) > 0$ for $0 \le r < r_{\rm trap}(\omega_C)$ and $x_*(r) \equiv 0$ for all $r \ge r_{\rm trap}(\omega_C)$. Both $\rho_C(r)$ and $p_C(r)$ vanish identically outside $r_{\rm trap}(\omega_C)$, leaving an exact vacuum/oscillon-tail exterior and finite ADM mass $M_{\rm ADM}(Q, Q_C)$ and collective charge $Q_C \in (0, Q_{C,\max})$.

---

### Theorem 3 (Joint Two-Charge ADM First Law and Whole-Body Boost Inertia)

> **Statement.** Express the coupled mass constraint $m'(r) = r^2\bigl(\rho_{\rm osc} + \rho_C\bigr)$ in terms of the canonical variables $\bigl(f(r), f'(r), P_{\rm osc}(r), P_C(r), m(r)\bigr)$, where
> $$P_{\rm osc}(r) = \frac{r^2 \Omega f(r)^2}{\sigma(r) F(r)} = q'(r), \qquad P_C(r) = \frac{r^2 n_C(r)}{\sqrt{F(r)}} = \frac{r^2 \omega_C x_*(r)}{\sigma(r) F(r)} = q_C'(r).$$
> Since $n_C = \sqrt{F}\,P_C / r^2$ and $\rho_C'(n_C) = \mu = \omega_C / (\sigma\sqrt{F})$, the mass density source is
> $$r^2 \rho\bigl(f, f', P_{\rm osc}, P_C, m\bigr) = r^2 V(f) + r^2 \rho_C\!\left(\frac{\sqrt{F}\,P_C}{r^2}\right) + \frac{1}{2}F\left(r^2 (f')^2 + \frac{P_{\rm osc}^2}{r^2 f^2}\right).$$
> 1. **Exact Integrating Factor:** Differentiating $m'(r) = r^2\rho$ with respect to $m(r)$ at fixed $\bigl(f, f', P_{\rm osc}, P_C\bigr)$ using $\partial F/\partial m = -2\alpha/r$ gives
>    $$-\frac{\partial (r^2\rho)}{\partial m} = \frac{\alpha}{r}\left(r^2(f')^2 + \frac{P_{\rm osc}^2}{r^2 f^2} + \frac{r^2 \rho_C'(n_C) n_C}{F}\right) = \alpha r\left[(f')^2 + \frac{\Omega^2 f^2 + \omega_C^2 x_*}{\sigma^2 F^2}\right] = \frac{\sigma'(r)}{\sigma(r)}.$$
>    Therefore, $\sigma(r)$ is the exact integrating factor of the linearized mass constraint for **any** barotropic collective equation of state $\rho_C(n_C)$.
> 2. **Joint Two-Charge ADM First Law:** Evaluating the functional derivatives of $M_{\rm ADM} = 4\pi m(\infty)$ on shell (where Euler–Lagrange variations with respect to $f$ vanish by the Klein–Gordon equation) yields
>    $$\sigma(r)\frac{\partial (r^2\rho)}{\partial P_{\rm osc}} = \frac{\sigma F P_{\rm osc}}{r^2 f^2} = \Omega, \qquad \sigma(r)\frac{\partial (r^2\rho)}{\partial P_C} = \sigma\sqrt{F}\,\rho_C'(n_C) = N(r)\mu(r) = \omega_C,$$
>    and therefore
>    $$\delta M_{\rm ADM} = 4\pi\int_0^\infty \sigma(r)\bigl(\delta(r^2\rho)\bigr)_{m\text{ fixed}}\,dr = \Omega\,\delta Q + \omega_C\,\delta Q_C.$$
> 3. **Threshold Slope and Smooth Vacuum Limit ($Q_C \to 0^+$):** As $\omega_C \to \omega_{C,\text{crit}}^+ = \mu_{C0} N_0(0)^+$, $r_{\rm trap}(\omega_C) \to 0$ and $Q_C \to 0^+$, so the coupled equilibrium converges continuously to `REFG_ISOLATED_COVARIANT_V2` with exact marginal mass-to-charge ratio equal to the redshifted central mass gap:
>    $$\left.\frac{\partial M_{\rm ADM}(Q, Q_C)}{\partial Q_C}\right|_{Q_C = 0^+} = \omega_{C,\text{crit}} = \mu_{C0} N_0(0).$$
> 4. **Whole-Body Boost Inertia Equivalence:** Because $x_*(r)$ vanishes identically for $r \ge r_{\rm trap}(\omega_C) < R$ and the unified action $S_{\rm uni}$ is diffeomorphism and local Lorentz invariant with standard Einstein–Hilbert/TEGR boundary structure, a boosted equilibrium state $\bigl(g_{\mu\nu}, \Psi, \Psi_C\bigr)$ has the exact asymptotic Schwarzschild multipole falloff outside $r_{\rm trap}$, yielding
>    $$E_{\rm ADM}(v) = \gamma M_{\rm ADM}(Q, Q_C), \qquad P_{\rm ADM}(v) = \gamma M_{\rm ADM}(Q, Q_C) v, \qquad M_I = M_{\rm ADM}(Q, Q_C) = M_{\rm Komar}(Q, Q_C).$$

---

## 3. Numerical BVP Verification Summary

[`verify_unified_ambient_inertia.py`](verify_unified_ambient_inertia.py) executes both the exact SymPy proofs and the numerical BVP verification at $\alpha = 0.001$, $Q_0 = 190.401136223484$, $\mu_{C0} = 1.0$, $\lambda_C = 10.0$, $R = 60.0$:

1. **Baseline & Sub-Threshold Vacuum Window ($\omega_C \le \mu_{C0} N_0(0) = 0.9918254623$):**
   - At $\omega_C = 0.990000 < \mu_{C0} N_0(0)$ and $\omega_C = \mu_{C0} N_0(0)$, the coupled BVP solver produces $Q_C = 0.0$, $r_{\rm trap} = 0.0$, $M_{\rm ADM} = 176.77035487722856$, and $\Omega = 0.79600883877507$, matching `REFG_ISOLATED_COVARIANT_V2` to machine precision ($< 10^{-14}$).
2. **Threshold Convergence Scan ($\delta\omega_C = \omega_C - \mu_{C0} N_0(0) \in \{2\times 10^{-3}, 10^{-3}, 4\times 10^{-4}, 2\times 10^{-4}, 10^{-4}\}$):**
   - As $\delta\omega_C \to 0^+$, the trapping radius shrinks ($r_{\rm trap}: 1.9901 \to 0.4213$), $Q_C \to 0^+$ ($5.01\times 10^{-3} \to 2.52\times 10^{-6}$), $M_{\rm ADM}(Q_0, Q_C) \to M_{\rm ADM}(Q_0, 0)$, and the secant slope $\bigl(M_{\rm ADM}(Q_0, Q_C) - M_{\rm ADM}(Q_0, 0)\bigr)/Q_C$ converges monotonically to $\mu_{C0} N_0(0) = 0.99182546$ (relative difference $1.19 \times 10^{-4}$ at $\delta\omega_C = 10^{-4}$).
3. **Trapped-Pocket Witness State ($\omega_C = 0.9935$, $r_{\rm trap} = 1.79572$):**
   - $Q_C = 3.134180 \times 10^{-3}$, $M_{\rm ADM} = 176.77346722$, $\Omega = 0.79600876$.
   - Clock–ruler stress integral reconstruction max error across $r \in [10^{-4}, 60]$: $7.98 \times 10^{-9} < 3 \times 10^{-7}$.
   - Komar volume vs. surface vs. ADM mass agreement: relative error $2.11 \times 10^{-11} < 10^{-5}$.
4. **Partial and Joint Two-Charge First Law Finite Differences around $(\omega_C = 0.9935, Q = Q_0)$:**
   - Fixed-$Q$ partial derivative: $\bigl(\partial M_{\rm ADM}/\partial Q_C\bigr)_Q = 0.99349895$ vs. $\omega_C = 0.99350000$ (relative error $1.05 \times 10^{-6} < 10^{-5}$).
   - Fixed-$\omega_C$ Legendre-transformed derivative: $\bigl(\Delta(M_{\rm ADM} - \omega_C Q_C)/\Delta Q\bigr)_{\omega_C} = 0.79600879$ vs. $\Omega = 0.79600876$ (relative error $4.71 \times 10^{-8} < 10^{-5}$).
   - Simultaneous $(\Delta Q, \Delta Q_C)$ step: $\Delta M_{\rm ADM} = 0.003518725$ vs. $\bar{\Omega}\,\Delta Q + \omega_C\,\Delta Q_C = 0.003518726$ (relative error $2.17 \times 10^{-7} < 10^{-5}$).
   - Residual collective slope from simultaneous step: $\bigl((\Delta M_{\rm ADM} - \bar{\Omega}\,\Delta Q)/\Delta Q_C\bigr)/\omega_C - 1$ relative error $1.56 \times 10^{-6} < 10^{-5}$.
5. **Negative Controls Rejected (`4/4`):**
   - `grand_canonical_threshold_finite_mass_ansatz`: assuming finite mass at $\omega_C = \mu_{C0}$ in an asymptotically flat $1/r$ metric yields divergent $\int_0^R 4\pi r^2 \rho_C\,dr \propto R^2$ — **rejected**.
   - `omitted_collective_pressure_in_clock_ruler_reconstruction`: omitting $p_C(r)$ from the radial stress reconstruction increases the reconstruction error by more than $20\times$ above the coupled baseline — **rejected**.
   - `wrong_collective_first_law_unredshifted_threshold`: replacing the threshold chemical potential $\omega_{C,\text{crit}} = \mu_{C0} N_0(0)$ by the unredshifted flat-space value $\mu_{C0}$ fails the threshold slope check by $> 8 \times 10^{-3}$ — **rejected**.
   - `omitted_collective_term_in_joint_first_law`: omitting $\omega_C\,\Delta Q_C$ from $\Delta M_{\rm ADM}$ on the simultaneous step violates the first-law balance by $> 10^{-2}$ — **rejected**.
