# W3-71 Preregistration: Covariant Scale Connection and Horizon–Material Separation

## Target and stopping rule

This stage constructs the minimum covariant readout that keeps three physical
roles separate:

1. the temporal scale read by an external clock comparison;
2. the spatial ruler projection carried by the one Einstein coframe; and
3. the oscillon's unchanged intrinsic local profile, the coordinate value
   assigned to that profile by an external reference standard, and the
   collective-phase density.

The construction must reproduce the frozen homogeneous law
p_t^2=n_C/n_C0, reproduce the exact static Killing-lapse readout without an
unhealthy density sign, preserve the W3-67 temporal/spatial split, and expose
the true-horizon branch in a horizon-regular coframe.

The stage stops after this branch-restricted readout closure, the exact
separation between the intrinsic profile and its external reference-standard
coordinate assignment, and the horizon decision. It opens no horizon-crossing
material-current dynamics, distinct-equilibrium backreaction calculation,
mixed-flow global integration, black-hole interior solve, or observational
calculation. Canon and the intuitive manuscripts remain unchanged.

## Claim contract

- CLAIM_ID: W3_71_COVARIANT_SCALE_CONNECTION_AND_HORIZON_MATERIAL_SEPARATION.
- CLAIM: Let u^mu be the normalized timelike congruence appropriate to the
  selected branch, h_mu^nu=delta_mu^nu+u_mu u^nu its spatial projector,
  a_mu=u^nu nabla_nu u_mu its acceleration, and
  Theta=nabla_mu u^mu its expansion. The covariant one-form

      W_mu = a_mu + (1/2) Theta u_mu

  defines the temporal readout by

      nabla_mu ln p_t = W_mu

  on simply connected patches where

      F_mu_nu = 2 nabla_[mu W_nu] = 0.

  On the homogeneous W3-50 current branch, current conservation gives
  dot(ln p_t)=(1/2)dot(ln n_C), hence p_t^2=n_C/n_C0 after reference
  normalization. On a static normalized-Killing branch,
  u^mu=xi^mu/calN, Theta=0, and a_mu=D_mu ln calN, hence p_t=calN. The W3-54
  Euler relation supplies the independent conditional crosscheck
  calN mu_C=constant and therefore p_t=mu_infinity/mu_C with the original
  healthy sound-speed interval intact. The full strong-field spatial ruler
  factor p_L is a separate coframe projection. On Schwarzschild's isotropic
  exterior,

      p_t=(1-U/2)/(1+U/2),
      p_L=(1+U/2)^(-2)=((1+p_t)/2)^2.

  They share the linear weak-field response and split at quadratic order.
  The oscillon's intrinsic radius R_O is defined in its local orthonormal
  frame by the W3-58 charge moment and is not p_L. For radial comparison with
  the external isotropic ruler,

      d rho = p_L d ell,
      Delta rho = integral p_L(ell) d ell.

  On a local patch where p_L is constant across the profile this reduces to

      R_O^ext = p_L R_O^loc.

  R_O^ext is the external reference-standard coordinate assignment of the
  same unchanged local profile; it is neither a second local property nor a
  resolved optical image. This is observer-to-observer ruler conversion, not
  local compression or dilation of the oscillon. W3-65 compares distinct
  equilibrium solutions; its changing
  charge-rms radius is not an environmental shrinkage law for one oscillon.
  Painlevé–Gullstrand continuation proves that the horizon is locally regular,
  the outgoing radial null characteristic vanishes at r=r_s, and an
  everywhere-static timelike material worldline cannot continue to r<=r_s.
  Any timelike material current crossing a true horizon is therefore
  nonstatic, while a static material surface must remain at R>r_s. This is a
  causal necessity, not a constructed RefG interior solution.
- TYPE:
  SELECTED_BRANCH_RESTRICTED_COVARIANT_READOUT_CLOSURE_WITH_EXACT_HOMOGENEOUS_STATIC_AND_HORIZON_REDUCTIONS.
