# Matter-induced medium response on the existing active branch

## Frozen question and scope — 2026-09-11

CLAIM_ID: W92_ACTIVE_SOURCE_RESPONSE_V1. Test whether the existing Stage 27 action responds to nonzero ordinary matter when its medium is active, and determine the first weak metric/clock/ruler response. Keep the action and polynomial fixed. Stage 28's constant-field and ordinary-flat-exterior exclusions remain valid.

- Type: exact conditional source response; local implicit-function result; finite-precision initial-data verification. The spatial result is a leading classical quasistatic kernel.
- Action: signature (-+++), S = integral sqrt(-g) [P R/2 + K(X) - g X Box(phi)] + S_O[g,psi], X = -partial(phi)^2/2. Here g is the cubic coupling, P is the constant Planck coefficient, and S_O is the retained canonical complex ordinary scalar, counted once.
- Frozen polynomial: K(X) = X + X^2/2 - 282 X^3 + 802 X^4 - 624 X^5. Use P=g=1 in the already registered dimensionless witness. No coefficient is adjusted to the new answers.
- Reference state: a=1, phi=0, v=phi_dot=1, H_c=1, ordinary field zero; J=-1, rho_phi=3, phi_ddot=1/3 and H_c_dot=2/3. H_c denotes the Hubble rate, not the original article's deficit scalar H.
- New source family: add rho_O=epsilon>0 at the initial slice with p_O=0, holding a=1 and a^3 J=-1 fixed. Solve for H_c and v jointly. Realize p_O=0 by equal phase kinetic and potential energies of the existing ordinary scalar, not by adding a permanently pressureless species.
- The fixed a^3 J is the medium's Noether shift charge. It is distinct from the ordinary scalar's phase charge and has no established foundation-particle-count interpretation.
- Domain: the locally unique branch through epsilon=0; finite checks at epsilon = 10^-6, 10^-5, 10^-4. No continuation to large density is selected.
- Exact targets derived before execution: constraint Jacobian determinant 27; H_c'=1/9, v'=-1/9, rho_phi'=-1/3, rho_total'=2/3 at epsilon=0. Primes in this sentence mean derivatives with respect to the added ordinary energy density.
- Numerical test: 60- and 90-digit independent root algorithms; equation residuals below 10^-45, common results within 10^-45. Verify the same initial scalar realization, current, Friedmann equation, acceleration equations and energy continuity.
- Spatial test: preserve independent Newtonian potentials until the traceless Einstein equation sets Phi_N=Psi. Derive the scalar/metric coefficients independently from the covariant current, Hilbert source and quadratic static action. No new static exterior or thin shell is imposed.
- Rejection controls: frozen H_c and v after adding matter must fail Friedmann; changing J silently must fail the family definition; omitting cubic mixing must erase the predicted forcing; applying the vacuum scalar-speed formula with nonzero ordinary background must fail its source correction.
- Observations, likelihood and calibrated physical cutoff: N/A to this calculation. The earlier prototype has no established physical EFT band. Same-P GR normalization is checked separately from the equality of clock and rod responses.
- Files: this report and verify_matter_medium_source_response.py; brief index in the W92 main diagnostic and idea.txt. Existing solvers, monographs and private article copies are unchanged. This package is Git-visible.
- Stop: derive and verify the finite-source response and the weak spatial readout. Full nonlinear collapse, new constitutive laws, global stability and singularity resolution are outside this bounded step.

## Existing foundations and what was absent in the constant branch

W3-51 already derives the fixed-active-source equation for u=-ln p. W92 Stage 8 already includes the reciprocal exp(-u) matter response, and Stage 9 diagnoses the missing independent gravitational constraint in that restricted static functional. Stages 6–7 contain a different source-coupled completion whose transverse instability is retained. Repeating those calculations would not close the current gap.

The Stage 27 derivative candidate has the conserved current

    j^mu = (K_X - g Box(phi)) partial^mu(phi) - g partial^mu(X).

