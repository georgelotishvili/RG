# W3-40 Preregistration: Single-Driver Expansion--Relaxation Causal Lock

**CLAIM_ID:** `W3_40_EXPANSION_RELAXATION_CAUSAL_LOCK`

**CLAIM:** On the frozen selected branch, foundation expansion is the sole primary cosmological driver. With fixed comoving link count, its increase of the foundation link scale lowers foundation pressure; through the positive bridge p^2=P_F/P_F0, that pressure relaxation contracts the material standard. These are causally ordered stages of one trajectory, not independent or additive effects. An internal observer reads the trajectory only through the relational scale A=a/p; A alone does not identify a and p. The gate proves the linked scale and rate identities but does not derive P_F(a) or an observational cosmology.

**TYPE:** `EXACT_CONDITIONAL_CAUSAL_DICTIONARY_AND_IDENTIFIABILITY_GATE`. This is an assumption--consequence and identifiability gate, not a derivation of background dynamics and not an observational fit.

**MODEL_VERSION:** `W3-40-v1.2-SINGLE-DRIVER-EXPANSION-RELAXATION-CAUSAL-LOCK`. A change to the causal ordering, unique-primary-root condition, sign assumptions, cadence--pressure bridge, operational scale, comoving convention, identifiability class, semantic constraints, or closure keys creates a new model version.

**ASSUMPTIONS:**

1. The selected homogeneous expansion branch uses positive differentiable scales and a fixed ideal-comoving link count, `N_12>0` and `dN_12/dt=0`.
2. One foundation link has length `ell_F(t)=ell_F0 a(t)`, with `a(t)>0` and `a_dot>0` on the selected branch.
3. Foundation pressure is positive and relaxes along that trajectory: `P_F>0` and `dP_F/da<0`. Locally define the positive logarithmic relaxation response `kappa=-d ln(P_F)/d ln(a)>0`. No function `P_F(a)` and no value or history of `kappa` is supplied.
4. The positive material scale and cadence obey `p^2=P_F/P_F0`, with `P_F0>0` and present normalization `p_0=1`.
5. A material ruler has length `ell_mat(t)=ell_mat0 p(t)`. The operational cosmological scale is `A=a/p`.
6. The causal order is `a -> P_F -> p`, followed by the internal readout `(a,p) -> A`. The graph has exactly one primary root, `a`. Pressure relaxation and material contraction are dependent stages of the foundation-expansion trajectory, not independently postulated or additive cosmological effects; `A` is a relational readout, not their sum.
7. Only the scale dictionary and its exact differential consequences are tested. The map from `A` to spectroscopic redshift, photon flux, luminosity distance, standard candles, standard rulers, thermal history, and structure growth is not assumed.

**DOMAIN:** Positive finite `a`, `P_F`, `P_F0`, `p`, `ell_F0`, `ell_mat0`, and `N_12`; differentiable homogeneous histories on any regular post-origin interval; `a_dot>0`; local logarithmic response `kappa>0`. The gate has no claim at singular endpoints or below the foundation's operational-resolution domain.

**CONVENTIONS:** A dot denotes differentiation with respect to the metric-coordinate parameter `t`; process time satisfies `d tau=p dt`; `N_12` counts the fixed links of the ideal expansion component; local peculiar motion may change an actual pair's link count and lies outside this gate; `P_F` is foundation pressure and is not thermodynamic pressure; `p` is a dimensionless material-size/cadence scale; `A` is the dimensionless operational scale.

**FREEDOM_LEDGER:** No fitted exponent, response history, cosmological parameter, source function, calibration, or datum is introduced; the current data-fitted effective dimension is zero.

