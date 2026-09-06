# W3-85: Regular black-hole benchmark and retained-source test

## Decision and stopping rule

Recover one published curvature-regular black-hole solution from its stated
spherical variational problem, then decide whether the retained RefG canonical
scalar source can support that exact metric in unchanged Einstein gravity.
This is a direct source-representability test. The published gravitational
response is external input, not a new RefG postulate or a microscopic result.
Stop after the exact identities, horizon/centre checks and source decision.
Do not add a parameter search, collapse simulation or another missing-law report.

Only this contract and `w3_85_regular_centre.py` may be created. Existing theory,
intuitive files and earlier packages remain unchanged. Output is finite JSON
to stdout; no result files, plots, caches, commits or publication.

## Frozen claim contract

- CLAIM_ID: W3_85_REGULAR_CENTRE_SOURCE_REPRESENTABILITY.
- CLAIM: The specified literature response yields a static spherical metric
  with finite central curvature and a two-horizon branch. Its effective
  Einstein source satisfies the NEC but cannot equal the retained minimally
  coupled canonical scalar source on the static exterior.
- TYPE: EXTERNAL_LITERATURE_BENCHMARK plus EXACT_RESTRICTED_SOURCE_TEST.
- MODEL_VERSION: W3-85-v1.0. The analytic benchmark and expected identities
  below are known before verification; the test is reproduction, not a blind
  prediction or an independently invented regularization mechanism.
- ASSUMPTIONS: One metric, four spacetime dimensions, static spherical
  symmetry, asymptotic flatness, G=c=1, positive geometric mass M and positive
  length ell. Retain the independent lapse during variation. The literature
  response is restricted to 0<=ell^2*psi<1 at r>0; r=0 is a limiting point.
- DOMAIN: r>0, with a regular-centre limit; all positive M,ell analytically.
  The source exclusion needs only the connected exterior f>0, real harmonic
  frequency, positive canonical kinetic coefficients and regular fields.
- CONVENTIONS: signature (-+++); r is areal radius, psi=(1-f)/r^2;
  ds^2=-n(r)^2*f(r)*dt^2+dr^2/f(r)+r^2*dOmega^2. M is the geometric ADM mass.
  The lapse n is unrelated to W84's rotor action; ell is not the Planck length.
- FREEDOM_LEDGER: H(psi) is supplied by the cited literature. ell is its free
  universal regularization scale; M is object data. Neither is derived from
  RefG. One numerical illustration uses ell=1,M=2, selected as a known
  two-horizon example, not fitted. No observational data or free functions
  are selected from a numerical outcome.
- DEPENDENCIES: W64/W73 supply only the canonical scalar action/source and
  the conditional Penrose boundary. W84 supplies no gravitational stress or
  identification of its link variable with psi. No numerical PASS is inherited.
- METHOD: Independent lapse variation; algebraic solution of the resulting
  radial constraint; direct metric curvature and Einstein tensor; exact
  centre/asymptotic limits, horizon polynomial and canonical-source positivity.
- PASS_CONDITION: All exact residuals below vanish; all registered inequality
  certificates and benchmark branch classifications hold; numerical roots
  obey their budgets; actual mutation controls fail the baseline equations.
  The software result and the physical source decision are separate fields.
- FAIL_CONDITION / FALSIFIER: A failed identity, wrong domain or invalid
  positivity step invalidates that claim. A canonical scalar matching the
  nonconstant benchmark stress on the static exterior would refute the
  source exclusion. A solver failure is numerical inconclusiveness, not physics.
- RESIDUAL / ERROR_BOUND: Exact symbolic zero for variation, field equations,
  curvature, source, conservation, limits and local geometry. Only the
  dimensionless illustrative horizon roots use floats, with relative
  polynomial residual <1e-11; root counts/signs also follow analytic calculus.
