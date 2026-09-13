# Saturating spherical gravity coupled to conserved matter

**შედეგი მოკლედ:** მიღებულია პოსტულატურ გაჯერების კანონზე დაფუძნებული
სფეროსიმეტრიული მოდელი, რომელშიც მატერიის შეკუმშვა და გარე ველი ერთი
მოქმედებით ითვლება. ერთგვაროვანი უწნევო წყაროს ამოხსნაში სიმრუდე
შეზღუდულია; კანონიკური ველის კოლაფსში მისი სასრულობა გამოთვლილ
მონაკვეთზეა შემოწმებული. §14 ადგენს, რომ თვითნებური ადგილობრივი წყაროს
შემთხვევაში გაჯერება ამ ზღვარს ავტომატურად ვერ უზრუნველყოფს.
სრული RefG-მიერთება ჯერ ვერ ჩაითვლება მიღწეულად:
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

## 12. Paired collapse continuation: registered trapping-window test

CLAIM_ID: W92_PAIRED_COLLAPSE_WINDOW_V1; registered 2026-09-13 before
the extended evolution. Goal: decide whether section 8's massive scalar
packet produces resolved future trapping under section 11's repaired
discretization. The immediate obstacle was the old early constraint
failure; section 11 cleared that obstacle through t=28.

TYPE: CONDITIONAL / NUMERICAL_EVIDENCE. MODEL_VERSION, ASSUMPTIONS and
DEPENDENCIES: the same postulated spherical saturation action, canonical
complex scalar, source preparation and harmonic gauge as sections 8-11.
DOMAIN and CONVENTIONS: dimensionless 0<=t<=51.75, radial one-metric
spherical evolution in the existing positive chart/action domain.
FREEDOM_LEDGER: no new physical parameter, initial profile, projection,
filter or fit; only the registered endpoint changes from 28 to 51.75.
The new --paired-collapse option leaves --paired-origin at its old endpoint.

METHOD / CROSSCHECK / BENCHMARK: recompute from the same initial slice
on h=.1,.05,.025 with R=120, plus h=.025 at half time step and R=160.
Retain all .25-spaced samples and apply the existing verdict/certify
functions unchanged to every prefix. Use the repaired nodal charge
weights while retaining the legacy-volume readout and gauge weights.
Section 11's overlapping t<=28 interval is the reproducibility benchmark.
RESIDUAL / ERROR_BOUND / VALIDITY_HEALTH: retain section 9's radial,
origin and metric residual budgets, mass/charge conservation, waveform
refinement and half-step/domain thresholds, plus section 11's positive
wave-coefficient and RK guards. The preflight suite must pass first.

PASS_CONDITION: all necessary certification controls pass and some
continuously accepted prefix contains the existing two-successive-sample
future-trapping certificate: both null expansions negative on all five
runs, at least four contiguous fine-grid trapped cells, and every run's
minimum F below the negative of the unchanged .005 floor or three times
the inter-run F uncertainty, whichever is larger. The inherited waveform/residual tests also
have to pass. This is sampled numerical evidence, not an event-horizon
or global-completeness theorem.
FAIL_CONDITION: no such accepted trapping certificate by the fixed
endpoint. A failed prerequisite/certification control invalidates promotion;
a later guard or terminal failure limits the validated interval while
preserving any earlier valid trapping certificate. Report fixed-window
completion, first rejected prefix, last accepted prefix and any later
uncertified candidate separately.
FALSIFIER: nonfinite state, action/chart exit or nonconvergent constraints
invalidates numerical claims beyond that point; this alone does not
reject the continuum physical mechanism. BRANCHES: this paired branch
only; section 9's late old-grid candidate is not inherited.

OBSERVABLE_MAP: F and both future null expansions from the evolved
physical metric; conserved phase charge, outer mass, charge RMS areal
radius, density and central proper time remain separately reported.
FORWARD_MODEL, DATA_ROLE and IDENTIFIABILITY: N/A, no observational
inference or parameter identification is performed in this numerical test.
CLOSURE_FLAGS: resolved_trapping is computed from the certificate;
global_regularity, singularity_removal and full_RefG_pressure_join stay false.
FILES: only this report, verify_spherical_saturation_bridge.py and
medium_health_horizon_diagnostic.md may change. Old engines, monographs,
the private-assumption folder and Git rules remain unchanged.
STOP: finish the five fixed-window runs and the stated decision. No new
parameter family or interior-regularity extension belongs to this stage.
PROVENANCE: code/source hashes are emitted and checked at run completion;
results go to stdout, without adding generated data files.

Preflight before the extended evolution: 33/33 checks pass.
Continuation verifier SHA256:
`3849c28a492dd5aba19f765ff6b2e2f2610b5fdfe4a5c5dfef7ec42f73448e12`.

Reproduce:

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --paired-collapse --verbose

### Completed result: resolved future trapping in the paired branch

**Decision: PAIRED_VALIDATED_FUTURE_TRAPPING.** All five runs complete
t=51.75 with 208 samples each. All 207 sampled prefixes from .25 to
51.75 pass the unchanged certificate; first_rejected=null. All 60/60
preflight, terminal and decision controls pass. The first certified
future-trapping pair ends at t=50.5. The earlier sign change at t=50
has fine F_min=-.00121916 and is below the registered .005 magnitude
floor, so it is retained only as the first numerical trapping sample.

| Run | h | Outer R | Final F_min | Contiguous trapped cells |
|---|---:|---:|---:|---:|
| Coarse | .1 | 120 | -.08250984767 | 40 |
| Middle | .05 | 120 | -.08211034576 | 80 |
| Fine | .025 | 120 | -.08199855666 | 160 |
| Fine, half time step | .025 | 120 | -.08199855667 | 160 |
| Fine, enlarged domain | .025 | 160 | -.08199855666 | 160 |

At the final fine-grid minimum, r=7.0875, the future null expansions
are theta_plus=-.02086798009 and theta_minus=-.3128957338. Their product
agrees with -4F/r^2 at emitted precision. Three times the largest
fine/middle, half-step or domain F difference is .0003353673, below
the .005 floor; every run's final negative F exceeds that floor in
magnitude. These are resolved future trapped surfaces of the evolved
metric, not a lapse-only or coordinate-slowing criterion.

| Whole-prefix maximum residual | Middle | Fine | Fine/middle |
|---|---:|---:|---:|
| Radial mass constraint | 2.28856008e-4 | 5.72550039e-5 | .25018 |
| Regular metric equation | 1.23371691e-5 | 3.35110029e-6 | .27163 |
| First-two-cell origin constraint | 1.42194075e-3 | 3.51476348e-4 | .24718 |

The waveform refinement ratios are .26266 (minimum F), .24078 (maximum
density), .25312 (charge RMS radius) and .25039 (central proper time).
Their normalized middle/fine differences are respectively 1.54777e-4,
1.89045e-4, 3.85557e-5 and 5.67875e-5. The maximum normalized half-step
difference is 3.62084e-11; the enlarged-domain maximum is 1.69387e-15.
The coarse origin maximum remains .01375454; the unchanged residual
accuracy decision uses the middle/fine pair.

The final fine state, in the same dimensionless units, is

    t=51.75, tau_c=35.1018512886, M_outer=129.8971827658,
    Q_RMS_radius=5.63427922389, rho_max=16.3889881409,
    L_c=.234094749876, F_min=-.081998556660, trapped_cells=160.

The outer mass equals its initial value at emitted precision. Maximum
relative nodal-charge drift is below 2.0e-13 on the fine grid and
8.0e-15 at half step. These refer to the conserved phase charge. The
fine t=28 radius, density, mass, lapse, proper time, F and origin residual
reproduce section 11 to its reported precision, including
F_min=.551117654554 and origin residual=7.11463890783e-5.

All runs stay inside the implemented chart/action and time-step guards.
Fine stage minima are A=.26493758, face A=.26493301, L=.23096239 and
q=.36395737. The largest five-run Courant and frozen-wave RK numbers
are .093506 and .254849, below .4 and 2.5. Tiny negative u values
(fine minimum -1.05e-14) remain within the same 100-machine-epsilon
zero-boundary allowance used in section 11; no clipping is applied.
The verifier and both source-engine hashes match their launch hashes.
Independent base 74/74 and paired-preflight 33/33 regressions also pass;
an AST/decision audit confirms unchanged source, RHS, verdict and certify
definitions. Only the CLI duration/routing and result label change.

Closure: resolved_trapping=true; validated_prefix_end=51.75;
first_certified_trapping=50.5; first_rejected=null;
same_saturation_action=true; global_regularity=false;
singularity_removal=false; full_RefG_pressure_join=false.
This closes the repaired finite-window trapping test. Its direct next
physical target is interior evolution and curvature after trapping in
the same action; full RefG pressure/scale identification remains a
separate unfinished connection. No monograph or publication claim changes.

## 13. Post-trapping curvature: registered finite-window test

CLAIM_ID: W92_PAIRED_INTERIOR_CURVATURE_V1, registered 2026-09-13 before
the extended evolution. Goal: test finite, convergent interior curvature
after section 12's resolved trapping, through the fixed endpoint t=60.
The missing readout is the full dynamical curvature of this saturation
action; Einstein-only source substitutions are unsuitable for that task.

TYPE / MODEL_VERSION / ASSUMPTIONS: conditional numerical evidence for
the same spherical action, canonical complex scalar, initial packet,
harmonic gauge and repaired evolution operators of sections 8-12.
DOMAIN / CONVENTIONS: dimensionless 0<=t<=60, the same positive A,L,q
chart and allowed action branch, curvature diagnostics on r<=80 with
the outer four grid cells excluded. Signed Lorentzian contractions are
retained. FREEDOM_LEDGER: no new physical parameter, source, projection
or smoothing. Only diagnostic readouts and the endpoint change.
DEPENDENCIES: section 12's trapping certificate and section 11's paired
discretization. BENCHMARK: reproduce the overlapping t=28 and t=51.75
states and independently test the metric curvature below.

METHOD / CROSSCHECK: rerun h=.1,.05,.025 at R=120 plus the same fine
half-step and R=160 controls. Keep .25-spaced samples from the initial
slice. Compute curvature both from the angular action equation and from
the evolving metric. Exact vacuum, FLRW, Einstein, boost and regular-centre
checks precede evolution; static metric and contracting constant-potential
controls test the discrete reconstruction.

