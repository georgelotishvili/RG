# W3-86: One localized excitation and reciprocal node-link feedback

## Decision and stopping rule

Use the UNCHANGED W84 finite graph Hamiltonian to decide how one localized
phase excitation modifies initially unperturbed links, and how that response
changes the subsequent phase/charge motion. Initial link-opening acceleration
is already known from W84; the new test is the finite reciprocal response.
No imposed rarefaction profile, trapping boundary, damping, pressure law,
metric, or extra interaction is allowed. Stop after this one initial-value
problem, the fixed controls below, and its physical classification.
No parameter scan, alternative model, longer-time extension or black-hole
calculation follows automatically.

Only this contract and w3_86_localized_node_link_feedback.py may be created.
Print finite JSON to stdout. No result files, plots, caches, manuscript or
idea edits, version changes, commits or publication.

## Frozen claim contract

- CLAIM_ID: W3_86_LOCALIZED_RECIPROCAL_NODE_LINK_FEEDBACK.
- CLAIM: The W84 Hamiltonian gives a numerically resolved finite evolution
  of the specified localized excitation. Its local link dilation, mechanical
  work, phase/charge redistribution and difference from a frozen-link
  diagnostic are determined with independently checked conservation and
  refinement. The physical response is classified, not required to be
  localized, self-trapping, slower, monotonic or stable.
- TYPE / MODEL_VERSION: FINITE_NUMERICAL_EVIDENCE_IN_EXISTING_NEW_GRAPH_HYPOTHESIS,
  W3-86-v1.0. This is a continuation of W84's candidate, not a microscopic
  derivation of RefG, an identified W58 oscillon, or a spacetime solution.
- ASSUMPTIONS / DOMAIN: Periodic one-dimensional label graph, N=48,
  0<=t<=8 in the inherited Hamiltonian time. Real theta,n,q,P; n is rotor
  action, not node count. Positive C=I=B=K0=d0=kappa=nbar=1, as in W84.
  Geometric bond readout d=exp(q); no three-dimensional embedding.
- INITIAL_DATA: centre c=N//2, theta_c=alpha=pi/6, all other theta=0;
  all n=1, q=P=0. Thus total rotor action=N, H0=2(1-cos alpha)=2-sqrt(3).
  The two initial nonzero phase differences have opposite signs.
  This is one discrete localized pulse, not a stationary particle profile.
- FREEDOM_LEDGER: Hamiltonian and all six positive coefficients unchanged
  from W84. N=48 and alpha=pi/6 reuse its graph size and primary phase scale;
  localization is the new synthetic initial condition. T=8 and numerical
  schedules below are frozen before any trajectory preview. No data fit.
- DEPENDENCIES: W84 contract and production coupling/forces/velocities/energy
  functions, hash-pinned below; import without invoking W84 main.
  Reuse does not import old PASS labels or continuum/Einstein conclusions.
- METHOD: Velocity Verlet for the full reciprocal system. Compare the same
  excitation on fixed q=P=0 links as a CONTROL Hamiltonian with those
  coordinates held fixed, not as the W84 solution. Independent DOP853 uses
  separately written RHS and energy formulas.
- CONVENTIONS / OBSERVABLE_MAP: delta_i=theta_(i+1)-theta_i, rightward
  charge flux=-J_i. Report label-distance spreading, bond d/d0, and rotor
  phase/action. Label RMS width is not a photon velocity or relativistic
  signal front. "Rarefaction" here means larger candidate bond spacing.
- FORWARD_MODEL / DATA_ROLE: Synthetic initial-value problem only;
  no observations, instrument response, inference or observational PASS.
- VALIDITY_HEALTH: Finite state/energy, n>0, finite positive d. For the
  conserved H0, positivity gives |n_i-1|,|q_i|,|P_i|<=sqrt(2H0)<1.
  This inherited finite-graph bound is not singularity resolution.
  Report instantaneous mixed stiffness only as a local diagnostic:
  no asymptotic or full nonstationary stability claim follows from its sign.
- BRANCHES: One fixed excitation, its frozen-link control and the same
  excitation on a wider N=96 ring. Outcomes of this finite experiment
  never reject all node models or all RefG.
- IDENTIFIABILITY / BENCHMARK: Resolve reciprocal feedback through actual
  link work plus full-vs-frozen phase/charge state difference. A positive
  initial q acceleration alone is insufficient. Frozen links remove the
  chosen feedback while retaining the same initial phase excitation.
