# W3-68 Preregistration: Born--Infeld f(T) Candidate Admissibility

## Result stated in advance

W3-68 tests one fully specified nonlinear gravitational action and stops at
the first decisive health gate. The candidate is the covariant teleparallel
Born--Infeld function

```text
f_BI(T) = Lambda_* [1-sqrt(1-2T/Lambda_*)],     Lambda_*>0,
```

inserted into the W3-54 gravitational coframe conventions on the exact
localized W3-64 source branch: `Lambda_F=0`, the ordinary complex-scalar
action `S_O[g,chi,theta_O]` is counted once, and the homogeneous collective
phase source `S_C` is absent locally.
This is a `NEWLY_SELECTED_UNIVERSAL_CANDIDATE_ACTION`: RefG does not derive it,
and the present inputs do not select it uniquely.

The candidate has an exact TEGR weak limit. Since torsion is first order in a
weak coframe perturbation while the torsion scalar is quadratic,
`T=O(epsilon^2)`, the first Born--Infeld correction to the action is
`O(epsilon^4)`. Its quadratic weak kinetic operator is therefore exactly the
TEGR operator and its field-equation correction begins at
`O(epsilon^3)`. This protects the frozen W3-52 1PN/PPN result on the analytic
weak branch.

The same property triggers the decisive veto. For finite `Lambda_*`,
`f_TT` is nonzero, so the nonlinear theory belongs to the non-TEGR `f(T)`
sector. Primary analyses find additional, background-dependent nonlinear
mode/constraint structure and an explicit mode first appearing at fourth
perturbative order around the trivial Minkowski tetrad. That sector has no
quadratic kinetic operator on the weak branch. W3-68 requires every nonlinear
physical mode to possess a nondegenerate, hyperbolic weak-branch kinetic
operator, or a derived cutoff demonstrating that its apparent strong-coupling
scale lies outside the theory's domain. The frozen one-parameter action
supplies neither. The health gate therefore fails and this Born--Infeld
candidate is rejected before any global black-hole solve.

An EFT analysis can soften this warning when a derived cutoff and complete
interaction hierarchy place the late-onset sector outside the domain of use.
That caveat is part of the decision: it does not rescue the frozen candidate,
because this one-parameter action supplies no such cutoff or completion.

Covariantizing the theory with the inertial spin connection is required and
removes frame-choice ambiguity. It does not by itself convert nonlinear
`f(T)` dynamics into TEGR or close the extra-mode health gate. No precise
nonlinear degree-of-freedom count is claimed here.

## Target, new input, and stopping rule

The stage asks one question:

```text
new universal Born--Infeld f(T) candidate
    -> exact action/domain/derivative audit
    -> W3-54 covariance plus W3-64 localized source-ledger audit
    -> W3-52 weak/1PN regression
    -> nonlinear-mode weak-branch health gate
    -> ACCEPT or REJECT
    -> STOP.
```

The new physical input that makes W3-68 distinct from W3-67 is the explicit
universal function `f_BI(T)` and its single universal scale `Lambda_*`.

The minimum result is a hard admissibility decision before solving a compact
object. The stopping condition is met as soon as a required mathematical
health gate fails. Static or dynamical black-hole integration, horizon or core
construction, waveform generation, observation fitting, alternative-action
searches, parameter scans, and intuitive-manuscript edits are outside this
stage.

The eventual package contains exactly three files:

1. `w3_68_born_infeld_candidate_admissibility_preregistration.md`
2. `w3_68_born_infeld_candidate_admissibility.py`
3. generated `w3_68_result.json`

## Frozen candidate action

On a regular connected post-Genesis patch, use the W3-54 coframe
`e^A_mu`, metric `g_mu_nu=eta_AB e^A_mu e^B_nu`, positive determinant
`e=det(e^A_mu)`, and flat metric-compatible inertial connection
`omega^A_Bmu`, with

```text
R^A_Bmu_nu(omega)=0,
omega=Lambda^(-1)dLambda
```

on its inertial orbit. The torsion scalar is the W3-54 TEGR combination

```text
T = T_TEGR = (1/4)I1+(1/2)I2-I3.
```

The candidate action is

