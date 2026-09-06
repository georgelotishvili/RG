# W3-81: Dynamical test of the branch-restricted scale connection

## One decision and stopping rule

Test whether the W3-71 connection can be extended to a single temporal-scale scalar on the actual collective-phase flow of the full W3-80 action coupled to Einstein gravity. The new input is a constrained, inhomogeneously expanding Cauchy slice of that action. W3-71 tested a freely specified mixed congruence; this test supplies the matter equations and gravitational source that determine the necessary time derivatives.

Only this frozen contract and one stdout-only verifier may be created in this folder. Stop after the integrability decision and its independent checks. No new pressure function, modified connection, potential, coupling, collapse evolution, manuscript edit or publication is authorized here.

## Frozen claim contract

- CLAIM_ID: W3_81_FULL_CONDENSATE_DYNAMIC_SCALE_INTEGRABILITY.
- CLAIM: The connection W_a=a_a+(Theta/5)u_a is tested for local exactness on the selected full Einstein-condensate Cauchy jet, with u the normalized timelike collective-phase gradient. A nonzero component of dW on any admissible member disproves its extension as d ln p_t on every such dynamical state. The original homogeneous and normalized-static-Killing branches retain their separate tests.
- TYPE: EXACT_LOCAL_DYNAMIC_COUNTEREXAMPLE_TEST; a verification PASS and the proposed extension's ACCEPTED/REJECTED/OPEN status are distinct.
- MODEL_VERSION: W3-81-v1.0; action, state family, reference cases, numerical budgets and controls frozen before execution.
- ASSUMPTIONS: W3-80 canonical neutral complex field, m_C>0, lambda_C>0; one operational Einstein metric, G>0 and Lambda=0. Ordinary field set to zero, a consistent sector of the additive system. Use the full amplitude and phase equations, without eliminating the amplitude or imposing the effective barotropic EOS during evolution. The identification of W3-71's congruence with u_C is the particular proposed extension under test.
- DOMAIN: Smooth local spherical Cauchy data on an open annulus r>0, sigma>0, zeta>0, R>0 and X>0. A compact subannulus and a sufficiently small smooth-development neighborhood avoid the centre and the polar-field coordinate endpoint. No global completion, central object, event horizon or finite-time endpoint is prescribed.
- CONVENTIONS: Signature (-+++); c0=hbar=1; ds^2=-sigma^2 dT^2+(dr+sigma*zeta*dT)^2+r^2 dOmega^2. e0=sigma^(-1)partial_T-zeta*partial_r. X=-g^{ab}theta_a theta_b, mu=sqrt(X)>0, u_a=-theta_a/mu, j^a=R^2 mu u^a and n=R^2 mu. Theta=div(u), a_a=u^b nabla_b u_a, F_Tr=partial_T W_r-partial_r W_T. S=T_hat0hat1 is minus ADM radial momentum density. Mechanical pressure P_C and foundation readout P_F remain distinct.
- FREEDOM_LEDGER: Inherited universal candidate constants m_C,lambda_C and gravitational G. Uniform R0>0 and A=2G M0>0 are initial/boundary data; b=8*pi*G*rho0/3 is determined, not an independent constitutive parameter. M0 is an annular mass integration datum, without a specified r=0 continuation. The overall lapse normalization sets sigma=1,sigma_T=0 on the slice. No fitted functions or altered exponent 1/5.
- DEPENDENCIES: Hash-pinned CODES, W3-71 contract/definition, W3-80 contract/action, and W3-79 source/geometry interface. For an independent curvature calculation, import only W3-73 geometry_base; its main and cached result JSON are never executed/read. Existing PASS labels are not substituted for residuals.
- METHOD: Vary the full action; compute its current and Hilbert stress; derive the full phase/amplitude time jets; check the Einstein constraints, evolution and angular projection against the metric-derived Einstein tensor. Obtain the acceleration derivative both from Christoffels and from the normalized-gradient identity. Differentiate W and test its exterior derivative. Crosscheck the radial derivative numerically at frozen synthetic points.
- PASS_CONDITION: All action, source, Cauchy-jet, geometry, derivative and regression identities vanish exactly; every registered numerical check meets its budget; all registered mutations fail the same unmodified production identities. The nonzero/zero curl is reported, not forced into the inputs.
- FAIL_CONDITION: An inconsistent constraint, matter equation, stress balance or time jet; disagreement between the independent curl derivations; a failed numerical budget or a mutation escaping detection. Such a failure leaves the proposed extension OPEN pending correction of the diagnostic.
- FALSIFIER: A verified nonzero F_Tr at an admissible on-shell jet rejects the UNIVERSAL extension on this specified congruence. Vanishing F in this family alone cannot prove universal integrability and leaves that broader claim OPEN. No test here rejects all possible temporal readouts, the W3-80 action, RefG as a whole or the already branch-restricted W3-71 result.
- RESIDUAL: Exact symbolic zeros for required field/Einstein/source/derivative identities; F_Tr itself is a diagnostic and need not vanish. Numerical derivative residuals are recorded separately.
- ERROR_BOUND: Exact local field-equation jet; no time-stepping truncation and no hydrodynamic derivative expansion. Numerical crosscheck is only a centered radial derivative with frozen step sizes and error budget below, not an existence certificate or a finite-time solution.
- VALIDITY_HEALTH: R0>0, X0=mu0^2>0, positive quartic, positive initial rho0 and rho0+P0; Lorentzian regular annular PG metric. Cartesian matter variables retain canonical wave principal terms. Smooth local Einstein-scalar development is the Cauchy framework; this package checks its initial constraints and the necessary field/evolution jets, not a new global well-posedness theorem.
- BRANCHES: A>0 inhomogeneous-expansion witness; A=0 homogeneous-expansion control; static normalized-Killing connection control. The evolved full amplitude field is not required to remain on the instantaneous homogeneous-minimum relation mu^2=m_C^2+lambda_C R^2.
- OBSERVABLE_MAP: The candidate scalar would satisfy d ln p_t=W. A nonzero F obstructs that definition. The associated infinitesimal path discrepancy is a mathematical property of this proposed readout, not a prediction of clock experiments, photon propagation or physical clock holonomy.
- FORWARD_MODEL: N/A for observations; action -> compatible Cauchy data -> local time derivatives -> exactness test.
- DATA_ROLE: No observations or fitting. Three preregistered synthetic radial points crosscheck an analytic derivative.
- IDENTIFIABILITY: A single admissible nonzero-curl witness discriminates the proposed universal exact-form extension from its restricted use. It neither identifies P_F nor selects an alternative flow or readout law.
- BENCHMARK: W3-71's homogeneous and static branches; independently computed Einstein tensor; differentiated full phase conservation rather than a supplied EOS; direct Christoffel acceleration rather than an assumed acceleration jet.
- CLOSURE_FLAGS: Start false and derive action_source_checked, einstein_cauchy_jet_checked, matter_cauchy_jet_checked, independent_curl_checked, branch_regressions_checked, numerical_crosscheck_passed, mutation_controls_passed and universal_extension_rejected from checks. universal_scale_map_derived, P_F_bridge_derived, full_time_evolution_solved, singularity_resolved, observational_pass, active_theory_changed and intuitive_files_changed stay false.
- CROSSCHECK: Tensor curvature vs reduced constraints; full phase divergence vs current conservation; Christoffel acceleration vs normalized-phase-gradient identity; analytic radial differentiation vs centered differences. Shared inputs are the declared action, metric and initial data, not an assumed zero/nonzero curl.
- PROVENANCE: Report SHA-256 of this contract, verifier and dependencies, package versions and finite JSON stdout; no bytecode, result caches, plots or runtime file writes.
- FILES: This contract and w3_81_dynamical_scale_integrability.py only.

