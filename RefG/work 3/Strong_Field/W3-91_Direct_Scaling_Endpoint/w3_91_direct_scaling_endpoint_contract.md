# W3-91: Direct endpoint test of the common scale law

## One physical question and source boundary

The author describes external ruler/clock suppression continued toward p=0:
arbitrarily much exterior time can pass while the falling wristwatch records
much less time. Infinite accumulated internal proper time is not required.
Test that clock comparison separately from local endpoint regularity, using
the simplest expression actually present in
W51: p=exp(-m/r), with its common-response isotropic metric. No bounce, F(n),
additional source, response function, cutoff or interpolation is introduced.

W51 derives this sourced profile only in its static weak-field/PPN domain.
W67 explicitly separates that result from an exact strong-field completion.
Here the displayed formula is deliberately extrapolated to r->0 as a
DIAGNOSTIC of that extrapolation. It is not promoted to the full RefG action's
solution, and its failure does not reject W51 in its actual domain or W87.

New information relative to W90: a specified existing metric and an actual
geodesic clock trajectory replace an unspecified asymptote. Evaluate both
external suppression and freely falling elapsed time/curvature on the same
trajectory. The endpoint identities were derived by hand and independently
checked before this verifier; there is no blind prediction or fitted outcome.

Revise only this contract and w3_91_direct_scaling_endpoint.py, in place as
W3-91 v1.1. Stop after separating the clock result from the curvature result.
All earlier packages, intuitive texts, source laws, public theory versions,
Git state and publications stay unchanged. No further candidate is selected.

## Frozen claim contract

- CLAIM_ID / TYPE / VERSION: W3_91_DIRECT_COMMON_SCALE_ENDPOINT;
  EXACT_CONDITIONAL_EXTRAPOLATION_DIAGNOSTIC; v1.1.
- CLAIM: The exact exponential metric satisfies external asymptotic clock
  and ruler suppression and permits arbitrarily large exterior/own elapsed
  time ratios on finite inward segments. Separately, its r=0 endpoint has
  unbounded freely transported curvature and finite affine/proper duration.
  Finite proper duration is compatible with the author's clock comparison;
  the independent curvature result obstructs a smooth regular endpoint.
- ASSUMPTIONS / DOMAIN: Static, spherical, isotropic-coordinate metric below,
  r>0, m>0, signature (-+++), c0=1. Test matter/light follow this one metric's
  geodesics, as in W51 assumption 4. Finite starting r_i>0; radial timelike
  inward geodesic with conserved E>=1. The sphere's centre is an ideal test
  worldline; neither its self-gravity nor an extended nonlinear core is solved.
- CONVENTIONS: r is isotropic coordinate radius, B=r/p is areal radius;
  t is static time normalized at infinity; tau is the falling centre's own
  metric proper time. T_s is a local stationary clock with dT_s=p dt.
  E=p^2 dt/dtau, w=sqrt(E^2-p^2), gamma=E/p. Null affine normalization
  epsilon>0 is independent of timelike E. No actual stationary observer is
  assigned to r=0. All endpoint statements are one-sided limits.
- FREEDOM_LEDGER: Inherited m=GM/c0^2, initial radius and geodesic energy;
  photon normalization is conventional. The sole new assumption is treating
  W51's expression as exact outside its declared weak domain for this test.
- DEPENDENCIES: W51 contract/code and intuitive section 2.2 for the expression;
  W67 for the source-domain boundary; CODES and protected intuitive hashes.
  W87/W90 are context, not the source of this geometry. No earlier PASS replaces
  the new metric calculation.
- METHOD: Construct the metric, Levi-Civita connection and curvature directly.
  Derive conserved momenta, normalization and geodesic evolution; compare
  static and moving clocks and an actual outgoing frequency-transfer protocol.
  Evaluate exact elapsed-time integrals/bounds and freely falling projections.
- PASS_CONDITION / RESIDUAL / ERROR_BOUND: Exact geometric, trajectory, time,
  readout and endpoint identities pass; actual altered expressions fail the
  unchanged validators. No numerical tolerance, observational fit or existence
  result for the unselected full theory. Report the clock comparison and
  the endpoint curvature in independent, dependency-derived fields.
- FAIL_CONDITION / FALSIFIER: A nonzero required identity invalidates that
  calculation. A bounded exterior/own elapsed-time ratio would falsify the
  arbitrarily large clock-comparison claim; a finite limit of the specified
  transported tidal component would falsify the curvature claim. A different pressure
  profile, coframe or nongeodesic trajectory is a different tested model.
- VALIDITY_HEALTH: Metric smooth and Lorentzian for r>0; E>=1 ensures w>0 on
  every finite starting segment. The required regularity concerns freely
  falling physical measurements, not only contractions of curvature scalars.
  No matter-spectrum, stability, extended-body survival or microscopic proof.
