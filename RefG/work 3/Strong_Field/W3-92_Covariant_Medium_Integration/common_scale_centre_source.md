# Common-scale centre: source conditions and a local constitutive candidate

Joining update: section 6 rejects the unchanged candidate as a regular
isolated-object completion. The original local-centre identities remain
valid in their stated domain.

## Frozen scope

`CLAIM_ID: W3_92_COMMON_SCALE_CENTRE_SOURCE_V1`.
The independently varied W3-92 fields give a definite central source lock.
The unchanged static algebraic-response/canonical-scalar branch fails a
strict positive material-energy gate at its first radial continuation.
An explicitly new response plus the already-listed normalized clock-label
operator admits a regular pure-medium central germ with a positive
leading short-wave matter Hamiltonian.

Types: exact identities, restricted exclusion, explicit local construction,
and bounded numerical evidence. This is a source-first test, with no
prescribed Hayward interior and no change to the monographs or private
hypothesis folder.

Conventions: positive-TT `(-+++)`, standard Einstein tensor,
`c=hbar=1`, `P=M_Pl^2>0`, `Q=M_*^4>0`, `omega_H=1`.
This convention changes the whole original action consistently.
The common-scale coordinates are isotropic. Mechanical Hilbert pressures
are distinct from the foundation-pressure readout.

Dependencies: [W3-92 action](FORMAL_COVARIANT_MEDIUM_INTEGRATION.md),
[static action and health analysis, Stages 9, 10 and 26](medium_health_horizon_diagnostic.md),
and the W58 canonical complex-scalar potential used in the rejected
numerical example. No prior PASS supplies a new result.

Freedom ledger: the original fields and `P,Q`; a freely selected positive
central strain `b_c`; a finite central value `H_c`; and the explicit
new response coefficients below. No observations, optimization, density
fit, shell, transition function, or extra matter source are used.
These coefficients are a constitutive postulate, not a derivation from
the existing oscillon self-regulation mechanism.

Pass condition: zero exact source/variation residuals, the stated
restricted sign contradiction, positive displayed leading Hamiltonian,
and a converged finite radial continuation. Failure/falsifier: a nonzero
independent equation, wrong energy sign, or failed numerical bounds.
The calculation stops at this central test; a global solution has separate
closure fields.

## 1. The shared scale fixes the central source

Write
```text
ds^2 = -N^2 dt^2 + A^2 dr^2 + S^2 dOmega^2,
N = exp(-H), A = exp(H), S = r exp(H), Phi=t,
p_clock = p_rod = exp(-H), c_coordinate = exp(-2H).
```
The last speed is a coordinate ratio; locally measured light speed is one.

Direct connection/Ricci evaluation gives
```text
rho_geometry = -P exp(-2H) [2(H''+2H'/r)+H'^2],
p_r,geometry = -P exp(-2H) H'^2,
p_t,geometry = +P exp(-2H) H'^2.
```
The projected H action supplies precisely the displayed gradient density
and pressures. The algebraic medium plus ordinary source must consequently
have zero total spatial stress on this static branch.

At a regular centre `H=H_c+h_2 r^2+...`,
```text
rho_0 = -12 P exp(-2H_c) h_2, p_r0=p_t0=0,
K_0 = 240 exp(-4H_c) h_2^2.
```
A finite `h_2<0` gives positive central density and finite curvature.

Let `y=Yhat=1`, `Bhat=b I`, and let `F_b` denote the derivative
with respect to ONE eigenvalue. Then
```text
J = y F_y - 3b F_b,
rho_F = Q(2y F_y-F), p_F = Q(F-2b F_b),
rho_total,0 = 2QJ, p_total,0 = 0,

rho_O + p_O = -4Qb F_b.
```
This last equality is the central enthalpy/strain lock. The matter energy
and medium response cannot be varied independently. Also `H'(0)=0`
leaves a nonzero central Laplacian; setting `J=0` would remove this
positive-density common-scale centre.

## 2. The first continuation rejects the original strict static gate

Use regular expansions
`ell=a r+d r^3`, `chi=chi_0+chi_2 r^2`, `a>0`.
Here `ell` is the radial material-label profile, not a length constant.
With `f=F_i`, `A_F=F_ii`, `B_F=F_ij (i!=j)`, define
```text
L = f+2a^2 A_F, T = f+a^2(A_F-B_F).
```
The independently varied label equation and spatial Einstein anisotropy
require, at their first nontrivial orders,
```text
10d L + 4h_2 a f = 0,
4 exp(-2H_c) chi_2^2 - 8Q a d T = 0.
```
For the original invariant-only medium, positive label inertia requires
`f<0`; positive longitudinal/transverse spatial energies require
`L<0,T<0`. With `h_2<0`, the first equation requires `d>0`,
whereas the second requires `d<=0`. Thus changing only the response
Hessian cannot repair this strictly static, clock-aligned, common-scale
canonical-matter branch. Clock mixing does not remove the negative
pure-label direction of its unconstrained leading Hamiltonian.

