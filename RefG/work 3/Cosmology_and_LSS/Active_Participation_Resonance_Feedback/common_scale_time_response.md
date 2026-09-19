# საერთო მასშტაბის დროითი პასუხი

2026-09-19. სივრცე–მატერიის უკუკავშირის გამოცდა ძლიერი ველის წინ.

## სამუშაოს საზღვარი და წინასწარი კონტრაქტი

სამიზნეა უკვე განსაზღვრული სკალარული კანდიდატის დროითი პასუხი:
მატერიის შეცვლილი მდგომარეობა როგორ ცვლის ფუძეს და როგორ უბრუნდება
ეს ცვლილება იმავე მატერიას. გამოიყენება
[სასრული წყაროს მოქმედება](common_scale_finite_source_candidate.md).
მისი არც ერთი კოეფიციენტი, პოტენციალი ან წყარო არ იცვლება.
დამოუკიდებელი აინშტაინური/სპინ-2 დინამიკის შეერთება ამ გამოცდას
არ აქვს; სრული RefG-ის ჩანაცვლება და ძლიერი ველი ამოცანის ფარგლებს გარეთაა.

- CLAIM_ID / MODEL_VERSION: COMMON_SCALE_TIME_RESPONSE_V1, unchanged
  COMMON_SCALE_FINITE_SOURCE_CANDIDATE_V1 action.
- CLAIM / TYPE: derive its time-dependent scale equation and sector energy
  exchange; test finite-time weak radial response; prove a separately
  scoped homogeneous charged-cell no-zero statement from conserved energy.
- ASSUMPTIONS / DOMAIN / CONVENTIONS: c0=1, alpha>0, p=exp(-u)>0,
  signature -+++, two real components of the inherited complex field.
  P_F/P_F0=p² is the retained pressure readout; p is its scale factor.
  Each proof/test below states its spatial and temporal domain.
- FREEDOM_LEDGER / DEPENDENCIES: unchanged sextic potential and W58 seed;
  alpha=.003 and fixed Q from the preceding stationary test. New test
  freedoms are perturbation amplitude/profile, grid and finite run time,
  frozen below. No added damping, source multiplier or pressure floor.
- METHOD: independent Euler–Lagrange and Noether derivations; exact
  constant-background solution scaling; coercive homogeneous energy
  bounds; conservative radial spatial discretization and time integration.
- PASS_CONDITION: exact identities have zero symbolic residual. Numerical
  run must preserve charge to 1e-7 and total energy to 1e-6 relative,
  remain |u|<.1, and have medium/fine central-p and charge-radius
  differences <2e-3 relative. Baseline-subtracted response must refine
  from coarse/medium to medium/fine, unless at roundoff. A return/turn is
  reported only if observed, never built into the acceptance definition.
- FAIL_CONDITION / FALSIFIER: nonzero symbolic residual rejects its
  identity; failed numerical thresholds withhold that test's evidence.
  No numerical finite time is used to certify all future times.
- RESIDUAL / ERROR_BOUND / BENCHMARK: three grids and identical-grid
  unperturbed controls; exact energy exchange checked separately from
  time-integration drift. Thresholds and initial data are fixed before
  the first evolution. Results and actual residuals are recorded below.
- VALIDITY_HEALTH / BRANCHES: positive kinetic energy and common p²
  principal cone of the specified action; small radial perturbations
  of the preceding weak stationary solution. No new high-density branch.
- OBSERVABLE_MAP: p=e^-u, local clock d tau=p dt, coordinate standard
  length/rest-energy/cadence scale p, light speed p². Global charge RMS
  radius and full energy are distinguished from a local standard.
- FORWARD_MODEL / DATA_ROLE / IDENTIFIABILITY: no observational data or
  fit. Internal candidate test, with no empirical or uniqueness claim.
- CLOSURE_FLAGS: exact_time_equations, exact_exchange, uniform_scaling,
  homogeneous_charged_no_zero and finite_time_response are separate.
  Full_RefG_closure, spatial_centre_no_zero, arbitrary_load_no_zero,
  singularity_resolution, asymptotic_relaxation and observational_pass
  remain false.