- VALIDITY_HEALTH: Finite Riemann components, regular horizon chart and
  positive-density NEC are benchmark checks. They do not establish general
  perturbative stability, a healthy four-dimensional action on every
  background, formation from physical initial data or global geodesic
  completeness. In particular, the inner Cauchy horizon remains relevant.
- BRANCHES: Horizonless, double-root extremal and two-positive-root cases;
  report all three analytically. The single-function target is the tested
  subclass, not every possible regular black hole.
- OBSERVABLE_MAP: ADM coefficient, areal horizon radii and local curvature.
  Coordinate clock slowing is not used as a substitute for those tests.
- FORWARD_MODEL / DATA_ROLE: N/A; no observations or inference pipeline.
- IDENTIFIABILITY / BENCHMARK: Literature regular geometry versus its Einstein
  limit and the fixed canonical-source class. The metric alone does not
  identify an underlying matter or gravitational action.
- CROSSCHECK: Compute the Einstein tensor and curvature directly from the
  metric connection, separately from the radial-action and mass-function
  formulas. The common premises are the chosen metric ansatz and literature H.
- PROVENANCE / FILES: Hash this contract, verifier, CODES, GE, W64, W73 and
  W84 source; report Python/SymPy/NumPy versions. Exactly two local files.
- CLOSURE_FLAGS: Compute variation, radial_solution, geometric_curvature,
  regular_centre, horizons, source_conservation, null_energy_counterexample,
  canonical_source_exclusion and mutation_controls from their tests.
  Keep RefG_response_derived, RefG_regular_black_hole, global_geodesic_completeness,
  generic_stability, formation, observational_pass, active_theory_changed and
  intuitive_files_changed false.

## Published variational problem

Borissova and Carballo-Rubio, PRD 113,124004 (2026), Eqs130-133 give, up to
boundary terms and in G=1 units,

    S_stat = (1/12) integral dt dr n(r) [r^3 H(psi)]'.

Use compactly supported variations, with both n and f independent. The
Euler-Lagrange derivatives must be

    E_n = [r^3 H(psi)]'/12,
    E_f = r*n'*H'(psi)/12.

For H' nonzero, vary first and then normalize n=1 at infinity. The mass
integration constant is r^3 H=12M because H=6psi+O(psi^2) gives the Einstein
weak-curvature normalization. This is a reduced spherical benchmark; it does
not silently prove a unique generally covariant RefG completion.

The published Hayward choice is

    H(psi)=6psi/(1-ell^2*psi).

Solve the algebraic constraint for psi rather than imposing a preferred f:

    psi=2M/(r^3+2M ell^2),
    f=1-2M r^2/(r^3+2M ell^2).

This known H was reconstructed from the known metric in the cited paper.
Reproducing its consequences establishes the benchmark, not its microscopic
origin. The Einstein control H=6psi gives f=1-2M/r.

## Geometry and horizon tests

