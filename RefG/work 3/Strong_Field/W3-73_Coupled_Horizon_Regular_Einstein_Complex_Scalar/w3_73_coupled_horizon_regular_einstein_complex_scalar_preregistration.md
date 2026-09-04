# W3-73 — Coupled Horizon-Regular Einstein–Complex-Scalar Evolution

**CLAIM_ID:** W3_73_COUPLED_HORIZON_REGULAR_EINSTEIN_COMPLEX_SCALAR

**CLAIM:** The unchanged W3-54 Einstein–Hilbert geometry and unchanged W3-58 complex ordinary-phase action admit a fully coupled spherical constrained evolution system in a generalized ingoing Painlevé–Gullstrand coframe. The metric, Hilbert source, scalar evolution, ordinary-phase current, Misner–Sharp mass balances, and future outer marginal-surface fluxes are regular at `zeta=1`. On the nondegenerate outer branch, positive horizon-crossing scalar flux increases the Misner–Sharp mass, advances the marginal radius, and increases its area. The intrinsic local field is evolved by its action and is never multiplied by a passive ruler factor. This stage closes the local coupled initial-value handoff; global collapse, a global event horizon, a regular centre or interior, geodesic completion, and singularity resolution remain outside the result.

**TYPE:** EXACT_ACTION_DERIVED_LOCAL_COUPLED_SPHERICAL_CONSTRAINED_EVOLUTION_WITH_SYMBOLIC_GEOMETRY_MATTER_AND_FLUX_AUDIT.

**MODEL_VERSION:** W3-73-v1.0-COUPLED-HORIZON-REGULAR-EINSTEIN-COMPLEX-SCALAR.

## Target and stopping rule

The target is the smallest action-derived system that removes W3-72's frozen-background boundary. It must derive the spherical metric constraints and evolution from the same Einstein equation that receives the W3-58 Hilbert tensor exactly once, retain a regular scalar Cauchy system at a future marginal sphere, derive its mass, charge, and area fluxes, reproduce the W3-58, W3-64, and W3-72 limits, and stop. No numerical collapse, centre integration, compact-object fit, waveform, ray image, or new constitutive action is opened.

## Assumptions

1. W3-54 supplies one connected, oriented, time-oriented, nondegenerate post-Genesis coframe, one metric with signature `(-,+,+,+)`, and the Einstein–Hilbert gravitational operator.
2. W3-58 supplies the unchanged canonical complex ordinary-phase action and bounded sextic potential.
3. W3-64 supplies the once-counted localized Hilbert source, the static horizonless Einstein–scalar branch, the null-energy identity, and the Penrose trapped-surface boundary.
4. W3-67 fixes the role boundary: a passive material-scale readout has no Euler–Lagrange equation and cannot alter a solution; an active foundation response requires a separately derived covariant action or exact elimination.
5. W3-71 separates temporal readout, spatial ruler projection, and intrinsic local oscillon profile. Its `p_t` and `p_L` are absent from the nonstatic local action used here.
6. W3-72 supplies the regular nonstatic material-current handoff on the frozen Schwarzschild/PG background.
7. The coupled calculation is local on a smooth spherical annulus with `r>0`, `sigma>0`, and the ingoing branch `zeta>0`. The annulus intersects `zeta=1` and excludes the centre `r=0` and the degenerate outer condition `D_H=0`.
8. Smooth scalar and metric fields and the displayed constraints are assumed on the local patch. The potential coefficients retain the W3-58 healthy domain.

## Domain and conventions

Use `c0=hbar=1`, keep `G>0`, and reserve `sigma(T,r)>0` for the generalized PG lapse so it is not confused with W3-64's dimensionless gravitational coupling `alpha`. The coframe is

    e^hat0=sigma dT,
    e^hat1=dr+sigma zeta dT,

and the metric is

    ds^2=-sigma^2(1-zeta^2)dT^2
         +2 sigma zeta dT dr+dr^2+r^2 dOmega_2^2.

The future unit normal and radial unit vector are

    n=sigma^(-1) partial_T-zeta partial_r,
    s=partial_r.

For each real scalar component define

    Pi_A=n(phi_A),
    Phi_A=partial_r phi_A,