- CROSSCHECK / PROVENANCE / FILES: independent symbolic companion
  common_scale_time_identities.py and numerical common_scale_time_response.py;
  both print results to stdout and write no output artifacts. The earlier
  stationary script and W58 source remain unchanged.
- STOP: record the actual time-response decision and the exact no-zero
  domain. No strong-field continuation or longer collapse run follows.

## 1. Same action, explicit pressure equation

Write psi=a+i b, w=exp(2u)=p^-2 and

    V = |psi|²/2 - |psi|⁴/4 + |psi|⁶/24.

The original action becomes

    L = [w_t² - |grad w|²/w²]/(8 alpha)
        + w² |psi_t|²/2 - |grad psi|²/2 - w V.

Its full time equations are

    psi_tt + 2(w_t/w) psi_t - w^-2 Delta psi + w^-1 V_psi = 0,
    w_tt - w^-2 Delta w
        = -w^-3 |grad w|² + 4 alpha w |psi_t|² - 4 alpha V.

The equivalent scale equation is

    p_tt - p⁴ Delta p
      = 3 p_t²/p - p³ |grad p|²
        - 2 alpha p |psi_t|² + 2 alpha p³ V.

Thus the pressure acceleration is determined by the same evolving matter,
spatial response and scale velocity. It is a second-order coupled law:
a separate imposed first-order p_t=-K p² is not inserted.
At a point with local clock d tau=p dt, psi_t=p psi_tau. Consequently
the matter contribution to this equation can also be written

    -2 alpha p³ (|psi_tau|² - V).

This source includes kinetic and potential response together; its sign
depends on the state. Spatial gradients and the scale's inertia are also
part of the equation. The pressure readout follows without another law:

    (P_F)_t/P_F0 = 2 p p_t,
    (P_F)_tt/P_F0 = 2 p_t² + 2 p p_tt.

## 2. Energy transferred once, with its sign retained

The canonical sector energies and their fluxes are

    H_u = [w_t² + |grad w|²/w²]/(8 alpha),
    H_m = w² |psi_t|²/2 + |grad psi|²/2 + w V,
    J_u = -w_t grad w/(4 alpha w²),
    J_m = -Re(psi_t* grad psi).

H_u is the kinetic/gradient energy of the scale-response field. It is
zero for every uniform static u, even though P_F=P_F0 exp(-2u) changes
between such states. Its growth therefore says nothing by itself about
growth of static foundation pressure or stored tension. A constitutive
stored-tension energy has not been derived in this candidate.
See the [energy-interpretation audit](foundation_tension_energy_audit.md).

On the same equations,

    partial_t H_u + div J_u = X,
    partial_t H_m + div J_m = -X,
    X = w_t (w |psi_t|² - V).

Hence total energy is conserved with its boundary flux. No energy is
discarded when the externally read matter energy changes. X may have
either sign: a conservative restoration can exchange energy back and
forth. A final damped equilibrium would require energy leaving the
chosen subsystem; this finite-time test does not impose such damping.
Here total energy means the complete Hamiltonian of the stated two-field
candidate; it does not silently include a further background reservoir.

## 3. Where the two external factors occur exactly

Choose a CONSTANT background scale s>0. From any solution in variables
(T,X), construct

    T=s t,    X=x/s,
    u_ext(t,x)=-ln s + U(T,X),
    psi_ext(t,x)=Psi(T,X),
    p_ext(t,x)=s p_local(T,X).

Every term of the action density scales as s^-2 while
d t d³x=s² dT d³X. The full action is unchanged, with the same alpha.
This is a map between solutions with correspondingly scaled constant
backgrounds, not a replacement of a varying p(t,x) by a constant.
At fixed spatial points the resulting readouts are

    E_ext=s E_local,       Q_ext=Q_local,
    L_ext=s L_local,       Omega_ext=s Omega_local,
    transported_power_ext=s² transported_power_local,
    partial_t p_ext=s² partial_T p_local,
    partial_t(p_ext²)=s³ partial_T(p_local²).

