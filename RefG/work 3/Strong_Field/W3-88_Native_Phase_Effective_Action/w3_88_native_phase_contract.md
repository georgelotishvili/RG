# W3-88: Native phase effective action and the density-closure test

## Decision and stopping rule

Extract the nonlinear static phase energy of the unchanged W84 node-link
Hamiltonian. Determine which native state variable controls its response,
as the microscopic check requested after W87. The new result is the exact
implicit nonlinear reduced energy and its leading induced interaction.
W84's equilibrium and linear Schur stiffness are regression targets.

Stop after this reduction and its independent verification. Exactly two files:
this contract and w3_88_native_phase.py. No new constitutive function, metric,
simulation, parameter scan, result file, cache, publication, or edits elsewhere.
The algebraic targets below were obtained by hand and independently checked
before this verifier; numerical budgets are frozen before its first run.

## Claim contract

- CLAIM_ID / TYPE / MODEL_VERSION: W3_88_NATIVE_PHASE_REDUCTION; exact static
  reduction plus leading adiabatic approximation of the W84-v1.0 TOY; v1.0.
- CLAIM: Eliminating the positive-stiffness link coordinate generates a
  nonlinear phase-strain energy. Across the admitted uniform states, native
  tangent phase stiffness cannot be represented by uniform rotor action alone.
- ASSUMPTIONS / DOMAIN / CONVENTIONS: The original N=48 periodic 1D graph,
  canonical Hamiltonian time, rotor pairs (theta,n), link pairs (q,P), and
  s=1-cos(Delta) in [0,2]. All W84 constants remain one. Derivations also use
  positive symbolic B,C,I and the inherited smooth positive K(q), K''(q)>0.
  q is logarithmic bond dilation and n is rotor action per graph site.
- FREEDOM_LEDGER: No new physical parameter or fitted coefficient. Inherit
  W84's postulated elastic energy and overlap law. Taylor angles below are
  single-bond constitutive probes, not additional periodic uniform states.
- DEPENDENCIES: W84 frozen Hamiltonian and coupling implementation. W87's
  F(n_C)T candidate is the motivation, with its current/operator map OPEN.
- METHOD: Canonical Legendre elimination, strictly convex static minimization,
  envelope differentiation, Taylor back-substitution, high-precision direct
  roots, independent finite differences of minimized original energy.
- PASS_CONDITION / RESIDUAL / ERROR_BOUND: All symbolic residuals zero; all
  numerical budgets below satisfied; each altered-expression control rejected.
- FAIL_CONDITION / FALSIFIER: A nonzero required identity or failed residual
  budget invalidates the corresponding reduction. Two stable states with
  equal rotor n and unequal phase stiffness reject a universal rotor-only
  stiffness for this family. A failed graph test does not reject all RefG.
- VALIDITY_HEALTH / BRANCHES: Unique link minimum for each s; phase stability
  additionally requires W_DeltaDelta>0. Dynamic use is leading adiabatic only:
  slow forcing compared with sqrt(D/I) and no unsuppressed free link mode.
  The exact full two-field Hamiltonian and its high-frequency branch remain.
- OBSERVABLE_MAP: Bond energy and tangent phase stiffness per material label.
  A 3D proper volume, physical collective current n_C, and torsion operator
  have no derived map from this graph. Same n means same rotor action, not
  necessarily the same proper-volume density or foundation pressure.
- FORWARD_MODEL / DATA_ROLE: N/A; synthetic algebraic checks, no observational
  data or empirical fit. No observational or strong-field validity claim.
- IDENTIFIABILITY / BENCHMARK: Compare the reduced energy with the original
  W84 potential at its minimum and with its frozen-q=0 expression. At fixed
  n compare W84's already admitted stable twists Q=0 and pi/6.
- CROSSCHECK: Generic Taylor stationarity versus minimized unexpanded W84
  energy; energy finite differences versus the analytic envelope curvature;
  original Hamilton equations versus a uniform rotor-action shift. Shared
  premise: W84 Hamiltonian. Independent reviewer checks the algebra and scope.
- CLOSURE_FLAGS: Compute provenance, Legendre_elimination, static_envelope,
  Taylor_reduction, direct_energy_check, native_state_variable_test,
  mutation_controls. Keep microscopic_gravitational_F_derived,
  physical_current_map, full_dynamical_equivalence, regular_black_hole,
  singularity_resolved, observational_pass, active_theory_changed,
  intuitive_files_changed false.
- PROVENANCE / FILES: Pin this contract, W84 verifier/contract, W87 contract
  and CODES; print this verifier's hash and library versions. Python -B,
  finite JSON stdout only. Existing source and intuitive files are protected.

## Reduction from the original Hamiltonian

For one link write

    V(q,s)=B*q^2/2+K(q)*s,
    K(q)=K0*exp[-q-kappa*d0*(exp(q)-1)].

Variation of n and P in sum(n*theta_dot+P*q_dot)-H gives
n=nbar+C*theta_dot and P=I*q_dot. The exact Lagrangian is

    L=sum[nbar*theta_dot+C*theta_dot^2/2+I*q_dot^2/2-V(q,s)].

