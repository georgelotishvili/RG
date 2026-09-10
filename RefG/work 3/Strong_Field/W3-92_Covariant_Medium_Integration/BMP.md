# BMP–RefG: source response, mass accounting and the regularity test

## გადაწყვეტილება მოკლედ

BMP-ის მოქმედებით შეთანხმებული წყაროს რუკა გამოსადეგია RefG-ის თვითრეგულირების შესამოწმებლად. იგი ენერგიის, წნევისა და დამატებითი გრავიტაციული წვლილის ერთობლივად გამოთვლის ზუსტ წესს გვაძლევს. შესაბამისი დენითი ინტერფეისი W3-79-ში უკვე გვაქვს; ხელახლა ასაგები არ არის.

სტატიის კონკრეტული ლოგარითმული კანონი მზა RefG-ამოხსნად ვერ გადმოვა: მისი სრული ასიმპტოტური მასა უცვლელია, სიმრუდეს სასრული ზედა ზღვარი არ აქვს და მისი დამოუკიდებელ ადგილობრივ სითხედ გამოყენება ჩვენს მდგრადობის პირობას ვერ გადის. ეს შედეგები ქვემოთ პირდაპირ მისი ფორმულებიდან მოწმდება.

გამოყენებაში შემოდის სრული წყაროს ლექსიკონი, მასის ზუსტი ეტალონი, გარე ენერგიის აღრიცხვა და სიმრუდის/დროის სწრაფი ფილტრი. ჩვენს უკვე მიღებულ წონასწორობასა და მასის კლებად ნამატს ეს შემოწმება ძალაში ტოვებს. შემდეგი ფიზიკური ამოცანაა ერთობლივი მატერია–გარემოს მდგომარეობითი პასუხი; მარტო ლოგარითმული სიმკვრივის ჩასმა მას ვერ ჩაანაცვლებს.

## Scope and decision contract

- CLAIM_ID: BMP_REFG_IMPORT_AUDIT_2026_09_10; TYPE: exact source dictionary, reference-model checks and bounded import decision.
- MODEL: BMP's published 2024 dust action and spherical matching; one directly related 2026 bounded-core example is a separate benchmark.
- ASSUMPTIONS: signature (-+++), c=1 and 8 pi G_N=1; epsilon>0, xi>0; homogeneous pressureless reference matter epsilon=m n; conserved proper-volume number current. Static radii are areal radii. M is geometric Misner–Sharp mass, with f=1-2M/R. BMP's F_eff=2M.
- FREEDOM: xi remains a free inverse-density scale; no RefG value, observed mass fit, node model, new species or preferred cutoff is supplied. epsilon=m n is a declared effective-dust identification, not an identification of n with the existing oscillon charge Q or foundation pressure P_F.
- PASS: source variation/conservation, independent mass matching, curvature limits and positive/negative controls agree. A physical drop-in additionally needs the existing local health conditions, a same-action exterior and a derived RefG operational map.
- FALSIFIER: any nonzero exact residual invalidates its identity; negative local sound-speed squared rejects the corresponding standalone barotropic drop-in, not every multi-field theory.
- DOMAIN: homogeneous dust, reference spherical exterior and local barotropic perturbations, separately labelled. No numerical RefG collapse or generic global completeness proof is asserted.
- METHOD/CROSSCHECK: current variation and thermodynamic volume work; boundary mass and Einstein exterior source; Friedmann curvature and static metric invariants; exact symbolic algebra and a high-precision double-horizon root.
- OBSERVATIONS/FORWARD MODEL: N/A; no detector data or observational acceptance. The horizon root reproduces a published mathematical example.
- STATUS: reference_source_dictionary=true; BMP_standalone_fluid_healthy=false; BMP_uniform_curvature_bound=false; BMP_same_action_global_exterior_established=false; RefG_regular_black_hole=false; RefG_theory_excluded=false.
- FILES/STOP: this report, verify_bmp_reference.py and verify_refg_source_boundary.py form the Git-visible verification package. Published monographs and existing solvers remain unchanged. The third-party article copy is optional and excluded from Git. The scope ends at the verified import decision.

## 1. What can be reused exactly

Let E(epsilon)=chi(epsilon) epsilon. BMP's action is Einstein–Hilbert plus -E, with the conserved-current constraints understood. In the notation below, E is an effective local energy density, not total ADM energy. Metric variation gives [1, Eqs. 1–7]:

    rho_eff = E,
    P_eff = (epsilon + P_bare) E' - E,
    G_eff/G_N = E',
    Lambda_eff = E - epsilon E'.

