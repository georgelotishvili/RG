# Oscillon inertia from one covariant foundation--matter action

Date: 2026-09-24. Action-level derivation and reproducible weak-field tests.

The action below is the isolated sector specified in
[the foundation revision](../../Inertia/foundation_revision.md), with
canonical Maxwell propagation included there.
Omission of W54's collective current is a new isolated-sector definition,
not a derived J_C=0 truncation of its n_C>0 action. The ADM proof and
canonical equilibrium equations below are unchanged; their inference to
a unified cosmological/microscopic medium is not established by this work.

## Model and verification contract

CLAIM_ID: REFG_COVARIANT_OSCILLON_INERTIA_V1.
Goal: derive inertia, conserved momentum and leading weak external-force
response of a localized oscillon including its gravitational environment.
The domain is an isolated localized body, its asymptotic momentum and its
leading weak external-force response. Horizon, collapse, cosmology,
particle-spectrum and observational calculations lie outside this domain.

MODEL / ASSUMPTIONS: select the existing W54 TEGR/EH + W58 canonical
complex-field branch (also explicitly combined in W64), signature -+++,
c0=1, alpha=4 pi G, Lambda=0, asymptotically flat isolated system,
matched gravitational boundary term, one universally coupled metric.
The isolated action omits the homogeneous collective source and sets
Lambda=0; no independent APR u-field or W92 material-label source is added.
This defines the isolated sector as a separate effective action. Its
derivation as a vacuum limit of the collective-current theory remains open.
In amplitude/phase form:

    S = integral sqrt(-g) [R/(16 pi G)
        - (grad f)^2/2 - f^2(grad theta)^2/2 - V(f)] d^4x + S_boundary,
    V(f)=f^2/2-f^4/4+f^6/24, Psi=f exp(i theta)/sqrt(2).

Here the canonically normalized complex field is Psi, so its kinetic term
is -grad(Psi*) grad(Psi). All radial equations below use the real amplitude f.

This uses the already declared low-energy constitutive action, not a
derivation of that action from microscopic foundation nodes. The model
choice replaces APR's preferred-frame scalar dynamics. It does NOT preserve
the exact APR rest profile, its energy value, fixed-Q Hessian, exact global
single-p diagonal ansatz, or finite-b law. The same potential, charge
normalization, universal matter/light metric, and self-consistent equilibrium
requirement are retained. Exact common p is not imposed on independent
metric equations. A coordinate boost is not used to repair the old APR
equations.

TYPE / DOMAIN: exact same-action Noether and asymptotic-charge derivation;
numerical evidence for one weak self-gravitating rest state. Uniform boosts
|v|<1 of a regular rest solution; leading adiabatic monopole acceleration in
a slowly varying external field. Finite-size, tidal, radiation-reaction and
fast internal-mode driving are outside that approximation. Flat-space
Laue is used only for the flat oscillon. Gravitating total energy/momentum
are ADM boundary charges, not a local gravitational Hilbert tensor.

METHOD:
1. Derive amplitude, phase-current and stress equations from this action.
2. Derive the flat oscillon's stress balance and boost energy/momentum.
3. Derive the FULL boosted asymptotic metric and independently integrate ADM
   energy and momentum, retaining shift and time-dependent spatial metric.
4. Construct one same-charge weak equilibrium using independent mass/lapse
   equations, with a scalar Robin tail and a charge equation.
5. Verify ADM=Komar rest mass, including exterior boundary information.
6. Obtain the leading worldline action from the rest energy, physical
   Lorentz symmetry and universal coupling; derive force and inertia.

BENCHMARK / FREEDOMS: fixed full Q=190.401136223484, alpha=.001; the
potential and W58 Omega=.8 flat seed are inherited, not fitted to inertia.
No coefficient is chosen to cancel APR's 2.178224% difference.
Use radii 40 and 60, tolerances 1e-7 and 3e-8, 8001 and 16001 integration
points respectively. Centre epsilon=1e-5 with regular series; an epsilon/2
check at the fine domain verifies the origin error. Angular boost integrals
use at least 48 Gauss nodes and v in {.2,.6,.8}. Fixed-Q solve is a new
equilibrium in this action; old stability campaigns are not rerun.

ACCEPTANCE / FALSIFIERS:
- exact symbolic action, boost, ADM and force identities have zero residual;
- deliberately omitted shift and preferred-frame APR controls are rejected;
- converged BVP, boundary residual <1e-7, Q relative error <2e-6,
  positive lapse/F and node-free core with min lapse>.9 (weak test only);
