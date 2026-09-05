# W3-70 Preregistration: Collective-Phase Carrier Admissibility

## Result stated in advance

W3-70 tests the most economical exterior carrier still present after W3-69:
the already retained W3-50/W3-54 neutral collective phase density.  The
candidate adds no field and no gravitational operator.  It extends the
homogeneous RefG dictionary locally,

```text
p_n(x)^5 = n_C,op(x)/n_infinity,       n_infinity>0,
```

and asks whether the same positive operational-volume density can reproduce
the decreasing static operational factor outside positive mass. W3-62 fixes
the one-charge, two-measure dictionary on the homogeneous branch:

```text
nHat_C,F = p^2,
nHat_C,op = p^3 nHat_C,F = p^5.
```

Here `nHat` means normalization by the corresponding reference density.
The factor `p^3` is the foundation-to-operational volume Jacobian. The local
static extension is the candidate being tested; the homogeneous Jacobian is
not assumed independently valid on a general inhomogeneous geometry.

The answer is fixed by the W3-54 phase equation and its health interval.  On
a stationary, static, no-flux branch with total lapse `calN`, the phase equation gives

```text
mu(n_C) calN = mu_infinity,
mu(n_C)=rho_C'(n_C)/c0,
c_s^2=d ln(mu)/d ln(n_C)=n_C rho_C''/rho_C' in [0,1].
```

For `c_s^2>0`, density therefore increases where `calN` decreases.  The
candidate map makes `p_n` increase there, whereas the W3-51 positive-mass
dictionary gives `p_op=calN=exp(-u)<1`.  Exact first-order matching would require
`c_s^2=-1/5`, outside the stable W3-54 branch.  The endpoint `c_s^2=0`
cannot support a regular varying-lapse equilibrium because `mu` is locally
constant.

The inverse-density control `p_inv^5=n_infinity/n_C` has the correct static
sign and matches the linear coefficient at `c_s^2=1/5`, but it reverses the
frozen homogeneous W3-50 map.  The chemical-potential ratio
`p_mu=mu_infinity/mu=calN` is an exact stationary readout; by itself it is
passive and adds no material-response dynamics.  Requiring it also to equal
the homogeneous density map again forces `c_s^2=-1/5`.

The natural single-density carrier is therefore rejected as the universal
RefG operational factor.  The exact remaining input is a covariantly derived
branch-sensitive constitutive bridge, involving additional state information,
or a different healthy carrier.  No global compact-object solve is opened.

## Target and stopping rule

The stage asks one question:

```text
unchanged W3-50/W3-54 collective phase
  -> freeze the minimal local density extension of p
  -> derive the stationary no-flux first integral
  -> compare its weak exterior sign with W3-51
  -> audit health and exact controls
  -> accept or reject this carrier role
  -> STOP.
```

Exactly three files belong to this package:

1. `w3_70_collective_phase_carrier_admissibility_preregistration.md`
2. `w3_70_collective_phase_carrier_admissibility.py`
3. generated `w3_70_result.json`

No new action, equation of state, mixed coupling, profile, global
strong-field integration, collapse evolution, black-hole solution,
observation, Canon change, or intuitive-manuscript edit belongs to this
stage.

## Frozen candidate and exact stationary reduction

Use the W3-54 covariant phase-current action and conventions, with
`n_C := n_C,op` as required by W3-62. The distinct `n_C,F` denotes the
foundation-volume density and does not replace the operational Hilbert density:

```text
S_C = integral d^4x [
        J^mu partial_mu theta_C
        -(e/c0) rho_C(n_C)],

n_C=sqrt(-g_mu_nu J^mu J^nu)/e>0,
u^mu=J^mu/(e n_C),
u^mu u_mu=-1.
```

Its `J^mu` variation is

```text
partial_mu theta_C + mu(n_C) u_mu = 0,
mu(n_C)=rho_C'(n_C)/c0>0.
```

On a static spherical branch,

```text
ds^2=-calN(r)^2 (dx^0)^2+h_ij dx^i dx^j,
theta_C=omega_C x^0,
J^r=0,
calN(infinity)=1.
```

Current conservation makes the radial flux constant.  Regularity at the
centre, or zero flux through the asymptotic boundary, fixes that constant to
zero.  The time component of the phase equation then gives the exact first
integral

```text
mu(n_C) calN = omega_C = mu_infinity.
```

The W3-54 stable causal barotropic branch has

```text
0 <= c_s^2 = d p_C/d rho_C
           = n_C rho_C''(n_C)/rho_C'(n_C)
           = d ln(mu)/d ln(n_C) <= 1.
```

