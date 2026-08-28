# W3-59 real-field open-radiation bridge

## Result

W3-59 closes the exact action/source map for a single real `Z2` field on the selected fixed RefG coframe and decisively rejects the frozen W3-58-to-real-oscillon benchmark as a 1000-period long-lived core.

The exact retained action is

```text
S_phi = -(1/c0) integral e [ (1/2)g^munu d_mu phi d_nu phi + V(phi) ] d4x,
V(phi) = (1/2)m^2 phi^2 - (1/4)lambda phi^4 + (1/6)g phi^6.
```

Metric variation gives the Hilbert source `T_phi`, and the active branch has the single-count ledger

```text
T_total = T_C + T_phi.
```

`T_phi` replaces the complex W3-58 source `T_O`; it is not added to it. The real field has exact `Z2` symmetry and no continuous internal `U(1)` charge.

## Frozen seed

At the preregistered values `a=1/4` and `Omega_seed=4/5`, the real one-harmonic Galerkin boundary problem converges to a positive, nodeless, monotone profile with

```text
F(0)                  = 2.0131041506
R_rms(seed)           = 2.9818445698
R_core=4 R_rms(seed)  = 11.9273782792
weighted residual     = 1.32438e-8
```

The W3-58 Q-ball profile is used only as the BVP solver's fixed initial guess. No amplitude, width, frequency, or potential coefficient is fitted after seeing the result.

## Open-domain decision

Three registered evolutions were run through 1000 seed periods:

| run | grid | domain / absorber | lifetime crossing |
|---|---|---|---:|
| canonical | `dx=0.05`, `du=0.0125` | `200 / [150,200]` | `110.931` periods |
| fine | `dx=0.025`, `du=0.00625` | `200 / [150,200]` | `110.982` periods |
| domain | `dx=0.05`, `du=0.0125` | `240 / [180,240]` | `110.931` periods |

During periods 80--100, the nonlinear core is unmistakably localized: its core energy exceeds the identical free massive-field control by a factor of `3721.6`, and its central RMS amplitude by `423.1`. Soon afterward, all three evolutions cross the preregistered `E_ref/e` lifetime boundary near period 111 and radiate away. By the late window, the surviving core-energy fraction is about `5.9e-4`. The registered one-sided submass search places its peak at the upper edge, while an unrestricted broadband search independently selects the same `omega=0.99987` peak. Because the core has already crossed its lifetime gate and dispersed, this is recorded as a late-remnant diagnostic rather than evidence for a surviving oscillon.

The agreement is quantitative:

- canonical/fine formation-energy difference: `0.155%`;
- canonical/fine late-frequency difference: `0.00199%`;
- maximum energy-plus-outward-flux residual: `1.25e-4` canonical and `3.12e-5` fine;
- independent KDK/RK4 profile difference: `0.00421`;
- independent centre-signal difference: `0.000787`;
- absorber excess reflection: `6.95e-9` at `3 Omega_seed` and `1.39e-9` at `5 Omega_seed`.

An outward massive-wave disturbance is detected: the measured detector delay is `21.25`, against the massive-wave prediction `21.205`. The preregistered persistent odd-harmonic criterion is not met at both detector radii.

## Verdict and boundary

Machine status:

```text
FAIL_FROZEN_W3_58_TO_W3_59_REAL_OSCILLON_BRIDGE__EXACT_REAL_FIELD_ACTION_RETAINED__ALTERNATIVE_BENCHMARKS_NOT_TESTED
```

This is a clean rejection of one frozen bridge, not a theorem against every real oscillon. Deleting the complex phase and second real component in this frozen construction does not preserve the W3-58 lifetime. The comparison does not establish `U(1)` as a universal requirement for real oscillons.

The test is confined to a fixed coframe. Dynamical coframe backreaction, foundation selection of the sextic coefficients, alternative foundation-motivated seeds, nonspherical stability, electric neutrality, and particle identity remain outside W3-59. Any alternative benchmark requires a new preregistered model version; it cannot be tuned inside this completed test.

## Reproduction

From the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python '.\RefG\work 3\Lagrangian_Formulation\One_Oscillon_Real_Field_Open_Radiation_Bridge\w3_59_one_oscillon_real_field_open_radiation.py'
```

The script verifies pinned dependencies, re-solves the Galerkin BVP, calibrates the absorber, compares two independent conservative integrators, runs the three long evolutions and the registered controls, then regenerates `w3_59_result.json` and `w3_59_result.sha256` atomically.