```text
S_68[e,omega,Psi]
  = -K_F integral d^4x e f_BI(T_TEGR)
    + S_O[g,chi,theta_O],

K_F = c0^3/(16 pi G),
f_BI(T) = Lambda_* [1-sqrt(1-2T/Lambda_*)],
Lambda_*>0,
Lambda_F=0.
```

The one localized source action is frozen exactly as

```text
S_O = -integral d^4x sqrt(-g) [
        (1/2) g^munu partial_mu chi partial_nu chi
      + (1/2) chi^2 g^munu partial_mu theta_O partial_nu theta_O
      + V(chi)],

V(chi) = (m_s^2/2) chi^2 - (lambda/4) chi^4 + (g_6/6) chi^6.
```

Its Hilbert tensor `T_O` is counted once. The homogeneous collective source
`T_C` is not re-added on this localized branch. `P_F`, the material response
`p`, metric self-energy, and any pressure-deficit readout are not added as
separate Hilbert sources.

The principal real square root fixes the action domain

```text
1-2T/Lambda_* > 0,       equivalently T < Lambda_*/2.
```

The boundary `T=Lambda_*/2`, where the derivatives diverge, is excluded. The
analytic TEGR expansion uses `|2T/Lambda_*|<1`.

## Claim contract

### CLAIM_ID

`W3_68_BORN_INFELD_FT_CANDIDATE_ADMISSIBILITY`

### CLAIM

For the frozen one-coframe, one-metric, covariant Born--Infeld `f(T)` action:

1. On the principal real branch,

   ```text
   f_BI(T)
     = T + T^2/(2 Lambda_*) + T^3/(2 Lambda_*^2)
       + 5T^4/(8 Lambda_*^3) + O(T^5/Lambda_*^4),

   f_T  = (1-2T/Lambda_*)^(-1/2),
   f_TT = Lambda_*^(-1)(1-2T/Lambda_*)^(-3/2).
   ```

   Hence `f(0)=0`, `f_T(0)=1`, and `f_TT(0)=1/Lambda_*>0`.
2. For `e^A_mu=delta^A_mu+epsilon h^A_mu+O(epsilon^2)`, torsion is
   `O(epsilon)` and `T_TEGR=O(epsilon^2)`. The candidate's first departure
   from TEGR is `T^2/(2Lambda_*)=O(epsilon^4)`. Its quadratic action and
   linearized field equations are exactly TEGR; the nonlinear correction to
   the Euler--Lagrange equations starts at `O(epsilon^3)` at fixed finite
   `Lambda_*` and fixed derivative scale.
3. On the analytic weak domain `|T|/Lambda_* << 1`, this cubic field-equation
   onset lies beyond every retained W3-52 1PN component order. The complete
   standard W3-52 PPN vector, including `beta=gamma=1`, is therefore inherited
   through its registered order. This is an order regression, not an all-order
   equivalence and not a uniform statement as `Lambda_* -> 0`.
4. The candidate is genuinely nonlinear: `f_TT` is nonzero everywhere in its
   open real domain. It is not related to TEGR by the W3-54 boundary identity,
   because a boundary term inside a nonlinear function does not remain a
   boundary term.
5. The covariant coframe-plus-inertial-spin-connection formulation is used.
   This ensures frame-independent equations when the tetrad and its compatible
   inertial connection are varied consistently. The nonlinear primary-
   constraint structure remains distinct from TEGR; covariance alone does not
   supply a healthy kinetic operator for modes absent from the quadratic
   action.
6. Published nonlinear analyses establish that non-TEGR `f(T)` theories have
   additional/background-dependent mode or constraint structure; a direct
   Minkowski perturbation analysis exhibits a new mode at fourth order around
   the trivial tetrad. W3-68 imports only the existence/late-onset health
   implication, not a universal exact count of degrees of freedom.
7. The frozen health condition requires the complete nonlinear physical
   sector to have a nondegenerate quadratic kinetic operator on the same weak
   branch used for the 1PN inheritance, or a derived EFT cutoff and interaction
   analysis that proves every late-onset mode remains above the domain of use.
   The action fails this condition: the additional nonlinear sector is absent
   from the quadratic TEGR Hessian and no independent cutoff or kinetic
   completion is present.
