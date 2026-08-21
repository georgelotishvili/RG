# W3-41 Preregistration: Foundation Constitutive Interface

**CLAIM_ID:** W3_41_FOUNDATION_CONSTITUTIVE_INTERFACE

**CLAIM:** For a homogeneous one-coordinate foundation cell with volume $V_F=V_0a^3$, the mechanical generalized pressure conjugate to volume is fixed exactly by its energy $E_F(a)$. On the separately declared candidate bridge $P_F\equiv\Pi_F$, this gives exact formulas for the relaxation response $\kappa$, the bulk modulus, the material scale, and the operational scale. The same interface admits every positive decreasing $P_F(a)$ and every positive $\kappa(a)$, so it does not select a physical constitutive law or a power-law exponent. A microscopic foundation dynamical principle, a derived $P_F$--$\Pi_F$ bridge, and an expansion equation remain necessary.

**TYPE:** EXACT_CONDITIONAL_CONSTITUTIVE_DICTIONARY_AND_RECONSTRUCTION_NONUNIQUENESS_GATE. This gate proves an energy--stress interface and its nonselection theorem. It is not a derivation of the foundation dynamics, the physical $P_F(a)$ law, or an observational cosmology.

**MODEL_VERSION:** W3-41-v1.2-FOUNDATION-CONSTITUTIVE-INTERFACE. Version 1.2 carries forward the explicit open volume-law and one-coordinate-reduction closures, positive-bulk-modulus terminology, exact $n\to3$ energy limit, and shared-validator mutations introduced in v1.1, while broadening the missing microscopic-premise flag from action alone to action, Hamiltonian, or equivalent foundation dynamics. A change to the volume map, energy derivative convention, pressure roles, candidate mechanical bridge, regularity class, reconstruction family, power-law audit, dependency hash, validator semantics, closure keys, or claim scope creates a new model version.

**ASSUMPTIONS:**

1. W3-40 v1.2 is the frozen upstream causal dictionary. Its result SHA-256 is e8104a664484ea0735387446c94367cca1035877ee6a26413eeddaf158b5be64.
2. The homogeneous post-origin branch has $a>0$, present normalization $a_0=1$, a fixed ideal-comoving cell/link count, and the declared interface ansatz $V_F(a)=V_0a^3$ with $V_0>0$. The microscopic theory has not yet derived this volume law.
3. $E_F(a)$ is the complete adiabatic energy of that fixed comoving foundation cell at fixed conserved charges and belongs to $C^2$ on the declared interval.
4. The mechanical generalized foundation pressure is defined by
   $$
   \Pi_F(a)=-\left.\frac{\partial E_F}{\partial V_F}\right|_{Q}.
   $$
5. W3-40's cadence-controlling foundation scalar $P_F$ and the mechanical generalized pressure $\Pi_F$ are distinct until the candidate bridge
   $$
   \mathcal B_{\rm mech}:\quad P_F\equiv\Pi_F
   $$
   is explicitly selected. This gate tests consequences of that bridge and does not derive it.
6. Matter--radiation thermodynamic pressure $P_{\rm th}$ is a third, distinct variable and supplies no equation of state to this gate.
7. On the candidate mechanical branch, $P_F>0$ and $dP_F/da<0$ define the selected relaxation sector. The positive logarithmic response is $\kappa=-d\ln P_F/d\ln a$.
8. W3-40's material dictionary $p^2=P_F/P_{F,0}$ and $A=a/p$ is used only after $P_F$ is supplied.
9. The one-coordinate cell is a declared state reduction, not a derived completeness result. It contains no hidden strain coordinates, hysteresis, entropy production, surface term, or undeclared inter-sector transfer. Any such variable requires an enlarged state space and lies outside this gate.
10. No datum, temperature, fitted exponent, desired age, source history, or target cosmological curve enters the calculation.

**DOMAIN:** A regular post-origin homogeneous interval $I\subset(0,\infty)$ containing $a=1$; $E_F\in C^2(I)$; positive $V_0$ and $P_{F,0}$. Reconstruction uses positive $C^1$ pressure or response functions. The gate has no claim at $a=0$, at the Genesis boundary, inside local compact-object deficits, or in a thermal/observational sector.

**CONVENTIONS:** Prime means $d/da$. Positive $\Pi_F=-dE_F/dV_F$ is compressive generalized pressure. The bulk modulus is $K_\Pi=-V_Fd\Pi_F/dV_F$. On the candidate bridge, $K_F=K_\Pi$. $P_F$ controls $p$; $\Pi_F$ is conjugate to foundation volume; $P_{\rm th}$ belongs to matter/radiation thermodynamics. These names are never interchanged silently.

**FREEDOM_LEDGER:** No data-fitted freedom is used; the present fitted effective dimension is zero.

