# W3-75: Dynamical homogeneous relaxation and the resonance-response boundary

## Working frame

One question: what pressure-relaxation result follows from the retained
Einstein/current dynamics, without prescribing the W3-47 Hubble history or
using the unproved identification of a resonance amplitude with p?

The minimum result is a future-time relaxation theorem and an action-level
decision about direct oscillon/collective transfer. The new physical input
relative to W3-71's continuity-only criterion is the W3-54 Einstein equation,
including its positive-enthalpy source. This supplies the missing dynamical
bound on accumulated expansion. No new interaction, equation of state,
pressure floor, fitted rate, or oscillator profile is selected.

Allowed files are this contract and one no-write symbolic verifier in the
existing Active_Participation_Resonance_Feedback topic. Stop after the proof,
source/response audit, dependency checks, and negative controls. Intuitive
manuscripts, upstream results, version numbers, and publication records stay
unchanged.

## Claim contract

- **CLAIM_ID:** W3_75_DYNAMICAL_HOMOGENEOUS_RELAXATION_RESPONSE.
- **CLAIM:** On the normalized W3-62 homogeneous pressure/readout branch,
  the flat expanding W3-54 Einstein/current system with the regular positive
  source class specified below preserves positive material scale and
  foundation-pressure readout at every finite future proper time. Both
  readouts decrease with strictly decreasing absolute loss rates and tend
  to zero only at infinite proper time. The additive W3-54/W3-58 matter
  action supplies separate phase-current and energy balances, but no
  direct collective/ordinary exchange term at fixed metric.
- **TYPE:** EXACT_CONDITIONAL_DYNAMICAL_THEOREM_AND_ACTION_RESPONSE_AUDIT.
- **MODEL_VERSION:** W3-75-v1.0. Changing the measure map, source class,
  curvature, vacuum sign, action coupling, or acceptance criteria requires
  a new version before the corresponding checks.
- **ASSUMPTIONS:** One operational metric; natural units c0=1; conserved
  neutral collective phase current; the already-selected W3-62 normalized
  volume and pressure maps; spatial flatness and initial expansion; one
  constant Lambda>=0; rho_C(n)>0, rho_C'(n)>0 and C2 regularity for all
  0<n<=n_i. The retained fluid health domain is
  0<=n rho_C''/rho_C'<=1. Optional separately counted pressureless and
  radiation components have nonnegative reference densities and standard
  separate conservation. A constant offset in rho_C belongs to the one
  Lambda slot, not a second vacuum source.
- **DOMAIN:** Homogeneous, isotropic, connected post-Genesis future
  evolution beginning at regular finite n_i>0 and H_i>0. This is neither
  an inhomogeneous compact-object theorem nor an extension through a
  past Genesis boundary. Optional fluids are alternative effective
  descriptions of ordinary content, not additional copies of the
  microscopic ordinary scalar.
- **CONVENTIONS:** tau is operational proper time; dot=d/dtau;
  A is the operational FLRW scale; H=dot(A)/A; kappa=8 pi G>0;
  n is density per operational volume; n_F is density per foundation
  volume. P_F is the inherited foundation-pressure readout. Pi_C denotes
  thermodynamic Hilbert pressure and remains distinct from P_F.
  Reference ratios satisfy A_i=p_i=1 and n_i=n_0, P_Fi=P_0.
- **FREEDOM_LEDGER:** No new fitted parameter or function. rho_C is the
  inherited universal function retained as a class, not chosen to force
  a result. kappa, Lambda, n_0, P_0 and optional B,R are inherited
  couplings/reference state data. The squared pressure map and cubic
  measure are inherited conditional premises, not newly derived here.
- **DEPENDENCIES:** W3-47 for the prior conditional result; W3-54 for
  the action/current/Hilbert source; W3-58 for the ordinary scalar;
  W3-62 for density measures; W3-71 for the continuity-only endpoint
  criterion. Their exact contract hashes are listed below.
