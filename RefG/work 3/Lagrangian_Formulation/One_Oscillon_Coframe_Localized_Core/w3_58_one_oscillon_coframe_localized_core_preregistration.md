# W3-58 Preregistration: One-Oscillon Coframe-Coupled Localized Core

**CLAIM_ID:** `W3_58_ONE_OSCILLON_COFRAME_LOCALIZED_CORE`

**CLAIM:** A single complex ordinary-phase order parameter `Psi_O=(chi/sqrt(2)) exp(i theta_O)`, minimally coupled to the same post-Genesis coframe metric as W3-54, admits a lowest-derivative bounded-binding action whose variation generates its amplitude equation, conserved ordinary-phase current, and Hilbert stress in one source ledger. For the minimal even sextic binding class, the vacuum-health condition and full harmonic finite-energy existence window follow analytically. At the frozen dimensionless benchmark `a=1/4`, `Omega=4/5`, the nodeless spherical ground state must be constructed with finite energy and charge, a converged intrinsic radius, virial and stress balance, and converged numerical orbital-stability evidence.

**TYPE:** `CONDITIONAL_EXACT_COFRAME_ACTION_AND_ANALYTIC_EXISTENCE_CLASS_WITH_PREREGISTERED_NUMERICAL_GROUND_STATE_AND_STABILITY_GATE`.

**MODEL_VERSION:** `W3-58-v1.0-MINIMAL-U1-SEXTIC-COFRAME-LOCALIZED-CORE`. A change to the field content, phase symmetry, derivative order, potential, coframe coupling, benchmark, boundary conditions, tolerances, stability criterion, or source ledger creates a new model version.

**ASSUMPTIONS:**

1. W3-54 supplies one connected, oriented, time-oriented, nondegenerate post-Genesis coframe and its operational metric with signature `(-+++)`.
2. One localized organized excitation is represented by `Psi_O=(chi/sqrt(2)) exp(i theta_O)`, with `chi>=0` and exact global shift `theta_O -> theta_O+constant`. The phases `theta_O` and `theta_C`, and process time, are distinct.
3. The core sector is local, reversible, parity even, minimally coframe-coupled, second order in derivatives, and canonically normalized. Its minimal even polynomial with a massive vacuum, attractive binding, and large-amplitude boundedness is

   ```text
   V(chi)=m^2 chi^2/2-lambda chi^4/4+g chi^6/6,
   m^2>0, lambda>0, g>0.
   ```

4. The zero-amplitude state is the strict global vacuum: `a=g m^2/lambda^2>3/16`.
5. The localized solution is evaluated on a fixed non-backreacting Minkowski coframe in local orthonormal coordinates. The tested branch is spherical, positive, nodeless, and harmonic: `theta_O=omega tau`, `chi=chi(r)`.
6. The core calculation uses `c0=hbar=1`. Units are restored by `x=m r`, `Omega=omega/m`, and `f=sqrt(lambda) chi/m`.

**DOMAIN:** One phase-supported localized core of the mathematical Q-ball class on the regular post-Genesis continuum; the minimal canonical two-derivative `U(1)` sextic action; `a>3/16`; the harmonic finite-energy window; the nodeless spherical ground-state branch; and its fixed-coframe non-backreacting stability problem. The stage stops after one core, its action-derived stress, radius, and numerical stability evidence. Foundation-scale coefficient selection, collective-background locking, W3-56 environmental scaling, localized gravitational backreaction, particle identity, particle families, mass ratios, Koide/C3, the Planck hierarchy, strong fields, cosmology, and observations are outside this stage.

**CONVENTIONS:** W3-54 signature `(-+++)`; `x^0=tau` in natural units; `e=det(e^A_mu)>0`; `T^O_mu_nu=-(2/e) delta S_O/delta g^mu_nu`; and `j_O^mu=-chi^2 partial^mu theta_O`, so positive frequency gives `j_O^0=omega chi^2>0`. Dimensionless variables are `x=m r`, `f=sqrt(lambda) chi/m`, `Omega=omega/m`, and `a=g m^2/lambda^2`. Prime denotes `d/dx` after nondimensionalization.

**FREEDOM_LEDGER:** One complex scalar order parameter is added. `m>0` fixes the length/frequency unit; `lambda>0` fixes amplitude and the common energy/charge normalization; `a` is the only dimensionless shape coefficient. The exact class retains every `a>3/16`. The numerical witness fixes `a=1/4` before computation because it is a simple strict-vacuum point with exact lower existence edge `Omega_min=1/2`. The canonical frequency `Omega=4/5` and derivative stencil frequencies `{0.78,0.79,0.795,0.800,0.805,0.81,0.82}` are frozen before computation. Nothing is fitted to data or to a generated profile.

