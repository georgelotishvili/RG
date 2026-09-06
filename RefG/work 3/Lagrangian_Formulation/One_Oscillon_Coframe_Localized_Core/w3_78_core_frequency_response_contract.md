# W3-78: Core frequency response through the common geometry

## Working decision

Determine the retained core's coupled radial frequency response to a weak,
spatially structured perturbation of the common metric. Compute the response,
its accessible scalar channels and energy accounting before proposing any
population filter. The probe tests the action-derived connection between
geometry and core motion; its production by a collective population is a
separate source problem.

The new result is a frequency-dependent susceptibility and channel-resolved
flux, with a bounded search for genuine internal modes. W3-58 provides the
core and fluctuation operators; W3-66 provides the two-channel methodology.
Its self-gravitating numerical frequencies are not imported into this flat
benchmark. W3-76/77 remain local exchange results.

Allowed files: this contract and w3_78_core_frequency_response.py in the
existing One_Oscillon_Coframe_Localized_Core folder. Runtime writes no files.
Stop after the registered response, checks and scoped spectral decision.
Intuitive files, upstream mathematics and release metadata stay unchanged.

## Frozen claim contract

- CLAIM_ID: W3_78_CORE_COMMON_GEOMETRY_FREQUENCY_RESPONSE.
- CLAIM: The minimally metric-coupled W3-58 action fixes a coupled
  amplitude/phase response operator and lapse-probe vertex. A structured
  probe has a calculable radial response whose outgoing scalar flux balances
  the supplied rotating-frame energy. Uniform lapse is an exact clock gauge
  control. Physical bound-mode candidates require both coupled equations
  and decaying exterior conditions.
- TYPE: CONDITIONAL_EXACT_RESPONSE_OPERATOR_WITH_NUMERICAL_SUSCEPTIBILITY.
- MODEL_VERSION: W3-78-v1.0, frozen before execution.
- ASSUMPTIONS: W3-58 canonical complex scalar and sextic binding action;
  a=1/4, Omega=4/5, positive nodeless core; local regular operational frame;
  prescribed infinitesimal lapse with flat spatial metric; linear response
  in probe amplitude epsilon; radial ell=0. All coefficients are inherited.
- DOMAIN: One core's linear radial response, not a nonlinear population
  trajectory. The flat core and an external weak metric are a test-response
  problem. No self-consistent Einstein/collective source is assigned to the
  probe. Bound search is 0.01<=kappa<=0.195; driven samples are below 0.8.
- CONVENTIONS: W3-58 dimensionless r=m r_physical, t=m tau;
  u=sqrt(lambda) chi exp(i theta_O)/m; signature (-+++).
  Reduced radial U,V include the factor r. All reported response amplitudes
  are per epsilon and powers per epsilon squared; q=lambda Q,
  Ehat=lambda E_physical/m. kappa is modulation frequency in mass units,
  not a particle mass or the background carrier Omega.
- FREEDOM_LEDGER: No new coupling, damping, potential or species parameter.
  The diagnostic lapse shape is fixed to s(r)=f(r)^2/f(0)^2; it is a probe,
  not a derived cosmological profile. Its amplitude is infinitesimal.
  Once computed from the background, s is held fixed during variation;
  it is not a field-dependent self-interaction of the perturbed core.
  Probe frequencies and numerical boundaries are specified below.
- DEPENDENCIES: Hash-pinned W3-58 contract/solver, W3-66 contract/solver
  (method only), W3-50 and W3-54 contracts. Record own contract/source hashes.
- METHOD: Vary the lapse-coupled radial action, linearize the complex field,
  derive the coupled pencil and retarded exterior, solve forced BVPs,
  cross-check by finite differences, and compare volume work with boundary
  flux. Search for nonzero bound poles using a sparse quadratic pencil,
  refining candidates with physical two-channel boundary conditions.
- PASS_CONDITION: All exact identities, pins and mutation controls pass;
  registered forced-response residual, charge, flux and convergence budgets
  pass. A bound pole is an independently reported result, not a required
  count. Unresolved pole candidates remain inconclusive rather than being
  relabelled absent. A finite search does not certify spectral completeness.
- FAIL_CONDITION: Incorrect variation, mixing, source, time/phase convention,
  outgoing sign, charge balance, energy accounting, dependency or numerical
  budget. Solver failure is numerical inconclusiveness, not a theory no-go.
- FALSIFIER: A nonzero exact residual falsifies the claimed operator or
  vertex. A converged solution violating current/flux identities falsifies
  the implementation. Bound candidates disappearing under physical boundary
  or mesh refinement fail their individual mode claim.
- RESIDUAL: Exact zero for variation, coupled pencil, exterior dispersion,
  uniform-lapse bulk response, charge identity, source-work/flux identity,
  and physical-energy minus Omega-charge accounting.
- ERROR_BOUND: Algebra exact at first order in epsilon; reported power is
  quadratic. Backreaction and finite-amplitude corrections are outside the
  probe approximation. Numerical budgets and omitted exterior-source
  control are below; floating-point evidence is not interval certification.
