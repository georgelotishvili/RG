# W3-47 Preregistration: Post-Genesis Participation Kernel

## Working frame

- One target: close the minimum homogeneous post-Genesis state law selected
  by W3-46.
- Immediate obstacle: the ontology fixes the directions of change but leaves
  the pressure map, locked-coupling magnitude, and time law unspecified.
- Minimum result: one pressure--participation map, one locked-coupling rule,
  one exact state equation, its fixed-point classification, and one declared
  conditional energy/flux bookkeeping partition.
- Allowed artifacts: this preregistration, one no-write symbolic verifier, the
  W3-46 downstream-handoff trace, the parent cosmology ledger, and the
  dependent low-energy architecture record.
- Stopping rule: finish after the exact pullback, registered identities,
  internal-transfer cancellation, stability, dependency, and mutation checks.
  No potential family, PDE, numerical
  solution, likelihood, or follow-on stage enters.

## Claim contract

- `CLAIM_ID`: `W3_47_POST_GENESIS_PARTICIPATION_KERNEL`.
- `CLAIM`: Conditional on the normalized maps
  `P_F/P_F0=eta` and `c_lock=p=sqrt(eta)`, the selected cubic
  relaxation closure and flat expanding operational Einstein--Hilbert
  background give one exact homogeneous state law,
  `eta'=-(6/5)H_A eta`. The pullback is algebraically consistent with the
  inherited ideal identity `Q_rel/Q_rel0=eta a^3=1`, has no positive fixed
  point on the expanding branch, and places localized, non-radiative, and
  freely radiative energy roles in one declared transfer-cancelling ledger.
- `TYPE`: `EXACT_CONDITIONAL_HOMOGENEOUS_MATCHING_AND_ENERGY_ROLE_LEDGER`.
- `MODEL_VERSION`:
  `W3-COSMOLOGY-v1.5-PARTICIPATION-BACKGROUND-MATCHING`. A change to either
  selected map, the cubic volume branch, the operational background equation,
  the sector registry, the stationary-flux rule, or any closure flag creates
  a new version.
- `ASSUMPTIONS`:
  1. The domain is connected and post-Genesis. Its homogeneous participation
     mean is `eta(tau)>0`, with reference normalization `eta_0=1`.
  2. The pressure readout is the selected zero-baseline normalized map
     `P_F/P_F0=eta`.
  3. The normalized locked-trace amplitude
     `c_lock=|J_R_lock|/|J_R_lock,0|` obeys the selected common-coupling rule
     `c_lock=p`.
  4. The inherited ideal branch obeys
     `Q_rel=P_F mathcal_V=constant`,
     `mathcal_V/mathcal_V_0=a^3`, `p^2=P_F/P_F0`, and `A=a/p`.
  5. The operational background is the selected flat expanding
     Einstein--Hilbert branch
     `H_A=H_A0 E(A)>0`, with
     `E(A)^2=Omega_r0 A^-4+Omega_m0 A^-3+Omega_Lambda0`, where
     `Omega_m0>=0`, `Omega_r0>=0`,
     `Omega_m0+Omega_r0<=1`, and
     `Omega_Lambda0=1-Omega_m0-Omega_r0`.
  6. One foundation state is partitioned conditionally for bookkeeping into
     localized phase-locked core content `E_L`; the remaining non-radiative
     foundation response `E_N`, including stationary source-locked dressing
     and homogeneous coherent/tension background; and freely propagating
     radiative content `E_R`. Their nonoverlap is a model-version postulate,
     not a derived microscopic decomposition. Internal transfers are
     antisymmetric.
  7. A stationary source-locked trace has zero cycle-averaged outward
     radiative flux. A changing source may populate `E_R`.
- `DOMAIN`: Homogeneous, isotropic, already-connected, expanding,
  positive-`eta` states on the selected flat leading-EH branch. Local compact
  deficits, Genesis, moving activation fronts, thermal history, strong-field
  tensor profiles, and observational likelihoods are outside this gate.
