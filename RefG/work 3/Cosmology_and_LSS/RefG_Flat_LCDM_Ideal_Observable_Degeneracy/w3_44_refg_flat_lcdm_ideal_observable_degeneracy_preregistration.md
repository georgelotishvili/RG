# W3-44 Preregistration: RefG--Flat-LCDM Ideal-Observable Degeneracy

## Target and stopping rule

This stage has one bounded target: independently implement the selected W3-43
RefG ideal-observable map in the operational-scale `A` domain and the matched
spatially flat dust--radiation--`Lambda` benchmark in the redshift `z` domain,
then test their numerical equality on a frozen finite registry.

The stage stops after dependency verification, the two-route regression,
quadrature convergence checks, the exact supernova intercept symmetry, negative
mutation controls, and report-schema validation. It reads no observational
catalogue, performs no parameter fit, creates no plot or result file, and opens
no follow-on fitting stage.

## Claim contract

- `CLAIM_ID`:
  `W3_44_REFG_FLAT_LCDM_IDEAL_OBSERVABLE_DEGENERACY`
- `CLAIM`: Conditional on the selected W3-43 ideal photon--atomic branch and
  equal benchmark inputs, the RefG `A`-domain implementation and the flat-LCDM
  `z`-domain implementation give the same redshift, signal-arrival dilation,
  expansion rate, comoving distance, angular-diameter distance, luminosity
  distance, and distance modulus within the frozen numerical error bound.
  Supernova magnitudes additionally possess the exact shared
  `H_0`--absolute-magnitude intercept symmetry. These observables therefore
  provide no empirical preference between the two ideal descriptions.
- `TYPE`:
  `CONDITIONAL_BOUNDED_NUMERICAL_IDENTIFIABILITY_REGRESSION`, with one exact
  nuisance-intercept identity.
- `MODEL_VERSION`:
  `W3-COSMOLOGY-v1.2-REFG-FLAT-LCDM-IDEAL-OBSERVABLE-DEGENERACY`.
- `ASSUMPTIONS`:
  1. W3-43 passes with its pinned operational metric, transparent
     photon-number-conserving Maxwell geometric-optics branch, and universal
     local proper atomic transition.
  2. The present normalization is `A_o=1` and `1+z=A_o/A_e`.
  3. The matched benchmark dictionary is
     `H_A0 <-> H_0`, `Omega_m0 <-> Omega_m0`,
     `Omega_r0 <-> Omega_r0`, and
     `Omega_Lambda0=1-Omega_m0-Omega_r0`.
     This is a benchmark-input dictionary, not an identification of `H_A0`
     with any measured Hubble estimator.
  4. Source, calibration, selection, covariance, likelihood, generic atomic
     response `g(A)`, and stellar-population clock response `C(A)` remain
     outside this regression.
- `DOMAIN`:
  1. Expanding, spatially flat, connected post-Genesis effective branch.
  2. `H_A0>0`, `Omega_m0>=0`, `Omega_r0>=0`,
     `Omega_Lambda0=1-Omega_m0-Omega_r0>=0`.
  3. Frozen parameter registry:
     - `reference`:
       `H_A0=70.0 km s^-1 Mpc^-1`,
       `Omega_m0=0.30000`, `Omega_r0=0.00009`;
     - `component_stress`:
       `H_A0=67.0 km s^-1 Mpc^-1`,
       `Omega_m0=0.25000`, `Omega_r0=0.05000`.
     The second point is a numerical component stress test, not an
     observational estimate.
  4. Frozen redshift grid:
     `[1e-4, 1e-3, 1e-2, 0.03, 0.1, 0.25, 0.5, 0.8, 1.0, 1.5, 2.0, 2.3, 3.0]`.
- `CONVENTIONS`:
  `c0=299792.458 km s^-1`; distances are in Mpc; `A_e=(1+z)^(-1)`;
  `mu=5 log10[D_L/Mpc]+25`; every logarithm used in the exact intercept
  identity has a positive argument. For that identity,
  `D_L=(c0/H_0)d(z;Omega)` with dimensionless `d` at fixed density
  parameters, and the supernova model is `m_B^model=M_B+mu`.
