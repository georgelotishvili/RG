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
  The conditional operational background completion below adds no exponent or
  free function and registers all of its finite inputs. Numerical background
  parameters, Genesis matching, and all photon--atomic and source-response maps
  remain open.
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
  action. The density closure alone supplies no time evolution; the separate
  conditional operational completion below supplies its leading-EFT equation.
- `BRANCHES`: conserved-density branch selected; W3-41's mechanical
  `P_F=Pi_F` bridge unused; W3-36's regular same-null-front `D>0` branch
  excluded because this closure gives `D=0`.
- `OBSERVABLE_MAP`: `A=a/p` is the current ideal relational readout; no
  identification with spectroscopic redshift is made here.
- `FORWARD_MODEL`: N/A until the finite background inputs, photon propagation,
  atomic response, source evolution, and measurement likelihood are supplied.
- `DATA_ROLE`: no data are read or fitted.
- `IDENTIFIABILITY`: the closure removes the W3-40 `A`-only degeneracy via
  `a=A^(2/5)`, `p=A^(-3/5)`, and `P_F/P_F0=A^(-6/5)`.
- `BENCHMARK`: exact recovery of the W3-40 scale identities and the
  independent W3-36 consequence `q=-1/3`, `D=0`.
- `CLOSURE_FLAGS`: `density_closure_selected=true`,
  `P_F_of_a_fixed=true`, `A_inversion_exact=true`,
  `Q_rel_microdynamics_derived=false`,
  `a_of_t_from_density_closure_alone=false`, and
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

The closure fixes `P_F(a)`, `p(a)`, and `A(a)`. By itself it supplies no time
history; the conditional operational completion below provides the expansion
equation. The photon--atomic observable map remains a separate closure.

### Conditional operational geometric completion

#### Dynamics contract

- `CLAIM_ID`: `W3_COSMOLOGY_OPERATIONAL_GEOMETRIC_FLRW_COMPLETION`.
- `CLAIM`: on the leading two-derivative operational EFT branch, one conserved
  nonrelativistic defect sector, one adiabatic radiation sector, the selected
  spatially flat branch, the Einstein--Hilbert `Lambda` term, and the expanding
  sign give a closed first-order background equation for `A`, whose exact
  pullback determines `a`, `p`, and `P_F` histories for finite supplied inputs.
- `TYPE`: `CONDITIONAL_EFFECTIVE_EFT_COMPLETION_WITH_EXACT_PULLBACK`.
- `MODEL_VERSION`: `W3-COSMOLOGY-v1.0-OPERATIONAL-GEOMETRIC-FLRW`; changing the
  effective action, source list, material energy channel, transfer law,
  curvature branch, `Lambda` branch, or scale/time dictionary creates a new
  version.
- `ASSUMPTIONS`: the conditional low-energy Einstein--Hilbert/EFE shell; the
  W3-36 operational metric; the selected `A=a^(5/2)`, `p=a^(-3/2)` closure;
  minimally coupled conserved Noether/proper energy for nonrelativistic
  localized defects; the W3-36 `Q_gamma=0` radiation specialization selected
  here; `k=0`; constant `Lambda`; and the W3-40 expanding branch.
- `DOMAIN`: a connected interval containing `A=1` on the already-connected
  homogeneous-isotropic post-Genesis branch, with `A>0`, `H_A0>0`,
  `Omega_m0>=0`, `Omega_r0>=0`, and `E(A)^2>0` throughout; below the cutoff
  where omitted higher-derivative EFT terms matter; and with no net energy
  transfer between the registered source sectors and the foundation.
- `CONVENTIONS`: `A_0=a_0=p_0=1`; prime is `d/dtau`, dot is `d/dt`;
  `d tau=p dt`; `H_A=(1/A)dA/dtau`; energy density has units of energy per
  operational volume; `[Lambda]=L^(-2)`; and the positive square root is the
  expanding branch.
- `FREEDOM_LEDGER`: there is no fitted function or exponent. The finite
  universal background inputs are `H_A0`, `Omega_m0`, and `Omega_r0`, with
  `Omega_Lambda0=1-Omega_m0-Omega_r0` on `k=0`; an additive time origin is a
  coordinate choice. The numerical inputs, the physical post-Genesis endpoint
  of the EFT interval, and the photon--atomic forward map remain open.
- `DEPENDENCIES`: the selected density closure above, W3-36's metric and
  `Q_gamma=0` identities, W3-40's expanding causal branch, and RefG's
  conditional low-energy Einstein--Hilbert/EFE architecture.
- `METHOD`: the `00` Einstein equation and an independent lapse variation of
  the same registered effective action, covariant source conservation, exact
  normalization, and substitution of `A=a^(5/2)` and
  `d tau=a^(-3/2)dt`. Both dynamical routes share the declared effective action
  and source map.
