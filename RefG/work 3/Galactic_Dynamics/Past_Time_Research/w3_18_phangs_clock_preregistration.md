# W3-18 PHANGS Vortex--Stellar Clock Test: Frozen Protocol

**Registration timestamp (UTC):** 2026-08-15T12:36:38Z  
**Protocol version:** W3-18-v1.1-PREREGISTERED  
**Outcome-data state at registration:** Public-product schemas, file sizes, galaxy overlap, aggregate cut counts, WCS alignment, and mask angular coverage were inspected for feasibility. No cluster age--azimuth association, likelihood, fitted clock ratio, model-comparison statistic, permutation statistic, or bootstrap clock ratio was inspected before this protocol and its v1.1 numerical clarifications were frozen.

This protocol tests one bounded prediction. It does not test the full RefG theory and it does not reconstruct the billion-year lifetime of a galaxy. It compares geometric drift accumulated over the last 6--50 Myr with compact-cluster stellar-evolution ages in NGC 4303.

## Mandatory claim contract

### CLAIM_ID

`W3_18_PHANGS_VORTEX_STELLAR_CLOCK`

### CLAIM

In a disk region governed by a coherent spiral pattern, the accumulated angular displacement of young stellar clusters relative to the present spiral-arm geometry can be described by one galaxy-wide clock ratio `q`. The common-ticking benchmark is `q = 1`; the proposed frozen-vortex/differential-clock effect predicts `q > 1`.

### TYPE

Observational numerical test with a circular forward model. Any positive result is, at most, `FIT_COMPATIBILITY` in one preregistered pilot galaxy.

### MODEL_VERSION

`W3-18-v1.1-PREREGISTERED`. The sample, cuts, parameter bounds, likelihood family, benchmark, and decision thresholds below are frozen before cluster age--phase data are evaluated. A material alteration after viewing the result requires a new model version and must be reported as exploratory.

### ASSUMPTIONS

1. PHANGS--HST DR5 compact-cluster ages and sky positions are usable evolutionary clocks and positions over 1--50 Myr.
2. The PHANGS spiral mask traces the current relevant star-forming spiral pattern.
3. Over the tested 3--5 kpc annulus and 50 Myr interval, a single effective spiral pattern speed is an adequate first-order description.
4. The Lang et al. CO rotation curve gives the mean material angular speed after interpolation.
5. The 1--3 Myr sample calibrates a radial birth-phase offset; it is not treated as zero age.
6. Cluster dissolution, epicyclic motion, migration, extinction, incompleteness, and non-arm formation are represented by intrinsic angular scatter, a uniform-background mixture, quality cuts, and robustness checks.
7. The proposed effect changes accumulated geometric drift relative to stellar evolutionary age. A coordinate relabeling or common multiplicative Doppler factor predicts `q = 1` and is not counted as the proposed effect.

### DOMAIN

- Primary galaxy: NGC 4303 only.
- Deprojected radius: `3.0 <= R < 5.0 kpc`, in four fixed 0.5-kpc radial blocks.
- Anchor ages: `1 <= age <= 3 Myr`; clock ages: `6 <= age <= 50 Myr`.
- Admitted simple-environment mask classes: spiral outside bar (`6`) and interarm (`7`). Center, bar, bar ends, interbar, central/ring structures, outer disk, and unclassified pixels are excluded.
- The HST and spiral-mask WCS must cover every selected object; no extrapolation outside the shared footprint is allowed.
- A block is usable only if `sign[Omega_m(R)-Omega_p]` is stable in at least 95% of nuisance draws and null phase leverage from 6 to 50 Myr exceeds twice the arm-template angular resolution.

### CONVENTIONS

- Angles are radians internally and wrapped to `[-pi, pi)`.
- Deprojected azimuth is positive in the selected physical disk-rotation direction. Both orientation branches are fitted before selection.
- `Omega_m = V_rot/R` and `Omega_p` are positive in `km s^-1 kpc^-1`, converted to `rad Myr^-1` with one pinned constant.
- `q = 1` is common ticking; `q > 1` means more accumulated geometric rotation per stellar-evolution Myr.
- Frozen disk geometry: center `(RA, Dec)=(185.478750 deg, 4.473639 deg)`, distance `16.99 Mpc`, inclination `23.5 deg`, and position angle `312.4 deg` east of north.
- The drizzled spiral-mask WCS is evaluated with inconsistent SIP coefficients disabled; its linear celestial WCS is retained. Categorical masks use nearest-pixel lookup through rounded zero-based pixel coordinates.

### FREEDOM_LEDGER