RESIDUAL / ERROR_BOUND / VALIDITY_HEALTH: all section 12 evolution and
trapping thresholds stay unchanged. Each new metric/action R2, R4 and
K maximum discrepancy is normalized by the maximum action readout or
the fixed dimensional floor ell^-2 (R2,R4), ell^-4 (K). Require fine
error<.005 and (fine<1e-6 or fine/middle<.6), at every sampled prefix.
The central and maximum-absolute R4,K waveforms use the existing
refinement rule (middle/fine difference<1e-4 or decay ratio<.6), and
half-step/domain differences<1e-3, with those same dimensional floors.
The two metric-time probes eps=1e-4 and eps/2 must agree within 1e-4
in all five runs. These fixed floors avoid normalization by an empty
centre's vanishing initial curvature; they are not fitted to residuals.

PASS_CONDITION: an unbroken accepted curvature prefix reaches beyond
t=51.75 with a trapping certificate and all prerequisite/decision checks
passing. Record its actual endpoint separately from completion of t=60.
FAIL_CONDITION / FALSIFIER: a nonfinite curvature, failed refinement,
metric/action disagreement or failed probe limits this new certificate;
an evolution guard limits the underlying solution. Report first rejected
and last accepted prefixes. A finite numerical failure does not identify
a physical singularity. A separate base-evolution certificate is recomputed
on retained samples; a curvature-only gate failure preserves trapping
already certified there or in section 12. A probe exception stops this
run before retaining its failing sample.
BRANCHES: paired saturation branch only. OBSERVABLE_MAP: curvature
scalars of the same physical metric, alongside existing masses, clocks,
charge radius and null expansions. FORWARD_MODEL / DATA_ROLE /
IDENTIFIABILITY: N/A; this is not an observational fit or uniqueness test.
CLOSURE_FLAGS: only finite-window posttrapping_curvature may close;
global_regularity, singularity_removal and full_RefG_pressure_join stay false.
FILES: this report, its verifier and the W92 diagnostic index only.
PROVENANCE: the verifier and both old engines are hashed at launch/exit;
all numerical output is stdout. No new data-file collection is created.
STOP: the five fixed-window runs and their decision, including a failed
gate if encountered. Further interior extension is a separate stage.

Preflight: 65/65 checks pass; the independent base regression passes
74/74. The frozen continuation verifier SHA256 is
`411bdbac4afe3aec3ac49e7c694f64e6e3b528355d2ffd6f9cb5752b6831be24`.

### Dynamical curvature from the same action

Let u=ell^2 z, q=1-u, b=alpha q^2 and C=z(1-3u)/2. The material
components are rho,p_r,p_t,J in an orthonormal radial frame, with

    p_t=A(|P|^2-|D|^2)/2-V, J=sqrt(A) S=A Re(conj(P)D),
    d=2C+b(p_r-rho),
    H=(C+b p_r)^2+(C-b rho)^2-2(b J)^2.

The already-varied radius/angular equation gives

    R2=2z(1-9u+9u^2)+2b(1-6u)(p_r-rho)-4b p_t
       +8 alpha^2 ell^2 q^3(rho p_r-J^2),
    R4=R2+2z-4d, K=R2^2+8H+4z^2.

There is no division by the trapping function F in these readouts.
The 25 exact checks include the original angular action equation, direct
static Hayward curvature, dust FLRW curvature and arbitrary radial boosts.

The independent metric reconstruction uses n=L^-1 partial_t-v partial_r,
e=sqrt(A) partial_r, acceleration a=sqrt(A) partial_r(log L), and

    Kg=v_r+(A_t/L-v A_r)/(2A)+v partial_r(log L),
    R2_metric=2[Kg^2-n(Kg)-e(a)-a^2],
    Hnn=-v_t/L+v v_r-A partial_r(log L),
    Hee=A_r/2-Kg v, Hne=(A_t/L-v A_r)/(2sqrt(A))+v a.

Use R4_metric=R2_metric+2z-4(-Hnn+Hee)/r and
K_metric=R2_metric^2+8(Hnn^2+Hee^2-2Hne^2)/r^2+4z^2.
The connection identity [n,e]=a n+Kg e fixes the curvature sign. A
separate general-metric Christoffel calculation verifies all four
geometric formulas. The shared z is the algebraic metric definition.
A_t comes from the actual evolved mu,v RHS. The time derivative of Kg
is obtained from centred directional probes of the metric expression;
the probes save/restore production guard extrema and never advance or
project the solution. Probe failure is separately labelled. Fourth-order
even/odd parity derivatives and regular H=(A-1)/r^2=k^2-z avoid centre
cancellation and incorrect reflection of odd fields.

### Conditional dynamic-centre bound

At a smooth isotropic centre, J=0, p_t=p_r=p and the mass constraint
gives rho=3z/(2alpha q). The exact identities are

    R2=-2(C+b p), R4=6[z-C-b p],
    K_centre=12[(C+b p)^2+z^2].

For the retained scalar V>=0 implies |p|<=rho. With w=p/rho in [-1,1],
ell^4 K is convex in w. Its endpoint values are 24u^2 and
12u^2(9u^2-12u+5), both at most 24 on 0<=u<=1. Therefore

    K_centre <= 24/ell^4.

This requires a smooth centre and its constraint, but no staticity.
It supplies a conditional dynamic bound; preservation of centre
regularity and off-centre curvature still require the evolution check.

Reproduce:

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --curvature-controls --verbose
    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --paired-interior --verbose

### Completed result: finite post-trapping curvature through t=60

The frozen five-run test returned `PAIRED_VALIDATED_POSTTRAPPING_CURVATURE`:
108/108 checks pass. Each run completed 241 samples on 0<=t<=60;
all 240 successive sampled prefixes pass, with first_rejected=null.
The separately recomputed base-evolution certificate also reaches t=60.
The first two-sample trapping certificate still ends at t=50.5, using
the t=50.25 and t=50.5 samples.

| Run | h | Outer radius | Final minimum F | Final central K |
|---|---:|---:|---:|---:|
| Coarse | .1 | 120 | -.39643516997 | .38104169092 |
| Middle | .05 | 120 | -.39612408548 | .38090692893 |
| Fine | .025 | 120 | -.39604343988 | .38086094209 |
| Fine, half time step | .025 | 120 | -.39604343989 | .38086094209 |
| Fine, enlarged domain | .025 | 160 | -.39604343988 | .38086094209 |

The terminal fine minimum is at r=5.2125, with 275 trapped grid cells.
At that minimum theta_plus=-.14260412093 and theta_minus=-.40886374620;
their product agrees with -4F/r^2 to 6.94e-18. The stated radius locates
the minimum of F, rather than a zero of F.

| Fine-grid model time | Central proper time | Central lapse | Central K | Maximum cell abs(K), r<=80 |
|---|---:|---:|---:|---:|
| 50 | 34.6668645545 | .26401923207 | .29165854000 | .29165695037 |
| 51.75 | 35.1018512886 | .23409474988 | .30825178520 | .30825167026 |
| 54 | 35.5925819127 | .20341821030 | .32699521207 | .33023315635 |
| 60 | 36.6362859755 | .14960062218 | .38086094209 | .38379914964 |

The central readout is a parity extrapolation, tabulated separately from
the cell maximum. At t=60 central R4=1.30182098385 and the cell maximum
abs(R4)=1.30873194028. The sampled fine-history maxima of central K and
the two absolute cell curvature readouts occur at this final time.
The smooth-centre bound is 24/ell^4=1.5 for ell=2; the largest sampled
central K is .38086094209. Its bound assumes the regular isotropic
centre and mass constraint stated above.

| Whole-prefix normalized metric/action discrepancy | Middle | Fine | Fine/middle |
|---|---:|---:|---:|
| R2 | .01159483840 | .00410160563 | .35374410 |
| R4 | .00344027833 | .00112845286 | .32801208 |
| K | .00655349998 | .00202017573 | .30825906 |

These are maximum norm discrepancies with the registered dimensional
floors, not pointwise relative errors. The accuracy gate applies to the
fine result and its middle/fine decrease. Fine-grid radial, regular-metric
and origin residual maxima are 5.72550039e-5, 3.35110029e-6 and
3.51476348e-4. The four curvature-waveform middle/fine discrepancies
(central R4, central K, maximum abs(R4), maximum abs(K)) are
3.70864389e-4, 2.67034680e-4, 2.22557058e-4 and 1.46941215e-4;
each satisfies the registered refinement-decrease rule. Across all
eight monitored waveforms, the largest normalized half-step difference
is 9.82482e-11 and the domain-control difference is 3.62426e-12.
The largest two-time-probe discrepancy over all five runs is
2.07607e-8, below the fixed 1e-4 threshold.

All chart/action and production time-step guards pass. Fine stage minima
are A=.1179909940, face A=.1179823487, L=.1373142901 and q=.3088361771.
The maximum five-run Courant number is .093506 and the frozen-wave RK
number is .254849. The roundoff allowance at u=0 is unchanged; the fine
minimum is -1.05e-14, with no clipping. The maximum fine relative phase
charge drift is 1.99e-13 (7.89e-15 at half step); outer mass remains
129.8971827658 at emitted precision. At t=60 the charge RMS radius is
3.59088044597 and maximum material density is 21.3140696056.

The overlapping retained t=0,28,50,51.75 readouts reproduce the previous
run exactly in emitted floating-point values: all 52 common numeric
entries per case agree. Source and evolution equations are unchanged;
the verifier and both old engines retain their launch hashes. Independent
arithmetic verifies the null-expansion identity, refinement ratios and
sample count. Preflight 65/65 and the base 74/74 regression pass.

Closure: posttrapping_curvature=true; resolved_trapping=true;
validated_prefix_end=60; first_certified_trapping=50.5;
first_rejected=null; same_saturation_action=true;
global_regularity=false; singularity_removal=false;
full_RefG_pressure_join=false.

This stage establishes finite, convergent curvature on the sampled
post-trapping interval of the same postulated saturation action. The
packet continues contracting and its peak curvature is still increasing
at t=60. A global regularity result requires control of the centre's
continued smoothness, off-centre curvature and causal continuation;
the RefG pressure/scale identification remains a separate derivation.
The registered five-run stage is complete; no further time extension
or monograph change is included.

## 14. Does saturation control the full interior source?