- BRANCHES: Incoming material geodesics, both radial null orientations,
  stationary clock/ruler comparison and outgoing photons to a receiver at
  infinity. The m=0 flat case is a control, not the singular-endpoint claim.
- OBSERVABLE_MAP: Static reference-clock/ruler assignment; falling proper
  time; locally measured outgoing photon frequency and received pulse spacing.
  An infinitesimal ruler snapshot is not a finite remotely resolved image.
- FORWARD_MODEL / DATA_ROLE: Metric -> trajectories and null transport ->
  elapsed proper time/readouts/curvature. No observational data or fitting.
- IDENTIFIABILITY / BENCHMARK: Tests this exact common-factor extrapolation,
  not every p->0 profile or all RefG continuations. Minkowski m=0 and
  independent warped-sphere curvature/geodesic identities are controls.
- CROSSCHECK: Independent hand derivations; metric connection vs conserved
  momentum/normalization; computed Ricci vs areal-radius null identity; static
  frame curvature vs boosted freely transported transverse tidal component;
  photon projection vs neighboring-pulse arrival-time derivative.
- CLOSURE_FLAGS: Derive metric_geometry_checked, geodesics_checked,
  external_readout_checked, elapsed_time_checked, falling_curvature_checked,
  mutation_controls_checked and clock_interpretation_checked. Derive separate
  external_asymptotic_suppression_verified and
  exponential_endpoint_pp_curvature_singular fields from their own necessary
  checks. Set proper_time_infinity_required false as the clarified scope.
  Keep full_RefG_rejected, W51_weak_result_rejected, W87_rejected,
  singularity_resolved, regular_black_hole, full_action_solution,
  microscopic_completion, observational_pass, active_theory_changed and
  intuitive_files_changed false.
- PROVENANCE / FILES: SHA-256 source/contract pins and own verifier hash;
  Python/SymPy versions; finite JSON stdout only, Python -B, no caches,
  generated result files or new plots.

Revision record: v1.0 incorrectly made infinite accumulated internal time an
author requirement. v1.1 removes that requirement and separates the two
decisions. The metric, geodesics and curvature formulas are unchanged.
Previous contract SHA-256: 6ceb34b479e275bc86724184635ef63d630704574cbae4f80d861c5ec375493e.
Previous verifier SHA-256: eb2ff9525907d74a0812c51423f159f10be75e5a4fefaad22158992cfa4416b8.

## 1. Metric and the actual material clock

Use W51's expression with a consistently converted signature:

    p=exp(-m/r),
    ds^2=-p^2 dt^2+p^(-2)(dr^2+r^2 dOmega^2), B=r/p.

Conserved Killing energy and unit timelike normalization yield

    u^t=E/p^2, u^r=-w, w=sqrt(E^2-p^2),
    d tau/dt=p^2/E,
    dr/dt=-p^2 sqrt(1-p^2/E^2).

Verify the full radial geodesic equation, not only its normalization. The
stationary local frame measures inward v=-w/E, gamma=E/p. The stationary
clock factor p and the moving sphere's factor p/gamma=p^2/E are distinct.
Both approach zero in the prescribed exterior-coordinate limit.

For a sufficiently small local ruler, a stationary coordinate footprint has
factor p. A moving radial rod at equal static t has factor p/gamma=p^2/E
relative to its rest length; its transverse local factor is p. These are
declared simultaneity/projection protocols and not isotropic finite-image
sizes, measured deformations or a solved oscillon profile.

## 2. A genuine external signal comparison

An outward photon with positive conserved Killing frequency epsilon has

    k^t=epsilon/p^2, k^r=epsilon,
    omega_em=-u.k=epsilon*(E+w)/p^2,
    omega_inf=epsilon,
    omega_inf/omega_em=p^2/(E+w)=E-w -> 0.

For neighboring emissions on the falling worldline, the arrival time at a
fixed large receiver is t_arr=t_em+integral_r_em^r_obs p^(-2) dr. Therefore

    dt_arr/dtau=(E+w)/p^2.

Its product with the frequency ratio is one (receiver normalized at
infinity). Infinity here denotes normalized retarded arrival-time differences,
with the common propagation offset subtracted, or the large-radius limit of
a fixed detector; it is not a finite event located at spatial infinity.
Thus external received pulses are diluted as well as coordinate
motion slowing. No extra p factor is applied to photon transport.

## 3. External infinity versus accumulated proper time

For r decreasing from any finite r_i>0 to zero, p(r)<=p_i<1. Hence

    r_i/E <= Delta tau=integral_0^r_i dr/sqrt(E^2-p^2)
      <= r_i/sqrt(E^2-p_i^2) < infinity.

Radial null normalization and energy give

    dr/dlambda=+/- epsilon, Delta lambda=r_i/epsilon.

