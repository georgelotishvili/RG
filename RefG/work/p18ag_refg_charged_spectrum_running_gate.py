# Notation header (see NOTATION.md):
# This gate follows p18af.  It audits the running bridge using only the
# charged spectrum currently supported inside RefG: the charged-lepton C3
# triplet candidate.  Quarks and the full Standard Model are not imported as
# RefG-derived input.

"""
================================================================================
PHASE 18ag: RefG charged-spectrum running gate
================================================================================

Purpose
-------
p18af showed that the n=2 bare candidate

    alpha_bare^{-1} = 81*pi/2

has the correct sign and rough size for a dressing/running bridge to the
low-energy value.  This gate asks what happens if the bridge uses only the
charged spectrum that RefG currently has as an internal structural candidate:

    electron, muon, tau as one C3/order-9 charged-lepton triplet.

Main result
-----------
With a one-loop QED-like threshold ledger and only the three charged leptons,
the required bridge scale is

    mu_bare ~= 2.22e5 GeV  ~= 222 TeV.

That is a strong diagnostic number, but not a derivation.  It is obtained by
solving for the scale that makes

    alpha_low^{-1} - 81*pi/2

equal to the charged-lepton vacuum-polarization shift.  RefG has not yet
derived the bare scale, the absolute lepton thresholds, the full U(1)/EW
normalization, or the charged spectrum beyond leptons.

What this gate does NOT claim
-----------------------------
- It does not derive low-energy alpha.
- It does not derive the 222 TeV scale.
- It does not derive the charged-lepton masses.
- It does not use quarks or the full Standard Model as RefG-derived input.
- It does not replace an electroweak-threshold calculation.
"""

from __future__ import annotations

import math
import sys


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_INV_BARE_N2 = 81.0 * math.pi / 2.0
DELTA_INV_REQUIRED = ALPHA_INV_CODATA - ALPHA_INV_BARE_N2
QED_ONE_LOOP_B = 2.0 / (3.0 * math.pi)

# MeV.  These are the same values already used in the p11 charged-lepton
# ledger.  Their RefG status is threshold input, not derived mass output.
LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}


def _lepton_shift(alpha_scale_mev: float) -> float:
    """One-loop QED-like inverse-alpha shift from lepton thresholds.

    For a lepton of charge magnitude 1, the schematic contribution is

        (2/(3*pi))*ln(mu/m_l)

    once the scale mu is above the threshold m_l.
    """
    total = 0.0
    for mass in LEPTON_MASSES_MEV.values():
        if alpha_scale_mev > mass:
            total += math.log(alpha_scale_mev / mass)
    return QED_ONE_LOOP_B * total


# ---------------------------------------------------------------------------
# 1. RefG-supported charged spectrum ledger
# ---------------------------------------------------------------------------