CLAIM_ID / MODEL_VERSION: W92_LOCAL_SOURCE_CONTROL_V1, 2026-09-13.
GOAL: decide whether the bound 0<=ell^2 z<1 in the retained spherical
action is sufficient for a source-independent bound on dynamical
off-centre curvature. Section 13 supplies the exact curvature formula
and finite-window numerical evidence; its smooth-centre hypothesis is
not an assumption at every noncentral point.
TYPE / METHOD: exact implication test, a conditional source bound and
a smooth constrained initial-data counterexample family. No new action,
matter coupling, physical parameter or time evolution is introduced.
ASSUMPTIONS / DOMAIN: the same canonical complex scalar with V>=0,
alpha>0, ell>0, positive q, one physical spherical metric and its radial
mass and momentum constraints. Readouts use an orthonormal radial frame;
the PG example uses the normal to its regular initial slice.
FREEDOM_LEDGER: retain alpha=.04, ell=2, M0=2 M_critical;
choose one shell midpoint r0=3 and widths 1/2,1/4,1/8,1/16 before
the numerical crosscheck. Width labels separate initial data, not
successive times of the section 13 packet.
DEPENDENCIES: sections 9 and 13's sourced equations and exact curvature.
PASS / FALSIFIER: verify the source inequalities, on-shell curvature
reduction and initial constraints symbolically. A smooth fixed-total-mass
family with fixed midpoint z and unbounded midpoint K refutes the
source-independent implication; it leaves section 13's fixed-packet
certificate intact. A nonzero constraint or curvature residual rejects
the proposed counterexample. Failed checks leave the decision unresolved.
ERROR_BOUND / CROSSCHECK: bump normalization at 40 and 60 decimal digits
must agree to relative 1e-30; the analytic width limit determines
unboundedness, while the four numerical examples check its readout.
The sufficient source bound is proved by inequalities, not inferred
from these four examples. Existing base and curvature controls are rerun.
OBSERVABLE_MAP / VALIDITY: full metric curvature and local frame source;
a bound in this frame is distinct from global causal continuation.
DATA_ROLE / FORWARD_MODEL / IDENTIFIABILITY: N/A; no observations, fit
or physical uniqueness claim. The shell is neutral scalar initial data,
not a stationary oscillon or a model of particle composition.
CLOSURE_FLAGS: record local_source_criterion and the automatic-bound
decision separately from fixed_packet_blowup, global_regularity,
singularity_removal and full_RefG_pressure_join.
PROVENANCE / FILES: this report, its existing verifier and the W92 index;
all numerical output remains stdout. Baseline verifier SHA256:
`411bdbac4afe3aec3ac49e7c694f64e6e3b528355d2ffd6f9cb5752b6831be24`.
STOP: complete this implication test and the precise remaining source
condition. A new constitutive action or longer evolution is a separate
stage. The intuitive monographs and previous evolution engines stay intact.

### A sufficient local source bound

Define E=alpha ell^2 q^(3/2) rho in the chosen orthonormal frame.
This dimensionless diagnostic combines the local source with the
gravitational response; it adds neither an energy component nor a
constitutive equation. For X=A|P|^2, Y=A|D|^2 and V>=0, the retained
canonical source obeys

    rho=(X+Y)/2+V, p_r=(X+Y)/2-V, p_t=(X-Y)/2-V,
    J^2<=XY, |p_r|,|p_t|,|J|<=rho.

With Delta=rho p_r-J^2, the identities

    rho^2-Delta=V(X+Y+2V)+J^2,
    rho^2+Delta=(X^2+Y^2)/2+(XY-J^2)+V(X+Y)

give |Delta|<=rho^2. In particular the angular curvature equation
contains 8 alpha^2 ell^2 q^3 Delta as well as linear source terms.
Let B(E)=5/2+24E+8E^2. The exact source inequalities imply

    |ell^2 R2| <= B(E),
    |ell^2 R4| <= B(E)+10+8E,
    |ell^4 K| <= B(E)^2+16(1+E)^2+16E^2+4.

For completeness, |u(1-3u)/2|<=1 and
|2u(1-9u+9u^2)|<=5/2 on 0<=u<=1. The normalized Hessian components
obey |ell^2 h_nn|,|ell^2 h_ee|<=1+E and |ell^2 h_ne|<=E.
Here h_ab=R_;ab/R in the orthonormal radial frame, as in section 13.
These component inequalities and the triangle inequality prove the
displayed bounds. They are conservative sufficient bounds, not sharp
predictions for the evolved packet.

At a smooth centre the already-established mass constraint gives
E_c=(3/2)u sqrt(1-u), with

    1/3-E_c^2=(3u-2)^2(3u+1)/12>=0.

Thus the centre automatically meets this sufficient source criterion.
Away from the centre, the same radial constraint fixes an enclosed
integral M; it does not equate the local rho to 3M/r^3.

### Fixed-mass smooth-shell implication test

Let b(x)=exp[-1/(1-x^2)] for |x|<1 and zero elsewhere,
I=integral b(x)^2 dx, g=b^2/I and G(x)=integral_{-infinity}^x g(y)dy.
For 0<w<r0 use the smooth initial data

    M_w(r)=M0 G((r-r0)/w), rho_w=M_w'/r^2,
    psi=D=0, P=sqrt(2rho_w), J=V=0, p_r=p_t=rho_w,
    A=L=1, v=r sqrt(z), k=sqrt(z), F=1-r^2 z,
    z=2alpha M_w/(r^3+2alpha ell^2 M_w).

Using g=b^2/I makes P smooth at both shell edges. The central cavity
is flat, each finite-width source is smooth, and the outer generalized
mass is exactly M0. The same mass constraint reads M_w'=r^2 rho_w;
the momentum constraint gives K^r_r=v_r. Differentiating z yields
v v_r=-r C+alpha r q^2 rho_w, so the geometric radial Hessian agrees
with the sourced equation. The regular-metric equation gives A_t=0
on this slice; the k equation supplies its normal-normal component.
These are dynamical initial data, with no static-support assumption.

At r=r0 symmetry gives M_w=M0/2 for every width. Consequently z and q
are fixed there while rho_w=M0 g(0)/(w r0^2). The full source curvature is

    R2=2z(1-9u+9u^2)-4alpha q^2 rho_w
       +8alpha^2 ell^2 q^3 rho_w^2,
    K=R2^2+16C^2+16alpha^2 q^4 rho_w^2+4z^2,
    limit_(w->0) w^4 K
      =64alpha^4 ell^4 q^6 [M0 g(0)/r0^2]^4 > 0.

The analytic limit tests a uniform cap across separate smooth sources
of the same total mass. Every finite-width member has finite curvature;
this family does not evolve the section 13 packet toward a singularity.

### Completed source-control decision

The standalone `--source-control` test passes 66/66 checks and returns
`AUTOMATIC_INTERIOR_CURVATURE_CAP_EXCLUDED`. The analytic fixed-mass
family disproves a universal off-centre curvature cap inferred solely
from z saturation; the conditional local-source criterion passes.

For M0=129.9038105677, r0=3, alpha=.04 and ell=2, every example has
q=.565035482652, u=.434964517348 and F(r0)=.0213298359673. The PG
spatial metric remains A=1 through both signs of F. The table evaluates
the same midpoint of each distinct initial configuration:

| Shell width w | Local rho(r0) | Weighted source E(r0) | ell^4 K(r0) |
|---|---:|---:|---:|
| .5 | 29.3553759443 | 1.99490037057 | 651.079124677 |
| .25 | 58.7107518886 | 3.98980074114 | 13208.6432405 |
| .125 | 117.421503777 | 7.97960148227 | 235166.871654 |
| .0625 | 234.843007555 | 15.9592029645 | 3956553.33807 |

The total mass and midpoint response stay fixed, while the local source
grows as 1/w. The exact positive coefficient of w^-4 establishes the
absence of a universal cap; the table is its finite numerical check.
The full curvature remains finite in every listed configuration and
satisfies the derived E-dependent bounds. The numeral 24 is the earlier
smooth-centre bound for ell^4 K, with different local hypotheses.

All initial-constraint and source-curvature symbolic residuals vanish.
The mixed PG check independently combines the physical mass flux and k
evolution to recover A_t=0. Independently, the scalar equation gives
S_t=rho_r on this slice. Differentiating the extrinsic-curvature
constraint in the metric readout then gives

    R2_metric=-2[C+r C_r+b rho+r b_r rho], b=alpha q^2,
    r z_r=2alpha q^2 rho-3zq.

This reproduces the full kinetic R2, including its quadratic-density
term, with zero symbolic residual in the same Python test. Omitting
that term is detected by a negative control. The bump normalization
relative discrepancy is 1.90626e-42; midpoint symmetry and total-mass
quadratures also pass their registered accuracy tests.
The base 74/74 and existing curvature preflight 65/65 regressions also
pass. An AST comparison confirms that all previous computational
functions are unchanged; only the new check function and CLI dispatch
are added. Three incompatible CLI combinations are rejected with exit 2.
Both old engine hashes remain unchanged. Tested verifier SHA256:
`a59d1e5d48ce54c93d48ad4f8fbaec8e403d3aaa109a51099c5a01c99af82ff0`.

Closure: local_source_criterion=true; automatic_uniform_cap_excluded=true;
uniform_cap_from_saturation_alone=false; smooth_fixed_mass_family=true;
bounded_source_derived=false; fixed_packet_blowup=false;
global_regularity=false; singularity_removal=false;
full_RefG_pressure_join=false.

The missing result is dynamical control of the local source along the
evolved packet. The existing h(z) bounds the enclosed-mass response;
its angular equation also depends on local pressure, gradients and
the stress determinant. The E bound supplies one sufficient target,
which may depend on the initial data. Section 14 tests a universal cap
over different initial data and establishes neither finite-time blow-up
of the fixed packet nor the necessity of changing its action. A modified
source-response law is one possible route, while the existing dynamics
must first be checked for feedback. RefG's intuitive section 1.5 calls
for that joint matter/environment response; section 15 derives its
actual local growth budget in the retained candidate. This correction
narrows the earlier interpretation without changing any section 14
equation, numerical result or counterexample.

Reproduce without time evolution or generated files:

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --source-control --verbose

## 15. Existing-action local feedback: a directional source test