8. The candidate is therefore `REJECTED` by a mathematical health veto before
   a global solution is attempted. The rejection applies to this selected
   Born--Infeld `f(T)` candidate, not to RefG and not to every possible
   covariant strong-field completion.

### TYPE

`EXACT_CANDIDATE_ACTION_AUDIT_WITH_THEOREM_HANDOFF_AND_HARD_HEALTH_REJECTION`.

The function identities, domain, perturbative order, source ledger, and weak
regression are exact in their declared domains. The nonlinear mode and
constraint statement is a pinned primary-literature handoff. The candidate is
not `MECHANISM_DERIVED`, is not a RefG prediction, and produces no black-hole
or singularity-resolution result.

### MODEL_VERSION

`W3-68-v1.0-COVARIANT-BORN-INFELD-FT-ADMISSIBILITY`.

A change to `f_BI`, the sign or domain of `Lambda_*`, the square-root branch,
the spin-connection treatment, source ledger, weak-order counting, health
criterion, or theorem handoff creates a new model version.

### ASSUMPTIONS

1. Every local dependency has the exact SHA-256 hash listed below.
2. W3-54 supplies one coframe, one metric, the flat inertial connection orbit,
   the TEGR scalar and sign convention, and `K_F`; it is a geometry and
   convention dependency here, not the localized matter-source selector.
3. W3-52 supplies the frozen full standard 1PN/PPN component and remainder
   contract.
4. W3-64 supplies the exact localized ordinary complex-scalar action `S_O`
   counted once, with `Lambda_F=0` and the homogeneous collective phase source
   not re-added locally.
5. W3-67 supplies the exact requirement that an active response enter the
   covariant master action and pass degrees-of-freedom, hyperbolicity,
   stability, causality, conservation, and strong-coupling gates.
6. `Lambda_*>0` is one finite universal constant independent of object,
   environment, and data. Its value is not fitted or inferred in this stage.
7. The principal real square-root branch is used and the boundary
   `T=Lambda_*/2` is excluded.
8. The weak expansion holds at fixed derivative scale with
   `|T|/Lambda_* <<1`; `epsilon` counts coframe-perturbation amplitude.
9. The covariant formulation uses the tetrad/coframe and compatible flat
   inertial spin connection together. A pure-tetrad arbitrary-frame shortcut
   is excluded.
10. The cited mode/constraint analyses are used only for the scoped statement
   that nonlinear `f(T)` contains late-onset/background-dependent structure
   not represented by the TEGR quadratic Hessian. No exact universal count is
   assumed.
11. No black-hole metric, regular core, desired curvature bound, observed
    waveform, fitted threshold, or archived theory file enters the candidate
    selection or decision.

### DOMAIN

The algebra applies on regular coframes with `e>0`, a compatible flat inertial
spin connection, and the principal real domain `T<Lambda_*/2`. The Taylor and
1PN regression further require `|2T/Lambda_*|<1` and weak coframe amplitude.
The hard health test is evaluated on the trivial Minkowski coframe and its
connected weak branch.

The stage has no claim at the square-root boundary, on another square-root
sheet, for degenerate coframes, at a solved horizon, in a rotating spacetime,
or in a completed ultraviolet theory.

### CONVENTIONS

- Metric, torsion, and action signs are those of W3-54.
- `T` means the W3-54 `T_TEGR`, with dimension `L^(-2)`.
- `Lambda_*` is a positive universal Born--Infeld scale with dimension
  `L^(-2)`; the localized branch fixes the distinct vacuum slot `Lambda_F=0`.
- `K_F=c0^3/(16piG)`.
- `f_T=df/dT` and `f_TT=d^2f/dT^2`.
- The square root is the positive principal real root.
- `epsilon` is a formal weak coframe-amplitude parameter; it is not a fitted
  coupling.
- The flat inertial connection obeys `R(omega)=0` and remains on its allowed
  inertial orbit under variation.
- The localized Hilbert source is `T_O` from the exact W3-64 `S_O`, counted
  once; the local count of the homogeneous collective source `T_C` is zero.
- `REJECTED` denotes this candidate-action decision under the frozen hard
  health gate.

### FREEDOM_LEDGER

