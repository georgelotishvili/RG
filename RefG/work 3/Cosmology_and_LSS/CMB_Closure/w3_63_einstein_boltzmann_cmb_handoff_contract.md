# W3-63 — Einstein–Boltzmann CMB Handoff

## 0. Target and stopping point

RefG reaches the standard CMB initial-value problem on one operational
Einstein metric. The gravitational operator remains the Einstein–Hilbert/TEGR
operator already closed upstream. RefG supplies the physical interpretation
and covariant state of the neutral cold source; the established
Einstein–Boltzmann and atomic-recombination machinery then carries the
calculation forward.

This gate ends when the background, linear scalar, collision, recombination,
and line-of-sight input registries map exactly to their standard counterparts.
It performs no Boltzmann-code run, spectrum calculation, likelihood, data fit,
primordial-spectrum derivation, reionization model, or nonlinear evolution.

## 1. Einstein continuation

The physical CMB metric is

```text
ds_op^2 = A(eta)^2 [-d eta^2 + d x^2],
Hc = A'/A,
```

and its field equation is

```text
G_mu_nu[g_op] + Lambda_eff g_op_mu_nu
  = 8 pi G [T_be_mu_nu + T_gamma_mu_nu + T_nu_mu_nu + T_C_mu_nu]
```

in units `c0=1`. The source-free operator, the metric degrees of freedom, and
the linearized Einstein constraints are exactly those of general relativity.
The RefG extension lies in the foundation origin of `g_op` and `T_C`.

The once-only source ledger is:

| Entry | Physical role |
|---|---|
| `T_be` | baryon–electron plasma, including its ordinary thermal response |
| `T_gamma` | photon/Maxwell phase-space sector |
| `T_nu` | one neutrino distribution across relativistic and nonrelativistic regimes |
| `T_C` | conserved neutral collective phase current |
| `Lambda_eff` | the single homogeneous vacuum slot on the geometric side |

`Omega_r` and `Omega_m` are derived sums:

```text
Omega_r = Omega_gamma + Omega_nu,rel,
Omega_m = Omega_b + Omega_C + Omega_nu,nr + Omega_other,nr.
```

## 2. Frozen upstream bridge

W3-62 gives one conserved collective charge in two volume measures,

```text
n_C,op = p^3 n_C,F,
n_C,op A^3 = constant,
```

and selects the positive fixed-specific-energy branch

```text
rho_C = mu_C n_C,op,
p_C = 0,
c_s,C^2 = 0,
sigma_C = 0,
rho_C = rho_C0 A^(-3).
```

The `cdm` label of a standard solver is therefore a numerical alias for this
collective phase-current state:

```text
rho_cdm   <-> rho_C,
delta_cdm <-> delta_C,
theta_cdm <-> theta_C.
```

It is one source represented by one alias.

## 3. Background handoff

The spatially flat background equations are

```text
Hc^2 = A^2 { (8 pi G/3)
             [rho_b + rho_gamma + rho_nu + rho_C]
             + Lambda_eff/3 },

rho_b'     + 3 Hc rho_b = 0,
rho_gamma' + 4 Hc rho_gamma = 0,
rho_nu'    + 3 Hc (rho_nu + p_nu) = 0,
rho_C'     + 3 Hc rho_C = 0.
```

Thus `rho_b` and `rho_C` dilute as `A^(-3)`, photons as `A^(-4)`, and
massive neutrinos retain their standard phase-space integral rather than being
assigned an extra power law. Photon temperature and redshift obey

```text
T_gamma A = T_gamma0,
1 + z = A0/A,  with A0 = 1.
```

## 4. Linear scalar handoff

Use the standard synchronous scalar decomposition

```text
h_ij = kHat_i kHat_j h
       + 6 (kHat_i kHat_j - delta_ij/3) eta_s.
```

The four scalar Einstein equations are