CLAIM_ID / MODEL_VERSION: W92_LOCAL_DYNAMIC_SOURCE_BUDGET_V1, 2026-09-13.
GOAL: derive the local energy-growth and saturation-feedback balance
from the retained action, then determine its initial sign in section
14's four already-fixed smooth sources. This directly tests whether
feedback is present before introducing a new constitutive law.
TYPE / METHOD: exact conservation and field-equation identities, with
bounded numerical evaluation of initial directional derivatives.
ASSUMPTIONS / DOMAIN: the same canonical complex scalar, nonnegative
sextic potential, spherical saturation action and positive A,L,q branch.
Use its orthonormal normal n and outward radial vector e. Logarithmic
rates are evaluated only where rho>0 and k>0; the full unlogged equation
defines the other regular limits. No candidate P(X) replacement is adopted.
FREEDOM_LEDGER / DATA_ROLE: unchanged alpha=.04, ell=2, M0=2M_critical,
r0=3 and widths .5,.25,.125,.0625. These are the previous counterexample
initial slices, not new fitted states or the earlier charged packet.
There are no observations, parameter scans or time-evolution runs.
DEPENDENCIES: sections 9, 13 and 14, plus the existing scalar equation;
the intuitive section 1.5 identifies the intended reciprocal mechanism
but supplies no additional equation. W69's potential-only response and
the W92 amplitude-only coupling leave this zero-amplitude initial slice
unchanged; neither is inserted as a substitute for its kinetic source.
PASS / FALSIFIER: obtain zero exact residuals for energy conservation,
mass transport, the q/E chain rules and the PG initial response.
Evaluate both n(E) and n(Kretschmann), reporting the actual signs.
An inconsistent conservation equation or directional derivative rejects
the claimed response. Sign changes among the fixed examples are results,
not reasons to alter them. No instantaneous sign closes a stability gate.
CROSSCHECK / ERROR_BOUND: derive energy transport independently from
the scalar equation; compare analytical E and curvature derivatives with
centred directional probes eps=1e-6 and 5e-7, each with normalized error
<1e-5. These probes check the readout derivative and do not advance a
solution. Rerun the base, curvature and source-control regressions.
CONVENTIONS / OBSERVABLE_MAP: n=(partial_t-Lv partial_r)/L is the
normal proper-time derivative, not a fixed-radius coordinate derivative.
J=T(n,e)=sqrt(A)S; positive outward energy flux has the opposite sign.
VALIDITY / CLOSURE_FLAGS: initial_feedback_demonstrated and initial
curvature_reduction are separate from persistent_regulation, stability,
fixed_packet_continuation, global_regularity, singularity_removal and
full_RefG_pressure_join. Weighted source E is a diagnostic, not P_F.
FORWARD_MODEL / IDENTIFIABILITY: N/A; this is an internal dynamical test.
PROVENANCE / FILES: only this report, its verifier and the W92 index.
The previous verifier hash is
`a59d1e5d48ce54c93d48ad4f8fbaec8e403d3aaa109a51099c5a01c99af82ff0`.
STOP: finish the exact budget, four directional responses and independent
checks. Neither a new action nor a further collapse interval is opened.

### Action-derived local balance

Write mu=M/r^3, u=ell^2 z, q=1-u and E=alpha ell^2 q^(3/2) rho.
The mass-response relation is q=(1+2 alpha ell^2 mu)^(-1).
Let k=v/r and K_r=K^r_r in the existing extrinsic-curvature convention,
e=sqrt(A) partial_r and a=sqrt(A) partial_r ln L. Splitting the complex
scalar into two real components, pi=n(psi) and chi=e(psi), its equation is

    n(pi) = e(chi) + (a+2 sqrt(A)/r) chi + (K_r+2k) pi - grad_psi V,
    n(chi) = e(pi) + a pi + K_r chi.

Contracting with pi and chi, including n(V), yields the exact energy budget

    n(rho) = e(J) + 2(a+sqrt(A)/r)J
             + K_r(rho+p_r) + 2k(rho+p_t).

The potential-force terms cancel in this balance. The radial and temporal
mass equations give, after the normal-frame advective correction,

    n(mu) = k(3mu+p_r) + A S/r,
    n(q) = -2 alpha ell^2 q^2 n(mu),
    n(E) = alpha ell^2 q^(3/2)
           [n(rho) - 3 alpha ell^2 q rho n(mu)].

The bracket separates increasing material energy density from the
decreasing geometric response factor. Both are supplied by the retained
action. E controls the sufficient curvature estimate of section 14;
its decrease has a precise geometric meaning without identifying q
with RefG's foundation pressure.

### Response of the four fixed initial slices

Section 14's smooth kinetic shells have A=L=1, psi=D=J=V=0 and
p_r=p_t=rho on the initial slice. Their inward normal flow has k=sqrt(z)>0.
With C=z(1-3u)/2, the constraint gives K_r=(-C+alpha q^2 rho)/k.
The scalar equation directly yields n(P)=(partial_r v+2k)P and hence
n(rho)=2rho(K_r+2k). The two competing logarithmic rates are therefore

    Gamma_rho = n(ln rho) = 3k(1+u) + 2 alpha q^2 rho/k > 0,
    Gamma_feedback = -3 alpha ell^2 q k(rho+3mu),
    Gamma_E = n(ln E) = Gamma_rho + Gamma_feedback
            = (3/2)k(2-u) + alpha q rho(2-5u)/k.

For u>2/5, the weighted source initially decreases exactly when

    rho > rho_turn = 3z(2-u) / [2 alpha q(5u-2)].

The original, unchanged midpoint has u=.4349645173478661 and
rho_turn=64.60647291443804. All rates below use the model units and
the future normal proper-time derivative at that midpoint.
Kretschmann curvature is denoted by Kcal, distinct from K_r.

| Shell width | rho | n(rho) | n(ln E) | n(Kcal) |
|---:|---:|---:|---:|---:|
| .5 | 29.35537594 | 108.41741697 | +.4223854710 | +79.99025264 |
| .25 | 58.71075189 | 350.32516147 | +.0706436712 | +439.22308913 |
| .125 | 117.42150378 | 1234.61163307 | -.6328399285 | -33903.78325311 |
| .0625 | 234.84300755 | 4605.06850669 | -2.0398071278 | -1965441.93975555 |

In the two strongest concentrations the geometric feedback exceeds
the density-growth term: local density increases while both E and
Kretschmann curvature initially decrease.

The curvature rates follow from the full on-shell expression in section
14, not solely from the sufficient E estimate. At this initial slice,
n(V)=n(|D|^2)=0 and the curvature's first J derivative vanishes at J=0.
Thus its complete first variation reduces to

    n(z) = 2 alpha q^2 k(rho+3mu),
    n(Kcal) = (partial_rho Kcal_kin)n(rho)
              + (partial_z Kcal_kin)n(z).

At fixed z, the leading high-density term is exactly

    n(Kcal) = [256 alpha^5 ell^4 q^7(2-5u)/sqrt(z)] rho^5
              + O(rho^4).

Its sign confirms the same initial curvature-reducing response for
sufficiently concentrated kinetic PG data with u>2/5.

### Verification and closure

`--source-budget --verbose` passes **104/104** checks, including the
66 section 14 prerequisites. The canonical energy balance was also
derived independently from the scalar equation with the same action
and conventions. Analytical E and curvature rates agree with centred
directional readout probes at both registered step sizes; maximum
normalized error is **1.98e-9**, below 1e-5. All probe states satisfy
rho>0 and 0<q<1. The separate base, curvature and source-control
regressions pass 74/74, 65/65 and 66/66, respectively.

The result establishes an instantaneous local feedback in the existing
candidate. The four rows are distinct initial slices. Flux starts to
develop according to n(J)=partial_r rho on this PG slice, so the initial
kinetic reduction supplies an initial derivative, not a closed trajectory.
The earlier evolving packet and the full RefG pressure/scale connection
remain separate targets. The next decisive physical question is whether
this feedback controls curvature along that fixed packet after trapping.

    local_budget_derived=true; initial_feedback_demonstrated=true;
    initial_curvature_reduction=true; existing_action=true;
    modified_action=false; time_evolution_performed=false;
    persistent_regulation=false; fixed_packet_continuation=false;
    stability=false; global_regularity=false;
    singularity_removal=false; full_RefG_pressure_join=false.

These local results correct section 14's earlier inference that the
failure of a universal initial-data cap required a new constitutive law.
The unchanged action already has the directional feedback just derived.

Reproduce without time evolution or generated files:

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --source-budget --verbose

Tested verifier SHA-256:
`13888ba6635fccfc9bad476a9649dd168a59d09e024066153f24e127c039eb14`.
Only the new budget function and its isolated CLI entry were added;
previous computational definitions and both population/evolution
engines are unchanged. No monograph, Git rule or private-note file changed.

## 16. Same-packet feedback during post-trapping evolution

CLAIM_ID / MODEL_VERSION: W92_PAIRED_FEEDBACK_EVOLUTION_V1, 2026-09-13,
registered before the new evolution. GOAL: test section 15's general
local energy/response balance along the original collapsing packet and
measure the actual curvature trend beyond t=60. The instantaneous
kinetic-shell threshold is replaced by its full flux/compression/response
budget, with no change to the action or matter dynamics.
TYPE: conditional numerical evidence on a fixed finite interval.
ASSUMPTIONS / DEPENDENCIES: sections 11-13's repaired paired discretization,
canonical complex scalar, spherical saturation action, harmonic clock,
initial packet and admissible positive A,L,q branch; section 15's exact
local balance. The previous RefG pressure/scale join retains its status.
DOMAIN / CONVENTIONS: 0<=t<=70, samples every .25, monitored r<=80 excluding
the outer four cells. The derivative n=L^-1 partial_t-v partial_r is along
the future normal; E=alpha ell^2 q^(3/2) rho and J=sqrt(A)S.
FREEDOM_LEDGER: the five existing runs h=.1,.05,.025 at R=120, the fine
half-step run and fine R=160 run. The endpoint is fixed at 70 before
inspection; no automatic extension or retuned initial state is allowed.
METHOD / CROSSCHECK: compute E_t analytically from the actual evolution
RHS, subtract radial advection, and independently reconstruct n(E) from
energy conservation and mass transport. Retain the existing independent
metric/action curvature comparison and all previous evolution gates.
ERROR_BOUND: normalize the n(E) discrepancy by the largest sum of absolute
flux/compression/response contributions or the fixed dimensional floor
ell^-1. Require fine error<.005 and (fine<1e-6 or fine/middle<.6) at every
sampled prefix. Central E, maximum E and central n(E) use the existing
waveform refinement and half-step/domain budgets, with fixed floors 1
for E and ell^-1 for its rate. All section 13 tolerances remain unchanged.
BENCHMARK: reproduce the recorded t=60 curvature, F, density, radius and
central proper-time readouts; verify zero-field and constant-core budgets.
PASS_CONDITION: all required gates pass on an unbroken prefix beyond 60.
Report the accepted endpoint independently of completion of t=70.
FAIL_CONDITION / FALSIFIER: the first failed constraint, convergence,
curvature, budget or chart/time-step guard limits the corresponding
certificate. Preserve a separate base/curvature certificate when only
the new budget fails. Numerical failure alone does not identify a
physical singularity. NaN and incomplete-time controls must be rejected.
OBSERVABLE_MAP: central and maximum E, central proper time, full curvature
histories, and the three local budget terms at the centre and at the
sampled maximum-|K| location. A negative local n(E) and a declining
maximum curvature are separate measurements. Curvature turning is a
reported classification, not a requirement for regularity or a fitted
stopping condition. FORWARD_MODEL / DATA_ROLE / IDENTIFIABILITY: N/A;
there are no observations, fitted parameters or uniqueness claims.
CLOSURE_FLAGS: finite-window feedback validation only; global regularity,
singularity removal, persistent regulation and full RefG pressure join
remain false. FILES: this report, its verifier and the W92 index only.
PROVENANCE: source hashes at launch/exit; results to stdout. No generated
dataset, monograph edit or Git-rule change. STOP: finish the five frozen
runs and classify their accepted prefixes; do not open another interval.

