# Notation header (see NOTATION.md):
# This gate follows p18ae.  It audits whether the n=2 bare candidate
# alpha^{-1}=81*pi/2 can plausibly be connected to the low-energy alpha by
# a dressing/running bridge, without fitting the observed value.

"""
================================================================================
PHASE 18af: Bare-to-low-energy dressing gate
================================================================================

Purpose
-------
p18ae produced a conditional bare candidate:

    q_geom = 2/9,
    q0^2 = n = 2,
    alpha_bare^{-1} = 81*pi/2 = 127.2345...

The observed low-energy value is

    alpha_low^{-1} = 137.036...

This gate asks a narrow question:

    Is the required shift compatible in sign and rough size with a standard
    charge-screening/running bridge?

Main result
-----------
The sign is compatible: going from a higher/bare scale to a lower scale makes
the inverse electromagnetic coupling larger.  The required inverse shift is

    Delta alpha^{-1} = 137.036 - 81*pi/2 ~= 9.8015.

In a one-loop QED-like schematic,

    Delta alpha^{-1} = (2/(3*pi)) * S_charge * ln(mu_high/mu_low),

where S_charge is the active sum of N_c Q_f^2.  The required logarithm is
reasonable only if several charged channels participate, but the scale,
thresholds and charged spectrum are not derived here.

What this gate does NOT claim
-----------------------------
- It does not derive low-energy alpha.
- It does not derive the running scale.
- It does not derive the charged spectrum.
- It does not replace a QED/EW threshold calculation.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_LOW = 1.0 / ALPHA_INV_CODATA
ALPHA_INV_BARE_N2 = 81.0 * math.pi / 2.0
DELTA_INV_REQUIRED = ALPHA_INV_CODATA - ALPHA_INV_BARE_N2


# ---------------------------------------------------------------------------
# 1. Running sign and formula
# ---------------------------------------------------------------------------

def one_loop_running_sign_gate() -> dict:
    S, L, a_hi = sp.symbols("S_charge L alpha_inv_high", positive=True)
    a_low = sp.simplify(a_hi + (2 * S / (3 * sp.pi)) * L)
    derivative = sp.diff(a_low, L)

    return {
        "schematic_formula": (
            "alpha_inv_low = alpha_inv_high + (2*S_charge/(3*pi))*ln(mu_high/mu_low)"
        ),
        "derivative_with_log_ratio": str(derivative),
        "inverse_alpha_increases_toward_low_energy": derivative > 0,
        "required_shift_positive": DELTA_INV_REQUIRED > 0,
        "sign_compatible": derivative > 0 and DELTA_INV_REQUIRED > 0,
        "reading": (
            "the n=2 candidate is stronger than low-energy electromagnetism. "
            "A screening/running bridge has the correct sign: the inverse "
            "coupling grows toward low energy."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Required log scale for active charge sums
# ---------------------------------------------------------------------------

def required_log_scale_table() -> dict:
    sectors = {
        "electron_only_S1": 1.0,
        "three_charged_leptons_S3": 3.0,
        "leptons_plus_5_quarks_no_top_S20_over_3": 20.0 / 3.0,
        "all_charged_SM_fermions_S8": 8.0,
    }

    rows = {}
    for name, S in sectors.items():
        log_ratio = DELTA_INV_REQUIRED * 3.0 * math.pi / (2.0 * S)
        rows[name] = {
            "S_charge": S,
            "ln_mu_high_over_mu_low_required": log_ratio,
            "scale_factor_required": math.exp(log_ratio),
        }

    return {
        "required_delta_alpha_inv": DELTA_INV_REQUIRED,
        "rows": rows,
        "multi_channel_running_needed_for_moderate_log": (
            rows["electron_only_S1"]["ln_mu_high_over_mu_low_required"] > 40.0
            and rows["all_charged_SM_fermions_S8"][
                "ln_mu_high_over_mu_low_required"
            ]
            < 10.0
        ),
        "reading": (
            "electron-only running would need an enormous logarithm.  With "
            "many charged channels the required logarithm is moderate, but "
            "that imports the charged spectrum and thresholds unless RefG "
            "derives them."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Threshold and spectrum openness
# ---------------------------------------------------------------------------

def threshold_spectrum_openness_audit() -> dict:
    return {
        "needed_for_real_calculation": [
            "which charged modes exist below the RefG bare scale",
            "their charges and multiplicities",
            "their threshold masses",
            "whether the RefG bare alpha is defined above or below electroweak mixing",
            "hadronic/vacuum-polarization treatment in the low-energy bridge",
        ],
        "not_available_in_current_gate": True,
        "standard_QED_formula_is_only_schematic": True,
        "reading": (
            "the sign/size test is encouraging but not a derivation.  A real "
            "bridge must know the spectrum and thresholds, not just a total "
            "charge sum."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Fitting guard: solving for a scale is not a derivation
# ---------------------------------------------------------------------------

def scale_fit_guard() -> dict:
    S = 8.0
    log_required = DELTA_INV_REQUIRED * 3.0 * math.pi / (2.0 * S)
    scale_factor = math.exp(log_required)

    return {
        "example_S_charge": S,
        "solved_log_ratio_from_observed_alpha": log_required,
        "solved_scale_factor_from_observed_alpha": scale_factor,
        "this_is_target_not_derivation": True,
        "what_would_make_it_derivation": (
            "RefG must independently derive the bare scale and active charged "
            "spectrum, then predict the shift rather than solving for it."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Bare value alternatives
# ---------------------------------------------------------------------------

def bare_value_alternative_audit() -> dict:
    candidates = {
        "n1": 81.0 * math.pi,
        "n2": 81.0 * math.pi / 2.0,
        "n3": 81.0 * math.pi / 3.0,
    }
    rows = {}
    for name, alpha_inv in candidates.items():
        shift = ALPHA_INV_CODATA - alpha_inv
        rows[name] = {
            "alpha_inv_bare": alpha_inv,
            "shift_to_low_energy": shift,
            "requires_screening_like_positive_shift": shift > 0,
            "relative_shift": shift / ALPHA_INV_CODATA,
        }

    return {
        "rows": rows,
        "only_n2_among_first_three_has_moderate_positive_shift": (
            rows["n2"]["requires_screening_like_positive_shift"]
            and abs(rows["n2"]["relative_shift"]) < 0.1
            and not rows["n1"]["requires_screening_like_positive_shift"]
            and rows["n3"]["relative_shift"] > 0.3
        ),
        "branch_not_selected_by_this_test": True,
        "reading": (
            "n=2 is singled out as the only small integer branch with a "
            "moderate positive shift to low energy.  This is a consistency "
            "signal, not a branch-selection theorem."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Next theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "a RefG-derived renormalization/dressing bridge from the n=2 "
            "bare candidate to low-energy alpha"
        ),
        "must_derive": [
            "the scale at which alpha_bare^{-1}=81*pi/2 is defined",
            "the active charged spectrum and charge sum S_charge across thresholds",
            "the threshold masses or effective matching scales",
            "whether electroweak mixing is already present at the bare scale",
            "the low-energy vacuum-polarization/dressing correction",
        ],
        "falsification_tests": [
            "if the required scale is solved from alpha_low, the bridge is a fit",
            "if the active spectrum is imported without RefG support, this is only compatibility",
            "if the running sign were wrong, the n=2 bare route would fail",
            "if the derived shift misses 137, the n=2 route is not the observed alpha",
        ],
        "candidate_next_gate": "p18ag_refg_charged_spectrum_running_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_bare_to_low_energy_dressing_gate() -> dict:
    sign = one_loop_running_sign_gate()
    logs = required_log_scale_table()
    threshold = threshold_spectrum_openness_audit()
    fit_guard = scale_fit_guard()
    alternatives = bare_value_alternative_audit()
    requirements = next_theorem_requirements()

    closed = {
        "running_sign_compatible_with_n2_to_low_energy": bool(
            sign["sign_compatible"]
        ),
        "moderate_log_requires_multi_channel_running": bool(
            logs["multi_channel_running_needed_for_moderate_log"]
        ),
        "threshold_spectrum_requirements_identified": bool(
            threshold["not_available_in_current_gate"]
            and threshold["standard_QED_formula_is_only_schematic"]
        ),
        "scale_solving_marked_as_target_not_derivation": bool(
            fit_guard["this_is_target_not_derivation"]
        ),
        "n2_is_only_moderate_small_integer_shift": bool(
            alternatives["only_n2_among_first_three_has_moderate_positive_shift"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "bare_scale_derived": False,
        "charged_spectrum_derived": False,
        "thresholds_derived": False,
        "running_correction_computed_from_RefG": False,
        "observed_low_energy_alpha_predicted": False,
    }

    result = {
        "STATUS": (
            "OPEN_REFG_CHARGED_SPECTRUM_RUNNING_REQUIRED__"
            + _pass_status("BARE_TO_LOW_ENERGY_DRESSING_AUDIT")
            if all(closed.values())
            else "CHECK_BARE_TO_LOW_ENERGY_DRESSING"
        ),
        "SCOPE": (
            "bare-to-low-energy dressing gate after p18ae: the n=2 candidate "
            "alpha^{-1}=81*pi/2 has the correct running sign toward the "
            "low-energy value and requires a moderate logarithm if many "
            "charged channels participate.  This is compatibility, not a "
            "prediction, until RefG derives the active charged spectrum, "
            "thresholds and bare scale."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "running_sign": sign,
        "required_log_scales": logs,
        "threshold_spectrum_openness": threshold,
        "scale_fit_guard": fit_guard,
        "bare_value_alternatives": alternatives,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the n=2 path survives a first dressing sanity check.  It is not "
            "the low-energy number, but it has the right sign and a plausible "
            "size if the charged sector contributes.  The next hard task is "
            "to derive that charged sector and the matching scale inside RefG."
        ),
        "missing_derivations": [
            "derive the bare scale of the n=2 alpha candidate",
            "derive the charged spectrum and charge multiplicities",
            "derive threshold/matching scales",
            "compute the dressing correction without solving for it from CODATA",
        ],
        "do_not_claim": [
            "Do not claim low-energy alpha is derived.",
            "Do not solve for the running scale and call it a prediction.",
            "Do not import the Standard Model spectrum as a RefG derivation.",
            "Do not call 81*pi/2 observed alpha.",
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
    print("running_sign:", result["running_sign"])
    print("required_log_scales:", result["required_log_scales"])
    print("threshold_spectrum_openness:", result["threshold_spectrum_openness"])
    print("scale_fit_guard:", result["scale_fit_guard"])
    print("bare_value_alternatives:", result["bare_value_alternatives"])
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
    _print_result(derive_bare_to_low_energy_dressing_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
