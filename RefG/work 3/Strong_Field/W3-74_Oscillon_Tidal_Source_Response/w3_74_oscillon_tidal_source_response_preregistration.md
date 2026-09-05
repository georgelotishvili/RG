# W3-74 — Oscillon response to a resolved gravitational environment

**CLAIM_ID:** W3_74_OSCILLON_TIDAL_SOURCE_RESPONSE

**CLAIM:** The inherited canonical ordinary-phase core has a definite linear quadrupolar response to a weak static vacuum tide: its field profile, action-conjugate source, and proper principal-axis lengths follow from the same action at fixed ordinary charge.

**TYPE:** EXACT_LINEAR_RESPONSE_EQUATIONS_AND_CONVERGED_NUMERICAL_BENCHMARK.

**MODEL_VERSION:** W3-74-v1.0-FIXED-CHARGE-TEST-CORE-STATIC-TIDE.

## Goal, barrier, minimal output, and stop

The immediate question is how the existing oscillon actually responds to a nonuniform environment. The inherited action already specifies its metric coupling. This package calculates that response before introducing an additional pressure-dependent interaction. The deliverable is one response coefficient and its proper-length interpretation at the existing core benchmark, with independent numerical checks. Stop after this calculation and its interpretation; no parameter survey, new potential, collapse evolution, or observational fit is opened.

Allowed files are this registration, its Python calculation, and one result JSON in this directory. Earlier calculations, the intuitive manuscripts, the dictionary, the Canon, and publication files remain unchanged.

## ASSUMPTIONS and DOMAIN

1. The ordinary-phase complex scalar is the minimal W3-58 field on the common W3-54 metric. Its potential coefficients retain their existing values; no new constitutive coefficient is introduced.
2. Take the W3-58 test-core limit: the core's gravitational backreaction is negligible. The imposed metric is a static external vacuum tidal perturbation in a local patch. W3-73's full self-gravitating evolution is the parent theory, not an equation solved numerically here.
3. Use the inherited nodeless localized branch at `a=g6*m^2/lambda^2=1/4`, `Omega=omega/m=4/5`. This is one benchmark, not a universal particle identification.
4. The deformation is stationary, even-parity, axisymmetric and `ell=2`. The conserved ordinary charge is fixed. A static continuation around the existing nondegenerate core is assumed in setting up linear response and tested by its Hessian.
5. The tidal amplitude is differentiated at zero. For finite illustrative amplitudes require both `|epsilon|*X^2 << 1` and `|epsilon*h/f| << 1` over the resolved core. The massive outer tail and the domain boundary are controlled by convergence. A quadratic external potential is a local probe, not a globally valid finite-amplitude spacetime.

## CONVENTIONS and inherited action

Signature `(-,+,+,+)`; natural units `c0=hbar=1`. Set `x=m*r`, `f=sqrt(lambda)*chi/m`, and measure stationary energy in `m/lambda`. Angular integrals include their full solid-angle normalization.

    Psi_O = (chi/sqrt(2))*exp(i*theta_O),
    S_O = - integral sqrt(-g) [ (partial chi)^2/2
             + chi^2*(partial theta_O)^2/2 + V(chi) ] d^4x,
    v(f) = f^2/2 - f^4/4 + a*f^6/6,
    theta_O = +Omega*t_dimensionless,
    j_O^mu = -chi^2*partial^mu(theta_O),   Q > 0.

The unperturbed profile obeys

    f'' + 2*f'/x = (1-Omega^2)*f - f^3 + a*f^5,
    f'(0)=0,   f'(X)+(sqrt(1-Omega^2)+1/X)*f(X)=0.

In fixed Newtonian/isotropic tidal coordinates put

    Phi = epsilon*x^2*P2(cos(theta)),  P2(z)=(3*z^2-1)/2,
    ds^2 = -(1+2*Phi)*dt^2 + (1-2*Phi)*d x_vector^2 + O(epsilon^2).

The central lapse is one and the central acceleration is zero. The local electric tidal tensor is `E_ij/m^2=epsilon*diag(-1,-1,2)` with the convention `E_ij=partial_i partial_j Phi`; `laplacian(Phi)=0`. The constant potential and uniform acceleration have already been removed by the choice of central frame.

## METHOD: action and source derivations

For a static metric with lapse `N` and spatial metric `gamma_ij`, the stationary fixed-frequency functional is

    F_Omega = E-Omega*Q
      = integral N*sqrt(gamma) [ gamma^ij*partial_i f*partial_j f/2
                               + v(f)-Omega^2*f^2/(2*N^2) ] d^3x.

At first order `N*sqrt(gamma)*gamma^ij=delta^ij`, `N*sqrt(gamma)=1-2*Phi`, and `sqrt(gamma)/N=1-4*Phi`. Consequently

    F_Omega = F0 + epsilon*integral x^2*P2*W(f) d^3x + O(epsilon^2),
    W(f)=2*Omega^2*f^2-2*v(f).