```text
k^2 eta_s - (Hc/2) h'
  = -4 pi G A^2 delta rho_tot,

k^2 eta_s'
  = 4 pi G A^2 (rho+p)_tot theta_tot,

h'' + 2 Hc h' - 2 k^2 eta_s
  = -24 pi G A^2 delta p_tot,

h'' + 6 eta_s'' + 2 Hc (h' + 6 eta_s') - 2 k^2 eta_s
  = -24 pi G A^2 (rho+p)_tot sigma_tot.
```

For the phase current,

```text
delta_C' = -theta_C - h'/2,
theta_C' = -Hc theta_C.
```

The comoving synchronous choice sets `theta_C=0`, hence

```text
delta_C' = -h'/2.
```

This source contributes density and momentum through the standard Einstein
right-hand side. Its intrinsic pressure perturbation and anisotropic stress
vanish. Photon and neutrino anisotropic stresses retain their standard roles.

## 5. Kinetic species and collision ledger

Each kinetic species satisfies the covariant phase-space equation

```text
Df_s/d eta = C_s[f],
```

on `g_op`. For photons and neutrinos, the usual Legendre hierarchy follows
from this equation. Its generic free-streaming part is

```text
F_s,l' = k/(2l+1) [l F_s,l-1 - (l+1) F_s,l+1]
         + metric source + collision source.
```

The lowest synchronous photon–baryon moments are

```text
delta_b' = -theta_b - h'/2,

theta_b' = -Hc theta_b + c_b^2 k^2 delta_b
           + [4 rho_gamma/(3 rho_b)] kappaDot
             (theta_gamma - theta_b),

delta_gamma' = -(4/3) theta_gamma - (2/3) h',

theta_gamma' = k^2 (delta_gamma/4 - sigma_gamma)
               + kappaDot (theta_b - theta_gamma).
```

The weighted photon and baryon collision momenta cancel exactly. Covariantly,

```text
nabla_mu T_gamma^(mu nu) = C_gamma,b^nu,
nabla_mu T_be^(mu nu)    = -C_gamma,b^nu,
nabla_mu T_C^(mu nu)     = 0,
sum_s C_s^nu             = 0.
```

The collective phase current couples to the plasma gravitationally on this
CMB branch.

## 6. Operational atomic and recombination handoff

The low-energy operational branch carries the standard locally measured
dimensionless matter/QED ratios into the CMB epoch. The common foundation
scale is already contained in the operational metric and cancels from

```text
Theta_gamma = k_B T_gamma/E_atom,
N_H         = n_H l_atom^3,
Sigma_T     = sigma_T/l_atom^2,
R_i         = Gamma_i/H_A.
```

These quantities, together with `alpha`, mass ratios, dimensionless binding
energies, branching ratios, and atomic rate ratios, are the arguments of the
standard atomic kernel. The recombination handoff is therefore

```text
T_gamma = T_gamma0/A,
n_H     = n_H0 A^(-3),
n_e     = x_e n_H,

x_e' = A F_atom^std(x_e,T_gamma,T_b,n_H;
                    alpha,m_e,mass ratios,...),

T_b' = -2 Hc T_b + A Gamma_Compton^std (T_gamma-T_b),

kappaDot = A n_e sigma_T,
kappa(eta) = integral_eta^eta0 kappaDot(etaBar) d etaBar,
g_vis = kappaDot exp(-kappa).
```

`F_atom^std` denotes the established Saha-to-nonequilibrium multilevel-atom
rate system. All quantities in these equations are operational. Their final
forms contain `A`, `eta`, local densities, and local microphysical ratios; the
foundation coordinates `a_F` and `p` have completed their geometric role
before this handoff.

## 7. Initial transfer mode and final CMB endpoint

The standard adiabatic unit transfer mode is admitted as the initial condition:

```text
delta_C = delta_b = (3/4) delta_gamma = (3/4) delta_nu,
S_ij = 3 (zeta_i-zeta_j) = 0
```

on the super-horizon initial boundary. Its primordial amplitude and scale
dependence enter through `P_R(k)`.

Once the system above is evolved, the standard line-of-sight endpoint is

```text
Delta_l^X(k,eta0)
  = integral_0^eta0 d eta S_X(k,eta)
    j_l[k(eta0-eta)],

C_l^(XY)
  = 4 pi integral d ln k P_R(k)
    Delta_l^X(k) Delta_l^Y(k).
```

