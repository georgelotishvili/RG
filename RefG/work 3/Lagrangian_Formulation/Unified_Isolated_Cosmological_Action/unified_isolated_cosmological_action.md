# Unified Isolated and Cosmological Action with Regular $J_C \to 0$ Reduction

## Decision Summary

Direct evaluation of W3-54's hydrodynamic current variables $(J_C^\mu, \theta_C)$ at $n_C \to 0^+$ fails around any gravitating localized body whenever $\rho_C'(0) = \mu_{C0} > 0$: $n_C = \sqrt{-g_{\mu\nu}J_C^\mu J_C^\nu}/e$ has a directional derivative discontinuity at $J_C^\mu = 0$, the unit velocity $u^\mu = J_C^\mu/(e n_C)$ is indeterminate ($0/0$), and the $J_C^\mu$ equation of motion forces the eikonal constraint $X_C \equiv -g^{\mu\nu}\partial_\mu\theta_C\partial_\nu\theta_C = (\mu_{C0}/c_0)^2$, which cannot be satisfied by a stationary phase $\theta_C = -\omega_C t$ on an inhomogeneous lapse $N(r) \neq \text{const}$.

This obstruction is resolved by retaining the non-negative collective squared-amplitude auxiliary variable $x \ge 0$ (or the regular Cartesian complex order parameter $\Psi_C = (\phi_{C1}+i\phi_{C2})/\sqrt{2}$ with $x = |\Psi_C|^2$) in the unified post-Genesis coframe action `REFG_UNIFIED_COVARIANT_V1`. Eliminating $J_C^\mu$ before $x$ produces the polynomial-in-$x$ action $S_C^{\rm (dual)}[e, x, \theta_C] = \frac{1}{c_0}\int d^4x\,e\left[\frac{1}{2}c_0^2 x X_C - U_C(x)\right]$ with $U_C(0)=0$. On the active branch $x > 0$, algebraic stationarity in $x$ recovers W3-54's exact barotropic current action, Hilbert tensor, and W3-62's dilute cold-dust limit. On the vacuum branch $x = 0$ ($\Psi_C = 0$), the collective Euler–Lagrange equations, current $J_C^\mu$, and Hilbert stress $T^C_{\mu\nu}$ vanish identically on every curved metric $g_{\mu\nu}$, reducing the unified action to `REFG_ISOLATED_COVARIANT_V2` with zero residual.

---

## Frozen Verification Contract

- `CLAIM_ID`: `REFG_UNIFIED_ISOLATED_COSMOLOGICAL_ACTION_V1`
- `CLAIM`: W3-54's hydrodynamic $(J_C^\mu, \theta_C)$ representation with $\rho_C'(0) = \mu_{C0} > 0$ has an exact directional-derivative and inhomogeneous-lapse eikonal obstruction at $J_C^\mu \to 0$. Formulating the collective sector in the parent envelope variables $(x, \theta_C, J_C^\mu)$ with $x \ge 0$ (or Cartesian complex $\Psi_C$) yields one unified covariant action `REFG_UNIFIED_COVARIANT_V1` that (1) reduces identically to `REFG_ISOLATED_COVARIANT_V2` on the regular $\Psi_C = 0$ ($x = 0, J_C^\mu = 0$) submanifold for any curved metric, and (2) reduces identically to W3-54's barotropic phase-current action and W3-62's dilute dust limit on the active $x > 0$ branch.
- `TYPE`: `EXACT_VARIATIONAL_UNIFICATION_AND_BOUNDARY_OBSTRUCTION_THEOREM`
- `MODEL_VERSION`: `REFG_UNIFIED_COVARIANT_V1`
- `ASSUMPTIONS`:
  1. Connected, oriented, time-oriented $3+1$ coframe $e^A{}_\mu$ with internal Minkowski metric $\eta_{AB} = \mathrm{diag}(-1,1,1,1)$, $g_{\mu\nu} = \eta_{AB}e^A{}_\mu e^B{}_\nu$, $e = \det(e^A{}_\mu) > 0$, and flat inertial spin connection $\omega^A{}_{B\mu}$ selected at the W3-54 TEGR ratio $(c_1,c_2,c_3)=(1/4,1/2,-1)$.
  2. Universal minimal metric coupling of the localized oscillon complex scalar $\Psi$, the Maxwell gauge field $A_\mu$, and the collective phase sector.
  3. Smooth convex collective potential $U_C(x)$ on $x \ge 0$ with $U_C(0) = 0$, $U_C'(0) = \frac{1}{2}\mu_{C0}^2 > 0$, and $U_C''(x) > 0$ (instantiated by $U_C(x) = \frac{1}{2}\mu_{C0}^2 x + \frac{1}{4}\lambda_C x^2$, $\lambda_C > 0$).
  4. Once-only vacuum slot $\Lambda_F$ on the geometric side; no vacuum offset inside $V(|\Psi|)$ or $U_C(x)$.