**DEPENDENCIES:** Hash-pinned W3-50 for the collective/ordinary phase distinction; hash-pinned W3-54 for the common coframe and Hilbert convention; hash-pinned W3-56 for the proper ordinary-phase role and fixed-background boundary; and hash-pinned W3-57 preregistration plus verified result for the missing-core-action diagnosis. Archived theories, Work 2, RefG-GR, observational data, Koide/C3, frequency-to-mass rules, and the selected W3-56 pressure readout are excluded from the dependency graph.

**METHOD:**

1. Vary the covariant action with respect to `chi`, `theta_O`, and `g^mu_nu`; derive the field equations, current, Hilbert tensor, local energy density, radial pressure, and tangential pressure.
2. Prove algebraically that `a>3/16` makes `chi=0` the strict global vacuum and that the complete harmonic existence window is `1-3/(16a)<Omega^2<1`.
3. Derive the dimensionless radial problem

   ```text
   f''+2 f'/x=(1-Omega^2)f-f^3+a f^5,
   f'(0)=0,
   f'(X)+(sqrt(1-Omega^2)+1/X)f(X)=0.
   ```

4. Solve the seven frozen frequencies by adaptive collocation, beginning at `Omega=0.8` from the frozen seed `1.8/(1+exp(x-4))` and continuing to the neighboring frequencies. Use `X=80`, an 801-point initial mesh, relative tolerance `1e-7`, and at most 100000 adaptive nodes. The accepted profile is nontrivial, positive, nodeless, and monotonically decreasing.
5. Recompute the canonical point at `X={60,80,100}` and tolerances `{1e-6,3e-7,1e-7}`. Evaluate integrals on Simpson grids `{4001,8001,16001}`. Require convergence of central amplitude, energy, charge, and charge-rms radius.
6. Cross-check the canonical point with a separate uniform-grid finite-difference nonlinear solve. The collocation profile may seed the nonlinear iteration; the finite-difference operator, boundary residual, and observables are recomputed independently.
7. Verify the equation residual, centre and Robin boundaries, Yukawa tail `f~C exp(-k x)/x` with `k=sqrt(1-Omega^2)`, the Nehari identity, the virial identity `E_grad+3(E_pot-E_phase)=0`, and the equivalent integrated Hilbert-stress balance.
8. Derive the reduced radial Hessian operators

   ```text
   L_+^(ell)=-d^2/dx^2+ell(ell+1)/x^2+1-Omega^2-3f^2+5a f^4,
   L_-^(ell)=-d^2/dx^2+ell(ell+1)/x^2+1-Omega^2-f^2+a f^4.
   ```

   Evaluate their lowest eigenvalues at spacings `{0.04,0.02,0.01}`. Check the `L_-^(0)` phase zero mode and absence of negative phase modes; exactly one negative `L_+^(0)` direction; the `L_+^(1)` translation zero mode and absence of angular negative modes; and a positive `ell=2` spectrum.
9. Solve the unreduced radial sensitivity equation `script_L_+^(0) z=2 Omega f`, equivalently `L_+^(0)(x z)=2 Omega x f` for the displayed reduced operator, where `z=partial f/partial Omega`, and compute `dQ/dOmega` from it. Cross-check the sign with centered five-point stencils at `h=0.01` and `h=0.005`. Combine a strictly negative slope with the Hessian index under the standard constrained solitary-wave stability theorem. Independently test `E/(mQ)<1`.
10. Run a manufactured-profile positive control and negative controls for a repulsive quartic, the localization edge `Omega^2>=1`, the vacuum boundary `a<=3/16`, phase-role collapse, stress relabelling, second-metric insertion, and benchmark mutation. Validate hashes and schema, write finite JSON, and stop.

**PASS_CONDITION:** Every exact action, variation, current, stress, vacuum, existence-window, nondimensionalization, radial-operator, and symmetry-mode identity passes. The canonical benchmark has a positive nodeless monotone finite-energy solution. Relative changes in central amplitude, energy, charge, and charge-rms radius are below `2e-4` across the registered domain/tolerance/quadrature checks; the independent finite-difference profile has weighted relative `L2` disagreement below `5e-4`; normalized equation, Nehari, virial, and stress residuals are below `2e-5`; the tail exponent differs from `sqrt(1-Omega^2)` by less than `2e-3`; the sensitivity and both finite-difference estimates give `dQ/dOmega<0`, with the two finite-difference estimates agreeing within `2e-2`; `E/(mQ)<1`; `L_+^(0)` has exactly one negative direction; the phase and translation eigenvalues converge to zero within `5e-4`; and all registered nonzero gaps exceed `1e-3`. Dependency, source-ledger, schema, and mutation controls must pass.

