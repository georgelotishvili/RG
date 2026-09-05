# W3-76: Same-field resonant exchange between two localized cores

## Working frame

One decision: does the retained W3-58 scalar action already support
phase-dependent energy exchange between two localized excitations, without
adding an ordinary/collective phase potential or imposing identical phases?

The author's tuning-fork clarification selects medium-mediated resonant
response as the phenomenon to test. The new calculation evaluates the
existing action on two separated excitations of ONE ordinary complex field.
It supplies an explicit pair-transfer kernel, a necessary building block
for a population response. W3-75's separate collective-current sector is
retained; pair exchange and collective pressure relaxation are different
questions.

Allowed files: this contract and one no-write verifier in the existing
Active_Participation_Resonance_Feedback topic. Stop after current, energy,
stress, asymptotic kernel, numerical witness and independent checks.
Intuitive files, upstream results, publication metadata and versions stay
unchanged. No long-time simulation or additional interaction is selected.

## Claim contract

- **CLAIM_ID:** W3_76_SAME_FIELD_RESONANT_EXCHANGE.
- **CLAIM:** The canonical W3-58 ordinary scalar supplies a nonzero,
  conservative, relative-phase-dependent initial exchange of ordinary
  Noether charge and energy across the bisector of two identical separated
  cores. Its exact initial current flux and full sextic stress follow from
  the retained action. In the distant-core limit, current transfer and
  leading force share one profile-determined exponentially decaying kernel.
- **TYPE:** CONDITIONAL_EXACT_INITIAL_DATA_FLUX_WITH_ASYMPTOTIC_INTERACTION
  AND_NUMERICAL_WITNESS.
- **MODEL_VERSION:** W3-76-v1.0. One field, the W3-58 action, current signs,
  initial data, benchmark, tolerances and domain below are frozen before
  verification. An altered model or acceptance threshold requires an
  explicit amendment before rerunning its gate.
- **ASSUMPTIONS:** The W3-58 fixed regular Minkowski coframe, canonical
  complex scalar and sextic potential; a smooth positive nodeless radial
  localized profile in the W3-58 frequency window; one field containing
  both excitations; identical positive initial frequencies; sufficiently
  regular local evolution for the conservation identities.
- **DOMAIN:** Exact instantaneous flux at t=0 for the specified smooth
  finite-energy Cauchy data. A two-centre interpretation uses separations
  larger than the isolated core size. The Yukawa formula is a large-D
  asymptotic statement. The superposition is initial data, not an exact
  stationary two-core solution or a proven long-time collective trajectory.
- **CONVENTIONS:** Natural units; dimensionless t=m tau, x=m r,
  u=sqrt(lambda) chi exp(i theta_O)/m=sqrt(2 lambda) Psi_O/m.
  Signature (-+++). The dimensionless action has overall factor 1/lambda.
  Vhat(s)=s/2-s^2/4+a s^3/6 with s=|u|^2 and a>3/16.
  j^0=Im(u* u_t), j^i=-Im(u* partial_i u).
  Left half-space is x<0; Delta=theta_R-theta_L; D is centre separation.
  Positive F_L points from the left centre toward the right centre.
  Dimensionless spatial integrals use the full solid angle, without
  W3-58's factored-out 4 pi.
- **FREEDOM_LEDGER:** No new coupling, phase-restoring potential, mediator,
  damping rate or fitted constant. Inherited m, lambda, a and Omega;
  initial-data freedoms D and Delta. The exterior coefficient C is
  determined by the isolated profile, not independently selected.
- **DEPENDENCIES:** Hash-pinned W3-58 contract and solver supply the action
  and numerical profile; W3-50 and W3-54 contracts preserve the ordinary/
  collective distinction and common metric; W3-75 locates the remaining
  collective-response boundary. Pins appear below.
- **METHOD:** Evaluate the Noether current and Hilbert flux directly in
  complex and real components; integrate over the bisector; use the
  isolated radial stress identity to remove self stresses; derive the
  linear exterior kernel; recompute the W3-58 benchmark and compare
  independent radial and cylindrical surface integrals.
- **PASS_CONDITION:** All exact residuals, hash checks and registered
  negative controls pass. Numerical profile and flux checks meet the
  frozen budgets below; the nonzero exchange witness survives domain,
  tolerance and quadrature comparisons. All scope flags remain separate.
- **FAIL_CONDITION:** A sign, normalization, polynomial, conservation,
  dependency or exact residual fails; independent surface integrals fail
  their numerical budget; a hidden extra field or fitted coupling is used.
  Numerical nonconvergence is INCONCLUSIVE, not a rejection of all cores.
- **FALSIFIER:** Zero cross-current for all relative phases in the SAME
  nonzero-overlap field would falsify the exchange claim. A different
  sextic cross-stress or a disagreement of the leading kernel with the
  action's surface flux falsifies the displayed formula. Two independent
  noninteracting fields are a distinct negative control, not this model.
- **RESIDUAL:** Exact symbolic zero for current, energy flux, current
  antiderivative, full cross-stress, isolated stress cancellation, exterior
  integral and shared-kernel generator identities. Numerical discrepancies
  are reported independently.
