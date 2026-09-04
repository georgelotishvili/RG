# W3-72 — Horizon-Crossing Ordinary-Phase Current

**CLAIM_ID:** W3_72_HORIZON_CROSSING_MATERIAL_CURRENT

**CLAIM:** On the single post-Genesis metric already selected by W3-54 and continued by W3-64, the unchanged W3-58 complex ordinary-phase action has a horizon-regular, nonstatic matter-current handoff. In the ingoing Painlevé–Gullstrand coframe supplied by W3-71, its amplitude equation, phase equation, Noether current, Hilbert stress, characteristic cone, charge balance, and Killing-energy flux remain finite at the Schwarzschild horizon. On the explicitly declared future-timelike phase-gradient branch, the normalized ordinary-phase current necessarily crosses the future horizon inward. Smooth horizon-crossing initial data form an open local class for the regular semilinear scalar system. This establishes the local dynamical handoff; it does not construct a stationary horizon-bound oscillon, a globally backreacting collapse solution, a regular interior, or a singularity-resolution theorem.

**TYPE:** EXACT_ACTION_DERIVED_LOCAL_HORIZON_HANDOFF_WITH_SYMBOLIC_AND_INDEPENDENT_CHART_AUDIT.

**MODEL_VERSION:** W3-72-v1.0-HORIZON-CROSSING-ORDINARY-PHASE-CURRENT.

## Assumptions

1. W3-54 supplies one connected, oriented, time-oriented, nondegenerate post-Genesis coframe and one operational metric with signature (-,+,+,+).
2. W3-58 supplies the unchanged localized ordinary-phase field

       Psi_O=(chi/sqrt(2)) exp(i theta_O)

   and the action

       S_O=-integral sqrt(-g) [
          (1/2) g^(mu nu) partial_mu chi partial_nu chi
          +(1/2) chi^2 g^(mu nu) partial_mu theta_O partial_nu theta_O
          +V(chi)
       ] d^4x,

       V(chi)=(m^2/2)chi^2-(lambda/4)chi^4+(g/6)chi^6.

3. W3-64 supplies the same Einstein metric and the once-only localized Hilbert source T^O_mu_nu. No second metric, duplicate localized source, readout source, or new gravitational operator is introduced.
4. W3-71 supplies the future-horizon-regular ingoing Painlevé–Gullstrand coframe

       e^0=dT,
       e^1=dr+v(r)dT,
       v(r)=sqrt(r_s/r),

   on a spherical annulus r>0 intersecting r=r_s.
5. The material-worldline interpretation is restricted to chi>0 and to the future-timelike ordinary-phase-gradient branch

       Pi_theta>0,
       X_theta=Pi_theta^2-Phi_theta^2>0.

   The action does not assert that its Noether current is timelike on every solution.
6. The metric is frozen to the inherited Schwarzschild/PG geometry for the exact horizon regularity, characteristic, and local flux audit. The stress derived here is the unique source for the later coupled Einstein evolution; that backreacting evolution is not solved in this stage.
7. The Schwarzschild mass M_bg that fixes r_s is a background-boundary role. It is not identified with the ADM mass, charge, or energy of the W3-64 horizonless oscillon witness.

## Domain and conventions

The exact domain is a smooth spherical horizon-crossing patch r in (r_s-epsilon,r_s+epsilon), with r_s>0 and epsilon<r_s, together with any compact radial shell contained in r>0 for the integrated balance. Angular dependence may be retained in the principal symbol, while displayed evolution equations use the spherical sector. W3-58 natural units c0=hbar=1 are retained and r_s=2 G M_bg.

For every scalar A define the regular coframe derivatives

    Pi_A=(partial_T-v partial_r)A,
    Phi_A=partial_r A.

The dual frame is E_hat0=partial_T-v partial_r and E_hat1=partial_r. The W3-58 current convention is

    j_O^mu=-chi^2 partial^mu theta_O,

so positive local phase frequency has j_O^hat0>0. The physical inward direction has decreasing areal radius r. The Noether current is an ordinary-phase charge current; it is not silently relabelled as invariant mass flux. On the timelike branch,

    n_O=chi^2 sqrt(X_theta),
    u_O^mu=j_O^mu/n_O,
    u_O^mu u^O_mu=-1.

## Branches