**FAIL_CONDITION:** Any exact identity, dependency, convergence, finite-energy, monotonicity, tail, integral balance, slope, spectral-index, zero-mode, positive-gap, source-ledger, schema, or mutation gate fails. A trivial or nodal profile, a hidden fitted parameter, phase-role collapse, second metric, duplicate source, or result-dependent benchmark change is a failure of this model version. A solver that cannot meet the registered numerical error budget yields `NUMERICALLY_INCONCLUSIVE`, not a physical rejection of the analytic class.

**FALSIFIER:** Core existence at the selected benchmark is falsified if no nontrivial regular finite-energy ground state survives the convergence and independent-solver gates. Fixed-coframe orbital-stability evidence fails if the converged ground state has an additional negative direction, lacks its symmetry zero modes, or has `dQ/dOmega>=0`. The separate free-quanta energetic bound fails if `E/(mQ)>=1`. The aggregate successful status requires all three results, but their decision meanings remain distinct. The analytic class statement is falsified by a nonzero symbolic residual in the vacuum or existence-window derivation.

**RESIDUAL:** Exact symbolic zero is required for the action variations, on-shell current divergence, Hilbert components, nondimensionalization, radial equation, vacuum threshold, existence edges, Nehari relation, virial/stress equivalence, and symmetry-mode identities. Numerical residuals are reported separately with the registered thresholds.

**ERROR_BOUND:** Algebraic statements have zero symbolic residual in the declared class. The numerical statement is restricted to the frozen benchmark, radial truncations, meshes, tolerances, and explicit error metrics. Infinite-domain error is controlled by domain convergence and the Yukawa-tail test. Floating-point results are `NUMERICAL_EVIDENCE`, never `COMPUTER_ASSISTED_PROOF` or interval-certified proof.

**VALIDITY_HEALTH:** Canonical kinetic terms are positive; the potential is bounded below; `a>3/16` supplies a strict zero-field global vacuum; the analytic window gives exponential decay; the ordinary-phase current is conserved; and the stress comes from the same covariant action. Orbital-stability evidence is restricted to the positive nodeless fixed-coframe ground state and the standard function-space hypotheses of the constrained stability theorem. Core coefficients remain selected constitutive input until a foundation-scale derivation fixes them.

**BRANCHES:** Analytic class: `a>3/16` and `1-3/(16a)<Omega^2<1`. Numerical branch: the positive nodeless spherical ground state around the frozen point `a=1/4`, `Omega=4/5`. Negative controls: repulsive quartic; `Omega^2>=1`; `a<=3/16`; removal of the sextic stabilizer; phase-role collapse; stress relabelling; second-metric insertion; and benchmark mutation.

**OBSERVABLE_MAP:** The action generates proper frequency `omega=m Omega`, charge density `j_O^0=omega chi^2`, energy density, radial and tangential stresses, total energy `E`, charge `Q`, and charge-rms radius `R_Q`. In physical units, `R_Q=x_Q/m`, `E=(4 pi m/lambda) mathcal_E`, `Q=(4 pi/lambda) q`, and `E/(mQ)=mathcal_E/q`. No particle species, observed mass, redshift, galactic, or cosmological observable is assigned.

**FORWARD_MODEL:** Input: the selected covariant action and frozen benchmark. Output: its spherical proper-frame profile, charge, energy, radius, stress balance, Hessian spectrum, and stability decision. There is no observational forward model or data fit.

**DATA_ROLE:** `N/A`: no observational or archived numerical data are read. The potential, benchmark, frequencies, and thresholds are preregistered theoretical inputs. Generated profiles are deterministic computational evidence.

**IDENTIFIABILITY:** The action identifies the PDE, current, stress, charge, energy, and dimensionless dependence on `(a,Omega)`. `m` and `lambda` set overall units; `a` controls shape. The benchmark can identify one dimensionless stable core. A foundation law is required to select `a`, set `m` and `lambda`, connect the core to `theta_C` and W3-56 background scaling, and identify a physical particle.

**BENCHMARK:** `a=1/4`, `Omega=4/5`, `X=80`. The analytic lower edge is `Omega_min=1/2`. Required outputs are one positive nodeless monotone profile; finite `mathcal_E`, `q`, and `x_Q`; Nehari, virial, and integrated-stress balance; tail exponent `3/5`; `dQ/dOmega<0`; `mathcal_E/q<1`; exactly one negative radial amplitude direction; phase and translation zero modes; and positive remaining registered gaps.