- `DOMAIN`: Smooth Lorentzian coframes ($e > 0$); both the vacuum submanifold $x = 0$ ($\Psi_C = 0, J_C^\mu = 0$) on arbitrary curved spacetimes and the active timelike collective branch $x > 0, X_C > 2 U_C'(0)/c_0^2$. Excluded are pregeometric node dynamics, Genesis percolation, and quantum loop corrections.
- `CONVENTIONS`: Signature `(-+++)`, $x^0 = c_0 t$, $e = \sqrt{-g} > 0$, Hilbert stress tensor $T_{\mu\nu} = -\frac{2c_0}{e}\frac{\delta S_{\rm matter}}{\delta g^{\mu\nu}}$, $X_C \equiv -g^{\mu\nu}\partial_\mu\theta_C\partial_\nu\theta_C$, and $n_C \equiv \sqrt{-g_{\mu\nu}J_C^\mu J_C^\nu}/e$.
- `FREEDOM_LEDGER`:
  - Gravitational constants: $G > 0$ and $\Lambda_F$ (with $\Lambda_F = 0$ on the asymptotically flat isolated branch).
  - Oscillon potential parameters: $(m, \lambda, g_6)$ inherited unchanged from W3-58 and `REFG_ISOLATED_COVARIANT_V2`.
  - Collective constitutive function: $U_C(x)$ with $U_C(0)=0, U_C'(0)>0, U_C''(x)>0$; no data-fitted parameters or interpolation switches.
- `DEPENDENCIES`:
  - `RefG/work 3/Inertia/foundation_revision.md`: `588ca272af1c7842c33836e3d73df3ed4d087c0ffe218863c6e5045b565f2425`
  - `RefG/work 3/Inertia/verify_foundation_revision.py`: `12e4cd5234569b0a564ea68b3542b5139675d70870859c57618dc746d7638baa`
  - `RefG/work 3/Lagrangian_Formulation/Oscillon_Inertia/oscillon_inertia.md`: `6a8c95f557d4ffac01a404eef3eef54b81c2fe3fd5aca97556cf39d9bda8ea55`
  - `RefG/work 3/Lagrangian_Formulation/Oscillon_Inertia/verify_oscillon_inertia.py`: `32cf32e9cfd590f93928eff16cbfe5494836df8b9d72bfd88b3cf3ba7da22076`
  - `RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md`: `6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879`
  - `RefG/work 3/Cosmology_and_LSS/CMB_Closure/w3_62_cmb_einstein_source_linear_closure_preregistration.md`: `b4068791b63e9a072a897e9aa85eae96c588b0d33533effb9664ffbd667ae810`