- `PASS_CONDITION`: the Hamiltonian constraint, both continuity laws, normalized
  sum rule, scale pullback, and time-coordinate pullback have zero algebraic
  residual; the lapse and `00` routes agree; differentiating the constraint
  with both continuity laws recovers the spatial Einstein equation; both
  implicit solutions differentiate back to their ODEs; and every source and
  freedom is registered.
- `FAIL_CONDITION`: nonconservation on the declared no-transfer branch,
  counting the cadence readout again as a source, using the refractive
  `m_eff` factor as a second energy scaling, a nonzero curvature term, an
  unregistered source, or a nonzero exact residual.
- `FALSIFIER`: a derived RefG source map in which the conserved operational
  gravitational energy is not the Noether/proper channel, a required nonzero
  transfer law, or unsuppressed higher-derivative terms in the stated domain
  falsifies this branch.
- `RESIDUAL`: exact symbolic zero for the lapse/`00` constraint agreement,
  both continuity laws, Hamiltonian normalization, `Omega` sum rule, spatial
  Einstein consistency equation, `A`-to-`a` pullback, `tau`-to-`t` pullback,
  and both implicit-history derivatives; exact key-set equality for the finite
  source registry and freedom ledger.
- `ERROR_BOUND`: zero algebraic error inside the displayed truncated model;
  the EFT truncation error is `OPEN` until a microscopic cutoff and
  higher-order coefficients are supplied.
- `VALIDITY_HEALTH`: the registered Einstein--Hilbert dust--radiation system
  is covariantly conserved and uses one geometric readout of foundation
  relaxation. The foundation action and the microscopic value of `Lambda`
  remain underived.
- `BRANCHES`: flat, expanding, leading-EH, no-transfer branch selected;
  `Q_rel` and `P_F` occupy the cadence/geometry dictionary, while localized
  Noether/proper energy and radiation occupy the operational source tensor.
- `OBSERVABLE_MAP`: `A` is the ideal operational scale. Its identification
  with spectroscopic redshift or a measured Hubble history remains open.
- `FORWARD_MODEL`: N/A until the photon, atomic, source, selection, and
  likelihood maps are supplied.
- `DATA_ROLE`: no data are read or fitted; the finite inputs are uncalibrated.
- `IDENTIFIABILITY`: supplied finite inputs fix the background ODE on each
  connected interval with `E(A)^2>0`; an additive time origin fixes its
  coordinate placement. This stage does not infer the inputs from observations.
- `BENCHMARK`: standard flat dust--radiation--`Lambda` FLRW evolution in `A`,
  followed by the exact RefG scale and time pullbacks.
- `CLOSURE_FLAGS`: required `true` are
  `operational_constraint_selected`, `operational_source_map_selected`,
  `finite_source_registry_complete`, `finite_freedom_ledger_complete`,
  `lapse_00_constraint_agreement_exact`, `matter_continuity_exact`,
  `radiation_continuity_exact`, `Hamiltonian_constraint_normalization_exact`,
  `Omega_sum_rule_exact`, `spatial_Einstein_consistency_exact`,
  `scale_pullback_exact`, `time_coordinate_pullback_exact`,
  `implicit_history_derivatives_exact`,
  `a_of_tau_equation_derived_within_conditional_EFT`, and
  `a_of_t_equation_derived_within_conditional_EFT`; required `false` are
  `operational_source_map_microphysically_derived`,
  `foundation_hamiltonian_derived`, `EFT_truncation_controlled`,
  `Lambda_value_derived`, `Genesis_matching_derived`,
  `numerical_history_fixed`, and `observable_forward_model_derived`.
  `conditional_background_pass` is the logical `AND` of every required-true
  flag and the negation of every required-false flag.
- `CROSSCHECK`: derive the Hamiltonian constraint from the `00` EFE and from
  lapse variation of the reduced action; recover both source powers from their
  continuity laws; compare the direct spatial EFE with the result of
  differentiating the constraint; verify both RefG pullbacks and both implicit
  histories by direct differentiation.
- `DECISION_STATUS`: `PASS_CONDITIONAL_BACKGROUND_EQUATION__MICROPHYSICS_PARAMETERS_AND_OBSERVABLES_OPEN`.
- `PROVENANCE`: registered on 2026-08-22 following the author's geometric RefG
  clarification and the retained conditional EFT architecture; the versioned
  exact verifier `w3_cosmology_operational_geometric_flrw.py` passes with
  Python 3.10.6 and SymPy 1.13.3; its source SHA-256 is
  `57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055`.
  It reads no external data, fits nothing, writes no files, and emits its
  deterministic JSON report to standard output; frozen W3-36/40/41/42
  artifacts remain unchanged.
