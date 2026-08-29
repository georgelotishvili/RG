# W3-62 — CMB Einstein-Source and Linear-Scalar Closure

## Target and stopping rule

This stage opens the cosmic-microwave-background program at the first place
where the existing RefG continuum can make a definite statement. RefG is an
extension and physical grounding of Einstein gravity. The gravitational
operator, null cone and single operational metric remain the
Einstein--Hilbert/TEGR ones already selected in W3-54. No modified Poisson
function, gravitational slip parameter, second metric or replacement field
equation is introduced.

The bounded target is to:

1. identify the density that belongs in the operational Einstein equation;
2. resolve the W3-50/W3-54 foundation-versus-operational volume ambiguity;
3. freeze a once-only CMB source ledger;
4. derive the unique pressureless branch of the W3-54 phase-current action;
5. derive its linear scalar equations and their exact Einstein dust limit;
6. stop before recombination, Boltzmann-code integration, spectra or data.

## 1. Einstein-extension lock

The physical metric used by clocks, rulers, photons and every CMB source is

```text
g_op(mu,nu) = eta_AB e_op^A_mu e_op^B_nu.
```

On a homogeneous spatially flat chart its scale factor is `A`, not the latent
foundation link scale `a_F`:

```text
ds_op^2 = A(eta)^2[-d eta^2 + d x^2],
A = a_F/p.
```

The field equation is therefore retained exactly as

```text
G_mu_nu[g_op] + Lambda_eff g_op_mu_nu
  = (8 pi G/c0^4) T_total_mu_nu.
```

W3-54's TEGR--Einstein--Hilbert derivation is unchanged. W3-62 fixes only the
homogeneous cosmological specialization of its coframe and current density:
the coframe entering the covariant source action is the operational coframe,
and the proper current density defined with `e_op=sqrt(-g_op)` is an
operational-volume density.

## 2. One conserved charge, two density representations

W3-50 and W3-55 define a conserved neutral collective phase charge on the
foundation measure. To prevent the old shared symbol `n_C` from silently
identifying two different measures, W3-62 uses

```text
Q_C        one conserved collective phase charge,
n_C,F      Q_C density per foundation volume V_F,
n_C,op     Q_C density per operational volume V_op.
```

For the same ideal-comoving reference cell,

```text
V_F/V_F0   = a_F^3,
V_op/V_op0 = A^3,
A          = a_F/p,
p          = a_F^(-3/2),
A          = a_F^(5/2).
```

Consequently, using normalized densities so that no absolute volume
normalization is asserted,

```text
nHat_C,F  := n_C,F/n_C,F0  = a_F^(-3),
nHat_C,op := n_C,op/n_C,op0,
nHat_C,op = p^3 nHat_C,F   = A^(-3).
```

This is one charge read with two volume measures, not two substances. The
direct identity `n_C,op=n_C,F` is valid only at the normalized reference
point and is rejected on an evolving branch. In the W3-54 covariant action,
the old symbol `n_C` is henceforth read as `n_C,op`. In the W3-50 definition
of `eta_F`, it is read as `n_C,F/n_C,F0`.

The background Jacobian is exact. A local inhomogeneous map may be written as
`n_C,op sqrt(h_op)=n_C,F sqrt(h_F)` when the two descriptions refer to the
same local charge element. W3-62 does not introduce an independent local
foundation metric or an additional propagating field; CMB perturbations are
evolved directly with the covariant operational current.

## 3. Once-only CMB source ledger

The CMB specialization of the Einstein equation is

```text
G_mu_nu + Lambda_eff g_mu_nu
  = (8 pi G/c0^4)
    [T_be_mu_nu + T_gamma_mu_nu + T_nu_mu_nu + T_C_mu_nu].
```

The source roles are:

| Source | Role |
|---|---|
| `T_be` | baryon--electron plasma; electron number also supplies opacity, not a second density slot |
| `T_gamma` | the minimally coupled photon/Maxwell sector |
| `T_nu` | one neutrino phase-space sector across relativistic and nonrelativistic regimes |
| `T_C` | the RefG neutral collective phase current, entered once |
| `Lambda_eff` | the one vacuum slot, retained only on the geometric side |

The W3-58 ordinary-core tensor `T_O` is the candidate microscopic
realization of ordinary species. Until a species map is derived it does not
sit beside `T_be`, `T_gamma` or `T_nu` as additional copies of the same
content. A future `T_O -> T_species` bridge replaces the corresponding
effective standard source; it never adds a duplicate source.