- **METHOD:** Vary the homogeneous phase actions, differentiate the
  Friedmann constraint using current conservation, prove signs and
  an integral comparison, then audit mixed derivatives and separate
  energy balances at fixed metric.
- **PASS_CONDITION:** All exact identities and dependency hashes agree;
  loss-rate derivatives have the proved signs in the declared domain;
  the positive finite-time bound and divergent endpoint-time comparison
  hold; the additive action has the stated independent currents and
  vanishing direct mixed response; all registered negative controls fail
  the same production identities. Physical transfer and microscopic
  pressure/amplitude identification remain separately open.
- **FAIL_CONDITION:** An identity, dependency, sign, comparison, or negative
  control fails, or an undeclared interaction/source is used.
- **FALSIFIER:** A regular solution in this exact source/map domain that
  reaches n=0 in finite future proper time or increases the absolute
  pressure-loss rate falsifies the theorem. A nonzero direct mixed
  derivative of the displayed additive action at fixed metric falsifies
  the direct-response audit. Curvature, negative Lambda, sources in the
  collective current, or different readout maps are outside this claim.
- **RESIDUAL:** Exact symbolic zero for current, density-map, Friedmann,
  loss-rate, polytropic benchmark and separate energy-balance identities.
- **ERROR_BOUND:** Zero algebraic error. No empirical or microscopic
  approximation error is estimated. No numerical evolution is used.
- **VALIDITY_HEALTH:** Positive energy and chemical potential are used
  explicitly. The inherited sound-speed interval is retained. The
  one-dimensional homogeneous initial-value problem is locally regular
  for n>0; the integral argument establishes its complete future time
  domain. This does not prove general spacetime geodesic completeness.
- **BRANCHES:** Lambda=0 and Lambda>0 are covered. Optional B=0 or R=0
  are retained. A contracting branch, curvature and negative Lambda are
  not included. Pure dust, radiation-like and stiff collective equations
  of state are algebraic witnesses within the fluid health interval.
- **OBSERVABLE_MAP:** p=(n/n_0)^(1/5), P_F/P_0=(n/n_0)^(2/5),
  nHat_F=p^2 and A=p^(-5/3), on the selected homogeneous branch.
- **FORWARD_MODEL / DATA_ROLE:** N/A: no observational claim, dataset,
  instrument, likelihood or parameter estimation enters.
- **IDENTIFIABILITY:** The theorem does not depend on c_lock. Independent
  normalized amplitude readouts p and p^2 leave the displayed action
  and theorem unchanged; selecting a physical resonance readout requires
  a constitutive measurement/action map.
- **BENCHMARK:** rho_C=M n^(1+w), M>0, Lambda=B=R=0,
  w in {0,1/3,1}; verify the exact solution below against the original
  continuity and Friedmann equations, not just the final scale identity.
- **CLOSURE_FLAGS:** Derived true flags concern variational current,
  normalized volume map, dynamic H bound, positive finite-time readouts,
  slowing absolute loss, infinite endpoint time, W3-47 overlap,
  separate additive-action balances, and negative controls. The flags
  microscopic_pressure_map_derived, resonance_amplitude_map_derived,
  direct_oscillon_collective_transfer_derived, singularity_resolution,
  observational_pass and intuitive_files_changed remain false.
- **CROSSCHECK:** Obtain Hdot both from Friedmann differentiation and
  the Hilbert enthalpy; obtain loss derivatives both by the time-chain
  rule and by differentiating D(n); obtain endpoint time both through
  the logarithmic comparison and exact polytropic solutions.
- **PROVENANCE:** This contract is fixed before the verifier is written
  and run. The verifier reports its own and this contract's hashes,
  dependency checks, exact residuals, and Python/SymPy versions to
  stdout, with no generated files.
- **FILES:** This contract and w3_75_dynamical_relaxation_response.py.