- MODEL_VERSION:
  W3-71-v1.1-COVARIANT-SCALE-CONNECTION-HORIZON-MATERIAL-SEPARATION.
  Any change to W_mu, its coefficient, the congruence roles, integrability
  rule, metric count, Schwarzschild benchmark, spatial readout, source ledger,
  intrinsic/external profile roles, horizon decision, or stopping rule creates
  a new model version.

## Assumptions

1. W3-54 supplies one connected Lorentzian coframe, one operational metric,
   TEGR/Einstein–Hilbert dynamics, a conserved phase current, and one
   once-counted Hilbert-source ledger.
2. W3-50 supplies the homogeneous positive current law
   dot(n_C)+Theta n_C=0 and the selected homogeneous response
   p^2=n_C/n_C0.
3. W3-52 and W3-67 supply the complete standard 1PN/PPN inheritance and prove
   that temporal and spatial ruler factors share their linear term but split
   at quadratic order.
4. W3-58 supplies a finite localized ordinary-phase oscillon minimally coupled
   to the same coframe and an intrinsic charge-moment radius measured in its
   local orthonormal frame. A coframe readout is not a deformation operator:
   it introduces no local rescaling, compression, or dilation, and the
   intrinsic charge-moment profile remains unchanged.
5. W3-64 supplies the unchanged Einstein strong-field operator, an
   asymptotically Schwarzschild exterior, and the retained-source
   NEC/Penrose boundary.
6. W3-65 supplies current finite-oscillon branch data used only as a role
   regression: between its registered anchor and first turn, the central lapse
   decreases while the charge-rms radius increases slightly. These are
   distinct equilibrium solutions, not the same oscillon viewed from two
   reference environments.
7. W3-70 excludes the algebraic local identification
   p_t^2=n_C/n_infinity on the static no-flux branch. It leaves the original
   collective phase current and Hilbert source unchanged.
8. The static vacuum benchmark has M>0 and r_s=2GM/c_0^2. The static
   congruence is used only where its Killing vector is timelike.
9. W_mu is a selected readout connection absent from the action. It contributes
   no Euler–Lagrange equation, Hilbert source, or new propagating degree of
   freedom in this gate.

## Domain

- Homogeneous, isotropic, vorticity-free W3-50 current branch with n_C>0.
- Static, nonrotating, asymptotically flat, normalized-Killing branch with
  calN>0.
- Static isotropic Schwarzschild exterior U=GM/(c_0^2 rho)<2 and its one-sided
  horizon limit.
- Ingoing Painlevé–Gullstrand Schwarzschild patch at areal radius r>0,
  including both sides of r=r_s.
- Local infinitesimal clock/ruler readouts and the exact radial line-integral
  conversion between local proper length and the external isotropic ruler.
- The constant-p_L finite-profile formula applies only in the local-uniform
  coframe limit; a resolved remote image additionally requires ray transport.

General mixed expanding/accelerating flow requires the independent
integrability condition F_mu_nu=0. Rotation, vorticity, collapse evolution,
interior equation of state, environment-dependent backreaction across
distinct equilibria, finite-image lensing, Hawking radiation, r=0, geodesic
completion, and observational likelihood lie outside this gate.

## Conventions

Signature: (-,+,+,+). The convective derivative is
dot(X)=u^mu nabla_mu X. The spatial derivative is
D_mu X=h_mu^nu nabla_nu X. The normalized Killing lapse is
calN=sqrt(-xi^2).

For the static isotropic Schwarzschild exterior, define

    m=GM/c_0^2,
    U=m/rho,
    q=U/2,
    r=rho(1+q)^2.

Then

    ds^2=-p_t^2 c_0^2 dt^2
         +p_L^(-2)(d rho^2+rho^2 d Omega_2^2),

    p_t=(1-q)/(1+q),
    p_L=(1+q)^(-2).

Local radial intervals obey d tau=p_t dt and d ell=d rho/p_L, so radial
coordinate light speed is d rho/dt=plus-or-minus c_0 p_t p_L and the local
speed is c_0.

