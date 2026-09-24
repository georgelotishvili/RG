# Weak same-action fixed-charge radial ADM Hessian

## Contract and scope

CLAIM_ID: `REFG_WEAK_SAME_ACTION_FIXED_CHARGE_RADIAL_ADM_HESSIAN_V1`.
MODEL_VERSION: full universal-metric EH/TEGR plus canonical U(1) amplitude-phase
action, V(f)=f^2/2-f^4/4+f^6/24, alpha=.001, full Q=190.401136223484.
TYPE: numerical evidence for positive fixed-charge radial energy curvature.
The source, charge and equilibrium are those of the
[covariant inertia solver](../Lagrangian_Formulation/Oscillon_Inertia/verify_oscillon_inertia.py).
This is the weak self-consistent body used for the inertia revision.

The primary method tests every direction of a two-channel finite-element space
after eliminating the spherical metric constraint and imposing delta Q=0.
Positive curvature gives radial linear energy-stability evidence in these
resolved spaces. The spatial-phase and amplitude-momentum quadratic terms are
positive for F>0; the constant U(1) phase is a symmetry direction. This evidence
has finite resolution and finite outer radius. Continuum certification,
oscillation frequencies, nonradial modes and nonlinear stability remain outside
this calculation. No strong-field, collapse or horizon campaign is performed.

The initial method selection and thresholds used exploratory calculations of
this same body. This saved contract was frozen before the reproducible verifier
was executed. Its result is regression/validation of that calculation, with the
exploration history retained; it is not a prediction on untouched data.

ASSUMPTIONS / CONVENTIONS: c=1 and dimensionless scalar mass and quartic coupling
equal to one; alpha=4 pi G; spherical areal radius r; asymptotically unit lapse;
positive regular F; fixed total canonical U(1) charge; isolated localized body.
FREEDOM_LEDGER: potential and alpha are fixed universal inputs of the tested
version, Q selects the body, the old Omega=.8 profile is only a numerical seed,
and grids/radii below are numerical controls. Omega is solved by fixed Q.
DEPENDENCIES: existing W54 coframe/TEGR action and W58 potential/seed, and the
weak same-action static BVP. The W66 equations were inspected during method
selection; its old alpha=.04 stability status is not inherited.
DATA_ROLE / IDENTIFIABILITY / OBSERVABLE_MAP / FORWARD_MODEL: N/A, mathematical
action-based radial energy test; no observational likelihood or unique
microphysical claim is evaluated.

## Constraint reduction and second variation

Write ds^2=-sigma^2 F dt^2+F^-1 dr^2+r^2 dOmega^2,
F=1-2 alpha m/r, and P=q', with Q=4 pi integral P dr.
At equilibrium P=Omega r^2 f^2/(sigma F). For radial time-symmetric amplitude
data and vanishing spatial phase gradient, define

    h = r^2 f'^2 + P^2/(r^2 f^2)
    m' + (alpha h/r) m = r^2 V + h/2.

Thus alpha h/r=(ln sigma)' at equilibrium. Let eta=delta f, zeta=delta P.
The linearized constraint and ADM Hessian are

    delta m' + (alpha h/r) delta m = r^2 V' eta + F delta h/2
    D^2 M/(4 pi) = integral sigma [r^2 V'' eta^2 + F delta^2 h/2
                                    - 2 alpha delta h delta m/r] dr.

The total charge is linear in P; the fixed-charge second variation therefore
requires no extra second derivative of the constraint.

The remaining radial canonical channels admit an exact positive-form check.
In polar-areal slicing with zero shift, the angular spatial metric r^2 dOmega^2
is time independent. Thus K^theta_theta=K^phi_phi=0 and only K^r_r can be
nonzero. Pointwise K^2-K_ij K^ij=(K^r_r)^2-(K^r_r)^2=0. The spherical momentum
constraint determines K^r_r from the matter radial momentum density; it adds
no independent radial gravitational kinetic term to the Hamiltonian constraint.
Define the amplitude momentum Pi_f=r^2 dot f/(sigma F), alongside
P=r^2 f^2 dot theta/(sigma F). General radial matter data then have

    h = r^2 f'^2 + r^2 f^2 theta'^2 + Pi_f^2/r^2 + P^2/(r^2 f^2)
    m' + (alpha h/r) m = r^2 V + h/2.

