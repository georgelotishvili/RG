# W3-64 Preregistration: Source-First Einstein Strong-Field Gate

**CLAIM_ID:** `W3_64_SOURCE_FIRST_EINSTEIN_STRONG_FIELD_GATE`

**CLAIM:** The W3-58 ordinary-phase sextic `U(1)` core, coupled minimally and exactly once to the unchanged W3-54 Einstein--Hilbert geometry, generates a closed static spherical Einstein--matter boundary-value problem with a regular centre, conserved Hilbert source, asymptotically Schwarzschild exterior, and a regular horizonless self-gravitating continuation of the frozen W3-58 ground state. The currently retained W3-54 and W3-58 sources satisfy the null energy condition identically on their selected domains. Consequently, whenever a future configuration also satisfies the global hypotheses of the Penrose trapped-surface theorem, this retained source class excludes a null-complete trapped regular interior. The gate must therefore establish both the fully nonlinear horizonless relativistic continuation segment and the exact boundary that at least one Penrose hypothesis must change before a regular trapped-core continuation is possible, without adding a new gravitational operator.

**TYPE:** `CONDITIONAL_EXACT_EINSTEIN_BACKREACTION_AND_NEC_GATE_WITH_CONVERGED_NUMERICAL_HORIZONLESS_WITNESS`.

**MODEL_VERSION:** `W3-64-v1.1-EH-SEXTIC-U1-SOURCE-FIRST-SCHWARZSCHILD-TAIL`. Version 1.1 replaces the flat-leading finite-radius Robin condition by the first Schwarzschild-corrected asymptotic power. A further change to the inherited actions, source ledger, potential, spherical ansatz, harmonic branch, asymptotic conditions, frozen benchmark, gravitational-coupling grid, numerical tolerances, or trapped-surface decision semantics creates a new model version.

## Decision and stopping point

This stage tests the most conservative strong-field continuation available in the active RefG core:

```text
W3-54 one coframe -> TEGR-equivalent Einstein--Hilbert geometry
W3-58 one localized ordinary-phase Hilbert source
                       |
                       v
unchanged Einstein equations + exact localized backreaction
                       |
                       +-- regular horizonless self-gravitating core witness
                       +-- NEC/trapped-surface boundary for a regular black hole
```

The stage stops after the exact coupled equations, regular-centre and asymptotic maps, source-energy gates, one converged backreacted witness, and the current-source trapped-core decision. Rotation, collapse evolution, Love numbers, quasinormal modes, Hawking radiation, a new high-gradient operator, and observational fitting are outside this stage.

## Inherited action and one-count source ledger

Use units `c0=hbar=1` and signature `(-+++)`. The inherited bounded action is

```text
S = integral d^4x sqrt(-g) R/(16 pi G) + S_O[g,chi,theta_O],

S_O = - integral d^4x sqrt(-g)
      [1/2 g^mu_nu partial_mu chi partial_nu chi
       +1/2 chi^2 g^mu_nu partial_mu theta_O partial_nu theta_O
       +V(chi)],

V(chi)=m_s^2 chi^2/2-lambda chi^4/4+g_6 chi^6/6.
```

The asymptotically flat localized calculation sets the single vacuum slot to zero. The homogeneous W3-54 collective source is not counted as a second localized source. Its NEC identity is audited separately because it is part of the retained source class. The localized ledger is

```text
Einstein metric self-energy on the geometric side       1
ordinary localized action S_O -> Hilbert T^O_mu_nu      1
P_F, p, clock/ruler readouts re-added                    0
W3-51 active Gauss mass inserted                         0
W3-54 homogeneous phase source re-added locally          0
second metric or vacuum slot                             0
```

## Static spherical system

Adopt

```text
ds^2=-sigma(x)^2 N(x) dt^2+N(x)^(-1) dr^2+r^2 dOmega_2^2,
N(x)=1-2 alpha M(x)/x,
theta_O=omega t,
x=m_s r,
f=sqrt(lambda) chi/m_s,
Omega=omega/m_s,
a=g_6 m_s^2/lambda^2,
alpha=4 pi G m_s^2/lambda.
```

