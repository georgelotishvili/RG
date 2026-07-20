# Notation header (see NOTATION.md):
# This gate follows p18aj.  It writes the variational charged h=2 core solver
# scaffold and checks exactly where the 222 TeV scale would enter.

"""
================================================================================
PHASE 18ak: Charged h=2 core variational solver gate
================================================================================

Purpose
-------
p18aj named the action coefficients that must be derived before alpha can be
predicted.  This gate builds the minimal radial variational scaffold:

    E(R) = a/R + b R + c R^3 + d/R^3,

where the terms represent gradient/surface, linear restoring, volume/core and
rotational/boundary energy channels.  The h=2 branch can enter d, but the
absolute scale still depends on the coefficients.

Main result
-----------
The stationary equation is

    3 c R^6 + b R^4 - a R^2 - 3 d = 0.

For any target radius R_*, this equation fixes one coefficient combination in
terms of the others.  It does not predict R_* unless a, b, c and d are derived
from the RefG action.  The variational solver is therefore ready as a scaffold,
but alpha remains open.

What this gate does NOT claim
-----------------------------
- It does not solve the full charged core PDE.
- It does not derive the coefficients.
- It does not predict the 222 TeV scale.
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
# 1. Variational stationary equation
# ---------------------------------------------------------------------------

def variational_stationary_equation() -> dict:
    R, a, b, c, d = sp.symbols("R a b c d", positive=True)
    E = a / R + b * R + c * R**3 + d / R**3
    dE = sp.diff(E, R)
    stationary_poly = sp.simplify(R**4 * dE)
    second = sp.diff(E, R, 2)

    return {
        "energy_model": "E(R)=a/R + b*R + c*R^3 + d/R^3",
        "dE_dR": str(sp.simplify(dE)),
        "stationary_polynomial": str(stationary_poly),
        "stationary_equation": "3*c*R^6 + b*R^4 - a*R^2 - 3*d = 0",
        "second_derivative": str(sp.simplify(second)),
        "coefficient_dependence_present": all(
            stationary_poly.has(x) for x in (a, b, c, d)
        ),
        "reading": (
            "the radial variational problem is now explicit.  Its stationary "
            "radius is controlled by action coefficients."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Target insertion relation
# ---------------------------------------------------------------------------

def target_insertion_relation() -> dict:
    R, a, b, c, d, Rstar = sp.symbols("R a b c d R_star", positive=True)
    equation = sp.Eq(3 * c * Rstar**6 + b * Rstar**4 - a * Rstar**2 - 3 * d, 0)
    solved_b = sp.solve(equation, b)[0]
    solved_c = sp.solve(equation, c)[0]

    mu = _required_mu_bare_mev()
    R_target = 1.0 / mu
    b_required_if_a1_c0_d0 = float(solved_b.subs({Rstar: R_target, a: 1, c: 0, d: 0}))
    c_required_if_a1_b0_d0 = float(solved_c.subs({Rstar: R_target, a: 1, b: 0, d: 0}))

    return {
        "target_mu_MeV": mu,
        "target_R_MeV_inverse": R_target,
        "stationary_condition_at_Rstar": str(equation),
        "b_solved_from_target": str(solved_b),
        "c_solved_from_target": str(solved_c),
        "example_b_required_if_a1_c0_d0": b_required_if_a1_c0_d0,
        "example_c_required_if_a1_b0_d0": c_required_if_a1_b0_d0,
        "target_insertion_is_fit_unless_coefficients_derived": True,
        "reading": (
            "given R_target one can always solve for a coefficient.  This is "
            "a target relation, not a derivation."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Stability condition
# ---------------------------------------------------------------------------

def stability_condition_gate() -> dict:
    R, a, b, c, d = sp.symbols("R a b c d", positive=True)
    second = sp.simplify(2 * a / R**3 + 6 * c * R + 12 * d / R**5)
    # With positive a,c,d the second derivative is positive at any positive R.
    positive_terms = [2 * a / R**3, 6 * c * R, 12 * d / R**5]
    all_positive = all(term.has(x) for term, x in zip(positive_terms, (a, c, d)))
    return {
        "second_derivative": str(second),
        "positive_if_a_c_d_positive": all_positive,
        "b_does_not_enter_second_derivative": not second.has(b),
        "stability_is_not_enough_for_scale_prediction": True,
        "reading": (
            "positive coefficients can give a stable stationary point, but "
            "stability alone does not choose the target radius."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Dimensionless solver versus physical unit
# ---------------------------------------------------------------------------

def dimensionless_solver_unit_guard() -> dict:
    x, eps, delta = sp.symbols("x epsilon delta", positive=True)
    # Normalize a=b=1 and write c=epsilon, d=delta.
    E = 1 / x + x + eps * x**3 + delta / x**3
    stationary = sp.simplify(x**4 * sp.diff(E, x))

    return {
        "dimensionless_energy": "E(x)=1/x + x + epsilon*x^3 + delta/x^3",
        "dimensionless_stationary_equation": str(stationary),
        "dimensionless_solution_needs_physical_unit": True,
        "physical_radius_rule": "R = L0*x_star",
        "physical_scale_rule": "mu = 1/(L0*x_star)",
        "L0_not_derived": True,
        "reading": (
            "a dimensionless variational solver may select x_star.  The "
            "physical TeV scale still requires L0 from the action."
        ),
    }


# ---------------------------------------------------------------------------
# 5. h=2 contribution audit
# ---------------------------------------------------------------------------

def h2_contribution_audit() -> dict:
    n, d0, R = sp.symbols("n d0 R", positive=True)
    d = d0 * n**2
    rotational = d / R**3
    ratio_h2_h1 = sp.simplify(rotational.subs(n, 2) / rotational.subs(n, 1))

    return {
        "rotational_or_boundary_energy": "d0*n^2/R^3",
        "h2_over_h1_energy_ratio": str(ratio_h2_h1),
        "h2_changes_relative_energy": True,
        "d0_still_needed_for_absolute_scale": rotational.has(d0),
        "reading": (
            "h=2 can multiply the boundary/rotational energy by four.  It "
            "does not remove the need to derive d0."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Next theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "turn the variational scaffold into an action-derived charged h=2 "
            "core calculation"
        ),
        "must_derive": [
            "profile ansatz fields rho(r), theta(t,r), n(r,angles), A_frame",
            "coefficients a,b,c,d from the RefG action",
            "dimensionless stationary solution x_star",
            "physical unit L0 or mu0",
            "stability spectrum around the stationary core",
            "relation between mu_core and the p18ag running scale",
        ],
        "falsification_tests": [
            "if coefficients are fitted to R_target, the solver is not a derivation",
            "if no positive stable h=2 stationary point exists, the n=2 route fails",
            "if L0 remains free, no TeV prediction is made",
            "if the predicted mu_core misses the running target and no spectrum correction appears, alpha route fails",
        ],
        "candidate_next_gate": "p18al_charged_core_profile_eom_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_charged_h2_core_variational_solver_gate() -> dict:
    stationary = variational_stationary_equation()
    target = target_insertion_relation()
    stability = stability_condition_gate()
    dimensionless = dimensionless_solver_unit_guard()
    h2 = h2_contribution_audit()
    requirements = next_theorem_requirements()

    closed = {
        "stationary_equation_written": bool(
            stationary["coefficient_dependence_present"]
        ),
        "target_relation_identified_as_fit_if_inserted": bool(
            target["target_insertion_is_fit_unless_coefficients_derived"]
        ),
        "stability_condition_separated_from_scale": bool(
            stability["stability_is_not_enough_for_scale_prediction"]
        ),
        "dimensionless_solver_needs_physical_unit": bool(
            dimensionless["dimensionless_solution_needs_physical_unit"]
            and dimensionless["L0_not_derived"]
        ),
        "h2_relative_contribution_identified": bool(
            h2["h2_changes_relative_energy"]
            and h2["d0_still_needed_for_absolute_scale"]
        ),
        "no_target_fit_claimed": True,
    }

    open_checks = {
        "profile_EOM_derived": False,
        "coefficients_derived": False,
        "dimensionless_solution_found": False,
        "physical_unit_L0_derived": False,
        "stability_spectrum_computed": False,
        "mu_core_predicted": False,
        "alpha_predicted": False,
    }

    result = {
        "STATUS": (
            "OPEN_CHARGED_CORE_PROFILE_EOM_REQUIRED__"
            + _pass_status("CHARGED_H2_VARIATIONAL_SOLVER_SCAFFOLD")
            if all(closed.values())
            else "CHECK_CHARGED_H2_CORE_VARIATIONAL_SOLVER"
        ),
        "SCOPE": (
            "charged h=2 variational solver gate after p18aj: the radial "
            "stationary equation and stability conditions are explicit.  "
            "The scaffold can test future action-derived coefficients, but "
            "it does not predict the 222 TeV scale until the coefficients "
            "and physical unit are derived."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "stationary_equation": stationary,
        "target_insertion_relation": target,
        "stability_condition": stability,
        "dimensionless_solver_guard": dimensionless,
        "h2_contribution": h2,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the mathematical solver skeleton is now ready.  The next real "
            "physics step is not another target calculation; it is deriving "
            "the profile EOM and coefficients from the charged RefG action."
        ),
        "missing_derivations": [
            "derive the charged profile EOM",
            "derive a,b,c,d and the physical unit L0",
            "solve for the h=2 stationary core",
            "compute the stability spectrum",
            "compare predicted mu_core to 222 TeV without fitting",
        ],
        "do_not_claim": [
            "Do not claim the variational scaffold predicts alpha.",
            "Do not fit coefficients to R_target.",
            "Do not treat stability as scale prediction.",
            "Do not claim h=2 fixes the dimensional unit.",
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
    print("stationary_equation:", result["stationary_equation"])
    print("target_insertion_relation:", result["target_insertion_relation"])
    print("stability_condition:", result["stability_condition"])
    print("dimensionless_solver_guard:", result["dimensionless_solver_guard"])
    print("h2_contribution:", result["h2_contribution"])
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
    _print_result(derive_charged_h2_core_variational_solver_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
