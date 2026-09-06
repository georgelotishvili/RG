# W3-80: Neutral resonant condensate constitutive candidate

## Working decision

Construct and test one new finite-density energy model that derives a collective equation of state and resonant propagation from the same action. The new physical input is a positive quartic self-interaction of a neutral complex order parameter. This is a classical continuum candidate, not a derived lattice of foundation nodes. Stop after its energy, source, propagation and rarefaction-domain decision; do not integrate a black hole or alter the active theory.

Allowed files: this frozen contract and one no-write verifier in this folder. Existing W3 results, intuitive documents, release metadata, and publication state remain unchanged.

## Claim contract

- **CLAIM_ID:** W3_80_NEUTRAL_RESONANT_CONDENSATE_CONSTITUTIVE_CANDIDATE.
- **CLAIM:** The new canonical neutral quartic action below has a unique homogeneous fixed-positive-charge energy minimum, an explicit stable causal barotropic leading-gradient reduction, and a two-mode linear spectrum whose low-frequency sound speed agrees with the thermodynamic derivative. Its pressure and infrared sound speed decrease with dilution, with a density-dependent hydrodynamic validity window.
- **TYPE:** EXACT_CLASSICAL_CANDIDATE_CONSTRUCTION_AND_LOCAL_LINEAR_TEST; leading-gradient matching is conditional, not an exact elimination in inhomogeneous spacetime.
- **MODEL_VERSION:** W3-80-v1.0; action, branch, numerical inputs, tolerances and controls are frozen before execution. This is a new candidate parent of the collective sector, not a modification of W54/W79 or automatic inheritance of their physical claims.
- **ASSUMPTIONS:** One existing operational metric; signature (-+++); zero temperature; classical field; m_C>0, lambda_C>0; independent neutral phase theta_C; positive future-timelike phase gradient on the coherent branch. Ordinary theta_O and its stress remain separate. No explicit ordinary/collective interaction, dissipation, quantum correction, photon coupling, lattice or vacuum offset is introduced.
- **DOMAIN:** Exact homogeneous condensate and local linear perturbations on a fixed Minkowski patch, mu>m_C, x=R_0^2>0, k>=0. Gravity enters the covariant source interface only. The full field current can leave the positive-timelike branch away from this domain. Curved-background slow-gradient matching additionally requires small amplitude derivatives/curvature relative to the local amplitude response scale; it is not certified by the homogeneous spectral test alone.
- **CONVENTIONS:** Set c0=hbar=1; Psi_C=R exp(i theta_C)/sqrt(2), R>=0; X=-g^{ab} theta_a theta_b; mu=sqrt(X)>0; u^a=-partial^a theta_C/mu. Define j^a=-R^2 partial^a theta_C so n=R^2 mu>0. P_C is Hilbert/thermodynamic pressure, distinct from foundation readout P_F. Define d=n^(-1/3) as a mean conserved-charge-volume length proxy; microscopic node identity and normalization are not inferred.
- **FREEDOM_LEDGER:** Two new universal candidate parameters m_C and lambda_C, neither inherited from the ordinary oscillon nor fitted. The positive quartic is the lowest nonlinear analytic U(1)-invariant potential term around R=0 under the chosen canonical-field restriction. Positive mass selects a dilute massive charge branch. Density/chemical potential and k are state/probe data. The fixed-charge normalization defines d; no exponent is selected to reproduce p, P_F, or a cosmological curve.
- **DEPENDENCIES:** CODES; W54 defines the target first-order collective sector and source accounting; W62 defines the cold comparison; W79 defines the local fluid/Einstein interface. Their contracts and the W79 verifier are hash-pinned below. No result-file PASS is inherited.
- **METHOD:** Vary the new covariant action; minimize its fixed-charge energy; compare pressure from volume work, Legendre transformation and Hilbert stress; expand the full amplitude/phase action to quadratic order; independently solve the real linear time-evolution matrix; compare exact dispersion with the leading-gradient action and derive an error bound. Test the static chemical-potential relation only to delimit pressure interpretation.
- **PASS_CONDITION:** All declared exact residuals vanish, the candidate branch satisfies energy/causality conditions, every numerical test meets its frozen budget, and every negative control is rejected by its unchanged production identity/validity condition. Derive rather than preset result booleans.
- **FAIL_CONDITION:** An action/source/current mismatch, nonunique fixed-charge minimum on the declared branch, an unstable local mode, incorrect source multiplicity, failed numerical budget, or unregistered parameter adjustment.
- **FALSIFIER:** A nonzero independently checked residual or instability on the declared classical branch invalidates the corresponding candidate claim. The candidate is not a universal explanation of RefG pressure unless an independent P_F/readout bridge passes; that bridge is outside this stage and stays open. A failure of this candidate does not reject every resonant-medium model.
- **RESIDUAL:** Exact symbolic zero for equations and matching identities; finite residuals reported separately for numerical crosschecks.
- **ERROR_BOUND:** Exact classical homogeneous algebra and linear spectrum. The sound approximation has the explicit bound in section 3. No nonlinear curved-background, quantum-loop, observational or full collapse error is calculated. Numerical budgets are specified below.
- **VALIDITY_HEALTH:** Bounded positive quartic energy, positive fixed-charge Hessian, nonnegative mode frequencies, positive low-energy temporal/spatial coefficients, 0<c_s^2<1/3, and metric-null full principal propagation. These are local matter tests, not absence of gravitational Jeans instability or a global nonlinear existence proof.
- **BRANCHES:** Selected R>0, mu>m_C coherent branch; vacuum R=0 is a separate endpoint, with singular polar coordinates but regular Cartesian fields; negative lambda is a rejection control; m_C=0 and finite-temperature states are outside the candidate.
- **OBSERVABLE_MAP:** Internal density n, pressure P_C, proper carrier frequency mu, and linear-mode frequencies are candidate local observables. The length d is a density proxy. Light propagation remains on the inherited metric; neither acoustic speed nor P_C is identified with its coordinate speed or P_F.
- **FORWARD_MODEL / DATA_ROLE:** N/A: no astronomical or laboratory data and no observational claim. The numerical states are preregistered synthetic checks of the classical model.
- **IDENTIFIABILITY:** The selected action determines rho_C(n) parametrically once m_C,lambda_C are specified. The study does not select these constants, identify real foundation nodes or identify this standard condensate construction uniquely with nature.
- **BENCHMARK:** Independent fixed-charge minimization, full real dynamical matrix, and the dilute cold limit. The construction belongs to established relativistic condensate/superfluid field theory; novelty is not claimed for those general formulas.
- **CLOSURE_FLAGS:** Start false; compute candidate action/EOS/source/spectrum/IR-bound/numerical checks from tests. Keep physical_foundation_nodes_identified, P_F_bridge_derived, all_signal_speeds_slow, ordinary_to_collective_origin_derived, exact_finite_density_CMB_dust, full_curved_gradient_control, strong_field_collapse_solved, singularity_resolved, observational_pass, active_theory_changed and intuitive_files_changed false.
- **CROSSCHECK:** Fixed-charge and grand-canonical derivations share only the declared action; metric variation is independent of the perfect-fluid identity; real 4x4 mode eigenvalues are independent of the closed-form dispersion; numerical thermodynamic derivatives use separate differences.
- **PROVENANCE:** Pin the contract and input hashes; report source hash and package versions; only finite JSON to stdout and progress to stderr; no output files, bytecode, plots or result caches.
- **FILES:** This contract and w3_80_neutral_resonant_condensate.py only.