For an intrinsic local radial profile interval, the same identity gives

    Delta rho = integral_0^(R_O^loc) p_L(ell) d ell.

If p_L is constant across a sufficiently local profile,

    R_O^ext = p_L R_O^loc.

R_O^loc remains the unchanged charge-moment radius in the local orthonormal
frame. R_O^ext is only the coordinate value assigned to that same profile by
the external reference standard; p_L is the ruler-conversion factor.

The ingoing Painlevé–Gullstrand coframe is

    e^0=dT,
    e^1=dr+v dT,
    v=sqrt(r_s/r),

with metric

    ds^2=-(e^0)^2+(e^1)^2+r^2 d Omega_2^2.

Future radial null characteristics obey dr/dT=-v plus-or-minus 1.

## Freedom ledger

- Coefficient 1/2 in W_mu: fixed by the inherited homogeneous law
  p_t^2=n_C/n_C0; no fitted freedom.
- Coefficient 1 multiplying a_mu: fixed by the normalized static
  Killing-lapse identity a_mu=D_mu ln calN; no fitted freedom.
- Reference normalization p_t=1: one conventional normalization at the
  selected reference worldline or epoch.
- W_mu integrability: a branch condition, not a tunable switch. Homogeneous
  and static target branches satisfy it exactly; general mixed flow remains
  unselected.
- p_L: fixed by the one Einstein coframe on the Schwarzschild benchmark.
- Intrinsic oscillon radius R_O^loc: the W3-58 charge-moment profile observable
  in the local orthonormal frame; it is not multiplied into its own local
  dynamics.
- External reference-standard assignment R_O^ext: fixed kinematically by
  integrating p_L across the local proper profile. It is not a second local
  radius and adds no response function or fit parameter.
- n_C and rho_C(n_C): unchanged W3-54 variables and universal EOS freedom; no
  identification with p_t is added on the static branch.
- M: one benchmark mass scale; no fit and no object-dependent rule.

## Hash-pinned dependencies

1. CODES.md.
2. W3-50 neutral collective phase-density bridge contract.
3. W3-52 full 1PN inheritance contract.
4. W3-54 coframe/TEGR/phase-source contract.
5. W3-58 one-oscillon preregistration.
6. W3-64 Einstein strong-field result.
7. W3-65 first-turning-point result.
8. W3-67 foundation strong-field response result.
9. W3-70 collective-phase carrier result.

Required upstream statuses and closure flags are the actual current records.
The verifier must reject a changed dependency hash, a changed source ledger,
a promoted W3-51 weak metric, a loss of the standard PPN vector, or a change
to the W3-70 density-carrier decision.

The current W3-52, W3-54, and W3-58 result artifacts are hash-pinned as
supporting closure records. They do not enlarge the nine-item dependency
ledger; they certify the exact current status fields read by the verifier.

## Method

1. Hash-audit every dependency and validate the exact upstream status and
   closure subset used here.
2. Verify covariantly that u^mu W_mu=-Theta/2 and
   h_mu^nu W_nu=a_mu.
3. On the homogeneous branch, combine
   dot(ln n_C)=-Theta with the first projection and derive
   p_t^2=n_C/n_C0.
4. On the static normalized-Killing branch, use Theta=0 and
   a_mu=D_mu ln calN to derive p_t=calN.
5. Independently apply the W3-54 Euler relation
   a_mu=-D_mu ln mu_C and verify
   p_t=mu_infinity/mu_C. Show that
   D ln p_t=-c_s^2 D ln n_C keeps 0<=c_s^2<=1 and never requires
   c_s^2=-1/2.
6. Derive the isotropic-to-areal Schwarzschild map, prove
   1-r_s/r=p_t^2, prove p_L=((1+p_t)/2)^2, and reproduce the W3-67 weak
   series and full 1PN metric coefficients.
7. Solve the radial null polynomial independently, recover both external
   coordinate-speed roots, and then reconstruct the local tetrad speed on
   0<U<2. Treat U->2^- only as a one-sided static limit.
