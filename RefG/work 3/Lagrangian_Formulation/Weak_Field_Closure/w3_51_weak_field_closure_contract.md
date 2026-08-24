# W3-51 — RefG static weak-field closure

## Frozen claim contract

- `CLAIM_ID`: `W3_51_REFG_STATIC_WEAK_FIELD_CLOSURE`
- `CLAIM`: On the static, asymptotically uniform, nonrotating and spherically
  symmetric weak-field branch, the frozen RefG common-response dictionary
  derives the biconformal operational metric, and the selected leading local
  additive log-response closure produces a source profile whose declared PPN-order
  metric has `beta=gamma=1` without inserting `GM/r`, either PPN coefficient,
  or a free response exponent.
- `TYPE`: `EXACT_DICTIONARY` for the operational kinematics;
  `CONDITIONAL_MATCHED_THROUGH_STATIC_SPHERICAL_PPN_BETA_GAMMA` for the
  sourced static solution.
- `MODEL_VERSION`: `W3-51-v1.1-STATIC-WEAK-FIELD`.
- `VERSION_HISTORY`: The v1.0 diagnostic execution acquired no closure
  status. Its Einstein-source substitution was a software failure, and its
  exterior profile check began from the target solution instead of deriving
  the integration constants. Version 1.1 freezes the generic radial ODE,
  adds the missing beta mutation control and restarts every gate.

### ASSUMPTIONS

1. A positive local foundation-response factor `p(x)>0` exists and tends to
   one at spatial infinity.
2. Relative to the asymptotic coordinate standards, the coordinate footprint
   of one local material ruler and a local material clock cadence obey
   `L_coord/L_0=p` and `Omega_t/Omega_t0=p`. `L_coord` is not the ruler's
   locally measured proper length; that proper length remains its local unit.
3. One local light signal crosses one local material standard in one local
   standard light-crossing time. The locally measured limiting speed is
   `c0`.
4. Matter and radiation couple universally to one operational metric and, at
   the effective level tested here, follow its timelike and null geodesics.
   No second refractive factor is added to the metric prediction.
5. The static scalar response is `u=-ln(p)`. At the leading local,
   isotropic, two-spatial-derivative effective level its sourced energy,
   retained in amplitude through the declared static 1PN gate, is

   ```text
   E_stat[u,rho] = integral d^3x [c0^4/(8 pi G) |grad u|^2
                                  - rho c0^2 u].
   ```

   Here `rho` is the effective active Gauss-source density per asymptotic
   coordinate volume. The variation fixes `delta u=0` at spatial infinity.
   Selecting the additive response variable `u=-ln(p)` with this canonical
   gradient term and linear source coupling is the explicit conditional
   premise of the sourced closure. Through this gate it also assumes no
   unsuppressed `K(u)|grad u|^2`, nonlinear `rho f(u)`, or local potential
   term at the same derivative and amplitude order. The common ruler/clock
   dictionary alone does not select these conditions and therefore does not
   determine `beta`. Their derivation from the complete foundation
   Hamiltonian and oscillon stress response is not part of W3-51.
6. The already selected conditional Einstein--Hilbert low-energy branch is
   used only as an independent overlap check. It does not choose the RefG
   response exponents or the pressure profile.

### DOMAIN

- Static, weak (`|u| << 1`), asymptotically uniform branch.
- Compact, nonrotating source; spherical exterior solution.
- Signature `(+---)` and isotropic spatial coordinates.
- `g00` is retained through `O(u^2)` and `gij` through `O(u)`, exactly the
  orders needed to extract the standard static PPN coefficients `beta` and
  `gamma`.
- Cosmological background gradients, preferred-frame sectors, radiation,
  strong fields, `2PN` spatial completion and microscopic oscillon structure
  are outside this claim.

### CONVENTIONS

- `U=GM/r>0` outside a positive isolated source.
- `u=U/c0^2` on the exterior solution.
- `nabla^2 U=-4 pi G rho`; consequently the Newtonian acceleration is
  `a=grad U`, directed inward for `U=GM/r`.
- Static PPN comparison:

  ```text
  g00 = 1 - 2u + 2 beta u^2 + O(u^3),
  gij = -(1 + 2 gamma u) delta_ij + O(u^2).
  ```

### FREEDOM_LEDGER

- `G`: one universal measured coupling normalization.
- `M=int rho d^3x`: effective active Gauss charge fixed by the source ledger.
  This gate does not establish equality with a separately defined proper or
  inertial mass.
- Boundary condition: `u -> 0` at spatial infinity.
- No fitted exponent, radial profile, interpolation function, object-specific
  coefficient or extra refractive factor is admitted.

### DEPENDENCIES

- `intuitive/RefG_GE.md`, Sections 1.5 and 2.1--2.2: oscillon pressure deficit
  and the common material response.
- `RefG/work 3/Lagrangian_Formulation/RefG_Formal_Proof.md`: conditional
  Einstein--Hilbert overlap branch.
- W3-01, W3-02 and W4-02--W4-06 are historical exploratory checks, not
  logical dependencies of this closure.

### METHOD

1. Derive the coordinate light-speed exponent from the frozen material length
   and cadence laws.
2. Derive `g00` from clock accumulation and `gij` from material-ruler
   calibration.
3. Vary `E_stat` with fixed asymptotic boundary value before imposing
   spherical symmetry and obtain the sourced field equation.
4. Solve the exterior spherical equation with the asymptotic and Gauss-flux
   conditions.
5. Expand the resulting operational metric and extract `beta` and `gamma`.
6. Cross-check the declared orders against isotropic Schwarzschild and the
   linearized Einstein `00` equation.
7. Verify the locally reconstructed null speed and run clock-only,
   pure-conformal, canonical-`p` and second-order constitutive mutation
   controls.