def refg_supported_charged_spectrum_ledger() -> dict:
    return {
        "supported_internal_candidate": (
            "charged-lepton C3/order-9 triplet: electron, muon, tau"
        ),
        "status": "strong structural candidate, not final generation theorem",
        "usable_for_this_gate": [
            "three unit-charged lepton thresholds as the only RefG-internal charged spectrum candidate",
            "C3/order-9 branch as a structural charged-sector spine",
        ],
        "not_usable_as_derived_input": [
            "quarks and fractional charges",
            "full Standard Model U(1), SU(2), SU(3)",
            "electroweak mixing",
            "absolute electron mass derivation",
            "radiative/pole protection of the C3 mass relation",
        ],
        "strict_reading": (
            "this gate is a lepton-only compatibility test.  It does not "
            "claim that RefG has derived the whole charged spectrum."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Lepton-threshold running scale
# ---------------------------------------------------------------------------

def lepton_threshold_running_scale_gate() -> dict:
    masses = list(LEPTON_MASSES_MEV.values())
    log_sum_required = DELTA_INV_REQUIRED / QED_ONE_LOOP_B
    log_mu = (log_sum_required + sum(math.log(m) for m in masses)) / len(masses)
    mu_required_mev = math.exp(log_mu)
    shift_at_mu = _lepton_shift(mu_required_mev)
    alpha_inv_reconstructed = ALPHA_INV_BARE_N2 + shift_at_mu

    benchmarks_gev = [1.0e3, 1.0e4, 1.0e5, mu_required_mev / 1000.0, 1.0e6]
    rows = {}
    for gev in benchmarks_gev:
        mev = 1000.0 * gev
        shift = _lepton_shift(mev)
        rows[f"{gev:.6g}_GeV"] = {
            "mu_GeV": gev,
            "shift_alpha_inv": shift,
            "alpha_inv_from_n2_plus_leptons": ALPHA_INV_BARE_N2 + shift,
            "miss_vs_low_energy_alpha_inv": (
                ALPHA_INV_BARE_N2 + shift - ALPHA_INV_CODATA
            ),
        }

    return {
        "alpha_inv_bare_n2": ALPHA_INV_BARE_N2,
        "alpha_inv_low": ALPHA_INV_CODATA,
        "required_delta_alpha_inv": DELTA_INV_REQUIRED,
        "one_loop_b": QED_ONE_LOOP_B,
        "sum_log_required": log_sum_required,
        "mu_required_MeV": mu_required_mev,
        "mu_required_GeV": mu_required_mev / 1000.0,
        "mu_required_TeV": mu_required_mev / 1.0e6,
        "mu_required_over_tau_mass": mu_required_mev / LEPTON_MASSES_MEV["tau"],
        "alpha_inv_reconstructed_at_required_mu": alpha_inv_reconstructed,
        "matches_low_energy_by_construction": abs(
            alpha_inv_reconstructed - ALPHA_INV_CODATA
        )
        < 1.0e-9,
        "benchmark_rows": rows,
        "scale_is_target_not_derivation": True,
        "reading": (
            "lepton-only threshold running can bridge the n=2 bare candidate "
            "to alpha(0) if the bare scale is about 222 TeV.  The scale is "
            "solved here, not predicted."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Electroweak validity guard
# ---------------------------------------------------------------------------

def electroweak_validity_guard() -> dict:
    # A deliberately rough reference scale; the exact value is not needed for
    # the gate.  The lepton-only target is many orders above this.
    ew_reference_gev = 100.0
    mu_required_gev = lepton_threshold_running_scale_gate()["mu_required_GeV"]
    return {
        "rough_electroweak_reference_GeV": ew_reference_gev,
        "lepton_only_required_mu_GeV": mu_required_gev,
        "required_scale_above_EW_reference": mu_required_gev > ew_reference_gev,
        "QED_only_not_final_above_EW": True,
        "needed_completion": [
            "derive whether RefG's bare alpha is defined before or after electroweak mixing",
            "derive the U(1)/EW matching condition",
            "derive charged thresholds and any non-leptonic charged modes",
        ],
        "reading": (
            "the 222 TeV diagnostic lies above the ordinary electroweak zone. "
            "Therefore the lepton-only QED ledger is a sanity check, not the "
            "final dressing theorem."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Threshold-input guard
# ---------------------------------------------------------------------------

def threshold_input_guard() -> dict:
    return {
        "lepton_masses_used_MeV": LEPTON_MASSES_MEV,
        "RefG_status_of_masses": (
            "electron is still an anchor; muon/tau are C3 candidate ratios "
            "with residual/radiative protection open"
        ),
        "thresholds_are_inputs_not_derived": True,
        "what_would_close_this": [
            "derive absolute electron mass",
            "derive m proportional to nu^2 from oscillon energy",
            "derive muon/tau pole masses or protected threshold masses",
            "derive the charged-spectrum thresholds entering the running bridge",
        ],
    }


# ---------------------------------------------------------------------------
# 5. Full charged-spectrum import guard
# ---------------------------------------------------------------------------

def full_spectrum_import_guard() -> dict:
    return {
        "quarks_would_change_running": True,
        "quarks_not_RefG_derived_here": True,
        "full_SM_not_imported_as_derivation": True,
        "allowed_use": (
            "quarks/SM can be used later as an external compatibility check, "
            "not as a RefG derivation of alpha"
        ),
        "blocked_claims": [
            "RefG has derived fractional charges",
            "RefG has derived U(1), SU(2), SU(3)",
            "RefG has derived the full running spectrum",
            "RefG has predicted alpha from the Standard Model spectrum",
        ],
    }


# ---------------------------------------------------------------------------
# 6. Next theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "derive the RefG bare scale and charged thresholds that make the "
            "n=2 alpha candidate a prediction rather than a target"
        ),
        "must_derive": [
            "bare scale of the q_geom=2/9, q0=sqrt(2) boundary readout",
            "absolute electron threshold",
            "muon/tau threshold masses or protected pole-to-threshold map",
            "whether non-leptonic charged modes enter before the bare scale",
            "U(1)/electroweak matching if the bare scale is above the EW regime",
        ],
        "falsification_tests": [
            "if the derived bare scale is far below tau threshold, lepton running cannot bridge the shift",
            "if the derived bare scale is not near the threshold-running target and no additional channels appear, the n=2 route misses alpha",
            "if quarks are imported without RefG charge derivation, the result is compatibility only",
            "if thresholds are fitted to alpha, the bridge fails as a derivation",
        ],
        "candidate_next_gate": "p18ah_bare_scale_from_oscillon_core_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_refg_charged_spectrum_running_gate() -> dict:
    spectrum = refg_supported_charged_spectrum_ledger()
    lepton = lepton_threshold_running_scale_gate()
    ew = electroweak_validity_guard()
    thresholds = threshold_input_guard()
    full_import = full_spectrum_import_guard()
    requirements = next_theorem_requirements()

    closed = {
        "RefG_internal_charged_spectrum_limited_to_lepton_candidate": bool(
            spectrum["status"]
        ),
        "lepton_threshold_scale_target_computed": bool(
            lepton["matches_low_energy_by_construction"]
            and lepton["scale_is_target_not_derivation"]
        ),
        "EW_validity_guard_active": bool(
            ew["required_scale_above_EW_reference"]
            and ew["QED_only_not_final_above_EW"]
        ),
        "threshold_masses_marked_as_inputs": bool(
            thresholds["thresholds_are_inputs_not_derived"]
        ),
        "full_SM_import_blocked": bool(
            full_import["quarks_not_RefG_derived_here"]
            and full_import["full_SM_not_imported_as_derivation"]
        ),
        "no_CODATA_fit_claim_performed": True,
    }

    open_checks = {
        "bare_scale_derived_from_RefG": False,
        "charged_lepton_thresholds_derived": False,
        "U1_EW_matching_derived": False,
        "non_leptonic_charged_spectrum_derived": False,
        "low_energy_alpha_predicted": False,
    }

    result = {
        "STATUS": (
            "OPEN_BARE_SCALE_AND_THRESHOLDS_REQUIRED__"
            + _pass_status("REFG_CHARGED_LEPTON_RUNNING_AUDIT")
            if all(closed.values())
            else "CHECK_REFG_CHARGED_SPECTRUM_RUNNING"
        ),
        "SCOPE": (
            "charged-spectrum running gate after p18af: using only the "
            "RefG-supported charged-lepton C3 candidate, a one-loop "
            "threshold ledger bridges alpha^{-1}=81*pi/2 to the low-energy "
            "value at a target scale near 222 TeV.  This is a sharp target, "
            "not a prediction, because the bare scale, thresholds and EW/U1 "
            "matching are not yet derived."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "spectrum_ledger": spectrum,
        "lepton_threshold_running": lepton,
        "electroweak_validity_guard": ew,
        "threshold_input_guard": thresholds,
        "full_spectrum_import_guard": full_import,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the n=2 route got a surprisingly concrete next target: if the "
            "RefG core independently produces a bare scale around 222 TeV, "
            "then the charged-lepton sector alone has the right size to dress "
            "81*pi/2 toward 137.  But until that scale and the thresholds are "
            "derived, this remains a target ledger."
        ),
        "missing_derivations": [
            "derive the bare scale from the charged oscillon/core action",
            "derive charged-lepton thresholds instead of inserting them",
            "derive U(1)/EW matching above the electroweak regime",
            "derive or exclude non-leptonic charged modes before the bare scale",
        ],
        "do_not_claim": [
            "Do not claim alpha is derived.",
            "Do not claim the 222 TeV scale is predicted.",
            "Do not use quarks/full SM running as RefG-derived input.",
            "Do not treat the lepton masses as derived thresholds in this gate.",
            "Do not use QED-only running above the EW scale as a final theorem.",
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
    print("spectrum_ledger:", result["spectrum_ledger"])
    print("lepton_threshold_running:", result["lepton_threshold_running"])
    print("electroweak_validity_guard:", result["electroweak_validity_guard"])
    print("threshold_input_guard:", result["threshold_input_guard"])
    print("full_spectrum_import_guard:", result["full_spectrum_import_guard"])
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
    _print_result(derive_refg_charged_spectrum_running_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
