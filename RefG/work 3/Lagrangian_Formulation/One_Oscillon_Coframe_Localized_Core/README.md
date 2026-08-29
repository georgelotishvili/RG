# W3-58 Phase-Supported Q-Ball-Type Candidate Core

Claim ID: `W3_58_ONE_OSCILLON_COFRAME_LOCALIZED_CORE`.

W3-58 was opened as the one-oscillon localization stage. Its selected exact
`U(1)` action closes a phase-supported Q-ball-type ordinary core: a candidate
for the oscillon role, not a neutral real oscillon. One complex ordinary-phase
order parameter

```text
Psi_O=(chi/sqrt(2)) exp(i theta_O)
```

is coupled minimally to the same W3-54 coframe metric. Its selected core action is

```text
S_O=-(1/c0) integral d^4x e
    [1/2 g^mu_nu partial_mu chi partial_nu chi
     +1/2 chi^2 g^mu_nu partial_mu theta_O partial_nu theta_O
     +V(chi)],

V(chi)=m^2 chi^2/2-lambda chi^4/4+g chi^6/6.
```

The quadratic term fixes the vacuum mass scale, the attractive quartic binds the core, and the positive sextic stabilizes the large-amplitude sector. This is the lowest even polynomial that carries all three roles. The action has one exact ordinary-phase `U(1)` symmetry and belongs mathematically to the non-topological Q-ball class.

## Exact analytic result

With

```text
x=m r,
f=sqrt(lambda) chi/m,
Omega=omega/m,
a=g m^2/lambda^2,
```

the radial ground-state equation is

```text
f''+2 f'/x=(1-Omega^2)f-f^3+a f^5.
```

The zero-field state is the strict global vacuum for

```text
a>3/16,
```

and the complete harmonic finite-energy window is

```text
1-3/(16a)<Omega^2<1.
```

The same action yields the conserved ordinary-phase current and the Hilbert
tensor. The complete selected source ledger is `T_total=T_C+T_O`: the W3-54
collective source plus this new ordinary-core source, each entered exactly
once. After extracting the common physical factor `m^4/lambda`, define

```text
v(f)=f^2/2-f^4/4+a f^6/6.
```

The dimensionless local densities and stresses in a spherical orthonormal
frame are

```text
rho_tilde =  f'^2/2 + Omega^2 f^2/2 + v(f),
p_r_tilde =  f'^2/2 + Omega^2 f^2/2 - v(f),
p_t_tilde = -f'^2/2 + Omega^2 f^2/2 - v(f).
```

The integrated identity
`integral x^2 (p_r_tilde+2p_t_tilde) dx=0` is the stress form of the radial
virial theorem.

## Preregistered numerical ground state

The frozen benchmark is

```text
a=1/4,
Omega=4/5,
Omega_min=1/2.
```

Adaptive collocation produces one positive, nodeless, monotone finite-energy profile. The converged dimensionless readings are approximately

```text
f(0)             = 1.82021051,
mathcal_E         = 14.10656629,
q                 = 15.15164096,
x_Q               = 2.72894693,
mathcal_E/q       = 0.93102564,
dq/dOmega         = -132.36879.
```

Here `x_Q` is the charge-rms radius. Physical units follow from

```text
R_Q=x_Q/m,
E=(4 pi m/lambda) mathcal_E,
Q=(4 pi/lambda) q.
```

Here `Q` is the conserved ordinary-phase Noether charge. It is not identified
with electric charge.

The profile passes the registered domain, tolerance, quadrature, independent finite-difference, equation-residual, Yukawa-tail, Nehari, virial, and Hilbert-stress balance gates.

## Stability result

The action generates two fluctuation operators,

```text
L_+^(ell)=-d^2/dx^2+ell(ell+1)/x^2+1-Omega^2-3f^2+5a f^4,
L_-^(ell)=-d^2/dx^2+ell(ell+1)/x^2+1-Omega^2-f^2+a f^4.
```

The sensitivity solve uses the unreduced radial operator
`script_L_+ z=2 Omega f`. With the displayed reduced one-dimensional operator,
the identical statement is `L_+(x z)=2 Omega x f`.

The unconstrained `L_+` amplitude Hessian has exactly one negative radial
direction. The phase and translation symmetry modes converge to zero, and the
remaining registered gaps are positive. Positivity of the `ell=2` sector
extends to every `ell>=2` by the increasing centrifugal term. The charge
constraint, together with `dQ/dOmega<0` from the sensitivity equation and two
independent five-point branch derivatives, supplies converged numerical
orbital-stability evidence under the standard solitary-wave theorem. The
separate inequality `E/(mQ)<1` is the bound against decay into free quanta.
Both statements concern the selected nodeless fixed-coframe matter ground
state; coframe backreaction is outside this result.

## Result and boundary

The successful machine status is

```text
PASS_CONDITIONAL_EXACT_MINIMAL_COFRAME_U1_CORE_ACTION_AND_ANALYTIC_EXISTENCE_WINDOW__CONVERGED_NUMERICAL_FINITE_ENERGY_ORBITALLY_STABLE_SPHERICAL_GROUND_STATE_EVIDENCE__FOUNDATION_COEFFICIENT_SELECTION_BACKGROUND_LOCK_BACKREACTION_AND_PARTICLE_IDENTITY_OPEN
```

The result closes one selected, action-generated, phase-supported Q-ball-type
candidate core. The remaining physical bridge is sharply defined: the
foundation dynamics must select the core coefficients and connect this proper
core to the collective background response. That later bridge will decide the
environmental cadence and core--background scaling and the identification of
a physical particle.

## Run

```powershell
python w3_58_one_oscillon_coframe_localized_core.py
```

The package contains exactly the preregistration, solver/verifier, generated result, checksum, and this independent summary.