- `CONVENTIONS`: A prime is `d/dtau`; `H_A=A'/A`; all scale variables
  are positive; `a_0=p_0=A_0=eta_0=c_lock,0=1`; outward radiative flux is
  positive; `E_N` is the non-radiative foundation sector.

- `FREEDOM_LEDGER`:
  - new continuous parameters: zero;
  - new instantiated or fitted functions in the homogeneous kernel: zero;
  - new fitted exponents and data freedoms: zero;
  - fixed structural choices: the two declared normalized maps
    `P_F/P_F0=eta` and `c_lock=p`;
  - open, uninstantiated microscopic functionals: the sector definitions
    `E_L[Phi_F]`, `E_N[Phi_F]`, and `E_R[Phi_F]`; transfer histories
    `T_LN`, `T_LR`, and `T_NR`; the boundary flux/stress map; and
    `I_R/J_R` transport;
  - inherited universal inputs: `H_A0`, `Omega_m0`, `Omega_r0`, the
    flatness-fixed `Omega_Lambda0`, reference normalizations, and an additive
    time origin.
- `DEPENDENCIES`:
  - W3-39 energy-ledger result:
    `ff2440311e2c4ceb5fe5a2393b6730d2a3c2a2c49dd5b2ceaf7e32f0a0ab1160`;
  - W3-40 scale-dictionary result:
    `6d16003df1f2d7a70371ec254f9cfc1692b7eac3df53874616135792eb2d63cf`;
  - W3-42 measure preregistration:
    `8ba44af154a3f9a18b207b4f17a3dcecdb27a8a9d59f7f9aa712c0946763ae98`;
  - W3-42 verifier source:
    `ae30251c3fb5eefae31dd9310de62dda2d3cf700c030bcb8c1e8f08c3e57724f`;
  - W3-42 generated result is a runtime artifact: its byte digest is checked
    against the adjacent checksum, while PASS/closure flags and embedded
    preregistration/source provenance are checked independently;
  - operational background source:
    `57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055`;
  - W3-46 constitutive skeleton:
    `0109ed3d5e8daec55dbd0f01f8b05932e6f653373438455c32a3d26378e0f3b2`;
  - W3-45 active-phase preregistration:
    `1a83a4a4cf9b2fa901cb7ba539d52bac84fd23aab0b79f6d23c2c77861ecd02a`;
  - W3-45 no-write verifier source:
    `7789b0a7e3d875b00dcfe910d67de0c03ef72fda3e2754adf8533d8a22ab2395`.
- `METHOD`: Exact substitution and logarithmic differentiation derive the
  homogeneous dictionary and state law. Direct sector summation checks only
  antisymmetric internal-transfer cancellation. Sign analysis classifies
  fixed points. A no-write SymPy verifier checks these results, flatness,
  frozen dependencies, schemas, and registered mutations by passing both the
  canonical and mutated candidates through the same validator.
- `PASS_CONDITION`: All dependency hashes and registered checks are exact;
  flatness, dictionary, state-law pullback, inherited `Q_rel` identity, and
  sector-transfer sum have zero residual; `eta'<0` for every physical
  expanding state; no positive fixed point exists; the `eta=0` boundary is
  one-sided asymptotically attracting; the stationary radiative-flux rule is
  selected; all mutations are detected; every
  microscopic, observational, and numerical-`Lambda` flag remains false.
- `FAIL_CONDITION`: A dependency, schema, identity, sign, sector sum, or
  mutation check fails; a new decay rate, pressure floor, fitted exponent,
  extra `p` factor, positive fixed point, steady stationary radiation, or
  duplicate energy source is inserted; or a conditional matching result is
  promoted to microscopic dynamics.
- `FALSIFIER`: Failure of either selected map rejects this W3-47 kernel.
  Within the declared maps, a nonzero pullback, registered-identity, or
  internal-transfer residual, a physical positive fixed point on `H_A>0`,
  non-cancelling internal transfer,
  or compulsory steady radiative leakage rejects it.
- `RESIDUAL`: Exact symbolic zero is required for flatness, the scale
  dictionary, background pullback, inherited `Q_rel` identity, and internal
  transfer sum. The stationary-flux condition is a selected registry rule,
  not an independently derived residual.