For a positive W3-51 source, write

```text
calN=p_op=exp(-u)=1-u+O(u^2),          u>0.
```

At the asymptotic state and for `c_s^2>0`,

```text
delta ln(mu) = -delta ln(calN) = u+O(u^2),
delta ln(n_C) = u/c_s^2+O(u^2),
delta ln(p_n) = u/(5c_s^2)+O(u^2).
```

The operational dictionary instead requires

```text
delta ln(p_op)=-u+O(u^2).
```

Matching the two coefficients gives uniquely

```text
1/(5c_s^2)=-1,                         c_s^2=-1/5.
```

The same veto is exact on any nonconstant interval where the candidate
identification holds:

```text
n_C=n_infinity calN^5,
mu(n_C)=mu_infinity (n_C/n_infinity)^(-1/5),
d ln(mu)/d ln(n_C)=-1/5,
rho_C''<0.
```

This violates the frozen W3-54 health interval.  At `c_s^2=0`, a finite
regular `O(u)` density perturbation leaves `mu` unchanged and cannot satisfy
`delta ln(mu)=u` for a nonzero exterior potential.

## Exact controls and surviving boundary

Two controls locate the obstruction.

1. With `p_inv^5=n_infinity/n_C`,
   `delta ln(p_inv)=-u/(5c_s^2)`; the static coefficient matches at the
   healthy value `c_s^2=1/5`.  This map has
   `d ln(p_inv)/d ln(n_C)=-1/5`, opposite to the frozen homogeneous
   W3-50/W3-62 operational-density derivative `+1/5`.
2. With `p_mu=mu_infinity/mu`, the stationary equation gives `p_mu=calN`
   exactly.  Compatibility with `p^5=n_C/n_infinity` over the same
   one-variable constitutive branch requires
   `d ln(mu)/d ln(n_C)=-1/5`, the same excluded value.

The original W3-50 homogeneous conservation law and the W3-54 phase source
remain intact in their declared domains.  This gate rejects only their
single-variable local extension as one universal operational `p`.  A
multivariate bridge may use a covariantly derived discriminator between
homogeneous dilution and static acceleration; a different carrier may also
be tested.  Either route is a new model version and must derive its action,
source exchange, weak screening, mode health, and strong-field solution.

## Claim contract

### CLAIM_ID

`W3_70_COLLECTIVE_PHASE_CARRIER_ADMISSIBILITY`

### CLAIM

On the frozen W3-50/W3-54 positive, shift-symmetric, stable causal phase
branch, the universal local extension `p_n^5=n_C/n_infinity` cannot equal
the W3-51 decreasing positive-mass operational factor on a stationary
no-flux exterior.  The exact stationary phase first integral and the
homogeneous operational-density derivative require `c_s^2=-1/5`, while W3-54
requires `0<=c_s^2<=1`.  The inverse-density and chemical-potential controls
show that the obstruction is the attempt to use the same one-variable
density map in homogeneous dilution and static acceleration, rather than the
existence of a covariant phase reference itself.

### TYPE

`EXACT_STATIONARY_PHASE_FIRST_INTEGRAL_AND_CONSTITUTIVE_SIGN_AUDIT_WITH_HARD_CARRIER_ROLE_REJECTION`.

### MODEL_VERSION

`W3-70-v1.1-COLLECTIVE-PHASE-CARRIER-ADMISSIBILITY`.

Version 1.1 corrects the operational-density exponent with W3-62's volume
Jacobian. Version 1.0's coefficient `1/2` conflated the two measures and is
superseded by `1/5`; the healthy-EOS sign rejection survives.

A change to the phase action, density meaning, homogeneous `p` map,
stationary branch, flux condition, sound-speed health interval, operational
weak dictionary, dependency hashes, carrier-role semantics, or stopping rule
creates a new version.

### ASSUMPTIONS

1. Every dependency file has the exact SHA-256 hash registered below.
2. W3-50 supplies the positive foundation-volume density `n_C,F`, its exact
   diagonal shift current, and `eta_F=n_C,F/n_C,F0`, `p^2=eta_F`.
   W3-62 fixes `nHat_C,op=p^3 nHat_C,F=p^5` on the homogeneous branch;
   `n_C := n_C,op` throughout the covariant W3-54 action.
3. W3-54 supplies the covariant one-potential phase-current action, its
   `J^mu` equation, one Hilbert source, and the stable causal interval
   `0<=n_C rho_C''/rho_C'<=1`.
