# Notation header:
# signature (+---); compact branch uses positive metric functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.
#
# This gate records a rejected attempt to derive the compact active weight of
# the diffuse F_min channel from residual matching.  The algebra shows the
# wrong ledger consequence, but the argument is circular.  The repair is the
# p05p no-double-count source ledger, not residual-matched Omega_F.

from __future__ import annotations

import sympy as sp

from p05_compact import (
    derive_c2_core_refg_medium_source_decomposition,
    derive_c2_junction_stress_closure,
)
from p05k_full_compact_source_residual_gate import (
    _raw_fmin_mixed_stress_over_cY2,
    derive_compact_projected_full_residual_gate,
)


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def derive_compact_fmin_weight_from_residual_matching_gate():
    """
    Rejected residual-matching attempt for Omega_F=0 on the compact exterior.

    The compact exterior has two logically separate source layers:

    1. The projected phase-deficit channel L_Delta^perp.
    2. The diffuse medium-stress channel represented by F_min.

    On the compact exponential exterior, L_Delta^perp already matches the full
    mixed Einstein tensor.  Therefore the required residual source outside the
    core is exactly zero.  If the diffuse F_min channel were active outside,
    its active contribution would be

        Omega_F M4 c_Y2 Theta_F,raw^mu_mu.

    Since the raw F_min mixed tensor is not identically zero for finite
    w=exp(r_s/r)>1, the tensor equation

        Omega_F Theta_F,raw^mu_mu = 0

    would force Omega_F=0 on the compact exterior.  This is not a derivation.
    It is the sign that raw F_min was placed in the wrong ledger: the compact
    branch already uses F_min structurally and must not add it again as
    ordinary active compact RHS matter.
    """
    r, r_s, G, M4 = sp.symbols("r r_s G M4", positive=True, real=True)
    c_Y2, Omega_F = sp.symbols("c_Y2 Omega_F", real=True)
    w = sp.symbols("w", positive=True, real=True)

    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    delta_p = sp.simplify(D / (8 * sp.pi * G))
    G_mixed = {
        "t": -D,
        "r": D,
        "theta": -D,
        "phi": -D,
    }
    theta_delta = {
        "t": -delta_p,
        "r": delta_p,
        "theta": -delta_p,
        "phi": -delta_p,
    }
    required_residual_after_ldelta = {
        key: sp.simplify(G_mixed[key] / (8 * sp.pi * G) - theta_delta[key])
        for key in G_mixed
    }

    theta_f_w = _raw_fmin_mixed_stress_over_cY2(w)
    theta_f_components = {
        "t": theta_f_w["ThetaF^t_t/(M4*cY2)"],
        "r": theta_f_w["ThetaF^r_r/(M4*cY2)"],
        "theta": theta_f_w["ThetaF^theta_theta/(M4*cY2)"],
        "phi": theta_f_w["ThetaF^phi_phi/(M4*cY2)"],
    }
    active_fmin_equations = {
        key: sp.Eq(
            Omega_F * M4 * c_Y2 * theta_f_components[key],
            required_residual_after_ldelta[key],
        )
        for key in theta_f_components
    }

    numerators = [
        sp.factor(sp.together(value).as_numer_denom()[0])
        for value in theta_f_components.values()
    ]
    common_numerator_gcd = sp.factor(
        sp.gcd(sp.gcd(numerators[0], numerators[1]), numerators[2])
    )
    finite_branch_gcd = sp.factor(
        sp.simplify(common_numerator_gcd / (w - 1))
        if sp.simplify(common_numerator_gcd.subs(w, 1)) == 0
        else common_numerator_gcd
    )
    no_common_finite_zero = sp.simplify(finite_branch_gcd) == 1

    omega_f_solution = sp.Eq(Omega_F, 0)

    c2_residual = derive_c2_core_refg_medium_source_decomposition()
    junction = derive_c2_junction_stress_closure()
    c2_boundary_residual_zero = c2_residual["boundary_residuals_zero"]
    c2_phase_match_zero = _all_zero(c2_residual["phase_C2_match_at_boundary"].values())
    c2_shell_zero = _all_zero(junction["Israel_surface_stress"].values())

    compact_projected = derive_compact_projected_full_residual_gate()
    compact_projected_zero = _all_zero(
        compact_projected["compact_projected_residuals"].values()
    )

    passed = (
        _all_zero(required_residual_after_ldelta.values())
        and no_common_finite_zero
        and c2_boundary_residual_zero
        and c2_phase_match_zero
        and c2_shell_zero
        and compact_projected_zero
    )

    return {
        "compact_fmin_weight_status": (
            "FAIL_RESIDUAL_MATCHING_OMEGA_F_ZERO_IS_CIRCULAR_WITHOUT_ACTION_MECHANISM"
            if passed
            else "CHECK_COMPACT_FMIN_ACTIVE_WEIGHT_MATCHING"
        ),
        "exterior_required_residual_after_LDelta": required_residual_after_ldelta,
        "raw_Fmin_mixed_stress_over_M4_cY2": theta_f_components,
        "active_Fmin_equations": active_fmin_equations,
        "common_raw_Fmin_tensor_numerator_gcd": common_numerator_gcd,
        "finite_w_greater_than_1_common_gcd": finite_branch_gcd,
        "raw_Fmin_tensor_has_no_common_finite_zero": no_common_finite_zero,
        "derived_compact_weight": omega_f_solution,
        "C2_phase_match_zero": c2_phase_match_zero,
        "C2_residual_medium_boundary_zero": c2_boundary_residual_zero,
        "C2_Israel_shell_zero": c2_shell_zero,
        "compact_projected_residuals": compact_projected[
            "compact_projected_residuals"
        ],
        "reading": (
            "The C2 core may carry a finite residual medium-stress channel, and "
            "that channel vanishes at the boundary with no thin shell.  But "
            "using the already closed L_Delta exterior equation to set the "
            "raw F_min exterior weight to zero is circular.  The valid repair "
            "is p05p: F_min is the compact structural medium sector and is not "
            "added again as ordinary active compact RHS stress."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18l: Compact F_min branch weight from residual matching")
    print("=" * 72)
    result = derive_compact_fmin_weight_from_residual_matching_gate()
    for key, value in result.items():
        print(f"{key:52s}: {value}")