### Runtime balance and independent readout

The nonlogarithmic budget used here applies to the complete evolving
scalar source, including spatial gradients and potential energy. With
f=alpha ell^2 q^(3/2) and a=sqrt(A) partial_r ln L, its three terms are

    F_E = f [sqrt(A) partial_r J + 2(a+sqrt(A)/r)J],
    C_E = f [K_r(rho+p_r) + 2k(rho+p_t)],
    R_E = -3 alpha ell^2 q f rho [k(3mu+p_r)+A S/r],
    n(E) = F_E + C_E + R_E.

The direct check instead differentiates rho=A(|P|^2+|D|^2)/2+V
using the actual evolution RHS, including A_t and D_t, then forms

    E_t = f [rho_t - 3 alpha ell^2 q rho mu_t],
    n(E)_RHS = E_t/L - v partial_r E.

The two routes share the action and current numerical state, but use
different energy-transport reconstructions. Their difference measures
the discretized budget error; finite-difference product rules are not
assumed exact. The fixed norm floor is 1/ell. The sum of the absolute
three contributions supplies the other normalization scale, avoiding
division by a nearly cancelling net rate. Odd radial parity is used
for J. No logarithm or division by rho is needed near vacuum.

The peak-location fields are descriptive: grid maxima can exchange
locations. Central E, maximum E and central n(E) have the registered
waveform controls. The final net change in maximum absolute curvature
is evaluated over [max(60,t_accepted-1),t_accepted]; a resolved sign
requires agreement of all five runs and a fine change larger than
three times the largest control difference in that change. This is an
interval trend, rather than a turning-point or stability certificate.

Preflight: 71/71 feedback/curvature controls and 104/104 source-budget
checks pass; the unchanged base regression passes 74/74. Three mixed-CLI
negative controls are rejected. Frozen evolution verifier SHA-256:
`06d27375a9496d003d9ed4f24d9b37cd09f69bf7b39c5cbc20fb353911a24143`.

### Completed result: certified feedback and curvature through t=62.5

All five runs complete 281 samples on 0<=t<=70 without a chart, action
or production time-step stop. The unbroken combined feedback/curvature
certificate reaches **t=62.5**; its first rejection is **t=62.75**.
The independently retained base-evolution certificate reaches t=70,
with no rejected prefix. Resolved future trapping is preserved, with
the original first certificate at t=50.5.

The driver returns `PAIRED_VALIDATED_FEEDBACK_EVOLUTION` for its accepted
prefix and **128/130** checks overall. It exits with code 1 because the
requested full t=70 interval fails two terminal curvature-accuracy gates:
`curvature_metric_R2_error` and `curvature_metric_K_error`. The frozen
tolerances are unchanged. All six t=60 regression checks, source-hash
checks and synthetic rejection controls pass.

| Whole-prefix normalized discrepancy | Fine at 62.5 | Fine at 62.75 | Fine at 70 | Required fine ceiling |
|---|---:|---:|---:|---:|
| Orbit R2, metric versus action | .00491340 | .00515407 | .02152305 | .005 |
| Four-dimensional Ricci scalar | .00126357 | .00131976 | .00495170 | .005 |
| Kretschmann scalar | .00248659 | .00259425 | .01090738 | .005 |
| Local E growth budget | .00016028 | .00016309 | .00136327 | .005 |

These are the registered normed discrepancies, not pointwise relative
errors. At the first rejected sample the R2 fine/middle ratio is .25176:
refinement still improves the reconstruction, while its absolute budget
has been exceeded. The feedback budget's ratio is .06790 over the
accepted prefix and .08364 over the full run. All feedback waveform,
half-step and enlarged-domain gates pass even at the requested endpoint.

### What the validated interval establishes

The centre shows a sustained sampled decrease of weighted source E:
n(E)<0 at all eleven samples from 60 through 62.5 in every run. Central
material density increases between those endpoints. Both central and
maximum curvature continue increasing.

| Fine-grid quantity | t=60 | t=62.5 |
|---|---:|---:|
| Central proper time | 36.63628598 | 36.99040029 |
| Central density | 20.87389476 | 21.68490523 |
| Central weighted source E | .57622919 | .57530473 |
| Central Kretschmann scalar | .38086094 | .39369754 |
| Maximum cell abs(K), r<=80 | .38379915 | .40092857 |
| Maximum weighted source E | .58530012 | .59009582 |
| Radius of maximum cell abs(K) | .9375 | 1.0625 |
| Minimum F | -.39604344 | -.45365565 |

At the accepted endpoint the two locations have different balances:

| Local proper-time contribution at t=62.5 | Centre | Curvature-maximum cell, r=1.0625 |
|---|---:|---:|
| Flux F_E | -.24295401 | -.21674399 |
| Compression C_E | +.28724691 | +.30556073 |
| Response R_E | -.04640225 | -.07333448 |
| Sum of the three contributions | -.00210935 | +.01548226 |
| Direct-RHS n(E) | -.00214503 | +.01548280 |
| Direct-RHS n(rho) | +1.66763215 | +3.39047194 |

The small sum/direct differences are retained as discretization errors.
At both locations the response contribution is negative. Together with
energy redistribution it exceeds compression at the centre; at the
curvature maximum, compression still exceeds the two reducing terms.
The peak-cell values describe the sampled location rather than a tracked
material element. Their signs agree across all five runs at this time.

Maximum absolute curvature rises by .00683549412 over the last accepted
unit, 61.5<=t<=62.5. Every run gives a rise, and the registered three-times
control-spread margin is .00019517934. Thus the accepted interval shows
local weighted-source suppression but continued growth of peak curvature.
The kinetic-shell sign of section 15 is consequently not a universal
sign rule for the complete evolving packet.

### Accuracy boundary and handoff

The raw t=70 fine values are central K=.40703195 and maximum abs(K)=.46598712.
They lie outside this stage's curvature certificate. The fine chart
minima across the run remain positive (A=.04069048, q=.27121269,
L=.08313606), and the base evolution continues to pass. These facts
distinguish the curvature reconstruction's accuracy boundary from a
singular physical endpoint or a failed local energy balance.

The next bounded task is to locate the metric/action R2 discrepancy
spatially at 62.5--62.75 and test the relevant derivative/resolution error
on that fixed interval. This targets the first failed gate before any
further time extension. The present result establishes the same-action
feedback during finite evolution; global control and the full RefG
pressure/scale derivation retain their separate status.

    feedback_evolution=true; validated_feedback_curvature_end=62.5;
    first_rejected=62.75; base_evolution_validated_end=70;
    requested_end=70; completed_all_five_runs=true;
    resolved_trapping=true; peak_curvature_trend=increasing;
    persistent_regulation=false; global_regularity=false;
    singularity_removal=false; full_RefG_pressure_join=false.

Reproduce the fixed five-run stage (stdout only):

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --feedback-evolution --verbose

Preflight without collapse evolution:

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --feedback-controls --verbose

Only the budget readout, isolated stage controls and finite-window
driver were extended. Both evolution RHS methods, initial packet,
curvature formula, paired operators and legacy engines are unchanged;
the frozen source hashes agree at launch and exit. No new file,
monograph, private-note or Git-rule change is included.

## 17. Fixed-window curvature-error localization

### Contract frozen before the two replays

This stage locates the first metric/action orbit-curvature discrepancy at
t=62.5 and 62.75. It replays only h=.025 and h=.0125, R=120,
Courant=.1, through t=62.75, with the original packet, saturation action,
harmonic clock, gravity and paired-matter RHS unchanged. The stop is a
localized numerical diagnosis; no later evolution window is authorized
by this check. The files are this report, its existing verifier and the
W92 diagnostic index. Results go to stdout without new datasets.

At both fixed times, the same state supplies D4 and D6 metric
reconstructions, the metric-only divergence form, and directional time
probes epsilon=1e-4 and 5e-5. All use r<=80 (excluding the last six cells)
and the original scale max(sup|R2_action|,ell^-2). The original D4
absolute gate .005 remains the acceptance test. Variant reconstructions
are diagnostics and cannot replace that gate after inspecting results.
The original sampled diagnostics are retained every .25 time unit;
this two-grid diagnostic does not replace the five-run certificate.

The metric-only identity used to separate product-rule truncation is

    R2 = -2 sqrt(A)/L [ d_t(Kg/sqrt(A))
                       + d_r(L acc - L v Kg/sqrt(A)) ].

The local audit records the maximum residual's radius, its five expanded
curvature terms, their cancellation, lapse, A and q. It also isolates
the constraint-amplified difference delta=Kg-(v_r-alpha*r*q^2*S):

    R2[Kg]-R2[Kg-delta]
      = 2 [2 (Kg-delta) delta + delta^2 - n(delta)].

This last decomposition uses an action equation and is solely an error
diagnostic. It is not an independent curvature certificate.