- **ERROR_BOUND:** Exact initial flux identities have zero algebraic error.
  Large-D corrections are bounded at the surface as in Section 3.
  Numerical witness: profile weighted radial equation residual <2e-5;
  positive nontrivial monotone profile; energy/charge/radius and transfer
  kernel relative variation <2e-4 across domain/tolerance runs; independent
  flux integration relative discrepancy <2e-4; quadrature refinement change
  <2e-4; Green coefficient versus exterior estimate at r=16 discrepancy
  <2e-3; current kernel and leading force discrepancy <5e-3 at the registered
  separations. Force discrepancies and isolated-plane stress residuals
  are normalized by the positive phase-independent coefficient -K'(D),
  including Delta=pi/2 where the leading phase-dependent force is zero.
  The normalized isolated-plane stress integral is <2e-4.
  These are floating-point checks, not interval-certified error bounds.
- **VALIDITY_HEALTH:** The canonical principal part and full-field U(1)
  conservation are inherited unchanged. Smooth finite-energy initial data
  admit the usual local semilinear-wave evolution. Single-core stability
  remains the W3-58 result; pair stability and global evolution are not
  implied. Energy transferred into one region is lost by the other.
- **BRANCHES:** Every Delta is kept; Delta=0, pi has zero initial charge
  transfer; Delta=pi/2 has nonzero exchange. The leading quadratic force
  vanishes at pi/2, while the exact nonlinear force generally does not.
- **OBSERVABLE_MAP:** Physical ordinary charge Q=q/lambda, energy
  E=m Ehat/lambda, force F=m^2 Fhat/lambda and dQ/dtau=(m/lambda) dq/dt.
  These are field-theory readouts, without particle-species assignments.
- **FORWARD_MODEL:** Existing action -> isolated profile -> two-core
  initial data -> bisector current, energy and stress. No cosmological
  pressure readout is substituted for a Hilbert component.
- **DATA_ROLE:** N/A: no observation, fit or archived-theory data.
- **IDENTIFIABILITY:** C and the pair kernel are fixed after the inherited
  (a,Omega) and units are fixed. Pair data do not determine a microscopic
  node interaction, P_F response, universal alpha or particle spectrum.
- **BENCHMARK:** Reuse a=1/4, Omega=4/5. Solve with the unchanged W3-58
  solver at (X,tol)=(60,1e-7),(80,1e-7),(80,3e-8).
  Use D={20,24,28}; Delta={0,pi/2,pi}; radial Simpson grids with
  {4001,8001} points. Independent cylindrical integration uses adaptive
  quadrature. Determine C from the source integral over [0,X] and
  cross-check r f(r) exp(k r) at r=16. No parameter is fitted.
- **CLOSURE_FLAGS:** Derived flags cover the exact initial pair current,
  initial energy balance, full sextic stress, isolated cancellation,
  large-D kernel, numerical nonzero-transfer witness, dependency and
  mutation checks. The flags long_time_synchronization_derived,
  pair_stability_proved, exact_rigid_two_core_solution,
  collective_pressure_feedback_derived, microscopic_node_coupling_derived,
  electromagnetic_alpha_derived, observational_pass and
  intuitive_files_changed remain false.
- **NEGATIVE_CONTROLS:** The same production residuals must reject a
  reversed current sign, a missing factor of two in the local cross-current,
  omitted cross-current (two independent fields), reversed raised-energy
  flux sign, a removed quartic cross term, a removed sextic cross term,
  reversed left boundary orientation and a wrong Yukawa decay exponent.
- **CROSSCHECK:** Complex current/stress versus real-component calculation;
  radial antiderivative versus cylindrical quadrature; full versus excess
  stress; Green-source coefficient versus exterior profile; independent
  human-readable algebra audit. Shared premises are the same scalar action
  and numerical isolated profile; the quadrature check is not an
  independent profile solver.
- **PROVENANCE:** Contract frozen before verifier execution. Python,
  SymPy, NumPy and SciPy versions and file hashes are printed to stdout.
  Runtime produces no files.
- **FILES:** This contract and w3_76_same_field_resonant_exchange.py.

## 1. Initial data and exact exchange

The radial equation and exterior exponent are

    f''+2 f'/r = k^2 f-f^3+a f^5,       k^2=1-Omega^2>0.

Place the centres at x=-b and x=+b, b=D/2. At t=0 set

    u=f_L+exp(i Delta) f_R,             u_t=i Omega u.

These are two excitations of one field. Their scalar sum is smooth even
where its polar phase is undefined. On x=0, r=sqrt(b^2+rho^2),

    u=f(r)[1+exp(i Delta)],
    u_x=(b/r) f'(r)[1-exp(i Delta)],
    j^x=2 (b/r) f f' sin(Delta),        T^{0x}=Omega j^x.

The surface measure is 2 pi rho d rho=2 pi r dr. Since f(infinity)=0,

    I_L_to_R = integral j^x dS = -pi D f(b)^2 sin(Delta),
    dq_L/dt = K_exact(D) sin(Delta),    dq_R/dt=-dq_L/dt,
    K_exact(D)=pi D f(D/2)^2>0,
    dEhat_L/dt=Omega dq_L/dt,           dEhat_R/dt=-dEhat_L/dt.

