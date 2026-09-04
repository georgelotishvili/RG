# W3-69 Preregistration: Algebraic Material-Response Candidate Admissibility

> **Version 1.2 corrective refreeze.** Independent validation rejected the
> unaccepted v1.0 contract (SHA-256
> `284d082244d76b692d3648e923cf927df93c112577d93714ab8cb860ba28d86d`)
> because it replaced the pinned W3-64 Schwarzschild-corrected scalar-tail
> power by its flat-space value and did not recursively audit package and
> immutable-file cleanliness. Version 1.1 (SHA-256
> `3080353296f7350478f3c1aeb7c7b031298f1b9f5863c60f6b24b2e2f13a2443`)
> corrected those defects but omitted four tracked `intuitive/figures` assets
> from its immutable manifest. Version 1.2 adds the complete recursive
> intuitive-file manifest without changing the candidate action, mathematics,
> or physical-role decision. This text is frozen before the corrected verifier
> is rerun; neither earlier PASS artifact is accepted as evidence.

## Result stated in advance

W3-69 freezes and audits one economical matter-sector candidate while leaving
the W3-54 TEGR/Einstein--Hilbert operator, one coframe, and one operational
metric unchanged. The candidate promotes a positive factor
`p_A=exp(zeta/2)` to an algebraic auxiliary field coupled to the W3-58
ordinary complex scalar. It has a unique healthy algebraic branch and an exact
self-limiting marginal response. Its decisive test is whether `p_A` can be the
already frozen RefG operational factor `p_op`.

The answer is fixed by the exterior asymptotics. The actual W3-64 localized
branch is not compactly supported: `Psi_O~C exp(-kr) r^s`, with its pinned
Schwarzschild-corrected finite power `s`. The candidate therefore gives
`1-p_A=O(exp(-2kr)r^(2s))=o(1/r)`. The W3-51 positive-mass operational factor
instead has `1-p_op=O(1/r)`. Wherever an exact scalar-vacuum open set is
considered as a structural test, the candidate further forces `p_A=1` there.
Thus it cannot be the already frozen operational factor. Keeping the two
factors distinct removes the contradiction, but the auxiliary field then
eliminates exactly to a new nonpolynomial Q-ball potential and supplies no
independent foundation dynamics. This is a hard physical-role veto. The stage
stops before a global strong-field solve.

## Target and stopping rule

The target is one decision:

```text
unchanged TEGR/EH + W3-58 ordinary scalar
  -> freeze one algebraic positive-response action
  -> vary once and eliminate the auxiliary field exactly
  -> audit health, source counting, weak recovery and NEC
  -> compare the candidate factor with the frozen vacuum p dictionary
  -> accept or reject it as the RefG matter--foundation closure
  -> STOP.
```

Exactly three files belong to this package:

1. `w3_69_algebraic_material_response_candidate_preregistration.md`
2. `w3_69_algebraic_material_response_candidate.py`
3. `w3_69_result.json`

No global boson-star continuation, collapse evolution, horizon integration,
waveform, Love number, quasinormal spectrum, observation, Canon change, or
intuitive-manuscript edit belongs to this stage. A decisive role veto closes
the candidate without opening those calculations.

## Claim contract

### CLAIM_ID

`W3_69_ALGEBRAIC_MATERIAL_RESPONSE_CANDIDATE_ADMISSIBILITY`

### CLAIM

Use signature `(-+++)`, `X=Psi_O^* Psi_O>=0`, and the W3-58 potential

```text
U_58(X)=m_s^2 X-lambda X^2+(4 g_6/3)X^3,
a=g_6 m_s^2/lambda^2>3/16.
```

Freeze the candidate action

```text
S_69 = integral d^4x sqrt(-g) R/(16 pi G)
       - integral d^4x sqrt(-g)
         [g^mu_nu partial_mu Psi_O^* partial_nu Psi_O
          +exp(zeta) U_58(X)+(rho_star/2) zeta^2],

rho_star>0,                 p_A=exp(zeta/2)>0.
```

Then:

1. `a>3/16` makes `U_58(X)>0` for every `X>0` and `U_58(0)=0`.
2. The auxiliary equation
   `rho_star zeta+exp(zeta)U_58=0` has the unique real branch
   `zeta=-W_0(U_58/rho_star)<=0`.