with `A in {1,2}`. The complex field and amplitude are

    Psi_O=(phi_1+i phi_2)/sqrt(2),
    chi^2=phi_1^2+phi_2^2.

The potential and its Cartesian gradient are

    V=m_s^2 chi^2/2-lambda chi^4/4+g_6 chi^6/6,
    V_,A=(m_s^2-lambda chi^2+g_6 chi^4)phi_A.

The Misner–Sharp mass is

    m_MS=r zeta^2/(2G),

and `F=1-2Gm_MS/r=1-zeta^2`. The surface `zeta=1` is a future marginally outer trapped sphere in this local spherical foliation. `D_H=1-2G partial_r m_MS|_H>0` selects the nondegenerate outer branch.

## Branches

- `LOCAL_INGOING_GPG`: `r>0`, `sigma>0`, `zeta>0`.
- `FUTURE_OUTER_MARGINAL`: `zeta=1`, `D_H>0`.
- `TIMELIKE_ORDINARY_PHASE`: `q>0`, `q^2>s_O^2`, where `q` and `s_O` are defined below.
- `EXCISION_INTERIOR`: `zeta>1`, where both radial scalar characteristics point toward decreasing areal radius.
- `W3_64_STATIC_REGRESSION`: `N=1-zeta^2>0`, zero radial charge flux.
- `W3_72_TEST_FIELD_REGRESSION`: metric backreaction bookkeeping is removed after deriving the coupled equations, then `sigma=1` and `zeta=sqrt(r_s/r)`.
- `W3_58_FLAT_REGRESSION`: `G->0`, `sigma->1`, `zeta->0`.

The centre, degenerate marginal surfaces, rotating fields, nonspherical gravitational radiation, global event-horizon location, and complete collapse spacetime are separate branches.

## Freedom ledger

No new field, coefficient, response function, activation scale, equation of state, cutoff, fit parameter, metric, or source is added. The dynamical fields are the inherited metric and the two Cartesian components of the inherited complex scalar. `sigma` is lapse gauge data fixed by one radial normalization, `zeta` is the ingoing metric shift/compactness variable, and `m_MS` is derived from `zeta`. Smooth local scalar initial data, one compatible mass boundary datum, and one lapse normalization are Cauchy/gauge data, not fitted theory parameters.

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

    RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_foundation_strong_field_response_preregistration.md
    31e6520d9b7917413b9f2978291b4a77f067abe8dd3d6a9e89e1b2cfb699da11

    RefG/work 3/Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_result.json
    659bdfe171a8279b465fdd49eaf590755da22a7522a83053a4a06450fd745385

    RefG/work 3/Strong_Field/W3-71_Horizon_Material_Scale_Separation/w3_71_horizon_material_scale_separation_preregistration.md
    45a9a9eed95a2d927a601f6b4e0822994da93176f1c25fe49ff2431bb35e9f4a

    RefG/work 3/Strong_Field/W3-71_Horizon_Material_Scale_Separation/w3_71_result.json
    5aeeed4a963e1a03769861f5b38e564a74ec718ee1a19048b37ee7affa72be81

    RefG/work 3/Strong_Field/W3-72_Horizon_Crossing_Material_Current/w3_72_horizon_crossing_material_current_preregistration.md
    29c0bbad8eee945820efe1eb7c335597bfe2c7f136bf02fdf2bd7e7bca6769a7

    RefG/work 3/Strong_Field/W3-72_Horizon_Crossing_Material_Current/w3_72_result.json
    269f4de4a7c17c7a0947d2d20288e3003beaa2a159386e94687ba39a5c4736a9

Archived theory, Work 2, RefG-GR, observational files, and external data are excluded from the executable dependency graph.

## Typed role and source ledger

    metric_ids: (g)
    Einstein geometric operator: multiplicity 1
    localized T_O from delta S_O/delta g: multiplicity 1
    localized T_C: multiplicity 0
    p_t, p_L, P_F, readout connection: Hilbert-source multiplicity 0
    j_O as an additional Einstein source: multiplicity 0
    sigma: DYNAMICAL_GPG_LAPSE_GAUGE, not nonstatic p_t
    zeta: DYNAMICAL_INGOING_SHIFT_AND_COMPACTNESS
    m_MS: DERIVED_MISNER_SHARP_MASS
    chi and Psi_O: INTRINSIC_LOCAL_FIELDS
    p_L: PASSIVE_EXTERNAL_RULER_FACTOR, absent from local dynamics

