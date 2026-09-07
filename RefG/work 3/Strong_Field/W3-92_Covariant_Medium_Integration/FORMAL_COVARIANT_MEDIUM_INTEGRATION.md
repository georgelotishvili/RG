# W3-92: Covariant-medium integration

## Decision and source of authority

The action and exact exterior in the author's root [RefG_ka.md](../../../../RefG_ka.md), equations (5)--(16) and Proposition 1, are now an explicit strong-field medium branch of the active RefG research core. They are not a value of the undetermined W3-87 coupling and are not an automatic replacement proof for the W3-54 continuum branch. This document integrates existing results and verifies their stated boundaries; it does not propose another action or a collapse model.

The source article is frozen for this integration at SHA256 `2571f9fbde25cd9e5258e5bb2c78797380123bf32621e4eaf068ce97c1b4c927`. The executable reads that source and this contract, and prints its own hashes and exact residuals. No changing monograph, private idea ledger, or formal-proof digest is a frozen dependency. Their editorial integration does not change the article's equations.

## Model, conventions and source ledger

Use signature `(+---)`, `c = hbar = 1`, `M_Pl^-2 = 8 pi G`, and the article's Riemann convention. The independent fields are the metric, a clock scalar `Phi`, three material-label scalars `phi^A`, and a dimensionless deficit-response scalar `H`:

```text
Y = g^{mu nu} Phi_mu Phi_nu > 0,   u_mu = Phi_mu/sqrt(Y),
gamma^{mu nu} = u^mu u^nu - g^{mu nu},
B^{AB} = -g^{mu nu} phi^A_mu phi^B_nu > 0,
Yhat = exp(-2H) Y,   Bhat = exp(2H) B,
I1 = tr(Bhat), I2 = [(tr Bhat)^2-tr(Bhat^2)]/2, I3 = det(Bhat),
S = integral sqrt(-g) [M_Pl^2 R/2 - M_*^4 F_med(Yhat,I1,I2,I3)
                      - omega_H M_Pl^2 gamma^{mu nu} H_mu H_nu]
    + S_m[g,psi].
```

`F_med` here denotes exactly the article's `F`; the subscript only prevents confusion with W3-87's multiplier of torsion. Ordinary matter is universally minimally coupled to the metric. The medium Hilbert tensor and any specified ordinary-matter Hilbert tensor are each counted once. Neither `H`, clock/ruler readouts, nor a copied W3-54 fluid tensor is an additional independent source.

The article selects a classical truncation: `omega_H=1` and a `C^2` response satisfying `F_med=F_med,Yhat=F_med,Bhat=0` at `Yhat=1,Bhat=identity`. Its Hessian and same-derivative-order omitted operators are not fixed by this exterior theorem. The symmetry does not by itself select those silent-point conditions or protect the truncation radiatively. No numerical response coefficients or cutoff are selected in W3-92.

On `r>=r_c>0`, `m>0`, the exact branch is

```text
A=exp(2m/r), B=exp(-2m/r),
ds^2=B dt^2-A(dr^2+r^2 dOmega^2),
Phi=t, phi^A=x^A, H=m/r.
```

Here `x^A` are isotropic Cartesian coordinates, not spherical labels. `Yhat=1`, `Bhat=identity`; the response and label/clock currents vanish on this background. The projected H equation has conserved normalized flux `Q_H=-r^2 H'=m`. Its nonzero Hilbert source is

```text
Z_H = m^2 exp(-2m/r)/r^4,
Theta^mu_nu/M_Pl^2 = Z_H diag(-1,+1,-1,-1) = G^mu_nu.
```

This establishes an actual source for this exterior and a negative radial null-energy sum. It does not establish the health of the coupled clock--H--label--metric perturbations. The spatially elliptic fixed-other-fields H-H principal block is not a full ghost/degree-of-freedom result.

## Compatibility map

