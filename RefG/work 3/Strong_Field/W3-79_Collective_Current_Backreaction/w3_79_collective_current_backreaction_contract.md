# W3-79: Collective-current backreaction in the strong-field system

## Working decision

Complete the local spherical strong-field source system by retaining the
ordinary oscillon field and the organized collective phase current together.
W3-73 supplies the coupled geometry/ordinary-field equations; W3-54 supplies
the collective action; W3-75 already admits their additive matter action.
The new result removes W3-73's zero-localized-collective-source truncation.
It supplies the collective evolution, its gravitating stress, the sound
characteristics and the joint horizon balances.

One bounded package contains this contract and
w3_79_collective_current_backreaction.py. The verifier writes finite JSON
to stdout and no files. Stop after exact closure, independent checks and
the registered nonvacuum regression. Existing theory, intuitive manuscripts,
W3-78, release metadata and Git history are unchanged.

## Frozen claim contract

- CLAIM_ID: W3_79_COLLECTIVE_CURRENT_BACKREACTION.
- CLAIM: The retained additive Einstein/ordinary-scalar/collective-current
  action yields a source-complete local spherical constrained evolution
  system, regular through a future marginal sphere. Collective primitive
  variables are locally invertible on the physical branch; the positive
  sound-speed subsystem is symmetric hyperbolic with its acoustic cone
  inside the common metric null cone. The two separately conserved
  currents and both Hilbert stresses enter the common geometry once.
- TYPE: CONDITIONAL_EXACT_LOCAL_COUPLED_SYSTEM_WITH_EXACT_REGRESSION.
- MODEL_VERSION: W3-79-v1.0; frozen before execution.
- ASSUMPTIONS: The selected W3-54 continuum action and W3-58 ordinary
  canonical complex scalar; one metric; W3-73's Lambda=0 local branch;
  smooth spherical fields on a simply connected annulus; a supplied
  universal isentropic irrotational rho_C(n); n>0, mu=rho_C'(n)>0,
  rho_C>0 and 0<c_s^2=n rho_C''/rho_C'<=1 for the hyperbolic claim.
  Smooth rho_C=mu_0 n dust is a separately identified degenerate regression.
- DOMAIN: r>0, sigma>0, zeta>0, |v|<1; smooth pre-shock/pre-caustic states
  in the selected continuum domain. No expansion in zeta or weak compactness
  is used. A future outer marginal sphere has zeta=1 and
  D_H=1-2G m_r>0. The centre, global endpoint and degenerate D_H=0 branch
  are outside this local result.
- CONVENTIONS: c0=1; metric signature (-+++); future normal
  e_0=sigma^(-1) partial_T-zeta partial_r, e_1=partial_r;
  ds^2=-sigma^2 dT^2+(dr+sigma zeta dT)^2+r^2 dOmega_2^2.
  S=T_hat0hat1 is minus the ADM radial momentum density.
  rho_C and P_C are rest-frame collective energy density and Hilbert
  pressure. P_F is the separate foundation-pressure readout.
- FREEDOM_LEDGER: No new action, coupling, species parameter, cutoff or
  pressure switch. rho_C is the inherited unselected universal function,
  not fitted by this work. Initial scalar/current profiles, an admissible
  mass boundary value and lapse normalization remain initial/gauge data.
  The cold regression parameters below define a mathematical test case,
  not a selected physical high-density equation of state.
- DEPENDENCIES: Hash-pin W3-54 and W3-58 contracts; W3-73 contract/solver;
  W3-75 contract; CODES.md. The current contract and source hashes and
  package versions are reported. Old printed PASS values are not substituted
  for re-derived equations.
- METHOD: Vary the current action before PG reduction; derive its Hilbert
  source and conservative phase/current equations; combine with the
  ordinary field and independently evaluated metric projections. Derive
  primitive Jacobian, characteristics, symmetrizer, source conservation,
  mass/current/horizon balances and exact nonvacuum regressions.
- PASS_CONDITION: Every required symbolic residual is exactly zero;
  dependency pins and production configuration pass; every registered
  mutation fails its relevant unchanged identity; all registered LTB
  numerical evaluations are finite and meet the fixed budgets below.
  This closes the local EOS-parameterized system, not EOS selection.