The scope is a strict nondegenerate leading material-energy gate.
Degenerate constraints, other derivative operators, flow, other matter
stresses, and a full finite-wavelength metric-constraint analysis are
outside this exclusion.

Concrete rejected example:
`F=y-4I1`, `P=1,Q=7/48,H_c=0,a=1/2,chi_0=1`,
`V=chi^2/2-chi^4/4+chi^6/24, Omega^2=7/12`.
It has `rho_O=7/12,p_O=0,h_2=-7/72,chi_2=-1/18`.
The label equation gives `d=7/360`; anisotropy gives `d=-1/189`.
Higher Taylor orders cannot reconcile those two requirements.

For the old `F_min`, the matter-free equations `F=F_r=F_t=0`
at `y=1` have only `b_r=b_t=1`, where `F_y=0`.
Its earlier `y!=1` central samples do not satisfy this shared-scale test.

## 3. Explicit new local response, varied before the ansatz

In the positive-TT convention define
```text
Y=-g^(mu nu) Phi_mu Phi_nu, u_mu=-Phi_mu/sqrt(Y),
B^(AB)=g^(mu nu) phi^A_mu phi^B_nu,
gamma^(mu nu)=g^(mu nu)+u^mu u^nu,
y=exp(-2H)Y, Bhat=exp(2H)B.

S = integral sqrt(-g) [
    P R/2 + Q F + P gamma^(mu nu) H_mu H_nu
    + Q lambda exp(2H) sum_A (u^mu phi^A_mu)^2 ],

F=(y-1)+(3/4)(y-1)^2-Tr[(Bhat-b_c I)^2]/(64 b_c^2),
lambda=1/(4 b_c), b_c>0.
```
The added invariant is already among W3-92's candidate operators.
Its coefficient and this F are newly selected here. The ordinary scalar
source is absent in this witness.

For the static branch `phi^A=sqrt(b_c) x^A`,
`y=1,Bhat=b_c I,F=F_B=0,F_y=1,J=1`.
The added invariant and its first variation vanish on the background,
while its second variation supplies material-label inertia.

The independently varied radial action, with angular and time integrals
suppressed and the Einstein boundary term removed, is
```text
L = P[N A + (N S'^2 + 2N' S S')/A]
    + N A S^2 [Q Fbar + P H'^2/A^2].
```
All of `N,A,S,H,ell` are independent until AFTER variation.
`Fbar` counts two tangential eigenvalues.
On the branch the five Euler-Lagrange expressions reduce to
```text
E_N=-2r exp(H) E, E_H=-2r E, E_A=E_S=E_ell=0,
E=P r H''+2P H'+Q r exp(2H).
```
The stationary clock equation is also satisfied: its only surviving
background current is time-independent and temporal. Spherical static
symmetry gives vanishing off-diagonal equations.

The resulting sourced radial equation and regular germ are
```text
H''+2H'/r = -(Q/P) exp(2H),
H=H_c-Q exp(2H_c)r^2/(6P)
     +Q^2 exp(4H_c)r^4/(60P^2)
     -2Q^3 exp(6H_c)r^6/(945P^3)+O(r^8),
rho_total(0)=2Q, K(0)=20Q^2/(3P^2).
```
Away from the centre the projected-gradient energy also contributes:
`rho_total=2Q-P exp(-2H)H'^2`.
Thus `2Q` is the constant algebraic-source density, not the full
density everywhere.

## 4. Local principal check and bounded numerical test

At the centre let `theta` be a clock fluctuation and `xi` the normalized
longitudinal material displacement. Expansion of the invariants gives
```text
L2/Q = 4 theta_t^2 - 3 theta_z^2/4
       + xi_t^2/4 - xi_z^2/16 - xi_t theta_z/2.
Hamiltonian/Q = pi_theta^2/16 + (pi_xi+theta_z/2)^2
                + 3theta_z^2/4 + xi_z^2/16.
```
With momenta normalized by Q, this Hamiltonian is positive.
The characteristic polynomial is
`(8v^2-3)(8v^2-1)/64`: longitudinal/clock squared speeds are
`1/8,3/8`, and the transverse squared speed is `1/8`.
These are local leading short-wave speeds, all below local light speed.
The centre's H fluctuation is elliptic at this order. Full finite-k
metric constraints and stability away from the centre remain separate.

The numerical test fixes `x=r exp(H_c)sqrt(Q/P)`, `w=H-H_c`,
`x in [10^-5,0.5]`. It integrates
`w''+2w'/x=-exp(2w)` with the sixth-order central germ.
DOP853 tolerances `10^-9,2*10^-12` and maximum steps
`0.025,0.00625` are compared. Required solution difference:
`<2*10^-9`; independent quadrature flux residual:
`<2*10^-10`; fourth-order finite-difference ODE residual:
`<2*10^-8`. These are numerical consistency thresholds, not rigorous
interval bounds or an infinite-domain theorem.

