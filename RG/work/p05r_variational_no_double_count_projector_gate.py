# Notation header:
# signature (+---); compact branch uses positive metric functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.
#
# Historical rejected gate.
#
# This file wrote the p05p source ledger as a source-role projector.  The
# referee objection is correct: a projector placed in source-role space is not
# by itself a variational mechanism for an action that contains raw F_min.
# The active repair is p05s, where the compact F_min branch is written with
# phase-normalized invariants and its stress vanishes at action level.
#
#     source roles = (F_min structural, L_Delta_perp active).
#
# This file is retained only as a rejected diagnostic/provenance ledger.

from __future__ import annotations

import sympy as sp

from p05k_full_compact_source_residual_gate import (
    _raw_fmin_mixed_stress_over_cY2,
)


def derive_variational_no_double_count_projector_gate():
    """
    Explicit compact source-role projector.

    Let the source variation vector be

        V = (Theta_F, Theta_Delta)^T,

    where Theta_F is the raw structural F_min stress one would obtain if the
    structural sector were varied as ordinary compact RHS matter, and
    Theta_Delta is the projected deficit active source.

    The compact active-RHS projector is

        P_c = [[0,0],
               [0,1]].

    The complementary structural projector is

        Q_c = I-P_c = [[1,0],
                       [0,0]].

    Therefore

        V_active = P_c V = (0, Theta_Delta)^T,
        V_struct = Q_c V = (Theta_F, 0)^T.

    Referee correction: the algebraic projector identities are true, and the
    projected residual is zero, but this does not prove that raw F_min is absent
    from delta S / delta g.  Therefore this is not the compact source closure.
    The accepted repair is the p05s phase-normalized action.
    """
    r, r_s, G = sp.symbols("r r_s G", positive=True, real=True)
    M4, c_Y2 = sp.symbols("M4 c_Y2", real=True)
    w = sp.symbols("w", positive=True, real=True)

    P_c = sp.Matrix([[0, 0], [0, 1]])
    Q_c = sp.eye(2) - P_c

    projector_checks = {
        "P_c_squared_minus_P_c": sp.simplify(P_c * P_c - P_c),
        "Q_c_squared_minus_Q_c": sp.simplify(Q_c * Q_c - Q_c),
        "P_c_Q_c": sp.simplify(P_c * Q_c),
        "Q_c_P_c": sp.simplify(Q_c * P_c),
        "P_c_plus_Q_c_minus_I": sp.simplify(P_c + Q_c - sp.eye(2)),
    }

    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    delta_p = sp.simplify(D / (8 * sp.pi * G))
    theta_delta = {
        "t": -delta_p,
        "r": delta_p,
        "theta": -delta_p,
        "phi": -delta_p,
    }
    G_mixed = {
        "t": -D,
        "r": D,
        "theta": -D,
        "phi": -D,
    }

    theta_f_w = _raw_fmin_mixed_stress_over_cY2(w)
    w_expr = sp.exp(r_s / r)
    theta_f = {
        "t": M4 * c_Y2 * theta_f_w["ThetaF^t_t/(M4*cY2)"].subs(w, w_expr),
        "r": M4 * c_Y2 * theta_f_w["ThetaF^r_r/(M4*cY2)"].subs(w, w_expr),
        "theta": M4
        * c_Y2
        * theta_f_w["ThetaF^theta_theta/(M4*cY2)"].subs(w, w_expr),
        "phi": M4 * c_Y2 * theta_f_w["ThetaF^phi_phi/(M4*cY2)"].subs(w, w_expr),
    }

    active_vectors = {}
    structural_vectors = {}
    active_source = {}
    structural_source = {}
    residuals = {}
    rejected_double_count_residuals = {}
    for key in G_mixed:
        V = sp.Matrix([theta_f[key], theta_delta[key]])
        V_active = sp.simplify(P_c * V)
        V_structural = sp.simplify(Q_c * V)
        active_vectors[key] = V_active
        structural_vectors[key] = V_structural
        active_source[key] = sp.simplify(sum(V_active))
        structural_source[key] = sp.simplify(sum(V_structural))
        residuals[key] = sp.simplify(G_mixed[key] - 8 * sp.pi * G * active_source[key])
        rejected_double_count_residuals[key] = sp.factor(
            sp.simplify(
                G_mixed[key]
                - 8 * sp.pi * G * (active_source[key] + structural_source[key])
            )
        )

    all_projector_checks_zero = all(
        value == sp.zeros(*value.shape) for value in projector_checks.values()
    )
    compact_active_closes = all(sp.simplify(value) == 0 for value in residuals.values())
    structural_not_deleted = any(
        sp.simplify(value) != 0 for value in structural_source.values()
    )
    double_count_fails = any(
        sp.simplify(value) != 0 for value in rejected_double_count_residuals.values()
    )

    return {
        "variational_projector_status": (
            "REJECTED_POST_VARIATION_PROJECTOR_NOT_ACTION_MECHANISM__USE_P05S"
            if all_projector_checks_zero
            and compact_active_closes
            and structural_not_deleted
            and double_count_fails
            else "CHECK_VARIATIONAL_NO_DOUBLE_COUNT_PROJECTOR"
        ),
        "source_role_vector": sp.Matrix(
            [sp.Symbol("Theta_F_structural"), sp.Symbol("Theta_Delta_active")]
        ),
        "compact_active_projector": P_c,
        "compact_structural_projector": Q_c,
        "projector_checks": projector_checks,
        "active_variation_vectors": active_vectors,
        "structural_variation_vectors": structural_vectors,
        "compact_active_source": active_source,
        "compact_structural_source": structural_source,
        "compact_active_field_residuals": residuals,
        "rejected_double_count_residuals": rejected_double_count_residuals,
        "projector_defined_before_residual": True,
        "what_this_closes": (
            "The projector algebra gives zero residual only after the raw "
            "F_min stress has been removed from the active RHS.  This is not "
            "an action-level mechanism for an action that contains raw F_min."
        ),
        "what_this_does_not_claim": (
            "This file must not be exported as closure.  Use p05s, where "
            "compact F_min is phase-normalized before variation and therefore "
            "has zero compact-branch stress."
        ),
        "article_export_statement": (
            "Do not export the P_c projector as the final compact source "
            "mechanism.  Export the phase-normalized F_min action of p05s."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18r: Variational no-double-count projector")
    print("=" * 72)
    result = derive_variational_no_double_count_projector_gate()
    for key, value in result.items():
        print(f"{key:44s}: {value}")