The accepted material branch has chi>0, Pi_theta>0, and X_theta>0 on a smooth horizon-crossing patch. X_theta=0 is its null boundary. X_theta<0 remains a valid field configuration where defined, but it has no timelike material-worldline interpretation. The independent rain witness uses Phi_theta=0. The flat regression is r_s/r to 0; the future-horizon benchmark is r=r_s. Static horizonless W3-64 equilibria and nonstatic horizon-crossing W3-72 data are distinct solution branches of the same action.

## Freedom ledger

No new coefficient, field, action term, metric, source, response function, fit parameter, cutoff, or observation is added. The exact variables are inherited chi, theta_O, g_mu_nu, and the W3-58 constants m, lambda, g. The horizon radius r_s labels the inherited Schwarzschild witness. Initial data are free smooth Cauchy data subject only to the declared local regularity and future-timelike inequalities; they are not fitted.

## Dependencies

Every dependency is frozen by exact relative path and SHA-256:

    CODES.md
    27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41

    RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md
    6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879

    RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_result.json
    ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991

    RefG/work 3/Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_one_oscillon_coframe_localized_core_preregistration.md
    ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db

    RefG/work 3/Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_result.json
    cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5

    RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field_preregistration.md
    25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1

    RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/w3_64_result.json
    b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b

    RefG/work 3/Strong_Field/W3-71_Horizon_Material_Scale_Separation/w3_71_horizon_material_scale_separation_preregistration.md
    45a9a9eed95a2d927a601f6b4e0822994da93176f1c25fe49ff2431bb35e9f4a

    RefG/work 3/Strong_Field/W3-71_Horizon_Material_Scale_Separation/w3_71_result.json
    5aeeed4a963e1a03769861f5b38e564a74ec718ee1a19048b37ee7affa72be81

Archived theory, Work 2, RefG-GR, observational files, and the internet are excluded from the executable dependency graph.

## Typed role and source ledger

    metric_ids: (g)
    localized T_O: HILBERT_SOURCE, multiplicity 1
    localized T_C: HILBERT_SOURCE, multiplicity 0
    localized readout: HILBERT_SOURCE, multiplicity 0
    j_O as an additional Einstein RHS source: multiplicity 0
    j_O: ORDINARY_PHASE_NOETHER_CURRENT
    M_bg and r_s: BACKGROUND_HORIZON_BOUNDARY_PARAMETERS
    Q_O and E_O: DYNAMICAL_MATTER_OBSERVABLES
    R_O_loc: INTRINSIC_LOCAL_CHARGE_MOMENT_RADIUS
    R_O_ext: EXTERNAL_RULER_ASSIGNMENT
    p_L: PASSIVE_EXTERNAL_RULER_FACTOR, absent from local dynamics

The intrinsic W3-58 profile and R_O_loc are unchanged by passive readout. W3-71's R_O_ext is a separate ruler conversion; no factor p_L multiplies chi, its local derivatives, its action, or R_O_loc. M_bg is not equated to the energy or ADM mass of the W3-64 horizonless equilibrium.

## Derived equations frozen before execution

The action equations are

    box chi-chi (partial theta_O)^2-V'(chi)=0,
    nabla_mu(chi^2 partial^mu theta_O)=0,

with the current and stress

    j_O^mu=-chi^2 partial^mu theta_O,

    T^O_mu_nu=
      partial_mu chi partial_nu chi
      +chi^2 partial_mu theta_O partial_nu theta_O
      -g_mu_nu [
         (1/2)(partial chi)^2
         +(1/2)chi^2(partial theta_O)^2
         +V
       ].

In the PG chart,

    j_O^T=chi^2 Pi_theta,
    j_O^r=-chi^2(v Pi_theta+Phi_theta),

    partial_T(r^2 j_O^T)+partial_r(r^2 j_O^r)=0,

and

    box chi=
      -partial_T Pi_chi
      +(1/r^2)partial_r[r^2(v Pi_chi+Phi_chi)].

The spherical first-order amplitude system is

    partial_T chi=Pi_chi+v Phi_chi,
    partial_T Phi_chi=partial_r(Pi_chi+v Phi_chi),
    partial_T Pi_chi=
      (1/r^2)partial_r[r^2(v Pi_chi+Phi_chi)]
      +chi(Pi_theta^2-Phi_theta^2)-V'(chi).

The phase equation is retained in conservative form,

    partial_T(r^2 chi^2 Pi_theta)
      -partial_r[r^2 chi^2(v Pi_theta+Phi_theta)]=0,