- `q`: one galaxy-wide parameter, bound `[0,4]`; fixed to `1` in the benchmark.
- `Omega_p`: one galaxy-wide spiral speed, bound `[0,80] km s^-1 kpc^-1`; inferred from cluster drift, not fixed to the external Williams value.
- `s`: one discrete orientation branch, `+1` or `-1`.
- `delta_b`: one zero-age angular offset per usable radial block, each in `[-45 deg,+45 deg]`, constrained by 1--3 Myr anchors.
- `sigma_int`: one galaxy-wide circular intrinsic scatter, `[1 deg,45 deg]`.
- `f_bg`: one galaxy-wide uniform-background fraction, `[0,0.8]`.
- No per-cluster phase, arm assignment, or clock parameter is fitted.

### DEPENDENCIES

`W3_17_PHANGS_DATA_INTEGRITY` must pass. Every raw file must match its W3-17 manifest hash and schema. W3-14, W3-15, and W3-16 are not inputs.

### METHOD

1. In each radial block, make a 1-degree circular angular template from the public NGC 4303 narrow spiral mask and smooth binary angular occupancy by a frozen circular Gaussian of `3 deg`.
2. Select PHANGS--HST human class 1+2 primary clusters. Require finite positive age limits and mass, `mass >= 10^4 solar masses`, `NON_DETECTION_FLAG <= 1`, reduced SED-fit chi-square `<10`, and 68% log-age half-width `<=0.30 dex`.
3. Include both spiral and interarm clusters in the shared radial domain; do not select by current distance to an arm.
4. Back-rotate each cluster by `s*q*[Omega_m(R)-Omega_p]*age` and compare its inferred birth phase with the present arm template shifted by block offset `delta_b`.
5. Use a normalized circular mixture likelihood: convolved arm-template density with weight `1-f_bg` plus uniform phase density with weight `f_bg`.
6. Fit `M0:q=1` and `M1:q free` with identical nuisance structure and deterministic multi-start optimization. Record all convergence flags and best solutions.
7. Profile `q` on `0.00,0.02,...,4.00`. Define 68%, 95%, and 99.7% profile intervals by `2 Delta ln L <= 1,4,9`.
8. Define `Delta BIC=BIC(M0)-BIC(M1)`, positive when the free-`q` model is favored.
9. Use random seed `317180`; perform 1,000 within-block age permutations and 1,000 radial-block bootstraps. If a required control cannot complete, its closure flag remains false.
10. Compare fitted `Omega_p` only after fitting with the independent stellar-Tremaine--Weinberg value `43.518 +5.283/-10.020 km s^-1 kpc^-1` (quality 1). It is a check, not a prior.

#### Frozen numerical implementation

- The primary fit uses SciPy differential evolution with seed `317180`, population multiplier `15`, tolerance `1e-8`, maximum `400` generations, and final L-BFGS-B polishing with `ftol=1e-12`, `gtol=1e-8`, and `maxiter=2000`. At least three deterministic differential-evolution seeds, `317180`, `317181`, and `317182`, must agree in objective value to `1e-5`; otherwise `optimizer_converged=False`.
- The circular template uses 360 one-degree samples at each cluster radius. Fixed ridge smoothing is a wrapped Gaussian with `sigma=3 deg`. Fitted intrinsic scatter is implemented on the exact integer grid `1,2,...,45 deg`; the global optimum is the best grid member, so BIC counts it as one fitted nuisance parameter.
- BIC uses `n` equal to the number of anchor plus clock clusters entering the likelihood. `k=7` for `q=1` and `k=8` for free `q`: one `Omega_p`, one scatter, one background fraction, four block offsets, and, in the alternative, `q`.
- Both orientation branches are discrete nuisance branches. Each observed fit minimizes over both. Every age permutation and every positive-control simulation repeats the same two-branch selection, so its look-elsewhere effect is included in the empirical null. A branch is called identified only when its BIC is at least 10 smaller than the other branch.
- The q profile uses the exact grid `0.00,0.02,...,4.00`; nuisance parameters and both orientation branches are reoptimized at each point. Confidence endpoints are the outermost grid points satisfying the stated likelihood-ratio threshold; touching 0 or 4 is an unbounded profile failure.
- The primary statistic is `T=Delta BIC=BIC(q=1)-BIC(q free)` after discrete orientation minimization. In each of 1,000 negative controls, ages and their paired limits are permuted together within each fixed radial block, and both complete models are refitted. The one-sided empirical p-value is `(1 + count[T_perm >= T_obs])/1001`.
- In each of 1,000 block bootstraps, the four 0.5-kpc blocks are sampled with replacement; all clusters in a selected block receive its multiplicity. Cluster ages are also drawn from a split-normal distribution in log age whose lower/upper widths are set by the DR5 absolute age limits. Both models are refitted. Failed fits remain recorded and make `block_bootstrap_complete=False` if more than 1% fail.
- Rotation-curve uncertainty has no published bin covariance in the adopted table. Its gate therefore uses a conservative coherent draw: one shared normal deviate moves every radius through its tabulated asymmetric error, while the Williams pattern speed is independently drawn through its asymmetric error. A radial block is sign-stable when the sign of its median `Omega_m-Omega_p` is unchanged in at least 95% of 10,000 draws.
- Phase leverage is `44 Myr * median(abs[Omega_m-Omega_p])` in a block. It must exceed `6 deg`, twice the frozen three-degree template smoothing scale.
- Per-block q estimates fix the joint best `Omega_p`, orientation, scatter, and background fraction, then profile q and that block offset. Cochran's Q with these profile variances supplies the preregistered heterogeneity p-value.
- External pattern-speed compatibility means overlap between the block-bootstrap 95% interval of fitted `Omega_p` and the asymmetric Williams two-standard-error interval `[43.518-2*10.020, 43.518+2*5.283]`.
- Robustness runs use the broad mask, a 6--100 Myr clock interval, and the machine class 1+2 catalog with ML confidence at least 0.9. A robustness shift passes when `abs(q_rob-q_primary) < sqrt(sigma_primary^2+sigma_rob^2)`, using half the 68% profile width for each sigma.
- Positive controls inject `q=1.25`, `1.50`, and `2.00`, 300 simulations each, into the actual radii, ages, selection functions, and fitted q=1 nuisance model. They repeat the complete two-orientation comparison. Recovery is valid when median bias is below 0.10, 68% interval coverage is 0.60--0.76, and at least 90% of `q=1.50` injections yield a 99.7% lower profile bound above 1.

