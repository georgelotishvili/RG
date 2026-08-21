# W3-41 Foundation Constitutive Interface

W3-40 leaves one decisive cosmological law open: `P_F(a)`. This gate asks
what follows from a declared one-coordinate homogeneous foundation-cell
interface without inventing that law. The volume law `V_F=V_0 a^3` and the
completeness of this state reduction are assumptions here, not derived facts.

For a fixed ideal-comoving cell,

```text
V_F(a) = V_0 a^3
Pi_F(a) = -E_F'(a)/(3 V_0 a^2)
K_Pi(a) = [a E_F''(a) - 2 E_F'(a)]/(9 V_0 a^2)
```

These are exact mechanical identities. They do not by themselves identify
W3-40's cadence-controlling scalar `P_F` with the mechanical stress `Pi_F`.

Only on the explicitly conditional bridge `P_F = Pi_F`, the exact response
dictionary becomes

```text
kappa = -d ln(P_F)/d ln(a) = 3 K_F/P_F = 2 - a E_F''/E_F'
p(a) = exp[-(1/2) integral_1^a kappa(u) du/u]
A(a) = a exp[+(1/2) integral_1^a kappa(u) du/u]
```

## Verdict

The gate passes, but its main result is a nonselection theorem. Every
admissible positive decreasing `P_F(a)` reconstructs an energy,

```text
E_F(a) = E_F(1) - 3 V_0 integral_1^a u^2 P_F(u) du,
```

and every positive `kappa(a)` reconstructs `P_F`, `p`, and `A`. Therefore the
energy--stress definitions alone select none of these functions. In
particular, `P_F=P_F0 a^(-n)` is exactly the additional constitutive choice
`kappa=n`; neither the interface nor the positive-bulk-modulus condition
determines `n`.

W3-42 now supplies the exact conditional volume dictionary and proves why
the missing physical premises cannot be skipped. A supplied
uniform-isotropic `d`-cell gives `mathcal V=mathcal V_0 a^d` and `d=3`
recovers every corresponding W3-41 formula. But the link scale alone does not
fix cell angles; one fixed graph admits inequivalent measures; and a cubic
volume can hide an additional homogeneous shape coordinate. W3-42 therefore
does not close the assumptions used here.

For the current cosmology target, the homogeneous-isotropic `d=3` branch is
used as an explicit effective input. The next bounded task asks one physical
question: does the existing RefG energy-and-activation account supply a
conservation/work statement that fixes `P_F(a)` without a fitted exponent?
No new calculation package is opened until that statement is explicit. If it
does not follow from the present ontology, the task closes `OPEN` with the
single missing premise recorded.

## Files

- `w3_41_foundation_constitutive_interface_preregistration.md`
- `w3_41_foundation_constitutive_interface.py`
- `w3_41_result.json`
- `w3_41_result.sha256`

## Current result

- model version: `W3-41-v1.2-FOUNDATION-CONSTITUTIVE-INTERFACE`
- status: `PASS_EXACT_CONSTITUTIVE_INTERFACE__RECONSTRUCTION_DEGENERACY_PROVED__PHYSICAL_BRIDGE_AND_DYNAMICS_OPEN`
- upstream W3-40 result SHA-256: `e8104a664484ea0735387446c94367cca1035877ee6a26413eeddaf158b5be64`
- preregistration SHA-256: `ab852e070871c707ed46e1ac2edde995931c12bd3a0d117e784c258e9f7ba99b`
- source SHA-256: `849fb7a649af526ebcdf00e114bc4cd93e6cdd81b2a1cbd246dfa4c77db18f05`
- result SHA-256: `f692c38c6deca0f20bc94cb048c4407ca3ed8520a566fa7d73b79d1fe8778ab9`
- W3-42 child result SHA-256: `5de8e1b5026f6fd7fac89699e6d09066ec309dd85ff679d69f5ad05df6eec329`
