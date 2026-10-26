# Rotating Horizonless Exponential Compact Objects (Kerr-Like Generalization), Golden-Ratio ISCO, Spinning EHT Shadow, and Dynamical Collapse Arrest (`REFG_ROTATING_HORIZONLESS_KERR_AND_COLLAPSE_ARREST_V1`)

- **Verification Script**: [`verify_rotating_horizonless_kerr_and_collapse_arrest.py`](verify_rotating_horizonless_kerr_and_collapse_arrest.py)
- **Result JSON**: [`rotating_horizonless_kerr_and_collapse_arrest_result.json`](rotating_horizonless_kerr_and_collapse_arrest_result.json)
- **Status**: **`18/18 PASS`**

---

## 1. Stationary Axisymmetric Rotating Horizonless Compact Object & Exact Frame Dragging

In the stationary axisymmetric Gordon–Painlevé–Gullstrand / Hartle–Thorne optical medium with total mass $M$ ($m \equiv GM/c_0^2$) and angular momentum $J = a m c_0 = a_* m^2 c_0$ ($a_* \equiv c_0 J / (G M^2) \in [0, 1]$), the effective line element is:
$$ds^2 = -\left[\mathcal{B}(r) - \mathcal{A}(r)\,r^2\sin^2\theta\,\frac{\omega^2(r)}{c_0^2}\right]c_0^2 dt^2 - \frac{2\omega(r)}{c_0}\,\mathcal{A}(r)\,r^2\sin^2\theta\,c_0 dt\,d\varphi + \mathcal{A}(r)\left(dr^2 + r^2 d\theta^2 + r^2\sin^2\theta\,d\varphi^2\right),$$
where $\mathcal{B}_+(r) = n^{-2}(r) = e^{-2m/r}$ and $\mathcal{A}_+(r) = n^2(r) = e^{2m/r}$ in the vacuum exterior ($r \ge r_c$), matched $C^2$-smoothly at the saturation boundary $r = r_c$ ($q \equiv 2m/r_c$) to the regular de Sitter-like core $\mathcal{B}_-(r) = \exp[-q + b_2(x^2-1) + b_4(x^2-1)^2]$ ($x \equiv r/r_c \le 1$, $b_2 = q/2, b_4 = q/8$) with $\mathcal{A}_-(r) = \mathcal{B}_-^{-1}(r)$.

### Theorem 1 (Exact Exterior Frame-Dragging Law & $C^2$-Regular Core Closure)
1. **Exact Closed-Form Exterior Frame Dragging ($r \ge r_c$)**: Because $\sqrt{-g} = \mathcal{A}(r)\sqrt{\mathcal{A}(r)\mathcal{B}(r)}\,r^2\sin\theta = e^{2m/r}r^2\sin\theta$ in the exterior ($r \ge r_c$), the stationary axisymmetric gravitomagnetic conservation equation $\partial_r\!\left(\sqrt{-g}\,g^{tt}g^{\varphi\varphi}\partial_r\omega\right) = 0$ reduces to:
   $$\frac{d}{dr}\!\left[r^4 e^{2m/r}\,\frac{d\omega_+(r)}{dr}\right] = 0 \implies \frac{d\omega_+(r)}{dr} = -\frac{6 J}{r^4}\,e^{-2m/r} = -\frac{6 a_* m^2 c_0}{r^4}\,e^{-2m/r}.$$
   Integrating from $r \to \infty$ ($\omega_+(\infty) = 0$) in exact closed form yields:
   $$\boxed{\omega_+(r) = \frac{3 J}{2 m^3}\left[1 - \left(1 + \frac{2m}{r} + \frac{2m^2}{r^2}\right)e^{-2m/r}\right] = \frac{3 a_* c_0}{2 m}\left[1 - \left(1 + \frac{2m}{r} + \frac{2m^2}{r^2}\right)e^{-2m/r}\right].}$$
2. **Weak-Field Lense–Thirring Recovery**: Expanding at $r \gg m$ gives:
   $$\omega_+(r) = \frac{2 G J}{c_0^2 r^3}\left(1 - \frac{3m}{2r} + \frac{6m^2}{5r^2} + \mathcal{O}\!\left(\frac{m^3}{r^3}\right)\right),$$
   recovering the exact general-relativistic Lense–Thirring frame-dragging angular velocity $\omega_{\rm LT}(r) = 2GJ/(c_0^2 r^3)$ at leading order with a falsifiable next-to-leading refractive correction $-3m/(2r)$.
