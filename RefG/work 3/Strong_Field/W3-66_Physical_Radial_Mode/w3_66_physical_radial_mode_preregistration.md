# W3-66 — Physical fixed-charge radial mode at the first post-anchor turn

**CLAIM_ID:** `W3_66_PHYSICAL_FIXED_Q_RADIAL_MODE_CROSSING_GATE`

**MODEL_VERSION:** `W3-66-v1.0-EH-SEXTIC-U1-FIXED-ALPHA-PHYSICAL-RADIAL-MODE`

## Purpose and scientific boundary

W3-66 tests the physical, spherically symmetric, charge-conserving linear perturbations of the unchanged W3-64/W3-65 Einstein–complex-scalar system. It asks whether the lowest radial mode crosses a simple zero at the first simultaneous ADM-mass/Noether-charge turn localized by W3-65.

This is not inferred from the static turning point. It is accepted only if the full two-channel complex-scalar pulsation problem, including the linearized metric response and fixed-total-charge boundary condition, independently produces the crossing. The gate concerns linear radial modes on the selected fixed-`alpha` branch only. It does not decide nonlinear or nonradial stability, collapse fate, horizons, black holes, geodesic completeness, singularity resolution, or the foundation-scale origin of `alpha`.

## Immutable dependencies

Only the following hash-pinned active-core artifacts may be imported:

```text
w3_64_source_first_einstein_strong_field.py
SHA-256 99bc4331bec07219308bd15e43a945792ecd59c60ef959d17684944a6635aa77

w3_64_source_first_einstein_strong_field_preregistration.md
SHA-256 25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1

w3_64_result.json
SHA-256 b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b

w3_65_fixed_alpha_first_turning_point.py
SHA-256 5cc24de6951bbd57e0091b687ab467dac2070eb73403d71c52ff91386dae1b73

w3_65_fixed_alpha_first_turning_point_preregistration.md
SHA-256 385402e843850725ed562a449adb246b510b65038685cad6521d9ff1c8be3942

w3_65_result.json
SHA-256 e3256094f5123e70f747d501d84c7db1301e7a2ab00742fc914e254007c67b0b
```

Both upstream artifacts must remain valid. The inherited source ledger is one Einstein–Hilbert metric and one localized source `T_O`; no operator, source, action coefficient, potential coefficient, or fitted parameter may be added.

## Frozen background system

```text
alpha=0.04,
a=1/4,
N=1-2 alpha M/x,
M'=x^2 rho,
(ln sigma)'=alpha x[f'^2+Omega^2 f^2/(sigma^2 N^2)],
(sigma x^2 N f')'/(sigma x^2)
  +Omega^2 f/(sigma^2 N)-v_f=0,
v=f^2/2-f^4/4+f^6/24,
sigma(infinity)=1.
```

The W3 phase convention is `exp(+i Omega tau)`. Define the phase-displacement variable by `dot xi=-Omega q` and `Z=xi'`; this retains the standard Gleiser–Kain pulsation signs.

## Exact perturbation problem

Use polar–areal diagonal gauge, `delta g_theta_theta=delta g_tau_x=0`, with

```text
exp(nu)=sigma^2 N,
exp(lambda_g)=1/N,
Psi=exp(+i Omega tau) f(x)[1+H(tau,x)+i q(tau,x)],
H,Z proportional to exp(-i kappa tau),
Lambda=kappa^2.
```

The global constant-phase mode is removed by using `Z`. Both real scalar channels are retained. The momentum constraint gives

```text
delta lambda_g=2 alpha x f (f' H-f Z),
delta Q(x)=-(sigma N x^2 f^2/Omega) Z,
delta M(x)=x N delta lambda_g/(2 alpha).
```

Define

