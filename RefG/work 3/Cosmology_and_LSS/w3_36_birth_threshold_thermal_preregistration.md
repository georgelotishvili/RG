# W3-36 Preregistration: Finite Birth, Activation Threshold, and Thermal Identifiability

**CLAIM_ID:** `W3_36_BIRTH_THRESHOLD_THERMAL_CLOSURE`

**CLAIM:** The finite-birth RefG dictionary is internally consistent and exactly identifies its own closure boundary: it allows a faster integrable early cadence, fixes the process-time, ruler, already-activated-null, and local-threshold identities, and leaves the physical, thermal, and observational histories underdetermined.

**TYPE:** `EXACT_IDENTITY_CONDITIONAL_NO_GO_AND_CLOSURE_LEDGER`. This is a symbolic closure gate, not an observational fit and not a physical cosmology PASS.

**MODEL_VERSION:** `W3-36-v1.2-FINITE-BIRTH`. This version adds an explicit local-continuity/Leibniz moving-boundary derivation, exact boundary/equality/thermal-sign proofs, and a single-scale-per-entry CODES freedom ledger. Any later change to the finite-origin convention, cadence-pressure bridge, scale split, threshold or moving-boundary domain, thermal source ledger, observable definitions, claim scope, or closure keys creates a new model version.

**ASSUMPTIONS:**

1. The history begins at finite metric coordinate time `t=0`; today is `t=T0>0`.
2. Material/process time is the elapsed quantity
   $$
   \tau(t)=\int_0^t p(s)\,ds,
   $$
   with `p(t)>0`. A finite value of `tau(T0)` is allowed and is not a failure.
3. The foundation cadence bridge and operational scale dictionary are
   $$
   p^2=P_F/P_{F0},\qquad d\tau=p\,dt,\qquad A=a/p,
   $$
   where `P_F` is foundation/background pressure and `a` is the foundation-link scale.
4. The homogeneous already-activated metric is
   $$
   ds^2=p^2c_0^2dt^2-\frac{a^2}{p^2}d\chi^2
       =c_0^2d\tau^2-A^2d\chi^2.
   $$
5. Cosmic birth is global and has no preferred spatial center. `R_act` in this gate denotes a local activation/correlation threshold scale, not a cosmic outer edge.
6. A threshold field `Phi(chi,t)` is differentiable near `Phi=Phi_*`, with nonzero spatial gradient there. The threshold is a level set; it is not assumed to be the infinitesimal null leading edge.
7. Foundation pressure `P_F` and matter--radiation thermodynamic pressure `P_th` are distinct state variables. No equality or constitutive map between them is assumed.
8. The radiation branch uses the conditional equilibrium identities `rho_gamma=a_R T^4` and `P_gamma=rho_gamma/3`, with positive radiation constant `a_R`, and the source ledger `rho_gamma'+4H_tau rho_gamma=Q_gamma`.
9. The statement `T_RefG<T_standard` is a hypothesis to be tested. It is not an input, pass condition, or derived fact in W3-36.
10. The moving-boundary subcheck uses a local flat spherical Eulerian radius `r`, the local conservation law `partial_t rho+r^(-2)partial_r(r^2 J)=S_E`, and a regular center `lim_(r->0) r^2 J=0`. It is a local ledger, not a centered global-universe model.

**DOMAIN:** Positive differentiable `p`, `a`, and `P_F` for `t in (0,T0]`; an integrable or classifiable one-sided origin; differentiable threshold fields with `partial_chi Phi != 0`; a local flat spherical Eulerian patch for the moving-boundary ledger; positive equilibrium radiation variables in the conditional thermal branch. No continuum claim is made below the theory's activation/resolution threshold.

