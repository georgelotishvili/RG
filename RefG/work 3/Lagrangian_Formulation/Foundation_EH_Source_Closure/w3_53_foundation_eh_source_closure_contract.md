# W3-53 Contract: Selected IR Spin-2 to Einstein--Hilbert and Source Map

## Decision and exact stopping point

**Status:**
`CONDITIONAL_EXACT_SELECTED_IR_SPIN2_TO_EINSTEIN_HILBERT_AND_OPERATIONAL_HILBERT_SOURCE_MAP`.

This stage closes one bounded theorem chain:

```text
selected conservative relational IR tensor branch
  -> unique Fierz--Pauli quadratic coefficients
  -> standard two-helicity spin-2 theorem
  -> Weinberg universal leading soft coupling
  -> Deser nonlinear Einstein--Hilbert completion
  -> generic S_loc-to-T_mn Hilbert map
  -> STOP.
```

It does not claim a node-scale Hamiltonian, a derived
`Phi_F -> h_mn -> g_mn` map, a foundation-ledger-to-`S_loc` coarse-graining,
an oscillon action, or numerical values for `G` and `Lambda`. Those facts are
not hidden inside a `PASS` label.

The evidence is split explicitly:

- **computed exactly here:** the volume/shape witness, Fierz--Pauli coefficient
  ratios, pure-gradient curvature cancellation, a reduced soft-coupling
  witness, source gauge conservation, and a scalar Hilbert/translation-ledger
  witness;
- **published theorem handoffs:** the Fierz--Pauli physical spectrum,
  Weinberg soft universality, Deser bootstrap, and Lovelock uniqueness;
- **selected IR premises:** the tensor branch, emergent Lorentz symmetry and
  common cone, retained field content, retained operator order, and one-source
  ledger.

No later calculation is opened by this result.

## 1. What the water analogy fixes

The water analogy fixes the foundation's conservative, wave-carrying and
pressure-sensitive character. It does not make an ordinary barotropic fluid
mathematically identical to gravity. A scalar inviscid fluid produces a
compressional acoustic mode; a massless gravitational field requires an
independent tensor sector.

RefG therefore uses one substance with different state components:

- participation, phase density and dilation describe its scalar/volumetric
  response;
- shape/shear and the still-separate coframe/orientation information provide
  the candidate tensor-capable sector;
- localized and radiative organizations provide the candidate operational
  source sector.

This is not a division into several media and does not create several gravity
sources.

## 2. W3-42-compatible volume/shape selection

W3-42 proved that its constraints do not uniquely select a physical cell,
dimension or measure. W3-53 does not reverse that result. It selects one
`d=3` comparison branch compatible with W3-42.

In a `G_0`-orthonormal reference frame and the principal-axis frame of a
symmetric trace-free shape matrix `s`, write

```text
G_rel = a^2 exp(2 s),     tr(s)=0.
```

Then

```text
sqrt(det G_rel) = a^3.
```

The verifier proves this determinant identity exactly. Here `a` is the
foundation link/volume-dilation coordinate. `P_F`, `eta_F` and `p` remain
distinct state/readout variables connected only by their already declared
conditional maps. They are not renamed as `a`.

The Gram matrix records lengths, angles, shape and shear. A separate coframe
or relational-frame variable is required to retain orientation information.
Neither the spatial Gram witness nor W3-50's `(n_C,theta_C)` pair constructs
the complete four-dimensional `h_mn[Phi_F]` map. W3-53 selects that IR tensor
branch explicitly rather than claiming to derive it.

The tensor field is independent and nonintegrable. It is not restricted to

```text
h_mn = partial_m u_n + partial_n u_m.
```

The verifier confirms that this pure-gradient form has identically zero
linearized Riemann tensor. Topological incompatibility can motivate an
independent tensor but is not used as a substitute for its dynamics.

## 3. Frozen IR premises

The following are the minimum premises of this theorem. None contains `R`,
`G_mn`, the Einstein equation, a Newtonian target profile, or a PPN target:

1. **Closed reversible foundation.** The connected post-Genesis foundation
   admits one time-translation-invariant canonical action with no external
   bath, viscosity or Rayleigh dissipation. This forbids fundamental friction;
   it does not forbid radiation from a changing configuration.
2. **Relational redundancy.** Foundation labels are nonphysical. The complete
   state includes an independent nonintegrable shape/shear tensor in addition
   to scalar participation and dilation.
3. **Selected relativistic IR phase.** The retained connected phase is `3+1`
   dimensional, has emergent Lorentz invariance, one universal causal speed
   `c0`, and the linear relabelling rule

   ```text
   delta h_mn = partial_m xi_n + partial_n xi_m.
   ```