with partial_T theta_O=Pi_theta+v Phi_theta and
partial_T Phi_theta=partial_r(Pi_theta+v Phi_theta).

At chi=0, polar variables are replaced by the two regular Cartesian components of Psi_O. The underlying Cartesian equations are two semilinear wave equations with the same metric principal part; no division by chi is permitted at a polar-coordinate zero.

## Method

1. Hash-audit CODES.md and the W3-54, W3-58, W3-64, and W3-71 records. Validate their successful status and exact scope boundaries.
2. Reconstruct the PG metric, inverse, determinant, dual frame, scalar d'Alembertian, and radial null speeds directly from the coframe.
3. Re-derive the W3-58 amplitude equation, phase equation, current, and Hilbert stress on this chart without changing the action.
4. Prove the coordinate/frame current dictionary, its norm, the normalized material velocity, and the exact horizon sign. Parameterize the complete future-timelike radial branch by

       Pi_theta=q cosh(eta),
       Phi_theta=q sinh(eta),
       q>0,

   so that at r=r_s,

       j_O^r=-chi^2 q exp(eta)<0.

5. Verify local charge balance on a shell:

       dQ_[r1,r2]/dT=-4 pi [r^2 j_O^r]_(r1 to r2).

6. Verify that the radial principal block is symmetric hyperbolic. For U=(Pi,Phi),

       partial_T U=A(v) partial_r U+lower order,
       A(v)=[[v,1],[1,v]].

   With this sign convention the coordinate characteristic speeds are -v+1 and -v-1, identical to the PG radial null speeds. At the future horizon they are 0 and -2 and every evolution coefficient is finite.
7. Verify that T=constant PG slices are spacelike across the horizon, and that finite smooth initial data with chi>0, Pi_theta>0, and X_theta>0 define an open local horizon-crossing initial-data class. The polynomial potential is lower order and does not change the cone.
8. Compute the local orthonormal energy density and stresses, the radial null-energy contractions, and the future-horizon Killing-energy flux. The absorbed horizon flux is

       T_TT at r_s
       =(Pi_chi+Phi_chi)^2
        +chi^2(Pi_theta+Phi_theta)^2
       >=0.

9. Cross-check the metric and horizon flux in ingoing Eddington–Finkelstein coordinates, smoothly related by dV=dT+dr/(1+v).
10. Verify the unit timelike PG rain congruence u^mu=(1,-v,0,0), its finite proper crossing time, and an exact continuity-only packet

       n(T,r)=r^(-3/2) F(r^(3/2)+(3/2)sqrt(r_s)T).

    This packet is an independent conservation-law witness only. It is not promoted to a solution of the amplitude equation and is not identified with the intrinsic oscillon profile.
11. Prove the isolated stationary-crossing exclusion: with zero outer flux, a time-independent exterior charge would require j_O^r(r_s)=0, contradicting the strict inward flux of every nonzero future-timelike horizon current.
12. Verify that the W3-71 scale connection is not promoted to a global scalar ruler on the nonstatic rain branch. Its curvature witness is nonzero, so no nonstatic global p_t is used.
13. Run every registered mutation through the same evaluator, validate the exact three-file package, emit finite JSON, and stop.

For step 12 the frozen rain-branch obstruction is

    a_mu=0,
    Theta=-3 sqrt(r_s)/(2 r^(3/2)),
    W_T=3 sqrt(r_s)/(4 r^(3/2)),
    W_r=0,
    F_Tr=partial_T W_r-partial_r W_T
        =9 sqrt(r_s)/(8 r^(5/2)) != 0.

This nonintegrability blocks a global mixed-branch scalar p_t; it does not obstruct the local coframe, current, stress, or scalar evolution.

## Cross-check

The PG metric is reconstructed independently from its coframe and transformed to the ingoing EF chart. The current is derived once from the inverse metric and again from orthonormal-frame components. The characteristic speeds are derived once from the scalar principal symbol and again from radial metric null curves. The horizon energy flux is derived from the Hilbert tensor and checked as a sum of regular-frame squares. The exact rain packet checks the phase continuity equation independently, while its generically nonzero amplitude residual prevents promotion to a full scalar solution. Every negative control is evaluated by the same production evaluator.

## Files

The package is recursively restricted to exactly:

    w3_72_horizon_crossing_material_current_preregistration.md
    w3_72_horizon_crossing_material_current.py
    w3_72_result.json