**CONVENTIONS:** `tau(0)=0` and elapsed process time is positive. Signature is `(+---)`. A dot denotes `d/dt`; a prime denotes `d/d tau`. `c0` has speed units; pressures and energy densities share energy-per-volume units; `J_b>0` is outward boundary energy flux density; `Q_V=int_0^R r^2 S_E dr` is the signed bulk energy-source rate per unit solid angle; `Q>0` transfers energy from the foundation sector to the thermal sector; `Q_gamma>0` injects energy into radiation; and positive `Pi_F` enters the foundation continuity equation as pressure. `P_F` controls the cadence bridge; `P_th` is obtained from a material stress tensor or equation of state. Temperature comparisons must be expressed through operational dimensionless quantities such as `k_B T/E_atom`, the photon occupation variable `h nu/(k_B T)`, and reaction-to-expansion ratios `Gamma/H_tau`.

**FREEDOM_LEDGER:** No fitted exponent, cosmological parameter, thermal rescaling, field potential, threshold value, source history, or desired age is introduced; current fitted effective dimension is `d_eff=0`. The asymptotic exponent `beta` only classifies integrability of a candidate output `p(t)~C t^(-beta)` and is neither selected nor fitted. Every entry below is open and uninstantiated; `scale` uses only the CODES categories, and `effective_complexity_measure` states what a future closure must count:

- `activation_and_threshold`: source = foundation action and initial state; domain = global birth and regular local-threshold neighborhoods; scale = `universal`; effective_complexity_measure = functional/infinite-dimensional field and initial-spectrum modes, one threshold scalar, and one discrete topology index until frozen.
- `background_dynamics`: source = foundation action and energy balance; domain = positive differentiable homogeneous histories on `(0,T0]`; scale = `universal`; effective_complexity_measure = functional/infinite-dimensional, including at least `P_F(t)`, `a(t)`, and every unfrozen stress or transfer history.
- `thermal_species_closure`: source = matter/radiation stress tensor and kinetic/EOS law; domain = each thermal species or sector; scale = `group`; effective_complexity_measure = functional/infinite-dimensional per species or sector until a finite EOS/collision parametrization is preregistered.
- `photon_propagation_law`: source = foundation radiative action; domain = universal massless propagation sector; scale = `universal`; effective_complexity_measure = functional/infinite-dimensional dispersion and coupling laws until frozen.
- `atomic_SPS_response`: source = atomic response and SPS calibration; domain = each transition, population, or response family; scale = `group`; effective_complexity_measure = functional/infinite-dimensional per response family until parameterized.
- `source_history_and_luminosity`: source = individual emitter history; domain = each astrophysical source; scale = `object`; effective_complexity_measure = one functional history per object, or `k_object` parameters per object after preregistration.
- `survey_instrument_calibration`: source = survey/instrument calibration model; domain = each survey or instrument configuration; scale = `group`; effective_complexity_measure = `N_calibration` parameters per survey/instrument group after preregistration.
- `datum_selection_and_noise`: source = datum-level likelihood and selection model; domain = individual measurements or catalog entries; scale = `data`; effective_complexity_measure = `N_nuisance` declared by a future forward model; `N_nuisance=0` in W3-36 because no data are read.

**DEPENDENCIES:** None. W3-36 is a self-contained symbolic gate. It derives dictionary and continuity consequences and checks explicitly labeled assumption--consequence branches without importing upstream result artifacts.

**METHOD:** Exact SymPy differentiation, substitution, integration, inequality classification, two-sector conservation, radiation-source algebra, rate/scale cancellation, mutation controls, exact schema-keyset checks, and strict atomic JSON output. Symbolic methods are selected because the single claim concerns identities and identifiability rather than parameter estimation or empirical fit. No real data are read.

**PASS_CONDITION:** Every declared exact identity simplifies to zero; every mutation is detected; the finite/infinite origin classification is correct; the two pressures remain independent; all required contract and result keys are exact; all physical and observational closure flags remain false; and the aggregate identity flag is the logical AND of its atomic checks.

**FAIL_CONDITION:** Any algebraic identity or mutation check fails; a finite process age is labeled a failure; the threshold is silently identified with the null front; a local threshold radius is called the universe's outer edge; `P_F` is equated with thermodynamic pressure; a numerical temperature, process age, `H_CC(z)`, or `D_L(z)` is reported without its missing closure; or the result schema/provenance is incomplete.