The integration uses integral f f' dr=-f(b)^2/2. At finite cutoff X,
include the explicit boundary term f(X)^2. Region charges contain the
overlap contribution; they are not separately conserved particle charges.
Conservation is exact for the full field. The energy-frequency identity
above is instantaneous, using the specified initial time derivative.

## 2. Exact initial stress

Let c=cos(Delta). Subtract the two isolated stresses before integrating:

    Delta T_xx =
      -c [f'^2+k^2 f^2]
      +f^4 [(1+c)^2-1/2]
      -a f^6 [(4/3)(1+c)^3-1/3].

The force on the left half-space is

    Fhat_L=-2 pi integral_b^infinity r Delta T_xx dr.

For one isolated core define

    p_r=f'^2/2-k^2 f^2/2+f^4/4-a f^6/6.

Its radial equation implies p_r'=-2 f'^2/r and

    r T_xx_self = d[(r^2-b^2) p_r/2]/dr.

Both boundary terms vanish on the infinite domain, so full and excess
stress give the same integrated force. This argument requires only the
isolated radial equation, not a stationary two-core ansatz.

## 3. Leading common kernel and its error boundary

For f(r)~C exp(-k r)/r,

    K(D)=4 pi C^2 exp(-k D)/D,
    dq_L/dt ~ K(D) sin(Delta),
    Fhat_L ~ -K'(D) cos(Delta)
           =4 pi C^2 exp(-k D)(k/D+1/D^2) cos(Delta).

The profile coefficient can be determined without fitting:

    C=(1/k) integral_0^infinity r sinh(k r)[f^3-a f^5] dr.

This follows from the regular radial Green function for
(-Laplacian+k^2)f=f^3-a f^5. The regular core, not a point source, fixes C.

Define I_j=integral_b^infinity r f^j dr. The explicit nonlinear force
remainder is bounded by

    |R_nl| <= 2 pi [(7/2) I_4+(31/3) a I_6].

There is a separate exterior-profile error. If on r>=b the relative
errors of f and f' against C exp(-kr)/r and its derivative are at most
epsilon, the quadratic-force error is at most
(2 epsilon+epsilon^2) times its positive quadratic force coefficient.
The same factor bounds the relative current-kernel error at b.
Numerical profile checks provide evidence at the registered benchmark,
not a rigorous bound for all r or all a,Omega.

The phase-dependent reduced generator

    G_int=-K(D) cos(theta_R-theta_L)

reproduces dq_L/dt=-partial G_int/partial theta_L and
Fhat_L=partial G_int/partial D. It denotes the leading phase/position
interaction generator (the leading excess of Ehat-Omega q
at fixed frequency); it is not the raw total energy of an unadjusted
superposition at fixed individual frequencies. A complete collective-
coordinate Hamiltonian and long-time phase evolution are outside the claim.

## 4. Interpretation and remaining physical bridge

This is a conservative ordinary-sector interaction already present in the
retained action. The stationary isolated core has zero outgoing flux;
the pair cross-current supplies a new, explicitly computed exchange
between regions. Uniform background rescaling and the response to a
second localized excitation are kept distinct. The latter can excite
corrections to the isolated profile; exact rigidity is not asserted.
The force here is the scalar contribution on a fixed metric, not the total
force including gravitational backreaction. At finite gravitational coupling,
an algebraically decaying gravitational force can dominate at large distance.

The massive scalar's sub-threshold exterior is evanescent. Its pair
kernel therefore decreases exponentially with separation. Propagating
vacuum scalar perturbations obey omega_wave^2=|k_wave|^2+1 in these units.
This channel alone does not supply the universal long-range network,
a photon sector, or cosmological pressure relaxation.

The ordinary current and neutral collective current remain distinct.
W3-75's missing physical map from resonant population response to the
collective action/P_F is unchanged. The concrete new result is the
existing-action pair kernel; no new theta_O-theta_C interaction is fitted.
The spatially and profile-dependent K(D) is not an identification of
the electromagnetic fine-structure constant.

## Sources and dependency pins

- W3-58 contract:
  ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db
- W3-58 solver:
  b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57
- W3-50 contract:
  c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635
- W3-54 contract:
  6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879
- W3-75 contract:
  31a1e6bd28b6698e64b790fd4692aba6616af5613c3919f322a790c7296d9f4a

Prior work on phase-dependent Q-ball interaction:
R. Battye and P. Sutcliffe, Q-ball Dynamics, Nuclear Physics B 590
(2000) 329-363, https://arxiv.org/abs/hep-th/0003252.
P. Bowcock, D. Foster and P. Sutcliffe, Q-balls, Integrability and Duality,
https://arxiv.org/abs/0809.3895 (one spatial dimension).
These are methodological and priority references, not substitutes for
the three-dimensional calculation here. The physical phenomenon is
established Q-ball dynamics; W3-76 checks its realization and coefficient
within the retained RefG core action.
