# W3-89: Spherical interior turning-point test of the W87 postulate

## One decision and stopping rule

Test the proposed density-dependent gravitational response in an anisotropic
spherical interior. Determine whether it permits a smooth positive minimum
of the areal radius on W87's already retained positive-phase-clock branch.
Microscopic derivation of the postulate is deferred by the user's instruction.
The action remains exactly W87; no particular F or matter energy function is
chosen to obtain a desired outcome. This is a new interior test, not a repeat
of the flat homogeneous cell or a full black-hole construction.

The identities below were derived by hand and independently checked before
this verifier. They are known analytic targets, not blind predictions. Freeze
this contract before execution. Stop after the turning-point decision, its
source-branch diagnostic and independent checks. Create exactly this contract
and w3_89_spherical_turning_point.py. No scans, evolution runs, extra reports,
manuscript or intuitive edits, Git operations, or publication.

## Claim contract

- CLAIM_ID / TYPE / MODEL_VERSION: W3_89_KS_POSITIVE_CLOCK_TURNING_POINT;
  EXACT_CONDITIONAL_LOCAL_OBSTRUCTION, W87 action v1.0 on the KS branch.
- CLAIM: On the real flat-spin-compatible Kantowski-Sachs (KS) branch, any
  regular finite areal-radius stationary point obeys
  bddot/b=-n*mu_eff/(4*K*F). Hence positive finite K,F,n,mu_eff forbid a
  nondegenerate radius minimum there. The negative-mu sector is classified
  separately by a fixed-geometry current diagnostic, not a full ghost theorem.
- ASSUMPTIONS / DOMAIN: Signature (-+++), K>0, conserved future timelike
  current, n>0, F(n)>0, rho(n)>0, differentiable functions. Finite positive
  lapse N and scale factors a,b, sufficiently smooth in this coordinate patch.
  The positive-clock condition mu_eff>0 is inherited from W87, not introduced
  after seeing the turning-point result. At a candidate turning point bdot=0.
- CONVENTIONS: t is coordinate time; overdots in final equations denote
  proper time d tau=N dt. Coordinates (t,x,theta,phi), b is areal radius,
  a the longitudinal scale, V=a*b^2 per unit x and unit solid angle.
  T is the TEGR torsion scalar with W87's sign; rho is rest energy density.
- FREEDOM_LEDGER: Universal symbolic F,rho and K; no extra function, profile,
  initial condition, new scale or fitted parameter. Geometry adds the KS
  symmetry assumption; discrete real connection orientations are equivalent
  for the stated scalar and spin test. Use the + orientation below.
- DEPENDENCIES: W87 full current/density variation and spin equation, and its
  positive-clock domain. W54 supplies the TEGR sign convention. W88 is context
  only and supplies no physical current/coframe identification here.
- METHOD: Compute connection flatness, torsion scalar and all six spin
  equations before reducing. Vary the lapse, scales, current and phase while
  retaining the composite n dependence. Check the radius equation both in a,b
  and logarithmic scales. Evaluate turning-point and current-sign identities.
- PASS_CONDITION / RESIDUAL / ERROR_BOUND: Required exact residuals simplify
  to zero; sign implications hold on declared positive domains; every actual
  altered-expression control fails the corresponding baseline evaluator.
  No floating tolerance or observational PASS. A verifier PASS certifies the
  local conditional result, not the requested global singularity resolution.
- FAIL_CONDITION / FALSIFIER: A nonzero required residual defeats that
  identity. A positive-mu regular KS point with bdot=0 and bddot>0 would
  falsify the stated conditional obstruction. This is not a no-go for all
  RefG, all F*T continuations, other current branches or inhomogeneous collapse.
- VALIDITY_HEALTH / BRANCHES: Check flatness and antisymmetric equations;
  lapse variation precedes gauge fixing. Retain mu>0,mu=0,mu<0 distinctly.
  At mu=0 the fixed-geometry spatial-current inversion is singular. At mu<0
  its phase block has a wrong kinetic or spatial-gradient sign when invertible.
  Metric/connection constraint mixing and complete perturbative health remain
  uncomputed. The reduced gravitational Hessian is not a health certificate.