- `ERROR_BOUND`: Zero algebraic error. Coarse-graining, leading-EH
  truncation, and the two constitutive selections have no calculated
  microscopic error bound. Numerical and data errors are N/A.
- `VALIDITY_HEALTH`: Positive finite states, `H_A>0`, nonnegative fractions
  satisfying the exact flatness sum, exact dependency integrity, monotone
  relaxation, a declared conditional sector registry, and explicit
  boundary/flux terms. The
  `eta=0` endpoint is a boundary limit rather than an interior state.
- `BRANCHES`: The flat expanding branch is selected. For
  `Omega_Lambda0>0` the zero boundary is one-sided exponentially attracting;
  for `Omega_Lambda0=0` with `Omega_m0+Omega_r0>0` it is one-sided
  asymptotically attracting and nonhyperbolic. A positive participation floor
  and an independent decay-timescale branch are rejected by this model
  version.
- `OBSERVABLE_MAP`: `eta -> (P_F,p,a,A)`, followed by the already-selected
  W3-43 ideal map from `A` to redshift and signal dilation. This gate adds
  no new measured factor.
- `FORWARD_MODEL`: N/A; no catalogue, instrument, selection function,
  likelihood, or new observational prediction enters.
- `DATA_ROLE`: `NO_DATA_READ_OR_FITTED`.

- `IDENTIFIABILITY`: The selected operational branch fixes
  `eta=A^(-6/5)`. It cannot distinguish microscopic participation count,
  node separation, and the pressure readout as independent observables.
  `E_L`, `E_N`, `E_R`, their microscopic definitions, normalizations,
  currents, completeness, and transfer histories remain underived.
- `BENCHMARK`: Exact agreement with the frozen cubic relaxation
  dictionary and operational flat-EH equation. The required metric is zero
  symbolic residual; no empirical comparison is performed.
- `CLOSURE_FLAGS`:
  - required true:
    `dependency_hashes_exact`,
    `pressure_participation_map_selected`,
    `locked_coupling_rule_selected`,
    `flatness_constraint_exact`,
    `homogeneous_dictionary_exact`,
    `state_evolution_pullback_exact`,
    `Q_rel_identity_consistency_exact`,
    `eta_monotone_on_expanding_branch_exact`,
    `no_positive_fixed_point_exact`,
    `zero_boundary_stability_classified_exact`,
    `late_boundary_powers_derived_exact`,
    `sector_transfer_cancellation_exact`,
    `stationary_zero_radiative_flux_selected`,
    `operational_source_registry_inherited_unchanged_exact`,
    `mutation_controls_pass`,
    `schema_keysets_exact`;
  - required false:
    `foundation_action_derived`,
    `microscopic_energy_density_derived`,
    `microscopic_energy_transfer_rate_derived`,
    `I_R_or_J_R_transport_derived`,
    `foundation_to_operational_source_map_derived`,
    `positive_fixed_point_derived`,
    `Lambda_value_derived`,
    `new_observation_tested`.
- `CROSSCHECK`: Derive the state law both from
  `A=eta^(-5/6)` and from logarithmic rates; derive each late-boundary power
  from the production right-hand side; independently sum the three
  antisymmetric sector sources; and route every registered mutation through
  the canonical candidate validator.
- `PROVENANCE`: Author ontology dated 2026-08-22; W3-39, W3-40, W3-42
  preregistration/source, W3-45, operational-background, and W3-46 SHA-256
  values frozen above. The W3-42 generated result is validated at runtime and
  is not frozen by its volatile full-file digest; the verifier reads no data
  and writes no file.
- `FILES`: This preregistration and
  `w3_47_post_genesis_evolution_pressure_coupling_kernel.py`; the frozen
  downstream-handoff trace in the W3-46 contract; and summary updates in the
  parent cosmology ledger and the low-energy architecture record.

## Frozen homogeneous kernel

The two selected normalized maps and inherited identities give

