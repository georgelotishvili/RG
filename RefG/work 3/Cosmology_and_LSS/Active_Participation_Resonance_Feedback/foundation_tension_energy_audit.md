# ფუძის დაჭიმულობა და საპასუხო ველის ენერგია

2026-09-19. ბოლო დროითი ანგარიშის ფიზიკური ინტერპრეტაციის შესწორება.

## დასკვნა და სამუშაოს საზღვარი

**ბოლო სკალარულ ანგარიშში H_u აღწერს მასშტაბური ველის რხევისა და
სივრცული ცვლილების ენერგიას. ფუძის ფონური დაჭიმულობის სრული
ენერგეტიკული მარაგი ამ სიდიდით გამოყვანილი არ არის.**
ამიტომ ფრაზა „მატერიას რაც აკლდება, ფუძეს ემატება“ ზედმეტად ფართოა.
ზუსტი სახელია: მოცემულ კანდიდატში მატერიისა და საპასუხო u-ველის
კანონიკური ენერგიების გაცვლა. ეს დაჭიმულობის მატებას არ აღნიშნავს.

მიღებულია სამი შემოწმება: ენერგიების გამიჯვნა; ძველი ფუძის მოქმედებიდან
წნევისა და ენერგიის სიმკვრივის კლების თანხვედრა ერთგვაროვან განშტოებაზე;
სკალარულ კანდიდატში ერთი პოტენციალის დამატების შესაძლებლობის ზუსტი
საზღვარი. სრული ახალი ფუძის კანონი ამ აუდიტით არ ინერგება.
ძლიერი ველი, ინტუიციური ტექსტი და ძველი მოქმედებები უცვლელია.

## Bounded contract, fixed before the saved verification

- CLAIM_ID / MODEL_VERSION: FOUNDATION_TENSION_ENERGY_AUDIT_V1; unchanged
  scalar-candidate action and separately retained W54/W75 current action.
- CLAIM / TYPE: exact energy-meaning and sign audit; scoped obstruction
  to a single derivative-free scalar potential preserving specified
  existing properties. No complete-theory rejection.
- ASSUMPTIONS / DOMAIN / CONVENTIONS: alpha>0, p=e^-u>0, w=p^-2,
  P_F=P_F0 p² with P_F0>0. The scalar and current-fluid branches below
  are kept separate. W75 requires its own n/n0=p⁵ map and rho_C'(n)>0.
  The potential test uses a differentiable W(u), unchanged kinetic
  terms/coupling, exact constant-background scaling and flat static vacuum.
- FREEDOM_LEDGER / DEPENDENCIES: no fitted or adopted new function.
  General W is tested as a possible minimal amendment; its nontrivial
  version is not installed. The exact-state witness is chosen solely to
  distinguish pressure decline from response-energy growth.
- METHOD: direct candidate energy/source identities; differentiation of
  the retained current-fluid map and fixed-charge first law; independent
  variation/scaling/virial tests for the possible W term.
- PASS_CONDITION: every registered symbolic residual vanishes; the
  explicit sign witness has falling P_F and increasing response energy;
  sign-flipped exchange and H_u=P_F negative controls are rejected.
- FAIL_CONDITION / FALSIFIER: nonzero residual invalidates that identity.
  A nonzero smooth W preserving all three registered properties would
  invalidate the restricted potential obstruction.
- RESIDUAL / ERROR_BOUND / VALIDITY_HEALTH: exact symbolic algebra,
  no approximation or new physical-fit claim; positive chemical
  potential belongs to the existing W75 class. No new stability theorem.
- BRANCHES / OBSERVABLE_MAP: scalar response H_u, operational P_F and
  current-fluid rho_C,Pi_C are explicitly distinguished below.
- FORWARD_MODEL / DATA_ROLE / IDENTIFIABILITY: no observations or data;
  neither a unique constitutive function nor empirical validation.
- BENCHMARK / CROSSCHECK: uniform static candidate with arbitrary p;
  admissible homogeneous initial data; W75 conserved-cell work law;
  potential scale condition independently recovered from mass/energy.
