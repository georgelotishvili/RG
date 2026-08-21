# Work 3 Cosmology and LSS Ledger

## Current account

W3-40 is the current causal-lock root for the cosmology branch. On the
selected mean Hubble-flow branch, a fixed comoving link count and a growing
foundation link length define the primary expansion. That expansion relaxes
the mean foundation pressure, while

```text
p^2 = P_F/P_F0
```

translates the pressure fall into contraction of the material scale-and-
cadence factor. An internal observer reads this one trajectory through
`A=a/p`. Before a constitutive closure is supplied, that observable ratio
does not identify `a` and `p` separately.

W3-40 passes the exact causal dictionary, linked sign/rate identities, and
the `A`-only non-identifiability check. It freezes `dP_F/da<0` as the selected
constitutive sign; it does not derive the law `P_F(a)`. At the W3-40 gate,
the foundation energy balance, complete histories `a(t)`, `P_F(t)`, and
`p(t)`, photon--atomic map, `H_CC(z)`, `D_L(z)`, CMB/BBN calculation,
and JWST growth model therefore remain open.

W3-41 is the constitutive-interface child of W3-40. It derives the exact
`E_F`--`Pi_F` mechanical-stress dictionary and proves a reconstruction
nonselection theorem: the interface admits an entire functional family and
therefore selects no physical `P_F(a)`, `kappa(a)`, or exponent. The identity
`P_F=Pi_F` is only a candidate mechanical bridge in that gate and is not
used by the selected density closure below. The cell-volume law and
one-coordinate state reduction are assumptions at W3-41.

W3-42 is the state-space and volume-map child. It derives the exact
conditional theorem

```text
mathcal_V/mathcal_V_0 = det(F)
F=a I_d  =>  mathcal_V=mathcal_V_0 a^d
```

and recovers the W3-41 cubic dictionary at `d=3`. Its constructive witnesses
prove that the existing foundation account selects neither physical
dimension, measure, isotropy, nor a one-coordinate homogeneous state:

- three equal link lengths can have a changing angle and a noncubic volume;
- one fixed graph supports measures scaling as `a^0`, `a^1`, and `a^3`;
- a trace-free shape coordinate can survive behind the same cubic volume;
- activated volume also depends on the independently open active-cell
  measure.

For the present cosmology objective, the observed homogeneous-isotropic
`d=3` geometry is retained as an explicit effective input. A microscopic
derivation of dimension and topology is a separate research program and is
not an automatic next stage.

## Selected post-W3-42 density closure

### Closure contract

- `CLAIM_ID`: `W3_COSMOLOGY_CONSERVED_RELAXATION_DENSITY_CLOSURE`.
- `CLAIM`: on the selected branch, conservation of `Q_rel=P_F mathcal_V`
  and `mathcal_V/mathcal_V_0=a^3` fixes `P_F/P_F0=a^(-3)` and all exact
  relational consequences below.
- `TYPE`: `AUTHOR_SELECTED_CONSTITUTIVE_POSTULATE_WITH_EXACT_CONSEQUENCES`.
- `MODEL_VERSION`: `W3-COSMOLOGY-v1.0-CONSERVED-RELAXATION-DENSITY`;
  changing the conserved content, density readout, cubic effective-volume
  input, cadence bridge, or branch domain creates a new version.
- `ASSUMPTIONS`: positive normalized scales; an already-connected
  homogeneous-isotropic effective `d=3` branch; one fixed ideal-comoving
  domain; conserved positive `Q_rel`; `P_F=Q_rel/mathcal_V`; and the frozen
  cadence bridge `p^2=P_F/P_F0`.
- `DOMAIN`: regular post-origin intervals after network connection; not the
  Genesis transition, a moving activation boundary, or a local compact-object
  deficit.
- `CONVENTIONS`: `a_0=p_0=A_0=1`; `tau` is process time; `mathcal_V` is
  physical foundation volume of the fixed comoving domain; `P_F` is a
  density-like cadence state and is not silently identified with `Pi_F`.
- `FREEDOM_LEDGER`: the density law has no fitted exponent or free function.
  The complete homogeneous constraint remains open and must finitely register
  its operational source sectors, curvature branch `k`, cosmological term
  `Lambda`, expanding/contracting branch, and one normalization or initial
  datum. The universal history `a(t)` and all photon--atomic and
  source-response maps remain open.
- `DEPENDENCIES`: the frozen W3-40 causal dictionary, W3-41 mechanical
  nonselection result, and W3-42 effective `d=3` volume branch.
- `METHOD`: exact substitution, logarithmic differentiation, inverse
  substitution, and a direct audit against the retained W3-36 benchmark; no
  data and no likelihood.
- `PASS_CONDITION`: every displayed relational identity and inverse has zero
  symbolic residual, the branch preserves the single-driver causal order,
  and no frozen gate is retroactively changed.
- `FAIL_CONDITION`: a nonzero algebraic residual, silent use of
  `P_F=Pi_F`, application across changing activation content, or promotion
  of an uncomputed `a(t)` or observable map.
