# W3-42 Foundation State Space and Volume Map

W3-41 used the conditional cell-volume law `V_F=V_0 a^3` and a
one-coordinate homogeneous state. W3-42 tests whether those two assumptions
follow from the frozen RefG foundation picture and from W3-40's link scale
`a`.

## Exact result

For a supplied nondegenerate `d`-cell with fixed combinatorics and a regular
orientation-preserving homogeneous deformation,

```text
B = B_0 F
G = F^T G_0 F
mathcal_V/mathcal_V_0 = det(F)
d ln(mathcal_V/mathcal_V_0)/d ln(a) = a tr(F^-1 F')
```

On the additional uniform-isotropic branch `F=a I_d`,

```text
G = a^2 G_0
mathcal_V_d = mathcal_V_d0 a^d
```

Therefore `d=3` returns the cubic map used in W3-41 exactly. This is a
conditional theorem: W3-42 did not microscopically derive `d=3`, a physical
cell complex, an invariant geometric measure, or the uniform-isotropic orbit.
The current cosmology branch later retains the observed homogeneous-isotropic
`d=3` geometry as an explicit effective input.

For any supplied positive geometric measure,

```text
nu(a) = d ln(mathcal_V)/d ln(a)
mathcal_V(a) =
    mathcal_V_0 exp[integral_1^a nu(u) du/u]
```

Only on the separately declared candidate bridge `V_F=mathcal_V`, the W3-41
mechanical dictionary generalizes to

```text
Pi_F = -a E_F'/(nu mathcal_V)
K_F  = -(a/nu) Pi_F'
kappa = nu K_F/P_F                    on P_F=Pi_F
```

For constant `nu=d`,

```text
Pi_F = -E_F'/(d V_0 a^(d-1))
K_F  = [a E_F''-(d-1)E_F']/(d^2 V_0 a^(d-1))
kappa = d-1-a E_F''/E_F'
```

The `d=3` specialization exactly reproduces W3-41.

All derivative ratios are statements on their regular loci. The general
mechanical formulas require `mathcal_V'!=0` (equivalently `nu!=0`), and
`kappa` additionally requires the candidate `P_F=Pi_F!=0`. The hidden-state
fixed-`q` ratio requires `mathcal_V_a!=0`; its along-path counterpart requires
`mathcal_V_a+mathcal_V_q q'!=0`. No claim is made at an excluded denominator.

## Constructive nonselection

The gate does not merely leave the missing premises unnamed; it constructs
exact witnesses showing why they are necessary.

### Link scale does not select volume

Three independent basis links can all have length `a` while their mutual
angle changes. With

```text
c(a) = (a-1)/(a+1)
```

the registered witness has three link lengths equal to `a`, but

```text
mathcal_V(a)/mathcal_V(1) = 2 a^(7/2)/(a+1),
```

which is not `a^3` away from the reference point. Thus W3-40's link scale
alone does not freeze cell angles or derive the cubic map.

### A graph does not select its physical measure or dimension

The finite periodic relational witnesses `T_5^d`, for `d=1,2,3`, all have
exact node/edge counts, regular degree, connectivity, translation symmetry,
and no unique graph center. Those shared qualitative properties do not
select one `d`.

On the same fixed `T_5^3` graph, three supplied extensive assignments scale
as

```text
node count             ~ a^0
total edge length      ~ a^1
filled-cell measure    ~ a^3
```

Adjacency plus `a` therefore does not define a unique physical volume
measure. The periodic graphs are comparison witnesses, not a proposed cosmic
topology.

### Cubic volume does not prove a one-coordinate state

The homogeneous family

```text
G_shape = a^2 diag(exp(2s), exp(-2s), 1)
```

has `mathcal_V=a^3` for every `s`, while a shape invariant changes with `s`.
Hence an additional homogeneous shape coordinate can remain invisible to
the cubic volume.

More generally, if `E=E(a,q)` and `mathcal V=mathcal V(a,q)`, then the
fixed-`q` pressure

```text
Pi_F = -E_a/mathcal_V_a
```

equals the pressure inferred along a path `q=q(a)` only if `q'=0` or

```text
E_q + Pi_F mathcal_V_q = 0.
```

Homogeneity by itself does not remove an internal scalar, phase, activation,
or shape mode.

### Cell volume is not activated volume

The global bookkeeping identity is

```text
V_act = N_act v_cell
d ln(V_act)/d ln(a) =
    d ln(N_act)/d ln(a) + d ln(v_cell)/d ln(a).
```

A conditional cell-volume law cannot determine the growth of activated
existence without a separately derived active-cell measure.

## Verdict

The exact gate passes:

```text
PASS_EXACT_HOMOGENEOUS_MEASURE_DICTIONARY__
DIMENSION_MEASURE_AND_STATE_COMPLETENESS_OPEN
```

This preserves W3-41 as a valid conditional `d=3` branch. It does not promote
`V_F=V_0 a^3`, `V_F=mathcal_V`, or the one-coordinate reduction to physical
facts.

For the current cosmology target, the homogeneous-isotropic `d=3` branch is
carried forward as an explicit effective input supported by observed spatial
geometry. Its microscopic origin is a separate research problem and does not
automatically open another gate.

## Downstream density selection

W3-42's result and hashed artifacts remain unchanged. For the current
cosmology objective, its effective homogeneous-isotropic `d=3` branch is
now combined with a selected density closure for a conserved
relaxation/coherence content `Q_rel` on a fixed, already-connected
ideal-comoving domain:

```text
Q_rel := P_F mathcal_V
dQ_rel/dtau = 0
mathcal_V = mathcal_V_0 a^3
```

Therefore `P_F/P_F0=a^(-3)`, `p=a^(-3/2)`, and `A=a^(5/2)`. This does
not retroactively derive the three-dimensional volume law from foundation
microstates, and it does not apply across a moving Genesis activation
boundary. The canonical statement and falsifier are recorded in the parent
`Cosmology_and_LSS/README.md`.

## Files

- `w3_42_foundation_state_space_volume_map_preregistration.md`
- `w3_42_foundation_state_space_volume_map.py`
- `w3_42_result.json`
- `w3_42_result.sha256`

## Frozen W3-42 gate result

- model version: `W3-42-v1.0-FOUNDATION-STATE-SPACE-VOLUME-MAP`
- upstream W3-41 result SHA-256: `48e6a981eaa2d696240323d6ccbbb4f744e67f2c37329ed292a1de11ce10c9fb`
- preregistration SHA-256: `8ba44af154a3f9a18b207b4f17a3dcecdb27a8a9d59f7f9aa712c0946763ae98`
- source SHA-256: `ae30251c3fb5eefae31dd9310de62dda2d3cf700c030bcb8c1e8f08c3e57724f`
- generated-result integrity: the runtime SHA-256 must match the adjacent
  `w3_42_result.sha256`; the result digest is not a logical dependency because
  `generated_utc` and runtime metadata are intentionally volatile
