# Covariant-to-Galactic Bridge Audit: AQUAL $k$-Essence Completion, Refractive Lensing, and Solar-System Screening

- **CLAIM_ID**: `REFG_COVARIANT_GALACTIC_BRIDGE_AUDIT_V1`
- **MODEL_VERSION**: `REFG_COVARIANT_GALACTIC_BRIDGE_V1`
- **STATUS**: `VERIFIED_EXACT_COVARIANT_GALACTIC_BRIDGE_AND_SCREENING_AUDIT`
- **SCOPE**: Research package in `RefG/work 3/Galactic_Dynamics/` connecting the covariant gravitational actions (`REFG_UNIFIED_COVARIANT_V1`, `W3-54`, and `W3-92`) to the galactic phenomenological suite (`w3_10_galactic_action_and_btfr.py`, `w3_11_sparc_rar_validation.py`, `w3_12_aqual_disk_solution.py`, `w3_13_refractive_lensing.py`).

---

## 1. Executive Conclusion

A purely quadratic spatial-gradient action in the weak-field regime ($\mathcal{L}_H \propto -\gamma^{\mu\nu}\nabla_\mu H \nabla_\nu H$) reduces to the linear Poisson equation $\nabla^2\Phi = 4\pi G_{\rm eff}\rho_{\rm b}$ and therefore yields Keplerian falloff $v_{\rm circ}(r) \propto r^{-1/2}$ rather than flat rotation curves. Embedding the galactic constitutive law of `w3_10_galactic_action_and_btfr.py` into the covariant preferred-frame framework requires promoting the projected spatial gradient invariant
$$
Z_H \equiv c^4 \gamma^{\mu\nu}\nabla_\mu H \nabla_\nu H, \qquad \gamma^{\mu\nu} \equiv g^{\mu\nu} + u^\mu u^\nu,
$$
to a covariant AQUAL $k$-essence density
$$
\mathcal{L}_{H,\rm IR}(Z_H) = -\frac{M_{\rm Pl}^2 a_0^2}{2 c^4}\,\mathcal{F}\!\left(\frac{Z_H}{a_0^2}\right) = -\frac{a_0^2}{8\pi G}\,\mathcal{F}\!\left(\frac{Z_H}{a_0^2}\right), \qquad \mathcal{F}'(x^2) = \mu(x), \qquad x \equiv \frac{\sqrt{Z_H}}{a_0}.
$$
For the `w3_10` algebraic constitutive potential $W(g_v, g_N) = \frac{1}{3}g_v^3 + \frac{1}{2}g_N g_v^2 - a_0 g_N g_v$, the interpolating function $\mu_1(x) = \frac{x}{1+x}$ integrates in closed elementary form to
$$
\mathcal{F}_1(x^2) = \int_0^{x^2}\frac{\sqrt{s}}{1+\sqrt{s}}\,ds = x^2 - 2x + 2\ln(1+x),
$$
which reproduces the canonical quadratic gradient kinetic term $-\frac{1}{8\pi G}|\nabla\Phi|^2$ at high acceleration ($x \gg 1$) and, via cancellation of the quadratic and linear terms in $2\ln(1+x) = 2x - x^2 + \frac{2}{3}x^3 - \dots$, the scale-invariant $p=3$ AQUAL kinetic term $-\frac{|\nabla\Phi|^3}{12\pi G a_0}$ in the deep-IR galactic regime ($x \ll 1$). On the common-scale optical metric $ds^2 = -e^{2\Phi/c^2}c^2 dt^2 + e^{-2\Phi/c^2}d\mathbf{x}^2$, this bridge preserves $\gamma_{\rm PPN} = \beta_{\rm PPN} = 1$, derives the exact Baryonic Tully–Fisher Relation $V_f^4 = G M a_0$, and yields the impact-parameter-independent weak-lensing deflection $\alpha = 2\pi V_f^2 / c^2 = 2\pi\sqrt{G M a_0}/c^2$ without dark matter. Finally, an objective Solar-System screening audit demonstrates that while $\mu_1(x) = \frac{x}{1+x}$ leaves a residual constant acceleration $\delta g \approx a_0 = 1.2\times 10^{-10}\text{ m/s}^2$ in the outer Solar System, the $n=2$ member of the same covariant family, $\mu_2(x) = \frac{x}{\sqrt{1+x^2}}$ with closed-form potential $\mathcal{F}_2(x^2) = x\sqrt{1+x^2} - \operatorname{arsinh}(x)$, preserves the exact BTFR and lensing deflection while suppressing the anomalous acceleration at Saturn ($r = 9.54\text{ AU}$) to $\delta g_{\mu_2} \approx 1.10\times 10^{-16}\text{ m/s}^2$ ($\delta g_{\mu_2}/g_N \approx 1.69\times 10^{-12}$).