### PASS_CONDITION

The declared gate passes exactly when all of the following hold:

1. `c_coord/c0=p^2` follows from the two frozen `p` laws.
2. The operational line element follows as
   `ds^2=p^2 c0^2 dt^2-p^(-2) d x^2`.
   The same dictionary reconstructs the local null speed exactly as `c0`.
3. Variation gives `nabla^2 u=-4 pi G rho/c0^2` with zero symbolic residual.
4. The spherical exterior gives `u=GM/(c0^2 r)` without an inserted radial
   ansatz coefficient beyond the Gauss-fixed charge.
5. The metric gives `beta=1` and `gamma=1` with no free response exponent.
6. The RefG and Einstein--Hilbert overlap residuals vanish through the
   declared PPN orders.
7. Clock-only and pure-conformal controls fail the GR `gamma=1` target;
   canonical harmonic `p` gives `beta=1/2`; and a generic second-order
   mutation displays explicitly how the missing constitutive coefficient
   changes `beta`.

### FAIL_CONDITION

The gate fails if any declared algebraic residual is nonzero, if a response
exponent or radial profile must be fitted to obtain the target, if the source
is counted twice, or if either extracted PPN coefficient differs from one.

### FALSIFIER

The closure is falsified in its domain by an independently derived RefG clock,
ruler or pressure-source law that changes the frozen common response, produces
an unsuppressed `O(u^2)` correction to the sourced potential that changes
`beta`, or yields a nonuniversal operational metric for matter and light.

### RESIDUAL

- Euler--Lagrange residual: evaluated symbolically.
- Exterior spherical residual: evaluated symbolically.
- PPN coefficient residuals: `beta-1`, `gamma-1`.
- Einstein overlap residuals: `g00` through `O(u^2)`, spatial scale through
  `O(u)` and linearized `G00` after the source equation is substituted.
- The first RefG--isotropic-Schwarzschild spatial difference occurs at
  `O(u^2)` and is recorded as an out-of-domain remainder rather than erased.

### ERROR_BOUND

All in-domain checks are exact symbolic identities. Truncation remainders are
`O(u^3)` for `g00` and `O(u^2)` for `gij`. There is no floating-point or data
error in this gate.

### VALIDITY_HEALTH

`p>0` keeps the operational metric nondegenerate. `G>0` gives the static bulk
gradient term a positive coefficient. W3-51 is an elliptic static closure; it
does not establish the dynamical spectrum, causal propagation, nonlinear
stability or microscopic health of the pressure sector.

### BRANCHES

- Live branch: pressure deficit `p=exp(-u)`, `u>0` outside positive mass.
- Negative control A: clock response with no spatial-ruler response.
- Negative control B: a purely conformal metric with the same factor in its
  temporal and spatial components.
- Negative control C: a canonical harmonic `p` field, which preserves the
  biconformal kinematics but gives `beta=1/2`.
- Mutation control: `ln(p)=-u+a u^2+O(u^3)`, which gives `beta=1+a` and
  exposes the precise second-order constitutive freedom.
- Pressure-surplus and strong-field branches are not selected by this claim.

### OBSERVABLE_MAP

The operational metric determines material geodesics, null trajectories,
clock-rate ratios and the standard static PPN observables. At `beta=gamma=1`,
the declared branch has the same perihelion, gravitational redshift, light
deflection and Shapiro-delay coefficients as General Relativity.

### FORWARD_MODEL

`N/A`: W3-51 is an analytic compatibility gate and performs no new fit. The
measured solar-system bounds test the same PPN coefficients, but no catalog or
likelihood is needed to decide the algebraic claim.

### DATA_ROLE

`N/A`: no observational data are selected, fitted or excluded.

### IDENTIFIABILITY

Within the declared static PPN observables, a branch with `beta=gamma=1` is
operationally degenerate with the corresponding General-Relativistic branch.
W3-51 tests compatibility, not ontological uniqueness.

### BENCHMARK

General Relativity in isotropic coordinates, compared coefficient by
coefficient through the frozen PPN orders. The threshold is exact equality.

### CLOSURE_FLAGS

All flags start as `false`:

- `COMMON_RESPONSE_TO_CCOORD`
- `OPERATIONAL_METRIC_DICTIONARY`
- `LOCAL_C_INVARIANCE`
- `STATIC_SOURCE_VARIATION`
- `SPHERICAL_EXTERIOR_PROFILE`
- `PPN_BETA`
- `PPN_GAMMA`
- `EH_OVERLAP`
- `NEGATIVE_CONTROLS`
- `BETA_CONSTITUTIVE_MUTATION_CONTROL`
- `MICRO_SOURCE_DERIVATION`
- `FULL_PPN`
- `NONLINEAR_EH_COMPLETION`

The first ten flags are tested here. The final three remain `false` by the
declared scope. A successful aggregate status is therefore
`CONDITIONAL_MATCHED_THROUGH_STATIC_SPHERICAL_PPN_BETA_GAMMA`.

### CROSSCHECK

The primary route uses the RefG clock/ruler dictionary and conditional
log-response functional. The independent route expands the isotropic Schwarzschild metric
and computes the linearized Einstein `G00` component. Shared conventions and
the measured normalization `G` are declared above.

### PROVENANCE

- Contract date: `2026-08-24` (Asia/Tbilisi).
- Symbolic engine: SymPy, version recorded in the result artifact.
- Source and result hashes are written by the executable gate.

### FILES

- `w3_51_weak_field_closure_contract.md`
- `w3_51_weak_field_closure.py`
- `w3_51_result.json`
- `../RefG_Formal_Proof.md` after closure synchronization.
- `../../../../intuitive/RefG_GE.md` and `../../../../intuitive/RefG_EN.tex`
  only after the result is known.
