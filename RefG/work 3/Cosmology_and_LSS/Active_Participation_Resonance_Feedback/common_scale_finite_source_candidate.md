# საერთო მასშტაბის სასრული წყარო — დამოუკიდებელი სკალარული კანდიდატი

2026-09-19. სუსტი ველის, ოსცილონისა და გარემოს ერთობლივი
წონასწორობის შეზღუდული გამოცდა. ძლიერი ველის ევოლუცია არ იწყება.

## მიზანი და არქიტექტურული საზღვარი

შევამოწმოთ ერთი განსაზღვრული მაკროსკოპული კანონი, სადაც ოსცილონის
პროფილიც და გარემოც ერთად იცვლება, ხოლო სრული ენერგია და შორეული
ველიდან წაკითხული წყაროს მასა ერთ ამოხსნაში თანხვდება.

ქვემოთ აგებული მოქმედება ახალი სკალარული კანდიდატია. მასში მეტრიკა
u-ისგან კონსტრუირდება; დამოუკიდებელი აინშტაინური მეტრიკა არ ვარიირდება.
ამიტომ ეს W54-ის მოქმედების შესწორება ან მისი სრული შედეგების
მემკვიდრე არ არის. დამოუკიდებელი სპინ-2 სექტორი ამ კანდიდატში არ დგას.
მისი მიღება სრული გრავიტაციული თეორიის ნაცვლად ამ გამოცდის მიზანში
არ შედის. მოწმდება კონკრეტული მინიმალური სკალარული უკუკავშირის
განტოლებები, ენერგიის თანხვედრა და სასრული წყაროს რადიალური პასუხი.

ახალი საყრდენი ძველ სტატიკურ საცდელ ანგარიშთან შედარებით:
წყარო აღარ არის ხელით უძრავად დატოვებული rho_b. W58-ის იგივე
კომპლექსური ველი საკუთარ განტოლებასაც ასრულებს. მისი სივრცული
დაძაბულობების ბალანსი მასისა და ენერგიის შედარებაში მონაწილეობს.
ეს ახალი მოქმედების გამოცდაა; ძველი EH-შეზღუდვის აცდენა მის საკუთარ
მოდელში უცვლელ შედეგად რჩება.

## Frozen contract, before numerical execution

- CLAIM_ID / MODEL_VERSION: COMMON_SCALE_FINITE_SOURCE_CANDIDATE_V1.
- TYPE: new internal effective scalar candidate; exact variational and
  virial identities; finite-domain numerical stationary-source evidence.
- CLAIM: test existence of weak regular fixed-charge spherical equilibria
  in the action below, their energy/Gauss-mass agreement, and constrained
  radial energy curvature. Passing does not adopt new gravity in Canon.
- ASSUMPTIONS / DOMAIN: preferred asymptotic coordinates, signature -+++,
  c0=1, u=-ln p finite, alpha=4 pi G>0, constant scalar stiffness
  1/alpha. Harmonic ordinary field, positive sextic potential, localized
  spherical source, u->0 at infinity, finite energy and charge.
- FREEDOM_LEDGER: inherited dimensionless V=f²/2-f⁴/4+f⁶/24 and W58
  reference frequency Omega0=.8; alpha in {.001,.003} is an explicitly
  selected weak-coupling benchmark, not fitted or foundation-derived.
  Charge is fixed to the uncoupled reference on R=80, tolerance=1e-8.
  The new scalar kinetic operator is a postulated candidate completion,
  chosen to share the operational null cone; no damping or pressure floor.
- DEPENDENCIES: W58 potential/profile only; common p/p² measurement map.
  No inheritance of W54/W52 full PPN, tensor modes, cosmic fits or W92
  independent-metric constraints. W58 source SHA256:
  b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57.
- METHOD: coupled boundary-value problem at fixed Q with Omega solved,
  independent volume/flux/virial energy balances, domain/tolerance and
  quadrature refinement; fixed-Q radial Hessian including charge rank-one
  term and the exterior gravitational tail.