- CLOSURE_FLAGS: energy_meaning_audited, current_branch_sign_derived and
  restricted_potential_obstruction checked separately;
  full_stored_tension_law, full_RefG_closure and singularity_resolution=false.
- PROVENANCE / FILES: companion foundation_tension_energy_audit.py;
  sources and affected output/report labels below. Saved scripts print
  hashes/results and write no generated artifacts.
- STOP: correct the interpretation, verify regression and record the
  minimal-amendment decision. No equation sign is changed by preference.

## 1. What the existing files already distinguish

- [Intuitive §1.5](../../../../intuitive/RefG_GE.md) gives the schematic
  weak-static relation Delta P proportional to -rho_dyn. It separately
  discusses static source-locked response and propagating radiation.
- [W46](w3_46_active_participation_resonance_feedback_contract.md), Physical
  closure, distinguishes static-tension and coherent-dynamical bookkeeping.
  The interpretation is selected; its quantitative transfer law is open.
- [W47](w3_47_post_genesis_evolution_pressure_coupling_kernel_preregistration.md),
  Conserved-content and energy-role ledgers, writes E_total=E_L+E_N+E_R.
  E_N includes both dressing and coherent/tension background. The split
  does not define a separate U_tension(P_F), and P_F times a volume is
  explicitly not established as mechanical work energy.
- [W54](../../Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md),
  §5, varies the retained current action to obtain rho_C and
  Pi_C=n rho_C'-rho_C. It distinguishes Pi_C from the readout P_F.
- [W75](w3_75_dynamical_relaxation_response_contract.md), §§1,2,4, supplies
  the homogeneous density/readout relation and its energy balance.

The two meanings were therefore already separate in the source material.
The recent numerical output's broad label obscured that distinction.

## 2. The candidate can lower pressure while response energy grows

In the unchanged scalar candidate,

    P_F = P_F0/w,
    H_u = [w_t² + |grad w|²/w²]/(8 alpha),
    X = w_t (w |psi_t|² - V).

For any constant, spatially uniform w, H_u=0 while P_F may have any
positive value. H_u consequently cannot itself be a stored static
tension-energy function of P_F.

The unchanged field equations imply

    (P_F)_t = -P_F0 w_t/w²,
    partial_t H_u + div J_u = X,
    partial_t H_m + div J_m = -X.

An exact admissible homogeneous initial-state witness is

    w=1, w_t=1, psi=a+i b, a=1, b=0, a_t=0, b_t=1,
    V(1)=7/24,       j=1,       epsilon=1/(8 alpha)+19/24.

At that instant, with zero spatial flux,

    (P_F)_t/P_F0 = -1,
    (H_u)_t = 17/24,       (H_m)_t = -17/24.

Pressure and externally described matter-sector energy BOTH decline.
The increasing quantity is response kinetic energy. The witness checks
compatibility of these signs; it is not a relaxation trajectory or
evidence for a microscopic stored-tension conversion.

Flipping only one exchange sign would violate the same action's total
energy identity. Changing the action would require a separately tested
model, not an interpretation patch.

## 3. The retained foundation law already permits both declines

On the W75 homogeneous expanding current branch, the actual retained
energy density is rho_C(n), not the new scalar candidate's H_u. With

    n/n0=p⁵,    P_F/P_F0=p²,    mu_C=rho_C'(n)>0,

the exact chain rule gives

    d rho_C/dP_F = 5 n mu_C/(2 P_F) > 0.

Thus when P_F decreases on that branch, the local rest-energy density
rho_C decreases as well. This uses the already specified positive-
chemical-potential class; no new EOS is fitted or selected.

Density is distinguished from the energy of an entire changing volume.
For a homogeneous cell of fixed collective charge N=n V_proper,

    Pi_C=n rho_C'-rho_C,
    d(rho_C V_proper) = -Pi_C dV_proper.