Let q*(s) solve B*q+K'(q)*s=0. Its derivative in q is
D=B+K''(q)*s>0; the force function crosses zero exactly once. At s=0
q*=0, and at s>0 q*>0. Define the exact static minimized energy

    W(s)=B*q*(s)^2/2+K(q*(s))*s.
    dq*/ds=-K'/D,
    dW/ds=K(q*),
    d^2W/ds^2=-K'^2/D.

Consequently W>=0 and increases with s, while its slope decreases. The
induced interaction is an energy reduction relative to keeping q fixed.
Phase curvature, which also differentiates s=1-cos(Delta), is

    S=d^2W/dDelta^2=K*cos(Delta)-K'^2*sin(Delta)^2/D.

This recovers W84's mixed Schur stiffness. D>0 alone does not imply S>0.
The phase-only leading adiabatic action is

    L_ad=sum[nbar*theta_dot+C*theta_dot^2/2-W(1-cos(Delta))].

Static elimination is exact. For time-varying strain, substitution already
produces the higher-derivative term I*(dq*/ds)^2*s_dot^2/2, and the full
link equation is I*q_ddot+V_q=0. These terms are omitted only in the stated
slow, unexcited-link limit. No convergence claim is made for arbitrary
histories, free link oscillations or a black-hole evolution.

## Leading nonlinear interaction

Set k_j=K^(j)(0). Taylor back-substitution into V_q=0 and V yields

    q*=(-k1/(2B))*Delta^2
       +(k1/(24B)+k1*k2/(4B^2))*Delta^4+O(Delta^6),
    W=k0*Delta^2/2-(k0/24+k1^2/(8B))*Delta^4
      +(k0/720+k1^2/(48B)+k2*k1^2/(16B^2))*Delta^6+O(Delta^8).

The new induced quartic term is -k1^2/(8B). The sixth-order coefficient
only checks the quartic truncation error; the polynomial is not extrapolated
to large strain. The exact W stays nonnegative. With the frozen constants:

    q*=Delta^2-19*Delta^4/12+O(Delta^6),
    W=Delta^2/2-13*Delta^4/24+601*Delta^6/720+O(Delta^8).

## Native state variable and the W87 boundary

The original equations admit the exact transformation

    n_i -> n_i+eta, theta_i(t) -> theta_i(t)+eta*t/C,
    q_i,P_i,Delta_i unchanged,

for constant eta. It changes the common phase rotation and energy, while
preserving link forces, phase differences and tangent stiffness. It is a
mapping between solutions, not a claim of gauge equivalence. Conversely,
the stable uniform states Q=0 and Q=pi/6 have the same n=nbar but different S.
Thus the native stiffness requires strain information; rotor action alone
is insufficient on this admitted family.

This supplies a derived phase interaction, not W87's gravitational F(n_C).
The physical current-density/coframe map and the gravitational operator's
microscopic origin remain the specific missing inputs. A spatial phase
stiffness, a bulk modulus and an Einstein/TEGR action coefficient are distinct
quantities. Neither identifying them by name nor replacing n_C with rotor n
constitutes the missing derivation. W87's physical candidate stays OPEN.

## Frozen numerical and alteration checks

1. Use mpmath at 80 decimal digits, 260 bisections on inherited q in [0,4],
   returning q=0 at Delta=0. Require equilibrium force residual <1e-60.
2. Single-bond angles {0.08,0.04,0.02}: compare unexpanded minimized V with
   the quartic Taylor energy. The residual divided by Delta^6 must approach
   601/720 monotonically in absolute error and lie within 5% of it at every
   probe. The q quadratic residual divided by Delta^4 must approach -19/12
   under the same rule. Repeat at 100 digits/330 bisections; q,W differences
   <1e-60. Both precisions and all probe results are retained.
3. At Q=pi/6, centered second differences of the directly minimized energy
   at h={1e-5,5e-6} must agree with S within 1e-8 absolute; the second error
   must be at most 0.4 times the first unless both are below 1e-20.
4. At Q=0,pi/6 require S>0 and an absolute between-state S gap >1e-3 at
   equal n=nbar. For each Q repeat n={0.5,1,2}: original W84 velocities must
   give the changed common phase rate, while forces and stiffness stay fixed
   to 1e-12. This checks native rotor action, not physical volume density.
5. Altered expressions: frozen-link quartic, omitted cosine quartic,
   reversed induced quartic sign, and omitted Schur term. Feed them into
   the same series/curvature residual evaluators as the baseline and require
   actual nonzero residuals. These are software controls, not new models.

## Outcome defined by the reduction

The unchanged W84 hypothesis produces a nonlinear, strain-dependent phase
energy and a definite negative quartic correction from link adjustment.
Its uniform rotor action controls common phase rotation independently.
This closes the native effective-energy calculation and rules out the
proposed rotor-only identification across the tested stable state family.
It does not supply the physical gravitational coefficient or a regular
black-hole solution. Stop here; no additional conditional algebra replaces
the missing microscopic current/coframe relation.
