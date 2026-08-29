# W3-45 Preregistration: Active-Phase Lambda Interface

## Target and stopping rule

This stage has one bounded target: determine the exact condition under which a
homogeneous active-phase energy contribution becomes the already registered
cosmological-constant term in the operational RefG action, distinguish that
condition from a constant total cell energy and from the cadence state
`P_F`, and expose the remaining microscopic nonselection.

The stage stops after dependency verification, the exact
energy--pressure--equation-of-state dictionary, continuity and reduced-action
matching, the phase-sign and bare/phase degeneracy checks, negative mutations,
and report-schema validation. It introduces no potential family, numerical
`Lambda`, fit, data, plot, result file, or follow-on calculation.

## Claim contract

- `CLAIM_ID`:
  `W3_45_ACTIVE_PHASE_LAMBDA_INTERFACE`
- `CLAIM`:
  Given a homogeneous stationary active-phase contribution already matched to
  the operational volume, `E_star=epsilon_star V_op` with constant
  `epsilon_star` is exactly equivalent to a cosmological term
  `Lambda_phase=8 pi G epsilon_star/c0^4` and has
  `P_star=-epsilon_star` and `w_star=-1`. A constant total energy in a fixed
  comoving cell instead has `P=0` and `w=0`. The current upstream ontology
  supplies an unactivated/active phase ledger and distinct pressure roles but
  does not derive `epsilon_star`, its operational matching, or a condition
  setting an independent bare cosmological term to zero; therefore only the
  exact interface and its nonselection are closed.
- `TYPE`:
  `EXACT_CONDITIONAL_EFT_INTERFACE_AND_MICROPHYSICAL_NONSELECTION`.
- `MODEL_VERSION`:
  `W3-COSMOLOGY-v1.3-ACTIVE-PHASE-LAMBDA-INTERFACE`. A change to the
  operational-volume convention, phase-gap sign, pressure definition,
  bare/phase split, dependency registry, mutation set, or claim scope creates
  a new version.
- `ASSUMPTIONS`:
  1. W3-39 passes its post-origin conservation and phase-sign ledger. Its
     `U` label is an unactivated bookkeeping phase on that post-origin
     ledger, not the pre-geometric or pre-birth foundation. Its phase free
     energy, latent sign, Genesis mechanism, and equation of state remain
     open.
  2. W3-40 passes its single-driver causal dictionary: foundation expansion,
     pressure relaxation, and material contraction are ordered stages of one
     trajectory read through `A=a/p`.
  3. W3-41 passes its exact conditional energy--mechanical-stress interface
     while keeping the cadence scalar `P_F`, mechanical pressure `Pi_F`, and
     thermal pressure distinct.
  4. The selected operational EFT passes with homogeneous volume
     `V_op=V_op0 A^3` and reduced vacuum term
     `-N A^3 Lambda c0^4/(8 pi G)`. Its `Lambda` value remains underived.
  5. `epsilon_star` is supplied at this interface as a homogeneous
     stationary energy density in operational units. Its derivation from an
     oscillon/foundation action and the foundation-to-operational
     energy/measure map are not assumptions hidden in this gate.
  6. The main positive branch has `epsilon_star>0`. Zero and negative
     branches are retained only for the exact sign dictionary.
  7. The thermodynamic pressure conjugate to operational volume is
     `P=-dE/dV_op` at fixed phase charges.
  8. The post-Genesis domain tested here is a regular active interior. A
     moving activation boundary remains governed by the W3-39 flux, sweep,
     source, and phase-conversion ledger.
- `DOMAIN`:
  Positive `V_op`, `A`, `c0`, and `G` on the homogeneous connected
  post-Genesis operational branch. The exact `w` ratios use nonzero energy
  density. The first active slice, a moving activation front, local compact
  objects, inhomogeneous phase mixtures, thermal history, quantum
  corrections, and observational inference are outside the gate.
- `CONVENTIONS`:
  `epsilon` and `P` have energy-density units and `w=P/epsilon`. W3-39's
  symbols `rho_U` and `rho_A` are energy-density bookkeeping symbols; W3-45
  relabels them `epsilon_U` and `epsilon_A` without changing units. Thus
  `L=epsilon_U-epsilon_A` and
  `epsilon_star=epsilon_A-epsilon_U=-L`. The active phase here means the
  homogeneous manifested post-Genesis vacuum of an already-connected
  operational interior. The matched `U`-phase baseline is carried inside
  `Lambda_bare`, while `epsilon_star` is the active-minus-`U` gap.
  `P_star` is vacuum stress and is never renamed `P_F` or `Pi_F`.
