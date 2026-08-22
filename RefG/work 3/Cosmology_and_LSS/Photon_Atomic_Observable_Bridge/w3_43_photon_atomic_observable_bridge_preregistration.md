# W3-43 Preregistration: Photon--Atomic Observable Bridge

## Target and stopping rule

This gate has one target: carry the selected operational FLRW geometry to the
ideal observables measured by a comoving atomic source and detector. The gate
stops when spectroscopic redshift, photon arrival-time dilation, the ideal
kinematic expansion rate, comoving distance, angular-diameter distance, and
luminosity distance are derived in one frame-consistent map and the explicit
double-counting controls pass. The generic atomic-drift and
stellar-population-clock boundary is recorded without solving it. The gate
reads no supernova or chronometer data and opens no new background,
source-evolution, clock-calibration, or likelihood calculation.

## Claim contract

**CLAIM_ID:** `W3_43_PHOTON_ATOMIC_OBSERVABLE_BRIDGE`.

**CLAIM:** On the selected spatially flat expanding operational FLRW branch,
a minimally coupled Maxwell geometric-optics sector, a universal local atomic
proper-frequency standard, and transparent photon-number-conserving
propagation give the exact ideal-observable map

```text
omega_o/omega_e = A_e/A_o
1+z_spec = A_o/A_e
Delta tau_o/Delta tau_e = A_o/A_e
chi(A_e,A_o) = c0 integral_[A_e]^[A_o] dA/[A^2 H_A(A)]
D_A(A_e,A_o) = A_e chi(A_e,A_o)
D_L(A_e,A_o) = (A_o^2/A_e) chi(A_e,A_o)
```

With the present normalization `A_o=1`, these endpoint relations become

```text
H_kin(z) = H_A(z)
chi(z) = (c0/H_A0) integral_0^z du/E_z(u)
D_A(z) = chi(z)/(1+z)
D_L(z) = (1+z) chi(z) = (1+z)^2 D_A(z).
```

The bridge adds no continuous freedom and no second material-scale factor.

**TYPE:** `CONDITIONAL_EXACT_IDEAL_OBSERVABLE_MAP`.

**MODEL_VERSION:** `W3-COSMOLOGY-v1.1-PHOTON-ATOMIC-OBSERVABLE-BRIDGE`.
Changing the operational metric, photon action, dispersion relation, local
atomic standard, transparency or photon-number law, curvature branch,
background source registry, or scale/time dictionary creates a new model
version.

**ASSUMPTIONS:**

1. The upstream conditional background gate
   `W3_COSMOLOGY_OPERATIONAL_GEOMETRIC_FLRW_COMPLETION` passes on its selected
   spatially flat expanding branch.
2. The already-connected post-Genesis operational metric is
   
   ```text
   ds_op^2 = c0^2 d tau^2
             - A(tau)^2 [d chi^2 + chi^2 d Omega_2^2],
   A>0,  d tau=p dt,  A=a/p.
   ```
3. The photon sector on this effective branch is the minimally coupled Maxwell
   action with time-independent operational coupling,
   
   ```text
   S_gamma = -(1/(4 mu0)) integral d^4x sqrt(-g) F_mn F^mn.
   ```
   Its geometric-optics limit obeys `k_m k^m=0`,
   `k^n nabla_n k^m=0`, and conservation of the vacuum wave-action/photon-number
   current.
4. Source and detector are ideal comoving observers. They use the same local
   atomic transition, whose proper phase satisfies
   `d phi_A/d tau=2 pi nu_*` with constant positive `nu_*` in the operational
   local frame. For the wider unsolved atomic boundary, write
   `nu_A(A)=nu_A0/g(A)` with `g(A)>0` and `g(1)=1`, so that
   `nu_A,o/nu_A,e=g(A_e)/g(A_o)`. The selected universal-atomic branch fixes
   `g=1`. The emitted photon is resonant with that transition.
5. The connecting ray is transparent and lies inside the effective metric
   domain. Absorption, scattering, plasma dispersion, frequency conversion,
   nonmetric photon coupling, and gravitational or peculiar-velocity endpoint
   perturbations are outside this ideal homogeneous map.
6. The direct flux ledger uses an ideal isotropic bolometric emitter with
   local proper luminosity `L_e` and an ideal detector measuring bolometric
   operational flux. An isotropic-equivalent directional luminosity gives the
   same geometric definition.
7. `A_o=1` is the present normalization when formulas are expressed as
   functions of observed redshift. The unnormalized endpoint derivation keeps
   positive `A_e` and `A_o` explicit.