- `foundation_expansion_history`: source = foundation action and initial state; domain = positive homogeneous histories; scale = `universal`; effective complexity = one functional history `a(t)` until derived; status = open.
- `pressure_relaxation_law`: source = foundation energy balance and constitutive dynamics; domain = the selected expansion branch; scale = `universal`; effective complexity = one functional relation `P_F(a)` or `kappa(a)` until derived; status = sign frozen, magnitude/history open.
- `material_response_law`: source = foundation--matter microphysics; domain = universal material standards; scale = `universal`; effective complexity = the frozen bridge `p^2=P_F/P_F0` in this gate, with its microscopic derivation open.
- `photon_atomic_response`: source = radiative and atomic action; domain = each response family; scale = `group`; effective complexity = functional per transition or response family until frozen; status = open.
- `source_history`: source = each astrophysical emitter; domain = each source; scale = `object`; effective complexity = one functional source history per object until parameterized; status = open.
- `likelihood_nuisance`: source = future surveys and likelihoods; domain = each datum or declared group; scale = `data`; effective complexity = zero here and future declared nuisance count; status = open.

**DEPENDENCIES:** None. W3-40 is a self-contained causal-dictionary gate and imports no upstream result artifact.

**METHOD:** Exact SymPy substitution, differentiation, logarithmic chain rules, positive-sign classification, comoving distance/ruler normalization, common-rescaling invariance, an explicit normalized functional-history many-to-one construction, acyclic causal-graph and unique-primary-root checking, mutation controls, exact schema-keyset checks, canonical LF validation, pinned preregistration hashing, strict JSON, and atomic result/checksum writes.

**PASS_CONDITION:** Every registered identity, causal-order consistency check, unique-primary-root check, identifiability construction, keyset check, and mutation control passes; every physical and observational closure flag remains false; the aggregate flag is the logical AND of its atomic checks.

**FAIL_CONDITION:** Any exact identity, sign consequence, graph check, invariance, non-identifiability construction, mutation, canonical-text check, or schema keyset fails; the causal graph has any primary root other than `a`; any physical or observational closure flag is true; the result treats `p` as an independent or additive cosmological driver; or the result reports `P_F(a)`, redshift, `H(z)`, or `D_L(z)` without a derived closure.

**FALSIFIER:** A symbolic counterexample to a registered exact consequence under the frozen assumptions falsifies this gate. Observations do not directly falsify this dictionary gate because it contains no observational forward model; they test a future closed physical branch.

**RESIDUAL:** Exact zero residuals for definitions and differential identities, strict inequalities under positive symbols, exact graph and keyset predicates, and exact equality of operational scales under the declared common rescaling.

**ERROR_BOUND:** Zero for exact algebra. Numerical, continuum, parameter-estimation, and observational errors are N/A because no numerical model or data are used.

**VALIDITY_HEALTH:** The gate can validate the internal causal dictionary and expose A-only non-identifiability. It cannot validate the expansion equation, pressure law, material microphysics, photon propagation, thermal history, structure formation, or observations.

**BRANCHES:**

- `IDEAL_COMOVING_CAUSAL_TRAJECTORY`: `N_12` is fixed; `a` is the unique primary causal root; `a_dot>0`, `dP_F/da<0`, `p^2=P_F/P_F0`, and `A=a/p`.
- `A_ONLY_EQUIVALENCE_CLASS`: positive simultaneous rescalings `(a,p,P_F)->(lambda a,lambda p,lambda^2 P_F)` preserve both `A` and the cadence--pressure bridge. For normalized histories, `lambda(t_0)=1` preserves the present normalization while leaving a nontrivial positive functional freedom away from `t_0`; `A` alone therefore leaves an equivalence class.
- `LOCAL_PECULIAR_MOTION`: outside the ideal expansion component, `N_12` may change; no identity here forbids local motion.

**OBSERVABLE_MAP:** The exact operational length statement is `L_12/ell_mat=(N_12 ell_F0/ell_mat0) A`. No identification of `A_0/A_e` with spectroscopic redshift is made. Atomic-frequency evolution, photon energy/phase transport, arrival rates, reciprocity, source luminosity, and survey calibration remain open.

**FORWARD_MODEL:** N/A. The gate produces no synthetic supernova, chronometer, BAO, CMB, BBN, standard-siren, or structure-growth observable.

**DATA_ROLE:** No data or upstream result artifact is read.