### PASS_CONDITION

A one-galaxy `OBSERVATIONAL_PASS` with strength `FIT_COMPATIBILITY` requires the logical AND of:

1. Every integrity, schema, WCS, sample, footprint, leverage, and optimizer gate passes.
2. At least 50 clock clusters, three independent radial blocks, and two spiral-template segments contribute.
3. The physical orientation beats the opposite branch by `Delta BIC>=10`.
4. The free-`q` model beats `q=1` by `Delta BIC>=10`.
5. The 99.7% profile interval lies wholly above `q=1`.
6. The within-block age-permutation p-value is `<=0.003`.
7. At least three blocks have the same `q>1` direction, with no decisive block heterogeneity (`p>=0.01`).
8. Fitted spiral speed is compatible at 95% with an independent published estimate; otherwise the one-pattern premise is unestablished.
9. All preregistered robustness checks complete and move `q` by less than one combined standard deviation.

This would support only the bounded clock-decoupling mechanism in NGC 4303; independent galaxies are required for stronger evidence.

### FAIL_CONDITION

The observational gate is `FAIL` when the data, identifiability, optimizer, null-control, bootstrap, and robustness channels all complete but one or more numerical `PASS_CONDITION` thresholds are missed. It is `OPEN` when a required data, identifiability, power, or control channel cannot be completed. Neither state rejects RefG as a whole.

The directional mechanism is marked `falsifier_triggered=True` only if all data and power gates pass, the 99.7% profile upper bound is `<=1`, and injection--recovery has at least 90% power for a numerical RefG `q_pred` frozen before a future confirmatory run. This pilot has no independently frozen `q_pred`; therefore it can constrain q and fail its pilot pass gate, but it cannot trigger a theory-level `REJECTED` status.

### FALSIFIER

For this mechanism: a powered, systematics-controlled measurement consistent with common ticking and excluding a preregistered `q_pred>1`. Transient/multiple patterns, weak leverage, or incompatible pattern speeds make this implementation inconclusive rather than falsifying the clock mechanism.

### RESIDUAL

For cluster `i` in block `b`, the diagnostic common-ticking residual is `r_i=wrap[theta_i-delta_b-s*(Omega_m(R_i)-Omega_p)*age_i-theta_arm(R_i)]`. The likelihood uses the full arm-template density, never a hard nearest-arm assignment.

### ERROR_BOUND

- Asymmetric DR5 age limits sampled in log age.
- Center, distance, inclination, and position angle propagated where source uncertainties exist.
- Asymmetric rotation-curve errors propagated by interpolation draws.
- Pattern speed fitted internally; published errors only enter the external check.
- Frozen 3-degree template smoothing plus fitted intrinsic scatter.
- Radial-block bootstrap for spatial dependence.
- Optimizer convergence, repeat starts, profile resolution, and likelihood normalization recorded.

