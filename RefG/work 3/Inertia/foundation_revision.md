# Foundation revision: one isolated action for geometry, inertia and light

2026-09-24. Research note and computational supplement.
MODEL_VERSION=`REFG_ISOLATED_COVARIANT_V2`.

## Decision and scope

The active **isolated, asymptotically flat low-energy sector** is the full
coframe TEGR/EH action with a canonical complex oscillon and Maxwell field.
The independent APR pressure scalar and the exact clock/ruler lock are
replaced in this sector. This is an explicit theory revision, not a correction
to the arithmetic of the old APR inertia calculation.

The aim is to remove the identified action-level inertia discrepancy while
retaining a self-consistent localized state, conserved energy and a common
causal metric. The sufficient result for this revision is an action-scoped
inertia law, source/geometry balance and a numerical radial energy-minimum
test for the reference state. Full cosmology and singularity resolution are
separate claims. No strong-field scan is part of this work.

The [covariant inertia derivation](../Lagrangian_Formulation/Oscillon_Inertia/oscillon_inertia.md)
and its [verifier](../Lagrangian_Formulation/Oscillon_Inertia/verify_oscillon_inertia.py)
provide the complete boosted shift and extrinsic-curvature terms in the
ADM surface charges. The additional calculations here connect
the released geometric response to the material stress, checks the
constrained energy first law and tests the complete finite-dimensional
radial constrained Hessian.

**Important change of foundation:** W54's collective-current action was
defined on n_C>0. Removing that independent current is the definition of
this new isolated sector. It has not been derived by setting J_C=0 in W54:
the normalized current J_C/(e n_C) is undefined there. A cosmological
completion must follow from a common action and demonstrate its isolated
limit; selecting different laws by the name of an object is not permitted.

## Frozen claims and verification contract

Contract fixed before execution of `verify_foundation_revision.py`.
The radial-Hessian implementation has its own recorded exploratory history
and frozen numerical criteria in `radial_stability_revision.md`.