Define

```text
v(f)=f^2/2-f^4/4+a f^6/6,

rho = N f'^2/2 + Omega^2 f^2/(2 sigma^2 N) + v,
p_r = N f'^2/2 + Omega^2 f^2/(2 sigma^2 N) - v,
p_t =-N f'^2/2 + Omega^2 f^2/(2 sigma^2 N) - v.
```

The dimensionless field equations to be independently derived and checked are

```text
M' = x^2 rho,

(ln sigma)' = alpha x [f'^2+Omega^2 f^2/(sigma^2 N^2)],

[sigma x^2 N f']'/(sigma x^2)
  + Omega^2 f/(sigma^2 N) - [f-f^3+a f^5] = 0.
```

The Misner--Sharp mass is the function defined by `N`; the ADM mass is
`M_ADM=(4 pi m_s/lambda) M(infinity)`. Neither is identified with the W3-51 active Gauss charge, W3-58 fixed-coframe proper energy, or an operational `m_eff` readout.

## Regular-centre and asymptotic conditions

At the centre,

```text
f=f_0+f_2 x^2+O(x^4),
M=M_3 x^3+O(x^5),
sigma=sigma_0[1+s_2 x^2+O(x^4)],

f_2=[f_0-f_0^3+a f_0^5-Omega^2 f_0/sigma_0^2]/6,
M_3=[Omega^2 f_0^2/(2 sigma_0^2)+v(f_0)]/3,
s_2=alpha Omega^2 f_0^2/(2 sigma_0^2).
```

At infinity,

```text
sigma -> 1,
M -> M_infinity,
k=sqrt(1-Omega^2),
d=alpha M_infinity,
s=-1+d(2 Omega^2-1)/k,
f -> C exp(-k x) x^s [1+O(1/x)],
0<Omega<1.
```

The scalar tail is exponential rather than compactly supported. The finite-radius boundary condition is `f'+(k-s/X)f=0`; it retains the first Schwarzschild power correction and reduces to `f'+(k+1/X)f=0` at `alpha=0`. The metric is therefore asymptotically Schwarzschild, with exponentially suppressed matter corrections, rather than exactly vacuum Schwarzschild at a finite matching radius.

## Frozen numerical witness

The upstream matter point is fixed before backreaction:

```text
a=1/4,
f_0=1.820210505787701,
alpha_grid={0,0.01,0.02,0.03,0.04},
X=80,
initial_mesh=801,
relative_tolerance=1e-7,
maximum_nodes=100000.
centre_start_epsilon=1e-5,
independent_residual_grid=20001,
independent_residual_centre_cut=0.02,
independent_residual_outer_cut=1,
quadrature_grids={4001,8001,16001},
tail_fit_window={x>3,1e-12<f<1e-5},
tail_fit_minimum_samples=50,
tail_fit_model={ln f=c-k_fit x+s_fit ln x+b_1/x+b_2/x^2},
curvature_centre_cut=0.02,
equation_mutation_residual_grid=12001,
equation_mutation_residual_domain={0.02<=x<=X-1}.
```

`Omega` is the eigenvalue and `sigma(infinity)=1` fixes the time normalization. Continuation proceeds in increasing `alpha`. The canonical backreacted witness is `alpha=0.04`. Domain/tolerance checks use `X={60,80,100}` and tolerances `{1e-6,3e-7,1e-7}`. No parameter is fitted to a target compactness, horizon, mass, radius, or observation.

The registered numerical gates are: `min f>=-1e-10`, `max f'<=1e-8`, scalar NEC component minima `>=-1e-12`, centre isotropy `<1e-8`, independently recomputed normalized scalar/mass/lapse/TOV residuals `<3e-4`, centre-series residuals and both Schwarzschild-corrected fitted tail-parameter errors `|k_fit-k|,|s_fit-s|<3e-3`, `max C<1`, finite Ricci and Kretschmann diagnostics, and relative convergence of `Omega`, ADM mass, charge, charge-rms radius and maximum Kretschmann scalar below `5e-4` across the frozen grid. Actual-equation mutation controls require the unmodified mass/lapse residuals `<3e-4` and each registered mutated residual `>0.1`.