Its divergence gives

    K_X Box(phi) - K_XX phi^mu phi^nu phi_mu_nu
      + g [phi_mu_nu phi^mu_nu - Box(phi)^2
           + R_mu_nu phi^mu phi^nu] = 0.

Einstein's equation makes the ordinary source contribution explicit:

    (g/P) [T^O_mu_nu - T_O g_mu_nu/2] phi^mu phi^nu.

On a timelike background this is g v^2 (rho_O+3p_O)/(2P). It vanishes for constant phi and is present for the existing active state. The scalar's own derivative stress must still be kept when the coupled equations are solved. This is the established curvature-mediated kinetic-braiding mechanism [1], now evaluated on the retained RefG prototype; no direct matter coupling has been invented.

## Exact source family at fixed medium charge

For X=v^2/2:

    rho_phi = v^2 K_X - K + 3g H_c v^3,
    p_phi = K - g v^2 phi_ddot,
    J = v K_X + 3g H_c v^2,
    3P H_c^2 = rho_phi + rho_O,     d(a^3 J)/dt = 0.

The ordinary homogeneous amplitude h and phase theta have

    rho_O = (h_dot^2 + h^2 theta_dot^2)/2 + U(h),
    p_O   = (h_dot^2 + h^2 theta_dot^2)/2 - U(h).

Choose h_dot=0, 2U(h)=epsilon and theta_dot=sqrt(epsilon)/h initially. The positive-mass canonical potential has such a small-amplitude branch. For the numerical realization use the retained dimensionless sextic U(h)=h^2/2-h^4/4+h^6/24; this specifies source initial data, not a new coupling or a persistent dust equation of state. Its subsequent pressure is determined by the ordinary field equation.

This is a homogeneous excitation of the retained ordinary field, not a localized stationary oscillon or a prepared particle ensemble. Holding v fixed instead would change J: at epsilon=0 that different family has J'=1 and H_c'=1/3. Fixed medium charge is the specified comparison here; the compensating fraction is not independent of how the initial family is defined.

At fixed a=1 and J=-1 the two constraint derivatives in variables (H_c,v) are

    [ 3  -6 ]
    [ 3   3 ],     determinant = 27.

Thus a locally unique family follows by the implicit-function theorem. The same equations give

    H_c = 1 + epsilon/9 + (238/243) epsilon^2 + O(epsilon^3),
    v   = 1 - epsilon/9 + (955/486) epsilon^2 + O(epsilon^3),
    rho_phi = 3 - epsilon/3 + (479/81) epsilon^2 + O(epsilon^3).

To first order, the medium compensates one third of the added ordinary density; total density increases by two thirds. These are local homogeneous initial densities at fixed medium charge, not the ADM mass of an assembled black hole. The positive quadratic coefficient already shows that this series does not establish a saturation ceiling or monotonically decreasing mass increments.

The action also fixes both accelerations:

    D = K_X + v^2 K_XX + 6g H_c v + 3g^2 v^4/(2P),
    D phi_ddot = -3H_c v K_X - 9g H_c^2 v^2
                 + 3g v^4 (K_X+3g H_c v)/(2P)
                 + 3g v^2 (rho_O+p_O)/(2P),
    2P H_c_dot = -[v^2 K_X+3g H_c v^3
                   -g v^2 phi_ddot+rho_O+p_O].

These satisfy the independent current equation, scale-factor equation and total energy continuity with the ordinary scalar's equation. The medium response is computed simultaneously with geometry; it is not assigned after solving the metric.

## Local spatial response and operational scales

In a local FLRW patch take

    ds^2=-(1+2Psi)dt^2+a^2(1-2Phi_N)dx^2,
    phi=phi_background+pi,   Delta=a^-2 nabla^2.