```text
P_F/P_F0 = eta
p = c_lock = eta^(1/2)
a = eta^(-1/3)
A = eta^(-5/6)
eta = A^(-6/5).
```

Consequently,

```text
eta' = -(6/5) H_A eta
     = -(6/5) H_A0 eta
       sqrt(Omega_r0 eta^(10/3)
            + Omega_m0 eta^(5/2)
            + Omega_Lambda0).
```

The absolute participation-loss rate tends to zero with `eta`. The same
law is `eta'=-(6/5)H_A c_lock^2`, so the weakening locked trace is the
single feedback readout rather than an additional rate factor.

For `eta>0` and `H_A>0`, `eta'<0`. The physical interior has no
fixed point. The boundary `eta=0` is approached asymptotically. Its linear
coefficient for `Omega_Lambda0>0` is

```text
f'(0) = -(6/5) H_A0 sqrt(Omega_Lambda0) < 0.
```

## Conserved-content and energy-role ledgers

The selected ideal coherence identity remains

```text
Q_rel/Q_rel0 = (P_F/P_F0)(mathcal_V/mathcal_V_0)
             = eta a^3
             = 1.
```

This is an inherited identity used to obtain `a=eta^(-1/3)`, not a newly
derived conservation law. `Q_rel` is neither `E_total`, `E_N`, nor a
mechanical work energy.

The declared conditional energy-role registry is

```text
E_total = E_L + E_N + E_R
q_L = -T_LN - T_LR
q_N =  T_LN - T_NR
q_R =  T_LR + T_NR
q_L + q_N + q_R = 0.
```

Here `E_L` is localized phase-locked core content; `E_N` is the remaining
non-radiative foundation response, including stationary source-locked
dressing and the homogeneous coherent/tension background; and `E_R` is
freely propagating radiative content. Their nonoverlap is a model-version
bookkeeping postulate, not a derived microscopic decomposition. The three
bins form a declared conditional bookkeeping partition. Antisymmetric
internal sources cancel exactly; microscopic sector densities, currents,
normalizations, transfer laws, and completeness remain underived.

Conditional on these bins admitting local densities, fluxes, and sources
obeying a continuity law, W3-39 supplies the moving-boundary identity as the
required ledger template:

```text
dE_total/dtau =
    4 pi (Q_V - F_b + F_0 + R^2 rho_b R').
```

This gate imports that identity; it does not derive its foundation
realization. A regular center sets `F_0=0`. A stationary source-locked trace
sets only the cycle-averaged radiative part of `F_b` to zero. It sets neither
`E_N`, the stationary trace energy, nor the total moving-boundary flux to
zero. Source change may populate `E_R`; its quantitative energy balance is
still open.

`E_L`, `E_N`, and `E_R` are foundation-side bookkeeping roles and are not
added to the inherited operational stress tensor. This gate derives no maps
`E_L -> epsilon_m`, `E_R -> epsilon_r`, or
`E_N -> epsilon_star/Lambda_eff`. `Omega_Lambda0` is the already-counted
inherited `Lambda_eff` slot: a future stationary `E_N` offset may enter that
slot once through W3-45 and must not be added again to `T_mn`. Likewise,
`m_eff`, `L_oper`, and `p` are readouts here; this gate does not derive
`E_L=m_eff c0^2`.

## Registered negative controls

The verifier must detect, through the same production candidate validator: an
extra independent decay coefficient; a pressure floor; a second `p` factor;
a positive participation fixed point; a non-cancelling internal transfer;
nonzero stationary radiative leakage; insertion of `Q_rel` or `P_F` into the
foundation energy-sector registry; duplicate operational mass or `Lambda`
source; and a flipped relaxation sign.

## Decision boundary

PASS closes the conditional homogeneous matching, fixed-point classification,
consistency with the inherited coherence identity, and declared energy-role
ledger. The microscopic continuity/current law, sector definitions and
normalizations, transfer rates, resonance transport, foundation action, and
numerical `Lambda` remain downstream physical inputs or blockers. No
additional algebraic background stage and no automatic W3-48 follow from this
result.