## ASSUMPTIONS

1. W3-54 supplies the selected one-coframe TEGR-equivalent Einstein--Hilbert branch and Hilbert convention.
2. W3-58 supplies the selected canonical complex ordinary-phase sextic action, strict vacuum point `a=1/4`, and positive nodeless flat-coframe ground state.
3. The isolated localized calculation is asymptotically flat and uses the single zero vacuum slot.
4. The tested equilibrium is static, spherically symmetric, nodeless, and harmonic in the ordinary phase.
5. The W3-58 coefficients remain selected continuum inputs; this stage does not derive them from nodes.
6. The Penrose implication is restricted to its declared global hypotheses: a globally hyperbolic spacetime with a noncompact Cauchy hypersurface, a closed trapped surface, and null convergence.

## DOMAIN

The exact equations cover the minimally coupled W3-58 field on the static spherical W3-54 Einstein branch with `a=1/4`, `alpha>=0`, `0<Omega<1`, `sigma>0`, and `N>0` for the numerical witness. The trapped-surface implication covers the same retained source class under the stated Penrose hypotheses. Rotating synchronized hair, charged fields, nonminimal curvature coupling, topology change, loss of global hyperbolicity, quantum stress, higher-gradient foundation dynamics, and modified gravitational operators lie outside this model version.

## CONVENTIONS

Prime denotes `d/dx`. `M(x)` is dimensionless and defines the Misner--Sharp mass through `N`. The time coordinate is normalized by `sigma(infinity)=1`. Local orthonormal stresses use `T_hat(a)hat(b)=diag(rho,p_r,p_t,p_t)` after extracting the common factor `m_s^4/lambda`. The radial compactness is `C(x)=2 alpha M(x)/x`.

## FREEDOM_LEDGER

- `a=1/4` and `f_0` are pinned to the W3-58 benchmark.
- `alpha` is the single new dimensionless gravitational coupling. The registered grid tests mathematical continuation and is not assigned a physical particle value.
- `Omega` is an eigenvalue fixed by regularity and decay, not a fitted input.
- `sigma_0` is a shooting normalization fixed by `sigma(infinity)=1`.
- No profile, switching function, curvature threshold, equation of state, surface radius, mass, or observational parameter is added.

## DEPENDENCIES

- W3-54 contract SHA-256: `6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879`.
- W3-58 preregistration SHA-256: `ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db`.
- W3-58 result SHA-256: `cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5`.
- W3-51 is a regression boundary only: its biconformal metric is a weak-field construction and is not extrapolated here.
- W3-41 and W3-47 exclude local compact deficits from their domains and supply no strong-field constitutive law.

## METHOD

1. Hash-verify W3-58's covariant Hilbert stress and scalar variation, then independently derive their static spherical components, the Einstein tensor, reduced scalar equation, exact flat limit, dimensional normalization, centre series, Schwarzschild-corrected asymptotic tail, Misner--Sharp/ADM map, and anisotropic conservation identity.
2. Prove the exact source-energy identities

   ```text
   rho_O+p_r_O=N f'^2+Omega^2 f^2/(sigma^2 N)>=0,
   rho_O+p_t_O=Omega^2 f^2/(sigma^2 N)>=0,
   T^O_mu_nu k^mu k^nu=(k.partial chi)^2+chi^2(k.partial theta_O)^2>=0,
   rho_C+p_C=n_C rho_C'(n_C)>0.
   ```

3. Derive the round-sphere null-expansion product `theta_+ theta_-=-4N/x^2`, and register the Penrose implication: retained Einstein geometry plus retained NEC sources plus a closed trapped surface and the theorem's global hypotheses imply null geodesic incompleteness.
4. Solve the frozen coupled boundary-value problem by adaptive collocation and continuation in `alpha`.
5. Recompute the canonical point across the frozen domain/tolerance grid. Independently recompute equation, Einstein-constraint, anisotropic-TOV, centre-series, tail, curvature, mass, charge, and compactness residuals on uniform quadrature grids.
6. Apply negative controls to the actual mass and lapse residual equations for a duplicated source, a sign-flipped Einstein coupling and a missing lapse source; apply structural registry controls for a second metric, a W3-51 strong-field insertion, local re-addition of `T_C`, and an NEC sign mutation.