- `METHOD`: Direct SymPy symbolic variation of the W3-54 hydrodynamic action, the envelope/dual action $S_C^{\rm (env)} / S_C^{\rm (dual)}$, and the Cartesian complex field action $S_C^{\rm (field)}$; Legendre/envelope elimination on $x > 0$; Kuhn–Tucker and Cartesian Euler–Lagrange evaluation at $x = 0$ ($\Psi_C = 0$); and negative mutation controls.
- `PASS_CONDITION`: Every symbolic residual simplifies to exact zero; the W3-54 $J_C \to 0$ directional and inhomogeneous-lapse obstructions are proved; the $\Psi_C = 0$ ($x = 0$) branch satisfies all collective field equations on an arbitrary curved metric and reproduces `REFG_ISOLATED_COVARIANT_V2`; the $x > 0$ branch reproduces W3-54 and W3-62; all upstream dependency hashes match; and all negative controls are rejected.
- `FAIL_CONDITION`: Any nonzero symbolic residual, failure of the $x = 0$ branch on a curved metric, mismatch with W3-54 on $x > 0$, source double-counting, or a passing negative control.
- `FALSIFIER`: A nonzero collective stress or unsatisfied collective field equation at $\Psi_C = 0$ ($x = 0$), or failure of the $x > 0$ envelope reduction to reproduce $p_C = n_C \rho_C'(n_C) - \rho_C(n_C)$.
- `RESIDUAL`: Exact symbolic zero across all variational, Legendre, stress-tensor, conservation, and reduction identities.
- `ERROR_BOUND`: Zero algebraic error.
- `VALIDITY_HEALTH`: Smooth polynomial dependence on $\Psi_C$ (and $x$) at the vacuum boundary $x = 0$; positive energy density $\rho_C > 0$, positive chemical potential $\rho_C'(n_C) > 0$, and causal sound speed $0 < c_{s,C}^2 < 1/3$ on the active quartic branch $x > 0$.
- `BRANCHES`:
  - Isolated vacuum branch: $\Psi_C = 0$ ($x = 0, J_C^\mu = 0, n_C = 0$), reducing to `REFG_ISOLATED_COVARIANT_V2`.
  - Active collective branch: $x > 0$ ($X_C > \mu_{C0}^2/c_0^2$), reducing at leading gradients to W3-54 and in the dilute limit $\eta \to 0^+$ to W3-62.
  - Sub-threshold phase branch in dual variables: $X_C \le \mu_{C0}^2/c_0^2 \implies x_* = 0, P_C = 0, n_C = 0$.
- `OBSERVABLE_MAP`: Inherits the clock $p_T = N$, ruler $p_L = 1/A_{\rm iso}$, and $M_I = M_{\rm active} = M_{\rm passive} = E_0/c_0^2$ dictionary on the $x = 0, \Lambda_F = 0$ branch, and the operational FLRW dictionary $A = a_F/p$ on the homogeneous cosmological branch.
- `FORWARD_MODEL`: N/A (exact action-level unification and reduction).
- `DATA_ROLE`: `NO_DATA_READ_OR_FITTED`.
- `IDENTIFIABILITY`: Fixes the mathematical bridge between the $J_C = 0$ isolated sector and the $n_C > 0$ collective sector; does not fix the numerical values of $\mu_{C0}, \lambda_C$, or $\Lambda_F$.
- `BENCHMARK`: Exact recovery of `REFG_ISOLATED_COVARIANT_V2` at $x = 0$ and W3-54 / W3-62 / W3-80 on $x > 0$.
- `CLOSURE_FLAGS`:
  - `w54_hydrodynamic_zero_current_obstruction_proved = true`
  - `unified_action_regular_at_zero_collective_field = true`
  - `isolated_covariant_v2_recovered_exact = true`
  - `w54_barotropic_source_recovered_on_positive_branch = true`
  - `w62_dilute_cold_dust_limit_recovered_exact = true`
  - `once_only_unified_source_ledger_verified = true`
  - `inhomogeneous_ambient_background_perturbation_solved = false`
  - `microscopic_node_origin_derived = false`
- `CROSSCHECK`: Compare (1) direct metric variation of $S_C^{\rm (env)}[e, x, \theta_C, J_C^\mu]$ at fixed $J_C^\mu$, (2) metric variation of the dual action $S_C^{\rm (dual)}[e, x, \theta_C]$ at fixed $\theta_C$, and (3) metric variation of W3-54's $S_C[e, J_C^\mu, \theta_C]$ after eliminating $x$; all three yield the identical Hilbert stress tensor $T^C_{\mu\nu}$ on $x > 0$.
- `PROVENANCE`: Standalone script `verify_unified_isolated_cosmological_action.py` verifying all upstream SHA-256 hashes and printing deterministic UTF-8 JSON to stdout.
- `FILES`: `unified_isolated_cosmological_action.md` and `verify_unified_isolated_cosmological_action.py`.

---

## 1. Exact Diagnosis of the W3-54 Hydrodynamic Vacuum Obstruction

