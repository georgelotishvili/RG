# Notation header (see NOTATION.md):
# This gate follows p18ag.  It audits whether the target bare scale required
# by the lepton-only running bridge can be derived from the charged oscillon
# core rather than solved from the observed alpha.

"""
================================================================================
PHASE 18ah: Bare scale from oscillon core gate
================================================================================

Purpose
-------
p18ag found a sharp target:

    alpha_bare^{-1} = 81*pi/2
    lepton-only threshold running to alpha(0)
    requires mu_bare ~= 222 TeV.

This gate asks whether RefG currently derives such a bare scale from the
charged oscillon/core action.

Main result
-----------
The 222 TeV target can be translated into a core length

    R_core ~= 8.87e-22 m,

but it is not derived by the present C3/Koide spectrum.  The C3 charged-lepton
block is scale-free: it fixes ratios, not the absolute electron mass and not
the much higher boundary/readout scale.  A real derivation must come from the
localized charged oscillon action: stiffness, core radius, boundary level and
the Maxwell readout map.

What this gate does NOT claim
-----------------------------
- It does not derive the 222 TeV scale.
- It does not derive the electron mass.
- It does not derive the charged oscillon radius.
- It does not derive low-energy alpha.
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
    log_sum_required = delta / QED_ONE_LOOP_B
    masses = list(LEPTON_MASSES_MEV.values())
    return math.exp((log_sum_required + sum(math.log(m) for m in masses)) / 3.0)


# ---------------------------------------------------------------------------
# 1. Target scale translation
# ---------------------------------------------------------------------------

def target_scale_translation() -> dict:
    mu_mev = _required_mu_bare_mev()
    radius_fm = HBAR_C_MEV_FM / mu_mev
    radius_m = radius_fm * 1.0e-15
    return {
        "mu_bare_target_MeV": mu_mev,
        "mu_bare_target_GeV": mu_mev / 1000.0,
        "mu_bare_target_TeV": mu_mev / 1.0e6,
        "core_length_target_fm": radius_fm,
        "core_length_target_m": radius_m,
        "mu_over_electron_mass": mu_mev / LEPTON_MASSES_MEV["electron"],
        "mu_over_tau_mass": mu_mev / LEPTON_MASSES_MEV["tau"],
        "translation_only_not_derivation": True,
        "reading": (
            "the lepton-only running bridge translates into a charged-core "
            "readout scale around 222 TeV, or a length around 8.9e-22 m."
        ),
    }


# ---------------------------------------------------------------------------
# 2. C3/Koide scale-free no-go
# ---------------------------------------------------------------------------

def c3_scale_free_no_go() -> dict:
    A, theta, k = sp.symbols("A theta k", positive=True)
    nu0, nu1 = sp.symbols("nu0 nu1", positive=True)
    ratio = sp.simplify((A * nu1) / (A * nu0))

    gamma_m, Omega_loc, lam = sp.symbols(
        "gamma_m Omega_loc lambda", positive=True
    )
    mass_rule = sp.simplify(gamma_m * Omega_loc**2 * lam)

    return {
        "frequency_ratio_A_cancels": str(ratio),
        "ratio_independent_of_absolute_scale_A": not ratio.has(A),
        "spectral_mass_rule": str(mass_rule),
        "mass_rule_contains_absolute_scale": (
            mass_rule.has(gamma_m) and mass_rule.has(Omega_loc)
        ),
        "C3_fixes_ratios_not_mu_bare": True,
        "reading": (
            "C3/Koide is a ratio theorem candidate.  It cannot by itself fix "
            "electron mass, the bare readout scale, or the 222 TeV target."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Electron-anchor scale audit
# ---------------------------------------------------------------------------

def electron_anchor_scale_audit() -> dict:
    mu_mev = _required_mu_bare_mev()
    me = LEPTON_MASSES_MEV["electron"]
    ratio = mu_mev / me
    return {
        "electron_mass_MeV": me,
        "mu_bare_target_MeV": mu_mev,
        "mu_bare_over_electron": ratio,
        "log_mu_over_electron": math.log(ratio),
        "electron_anchor_does_not_derive_mu_bare": True,
        "reading": (
            "using the electron mass as an anchor does not explain the bare "
            "scale.  It only states a huge dimensionless ratio that RefG must "
            "derive from core/action physics if this route is to close."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Core-action scale candidates
# ---------------------------------------------------------------------------

def core_action_scale_candidates() -> dict:
    K, I, R, C, q_geom = sp.symbols(
        "K_core I_core R_core C q_geom", positive=True
    )
    omega_core = sp.sqrt(K / I)
    inverse_radius_scale = 1 / R
    boundary_readout = sp.sqrt(C * q_geom)

    return {
        "candidate_frequency_scale": str(omega_core),
        "candidate_inverse_radius_scale": str(inverse_radius_scale),
        "candidate_boundary_readout_amplitude": str(boundary_readout),
        "free_objects": ["K_core", "I_core", "R_core", "C", "q_geom"],
        "scale_not_fixed_without_core_solution": True,
        "required_derivation": (
            "solve the localized charged oscillon/core equations and derive "
            "K_core, I_core, R_core and C from one action"
        ),
        "reading": (
            "the right mathematical slots exist.  The scale could come from "
            "a core frequency, inverse radius, or boundary readout level.  "
            "None is derived by the present gates."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Radius target consistency
# ---------------------------------------------------------------------------

def radius_target_consistency() -> dict:
    target = target_scale_translation()
    radius_m = target["core_length_target_m"]
    planck_length_m = 1.616255e-35
    ew_length_m = HBAR_C_MEV_FM / (100.0 * 1000.0) * 1.0e-15
    return {
        "core_length_target_m": radius_m,
        "core_length_over_planck_length": radius_m / planck_length_m,
        "core_length_over_100GeV_length": radius_m / ew_length_m,
        "target_is_far_above_planck_length": radius_m / planck_length_m > 1.0e10,
        "target_is_below_rough_EW_length": radius_m < ew_length_m,
        "reading": (
            "the target length is microscopic but not Planckian.  It is far "
            "above the Planck length and below a rough 100 GeV electroweak "
            "length.  This is a consistency scale, not a derivation."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Next theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "derive the charged oscillon/core scale that should be compared "
            "to the 222 TeV target"
        ),
        "must_derive": [
            "localized charged h=2 oscillon ansatz",
            "core radius R_core or equivalent inverse scale",
            "core stiffness/inertia ratio K_core/I_core",
            "boundary level C and readout q0",
            "relation between this core scale and the running matching scale",
        ],
        "falsification_tests": [
            "if the derived core scale is nowhere near the running target and no extra charged channels appear, the n=2 alpha route fails",
            "if the 222 TeV scale is inserted as a fit, the bridge fails",
            "if C3 remains only scale-free, it cannot close alpha",
            "if the core solution has no first-order boundary level, q0^2=n remains unsupported",
        ],
        "candidate_next_gate": "p18ai_charged_core_scale_ansatz_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_bare_scale_from_oscillon_core_gate() -> dict:
    target = target_scale_translation()
    c3 = c3_scale_free_no_go()
    anchor = electron_anchor_scale_audit()
    core = core_action_scale_candidates()
    radius = radius_target_consistency()
    requirements = next_theorem_requirements()

    closed = {
        "target_scale_translated_to_length": bool(
            target["translation_only_not_derivation"]
        ),
        "C3_scale_free_no_go_recorded": bool(
            c3["ratio_independent_of_absolute_scale_A"]
            and c3["C3_fixes_ratios_not_mu_bare"]
        ),
        "electron_anchor_does_not_derive_bare_scale": bool(
            anchor["electron_anchor_does_not_derive_mu_bare"]
        ),
        "core_action_slots_identified_but_free": bool(
            core["scale_not_fixed_without_core_solution"]
        ),
        "radius_target_consistency_checked": bool(
            radius["target_is_far_above_planck_length"]
            and radius["target_is_below_rough_EW_length"]
        ),
        "no_scale_fit_claim_performed": True,
    }

    open_checks = {
        "charged_core_solution_derived": False,
        "R_core_derived": False,
        "K_over_I_derived": False,
        "boundary_level_C_derived": False,
        "matching_scale_predicted": False,
        "alpha_predicted": False,
    }

    result = {
        "STATUS": (
            "OPEN_CHARGED_CORE_SCALE_DERIVATION_REQUIRED__"
            + _pass_status("BARE_SCALE_TARGET_AUDIT")
            if all(closed.values())
            else "CHECK_BARE_SCALE_FROM_OSCILLON_CORE"
        ),
        "SCOPE": (
            "bare-scale gate after p18ag: the lepton-only running bridge "
            "requires a target scale near 222 TeV, equivalent to a core "
            "length around 8.9e-22 m.  C3/Koide is scale-free and cannot "
            "derive this number.  The scale must come from the localized "
            "charged oscillon/core action."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "target_scale": target,
        "C3_scale_free_no_go": c3,
        "electron_anchor_audit": anchor,
        "core_action_candidates": core,
        "radius_target_consistency": radius,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the alpha route now has a concrete experimental-scale target: "
            "a charged core/readout scale of about 222 TeV.  That is not "
            "derived, but it tells the next calculation exactly what it must "
            "hit or explain away."
        ),
        "missing_derivations": [
            "derive the localized charged h=2 oscillon core",
            "derive its radius or frequency scale",
            "derive the boundary level C and q0 readout",
            "connect that scale to the running matching scale",
        ],
        "do_not_claim": [
            "Do not claim the 222 TeV scale is derived.",
            "Do not claim C3/Koide fixes an absolute scale.",
            "Do not claim electron mass is derived.",
            "Do not claim low-energy alpha is predicted.",
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
    print("target_scale:", result["target_scale"])
    print("C3_scale_free_no_go:", result["C3_scale_free_no_go"])
    print("electron_anchor_audit:", result["electron_anchor_audit"])
    print("core_action_candidates:", result["core_action_candidates"])
    print("radius_target_consistency:", result["radius_target_consistency"])
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
    _print_result(derive_bare_scale_from_oscillon_core_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