### VALIDITY_HEALTH

Report one-pattern adequacy, orientation identifiability, radial sign stability, phase leverage, shared-footprint coverage, optimizer convergence, likelihood normalization, finite profile bounds, and robustness completion. Any mandatory failure prevents `OBSERVATIONAL_PASS`.

### BRANCHES

- Both rotation directions `s=+1,-1`.
- `q=1` benchmark and `q in [0,4]` alternative.
- One rigid effective spiral pattern; incompatible multiple patterns set `OPEN`.
- Other galaxies are excluded from this claim and require separately versioned replication.

### OBSERVABLE_MAP

The instantaneous Doppler rotation curve supplies `Omega_m(R)`; the stellar catalog supplies an independent evolutionary age. Their time integral predicts accumulated angular phase relative to the current spiral pattern. This phase--age relation, not an absolute Doppler rescaling, is the clock comparison.

### FORWARD_MODEL

`(q,Omega_p,s,age,rotation curve,birth offset)` -> back-rotated birth phase -> arm-template circular density -> cluster-phase likelihood, convolved with scatter and mixed with a uniform non-arm component. WCS, deprojection, cuts, age errors, rotation errors, and block dependence are explicit.

### DATA_ROLE

- PHANGS--HST DR5 human class 1+2 catalog: fit positions, ages, limits, masses, flags, and SED quality.
- Narrow spiral and simple environment masks: fixed geometry/selection, not tuned to cluster phases.
- Lang et al. CO rotation curve: fixed kinematic input.
- Williams et al. stellar pattern speed: external post-fit check only.
- The fitted clusters are not an independent validation set; a later galaxy is required for `VALIDATION_PASS`.

### IDENTIFIABILITY

Radial variation of `Omega_m(R)` separates multiplicative `q` from intercept-like `Omega_p`. Require a bounded two-dimensional likelihood, finite `q` interval, unique orientation, at least three blocks, and adequate leverage; otherwise status is `OPEN`.

### BENCHMARK

The frozen benchmark is the same forward model with `q=1`. Compare by `Delta BIC`. The opposite orientation and within-block permutations are negative controls; injected coherent ratios are positive controls.

### CLOSURE_FLAGS

All begin `False` and are computed, never hand-set: `data_integrity`, `schema_valid`, `wcs_valid`, `sample_size_valid`, `shared_footprint_valid`, `radial_leverage_valid`, `orientation_identified`, `optimizer_converged`, `likelihood_normalized`, `q_profile_finite`, `pattern_speed_external_consistency`, `permutation_complete`, `block_bootstrap_complete`, `injection_recovery_complete`, `injection_recovery_valid`, `robustness_complete`, `pass_statistical_thresholds`. Aggregate pass is their logical AND plus every `PASS_CONDITION` item.

### CROSSCHECK

1. Within-block age permutations.
2. Radial-block bootstrap.
3. External pattern-speed comparison.
4. Broad instead of narrow spiral mask.
5. Clock ages 6--100 rather than 6--50 Myr.
6. High-confidence machine rather than human catalog.
7. Individual-cluster likelihood versus radial/age-bin cross-correlation.

The first three are mandatory for a numerical pilot; all are mandatory before `OBSERVATIONAL_PASS` under this version. The HST machine catalog overlaps the human catalog and is only a robustness sample, never an independent validation sample.

### PROVENANCE

W3-17 records retrieval UTC, survey/release/product identifiers, DOI/archive URL, license where exposed, relative paths, byte sizes, SHA-256 hashes, code hashes, package versions, and output hashes. Absolute paths are forbidden. W3-18 aborts if W3-17 is absent, stale, wrong-claim/wrong-status, or any raw hash differs.

### FILES

- `w3_18_phangs_clock_preregistration.md` -- frozen protocol.
- `w3_17_phangs_data_manifest.py` / `w3_17_result.json` -- acquisition and integrity gate/artifact.
- `w3_18_phangs_vortex_stellar_clock_test.py` / `w3_18_result.json` -- physical test/artifact.
- `phangs_vortex_stellar_clock_test.png` -- diagnostic.
- `PHANGS_data/{raw,derived,manifests}` -- ignored public/generated data.

## Interpretation boundary

This can establish or constrain a recent relative clock ratio between spiral geometry and stellar evolution. It cannot reveal an absolute historical tempo or NGC 4303's formation redshift. It also contains no RefG calculation of a numerical `q_pred`; a fitted positive q is phenomenological compatibility with the bounded mechanism, not a post-hoc prediction of the cosmological clock law. A null result is informative: the two accessible clocks tick together within measured precision on 6--50 Myr scales.