- PASS_CONDITION: at both alpha benchmarks and both resolutions,
  converged nodeless nonzero core, |u|<.1, charge relative error<1e-7,
  solver residual<=2*tolerance, energy/flux mass and virial relative
  residual<2e-5. R/tolerance changes of E,M,Omega,p(0),charge radius<3e-4.
  The radial Hessian test at alpha=.003 is separately reported.
- FAIL_CONDITION / FALSIFIER: a nonzero exact identity residual falsifies
  that identity; a failed numerical threshold withholds its numerical
  status, not an entire theory no-go. A resolved negative radial energy
  direction rejects radial-energy-minimum status of that equilibrium.
- RESIDUAL / ERROR_BOUND: exact symbolic checks versus numeric errors;
  radial boxes (40,1e-6) and (60,3e-8); integral checks at 8001 and 16001
  points; Hessian grids (R,N)=(40,240),(40,480),(60,360),(60,720).
  No interval-arithmetic proof or infinite-domain positive spectral gap.
- VALIDITY_HEALTH: positive local kinetic coefficients and shared
  principal cone at finite u; radial constrained-energy test only.
  Nonspherical, preferred-frame/full-PPN and tensor/radiation completion
  are not part of the claimed closure.
- BRANCHES: retain the continuous weak-coupling branch from the W58
  .8 core; do not tune Omega or source profiles to a preferred outcome.
- OBSERVABLE_MAP: external p=e^-u, rest-energy/clock/ruler readout p,
  coordinate light speed p²; Gauss mass from u~G M/r; charge-radius in
  the reference spatial coordinates is distinguished from proper size.
- FORWARD_MODEL / DATA_ROLE / IDENTIFIABILITY: no data or observations.
  One candidate selected openly; no uniqueness or empirical validation.
- BENCHMARK: alpha=0 W58 core; static exterior beta=gamma=1 subset only;
  deliberately fixed matter is not a substitute for the coupled solution.
- CLOSURE_FLAGS: variational_source, on_shell_virial and numerical
  finite_source gates separated; full_RefG_closure, EH_equivalence,
  full_PPN, singularity_resolution, arbitrary_load_no_zero, nonlinear
  relaxation, observational_pass and Canon_changed remain false.
- CROSSCHECK: fixed-Omega action dilation versus fixed-Q energy dilation;
  boundary mass versus source integral versus total Noether energy.
  An independent derivation verifies the radial Hessian and tail.
- PROVENANCE / FILES: this contract and stdout-only
  common_scale_finite_source_candidate.py. Existing scientific files and
  Git rules are unchanged. No public upload or commit is performed.
- STOP: record the finite-source decision and its architectural limit.
  No collapse run, additional unregistered coupling scan, or promotion
  to a complete gravitational theory follows from a successful test.

## 1. One specified action

Use psi for the complex ordinary field and u=-ln p for the common scale.
The operational metric and action density in the reference coordinates are

    g_mu_nu(u) = diag(-exp(-2u),exp(2u),exp(2u),exp(2u)),
    L = [exp(4u) u_t² - |grad u|²]/(2 alpha)
        + exp(4u)|psi_t|²/2 - |grad psi|²/2
        - exp(2u)V(|psi|),
    V(f) = f²/2 - f⁴/4 + f⁶/24.

The ordinary-field terms are its canonical action in g(u), including
sqrt(-g). The u kinetic term is the explicitly new dynamical choice.
Its Hamiltonian measures kinetic/gradient energy of the scale response.
It does not supply a derived stored background-tension energy as a
function of P_F. The [tension/energy audit](foundation_tension_energy_audit.md)
fixes this interpretation without changing the candidate action.
It supplies a positive principal kinetic coefficient exp(4u)/alpha.
For the two real components of psi the coefficient is exp(4u).
Their principal speed in these coordinates is exp(-2u)=p². Maxwell
light minimally coupled to g(u) shares this cone; no light energy is
added to the stationary source calculation.

