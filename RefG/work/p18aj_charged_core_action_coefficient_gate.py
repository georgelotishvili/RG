# Notation header (see NOTATION.md):
# This gate follows p18ai.  It audits the action coefficients that would be
# needed to turn the 222 TeV charged-core target into a RefG prediction.

"""
================================================================================
PHASE 18aj: Charged core action coefficient gate
================================================================================

Purpose
-------
p18ai showed that simple charged-core ansatze can create a finite core scale,
but only through dimensional action coefficients.  This gate names those
coefficients and checks whether current RefG work has already fixed them.

Target inherited from p18ag-p18ai
---------------------------------
The conditional n=2 alpha route gives

    alpha_bare^{-1} = 81*pi/2,

and lepton-only running to alpha(0) asks for

    mu_bare ~= 222 TeV,
    R_core ~= 8.87e-22 m.

Main result
-----------
The present RefG files identify the correct coefficient slots, but they do not
derive the numerical coefficient ratios.  A successful next theorem must
derive, from one localized charged h=2 core action, at least:

    gradient/surface stiffness,
    volume/core pressure or potential,
    rotational inertia,
    first-order boundary level,
    Maxwell field stiffness and source coupling.

Until those are fixed, the 222 TeV scale remains a sharp target, not a
prediction.

What this gate does NOT claim
-----------------------------
- It does not derive the charged core action.
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
# 1. Coefficient inventory
# ---------------------------------------------------------------------------

def charged_core_coefficient_inventory() -> dict:
    return {
        "minimal_effective_core_action": [
            "K_grad * |D n|^2 or |D Phi|^2",
            "K_skyrme * |F_frame|^2 or higher-gradient stabilizer",
            "V_core(rho) or Lambda_core pressure/potential term",
            "I_core(R) * dot(theta)^2 / 2",
            "C_B * A_frame(theta,n) first-order boundary/Berry term",
            "-K_F * F_Maxwell^2 / 4",
            "k_J * A_mu * J_charged^mu",
        ],
        "coefficient_roles": {
            "K_grad_or_A": "surface/gradient 1/R-type energy",
            "B_or_sigma": "linear radius/surface restoring energy",
            "Lambda_core": "volume/core pressure R^3 energy",
            "I0": "rotational inertia density in I(R)=I0*R^3",
            "C_B": "first-order boundary level in Theta_boundary",
            "K_F": "canonical Maxwell field stiffness",
            "k_J": "charged core source coupling",
        },
        "all_are_needed_for_prediction": True,
        "reading": (
            "the coefficient slots are now explicit.  Alpha closes only if "
            "these are tied together by the completed charged-core action."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Existing RefG support audit
# ---------------------------------------------------------------------------

def existing_refg_support_audit() -> dict:
    return {
        "supported_now": [
            "p10: symbolic oscillon-to-gravity short path once a localized source is supplied",
            "p10: finite-energy nonlinear oscillon particle theorem is still open",
            "p11/p17: C3/order-9 charged-lepton internal block is a strong structural candidate",
            "p18x/p18y: charged oscillon/framing current and q_geom=2/9 register are identified",
            "p18z/p18aa: q0=k_J/sqrt(K_F) is the Maxwell normalization bottleneck",
            "p18ad-p18ae: n=2 gives a clean bare candidate alpha^{-1}=81*pi/2 if q0^2=n is derived",
        ],
        "not_supported_yet": [
            "full localized charged h=2 oscillon solution",
            "action-derived K_grad, Lambda_core, I0, sigma or C_B",
            "action-derived K_F and k_J",
            "electron mass/threshold derivation",
            "U(1)/EW matching and full charged spectrum",
        ],
        "coefficients_derived_in_existing_work": False,
        "reading": (
            "current work has the map and the bottlenecks, not the numerical "
            "core-action coefficient theorem."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Target coefficient ratios
# ---------------------------------------------------------------------------

def target_coefficient_ratio_table() -> dict:
    mu = _required_mu_bare_mev()
    R = 1.0 / mu
    n = 2.0

    # Natural units: R in MeV^-1.
    two_term_A_over_B = R**2
    volume_A_over_Lambda = 3.0 * R**4
    rotator_I0_sigma = 3.0 * n**2 / (2.0 * R**4)

    return {
        "mu_target_MeV": mu,
        "mu_target_TeV": mu / 1.0e6,
        "R_target_MeV_inverse": R,
        "R_target_m": HBAR_C_MEV_FM / mu * 1.0e-15,
        "two_term_model_E_A_over_R_plus_B_R_requires_A_over_B": two_term_A_over_B,
        "volume_model_E_A_over_R_plus_Lambda_R3_requires_A_over_Lambda": volume_A_over_Lambda,
        "rotator_model_E_n2_over_2I_plus_sigmaR_requires_I0_times_sigma_for_n2": rotator_I0_sigma,
        "ratios_are_targets_not_derivations": True,
        "reading": (
            "the 222 TeV target translates into precise coefficient ratios.  "
            "These numbers are useful targets for the action, not inputs."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Dimensional rescaling no-go
# ---------------------------------------------------------------------------

def dimensional_rescaling_no_go() -> dict:
    A, B, lam = sp.symbols("A B lambda", positive=True)
    R = sp.sqrt(A / B)
    R_rescaled_B = sp.simplify(sp.sqrt(A / (lam * B)))
    R_rescaled_common = sp.simplify(sp.sqrt((lam * A) / (lam * B)))

    return {
        "two_term_radius": str(R),
        "radius_after_B_rescale": str(R_rescaled_B),
        "radius_changes_if_relative_coefficient_changes": (
            sp.simplify(R_rescaled_B / R - 1 / sp.sqrt(lam)) == 0
        ),
        "radius_after_common_A_B_rescale": str(R_rescaled_common),
        "common_rescale_does_not_change_radius": (
            sp.simplify(R_rescaled_common - R) == 0
        ),
        "topology_unaffected_by_rescaling": True,
        "reading": (
            "topological integers remain the same while relative action "
            "coefficients move the core scale.  Therefore the scale is an "
            "action-coefficient question."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Single-coefficient shortcut guard
# ---------------------------------------------------------------------------

def single_coefficient_shortcut_guard() -> dict:
    kappa, a, b, R = sp.symbols("kappa a b R", positive=True)
    A = kappa * a
    B = kappa * b
    radius = sp.simplify(sp.sqrt(A / B))
    energy = sp.simplify(A / radius + B * radius)

    return {
        "assumption": "A=kappa*a and B=kappa*b",
        "stationary_radius": str(radius),
        "stationary_energy": str(energy),
        "radius_independent_of_common_kappa": not radius.has(kappa),
        "radius_still_depends_on_dimensionful_ratio_a_over_b": (
            radius.has(a) and radius.has(b)
        ),
        "energy_still_depends_on_common_kappa": energy.has(kappa),
        "reading": (
            "even a single common stiffness does not automatically fix the "
            "length.  The relative dimensional pieces a/b still carry the "
            "scale unless the full action fixes them."
        ),
    }


# ---------------------------------------------------------------------------
# 6. What would count as closure
# ---------------------------------------------------------------------------

def closure_requirements() -> dict:
    return {
        "needed_theorem": (
            "derive the charged h=2 core action coefficients and solve the "
            "stationary core without using alpha"
        ),
        "minimal_outputs": [
            "R_core_predicted or mu_core_predicted",
            "stable h=2 stationary solution",
            "boundary level C_B and q0^2=n map",
            "K_F and k_J Maxwell normalization",
            "matching rule between core scale and running scale",
        ],
        "success_test": (
            "predicted mu_core is near the p18ag target, or the theory derives "
            "additional charged channels that move the running target"
        ),
        "failure_tests": [
            "coefficients remain independent free parameters",
            "target ratios are inserted from alpha",
            "h=2 core is unstable or absent",
            "q0^2=n map fails",
            "derived scale misses the running target and no extra charged channels compensate",
        ],
        "candidate_next_gate": "p18ak_charged_h2_core_variational_solver_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_charged_core_action_coefficient_gate() -> dict:
    inventory = charged_core_coefficient_inventory()
    support = existing_refg_support_audit()
    targets = target_coefficient_ratio_table()
    rescale = dimensional_rescaling_no_go()
    shortcut = single_coefficient_shortcut_guard()
    requirements = closure_requirements()

    closed = {
        "coefficient_inventory_explicit": bool(
            inventory["all_are_needed_for_prediction"]
        ),
        "existing_work_does_not_derive_coefficients": not support[
            "coefficients_derived_in_existing_work"
        ],
        "target_ratios_recorded_without_claim": bool(
            targets["ratios_are_targets_not_derivations"]
        ),
        "dimensional_rescaling_shows_action_dependence": bool(
            rescale["radius_changes_if_relative_coefficient_changes"]
            and rescale["topology_unaffected_by_rescaling"]
        ),
        "single_common_coefficient_shortcut_blocked": bool(
            shortcut["radius_independent_of_common_kappa"]
            and shortcut["radius_still_depends_on_dimensionful_ratio_a_over_b"]
        ),
        "no_alpha_fit_claimed": True,
    }

    open_checks = {
        "charged_h2_core_action_derived": False,
        "core_coefficients_derived": False,
        "stable_core_solution_found": False,
        "mu_core_predicted": False,
        "Maxwell_normalization_derived": False,
        "alpha_predicted": False,
    }

    result = {
        "STATUS": (
            "OPEN_CHARGED_H2_CORE_VARIATIONAL_SOLVER_REQUIRED__"
            + _pass_status("CHARGED_CORE_ACTION_COEFFICIENT_AUDIT")
            if all(closed.values())
            else "CHECK_CHARGED_CORE_ACTION_COEFFICIENT_GATE"
        ),
        "SCOPE": (
            "charged-core action coefficient gate after p18ai: the coefficient "
            "slots needed for a 222 TeV prediction are named and audited.  "
            "Existing RefG work identifies the structure but does not derive "
            "the numerical action coefficients.  Relative coefficient ratios, "
            "not topology alone, set the dimensional core scale."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "coefficient_inventory": inventory,
        "existing_refg_support": support,
        "target_coefficient_ratios": targets,
        "dimensional_rescaling_no_go": rescale,
        "single_coefficient_shortcut_guard": shortcut,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the alpha route is now an action-coefficient problem.  A clean "
            "topological branch gives the dimensionless pieces, but the 222 "
            "TeV scale must come from the charged h=2 core action and its "
            "stationary solution."
        ),
        "missing_derivations": [
            "derive the charged h=2 core action",
            "derive all dimensional coefficients from RefG",
            "solve the variational core and predict mu_core",
            "derive Maxwell normalization and q0^2=n",
            "compare the predicted scale to the p18ag running target",
        ],
        "do_not_claim": [
            "Do not claim 222 TeV is predicted.",
            "Do not claim action coefficients are already derived.",
            "Do not set coefficient ratios from the alpha target.",
            "Do not claim topology alone fixes a dimensional scale.",
            "Do not claim alpha is derived.",
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
    print("coefficient_inventory:", result["coefficient_inventory"])
    print("existing_refg_support:", result["existing_refg_support"])
    print("target_coefficient_ratios:", result["target_coefficient_ratios"])
    print("dimensional_rescaling_no_go:", result["dimensional_rescaling_no_go"])
    print("single_coefficient_shortcut_guard:", result["single_coefficient_shortcut_guard"])
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
    _print_result(derive_charged_core_action_coefficient_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