## 1. Full action and allowed initial data

The collective matter Lagrangian is

    L_C = -(partial R)^2/2 - R^2(partial theta)^2/2 - V(R),
    V(R)=m_C^2 R^2/2+lambda_C R^4/4.

Vary before substitution:

    Box R + R X - V'(R)=0,
    nabla_a(R^2 partial^a theta)=0,
    T_ab=R_a R_b+R^2 theta_a theta_b+g_ab L_C.

At T=0 choose spatially uniform R0 and phase, with

    R=R0, R_T=R_r=0,
    theta_r=0, theta_T=mu0,
    mu0^2=m_C^2+lambda_C R0^2,
    sigma=1, sigma_T=0,
    rho0=m_C^2 R0^2+3 lambda_C R0^4/4,
    P0=lambda_C R0^4/4,
    zeta(r)=sqrt(A/r+b*r^2), b=8*pi*G*rho0/3, A>0.

Uniform fields mean all initial spatial derivatives vanish; mixed derivatives of the subsequent evolution must be derived rather than set to zero. Initially u=e0 and T_hat=diag(rho0,P0,P0,P0). Einstein's mass constraint is

    m_MS(r)=r*zeta^2/(2G)=M0+4*pi*rho0*r^3/3.

The pressure term in radial Einstein evolution, the full angular Einstein equation, and mass-balance integrability must all be checked. Setting sigma_T=0 is consistent only if the differentiated momentum constraint gives sigma_rT=0.