- volume ADM / Komar discrepancy <3e-5 relative; domain/refinement changes
  of ADM mass, frequency and centre lapse <3e-5 relative;
- angular ADM boost charges agree with derived gamma E0 and gamma E0 v
  within 1e-10 relative; invariant mass within 1e-10 relative;
- flat virial/stress residual <3e-6 of total rest energy;
- scalar stress principal kinetic sign and EH tensor sign retained.
Numerical failure is recorded, not suppressed or repaired by changing a
threshold. Floating-point passes are not interval-certified proofs.
The algebraic mass identity is not established by assigning M_I=E0 in code:
the ADM integrands and momentum derivative must be computed separately.

SCOPE: the explicit inertia derivation and weak-state witness apply to the
specified covariant action. Microscopic origin of that action, exact APR
continuation, nonlinear stability and a unified RefG completion are distinct
claims.
No evidence of observational validation is claimed. The old APR mismatch
remains a valid result in the old action.

FILES: this report and [verify_oscillon_inertia.py](verify_oscillon_inertia.py),
with the [foundation revision](../../Inertia/foundation_revision.md) and
[radial energy-stability test](../../Inertia/radial_stability_revision.md)
providing the current-sector extension.
PROVENANCE: print hashes of this report, verifier, W58 and W54 inputs,
plus environment and numerical output; stdout only, no simulation cache.
DEPENDENCIES: W58 flat profile/potential, W54 TEGR boundary identity,
W64 previously derived spherical equations as a cross-check, APR slow-motion
mismatch as comparison only. All are identified by paths/hashes.
DATA_ROLE / FORWARD_MODEL / IDENTIFIABILITY: N/A for observations; this is
an action-level mathematical construction, not fitting or unique selection
of an ontology. No observational data or physical particle identity used.

## Sources

- W54: ../Relational_Coframe_TEGR_Phase_Source_Closure/.
- W58: ../One_Oscillon_Coframe_Localized_Core/.
- Existing combined action/equations: ../../Strong_Field/W3-64_Einstein_Continuation/
  (read-only dependency; no strong-field calculation is run).
- The earlier APR scalar model is used only for the historical comparison
  in §6; its numerical results are not inputs to this derivation or verifier.
- D. Giulini, Laue's Theorem Revisited (2018), https://arxiv.org/abs/1808.09320:
  total stress, boundary hypotheses and boost covariance in flat space.
- R. Arnowitt, S. Deser and C. W. Misner, The Dynamics of General Relativity
  (1962; accessible reprint 2004), https://arxiv.org/abs/gr-qc/0405109:
  Hamiltonian energy/momentum as asymptotic gravitational surface charges.

## Derivation and verified result

In the selected existing covariant branch, the whole localized object's
inertia is its total rest energy divided by c0 squared. The same mass
sources the static far field and multiplies the leading external
gravitational force. The result includes the oscillon phase, spatial
stress and gravitational environment:

\[
 M_I=M_{\rm active}=M_{\rm passive}=\frac{E_0}{c_0^2},\qquad
 E=\gamma E_0,\quad {\bf P}=\gamma\frac{E_0}{c_0^2}{\bf v}.
\]

The derivation below establishes these statements from the specified
action. Section 6 records the exact change from the old APR model.

### 1. Field equations and the energy ledger

With signature -+++ and c0=1, variation gives

\[
 \Box f-f(\nabla\theta)^2-V_f=0,\qquad
 j^\mu=-f^2\nabla^\mu\theta,\qquad \nabla_\mu j^\mu=0,
\]
\[
 T_{\mu\nu}=\partial_\mu f\partial_\nu f
 +f^2\partial_\mu\theta\partial_\nu\theta
 -g_{\mu\nu}\left[\tfrac12(\nabla f)^2+
 \tfrac12f^2(\nabla\theta)^2+V\right],\qquad
 G_{\mu\nu}=8\pi G T_{\mu\nu}.
\]

The current sign is chosen so that theta=Omega t, Omega>0 has positive
charge on a constant-t slice. On the field equations,
\(\nabla_\mu T^{\mu\nu}=0\). The scalar is the sole localized matter
source in this branch. The gravitational environment contributes to the
total boundary energy through the solved metric. Adding the old APR
foundation-gradient energy to that total would duplicate a sector that
does not occur in this action.

The potential satisfies

\[
 V=\frac{f^2[(f^2-3)^2+3]}{24}\geq0,\qquad
 V_f=f-f^3+\frac{f^5}{4}.
\]