The scale hierarchy is kept covariant: a constant reference rescaling is a unit/gauge normalization; first coframe derivatives enter connection and acceleration; relative deformation is read from curvature and geodesic deviation. No scalar foundation-pressure law is inferred from `sigma` or `zeta` on the nonstatic branch.

## Frozen equations

The inherited action is

    S=integral sqrt(-g) R/(16 pi G) d^4x
      -integral sqrt(-g)[
          (1/2) sum_A (partial phi_A)^2+V(chi)
       ]d^4x.

The regular first-order scalar system is

    partial_T phi_A=sigma(Pi_A+zeta Phi_A),
    partial_T Phi_A=partial_r[sigma(Pi_A+zeta Phi_A)],
    partial_T Pi_A=
      r^(-2) partial_r[sigma r^2(Phi_A+zeta Pi_A)]
      -sigma V_,A.

Its auxiliary constraint `C_A=Phi_A-partial_r phi_A` obeys `partial_T C_A=0`. The radial characteristic speeds are

    c_plus=sigma(1-zeta),
    c_minus=-sigma(1+zeta),

which equal the metric null speeds. At `zeta=1` they are `0` and `-2 sigma`; at `zeta>1` both are negative.

The orthonormal Hilbert components are

    rho=(1/2)sum_A(Pi_A^2+Phi_A^2)+V,
    S=sum_A Pi_A Phi_A,
    p_r=(1/2)sum_A(Pi_A^2+Phi_A^2)-V,
    p_T=(1/2)sum_A(Pi_A^2-Phi_A^2)-V.

Here `S=T_hat0hat1`; the ADM radial momentum density is `-S` with the stated extrinsic-curvature convention.

The independent Einstein relations reduce to

    partial_r ln sigma=-4 pi G r S/zeta,

    partial_r zeta=
      4 pi G r(rho/zeta+S)-zeta/(2r),

    partial_T zeta=
      sigma zeta partial_r zeta-partial_r sigma
      +sigma zeta^2/(2r)+4 pi G sigma r p_r.

Equivalently, the Misner–Sharp balances are

    partial_r m_MS=4 pi r^2(rho+zeta S),

    partial_T m_MS=4 pi sigma r^2 sum_A
      (Pi_A+zeta Phi_A)(zeta Pi_A+Phi_A).

The radial and temporal mass balances are compatible on the scalar equations and metric constraints. The remaining angular Einstein equation follows from the contracted Bianchi identity and on-shell Hilbert-stress conservation on the regular local branch.

Define the Cartesian ordinary-phase densities

    q=phi_1 Pi_2-phi_2 Pi_1,
    s_O=phi_1 Phi_2-phi_2 Phi_1.

Then

    j_O^T=q/sigma,
    j_O^r=-(zeta q+s_O),
    j_O^mu j^O_mu=-q^2+s_O^2,

and

    partial_T(r^2 q)-partial_r[sigma r^2(zeta q+s_O)]=0.

On `q>0`, `q^2>s_O^2`, the current is future timelike. At `zeta=1`, `j_O^r=-(q+s_O)<0`.

Let a smooth marginal tube satisfy `H(T,r)=r-2Gm_MS(T,r)=0` and `D_H=partial_r H|_H>0`. Then

    partial_T m_MS|_H
      =4 pi sigma_H r_H^2 sum_A(Pi_A+Phi_A)^2 >=0,

    dot(r_H)=2G partial_T m_MS|_H/D_H >=0,
    dot(A_H)=8 pi r_H dot(r_H)>=0.

The tangent `h=partial_T+dot(r_H)partial_r` has

    g(h,h)|_H=dot(r_H)[dot(r_H)+2 sigma_H].

It is spacelike for strict positive flux and null for zero flux. The moving-surface current crossing is

    j_O^mu partial_mu(r-r_H)
      =j_O^r-dot(r_H)j_O^T<0