- foundation_dynamics: source = pregeometric microscopic theory; domain = universal foundation; scale = universal; effective complexity = an unselected action, Hamiltonian, or equivalent dynamical principle with field content, symmetries, and boundary data; status = open.
- homogeneous_energy: source = homogeneous reduction of the foundation dynamics; domain = fixed-charge comoving cells; scale = universal; effective complexity = one unselected function $E_F(a,Q)$ plus every omitted state coordinate; status = interface variable only.
- pressure_bridge: source = foundation state/clock microphysics; domain = homogeneous foundation branch; scale = universal; effective complexity = one unselected map between $P_F$ and mechanical stress $\Pi_F$; status = identity used only on a labeled candidate branch.
- background_kinetics: source = kinetic part of the foundation dynamics and initial state; domain = homogeneous histories; scale = universal; effective complexity = an unselected kinetic functional and initial data; status = open.
- material_response: source = foundation--oscillon microphysics; domain = material standards; scale = universal; effective complexity = W3-40's frozen bridge with microscopic derivation open.
- future_observables: source = photon, matter, source, and likelihood models; domain = each declared group or datum; scale = group/data; effective complexity = zero here and fully declared in a future forward model; status = open.

**DEPENDENCIES:** The script reads and verifies the exact W3-40 result and checksum, including the single primary root $a$, the dependent material response, the $A$-only nonidentifiability result, and every still-open physical closure needed here. W3-36 is not an algebraic dependency.

**METHOD:** Exact SymPy differentiation, chain rules, fundamental-theorem reconstruction, branch-sign classification, two distinct power-law witnesses, generic and $n=3$ energy reconstruction, the exact $n\to3$ limit, upstream result/hash verification, semantic role separation, shared-validator negative mutations, strict JSON, and atomic checksum output.

**PASS_CONDITION:** Every declared derivative, reconstruction, sign, and power-law identity has exact zero residual; W3-40 is verified; $P_F$, $\Pi_F$, and $P_{\rm th}$ remain distinct; the candidate bridge is labeled conditional; two admissible normalized pressure laws demonstrate nonselection; no exponent or physical history is selected; every mutation is detected; every physical and observational closure flag remains false.

**FAIL_CONDITION:** Any exact identity, dependency, schema, or mutation fails; $P_F=\Pi_F$ is reported as a derived fact; $P_{\rm th}$ is substituted for either foundation pressure; existence of an energy function is reported as selection of a unique $P_F(a)$; a value of $n$ is chosen, fitted, or promoted to a prediction; an independent material driver is inserted; or $a(t)$, $H(z)$, $D_L(z)$, temperature, or data compatibility is reported without its missing dynamics.

**FALSIFIER:** An exact counterexample to any registered identity under the frozen assumptions falsifies this gate. A future microscopic action, Hamiltonian, or equivalent dynamics that selects a specific $E_F$ does not falsify the nonselection theorem; it supplies the missing premise and opens a separate mechanism-derived gate.

**RESIDUAL:** Exact symbolic zero for all derivative and reconstruction identities; exact Boolean branch and role predicates; exact upstream hash/status checks.

**ERROR_BOUND:** Zero for exact algebra and hashes. Numerical, continuum, parameter-estimation, and observational errors are not applicable.

**VALIDITY_HEALTH:** PASS establishes the minimal constitutive interface and proves that it cannot select the physical law by itself. It does not validate the candidate bridge, choose $E_F$, derive $a(t)$, or confront data.

**BRANCHES:**

- MECHANICAL_STRESS_DICTIONARY: $V_F=V_0a^3$ and $\Pi_F=-dE_F/dV_F$.
- CANDIDATE_FOUNDATION_MECHANICAL_BRIDGE: $P_F=\Pi_F$, explicitly conditional.
- POSITIVE_BULK_MODULUS_RELAXATION: $P_F>0$, $K_F>0$, and $P_F'<0$. This is a one-coordinate constitutive condition, not a claim of full dynamical or spectral stability.
- GENERAL_PRESSURE_RECONSTRUCTION: any positive $C^1$ $P_F(a)$ reconstructs an $E_F(a)$ up to an additive constant.
- GENERAL_KAPPA_RECONSTRUCTION: any positive $\kappa(a)$ reconstructs $P_F$, $p$, and $A$ but is not selected.
- POWER_LAW_AUDIT: $P_F=P_{F,0}a^{-n}$ is equivalent to the constitutive choice $\kappa=n$.
- HIDDEN_STATE_VARIABLES: outside the gate; an enlarged state space is required.

**OBSERVABLE_MAP:** None. The gate produces only $E_F$--$\Pi_F$--$P_F$--$\kappa$--$p$--$A$ conditional identities as functions of $a$. No time history or photon observable is defined.

**FORWARD_MODEL:** Not applicable. No synthetic redshift, distance, thermal, structure-growth, or likelihood prediction is generated.

**DATA_ROLE:** No observational or calibration data are read. W3-40 is a logical upstream artifact, not a fitted datum.