- `FREEDOM_LEDGER`:
  The inherited background freedoms are `H_A0`, `Omega_m0`, and
  `Omega_r0`. They are frozen at the two registered points and are not fitted.
  `M_B` appears only in the exact shared supernova-intercept identity. No new
  physical parameter, function, prior, profile, or switch is introduced.
- `DEPENDENCIES`:
  1. W3-43 preregistration SHA-256:
     `f5d4b632c32025119029ce988e5b78b38c05e03efbe5ee735835f86ec853ac49`.
  2. W3-43 verifier SHA-256:
     `90682b118f9ef8eaa8d5885bb87ba5e0d3864018401495085c1f1011b6a8df7b`.
  3. Conditional operational-background source SHA-256:
     `57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055`.
- `METHOD`:
  1. Load W3-43 read-only and require its exact conditional ideal-map pass.
  2. RefG route:
     `E_A(A)^2=Omega_r0 A^-4+Omega_m0 A^-3+Omega_Lambda0` and
     `chi_A=(c0/H_A0) int_[A_e]^1 dA/[A^2 E_A(A)]`.
  3. Benchmark route:
     `E_z(z)^2=Omega_r0(1+z)^4+Omega_m0(1+z)^3+Omega_Lambda0` and
     `chi_z=(c0/H_0) int_[0]^z du/E_z(u)`.
  4. Use independent numerical implementations: adaptive QUADPACK in the
     `A` domain and deterministic composite Simpson integration in the `z`
     domain.
  5. Construct both observable vectors independently:
     `H`, `chi`, `D_A`, `D_L`, `mu`, recovered `z`, and signal-arrival
     dilation.
  6. Re-run the Simpson route at half resolution and require convergence.
  7. Construct `D_L=(c0/H_0)d(z;Omega)`,
     `mu=5 log10[D_L/Mpc]+25`, and `m_B^model=M_B+mu` symbolically;
     derive from those source equations, rather than insert as a target
     expression, the exact shared supernova intercept symmetry
     `H_0 -> lambda H_0`,
     `M_B -> M_B+5 log10(lambda)`.
  8. Apply all frozen negative mutations and validate the exact report schema.
- `PASS_CONDITION`:
  1. All dependency hashes and the W3-43 status are exact.
  2. Every registered observable pair satisfies
     `|x-y| <= ABS_TOL + REL_TOL max(|x|,|y|)` with
     `ABS_TOL=1e-9` and `REL_TOL=1e-9`.
  3. Simpson fine/coarse drift satisfies the same bound.
  4. The exact intercept-symmetry residual is zero.
  5. Every registered negative mutation has normalized error greater than
     `MUTATION_MIN_ERROR=1e-4` at at least one frozen point.
  6. All required true flags are true, all required false flags are false,
     and the schema keysets are exact.
- `FAIL_CONDITION`:
  Any failed dependency, non-finite value, tolerance violation, convergence
  failure, undetected mutation, intercept residual, or schema mismatch.
- `FALSIFIER`:
  Within this frozen effective branch, a verified mismatch above the stated
  numerical bound after convergence and implementation audit falsifies the
  claimed ideal-observable equivalence at that point. It does not by itself
  reject other RefG branches.
- `RESIDUAL`:
  Maximum absolute and normalized route differences for every observable,
  maximum Simpson convergence drift, and the exact intercept residual.
- `ERROR_BOUND`:
  The declared absolute-plus-relative bound above. QUADPACK absolute and
  relative targets are `1e-12`. Composite Simpson uses `N=32768` subintervals
  and is compared with `N=16384`. Floating-point results are
  `NUMERICAL_EVIDENCE`, while the intercept symmetry is exact.
- `VALIDITY_HEALTH`:
  Require finite positive `E_A^2`, `E_z^2`, `H`, `chi`, `D_A`, and `D_L`
  over the registry; positive logarithm arguments; deterministic output; no
  file writes; and upstream W3-43 regression.
- `BRANCHES`:
  Only the selected W3-43 ideal branch and its matched flat-LCDM benchmark are
  tested. Generic `g(A)`, `C(A)`, opacity, dispersion, non-flat geometry, other
  effective actions, and astrophysical source branches are excluded.
