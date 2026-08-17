# W3-39 Preregistration: Genesis Energy, Phase, and Causality Gate

**CLAIM_ID:** `W3_39_GENESIS_ENERGY_PHASE_CAUSALITY`

**CLAIM:** For a post-origin multi-sector description with antisymmetric
internal transfers, local continuity, and a regular moving boundary, total
energy and phase-conversion signs obey exact ledgers; under the frozen
global-centerless birth postulate, a single strictly distance-graded centered
explosion is a conditional incompatibility rather than a Genesis mechanism.

**TYPE:** `EXACT_CONSERVATION_SIGN_LEDGER_AND_CENTERED_BIRTH_SYMMETRY_NO_GO`.
PASS validates bookkeeping identities and the declared conditional
incompatibility only. It does not derive the Genesis mechanism, an equation of
state, a phase transition, temperature, expansion, or observations.

**MODEL_VERSION:** `W3-39-v1.0-ENERGY-PHASE-CAUSALITY`. Any change to the
sector-transfer convention, moving-boundary ledger, phase sign convention,
centered-front witness, closure flags, or scope creates a new version.

**ASSUMPTIONS:**

1. Physical process time begins at the finite origin; all differential ledgers
   apply only after the first active slice.
2. Three illustrative post-origin sectors `F`, `C`, and `R` exchange energy
   through antisymmetric internal transfers. Positive `q_I` injects energy
   into sector `I`; their sum is zero.
3. The homogeneous perfect-fluid consequence uses one supplied process Hubble
   rate `H_tau`; it does not derive the background.
4. The local spherical moving-boundary check uses a flat physical Eulerian
   radius, local continuity, signed bulk source, signed outward flux, and a
   signed boundary speed. A regular center has zero central flux primitive.
   `F=r^2 J_r` and `Q_V=int_0^R r^2 S dr` are per unit solid angle; the total
   energy ledger carries an external factor `4 pi`.
5. A sharp phase interface without surface source obeys the supplied local
   Rankine-Hugoniot balance. `in` is the tracked active side; the normal points
   from `in` to `out`; positive `J_n` and `v_n` point outward.
6. Phase fraction `X` converts an unactivated bookkeeping phase `U` into an
   active phase `A`. The latent sign is classified, not chosen physically.
7. The centered-explosion incompatibility is tested on a vertex-transitive
   five-cycle with activation time strictly increasing with distance from one
   selected vertex. The cycle is a logical witness, not cosmic topology.
8. Global centerless birth remains a frozen scenario postulate, not a result.

**DOMAIN:** Exact post-origin sector algebra; one local spherical patch; one
sharp-interface sign check; one finite transitive-graph no-go witness. No
pre-birth conservation law, total cosmic radius, physical topology, thermal
history, or observable forward model is asserted.

**CONVENTIONS:** `q_I>0` is sector injection. `J.n>0` leaves the tracked active
domain. `v_n>0` expands its boundary and adds swept energy already present at
the boundary. `Q_V` is signed bulk injection. `[Y]=Y_out-Y_in`. For `X'>0`,
`L=rho_U-rho_A>0` is release to recipient sectors; `L<0` requires input. The
word `melting` is reserved for the endothermic branch and remains unestablished.
Pair-transfer signs are `q_FC>0: F->C`, `q_FR>0: F->R`, and
`q_CR>0: C->R`.

**FREEDOM_LEDGER:** Current fitted effective dimension is `d_eff=0`; all
physical freedoms remain open:

- `genesis_action_initial_charge`: source = foundation action/boundary rule;
  domain = first active slice; scale = `universal`;
  effective_complexity_measure = functional/infinite-dimensional action plus
  initial charge constraint.
- `sector_stress_transfer_matrix`: source = sector field equations; domain =
  post-origin sectors; scale = `group`; effective_complexity_measure = stress
  tensor and antisymmetric transfer functions per sector pair.
- `phase_free_energy_interface`: source = thermodynamic field theory; domain =
  each phase/interface family; scale = `group`; effective_complexity_measure =
  EOS, free energy, surface terms, and kinetic functional per family.
- `local_seed_boundary_history`: source = local activation dynamics; domain =
  each seed/domain; scale = `object`; effective_complexity_measure = one moving
  boundary and flux history per object.
- `future_thermal_observable_calibration`: source = future likelihood; domain =
  each datum; scale = `data`; effective_complexity_measure = `N_nuisance=0`
  because no data are read.

**DEPENDENCIES:** None. W3-39 is self-contained and imports no W3-37/W3-38
result or manuscript.

**METHOD:** Exact SymPy substitution of antisymmetric transfers; exact
Leibniz differentiation, local continuity, and fundamental theorem of calculus;
exact interface and phase cancellation; finite graph automorphism/invariance
check; negative mutations; exact schemas; strict atomic JSON and SHA-256.