## PASS_CONDITION

All action, stress, ODE, centre, tail, mass, conservation, NEC, round-sphere expansion and trapped-surface implication registries pass exactly. Dependency hashes and the one-localized-source ledger are exact. Every continuation point converges to a positive nodeless decaying profile with `sigma>0` and `N>0`. The `alpha=0` solution reproduces the W3-58 `Omega`, energy and charge within `3e-4`. Across the canonical convergence grid, relative changes in `Omega`, ADM mass, charge, charge-rms radius and maximum Kretschmann scalar remain below `5e-4`. Independently recomputed normalized scalar, mass-constraint, lapse and TOV residuals remain below `3e-4`; centre-series and Schwarzschild-corrected tail residuals remain below `3e-3`; `max C(x)<1`; all mutation controls are detected.

## FAIL_CONDITION

Any exact action, source, sign, normalization, NEC, conservation, centre, asymptotic, mass-ledger, dependency, source-count, or theorem-scope registry fails. The numerical witness fails if continuation loses regularity, positivity, decay, `N>0`, convergence, or the registered error budget. Solver failure is `NUMERICALLY_INCONCLUSIVE` for the witness and does not reverse the exact NEC/trapped-surface implication.

## FALSIFIER

The exact current-source boundary is falsified by a valid configuration in the declared Einstein/source class that satisfies every Penrose hypothesis, contains a closed trapped surface, remains null-geodesically complete, and preserves the registered NEC identities. A future foundation-derived source that violates one theorem hypothesis creates a new model version; it does not retroactively alter this gate.

## RESIDUAL

Exact symbolic zero is required for the dimensional reduction, stress identities, centre coefficients, conservation identity, flat limit, and source ledger. Numerical residuals are reported separately with the registered thresholds.

## ERROR_BOUND

Exact identities carry zero algebraic error in the declared class. The equilibrium witness is `NUMERICAL_EVIDENCE` on the frozen domains, tolerances and quadrature grids. It is not an interval-certified existence proof and carries no observational error model.

## VALIDITY_HEALTH

The inherited scalar has a positive canonical kinetic term and a nonnegative potential bounded from below at `a=1/4`. The retained sources satisfy NEC. The numerical continuation segment must remain horizonless, asymptotically flat, finite-energy and free of coordinate degeneration. Radial dynamical stability at fixed `alpha`, nonlinear collapse stability, and a near-horizon completion beyond the first turning point are separate gates.

## BRANCHES

- `ALPHA_ZERO_REGRESSION`: exact W3-58 flat-coframe limit.
- `REGULAR_HORIZONLESS_BACKREACTION`: continued `N>0` self-gravitating Q-ball/Q-star witness.
- `TRAPPED_REGULAR_BLACK_HOLE_WITH_CURRENT_SOURCES`: excluded under the registered Penrose hypotheses if the exact NEC gate passes.
- `ROTATING_OR_NONMINIMAL_BRANCHES`: outside this model version.

## OBSERVABLE_MAP

The stage produces the asymptotic-time-normalized scalar eigenfrequency `Omega`, Noether charge, local energy density and stresses, Misner--Sharp mass, ADM mass, charge-rms radius, lapse, and compactness. The local proper angular frequency is `omega/(sigma sqrt(N))`. The stage assigns no observed particle species and no black-hole observable.

## FORWARD_MODEL

Input: the inherited actions and frozen dimensionless benchmark. Output: one registered set of static spherical equilibria across the declared `alpha` grid and its exact source-energy classification. This grid tests continuation of the equations across couplings; it is not a fixed-theory stability branch. There is no telescope, waveform, likelihood, or detector model.

## DATA_ROLE

`N/A`: no observational data are read or fitted. W3-58 generated values are a pinned upstream theoretical benchmark used only for the `alpha=0` regression.

## IDENTIFIABILITY