An independent Hilbert-source calculation gives `W=T00+T11+T22+T33` on the flat stationary core. It includes spatial stresses as well as energy density. This is the existing source, counted once.

Write `f_epsilon=f+epsilon*h(x)*P2+O(epsilon^2)`. Variation gives

    H2*h = S,
    H2 = -d^2/dx^2 - (2/x)*d/dx + 6/x^2 + U(x),
    U(x)=1-Omega^2-3*f^2+5*a*f^4,
    S(x)=2*x^2*(v'(f)-2*Omega^2*f).

Regularity requires `h=O(x^2)` at the centre. Use `h(X)=0` at large finite `X`; boundary dependence is part of the numerical test. The reduced response `y=x*h` obeys the symmetric tridiagonal discretization of `[-d^2/dx^2+6/x^2+U]*y=x*S`. Independently, `h=x^2*z` gives

    -z'' - 6*z'/x + U*z = 2*(v'(f)-2*Omega^2*f),
    z'(0)=0, z(X)=0.

Since `integral P2 dOmega=0`, the total charge has no first-order variation, including the perturbed proper-volume/lapse measure `sqrt(gamma)/N`. The inherited nonzero `dQ/dOmega` at the benchmark then fixes `delta Omega=0` at first order. Thus the linear shape is already a fixed-charge response. The second-order frequency correction cancels in the fixed-charge Legendre transform for the response term below.

Define the dimensionless profile-relaxation coefficient

    C_profile = (4*pi/5)*integral_0^X x^2*S*h dx.

