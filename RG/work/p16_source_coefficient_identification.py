# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16: Source/coefficient identification gate.

This file tests whether the compact branch selector can replace abstract
``S`` and ``chi`` by physical inputs and action coefficients.

Closed by existing work:
  * p10 fixes the exterior source coefficient by asymptotic charge:
    ``mu_src = 2 G M / c^2``.
  * p05y fixes the static selected load once ``S`` and ``chi`` are supplied.
  * p14 gives a stable one-variable deficit feedback for positive ``S, chi``.

Open here:
  * the map from a compact object/EOS to ``S`` is not derived;
  * the map from ``c_Y, c_Y2, c_YI1, omega_Delta`` to ``chi`` is not derived.

The gate therefore does not claim that the dynamical branch-selection gap is
closed.  It records the exact obstruction.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp

from p16f_compactness_band_source_map import (
    derive_stated_compactness_class_source_map,
)


def derive_source_coefficient_identification_gate() -> dict[str, Any]:
    """Identify what is physical and what remains an undetermined response."""
    G, M, c, R_source = sp.symbols("G M c R_source", positive=True, real=True)
    Q, S, chi = sp.symbols("Q S chi", positive=True, real=True)
    c_Y, c_Y2, c_YI1, omega_Delta = sp.symbols(
        "c_Y c_Y2 c_YI1 omega_Delta",
        real=True,
    )

    r = sp.symbols("r", positive=True, real=True)
    mu_symbol = sp.Symbol("mu_src", positive=True, real=True)
    mu_src = sp.simplify(2 * G * M / c**2)
    C0 = sp.simplify(mu_src / R_source)
    phi = -mu_symbol / r
    phi_newton = sp.simplify(c**2 * phi / 2)
    acceleration = sp.simplify(-sp.diff(phi_newton, r))
    mu_needed = sp.solve(sp.Eq(acceleration, -G * M / r**2), mu_symbol)[0]

    q_v = sp.simplify(sp.Rational(3, 2) * Q)
    S_required = sp.simplify(q_v * sp.exp(chi * q_v))
    dS_dQ = sp.factor(sp.diff(S_required, Q))
    Q_selected = sp.simplify(sp.Rational(2, 3) * sp.LambertW(chi * S) / chi)
    q_selected = sp.simplify(sp.LambertW(chi * S) / chi)
    selector_residual = sp.simplify(
        q_selected - S * sp.exp(-chi * q_selected)
    ).subs(
        S * sp.exp(-sp.LambertW(chi * S)),
        sp.LambertW(chi * S) / chi,
    )
    clock_residual = sp.simplify(sp.Rational(3, 2) * Q_selected - q_selected)
    S_window_lower = sp.simplify(S_required.subs(Q, 1))
    S_window_upper = sp.simplify(S_required.subs(Q, 2))

    feedback_rhs = sp.simplify(S * sp.exp(-chi * q_selected) - q_selected)
    feedback_identity = sp.simplify(
        feedback_rhs.subs(
            S * sp.exp(-sp.LambertW(chi * S)),
            sp.LambertW(chi * S) / chi,
        )
    )
    chi_mass_only = sp.Rational(1, 2)

    closed_checks = {
        "p10_mu_src_charge_normalization_reproduced": sp.simplify(mu_src - mu_needed) == 0,
        "p05y_static_source_selector_reproduced": selector_residual == 0,
        "surface_clock_residual_zero": clock_residual == 0,
        "source_required_monotone_for_positive_inputs": dS_dQ.is_positive,
        "p14_feedback_identity_reproduced_given_S_chi": feedback_identity == 0,
    }
    open_checks = {
        "arbitrary_S_as_function_of_C0_or_rho_c_and_mu_src": False,
        "chi_as_function_of_action_coefficients": False,
        "arbitrary_EOS_one_input_source_map": False,
    }
    stated_class = derive_stated_compactness_class_source_map()

    return {
        "STATUS": "OPEN_SOURCE_COEFFICIENT_IDENTIFICATION__PASS_STATIC_INPUTS__S_CHI_MAP_MISSING",
        "STATED_CLASS_STATUS": stated_class["STATUS"],
        "SCOPE": (
            "Algebraic identification gate only.  It proves the asymptotic "
            "source coefficient and static selector formulas, but it does not "
            "derive an EOS/action coefficient map for S and chi."
        ),
        "closed_checks": closed_checks,
        "open_checks": open_checks,
        "mu_src_from_asymptotic_charge": sp.Eq(sp.Symbol("mu_src"), mu_src),
        "compactness_input": sp.Eq(sp.Symbol("C0"), C0),
        "surface_clock_matching": sp.Eq(sp.Symbol("q_v"), q_v),
        "S_required_for_selected_load": sp.Eq(
            sp.Symbol("S_required_Q_chi"),
            S_required,
        ),
        "S_required_derivative": sp.Eq(sp.Symbol("dS_required_dQ"), dS_dQ),
        "selected_Q_from_S_chi": sp.Eq(sp.Symbol("Q_selected"), Q_selected),
        "selector_residual": selector_residual,
        "clock_residual": clock_residual,
        "compact_window_Q": sp.And(Q > 1, Q < 2),
        "compact_window_S_given_chi": sp.And(
            S > S_window_lower,
            S < S_window_upper,
        ),
        "S_window_lower_Q1": S_window_lower,
        "S_window_upper_Q2": S_window_upper,
        "action_coefficients_requested": [c_Y, c_Y2, c_YI1, omega_Delta],
        "chi_mass_scaling_only_reference": sp.Eq(sp.Symbol("chi_mass"), chi_mass_only),
        "existing_work_references": [
            "p10_oscillons.py: poisson_to_newton_normalization_gate",
            "p05y_source_amplitude_branch_selector_theorem.py",
            "p14_nec_deficit.py: mass_deficit_feedback_balance_gate",
            "p05x_branch_selection_defect_response_gate.py",
        ],
        "stated_class_source_map": {
            "compactness_band_C0": stated_class["compactness_band_C0"],
            "source_map": stated_class["source_map"],
            "volume_response_chi": stated_class["volume_response_chi"],
            "sample_realizing_point": stated_class["sample_realizing_point"],
            "scope": stated_class["SCOPE"],
        },
        "missing_derivations": [
            "derive S(C0 or rho_c, mu_src) for arbitrary EOS/collapse histories",
            "derive chi(c_Y, c_Y2, c_YI1, omega_Delta) from the action response",
            "upgrade the stated volume-response class to a full action-coefficient theorem",
        ],
        "do_not_claim": [
            "do not claim arbitrary EOS objects land in 1<Q<2",
            "do not claim chi is fixed by the action coefficients here",
            "do not claim full nonlinear collapse is solved",
            "do not remove global conditional wording from compact predictions",
        ],
    }


def _print_result(result: dict[str, Any]) -> None:
    print("STATUS:", result["STATUS"])
    print("STATED_CLASS_STATUS:", result["STATED_CLASS_STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, value in result["closed_checks"].items():
        print(f"  - {key}: {value}")
    print("open_checks:")
    for key, value in result["open_checks"].items():
        print(f"  - {key}: {value}")
    for key in (
        "mu_src_from_asymptotic_charge",
        "compactness_input",
        "surface_clock_matching",
        "S_required_for_selected_load",
        "S_required_derivative",
        "selected_Q_from_S_chi",
        "selector_residual",
        "clock_residual",
        "compact_window_Q",
        "compact_window_S_given_chi",
        "S_window_lower_Q1",
        "S_window_upper_Q2",
        "chi_mass_scaling_only_reference",
        "stated_class_source_map",
    ):
        print(f"{key}: {result[key]}")
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
    _print_result(derive_source_coefficient_identification_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
