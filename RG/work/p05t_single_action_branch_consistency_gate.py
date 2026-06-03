# Notation header:
# signature (+---); compact branch uses B=exp(-r_s/r), A=exp(r_s/r).
#
# Referee-level gate:
# The compact branch must not look like a different action.  This file audits
# the single-action reading:
#
#     F_branch(Y,lambda_i,H) = F_min(e^(-2H)Y, e^(2H)lambda_i),
#
# with H an independent pressure/energy-deficit channel of the EFT.  The weak
# Solar branch is the unloaded background H=0.  The compact pure-phase branch is
# the loaded background H=h.  The action template is the same; only the
# background branch values differ.

from __future__ import annotations

import hashlib

import sympy as sp

from p03d_phase_normalized_solar_global_audit import (
    phase_normalized_solar_global_audit,
)
from p05g_exponential_source_eom import (
    auxiliary_deficit_operator_health_gate,
    derive_covariant_deficit_operator_from_medium_fields_gate,
)
from p05j_fmin_compact_exterior_gate import (
    _coefficient_symbols,
    _fmin_polynomial,
    derive_fmin_compact_identity_branch_residual_gate,
    derive_phase_normalized_fmin_compact_gate,
    solar_physical_fmin_coefficients,
)
from p05s_phase_normalized_fmin_action_gate import (
    derive_phase_normalized_fmin_action_gate,
)


def _expr_id(expr: sp.Expr) -> str:
    return hashlib.sha256(sp.srepr(sp.simplify(expr)).encode("utf-8")).hexdigest()


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def derive_weak_solar_H_euler_source_gate() -> dict[str, object]:
    """
    H-Euler source on the weak Solar branch.

    The single-action claim needs more than F(H=0)=F_raw.  If H is a real
    branch field, H=0 must also satisfy the H equation on the weak Solar
    background to the order claimed by the Solar guard.  This gate computes the
    algebraic F_min source

        S_H = d F_branch / dH

    before the projected H_Delta stiffness is added.  For H=0 the stiffness
    term has zero current, so the F_min source must vanish on the Solar branch.
    """
    template = _single_fmin_template()
    symbols = template["symbols"]
    Y = symbols["Y"]
    lambda_r = symbols["lambda_r"]
    lambda_t = symbols["lambda_t"]
    H = symbols["H"]
    c_Y2 = symbols["c_Y2"]

    eps = sp.Symbol("eps")
    y1, y2, r1, r2, t1, t2 = sp.symbols(
        "y1 y2 r1 r2 t1 t2", real=True
    )
    source = sp.diff(template["single_action_Fmin_template"], H)
    series_subs = {
        Y: 1 + y1 * eps + y2 * eps**2,
        lambda_r: 1 + r1 * eps + r2 * eps**2,
        lambda_t: 1 + t1 * eps + t2 * eps**2,
        H: 0,
    }
    source_series_expanded = sp.expand(
        sp.series(source.subs(series_subs), eps, 0, 3).removeO() / c_Y2
    )
    source_series = sp.factor(source_series_expanded)
    source_o1 = sp.factor(source_series_expanded.coeff(eps, 1))
    source_o2 = sp.factor(source_series_expanded.coeff(eps, 2))

    u = sp.Symbol("U", real=True)
    solar_1pn = {y1: u, r1: -u, t1: 0}
    exact_gr_2pn = {
        y1: u,
        r1: -u,
        t1: 0,
        y2: u**2,
        r2: u**2,
        t2: -u**2,
    }
    solar_o1 = sp.factor(sp.simplify(source_o1.subs(solar_1pn)))
    solar_o2_exact_gr = sp.factor(sp.simplify(source_o2.subs(exact_gr_2pn)))

    r, r_s = sp.symbols("r r_s", positive=True, real=True)
    h = r_s / (2 * r)
    compact_source = sp.simplify(
        source.subs(
            {
                H: h,
                Y: sp.exp(2 * h),
                lambda_r: sp.exp(-2 * h),
                lambda_t: sp.exp(-2 * h),
            }
        )
    )

    passed = solar_o1 == 0 and solar_o2_exact_gr == 0 and compact_source == 0

    return {
        "status": (
            "PASS_H_EULER_SOURCE_VANISHES_ON_WEAK_SOLAR_AND_COMPACT_BRANCHES"
            if passed
            else "CHECK_H_EULER_SOURCE_ON_BRANCHES"
        ),
        "H_source_definition": "S_H = dF_branch/dH",
        "generic_H_source_series_over_cY2": source_series,
        "generic_O1_over_cY2": source_o1,
        "generic_O2_over_cY2": source_o2,
        "Solar_1PN_relation": "y1=U, r1=-U, t1=0",
        "Solar_O1_source_over_cY2": solar_o1,
        "Solar_exact_GR_2PN_coefficients": {
            "y1": u,
            "r1": -u,
            "t1": 0,
            "y2": u**2,
            "r2": u**2,
            "t2": -u**2,
        },
        "Solar_exact_GR_2PN_source_over_cY2": solar_o2_exact_gr,
        "compact_pure_phase_H_source": compact_source,
        "reading": (
            "The weak H=0 branch is not only a functional reduction to raw "
            "F_min.  The H-Euler source from F_min vanishes through the Solar "
            "1PN/2PN exact-GR strain ledger.  The O(U) cancellation follows "
            "from y1+r1+2*t1=0, not merely from the unit-state tadpole."
        ),
    }