Preflight requires parity/polynomial derivative controls, constant-core
and manufactured metric identities, time-probe and guard-restoration
checks. Nonfinite values or any preflight failure stop the replay.
All source hashes must match launch and exit. Endpoint reproduction on
h=.025 is checked against section 16 before interpreting the finer run.

A substantial D4/D6 or expanded/divergence difference identifies readout
sensitivity. Small same-state differences with improvement on the finer
evolution grid identify accumulated spatial-discretization sensitivity.
The term audit locates any constraint or cancellation amplification;
convergence alone does not identify a unique defective stencil.
Failure of the .005 gate is an accuracy limitation, not a physical
singularity test. Full RefG pressure joining and global regularity retain
their existing status.

The preflight passes 93/93 checks, including a nonzero manufactured
constraint defect and unchanged-state check. The frozen verifier SHA-256
is `07d40adc7edff2e1c1d9d0676694acb1c6767ef7595e4ed0afd193508c74b85c`.
The two engine hashes remain those recorded in section 16. A read-only
AST comparison confirms the original initial-state factory, evolution
RHS, geometry and paired operators are unchanged.

Reproduce only this fixed-window diagnosis (two concurrent workers,
stdout results and stderr progress; no generated files):

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --curvature-localization

Controls only:

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --localization-controls

### Result: localized finite-resolution error (2026-09-14)

`CURVATURE_LOCALIZATION_COMPUTED`: 104/104 control and reproduction
checks pass. Both runs complete all 252 samples through t=62.75.
The h=.025 replay takes 372.604 s and h=.0125 takes 1498.706 s;
the complete concurrent stage takes 1523.087 s. All three source hashes
agree at preflight, worker entry and exit. The previous h=.025 R2
errors at both target times reproduce exactly. Separate regressions
pass 74/74 base and 104/104 source-budget checks.

| t | Original D4 error, h=.025 | Original D4 error, h=.0125 | Finer/fine | Radius of maximum residual, fine / finer |
|---|---:|---:|---:|---:|
| 62.5 | .00491340010 | .00129042828 | .262634 | 2.98750 / 2.98125 |
| 62.75 | .00515406671 | .00133836425 | .259672 | 2.96250 / 2.95625 |

These are normalized sup errors, with the preregistered action-curvature
scale (at 62.75: .3500968918 and .3502950397). The absolute residuals at
the worst cells are respectively -.00180442274 and -.00046882236.
The smooth local residual maximum lies near r=3, well away from both
the centre and the outer numerical boundary. Refinement reduces the
error by factors 3.81 and 3.85, corresponding to observed orders 1.929
and 1.945. The finer run's original D4 absolute-error component passes
at every sampled time through 62.75; the old h=.025 component first
fails at 62.75, as before.

The fixed-state controls at the first formerly rejected time separate
the possible readout explanations:

| Diagnostic at t=62.75 | h=.025 | h=.0125 |
|---|---:|---:|
| D4 expanded metric/action error | .00515406671 | .00133836425 |
| D6 expanded metric/action error | .00512215901 | .00133874511 |
| D4 divergence metric/action error | .00515382048 | .00133829391 |
| D6 divergence metric/action error | .00512169669 | .00133873483 |
| sup(D6-D4) / original error norm | .0471020 | .0120518 |
| sup(divergence-D4) / original error norm | .00368347 | .000882404 |
| Error after diagnostic constraint subtraction | .00616044931 | .00154497828 |

Changing only the readout stencil leaves the original grid above .005.
The divergence form has an even smaller effect. The directional-probe
sensitivity over both times and grids is at most 7.23e-8. At the worst
cells the sum of absolute R2 terms divided by the local curvature scale
is only 1.62--1.64. Thus neither a missing time-derivative factor nor
catastrophic floating-point cancellation explains this discrepancy.

Constraint amplification contributes locally but its subtraction raises
the global residual norm by 15--21 percent. It is not a repair for the
independent curvature test. Both diagnostic decomposition identities
have residuals below 4.3e-15. At the finer worst cell at 62.75,
L=.13264178, A=.14056996 and q=.51163150; the amplified constraint
difference in Kg is 9.43846e-6.

The result points to approximately second-order finite-resolution error
in the evolved geometry/source state, rather than the final curvature
readout. The retained metric transport and face/cell mappings contain
second-order operations. The paired matter derivative and independent
readout already have higher-order controls. The two new runs co-refine
h and the RK step; the spatial interpretation is also supported by
section 16's half-step physical-waveform checks (at 62.75 the maximum-K
change under that half step is 1.33e-12). This localizes the numerical
problem without identifying one particular evolution stencil uniquely.

### Physical readout and precise handoff

On the finer grid the central weighted source decreases from .57625051
at t=60 to .57527308 at 62.75, while maximum absolute K increases from
.38378670 to .40265105. The finite-window feedback result therefore
survives refinement with continued peak-curvature growth. Across the
finer run, the minimum cell A, lapse and q are .08755401, .11817762 and
.29802155. The maximum Courant number is .09134007 and the paired-wave
RK number .24894723. Relative charge drift is 7.44e-15; the exterior
mass readout is unchanged. The maximum feedback-budget error is
4.00836e-5.

The next bounded repair should target the retained metric transport and
face/cell consistency, with parity, constant-core, mass/charge and action
identities preserved. Its decision test is this same 62.5--62.75 window
on the original h=.025 grid, against the finer reference above. Merely
substituting the constraint-based curvature or repeatedly shrinking h
does not resolve that implementation choice. No later time window or
new physical action is opened in this stage.

The two-grid diagnostic passes; the previous five-run curvature/feedback
certificate remains at 62.5 because new finer step/domain controls were
not run. Global regularity, singularity removal and the full RefG
pressure/scale join retain their separate open status.

    curvature_error_localized=true; original_grid_reproduced=true;
    finer_D4_component_passes_through=62.75;
    five_run_certificate_extended=false; changed_action=false;
    changed_evolution_RHS=false; changed_original_threshold=false;
    unique_defective_stencil_identified=false; singularity_removal=false.

## 18. Higher-order interior metric operators, fixed-window repair

### Contract before nonlinear evolution

The decision is whether a coherent upgrade of metric numerics resolves
section 17's independent-curvature discrepancy on the original h=.025
grid. This is a numerical implementation test of the same saturation
action, harmonic clock and charged packet. The original solver remains
available unchanged. Files are this report, its verifier and the W92
index; output is stdout only. The stop remains t=62.75.

The candidate uses fourth-order parity interpolation between metric
faces and cells; the existing sixth-order staggered gradient and its
nodal weighted-adjoint radial divergence; and fourth-order shift/lapse
derivatives. The outermost six entries retain the original closure.
Initial matter and the polar initial-geometry construction stay fixed.
The latter retains second-order numerical ingredients, so an interior
operator upgrade does not assert globally fourth-order evolution.

Preflight requires even/odd polynomial and centre tests, compact-support
gauge adjointness, unchanged paired-matter charge balance, constant-core
clock/curvature tests, manufactured nonlinear metric-RHS convergence,
and frozen gauge spectrum controls against the legacy boundary. The
zero-Jordan chain G(1)=0, G(r^2)=2r, D(r)=3 is checked explicitly;
near-zero eigenvalue splitting already present in the old open closure
is separated from resolved nonzero-frequency instability. A four-unit
linear pulse control additionally checks finite response and no more
than five percent excess energy growth over the old closure. All must
pass before the nonlinear packet is run.

The five fixed cases are h=.1,.05,.025 at R=120, a half-time-step control
at h=.025, and R=160 at h=.025. Courant=.1 except the .05 half-step
control. Sampling is every .25 through 62.75. The same original D4
curvature readout, .005 error ceilings, charge/mass, refinement,
time-step and domain gates are used. Metric readout substitutions and
constraint projection are excluded. Runs may execute in isolated
parallel processes, with source hashes checked at entry and exit.

The additional repair target is a fine-grid maximum R2 error below
.0013383642549746441, section 17's twice-finer result. At 62.75,
maximum |K|, minimum F, maximum density, central proper time and central
weighted source must agree with that reference within normalized .001.
Failure is retained as a bounded numerical result; thresholds and
parameters are not retuned after production output. Neither a further
time extension nor another finer-grid sequence is part of this stage.

Pre-production freeze: verifier SHA256
`d84043f818c88b7807879f5a146a064d6e23f61f6671227e8ff0d4dd005dad01`.
The final-source metric preflight passed 122/122 checks; the unchanged
base and source-budget suites passed 74/74 and 104/104. The two imported
engine hashes remain those recorded in section 17. An independent
code audit confirmed unchanged old solver classes, initial packet,
paired-matter operators and original certification functions.

### Result: the candidate fails its physical-domain reconstruction

The frozen five-case attempt fails the registered repair target. Its
preserved progress output records:

| Case | Last completed sampled time | Evolution wall time (s) | Status |
|---|---:|---:|---|
| h=.1, R=120, C=.1 | No initial sample | 0.0 | NUMERICAL_LIMIT |
| h=.05, R=120, C=.1 | 0 | 0.1 | NUMERICAL_LIMIT |
| h=.025, R=120, C=.1 | 25.75 | 206.0 | NUMERICAL_LIMIT |
| h=.025, R=120, C=.05 | 25.75 | 413.6 | NUMERICAL_LIMIT |
| h=.025, R=160, C=.1 | 25.75 | 258.6 | NUMERICAL_LIMIT |

The coarse worker's unmeasured guard minima remained infinite sentinels.
Strict JSON serialization rejected them, and the coordinator then failed
to parse that worker's empty output. Consequently this attempt has no
aggregate check count or preserved detailed fine-grid failure state.
The common stop time alone cannot identify the finer runs' cause.

A same-source, immediate coarse replay recovers the exact exception:
`NUMERICAL_ACTION_DOMAIN_LIMIT: resolved negative u`. A separate static
initial-data audit (53/53 prerequisites) reproduces it without evolution.
At r=20.4 the four positive cell values of mu are
`(4.393865254777e-16, 2.644963433307e-13,
1.747211351475e-11, 3.261868846568e-10)`.
The new face interpolation `(-1,9,9,-1)/16` gives
`mu_face=-1.040986470753603e-11`, whereas the original interpolation
there gives `+8.868304929039301e-12`. The corresponding
`u=-3.3311567064226263e-12` crosses the unchanged action-domain
tolerance `-100*machine_epsilon=-2.220446049250313e-14`.
The location is the packet's inner edge, well away from the centre and
the outer closure. The negative interpolation coefficient supplies the
identified defect; the underlying initial cell source remains nonnegative.