No subdirectory, cache, plot, temporary output, copied dependency, or auxiliary note is permitted.

## Pass condition

Every dependency, metric, inverse, determinant, dual-frame, action equation, current, norm, material normalization, charge-balance, first-order evolution, principal-symbol, characteristic-speed, local-slice, stress, NEC, energy-flux, EF/PG cross-chart, rain-congruence, proper-time, continuity-witness, stationary-exclusion, source-ledger, profile-separation, scale-domain, schema, package, and mutation gate passes with exact symbolic zero residual. All required true flags are exactly true and all required false flags are exactly false.

## Fail condition

The model version fails if any exact identity or dependency fails; if a 1/(1-r_s/r) pole is needed in the horizon-regular chart; if the scalar cone differs from the inherited null cone; if the current sign or radial term is changed; if the material interpretation is asserted outside X_theta>0 and Pi_theta>0; if a continuity-only packet is called a full scalar solution; if passive ruler conversion is inserted into the intrinsic local profile; if a second metric or duplicate source is introduced; or if a local handoff is promoted to global collapse, interior regularity, geodesic completeness, or singularity resolution.

## Falsifier and residual

This exact handoff is falsified by a nonzero symbolic residual in the PG metric reconstruction, action equations, current conservation, Hilbert stress, characteristic factorization, EF cross-check, or horizon flux identities. It is also falsified if a smooth future-timelike nonzero radial current can have zero or outward j_O^r on the future Schwarzschild horizon under the declared sign conventions. Exact algebra requires zero residual; strict signs follow from q>0, chi>0, and exp(eta)>0.

## Error bound and validity health

There is no numerical approximation and no observational likelihood. All accepted identities are symbolic. Local existence is restricted to the standard smooth semilinear hyperbolic initial-value domain on a PG spacelike slice. The potential is smooth and lower order. The future-timelike condition is an open branch condition, not an automatic theorem about arbitrary U(1) field configurations. Finite field amplitude alone is insufficient: the regular-frame first derivatives and stress must also be finite.

## Observable map, forward model, and data role

The outputs are the local ordinary-phase charge density, radial charge flux, normalized material velocity on the timelike branch, regular-frame energy and stresses, horizon absorbed charge, and horizon absorbed Killing energy. The forward model maps smooth local scalar initial data to the regular hyperbolic evolution problem on the inherited metric. No observational data, archive, likelihood, calibration, or parameter fit enters this stage.

## Identifiability and benchmark

The action uniquely fixes the local equations, current, stress, and cone. It does not identify every solution as a particle, fix the full infalling profile, or determine a global black-hole endpoint. The exact benchmark is the symbolic Schwarzschild/PG horizon r=r_s with a representative open-set center point

    chi=A>0, Pi_theta=q>0, Phi_theta=0,

and finite Pi_chi, Phi_chi. This point has a timelike current, strict inward horizon charge flux, and strictly positive phase contribution to the absorbed energy flux.

## Closure flags

Required true:

    dependency_hashes_exact
    upstream_status_and_scope_exact
    one_metric_one_localized_source_exact
    w3_58_action_unchanged_exact
    pg_metric_inverse_volume_exact
    pg_dual_frame_dictionary_exact
    scalar_amplitude_equation_exact
    ordinary_phase_equation_exact
    ordinary_phase_current_exact
    current_coordinate_frame_dictionary_exact
    timelike_material_domain_exact
    normalized_material_velocity_exact
    horizon_inward_current_exact
    charge_balance_exact
    rain_congruence_exact
    finite_proper_horizon_crossing_exact
    continuity_witness_exact
    continuity_witness_not_full_scalar_solution_exact
    scalar_box_pg_exact
    first_order_scalar_system_exact
    principal_symbol_exact
    characteristic_speeds_exact
    horizon_hyperbolicity_regular_exact
    pg_cauchy_slice_spacelike_exact
    local_initial_data_open_set_exact
    polar_cartesian_domain_guard_exact
    hilbert_stress_exact
    regular_frame_stress_finite_exact
    horizon_energy_flux_nonnegative_exact
    scalar_nec_exact
    isolated_stationary_crossing_no_go_exact
    nonstatic_scale_connection_not_promoted_exact
    intrinsic_profile_not_passively_rescaled_exact
    potential_lower_order_exact
    mutation_controls_pass
    g0_goal_pass
    g1_conventions_pass
    g2_action_current_pass
    g3_horizon_hyperbolicity_pass
    g4_independent_crosscheck_pass
    g5_limits_regression_pass
    g6_physical_scope_pass
    g7_observation_not_applicable_exact
    g8_export_not_applicable_exact
    package_clean_pass
    aggregate_gate_pass

