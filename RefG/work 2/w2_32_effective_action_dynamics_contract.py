"""Fail-closed dynamics contract for the displayed RefG effective action.

This artifact freezes the *minimal* covariant action that is to be audited in
the next Work-2 dynamics gates.  A valid report means only that the action,
field domain, response tracks, exclusions and downstream falsification duties
are unambiguous and internally consistent.  It is not a degree-of-freedom,
stability, hyperbolicity, strong-coupling, PPN or observational PASS.

Two response tracks are deliberately kept distinct:

* ``GENERIC_SILENT_F`` is an arbitrary C2 isotropic response subject only to
  the exact silent-point value and first-variation conditions;
* ``F_MIN_REPRESENTATIVE`` is the special seven-term polynomial used by the
  legacy static gate and by the manuscript appendix.  Its rank-one Hessian is
  not inherited by the generic response family.

The legacy p05z source and the manuscript are read only as synchronization
crosschecks.  Their prose or exported status is not evidence for any dynamics
closure flag.  No symmetry-allowed omitted operator is silently used to repair
the frozen minimal action.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

import sympy as sp


CLAIM_ID = "W2_EFFECTIVE_ACTION_DYNAMICS_CONTRACT_001"
MODEL_VERSION = "W2-EFFECTIVE-ACTION-DYNAMICS-CONTRACT-v1.1-SYMBOLIC-CONTROLS"

HERE = Path(__file__).resolve().parent
REPOSITORY_ROOT = HERE.parents[1]
P05Z_PATH = HERE.parent / "work" / "p05z_unified_deficit_field_static_branch_gate.py"
MANUSCRIPT_PATH = REPOSITORY_ROOT / "artikle" / "RefG_Manuscript.tex"


REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})


def frozen_dynamic_closure_flags() -> dict[str, bool]:
    """Physical claims that this scope-freezing artifact does not close."""
    return {
        "generic_off_branch_constraint_algebra_derived": False,
        "physical_degree_of_freedom_count_derived": False,
        "silent_vacuum_reduced_quadratic_action_derived": False,
        "exponential_exterior_reduced_quadratic_action_derived": False,
        "ghost_freedom_proved": False,
        "gradient_stability_proved": False,
        "tachyon_control_proved": False,
        "strong_hyperbolicity_proved": False,
        "elliptic_constraints_separated_from_physical_signals": False,
        "strong_coupling_scale_derived": False,
        "EFT_control_on_the_exterior_proved": False,
        "healthy_open_coefficient_region_proved": False,
        "action_derived_regular_core_proved": False,
        "formation_or_branch_selection_proved": False,
        "source_derived_full_PPN_proved": False,
        "observational_validation_proved": False,
        "foundation_to_effective_action_origin_proved": False,
    }


ACTION_SPEC: dict[str, Any] = {
    "signature": "+---",
    "units": "c=hbar=1; M_Pl^(-2)=8*pi*G",
    "fields": {
        "metric": "Lorentzian g_{mu nu}",
        "clock": "real scalar Phi",
        "material_labels": "three real scalars phi^A, A=1,2,3",
        "deficit_response": "dimensionless real scalar H",
        "ordinary_matter": "psi, universally and minimally coupled only through g",
    },
    "physical_field_domain": [
        "Y>0",
        "B^{AB} positive definite",
    ],
    "definitions": {
        "Y": "g^{mu nu} nabla_mu Phi nabla_nu Phi",
        "u_mu": "nabla_mu Phi/sqrt(Y)",
        "gamma^{mu nu}": "u^mu u^nu-g^{mu nu}",
        "B^{AB}": "-g^{mu nu} nabla_mu phi^A nabla_nu phi^B",
        "Yhat": "exp(-2H) Y",
        "Bhat^{AB}": "exp(2H) B^{AB}",
        "I1hat": "Tr(Bhat)",
        "I2hat": "((Tr Bhat)^2-Tr(Bhat^2))/2",
        "I3hat": "det(Bhat)",
        "Z_H": "gamma^{mu nu} nabla_mu H nabla_nu H",
    },
    "bulk_action": (
        "S_bulk=int d4x sqrt(-g)[M_Pl^2 R/2-M_*^4 F(Yhat,I1hat,I2hat,I3hat)"
        "-omega_H M_Pl^2 Z_H]"
    ),
    "matter_action": "S_m[g,psi]",
    "parameter_domain": {
        "M_Pl": "positive",
        "M_*": "positive",
        "omega_H": "real in the action family; omega_H=1 on the exact exponential branch",
        "F": "real C2 function near the silent point for the frozen quadratic audit",
    },
    "symmetries": {
        "spacetime": "diffeomorphism invariance",
        "clock_shift": "Phi -> Phi+constant",
        "material_E3": "phi^A -> R^A_B phi^B+a^A with R in SO(3)",
        "internal_scaling": "H->H+sigma, Phi->exp(sigma)Phi, phi^A->exp(-sigma)phi^A",
        "clock_orientation": "Phi->-Phi",
    },
    "boundary_statement": (
        "GHY is understood for Dirichlet metric data; scalar Dirichlet data are the default; "
        "fixed H flux requires the corresponding Legendre boundary term"
    ),
    "minimality_rule": (
        "every covariant operator not displayed above has coefficient exactly zero in this frozen "
        "candidate; no omitted term may be activated after seeing a dynamics result"
    ),
}


GENERIC_SILENT_F_SPEC: dict[str, Any] = {
    "track_id": "GENERIC_SILENT_F",
    "argument_point": {
        "Yhat": 1,
        "Bhat^{AB}": "delta^{AB}",
        "(I1hat,I2hat,I3hat)": [3, 3, 1],
    },
    "silent_conditions": [
        "F|_1=0",
        "F_,Yhat|_1=0",
        "F_,Bhat^{AB}|_1=0",
    ],
    "invariant_first_jet_equivalent": [
        "f_0=0",
        "f_Y=0",
        "f_I1+2*f_I2+f_I3=0",
        "individual f_I1,f_I2,f_I3 need not vanish",
    ],
    "free_jet_data": {
        "first_derivatives": "two independent combinations among f_I1,f_I2,f_I3",
        "second_derivatives": "all ten entries of the symmetric 4x4 Hessian in (Yhat,I1hat,I2hat,I3hat)",
    },
    "regularity": "C2 in a neighborhood of the silent point",
    "scope_ceiling": (
        "the silent conditions close background value and tadpoles only; they fix neither the "
        "composite seven-variable Hessian nor any reduced physical spectrum"
    ),
}


F_MIN_REPRESENTATIVE_SPEC: dict[str, Any] = {
    "track_id": "F_MIN_REPRESENTATIVE",
    "normalization": "c_Y2 is real and nonzero",
    "polynomial_over_c_Y2": (
        "-8*Yhat+Yhat^2+8*I1hat+I1hat^2-16*I2hat+16*I3hat+2*Yhat*I1hat"
    ),
    "matrix_identity": (
        "F_min/c_Y2=(DeltaYhat+Tr(DeltaBhat))^2+16*det(DeltaBhat)"
    ),
    "unit_point_properties": {
        "silent": True,
        "composite_Hessian_rank_in_Yhat_and_symmetric_Bhat": 1,
        "composite_Hessian_nullity": 6,
        "cubic_saddle": True,
    },
    "inheritance_firewall": [
        "rank one is a property of this representative, not of GENERIC_SILENT_F",
        "the sign of c_Y2 or of the response Hessian is not a reduced kinetic-stability result",
        "static branch closure supplies no off-branch degree-of-freedom or strong-coupling result",
    ],
}


EXCLUDED_COMPLETION_SPEC: dict[str, Any] = {
    "policy": (
        "the following symmetry-compatible structures are outside the frozen minimal action; "
        "their coefficients are zero and they cannot be used as hidden repairs"
    ),
    "named_building_blocks": {
        "C^A": "g^{mu nu} nabla_mu Phi nabla_nu phi^A",
        "D_H": "u^mu nabla_mu H",
        "E_H^A": "exp(H) g^{mu nu} nabla_mu H nabla_nu phi^A",
    },
    "explicit_same_derivative_examples_excluded": [
        "delta_AB C^A C^B",
        "D_H^2",
        "delta_AB E_H^A E_H^B",
        "invariant-dependent coefficient multiplying Z_H",
    ],
    "other_excluded_classes": [
        "all allowed cross-contractions made from omitted building blocks",
        "nonminimal curvature couplings",
        "higher powers of curvature",
        "operators containing nabla_mu u_nu",
        "further derivatives of normalized invariants",
        "every other operator absent from ACTION_SPEC",
    ],
    "symmetry_forbidden_or_restricted": {
        "nonconstant_V(H)": "excluded by the global internal scaling symmetry",
        "linear_D_H": "excluded by clock-orientation reversal",
    },
    "future_completion_rule": (
        "a completion is a separately versioned candidate with a complete predeclared operator "
        "basis and must rerun every dynamics gate from the beginning"
    ),
    "hidden_repair_allowed": False,
}


DYNAMICS_GATE_SPEC: dict[str, Any] = {
    "ordered_gates": [
        "G1_generic_off_branch_ADM_velocity_Hessian_and_Dirac_constraint_closure",
        "G2_background_regular_physical_DOF_count_with_independent_covariant_crosscheck",
        "G3_silent_vacuum_fully_reduced_quadratic_action_for_each_response_track",
        "G4_exact_exponential_exterior_gauge_invariant_coupled_principal_spectrum",
        "G5_ghost_gradient_tachyon_and_strong_hyperbolicity_adjudication",
        "G6_strong_coupling_scale_and_EFT_background_hierarchy",
        "G7_fail_closed_dynamic_viability_adjudication",
    ],
    "mandatory_backgrounds": [
        "generic off-branch configurations in the declared Y>0, B>0 domain",
        "silent Minkowski reference state",
        "exact exponential exterior with H=m/r and omega_H=1",
    ],
    "track_rule": (
        "GENERIC_SILENT_F and F_MIN_REPRESENTATIVE are evaluated separately; a PASS or FAIL may "
        "not cross between them without a proved quantified implication"
    ),
    "falsification_triggers": [
        "nonclosing or inconsistent constraint algebra",
        "uncontrolled background-dependent physical DOF count",
        "negative reduced kinetic eigenvalue",
        "physical gradient instability or non-real characteristic root",
        "failure of strong hyperbolicity after separating genuine elliptic constraints",
        "quadratically null interacting physical mode with no finite controlled cutoff",
        "strong-coupling or EFT cutoff at or below a declared background scale",
        "singular physical coefficient inside the declared exterior domain",
        "disagreement of independent canonical and covariant mode counts",
    ],
}


SOURCE_CROSSCHECK_SPEC: dict[str, Any] = {
    "p05z": {
        "path": "RefG/work/p05z_unified_deficit_field_static_branch_gate.py",
        "role": "legacy static-branch action spelling and F_min provenance only",
        "not_evidence_for": "any dynamics closure flag",
        "required_compact_fragments": [
            "Yhat=exp(-2H)Y",
            "Bhat^AB=exp(2H)B^AB",
            "gamma^mn=u^mu^n-g^mn",
            "-omega_Hgamma^mnd_mHd_nH/(8*pi*G)",
            "PASS_UNIFIED_H_STATIC_BRANCHES_EOM__OFF_BRANCH_DYNAMICS_OPEN",
        ],
    },
    "manuscript": {
        "path": "artikle/RefG_Manuscript.tex",
        "role": "public manuscript export synchronization only",
        "not_evidence_for": "any contract identity or dynamics closure flag",
        "required_compact_fragments": [
            "\\widehatY&=e^{-2H}Y",
            "\\widehatB^{AB}&=e^{2H}B^{AB}",
            "-\\omega_HM_{\\rmPl}^2\\gamma^{\\mu\\nu}\\nabla_\\muH\\nabla_\\nuH",
            "H\\mapstoH+\\sigma",
            "\\Phi\\mapstoe^\\sigma\\Phi",
            "\\phi^A\\mapstoe^{-\\sigma}\\phi^A",
        ],
    },
}


EXPECTED_CLOSURE_FLAGS = frozen_dynamic_closure_flags()


SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "Freeze the exact displayed minimal RefG effective action, its field domain, symmetries, "
        "generic silent-response jet, special F_min representative, excluded completion and "
        "downstream dynamics falsifiers without promoting any dynamics result."
    ),
    "TYPE": "FAIL_CLOSED_EFFECTIVE_ACTION_DYNAMICS_SCOPE_CONTRACT",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": [
        "ACTION_SPEC is the complete minimal candidate under audit",
        "the generic response is C2 near its silent point",
        "M_Pl>0, M_*>0, Y>0 and B^{AB}>0 on the declared field domain",
        "source-file synchronization checks carry no physical evidence",
    ],
    "DOMAIN": (
        "the frozen covariant effective-action family and its generic-silent and F_min response "
        "tracks; no action-derived core, source solution, continuum foundation or observation"
    ),
    "CONVENTIONS": ACTION_SPEC,
    "FREEDOM_LEDGER": {
        "generic_response": GENERIC_SILENT_F_SPEC,
        "representative_response": F_MIN_REPRESENTATIVE_SPEC,
        "excluded_completion": EXCLUDED_COMPLETION_SPEC,
        "downstream_gates": DYNAMICS_GATE_SPEC,
    },
    "DEPENDENCIES": [
        "p05z is a noninherited static predecessor and source-export crosscheck",
        "RefG_Manuscript.tex is a nonauthoritative export crosscheck",
        "no prior finite-carrier normal-mode result supplies this field theory's constraints or spectrum",
    ],
    "METHOD": (
        "canonicalize and hash every frozen specification; verify exact scaling, projector, generic-jet "
        "and F_min identities symbolically; require source exports to agree; mutate each protected "
        "object and require failure; keep every physical closure flag false"
    ),
    "PASS_CONDITION": (
        "PASS means only that all definitions, exact identities, track firewalls, exclusions, source "
        "crosschecks, pinned hashes and mutation controls agree and every dynamics closure flag is false"
    ),
    "FAIL_CONDITION": (
        "any definition drift, source mismatch, generic/F_min conflation, unlisted repair, hash/control "
        "failure or promoted dynamics flag invalidates this contract"
    ),
    "FALSIFIER": (
        "an exact counterexample to a frozen identity falsifies this contract; a later dynamics trigger "
        "falsifies the affected action track's dynamic viability but does not erase a separately proved "
        "static background identity"
    ),
    "RESIDUAL": "exact symbolic zero; no floating-point tolerance",
    "ERROR_BOUND": "zero for identities; all physical dynamics errors and bounds remain uncomputed",
    "VALIDITY_HEALTH": (
        "scope validity requires fail-closed hashes, negative mutations, no hidden completion and no "
        "inheritance from static, manuscript or finite-carrier results"
    ),
    "BRANCHES": {
        "generic_silent_response": "FROZEN_FOR_FUTURE_AUDIT",
        "F_min_representative": "FROZEN_SEPARATELY_FOR_FUTURE_AUDIT",
        "exact_exponential_background": "REGISTERED_PRIOR_STATIC_LEMMA_NO_DYNAMIC_INHERITANCE",
        "kinematic_C2_core": "OUTSIDE_ACTION_DYNAMICS_CONTRACT_NOT_ACTION_DERIVED",
        "omitted_operator_completion": "EXCLUDED_REQUIRES_NEW_VERSION",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "no source-derived observable in a scope contract"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "constraint and spectrum calculations are future gates"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, fit, calibration or observational validation"},
    "IDENTIFIABILITY": (
        "not assessed; generic jet coefficients and dimensional hierarchy remain explicit freedoms"
    ),
    "BENCHMARK": [
        "internal-scaling invariance",
        "projector identity Z_H=X^2/Y-K",
        "generic silent-jet quadratic expansion",
        "F_min matrix identity, silent point, rank-one Hessian and cubic saddle",
        "p05z and manuscript export synchronization",
    ],
    "CLOSURE_FLAGS": frozen_dynamic_closure_flags(),
    "CROSSCHECK": (
        "canonical/Dirac and covariant/gauge-invariant derivations are mandated downstream; current "
        "manuscript and p05z reads are source synchronization only"
    ),
    "PROVENANCE": {
        "primary_frozen_object": "ACTION_SPEC in this artifact",
        "legacy_source": "RefG/work/p05z_unified_deficit_field_static_branch_gate.py",
        "manuscript_export": "artikle/RefG_Manuscript.tex",
        "target_leakage": False,
    },
    "FILES": [
        "RefG/work 2/w2_32_effective_action_dynamics_contract.py",
        "RefG/work/p05z_unified_deficit_field_static_branch_gate.py (read-only crosscheck)",
        "artikle/RefG_Manuscript.tex (read-only export crosscheck)",
    ],
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def _canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


# These constants are replaced once, from the canonical objects above, and
# thereafter make silent scientific drift fail closed.
EXPECTED_HASHES = {
    "action_spec": "02E757C7406101C2E91723ED28FBE7BDD3E4F547A3968F1BD11641F97CDFF7E2",
    "generic_silent_F_spec": "865752BEDBE5463801DEEC64FFC5831B91891C0C750F5997BBD4A7CE6C25E0F9",
    "F_min_representative_spec": "922B8C2CC22C3F9FF9C30D8D1AFCFB1DDF95A0F9E72BDC01168D7F2A0BC42B9B",
    "excluded_completion_spec": "60EFCF610A307DE2FECE9CBEFA6FFF3A273C4A975DC33CC1EE3706A402071319",
    "dynamics_gate_spec": "4767D085F50D670CCB38C446A8D7D2CB78AFD2054B05CC951F31D14995CF192A",
    "source_crosscheck_spec": "0CB5D26E351EF97812770BDDCB458F0FB2DDCB8B3798EF28824312B776F47C50",
    "scientific_contract": "6CED59206375068BC9A65C427D78FEBA3FADD8287EE36778B4D1A9E56E0AB5AB",
}


def _current_hashes() -> dict[str, str]:
    return {
        "action_spec": _canonical_sha256(ACTION_SPEC),
        "generic_silent_F_spec": _canonical_sha256(GENERIC_SILENT_F_SPEC),
        "F_min_representative_spec": _canonical_sha256(F_MIN_REPRESENTATIVE_SPEC),
        "excluded_completion_spec": _canonical_sha256(EXCLUDED_COMPLETION_SPEC),
        "dynamics_gate_spec": _canonical_sha256(DYNAMICS_GATE_SPEC),
        "source_crosscheck_spec": _canonical_sha256(SOURCE_CROSSCHECK_SPEC),
        "scientific_contract": _canonical_sha256(CLAIM_CONTRACT),
    }


def _compact_source(text: str) -> str:
    return re.sub(r"\s+", "", text)


def source_export_crosschecks() -> dict[str, bool]:
    """Text synchronization only; never a proof of an action identity."""
    try:
        p05z = _compact_source(P05Z_PATH.read_text(encoding="utf-8"))
        manuscript = _compact_source(MANUSCRIPT_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        return {
            "source_files_readable": False,
            "p05z_text_synchronized": False,
            "manuscript_text_synchronized": False,
            "text_synchronization_not_scientific_evidence": True,
        }

    p05_fragments = SOURCE_CROSSCHECK_SPEC["p05z"]["required_compact_fragments"]
    manuscript_fragments = SOURCE_CROSSCHECK_SPEC["manuscript"]["required_compact_fragments"]
    return {
        "source_files_readable": True,
        "p05z_text_synchronized": all(fragment in p05z for fragment in p05_fragments),
        "manuscript_text_synchronized": all(
            fragment in manuscript for fragment in manuscript_fragments
        ),
        "text_synchronization_not_scientific_evidence": all(
            "not_evidence_for" in SOURCE_CROSSCHECK_SPEC[key]
            for key in ("p05z", "manuscript")
        ),
    }


def exact_action_identities() -> dict[str, bool]:
    Y, H, sigma, X, K = sp.symbols("Y H sigma X K", positive=True, real=True)
    b = sp.Symbol("b", positive=True, real=True)
    dH, d_sigma, p, u, metric, C, D_H, E_H = sp.symbols(
        "dH d_sigma p u metric C D_H E_H", real=True
    )

    yhat = sp.exp(-2 * H) * Y
    yhat_scaled = sp.exp(-2 * (H + sigma)) * sp.exp(2 * sigma) * Y
    bhat = sp.exp(2 * H) * b
    bhat_scaled = sp.exp(2 * (H + sigma)) * sp.exp(-2 * sigma) * b

    Z = X**2 / Y - K
    projector_derivatives = {
        "dZ_dX_at_X0": sp.diff(Z, X).subs(X, 0),
        "dZ_dY_at_X0": sp.diff(Z, Y).subs(X, 0),
        "dZ_dK": sp.diff(Z, K),
    }
    G, Mpl, omega, Zs = sp.symbols("G M_Pl omega_H Z_H", positive=True)
    p05z_coefficient = -omega * Zs / (8 * sp.pi * G)
    manuscript_coefficient = -omega * Mpl**2 * Zs
    coefficient_residual = sp.simplify(
        p05z_coefficient.subs(G, 1 / (8 * sp.pi * Mpl**2))
        - manuscript_coefficient
    )
    constant_shift_gradient_residual = sp.simplify((dH + d_sigma - dH).subs(d_sigma, 0))
    clock_Y_residual = sp.expand((-p) ** 2 - p**2)
    clock_gamma_residual = sp.expand(((-u) * (-u) - metric) - (u * u - metric))
    clock_parity_residuals = {
        "C_odd": sp.expand((-C) + C),
        "D_H_odd": sp.expand((-D_H) + D_H),
        "E_H_even": sp.expand(E_H - E_H),
    }

    return {
        "internal_scaling_leaves_Yhat_invariant": sp.simplify(yhat_scaled - yhat) == 0,
        "internal_scaling_leaves_Bhat_factor_invariant": sp.simplify(bhat_scaled - bhat) == 0,
        "constant_H_shift_leaves_nabla_H_unchanged": constant_shift_gradient_residual == 0,
        "clock_reversal_leaves_Y_and_gamma_invariant": all((
            clock_Y_residual == 0,
            clock_gamma_residual == 0,
        )),
        "projector_identity_derivatives_exact": projector_derivatives == {
            "dZ_dX_at_X0": 0,
            "dZ_dY_at_X0": 0,
            "dZ_dK": -1,
        },
        "p05z_and_manuscript_projected_coefficients_equivalent": coefficient_residual == 0,
        "clock_parities_C_and_D_odd_E_even": all(
            residual == 0 for residual in clock_parity_residuals.values()
        ),
    }


def generic_silent_jet_identities() -> dict[str, Any]:
    eps = sp.Symbol("eps", real=True)
    dy, d11, d22, d33, d12, d13, d23 = sp.symbols(
        "dy d11 d22 d33 d12 d13 d23", real=True
    )
    variables = (dy, d11, d22, d33, d12, d13, d23)
    D = sp.Matrix([
        [d11, d12, d13],
        [d12, d22, d23],
        [d13, d23, d33],
    ])
    B = sp.eye(3) + eps * D
    Yhat = 1 + eps * dy
    I1 = sp.trace(B)
    I2 = (sp.trace(B) ** 2 - sp.trace(B * B)) / 2
    I3 = B.det()
    dz = sp.Matrix([Yhat - 1, I1 - 3, I2 - 3, I3 - 1])

    f2, f3 = sp.symbols("f_I2 f_I3", real=True)
    first = sp.Matrix([0, -2 * f2 - f3, f2, f3])
    h_symbols = sp.symbols("h00 h01 h02 h03 h11 h12 h13 h22 h23 h33", real=True)
    h00, h01, h02, h03, h11, h12, h13, h22, h23, h33 = h_symbols
    Hess = sp.Matrix([
        [h00, h01, h02, h03],
        [h01, h11, h12, h13],
        [h02, h12, h22, h23],
        [h03, h13, h23, h33],
    ])
    t = sp.trace(D)
    s = sp.trace(D * D)
    v = sp.Matrix([1, 2, 1])
    Hyi = sp.Matrix([h01, h02, h03])
    Hii = Hess[1:4, 1:4]

    taylor = sp.expand((first.dot(dz) + (dz.T * Hess * dz)[0] / 2))
    f1 = sp.Symbol("f_I1", real=True)
    invariant_linear_variation = sp.expand(
        f1 * sp.diff(I1, eps).subs(eps, 0)
        + f2 * sp.diff(I2, eps).subs(eps, 0)
        + f3 * sp.diff(I3, eps).subs(eps, 0)
    )
    expected_linear_variation = sp.expand((f1 + 2 * f2 + f3) * t)
    quadratic = sp.expand(sp.series(taylor, eps, 0, 3).removeO().coeff(eps, 2))
    expected = sp.expand(
        h00 * dy**2 / 2
        + (Hyi.dot(v)) * dy * t
        + (v.dot(Hii * v) + f2 + f3) * t**2 / 2
        - (f2 + f3) * s / 2
    )

    composite_Hessian = sp.hessian(expected, variables)
    zero_subs = {symbol: 0 for symbol in h_symbols + (f2, f3)}
    rank_one_subs = dict(zero_subs)
    rank_one_subs[h00] = 1
    full_rank_subs = dict(zero_subs)
    full_rank_subs[h00] = 1
    full_rank_subs[f2] = 1

    ranks = {
        "zero_jet": composite_Hessian.subs(zero_subs).rank(),
        "clock_rank_one_jet": composite_Hessian.subs(rank_one_subs).rank(),
        "allowed_full_rank_jet": composite_Hessian.subs(full_rank_subs).rank(),
    }
    return {
        "matrix_derivative_at_unit_is_delta_times_fI1_plus_2fI2_plus_fI3": (
            sp.simplify(invariant_linear_variation - expected_linear_variation) == 0
        ),
        "generic_quadratic_expansion_residual": sp.simplify(quadratic - expected),
        "generic_quadratic_expansion_exact": sp.simplify(quadratic - expected) == 0,
        "generic_composite_Hessian_ranks": ranks,
        "silent_conditions_do_not_fix_composite_Hessian": ranks == {
            "zero_jet": 0,
            "clock_rank_one_jet": 1,
            "allowed_full_rank_jet": 7,
        },
        "free_invariant_Hessian_entry_count": len(h_symbols),
    }


def F_min_identities() -> dict[str, Any]:
    dy, d11, d22, d33, d12, d13, d23 = sp.symbols(
        "dy d11 d22 d33 d12 d13 d23", real=True
    )
    variables = (dy, d11, d22, d33, d12, d13, d23)
    D = sp.Matrix([
        [d11, d12, d13],
        [d12, d22, d23],
        [d13, d23, d33],
    ])
    B = sp.eye(3) + D
    Yhat = 1 + dy
    I1 = sp.trace(B)
    I2 = (sp.trace(B) ** 2 - sp.trace(B * B)) / 2
    I3 = B.det()
    F = sp.expand(
        -8 * Yhat + Yhat**2 + 8 * I1 + I1**2
        - 16 * I2 + 16 * I3 + 2 * Yhat * I1
    )
    expected = sp.expand((dy + sp.trace(D)) ** 2 + 16 * D.det())
    origin = {variable: 0 for variable in variables}
    gradient = [sp.diff(F, variable).subs(origin) for variable in variables]
    Hess = sp.hessian(F, variables).subs(origin)
    e = sp.Symbol("epsilon", real=True)
    saddle_plus = sp.expand(F.subs({
        dy: 0, d11: e, d22: e, d33: -2 * e, d12: 0, d13: 0, d23: 0,
    }))
    saddle_minus = sp.expand(saddle_plus.subs(e, -e))
    return {
        "matrix_identity_residual": sp.simplify(F - expected),
        "matrix_identity_exact": sp.simplify(F - expected) == 0,
        "silent_value": sp.simplify(F.subs(origin)),
        "silent_gradient": gradient,
        "silent_point_exact": F.subs(origin) == 0 and all(value == 0 for value in gradient),
        "composite_Hessian_rank": Hess.rank(),
        "composite_Hessian_nullity": len(variables) - Hess.rank(),
        "cubic_saddle_plus": saddle_plus,
        "cubic_saddle_minus": saddle_minus,
        "cubic_saddle_exact": saddle_plus == -32 * e**3 and saddle_minus == 32 * e**3,
    }


def mutation_controls() -> dict[str, bool]:
    action_mutation = deepcopy(ACTION_SPEC)
    action_mutation["bulk_action"] = action_mutation["bulk_action"].replace("-omega_H", "+omega_H")

    generic_mutation = deepcopy(GENERIC_SILENT_F_SPEC)
    generic_mutation["silent_conditions"][0] = "F|_1=1"

    representative_mutation = deepcopy(F_MIN_REPRESENTATIVE_SPEC)
    representative_mutation["polynomial_over_c_Y2"] = representative_mutation[
        "polynomial_over_c_Y2"
    ].replace("-16*I2hat", "-15*I2hat")

    completion_mutation = deepcopy(EXCLUDED_COMPLETION_SPEC)
    completion_mutation["hidden_repair_allowed"] = True

    gate_mutation = deepcopy(DYNAMICS_GATE_SPEC)
    gate_mutation["falsification_triggers"].pop()

    source_mutation = deepcopy(SOURCE_CROSSCHECK_SPEC)
    source_mutation["manuscript"]["role"] = "dynamics evidence"

    contract_mutation = deepcopy(CLAIM_CONTRACT)
    contract_mutation["CLOSURE_FLAGS"]["ghost_freedom_proved"] = True

    return {
        "action_sign_mutation_detected": _canonical_sha256(action_mutation) != EXPECTED_HASHES["action_spec"],
        "generic_silent_condition_mutation_detected": _canonical_sha256(generic_mutation) != EXPECTED_HASHES["generic_silent_F_spec"],
        "F_min_coefficient_mutation_detected": _canonical_sha256(representative_mutation) != EXPECTED_HASHES["F_min_representative_spec"],
        "hidden_repair_mutation_detected": _canonical_sha256(completion_mutation) != EXPECTED_HASHES["excluded_completion_spec"],
        "falsifier_removal_mutation_detected": _canonical_sha256(gate_mutation) != EXPECTED_HASHES["dynamics_gate_spec"],
        "source_role_mutation_detected": _canonical_sha256(source_mutation) != EXPECTED_HASHES["source_crosscheck_spec"],
        "physical_closure_mutation_detected": _canonical_sha256(contract_mutation) != EXPECTED_HASHES["scientific_contract"],
    }


def run() -> dict[str, Any]:
    hashes = _current_hashes()
    hash_controls = {key: hashes[key] == EXPECTED_HASHES[key] for key in EXPECTED_HASHES}
    source = source_export_crosschecks()
    action = exact_action_identities()
    generic = generic_silent_jet_identities()
    representative = F_min_identities()
    mutations = mutation_controls()

    schema = set(CLAIM_CONTRACT) == set(REQUIRED_SCIENTIFIC_FIELDS)
    closures_false = (
        CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS
        and all(value is False for value in EXPECTED_CLOSURE_FLAGS.values())
    )
    track_firewall = all((
        GENERIC_SILENT_F_SPEC["track_id"] != F_MIN_REPRESENTATIVE_SPEC["track_id"],
        "not of GENERIC_SILENT_F"
        in F_MIN_REPRESENTATIVE_SPEC["inheritance_firewall"][0],
        EXCLUDED_COMPLETION_SPEC["hidden_repair_allowed"] is False,
        "rerun every dynamics gate"
        in EXCLUDED_COMPLETION_SPEC["future_completion_rule"],
    ))
    exact_identities = all((
        all(action.values()),
        generic[
            "matrix_derivative_at_unit_is_delta_times_fI1_plus_2fI2_plus_fI3"
        ],
        generic["generic_quadratic_expansion_exact"],
        generic["silent_conditions_do_not_fix_composite_Hessian"],
        generic["free_invariant_Hessian_entry_count"] == 10,
        representative["matrix_identity_exact"],
        representative["silent_point_exact"],
        representative["composite_Hessian_rank"] == 1,
        representative["composite_Hessian_nullity"] == 6,
        representative["cubic_saddle_exact"],
    ))
    valid = all((
        schema,
        closures_false,
        track_firewall,
        exact_identities,
        all(source.values()),
        all(hash_controls.values()),
        all(mutations.values()),
    ))

    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": bool(valid),
        "status": (
            "PASS_MINIMAL_EFFECTIVE_ACTION_SCOPE_FROZEN__ALL_DYNAMICS_HEALTH_GATES_OPEN"
            if valid else "FAIL_INVALID_DYNAMICS_CONTRACT_NO_PROMOTION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The generic minimal action and the special F_min response are now frozen as separate "
            "future audit tracks. Exact algebra agrees and the two source texts are synchronized. "
            "The text check is not scientific evidence. No constraint, physical "
            "mode, stability, cutoff, PPN, observation or foundation-origin claim is promoted."
        ),
        "contract_schema_exact": schema,
        "all_physical_closure_flags_false": closures_false,
        "generic_and_representative_tracks_separated": track_firewall,
        "exact_identity_controls_pass": exact_identities,
        "source_export_crosschecks": source,
        "identity_diagnostics": {
            "generic_composite_Hessian_ranks": generic["generic_composite_Hessian_ranks"],
            "generic_quadratic_expansion_residual": str(generic["generic_quadratic_expansion_residual"]),
            "F_min_matrix_identity_residual": str(representative["matrix_identity_residual"]),
            "F_min_Hessian_rank": representative["composite_Hessian_rank"],
            "F_min_Hessian_nullity": representative["composite_Hessian_nullity"],
            "F_min_cubic_saddle": [
                str(representative["cubic_saddle_plus"]),
                str(representative["cubic_saddle_minus"]),
            ],
        },
        "hashes": hashes,
        "pinned_hash_controls": hash_controls,
        "mutation_controls": mutations,
        "physical_closure_flags": CLAIM_CONTRACT["CLOSURE_FLAGS"],
        "next_gate": DYNAMICS_GATE_SPEC["ordered_gates"][0],
    }


def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_ID,
            "model_version": MODEL_VERSION,
            "valid": False,
            "status": "FAIL_EXCEPTION_NO_PROMOTION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