| h | Minimum initial face mu | Radius | Initial negative-u gate |
|---|---:|---:|---|
| .1 | -1.040986470753603e-11 | 20.4 | Fails |
| .05 | -3.745638311796453e-14 | 20.35 | Within tolerance |
| .025 | -7.558037204236142e-18 | 20.275 | Within tolerance |

This rejects the tested unrestricted interpolation package as an
admissible repair for this packet. The smooth manufactured and linear
preflight controls passed but missed the actual packet's near-vacuum
edge. Initial-packet admissibility is therefore added to the preflight
after this failed attempt. A failed-result reporting repair preserves
nonfinite metadata explicitly and prevents one worker from discarding
its siblings; neither change alters evolution equations or tolerances.

The previous five-run certificate remains t=62.5. The unmodified
saturation action, old solver results and physical interpretation keep
their prior status. The next numerical candidate would need a
positivity-preserving face reconstruction, tested first on this actual
initial edge; later fine-grid failure attribution is still unmeasured.
No new nonlinear replay, clipping rule, threshold change or further
time extension is part of this completed stage. Global regularity and
the full RefG pressure connection retain their existing open status.

Post-failure verifier SHA256:
`e9f51739fc48b17010fa521232e063550873b11aa3d56758700878b569bcf4b1`.
The revised metric preflight reports 123/124, with the single failure
`metric_initial_packet_admissibility_0.1`; it now blocks production
before spawning workers. These are diagnostic results after the failed
trial, not a reclassification of the frozen production run. Reporting
fixtures pass 18/18; base and source-budget regressions pass 74/74 and
104/104. AST comparison also confirms unchanged original solver classes,
paired-matter operators, initial-data factory and certification functions.

Reproduce the early rejection with `--metric-controls` or
`--metric-upgrade` on the verifier (expected exit code 1).
`metric_reporting_checks()` runs only the in-memory reporting fixtures.

## 19. Source-only positivity repair and bounded replay

### Contract before implementation and replay

The target is to remove section 18's artificial negative face source
without changing cell mass, the saturation action, matter equations,
clock gauge, packet, domain tolerances or curvature acceptance tests.
Only this report, the existing verifier and W92 index are in scope.
The old numerical modes remain available; a default source-face hook
is a behavior-preserving refactor used to isolate the new reconstruction.

For the existing high-order face value H and the nonnegative adjacent
mean L, use the maximal admissible convex blend: retain H when H>=0;
for H<0, theta=L/(L-H) gives (1-theta)L+theta H=0. At L=0 use the
zero endpoint. This is explicitly a face limiter (the positive part
of H on admissible input), not a modification of evolved cell values.
The outer face's low-order endpoint is the last cell value. If both
reconstructions are negative they are left to the existing domain
guard; resolved negative cell values are independently rejected.
Generic interpolation of lapse and signed stresses stays unchanged.
The high-order formula is retained wherever its raw face value is
admissible; smooth profiles bounded away from zero retain fourth-order
accuracy once resolved.

Preflight requires the actual three initial packets; unchanged primary
state, charge/mass update and signed interpolation; empty-cavity and
outer-face controls; a resolved-negative-primary-state rejection;
smooth positive fourth-order reconstruction; the existing manufactured,
parity, gauge, curvature and directional-probe controls. Limiter
statistics must not be contaminated by diagnostic trial states.

After all preflight checks pass, run the h=.1,R=120,C=.1 pilot only
through t=28, sampling every .25. If it cannot complete, retain its
last sample, failing phase/time and exception and stop this stage.
Action-domain failures additionally record the exact cell/face,
radius, primary values, RK substage and diagnostic-probe origin;
other guards retain their own message without an inferred location.
If it completes, run h=.05,.025 plus the h=.025 half-step and R=160
controls to the same endpoint, and apply the original five-case
prefix gates. No t=62.75 precision claim or further time extension
is sought here. A failure keeps its actual status; neither a new
physical term nor a retuned tolerance is introduced after output.

Pre-replay verifier SHA256:
`ec7e3efc02ee7dd9e945028fe7cf43e29f5e99b386df55775b449345d720b5c4`.
All 156 source-positive preflight checks and 19 reporting fixtures pass.
Base, source-budget and legacy localization regressions pass 74/74,
104/104 and 93/93. An independent AST audit confirms the old equations,
initializer and certification gates, modulo the default delegation hook.

### Result: initial repair passes; the pilot isolates a tolerance mismatch

The source-face limiter repairs the initial packet on all three grids.
Its smooth positive interpolation errors for h=.1,.05,.025 are
`2.651805502873472e-5, 1.7323106571431879e-6, 1.0946325845750948e-7`.
The initial curvature time-probe discrepancies are at most 2.76e-11;
the primary state and initial source/matter update remain unchanged.

The preregistered coarse pilot then stops, so the other four runs are
not launched. The command returns `POSITIVE_SOURCE_PILOT_FAILED`,
156/157 aggregate checks and exit code 1. Total elapsed time is 25.584 s
including preflights; the evolution itself takes .094 s. The last
accepted RK endpoint is t=.09 and the attempted step endpoint is .10.
The failure is its third RK substage (nominal midpoint t=.095), at
source face index 201, r=20.2. It is a true evolution-stage guard,
not a directional curvature probe. The exception is
`NUMERICAL_ACTION_DOMAIN_LIMIT: resolved negative u`.

The retained values give the cause directly:

| Quantity | Value |
|---|---:|
| Raw high-order face H | -7.029049897307989e-14 |
| Low-order adjacent mean L | -6.838811314713941e-16 |
| u(H) | -2.2492959671386072e-14 |
| u(L) | -2.1884196207084617e-16 |
| Existing negative-u limit | -2.220446049250313e-14 |

For kappa=2 alpha ell^2=.32 and q>0, the same guard is exactly

    u=kappa*mu/(1+kappa*mu) >= -delta
    iff mu >= -delta/[kappa*(1+delta)],  delta=100*machine_epsilon.

Its lower mu boundary is `-6.938893903907074e-14`. Every contributing
cell and the linear face L satisfy it; H exceeds the allowed negative
u magnitude by about 1.30 percent. The strict limiter predicate
`H<0 and L>=0` is false because L is slightly negative. Consequently
it leaves H unchanged despite having a numerically admissible linear
endpoint. The negative outer coefficient on the positive cell at
r=20.35 dominates the rejected reconstruction. The four primary values
at r=(20.05,20.15,20.25,20.35) are
`(1.165691706620534e-19, -4.378100645570907e-17,
-1.3239812564870792e-15, 1.1123380066336225e-12)`.
An independent static audit reproduces this classification exactly.
These records establish tolerated numerical undershoot, without
separating its roundoff and truncation contributions.

Only the t=0 sample was completed; its zero sampled conservation drift
is not an evolved conservation certificate. The physical-stage
Courant and paired-wave maxima are .09135 and .24896, below their
unchanged .4 and 2.5 guards. Failure metadata and the last sample are
preserved in strict JSON. No new time prefix or singularity-removal
claim is established; the old t=62.5 certificate retains its scope.

The next bounded numerical correction is to make face reconstruction
respect the already registered admissible interval, rather than mix
an exact-sign predicate with a tolerance-based cell guard. That uses
the same tolerance, source equation and primary data. This stage ends
with the identified mismatch; the older fine-grid t=25.75 cause remains
unattributed. Reproduce with `--positive-metric controls` (156/156,
exit 0) or `--positive-metric pilot` (recorded failure, exit 1).

## 20. Source-face reconstruction in the registered numerical domain

### Contract before the nonlinear replay

The bounded target is section 19's face-domain mismatch. Keep its
coarse-first t=28 ladder, packet, action, primary variables, clock,
signed-field interpolation, sampling and all original acceptance limits.
Only the verifier, this report and W92 index are editable. The stage19
class and command without the new modifier remain reproducible.

The new `--source-domain` modifier of `--positive-metric` selects an
isolated source-face reconstruction. Compute q, z and u in exactly the
production floating-point order. Retain every admissible high-order H,
including negative values within the existing 100-epsilon buffer.
For finite H,q,z,u with q>0 and u below that buffer, select the adjacent
mean L only when L satisfies the same original domain predicate. The
outer L is the last cell value. All other H values remain subject to
the original guards. No primary clipping, zero projection, floor or
larger tolerance is introduced; ell=0 uses the raw reconstruction.

Required controls are the saved four-cell RK3 failure, accepted negative
values, both-endpoint failure, representable neighbours of the guard,
nonfinite/wrong-branch/saturation rejection, ell=0, unchanged state and
signed fields, smooth reconstruction order, the three actual initial
packets, curvature probes and restoration of diagnostic-only statistics.
The existing base, source-budget, localization and reporting regressions
must also pass. Stage19 remains a historical numerical comparator.

After preflight, run only h=.1,R=120,C=.1 through t=28 with .25 samples.
On failure, retain the actual last sample, RK endpoint/substage when
available, exception and raising location, and finish this stage. If
the pilot completes, run h=.05,.025 plus the .025 half-step and R=160
controls to t=28 and require the original uninterrupted five-case
prefix gates. Completion of a worker alone is insufficient. This is
a numerical-method validation on the existing action, with no new
observational claim. Physics/source-join/global-regularity flags stay
false; no later-time extension or second repair is authorized within
this stage. The code hash is recorded after controls and before replay.

Pre-replay verifier SHA256:
`7ee5522ac8fd55b9c6a306ae3e2144921a52958ea73136c283ab854f39ec5586`.
Controls pass 168/168, reporting fixtures 19/19, and base/source-budget/
legacy-localization/stage19 controls 74/74, 104/104, 93/93 and 156/156.
Independent AST and numerical audits agree on the ordered source-domain
predicate, unchanged production equations, worker selector propagation
and diagnostic-statistics restoration. Both imported engines retain
their section 18 hashes. No nonlinear stage20 result has been used to
choose the reconstruction, its endpoint or its acceptance thresholds.

### Result: five-case source-domain prefix validated

The command `--positive-metric pilot --source-domain` returns
`POSITIVE_METRIC_PREFIX_VALIDATED`, **228/228**, exit 0. All five
runs complete t=28 with 113 samples each. The base, curvature and
feedback certificates accept every sampled prefix from .25 to 28;
their first-rejection fields are null. Total elapsed time, including
repeated controls and aggregation, is 582.978 s. The verifier and both
engine hashes stay equal to the preregistered hashes throughout.