- `FREEDOM_LEDGER`:
  1. `epsilon_star`: source = future two-phase foundation/oscillon action and
     matching; scale = universal; effective complexity = one underived
     constant at this interface.
  2. `Lambda_bare`: source = microscopic gravitational action or matching
     condition; scale = universal; effective complexity = one underived
     constant.
  3. Only
     `Lambda_eff=Lambda_bare+8 pi G epsilon_star/c0^4` enters the current
     homogeneous operational action. No value is fitted and no extra
     observable freedom is introduced by rewriting this sum.
  4. A general varying `epsilon_star(A)`, order-parameter potential, new field,
     transition profile, radiative correction, or nuisance parameter is
     excluded from this version.
- `DEPENDENCIES`:
  1. W3-39 result SHA-256:
     `ff2440311e2c4ceb5fe5a2393b6730d2a3c2a2c49dd5b2ceaf7e32f0a0ab1160`.
  2. W3-39 checksum-file SHA-256:
     `6a15bdd5234330443b27d865d7b9c223b9edb3de621480d954b8df1f55f6e294`.
  3. W3-40 result SHA-256:
     `6d16003df1f2d7a70371ec254f9cfc1692b7eac3df53874616135792eb2d63cf`.
  4. W3-40 checksum-file SHA-256:
     `6e0449c73d85d331d3dcf664cdabbbc6be0c4cb15fb520617dcd0aaaea749b5f`.
  5. W3-41 preregistration SHA-256:
     `4e19d4d0ece49a3f126cf24be3c2275923de5a291db29efad01b68332fdd7658`.
  6. W3-41 verifier SHA-256:
     `b22ad1cdff8754f791b8955a6408e11e8324cb4380ed8dab321c2b1f0f76a9f3`.
  7. Conditional operational-background verifier SHA-256:
     `57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055`.
- `METHOD`:
  1. Verify all frozen files, upstream statuses, open flags, checksum
     contents, canonical text, W3-40 single-driver semantics, and W3-41
     pressure roles.
  2. Starting from `V_op=V_op0 A^3` and
     `E=epsilon(A)V_op`, derive
     `P=-epsilon-(A/3)d epsilon/dA`.
  3. On constant `epsilon_star`, verify `P_star=-epsilon_star`,
     `w_star=-1`, and the homogeneous continuity residual.
  4. Match `-N A^3 epsilon_star` to the existing reduced
     Einstein--Hilbert `Lambda` term and verify both
     `Lambda_phase=8 pi G epsilon_star/c0^4` and the Friedmann-source
     identity.
  5. Prove within `E=k V^n` that constant density and `w=-1` select
     `n=1`, while a constant total fixed-cell energy has `n=0` and `w=0`.
  6. Verify `epsilon_star=-L` and the positive/zero/negative
     `Lambda_phase` to W3-39 latent-sign dictionary.
  7. Verify that a common constant shift of two phase potentials cancels from
     their gap, while a constant shift of one local potential leaves its
     Euler--Lagrange derivative unchanged. This establishes why local
     dynamics alone does not select the gravitating offset.
  8. Verify the exact
     `(Lambda_bare,epsilon_star)` degeneracy at fixed `Lambda_eff` and detect
     all frozen mutations.
- `PASS_CONDITION`:
  All dependency, checksum, status, open-flag, role, exact-identity, branch,
  mutation, and schema checks pass; all microscopic, numerical,
  observational, and pressure-identification flags remain false.
- `FAIL_CONDITION`:
  Any dependency or exact residual fails; the pressure sign is reversed; a
  constant total cell energy is promoted to `Lambda`; the phase contribution
  is added twice; `Lambda_bare` is hidden; `P_star` is identified with
  `P_F` or `Pi_F`; flatness is reported as a microphysical derivation; a
  potential/value/sign is invented; or an open flag becomes true.
- `FALSIFIER`:
  Failure of any exact identity under the registered assumptions falsifies
  this interface. A microscopic active-phase action that produces a
  nonstationary operational density, a different stress tensor, or no
  positive stable gap rejects this `Lambda` mechanism while leaving other
  RefG branches logically open.