## 1. New energy and fixed-charge equilibrium

The candidate collective action, replacing rather than supplementing the old effective S_C, is

    S_C,new = integral sqrt(-g) [
        - (partial R)^2/2 - R^2 (partial theta_C)^2/2
        - m_C^2 R^2/2 - lambda_C R^4/4 ].

The ordinary action and Einstein operator are unchanged comparison inputs. The full collective amplitude is a new propagating degree of freedom. At leading gradients, its elimination is to recover one effective collective stress, not two.

At fixed positive charge density n, write x=R^2>0:

    e(x;n)=n^2/(2x)+m_C^2 x/2+lambda_C x^2/4.

Stationarity, endpoint behavior and the positive Hessian are to establish the unique global minimum. Parametrize it by

    mu^2=m_C^2+lambda_C x,  n=mu x,
    rho_C=m_C^2 x+3 lambda_C x^2/4,
    P_C=lambda_C x^2/4,
    d rho_C/dn=mu,  rho_C+P_C=mu n.

Pressure must also follow by -partial E(Q,V)/partial V at fixed Q, using n=Q/V and the stationary amplitude (envelope theorem). In terms of the phase invariant,

    R_*^2=(X-m_C^2)/lambda_C,
    L_eff=P_C(X)=(X-m_C^2)^2/(4 lambda_C),  X>m_C^2.

Vary the full action before homogeneous substitution. Verify the phase current, amplitude equation, and all independent metric variations. Show the leading-gradient current and Hilbert tensor equal W54's one-current perfect-fluid source with this rho_C(n). The discarded amplitude-gradient stress is explicit; it vanishes on homogeneous states, not universally.

Dilute parameter eta=lambda_C x/m_C^2>0:

    rho_C/(m_C n)=(1+3 eta/4)/sqrt(1+eta),
    0 <= rho_C/(m_C n)-1 <= eta/4,
    P_C/rho_C=eta/(4+3 eta),
    c_s^2=eta/(2+3 eta).

This is a controlled cold limit, not exact dust at finite eta. Both P_C and c_s increase with n and hence decrease with d. Proper carrier cadence mu approaches m_C rather than zero.

## 2. Full local propagation

Set R=R_0+s, theta_C=mu t+pi/R_0. Derive the quadratic Lagrangian, including its mixing term:

    L2=1/2[s_dot^2-(grad s)^2+pi_dot^2-(grad pi)^2-h s^2]
        +2 mu s pi_dot,
    h=2 lambda_C x,
    B=2m_C^2+3lambda_C x=(h+4mu^2)/2.

