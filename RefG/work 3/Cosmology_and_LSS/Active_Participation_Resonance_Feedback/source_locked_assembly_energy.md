# წყაროსთან შეკრული ენერგეტიკული პასუხი

2026-09-19. ძლიერი ველის დაწყებამდე, არსებული სკალარული კანდიდატის
ენერგიის ზუსტი აღრიცხვა და ცალკე მონიშნული ადიტიური დატვირთვის გამოცდა.

## საკითხი და მიღებული გზა

ოსცილონის ენერგიის შემცირება, გარემოს წნევის ამოკითხვის შემცირება
და გარემოს გადაწყობის დადებითი ენერგია ერთმანეთთან ერთი მოქმედებით
უნდა შევადაროთ. ამისთვის ვიყენებთ უკვე აგებულ
[სასრული წყაროს კანდიდატს](common_scale_finite_source_candidate.md).
მის განტოლებებს ახალი ფონური წყარო ან ენერგიის ხელით არჩეული
გადაცემის ნიშანი არ ემატება.

ქვემოთ პირველი შედეგი ამავე მოქმედების ზუსტი წონასწორული ენერგეტიკული
კავშირია. მეორე შედეგი ცალკე გამოცდაა: იმავე ტიპის დამოუკიდებელი,
ადიტიური მატერიული ასლების საერთო პროფილით დატვირთვა. ეს არჩევანი
გამოცხადებული გამარტივებაა. ერთი არაწრფივი ველის რამდენიმე
გადაფარული ოსცილონისგან ასეთი ადიტიურობა ჯერ გამოყვანილი არ არის.

## Frozen contract — before execution

- CLAIM_ID: SOURCE_LOCKED_EQUILIBRIUM_ENERGY_RESPONSE_V1.
- CLAIM / TYPE: derive the fixed-charge stationary energy response of
  COMMON_SCALE_FINITE_SOURCE_CANDIDATE_V1, verify it numerically, and
  separately test its additive-replica loading toy. Exact variational
  identities and bounded weak-field numerical evidence have distinct status.
- MODEL_VERSION: the original one-field action is unchanged. ADDITIVE_REPLICA_TOY_V1
  adds N independent copies of that matter action with equal individual
  charges and a common stationary profile, coupled to the same u.
  Real N is a formal load interpolation; integer N counts model copies.
  The nonlinear potential is evaluated separately for each copy.
- ASSUMPTIONS / DOMAIN: regular localized radial stationary branch,
  fixed Q per copy, u tending to zero at infinity, positive alpha;
  signature -+++, c0=1, p=exp(-u), P_F/P_F0=p^2.
  The conditional concavity theorem requires a differentiable branch
  with an invertible positive constrained Hessian in the considered sector.
- FREEDOM_LEDGER: inherited sextic V and W58 Omega0=.8 reference;
  physical toy coupling alpha0=.001, N in [1,3], hence effective coupling
  g=alpha0*N in [.001,.003]. No new EOS, dissipation, pressure floor,
  independent collective current, fitted source coefficient or data fit.
  Additive copies and the common-profile restriction are explicit
  additional modelling choices, not consequences of random phases.
- DEPENDENCIES: existing candidate Python SHA256
  6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8;
  unchanged W58 SHA256
  b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57.
  No inheritance of independent Einstein/tensor-sector closure.
- METHOD / CROSSCHECK: stationary energy envelope versus independently
  re-solved finite differences; integrated envelope versus endpoint
  energies; direct sector bookkeeping; positive constrained radial
  Hessian versus sampled load concavity. The BVP implementation is shared
  with the old solver and is disclosed, not called independent code.
- BENCHMARK: W58 reference at R=80, tolerance=1e-8, 24001 quadrature points;
  new coupled solves (R,tolerance,points)=(40,1e-7,8001),(60,1e-9,16001).
  Main N grid is 1,.25 increments,3; derivative probes 2+/- .02 and 2+/- .01.
  Radial Hessian at N=2 uses (R,cells)=(40,240),(40,480),(60,360),(60,720).