3. Writing `w=W_0(U_58/rho_star)` gives

   ```text
   p_A^2=exp(-w) in (0,1],
   U_eff=rho_star(w+w^2/2),
   dU_eff/dU_58=p_A^2>0,
   d(p_A^2)/dU_58=-p_A^4/[rho_star(1+w)]<0.
   ```

   Thus the local marginal potential weight decreases monotonically with
   activation. This identity does not predetermine a global tail integral.
4. The algebraic Hessian is `rho_star(1+w)>0`; no propagating auxiliary mode,
   ghost, Ostrogradsky derivative, or new characteristic cone is present. The
   complex scalar retains its canonical principal symbol.
5. `U_eff=U_58-U_58^2/(2rho_star)+O(U_58^3)`. The vacuum Klein--Gordon Hessian
   and mass pole are unchanged. The gravitational field equation remains
   Einstein's equation with one minimally coupled Hilbert source, so the
   W3-52 standard GR 1PN/PPN vector is inherited and no long-range scalar fifth
   force is created.
6. The complete matter source is varied once from the displayed joint action.
   On the auxiliary equation its null contraction is
   `T_mu_nu k^mu k^nu=2|k^mu partial_mu Psi_O|^2>=0`. The W3-64
   NEC/Penrose boundary therefore remains unchanged.
7. On every structural-test open region with `Psi_O=0`, the candidate gives
   `U_58=0`, `zeta=0`, and `p_A=1`. The actual W3-64 localized branch has no
   finite-radius scalar-vacuum exterior; its pinned asymptotic field is
   `Psi_O~C exp(-kr) r^s`, where
   `s=-1+alpha M_infinity(2 Omega^2-1)/k` is finite and `k>0`. Hence
   `1-p_A=O(exp(-2kr)r^(2s))=o(1/r)`. By contrast, the W3-51 operational
   factor satisfies `1-p_op=O(1/r)` for positive mass. Therefore
   `p_A=p_op` fails on the actual asymptotic localized branch; the open-vacuum
   statement is retained only as a complementary structural test.
8. Renaming `p_A` as an internal suppression factor `s` avoids the dictionary
   contradiction. Because `zeta` is algebraically eliminable, that branch is
   exactly Einstein gravity plus the canonical complex scalar with the new
   potential `U_eff(X)`. It is a candidate self-interaction, not a derivation
   of the RefG operational factor or its foundation dynamics.
9. The finite-`rho_star` potential differs from W3-58 beginning at `X^2`, so
   the W3-58 finite-amplitude profile, existence proof, charge slope, and
   stability spectrum are not inherited. At large `X`,
   `U_eff~(rho_star/2) ln^2(U_58/rho_star)` and `U_eff/X->0`; a new Q-ball
   existence and stability gate would be required for the renamed toy branch.
10. `p_A>0` at finite `U_58` is a parametrization fact. Since `p_A->0` only as
    `U_58->infinity`, while `U_eff` also diverges, this fact supplies neither a
    density bound, a curvature bound, an infinite proper/affine distance, nor
    geodesic completeness.

The candidate is therefore mathematically healthy in its declared local
domain and rejected as the requested RefG matter--foundation `p` closure.

### TYPE

`EXACT_CANDIDATE_ACTION_VARIATION_HEALTH_AND_OPERATIONAL_DICTIONARY_AUDIT_WITH_HARD_ROLE_REJECTION`.

The Lambert-W elimination, derivative signs, Hessians, asymptotics, source
ledger, NEC identity, and exterior mismatch are exact in the declared class.
This is not a strong-field solution, singularity-resolution result, or
observational prediction.

### MODEL_VERSION

`W3-69-v1.2-ALGEBRAIC-MATERIAL-RESPONSE-CANDIDATE-AUDIT`.

A change to the action, auxiliary-field role, potential, stiffness sign,
Lambert branch, source ledger, operational-p definition, dependency hashes,
hard-veto semantics, or stopping rule creates a new model version.

### ASSUMPTIONS

1. Every dependency file has the exact SHA-256 hash listed below.
2. The active post-Genesis branch contains one W3-54 coframe and its one
   operational metric. The gravitational operator remains exactly TEGR/EH.
3. `Psi_O` and `U_58` use the W3-58 field and normalization; `a>3/16`,
   `m_s^2>0`, `lambda>0`, `g_6>0`, `X>=0`, and `rho_star>0`.
4. The candidate auxiliary field is varied before it is eliminated. It is not
   prescribed as an external spacetime profile.
5. W3-51 supplies `p_op=exp(-u)` only on its static weak exterior domain. No
   strong-field extrapolation of that formula is used.
