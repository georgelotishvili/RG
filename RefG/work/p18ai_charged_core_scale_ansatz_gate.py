# Notation header (see NOTATION.md):
# This gate follows p18ah.  It tests simple charged-core energy ansatze to see
# whether the 222 TeV target scale can arise from topology/regularity alone, or
# whether dimensional action coefficients remain necessary.

"""
================================================================================
PHASE 18ai: Charged core scale ansatz gate
================================================================================

Purpose
-------
p18ah translated the lepton-running bridge into a target core/readout scale:

    mu_target ~= 222 TeV,
    R_target ~= 8.87e-22 m.

This gate tests simple localized-core energy models.  The question is not
whether one can write a formula for a scale.  The question is whether the scale
is fixed by topology/regularity, or whether it depends on dimensional action
coefficients that RefG has not derived.

Main result
-----------
The scale is not fixed by the ansatz alone.  Derrick-type balances can create
a finite radius, but the radius and energy always depend on coefficients such
as gradient stiffness, core pressure, Skyrme stiffness, inertia or boundary
level.  Topology can fix integers such as n=2; it does not fix the dimensional
scale 222 TeV.

What this gate does NOT claim
-----------------------------
- It does not derive the charged core.
- It does not derive the 222 TeV scale.
- It does not derive alpha.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_INV_BARE_N2 = 81.0 * math.pi / 2.0
QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)
LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}
HBAR_C_MEV_FM = 197.3269804


def _required_mu_bare_mev() -> float:
    delta = ALPHA_INV_CODATA - ALPHA_INV_BARE_N2
    masses = list(LEPTON_MASSES_MEV.values())
    log_sum_required = delta / QED_ONE_LOOP_B
    return math.exp((log_sum_required + sum(math.log(m) for m in masses)) / 3.0)


# ---------------------------------------------------------------------------
# 1. Two-term finite-radius balance
# ---------------------------------------------------------------------------

def two_term_core_balance_audit() -> dict:
    R, A, B = sp.symbols("R A B", positive=True)
    energy = A / R + B * R
    dE = sp.diff(energy, R)
    R_solution = sp.solve(sp.Eq(dE, 0), R)[0]
    E_solution = sp.simplify(energy.subs(R, R_solution))

    return {
        "energy_model": "E(R)=A/R + B*R",
        "stationary_radius": str(R_solution),
        "stationary_energy": str(E_solution),
        "radius_depends_on_coefficients": R_solution.has(A) and R_solution.has(B),
        "energy_depends_on_coefficients": E_solution.has(A) and E_solution.has(B),
        "reading": (
            "a finite radius can appear from balance, but the scale is "
            "sqrt(A/B).  Topology alone has not fixed A or B."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Volume-pressure balance
# ---------------------------------------------------------------------------

def volume_pressure_balance_audit() -> dict:
    R, A, Lambda = sp.symbols("R A Lambda", positive=True)
    energy = A / R + Lambda * R**3
    dE = sp.diff(energy, R)
    R_solution = sp.solve(sp.Eq(dE, 0), R)[0]
    E_solution = sp.simplify(energy.subs(R, R_solution))

    return {
        "energy_model": "E(R)=A/R + Lambda*R^3",
        "stationary_radius": str(R_solution),
        "stationary_energy": str(E_solution),
        "radius_depends_on_coefficients": (
            R_solution.has(A) and R_solution.has(Lambda)
        ),
        "energy_depends_on_coefficients": (
            E_solution.has(A) and E_solution.has(Lambda)
        ),
        "reading": (
            "a bag/pressure term gives R=(A/(3*Lambda))^(1/4).  This is a "
            "real scale only after A and Lambda are derived from the action."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Rotating/boundary-level core balance
# ---------------------------------------------------------------------------

def boundary_rotator_balance_audit() -> dict:
    R, n, I0, sigma = sp.symbols("R n I0 sigma", positive=True)
    # I(R)=I0*R^3, rotational energy n^2/(2I), plus surface/gradient sigma*R.
    energy = n**2 / (2 * I0 * R**3) + sigma * R
    dE = sp.diff(energy, R)
    R_solution = sp.solve(sp.Eq(dE, 0), R)[0]
    E_solution = sp.simplify(energy.subs(R, R_solution))

    return {
        "energy_model": "E(R)=n^2/(2*I0*R^3)+sigma*R",
        "stationary_radius": str(R_solution),
        "stationary_energy": str(E_solution),
        "h2_branch_radius_scaling": str(sp.simplify(R_solution.subs(n, 2))),
        "radius_depends_on_I0_and_sigma": (
            R_solution.has(I0) and R_solution.has(sigma)
        ),
        "topological_n_changes_power_but_not_scale_coefficients": True,
        "reading": (
            "the integer branch n can enter the radius, but dimensional "
            "coefficients I0 and sigma still set the actual scale."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Target coefficient ledger
# ---------------------------------------------------------------------------

def target_coefficient_ledger() -> dict:
    mu_mev = _required_mu_bare_mev()
    R_target_fm = HBAR_C_MEV_FM / mu_mev

    # For E=A/R+B*R, R=sqrt(A/B).  In natural units with R in MeV^-1, the
    # target only fixes A/B=R^2.  It does not fix A and B.
    R_target_mev_inv = 1.0 / mu_mev
    ratio_A_over_B = R_target_mev_inv**2

    return {
        "mu_target_MeV": mu_mev,
        "R_target_fm": R_target_fm,
        "R_target_MeV_inverse": R_target_mev_inv,
        "A_over_B_required_in_two_term_model": ratio_A_over_B,
        "target_ratio_not_derivation": True,
        "reading": (
            "the target scale can be expressed as a required coefficient "
            "ratio, but this only moves the problem into A/B unless the "
            "action derives those coefficients."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Scale-free topology guard
# ---------------------------------------------------------------------------

def scale_free_topology_guard() -> dict:
    n, A, B = sp.symbols("n A B", positive=True)
    R = sp.sqrt(A / B) * sp.sqrt(n)
    scaled = sp.simplify(R.subs(n, 2) / R.subs(n, 1))
    return {
        "integer_branch_changes_relative_radius": str(scaled),
        "absolute_radius_still_contains_A_over_B": R.has(A) and R.has(B),
        "topology_sets_integer_not_dimensionful_unit": True,
        "reading": (
            "integer topology can select relative branches such as sqrt(2). "
            "It cannot supply MeV, TeV or meters without a dimensional action "
            "coefficient."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Next theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "derive the dimensional coefficients of the charged h=2 core "
            "from the RefG action"
        ),
        "must_derive": [
            "gradient/surface stiffness coefficient",
            "volume pressure or core potential coefficient",
            "rotational inertia functional I(R)",
            "boundary first-order level C",
            "matching rule between stationary core energy/radius and running scale",
        ],
        "falsification_tests": [
            "if all coefficients remain free, the 222 TeV scale is not derived",
            "if the target coefficient ratio is inserted, the route is a fit",
            "if the h=2 branch has no stable stationary core, the n=2 route fails",
            "if the stationary core scale differs strongly from 222 TeV and no extra channels appear, the alpha route fails",
        ],
        "candidate_next_gate": "p18aj_charged_core_action_coefficient_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_charged_core_scale_ansatz_gate() -> dict:
    two_term = two_term_core_balance_audit()
    volume = volume_pressure_balance_audit()
    rotator = boundary_rotator_balance_audit()
    target = target_coefficient_ledger()
    topology = scale_free_topology_guard()
    requirements = next_theorem_requirements()

    closed = {
        "two_term_balance_leaves_coefficients": bool(
            two_term["radius_depends_on_coefficients"]
            and two_term["energy_depends_on_coefficients"]
        ),
        "volume_balance_leaves_coefficients": bool(
            volume["radius_depends_on_coefficients"]
            and volume["energy_depends_on_coefficients"]
        ),
        "rotator_balance_leaves_coefficients": bool(
            rotator["radius_depends_on_I0_and_sigma"]
        ),
        "target_ratio_recorded_as_target_only": bool(
            target["target_ratio_not_derivation"]
        ),
        "topology_guard_active": bool(
            topology["absolute_radius_still_contains_A_over_B"]
            and topology["topology_sets_integer_not_dimensionful_unit"]
        ),
        "no_222TeV_derivation_claimed": True,
    }

    open_checks = {
        "charged_core_action_coefficients_derived": False,
        "stable_h2_core_solution_found": False,
        "R_core_predicted": False,
        "mu_bare_predicted": False,
        "alpha_predicted": False,
    }

    result = {
        "STATUS": (
            "OPEN_CHARGED_CORE_ACTION_COEFFICIENTS_REQUIRED__"
            + _pass_status("CHARGED_CORE_SCALE_ANSATZ_AUDIT")
            if all(closed.values())
            else "CHECK_CHARGED_CORE_SCALE_ANSATZ"
        ),
        "SCOPE": (
            "charged-core scale ansatz gate after p18ah: simple finite-radius "
            "balances show how a scale could arise, but all such scales "
            "depend on action coefficients.  Topology can select n=2 or "
            "sqrt(2)-type relative factors; it cannot by itself derive the "
            "222 TeV dimensional scale."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "two_term_balance": two_term,
        "volume_pressure_balance": volume,
        "boundary_rotator_balance": rotator,
        "target_coefficient_ledger": target,
        "scale_free_topology_guard": topology,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "we now know what a successful alpha-scale calculation must do: "
            "not merely write a stable core, but derive the coefficients whose "
            "balance places that core near the 222 TeV target."
        ),
        "missing_derivations": [
            "derive core action coefficients from RefG",
            "solve the charged h=2 stationary core",
            "predict R_core or mu_bare without alpha input",
            "compare the predicted scale to the 222 TeV target",
        ],
        "do_not_claim": [
            "Do not claim topology fixes the dimensional core scale.",
            "Do not insert the target coefficient ratio as a derivation.",
            "Do not claim a stable core exists until the EOM is solved.",
            "Do not claim alpha is predicted.",
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
    print("two_term_balance:", result["two_term_balance"])
    print("volume_pressure_balance:", result["volume_pressure_balance"])
    print("boundary_rotator_balance:", result["boundary_rotator_balance"])
    print("target_coefficient_ledger:", result["target_coefficient_ledger"])
    print("scale_free_topology_guard:", result["scale_free_topology_guard"])
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
    _print_result(derive_charged_core_scale_ansatz_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