The last two terms are a decomposition of one source. For dust:

    P_eff = epsilon E' - E = -Lambda_eff,
    T_eff = epsilon E' u u + P_eff g.

Equivalently, for epsilon=m n:

    rho(n)=E(m n),  mu=m E',  P=n mu-rho,
    T_eff=n mu u u+P g,  div(n u)=0.

This is exactly the current-source interface already derived in W3-79, §§1–2. It can be reused without resolving constituent molecules or inventing node collisions. Replacing a current energy function changes that sector's constitutive physics; adding the same effective source on top of its old source would count it twice.

The volume-work identity independently fixes the pressure:

    d[rho(n) V]/dV at fixed N=nV = -P.

The average mass contribution per bare mass is E/epsilon. The additional contribution when the bare source changes is E'. They differ:

    E'=chi+epsilon chi'.

Using chi as though it were E' omits the change in the previously present matter's effective contribution. In this precise sense the article supplies a useful version of the reciprocal feedback bookkeeping sought in RefG.

For nonuniform states, conservation of the effective source follows its own matter equations. Simultaneous conservation of a separately prescribed bare perfect-fluid stress imposes an additional spatial condition proportional to (epsilon+P_bare) E'' grad_perp(epsilon). Homogeneous dust satisfies it. An inhomogeneous implementation must vary and solve the current equations rather than assume both Euler equations.

## 2. BMP's explicit response and the mass ledger

For x=xi epsilon [1, Eqs. 18–19]:

    E = ln(1+x)/xi,
    chi = ln(1+x)/x,
    E' = 1/(1+x),
    P = epsilon/(1+x) - ln(1+x)/xi.

E is increasing and concave; chi and E' decrease. For an ideal fixed-volume dust cell, dE_total/dN=m E' and d²E_total/dN²=m² E''/V<0. This is an exact reference example of diminishing increments. It does not yet describe a self-gravitating equilibrium sequence with changing volume.

Matching a homogeneous boundary R_b=r_b a to the selected static exterior gives [1, Eqs. 23–31]:

    M(R) = R³ E(6M0/R³)/6
         = R³ ln(1+6M0 xi/R³)/(6xi).

Writing q=6M0 xi/R³:

    M/M0=ln(1+q)/q,
    partial M/partial M0 at fixed R=1/(1+q),
    partial² M/partial M0²=-6xi/[R³(1+q)²].

At fixed R, M grows logarithmically without a finite cap as M0 grows. Throughout a collapse with fixed M0, the total ADM mass at spatial infinity is M0. The shrinking material cloud encloses M(R_b), while the geometric exterior contribution is:

    integral_(R_b)^infinity M'(R) dR = M0-M(R_b).

This is an Einstein mass-function integral, not the unweighted proper-volume integral of local energy. It is not a model of radiated merger energy.

An independent Einstein-tensor readout of the static metric gives:

    rho_ext=2M'/R²=[ln(1+q)-q/(1+q)]/xi>0,
    P_r=-rho_ext,  P_t=-M''/R.

At the boundary P_r agrees with the interior P. The exterior is therefore an effective anisotropic source region, not vacuum. Setting epsilon=0 literally outside the dust in the action above gives vacuum Einstein equations and M'=0 instead. Matching determines the required exterior stress; its origin from the complete physical action remains a separate obligation. RefG's exterior medium is a possible place for that obligation, not an already established identification.

## 3. What the endpoint calculation actually establishes

In BMP's interior ds²=-dt²+a² dSigma², t is the comoving proper time. Its a is an operational FLRW contraction scale, not RefG's foundation expansion scale and not the exterior-to-local clock factor p.