| Case | h | Outer R | dt | Samples | Prefix maximum normalized metric R2 error |
|---|---:|---:|---:|---:|---:|
| coarse | 0.1 | 120 | 0.01 | 113 | 2.3594011e-4 |
| middle | 0.05 | 120 | 0.005 | 113 | 2.9701348e-5 |
| fine | 0.025 | 120 | 0.0025 | 113 | 2.5409773e-6 |
| half_step | 0.025 | 120 | 0.00125 | 113 | 2.5409832e-6 |
| domain | 0.025 | 160 | 0.0025 | 113 | 2.5409773e-6 |

On h=.025, the prefix maxima are 5.725500394578196e-5 for the radial
constraint, 6.392025999675537e-8 for the regular-metric residual,
7.191970797697697e-5 for the origin constraint, 2.540510743066424e-6
for metric Ricci error, 2.102205250156743e-8 for metric Kretschmann
error and 1.525745148858032e-6 for the feedback-budget error. These
are the existing verifier's normalized diagnostics. The coarse
origin residual is .013770349395765512; the original gate applies
its absolute bound to the fine result and requires refinement from
the middle result (.000999391292412515). Those requirements pass.

Across all sampled times and grids, the largest relative charge drift
is 1.0386069781986862e-10. The sampled outer total mass is unchanged
to the reported floating-point precision on each grid. The largest
registered half-step discrepancy is 2.002103156005519e-9; the largest
enlarged-domain discrepancy is 2.2967785307814103e-16, using each
observable's original normalization. The largest curvature time-probe
discrepancy is 4.0911575169277903e-10. Physical-stage Courant and paired
wave maxima are .09350520719087464 and .2548482275806726, respectively,
below the unchanged .4 and 2.5 guards.

The actual-source correction is localized: its maximum simultaneous
replacement count is three faces on coarse/middle and two on the fine
and control grids. Counts are per reconstruction call, not total events.
On the fine run the most negative raw face is -7.346034961246577e-12
and the largest H-to-L change is 4.886594736875152e-11. Primary values
are never clipped. Its minimum accepted u is -2.2193628367497117e-14,
inside the original -2.220446049250313e-14 numerical buffer. Diagnostic
trial states are excluded from these stage extrema.

At t=28 the fine run has minimum F=.5511170695662444, maximum scalar
density .05463538957720123 and central elapsed proper time
20.86282622514792. The positive F and absent trapping certificate
place this new-method check before the trapped region. The previous
reconstruction obstacle is removed on this registered interval; the
old stage18 fine-run exception still has no preserved direct diagnosis.
The only new closure is the short source-reconstruction prefix.
Global regularity, singularity removal, persistent regulation and the
full RefG pressure join remain false. The old method's t=62.5 certificate
retains its separate scope. No monograph or Git rules were changed.

This bounded stage is complete. The next direct numerical decision is
whether the same frozen reconstruction passes the five-case independent
curvature/source gates through the previously problematic t=62.75,
without changing physics or precision limits. That later replay has
not been performed here.

## 21. Frozen source-domain continuation through t=62.75

### Contract before implementation and evolution

The decision is whether the section 20 reconstruction carries the same
packet through the previously problematic late interval with the original
five-case curvature/source accuracy gates. Only the verifier, this report
and W92 index may change. The action, packet, AdmissibleMetricClock,
production equations, reconstruction, domain guards, time steps, radii
and acceptance thresholds are frozen. The new `--late-metric` modifier
requires both `--positive-metric` and `--source-domain` and selects only
the endpoint 62.75; the existing t=28 commands retain their behavior.

Run the same 168 controls and reporting/regression checks first. Then
run the h=.1,R=120,C=.1 pilot to 62.75 with .25 samples. Stop this stage
on pilot failure and preserve its actual exception/context and last
sample. On pilot completion, run the h=.05,.025 cases, the h=.025,C=.05
half-step case and h=.025,R=160 domain case to the same endpoint.
Each completed case must reproduce section 20's t=28 mass, minimum F,
maximum density and central proper time to absolute tolerance 1e-10.
These are numerical regression data from the same packet, not new
physical or observational fitting targets.

Success requires all 252 samples per case and the original uninterrupted
base/independent-curvature/feedback prefix gates through 62.75, together
with unchanged source hashes. Retain the first rejected prefix and its
actual failed gates on any accuracy failure. Trapping, posttrapping
curvature and feedback flags retain their original dependency rules;
global regularity, singularity removal and full RefG pressure join stay
false. No additional stage18 precision threshold or substituted curvature
readout is introduced. This stage ends with that bounded decision: no
post-output retuning, new physical term or further time extension.

The only execution/reporting addition is live, case-labelled progress
for these longer workers; results remain stdout JSON and no generated
files are created. The frozen verifier hash and control results are
recorded before the replay.

Pre-replay verifier SHA256:
`369131e7fe9b24a147eaf94dbe1c599d3feb7742563f54588bbb3190ada6df22`.
The late preflight passes 168/168 and the reporting/replay fixtures 22/22.
Base, source-budget, legacy-localization and stage20 controls pass
74/74, 104/104, 93/93 and 168/168. Independent read-only inspection
confirms unchanged reconstruction/dynamics and thresholds, endpoint
propagation, the t=28 regression values and the coarse-first stop rule.
The imported engine hashes remain those recorded in section 20.

### Result: the late independent-curvature prefix passes

The command `--positive-metric pilot --source-domain --late-metric`
returns `LATE_SOURCE_DOMAIN_PREFIX_VALIDATED`, **228/228**, exit 0.
All five cases complete t=62.75 with 252 samples each. Every registered
base, independent-curvature and feedback prefix passes; all three
first-rejection fields are null. The first resolved trapping certificate
is at t=50.5. Source hashes remain unchanged throughout. All twenty
section20 t=28 replay differences (four quantities on five grids) are
exactly zero at the emitted floating-point precision. Total elapsed
time, including controls and aggregation, is 1273.156 s.

| Case | h | Outer R | dt | Samples | Maximum normalized metric R2 error on the full prefix |
|---|---:|---:|---:|---:|---:|
| coarse | 0.1 | 120 | 0.01 | 252 | 9.43062188e-2 |
| middle | 0.05 | 120 | 0.005 | 252 | 8.96522298e-3 |
| fine | 0.025 | 120 | 0.0025 | 252 | 1.00170848e-3 |
| half_step | 0.025 | 120 | 0.00125 | 252 | 1.00170709e-3 |
| domain | 0.025 | 160 | 0.0025 | 252 | 1.00170848e-3 |

The unchanged residual gate bounds the fine-grid error below .005 and
requires improvement over the middle grid. The larger coarse and
middle R2 values are retained as measured refinement data; an absolute
.005 ceiling on each individual grid was never the acceptance rule.
The fine/middle R2 ratio is 0.111732690.
The fine prefix maxima for radial constraint, regular-metric residual,
origin constraint, metric Ricci error, metric Kretschmann error and
feedback-budget error are respectively
`6.652832375883471e-5, 5.924001012895404e-7, 3.514580229916607e-4,
8.768238598036993e-4, 2.403369590161289e-4, 1.608615509948713e-4`.

At the previously problematic endpoint t=62.75, the h=.025 metric R2
error is `0.0005996325239100663`. Section17's same-h,
same-time original-method error was `.005154066711989016`: the endpoint
error is lower by a factor 8.595376. This endpoint comparison is
distinct from the new method's larger full-prefix maximum shown above.
The saturation action and independent curvature readout are unchanged.

Across all grids and sampled times, relative charge drift is at most
1.8685886171709853e-10. The sampled outer total mass has zero reported
drift on each grid; this finite-run observation does not assert exact
universal conservation. The largest registered half-step and outer-domain
discrepancies are 2.002103156005519e-9 and 1.7810010245299012e-11,
using the original observable normalizations. The curvature time-probe
error is at most 3.485985036892727e-8. Courant and paired-wave bounds
remain below .09350520719087464 and .2548482275806726 respectively.
The source-face correction retains the section20 extrema and at most
three simultaneous replacements on coarse/middle or two on fine/control
grids; no primary-state clipping or new floor has been applied.

The final fine state has minimum F=-.4584434107681472, 284 contiguous
trapped cells, negative outgoing and ingoing null expansions, maximum
scalar density 22.68267894119321 and central proper time
37.02387656501605. Its maximum absolute Kretschmann scalar is
.4026469183541146; the central value is .39453693451423005. The
minimum q over its evolved stages is .2980222980952612. These are
finite, resolved quantities in this declared model and finite interval.

### Physical reading and the next decision

The existing curvature-controlling weighted density is
`E=alpha*ell^2*q^(3/2)*rho`; it is distinct from total outer mass.
At t=62.75 the fine-grid central normal rates are
`n(rho)=+1.5521328655355988` and `n(E)=-.0020270216951075674`.
The source weighting therefore weakens the central contribution while
its material density grows. This sign pairing occurs on all five grids.
At the curvature maximum r=1.0875, however, the fine result is
`n(E)=+.017832769390740483` and `n(rho)=+3.515526256238848`.
The location-dependent contrast is essential to the global question.

The maximum absolute curvature still increases from t=61.75 to 62.75:
the fine change is .006878783351028428, while three times the largest
control spread is .00019833678234504326. All five changes are positive,
so the registered trend classification is `increasing`. Local feedback
is supported; a global arrest of curvature growth is not established.
The accepted flags are finite-window trapping, posttrapping curvature,
feedback evolution and the source-reconstruction prefix. Global
regularity, singularity removal, persistent regulation and the full
RefG pressure join remain false.

This stage closes the late numerical-accuracy obstacle on its specified
interval and ends here. The next finite-time decision is how the
off-centre curvature growth changes under continued same-action
compression, using the source budget at that maximum. A monotone
approach to a finite limit is admissible; a turnover is not required
for regularity. An all-time bound remains a separate mathematical
result. Any later interval needs a separate bounded contract.
No reconstruction retuning, new
physical term, monograph edit, Git-rule edit or extra artifact was made.

## Reproduction and attribution

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py"
    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_inverse_saturation_candidate.py"

Results and numerical examples are emitted to stdout; no generated files.

The base sourced-dust verifier passed 74/74 assumption-scoped checks. Independent read-only
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