This follows from the same current action and states its work balance.
The sign of the cell's total-energy change depends on Pi_C and volume.
P_F is not identified with Pi_C by changing a name.

This is a scoped consequence of the existing W75 law, not the missing
inhomogeneous coupling of that law to the scalar candidate. In particular,
W75 has V_proper proportional to p^-5 for its conserved cell; the scalar
candidate's fixed-coordinate homogeneous cell has V_proper proportional
to p^-3. Inserting n proportional to p⁵ for the same conserved N in the
latter would yield N proportional to p². Those reductions are not merged.

## 4. Why a single added potential cannot silently supply the missing energy

Test the smallest derivative-free amendment to the scalar candidate:

    L_new = L_old - W(u).

Its stored coordinate energy would be W(u); the u-source receives -W'(u).
Preserve the candidate's exact constant-background rescaling

    u_ext=U-ln s, t=T/s, x=s X.

The density/measure transformation requires

    W(U-ln s)=s^-2 W(U).

Differentiating at s=1 gives W'=2W, hence W=C exp(2u).
Since sqrt(-g)=exp(2u), this term is a CONSTANT covariant local energy
density C, not a derived variable tension density. In the same scalar
model a flat static vacuum u=0 requires W'(0)=0. Therefore C=0.

Subtracting W(0) from the coordinate energy leaves the force W'(0)=2C.
Subtracting a linear term can fix that force but changes the exact
constant-background scaling. Both are genuine modifications, not
zero-point relabelings that preserve all the old properties.

The mass check agrees independently. Let T, Vbar and G denote the
stationary ordinary kinetic, ordinary potential and combined gradient
integrals. On a localized stationary solution where the integrals and
boundary terms exist, the new dilation identity is

    G=3(T-Vbar-W_integrated),
    E_total=4T-2Vbar-2W_integrated,
    M_Gauss=4T-2Vbar-integral W',
    M_Gauss-E_total=integral(2W-W').

Thus W'=2W also preserves the old mass identity term by term.
This is a restricted obstruction to one extra potential with unchanged
scaling, vacuum and mass properties. It is not a rejection of general
medium actions, nonflat backgrounds or the RefG research programme.

## 5. Correction applied

The numerical output now calls the calculated quantity
energy_scale_response and its exchange energy_exchange_to_scale_response.
The old field names energy_foundation and energy_exchange_to_foundation
were presentation labels, not separate equations. The response script and
exact identity script explicitly state stored_background_tension_energy_derived=false.
The stationary-candidate and time-response reports carry the same distinction.
The minimum-closure map links this audit.

Equations, initial conditions, sign conventions, thresholds, total
Hamiltonian and computed trajectories are unchanged. The old conditional
no-zero and finite-time results remain scoped to that unchanged candidate.
They do not certify a stored-tension constitutive law.

## Verification

The saved exact audit passed 32/32 checks. Independent reruns of the
existing time-identity and finite-time scripts passed their unchanged
43 and 29 checks, respectively, plus the discrete-Hamiltonian audit.
All exited 0. Comparison with the saved pre-edit execution confirmed:

- identical complete baseline-subtracted time trace;
- identical refinement results;
- identical total energies and charges;
- identical response-energy numbers under their corrected field names.

The newly derived identities were independently checked before the
saved execution. No altered dynamics is presented as a successful
regression. Source SHA256 values after the label correction:

    foundation_tension_energy_audit.py
      20f070f7b2400c6e2f86252630628b41eab3a5cc375fffa88aca2c8cbf6c0d51
    common_scale_time_identities.py
      860a76a76e151bf8d6ba8e3e6a0a10d887adea88df33e983756eb47243e0ee8f
    common_scale_time_response.py
      c49f1163a1983ec8057eb51978959bfa49b12b3ec65e914f64f2966d3c785a3c

Run from the repository root:

    python -X utf8 -B "RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/foundation_tension_energy_audit.py"

The two time-response commands remain in their
[report](common_scale_time_response.md). All three verifiers write
results only to stdout.