| Existing result | Relationship to this branch |
| --- | --- |
| W3-54 constant-coefficient TEGR/EH selection | Retained conditional theorem for its declared coframe/current action. The article uses the EH operator explicitly and supplies a different medium source; its five scalars have not been reduced to W3-54's one-current source. |
| W3-51 and W3-91 exponential metric | The same static exterior geometry now has the article's explicit action embedding on `r>=r_c`. W3-91's singular parallel-propagated endpoint concerns the *uncut* continuation to `r=0`; it is not erased by providing an exterior source. |
| W3-64--83 Einstein/scalar/current work | Generic metric identities and operational measurements remain reusable after conventions are converted. Particular source solutions, oscillons, spectra, stability and collapse runs remain attached to their original actions. |
| W3-84, W3-86, W3-88 node/link model | Finite lattice feedback and its native phase reduction remain candidate-model evidence, not a microscopic derivation of this continuum action. |
| W3-85 regular-centre benchmark | Useful geometric/source comparison, not a theorem forbidding the article's noncanonical anisotropic medium. |
| W3-87, W3-89, W3-90 | Statements about `F_grav(n_C) T` and its Kantowski--Sachs reduction remain on that separate postulated action. `F_med`, `H`, `Phi`, and `phi^A` are not identified with `F_grav`, `n_C` or `theta_C`. |
| Full PPN, CMB and quantum-matter work | No same-action inheritance. Static spherical beta/gamma coefficients can be checked here; preferred-frame parameters, cosmological branches and quantum/oscillon sectors require their own matching. |

The article uses the opposite metric signature from W3-54 and most strong-field packages. Metric conventions must be converted before reusing component formulas. The article's `H` is not a Hubble function, its `Phi` is not the ordinary oscillon phase, and its conserved exterior `Q_H` is not the collective particle/phase number.

## Regular-core target and the restricted-source discriminator

The article's core is a geometric target, not an action-derived interior. Set `x=r/r_c`, `q=2m/r_c`, and `1<q<2`:

```text
lA = q(35 x^2/8 - 21 x^4/4 + 15 x^6/8),
lB = -q + q(-11 x^2/8 + 9 x^4/4 - 7 x^6/8),
A=exp(lA), B=exp(lB).
```

At `x=1`, both metric functions and their first two derivatives match the exterior. At the Cartesian centre they are positive even functions with zero first derivatives. The source article proves the joined target horizonless and geodesically complete; W3-92 checks the matching and local source geometry, not a new numerical or global-completeness proof. The target retains the outer light ring; a transparent horizonless target's light-ring critical scale is a scattering separatrix, not automatically an absorption shadow.

Two exact boundaries matter for further work:

1. `lA+lB=q(x^2-1)^3`. The stationary clock ratio to infinity is `p_clock=sqrt(B)` and the isotropic coordinate size per unit local proper rod is `p_ruler=1/sqrt(A)`. They coincide on the exterior, but not throughout the core. Neither is an image size or a universal moving-observer ratio.
2. On the narrower ordinary-matter-free static branch `Phi=t, phi^A=x^A`, isotropy makes `F_med,Bhat^{AB}=F_b delta_AB`. The Cartesian label equations imply `d_r[sqrt(A B) exp(2H) F_b]=0`. Smooth connection to the silent exterior forces this constant to zero; positivity of the metric and finite `H` then give `F_b=0`. The remaining response has isotropic spatial stress, while the projected H sector gives

   `p_t-p_r = 2 M_Pl^2 H'^2/A >= 0`.

   For the article's core, let `Z=(G^r_r-G^theta_theta)/2`. Direct geometry gives

```text
r_c^2 exp(lA) Z = q x^2 [153 q x^8 - 360 q x^6 + 30 q x^4
                         + 360 q x^2 - 167 q + 384 x^2 - 384]/64.
```

Its leading coefficient is `-q(167q+384)/64 < 0` for every `q>0`. Thus this *specific core target and restricted source/label branch* cannot satisfy the full metric equations near the centre. This excludes neither different regular label profiles, specified additional matter, other core geometries, nor the full article action.

Independently, the full H equation implies the article's flux balance (48). A regular centre has `Q_H(0)=0`, while matching fixes `Q_H(r_c)=m>0`; hence the integrated response source must be nonzero somewhere inside. Keeping the entire interior at the silent point cannot provide that flux without a separately specified H source or shell. Minimal metric-coupled ordinary matter does not directly add such a source to the H equation.

## Frozen verification contract (CODES section 5)

