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

## 8. Supercritical inward source data

### Frozen construction, 2026-09-12

- CLAIM_ID / MODEL_VERSION: W92_SATURATION_SUPERCRITICAL_DATA_V1;
  same spherical saturation and canonical sextic action as sections 6--7,
  alpha=0.04, ell=2. CLAIM / TYPE: construct regular, initially untrapped,
  inward charged-scalar Cauchy data with M_outer=2 M_critical. Conditional
  source construction with exact identities and numerical evidence.
- GOAL / STOP: remove the subcritical-mass obstruction of section 7.
  Stop at a validated initial slice, or record its failed accuracy/existence
  test. A separate evolution must determine trapping and the endpoint.
- ASSUMPTIONS / DOMAIN / CONVENTIONS: polar-areal B>0, same time and scalar
  conventions as section 7; r in [0,60], comparison domain [0,80]. A smooth
  packet is supported on 20<r<40. Its cavity uses the already-declared
  z=0 spherical-equation limit. Generic off-shell action regularity at z=0
  is outside this construction.
- FREEDOM_LEDGER: x=(r-30)/10; b=exp(1-1/(1-x^2)) for |x|<1 and zero
  otherwise. Set k=1, omega=sqrt(2), v=1/sqrt(2), psi=a b exp(i k r),
  Pi=a exp(i k r)[v b'+i omega b]. Only the initial-data amplitude a>0 is
  normalized to M_outer=2 M_critical; the action has no new parameter.
  These are free, non-equilibrium many-mode scalar data, with a nonzero
  conserved phase charge, rather than a rescaled equilibrium oscillon.
- METHOD / DEPENDENCIES: solve the same nonlinear mass and lapse
  constraints with independent adaptive radial ODE integration, and
  reproduce them with section 7's grid reconstruction. Use the analytic
  shell derivative in the ODE and the grid derivative in reconstruction.
  Amplitude shooting is monotonic on the positive-B branch. Stop shooting
  trials at M=1.1 M_target to keep a uniform positive-B bracket.
- PASS_CONDITION: nonzero positive phase charge, inward energy and charge
  flux, regular centre, B>=1-2 alpha M_target/20>0, q,sigma>0; outer mass
  matches target fractionally within 1e-9. Fixed-amplitude grid/ODE metric
  and charge discrepancies at h=.025 are <3e-4 and improve from h=.1,.05
  with successive ratios <0.6 unless already <1e-7. Local mass-flux and
  radial-constraint errors are <2e-3 on the fine grid with the same
  convergence rule. Their diagnostic radius is 50, enclosing the source.
- ERROR_BOUND / CROSSCHECK: adaptive ODE relative tolerances 1e-10/1e-12,
  max steps .1/.05; their mass/charge/lapse differences <1e-8; independent
  source integrals <1e-8; opposite-flux data have the same initial geometry,
  mass and charge. R=80 reconstruction changes core data by <1e-10.
  Zero field and the subcritical/extremal/supercritical vacuum-root
  classification are controls. Fixed-point tolerance remains unchanged.
- FAIL_CONDITION / FALSIFIER / RESIDUAL: a finite-radius pole, negative B,
  source/constraint mismatch or unmet numerical tolerance fails this
  construction. A solver failure leaves its continuation unresolved.
  Source normalization alone is not evidence for future black-hole formation.
- VALIDITY_HEALTH / BRANCHES: positive-B canonical scalar initial value
  domain, finite smooth stress and screened geometric response. Future
  stability and horizon continuation require their own evolved tests.
- OBSERVABLE_MAP: generalized mass, scalar phase charge, energy/charge
  flux, areal mass/charge radii and metric coefficients on this initial
  slice. OBSERVATION / FORWARD_MODEL / DATA_ROLE / IDENTIFIABILITY: N/A,
  no detector data, fit, microscopic particle identification or uniqueness
  inference. BENCHMARK: independent same-action ODE and zero-field limit.
- CLOSURE_FLAGS: initial_data_ready=False until all checks pass;
  black_hole_formation=False; singularity_removal=False;
  full_RefG_pressure_join=False. PROVENANCE: code hash and numerical
  evidence on stdout. FILES: this report, its existing verifier, W92 index.
  Monographs, earlier source engines, private assumptions and Git rules
  remain unchanged; no generated output files or external publication.

### Source normalization and initial geometry

The packet is an admissible non-equilibrium configuration of the same
complex scalar. With D=psi_r, its phase charge density and inward currents
are explicit:

    Im(conj(psi)Pi) = omega a^2 b^2 > 0,
    Im(conj(psi)D) = k a^2 b^2 > 0,
    Re(conj(Pi)D) = a^2 [v (b')^2 + omega k b^2] > 0

where the nonzero packet is supported. Thus both outward charge flux
-r^2 sigma B Im(conj(psi)D) and outward energy flux -M_t are negative.
The packet's v=1/sqrt(2) is an initial-data coefficient; it is distinct
from any future metric shift. The choices omega^2=k^2+1 and v=k/omega
give a flat, linear massive-wave reference. In the nonlinear curved
initial slice the exact equations, not that flat dispersion relation,
determine subsequent motion.

With S=|Pi|^2+|D|^2=a^2 S_b, solve

    M_r = r^2 (B S/2+V),
    (log sigma)_r = alpha r q^2 S,
    Q_r = r^2 omega a^2 b^2,
    M(20)=Q(20)=0, sigma(40)=1.

The interior has M=0, B=1 and constant sigma. Outside the packet, M is
constant, sigma=1, and B is the same saturation vacuum exterior.
All packet derivatives vanish at its boundaries, so the source joins
smoothly without a distributional surface layer. The central limit is
the existing flat branch of the reduced spherical equations.

Only a is adjusted to the specified source mass. Its variational equation

    (M_a)_r + alpha r q^2 S M_a
      = r^2 [B a S_b + V_f b],   V_f=f(1-f^2/2)^2

has a nonnegative source on B>0. This establishes monotonic amplitude
shooting within the declared family. A finite-difference derivative of
the independently solved mass verifies M_a numerically. The freely
chosen target mass defines the experiment, rather than a successful
future-collapse result.

For the target mass, positive density and 0<=M(r)<=M_target imply

    B=1-2 alpha M(r)q(r)/r
      >=1-2 alpha M_target/20=0.4803847577

throughout the packet and exterior, while B=1 in the cavity. The slice
is initially untrapped despite its supercritical total mass. If that
same total mass were subsequently enclosed within a sufficiently small
radius, its vacuum polynomial would have two positive roots. At the
present initial time those formal roots lie in the flat cavity and
are not horizons of the actual source solution.

### Numerical result and continuation boundary

The normalized amplitude is a=0.0905332116650878. Independent radial
integration gives

    M_critical = 64.9519052838,
    M_outer   = 129.9038105677,
    Q         = 103.8976654496,
    sigma(0)  = 0.7450827745,
    dM_outer/da = 2492.41208509.

These are dimensionless model quantities. The scalar phase charge has
the same definition as in section 7. The formal vacuum radii for the
total mass are 2.2610317497 and 9.9744830659, both below the packet's
inner edge at 20, where the actual metric is flat up to its constant
time normalization.

The same amplitude is used on every grid, without grid-by-grid mass
refitting:

| h | Reconstructed outer mass | Maximum mass-profile error / M_target | Minimum B |
|---|---:|---:|---:|
| 0.1 | 129.7979280884 | 8.18e-4 | 0.72392757 |
| 0.05 | 129.8773074860 | 2.05e-4 | 0.72375752 |
| 0.025 | 129.8971827658 | 5.12e-5 | 0.72371578 |

At h=.025, the metric-B and lapse relative errors against the ODE are
1.94e-5 and 2.40e-5, and the scalar-charge error is 5.71e-8. The local
mass-flux residual is 6.08e-5, while independent radial mass/lapse
residuals are 3.98e-6 and 3.61e-6. Each of these discretization errors
decreases approximately fourfold when h halves. The diagnostic radius
50 contains the full matter support. The R=80 check gives the same
reconstructed core geometry. ODE tolerance and independent quadrature
differences are below 5e-15, which does not supersede the larger grid
error budget.

The maximum initial enclosed-mass growth rate is about 6.454 model
units and the outward charge flux reaches -5.571. Reversing the packet
with (psi,Pi)->(conj(psi),-conj(Pi)) reverses both currents while keeping
its mass, charge and geometry unchanged. This checks the direction of
transport without changing the source budget.

The first implementation passed 51/53 checks. Its two failing tests
required exactly zero discrete mass right up to the analytic inner
support boundary. A centred derivative there samples the adjacent
nonzero packet cell. The corrected exact-flat test covers r<20-2h;
the separately retained inner-edge mass fractions are 9.72e-89,
2.70e-175 and zero on the three grids, below a 1e-12 bound. The field,
action, target mass, numerical solvers and accuracy thresholds remained
unchanged. This records a stencil-domain correction rather than a
physical change to the candidate.

Outcome: SUPERCRITICAL_INWARD_DATA_READY, 53/53 checks. The concrete
obstruction removed is the insufficient mass of section 7's small
oscillon. This stage establishes an inward, source-consistent starting
slice for collapse. Formation of a trapped region and the later
regularity of that evolution remain to be calculated; the full
foundation-pressure/readout match retains its earlier status.

An independent read-only rerun reproduced 53/53 with the same code hash.
The existing default, stationary and finite-window dynamics regressions
also passed 74/74, 63/63 and 85/85 respectively. All response fields for
both previous perturbation signs reproduced their earlier values exactly.
The new grid-access option and diagnostic radius therefore preserve the
previous dynamics. No monograph, private assumption file, Git rule or
earlier evolution engine was edited.

The next numerical implementation can reuse the accepted staggered
general-areal framework in `population_assembly_initial_data.py`,
particularly `StaggeredClockGrid` and `clock_rk4`. The same initial
slice has spatial A=B, lapse L=sigma sqrt(B), zero angular metric-shift
variable, and normalized scalar momentum P=Pi. Its gravity, source
constraints and curvature diagnostics require the saturation-action
expressions. The earlier Einstein-specific curvature substitutions
and rejected collocated-clock extension are not the continuation
equations for this candidate. The present polar-areal solver is used
only to prepare the untrapped initial slice.

Reproduce the data, convergence tables and failure ledger on stdout:

    python -B verify_spherical_saturation_bridge.py --supercritical-data --verbose

The implementation SHA-256 is
`04e14056f0527e16cef5a5efa2d6857a4a7c0498a88bbf1b86f2b7459bbf59de`.
No extra source data files are required: the profile, amplitude-selection
rule and all constraints are contained in this existing verifier.

## 9. Horizon-regular evolution of the supercritical source

### Frozen bounded experiment, 2026-09-12

CLAIM_ID: W92_SATURATION_COLLAPSE_V1. Evolve section 8's identical inward
packet under the SAME spherical saturation and sextic action. The
decision is whether a future-trapped region forms in a numerically
validated finite interval. The model parameters, amplitude-selection
rule and incoming phase are fixed. No material or gravitational law is
added. This is a conditional dynamical test, not an observational fit.

Use the existing staggered harmonic general-areal discretization, with
its gravity explicitly replaced by the saturation equations. Store
(psi,P,mu=M/r^3,v_faces,log L,tau_c). The spatial metric is
A=1-r^2 z+v^2, z=2 alpha mu/(1+2 alpha ell^2 mu). Cell/face A, L and q
must remain positive. Stop on a guard violation; retain all accepted
and failed diagnostics. The zero-shift initial slice has A=B,
L=sigma sqrt(B), P=Pi from section 8. Use the declared z=0 limit in the
empty cavity. Generic action smoothness or stability outside this
spherical domain is not a premise of the numerical decision.

Preflight: exact action/constraint identities, zero field, ell=0 full-RHS
agreement with the previous staggered engine, and the exact saturated
constant-potential contracting core with a harmonic clock. Neither the
old Einstein curvature formulas nor its collocated clock are inherited.

Pilot: h=.1, R=120, Courant .1, sample every .25, maximum T=80. If
F=1-r^2 z falls below -.02 with future trapping, continue one additional
time unit and stop. On a numerical guard, stop at the last full sample.
The full suite uses the pilot's terminal time (minus .5 if it hit a guard),
with h=.1,.05,.025, fine half-step and fine R=160 controls. This is a
predeclared stopping rule, not a selected late-time endpoint claim.

Accuracy: charge drift <1e-5, outer-mass drift <5e-3; independent radial
mass and regular-metric residuals <5e-3 on r<=80, with middle/fine ratio
<.6 unless below 1e-6. The origin mass constraint uses a nonzero global
source scale during the initially empty-cavity interval; its absolute
residual and local source are also recorded. Do not divide by an empty
centre's density. Waveform errors in minimum F, maximum density, charge
RMS radius and central proper time must refine (ratio<.6 or error<1e-4),
and time-step/domain errors must be <1e-3. All clocks and radial
geometric observables use the same gauge and sampling for comparison.

A trapped-region claim additionally requires at least four trapped fine
cells, theta_+<0 and theta_-<0 in every resolution/control case on two
successive samples, and negative F larger than three times the actual
resolution/control differences (with minimum magnitude .005). If the
terminal interval fails accuracy, report the maximal contiguous tested
prefix and retain rejected later samples. A numerical limit does not
decide the physical endpoint. This stage stops with validated trapping,
validated finite-time evolution without trapping, or unresolved evolution.

No detector data or uniqueness inference: FORWARD_MODEL/DATA_ROLE and
observational IDENTIFIABILITY are N/A. Dependencies are sections 6--8 and
the retained scalar/gauge finite-volume stencils. CROSSCHECK: independent
symbolic action projections, Einstein/constant-core limits, grid/time/domain
controls. CLOSURE_FLAGS start false for resolved_trapping, global_regularity,
singularity_removal and full_RefG_pressure_join. Only resolved_trapping
may be closed by this experiment. Residuals, code/source hashes and failed
guards go to stdout and this report. Allowed edits are the existing
verifier, this report and W92 index; old engines, monographs, private
assumptions and Git rules remain unchanged.

### Same-action horizon-regular equations

Pre-certification audit: the initial nine preflight checks and coarse pilot
passed, reaching F_min=-0.0741527 at t=51.75. The first refinement run was
stopped by the operator while the fine grid was running, to incorporate
independent review findings before issuing any certificate. This
preliminary pilot is not used as a validated result. The final suite is
rerun from its original initial data after these guard-only corrections:

- latch a trapping event even if the region later disappears, and stop the
  pilot exactly one time unit after its first qualifying event;
- reject nonfinite diagnostic inputs and finite/positive-lapse violations
  on cells and faces; test both failure paths with synthetic fixtures;
- freeze verifier and both source-engine hashes at entry and verify them
  unchanged at exit;
- check the action's real branch at every cell/face RK stage. With
  u=ell^2 z the allowed domain is 0<u<1 plus the checked u=0 vacuum limit.
  A negative-u allowance of 100 machine epsilons covers only roundoff;
  larger undershoot stops the run as NUMERICAL_ACTION_DOMAIN_LIMIT. Mu is
  never clipped and no negative-curvature action is introduced. Record
  minimum mu,u and maximum q, including the failed stage if there is one.

The physical acceptance tolerances and equations remain frozen. For
x=|psi|^2, V=x[(x-3)^2+3]/24 is nonnegative. The canonical source satisfies
|J|<=rho, J=sqrt(A) S. Before trapping, |v|<sqrt(A), so
M_r>=r^2 rho(1-|v|/sqrt(A))>=0. A resolved negative mass originating in a
regular empty cavity would therefore be a numerical/domain error on this
branch. After trapping the guard continues to enforce the established
action domain, without assuming monotonicity of M(r).

Use the general-areal metric

    ds^2 = -L^2 dt^2 + (dr+L v dt)^2/A + r^2 dOmega^2,
    mu=M/r^3, q=(1+2 alpha ell^2 mu)^(-1), z=2 alpha mu q,
    F=1-r^2 z, A=F+v^2, k=v/r, P=n(psi)/sqrt(A), D=psi_r.

Here v is the metric shift variable, not section 8's packet coefficient.
For the same canonical complex scalar and sextic potential,

    rho=A(|P|^2+|D|^2)/2+V, p=rho-2V,
    S=sqrt(A) Re(conj(P) D), beta=L v.

The spherical action projections and its conserved mass give

    M_r = r^2 (rho+v S),
    M_t = L r^2 [v(rho+p)+(A+v^2)S],
    k_t = L v k_r + L[k^2+z(1-3 ell^2 z)/2+alpha q^2 p]-A L_r/r,
    K^r_r = k+r k_r-alpha r q^2 S.

The physical mass flux is not multiplied by q^2. The saturation factor
belongs to the gravitational response, including both the pressure term
and the mixed extrinsic-curvature constraint. The unchanged scalar and
harmonic-clock equations are

    psi_t = L sqrt(A) P + L v D,
    P_t = r^(-2) partial_r[r^2 L(sqrt(A)D+vP)]-L V_force/sqrt(A),
    (log L)_t = beta (log L)_r-L[div(v)-alpha r q^2 S],
    (tau_c)_t = L_c.

The implementation evolves v on radial faces. Face q and z are calculated
from interpolated mu; the complete gravitational RHS is replaced, rather
than merely substituting the metric into the old Einstein solver.
An independent regular-metric identity is

    A_t-L v A_r+2 v A L_r+2 alpha q^2 L r A S=0.

Writing H=k^2-z=(A-1)/r^2 gives its centre-regular diagnostic without
subtracting nearly equal metric coefficients. Its radial derivatives and
the M_r constraint use a fourth-order diagnostic stencil, distinct from
the evolution stencil. The initial empty cavity is normalized by the
initial global density scale, or the actual local density once larger;
the absolute origin error is retained too.

The two radial null expansions are

    theta_plus=2(sqrt(A)-v)/r,
    theta_minus=-2(sqrt(A)+v)/r,
    theta_plus theta_minus=-4 F/r^2.

Both must be negative for future trapping. A negative F alone does not
distinguish a future-trapped region from a past-trapped one. Neither a
zero lapse nor the vacuum roots extrapolated inside the source are used
as horizon evidence.

The exact saturated constant-potential preflight has psi=sqrt(2), P=D=0,
rho=1/3, p=-1/3, mu=1/9, A=1 and

    k=sqrt[2 alpha/(9+2 alpha ell^2)],
    L(t)=L0/(1+3 k L0 t), tau_c=log(1+3 k L0 t)/(3 k).

It tests the saturation terms and the integrated clock simultaneously.
It is a local analytic control, not the collapse packet's exterior.

### Completed bounded result: accepted prefix and later trapping candidate

**Decision: VALIDATED_PRETRAPPING_PREFIX, 0<=t<=27.5.** All five runs
completed through t=51.75. The later solution contains a future-trapped
region in every grid/control case, but the registered continuous-history
certificate stops at an earlier origin-refinement failure. The numerical
candidate is retained explicitly; resolved_trapping remains false.

The first rejected prefix ends at t=27.75. Its normalized origin mass
constraint is 1.27797920909e-4 on h=.05 and 1.95950064690e-4 on h=.025:
the fine/middle ratio is 1.53328. Both absolute normalized errors are
below .005, but the fine error exceeds 1e-6 and its ratio exceeds .6.
Every other gate at that prefix passes. No threshold is relaxed and the
later good interval does not erase this failed intermediate check.
This stage identifies a local convergence limitation. Section 10 below
identifies its dominant local spatial-error term.

There are **39/39 passing preflight, terminal and implementation-control
checks**, with zero failures in that list. That count is distinct from
the continuous-prefix certificate: the complete t<=51.75 evolution has
not passed the latter. The program returns both the accepted prefix and
the first rejected prefix, alongside the terminal-only verdict.

The following values are the **later, uncertified candidate at t=51.75**,
in the same dimensionless model units used above:

| Run | Outer mass | Minimum F | Consecutive trapped cells | Central proper time |
|---|---:|---:|---:|---:|
| h=.1, R=120 | 129.7979280884 | -0.0741527449 | 38 | 35.1393885168 |
| h=.05, R=120 | 129.8773074860 | -0.0800260725 | 79 | 35.1112040252 |
| h=.025, R=120 | 129.8971827658 | -0.0814830888 | 159 | 35.1041542045 |
| Fine, half time step | 129.8971827658 | -0.0814830888 | 159 | 35.1041542045 |
| Fine, R=160 | 129.8971827658 | -0.0814830888 | 159 | 35.1041542045 |

At the fine minimum, r=7.0875, theta_plus=-0.02073655306 and
theta_minus=-0.31289942405. The charge RMS radius is 5.6381372991,
maximum density is 16.3746830482 and central lapse is 0.2341611488.
The first negative-F sample is t=50 on the fine, half-step and enlarged
domain grids, and t=50.25 on the other two. The earliest tiny negative
sample alone is not the registered two-sample trapping certificate.

The whole-window terminal diagnostics are:

| Residual maximum on 0<=t<=51.75 | h=.05 | h=.025 |
|---|---:|---:|
| Radial mass constraint | 4.62492256e-3 | 1.16208160e-3 |
| Regular metric identity | 8.17822951e-5 | 2.01364940e-5 |
| Source-normalized origin constraint | 3.51600347e-3 | 7.86715419e-4 |

The middle-to-fine versus coarse-to-middle waveform error ratios are
0.24807 for minimum F, 0.25486 for maximum density, 0.25007 for charge
RMS radius and 0.25013 for central proper time. The largest normalized
half-step difference across those waveforms is 1.20e-10; the largest
domain difference is 1.64e-15. These convergent late/full-window maxima
coexist with the failed early prefix and cannot substitute for it.

Outer mass is constant to the emitted precision in every run. Final
relative charge drifts are -1.84e-10, -5.93e-12 and -1.97e-13 on the
three grids, and -6.88e-15 in the half-step control. The zero outer
scalar flux makes mass/charge checks necessary but insufficient alone;
the enlarged-domain and local constraints are retained independently.
All RK stages stay in the registered action/chart domain: minimum mu=u=0,
maximum q=1; fine minimum q=0.3641357654, cell A=0.2650973242, face
A=0.2650908410 and lapse=0.2310458871. Maximum Courant across the suite
is 0.09350521. No action-domain or evolution guard was triggered.

Independent read-only checks reproduce the pilot exactly (12/12,
t=51.75, 38 trapped cells), plus the previous 74/74 base, 63/63 stationary,
53/53 initial-data and 85/85 small-perturbation suites. The old radius
responses are unchanged. The Einstein-RHS limit error is 1.73e-18; the
saturated-core clock errors at dt=.05,.025 are 1.19e-11 and 7.34e-13.
Two independent reviews confirmed the equations and the distinction
between the terminal verdict and the broken continuous prefix.

The verifier hash was recorded before launching the full run and remained
unchanged through its end:
`189a9d7fee09a14983d87ad09b9cfc72f5f614b197d6e9b68d3c2831a6ef2cba`.
Retained staggered engine:
`df0d16c7715a2c3e3e02ec3487f2cad2860bf772e69983de6e2fb5af295af97d`.
Retained scalar engine:
`2c310a3a600b2ced39333c14a208a2fcb97ed6178c6906e0a55366e35ab1e4ca`.
Both intuitive monographs, the old engines, private assumptions and Git
rules remain unchanged. No result files are generated.

**Registered follow-up, completed in section 10:** diagnose only the t=27.5--28 origin transition,
using the same action and thresholds. Record the absolute constraint,
normalization/local density and its separate 3mu, r mu_r, -rho and -vS
terms on the first two cells; compare half steps, an even-parity estimate
at the common centre and an independently integrated mass constraint at
fixed physical radii. The present first-two-cell norm samples different
radii on different grids; test that effect explicitly. Add a finer grid
only if these diagnostics cannot discriminate the cause. A short rerun
through t=28 covers the first failure. Wavefront arrival, cancellation or stencil error
are diagnostic possibilities, not established explanations. No new
material law or longer collapse scan is called for before this check.

Closure: same_action_source_evolution=true; validated_prefix_end=27.5;
resolved_trapping=false; global_regularity=false; singularity_removal=false;
full_RefG_pressure_join=false. This stage adds an evolved massive-source
candidate and a precisely located certification obstacle.

Reproduce the complete decision and all sampled diagnostics with:

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --saturation-collapse --verbose

## 10. Bounded diagnosis of the early origin-refinement failure

Frozen before replay, 2026-09-12. CLAIM_ID: W92_SATURATION_ORIGIN_AUDIT_V1.
Goal: identify the discrete cause of section 9's first failed origin gate,
at t=27.75. The action, source, gauge, integration scheme and section 9
acceptance thresholds remain unchanged. This is a numerical diagnosis,
not a new physical model or a new trapping certificate.

Replay only to t=28: h=.1,.05,.025 on R=120, plus the fine half-step
control. Reproduce the recorded middle/fine normalized residuals within
1e-10 absolute. Record both normalization and absolute errors, separate
3mu, r Dmu, -rho, -vS terms, and their evolution rates at t=27.5,27.75,28.
Compare the common-centre even-parity extrapolation and independent
source-integrated mass at fixed radii .1,.2,.4. These are diagnostic
crosschecks; none replaces the original first-two-cell gate. Synthetic
even-polynomial checks audit the derivative and integrated constraint.
Time-step agreement of the failing absolute residual must be within
1e-3 relative before assigning the issue to spatial discretization.

One finer h=.0125 replay is allowed only if the initial term/radius/time
comparison cannot distinguish the origin of the failure. No longer
collapse scan, new constitutive term, relaxed threshold or monograph
change is authorized by this diagnostic. Stop with a demonstrated
numerical cause and any directly justified, separately checked repair,
or a precise unresolved numerical term. Physics/observational inference,
DATA_ROLE, FORWARD_MODEL and IDENTIFIABILITY are N/A for this solver audit.
Dependencies: sections 8--9 and their unchanged source engines. Allowed
files: this report, its verifier and W92 index. Output goes to stdout;
the report retains the conclusion, errors and hashes. Closure of trapping,
global regularity, singularity removal and the full pressure join remains
separate from diagnosis of this numerical gate.

### Completed audit: identified leading spatial discrepancy

**Decision: ORIGIN_LEADING_SPATIAL_DISCREPANCY_IDENTIFIED.** The mass-source
and scalar wave operators have unequal leading spatial truncation errors
at the regular centre. Their predicted mismatch quantitatively reproduces
the measured local constraint-production rate. There is no missing
leading centre factor or sign in the continuum equations. No evolution
equation, acceptance threshold or physical postulate was changed.

The four registered replays pass 25/25 controls and reproduce the original
middle/fine origin residuals exactly. At t=27.75 the fine half-time-step
relative difference of the first-two-cell absolute residual is
1.4988792e-6, far below the registered 1e-3. Throughout the sampled
transition, normalization remains the fixed initial global-density floor,
not a switch to the local density. A three-point even extrapolation to
the common r=0 point retains the error:

| h | Original normalized origin error, t=27.75 | Common-centre C | Common-centre density |
|---|---:|---:|---:|
| .1 | 3.53098611e-5 | -6.27268626e-7 | 9.09234952e-5 |
| .05 | 1.27797921e-4 | -2.07986456e-6 | 6.79501828e-4 |
| .025 | 1.95950065e-4 | -3.15034064e-6 | 2.30847312e-3 |
| .0125 | 1.03352917e-4 | -1.64636166e-6 | 3.39600458e-3 |

Thus time integration, normalization and sampling different cell radii
cannot account for the discrepancy alone. The incoming source profile
itself still differs substantially between resolutions. Its uniform
spatial convergence through this transition has not been established.

For smooth even psi=psi0+psi2 r^2+psi4 r^4+..., the native derivative gives
D_h psi/r=psi_r/r+4 psi4 h^2+O(h^4). Freeze the flat principal part,
L=L0, v=0, with locally constant P. The first two cells then give

    delta(mudot at r=0) = 4 L0 Re(conj(P0) psi4) h^2,
    delta(Cdot)_first_two = L0 Re(conj(P0) psi4) h^2 [2, 6/7],
    C = 3mu+r D_h mu-rho-vS.

These are leading truncation terms, not corrections inserted into the
physics. The actual production RHS, tested off shell with mu=v=logL=0,
P=1 and psi=r^4, gives the scalar wave operator
20r^2+h^2[10,78/7] and the differentiated mass operator
20r^2+12h^2. Their difference is exactly h^2[2,6/7] up to roundoff
(maximum absolute discrepancy below 2.3e-16 on three grids).
Both operators approximate the same continuum identity, but their
finite-grid errors differ.

At t=27.75, h=.025, fitting psi4 and P0 from the existing first three
nodes predicts the central mudot defect -3.48040650e-5; the measured
discrete-minus-centre-continuum defect is -3.48167365e-5. The corresponding
first-cell Cdot prediction is -1.74020325e-5 versus -1.71389166e-5 measured.
The disagreements are about .04% and 1.6%, respectively. At h=.0125
the same predictions are -6.82982307e-6 and -3.41491154e-6, versus measured
-6.84246766e-6 and -3.41006218e-6. The latter disagreements are .19%
and .15%. Nonflat terms, higher spatial coefficients and fitting errors
are not set to zero in the actual evolution; this is a local leading
error budget, not an exact decomposition of every accumulated error.
The full semidiscrete chain-rule Cdot independently agrees with a
directional finite difference to 5.74e-12.

The independent fixed-radius constraint
[R^3 mu(R)-integral_0^R r^2(rho+vS)dr]/R^3 remains nonzero away from the
first cell. At R=.2,t=27.75 its cubic-reconstruction values are
4.40251589e-7 on h=.025 and 3.67398090e-7 on h=.0125. The corresponding
linear-in-r^2 values are 4.64996727e-7 and 3.67397718e-7. This crosscheck
does not replace the gate; the two source reconstructions' difference
is not a rigorous quadrature or total-error bound.

The one authorized finer replay completes t=28 with 19/19 controls,
without action-domain or chart failure. It improves the targeted error
but does not repair the continuous-prefix certification:

| t | Original origin norm, h=.025 | Same norm, h=.0125 | Finer/fine |
|---|---:|---:|---:|
| 27.5 | 4.01358504e-6 | 4.48541894e-6 | 1.11756 |
| 27.75 | 1.95950065e-4 | 1.03352917e-4 | .52745 |
| 28 | 5.67296702e-4 | 1.87485922e-4 | .33049 |

In particular, the finer pair still fails the unchanged local refinement
criterion at t=27.5. The audit retains transition samples, not a new
whole-history certificate. It neither withdraws section 9's original
accepted h=.05/.025 prefix nor upgrades its later trapping candidate.

Both replay commands used unchanged verifier hash
`78ac9ec249f2e9edaebd9144172f0c08341c44459d1c4f5f9c93feaa1ad76ddb`.
After replay, the diagnostic-only quartic budget and short operator-test
entry point were added. Their version is
`bb7d435f8195193d5cf814b51e32e94539e0cb344731d9acea20c091783196ba`:
21/21 short controls and the base 74/74 suite pass, independently rerun
at this later hash. The new budget function also reproduces all twelve
retained four-run snapshot estimates. The 12/12 pilot regression used
the earlier 78ac9ec... hash and reproduced its prior numerical results;
no frozen replay is claimed to have used the later diagnostic-only hash.
The two source-engine hashes remain those in section 9.

**Next bounded implementation:** make the central spatial mass balance
and scalar flux discretization mutually consistent, preserving the
retained charge balance and continuum equations. First require the
quartic manufactured mismatch to vanish at leading order; then replay
only through t=28 and apply the original constraints and time-step tests.
Do not enforce mu=rho/3 after a time step, alter the normalization, or
subtract the fitted error from reported residuals. No new matter law or
longer collapse scan is justified before this paired-operator check.

Closure: local_numerical_cause_identified=true; numerical_repair=false;
resolved_trapping=false; global_regularity=false; singularity_removal=false;
full_RefG_pressure_join=false. The monographs, private assumptions and Git
rules are unchanged; no generated result files are left behind.

Reproduce the short controls or the bounded replays:

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --origin-controls --verbose
    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --origin-audit --verbose
    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --origin-finer --verbose

The latter two now include the three new operator checks (28 and 22
checks respectively if all pass), plus the snapshot quartic budget.
This accounting change is not additional evolved physics.

## 11. Paired spatial repair: registered short test

CLAIM_ID: W92_PAIRED_ORIGIN_REPAIR_V1, registered 2026-09-12 before replay.
Goal: remove section 10's leading centre mismatch and test the same
massive-source evolution through t=28. Only this report, its verifier and
the W92 diagnostic index may change. The old numerical branch, continuum
action, source preparation, gauge and acceptance thresholds are retained.

Candidate: a sixth-order staggered field gradient and its radial weighted
adjoint in the wave operator, a fourth-order adjoint transport pair and a
fourth-order physical field gradient in the mass source. This factorized
wave operator has a nonpositive quadratic form for every positive face
coefficient in its nodal-weighted inner product. The transformed-u fourth-order preliminary construction was
replaced before evolution: its diagonal correction failed this general
energy-sign requirement. No collapse results were used in that choice.
Its exact discrete charge uses midpoint nodal weights h r^2; the old
finite-volume weights h(r^2+h^2/12) remain in the reference branch.
This quadrature change is declared before testing; both approximate the
same continuum charge. The relative charge-drift threshold stays 1e-5.
The original mass, origin, metric and waveform thresholds are unchanged.
No state projection, fitted correction or new material parameter is used.

First require constant/quadratic/quartic centre controls, cancellation of
the leading manufactured mass/wave mismatch, the actual semidiscrete
charge identity and finite positive kinetic weights. Check the symmetric
wave spectrum on constant and smooth positive coefficient controls.
Only then run h=.1,.05,.025, R=120, a fine half-step and R=160 control,
all through t=28, retaining every sample from t=0. Apply section 9's
continuous-prefix gate unchanged, with the declared charge quadrature.
PASS requires the full t<=28 prefix and preflight/control gates. FAIL
identifies a numerical limitation of this discretization, not a physical
no-go. Stop at that decision; no longer collapse run or monograph export.
Theoretical and observational closure flags remain separate. DATA_ROLE,
FORWARD_MODEL and IDENTIFIABILITY are N/A for this numerical repair.

### Discrete equations and scope

Let W=diag(h r_i^2), V_f=diag(h w_f r_f^2), with endpoint face weights
w_f=1/2 and interior weights 1. G is the sixth-order staggered derivative,
E the fourth-order centred even-parity derivative, and c_f the four-point
interpolation of c=L sqrt(A). The actual scalar operators are

    G = [-9,125,-2250,2250,-125,9]/(1920h),
    E = [1,-8,0,8,-1]/(12h),
    I_face = [-1,9,9,-1]/16,
    wave(psi) = -W^(-1) G^T V_f diag(c_f) G psi,
    K psi = diag(beta) E psi,
    psi_t = c P + K psi,
    P_t = wave(psi) - W^(-1) K^T W P - L V_force/sqrt(A).

Even reflection supplies the radial scalar boundary closure. Its outer
boundary remains a closed computational boundary and is checked by the
enlarged domain. With positive c_f, the exact weighted quadratic form is
conj(psi)^T W wave(psi)=-sum(h w_f r_f^2 c_f |G psi|^2)<=0.
The transport pair cancels in Qdot,
and the real local potential contributes no imaginary charge source.
These identities apply to the implemented matrices, including boundaries.
The gauge keeps its original finite-volume denominator; replacing that
denominator by W would spoil its exact linear radial-divergence control.
Both charge quadratures are reported separately at every sampled time.

The mass evolves by the original independent action equation using E psi
in rho and S. Nothing sets the mass from a constraint residual. The
original diagnostic derivative of mu, its normalization and the acceptance
thresholds remain unchanged. The new wave/source pair is exact at the
centre for the tested quadratic and quartic profiles; the sixth-power
wave error decreases as h^4. This does not assign fourth-order accuracy
to the entire evolution: the retained gravity/gauge scheme is second
order, and the r^(-2)-weighted E-adjoint transport can also retain a
second-order centre term. For beta=k r and P=P2 r^2, that transport's
first-cell defect is -16 k P2 h^2. Its effect is subject to the original
replay gates, not removed from the measured error.

The additional frozen-wave RK bound is computed from an absolute-matrix
upper bound on the symmetric wave operator's frequency, including the
actual face/node wave coefficients. dt*omega_bound must remain below 2.5,
inside RK4's imaginary-axis limit. This complements the retained Courant
guard and the half-step experiment; it is not a theorem about the full
time-dependent nonlinear evolution.

The implemented preflight passes 33/33 checks, independently rerun.
The three-grid quartic mass/wave mismatch is at most 2.71e-16; the
variable-coefficient quadratic check is below 8e-15. The r^6 wave errors
are .0084375, .00052734375 and .000032958984375 on h=.1,.05,.025,
decreasing by 16 at each refinement. The normalized adjoint-charge
residual is 1.44e-16 and the complete RHS charge rate is -1.30e-18.
The symmetric wave sign also passes the deliberately sharp positive
face-coefficient control. The unit-speed frozen-wave RK number is .272551.
Independent base 74/74 and original-origin 21/21 regressions pass.
The original gravity RHS, verdict and certify functions are unchanged
at AST level. The replay version, frozen before evolution, is

`8eb53c01c163a69636cfe88ea71ed23a792c13c8d52fb34c72b49a7f8b6d0613`.

### Completed result: the full short prefix passes

**Decision: PAIRED_ORIGIN_REPAIR_VALIDATED, 0<=t<=28.** All five runs
complete 113 samples, including the initial slice. Every registered
prefix from .25 through 28 passes; first_rejected=null. The 60/60
preflight, terminal and decision-control checks pass as well. In
particular, section 9's earlier t=27.75 certification obstacle is cleared
by a changed numerical discretization with the same physical equations.

| t | Origin norm, h=.05 | Origin norm, h=.025 | Fine/middle |
|---|---:|---:|---:|
| 27.5 | 1.42537878e-4 | 1.29663390e-5 | .09097 |
| 27.75 | 8.17361046e-4 | 5.09026202e-5 | .06228 |
| 28 | 9.92543241e-4 | 7.11463891e-5 | .07168 |

The whole-window maximum radial mass constraints are 2.28856008e-4 and
5.72550039e-5 (fine/middle .25018); the regular metric residuals are
7.95834990e-7 and 3.90224329e-7 (.49033). The origin maxima are the
t=28 values above. These meet the original fine error <.005 and
(fine error <1e-6 or fine/middle <.6) condition at every sampled prefix.
The coarse origin maximum is .01375454; the unchanged accuracy decision
uses the middle/fine pair, not a claim that the coarse grid has the
fine-grid accuracy. Individual old/new residuals need not decrease at
every time and resolution; the improvement is the now-passing continuous
refinement certificate.

The normalization formula remains the initial/global or larger local
density. Its initial value is recomputed with the selected physical
gradient: .01463681618 on the middle grid and .01463652332 on the fine
grid; neither is fitted to the residual. The fine first-two-cell
absolute error at t=27.75 is 7.45037387e-7. Its half-step relative
difference is 8.0281e-6, below the 1e-3 short-audit criterion.

The waveform refinement ratios are .25016 (minimum F), .23825 (maximum
density), .25142 (charge RMS radius) and .25080 (central proper time).
The largest normalized half-step difference for these waveforms is
6.50e-12; the largest enlarged-domain difference is 3.45e-16.
The final dimensionless fine-grid state is

    t=28, tau_c=20.8628329776, M_outer=129.8971827658,
    F_min=.5511176546 at r=21.3875, Q_RMS_radius=16.8385894819,
    rho_max=.05463524459, L_c=.7452667905, trapped_cells=0.

Outer mass stays constant to emitted precision. Nodal relative charge
drifts are -1.04e-10, -3.30e-12 and -1.07e-13 on the three grids,
and -3.97e-15 for the half step. The initial legacy-volume/nodal charge
differences are 9.14e-7, 2.29e-7 and 5.71e-8 relative, with second-order
quadrature scaling. At t=28 the fine difference is 2.43e-7; its legacy
charge drifts by 1.86e-7. Both readouts remain visible, and the selected
nodal charge obeys the exact implemented semidiscrete identity.

No chart, action or time-step guard triggers. The fine minimum cell/face
A values are .5724291132/.5724303452, minimum lapse .7450985976 and
minimum q .9951844168. The smallest recorded u is -1.05e-14 and the
largest q is 1+1.07e-14, within the existing 100-machine-epsilon allowance
at the zero-curvature action boundary; no value is clipped. Across
all cases the maximum retained Courant number is .093506 and the
maximum new frozen-wave RK number is .254849, below their respective
.4 and 2.5 guards. The verifier and both source-engine hashes remain
unchanged from launch to completion.

Closure: paired_origin_repair=true; validated_prefix_end=28;
same_saturation_action=true; resolved_trapping=false;
global_regularity=false; singularity_removal=false;
full_RefG_pressure_join=false. This short interval is entirely untrapped.
Section 9's later trapping candidate belongs to the old discretization
and must be recomputed with the repaired pair before promotion.

**Next bounded step:** continue this verified numerical branch to the
previously targeted trapping interval, applying the same prefix,
two-null-expansion and refinement controls. This stage stops at t=28 as
registered. Both monographs, the private-assumption folder, old engines
and Git rules are unchanged. No generated result files are added.

Reproduce:

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --paired-controls --verbose
    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --paired-origin --verbose

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