By contrast, the falling external time has integrand
E/[p^2 sqrt(E^2-p^2)]>=p^(-2). Its integral diverges at zero. Establish this
by an exact near-zero comparison with 1/r^2, or an equivalent exact limit.
The emitted pulse-arrival time also diverges. The actual same trajectory has
external asymptotic slowing and finite falling proper duration: precisely
compatible clock statements under the clarified requirement. The coordinate
radius, areal radius and particle's own size remain distinct quantities.

For the finite inward segment r_i -> r_i/2, use the positive proper-time
measure and the monotonicity of E/p^2 to bound the elapsed-time ratio:

    E exp(2m/r_i) <= Delta t/Delta tau <= E exp(4m/r_i).

Both durations are finite for each r_i>0. The lower bound becomes unbounded
as r_i->0, so arbitrarily large exterior/own-time ratios occur without any
new profile. The author's million-years/one-hour example specifies a clock
contrast, not fitted masses, radii or a numerical prediction. At a fixed
finite detector, normalized retarded arrival differences additionally obey
Delta t < Delta t_arr < 2 Delta t; receiver proper time includes its fixed p.

Under the inherited ideal-clock assumption, an internal oscillator of fixed
proper angular frequency Omega_0 has phase increment dchi=Omega_0 d tau.
Thus dchi/dt=Omega_0 p^2/E for the falling centre. The geometric proper time
already includes the internal cadence conversion. Applying another factor
p would introduce a new clock law; reject that double counting against the
same clock-normalization validator. No microscopic core evolution is solved.

## 4. Check the internal endpoint in a falling frame

The metric-derived Ricci tensor in these coordinates is

    R_rr=-2m^2/r^4, with the other Ricci components zero.

Consequently

    R=-2m^2 p^2/r^4 -> 0,
    R_ab k^a k^b=-2 epsilon^2 m^2/r^4 -> -infinity,
    R_ab u^a u^b=-2m^2(E^2-p^2)/r^4 -> -infinity.

An independent geometric check uses the affine radial coordinate and
B''(r)/B=m^2/r^4, giving R_kk=-2 epsilon^2 B''/B.

Compute static orthonormal Riemann components (0,1 radial/time, 2,3 angular):

    A=R0101=2m(m-r)p^2/r^4,
    Bc=R0202=m(r-m)p^2/r^4,
    C=R1212=-m p^2/r^3,
    D=R2323=m(2r-m)p^2/r^4.

They vanish as r->0, and

    Kretschmann=4m^2 p^4(7m^2-16mr+12r^2)/r^8 -> 0.

The transverse unit vector e2=(p/r)partial_theta is parallel transported
along a radial geodesic. Project the computed Riemann tensor onto (u,e2):

    R(u,e2,u,e2)=gamma^2(Bc+v^2 C)
               =-E^2 m^2/r^4+m p^2/r^3 -> -infinity.

For every r>0, the metric and transported curvature are finite and smooth.
Every finite exterior-time point on this fall lies in that open domain.
The limiting endpoint has divergent freely transported tidal curvature,
despite its benign scalar invariants and external suppression.
This is a physical endpoint obstruction to a smooth regular continuation,
independent of any requirement for infinite accumulated proper time. It does not calculate an
extended sphere's deformation or impose the metric on the full RefG theory.
Here u and e2 are already normalized by the operational metric's clocks and
rulers. For a fixed proper oscillator frequency Omega_0>0, the dimensionless
coefficient R(u,e2,u,e2)/Omega_0^2 is also unbounded. This checks the same
measurement in internal cycle units, without counting the clock factor twice.

## 5. Controls, outcome and stop

Registered actual mutations: substitute stationary p for the moving clock
rate; delete the spatial ruler factor from the metric/geodesic check; equate
the affine radial speed with the vanishing coordinate speed; remove R_rr
from the curvature projection; multiply the proper clock rate by another p.
Each must fail the same relevant baseline validator. Use flat-space
regression and independently recomputed curvature.

Decision 1: the exact static common-factor exponential continuation realizes
the clarified exterior-slowing clock picture. Accumulated own time follows
the same metric and is allowed to be finite.

Decision 2: the same extrapolation has a pp-curvature-singular endpoint.
This independent regularity obstruction remains after correcting the clock
criterion. Its scope is the tested extrapolation of the sourced profile and
coframe; the in-domain weak-field result is unchanged. No replacement
mechanism is introduced, and no regular black hole is claimed.

Primary independent literature: C. Martinez and M. Nozawa, Static spacetimes
haunted by a phantom scalar field: classification and global structure in
the massless case, Phys. Rev. D 103,024003 (2021),
https://doi.org/10.1103/PhysRevD.103.024003 and
https://arxiv.org/abs/2010.05183, section 3.2 (Ellis-Gibbons, n=4, M=2m).
Their equations 3.25,3.31,3.33,3.34 and Table 3 identify the same metric's
finite-affine, parallelly propagated curvature-singular endpoint. Their
phantom-scalar action is not imported into RefG. The verifier recomputes the
geometric result from the displayed metric instead of trusting the citation.