4. The candidate is the new universal local extension
   `p_n^5=n_C/n_infinity`; it is tested rather than assumed true.
5. The target exterior is static, admits an asymptotically normalized
   timelike Killing field `xi`, and carries no radial collective-phase flux.
   Its total lapse is `calN=sqrt(-xi^2)`, with `calN(infinity)=1`.
6. W3-51 supplies `p_op=calN=exp(-u)` on the positive-mass static weak branch.
   Only the temporal operational factor and its linear weak sign are used;
   no exact common temporal/spatial strong-field factor is assumed.
7. `n_infinity>0`, `rho_C'>0`, and the perturbation about infinity is
   regular.  The polar phase boundary `n_C=0` is excluded.
8. No phase-breaking source, radial flux, vorticity, multi-potential fluid,
   mixed torsion-current operator, nonminimal matter coupling, or new field
   is inserted.
9. No datum, archived theory, target compactness, desired core, or
   result-selected parameter enters.

### DOMAIN

Connected, regular W3-54 phase states with `n_C>0`; a static, stationary,
no-flux positive-mass exterior; an asymptotically normalized lapse; and a
regular weak expansion about `calN=1`.  The exact Bernoulli identity applies
throughout that branch.  The coefficient contradiction is evaluated at the
asymptotic state and therefore does not require a global interior solution.

Rotating flow, nonzero phase flux, explicit shift breaking, phase transitions,
nonanalytic zero-sound-speed responses, multiple fluid potentials,
higher-gradient or nonminimal operators, and dynamical collapse are outside
this version.

### CONVENTIONS

- Signature is `(-+++)`; `calN=sqrt(-xi^mu xi_mu)>0`.
- `xi` is normalized at infinity and `u_C^mu=xi^mu/calN` on the target
  stationary branch.
- In W3-64 static notation the total lapse would be
  `calN=sigma sqrt(N_radial)`; the radial metric function alone is never
  substituted for `calN`.
- `n_C := n_C,op` is the operational-volume density; `n_C,F` is the distinct
  foundation-volume density. The homogeneous normalized Jacobian is
  `nHat_C,op=p^3 nHat_C,F=p^5`.
- `mu=rho_C'/c0>0` is the phase chemical potential per the W3-54
  convention; `mu calN=mu_infinity`.
- `c_s^2=n_C rho_C''/rho_C'=d ln(mu)/d ln(n_C)`.
- `u=-ln(p_op)>0` outside positive mass, so
  `calN=p_op=exp(-u)`.
- `p_n` names the tested density candidate, `p_inv` its inverse-density
  control, and `p_mu` its chemical-potential control.  They are not silently
  identified after the candidate veto.

### FREEDOM_LEDGER

- new fields, metrics, sources, action operators, fitted parameters and fitted
  functions: zero;
- candidate choice: one local extension `p_n^5=n_C/n_infinity`, frozen
  before evaluation;
- inherited universal function: `rho_C(n_C)`, restricted only by the
  W3-54 health interval;
- background normalization: `n_infinity>0`, which cancels from the
  logarithmic decision;
- object-specific coefficients, profiles, switches, thresholds and data
  freedoms: zero.

### DEPENDENCIES

Hash-locked logical inputs:

| Role | File | SHA-256 |
|---|---|---|
| Homogeneous phase-density map and current | `Cosmology_and_LSS/Active_Participation_Resonance_Feedback/w3_50_neutral_collective_phase_density_bridge_contract.md` | `c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635` |
| One charge, two density measures and normalized volume Jacobian | `Cosmology_and_LSS/CMB_Closure/w3_62_cmb_einstein_source_linear_closure_preregistration.md` | `b4068791b63e9a072a897e9aa85eae96c588b0d33533effb9664ffbd667ae810` |
| Generated W3-62 density-map result | `Cosmology_and_LSS/CMB_Closure/w3_62_result.json` | `ebc772b6dae31d395aaf4635095ef8ea01333da6ffeb31bbe0c30da703cac8d1` |
| Positive-mass static operational dictionary | `Lagrangian_Formulation/Weak_Field_Closure/w3_51_weak_field_closure_contract.md` | `86bc2ed86cddee36bec5e46fdfa407701107290c783bfa81ba1440b96becc7cf` |
| Generated W3-51 status | `Lagrangian_Formulation/Weak_Field_Closure/w3_51_result.json` | `a74e0f02c5a5c794723a5797049bd28d95684a95be869db30f10a575d3ee9cf8` |
| One-coframe phase action and health interval | `Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md` | `6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879` |
| Generated W3-54 closure record | `Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_result.json` | `ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991` |
| Strong-field response admissibility boundary | `Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_foundation_strong_field_response_preregistration.md` | `31e6520d9b7917413b9f2978291b4a77f067abe8dd3d6a9e89e1b2cfb699da11` |
| Generated W3-67 boundary record | `Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_result.json` | `659bdfe171a8279b465fdd49eaf590755da22a7522a83053a4a06450fd745385` |
| Exterior failure of the matter-only algebraic carrier | `Strong_Field/W3-69_Algebraic_Material_Response_Candidate/w3_69_algebraic_material_response_candidate_preregistration.md` | `b5ef9e7a7740fae6d8fbf8b42058ea275afb96b6a801c5c4a5ce0e83cebd0c38` |
| Generated W3-69 role decision | `Strong_Field/W3-69_Algebraic_Material_Response_Candidate/w3_69_result.json` | `ad3d0315acfe2276ecf0d7f3c6d60d89e06bae39afc18fc34d35138742626f22` |