- VALIDITY_HEALTH: Same kinetic operator and current as W3-58. Retarded
  outgoing waves carry energy/charge; no phenomenological friction is added.
  A uniformly time-dependent lapse alone is a coordinate change. Genuine
  source curvature is provided by the spatially nonconstant probe.
- BRANCHES: Phase zero mode; frequency-family generalized zero mode;
  nonzero radial modes; two closed scalar channels below kappa=0.2;
  one open upper channel on 0.2<kappa<0.8.
- OBSERVABLE_MAP: The dimensionless core amplitude readout is
  A(kappa)=integral r f U dr / integral r^2 f^2 dr.
  Also report the full reduced response and channel fluxes. This readout
  depends on the specified probe. Natural mode frequencies, if found, are
  poles of the homogeneous operator rather than imposed drive frequencies.
- FORWARD_MODEL: Action -> core -> metric vertex -> retarded response ->
  amplitude and scalar flux. No experimental instrument or likelihood.
- DATA_ROLE: N/A: no observational data, mass fit or Koide target.
- IDENTIFIABILITY: A response to a prescribed metric determines a
  susceptibility, not the distribution or physical generation of that
  metric. theta_O, neutral theta_C and the family mass-map angle stay
  distinct. No microscopic mode-selection or mass map is supplied by
  identifying these variables.
- BENCHMARK: The inherited a=1/4, Omega=4/5 core, as detailed below.
- CROSSCHECK: Complex versus real-component field variation; time-domain
  versus coupled frequency-domain equations; collocation versus independent
  finite differences; charge integral; work integral versus outgoing flux;
  domain/tolerance comparison; optional poles checked with physical BVPs.
- NEGATIVE_CONTROLS: Remove gyroscopic mixing; reverse one mixing sign;
  omit lapse time derivative; omit spatial-gradient vertex; remove lapse
  correction to charge; reverse outgoing sign; confuse full energy with
  rotating-frame work; replace the dynamic pencil by static Hessians.
- CLOSURE_FLAGS: Separate exact operator/metric vertex, gauge control,
  numerical response, radiative channel balance and accepted pole flags.
  Full_collective_mode_selection, theta_C_probe_source_derived,
  particle_mass_spectrum_derived, Koide_derived, nonlinear_core_quantized,
  alpha_derived, observational_pass and intuitive_files_changed remain false.
- PROVENANCE: Frozen dependency and contract hashes, source hash, versions,
  residuals and all numerical outcomes printed as finite JSON to stdout.
- FILES: This contract and one no-write verifier; no result/report files.

## 1. Coupled response and the inherited metric vertex

The dimensionless ordinary field obeys

    u_tt - Laplacian u + u - |u|^2 u + a |u|^4 u = 0,
    u_0 = exp(i Omega t) f(r).

Write u=exp(i Omega t)[f+epsilon(eta+i xi)]. Then

    eta_tt - 2 Omega xi_t + script_L_plus eta = S_R,
    xi_tt + 2 Omega eta_t + script_L_minus xi = S_I.

For ell=0 the reduced radial operators are

    L_plus  = -d_r^2 + 1-Omega^2-3f^2+5a f^4,
    L_minus = -d_r^2 + 1-Omega^2-f^2+a f^4.

Use eta=Re[(U/r) exp(-i kappa t)] and
xi=Re[i(V/r) exp(-i kappa t)]. The real symmetric bulk pencil is

    P(kappa) = [[L_plus-kappa^2, -2 Omega kappa],
                [-2 Omega kappa, L_minus-kappa^2]].

Individual static Hessian eigenvalues do not replace this dynamic pencil.

For ds^2=-N^2 dt^2+dr^2+r^2 dOmega_2^2 and N=1+epsilon Phi,
the radial action gives

    u_tt/N^2 - N_t u_t/N^3 - u_rr
      - (2/r+N_r/N)u_r + (1-|u|^2+a|u|^4)u = 0.

At first order, Phi=s(r)cos(kappa t) supplies P(kappa)y=J, where

    J_U = r [s' f' - 2 Omega^2 s f],
    J_V = -Omega kappa r s f,           s=f^2/f(0)^2.

This vertex is the variation of the retained minimal metric coupling.
A generic common-metric perturbation similarly acts through delta Box_g u_0.
Producing it from the collective source and solving its backreaction requires
the retained Einstein and collective equations in addition to this response.

## 2. Gauge, charge and energy accounting

For uniform s=1 the exact bulk gauge response is

    U=0,             V=Omega r f/kappa.

It changes only the clock coordinate. At finite R its nonzero exterior
source requires the exact inhomogeneous boundary data for this control,
rather than a homogeneous free-wave Robin condition.

The physical first-order charge constraint is

    integral [r f(2 Omega U+kappa V)-Omega r^2 s f^2] dr = 0.