The field equations are, with V_A the derivative with respect to each
real component psi_A,

    partial_t[exp(4u) partial_t psi_A] - Delta psi_A
        + exp(2u) V_A = 0,
    exp(4u)(u_tt+2u_t²) - Delta u
        = alpha [2exp(4u)|psi_t|²-2exp(2u)V].

These are the candidate's actual response equations, not an extra p
multiplier attached to an earlier gravitational source. The common
factor and coordinate cone apply at finite u. Neither positivity of
p=exp(-u) by definition nor these equations alone prove that u cannot
diverge in a future evolution.

## 2. Complete stationary source and mass identity

For psi=exp(i Omega t) f(r), define

    T=Omega² exp(4u) f²/2,  G_f=f'²/2,
    W=exp(2u)V(f),         G_u=u'²/(2 alpha),
    D=4T-2W.

The radial equations and charge are

    f''+2f'/r = exp(2u)V_f - Omega² exp(4u)f,
    u''+2u'/r = -alpha D,
    Q=4 pi Omega integral r² exp(4u)f² dr.

The regular centre has f'(0)=u'(0)=0; infinity has f=u=0.
The finite box uses the decaying matter Robin condition and u'+u/R=0.
The asymptotic exterior u=C/r gives

    M_Gauss = -4 pi r² u'/alpha = 4 pi integral r² D dr,
    E_total = 4 pi integral r²(T+G_f+W+G_u)dr.

The matter-dependent source D includes stresses. A source that remains
stationary in this model need not have a nonzero outgoing energy flux.

Dilation of the complete stationary action, including u, gives

    integral(G_f+G_u)=3 integral(T-W),
    E_total=integral(4T-2W)=M_Gauss.

Here integrals without radial factors denote the full spatial integral.
Fixed-Q energy variation gives the same relation: under radius scaling
by lambda, its phase kinetic energy scales as lambda^-3, gradients as
lambda and potential as lambda³. The identity is on shell.

The exterior scalar tail energy outside R is 2 pi R u(R)²/alpha and is
included. It must not be omitted when comparing energy with Gauss mass.
For constant stiffness, u=GM/r outside the localized source; expansion
of g00=-exp(-2u) and gij=exp(2u)delta_ij gives beta=gamma=1 in the static
spherical PPN subset. This is not the independent-Einstein full PPN result.

## 3. Small radial response at fixed charge

Eliminating uniform phase momentum at fixed Q yields

    I=4 pi integral r² exp(4u) f² dr,       Omega=Q/I,
    E_Q=Q²/(2I)+4 pi integral r²(G_f+W+G_u)dr
        + 2 pi R u(R)²/alpha.

Set h=r delta f, k=r delta u/sqrt(alpha). The independent second
variation has unit radial gradient terms and local potential matrix

    U_ff=exp(2u)V_ff-Omega²exp(4u),
    U_fu=2exp(2u)V_f-4Omega²exp(4u)f,
    U_uu=4exp(2u)V-8Omega²exp(4u)f²,
    U_matrix=[[U_ff,sqrt(alpha)U_fu],[sqrt(alpha)U_fu,alpha U_uu]].

It additionally contains the positive rank-one charge term

    (4 pi Omega²/I)
      [integral r exp(4u)(2 f h+4sqrt(alpha)f² k) dr]²

in delta²E_Q/(4 pi). Boundary conditions are h(0)=k(0)=h(R)=0 and
k'(R)=0. The last condition follows after including the exterior tail;
it is equivalent to delta u'(R)+delta u(R)/R=0.

A positive computed Hessian is numerical evidence for the constrained
radial energy test. The massless u channel has arbitrarily soft
long-wavelength modes; finite-box positivity is not a positive
infinite-domain spectral gap. The test does not simulate damping or
claim final relaxation. Phase gradients and u momentum add nonnegative
energy in this candidate.

## Results