**FALSIFIER:** A symbolic counterexample to a claimed exact identity under the frozen assumptions falsifies that identity. This gate has no RefG-wide falsifier because it does not close a physical cosmology.

**RESIDUAL:** Exact symbolic expressions required to simplify to integer zero. For the thermal comparison, the required result is non-identifiability: `T_RefG/T_standard=(P_gamma,RefG/P_gamma,standard)^(1/4)` under the radiation EOS, while the pressure ratio is not fixed by `p` alone.

**ERROR_BOUND:** Zero for exact algebra. Numerical, observational, and continuum-truncation errors are N/A because no such result is produced.

**VALIDITY_HEALTH:** W3-36 may validate a dictionary and identify missing closures. It cannot validate the universe's birth mechanism, a physical temperature reduction, CMB/BBN compatibility, or cosmological observations.

**BRANCHES:**

- `GENERIC_FINITE_BIRTH`: classifies `p~C t^(-beta)`; process age is finite for `beta<1`, logarithmically divergent at `beta=1`, and power divergent for `beta>1`.
- `THRESHOLD_LEVEL_SET`: derives threshold speed from `Phi(chi_act(t),t)=Phi_*` without choosing a PDE.
- `ALREADY_ACTIVATED_NULL`: checks the metric null ray only inside the activated effective geometry and does not identify it with cosmic birth.
- `MOVING_BOUNDARY_ENERGY`: derives the exact Reynolds energy ledger; it forbids constant active energy unless boundary flux, source, and sweep terms satisfy the required cancellation.
- `RADIATION_EQUILIBRIUM`: converts a specified thermodynamic radiation pressure to temperature and gives `d ln(TA)/d tau=Q_gamma/(4rho_gamma)`. For `Q_gamma=0` and `1+z=A0/Ae`, it recovers `T_e=T_0(1+z)`; cadence rescaling alone cannot lower the temperature.
- `THERMAL_SOURCE_CLASSIFIER`: with `J_e=int_e^0 Q_gamma/(4rho_gamma)d tau`, `T_e/[T_0(1+z)]=exp(-J_e)`; strict monotonicity classifies the sign of the full integrated `J_e` relative to the adiabatic reference with the same scale-factor endpoints. A lower, equal, or higher temperature cannot be chosen from `p` alone.
- `COMMON_CADENCE_CANCELLATION`: if `Gamma_t=p Gamma_tau` and `H_t=p H_tau`, then `Gamma_t/H_t=Gamma_tau/H_tau` and accumulated cycle counts are invariant.
- `CONDITIONAL_FRONT_CROSSCHECK`: define `q=d ln a/d ln P_F` and `D=1+3q`. Assume, only inside this hypothetical branch, constant active energy, spherical volume, and a same-null front. Check the consequences `D(R) dR/dt=c0 p^2` and `d tau/dR=D(R)/(c0 p)`. The further results `p~t^(-3/8)` and elapsed interval `8T0/5` belong only to the constant-`D=D0>0` (constant-`q`) sub-branch. This is an assumption-consequence check, not a derivation of the closure, the current birth model, or an inferred age.

**OBSERVABLE_MAP:** Only the operational definitions
$$
H_{CC}=-(1+z_{spec})^{-1}\frac{dz_{spec}}{d\tau_{SPS}},
\qquad
1+z_{spec}=\frac{\nu_{A,0}}{\nu_{obs}}
$$
are recorded. The factorization `nu_obs=nu_A,e A_e/A_0`, and hence `1+z_spec=(A_0/A_e)(nu_A,0/nu_A,e)`, is an open photon/atomic map rather than a definition. These expressions become predictions only after the stellar-population clock, atomic-frequency, photon-energy, and geometric maps are derived. `D_L` remains undefined until photon flux, arrival rate, reciprocity, and source luminosity are closed.

**FORWARD_MODEL:** N/A. W3-36 produces no synthetic CMB, abundance, supernova, chronometer, BAO, or JWST observable.

**DATA_ROLE:** No observational data or upstream result artifacts are used.

