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

## 4. Dressed slow motion and weak external gradients

### Contract before new numerical execution (2026-09-24)

CLAIM_ID: APR_DRESSED_SLOW_MOTION_V1. TYPE: same-action slow-velocity
reduction, exact identities and one bounded numerical translation test.
The purpose is to compare the whole body's rest energy, translational
inertia, passive response and moving weak exterior before strong fields.

MODEL: exactly COMMON_SCALE_FINITE_SOURCE_CANDIDATE_V1 above, with its
quadratic u_t term, alpha=0.001, sextic potential and retained charge
Q=190.401136223484. No independent Einstein metric, new F, force term or
Lorentz boost of the full preferred-frame theory is introduced. The later
rate-limited action is compared only at quadratic velocity order; it is
not substituted silently as the model of this run.

REFERENCE / DOMAIN: the existing nodeless spherical stationary branch
continued from Omega0=0.8; |v|<<1; fixed total U(1) charge, weak and slowly
varying external u with tidal gradients neglected at leading monopole
order. Include both matter and the full scalar self-field. The calculation
finds the regular translation tangent and its energy coefficient; it does
not prove a finite-speed nonlinear traveling family or radiation/stability.

METHOD: derive the required O(v) phase response and solve its l=1 radial
linear problem. Use both fixed-Q Routh reduction and Noether momentum for
inertia, and the retained stationary virial for the comparison with rest
energy. Restore the old alpha=.001 profile because the old executable
saved stdout quantities, not an interpolated solution; this restoration
is input for a NEW angular response, not a rerun of the old radial-health
or energy-equality campaign. The W58 profile is only the unchanged seed.
Use background rescaling for the dressed external-gradient coupling and
the weak exterior wave operator for the moving scalar monopole.

NUMERICAL SCOPE: restored domains (R,tol)=(40,1e-7),(60,3e-8), with
linear phase grids of 600 and 1200 cells and Gaussian element quadrature.
No coupling or frequency scan. Include the analytic 1/r foundation tail
in inertia and rest energy; the exponentially small matter tail remains
a finite-domain error controlled by changing R. Solve for the phase
correction to the exact zero-gravity boost, not a rigid translated phase.

BOUNDARIES: regular dipole phase at the centre, finite weighted phase
energy at infinity. Its allowed asymptote includes linear and logarithmic
terms; it is not forced to vanish. At finite R use the natural total
phase-current boundary, whose error is weighted by the decaying f^2.
Translation differentiates the 1/r tail to 1/r^2; the older divergent
breathing-mode inertia is not transferred to this different perturbation.

PASS / DECISION: exact identities have zero residual; linear relative
algebraic residual <1e-9; independent momentum/energy phase formulas
agree relatively within 1e-9. Restored energy is within 3e-7 relative of
the stored .001 anchor. Grid/domain changes in M_I are <2e-5 relative and
in its nonzero energy difference <2e-3 relative. A difference exceeding
10 times its measured refinement change is resolved; either equality or
inequality is an admissible scientific decision. Positivity of u is
checked on the restored profile and the sufficient source-sign domain
f^2<6, |u|<.03, Omega>.75; a universal sign outside this domain is not
assumed. Numerical checks are not interval-arithmetic theorems.

FREEDOMS / STOP: all parameters and source dynamics are retained. Finish
with the dressed inertia, external-gradient acceleration and first
nonzero moving-exterior correction, plus any mismatch and its scope.
No full PPN fit, radiation campaign, new molecule/cosmology study or
strong-field continuation is part of this bounded task.

FILES / PROVENANCE: append this existing report; add one stdout-only
common_scale_slow_motion.py because it has a distinct l=1 solver and the
old candidate source is hash-pinned by other work. Update idea.txt after
the result. Keep the old source/response programs unchanged; runtime
prints hashes. Source SHA256:
6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8.
Historical E=M_G and restoring results remain in their original scope.

