# Notation header:
# signature (+---); compact branch uses positive metric functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.
#
# Referee-level repair after the post-variation projector objection.
# The compact F_min sector is not silenced by a projector applied after
# delta S / delta g.  The repair is action-level: on the compact pure-phase
# branch F_min is written in phase-normalized strain invariants.  The branch is
# then unstrained in the local phase frame, so the F_min metric stress and the
# phi^A Euler residual vanish before the compact field equation is evaluated.

from __future__ import annotations

import sympy as sp

from p05j_fmin_compact_exterior_gate import (
    derive_fmin_compact_identity_branch_residual_gate,
    derive_phase_normalized_fmin_compact_gate,
)
from p03d_phase_normalized_solar_global_audit import (
    phase_normalized_solar_global_audit,
)


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def derive_phase_normalized_fmin_action_gate() -> dict[str, object]:
    """
    Action-level compact F_min closure.

    The rejected raw audit uses absolute invariants on the compact exterior,

        Y=e^(2h), lambda_r=lambda_t=e^(-2h),

    and obtains a nonzero raw Theta_F.  That is the referee's tensor objection.

    The compact pure-phase branch must instead measure the residual strain
    relative to the local phase-pressure deficit:

        Y_hat = e^(-2H) Y,
        lambda_hat_i = e^(2H) lambda_i.

    Here H is the independent pressure/energy-deficit channel in the action.
    It is not the directly measured stretch of the base medium and it is not a
    global pre-variation substitution H=-log(I3)/6 in the F_min sector.  p03d
    checks the difference: the determinant lock breaks the weak Solar 1PN
    stress ledger, while the unloaded deficit H=0 preserves the p03c Solar 2PN
    branch.

    On the compact branch H=h, so

        Y_hat=lambda_hat_r=lambda_hat_t=1.

    The Solar F_min slice is already tadpole-free at the unit state.  Therefore
    the F_min density, its metric stress, and the radial phi^A Euler residual
    vanish on the compact pure-phase branch.  This is not a post-variation
    deletion of stress.  It is the compact branch action written in the correct
    local phase frame.
    """
    raw = derive_fmin_compact_identity_branch_residual_gate()
    normalized = derive_phase_normalized_fmin_compact_gate()
    solar_guard = phase_normalized_solar_global_audit()

    H, Y, lambda_r, lambda_t = sp.symbols(
        "H Y lambda_r lambda_t", positive=True, real=True
    )
    Y_hat = sp.exp(-2 * H) * Y
    lambda_r_hat = sp.exp(2 * H) * lambda_r
    lambda_t_hat = sp.exp(2 * H) * lambda_t

    weak_unloaded_reduction = {
        "Y_hat_minus_Y_at_H0": sp.simplify(Y_hat.subs(H, 0) - Y),
        "lambda_r_hat_minus_lambda_r_at_H0": sp.simplify(
            lambda_r_hat.subs(H, 0) - lambda_r
        ),
        "lambda_t_hat_minus_lambda_t_at_H0": sp.simplify(
            lambda_t_hat.subs(H, 0) - lambda_t
        ),
    }

    raw_objection_real = (
        raw["p05j_status"] == "FAIL_FMIN_HAS_NONZERO_COMPACT_EXTERIOR_RESIDUAL"
        and raw["nonzero_checks"]["Tt_not_zero"]
        and raw["nonzero_checks"]["Tr_not_zero"]
        and raw["nonzero_checks"]["Ttheta_not_zero"]
        and raw["nonzero_checks"]["Ef_not_zero"]
    )
    normalized_stress_zero = _all_zero(
        normalized["Fhat_stress_on_compact_identity"].values()
    )
    normalized_eom_zero = sp.simplify(normalized["Fhat_phiA_Euler_identity"]) == 0
    normalized_density_zero = sp.simplify(normalized["Fhat_on_compact_identity"]) == 0
    weak_reduces_to_raw = _all_zero(weak_unloaded_reduction.values())

    passed = (
        raw_objection_real
        and normalized["phase_normalized_status"]
        == "PASS_IF_FMIN_IS_DEFINED_WITH_PHASE_NORMALIZED_BRANCH_INVARIANTS"
        and normalized_density_zero
        and normalized_stress_zero
        and normalized_eom_zero
        and weak_reduces_to_raw
        and solar_guard["status"]
        == "PASS_INDEPENDENT_H_RETAINS_SOLAR_1PN_2PN__GLOBAL_I3_LOCK_REJECTED"
    )

    return {
        "phase_normalized_action_status": (
            "PASS_ACTION_LEVEL_PHASE_NORMALIZED_FMIN_IS_QUIET_ON_COMPACT_BRANCH"
            if passed
            else "CHECK_ACTION_LEVEL_PHASE_NORMALIZED_FMIN"
        ),
        "raw_absolute_invariant_audit": raw["p05j_status"],
        "raw_absolute_invariant_objection_is_real": raw_objection_real,
        "raw_ThetaF_radial_at_w_equals_2_over_M4_cY2": raw[
            "Fmin_mixed_stress_over_M4_cY2"
        ]["ThetaF^r_r/M4"].subs(sp.Symbol("w", positive=True, real=True), 2),
        "compact_phase_normalized_invariants": normalized[
            "normalized_invariants"
        ],
        "Fhat_on_compact_identity": normalized["Fhat_on_compact_identity"],
        "Fhat_stress_on_compact_identity": normalized[
            "Fhat_stress_on_compact_identity"
        ],
        "Fhat_phiA_Euler_identity": normalized["Fhat_phiA_Euler_identity"],
        "weak_unloaded_reduction": weak_unloaded_reduction,
        "p03d_solar_global_audit_status": solar_guard["status"],
        "p03d_solar_O1_guard": solar_guard["weak_Solar_O1_stress"],
        "p03d_solar_2PN_guard": solar_guard[
            "Solar_2PN_exact_GR_constant_strain_solutions"
        ],
        "action_level_rule": (
            "Compact F_min is evaluated on phase-normalized strain invariants "
            "with H treated as an independent pressure/energy-deficit channel. "
            "The compact pure-phase exterior is unstrained in that local phase "
            "frame, so F_min contributes no compact exterior metric stress. "
            "The active exterior source is then L_Delta_perp.  A global "
            "determinant lock H=-log(I3)/6 inside F_min is rejected by p03d."
        ),
        "what_was_wrong_before": (
            "The post-variation source-role projector and the double-count "
            "label were not a sufficient variational mechanism.  The raw "
            "absolute-invariant Theta_F is a wrong-branch audit, not the "
            "compact branch action."
        ),
        "solar_guard": (
            "In the diffuse weak Solar branch the pressure-deficit channel H "
            "is unloaded through 2PN.  Then the hatted invariants reduce to the raw F_min "
            "invariants and p03d recovers the exact-GR Solar strain "
            "sigma=-1/2.  If H is instead locked globally to -log(I3)/6 before "
            "variation, p03d gives a nonzero O(U) Solar stress and rejects that "
            "reading."
        ),
        "remaining_work": (
            "derive the continuous compactness/deficit-loading law for H between the "
            "unloaded diffuse Solar branch and the loaded compact pure-phase "
            "branch.  The Solar 1PN/2PN guard and the static compact source "
            "ledger are both machine-checked."
        ),
        "article_export_statement": (
            "In the compact phase-spherical branch the elastic core is written "
            "with phase-normalized strain invariants "
            "Yhat=e^{-2H}Y and lambdahat_i=e^{2H}lambda_i.  For H=h these "
            "invariants equal one on the pure-phase exterior, and the "
            "tadpole-free F_min sector has zero density, zero metric stress, "
            "and zero phi^A Euler residual.  Thus the compact exterior is "
            "sourced by L_Delta_perp without deleting a nonzero F_min stress "
            "after variation."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18s: Action-level phase-normalized F_min compact gate")
    print("=" * 72)
    result = derive_phase_normalized_fmin_action_gate()
    for key, value in result.items():
        print(f"{key:56s}: {value}")
