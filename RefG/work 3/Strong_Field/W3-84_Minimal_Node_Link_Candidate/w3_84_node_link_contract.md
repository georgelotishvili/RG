# W3-84: Minimal dynamical node-link hypothesis

## One decision and stopping rule

Test one explicit joint energy for phase transfer and the links carrying it.
The new physical input is the Hamiltonian below, not a result inherited from
RefG. Decide whether its selected equilibria have a healthy coupled response
and slower long-wavelength transfer, and verify one small nonlinear traveling
wave. Stop after this decision and its independent checks. No new potential,
parameter scan, collapse evolution, active-theory edit or publication follows.

Only this contract and `w3_84_node_link.py` belong to this package. The verifier
writes finite JSON to stdout only. Intuitive files and all previous results
remain unchanged. A failed test retains its actual error; no silent adjustment
of the physical model, state, integration interval or acceptance budget.

## Claim contract

- CLAIM_ID: W3_84_MINIMAL_DYNAMICAL_NODE_LINK.
- CLAIM: The specified finite Hamiltonian graph supplies an explicit reciprocal
  phase/link coupling, exact energy and rotor-charge balances, and a calculable
  mixed stability domain. Classify every fixed state below. Test the selected
  primary state by a finite nonlinear traveling-mode evolution.
- TYPE: NEW_CLASSICAL_FINITE_GRAPH_HYPOTHESIS; exact identities plus numerical
  evidence for the stated equilibria and finite trajectory, not a microscopic
  derivation of the active RefG continuum.
- MODEL_VERSION: W3-84-v1.0. The Hamiltonian, constants and four twists were
  chosen before an independent design-stage spectral preview. That preview
  found three stable states and one unstable state; all four are retained.
  The nonlinear protocol and budgets below are frozen before its execution.
- ASSUMPTIONS / DOMAIN: Periodic one-dimensional material-label graph, N=48;
  real canonical pairs (theta_i,n_i) and (q_i,P_i), with theta an angle and
  q a dimensionless internal link dilation. d_i=d0 exp(q_i)>0 assigns a bond
  length. A general three-dimensional embedding or spacetime is not specified.
- CONVENTIONS: Link i joins i to i+1 modulo N; Delta_i=theta_(i+1)-theta_i.
  The evolution parameter is the Hamiltonian time, not a derived local clock.
  n is rotor phase action, not the number of foundation nodes. It is a real
  canonical variable; positivity is monitored in the selected small run.
- FREEDOM_LEDGER: C,I,B,K0,d0,kappa are positive new hypothesis parameters;
  C=I=B=K0=d0=kappa=nbar=1 are fixed synthetic benchmark choices, including
  the dimensionless kappa*d0=1. They are not all removable choices of units
  and are not measured or derived constants. N=48 and the winding are state
  data. The logarithmic elastic energy and evanescent-overlap form of K are
  postulates. No coefficient is fitted to a desired black-hole outcome.
- DEPENDENCIES: W50 motivates common phase-shift symmetry; W76 motivates
  the exponentially decaying inverse-distance shape. Its ordinary-core
  interaction is not a derivation of the present node-link stiffness.
- METHOD: Hamiltonian variation, bond Hessian and Bloch spectrum, independent
  finite-difference Jacobian of the full production force, then velocity
  Verlet and timestep refinement of one small traveling eigenmode.
- PASS_CONDITION: All registered identity, force, spectrum, conservation,
  mode and refinement tests pass. Report state stability and physical
  transfer outcome separately; an unstable diagnostic state is retained.
- FAIL_CONDITION / FALSIFIER: A wrong reciprocal force or balance, spectral
  mismatch, instability of the selected primary state, or failed numerical
  budget invalidates the corresponding candidate claim. This does not reject
  every node model. No preferred outcome is supplied as a source term.
- RESIDUAL / ERROR_BOUND: Exact symbolic residuals and numerical budgets below.
  Finite lattice evidence; no continuum, quantum or observational error bound.
- VALIDITY_HEALTH: Positive C,I,B,K0; finite variables; positive mixed stiffness
  on the primary branch; positive n and finite positive d throughout the run.