- `Lambda_*`: one positive, finite, universal dimensional parameter;
  newly selected but numerically unspecified; effective dimension 1.
- square-root sheet: principal real branch; fixed; no freedom.
- function `f_BI`: fixed exactly; no functional freedom.
- coframe and inertial connection: dynamical/gauge variables inherited from
  W3-54; no object-specific rule.
- source fields and source parameters: the exact W3-64 localized ordinary
  complex scalar, inherited unchanged and counted once; local `S_C` count zero.
- strong-coupling cutoff/completion: absent; zero inserted parameters; health
  requirement unresolved and therefore failed.
- object-specific parameters: zero.
- data-fit parameters and priors: zero.

### DEPENDENCIES

| Physical role | File | SHA-256 |
|---|---|---|
| Full standard 1PN/PPN inheritance and componentwise remainder contract | `Lagrangian_Formulation/Full_1PN_Inheritance/w3_52_full_1pn_inheritance_contract.md` | `66a33a82d29bd65fabc37b6e55f29a64674f0e44f5a4c0893611c261d00792b6` |
| Generated W3-52 closure record | `Lagrangian_Formulation/Full_1PN_Inheritance/w3_52_result.json` | `8ae2d80cbc983e29a7ccc9ef4e3f6685b36cb4e6ade06e6d2a494fd9f46e11e2` |
| One-coframe TEGR action, flat inertial connection, and once-only source ledger | `Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md` | `6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879` |
| Generated W3-54 closure record | `Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_result.json` | `ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991` |
| Localized ordinary-scalar strong-field branch and once-only local source ledger | `Strong_Field/W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field_preregistration.md` | `25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1` |
| Generated W3-64 closure record | `Strong_Field/W3-64_Einstein_Continuation/w3_64_result.json` | `b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b` |
| Active-response action boundary and health requirements | `Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_foundation_strong_field_response_preregistration.md` | `31e6520d9b7917413b9f2978291b4a77f067abe8dd3d6a9e89e1b2cfb699da11` |
| Generated W3-67 closure record | `Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_result.json` | `659bdfe171a8279b465fdd49eaf590755da22a7522a83053a4a06450fd745385` |

All paths are resolved inside the active `RefG/work 3` tree. No archived or
older-theory directory is an admissible dependency.

### METHOD

The selected method is exact symbolic differentiation and series algebra,
hash-pinned upstream regression, source-ledger validation, and a primary-
literature theorem handoff for the nonlinear health boundary.

1. Verify dependency hashes and required upstream statuses.
2. Register the exact covariant action and one-source ledger.
3. Differentiate `f_BI` independently and verify `f_T` and `f_TT`.
4. Expand about `T=0`, verify all displayed coefficients, and check the real
   domain and excluded derivative singularity.
5. Substitute `T=epsilon^2 tau_2+O(epsilon^3)` and verify that the first
   action correction is fourth order and its Euler--Lagrange correction begins
   at cubic weak amplitude.
6. Import and validate the complete W3-52 PPN vector and componentwise omitted
   orders; require the candidate correction to start beyond the retained 1PN
   orders on the analytic weak branch.
7. Verify `f_TT!=0` for every finite `Lambda_*` in the open real domain.
8. Register the covariant spin-connection requirement and reject the
   pure-tetrad arbitrary-frame mutation.
9. Import the scoped nonlinear mode/constraint and fourth-order-mode results
   from the cited primary sources without assigning a disputed exact count.
10. Apply the preregistered health criterion. The missing quadratic kinetic
    term for a nonlinear physical sector triggers rejection.
11. Stop before any global field-equation integration.

Universal gate declaration:

- `G0_GOAL`, `G1_CONVENTIONS`, and `G2_CORE_ALGEBRA` are required and must
  pass.
- `G3_STRUCTURE` is a required audit gate. Its audit-level `pass` is true only
  when the preregistered candidate health veto is detected exactly; the nested
  `candidate_structure_health_pass` remains false.
- `G4_INDEPENDENT_CHECK`, `G5_LIMITS_REGRESSION`, and `G6_PHYSICAL_MATCH` are
  required to establish that the rejection is not an algebra, limit, frame,
  or source-count artifact.
- `G7_OBSERVATION` is `N/A`: the candidate is rejected before producing an
  admissible observable model.
