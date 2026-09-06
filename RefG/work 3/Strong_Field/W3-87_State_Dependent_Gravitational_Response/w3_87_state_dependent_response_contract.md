# W3-87: State-dependent gravitational response -- action-first test

## Decision, provenance and stopping rule

Test one constitutive extension of W54: let its gravitational stiffness depend
on the EXISTING conserved collective density. Derive the induced current,
stress and connection equations before reducing symmetry. Use one homogeneous
contracting cell to determine whether the new term changes focusing and what
asymptotic response a regular continuation would require. Stop at that decision.
No fitted function, extra fluid, target black-hole metric, parameter search,
collapse simulation or subsequent package is authorized by this contract.

The new operator is an explicit CANDIDATE, not an extraction of a previously
hidden W54 term. W54 selected constant coefficients and excluded this coupling.
W84/W86 motivate reciprocal response but do not identify their graph variables
with this density or derive this coefficient. No microscopic F is selected here.
The identities and asymptotic thresholds below were derived by hand and checked
by two independent reviewers BEFORE writing/running this verifier; this is
reproducible verification of known analytic targets, not a blind prediction.

Create exactly this contract and w3_87_state_dependent_response.py in this
directory. Print finite JSON to stdout. No result files, caches, changes to
intuitive/idea files, earlier packages, versions, Git or publication.

## Claim contract

- CLAIM_ID / TYPE / VERSION: W3_87_STATE_DEPENDENT_RESPONSE;
  EXACT_VARIATIONAL_IDENTITIES_AND_CONDITIONAL_DYNAMICAL_FILTER; v1.0.
- CLAIM: The stated F(n)T action has a nonseparable density--geometry
  interaction. Its current and density-induced stress obey one consistent
  exchange identity. A lapse-preserving homogeneous variation supplies an
  explicit correction to focusing and distinguishes finite curvature,
  comoving proper time and radial-null affine continuation.
- ASSUMPTIONS / CONVENTIONS: Four dimensions, signature (-+++), c0=1,
  K=1/(16 pi G)>0, oriented nondegenerate coframe, flat metric-compatible
  inertial connection. T means the W54 TEGR scalar, not temperature or trace.
  Zero separate vacuum slot in the diagnostic. The selected future current
  has n>0, rho(n)>0, F(n)>0, sufficiently smooth on the tested domain.
- DOMAIN / FREEDOM_LEDGER: F and rho remain universal symbolic constitutive
  functions. No new scalar is treated as independent of the existing current.
  No identification n=P_F, n=node count, or F=p is made. The homogeneous cell
  has flat spatial slices, unit comoving coordinate volume, a,N,j>0. It is
  a symmetry-reduced diagnostic, not a black-hole interior model.
- DEPENDENCIES: W54 action and density definition, W67 once-only source rule;
  W79's minimal two-sector coupling and W84/W86's graph are context only.
  W54's full mode/PPN proof and W79's fluid health are NOT inherited for F'.
- METHOD: Product rule; density variation at fixed vector-density current;
  invariant fluid projection; restricted flat-spin variation; lapse/current/
  scale Euler--Lagrange equations; differentiated constraint; exact power
  asymptotics and geodesic integrals. No numerical differential solver.
- PASS_CONDITION / RESIDUAL / ERROR_BOUND: All registered algebraic residuals
  simplify to exact zero; all actual wrong-formula controls have nonzero
  residuals. Exact rational local-frame checks supplement general derivations.
  No floating tolerance, fit, empirical calibration or observational PASS.
- FAIL_CONDITION / FALSIFIER: Nonzero required residual invalidates that
  identity. Identically trivial connection variation on arbitrary states is
  incompatible with nonconstant F. Positive finite F,rho exclude a finite-n
  bounce of this flat cell. Neither exclusion rejects all RefG continuations.
- VALIDITY_HEALTH: Nondegenerate metric and positive F are necessary domains.
  The phase-as-clock branch additionally needs mu_eff>0. Frozen-geometry
  susceptibility is not the full coupled characteristic matrix. The general
  connection/constraint sector is recorded, not declared healthy from FLRW.
- BRANCHES: F=1 recovers the retained homogeneous Einstein/current system;
  other positive constants renormalize K. The contracting branch has H<0.
  No division by H is used at a putative bounce. The exact exponential
  contracting patch is a counterexample to equating proper and affine time.
- OBSERVABLE_MAP: a is the operational metric scale, d tau=N dt, n is charge
  per proper volume; these are not the foundation scale or coordinate p.
  Metric curvature and null affine length refer to this physical-metric
  candidate with the declared current coupling. General operational
  equivalence under field/units transformations is not asserted or excluded.