def _single_fmin_template() -> dict[str, object]:
    Y, lambda_r, lambda_t, H = sp.symbols(
        "Y lambda_r lambda_t H", positive=True, real=True
    )
    coeffs = _coefficient_symbols()
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = coeffs

    raw = _fmin_polynomial(Y, lambda_r, lambda_t, coeffs)
    F = raw.subs(solar_physical_fmin_coefficients(coeffs))
    F = sp.simplify(F.subs(c_Y2, c_Y2))

    Y_hat = sp.exp(-2 * H) * Y
    lambda_r_hat = sp.exp(2 * H) * lambda_r
    lambda_t_hat = sp.exp(2 * H) * lambda_t
    Fhat = sp.simplify(
        F.subs({Y: Y_hat, lambda_r: lambda_r_hat, lambda_t: lambda_t_hat})
    )
    raw_from_template = sp.simplify(Fhat.subs(H, 0))

    return {
        "symbols": {
            "Y": Y,
            "lambda_r": lambda_r,
            "lambda_t": lambda_t,
            "H": H,
            "c_Y2": c_Y2,
        },
        "raw_Fmin": F,
        "single_action_Fmin_template": Fhat,
        "template_id": _expr_id(Fhat),
        "raw_from_unloaded_H0": raw_from_template,
        "unloaded_equals_raw": sp.simplify(raw_from_template - F) == 0,
        "normalized_invariants": {
            "Yhat": Y_hat,
            "lambda_r_hat": lambda_r_hat,
            "lambda_t_hat": lambda_t_hat,
        },
    }