- `G8_EXPORT` is `N/A`: this internal candidate test changes neither Canon nor
  the intuitive manuscripts.

### PASS_CONDITION

The W3-68 audit passes only if dependency integrity, action registration,
exact derivatives, Taylor coefficients, real-domain checks, weak-order
counting, complete W3-52 regression, covariant spin-connection registry,
once-counted source ledger, scoped primary-source handoffs, mutations, and
package checks all pass; every required audit-gate `pass` must be true, while
the hard health validator detects the
quadratic/nonlinear mode mismatch and assigns `REJECTED` to this candidate.

An `ACCEPTED` candidate is impossible under this frozen v1.0 contract unless
the same action supplies a nondegenerate quadratic kinetic operator for every
nonlinear physical mode or a derived and independently verified cutoff that
places the late-onset sector outside the declared domain. Adding such a
completion changes the model version.

### FAIL_CONDITION

The audit fails if any dependency, derivative, series coefficient, domain,
weak-order, 1PN, covariance, source-ledger, theorem-scope, mutation, or package
check fails; if `Lambda_*` is fitted to a desired core; if the singular
square-root boundary is admitted as regular; if a pure-tetrad frame choice is
called covariant; if a precise universal mode count is claimed; if absence
from the quadratic action is called proof that the nonlinear mode does not
exist; if a black-hole solution is imported as a health proof; or if the
candidate is promoted after the hard health veto.

### FALSIFIER

For the candidate-admissibility claim, a derivation from this exact frozen
action showing that every nonlinear physical mode has a nondegenerate,
hyperbolic weak-branch quadratic kinetic operator would falsify the health
rejection. A derived EFT cutoff plus complete interaction analysis proving
that each late-onset mode remains outside the action's domain would also
falsify it and require a new version.

An exact counterexample to any displayed algebraic identity under the frozen
domain falsifies that atomic gate. A healthy different strong-field action
does not falsify this result; it defines another candidate.

### RESIDUAL

Exact symbolic zero is required for the function value, first and second
derivatives, Taylor coefficients, weak-order substitution, TEGR quadratic
Hessian regression, and source count. The nonlinear-mode result is a
hash/identifier-pinned analytic handoff and is not represented as a newly
computed field-theory residual.

### ERROR_BOUND

Zero for symbolic identities, integer order counting, hashes, and Boolean
source registries. No floating-point solve, likelihood, or observational
estimate is used. The primary-literature handoff carries scope uncertainty in
the exact nonlinear degree-of-freedom count; W3-68 avoids that count and uses
only the shared late-onset-sector conclusion required by the health gate.

### VALIDITY_HEALTH

The action is local, diffeomorphism covariant, one-coframe, one-metric, and
second order in field equations in the covariant teleparallel formulation.
Its square-root domain and derivative singularity are explicit. The TEGR
quadratic sector is healthy and preserves the weak limit. The full nonlinear
candidate fails the required perturbative-health/strong-coupling gate because
its additional late-onset sector lacks a quadratic weak-branch kinetic
operator and the frozen action supplies no derived cutoff completion.

### BRANCHES

- `TEGR_LIMIT`: `Lambda_* -> infinity` at fixed `T`; recovers W3-54 but removes
  the proposed strong-field modification.
- `ANALYTIC_WEAK_BRANCH`: `|2T/Lambda_*|<1`; exact TEGR quadratic action and
  inherited 1PN/PPN result.
- `FINITE_NONLINEAR_FT_BRANCH`: finite `Lambda_*`, `f_TT!=0`; fails the hard
  weak-branch health gate.
- `SQUARE_ROOT_BOUNDARY`: `T=Lambda_*/2`; excluded because `f_T` and `f_TT`
  diverge.
- `OTHER_SQUARE_ROOT_SHEET`: outside the frozen model.
- `PURE_TETRAD_ARBITRARY_FRAME`: rejected covariance mutation.
- `REGULAR_BLACK_HOLE_SOLUTION`: not opened because the candidate is rejected
  first.

### OBSERVABLE_MAP

The admissible map stops at the inherited W3-52 weak observables. No new
strong-field observable is defined. A waveform, shadow, Love number,
quasinormal spectrum, core radius, limiting curvature, or remnant property
requires a healthy accepted action and a solved branch.