4. **Retained healthy field content.** No tensor mass and no extra
   unsuppressed long-range scalar, vector or second tensor geometry mode is
   retained.
5. **Leading local truncation.** The gravitational action is local and has at
   most two derivatives at this order.
6. **Soft consistency.** The IR theory is unitary and analytic with a
   factorizing soft pole. No unsuppressed nonminimal curvature/tidal matter
   coupling contributes at the retained W3-52 order.
7. **One operational source ledger.** The selected effective split has one
   `S_loc[g,Y]` for localized and radiative excitations. Metric self-energy,
   background pressure/readouts and a homogeneous vacuum offset are not added
   to it a second time.

Premises 3--6 are the irreducible bridge that an ordinary pressure-only ocean
cannot supply. A future node-scale spectrum may realize or falsify them. Until
then they are selected premises, not microscopic outputs.

## 4. Exact Fierz--Pauli coefficient derivation

Use the standard `(-+++)` theorem convention. RefG's operational `(+---)`
presentation is the overall-sign-reversed metric convention already permitted
by W3-52.

Modulo boundary terms, the most general local Lorentz-invariant quadratic
two-derivative action for an independent symmetric field is

```text
L_2 = a1 partial_l h_mn partial^l h^mn
    + a2 partial_m h^mn partial^l h_ln
    + a3 partial_m h^mn partial_n h
    + a4 partial_l h partial^l h.
```

The divergence of its Euler tensor has three independent structures. Exact
linear gauge invariance requires

```text
2 a1 + a2 = 0,
a2 + a3 = 0,
a3 + 2 a4 = 0.
```

The coefficient matrix has rank three, so its nullspace is one-dimensional.
Positive transverse-traceless normalization in `(-+++)` fixes

```text
(a1,a2,a3,a4) = (-1/2,1,-1,1/2).
```

These ratios are derived symbolically rather than inserted. Mutating any one
coefficient while holding the other three fixed breaks the same gauge
validator.

The physical two-helicity result is the standard Fierz--Pauli Hamiltonian
theorem, not a new constraint derivation by the script. Its registered count
is

```text
20 phase-space dimensions
  - 2 x 8 first-class constraints
  = 4 physical phase-space dimensions
  = 2 configuration degrees of freedom.
```

The verifier checks this arithmetic and applies the theorem; it does not
pretend to have derived the eight constraints from a node Hamiltonian.

## 5. Coupling and nonlinear theorem handoffs

At linear order the source term has the form

```text
S_int proportional to integral h_mn tau^mn.
```

Its gauge variation is a boundary term exactly when

```text
partial_m tau^mn = 0.
```

For a two-leg reduced soft witness, momentum conservation leaves the residual

```text
(g_1-g_2) p^n.
```

The verifier checks all four components: `g_2=g_1` cancels them, while a
species-dependent mutation does not. The general statement for arbitrary
external legs is Weinberg's soft-graviton theorem. It fixes the common leading
soft charge, not every possible higher-derivative tidal interaction. The
absence of an unsuppressed nonminimal coupling at retained order is therefore
listed separately as a premise.

Deser's first-order proof then supplies the nonlinear completion. W3-53 keeps
a schematic operator registry

```text
h partial Gamma + eta Gamma Gamma + h Gamma Gamma
```

only to record the theorem's handoff. That registry is not called an
independent symbolic derivation of the Palatini contractions or connection
variation. Under Deser's locality, gauge-consistency and universal-coupling
conditions, the endpoint is the Einstein--Hilbert `R` operator.

Four-dimensional Lovelock uniqueness independently supplies the same local
metric-only zero-plus-two-derivative basis. It also permits one independent
zero-derivative matching term `Lambda`. Thus:

- the flat-space Fierz--Pauli/Deser route derives the nonlinear `R` operator;
- `Lambda` is allowed separately and its value is not derived;
- for nonzero `Lambda`, the exact linear theory must be formulated on the
  corresponding Einstein/(A)dS background, or the flat calculation is used
  only locally at scales `L << |Lambda|^(-1/2)`.

The bounded endpoint action is

```text
S_op^(0+2) = c0^3/(16 pi G) integral d^4x sqrt(-g)(R-2 Lambda)
             + S_loc[g,Y] + S_boundary.
```

## 6. Generic operational source map

W3-53 uses the W3-52-compatible variational convention with
`x^0=c0 tau`:

```text
T_mn = -(2 c0/sqrt(-g)) delta S_loc/delta g^mn,
delta S_loc = -(1/(2 c0)) integral sqrt(-g) T_mn delta g^mn.
```

