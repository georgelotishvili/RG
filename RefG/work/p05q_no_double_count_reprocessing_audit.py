# Notation header:
# signature (+---); compact branch uses positive metric functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.
#
# This file audits the reprocessing required after the referee correction:
# the old double-count/projector ledger is superseded.  The compact repair is
# action-level phase normalization of F_min in p05s.

from __future__ import annotations

import p05_compact as compact
import p05g_exponential_source_eom as p05g
from p05j_fmin_compact_exterior_gate import (
    derive_fmin_compact_identity_branch_residual_gate,
)
from p05k_full_compact_source_residual_gate import (
    derive_compact_projected_full_residual_gate,
    derive_full_raw_fmin_plus_ldelta_residual_gate,
)
from p05l_compact_fmin_weight_matching_gate import (
    derive_compact_fmin_weight_from_residual_matching_gate,
)
from p05m_fmin_tadpole_renormalization_gate import (
    derive_compact_linear_tail_vs_solar_family_gate,
    derive_unit_background_tadpole_subtraction_gate,
)
from p05s_phase_normalized_fmin_action_gate import (
    derive_phase_normalized_fmin_action_gate,
)
from p14_nec_deficit import nec_deficit_interpretation_ledger


def phase_normalized_fmin_reprocessing_audit():
    raw_identity = derive_fmin_compact_identity_branch_residual_gate()
    raw_full = derive_full_raw_fmin_plus_ldelta_residual_gate()
    projected = derive_compact_projected_full_residual_gate()
    matching = derive_compact_fmin_weight_from_residual_matching_gate()
    tadpole = derive_unit_background_tadpole_subtraction_gate()
    solar_tail = derive_compact_linear_tail_vs_solar_family_gate()
    phase_normalized_action = derive_phase_normalized_fmin_action_gate()
    central = p05g.p05g_central_exponential_source_gate()
    compact_gate = compact.compact_central_claim_gate()
    nec = nec_deficit_interpretation_ledger()

    checks = {
        "raw_identity_objection_is_real": raw_identity["p05j_status"]
        == "FAIL_FMIN_HAS_NONZERO_COMPACT_EXTERIOR_RESIDUAL",
        "raw_full_objection_is_real": raw_full["full_raw_residual_status"]
        == "FAIL_RAW_FMIN_ADDS_NONZERO_TENSOR_RESIDUAL",
        "projected_only_ledger_superseded": projected[
            "projected_compact_residual_status"
        ]
        == "SUPERSEDED_PROJECTED_RESIDUAL_ZERO__USE_P05S_ACTION_LEVEL_FMIN",
        "residual_matching_rejected": matching["compact_fmin_weight_status"]
        == "FAIL_RESIDUAL_MATCHING_OMEGA_F_ZERO_IS_CIRCULAR_WITHOUT_ACTION_MECHANISM",
        "tadpole_repair_rejected": tadpole["tadpole_subtraction_status"]
        == "FAIL_TADPOLE_SUBTRACTION_DOES_NOT_REMOVE_COMPACT_LINEAR_TAIL",
        "solar_tail_forced_rhs_rejected": solar_tail[
            "compact_tail_vs_solar_family_status"
        ]
        == "FAIL_SOLAR_PHYSICAL_SLICE_CONFLICTS_WITH_COMPACT_FMIN_TAIL_SILENCING",
        "phase_normalized_action_passes": phase_normalized_action[
            "phase_normalized_action_status"
        ]
        == "PASS_ACTION_LEVEL_PHASE_NORMALIZED_FMIN_IS_QUIET_ON_COMPACT_BRANCH",
        "central_gate_uses_phase_normalized_action": central["p05g_status"]
        == "PASS_P05G_STATIC_COMPACT_SOURCE_LEDGER_WITH_PHASE_NORMALIZED_FMIN__DYNAMICS_OPEN",
        "compact_file_reprocessed": compact_gate["phase_normalized_fmin_action"]
        == "PASS_ACTION_LEVEL_PHASE_NORMALIZED_FMIN_IS_QUIET_ON_COMPACT_BRANCH",
        "nec_uses_active_deficit_source": nec["p14_status"]
        == "PASS_NEC_SIGN_REWRITTEN_AS_REFG_ACTIVE_DEFICIT_LEDGER",
    }

    return {
        "p05q_status": (
            "PASS_PHASE_NORMALIZED_FMIN_REPROCESSING_AUDIT"
            if all(checks.values())
            else "CHECK_PHASE_NORMALIZED_FMIN_REPROCESSING_AUDIT"
        ),
        "checks": checks,
        "raw_identity_status": raw_identity["p05j_status"],
        "raw_full_status": raw_full["full_raw_residual_status"],
        "projected_status": projected["projected_compact_residual_status"],
        "phase_normalized_action_status": phase_normalized_action[
            "phase_normalized_action_status"
        ],
        "central_p05g_status": central["p05g_status"],
        "compact_phase_normalized_fmin_action": compact_gate[
            "phase_normalized_fmin_action"
        ],
        "nec_status": nec["p14_status"],
        "current_reading": (
            "The old failure is reprocessed as an action-branch error: raw "
            "absolute-invariant F_min is not the compact pure-phase action. "
            "Compact F_min uses phase-normalized invariants and is quiet at "
            "action level; L_Delta_perp supplies the active exterior source."
        ),
        "remaining_work": (
            "Derive the continuous weak-to-compact H-loading law.  Remaining "
            "compact work is core dynamics, rotation, perturbations, and "
            "observational tests."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18q: Phase-normalized F_min reprocessing audit")
    print("=" * 72)
    result = phase_normalized_fmin_reprocessing_audit()
    for key, value in result.items():
        print(f"{key:44s}: {value}")