- `FALSIFIER`: within the declared domain, a derived nonzero source for
  `Q_rel`, failure of `P_F mathcal_V=constant`, or failure of the adopted
  cubic effective-volume law.
- `RESIDUAL`: exact symbolic zero for the density, cadence, operational-scale,
  inversion, `kappa=3`, and `q=-1/3` identities.
- `ERROR_BOUND`: zero algebraic error; numerical and observational error are
  N/A because no numerical approximation or data are used.
- `VALIDITY_HEALTH`: the consequences are exact under the selected postulate;
  conservation of `Q_rel` is selected rather than derived from a foundation
  action, and time evolution and observables remain open.
- `BRANCHES`: conserved-density branch selected; W3-41's mechanical
  `P_F=Pi_F` bridge unused; W3-36's regular same-null-front `D>0` branch
  excluded because this closure gives `D=0`.
- `OBSERVABLE_MAP`: `A=a/p` is the current ideal relational readout; no
  identification with spectroscopic redshift is made here.
- `FORWARD_MODEL`: N/A until `a(t)`, photon propagation, atomic response,
  source evolution, and measurement likelihood are supplied.
- `DATA_ROLE`: no data are read or fitted.
- `IDENTIFIABILITY`: the closure removes the W3-40 `A`-only degeneracy via
  `a=A^(2/5)`, `p=A^(-3/5)`, and `P_F/P_F0=A^(-6/5)`.
- `BENCHMARK`: exact recovery of the W3-40 scale identities and the
  independent W3-36 consequence `q=-1/3`, `D=0`.
- `CLOSURE_FLAGS`: `density_closure_selected=true`,
  `P_F_of_a_fixed=true`, `A_inversion_exact=true`,
  `Q_rel_microdynamics_derived=false`, `a_of_t_derived=false`, and
  `observable_forward_model_derived=false`.
- `CROSSCHECK`: direct exponent algebra and inverse substitution agree; the
  W3-36 incompatibility is obtained independently from `D=1+3q`.
- `PROVENANCE`: author-selected on 2026-08-22; no external data; frozen
  W3-40/41/42 preregistrations, scripts, results, and checksums unchanged.
- `FILES`: this README is canonical; the W3-40, W3-41, and W3-42 READMEs
  carry synchronized downstream-status notes.

For the already-connected, homogeneous-isotropic post-origin branch, RefG now
adopts one physical closure. A fixed ideal-comoving foundation domain carries
an extensive conserved relaxation/coherence content `Q_rel`; the cadence-
controlling scalar `P_F` is its density in the domain's physical foundation
volume:

```text
Q_rel := P_F mathcal_V
dQ_rel/dtau = 0
mathcal_V = mathcal_V_0 a^3
```

With `a_0=1`, this gives the exact, parameter-free relations

```text
P_F/P_F0 = a^(-3)
kappa = -d ln(P_F)/d ln(a) = 3
p = sqrt(P_F/P_F0) = a^(-3/2)
A = a/p = a^(5/2)
```

The exponent `3` is not fitted: it is the volume exponent of the explicitly
selected effective three-dimensional homogeneous-isotropic branch. `Q_rel`
is the conserved content whose density is read as `P_F`; it is not W3-41's
mechanical potential `E_F`. Consequently this closure neither assumes nor
needs `P_F=Pi_F`, where `Pi_F=-dE_F/dV_F`.

This also collapses W3-40's downstream `A`-only equivalence class:

```text
a = A^(2/5)
p = A^(-3/5)
P_F/P_F0 = A^(-6/5)
```

The law applies only after the network is already connected and to a fixed
ideal-comoving content. It does not assert conserved active-domain energy at
the Genesis transition or across a moving activation boundary, where source,
flux, and changing active-cell terms remain necessary. Within its stated
domain, a nonzero source for `Q_rel`, failure of `P_F mathcal_V=constant`, or
failure of the selected cubic effective-volume law falsifies this closure.

The closure fixes `P_F(a)`, `p(a)`, and `A(a)`. It does not yet determine
the time history `a(t)`; that requires one expansion equation. It also does
not by itself supply the photon--atomic observable map.

### Bounded expansion-dynamics audit

Let a prime denote `d/dtau` and define
`H_a^(tau)=a'/a`. The selected density closure gives

```text
P_F' + 3 H_a^(tau) P_F = 0
H_A^(tau) = (1/A) dA/dtau = (5/2) H_a^(tau)
```

These are conservation and scale identities. They hold for every positive
differentiable history `a(tau)` and therefore do not determine expansion.

The strongest existing dynamical shell is RefG's
[conditional low-energy Einstein--Hilbert/EFE architecture](../Lagrangian_Formulation/RefG_Formal_Proof.md),
combined with the
[W3-36 metric dictionary](w3_36_birth_threshold_thermal_preregistration.md).
For a homogeneous isotropic operational FLRW completion it gives

```text
[H_A^(tau)]^2 =
    (8 pi G/(3 c0^2)) epsilon_eff(A)
    + Lambda c0^2/3
    - k c0^2/A^2
```