- PASS_CONDITION: inherited charge residual<1e-7, energy/Gauss/virial
  residuals<2e-5, collocation residual<=2*tolerance, nonzero nodeless core,
  maximum |u|<.1. Envelope derivative relative error and step refinement
  <2e-5. Integral identity and quadrature refinement relative error<2e-5.
  Sampled load mass rises, mass per copy falls, and the second discrete
  mass increment is smaller. Second derivative at N=2 is negative,
  with step/domain relative changes<.01. Radial Hessian eigenvalues
  positive, residuals<1e-7. Cross-domain first-order observables<2e-5.
- FAIL_CONDITION / FALSIFIER: nonzero exact residual rejects its identity;
  a numerical threshold failure withholds that numerical claim.
  Negative curvature of the constrained energy rejects minimum status.
  A failed toy does not reject all RefG matter closures.
- RESIDUAL / ERROR_BOUND: analytic identities apply to localized
  infinite-domain solutions; numerical results include the exact vacuum
  u tail and report the omitted exponentially small matter-tail estimate.
  That estimate is an asymptotic diagnostic, not an interval bound.
  Require estimated tail energy/total<1e-12. No-tail negative controls
  must fail the same 2e-5 envelope/integral tolerance.
- VALIDITY_HEALTH / BRANCHES: retain the nodeless weak branch from W58;
  finite-box symmetric radial Hessians, with no claim about independent
  replica distortions or a global infinite-domain spectral gap.
- OBSERVABLE_MAP: total stationary energy equals the Gauss mass with
  physical alpha0; p, clock/ruler and p^2 light readouts retain their
  existing definitions. Q and N are not calibrated physical particle counts.
- FORWARD_MODEL / DATA_ROLE / IDENTIFIABILITY: no observational data;
  internal consistency experiment, not empirical validation or uniqueness.
- CLOSURE_FLAGS: exact envelope and numerical energy response separate
  from additive-toy evidence. Stored-background-tension EOS, microscopic
  population reduction, actual assembly evolution, full RefG closure,
  singularity removal and observational validation stay false.
- PROVENANCE / FILES: this report and source_locked_assembly_energy.py,
  stdout-only execution, dependency and script hashes in output.
  No manuscript, strong-field code, Git rule, Canon or public upload changes.
- STOP: resolve the energy accounting and decide the frozen weak
  loading experiment. Do not launch collapse or enlarge the scan.

## 1. The same source and the same energy

Write g for the coupling parameter in a single-copy calculation, to
distinguish it from the fixed physical alpha0 of the loading toy.
At fixed charge Q, the stationary energy is

    e(g) = F[z] + S[z]/g,           z=(f,u),
    F = Q^2/(2 I) + integral (|grad f|^2/2 + exp(2u)V(f)),
    I = integral exp(4u) f^2,
    S = integral |grad u|^2/2.

Spatial integrals cover all space. On a numerical box the exterior
contribution is S_tail=2 pi R u(R)^2. Define G(g)=S[z(g)]/g,
the scale-response gradient energy. F is ordinary-sector energy.
G is the previously calculated response energy, not a constitutive
formula for stored background tension.

Since z(g) is stationary under admissible fixed-Q variations,

    de/dg = -G(g)/g.

The derivative of the solution itself cancels by its field equations.
Including the exterior tail is essential for this cancellation.
Consequently, between two equilibria on the same smooth branch,

    e(g1)-e(g2) = integral_g1^g2 G(g)/g dg,
    F(g1)-F(g2) = [e(g1)-e(g2)] + [G(g2)-G(g1)].

This is the precise energy accounting: a decrease in ordinary-sector
energy can supply a change in the response energy while reducing total
energy as well. The sign of a constitutive background-tension change
has not been inserted or inferred from G.

Changing g alone compares coupling strengths. It is not a time history.
The separate load construction below keeps its physical alpha0 fixed.

## 2. A controlled additive loading experiment

Take N additive copies, each with the same fixed Q and the same
stationary profile. Their constrained energy is

    M(N) = stationary_z [N F[z] + S[z]/alpha0].

