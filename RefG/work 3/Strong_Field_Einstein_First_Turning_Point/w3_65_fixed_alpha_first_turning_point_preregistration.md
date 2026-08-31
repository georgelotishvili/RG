# W3-65 — First simultaneous mass–charge turn encountered after the W3-64 anchor

**CLAIM_ID:** `W3_65_ANCHOR_FORWARD_FIRST_TURNING_POINT_GATE`

**MODEL_VERSION:** `W3-65-v1.1-EH-SEXTIC-U1-FIXED-ALPHA-ANCHOR-FORWARD-FIRST-TURN`

## Purpose

W3-65 keeps the W3-64 Einstein–Hilbert operator, one metric, localized source ledger, sextic complex-scalar action, spherical ansatz, centre expansion and Schwarzschild-corrected tail unchanged. At the selected mathematical coupling `alpha=0.04`, it maps the nodeless equilibrium family in the increasing-`f_0` direction from the W3-64 anchor through the first simultaneous extrema of dimensionless ADM mass and Noether charge encountered in that registered direction.

The target is the first observable turning point encountered after the anchor in the registered increasing-`f_0` direction, not the first turn of the entire family and not its final endpoint. A turning point is accepted only after continuation through both sides, forward/backward retracing, nested-step localization, the on-shell branch first law, independent residual reconstruction and domain/tolerance convergence. Solver failure is never interpreted as physics.

## Design-history disclosure

Before this registration was frozen, a no-file pilot continuation was used only to identify the finite bracket `2.16<=f_0<=2.22` and to verify that the target precedes any static-chart horizon. All reported evidence is recomputed after this registration from the hash-pinned W3-64 anchor. The pilot output is not an artifact and is not used by the verifier.

## Immutable dependency

The verifier may read only these W3-64 files:

```text
w3_64_source_first_einstein_strong_field.py
SHA-256 4ecdd745404d1be64ec9f6f1220b9ce16ddfcd719178783758dcf2cc1fbe6499

w3_64_source_first_einstein_strong_field_preregistration.md
SHA-256 25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1

w3_64_result.json
SHA-256 5965c6aef9a3718ec4c028155a4ee3b10ed215f8201c45eec2ac01fbbaee4866
```

W3-64 must have `artifact_valid=true`, every closure flag true, one localized Einstein source `T_O`, no second metric and no new gravitational operator.

## Inherited exact system

No action coefficient, source or field equation is changed. In W3-64 dimensionless variables,

```text
N=1-2 alpha M/x,
M'=x^2 rho,
(ln sigma)'=alpha x[f'^2+Omega^2 f^2/(sigma^2 N^2)],
(sigma x^2 N f')'/(sigma x^2)
    +Omega^2 f/(sigma^2 N)-v_f=0,
v(f)=f^2/2-f^4/4+f^6/24.
```

The ordinary phase is harmonic, `theta_O=omega t`, `Omega=omega/m_s`, and `sigma(infinity)=1`. The finite-radius scalar boundary condition retains the W3-64 Schwarzschild power correction.

## On-shell branch first law

For stationary solutions of the same fixed action and fixed `alpha`, variation of the constrained energy gives

```text
dE_phys=omega_phys dQ_phys.
```

With the inherited normalizations

```text
E_phys=(4 pi m_s/lambda) M,
Q_phys=(4 pi/lambda) Q,
omega_phys=m_s Omega,
```

the dimensionless identity is

```text
dM/ds=Omega dQ/ds.
```

Because `Omega>0`, a nondegenerate stationary point of `Q` on a regular one-parameter branch is simultaneously a stationary point of `M`. The normalization is checked symbolically; the differential identity is checked numerically on the resolved branch.

## Frozen branch coordinate and continuation

The target is reached before any fold of the central amplitude itself. Therefore `f_0` is the registered local branch coordinate for this gate; `Omega` remains the BVP eigenvalue. This crosses extrema of `M`, `Q` and `Omega` without confusing them with an endpoint. W3-65 does not claim a complete pseudo-arclength map of the later spiral.

```text
a=1/4,
alpha=0.04,
anchor_f_0=1.820210505787701,
X=80,
initial_mesh=801,
relative_tolerance=1e-7,
maximum_nodes=100000,
centre_start_epsilon=1e-5.
```

The main forward grid is the hash-pinned inherited numerical anchor followed by `f_0=1.83,1.84,...,2.24`. The same grid is retraced backwards from `2.24` to the anchor. Every solve is seeded only by its adjacent accepted solution.

The turning bracket is frozen to `[2.16,2.22]`. It is recomputed on nested grids with steps `{0.01,0.005,0.0025}`. On each grid, natural cubic splines of `M(f_0)` and `Q(f_0)` are differentiated; the unique roots inside the bracket are the registered turning estimates. The canonical turning coordinate is the mean of the finest mass and charge roots. The branch-tangent probe uses `h=0.001` around the finest charge root.

## Frozen numerical controls