The first power in transported energy and the first power in cadence
produce the quadratic transported-power factor. Coordinate source
density scales as s^-2 and coordinate volume as s³, giving total source
mass proportional to s. Multiplying that source once more by an
independent size factor would change the action's derived equation.

აქ ორი გარე ფაქტორი ერთიან დინამიკასთან შეთანხმებულია.
ერთი პროცესის სხვადასხვა მუდმივ ფონზე შედარება და ერთი სისტემის
დროში განვითარება სხვადასხვა ოპერაციაა. მეორე უკვე §1-ის სრული
განტოლებებით გამოითვლება. ასევე გამიჯნულია p-ს კვადრატული ტემპის
ამოკითხვა და ძველი P_F=p² P_F0 წნევის კუბური ტემპის ამოკითხვა.

## 4. A derived no-zero theorem in a homogeneous charged cell

Consider the SAME equations with no spatial gradients, in a homogeneous
closed periodic coordinate cell. There is no influx or boundary work.
Its coordinate volume is fixed; proper volume follows p^-3 through the
same metric. No independent prescribed expansion is added.
Its energy and U(1) charge per coordinate volume are conserved:

    epsilon = w_t²/(8 alpha) + w² |psi_t|²/2 + w V,
    j = w² Im(psi* psi_t).

Assume finite initial epsilon>0, w0>0 and j!=0. This j is the model's
charge, not a separately established count of particles.
The inherited potential has the exact positive decomposition

    V(f) = f² [(f²-3)²+3]/24 >= f²/8,    f=|psi|.

Charge and the positive energy therefore give

    epsilon >= j²/(2 w² f²) + w f²/8 >= |j|/(2 sqrt(w)),
    w >= j²/(4 epsilon²) > 0,
    |w_t| <= v := sqrt(8 alpha epsilon).

For all forward coordinate times,

    w(t) <= w0 + v t,
    p(t) >= 1/sqrt(w0+v t),
    P_F(t)/P_F0 >= 1/(w0+v t).

The lower bound on w, upper bounds on w and |w_t|, and

    |psi|² <= 8 epsilon/w,    |psi_t|² <= 2 epsilon/w²

keep the homogeneous ordinary differential equations smooth on every
finite interval. Thus their solution continues globally; the argument
does not assume a solution exists up to infinity.

The cell's proper time obeys

    tau(t)-tau(0) >= (2/v)[sqrt(w0+v t)-sqrt(w0)] -> infinity.

Therefore p and P_F cannot reach zero at finite external OR proper time
in this domain. No monotonicity, imposed pressure floor, bounded-Gamma
postulate or hand-added p² relaxation law was assumed. For completeness,

    |p_t| <= sqrt(2 alpha epsilon) p³

is a derived RATE BOUND, not the exact trajectory or a universal p³ law.
The theorem permits oscillatory pressure and says nothing by itself
about convergence to zero or a particular final equilibrium.

## 5. Exact boundary of the spatial extension

For a finite-energy spherical configuration on all space, u->0 at
infinity, positive energy gives at every fixed r>0

    |u(t,r)| <= sqrt[alpha E_total/(2 pi r)].

This follows directly by integrating u_r from r to infinity and applying
Cauchy–Schwarz to the radial gradient energy. If a smooth all-time
solution exists with conserved E_total, this fixed-radius bound also
makes its corresponding proper time unbounded. Independently,

    ||w(t)-w(0)||_L2 <= t sqrt(8 alpha E_total).

Neither estimate controls the point r=0: finite total energy alone does
not bound a pointwise concentration in three spatial dimensions.
The homogeneous theorem consequently has its own precise scope.
Central nonlinear continuation of an inhomogeneous source remains a
distinct unresolved condition; a finite numerical run cannot replace it.