- OBSERVABLE_MAP: Metric areal radius, proper-time acceleration and metric
  Kretschmann scalar. The local fixed-background phase block is a diagnostic,
  not the full constrained characteristic system or an observer-scale change.
- FORWARD_MODEL / DATA_ROLE: N/A; no observations, fitting or synthetic
  trajectory. Schwarzschild interior is an exact GR regression, not data.
- IDENTIFIABILITY / BENCHMARK: A function-independent sign relation tests the
  finite-radius bounce mechanism. Compare F=1 with Einstein's interior and
  compare the valid KS spin pair with the misleading static-spherical pair.
- CROSSCHECK: Coordinate torsion calculation versus the cited covariant KS
  pair; direct scale variation versus logarithmic variation; metric curvature
  from Levi-Civita connection versus orthonormal expression and Schwarzschild;
  canonical current expansion versus its quadratic Legendre elimination.
  Independent review shares the W87 action and the stated symmetry premises.
- CLOSURE_FLAGS: Compute provenance, flat_spin_pair, torsion_scalar,
  lapse_preserving_KS_variation, turning_point_identity,
  fixed_geometry_current_diagnostic, curvature_regression, mutation_controls.
  Conditional_positive_clock_local_bounce_excluded follows from these tests.
  Keep global_singularity_resolved, regular_black_hole, all_regular_branches_excluded,
  full_coupled_health, microscopic_F_derived, observational_pass,
  active_theory_changed and intuitive_files_changed false.
- PROVENANCE / FILES: Pin this contract, CODES, W87 contract/verifier and
  protected intuitive files; print verifier hash and Python/SymPy versions.
  Python -B; finite JSON stdout only, no caches or output files.

## 1. Real covariant spherical interior

Use

    ds^2=-N^2 dt^2+a^2 dx^2+b^2(dtheta^2+sin(theta)^2 dphi^2),
    e^A_mu=diag(N,a,b,b*sin(theta)),
    omega^1_2=sin(theta) dphi,
    omega^1_3=-dtheta,
    omega^2_3=-cos(theta) dphi,

with antisymmetric spatial partners and zero temporal components. Compute
d omega+omega wedge omega=0 and the W87 spin equation

    D_nu[e e_[A^nu e_B]^mu partial_mu F]=0.

All six equations vanish for F(t). The usual static-spherical connection
omega^1_2=-dtheta, omega^1_3=-sin(theta)dphi, omega^2_3=-cos(theta)dphi
is also flat but fails the time-dependent-F spin test. Its reduced torsion
scalar happens to agree here; checking the scalar alone misses this failure.

On the valid pair, H_a=adot/(N*a), H_b=bdot/(N*b), and

    T=4 H_a H_b+2 H_b^2-2/b^2.

The last term is intrinsic sphere curvature; deleting it changes the geometry.
The homogeneous current has J^t=j*sin(theta), other components zero, so
n=j/(a*b^2) independently of N. Adapt the geometry from the primary references;
derive the composite-density field equations anew, not from f(T) matter FEs.

## 2. Action-first reduction and the decisive identity

The W87 action gives, per unit longitudinal length and solid angle,

    L=-2K F(n)[a*bdot^2+2b*adot*bdot]/N
      +2K N a F(n)-N a b^2 rho(n)+j*thetadot.

Vary N,a,b,j,theta before choosing N=1. Define
P=n rho'-rho, beta=n F'/F, gamma=n rho'/rho, and mu_eff=rho'+K*T*F'.
The resulting proper-time equations are

    2KF(2H_a H_b+H_b^2+b^-2)=rho,
    jdot=0, thetadot=mu_eff,
    2 dotH_b+(1-beta)(3H_b^2+b^-2)+P/(2KF)=0,
    dotH_a+dotH_b+(1-beta)(H_a^2+H_a H_b+H_b^2)
      -beta/b^2+P/(2KF)=0.

At H_b=0 with finite positive a,b,F,n, the constraint and current variation give

    rho=2KF/b^2,  T=-2/b^2,
    mu_eff=(rho/n)(gamma-beta),
    bddot/b=dotH_b=(beta-gamma)/(2b^2)=-n*mu_eff/(4KF).

