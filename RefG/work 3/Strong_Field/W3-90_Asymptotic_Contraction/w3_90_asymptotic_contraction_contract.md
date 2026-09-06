# W3-90: Non-bouncing contraction and the physical asymptote

## One decision, author intent and stopping rule

The author requests continued external operational shrinkage, asymptotically
approaching zero, with local material physics persisting. A reversal of the
areal radius is not the target. Test what the unchanged W87 action requires
for an initially contracting W89 spherical interior to remain at positive
areal radius for an infinite future radial-null affine length. Derive one
function-independent discriminator and check the existing operational map.

The new input is the full contraction equation away from a stationary radius,
together with independently parametrized radial null geodesics. W89's finite
turning-point test does not settle this question. The analytic targets below
were independently derived before this verifier; they are not blind predictions.

Create only this contract and w3_90_asymptotic_contraction.py in this directory.
Stop at the discriminator and the measurement-map audit. No chosen F(n), rho(n),
target metric, new matter component, numerical collapse scan, intuitive edit,
earlier-package edit, Git operation or publication is part of this stage.

## Frozen claim contract

- CLAIM_ID / TYPE / VERSION: W3_90_NONBOUNCING_AFFINE_CONTRACTION;
  EXACT_CONDITIONAL_DYNAMICAL_DISCRIMINATOR_AND_READOUT_AUDIT; v1.0.
- CLAIM: On the retained positive-current-clock KS branch, the weighted inward
  areal velocity increases in magnitude. A positive-radius future extending to
  infinite radial-null affine parameter requires finite integrated inverse
  gravitational stiffness. Bounded stiffness cannot support that continuation
  within this patch. The external material ruler is a different observable.
- ASSUMPTIONS / DOMAIN: W87 action and W89 valid flat-spin KS pair, signature
  (-+++), K>0, F(n)>0, rho(n)>0, n>0, mu>0; smooth nondegenerate metric at every
  finite state, initially bdot<0. Positive a,b,N in the patch. A monotone
  positive limiting b is a tested target, not an imposed solution. No assumption
  of finite limiting F, n, rho, a or mu is silently added.
- CONVENTIONS: Proper time d tau=N dt, longitudinal scale a, areal radius b,
  conserved j>0, n=j/(a b^2). F is the gravitational coefficient, not pressure.
  mu=rho'(n)+K T F'(n)=dtheta/dtau. Null affine parameter is lambda;
  P=|a^2 dx/dlambda|>0 fixes its arbitrary normalization. The new Q below is a
  weighted radial velocity, not the current charge. p_t,p_L are readout factors.
- FREEDOM_LEDGER: Only inherited symbolic F,rho,K, initial a,b,j and null
  normalization P; no physical constitutive choice or additional free scale.
  Elementary functions used in logical controls are not W87 solutions.
- DEPENDENCIES: W87 full density/current variation, W89 KS action/spin pair,
  W71 restricted static clock/ruler map, W81 integrability scope and W82
  observer-and-ray interface. Pin source versions and protected text hashes.
- METHOD: Recompute lapse, scale and current variations; eliminate constraint
  pointwise without differentiating it inside rho'. Derive the null geodesics
  and their Ricci projection from the metric. Compare proper-time and affine
  forms, then integrate the sign inequality. Check exact static readout limits.
- PASS_CONDITION / RESIDUAL / ERROR_BOUND: All registered exact identities
  vanish; actual expression mutations fail the same unchanged identity tests.
  No floating tolerance, numerical existence claim or observational PASS.
- FAIL_CONDITION / FALSIFIER: A failed variational, geometric, chain-rule or
  comparison identity defeats that component. A complete positive-radius KS
  contracting ray with uniformly bounded positive F and mu>0 would falsify
  the conditional obstruction. F unbounded alone never certifies a solution.
- VALIDITY_HEALTH: Check metric/current domain and existing positive-mu branch.
  Growing F changes focusing but does not certify full constrained stability,
  causal propagation of all modes, cutoff control or regular local matter.
