# W3-83: Finite-time self-gravitating charged-pulse accretion

## One physical decision

Evolve one localized pulse of the FULL W3-80 collective complex field into a
pre-existing trapped region, including its gravitational backreaction, and
measure the changing outer marginal sphere and conserved-charge transport.
The output is an actual time history. Parameters are fixed below, not searched
for a desired outcome. The existing W3-73/W3-79 Einstein equations are reused.
No new pressure law, scale connection, potential, ordinary/collective coupling,
or interpretation of the lapse as foundation pressure is introduced.

Only this contract and one stdout-only solver/verifier may be created in this
folder. Stop after one physical run, its prescribed numerical comparisons and
independent audit. Intuitive files, upstream packages, publication and versions
remain unchanged. No generated results, plots, caches or bytecode are written.

## Frozen claim and domain

- CLAIM_ID: W3_83_FULL_COLLECTIVE_CHARGED_PULSE_ACCRETION.
- CLAIM: The specified full Einstein--complex-scalar initial/boundary problem
  has a numerically resolved finite evolution on the stated excised domain;
  the outer marginal-sphere trajectory and charge transfer are computed with
  independently monitored Einstein and matter constraints. The physical
  outcome is classified after the evolution, separately from numerical PASS.
- TYPE: NUMERICAL_EVIDENCE_FOR_ONE_FINITE_TIME_INITIAL_VALUE_PROBLEM.
- MODEL_VERSION: W3-83-v1.1. The v1.0 physical problem remains unchanged.
  Its first numerical protocol and actual failures are retained below.
  The explicit v1.1 amendment at the end supersedes only the identified
  refinement and horizon diagnostics before the amended runs are executed.
- ASSUMPTIONS: One Einstein metric; G=m_C=lambda_C=M_seed=1, Lambda=0.
  Only the W3-80 collective Cartesian scalar is populated. The ordinary
  scalar is identically zero, a consistent sector of the additive action.
  The full amplitude is retained, with no instantaneous fluid-EOS elimination.
- DOMAIN: Spherical ingoing PG coordinates, 1<=r<=14, 0<=T<=4. A seeded
  trapped interior is excised at r=1. This is accretion onto an existing
  object, not first formation from a regular centre or a central endpoint.
  Cartesian fields include vacuum and non-fluid states without singularity.
- CONVENTIONS: Signature (-+++), natural units, dOmega^2 the unit sphere;
  ds^2=-sigma^2 dT^2+(dr+sigma*zeta*dT)^2+r^2 dOmega^2.
  zeta=sqrt(2m/r)>0, sigma>0; m is Misner--Sharp mass, not scalar rest mass.
  Phi_A=partial_r phi_A; Pi_A=sigma^(-1)partial_T phi_A-zeta Phi_A.
  q and Q_C are collective U(1) charge, not an additional gravitational source.
- FREEDOM_LEDGER: Inherited action coefficients fixed to the units above;
  one initial-data choice with amplitude 0.02, centre 5, half-width 1 and
  initial rotational rate 1. No parameter fit, scan or pressure floor.
  Inner seed mass 1 is initial data, not a fixed later-time boundary mass.
- DEPENDENCIES: W3-73 generic scalar equations/geometry, W3-79 once-counted
  source convention, W3-80 full positive-quartic collective action. The
  below source/contract hashes are pinned and checked before execution.
- METHOD: Fourth-order radial differences and RK4 evolution of six matter
  fields plus m; solve the lapse constraint by cumulative Simpson quadrature
  at each stage. Solve only the initial radial mass constraint; do not
  project m back onto that constraint during evolution.
- OBSERVABLE_MAP: m, outer root r_H of r-2m=0, area 4pi r_H^2, charge in
  the computational exterior and through r=1, and local Hilbert stress.
  These are spherical candidate diagnostics, not a resolved optical image.
- FORWARD_MODEL: Frozen pulse -> full scalar/Einstein evolution -> marginal
  sphere/current diagnostics. No instrumental or observational comparison.
- DATA_ROLE: NO_OBSERVATIONAL_DATA; parameters are synthetic initial data.
- IDENTIFIABILITY: One evolution tests this candidate and state only. It
  does not determine foundation-node physics or a universal pressure map.
- BRANCHES: Canonical full scalar, future ingoing PG, positive m and lapse;
  no polar/irrotational-fluid requirement at vacuum zeros or radiative states.
