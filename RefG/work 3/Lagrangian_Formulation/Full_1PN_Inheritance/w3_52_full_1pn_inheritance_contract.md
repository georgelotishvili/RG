# W3-52 — Full standard 1PN inheritance on the RefG operational branch

## Frozen claim contract

- `CLAIM_ID`: `W3_52_REFG_FULL_1PN_INHERITANCE`
- `CLAIM`: On the selected connected post-Genesis low-energy branch, if the
  complete RefG operational action through first post-Newtonian order is the
  Einstein--Hilbert action with one universally and minimally coupled matter
  sector, one conserved source ledger, the same local source/boundary problem
  and no additional unsuppressed operational field or operator at that order,
  then the complete standard 1PN metric and weak-body equations of motion are
  exactly those of General Relativity. The inherited published PPN vector is

  ```text
  beta=gamma=1,
  xi=alpha1=alpha2=alpha3=zeta1=zeta2=zeta3=zeta4=0.
  ```

  The RefG pressure factor `p` is a bounded clock/ruler readout of this one
  geometry on its static isotropic slice. It is not a second field added to
  the metric and it is not a second source entry.
- `TYPE`: `EXACT_CONDITIONAL_EFFECTIVE_ACTION_INHERITANCE` and
  `CONDITIONAL_MATCHED_THROUGH_FULL_STANDARD_1PN_PPN`.
- `MODEL_VERSION`: `W3-52-v1.1-FULL-1PN-INHERITANCE`.
- `EVIDENCE_STATUS`: `CONDITIONAL_IMPLICATION_PASS` when every antecedent and
  audit gate passes. The antecedents are effective premises, not outputs of
  this script.
- `VERSION_HISTORY`: v1.1 explicitly separates frozen effective premises,
  published benchmark theorems, derived corollaries and transcription audits;
  corrects the preferred-frame `g0i` registry; makes all PN remainders
  componentwise; and removes any claim of an independent EH-to-PPN derivation.

### ASSUMPTIONS

1. RefG has one Lorentzian operational metric `g_mn`; matter, radiation,
   clocks and rulers all couple to that same metric.
2. Through retained 1PN order the complete local operational action is

   ```text
   S_1PN = c0^3/(16 pi G) integral sqrt(-g) (R-2 Lambda_eff) d^4x
           + S_matter[g,Psi] + boundary.
   ```

   This is the selected effective branch premise. W3-52 does not derive it
   from the pregeometric foundation.
3. `S_matter` is diffeomorphism invariant and defines one tensor `T_mn`.
   Density, momentum current, pressure, internal energy and stress belong to
   this one ledger. Pressure, cadence, mass and ruler readouts are not counted
   again as independent sources.
4. No additional long-range scalar, vector or tensor field, preferred
   operational direction, nonuniversal metric coupling, or unsuppressed
   higher-derivative operator contributes through the retained component
   orders.
5. With `q~U/c0^2~v^2/c0^2`, the metric is retained through

   ```text
   g00: q^2,    g0i: q^(3/2),    gij: q.
   ```

   Local `Lambda_eff` and higher-operator corrections begin no earlier than

   ```text
   delta g00: q^3,    delta g0i: q^(5/2),    delta gij: q^2.
   ```

6. RefG and the GR benchmark use the same measured `G`, matter action,
   source data, standard PPN gauge, local background subtraction and boundary
   conditions. No PPN coefficient is fitted to an observation.
7. The standard PPN metric, GR parameter vector and weak-body EIH result are
   registered external benchmark theorems. The script integrity-checks and
   applies them; it does not rederive them from the Einstein equations.

### DOMAIN

- Isolated, weak-field, slowly moving, weakly self-gravitating sources of
  arbitrary shape and motion in the standard PPN regime.
- A local asymptotically Minkowskian patch after homogeneous cosmological
  background subtraction.
- Conservative dynamics through 1PN, including the moving-source `g0i`
  sector and the standard weak-body many-body/EIH corollary.
- Excluded: microscopic oscillon-to-`T_mn` matching, strong-field
  sensitivities, spinning-body finite-size terms, 2PN completion, radiation
  reaction at 2.5PN, cosmological gradients and the foundation derivation of
  the effective Einstein--Hilbert branch.

### CONVENTIONS

- The PPN fixture uses the standard `(-,+,+,+)` presentation; reversing the
  overall metric signature to RefG's `(+,-,-,-)` convention does not change
  any PPN parameter.
- Standard powers of `c0` are absorbed into the PPN potentials
  `U, Phi_W, Phi_1, Phi_2, Phi_3, Phi_4, A, V_i, W_i, U_ij`.
- The parameter order is
  `(gamma,beta,xi,alpha1,alpha2,alpha3,zeta1,zeta2,zeta3,zeta4)`.
- `q` is PN amplitude bookkeeping, not a fitted physical parameter.

### ONTOLOGICAL_MAP