At leading quasistatic spatial-derivative order, use a nonrelativistic,
slowly varying ordinary source with negligible pressure and anisotropic
stress, conserved to the retained order:

    C = K_X + 2g phi_ddot + 4g H_c v,
    B_mix = g v^2,        A_eff = C - B_mix^2/(2P),
    C Delta pi + B_mix Delta Psi = 0,
    2P Delta Psi + B_mix Delta pi = delta rho_O,
    Phi_N = Psi.

The direct Hessian expansion of the scalar equation gives C; the high-spatial-derivative medium density is -B_mix Delta pi. An independent quadratic static action is

    L_QS = P[(grad Phi_N)^2-2 grad Phi_N.grad Psi]
           - C (grad pi)^2/2 - B_mix grad Psi.grad pi - delta rho_O Psi.

Its three Euler equations reproduce the same constraints. At the original active witness:

    C=2/3, A_eff=1/6, Delta Psi=2 delta rho_O,
    Delta pi=-3 delta rho_O, pi=-3Psi/2,
    G_eff/G_EH=4,   G_EH=1/(8pi P).

For a smooth Gaussian source of total initial ordinary mass B and width L, the formal local kernel is

    delta rho_O=B exp(-r^2/L^2)/(pi^(3/2)L^3),
    Psi=-G_eff B erf(r/L)/r,  pi=-3Psi/2.

It is regular at the source centre, with Psi(0)=-2G_eff B/(sqrt(pi)L). Decay here means matching the perturbation to the homogeneous background in the local approximation, not a globally asymptotically flat spacetime or an ADM construction.

The Gaussian is an illustrative Green-function source profile. An
inhomogeneous solution of the ordinary W58 scalar field realizing that
profile has not been constructed in this calculation.

For slowly moving probes relative to that local background:

    clock ratio = 1+Psi+O(Psi^2),
    coordinate length per unit local rod = 1+Phi_N+O(Phi_N^2),
    rest-energy readout / local rest energy = 1+Psi+O(Psi^2),
    coordinate light-speed ratio = 1+Psi+Phi_N+O(perturbation^2).

Thus the linear p/p^2 readout is recovered when Phi_N=Psi. The scalar pi itself is not identified with p or the original article's H. The factor four differs from same-P vacuum GR and requires a physical background and gravitational normalization before observational use; it is not by itself a measured discrepancy.

## Health and interpretation boundary

The original active vacuum witness retains D=9/2 and A_eff=1/6, giving A_eff/D=1/27. With an ordinary background, the exact relation is

    F_s Theta^2/(P^2 X) = A_eff + (rho_O+p_O)/(2X),
    Theta=P H_c-g v X.

Consequently the earlier vacuum-only F_s/G_s expression cannot simply be assigned to the new coupled matter system. A full finite-matter perturbation analysis is not claimed by the initial-data test.

The background is rapidly varying. Quasistatics needs c_s k_physical larger than the variation rates of all retained coefficients and the source frequency, while also remaining below a valid physical cutoff and within the linear-gradient regime. The prototype's physical cutoff band is unknown. The Gaussian solution is therefore a formal classical local kernel, not a demonstrated astrophysical profile. The exact homogeneous source-family calculation does not require that spatial hierarchy.

The result supplies a source-induced compensating response within the frozen derivative prototype. Its connection to the original RefG pressure variable, the selection of an admissible cosmological background, a controlled strong-field continuation and global singularity removal remain distinct physical tasks. The full RefG theory is neither replaced nor rejected by this calculation.

## Reproduction and sources

The executed standalone calculation passed 61/61 checks with SymPy 1.13.3 and mpmath 1.3.0. All three finite source points were solved independently by a two-variable Newton method and a one-variable bisection after exact charge elimination. The largest final constraint residual was below 2.6e-75; the largest cross-method state difference was below 4.8e-63. These are numerical residuals and crosschecks, not interval-arithmetic certificates.

| Added ordinary density | Medium-density change | Total-density change | Compensated fraction |
|---:|---:|---:|---:|
| 0.000001 | -0.000000333327419965 | 0.000000666672580035 | 0.333327419965 |
| 0.00001 | -0.000003332742186715 | 0.000006667257813285 | 0.333274218671 |
| 0.0001 | -0.000033274408091058 | 0.000066725591908942 | 0.332744080911 |

