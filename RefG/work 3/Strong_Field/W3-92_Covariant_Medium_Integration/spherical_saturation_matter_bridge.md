# Saturating spherical gravity coupled to conserved matter

**შედეგი მოკლედ:** მიღებულია პოსტულატურ გაჯერების კანონზე დაფუძნებული
სფეროსიმეტრიული მოდელი, რომელშიც მატერიის შეკუმშვა და გარე ველი ერთი
მოქმედებით ითვლება, ხოლო სიმრუდე სასრული რჩება. ეს უკვე წყაროს მქონე
დინამიკური ამონახსნია. სრული RefG-მიერთება ჯერ ვერ ჩაითვლება მიღწეულად:
წნევა–ოსცილონის მასშტაბური კანონი ამ მოქმედებიდან გამოსაყვანია, ზუსტად
ერთი სტატიკური საათი–სახაზავის ფაქტორი კი არჩეულ გეომეტრიასთან ვერ თავსდება.

## Decision — 2026-09-11

The existing inverse Hayward candidate is developed into a **sourced,
time-dependent spherical effective theory**. Its gravitational response and
ordinary material source are varied together. The finite response is an explicit
new constitutive postulate, not a result inherited from the old canonical
Einstein–scalar evolutions or from the separate five-field medium.

This package tests an actual collapsing conserved-current source and its
exterior, rather than assigning an interior stress after choosing a metric.
The author's speculative node-resolution directory is outside this work.

### Frozen contract

- CLAIM_ID / MODEL_VERSION: W92_SPHERICAL_SATURATION_MATTER_V1.
- CLAIM / TYPE: The stated two-dimensional covariant spherical action admits
  a flat homogeneous dust interior joined without a spherical thin shell to
  the previously selected Hayward exterior. Its curvature remains bounded
  as the material surface contracts toward zero at infinite comoving proper
  time. Type: conditional effective-action construction, exact identities
  and numerical crosschecks.
- AUTHORITY: The author authorized choosing a singularity-removal mechanism
  and connecting it to RefG, including explicitly identified postulates.
  No change to the published monographs or earlier source solvers is made.
- ASSUMPTIONS / FREEDOM: One physical metric, spherical symmetry, conserved
  timelike dust current, zero material pressure, marginally bound flat
  interior, and the universal response length ell>0. The rational
  characteristic h(z)=z/(1-ell²z) is selected from the existing inverse
  candidate. M>0 labels a material cloud, not an action coefficient.
  Dust is a declared macroscopic source sector; no derivation of dust from
  the full interacting oscillon spectrum is assumed.
- CONVENTIONS / DOMAIN: Signature (-+++), G=c=1 unless G is displayed.
  R is areal radius, gamma_ab the Lorentzian orbit-space metric,
  X=(grad R)², z=(1-X)/R², 0<ell²z<1 for the action as written.
  Spherical field equations also have the z=0 limiting branch.
  Centre values use regular limits.
  The contracting interior covers finite proper times and a finite
  comoving ball; exterior regions use horizon-regular coordinates.
- DEPENDENCIES: Existing inverse_saturation_candidate.md; W3-85's action
  normalization; RefG's minimally coupled material and conserved-current
  sectors. Borrowed mathematical input: [1], equations 1–9, 46, 156–161.
  Previous numerical PASS results are not inherited by the new action.
- METHOD / PASS: Derive action coefficients before solving; verify all
  orbit-space and angular equations, current conservation, mass balance,
  boundary geometry and curvature limits. Independent quadrature and an
  ODE integrator must reproduce the analytic boundary trajectory.
- FAIL / FALSIFIER: A nonzero equation or junction residual rejects its
  claimed solution; finite-radius poles reject that branch. Exact universal
  static clock/rod equality is separately tested against the candidate,
  not silently assumed. A failed numerical solver is inconclusive.
- RESIDUAL / ERROR: Exact symbolic zeros; quadrature tolerance 1e-35 at
  50 digits; independent double-precision time-evolution relative error
  <2e-8, with tighter-tolerance convergence and a fixed 12-unit interval.
  These are numerical checks, not observational error bars.
- HEALTH / BRANCHES: Positive h' ensures a unique algebraic response and
  positive screened radial null coupling. This is not a proof of generic
  perturbative stability. Horizonless, extremal and two-horizon exteriors
  retain their existing classification.
- OBSERVABLE_MAP: Local proper time, areal surface radius, quasilocal
  geometric mass, conserved asymptotic mass, null expansions and curvature.
  Material density, foundation pressure P_F, geometric response fraction q,
  clock lapse and ruler factor remain explicitly distinguished.
- DATA_ROLE / FORWARD_MODEL / IDENTIFIABILITY: No data, fitting, detector
  pipeline or uniqueness claim. Known literature geometry motivated the
  postulate. Observation and microscopic inference are N/A to this test.