- `FILES`: this README records the completion; the
  [exact symbolic verifier](w3_cosmology_operational_geometric_flrw.py)
  reproduces its registered residuals and closure flags; `RefG_Formal_Proof.md`
  and the W3-36 preregistration provide its unchanged upstream EFT and metric
  inputs.

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
`[Lambda]=L^(-2)`, and `Lambda>0` raises `[H_A^(tau)]^2`. W3-36 supplies the
metric/time dictionary but does not select global spatial curvature; `k=0` is
the separate effective branch selected in the completion below.
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

RefG's refractive field is the operational geometry. The minimum completion
uses one metric action, with foundation relaxation appearing once through the
metric dictionary:

```text
S_op = [c0^3/(16 pi G)] int d^4x sqrt(-g) (R-2 Lambda)
       + S_m[g,psi_m] + S_r[g,psi_r] + S_boundary

G_mn + Lambda g_mn = (8 pi G/c0^4) (T_mn^m + T_mn^r)
```

Here `x^0=c0 tau`, and `S_boundary` is the standard Gibbons--Hawking--York
fixed-boundary term. The material tensor uses the conserved Noether/proper
energy of localized nonrelativistic defects, the same invariant energy channel
that supplies inertial and gravitational charge. The factor `m_eff/m_0=p` is
its external refractive readout and is already represented by the metric
dictionary. `Q_rel` and `P_F` complete their role through `p(a)` and `A(a)`.
The operational source tensor in this model version consists exactly of the
registered localized-defect and radiation sectors.

The independent homogeneous variation keeps the lapse until after variation:

```text
ds_op^2 = N(lambda)^2 c0^2 d lambda^2 - A(lambda)^2 d chi^2

S_red/V_c = int d lambda {
    - [3 c0^2/(8 pi G)] [A/N] (dA/dlambda)^2
    - N A^3 [epsilon_m + epsilon_r + Lambda c0^4/(8 pi G)]
}
```

The source term is the reduced matter Hamiltonian form. Varying `N`, then
setting `N=1` and `lambda=tau`, gives exactly the displayed flat `00`
Hamiltonian constraint.

On the registered no-transfer branch,

```text
P_m = 0
P_r = epsilon_r/3
epsilon_m' + 3 H_A^(tau) epsilon_m = 0
epsilon_r' + 4 H_A^(tau) epsilon_r = 0

epsilon_m = epsilon_m0 A^(-3)
epsilon_r = epsilon_r0 A^(-4)
```

The completion selects the spatially flat branch `k=0`. Define

```text
Omega_m0      = 8 pi G epsilon_m0/(3 c0^2 H_A0^2)
Omega_r0      = 8 pi G epsilon_r0/(3 c0^2 H_A0^2)
Omega_Lambda0 = Lambda c0^2/(3 H_A0^2)

E(A)^2 = Omega_r0 A^(-4) + Omega_m0 A^(-3) + Omega_Lambda0
Omega_r0 + Omega_m0 + Omega_Lambda0 = 1
H_A^(tau) = +H_A0 E(A)
```

The corresponding spatial Einstein equation is

```text
A''/A = -(H_A0^2/2) [
    Omega_m0 A^(-3)
    + 2 Omega_r0 A^(-4)
    - 2 Omega_Lambda0
]
```

Direct evaluation of the spatial EFE gives this equation; differentiating the
Hamiltonian constraint and using both continuity laws reproduces it. The source
sectors determine the rate of the single operational geometric scale `A`,
hence the rate of `a`; W3-40's causal chain `a -> P_F -> p` retains one
material response and one operational readout. Pulling the constraint back
through `A=a^(5/2)` gives

```text
(25/4) (a'/a)^2 = H_A0^2 [
    Omega_r0 a^(-10)
    + Omega_m0 a^(-15/2)
    + Omega_Lambda0
]

(25/4) a (da/dt)^2 = H_A0^2 [
    Omega_r0 a^(-10)
    + Omega_m0 a^(-15/2)
    + Omega_Lambda0
]
```

Equivalently, the two first-order histories are

```text
da/dtau = (2/5) H_A0 a E(a^(5/2))
da/dt   = (2/5) H_A0 a^(-1/2) E(a^(5/2))
```

Anchoring the integration at the normalized present point `A_0=1`, the unique
implicit expanding solutions on each connected interval with `E(A)^2>0` are

```text
tau-tau_0 = H_A0^(-1) int_[1]^A du/[u E(u)]
t-t_0     = H_A0^(-1) int_[1]^A u^(-2/5) du/E(u)
```

Thus the functional freedom in `a(t)` is closed on this conditional EFT
branch. A numerical history requires only the registered finite inputs and the
choice of time origin. The physical endpoint at which this post-Genesis EFT
attaches to the Genesis transition remains a separate open interface. `H_A0`
is the process-time expansion rate at `A=1`; its identification with a measured
Hubble constant belongs to the still-open photon--atomic and clock forward
map. On the present leading-EH branch, positive `Lambda` carries late-time
operational acceleration. A future `Lambda`-free RefG acceleration law would
be a different geometric action and therefore a new model version.

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