- BRANCHES: Strict contraction with positive mu; constant-F regression;
  vacuum Einstein regression may have mu*n=0 and constant Q. A patch ending at
  a horizon or another finite-affine boundary needs an extension test and is
  not automatically a singular spacetime. Other geometries are outside scope.
- OBSERVABLE_MAP: b is defined by sphere area, not by oscillon size. Radial
  optical frequency uses emitter/receiver projections and null transport on
  the inherited metric-optics branch. mu is a local collective phase frequency,
  not an externally measured clock ratio. No n=P_F or F=1/p identification.
- FORWARD_MODEL / DATA_ROLE: Action to interior equation to geometric ray to
  exact comparison condition; no observational data or fitting.
- IDENTIFIABILITY / BENCHMARK: Discriminates bounded-F candidates from the
  proposed infinite-affine positive-radius continuation. It does not determine
  a unique F or reconstruct p_L from n. Static Schwarzschild clock/ruler limits
  and an independently derived radial Ricci contraction are benchmarks.
- CROSSCHECK: Independent hand derivations sharing only the action/domain;
  scale EL versus reduced constraint algebra; Christoffel geodesics and Ricci
  versus affine chain rule; same-evaluator negative controls.
- CLOSURE_FLAGS: Derive action_identity_checked, null_geometry_checked,
  weighted_focusing_checked, comparison_condition_checked, readout_scope_checked,
  mutation_controls_checked and conditional_bounded_F_obstruction.
  Keep external_shrinkage_trajectory_derived, microscopic_F_derived,
  full_coupled_health, actual_asymptote_constructed, singularity_resolved,
  regular_black_hole, global_completion, observational_pass,
  active_theory_changed and intuitive_files_changed false.
- PROVENANCE / FILES: SHA-256 source pins, contract/verifier hashes and package
  versions printed to stdout; Python -B, no caches or generated output files.

## 1. Exact contraction equation, with no bounce condition

In W89 conventions,

    ds^2=-N^2 dt^2+a^2 dx^2+b^2 dOmega^2,
    n=j/(a b^2), T=4 H_a H_b+2 H_b^2-2/b^2,
    L=-2K F(n)(a bdot^2+2b adot bdot)/N
      +2K N a F(n)-N a b^2 rho(n)+j thetadot.

Vary before N=1. In proper time, H_a=adot/a, H_b=bdot/b,
beta=n F'/F, P_m=n rho'-rho and mu=rho'+K T F'. The constraint and radial
equation, together with ndot=-n(H_a+2H_b), imply

    bddot+(Fdot/F-H_a)bdot=-b n mu/(4K F),
    d/dtau(F bdot/a)=-b n mu/(4K a)<0.

At bdot=0 this recovers W89's stationary-point identity. At bdot<0 it has
a different use: Fdot>0 contributes a positive term to bddot, permitting
slowing without reversing bdot. The other terms must also be evaluated;
Fdot>0 alone is not sufficient for positive bddot or a regular asymptote.

## 2. Null affine form and the invariant focusing term

Metric radial null geodesics have

    dtau/dlambda=P/a, dx/dlambda=+/- P/a^2.

Define Q=F db/dlambda. Directly derive

    dQ/dlambda=-P^2 b n mu/(4K a^2)<0,
    d^2b/dlambda^2+(d ln F/dlambda)(db/dlambda)
        =-b n mu/(4K F)*(P/a)^2.

The metric Ricci projection independently satisfies

    R_ab k^a k^b=-2 b^(-1) d^2b/dlambda^2
      =n mu/(2K F)*(P/a)^2
       +2(d ln F/dlambda)(db/dlambda)/b.

For contraction and increasing F, the second term is negative. It is a
genuine term in the candidate's field equations, not an apparent cure obtained
by changing length units. Its magnitude relative to the positive source term
decides local null defocusing. Global regularity remains a separate requirement.

