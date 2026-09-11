# Inverse design: a saturating collective gravitational response

## Frozen construction contract — 2026-09-11

- CLAIM_ID: W92_INVERSE_SATURATION_V1.
- CLAIM / TYPE: An explicitly postulated quasilocal response law produces a
  curvature-regular spherical black-hole candidate. Derive its required
  effective source and test infalling, rather than only static, observers.
  Status is CONDITIONAL_CANDIDATE, not a derivation from the existing RefG action.
- NEW AUTHORITY / INPUT: The author authorized inverse construction and
  explicit postulates, with subsequent joining to RefG. The new physical
  premise is a finite threshold of collective curvature response. Its
  simplest linear response fraction is chosen below; it is not inferred
  from the previous homogeneous one-third compensation.
- MODEL / CONVENTIONS: G=c=1, signature (-+++), r is areal radius, M>0 is
  asymptotic geometric mass, ell>0 is a universal response length. Define
  y=2M/r^3 and z=2m(r)/r^3. These have dimensions length^-2.
- POSTULATE / FREEDOM_LEDGER: z=y F(ell^2 z), with F(x)=1-x on 0<=x<1.
  The collective response fraction q=F is distinct from the operational
  clock/rod factor p. ell and this function are explicit new assumptions;
  M labels the object. No parameter is fitted. The known Hayward target
  motivated this inverse choice; the result is not a blind prediction.
- GEOMETRIC CLOSURE: ds^2=-f dt^2+dr^2/f+r^2 dOmega^2, f=1-r^2 z.
  The reciprocal temporal/radial coefficients are an additional restriction
  of this candidate. A general RefG two-function geometry is not assumed
  equivalent to it.
- DOMAIN: Static spherical r>0 plus centre and horizon extensions.
  The optional ingoing loading check covers finite advanced-time intervals
  with smooth M(v)>=M_min>0 and bounded derivative, not creation from vacuum.
- DEPENDENCIES / BENCHMARK: W85 already reproduces the Hayward geometry,
  its reduced action and canonical-source exclusion. Reuse that benchmark.
  The new decision distinguishes an everywhere-positive exponential feedback
  from a finite-threshold response and makes the latter an explicit candidate.
  W92's previous derivative candidate and its results stay unchanged.
- METHOD / CROSSCHECK: Solve the feedback equation; vary the independent
  radial lapse; compute the Einstein tensor and selected Riemann components
  directly in horizon-regular coordinates; compare with mass derivatives.
  Check radial proper time by an exact primitive and independent quadrature.
- PASS / FAIL / FALSIFIER: Exact identities, positive denominators, finite
  centre curvature and radial freely falling tides, and the two-horizon
  threshold must hold. Failure invalidates that particular result.
  Singular curvature or finite-radius poles reject geometric regularity.
  A source that omits the required pressures must fail Einstein's equations.
- ERROR / HEALTH: Symbolic identities are exact in the declared domain.
  Numerical examples use 50-digit arithmetic and residual tolerance 1e-35.
  Background regularity and energy conditions do not establish dynamical
  stability of a four-dimensional material action.
- OBSERVABLE_MAP: Quasilocal mass, ADM coefficient, areal horizons, effective
  source, and tidal curvature along radial geodesics. q is not a measured
  individual-oscillon mass factor. The construction does not calculate
  ADM mass as a function of conserved oscillon number.
- DATA_ROLE / FORWARD_MODEL / IDENTIFIABILITY: N/A to observations; no
  likelihood or detector data. This known geometry admits different source
  descriptions and does not uniquely identify RefG microphysics.
- FILES / STOP: This report, verify_inverse_saturation_candidate.py, a short
  W92 index and idea.txt. No official monograph, earlier action, solver,
  gitignore or publication changes. Stop after the inverse mechanism and
  its necessary source/observer tests; joining and perturbative stability
  are separate physical tasks.

## 1. Which feedback can actually bound the centre?

For continuous F with F(0)=1, suppose z approaches a finite positive limit
as y tends to infinity. The equation F(ell^2 z)=z/y requires F to reach
zero at a finite argument. Thus a smaller response by itself is insufficient.
The location and form of the first zero supply new constitutive information.