**PASS_CONDITION:** Sector sources cancel; total continuity follows; the full
moving-boundary ledger and regular-center specialization have zero residual;
omitted sweep/flux/center terms and a flipped interface sign are detected;
interface and phase ledgers cancel; all three latent-sign branches are
classified; the centered radial
activation record fails transitive invariance; schemas/mutations pass; all
physical flags remain false; aggregate is the AND of atomic checks.

**FAIL_CONDITION:** Any exact ledger fails; an internal transfer creates net
energy; boundary sweep or central flux is silently dropped; latent energy is
double counted; a sign branch is called physically selected; a centered front
is called centerless; constant active energy or heating/cooling is asserted
without closure; or any physical flag becomes true.

**FALSIFIER:** An exact counterexample under the frozen algebra falsifies this
gate only. It neither falsifies nor validates RefG.

**RESIDUAL:** Exact symbolic zero residuals and finite invariance predicates.

**ERROR_BOUND:** Zero algebraic error; numerical/observational error N/A.

**VALIDITY_HEALTH:** PASS establishes conservation/sign discipline and rejects
one centered distance-graded birth construction under supplied transitive
symmetry. It does not exclude later local centered fronts. Genesis dynamics,
phase physics, and all observations remain open.

**BRANCHES:** `ANTISYMMETRIC_SECTOR_LEDGER`, `LOCAL_MOVING_BOUNDARY`,
`REGULAR_CENTER`, `SHARP_INTERFACE_NO_SURFACE_SOURCE`,
`EXOTHERMIC_CONVERSION`, `NEUTRAL_CONVERSION`, `ENDOTHERMIC_CONVERSION`,
`CENTERED_RADIAL_FRONT_MUTATION`, `GLOBAL_CENTERLESS_POSTULATE`.

**OBSERVABLE_MAP:** N/A. No map to temperature, redshift, clocks, distances,
abundances, or structure is derived.

**FORWARD_MODEL:** N/A. No physical Genesis simulation or likelihood.

**DATA_ROLE:** No data are read.

**IDENTIFIABILITY:** The gate identifies transfer cancellation,
moving-boundary terms, phase-sign bookkeeping, and one symmetry conflict. It
does not identify the sectors, initial energy, EOS, latent sign, transfer
matrix, expansion, oscillon spectrum, temperature, or observables.

**BENCHMARK:** Three-sector antisymmetric source sum zero; Reynolds/Leibniz
residual zero including the central term; regular-center ledger zero;
`v[rho]=[J]`; `conversion_only_rate+L X'=0`, with the phase-background
derivatives retained separately; five-cycle radial activation times
`(0,1,2,2,1)` are changed by a one-step translation.

**CLOSURE_FLAGS:**

Exact/computational flags, all required true:

- `antisymmetric_transfer_sum_exact`
- `total_sector_continuity_exact`
- `moving_boundary_leibniz_FTC_exact`
- `regular_center_spherical_ledger_exact`
- `boundary_sweep_and_center_terms_required_exact`
- `rankine_hugoniot_balance_exact`
- `latent_transfer_cancellation_exact`
- `latent_sign_classifier_exact`
- `centered_explosion_breaks_transitive_invariance_exact`
- `branch_keysets_exact`
- `schema_keysets_exact`
- `mutation_controls_pass`
- `aggregate_identity_pass`

Physical flags, all required false:

- `pregeometric_state_space_derived`
- `genesis_action_or_Hamiltonian_derived`
- `origin_trigger_or_boundary_condition_derived`
- `initial_energy_charge_derived`
- `sector_stress_tensors_derived`
- `sector_transfer_matrix_derived`
- `foundation_volume_measure_derived`
- `foundation_energy_balance_derived`
- `phase_free_energy_EOS_derived`
- `latent_heat_sign_derived`
- `surface_tension_interface_terms_derived`
- `entropy_current_time_arrow_derived`
- `activation_field_and_front_eom_derived`
- `global_centerlessness_derived`
- `physical_cosmic_topology_derived`
- `proto_oscillon_solution_derived`
- `tail_energy_flux_derived`
- `percolation_dynamics_derived`
- `stable_oscillon_spectrum_derived`
- `background_expansion_derived`
- `cadence_history_derived`
- `thermal_history_derived`
- `CMB_BBN_structure_validated`
- `observable_forward_model_derived`
- `data_validated`

**CROSSCHECK:** Independent sector-sum and total-continuity routes; general and
regular-center moving-boundary routes; missing-term mutations; phase derivative
and recipient-source cancellation; explicit five-cycle translation.

**PROVENANCE:** The source pins this preregistration's raw SHA-256 and records
its own hash, Python/SymPy/platform versions, UTC, LF convention, and paths.
Strict finite JSON and its checksum are atomically replaced.

**FILES:** `w3_39_energy_phase_causality_preregistration.md`,
`w3_39_energy_phase_causality.py`, `w3_39_result.json`, and
`w3_39_result.sha256`.