**სასრული წყაროსა და რადიალური ენერგეტიკული პასუხის გამოცდები გაიარა.**
ორივე რიცხვით მდგომარეობაში ოსცილონი და გარემო ერთადაა ამოხსნილი.
წონასწორობის სრული ენერგია და შორეული წყაროს მასა თანხვდება.

Fixed Q=190.401136223484. Fine-domain results (R=60, tolerance=3e-8):

| alpha | Total energy | Gauss mass | Central p | Coordinate charge-radius / reference |
|---:|---:|---:|---:|---:|
| 0, reference | 177.268340520 | N/A, uncoupled reference | 1 | 1 |
| .001 | 176.739457346 | 176.739457365 | .991817422 | .990769838 |
| .003 | 175.675574925 | 175.675574945 | .975332142 | .972321731 |

These are comparisons between specified coupling benchmarks at fixed
charge, not a time evolution or a sequence of added particles. Q is the
ordinary field's conserved U(1) charge, not an established particle count.
The radius is a global coordinate RMS charge radius; it is not a local
standard ruler. The actual p varies across the body, whose profile responds
to the field. Its integrated energy and radius ratios need not equal the
single central p.

At alpha=.003, relative to the uncoupled reference, total energy is lower
by .8985054 percent and the coordinate charge radius by 2.7678269 percent.
These changes are outputs of the coupled solution, not prescribed target
values. The largest fine-run energy/Gauss-mass relative disagreement is
1.12e-10. The largest change between the two frozen domain/tolerance
resolutions is 3.36e-9; the same-profile quadrature change is below 4.45e-12.
Dropping the exterior field energy breaks the mass/energy check in all
four runs, as tested against the unchanged tolerance.

The smallest radial fixed-Q energy eigenvalues at alpha=.003 are:

| R | cells | minimum energy-Hessian eigenvalue |
|---:|---:|---:|
| 40 | 240 | .001545337082 |
| 40 | 480 | .001545321639 |
| 60 | 360 | .000686347593 |
| 60 | 720 | .000686343430 |

The eigen-equation residuals ||Hv-lambda Mv||_2/||Mv||_2 are below 5.5e-12.
The positive, grid-stable results support a local constrained radial
energy minimum in these finite-domain tests. Their fall with R is the
expected soft massless channel; no uniform positive spectral gap or
nonlinear long-time relaxation is inferred.

The saved executable passed 10 symbolic and 31 numerical acceptance checks
and exited 0. These include source/action consistency, the exact dynamic
Noether energy balance, the independent virial mass identity and the
registered finite-domain tests. A second execution reproduced the results.
Independent derivations checked the fixed-Omega/fixed-Q identities and
the radial Hessian including its charge and exterior-tail contributions.

Run from the repository root:

    python -X utf8 -B "RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/common_scale_finite_source_candidate.py"

Script SHA256:
6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8.
Environment: Python 3.10.6, NumPy 1.24.3, SciPy 1.15.2, SymPy 1.13.3.
The script prints the current contract and source hashes; it writes no
result files. The W58 dependency remains byte-identical.

**დასრულებული შედეგი:** მიღებულია ერთი განსაზღვრული, საცდელი
სკალარული კანონის ენერგეტიკულად შეთანხმებული სუსტი ველის წყარო,
მისი საერთო p-საზომები და მცირე რადიალური გადახრის დადებითი
ენერგეტიკული პასუხი.

**შეუერთებელი ნაწილი:** ამ კანდიდატს დამოუკიდებელი აინშტაინური და
სპინ-2 დინამიკა არ აქვს. მისი დაკავშირება სრულ RefG გრავიტაციასთან
ცალკე ფიზიკური ამოცანაა და მოცემული წარმატებით არ დახურულა.
წნევის ნულამდე მიუღწევლობის ზოგადი მტკიცება, ძლიერი ველი და
სინგულარობის მოხსნა ამ ანგარიშში მიღებული არ არის.