- BENCHMARK / CROSSCHECK: Einstein limit, old vacuum candidate, symbolic
  verification of the published action-to-equation differentiation map,
  independent metric connection, source checks and ODE/quadrature.
  Common premises of the independent routes are the stated action and dust.
- PROVENANCE / FILES: This report and verify_spherical_saturation_bridge.py,
  plus one short index in medium_health_horizon_diagnostic.md. No copied
  third-party article, generated output, publication, or git operation.
- CLOSURE_FLAGS: Compute spherical_action, sourced_equations, dust_solution,
  junction, bounded_curvature, trajectory_crosschecks from their tests.
  full_RefG_pressure_join, universal_common_p, global_completeness,
  generic_stability, oscillon_formation and observational_pass stay false.
- STOP: End after this sourced construction and the compatibility decision.
  Do not substitute an unrestricted new scalar-polynomial search or a
  long collapse run for the remaining physical pressure/action conditions.

## 1. One response action, one material ledger

Write ds²=gamma_ab dy^a dy^b+R²dOmega². A precise spherical action is

    S_g = (1/4G) integral sqrt(-gamma) [
      h2 - h3 Box R + h4 R2
      - 2 h4_X ((Box R)² - R_;ab R^;ab)] d²y,

where R2 is the orbit-space Ricci scalar. Define h2=R² H2(z),
h3=R H3(z), h4=R² H4(z), with

    H2 = 2z(1-3ell²z)/(1-ell²z)²,
    H3 = 4/(1-ell²z)²,
    H4 = 1-ell²z/(1-ell²z)
         +2ell²z log[(1-ell²z)/(ell²z)].

These are the published Hayward functions [1]. The constant inside the log
makes its argument dimensionless; its change contributes a topological
term to the spherical equations. H4 has a finite z->0+ value, while H4'
diverges logarithmically. The simplified spherical equations have continuous
Einstein/vacuum limits there. A smooth generic off-shell action through
z=0 or into negative z is not established. Finite-time dust states and
finite-radius vacuum states tested here have z>0.

Add the physical material action S_m[g,J,theta] once. For this demonstration
its local energy is m0 n with conserved current, so T_mu_nu=rho U_mu U_nu
and P=0. This uses a continuum current rather than particle or molecular
structure calculations.

The spherical equations are

    E_ab = beta R_;ab - (alpha/2+beta Box R) gamma_ab
         = 8piG R² T_ab,
    alpha = 2R² z(1-3ell²z)/(1-ell²z)²,
    beta  = -2R/(1-ell²z)²,
    F = partial_X alpha - partial_R beta = 0.

The angular equation follows from the same action and its Bianchi identity;
it is independently evaluated in the verifier. Partial_R here holds X fixed.

For the generalized mass and the ordinary geometric mass,

    mu = R³ h(z)/2,       h(z)=z/(1-ell²z),
    m_geo = R³ z/2,
    grad_a mu = 4piG R² (T_ab grad^b R - T^(2) grad_a R).

Thus matter changes the gravitational constraint directly. This is the
equation missing from a mass-only or externally imposed source prescription.
For radial null vectors the same equations give

    R_mu_nu k^mu k^nu = 8piG (1-ell²z)² T_mu_nu k^mu k^nu.

The response to the material null source decreases by q², where q=1-ell²z.
It comes from variation of the postulated action. In an alternative Einstein
ledger, the correction can be written as an effective medium tensor.
Counting that tensor again as extra matter in the modified equation would
double count the response.

In static matter configurations the corresponding constraints are

    mu' = 4piG R² rho,
    (log N)' = 4piG R(rho+P_r)/(f h'(z)),

for ds²=-N² f dt²+dR²/f+R²dOmega². N and f are retained until variation.
These equations permit specified ordinary RefG sources; they do not force
a nonzero canonical oscillon into the old vacuum N=1 solution.

## 2. A source-driven contraction, not a prescribed infall curve

Choose the flat homogeneous interior

    ds²=-dτ²+a(τ)²[dχ²+χ²dOmega²],    Hc=a_dot/a.

The action equations, including the angular equation, reduce to

    h(Hc²)=8piG rho/3,
    Hc_dot=-4piG(rho+P)/h'(Hc²),
    rho_dot+3Hc(rho+P)=0.

For dust, rho a³ is constant. On the contracting branch,

    z=Hc²=(8piG rho/3)/(1+8piG ell²rho/3),
    Hc=-sqrt(z),
    Hc_dot=-(3/2)z(1-ell²z).

A comoving surface R=a χ_b has constant material mass
M=4pi rho R³/3 and obeys

    R_dot = -R sqrt[2GM/(R³+2GM ell²)].