3. **$C^2$-Smooth Core Matching & Absence of Ring Singularity and CTCs**: Across $r = r_c$ ($x = 1$), $\omega_+(r)$ matches $C^2$-smoothly to the regular even core profile $\omega_-(x) = \omega_+(r_c) + a_1(x^2-1) + a_2(x^2-1)^2$ ($x \le 1$) with:
   $$a_1 = -\frac{3}{8}\,q^3 e^{-q}\,\frac{a_* c_0}{r_c}, \qquad a_2 = \frac{3}{32}\,q^3(5 - q)e^{-q}\,\frac{a_* c_0}{r_c}.$$
   At the origin $r = 0$, the frame-dragging angular velocity is strictly finite ($\omega(0)/(a_* c_0/r_c) = 0.612171$ for $q = 3/2$) and regular ($\omega'(0) = 0$). Furthermore, because $g_{\varphi\varphi}(r,\theta) = \mathcal{A}(r)r^2\sin^2\theta > 0$ everywhere for $r > 0, \sin\theta \neq 0$, both the Kerr ring singularity ($r=0, \theta=\pi/2$) and Closed Timelike Curves ($g_{\varphi\varphi} < 0$) are completely absent.

---

## 2. Exact Golden-Ratio Static ISCO and Spinning Prograde/Retrograde ISCO

### Theorem 2 (Exact Golden-Ratio ISCO & Spinning Accretion Efficiency)
1. **Static ISCO at Golden-Ratio Radius**: For equatorial circular orbits of massive test particles in the static limit ($a_* = 0$) with $\mathcal{B}(r) = e^{-2m/r}$ and $\mathcal{A}(r) = e^{2m/r}$ (areal radius $R_{\rm ar}(r) = r e^{m/r}$), the specific energy $\tilde{E} = E/(m_0 c_0^2)$ and specific angular momentum $\tilde{L} = L/(m_0 m c_0)$ are:
   $$\tilde{E}^2(r) = \frac{r - m}{r - 2m}\,e^{-2m/r}, \qquad \tilde{L}^2(r) = \frac{r^2}{m(r - 2m)}\,e^{2m/r}.$$
   Marginal stability ($d\tilde{E}^2/dr = 0 \iff d\tilde{L}^2/dr = 0$) satisfies the exact quadratic equation:
   $$r^2 - 6mr + 4m^2 = 0 \implies \boxed{r_{\rm ISCO}^{(0)} = (3 + \sqrt{5})\,m = 2\phi^2 m \approx 5.236068\,m,}$$
   where $\phi = \frac{1+\sqrt{5}}{2}$ is the golden ratio! The corresponding gauge-invariant areal radius is $R_{\rm ar, ISCO}^{(0)} = (3+\sqrt{5})e^{1/(3+\sqrt{5})}m \approx 6.337940\,m$ (compared to $6m$ in Schwarzschild), with specific energy $\tilde{E}_{\rm ISCO}^{(0)} \approx 0.945210$, angular momentum $\tilde{L}_{\rm ISCO}^{(0)} \approx 3.513135$, and radiative thin-disk accretion efficiency:
   $$\eta_{\rm acc}^{(0)} = 1 - \tilde{E}\!\left(r_{\rm ISCO}^{(0)}\right) = 5.4790\% \quad (\text{vs. } 5.7191\% \text{ in Schwarzschild}).$$
2. **Spinning Prograde and Retrograde ISCO Shifts**: For general spin $a_* \in [0, 0.9]$, the circular orbit condition $\partial_r g_{tt} + 2\Omega\,\partial_r g_{t\varphi} + \Omega^2\,\partial_r g_{\varphi\varphi} = 0$ and marginal stability condition $d\tilde{E}/dr = 0$ yield monotonic inward (prograde) and outward (retrograde) shifts:

| Spin $a_*$ | $r_{\rm ISCO}^{\rm pro}/m$ | $R_{\rm ar, ISCO}^{\rm pro}/m$ | $\eta_{\rm acc}^{\rm pro}$ (%) | $r_{\rm ISCO}^{\rm ret}/m$ | $\eta_{\rm acc}^{\rm ret}$ (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| $0.0$ | $5.2361$ | $6.3379$ | $5.479\%$ | $5.2361$ | $5.479\%$ |
| $0.3$ | $4.5732$ | $5.6897$ | $6.517\%$ | $5.8599$ | $4.756\%$ |
| $0.5$ | $4.1003$ | $5.2323$ | $7.551\%$ | $6.2597$ | $4.389\%$ |
| $0.7$ | $3.5993$ | $4.7564$ | $9.124\%$ | $6.6499$ | $4.084\%$ |
| $0.9$ | $3.0616$ | $4.2546$ | $11.988\%$ | $7.0319$ | $3.825\%$ |

---

## 3. Spinning Equatorial Photon Rings and EHT Shadow Diameter ($d_{\rm sh}(a_*, i)$)

For equatorial null geodesics, the critical photon orbits $r_{\rm ph}^{\pm}(a_*)$ and impact parameters $b_{\rm ph}^{\pm}(a_*)$ satisfy $\frac{d}{dr}\!\left(\frac{g_{\varphi\varphi}}{D(r, b)}\right) = 0$ with $D(r, b) = -g_{tt} - 2\omega g_{\varphi\varphi}/b - g_{\varphi\varphi}/b^2 = 0$. For an observer at inclination $i$, the horizontal centroid shift is $\Delta x_{\rm sh}(a_*, i) = \frac{1}{2}(b_{\rm ph}^- - b_{\rm ph}^+)\sin i$ and the orientation-averaged shadow radius is $\bar{b}_{\rm sh}(a_*, i) = \frac{1}{2}\!\left[\frac{1}{2}(b_{\rm ph}^+ + b_{\rm ph}^-)\sin i + b_{\rm ph}^{(0)}(1 - \frac{1}{2}\sin i)\right]$:

- **Static Limit ($a_* = 0$)**: $r_{\rm ph}^{(0)} = 2m$, $b_{\rm ph}^{(0)} = 2e\,m \approx 5.436564\,m$.
- **M87* ($a_* = 0.9, i = 17^\circ, \theta_g = 3.8\,\mu\text{as}$)**:
  $$b_{\rm ph}^+ = 3.6350\,m, \quad b_{\rm ph}^- = 6.2351\,m, \quad \bar{b}_{\rm sh} = 5.3629\,m \implies \boxed{d_{\rm sh}^{\rm RefG}(\text{M87}^*) = 40.76\,\mu\text{as}},$$
  versus EHT observed $42.0 \pm 3.0\,\mu\text{as}$ (**$0.41\sigma < 1\sigma$**, with horizontal centroid shift $\Delta x_{\rm sh} = 0.380\,m$).
- **Sgr A* ($a_* = 0.7, i = 30^\circ, \theta_g = 5.028\,\mu\text{as}$)**:
  $$b_{\rm ph}^+ = 4.2124\,m, \quad b_{\rm ph}^- = 6.0870\,m, \quad \bar{b}_{\rm sh} = 5.3150\,m \implies \boxed{d_{\rm sh}^{\rm RefG}(\text{Sgr A}^*) = 53.45\,\mu\text{as}},$$
  versus EHT observed $48.7 \pm 7.0\,\mu\text{as}$ (**$0.68\sigma < 1\sigma$**, improving over the static $0.85\sigma$ tension, with horizontal centroid shift $\Delta x_{\rm sh} = 0.469\,m$).

---

## 4. Dynamical Gravitational Collapse Arrest at $R = r_c$

### Theorem 4 (Singularity-Free Bounce & Stable Equilibrium at $R = r_c$)
During dynamical gravitational collapse of a spherical shell of radius $R(\tau)$ ($y \equiv R/r_c$), the competition between the inward gravitational pull of the enclosed active mass $m_{\rm eff}(y) = m\,y^3 e^{q(1-y^2)}$ (for $y \le 1$) and the outward refractive vacuum saturation pressure $p_r = -\rho c_0^2$ generates the dimensionless radial equation of motion:
$$\ddot{y} + \gamma_{\rm rad}\dot{y} = F_{\rm rad}(y) = -\frac{dU_{\rm eff}(y)}{dy} = \begin{cases} -\dfrac{q}{2y^2}, & y \ge 1, \\[8pt] -\dfrac{q}{2y^2}\left[1 - y^{-2}e^{q(1-y^2)}\right], & 0 < y < 1. \end{cases}$$
1. **Exact Equilibrium at $R = r_c$ ($y = 1$)**: At $y = 1$, the inward gravitational acceleration and outward refractive saturation stress balance identically:
   $$F_{\rm rad}(1) = -\frac{q}{2}\left[1 - 1^{-2}e^0\right] = 0.$$
2. **Positive Restoring Stiffness & Bounce Frequency**: Differentiating at $y = 1^-$ yields a strictly positive restoring stiffness for all $q > 0$:
   $$\boxed{U_{\rm eff}''(1) = -\left.\frac{dF_{\rm rad}}{dy}\right|_{y=1^-} = q(1 + q) > 0, \qquad \omega_{\rm bounce} = \sqrt{q(1+q)}\,\frac{c_0}{r_c}.}$$
   For the canonical saturation parameter $q = 3/2$ ($r_c = 4m/3$), $U_{\rm eff}''(1) = 15/4 = 3.75 > 0$ and $\omega_{\rm bounce} = \frac{\sqrt{15}}{2}\frac{c_0}{r_c} \approx 1.9365\,\frac{c_0}{r_c}$.
3. **Repulsive Core Barrier & Time-Dependent Bounce**: As $y \to 0^+$, $U_{\rm eff}(y) \sim \frac{q e^q}{6 y^3} \to +\infty$, creating an impenetrable repulsive refractive core barrier that guarantees a strictly positive turning point $y_{\rm turn} > 0$ ($y_{\rm turn} = 0.7303 > 0$ for infall from $y_0 = 2.5$). With radiative ringdown damping ($\gamma_{\rm rad} > 0$), the collapsing shell bounces smoothly at $y_{\min} = 0.8126 > 0$ without forming a curvature singularity or an event horizon, and settles asymptotically to the stable equilibrium radius $y_\infty = 1.0000$ ($R_\infty = r_c$).