8. The upstream background function is
   
   ```text
   H_A(A)=+H_A0 E(A),
   E(A)^2=Omega_r0 A^(-4)+Omega_m0 A^(-3)+Omega_Lambda0,
   Omega_Lambda0=1-Omega_m0-Omega_r0.
   ```

**DOMAIN:** The already-connected homogeneous-isotropic post-Genesis interval
on which the upstream leading two-derivative EFT is valid, `A>0`, `H_A0>0`,
and `E(A)^2>0`; wavelengths are short compared with the curvature scale and
long compared with the microscopic EFT cutoff length; source and observer are
connected by a unique ideal radial null bundle without caustic ambiguity; the
path is transparent and photon number is conserved.

**CONVENTIONS:** Signature is `(+---)`. Prime denotes `d/d tau`. `u^m` is the
comoving four-velocity and the locally measured photon frequency is
`omega=|k_m u^m|` up to a fixed positive unit convention that cancels in all
ratios. `e` and `o` denote emission and observation. Spectroscopic redshift is
`1+z_spec=nu_A,o/nu_gamma,o` for a photon emitted by the same transition.
`D_A` and `D_L` use operational proper areas, local proper isotropic
bolometric source power, and bolometric measured flux.
`D_ref=10 pc` only fixes the conventional zero point of the distance modulus.

**FREEDOM_LEDGER:** The ideal bridge inherits exactly the three upstream
background inputs `H_A0`, `Omega_m0`, and `Omega_r0`; spatial flatness fixes
`Omega_Lambda0=1-Omega_m0-Omega_r0`. The selected optical and atomic branch
adds no continuous parameter or free function. A real supernova likelihood
will later register absolute-luminosity calibration, source-population,
host, selection, instrument, covariance, and other nuisance freedoms; none
enters this gate.

The generic boundary functions `g(A)>0` and
`C(A)=d tau_SPS/d tau>0` are displayed only to mark where foundation-level
atomic physics and a stellar-population clock would enter. They are not fixed,
fitted, or counted as freedoms of the selected `g=1` ideal bridge; choosing
them for an observational chronometer model requires a separate contract.

**IDEAL_SOURCE_REGISTRY:** The direct flux derivation uses exactly
`local_proper_isotropic_or_isotropic_equivalent_bolometric_source_power` and
`ideal_bolometric_operational_flux_measurement`. The normalization `L_e`
cancels from the derived `D_L` and is not a fitted supernova luminosity or a
claim that intrinsic luminosity has been derived.

**DEPENDENCIES:** W3-36 supplies the exact metric/process dictionary. W3-40
supplies the single-driver semantic context of `A=a/p`; no W3-40 artifact
enters this gate's pass logic. The selected conserved relaxation-density
closure supplies `p=A^(-3/5)` and `a=A^(2/5)`. The upstream operational
geometric FLRW verifier supplies the conditional background equation and its
finite freedom ledger. The W3-36 source and preregistration are pinned and its
read-only `build_report()` identity flags are checked directly.

**METHOD:** Two independent photon-frequency derivations are used: the
homogeneous eikonal with conserved comoving wave number and the radial null
geodesic equation with the metric Christoffel symbol. Neighboring null rays
give arrival-time dilation. Endpoint conversion between `tau` and foundation
coordinate time `t` checks exact cancellation of the common cadence `p` in the
dimensionless photon/atom ratio. The generic `g(A)` and `C(A)` chain rule is
retained symbolically, after which the selected `g=1` branch gives the ideal
kinematic expansion rate. Radial null integration gives `chi(z)`. Direct
energy/rate/area flux bookkeeping and Etherington reciprocity independently
give the same `D_L`. Exact SymPy residuals, registry/key-set checks, pinned
upstream hashes, and negative mutations enforce the result. No numerical
integration, data, fit, or likelihood is used.

**PASS_CONDITION:**

1. Both eikonal and geodesic routes give `d(A omega)/d tau=0` and
   `omega_o/omega_e=A_e/A_o` with exact zero residuals.
2. The universal local atomic endpoint map gives
   `1+z_spec=A_o/A_e`; the `t`- and `tau`-coordinate photon/atom ratios agree
   exactly and contain no residual `p_e/p_o` factor.
3. Before `g=1` is selected, the executable boundary gives
   `1+z_spec=(A_o/A_e)g(A_e)/g(A_o)` and, for `A_o=1`,
   `H_CC=H_A[1-d ln g/d ln A]/C(A)` with
   `C=d tau_SPS/d tau`. Its identities close while `g` and `C` remain
   physically undetermined.