Together with the declared Einstein--Hilbert variation, stationarity gives

```text
G_mn + Lambda g_mn = (8 pi G/c0^4) T_mn.
```

Diffeomorphism invariance gives `nabla_m T^mn=0` on the excitation equations.
The tensor's components package energy density, momentum density, pressure
and shear/momentum flux in one object.

The scalar witness checks the generic map in the standard `(-+++)`
convention. It verifies positive `T_00`, the momentum components, symmetric
stress, and agreement with the translation energy-current after the standard
mixed-index sign conversion. It is not a RefG particle model.

The source ledger is selected and duplication-audited:

```text
selected operational S_loc variation            1
metric self-energy re-added on the right         0
P_F or p readout re-added                        0
clock/ruler readout re-added                     0
homogeneous vacuum offset re-added               0
```

Metric self-energy is already on the Einstein--Hilbert side. `P_F`, `p`,
material scale and cadence are readings of the metric/foundation state, not
additional matter sources. A stationary homogeneous offset occupies the
single `Lambda` slot.

What is derived is

```text
given diffeomorphism-invariant S_loc[g,Y]
  -> one Hilbert T_mn and its conservation law.
```

What is not derived is

```text
Phi_F energy bins / W3-50 H_C
  -> the concrete coarse-grained S_loc[g,Y].
```

Accordingly, `MICROSCOPIC_SOURCE_MATCHING=false` remains explicit.

## 7. No-go and dependency boundary

A pressure-only scalar fluid and a pure-gradient displacement strain are
failing controls. The historical files

```text
w3_01_emergent_metric_from_pressure.py
w3_02_emergent_action_from_pressure.py
w4_02_biconformal_gravity.py
w4_04_strain_tensor_action.py
w4_05_defect_tensor_gravity.py
w4_06_kleinert_equivalence.py
```

are forbidden logical dependencies. They either insert the desired potential
or action, use pure gauge, assume TT/massless structure before counting, or
construct the Einstein tensor before naming it a defect tensor.

W3-52 is not a W3-53 dependency. It consumes the Einstein--Hilbert branch
downstream and is rerun only as a regression:

```text
W3-42 / W3-46 / W3-50
             -> W3-53
             -> W3-52 downstream inheritance check.
```

The Weinberg--Witten scope is also explicit. The pregeometric foundation is
not assumed to be a Lorentz-covariant QFT on a pre-existing Minkowski
background with a gauge-invariant local microscopic stress tensor. Lorentz
covariance, the metric and `T_mn` emerge only in the selected operational IR
phase. If a future microtheory has all forbidden premises, the composite
spin-two branch fails.

## 8. Claim contract

- `CLAIM_ID`: `W3_53_SELECTED_IR_SPIN2_EH_SOURCE_MAP`.
- `CLAIM`: Conditional on the explicitly selected conservative, relational,
  Lorentz-invariant, common-cone IR tensor branch, gauge invariance uniquely
  fixes the Fierz--Pauli coefficient ratios. Published Fierz--Pauli, Weinberg,
  Deser and Lovelock theorems then take the branch to the Einstein--Hilbert
  operator, while any selected diffeomorphism-invariant `S_loc` generates one
  operational Hilbert `T_mn`. The node-scale tensor/full-metric map and the
  foundation-to-`S_loc` source matching are not claimed.
- `TYPE`:
  `EXACT_CONDITIONAL_IR_COEFFICIENT_DERIVATION_WITH_EXTERNAL_THEOREM_HANDOFFS_AND_GENERIC_SOURCE_MAP`.
- `MODEL_VERSION`: `W3-53-v1.1-SELECTED-IR-SPIN2-EH-SOURCE-MAP`.
  Changing the selected IR field content, Lorentz/common-cone premise, gauge
  law, derivative order, retained nonminimal-coupling boundary, source split,
  signature/variation convention, or theorem set creates a new version.
- `ASSUMPTIONS`: Exactly the seven premises in Section 3. W3-42, W3-46 and
  W3-50 supply the hash-locked upstream state/ontology constraints. W3-52 is a
  downstream regression and never an input.
- `DOMAIN`: Connected post-Genesis `3+1` IR phase; emergent Lorentz invariance;
  stable massless tensor branch; leading local zero-plus-two-derivative
  metric order. The flat Fierz--Pauli calculation has `Lambda=0` exactly, or
  applies locally for `L << |Lambda|^(-1/2)`; nonzero `Lambda` globally
  requires the corresponding Einstein-background spin-two formulation.
  Genesis, node spectra, Lorentz-breaking corrections, explicit particles,
  higher curvature, parameter matching and observations lie outside.