### FORWARD_MODEL

`N/A`. There is no detector, telescope, waveform, catalogue, likelihood, or
instrument model. The action fails before an observational forward model is
authorized.

### DATA_ROLE

`NO_DATA_READ_OR_FITTED`. Primary papers are analytic provenance and theorem
handoffs, not fit data. The Böhmer--Fiorini regular-interior result motivates
the candidate form but is not imported as a RefG solution or validation datum.

### IDENTIFIABILITY

The function shape and branch are fixed, while `Lambda_*` remains one
unspecified universal scale. Weak/1PN data cannot identify it at the retained
order because the correction begins beyond that order. No identifiability
claim is made after the health veto, and no parameter scan is allowed.

### BENCHMARK

Required exact benchmarks are:

```text
f_BI(0)=0,
f_T(0)=1,
f_TT(0)=1/Lambda_*,

f_BI(T)=T+T^2/(2Lambda_*)+T^3/(2Lambda_*^2)
          +5T^4/(8Lambda_*^3)+O(T^5),

T=O(epsilon^2)
  -> f_BI-T=O(epsilon^4)
  -> delta(Euler--Lagrange)=O(epsilon^3),

T < Lambda_*/2,
T -> (Lambda_*/2)^-  -> f_T,f_TT -> +infinity.
```

The upstream W3-52 ten-entry PPN vector must equal its registered GR values,
including `beta=gamma=1`, and its retained/first-omitted component orders must
remain exact. The candidate health benchmark requires a kinetic term in the
quadratic Hessian for every nonlinear physical mode; the late-onset `f(T)`
sector has none and triggers rejection.

### CLOSURE_FLAGS

All atomic flags start false.

Required true for a valid completed audit:

- `g0_goal_pass`
- `g1_conventions_pass`
- `g2_core_algebra_pass`
- `g3_audit_pass`
- `g3_structure_health_veto_failed_exact`
- `g4_independent_check_pass`
- `g5_limits_regression_pass`
- `g6_physical_match_pass`
- `g7_observation_not_applicable_exact`
- `g8_export_not_applicable_exact`
- `dependency_hashes_exact`
- `upstream_status_and_scope_exact`
- `newly_selected_universal_candidate_action_registered_exact`
- `born_infeld_function_and_principal_branch_exact`
- `square_root_domain_exact`
- `f_T_exact`
- `f_TT_exact`
- `low_T_series_exact`
- `torsion_weak_order_exact`
- `born_infeld_correction_quartic_action_order_exact`
- `born_infeld_correction_cubic_eom_order_exact`
- `tegr_quadratic_hessian_exact`
- `full_standard_1pn_ppn_regression_exact`
- `full_1pn_componentwise_remainder_regression_exact`
- `covariant_flat_inertial_spin_connection_registered_exact`
- `pure_tetrad_arbitrary_frame_mutation_rejected`
- `one_coframe_one_metric_once_counted_source_ledger_exact`
- `finite_lambda_nonzero_f_TT_exact`
- `nonlinear_ft_late_onset_mode_handoff_registered_exact`
- `precise_universal_dof_count_not_claimed_exact`
- `weak_branch_kinetic_health_requirement_exact`
- `late_onset_sector_missing_quadratic_kinetic_exact`
- `strong_coupling_cutoff_completion_absent_exact`
- `hard_health_veto_triggered_exact`
- `born_infeld_ft_candidate_rejected_exact`
- `global_solution_stop_rule_enforced`
- `mutation_controls_pass`
- `package_clean_pass`
- `aggregate_audit_pass`

Required false:

- `candidate_structure_health_pass`
- `aggregate_candidate_admissibility_pass`
- `born_infeld_candidate_refg_derived`
- `born_infeld_candidate_unique`
- `Lambda_star_derived_from_foundation`
- `Lambda_star_observationally_identified`
- `nonlinear_mode_quadratic_kinetic_closed`
- `strong_coupling_scale_derived`
- `full_nonlinear_dof_count_claimed`
- `foundation_strong_field_response_derived`
- `regular_black_hole_solution_derived`
- `trapped_surface_derived`
- `geodesic_completeness_derived`
- `singularity_resolution_completed`
- `new_strong_field_prediction_derived`
- `observational_forward_model_built`
- `observational_likelihood_evaluated`
- `canon_changed`
- `intuitive_files_changed`