```text
E=1/(sigma^2 N^2),
A=v_f/f=1-f^2+a f^4,
S=v_ff-v_f/f=-2 f^2+4 a f^4,
P=2f'/f+2/x+(nu'-lambda_g')/2,
C=2/x+2f'/f-lambda_g'+alpha x f'^2,
R=f'/(2f)(nu'-lambda_g'+2/x)
  +exp(lambda_g)(Omega^2 exp(-nu)-A).
```

The registered two-channel equations are

```text
H''=-Lambda E H-P H'+2 C Z+2 Z'-delta_lambda_g R
    +[4 Omega^2 E
      +2 alpha x exp(lambda_g) f f'(Omega^2 exp(-nu)+A)
      +exp(lambda_g) S]H,

Z''=-Lambda E Z-2 Omega^2 E H'
    -C[(nu'-lambda_g')Z+Z']-J Z-(nu'-lambda_g')Z'
    -alpha Omega^2 E K,

J=2f''/f-2(f'/f)^2-2/x^2-lambda_g''
  +alpha(f'^2+2x f' f''),

K=(f^2+2x f f')Z+x f^2 Z'
  -x f(nu'-lambda_g'+2/x)(f'H-fZ)
  +2x exp(lambda_g) f^2 A H.
```

The implementation must verify the sextic Hessian, metric constraint, current relation, centre expansion, and exact term-by-term reduction to the published two-channel form. An amplitude-only or Cowling calculation is a registered mutation, not the model.

## Physical domain and boundary conditions

At the regular centre,

```text
H=H0+H2 x^2+O(x^4),
Z=Z1 x+O(x^3),
H2=Z1+[((4 Omega^2-Lambda)/sigma0^2+S(f0))/6] H0.
```

The primary solve normalizes `H0=1`. A two-basis centre construction with independent `(H0,Z1)` checks that this normalization misses no mode.

At infinity the additive scalar perturbation must lie in the two-dimensional decaying sideband subspace. The sideband exponents reduce asymptotically to

```text
k_plus=sqrt(1-(Omega+kappa)^2),
k_minus=sqrt(1-(Omega-kappa)^2).
```

The numerical outer projector is constructed from the two locally decaying eigenvectors of the full first-order pulsation matrix; decay is classified for the additive field, not for the relative variables `H,Z`. The projector is recomputed at each trial `Lambda` and domain. Accepted modes must also satisfy `delta Q(infinity)=0`, `delta M(infinity)=0`, zero scalar flux, and the discrete bound-mode condition below the first sideband continuum threshold whenever `Lambda>0`.

## Frozen probes and numerical methods

The canonical W3-65 coordinate is

```text
f_turn=2.188601437933647.
```

The registered branch probes are

```text
anchor=1.820210505787701,
f_turn-h,
f_turn,
f_turn+h,
h in {0.02,0.01,0.005,0.0025}.
```

Backgrounds are regenerated by adjacent continuation from the W3-64 anchor. No stored profile table is used as a substitute for the field equations.

Primary method: nonlinear collocation of the four first-order pulsation equations with the exact centre series, a dynamically constructed two-dimensional decaying outer projector, and `Lambda` as the BVP eigenparameter.

Independent method: propagate the complete two-dimensional regular centre subspace, compare it with the independently constructed two-dimensional decaying outer subspace by a scaled Evans/principal-angle determinant, and refine the matching minimum without using the collocation eigenfunction.

Controls:

```text
background radius=80,
background tolerances={1e-6,3e-7,1e-7},
mode outer radii={24,28,32},
mode centre epsilons={2e-5,1e-5,5e-6},
collocation tolerances={3e-6,1e-6,3e-7},
shooting tolerances={1e-8,3e-9,1e-9}.
```

The zero of the tracked nodeless mode is localized on the registered nested `h` set. Forward and backward mode continuation must retrace the same branch. Solver failure is `NUMERICALLY_INCONCLUSIVE`, never a physical endpoint or an instability.

## Acceptance gates

All of the following are required:

1. Dependency hashes, W3-64/W3-65 artifact validity, source ledger, fixed action, `alpha`, and sextic coefficient are exact.
2. The full two-channel equations, current relation, metric constraints, phase quotient, centre expansion, and potential Hessian pass symbolic/algebraic checks.
3. Every background re-passes W3-65 regular, nodeless, horizonless, residual, centre, and tail gates.
4. The primary and independent methods identify the same nodeless lowest mode. The next mode, if inside the registered discrete window, has one additional node and remains separated from the lowest mode.
5. Normalized pulsation-equation and centre residuals are below `3e-5`; normalized fixed-charge and ADM-mass boundary residuals are below `1e-6`.
6. The total deterministic eigenvalue error is the maximum domain, centre, background-tolerance, collocation-tolerance, and primary/independent discrepancies. It must be below `5e-4*max(|Lambda|,1e-2)`.
7. Every tested pre-turn sign is `Lambda0>5 error`; every immediate post-turn sign is `Lambda0<-5 error`; at the W3-65 turn `|Lambda0|<=5 error`.
8. The independently localized zero agrees with `f_turn` within `5e-4`; the last nested-root change is below `5e-4`; the last two crossing slopes have the same nonzero sign.
9. The near-zero physical kernel is simple after phase/gauge removal; adjacent tracked eigenfunctions have overlap above `0.95`; forward/backward retrace overlap exceeds `0.99`.
10. The W3-65 fixed-charge equilibrium tangent, after gauge/constraint projection, overlaps the physical zero mode above `0.98`.
11. Every registered mutation is detected.
12. The package contains exactly the three registered files and no subdirectory.

## Mutation controls

The verifier must reject: amplitude-only perturbations; Cowling/frozen metric; omission of `delta Q(infinity)=0`; admission of the constant U(1) phase mode; omission or sign reversal of either Einstein constraint; omission of the sextic term in `S`; reversal of the `Lambda` weight; replacement of the sideband projector by the background scalar Robin condition; drift of `alpha`, the action, metric count, operator, or source ledger; use of the static family tangent as a physical mode away from the turn; mode reordering without overlap/node tracking; sign declaration inside numerical error; and treatment of solver failure as physics. A known self-adjoint Sturm–Liouville benchmark must also be solved before the physical spectrum is accepted.

## Required true closure flags

```text
dependency_hashes_exact
upstream_artifacts_and_source_ledger_exact
fixed_action_metric_source_alpha_and_potential_exact
full_two_channel_radial_linearization_exact
physical_centre_and_decaying_outer_domain_pass
phase_gauge_quotient_and_fixed_charge_pass
background_regression_pass
primary_collocation_spectrum_pass
independent_evans_spectrum_pass
lowest_mode_identification_pass
simple_zero_and_transverse_crossing_pass
turning_point_agreement_pass
domain_resolution_tolerance_convergence_pass
equilibrium_tangent_to_physical_kernel_match_pass
mutation_controls_pass
package_clean_pass
aggregate_gate_pass
```

## Required false scope flags

```text
physical_alpha_from_foundation_derived
vacuum_to_anchor_branch_mapped
full_equilibrium_spiral_mapped
nonradial_stability_completed
nonlinear_stability_completed
collapse_evolution_completed
final_equilibrium_endpoint_derived
near_horizon_limit_derived
trapped_surface_derived
black_hole_solution_derived
geodesic_completeness_derived
singularity_resolution_completed
foundation_strong_field_response_derived
observational_likelihood_evaluated
```

## Permitted conclusion after PASS

At `alpha=0.04`, within the physical spherically symmetric fixed-charge linear sector, the nodeless lowest radial mode crosses a simple zero at the first W3-65 post-anchor simultaneous mass–charge turn. The tested pre-turn backgrounds have positive lowest squared frequency, while the immediate tested post-turn backgrounds have one negative radial mode. No broader stability or endpoint claim is implied.

## Package

Exactly three files belong to W3-66:

```text
w3_66_physical_radial_mode_preregistration.md
w3_66_physical_radial_mode.py
w3_66_result.json
```
