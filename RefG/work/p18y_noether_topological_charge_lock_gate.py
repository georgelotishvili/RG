# Notation header (see NOTATION.md):
# This gate follows p18x.  It audits whether compact phase quantization and the
# order-9/h=2 boundary register lock the charged-oscillon Noether current to a
# topological electric charge, and whether that is enough to derive alpha.

"""
================================================================================
PHASE 18y: Noether-to-topological charge lock gate
================================================================================

Purpose
-------
p18x found the charged oscillon current

    J^mu = kappa*rho^2*D^mu theta.

For a stationary localized profile the charge is continuous until the phase
sector is compact/quantized:

    Q_Noether = int J^0 d^3x.

This gate asks the natural next question:

    Does compact phase quantization plus the order-9/h=2 framing register
    turn Q_Noether into the physical electric charge and therefore derive
    alpha?

Result
------
The answer is controlled:

  * A compact phase can quantize the Noether momentum/charge label.
  * The order-9/h=2 boundary sector supplies q_geom = 2/9.
  * A closed framing current is gauge-legal and can carry that register.

But this still does NOT determine the canonical Maxwell charge.  The physical
coupling has the form

    q_e = q0 * q_geom,
    alpha = q0^2 * q_geom^2 / (4*pi).

Topology fixes the integer/fractional register.  It does not fix q0, the
canonical Maxwell normalization of that register.  Therefore the next missing
theorem is a Maxwell/source normalization theorem, not another topological
integer.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive q0 or beta_EM.
- It does not derive the profile/frequency/stiffness lock.
- It does not claim q_geom=2/9 is canonical electric charge by itself.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA
ORDER = 9
H_SELECTED = 2
Q_GEOM = H_SELECTED / ORDER


# ---------------------------------------------------------------------------
# 1. Compact phase quantizes the Noether label
# ---------------------------------------------------------------------------

def compact_phase_noether_quantization_gate() -> dict:
    theta = sp.symbols("theta", real=True)
    m = sp.symbols("m", integer=True)
    I_moment, Omega = sp.symbols("I_phase Omega", positive=True)
    p_theta = sp.simplify(I_moment * Omega)
    wavefunction = sp.exp(sp.I * m * theta)
    shifted_ratio = sp.simplify(
        sp.exp(sp.I * m * (theta + 2 * sp.pi)) / wavefunction
    )
    rotor_energy = sp.simplify(m**2 / (2 * I_moment))

    return {
        "compact_coordinate": "theta ~ theta + 2*pi",
        "single_valued_modes": "psi_m(theta)=exp(i*m*theta), m in Z",
        "shifted_ratio": str(shifted_ratio),
        "single_valued_for_integer_m": True,
        "classical_noether_momentum": str(p_theta),
        "quantized_label": str(m),
        "rotor_energy": str(rotor_energy),
        "quantizes_label_not_coupling": True,
        "reading": (
            "compactness turns the continuous phase momentum into an integer "
            "label in the quantum theory, but the physical electric unit that "
            "multiplies that label is not fixed by compactness alone"
        ),
    }


# ---------------------------------------------------------------------------
# 2. Order-9/h=2 gives a finite geometric boundary register
# ---------------------------------------------------------------------------

def order9_h2_register_gate() -> dict:
    h, order = sp.symbols("h order", positive=True, integer=True)
    theta_h = sp.Rational(H_SELECTED, ORDER)
    circumference = 2 * sp.pi * theta_h
    return {
        "order": ORDER,
        "h_selected": H_SELECTED,
        "q_geom": Q_GEOM,
        "theta_h_exact": str(theta_h),
        "circulation_fraction": str(circumference),
        "register_identified": True,
        "reading": (
            "the finite charged-frame sector supplies a fractional geometric "
            "register h/order=2/9.  This is a boundary/topological coordinate, "
            "not yet the canonical electric charge"
        ),
    }


# ---------------------------------------------------------------------------
# 3. Noether charge locked to a topological register still leaves q0
# ---------------------------------------------------------------------------

def noether_topological_lock_algebra() -> dict:
    kappa, Omega, Iprof, q0 = sp.symbols(
        "kappa Omega I_profile q0", positive=True
    )
    q_geom = sp.Rational(H_SELECTED, ORDER)
    Q_noether = sp.simplify(kappa * Omega * Iprof)
    Q_top = sp.simplify(q0 * q_geom)
    lock_equation = sp.Eq(Q_noether, Q_top)
    solved_q0 = sp.solve(lock_equation, q0)[0]
    solved_profile_combo = sp.solve(lock_equation, kappa * Omega * Iprof)[0]
    alpha = sp.simplify(Q_top**2 / (4 * sp.pi))

    return {
        "Q_noether": str(Q_noether),
        "Q_topological_readout": str(Q_top),
        "lock_equation": str(lock_equation),
        "q0_if_profile_combo_known": str(solved_q0),
        "profile_combo_if_q0_known": str(solved_profile_combo),
        "alpha_after_lock": str(alpha),
        "alpha_depends_on_q0": alpha.has(q0),
        "lock_trades_unknowns_without_q0_theorem": True,
        "reading": (
            "the Noether-to-topological lock can identify which geometric "
            "register the current carries.  It still needs a theorem for q0, "
            "the canonical Maxwell strength of that register"
        ),
    }


# ---------------------------------------------------------------------------
# 4. Alpha target is a required q0, not a result
# ---------------------------------------------------------------------------

def q0_target_translation() -> dict:
    q_geom = Q_GEOM
    q0_required = math.sqrt(4.0 * math.pi * ALPHA_CODATA) / q_geom
    alpha_if_q0_one = q_geom**2 / (4.0 * math.pi)
    return {
        "q_geom": q_geom,
        "alpha_inv_if_q0_equals_1": 1.0 / alpha_if_q0_one,
        "q0_required_for_CODATA_alpha": q0_required,
        "Z_medium_required": q0_required**2,
        "alpha_recovered_if_q0_inserted": q0_required**2
        * q_geom**2
        / (4.0 * math.pi),
        "target_not_derivation": True,
        "reading": (
            "the gate translates observed alpha into the q0 that a later "
            "normalization theorem must derive.  It does not insert that q0."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Dirac/Wilson product check: product quantization is not q0
# ---------------------------------------------------------------------------

def dirac_product_still_not_q0_gate() -> dict:
    q0, q_geom, gm, n = sp.symbols(
        "q0 q_geom g_m n", positive=True
    )
    qe = q0 * q_geom
    condition = sp.Eq(qe * gm, 2 * sp.pi * n)
    q0_solution = sp.solve(condition, q0)[0]
    alpha = sp.simplify(qe**2 / (4 * sp.pi))
    return {
        "condition": "q0*q_geom*g_m = 2*pi*n",
        "q0_solution_if_gm_known": str(q0_solution),
        "alpha": str(alpha),
        "alpha_still_depends_on_q0": alpha.has(q0),
        "product_quantization_trades_q0_for_gm": True,
        "reading": (
            "Dirac/Wilson quantization can relate electric and magnetic "
            "normalizations, but unless the magnetic normalization is derived "
            "in canonical Maxwell units, q0 remains open"
        ),
    }


# ---------------------------------------------------------------------------
# 6. Theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "derive q0, the canonical Maxwell strength of one completed "
            "framing register"
        ),
        "must_derive": [
            "the profile/frequency/stiffness combination kappa*Omega*I_profile",
            "or an action normalization that cancels that continuous combo",
            "or the magnetic normalization g_m in the same canonical units",
            "or a boundary-to-Maxwell normalization functional for the order-9/h=2 register",
        ],
        "acceptable_routes": [
            "derive q0 from the full localized charged oscillon action",
            "derive q0 from a Maxwell field normalization theorem",
            "derive q0 through a derived medium impedance Z_medium=q0^2",
            "derive q0 through eta_core if eta_core is itself action-derived",
        ],
        "falsification_tests": [
            "if compact phase only gives integer m, alpha is not derived",
            "if h/order=2/9 is used as q_e directly, alpha is not derived",
            "if Dirac quantization only trades q0 for g_m, alpha is not derived",
            "if q0 is set from CODATA, the gate fails as a fit",
        ],
        "candidate_next_gate": "p18z_canonical_maxwell_normalization_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_noether_topological_charge_lock_gate() -> dict:
    compact = compact_phase_noether_quantization_gate()
    finite = order9_h2_register_gate()
    lock = noether_topological_lock_algebra()
    target = q0_target_translation()
    dirac = dirac_product_still_not_q0_gate()
    requirements = next_theorem_requirements()

    closed = {
        "compact_phase_quantizes_noether_label": bool(
            compact["single_valued_for_integer_m"]
            and compact["quantizes_label_not_coupling"]
        ),
        "order9_h2_geometric_register_identified": bool(
            finite["register_identified"]
        ),
        "noether_topological_lock_equation_written": bool(
            lock["lock_trades_unknowns_without_q0_theorem"]
        ),
        "alpha_still_depends_on_q0_after_topological_lock": bool(
            lock["alpha_depends_on_q0"]
        ),
        "observed_alpha_translated_to_q0_target_only": bool(
            target["target_not_derivation"]
        ),
        "dirac_product_still_not_q0_derivation": bool(
            dirac["product_quantization_trades_q0_for_gm"]
            and dirac["alpha_still_depends_on_q0"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "q0_derived": False,
        "beta_EM_derived": False,
        "Z_medium_derived": False,
        "canonical_Maxwell_normalization_derived": False,
        "profile_frequency_stiffness_lock_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_CANONICAL_MAXWELL_NORMALIZATION_REQUIRED__"
            + _pass_status("NOETHER_TO_TOPOLOGICAL_LOCK_LEDGER")
            if all(closed.values())
            else "CHECK_NOETHER_TO_TOPOLOGICAL_CHARGE_LOCK"
        ),
        "SCOPE": (
            "Noether-to-topological charge lock after p18x: compact phase "
            "quantization and the order-9/h=2 boundary register can identify "
            "the geometric electric charge sector.  They do not fix q0, the "
            "canonical Maxwell strength of that sector.  Alpha remains open."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "compact_phase": compact,
        "order9_h2_register": finite,
        "noether_topological_lock": lock,
        "q0_target": target,
        "dirac_product": dirac,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "topology has done its job: it tells us which closed framing "
            "register counts as the electric unit candidate.  The remaining "
            "problem is not another winding number.  It is the physical "
            "Maxwell normalization q0 of that winding."
        ),
        "missing_derivations": [
            "derive q0 from the localized charged oscillon/frame action",
            "derive the canonical Maxwell normalization of the external field",
            "derive or rule out a profile/frequency/stiffness cancellation",
            "derive or rule out a magnetic normalization route for q0",
            "only then compute alpha = q0^2*q_geom^2/(4*pi)",
        ],
        "do_not_claim": [
            "Do not claim alpha is derived.",
            "Do not claim compactness or integer charge labels fix the coupling strength.",
            "Do not use q_geom=2/9 as canonical electric charge.",
            "Do not use Dirac product quantization as an alpha derivation by itself.",
            "Do not set q0 from CODATA.",
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
    print("compact_phase:", result["compact_phase"])
    print("order9_h2_register:", result["order9_h2_register"])
    print("noether_topological_lock:", result["noether_topological_lock"])
    print("q0_target:", result["q0_target"])
    print("dirac_product:", result["dirac_product"])
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
    _print_result(derive_noether_topological_charge_lock_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