- One foundation relaxation process has one operational geometry.
- On the static isotropic Einstein--Hilbert slice, the exact clock factor is

  ```text
  p_t=sqrt(g00)=(1-u/2)/(1+u/2),
  -ln(p_t)=u+O(u^3).
  ```

- The coordinate ruler-footprint factor is

  ```text
  p_L=(1+u/2)^(-2).
  ```

  `p_t` and `p_L` share `1-u+O(u^2)`, which is precisely the retained spatial
  order fixing `gamma`. They differ at `O(u^2)`, so W3-52 does not falsely
  impose one exact scalar factor on the unretained 2PN spatial sector.
- For moving or nonspherical sources, current, shear and tensor entries are
  components of the same `g_mn`; they are not a second geometry added to `p`.
- Foundation pressure/energy/geometry and material mass/size/cadence are
  linked readouts of one state and do not duplicate `T_mn`.

### FREEDOM_LEDGER

- `G`: one measured universal coupling.
- `Lambda_eff`: one homogeneous coefficient whose local componentwise effect
  is frozen below the retained 1PN boundary.
- Source: one conserved `T_mn` generated by `S_matter`.
- Gauge/background/boundary data: one shared standard PPN problem.
- Fitted exponents, interpolation functions, object-specific coefficients,
  second metrics and extra retained 1PN fields: none.

### DEPENDENCIES

- `EXECUTION_DEPENDENCIES`: Python standard library and SymPy only. The gate
  reads no other project file except its sibling contract for provenance.
- `PHYSICAL_LINEAGE`: the selected conditional Einstein--Hilbert architecture
  registered in `RefG_Formal_Proof.md`.
- `BOUNDED_REGRESSION_LINEAGE`: W3-51's static spherical `beta=gamma=1` gate;
  W3-52 recreates the overlap algebra and does not import its result.
- Old-theory and Work 2 files are neither evidence nor dependencies.

### METHOD

1. Audit the independently written selected-action and canonical
   Einstein--Hilbert operator registries. This checks the frozen premise; it
   does not derive that premise.
2. Apply the registered Einstein--Hilbert basis variations and verify the
   Einstein field-equation coefficients and Bianchi conservation corollary.
3. Verify universal one-metric coupling, one-source counting, exact retained
   component orders and componentwise remainder bounds.
4. Apply the functional-identity theorem: identical action, matter,
   source/gauge/background and boundary problems have identical
   Euler--Lagrange equations and order-by-order solutions.
5. Integrity-check the published standard PPN formula registry and GR vector.
   Check rank ten and invert its coefficients only as a transcription/formal-
   identifiability regression, never as an independent derivation.
6. Register the complete GR PPN vector and weak-body EIH result as exact
   corollaries of Step 4.
7. Reconstruct the bounded static clock/ruler readout and run mutations that
   break action identity, universality, source counting, conservation,
   component order, preferred-frame neutrality, benchmark integrity,
   remainder bounds or the static constitutive law.

### PASS_CONDITION

The conditional implication passes exactly when:

1. Every effective antecedent is explicitly registered and internally
   consistent; no antecedent is reported as foundation-derived.
2. Einstein--Hilbert basis variation and Bianchi residuals vanish exactly.
3. One metric and one conserved source ledger pass with no duplicate readout.
4. `g00`, `g0i`, `gij` and their componentwise first-omitted orders match the
   frozen registry exactly.
5. Published PPN formula/vector integrity locks pass, the formal registry has
   rank ten, and its transcription inversion returns the registered vector.
6. Functional identity transfers the complete published GR PPN vector and
   weak-body EIH result.
7. The static readout gives `beta=gamma=1` through its declared orders.
8. Every mutation breaks its targeted antecedent or audit.

### FAIL_CONDITION

The gate fails if an antecedent is absent, a retained action or variation
residual is nonzero, a second source/metric/field is required, `g0i` or its
order is missing, a componentwise correction enters within a retained order,
either benchmark integrity lock changes, or any mutation goes undetected.

### FALSIFIER

Within the stated domain, an independently derived unsuppressed foundation
mode, nonuniversal coupling, preferred direction, duplicated/nonconserved
source, or non-Einstein operator at retained order falsifies this exact
inheritance theorem's applicability. A measured non-GR PPN coefficient would
falsify the selected effective branch, while leaving identification of the
failed antecedent to a separate test.

### RESIDUAL

- Selected-action minus canonical-EH premise registry: exact symbolic zero.
- Registered EH variation minus Einstein equation: exact symbolic zero.
- Bianchi divergence solution: `nabla_m T^mn=0`.
- Order registries: exact componentwise equality.
- PPN fixture and GR-vector hashes: exact equality to frozen published
  transcriptions.
- PPN transcription regression: rank minus ten and solution-count minus one.
- Static readout: coefficients of `-ln(p_t)-u` through `O(u^2)` and the
  clock/ruler common coefficient through `O(u)`.

### ERROR_BOUND