This is the requested handoff point. Every quantity needed by the established
CMB calculation has reached its standard Einstein–Boltzmann form.

## 8. Claim contract

- `CLAIM_ID`: `W3_63_EINSTEIN_BOLTZMANN_CMB_HANDOFF`.
- `CLAIM`: On the pinned W3-54/W3-62 branch and the declared operational
  low-energy matter/QED branch, RefG maps exactly to the standard spatially
  flat Einstein–Boltzmann–recombination starting system under
  `A <-> a_EB` and `T_C <-> T_cdm`. The line-of-sight spectrum equations then
  receive the standard source functions.
- `TYPE`: `CONDITIONAL_EXACT_DICTIONARY_AND_SOURCE_CLOSURE`.
- `MODEL_VERSION`: `W3-CMB-v1.1-EINSTEIN-BOLTZMANN-HANDOFF`.
- `ASSUMPTIONS`:
  1. the pinned W3-54 Einstein/TEGR and W3-62 phase-source closures pass;
  2. the post-Genesis CMB continuum is spatially flat and linear;
  3. standard matter, Maxwell, neutrino, and local atomic/QED physics are
     minimally coupled to the one operational metric;
  4. local dimensionless atomic/QED ratios keep their standard values on the
     selected low-energy operational branch;
  5. `T_C` is the W3-62 positive cold, shear-free, gravity-only branch;
  6. the primordial transfer seed is standard adiabatic input.
- `DOMAIN`: homogeneous background plus linear scalar perturbations through
  recombination and the formal line-of-sight endpoint.
- `CONVENTIONS`: `c0=1`; prime is `d/d eta`; `Hc=A'/A`; `kappaDot>0` is the
  positive Thomson scattering rate; `kappa(eta)` integrates from emission to
  observation; `A0=1`.
- `FREEDOM_LEDGER`: No new CMB function or fitted coefficient is introduced.
  `Omega_C0` is the normalization of the phase source. `Omega_m` and `Omega_r`
  are derived sums. `T_gamma0` fixes the photon density, and the baryon
  normalization fixes the hydrogen density once composition is specified.
  Primordial and late-reionization parameters belong to the standard forward
  model beyond this gate.
- `DEPENDENCIES`: W3-54, W3-62, the operational FLRW completion, and W3-43's
  one-metric photon/atomic endpoint map, all hash-pinned by the verifier.
- `METHOD`: Construct the RefG and canonical Einstein–Boltzmann registries
  independently, apply the declared one-to-one dictionary, demand zero
  symbolic residuals, verify collision conservation and operational scale
  cancellation, and reject registered mutations.
- `PASS_CONDITION`: Dependency integrity; exact metric/operator and source
  keysets; zero background, linear-dust, source, collision, thermal-scale,
  opacity, adiabatic, and endpoint dictionary residuals; and rejection of all
  duplicate-source, second-metric, modified-operator, wrong-scale, extra-`p`,
  non-cold-source, and collision-sign mutations.
- `FAIL_CONDITION`: Any pinned dependency fails; the canonical mapping needs a
  second metric or modified Einstein operator; `T_C` fails the cold conserved
  source equations; the source/collision ledger double-counts a sector; an
  operational CMB equation retains `a_F` or `p`; or the standard recombination
  and line-of-sight inputs cannot be written in the operational variables.
- `FALSIFIER`: A nonzero exact residual in the declared dictionary, unavoidable
  nonstandard local dimensionless atomic physics, unavoidable direct
  phase–photon scattering, or an additional gravitational degree of freedom
  required within this domain.
- `RESIDUAL`: Exact symbolic/structural residuals written by the verifier.
- `ERROR_BOUND`: Zero for symbolic identities and exact keysets; numerical
  CMB errors are `N/A` because no spectrum is computed.
- `VALIDITY_HEALTH`: Positive background densities and opacity, conserved
  total collision transfer, stable cold phase source, one metric, and a finite
  once-only source ledger.