| Field | Contract |
|---|---|
| CLAIM_ID | `REFG_REVISION_STRESS_DICTIONARY_V1`; `REFG_REVISION_ADM_FIRST_LAW_V1` |
| CLAIM | The same isolated action determines the unequal clock/ruler responses from its radial stress; its equilibria extremize ADM energy at fixed phase charge, with dM/dQ=Omega. |
| TYPE | Action-defined construction; exact conditional identities and numerical evidence, recorded separately. |
| MODEL_VERSION | REFG_ISOLATED_COVARIANT_V2; frozen action below, no fitted correction to inertia. |
| ASSUMPTIONS | Universal minimal metric coupling; regular neutral stationary spherical scalar; asymptotic flatness; F,N>0; localized tail; Lambda=0; Maxwell background zero. |
| DOMAIN | Exact identities on static regular spherical sector. Numerical witness alpha=.001, Q0=190.401136223484 and Q0(1 +/- .001,.002); no claim at arbitrary compactness. |
| CONVENTIONS | Signature -+++; c0=hbar=1; alpha=4 pi G; Psi=f exp(i theta)/sqrt(2); areal r; theta=Omega t; M=4 pi m(infinity). |
| FREEDOM_LEDGER | Potential coefficients fixed to W58; gravitational coupling .001 fixed reference value; Q selects object; lapse normalized at infinity; regular nodeless branch seeded at flat Omega=.8; independent lapse/spatial geometry allowed. No inertia fit, switches or new profile parameters. |
| DEPENDENCIES | Existing covariant action variation/ADM boost proof, reused with pinned solver and seed hashes. Current omission is a new sector definition, not inherited closure. |
| METHOD | Symbolic identities, two independent clock/ruler reconstructions, neighboring-charge BVPs, centered ADM derivative. |
| PASS_CONDITION | All symbolic residuals zero; pressure reconstruction max difference <3e-7; radius40/60 mass relative difference <1e-7 and central-product difference <2e-7; boundary residual <1e-8; max BVP residual <1e-6; central lock defect >1e-4; fine centered first-law relative error <1e-5 and coarse/fine derivative difference <2e-5. |
| FAIL_CONDITION | Any declared numerical gate fails, F<=0, nonlocalized field, failed BVP or source hash mismatch. |
| FALSIFIER | Nonzero exact variation residual, missing conserved source, or loss of common principal light cone invalidates the claimed construction. Negative constrained Hessian direction invalidates energy-minimum interpretation for that state. |
| RESIDUAL | Exact symbolic residuals and BVP/pressure residuals stored separately in JSON. |
| ERROR_BOUND | Floating-point estimates from domain and grid comparison, not interval-certified bounds; charge step refinement for first law. |
| VALIDITY_HEALTH | Canonical scalar and Maxwell kinetic signs in local frame; same metric principal cone; gravitational constraints retained. Numerical radial minimum has its own finite-domain status. |
| BRANCHES | One regular nodeless weakly gravitating branch; no all-branch uniqueness assertion. Exact common-p APR branch retained as historical independent model. |
| OBSERVABLE_MAP | Proper clock N dt, proper length A_iso dx; local c0; coordinate speed c0 N/A_iso; total ADM/Komar mass; leading monopole passive mass. |
| FORWARD_MODEL | N/A for exact mathematical tests; telescope, laboratory composition and cosmological likelihoods not tested. |
| DATA_ROLE | Synthetic calculations only; existing witness used for development, not independent observational prediction. Exploratory Hessian runs labeled as such. |
| IDENTIFIABILITY | This sector is the standard Einstein/canonical-scalar/Maxwell class in metric variables; no unique microscopic-medium inference follows. |
| BENCHMARK | Flat limit and Schwarzschild vacuum dictionary; same-Q old APR numbers are diagnostic, not a data fit. |
| CLOSURE_FLAGS | Separate exact dictionary, numerical source balance, first law, inherited ADM law, finite radial Hessian, microscopic derivation, cosmological completion and observational validation. |
| CROSSCHECK | Stress-integral reconstruction vs metric reconstruction; dM/dQ vs independently solved Omega; radial Hessian vs finite differences of constrained energy. |
| PROVENANCE | Date above; script/dependency hashes, library versions and output in foundation_revision_result.json. |
| FILES | This report; verify_foundation_revision.py and foundation_revision_result.json; radial_adm_hessian.py, radial_stability_revision.md and radial_stability_result.json; the linked covariant inertia derivation and verifier. |

Repository source identifiers used below:

- **W54:** [coframe/TEGR phase-source formulation](../Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md).
- **W58:** [canonical localized-core solver](../Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_one_oscillon_coframe_localized_core.py).
- **APR:** the earlier preferred-coordinate scalar pressure candidate,
  retained here only as a comparison; it is not a runtime dependency of
  the present calculations.

The publication edit changes source navigation and presentation only;
model equations, numerical thresholds and exploratory-selection history
are preserved. Source/contract hashes are regenerated from the exported files.

## 1. One action and its equations

In units c0=hbar=1:

    S_iso = integral sqrt(-g) [R/(16 pi G)
              - (grad f)^2/2 - f^2 (grad theta)^2/2 - V(f)
              - F_em,mu,nu F_em^mu,nu/4] d^4x + S_boundary,
    V(f) = f^2/2 - f^4/4 + f^6/24.

The TEGR coframe representation is equivalent to EH up to the prescribed
boundary term; use one representation once. The oscillon is a neutral
complex scalar with global phase charge, not an identified electron.
In Cartesian field components the action remains regular where f=0.
Maxwell is included explicitly; on the neutral reference state F_em=0.

Independent variations give

    G_mu,nu = 8 pi G (T_oscillon,mu,nu + T_EM,mu,nu),
    box f - f (grad theta)^2 - V'(f) = 0,
    div(f^2 grad theta) = 0,
    nabla_mu F_em^mu,nu = 0.

T_oscillon = df df + f^2 dtheta dtheta
             - g [(grad f)^2/2 + f^2(grad theta)^2/2 + V].
The scalar Noether current can be oriented as j^mu=-f^2 grad^mu theta,
giving positive charge for theta=Omega t. The total stress is conserved on
shell. There is no extra APR energy to add to the ADM charge. The geometric
binding contribution is already accounted for by the metric constraint.
Gravitational radiation and Maxwell radiation use the same metric null
cone; this is a statement of their principal parts, not of massive
oscillon group velocity equaling light speed.

