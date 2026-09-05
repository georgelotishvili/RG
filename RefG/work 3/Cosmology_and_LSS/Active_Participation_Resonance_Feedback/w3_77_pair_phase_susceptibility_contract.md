# W3-77: Pair phase susceptibility and pressure projection

## Working frame

One decision: what feedback does the W3-76 exchange law produce when the
receiving core follows the already computed W3-58 charge-frequency branch,
and does this justify a self-settling resonant pair or a pressure closure?

The new physical input is the action-derived frequency response to charge,
combined with the W3-76 interaction force. Replacing that response by the
positive inertia of a rigid tuning fork would select a different model.
This stage derives the leading phase/charge feedback and the same
interaction's dilation stress, then checks the regime in which they can be
used. It stops at this decision, without selecting damping, a new medium,
an equation of state, or a long-time trajectory.

Allowed files: this contract and one no-write verifier in this topic.
Upstream mathematics, intuitive files, release metadata and versions stay
unchanged.

## Claim contract

- **CLAIM_ID:** W3_77_PAIR_PHASE_SUSCEPTIBILITY_PRESSURE_PROJECTION.
- **CLAIM:** In the dilute, adiabatic collective-coordinate reduction of
  the retained W3-58/W3-76 ordinary scalar, the phase/charge response is
  fixed by the isolated branch curvature E''(q)=1/q'(Omega). On its
  verified negative-slope branch, the equal-phase instantaneous subsystem
  is hyperbolic and the opposite-phase subsystem is elliptic. The pair
  interaction also fixes a phase-dependent virial stress. These identities,
  together with the recoil and scalar-threshold diagnostics, delimit the
  use of pair exchange as a collective relaxation mechanism.
- **TYPE:** CONDITIONAL_LEADING_ORDER_MODULATION_AND_STRESS_DIAGNOSTIC.
- **MODEL_VERSION:** W3-77-v1.0; the action, branch, kernel and tests below
  are fixed before execution. The reduction is a stated approximation,
  not an exact two-core solution or a microscopic foundation law.
- **ASSUMPTIONS:** W3-58 canonical one-complex-field action, regular
  nodeless branch near a=1/4, Omega=4/5, E_Omega=Omega q_Omega and
  q_Omega<0; W3-76 distant-core kernel; local fixed Minkowski coframe;
  small velocities and small charge imbalance; adiabatic following of
  the isolated branch; leading order in exponentially small overlap.
  Both ordinary cores belong to the same field. Neutral theta_C stays
  distinct.
- **DOMAIN:** Leading dilute-pair modulation and instantaneous subsystem
  coefficients. Separation D is a mechanical coordinate, not an externally
  imposed permanent constraint. Classification at one D does not establish
  a stationary full pair, a long-time frequency, or full PDE instability.
- **CONVENTIONS:** Use W3-76 t=m tau, x=m r and full-angle dimensionless
  q=lambda Q, Ehat=lambda E/m. Below E denotes Ehat, q is full-angle
  charge, s=dOmega/dq, and V is a dimensionless averaging-cell volume.
  W3-58 radial charge q_r and energy E_r obey q=4 pi q_r, E=4 pi E_r.
  z=(q_L-q_R)/2, Delta=theta_R-theta_L, k=sqrt(1-Omega^2)>0.
- **FREEDOM_LEDGER:** No new coefficient or function. Inherited a,Omega
  select the existing branch; m,lambda restore units. D,Delta and cell
  volume V are state/geometry data. K(D)=4 pi C^2 exp(-kD)/D is inherited,
  with C determined from the radial profile rather than fitted.
- **DEPENDENCIES:** Hash-pinned W3-58 contract/solver, W3-76
  contract/verifier, W3-54 source action, and W3-75 pressure distinction.
- **METHOD:** Use the first law along the solitary-wave family, perform
  the fixed-charge Legendre cancellation of overlap energy, derive
  the relative canonical one-form and Hamilton equations, linearize,
  differentiate under spatial dilation, and evaluate recoil/sidebands.
- **PASS_CONDITION:** All exact identities, dependency checks and
  negative controls pass; numerical first-law and charge-slope checks meet
  the budgets below. Each physical diagnostic reports its actual outcome.
  A failed frozen-separation validity criterion is a scope result, not a
  numerical error or an instruction to tune parameters.
- **FAIL_CONDITION:** Nonzero exact residual, incorrect charge normalization,
  wrong current sign, failed numerical budget, changed inherited action,
  or use of an unregistered fitted restoring/damping coefficient.
- **FALSIFIER:** At leading order in the declared reduction, a different
  canonical response or dilation derivative falsifies the displayed
  identities. A positive converged q_Omega would invalidate the stated
  negative-slope classification at the benchmark. These are scoped tests,
  not exclusion of the full Einstein-scalar theory or of many-body states.