---

## 2. Theorem 1: Canonical Quadratic-Gradient No-Go in the Galactic IR Regime

### 2.1 Weak-Field Reduction of the Canonical $H$-Kinetic Term

In `W3-54` and `W3-92`, the common-scale refractive scalar $H$ has the projected spatial kinetic term
$$
\mathcal{L}_{H,\rm quad} = -\frac{M_{\rm Pl}^2}{2}\omega_H(\widehat{Y})\,\gamma^{\mu\nu}\nabla_\mu H \nabla_\nu H, \qquad M_{\rm Pl}^2 = \frac{c^4}{4\pi G},
$$
where $u^\mu = N^{-1}\delta^\mu_0$ is the static medium four-velocity and $\widehat{Y} = N e^H$. On the common-scale weak-field metric
$$
ds^2 = -e^{2\Phi/c^2}c^2 dt^2 + e^{-2\Phi/c^2}\delta_{ij}dx^i dx^j, \qquad H = -\frac{\Phi}{c^2}, \qquad \widehat{Y} = e^{\Phi/c^2}e^{-\Phi/c^2} \equiv 1,
$$
the projected spatial gradient invariant is
$$
Z_H \equiv c^4 \gamma^{\mu\nu}\nabla_\mu H \nabla_\nu H = e^{2\Phi/c^2}|\nabla\Phi|^2 = |\nabla\Phi|^2\left(1 + \frac{2\Phi}{c^2} + O(\Phi^2/c^4)\right).
$$
With $\omega_H(1) = 1$, the static weak-field action reduces to the quadratic Dirichlet functional
$$
S_{\rm quad}[\Phi] = \int dt\,d^3x\left[-\frac{1}{8\pi G}|\nabla\Phi|^2 - \rho_{\rm b}\Phi\right],
$$
whose Euler–Lagrange equation is the linear Poisson equation
$$
\nabla^2\Phi = 4\pi G \rho_{\rm b}.
$$
Outside a compact baryonic mass $M$, Gauss's law gives
$$
g_{\rm quad}(r) = \frac{G M}{r^2}, \qquad v_{\rm circ}^2(r) = r g_{\rm quad}(r) = \frac{G M}{r} \xrightarrow{r \to \infty} 0.
$$

> [!IMPORTANT]
> **Structural Bridge Conclusion:** Any covariant action that remains analytic and quadratic in $\nabla_\mu H$ as $Z_H \to 0$ produces $g(r) \propto r^{-2}$ (or Yukawa decay $e^{-m_H r}/r^2$ if a mass term is present) and cannot generate flat galactic rotation curves or $V_f^4 = G M a_0$ without non-baryonic dark matter. Reproducing the galactic dynamics of `w3_10`–`w3_13` from the covariant action requires a non-quadratic infrared behaviour $\mathcal{L}_{H,\rm IR}(Z_H) \propto -Z_H^{3/2}/a_0$ for $Z_H \ll a_0^2$.

---

## 3. Theorem 2: Exact Equivalence Between `w3_10` and the Covariant AQUAL $k$-Essence Sector

### 3.1 Algebraic Constitutive Potential of `w3_10_galactic_action_and_btfr.py`