8. Build the Painlevé–Gullstrand metric from its coframe, verify its inverse
   and nonzero determinant at r=r_s, derive both radial null characteristics,
   and classify their signs outside, at, and inside the horizon.
9. Evaluate the round-sphere expansion signs, the finite horizon
   Kretschmann scalar K=12r_s^2/r^6, and the static tangent norm.
10. Keep the intrinsic charge-moment radius distinct from p_L and derive
    Delta rho=integral p_L d ell, with R_O^ext=p_L R_O^loc only in the
    local-uniform limit. Audit W3-65 solely to block its distinct-equilibrium
    radius change from being misread as local compression or expansion.
11. Run production mutations for the W_mu coefficients, static density
    relabelling, p_t=p_L, radial metric function in place of total lapse,
    nonintegrable W_mu accepted as a scalar, removed Painlevé–Gullstrand
    shift, static sub-horizon material worldline, duplicated metric/source,
    passive readout dynamics, intrinsic-radius relabelling that also breaks
    the external p_L projection, local-time stopping, and
    interior/singularity overclaim.

## Pass condition

Every dependency, projection, branch reduction, EOS-health crosscheck,
Schwarzschild identity, 1PN regression, light-speed reconstruction,
horizon-regular metric identity, causal sign, static-worldline
classification, intrinsic/external profile separation, package audit, and
mutation control passes.

The aggregate result must preserve exactly these roles:

- p_t: branch-restricted temporal scale readout generated by W_mu;
- p_L: independent spatial coframe projection;
- n_C: collective phase-action density;
- R_O^loc: intrinsic charge-moment profile radius in the local frame;
- R_O^ext: the coordinate value assigned to the same unchanged local profile
  by the external reference standard through the p_L line integral; it is
  not a local property or a resolved optical image.

Any timelike material current that crosses a true horizon must be nonstatic.
An everywhere-static material worldline is admissible only at R>r_s. This is
a necessity statement; no RefG horizon-crossing material solution is claimed.

## Fail condition

The model version fails if either W_mu coefficient changes; a target branch
has nonzero F_mu_nu; the homogeneous or static reduction fails; the static
branch requires negative c_s^2; p_t is equated algebraically with n_C; p_L is
forced equal to p_t beyond the weak order; the standard 1PN metric is lost;
the Painlevé–Gullstrand coframe degenerates at the horizon; an outgoing future
null characteristic remains outward inside r_s; a fixed-r tangent is declared
timelike at r<=r_s; finite oscillon radius is equated with p_L; passive W_mu is
assigned dynamics or stress; the external reference-standard coordinate
assignment is not obtained from the p_L line integral; a second metric or
duplicate source enters; or any open interior result is promoted.

## Falsifier

An exact counterexample within a declared target branch to any projection,
branch reduction, metric identity, or horizon sign falsifies this model
version. A healthy W3-54 EOS that forces c_s^2=-1/2 under the differential
static bridge would falsify the claimed resolution of the W3-70 sign
contradiction. A fixed-r timelike Schwarzschild worldline at r<r_s would
falsify the horizon binary.

## Residual and error bound

All connection projections, reductions, coordinate maps, metric identities,
series coefficients, null characteristics, curvature expressions, and
intrinsic/external ruler conversions carry exact symbolic zero residual. The
W3-65 role regression uses the already frozen numerical artifact and only
checks that distinct equilibrium radii cannot be relabelled as p_L or as an
environmental shrinkage law; it creates no new numerical solve or fit.

## Validity and health

W_mu is a covariant one-form assembled from the selected congruence. A scalar
p_t exists locally only when F_mu_nu=0; the target homogeneous and static
branches satisfy this exactly. The readout introduces no new mode and leaves
the W3-54 EOS health interval, one metric, and once-counted source unchanged.

The Painlevé–Gullstrand coframe is nondegenerate at r=r_s. Static Killing
alignment ends there; local proper time on a horizon-regular timelike
worldline remains regular.