The phase zero mode is (U,V)=(0,r f). The generalized frequency-family
mode follows L_plus(r f_Omega)=2 Omega r f. Both are separate from nonzero
internal resonances.

For w_plus=U+V, w_minus=U-V, the physical perturbation is

    delta u = exp(i Omega t)
       [w_minus exp(-i kappa t)+conj(w_plus) exp(i kappa t)]/(2r).

Below threshold, impose w_plus'=-k_plus w_plus and
w_minus'=-k_minus w_minus, with k_plus/minus=sqrt[1-(Omega+/-kappa)^2].
Above the first threshold the upper retarded condition is
w_plus'=+i q_plus w_plus, q_plus=sqrt[(Omega+kappa)^2-1];
the lower channel remains decaying in the tested window.
These are the zero-regulator retarded conditions, not a damping model.

The rotating-frame quadratic energy is Ehat-Omega q. For real J,

    P_in = 2 pi kappa Im integral (J_U U+J_V V) dr,
    P_out = 2 pi kappa Im [conj(U)U'+conj(V)V']_R
          = pi kappa q_plus |w_plus(R)|^2      (one open channel).

The full ordinary fluxes at infinity are

    F_q = pi q_plus |w_plus|^2,
    F_E = (Omega+kappa) F_q,
    P_out = F_E-Omega F_q.

All powers are per epsilon^2. Outgoing charge changes the core at second
order on long times; the fixed-background linear response does not claim a
strictly stationary finite-amplitude emitter.

## 3. Frozen numerical protocol

1. Recompute W3-58 f at radius 80, tolerances 1e-7 and 3e-8, without invoking
   its file-writing main. No archived profile is substituted for the ODE.
2. At kappa={0.04,0.08,0.12,0.16,0.19,0.24,0.32,0.48}, solve the forced
   four-component complex BVP at R={30,40,50}, tolerance 1e-7; repeat R=40
   at 3e-8. Impose U(0)=V(0)=0 and the two physical exterior conditions.
3. Require solver success and maximum collocation residual <2e-6.
   Use profile-weighted core norms to compare responses across domains
   and tolerances; require relative variation <2e-4. Report complex
   A(kappa), with real and imaginary parts, and outgoing channel amplitudes.
   The neglected exterior potential/source is controlled by this comparison.
4. Independently solve the forced reduced equations using sparse central
   finite differences at R=40, h={0.02,0.01,0.005}, including second-order
   endpoint Robin conditions. Finest-grid profile-weighted response error
   against collocation must be <3e-3; report all three errors.
5. Evaluate charge and work with Simpson integration, independently of the
   collocation residual. The normalized first-order charge error is <2e-5.
   For the open-channel samples require relative volume-work/boundary-flux
   error <2e-4. For closed channels report zero imaginary work/flux within
   numerical roundoff. The first-order charge condition includes the lapse.
6. At kappa=0.12 run the uniform-lapse control with its exact inhomogeneous
   endpoint values; compare with U=0,V=Omega r f/kappa to relative error
   <2e-5. The spatially structured probe has nonzero lapse Hessian.
7. Bounded internal-mode search: on R=40, h=0.04 use the sparse quadratic
   pencil linearization [[0,I],[diag(L_plus,L_minus),-C]],
   C=[[0,2Omega I],[2Omega I,0]], at shifts {0.05,0.10,0.15},
   requesting 16 eigenvalues per shift. Record real and complex candidates.
   Only positive real candidates in [0.01,0.195] are eligible for bound-mode
   refinement. Refine with the full coupled homogeneous BVP, physical
   frequency-dependent decaying conditions and unit integral(U^2+V^2).
   Require solver success, equation residual <2e-6, normalized charge
   residual <2e-5, and relative frequency agreement <2e-4 across R=30,40,50.
   Cross-check with h=0.02 and 0.01 quadratic pencils; finest frequency
   discrepancy <3e-3. Track zero-mode/finite-box artifacts separately.
   Failure to resolve a candidate is explicitly INCONCLUSIVE, never a
   manufactured absence claim. No claim covers every threshold/complex mode.
8. Exact controls and dependency pins must pass before numerical work.
   Numerical failures keep their actual outcomes; parameters, sample
   frequencies and thresholds are not adjusted to produce desired peaks,
   three modes or a Koide relation.

## Sources and retained scope

Kovtun, Nugaev and Shkerin, Vibrational modes of Q-balls,
https://arxiv.org/abs/1805.03518, gives the coupled vibrational framework.
Ciurla, Dorey, Romanczukiewicz and Shnir,
https://arxiv.org/abs/2405.06591, studies normal/scattering channels in one
spatial dimension. These are methodological sources, not this benchmark's
numerical evidence. The present calculation uses the retained 3D radial
action and its independently recomputed profile.

The completed object is a common-geometry-to-core response function.
Particle-species selection, the nonlinear collective environment, its
source statistics and the energy-to-observed-mass bridge remain the
separate physical steps named in W3-50 and intuitive sections 1.4,4.3-4.5.