- **RESIDUAL:** Exact zero for canonical reduction, Hamilton equations,
  linear eigenvalue polynomial, phase-space divergence, Legendre
  cancellation, dilation stress and recoil identities.
- **ERROR_BOUND:** Algebra is exact within the leading reduction.
  Omitted overlap and nonadiabatic corrections are not bounded for the
  full two-core PDE at finite D. Numerical witness uses X=80 and profile
  tolerances 1e-7 and 3e-8. Independently recompute the W3-58 sensitivity
  and its frozen five-point stencils h=0.01,0.005. Require all slopes
  negative; relative sensitivity/stencil disagreement <2e-2; relative
  first-law residual |E_Omega-Omega q_Omega|/|Omega q_Omega| <2e-3;
  relative change in q_Omega,E and C between the two profile runs <2e-4.
- **VALIDITY_HEALTH:** No new fundamental kinetic operator is introduced.
  Negative E'' is the constrained solitary-family response, not a
  negative fundamental scalar kinetic energy. The total canonical flow
  preserves phase-space volume. The isolated-core stability result remains
  distinct from exchange stability.
- **BRANCHES:** Delta=0 and Delta=pi; K=0 decoupling as a control; the
  opposite sign s>0 as a mathematical comparison, not the retained branch.
  Resting finite-D equal/opposite-phase pairs have nonzero scalar force.
- **OBSERVABLE_MAP:** The calculation yields an instantaneous phase
  growth/libration scale, charge-exchange response, scalar interaction
  stress and recoil diagnostic. Physical pressure is m^4/lambda times
  the dimensionless pressure. No particle identity is assigned.
- **FORWARD_MODEL / DATA_ROLE:** N/A for observational inference; no
  measurement, likelihood or empirical fit. Existing profiles are
  theoretical numerical inputs, not experimental validation.
- **IDENTIFIABILITY:** The two retained actions do not equate pair
  interaction stress with foundation readout P_F. Phase correlations and
  spatial distribution would be needed to average a population; no such
  distribution is selected here.
- **BENCHMARK:** Reuse a=1/4,Omega=4/5 and D={20,24,28}. Determine C by
  the W3-76 Green-source integral with 16001 radial Simpson points.
  Use q_Omega from the sensitivity equation, with full angular factor.
  Report sigma=sqrt(-2K/q_Omega), the two frozen sideband squared wave
  numbers (Omega +/- sigma)^2-1 and the recoil index k L_recoil.
  The diagnostic frozen-separation requirement is k L_recoil<=0.1;
  its failure forbids interpreting sigma as a long-time pair frequency.
- **CLOSURE_FLAGS:** Derived flags cover the canonical/first-law
  response, leading phase classification, dilation stress, recoil and
  threshold diagnostics, numerical crosschecks and mutation controls.
  Full_PDE_pair_stability_proved, asymptotically_attracting_lock_derived,
  collective_P_F_feedback_derived, damping_kernel_derived,
  electromagnetic_alpha_derived, observational_pass and
  intuitive_files_changed remain false. Frozen_separation_valid_on_phase_time
  is calculated from the registered recoil criterion.
- **CROSSCHECK:** Derive the relative canonical equations both from the
  one-form and the original two charge/phase pairs; compare sensitivity
  with finite differences; check E_Omega=Omega q_Omega independently;
  compare pressure from dilation with the pair-force virial; verify
  eigenvalues by the characteristic polynomial. Shared premises are the
  same isolated branch and dilute reduction, not independent evidence
  for the underlying ontology.
- **NEGATIVE_CONTROLS:** Reject the reversed relative symplectic sign,
  a missing factor of two in the imbalance response, omitted 4 pi in the
  charge susceptibility, reversed interaction force/pressure sign,
  inserted friction in the closed Hamilton flow, and treating the
  unadjusted overlap energy as fixed-total-charge energy.
- **PROVENANCE:** Contract fixed before verifier execution. Dependency,
  contract and source hashes, Python/library versions, residuals and
  numerical diagnostics are printed as finite JSON to stdout.
- **FILES:** This contract and w3_77_pair_phase_susceptibility.py.
  Neither program output files nor publication changes are produced.

## 1. The inherited response and the correct charge ensemble

Along the isolated branch,

    dE/dOmega=Omega dq/dOmega,       dE/dq=Omega,
    s=dOmega/dq=1/q_Omega,           q_Omega<0.

For equal-frequency overlapping cores, with S=integral f_L f_R d^3x,
the cross-charge is q_cross=2 Omega S cos(Delta). W3-76 gives

    E_cross-Omega q_cross=-K cos(Delta).

At fixed actual total charge the isolated contributions shift by
delta q_L+delta q_R=-q_cross. Their leading energy shift cancels
Omega q_cross. The leading interaction in fixed-charge variables is

    H_int=-K cos(Delta).