For spatial curvature K=0 [1, Eqs. 11–22]:

    H²=E/3,  dot(H)=-epsilon E'/2,
    Ricci=4E-3epsilon E',
    Kretschmann=12[(E/3-epsilon E'/2)²+(E/3)²].

The late-time result a~exp[-(t-t0)²/(4xi)] means no zero radius at finite comoving proper time. Direct limits give:

    Ricci/ln(x) -> 4/xi,
    Kretschmann/[ln(x)]² -> 8/(3xi²).

Thus this branch has unbounded late-time curvature. Continuing the static exterior formula alone to R=0 also gives logarithmically divergent curvature. BMP's actual moving-boundary exterior excludes R=0 at every finite t, so the static extrapolation is not by itself a counterexample inside that finite-time domain.

The W3-87 geodesic test applies independently:

    d lambda_null is proportional to a dt.

The Gaussian contracting homogeneous patch has finite future null affine length although comoving proper time is infinite. A finite material cloud has a boundary that a ray can cross; its complete matched spacetime must be tested across that boundary and possible extensions. Neither a>0 nor the patch integral alone establishes the global verdict.

Positive E' leaves rho_eff+P_eff=epsilon E'>0. BMP weakens the source and can violate the strong energy condition; it does not automatically supply negative radial null focusing. This distinguishes it from the particular defocusing target of W92 Stages 26–28.

## 4. The shortest useful regular-centre filter

Since E(0)=0:

    E(epsilon)=integral_0^epsilon [G_eff(s)/G_N] ds.

For a nonnegative response, a finite integral as epsilon tends to infinity is exactly the bounded-energy criterion. In the homogeneous Einstein cell, bounded E and bounded epsilon E' give bounded algebraic curvature. With sufficiently controlled derivatives, the same matching formula then has M(R)=O(R³), the regular static-centre scaling.

BMP's 1/epsilon marginal decay fails this integral test logarithmically. A strict positive power response E'~epsilon^(-q) passes it for q>1; borderline logarithmic modifications must be tested by the integral itself. This is a mathematical filter, not a selected RefG function.

The directly related 2026 paper [2, §V, Eqs. 44, 46–47] supplies a useful bounded-core benchmark, its p=2 case:

    E_2=epsilon [1-exp(-1/(xi epsilon))],
    M_2(R)=M0[1-exp(-R³/(6xi M0))].

Independent substitution here gives E_2->1/xi, P_2->-1/xi and central Kretschmann->8/(3xi²). It demonstrates precisely what the logarithmic BMP response lacks. Its marginal response is positive and tends to zero, so a curvature-bounded core does not require repulsive negative G. This remains a background/metric benchmark, with ADM mass M0 and a separate global-extension problem.

There is also a 2026 preprint directly questioning singularity resolution by effective sources [3]. Its revised claim concerns homogeneous spatially flat collapse and specified analytic gravitational responses. It reinforces the need to separate curvature and affine completeness. It is not treated here as a peer-reviewed or universal exclusion of RefG, and none of the calculations above depends on accepting its theorem.

## 5. Compatibility with existing RefG: what is and is not the same

| Item | Exact relationship and decision |
|---|---|
| Self-regulating feedback in RefG_GE §1.5 | Compatible motivation for a joint source law; BMP does not derive the foundation-pressure or clock/rod map. |
| W3-79 conserved-current action | E(m n) is an exact source dictionary. It must pass that action's local health test. |
| W92 global mass response | The existing dM_ADM=Omega dQ and decreasing Omega on the tested stable branch are retained. Global mass concavity is different from negative local fluid compressibility. |
| Operational scaling p | W92 already gives E_K=m0 N with lapse N=p. Replacing m0 by p m0 again double counts clock redshift. chi, E' and p cannot be equated by name. |
| W3-87 F_grav(n) T action | Different operator: its weighted TEGR-to-Einstein conversion contains a bulk torsion-gradient term. It is not BMP's E(epsilon). |
| W92 Stage 26 | The healthy algebraic comoving-medium class has positive radial null source. BMP's dust source also has positive null contraction. |
| W92 Stages 27–28 | The derivative prototype's tested ordinary-exterior connections fail. BMP matching does not repair that action's current equations or derive its source coupling. |
| Finite exterior / horizons | Matching and horizon benchmarks are reusable; global causal completion and inner-horizon stability are separate. |

The decisive local health check already exists in W3-79:

    c_ad²=n rho''/rho' = epsilon E''/E'.

For BMP it is -x/(1+x)<0. For the bounded E_2 example, E_2'>0 and E_2''=-exp[-1/(xi epsilon)]/(xi² epsilon³)<0, so its standalone barotropic interpretation also fails this test. The corresponding short-wave fluid perturbation has omega²=c_ad² k² and an exponentially growing mode when a valid fluid wavelength band exists.

This is a conditional, local EOS obstruction. It does not negate the stable, self-gravitating oscillon configurations already calculated in W64–66/W92. In particular, their concave total M(Q) is not rho(n) in a fixed local volume. Nor does this test determine the full perturbation theory of an unspecified microscopic asymptotic-safety completion.

The maximum justified import is therefore the source/pressure/mass dictionary and the tested reference solutions. A successful RefG continuation must obtain the joint constitutive response from its matter–medium action, count the exterior stress once, and check its constrained modes. A density-only logarithm, silently added to the existing canonical solver, would import both the local instability and a source-counting ambiguity.

## Sources and local anchors

1. A. Bonanno, D. Malafarina, A. Panassiti, “Dust Collapse in Asymptotic Safety: A Path to Regular Black Holes,” Physical Review Letters 132, 031401 (2024), DOI https://doi.org/10.1103/PhysRevLett.132.031401. The relevant formulas (Eqs. 1–33) and completeness wording were checked in https://arxiv.org/html/2308.10890v2 (revision listed 4 May 2026).
2. A. Panassiti, “Regular black hole cores via gravitational evanescence of collapsing matter,” Physical Review D 113, 064057 (26 March 2026), DOI https://doi.org/10.1103/fbz2-8n2h; https://arxiv.org/html/2509.17234v2, §V. Only the explicitly identified p=2 example is imported as a benchmark here.
3. Z.-X. Zhang, C. Lan, Y.-G. Miao, “No-Go Theorem for Singularity Resolution,” preprint https://arxiv.org/html/2604.00204v2 (7 July 2026), §§III–IV and affine-parameter supplement. No journal acceptance is inferred from the arXiv record.
4. intuitive/RefG_GE.md, §§1.5, 2.2, 3.1; W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction_contract.md, §§1–2; W3-87_State_Dependent_Gravitational_Response/w3_87_state_dependent_response_contract.md, §§1–4.
5. W3-92_Covariant_Medium_Integration/medium_health_horizon_diagnostic.md, Stage 15 parts A–C and Stages 25–28. The source equations and branch restrictions remain those of the cited RefG documents.

## Reproducible verification

The author-written checks are standalone Python programs in this directory:

- [verify_bmp_reference.py](verify_bmp_reference.py): 42 scientific checks of the source dictionary, enclosed/ADM mass, curvature, fluid response and double-horizon benchmark.
- [verify_refg_source_boundary.py](verify_refg_source_boundary.py): 41 scientific checks of the RefG clock, source tensor and moving-boundary mass, pressure and flux.

Tested dependencies: Python 3 with SymPy 1.13.3 and mpmath 1.3.0. Install these in the chosen Python environment if needed:

~~~powershell
python -m pip install sympy==1.13.3 mpmath==1.3.0
~~~

From the repository root:

~~~powershell
python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_bmp_reference.py"
python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_refg_source_boundary.py"
~~~

Append --verbose to either command to print every check, its type and any exact residual. Each script prints a JSON summary and exits 0 when all declared checks pass, 1 when a check fails. Both also expose run_checks() for programmatic verification; importing either module runs no calculations. An absolute script path works from any working directory.

The scripts read no project files, require no downloaded article copy, and write no output files. Formulas and controls retain the original audit mathematics. The main code is stored only in the .py files; this report supplies its assumptions, derivations, citations and interpretation.

The original embedded suites had 50 and 44 checks: respectively 42 scientific plus 8 file-hash checks, and 41 scientific plus 3 file-hash checks. All 83 scientific checks are retained. The 11 file-hash checks recorded the earlier workspace state; their values are preserved below as historical provenance instead of runtime mathematical dependencies.

The double-horizon benchmark gives xi/M0²=0.4564624856615580 and R/M0=1.2515650684025658. Its function and derivative residuals must each be below 1e-50 at 60-digit precision. The source-boundary example gives the clock relative error 0.17563936464993593. Passing these checks establishes the identities and stated import decisions within the report's domain.

## RefG implementation: preserve the clock and the moving-boundary source

### Decision and frozen scope — 2026-09-11

CLAIM_ID: REFG_SOURCE_BOUNDARY_IMPORT_V1. This addition adapts the useful BMP matching method to the retained RefG scalar/current and explicit medium sources. It supplies a necessary source-consistency gate for a proposed exterior, rather than a new density law.

The new question is concrete: can a mass-matched exterior retain the actual RefG clock, radial pressure and energy flux? The previous comparison tested BMP's constitutive function; this calculation tests its exterior restriction against RefG's own sources.

Conventions are (-+++), c=1, G>0, physical Misner–Sharp mass m and areal radius R. Static orthonormal formulas apply on f>0; the covariant timelike-boundary formulas also apply in a regular orthonormal frame through a horizon. All sources below are the total Hilbert tensor, counted once. The W64 scaled equations replace 4 pi G by alpha and use M'=R² rho.

The junction is a Darmois junction with no surface layer or distributional shell stress. A physical Israel shell has its own energy, pressure and evolution equations and is outside this gate.

No action coefficient, matter content, clock/ruler law, boundary radius or observational parameter is changed. Necessary residuals must vanish identically; explicit dropped-pressure, dropped-flux and frozen-clock mutations must fail. The source gate is not sufficient for a complete junction: induced metric, both extrinsic curvatures, field/current boundary equations and existence of the boundary must also be satisfied. This is an exact conditional interface, with numerical evaluation of one already specified metric only.

The implementation consists of this report and its two Python verification scripts. Existing W64/W79/W92 solvers and monographs retain their original equations. The stopping point is the verified import decision on the existing sources.

### 1. Two metric functions are required by the source

Preserve the general static spherical form already used by RefG:

    ds²=-exp(2d(R)) f(R) dt²+dR²/f(R)+R²dOmega²,
    f=1-2G m(R)/R,   lapse=exp(d) sqrt(f).

Direct evaluation of the Einstein tensor gives:

    m'=4 pi R² rho,
    d'=4 pi G R (rho+p_r)/f.

BMP's d=0 is therefore a physical restriction rho+p_r=0 throughout the region, after normalizing the exterior clock. A radial change of coordinates cannot remove it while preserving the areal radius and the stated metric form.

For the actual canonical W64/W92 oscillon with amplitude h, frequency Omega and sigma=exp(d):

    rho+p_r=f h'²+Omega² h²/(sigma² f)>0 where h is nonzero.

The second metric function carries an essential clock response. This conclusion holds independently of the potential and requires no molecular calculation.

For W92's explicit exponential-medium exterior, on its outer areal branch r>m_g:

    u=m_g/r,  R=r exp(u),  f=(1-u)²,
    d=-u-ln(1-u),  lapse=exp(-u),
    rho=p_r=-u²/(8 pi G R²),
    d'=-u²/[R(1-u)²].

Both source components are reproduced by the two-function geometry. Setting d=0 would keep the same mass function but change its radial pressure and clock. At the illustrative point r=2m_g, the correct lapse is exp(-1/2)=0.60653066; the forced one-function lapse would be 0.5, a 17.56% relative error. This is an exact-metric comparison on the existing candidate exterior, not an observational prediction or a health endorsement of its perturbations.

### 2. Mass matching must propagate with pressure and flux

Let U be the unit tangent of a timelike spherical boundary and N its outward unit normal. Define:

    Rdot=U(R), beta=N(R),
    q_Sigma=T(U,N), P_Sigma=T(N,N).

q_Sigma is a tensor contraction; its sign is opposite to the outward energy flux measured by the boundary observer. Relative to a local orthonormal frame with S=T_hat0hat1 and boundary velocity v:

    q_Sigma=[v(rho+p_r)+(1+v²)S]/(1-v²),
    P_Sigma=[v²rho+2vS+p_r]/(1-v²).

The exact Einstein mass identity then gives:

    U(m)=4 pi R² [beta q_Sigma-Rdot P_Sigma].

This follows independently by substituting W79's m_T and m_R into U(m). If the angular matching condition fixes a common beta and the induced radius history agrees, the jumps obey:

    U(Delta m)=4 pi R² [beta Delta q_Sigma-Rdot Delta P_Sigma].

Thus equal masses on one slice remain equal only when the subsequent source balance is also correct. An omitted pressure or flux can be invisible in the initial mass number and immediately violate its evolution.

A one-function static exterior has, in every boundary frame:

    q_Sigma^+=0,  P_Sigma^+=-rho_ext,
    rho_ext=m_ext'/(4 pi R²).

Its necessary import gate is:

    Delta m=0,  q_Sigma^-=0,  P_Sigma^-+rho_ext=0.

For a general two-function static exterior, with boundary velocity v relative to its static frame:

    q_Sigma^+=v(rho_ext+p_r_ext)/(1-v²),
    P_Sigma^+=(v²rho_ext+p_r_ext)/(1-v²).

These are the quantities to compare with the interior. The implementation therefore preserves the second clock function and supports the actual scalar and medium stresses.

### 3. Concrete consequence for the next RefG construction

A homogeneous comoving perfect-fluid interior has q_Sigma^-=0. For a boundary moving relative to a static exterior, flux continuity consequently requires rho_ext+p_r_ext=0. BMP's chosen exterior satisfies this condition. The nonzero exponential RefG medium has rho_ext+p_r_ext<0 and fails that particular homogeneous/comoving-to-static construction.

This is an exclusion of that combination of boundary and exterior assumptions. A RefG construction must supply the corresponding interior flux, use an appropriate noncomoving/nonhomogeneous boundary, or solve a dynamical exterior, as dictated by the same action. These are options to be derived, not extra contributions inserted by hand. The existing canonical oscillon and exponential-medium branches remain separate source models; they have not been joined here.

The independent clock equation and all three boundary residuals are now the selected import checks for subsequent RefG source candidates. The existing W92 Stage 28 constitutive obstruction remains unchanged. This implementation strengthens the formal matching test; it does not select a healthy new medium or establish singularity resolution.

### Source and verification anchors

BMP source [1], Eqs. 23–28, supplies the matching-method motivation. The complete RefG interface uses W3-79 contract §§1–3 and W3-64 preregistration/source equations for the scalar. The exponential source is from W3-92/FORMAL_COVARIANT_MEDIUM_INTEGRATION.md, “Model, conventions and source ledger,” with its documented signature conversion and branch limits. No claim of original discovery is made for the Einstein mass identity or Darmois–Israel junction conditions.

[verify_refg_source_boundary.py](verify_refg_source_boundary.py) computes the static Einstein tensor directly, reconstructs the actual RefG stresses, and verifies the boundary law independently in W79's horizon-regular coordinates. Its direct connection calculation also tests the boundary acceleration. The commands and dependency versions are given under “Reproducible verification” above.

### Standalone Python verification — 2026-09-11

The reference script passed 42/42 scientific checks; the source/clock/boundary script passed 41/41. Every check record (name, kind, result and exact residual where present) was compared with the corresponding original block after separating the historical file hashes; all 83 records agreed exactly. The horizon and clock numbers were unchanged. Both command-line programs were also run from their own directory using absolute paths and --verbose. Imports were silent, and an injected failed-check result produced exit status 1.

The useful transfer is complete at this scope: RefG retains its actual clock and source tensor, while proposed spherical exteriors must satisfy mass, radial traction and energy-flux matching together. A mass-only match is no longer an admissible substitute for this necessary test. The next physical construction must supply a compatible source and boundary from the same action; the present gate does not supply them or remove the Stage 28 obstruction.

The report and both Python files are available to Git under the user's explicit export instruction. The third-party article copy remains excluded. Existing model equations and monographs were unchanged. No commit, push or external publication was performed.

### Historical workspace provenance

The original embedded runs checked raw-byte SHA-256 values below (8 reference checks and 3 boundary checks; W3-79 appears in both). These values identify that workspace snapshot. Line-ending conversions and later edits can change them without changing the mathematics. The standalone scripts do not read or require these files; the cited formulas are explicit in their source. The locally retained paper copy is optional and is not distributed with this package.

| Original suite | Repository-relative file | Original SHA-256 |
|---|---|---|
| Reference | BMP.md | de897e0b8665cf9b205ec7df2e89c9acb76d4011afae6077d3b66be71801fcd5 |
| Reference | intuitive/RefG_GE.md | 1ec492831c688a372b955ecdf80863c13e258e63891043aa3664279aa94e9f7c |
| Reference | intuitive/RefG_EN.tex | c30c4e0f5e66cf27eccfec8dbbd9d6cc744bf6f6739820a8703b3ada3d971398 |
| Reference | .gitignore | 1a509202c41432c1206dee4be2cd844d5c83ea74d815e6d769a23866d7687fcf |
| Reference + Boundary | RefG/work 3/Strong_Field/W3-79_Collective_Current_Backreaction/w3_79_collective_current_backreaction_contract.md | 7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa |
| Reference | RefG/work 3/Strong_Field/W3-87_State_Dependent_Gravitational_Response/w3_87_state_dependent_response_contract.md | 7c47bcd4efe292a91d13717a3ec3962776488b01c521dfb27b9df1e989fcee80 |
| Reference | RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/medium_health_horizon_diagnostic.md | cc6d046e68c660aa47de5128f9960788a2a48caaf40d40ff189c8b3a3f79b0e4 |
| Reference | RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/population_assembly_initial_data.py | df0d16c7715a2c3e3e02ec3487f2cad2860bf772e69983de6e2fb5af295af97d |
| Boundary | RefG/work 3/Strong_Field/W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field_preregistration.md | 25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1 |
| Boundary | RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/FORMAL_COVARIANT_MEDIUM_INTEGRATION.md | 3c01e91cc42ce05e2b26a0c98e63a89e24faa609de87164094f4d7acd485085c |