6. The W3-58 localized tail is exponential and the asymptotically flat metric
   has the W3-64 Schwarzschild `1/r` exterior mass term.
7. The Penrose implication is used only under the global hypotheses registered
   by W3-64 and W3-67.
8. `rho_star` is a newly selected universal candidate density, not a fitted
   object parameter and not a foundation-derived value.
9. No archived theory, Work 2 file, observation, target compactness, desired
   core, or result-dependent parameter enters this audit.

### DOMAIN

The algebraic calculation covers the principal real Lambert branch for
`U_58/rho_star>=0`. The weak comparison covers the common static,
asymptotically flat, positive-mass exterior of W3-51 and W3-64. The source and
health statements cover regular configurations of the displayed local action.
The theorem handoff applies only when every registered Penrose hypothesis
holds.

The audit makes no claim for a solved finite-amplitude Q-ball of `U_eff`, a
dynamical horizon, a rotating configuration, collapse, or a complete spacetime.

### CONVENTIONS

- `p_op` is the unique frozen operational clock/ruler factor read from the
  RefG coframe/metric dictionary.
- `p_A=exp(zeta/2)` is the candidate auxiliary factor tested for that role.
- If the operational identification fails, `s=exp(zeta/2)` denotes only the
  renamed internal suppression factor of the equivalent toy potential.
- `W_0` is the principal real Lambert function on `[0,infinity)`.
- `T_mu_nu=-(2/sqrt(-g)) delta S_m/delta g^mu_nu` and every source term is
  counted once.
- `k^mu` is an arbitrary metric-null vector.
- `p_A->0` denotes a field-space limit, not a spacetime boundary proof.

### FREEDOM_LEDGER

- Existing measured `G` and W3-58 coefficients `(m_s,lambda,g_6)`: inherited.
- `rho_star`: one new positive universal density scale; selected for the
  candidate class, not derived or fitted.
- Object-specific couplings, response functions, switches, profiles, target
  radii, compactness values, and observational parameters: zero.
- New propagating fields, second metrics, higher-curvature operators, and
  duplicate sources: zero.
- Identification `p_A=p_op`: tested, not assumed, and rejected by the exterior
  gate.

### DEPENDENCIES

| Role | File | SHA-256 |
|---|---|---|
| Static operational `p_op` dictionary | `Lagrangian_Formulation/Weak_Field_Closure/w3_51_weak_field_closure_contract.md` | `86bc2ed86cddee36bec5e46fdfa407701107290c783bfa81ba1440b96becc7cf` |
| Generated W3-51 result | `Lagrangian_Formulation/Weak_Field_Closure/w3_51_result.json` | `a74e0f02c5a5c794723a5797049bd28d95684a95be869db30f10a575d3ee9cf8` |
| Full standard 1PN inheritance | `Lagrangian_Formulation/Full_1PN_Inheritance/w3_52_full_1pn_inheritance_contract.md` | `66a33a82d29bd65fabc37b6e55f29a64674f0e44f5a4c0893611c261d00792b6` |
| Generated W3-52 result | `Lagrangian_Formulation/Full_1PN_Inheritance/w3_52_result.json` | `8ae2d80cbc983e29a7ccc9ef4e3f6685b36cb4e6ade06e6d2a494fd9f46e11e2` |
| One-coframe TEGR/EH and source ledger | `Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md` | `6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879` |
| Generated W3-54 result | `Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_result.json` | `ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991` |
| W3-58 ordinary complex scalar | `Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_one_oscillon_coframe_localized_core_preregistration.md` | `ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db` |
| Generated W3-58 result | `Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_result.json` | `cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5` |
| Einstein--scalar strong-field and Penrose boundary | `Strong_Field/W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field_preregistration.md` | `25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1` |
| Generated W3-64 result | `Strong_Field/W3-64_Einstein_Continuation/w3_64_result.json` | `b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b` |
| Strong-field response boundary | `Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_foundation_strong_field_response_preregistration.md` | `31e6520d9b7917413b9f2978291b4a77f067abe8dd3d6a9e89e1b2cfb699da11` |
| Generated W3-67 result | `Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_result.json` | `659bdfe171a8279b465fdd49eaf590755da22a7522a83053a4a06450fd745385` |
| Rejected gravitational-operator candidate | `Strong_Field/W3-68_Born_Infeld_Candidate_Admissibility/w3_68_born_infeld_candidate_admissibility_preregistration.md` | `afd38da6bd297e6ed029936d9a1162ea7da85377935adf06cb5326edade53f5e` |
| Generated W3-68 result | `Strong_Field/W3-68_Born_Infeld_Candidate_Admissibility/w3_68_result.json` | `fbe366a7bf20119f460ff461125d17ebb0a1ebe220d3de6d7c38e4627729c5ec` |