def derive_single_action_branch_consistency_gate() -> dict[str, object]:
    """
    Single-action branch consistency audit.

    What this closes:
    - The compact branch is not obtained by changing the action.
    - The same phase-normalized F_min template is used in both branches.
    - Weak Solar: H=0, so the template reduces exactly to raw F_min and the
      p03d Solar 1PN/2PN ledger stays GR-compatible.
    - Compact pure phase: H=h and Y=e^(2h), lambda_i=e^(-2h), so the hatted
      invariants equal one; F_min density, metric stress and phi^A Euler
      residual vanish before the exterior source equation is evaluated.
    - The active compact exterior source is the independent H_Delta projected
      deficit operator L_Delta_perp.
    - The determinant-locked reading H=-log(I3)/6 is a rejected audit, not the
      branch action.
    """
    template = _single_fmin_template()
    symbols = template["symbols"]
    Y = symbols["Y"]
    lambda_r = symbols["lambda_r"]
    lambda_t = symbols["lambda_t"]
    H = symbols["H"]

    r, r_s = sp.symbols("r r_s", positive=True, real=True)
    h = r_s / (2 * r)
    compact_subs = {
        H: h,
        Y: sp.exp(2 * h),
        lambda_r: sp.exp(-2 * h),
        lambda_t: sp.exp(-2 * h),
    }
    weak_subs = {H: 0}

    compact_invariants = {
        name: sp.simplify(expr.subs(compact_subs))
        for name, expr in template["normalized_invariants"].items()
    }
    weak_invariants = {
        name: sp.simplify(expr.subs(weak_subs))
        for name, expr in template["normalized_invariants"].items()
    }

    p05s = derive_phase_normalized_fmin_action_gate()
    p03d = phase_normalized_solar_global_audit()
    p05g_operator = derive_covariant_deficit_operator_from_medium_fields_gate()
    p05g_health = auxiliary_deficit_operator_health_gate()
    raw_audit = derive_fmin_compact_identity_branch_residual_gate()
    compact_quiet = derive_phase_normalized_fmin_compact_gate()
    H_euler = derive_weak_solar_H_euler_source_gate()

    compact_unit_invariants = all(value == 1 for value in compact_invariants.values())
    weak_unloaded_is_raw = template["unloaded_equals_raw"] and all(
        sp.simplify(value - symbols[key]) == 0
        for key, value in {
            "Y": weak_invariants["Yhat"],
            "lambda_r": weak_invariants["lambda_r_hat"],
            "lambda_t": weak_invariants["lambda_t_hat"],
        }.items()
    )
    compact_fmin_quiet = (
        sp.simplify(compact_quiet["Fhat_on_compact_identity"]) == 0
        and _all_zero(compact_quiet["Fhat_stress_on_compact_identity"].values())
        and sp.simplify(compact_quiet["Fhat_phiA_Euler_identity"]) == 0
    )
    solar_guard_pass = (
        p03d["status"]
        == "PASS_INDEPENDENT_H_RETAINS_SOLAR_1PN_2PN__GLOBAL_I3_LOCK_REJECTED"
    )
    action_gate_pass = (
        p05s["phase_normalized_action_status"]
        == "PASS_ACTION_LEVEL_PHASE_NORMALIZED_FMIN_IS_QUIET_ON_COMPACT_BRANCH"
    )
    active_source_pass = (
        p05g_operator["operator_status"]
        == "PASS_COVARIANT_DEFICIT_OPERATOR_REDUCES_TO_STATIC_PROJECTED_SOURCE"
        and p05g_health["operator_health_status"]
        == "PASS_INDEPENDENT_PRESSURE_DEFICIT_OPERATOR_CLOSES_EXTERIOR"
    )
    raw_compact_obstruction = all(raw_audit["nonzero_checks"].values())
    determinant_lock_rejected = (
        raw_compact_obstruction
        and any(value != 0 for value in p03d["weak_Solar_O1_stress"]["determinant_locked_Fhat"].values())
        and p03d["Solar_2PN_exact_GR_constant_strain_solutions"][
            "determinant_locked_Fhat"
        ]
        == []
    )

    passed = (
        weak_unloaded_is_raw
        and compact_unit_invariants
        and compact_fmin_quiet
        and solar_guard_pass
        and action_gate_pass
        and active_source_pass
        and determinant_lock_rejected
        and H_euler["status"]
        == "PASS_H_EULER_SOURCE_VANISHES_ON_WEAK_SOLAR_AND_COMPACT_BRANCHES"
    )

    return {
        "status": (
            "PASS_SINGLE_ACTION_PHASE_NORMALIZED_BRANCH_LEDGER"
            if passed
            else "CHECK_SINGLE_ACTION_PHASE_NORMALIZED_BRANCH_LEDGER"
        ),
        "single_action_statement": (
            "The EFT uses one phase-normalized F_min action template.  Branches "
            "are background regimes of the independent deficit channel H: H=0 "
            "on the unloaded weak Solar guard, and H=h on the compact pure-phase "
            "exterior.  The action is not changed between branches."
        ),
        "single_action_template_id": template["template_id"],
        "action_template": sp.Eq(
            sp.Symbol("F_branch"), template["single_action_Fmin_template"]
        ),
        "weak_branch_substitution": {
            "H": 0,
            "Yhat": weak_invariants["Yhat"],
            "lambda_r_hat": weak_invariants["lambda_r_hat"],
            "lambda_t_hat": weak_invariants["lambda_t_hat"],
            "unloaded_template_equals_raw_Fmin": weak_unloaded_is_raw,
        },
        "compact_branch_substitution": {
            "H": h,
            "Y": sp.exp(2 * h),
            "lambda_r": sp.exp(-2 * h),
            "lambda_t": sp.exp(-2 * h),
            "Yhat": compact_invariants["Yhat"],
            "lambda_r_hat": compact_invariants["lambda_r_hat"],
            "lambda_t_hat": compact_invariants["lambda_t_hat"],
            "unit_invariants": compact_unit_invariants,
        },
        "compact_Fmin_quiet_checks": {
            "Fhat_on_compact_identity": compact_quiet["Fhat_on_compact_identity"],
            "Fhat_stress_on_compact_identity": compact_quiet[
                "Fhat_stress_on_compact_identity"
            ],
            "Fhat_phiA_Euler_identity": compact_quiet["Fhat_phiA_Euler_identity"],
            "all_quiet": compact_fmin_quiet,
        },
        "weak_solar_guard": {
            "p03d_status": p03d["status"],
            "weak_O1_raw": p03d["weak_Solar_O1_stress"]["raw_Fmin"],
            "weak_O1_independent_H_unloaded": p03d["weak_Solar_O1_stress"][
                "independent_H_unloaded"
            ],
            "Solar_2PN_exact_GR_independent_H_unloaded": (
                p03d["Solar_2PN_exact_GR_constant_strain_solutions"][
                    "independent_H_unloaded"
                ]
            ),
        },
        "H_euler_source_guard": H_euler,
        "active_compact_source_guard": {
            "covariant_operator_status": p05g_operator["operator_status"],
            "operator_health_status": p05g_health["operator_health_status"],
            "H_Delta_static_branch": p05g_operator["static_branch_H_Delta"],
            "compact_H_eom_residual": p05g_health["compact_H_eom_residual"],
            "field_equation_residuals": p05g_health["field_equation_residuals"],
        },
        "rejected_reading_guard": {
            "raw_absolute_invariant_compact_audit": (
                "REJECTED_RAW_FMIN_NONZERO_COMPACT_RESIDUAL"
            ),
            "raw_compact_obstruction": raw_compact_obstruction,
            "raw_ThetaF_radial_at_w_equals_2_over_M4_cY2": raw_audit[
                "Fmin_mixed_stress_over_M4_cY2"
            ]["ThetaF^r_r/M4"].subs(sp.Symbol("w", positive=True, real=True), 2),
            "determinant_locked_weak_O1_stress": p03d["weak_Solar_O1_stress"][
                "determinant_locked_Fhat"
            ],
            "determinant_locked_2PN_exact_GR_solutions": p03d[
                "Solar_2PN_exact_GR_constant_strain_solutions"
            ]["determinant_locked_Fhat"],
            "determinant_lock_rejected": determinant_lock_rejected,
        },
        "article_export_statement": (
            "The same covariant EFT action is used in both regimes.  Its "
            "elastic core is F_min evaluated on the phase-normalized invariants "
            "Yhat=e^{-2H}Y and lambdahat_i=e^{2H}lambda_i, with H an "
            "independent pressure/energy-deficit channel.  The weak Solar guard "
            "is the unloaded background H=0, where the template reduces to the "
            "raw F_min, preserves the GR 1PN/2PN ledger, and satisfies the "
            "H-Euler equation through the same Solar strain identities.  The compact "
            "pure-phase exterior is the loaded background H=h, where the "
            "hatted invariants equal one and the tadpole-free F_min sector has "
            "zero density, zero metric stress and zero phi^A Euler residual.  "
            "The compact exterior source is then the independent projected "
            "deficit operator L_Delta_perp.  The determinant-locked reading "
            "H=-log(I3)/6 is a rejected audit because it gives a nonzero Solar "
            "O(U) stress and no exact-GR constant-strain 2PN solution."
        ),
        "remaining_status": (
            "The static exterior branch ledger is closed at the level tested "
            "here.  The finite-core dynamical branch-selection law and curved "
            "background hyperbolicity remain separate layers, not assumptions "
            "inside this gate."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18t: Single-action branch consistency gate")
    print("=" * 72)
    result = derive_single_action_branch_consistency_gate()
    for key, value in result.items():
        print(f"{key:56s}: {value}")