- FALSIFIER: Failure to resolve the constraints and convergence invalidates
  this numerical result. Resolved horizon shrinkage inconsistent with the
  independent positive-null-flux law triggers a physical/equation audit.
  A numerical failure does not reject RefG or all initial conditions.
- VALIDITY_HEALTH: Finite fields; m>0; sigma>0; max characteristic Courant
  number <0.45; zeta(r=1)>1 throughout. Record curvature/stress diagnostics
  and stop as unresolved if the numerical domain ceases to be controlled.
  Bound the exterior boundary domain of dependence as specified below.
- CLOSURE_FLAGS: finite_evolution, constraints, current_balance,
  refinement, independent_time_check, exterior_boundary_check, vacuum_control
  and mutation_controls are computed. first_horizon_formation,
  full_collapse_endpoint, singularity_resolution, foundation_pressure_map,
  observational_pass and intuitive_files_changed remain false.
- FILES: This contract and w3_83_charged_pulse_accretion.py only.

## Initial data and the unchanged full action

V=.5*(phi_1^2+phi_2^2)+.25*(phi_1^2+phi_2^2)^2,
V_,A=(1+phi_1^2+phi_2^2)*phi_A.
This is the W3-80 action in Cartesian components; it replaces its effective
fluid description and is never counted beside that same fluid as a new source.

Let x=r-5 and b(x)=exp(1-1/(1-x^2)) for |x|<1, zero otherwise.
Initially phi_1=.02*b, phi_2=0, Phi_1=dphi_1/dr, Phi_2=0,
Pi_1=Phi_1+phi_1/r, Pi_2=phi_1. These are prescribed smooth Cauchy data,
not a stationary condensate or an exact isolated oscillon profile.
Set m(1)=1 and integrate m_r=4pi r^2(rho+zeta*S) to r=14 using
DOP853 with rtol=1e-12, atol=1e-14 and max_step=0.01, evaluated on each
evolution grid. The pulse vanishes for r<=4 and r>=6. Normalize sigma(14)=1.

## Production evolution and independent balances

rho=.5*sum(Pi_A^2+Phi_A^2)+V,
S=sum(Pi_A*Phi_A), p_r=.5*sum(Pi_A^2+Phi_A^2)-V,
p_T=.5*sum(Pi_A^2-Phi_A^2)-V.

phi_A,T=sigma*(Pi_A+zeta*Phi_A),
Phi_A,T=partial_r[sigma*(Pi_A+zeta*Phi_A)],
Pi_A,T=r^(-2)*partial_r[sigma*r^2*(Phi_A+zeta*Pi_A)]-sigma*V_,A,
m_T=4pi*sigma*r^2*sum[(Pi_A+zeta*Phi_A)*(zeta*Pi_A+Phi_A)],
partial_r ln sigma=-4pi*r*S/zeta.

The independently monitored constraints are Phi_A-partial_r phi_A and
m_r-4pi*r^2*(rho+zeta*S). Also reconstruct m by a radial integral from
its evolved inner value and compare with the freely evolved mass profile.
Do not replace this check by an accumulator of the same m_T RK stages.

q=phi_1*Pi_2-phi_2*Pi_1, s=phi_1*Phi_2-phi_2*Phi_1,
Q_domain=4pi*integral_1^14 r^2*q dr,
F_Q=4pi*sigma*r^2*(zeta*q+s).
Check Q_domain(T)+integral_0^T(F_Q(1)-F_Q(14))dT=Q_domain(0) using
independent spatial/time Simpson quadratures on actual output states.
Also compare m at fixed radii with the separately quadrature-integrated
energy flux. Charge can have either local sign; do not clamp it.

At a smooth outer root r_H-2m=0, D_H=1-2m_r>0, use the independent law
dot(r_H)=2*m_T|H/D_H with m_T|H=4pi*sigma*r_H^2*sum(Pi_A+Phi_A)^2.
Compare its integrated trajectory to the roots of evolved m. All roots
must be recorded before selecting the outermost. Track whether the pulse
crosses the marginal sphere and inner excision; those are different surfaces.

## Frozen numerical protocol and budgets

1. Uniform h={0.04,0.02,0.01} (N={326,651,1301}), dt=0.1*h, RK4;
   shorten steps only to land on each output T=j/100, j=0,...,400.
   D_r uses centred fourth-order five-point differences in the interior
   and matching fourth-order five-point one-sided stencils at the first/
   last two points. No filtering, clipping or constraint projection.
   Cumulative Simpson is used for the lapse. Inner stencils are outflow;
   no reflected or injected inner matter boundary value is prescribed.
   Outer matter fields stay zero and outer m stays at its initial value.