In W3-54, the collective sector is written solely in terms of the vector density $J_C^\mu$ and phase $\theta_C$:
$$S_C^{\rm (W54)}[e, J_C^\mu, \theta_C] = \int d^4x \left[ J_C^\mu \partial_\mu \theta_C - \frac{e}{c_0} \rho_C(n_C) \right], \qquad n_C = \frac{\sqrt{-g_{\mu\nu} J_C^\mu J_C^\nu}}{e}.$$

Attempting to take the isolated vacuum limit $J_C^\mu \to 0$ directly inside $S_C^{\rm (W54)}$ encounters two exact obstructions:

1. **Directional non-differentiability at $J_C^\mu = 0$:**
   For any timelike ray $J_C^\mu = \epsilon w^\mu$ with $\epsilon > 0$ and $-g_{\mu\nu} w^\mu w^\nu > 0$,
   $$\frac{\partial n_C}{\partial J_C^\mu} = -\frac{g_{\mu\nu} w^\nu}{e \sqrt{-g_{\alpha\beta} w^\alpha w^\beta}},$$
   which is independent of $\epsilon$ and depends on the unit direction $u^\mu = w^\mu / \sqrt{-g_{\alpha\beta} w^\alpha w^\beta}$. Thus $\lim_{J_C \to 0} (\partial n_C / \partial J_C^\mu)$ does not exist, and the Euler–Lagrange derivative $\frac{\delta S_C^{\rm (W54)}}{\delta J_C^\mu} = \partial_\mu \theta_C + \frac{\rho_C'(n_C)}{c_0} u_\mu$ is undefined at $J_C^\mu = 0$ whenever $\rho_C'(0) = \mu_{C0} > 0$.

2. **Inhomogeneous-lapse eikonal incompatibility:**
   On any open domain where $n_C > 0$, contracting $\partial_\mu \theta_C = -\frac{\rho_C'(n_C)}{c_0} u_\mu$ with $g^{\mu\nu}$ gives the eikonal identity
   $$X_C \equiv -g^{\mu\nu} \partial_\mu \theta_C \partial_\nu \theta_C = \left(\frac{\rho_C'(n_C)}{c_0}\right)^2.$$
   In the limit $n_C \to 0^+$ with $\rho_C'(0) = \mu_{C0} > 0$ (required by W3-62's cold dust law $\rho_C = \mu_{C0} n_C + O(n_C^2)$), this forces $X_C = (\mu_{C0}/c_0)^2 = \text{const}$. However, on the static spherically symmetric spacetime of a localized oscillon,
   $$ds^2 = -N(r)^2 c_0^2 dt^2 + A_{\rm iso}(r)^2 d\mathbf{x}^2,$$
   a stationary collective phase $\theta_C = -\omega_C t$ has $X_C(r) = \frac{\omega_C^2}{c_0^2 N(r)^2}$ and radial derivative
   $$\frac{d X_C}{dr} = -\frac{2 \omega_C^2 N'(r)}{c_0^2 N(r)^3} \neq 0 \quad \text{whenever } N'(r) \neq 0.$$
   Hence no global stationary $n_C \to 0^+$ limit exists in the bare hydrodynamic variables $(J_C^\mu, \theta_C)$ around a gravitating body.

---

## 2. Regular Parent Formulation and the Unified Action `REFG_UNIFIED_COVARIANT_V1`

The obstruction arises because W3-54 eliminated the collective squared amplitude $x = |\Psi_C|^2 \ge 0$ prior to taking $J_C^\mu \to 0$. Retaining $x \ge 0$ (or the full complex order parameter $\Psi_C = (\phi_{C1} + i \phi_{C2})/\sqrt{2}$) removes the square root $\sqrt{-g_{\mu\nu} J_C^\mu J_C^\nu}$ from the action.

The unified post-Genesis action is
$$S_{\rm unified} = S_{\rm TEGR}[e, \omega] + S_{\rm osc}[e, \Psi] + S_{\rm EM}[e, A_\mu] + S_C + S_{\rm boundary},$$
where:
$$S_{\rm TEGR}[e, \omega] = -\frac{c_0^3}{16\pi G} \int d^4x \, e \left( T_{\rm TEGR} + 2\Lambda_F \right) = \frac{c_0^3}{16\pi G} \int d^4x \, e \left( R_{\rm LC} - 2\Lambda_F \right) + S_{\rm boundary}^{\rm TEGR},$$
$$S_{\rm osc}[e, \Psi] = -\int d^4x \, e \left[ g^{\mu\nu} \partial_\mu \Psi^* \partial_\nu \Psi + V(|\Psi|) \right], \qquad V(f) = \frac{1}{2}m^2 f^2 - \frac{1}{4}\lambda f^4 + \frac{1}{6}g_6 f^6,$$
$$S_{\rm EM}[e, A_\mu] = -\frac{1}{4} \int d^4x \, e \, g^{\mu\alpha} g^{\nu\beta} F_{\mu\nu} F_{\alpha\beta}.$$

For the collective sector $S_C$, the first-order envelope representation is
$$S_C^{\rm (env)}[e, x, \theta_C, J_C^\mu] = \int d^4x \left[ J_C^\mu \partial_\mu \theta_C - \frac{e}{c_0} \left( \frac{-g_{\mu\nu} J_C^\mu J_C^\nu}{2 e^2 x} + U_C(x) \right) \right].$$
Varying $J_C^\mu$ at fixed $(e, x, \theta_C)$ gives the non-singular linear relation
$$J_C^\mu = -c_0 e x g^{\mu\nu} \partial_\nu \theta_C,$$
and substituting this back into $S_C^{\rm (env)}$ yields the polynomial-in-$x$ dual action
$$S_C^{\rm (dual)}[e, x, \theta_C] = \frac{1}{c_0} \int d^4x \, e \left[ \frac{1}{2} c_0^2 x X_C - U_C(x) \right], \qquad x \ge 0.$$
Including the collective amplitude gradient $\partial_\mu \sqrt{x}$ corresponds to the full complex-scalar parent action
$$S_C^{\rm (field)}[e, \Psi_C] = -\frac{1}{c_0} \int d^4x \, e \left[ \frac{1}{2} c_0^2 g^{\mu\nu} \partial_\mu \Psi_C^* \partial_\nu \Psi_C + U_C(|\Psi_C|^2) \right], \qquad \Psi_C = \frac{\phi_{C1} + i \phi_{C2}}{\sqrt{2}}.$$

---

## 3. Exact Reductions to `REFG_ISOLATED_COVARIANT_V2`, W3-54, and W3-62

### 3.1. Regular Vacuum Reduction ($J_C^\mu \to 0 \iff x = 0 \iff \Psi_C = 0$)
1. **In Cartesian complex variables ($\Psi_C = 0$):**
   For $U_C(|\Psi_C|^2)$ with $U_C(0) = 0$ and finite $U_C'(0)$, the Euler–Lagrange equations
   $$\frac{\delta S_C^{\rm (field)}}{\delta \phi_{C a}} = \frac{e}{c_0} \left[ c_0^2 \Box_g \phi_{C a} - U_C'\!\left(\frac{\phi_{C1}^2+\phi_{C2}^2}{2}\right) \phi_{C a} \right] = 0 \quad (a=1,2)$$
   are satisfied **identically** at $\phi_{C1} = \phi_{C2} = 0$ on **any** curved metric $g_{\mu\nu}(x)$, with $J_C^\mu = 0$ and $T^C_{\mu\nu} = 0$.
2. **In dual envelope variables ($x \ge 0$):**
   For $U_C(x) = \frac{1}{2}\mu_{C0}^2 x + \frac{1}{4}\lambda_C x^2$ ($\lambda_C > 0$), the derivative with respect to $x$ is
   $$\frac{\partial}{\partial x}\left[\frac{1}{2} c_0^2 x X_C - U_C(x)\right] = \frac{1}{2}\left(c_0^2 X_C - \mu_{C0}^2\right) - \frac{1}{2}\lambda_C x.$$
   Throughout any sub-threshold region where $c_0^2 X_C \le \mu_{C0}^2$, the unique maximum on $x \ge 0$ is the boundary point $x_* = 0$, at which $J_C^\mu = -c_0 e x_* g^{\mu\nu}\partial_\nu\theta_C = 0$, $n_C = x_* c_0 \sqrt{X_C} = 0$, $p_C = 0$, and $T^C_{\mu\nu} = 0$.
3. **Exact recovery of `REFG_ISOLATED_COVARIANT_V2`:**
   Setting $\Psi_C = 0$ ($x = 0$) and $\Lambda_F = 0$ leaves
   $$S_{\rm unified}\big|_{\Psi_C=0, \Lambda_F=0} = S_{\rm REFG\_ISOLATED\_COVARIANT\_V2}[e, \omega, \Psi, A_\mu], \qquad T^{\rm total}_{\mu\nu}\big|_{\Psi_C=0} = T^{\rm osc}_{\mu\nu} + T^{\rm EM}_{\mu\nu},$$
   preserving the exact whole-body ADM inertia theorem $M_I = M_{\rm active} = M_{\rm passive} = E_0/c_0^2$ and the spherical clock-ruler departure identity.

### 3.2. Active Collective Branch ($x > 0$) and W3-54 / W3-62 Recovery
On the active branch $x > 0$ ($c_0^2 X_C > \mu_{C0}^2$):
1. **Envelope elimination of $x$ at fixed $J_C^\mu$:**
   With $n_C = \sqrt{-g_{\mu\nu}J_C^\mu J_C^\nu}/e > 0$, minimizing $\rho_C^{\rm (env)}(x; n_C) \equiv \frac{n_C^2}{2x} + U_C(x)$ over $x > 0$ gives
   $$-\frac{n_C^2}{2 x_*^2} + U_C'(x_*) = 0 \implies n_C = x_* \sqrt{2 U_C'(x_*)},$$
   and by the envelope theorem,
   $$\rho_C(n_C) = \frac{n_C^2}{2 x_*} + U_C(x_*), \qquad \rho_C'(n_C) = \frac{n_C}{x_*} = \sqrt{2 U_C'(x_*)} = c_0 \sqrt{X_C},$$
   $$p_C(n_C) = n_C \rho_C'(n_C) - \rho_C(n_C) = \frac{n_C^2}{2 x_*} - U_C(x_*) = \frac{1}{2} c_0^2 x_* X_C - U_C(x_*).$$
2. **Exact equivalence of Hilbert stress tensors:**
   Varying $g^{\mu\nu}$ in $S_C^{\rm (dual)}[e, x, \theta_C]$ gives
   $$T^{C,{\rm dual}}_{\mu\nu} = c_0^2 x \partial_\mu \theta_C \partial_\nu \theta_C + \left[\frac{1}{2} c_0^2 x X_C - U_C(x)\right] g_{\mu\nu}.$$
   Substituting $\partial_\mu \theta_C = -\sqrt{X_C} u_\mu$ and $x = x_*(n_C)$ yields identically
   $$T^{C,{\rm dual}}_{\mu\nu} = (\rho_C + p_C) u_\mu u_\nu + p_C g_{\mu\nu} = T^{C,{\rm W54}}_{\mu\nu}.$$
3. **Dilute W3-62 cold-dust limit:**
   For $U_C(x) = \frac{1}{2}\mu_{C0}^2 x + \frac{1}{4}\lambda_C x^2$ (in $c_0 = 1$ units) with dimensionless dilution parameter $\eta \equiv \lambda_C x / \mu_{C0}^2 > 0$:
   $$\frac{\rho_C}{\mu_{C0} n_C} = \frac{1 + \frac{3}{4}\eta}{\sqrt{1 + \eta}} = 1 + \frac{1}{4}\eta - \frac{3}{32}\eta^2 + O(\eta^3), \qquad w_C = \frac{p_C}{\rho_C} = \frac{\eta}{4 + 3\eta}, \qquad c_{s,C}^2 = \frac{dp_C}{d\rho_C} = \frac{\eta}{2 + 3\eta}.$$
   As $\eta \to 0^+$ on the expanding cosmological branch ($n_{C,{\rm op}} \propto A^{-3} \to 0$), $w_C \to 0$, $c_{s,C}^2 \to 0$, and $\rho_C / (\mu_{C0} n_C) \to 1$, recovering W3-62's cold Einstein dust branch without losing regularity at $x = 0$.