on the nonzero future-timelike branch. With zero charge flux at the exterior boundary,

    dot(Q_ext)=4 pi r_H^2[
       sigma_H j_O^r-q_H dot(r_H)
    ]<0.

The canonical scalar satisfies

    T_mu_nu k^mu k^nu=sum_A(k^mu partial_mu phi_A)^2>=0

for every null `k`. The W3-64 Penrose boundary therefore remains part of the coupled system.

## Method

1. Verify every dependency hash, successful upstream status, source role, and immutable-file boundary.
2. Reconstruct the generalized PG metric, inverse, determinant, dual frame, Misner–Sharp mass, null speeds, expansions, and horizon regularity directly from the coframe.
3. Derive the Cartesian scalar equations, Hilbert tensor, ordinary-phase current, conservation law, auxiliary-constraint propagation, principal block, and characteristic cone from the unchanged W3-58 action.
4. Compute the four-dimensional Einstein tensor directly from the metric. Project it on `(n,s)` and derive the Hamiltonian, momentum, radial evolution, `m_r`, and `m_T` equations without inserting a target flux.
5. Check `partial_T(partial_r m_MS)=partial_r(partial_T m_MS)` on the production equations. Independently verify the contracted Bianchi identity and on-shell matter conservation that close the angular equation.
6. Derive the marginal-surface mass square, radius velocity, area law, tube signature, moving-horizon current crossing, and exterior charge balance. Keep fixed-radius partial mass flux distinct from total differentiation along the moving tube.
7. Reproduce the W3-64 static coordinate map, W3-72 test-field equations, and W3-58 flat limit.
8. Audit the local scale/gradient/tidal roles: the lapse is not relabelled as nonstatic `p_t`; passive `p_L` never multiplies the field; curvature expressions require no denominator `1-zeta^2` at the marginal surface.
9. Run every registered mutation through the same evaluator, validate the exact three-file package, emit deterministic finite JSON, and stop.

## Cross-check

The Einstein tensor is obtained from the coordinate metric and independently compared with the ADM frame constraints. The mass balances are derived from `m_MS=r zeta^2/(2G)` and checked by mixed-derivative integrability. The scalar equations are derived in Cartesian variables and cross-checked against the polar current wherever `chi>0`. Characteristic speeds are obtained from both the first-order scalar principal block and the metric null polynomial. The horizon mass flux is derived once from the mass balance and again from the null Hilbert contraction. The static coordinate transformation is an independent sign and normalization regression.

## Files

The package is recursively restricted to exactly:

    w3_73_coupled_horizon_regular_einstein_complex_scalar_preregistration.md
    w3_73_coupled_horizon_regular_einstein_complex_scalar.py
    w3_73_result.json

No subdirectory, cache, plot, temporary output, copied dependency, or auxiliary note is permitted.

## Pass condition

Every dependency, source-ledger, coframe, metric, Einstein-tensor, scalar-action, stress, current, constraint, evolution, mass-balance, integrability, characteristic, marginal-flux, moving-surface, regression, scope, schema, package, and mutation gate passes with exact symbolic zero residual. All required true flags are exactly true and all required false flags are exactly false.

## Fail condition

The model version fails if any exact identity or dependency fails; if the coupled equations require a pole in `1-zeta^2`; if the metric and scalar cones differ; if either mass balance is omitted or inconsistent; if the Hilbert source is counted twice; if the horizon mass square or current sign changes; if `p_t`, `p_L`, or a foundation-pressure readout is inserted into the local action; if a marginal surface is promoted to a global event horizon; or if local constrained evolution is promoted to a complete collapse, regular interior, or singularity theorem.

## Falsifier and residual

A nonzero symbolic residual in the metric inverse, Einstein projections, scalar equations, Hilbert tensor, current conservation, Misner–Sharp balances, mixed-derivative compatibility, characteristics, horizon flux identities, or frozen regressions falsifies the corresponding atomic claim. Exact gates require symbolic zero. Strict signs use `sigma>0`, `r_H>0`, `D_H>0`, and the declared nonzero future-timelike branch.