## 1. One charge and the correct density measure

For the same normalized comoving cell, W3-62 supplies

    n/n_0 = p^3 (n_F/n_F0),       n_F/n_F0 = p^2.

Thus n/n_0=p^5. It is the operational n that enters the covariant action.
The current variation gives

    d(A^3 n)/d tau = 0,          dot(n) = -3 H n,
    dot(p) = -(3/5) H p,         dot(P_F) = -(6/5) H P_F.

The exponents use the inherited pressure map. Replacing n/n_0 by p^2
would conflate two volume measures.

## 2. A dynamical Hubble bound

Write x=n/n_0 and the once-counted source as

    E(n) = rho_C(n) + B x + R x^(4/3),        B,R>=0,
    3 H(n)^2 = kappa E(n) + Lambda,          H(n)>0,
    Pi_C = n rho_C'(n) - rho_C(n).

The optional terms denote one dust component and one radiation component.
They are omitted when those contents are already included elsewhere.
Current conservation, or equivalently the Einstein enthalpy equation, gives

    dot(H) = -(kappa/2) n E'(n),
    n E'(n) = n rho_C'(n) + B x + (4/3) R x^(4/3) > 0.

Consequently 0<H<=H_i. This bound follows from dynamics; the W3-47
specific Hubble function and c_lock=p are not used.

For D_p=-dot(p)>0 and D_F=-dot(P_F)>0,

    dot(D_p) = (3/5) p [dot(H) - (3/5) H^2] < 0,
    dot(D_F) = (6/5) P_F [dot(H) - (6/5) H^2] < 0.

The density, material-scale readout, pressure readout and their absolute
loss rates therefore decrease. This is a dynamical homogeneous result;
a smaller fractional pressure does not by itself represent an energy
transfer from an ordinary oscillon to the collective field.

## 3. Positive finite-time scales and the future endpoint

Integrating the current with H<=H_i gives, for Delta tau>=0,

    n >= n_i exp(-3 H_i Delta tau),
    p >= p_i exp[-(3/5) H_i Delta tau],
    P_F >= P_Fi exp[-(6/5) H_i Delta tau] > 0.

More directly the exact separable initial-value problem has elapsed time

    Delta tau(n) = integral_n^n_i ds / [3 s H(s)]
                >= log(n_i/n)/(3 H_i).

H(s) is positive and regular on every compact subinterval of (0,n_i].
Hence every positive target density is reached in finite time, the
solution continues through every such state, and the zero-density
endpoint requires infinite time. The limiting density is zero: a
positive limiting density would keep H bounded away from zero and
would contradict dot(n)/n=-3H. The absolute loss rates tend to zero
because H remains bounded and p,P_F tend to zero.

This replaces W3-71's freely supplied expansion history by the W3-54
dynamical restriction on the stated homogeneous branch. It supplies no
claim about inhomogeneous collapse, a black-hole interior or past
singularities.

For the polytropic benchmarks, with u=1+(3/2)(1+w)H_i Delta tau,

    n/n_i = u^[-2/(1+w)],
    H/H_i = u^(-1),
    p/p_i = u^[-2/(5(1+w))],
    P_F/P_Fi = u^[-4/(5(1+w))],
    H_i^2 = kappa M n_i^(1+w)/3.

All three selected w values have u>0 for every future proper time.
Their pressure-loss powers reproduce the dust/radiation W3-47 overlap
and test the additional healthy stiff-fluid case. They are exact
benchmarks, not fitted cosmic histories.

## 4. What the ordinary oscillon contributes to this action

On a homogeneous patch of the same operational metric, the matter
Lagrangian density of the retained additive actions is

    L/A^3 = n dot(theta_C) - rho_C(n)
            + dot(chi)^2/2 + chi^2 dot(theta_O)^2/2 - V(chi),
    V(chi) = m^2 chi^2/2 - lambda chi^4/4 + g chi^6/6.

