# Single-Driver Expansion--Relaxation Causal Lock

This isolated Work-3 gate records the exact reduced scale dictionary of the
cosmology branch:

`foundation expansion -> foundation-pressure relaxation -> material-standard response`

Within the reduced `(a,P_F,p,A)` graph, `a` parametrizes the expanding branch
and `P_F` decreases monotonically along it. W3-46 supplies the upstream
post-Genesis interpretation: phase-locked oscillon overlap lowers the
background tension/pressure of one foundation state. Increasing `a` is the
selected latent geometric representation of that relaxation, while material
contraction follows through `p` and `A=a/p` remains the single internal
geometric readout. Foundation-node separation and count have no
foundation-independent operational measurement. The original primary-driver
label is therefore scoped to this reduced parametrization rather than to the
complete microscopic ontology.

For an ideal comoving pair on this latent branch, the link count `N_12` is
fixed, the coordinate `a` grows, foundation pressure `P_F` falls, and the
positive bridge `p^2=P_F/P_F0` makes the material standard `p` fall. An
internal observer reads the single causal history through `A=a/p` rather
than measuring the foundation link scale directly.

W3-40 proves only the exact consequences of this frozen branch dictionary and
the non-identifiability of `a` and `p` from `A` alone. It does not derive the
constitutive law `P_F(a)`, the expansion dynamics, or any redshift, distance,
thermal, structure-growth, or likelihood forward model.

## Subsequent selected closure

W3-40's historical result and hashed artifacts remain unchanged. Downstream
of that gate, the current cosmology branch now selects `P_F` as the density
of a conserved relaxation/coherence content `Q_rel` within a fixed, already-
connected ideal-comoving domain whose physical volume grows with `a`:

```text
Q_rel := P_F mathcal_V
dQ_rel/dtau = 0
mathcal_V = mathcal_V_0 a^3
P_F/P_F0 = a^(-3)
p = a^(-3/2)
A = a^(5/2)
```

This is the selected ideal dilution closure, not a microscopic energy-transfer
law. W3-46 leaves open whether resonant, localized-participation, and diffuse
components are already implicit in `Q_rel` or require an explicit internal
exchange ledger.

This density closure does not use the candidate mechanical identification
`P_F=Pi_F`. Once it is imposed, the W3-40 equivalence class collapses to

```text
a = A^(2/5)
p = A^(-3/5)
P_F/P_F0 = A^(-6/5)
```

Its canonical statement, domain, and falsifier are recorded in the parent
`Cosmology_and_LSS/README.md`. This density closure alone leaves `a(t)` open;
the parent README now records a separate conditional operational-EFT
background equation. Numerical calibration and observable forward maps remain
open.

## Files

- `w3_40_expansion_relaxation_causal_lock_preregistration.md`
- `w3_40_expansion_relaxation_causal_lock.py`
- `w3_40_result.json`
- `w3_40_result.sha256`

## Frozen W3-40 gate result

- model version: `W3-40-v1.2-SINGLE-DRIVER-EXPANSION-RELAXATION-CAUSAL-LOCK`
- status: `PASS_EXACT_CAUSAL_LOCK_DICTIONARY__DYNAMICS_AND_OBSERVABLES_OPEN`
- preregistration SHA-256: `6da72a4fea86fe6bd4c29f007593c9c2c176062150d2090ee597845a53c9f5eb`
- source SHA-256: `1b76f5e847a68deacfb345bcf2e98d46ada4e85591e69b1bbc4cc4651945a585`
- result SHA-256: `6d16003df1f2d7a70371ec254f9cfc1692b7eac3df53874616135792eb2d63cf`