- `CONVENTIONS`: The theorem calculation uses `(-+++)` and
  `T_mn=-(2c0/sqrt(-g)) delta S_loc/delta g^mn`; RefG's operational `(+---)`
  convention is the overall reversal already allowed by W3-52. `a` is link
  dilation; `P_F`, `eta_F` and `p` remain distinct. Boundary terms and
  invertible local field redefinitions do not change the endpoint.
- `FREEDOM_LEDGER`:
  - zero fitted parameters and zero fitted functions;
  - one overall tensor normalization later identified with measured `G`;
  - one allowed zero-derivative coefficient `Lambda`;
  - one unresolved cutoff controlling higher operators;
  - selected, not fitted: dimension, Lorentz/common cone, tensor/gauge branch,
    retained field content, no retained nonminimal matter coupling, and one
    operational source ledger;
  - no object-specific coupling, target PPN value, profile, potential or data
    calibration.
- `DEPENDENCIES`: Hash-locked W3-42, W3-46 and W3-50 only. W3-52 and the
  historical ansatz scripts are not dependencies.
- `METHOD`: Exact determinant witness; exact coefficient-matrix nullspace;
  direct gauge residuals; pure-gradient Riemann cancellation; independent
  tensor curvature witness; reduced four-component soft residual; source
  conservation identity; schematic Deser registry labeled as such; published
  theorem handoffs; scalar Hilbert/translation-ledger comparison; source-count
  and mutation controls.
- `PASS_CONDITION`: Every exact residual vanishes; every registered dependency
  hash matches; every theorem premise is explicitly selected; FP coefficient,
  species-coupling, source-duplication and selected-premise mutations fail;
  evidence roles and unclosed microscopic maps remain correctly classified.
- `FAIL_CONDITION`: Einstein curvature or a target solution enters the IR
  premises; W3-52 becomes an upstream dependency; a pressure-only or
  pure-gradient field passes the tensor gate; a species-dependent leading
  soft coupling survives; a theorem registry is reported as a new proof;
  `S_loc` is claimed to come from `Phi_F` without a coarse-graining; a readout
  is added twice; or any exact/mutation/dependency gate fails.
- `FALSIFIER`: The selected branch fails if a future foundation spectrum lacks
  the tensor mode, contains ghosts or extra unsuppressed modes, violates
  emergent Lorentz/common-cone behavior, requires species-dependent leading
  coupling, or satisfies the Weinberg--Witten forbidden microscopic premises.
- `RESIDUAL`: Exact zero for the principal-axis Gram determinant and
  trace-free identities, the three FP gauge-identity coefficients, 256
  pure-gradient linearized-curvature components, the reduced soft
  substitution, source-gauge conditions and scalar source-map witness.
  Deser, Lovelock, Weinberg and the FP spectrum are theorem applications, not
  entries in this computed-residual list.
- `ERROR_BOUND`: Zero for exact algebra and hashes. No numerical approximation
  enters. No bound is claimed for omitted higher operators before the cutoff
  is derived. On a nonzero-`Lambda` background, flat-branch errors are
  controlled only in the declared local regime `L << |Lambda|^(-1/2)`; no
  numeric remainder is supplied.
- `VALIDITY_HEALTH`: Correct FP normalization on the selected signature,
  registered two-helicity theorem, conserved leading soft source, generic
  Hilbert source map, one-count consistency and explicit no-go scope. This
  validates the conditional IR chain, not its node-scale realization.
- `BRANCHES`: Selected: conservative relational IR tensor, emergent Lorentz
  symmetry, common cone, massless metric-only leading order. Rejected:
  pressure-only acoustic completion, pure-gradient strain, tensor mass,
  extra unsuppressed mode, species-dependent leading soft coupling, duplicate
  source and ordinary background-QFT composite graviton.
- `OBSERVABLE_MAP`: None added. W3-52 remains the downstream full-1PN
  inheritance test; it is not evidence used to select W3-53.
- `FORWARD_MODEL`: `N/A`; no synthetic observable, catalogue or likelihood.
- `DATA_ROLE`: `NO_DATA_READ_OR_FITTED`.
- `IDENTIFIABILITY`: Symmetry and theorems fix the leading operator form and
  leading coupling equality. They do not determine `G`, `Lambda`, the cutoff,
  `h_mn[Phi_F]`, a concrete `S_loc`, or particle properties.
- `BENCHMARK`: Fierz--Pauli gauge identity/spectrum, Weinberg soft theorem,
  Deser first-order bootstrap, Lovelock 4D uniqueness, and the standard
  Hilbert source definition.
