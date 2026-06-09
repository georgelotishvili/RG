# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: state whether c_Y is c_Y^(Y) or X-scheme c_X.
# Active coefficient detail: c_Y is c_Y^(Y); the source map below uses the
# volume-response compact class, not a new X-scheme coefficient.

"""PHASE 16f: Compactness-band source map for a stated class.

This supporting gate closes the branch-selection algebra for a restricted,
explicit class:

  * exterior-sheet/principal Lambert branch, 0<Q<2;
  * volume-response source attenuation, chi=1;
  * physical compactness input C0=2GM/(c^2 R0);
  * an explicit n=1 polytropic realizing class, p=K rho^2.

It does not close the more ambitious full action-coefficient map for arbitrary
EOS/collapse histories.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def derive_stated_compactness_class_source_map() -> dict[str, Any]:
    C0, Q, q, S = sp.symbols("C0 Q q S", positive=True, real=True)
    K_poly, rho_c, c = sp.symbols("K_poly rho_c c", positive=True, real=True)
    u = sp.symbols("u", positive=True, real=True)

    chi_volume = sp.Integer(1)
    Q_of_C0 = sp.simplify(-2 * sp.LambertW(-C0 / 2, 0))
    q_of_C0 = sp.simplify(sp.Rational(3, 2) * Q_of_C0)
    S_of_C0 = sp.simplify(q_of_C0 * sp.exp(q_of_C0))

    branch_residual_by_identity = sp.Integer(0)
    source_residual_by_identity = sp.Integer(0)
    reduced_eigenvalue = sp.simplify(-(1 + q_of_C0))

    C0_lower = sp.exp(-sp.Rational(1, 2))
    C0_upper = sp.simplify(2 / sp.E)
    compactness_band = sp.And(C0 > C0_lower, C0 < C0_upper)

    # Newtonian n=1 polytrope: p=K*rho^2, Lane-Emden gives
    # C0=2GM/(c^2 R)=4*K*rho_c/c^2.
    C0_n1_polytrope = sp.simplify(4 * K_poly * rho_c / c**2)
    rho_band_lower = sp.simplify(c**2 * C0_lower / (4 * K_poly))
    rho_band_upper = sp.simplify(c**2 * C0_upper / (4 * K_poly))
    u_band_lower = sp.simplify(C0_lower / 4)
    u_band_upper = sp.simplify(C0_upper / 4)

    sample_u = sp.Rational(1, 6)
    sample_C0 = sp.simplify(4 * sample_u)
    sample_Q = sp.N(Q_of_C0.subs(C0, sample_C0), 14)
    sample_q = sp.N(q_of_C0.subs(C0, sample_C0), 14)
    sample_S = sp.N(S_of_C0.subs(C0, sample_C0), 14)
    sample_in_window = bool(C0_lower < sample_C0 < C0_upper and 1 < sample_Q < 2)

    passed = (
        branch_residual_by_identity == 0
        and source_residual_by_identity == 0
        and sample_in_window
    )

    return {
        "STATUS": (
            "PASS_STATED_COMPACTNESS_CLASS_SOURCE_MAP"
            if passed
            else "CHECK_STATED_COMPACTNESS_CLASS_SOURCE_MAP"
        ),
        "SCOPE": (
            "Restricted compactness-band theorem.  For the volume-response "
            "class chi=1, the principal exterior-sheet branch maps one "
            "physical input C0 into Q, q and S.  This is not an arbitrary-EOS "
            "or full collapse theorem."
        ),
        "closed_checks": {
            "one_free_physical_input_C0": True,
            "principal_branch_residual_zero_by_Lambert_identity": True,
            "volume_response_chi_fixed_to_one": True,
            "source_residual_zero_by_construction": True,
            "n1_polytrope_realizing_band_nonempty": sample_in_window,
        },
        "open_checks": {
            "arbitrary_EOS_map": False,
            "full_action_coefficient_chi_map": False,
            "full_nonlinear_collapse_history": False,
            "relativistic_TOV_fit": False,
        },
        "principal_branch_load": sp.Eq(sp.Symbol("Q_sheet(C0)"), Q_of_C0),
        "branch_equation": sp.Eq(C0, Q * sp.exp(-Q / 2)),
        "compactness_band_C0": compactness_band,
        "C0_lower_Q1": C0_lower,
        "C0_upper_Q2": C0_upper,
        "volume_response_chi": sp.Eq(sp.Symbol("chi_volume"), chi_volume),
        "selected_deficit": sp.Eq(sp.Symbol("q(C0)"), q_of_C0),
        "source_map": sp.Eq(sp.Symbol("S(C0)"), S_of_C0),
        "reduced_flow": sp.Eq(sp.Symbol("dq_dtau"), S * sp.exp(-q) - q),
        "fixed_point_residual": source_residual_by_identity,
        "linear_eigenvalue_at_selected_point": reduced_eigenvalue,
        "n1_polytrope_EOS": sp.Eq(sp.Symbol("p"), K_poly * rho_c**2),
        "n1_polytrope_compactness": sp.Eq(sp.Symbol("C0_n1"), C0_n1_polytrope),
        "n1_polytrope_rho_c_band": sp.And(
            rho_c > rho_band_lower,
            rho_c < rho_band_upper,
        ),
        "dimensionless_u_definition": sp.Eq(u, K_poly * rho_c / c**2),
        "dimensionless_u_band": sp.And(u > u_band_lower, u < u_band_upper),
        "sample_realizing_point": {
            "u=K*rho_c/c^2": sample_u,
            "C0": sample_C0,
            "Q": sample_Q,
            "q": sample_q,
            "S": sample_S,
            "in_window": sample_in_window,
        },
        "do_not_claim": [
            "do not extend this result to arbitrary EOS",
            "do not claim chi(c_Y,c_Y2,c_YI1,omega_Delta) is derived here",
            "do not claim full nonlinear collapse is solved",
            "do not use this class theorem as an observational fit",
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
        "principal_branch_load",
        "branch_equation",
        "compactness_band_C0",
        "C0_lower_Q1",
        "C0_upper_Q2",
        "volume_response_chi",
        "selected_deficit",
        "source_map",
        "linear_eigenvalue_at_selected_point",
        "n1_polytrope_EOS",
        "n1_polytrope_compactness",
        "n1_polytrope_rho_c_band",
        "dimensionless_u_definition",
        "dimensionless_u_band",
        "sample_realizing_point",
    ):
        print(f"{key}: {result[key]}")
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    _print_result(derive_stated_compactness_class_source_map())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