Run result: at `x=0.5`, `w=-0.0406569435553`,
`p/p_c=1.04149475277` and `K P^2/Q^2=6.52843124903`.
The maximum solution difference is `1.43*10^-12`, independent flux
residual `6.67*10^-18`, and finite-difference residual below
`9*10^-13`. The rise of `p/p_c` is outward from the normalized centre;
there is no infinity-normalized exterior clock in this local test.

## 5. Local-stage decision and closure

The concrete progress is an explicit regular, common-scale, source-first
central medium solution and a precise reason the original canonical-matter
static join fails. The constitutive extension is retained as a local
comparison candidate.

This candidate remains on `J=1` with locked central strain.
It cannot acquire the old silent exterior merely by integration. Its
constant algebraic density and absent ordinary scalar leave the
oscillon self-regulation and exterior connection unestablished.
The added kinetic invariant alone leaves the canonical-source sign
contradiction intact when its positive central enthalpy forces `f<0`.

Section 6 performs the next same-action joining test. Its rejection
supersedes the earlier open joining status while preserving the local
identities. A chosen geometric interpolation would bypass the source
equations.

Closure fields:
```text
central_source_lock_verified = executable result
original_strict_static_material_gate_excluded = executable result
new_local_medium_germ_verified = executable result
local_leading_principal_gate_verified = executable result
ordinary_oscillon_join_derived = false
silent_exterior_joined = false
finite_wavelength_full_constraint_health = false
global_curvature_bound = false
regular_black_hole_derived = false
observational_validation = false
```
No observational channel or likelihood is used; data role, empirical
forward model and statistical identifiability are N/A for this local
theoretical test. It does not inherit observational validation from the
monograph. The benchmark is the explicitly rejected linear response.
Crosschecks: fresh Ricci evaluation, independent radial variation,
invariant expansion, negative controls, and quadrature versus ODE flux.
The verifier prints checks, numerical residuals, software versions and
SHA256 provenance, without creating results files.

Initial local-only run: 60/60 checks, Python 3.10.6, SymPy 1.13.3.
Verifier SHA256:
`4ad419c023e2444acc4a0bc32c542fdea9ed65e540d7f4f18d6f04869604007e`.
The pass count includes rejection and negative-control checks; it counts
this contract's checks, not sixty independent physical predictions.

Files: this report and
[verify_common_scale_centre_source.py](verify_common_scale_centre_source.py).

## 6. Joining audit: the local candidate fails isolated completion

**Status: REJECTED_AS_REGULAR_ISOLATED_COMPLETION.**
The local centre calculation in sections 1--4 remains valid. The
extension attempted here fails both its asymptotic-vacuum condition and
its retained radial principal-energy gate. This is a rejection of this
constitutive candidate for the declared completion, not a RefG no-go.

### Frozen joining contract

`CLAIM_ID: W3_92_COMMON_SCALE_CENTRE_JOIN_V1`.
Keep the section 3 action and central data unchanged. Test whether they
can reach a regular constant-H stress-free asymptotic state and retain
the declared principal-energy gate. Also test the minimal repair of a
smoothly fading algebraic response, keeping the common-p geometry,
EH operator and clock-aligned medium.

Domain: timelike clock, positive-definite normalized material strain,
finite positive P,Q,b_c, regular static centre. Relative label flow is
allowed in the asymptotic-vacuum test. The radial perturbation calculation
uses the regular high-frequency metric-ordering assumption of Stage 26;
full finite-wavelength gravitational constraints are a separate question.
The asymptotic test assumes derivatives of H vanish invariantly and
ordinary matter tends to vacuum; a cosmological, flowing or singular
boundary is a different problem.

Method: independent inverse-metric momentum variation; algebraic vacuum
conditions; exact radial principal action; continuation to its first
zero spatial-energy coefficient; source-uniqueness argument; and
asymptotic null-source/1PN expansion. Pass for a completion requires
all necessary gates. One demonstrated incompatibility rejects that
completion. Exact residual tests and checks that confirm a rejection
are separately reported from physical acceptance.

Numerical contract: DOP853 with the existing central germ, x starting
at 10^-5, terminal event eta=3/4, search ending at x=10 if no event;
tolerances 10^-9 and 2*10^-12, maximum steps 0.025 and 0.00625.
Required event-radius and common-domain state differences are below
2*10^-8; event residual below 2*10^-11. Pilot numbers locate this test;
they are not independent predictions. No data or observation is fitted.
Stop at the connection decision; do not evolve the failed branch as a
physical solution or add an unprescribed shell.

### A. The unchanged action has no regular stress-free vacuum