## 2. Derivatives that decide integrability

Compute Theta from the normalized flow and invariant volume element. Derive mu_T, R_TT, theta_TT, theta_rTT, n_T, stress time derivatives and zeta_T from the field equations and gravitational evolution. In particular, initially vanishing a_r or W_r does not imply a vanishing time derivative.

Independently derive the kinematic identity for a normalized timelike phase gradient,

    a_a=-(delta_a^b+u_a*u^b) partial_b ln mu,

and compare its initial acceleration derivative to one computed with the PG Christoffels. Then evaluate F_Tr and its radial dependence. The identity is used for the full field's phase flow, not a barotropic assumption. Differentiating the initial minimum relation as if it held throughout evolution is an explicit error control.

For the homogeneous control A=0, test that F vanishes and current conservation gives dot(ln n)=-Theta, compatible with the W3-71 factor 1/5. For a static normalized Killing flow, independently test Theta=0 and W=d ln N. These are the same restricted claims as before.

## 3. Frozen numerical and mutation checks

Numerical parameters: m_C=lambda_C=R0=1, hence rho0=7/4, P0=1/4 and mu0=sqrt(2). Set b=1/100, G=3/(1400*pi), A=1, M0=A/(2G). Evaluate r in {2,3,4}. These points have zeta^2<1 and demonstrate that a centre or horizon is unnecessary for this test.

At each point compare the symbolic derivative of Theta against centered differences with h/r in {1e-3,5e-4}. Require finite results, relative error below 2e-5 for both steps, and fine-step error at most 0.35 times coarse-step error plus 1e-10 relative roundoff slack. Report the computed F_Tr and its sign without adjusting parameters.

Four negative controls must fail their corresponding unchanged identity:

1. Replace the acceleration time derivative by zero because acceleration initially vanishes.
2. Delete the Theta*u/5 term from the declared W when comparing its curl to the actual definition.
3. Double the collective Hilbert source in the unchanged Einstein equations.
4. Enforce the time-differentiated homogeneous-minimum relation on the full initial jet; test it against the amplitude and phase equations.

A nonzero-curl decision is allowed only after all consistency checks and independent controls pass. Do not replace a failed diagnostic with the anticipated conclusion.

## Input SHA-256 pins

Paths are relative to the RefG workspace root.

- CODES.md: 27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41
- RefG/work 3/Strong_Field/W3-71_Horizon_Material_Scale_Separation/w3_71_horizon_material_scale_separation_preregistration.md: 1d3f74489f6cc52061253b6e1ea3d7f96e5d423f8b2afb88e79a44a38ae916c3
- RefG/work 3/Strong_Field/W3-73_Coupled_Horizon_Regular_Einstein_Complex_Scalar/w3_73_coupled_horizon_regular_einstein_complex_scalar.py: 47f2c97b64544f124cc2a5cb8d04825188664493cb5d770b6c3faf4ce2d5d7ca
- RefG/work 3/Strong_Field/W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction_contract.md: 7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa
- RefG/work 3/Strong_Field/W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction.py: 4efe86c593db5ad9f5dfb7a1efe1aa0f4d5f2ea0af410d25ba1c7743534c5672
- RefG/work 3/Strong_Field/W3-80_Resonant_Constitutive_Candidate/w3_80_neutral_resonant_condensate_contract.md: 27e359b9980df14a287ca89cc38a895eb5015a732154d7a055fd7666b418d841
- RefG/work 3/Strong_Field/W3-80_Resonant_Constitutive_Candidate/w3_80_neutral_resonant_condensate.py: da4c0c7574e5ef9b8347562d628bff31b9be8c14c5417f29c185f977c0eb7381

The condensate conventions are those of W3-80, with the complex-scalar precedent identified there: M. G. Alford et al., https://arxiv.org/abs/1212.0670. The present curved Cauchy-jet and scale-integrability test are derived directly from the displayed action.