The canonical scalar and positive-sign EH tensor term retain their healthy
principal kinetic signs and share the metric causal cone. This principal
statement is separate from the bound object's radial or nonlinear stability.

### 2. The flat oscillon: why its internal stress matters

First set G=0. For \(f=f(r)\), \(\theta=\Omega t\), define

\[
 T=\frac{\Omega^2 f^2}{2},\quad X=\frac{f'^2}{2},\quad
 \rho=T+X+V,\quad p_r=T+X-V,\quad p_t=T-X-V.
\]

The amplitude equation is \(f''+2f'/r=V_f-\Omega^2f\).
Although the phase oscillates, the stress tensor is stationary.
Conservation and localization imply the Laue balance:

\[
 0=\int \partial_k(x^iT^{kj})\,d^3x
   =\int T^{ij}\,d^3x .
\]

The boundary term vanishes for the exponentially localized profile.
Spherical symmetry reduces this to

\[
 S_z=\frac{4\pi}{3}\int_0^\infty r^2(p_r+2p_t)\,dr=0.
\]

Under a physical boost along z the full solution transforms, including
its phase and longitudinal profile:
\(z'=\gamma(z-vt)\), \(t'=\gamma(t-vz)\),
\(\Psi=f(\sqrt{x^2+y^2+z'^2})e^{i\Omega t'}/\sqrt2\).
Transformation of the stress tensor and the integration volume yields

\[
 E(v)=\gamma(E_{\rm flat}+v^2S_z),\qquad
 P_z(v)=\gamma v(E_{\rm flat}+S_z).
\]

Thus stress balance gives \(E=\gamma E_{\rm flat}\) and
\(P_z=\gamma vE_{\rm flat}\). Equivalently, direct translation/phase
response gives

\[
 M_{I,\rm flat}=4\pi\int_0^\infty r^2
 \left(\Omega^2 f^2+\frac{f'^2}{3}\right)dr
 =E_{\rm flat}+S_z=E_{\rm flat}.
\]

The equality follows from the field's virial balance; inertia is not
chosen as an extra parameter. The numerical W58 seed at Omega=.8 gives

\[
 E_{\rm flat}=177.268340519991,\quad
 M_{I,\rm flat}=177.268340519540,\quad
 S_z=-4.50\,10^{-10},
\]

with a relative mass difference of \(-2.54\,10^{-12}\).
The flat-space theorem is applied here only to the flat solution.
The self-gravitating calculation instead uses total ADM boundary charges.

### 3. A rest object in the same self-gravitating action

To ensure the inertia law describes an actual localized solution, solve
the coupled equations at fixed charge. Use areal radius r and

\[
 ds^2=-\sigma^2F\,dt^2+F^{-1}dr^2+r^2d\Omega_2^2,\qquad
 F=1-\frac{2\alpha m}{r},\quad \alpha=4\pi G.
\]

Here \(N=\sigma\sqrt F\) is the lapse. Define

\[
 T=\frac{\Omega^2f^2}{2\sigma^2F},\quad
 X=\frac{Ff'^2}{2},\quad
 \rho=T+X+V,\quad p_r=T+X-V,\quad p_t=T-X-V.
\]

Variation of the action gives the radial system

\[
 m'=r^2\rho,\qquad
 (\ln\sigma)'=\alpha r\left(f'^2+
            \frac{\Omega^2f^2}{\sigma^2F^2}\right),
\]
\[
 (\sigma r^2Ff')'=
 \sigma r^2\left(V_f-\frac{\Omega^2f}{\sigma^2F}\right),\qquad
 q'=\frac{\Omega r^2f^2}{\sigma F},\quad Q=4\pi q_\infty.
\]

These are also the existing W64 equations in the stated normalization.
Boundary conditions are a regular centre, exponentially decaying scalar,
sigma(infinity)=1 and fixed Q. Omega is solved, not fitted to an inertia
target. At a small epsilon the regular series uses

\[
 f=f_c+f_2r^2+\cdots,\quad
 f_2=\frac{V_f(f_c)-\Omega^2f_c/\sigma_c^2}{6},\quad
 m=\rho_c r^3/3+\cdots,\quad
 q=\Omega f_c^2r^3/(3\sigma_c)+\cdots .
\]

For the finite outer boundary the Schwarzschild-corrected scalar tail is

\[
 f\sim r^{\,s}e^{-kr},\quad
 k=\sqrt{1-\Omega^2},\quad
 s=-1+\frac{\mu(2\Omega^2-1)}{k},\quad \mu=\alpha m_\infty .
\]

Use \(f'+(k-s/R)f=0\). Domain extension and the tail amplitude control the
truncation numerically; no rigorous infinite-domain error certificate is
asserted.

The full energy, active asymptotic mass and stationary Komar mass are

\[
 E_0=M_{\rm ADM}=4\pi m_\infty
 =4\pi\int_0^\infty r^2\rho\,dr,
\]
\[
 M_{\rm K}=4\pi\int_0^\infty \sigma r^2
                 (\rho+p_r+2p_t)\,dr
 =4\pi\int_0^\infty \sigma r^2(4T-2V)\,dr.
\]

The Komar surface expression is \(4\pi\sigma(m+r^3p_r)\) at infinity.
The factor 4pi is essential: m alone is not the full ADM mass. The proper
matter integral \(4\pi\int r^2\rho/\sqrt F\,dr\) is a different quantity;
it is reported separately and never added to the ADM energy.

### 4. Inertia with the gravitational environment included

In asymptotically isotropic Cartesian coordinates the rest metric has

\[
 g_{\mu\nu}=\eta_{\mu\nu}
 +\frac{2\mu}{r}(\eta_{\mu\nu}+2U_\mu U_\nu)+O(r^{-2}),\qquad
 U_\mu=(-1,0,0,0),\quad \mu=GE_0.
\]

A boost of the complete solution gives

\[
 R_b^2=x^2+y^2+\gamma^2(z-vt)^2,\quad
 U_\mu=(-\gamma,0,0,\gamma v),\quad
 h_{\mu\nu}=\frac{2\mu}{R_b}(\eta_{\mu\nu}+2U_\mu U_\nu)
             +O(R_b^{-2}).
\]

In particular \(h_{0z}=-4\mu\gamma^2v/R_b\). Motion therefore involves
the time-space part of the metric and the changing spatial geometry,
together with the scalar field. This branch has an asymptotically
Poincare-invariant vacuum and no fixed timelike APR medium background.

Using the convention
\(K_{ij}=(\partial_i\beta_j+\partial_j\beta_i-\partial_t h_{ij})/2\)
at leading asymptotic order, \(\beta_i=h_{0i}\), compute independently

\[
 E=\frac1{16\pi G}\lim_{r\to\infty}
 \oint(\partial_jh_{ij}-\partial_ih_{jj})n_i\,dS ,
\]
\[
 P_i=\frac1{8\pi G}\lim_{r\to\infty}
 \oint(K_{ij}-K\delta_{ij})n_j\,dS .
\]

At t=0 let \(c=\cos\vartheta\) and
\(\lambda^2=1+(\gamma^2-1)c^2\). Differentiating the boosted metric gives
the contracted surface integrands

\[
 e_{\rm surf}=\frac{4\mu\gamma^2}{r^2\lambda^3},\qquad
 p_{z,\rm surf}=\frac{2\mu\gamma^2v}{r^2\lambda^3}.
\]

The angular integral is exact:

\[
 \int d\Omega_2\,\lambda^{-3}
 =2\pi\left[\frac{c}{\sqrt{1+(\gamma^2-1)c^2}}\right]_{-1}^1
 =\frac{4\pi}{\gamma}.
\]

Consequently

\[
 E(v)=\gamma E_0,\quad P_z(v)=\gamma E_0v,\quad E^2-P_z^2=E_0^2,
\]
\[
 M_I=\left.\frac{dP_z}{dv}\right|_{v=0}
     =\left.\frac{d^2E}{dv^2}\right|_{v=0}=E_0.
\]

This establishes inertia from the independently differentiated full
boundary momentum. It does not insert equality into a fitted kinetic
coefficient. Omitting the shift changes the momentum integrand; the
verifier includes that failing control explicitly. Terms beyond 1/r
do not contribute at the asymptotic surface.

### 5. Force, acceleration and the intuitive mechanism

At fixed internal charge the rest energy is a property of the localized
state. Covariance, reparametrization invariance and universal coupling to
one metric select the leading, spinless monopole action

\[
 S_{\rm body}=-M c_0^2\int d\tau_{\rm ext},\qquad M=E_0/c_0^2.
\]

Its coefficient is matched to the rest energy and the ADM momentum just
derived. There is no additional long-range scalar charge in this massive,
exponentially localized scalar branch. Curvature/finite-size couplings
belong to higher multipoles. These are the assumptions that justify
using the worldline action for an extended object.

In a flat external region,

\[
 L=-E_0\sqrt{1-v^2/c_0^2},\quad
 {\bf P}=\gamma M{\bf v},\quad E=\gamma Mc_0^2,
\]
\[
 {\bf F}=\frac{d{\bf P}}{dt}
 =M\gamma\left[{\bf a}
 +\gamma^2\frac{{\bf v}({\bf v}\cdot{\bf a})}{c_0^2}\right].
\]

Thus \(F_\parallel=\gamma^3Ma_\parallel\),
\(F_\perp=\gamma Ma_\perp\), and the slow-motion limit is
\({\bf F}=M{\bf a}\). The invariant mass M is a single quantity; the
longitudinal/transverse coefficients arise from differentiating momentum.

For the weak external metric, in c0=1 units and positive
\(u=GM_{\rm ext}/r\),

\[
 g_{00}=-(1-2u),\quad g_{ij}=(1+2u)\delta_{ij},\qquad
 L=-E_0+E_0u+\tfrac12E_0v^2+
 O(u^2,uv^2,v^4).
\]

It follows that \(M_{\rm passive}=E_0=M_I=M_{\rm active}\), and
\({\bf a}=\nabla u\) at leading order. The gradient points towards the
source under this positive-u convention.

Intuitively, the moving object is its oscillating core plus the field
configuration it carries. Uniform motion transports their combined
conserved momentum. Acceleration requires changing that momentum,
including the phase and the surrounding geometry. Internal exchanges
cancel in the total balance; a closed, uniformly moving object has no
drag term. The whole field configuration therefore participates in inertia
through its conserved momentum.

The acceleration result is a leading adiabatic monopole derivation:
body size must be small compared with the external variation scale,
and forcing must not significantly excite internal modes or radiation.
An explicit rapidly accelerated, deformed field configuration has not
been simulated. Exact uniform-boost kinematics and this leading force
law have different approximation scopes.

### 6. What changes relative to APR

The rest energy, inertia and force follow the isolated action stated above,
which uses the W54 geometric representation and W58 scalar potential.
The old APR preferred-frame scalar action is retained as a separate
historical candidate. At the same alpha and conserved charge it gave

\[
 E_{0,\rm APR}=176.7394573463,\qquad
 M_{I,\rm APR}=180.5892390013 .
\]

Its 2.178224% gap is a genuine result of that old action. The present
calculation does not algebraically cancel it by adding a fitted term.
It solves a different, already available covariant action and a new rest
state, whose \(E_0=176.770354877229\).

One universally coupled metric remains. The stronger exact ansatz
\(N=p,\ A=p^{-1}\), hence \(NA=1\), in isotropic spatial coordinates is
released. To measure this explicitly, reconstruct the isotropic radius
varrho from the areal solution:

\[
 r=A\varrho,\quad \frac{d\ln\varrho}{dr}=\frac1{r\sqrt F},\quad
 \frac{d\ln A}{dr}=\frac{1-1/\sqrt F}{r}.
\]

Use the asymptotic Schwarzschild normalization. The tested object gives

\[
 (NA)_c=0.997952570584093,\qquad 1-(NA)_c=0.002047429415907 .
\]

This 0.20474294% mismatch with exact reciprocal clock/ruler locking is
a real scope cost. It cannot be hidden by calling the lapse and spatial
coframe a single scalar. Even the exterior has
\(NA=1-[GE_0/(2\varrho)]^2\), although its first weak-potential order has
the reciprocal form. Interior relativistic stresses can affect that
product already at first order in the coupling.

The translation law is derived in the selected covariant low-energy
sector. Its physical distinction from the exact APR single-p mechanism is
part of the [foundation revision](../../Inertia/foundation_revision.md).
The APR fixed-Q restoring Hessian, finite-b rate law and exact scalar
self-regulation are not inherited. The new sector has its own equilibrium
and fixed-charge radial energy-stability test.

### 7. Numerical witness and error controls

The fixed inputs are alpha=.001 and Q=190.401136223484. The equilibrium
and boost tests use the parameters frozen before execution.

| Quantity | R=40, eps=1e-5 | R=60, eps=1e-5 | R=60, eps=5e-6 |
|---|---:|---:|---:|
| ADM energy | 176.770354873524 | 176.770354877229 | 176.770354877229 |
| Komar volume energy | 176.770354842637 | 176.770354870330 | 176.770354870330 |
| Omega | .796008838718068 | .796008838775070 | .796008838775070 |
| Centre lapse | .991825462270063 | .991825462269472 | .991825462269430 |
| Charge from quadrature | 190.401136224334 | 190.401136223408 | 190.401136223408 |
| Outer scalar amplitude | 1.25e-11 | 4.63e-17 | 4.63e-17 |

At the finest setting:

- minimum F=.993834074092495, positive lapse, node-free profile;
- maximum BVP normalized spline residual=2.98657e-8;
- boundary residual=7.41154e-22;
- volume mass=176.770354877226 and surface Komar mass=176.770354877229;
- proper matter energy=177.170069033173, kept distinct from total energy.

The mass domain/refinement change is 3.71e-9 absolute; the finest
Komar/ADM discrepancy is 6.90e-9 absolute. These are numerical consistency
and convergence estimates, not certified continuum error bounds.
The same-charge flat energy is higher by about .497985643.

The independently differentiated ADM surface expressions give:

| Speed v/c0 | Total E (c0=1) | Total P | Invariant mass |
|---|---:|---:|---:|
| .2 | 180.415487958297 | 36.083097591659 | 176.770354877229 |
| .6 | 220.962943596536 | 132.577766157921 | 176.770354877229 |
| .8 | 294.617258128714 | 235.693806502972 | 176.770354877229 |

64-point angular quadrature agrees with the analytic boost charges to
2.22e-16 relative at these speeds. This is an asymptotic charge calculation
using the solved rest mass, not a moving-grid evolution of the entire body.

69/69 checks pass: 25 symbolic identities/negative controls and 44
numerical/consistency checks. The angular Einstein and stress-conservation
residuals reconstruct derivatives using the same radial ODEs; they are
on-shell algebraic consistency checks. Independent numerical controls are
the BVP spline residual, boundary conditions, separate mass/charge
quadratures and domain/origin comparisons. Their roles are explicitly
separated in the verifier.

### 8. Reproduction, provenance and exact completion boundary

Run from the repository root:

    python -B "RefG/work 3/Lagrangian_Formulation/Oscillon_Inertia/verify_oscillon_inertia.py"

The script writes JSON to stdout and returns nonzero if a required check
fails. It produces no simulation cache. The first execution gave 69/69,
exit 0, with Python 3.10.6, NumPy 1.24.3, SciPy 1.15.2 and SymPy 1.13.3.
The checks cover the equations, stress/charge normalization, ADM boost
integrands and isotropic-radius reconstruction.

The following hashes document the original verification and subsequent
review. Report hashes are historical: editorial publication changes alter
the report, while the numerical verifier and its input equations are unchanged.
The pre-execution report SHA256 was
c6fea2c8972ce967db3350763de570efb18a3acf5ca8ad057907cacfd55d0c0d.
The initial verifier SHA256 was
c3a680999957173b903b82eb151f36c29a4401d66dea97bfe0822108b3cb9653.
After review the success status became conditional, consistency-check
labels were clarified, and the isolated-source assumptions were made
explicit. Physics, thresholds and numerical parameters were unchanged.
The final verifier SHA256 is
32cf32e9cfd590f93928eff16cbfe5494836df8b9d72bfd88b3cf3ba7da22076.
The final reviewed verifier was executed again: 69/69, exit 0, with the
same numerical values. That run's completed-report SHA256 was
6148868983fb5a845a9b0654868bdf2394dd06b8db0c2b6e22cd2d92c405dc28;
this final provenance sentence and list spacing were added afterwards.

W58 input SHA256:
b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57.
W54 reference SHA256:
ab8748d0117c8d8588fca1b54a3a5a76822ef082d58cc073e69b8cf88409c72d.
Each run prints current report/verifier/input hashes; the report hash
naturally changes when the completed derivation is added.

Final atomic status:

- same-action conserved phase charge and stress: derived;
- flat oscillon full-stress inertia: derived and numerically checked;
- self-gravitating total ADM inertia: exact asymptotic derivation;
- one same-charge weak regular equilibrium: numerical evidence;
- leading universal external force/passive mass: derived under §5's
  adiabatic monopole assumptions;
- exact APR dynamics or exact common-p inheritance: false;
- microscopic action derivation, nonlinear bound-state stability,
  high-frequency accelerated-profile response: not established here;
- strong-field and observational validation: outside this task.

This completes the explicit inertia law and weak-state witness in the
declared covariant sector. The foundation revision selects this sector
for isolated inertia and releases the old exact clock/ruler lock. The
historical APR mismatch retains its original model-specific meaning.