Therefore a nondegenerate positive-radius minimum requires beta>gamma and
mu_eff<0. On the inherited strictly positive-clock branch every such stationary
point is a local maximum. The equality mu=0 needs higher-order analysis; the
present calculation neither permits nor excludes a degenerate minimum there.
For a continuous trajectory starting at mu>0 and reaching a mu<0 bounce,
the zero of mu must be accounted for rather than skipped by a numerical solver.

## 3. What the sign change means, and what it does not establish

At fixed metric and fixed torsion scalar write E(n;T)=rho(n)+KT F(n).
Then E_n=mu_eff and h=E_nn. In a local rest frame let deltaJ0, deltaJi
be current perturbations and pi the phase perturbation. After removing the
background linear terms the quadratic first-order current action is

    L2=deltaJ0*pi_dot+deltaJi*partial_i pi
       -h*(deltaJ0)^2/2+mu_eff*deltaJi*deltaJi/(2n).

For h and mu nonzero, eliminating these auxiliary currents yields

    L2=pi_dot^2/(2h)-n*(grad pi)^2/(2mu_eff).

Positive h,mu give the ordinary signs. Negative mu gives a wrong spatial
sign if h>0 and a wrong temporal sign if h<0; h=0 or mu=0 makes the respective
algebraic inversion degenerate. This is an explicit fixed-geometry diagnostic.
The complete nonminimal theory mixes current, coframe and connection constraints;
no full coupled ghost or instability theorem is inferred from this block alone.
The change of phase sign is not by itself a reversal of physical time.

## 4. Curvature and scope of the result

For the metric above, in proper time,

    Kretschmann=4[(addot/a)^2+2(bddot/b)^2
                  +2(H_a H_b)^2+(H_b^2+b^-2)^2] >= 4/b^4.

Thus b approaching zero within this KS patch is not regularized by merely
slowing its approach: metric curvature diverges there. This statement concerns
the KS time-dependent-radius patch. An inner horizon leading to a different
patch, an asymptotic positive-radius region, or a genuinely inhomogeneous
solution is outside the local turning-point test. Even bounded curvature
would additionally require causal extension/geodesic analysis for a complete
singularity claim. No global black-hole verdict is silently inferred.

For the exact Einstein regression F=1 and absent current, take 0<b<2M,
a=sqrt(2M/b-1), bdot=-a, adot=M/b^2. The vacuum KS equations must vanish
and Kretschmann must equal 48 M^2/b^6. This is a geometry/sign regression;
it is not an assertion that the n>0 matter branch has reached vacuum.

## 5. Actual negative controls and final decision

Require failures when: (i) the static-spherical spin pair replaces the valid
KS pair; (ii) the intrinsic -2/b^2 torsion term is omitted; (iii) F is frozen
during density-dependent scale variation; (iv) KT F' is omitted from current
variation; (v) the bddot/mu relation has its sign reversed; (vi) the eliminated
spatial phase-gradient term has its sign reversed. Apply the same residual
evaluators as for the baseline, retaining nonzero residuals or exact witnesses.

Outcome: the postulate changes the interior equations, but the finite-radius
bounce route crosses W87's retained positive-clock domain and triggers a real
current-sector diagnostic. A healthy nonsingular black hole is therefore not
established. The specific result is the local sign obstruction; other routes
and the full coupled health question remain OPEN. Stop rather than fitting a
function or adding another term to manufacture the requested conclusion.

## Primary geometry references

- Coley, Landry, van den Hoogen and McNutt, Spherically symmetric teleparallel
  geometries, EPJC 84,334 (2024), section 5, equations 103,107,110:
  https://doi.org/10.1140/epjc/s10052-024-12629-5 .
- van den Hoogen and Forance, Teleparallel Geometry with Spherical Symmetry:
  The diagonal and proper frames, section 6.2, equations 104-105:
  https://arxiv.org/html/2408.13342v2#S6.SS2 .

Their geometric pair is used and recomputed here. Their independent f(T)
matter equations are not substitutes for the composite-density W87 variation.