4. Neighboring null fronts give
   `Delta tau_o/Delta tau_e=A_o/A_e=1+z_spec`.
5. `H_kin=-(1+z)^(-1) dz/d tau` gives `H_kin=H_A`; hence the ideal present
   kinematic rate is `H_kin,0=H_A0`. Identification with a specific measured
   `H_0` estimator remains outside the gate until that estimator's clock,
   source, calibration, and likelihood chain is supplied.
6. The redshift-space background, radial null integral, distance duality,
   direct flux ledger, distance modulus, and low-redshift derivative all have
   exact zero residuals.
7. The optical, ideal-source, and freedom registries have exact expected key
   sets, the upstream background pass and pinned hashes are valid, and every
   negative mutation is detected.
8. Every declared ideal-map flag is true and every microphysical,
   source-population, survey, calibration, numerical-fit, and observational
   flag remains false.

**FAIL_CONDITION:** Any required exact residual is nonzero; the two photon
routes or the flux/reciprocity routes disagree; a final photon/atom ratio
retains an endpoint cadence factor; `p` is multiplied onto the operational
redshift as a second physical effect; an unregistered optical freedom or
source is introduced; the retired stationary or `D_L proportional to
z(1+z)` map reappears; a pinned dependency fails; or ideal geometric
equivalence is reported as a supernova data pass.

**FALSIFIER:** Within the declared effective domain, a derived RefG photon or
atomic action with nonuniversal operational coupling, non-null dispersion,
nonconserved vacuum photon number, or a time-varying local dimensionless
atomic frequency ratio falsifies this selected bridge. A failed real-data
supernova gate would falsify the completed background-plus-forward-model
version tested there, not this algebraic identity by itself.

**RESIDUAL:** Every displayed kinematic, redshift, clock, rate, distance,
duality, flux, low-redshift, coordinate-cancellation, and background
substitution residual must simplify to exact integer zero. Negative-control
residuals must simplify to a provably nonzero expression on generic positive
endpoints.

**ERROR_BOUND:** Algebraic error is zero within the declared assumptions.
Geometric-optics, local-laboratory, opacity, lensing, peculiar-velocity,
higher-derivative EFT, source-evolution, calibration, and observational
errors are outside this ideal gate and must be budgeted in their own forward
model.

**VALIDITY_HEALTH:** The selected Maxwell plus local-atomic branch is
covariant, uses one operational metric, preserves the upstream finite freedom
ledger, and counts the foundation cadence once through `(t,a)->(tau,A)`.
Foundation-level derivations of the Maxwell action and atomic spectrum remain
separate microscopic tasks. The ideal map is valid before astrophysical and
instrumental perturbations are added.

**BRANCHES:** Selected: spatially flat, expanding, minimally coupled,
transparent, photon-number-conserving operational branch with universal local
atomic proper frequency. Nonmetric photon coupling, opacity, dispersion,
frequency conversion, varying operational constants, nonzero curvature, and
Lambda-free acceleration are separate model versions. The strict stationary
observable branch remains retired.

**OBSERVABLE_MAP:** With `A_o=1`,

```text
1+z = 1/A_e
E_z(z)^2 = Omega_r0 (1+z)^4 + Omega_m0 (1+z)^3
           + 1-Omega_m0-Omega_r0
H_kin(z) = H_A0 E_z(z)
chi(z) = (c0/H_A0) integral_0^z du/E_z(u)
D_A(z) = chi(z)/(1+z)
D_L(z) = (1+z) chi(z)
mu(z) = 5 log10[D_L(z)/(10 pc)]
Delta tau_o = (1+z) Delta tau_e
```

These are ideal operational observables on the selected branch.

The unsolved boundary around that selected branch is

```text
1+z_spec = g(A_e)/A_e
H_spec(A) = H_A(A) [1-d ln g/d ln A]
H_CC(A) = H_A(A) [1-d ln g/d ln A]/C(A)
C(A) = d tau_SPS/d tau > 0.
```

Thus `g=1` recovers the selected ideal spectroscopic map. A catalog-level
cosmic-chronometer rate is not identified with `H_A` unless its independent
clock response `C` is also supplied.

**FORWARD_MODEL:** The geometry-to-ideal-observable chain is closed here.
The real-supernova chain still requires intrinsic luminosity/absolute
magnitude, light-curve and spectral evolution, dust and host response,
K-corrections, lensing and peculiar velocities, instrument calibration,
selection, covariance, and a preregistered likelihood. A cosmic-chronometer
catalog additionally requires a stellar-population-synthesis clock map.