**IDENTIFIABILITY:** Once a physical $E_F(a)$ and the bridge $P_F=\Pi_F$ are supplied, $P_F(a)$ is identified up to no further functional freedom. Conversely, every admissible $P_F(a)$ reconstructs an $E_F(a)$ up to an additive constant, so the interface alone selects neither function. Every positive $\kappa(a)$ generates a distinct admissible history family. Microscopic foundation dynamics and a derived state-space reduction are required to choose among them.

**BENCHMARK:** Recover
$$
\Pi_F=-\frac{E_F'}{3V_0a^2},\qquad
K_\Pi=\frac{aE_F''-2E_F'}{9V_0a^2},
$$
$$
\Pi_F'=-\frac{3K_\Pi}{a},\qquad
\kappa=\frac{3K_F}{P_F}=2-\frac{aE_F''}{E_F'}
$$
on the candidate bridge. Recover
$$
E_F(a)=E_F(1)-3V_0\int_1^a u^2P_F(u)\,du,
$$
$$
P_F(a)=P_{F,0}\exp\!\left[-\int_1^a\frac{\kappa(u)}{u}\,du\right],
$$
$$
p(a)=\exp\!\left[-\frac12\int_1^a\frac{\kappa(u)}{u}\,du\right],
\qquad
A(a)=a\exp\!\left[\frac12\int_1^a\frac{\kappa(u)}{u}\,du\right].
$$
For $P_F=P_{F,0}a^{-n}$ recover $K_F=nP_F/3$, $\kappa=n$, $p=a^{-n/2}$, $A=a^{1+n/2}$, the generic energy on the explicit domain $n>0$, $n\ne3$, and the logarithmic $n=3$ branch. Verify the exact limit of the generic energy as $n\to3$, and verify separately that $n=1$ and $n=2$ satisfy every sign and positive-bulk-modulus condition but remain distinct.

**CLOSURE_FLAGS:**

Exact/computational flags required true:

- foundation_volume_jacobian_exact
- mechanical_pressure_from_energy_exact
- bulk_modulus_from_energy_exact
- pressure_slope_bulk_modulus_identity_exact
- kappa_bulk_modulus_identity_exact
- energy_derivative_branch_conditions_exact
- pressure_to_energy_reconstruction_exact
- kappa_to_pressure_reconstruction_exact
- kappa_to_material_scale_exact
- kappa_to_operational_scale_exact
- power_law_equivalence_exact
- power_law_energy_generic_exact
- power_law_energy_n3_exact
- power_law_energy_n3_limit_exact
- power_law_family_nonselection_exact
- foundation_pressure_roles_distinct_exact
- w3_40_dependency_verified
- registered_top_level_keysets_exact
- mutation_controls_pass
- aggregate_identity_pass

Physical and observational closure flags required false:

- foundation_volume_law_derived
- one_coordinate_state_reduction_derived
- foundation_pressure_equals_mechanical_pressure_derived
- foundation_dynamics_derived
- foundation_energy_function_selected
- foundation_energy_balance_derived
- P_F_of_a_selected
- kappa_history_selected
- power_law_exponent_selected
- material_bridge_microphysics_derived
- expansion_equation_derived
- a_of_tau_derived
- spectroscopic_redshift_forward_map_derived
- H_of_z_derived
- luminosity_distance_derived
- thermal_history_derived
- CMB_BBN_BAO_validated
- structure_growth_validated
- observational_discriminator_validated

**CROSSCHECK:** Derive pressure both by $-dE/dV$ and by the $a$-chain rule; derive the bulk modulus both from $-VdP/dV$ and $-(a/3)P'$; reconstruct energy from an arbitrary pressure; reconstruct pressure from an arbitrary $\kappa$; differentiate both reconstructions back; check the generic $n\ne3$ power branch, the separate $n=3$ formula, and their exact $n\to3$ agreement; compare the distinct $n=1$ and $n=2$ witnesses; and require wrong-volume, wrong-sign, missing-factor, wrong-measure, pressure-conflation, exponent-selection, dependency-hash, keyset, and physical-flag mutations to fail through the same validators used by the final gate.

**PROVENANCE:** Freeze the preregistration SHA-256 in the source; pin and verify the W3-40 result hash and checksum; require canonical UTF-8 LF text; record source hash, Python/SymPy/platform versions, UTC, closure flags, and upstream record; serialize with allow_nan disabled; write result and checksum atomically.

**FILES:** README.md, w3_41_foundation_constitutive_interface_preregistration.md, w3_41_foundation_constitutive_interface.py, w3_41_result.json, and w3_41_result.sha256.

## Decision semantics

If every exact check passes while every physical closure remains false, the status is PASS_EXACT_CONSTITUTIVE_INTERFACE__RECONSTRUCTION_DEGENERACY_PROVED__PHYSICAL_BRIDGE_AND_DYNAMICS_OPEN. This validates the interface and its nonselection result only.
