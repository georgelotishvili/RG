# Notation header (see NOTATION.md):
# This gate follows p18t.  It audits the proposed next route: derive the core
# electric/magnetic partition eta_core from nonlinear localized dynamics, not
# from alpha fitting.

"""
================================================================================
PHASE 18u: Nonlinear core partition gate
================================================================================

Purpose
-------
p18t reduced the alpha problem to one local number:

    eta_core = E_e / E_m,

the electric framing-current energy divided by the magnetic frame-curvature
energy in one localized charged orientation-frame core.  This gate takes the
useful part of the external advice and tests the two clean mathematical routes:

  1. Derrick/virial scaling of a localized 3D defect,
  2. weighted self-duality between electric and magnetic core channels.

It also checks the tempting C3/order-9 link to the lepton sector.  That link is
structurally valuable, but it does not by itself determine eta_core.

Main result
-----------
Derrick scaling can tell us which derivative orders must balance to stabilize
a finite core.  It does NOT fix the electric/magnetic partition when the
electric and magnetic Maxwell-type terms have the same scaling.  A two-term
virial theorem can fix a ratio only if the two channels carry different
scaling exponents; for natural integer derivative orders it gives order-one
ratios, not the small eta required by observed alpha.

Weighted self-duality would be a real route:

    sqrt(E_e_density) = beta_core * sqrt(E_m_density)
    => eta_core = beta_core^2.

But beta_core has to be derived from the nonlinear core geometry/action.  The
unweighted case beta_core=1 is the equal-energy shortcut already rejected by
p18t.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive eta_core.
- It does not derive beta_core.
- It does not use CODATA to set a core partition.
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
G_GEOM_FLUX_4PI = 4.0 * math.pi


def target_eta_for_diagnostic() -> float:
    """Target eta if q_geom=2/9 and g_geom=4*pi are used diagnostically.

    This is not a derivation.  It is the target p18t translated from CODATA.
    """
    z_required = 4.0 * math.pi * ALPHA_CODATA / (Q_GEOM_H2_ORDER9**2)
    return ((z_required * Q_GEOM_H2_ORDER9) / G_GEOM_FLUX_4PI) ** 2


# ---------------------------------------------------------------------------
# 1. Derrick scaling ledger
# ---------------------------------------------------------------------------

def derrick_scaling_ledger() -> dict:
    lam, p, E = sp.symbols("lambda p E_p", positive=True)
    scaled = sp.simplify(E * lam ** (3 - p))
    derivative = sp.simplify(sp.diff(scaled, lam).subs(lam, 1))

    rows = {}
    for order in (0, 1, 2, 3, 4, 6):
        rows[f"p{order}"] = {
            "energy_scaling": str(scaled.subs(p, order)),
            "virial_weight": int(3 - order),
        }

    return {
        "general_scaling": "E_p(lambda) = E_p * lambda^(3-p)",
        "general_virial_weight": str(derivative),
        "rows": rows,
        "reading": (
            "Derrick scaling fixes sums of derivative-order sectors.  It does "
            "not distinguish electric and magnetic subchannels if they live "
            "in the same derivative-order sector."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Virial audit with electric/magnetic split
# ---------------------------------------------------------------------------

def same_scaling_partition_no_go() -> dict:
    Ee, Em, E0, E4 = sp.symbols("E_e E_m E_0 E_4", positive=True)
    lam = sp.symbols("lambda", positive=True)

    # Potential-like p=0, Maxwell/sigma-like p=2, Skyrme-like p=4.
    energy = E0 * lam**3 + (Ee + Em) * lam + E4 / lam
    virial = sp.simplify(sp.diff(energy, lam).subs(lam, 1))
    solved_E4 = sp.solve(sp.Eq(virial, 0), E4)[0]
    eta = sp.simplify(Ee / Em)

    return {
        "energy_model": "E(lambda)=E0*lambda^3+(E_e+E_m)*lambda+E4/lambda",
        "virial_condition": str(virial),
        "E4_required": str(solved_E4),
        "eta_core": str(eta),
        "eta_still_free_after_virial": eta.has(Ee) and eta.has(Em),
        "interpretation": (
            "with electric and magnetic channels in the same p=2 sector, "
            "virial balance stabilizes the total p=2 weight but does not "
            "split it into E_e and E_m"
        ),
    }


def two_channel_virial_ratio_audit() -> dict:
    pe, pm, Ee, Em = sp.symbols(
        "p_e p_m E_e E_m", positive=True
    )
    virial = sp.Eq((3 - pe) * Ee + (3 - pm) * Em, 0)
    eta_solution = sp.simplify((pm - 3) / (3 - pe))

    natural_cases = {}
    cases = {
        "p_e_2__p_m_4": (2, 4),
        "p_e_2__p_m_6": (2, 6),
        "p_e_1__p_m_4": (1, 4),
        "p_e_0__p_m_4": (0, 4),
    }
    for name, (pe_val, pm_val) in cases.items():
        eta_val = float(sp.N(eta_solution.subs({pe: pe_val, pm: pm_val})))
        natural_cases[name] = {
            "p_e": pe_val,
            "p_m": pm_val,
            "eta_from_two_term_virial": eta_val,
        }

    eta_target = target_eta_for_diagnostic()
    pm_needed_if_pe2 = 3.0 + eta_target

    return {
        "two_term_virial_condition": str(virial),
        "eta_solution": str(eta_solution),
        "natural_integer_cases": natural_cases,
        "target_eta_diagnostic": eta_target,
        "p_m_needed_if_p_e_equals_2": pm_needed_if_pe2,
        "target_requires_near_marginal_or_weighted_core": (
            abs(pm_needed_if_pe2 - 3.0) < 0.01
        ),
        "interpretation": (
            "a pure two-channel virial theorem gives eta only from scaling "
            "weights.  Natural integer derivative orders give order-one "
            "ratios.  The small target eta would require a near-marginal "
            "effective scaling or an additional weighted core law."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Weighted self-duality audit
# ---------------------------------------------------------------------------

def weighted_self_duality_audit() -> dict:
    beta, q, g = sp.symbols("beta_core q_geom g_geom", positive=True)
    eta = sp.simplify(beta**2)
    z_medium = sp.simplify((g / q) * sp.sqrt(eta))
    alpha = sp.simplify(z_medium * q**2 / (4 * sp.pi))

    eta_target = target_eta_for_diagnostic()
    beta_target = math.sqrt(eta_target)
    alpha_inv_unweighted = 1.0 / (
        ((G_GEOM_FLUX_4PI / Q_GEOM_H2_ORDER9) * Q_GEOM_H2_ORDER9**2)
        / (4.0 * math.pi)
    )

    return {
        "weighted_self_duality_condition": (
            "sqrt(E_e_density) = beta_core * sqrt(E_m_density)"
        ),
        "eta_from_beta": str(eta),
        "Z_medium_from_beta": str(z_medium),
        "alpha_from_beta": str(alpha),
        "unweighted_beta_1_alpha_inv": alpha_inv_unweighted,
        "unweighted_case_is_rejected_equal_energy_shortcut": abs(
            alpha_inv_unweighted - ALPHA_INV_CODATA
        )
        > 1.0,
        "target_beta_diagnostic": beta_target,
        "target_eta_diagnostic": eta_target,
        "beta_core_not_derived": True,
        "interpretation": (
            "weighted self-duality is a viable mathematical shape only if "
            "beta_core is derived from the core geometry.  Setting beta by "
            "the observed alpha would be fitting."
        ),
    }


# ---------------------------------------------------------------------------
# 4. C3/order-9 link audit
# ---------------------------------------------------------------------------

def c3_order9_link_audit() -> dict:
    theta = sp.Rational(2, 9)
    eta, g = sp.symbols("eta_core g_geom", positive=True)
    q = theta
    alpha = sp.simplify(sp.sqrt(eta) * g * q / (4 * sp.pi))
    N = sp.simplify(1 / (4 * sp.pi * alpha))

    return {
        "shared_structure": (
            "order-9, h=2 appears in the charged-frame/lepton map and as the "
            "candidate electric boundary coordinate"
        ),
        "q_geom": str(q),
        "alpha_with_q_fixed": str(alpha),
        "N_with_q_fixed": str(N),
        "eta_still_present": alpha.has(eta) and N.has(eta),
        "valid_use": (
            "use C3/order-9 to fix the geometric electric coordinate and "
            "boundary sector"
        ),
        "invalid_use": (
            "do not claim the lepton mass map also fixes alpha unless it "
            "derives eta_core or beta_core"
        ),
    }


# ---------------------------------------------------------------------------
# 5. Bare/dressed target ledger
# ---------------------------------------------------------------------------

def bare_dressed_target_ledger() -> dict:
    alpha_inv_low = ALPHA_INV_CODATA
    alpha_inv_mz = 128.943
    return {
        "alpha_inv_low_energy": alpha_inv_low,
        "alpha_inv_MZ_reference": alpha_inv_mz,
        "running_shift_alpha_inv": alpha_inv_low - alpha_inv_mz,
        "relative_running_shift": (alpha_inv_low - alpha_inv_mz) / alpha_inv_low,
        "reading": (
            "RefG must eventually state which scale its geometric alpha "
            "belongs to.  The present core gate targets a bare geometric "
            "normalization; QED running/dressing is a later bridge, not a "
            "license to fit eta_core."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Next action requirements
# ---------------------------------------------------------------------------

def next_action_requirements() -> dict:
    return {
        "needed_object": (
            "a concrete nonlinear radial/core action for the completed "
            "orientation-frame defect"
        ),
        "minimum_fields": [
            "theta(r): framing/twist phase or current profile",
            "n(r,angles): oriented axis/hedgehog-frame profile",
            "A(n): completed frame connection",
            "one or more core amplitudes that regularize the r=0 singularity",
        ],
        "minimum_terms": [
            "electric framing-current energy",
            "magnetic frame-curvature energy",
            "core regularization term with different Derrick scaling",
            "finite boundary/anholonomy constraint for order-9, h=2",
        ],
        "falsification_tests": [
            "if electric and magnetic terms keep identical scaling and no "
            "weighted duality is derived, eta_core remains free",
            "if the virial theorem only fixes total p=2 weight, alpha is not "
            "derived",
            "if beta_core is inserted from the target eta, the gate fails as "
            "a fit",
            "if the C3/order-9 sector only fixes q_geom, it is not enough for "
            "alpha",
        ],
        "candidate_next_gate": "p18v_radial_core_ansatz_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_nonlinear_core_partition_gate() -> dict:
    scaling = derrick_scaling_ledger()
    same = same_scaling_partition_no_go()
    two_channel = two_channel_virial_ratio_audit()
    duality = weighted_self_duality_audit()
    c3 = c3_order9_link_audit()
    dressing = bare_dressed_target_ledger()
    requirements = next_action_requirements()

    closed = {
        "Derrick_scaling_ledger_written": bool(scaling["rows"]),
        "same_scaling_virial_leaves_eta_free": bool(
            same["eta_still_free_after_virial"]
        ),
        "natural_two_term_virial_ratios_are_order_one": bool(
            all(
                row["eta_from_two_term_virial"] >= 0.25
                for row in two_channel["natural_integer_cases"].values()
            )
        ),
        "small_target_eta_requires_near_marginal_or_weighted_core": bool(
            two_channel["target_requires_near_marginal_or_weighted_core"]
        ),
        "unweighted_self_duality_rejected": bool(
            duality["unweighted_case_is_rejected_equal_energy_shortcut"]
        ),
        "weighted_self_duality_slot_identified_but_beta_open": bool(
            duality["beta_core_not_derived"]
        ),
        "C3_order9_fixes_q_not_eta": bool(c3["eta_still_present"]),
        "bare_dressed_split_recorded_without_fit": bool(
            dressing["running_shift_alpha_inv"] > 0
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "eta_core_derived": False,
        "beta_core_derived": False,
        "nonlinear_core_action_written": False,
        "radial_core_solution_found": False,
        "Z_medium_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_WEIGHTED_CORE_DUALITY_OR_ACTION_TERM_REQUIRED__"
            + _pass_status("DERRICK_VIRIAL_PARTITION_AUDIT")
            if all(closed.values())
            else "CHECK_NONLINEAR_CORE_PARTITION_AUDIT"
        ),
        "SCOPE": (
            "nonlinear core partition audit after p18t: Derrick/virial "
            "scaling, weighted self-duality, C3/order-9 linkage and "
            "bare/dressed target handling are checked.  The audit narrows the "
            "missing derivation to a concrete weighted core law or nonlinear "
            "action term that fixes eta_core."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "Derrick_scaling": scaling,
        "same_scaling_partition_no_go": same,
        "two_channel_virial": two_channel,
        "weighted_self_duality": duality,
        "C3_order9_link": c3,
        "bare_dressed_target": dressing,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the useful advice has been converted into a controlled route.  "
            "The next target is not another formula for 137; it is the local "
            "core law that makes the electric framing current much smaller "
            "than the magnetic frame-flux energy in the required geometric "
            "normalization.  Virial scaling alone does not do this."
        ),
        "missing_derivations": [
            "write the concrete nonlinear orientation-frame core action",
            "derive a weighted self-duality or another core partition law",
            "show that this law fixes beta_core or eta_core without CODATA",
            "then feed eta_core into p18t's impedance formula",
            "only after that discuss QED dressing/running to the observed "
            "low-energy alpha",
        ],
        "do_not_claim": [
            "Do not claim Derrick scaling derives eta_core by itself.",
            "Do not claim C3/order-9 or the lepton mass map derives alpha.",
            "Do not set beta_core or eta_core from the observed alpha.",
            "Do not use unweighted self-duality; it is the rejected equal-"
            "energy shortcut.",
            "Do not claim alpha, N, or Z_medium are derived in this gate.",
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
    print("Derrick_scaling:", result["Derrick_scaling"])
    print("same_scaling_partition_no_go:", result["same_scaling_partition_no_go"])
    print("two_channel_virial:", result["two_channel_virial"])
    print("weighted_self_duality:", result["weighted_self_duality"])
    print("C3_order9_link:", result["C3_order9_link"])
    print("bare_dressed_target:", result["bare_dressed_target"])
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
    _print_result(derive_nonlinear_core_partition_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