**DATA_ROLE:** No observational data are read, selected, calibrated, or fit.
The retained Pantheon files are not used. The future supernova test will be a
separate preregistered data gate.

**IDENTIFIABILITY:** Exact ideal measurements of `z` and `D_L(z)` identify
the same background expansion history as the corresponding flat
dust--radiation--Lambda FLRW geometry. Supernova distance moduli alone retain
the standard absolute-luminosity--`H_A0` degeneracy. This bridge is therefore
background-observable equivalent to that benchmark and supplies no separate
empirical identification of the RefG ontology. On a generic atomic branch
`1+z_spec=(A_o/A_e)g(A_e)/g(A_o)`; the selected result
`z_spec=A_e^(-1)-1` holds at `A_o=1` and `g=1`. A stellar-population
chronometer additionally carries `C(A)=d tau_SPS/d tau`, so a specific
measured `H_0` estimator remains outside this gate.

**BENCHMARK:** Standard spatially flat, minimally coupled
dust--radiation--Lambda FLRW geometry with the same `H_A0`, `Omega_m0`, and
`Omega_r0`. Required exact benchmark residuals are zero. No observational
preference claim is part of this gate.

**CLOSURE_FLAGS:** Required true flags are:

- `upstream_background_pass_verified`
- `w3_36_metric_dictionary_pass_verified`
- `pinned_dependency_hashes_exact`
- `operational_metric_branch_pinned`
- `minimal_Maxwell_branch_selected`
- `local_atomic_proper_frequency_selected`
- `transparent_photon_number_transport_selected`
- `generic_atomic_chronometer_boundary_exact`
- `photon_null_geodesic_exact`
- `photon_frequency_transport_exact`
- `coordinate_cadence_cancellation_exact`
- `spectroscopic_redshift_exact`
- `arrival_time_dilation_exact`
- `kinematic_Hubble_map_exact`
- `redshift_background_substitution_exact`
- `comoving_distance_exact`
- `angular_diameter_distance_exact`
- `photon_flux_ledger_exact`
- `Etherington_reciprocity_exact`
- `luminosity_distance_exact`
- `distance_modulus_definition_exact`
- `low_redshift_Hubble_slope_exact`
- `finite_optical_registry_complete`
- `finite_ideal_source_registry_complete`
- `finite_freedom_ledger_complete`
- `mutation_controls_pass`
- `schema_keysets_exact`

The aggregate output flag
`conditional_ideal_observable_map_pass` is computed only after all atomic
required-true and required-false flags, registries, hashes, residual keys, and
mutation keys have been assembled. It is not one of its own required inputs.

Required false flags are:

- `Maxwell_sector_derived_from_foundation`
- `atomic_spectrum_derived_from_foundation`
- `nonmetric_or_opacity_branches_excluded_by_data`
- `stellar_population_clock_derived`
- `supernova_intrinsic_luminosity_derived`
- `survey_selection_and_likelihood_supplied`
- `numerical_background_calibrated`
- `H_A0_identified_with_specific_measured_H0`
- `observational_data_fit_performed`
- `observational_pass`

**CROSSCHECK:** Eikonal and affine-geodesic frequency transport; process-time
and foundation-time endpoint ratios; neighboring-null-ray dilation; direct
redshift differentiation; direct radial-null integration; flux dilution and
Etherington duality; present-point and low-redshift normalization; exact
upstream dependency verification; and mutations for an `A^(-2)` photon law,
an extra `p_o/p_e` endpoint factor, a missing arrival-rate loss, and the retired
`z(1+z)` distance law. Separate mutations require detection of an omitted
generic atomic-drift term and an omitted stellar-clock factor.

**PROVENANCE:** The verifier will pin the canonical UTF-8 LF preregistration,
W3-36 source/preregistration, and upstream operational-background source
hashes; call both upstream read-only report builders and verify the required
identity/background flags; record Python/SymPy versions and its own source
SHA-256; emit strict deterministic JSON to standard output; and write no
files.

**FILES:** This preregistration, the exact symbolic verifier
`w3_43_photon_atomic_observable_bridge.py`, and the parent
`Cosmology_and_LSS/README.md` status entry.

## Decision semantics

If all exact checks pass while every required open flag remains false, the
decision is
`PASS_CONDITIONAL_IDEAL_OBSERVABLE_MAP__ASTROPHYSICAL_FORWARD_MODEL_AND_DATA_TEST_OPEN`.
This closes the ideal photon--atomic and geometric distance bridge on the
selected effective branch. It does not assign an observational-pass label.