In `w3_10_galactic_action_and_btfr.py`, the vacuum response field $g_v = g - g_N$ is governed by the local constitutive potential
$$
W(g_v, g_N) = \frac{1}{3}g_v^3 + \frac{1}{2}g_N g_v^2 - a_0 g_N g_v.
$$
Stationarity $\partial W / \partial g_v = 0$ yields the quadratic response law
$$
g_v^2 + g_N g_v - a_0 g_N = 0 \implies g_v = \frac{-g_N + \sqrt{g_N^2 + 4 a_0 g_N}}{2} > 0.
$$
Substituting $g_v = g - g_N$ gives the exact algebraic relation between the total acceleration $g = |\nabla\Phi|$ and the Newtonian baryonic acceleration $g_N = |\nabla\Phi_N|$:
$$
(g - g_N)^2 + g_N(g - g_N) - a_0 g_N = 0 \iff g^2 - g g_N - a_0 g_N = 0 \iff \frac{g}{g + a_0}\,g = g_N.
$$
Defining the dimensionless acceleration variables $x \equiv g / a_0 = |\nabla\Phi|/a_0$ and $y \equiv g_N / a_0$, this algebraic law is equivalent to
$$
\mu_1(x)\,x = y, \qquad \mu_1(x) \equiv \frac{x}{1+x},
$$
with inverse QUMOND interpolating function
$$
x = \nu_1(y)\,y, \qquad \nu_1(y) \equiv \frac{1 + \sqrt{1 + 4/y}}{2}, \qquad \mu_1\bigl(y\nu_1(y)\bigr)\,\nu_1(y) \equiv 1.
$$

### 3.2 Covariant AQUAL $k$-Essence Action and Exact Elementary Potential $\mathcal{F}_1(x^2)$