This is a Legendre conversion, not identification of raw superposition
energy with interaction energy. Smooth finite-q_Omega branch response
makes the charge-coordinate and symplectic overlap corrections vanish
as separation grows. Finite-D corrections are not quantified here.

## 2. Instantaneous relative phase/charge dynamics

To the retained order, around q_L=q_R=q_0,

    q_L dtheta_L+q_R dtheta_R=q_total dtheta_mean-z dDelta,
    H_phase=constant+s z^2-K(D) cos(Delta),
    dot z=partial_Delta H_phase=K(D) sin(Delta),
    dot Delta=-partial_z H_phase=-2s z.

The Jacobian at z=0, Delta=Delta_0 in {0,pi} satisfies

    tr J=0,       eigenvalue^2=-2s K(D) cos(Delta_0).

For s<0, Delta=0 is hyperbolic and Delta=pi is elliptic in this
instantaneous phase/charge subsystem. Define sigma^2=-2sK>0.
The closed Hamiltonian flow has zero divergence; an elliptic point is
conservative libration, not an asymptotically attracting state.
This volume argument applies to this finite-dimensional closed reduction;
it does not exclude phase mixing or radiative relaxation of subsystems
in the full field theory.

## 3. The interaction stress and translation

For two identical slow cores the leading relative mechanical sector is

    H_mech=P_D^2/E_0-K(D) cos(Delta),    E_0=E(q_0)>0,
    dot D=2P_D/E_0,
    dot P_D=K'(D) cos(Delta).

The once-counted scalar pair virial in a cell of volume V is

    P_int=D K'(D) cos(Delta)/(3V).

The same expression follows from minus the derivative of H_int with
respect to V under D proportional to V^(1/3), at fixed charges and
phases. K'<0: equal phase gives attraction and negative interaction
stress; opposite phase gives repulsion and positive interaction stress.
Kinetic and self contributions are not included in P_int. All these
contributions belong to the existing T_O, not an additional stress tensor.

A resting finite-D pair would require sin(Delta)=0 and cos(Delta)=0
simultaneously in this leading scalar model. Thus the two phase
configurations are not full static-pair equilibria. This statement excludes
neither additional Einstein attraction nor force balance in a population.
Neither sign of P_int is a criterion for cosmological pressure relaxation:
P_F is the separate operational foundation readout retained in W3-75.

## 4. Two checks against an uncontrolled synchronization claim

Starting from rest, the instantaneous translation acceleration has magnitude

    |ddot D|=2[-K'(D)]/E_0.

Using only its initial Taylor coefficient over the local scale 1/sigma,

    L_recoil=|ddot D|/(2 sigma^2)
            =|q_Omega|(k+1/D)/(2E_0).

This is a diagnostic, not a computed displacement after 1/sigma.
Because K is exponentially sensitive to separation, the control parameter
is k L_recoil, not only L_recoil/D. A large value requires evolving
translation before interpreting a frozen phase frequency over long times.

The vacuum scalar dispersion is omega_wave^2=k_wave^2+1.
The formal frozen-coefficient sidebands Omega +/- sigma have

    k_wave_plus^2=(Omega+sigma)^2-1,
    k_wave_minus^2=(Omega-sigma)^2-1.

Negative values close these monochromatic linear massive-scalar channels.
They do not exclude radiation from transients, higher harmonics, orbital
motion or the massless Einstein tensor modes already in W3-54. A
retarded damping kernel for the actual coupled pair is not computed here.

## Decision and stopping boundary

This stage determines the intrinsic exchange feedback and its mechanical
stress, and tests the frozen-separation shortcut. It preserves the exact
W3-76 initial-current result. It does not replace common-medium dynamics
by a positive-inertia phase oscillator or an inserted friction constant.

The remaining physical object is a controlled many-body or retarded
medium response, with energy accounting and its relation to P_F derived
from the retained action. No arbitrary local pressure formula or
damping coefficient is selected in this package.

## Sources and dependency pins

- W3-58 contract:
  ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db
- W3-58 solver:
  b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57
- W3-76 contract:
  e10781a73470220065c664196efe0c361dbfb1c6c2404864e895d6ad2380bd02
- W3-76 verifier:
  c3ad4b140c7b89a3e6d587b6b46480db1da0bb94b6b5307a32237df876285a6f
- W3-54 contract:
  6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879
- W3-75 contract:
  31a1e6bd28b6698e64b790fd4692aba6616af5613c3919f322a790c7296d9f4a

R. Battye and P. Sutcliffe, Q-ball Dynamics,
https://arxiv.org/abs/hep-th/0003252, Section 3: phase-dependent charge
transfer and limitations of fixed-profile, fixed-position reductions.
This prior work motivates the scope checks, not the numerical coefficient
or an assumption of permanent synchronization.