At the equilibrium theta'=Pi_f=0. These two channels have zero first variation
of h, zero first-order delta m of their own, and zero mixed Hessian terms with
the (delta f,delta P) block. Their complete contribution is

    D^2 M_other/(4 pi) = integral sigma F [r^2 f^2 (delta theta')^2
                                          + (delta Pi_f)^2/r^2] dr.

It is positive for F>0 and sigma>0, modulo the constant U(1) phase symmetry.
Therefore the (delta f,delta P) calculation covers the potentially indefinite
radial canonical block after both spherical gravitational constraints are
accounted for. The numerical continuum limitations stated above still apply.

Use eta=a/r and zeta=r f b. Then

    delta h = 2[r f' a' - f' a
                + r f/(sigma F)(Omega b-Omega^2 a/(sigma F))]
    delta^2 h = 2(a'-a/r)^2 + 2 b^2 - 8 Omega a b/(sigma F)
                + 6 Omega^2 a^2/(sigma^2 F^2)
    delta Q/(4 pi) = integral r f b dr.

The quadratic form is the Hessian of the ADM energy on the spherical constraint
surface. Its reported eigenvalues use the norm integral a^2 dr after momentum
minimization. They are energy-curvature coefficients, not squared dynamical
oscillation frequencies.

## Discretization and frozen acceptance

Continuous piecewise-linear a,b vanish at r=0,R. Regular spherical data have
a,b=O(r) at the centre. These spaces approximate compactly supported physical
perturbations. Two Gauss points per uniform element evaluate the local form.
The nonlocal linearized mass uses its sigma integrating factor and an ordered
Volterra quadrature: full weights at preceding points plus half the current
weight. Refinement tests this approximation together with the finite elements.

Partition the assembled form as Haa, Hab, Hbb=B. For q_i=integral r f B_i dr,
all momentum directions are minimized analytically subject to q^T b=0:

    Hred = Haa - Hab B^-1 Hab^T
           + (Hab B^-1 q)(Hab B^-1 q)^T/(q^T B^-1 q).

The full charge-preserving momentum minimizer is checked as a matrix, so charge
projection covers every amplitude direction. The criterion consists of B>0
and Hred>0, checked by lowest generalized eigenvalues against the P1 L2 mass
matrix. The three runs are R=24 with 200 and 400 intervals (199 and 399 internal
modes per channel), and R=32 with 400 intervals. Their fixed-charge spaces have
397, 797 and 797 independent directions.

PASS_CONDITION, frozen after exploration and before saved verification:

- Each minimum B eigenvalue exceeds .9 and each minimum Hred eigenvalue exceeds
  .3; the R=24 refinement difference is below 3e-5 absolute.
- The larger R=32 domain retains the .3 positivity margin. Domain-dependent
  lowest eigenvalues are reported separately, not claimed converged to an
  isolated bound mode. The asymptotic Hred threshold is 1-Omega^2.
- Normalized full-map fixed-charge residual is below 1e-11 and matrix symmetry
  residual below 1e-10.
- A diagnostic negative-curvature mutation Hred -> Hred-Mass must produce a
  lowest eigenvalue below -.5. It is a validator control, not a physical action
  proposed for this body.
- Independent nonlinear-ADM second differences have finest relative error
  below 2e-6 and each halving of epsilon reduces that error by a factor below
  .3. The two quadrature-grid second variations agree within 1e-7 relative;
  stationarity is below 1e-7 absolute.
- The supplied BVP remains weak and regular (minimum F and lapse above .9),
  with charge quadrature within 2e-6 relative of the fixed charge and maximum
  normalized BVP spline residual below 1e-6.
- The weak-equilibrium source SHA-256 is pinned to
  `32cf32e9cfd590f93928eff16cbfe5494836df8b9d72bfd88b3cf3ba7da22076`.
  A mismatch stops execution before loading that source; the reuse API also
  enforces this pin. The BVP-residual and source-pin guards were added in the
  final mathematical/dependency audit, without changing the physical model.

FAIL_CONDITION: any required numerical check fails. FALSIFIER: a reliably
resolved negative physical fixed-charge radial direction invalidates the
positive-radial-curvature claim at this body. An unresolved or nonconverged
numerical calculation remains inconclusive for the continuum claim.

## Independent nonlinear-energy control

At fixed f_epsilon=f+epsilon eta, P_epsilon=P+epsilon zeta, directly solve the
nonlinear spherical constraint by its integrating factor:

    A'(r)=alpha h_epsilon/r
    m_epsilon(R)=integral exp[A(r)-A(R)] [r^2 V(f_epsilon)+h_epsilon/2] dr.

Use eta=exp(-r^2/4) and
b=r[exp(-r^2/9)-k exp(-r^2/16)], with k chosen to make integral r f b dr=0.
On 16001 and 32001 fixed quadrature points over [1e-6,40], compare analytic
D^2 m with centred differences at epsilon=.004,.002,.001. Fixed meshes avoid
the adaptive-IVP cancellation noise observed during exploration. This one
perturbation checks the Hessian formula independently; the separate full-matrix
test supplies the resolved-space positivity evidence.

## Reproduction and result ownership

Run `python radial_adm_hessian.py` inside this directory. It reuses the existing
weak-profile solver without invoking any old campaign, prints the result and
writes `radial_stability_result.json`. The combined foundation verifier can
reuse an already solved BVP via `verify_radial_stability(background)`.
The JSON is the numerical result record and includes each acceptance check,
source/contract hashes, resolutions, residuals, convergence differences and
explicit scope flags. Any altered model or numerical contract requires a new
verification and dependency review.