- BRANCHES: All four frozen twists, including a possible mixed instability;
  remove only the exact global phase zero mode when assessing positive modes.
- OBSERVABLE_MAP: Rotor charge, graph energy, bond length, wave frequency,
  and physical-distance long-wavelength velocity on a uniform equilibrium.
  An acoustic/group velocity is not a strict relativistic signal front.
- FORWARD_MODEL / DATA_ROLE: N/A: synthetic states, no observations or fit.
- IDENTIFIABILITY / BENCHMARK: One testable hypothesis, not a uniquely selected
  foundation law. Compare full coupled dynamics with its own independently
  linearized limit and with the same hypothesis at zero twist.
- CROSSCHECK: Full real-space force Jacobian and eigenvalues are independent
  of the analytic Bloch block; measured traveling-wave phase is extracted
  from the nonlinear trajectory. Shared premises are the frozen Hamiltonian.
- PROVENANCE / FILES: Hash the present contract, verifier, CODES, W50 and W76;
  report Python/NumPy/SciPy/SymPy versions. Exactly two files, no caches.
- CLOSURE_FLAGS: Compute joint_energy_defined, reciprocal_forces,
  conservation_identities, equilibrium, mixed_spectrum, nonlinear_mode,
  energy_balance, charge_balance, refinement and mutation_controls.
  Keep microscopic_law_derived, physical_node_identity, oscillon_solution,
  foundation_pressure_map, relativistic_covariance, Einstein_source_derived,
  weak_field_inheritance, singularity_resolution, observational_pass,
  active_theory_changed and intuitive_files_changed false.

## Hypothesis and equations

The new joint energy is

    H = sum_i (n_i-nbar)^2/(2C)
        + sum_i [P_i^2/(2I) + B q_i^2/2
                 + K(q_i)(1-cos Delta_i)],
    d=d0 exp q,
    K(q)=K0 exp[-q-kappa*d0*(exp q-1)].

This is a cosine phase coupling with a movable, energetically restoring link.
Writing x=kappa*d gives K'=-(1+x)K and K''=(1+x+x^2)K>0. Thus

    theta_dot=(n-nbar)/C,       q_dot=P/I,
    J_i=K_i sin Delta_i,
    n_dot_i=J_i-J_(i-1),
    P_dot_i=-B q_i-K'_i(1-cos Delta_i).

The same interaction produces the phase current and the link-opening force.
The force due to phase difference is nonnegative and vanishes at equal phases.
It weakens as q increases because K''>0. The restoring force is part of the
postulated energy, not an independently inserted damping/pressure equation.
At free-link equilibrium the total generalized mechanical force is zero;
neither this force nor B is identified with the RefG pressure readout P_F.

Verify dH/dt=0 and d(sum n)/dt=0 from these actual equations. With
E_i=(n_i-nbar)^2/(2C)+(h_link_i+h_link_(i-1))/2, the rightward energy flux is
-J_i*(theta_dot_i+theta_dot_(i+1))/2, and the rightward charge flux is -J_i.
Verify the local continuity identity as well as the global sums.

All summands in H are nonnegative. The finite-energy bound
|q_i|<=sqrt(2H/B) is due to the chosen elastic energy; it is not a spacetime
singularity result. No dissipation or asymptotic attractor is assumed.

## Equilibria and complete mixed spectrum

For Q in {0,pi/12,pi/6,pi/4}, set theta_i=Q*i, n_i=nbar, P_i=0, and let
q0 solve B*q0+K'(q0)*(1-cos Q)=0. The winding integers are {0,2,4,6}.
Use brentq on [0,4], xtol=1e-14, rtol=1e-14, returning q0=0 at Q=0.
The residual derivative B+K''*(1-cos Q)>0 proves uniqueness; q0>=0.

Define A=K cos Q, b=K' sin Q, D=B+K''*(1-cos Q), and
L_k=4 sin^2(k/2), z_k=exp(i k)-1, k=2*pi*j/N. The mass-weighted block is

    [[A*L_k/C,       b*conj(z_k)/sqrt(C*I)],
     [b*z_k/sqrt(C*I),              D/I]].