Expected upstream status:

- W3-50 ends with
  `PASS_EXACT_CONDITIONAL_NEUTRAL_PHASE_DENSITY_CANDIDATE_CURRENT__W3_48_BRIDGE_CLOSED_GIVEN_SELECTED_ETA_AND_CUBIC_MEASURE__MASTER_FOUNDATION_ORIGIN_OPEN`.
- W3-62 has `aggregate_pass=true`, one conserved charge with two distinct
  volume measures, normalized Jacobian exponent `3`, and operational dilution
  `nHat_C,op=A^(-3)`; only this measure identity is inherited, not a global
  cold-EOS restriction or a local inhomogeneous foundation geometry.
- W3-51 has `gate_status=PASS`, `beta=gamma=1`, and strong field
  `NOT_TESTED`.
- W3-54 has its exact TEGR/EH plus phase-current status, derives the phase
  current and Hilbert tensor, and keeps `P_F_EQUALS_P_C_DERIVED=false`.
- W3-67 has a valid passing boundary artifact and keeps the active response
  open.
- W3-69 has a valid passing audit, rejects its matter-only algebraic factor
  as operational `p`, and leaves the global strong-field solve unopened.

Work 2, old theory folders, archived files, and intuitive prose are neither
evidence nor dependencies.

### METHOD

1. Verify all dependency hashes and required upstream status fields.
2. Derive the stationary no-flux first integral from the frozen W3-54
   `J^mu` equation.
3. Express the W3-54 sound speed as the logarithmic slope
   `d ln(mu)/d ln(n_C)`.
4. Reconstruct the homogeneous Jacobian from `a_F`, `A=a_F/p`, and conserved
   charge in both measures, deriving `nHat_C,op=p^5`. Reject the old
   `nHat_C,op=p^2` conflation through the same validator.
5. Combine the Bernoulli residual
   `c_s^2 d ln(n_C)+d ln(calN)=0` with the candidate residual
   `d ln(n_C)-2d ln(calN)=0`.
6. Solve the joint residuals on a nonconstant exterior and compare the result
   with the frozen health interval.
7. Evaluate the weak positive-mass sign independently.
8. Run the inverse-density and chemical-potential controls.
9. Audit one-metric/one-source preservation, package cleanliness, immutable
   CODES/intuitive controls, and false scope flags.
10. Apply every mutation through the same production validators.

Required universal gates are G0 through G6.  G7 is N/A because no datum or new
observable enters.  G8 is N/A because this stage changes no Canon, intuitive,
or article file.

### PASS_CONDITION

The audit passes when dependency and immutable-control hashes are exact; the
W3-54 stationary no-flux equation yields `mu calN=mu_infinity`; its logarithmic
slope equals the registered sound speed; the candidate and Bernoulli
residuals jointly require `c_s^2=-1/5` on every nonconstant branch; that
value fails the W3-54 health interval; the independent weak-sign check agrees;
the zero-sound-speed endpoint fails regular response; the inverse-density and
chemical-potential controls give their registered outcomes; one metric,
one once-counted source, and the upstream Einstein/1PN branch remain
unchanged; the candidate is rejected; every scope flag remains false; all
mutations are detected; and the package contains exactly three files.

### FAIL_CONDITION

