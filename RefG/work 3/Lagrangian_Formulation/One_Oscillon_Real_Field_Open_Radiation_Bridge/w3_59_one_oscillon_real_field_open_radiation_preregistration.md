# W3-59 preregistration: one real oscillon in an open radiation domain

## CLAIM

Test whether the frozen W3-58 sextic localized branch supplies, without post-result tuning, a seed for a finite-energy, long-lived, slowly radiating, spherically symmetric oscillon of one real field on the already selected fixed RefG coframe.

This stage can establish an exact real-field action/source bridge and converged numerical evidence for one radiating oscillon candidate. It cannot establish an exact eternal breather, electric neutrality, particle identity, nonspherical stability, foundation-level coefficient selection, or dynamical coframe backreaction.

## MODEL_AND_SOURCE_LEDGER

The W3-59 branch contains one real ordinary-sector field:

```text
S_phi = -(1/c0) integral e [ (1/2) g^{mu nu} d_mu phi d_nu phi + V(phi) ] d4x
V(phi) = (1/2)m^2 phi^2 - (1/4)lambda phi^4 + (1/6)g phi^6
a = g m^2/lambda^2 = 1/4
T_total = T_C + T_phi
```

`T_phi` replaces the W3-58 complex-field source `T_O`; it is not added to it. The branch forbids a second metric, a duplicate ordinary source, a fitted confinement term, a harmonic filter, and an electric-neutrality declaration.

With `u=m tau`, `x=m r`, and `f=sqrt(lambda) phi/m`, the fixed-flat-coframe evolution equation is

```text
f_uu - f_xx - (2/x)f_x + f - f^3 + a f^5 = 0.
```

The target-space symmetry is the exact discrete transformation `f -> -f`. A continuous internal `U(1)` generator and its Q-ball charge are absent.

## FROZEN_BENCHMARK_AND_SEED

```text
a = 0.25
Omega_seed = 0.80
initial velocity = 0
W3-58 profile role = BVP initial guess only
post-result amplitude, width, frequency, or potential tuning = forbidden
```

The deterministic one-harmonic Galerkin seed solves

```text
F_xx + (2/x)F_x = (1-Omega_seed^2)F - (3/4)F^3 + (5/8)a F^5,
F_x(0)=0,
F_x(X)+[sqrt(1-Omega_seed^2)+1/X]F(X)=0.
```

The analytic seed window is

```text
0 < 1-Omega_seed^2 < 27/(160a).
```

The W3-58 profile enters only through the leading seed constructor

```text
F_guess = (2/sqrt(3)) f_Q.
```

The converged Galerkin profile, rather than the Q-ball profile, becomes the turning-point datum `f(x,0)=F(x)`, `f_u(x,0)=0`.

The one-harmonic truncation omits the exact nonzero sources

```text
R3 = -(1/4)F^3 + (5a/16)F^5,
R5 = (a/16)F^5.
```

The full time evolution retains every generated harmonic.

## EXACT_RADIATION_GATE

For an odd-harmonic spherical periodic expansion, each vacuum-tail mode obeys

```text
F_n,xx + (2/x)F_n,x + [(n omega)^2-1]F_n = 0.
```

For `n omega>1`, a nonzero standing periodic tail scales as an oscillatory `1/x` field and carries infinite total energy on an infinite domain. A finite-energy exact periodic solution must therefore cancel every open-harmonic amplitude. W3-59 instead tests for a converged nonzero outgoing open harmonic. Its detection identifies the constructed branch as a radiating oscillon and excludes exact periodicity for that branch; it is not a universal no-breather theorem.

## NUMERICAL_METHOD

The full nonlinear spherical PDE is evolved on a cell-centred finite-volume radial grid. The origin has exactly zero inner-face flux. A quartic absorbing layer precedes the outer zero-gradient face. The canonical integrator is staggered kick-drift-kick with a symmetric exact local damping split. All energy and flux quantities use the same `4 pi` convention.

The seed RMS radius determines the core radius before evolution:

```text
R_core = 4 R_rms(seed).
T0 = 2 pi/Omega_seed.
samples = 32 per T0
formation/reference window = periods 80 through 100
lifetime threshold = first 20-period moving mean E_core < E_ref/e
```

Three registered long runs extend through 1000 seed periods:

```text
canonical: Xmax=200, absorber=[150,200], dx=0.050, du=0.0125
fine:      Xmax=200, absorber=[150,200], dx=0.025, du=0.00625
domain:    Xmax=240, absorber=[180,240], dx=0.050, du=0.0125
absorber profile power=4, gamma_max=1
radiation detectors x=40 and x=60
```

Registered controls:

```text
linear massive Klein-Gordon control with the identical seed through 100 periods
nonlinear 0.99F and 1.01F seeds through 200 periods
independent conservative pre-reflection comparison through u=200
absorber calibration at omega=3 Omega_seed and 5 Omega_seed against an Xmax=400 no-return reference
```