This matches the old E=1 curve, now derived for a material boundary from
the sourced field equations. M is also the exterior ADM mass in this
marginal, non-radiating dust example. This example therefore does not
compute an assembly mass defect.

The geometric mass enclosed at that moving surface is

    m_geo/G = M R³/(R³+2GM ell²).

It decreases during contraction while the conserved material/ADM M stays
fixed. Local material density, geometric enclosed mass and ADM mass are
different ledger entries with the relation derived above.

At fixed R the response to increasing M has positive diminishing increments.
At small R the contraction is R_dot~ -R/ell; the surface remains positive
at every finite comoving proper time. Its limiting contraction is
exponential, with no bounce in this dust branch.

## 3. Boundary, horizons and curvature

The same action's exterior has mu=GM and

    f(R)=1-2GM R²/(R³+2GM ell²).

For the comoving boundary, both sides give induced metric
-dτ²+R²dOmega², K_ττ=0 and K_theta_theta=R.
Indeed f+R_dot²=1 and R_ddot=-f'/2. The advanced exterior time obeys
v_dot=1/(1-R_dot), which stays finite at either simple horizon.
The generalized mass and z are continuous. A piecewise C1 matching
has no distributional shell in the stated second-order spherical equations.
This assertion concerns this reduced action, not an unspecified nonspherical
higher-derivative completion.

For GM>3sqrt(3)ell/4 the surface crosses the outer and inner marginal radii;
in the interval between them its outgoing null expansion is negative.
Horizon crossing happens at finite surface proper time.

In the interior,

    Ricci = 3z(1+3ell²z),
    Kretschmann = 3z²[(3ell²z-1)²+4].

For 0<=ell²z<1 these obey 0<=Ricci<=12/ell² and
0<=Kretschmann<=24/ell⁴. The equality limits occur as τ tends to infinity.
The exterior curvature and freely falling tidal checks are retained from
the independently rerun inverse-candidate verifier.

## 4. Actual RefG compatibility decision

The construction joins a **new spherical gravitational response** to a
conserved macroscopic material sector using one action and one metric.
It preserves the spherical Einstein limit at ell²z<<1, local metric light
speed, current conservation, and the joint solution of matter and geometry.

There are three exact boundaries to calling it a completed RefG black hole:

1. Foundation pressure P_F and the operational oscillator scales have not
   been derived from h(z). A local state and its several readouts can be
   coupled without being independently varied; the required constitutive
   map must still be specified. Here q is the collective response fraction.
   It cannot be renamed p: at the vacuum centre q tends to zero whereas
   the static lapse sqrt(f) tends to one.