2. Time crosscheck: h=0.02 with dt=0.05*h, all other choices unchanged.
   Boundary crosscheck: r_out=18, h=0.02, dt=0.002; identical physical
   initial data on the shared region and sigma normalized in vacuum.
3. Store the sampled states only in memory. Compute diagnostics on the
   full annulus, reporting derivative norms also with the first/last
   four grid points excluded. Those excluded points remain evolved and
   are included in the charge integrals and boundary-flux accounting.
4. For each output time, define the radial constraint L2 relative residual
   using max(||m_r||_2,||4pi r^2(rho+zeta*S)||_2,1e-8) as denominator;
   use the analogous max(||Phi||_2,||D_r phi||_2,1e-8) for the auxiliary
   constraint. Fine-grid maximum interior residuals must be <0.005 and
   <0.002 respectively. Radially reconstructed mass must agree within
   0.001 of the initial pulse excess mass (m_outer-M_seed).
5. Charge balance maximum error <0.0002*Q_initial. Independent fixed-radius
   mass-flux balance maximum error <0.0002*(m_outer-M_seed). Integrated
   horizon-flux trajectory error <0.0002*r_H(initial). D_H must remain
   positive for the outer smooth branch on which that diagnostic is used.
6. Compare horizon radius, m(1), Q_domain/Q_initial, and total captured
   charge/Q_initial at common output times. Medium/fine differences must
   be <0.001 on scales {initial horizon radius, initial pulse excess mass,
   1,1}. Each error must decrease by at least a factor 2 from coarse/medium
   to medium/fine, unless already below 1e-7 on that scale. Interior mass
   constraint maxima must improve by at least factor 2 at each refinement,
   unless below 1e-7. Time crosscheck and outer-boundary changes in those
   diagnostics must be <0.0002 on the same scales.
7. Require accumulated maximum characteristic travel in the exterior
   region r>=6 over T<=4 to be less than the initial distance 8 between
   pulse support and r_out=14. Also
   inspect outermost two radial units for negligible stress (<1e-10 times
   the initial peak); compare the enlarged-domain run. This is a sampled
   numerical boundary check, not a rigorous continuum causality certificate.
8. Vacuum control A=0: the same production RHS and an evolution on h=0.04
   preserve phi=Pi=Phi=0, m=1, sigma=1 and r_H=2 to 1e-11. At least four
   negative controls must feed altered expressions to actual production
   identities: missing quartic potential force, reversed mass flux,
   wrong charge-flux sign and misnormalized mass source. They must fail
   the same evaluators used for the baseline, not simply flip flags.

PASS requires all listed numerical, provenance, finite-value and independent
checks. Failure is reported with the actual residual and remains unresolved;
no hidden threshold relaxation, amplitude search or replacement physical model
is allowed. A coding mistake can be corrected against the frozen equations.
Any scientific or numerical-protocol amendment is explicit before rerunning.

The outcome is reported separately: resolved accretion/horizon growth if its
increase exceeds the measured refinement error by at least tenfold; otherwise
resolved small/no change, or unresolved if numerical tests fail. Neither
accretion nor horizon growth is inserted into the PASS conditions.

## Provenance and scope

SHA-256, paths relative to the RefG workspace:

- CODES.md: 27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41
- RefG/work 3/Strong_Field/W3-73_Coupled_Horizon_Regular_Einstein_Complex_Scalar/w3_73_coupled_horizon_regular_einstein_complex_scalar.py: 47f2c97b64544f124cc2a5cb8d04825188664493cb5d770b6c3faf4ce2d5d7ca
- RefG/work 3/Strong_Field/W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction_contract.md: 7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa
- RefG/work 3/Strong_Field/W3-80_Resonant_Constitutive_Candidate/w3_80_neutral_resonant_condensate_contract.md: 27e359b9980df14a287ca89cc38a895eb5015a732154d7a055fd7666b418d841

Report own source/contract hashes and Python/NumPy/SciPy versions. The main
result concerns finite accretion in a specific candidate, not the full
formation/interior history, geodesic completeness or singularity removal.