As a concrete rejected control, F(x)=exp(-x) gives

    ell^2 z = W(ell^2 y).

W is the positive Lambert function. It grows without bound. Although
m/M=exp(-ell^2 z) tends to zero and f tends to one at r=0, the Kretschmann
scalar grows as 24 W^2/ell^4. This control is an exponential law for the
new collective source, not a test of RefG's separate operational p=exp(-u).

The selected first-zero response instead gives

    z = y(1-ell^2 z) = 2M/(r^3+2M ell^2),
    q = 1-ell^2 z = r^3/(r^3+2M ell^2),
    m = M q,                       0<q<1 at r>0,
    d m/d M |_r = q^2 > 0,         d^2 m/d M^2 |_r < 0,
    m(M->infinity,r fixed) = r^3/(2ell^2).

This caps the enclosed response at a specified radius. M itself remains
the arbitrary mass at infinity. y is a reference Gauss load, not a claim
that the same bare matter inventory occupies every nested sphere.
The algebraic negative feedback does not specify a relaxation rate.

The resulting metric is exactly Hayward's [1]:

    f=1-2M r^2/(r^3+2M ell^2).

W85 already tested it as a literature benchmark. The corresponding reduced
spherical variational representation [2] is

    S_red=(1/12) integral dt dr N(r) [r^3 H(z)]',
    H(z)=6z/(1-ell^2 z).

Independent variation gives [r^3 H]'=0 and r N' H'/12=0. Normalizing the
outer lapse fixes N=1; the first integral is r^3 H=12M. This is a
spherical action representation of the postulate, not a covariant
RefG matter-medium completion.
H has a pole at the limiting central value ell^2 z=1; the geometric centre
extension therefore does not itself establish regular field dynamics
at that boundary of the reduced-action domain.

## 2. Regular centre, horizons and the source that must be supplied

The small-r and large-r limits are

    f=1-r^2/ell^2+O(r^5),
    f=1-2M/r+4M^2 ell^2/r^4+O(r^-7).

R(0)=12/ell^2 and K(0)=24/ell^4. The independent curvature components
contain only positive powers of r^3+2M ell^2 in their denominators.
They have finite limits at the centre. For all r>=0 a sufficient bound is
K<=105/(4ell^4); no sharpness claim is needed.

M_crit=3 sqrt(3) ell/4 separates the horizonless, extremal, and two-horizon
branches. The extremal radius is sqrt(3) ell. For M>M_crit the region
between the two roots is trapped. In the usual eternal asymptotically
flat extension the outer root is the black-hole event horizon relative
to the selected exterior. The ingoing (v,r) metric has determinant -1,
so finite-radius horizons are regular coordinate surfaces.

In an Einstein-source ledger the required total stress is

    rho_* = 3/(8pi ell^2),
    rho = m'/(4pi r^2) = rho_* (1-q)^2,
    P_r = -rho,
    P_t = -m''/(8pi r) = (3q-1)rho.

The density is finite and positive. Radial null stress is zero and
tangential null stress is 3q rho>=0. The centre has P_r=P_t=-rho_*:
negative pressure, or tension, is a necessary part of this response.
The anisotropic conservation equation holds. Tangential dominant-energy
inequality fails for q>2/3; the inferred stress is therefore not
automatically a healthy ordinary material fluid.