2. The strictly static, isotropic common-p ansatz has
   R=s/p(s) and (grad R)²=(1-s p'/p)²>=0. Combining it with the selected
   reciprocal-areal metric requires p=s/(s+C) on the outward branch,
   producing f=(1-C/R)², not Hayward. Therefore exact universal static
   clock/rod equality is **incompatible with this chosen target**.
   W3-71 and the full coframe already distinguish component readouts.
   Extending the weak common-p rule needs an explicit physical decision;
   this report makes no silent change to it.
3. The non-bouncing dust density grows without bound at infinite proper
   time. Bounded curvature does not prove global geodesic completeness.
   Radial null convergence remains nonnegative, and the inner Cauchy
   horizon/global-extension conditions remain essential. For an infinite
   FLRW patch the future null-affine integral is finite; null rays in a
   finite dust ball leave that interior, so that integral alone does not
   decide completeness of the matched spacetime.

The four-dimensional non-polynomial lifting in [1] is nonunique and may
have generic-background pathologies. Its invariant-ratio formula also
requires domain/continuation control on algebraically special metrics.
Only the directly defined spherical action is used here. Its coefficients
grow as ell²z approaches one. No generic hyperbolicity, radiative stability,
or all-sector CMB/PPN/quantum inheritance is claimed.

The selected route is therefore a **conditional sourced regular-curvature
candidate**, with a genuine dynamical improvement over the vacuum target.
A completed pressure–oscillon theory and a globally nonsingular, stable
black hole remain unestablished.

## 5. Alternative rejected at its first decisive test

A minimal magnetic nonlinear-electrodynamic realization can reproduce the
same background using L(F)=rho_* x²/(1+x)²,
x=(F/F0)^(3/4), F=Q²/(2R⁴), rho_*=3/(8pi ell²).
Its extraordinary mode has

    c_mode²=(L_F+2F L_FF)/L_F=(4-5x)/[2(1+x)].

It is negative at x>4/5. This reconstruction is rejected as a globally
healthy material completion before undertaking any evolution. It also adds
a flux sector and a mass/flux relation, neither supplied by RefG here.
The ordinary light cone is not altered by inserting this rejected model.
The code verifies this test directly from L(F), not from a claimed speed.

## 6. Stationary oscillon source in the existing saturation action

### Frozen bounded construction

CLAIM_ID: W92_SATURATION_CANONICAL_OSCILLON_V1. The next test replaces the
demonstration dust source by the retained W58/W64 canonical complex scalar,
while keeping this report's already-postulated spherical gravitational
action unchanged. It seeks a regular horizonless stationary solution at
fixed scalar charge and its Einstein limit. It does not evolve collapse.

This is an explicitly different branch from the five-field EH medium.
The latter's Q Fbar+W-V source identity is not imposed on a different
gravitational action. Its regular comoving algebraic-response limitations
motivate this choice; no coefficient search in that excluded class is made.
The W64/W65 scalar potential, normalization and minimally coupled field
equation are retained. No molecular structure or new matter interaction
is introduced.

Freedoms and domain: dimensionless alpha=0.04,
V(chi)=chi^2/2-chi^4/4+chi^6/24, fixed positive scalar charge
Q_dim=8.588382857985234 (the existing fine W65 reference), and the
already-postulated universal response length ell. Continue through
ell=0,0.5,1,2 with positive lapse and radial metric coefficient.
This is a comparison of theories at fixed charge, not changing ell
during one object's evolution or an assembly mass-defect experiment.

Checks and stopping rule: derive radial constraints and scalar equation
from the stated action, check the radius/angular equation independently,
and solve the fixed-charge boundary problem on EPS=1e-5<=r<=80 with
tolerance 1e-7. Repeat the final accepted branch at tolerance 1e-8 and
outer radius 100. Independent source/metric and matter-conservation
relative residuals must be below 100 times the validation tolerance away from
the coordinate centre; charge and mass integrals use two quadrature
grids. Report finite-domain/tolerance changes separately. Failure of a
solver is inconclusive, not a physical no-go; no numerically unresolved
sample is accepted as a solution. Stop after a reproducible source
solution or the first unresolved continuation boundary.

Status boundary: finite stationary curvature, h'>0, conserved scalar
charge and the Einstein limit are separate checks. Full perturbative
stability, pressure/clock/rod identification, actual horizon formation,
singularity removal and observations remain unproved by this test.
There are no observational data or fit parameters. The source equations
and existing solver pins supply provenance; an independent agent checks
the equations. Only this report, its verifier and the W92 index change.

### Same scalar, independently solved saturated geometry

Use ds^2=-sigma(r)^2 B(r) dt^2+dr^2/B(r)+r^2 dOmega^2 and
psi=chi(r) exp(i Omega t), with a positive conserved scalar charge.
The W64 dimensionless units suppress the common 4pi normalization;
alpha=4pi G m_s^2/lambda, ell=m_s ell_physical. Write

```text
z=2alpha M/(r^3+2alpha ell^2 M), q=1-ell^2 z, B=1-r^2 z,
W=Omega^2 chi^2/(sigma^2 B), X=B chi'^2,
rho=(W+X)/2+V, p_r=(W+X)/2-V, p_t=(W-X)/2-V.
```

The existing spherical action supplies, before solving,

```text
M'=r^2 rho,
(ln sigma)'=alpha r q^2 (rho+p_r)/B,
B'=r z(1-3ell^2 z)-2alpha r q^2 rho,
(sigma B r^2 chi')'=sigma r^2[V_chi-Omega^2 chi/(sigma^2 B)],
Q_dim'=r^2 Omega chi^2/(sigma B).
```

The boundary conditions fix regularity, sigma(R)=1, the existing
Schwarzschild-corrected decaying scalar tail and total Q_dim. Central
amplitude and Omega are solved, not held fixed as ell changes. Each
trial updates the full matter source and geometry. At ell=0 these
equations and the numerical solution recover the retained Einstein--scalar
reference. The scalar charge is not identified with a count of oscillons.

The independent orbit and angular equations are evaluated from the same
action. In particular, with L=ln sigma,

```text
R2=-B''-3B'L'-2B(L''+L'^2), Box r=B'+BL',
Hess(r)^2=(B'/2+BL')^2+(B'/2)^2,
E_r=-beta R2+alpha_orbit,R+2 beta_,R Box r
    +2 beta_,X[(Box r)^2-Hess(r)^2],
-E_r/(4r)=2alpha p_t.
```

The partial derivatives here hold X=(grad r)^2 fixed as required by the
action. The test uses derivatives of the solution spline rather than
substituting the solved RHS into its own validation. An independent
symbolic Bianchi check relates its residual to alpha r times the scalar
stress-conservation residual once the two metric equations hold.

In this modified action M is the generalized mass, with its asymptotic
value read as ADM mass. The ordinary geometric enclosed mass is Mq.
The old EH Komar integral of ordinary matter alone is not its mass law;
its effective gravitational correction would otherwise be omitted.
Neither the five-field H variable nor a renamed q is introduced into
the matter action as an additional mass multiplier.

### Actual source results at fixed charge

The validated continuation is a sequence of horizonless stationary
oscillon configurations. All have Q_dim=8.588382857985234.

| ell | ADM mass | Central clock lapse | Central q | Central Kretschmann |
|---|---:|---:|---:|---:|
| 0 | 7.968956979 | 0.754692095 | 1 | 0.101434389 |
| 0.5 | 7.973839522 | 0.759773156 | 0.986791320 | 0.093122774 |
| 1 | 7.987741913 | 0.773538020 | 0.950784128 | 0.073722370 |
| 2 | 8.034881445 | 0.814164576 | 0.841336381 | 0.036172901 |

The central metric response is genuine: the nonzero scalar gives
(ln sigma)'>0 and hence sigma_c<1 with asymptotic time normalized.
It differs from the old vacuum centre with sigma=1. The geometric
curvature is reduced along this fixed-charge comparison, and the
minimum B remains positive (about 0.844 for ell=2).

ADM mass INCREASES as ell increases in this comparison: weaker binding
raises it from 7.968956979 to 8.034881445. This is not a mass-addition
experiment, a time history of one object, or proof of the proposed
individual-oscillon mass/readout law. The clock lapse and q are separately
computed quantities; they have not been identified as the same p.

### Central curvature bound and numerical control

Regular centre data give

```text
rho_c=W_c/2+V_c, z_c=2alpha rho_c/(3+2alpha ell^2 rho_c),
q_c=1-ell^2 z_c,
N_lapse=N_c(1+n_2 r^2+...),
n_2=alpha q_c^2 W_c/2-z_c/2,
K_c=12 z_c^2+48 n_2^2.
```

Because V=chi^2[(chi^2-3)^2+3]/24>=0, for ell>0 define
u=ell^2 z_c in [0,1) and w=W_c/(2rho_c) in [0,1]. Then

```text
K_c ell^4=12u^2{1+[3w(1-u)-1]^2} <= 24.
```

The expression is convex in w. At w=0 it is 24u^2; at w=1 its
u derivative is 24u[18(u-1/2)^2+1/2]>0 and its endpoint value is 24.
The zero-density case follows by continuity. The verifier checks the
independent sectional-curvature formula and these polynomial identities.
This is a central bound for this regular static sector, not a global
bound for arbitrary inhomogeneous collapse.

The first run passed 55/61 checks: all six independent angular tests
failed their numerical accuracy threshold, including the Einstein
reference. Dense central sampling improved them but did not suffice.
The spline second derivatives require more accuracy than the first-order
collocation residual. The solver tolerance was therefore reduced to
1e-9/1e-10 while retaining the original validation tolerances 1e-7/1e-8
and angular acceptance bounds 1e-5/1e-6. No equation or acceptance
threshold was changed to obtain a passing solution.

The final solver uses 1201 initial points on [EPS,2] and 801 on [2,R],
followed by adaptive collocation. At ell=2, R=80 and 100, the fine angular
relative residuals are 4.39e-7 and 4.32e-7; first-order residuals are
about 1.1e-10. Angular/source checks cover 0.03<=r<=R-1, with separate
regular-centre expansion and boundary conditions. Mass and charge
integral errors are below 4.4e-13 for the first four runs and 2.5e-14
for the fine runs, using 16001/32001-point quadratures. These small
integral differences do not supersede the larger local curvature error.
Neither finite radius nor these numerical controls certify the infinite
domain. The scalar tail and O(EPS^3) central source remainder are retained
in the interpretation rather than declared exactly zero.

Outcome: 63/63 checks, CONDITIONAL_STATIONARY_OSCILLON_COUPLED. The
existing saturation mechanism now has a nonzero canonical oscillon
source solution, not only dust or an imposed vacuum profile. A full
foundation-pressure/readout match, perturbative stability and a
singularity-free black hole remain separate. Run
`python -B verify_spherical_saturation_bridge.py --oscillon-source`;
stdout contains cases, residuals and code/source hashes. The original
default dust/action checks remain a separate regression.

## 7. Bounded dynamical response of the coupled oscillon

### Frozen scope, 2026-09-12

CLAIM_ID: W92_SATURATION_OSCILLON_DYNAMICS_V1. Keep the existing spherical
saturation action, ell=2, alpha=0.04, canonical sextic matter and the
freshly solved fixed-charge stationary reference of section 6. The task
is a finite-time response to a small inward energy-flux perturbation,
with an unperturbed reference and a sign-reversed control. No constitutive
coefficient or official pressure/readout law is changed.

Use the polar-areal chart only while B>0. This is sufficient for this
small perturbation of the B_min~0.844 reference; stop with unresolved
continuation if the chart/domain or constraint iteration fails. Horizon
crossing and a singularity-free endpoint are not tests in this stage.

Prepare psi=f real and Pi=i Omega f/(sigma B)+epsilon r f', with
epsilon=0,+0.01,-0.01. The positive sign gives inward energy transport
where f'!=0 and preserves the initial scalar charge pointwise. It is not
an imposed charge-current velocity: the initial charge flux remains zero.
Both signs add the same quadratic kinetic energy. Recompute the nonlinear
mass constraint and lapse before evolution, and at every RK4 substage.

Registered numerical suite: T=32, R=40, spacings 0.1,0.05,0.025, common
sample interval 0.5 and Courant parameter 0.2. Use an unperturbed reference
at every spacing, both perturbation signs at every spacing, a fine-grid
half-step control and an R=50 control. A coarse T=8 pilot may debug the
implementation; it cannot establish the final outcome. Zero boundary
scalar flux is tested by the larger domain.

Required accuracy: finite states and B,sigma>0 at every evaluated stage;
mass-constraint fixed-point relative defect below 2e-13; relative charge
drift <1e-5 and mass drift <5e-3. Independent local mass-flux and radial
constraint residuals on the fine grid must be <5e-3 and decrease under
refinement (fine/middle<0.6 unless already <1e-6). Waveform differences
must decrease (ratio<0.6) or be <1e-4. Half-step and domain differences
must be <1e-3. Hamiltonian-directional and Einstein-limit checks precede
the accepted dynamics.

An observed contraction/recovery is reported only if it exceeds three
times the reference drift and resolution error. Recovery, damping or
stability are not forced into a numerical PASS condition. The result may
be an oscillatory finite-window response, continued contraction, or an
unresolved change. Generic stability, physical damping, long-time
collapse, full RefG pressure matching and observations remain outside
this test. Allowed files: this report, its existing verifier and the W92
index. No new source model, generated result file or publication edit.

### Equations and independent energy check

In this subsection B is the radial metric coefficient, not the lapse:

    ds^2 = -sigma^2 B dt^2 + dr^2/B + r^2 dOmega^2,
    Pi = psi_t/(sigma B), D = psi_r, S = |Pi|^2+|D|^2,
    V = |psi|^2/2-|psi|^4/4+|psi|^6/24,
    F = (1-|psi|^2+|psi|^4/4) psi,
    q = r^3/(r^3+2 alpha ell^2 M), B = 1-2 alpha M q/r.

The same sourced spherical action gives

    M_r = r^2 (B S/2+V),
    (log sigma)_r = alpha r q^2 S,
    psi_t = sigma B Pi,
    Pi_t = r^-2 (r^2 sigma B D)_r - sigma F.

Its off-diagonal orbit equation, rather than an imported Einstein
constraint, fixes the energy flux:

    E_tr = -r B_t/(B q^2) = 2 alpha r^2 sigma B Re(conj(Pi)D),
    M_t = r^2 sigma B^2 Re(conj(Pi)D),
    B_t = -(2 alpha/r) q^2 M_t.

There is NO additional q^2 in M_t. The scalar equations independently
give, with j=Re(conj(Pi)D),

    r^2 rho_t - (r^2 sigma B^2 j)_r
      = r^2 (B_t S/2 + B^2 sigma_r j) = 0.

Thus the radial constraint is propagated. The phase charge satisfies
Q_t=[r^2 sigma B Im(conj(psi)D)] at the boundaries. It is an internal
scalar charge, not an asserted count of electrons or all matter species.

The nonlinear ADM functional provides a second check. At fixed r,

    delta M_r + alpha r q^2 S delta M
      = r^2 [B Re(conj(Pi)delta Pi+conj(D)delta D)
             + Re(conj(F)delta psi)].

The integrating factor of this VARIATION is sigma, normalized to one
at the outer boundary. Consequently

    delta M_R = integral_0^R sigma r^2
        [B Re(conj(Pi)delta Pi+conj(D)delta D)
         + Re(conj(F)delta psi)] dr.

With canonical momenta r^2 Pi and the retained boundary work, this
generates the two matter evolution equations. The numerical directional
test uses compactly supported variations, so their boundary work is zero.

### Discretization and measurement definitions

The original `nonlinear_equilibrium_evolution.py` is imported unchanged
for its cell-centred finite-volume scalar flux, RK4-compatible RHS,
gradient, quadrature and charge-weighted diagnostics. Its GR geometry
reconstruction is NOT reused unchanged. The subclass in the existing
verifier solves the nonlinear mass equation at every RK substage:

    M_r + alpha r S q(M) M = r^2 (S/2+V).

Freezing q only within each fixed-point iteration gives a linear
integrating-factor solve; iteration then updates q(M). This finite
reconstruction uses q, whereas the physical lapse and the functional
variation use q^2. They must not be identified. In the ell=0 limit the
new geometry reconstruction is tested against the original solver.

The reported charge radii are RMS radii, weighted by
Im(conj(psi)Pi) r^2 dr. One uses areal r; the other uses the slice's
proper radial length integral dr/sqrt(B). Neither is a sharp surface or
a direct particle-size measurement. Central amplitude and sigma(0)
measure the field magnitude and the central clock rate relative to the
chosen outer time normalization.

Mass flux is checked by a directional finite difference of the
independently reconstructed mass along the actual numerical RHS.
Radial constraints use a fourth-order derivative different from the
reconstruction quadrature. These local diagnostics cover r<=15; radial
derivative diagnostics additionally omit the first two cells. Centre
regularity is built into the field boundary condition and reconstruction,
not independently certified by that excised derivative norm. Global
charge and outer-mass budgets and positivity tests use the full domain.

### Finite-window result

The prescribed suite contains nine T=32 runs (three spacings, each with
epsilon=0,+0.01,-0.01), plus the half-step and larger-domain inward-kick
controls. No restoring term, friction, mass subtraction or manually
specified turnaround is introduced. The scalar and geometry jointly
evolve under the equations above.

For a reported quantity X, the response is

    Delta_X(t) = [X_kick(t)-X_kick(0)]/X_kick(0)
                 -[X_zero(t)-X_zero(0)]/X_zero(0).

The resolution estimate compares this SAME subtracted response on the
middle and fine grids. The acceptance margin is three times the largest
of this estimate, the fine reference drift and the available inward-kick
time-step/domain differences. The physical interpretation concerns that
inward case; the sign-reversed run additionally tests response direction.
Recovery past the initial radius requires a resolved negative minimum
followed by at least three stored samples above the positive margin.
This is a finite-window return, not asymptotic relaxation.

The fine inward run gives the following extrema of Delta_X. Percentages
are relative changes, not absolute measurement errors. Times are model
coordinate time in the stated outer normalization, not seconds.

| Quantity | Minimum response | Time | Maximum response | Time |
|---|---:|---:|---:|---:|
| Charge-weighted areal RMS radius | -0.477827% | 3.0 | +0.373377% | 18.5 |
| Charge-weighted proper RMS radius | -0.467607% | 3.0 | +0.385188% | 18.5 |
| Central field amplitude | -0.792959% | 9.5 | +0.971679% | 3.0 |
| Central clock coefficient sigma(0) | -0.168609% | 1.0 | +0.110672% | 16.0 |

Thus small inward energy transport produces resolved contraction,
followed by re-expansion past the initial radius, with an oscillatory
field/clock response. The sign-reversed run first expands instead.
The central amplitude's decrease is not called a contraction: the radius
diagnostic, not the sign of every observable, establishes contraction.
At T=32 the inward areal-radius response is approximately -0.00150%,
but closeness to its initial value at one time is not proof of settling.

On the fine inward run, the maximum fractional charge drift is 2.78e-13
and outer-mass drift is 5.24e-7. The minimum B over all RHS stages is
0.843057 and the minimum sigma is 0.812741. The maximum local mass-flux,
radial mass and radial lapse residuals are respectively 9.48e-6,
6.83e-5 and 5.04e-5 on their declared diagnostic domain; their
middle-to-fine ratios are approximately 0.25. These are numerical
accuracy checks, not independent experimental confirmations.

The kick preserves initial charge but adds energy: on the fine grid
M_zero(0)=8.0347934404 and M_kick(0)=8.0361134649. Both kick signs have
the latter mass. Discrete initial Q=8.5886447679 differs from the
continuum BVP target 8.5883828580 by about 3.05e-5 fractionally; this
projection error decreases with grid refinement and is not represented
by the much smaller temporal conservation error. The unperturbed
fine-grid mass similarly differs from the BVP value by about 1.10e-5
fractionally. Tiny charge drift does not imply that overall accuracy.

The directional Hamiltonian error decreases from 3.59e-4 at h=0.1 to
5.39e-6 at h=0.0125. Scalar waveform and metric constraint errors decrease
under refinement; half-step and domain controls do not set the observed
response. Signed charge-density fluctuations are allowed by the canonical
complex field; the measured RMS radii are not radii of a strictly positive
particle-number distribution.

The final resolved-response margins are 0.01471% for the areal radius
and 0.01490% for the proper radius, both dominated by the unperturbed
reference drift. They are well below the measured contraction and later
expansion. Across all four observables, the maximum pointwise difference
of normalized changes is 2.67e-9 for the half-step control and 2.16e-13
for the R=50 control. Both radius returns satisfy the stated time-order
and three-sample requirement in the final independent rerun.

The coarse T=8 debugging pilot passed 29 checks. The initial full version
passed 81; read-only review then tightened the *reporting/validation*
layer to include the areal-radius waveform controls, compare the same
reference-subtracted observable across grids, and require time-ordered
return. An independent symbolic expansion of the scalar energy balance
was also added. The evolution equations, data, domain, time window,
perturbation and registered accuracy thresholds were not changed.

The final implementation passed 85/85 checks, independently rerun with
exit status zero and decision BOUNDED_DYNAMICAL_RESPONSE_COMPUTED. Its
default action/dust regression passed 74/74, and its stationary source
prerequisite passed 63/63. Implementation SHA-256:
`2053a308398d7dde8703b2bfcdc34a4bcdf285a7bcf7ab41945a2fbae13e4473`.
The unchanged reused evolution engine SHA-256 is
`2c310a3a600b2ced39333c14a208a2fcb97ed6178c6906e0a55366e35ab1e4ca`.
The fixed-point defect stayed below 5e-15; this measures convergence of
the discrete nonlinear solve, not the independent continuum residuals
listed above. Both monographs, CODES.md, .gitignore and the private
assumption folder remain unchanged.

This stage supplies a time-dependent sourced test of the existing
saturation postulate. It does not derive that postulate from the complete
RefG foundation-pressure action, identify q with physical pressure, prove
generic stability, establish damping or resolve a black-hole singularity.
The observed small-amplitude return must not be extrapolated to the
previous large-compression Einstein--scalar runs, which use a different
gravitational action.

This is a compatibility test, not a demonstration that small-amplitude
restoration uniquely distinguishes saturation from Einstein--scalar
gravity. There is an additional concrete scale restriction: section 3's
vacuum threshold, expressed in the present source normalization, is

    M_critical = 3 sqrt(3) ell/(4 alpha) = 64.95190528.

The tested M~8.036 is well below it. If the enclosed generalized mass is
nonnegative and bounded by this outer mass, then

    1-B <= (4 alpha M_outer/ell)^(2/3)/3 ~ 0.248296.

Hence absence of B=0 in this small-mass test is expected; it is not a
demonstration of singularity removal in a black hole. A later
black-hole-forming source test must first meet the appropriate mass and
trapping conditions within this SAME action and use a chart that can
cross B=0. Merely extending the present small-mass run is not that test.

Reproduce without output files:

    python -B verify_spherical_saturation_bridge.py --oscillon-dynamics

The optional `--dynamics-pilot` is explicitly PILOT_ONLY. Full stdout
contains all eleven trajectories, constraint diagnostics, refinements,
source/engine hashes and the implementation hash. It does not silently
discard failed cases.

## Reproduction and attribution

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py"
    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_inverse_saturation_candidate.py"

Results and numerical examples are emitted to stdout; no generated files.

The final run passed 74/74 assumption-scoped checks. Independent read-only
reruns confirmed the initial check suite; the old vacuum verifier also
passed its unchanged 84/84 checks.
The final verifier also checks the zero-curvature action boundary, both
interior extrinsic-curvature components and the ingoing-chart acceleration.
The independent ODE runs on 0<=tau<=12 gave maximum relative radius errors
1.39e-8 and 2.41e-11 at tolerances 1e-8 and 1e-11. These bounded checks
are supplemented by the exact logarithmic endpoint limit.

For the dimensionless illustration G=ell=1, M=2 and initial R=8:

| Surface event | R | Elapsed proper time | Enclosed geometric mass | ADM mass |
|---|---:|---:|---:|---:|
| Outer horizon | 3.70927536 | 5.22446273 | 1.85463768 | 2 |
| Inner horizon | 1.19393657 | 7.52571151 | 0.59696828 | 2 |
| Later finite radius | 0.05 | 10.76628533 | 0.0000624980 | 2 |

The last state's interior density is 3819.7186 and its Kretschmann scalar
23.9973752 in these model units. The contrast makes the distinction between
bounded geometric response and a bounded material density explicit.

[1] J. Borissova and R. Carballo-Rubio, *Regular black holes from pure gravity
in four dimensions*, Phys. Rev. D 113, 124004 (2026),
[primary text](https://arxiv.org/html/2602.16773v2).
The spherical action and known Hayward choice are credited to this source.
The source-coupling, dust-boundary and compatibility calculations here are
explicit reproductions/extensions for the RefG research decision, not a
claim that the underlying regular metric was newly discovered.

[2] S. A. Hayward, Phys. Rev. Lett. 96, 031103 (2006),
[primary text](https://arxiv.org/abs/gr-qc/0506126).