- FAIL_CONDITION: Wrong action variation, source count/sign, primitive
  Jacobian, sound cone, conservation, Einstein projection, horizon flux,
  branch classification or registered regression budget.
- FALSIFIER: A nonzero exact residual or an admissible state violating a
  claimed sign/causal identity falsifies that claim. Solver/numerical
  failure is inconclusive for the associated diagnostic, not a new physics
  exclusion.
- RESIDUAL: Exact zero for action/current/source variation, reduced
  current and phase equations, metric constraints/evolution, conservation,
  Jacobian/characteristic identities, source/horizon balances and
  analytic regression equations.
- ERROR_BOUND: Algebra exact in the selected continuum/action and smooth
  local domain. LTB root/evaluation budgets are numerical crosschecks,
  not interval certification or numerical evolution of an oscillon.
- VALIDITY_HEALTH: mu>0 and causal c_s^2; regular local primitive inversion.
  Symmetric hyperbolicity is claimed for the collective principal block
  at c_s^2>0, not global well-posedness of the full constrained system.
  At c_s=0 a repeated generally defective Eulerian block is recorded.
  Ordinary scalar characteristics remain metric-null. No extra metric.
- BRANCHES: Strict positive-sound-speed branch; stiff endpoint c_s=1;
  degenerate smooth dust regression; finite future outer marginal sphere;
  trapped annulus. Primitive inversion is local on the image of physical
  states, not asserted for arbitrary unphysical conservative data.
- OBSERVABLE_MAP: Local stresses, two current densities/fluxes, invariant
  areal radius, Misner--Sharp mass, marginal-surface radius/area and
  sound/null propagation speeds in the declared frame.
- FORWARD_MODEL: Compatible local initial data -> coupled constrained
  evolution system and its physical fluxes. No detector or likelihood.
- DATA_ROLE: N/A: no observations, particle masses or fitting data.
- IDENTIFIABILITY: This derives the evolution interface for supplied
  rho_C; it does not identify its microscopic form, a strong-field P_F
  readout, or a relation between the independent ordinary/collective charges.
- BENCHMARK: W3-73 at zero collective source; homogeneous current
  dilution; metric-null/stiff and smooth dust limits; the exact LTB
  annulus below, independently checked in comoving and PG coordinates.
- CROSSCHECK: Action variation vs projected fluid stress/conservation;
  conservative-flux Jacobian vs local Lorentz sound speeds; direct metric
  Einstein projections vs mass constraints; LTB comoving shell solution
  vs PG matter and metric residuals. Shared assumptions are the same action,
  spherical symmetry and the explicitly declared test EOS.
- CLOSURE_FLAGS: Exact collective action/source/evolution, one-counted
  total source, local primitive inversion, positive-sound-speed
  symmetrizer, horizon characteristic/flux balance and exact nonvacuum
  regression are separate. high_density_EOS_selected,
  foundation_pressure_feedback_derived, full_nonstatic_material_scale_map,
  collective_origin_from_ordinary_modes, nonlinear_oscillon_collapse_solved,
  regular_centre_derived, singularity_resolution, observational_pass and
  intuitive_files_changed remain false.
- PROVENANCE: Contract/source/dependency SHA-256, Python/SymPy versions,
  exact residual outcomes, diagnostic inputs/results and finite JSON stdout.
- FILES: This contract and one no-write verifier in this folder.

## 1. Action, current variables and the single source ledger

The retained local action is

    S = integral sqrt(-g) R/(16 pi G)
        - integral sqrt(-g)[sum_A (partial phi_A)^2/2+V(chi)]
        + integral [J_C^mu partial_mu theta_C-sqrt(-g)rho_C(n)],
    chi^2=phi_1^2+phi_2^2,
    V=m_O^2 chi^2/2-lambda chi^4/4+g6 chi^6/6,
    n=sqrt(-g_mu_nu J_C^mu J_C^nu)/sqrt(-g).

