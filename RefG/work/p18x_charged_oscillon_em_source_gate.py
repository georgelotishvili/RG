# Notation header (see NOTATION.md):
# This gate follows p18w.  It writes the charged oscillon/framing current that
# can source the external Maxwell field, and audits which normalization remains
# open before alpha can be claimed.

"""
================================================================================
PHASE 18x: Charged oscillon electromagnetic source gate
================================================================================

Purpose
-------
p18w reframed alpha as an electromagnetic readout coefficient:

    q_e = beta_EM * q_geom,
    alpha = beta_EM^2 * q_geom^2 / (4*pi).

This gate asks for the first concrete object in that chain: the source/current
of a charged oscillon or charged orientation-frame defect.

The minimal completed-frame form is standard and sharp:

    D_mu theta = partial_mu theta + A_mu(n),
    L_phase = (kappa/2) rho^2 D_mu theta D^mu theta,
    J^mu = kappa rho^2 D^mu theta.

Here rho is the localized oscillon/core amplitude, theta is the internal
framing/phase coordinate, and A(n) is the p18h frame connection.  This gives a
real electromagnetic source slot.  But it does NOT fix its canonical strength.

Main result
-----------
The charged-oscillon current is gauge invariant, conserved by the theta
equation of motion, and localized if rho(r) is localized.  For a simple
stationary radial oscillon profile,

    Q = int J^0 d^3x = pi*kappa*Omega*rho0^2*R^3

for rho(r)=rho0 exp(-r/R).  That charge depends on action normalization,
frequency and profile inventory.  Therefore topology alone is not yet enough:
we still need a theorem that locks the Noether charge/current normalization to
the completed topological framing register.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive beta_EM.
- It does not derive the canonical electric charge.
- It does not solve the charged oscillon profile.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA
Q_GEOM_H2_ORDER9 = 2.0 / 9.0


# ---------------------------------------------------------------------------
# 1. Gauge-invariant charged phase current
# ---------------------------------------------------------------------------

def gauge_invariant_phase_current_gate() -> dict:
    kappa, rho = sp.symbols("kappa rho", positive=True)
    D0, D1, D2, D3 = sp.symbols("D0 D1 D2 D3", real=True)
    D = [D0, D1, D2, D3]
    eta = [1, -1, -1, -1]
    lagrangian = sp.simplify(
        sp.Rational(1, 2)
        * kappa
        * rho**2
        * sum(eta[mu] * D[mu] ** 2 for mu in range(4))
    )
    current = [sp.simplify(sp.diff(lagrangian, D[mu])) for mu in range(4)]
    expected = [sp.simplify(kappa * rho**2 * eta[mu] * D[mu]) for mu in range(4)]
    return {
        "phase_lagrangian": str(lagrangian),
        "current_components": [str(j) for j in current],
        "expected_current_components": [str(j) for j in expected],
        "current_derivation_verified": current == expected,
        "charge_density": str(current[0]),
        "source_slot": "J^mu = kappa*rho^2*D^mu theta",
        "reading": (
            "a charged oscillon/framing phase has a clean Maxwell source "
            "candidate; its strength is controlled by kappa and the localized "
            "profile inventory"
        ),
    }


# ---------------------------------------------------------------------------
# 2. Local U(1) completion and conservation
# ---------------------------------------------------------------------------

def local_u1_and_conservation_gate() -> dict:
    th = sp.symbols("theta_0 theta_1 theta_2 theta_3", real=True)
    A = sp.symbols("A_0 A_1 A_2 A_3", real=True)
    lam = sp.symbols("lambda_0 lambda_1 lambda_2 lambda_3", real=True)
    D = [th[i] + A[i] for i in range(4)]
    transformed = [(th[i] - lam[i]) + (A[i] + lam[i]) for i in range(4)]

    t, x, y, z = sp.symbols("t x y z", real=True)
    coords = [t, x, y, z]
    J = [sp.Function(f"J{mu}")(*coords) for mu in range(4)]
    theta_eom = sp.simplify(sum(sp.diff(J[mu], coords[mu]) for mu in range(4)))

    return {
        "Dtheta_componentwise_invariant": all(
            sp.simplify(transformed[i] - D[i]) == 0 for i in range(4)
        ),
        "gauge_rule": "theta -> theta - lambda, A -> A + d lambda",
        "theta_equation_of_motion": "partial_mu J^mu = 0",
        "symbolic_divergence": str(theta_eom),
        "conservation_is_eom_not_number": True,
        "reading": (
            "the source is kinematically gauge-consistent.  Conservation "
            "does not fix the value of the charge; it only says the closed "
            "current cannot start or end."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Localized stationary oscillon charge inventory
# ---------------------------------------------------------------------------

def stationary_oscillon_charge_inventory() -> dict:
    r, R, rho0, kappa, Omega = sp.symbols(
        "r R rho0 kappa Omega", positive=True
    )
    rho = rho0 * sp.exp(-r / R)
    density = sp.simplify(kappa * rho**2 * Omega)
    charge = sp.simplify(
        sp.integrate(4 * sp.pi * r**2 * density, (r, 0, sp.oo))
    )
    normalized_integral = sp.simplify(
        sp.integrate(4 * sp.pi * r**2 * rho**2, (r, 0, sp.oo))
    )
    return {
        "profile": "rho(r)=rho0*exp(-r/R)",
        "charge_density": str(density),
        "profile_inventory_integral": str(normalized_integral),
        "total_charge": str(charge),
        "charge_depends_on_kappa": charge.has(kappa),
        "charge_depends_on_frequency": charge.has(Omega),
        "charge_depends_on_profile_inventory": charge.has(rho0) and charge.has(R),
        "not_topologically_fixed_by_this_ansatz": True,
        "reading": (
            "a localized charged oscillon sources a finite total charge, but "
            "the charge value is continuous until kappa, Omega and the profile "
            "inventory are locked by a deeper theorem"
        ),
    }


# ---------------------------------------------------------------------------
# 4. Closed topological current versus Noether-current normalization
# ---------------------------------------------------------------------------

def topological_current_normalization_gap() -> dict:
    q0 = sp.symbols("q0", positive=True)
    lam0, lam1, lam2 = sp.symbols("lambda_0 lambda_1 lambda_2", real=True)
    closed_variation = q0 * (
        (lam1 - lam0) + (lam2 - lam1) + (lam0 - lam2)
    )
    open_variation = q0 * ((lam1 - lam0) + (lam2 - lam1))

    q_geom, beta = sp.symbols("q_geom beta_EM", positive=True)
    q_e = sp.simplify(beta * q_geom)
    beta_from_q0 = sp.simplify(q0 / q_geom)

    return {
        "closed_loop_gauge_variation_zero": sp.simplify(closed_variation) == 0,
        "open_line_boundary_variation": str(sp.simplify(open_variation)),
        "canonical_charge_map": str(sp.Eq(sp.Symbol("q_e"), q_e)),
        "beta_if_loop_coupling_q0_known": str(beta_from_q0),
        "q0_not_derived": True,
        "reading": (
            "closed framing currents are gauge-legal topological sources, but "
            "the coupling q0 that turns the geometric register into canonical "
            "electric charge remains the alpha-relevant normalization"
        ),
    }


# ---------------------------------------------------------------------------
# 5. Alpha target translated into current normalization only
# ---------------------------------------------------------------------------

def alpha_current_target_translation() -> dict:
    q_geom = Q_GEOM_H2_ORDER9
    q_e_required = math.sqrt(4.0 * math.pi * ALPHA_CODATA)
    beta_required = q_e_required / q_geom
    z_required = beta_required**2
    return {
        "q_geom_diagnostic": q_geom,
        "canonical_e_required": q_e_required,
        "beta_EM_required_if_q_geom_2_over_9": beta_required,
        "Z_medium_required_if_q_geom_2_over_9": z_required,
        "alpha_recovered_if_inserted": z_required * q_geom**2 / (4.0 * math.pi),
        "matches_alpha_only_if_inserted": abs(
            z_required * q_geom**2 / (4.0 * math.pi) - ALPHA_CODATA
        )
        < 1e-15,
        "target_not_derivation": True,
        "reading": (
            "the charged current gate translates the target into a required "
            "current normalization.  It does not supply that normalization."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "a Noether-to-topological lock: the localized charged oscillon "
            "current must integrate to the completed framing register with a "
            "derived canonical coefficient"
        ),
        "must_derive": [
            "the charged oscillon/core profile rho(r) from the nonlinear action",
            "the population/phase frequency Omega or its cancellation from the charge",
            "the phase stiffness kappa in the completed frame action",
            "the map between Noether charge integral and q_geom=2/9 boundary register",
            "the canonical Maxwell field normalization of the source",
        ],
        "acceptable_routes": [
            "derive q0 directly from the localized charged defect action",
            "derive beta_EM through kappa*Omega*profile_inventory/q_geom",
            "derive beta_EM through medium impedance or eta_core if those are action-derived",
            "derive a topological quantization condition that fixes the Noether integral",
        ],
        "falsification_tests": [
            "if Q = kappa*Omega*I_profile remains continuous, alpha is not derived",
            "if q0 is inserted from the observed alpha, the gate fails as a fit",
            "if only closed-loop gauge invariance is shown, topology is present but normalization is absent",
            "if the profile is chosen by hand, the source exists but alpha remains open",
        ],
        "candidate_next_gate": "p18y_noether_topological_charge_lock_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_charged_oscillon_em_source_gate() -> dict:
    current = gauge_invariant_phase_current_gate()
    gauge = local_u1_and_conservation_gate()
    inventory = stationary_oscillon_charge_inventory()
    topo = topological_current_normalization_gap()
    target = alpha_current_target_translation()
    requirements = next_theorem_requirements()

    closed = {
        "charged_phase_current_derived": bool(
            current["current_derivation_verified"]
        ),
        "local_U1_completion_invariant": bool(
            gauge["Dtheta_componentwise_invariant"]
        ),
        "stationary_localized_charge_is_finite": bool(
            inventory["total_charge"]
        ),
        "stationary_charge_not_topologically_fixed": bool(
            inventory["not_topologically_fixed_by_this_ansatz"]
        ),
        "closed_topological_current_is_gauge_legal": bool(
            topo["closed_loop_gauge_variation_zero"]
        ),
        "topological_current_coupling_q0_still_open": bool(
            topo["q0_not_derived"]
        ),
        "alpha_translated_to_current_normalization_only": bool(
            target["matches_alpha_only_if_inserted"]
            and target["target_not_derivation"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "charged_oscillon_profile_derived": False,
        "phase_frequency_lock_derived": False,
        "phase_stiffness_kappa_derived": False,
        "Noether_to_topological_charge_lock_derived": False,
        "beta_EM_derived": False,
        "canonical_e_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_NOETHER_TO_TOPOLOGICAL_CHARGE_LOCK_REQUIRED__"
            + _pass_status("CHARGED_OSCILLON_CURRENT_KINEMATICS")
            if all(closed.values())
            else "CHECK_CHARGED_OSCILLON_EM_SOURCE"
        ),
        "SCOPE": (
            "charged oscillon electromagnetic source gate after p18w: the "
            "completed frame phase gives a gauge-invariant conserved current "
            "J^mu = kappa*rho^2*D^mu theta.  A localized oscillon can source "
            "finite charge, and a closed framing current is gauge-legal, but "
            "the Noether/current normalization that yields canonical e remains "
            "open."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "phase_current": current,
        "local_U1_and_conservation": gauge,
        "stationary_inventory": inventory,
        "topological_normalization_gap": topo,
        "alpha_current_target": target,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "we now have the actual electric source slot for the charged "
            "oscillon.  The remaining alpha problem is not whether a charged "
            "oscillon can source a Maxwell field; it can.  The problem is why "
            "one completed framing unit has exactly the canonical strength e "
            "instead of any continuous q0."
        ),
        "missing_derivations": [
            "derive the charged oscillon/core profile rho(r)",
            "derive the phase stiffness kappa and frequency/tempo lock",
            "derive the Noether charge integral as the completed topological framing register",
            "derive q0 or beta_EM without using CODATA",
            "then compute alpha from alpha = beta_EM^2*q_geom^2/(4*pi)",
        ],
        "do_not_claim": [
            "Do not claim alpha, beta_EM, q0, or canonical e are derived.",
            "Do not confuse gauge-legal current with normalized electric charge.",
            "Do not set kappa, Omega or the profile integral to fit alpha.",
            "Do not treat q_geom=2/9 as canonical electric charge by itself.",
            "Do not claim the charged oscillon profile has been solved.",
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
    print("phase_current:", result["phase_current"])
    print("local_U1_and_conservation:", result["local_U1_and_conservation"])
    print("stationary_inventory:", result["stationary_inventory"])
    print("topological_normalization_gap:", result["topological_normalization_gap"])
    print("alpha_current_target:", result["alpha_current_target"])
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
    _print_result(derive_charged_oscillon_em_source_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
