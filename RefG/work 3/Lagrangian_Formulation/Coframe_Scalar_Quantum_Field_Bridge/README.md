# W3-61 Coframe Scalar Quantum-Field Bridge

Claim ID: `W3_61_COFRAME_SCALAR_QUANTUM_FIELD_BRIDGE`.

## Result

This package connects the existing RefG matter action directly to established
quantum field theory. The complex ordinary-phase action documented in
[One Oscillon Coframe Localized Core](../One_Oscillon_Coframe_Localized_Core/README.md)
(W3-58) has the exact free complex Klein--Gordon vacuum Hessian on the
operational geometry selected in the
[Relational Coframe TEGR Phase-Source Closure](../Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md)
(W3-54); equivalently, its quadratic vacuum action is the standard free
complex Klein--Gordon action. On the fixed Minkowski branch, standard
canonical quantization produces the complete free complex-scalar QFT:

```text
W3-58 complex coframe field
  -> exact vacuum Hessian
  -> complex Klein--Gordon equation
  -> canonical field/momentum pair
  -> bosonic CCR and positive-frequency Minkowski vacuum
  -> particle/antiparticle Fock sectors
  -> mass m, spin 0, global charges -1 and +1
  -> microcausal commutator and simple mass-shell pole.
```

The machine status is

```text
PASS_CONDITIONAL_EXACT_STANDARD_FREE_COMPLEX_SCALAR_QFT_LANDING_ON_SELECTED_FIXED_COFRAME__KLEIN_GORDON_CANONICAL_FOCK_MASS_SHELL_U1_CHARGE_SPIN_ZERO_AND_SCHRODINGER_LIMIT_CLOSED__FOUNDATION_ORIGIN_OF_HBAR_CCR_AND_VACUUM_CHOICE_PLUS_INTERACTING_RENORMALIZED_SPINOR_GAUGE_SOLITON_QUANTIZATION_AND_QUANTUM_BACKREACTION_OPEN
```

## Exact field bridge

With

```text
Psi_O=(chi/sqrt(2)) exp(i theta_O),
X=Psi_O^* Psi_O,
U(X)=m^2 X-lambda X^2+(4g/3)X^3,
```

the W3-58 action is exactly

```text
S_O=-integral d4x e
    [g^mu_nu partial_mu Psi_O^* partial_nu Psi_O+U(X)].
```

Its strict-vacuum quadratic sector is

```text
S_O^(2)=-integral d4x e
        [g^mu_nu partial_mu Psi_O^* partial_nu Psi_O
         +m^2 Psi_O^* Psi_O],

(Box_g-m^2)Psi_O=0.
```

The quartic and sextic terms retain their role as the interacting binding
sector. The free landing is an expansion about `Psi_O=0`; it does not take a
singular zero-coupling limit of the localized Q-ball profile.

The action itself supplies the canonical momenta, conserved symplectic form,
Klein--Gordon product, positive classical Hamiltonian, global current, and
Hilbert tensor. Canonical quantization supplies the operator promotion,
`hbar`, bosonic equal-time commutators, and the Minkowski positive-frequency
vacuum. Once that handoff is made, the mode algebra fixes

```text
:H:   = sum_k E_k (N_a+N_b),
:P:   = sum_k k (N_a+N_b),
:Q_O: = sum_k (N_b-N_a),
E_k^2 = k^2+m^2.
```

Thus the retained W3-58 sign convention is `Q_O=N_b-N_a`: `a^dagger`
creates charge `-1` and `b^dagger` creates charge `+1`. This is the global
ordinary-phase charge. A future local gauge bridge determines electric
charge.

The canonical equal-time algebra, together with the standard
Lorentz-covariant Pauli--Jordan theorem, makes the field commutator vanish at
spacelike separation. Because `Psi_O` is a Lorentz scalar, the standard Wigner
classification fixes spin zero. These are registered theorem handoffs from
established QFT, with their Lorentz-covariant and scalar-representation
premises verified.

The propagator is

```text
G_F(k)=i/(-k^2-m^2+i0),
```

with its pole at `k^2=-m^2`. In the spectral variable `s=-k^2`, it has unit
positive spectral weight at `s=m^2`. The one-particle Casimirs are
`P^2=-m^2` and `W^2=0`, so the free quanta are massive spin-zero bosons.
The nonrelativistic envelope
`Psi_O=exp(-imt) psi/sqrt(2m)` gives the Schrödinger equation at leading order,
with the exact suppressed second-time-derivative remainder displayed in the
result ledger.

## One geometry and one quadratic stress representation

Canonical quantization promotes the inherited free Hilbert tensor to an
operator. Normal ordering with respect to the fixed Minkowski vacuum supplies
the ordering and vacuum-subtraction prescription:

```text
:T_hat^{O,(2)}_mn:=:[partial_m Psi_O^* partial_n Psi_O
                     +partial_n Psi_O^* partial_m Psi_O
                     -g_mn(partial_r Psi_O^* partial^r Psi_O
                           +m^2 Psi_O^* Psi_O)]:.
```

Its `00` component equals the normal-ordered Hamiltonian density on the fixed
Minkowski branch. The free-vacuum O-sector has two alternative representations:

```text
classical representation: T_O^(2),
quantum representation:   :T_hat_O^(2):.
```

These are alternative representations of the same quadratic O-sector, so the
ledger selects exactly one of them. A quantum state contributes to a classical
Einstein equation through a specified renormalized state expectation such as
`<:T_hat_O^(2):>_ren`. The full nonlinear quantum stress additionally contains
the operators inherited from the quartic and sextic interactions. Their
renormalization and coframe backreaction define the later interacting bridge.

## Meaning and stopping boundary

The result is an exact landing on standard free spin-zero QFT under the
declared canonical quantization rule. It establishes that the same RefG
coframe which carries the Einstein--Hilbert geometry also carries standard
free quantum matter without changing geometry or duplicating energy.

The next physical bridge is sharply separated: derive `hbar`, the canonical
operator algebra, the Hilbert-space probability rule, and the vacuum choice
from the foundation dynamics; then quantize the W3-58 localized core or build
the spinor and gauge sectors. W3-61 stops before those tasks and opens no
automatic calculation chain.

W3-59 had conditionally reserved W3-60 for dynamical coframe backreaction
after a W3-59 pass. That condition failed, so the unopened number remains
untouched and this independent user-directed quantum-field branch is W3-61.

## Reproduction

From the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python '.\RefG\work 3\Lagrangian_Formulation\Coframe_Scalar_Quantum_Field_Bridge\w3_61_coframe_scalar_quantum_field_bridge.py'
```

The verifier checks pinned W3-54/W3-58 dependencies, the full contract schema,
the exact symbolic field and source identities, independent Hamiltonian and
charge crosschecks, structural mutations, deterministic JSON, and the result
checksum.
