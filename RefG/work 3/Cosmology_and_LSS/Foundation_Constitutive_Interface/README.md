# W3-41 Foundation Constitutive Interface

At its frozen scope, W3-40 left one decisive cosmological law open:
`P_F(a)`. W3-41 asks what follows from a declared one-coordinate homogeneous
foundation-cell interface without inventing that law. The volume law
`V_F=V_0 a^3` and the completeness of this state reduction are assumptions
here, not derived facts.

For a fixed ideal-comoving cell,

```text
V_F(a) = V_0 a^3
Pi_F(a) = -E_F'(a)/(3 V_0 a^2)
K_Pi(a) = [a E_F''(a) - 2 E_F'(a)]/(9 V_0 a^2)
```

These are exact mechanical identities. They do not by themselves identify
W3-40's cadence-controlling scalar `P_F` with the mechanical stress `Pi_F`.

Only on the explicitly conditional bridge `P_F = Pi_F`, the W3-41
mechanical response dictionary becomes

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

## Downstream density selection

W3-41's result and hashed artifacts remain unchanged: this gate proved that
the mechanical interface alone cannot select `P_F(a)`. The current cosmology
branch subsequently supplies a different physical closure rather than
promoting W3-41's candidate `P_F=Pi_F` bridge.

On the already-connected fixed-comoving branch, `P_F` is selected as the
density of a conserved relaxation/coherence content `Q_rel`. With the effective
homogeneous-isotropic input `mathcal_V=mathcal_V_0 a^3`,

```text
Q_rel := P_F mathcal_V
dQ_rel/dtau = 0
P_F/P_F0 = a^(-3)
p = a^(-3/2)
A = a^(5/2)
```

`Q_rel` is not the mechanical potential `E_F`; therefore constant `Q_rel`
does not imply `Pi_F=-dQ_rel/dmathcal_V`. The canonical domain and falsifier
are recorded in the parent `Cosmology_and_LSS/README.md`.

## Files

- `w3_41_foundation_constitutive_interface_preregistration.md`
- `w3_41_foundation_constitutive_interface.py`
- `w3_41_result.json`
- `w3_41_result.sha256`

## Frozen W3-41 gate result

- model version: `W3-41-v1.2-FOUNDATION-CONSTITUTIVE-INTERFACE`
- status: `PASS_EXACT_CONSTITUTIVE_INTERFACE__RECONSTRUCTION_DEGENERACY_PROVED__PHYSICAL_BRIDGE_AND_DYNAMICS_OPEN`
- upstream W3-40 result SHA-256: `e8104a664484ea0735387446c94367cca1035877ee6a26413eeddaf158b5be64`
- preregistration SHA-256: `ab852e070871c707ed46e1ac2edde995931c12bd3a0d117e784c258e9f7ba99b`
- source SHA-256: `849fb7a649af526ebcdf00e114bc4cd93e6cdd81b2a1cbd246dfa4c77db18f05`
- result SHA-256: `f692c38c6deca0f20bc94cb048c4407ca3ed8520a566fa7d73b79d1fe8778ab9`
- W3-42 child logical pins: preregistration
  `4cc4674775525a3c76cd8cb282461e5e83b651aff3554de21983568ee7e1f9f1`
  and verifier source
  `0593c452dae764c2b0455d31807a6a81d033bd928db40717a0eec6df5fe04188`;
  its generated result is checked at runtime against its adjacent checksum