Dividing its variational equation by N gives the original single-copy
problem at g=alpha0 N. Thus

    M(N) = N e(alpha0 N),
    E_matter(N) = N F(alpha0 N),
    E_response(N) = N G(alpha0 N).

The exterior source normalization uses alpha0:

    M_Gauss(N) = -4 pi r^2 u'(r)/alpha0
               = N [-4 pi r^2 u'(r)/g] = M(N).

Two exact derivatives follow:

    d[M(N)/N]/dN = -G(alpha0 N)/N <= 0,
    dM/dN = F(alpha0 N) > 0

for a nontrivial positive-energy copy. Mass per copy declines while
total mass increases. Relative to N isolated gravitating model copies,

    B_N = N e(alpha0) - M(N),
    ordinary_loss_N = N [F(alpha0)-F(alpha0 N)],
    response_change_N = N [G(alpha0 N)-G(alpha0)],
    ordinary_loss_N = B_N + response_change_N.

The isolated reference already contains each copy's own field.
Counting it as entirely field-free would change the question.

The additive assumption excludes the cross terms that arise if one
instead superposes several overlapping excitations of one nonlinear
complex field. The experiment therefore provides a transparent
macroscopic loading test, with its constitutive limitation recorded.

## 3. Why progressively smaller increments require stability

Let H_N be the constrained Hessian of N F+S/alpha0 on the allowed
profile variations. Differentiating the stationary equation gives

    H_N dz/dN = -grad_z F,
    d^2M/dN^2 = -<grad F, H_N^(-1) grad F>.

A positive invertible H_N makes this nonpositive. This is a conditional
stability-to-concavity theorem, rather than an imposed suppression
factor. It is local on the selected branch and in the variation sector
where H_N is positive. In an infinite-dimensional setting the inverse
must exist on this source and the pairing must be finite.

The numerical Hessian checks below cover the symmetric radial sector
at N=2. The directly computed masses and finite differences separately
test the sampled loading behaviour. Neither check certifies all
independent deformations of N copies.

## 4. Decision on additional medium terms

An independently conserved radiationlike collective current would add
an energy A/w, w=p^(-2), and the contribution 4 alpha A/w^2 to
the homogeneous w_tt equation. It persists when the ordinary oscillon vanishes.
This is an additional physical sector, not the requested sole-oscillon
source mechanism; it is not inserted here.

A derivative self-interaction such as beta X_psi^2 would introduce a
new constitutive coefficient and change the oscillon action. Its
homogeneous health also does not establish health for arbitrary spatial
gradients. There is no need to adopt that change to establish the
energy identity above.

## Execution results

**არსებულ სკალარულ კანდიდატში წონასწორული ენერგეტიკული კავშირი
გამოიყვანა და რიცხვითმა შემოწმებამ გაიარა.** ადიტიურ საცდელ ჯგუფში
იზრდება მთლიანი მასა, მცირდება ერთ ასლზე მოსული მასა და ყოველი
მომდევნო ასლის დამატებით მიღებული მატება.

Fine-domain values, with the isolated gravitating copy normalized to one:

| Model copies N | Total mass / M(1) | Central p | Central P_F/P_F0 | Coordinate charge RMS radius |
|---:|---:|---:|---:|---:|
| 1 | 1.000000000 | .991817422 | .983701798 | 2.703758311 |
| 2 | 1.993992167 | .983595144 | .967459406 | 2.678582634 |
| 3 | 2.981941513 | .975332142 | .951272787 | 2.653414407 |

These are separately solved stationary configurations, not frames from
a formation movie. The radius is a coordinate charge measure, not a
local standard ruler. The central pressure is the inherited readout
P_F/P_F0=p^2, not a newly derived thermodynamic EOS.

For N=3 the dimensionless energy ledger is:

    three isolated total energies       530.218372039
    common-profile total energy         527.026724777
    binding difference                    3.191647261

    three isolated ordinary energies    528.628697798
    common-profile ordinary energy      522.220597366
    ordinary-sector decrease              6.408100432

    three isolated response energies      1.589674241
    common-profile response energy        4.806127411
    response-energy increase              3.216453171

    6.408100432 = 3.191647261 + 3.216453171.

ამრიგად, ამ გამოთვლაში წნევის ამოკითხვა მცირდება; მატერიული ნაწილის
ენერგიაც მცირდება; გადაწყობილი გარემოს პროფილის ენერგია იზრდება;
მთლიანი ენერგია კი სამ ცალკე მდგომ ასლთან შედარებით ნაკლებია.
ენერგიის ეს აღრიცხვა ერთსა და იმავე ამოხსნებსა და მოქმედებას იყენებს.
ცალკე ფონური დაჭიმულობის მარაგის კანონი ამ შედეგით გამოყვანილი
არ არის — G სწორედ პროფილის ენერგიად რჩება.

The two integer mass increments in the original dimensionless units are
175.677636138 and 174.609631293. At N=2:

    numerical M'(2) = 175.144675790631,
    on-shell F(2)   = 175.144675894893,
    relative difference = 5.95e-10,
    numerical M''(2) = -1.06799296645.

The single-copy coupling derivative is independently checked:

    numerical de/dg = -531.935424203,
    -G/g            = -531.935423599,
    relative difference = 1.14e-9.

The integrated identity gives

    e(.001)-e(.003)                = 1.06388242045972,
    integral_1^3 G(.001 N)/N dN    = 1.06388242046344.

The maximum cross-domain relative change in the registered first-order
observables is 2.14e-10. The maximum total-energy/Gauss-mass relative
residual is 6.43e-11. The largest omitted leading-flat matter-tail
estimate is 1.43e-20 of the energy; this remains an asymptotic estimate.
Maximum |u| is .02498, so every solve stays in the frozen weak domain.

All four sampled N=2 radial Hessians are positive. Their minimum
eigenvalues at the finer grids are .001544261425 (R=40) and
.0006860270473 (R=60), with maximum eigen-equation residual 5.44e-12.
The fall with box size retains the known massless soft channel;
the conditional theorem in section 3 is not promoted to a universal
stability result.

Omitting the exterior response tail fails the negative controls.
At R=60 the binding integral is wrong by 3.87 percent and the
mass-derivative prediction by 2.35e-4 relative, both beyond the
unchanged 2e-5 tolerance.

### Reproduction and decision

The final saved verifier passed **12 symbolic and 222 numerical checks**
and exited 0. Its N=1,2,3 energies agree with the prior full execution
to the reported precision; the final execution additionally enforces
the separately requested envelope step-refinement and radius comparisons. These checks
share the declared action and BVP solver; their count is not a count of
independent physical observations.

The existing tension/energy audit also passed its unchanged 32 checks.
The original candidate, W58, intuitive manuscript and protected
strong-field source hashes stayed unchanged.

Run from the repository root:

    python -X utf8 -B "RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/source_locked_assembly_energy.py"

The executable prints JSON to stdout and writes no result files.
It includes the full sampled cases, checks, exact residuals and hashes.
Its final source SHA256 is

    82a476e5531e7b0cb13c523d9eff2f87007e25ffcc54a6790058ad5685a4d7cc

The report SHA256 at the final execution, before appending this results
section, was

    d0550705cde0c8abead297c05cdcece3d2cc8dc0ca74d99f056c90b5a7c739e1

Environment: Python 3.10.6, NumPy 1.24.3, SciPy 1.15.2, SymPy 1.13.3.

**დასრულებული ნაწილი:** სკალარული კანდიდატის წონასწორული ენერგიის
პასუხი და ადიტიური სუსტი დატვირთვის გამოცდა. ენერგიის დადებითი
გრადიენტული წვლილი საერთო მასის შემცირებასთან შეთანხმებულია.

**დარჩენილი ფიზიკური შეერთება:** ფონური დაჭიმულობის ენერგიის
განსაზღვრული კანონი და რეალური ოსცილონური მატერიის მაკროსკოპული
დატვირთვის დასაბუთება. ამ დამატებითი ასლების მოდელს სრული RefG-ის
ან სინამდვილეში მიმდინარე შეკრების სტატუსი არ ენიჭება.
ძლიერი ველი და სინგულარობის ანგარიში არ დაწყებულა.