The coupled equations identify `Omega`, `sigma`, the dimensionless mass profile and charge for each registered `(a,f_0,alpha)`. They do not select the physical value of `alpha=4 pi G m_s^2/lambda`, because `m_s` and `lambda` remain foundation-selected inputs. The current-source no-go establishes that at least one Penrose hypothesis must fail before a null-complete trapped regular interior is possible; it does not select which hypothesis changes.

## BENCHMARK

Recover W3-58 at `alpha=0`, then continue the same central-amplitude state to `alpha=0.04`. Report `Omega`, `sigma_0`, `M_ADM`, charge, charge-rms radius, maximum compactness, minimum `N`, centre coefficients, tail exponent, and every registered residual.

## CLOSURE_FLAGS

Required true:

```text
dependency_hashes_exact
one_einstein_metric_exact
one_localized_hilbert_source_exact
einstein_scalar_odes_exact
dimensionless_field_reduction_exact
dimensionless_mass_normalization_exact
alpha_zero_equation_limit_exact
regular_centre_series_exact
asymptotic_schwarzschild_yukawa_map_exact
misner_sharp_adm_mass_roles_exact
ordinary_scalar_nec_exact
covariant_scalar_nec_exact
collective_phase_nec_exact
anisotropic_tov_conservation_exact
round_sphere_null_expansion_exact
penrose_trapped_surface_implication_registered_exact
alpha_zero_w3_58_regression_pass
regular_horizonless_backreaction_witness_numerical
domain_tolerance_convergence_pass
curvature_convergence_pass
independent_residual_recomputation_pass
mutation_controls_pass
aggregate_gate_pass
```

Required false:

```text
physical_alpha_from_foundation_derived
localized_core_coefficients_from_nodes_derived
regular_trapped_black_hole_from_current_sources_derived
singularity_resolution_completed
rotation_completed
collapse_evolution_completed
backreacted_radial_stability_completed
love_number_or_qnm_derived
observational_likelihood_evaluated
near_horizon_endpoint_derived
fixed_alpha_equilibrium_branch_derived
geodesic_completeness_derived
```

## CROSSCHECK

The scalar equation is obtained both from covariant variation and from the reduced spherical action. The lapse equation is checked against `G^r_r-G^t_t`; the mass equation against `G^t_t`; the matter equation against anisotropic TOV conservation. The `alpha=0` limit is checked against W3-58. Numerical collocation residuals are recomputed independently on uniform grids. The trapped-core decision is checked both by direct NEC contraction and by the stress-component identities.

## PROVENANCE

The verifier is deterministic Python/SymPy/NumPy/SciPy. It reads only the hash-pinned active W3-54 and W3-58 dependencies. Primary theorem references are R. Penrose, *Gravitational Collapse and Space-Time Singularities*, Physical Review Letters 14, 57 (1965), DOI `10.1103/PhysRevLett.14.57`; D. J. Kaup, *Klein-Gordon Geon*, Physical Review 172, 1331 (1968), DOI `10.1103/PhysRev.172.1331`; J. D. Bekenstein, *Transcendence of the Law of Baryon-Number Conservation in Black-Hole Physics*, Physical Review Letters 28, 452 (1972), DOI `10.1103/PhysRevLett.28.452`; and S. Coleman, *Q-balls*, Nuclear Physics B 262, 263 (1985), DOI `10.1016/0550-3213(85)90286-X`.

## FILES

Exactly three files belong to the package:

```text
w3_64_source_first_einstein_strong_field_preregistration.md
w3_64_source_first_einstein_strong_field.py
w3_64_result.json
```

## Decision semantics

If every exact and numerical gate passes, the status is

```text
PASS_CONDITIONAL_EXACT_UNCHANGED_EINSTEIN_BACKREACTION_AND_CURRENT_SOURCE_NEC_BOUNDARY__CONVERGED_NUMERICAL_REGULAR_HORIZONLESS_SELF_GRAVITATING_Q_BALL_WITNESS__REGULAR_TRAPPED_NULL_COMPLETE_INTERIOR_REQUIRES_FAILURE_OF_AT_LEAST_ONE_PENROSE_HYPOTHESIS
```

This closes the first source-first strong-field gate and stops.