The old background aliases become sums:

```text
Omega_r0 = Omega_gamma0 + Omega_nu,rel0,
Omega_m0 = Omega_b0 + Omega_C0 + Omega_nu,nr0 + Omega_other,nr0.
```

`Omega_m0` and `Omega_r0` are not retained as independent entries beside
their components. The following are readouts or geometric bookkeeping and
never additional Hilbert sources: `P_F`, the material factor `p`, clock/ruler
rescaling, metric self-energy, and the internal W3-47 `E_L/E_N/E_R` bins.
The affine vacuum part of `rho_C` is likewise excluded because `Lambda_eff`
already owns the unique vacuum slot.

## 4. W3-54 phase-current source

With `n := n_C,op`, W3-54 gives

```text
p_C(n) = n rho_C'(n) - rho_C(n),
T_C(mu,nu) = [rho_C+p_C] u_mu u_nu + p_C g_mu_nu,
partial_mu J^mu = 0.
```

Its background equations in operational conformal time are

```text
n'     + 3 Hc n                 = 0,
rho_C' + 3 Hc (rho_C+p_C)       = 0,
Hc := A'/A,
w_C := p_C/rho_C,
c_s,C^2 := dp_C/d rho_C
         = n rho_C''(n)/rho_C'(n).
```

The one-potential barotropic source has

```text
delta p_C = c_s,C^2 delta rho_C,
sigma_C   = 0,
```

so it carries no independent entropy mode or intrinsic anisotropic stress.
Photon and neutrino anisotropic stress remains present in their standard
sectors.

## 5. Unique cold phase-current branch

The CMB cold branch is selected by one infrared physical statement:

> On the CMB continuum domain, each conserved unit of operational collective
> phase charge carries a density-independent positive proper energy `mu_C`,
> and no additional vacuum offset is stored in the phase source.

This is the additive fixed-specific-energy limit of the retained conserved
phase action. It opens no fitted exponent or function. It gives

```text
rho_C(n) = mu_C n,      mu_C>0.
```

The branch is unique. From `p_C=0`,

```text
n rho_C'(n)-rho_C(n)=0
  <=> d[rho_C(n)/n]/dn=0
  <=> rho_C(n)=mu_C n.
```

Demanding only `c_s,C^2=0` gives the affine family
`rho_C=mu_C n+C`. Its pressure is `p_C=-C`; the once-only vacuum ledger moves
`C` into `Lambda_eff`, leaving `C=0` in `rho_C`. Hence

```text
w_C=0,
c_s,C^2=0,
sigma_C=0,
rho_C/rho_C0=A^(-3).
```

The W3-54 stability/causality inequalities are satisfied:

```text
rho_C>0,
rho_C'=mu_C>0,
rho_C+p_C=mu_C n>0,
0 <= c_s,C^2 <= 1.
```

`mu_C` fixes the overall cosmological abundance `Omega_C0`; W3-62 derives
the functional form and evolution but does not derive that normalization or
its later relation to the galactic coherence scale `a0`.

## 6. Linear scalar closure

Use the operational conformal-Newtonian convention

```text
ds_op^2=A^2[-(1+2 Psi)d eta^2+(1-2 Phi)d x^2].
```

For `delta_C=delta rho_C/rho_C` and velocity divergence `theta_C`, covariant
conservation gives the exact barotropic system

```text
delta_C'
  = -(1+w_C)(theta_C-3 Phi')
    -3 Hc(c_s,C^2-w_C) delta_C,

theta_C'
  = -Hc(1-3 c_s,C^2) theta_C
    +[c_s,C^2/(1+w_C)] k^2 delta_C
    +k^2 Psi.
```

On the selected cold branch,

```text
delta_C' = -theta_C + 3 Phi',
theta_C' = -Hc theta_C + k^2 Psi.
```

In synchronous gauge the same branch obeys

```text
delta_C' = -theta_C - h'/2,
theta_C' = -Hc theta_C.
```

Choosing coordinates comoving with the irrotational cold phase flow gives
`theta_C=0` and `delta_C'=-h'/2`, exactly the standard Einstein dust system.
The scalar Einstein equations remain

```text
delta G^mu_nu[g_op]
  = (8 pi G/c0^4)
    (delta T_be^mu_nu + delta T_gamma^mu_nu
     + delta T_nu^mu_nu + delta T_C^mu_nu).
```

Thus a Boltzmann solver may use its `cdm` numerical slot as an implementation
alias for `T_C` only when no additional particle-CDM source is active. The
alias changes no ontology and adds no second component.