Normalize C=Bhat/b_c. In the clock rest frame write
v_A=exp(H)(u.partial phi^A)/sqrt(b_c), with spatial label matrix L.
Then C=L^T L-vv^T>0 and M=F_C=-(C-I)/32.
Inverse-metric variation gives
```text
T_0i/Q = -2 L_iA (M_AB-delta_AB/4) v_B.
```
L is invertible because L^T L=C+vv^T>0. Zero momentum stress requires
Cv=-7v, impossible for positive C unless v=0. Thus relative flow does
not supply a hidden asymptotic branch of this action.

With flow and H gradient zero, the metric and H equations require
```text
F=2y F_y, C F_C=(F/2) I, y F_y-Tr(C F_C)=0.
```
Taking the trace gives F=0, and hence F_y=F_C=0.
The only stationary point of the chosen polynomial is
y=1/3,C=I, where F=-1/3. These requirements contradict one another.
This failure is stronger than the already-known J=1 on the central
branch: changing its asymptotic clock rate or anisotropic strain also
fails. A separate polynomial with a zero stationary point is included
as a control, not adopted as another candidate.

### B. Actual radial continuation loses the retained energy gate

Let eta=(P/Q)exp(-2H)H'^2. Eliminating the projected H fluctuation at
leading radial order changes the local principal action to
```text
L2/Q=(4-eta)theta_t^2-(3/4-eta)theta_z^2
      +xi_t^2/4-xi_z^2/16-xi_t theta_z/2,

Hamiltonian/Q=pi_theta^2/[4(4-eta)]
 +(pi_xi+theta_z/2)^2+(3/4-eta)theta_z^2+xi_z^2/16.
```
The normalized mixed operator's background value is zero; derivatives
of its prefactor add no leading quadratic derivative term.
Strict positivity requires 0<=eta<3/4. For z=squared mode speed,
```text
64D(z)=(64-16eta)z^2+(20eta-32)z+3-4eta.
```
At eta=3/4 the squared speeds are 0 and 17/52. Immediately beyond,
their product is negative, so one radial squared speed is negative.
The central positive test therefore cannot be inherited by the full
radial solution. The event is a principal-gate failure, not curvature
blow-up or an observational claim.

The computed first event is `x=3.4363520119362554`,
`w=-0.9903851892807196`, `w'=-0.3216709258203599`.
The two integrations differ in event radius by `2.67*10^-15` and in
common-domain state by `7.60*10^-13`; these roundoff-level comparisons
are not a rigorous error enclosure. The physical radius is
`r=x exp(-H_c)sqrt(P/Q)`, with no astronomical scale calibrated here.

There is also an analytic reason this event must occur. Set t=ln x,
z=w+ln x, u=dz/dt. The unchanged radial equation gives
```text
z_tt+z_t=1-exp(2z),
E=u^2/2+exp(2z)/2-z, dE/dt=-u^2.
```
For any finite starting t, this energy confines z,u to a compact set.
Its zero-dissipation set u=0 has only the invariant point z=0.
Consequently z,u tend to zero and
eta=exp(-2z)(u-1)^2 tends to 1. Since eta starts at zero, it must cross
3/4 at a finite radius. This mathematical continuation has
S_areal tending to sqrt(P/Q), rather than an asymptotically flat end.
Its use here is to establish the inevitable stopping boundary.

### C. A zero ordinary scalar does not switch on outside

For the existing canonical W58 scalar,
```text
(r^2 chi')'=r^2[exp(2H)V_chi-Omega^2 exp(4H)chi].
```
The chosen centre has chi(0)=chi'(0)=0. The polynomial potential has
V_chi(0)=0 and is locally Lipschitz. The regular integral equation bounds
sup|chi| by (L_chi r^2/6)sup|chi| on a sufficiently small interval, forcing
chi=0. Ordinary ODE uniqueness continues that result at each regular
positive radius. Thus the zero scalar remains zero. A nonzero shell
requires new initial/boundary content or a different source equation;
it cannot be attached as an unnoticed part of this solution.
Here L_chi is a uniform local Lipschitz constant of the full radial
right-hand side, including its H- and frequency-dependent terms.

### D. Fading the response alone does not close the join

In the retained radial principal class define B=yF_y, C=-bF_b,
L=b lambda, and eta=(P/Q)(proper H gradient)^2. Necessary energy
coefficients satisfy
```text
S_clock=Q(B-eta-L), K_label=Q(C+L),
T_medium(null,null)=2(S_clock+K_label).
```
Changing the finite mixing coefficient leaves their sum fixed.
Positive coefficients require a positive radial null source; canonical
ordinary matter adds a nonnegative contribution. Explicit smooth H
dependence of an algebraic response does not alter this leading identity.