The following repository files are immutable controls for this stage rather
than scientific inputs:

| Control | Repository path | SHA-256 |
|---|---|---|
| Rules | `CODES.md` | `27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41` |
| Dictionary | `intuitive/Dictionary.txt` | `f6e12b67f38e49bb547d37e6c92375a2ee5b2f596ed481a866cbc490be32ed0b` |
| Figure 3 PDF | `intuitive/figures/figure_3.pdf` | `d3fc89edf7ed59b499467999c16504c8cc36dbe614f9b1dcc612caaee1f35f5f` |
| Figure 3 PNG | `intuitive/figures/figure_3_v2.png` | `43e673eeac9d44cb595303bf55d0622ac2fcb87b641627ff8e3a5e8781365a4e` |
| Logo PDF | `intuitive/figures/logo.pdf` | `e585eaa93b8d60b6294fcd3e7448469265502defd7725f74fdb0a56d33d907ab` |
| SPARC validation figure | `intuitive/figures/sparc_rar_real_validation.png` | `1afefcc99ca6223230959b8ab3a6cfc015035de20178b7eed8f7f3728a7fe3f0` |
| Private idea ledger | `intuitive/idea.txt` | `98cf98f70e3ac146ef3b106cdd6b2df6c6861d2c277e9c9adae5262959d2dd8d` |
| English bibliography | `intuitive/RefG_EN.bib` | `78a2889e8da0eb206d6282dac610a82af77ad1340e48c7dbd2e042e1f317fe43` |
| English PDF | `intuitive/RefG_EN.pdf` | `2d1c65687fb6c9bbb5c3004299d6205ad494f361a956d646851571996a448ddc` |
| English source | `intuitive/RefG_EN.tex` | `6e69d616229688d885320d9b26b8c4637c563ae47f8da006feee8548d6ad910e` |
| Georgian monograph | `intuitive/RefG_GE.md` | `433d3ac96ff6d91eaae1da60cd3f27f84ead2b7bddea26885034e2995dd8787f` |

The verifier must hash-check this exact manifest. It must also recurse through
the W3-69 directory and reject any file or directory beyond the three declared
package artifacts; a top-level-only file count is insufficient.

All paths resolve inside the active `RefG/work 3` tree. No archived theory is
an admissible dependency.

### METHOD

1. Verify dependency hashes and required upstream statuses and scope flags.
2. Prove global positivity of `U_58` from the quadratic discriminant of
   `U_58/X` for `a>3/16`.
3. Vary `zeta`, prove strict monotonicity of its equation, and solve its unique
   real branch with `W_0`.
4. Eliminate `zeta`; verify `U_eff`, its first two response derivatives, the
   weak series, and the large-field limit.
5. Audit the algebraic Hessian, degree-of-freedom count, complex-scalar
   principal symbol, vacuum Hessian, and unchanged EH/TEGR operator.
6. Derive the Hilbert source once, its on-shell conservation identity, and the
   null contraction.
7. Regress the W3-52 PPN vector and show that the candidate creates no exterior
   propagating scalar charge.
8. Compare `p_A` and `p_op` first as a structural exact-vacuum test and then,
   decisively, on the actual W3-64 Schwarzschild-corrected exponential tail.
9. Prove exact equivalence of the renamed auxiliary branch to `U_eff(X)` and
   register which W3-58 finite-amplitude results cease to be inherited.
10. Separate finite-field positivity of `p_A` from density, curvature,
    proper/affine-distance, and geodesic-completeness claims.
11. Import the W3-64/W3-67 NEC/Penrose boundary and apply it to the candidate.
12. Run all negative mutations through the same validators, require a clean
    three-file package, write strict finite JSON, and stop.

G0_GOAL through G6_PHYSICAL_MATCH are required. G7_OBSERVATION and G8_EXPORT
are exact N/A gates because the candidate is rejected before either stage.

### PASS_CONDITION

PASS means the audit is complete, not that the candidate is accepted. Every
dependency, algebraic, variation, health, source, weak-limit, asymptotic,
dictionary, equivalence, NEC, theorem-boundary, mutation, and package gate
passes; the candidate mathematical-health flag is true; the operational-role
admissibility flag is false; the hard role veto is triggered; and no global
strong-field solve or physical prediction is opened.