- `BRANCHES`: Selected: expanding `A>0`, positive phase density, standard local
  operational matter/QED ratios, and adiabatic unit transfer mode. Mutation
  branches are recorded only as negative controls.
- `OBSERVABLE_MAP`: The standard source functions `S_X` and transfer functions
  `Delta_l^X` feed the formal `C_l` endpoint.
- `FORWARD_MODEL`: Standard Einstein–Boltzmann plus established recombination
  and line-of-sight integration, with the solver's cold slot interpreted as
  `T_C`.
- `DATA_ROLE`: `NO_OBSERVATIONAL_DATA_READ_OR_FITTED`.
- `IDENTIFIABILITY`: At equal source normalizations and primordial inputs, the
  W3-62 cold phase branch is linearly CMB-degenerate with the standard cold
  Einstein source because their Hilbert stress and evolution equations agree.
- `BENCHMARK`: Ma & Bertschinger's linear Einstein–Boltzmann system, CLASS's
  standard solver architecture, and HyRec's standard recombination kernel.
- `CROSSCHECK`: Independent background/source, collision-momentum,
  operational-scale, synchronous-dust, and line-of-sight registry checks.
- `PROVENANCE`: Dependency and script hashes are written to deterministic JSON.
- `FILES`: this contract, verifier, result JSON, and result checksum in
  `Cosmology_and_LSS/CMB_Closure`.

Required true closure flags:

```text
REFG_EINSTEIN_CONTINUATION_EXACT
ONE_OPERATIONAL_METRIC_A_EXACT
EH_OPERATOR_INHERITED_EXACT
W3_62_PHASE_DUST_INHERITED_EXACT
FINITE_ONCE_ONLY_SOURCE_LEDGER_EXACT
BACKGROUND_EINSTEIN_BOLTZMANN_DICTIONARY_EXACT
LINEAR_SCALAR_EINSTEIN_DICTIONARY_EXACT
PHOTON_BARYON_COLLISION_TRANSFER_CANCELS_EXACT
STANDARD_NEUTRINO_HIERARCHY_INHERITED_EXACT
OPERATIONAL_ATOMIC_RATIOS_SCALE_FREE_EXACT
RECOMBINATION_OPACITY_HANDOFF_EXACT
ADIABATIC_UNIT_TRANSFER_MODE_COMPATIBLE_EXACT
STANDARD_LINE_OF_SIGHT_ENDPOINT_REGISTERED_EXACT
ALL_REGISTERED_MUTATIONS_REJECTED
EINSTEIN_BOLTZMANN_CMB_HANDOFF_CLOSED
```

Required false boundary flags:

```text
MODIFIED_GRAVITY_OPERATOR_INTRODUCED
SECOND_OPERATIONAL_METRIC_INTRODUCED
PARTICLE_CDM_ADDED_BESIDE_T_C
FOUNDATION_ATOMIC_QED_RATIOS_DERIVED
PRIMORDIAL_SPECTRUM_DERIVED
REIONIZATION_MODEL_COMPLETED
BOLTZMANN_CODE_RUN
CMB_SPECTRA_COMPUTED
CMB_DATA_READ
CMB_OBSERVATIONAL_PASS
```

Successful status:

```text
PASS_CONDITIONAL_EXACT_REFG_TO_STANDARD_EINSTEIN_BOLTZMANN_RECOMBINATION_AND_LINE_OF_SIGHT_HANDOFF__CMB_FORWARD_CALCULATION_INHERITED
```

## 9. Reference anchors

- C.-P. Ma and E. Bertschinger, *Cosmological Perturbation Theory in the
  Synchronous and Conformal Newtonian Gauges*, Astrophysical Journal 455
  (1995), arXiv:astro-ph/9506072.
- J. Lesgourgues, *The Cosmic Linear Anisotropy Solving System (CLASS) I:
  Overview* (2011), arXiv:1104.2932.
- Y. Ali-Haïmoud and C. M. Hirata, *HyRec: A Fast and Highly Accurate
  Primordial Hydrogen and Helium Recombination Code*, Physical Review D 83
  (2011), arXiv:1011.3758.