**IDENTIFIABILITY:** The frozen identities identify `p` from `P_F`, `A=a/p`, elapsed `tau` once `p(t)` is known, threshold speed once `Phi` is known, and equilibrium `T` once `P_gamma` is known. They do not identify `P_F(t)`, `P_th(t)`, `Phi`, `a(t)`, `T(t)`, `z_spec(t)`, `H_CC(z)`, or `D_L(z)`.

**BENCHMARK:** Exact checks must reproduce the metric/process dictionary, the level-set chain rule, the spherical moving-boundary energy balance, origin integrability, and the constant-`D` conditional `8T0/5` interval. Deliberately altered signs, missing boundary sweep, conflated pressures, and null-front identification must fail.

**CLOSURE_FLAGS:**

Exact/computational flags:

- `cadence_pressure_identity_exact`
- `metric_process_dictionary_exact`
- `simultaneous_expansion_and_ruler_shrinkage_consistent`
- `operational_scale_rate_identity_exact`
- `already_activated_null_identity_exact`
- `threshold_level_set_speed_exact`
- `foundation_threshold_radius_chain_rule_exact`
- `moving_boundary_energy_ledger_exact`
- `constant_active_energy_condition_exposed`
- `foundation_thermal_pressures_independent`
- `finite_process_origin_classified`
- `high_cadence_process_bound_exact`
- `volume_measure_jacobian_exact`
- `two_sector_conservation_sum_exact`
- `radiation_temperature_identity_exact`
- `radiation_temperature_source_identity_exact`
- `adiabatic_Tz_no_go_exact`
- `lower_temperature_sign_classifier_exact`
- `lower_temperature_nonidentifiability_exact`
- `common_cadence_rate_H_cancellation_exact`
- `same_null_residual_exposed`
- `conditional_front_assumption_crosscheck_exact`
- `observable_definitions_recorded`
- `schema_keysets_exact`
- `mutation_controls_pass`
- `aggregate_identity_pass`

Physical/observational closure flags, all required to remain false:

- `amplitude_action_derived`
- `threshold_value_derived`
- `initial_spectrum_and_topology_derived`
- `activation_front_eom_derived`
- `foundation_energy_balance_derived`
- `foundation_to_thermal_transfer_derived`
- `a_of_P_F_derived`
- `finite_process_age_numerically_predicted`
- `temperature_history_derived`
- `temperature_below_standard_derived`
- `spectroscopic_redshift_derived`
- `stellar_population_clock_derived`
- `H_CC_curve_derived`
- `luminosity_distance_derived`
- `CMB_recombination_BBN_validated`
- `JWST_structural_growth_validated`

**CROSSCHECK:** Use two independent process-time derivations; differentiate the threshold constraint directly; verify the moving-boundary ledger with and without flux/source/sweep terms; derive the general beta-not-equal-to-one antiderivative and classify `beta={1/2,1,3/2}`; recover `8/5` at `beta=3/8` only on the constant-`D` sub-branch; prove `tau_0>=T_0` for early `p>=1`; distinguish `a^3` and `A^3` volume ledgers; cancel a common cadence in `Gamma/H`; recover adiabatic `T(z)`; and demonstrate two different positive thermodynamic pressures at fixed `P_F` and `p`.

**PROVENANCE:** Freeze the preregistration SHA-256 in the source. Record source hash, Python/SymPy versions, UTC time, and all closure flags in strict JSON. Write the generated result SHA-256 to a separate LF-stable checksum file. Write both outputs atomically with `allow_nan=False`.

**FILES:** `w3_36_birth_threshold_thermal_preregistration.md`, `w3_36_birth_threshold_thermal.py`, `w3_36_result.json`, and `w3_36_result.sha256`.

## Decision semantics

If all exact checks pass while every physical closure remains false, the status is `PASS_EXACT_IDENTITIES__FINITE_BIRTH_COMPATIBLE__PHYSICAL_AND_THERMAL_CLOSURES_OPEN`. This status validates the bookkeeping only. It neither establishes that the early physical temperature was lower than the standard reconstruction nor supplies an observational cosmology.