- PASS_CONDITION / ERROR_BOUND: All numerical/algebraic gates below.
  Physical effect presence or sign is separate from software PASS.
- FAIL_CONDITION / FALSIFIER: Failed residual, balance, resolution, boundary
  or independent-integration check leaves this experiment UNRESOLVED.
  Resolved absence of the specified feedback is a valid negative physical
  result. Do not adjust initial data, duration, parameters or budgets to
  turn a failure into a preferred response.
- CROSSCHECK: Independent energy-gradient force check; off-shell local
  flux identity; mechanical-work integral; separately coded adaptive
  integration and N=96 boundary sensitivity. Shared premise is W84 H.
- CLOSURE_FLAGS: Compute provenance, force_and_flux_checks, finite_domain,
  energy_charge_balance, link_work_balance, timestep_refinement,
  independent_integrator, boundary_control and mutation_controls.
  Keep oscillon_identified, microscopic_RefG_law_derived, Einstein_source_derived,
  horizon_formed, singularity_resolved, asymptotic_stability,
  observational_pass, active_theory_changed and intuitive_files_changed false.
- PROVENANCE / FILES: Pin this contract before execution; report its hash,
  source hash, dependency hashes, protected-file hashes and library versions.
  Exactly two files in the new package.

## Inherited equations and independently observable exchange

H=sum [(n-1)^2/2 + P^2/2 + q^2/2 + K(q)(1-cos delta)],
K=exp[-q-(exp(q)-1)], K'=-(1+exp(q))K.

theta_dot=n-1; q_dot=P;
J_i=K_i sin(delta_i);
n_dot_i=J_i-J_(i-1);
P_dot_i=-q_i-K'_i(1-cos delta_i).

For the initial pulse, the two adjacent links have
q_ddot=2(1-cos alpha)>0. This identity is a regression, not the new result.

Split positive energy into:
E_phase=sum [(n-1)^2/2+K(1-cos delta)];
E_link=sum [(P^2+q^2)/2].
The actual instantaneous transfer into link mechanics is
Wdot_link=-sum P K'(1-cos delta).
Check E_link(t)-E_link(0)=integral Wdot_link dt, independently of total-H drift.

Assign half of each adjacent bond energy to each node:
e_phase_i=(n_i-1)^2/2+(V_i+V_(i-1))/2,
e_link_i=(L_i+L_(i-1))/2.
Then e_dot_i+F_i-F_(i-1)=0 with
F_i=-J_i[(n_i-1)+(n_(i+1)-1)]/2.
Neither E_link nor retained elastic energy is an oscillon.

## Fixed runs and numerical gates

Output common states at t=j/50, j=0,...,400. No filtering, wrapping,
recentring phase, energy projection, clipping, artificial damping or floors.

1. Full N48 Verlet at dt={0.004,0.002,0.001}; N48 frozen-link control at
   dt={0.002,0.001}; full N96 at dt=0.001. Time steps divide output spacing.
   Use the same central excitation and align N96 centre to N48 centre
   without subtracting separate mean phases. N96 is a boundary control,
   not a continuum limit.
2. Independent full N48 DOP853: rtol=1e-11, atol=1e-13, max_step=0.02,
   same outputs; separately coded force, velocity and energy formulas.
   Independently test the frozen-link control with the same method/budgets.
3. On deterministic nonuniform diagnostic data independent of trajectories,
   compare production forces with centred differences of H at h=1e-6.
   Max normalized residual <2e-7, normalizer=max(1,max|force|).
   Direct off-shell local flux and total charge residual <1e-12.
   Initial energy/action/adjacent force checks <1e-12.
4. Every Verlet step: finite state, n>0, finite d>0, energy-bound ratio
   max(|n-1|,|q|,|P|)/sqrt(2H0)<=1.0001. On every required run,
   max|H-H0|/H0<2e-5 and max|sum n-N|/N<1e-11.
5. Accumulate mechanical work by quadratic cumulative Simpson quadrature
   on actual full-run states at every integration step, diagnostic only.
   Complete two-step panels use dt*(f0+4*f1+f2)/3. An odd endpoint inside
   a panel uses dt*(5*f0+8*f1-f2)/12 added to the preceding even prefix,
   using the next stored point only after evolution. This covers all output
   prefixes without altering the dynamics. Max output residual
   |Delta E_link-W|/H0<2e-5. No energy difference manufactures Wdot.