## 7. Claim contract

- `CLAIM_ID`: `W3_62_CMB_EINSTEIN_SOURCE_LINEAR_CLOSURE`.
- `CLAIM`: On the selected one-metric post-Genesis Einstein continuum, one
  conserved RefG collective phase charge has foundation- and
  operational-volume density representations related by the exact normalized
  Jacobian `nHat_C,op=p^3 nHat_C,F=A^-3`. The once-only source ledger is
  `T_be+T_gamma+T_nu+T_C`, with one geometric `Lambda_eff`. On the selected
  additive fixed-specific-energy infrared branch, the W3-54 barotropic source
  has the unique vacuum-free equation `rho_C=mu_C n_C,op`, and its background
  and linear scalar dynamics are exactly those of pressureless irrotational
  Einstein dust.
- `TYPE`:
  `EXACT_ONE_CHARGE_TWO_MEASURE_AND_LINEAR_EINSTEIN_SOURCE_CLOSURE_ON_SELECTED_FIXED_SPECIFIC_ENERGY_IR_BRANCH`.
- `MODEL_VERSION`: `W3-CMB-v1.0-EINSTEIN-SOURCE-LINEAR-CLOSURE`.
- `ASSUMPTIONS`:
  1. The W3-54 TEGR-equivalent Einstein--Hilbert continuum and one
     operational metric.
  2. The W3-43 operational cosmological metric has scale factor `A` and is
     the metric used in the Einstein--Boltzmann system.
  3. W3-50's conserved `Q_C` is represented on both the selected foundation
     volume and the operational volume of the same normalized comoving cell.
  4. The positive W3-40/W3-47/W3-55 scale branch
     `p=a_F^-3/2`, `A=a_F/p=a_F^(5/2)`.
  5. The W3-54 phase current is minimally coupled and barotropic,
     isentropic and irrotational.
  6. The CMB-domain collective phase sector is on the additive
     fixed-specific-energy branch `rho_C=mu_C n_C,op`, `mu_C>0`.
  7. Standard effective baryon--electron, photon and neutrino sectors couple
     minimally to the same operational metric.
  8. One vacuum slot is carried by `Lambda_eff`; no affine phase-source
     constant is counted again.
- `DOMAIN`: Linear scalar perturbations of the connected, spatially flat,
  post-Genesis operational FLRW continuum; positive scales and densities;
  wavelengths below the homogeneous horizon treatment but above the
  uninstantiated foundation cutoff; pre-recombination through the linear
  late-time regime. Genesis, nonlinear collapse and microscopic species
  construction are outside this gate.
- `CONVENTIONS`: `A_0=a_F0=p_0=1`; prime denotes operational conformal time;
  `Hc=A'/A`; signature `(-+++)`; `n_C,F` and `n_C,op` are density
  representations of one `Q_C`; `T_C` is entered once.
- `FREEDOM_LEDGER`:
  - new fitted functions: zero;
  - new fitted exponents: zero;
  - selected infrared branch: one fixed-specific-energy law
    `rho_C=mu_C n_C,op`;
  - one abundance normalization `Omega_C0` (equivalently the product of
    present charge density and `mu_C`) remains for the CMB forward model;
  - standard CMB species abundances, primordial and reionization parameters
    are not opened here.
- `DEPENDENCIES`:
  - operational FLRW verifier SHA-256
    `57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055`;
  - W3-50 contract SHA-256
    `c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635`;
  - W3-54 contract SHA-256
    `6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879`;
  - W3-55 contract SHA-256
    `a222c494b9ad2d5175b1f746dafa0a90c4d9d858a40a53cd069009614b1be228`;
  - W3-58 summary SHA-256
    `670efde60b6aaea932d972a3f0235a51afe76da322d3e25ec12ffe9291b02c84`.
- `METHOD`: Role audit; normalized two-measure Jacobian; exact barotropic
  identities; zero-pressure uniqueness theorem; background conservation;
  Newtonian- and synchronous-gauge scalar reduction; source-ledger and
  mutation checks; logarithmic-grid numerical smoke test.
- `PASS_CONDITION`: Every exact identity and dependency hash passes; the
  operational density scales as `A^-3`; the vacuum-free cold branch is unique,
  stable and causal; its scalar equations reduce exactly to Einstein dust;
  and every duplicate source and wrong-Jacobian mutation is rejected.