### CROSSCHECK

The verifier must obtain the Taylor series both from symbolic expansion and
from derivatives at `T=0`; obtain `f_T` and `f_TT` both by direct
differentiation and substitution; verify the weak order by an explicit formal
`epsilon` substitution; import the complete W3-52 PPN vector and its
componentwise remainder contract; verify the one-source ledger independently
of the function algebra; and apply the same production validators to wrong
quadratic coefficient, wrong derivative sign, missing square-root domain,
included singular boundary, `f_TT=0`, pure-tetrad arbitrary-frame, duplicated
source, promoted 1PN correction, precise-mode-count, imported-regular-black-
hole, bypassed-health-veto, and false-scope mutations.

### PROVENANCE

The verifier pins this preregistration and every local dependency by SHA-256.
It records Python/SymPy/platform versions and deterministic execution. A
wall-clock UTC timestamp is deliberately omitted from the payload so repeated
runs are byte-identical. `network_used_by_verifier=false` and
`archived_theory_used=false`. The result is strict finite UTF-8 JSON written
atomically with `allow_nan=false`.

Primary-source provenance:

1. M. Krššák and E. N. Saridakis, *The covariant formulation of f(T)
   gravity*, Class. Quantum Grav. 33, 115009 (2016),
   https://arxiv.org/abs/1510.08432.
2. Y. C. Ong, K. Izumi, J. M. Nester, and P. Chen, *Problems with
   Propagation and Time Evolution in f(T) Gravity*, Phys. Rev. D 88, 024019
   (2013), https://arxiv.org/abs/1303.0993.
3. J. Beltrán Jiménez, A. Golovnev, T. Koivisto, and H. Veermäe,
   *Minkowski space in f(T) gravity*, Phys. Rev. D 103, 024054 (2021),
   https://arxiv.org/abs/2004.07536.
4. A. Golovnev and M.-J. Guzmán, *Lorentz symmetries and primary constraints
   in covariant teleparallel gravity*, Phys. Rev. D 104, 124074 (2021),
   https://arxiv.org/abs/2110.11273.
5. C. G. Böhmer and F. Fiorini, *The regular black hole in four dimensional
   Born--Infeld gravity*, Class. Quantum Grav. 36, 12LT01 (2019),
   https://arxiv.org/abs/1901.02965.
6. Y.-M. Hu, Y. Zhao, X. Ren, B. Wang, E. N. Saridakis, and Y.-F. Cai,
   *The effective field theory approach to the strong coupling issue in f(T)
   gravity*, JCAP 07 (2023) 060, https://arxiv.org/abs/2302.03545.

The fifth source uses
`lambda[sqrt(1+2T/lambda)-1]`; its negative branch
`lambda=-Lambda_*<0` is exactly the frozen function above. Its regular
interior motivates the one-candidate test. Its solution is not imported
because W3-68 applies the health veto first and uses the covariant connection
registry.

### FILES

- `w3_68_born_infeld_candidate_admissibility_preregistration.md`
- `w3_68_born_infeld_candidate_admissibility.py`
- generated `w3_68_result.json`

No Canon, article, intuitive file, or other work package is changed by this
stage.

## Decision semantics

A completed W3-68 audit may pass while the candidate fails. Audit PASS means
that the candidate was specified, checked, regressed, and rejected by the
predeclared health criterion without continuing into an irrelevant global
solve. Accordingly, the required G3 audit gate passes when it correctly
detects the failed candidate structure-health gate; these are distinct
Booleans and must not be conflated.

The required completed status is

```text
PASS_EXACT_BORN_INFELD_FT_ACTION_AND_WEAK_TEGR_1PN_REGRESSION__REJECTED_CANDIDATE_BY_LATE_ONSET_MODE_WEAK_BRANCH_HEALTH_VETO__GLOBAL_STRONG_FIELD_SOLVE_NOT_OPENED
```

This status rejects only the frozen Born--Infeld `f(T)` candidate and closes
W3-68 at the first decisive obstruction.