- `CLOSURE_FLAGS`:
  - true: `FOUNDATION_CANONICAL_CONSERVATION_SELECTED`,
    `W3_42_COMPATIBLE_VOLUME_SHAPE_BRANCH_SELECTED`,
    `INDEPENDENT_IR_TENSOR_BRANCH_SELECTED`,
    `EMERGENT_LORENTZ_AND_COMMON_CONE_SELECTED`,
    `LINEAR_RELABELING_GAUGE_BRANCH_SELECTED`,
    `FIERZ_PAULI_COEFFICIENTS_DERIVED`,
    `FP_TWO_HELICITY_THEOREM_APPLIED`,
    `WEINBERG_SOFT_UNIVERSALITY_THEOREM_APPLIED`,
    `DESER_PALATINI_BOOTSTRAP_THEOREM_APPLIED`,
    `LOVELOCK_0PLUS2_THEOREM_APPLIED`,
    `GENERIC_SLOC_TO_HILBERT_T_MAP_DERIVED`,
    `ONE_SOURCE_LEDGER_SELECTED_AND_CONSISTENT`,
    `SELECTED_IR_SPIN2_TO_EH_AND_GENERIC_T_MAP_GATE_CLOSED`;
  - false: `NODE_SCALE_MASTER_HAMILTONIAN_DERIVED`,
    `FOUNDATION_TO_FULL_METRIC_MAP_DERIVED`,
    `COMMON_CONE_FROM_NODE_SPECTRUM_DERIVED`,
    `FOUNDATION_LEDGER_TO_S_LOC_COARSE_GRAINING_DERIVED`,
    `MICROSCOPIC_SOURCE_MATCHING`, `PARTICLE_SPECIFIC_S_LOC_DERIVED`,
    `G_VALUE_DERIVED`, `LAMBDA_VALUE_DERIVED`,
    `HIGHER_DERIVATIVE_COEFFICIENTS_DERIVED`.
- `CROSSCHECK`: Nullspace plus direct FP residuals; correct registered
  phase-space count; pure-gradient zero-curvature versus independent-tensor
  nonzero-curvature witnesses; universal versus species-mutated soft residual;
  source-gauge conservation; scalar energy/momentum/stress; duplicate-source
  selected-premise mutations; and dependency DAG audit.
- `PROVENANCE`: Local W3-42/W3-46/W3-50 snapshots hash-locked in the verifier;
  Python/SymPy/platform/UTC in the result; theorem sources below.
- `FILES`: This contract, `w3_53_foundation_eh_source_closure.py`, generated
  `w3_53_result.json`, and the synchronized `RefG_Formal_Proof.md`.
- `STOP_RULE`: Stop after the Einstein--Hilbert operator and generic
  operational Hilbert source map are registered. Do not open node spectra,
  particle species, masses, cosmology, 2PN, strong field, higher-curvature
  fitting or observations.

## 9. Interpretation

W3-53 answers the current question without hiding the hard part. Once RefG's
relational foundation is selected to possess the stated Lorentz-invariant
massless tensor IR branch, the leading gravitational action is no longer an
arbitrary curve-fitting choice: Fierz--Pauli plus the standard consistency
theorems forces Einstein--Hilbert. Once an operational excitation action is
given, its source is not arbitrary either: metric variation produces one
conserved `T_mn`.

The remaining microscopic problem is narrower and clearly named: derive the
selected tensor/common-cone branch and the concrete `S_loc` from a node-scale
foundation Hamiltonian. W3-53 does not solve that problem and does not need
its algebra for the present stopping point.

## Primary theorem sources

- Steven Weinberg, [*Photons and Gravitons in S-Matrix Theory: Derivation of
  Charge Conservation and Equality of Gravitational and Inertial Mass*](https://doi.org/10.1103/PhysRev.135.B1049)
  (1964).
- Steven Weinberg, [*Photons and Gravitons in Perturbation Theory: Derivation
  of Maxwell's and Einstein's Equations*](https://doi.org/10.1103/PhysRev.138.B988)
  (1965).
- Stanley Deser, [*Self-Interaction and Gauge Invariance*](https://doi.org/10.1007/BF00759198)
  (1970; [arXiv reprint](https://arxiv.org/abs/gr-qc/0411023)).
- David Lovelock, [*The Einstein Tensor and Its Generalizations*](https://doi.org/10.1063/1.1665613)
  (1971).
- Steven Weinberg and Edward Witten, [*Limits on Massless Particles*](https://doi.org/10.1016/0370-2693(80)90212-9)
  (1980).