### 4.1. Translation requires an internal phase response

Let U(r), f(r), Omega be the retained stationary solution, a=exp(4U),
alpha=4 pi G. The precise action tested here is

    L = [exp(4u) u_t^2 - |grad u|^2]/(2 alpha)
        + exp(4u)|psi_t|^2/2 - |grad psi|^2/2 - exp(2u)V(|psi|),
    V(f)=f^2/2-f^4/4+f^6/24.

For translation along z, xi=x-vt e_z, use the regular slow-motion tangent

    u=U(xi)+O(v^2),
    psi=[f(xi)+O(v^2)] exp{i[omega t+v eta(xi)]},
    eta=h(r)cos(theta), omega=Omega+O(v^2).

The phase Euler equation at first order is

    div(f^2 grad eta) = -Omega partial_z(a f^2),
    (r^2 f^2 h')' - 2f^2 h = -Omega r^2(a f^2)'.

Simply translating the rest profile with unchanged phase does not solve
this equation. The zero-self-gravity solution is eta=-Omega z. Define
k=h+Omega r and zeta=eta+Omega z. The new response is obtained from

    integral [r^2 f^2 k' w' + 2f^2 k w] dr
      = -Omega integral (a-1)f^2[r^2 w'+2rw] dr.

Regularity requires k(0)=0. Finite weighted phase energy admits
h=-Omega[r+4C log(r)+O(1)] when U=C/r asymptotically; h itself need not
decay. At finite R the weak problem imposes the natural total-current
condition h'(R)+Omega a(R)=0. Individual integration-by-parts surface
terms there cancel through this condition; they are not separately zero.
The exponentially small matter amplitude controls the truncation error.

### 4.2. Inertia of matter and its entire environment

At fixed Q, eliminate the phase frequency with the Routhian L-omega Q.
Frequency and profile corrections of order v^2 cancel by stationarity of
the rest constrained functional. The reduced translational Lagrangian,
Noether momentum and energy are therefore

    L_body=-E0+M_I v^2/2+O(v^4),
    P_z=M_I v+O(v^3), E(v,Q)=E0+M_I v^2/2+O(v^4),
    M_I=integral a[(partial_z f)^2+(partial_z U)^2/alpha] d^3x
        + integral f^2 |grad eta|^2 d^3x
       =(4 pi/3) integral {r^2 a[f'^2+U'^2/alpha]
                          + f^2[r^2 h'^2+2h^2]} dr.

The independent phase contribution from momentum is

    -Omega integral a f^2 partial_z eta d^3x
      = integral f^2 |grad eta|^2 d^3x.

The phase equation tested against z also gives
integral f^2 partial_z eta=-Omega integral a f^2. Both identities hold for
the finite-ball natural-current problem and are preserved by consistent
P1 quadrature, since its test space contains r exactly.

For the exterior U=C/r, the full foundation translation contribution is

    M_I,u(>R) = pi C [exp(4C/R)-1]/(3 alpha),
    E_u(>R) = 2 pi C^2/(alpha R).

These are included analytically. The restored matter tail makes U=C/r an
asymptotic approximation, whose finite-R error is checked by changing R.
The translation derivative of the tail falls as 1/r^2 and has finite
kinetic energy. The earlier amplitude/breathing coordinate differentiates
its coefficient and has a different, 1/r falloff.

Using the retained stationary virial, write

    E0=Omega^2 integral a f^2 +(1/3) integral[|grad f|^2+|grad U|^2/alpha].

Completing the phase square gives the decisive identity

    M_I-E0 = (1/3) integral (a-1)[|grad f|^2+|grad U|^2/alpha]
             + Omega^2 integral (a-1)f^2
             + integral f^2 |grad zeta|^2.                         (SM1)

All integrals in SM1 are over full space. Its exterior gradient term is
pi C[exp(4C/R)-1-4C/R]/(3 alpha), because the virial has already combined
the rest potential and gradient energies. Subtracting the entire rest
tail here would double-count that rearrangement.

For nontrivial U>=0, SM1 is strictly positive. On the tested branch the
sufficient sign bounds are satisfied: f^2<6 implies V/f^2<=1/2, and
|U|<.03, Omega>.75 imply Omega^2 exp(2U)>1/2. Thus the stationary source
D=2exp(2U)f^2[Omega^2 exp(2U)-V/f^2] is nonnegative, and regularity with
U(infinity)=0 gives U>0. The numerical profile bounds support applying
this conditional analytic result; the numerics are not an interval proof.
The sign outside the specified branch is not inferred. At zero coupling,
U=0, zeta=0 and M_I=E0 as required for the flat canonical scalar.

### 4.3. Response to a weak external gradient

A constant external U_b is removed exactly from the action by
u=U_b+u_tilde, tau=exp(-U_b)t, X=exp(U_b)x. This rescales the entire dressed
body at fixed Q, including its frequency, profile and self-field tail:

    L_body(U_b,v)=exp(-U_b)L_body(0,exp(2U_b)v)
       =-exp(-U_b)E0+exp(3U_b)M_I v^2/2+O(v^4).

For a weak external field varying slowly across the body, at U_b=0 and
leading adiabatic monopole order,

    M_passive=E0=M_G,static,
    F=E0 grad u_ext, acceleration=(E0/M_I) grad u_ext.     (SM2)

The force also follows from the interaction stress flux through a buffer
sphere between body size and external-gradient scale. With self-field
C/r and external gradient g, the cross stress has surface integral
-4 pi C g/alpha, giving force +E0 g on the body. The pure external stress
is subtracted. A globally linear external potential is not assigned a
finite isolated-system energy. Tidal, radiation and finite-frequency
corrections are beyond this leading calculation.

### 4.4. First moving-exterior correction

The scalar charge read by the long-wavelength exterior follows from the
same background variation:

    q(v)=partial L_body/partial U_b|0=-L_body+2v.P=E+v.P
        =E0+(3/2)M_I v^2+O(v^4).                         (SM3)

The noncompact self-field produces no missing surface variation: a
change of its 1/r coefficient multiplies a derivative falling as 1/r^2,
so the additional boundary integral tends to zero. Equivalently, on the
uniformly translating solution its integrated source is

    q=integral [S_m + 2exp(4u)(v.grad u)^2/alpha] d^3x,
    S_m=2exp(4u)|psi_t|^2-2exp(2u)V.

This includes the moving foundation contribution. The asymptotic flux is
anisotropic:

    q=-(1/alpha) lim integral_sphere [(I-v v^T)grad u].n dS.

In the weak far region the wave equation gives the leading monopole,
with R=x-vt, n=R/|R| and the parallel direction along v:

    u=G q(v)/sqrt(R_parallel^2+(1-v^2)R_perpendicular^2)
     =G/|R| {E0+[(3M_I+E0)/2]v^2-(E0/2)(v.n)^2}+O(v^4/|R|).

Subleading spatial multipoles and nonlinear far-field terms are omitted.
There is no linear-in-v scalar correction. The ordinary spherical Gauss
flux is a different moving quantity:

    M_G,spherical=q atanh(|v|)/|v|
      =E0+[(3/2)M_I+E0/3]v^2+O(v^4).

At leading order in G, negligible self-gravity gives M_I=E0. An independent
flat-matter stress calculation then yields integral(T00+sum Tii)
=gamma E0(1+v^2), agreeing with SM3 and
u=G E0[1+2v^2-(v.n)^2/2]/|R|. This check boosts only the zero-gravity
canonical matter theory. The full preferred-frame scalar action was not
assumed Lorentz invariant. Its composite metric retains g_0i=0 in its
preferred coordinates; a GR gravitomagnetic sector has not been supplied.

### 4.5. Bounded numerical result and decision

The unchanged W58 seed and candidate BVP reconstructed only the required
alpha=.001 profile. The new angular problem used six-point Gaussian
quadrature per P1 element. No old radial Hessian or restoring-response
campaign was executed.

| R | phase cells | E0 | M_I | M_I-E0 |
|---:|---:|---:|---:|---:|
| 40 | 600 | 176.7394573473 | 180.5892388066 | 3.8497814593 |
| 40 | 1200 | 176.7394573471 | 180.5892391302 | 3.8497817831 |
| 60 | 600 | 176.7394573455 | 180.5892382725 | 3.8497809270 |
| 60 | 1200 | 176.7394573463 | 180.5892390013 | 3.8497816550 |

On the finest retained domain:

- Inertial excess (M_I-E0)/E0 = 0.02178224214 (2.178224214%).
- External-gradient acceleration coefficient E0/M_I = 0.9786821093.
- Phase, amplitude-gradient and foundation contributions to M_I are
  154.8997155298, 25.3318060310 and 0.3577174406 respectively.
- The included exterior foundation contribution is 0.01381618963.
- The three positive terms of SM1 are 0.4599431577, 3.3130802483 and
  0.07675825248; their sum differs from direct M_I-E0 by 3.57e-9.
- Omega=0.79574040384, max |U|=0.00821624 and max f^2=3.32166.
  The exterior coefficient C=0.01406447914 is positive; f(60)=4.49e-17.

The largest change in the gap under the prescribed refinements is
7.28e-7, over five million times smaller than the gap. The linear weak
system residual is below 5.2e-13, phase energy/momentum agree within
2e-16 relative and the first-moment identity within 4.5e-16. Rest energy
agrees with the saved anchor within 7.4e-12 relative. All registered
acceptance criteria pass: 13 algebraic checks and 36 numerical checks,
49/49, exit 0. This is successful detection of an inequality; the physical
mass-equality target fails on this branch.

The first development execution exposed a missing Omega factor in a
symbolic test substitution and NumPy Boolean JSON serialization. Both
were corrected; the phase solver's four numerical rows were unchanged.
The corrected saved executable passed the complete new bounded test.
Independent derivations checked the phase/current boundaries, full tail,
background stress force and moving charge definition.

Run:

    python -X utf8 -B "RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/common_scale_slow_motion.py"

Validated script SHA256:
4a3595f567a86299f172e4f902db6ee7b839941ed3cab9007f1d497d3ea45417.
Pre-execution contract report SHA256:
d80dffbb16642d80907708f8718b9d4e05ba6d510eac82580c06a79a1f7e915b.
Environment: Python 3.10.6, NumPy 1.24.3, SciPy 1.15.2, SymPy 1.13.3.
The script prints source, contract and unchanged dependency hashes and
writes no result files. The report hash changes when these results are
appended; the pre-execution contract is retained above.

**Decision:** the same APR action consistently defines conserved energy,
translation momentum and scalar gravitational response, but on this
self-gravitating branch M_I>E0=M_passive=M_G,static. Its static balance
and restoring results remain valid. The new obstacle is the equivalence
of translational inertia and gravitational response, with a precisely
located positive difference SM1. Its magnitude here is a model benchmark,
not an observational bound or a prediction for a specified real object.

The later finite-b rate-limited kinetic term expands as

    b^2/(alpha p^2)[1-sqrt(1-u_t^2/(b^2p^2))]
      =u_t^2/(2alpha p^4)+u_t^4/(8alpha b^2p^6)+O(u_t^6).

It therefore leaves the quadratic translation coefficient unchanged on
the same rest profile. Choosing b alone cannot remove SM1. Before using
this candidate as the strong-field dynamical foundation, the next action
construction must address the leading moving matter/environment response
and repeat this mass/force test from that explicitly stated action. Any
changed action must establish which static results it preserves.
Finite-velocity existence, coupled dynamical stability, radiation and a
full PPN/observational analysis are outside the completed claim.