Methodological precedent for horizon-crossing scalar evolution in these
coordinates: J. Ziprick and G. Kunstatter, *Spherically Symmetric Black Hole
Formation in Painleve--Gullstrand Coordinates*,
https://arxiv.org/abs/0812.0993 (2008; Phys. Rev. D 79, 101503, 2009).
That paper uses a massless scalar; its physical model is not substituted
for the retained W3-80 massive quartic field.

## Explicit numerical amendment v1.1, before amended execution

The first complete v1.0 execution reached T=4 on all six runs. Its actual
aggregate result was UNRESOLVED, with two failing gates: refinement and a
single smooth outer-horizon trajectory. The fine-grid mass constraint was
0.00381233, auxiliary constraint 0.00020192, radial mass reconstruction
9.11e-6, charge balance 5.03e-6 and fixed-radius mass-flux balance 5.995e-5;
these passed the unchanged budgets. Time, boundary, vacuum and controls
also passed. Medium/fine maxima were r_H 0.00812460, m_inner 0.00221642,
Q_domain 0.000435949 and captured charge 0.000432076 on their registered
scales. The mass error decreases with refinement but exceeded 0.001.
The v1.0 verifier source SHA-256 was
af9e26509a0957625f961e744fb95f94c2feebd74478df7946d61af1929a1b44.

All-root records and an independent implementation found creation and
annihilation of marginal-surface pairs. Selecting the outermost root then
produces jumps. A global smooth-radius integral and a pointwise sup norm
across shifted discontinuities are inappropriate diagnostics for that
topology. The following numerical changes resolve these identified issues;
they do not change the action, pulse, domain, endpoint or physical outcome.

1. Extend the spatial ladder by h=0.005, N=2601, dt=0.0005. Retain every
   original run and report its diagnostics. The primary refinement triple
   is now h={0.02,0.01,0.005}. All field, constraint, mass reconstruction,
   charge, mass-flux, time, boundary, vacuum, finite-domain and numerical
   tolerance budgets remain exactly those of v1.0. Output times remain
   T=j/100. This is a resolution increase, not a relaxed tolerance.
2. Resolve every observed pair creation/annihilation by solving
   H(T,r)=r-2m(T,r)=0 and partial_r H(T,r)=0 in each recorded root-count
   transition bracket. Use a cubic interpolant of the stored mass in time
   and radius. Seed the radius with the disappearing/appearing unmatched
   pair, determined by minimal-distance matching to the persistent roots.
   The nonlinear root must remain inside the time bracket and radial
   domain, with both dimensionless residuals below 1e-8. Report all events
   and their creation/annihilation labels, not only a selected pair.
3. Compare event counts/order and corresponding event times/radii across
   the primary refinement triple. Normalize time by 4 and radius by the
   initial horizon radius 2. Each medium/fine difference must be <0.001,
   with at least factor-2 improvement unless already below 1e-7. For the
   ordinary pointwise r_H comparison, exclude only the fixed +/-0.02
   neighborhoods of the union of these events; report this exclusion
   explicitly. The field/mass/charge comparisons remain over ALL times.
   No transition is omitted from the separate event comparison.
4. Validate the independent horizon null-flux identity at EVERY sampled
   root using the derivative of the stored mass history, not a divided
   speed of the outermost envelope. Obtain m_T by a quintic interpolating
   spline in time, then cubic interpolation in radius. At T indices 2
   through 398 compare it with 4pi*sigma*r_H^2*sum(Pi_A+Phi_A)^2.
   Normalize the maximum discrepancy by the larger of the maximum
   absolute source rate on these roots and initial pulse mass/4. The
   fine-grid error must be <0.0002. This finite output-time derivative
   is a numerical crosscheck, not an interval-certified derivative bound.
5. Retain the independent integrated horizon-speed check on the fixed
   terminal interval 2<=T<=4, requiring one smooth outer root and D_H>0
   throughout that interval. Initialize the integral with r_H(2), and
   keep the original tolerance 0.0002*r_H(0). The full earlier topology
   is covered by the event and all-root flux tests above, rather than
   being spliced into this smooth trajectory.

The amended aggregate requires all unchanged physical/numerical checks,
the finer-grid convergence, every event comparison, all-root flux and the
terminal smooth-branch integral. Preserve the v1.0 failed-gate summary in
the emitted JSON. No further refinement or diagnostic amendment is implicit;
if v1.1 fails, report the named unresolved test with its actual error.