The current and phase variations give

    partial_mu J_C^mu=0,
    partial_mu theta_C=-mu u_mu,
    mu=rho_C'(n),  P_C=n mu-rho_C,  w_C=n mu,
    T_C,mu,nu=w_C u_mu u_nu+P_C g_mu_nu.

Let u=gamma(e_0+v e_1), gamma=(1-v^2)^(-1/2), and define

    D=n gamma,  B=mu gamma v,  W=mu gamma.
    theta_C,T=sigma(W-zeta B),   theta_C,r=-B.

The two collective evolution equations are

    partial_T D + r^(-2) partial_r[sigma r^2 D(v-zeta)]=0,
    partial_T B + partial_r[sigma(W-zeta B)]=0.

The scalar fields obey the unchanged W3-73 equations

    partial_T phi_A=sigma(Pi_A+zeta Phi_A),
    partial_T Phi_A=partial_r[sigma(Pi_A+zeta Phi_A)],
    partial_T Pi_A=r^(-2)partial_r[sigma r^2(Phi_A+zeta Pi_A)]
                    -sigma V_,A.

Define rho_O=sum(Pi_A^2+Phi_A^2)/2+V,
S_O=sum(Pi_A Phi_A), p_rO=sum(Pi_A^2+Phi_A^2)/2-V.
The ordinary tangential pressure is
p_TO=sum(Pi_A^2-Phi_A^2)/2-V.

The common metric receives exactly

    rho=rho_O+w_C gamma^2-P_C,
    S=S_O-w_C gamma^2 v,
    p_r=p_rO+w_C gamma^2 v^2+P_C,
    p_T=p_TO+P_C.

The multiplicities of the Einstein operator, T_O and T_C are each one.
P_F, passive ruler factors and the phase currents themselves have zero
additional Hilbert-source multiplicity. The ordinary scalar is not also
included in rho_C as a duplicate coarse-grained copy.
Each sector obeys its own on-shell covariant conservation; their coupling
is through the common dynamical metric.

## 2. Coupled geometry, primitive recovery and characteristics

With total sources above, the retained Einstein equations read

    partial_r ln sigma=-4 pi G r S/zeta,
    partial_r zeta=4 pi G r(rho/zeta+S)-zeta/(2r),
    partial_T zeta=sigma zeta partial_r zeta-partial_r sigma
                   +sigma zeta^2/(2r)+4 pi G sigma r p_r.

For m=r zeta^2/(2G),

    m_r=4 pi r^2(rho+zeta S),
    m_T=4 pi sigma r^2[zeta(rho+p_r)+(1+zeta^2)S].

The collective part of m_T is
4 pi sigma r^2 w_C gamma^2(zeta-v)(1-zeta v).
No fixed background is imposed in this system.

The primitive map has Jacobian

    det partial(D,B)/partial(n,v)
       =mu gamma^4(1-c_s^2 v^2)>0,
    c_s^2=n mu'/mu.

The two acoustic coordinate speeds are

    lambda_plus/minus=sigma[(v+/-c_s)/(1+/-v c_s)-zeta].

For primitive variables (ln n, atanh v), a symmetric principal pair is

    A0=[[c_s^2,c_s^2 v],[c_s^2 v,1]],
    A1=[[c_s^2 v,c_s^2],[c_s^2,v]],
    A0 partial_T + sigma(A1-zeta A0) partial_r.

A0 is positive definite for c_s^2>0 on the physical branch.
Both sound speeds lie between sigma(-1-zeta) and sigma(1-zeta).
At c_s=0 the conservative-flux principal block is tested separately for
its repeated eigenvalue and generic defectiveness.

## 3. Two currents and the marginal-surface balances

Ordinary charge q_O=phi_1 Pi_2-phi_2 Pi_1 and
s_O=phi_1 Phi_2-phi_2 Phi_1 obey

    partial_T(r^2 q_O)-partial_r[sigma r^2(zeta q_O+s_O)]=0.

The collective current is j_C^T=D/sigma, j_C^r=D(v-zeta).
Its integral uses 4 pi r^2 D, independently of ordinary charge.
For either density q and coordinate radial current j^r,
the exterior moving-inner-boundary balance includes
+4 pi r_H^2[sigma j^r-q dot(r_H)] at that boundary.