Here `epsilon_eff` is operational effective energy density. Because `A` is
dimensionless, `[k]=L^(-2)`; `k>0` denotes positive operational spatial
curvature and contributes with the displayed minus sign. Likewise,
`[Lambda]=L^(-2)`, and `Lambda>0` raises `[H_A^(tau)]^2`. The spatially flat
W3-36 specialization has `k=0`.
Substituting `A=a^(5/2)` gives the exact foundation-scale interface

```text
(25/4) (a'/a)^2 =
    (8 pi G/(3 c0^2)) epsilon_eff(a^(5/2))
    + Lambda c0^2/3
    - k c0^2/a^5
```

Since `d tau=p dt=a^(-3/2)dt`, the same constraint in coordinate time is

```text
(25/4) a (da/dt)^2 =
    (8 pi G/(3 c0^2)) epsilon_eff(a^(5/2))
    + Lambda c0^2/3
    - k c0^2/a^5
```

This interface is not yet a closed prediction for `a(t)`. Exactly one complete
dynamical object is missing: a homogeneous source-coupled Hamiltonian
constraint (or equivalent minisuperspace action), schematically

```text
C_hom[a, a'; Q_rel, T_matter, T_radiation; k, Lambda] = 0
```

This one object must define how `Q_rel` and each finitely registered material
or radiative sector supply `epsilon_eff` and isotropic stress; select `k` and
`Lambda`; select the expanding or contracting sign; and state one
normalization or initial datum. No unnamed `...` source sector is permitted:
adding a further sector creates a new registered version. `P_F` cannot be
inserted as effective energy density merely because it has energy-density
units, and `Q_rel` cannot be inserted as mechanical energy after it has been
separated from `E_F` and `Pi_F`. Until this complete constraint is physically
supplied, no particular `a(t)`, Friedmann component history, or acceleration
claim is selected. The expansion-dynamics status is therefore `OPEN` at this
exact premise, and no additional calculation stage is opened.

W3-36 remains the bookkeeping root for the finite-origin, process-time,
metric, thermal, and local-threshold identities. Version 1.3 removes its old
independent scale-split diagnostic and preserves the exact `A=a/p` dictionary.
W3-40 supplies the active single-driver interpretation: foundation expansion
is primary, while pressure relaxation and material contraction are dependent
stages of that one trajectory.

One exact thermal result is already decisive for future work. On the
adiabatic radiation branch, Q_gamma=0 gives T A=constant; with the
conditional map 1+z=A0/Ae, this is the standard T_e=T_today(1+z) law.
Faster cadence alone cannot produce a lower temperature. A different
temperature requires a derived source history, equation of state, or
non-universal sector response.

## Salvaged exact results

W3-36 checks the useful metric, process-time, null-ray, radius, and volume
identities inside one self-contained symbolic artifact.

It also preserves a conditional-front assumption-consequence check. Under
the hypothetical constant-energy, spherical-volume, same-null-front closure,
define q=d ln a/d ln P_F and D=1+3q:

- D dR/dt=c0 p^2;
- d tau/dR=D/(c0 p);
- for 0<D<1 and p>=1, 0<Delta tau<R_final/c0;
- only the constant-D=D0>0, constant-q sub-branch has p proportional to
  t^(-3/8) and elapsed process time 8 T0/5.

This calculation is a conditional consistency benchmark. Its closure has not
been derived, and its local radial front is not the global birth geometry.
The selected density closure gives `q=-1/3` and therefore `D=0`; it is
incompatible with the benchmark's regular `D>0` same-null-front branch and
with `D dR/dt=c0 p^2` for positive `p`. That branch is consequently
excluded from the current cosmology and retained only as a historical
assumption--consequence check.
The source snapshots were removed after these valid results were made
self-contained in W3-36.

## Retired branch evidence

The superseded exploratory branches were removed from the active tree. They
encoded a superseded total-age postulate, an unresolved ruler note, a
stationary a=1 branch, an exploratory observational test, a superseded
requirements draft, and an arbitrary power-law fit. None is an input to
W3-36.

The strongest negative result from the strict stationary branch is preserved
here as an archival audit record, not as a reproducible gate. The removed
exploratory source/result were not provenance-complete, and W3-36 does not
depend on these numbers. Conditional on that branch's luminosity-distance
map, the 40-bin Pantheon comparison with the full supplied covariance gave:

- chi2_STB=401.0154718937386;
- chi2_LCDM=40.021348345228716;
- Delta_chi2=360.9941235485099;
- p_STB=1.2851783751590529e-61;
- 39 degrees of freedom.

For the branch's correctly transformed physical-clock chronometer
prediction, a fixed constant H_CC=1/T0 gave:

- chi2_STB=182.4119037277066;
- chi2_LCDM=14.872777476363384;
- p_STB=9.142349049942303e-24;
- 30 degrees of freedom.

These numbers reject the strict stationary observable map, not RefG as a
whole. Future derivations must not silently reduce to a=1, H_CC=constant,
or D_L proportional to z(1+z).

## Retained data

lcparam_DS17f.txt and sys_DS17f.txt are retained as the canonical local
Pantheon inputs for a future preregistered observable test. They do not
constitute a current RefG fit.
