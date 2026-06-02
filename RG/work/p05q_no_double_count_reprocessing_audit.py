# Notation header:
# signature (+---); compact branch uses positive metric functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.
#
# This file audits the reprocessing required after the source-ledger correction:
# F_min is structural on the compact branch and is not counted again as an
# ordinary active RHS source on the same geometry.

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
from p05p_no_double_count_source_ledger_gate import (
    derive_compact_no_double_count_source_ledger_gate,
)
from p05r_variational_no_double_count_projector_gate import (
    derive_variational_no_double_count_projector_gate,
)
from p14_nec_deficit import nec_deficit_interpretation_ledger


def no_double_count_reprocessing_audit():
    raw_identity = derive_fmin_compact_identity_branch_residual_gate()
    raw_full = derive_full_raw_fmin_plus_ldelta_residual_gate()
    projected = derive_compact_projected_full_residual_gate()
    matching = derive_compact_fmin_weight_from_residual_matching_gate()
    tadpole = derive_unit_background_tadpole_subtraction_gate()
    solar_tail = derive_compact_linear_tail_vs_solar_family_gate()
    source_ledger = derive_compact_no_double_count_source_ledger_gate()
    variational_projector = derive_variational_no_double_count_projector_gate()
    central = p05g.p05g_central_exponential_source_gate()
    compact_gate = compact.compact_central_claim_gate()
    nec = nec_deficit_interpretation_ledger()

    checks = {
        "raw_identity_is_double_count_diagnostic": raw_identity["p05j_status"]
        == "FAIL_FMIN_HAS_NONZERO_COMPACT_EXTERIOR_RESIDUAL",
        "raw_full_is_double_count_diagnostic": raw_full["full_raw_residual_status"]
        == "FAIL_RAW_FMIN_ADDS_NONZERO_TENSOR_RESIDUAL",
        "projected_source_closes_compact_branch": projected[
            "projected_compact_residual_status"
        ]
        == "PASS_COMPACT_BRANCH_CLOSES_WHEN_ACTIVE_FMIN_WEIGHT_IS_ZERO",
        "residual_matching_rejected": matching["compact_fmin_weight_status"]
        == "FAIL_RESIDUAL_MATCHING_OMEGA_F_ZERO_IS_CIRCULAR_WITHOUT_ACTION_MECHANISM",
        "tadpole_repair_rejected": tadpole["tadpole_subtraction_status"]
        == "FAIL_TADPOLE_SUBTRACTION_DOES_NOT_REMOVE_COMPACT_LINEAR_TAIL",
        "solar_tail_forced_rhs_rejected": solar_tail[
            "compact_tail_vs_solar_family_status"
        ]
        == "FAIL_SOLAR_PHYSICAL_SLICE_CONFLICTS_WITH_COMPACT_FMIN_TAIL_SILENCING",
        "source_ledger_passes": source_ledger["no_double_count_ledger_status"]
        == "PASS_COMPACT_FMIN_RAW_RESIDUAL_IS_LEDGER_DOUBLE_COUNT_NOT_PHYSICAL_RHS",
        "variational_projector_passes": variational_projector[
            "variational_projector_status"
        ]
        == "PASS_VARIATIONAL_NO_DOUBLE_COUNT_PROJECTOR_CLOSES_COMPACT_ACTIVE_RHS",
        "central_gate_uses_source_ledger": central["p05g_status"]
        == "CHECK_P05G_NO_DOUBLE_COUNT_VARIATIONAL_PROJECTOR_PASS__CORE_DYNAMICS_OPEN",
        "compact_file_reprocessed": compact_gate["no_double_count_source_ledger"]
        == "COMPACT_ACTIVE_RHS_IS_L_DELTA_PERP__FMIN_IS_STRUCTURAL_MEDIUM_SECTOR",
        "nec_uses_active_deficit_source": nec["p14_status"]
        == "PASS_NEC_SIGN_REWRITTEN_AS_REFG_ACTIVE_DEFICIT_LEDGER",
    }

    return {
        "p05q_status": (
            "PASS_NO_DOUBLE_COUNT_REPROCESSING_AUDIT"
            if all(checks.values())
            else "CHECK_NO_DOUBLE_COUNT_REPROCESSING_AUDIT"
        ),
        "checks": checks,
        "raw_identity_status": raw_identity["p05j_status"],
        "raw_full_status": raw_full["full_raw_residual_status"],
        "projected_status": projected["projected_compact_residual_status"],
        "source_ledger_status": source_ledger["no_double_count_ledger_status"],
        "variational_projector_status": variational_projector[
            "variational_projector_status"
        ],
        "central_p05g_status": central["p05g_status"],
        "compact_source_ledger": compact_gate["no_double_count_source_ledger"],
        "nec_status": nec["p14_status"],
        "current_reading": (
            "The old failure is reprocessed as a ledger error: raw F_min is "
            "not an extra compact RHS source.  The compact active source is "
            "L_Delta_perp; F_min is structural medium sector."
        ),
        "remaining_work": (
            "The source-ledger separation is now written as a variational "
            "projector in p05r.  Remaining compact work is core dynamics, "
            "rotation, perturbations, and observational tests."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18q: No-double-count reprocessing audit")
    print("=" * 72)
    result = no_double_count_reprocessing_audit()
    for key, value in result.items():
        print(f"{key:44s}: {value}")