## Error bound and validity health

There is no numerical approximation or observational likelihood. Accepted identities are symbolic. The formulation is local on a smooth `r>0`, `sigma>0`, `zeta>0` annulus. The scalar principal block is symmetric hyperbolic; the potential is smooth and lower order. The lapse and radial metric relations are constraints with one boundary normalization. The canonical kinetic term and null-energy identity remain healthy. The result supplies a constrained local evolution system rather than a global well-posedness or completeness proof.

## Observable map, forward model, and data role

Outputs are the local scalar fields and stresses, ordinary-phase charge density and flux, Misner–Sharp mass and its radial/time balances, marginal-surface location, local area velocity, and exterior charge loss. The forward model maps compatible smooth spherical initial data to the local constrained Einstein–complex-scalar evolution problem. No detector, telescope, waveform, likelihood, archive, calibration, or fitted parameter enters this stage.

## Identifiability and benchmark

The inherited action uniquely fixes the displayed local coupled equations and horizon-flux identities in the declared gauge branch. It does not select a global initial profile, determine the many-oscillon state, derive a foundation constitutive response, establish horizon formation, or determine a global endpoint. The exact benchmark is a smooth annulus crossing one nondegenerate future outer marginal sphere, with a nonzero future-timelike ordinary-phase current and finite Cartesian fields and derivatives.

## Closure flags

Required true:

    dependency_hashes_exact
    upstream_status_and_scope_exact
    one_metric_one_localized_source_exact
    w3_58_cartesian_action_unchanged_exact
    gpg_metric_inverse_volume_exact
    gpg_dual_frame_exact
    misner_sharp_definition_exact
    radial_null_speeds_exact
    null_expansions_exact
    marginal_surface_horizon_regular_exact
    scalar_evolution_system_exact
    scalar_auxiliary_constraint_propagation_exact
    scalar_principal_block_symmetric_exact
    matter_metric_characteristic_cone_match_exact
    potential_lower_order_exact
    hilbert_stress_exact
    ordinary_phase_current_cartesian_exact
    ordinary_phase_conservation_exact
    timelike_current_domain_exact
    horizon_inward_current_exact
    einstein_frame_components_exact
    hamiltonian_constraint_exact
    momentum_constraint_exact
    radial_metric_evolution_exact
    mass_radial_balance_exact
    mass_time_balance_exact
    mass_balance_integrability_exact
    angular_einstein_bianchi_closure_exact
    coupled_constraint_propagation_exact
    horizon_mass_flux_square_exact
    outer_marginal_radius_velocity_exact
    outer_marginal_area_law_exact
    marginal_tube_signature_exact
    moving_horizon_charge_crossing_exact
    exterior_charge_balance_exact
    static_w3_64_regression_exact
    test_field_w3_72_regression_exact
    flat_w3_58_regression_exact
    intrinsic_profile_not_passively_rescaled_exact
    readout_absent_from_local_dynamics_exact
    scale_gradient_tidal_role_separation_exact
    curvature_no_marginal_pole_exact
    local_constrained_data_handoff_exact
    excision_characteristic_direction_exact
    scalar_nec_exact
    penrose_boundary_inherited_exact
    mutation_controls_pass
    g0_goal_pass
    g1_conventions_pass
    g2_geometry_pass
    g3_einstein_system_pass
    g4_matter_system_pass
    g5_limits_regression_pass
    g6_physical_flux_pass
    g7_observation_not_applicable_exact
    g8_export_not_applicable_exact
    package_clean_pass
    aggregate_gate_pass

Required false:

    second_metric_introduced
    duplicate_localized_source_introduced
    noether_current_added_as_einstein_source
    foundation_response_action_added
    full_foundation_pressure_constitutive_law_derived
    nonstatic_lapse_identified_as_p_t
    p_L_inserted_into_local_action
    intrinsic_oscillon_profile_rescaled
    whole_oscillon_dynamical_rigidity_derived
    static_horizon_bound_oscillon_derived
    degenerate_outer_horizon_branch_derived
    global_gpg_coverage_derived
    horizon_formation_completed
    marginal_surface_promoted_to_event_horizon
    global_collapse_evolution_completed
    regular_centre_derived
    regular_black_hole_interior_derived
    singularity_resolution_completed
    geodesic_completeness_derived
    penrose_boundary_evaded
    scalar_nec_violated
    tensor_gravitational_waveform_derived
    new_observation_tested
    canon_changed
    intuitive_files_changed