The gate fails if any hash, status, exact residual, sign, health bound,
control, package, immutable file, density measure, or mutation differs from the registration;
if the homogeneous W3-50 map is misreported as already valid locally; if the
candidate is accepted by silently allowing `c_s^2<0`; if the inverse map is
substituted for the frozen candidate; if the total static lapse is confused
with a radial metric function; if the temporal factor is promoted to an exact
full strong-field coframe; if a new action/source is inserted; or if a global
solution or singularity result is promoted.

### FALSIFIER

An exact counterexample to the stationary first integral or slope algebra
under the frozen assumptions falsifies this audit.  A future derived
multivariate bridge, mixed operator, or different carrier does not falsify
the rejection of this single-density extension; it supplies the new physical
input and creates a new model version.

### RESIDUAL

- homogeneous measure residual: `nHat_C,op-p^3 nHat_C,F=0`;
- operational density-power residual: `nHat_C,op-p^5=0`;
- conserved operational-charge residual: `nHat_C,op A^3-1=0`;
- Bernoulli differential residual:
  `R_B=c_s^2 d ln(n_C)+d ln(calN)=0`.
- candidate residual:
  `R_p=d ln(n_C)-5 d ln(calN)=0`.
- joint nonconstant-branch residual:
  `(5c_s^2+1)d ln(calN)=0`.
- health residual at the matched candidate point:
  `c_s^2+1/5=0`, with `c_s^2=-1/5` outside `[0,1]`.
- weak sign and both control residuals: exact symbolic values recorded by the
  verifier.

### ERROR_BOUND

Zero for algebra, hashes, Boolean status checks, and the first-order
coefficient decision.  The weak series has an `O(u^2)` remainder, but the
opposite nonzero linear coefficients decide the gate independently of that
remainder.  No numerical integration or observational uncertainty enters.

### VALIDITY_HEALTH

The W3-54 phase sector is retained only on
`rho_C'>0`, `0<=c_s^2<=1`.  The required `c_s^2=-1/5` is a gradient-
stability veto for this candidate role.  The gate leaves the accepted phase
action healthy in its original domain and inserts no new degree of freedom,
characteristic cone, strong coupling, or source.  Health of a future
multivariate bridge or new carrier requires a separate action-level audit.

### BRANCHES

- `FROZEN_HOMOGENEOUS_PHASE_DENSITY`: retained exactly in its W3-50 domain.
- `TESTED_LOCAL_DENSITY_EXTENSION`: rejected by the exact health/sign veto.
- `CHEMICAL_POTENTIAL_LAPSE_READOUT`: exact stationary passive identity.
- `INVERSE_DENSITY_CONTROL`: healthy static sign at `c_s^2=1/5`, but a
  different homogeneous dictionary and therefore a new model.
- `ZERO_SOUND_SPEED_ENDPOINT`: no regular finite linear response to a
  varying lapse.
- `BRANCH_SENSITIVE_OR_DIFFERENT_CARRIER`: admissible future class, not
  selected here.

### OBSERVABLE_MAP

No new observable is added.  The comparison uses the already frozen
positive-mass temporal operational factor `p_op=calN=exp(-u)`.  The result is a
carrier-selection veto, not a new prediction.

### FORWARD_MODEL

`N/A`; no instrument, catalogue, likelihood, synthetic observation, or
population model enters.

### DATA_ROLE

`NO_DATA_READ_OR_FITTED`.

### IDENTIFIABILITY

The current inputs identify the failure of the single-variable extension
`p_n^5=n_C/n_infinity`.  They do not identify a unique replacement.
The inverse-density and chemical-potential controls demonstrate that the
static exterior alone cannot choose between a revised density dictionary, a
multivariate bridge, and a different carrier.  Homogeneous continuity,
static hydrostatics, action health, and 1PN screening must be imposed
together in the next candidate gate.

### BENCHMARK

Required exact values:

```text
d ln(mu)+d ln(calN) = 0,
d ln(mu)=c_s^2 d ln(n_C),
d ln(n_C)=5 d ln(calN)           [tested candidate],
c_s^2_required=-1/5,
c_s^2_inverse=+1/5,
p_mu=mu_infinity/mu=calN,
d ln(p_homogeneous)/d ln(n_C,op)=+1/5,
d ln(p_inverse)/d ln(n_C,op)=-1/5.
```

### CLOSURE_FLAGS

All atomic flags start false.

Required true:

