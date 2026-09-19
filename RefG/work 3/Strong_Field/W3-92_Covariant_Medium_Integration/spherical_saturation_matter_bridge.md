# Saturating spherical gravity coupled to conserved matter

**მიმდინარე კონტექსტი — 2026-09-19:** სხვადასხვა მოქმედების შედეგების
მოქმედების არეები შეკრულია [ერთიან სამუშაო რუკაში](medium_health_horizon_diagnostic.md).
ამ ფაილის q არის პოსტულატური გრავიტაციული გაჯერების ფაქტორი;
მისი RefG-ის საერთო წნევით p-ფაქტორთან იდენტიფიკაცია გამოყვანილი
არ არის (§36). ქვემოთ დათარიღებული შედეგები თავიანთ თავდაპირველ
მოდელსა და პირობებს ინარჩუნებს. ეს შენიშვნა ახალ გამოთვლას არ ამატებს.

**შედეგი მოკლედ (2026-09-14):** პოსტულატურ გაჯერების კანონზე დაფუძნებულ
სფეროსიმეტრიულ მოდელში ერთგვაროვანი უწნევო წყაროს კოლაფსის სიმრუდე
შეზღუდულია. ეს ნამდვილი დადებითი შედეგია. კანონიკური ველის კოლაფსის
რიცხვითი შემოწმება ცალკე შედეგია და მხოლოდ გამოთვლილ მონაკვეთს ეხება.
ადგილობრივი წყაროს ნებისმიერი განაწილებისთვის გაჯერება სიმრუდის
უნივერსალურ ზღვარს არ იძლევა; რეგულარული გლობალური გაგრძელება ყველა
წყაროსა და მოქმედების განტოლებით ჯერ არ არის დასრულებული.

RefG-სთან მისაერთებლად შემოწმებული სიმკვრივეზე დამოკიდებული F(n)T
ფორმულების კლასისთვის მიღებულია მკაცრი უარყოფითი შედეგი: §§27,31,32-ის
ზუსტ პირობებში ის ვერ იძლევა ერთდროულად მდგრად, სიმრუდით შემოსაზღვრულ
და სრულად გაგრძელებად მუდმივად შემკუმშავ KS ბირთვს. ეს დასკვნა მიღებულია
გარემოსა და მატერიის სრული დაკავშირებული განტოლებებიდან, არა გარემოს
ცალკე, ხელოვნურად გაყინული ცვლილებიდან. ყველა 293 ანალიტიკური შემოწმება
დამოუკიდებლად გამეორდა; მათ შორისაა უარყოფითი შედეგების შემოწმებებიც.

**სრული უსინგულარო RefG შავი ხვრელი ჯერ არ არის დამტკიცებული; მთელი
RefG-ის შეუძლებლობაც არ არის დამტკიცებული.** ორი სხვადასხვა მოქმედების
შედეგები ერთმანეთს არ უნდა გადაეცეს. წნევა–ოსცილონის მასშტაბური კანონის
სრული მიერთება კვლავ საჭიროა; ზუსტად ერთი სტატიკური საათი–სახაზავის
ფაქტორი არჩეულ გეომეტრიასთან ვერ თავსდება. გამოთვლილი შეზღუდვები ეხება
აქ განსაზღვრულ მოდელებსა და პირობებს, არა ყველა შესაძლო განვითარებას.

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

## 22. Fixed same-action curvature-growth window through t=70

### Contract before implementation and evolution

The decision is the finite-time behavior of the off-centre maximum
curvature after the certified section21 interval. Use the same action,
packet, source reconstruction, grids, time steps, boundaries and original
prefix acceptance gates. Only the verifier, this report and W92 index
may change; no primary clipping, new physical term or tolerance change.
The optional `--late-end 70` requires the existing late/source-domain
mode. Its default remains 62.75 so section21 stays reproducible.

After the existing controls and reporting/regression tests, run the
coarse pilot to70; stop this stage if it fails. Otherwise run the same
four refinement/half-step/domain controls, with at most two workers
concurrent. Require 281 samples per completed case, unchanged code
hashes and the original unbroken base/curvature/feedback prefix gates.
The t=28 regression remains; the five section21 t=62.75 values of mass,
minimum F, maximum density, central proper time and maximum absolute
Kretschmann scalar must also repeat within absolute 1e-10. Missing or
failed cases keep their actual failure context and cannot be certified.

The physical trend is a diagnostic, not a desired-sign acceptance gate.
Use the existing Kmax=max(abs(Kretschmann)) readout: record changes on
the fixed baseline [61.75,62.75] and the one-unit windows [63,64],
[64,65], [65,66], [66,67], [67,68], [68,69], [69,70]. A signed trend
is resolved only when all five signs agree and the fine change exceeds
three times the largest difference from any of the four controls.
Compare the last available certified window's change with the baseline
using the same five-case spread rule; label growing curvature as
slowing/accelerating only when its change-of-rate is resolved.
Report E and its existing normal-frame budget at the curvature peak
at62.75,65,67.5,70 when those snapshots are inside the accepted prefix.
Instantaneous local n(E) is distinct from the time change of a moving
global maximum. No extrapolation from these finite windows is allowed.

If accuracy fails, retain the first failed gates and restrict all new
physical interpretation to the certified prefix. If no new certified
window survives, return that numerical limit rather than infer a trend.
A turnover is not required: monotone approach to a finite limit is an
admissible physical possibility. Neither slowing nor a finite-time
turnover proves an all-time bound. Global regularity, singularity
removal, persistent regulation and the full RefG pressure join remain
separate open flags. Stop after this one registered decision, with no
post-output retuning or further time extension and no generated files.

Pre-replay verifier SHA256:
`03fa8560cb014f4e9a09b192deec7efd3a9649dbe245345a666a15385589afdf`.
The t=70 preflight passes 168/168 and reporting/growth controls 30/30.
Base, source-budget, localization and section21 controls pass 74/74,
104/104, 93/93 and 168/168. AST comparison against the committed
section21 version confirms identical evolution classes, run loop and
verdict/certify functions. Endpoint misuse is rejected. The two imported
engine hashes remain unchanged. No nonlinear section22 output was used
to select these rules.

### Outcome of the registered run (2026-09-14)

All five cases complete t=70 with 281 samples each. The frozen verifier
returns `CURVATURE_GROWTH_PREFIX_OPEN`: **226/228** aggregate checks
pass. The two failed checks are `terminal_curvature_metric_R2_error`
and its dependent `terminal_positive_unbroken_prefix`. The base
evolution passes through70; the joint curvature/feedback sampled prefix
passes through **69.5**, with first resolved trapping still at50.5.
The first rejected sample is69.75 and fails only the R2 accuracy gate.
The five t=62.75 checkpoint quantities reproduce section21 exactly in
every case (all25 absolute differences zero); t=28 replay gates also pass.

| Prefix end | Fine normalized R2 error maximum | Middle maximum | Joint prefix |
|---|---:|---:|---|
| 69.5 | .004715164558097584 | .06613396785066517 | accepted |
| 69.75 | .005143821862437554 | .07087981359358365 | first rejected |
| 70 | .005611957866249050 | .07558564306381411 | rejected |

The original gate requires fine error below .005 and refinement relative
to the middle grid. Refinement survives; the fine absolute error exceeds
.005. At70 the coarse R2 maximum is1.1178144343792542, the half-step
maximum .005611956065397421 and the expanded-domain maximum equals
the fine value. Coarse and middle values are refinement controls, not
individually certified fine-grid accuracy. The close half-step/domain
agreement locates the unresolved accuracy in the spatial calculation
rather than supplying an independent continuation certificate.

At the accepted69.5 prefix, fine error maxima are: radial constraint
.0002364396037185474, regular metric .000001749253707582351, origin
.00035145802299166074, Ricci .001084468538736610, Kretschmann
.002636032899555008 and feedback budget .0011295857156654984.
Reported sampled mass drift is zero in all five complete runs; the
largest charge drift through70 is1.8743850915825533e-10.

### Certified physical readout

Every registered complete window inside the accepted prefix has
positive maximum-absolute-Kretschmann growth, resolved by the fixed
five-case spread rule. Rates use the model coordinate time.

| Window | Fine change per unit time | Three times largest control spread |
|---|---:|---:|
| 61.75--62.75 | .006878783351028428 | .0001983367823450433 |
| 63--64 | .007224303059618076 | .0002913351391807817 |
| 64--65 | .007624974335917134 | .0003987663664386520 |
| 65--66 | .008158828759446290 | .0001441567991368187 |
| 66--67 | .008903419163419524 | .0005893727756484113 |
| 67--68 | .009891609420797254 | .002098212767913110 |
| 68--69 | .010295487315045593 | .003638897613409353 |

The registered baseline-to-last-window rate difference is
+.003416703964017165 on the fine grid, below its three-spread threshold
.003440560831064310. Its classification is therefore **unresolved**.
The supported physical statement is continued growth. Neither slowing
nor acceleration is promoted to a resolved rate-change claim. The
[69,70] window and t=70 physical snapshot are excluded because they
extend beyond the joint accuracy certificate.

At the off-centre curvature maximum, the fine-grid source readout is:

| t | Peak radius | Kmax | E | n(E) | n(rho) |
|---|---:|---:|---:|---:|---:|
| 62.75 | 1.0875 | .402646918354115 | .590496570563721 | +.017832769390740 | +3.515526256238848 |
| 65 | 1.1875 | .419251840439430 | .598228757005243 | +.030679231710463 | +4.272029975106355 |
| 67.5 | 1.2625 | .441105022749825 | .608446361160210 | +.042864402778202 | +5.428786546361598 |

Here E=alpha*ell^2*q^(3/2)*rho is the curvature-controlling weighted
density; n is the normal-frame derivative defined in section21.
All five snapshot cases have positive n(E) and n(rho). At67.5 the
fine E budget contains flux -.20254570196687094, compression
+.3328379009399843 and response -.08742836001214889. The negative
response is active while the net local source still increases. The
moving peak's coordinate-time curvature growth and local n(E) are
distinct readouts.

The stage extends the verified finite interval from62.75 to69.5 and
identifies the next numerical limit precisely. Its full t=70 acceptance
condition fails. Global regularity, singularity removal, persistent
regulation and the full RefG pressure join remain false. The existing
section21 certificate remains valid within its original interval.

The bounded follow-up, if authorized, is a spatial-refinement test of
this same late R2 mismatch at fixed endpoint70, with an independent
metric/source curvature comparison. Further time extension alone cannot
settle it. This stage ends with the recorded result; no threshold
retuning, new physical term or additional evolution was performed.

Reproduce with
`--positive-metric pilot --source-domain --late-metric --late-end 70`.
Production SHA256 equals the preregistered verifier hash above; both
imported engine hashes are unchanged. Total elapsed time was
1374.5457141 seconds. The reporting controls remain30/30.

## 23. Fixed-endpoint spatial refinement and global-decision audit

### Contract before implementation and new evolution (2026-09-14)

The author authorizes multiple consecutive research stages toward a
singularity-removal decision. Each stage retains a separate frozen
contract and actual outcome; finite numerical success is not a global
proof and numerical failure is not a spacetime singularity. The work
remains in this strong-field package. Monographs, speculative material,
Git rules and external publication remain unchanged.

CLAIM_ID / MODEL_VERSION: W92_SPATIAL_REFINEMENT_T70_V1.
GOAL: test whether the section22 late R2 mismatch is reduced by halving
the spatial mesh, at the same endpoint70 and with unchanged action.
TYPE: numerical refinement evidence for this fixed initial packet.
ASSUMPTIONS / FREEDOM / DOMAIN: retain alpha=.04, ell=2, original
packet, source-domain reconstruction, original guards and all acceptance
thresholds. The new (coarse,middle,fine) mesh spacings are (.05,.025,.0125)
at R=120 with dt=.1h; the half-step case uses h=.0125, dt=.05h and the
domain case h=.0125, R=160, dt=.1h. Start every case at t=0.
No interpolated restart or later time extension is permitted.
METHOD / CROSSCHECK: existing independent metric/source curvature,
constraint, conservation, time-step, domain and refinement tests;
run the new coarse pilot first, then remaining controls with at most
two concurrent workers. The initial-packet preflight explicitly covers
h=.0125. Existing run/evolution/verdict/certify mathematics is unchanged.
PASS: all five cases finish70 with281 samples, code hashes agree, the
original unbroken curvature/feedback certificate reaches70, and exact
overlap checkpoints repeat within1e-10. New coarse repeats old middle;
new middle repeats old fine at28 and62.75. New resolutions have no old
exact target and are assessed by refinement rather than assigned replay
success. Report the same fixed growth windows and original spread rule.
FAIL: retain the actual first failed gate or numerical guard. A shortened
valid prefix is reported precisely. No threshold or physical retuning
after output; no singularity inference from failed resolution.
BENCHMARK: section22 h=.025 R2 mismatch at69.75 and70; section21 overlap
checkpoints. INPUT/DATA_ROLE: model-produced numerical controls, no
observational fit or predictive data claim. ERROR_BOUND: original
normalized residual/refinement thresholds, not rigorous interval bounds.
VALIDITY / FLAGS: finite-window trapping and curvature are separate from
global regularity, singularity removal and full RefG pressure join.
PROVENANCE / FILES: existing verifier, this report and the W92 index.
Results to stdout; no large generated output files. Freeze the verifier
hash after controls and before nonlinear runs.
STOP: obtain this fixed-endpoint refinement decision. A separate bounded
analytic audit will test the global source/causal conditions; it may run
concurrently read-only. Any subsequent physical change requires its own
explicit contract and fresh tests, as already authorized by the user.

Pre-evolution verifier SHA256:
`1a23833cd7bc907da7bdda32f26c8ced9ec866f298423a646fb4827f7ce40500`.
Refined preflight172/172, default preflight168/168 and reporting42/42
pass; four invalid CLI combinations are rejected. The five evolution
classes and run/verdict/certify ASTs match the previous engine. The
returned grids are explicitly checked against the registered ladder.

### Result: full fixed-endpoint refinement passes (2026-09-14)

All five registered cases finish t=70 with281 samples each. The final
decision is SPATIAL_REFINEMENT_PREFIX_VALIDATED:237/237 checks pass,
first_rejected=null. Base evolution, independent curvature and feedback
all accept the unbroken sampled interval0-70. Resolved future trapping
is first certified at50.5. Total concurrent runtime is5036.718seconds;
no run was restarted from an interpolated checkpoint.

| Case | h | Outer radius | dt | Maximum normalized R2 error on0-70 | Final max abs(K) |
|---|---:|---:|---:|---:|---:|
| Coarse | .05 | 120 | .005 | .075585643064 | .465699512571 |
| Middle | .025 | 120 | .0025 | .005611957866 | .466026613684 |
| Fine | .0125 | 120 | .00125 | .000376201094 | .466068868357 |
| Half step | .0125 | 120 | .000625 | .000376203606 | .466068868360 |
| Wider domain | .0125 | 160 | .00125 | .000376201094 | .466068868357 |

The absolute R2 threshold .005 is the fine-grid gate; coarser levels are
the registered convergence controls, not separately certified fine-grid
solutions. Halving h from.025 to.0125 reduces its full-prefix maximum
error by14.9174, without changing the equation or tolerance. The fine
K-readout and feedback-budget errors are .000226640112 and .000096999091.
All cases report zero sampled mass drift; the largest relative charge
drift is5.964e-12. The parent independently repeated the172/172 refined
preflight and rechecked the production and both engine hashes.

The registered replay mapping is new coarse->old middle and new
middle->old fine, with8 scalar targets at28 and10 at62.75. All pass.
An additional parent comparison of every shared numerical checkpoint
field at these four mapped states gives maximum absolute difference0.
New h=.0125 data are judged by convergence, not assigned an old target.

Every registered complete curvature-growth window remains positive.
The fine mean rate is .006876915734 on[61.75,62.75] and .009521002712
on[69,70]. Their difference .002644086978 exceeds the unchanged
three-times-five-case-spread threshold .000116432057. The final window
therefore grows faster than the baseline. This is NOT monotonic
acceleration: the immediately preceding[68,69] rate was .010355467540,
larger than the final rate. The comparison is in the model coordinate
time, not a claim about every observer's proper-time acceleration.

At70 the fine max abs(K)=.466068868357 occurs at r=1.30625. The local
weighted-source budget there is

    normal_rate(E)= -.213091386738 + .341792710605 - .102497075406
                  = .026204312885,
                   flux             compression     response.

The negative response is active, but the sum is still positive at that
point. At the centre E instead decreases at rate-.002106897189 while
density increases at1.381305839816. The two locations must not be
conflated. The fine terminal minimum q=.271214207905 and minimum
lapse=.083139840313 remain within the registered domain.

DECISION: the previous late R2 failure was reduced by spatial refinement;
it is not evidence of a physical singularity. The validated packet still
has finite, increasing maximum curvature through70. Neither eventual
blow-up nor an all-time bound follows. The global/source and compatibility
decisions are supplied separately by sections24-32, not by extending the
same time integration without a new mathematical criterion.

Reproduce the full stage with

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py" --positive-metric pilot --source-domain --late-metric --late-end 70 --spatial-refine

The production verifier remains at the preregistered hash above; both
source engines and all physical parameters are unchanged.

## 24. Source and causal completion boundary of the retained action

### Contract before exact tests (2026-09-14)

This stage answers two bounded questions that additional time samples
cannot settle: whether enclosed-mass saturation alone controls local
source concentration in a trapped region, and whether its radial-null
response can by itself produce a future-null-complete, globally
hyperbolic trapped spacetime with noncompact Cauchy surface.
CLAIM_ID / MODEL_VERSION: W92_SATURATION_COMPLETION_BOUNDARY_V1.
TYPE: exact local identities/counterexample and a conditional application
of the spherical trapped-surface focusing argument.
ASSUMPTIONS: the same sourced action and canonical scalar, alpha>0,
ell>0, A,L,q>0, smooth regular orbit frame, z=(1-q)/ell^2. The causal
claim additionally assumes a smooth spacetime, a closed acausal round future
trapped surface, radial null convergence along its normal generators,
and a connected noncompact Cauchy surface. Global hyperbolicity is an
explicit condition, not something inferred from a finite simulation.
METHOD / FREEDOM: at a fixed trapped point F=A-v^2<0 choose real scalar
data psi=0, P!=0 and D/P=-v/sqrt(A)+sqrt(v^2/A-1). Verify the canonical
stress and the exact mass-gradient cancellation rho+vS=0. Amplitude
labels distinct local source data, not successive times of the evolved
packet. Use the concrete point alpha=1/25, ell=2, A=L=1, v=sqrt(2),
r=4, q=1/2 as an exact/numerical crosscheck. No physical parameter is
fitted and no modified action is introduced.
PASS: zero symbolic residuals for mass/metric constraint compatibility,
canonical energy inequalities, stress determinant and leading curvature
coefficient; demonstrate E is unbounded with amplitude at fixed q and
fixed local M and M_r. Independently derive R''=-(R/2)Ric(k,k) for an
affinely parameterized radial null ray, and insert the positive screened
canonical null source. Record the focusing bound from theta'<=
-theta^2/2 with theta_initial<0.
FAIL / FALSIFIER: any nonzero required identity invalidates that claim.
A local initial-data witness is explicitly not a solution evolving into
blow-up. A focal point is explicitly not a curvature singularity.
BENCHMARK / CROSSCHECK: derive stress directly from P,D and also from
orthonormal variables; negative controls break the cancellation and
the null-source sign. Prove the sufficient contrast bound from
rho<=C M/r^3 by maximizing x/(1+2x)^(3/2).
ERROR_BOUND: exact symbolic checks; numerical examples only illustrate
those identities. No interval proof of the nonlinear PDE is claimed.
CAUSAL ARGUMENT: the compact future-boundary/noncompact-Cauchy
contradiction is a mathematical argument under the above conditions;
a Python test checks the action and focusing algebra, not the global
topology. Extensions beyond a Cauchy horizon remain outside that
globally hyperbolic conclusion and require their own regularity test.
DATA_ROLE / OBSERVATION: N/A, no observational data or fitting.
FLAGS: local_mass_cap_insufficient and conditional_global_obstruction
are separate from fixed_packet_blowup, curvature_singularity_proved,
all_RefG_rejected, global_regular_completion and full_pressure_join.
PROVENANCE / FILES: one additional reproducible exact-check script,
verify_saturation_completion_boundary.py, this report and W92 index.
The running evolution verifier and both engines stay unchanged.
STOP: establish these precise restrictions and required next conditions;
do not manufacture a binary conclusion about the undeveloped full RefG
theory. This stage can finish while the independent fixed-endpoint
spatial-refinement run continues.

### Exact result and independent verification

The isolated checker passes48/48, including an independent metric
reconstruction of R2, the radial Hessian and the Kretschmann scalar.
SHA256: `2073eb1141f406432dc7e0dbcaa4a27ff5e96c8b14459a67d095378ab4f41c24`.
A second run reproduces48/48. The numerical evolution verifier remains
at its preregistered section23 hash.

At the registered trapped point, with arbitrary finite real P>0,

    rho=(2-sqrt(2))*P^2, S=J=-rho/sqrt(2),
    p_r=rho, p_t=rho/sqrt(2), M_r=0,
    M_t=8sqrt(2)rho, A_t=sqrt(2)rho/25,
    E=sqrt(2)rho/25,
    R2=2rho^2/625-sqrt(2)rho/50-5/16,
    K=R2^2+rho^2/1250+5/64,
    limit_(P->infinity) K/rho^4=4/390625>0.

The radial and temporal mass equations, metric/shift derivatives,
momentum constraint, clock equation and scalar energy balance all agree.
In particular the metric is allowed to respond in time: holding A_t=0
would violate its equation and is detected by a negative control.
This local source/geometry jet demonstrates the failure of a pointwise
density bound inferred from M and M_r inside trapping. It is a family
of finite local data, not a fixed-packet blow-up trajectory.

For a radial affine null vector k the retained equations give exactly

    Ric4(k,k)=2 alpha q^2 T(k,k)>=0,
    d^2r/dlambda^2=-alpha r q^2 T(k,k)<=0.

The canonical source is a sum of squared null field derivatives; its
potential cancels in this contraction. For a round trapped sphere,
its initially negative expansion obeys theta'<=-theta^2/2, so focusing
occurs within2/abs(theta_initial). Making q smaller leaves the
expansion-squared term and preserves the focusing inequality.