These equations are a known Einstein-complex-scalar system, extended here
by neutral Maxwell propagation. Their adoption is a structural correction
of RefG's selected effective sector, not a new discovery of mass
equivalence. For the established self-gravitating soliton framework see
Liebling and Palenzuela, *Dynamical boson stars*,
https://doi.org/10.1007/s41114-023-00043-4 . The specific checks below are
performed on the project's fixed potential and charge.

## 2. Source, clock and ruler are solved together

Use ds^2=-sigma^2 F dt^2+dr^2/F+r^2 dOmega_2^2,
F=1-2 alpha m/r and N=sigma sqrt(F). Define

    T = Omega^2 f^2/(2 sigma^2 F), X = F f'^2/2,
    rho=T+X+V, p_r=T+X-V, p_t=T-X-V.

Independent field equations are

    m' = r^2 rho,
    (ln sigma)' = alpha r [f'^2+Omega^2 f^2/(sigma^2 F^2)],
    (sigma r^2 F f')' = sigma r^2 [V'-Omega^2 f/(sigma^2 F)],
    q' = Omega r^2 f^2/(sigma F), Q=4 pi q(infinity).

Regular center, decaying scalar, fixed Q and sigma(infinity)=1 close this
boundary-value problem. No prescribed pressure profile or hand-set
inertial mass enters its boundary conditions.

In isotropic radius x, r=A_iso x. The exact dictionary is

    d tau=N dt, d ell=A_iso |dx|,
    p_T=N, p_L=1/A_iso, c_coord=c0 p_T p_L.

For fixed local standards, coordinate length scales with p_L and clock
frequency with p_T. Redshifted rest energy scales with p_T. The small
coordinate-velocity kinetic coefficient of a test body is m A_iso^2/N;
it is not the invariant mass nor the total ADM mass.

The missing response is now explicit:

    (ln A_iso)' = (1-1/sqrt(F))/r,
    (ln N)' = alpha (m+r^3 p_r)/(r^2 F),
    (ln[N A_iso])' = alpha r p_r/F
                         + (1-sqrt(F))^2/(2 r F).                 (1)

Equation (1) follows from the two independent geometric equations. It
determines the departure from the APR lock N A_iso=1, with no added
adjustment function. In a vacuum exterior the first term vanishes, while
the second is positive for nonzero mass. Therefore imposing N A_iso=1
through a vacuum interval would exclude a nonzero Schwarzschild mass in
this action. A local counterterm cannot restore that lock while keeping
these same vacuum equations.

Schwarzschild vacuum in isotropic x has N=(1-z)/(1+z),
A_iso=(1+z)^2, z=GM/(2x), and N A_iso=1-z^2. The old common scale agrees
at leading weak vacuum order, not to all orders or through arbitrary
material interiors. Its exact exponential exterior belongs to its old
source action and is not silently reused here.

## 3. Inertia and mass bookkeeping

The existing ADM surface calculation for the complete boosted solution
gives E=gamma E0 and P=gamma E0 v/c0^2. Consequently

    M_inertial = (dP/dv)_(v=0) = E0/c0^2 = M_active,
    S_worldline = -M_inertial c0^2 integral d tau.

Universal metric coupling gives the same passive coefficient in the
leading adiabatic monopole approximation. Extended tidal response and
radiation reaction are higher-order, separately calculable effects.
Motion changes the full field, its phase and the time-space geometry;
keeping only a rigidly translated static deficit loses those terms.

The total energy of a moving isolated body increases as gamma E0;
its invariant mass remains E0/c0^2. Coordinate ruler shrinkage and
frequency redshift are distinct measurements and must not be called a
universal reduction of moving inertial mass.

## 4. Independent constrained-energy check

On momentarily stationary spherical data put P=q' and

    h=r^2 f'^2+P^2/(r^2 f^2),
    m'+(alpha h/r)m=r^2 V+h/2,
    M=4 pi m(infinity), Q=4 pi integral P dr.

This is the Hamiltonian constraint rewritten as a linear mass equation.
At equilibrium alpha h/r=(ln sigma)'. Its integrating factor gives

    delta M = 4 pi integral sigma [r^2 V' delta f + F delta h/2] dr,
    delta M/delta P = 4 pi sigma F P/(r^2 f^2)=4 pi Omega.

The f variation reproduces the radial scalar equation after integration
by parts. Thus delta M=Omega delta Q and the constrained first variation
vanishes. This ties the source, phase charge and total energy to the same
action. The numerical check varies Q, solves each equilibrium, and compares
the centered slope of M(Q) with Omega; it does not insert that slope into
the boundary-value problem.

## 5. Dependency ledger and physical cost

| Existing claim | Decision in this revision |
|---|---|
| APR M_I/E0-1=2.178224% | Correct result of its old action; that action is superseded for active isolated inertia. |
| Full coframe geometry and canonical W58 oscillon | Reused, with explicit action and normalization above. |
| W54 independent collective current | Omitted by new isolated-sector definition; vacuum reduction and cosmological completion remain unproved. |
| Local common metric and local light speed | Preserved and explicitly implemented with Maxwell. |
| Universal exact p_T=p_L and c_coord=c0 p^2 | Replaced by derived p_T,p_L and product law; historical special ansatz preserved. |
| E_t=N E_local and two clock factors in power | Local stationary redshift remains; spatial profiles and actual energy transfer require the chosen action. |
| Planck-scale or dimensionful pressure scaling | Not supplied by the new action; old exact-p scaling is not inherited. |
| Static APR restorative response and population law | Historical model results; the new equilibrium and Hessian supply their own evidence. |
| Article exact exterior, fitted cosmology, strong-field completion | Preserved in their original models; no automatic transfer to this sector. |
| Delayed self-gradient interpretation | Motivation for field inertia; no claim of a new microscopic derivation from foundation particles. |

The field energy and shared geometry provide a closed effective inertia
sector. Deriving that action from microscopic pressure degrees of freedom,
identifying real particle species and extending one action to cosmology
are different research targets. Choosing this sector resolves the known
inertia contradiction within it; it does not certify the full RefG program.

## 6. Results

The saved source/energy verifier passed 39/39 checks, including the Maxwell
principal symbol, gauge direction and two transverse polarizations. The reference body has
M_ADM=176.770354877229, Q=190.401136223484 and Omega=.796008838775070.
Its centre has p_T=.991825462269472, p_L=.993860321126289 and
c_coord/c0=.985735972432367. The exact common-scale lock defect is
1-N A_iso=.00204742941595. The stress-integral and direct metric
reconstructions agree within 1.34e-9 in ln(N A_iso).

Radius40/60 ADM masses differ by 4.04e-12 relative; the reference BVP
residual is below 2.99e-8. Centered dM/dQ differs from Omega by
3.75e-8 relative at the finer charge step, improving by approximately four
when that step is halved. No matching coefficient was fitted.

The complete finite-element fixed-charge radial forms are positive on
397/797/797 independent directions, for radii24/24/32 and
200/400/400 intervals. Their lowest reduced energy-curvature coefficients
are .38763345, .38762434 and .37709007. These are Hessian values, not
oscillation frequencies. Refinement at fixed radius changes the minimum
by 9.12e-6; the larger domain retains a wide positive margin. The
independent nonlinear-energy second difference agrees with the Hessian
to 3.31e-7 relative. This supplies resolved-space radial energy-stability
evidence for the localized body, beyond a static solution alone.

Authoritative output: `foundation_revision_result.json`; radial test:
`radial_stability_revision.md` and `radial_stability_result.json`.
The model-level inertia, source balance and shared-cone construction are
closed in the stated isolated sector. Continuum/nonradial/nonlinear
stability, a microscopic pressure derivation, a common cosmological
completion, observational validation and singularity removal are separate
unclosed claims. They are not inferred from the numerical pass count.

Reproduce from the project root:

```powershell
python -B "RefG/work 3/Inertia/verify_foundation_revision.py" --output "RefG/work 3/Inertia/foundation_revision_result.json"
python -B "RefG/work 3/Inertia/radial_adm_hessian.py"
```