The exact common-p exponential exterior instead requires
T_geometry(null,null)=-2P m^2 exp(-2m/r)/r^4<0.
Even replacing that exact exterior with a smooth 1PN-compatible tail
does not fix this conflict within the same class. Assume the asymptotic
expansion and remainder estimates hold through two radial derivatives.
For real a,
```text
H=m/r+a/r^2+O(r^-3),
rho+p_r=-2P(m^2+2a)/r^4+O(r^-5),
g_tt=-1+2m/r-2(m^2-a)/r^2+O(r^-3),
beta=1-a/m^2, gamma=1.
```
These are the static spherical metric/PPN coefficients, not a new full
PPN calculation.
A nonnegative leading radial null source requires a<=-m^2/2,
or beta>=3/2. The beta=1 target retained by the existing RefG weak-field
branch is therefore incompatible with this positive-energy static
common-p/EH response class. This compares two mathematical requirements,
not a new fit to measured PPN data. The equality case needs subleading
analysis, which cannot restore beta=1.

**Decision:** retain the finite-centre construction as a local diagnostic,
remove it from the list of viable isolated-object completions, and stop
the unchanged-action integration. A next candidate must change the
derivative/constrained response or the stationary medium branch, and
pass its exterior, source and central gates together. The previously
tested cubic prototype in Stages 27--28 has its own failed connection
and supplies no automatic replacement. No extra response profile or
higher-order Taylor scan is justified by the current result.

Recorded combined run: **87/87 contract checks pass**. The joining
decision is **rejected**, as those checks verify the stated obstructions.
Python 3.10.6, SymPy 1.13.3; verifier SHA256:
`60257e3ec990e23d03d0c141fd86a40fa2fd42a5a0b54c1635c8494a84402241`.

## 7. Feedback and extra-assumption audit

`CLAIM_ID: W3_92_FEEDBACK_ASSUMPTION_AUDIT_V1`.
Scope: identify which reciprocal loops already exist and which extra
choices produced the failed centre. No new action, pressure law, collapse
run or monograph amendment is part of this audit. Existing successful
calculations retain their own domains; a shared name does not identify
different state variables or actions.

The intuitive premise is explicit in RefG_GE.md section 1.5, line 299:
oscillon response, medium response, equilibrium and perturbations must
come from the same action and energy balance. Sections 2.2 and 3.1 qualify
the static biconformal branch; line 390 describes the static p profile
as the volume-scalar projection of a full coframe with shape, shear,
orientation and temporal direction. No universal immobility or particular
polynomial F is selected by this premise.

### Existing loops and what they actually establish

| Existing calculation | Reciprocal loop already present | Boundary relevant here |
|---|---|---|
| Main diagnostic, Stage 8, lines 1649--1736; `--scale-feedback-only` | All rest contributions use the same p; E_matter=Bp and dE_matter/dB=p+B dp/dB. The entire pre-existing ensemble changes with the added load. | Restricted static functional, fixed-radius comparison. Its unmatched Einstein constraint prevents promotion to a complete object. Stage 9 identifies that constraint; the feedback algebra itself survives. |
| `nonlinear_equilibrium_evolution.py:114--149,236--240` | Each RHS recomputes geometry from current scalar/gradient/momentum; that geometry updates both matter equations. All four RK4 substages repeat the loop. The constrained Hamiltonian differentiates to the same equations. | Canonical Einstein--scalar action. This implements time-dependent reciprocal feedback, not the independent five-field foundation action. |
| `population_assembly_initial_data.py:229--248,281--295` | Constraint iterations update the source with the metric; outer iterations update all prepared core scales. | Default assembly is prepared initial data. Its local-dilation prescription is not a derived universal pressure law. |
| Same population file, `RegularGrid:1672--1709`, central-clock RHS `2145--2163` | Later modes really evolve matter, mass and geometry, including clock variables. | The file as a whole must not be labelled static. Its source remains the stated canonical scalar. |
| `matter_medium_source_response.md:26--84` and its verifier | An active derivative medium is forced through curvature by ordinary matter. Initial geometry and medium state are solved jointly; the coupled medium and ordinary-matter evolution equations and continuity are checked. | The fixed-charge homogeneous compensation is not the local spatial source law. Its pressure-map extension rejects direct identification with foundation pressure. |

The active derivative example gives homogeneous medium compensation
-delta rho_O/3 on a fixed-a, fixed-shift-charge initial family. Its
separate quasistatic spatial experiment gives +3 delta rho_O at the
registered witness. The existing pressure-map check distinguishes these
experiments and rejects P_F proportional to that medium energy under
the declared current/volume map. Neither result should be relabelled as
a derived universal RefG source law.

W88 additionally derives a genuine coupled phase/response energy and
its static elimination; its contract lines 70--106 and 124--143 also
state precisely why phase stiffness alone does not identify the
gravitational response. No new microscopic node calculation is needed
for this audit, and no such identification is assumed here.

### Extra choices in the failed centre

The new central construction used, together:

- the exact one-function isotropic metric N=exp(-H), A=exp(H);
- clock Phi=t and material labels phi^A=sqrt(b_c)x^A;
- the selected response polynomial and derivative truncation;
- no ordinary canonical scalar excitation.

These choices lock y=1, Bhat=b_c I, F_y=J=1 and rho_F=2Q. The clock/label
sector carries energy; calling it an oscillon population would require
an action-level identification that was not made. Thus the full
previously computed oscillon--geometry loop was not transferred into
this pure-medium central example. Its failure cannot serve as a test
of the full intuitive feedback principle.

Phi=t can itself be a coordinate gauge choice. The restriction here is
the complete metric/clock/label combination, not that gauge condition
in isolation.

### Direct test: adding time dependence alone does not release the lock

Keep that combination but replace H(r) by arbitrary H(t,x).
Direct evaluation of the defining invariants still gives
```text
Yhat=exp(-2H)(-g^00)=1,
Bhat=exp(2H) g^ij phi^A_i phi^B_j=b_c delta^AB,
J=1, rho_F=2Q.
```
The fixed-other-fields projected H block is still
exp(-2H)|grad H|^2. This does not compute the full gravitational kinetic
action or prove that arbitrary H(t,x) solves the equations. It proves
that removing only staticness does not make the selected algebraic
source track an oscillon state.

A second distinction is checked explicitly. At fixed independent metric,
minimal matter has no explicit H variation; after the metric pullback,
its variation is proportional to rho plus spatial stress trace.
For a minimally coupled rest constituent with constant m_0,
L=-m_0 N, N=exp(-H), this source is m_0 exp(-H).
Thus zero direct delta S_m/delta H never meant zero metric-mediated
backreaction. For this constituent, multiplying the rest mass by a
second p would double count the already present redshift; this is not
a prohibition of independently derived environmental mass terms.

### Audit decision

Retain the existing Einstein--scalar and all-constituent feedback results.
Keep the recent centre rejected as an isolated completion.
Do not treat the exact static exponential metric, fixed normalized
clock/strain, or the selected polynomial as universal consequences of
the intuitive premise. Also do not remove shared local measurement
relations or change the monograph by inference.

The concrete missing connection is the action-level map from the
retained nonzero matter state and full medium/coframe response to the
foundation-pressure readout and its Hilbert source. Existing scalar
energy, shift charge, static p, and the independent deficit H are not
interchangeable. A next candidate must specify this map and recover the
already tested weak and source limits; neither merely adding time
dependence nor another isolated polynomial centre supplies it.

### Reproduction and provenance boundary

The added `--feedback-assumptions-only` mode performs exact invariant,
projector, matter-pullback and all-constituent chain-rule checks.
Negative controls detect the frozen-old-ensemble derivative and doubled
redshift. It has no observed-data or numerical-collapse claims. Source
inspection, existing-code unit checks and these new identities are
distinct evidence types.

Read-only existing-code reruns:

- active source-response: 61/61;
- pressure-map extension: 29/29 (including rejected-map controls);
- nonlinear exact controls: 9/9;
- constrained Hamiltonian directional check: PASS; finest relative
  error 5.3433e-6 with successive error ratios about 1/4;
- population interior algebra controls: 11/11.

Three legacy CLI gates retain obsolete monograph hashes. Stage 8's
scale-feedback mode returned 58/59, its only failed item being the
Georgian monograph hash. The source-completeness and joint-focusing
modes returned DEPENDENCY_FAILURE before their calculation bodies.
Their article and evolution-code hashes still matched. These full
legacy runs are not reported as passing and their frozen hashes were
not overwritten. This is a provenance mismatch distinct from a
physical residual; the independently rerun tests above are unaffected.

The audit changes only this report, its verifier and the W92 index.
The evolution engines, both monographs, .gitignore and private
hypothesis folder are unchanged.

Audit run: 13/13 exact checks. The unchanged centre/joining mode retains
its separate 87-check contract. Verifier SHA256 for this extension:
`4ad8894c0d1010c92f7677d29546212cf4a415b51c7797d4835ad29d7423dfde`.

## 8. Matter-to-medium source balance from independent equations

### Bounded contract

`CLAIM_ID: W3_92_MATTER_MEDIUM_SOURCE_BRIDGE_V1`.
The task is to derive the necessary source balance connecting the retained
canonical oscillon to the independent W92 medium and test its ordinary
Einstein--scalar limit. The constitutive response is left unspecified; no new
constitutive law, centre profile or collapse trajectory is selected.

Model and assumptions: positive-TT conventions of this report, P,Q>0,
static spherical metric with independent N,A,S,H, material profile ell,
Phi=t, phi^A=ell(r) n^A, and psi=chi(r) exp(-i Omega t).
N,A,S>0 away from a regular centre. The scalar action is the existing
two-real-component canonical action, with
V=chi^2/2-chi^4/4+chi^6/24 in the numerical ordinary-source control.
These static equations describe a stationary stress tensor, not a
time-dependent collapse. Metric functions remain independent throughout
variation. The mixed clock-label operator vanishes with its first
variation on this aligned static background; its perturbations are not
discarded from a future health test.