- `OBSERVABLE_MAP`:
  `1+z=1/A_e`,
  `Delta_tau_o/Delta_tau_e=1/A_e`,
  `H=H_A0 E`,
  `D_A=A_e chi`,
  `D_L=chi/A_e`,
  and `mu=5 log10[D_L/Mpc]+25`.
- `FORWARD_MODEL`:
  The ideal geometry-to-observable map is used directly. The real
  source--instrument--selection--calibration--covariance--likelihood chain is
  not supplied and no data-level result is claimed.
- `DATA_ROLE`:
  `NO_OBSERVATIONAL_DATA_READ_OR_FITTED`. Local legacy Pantheon files are
  explicitly outside the file registry and must not be opened by the script.
- `IDENTIFIABILITY`:
  The two ideal descriptions are declared observationally degenerate only for
  the frozen shared observable vector and matched input dictionary. Equality
  of the vectors implies equality of any likelihood that uses the same
  forward model, nuisance treatment, and covariance. The exact supernova
  intercept symmetry additionally shows that supernova magnitudes alone do
  not identify an absolute `H_0` without external absolute calibration.
- `BENCHMARK`:
  Spatially flat dust--radiation--`Lambda` FLRW with the same frozen inputs.
  The metric is the maximum normalized observable difference; the threshold
  is the declared error bound. No model-selection score is computed because
  the tested prediction vectors are identical by claim.
- `CROSSCHECK`:
  Independent coordinates and integration algorithms, half-resolution
  convergence, upstream exact W3-43 verification, and negative mutations.
- `PROVENANCE`:
  Frozen local dependency hashes listed above; Python, SciPy, and SymPy
  versions emitted at runtime; deterministic JSON to stdout; no output file.
- `FILES`:
  1. `w3_44_refg_flat_lcdm_ideal_observable_degeneracy_preregistration.md`
  2. `w3_44_refg_flat_lcdm_ideal_observable_degeneracy.py`
  3. Parent `Cosmology_and_LSS/README.md` ledger entry.

## Frozen negative controls

The script must detect all of the following:

1. `extra_endpoint_p_factor`: multiply the RefG luminosity distance by the
   extra endpoint factor `p_o/p_e=A_e^(3/5)`, double-counting the material
   response already contained in `A`.
2. `wrong_A_redshift_power`: use `A_e=(1+z)^(-1/2)`.
3. `omitted_radiation_component`: remove `Omega_r0` from the RefG `E_A` law.
4. `wrong_single_factor_distance_duality`: replace
   `D_L=(1+z)^2D_A` by `D_L=(1+z)D_A`.
5. `wrong_signal_dilation_sqrt`: replace `1+z` by `sqrt(1+z)`.
6. `wrong_supernova_intercept_sign`: transform
   `M_B -> M_B-5 log10(lambda)` while scaling
   `H_0 -> lambda H_0`.

## Closure flags

Required true:

- `upstream_w3_43_pass_verified`
- `dependency_hashes_exact`
- `canonical_dependency_text`
- `frozen_parameter_registry_exact`
- `frozen_redshift_grid_exact`
- `independent_coordinate_routes_used`
- `quadrature_convergence_pass`
- `redshift_map_match`
- `signal_dilation_match`
- `expansion_rate_match`
- `comoving_distance_match`
- `angular_diameter_distance_match`
- `luminosity_distance_match`
- `distance_modulus_match`
- `supernova_intercept_symmetry_exact`
- `mutation_controls_pass`
- `schema_keysets_exact`

Required false:

- `observational_data_read`
- `observational_fit_performed`
- `observational_pass`
- `empirical_preference_established`
- `measured_H0_identified`
- `new_physical_freedom_introduced`

The aggregate `ideal_observable_degeneracy_regression_pass` flag is computed
only after all atomic residual, convergence, dependency, mutation, and schema
checks have been assembled. It is not one of its own required inputs.

## Decision semantics

Passing status:

`PASS_BOUNDED_NUMERICAL_IDEAL_OBSERVABLE_DEGENERACY__NO_DATA_FIT_OR_EMPIRICAL_PREFERENCE`

This status is a bounded implementation and identifiability regression. It
adds no observational pass, fitted parameter, or empirical preference to the
exact conditional result already established by W3-43.