- `RESIDUAL`:
  Exact symbolic residuals for pressure, equation of state, continuity,
  reduced-action and Friedmann matching, scaling selection, phase-gap signs,
  potential shifts, and bare/phase reparameterization.
- `ERROR_BOUND`:
  Zero symbolic error. Numerical, approximation, and observational errors are
  `N/A` because no floating-point calculation or data are used.
- `VALIDITY_HEALTH`:
  Require finite positive main-branch symbols, nonzero denominators, exact
  upstream/open-state preservation, distinct pressure roles, one
  representation of the phase contribution in `Lambda_eff`, no file writes,
  and deterministic output.
- `BRANCHES`:
  `POSITIVE_ACTIVE_PHASE_OFFSET`, `ZERO_PHASE_GAP`,
  `NEGATIVE_ACTIVE_PHASE_OFFSET`, `FIXED_TOTAL_CELL_ENERGY`,
  `EXPLICIT_BARE_PLUS_PHASE_SPLIT`, and
  `CONDITIONAL_PHASE_REPLACEMENT_OF_EXISTING_LAMBDA`. The last branch requires
  `Lambda_bare=0` and is not selected here.
- `OBSERVABLE_MAP`:
  `N/A` for direct data. The gate ends at the exact effective-action source
  `Lambda_eff`; W3-43/W3-44 observables remain downstream and unchanged.
- `FORWARD_MODEL`:
  `N/A`. No source, instrument, selection, calibration, covariance, or
  likelihood chain is used.
- `DATA_ROLE`:
  `NO_DATA_READ_OR_FITTED`.
- `IDENTIFIABILITY`:
  The operational background identifies only `Lambda_eff`.
  `epsilon_star -> epsilon_star+delta_epsilon` and
  `Lambda_bare -> Lambda_bare-8 pi G delta_epsilon/c0^4` leave it
  invariant. A two-phase microscopic action, operational matching, and a
  bare-term condition are required to identify the decomposition and value.
- `BENCHMARK`:
  The already selected operational Einstein--Hilbert `Lambda` term. The
  metric is exact zero residual; no model-selection score is defined.
- `CLOSURE_FLAGS`:
  Independent literal required-true and required-false registries are frozen
  in the verifier. The aggregate is their logical conjunction after exact
  schema validation.
- `CROSSCHECK`:
  Independent thermodynamic, continuity, reduced-action, Friedmann-source,
  scaling-family, phase-gap, and reparameterization routes; frozen negative
  mutations.
- `PROVENANCE`:
  Frozen local dependency hashes; Python and SymPy versions emitted at
  runtime; deterministic canonical JSON to stdout; no output file.
- `FILES`:
  1. `w3_45_active_phase_lambda_interface_preregistration.md`
  2. `w3_45_active_phase_lambda_interface.py`
  3. Parent `Cosmology_and_LSS/README.md` ledger entry.

## Frozen negative controls

The verifier must detect all of the following:

1. `wrong_pressure_sign`: use `P=+dE/dV`.
2. `fixed_total_energy_promoted_to_lambda`: treat `E=C` as constant density.
3. `quadratic_volume_energy_promoted_to_lambda`: use `E=k V^2`.
4. `wrong_lambda_factor_two`: use
   `Lambda_phase=4 pi G epsilon_star/c0^4`.
5. `wrong_latent_sign`: identify `epsilon_star=L`.
6. `double_counted_phase_contribution`: use
   `Lambda_eff=Lambda_bare+2 Lambda_phase`.
7. `hidden_bare_term`: report `Lambda_eff=Lambda_phase` while retaining a
   symbolic nonzero `Lambda_bare`.
8. `vacuum_pressure_renamed_cadence_pressure`: identify `P_star=P_F`
   despite the frozen role and sign distinctions.

## Decision semantics

The pass status is
`PASS_EXACT_CONDITIONAL_ACTIVE_PHASE_LAMBDA_INTERFACE__ABSOLUTE_ENERGY_NORMALIZATION_AND_LAMBDA_VALUE_OPEN`.
It establishes the unique constant-operational-density interface and its
nonselection boundary. It is not `MECHANISM_DERIVED`, does not calculate
`Lambda`, and does not alter any intuitive manuscript in this stage.
