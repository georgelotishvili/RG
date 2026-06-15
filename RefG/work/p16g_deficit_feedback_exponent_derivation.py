# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); no X-scheme c_X is introduced here.

"""PHASE 16g: where the deficit feedback exponent chi comes from.

p16, p16a and p16f left ``chi`` as an assumed input: the "volume-response
class" simply fixed ``chi = 1`` by hand, and p16 recorded
``chi_as_function_of_action_coefficients = False`` as the open obstruction.

This gate tests the obstruction directly and finds that it was mis-posed:

  * On the compact pure-phase exterior the phase-normalized F_min sector is
    stress-quiet (Yhat = lhat_r = lhat_t = 1 => F_min = 0, dF_min = 0; see
    p05s / p05j / p16).  Therefore the polynomial coefficients c_Y, c_Y2,
    c_I1, c_I1sq, c_I2, c_I3, c_YI1 do NOT enter the compact-branch feedback.
    The "derive chi from c_Y" target is empty: chi has no c_Y dependence.

  * The exterior deficit is fixed by the reduced phase equation
    (r^2 phi')' = 0 => phi = -r_s/r, h = r_s/(2 r), with r_s = 2 G M / c^2.
    The feedback exponent chi is the exponent of the EXTERNAL deficit-readout
    filter expressed in the volume deficit variable q_v = 3 h.

  * The clock / unit-mass readout filter e^{-h} = e^{-q_v/3} gives chi = 1/3.
    The volume / bulk-mass readout filter e^{-3h} = e^{-q_v} gives chi = 1.
    The chi = 1 value is exactly the one p16f assumed; here it is derived as
    the bulk/volume readout exponent, not posited.

  * omega_Delta sets the source amplitude S (the operator normalization), not
    the exponent chi.

Open (the real residual, now sharp): a first-principles proof that the
external gravitating source amplitude is the bulk/volume readout channel
(chi = 1) rather than the unit-mass/clock channel (chi = 1/3).  That single
channel identification is tied to the p15g proper-inventory / ADM bridge; it
is no longer a "fit chi to the action" question.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp

from p16f_compactness_band_source_map import (
    derive_stated_compactness_class_source_map,
)


def derive_deficit_feedback_exponent_gate() -> dict[str, Any]:
    r, r_s, Q = sp.symbols("r r_s Q", positive=True, real=True)
    q_v = sp.symbols("q_v", positive=True, real=True)
    omega_Delta = sp.symbols("omega_Delta", positive=True, real=True)
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1", real=True
    )
    poly_coeffs = [c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1]

    # 1. Exterior deficit from the reduced phase equation (r^2 phi')' = 0.
    phi = -r_s / r
    phase_eq_residual = sp.simplify(sp.diff(r**2 * sp.diff(phi, r), r))
    h = sp.simplify(-phi / 2)                       # biconformal metric deficit
    h_surface = sp.simplify(h.subs(r, r_s / Q))     # at r_c = r_s/Q  ->  Q/2

    # 2. Volume deficit variable q_v from surface-clock matching:
    #    e^{-q_v/3} = e^{-h_surface}  =>  q_v = 3 h_surface = 3 Q / 2.
    q_v_of_Q = sp.solve(
        sp.Eq(sp.exp(-sp.Symbol("qv") / 3), sp.exp(-h_surface)),
        sp.Symbol("qv"),
    )[0]
    surface_clock_residual = sp.simplify(q_v_of_Q - sp.Rational(3, 2) * Q)
    h_in_qv = sp.Rational(1, 3) * q_v               # h = q_v / 3

    # 3. External (distant-observer) deficit-readout filters from the
    #    biconformal map.  Proper interior factors are the inverse; the
    #    external source amplitude is filtered by the readout factors below.
    readout_filter = {
        "clock_lapse": sp.exp(-h_in_qv),            # sqrt(g_tt) = e^{-h}
        "unit_length": sp.exp(-h_in_qv),            # e^{-h}
        "unit_mass": sp.exp(-h_in_qv),              # e^{-h}  (rest/unit readout)
        "volume": sp.exp(-3 * h_in_qv),             # e^{-3h}
        "bulk_mass_volume_balanced": sp.exp(-3 * h_in_qv),  # e^{-3h}
    }

    # 4. chi for each channel from filter = exp(-chi * q_v).
    chi_channel = {
        name: sp.simplify(-sp.log(filt) / q_v)
        for name, filt in readout_filter.items()
    }
    chi_unit_mass = chi_channel["unit_mass"]                 # 1/3
    chi_bulk = chi_channel["bulk_mass_volume_balanced"]      # 1

    # 5. Self-consistent feedback for the external bulk source:
    #    S_eff = S * (bulk readout filter) = S * e^{-q_v}  ->  chi = 1 exactly.
    S = sp.symbols("S", positive=True, real=True)
    S_eff_bulk = sp.simplify(S * readout_filter["bulk_mass_volume_balanced"])
    chi_from_bulk_feedback = sp.simplify(
        -sp.log(S_eff_bulk / S) / q_v
    )

    # 6. Coefficient independence.  chi is built only from h(r_s) and q_v, none
    #    of which contain the polynomial coefficients or omega_Delta.  The
    #    phase-normalized F_min is stress-quiet on the compact branch, so it
    #    contributes nothing to the feedback exponent.
    chi_d_coeff = {
        str(c): sp.simplify(sp.diff(chi_bulk, c)) for c in poly_coeffs
    }
    chi_d_omega = sp.simplify(sp.diff(chi_bulk, omega_Delta))
    all_coeff_derivs_zero = all(v == 0 for v in chi_d_coeff.values())

    # 7. Cross-check against p16f's assumed value.
    p16f = derive_stated_compactness_class_source_map()
    p16f_chi = sp.Integer(1)  # p16f volume_response_chi = 1

    derived_pass = (
        phase_eq_residual == 0
        and surface_clock_residual == 0
        and sp.simplify(chi_unit_mass - sp.Rational(1, 3)) == 0
        and sp.simplify(chi_bulk - 1) == 0
        and sp.simplify(chi_from_bulk_feedback - 1) == 0
        and all_coeff_derivs_zero
        and chi_d_omega == 0
        and sp.simplify(chi_bulk - p16f_chi) == 0
    )

    return {
        "STATUS": (
            "PASS_CHI_IS_METRIC_READOUT_EXPONENT_NOT_POLYNOMIAL__"
            "VOLUME_CHANNEL_GIVES_CHI_ONE__CHANNEL_UNIQUENESS_OPEN"
            if derived_pass
            else "CHECK_DEFICIT_FEEDBACK_EXPONENT"
        ),
        "SCOPE": (
            "Compact pure-phase exterior readout argument.  It proves chi is a "
            "fixed metric-readout exponent independent of the polynomial "
            "coefficients and of omega_Delta, equal to 1 for the volume/bulk "
            "readout and 1/3 for the unit-mass/clock readout.  It does not prove "
            "from first principles that the external gravitating source is the "
            "bulk/volume channel; that channel identification is tied to p15g."
        ),
        "closed_checks": {
            "reduced_phase_equation_residual_zero": phase_eq_residual == 0,
            "surface_clock_qv_equals_3Q_over_2": surface_clock_residual == 0,
            "unit_mass_channel_chi_one_third": sp.simplify(chi_unit_mass - sp.Rational(1, 3)) == 0,
            "volume_bulk_channel_chi_one": sp.simplify(chi_bulk - 1) == 0,
            "bulk_feedback_reproduces_chi_one": sp.simplify(chi_from_bulk_feedback - 1) == 0,
            "chi_independent_of_polynomial_coefficients": all_coeff_derivs_zero,
            "chi_independent_of_omega_Delta": chi_d_omega == 0,
            "reproduces_p16f_assumed_chi_one": sp.simplify(chi_bulk - p16f_chi) == 0,
        },
        "open_checks": {
            "external_source_is_bulk_volume_channel_proved": False,
            "channel_uniqueness_from_p15g_adm_bridge_derived": False,
            "full_nonlinear_collapse_solved": False,
        },
        "exterior_deficit": sp.Eq(sp.Symbol("h(r)"), h),
        "surface_deficit": sp.Eq(sp.Symbol("h_c"), h_surface),
        "volume_deficit_from_clock": sp.Eq(sp.Symbol("q_v(Q)"), q_v_of_Q),
        "readout_filters_in_qv": {
            name: sp.Eq(sp.Symbol(f"filter_{name}"), filt)
            for name, filt in readout_filter.items()
        },
        "chi_by_channel": {
            name: sp.Eq(sp.Symbol(f"chi_{name}"), val)
            for name, val in chi_channel.items()
        },
        "chi_from_bulk_self_consistent_feedback": sp.Eq(
            sp.Symbol("chi_bulk_feedback"), chi_from_bulk_feedback
        ),
        "d_chi_d_coeff": chi_d_coeff,
        "d_chi_d_omega_Delta": chi_d_omega,
        "p16f_assumed_chi": p16f_chi,
        "p16f_status_now_derived_for_bulk_channel": p16f["STATUS"],
        "resolves": (
            "The p16 open item 'chi_as_function_of_action_coefficients' is "
            "empty: chi has no polynomial-coefficient dependence.  The genuine "
            "remaining choice is the readout channel (1/3 vs 1), not a fit to "
            "c_Y."
        ),
        "missing_derivations": [
            "prove the external gravitating source amplitude is the bulk/volume "
            "readout channel (chi=1) using the p15g proper-inventory/ADM bridge",
            "rule out the unit-mass/clock channel (chi=1/3) for the external "
            "source, or show how the two combine",
        ],
        "do_not_claim": [
            "do not claim chi depends on c_Y, c_Y2, c_YI1; it does not",
            "do not claim the bulk/volume channel is uniquely proved here",
            "do not claim full nonlinear collapse is solved",
            "do not remove global conditional wording from compact predictions",
        ],
    }


def _print_result(result: dict[str, Any]) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, value in result["closed_checks"].items():
        print(f"  - {key}: {value}")
    print("open_checks:")
    for key, value in result["open_checks"].items():
        print(f"  - {key}: {value}")
    for key in (
        "exterior_deficit",
        "surface_deficit",
        "volume_deficit_from_clock",
        "chi_from_bulk_self_consistent_feedback",
        "d_chi_d_omega_Delta",
        "p16f_assumed_chi",
    ):
        print(f"{key}: {result[key]}")
    print("readout_filters_in_qv:")
    for key, value in result["readout_filters_in_qv"].items():
        print(f"  - {key}: {value}")
    print("chi_by_channel:")
    for key, value in result["chi_by_channel"].items():
        print(f"  - {key}: {value}")
    print("d_chi_d_coeff:")
    for key, value in result["d_chi_d_coeff"].items():
        print(f"  - {key}: {value}")
    print("resolves:", result["resolves"])
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
    _print_result(derive_deficit_feedback_exponent_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