**IDENTIFIABILITY:** The dictionary identifies `p` once `P_F` is supplied and identifies `A` once `a` and `p` are supplied. `A` alone is many-to-one under any admissible positive differentiable function `lambda(t)` through `(a,p,P_F)->(lambda(t)a,lambda(t)p,lambda(t)^2P_F)`. The normalized witness fixes `lambda(t_0)=1`, preserves `a(t_0)=p(t_0)=P_F(t_0)/P_F0=1`, and leaves distinct histories away from `t_0`. A derived `P_F(a)` law, normalization history, or independent dimensionless response channel is required to separate `a` and `p`.

**BENCHMARK:** The exact benchmark must reproduce `L_12=N_12 ell_F0 a`, `p=sqrt(P_F/P_F0)`, `A=a/p`, `d ln p/d ln a=-kappa/2`, and `H_A^(tau)=(H_a/p)(1+kappa/2)`, and must verify that `a` is the unique primary causal root. For `x=(t-t_0)/t_0` and positive `h,epsilon,delta`, it must also compare `a_1=exp(hx)`, `p_1=exp[-(epsilon+delta)x]`, `P_1=P_F0 p_1^2` with the normalized rescaling `lambda=exp(epsilon x)`, `a_2=lambda a_1`, `p_2=lambda p_1`, `P_2=lambda^2P_1`; verify identical `A`, present normalization, the bridge identity in each history, causal signs, and distinct histories; and detect reversed pressure response, a broken square-root bridge, a product-scale mutation, independent material-rate insertion, an independent-material-root mutation, keyset drift, and a physical-closure flag flip.

**CLOSURE_FLAGS:**

Exact/computational flags required true:

- `fixed_comoving_link_count_encoded_exact`
- `foundation_link_and_distance_identity_exact`
- `cadence_pressure_bridge_exact`
- `pressure_relaxation_implies_material_contraction_exact`
- `operational_scale_identity_exact`
- `causal_DAG_acyclic_exact`
- `single_primary_foundation_expansion_root_exact`
- `causal_locked_log_rate_identity_exact`
- `causal_locked_process_rate_identity_exact`
- `single_trajectory_operational_growth_positive_exact`
- `A_common_rescaling_invariance_exact`
- `A_only_nonidentifiability_exact`
- `registered_top_level_keysets_exact`
- `mutation_controls_pass`
- `aggregate_identity_pass`

Physical and observational closure flags required false:

- `foundation_action_derived`
- `expansion_equation_derived`
- `foundation_energy_balance_derived`
- `P_F_of_a_derived`
- `material_bridge_microphysics_derived`
- `kappa_history_derived`
- `absolute_foundation_link_scale_observed`
- `absolute_material_scale_observed`
- `spectroscopic_redshift_forward_map_derived`
- `photon_atomic_transport_derived`
- `H_of_z_derived`
- `luminosity_distance_derived`
- `supernova_time_dilation_derived`
- `CMB_BBN_BAO_validated`
- `structure_growth_validated`
- `observational_discriminator_validated`

**CROSSCHECK:** Re-derive the ruler-normalized distance directly; compute the pressure-to-material chain with ordinary and logarithmic derivatives; differentiate `A=a/p` in coordinate and process time; verify the causal DAG and its unique primary root `a`; execute the normalized positive functional-history equivalence witness at fixed `A`; and require deliberate sign, bridge, product-scale, independent-rate, independent-root, rescaling, keyset, and physical-flag mutations to fail.

**PROVENANCE:** Freeze the preregistration SHA-256 in the source; require canonical UTF-8 LF text ending in one newline; record preregistration/source hashes, Python/SymPy versions, UTC generation time, and all closure flags; serialize with `allow_nan=False`; write result and checksum atomically.

**FILES:** `README.md`, `w3_40_expansion_relaxation_causal_lock_preregistration.md`, `w3_40_expansion_relaxation_causal_lock.py`, `w3_40_result.json`, and `w3_40_result.sha256`. Repository-level `.gitattributes` and `.gitignore` provide the canonical LF and generated-file rules.

## Decision semantics

If all exact checks pass while every physical and observational closure remains false, the status is `PASS_EXACT_CAUSAL_LOCK_DICTIONARY__DYNAMICS_AND_OBSERVABLES_OPEN`. This status validates one supplied single-driver causal trajectory and its relational operational dictionary; it does not derive the trajectory from the foundation action or establish an observational cosmology.