- `FAIL_CONDITION`: The Einstein operator or operational metric is replaced;
  `n_C,F` is equated directly to `n_C,op` on an evolving branch; the Jacobian
  is not `p^3`; an arbitrary EOS function or fitted exponent is introduced;
  a cold branch has nonzero pressure, sound speed or shear; or any source,
  matter alias or vacuum term is counted twice.
- `FALSIFIER`: This branch is rejected if the physical collective phase
  sector has density-dependent proper energy that produces appreciable
  pressure, sound speed, anisotropic stress, decay or nonadiabatic exchange
  across the CMB domain, or if the full CMB spectra cannot be reproduced after
  the Einstein--Boltzmann forward model is implemented.
- `RESIDUAL`: Exact symbolic residuals for scale reconstruction, density
  Jacobian, EOS, conservation, perturbation reduction and mutation controls;
  machine-precision numerical residual on a logarithmic `A` grid.
- `ERROR_BOUND`: Algebraic residual zero. Numerical smoke-test residual must
  be below `5e-13`. No observational error is evaluated in W3-62.
- `VALIDITY_HEALTH`:
  `STABLE_CAUSAL_IRROTIONAL_EINSTEIN_DUST_BRANCH_ON_THE_DECLARED_LINEAR_CONTINUUM_DOMAIN`.
- `BRANCHES`:
  - selected: positive additive fixed-specific-energy cold phase current;
  - retained general comparison: stable causal barotropic `rho_C(n)`;
  - rejected: direct two-measure density identity, duplicate particle CDM,
    affine vacuum duplication and arbitrary phenomenological EOS fitting.
- `OBSERVABLE_MAP`: No CMB spectrum is claimed. W3-62 supplies the source
  module and background/linear transfer equations required by the next
  Einstein--Boltzmann implementation gate.
- `FORWARD_MODEL`: No instrumental or likelihood model. The exact physical
  handoff is `T_C -> pressureless irrotational source` in the standard
  Einstein--Boltzmann system.
- `DATA_ROLE`: `NO_OBSERVATIONAL_DATA_READ_OR_FITTED`.
- `IDENTIFIABILITY`: Linear CMB observables cannot distinguish the selected
  `T_C` branch from particle CDM at equal abundance because both have the same
  Hilbert tensor and transfer equations. RefG becomes distinguishable through
  a derived abundance/galactic link, departures from the cold branch,
  nonlinear response, or independent microphysical observables.
- `BENCHMARK`: Exact recovery of
  `rho_C/rho_C0=A^-3`, `w_C=c_s,C^2=sigma_C=0`, Newtonian dust evolution and
  synchronous-comoving `delta_C'=-h'/2` while the Einstein tensor is unchanged.

### Required true closure flags

```text
REFG_DECLARED_AS_EINSTEIN_EXTENSION
ONE_OPERATIONAL_METRIC_G_OP_WITH_SCALE_A
ONE_QC_TWO_DENSITY_REPRESENTATIONS
FOUNDATION_TO_OPERATIONAL_DENSITY_JACOBIAN_EXACT
DIRECT_DENSITY_IDENTITY_MUTATION_REJECTED
ONCE_ONLY_CMB_SOURCE_LEDGER
UNIQUE_VACUUM_FREE_PHASE_DUST_BRANCH
PHASE_DUST_STABLE_AND_CAUSAL
NEWTONIAN_GAUGE_DUST_REDUCTION_EXACT
SYNCHRONOUS_GAUGE_DUST_REDUCTION_EXACT
EINSTEIN_OPERATOR_UNCHANGED
READY_FOR_EINSTEIN_BOLTZMANN_IMPLEMENTATION
```

### Required false boundary flags

```text
EINSTEIN_GRAVITY_REPLACED
SECOND_OPERATIONAL_METRIC_INTRODUCED
PARTICLE_CDM_ADDED_BESIDE_T_C
RHO_C_MICROSCOPIC_NORMALIZATION_DERIVED
OMEGA_C0_FROM_GALACTIC_A0_DERIVED
RECOMBINATION_BRIDGE_CLOSED
CLASS_IMPLEMENTATION_COMPLETED
CMB_SPECTRA_COMPUTED
CMB_DATA_TESTED
GENESIS_PRIMORDIAL_SPECTRUM_DERIVED
```

## Decision

Passing W3-62 authorizes the next, and only the next, CMB step: implement this
already closed source in the standard Einstein--Boltzmann pipeline, verify
the recombination ratios, and test the spectra. It does not authorize a
second dark source, an arbitrary EOS scan, a modified-gravity response
function, or a CMB compatibility claim before the forward model is run.