Promote the quadratic $H$-kinetic term in the covariant action to the $k$-essence functional
$$
S_{H,\rm IR}[g_{\mu\nu}, u^\mu, H] = \int d^4x\sqrt{-g}\left[-\frac{M_{\rm Pl}^2 a_0^2}{2 c^4}\,\mathcal{F}\!\left(\frac{c^4\gamma^{\mu\nu}\nabla_\mu H \nabla_\nu H}{a_0^2}\right)\right],
$$
where $s \equiv Z_H / a_0^2 = x^2$. In the quasi-static weak-field regime ($H = -\Phi/c^2$, $\sqrt{-g} = c(1 + O(\Phi/c^2))$, $Z_H = |\nabla\Phi|^2(1 + O(\Phi/c^2))$), varying $S_{H,\rm IR} + S_{\rm bar}$ with respect to $\Phi$ gives the nonlinear AQUAL field equation
$$
\nabla\cdot\left[\mathcal{F}'\!\left(\frac{|\nabla\Phi|^2}{a_0^2}\right)\nabla\Phi\right] = 4\pi G \rho_{\rm b}.
$$
Identifying $\mathcal{F}'(x^2) = \mu_1(x) = \frac{x}{1+x}$ with $\mathcal{F}_1(0) = 0$ yields the unique closed-form potential
$$
\mathcal{F}_1(x^2) = \int_0^{x^2}\frac{\sqrt{s}}{1+\sqrt{s}}\,ds = 2\int_0^x \frac{u^2}{1+u}\,du = x^2 - 2x + 2\ln(1+x).
$$

### 3.3 Asymptotic Limits and Strict Ellipticity

1. **High-Acceleration (Newtonian / Strong-Field) Limit ($x \to \infty$)**:
   $$
   \mathcal{F}_1(x^2) = x^2 - 2x + 2\ln(1+x), \qquad \frac{\mathcal{F}_1(x^2)}{x^2} = 1 - \frac{2}{x} + \frac{2\ln(1+x)}{x^2} \xrightarrow{x\to\infty} 1,
   $$
   recovering the canonical quadratic gradient term $-\frac{M_{\rm Pl}^2}{2}\gamma^{\mu\nu}\nabla_\mu H \nabla_\nu H$ with $\omega_H = 1$.
2. **Low-Acceleration (Deep-MOND / Galactic Halo) Limit ($x \to 0^+$)**:
   Expanding $2\ln(1+x) = 2x - x^2 + \frac{2}{3}x^3 - \frac{1}{2}x^4 + \frac{2}{5}x^5 - \dots$, the $O(x)$ and $O(x^2)$ terms cancel identically against $x^2 - 2x$:
   $$
   \mathcal{F}_1(x^2) = \frac{2}{3}x^3 - \frac{1}{2}x^4 + \frac{2}{5}x^5 - \frac{1}{3}x^6 + O(x^7),
   $$
   recovering the scale-invariant $p=3$ AQUAL Lagrangian $-\frac{|\nabla\Phi|^3}{12\pi G a_0}$. Outside a spherical baryonic mass $M$, Gauss's law gives
   $$
   \mu_1\!\left(\frac{g}{a_0}\right)g = \frac{G M}{r^2} \xrightarrow{g \ll a_0} \frac{g^2}{a_0} = \frac{G M}{r^2} \implies g(r) = \frac{\sqrt{G M a_0}}{r}, \qquad V_f^4 = \bigl(r g(r)\bigr)^2 = G M a_0.
   $$
3. **Strict Ellipticity and Absence of Gradient Instabilities**:
   For the second-order operator $\nabla_i\bigl[\mu_1(x)\nabla^i\Phi\bigr] = 4\pi G \rho_{\rm b}$, the tangent-operator eigenvalues in the radial (gradient-parallel) and transverse directions are
   $$
   \lambda_\parallel(x) = \frac{d}{dx}\bigl[x\mu_1(x)\bigr] = \frac{x(2+x)}{(1+x)^2} > 0, \qquad \lambda_\perp(x) = \mu_1(x) = \frac{x}{1+x} > 0 \qquad (\forall x > 0),
   $$
   with ellipticity ratio
   $$
   \frac{\lambda_\parallel(x)}{\lambda_\perp(x)} = 1 + \frac{d\ln\mu_1}{d\ln x} = 1 + \frac{1}{1+x} \in (1, 2) \qquad (\forall x > 0).
   $$

---

## 4. Theorem 3: Common-Scale Refractive Lensing and Solar-System 1PN Audit

### 4.1 Exact Factor-of-2 Lensing and Asymptotic Bending Angle

On the common-scale optical metric $ds^2 = -e^{2\Phi/c^2}c^2 dt^2 + e^{-2\Phi/c^2}d\mathbf{x}^2$, null geodesics ($ds^2 = 0$) obey $|d\mathbf{x}|/dt = c\,e^{2\Phi/c^2}$, so the effective refractive index of the vacuum medium is
$$
n(\mathbf{x}) = e^{-2\Phi(\mathbf{x})/c^2} = 1 - \frac{2\Phi(\mathbf{x})}{c^2} + \frac{2\Phi(\mathbf{x})^2}{c^4} + O(\Phi^3/c^6).
$$
Because the temporal metric perturbation $h_{00} = -2\Phi/c^2$ and spatial metric perturbation $h_{ij} = -(2\Phi/c^2)\delta_{ij}$ share the same scalar potential $\Phi = -c^2 H$, the Eddington PPN light-bending parameter is identically
$$
\gamma_{\rm PPN} = 1, \qquad \frac{1 + \gamma_{\rm PPN}}{2} = 1.
$$
In the deep-IR galactic halo ($r \gg r_M \equiv \sqrt{G M / a_0}$), integrating $d\Phi/dr = \sqrt{G M a_0}/r = V_f^2/r$ gives the logarithmic potential $\Phi(r) = V_f^2\ln(r/r_0)$. Along a straight-line impact parameter $b$ ($r = \sqrt{b^2 + z^2}$), the weak-lensing deflection angle is
$$
\alpha_{\rm gal}(b) = -\int_{-\infty}^{+\infty}\nabla_\perp\ln n\,dz = \frac{2}{c^2}\int_{-\infty}^{+\infty}\frac{\partial\Phi}{\partial b}\,dz = \frac{2 V_f^2}{c^2}\int_{-\infty}^{+\infty}\frac{b}{b^2 + z^2}\,dz = \frac{2\pi V_f^2}{c^2} = \frac{2\pi\sqrt{G M a_0}}{c^2},
$$
which is independent of $b$ and matches the isothermal dark-matter halo prediction $\alpha_{\rm iso} = 4\pi(\sigma_v/c)^2$ with $\sigma_v = V_f/\sqrt{2}$.

For a finite-radius spherical galaxy at arbitrary impact parameter $b$, integrating the exact `w3_10` acceleration law $g(r) = \frac{g_N(r) + \sqrt{g_N(r)^2 + 4 a_0 g_N(r)}}{2}$ with $g_N(r) = G M / r^2$ gives
$$
\alpha_{\rm exact}(b) = \frac{2}{c^2}\int_{-\infty}^{+\infty}g\!\left(\sqrt{b^2+z^2}\right)\frac{b}{\sqrt{b^2+z^2}}\,dz = \frac{4 G M}{c^2 b} + \frac{2\pi\sqrt{G M a_0}}{c^2}\,\mathcal{J}\!\left(\frac{b}{r_M}\right),
$$
which smoothly interpolates between the Schwarzschild–Einstein deflection $\alpha_{\rm GR}(b) = \frac{4 G M}{c^2 b}$ for $b \ll r_M$ and the constant asymptotic plateaux $\alpha_\infty = \frac{2\pi\sqrt{G M a_0}}{c^2}$ for $b \gg r_M$.

### 4.2 Objective Solar-System Screening Audit: $\mu_1(x)$ vs. $\mu_2(x)$

In the Solar System ($M_\odot = 1.98847\times 10^{30}\text{ kg}$, $a_0 = 1.2\times 10^{-10}\text{ m/s}^2$), the transition radius is
$$
r_{M,\odot} = \sqrt{\frac{G M_\odot}{a_0}} \approx 1.052\times 10^{15}\text{ m} \approx 7031\text{ AU}.
$$
At Earth ($r_\oplus = 1\text{ AU}$) and Saturn ($r_{\rm Sat} = 9.54\text{ AU}$), the Newtonian accelerations and dimensionless ratios $y = g_N/a_0$ are:
- Earth ($1\text{ AU}$): $g_{N,\oplus} = 5.93008\times 10^{-3}\text{ m/s}^2$, $y_\oplus = 4.9417\times 10^7$.
- Saturn ($9.54\text{ AU}$): $g_{N,\rm Sat} = 6.51573\times 10^{-5}\text{ m/s}^2$, $y_{\rm Sat} = 5.4298\times 10^5$.

For the general $n$-family of covariant AQUAL interpolating functions
$$
\mu_n(x) = \frac{x}{(1 + x^n)^{1/n}}, \qquad \nu_n(y) = \left[\frac{1 + \sqrt{1 + 4 y^{-n}}}{2}\right]^{1/n},
$$
the high-acceleration expansion ($x \gg 1$) is
$$
\mu_n(x) = 1 - \frac{1}{n\,x^n} + O(x^{-2n}) \implies \delta g_{\mu_n}(r) \equiv g(r) - g_N(r) = \frac{a_0}{n}\left(\frac{a_0}{g_N(r)}\right)^{n-1}\bigl(1 + O(y^{-n})\bigr).
$$

| Interpolating Family | Closed-Form $k$-Essence Potential $\mathcal{F}_n(x^2)$ | BTFR $V_f^4$ | Asymptotic Lensing $\alpha_\infty$ | $\delta g(1\text{ AU})\ [\text{m/s}^2]$ | $\delta g(9.54\text{ AU})\ [\text{m/s}^2]$ | $\delta g / g_N(9.54\text{ AU})$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $n=1$: $\mu_1(x) = \frac{x}{1+x}$ | $x^2 - 2x + 2\ln(1+x)$ | $G M a_0$ | $\frac{2\pi\sqrt{G M a_0}}{c^2}$ | $1.200\times 10^{-10}$ | $1.200\times 10^{-10}$ | $1.84\times 10^{-6}$ |
| $n=2$: $\mu_2(x) = \frac{x}{\sqrt{1+x^2}}$ | $x\sqrt{1+x^2} - \operatorname{arsinh}(x)$ | $G M a_0$ | $\frac{2\pi\sqrt{G M a_0}}{c^2}$ | $1.214\times 10^{-18}$ | $1.105\times 10^{-16}$ | $1.70\times 10^{-12}$ |

> [!NOTE]
> **Scientific Assessment:** Both $\mu_1(x)$ and $\mu_2(x)$ possess elementary closed-form covariant $k$-essence potentials $\mathcal{F}_n(Z_H/a_0^2)$ and share the exact same deep-IR galactic asymptotics ($\mathcal{F}_n(x^2) = \frac{2}{3}x^3 + O(x^{3+n})$, $V_f^4 = G M a_0$, $\alpha_\infty = 2\pi\sqrt{G M a_0}/c^2$). However, because $\mu_1(x) = 1 - x^{-1} + \dots$ produces a constant anomalous acceleration $\delta g \approx a_0 = 1.2\times 10^{-10}\text{ m/s}^2$ that is in tension with outer-planet Cassini ranging, $\mu_2(x) = \frac{x}{\sqrt{1+x^2}}$ ($\mathcal{F}_2(x^2) = x\sqrt{1+x^2} - \operatorname{arsinh}(x)$) provides the Solar-System-safe covariant completion while differing from $\mu_1(x)$ by at most $\frac{1}{2}\log_{10}(\frac{1+\sqrt{5}}{2}) \approx 0.1045\text{ dex}$ at $g_N = a_0$ (within the $0.13\text{ dex}$ SPARC observational scatter).