- FORWARD_MODEL / DATA_ROLE / BENCHMARK: N/A to observations; compare exact
  candidate variation with the F=1 action. No selected function has been
  confronted with existing weak-field observations.
- IDENTIFIABILITY: F' enters a mixed density/torsion derivative and cannot
  be absorbed into rho(n) alone when T varies independently. This does not
  identify F microphysically or prove uniqueness under all field changes.
- CROSSCHECK: Inverse-metric and coframe density variations; generic lapse
  EL versus differentiated Hamiltonian constraint; curvature built from
  the FLRW connection versus the standard expression; proper-time versus
  separately derived null-geodesic affine integral. Independent agent audit.
- CLOSURE_FLAGS: Calculate provenance, density_variation, weighted_identity,
  current_stress_exchange, connection_variation, lapse_preserving_dynamics,
  curvature_and_time_filter, constant_coefficient_recovery, mutation_controls.
  Keep microscopic_F_derived, generic_4d_health, weak_field_observational_pass,
  spherical_collapse_solved, regular_black_hole, global_completion,
  singularity_resolved, active_theory_changed, intuitive_files_changed false.
- PROVENANCE / FILES: Hash-pin this contract before verification; hash this
  verifier, relevant source contracts and protected files at runtime. Print
  the SymPy/Python versions. The two authorized files are the complete package.

## 1. Candidate action and full variational accounting

Let e=sqrt(-g), J^mu a vector density, and

    n=sqrt(-g_mu_nu J^mu J^nu)/e,   u^mu=J^mu/(en).
    S=-K integral e F(n) T + integral [J^mu theta_,mu - e rho(n)].

At fixed J and at fixed metric, respectively,

    delta n=(n/2)(g_mu_nu+u_mu u_nu) delta g^(mu nu),
    partial n/partial J^mu=-u_mu/e.

Equivalently, fixed J gives delta n=-n(e_A^mu+u_A u^mu) delta e^A_mu.
Vary the phase and current before identifying any density with a lapse:

    partial_mu J^mu=0,
    theta_,mu + mu_eff u_mu=0,
    mu_eff=rho'(n)+b,    b=K T F'(n).

The mixed derivative partial mu_eff/partial T=K F' is the discriminating
interaction. Positivity of F alone does not guarantee positive mu_eff.

Define G^F by varying -K e F T while temporarily holding F independent:
delta S_grav=K integral e G^F_mu_nu delta g^(mu nu), plus its flat-spin
equation. G^1 is the Einstein tensor. Restoring the composite F(n) gives

    2K G^F_mu_nu = T^rho_mu_nu + DeltaT_mu_nu,
    T^rho_mu_nu = n rho' u_mu u_nu + (n rho'-rho) g_mu_nu,
    DeltaT_mu_nu = n b (g_mu_nu+u_mu u_nu).

DeltaT has zero rest-energy contraction and isotropic pressure n b. It is
the density chain-rule term, not the whole geometrical correction G^F-G.
Varying composite F already includes it: adding it again double counts.

Let C=div(nu), C_nu=theta_,nu+mu_eff u_nu. The fluid identity is

    div(T^rho+DeltaT)_nu
      =mu_eff u_nu C + n u^alpha(d C)_(alpha nu) + b partial_nu n.

On both current equations, this is K T partial_nu F. The weighted gravity
Ward identity has the same right side on its flat-spin equation. Old fluid
stress alone is not separately conserved: its exchange is
div(T^rho)_nu=-n[D_nu b+b a_nu], with D the orthogonal derivative.
The verifier checks this projection algebra; it does not purport to calculate
all 16 general tetrad equations or their Hamiltonian constraint algebra.

## 2. Weighted TEGR identity and the connection equation

W54 gives R=-T+2 div(T^mu). The product rule gives exactly

    -e F T=e F R+2e T^mu partial_mu F-2 partial_mu(e F T^mu).

Thus simply substituting F R loses a bulk derivative interaction.
The last term is a boundary only under the usual compact-variation conditions.
Restricted flat-spin variation delta omega=D lambda yields, up to an
irrelevant nonzero overall factor,

    D_nu[e e_[A^nu e_B]^mu partial_mu F]=0.

The current density is spin-independent, so no extra F-chain term enters
this equation. It is equivalent to the antisymmetric coframe equation.
It is identically empty for constant F and vanishes by symmetry for the
Cartesian FLRW pair. An off-shell witness e^A_mu=diag(1,1,B(x),1), omega=0,
n=n(t), gives the 01 equation -B'(x) dF/dt /2. Therefore preserving TEGR's
IDENTICALLY trivial spin variation for arbitrary configurations forces F'=0.
A nontrivial connection equation is not itself a ghost or extra-mode proof.