The exact first-order compensation is 1/3 on this specified branch. The finite values converge to it while their quadratic correction has the independently derived positive sign. The value 1/3 is a property of this frozen prototype and preparation, not a universal RefG prediction.

Run from the repository root:

~~~powershell
python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_matter_medium_source_response.py"
~~~

Use --verbose for individual residuals. The program uses SymPy and mpmath, prints JSON, writes no files, and exits nonzero on a failed declared check. It needs no private article copy.

1. Deffayet, Pujolas, Sawicki and Vikman, *Imperfect Dark Energy from Kinetic Gravity Braiding*, JCAP 10 (2010) 026, [DOI](https://doi.org/10.1088/1475-7516/2010/10/026), [full text](https://arxiv.org/html/1008.0048v2), especially §§2–3. Sign conventions are converted explicitly above.
2. Kobayashi, Yamaguchi and Yokoyama, *Generalized G-inflation*, Prog. Theor. Phys. 126 (2011) 511–529, [DOI](https://doi.org/10.1143/PTP.126.511), [full text](https://arxiv.org/html/1105.5723v4), §4 for the vacuum constrained scalar/tensor action.
3. [W92 main diagnostic](medium_health_horizon_diagnostic.md), Stages 8–9, 25, 27–28; the polynomial and active state are unchanged. [W64 source code](../W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field.py) supplies the canonical scalar normalization and sextic potential.
4. [BMP–RefG source/boundary audit](BMP.md) motivates maintaining independent source, pressure, clock and spatial-metric equations. Its one-function exterior is not imposed on this cosmological calculation.

## Pressure-map decision: two different responses

### Frozen extension contract — 2026-09-11

CLAIM_ID: W92_ACTIVE_PRESSURE_MAP_V1. Determine whether the calculated
homogeneous compensation supplies the RefG pressure/scale feedback in the
same candidate. Keep the polynomial, coupling, ordinary action, source
family and quasistatic approximation above fixed. The allowed files are
this report, its existing verifier, the W92 index and idea.txt.

The minimum decision has three parts: distinguish homogeneous and spatial
responses; test the direct identification of medium energy density with
foundation pressure; identify the metric readout actually inherited.
Use exact source equations and independent elimination of the static
quadratic action. A positive pressure map must satisfy the declared
clock/volume/current relations as well as the source equations. A nonzero
residual rejects that identification in the tested domain. It does not
reject every possible constitutive completion.

The spatial domain is precisely the leading local quasistatic domain above,
with frozen coefficients, P>0, A_eff>0 and matched homogeneous solutions.
The homogeneous domain is the regular active state, its time derivatives
and the fixed-charge initial family. No observational data or new physical
scale is used. Physical cutoff, full coupled health, nonlinear collapse and
singularity resolution retain their existing status. Stop at the mapping
decision; neither a new action nor a collapse run is part of this extension.

### Spatial source sign from the unchanged action

Write B=B_mix and A=A_eff. Eliminating the scalar in the two spatial
constraints gives

    delta rho_phi,QS = -B Delta pi = [B^2/(2P A)] delta rho_O,
    G_eff/G_EH = C/A = 1+B^2/(2P A).

Independent elimination in the quadratic action gives

    L_QS,reduced = -P_eff (grad Psi)^2 - delta rho_O Psi,
    P_eff = P-B^2/(2C) = P A/C.

For positive P and A the additional scalar response is nonnegative,
strictly positive when B is nonzero. At the frozen active state it is
+3 delta rho_O, and the effective source in the metric constraint is
4 delta rho_O. Thus this candidate's leading spatial response enhances
attraction relative to the same bare Einstein coefficient P.

This differs from the -delta rho_O/3 homogeneous response because the
experiments fix different data and solve different constraints. The
homogeneous result compares whole initial slices at equal scale factor and
shift charge; the spatial result describes a local source perturbation
of one background. Both follow from the same action. Substituting the
homogeneous coefficient into the spatial field equation is inconsistent.
Changing K's polynomial coefficients while retaining this positive-A,
constant-P, minimally coupled quasistatic structure cannot reverse this
additional source sign. Nonlinear strong-field response is outside this
sign result. The factor four has no observational status without physical
normalization and an established scale window.

### Which RefG map is available

The independent metric potentials give, to first order,

    p_clock=1+Psi, p_rod=1+Phi_N, Phi_N=Psi,
    u_readout=-ln(p_clock)=-Psi+O(perturbation^2),
    c_coordinate/c_background=1+2Psi+O(perturbation^2).

These recover the declared linear common-scale readout. At this witness,
and with the already specified matching condition, pi=(3/2)u_readout
to the same quasistatic order. It is a solution-level perturbation
relation, not an identification of the absolute KGB field with RefG's
pressure variable.

The existing homogeneous RefG dictionary instead uses a specific
collective current and volume map:

    n_op/n_0 = p^3 (n_F/n_F0),  n_F/n_F0=P_F/P_F0=p^2,
    n_op/n_0=p^5,  p=A_op^(-3/5),  P_F/P_F0=A_op^(-6/5).

Here A_op is the operational FLRW scale, equal to the variable called a
in the KGB metric, if that geometry is used. It is not the foundation
scale a_F=A_op^(2/5). These are the premises of
[W75](../../Cosmology_and_LSS/Active_Participation_Resonance_Feedback/w3_75_dynamical_relaxation_response_contract.md),
sections "Conventions", "Observable map" and "One charge and the correct
density measure", and RefG_GE sections 2.2 and 3.3. W51's log-source
functional remains a conditional static closure, not a derivation of
these premises from the cubic scalar.

Even provisionally assigning n_op=-J on the active J<0 branch leaves
n_op, p and P_F unchanged across the fixed-a, fixed-J initial family.
The medium energy nevertheless changes by -epsilon/3. Along time
evolution the discrepancy is also exact at the vacuum witness:

    d(rho_phi/rho_phi,0)/dt = 4/3,
    d(P_F/P_F0)/dt = -6/5                 [inherited homogeneous map],
    difference = 38/15.

Consequently P_F/P_F0=rho_phi/rho_phi,0 fails this declared map. The KGB
Hilbert pressure is a third quantity, K-g v^2 phi_ddot=-13/3 at the
witness; neither it nor the shift charge acquires a foundation-pressure
interpretation merely by renaming it. A different constitutive function
would be additional physical information.

The W75 slowing theorem also has a positive-enthalpy premise. The active
KGB state has rho_phi+p_phi=-4/3 and H_c_dot=2/3. Even imposing its
homogeneous dictionary yields p_ddot=9/25-2/5=-1/25 initially, so the
absolute decrease rate of p initially grows. W75's theorem remains valid
in its own declared source class; it does not transfer to this state.

### Decision and reproduction

The linear metric readout matches. The direct energy-density pressure
identification fails, and the homogeneous one-third compensation supplies
no local gravitational weakening in the tested spatial branch. Therefore
this candidate is not promoted to a derived RefG self-regulation law.
The missing input is an action-level identification of the foundation
pressure and its source response; repeating the same dictionary cannot
supply it. Existing oscillon and Einstein-sector results are unchanged.

Run the separate bounded extension with:

~~~powershell
python -X utf8 -B "RefG/work 3/Strong_Field/W3-92_Covariant_Medium_Integration/verify_matter_medium_source_response.py" --pressure-map-only
~~~

The extension passed 29/29 exact checks and identification controls,
including an independent read-only rerun. The default command retains and
passes the original 61 source-response checks; the preceding reference and
source/boundary verifiers also retain 42/42 and 41/41 checks. Passed
identification controls certify the displayed failed-identification
residuals; they do not turn the rejected pressure map into an accepted law.