### FAIL_CONDITION

FAIL occurs if a dependency or exact identity fails; if a second metric,
gravitational modification, propagating late-onset mode, duplicate source,
external `p_A` profile, fitted `rho_star`, or hand-selected object profile is
introduced; if `p_A` is silently equated with `p_op`; if W3-58 finite-amplitude
stability is inherited after changing its potential; if local positivity is
promoted to a singularity-resolution theorem; if NEC is reported as violated;
or if a global solve is opened after the decisive candidate veto.

### FALSIFIER

The exterior mismatch is falsified if the displayed local candidate action,
without a metric-dependent, nonlocal, or new dynamical premise, produces on
the pinned W3-64 localized branch a candidate response with a nonzero
Schwarzschild-order `1/r` coefficient equal to that of
`p_op=exp[-GM/(c0^2 r)+...]`. The auxiliary-potential equivalence is falsified
if eliminating the unique algebraic branch changes the classical
Euler--Lagrange system. Either counterexample must stay inside the frozen
action and domain.

### RESIDUAL

Exact symbolic zero is required for the auxiliary variation, elimination,
derivative identities, weak coefficients, Hessian, source/NEC contraction,
vacuum value, asymptotic order registry, and mutation validators. Dependency
hash and upstream-status checks are exact Boolean gates.

### ERROR_BOUND

Zero for all algebraic identities and hashes. No floating-point compact-object
solution or observational estimate is used. Series are formal local or
asymptotic identities with their omitted orders recorded explicitly.

### VALIDITY_HEALTH

The frozen candidate has a positive algebraic Hessian, no added propagating
degree of freedom, a canonical hyperbolic complex-scalar principal symbol, an
unchanged vacuum mass pole, one metric, and a once-counted conserved source.
These facts establish local mathematical health. They do not repair the
operational-role mismatch, restore W3-58 finite-amplitude stability, cap the
source, or prove a regular spacetime.

### BRANCHES

- `ALGEBRAIC_P_A_CANDIDATE`: mathematically healthy, rejected as `p_op`.
- `RENAMED_INTERNAL_S_TOY`: exactly Einstein plus canonical `Psi_O` with
  `U_eff`; admissible only as a separate future potential test.
- `FROZEN_OPERATIONAL_P_OP`: remains the metric/coframe readout of W3-51/52.
- `CURRENT_NEC_PENROSE_BOUNDARY`: unchanged.
- `GLOBAL_STRONG_FIELD_SOLVE`: not opened.

### OBSERVABLE_MAP

No new observable is produced. The audit distinguishes the candidate's
W3-64-pinned exponentially suppressed, Schwarzschild-power-corrected response
from the frozen `1/r` operational response. No telescope or detector quantity
is predicted.

### FORWARD_MODEL

N/A. A global solution or likelihood cannot repair a local exterior identity
mismatch in the frozen candidate action.

### DATA_ROLE

`NO_DATA_READ_OR_FITTED`. Published theorem handoffs and upstream formal
artifacts are logical inputs, not fit data.

### IDENTIFIABILITY

The action identifies the unique algebraic branch for every positive
`rho_star`, but the active RefG core does not determine `rho_star`. More
importantly, the action identifies an internal potential suppression factor,
not the already frozen exterior operational factor. Reinterpreting the field
changes its physical role and leaves the original matter--foundation bridge
unidentified.

### BENCHMARK

Use the exact W3-58 class `a>3/16` and its canonical point `a=1/4` only as an
algebraic regression. Required witnesses are:

```text
U_58/X=m_s^2[1-y+(4a/3)y^2],  y=lambda X/m_s^2,
discriminant=1-16a/3<0,
p_A(X=0)=1,
p_op(r)=exp[-GM/(c0^2 r)+...]<1 for finite r and M>0,
Psi_O~C exp(-kr)r^s,
1-p_A=O(exp(-2kr)r^(2s))=o(1/r),
1-p_op=O(1/r),
T_kk=2|k.partial Psi_O|^2>=0.
```

No numerical value of `rho_star` is selected.

### CLOSURE_FLAGS

All flags start false.

Required true:

- `g0_goal_pass`
- `g1_conventions_pass`
- `g2_core_algebra_pass`
- `g3_structure_and_health_pass`
- `g4_independent_check_pass`
- `g5_limits_regression_pass`
- `g6_physical_match_and_role_decision_pass`
- `g7_observation_not_applicable_exact`
- `g8_export_not_applicable_exact`
- `dependency_hashes_exact`
- `immutable_control_hashes_exact`
- `upstream_status_and_scope_exact`
- `candidate_action_registered_exact`
- `u58_global_positivity_exact`
- `auxiliary_euler_equation_exact`
- `unique_principal_lambert_branch_exact`
- `finite_field_p_A_positive_exact`
- `effective_potential_elimination_exact`
- `marginal_response_feedback_sign_exact`
- `algebraic_hessian_positive_exact`
- `no_new_propagating_mode_exact`
- `canonical_principal_symbol_preserved_exact`
- `vacuum_kg_hessian_and_mass_pole_preserved_exact`
- `tegr_eh_operator_unchanged_exact`
- `full_standard_1pn_ppn_regression_exact`
- `one_metric_once_counted_hilbert_source_exact`
- `total_source_conservation_registered_exact`
- `candidate_nec_exact`
- `candidate_vacuum_p_A_unity_exact`
- `w3_51_positive_mass_exterior_p_op_nontrivial_exact`
- `w3_64_exponential_tail_vs_schwarzschild_order_mismatch_exact`
- `p_A_equals_p_op_rejected_exact`
- `renamed_s_exactly_potential_redefinition_exact`
- `rho_star_foundation_selection_open_exact`
- `w3_58_finite_amplitude_results_not_inherited_exact`
- `large_field_subquadratic_ratio_exact`
- `finite_field_p_positivity_not_singularity_resolution_exact`
- `penrose_boundary_inherited_exact`
- `candidate_mathematical_health_pass`
- `hard_operational_role_veto_triggered_exact`
- `candidate_rejected_as_refg_p_closure_exact`
- `global_strong_field_solve_stop_rule_enforced`
- `mutation_controls_pass`
- `package_clean_pass`
- `aggregate_audit_pass`

Required false:

- `candidate_operational_role_admissibility_pass`
- `p_A_equals_p_op_derived`
- `algebraic_candidate_foundation_derived`
- `rho_star_from_foundation_derived`
- `rho_star_observationally_fitted`
- `w3_58_finite_amplitude_solution_inherited`
- `w3_58_stability_spectrum_inherited`
- `foundation_strong_field_response_derived`
- `global_tail_weakening_solution_derived`
- `density_upper_bound_derived`
- `curvature_upper_bound_derived`
- `p_zero_infinite_proper_or_affine_distance_derived`
- `trapped_surface_derived`
- `regular_black_hole_solution_derived`
- `geodesic_completeness_derived`
- `singularity_resolution_completed`
- `new_strong_field_prediction_derived`
- `observational_forward_model_built`
- `observational_likelihood_evaluated`
- `canon_changed`
- `intuitive_files_changed`

### CROSSCHECK

The verifier obtains the branch both by direct substitution and by the inverse
Lambert identity; obtains response derivatives both before and after
elimination; compares the candidate vacuum equation with the W3-51 exterior
registry; derives the squared W3-64 Schwarzschild-corrected exponential-tail
order independently and proves that it is `o(1/r)`; checks the source null
contraction before and after
auxiliary elimination; validates the imported PPN vector and Penrose flags;
and applies negative controls for a wrong Lambert sign, a nonpositive
stiffness, a fabricated propagating mode, a duplicate source, a false exterior
identification, inherited W3-58 stability, a false NEC violation, a finite-p
singularity-resolution promotion, and an illicit global-solve flag.

### PROVENANCE

The verifier pins every dependency and this preregistration by SHA-256. It
records source/preregistration hashes, Python, SymPy, platform, UTC,
deterministic execution, `network_used_by_verifier=false`, and
`archived_theory_used=false`. It writes strict finite UTF-8 JSON through an
atomic replacement.

### FILES

- `w3_69_algebraic_material_response_candidate_preregistration.md`
- `w3_69_algebraic_material_response_candidate.py`
- generated `w3_69_result.json`

No intuitive file is changed by this stage.

## Decision semantics

Passing W3-69 means that the selected algebraic candidate has been completely
audited and rejected at its first decisive physical-role gate. It does not
mean that the candidate is accepted as RefG dynamics.

The passing status is:

`PASS_EXACT_ALGEBRAIC_RESPONSE_ACTION_AND_HEALTH_AUDIT__REJECTED_AS_REFG_OPERATIONAL_P_BY_EXTERIOR_DICTIONARY_MISMATCH_AND_POTENTIAL_REDEFINITION__GLOBAL_STRONG_FIELD_SOLVE_NOT_OPENED`