With a smooth spacetime, a compact acausal trapped sphere and a connected
noncompact Cauchy surface, the null-generator version of the singularity
theorem excludes future-null completeness. Only convergence along the
orthogonal generators is needed; spherical symmetry keeps them radial.
This is a conditional causal obstruction, supported by
[Fewster and Galloway, Theorem5.2](https://arxiv.org/html/1012.6038v3).
Set their damping parameter to zero: the nonnegative Ricci integral
exceeds the negative initial expansion. The theorem supplies the global
step; Python verifies the local action/geometry premises.

A focal point alone is a caustic. The global conclusion is incompleteness,
not a proof of divergent K or an inextendible metric. A continuation
beyond a Cauchy horizon drops the global-Cauchy hypothesis and must be
tested separately. A compact cosmological Cauchy surface is another
different domain. Finite-grid trapping supports, but does not rigorously
prove, the continuum trapped-surface premise for this packet.

Thus the positive-screening, canonical-source action is excluded as a
future-null-complete **globally hyperbolic trapped completion** with the
stated noncompact initial topology. Changing only the strength of its
positive null response cannot remove this obstruction. The full RefG
theory and regular-curvature non-globally-hyperbolic extensions are not
excluded by this result.

A separate sufficient curvature target is explicit: if its actual
dynamics supplies rho<=C M/r^3 uniformly in a regular frame, then
E<=C/(3sqrt(3)) and section14 supplies curvature bounds. The new trapped
source witness shows why the mass constraint alone cannot supply C.
The existing pressure/action relation and causal extension are therefore
substantive missing conditions, not tasks that more time samples close.

## 25. Existing current-action bridge: homogeneous compatibility filter

### Contract before new symbolic tests

CLAIM_ID: W92_EXISTING_CURRENT_HOMOGENEOUS_JOIN_V1.
GOAL: use the already-derived W3-87 action, rather than an invented
pressure identification, to test which constitutive coefficient
reproduces the current homogeneous rational response and what it does
to the phase equation and null focusing.
MODEL: S=-K integral e F_grav(n)T + integral(J.dtheta-e rho(n)),
K=1/(16piG), n a^3=constant, T=6H^2; positive n,rho,K,ell.
Full W3-87 density-chain, exchange and connection terms are retained
as dependencies; the test reduces only its established FLRW equations.
METHOD: solve 6K F H^2=rho for F under the section2 target H^2;
independently differentiate the constraint and compare the scale
Euler equation. Retain the current variation in the phase equation.
PASS: exact agreement with the same-action homogeneous target, explicit
phase shift, and the correct sign of Hdot for rho'>=0. A mutation omitting
F' must fail the phase/scale equations. This is a branch-restricted
dictionary, not an independent microscopic derivation.
FREEDOM / DATA: no fit or observation; the target response fixes F on
this homogeneous branch. No spatial source, pressure P_F or clock/rod
identification is inferred. Files: the existing completion-boundary
checker, this report and W92 index; production evolution stays frozen.
STOP: determine whether this exact existing-action match supplies a new
defocusing mechanism or merely reproduces the previous homogeneous
one, then record the decision before considering any further postulate.

### Result: exact match, not a new focusing sign

The unchanged48 section24 checks and22 new checks pass70/70. The parent
independently reran the complete checker with the same result. At this stage
its SHA256 is `b184e6a412a5c1e2b83cda2669ef17b3d09d15bc840fe6512b8c155ab32c8c25`;
the production verifier remains at its frozen section23 hash.

Varying N,a,j,theta independently before N=1 gives

    6K F H^2=rho, n_dot=-3Hn,
    theta_dot=rho'+6K H^2 F',
    2F Hdot+3(F-nF')H^2=-(n rho'-rho)/(2K).

The target response uniquely fixes this homogeneous-branch coefficient:

    F=1+ell^2 rho/(6K), q=1/F,
    Hdot=-n rho'/(4K F^2),
    theta_dot=rho'(1+ell^2 H^2).

The independent derivative of the Hamiltonian constraint agrees exactly
with the scale equation. Omitting the F' contribution fails both the
phase and scale negative controls. For rho'>=0 the metric null focusing
keeps its original sign. The collective phase changes as well: matching
H^2 does not make the two complete actions or their sources identical.
This phase rate is not an externally measured clock factor and neither
it nor q identifies the foundation pressure P_F.

DECISION: retain this explicit branch-restricted dictionary; it supplies
no new defocusing mechanism. Do not launch a duplicate spherical evolution
by treating a homogeneous identity as a full covariant equivalence.

## 26. Minimal stronger-response candidate: homogeneous and spherical filter

### Contract before independent verification

CLAIM_ID: W92_QUADRATIC_CURRENT_SPHERICAL_FILTER_V1.
GOAL: test whether the next analytic term in the existing W87 coefficient
can cure the preceding causal obstruction without discarding its current
equation. The candidate was identified by an exploratory algebraic audit;
this contract registers the independent verification, not a blind discovery.
MODEL: the same W87 action, dust rho=m*n and the explicitly new constitutive
candidate F_grav=1+x+x^2, x=ell^2*m*n/(6K), K,m,n,ell>0. It preserves the
linear candidate's vacuum value and first density correction. It is not
derived from the RefG pressure law and is not adopted in the active theory.
METHOD: derive H^2, Hdot and mu_eff from the full existing FLRW equations;
check curvature bounds, high-density proper-time and null-affine asymptotes,
and the fixed-geometry current block. Then apply the identical coefficient
to W89's valid spherical KS coframe/connection and its full torsion scalar.
Use W90's weighted affine focusing identity without changing its assumptions.
PASS: exact residuals; keep homogeneous future regularity, fixed-background
current health, coupled health and regular-black-hole existence separate.
If mu_eff>0 and inward b<=b0 bound x and F, the already-established W90
finite-affine patch obstruction rejects this candidate for that target.
FALSIFIER / CONTROL: using the FLRW torsion scalar in KS must fail; omitting
the intrinsic sphere-curvature term must change the current equation.
ERROR / FREEDOM: exact symbolic identities and analytic comparison bounds;
no fitting, tuned parameter scan or new numerical black-hole evolution.
SCOPE: positive-current-clock, non-bouncing complete KS interior only.
Inhomogeneous interiors and extensions outside this patch are not excluded
by this filter. A homogeneous regular asymptote is not a black hole.
FILES: completion-boundary checker, this report and index only; the running
production verifier remains frozen. No monograph or Git-rule changes.
STOP: accept or reject the specified transfer before any larger simulation.

### Result: homogeneous improvement fails the retained KS transfer

The checker passes110/110: all preceding70 plus40 new tests. Its stage26
SHA256 is `169e51e796351723743e91938fa4f4f66fb10d3b2be6cdb6a5be77f0f0b10e24`.
For the explicitly postulated quadratic coefficient,

    H^2=x/[ell^2(1+x+x^2)],
    Hdot=-3x(1-x^2)/[2ell^2(1+x+x^2)^2],
    mu_eff/m=(1+2x+3x^2)/(1+x+x^2).

The identities give H^2<=1/(3ell^2), |Hdot|<=1/(2ell^2), hence conservative
|Ricci|<=7/ell^2 and K<=29/(3ell^4). At high density a~tau^(-2/3): future
null affine length diverges and the boosted curvature term Hdot/a^2 tends
to zero. This is a homogeneous future asymptote, not a complete cosmological
history or a black-hole solution. The fixed-geometry current block has
h>0 and c_fixed^2=2x^2/(1+2x+3x^2)<2/3; coupled health is not established.

The actual spherical torsion scalar is not its flat homogeneous value.
Independent lapse/current variation on the valid W89 KS pair gives

    K*T=rho/F-4K/b^2,
    mu_eff/m=(1+2x+3x^2)/F-2ell^2(1+2x)/(3b^2).

Because the first ratio is strictly below3, mu_eff>0 along b<=b0 requires
x<9b0^2/(4ell^2)-1/2. Thus F is bounded above on that retained branch.
The unchanged W90 identity Q=F db/dlambda<0, Q'<0 then forces zero radius
or exit from the patch/domain in finite affine length. Both mutations
that use the FLRW torsion scalar or omit the intrinsic sphere term fail.

DECISION: reject the quadratic candidate for a positive-clock, complete
contracting KS core. Do not run an expensive black-hole simulation of
this already-excluded transfer. Inhomogeneous sources and extensions
outside this patch are separate questions, not rejected by this result.

## 27. Constitutive-family test using the second spherical scale equation

### Contract before independent verification

CLAIM_ID: W92_CURRENT_KS_TWO_SCALE_COMPLETION_FILTER_V1.
GOAL: decide whether another smooth density-only F(n), rather than the
quadratic example, can evade the existing inward-KS obstruction while
retaining a nondegenerate gravitational response and positive current.
The identity was found in an exploratory audit; independent verification
and its conditional theorem are registered here before adding tests.
MODEL: unchanged W87 action and valid W89 KS coframe/connection; j>0,
a,b,F>0, mu_eff>0, conserved n=j/(a*b^2), inward db/dlambda<0.
ADDITIONAL CONDITIONS: the same KS patch covers an alleged complete
future radial null ray; F(n)>=F_min>0 on it; F is continuous and finite
for bounded n including n=0. These are explicit constitutive assumptions.
METHOD: vary N,a,b,j,theta before fixing N=1. Independently verify the
off-shell difference of the two scale equations for
U=F*a*b^2*(H_a-H_b): Udot=F*a, hence dU/dlambda=P*F, P>0.
Combine this with W90's independently derived Q=F*db/dlambda<0, Q'<0.
PASS: exact EL identity, null-affine conversion, Schwarzschild KS and
contracting de Sitter KS benchmarks, and an intrinsic-curvature omission
negative control. State the analytic comparison argument in full.
THEOREM TARGET: bounded curvature requires b>=b_min>0. Complete affine
length would make U eventually positive; a/b then increases, keeping
a and thus 1/n bounded below. Continuous F is then bounded above, in
contradiction with the Q focusing bound. No power-law or limiting-n
assumption is permitted in the proof.
SCOPE: excludes a complete inward, bounded-curvature KS patch under these
conditions, not every inhomogeneous interior or continuation across a
coordinate horizon. The de Sitter benchmark must demonstrate the latter
distinction rather than be misclassified as globally singular.
FILES: completion-boundary checker, this report and index. No production
evolution, intuitive-file, physical-law or Git-rule changes.
STOP: record this family-level filter; do not scan further polynomials
inside the same excluded assumptions or claim all of RefG is rejected.

### Result: a family-level patch obstruction

All144 checks pass, including34 new section27 checks. The parent read
the new derivation and independently reran the entire suite with the
same result. Stage27 checker SHA256:
`07e1c2295dd1674bd2e931aa885852ed1f4086122bf6d546011c6e717918dd68`.
Direct unfixed-lapse variation verifies the off-shell identity

    dU/dt-NFa=-(b E_b-2a E_a)/(4K),

where E_a=d/dt(dL/dadot)-dL/da and likewise E_b. Thus the two independent
on-shell affine identities are

    U'=P F,
    Q'=-P^2 b n mu_eff/(4K a^2).

Here prime denotes affine differentiation, not density differentiation.
The comparison proof actually works for mu_eff>=0, including a vanishing
limit, not only the strictly positive branch in the contract:

1. If affine length were infinite, F>=F_min>0 would make U positive
   after a finite interval.
2. Then H_a-H_b>0, so a/b has a positive lower bound c_min.
3. Bounded KS curvature requires b>=b_min>0 because K>=4/b^4.
   Consequently a>=c_min b_min and n<=j/(c_min b_min^3).
4. Continuity of F on that compact density interval, including n=0,
   gives a finite F_max.
5. Q'<=0 and initially inward Q<0 give db/dlambda<=-|Q_1|/F_max.
   This contradicts b>=b_min within finite affine length.

No limiting density, power law or infinite proper-time assumption was
used. Schwarzschild and contracting de Sitter KS benchmarks verify the
signs; removing intrinsic sphere curvature from the actual Lagrangian
fails the unchanged identity. The de Sitter patch has finite K=24H^4
but ends at a regular metric horizon in finite affine length, so the
patch conclusion cannot be promoted to a global singularity theorem.
If a nonzero retained current j>0 is imposed at its a->0,b->1/H endpoint,
however, its invariant norm -n^2 diverges. A metric extension alone
does not extend that current smoothly; the vacuum j=0 control differs.

DECISION: further smooth nondegenerate density-only F(n) trials cannot
produce the specified complete inward KS core. Inhomogeneous dynamics,
an actual all-field extension, or a different physical source/response
structure must be evaluated on their own equations, not inherited from
this excluded class. This is not an exclusion of every RefG completion.

## 28. Finite dust ball, inner-horizon extension and centre-domain audit

### Contract before new independent checks

CLAIM_ID: W92_FINITE_BALL_LOCAL_EXTENSION_DOMAIN_V1.
GOAL: test the concrete extension left open by section24; do not confuse
the incomplete globally hyperbolic region with a curvature singularity.
MODEL: the already-derived matched flat dust ball and Hayward exterior,
G=1, ell>0, M>3sqrt(3)ell/4. No new field equation or source is introduced.
METHOD: at an inner root r_h use M=r_h^3/[2(r_h^2-ell^2)],
ell<r_h<sqrt(3)ell, kappa=-f'(r_h)/2>0. Substitute
V=exp(-kappa*v), r=r_h+V*y into the ingoing metric and verify the finite,
nondegenerate metric limit at V=0 and q(r_h)>0. Check the comoving dust
current's zero normal jump. Use the contracting finite ball's conformal
geodesics to distinguish its exit from the infinite-FLRW affine limit.
CENTRE CHECK: retain the action's q>0 domain. Compute coefficient and
full on-shell density limits independently; cancellation in the latter
must not be confused with a smooth off-shell variational extension.
PASS: exact local-horizon residuals and nonzero metric determinant,
finite horizon curvature, zero current boundary flux, and correctly scoped
centre limits. Record a local regular extension, not global completion.
FAIL / CONTROL: an arbitrary exponential rate must leave an uncancelled
1/V pole; a noncomoving current must fail the zero-flux matching condition.
BOUNDARY: a finite-affine ray leaving an infinite FLRW patch is not a
finite-ball singularity proof. The classical action at q=0 and dynamical
packet inner-horizon stability are separate, still required questions.
FILES: completion checker, report and index only. Production evolution
stays frozen. No copied third-party file, monograph edit or publication.
ADDITIONAL PROSPECTIVE JOIN CONTROL (before adding its tests): the
time-reversed dust ball is an existing same-action building block, not
a new equation. Test the proposed direct join by its necessary current
flux condition across a null vacuum/dust interface, and by continuity
of the finite-radius boundary velocity. A failed direct join does not
exclude another globally placed matter continuation with additional data.
STOP: decide which local extension is actually verified and isolate the
remaining central variational/domain problem before claiming completion.

### Result: local extension exists; it does not decide the global completion

The38 new section28 checks pass. In the final combined run the parent
independently reproduced all203 checks (48+22+40+34+38+21). Final checker
SHA256: `de2a3997c79c7b74a2cf7e64e546d65d62f508cb015c83194df99b3bcef910ef`.

At the inner root ell<r_h<sqrt(3)ell,

    kappa=(3ell^2-r_h^2)/(2r_h^3)>0,
    q_h=1-ell^2/r_h^2>0.

The explicit transformation V=exp(-kappa v), r=r_h+V*y gives

    g_Vy=-1/kappa,
    g_VV=-(f(r_h+Vy)+2kappa Vy)/(kappa^2 V^2),
    det(g_orbit)=-1/kappa^2,
    limit g_VV=-f''(r_h)y^2/(2kappa^2).

The rational metric is regular and nondegenerate across V=0. Horizon
curvature and freely falling tidal components are finite, and the local
action coefficients remain within q>0. An arbitrary exponential rate
leaves the expected uncancelled 1/V pole. This directly verifies a local
vacuum continuation and prevents promoting section24 to a universal
curvature-blow-up or no-extension claim.

For the finite contracting dust ball, |H|>=h0>0 after any finite launch
time gives a<=a0 exp(-h0 Delta_tau). Its available conformal distance
exceeds [exp(h0 Delta_tau)-1]/(a0 h0). Every radial null ray crosses at
most2chi_b before leaving the ball, hence exits by
Delta_tau<=log(1+2chi_b a0 h0)/h0. A comoving worldline instead retains
infinite future proper time. The finite affine length of an infinite
FLRW patch is therefore not a proof of a singularity in this finite ball.
The missing explicit current-jump check passes: the comoving interface
has zero normal dust flux.

The time-reversed expanding ball is a separate same-action building
block. Directly pasting it onto collapse at finite radius fails velocity
continuity, since the two nonzero velocities have opposite signs. Direct
attachment of nonzero timelike dust current to vacuum across a null
surface also fails: locally J.k=-n exp(+/-eta) is nonzero. These tests
exclude those direct joins, not every placement of additional matter
data beyond the original determined domain.

For the selected static vacuum centre q~r^3/(2Mell^2), and individual
coefficients diverge: h2~ -16M^2ell^2/r^4, h3~16M^2ell^4/r^5,
h4~ -2Mell^2/r. However, their full on-shell volume density is
D0~(36/ell^2)r^2 log(r/ell), which tends to zero and is integrable.
The coefficient poles therefore do not prove a divergent on-shell
action, strong coupling or curvature singularity. The unresolved issue
is the off-shell central variational/domain extension in section29.

## 29. Central variational prescription, beyond the on-shell density

### Contract before independent verification

CLAIM_ID: W92_HAYWARD_CENTRE_VARIATIONAL_DOMAIN_V1.
GOAL: decide whether a finite metric and finite on-shell action density
already supply a source-free variational extension through q=0.
The lapse-variation surface term was identified in an exploratory audit;
its independent exact test and interpretation are registered here.
MODEL: unchanged spherical action, generic static lapse N(r) retained
until variation, and only then the vacuum Hayward metric f(r). Positive
M,ell and r>0; the centre is a limit of that open domain, not silently
added to it. Test regular radial lapse perturbations eta=1 and eta=r^2
near r=0, compactly supported at larger radius.
METHOD: derive delta L=eta D0+eta' A+eta'' B from the full reduced action;
verify the punctured-domain Euler identity D0-A'+B''=0 and the central
flux eta(A-B')+eta'B. Check general-M,ell limits and the finite on-shell
density separately. Examine ordinary total-derivative/boundary freedoms
explicitly before interpreting a nonzero bare-action flux.
PASS: exact bulk cancellation, reproducible central flux and a negative
control showing why setting N=1 before varying misses the issue.
Any scalar coefficient pole is not by itself a curvature singularity,
divergent on-shell action or proof of strong coupling.
SCOPE: whether the currently written action and unrestricted regular
variations suffice at the centre. A required boundary/domain prescription
is a missing completion, not a theorem forbidding every completion.
ERROR / FREEDOM: symbolic limits, no fitted central cutoff or silently
added boundary source. New counterterms, boundary degrees of freedom or
matter profiles must be separately identified, not called already derived.
FILES: completion checker, report and index only. No change to production
evolution or the intuitive monographs.
STOP: state the exact central condition still required, and whether the
current calculation supplies it; do not conflate regular metric extension
with a proven regular solution of all fields and variational equations.

### Result: the written action needs a central prescription

The21 new section29 checks and all preceding checks pass203/203,
independently repeated by the parent at the section28 final hash. For
G=1, varying the independent static lapse gives

    delta L=eta D0+eta' A+eta'' B,
    D0-A'+B''=0 for r>0,
    limit(A-B')=-4M, limit(rB)=4Mell^2.

For a regular local perturbation eta=eta0+eta2*r^2+..., the lower
endpoint bracket is -4M eta0+8Mell^2 eta2. With compact outer support
and action prefactor1/4, the corresponding bare-action variation is
M eta0-2Mell^2 eta2. Fixing the lapse before variation erases this
equation and fails the registered control.

Boundary freedom is explicitly retained, not dismissed. The exact
reduction is L=B_total'+4N mu', with
B_total=-r^2 H4(N f'+2f N'). Subtracting that total derivative removes
the displayed bare lapse flux; varying f then leaves4N delta_mu at
the centre. A further Legendre boundary exchanges it for-4mu delta_N.
These are different variational prescriptions, not a demonstrated
source-free completion with all regular variations unrestricted.

The central domain issue is visible independently in

    delta_mu=-r delta_f/(2q^2).

Take delta_f=epsilon*r^2 near the centre, with a smooth outer cutoff
and0<epsilon<ell^-2. Then delta_mu~ -2M^2ell^4 epsilon/r^3.
For z=z_Hayward-epsilon, the centre-first limit of mu is0 whereas the
variation-first limit isM. This is a nonuniform constitutive limit,
not divergent spacetime curvature. A radial r^5 control gives finite
delta_mu; no C-infinity Cartesian smoothness is inferred from that test.

DECISION: the current bare action, metric limit and finite on-shell
density do not by themselves specify a regular central variational
completion. A boundary/domain prescription or an independently solved
matter-containing continuation is still needed. No new centre source,
cutoff or counterterm is adopted here. This conclusion concerns the
chosen static vacuum continuation; other global continuations have not
been classified or excluded.

## 30. Check the unexcluded coupled-current branch before rejecting it

### Bounded action-reduction contract

CLAIM_ID: W92_CURRENT_COUPLED_RADIAL_OPERATOR_ENTRY_V1.
GOAL: determine whether the negative-mu branch, left outside sections26–27,
can be tested with the full existing action rather than the insufficient
fixed-geometry current block. No negative phase rate is identified with
reversed physical time or automatically with a coupled ghost.
MODEL: unchanged W87 F(n)T/current action, with the section26 constitutive
candidate available but no new one introduced. For a radial reduction use
ds^2=-N^2dt^2+a^2(dx+Bdt)^2+b^2dOmega^2, densitized current (j,i)sin(theta),
n=sqrt(N^2 j^2-a^2(i+Bj)^2)/(N a b^2). Keep the flat-spin/Lorentz variables
required by spherical symmetry, the lapse, shift and both current
components independent. The action includes j theta_dot+i theta_x.
METHOD: derive the torsion/reduced action before eliminating constraints;
retain density–torsion mixing and test the valid W89 KS limit and TEGR
boundary identity. Only if this entry test succeeds is a leading radial
constraint/principal calculation justified. Existing minimal-current,
f(T), KGB and frozen-background operators are not interchangeable here.
PASS: consistent complete spherical reduction and explicit surviving
constraints, or one decisive obstruction to that reduction. A partial
quadratic block does not establish full health or full instability.
FALSIFIER: missing antisymmetric equations, wrong KS torsion, lost lapse
constraint or a division through mu=0 without a rank check invalidates
the proposed operator. A failed ansatz is not a theory no-go.
FILES: prospective verification belongs only in the completion checker
and this report/index. Production evolution and monographs stay frozen.
STOP: the action-entry/principal decision, not an unrestricted 3+1
Hamiltonian programme or a new numerical collapse. This stage is needed
to avoid rejecting an unresolved branch using the wrong health test.

### Action-entry result

In sections30-32, F(n) denotes the density-dependent torsion coefficient,
not the metric trapping function F printed by the collapse code.

The complete spherical reduction retains four metric functions and the
independent radial boost psi and tangential rotation chi. This local
frame/spin parametrization follows the spherical classification in[3];
the density-current coupling below is derived from W87, not imported
from a different f(T) perturbation operator. The direct torsion contraction
recovers T=4H_a*H_b+2H_b^2-2/b^2 on the W89 KS branch
(psi=0,chi=pi/2), and T=0 for the inertial Minkowski control.

After the TEGR integration by parts, the nonminimal Lorentz-dependent
piece of the reduced Lagrangian is

    L_L=2K b^2(F_x psi_t-F_t psi_x)
        +4K N a b cos(chi)[-F0 sinh(psi)+F1 cosh(psi)],
    F0=(F_t-B F_x)/N, F1=F_x/a.

Writing d_r=b_x/(a*b), its two spin equations are

    F0[b*d_r-cos(chi)cosh(psi)]
      +F1[cos(chi)sinh(psi)-b*H_b]=0,
    sin(chi)[F0 sinh(psi)-F1 cosh(psi)]=0.

Direct antisymmetric field-equation contraction gives the same two
equations; the other four spherical components vanish. Fixing both
Lorentz variables to their homogeneous values before radial variation
would lose these equations and the resulting gradient contribution.
The independent lapse, shift and both current components are retained.
This establishes the entry to the constrained radial calculation, not
stability by itself. The executable aggregate is recorded after section32.

## 31. Full constrained radial health, without a frozen geometry

### Verification contract after exploratory action derivation

CLAIM_ID: W92_COUPLED_CURRENT_RADIAL_PRINCIPAL_V1.
GOAL: test the remaining inward, density-increasing F(n)T branch with
the actual coupled spherical action. The formulas below were derived
exploratorily by the parent and independently crosschecked before this
executable-verification contract; this is not a blind prediction claim.
MODEL: unchanged section30 action, regular KS background, K>0,F>0,
n>0,a>0,b>0. Retain lapse, shift, flux, radial boost and tangential
rotation until their equations are obtained. For the nonzero radial
Fourier mode use the spatial-flat gauge only when H_b is nonzero.
Do not divide through mu=0, F_dot=0 or H_b=0.
HYPOTHESIS: with V3=a*b^2, Fp=dF/dn and d=delta(j), the constrained
first-order quadratic action has density Hamiltonian coefficient
A(k)=[h_eff+8K H_b Fp*k^2/(a^2*n_dot)]/V3, where
h_eff=rho''+K*T*F''+2rho'*Fp/F-4K*Fp^2/(F*b^2).
Its phase coefficient is B(k)=j*k^2/(mu*a^2)+O(1), and hence the leading
radial frequency squared is 8K*n*H_b*Fp*k^4/(mu*a^4*n_dot).
METHOD: independently verify spherical torsion, both surviving flat-spin
equations, the TEGR boundary relation, quadratic expansion before flux
elimination, lapse/shift constraints, and the reduced principal operator.
Use Fp=0 as the minimal-fluid control and retain the undivided mu=0
flux equation as a rank boundary. Wrong-spin/freezing and dropped-mixing
controls must fail the unchanged comparison equations.
PASS: exact identities and independently audited gauge/constraint rank;
state the sign result only for H_b<0,n_dot>0,Fp>0 and the nonsingular
elimination domain. Oscillatory frequencies alone are not positive energy.
SCOPE: a necessary radial continuum-health condition, not a complete
3+1 stability theorem or a singularity theorem. Without an independently
specified ultraviolet cutoff, do not claim a measured physical unstable
wavelength range. Degenerate surfaces and density-decreasing branches
remain separate; one failed constitutive family is not all of RefG.
FILES: completion checker, this report and the index only; production
evolution remains frozen. No new action, cutoff or phenomenological force.
STOP: decide this branch from its own constrained equations, then combine
with the fixed numerical refinement and existing global/domain results.

### Result: the coupled radial operator excludes the tested healthy route

Let V3=a*b^2, j=n*V3, d=delta(j), pi=delta(theta), phi=delta(N),
and mu=rho'+K*T*Fp. The two coordinate conditions delta(a)=delta(b)=0
have Fourier gauge determinant i*k*a*b_dot, so this gauge is admissible
on k*H_b!=0. The Lorentz equations are eliminated only for F_dot!=0.
The undivided current-flux equation is retained at mu=0; no conclusion
requiring division by mu is extended to that surface.

For the regular domain, the independently expanded quadratic action gives

    phi=Fp*d/(V3*F)+n*pi/(4K*F*H_b),
    L2=d*pi_dot-[A(k)*d^2+2C*d*pi+B(k)*pi^2]/2,
    A(k)=[h_eff+8K*H_b*Fp*k^2/(a^2*n_dot)]/V3,
    h_eff=rho''+K*T*F''+2rho'*Fp/F-4K*Fp^2/(F*b^2),
    B(k)=j*k^2/(mu*a^2)+V3*n^2*(4H_a*H_b+2H_b^2)/(8K*F*H_b^2),
    C=n*mu/(4K*F*H_b).

The remaining lapse equation determines the shift gradient; it does not
remove the surviving canonical pair. Independent derivations starting
with the original current norm agree with this reduction. The leading
frozen-coefficient radial frequency is therefore

    omega^2=8K*n*H_b*Fp*k^4/(mu*a^4*n_dot)+O(k^2).

For inward density increase, H_b<0,n_dot>0,Fp>0:

- mu>0 gives A<0,B>0 at sufficiently large k, hence a radial gradient
  instability, not a restoring oscillation.
- mu<0 gives A<0,B<0: frequencies can be oscillatory, but the reduced
  phase kinetic term is negative, 1/(2A)<0, relative to positive-F gravity.

More generally, mu<0 makes the high-frequency phase Hamiltonian
coefficient negative on every regular patch of this reduction: either a
negative kinetic sign or an unstable frequency remains. This is an
instantaneous high-frequency statement on an evolving background, not
a conserved global energy assertion or reversal of an observer's time.
The Fp=0 control recovers the minimally coupled fluid's principal sound
coefficient n*rho''/rho'. Thus the negative conclusion is obtained from
the actual coupled action, not from the previously insufficient
fixed-geometry current block.

DECISION: the linear and quadratic positive-slope density-only joins
cannot be accepted as healthy inward density-increasing continuum cores
on this nondegenerate domain. No ultraviolet cutoff is supplied by the
present model; none is invented to hide the large-k sign. If a finite
effective-theory cutoff is independently derived, its relation to the
instability scale must be checked before making a physical wavelength
claim. Degenerate open branches, non-KS backgrounds and the different
spherical saturation action are not silently included in this result.

## 32. Constant-density degeneracy of the same inward KS branch

### Bounded verification contract

CLAIM_ID: W92_CONSTANT_DENSITY_KS_PIVOT_V1.
GOAL: check the open-interval F_dot=0 case excluded from the section31
division, rather than treating that division as a universal obstruction.
The identities were found analytically before these executable checks.
MODEL: the same W87/W89 action, j>0,F>0,Fp>0, regular a,b>0 and a
connected KS interval on which F_dot=0. No changed action or source.
METHOD: current conservation fixes n=n0 and V3=a*b^2, so H_a=-2H_b.
Use the already varied lapse equation and anisotropy identity to test
H_b_dot=-1/(3b^2), b_dot^2=1/3-c*b^2, b_ddot=-c*b,
where c=rho(n0)/(6K F(n0)) is constant. These are necessary subsystem
identities, not by themselves a constructed solution. Independently test
the remaining scale equation: the exploratory peer audit gives
(4/3-2beta)/b^2+[n*rho'-2rho+beta*rho]/(2KF)=0, beta=nFp/F.
An open changing-b interval would then require beta=2/3 and n*rho'=4rho/3;
positive dust may fail this stronger compatibility condition altogether.
Only if all equations admit the branch, check the proper-time endpoint
and K>=4/b^4, retaining the possibility of leaving this interval first.
PASS: exact residuals and finite inward time to b=0 if this entire
constant-density branch is retained. For c>=0 the inward speed does
not decrease; for c<0 its magnitude is at least1/sqrt(3). At c>0 a
zero-speed point is a maximum radius, not a contraction-to-expansion
bounce. A wrong sign in the intrinsic sphere term must fail a control.
BOUNDARY: this does not classify every rank-degenerate background.
An isolated F_dot=0 point is not an open constant-density solution;
mu=0 remains within section27's nonnegative-mu comparison assumptions.
No conclusion is transferred to the different spherical saturation action.
FILES: completion checker, this report and index only.
STOP: close this particular pivot loophole, then report the exact
candidate exclusions and the limits of what the available theory decides.

### Result: the retained dust branch does not have this escape

The full radial and angular Euler-Lagrange equations were differentiated
before imposing constant density. Both independently give

    (4/3-2beta)/b^2+[n*rho'-2rho+beta*rho]/(2KF)=0.

Since b changes on an open inward interval while n=n0 is fixed, the
two coefficients require beta=2/3 and n*rho'=4rho/3. Positive dust
rho=m*n instead leaves the nonzero residual -rho/(6KF). Thus the
retained W89 coframe/flat-spin branch has no such open constant-density
dust solution; the lapse/shear subsystem alone must not be called one.

For a different constitutive source that does satisfy all the equations,
the necessary subsystem has b_dot^2=1/3-c*b^2 and b_ddot=-c*b. If it is
retained for the entire inward continuation, its proper-time endpoint is

    asin(sqrt(3c)*b0)/sqrt(c)        for c>0,
    sqrt(3)*b0                     for c=0,
    asinh(sqrt(-3c)*b0)/sqrt(-c)     for c<0.

Each is finite on the real inward branch. Its direct curvature contraction
gives b^4*Kretschmann->80/3. The exact test corrected an auxiliary
hand-entered endpoint coefficient32 to80/3; no action, physical parameter
or acceptance tolerance was changed. This conditional endpoint is not
asserted for the excluded dust solution or for a trajectory that leaves
the constant-density interval first.

### Combined retained-branch decision

For smooth positive-slope density-only dust F(n)T with F>=F_min>0 and F
finite and continuous on bounded density intervals including zero, the
retained W89 coframe/flat-spin branch cannot provide a future-affine-
complete, bounded-curvature, persistent inward KS core that is continuum-
healthy at every regular point. The same branch and KS patch must cover
the whole proposed continuation, including any degenerate intervals.

Proof: a negative-mu point gives an open negative interval by continuity.
Section32 forbids this entire inward dust interval from having F_dot=0.
It therefore contains a regular point where section31's negative phase
Hamiltonian coefficient violates the necessary radial health condition.
Health consequently requires mu>=0 throughout; section27 then excludes
the proposed complete bounded-curvature inward patch. Isolated zero-mu
or zero-F_dot points do not remove that argument.

This is a scoped constitutive-branch exclusion, not a theorem against
bounces, different spin branches, inhomogeneous interiors, global
extensions, the separate spherical saturation action, or RefG generally.
The high-frequency continuum qualification is essential; no missing
ultraviolet completion is silently treated as already tested.

### Existing-resource crosscheck: no ready-made term was omitted

The [W87 action contract](../W3-87_State_Dependent_Gravitational_Response/w3_87_state_dependent_response_contract.md),
sections1-2, already includes the induced pressure n*K*T*Fp and the
weighted-TEGR bulk derivative term. Both enter sections30-31; adding
that pressure again would double count it. The separate five-field
medium in [the W92 formal integration](FORMAL_COVARIANT_MEDIUM_INTEGRATION.md)
is not a missing operator of this density-only action.

The existing cubic derivative-medium prototype is also retained, not
forgotten: the W92 main diagnostic's stages27-29 and
[source-response audit](matter_medium_source_response.md) contain a
genuine local healthy negative-null-source example. Its registered
ordinary-exterior and direct pressure-identification tests do not give
the missing full connection. Installing it here would change the action
and require a new source/pressure derivation; its local PASS is not a
ready-made completion of the rejected join. This inventory is a read-only
check of existing results, not a new rejection of all derivative models.

### Reproduction of the completed analytic audit

The parent independently reran the complete checker:293/293 PASS, no
failed checks. The original203 checks are retained; section30 adds20,
section31 adds43, and section32 adds27. These passes verify both positive
identities and the stated negative results; they do not mean293 proofs
of singularity removal. Checker SHA256:
`dbf26e1b50aba9612a13d3fa2b766d819b5b268dabc4f23c14792f46a961513c`.
The production verifier remains at the section23 preregistered hash.

## 33. Regular-centre source and common-readout compatibility

### Bounded verification contract (2026-09-14)

GOAL: decide whether the existing finite-source regular centre can retain
the exact static isotropic common clock/rod readout all the way to the
selected saturation limit. This is the specific missing comparison after
the source construction in sections1 and6; those constructions are reused.

CLAIM_ID: W3-92-SAT-CENTRAL-SOURCE-READOUT-33.
TYPE: exact local necessary-condition test and source-ledger audit.
MODEL_VERSION: unchanged spherical rational action h(z)=z/(1-ell^2 z),
unchanged canonical sextic matter; no W87 F(n)T substitution.
ASSUMPTIONS/DOMAIN: smooth static isotropic centre, alpha>0, ell>0,
finite nonnegative material density, generalized M(0)=0, positive finite
central lapse, 0<=u=ell^2 z_c<1. Nonvacuum division requires rho_c>0.
The additional tested readout is ds^2=-p(s)^2dt^2+p(s)^(-2)
[ds^2+s^2dOmega^2], p=p0+p2 s^2+O(s^4).
CONVENTIONS: signature -+++, r=s/p is areal radius, N_lapse=sigma sqrt(B);
q=1-u is the action response, p0 is the clock normalization, and P_c is
mechanical material pressure. These three quantities stay distinct.
FREEDOM_LEDGER: alpha,ell retain their action roles; p0,p2 and scalar
central data are local test variables, not fitted object parameters.
DEPENDENCIES: sections1,4,6,13,28,29; common_scale_centre_source.md section1.
METHOD: derive centre jets independently from the isotropic metric and
from the mass/lapse constraints; compare them with the canonical stress.
Audit the exact vacuum Hayward target in both the modified-action and
Einstein-effective ledgers. No nonlinear evolution is needed.
PASS_CONDITION: both derivations and source ledgers agree; admissible and
inadmissible local controls are correctly distinguished.
FAIL_CONDITION/FALSIFIER: any nonzero exact identity residual, lost
regular-source branch, or a valid nonnegative-potential counterexample
to the claimed necessary restriction.
RESIDUAL/ERROR_BOUND: exact symbolic residuals; only leading centre
coefficients are claimed, with O(r^4) metric remainder.
VALIDITY_HEALTH: scalar positivity is a necessary local matter test;
global solutions, coupled perturbative health and dynamical persistence
are outside this step.
BRANCHES: zero-density limit is separate; the M(0)>0 vacuum saturation
limit is compared separately, without dividing by q=0.
OBSERVABLE_MAP: local clock/rod jets and invariant central curvature;
q is not identified with foundation pressure or clock p0.
FORWARD_MODEL/DATA_ROLE: N/A, no observational data or astrophysical fit.
IDENTIFIABILITY: necessary local compatibility, not a unique source
reconstruction or a sufficient black-hole existence theorem.
BENCHMARK: constant-scale flat centre, ell->0 common-scale pressure,
retained positive sextic and the same-action vacuum Hayward geometry.
CROSSCHECK: independent derivation by a second agent; separate curvature
and mass-ledger identities plus the preceding verification suite.
CLOSURE_FLAGS initially false: central_comparison_verified,
common_readout_restriction_verified, full_pressure_join,
global_black_hole, perturbative_stability.
PROVENANCE: exploratory hand derivation preceded this contract; exact
verification follows. This is not a blind prediction.
FILES: this report, verify_saturation_completion_boundary.py and the
existing medium_health_horizon_diagnostic.md index only.
STOP: record the exact compatibility range and missing physical join;
do not repeat the 70-time evolution or open a new constitutive family.

### Result: the additional static readout restriction is identified

All42 new checks and all293 preceding checks pass: **335/335**, failed=[].
The full suite ran from the unchanged section23 production hash
`1a23833cd7bc907da7bdda32f26c8ced9ec866f298423a646fb4827f7ce40500`.
The completed checker's hash is
`34b60949d239d88215430f0ce4298f815def9a9824dca3736c59d3baa3742e2d`.
A second agent independently derived the coordinate/source relations and
then read the implementation; a separate read-only repository inventory
confirmed the distinction from the earlier centre tests.

**Already available:** sections1 and6 constructed the canonical sourced
regular centre, including the independent lapse equation and central
curvature bound. W3-85's regular-centre test and
[inverse_saturation_candidate.md](inverse_saturation_candidate.md) already
reconstructed the vacuum target's effective Einstein tensor.
[common_scale_centre_source.md](common_scale_centre_source.md) already
tested a different Einstein/medium common-scale source. Their results
are retained; the new question is the local compatibility of exact static
common scaling with this spherical saturation action.

For the smooth isotropic scale p(s)=p0+p2 s^2+O(s^4), the areal map gives

    r=s/p, B=(1-s p'/p)^2,
    z_c=4p0 p2, N_lapse=p0[1+(z_c/4)r^2+O(r^4)].

The two source constraints of section6 instead give

    rho_c=3z_c/(2alpha q_c), q_c=1-u, u=ell^2 z_c,
    N_lapse=N_c[1+n_2 r^2+O(r^4)],
    n_2=alpha q_c^2(rho_c+P_c)/2-z_c/2.

Equating the two lapse coefficients, with rho_c>0, yields

    P_c/rho_c = u/(1-u).

This is a condition on mechanical material stress for the additional
static metric restriction. The actual retained canonical scalar has

    rho_c=W_c/2+V_c, P_c=W_c/2-V_c,
    V_c/W_c=(1-2u)/2.

Nonnegative V_c requires u<=1/2. The retained sextic
V(chi)=chi^2[(chi^2-3)^2+3]/24 is strictly positive for chi!=0, giving
**u<1/2, q_c>1/2** on the nonzero smooth harmonic central branch.
Thus the unchanged canonical source and this exact static common
clock/rod restriction cannot jointly approach the selected u->1 centre.

The independent sectional-curvature calculation gives
K_c=48n_2^2+12z_c^2, hence K_c=15z_c^2 under the common readout.
The zero-density limit is flat at central order. A positive leading
central-jet control uses chi_c=1, ell=1, alpha=4/7:
V_c=7/24, W_c=7/6, rho_c=7/8, P_c=7/24, u=1/4 and n_2=1/16.
Its leading scalar equation gives chi_2=-11/72. This verifies the
retained central coefficients; it does not establish an all-orders or
global solution under the extra readout restriction.

A control with u=3/4 and P_c=0 has finite density and curvature when
the lapse is allowed its independently solved coefficient
n_2=-5z_c/16. Therefore the new obstruction belongs specifically to
the locked static readout. It is not an exclusion of low-q regular
source data. In particular **q_c is not p0**: p0 cancels from the
compatibility relation. The result gives no lower bound on the local
clock normalization or foundation pressure.

### Exact target and the energy ledger

For the original constant-generalized-mass Hayward target,

    z=2alpha M0/(r^3+2alpha ell^2 M0), sigma=1,
    M_generalized=M0, rho_material=M_generalized'/r^2=0  (r>0).

The remaining radial equation is vacuum as well. In an alternative
Einstein representation the same metric has

    rho_effective=6alpha ell^2 M0^2/(r^3+2alpha ell^2 M0)^2,
    P_r,effective=-rho_effective,
    P_t,effective=(3q-1)rho_effective.

Its central effective density is 3/(2alpha ell^2). These are two
representations of the gravitational equations; adding the effective
tensor as extra matter to the modified-action equation double counts
the response. The geometric mass tends to zero at the centre and to
M0 at infinity, while the vacuum generalized mass is M0 throughout
r>0. The finite smooth material centre has M_generalized(0)=0.
Section29's variational prescription remains relevant to the different
M0>0 central limit.

The vacuum central lapse has n_2=-1/(2ell^2). The exact common readout
at z_c=1/ell^2 requires n_2=+1/(4ell^2), an explicit mismatch of
-3/(4ell^2). Both statements concern metric coefficients; the vacuum
target still has its already verified finite central curvature.

### Decision and stopping point

The proposed source comparison is now localized to a definite
mathematical incompatibility: the unchanged spherical saturation action,
the retained canonical source, and the exact static common-scale
strong-field extrapolation cannot all realize the selected saturated
centre together. The weak-field common-scale readout in
`intuitive/RefG_GE.md` section2.2 is not silently promoted to a universal
static strong-field law by this test.

The full RefG join requires a same-action physical derivation relating
foundation pressure to the temporal and spatial metric components in
the actual strong-field state. Simply renaming q as p, prescribing
the desired centre, or adding its effective Einstein density as matter
does not provide that derivation. No new constitutive law is introduced
by this step. Central-source comparison and its restriction are verified;
full pressure join, global black-hole regularity and perturbative
stability remain unestablished. No additional time evolution was run.
The intuitive monographs, speculative folder, Git rules and production
evolution equations are unchanged.

## 34. Time-dependent common readout and a canonical central source

### Bounded verification contract (2026-09-14)

CLAIM_ID: W3-92-SAT-DYNAMIC-COMMON-CENTRE-34.
GOAL/CLAIM: decide whether the section33 static source restriction also
holds for time-dependent common clock/rod scaling by checking a charged
canonical central jet in its excluded static range.
TYPE: exact local source/metric compatibility and negative-control test.
MODEL_VERSION: unchanged spherical rational action and canonical sextic;
p(t,s) is allowed time dependence, with zero shift, while the exact
common metric ds^2=-p^2dt^2+p^(-2)(ds^2+s^2dOmega^2) is retained.
ASSUMPTIONS/DOMAIN: p0>0, smooth isotropic centre, r=s/p, finite source,
M(0)=0, alpha,ell>0, 0<u=ell^2 z<1. Statements concern retained central
Taylor coefficients at one event, not an all-orders or global solution.
CONVENTIONS: normal proper derivative dot=p0^(-1)partial_t, normal
expansion H=-partial_t p0/p0^2, z_s=4p0 p2. J=T_01 is the covariant
energy component; positive J corresponds to inward physical energy flux.
FREEDOM_LEDGER: p0,H,z,zdot and central complex scalar data are local
initial-jet choices, not fitted observables or a new constitutive law.
DEPENDENCIES: sections1,13,33. H=Hdot=0 must recover section33.
METHOD: direct orbit metric/curvature calculation and the original
orbit field equations; independent central conservation and complex
scalar equation; nonzero phase-current conservation.
PASS_CONDITION: an exact local witness with pdot<0, u>1/2, positive
canonical potential and finite curvature satisfies all retained central
metric, source, scalar and flux equations. Its static or flux-deleted
counterparts must fail their registered equations.
FAIL_CONDITION/FALSIFIER: nonzero exact residual, wrong flux/time sign,
or reliance on independent unconstrained source changes.
RESIDUAL/ERROR_BOUND: exact symbolic central coefficients; metric/source
diagonal equations at order r^0 after normalization, mixed equation
through its leading order r, no error claim beyond these Taylor orders.
VALIDITY_HEALTH: canonical positive kinetic energy and potential at the
tested event; coupled PDE health, existence and stability remain separate.
BRANCHES: static limit and zero-spatial-curvature homogeneous limit
checked separately; no vacuum q=0 substitution or exterior join.
OBSERVABLE_MAP: local clock p0, normal expansion, actual scalar stress,
phase current and central curvature. q is not foundation pressure.
FORWARD_MODEL/DATA_ROLE/IDENTIFIABILITY: N/A for observational inference;
this is a local counterexample to extending the static restriction.
BENCHMARK: static section33, homogeneous section2, canonical zero flux.
CROSSCHECK: independent agent derivation; direct metric versus
already-varied source equations; matter/phase continuity from the scalar.
CLOSURE_FLAGS initially false: dynamic_central_compatibility,
static_restriction_not_universal, foundation_pressure_join,
all_orders_solution, global_regular_black_hole, perturbative_stability.
PROVENANCE: exploratory central derivation and rational witness were
specified before this verification; not a blind prediction.
FILES: existing completion checker, this report and main diagnostic index.
STOP: decide this local compatibility question, record the actual flux
and expansion interpretation, and stop without a time-extension run or
a new action.

### Result: the dynamic common-readout central jet passes

The independent central derivation gives

    z=H^2+z_s, rho=3z/(2alpha q),
    Hdot=-3H^2/2+3zu/2-alpha q^2 P,
    P/rho=u/q-(2Hdot+3H^2)/(3zq),
    J=j1 r+O(r^3),
    j1=(z_sdot+3H z_s)/(2alpha q^2),
    rhodot+3H(rho+P)=3j1.

It reproduces section33 when H=Hdot=0. These temporal terms permit
canonical central stresses in the formerly excluded static range.

A specified charged canonical witness has alpha=ell=1, z=u=3/4,
q=1/4, H=1/4, Hdot=53/96, zdot=1/8. At the event phi0=2,
Pi=i sqrt(23/3), with spatial coefficient
kappa=i35/[24 sqrt(23/3)] in phi=phi0+kappa r^2+O(r^4).
The unchanged sextic gives V=2/3, rho=9/2, P=19/6. Its mixed
energy coefficient is j1=35/12, and its scalar equation fixes
Pi_dot=-2+3i/sqrt(23/3), giving rhodot=3. Energy and conserved
phase-current continuity agree in an independent hand derivation.

The common clock scale is p0=1/2 with proper derivative -1/8.
The positive normal-grid expansion H=1/4 is distinct from material
flow: both the energy-rest and charge-flow normal-frame velocities
have leading coefficient -35/92, so their areal rate is
u_flow(r)=-3r/23+O(r^3). The source therefore contracts locally
while the common clock scale decreases. The expected central
curvature is K=1465/192 and Ricci scalar is 49/8, both finite.
The selected equality of qdot and p0dot is accidental; q and p0
are distinct variables with different values at this event.

The new function dynamic_common_centre_checks in the existing
completion checker independently reconstructs the orbit metric,
angular equation, scalar source and central curvature. All43 new
checks and335 preceding checks pass: **378/378**, failed=[].
The direct orbit density, radial pressure, leading mixed flux and
angular pressure reproduce the specified canonical source. A separate
agent independently derived the equations, audited the local-flow
interpretation and reviewed the implementation.

The first running verification was interrupted while forming an
unnecessarily large rational expression. The final implementation
takes the exact finite limits of normalized factors before their
products; the action, witness and acceptance conditions are identical.
The full successful checker hash is
`74a02d77217cf5ea8918c72c6c4b13f09c9469d40fc551a6b7ffcd7c8f017e1d`.
The production evolution retains hash
`1a23833cd7bc907da7bdda32f26c8ced9ec866f298423a646fb4827f7ce40500`.
Initial approval-service launch failures occurred before execution
and supply no physical or numerical result.

This resolves the question posed in section34: the particular static
restriction of section33 is not a universal consequence of common
clock/rod scaling. Time dependence and a conserved canonical source
are locally compatible without a new action or negative potential.

This is a finite-order central construction. An all-orders solution,
propagation through an interior, the foundation-pressure derivation,
horizon matching and dynamical stability are still separate tasks.
The original production evolution and intuitive monographs are unchanged.

## 35. First continuation and the full spatial compatibility condition

### Bounded verification contract (2026-09-14)

CLAIM_ID: W3-92-SAT-CENTRAL-PROLONGATION-35.
GOAL: decide the section34 event's first nontrivial spatial and temporal
compatibility, then use a full spatial identity to check whether the
same globally imposed metric restriction can have a standard isolated
finite-mass exterior. This replaces an unbounded Taylor-coefficient ladder.
TYPE: exact finite-order compatibility and conditional asymptotic filter.
MODEL_VERSION: unchanged common p(t,s), zero shift, canonical complex
sextic and spherical rational action. General alpha,ell for the identity;
alpha=ell=1 and all section34 lower jets fixed for the example.
ASSUMPTIONS/DOMAIN: smooth even profiles, p0=1/2,q0=1/4 near the centre;
0<q throughout any domain used in the full identity.
CONVENTIONS: r=s/p, n=p^(-1)partial_t, e=p partial_s, k=e ln p=p_s.
Un=Hess_nn(r)/r, Ue=Hess_ee(r)/r, Une=Hess_ne(r)/r;
rho,Pr,Pt,J are the actual source in that orthonormal frame.
FREEDOM_LEDGER: solve p4,p2_tt,Im(phi2_t), and the necessary p0_ttt.
Re(phi2_t) remains free if absent from the retained equations.
EXTERIOR ASSUMPTIONS: differentiated asymptotic expansion
p=1-m/s+O(s^-2), p_s=m/s^2+O(s^-3), p_t=O(s^-2),
fixed finite ell, and rho,Pr,J=O(s^-3-epsilon), epsilon>0.
For canonical matter Pr-Pt>=0. These are a restricted isolated
spatial-infinity class, not arbitrary time-dependent infinity.
DEPENDENCIES: section34 event and KG; already-varied orbit/angular
equations. Do not substitute an Einstein-effective tensor as extra matter.
METHOD: derive compact equations before expansion; solve the finite
coefficient system and check the t derivative of the leading mixed
constraint; independently derive an exact unexpanded spatial identity
and its exterior powers.
PASS_CONDITION: finite coefficient solution with zero residual and
correct constraint propagation. The exterior filter has its own outcome;
passing local conditions does not preselect its result.
FAIL_CONDITION/FALSIFIER: inconsistent coefficients, changed frozen
lower data, nonzero identity residual, or a counterexample satisfying
all stated exterior assumptions.
RESIDUAL/ERROR_BOUND: normalized diagonal equations through s^2,
mixed through s and its t derivative at the event. Exact spatial
identity on q>0; explicit asymptotic remainders, no numerical error.
VALIDITY_HEALTH: only local canonical signs; no full stability claim.
BRANCHES: declare matrix rank/free data; the exterior statement
excludes only the globally exact common-p branch with stated falloffs.
OBSERVABLE_MAP: local clock/source/flow; m is the ADM mass parameter
of this standard asymptotic conformal spatial metric, not q or p0.
FORWARD_MODEL/DATA_ROLE/IDENTIFIABILITY: no observed data or fit;
conditional mathematical compatibility, not unique physical origin.
BENCHMARK/CROSSCHECK: section34, direct connection algebra,
independent agent calculations, perturbed coefficients, ell->0 and
zero-mass controls.
CLOSURE_FLAGS initially false: first_radial_compatibility,
leading_momentum_propagation, full_spatial_identity,
specified_isolated_extension_excluded, full_RefG_rejected,
global_regular_black_hole.
PROVENANCE: compact geometric and independent coefficient derivations
preceded runtime verification. An initial contract write failed at the
approval service; this complete contract is not a blind prediction.
FILES: existing completion checker, this report and main diagnostic index.
STOP: decide these concrete compatibility questions; do not continue
a Taylor ladder, tune an exterior profile or change the physical action.

### Result: finite-order compatibility passes; the specified isolated end fails

The three diagonal metric/source equations at order s^2 have rank three.
With every section34 lower coefficient fixed, they give exactly

\[
p_4=\frac{16603}{812544},\qquad
p_{2,tt}=-\frac{392533}{3250176},\qquad
\operatorname{Im}\phi_{2,t}=\frac{12353\sqrt{69}}{292008}.
\]

For A=sqrt(23/3), the independently obtained geometric coefficients are

\[
\rho_2=160p_4-\frac{35}{8},\quad
P_{r2}=\frac{736}{3}p_4+128p_{2,tt}+\frac{1345}{144},\quad
P_{t2}=\frac{1472}{3}p_4+128p_{2,tt}-\frac19.
\]

They equal the unchanged scalar coefficients. Re(phi2_t) is absent at
this order and remains free; it was not set to zero. The necessary time
derivative of the leading mixed constraint is also compatible:

\[
(J_{1,t})_{\rm geometry}=64p_{2,tt}+\frac{875}{96},\qquad
(J_{1,t})_{\rm scalar}=A\operatorname{Im}\phi_{2,t}+\frac{455}{1104}.
\]

Their difference vanishes. The central pressure's time derivative fixes
p0_ttt=191/3072, and rho0_t=Pr0_t=3/2. The source acceleration is the
section34 scalar-equation value, not an added adjustable acceleration.
These results concern the diagonal equations through s^2 and the leading
mixed constraint's time derivative at one event. The scalar equation
through s^2, higher orders, finite-neighbourhood existence and stability
are not established by this finite jet.

The shorter global test does not depend on truncating that jet. Direct
geometry gives

\[
R_2=2(z+U_n+U_e)-4k^2.
\]

Combining the independently varied angular and radial equations gives

\[
\alpha q^3(P_r-P_t)
=-qk^2+2\ell^2[(z-U_n)(z+U_e)+U_{ne}^2].
\]

After substituting the orbit equations, the exact source condition is

\[
\boxed{\quad
k^2+\alpha q^2(P_r-P_t)
=2\ell^2q\left[
\left(\frac{3z}{2}+\alpha qP_r\right)
\left(\frac{3z}{2}-\alpha q\rho\right)
+\alpha^2q^2J^2\right].\quad}
\]

Here q=1-ell^2*z, k=p_s, and Pr-Pt=|e phi|^2>=0 for the retained
canonical source. The identity follows from the unchanged action;
no Einstein-effective stress tensor is added as another source.
The code checks the generic unexpanded geometric identity, the angular
subtraction, source substitution and the solved finite jet separately.
The Einstein-limit control is k^2+alpha*|e phi|^2=0.

Now impose the contract's isolated spatial end, with alpha>0, fixed
finite ell, and constant nonzero mass parameter m:

\[
p=1-\frac{m}{s}+O(s^{-2}),\quad
p_s=\frac{m}{s^2}+O(s^{-3}),\quad p_t=O(s^{-2}),\qquad
\rho,P_r,J=O(s^{-3-\epsilon}),\quad\epsilon>0.
\]

The derivative falloffs are explicit assumptions, not inferred by
differentiating an uncontrolled remainder. Finite total energy alone
does not imply the pointwise source falloffs used here. They yield
z=2m/s^3+O(s^-4), q->1, and therefore

\[
\mathrm{LHS}\ge\frac{m^2}{s^4}(1+o(1)),\qquad
\mathrm{RHS}=\frac{18\ell^2m^2}{s^6}+o(s^{-6}).
\]

Multiplication by s^4 makes the contradiction explicit: the left side
has positive limiting lower bound m^2, while the right side tends to
zero. The exact common-p metric therefore has no such isolated
nonzero-mass end with this canonical source and action. A representative
series checks the leading and subleading z coefficients and the mass
limit r^3*z/(2*alpha*q)->m/alpha; the proof uses the stated remainder
bounds and positivity, not that representative alone.

**Verified: 414/414 checks, including 36 new and all 378 previous checks.**
Independent read-only derivations reproduce both the coefficient system
and the full spatial identity; a separate review checked its code and
claim boundaries. These are symbolic verification of the identities
and coefficients plus the explicit asymptotic proof above, not 414
independent physical predictions. The contract and exploratory
derivations preceded runtime verification; this is not a blind test.

**Decision.** Stop the globally exact common-p/canonical isolated-end
route here. More central coefficients or longer integration cannot
repair its asymptotic incompatibility. This does not reject local
common scaling, the spherical saturation action, self-regulation, or
full RefG, and it does not demonstrate a curvature blow-up. It also
does not establish a nonsingular black hole. The next distinct question
is the action-determined relation between clock and spatial metric
coefficients when their global exact reciprocal identification is not
imposed. Any connection of that relation to the foundation state must
be derived or explicitly proposed, not silently declared equivalent.
No new readout law, extra source, intuitive-file change or numerical
evolution was introduced in this stage.

## 36. Full-coframe readout and decisive source-completion tests

### Connected verification contract (2026-09-14)

CLAIM_ID: W92_FULL_READOUT_AND_SOURCE_DECISION_36.
GOAL: resolve the section35 restriction against the existing formal theory,
derive the selected action's actual clock/rod relation, then decide two
short source-completion routes without stopping at a coordinate dictionary.
TYPE: exact readout reconstruction, conditional stationary-source theorem,
and a distinct conditional barotropic saturation theorem.
MODEL_VERSION: unchanged rational spherical action, retained neutral
canonical sextic V(chi)=chi^2/2-chi^4/4+chi^6/24. The last test considers
an explicitly separate minimal conserved-current energy rho(n), not an
unannounced replacement of that scalar or the W87 nonminimal action.
ASSUMPTIONS/DOMAIN: readout on outward static f>0 branch, sigma>0,
q=1-ell^2*z>0, finite ell and positive geometric mass m; asymptotically
flat vacuum. Source theorem: one real harmonic frequency, static
spherical metric, C1 horizon-regular scalar satisfying KG, simple regular
horizons with q_h>0; zero-frequency field has the usual decaying vacuum
tail. Barotropic test: n>0, rho C2, rho'>0 and c_s^2=n*rho''/rho'>=0
throughout the density interval being claimed.
CONVENTIONS: ds^2=-sigma^2*f*dt^2+dr^2/f+r^2*dOmega^2;
p_T=sigma*sqrt(f), p_L=s/r, alpha=4piG, mu=r^3*z/(2q).
The isotropic-coordinate factors are not defined as foundation pressure.
FREEDOM_LEDGER: exterior m,ell and asymptotic clock/coordinate normalization;
no free readout function fitted. Frequency is arbitrary real within its
declared cases. No horizon cutoff, surface layer or central source added.
DEPENDENCIES: W51 weak-field domain, W52 full-1PN component readouts,
W54 complete coframe, W67/W71 scale separation; this report sections1,
6,24,29,33,35. Einstein benchmarks remain limits, not substituted dynamics.
METHOD: exact coordinate pullback plus original static mass/lapse equations;
coefficient reconstruction through inverse-radius order4; original orbit
E_vv and KG in ingoing EF coordinates; nonnegative integral and local
horizon uniqueness; convexity implication for the separate current model.
PASS_CONDITION: zero exact algebraic residuals; explicit analytical proofs
with all boundary/regularity premises; recovery of established weak order.
FAIL_CONDITION/FALSIFIER: wrong reconstruction or flux coefficient, a
nonzero stationary solution satisfying every declared condition, or a
bounded increasing convex rho on an unbounded density interval.
RESIDUAL/ERROR_BOUND: exact identities and explicit O(s^-5) series;
analytical comparison proofs are recorded separately from symbolic checks.
VALIDITY_HEALTH: source theorem tests existence, not perturbative stability;
current convexity is only a necessary local acoustic condition.
BRANCHES: nonextremal stationary source; omega=0 and omega!=0 separately.
Extremal, rotating, charged/synchronized, nonminimal and genuinely dynamic
matter are outside that exclusion. The geometry's q=0 centre-domain issue
is inherited unchanged and is not repaired by coordinates.
OBSERVABLE_MAP: d tau=p_T dt, d ell=ds/p_L, c_coord=c0*p_T*p_L
on the static chart; local c0 unchanged. ADM mass, local source energy and
single-oscillon redshifted mass are different entries.
FORWARD_MODEL/DATA_ROLE: N/A, no observational data or fitting in this test.
IDENTIFIABILITY: readout determined by chosen action/geometry; no unique
microscopic pressure interpretation follows from it.
BENCHMARK/CROSSCHECK: independent exterior and horizon derivations,
Schwarzschild ell=0, asymptotic and horizon limits, sqrt2 scalar extremum,
linear-energy healthy control and an explicitly rejected rational density.
CLOSURE_FLAGS initially false: full_readout_verified,
stationary_source_excluded_in_domain, minimal_density_cap_excluded;
foundation_pressure_join, global_singularity_removal, full_RefG_rejected.
PROVENANCE: source audit and exploratory independent derivations precede
this runtime verification; it is not a blind test. Preserve old414 checks.
FILES: same completion checker, this report and main diagnostic index.
STOP: complete all three connected decisions. Do not rerun another long
collapse window, repeat a failed static shooting problem or silently
choose a new constitutive law. The final result must identify which
remaining physical equation, rather than another coordinate change,
would be needed for a complete RefG nonsingularity claim.

### Result: the full metric is recovered and two source routes are decided

**452/452 checks pass: 38 new plus all414 previous checks.** The source
and exterior derivations were independently reproduced and the resulting
code reviewed separately. The analytical arguments below supply the
existence exclusions; the symbolic tests check their algebraic premises.

#### A. The extra common-p restriction is removed using existing theory

The source audit identifies an earlier unnecessary restriction. W3-51's
`Weak_Field_Closure/w3_51_weak_field_closure_contract.md:60` restricts the
common-factor sourced calculation to g00 through u^2 and gij through u.
W3-52's `Full_1PN_Inheritance/w3_52_full_1pn_inheritance_contract.md:99`
already distinguishes exact clock and ruler coefficients. Both are under
`RefG/work 3/Lagrangian_Formulation/`. W3-54 supplies the complete coframe,
and `Strong_Field/W3-67_Foundation_Strong_Field_Response/` explicitly
limits the weak common factor at lines50-65 of its preregistration.
Section35 remains a valid exclusion of its additional global ansatz;
that ansatz is not a necessary requirement of the established full
RefG coframe. The source-file hashes are included in the checker output.

For the retained action, the vacuum mass and lapse constraints give

\[
f=1-\frac{2mr^2}{r^3+2m\ell^2},\qquad \sigma=1.
\]

On the outward static branch, define s/r->1 at infinity and
d ln(s)/dr=1/(r sqrt(f)). Then p_L=s/r and the exact relation is

\[
\boxed{p_T=\sigma\left(1-\frac{s p_L'}{p_L}\right)},\qquad
\frac{\sigma'}{\sigma}=\frac{\alpha r q^2(\rho+P_r)}{f}.
\]

The prime in the first expression differentiates s; the second
differentiates r. This is an action-determined one-metric relation.
It introduces no freely fitted function. In particular,

\[
p_L=1-\frac m s+\frac{3m^2}{4s^2}+O(s^{-3}),\qquad
p_T=1-\frac m s+\frac{m^2}{2s^2}+O(s^{-3}).
\]

The checker independently reconstructs both series through s^-4.
Their leading common response and the established PPN orders are
retained. The readouts are d tau=p_T dt, d ell=ds/p_L and
c_coord=c0*p_T*p_L. Restoring their action-determined difference repairs
the extra restriction, not the underlying physical action.

Mass normalization is explicit: mu=r^3*z/(2q)=m, the earlier normalized
M_code=mu/alpha, and M_physical=m/G=4pi*M_code when alpha=4piG.
Thus section35's m/alpha limit and the present m are different units
of the same asymptotic charge.

At a simple outer horizon p_T->0 while p_L->s_h/r_h>0; dr/ds->0.
The static isotropic chart ends there. The same geometry continues in
ingoing EF coordinates. The extremal isotropic limit is different and
is outside that simple-horizon statement. At the vacuum centre q->0
while the infinity-normalized static clock sqrt(f)->1. Hence a
foundation-pressure/oscillator law is still distinct from this coordinate
reconstruction; section29's central variational-domain condition remains.

#### B. The retained coherent stationary scalar cannot fill a regular simple-horizon black hole

Use ds^2=-sigma^2*f*dv^2+2sigma*dv*dr+r^2*dOmega^2 and
phi=exp(-i omega v) F(r), with F C1 at a simple regular horizon and C2
on adjacent punctured intervals. Direct evaluation of the original
rational-action tensor, with finite coefficients at q_h>0, gives

\[
E_{vv}=\frac{\sigma^2f}{2}(\alpha_{\rm orbit}+\beta f'),\qquad
T_{vv}|_h=\omega^2|F_h|^2.
\]

For omega!=0 the field equation therefore requires F_h=0. The unchanged
scalar equation is, with a=sigma*r^2*f and g=(1-|F|^2/2)^2,

\[
(aF')'-2i\omega r^2F'-(2i\omega r+\sigma r^2g)F=0.
\]

Set b=2i omega r+sigma*r^2*g and
mu=exp[-integral(2i omega r^2/a)dr]. This integrating factor has unit
modulus and (mu*a*F')'=mu*b*F. A simple horizon gives
|a|>=c|r-r_h|; regular F makes b bounded, |b|<=B, and aF'->0.
Integration from the horizon on either side gives
|F'|<=(B/c) sup|F|. Since F_h=0, an interval epsilon<c/B obeys
sup|F|<=(B epsilon/c) sup|F|, forcing F=0 there. Ordinary uniqueness
propagates this result through connected regular intervals, with the
same argument at further simple horizons. Analyticity is not assumed.

For omega=0 the actual potential has
V'(chi)=chi(1-chi^2/2)^2. Multiplication of KG by the complex conjugate
field and exterior integration yields

\[
[\operatorname{Re}(F^*aF')]_{r_h}^{\infty}
=\int_{r_h}^{\infty}\sigma r^2
\left[f|F'|^2+|F|^2(1-|F|^2/2)^2\right]dr.
\]

The regular-horizon and decaying vacuum boundaries vanish. Positivity
on f>0 forces a constant field. The alternative constant |F|=sqrt2
has V=1/3 and fails the asymptotically flat vacuum boundary; F=0 is
selected. The same horizon-uniqueness argument prevents an otherwise
smooth, interior-only stationary field.

This completes the specified stationary-source exclusion. A horizonless
coherent star from section6 cannot be continued into a regular
nonextremal black hole while keeping that same global harmonic/static
ansatz. Genuinely dynamical matter remains a separate possibility;
extremal, rotating, gauge-synchronized and nonminimal sources are outside
this theorem. No Einstein field equation was used in the proof.

#### C. Simply capping local energy fails the minimal healthy-current test

A separate possible shortcut is a minimally coupled isentropic current
whose local energy rho(n) saturates when its conserved number density
n grows. On the standard positive-energy acoustic branch,

\[
\rho'>0,\qquad c_s^2=\frac{n\rho''}{\rho'}\ge0
\quad\Longrightarrow\quad\rho''\ge0.
\]

Consequently, for n>=n0>0,

\[
\rho(n)\ge\rho(n_0)+\rho'(n_0)(n-n_0)\longrightarrow\infty.
\]

An increasing bounded local energy is incompatible with these assumptions
on an unbounded density interval. The explicitly tested illustration
rho=rho_star*n/(n+n_star) instead gives
c_s^2=-2n/(n+n_star)<0, whereas the linear dust control gives zero.
The saturating illustration is rejected and is not adopted. This test
concerns local energy density; a binding-corrected ADM mass or a
redshifted constituent mass is not rho(n) and is not constrained by
this convexity argument.

**Combined decision.** Use the already established complete coframe,
not a globally locked weak-field scalar metric. For a matter-filled
black hole, the retained coherent canonical source must be dynamically
evolved; the static shooting shortcut is excluded. A stable minimal
local-density cap cannot replace that evolution. The remaining physical
task is a source-and-geometry evolution or a separately specified healthy
medium response which controls the interior source and admits global
continuation. None of these three tests supplies that missing dynamical
estimate. The old finite-time numerical evidence is retained with its
original domain. No intuition, potential, action, production evolution,
Git rule or published claim was changed.

## 37. A finite-mass dynamical inner-horizon counterexample

### Contract before implementation and verification (2026-09-14)

CLAIM_ID: W92_VAIDYA_PARALLEL_CURVATURE_37.
GOAL: decide whether the same spherical rational response alone removes
singularities for an ordinary conserved positive null source, using an
actual time-dependent solution rather than a local jet or a longer replay.
TYPE: exact sourced solution and analytical finite-affine curvature proof.
MODEL_VERSION: same gravitational action, explicitly separate ingoing null
fluid replacing the harmonic scalar for this diagnostic. Its covariant
action is S_null=-1/2 integral sqrt(-g) xi*(grad V)^2, with xi>=0;
variation imposes null gradient and conserved flux. It is not the fixed
canonical-sextic initial packet or a derivation of RefG photon microphysics.
ASSUMPTIONS/DOMAIN: ell>0, ingoing EF metric -f(v,r)dv^2+2dvdr+r^2dOmega^2,
f=1-2m(v)r^2/(r^3+2m(v)ell^2), q>0, smooth increasing m(v).
Concrete certificate ell=1, m(v)=2-1/[4(1+v)], v>=24,
r in [7/6,5/4], outgoing geodesic r(24)=6/5, k^v(24)=1.
CONVENTIONS: alpha=4piG; m is geometric generalized mass; signature -+++;
T_vv=m'(v)/(alpha*r^2), all other orbit components and angular pressure0.
FREEDOM_LEDGER: one explicit tail and affine normalization; no fitted
profile, coordinate cutoff, altered response, second stream or bounce.
DEPENDENCIES: original orbit/angular equations, generalized-mass balance,
section28 vacuum horizon extension. Previous static bounds are controls,
not a proof for the new time-dependent source.
METHOD: direct EF Christoffel, orbit, angular and source-conservation
checks; exact null-geodesic equation; rational inward-vector-field,
q and connection bounds on an invariant rectangle; explicit divergence
lower bound and finite-affine upper bound. No numerical trajectory is
needed for the certificate.
PASS_CONDITION: exact field/source residuals and all rectangle inequalities;
the geodesic persists for every finite v, has finite future affine length,
and R_ab*k^a*k^b diverges. This is a failure of universal regularity in
the declared gravity-plus-null-source class, not a desired positive claim.
FAIL_CONDITION/FALSIFIER: nonzero field/angular/conservation residual,
failure of any invariant-region bound, nonaffine k, or a regular C2
extension along that ray with bounded parallel curvature.
RESIDUAL/ERROR_BOUND: exact symbolic algebra and rational bounds;
analytical ODE existence/extension and comparison argument, no floating fit.
VALIDITY_HEALTH: positive conserved null source, same local metric cone;
q stays above1/4 and the calculation avoids the q=0 action boundary.
BRANCHES: a nonextremal inner-horizon neighbourhood; not a smooth-centre
formation simulation or a scalar-polynomial curvature blow-up assertion.
OBSERVABLE_MAP: affine-parallel null contraction of Ricci, invariant under
coordinate changes; fixed finite affine rescalings do not remove divergence.
FORWARD_MODEL/DATA_ROLE: N/A, no observed-data fit or astronomical prediction.
IDENTIFIABILITY: explicit counterexample to a universal mechanism in this
source class; not classification of every source or rejection of full RefG.
BENCHMARK/CROSSCHECK: constant-m vacuum gives zero null contraction;
Einstein ell=0; direct angular equation; independent exact derivation and
independent rational interval certificate.
CLOSURE_FLAGS initially false: null_source_solution, finite_affine_pp_blowup,
universal_null_source_regularization_excluded; fixed_scalar_packet_blowup,
scalar_polynomial_blowup, full_RefG_rejected, global_singularity_removal.
PROVENANCE: explicit solution and candidate rational bounds were derived
exploratorily before these tests; no blind or observational prediction.
FILES: same completion checker, report and diagnostic index only.
STOP: complete this dynamical yes/no test and report its exact model scope;
do not rebrand it as fixed-packet scalar failure or all-theory rejection.

TIMELIKE ADDENDUM before its implementation: check the same solution and
invariant annulus for a radial geodesic U^v(24)=8, r(24)=6/5,
U^r=(f U^v-1/U^v)/2. Test the unit-timelike norm, both geodesic equations,
the inward boundary signs with the added -1/(2(U^v)^2) term, proper-time
remainder<=1/3 and the divergent parallel angular tidal component.
This strengthens the physical readout of the same counterexample;
the original null test has already passed495/495, so it is not blind.

### Exact dynamical result and independent certificate

**506/506 checks pass: 54 new plus all452 earlier checks.** An independent
derivation reproduces the original field and source equations, rational
interval bounds and both geodesic certificates. A separate adversarial
review verifies the null argument and its scope. The final checker hash
is `4cc848a6664fcc971e092747342a16f58e2b99e7fde2f570579ce06d3b86a750`.

#### The source and metric solve the actual equations

For the metric registered above, direct calculation gives

\[
R_{;vv}=(f_v-ff_r)/2,\quad R_{;vr}=f_r/2,\quad R_{;rr}=0,
\qquad \Box r=f_r,\quad R_{;ab}R^{;ab}=f_r^2/2,\quad R_2=-f_{rr}.
\]

The original rational orbit equations give E_vv=2m'(v), E_vr=E_rr=0;
the independently varied angular equation gives zero angular pressure.
Thus T_vv=m'/(alpha*r^2), with all other listed stresses zero, is an
exact source. The null-fluid action gives (grad V)^2=0 and
div(xi grad V)=0. With V=v, xi=m'/(alpha*r^2)>0, conservation reduces
to partial_r(r^2 xi)=0. The future ingoing vector -partial_r is affine.
There is one positive source ledger and no added effective medium tensor.

The mass aspect is mu=r^3*z/(2q)=m(v). It is an ingoing/generalized
mass aspect, not a claim that the ADM mass of a closed complete system
varies. The incoming energy after v=24 is finite: Delta m=1/100.

#### The exact trajectory certificate

On the rectangle r in [7/6,5/4], m in [199/100,2], f decreases with m.
The boundary signs are

\[
f(7/6,2)=\frac{31}{1207}>0,\qquad
f(5/4,199/100)=-\frac{457}{9493}<0.
\]

The outgoing null equation dr/dv=f/2 therefore preserves this annulus.
Its vector field is smooth and bounded there, so the ray exists for
every finite v>=24. Separately bounding positive factors gives

\[
-\frac{f_r}{2}
=\frac{mr(4m-r^3)}{(r^3+2m)^2}
\ge\frac{107104984}{272176875}>\frac38,\qquad
q\ge\frac{2744}{10287}>\frac14.
\]

For affine normalization k^v(24)=1, the exact geodesic equation is
d ln(k^v)/dv=-f_r/2. Hence

\[
k^v\ge e^{3(v-24)/8},\qquad
\lambda_\infty-\lambda_{24}\le\int_{24}^{\infty}e^{-3(v-24)/8}dv=\frac83.
\]

The Ricci contraction follows independently from geometry and source:

\[
R_{kk}=-\frac{f_v}{r}(k^v)^2
=\frac{2q^2m'}{r^2}(k^v)^2
\ge\frac{e^{3(v-24)/4}}{50(1+v)^2}\longrightarrow+\infty.
\]

The unit angular vectors r^-1 partial_theta and
(r sin(theta))^-1 partial_phi are parallel transported along the
radial ray. Their tidal contraction is R(k,e_theta,k,e_theta)=R_kk/2.
This is parallel-frame curvature divergence at a finite affine endpoint.

#### A freely falling massive observer reaches the same obstruction

Set U^v=K, U^r=(fK-1/K)/2, with K(24)=8 and r(24)=6/5. The checker
verifies g(U,U)=-1 and both geodesic equations:

\[
\frac{dr}{dv}=\frac f2-\frac1{2K^2},\qquad
\frac{d\ln K}{dv}=-\frac{f_r}{2}.
\]

The lower inward margin is 31/1207-1/64=777/77248>0; the upper
boundary remains inward. Thus r remains in the same annulus and
K>=8 exp[3(v-24)/8]. Its own remaining proper time obeys

\[
\tau_\infty-\tau_{24}\le\frac13.
\]

The angular unit vector is also parallel transported along this timelike
geodesic. The observer's tidal component is

\[
\mathcal T=R(U,e_\theta,U,e_\theta)
=-\frac{r''}{r}
=\frac{q^2m'K^2}{r^2}+\frac{f_r}{2r}.
\]

For ell=1, exactly
1+f_r/(2r)=r^3(r^3+5m)/(r^3+2m)^2>0. Therefore

\[
\boxed{\quad\mathcal T\ge
\frac{16}{25}\frac{e^{3(v-24)/4}}{(1+v)^2}-1
\longrightarrow+\infty.\quad}
\]

All times and curvatures here are in the declared ell=1 model units.
The finite initial K=8 selects a particular freely falling observer;
it is not an imposed force or a time-dependent change of frame.

The limiting radius is the inner root of the m=2 metric. To see this,
f(r,m(v))/2 converges uniformly on the annulus to f(r,2)/2, whose
radial derivative is at most -3/8. Relative to its unique zero, the
radius satisfies a contracting equation with a forcing tending to zero.
For the timelike ray the extra forcing -1/(2K^2) tends exponentially
to zero as well. Variation of constants gives convergence to that root.

#### What this settles

The explicitly checked Ricci and Kretschmann scalars are

\[
R_4=-f_{rr}-4f_r/r+2(1-f)/r^2,\qquad
\mathcal K=f_{rr}^2+4f_r^2/r^2+4(1-f)^2/r^4.
\]

They stay bounded on the compact (r,m) rectangle. The freely falling
tidal component nevertheless diverges, obstructing a regular C2
continuation along that geodesic. A finite scalar curvature plot is
therefore insufficient for this model's regularity claim. The physical
reason is explicit: the ingoing flux decays only as (1+v)^-2, while
its freely falling frequency factor grows exponentially. The screening
q^2 stays bounded away from zero and cannot compensate that growth.

The same comparison structure applies near any simple inner horizon
of a finite nonextremal member: ell<r_-<sqrt(3)ell gives q_h>0 and
-f_r(r_-)/2>0. A sufficiently small annulus and sufficiently late
positive power-law tail supply the same positive lower bounds, with
mass-dependent constants. The explicit rational certificate above is
one fully reproduced member, not an astronomical fit.

**Decision:** the selected rational screening action fails to guarantee
nonsingularity for every allowed positive conserved null-source solution.
This is an actual dynamical counterexample; infinite total mass, a
q=0 domain crossing and a numerical failure are absent from its proof.
The same-action vacuum inner-horizon extension in section28 is therefore
not a regularity guarantee once this ingoing source is included.

The exact scope is the specified null-fluid sector in the regular
inner-horizon neighbourhood q>1/4. The proof does not construct collapse
from globally smooth-centre data: extending this particular null source
to r=0 would require separate treatment. It is also not a blow-up proof
for the old canonical-sextic packet or a rejection of full RefG. Weaker
C0/C1 extensions are not classified. These boundaries are retained in
the machine-readable output.

**Research consequence:** a complete RefG mechanism must also control
the physical inner-horizon blueshift, or avoid that inner horizon through
derived dynamics. A bounded central z, decreased external mass or a
different coordinate readout alone does not meet that requirement.
The present candidate is not certified as a nonsingular black hole;
the negative regularity test above is complete in its declared class.

## 38. Existing-light compatibility and the radiation scope boundary

### Contract before implementation (2026-09-17)

CLAIM_ID: W92_EXISTING_LIGHT_NULL_SOURCE_AUDIT_38.
GOAL: decide whether section37 bypassed the already established RefG light,
clock or source-response rules. Stop at this compatibility decision; no new
collapse run, matter law, attenuation factor or singularity-removal claim.
TYPE: conditional exact transport/source identities and an approximation-scope audit.
MODEL_VERSION: unchanged rational gravity and section37 null source; W43's
selected minimal-Maxwell geometric-optics branch, W82's dynamic observer/ray
map and W91's clock/projection controls. These existing optical formulas are
reused; their old Einstein benchmark is not transferred as a gravity result.
ASSUMPTIONS: one operational metric, transparent propagation, positive incoming
wave action, an ideal proper clock, and no extra nonmetric interaction.
DOMAIN: smooth r>0, q>0 EF patch. Electromagnetic interpretation is leading
geometric optics, with its inherited wavelength/EFT restrictions. Exact null
fluid equations remain a separately declared mathematical source model.
CONVENTIONS: signature -+++, c0=hbar=1, alpha=4piG; incoming phase
theta=-integral omega_in(v)dv, omega_in>0, distinct from observer frequency.
FREEDOM_LEDGER: section37 incoming mass profile retained unchanged; positive
carrier frequency is boundary data, not an extra pressure law. No fitting.
DEPENDENCIES: W43 contract, W82 contract and pure exact-interface verifier,
W91 contract, sections36-37, and the relevant intuitive scale descriptions.
METHOD: recompute W82's pure symbolic interface and its negative controls;
derive EF phase, wave-action current, local photon speed, observer frequency
and stress; reconstruct the leading Maxwell stress with transverse polarization;
check source feedback and static/common-scale limits without double counting.
Compare an exactly rotation-invariant Maxwell field to the averaged ray source.
PASS_CONDITION: identical null transport, phase/pulse and stress/source ledgers;
negative controls reject an extra radial attenuation without compensating
exchange. A genuine mismatch is reported rather than patched into the result.
FAIL_CONDITION/FALSIFIER: a nonzero required residual, failed inherited optical
identity, contradictory source ledger or a claimed Maxwell/RefG endpoint proof
without the required wave/EFT completion invalidates that respective claim.
RESIDUAL/ERROR_BOUND: exact symbolic zeros; no fitted or numerical evolution.
No bound on subleading Maxwell errors uniform to the infinite-v endpoint is
assumed. Its absence limits transfer of the exact null-model theorem.
VALIDITY_HEALTH: positive incoming current and one local light cone. The
geometric-optics approximation and the microscopic cutoff are separate limits;
neither is presumed to cure, nor to realize, the null-model singular endpoint.
BRANCHES: exact null fluid; leading optical/kinetic photon interpretation;
exact rotation-invariant Maxwell field as a non-equivalence control.
OBSERVABLE_MAP: omega=-u.k, local speed, proper pulse spacing, T_ab u^a u^b.
FORWARD_MODEL/DATA_ROLE: N/A, no observations or emission-source fit.
IDENTIFIABILITY: distinguishes a missing optical factor from an unproved full
wave/foundation completion; no microscopic emitter is inferred from a tail.
BENCHMARK: W82 dynamic Hamiltonian/geodesic/clock identities, W91 static limit,
local orthonormal Maxwell stress and independent null-current conservation.
CROSSCHECK: existing pure verifier vs direct EF derivation; independent review.
CLOSURE_FLAGS initially false: existing_light_transport_compatible,
leading_optical_stress_matches, no_extra_scale_factor_needed,
source_backreaction_included, optical_scope_boundary_verified.
Keep exact_coherent_Maxwell_solution, uniform_endpoint_optical_validity,
incoming_tail_derived_from_oscillons, full_foundation_photon_action_derived,
full_RefG_rejected and global_singularity_removal false.
PROVENANCE: identities explored analytically before implementation; this is
a consistency audit, not a blind prediction. Input hashes and exact residuals
will be emitted by the completion checker. Source attribution: W43/W82/W91
and S. R. Dolan, https://arxiv.org/abs/1806.08617, sections3.2-3.2.2, for the
established leading Maxwell geometric-optics expansion.
FILES: this report, verify_saturation_completion_boundary.py and the existing
diagnostic index only. Production evolution, intuition and Git rules unchanged.

### Completed compatibility result

**571/571 checks pass: all506 previous checks and65 new audit checks.**
The new suite also recomputes W82's76 existing symbolic identities (reported
as six group checks, not76 new discoveries) and its four negative controls.
The final checker SHA-256 is
016b0f84ba97f41fa5f207ef079b523074f8603c2d1f5356c6b72e5a37025329.
The result is compatibility with the selected existing light sector, with
no omitted universal p attenuation identified.

The relevant pre-existing resources, relative to work3, are:

- Cosmology_and_LSS/Photon_Atomic_Observable_Bridge/
  w3_43_photon_atomic_observable_bridge_preregistration.md, assumptions3-5:
  minimal Maxwell action, null geodesics and conserved wave-action current.
  Its Maxwell-from-foundation flag remains open.
- Strong_Field/W3-82_Dynamical_Clock_Radar_Readout/
  w3_82_dynamical_clock_radar_contract.md, sections1 and3, and the associated
  executable exact_interface(): dynamic ray transport, omega=-u.k, proper
  pulse reciprocity and regular moving-observer limits. Its previous
  test-signal scope does not prohibit a later sourced photon model.
- Strong_Field/W3-91_Direct_Scaling_Endpoint/
  w3_91_direct_scaling_endpoint_contract.md, section2: clock projection and
  signal arrival use the same metric, with no second photon p factor.
- Workspace intuitive/RefG_GE.md, sections2.1-2.2: local c0, coordinate p^2
  on the common-scale branch, and the complete coframe extension. A
  coordinate speed reduction is not a separate absorption coefficient.

#### The source follows the existing optical laws

In the same EF geometry of section37, write

\[
\theta=-\int\omega_{\rm in}(v)\,dv,\qquad
k_a=(-\omega_{\rm in},0),\quad k^a=(0,-\omega_{\rm in}),\qquad
I=\frac{m'(v)}{\alpha r^2\omega_{\rm in}^2}.
\]

Here omega_in(v)>0 is an incoming carrier-frequency label; alpha=4piG.
The phase-averaged/RMS normalization I absorbs electromagnetic units and
the real-wave averaging factor. The phase gradient is null and affine, and

\[
N^a=I k^a,\quad \nabla_aN^a=0,\qquad
T_{ab}=I k_a k_b,\quad T_{vv}=\frac{m'}{\alpha r^2}.
\]

This is the leading Maxwell wave-action/stress dictionary, also admitting
a radial collisionless photon-stream interpretation at this effective level.
The transverse-polarization Hilbert tensor is recomputed explicitly in
Python, rather than inferred merely from a common null cone. The usual
photon-number interpretation fixes the wave-action normalization; it is
not a microscopic derivation of quantization.

For a radial observer and its outward unit ruler,

\[
U^a=\left(K,\frac{fK-K^{-1}}2\right),\qquad
e^a=\left(K,\frac{fK+K^{-1}}2\right),
\quad U^2=-1,\ e^2=1,\ U\cdot e=0.
\]

Then k^a=omega_in K(U^a-e^a), so the observer measures

\[
c_{\rm local}=1,\qquad \omega=\omega_{\rm in}K,\qquad
T_{\rm inst}=\frac{2\pi}{\omega_{\rm in}K},\qquad
\rho_\gamma=T_{ab}U^aU^b=\frac{m'K^2}{\alpha r^2}.
\]

T_inst is an instantaneous proper period; the adjacent-front reciprocity
is a differential timing statement. It is not an exact finite interval
between two crests when the frequency varies appreciably during that interval.
The source's wave fronts are v=constant; K=dv/dtau is the receiving clock
and motion factor. Section37's stronger local signal is a frequency and
intensity increase under this same measurement law, not superluminal
propagation. The static control recovers c_coord=p_T p_L, c_local=1 and
omega=epsilon/p_T; the common-scale limit gives exactly c_coord=p^2.

Backreaction is present. Substituting this recovered T_vv into the
unchanged original equation gives E_vv=2alpha r^2 T_vv=2m'(v).
The tidal response obeys -f_v/(2r)=alpha q^2 T_vv. Thus q^2 was already
active in the coupled solution; the geometry responds to the incoming flux.

Multiplying the current or intensity by a new S(v,r) gives

\[
\nabla_a(SN^a)=-\frac{m'}{\alpha r^2\omega_{\rm in}}\,\partial_rS.
\]

A radial attenuation needs a derived compensating exchange and a changed
source/metric solution. A factor S(v) alone changes incoming luminosity
and hence m'(v). Neither operation is an automatic missing pressure
correction to the existing transparent branch. The checker rejects radial
attenuation without exchange, an omitted receiving-clock factor, a doubled
static p factor and changed source with unchanged mass balance.

#### Exact source model and full light/foundation completion

Section37 is an exact theorem for its gravity-plus-null-fluid equations.
The match above establishes its leading optical source interpretation.
The full finite-wavelength Maxwell solution has not been constructed.
A source-free electromagnetic field which itself is exactly rotation-invariant
has Coulomb components: F_vr=Q/r^2 and F_theta_phi=Qm sin(theta), with
constant charges. Maxwell and Bianchi constraints, the mixed stress
T_vr=-(Q^2+Qm^2)/(2r^4), and zero radial flux T^r_v are checked directly.
A spherical distribution of incoherent photons is a different description
and is not excluded by that coherent-field control.

The power-law tail is prescribed incoming boundary data persisting to
arbitrarily late v with finite integrated energy. Its production by
specific oscillons has not been derived. Such boundary data are legitimate
for the stated source-model test; physical formation and genericity are
separate claims. When late influx is zero, this particular flux-driven
tidal term is zero; that control does not establish global regularity.

Neither an assumed breakdown nor an assumed unlimited validity of the
optical approximation settles the endpoint. For constant omega_in,

\[
\frac{q^2m'K^2/r^2}{\omega^2}
 =\frac{q^2m'}{r^2\omega_{\rm in}^2}\longrightarrow0.
\]

The convergence is uniform on section37's compact annulus: q<=1,
r>=7/6 and m'->0. The checker verifies the exact cancellation and the
fixed-radius limit. Thus growing frequency alone is not evidence that
geometric optics fails. A uniform error bound for a complete coupled
wave/foundation solution, including its effective-theory domain, is absent.

**Decision:** no conflict with the already computed light propagation,
clock or leading energy-current rules was found. Section37's exact
null-model counterexample is retained. Its transfer to an exact
finite-wavelength light source and to the complete RefG foundation remains
unproved. The suggestion in conversation that an omitted pressure factor
probably caused the result is not supported by this audit.
Production collapse code and all intuitive text remain unchanged.

## 39. Inner-extremal geometry and the fixed-law bridge

### Bounded contract, 2026-09-18

CLAIM_ID: W92-INNER-EXTREMAL-FIXED-LAW.
CLAIM: decide whether the mass-robust inner-extremal construction can enter
the existing regular one-function vacuum response without retuning its law.
TYPE: exact construction and restricted analytical obstruction; a separate
conditional null-transport bound is geometric, not a derived source solution.
MODEL_VERSION: retain sections37-38 and all production equations unchanged.
The comparison target specializes equation(12) of Carballo-Rubio et al.,
https://arxiv.org/abs/2205.13556 (JHEP09(2022)118).
ASSUMPTIONS/DOMAIN: a>0, M>a/2, r>=0, with a fixed; target N=(r-a)^3(r-2M),
D=N+2M*r^3+a^2*r^2, f=N/D. The old-law comparison is r^3 H(z)=12M,
z=(1-f)/r^2, fixed H, finite positive r,M and finite nonzero H'.
CONVENTIONS: G=c=1; ds^2=-f dv^2+2dvdr+r^2 dOmega^2; kappa=f_r/2.
a is a new geometric target scale, not an identification with P_F or the
old action scale ell. Their physical relation has not been prescribed.
FREEDOM_LEDGER: M is the state mass; a is fixed; outer root 2M and b2=a^2
are construction choices. No fitted data or modified photon law.
DEPENDENCIES: sections1,37,38; published geometry only, not inherited stability.
METHOD: exact derivatives, a positive denominator certificate, inverse-law
comparison and analytical geodesic bounds on a compact annulus.
PASS_CONDITION: verify target regularity and mass-persistent triple root;
decide the fixed-law bridge with a nonzero residual or an exact obstruction.
FAIL_CONDITION: an incorrect identity, a hidden denominator zero, retuned
couplings counted as states, or a geometric family labelled derived dynamics.
FALSIFIER: any counterexample to the stated fixed-H derivative identities
within their domain, or a pole in the registered target metric.
RESIDUAL/ERROR_BOUND: exact symbolic zero residuals; the annular asymptotic
estimate uses explicit compact-domain sign and boundedness assumptions.
VALIDITY_HEALTH: C2 central metric and finite algebraic curvature, not smooth
higher-curvature derivatives; causal cones come from the Lorentzian metric.
No healthy matter action, global extension or observation claim is registered.
BRANCHES: existing Hayward control; prescribed inner-extremal target; regular
fixed-H vacuum response. Extra dynamical matter states remain outside the
fixed-H vacuum obstruction.
OBSERVABLE_MAP: horizon multiplicity, mass susceptibility, parallel null Ricci
contraction. FORWARD_MODEL/DATA_ROLE: N/A, no observational comparison.
IDENTIFIABILITY: distinguish a geometric mass family from solutions of one
regular constitutive/action law. BENCHMARK: exact old Hayward degeneracy.
CROSSCHECK: independent derivative and candidate audits, full old regression.
CLOSURE_FLAGS initially false: target_geometry_verified,
conditional_null_Ricci_bound_verified, fixed_H_bridge_excluded.
Keep fixed_theory_dynamics_derived, self_regulating_attractor,
full_RefG_pressure_join and global_singularity_removal false.
PROVENANCE: candidate and derivative relations explored analytically before
coding; no blind prediction. Checks write only stdout.
FILES: this report, verify_saturation_completion_boundary.py and the existing
diagnostic index. Production solver, intuition, manuscripts and Git rules stay
unchanged. STOP: one verified bridge decision and its exact missing physical
input; no parameter scan or long collapse simulation.

### 39.1 Result and concrete target

The prescribed inner-extremal family passes the geometry audit. For the same
finite-energy incoming mass history used in section37, its outgoing radial
null Ricci contraction is bounded and decays. A regular fixed one-function
vacuum response of the existing form cannot generate a continuously
mass-varying family of degenerate horizons. These are separate results:
the candidate supplies a target response, and the obstruction identifies
the dynamical structure that must change to realize it.

The target specializes the geometry of Carballo-Rubio, Di Filippo, Liberati,
Pacilio and Visser [4], equation(12), with r_-=a, r_+=2M and b2=a^2:

    P=(r-a)^3, N=P(r-2M),
    D=N+2Mr^3+a^2r^2, f=N/D, a>0, M>a/2.

Here a stays fixed when the state mass M changes. This is a construction
choice, not a derivation of a from RefG's physical foundation pressure.
Setting b=2M, the denominator has the exact certificate

    D=r^2(r-3a/2)^2+c2*r^2+a^3*b*[1-r(3/a+1/b)/2]^2,
    c2=(a^2+3ab-a^3/b)/4 > 0.

For b>a, c2 is positive. Thus D>0 for r!=0; D(0)=a^3b>0 as well.
At the centre and infinity,

    f=1-r^2/(ab)-[1/a^3+3/(a^2b)+1/(ab^2)]r^3+O(r^4),
    R(0)=12/(ab), K(0)=24/(a^2b^2),
    f=1-2M/r+O(r^-2).

K denotes the Kretschmann scalar. The centre has a C2 local metric and
finite algebraic curvature; the nonzero cubic term does not certify
arbitrary higher-order smoothness. At fixed r>0, a->0 recovers Schwarzschild.
No observational fitting or full RefG weak-field match is performed here.

The inner horizon r=a is a triple root for every M>a/2, the outer horizon
r=b is simple, and f<0 throughout a<r<b. More precisely,

    f=-alpha*(r-a)^3+O((r-a)^4),
    alpha=(b-a)/[a^3(a+b)]>0,
    kappa_-=0, kappa_+=(b-a)^3/[2b^2(b^2+a^2)]>0.

This realizes the geometric feature selected from the published construction.
The mass susceptibility is also essential:

    f_M=-2r^2(r-a)^3(r^2+a^2)/D^2.

It vanishes cubically at the inner horizon. Its sign changes across r=a;
the formula specifies a required geometric response, not a matter-health test.

### 39.2 The same incoming tail: bounded null Ricci response

Use a=1 and exactly the section37 mass history,

    M(v)=2-1/[4(1+v)], v>=24, r(24)=6/5,
    dr/dv=f/2, delta=r-1, K_aff=dv/dlambda>0.

K_aff denotes the affine boost, not the Kretschmann scalar. The closed
rectangle 1<=r<=6/5, 199/100<=M<=2 has D>0 and
2M-r>=139/50. Consequently c=(2M-r)/D is smooth and has
strictly positive finite lower and upper bounds there. The exact equation

    delta'=-c*delta^3/2, (delta^-2)'=c

keeps delta positive at every finite v and proves delta=Theta(v^-1/2).
The ray remains in the rectangle, approaches r=1, and c->3/5, so

    delta~sqrt[5/(3v)].

The unchanged affine null-geodesic equation is
d log(K_aff)/dv=-f_r/2. With Y=(-f)K_aff>0,

    d log(Y)/dv=(f_M/f)M'
               =2r^2(r^2+1)M'/[D(2M-r)].

The coefficient multiplying M' is bounded on that same rectangle.
Since the remaining integral of M' is 1/100, Y tends to a strictly positive
finite constant Y_inf. Therefore

    K_aff~Y_inf*sqrt(3/5)*v^(3/2).

For the unit-cross-term ingoing metric, warped-sphere curvature gives

    R_ab k^a k^b=-f_v*K_aff^2/r
               =2r(r-1)^3(r^2+1)M'*K_aff^2/D^2
               ~[Y_inf^2*sqrt(3/5)/15]*v^(-1/2).

This geometric null convergence is finite along the entire specified ray
and tends to zero. The proof is an analytical comparison using the compact
rectangle, with exact identities checked by Python; it uses no finite-time
extrapolation. The remaining affine interval is finite because
integral(dv/K_aff) converges. An extension through that endpoint and a bound
on every parallel-frame curvature component require their own proof.

The source interpretation fixes the scope of this positive result.
For independently conserved incoming photon stress on the same metric,
with normalization T_vv=M'/(4*pi*r^2), the measured contraction is

    T_ab k^a k^b=M'*K_aff^2/(4*pi*r^2)
               ~[3Y_inf^2/(80*pi)]*v.

Thus ordinary photon transport still blueshifts the stress. Choosing this
normalization specializes section37's alpha_source to 4*pi; it changes no
power or decision. The prescribed metric responds weakly enough to keep
the displayed Ricci contraction bounded. A coupled gravitational/source
law must produce that response; imposing f alone does not establish it.
No photon absorption, frequency cutoff, exchange term or extra scale factor
has been inserted.

### 39.3 Exact obstruction for the existing one-function vacuum law

The existing spherical vacuum response can be written

    r^3 H(z)=12M, z=(1-f)/r^2,

where H=6h in the normalization of the original spherical action. All
couplings in H are fixed. On a finite-radius, finite-mass regular branch
with finite nonzero H', implicit differentiation gives

    f_M=-12/(r H'), f_r=r*(3H/H'-2z).

At any degenerate horizon, f=0 and f_r=0 imply

    z=1/r_h^2, H=12M/r_h^3, H'=18M/r_h,
    f_M=-2/(3M).

A differentiable family r_h(M) of such horizons would instead require

    0=d f(r_h(M),M)/dM=f_M+f_r*r_h'(M)=-2/(3M),

which is impossible for finite positive M. This excludes a mass-robust
degenerate-horizon family in the stated regular fixed-H vacuum class.
It includes a moving horizon radius; fixing r_h was not assumed.

The second-derivative test at a double root is

    f_rr=2z(2zH''-H')/H'.

A triple root at one selected mass can therefore be tuned by
2zH''=H', but that does not remove the mass-family obstruction.
For the old Hayward choice the sole degenerate mass is
M=3*sqrt(3)*ell/4, with coincident inner and outer horizons at
r=sqrt(3)*ell. It supplies a useful control, not separated mass-robust horizons.

Vanishing inverse susceptibility alone is also insufficient within the
same response class: writing z=Z(s), s=12M/r^3, gives

    f_M=-12Z'/r, f_r=r[-2Z+3sZ'].

If Z'=0 at a finite-load horizon, then f_r=-2/r_h, a simple root.
This closes the specific proposal to obtain extremality just by placing
a flat segment in the old inverse response.

### 39.4 Where a new dynamical completion must differ

For the target of 39.1, the explicit inverse mass relation away from
degenerate points is

    Q=r^3-(r-a)^3,
    Mcal(r,z)={z*r[(r-a)^3+a^2r]-a^2}/{2(r-zQ)}.

Substitution of z=(1-f)/r^2 returns M exactly. At
(r,z)=(a,1/a^2), both numerator and denominator vanish for every M.
Approaching that same point along two target geometries of masses M1 and
M2 gives two different inverse limits. Moreover,

    Mcal_z|target=D^2/[2(r-a)^3(r^2+a^2)].

Hence this mass family cannot simply be relabelled a regular single-valued
constitutive inverse through its inner horizon. It is a useful target
family whose field equations remain to be supplied.

The needed new input is a fixed physical action or field equation whose
solutions escape the regular one-function vacuum relation. An actual
evolving medium/source state is one option; a different gravitational
vacuum structure is another. For an additional state S, the horizon-family
condition would read f_M+f_S*dS/dM=0. The state equation must determine dS/dM.
Choosing that derivative solely to cancel f_M would again impose the answer.
Replacing a universal coupling by an object-dependent fitted function of
M similarly changes the theory rather than solving one fixed theory.

The obstruction is restricted to the stated static regular fixed-H class.
It leaves sourced non-vacuum solutions, additional physical states,
different field equations and genuinely time-dependent horizon avoidance
outside its scope. Neither the obstruction nor the candidate settles the
full RefG singularity question.

### 39.5 Verification, decision and stop

The completion verifier passes 631/631 checks: all 571 earlier checks and
60 new exact checks/controls. The new checks cover the positive denominator,
central jet, horizons, mass derivatives, inverse obstruction and identities
in the compact-domain ray proof. Independently repeated derivative and
ray analyses agree; code review confirms that bounded Ricci response is
kept separate from unbounded transported photon stress.

Decision: GEOMETRIC_TARGET_VERIFIED_REGULAR_FIXED_H_BRIDGE_EXCLUDED.

    target_geometry_verified = True
    conditional_null_Ricci_bound_verified = True
    fixed_H_bridge_excluded = True
    inverse_law_obstruction_verified = True
    fixed_theory_dynamics_derived = False
    self_regulating_attractor = False
    full_RefG_pressure_join = False
    photon_stress_bounded = False
    global_singularity_removal = False
    full_RefG_rejected = False

The first four flags are computed from their required check groups; the
conditional ray flag also uses the analytical proof in 39.2. A successful
regression includes verification of the restricted obstruction, so its
check count is not a singularity-removal certificate.

The concrete next physical task is to select and derive a fixed response
law for the coupled source and foundation that can generate the required
suppression as the source changes. This bounded stage stops at that
identified missing input, without changing the production action or
conducting another collapse run under a prescribed answer.

## 40. Coupled-source entry: a shrinking inner radius and the required stress

### Bounded contract, 2026-09-18

CLAIM_ID: W92-INNER-EXTREMAL-SOURCE-ENTRY.
CLAIM: determine what the stage39 geometry requires of the existing
independent medium/source sector, and test the smallest moving-radius
control before proposing any new response function.
TYPE: exact source identities, restricted source-class exclusion, and
conditional geometric ray result. This is not an action derivation.
MODEL_VERSION: the stage39 target family; the existing W92 five-field
medium and its independent source equations are retained as reference.
CONVENTIONS: (-+++), G=c=1, G_ab=8*pi*T_total, and the unit-cross ingoing
metric unless the explicitly stated regular lapse is retained.
ASSUMPTIONS/DOMAIN: a>0, M>a/2. The positive control holds L fixed and
sets a=L^2/(2M), with 0<a<=M. This is a registered fixed-central-curvature
geometric restriction; a is a state radius, not a retuned universal coupling.
Its dynamical realization and relation to oscillon size/physical pressure
are not assumed. For the ray comparison L=2, the old M(v) is unchanged,
v>=24, and r(24)=6/5.
FREEDOM_LEDGER: L is a fixed candidate core-curvature scale; M is a state;
a(M) is a diagnostic relation selected before numerical or symbolic
execution, not a measured or action-derived relation. No matter or light
law is changed. The off-silent F_med remains unspecified, as in the source.
DEPENDENCIES: sections37-39; FORMAL_COVARIANT_MEDIUM_INTEGRATION.md;
common_scale_centre_source.md section8; the existing source-response audit.
METHOD: independent EF connection, exact Einstein-source ledger and
mass derivatives; polynomial positivity; compact-domain geodesic proof.
PASS_CONDITION: identify the necessary medium null stress at the moving
triple surface and decide the proposed positive-source shortcut; test
whether the shrinking control removes the fixed-radius radial sign fault.
FAIL_CONDITION: incorrect residual, a radius/coupling identification
without a state equation, or prescribed total stress called a derived medium.
FALSIFIER: nonzero residual in the stated source/geometry identities,
or a negative radial-loading response in the positive control's domain.
RESIDUAL/ERROR_BOUND: exact symbolic residuals; the late-ray result uses
the explicit analytic comparison proof, not finite-time extrapolation.
VALIDITY_HEALTH: NEC is a filter for sums of individually NEC-respecting
Einstein sources, not a universal synonym for stability. Existing
noncanonical medium and modified-gravity alternatives remain distinct.
OBSERVABLE_MAP: source-null projections, transverse pressure, centre
curvature and affine null Ricci contraction. DATA_ROLE/FORWARD_MODEL: N/A,
no observational fit. BENCHMARK: the fixed-a family of section39.
IDENTIFIABILITY: separate the state-radius control from its missing
constitutive dynamics. CROSSCHECK: independent source and ray derivations,
existing-equation audit, negative controls and full regression.
CLOSURE_FLAGS initially false: source_entry_verified,
shrinking_radial_control_verified, conditional_shrinking_ray_bound_verified,
ordinary_positive_source_shortcut_excluded.
Keep medium_dynamics_derived, self_regulating_attractor,
full_RefG_pressure_join and global_singularity_removal false.
PROVENANCE: analytic relations explored before coding; not a blind prediction.
FILES: this report, verify_saturation_completion_boundary.py, diagnostic
index. Production solver, intuition, manuscripts and Git rules unchanged.
STOP: one source-entry decision and one bounded positive control; no new
phenomenological F, absorption law, parameter scan or collapse simulation.

### 40.1 The existing medium is an actual entry, with independent equations

The five-field medium in FORMAL_COVARIANT_MEDIUM_INTEGRATION.md uses
Einstein gravity plus independent clock, label/strain and deficit fields.
This is a different source-entry test from section39's one-function
modified-vacuum relation; the two gravitational operators are not added
together. The exact independent static balances already derived in
common_scale_centre_source.md section8 are

    P0*K_N' = N A S^2 [Q0(J+Fbar)+W-V],
    P0*Q_H' = Q0 N A S^2 J,
    P0[(N S^2/A)(ln N+H)']' = N A S^2[Q0 Fbar+W-V].

Here P0 is the constant Planck coefficient, Q0 the fixed medium
normalization, N the lapse, A the radial scale, S the areal radius,
K_N=S^2 N'/A, Q_H=-N S^2 H'/A, and W=Omega^2 chi^2/N^2.
V is the retained canonical scalar potential. Fbar depends on the
independent clock and strain invariants y,b_r,b_t, and
J=y Fbar_y-b_r Fbar_r-b_t Fbar_t.

Those states escape the vacuum-only hypothesis of section39, but their
off-silent constitutive response has not been selected by the existing
action. Assigning Fbar to cancel W-V along a desired profile would impose
the answer. The registered derivative-medium prototype has a separate
homogeneous compensating response and an enhanced quasistatic spatial
response; its already-failed direct pressure map supplies no such law.
The positive-energy static common-scale join also already failed its
exterior test (common_scale_centre_source.md section6D).

The present calculation determines the required dynamical source at the
triple surface directly. Static equations valid for positive N,A are
not extrapolated through the trapped region.

### 40.2 Exact source requirement, including a regular lapse

Take the horizon-regular two-function metric

    ds^2=-exp(2psi) f dv^2+2 exp(psi) dv dr+r^2 dOmega^2,
    l=partial_v+exp(psi) f partial_r/2,
    n=-exp(-psi) partial_r, l.n=-1.

Direct connection calculation and spherical warped-product curvature give

    R_ll=-exp(psi) f_v/r+exp(2psi) f^2 psi_r/(2r),
    R_nn=2 exp(-2psi) psi_r/r.

If f has a smooth moving triple root r=a(v), differentiation of
f(v,a(v))=f_r(v,a(v))=f_rr(v,a(v))=0 gives f_v=f_rv=0
on that surface. For finite exp(psi)>0 and bounded psi_r,
R_ll=G_ll=0 there. A smooth lapse cannot supply the missing null source.

In the unit-cross target, set m=r(1-f)/2 and use Einstein-source variables

    rho=m_r/(4*pi*r^2), p_r=-rho, p_t=-m_rr/(8*pi*r).

At the triple surface,

    m=a/2, m_r=1/2, m_rr=0,
    rho=1/(8*pi*a^2), p_r=-rho, p_t=0.

Thus the stationary surface requires anisotropic tension. It is locally
compatible with nonnegative total null projections in the stationary
limit. The extra requirement comes from a transparent incoming stream.

Use the same ordinary photon normalization as section39,
T_gamma,vv=Lum(v)/(4*pi*r^2), Lum=M'>0. This stream is separately
conserved in the unit-cross metric: its radial conservation equation is
partial_r(r^2 T_gamma,vv)=0. With the total derivative along a(M), define

    chi_M=partial_M m=-r*(f_M+f_a*a_M)/2.

The exact Einstein-source split then requires

    T_total,ll=chi_M*T_gamma,ll,
    T_medium,ll=(chi_M-1)*T_gamma,ll,
    T_medium,ll|horizon=-T_gamma,ll|horizon.

The target therefore requires a compensating medium null stress, even
though the photons themselves follow their unchanged conserved transport.
This quantity combines energy and stress in a null direction; it is not
an assertion that every observer measures negative medium energy.
Defining T_medium=G/(8*pi)-T_gamma makes a formally conserved tensor by
the Bianchi identity, but it supplies no field equation for that medium.

A sum of individually null-energy-condition-respecting Einstein sources
cannot satisfy this requirement with a nonzero transparent incoming
stream. This excludes the positive-source shortcut, not general healthy
modified gravity or every noncanonical medium. The original projected-H
sector already has a negative radial null sum on its exterior,
rho_H+p_rH=-2P0 Z_H, Z_H>0. It has the required possible sign; matching its
magnitude and checking its coupled health on this target remain necessary.

### 40.3 A shrinking state radius fixes the radial-loading sign

For the same rational geometry of section39 with a now a state variable,

    f_M(total)=-r^2(r-a)^2 B/D^2,
    B=2(r-a)(r^2+a^2)+a_M(r-2M)[(6M+2a)r+a^2].

At fixed a the response changes sign across the inner surface. Near a
moving triple root it instead has the leading form

    f_M(total)=3 alpha*a_M*(r-a)^2+O((r-a)^3).

Thus a_M<0 gives a nonnegative radial Einstein-source response to M'>0
on both sides locally. Merely increasing a gives the opposite sign.

As a single positive control, keep the central curvature fixed:

    R(0)=6/(Ma)=12/L^2,
    a=L^2/(2M), a_M=-a/M, K(0)=24/L^4.

L is held fixed. This relation follows from the registered geometric
central-curvature condition; it has not been derived from a medium state
equation. It does not identify the inner areal radius with an oscillon's
operational size or assert a universal bound on curvature away from the
centre.

For 0<a<=M the response has the global radial sign certificate

    f_M(total)=-r^3(r-a)^2 Q2(r)/D^2,
    Q2=2r^2-(8a+2a^2/M)r+12Ma+6a^2-a^3/M,
    discriminant(Q2)=4a(2M+a)(a^2+8Ma-12M^2)/M^2<0.

The positive leading coefficient and negative discriminant imply Q2>0,
so chi_M>=0 for every r>0. Both triple degeneracy and the central
curvature values persist as M varies within this prescribed family.
Mass-dependent inner radii and quadratic susceptibility also appear in
the general construction [4], equations(23)-(27); this particular
fixed-central-curvature control and its sign certificate are calculated here.

The full source still has a separate transverse requirement. Its central
expansion gives

    z=(1-f)/r^2=1/(2Ma)+z1*r+O(r^2),
    z1=(4M^2+6Ma+a^2)/(4M^2*a^3)>0,
    rho+p_t=-z1*r/(4*pi)+O(r^2)<0.

Consequently this same unit-cross target still fails the all-NEC Einstein
source shortcut near its centre. The successful radial sign repair
therefore selects a viable direction of motion, not a healthy complete
matter model. A general lapse/source system or a modified gravitational
response has to be tested on its own equations.

### 40.4 The known late incoming history remains geometrically bounded

Set L=2, retain M(v)=2-1/[4(1+v)], v>=24 and r(24)=6/5. Then

    a(v)=1+1/(8v+7), -a_dot=8/(8v+7)^2,
    delta=r-a(v), c=(2M-r)/D,
    delta'=-c*delta^3/2-a_dot.

The ray stays in a(v)<r<=6/5. On its moving lower boundary delta'=-a_dot>0;
at the upper boundary f<0. All coefficients are smooth and c is bounded
above and below by positive constants on the enclosing compact set.
The decreasing r tends to 1, since any larger limiting radius would
leave f strictly negative. Thus delta->0 and c->3/5.

The comparison delta'>=-c_max*delta^3/2 gives

    delta>=[delta_24^-2+c_max*(v-24)]^-1/2.

Writing w=delta^-2 yields
w'=c-2(-a_dot)w^(3/2)->3/5: the second term is O(v^-1/2).
Hence delta~sqrt[5/(3v)], as in the fixed-radius control.
For K_aff=dv/dlambda and Y=(-f)K_aff,

    d ln(Y)/dv=f_v/f=c_v/c-3a_dot/delta.

Here c_v is the partial derivative at fixed r, including the dependence
on M(v) and a(v). Its contribution is O(v^-2), while a_dot/delta is
O(v^-3/2). Both are integrable, giving a finite positive Y_inf and
K_aff~Y_inf*sqrt(3/5)*v^(3/2).

The geometric null contraction is

    R_kk=(Y^2/r)[c_v/(c^2 delta^3)-3a_dot/(c delta^4)]
         ->9Y_inf^2/40.

It remains finite and approaches a positive constant. Ordinary
T_gamma,kk still grows as v; the necessary medium contribution cancels
its leading effect in the prescribed geometry. This result concerns
the specified ray and incoming history, not arbitrary irradiation.
The remaining affine interval is finite. At finite v the surface
r=a(v) has normal norm -2a_dot>0 and is a timelike degenerate marginal
tube; its name or existence alone does not establish a global Cauchy
horizon, endpoint extension or geodesic completeness.

### 40.5 Decision and exact next physical input

The completion verifier passes 680/680 checks: all 631 earlier checks and
49 new checks, including an independent connection calculation, source
requirements, sign controls and the exact identities supporting the
analytical ray proof. Independent derivative, source and ray reviews
agree. The closure flags below retain the distinction between verified
conditional geometry and a derived dynamical medium.

    source_entry_verified = True
    shrinking_radial_control_verified = True
    conditional_shrinking_ray_bound_verified = True
    ordinary_positive_source_shortcut_excluded = True
    medium_dynamics_derived = False
    self_regulating_attractor = False
    full_RefG_pressure_join = False
    global_singularity_removal = False
    full_RefG_rejected = False

The new result is a concrete response requirement: the coupled medium
must determine a shrinking state radius and the compensating null stress
while satisfying its independent clock, label, deficit and metric equations.
The old source audit supplies these independent fields, but leaves their
off-silent constitutive response undetermined. The retained positive-energy
static shortcut and the separately tested derivative prototype cannot
be reused as if they had already supplied it.

This fixes where the next physical law has to enter. Another prescribed
metric or another run of the unchanged collapse solver cannot derive that
law. The present stage adds no fitted absorption term, imposed stress
profile to the evolution, or change to the photon's propagation equation.

## 41. Relative flow and minimal mixing: source decision (2026-09-18)

### 41.1 Registered bounded contract

Decision to test: can the existing independent Einstein--medium action
supply the negative radial null stress required in section40, once the
radial material labels are allowed to move relative to the regular clock?
Also test the smallest already-listed amendment, a constant coefficient
lambda multiplying W^2, W=u.d(phi). This operator is absent from the
defined action; testing it is explicitly an amendment, not a reinterpretation.

The registered domain is a local orthonormal clock frame, positive radial
strain, a regular nondegenerate short-wavelength material branch, and a
strictly positive reduced principal Hamiltonian. For the amendment also
require that radial characteristics stay within the existing local light
cone. Arbitrary first and second derivatives of F are retained; no equation
of state, numerical fitting or coefficient scan is selected for a result.
The old projected-H constraint reduction is a dependency to reproduce,
not a new degree of freedom. Finite-wavelength metric-constraint reduction,
degenerate branches and general higher-derivative actions are out of scope.

Write scope: this report, the existing completion verifier, and the current
diagnostic summary only. Preserve the production solver, optical law,
intuition, articles and Git settings. Success means a reproducible source
compatibility decision in the stated class, not a global singularity result.
If a sign obstruction holds for the whole registered class, close this
route without presenting further coefficient tuning as a physical mechanism.

### 41.2 Existing action, allowing radial motion relative to the clock

Section40 fixes an actual source requirement. For a smooth moving triple
surface and regular lapse, R_ll=0; a positive ordinary photon stream
therefore needs T_medium,ll=-T_gamma,ll<0 in the Einstein-source completion.
This is an energy-plus-stress contraction, not a statement that the
medium must have negative energy density in every frame.

The whole-action (-+++) convention of the existing source audit gives

    L=Q F(y,B)+kappa h^ab H_a H_b,   Q,kappa>0.

Use a regular local clock-rest frame and normalize the positive background
clock norm to y=1. Positive frozen label/deficit normalizations are absorbed
into F and its derivatives. With the other two label eigenvalues fixed,

    Phi=t+theta,   phi=Vt+Sx+xi,   S^2>V^2,
    H=q t+g_H x+h,   d=kappa g_H^2>=0.

The derivatives F_y,F_b,F_yy,F_yb,F_bb are arbitrary local derivatives of
this normalized F, not coefficients chosen by a scan. In an unnormalized
clock notation the clock slope is y F_y. The radial subsystem gives
necessary conditions for the full spherical medium; it is not a sufficient
test of all its modes.

The previously established normalized-projector calculation is reproduced:
eta=h-q theta gives, at principal order,

    L_H,2=kappa[eta_x^2-2g_H eta_t theta_x+g_H^2 theta_x^2].

Integration by parts replaces eta_t theta_x by eta_x theta_t. For nonzero
radial wave number the auxiliary constraint sets eta_x=g_H theta_t,
leaving -d(theta_t^2-theta_x^2). Thus a nonzero background q is not a
missing independent response. This repeats a dependency of stage26;
the new test here is the noncomoving label, V!=0.

For z=(theta,xi), the complete radial matter principal form is

    L_2=z_t^T K z_t+2 z_t^T N z_x-z_x^T G z_x,
    A=Q(F_y+2F_yy)-d, B=QF_y-d,
    C=Q(-F_b+2V^2 F_bb), D=Q(-F_b-2S^2 F_bb),
    K=[[A,-2QV F_yb],[-2QV F_yb,C]],
    N=[[0,2QS F_yb],[0,-2QVS F_bb]], G=diag(B,D).

The canonical Hamiltonian is

    H_2=(p-2Nz_x)^T K^-1(p-2Nz_x)/4+z_x^T G z_x.

On the registered regular positive-energy branch K>0 and G>0, hence
B,C,D>0. This requirement is stronger than merely real characteristic
speeds and is stated explicitly. The exact identity

    -QF_b=(S^2 C+V^2 D)/(S^2+V^2)>0

then fixes the sign. Independent inverse-metric variation, including the
clock dependence of h^ab, gives on k_+=(1,1) and k_-=(1,-1)

    T_medium,++/2=B-QF_b(V+S)^2>0,
    T_medium,--/2=B-QF_b(V-S)^2>0.

No subluminality premise was used in this original-action sign result.
Neither arbitrary F_yb nor radial label motion can supply section40's
negative radial null stress within this branch. A coefficient retuning
of F cannot change this conclusion while preserving the registered energy
gate. The positive and negative test controls in the code are local
principal data only, not solutions of the background field equations.

### 41.3 Smallest listed amendment: constant lambda W^2

The mixed clock--label invariant W=u.d(phi) is permitted by the field
symmetries but its coefficient is zero in the defined action; see root
RefG_ka.md, equations(15) and the adjoining operator list. Its introduction
here is an explicitly tested amendment. With lambda any real constant,

    Delta L_2=lambda[(xi_t-S theta_x)^2+V^2 theta_x^2
                     -2V theta_x xi_x+2VS theta_t theta_x],
    Delta T_++/2=lambda(V^2+2VS),
    Delta T_--/2=lambda(V^2-2VS).

Let beta=S^2+V^2, replace B by B_lambda=B-lambda beta and C by
C_lambda=C+lambda. The new off-diagonal G entry is lambda V;
N_theta,theta=lambda VS and N_xi,theta=-lambda S. K's other entries
and D are unchanged. Positive energy necessarily gives
B_lambda,C_lambda,D>0.

For lambda>=0 the exact certificates are

    T_++/2=B_lambda+(V+S)^2(S^2 C_lambda+V^2 D)/beta
                      +2lambda V^2(beta+VS)/beta>0,
    T_--/2=B_lambda+(V-S)^2(S^2 C_lambda+V^2 D)/beta
                      +2lambda V^2(beta-VS)/beta>0.

Both beta+VS and beta-VS are positive. No cone condition is needed in
this sign case.

For lambda=-ell<0, with ell>0, choose S>V>=0 without loss of generality:
positive radial strain gives |S|>|V| and changes of label basis/radial
orientation only interchange the two null directions. The principal
characteristic pencil is P(c)=K c^2-(N+N^T)c-G. If P(-1) has a negative
eigenvalue, while K>0, continuity from sufficiently negative c (where
P(c)>0) forces det P(c_*)=0 at some c_*<-1. Thus the unchanged local
light cone necessarily requires

    p_-=P(-1)_xi,xi=-ell+2Q(S-V)^2 F_bb>=0.

This endpoint test is necessary, not sufficient, for all modes to be
healthy and subluminal. It is enough for the exclusion:

    T_--/2=B_lambda+D(S-V)^2+S^2 p_-+2ell V(S-V)>0,
    -QF_b-ell=D+S^2 p_-/(S-V)^2
                 +ell V(2S-V)/(S-V)^2>0,
    T_++-T_--=8VS(-QF_b-ell)>=0.

Consequently the constant W^2 amendment also cannot supply the required
negative null stress with both positive radial principal energy and the
existing light-cone bound. This is a certificate for all constant lambda
and arbitrary retained F jets, not a failed search through a few examples.
Related general energy/cone issues are discussed in [5]; the explicit
RefG field, constraint and sign calculations above are performed here.

### 41.4 Decision, verification and boundary

The new function flowing_medium_source_checks in the existing completion
verifier checks the invariant expansion, full projected-H null variation,
auxiliary reduction, canonical energy, the two null-source signs,
constant-W mixing and its cone/sign certificates. Its 45 checks pass;
the complete regression passes 725/725, retaining all 680 earlier checks.
Independent algebraic and conceptual reviews agree with the source
signs and the stated energy/cone domain.
The analytical eigenvalue-continuity lemma and the sign reasoning above
are the proofs; passing Python identities is their reproducible algebraic
check, not a numerical proof of global regularity.

The result closes two concrete source routes: the original regular
relative-flow F branch and its constant-W^2 amendment under the stated
energy/cone conditions. It does not close RefG itself. In particular,
this is not a complete finite-wavelength lapse/shift reduction, a
degenerate-constraint theorem, or an exclusion of field-dependent
mixed invariants, nonminimal curvature couplings or higher derivatives.
The regular high-frequency ordering used by the earlier source-health
audit is retained as a premise; an actual applicable EFT band has not
been derived here.

    original_flow_source_join_excluded_in_domain = True
    constant_W2_source_join_excluded_in_domain = True
    complete_finite_wavelength_metric_reduction = False
    degenerate_branches_excluded = False
    general_mixed_invariant_action_excluded = False
    medium_dynamics_derived = False
    full_RefG_pressure_join = False
    global_singularity_removal = False
    full_RefG_rejected = False

The obstruction is structural, not an omitted overall pressure multiplier
or a newly added radiation species. The candidate geometry remains a
conditional construction; the tested source action does not generate
its compensating response in the admissible branch. Repeating the old
collapse evolution or tuning more F derivatives cannot complete this
join. If this geometric target is retained, a further construction must explicitly change a premise of this
source-action class, derive its constraints and conserved total source,
and preserve the existing weak-field/light limit. The self-regulation
principle alone does not select that new dynamical operator. This stage
therefore ends with the exact class decision instead of naming an
untested new operator as the solution.

## 42. Source-led metric and moving-inner-surface budget (2026-09-18)

### 42.1 Bounded verification contract

CLAIM_ID: W92-SOURCE-LED-HORIZON-BUDGET.
CLAIM: remove the imposed degenerate surface and determine the independent
Einstein metric constraints and the positive-source budget for a moving
simple inner marginal surface. Decide whether merely keeping its
instantaneous radial slope small can persist under the retained incoming
history without exhausting its radius-squared budget.
TYPE: exact field-equation identities and a conditional integral bound.
MODEL_VERSION: the section41 regular positive-energy matter branch coupled
to Einstein gravity; no new F, interaction, absorption or photon law.
ASSUMPTIONS/DOMAIN: spherical areal ingoing chart, finite positive exp(psi),
r>0, regular stress; f(v,a(v))=0, f_r|a<0 for the inner-surface result.
The budget additionally assumes T_medium,ll>=0 and the specified positive
ingoing photon luminosity. All statements end if these premises fail.
CONVENTIONS: (-+++), G=c=1; v normalized to exterior advanced time.
FREEDOM_LEDGER: retain both independent f(v,r),psi(v,r); neither a(M) nor
an interior profile is prescribed. The diagnostic slope bound kappa_h<=c/(1+v)
has one fixed c>0, not a fitted dynamical law.
DEPENDENCIES: sections40--41 and the existing independent-medium action.
METHOD: radial Einstein equations from an independent connection; null
source conservation, moving-root differentiation and exact integral budget.
PASS_CONDITION: reproduce the unrestricted source equations and prove or
refute the stated low-slope persistence possibility in its full domain.
FAIL/FALSIFIER: nonzero identity residual or a regular positive-radius
counterexample satisfying every stated inequality at arbitrarily late v.
ERROR_BOUND: zero algebraic residual; integral argument analytical.
VALIDITY_HEALTH: retain section41's regular principal-energy domain; do not
infer complete metric/matter stability from these necessary conditions.
BRANCHES: unit-cross target, unrestricted two-function metric and simple
shrinking marginal surface; no selected complete medium solution.
OBSERVABLE_MAP: local curvature/source, areal radius, instantaneous surface
slope. DATA_ROLE/FORWARD_MODEL: N/A, no observational comparison.
IDENTIFIABILITY: a source-determined metric is distinguished from inverse
assignment of a desired profile. BENCHMARK: section40's imposed triple root
and constant-central-curvature radius law.
CROSSCHECK: separate source and horizon-budget derivations; old regression.
CLOSURE_FLAGS initially false: source_led_constraints_verified,
unit_cross_strict_source_excluded, slow_slope_persistence_excluded.
Full medium closure, ray bounds and global singularity removal remain false.
FILES: this report, existing completion verifier and diagnostic index only.
STOP: one source-led constraint/budget decision; no arbitrary constitutive
polynomial, new long collapse run or selection of a geometry as a solution.

### 42.2 Free radial geometry: two independent functions are necessary

Keep the general areal ingoing form

    ds^2=-exp(2psi) f dv^2+2 exp(psi) dv dr+r^2 dOmega^2,
    m=r(1-f)/2.

The radial Einstein equations, derived directly from its connection, are

    psi_r=4pi r T_rr,
    m_r=-4pi r^2 exp(-psi) T_vr,
    m_v=4pi r^2[exp(-psi) T_vv+f T_vr].

These are source-led necessary equations; the angular equation and
independent medium equations remain part of the full system. The null
curvature identities in section40 already contain the first relation.
Its implication for the now-tested strict source branch is the new
ansatz decision: setting psi=0 imposes T_rr=0 everywhere. For ingoing
photons T_gamma,rr=0, whereas section41 gives T_medium,nn>0 and therefore
T_medium,rr=exp(2psi) T_medium,nn>0 wherever that branch is present.
The unit-cross ansatz cannot represent it, with or without a horizon.

Consequently both f and psi must remain free in this Einstein-source
branch. A time relabelling v->V(v) changes psi by an r-independent term;
it cannot remove psi_r. Allowing the second metric function restores a
physical radial constraint, not a second independent foundation substance
or a new particle-scale mechanism.

### 42.3 The source determines the motion of a simple inner surface

For l=partial_v+exp(psi)f partial_r/2 and n=-exp(-psi)partial_r, l.n=-1.
An ingoing photon source

    T_gamma,ab=[Lum(v)/(4pi r^2)](dv)_a(dv)_b

is conserved for general psi: n is affinely geodesic and the current
divergence reduces to partial_r(r^2 T_gamma,vv)=0. No new attenuation
coefficient or nonstandard photon law is introduced.

Let f(v,a(v))=0 be a SIMPLE inner marginal surface, f_r|a<0. Differentiating
this equation gives f_v|a=-a' f_r|a, hence

    G_ll|a=exp(psi) a' f_r/a.

Define kappa_h=-exp(psi) f_r|a/2>0 in this fixed advanced-time coordinate,
and U=T_medium,ll|a. The local Einstein equation gives the exact motion law

    a'= -[Lum/a+4pi a U]/kappa_h.

Positive incoming photons and U>=0 force the inner surface to move inward.
The same formula before fixing the inner sign gives outward motion for
a simple outer surface with positive T_ll. A persistent degenerate
surface would still set G_ll=0; adding psi alone cannot rescue that
earlier target.

A local smooth geometric source-sign control uses a(v)=1-v,
f=-(r-a)-(r-a)^3 and psi=r-1. At v=0,r=1 it has G_ll=1,G_rr=2.
With Lum=1/4, the required medium remainder is
T_medium,ll=1/(16pi)>0 and T_medium,rr=1/(4pi)>0. The metric determinant
is nonzero and all coefficients are smooth at this point. This verifies
that freeing both restrictions removes the local sign contradiction.
It does not solve the independent clock, label and deficit equations.

### 42.4 Finite source budget excludes arbitrary late flattening

The same motion equation imposes

    -d(a^2)/dv = 2 Lum/kappa_h+8pi a^2 U/kappa_h,
    integral_[v0,v] Lum/kappa_h dv <= [a0^2-a(v)^2]/2.

Thus a finite initial radius supplies a finite radius-squared budget.
Retain the previously specified incoming light history
Lum=1/[4(1+v)^2], and test kappa_h<=c/(1+v) for a fixed c>0 throughout
v>=v0. Then

    a(v)^2 <= a0^2-ln[(1+v)/(1+v0)]/(2c).

The right-hand side reaches zero at
1+v=(1+v0)exp(2c a0^2) and becomes negative afterwards. No positive-radius
simple inner surface can obey all these premises indefinitely. Faster
flattening satisfies the same upper bound and is excluded as well.
This establishes a failure of simultaneous persistence assumptions;
it does not predict that an actual object reaches zero radius. Before
that bound, the source, the slope bound, the horizon branch or the
retained equation/domain must change.

Here v remains the SAME exterior-normalized advanced time used to
prescribe Lum. A time reparametrization transforms both T_vv and kappa_h
and cannot be used while leaving the old luminosity/slope formulas fixed.
In this source-led calculation total asymptotic mass evolution is not
prescribed separately as M'=Lum: it must include the complete source flux.

As a separate benchmark only, if the older a=L_core^2/(2M) and M'=Lum
are both imposed again, U>=0 requires kappa_h>=M/a^2. For the old
L_core=2, M->2, a->1 control, that is kappa_h>=2+o(1). Thus even an
asymptotically degenerate replacement is incompatible with that exact
old radius/mass/flux prescription on the retained nonnegative-source branch.

This surface budget is not a blueshift theorem for an actual ray. Its
affine rate is evaluated at the ray position and has the full expression

    d ln(dv/dlambda)/dv=-psi_v-exp(psi) f_r/2-exp(psi) f psi_r.

Neither its additional lapse terms nor its evaluation away from r=a(v)
can be dropped when kappa_h tends to zero. No ray or global-regularity
conclusion is inferred from the surface inequality alone.

### 42.5 Decision and actual remaining input

The new source_led_horizon_checks function passes 39/39 exact checks;
the complete verifier passes 764/764, retaining all 725 previous checks.
The new checks cover
independent radial connection identities, general-lapse photon
transport, moving-root balance and the finite-budget primitive.
Independent source and budget reviews agree.

The permissible metric description is now narrowed by the field equations:
both radial functions must be determined by the source, and an illuminated
simple inner surface must move according to that source. The unit-cross
restriction and arbitrary late flattening are rejected in their stated
domains. The earlier prescribed geometry remains a historical conditional
control and is not imposed on the new equations.

The underlying matter constitutive closure has not become specified by
releasing these geometric restrictions. The original medium action fixes
its silent exterior but leaves its off-silent F response open
(FORMAL_COVARIANT_MEDIUM_INTEGRATION.md, model/source ledger).
The independent matter--medium balance in common_scale_centre_source.md,
section8, explicitly keeps F undetermined. Its earlier polynomial has
failed its separate completion test; the homogeneous derivative prototype
has a different action and no accepted inhomogeneous pressure join.
Consequently none can be silently substituted as a completed source law
for a new collapse simulation.

    source_led_constraints_verified = True
    unit_cross_strict_source_excluded = True
    slow_slope_persistence_excluded = True
    full_medium_constitutive_law_selected = False
    independent_medium_equations_solved = False
    ray_boost_bound_derived = False
    full_RefG_pressure_join = False
    global_singularity_removal = False
    full_RefG_rejected = False

This step ends with the source-led geometry and persistence decision.
An actual solution requires a specified admissible off-silent response
and its independent field equations, not another assigned radius profile.
The production solver, intuitive text, articles, optical law and Git
configuration are unchanged.

## 43. Explicit deficit--curvature response: radiation activation test (2026-09-18)

Scope correction (section44): this standalone scalar--tensor control
does not replace the already-derived common-pressure matter coupling.
Its trace-only scalar equation cannot be used to claim that RefG light
was uncoupled from the medium or that the old pressure source vanishes.

### 43.1 Frozen operator-selection contract

CLAIM_ID: W92-DEFICIT-CURVATURE-RADIATION-RESPONSE.
CLAIM: test whether the simplest positive deficit-dependent Einstein
coefficient supplies automatic self-regulation under the retained ingoing
null-fluid source. This tests an actual specified action rather than
another undetermined response function or target metric.
MODEL_VERSION: standalone scalar--tensor control
S=integral sqrt(-g)[P exp(2H)R/2-P exp(2H)(partial H)^2/2]+S_m[g], P>0.
This is a new restricted prototype, NOT a reduction of the five-field
medium or a replacement of its clock/label equations. H is the proposed
deficit variable; its RefG pressure/oscillon identification is not assumed
proved by its name. The physical matter/photon metric is g.
TYPE: exact field/source check and restricted mechanism falsifier.
FREEDOM_LEDGER: exp(2H) and the kinetic coefficient are fixed before
execution, with no potential, fitted profile or tuned threshold.
P is universal; constant H0 and the existing mass/flux history are state
and boundary data. No new particle species or absorption law is introduced.
DOMAIN/CONVENTIONS: (-+++), r>0, A=exp(2H)>0, regular invertible conformal
map g_E=A g; classical two-derivative action and the already-used null-fluid
source. The r->0 limit is a model curvature test, not an exact Maxwell
beam or smooth-centre formation calculation.
DEPENDENCIES: source completeness, sections37--42, scalar--tensor
variation/conformal identities [6]. No successful old branch is inherited.
METHOD: vary metric and H, eliminate the trace, test full equations on
an exact ingoing null-source branch and independently compute its curvature.
PASS_CONDITION: verify local kinetic/cone eligibility and decide whether
the source necessarily activates H. FALSIFIER for AUTOMATIC regulation:
an exact positive-flux constant-H branch retaining unbounded curvature.
RESIDUAL/ERROR_BOUND: exact algebraic zero residual; no numerical fit.
HEALTH: positive tensor/scalar kinetic terms on A>0; global stability,
full RefG constraints and a physical EFT cutoff are not supplied.
OBSERVABLE_MAP: curvature and source activation; the static force ratio
is only a fixed-background tree-level control. DATA/FORWARD_MODEL: N/A.
BENCHMARK: constant-coefficient Einstein plus the same null-fluid source.
IDENTIFIABILITY: a larger coefficient versus a source-induced change of
that coefficient. CROSSCHECK: independent action and null-branch reviews.
FILES: this report, existing completion verifier and diagnostic index.
CLOSURE_FLAGS initially false: explicit_action_eligibility_verified,
constant_deficit_null_branch_verified, automatic_regulation_excluded.
Production, intuition, articles, Canon, Git and the original action stay
unchanged. STOP after this operator's source decision; do not tune a
potential after the failed test or declare another mechanism without testing it.

### 43.2 Action variation and the source that activates the deficit

Write A=exp(2H), Z=P A. Varying the metric and H independently gives

    P A G_ab = T_ab + P A (H_a H_b - g_ab (partial H)^2/2)
               + P (nabla_a nabla_b A - g_ab box A),
    R + box H + (partial H)^2 = 0.

T_ab is the minimally coupled material/radiation stress, and
T=g^ab T_ab is its trace. Taking the metric trace and then using the
independent H equation gives the exact reduced equation

    7 P A [box H + 2 (partial H)^2] = T,
    (7P/2) box A = T.

This identifies the activation problem: the scalar responds directly
to the stress trace. An ingoing null fluid has positive energy and
T=0 simultaneously. Constant H is therefore an allowed solution even
while the radiation gravitates. The scalar curvature R can also vanish
while the full curvature is large; coupling H to R alone does not make
H respond to every kind of curvature.

The regular transformation g_E=A g puts the gravity/scalar kinetic
terms into Einstein form [6]. Their scalar coefficient is

    K_E = Z/A + (3P/2)(A_H/A)^2 = 7P > 0,
    chi = sqrt(7P) H,       g = exp[-2 chi/sqrt(7P)] g_E.

Thus the local tensor/scalar principal terms have positive kinetic
coefficients and the same conformal null cone. This is local
two-derivative eligibility, with no statement of global stability.
Around a constant background the massless scalar force gives
G_eff/G_bare=1+P A_H^2/(2 A^2 K_E)=9/7. A chosen larger background A
and a dynamically source-induced increase of A are different claims;
the positive kinetic result supplies neither the latter nor screening.

### 43.3 Exact null-source branch and independent curvature check

Keep H=H0 finite and constant, A0=exp(2H0), and use the physical metric

    ds^2 = -[1-2m(v)/r] dv^2 + 2 dv dr + r^2 dOmega^2,
    T_vv = 2 P A0 m'(v)/r^2.

This fixes the geometric history and derives its physical source.
For an equal-luminosity comparison at different H0, fixing
T_vv=Lum/(4pi r^2) instead gives m'=Lum/(8pi P A0).
H0=0 and P=1/(8pi) recover the earlier G=1 source normalization.

The connection gives R=0, G_vv=2m'/r^2 and every other independent
Einstein component zero. Both metric and scalar equations above are
satisfied exactly. The null-fluid equation is also retained:
V=v obeys (partial V)^2=0, and the density current is conserved because
partial_r(r^2 T_vv)=0. No absorption, faster light or extra energy
component was added.

An independent spherical warped-product contraction gives

    K = R_abcd R^abcd = 48 m(v)^2/r^6.

For the unchanged geometric history m(v)=2-1/[4(1+v)], v>=24,
m'>0, m(24)=199/100 and m(infinity)=2. Its finite extra incoming
geometric mass is 1/100. Nevertheless K diverges as r->0.
The explicit action therefore admits positive incoming energy with
no deficit response and no central curvature cap.

Scope of the falsifier: this branch already has a singular centre
on its initial slice; the fluid density grows as r^-2 there. It rejects
AUTOMATIC UNIVERSAL regulation by this standalone operator. It does
not settle formation from regular-centre oscillon data, the response
of every possible scalar--tensor action, or the full five-field RefG
model. The original pressure/mass/clock identification remains unjoined.

### 43.4 Decision, reproducibility and stop

The explicit operator passes the local kinetic/cone check and fails
the proposed automatic radiation-regulation mechanism. This specified
zero-potential prototype is rejected as an automatic regular completion:
its positive coefficient multiplying R leaves the trace-free radiation
channel unregulated on the exact branch above.

The existing completion verifier contains
deficit_curvature_activation_checks, including the uneliminated scalar
equation, all independent metric components, source conservation and
the curvature invariant. A nonzero-R constant-H control fails the
scalar equation, so that equation cannot be silently dropped. The flat
limit has zero curvature. Two read-only action/source reviews reproduce
the trace equation, null-source normalization and curvature result.
No new numerical evolution, boundary profile or constitutive fit was used.

The new checks pass **36/36**, and the full regression passes **800/800**
(all 764 earlier checks retained). Exact identity residuals are zero.
The first isolated run left the flux-sign query undecided because v
was unrestricted at its pole v=-1; the gate now uses the registered
v=24+t, t>0 domain. Its v=24 endpoint is positive by direct substitution.
The physical action and source were unchanged by that test correction.
Completion verifier SHA256:
1049769b74ea3d919f84616e5248f6b5c6717206594afcf9c6b70db521cea575.
Production verifier SHA256 remains:
1a23833cd7bc907da7bdda32f26c8ced9ec866f298423a646fb4827f7ce40500.
The three local verification flags close; full_medium_constitutive_law_selected,
full_RefG_pressure_join, global_singularity_removal and full_RefG_rejected
remain false.
The physical outcome is an excluded shortcut, not a singularity-removal
PASS. The full-medium task returns to the existing shared metric and
its independent equations; section44 checks their nonzero light-source
projection. This section chooses no replacement coupling. The registered stop is
reached at this operator decision. Production, intuition, articles,
Canon and Git configuration remain unchanged.

## 44. Existing common-pressure light coupling: source-map correction (2026-09-18)

### 44.1 Frozen correction contract

CLAIM_ID: W92-COMMON-PRESSURE-LIGHT-SOURCE-MAP.
CLAIM/TYPE: exact action/source audit of the already-used pressure
metric; decide whether section43's trace-only scalar source can stand
for that metric's pressure variation. No new mechanism is proposed.
MODEL_VERSION/ASSUMPTIONS: minimal Maxwell action on
g=diag(-p^2,p^-2,p^-2,p^-2), p=exp(-H_p), signature (-+++), c=1.
H_p is the common-scale coordinate, distinct from the independent
section43 scalar and from the independent five-field H until a map is
derived. The zero-shift isotropic branch is a source diagnostic.
DOMAIN: finite H_p, p>0, smooth fields; local principal symbol at frozen
coefficients; time-dependent energy check within this declared metric.
FREEDOM_LEDGER: existing metric and Maxwell normalization, no new
coefficient, absorption, density profile, cutoff or fitted potential.
DEPENDENCIES: intuitive sections2.1--2.2; W43 minimal Maxwell branch;
common_scale_centre_source.md source-pullback audit and section8;
verify_common_scale_centre_source.py feedback_assumption_checks.
METHOD/CROSSCHECK: independently vary the full Maxwell contraction
and the metric through its Hilbert stress; check the canonical energy
balance and existing light cone. Carry that source into the existing
static lapse/deficit balance with zero total radial flux, retaining the
independent H equation. A static Maxwell control checks its coefficient;
it is not an ingoing-collapse ansatz. Rerun the old source audit unchanged.
PASS_CONDITION: equal nonzero radiation source in both variations,
unchanged common-scale optics and exact energy-balance identity.
FAIL/FALSIFIER: nonzero symbolic residual, wrong sign/factor, or
identification of the trace-only auxiliary scalar with H_p without
the metric/source map. Full independent equations remain required.
RESIDUAL/ERROR_BOUND: exact zero identities; no numerical fit.
HEALTH: positive Maxwell kinetic/Hamiltonian and the existing local
light cone on p>0; medium stability is outside this source-map audit.
OBSERVABLE_MAP: proper energy, coordinate flux, clock and ruler.
DATA/FORWARD_MODEL: N/A, no observational inference.
IDENTIFIABILITY/BENCHMARK: opposite time/space scale variation versus
uniform conformal variation; rest constituent and null wave controls.
BRANCHES: common-pressure optical branch retained, section43 separate.
FLAGS initially false: existing_pressure_source_verified,
trace_only_identification_excluded, photon_energy_balance_verified.
Full medium closure and singularity-removal flags remain false.
PROVENANCE/FILES: the existing completion verifier, this report and
diagnostic index only. Original source verifiers, production, intuition,
articles, Canon and Git unchanged. STOP after source-map correction,
its regression and the exact remaining dynamical boundary are recorded.

### 44.2 Located mismatch and unchanged prior source

The pre-existing feedback_assumption_checks in
verify_common_scale_centre_source.py already verifies

    (1/2) T^ab partial_Hp g_ab = rho + p_r + 2 p_t.

Its accompanying report, source-pullback audit and section8, distinguishes
this metric-mediated source from fixed-metric variation of an independent
medium H. The unchanged audit was rerun: 13/13 checks pass.
The general identity is reused here, not claimed as a new mechanism.

Section43 instead selected a separate scalar--tensor action with
independent g and H. In its Einstein-frame representation the scalar
changes the physical metric conformally, so its direct matter source
is proportional to the Lorentz trace, -rho+p_r+2p_t. A map from that
scalar to the old common-pressure coordinate was never derived.
Identifying the two source equations would be the model-selection error.

For H_p=-ln p, time and space coefficients vary with opposite signs:
partial_Hp g_00=-2g_00 and partial_Hp g_ij=2g_ij.
For traceless radiation, p_r+2p_t=rho; its common-pressure source is
therefore 2rho, while its Lorentz trace is zero.
Section38's existing photon source and q^2 geometric backreaction remain
present and unchanged. The conclusion that light needs a newly invented
coupling to pressure is withdrawn.

### 44.3 Direct Maxwell variation and reciprocal energy bookkeeping

With E_i=F_0i, B_i=epsilon_ijk F_jk/2 and sqrt(-g)=p^-2,
direct contraction of the full Maxwell action gives

    L_EM = (p^-2 E^2 - p^2 B^2)/2,
    rho_EM = (E^2 + p^4 B^2)/2,
    delta S_EM/delta H_p = p^-2 E^2+p^2 B^2
                         = 2 sqrt(-g) rho_EM.

The independent Hilbert-tensor variation gives exactly the same source.
It is nonzero for a nonzero null beam even though F_ab F^ab=0.
Variation must precede the null-wave substitution; inserting its
on-shell zero Lagrangian first would incorrectly erase the source.

The canonical momentum is pi_i=p^-2 E_i. Up to the Gauss constraint
and a boundary term, the positive coordinate Hamiltonian density is

    epsilon_EM = p^2(pi^2+B^2)/2 = p^-2 rho_EM,
    partial_Hp epsilon_EM |_pi,B = -2 epsilon_EM.

For a transverse potential A_y(t,x), exact Maxwell evolution yields

    partial_t epsilon_EM + partial_x S^x
       = -2 (partial_t H_p) epsilon_EM,
    S^x = -p^2 (partial_t A_y)(partial_x A_y).

The sign follows E_i=F_0i. The executable checks the off-shell residual
against (partial_t A_y) times the Maxwell equation. This is metric work
in the declared common-scale description, not extra absorption or a
violation of covariant Maxwell stress conservation. In a complete
autonomous coupled action the opposite contribution enters the field
sector's energy accounting. No total-medium Hamiltonian was solved here.

The same metric gives c_coord=p^2, d tau=p dt and d ell=p^-1 dx;
the locally measured light speed stays one. Thus propagation, source
and energy bookkeeping use one metric, with no second pressure factor.

### 44.4 Source carried into the existing independent equations

In common_scale_centre_source.md section8 the static spherical metric is
ds^2=-N^2 dt^2+A^2 dr^2+S^2 dOmega^2. Define

    K=S^2 N'/A,    Q_H=-NS^2 H'/A,    D=K-Q_H.

P is the constant Einstein coefficient, Q the medium normalization,
Fbar its response, and W,V the retained oscillon kinetic/potential
terms defined in that source. Adding a minimally coupled Maxwell
stress once extends the existing balance to

    P D' = NAS^2 [Q Fbar + W - V + rho_EM].

The coefficient follows from rho_EM+p_rEM+2p_tEM=2rho_EM and the
factor 1/2 in the lapse source. An independent reduced Maxwell action

    L_EM,rad = S^2 (V_e')^2/(2NA) - NA q_m^2/(2S^2)

checks the full source combination N E_N-A E_A-S E_S=-2NAS^2 rho_EM.
V_e is an electrostatic potential, distinct from the oscillon V;
q_m is a magnetic-charge control, which may be set to zero.
The fixed-metric independent H equation gains no second direct source.

This last balance is restricted to static spherical stress with zero
total radial energy flux. It is not the equation for the one-way
incoming dynamical stream. Requiring N=exp(-H) in this static sector
imposes Q Fbar+W-V+rho_EM=0 as an additional compatibility condition.
All independent metric, clock, label, H and Maxwell equations still
have to be solved together. A projected source equation alone cannot
replace them.

### 44.5 Correction outcome and verification

The existing light--pressure coupling is retained and its exact Maxwell
source is verified. Section43 remains a mathematical test of its own
auxiliary scalar--tensor action; its trace-only response is not RefG's
common-pressure response. This corrects the interpretation and equation
selection, without fabricating a new medium coupling.

The original source audit passes **13/13** unchanged. The completion
verifier passes **834/834**, comprising the new **34/34** source-map
checks and all 800 previous checks; no failed residuals remain.
Completion verifier SHA256:
dc0b4e58fbad77956c34e788266c2ce3f857f78ee72e34b7ea445e2f2ac32c0b.
Unchanged original source-audit verifier SHA256:
0a864e0c681d58ef84beb5f03d12f531aa393023ccff5c3956dc1f805f263c51.
The three source-map verification flags close. Independent medium
evolution, full pressure join and global singularity removal stay false.
Two independent read-only reviews checked the variation, energy balance
and the static source coefficient. No production evolution or article
was changed, and no all-time curvature bound or singularity-removal
claim is made by this source-map correction.

## 45. Full-equation irradiation gate for the exact exterior (2026-09-18)

### 45.1 Frozen dynamical-entry contract

CLAIM_ID: W92-SILENT-EXTERIOR-RADIATION-DYNAMICS.
GOAL/TYPE: decide whether promoting the existing exact exponential
exterior to H(t,r), with its clock and labels retained, permits nonzero
radial null irradiation. This is a restricted full-equation gate, not
another Maxwell-source identity or an all-RefG exclusion.
MODEL: unchanged five-field action P R/2+Q F(y,Bhat)+P gamma^ab H_a H_b
plus minimally coupled radiation, in the established (-+++) convention.
P>0; gamma^ab=g^ab+u^a u^b; clock Phi and labels phi^A are independent
fields before variation. The exact exterior has y=1,Bhat=I and
F=F_y=F_B=0. No Hessian or off-silent coefficients are selected.
TESTED ANSATZ: g=diag(-exp(-2H),exp(2H),exp(2H),exp(2H))
in isotropic Cartesian coordinates, Phi=t, phi^A=x^A, then H=H(t,r).
DOMAIN: smooth classical fields on a spherical annulus r>0; the centre
and isolated asymptotic boundary are optional additional restrictions.
FREEDOMS: arbitrary smooth H(t,r), same universal P, no luminosity fit,
new constitutive term, attenuation, or prescribed absorbing boundary.
METHOD: vary the projected-gradient action with respect to the clock,
H and metric independently; evaluate its constraints; subtract its
Hilbert stress from the independently computed Einstein tensor.
PASS/FAIL: admit a nonzero radial null source satisfying all equations,
or exclude that source by their simultaneous algebraic requirements.
FALSIFIER: a missed independent equation, a nonzero identity residual,
or a positive radial-null counterexample inside the stated ansatz.
CROSSCHECK: independent analytic current/Einstein derivation; retain
the static exterior and a non-isolated homogeneous radiation control.
ERROR/HEALTH: exact residuals; no numerical or observational tolerance;
background equations only, no finite-wavelength stability certificate.
OBSERVABLE: orthonormal energy, radial/tangential pressure and flux.
DATA/FORWARD_MODEL: N/A. BENCHMARK: existing static silent exterior.
DEPENDENCIES: original W92 action; common_scale_centre_source.md
independent-field/source audit; section44's unchanged photon coupling.
FLAGS initially false: independent_clock_constraint_verified,
required_matter_tensor_verified, strict_radial_irradiation_excluded,
homogeneous_radiation_control_verified. No full-medium closure inherited.
FILES: existing completion verifier, this report, diagnostic index.
STOP: complete this dynamical-entry decision; do not simulate a rejected
ansatz or silently replace the off-silent material law afterward.

### 45.2 Independent clock equation locks the exterior charge

Define Y=-g^ab Phi_a Phi_b, u_a=-Phi_a/sqrt(Y),
s^a=(g^ab+u^a u^b)H_b and q_H=u^a H_a. Variation BEFORE any
clock/metric substitution gives, with J=yF_y-Bhat:F_B,

    P nabla_a s^a + Q J = 0,
    nabla_a J_Phi^a = 0,
    J_Phi^a = 2Q exp(-2H) sqrt(Y) F_y u^a
              - 2P q_H s^a/sqrt(Y).

The proposed time-dependent exact-exterior ansatz keeps y=1 and
Bhat=I everywhere. Its silent values F=F_y=F_B=0 therefore remain
fixed. All three Cartesian-label currents and the algebraic F stress
vanish identically at this state, but the clock equation still contains
the projected-gradient term. In isotropic Cartesian coordinates the
two independent equations reduce to

    Delta H = 0,             div(H_t grad H) = 0.

The second equation plus the first gives partial_t |grad H|^2=0.
On a spherical annulus the harmonic solution is

    H(t,r)=h0(t)+C(t)/r,      C C'=0.

Thus C^2 is constant and smooth real solutions have constant C,
including the zero-charge case. No division by a possibly zero C is
needed. The article's exterior parameter therefore cannot simply be
replaced by an accreting C(t) while retaining these clock, label and
silent-state restrictions.

### 45.3 All independent Einstein components reject a radial stream

The independently varied projected-H Hilbert tensor is

    T_H,ab=P[g_ab s_c s^c-2s_a s_b].

In the tested clock gauge its time/radial component is zero.
For H=h0(t)+C/r with constant C, subtracting this tensor from the
independently calculated P G_ab gives the required ordinary source
in the orthonormal clock/ruler frame:

    rho_m = 3P exp(2H) h0_dot^2,
    p_r,m = p_t,m = -P exp(2H) [2h0_ddot+5h0_dot^2],
    T_hat0r,m = 2PC h0_dot/r^2.

These are the independent time, radial, angular and mixed metric
equations. A radial null stream has p_r=rho, p_t=0 and rho>0.
Here p_r=p_t, so both required null-pressure conditions force rho=0,
then h0_dot=0 and zero flux. Positive counterpropagating radial streams
have the same pressure obstruction. No assumption about the sign of an
uncomputed radiation-feedback coefficient enters this result.

This excludes nonzero radial irradiation on the strict silent ansatz
even before imposing a regular centre or an asymptotically flat boundary.
The latter restrictions further set C=0 and h0=0, respectively.
It excludes a particular attempted continuation of an equilibrium
solution; the general five-field action permits additional field states.

### 45.4 Positive-radiation control and actual remaining input

For C=0, the same background equations admit the NON-isolated homogeneous
isotropic radiation control

    h0=(1/3) ln(t/t_star),     t,t_star>0,
    rho_m=3p_m>0,             rho_m exp(4h0)=P/(3t_star^2).

The photon-gas energy law and Einstein equation agree. This is an
isotropic radiation-fluid background control, not a constructed single
coherent Maxwell field. It is the ordinary homogeneous radiation geometry, not a radial
incoming beam or an isolated black hole. Perturbative medium health
is not established by this exact background control. It prevents the
restricted radial exclusion from being misread as a claim that the
theory forbids all radiation or all time dependence.

The operative decision is to retire the time-promoted silent exterior
as a radiation-evolution ansatz. A full calculation must evolve the
independent geometry, clock and material labels away from at least one
of its fixed-state restrictions. Keeping a common observational scale
does not authorize dropping their independent equations.

The repository inventory supplies no accepted ready off-silent response
for that calculation. Specifically, the exterior fixes F and its first
derivatives at one state, whereas sourced clock/compression/shear
evolution depends on F_yy, F_yB, F_BB and any retained derivative terms.
The existing explicit centre polynomial in common_scale_centre_source.md
section3 has local principal-health evidence but fails its isolated
join and radial continuation in section6. The KGB polynomial in
matter_medium_source_response.md is a different action, and its
original-pressure identification failed its own pressure-map test.
Neither is silently substituted for the full five-field response.

### 45.5 Verification and stop

The independent clock/H variations, full metric/source check, static
control and positive homogeneous-radiation control are implemented in
silent_exterior_irradiation_checks. Its **28/28** checks pass, and the full
completion regression passes **862/862**, retaining all 834 prior checks.
An independent isolated rerun also passes 28/28. All exact residuals are zero.
Completion verifier SHA256:
aee8c350034c74d4efba3ed64a4299caf9cf320327adf53ccc9953bd69230153.
Production verifier SHA256 remains:
1a23833cd7bc907da7bdda32f26c8ced9ec866f298423a646fb4827f7ce40500.
The four restricted verification flags close; full_medium_evolution_solved,
global_singularity_removal and full_RefG_rejected remain false.
An independent read-only derivation reproduces all
four required matter components and the clock-charge constraint.

This step makes an actual dynamical-entry decision: the exact silent
exterior cannot be the ansatz for the requested radial irradiation.
No new constitutive law or numerical collapse run is claimed. The
off-silent response must be selected and checked before a full coupled
evolution is determined. The original production equations, intuitive
files, articles and Git settings remain unchanged.

## 46. Pressure-wave completion: independent-metric admission test

### 46.1 Registered candidate and decision

CLAIM_ID: W92-PRESSURE-WAVE-EINSTEIN-ADMISSION.
GOAL/TYPE: test one explicit dynamical pressure law for admission as a
completion of the existing theory, before a numerical light-pulse run.
MODEL_VERSION: local pressure-wave prototype v1; p=exp(-H),
g=diag(-p^2,p^-2,p^-2,p^-2), preferred coordinates, c0=1,

    L_H = C/2 [exp(4H) H_t^2 - |grad H|^2],
    L_EM = 1/2 [exp(2H) E^2 - exp(-2H) B^2].

This positive-kinetic completion is a NEW trial action. Its static
gradient term has the Stage8 ancestor recorded in the health diagnostic.
It is not obtained by eliminating the independent fields of W92.
FREEDOM_LEDGER: one positive coefficient C; stationary massive probes
have L_probe=-m exp(-H). Matching the existing Newtonian normalization
fixes C=1/(4 pi G)=2P, with P=1/(8 pi G). No fitted pulse profile,
attenuation coefficient, new light cone or luminosity-dependent rule.
ASSUMPTIONS/DOMAIN: first derive the trial pressure equation exactly;
then test a smooth, weak, locally plane transverse Maxwell wave about
H=0. Field amplitude a gives radiation stress O(a^2), H=O(a^2),
and the original projected-H stress O(a^4). The exterior clock,
Cartesian labels and silent constitutive state are retained only for
the proposed embedding test. No isolated finite-energy plane wave is
claimed.
DEPENDENCIES: section44's common-pressure Maxwell action; section45's
independent-metric convention and silent-state restrictions.
METHOD/CROSSCHECK: Euler-Lagrange and Legendre transforms of the trial
action; derive the linearized Einstein tensor and Maxwell Hilbert
tensor independently, and compare all relevant components.
PASS_CONDITION: the trial equation and independent Einstein equations
admit the same nonzero weak pulse under the stated embedding.
FAIL_CONDITION/FALSIFIER: a nonzero leading-order metric residual after
the Hamiltonian and momentum constraints have been imposed. A missing
stress term of that order or an independent counterexample invalidates
the exclusion.
BENCHMARK: the zero-field vacuum and stationary Newtonian source.
OBSERVABLE_MAP: shared metric clock/ruler factors and local radiation
energy/stress, equal to their coordinate values at the tested leading
order. DATA_ROLE/FORWARD_MODEL/IDENTIFIABILITY: N/A; no observational
fit, model selection from data or empirical uniqueness claim.
RESIDUAL/ERROR_BOUND: symbolic leading-order coefficients; discarded
terms are O(a^4) in the perturbative expansion. No finite-amplitude
error bound or numerical evolution claim.
VALIDITY_HEALTH: positive trial Hamiltonian at finite H; this local
property does not supply the omitted independent metric equations.
BRANCHES: zero-field control retained; the nonzero Maxwell embedding
is the tested branch.
CLOSURE_FLAGS initially false: pressure_wave_variation_verified,
weak_metric_embedding_excluded. Full-medium and singularity flags
remain false.
FILES: existing completion verifier, this report and diagnostic index.
STOP: an admission failure ends this candidate test before simulation.
No change to the production action or solver is authorized by a
successful calculation inside this restricted trial action.

### 46.2 Calculation and decision

Varying the specified trial action gives

    C [exp(4H)(H_tt+2 H_t^2)-Delta H] = 2 epsilon_EM,
    epsilon_EM = [exp(2H) E^2+exp(-2H) B^2]/2.

Its canonical variables D=exp(2H)E and Pi=C exp(4H)H_t give

    Hamiltonian = Pi^2 exp(-4H)/(2C) + C |grad H|^2/2
                  + exp(-2H)(D^2+B^2)/2.

This energy is positive for real finite H and C>0; its scalar and
Maxwell principal coordinate speeds are p^2. The radiation source is
present. These properties make it a consistent restricted trial, but
the independent Einstein equations are a separate admission condition.

At the first nonzero order in Maxwell amplitude, write rho=a^2>0.
A right-moving transverse wave gives, with lower indices and
coordinates (t,x,y,z),

    (T_00,T_0x,T_xx,T_yy,T_zz) = (rho,-rho,rho,0,0).

For the reciprocal common-pressure metric the linearized Einstein
tensor is

    G_00=-2 H_xx, G_0x=-2 H_tx,
    G_xx=G_yy=G_zz=-2 H_tt.

The original projected-H stress starts at O(a^4); the retained silent
F stress vanishes. Consequently the independent x and y equations
already require both H_tt=-rho/(2P) and H_tt=0. The nonzero pulse
cannot satisfy this particular embedding.

This decision survives correctly prepared initial metric constraints
(the Einstein Hamiltonian/momentum pair, not all five-field equations).
At an event choose H_xx=-rho/(2P) and H_tx=rho/(2P). The Hamiltonian
and momentum residuals are then zero. The new trial equation with
C=2P predicts H_tt=rho/(2P), giving

    P G_xx-T_xx = -2 rho,     P G_yy-T_yy = -rho.

The failure is therefore at O(a^2), before strong-field or late-time
questions arise. A nonzero constant-pressure vacuum and the zero-field
limit have no such radiation source; the test is about the response to
an added weak source. No long numerical run can remove this leading
local incompatibility.

As a positive SOURCE control, releasing the reciprocal metric
restriction permits the linear conformal perturbation h_ab=2 f(x-t) eta_ab.
It satisfies all these Einstein source components when -2P f''=rho.
This is a local pure-Einstein control, not a full RefG branch or an
isolated plane-wave spacetime. It verifies that the tensor calculation
can admit nonzero light stress when the restrictive readout is released.

Decision: REJECTED_AS_SILENT_EINSTEIN_COMPLETION for pressure-wave v1.
The trial has not been inserted into the production model and no pulse
simulation is run. Its rejection applies neither to arbitrary
constitutive responses nor to the common-pressure principle in general.
In particular, an off-silent medium can contribute anisotropic stress
at O(a^2); that contribution was frozen out in this tested embedding.

The development target is now specifically the coupled directional
stress/flow response with the independent metric equations retained.
Adding a positive H_t^2 term to a single-readout reduction does not
supply it. This failed candidate does not determine which replacement
constitutive action passes. Full medium evolution and singularity
removal remain open; the original production equations, intuitive
files, articles and Git configuration are unchanged.

### 46.3 Verification record

The new pressure_wave_admission_checks passes 27/27 checks; the full
completion regression passes 889/889, including all 862 previous checks.
An independent read-only derivation and isolated rerun also pass 27/27.
The first isolated run exposed an unspecified real-field assumption in
the symbolic positivity predicate. Declaring real H explicitly resolved
that check without changing any physical equation or residual.
All identity residuals are zero; the physically obstructing Einstein
residuals are the nonzero values explicitly verified in section46.2.
Thus passing the regression verifies the rejection, not the candidate's
physical admission.

Completion verifier SHA256:
76de8dec37df9f0c5ca3bd3675723c67d9b8c9d4f177bd213dfc786e202411e4.
Production verifier SHA256 remains:
1a23833cd7bc907da7bdda32f26c8ced9ec866f298423a646fb4827f7ce40500.
Only pressure_wave_variation_verified and weak_metric_embedding_excluded
close. Full-medium evolution, global singularity removal and full RefG
rejection flags remain false. This completes the registered admission
decision and stops the rejected prototype before numerical evolution.

## 47. Locating the obstruction: outer black-hole scale versus inner scale

### 47.1 Bounded scale-location contract (2026-09-18)

CLAIM_ID: W92-INNER-OUTER-SCALE-LOCATION.
GOAL: decide whether the known inner-horizon obstruction must lie at the
outer black-hole size or can lie at a parametrically smaller areal radius.
TYPE: exact geometry and controlled small-ratio asymptotics of the
EXISTING spherical rational-response candidate, not a new response law.
MODEL_VERSION: f=1-2mr^2/(r^3+2m ell^2), m>3sqrt(3)ell/4, ell>0.
DOMAIN: its two simple positive horizons r_minus<r_plus. The extremal
limit is a boundary control, not part of the simple-horizon claim.
CONVENTIONS/OBSERVABLE_MAP: m=GM/c0^2 is geometric mass, r is areal
radius (sphere area 4 pi r^2), ell is the candidate's fixed core length;
surface gravity uses the infinity-normalized static Killing field.
ASSUMPTIONS/FREEDOM_LEDGER: ell remains unspecified by observations or
the RefG medium. No Planck-length identification, astronomical mass,
pressure readout or universal microscopic ontology is assumed.
DEPENDENCIES: the sourced candidate of sections1--3; its certified
finite-time evolution in section23; the source-specific inner-horizon
counterexample in section37; the full-coframe interpretation in section36.
METHOD/CROSSCHECK: factor the horizon polynomial using the horizon
ratio eta=r_minus/r_plus; independently differentiate f at fixed m
before restricting to a horizon. Check cubic residuals, monotonic
mass-ratio inversion, curvature and asymptotic coefficients.
BENCHMARK: the m/ell=2 member used in section37; large m/ell and the
coincident-horizon endpoint. Three ILLUSTRATIVE dimensionless mass
ratios 2, 10^3 and 10^6 are fixed before numerical evaluation.
PASS_CONDITION: an exact positive branch permits eta->0 as m/ell->infinity,
with the actual inner radius, q and surface gravity quantified.
FAIL_CONDITION/FALSIFIER: incorrect root, lost positive branch, a
nonzero identity residual or an inner radius tied to the outer size
throughout the stated family.
RESIDUAL/ERROR_BOUND: exact identities; asymptotic orders reported
explicitly. Numerical inversion uses 120 bisections on eta in (0,1)
with exact rational endpoint signs; decimal readouts are illustrations.
VALIDITY_HEALTH: this is a geometry-location test. No medium stability,
new source evolution, centre prescription or singularity removal follows.
BRANCHES: nonextremal two-horizon branch; extremal boundary; the
horizonless family is outside this decision.
DATA_ROLE/FORWARD_MODEL/IDENTIFIABILITY: N/A, no observational fit or
unique determination of ell.
CLOSURE_FLAGS initially false: horizon_scale_location_verified,
inner_core_scale_separation_verified; global and full-medium flags
remain false.
FILES: existing completion verifier, this report and diagnostic index.
STOP: locate the known problem and delimit the BH-regime claim. Do not
repeat the t<=70 evolution, relabel an inner BH horizon as outside the
black hole, or select another constitutive action in this stage.

### 47.2 Calculation and decision

Define eta=r_minus/r_plus in (0,1) and D=1+eta+eta^2. Exact
factorization of r^3-2mr^2+2m ell^2 gives

    r_minus/ell = sqrt(D),       r_plus/ell = sqrt(D)/eta,
    m/ell = D^(3/2)/[2 eta(1+eta)].

The third root is -ell sqrt(D)/(1+eta)<0. The logarithmic derivative
of the mass ratio is

    d ln(m/ell)/d eta =
      (eta-1)(eta+2)(2eta+1)/[2 eta(1+eta)D] < 0.

Thus each nonextremal mass ratio has exactly one admissible eta.
At eta=1 the horizons coincide and m/ell=3sqrt(3)/4. As eta->0,
m/ell->infinity, r_minus->ell and r_plus/(2m)->1.
Writing mu=m/ell, the inverse-mass expansions are

    r_minus/ell = 1 + 1/(4mu) + 5/(32mu^2) + O(mu^-3),
    r_plus/(2m) = 1 - 1/(4mu^2) - 1/(8mu^4) + O(mu^-6),
    r_minus/r_plus ~ 1/(2mu).

The three registered examples give:

| m/ell | r_minus/ell | r_plus/ell | r_minus/r_plus |
| ---: | ---: | ---: | ---: |
| 2 | 1.1939365665 | 3.7092753594 | 0.3218786557 |
| 1,000 | 1.0002501564 | 1999.9995000 | 0.0005001252 |
| 1,000,000 | 1.0000002500 | 1999999.9999995 | 0.000000500000125 |

These are dimensionless model examples. Each ratio is enclosed by
exact rational endpoints separated by 2^-120; the script emits them.
The large example puts the inner horizon at approximately one
two-millionth of the outer horizon's areal radius.

### 47.3 What is and is not moved to the deeper scale

For this metric, at fixed finite mu, the screening and inner surface
gravity are

    q_minus = eta(1+eta)/D = r_minus/(2m) > 0,
    kappa_minus = (3-D)/(2 ell D^(3/2)) > 0.

The corresponding outer surface gravity is
eta(D-3eta^2)/(2 ell D^(3/2)); hence
kappa_minus/kappa_plus=(eta+2)/[eta(2eta+1)].
At large mu,

    q_minus ~ 1/(2mu),         kappa_minus ~ 1/ell,
    K_background(r_minus) -> 24/ell^4,
    K_background(r_plus) ~ 3/(4m^4).

Here q is the rational gravitational response coefficient, not a newly
identified foundation-pressure or clock factor. These curvature values
belong to the stationary background. Section37's freely falling tidal
divergence concerns the additional specified incoming null source.

The scale distinction is real: when m>>ell, the previously identified
inner-horizon difficulty is located at the core scale, very far inside
the outer black-hole scale. This supports the possibility raised by the
user that the relevant limitation is much deeper than the outer
black-hole environment. It does not put that inner horizon outside the
black hole or determine ell in metres. Near the extremal threshold the
two scales are comparable; large separation is conditional on m>>ell.

For each fixed finite nonextremal mu, q_minus and kappa_minus remain
positive. Therefore their large-mass limits do not remove section37's
late-time counterexample. Small fixed screening can coexist with
unbounded freely falling amplification. Taking an infinite-mass limit
first would change the question. No new all-source theorem is claimed.

The existing positive result in section23 remains finite-time sourced
trapping with bounded tested curvature through t=70. The existing
negative result in section37 remains a different, precisely specified
source with a finite-proper-time inner obstruction. The present result
locates their relevant geometric scales; it changes neither verdict.

The next dynamical development must use the full coframe already
restored in section36 and a specified medium response in this inner
region. Reimposing the exact reciprocal single-H metric would reopen
the restricted failures in sections45--46. No new constitutive law is
selected here, and neither a quantum hierarchy nor Planck-scale physics
has been inserted into the model.

### 47.4 Verification and stop

horizon_scale_location_checks passes 24/24 new checks; the full
completion regression passes 913/913, including all 889 prior checks.
An independent derivation, code review and isolated rerun confirm
24/24 and the three numerical ratios. All registered identity
residuals are zero; the exact root brackets pass their sign checks.
The script implements the series using d=ell/(2m), with inner residual
O(d^3) and normalized outer residual O(d^6).

Completion verifier SHA256:
7c0079a7b6a7b903caa878c24cf7c8e012d7a3ed1cb807bf07956afd7d26b328.
Production verifier SHA256 remains:
1a23833cd7bc907da7bdda32f26c8ced9ec866f298423a646fb4827f7ce40500.
Only horizon_scale_location_verified and
inner_core_scale_separation_verified close. Physical calibration of
ell, full-medium evolution, singularity removal and full RefG rejection
remain false. The registered location decision is complete.
Production, intuitive files, articles and Git configuration are unchanged.

## 48. Source weakening and the pressure-zero endpoint: keep both clocks

Internal admission decision, 2026-09-18. The author's input is reciprocal
feedback: matter produces the pressure deficit, and that same deficit
reduces its source strength. The decision here is the precise time bound
this mechanism must meet. No additional source or evolution law is introduced.

### 48.1 Frozen contract

CLAIM_ID: W3_92_PRESSURE_CLOCK_ENDPOINT; TYPE: conditional comparison
theorem with exact algebra/control checks; MODEL_VERSION: clock audit v1.
GOAL: decide whether source weakening alone establishes a never-zero
pressure, and specify the sufficient rate bound in the existing clock map.
ASSUMPTIONS/DOMAIN/CONVENTIONS: p>0 is the dimensionless material/clock
factor; t and tau denote the two specified clocks, d tau=p dt. This is
the at-rest common-scale dictionary of section44, not the proper time of
an arbitrary moving observer or a chart assumed across a BH horizon.
For the autonomous endpoint test F(p)>0 is continuous, and the branch
continues through every positive pressure level. For the comparison,
Gamma_max>0 is an assumed finite bound along the branch.
FREEDOM_LEDGER: p0 is an initial value; gamma in the controls is a rate
with inverse-time units, not a fitted coupling or selected RefG law.
DEPENDENCIES: section44's clock dictionary; Stage8's static response;
W3-75's separately defined homogeneous branch.
METHOD/CROSSCHECK: chain rule and comparison proof, verified by exact
primitives and independent substitution of the equality history.
PASS: the clock conversion and endpoint primitives agree; controls
distinguish vanishing loss from infinite endpoint time.
FAIL/FALSIFIER: wrong clock factor, nonzero identity residual, or use
of an assumed Gamma bound as if derived from the matter action.
RESIDUAL/ERROR_BOUND: exact algebra, no numerical endpoint extrapolation.
VALIDITY_HEALTH: an ODE endpoint comparison, conditional on the stated
continuation; no PDE regularity, mode health or curvature gate closes.
BRANCHES: quadratic-loss equality control and linear/root-loss negative
controls are mathematical examples only. OBSERVABLE_MAP: stated clocks.
FORWARD_MODEL/DATA_ROLE/IDENTIFIABILITY/BENCHMARK: no data or fit; the
controls only test the endpoint inference, not competing physical laws.
CLOSURE_FLAGS: only clock_criterion_algebra_verified may close.
PROVENANCE/FILES: this section and pressure_clock_endpoint_checks in
verify_saturation_completion_boundary.py. All dynamics, intuition,
articles and Git settings remain unchanged. STOP: record this one
admission condition and the existing evidence; no new constitutive scan.

### 48.2 The clock-correct sufficient condition

Write the pressure loss along the specified clock as dp/dt=-F. Then

    dp/dtau=-F/p,     Gamma=-(dp/dtau)/p=F/p^2.

Thus if 0<=Gamma<=Gamma_max along the solution,

    d(1/p)/dt=Gamma <= Gamma_max,
    p(t) >= p0/[1+Gamma_max*p0*(t-t0)],
    p(tau) >= p0*exp[-Gamma_max*(tau-tau0)].

Integration of d tau=p dt also gives

    tau-tau0 >= log[1+Gamma_max*p0*(t-t0)]/Gamma_max.

Both finite-time lower bounds are positive; if the branch continues
to arbitrarily large t, its local elapsed time is also unbounded.
For a zero asymptote one additionally needs integral Gamma d tau to
diverge. Otherwise a positive limiting value is possible.
These are comparison results, not a selection of constant Gamma.

For a positive autonomous F, the exact zero-endpoint tests are

    t_* - t0 = integral_0^p0 dp/F(p),
    tau_* - tau0 = integral_0^p0 p dp/F(p).

A linear loss F=gamma*p vanishes at p=0 but gives infinite t and finite
tau_*-tau0=p0/gamma. A root loss F=gamma*sqrt(p) even gives finite
t_*-t0=2*sqrt(p0)/gamma. They show why vanishing source/loss alone
does not supply a sufficient endpoint estimate. These controls are not
introduced into RefG. A finite endpoint here is a boundary of this
clock description, not a proof of a spacetime singularity.

### 48.3 What the existing calculations actually supply

W92 Stage8 solves a fixed-radius static ensemble:
u=W_0(kB), p=exp(-u), M_G=Bp and dp/dB=-kp^2/(1+u).
It includes the weakened contribution of every pre-existing constituent.
B is a population parameter, not time. This equation supplies no
dp/dtau for collapse at fixed B; the documented independent-source
and total-energy closure failures of that trial remain in force.

W3-75 genuinely proves a future proper-time no-zero result:
dp/dtau=-(3/5)Hp with 0<H<=H_i from its homogeneous current/Einstein
equations. Its verifier was rerun: 38 identity checks pass, all
dependency hashes agree, and aggregate_pass is true.
The branch uses n/n0=p^5, P_F/P0=p^2 and operational A=p^(-5/3).
It is expanding and homogeneous. Its microscopic pressure map and
direct ordinary-oscillon/collective transfer remain un-derived.
Its A is not section44's spatial factor p^(-1); relabelling time
does not identify those two geometries or transfer the theorem to a BH.

The Stage8 rerun passed all 56 mathematical/numerical checks and two
of three dependency checks. The remaining historical pin for
intuitive/RefG_GE.md is stale (current hash begins 1ec492831c68);
the unmodified mode therefore returns failure. The pin was not
silently updated and this rerun is not labelled an aggregate pass.

Decision: the explicit missing physical input is the coupled
inhomogeneous response law or a sufficient endpoint estimate, such
as a finite bound on the local fractional response Gamma.
The single-oscillon source scaling and optical clock identities do
not by themselves determine it. The admission condition is now fixed;
neither a new BH solution nor its impossibility is inferred.

### 48.4 Verification

The scoped check and an independent read-only rerun each pass 22/22.
The full completion regression passes 935/935 (22 new and 913 prior).
All new exact residuals are zero. The counterexamples establish the
limits of the endpoint inference, not failures of a simulated RefG
source. No constitutive coefficient or pressure trajectory was fitted.
Only clock_criterion_algebra_verified closes. The sufficient rate
bound, BH interior and global singularity-removal flags remain false.
The analytic comparison above supplies the theorem; test counts
check its algebra and controls, rather than proving global evolution.

## Reproduction and attribution

    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_spherical_saturation_bridge.py"
    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_inverse_saturation_candidate.py"
    python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_saturation_completion_boundary.py"

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

[3] R. J. van den Hoogen and H. Forance, *Teleparallel Geometry with
Spherical Symmetry: The diagonal and proper frames*, sections4.2-4.5,
[primary text](https://arxiv.org/html/2408.13342v1).
Used for the complete spherical frame/spin parametrization; the
F(n)T/current quadratic action and constrained radial operator are
independently derived here.

[4] R. Carballo-Rubio, F. Di Filippo, S. Liberati, C. Pacilio and M. Visser,
*Regular black holes without mass inflation instability*, JHEP 09 (2022) 118,
[primary text](https://arxiv.org/html/2205.13556v1).
Section39 specializes equation(12), checks the denominator independently,
and derives its own fixed-law and null-ray results. The construction is
credited to this source; RefG compatibility is tested separately.

[5] S. Dubovsky, T. Gregoire, A. Nicolis and R. Rattazzi,
*Null energy condition and superluminal propagation*, JHEP 03 (2006) 025,
[primary text](https://arxiv.org/abs/hep-th/0512260).
Context for conditional energy/characteristic-cone restrictions, not a
substitute for section41's explicit medium calculation.

[6] V. Faraoni, E. Gunzig and P. Nardone,
*Conformal transformations in classical gravitational theories and in
cosmology*, Fund. Cosmic Phys. 20, 121 (1999),
[primary text](https://arxiv.org/html/gr-qc/9811047v1), sections1--2.
Source for the conformal/scalar--tensor framework and physical-frame
distinction. Section43 specifies its own restricted action and checks
its independent equations; the framework is not claimed as new RefG physics.