**CLOSURE_FLAGS:** Required true: `dependency_hashes_pinned_exact`, `w3_50_collective_phase_role_preserved_exact`, `w3_54_common_coframe_minimal_coupling_exact`, `ordinary_phase_u1_action_defined_exact`, `canonical_amplitude_gradient_present_exact`, `bounded_binding_sextic_present_exact`, `zero_vacuum_global_threshold_exact`, `euler_lagrange_equations_exact`, `ordinary_phase_current_exact`, `hilbert_stress_from_same_action_exact`, `one_source_ledger_no_duplicate_exact`, `dimensionless_radial_bvp_exact`, `analytic_existence_window_exact`, `finite_energy_ground_state_constructed_numerical`, `intrinsic_charge_radius_constructed_numerical`, `domain_tolerance_quadrature_convergence_pass`, `independent_finite_difference_crosscheck_pass`, `radial_nehari_virial_stress_tail_checks_pass`, `hessian_operators_exact`, `phase_and_translation_zero_modes_numerical`, `single_unconstrained_L_plus_negative_direction_numerical`, `negative_charge_slope_numerical`, `free_quantum_decay_bound_numerical`, `converged_numerical_orbital_stability_evidence`, `registered_contract_keysets_exact`, `mutation_controls_pass`, and `aggregate_gate_pass`. Required false: `core_action_from_nodes_derived`, `benchmark_a_from_foundation_derived`, `m_and_lambda_from_foundation_derived`, `neutral_real_oscillon_derived`, `theta_O_theta_C_lock_derived`, `w3_56_background_scaling_from_core_derived`, `P_F_from_core_stress_derived`, `square_pressure_law_from_core_stress_derived`, `localized_gravitational_backreaction_derived`, `physical_particle_identity_derived`, `all_particle_families_universalized`, `particle_mass_spectrum_derived`, `Koide_or_C3_used`, `Planck_hierarchy_derived`, `strong_field_or_2PN_completed`, `cosmological_history_modified`, and `observational_likelihood_evaluated`.

**CROSSCHECK:** Polar and complex-field variations must agree. The radial equation is derived from both the covariant equation and reduced fixed-frequency action. Nehari and virial identities are checked against the integrated Hilbert stress. Adaptive collocation is checked by an independent finite-difference solve. Fixed-coframe orbital stability combines the Hessian index, symmetry zero modes, the sensitivity equation, and two charge-slope stencils. The free-quanta energy bound is tested independently.

**PROVENANCE:** Frozen UTF-8 LF preregistration with SHA-256 pins for W3-50, W3-54, W3-56, W3-57 preregistration, and W3-57 result; deterministic Python/SymPy/NumPy/SciPy; no network or archived-theory dependency; runtime source/result hashes; strict finite JSON; atomic result/checksum writes. Analytic existence follows S. Coleman, *Q-balls*, Nuclear Physics B 262 (1985) 263–283, DOI `10.1016/0550-3213(85)90286-X`. Stability logic follows M. Grillakis, J. Shatah, and W. Strauss, *Stability theory of solitary waves in the presence of symmetry I*, Journal of Functional Analysis 74 (1987) 160–197, DOI `10.1016/0022-1236(87)90044-9`.

**FILES:** `README.md`, `w3_58_one_oscillon_coframe_localized_core_preregistration.md`, `w3_58_one_oscillon_coframe_localized_core.py`, `w3_58_result.json`, and `w3_58_result.sha256`.

## Decision semantics and stop rule

Successful status:

```text
PASS_CONDITIONAL_EXACT_MINIMAL_COFRAME_U1_CORE_ACTION_AND_ANALYTIC_EXISTENCE_WINDOW__CONVERGED_NUMERICAL_FINITE_ENERGY_ORBITALLY_STABLE_SPHERICAL_GROUND_STATE_EVIDENCE__FOUNDATION_COEFFICIENT_SELECTION_BACKGROUND_LOCK_BACKREACTION_AND_PARTICLE_IDENTITY_OPEN
```

The successful stage establishes one action-generated phase-supported localized core and its fixed-coframe numerical stability evidence. It stops there.

### Audit amendment

After the first frozen execution, a scope audit separated the existence,
orbital-stability, and free-quanta decision semantics; corrected the reduced
versus unreduced sensitivity notation; and renamed one closure key from
`single_negative_constrained_direction_numerical` to
`single_unconstrained_L_plus_negative_direction_numerical`. The original
preregistration SHA-256 was
`7974fa60b1d0cf420bceb8fad9e2cd2a913d263b09fe41c603ac8af8428108f2`.
This audit amendment changes no field content, action, benchmark, frequency,
threshold, solver, pass gate, or numerical result.