This stress is the entire effective source G_ab/(8pi). Adding it on top
of an already counted copy of the same gravitational response would
double count. W85's exclusion of the unchanged canonical scalar as the
sole source remains valid. A RefG completion must supply a collective
contribution which, together with the retained ordinary matter stress,
reproduces this total tensor. On a static exterior with canonical ordinary
fields, its radial null contribution must cancel
f*(chi')^2+omega^2*chi^2/f whenever that quantity is nonzero.

## 3. Freely falling observers and a non-bouncing infall channel

For a radial timelike geodesic with conserved energy E>0,

    (dr/dtau)^2=E^2-f.

In horizon-regular coordinates let w=sqrt(E^2-f) on the inward segment.
The orthonormal radial pair is u=(1/(E+w),-w), n=(1/(E+w),E).
Direct curvature contraction gives the electric tidal eigenvalues

    f''/2, f'/(2r), f'/(2r).

They are independent of the radial boost and all approach -1/ell^2
at the centre. Geodesic deviation has the opposite sign, giving finite
central defocusing. Neither simple horizon introduces a radial
freely falling tidal divergence in the exact background.

For the marginal E=1 channel,

    dr/dtau=-r sqrt[2M/(r^3+2M ell^2)] ~ -r/ell.

The inward trajectory approaches the centre exponentially in its own
proper time, r~C exp(-tau/ell), without a bounce. With a=2M ell^2,

    I(r)=2sqrt(r^3+a)/(3sqrt(2M))
         +(ell/3)ln[(sqrt(r^3+a)-sqrt(a))/(sqrt(r^3+a)+sqrt(a))],
    tau(r)-tau(r0)=I(r0)-I(r),       I(r)=ell ln r+O(1).

This is a trajectory result, not a collapse simulation. E>1 radial
timelike trajectories reach and locally cross the regular centre in finite
proper time. Admissible E<1 trajectories turn; radial null trajectories
cross in finite affine parameter. The centre has a C2 Cartesian extension.
Global geodesic completeness and perturbed inner-horizon stability are
not inferred from the radial tests.

## 4. Smooth loading test and the RefG joining boundary

For the limited ingoing extension M=M(v)>0, the direct Einstein tensor
requires the same instantaneous density/pressures and an additional flux

    T^r_v = (partial_v m)/(4pi r^2)
          = q^2 M_dot/(4pi r^2)
          = M_dot r^4/[4pi (r^3+2M ell^2)^2].

Positive mass input has positive flux. For bounded M_dot and M bounded
away from zero, the flux vanishes as r^4 at the centre. This is a
specified effective-source loading check. It supplies neither oscillon
formation dynamics nor generic inner-horizon stability.

The source fraction q tends to zero at the centre whereas the static
metric coefficient f tends to one. Hence q cannot be silently identified
with RefG's common clock/rod factor p. In the exterior, isotropic
coordinates recover the usual common clock/rod response at linear
Newtonian order; the interior identification needs the full RefG coframe
and its stress law. No official pressure or scaling law is altered here.

The candidate's central curvature singularity is removed under the stated
postulate and geometric closure. A derived RefG realization, stable
perturbations, physical formation, the value of ell and observational
agreement remain separate requirements.

## Reproduction and attribution

Run from the repository root:

~~~powershell
python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_inverse_saturation_candidate.py"
~~~

The script reads no private files, writes no outputs and reports exact
residuals, numerical crosschecks and physical scope separately.

The completed run passed 84/84 checks with SymPy 1.13.3 and mpmath 1.3.0.
An independent read-only review and rerun confirmed all 84. In the
dimensionless M=2, ell=1 illustration the two horizon radii are
1.193936566474630448256 and 3.709275359436922839229. From r0=8, the E=1
trajectory reaches r=0.5, 0.05 and 0.005 at elapsed proper times
8.458517244287734406406, 10.76628532612654680272 and
13.06887562222524766692. Independent quadrature and the primitive differed
by less than 1.8e-44 at these three points. The infinite-time endpoint
follows from the exact logarithmic divergence, not numerical extrapolation.

1. S. A. Hayward, *Formation and evaporation of non-singular black holes*,
   Phys. Rev. Lett. 96, 031103 (2006),
   [DOI](https://doi.org/10.1103/PhysRevLett.96.031103),
   [primary full text](https://arxiv.org/html/gr-qc/0506126v2).
2. J. Borissova and R. Carballo-Rubio, *Regular black holes from pure gravity
   in four dimensions*, Phys. Rev. D 113, 124004 (2026),
   [primary full text](https://arxiv.org/html/2602.16773v2).
3. [W85 benchmark and retained-source test](../W3-85_Regular_Centre_Source_Test/w3_85_regular_centre_contract.md).
   The known metric and action are credited to these sources; only the
   explicit adoption and testing of the inverse RefG candidate occurs here.