The coframe readout is not a deformation operator. The oscillon retains its
intrinsic local orthonormal profile, while an external observer assigns a
coordinate value to that same profile through the spatial coframe. A finite
resolved image additionally requires ray transport and is not supplied by
the ruler conversion alone. The inherited Penrose
boundary remains active: a future null-complete regular trapped interior must
change at least one explicit theorem hypothesis through completed dynamics.

## Branches

- Homogeneous selected branch: a_mu=0, F_mu_nu=0,
  p_t^2=n_C/n_C0.
- Static selected branch: Theta=0, F_mu_nu=0,
  p_t=calN=mu_infinity/mu_C.
- Static isotropic Schwarzschild exterior: U<2 with exact p_t and p_L.
- Horizon-crossing representation: ingoing Painlevé–Gullstrand at r>0.
- True-horizon material requirement: any crossing timelike current is
  nonstatic; its RefG dynamics are not constructed here.
- Static material worldline branch: admissible only at R>r_s.
- Deferred mixed branch: F_mu_nu must be derived and tested from a selected
  material-current dynamics.
- Deferred finite-image branch: integrate the coframe and null-ray transfer
  across a resolved profile; do not deform the intrinsic local oscillon merely
  to express it in an external ruler convention.

## Observable map, data role, and identifiability

Static redshift, infinitesimal ruler conversion, the local-uniform external
size projection, and the sign of future radial null expansions are ideal
geometric readouts. This gate builds no instrument, waveform, resolved-image
transfer, likelihood, or population model and uses no observational data.

The homogeneous and static reductions fix p_t up to one reference
normalization. Schwarzschild fixes p_L after coordinate and asymptotic-time
normalization. The intrinsic radius is fixed by the W3-58 charge moment and
its external radial expression by the p_L line integral. General mixed-flow
integrability and a horizon-crossing material-current solution remain
unidentified without new dynamics.

## Benchmark

The exact benchmarks are:

1. W3-50 homogeneous p_t^2=n_C/n_C0;
2. W3-54 stationary Bernoulli relation calN mu_C=constant;
3. W3-67 temporal/spatial Schwarzschild split and standard 1PN limit;
4. horizon-regular Schwarzschild in ingoing Painlevé–Gullstrand form; and
5. W3-65 distinct-equilibrium anchor-to-turn role regression, with no
   environmental-scaling inference.

## Closure flags

Required true:

- dependency_hashes_exact
- upstream_status_and_scope_exact
- scale_connection_covariant_exact
- scale_connection_coefficients_inherited_exact
- scale_connection_projections_exact
- target_branch_integrability_exact
- homogeneous_reduction_exact
- static_killing_reduction_exact
- w3_54_euler_crosscheck_exact
- healthy_sound_speed_interval_preserved_exact
- static_density_algebraic_map_rejected_exact
- one_metric_one_source_unchanged_exact
- isotropic_areal_map_exact
- schwarzschild_reconstruction_exact
- temporal_spatial_coframe_split_exact
- exact_temporal_spatial_relation
- full_1pn_regression_exact
- external_radial_null_speed_exact
- local_light_speed_exact
- pg_metric_from_coframe_exact
- pg_inverse_exact
- pg_determinant_regular_at_horizon_exact
- pg_radial_null_characteristics_exact
- round_sphere_trapping_sign_exact
- kretschmann_finite_at_horizon_exact
- static_worldline_timelike_iff_outside_exact
- true_horizon_requires_nonstatic_material_current_exact
- finite_oscillon_radius_role_separate_exact
- intrinsic_local_oscillon_radius_definition_exact
- external_ruler_projection_exact
- finite_profile_local_uniform_scope_exact
- w3_65_distinct_equilibria_scope_exact
- passive_readout_no_new_dof_or_action_exact
- penrose_boundary_inherited_exact
- binary_branch_decision_exact
- mutation_controls_pass
- g0_goal_pass
- g1_conventions_pass
- g2_core_algebra_pass
- g3_structure_pass
- g4_independent_check_pass
- g5_limits_regression_pass
- g6_physical_match_pass
- g7_observation_not_applicable_exact
- g8_export_not_applicable_exact
- package_clean_pass
- aggregate_gate_pass