6. All-state maximum absolute differences, normalized by alpha, use fixed
   gauge and ALL outputs/components. Full medium/fine error <2e-5 and
   <=0.4 coarse/medium unless medium/fine <1e-9. Frozen medium/fine <2e-5.
   Full and frozen fine-Verlet/DOP853 error <2e-5.
7. Compare N48 with centred N96 block at all outputs/components, /alpha:
   error <1e-6. Max N48 energy fraction at labels |i-c|>=20 <1e-6.
   These check finite-period sensitivity, not an exact finite-speed theorem.

Minimal genuine mutations on the same off-shell evaluators:
reverse phase current; omit link-opening force; use K(0) for the phase
current while retaining moving links; reverse the reported energy-flux sign.
Each must fail at least one baseline force or local energy/charge gate.
No rerun of a different physical theory is hidden in a mutation control.

## Predeclared physical classification

Report time series of E_phase/H0, E_link/H0, total and phase-only central
fractions (|i-c|<=2), phase/total label RMS widths, max/min d, minimum
instantaneous mixed stiffness, and the final full-vs-frozen state difference.
Use energy-weighted label distance from the fixed centre, not a fitted centre.

Let e_state be the largest alpha-normalized discrepancy among full and
frozen medium/fine, both fine/DOP853 and N48/N96 comparisons.
Resolved phase/charge backreaction means max_t,i |full-frozen|/alpha on
(theta,n) exceeds 10*max(e_state,1e-8).
Resolved dilation means max(d-1)>10*max(e_state,1e-8).
Resolved mechanical exchange means max(E_link/H0)>10*max(e_work,1e-8),
where e_work includes measured work residual and energy-balance errors.

Report these separately; only their joint occurrence supports "resolved
local reciprocal dilation feedback in this candidate."
For endpoint RMS comparisons use ten times the maximum observed
medium/fine, DOP853 and N48/N96 error of that same metric.
Classify phase spreading as narrower, wider, or unresolved relative to
frozen links. This is a finite packet-width comparison, not wavefront speed.

Use central total-energy fraction at T=8 with its corresponding error:
below 0.5 by >10 errors = majority redistributed out of central five labels;
above 0.5 by >10 errors = majority retained during this finite interval;
otherwise undecided. Report central phase/link fractions separately.
Report maximum and endpoint dilation; no permanent deficit or future
attractor is inferred. A local stiffness sign change is recorded, not promoted
to a complete time-dependent instability verdict.

Stop with this classification even if it is dispersion, contraction,
unresolved feedback or a failed numerical gate.

## Source pins and protected files

All paths are relative to C:/Users/george/Desktop/fizikis statiebi/RefG.
- CODES.md: 27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41
- RefG/work 3/Strong_Field/W3-84_Minimal_Node_Link_Candidate/w3_84_node_link_contract.md: ff1b94280a533e6aba4109465de7afcd2b5c7019c5292cb78c1040982c47d1dd
- RefG/work 3/Strong_Field/W3-84_Minimal_Node_Link_Candidate/w3_84_node_link.py: acd70be11d4734b5b208fa5b7166475166c48ee5f090640a05e19dfa081c3916
- intuitive/idea.txt: a73a06e1ed5b75298fae1bf22c88418e175b6628b12fa08a9e9c3992da59b48e
- intuitive/RefG_GE.md: 7c28f8848ae5ac441efae05e5a551973f37cca711202a0865e007793e282acd1
- intuitive/RefG_EN.tex: 6e69d616229688d885320d9b26b8c4637c563ae47f8da006feee8548d6ad910e
- intuitive/Dictionary.txt: f6e12b67f38e49bb547d37e6c92375a2ee5b2f596ed481a866cbc490be32ed0b

## Pre-production numerical clarification

The original contract hash was
9511a8148200f534c14aaef9df6fceeab7fc80e3c2c8842b39851a787bfaa6dc.
Before production code/execution and before the contract author received
the independent trajectory outcome, the Simpson endpoint convention was
specified above: dt=0.004
has odd interval counts at alternate outputs. This clarification changes
neither physics, run schedules, output times nor acceptance budgets.

The independent DOP853 run used the unchanged physics and completed
separately. The clarification hash 3097f369f82ecba9d21884014d3ee5b963d0b37b31d7f7401369442e3e1b47f3
was recorded before its outcome reached the contract author. This final
chronology sentence changes provenance wording only, not the protocol.