Independently derive from the metric connection, then compare with

    R=-f''-4f'/r+2(1-f)/r^2,
    K=(f'')^2+4(f'/r)^2+4((1-f)/r^2)^2.

The centre expansion is f=1-r^2/ell^2+O(r^5). Verify limits

    R(0)=12/ell^2, K(0)=24/ell^4,
    (1-f)/r^2 -> 1/ell^2, f'/r -> -2/ell^2,
    f'' -> -2/ell^2.

All component functions are rational with denominator powers of
r^3+2M ell^2>0 for r>=0, and decay at infinity. Verify the asymptotic ADM term
and the leading correction f=1-2M/r+4M^2 ell^2/r^4+O(r^-7).
Finite curvature is stated for this metric, not for every covariant action
that can reconstruct it.

The horizon polynomial is r^3-2M r^2+2M ell^2. Its positive minimum is at
r=4M/3. This yields Mcrit=3*sqrt(3)*ell/4. At equality r=sqrt(3)*ell is a
double positive root. For larger mass there are two positive simple roots;
for smaller mass none. Verify their classification and one M=2,ell=1 witness.
The ingoing Eddington-Finkelstein radial metric [[-f,1],[1,0]] has determinant
-1; finite-r horizons are coordinate regular. At the centre use the static
Cartesian extension, g_ij=delta_ij+(1/f-1)x_i*x_j/r^2, whose correction is
O(r^2); do not mistake the polar-coordinate determinant for a singularity.
The metric has sufficient differentiability for curvature and local geodesics;
no global completeness inference is made from this local check.

## Source test and the actual intuition correction

One may describe this metric either as the published modified-gravity vacuum
or as an Einstein geometry with the effective tensor G_ab/(8pi). These are
alternative ledgers, never simultaneous additional sources. With
m(r)=r(1-f)/2 the latter ledger gives

    rho=m'/(4pi r^2), p_r=-rho, p_t=-m''/(8pi r).

Derive these independently from the Einstein tensor. Verify anisotropic
conservation p_r'+2(p_r-p_t)/r=0, since rho+p_r=0. For the selected metric,

    rho=3M^2 ell^2/[2pi (r^3+2M ell^2)^2],
    rho+p_t=9M^2 ell^2 r^3/[2pi (r^3+2M ell^2)^3].

Thus rho>0 and the NEC is satisfied (radially saturated), including by
continuation through the horizons; p_r,p_t -> -rho at the centre. Verify
rho'(r)<0 at r>0. No fluid equation of state or microscopic source is derived
by this reconstruction.

W64 uses L_m=-[(partial chi)^2+chi^2(partial theta)^2]/2-V(chi).
On a static exterior with theta=omega*t, its source obeys

    rho_scalar+p_r_scalar=f*(chi')^2+omega^2*chi^2/(n^2*f).

Positive kinetic terms imply that equality to the target's zero requires
chi'=0 and omega*chi=0. Consequently its stress there reduces to a constant
potential, whereas the target density varies with r. This excludes the exact
Hayward metric sourced solely by this canonical field (or a finite sum with
positive kinetic coefficients) in unchanged Einstein gravity. It does not
exclude two-function geometries, other sources or modified gravity, and
does not rest on an overbroad use of Penrose's theorem.

The GE paragraph at line584 says that a regular core's source must violate
the NEC. The benchmark is a counterexample to that unconditional wording.
The actual W64/W67 contracts explicitly also require global hyperbolicity,
a noncompact Cauchy surface and a trapped surface. Their conditional theorem
statements remain valid. GE/EN are not edited by this scoped work package.

## Minimal negative controls and disposition

1. Setting n=1 before variation removes the radial constraint. Detect the
   lost equation, not merely a changed configuration flag.
2. Change the sign in H's denominator, solve its actual constraint and
   detect its positive-radius pole and nonzero residual against the baseline.
3. Flip the reconstructed tangential pressure and evaluate its actual
   conservation/Einstein residual; require nonzero residual.

The source decision is computed from the verified target stress and the
positive canonical kinetic identity. Report benchmark verification separately
from REJECTED_FOR_THIS_METRIC_SOURCE_PAIR. An unselected response H or absent
W84 metric variation remains unprovided physical input. Do not replace it with
a fitted constitutive law or start another parameter scan after this result.

## Sources and pins

- https://doi.org/10.1103/6x2z-qbkh ;
  https://arxiv.org/html/2602.16773v2 (III.2,III.4,IV.1,V).
- https://doi.org/10.1103/PhysRevLett.96.031103 (original metric construction).
- https://doi.org/10.1103/PhysRevD.111.104054 (NEC and global hypotheses).
- CODES.md: 27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41
- intuitive/RefG_GE.md: 7c28f8848ae5ac441efae05e5a551973f37cca711202a0865e007793e282acd1
- W64 contract: 25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1
- W73 contract: 8a3c3887fc0a28edc8fced67da0bc66ccaff39ade1f6e5b7e339f579fc02c49e
- W84 verifier: acd70be11d4734b5b208fa5b7166475166c48ee5f090640a05e19dfa081c3916