Type, method and pass condition: exact independent Euler--Lagrange/Hilbert
identities, the radial conservation identity, and a fresh finite-radius
Einstein--scalar equilibrium charge comparison. Symbolic residuals must
vanish; deliberately omitted matter terms must fail. Numerical comparison
uses the existing W65 anchor and reports its collocation and quadrature
errors, rather than treating a floating-point equality as exact.
Exploratory existing-code runs assessed precision before adding the
regression: the independent residual limit is 100 times the requested
collocation tolerance, quadrature change is below that tolerance, and
the solver's reported residual is at most twice it. This is a numerical
consistency regression, not a prospectively frozen observational test.

Freedom ledger: only the existing P,Q, F, scalar potential and boundary
data; general response derivatives are kept symbolic. Dependencies:
W92 independent action, W64/W65 source equations and existing scalar
normalization. Data, fitting, observational forward model and model
uniqueness are N/A: this is a source consistency calculation. Falsifier:
an independent nonzero field/charge residual in the declared domain.
Changing F, deleting an equation, or assigning reconstructed stresses as
a constitutive law does not count as passing this contract.

Closure boundary: a verified source balance is not a healthy global
medium solution, a derivation of foundation pressure, or a regular black
hole. Those fields stay false. The stopping condition is the explicit
coupling equation, its independent checks and its consequence for the
next admissible source. Allowed changes: this report, its verifier and
one short W92 index entry; no monograph or private-hypothesis changes.

### Existing equations retained; a new source discriminator

The complete static radial action and its variations already appear in
the main diagnostic's Stage 9 and
`verify_medium_health_horizon_diagnostic.py:1564--1654`. They are retained,
not presented as a newly invented matter coupling. The present check
independently differentiates them to extract the lapse--deficit mismatch
equation, the radial Noether identity and a numerical charge control.

With the angular integral suppressed, write

```text
y=e^(-2H)/N^2, b_r=e^(2H)ell'^2/A^2, b_t=e^(2H)ell^2/S^2,
Fbar(y,b_r,b_t)=F(y,b_r,b_t,b_t),
J=y Fbar_y-b_r Fbar_r-b_t Fbar_t,
W=Omega^2 chi^2/N^2, X=chi'^2/A^2,

L=P[NA+(NS'^2+2N'SS')/A]
  +NAS^2[Q Fbar+P H'^2/A^2+W/2-X/2-V].
```

Fbar_t includes BOTH tangential eigenvalue derivatives. J is the H-source
combination, not the ordinary phase charge or a mechanical pressure.
The retained ordinary scalar satisfies

```text
(NS^2 chi'/A)' + NAS^2[Omega^2 chi/N^2-V_chi]=0,
Q_O=4pi integral Omega A S^2 chi^2/N dr.
```

The positive charge convention uses psi -> exp(-i alpha) psi for the
displayed exp(-i Omega t) phase. The existing evolution's opposite phase
orientation has the same positive charge magnitude after conversion.

Its active source is rho_O+p_rO+2p_tO=2(W-V). For the algebraic
medium it is 2Q(J+Fbar); the projected H contribution cancels in this
particular active-source sum. Each sector is counted once.

Define the two independently sourced fluxes and their difference:

```text
K=S^2 N'/A, Q_H=-NS^2 H'/A,
D=K-Q_H=(NS^2/A)(ln N+H)',
P K'=NAS^2[Q(J+Fbar)+W-V],
P Q_H'=Q NAS^2 J.
```

Their difference gives the required compatibility equation:

```text
P[(NS^2/A)(ln N+H)']'=NAS^2[Q Fbar+W-V].
```

This is an equation of the existing model, not an assigned response law.
It displays how matter reaches the deficit sector through the independent
metric and hence through y,b_r,b_t and J. Minimal matter still has zero
direct H variation at fixed metric. Those two statements are consistent.