## 6. Frozen finite-source time test

The initial equilibrium has alpha=.003 and the unchanged reference
charge Q=190.401136223484, solved on R=60. Use the exact same action's
radial Hamiltonian equations for u,a,b and their canonical momenta.
The spatial discretization is conservative radial finite volume, with
the static exterior u-tail energy and its variational Robin boundary.
Run RK4 with dt=.2 dr, dr in {.12,.06,.03}, T_end=24; sample every .12.
Each grid has its own unperturbed control.

The small perturbation is delta u=.005 B(r). Here B=1 for r<=8,
B=0 for r>=12, and the intervening shape is the fixed C2 quintic
1-10 z³+15 z⁴-6 z⁵, z=(r-8)/4. With s(r)=r exp(delta u),

    u_initial(r)=u_equilibrium(s(r))+delta u(r),
    a_initial(r)=f_equilibrium(s(r)), b_initial=0,
    pi_u=pi_a=0,
    pi_b=C_Q exp(4 u_initial) Omega exp(-delta u) a_initial.

C_Q is the single normalization preserving the discrete equilibrium Q.
Its computed deviation from one is reported. This sets a common-scaled
core with a finite physical transition to its surroundings; it is not
an independent mass reduction or a new equilibrium boundary condition.
The taper makes it a real perturbation, not a uniform global symmetry.

Matter's outer boundary is effectively zero in its exponentially small
tail. The perturbation begins inside r=12, and the r=60 outer boundary
is causally too distant to return its signal to the core by t=24.
No external radiation stream or phenomenological loss term is inserted.
Any emitted response belongs to the already specified coupled fields.

## Results

**საცდელი მოქმედებიდან დროითი უკუკავშირის განტოლებები გამოვიყვანეთ და
სასრულ შუალედში მცირე გადახრაზე აღდგენითი მოძრაობა გამოვითვალეთ.** ენერგიის გაცვლა, საათის
ამოკითხვა და ფუძის პასუხი ერთსა და იმავე განტოლებებში მონაწილეობს.
ცალკე მიღებულია §4-ის ერთგვაროვანი დამუხტული უბნის ზუსტი
მიუღწევლობის მტკიცება. მისი პირობები სივრცულ ცენტრზე არ გადაგვაქვს.

### Exact identities and endpoint proof

The saved independent verifier passed 43 checks, including re-variation
of the original and transformed actions, off-shell Noether identities,
constant-background scaling, positivity certificates, and negative
controls for an extra scale factor and omitted work. All exact residuals
are zero. The homogeneous continuation proof uses the displayed energy
and charge bounds, rather than a finite numerical time interval.

### Actual finite-source evolution

All 29 original numerical checks passed at the frozen three resolutions
and T_end=24, with identical-grid unperturbed controls. The saved run was
independently repeated. On the fine grid, the perturbation starts with

    delta p_c(0) = -0.004864489351,
    delta R_Q(0) = -0.013154671741.

Both quantities are differences from the unperturbed control, not absolute
pressure or size. The source responds dynamically:

| External time | Central p difference | Charge-radius difference |
|---:|---:|---:|
| 0 | -.004864489351 | -.013154671741 |
| 6 | -.004864398510 | -.014257806420 |
| 12 | +.001351398598 | +.025784918349 |
| 18 | -.000649620358 | +.019907556581 |
| 24 | +.000175060376 | +.009754376957 |

Central p crosses its control near t=9.00; the charge radius crosses near
t=10.80. The first resolved radius reversal occurs near t=8.64, with
sample spacing .12. These are restoring/overshooting motions, not final
settling. The central p excursion includes an inward spherical pulse
from the finite taper; its largest positive difference is .02083958665.
It is not a pure normal-mode measurement. Turn diagnostics added after
the first run require prominence above twice the measured medium/fine
response difference; the original physical acceptance tests are unchanged.