- Independent residual grid: `20001` points on `0.02<=x<=X-1`.
- Profile and quadrature grid at accepted points: `8001` points.
- Turning-point canonical profile: `16001` points.
- Branch-tangent linearized residual grid: `12001` points on `0.02<=x<=X-1`.
- Domain checks: `X={60,80,100}` at tolerance `1e-7`.
- Tolerance checks: `{1e-6,3e-7,1e-7}` at `X=80`.
- On every domain and tolerance control, the complete `[2.16,2.22]` turning bracket is rescanned at step `0.005`; both mass and charge roots are recomputed before comparing the turning coordinate and its observables.
- Turning localization steps: `{0.01,0.005,0.0025}`.
- The branch first-law residual is recomputed on all three nested turning grids and must improve from the coarsest to the finest grid.
- Tangent half-step: `0.001`.
- Forward/backward profile comparison grid: `2001` points.

## Acceptance gates

Every retained profile must be nodeless and outward nonincreasing within numerical error, with `sigma>0`, `N>0`, finite Ricci and Kretschmann diagnostics, finite ADM mass and charge, and the inherited NEC component checks.

The inherited W3-64 numerical gates remain:

```text
min f>=-1e-10,
max f'<=1e-8,
minimum NEC components>=-1e-12,
centre isotropy<1e-8,
independent scalar/mass/lapse/TOV residuals<3e-4,
centre residuals<3e-3,
Schwarzschild-corrected tail k and s errors<3e-3,
maximum compactness<1.
```

Additional W3-65 gates are:

```text
maximum forward/backward observable relative mismatch<5e-5,
maximum forward/backward full-state component relative L2 mismatch<5e-5,
branch first-law normalized L2 residual<2e-3,
mass and charge derivative signs are positive below and negative above the turn,
|f_turn_M-f_turn_Q|<5e-4,
maximum nested-step turning-coordinate change<5e-4,
turning-point domain/tolerance maximum relative change<5e-4,
|dQ/df_0|/max(|Q|,1)<1e-4 at the charge-root tangent probe,
|dM/df_0|/max(|M|,1)<1e-4 at the charge-root tangent probe,
normalized linearized branch-tangent ODE residual<3e-4,
normalized linearized branch-tangent boundary residual<3e-4.
```

The tangent of an exact equilibrium family lies in the null space of the extended static linearized equilibrium BVP, where the BVP eigenvalue `Omega` varies along with the profile. At the simultaneous `M,Q` turn this tangent is charge-conserving to the registered numerical accuracy. W3-65 calls it a **charge-conserving null tangent of the extended static linearized equilibrium BVP**. It is not identified with a physical radial zero-frequency eigenmode, does not identify a lowest radial eigenmode and does not determine the sign of the radial spectrum on either side.

## Endpoint semantics

The accepted event is `FIRST_POST_ANCHOR_SIMULTANEOUS_MASS_CHARGE_TURNING_POINT_IN_INCREASING_F0_DIRECTION`. It is neither the first turn of the entire family, the final equilibrium endpoint nor a horizon. The same runtime classifier used by the production path must map a last converged point, a singular collocation Jacobian, maximum-node exhaustion or any unclassified solver failure to `NUMERICALLY_INCONCLUSIVE`, never to a physical endpoint.

## Mutation controls

The verifier must detect or reject:

1. drift of `alpha` away from `0.04`;
2. a hard-coded anchor amplitude falsely used for every boundary condition;
3. a mass-only extremum with a displaced charge extremum;
4. omission of `Omega` from the first-law identity;
5. declaration of the last grid point as a turning point without a derivative sign change;
6. declaration of injected solver failure as a physical endpoint;
7. a nodeful profile admitted to the ground-state branch;
8. a tangent probe with nonconserved charge;
9. replacement of the Schwarzschild-corrected tail by the flat finite-radius Robin condition;
10. a second metric, a new gravity operator or a duplicated localized source.

## Required closure flags

```text
dependency_hashes_exact
w3_64_artifact_and_source_ledger_exact
fixed_action_metric_source_and_alpha_exact
branch_first_law_normalization_exact
anchor_regression_pass
forward_branch_segment_pass
backward_retrace_pass
branch_first_law_numerical_pass
simultaneous_mass_charge_turning_point_pass
turning_point_step_convergence_pass
turning_refinement_profiles_pass
turning_point_domain_tolerance_convergence_pass
charge_conserving_static_equilibrium_bvp_null_tangent_pass
regular_nodeless_horizonless_segment_pass
independent_residual_recomputation_pass
mutation_controls_pass
package_clean_pass
aggregate_gate_pass
```

## Required false scope flags

```text
physical_alpha_from_foundation_derived
vacuum_to_anchor_branch_mapped
full_pseudo_arclength_spiral_mapped
physical_radial_zero_frequency_eigenmode_derived
lowest_radial_eigenmode_derived
linear_radial_stability_completed
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

## Decision semantics

If every registered exact and numerical gate passes, the status is

```text
PASS_EXACT_UNCHANGED_EINSTEIN_SCALAR_FIXED_ALPHA_SYSTEM__CONVERGED_FIRST_POST_ANCHOR_SIMULTANEOUS_MASS_CHARGE_TURN_IN_INCREASING_F0_DIRECTION__CHARGE_CONSERVING_NULL_TANGENT_OF_EXTENDED_STATIC_EQUILIBRIUM_BVP__REGULAR_NODELESS_HORIZONLESS_RESOLVED_SEGMENT
```

This closes W3-65 and stops before radial-spectrum, collapse, near-horizon or foundation-response calculations.

## Package

Exactly three files belong to W3-65:

```text
w3_65_fixed_alpha_first_turning_point_preregistration.md
w3_65_fixed_alpha_first_turning_point.py
w3_65_result.json
```