Required false:

    ordinary_phase_current_automatically_timelike
    noether_charge_identified_as_mass_flux
    continuity_witness_full_scalar_solution
    full_scalar_amplitude_equation_solution_constructed
    stationary_bound_oscillon_horizon_solution_derived
    intrinsic_oscillon_profile_rescaled
    dynamical_profile_rigidity_derived
    background_horizon_mass_identified_as_oscillon_mass
    nonstatic_global_scale_scalar_derived
    global_infalling_oscillon_solution_derived
    dynamic_einstein_backreaction_solved
    collapse_evolution_completed
    regular_black_hole_interior_derived
    singularity_resolution_completed
    geodesic_completeness_derived
    new_gravity_operator_introduced
    second_metric_introduced
    duplicate_localized_source_introduced
    new_observation_tested
    canon_changed
    intuitive_files_changed

## Frozen mutation registry

    pg_shift_removed -> pg_shift_coefficient
    current_sign_flipped -> current_sign
    phase_radial_term_removed -> phase_radial_coefficient
    timelike_domain_dropped -> require_timelike_branch
    potential_promoted_to_principal -> potential_principal_coefficient
    horizon_flux_forced_zero -> horizon_flux_rule
    stress_not_from_action -> stress_rule
    duplicate_metric_source -> metric_ids, localized_source_ledger
    profile_passively_rescaled -> profile_scale_power
    nonstatic_scale_scalar_promoted -> accepted_scale_domains
    continuity_witness_promoted_full_solution -> continuity_witness_role
    background_mass_identified_with_oscillon -> mass_role
    global_interior_overclaim -> promoted_claims

## Gate registry

- G0_GOAL: frozen preregistration, hashes, upstream status, exact package, and claim scope.
- G1_CONVENTIONS: signature, frame, current sign, source ledger, background-mass role, and charge/energy role separation.
- G2_ACTION_CURRENT: action equations, current, material normalization, stress, conservation, and flux.
- G3_HORIZON_HYPERBOLICITY: regular PG evolution, principal cone, characteristic speeds, spacelike slice, and local initial-data domain.
- G4_INDEPENDENT_CROSSCHECK: EF chart, rain congruence, proper crossing, and continuity-only packet.
- G5_LIMITS_AND_REGRESSION: flat limit, horizon value, W3-58 action, W3-64 source, and W3-71 geometry.
- G6_PHYSICAL_SCOPE: inward timelike crossing, nonnegative energy absorption, nonstationarity, profile separation, and nonintegrable scale-connection boundary.
- G7_OBSERVATION: not applicable; no data are read.
- G8_EXPORT: not applicable; no article, intuitive monograph, canon, or release artifact is changed.

## Provenance and references

The package uses deterministic Python and SymPy, UTF-8 text, SHA-256 dependency pins, strict finite JSON, one preregistration, one verifier, and one result. It reads no archived theory and performs no network or observational operation. Horizon-regular chart identities are cross-checked against D. Finkelstein, Physical Review 110 (1958) 965, DOI 10.1103/PhysRev.110.965; K. Martel and E. Poisson, American Journal of Physics 69 (2001) 476, arXiv:gr-qc/0001069, DOI 10.1119/1.1336836; D. Philipp and V. Perlick, International Journal of Modern Physics D 24 (2015) 1542006, arXiv:1503.08361, DOI 10.1142/S0218271815420067; and J. Barranco et al., Physical Review D 96 (2017) 024049, arXiv:1704.03450, DOI 10.1103/PhysRevD.96.024049.

## Successful status

    PASS_EXACT_ACTION_DERIVED_HORIZON_REGULAR_NONSTATIC_ORDINARY_PHASE_CURRENT_AND_LOCAL_INITIAL_VALUE_HANDOFF__FINITE_INWARD_CHARGE_NONNEGATIVE_ENERGY_FLUX_AND_MATCHED_CHARACTERISTIC_CONE_ON_THE_INHERITED_ONE_METRIC__GLOBAL_BACKREACTION_INTERIOR_AND_SINGULARITY_NOT_SOLVED

The successful stage establishes the exact local horizon-crossing handoff and stops there.