## 3. One homogeneous contraction filter

The Cartesian coframe is diag(N,a,a,a), omega=0, J=(j,0,0,0), n=j/a^3.
Calculate T directly from this coframe: T=6H^2, H=adot/(Na).
The current density is independent of N. Reduce only after the full
variational structure above has been recorded:

    L=-6K a F(j/a^3) adot^2/N - N a^3 rho(j/a^3) + j thetadot.

Keep N,a,j,theta independent in variation. Then use jdot=0 and proper time:

    6K F H^2=rho,
    dtheta/dtau=rho'+6K H^2 F',
    dn/dtau=-3Hn,
    2F dH/dtau+3(F-nF')H^2=-(n rho'-rho)/(2K).

The differentiated constraint independently gives

    dH/dtau=-n[rho'-rho F'/F]/(4KF).

With gamma=n rho'/rho and beta=n F'/F on this branch,
dH/dtau/H^2=-(3/2)(gamma-beta). The new term can change null focusing:
R_mu_nu k^mu k^nu=-2(dH/dtau)(k^tau)^2. Bare positive enthalpy does not fix
its sign here. The function F remains to be derived from foundation physics.
For F,rho finite and strictly positive, H=0 is incompatible with the lapse
constraint. This excludes a finite-density flat bounce in this candidate
domain, not throats, curvature-supported bounces or other black-hole interiors.

## 4. Exact asymptotic discrimination (no constitutive fit)

Only for this contracting cell, test strict power asymptotics
rho~rho0(n/n0)^gamma, F~F0(n/n0)^beta, with positive constants and gamma>0.
Require the corresponding differentiated asymptotics; arbitrary logarithmic
corrections at thresholds are outside this stated claim. No value of beta
is selected as a physical theory. Write delta=beta-gamma.

    H^2 ~ const n^(-delta),
    R=6(dotH+2H^2),
    Kretschmann=12[(dotH+H^2)^2+H^4].

Consequently bounded scalar curvature invariants and infinite comoving
future proper time require delta>=0 within this family. The time integrals are

    Delta tau ~ integral^infinity n^(-1+delta/2) dn,
    Delta lambda_null ~ integral^infinity n^(-4/3+delta/2) dn.

The affine relation follows independently from the radial null geodesic:
a^2 dx/dlambda=constant and dtau/dlambda=constant/a, so dlambda is
proportional to a d tau. Radial-null affine length is infinite for delta>=2/3.
The stricter threshold matters: the contracting de Sitter metric patch
a=exp(-h tau) has bounded curvature, infinite comoving time, but finite
future null affine length 1/h with that normalization. An incomplete PATCH
may admit extension; neither this example nor a convergent integral proves
that no extension exists. Also n and rho grow without bound at the asymptote;
no finite-density regular centre or physical completion is established here.

## 5. Verification and explicit negative controls

Verify density variations in all independent inverse-metric, coframe and
current directions in an exact rational boosted local frame. Check weighted
conversion, exchange projections, connection witness and its FLRW regression.
Derive all four reduced EL equations with the lapse present, crosscheck the
constraint derivative, and compute FLRW curvature directly from its connection.
Check the two time-integral exponents and the finite-affine exponential case.

Actual mutated calculations must fail unchanged identities: omit the weighted
bulk gradient term; hold F independent of density in the phase equation; omit
the induced pressure; freeze F during scale variation; incorrectly include
N in n=j/a^3; equate null affine time with comoving proper time.
These checks validate this bounded calculation. They do not certify all
constraints, causal speeds, ghosts, observational agreement or a black hole.

## References and source boundary

- W54, sections 2 and 4: retained constant-coefficient action and TEGR identity.
- W67: action-first response and once-only source/conservation accounting.
- Brown, Action functionals for relativistic perfect fluids (1993),
  https://arxiv.org/abs/gr-qc/9304026 -- densitized-current variational framework.
- Hohmann, Jarv and Ualikhanova, PRD 97,104011 (2018),
  https://arxiv.org/abs/1801.05786 -- flat-spin and antisymmetric equations.
- Hohmann and Pfeifer, PRD 98,064003 (2018),
  https://arxiv.org/abs/1801.06536 -- derivative scalar--torsion coupling.

The last two works use scalar-torsion frameworks; replacing their independent
scalar by the composite current density requires the explicit chain-rule
variation above. Their results are not a ready-made RefG microscopic law.