- `CLAIM_ID`: `W3_92_EXISTING_COVARIANT_MEDIUM_INTEGRATION`.
- `CLAIM`: The article's declared action admits its exact exponential exterior, while the specified core has the stated matching/readout identities and fails the stated narrower source-branch anisotropy condition; these results can be integrated without identifying inequivalent earlier actions.
- `TYPE`: `EXACT_IDENTITY` and restricted source incompatibility; editorial compatibility map. No `MECHANISM_DERIVED` or observational pass.
- `MODEL_VERSION`: `W3-92 v1.0`, article hash above; this contract is written before its verifier is executed. No action or parameter change is authorized by a failed test.
- `ASSUMPTIONS`: The action, silent-point conditions, signatures, static field ansatz and smooth source-free matching stated above. The restricted label conclusion uses a connected branch and a nondegenerate positive metric, not arbitrary material labels.
- `DOMAIN`: Exterior `m>0,r>=r_c>0`; target `r_c>0,0<=x<=1,1<q<2`; local obstruction also holds for every `q>0` at sufficiently small positive `x`. Spherical-coordinate formula limits at zero are taken in the regular Cartesian extension.
- `CONVENTIONS`: Article conventions above; dimensionless `x` computations use `r_c=1` and report curvature/stress with the required `r_c^-2` factor restored. No coordinate radius is called an areal radius.
- `FREEDOM_LEDGER`: Universal `M_Pl,M_*,omega_H=1`; response function restricted only by the silent point; object/boundary parameter `m`; target matching choice `q` in its declared interval. No fitted data parameters, optimization, density profile, EOS or phenomenological switch.
- `DEPENDENCIES`: Root article equations (5)--(16), (18)--(30), (31)--(33), (35)--(48); no prior stored PASS or mutable monograph hash is used as evidence. CODES supplies methodology, not physical premises.
- `METHOD`: Fresh SymPy metric connection/Ricci/Einstein calculation, direct Hilbert variation of the projected gradient, exterior flux/field substitution, exact weak-field series, polynomial core identities, and a small set of altered-expression controls against the unchanged validators.
- `PASS_CONDITION`: Exact residuals simplify to zero, source-branch contradiction has the strict negative analytic coefficient, required altered expressions are rejected, source provenance matches, and JSON serialization is finite. Integration success and physical closure flags remain separate.
- `FAIL_CONDITION`: Any identity, provenance check, required strict sign or negative control fails. Exit nonzero and report the actual failure; do not modify the article or tune a profile.
- `FALSIFIER`: A nonzero residual of an asserted identity within its domain, or failure of the explicitly stated restricted-label source derivation. Passing these checks does not preclude a coupled health failure of the model.
- `RESIDUAL`: Named exact symbolic residuals in standard output; nonzero symbolic residuals are retained, not replaced by a declared PASS.
- `ERROR_BOUND`: Zero symbolic truncation error for identities; weak-field equalities hold only to the displayed order. No floating-point physics acceptance threshold or dataset error budget is relevant.
- `VALIDITY_HEALTH`: Positive exterior field-domain and metric factors; local source/clock/ruler consistency. Full constrained coupled principal symbol, Hamiltonian spectrum, formation, nonlinear stability, strong coupling and radiative/EFT completion remain untested.
- `BRANCHES`: Exact nonzero-flux exterior integrated; regular geometric target retained; its restricted source/label realization rejected; other action-derived interiors not selected or ruled out.
- `OBSERVABLE_MAP`: Static clock and local rod maps above; radial optical index `sqrt(A/B)`, ADM leading mass coefficient, static spherical beta/gamma expansion. No full PPN inference.
- `FORWARD_MODEL`: N/A for data comparison: no radiative-transfer, inclination, spin, absorption/emission, detector or likelihood model is supplied.
- `DATA_ROLE`: No observational data; no calibration, validation set or fit.
- `IDENTIFIABILITY`: The exterior leaves the response Hessian and omitted operators undetermined; geometry alone cannot select a unique medium completion. No model-selection claim.
- `BENCHMARK`: Article's analytic exterior/core identities; Schwarzschild's static isotropic spatial quadratic coefficient is a comparison only. No numerical trajectory benchmark.
- `CLOSURE_FLAGS`: Computed exterior/matching/readout/source-discriminator flags are independent. Full coupled health, action-derived regular interior, regular black hole, formation, full PPN, CMB, quantum matching, W54/W87 equivalence and microscopic derivation remain false.
- `CROSSCHECK`: Independently derived metric curvature versus independently varied medium stress; generic core geometry versus article's component formulas; altered source/readout/matching expressions must fail their original identities.
- `PROVENANCE`: Article SHA256 above, runtime Python/SymPy versions, contract and verifier SHA256 printed to stdout. No saved result file; exact two-file package.
- `FILES`: This contract and `verify_covariant_medium_integration.py`; article remains read-only at repository root. Run `python -B verify_covariant_medium_integration.py` from this folder, or pass its path from the repository root.

Stop after this bounded integration. The next strong-field source calculation, if separately authorized, must use the article's complete field equations and a stated admissible branch rather than copying a W3-87 equation or silently imposing the target metric as a solution.