The maximum |u| on the fine perturbed run is .02997917. The minimum p over
the evolved cell values is .97046575. The extrapolated central diagnostic
can differ slightly from this cellwise minimum. No strong-field regime
is entered.

### Energy, charge and clocks

The fine-grid discrete initial charges of the control and perturbation
agree at Q=190.407020706945. This finite-volume quadrature approximates
the continuum reference 190.401136223484; its offset decreases as dr².
Charge is preserved between the two initial states on each grid and
through each evolution. The fine-grid preparation factor C_Q is
.999995499034, a -4.50097e-6 relative correction.

Preparing the finite perturbation changes the total initial energy by
1.861051411 compared with its control: it is an explicitly excited state,
not spontaneous energy creation. After preparation each system is closed.
For the fine perturbed run:

| Time | Scale-response kinetic/gradient energy | Matter energy | Sum |
|---:|---:|---:|---:|
| 0 | 4.3312927101 | 173.2081167439 | 177.5394094540 |
| 12 | 2.2672777311 | 175.2721317225 | 177.5394094536 |
| 24 | 3.3179159869 | 174.2214934667 | 177.5394094536 |

The instantaneous Hamiltonian derivatives independently satisfy
dot E_u=X_integrated and dot E_m=-X_integrated to 1.13e-14 on the fine
perturbed run. For example X_integrated is -.0755731 at t=6 and
+.6839091 at t=12: exchange reverses direction within the same evolution.
The maximum total-energy relative drift is 2.68e-12 and charge drift
1.34e-12 on that run; the worst across all six runs is respectively
1.14e-9 and 7.08e-10.

At external t=24 the central clock integral is tau=23.40590247, versus
23.40793890 in its control. These are dimensionless simulation times.
The perturbed central phase cadence changes from .7832546822 to
.7910215495 in external time; its local-clock values change from
.8070899429 to .8108833943. A real excited state evolves locally as well;
the invariance in §3 compares identically scaled local states, not
different points of this physical oscillation.

R_Q is the signed U(1)-charge second-moment diagnostic, not a particle
probability radius. Its integrand develops a small negative component,
with maximum integrated negative fraction 3.03e-6 in the fine run.

### Numerical accuracy and independent implementation check

Medium/fine maximum relative differences are 2.42e-4 for central p and
1.33e-4 for R_Q. Baseline-subtracted maximum differences fall from
5.7740e-4 to 2.3694e-4 for p, and from 1.2196e-4 to 3.0429e-5 for R_Q.
Thus refinement ratios are 2.44 and 4.01 respectively. Energy conservation
errors are distinguished from these larger spatial-discretization errors.

The instantaneous discrete pressure-acceleration budget closes to
2.1e-17 on the fine run. This verifies the implemented equation's terms;
pointwise second derivatives themselves have no convergence claim.

An additional reproducible off-shell check compares finite differences
of the full discrete Hamiltonian, including boundary energy, with its
canonical right-hand side. Its best relative directional-derivative
error is 1.01e-10. This implementation audit was added after the first
evolution and does not tune the physical experiment.

### Status and reproducibility

Completed within this candidate: explicit pressure-time law, one conserved
energy budget with sector exchange, common-scale solution covariance,
homogeneous charged-cell no-zero theorem, and finite-time weak radial
restoring response. The spatial centre's all-time nonlinear continuation
and attachment to the full RefG tensor theory remain unresolved.
Strong-field calculations, Canon and the intuitive manuscript are unchanged.

Run from the repository root:

    python -X utf8 -B "RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/common_scale_time_identities.py"
    python -X utf8 -B "RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/common_scale_time_response.py"

Both scripts print provenance and results to stdout. They do not save
simulation files or caches. The unchanged candidate source is pinned by
SHA256 6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8.
Both verifiers print their current own SHA256. A subsequent interpretation
audit renamed response-energy output keys and added explicit scope flags;
the action, evolution, thresholds and numerical values remain unchanged.
Environment: Python 3.10.6, NumPy 1.24.3, SymPy 1.13.3, SciPy 1.15.2.