For E_q=partial L/partial q-(partial L/partial q')', the verifier checks
the stronger off-shell identity

```text
N E_N-A E_A-S E_S-E_H
  =2{P D'-NAS^2[Q Fbar+W-V]}.
```

It also checks sum_q E_q q'-(A E_A)'=0 before any field equation is used.
This controls the radial constraint and prevents an early common-scale
substitution from silently removing an independent equation.

### What a common clock scale actually requires

Regularity gives D(0)=0. If N=e^(-H) is imposed throughout the object,
then necessarily

```text
Q Fbar+Omega^2 chi^2/N^2-V=0 at every radius.
```

If that equality of clock and deficit is required only on the outer
branch, the necessary condition is instead the weighted integral

```text
integral_0^outer NAS^2[Q Fbar+Omega^2 chi^2/N^2-V]dr=0.
```

For a localized smooth scalar with a tail, use the convergent asymptotic
limit with D_infinity=0; do not truncate chi and chi' to zero at a finite
matching radius. This requires matching the asymptotic lapse and deficit
charges, not just their constant normalizations. For N=exp(-m_N/r),
H=m_H/r, A=exp(m_A/r), S=r, both normalized fields tend to their vacuum
values but D_infinity=m_N-m_H. The verifier checks this counterexample
to inferring charge equality from field-value equality.
The pointwise or integrated equality is a necessary test, not a sufficient
solution of the spatial metric, scalar and material-label equations.
In particular, defining Fbar to equal the negative scalar expression
along a desired profile would be inverse assignment, not its derivation.

At a regular isotropic-coordinate centre, with
N=N_c(1+n_2 r^2+...), A=A_c+O(r^2), S=A_c r+O(r^3),
H=H_c+h_2 r^2+..., the independent equations give

```text
n_2+h_2=A_c^2[Q Fbar_c+W_c-V_c]/(6P).
```

This supplies an explicit residual test of a selected shared-scale
ansatz. Existing reciprocal Einstein--scalar dynamics retain their
previously verified feedback; the additional medium-source condition
must be checked separately.

### Independent retained-equilibrium charge control

With N_infinity=1, physical Komar mass is M_K=8pi P K. Its volume source
is 4pi NAS^2(rho+p_r+2p_t). The test freshly solves the existing W65
Einstein--sextic equilibrium, retaining its canonical source and all
of its metric backreaction. The independent W92 medium is absent in this
ordinary-source limit control; its equations are not claimed satisfied.

In W64 dimensionless units, alpha=0.04 and f(0)=1.820210505787701.
The areal metric is N_lapse=sigma sqrt(B), A=1/sqrt(B), S=x,
B=1-2alpha M/x. The comparison uses the spline metric derivative,
the original ODE derivative, the volume stress integral and
M_K,dim=2 Omega Q_dim-2 integral x^2 sigma V dx in these dimensionless,
suppressed-4pi units. Q_dim is the numerical charge, not physical Q_O.
No matter interaction or molecular model is added.

The integration interval is EPS=1e-5 to R, with sigma(R)=1 and the
existing Schwarzschild-corrected nonzero scalar-tail boundary condition.
The omitted regular-centre contribution is O(EPS^3), with a finite
source-dependent coefficient; it is not silently equated to zero.

| R, solver tolerance | Geometric M(R) | Komar volume | Relative difference |
|---|---:|---:|---:|
| 80, 1e-7 | 7.968956980534204 | 7.968956979281093 | 1.57e-10 |
| 80, 1e-8 | 7.968956978959599 | 7.968956978896625 | 7.90e-12 |
| 100, 1e-8 | 7.968956978996326 | 7.968956978924493 | 9.01e-12 |

Two quadrature grids, 16001 and 32001 points, differ by less than
9.2e-13 in the Komar volume integral. Tolerance refinement changes M by
1.57e-9; outer-radius enlargement changes it by 3.67e-11. The independent
local spline/ODE flux difference falls from 2.05e-7 to 1.08e-8 relative
to M, while the fine solver's maximum collocation residual is about
1e-8. These are numerical controls, not rigorous infinite-domain bounds.
The tiny integrated mass residual does not replace the larger local
solution-error diagnostic.

For the fine R=80 state, integrating only N rho_O over proper volume
gives matter Killing energy 7.250627837644094. The test deliberately
rejects equating this subtotal to the total gravitational mass. Its
difference from 7.968956978959599 does not indicate nonconservation:
the stationary Komar source includes the spatial stress trace, and the
total ADM Hamiltonian includes the gravitational constraint/boundary
structure. This is distinct from Stage 8's off-constraint energy error.

### Result and stopping point

`--matter-source-bridge-only` passes 40/40 checks: 19 exact/negative
controls and 21 retained-equilibrium controls. These are identity and
reference-limit checks, not 40 tests of a full medium solution.
The explicit new discriminator is the Q Fbar+W-V balance. An admissible
next response must produce it from the independent equations while
satisfying the remaining source and health conditions; reusing the
ordinary equilibrium alone or adding a time variable does not achieve
that. No new F, full pressure identification or singularity-removal
claim is introduced in this stage.

Reproduction: run `python -B verify_common_scale_centre_source.py
--matter-source-bridge-only` (one command) from this directory. Standard
output contains all checks, numerical rows and source hashes; no result
file is generated. Verifier SHA256 at this stage:
`0a864e0c681d58ef84beb5f03d12f531aa393023ccff5c3956dc1f805f263c51`.
The separate centre/joining and feedback-audit regressions retain 87/87
and 13/13 checks respectively. Legacy monograph-hash failures recorded
in section 7 are unchanged; they have not been silently repaired.