- `g0_goal_pass`
- `g1_conventions_pass`
- `g2_core_algebra_pass`
- `g3_structure_pass`
- `g4_independent_check_pass`
- `g5_limits_regression_pass`
- `g6_physical_match_pass`
- `g7_observation_not_applicable_exact`
- `g8_export_not_applicable_exact`
- `dependency_hashes_exact`
- `upstream_status_and_scope_exact`
- `one_charge_two_measure_jacobian_exact`
- `operational_density_fifth_power_exact`
- `immutable_controls_exact`
- `candidate_local_extension_registered_exact`
- `static_total_lapse_and_no_flux_branch_registered_exact`
- `phase_bernoulli_first_integral_exact`
- `sound_speed_log_slope_exact`
- `positive_mass_operational_lapse_sign_exact`
- `healthy_density_response_sign_exact`
- `candidate_joint_residual_requires_cs2_minus_fifth_exact`
- `required_cs2_violates_w3_54_health_exact`
- `zero_sound_speed_regular_response_rejected_exact`
- `inverse_density_control_matches_at_cs2_fifth_exact`
- `inverse_density_control_breaks_homogeneous_dictionary_exact`
- `chemical_potential_lapse_readout_exact`
- `chemical_potential_map_is_passive_exact`
- `temporal_only_scope_and_coframe_split_preserved_exact`
- `one_metric_one_source_no_new_action_exact`
- `upstream_einstein_and_1pn_branch_unchanged_exact`
- `candidate_role_rejected_before_global_solve_exact`
- `next_missing_premise_narrowed_exact`
- `mutation_controls_pass`
- `package_clean_pass`
- `aggregate_gate_pass`

Required false:

- `candidate_admissible`
- `collective_density_universal_local_operational_p_derived`
- `accepted_homogeneous_phase_law_falsified`
- `healthy_barotropic_eos_realizes_frozen_candidate`
- `P_F_equals_p_C_derived`
- `exact_common_factor_full_strong_field_coframe_derived`
- `branch_discriminator_derived`
- `multivariate_response_bridge_derived`
- `alternative_carrier_selected`
- `active_mixed_response_action_derived`
- `foundation_strong_field_response_derived`
- `global_strong_field_solve_opened`
- `black_hole_solution_derived`
- `penrose_hypothesis_change_selected`
- `singularity_resolution_completed`
- `new_strong_field_prediction_derived`
- `observation_tested`

### CROSSCHECK

The measure regression reconstructs the operational density directly from
`A^(-3)` and independently from `p^3 a_F^(-3)`. It rejects an old-density
mutation that substitutes `p^2`, along with wrong Jacobian exponents.
The primary route solves the exact differential residuals.  The independent
route uses monotonicity: `calN<1` implies `mu>mu_infinity`; a healthy
`mu'(n_C)>=0` implies `n_C>=n_infinity`, while
`p_n=calN<1` and `p_n^5=n_C/n_infinity` require
`n_C<n_infinity`.  The inverse-density and chemical-potential controls
separately reproduce the sign boundary.  Mutations change the Bernoulli sign,
density exponent, health interval, zero-sound endpoint, total-lapse role,
temporal scope, source ledger, candidate decision, dependency integrity,
package contents, or global-solve flag and must fail through the same
validators.

### PROVENANCE

The verifier pins this preregistration, all dependencies, `CODES.md`, and
the complete recursive intuitive-file manifest by SHA-256.  It records the
source hash, Python, SymPy, platform, UTC, exact algebra, status registries,
mutations, package contents, `network_used_by_verifier=false`, and
`archived_theory_used=false`.  Strict finite UTF-8 JSON is written
atomically.

### FILES

- `w3_70_collective_phase_carrier_admissibility_preregistration.md`
- `w3_70_collective_phase_carrier_admissibility.py`
- generated `w3_70_result.json`

### STOP_RULE

Stop after the exact stationary sign/health audit rejects or accepts the
single-density carrier role.  A rejected candidate does not open an
alternative-action search, EOS construction, global compact-object solve,
black-hole calculation, observation, or manuscript update.

## Decision semantics

Passing W3-70 means that the natural use of the already retained collective
phase density as one universal local operational factor has received a hard
action-level health/sign decision.  The passing rejection leaves the
homogeneous W3-50 law and W3-54 source intact, eliminates one apparently
minimal carrier, and narrows the missing premise to a derived
branch-sensitive bridge or a different healthy carrier.

The passing status is

```text
PASS_EXACT_STATIONARY_PHASE_BERNOULLI_AND_RESPONSE_SIGN_AUDIT__REJECTED_AS_UNIVERSAL_LOCAL_P_CARRIER_BY_HEALTHY_EOS_SIGN_CONTRADICTION__GLOBAL_STRONG_FIELD_SOLVE_NOT_OPENED
```