For a positive `H2`, it is positive. The relaxed-profile contribution to the stationary energy is `-epsilon^2*C_profile/2`. The energy identity is

    integral x^2*S*h dx
      = integral [x^2*h'^2 + 6*h^2 + x^2*U*h^2] dx
        - [x^2*h*h']_0^X.

This coefficient refers to profile relaxation in the declared gauge. A full second-order tidal energy also contains explicit quadratic metric terms; a Love number requires the coupled metric response and exterior matching. Neither is inferred from `C_profile`.

## OBSERVABLE_MAP

Define a material contour by the scalar amplitude `f(r_c)=f(0)/2` at zero tide. Its central scalar value has zero first-order quadrupolar change. In the static rest slice the proper distance from the centre to that contour, along a principal axis, changes by

    delta(m*ell_axis) = -epsilon*[h(r_c)/f'(r_c)+r_c^3/3]*P2(axis),
    K_shape = d[m*(ell_pole-ell_equator)]/d epsilon at zero
            = -(3/2)*[h(r_c)/f'(r_c)+r_c^3/3].

The second term is the local ruler/metric contribution. Omitting it confuses a coordinate displacement with a proper length. Under a smooth radial coordinate shift fixing the centre, the contour displacement and integrated radial-metric correction cancel their opposite gauge shifts. The observable remains tied to this specified static rest slice and scalar contour.

At this order the angularly averaged amplitude, total charge, and mean contour radius do not change. The calculation tests anisotropic response to a tidal environment; it does not produce a uniform change of material scales. `W(f)` supplies the corresponding fixed-gauge source projection; its intrinsic derivative is `delta W=W'(f)*h*P2`.

## FREEDOM_LEDGER and BRANCHES

Inherited universal parameters `m,lambda,g6` enter through the fixed dimensionless benchmark. `epsilon` is the imposed environmental probe amplitude, not a fitted constant or an activation threshold. `X`, mesh spacing, tolerance and quadrature size are numerical controls. The half-central-amplitude contour is fixed before results. Only the nodeless test-core branch, static tracefree tide and its linear response are computed. Finite-self-gravity, monopolar pressure forcing, rapid evolution and finite-amplitude tides are separate domains.

## DEPENDENCIES

- W3-58 localized ordinary-phase action, core and Hessian: `../../Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/` relative to this package. The exact workspace-relative paths and hashes are recorded below.
- W3-73 common-metric coupled Einstein–complex-scalar action supplies the parent source ledger; its test-core limit is used, with no additional collective source.
- W3-71's distinction between intrinsic profile and remote ruler readout is retained. No operational density is substituted for foundation-volume density, and no universal local `p` is assumed.

Pinned paths relative to `work 3`:

| File | SHA-256 |
| --- | --- |
| Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_one_oscillon_coframe_localized_core.py | b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57 |
| Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_one_oscillon_coframe_localized_core_preregistration.md | ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db |
| Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_result.json | cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5 |
| Strong_Field/W3-73_Coupled_Horizon_Regular_Einstein_Complex_Scalar/w3_73_coupled_horizon_regular_einstein_complex_scalar_preregistration.md | 8a3c3887fc0a28edc8fced67da0bc66ccaff39ade1f6e5b7e339f579fc02c49e |

## BENCHMARK, CROSSCHECK, RESIDUAL and ERROR_BOUND

Freeze before numerical evaluation:

- Background: reuse W3-58's `solve_profile`, `a=0.25`, `Omega=0.8`, central seed unchanged, canonical `X=80`, tolerance `1e-8`; repeat `X=40,60,80` and canonical tolerance `1e-7`.
- Response: adaptive collocation for `z` at tolerances `1e-7,1e-8`, and independent reduced-field finite differences for `y` with spacings `0.04,0.02,0.01` at `X=80`; finite-difference domain repeats at `X=40,60,80` with spacing `0.01`.
- Quadrature: `8001,16001` points; angular factor independently integrated symbolically.
- Require relative changes of `C_profile` and `K_shape` below `2e-3` for finest mesh versus the next mesh, all tested domains, the two collocation tolerances, and independent methods. Normalization is `max(abs(reference),1)` for signed shape coefficients and `max(abs(reference),1e-30)` for positive coefficients.
- Require the lowest finite-difference `ell=2` Hessian eigenvalue above `1e-4`, with finest-mesh relative change below `2e-3`. This is numerical evidence for the benchmark, not a certified spectrum over all parameters.
- Require normalized response differential residual and energy-identity residual below `1e-5`; collocation solver residuals below their registered tolerance. Background normalized equation and virial residuals below `1e-5`. Require nonzero nodeless background with `f(0)>0.1`, positive charge, and decreasing profile through the registered contour.
- Test an independently manufactured regular reduced profile `y=x^3*(1-x/X)` under the same finite-difference radial operator. Require normalized solution error below `2e-3` and improvement with refinement.
- Mutation controls detect reversed forcing, energy-density-only forcing, dropped centrifugal term, dropped proper-ruler correction, and replacing the angular average of `P2` by unity. Their failure against the original equations is recorded rather than retuning the model.

Convergence differences are empirical numerical error estimates; no interval-certified error bound is claimed. Physical truncation errors are `O(epsilon^2)` in linear shape, neglected self-gravity in the test-core limit, and higher spatial/time variations of the external tide. The calculation does not supply an error-controlled extrapolation to a black-hole centre.

## PASS_CONDITION, FAIL_CONDITION and FALSIFIER

`PASS` is the logical AND of source/action identities, correct fixed-charge and proper-length maps, dependency checks, converged response, positive benchmark Hessian, residual checks, independent method and mutation controls. A failed numerical tolerance gives `NUMERICALLY_INCONCLUSIVE`; an exact identity/dependency failure gives `FAIL`. An independently verified nonpositive response operator invalidates the assumed static stable-response branch. A nonzero exact residual invalidates the claimed derivation. None of these outcomes rejects the entire theory outside the registered branch.

## VALIDITY_HEALTH

The principal scalar kinetic operator and the separately conserved ordinary `U(1)` current are unchanged. Only a static response is tested. Positivity of this static quadrupole Hessian does not establish the complete time-dependent spectrum. The source/action reciprocity is checked through both metric variation and profile variation; self-consistent gravitational backreaction remains in the parent system. The two phase currents and their densities are never identified here.

## FORWARD_MODEL, DATA_ROLE and IDENTIFIABILITY

`FORWARD_MODEL`: N/A for detector data; output is a local proper-length derivative and a gauge-specified source susceptibility. Waveforms, exterior multipole matching and inference are outside this package.

`DATA_ROLE`: no observational data, fits or new empirical comparisons. Existing W3-58 results are a development benchmark; recomputation and numerical crosschecks share its action and equilibrium branch.

`IDENTIFIABILITY`: the registered boundary problem determines the response at the benchmark. Its coefficients neither identify microscopic foundation constituents nor select a unique pressure–oscillon interaction. Standard scalar theories with the same action have the same response.

## CLOSURE_FLAGS and status boundary

All flags start `false`. Successful tests can close `dependencies_pinned`, `linear_action_and_source_exact`, `fixed_charge_selection_exact`, `proper_length_map_exact`, `response_converged_numerical`, `quadrupole_hessian_positive_numerical`, `independent_crosscheck_pass`, `mutation_controls_pass`, and their aggregate `local_tidal_response_pass`.

`foundation_pressure_feedback_derived`, `uniform_mass_radius_tail_scaling_derived`, `full_self_gravitating_tidal_love_number`, `nonlinear_collapse_solved`, `singularity_resolution_proved`, and `observational_pass` remain independent open tasks. In particular, the conjectured weakening of pressure depletion as external material scales decrease still requires its own dynamical closure.

## PROVENANCE and FILES

The Python output records the registration/source/dependency hashes, numerical package versions, all tests, numerical convergence and independent closure fields. Only these three files form the package:

- `w3_74_oscillon_tidal_source_response_preregistration.md`
- `w3_74_oscillon_tidal_source_response.py`
- `w3_74_result.json`

Context for the distinction between an internal response and a fully matched gravitational tidal deformability: Sennett et al., *Physical Review D* **96**, 024002 (2017), [original paper](https://arxiv.org/abs/1704.08651). The calculation here is derived from the displayed inherited action; no published Love number is used as its numerical target.