For exp(-i omega t+i k.r), the determinant is

    (k^2+h-omega^2)(k^2-omega^2)-4mu^2 omega^2=0,
    omega_+-^2=k^2+B +- sqrt(B^2+4mu^2 k^2).

The gapped value is omega_+^2(0)=2B. The lower root is evaluated stably as

    omega_-^2=k^2(k^2+h)/(k^2+B+sqrt(B^2+4mu^2 k^2)).

Prove positive roots for k>0, the zero Goldstone mode at k=0, and the full Cartesian principal metric-null cone. The acoustic slope is c_s^2=lambda_C x/B and must equal dP_C/d rho_C. Expanding P_C(X) independently in the convention L2_eff=(K_time pi_theta_dot^2-K_space |grad pi_theta|^2)/2 gives K_time=(3mu^2-m_C^2)/lambda_C and K_space=(mu^2-m_C^2)/lambda_C, with their ratio c_s^2.

## 3. Dilution and the controlled sound window

For x>0,k>0 define S=sqrt(B^2+4mu^2 k^2). Verify

    omega_-^2-c_s^2 k^2 = 8mu^4 k^4/[B(S+B)^2],
    0 <= omega_-^2/(c_s^2 k^2)-1 <= k^2/h.

The sufficient linear sound condition is k^2/h small. A small k relative only to the finite gapped frequency is not sufficient during dilution.

At fixed k and x->0, the exact lower frequency tends to

    omega_-=sqrt(m_C^2+k^2)-m_C.

The vacuum limit and the hydrodynamic long-wavelength limit therefore have different scaling. At fixed positive eta, increasing k eventually leaves the acoustic approximation. These statements concern this candidate's internal mode, not photons or an oscillon's universal material scale.

For stationary, no-flux equilibrium the same current relation gives mu N=constant. Thus the resulting mechanical P_C increases as the lapse N decreases on the coherent branch. This sign must be reported alongside the separate open P_F bridge, preventing the new EOS from silently becoming a foundation-pressure deficit law.

## 4. Frozen numerical checks and negative controls

Numerical units m_C=lambda_C=1. Use eta in {1e-6,1e-3,1,100}. For each state:

1. Independently find the positive stationary x at fixed n using a scalar root of partial_x e, bracket [1e-12,1e3], absolute root tolerance 1e-18 and relative tolerance 4 machine eps. Require relative x agreement below 1e-8.
2. Compare dP/d rho from centered differences at x(1+-epsilon), epsilon in {1e-3,5e-4}, with the analytic c_s^2; relative disagreement below 2e-6 and second difference at least as accurate up to 1e-10 roundoff slack.
3. For k/sqrt(h) in {0.03,0.1}, compare positive frequencies from the real 4x4 time-evolution matrix on (s,pi,s_dot,pi_dot) with both exact branches. Require relative frequency disagreement below 1e-6 and real eigenvalue parts below 1e-10 times max(1,omega_+). Check the exact acoustic relative-error bound k^2/h with slack 1e-10. There are exactly eight state/wavenumber cases.
4. Report energy, pressure, density proxy, carrier cadence and both limiting trends; do not tune a parameter to a desired p law.

One fixed invalid-domain witness: eta=1e-8, k=0.01 in the same units. The proposed gap-only shortcut k^2/(2B)<=0.01 must pass while the actual acoustic relative error exceeds 0.01; the production hydrodynamic condition k^2/h<=0.01 must reject it. This is a scope counterexample, not a failure of the full action.

Negative controls use the unchanged action/current/source/dispersion identities or validity tests: reverse the quartic sign (boundedness), halve the Noether density, double the collective stress, remove amplitude/phase mixing, replace acoustic speed by metric light speed, set finite-density pressure to exact dust, and accept the gap-only sound condition. Each changed expression must fail its designated production test, not merely flip a status flag.

Stop after these tests and the candidate decision. No second potential, lattice fit, phenomenological pressure function or strong-field time integration is opened.

## Dependency hashes and primary sources

Paths below are relative to the RefG workspace root.

- CODES.md: 27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41
- RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md: 6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879
- RefG/work 3/Cosmology_and_LSS/CMB_Closure/w3_62_cmb_einstein_source_linear_closure_preregistration.md: b4068791b63e9a072a897e9aa85eae96c588b0d33533effb9664ffbd667ae810
- RefG/work 3/Strong_Field/W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction_contract.md: 7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa
- RefG/work 3/Strong_Field/W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction.py: 4efe86c593db5ad9f5dfb7a1efe1aa0f4d5f2ea0af410d25ba1c7743534c5672

D. T. Son, Low-Energy Quantum Effective Action for Relativistic Superfluids (2002), https://arxiv.org/abs/hep-ph/0204199, provides the effective-pressure/phase framework.

M. G. Alford et al., From a complex scalar field to the two-fluid picture of superfluidity (2013), https://arxiv.org/abs/1212.0670, provides a microscopic complex-scalar/superfluid precedent. This stage uses only the declared zero-temperature classical candidate and independently checks its formulas.
