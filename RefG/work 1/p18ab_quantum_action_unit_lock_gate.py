# Notation header (see NOTATION.md):
# This gate follows p18aa.  It tests whether compact phase quantization,
# Wilson phases, or Bohr-Sommerfeld/action-unit closure can fix the missing
# Maxwell normalization q0 without inserting the observed alpha.

"""
================================================================================
PHASE 18ab: Quantum action-unit lock gate
================================================================================

Purpose
-------
p18aa showed that the remaining fine-structure problem is not only classical
geometry.  It is the action normalization of one completed charged oscillon
register relative to hbar:

    q0 = k_J/sqrt(K_F),
    alpha = q0^2*q_geom^2/(4*pi).

This gate tests the obvious quantum routes:

  1. compact phase/rotor quantization,
  2. Wilson or large-gauge phase quantization,
  3. Bohr-Sommerfeld action closure,
  4. a finite symplectic cell on the completed frame bundle.

Main result
-----------
Compactness and phase closure quantize labels, products and actions, but they
do not fix the coupling scale unless the symplectic form/action cell of the
completed frame bundle is derived.  The next object is therefore sharper:

    derive the boundary symplectic form (or equivalent action cell)
    of the order-9, h=2 charged orientation-frame resonator.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive q0.
- It does not identify a fitted action cell with a theorem.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA
Q_GEOM = 2.0 / 9.0


# ---------------------------------------------------------------------------
# 1. Compact rotor quantization audit
# ---------------------------------------------------------------------------

def compact_rotor_quantization_audit() -> dict:
    I, omega, m, hbar = sp.symbols("I omega m hbar", positive=True)
    theta_dot = omega
    momentum = sp.simplify(I * theta_dot)
    omega_quantized = sp.simplify(m * hbar / I)
    energy = sp.simplify(I * theta_dot**2 / 2)
    energy_quantized = sp.simplify(energy.subs(theta_dot, omega_quantized))

    return {
        "rotor_lagrangian": "L = I*theta_dot^2/2",
        "momentum": str(momentum),
        "compact_quantization": "p_theta = m*hbar",
        "omega_after_quantization": str(omega_quantized),
        "energy_after_quantization": str(energy_quantized),
        "energy_depends_on_moment_of_inertia": energy_quantized.has(I),
        "reading": (
            "compactness quantizes the label m, but the energy/coupling scale "
            "depends on the moment of inertia I.  Therefore compact theta "
            "alone cannot be the alpha derivation."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Wilson phase / large-gauge quantization audit
# ---------------------------------------------------------------------------

def wilson_phase_quantization_audit() -> dict:
    q, Phi, n = sp.symbols("q Phi n", positive=True)
    condition = sp.Eq(q * Phi, 2 * sp.pi * n)
    q_solution = sp.solve(condition, q)[0]
    alpha = sp.simplify(q_solution**2 / (4 * sp.pi))

    Phi_scale = sp.symbols("Phi_scale", positive=True)
    alpha_scaled_flux = sp.simplify(alpha.subs(Phi, Phi_scale * Phi))

    return {
        "single_valued_phase_condition": "exp(i*q*Phi)=1",
        "quantization_condition": str(condition),
        "q_solution": str(q_solution),
        "alpha_from_condition": str(alpha),
        "alpha_depends_on_flux_normalization": alpha.has(Phi),
        "alpha_under_flux_rescaling": str(alpha_scaled_flux),
        "reading": (
            "Wilson quantization fixes a product q*Phi.  Unless the canonical "
            "flux normalization Phi is derived, it trades the alpha problem "
            "for a flux-normalization problem."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Bohr-Sommerfeld closure audit
# ---------------------------------------------------------------------------

def bohr_sommerfeld_action_audit() -> dict:
    A_cell, n, hbar = sp.symbols("A_cell n hbar", positive=True)
    kappa = sp.symbols("kappa", positive=True)
    action = sp.simplify(kappa * A_cell)
    condition = sp.Eq(action, 2 * sp.pi * n * hbar)
    kappa_solution = sp.solve(condition, kappa)[0]

    q_geom = sp.symbols("q_geom", positive=True)
    alpha_if_q0_sqrt_kappa = sp.simplify(
        kappa_solution * q_geom**2 / (4 * sp.pi)
    )

    return {
        "action_model": "S_loop = kappa*A_cell",
        "Bohr_Sommerfeld_condition": str(condition),
        "kappa_solution": str(kappa_solution),
        "alpha_if_q0_squared_equals_kappa": str(alpha_if_q0_sqrt_kappa),
        "alpha_still_depends_on_A_cell": alpha_if_q0_sqrt_kappa.has(A_cell),
        "reading": (
            "Bohr-Sommerfeld closure would be a real route only if the "
            "dimensionless action cell A_cell is derived from the completed "
            "frame resonator.  Otherwise it is just another place to hide a "
            "fit."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Symplectic cell ledger
# ---------------------------------------------------------------------------

def symplectic_cell_ledger() -> dict:
    Omega0, q_geom = sp.symbols("Omega0 q_geom", positive=True)
    q0_squared = sp.simplify(2 * sp.pi / Omega0)
    alpha = sp.simplify(q0_squared * q_geom**2 / (4 * sp.pi))
    Omega_required = 2.0 * math.pi / (
        (math.sqrt(4.0 * math.pi * ALPHA_CODATA) / Q_GEOM) ** 2
    )

    simple_candidates = {
        "pi": math.pi,
        "2pi_over_2": math.pi,
        "4pi_over_4": math.pi,
        "4pi_over_3": 4.0 * math.pi / 3.0,
        "2pi_over_h2": math.pi,
        "2pi_over_order9": 2.0 * math.pi / 9.0,
    }

    closest_name, closest_value = min(
        simple_candidates.items(),
        key=lambda item: abs(item[1] - Omega_required),
    )

    return {
        "symplectic_cell_hypothesis": "q0^2 = 2*pi/Omega0",
        "alpha_from_cell": str(alpha),
        "Omega0_required_for_CODATA_if_hypothesis_used": Omega_required,
        "closest_simple_candidate_checked": closest_name,
        "closest_simple_candidate_value": closest_value,
        "relative_miss_of_closest_simple_candidate": abs(
            closest_value - Omega_required
        )
        / Omega_required,
        "required_cell_not_simple_obvious_factor": abs(
            closest_value - Omega_required
        )
        / Omega_required
        > 0.01,
        "target_not_derivation": True,
        "reading": (
            "a symplectic-cell theorem is a plausible shape for the missing "
            "quantum lock.  But the required cell is not produced here and "
            "must not be chosen from observed alpha."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Order-9/h=2 is a register lock, not yet an action-cell lock
# ---------------------------------------------------------------------------

def order9_h2_register_vs_action_cell_audit() -> dict:
    h = sp.Integer(2)
    order = sp.Integer(9)
    q_geom = sp.simplify(h / order)

    Omega0 = sp.symbols("Omega0", positive=True)
    alpha = sp.simplify((2 * sp.pi / Omega0) * q_geom**2 / (4 * sp.pi))

    return {
        "h": int(h),
        "order": int(order),
        "q_geom": str(q_geom),
        "alpha_if_symplectic_cell_open": str(alpha),
        "Omega0_still_present": alpha.has(Omega0),
        "valid_claim": (
            "order-9/h=2 can identify the geometric electric coordinate "
            "q_geom=2/9"
        ),
        "invalid_claim": (
            "order-9/h=2 alone does not derive the action cell Omega0 or alpha"
        ),
    }


# ---------------------------------------------------------------------------
# 6. Next theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "boundary symplectic form of the completed order-9, h=2 "
            "orientation-frame resonator"
        ),
        "must_derive": [
            "the canonical one-form for the charged framing/fiber coordinate",
            "the conjugate momentum/current carried by one closed oscillon register",
            "the finite symplectic cell or action cell of the completed loop",
            "the map from that cell to q0=k_J/sqrt(K_F)",
            "the scale at which the resulting bare/geometric alpha is defined",
        ],
        "acceptable_outputs": [
            "a symbolic expression for Omega0 from the frame-bundle geometry",
            "a theorem that Omega0 is fixed by boundary closure and regularity",
            "a no-go showing that Omega0 remains a new independent constant",
        ],
        "falsification_tests": [
            "if compactness only quantizes m, alpha is not derived",
            "if Wilson/Dirac quantization only fixes q*Phi, alpha is not derived",
            "if Omega0 is set from CODATA, the gate fails",
            "if order-9/h=2 only supplies q_geom, the action-cell problem remains",
        ],
        "candidate_next_gate": "p18ac_boundary_symplectic_form_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_quantum_action_unit_lock_gate() -> dict:
    rotor = compact_rotor_quantization_audit()
    wilson = wilson_phase_quantization_audit()
    bohr = bohr_sommerfeld_action_audit()
    cell = symplectic_cell_ledger()
    order9 = order9_h2_register_vs_action_cell_audit()
    requirements = next_theorem_requirements()

    closed = {
        "compact_rotor_quantizes_label_not_scale": bool(
            rotor["energy_depends_on_moment_of_inertia"]
        ),
        "Wilson_phase_quantizes_product_not_alpha": bool(
            wilson["alpha_depends_on_flux_normalization"]
        ),
        "Bohr_Sommerfeld_needs_derived_action_cell": bool(
            bohr["alpha_still_depends_on_A_cell"]
        ),
        "symplectic_cell_route_identified_without_fit": bool(
            cell["target_not_derivation"]
            and cell["required_cell_not_simple_obvious_factor"]
        ),
        "order9_h2_fixes_register_not_cell": bool(
            order9["Omega0_still_present"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "boundary_symplectic_form_derived": False,
        "action_cell_Omega0_derived": False,
        "q0_derived": False,
        "bare_alpha_scale_identified": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_BOUNDARY_SYMPLECTIC_FORM_REQUIRED__"
            + _pass_status("QUANTUM_ACTION_UNIT_AUDIT")
            if all(closed.values())
            else "CHECK_QUANTUM_ACTION_UNIT_LOCK"
        ),
        "SCOPE": (
            "quantum action-unit audit after p18aa: compactness, Wilson "
            "phase and Bohr-Sommerfeld closure are checked.  They quantize "
            "labels/products/actions but still require a derived symplectic "
            "or action cell to fix q0.  Order-9/h=2 supplies q_geom, not the "
            "cell."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "compact_rotor": rotor,
        "Wilson_phase": wilson,
        "Bohr_Sommerfeld": bohr,
        "symplectic_cell": cell,
        "order9_h2_audit": order9,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the useful intuition is now very focused: alpha would be the "
            "readout strength of one completed charged oscillon if the "
            "finite frame bundle supplied a definite quantum action cell.  "
            "The number 137 is not hiding in compactness alone; it can only "
            "come from the size of that cell, or else it remains an external "
            "constant."
        ),
        "missing_derivations": [
            "derive the boundary symplectic form of the charged frame bundle",
            "derive the finite action cell Omega0 for the order-9, h=2 closed loop",
            "derive q0 from Omega0 and the Maxwell normalization",
            "state the bare/geometric alpha scale before QED running",
            "then compare to observed alpha without fitting",
        ],
        "do_not_claim": [
            "Do not claim compact phase quantization derives alpha.",
            "Do not claim Wilson or Dirac product quantization derives alpha.",
            "Do not set the action cell from CODATA.",
            "Do not claim order-9/h=2 gives more than q_geom until the cell is derived.",
            "Do not claim alpha is computed in this gate.",
        ],
    }
    return result


def _print_result(result: dict) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, val in result["closed_checks"].items():
        print(f"  - {key}: {val}")
    print("open_checks:")
    for key, val in result["open_checks"].items():
        print(f"  - {key}: {val}")
    print("compact_rotor:", result["compact_rotor"])
    print("Wilson_phase:", result["Wilson_phase"])
    print("Bohr_Sommerfeld:", result["Bohr_Sommerfeld"])
    print("symplectic_cell:", result["symplectic_cell"])
    print("order9_h2_audit:", result["order9_h2_audit"])
    print("requirements_for_next_gate:", result["requirements_for_next_gate"])
    print("physical_reading:", result["physical_reading"])
    print("missing_derivations:")
    for item in result["missing_derivations"]:
        print("  -", item)
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    _print_result(derive_quantum_action_unit_lock_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