Its eigenvalues are omega_minus^2 and omega_plus^2. The homogeneous state
is stable apart from its phase zero mode precisely when D>0 and A-b^2/D>0.
For stable states the long-wavelength speed per label is sqrt((A-b^2/D)/C);
multiply by d0*exp(q0) for the physical-distance readout.

For the frozen kappa*d0=1 and q0>=0,

    c_long^2 <= d^2*K*cos Q/C <= d0^2*K0*exp(q0-exp(q0)+1)/C
               <= d0^2*K0/C.

Use this only on a stable admitted branch; never take the square root of a
negative stiffness. Comparing different Q compares different equilibria,
not a solved time-dependent cosmological dilution or an unchanged oscillon.

Independently differentiate the production force by centred differences at
steps {1e-5,5e-6}, assembling the full 96-dimensional potential Hessian.
Require normalized entry errors <1e-8 and spectrum errors <1e-7 against the
analytic block union (normalizer max(1,max absolute analytic entry/eigenvalue)).
Equilibrium force residual <1e-12. Report both Jacobian-step errors and every
state's minimum eigenvalue and mixed stiffness. Classify, do not omit, the
large-twist state. Primary Q=pi/6 must be stable for its nonlinear run.

## One finite nonlinear traveling-wave check

Primary Q=pi/6, q0 as above, N=48, k=2*pi/N, epsilon=1e-3, 0<=t<=160.
Use the lower Bloch eigenvalue omega^2 at k, with theta eigenvector component
1 and q component r=-b*z_k/(D-I*omega^2). Initialize the real traveling mode:

    theta_i=Q*i+epsilon Re(exp(i*k*i)),
    q_i=q0+epsilon Re(r*exp(i*k*i)),
    n_i=nbar+C*epsilon Re(-i*omega*exp(i*k*i)),
    P_i=I*epsilon Re(-i*omega*r*exp(i*k*i)).

Evolve the FULL Hamiltonian equations by velocity Verlet at dt={.04,.02,.01};
store only in memory at t=j/5, j=0,...,800. No clipping, wrapping projection,
frozen link, filtering or damping. Shorten a step only to land on output times.

Acceptance:

1. Energy drift on the fine run <5e-4 times the actual positive initial
   perturbation energy H(initial)-H(equilibrium), and report drift relative
   to total H too. Report the subtraction/roundoff scale explicitly.
2. Max total charge drift <1e-10*max(1,abs(Q_initial)); n_min>0 and finite
   positive lengths. Monitor the local sufficient stiffness A_i-b_i^2/D_i
   throughout the fine trajectory; it must remain positive.
3. Project theta-Q*i onto exp(-i*k*i), unwrap its phase, and determine the
   fitted frequency by an ordinary straight-line fit in t. Its relative
   error against omega <1e-3; maximum phase-fit residual <.01 radians and
   relative amplitude change <.01. Report the full recorded phase history.
4. At every common output time compare all four canonical-variable arrays;
   normalize their Euclidean difference by epsilon*sqrt(N). The maximum
   medium/fine difference must be <1e-3 and at most half coarse/medium,
   unless already <1e-7. Report every run, not only the accepted grid.
5. At least four altered expressions must fail the same exact/force/spectral
   evaluators: reverse phase current, omit link backreaction, omit the mixed
   Hessian block, and omit bond length from the physical velocity readout.
   A detected alteration is a software control, not a physical exclusion of
   a different Hamiltonian. Do not replace evaluations by preset flags.

## Provenance

Paths are relative to C:/Users/george/Desktop/fizikis statiebi/RefG.

- CODES.md: 27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41
- RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/w3_50_neutral_collective_phase_density_bridge_contract.md: c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635
- RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/w3_76_same_field_resonant_exchange_contract.md: e10781a73470220065c664196efe0c361dbfb1c6c2404864e895d6ad2380bd02

Cosine rotor-chain precedent: W. De Roeck and F. Huveneers, Glassy dynamics
in strongly anharmonic chains of oscillators (2019),
https://doi.org/10.1016/j.crhy.2019.08.007 (C. R. Physique 20, 419-428).
The present constitutive law is defined above and does not depend on this
reference as an unexamined physical premise.