Only cycle summaries and detector time series are retained. Full field histories and parameter scans are outside scope.

## SYMBOLIC_PASS_GATES

All must pass:

1. Euler-Lagrange variation yields the stated real-field equation.
2. Metric variation yields the Hilbert tensor, with on-shell covariant conservation.
3. The potential has exact `Z2` symmetry.
4. No nonzero continuous one-dimensional target-space Killing generator preserves the potential.
5. Nondimensionalization yields the stated PDE.
6. At `a=1/4`, `v'(f)=f(1-f^2/2)^2`.
7. Cosine projection yields Galerkin coefficients `3/4` and `5/8`.
8. The benchmark satisfies `0.36 < 0.675` in the analytic seed window.
9. The leading W3-58-to-real seed coefficient is `2/sqrt(3)`.
10. `R3` and `R5` are nonzero polynomial sources.
11. The open-harmonic tail equation and finite-energy condition follow exactly.
12. The source ledger is exactly `T_total=T_C+T_phi`, with replacement rather than duplication.

## NUMERICAL_PASS_GATES

All must pass for the full W3-59 success status:

1. Galerkin BVP solutions at `X=60,80,100` and tolerances `1e-6,3e-7,1e-7` are finite, positive, nodeless, monotone, and converged in central amplitude and RMS radius below `1e-4` relative change.
2. The nonlinear formation-window core energy and central RMS amplitude each exceed the identical linear control by a factor of at least `10` and calibrated numerical noise by at least `1000`.
3. No registered long run crosses the frozen `E_ref/e` lifetime threshold through 1000 periods.
4. The late fundamental angular frequency lies below the mass threshold by at least three spectral bins and above `0.5`.
5. Canonical-versus-fine frequency differs by below `0.5%`, formation energy by below `2%`, and final normalized core energy by below `5%`.
6. Canonical-versus-domain energy and frequency observables differ by below `2%`.
7. The maximum normalized energy-plus-outward-flux residual is below `5e-3` in canonical/domain runs and below `1.5e-3` in the fine run, and decreases under refinement.
8. At least one odd harmonic above the mass threshold is detected at both radii with `SNR>=10`; its retarded propagation delay agrees with the massive-wave group delay within `10%`.
9. The absorber's reference-subtracted excess reflected-energy fraction is below `1e-6` at both registered open-harmonic frequencies.
10. Independent pre-reflection methods differ by below `5e-3` in normalized profile and centre signal, while each normalized energy drift is below `2e-3`.
11. Both `+/-1%` seeds remain localized through 200 periods, avoid the `E_ref/e` crossing, and retain a sub-mass fundamental frequency.

If long-lived localization passes while the open harmonic remains unresolved, the result is `NUMERICALLY_INCONCLUSIVE_RADIATION`. A failed convergence, formation, lifetime, or robustness gate rejects this frozen W3-58-to-W3-59 bridge, not the entire real-oscillon class.

## MUTATION_CONTROLS

The verifier must reject: a complex/two-component replacement; Q-ball charge, VK, or GSS gates; a second metric; `T_C+T_O+T_phi`; W3-56 readout used as dynamics; any change to the frozen benchmark, grids, durations, windows, or thresholds; harmonic filtering; selective reporting of one perturbation sign; reflecting-cavity longevity presented as open-boundary evidence; and any claim of electric neutrality or particle identity.

## PINNED_DEPENDENCIES

```text
W3-54 source-ledger contract sha256 = 6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879
W3-58 preregistration sha256 = 962980d4607ba506a5b65fe458f04ab31d8a78ac74511c68d43ff2d95f911dda
W3-58 result sha256 = 04412d4b1c55e5a94eae25ae401f3f574c051f883e78251ec27238679ccb1940
W3-58 source sha256 = f4894b3608a0a5964592fe2d42015497709c35b58ba62a336dc15f7c64bd60cf
```

## STOP_RULE

Stop when the exact real-field bridge and the registered open-boundary numerical decision are complete. Dynamical coframe backreaction is the separate W3-60 gate and opens only after a W3-59 pass. Particle spectrum, charge, spin, Standard-Model identifications, and intuitive-manuscript edits are outside W3-59.

## ALLOWED_SUCCESS_STATUS

```text
PASS_CONDITIONAL_EXACT_SINGLE_REAL_Z2_COFRAME_CORE_ACTION_AND_CONTINUOUS_INTERNAL_CHARGE_ABSENCE__CONVERGED_OPEN_BOUNDARY_LONG_LIVED_RADIATING_SPHERICAL_OSCILLON_NUMERICAL_EVIDENCE__FOUNDATION_COEFFICIENT_SELECTION_LOCALIZED_DYNAMICAL_BACKREACTION_NONSpherical_STABILITY_ELECTRIC_NEUTRALITY_AND_PARTICLE_IDENTITY_OPEN
```