This homogeneous patch is used to audit the action's symmetry and energy
exchange, not to replace the localized W3-58 solution by a homogeneous
particle.

Independent phase shifts imply separate conserved currents. The
collective equation is the current above, while

    d[A^3 chi^2 dot(theta_O)]/d tau = 0,
    dot(theta_C) = rho_C'(n).

At fixed metric, the direct mixed derivatives with respect to n and
the ordinary amplitude or phase vanish. On the respective equations,

    dot(rho_C) + 3 H (rho_C+Pi_C) = 0,
    dot(rho_O) + 3 H (rho_O+Pi_O) = 0.

The sectors still interact gravitationally through their shared metric.
Separate phase conservation alone would not exclude every possible
interaction; the direct-response conclusion uses the explicit additive
action as well. No direct conversion-rate equation or c_lock readout
has thereby been produced.

In particular, P_F is not Pi_C. The permitted dust example has
Pi_C=0 while P_F>0. Adding P_F to the Einstein source would count an
unintroduced source, not derive the missing pressure interpretation.

## 5. Decision and the remaining physical input

The result is conditional on the existing pressure/measure dictionary
but requires neither an assumed Hubble history nor a resonance-amplitude
law. It derives homogeneous dynamical slowing and the infinite-time
zero boundary from the retained Einstein/current system.

The direct microscopic target remains one physical input: an
action-derived or independently specified ordinary-core/collective-medium
response law, including how its measurable resonance amplitude and
foundation-pressure readout are constructed. A local size conversion,
an assumed declining resonance amplitude, or a second imposed decay
coefficient does not determine that law.

Work ends after this decision. No new oscillator state, background
coupling or interaction is silently inserted.

## Dependency pins

Paths are relative to RefG/work 3.

| Dependency contract | SHA-256 |
|---|---|
| Cosmology_and_LSS/Active_Participation_Resonance_Feedback/w3_47_post_genesis_evolution_pressure_coupling_kernel_preregistration.md | 9b603b1df55edf994f1e528a6cc8e16b69c474dd4c1b3df815e2654a6c279d50 |
| Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md | 6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879 |
| Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_one_oscillon_coframe_localized_core_preregistration.md | ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db |
| Cosmology_and_LSS/CMB_Closure/w3_62_cmb_einstein_source_linear_closure_preregistration.md | b4068791b63e9a072a897e9aa85eae96c588b0d33533effb9664ffbd667ae810 |
| Strong_Field/W3-71_Horizon_Material_Scale_Separation/w3_71_horizon_material_scale_separation_preregistration.md | 1d3f74489f6cc52061253b6e1ea3d7f96e5d423f8b2afb88e79a44a38ae916c3 |

## Verification specification

The no-write verifier must check the proof identities above using SymPy.
Required negative controls perturb the volume exponent, current sign,
Friedmann-to-Raychaudhuri coefficient, loss-rate coefficient, polytropic
solution exponent, internal exchange balance, and an added n*chi^2
direct interaction. Each is evaluated by the corresponding production
identity; merely printing a false closure flag is not a test.

The analytic proof and its domain are the evidence for the infinite-time
statement. Symbolic comparisons verify its algebraic steps and exact
benchmarks; a finite sample is not a proof of the general EOS class.

## Standard mathematical references

The isentropic current/Hilbert-pressure construction is the restricted
one-potential fluid action used in
[J. D. Brown, Action functionals for relativistic perfect fluids (1993)](https://arxiv.org/abs/gr-qc/9304026).
The background equations and flat-fluid benchmark histories are standard
Einstein cosmology; see
[M. Trodden and S. M. Carroll, TASI Lectures, section 2.3](https://ned.ipac.caltech.edu/level5/Sept03/Trodden/Trodden2_3.html).
The RefG-specific content here is their use with the retained density/scale
map and the explicit scope separation from microscopic resonant transfer.