## Frozen mutation registry

    pg_shift_sign_flipped -> shift_sign
    misner_sharp_coefficient_changed -> mass_definition_factor
    einstein_coupling_sign_flipped -> einstein_sign
    lapse_momentum_sign_flipped -> lapse_momentum_sign
    mass_radial_cross_term_removed -> mass_radial_cross_coefficient
    radial_metric_pressure_removed -> metric_pressure_coefficient
    mass_time_cross_terms_removed -> mass_time_cross_coefficient
    scalar_radial_cross_flux_removed -> scalar_cross_flux_coefficient
    potential_promoted_to_principal -> potential_principal_coefficient
    current_orientation_flipped -> current_sign
    horizon_potential_added -> horizon_potential_coefficient
    duplicate_metric_source -> metric_ids, source_ledger
    profile_passively_rescaled -> profile_scale_power
    lapse_relabelled_as_p_t -> lapse_role
    marginal_promoted_to_event_horizon -> horizon_role
    static_horizon_oscillon_promoted -> static_horizon_role
    degenerate_outer_branch_admitted -> outer_branch_rule
    global_interior_overclaim -> promoted_claims

## Gate registry

- G0_GOAL: frozen contract, hashes, exact package, claim, and stopping rule.
- G1_CONVENTIONS: coframe, signs, Cartesian/polar dictionary, source ledger, and field roles.
- G2_GEOMETRY: generalized PG metric, inverse, determinant, frame, mass, null cones, expansions, and horizon regularity.
- G3_EINSTEIN_SYSTEM: projected Einstein tensor, constraints, radial evolution, mass balances, compatibility, and Bianchi closure.
- G4_MATTER_SYSTEM: action-derived scalar evolution, Hilbert stress, U(1) current, auxiliary constraint, hyperbolicity, and NEC.
- G5_LIMITS_REGRESSION: W3-58 flat, W3-64 static, and W3-72 test-field limits.
- G6_PHYSICAL_FLUX: marginal mass square, radius and area velocity, tube signature, moving-surface charge crossing, source/profile separation, and Penrose boundary.
- G7_OBSERVATION: not applicable; no data are read.
- G8_EXPORT: not applicable; Canon, intuitive manuscripts, and release artifacts are unchanged.

## Provenance and references

The verifier uses deterministic Python and SymPy, UTF-8 text, SHA-256 dependency pins, strict finite JSON, one preregistration, one source, and one result. It reads no archived theory and performs no network or observational operation. The horizon-penetrating spherical formulation is cross-checked against V. Husain and O. Winkler, *Flat slice Hamiltonian formalism for dynamical black holes*, Physical Review D 71, 104001 (2005), DOI `10.1103/PhysRevD.71.104001`, arXiv `gr-qc/0503031`; J. Ziprick and G. Kunstatter, *Numerical study of black-hole formation in Painlevé–Gullstrand coordinates*, Physical Review D 79, 101503 (2009), DOI `10.1103/PhysRevD.79.101503`; and C. W. Misner and D. H. Sharp, *Relativistic Equations for Adiabatic, Spherically Symmetric Gravitational Collapse*, Physical Review 136, B571 (1964), DOI `10.1103/PhysRev.136.B571`.

## Successful status

    PASS_EXACT_HORIZON_REGULAR_SPHERICAL_EINSTEIN_COMPLEX_SCALAR_CONSTRAINED_EVOLUTION_FROM_THE_INHERITED_ACTION__MISNER_SHARP_CHARGE_AND_OUTER_MARGINAL_AREA_FLUX_IDENTITIES_CLOSED_WITHOUT_PASSIVE_PROFILE_RESCALING__GLOBAL_COLLAPSE_EVENT_HORIZON_INTERIOR_AND_SINGULARITY_NOT_SOLVED

The successful stage establishes the local fully coupled constrained handoff and stops there.