Required false:

- mixed_branch_global_integrability_derived
- horizon_crossing_material_current_derived
- w3_65_environmental_shrinkage_inference_allowed
- intrinsic_profile_rescaling_action_present
- exact_common_strongfield_clock_ruler_factor_derived
- horizon_crossing_static_congruence_valid
- static_material_worldline_inside_horizon_admissible
- global_strong_field_solution_derived
- global_solve_opened
- collapse_evolution_completed
- regular_black_hole_interior_derived
- singularity_resolution_completed
- geodesic_completeness_derived
- new_observation_tested
- canon_changed
- intuitive_files_changed

## Crosscheck and mutation controls

The homogeneous reduction is derived from both the W_mu projection and direct
current conservation. The static reduction is derived from normalized Killing
kinematics and independently from the W3-54 Euler/Bernoulli relation. The
Schwarzschild map is checked by direct metric substitution and by the
isotropic-to-areal identity. Radial light speeds are obtained from the metric
polynomial before tetrad conversion. Integrability is checked independently
by both F_mu_nu and a mixed-witness loop integral. The intrinsic/external
profile map is checked by the charge moment and the p_L line integral. The
horizon decision is checked by coframe determinant, characteristic roots,
expansion signs, curvature, and the full static-tangent inequality.

The frozen mutation registry is:

1. theta_coefficient_changed: theta_coefficient;
2. acceleration_coefficient_sign_flipped: acceleration_coefficient;
3. static_density_relabelled: static_density_power;
4. p_t_forced_equal_p_L: spatial_rule;
5. radial_N_used_as_lapse: lapse_rule;
6. passive_readout_made_dynamic: readout_action_coefficient;
7. nonintegrable_W_accepted: accepted_connection_domains;
8. pg_shift_removed: pg_shift_coefficient;
9. static_subhorizon_worldline_admitted: static_material_domain;
10. metric_source_duplicated: metric_ids and branch_source_ledger;
11. finite_radius_relabelled_as_p_L: finite_radius_rule;
12. p_t_zero_called_local_time_stop: local_time_rule;
13. interior_singularity_overclaim: promoted_claims.

Every negative control passes through the same validators as production. The
result must hash-pin this preregistration and verifier source, contain finite
UTF-8 JSON, match the exact required-true and required-false key sets, and
contain exactly three package files: preregistration, verifier, and result.

## Primary references

- K. Schwarzschild, Sitzungsberichte der Königlich Preussischen Akademie der
  Wissenschaften (1916), 189–196.
- K. Martel and E. Poisson, Regular coordinate systems for Schwarzschild and
  other spherical spacetimes, American Journal of Physics 69, 476 (2001),
  DOI 10.1119/1.1336836, arXiv:gr-qc/0001069.
- R. Penrose, Gravitational Collapse and Space-Time Singularities, Physical
  Review Letters 14, 57 (1965), DOI 10.1103/PhysRevLett.14.57.

## Decision semantics

PASS establishes one covariant, parameter-free scale connection whose target
projections reproduce both the homogeneous and static temporal readouts. It
establishes the exact separation of temporal lapse, spatial ruler projection,
collective density, intrinsic local oscillon profile, and the same profile's
external ruler projection, together with the horizon-regular causal handoff.
The next physical input is a horizon-regular nonstatic material-current
dynamics or an exact elimination from existing fields. A resolved external
image is a separate ray-transfer calculation; neither task requires declaring
the local oscillon itself compressed.

The preregistered successful status is:

PASS_EXACT_COVARIANT_SCALE_CONNECTION_ON_HOMOGENEOUS_AND_STATIC_BRANCHES__TEMPORAL_LAPSE_SPATIAL_RULER_AND_INTRINSIC_OSCILLON_PROFILE_SEPARATED_WITH_EXACT_COFRAME_RULER_CONVERSION_EINSTEIN_EXTERIOR_AND_1PN__HORIZON_CROSSING_MATERIAL_CURRENT_NOT_DERIVED