All retained implication and audit checks are exact symbolic identities. The
first untested metric contributions are componentwise

```text
delta g00=O(q^3),    delta g0i=O(q^(5/2)),    delta gij=O(q^2).
```

The local `Lambda_eff` and higher-operator contributions are assumed to begin
at or beyond those same componentwise orders. There is no floating-point,
catalog or likelihood error in this gate.

### VALIDITY_HEALTH

The frozen Einstein--Hilbert branch has the standard healthy massless spin-2
effective kinetic structure and universal minimal coupling. W3-52 does not
prove the foundation origin, sign, cutoff, source map or stability of a
microscopic pressure sector; these remain explicit open flags.

### BRANCHES

- Live branch: one operational Einstein--Hilbert metric with universal
  coupling and all non-EH effects beyond the retained component orders.
- Mutation branches: extra scalar/vector, bimetric light coupling, preferred
  direction, duplicate/nonconserved source, missing/wrong-order `g0i`, early
  `Lambda_eff`/higher-operator contribution, altered PPN fixture/vector and
  second-order logarithmic response.
- A mutation only breaks this exact inheritance theorem; it is not a blanket
  rejection of every possible alternative theory.

### OBSERVABLE_MAP

The inherited metric fixes the standard weak-field 1PN clock, light,
test-body and conservative weak-body many-body observables. In the declared
domain RefG's selected branch is operationally indistinguishable from GR at
1PN. This establishes compatibility, not a new deviation.

### FORWARD_MODEL

`N/A`: this is an analytic conditional-identity gate. It constructs no
instrument response, selection function or likelihood. The ideal standard
1PN observables are inherited with the metric; re-fitting the same GR curve
would not test the foundation ontology separately.

### DATA_ROLE

`N/A`: no observational catalog is selected, fitted or excluded.

### IDENTIFIABILITY

The standard PPN potential-coefficient registry has formal algebraic rank ten
in an independent-potential basis. This is not a claim that real observations
measure all ten parameters independently. RefG and GR are ontologically
non-identifiable using observables that depend only on their shared 1PN
metric.

### BENCHMARK

- The standard ten-parameter PPN metric and published GR vector. Their
  transcriptions are integrity-locked in the script.
- The standard weak-body 1PN/EIH corollary of the Einstein--Hilbert action.
- Threshold: exact conditional identity, not an observational tolerance.

Primary references:

- C. M. Will and K. Nordtvedt Jr., *Conservation Laws and Preferred Frames in
  Relativistic Gravity. I*, Astrophysical Journal 177 (1972) 757,
  DOI: `10.1086/151754`.
- C. M. Will, *The Confrontation between General Relativity and Experiment*,
  Living Reviews in Relativity 17 (2014) 4, arXiv: `1403.7377`.
- A. Einstein, L. Infeld and B. Hoffmann, *The Gravitational Equations and the
  Problem of Motion*, Annals of Mathematics 39 (1938) 65--100,
  DOI: `10.2307/1968714`.

### CLOSURE_FLAGS

The result separates evidence roles:

- `*_PREMISE_REGISTERED`: frozen effective input, not derived.
- `*_COROLLARY`: exact consequence of the frozen inputs and registered
  external theorem.
- `*_INTEGRITY`, `*_REGRESSION`, `*_RANK_TEN`: mechanical audits only.

All tested premise, corollary, integrity, regression, order and mutation flags
must be `true`. These scope flags remain `false`:

- `FOUNDATION_TO_EH_DERIVATION`
- `FOUNDATION_TO_FULL_METRIC_MAP`
- `MICROSCOPIC_SOURCE_MATCHING`
- `STRONG_FIELD_AND_2PN_COMPLETION`

Successful aggregate status:
`CONDITIONAL_MATCHED_THROUGH_FULL_STANDARD_1PN_PPN`.

### CROSSCHECK

The proof route is the conditional functional-identity theorem. The PPN
coefficient inversion is only a fixture transcription/identifiability audit.
The static clock/ruler calculation is a separate bounded regression. No route
imports a target radial profile or an old-theory artifact.

### PROVENANCE

- Deterministic symbolic execution under the Python and SymPy versions
  recorded in `w3_52_result.json`.
- SHA-256 hashes of the script and contract are recorded in the result.
- The PPN formula registry and published GR vector have separate frozen
  SHA-256 integrity locks.
- External project-file runtime dependencies: none.

### FILES

- `w3_52_full_1pn_inheritance_contract.md`: frozen claim and evidence roles.
- `w3_52_full_1pn_inheritance.py`: premise audit, conditional implication,
  benchmark integrity, bounded regression and mutation controls.
- `w3_52_result.json`: deterministic machine-readable result.

### STOP_RULE

Stop when the complete tested flag set passes. Do not open 2PN, strong-field,
radiation-reaction, cosmological or particle-microphysics calculations inside
this gate. The next distinct research problem is the foundation derivation of
the effective metric/action and microscopic source map.