## 3. Exact integral condition and bounded-F exclusion

Let Q(lambda0)=-q0<0. Then -Q(lambda)>=q0 throughout the same positive-mu
contracting patch, and

    b(lambda)=b0-integral_lambda0^lambda [-Q(s)]/F(s) ds.

A monotone positive limiting radius b_*>0 at lambda=infinity requires

    integral_lambda0^infinity [-Q(s)]/F(s) ds=b0-b_*<b0.

In particular integral d lambda/F must converge. Hence F cannot remain
uniformly bounded above on this ray. This does not imply pointwise F->infinity
without additional assumptions, and unbounded F alone does not suffice: even
F=1+lambda has divergent integrated inverse (an elementary mathematical
control, not a physical candidate). No necessary mu->0 claim is made.

If F<=Fmax on a future tail, choose lambda0 within that tail and define
b0=b(lambda0), q0=-Q(lambda0)>0 there. Then

    b(lambda)<=b0-q0*(lambda-lambda0)/Fmax.

Positive b cannot persist in this patch beyond lambda0+b0*Fmax/q0. Reaching
b=0 has W89's divergent KS curvature; exiting the patch first may instead
permit an extension. This is not a global no-go for regular black holes.

## 4. Translate the external zero into the correct observable

The intuitive external-shrinkage target is p_L>0 at each finite physical state,
p_L decreasing towards zero asymptotically, with oscillon/local-ruler ratios
preserved. The physical evolution parameter, reference observer, profile
assignment and ray protocol must be specified before that target is a solution.
No equality p_L=b, p_L=F^-1, n=p_L^-3 or mu=p_t follows from W87.

W71 already distinguishes clock and ruler factors on its exact static Einstein
benchmark. In isotropic radius, q=GM/(2 c0^2 rho_iso), 0<=q<1,

    p_t=(1-q)/(1+q), p_L=(1+q)^(-2),
    d tau=p_t dt, d ell=d rho_iso/p_L, c_coord=c0*p_t*p_L.

At q->1, p_t->0 and p_L->1/4. This is a one-sided static-coordinate limit;
it assigns no static observer to the horizon. Thus a clock factor reaching
zero and an external material ruler reaching zero are different statements.
The common leading weak-field response is not an exact universal strong-field
identification. The earlier conversational single-p shorthand must be read
as an intuitive target, not a map already derived for this dynamical interior.

W81 excludes one proposed universal scalar extension on a particular full
matter flow. W82 supplies protocol-dependent dynamic measurements once a
metric and observer paths are known. W87 specifies neither the physical F
nor a foundation-pressure/current/oscillon/ruler map. This is the precise
remaining input for testing the author's full operational-shrinkage mechanism;
relabeling F or the lapse as p_L would not supply it.

An elementary clock-only check illustrates why positivity and external
asymptotics are insufficient: p_t=(1+t)^(-2)>0 for t>=0 approaches zero only
at t=infinity, but integral_0^infinity p_t dt=1. This is not a spacetime or a
physical RefG solution; it falsifies only the inference that those two
properties alone guarantee unending internal proper time.

## 5. Required controls and precise result

Use actual altered expressions against unchanged production identities:
drop the Fdot/F term; drop K T F' from the current frequency; replace the
null affine conversion P/a by P*a; identify static p_t with p_L. Add only
controls needed to test the integral comparison and derivative bookkeeping.

The result is a derived condition for a non-bouncing continuation and a
checked boundary of the available measurement map. A successful verifier
does not construct a regular black hole or establish the author's desired
external-shrinkage trajectory. Stop rather than insert an arbitrary F or
additional metric solely to achieve that endpoint.

External context: Böhmer and Fiorini (2019),
https://doi.org/10.1088/1361-6382/ab1e8d, exhibit a limiting-radius interior in
a different vacuum Born-Infeld f(T) action. That model is not substituted for
the density-dependent W87 action, and its regularity is not inherited here.