At zeta=1 on D_H=1-2G m_r>0,

    m_T|H=4 pi sigma_H r_H^2[
        sum_A(Pi_A+Phi_A)^2+w_C gamma^2(1-v)^2],
    dot(r_H)=2G m_T|H/D_H,
    dot(area_H)=8 pi r_H dot(r_H).

The collective inward moving-surface flux has sign
D[(v-1)-dot(r_H)/sigma_H]<0.
Sound characteristics are nonpositive at the marginal sphere and strictly
inward at zeta>1. These are local future-outer balances.

## 4. Exact regression and frozen numerical checks

Use the marginally bound LTB dust annulus solely as a nonvacuum exact
test of the current, Einstein source and horizon balances:

    phi_A=Pi_A=Phi_A=0,  rho_C=mu_0 n,  mu_0>0,
    sigma=1, v=0, theta_C=mu_0 T,
    M(a)=M_b+b a,
    R(T,a)=[a^(3/2)-(3/2)sqrt(2G M(a))T]^(2/3),
    zeta=sqrt(2G M(a)/R),
    n=M'(a)/(4 pi mu_0 R^2 R_a).

Restrict to R>0 and R_a>0. Transform derivatives by

    partial_r=R_a^(-1)partial_a,
    partial_T|r=partial_T|a+(zeta/R_a)partial_a.

The regression must satisfy both collective equations, all independent
Einstein projections, both mass balances and ordinary zero-field equations.
The angular Einstein equation is included. At T=0 the outer horizon is

    a_H=2G M_b/(1-2G b),  D_H=1-2G b>0.

Also check the action's dust degeneracy and the zero-collective W3-73 limit.
This test makes no strong-field physical selection of the cold EOS.

Numerical crosscheck inputs are fixed to G=mu_0=1, M_b=1/2, b=1/20,
T={0,1/20,1/10}, a={3/4,1,5/4,3/2,2}. Require R>0, R_a>0, n>0
and finite quantities at these points. Locate one R=2GM root on
a in [3/4,2] at each T with absolute root tolerance 1e-12; require
normalized horizon residual below 1e-10 and D_H>0.
Independently compare the horizon radius derivative from the implicit
shell root to 2G m_T/D_H: exact identity plus finite numerical relative
error below 1e-9. No parameter or domain search is opened.
Numerical checks support the exact regression, not a time-evolution claim.

## 5. Verification and stopping rule

Check the symbolic identities directly, including covariant stress
conservation from phase/current equations and consistency of the total
mass balances. Recompute geometry rather than accepting a stored PASS.
Mutations rerun the corresponding production identities with:
(1) omitted T_C, (2) doubled T_C, (3) reversed collective momentum sign,
(4) reversed phase-flux sign, (5) omitted spherical r^2 current measure,
(6) Newtonian rather than relativistic acoustic speeds,
(7) misidentified P_F as an extra Hilbert pressure,
(8) omitted moving-surface charge term.
Each mutation must fail a designated unchanged action/conservation/geometry
identity. Merely setting a scope flag false is not a negative control.

The completed result is one source-complete, EOS-parameterized local
strong-field system. The inherited high-density constitutive function and
the nonstatic foundation-pressure/material-scale readout retain their
separate status. No zero-avoidance rule, regular centre, core rigidity or
global collapse endpoint is inferred from the action-level handoff.

## Primary methodological sources

J. D. Brown, Action functionals for relativistic perfect fluids (1993),
https://arxiv.org/abs/gr-qc/9304026, for the variational current framework.
P. D. Lasky and A. W. C. Lun, Spherically Symmetric Gravitational Collapse
of Perfect Fluids (2006), https://arxiv.org/abs/gr-qc/0611002, for the
spherical fluid/geometry setting.
J. Ziprick and G. Kunstatter (2008), https://arxiv.org/abs/0812.0993,
for horizon-crossing PG evolution methodology.
These references are methodological; the displayed identities and test
configuration are checked from the retained RefG actions.

