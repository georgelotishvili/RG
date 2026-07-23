"""Exact direct-block diagnostics on the exponential exterior.

The exact exterior keeps the normalized response invariants at the silent
point at every radius.  This gate derives two consequences of that fact: the
direct material-label velocity Hessian of the minimal F sector and the
unitary-gauge medium shift Hessian both vanish.  It also records the spatially
elliptic fixed-field H--H block.

These are unreduced blocks.  Their degeneration is a necessary warning that
forbids dynamic promotion before the full constraint/gauge reduction, but it
is not a proof of a physical ghost, strong coupling, ill-posedness, or theory
failure.  Extra constraints or auxiliary/gauge removal remain live outcomes.
The physical verdict is therefore OPEN.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any

import sympy as sp


CLAIM_ID = "W2_EXACT_EXTERIOR_DIRECT_BLOCK_WARNING_GATE_002"
MODEL_VERSION = "W2-EXTERIOR-DIRECT-BLOCK-WARNING-v2.1-PINNED"
HERE = Path(__file__).resolve().parent

UPSTREAM_PIN_SPEC: dict[str, Any] = {
    "w2_32": {
        "claim_id": "W2_EFFECTIVE_ACTION_DYNAMICS_CONTRACT_001",
        "model_version": "W2-EFFECTIVE-ACTION-DYNAMICS-CONTRACT-v1.1-SYMBOLIC-CONTROLS",
        "hashes": {
            "action_spec": "02E757C7406101C2E91723ED28FBE7BDD3E4F547A3968F1BD11641F97CDFF7E2",
            "generic_silent_F_spec": "865752BEDBE5463801DEEC64FFC5831B91891C0C750F5997BBD4A7CE6C25E0F9",
            "F_min_representative_spec": "922B8C2CC22C3F9FF9C30D8D1AFCFB1DDF95A0F9E72BDC01168D7F2A0BC42B9B",
            "excluded_completion_spec": "60EFCF610A307DE2FECE9CBEFA6FFF3A273C4A975DC33CC1EE3706A402071319",
            "dynamics_gate_spec": "4767D085F50D670CCB38C446A8D7D2CB78AFD2054B05CC951F31D14995CF192A",
            "source_crosscheck_spec": "0CB5D26E351EF97812770BDDCB458F0FB2DDCB8B3798EF28824312B776F47C50",
            "scientific_contract": "6CED59206375068BC9A65C427D78FEBA3FADD8287EE36778B4D1A9E56E0AB5AB",
        },
    },
    "w2_33": {
        "claim_id": "W2_ADM_DIRAC_STRUCTURAL_CONSTRAINT_GATE_001",
        "model_version": "W2-ADM-DIRAC-MINIMAL-ACTION-v1.1-FROZEN-INVARIANT-FAIL-CLOSED",
        "hashes": {
            "action_spec": "02E757C7406101C2E91723ED28FBE7BDD3E4F547A3968F1BD11641F97CDFF7E2",
            "adm_gauge_spec": "3A4CDD1F9ADD897CE9E786B53F9F737176F1EF14F9C3F23AA6B3093D7F6A0658",
            "invariant_response_spec": "EB4D0E5E83159F089068FEC5C662D57574BEAB68AD4F7E7C180CC8039355AF9C",
            "dirac_scope_spec": "E55D25A4C0E12F237779BFC3EC87F247DB4BB3DA9F3A96D621DB5B16F23E2CCC",
            "scientific_contract": "FA6431F6BE588284CF8E96B1F6AA20C9C9C0768BF0C9D21B1CD395B7D7BEC6AB",
        },
    },
    "w2_34": {
        "claim_id": "W2_SILENT_MINKOWSKI_UNREDUCED_ACTION_PERTURBATIVE_AUDIT_001",
        "model_version": "W2-SILENT-MINKOWSKI-UNREDUCED-ACTION-v1.1-DEPENDENCY-LOCKED",
        "hashes": {
            "jet_spec": "33bbd5a1a68168b1e82e659fecd9f95ec9c2de014071b3d76c65c05f479d2f56",
            "Fmin_spec": "74c898d7e5d58df3c7c58e94a88bdc0f0b24dd0b67f56d45eef3292eedb3d5d7",
            "dependency_spec": "a7a5f415438b183e1ad00ad3413d43a57ea3d47f14b4e87eb4096dc358038c30",
            "outcomes": "3d3353e3f3497a83329e3a86f3157d7ab8dc9112e1da9eee77e94babee7f909b",
            "closure_flags": "e59b0e51ecf7e223d4df12afeae85f4b71bcdd491520174964ddc3d2f742c49b",
            "scientific_contract": "585e277ec717a852fdd71f9993fbd409f847148352d33ea59ef49473cdfc4971",
        },
    },
}

REQUIRED_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

EVIDENCE_KEYS = frozenset({
    "unit_normalized_clock_invariant_exact",
    "unit_normalized_strain_eigenvalues_exact",
    "material_velocity_hessian_derived_exact",
    "silent_material_velocity_hessian_zero_exact",
    "shift_hessian_matches_w2_33_normalization_exact",
    "silent_shift_hessian_zero_exact",
    "HH_principal_polynomial_has_no_time_term",
    "HH_spatial_principal_hessian_positive",
    "radial_H_gradient_vanishes_asymptotically",
    "ZH_matches_exact_exterior_profile",
})

UPSTREAM_KEYS = frozenset({
    "w2_32_valid_and_self_pinned",
    "w2_33_valid_and_self_pinned",
    "w2_34_valid_and_self_pinned",
    "upstream_claim_identities_exact",
    "upstream_physical_reduction_remains_open",
})

DECISION_KEYS = frozenset({
    "direct_block_warning",
    "constraint_or_gauge_removal_open",
    "promotion_not_authorized",
    "physical_verdict_open",
    "physical_health_proved",
    "physical_failure_proved",
    "upstream_integrity_satisfied",
})


def frozen_outcomes() -> dict[str, bool]:
    return {
        "exact_exterior_unit_normalized_invariants_proved": True,
        "direct_material_velocity_block_zero_at_every_radius_proved": True,
        "medium_ADM_shift_hessian_zero_at_every_radius_proved": True,
        "fixed_field_HH_block_spatial_ellipticity_proved": True,
        "fixed_field_HH_block_has_time_principal_term": False,
        "radial_H_gradient_vanishes_asymptotically_proved": True,
        "unreduced_direct_block_degeneracy_warning_proved": True,
        "full_constraint_reduced_exterior_symbol_derived": False,
        "constraint_or_gauge_removal_of_null_directions_excluded": False,
        "physical_strong_coupling_or_instability_proved": False,
        "physical_dynamic_health_proved": False,
        "full_exterior_strong_hyperbolicity_proved": False,
        "dynamic_exterior_promotion_authorized": False,
        "physical_dynamic_verdict_closed": False,
        "exact_static_background_closure_retained": True,
    }


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "exact_exponential_background_embedding_retained": True,
        "direct_block_warning_closed": True,
        "full_ADM_Dirac_reduction_closed": False,
        "null_directions_classified_as_physical_or_auxiliary": False,
        "full_coupled_exterior_spectrum_closed": False,
        "uniform_exterior_hyperbolicity_closed": False,
        "strong_coupling_EFT_control_closed": False,
        "physical_dynamic_verdict_closed": False,
        "full_PPN_or_observational_validation_closed": False,
    }


EXPECTED_OUTCOMES = frozen_outcomes()
EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "On the exact H=m/r exterior of the displayed minimal action, derive the "
        "vanishing direct material-label and medium-shift Hessians at the silent "
        "point and the fixed-field spatial H--H block.  Treat the degeneracy only "
        "as a necessary warning: dynamic promotion is not authorized and the "
        "physical verdict remains open until the constraints are reduced."
    ),
    "TYPE": "EXACT_UNREDUCED_BLOCK_IDENTITIES_WITH_FAIL_CLOSED_PROMOTION_WARNING",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "The displayed minimal RefG action is used with omega_H>0, no omitted "
        "completion operators, the exact static fields Phi=t, phi^A=x^A, H=m/r, "
        "and a C2 response satisfying the silent-point conditions."
    ),
    "DOMAIN": "The ordinary-matter-free exact exterior r>=r_c>0 with m>0.",
    "CONVENTIONS": (
        "Signature (+---). Principal covectors are evaluated in a local orthonormal "
        "medium frame. Direct/unreduced Hessians are never identified with the "
        "constraint-reduced physical kinetic matrix."
    ),
    "FREEDOM_LEDGER": {
        "response": "arbitrary C2 F subject to the silent-point value and first derivatives",
        "completion_operators": "excluded from this action version",
        "constraint_class": "uncomputed on the silent exterior",
        "data_or_fit": "none",
    },
    "DEPENDENCIES": {
        "files": [
            "RefG/work 2/w2_32_effective_action_dynamics_contract.py",
            "RefG/work 2/w2_33_adm_dirac_constraint_gate.py",
            "RefG/work 2/w2_34_silent_vacuum_reduced_spectrum_gate.py",
        ],
        "frozen_upstream_pins": UPSTREAM_PIN_SPEC,
    },
    "METHOD": (
        "Import and enforce the self-pinned upstream reports. Substitute the exact "
        "branch into the normalized invariants. Derive the material Hessian from "
        "Delta Bhat=-v v^T and the shift Hessian from the full local ADM Lagrangian "
        "density, then set F_,B=0. Compute the fixed-field H principal polynomial."
    ),
    "PASS_CONDITION": (
        "PASS means that the direct-block identities, upstream integrity, hashes and "
        "mutation controls are exact, while promotion is not authorized and every "
        "constraint-reduced physical verdict remains open."
    ),
    "FAIL_CONDITION": (
        "An algebraic mismatch, upstream invalidity or drift, a hard-coded conclusion, "
        "or promotion of the unreduced warning to a physical failure invalidates this audit."
    ),
    "FALSIFIER": (
        "A counterexample to a displayed direct-block identity falsifies that identity. "
        "A completed constraint reduction does not falsify this warning; it resolves "
        "the currently open physical interpretation in a later gate."
    ),
    "RESIDUAL": "Zero for the exact branch, Hessian and principal-polynomial identities.",
    "ERROR_BOUND": "Zero symbolic error; no numerical fit, cutoff or physical spectrum estimate.",
    "VALIDITY_HEALTH": (
        "The direct rank loss is proved. Whether its directions are physical, gauge, "
        "auxiliary, constrained, healthy or strongly coupled is not proved. A completed "
        "classification requires separate positive health or failure evidence; absence of "
        "failure is never treated as proof of health."
    ),
    "BRANCHES": {
        "exact_static_background": "RETAINED",
        "direct_material_and_shift_blocks": "DEGENERATE_NECESSARY_WARNING",
        "fixed_field_HH_operator": "SPATIALLY_ELLIPTIC",
        "constraint_or_gauge_removal": "OPEN",
        "physical_dynamic_verdict": "OPEN",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "pre-observational direct-block audit"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "physical reduced evolution is open"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data, target or calibration"},
    "IDENTIFIABILITY": (
        "The direct blocks are identifiable algebraically. Their physical-mode content "
        "is not identifiable before the full Dirac/gauge reduction."
    ),
    "BENCHMARK": (
        "The shift Hessian must equal the w2_33 Lagrangian-density normalization, "
        "and the r->infinity limit must return the silent Minkowski diagnostics."
    ),
    "CLOSURE_FLAGS": frozen_closure_flags(),
    "CROSSCHECK": (
        "The covariant material Hessian and the unitary-gauge medium shift Hessian "
        "are independently differentiated and compared with the exact w2_33 formula."
    ),
    "PROVENANCE": {"date": "2026-07-23", "data": "none", "code_version": "w2_35 v2.1"},
    "FILES": ["RefG/work 2/w2_35_exponential_exterior_coupled_symbol_gate.py"],
}

CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def _sha(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()


EXPECTED_CONTRACT_SHA256 = "E1A2ABFDC6FDE009A391DA2D0BE3D55759C3EE95A8070B64CE3FD53612E210FC"
EXPECTED_OUTCOMES_SHA256 = "BB2DC16DE55CECD5C4CCCD62E251E62233EA1A62207952ED1158B010932425D5"
EXPECTED_UPSTREAM_PIN_SHA256 = "B3FD1F929A13B624B1310E5973529DBF785AF6FEA7E22582E072757252368409"


def _load_module(filename: str, tag: str) -> ModuleType:
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(tag, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def load_upstream_reports() -> dict[str, Any]:
    w32 = _load_module("w2_32_effective_action_dynamics_contract.py", "w2_32_for_w2_35")
    w33 = _load_module("w2_33_adm_dirac_constraint_gate.py", "w2_33_for_w2_35")
    w34 = _load_module("w2_34_silent_vacuum_reduced_spectrum_gate.py", "w2_34_for_w2_35")
    reports = {"w2_32": w32.run(), "w2_33": w33.run(), "w2_34": w34.evaluate()}
    return {"modules": {"w2_32": w32, "w2_33": w33, "w2_34": w34}, "reports": reports}


def upstream_integrity_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    loaded = load_upstream_reports()
    modules = loaded["modules"]
    reports = loaded["reports"]
    w32, w33, w34 = modules["w2_32"], modules["w2_33"], modules["w2_34"]
    r32, r33, r34 = reports["w2_32"], reports["w2_33"], reports["w2_34"]

    expected32 = UPSTREAM_PIN_SPEC["w2_32"]["hashes"]
    expected33 = UPSTREAM_PIN_SPEC["w2_33"]["hashes"]
    expected34 = UPSTREAM_PIN_SPEC["w2_34"]["hashes"]
    controls = {
        "w2_32_valid_and_self_pinned": all((
            r32.get("valid") is True,
            r32.get("hashes") == expected32,
            all(r32.get("pinned_hash_controls", {}).values()),
        )),
        "w2_33_valid_and_self_pinned": all((
            r33.get("valid") is True,
            r33.get("hashes") == expected33,
            w33.payload_integrity_screen(w33.ACTION_SPEC, w33.DIRAC_SCOPE_SPEC, w33.CLAIM_CONTRACT),
        )),
        "w2_34_valid_and_self_pinned": all((
            r34.get("valid") is True,
            r34.get("hashes") == expected34,
            all(r34.get("hash_controls", {}).values()),
            w34.contract_valid(w34.CLAIM_CONTRACT),
        )),
        "upstream_claim_identities_exact": all((
            w32.CLAIM_ID == UPSTREAM_PIN_SPEC["w2_32"]["claim_id"],
            w33.CLAIM_ID == UPSTREAM_PIN_SPEC["w2_33"]["claim_id"],
            w34.CLAIM_ID == UPSTREAM_PIN_SPEC["w2_34"]["claim_id"],
            w32.MODEL_VERSION == UPSTREAM_PIN_SPEC["w2_32"]["model_version"],
            w33.MODEL_VERSION == UPSTREAM_PIN_SPEC["w2_33"]["model_version"],
            w34.MODEL_VERSION == UPSTREAM_PIN_SPEC["w2_34"]["model_version"],
            w32.EXPECTED_HASHES == expected32,
            {
                "action_spec": w33.EXPECTED_ACTION_SPEC_SHA256,
                "adm_gauge_spec": w33.EXPECTED_ADM_GAUGE_SPEC_SHA256,
                "invariant_response_spec": w33.EXPECTED_INVARIANT_RESPONSE_SPEC_SHA256,
                "dirac_scope_spec": w33.EXPECTED_DIRAC_SCOPE_SPEC_SHA256,
                "scientific_contract": w33.EXPECTED_SCIENTIFIC_CONTRACT_SHA256,
            } == expected33,
            {
                "jet_spec": w34.EXPECTED_JET_SPEC_SHA256,
                "Fmin_spec": w34.EXPECTED_FMIN_SPEC_SHA256,
                "dependency_spec": w34.EXPECTED_DEPENDENCY_SPEC_SHA256,
                "outcomes": w34.EXPECTED_OUTCOMES_SHA256,
                "closure_flags": w34.EXPECTED_CLOSURE_SHA256,
                "scientific_contract": w34.EXPECTED_SCIENTIFIC_CONTRACT_SHA256,
            } == expected34,
            r32.get("artifact") == w32.CLAIM_ID,
            r33.get("artifact") == w33.CLAIM_ID,
            r34.get("artifact") == w34.CLAIM_ID,
            r32.get("model_version") == UPSTREAM_PIN_SPEC["w2_32"]["model_version"],
            r33.get("model_version") == UPSTREAM_PIN_SPEC["w2_33"]["model_version"],
            r34.get("model_version") == UPSTREAM_PIN_SPEC["w2_34"]["model_version"],
        )),
        "upstream_physical_reduction_remains_open": all((
            r33["outcomes"]["silent_background_constraint_classification_proved"] is False,
            r33["outcomes"]["silent_background_strong_coupling_excluded"] is False,
            r34["outcomes"]["full_metric_constraint_reduction_performed"] is False,
            r34["outcomes"]["reduced_physical_spectrum_or_DOF_health_proved"] is False,
        )),
    }
    diagnostics = {
        "claim_ids": {key: loaded["modules"][key].CLAIM_ID for key in loaded["modules"]},
        "hashes": {key: reports[key]["hashes"] for key in reports},
        "statuses": {key: reports[key]["status"] for key in reports},
    }
    return controls, diagnostics


def exact_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    r, m = sp.symbols("r m", positive=True, finite=True)
    omega, mpl = sp.symbols("omega_H M_Pl", positive=True, finite=True)
    M4, N, sqrt_h = sp.symbols("M_star4 N sqrt_h", positive=True, finite=True)
    H = sp.symbols("H", real=True)
    k0, k1, k2, k3 = sp.symbols("k_0 k_1 k_2 k_3", real=True)
    v_symbols = sp.symbols("v_1:4", real=True)
    v = sp.Matrix(v_symbols)
    n_symbols = sp.symbols("N_1:4", real=True)
    shift = sp.Matrix(n_symbols)
    f11, f22, f33, f12, f13, f23 = sp.symbols(
        "F11 F22 F33 F12 F13 F23", real=True,
    )
    F_B = sp.Matrix([[f11, f12, f13], [f12, f22, f23], [f13, f23, f33]])
    silent = {item: 0 for item in (f11, f22, f33, f12, f13, f23)}

    profile = m / r
    y = sp.exp(2 * profile)
    b_eigenvalue = sp.exp(-2 * profile)
    y_hat = sp.simplify(sp.exp(-2 * profile) * y)
    b_hat = sp.simplify(sp.exp(2 * profile) * b_eigenvalue)

    # In a normalized local medium frame, the velocity contribution is
    # Delta Bhat=-v v^T. Differentiating the Lagrangian, rather than inserting a
    # zero matrix by hand, gives 2 M_*^4 F_B.
    delta_b_velocity = -v * v.T
    F_linear_velocity = sum(
        F_B[A, B] * delta_b_velocity[A, B] for A in range(3) for B in range(3)
    )
    L_velocity = sp.expand(-M4 * F_linear_velocity)
    material_hessian = sp.hessian(L_velocity, v_symbols)
    expected_material_hessian = 2 * M4 * F_B
    silent_material_hessian = material_hessian.subs(silent)

    # Repeat w2_33's Lagrangian-density ADM derivation, including sign and all
    # nonzero scalar prefactors.
    e2H = sp.exp(2 * H)
    delta_b_shift = -e2H * shift * shift.T / N**2
    F_linear_shift = sum(
        F_B[A, B] * delta_b_shift[A, B] for A in range(3) for B in range(3)
    )
    L_shift = sp.expand(-N * sqrt_h * M4 * F_linear_shift)
    shift_hessian = sp.hessian(L_shift, n_symbols)
    expected_shift_hessian = 2 * sqrt_h * M4 * e2H * F_B / N
    silent_shift_hessian = shift_hessian.subs(silent)

    # Consume w2_33's independently derived matrix, not merely its spelling.
    loaded = load_upstream_reports()
    w33_module = loaded["modules"]["w2_33"]
    _, w33_shift_diagnostics = w33_module.shift_hessian_controls()
    w33_expected_shift_hessian = w33_shift_diagnostics["expected_shift_hessian"]
    local_symbols = {symbol.name: symbol for symbol in expected_shift_hessian.free_symbols}
    local_symbols.update({
        "M4": M4,
        "mu1": f11,
        "mu2": f22,
        "mu3": f33,
    })
    w33_to_local = {
        symbol: local_symbols[symbol.name]
        for symbol in w33_expected_shift_hessian.free_symbols
        if symbol.name in local_symbols
    }
    imported_shift_hessian = sp.simplify(
        w33_expected_shift_hessian.xreplace(w33_to_local)
    )
    local_invariant_eigenframe_shift_hessian = expected_shift_hessian.subs({
        f12: 0, f13: 0, f23: 0,
    })

    # Derive the fixed-field H principal block directly from
    # gamma^{mu nu}=u^mu u^nu-g^{mu nu} in a local orthonormal medium frame.
    eta_inverse = sp.diag(1, -1, -1, -1)
    medium_u = sp.Matrix([1, 0, 0, 0])
    gamma_inverse = medium_u * medium_u.T - eta_inverse
    covector = sp.Matrix([k0, k1, k2, k3])
    z_h_principal = sp.expand((covector.T * gamma_inverse * covector)[0])
    p_h = sp.expand(omega * mpl**2 * z_h_principal)
    p_h_spatial_hessian = sp.hessian(p_h, (k1, k2, k3))
    oriented_radial_derivative = sp.diff(profile, r)
    radial_gradient_magnitude = sp.simplify(
        -sp.exp(-profile) * oriented_radial_derivative
    )
    z_h = sp.simplify(radial_gradient_magnitude**2)

    controls = {
        "unit_normalized_clock_invariant_exact": y_hat == 1,
        "unit_normalized_strain_eigenvalues_exact": b_hat == 1,
        "material_velocity_hessian_derived_exact": (
            sp.simplify(material_hessian - expected_material_hessian) == sp.zeros(3)
        ),
        "silent_material_velocity_hessian_zero_exact": silent_material_hessian == sp.zeros(3),
        "shift_hessian_matches_w2_33_normalization_exact": (
            sp.simplify(shift_hessian - expected_shift_hessian) == sp.zeros(3)
            and sp.simplify(
                imported_shift_hessian - local_invariant_eigenframe_shift_hessian
            ) == sp.zeros(3)
        ),
        "silent_shift_hessian_zero_exact": silent_shift_hessian == sp.zeros(3),
        "HH_principal_polynomial_has_no_time_term": all((
            gamma_inverse == sp.diag(0, 1, 1, 1),
            sp.diff(p_h, k0, 2) == 0,
        )),
        "HH_spatial_principal_hessian_positive": (
            p_h_spatial_hessian == 2 * omega * mpl**2 * sp.eye(3)
        ),
        "radial_H_gradient_vanishes_asymptotically": all((
            oriented_radial_derivative == -m / r**2,
            sp.limit(radial_gradient_magnitude, r, sp.oo) == 0,
        )),
        "ZH_matches_exact_exterior_profile": (
            z_h == m**2 * sp.exp(-2 * m / r) / r**4
        ),
    }
    diagnostics = {
        "Y_hat": y_hat,
        "B_hat_eigenvalue": b_hat,
        "material_velocity_lagrangian": L_velocity,
        "material_velocity_hessian": material_hessian,
        "silent_material_velocity_hessian": silent_material_hessian,
        "shift_lagrangian": L_shift,
        "shift_hessian": shift_hessian,
        "w2_33_imported_expected_shift_hessian": imported_shift_hessian,
        "local_invariant_eigenframe_shift_hessian": (
            local_invariant_eigenframe_shift_hessian
        ),
        "silent_shift_hessian": silent_shift_hessian,
        "gamma_inverse_local_medium_frame": gamma_inverse,
        "Z_H_principal": z_h_principal,
        "P_HH": p_h,
        "oriented_dH_dr": oriented_radial_derivative,
        "radial_H_gradient_magnitude": radial_gradient_magnitude,
        "Z_H": z_h,
    }
    return controls, diagnostics


def _strict_bool_map(value: Any, keys: frozenset[str]) -> bool:
    return isinstance(value, dict) and set(value) == set(keys) and all(
        type(item) is bool for item in value.values()
    )


def warning_decision(
    evidence: dict[str, bool],
    upstream: dict[str, bool],
    *,
    constraint_reduction_complete: bool,
    reduced_classification_complete: bool,
    reduced_physical_health_evidence: bool,
    reduced_physical_failure_evidence: bool,
) -> dict[str, bool]:
    evidence_valid = _strict_bool_map(evidence, EVIDENCE_KEYS) and all(evidence.values())
    upstream_valid = _strict_bool_map(upstream, UPSTREAM_KEYS) and all(upstream.values())
    direct_degeneracy = bool(
        upstream_valid
        and evidence_valid
        and evidence["silent_material_velocity_hessian_zero_exact"]
        and evidence["silent_shift_hessian_zero_exact"]
    )
    constraint_open = bool(direct_degeneracy and not constraint_reduction_complete)
    classification_complete = bool(
        direct_degeneracy
        and constraint_reduction_complete
        and reduced_classification_complete
    )
    resolved_healthy = bool(
        classification_complete
        and reduced_physical_health_evidence
        and not reduced_physical_failure_evidence
    )
    resolved_failure = bool(
        classification_complete
        and reduced_physical_failure_evidence
        and not reduced_physical_health_evidence
    )
    verdict_open = bool(
        direct_degeneracy and not resolved_healthy and not resolved_failure
    )
    return {
        "direct_block_warning": direct_degeneracy,
        "constraint_or_gauge_removal_open": constraint_open,
        "promotion_not_authorized": bool(direct_degeneracy and not resolved_healthy),
        "physical_verdict_open": verdict_open,
        "physical_health_proved": resolved_healthy,
        "physical_failure_proved": resolved_failure,
        "upstream_integrity_satisfied": upstream_valid,
    }


def definition_controls() -> tuple[dict[str, bool], dict[str, bool]]:
    contract_mutation = deepcopy(CLAIM_CONTRACT)
    contract_mutation["BRANCHES"]["physical_dynamic_verdict"] = "FAIL"
    outcomes_mutation = deepcopy(EXPECTED_OUTCOMES)
    outcomes_mutation["physical_strong_coupling_or_instability_proved"] = True
    controls = {
        "contract_schema_exact": set(CLAIM_CONTRACT) == set(REQUIRED_FIELDS),
        "claim_identity_exact": all((
            CLAIM_CONTRACT["CLAIM_ID"] == CLAIM_ID,
            CLAIM_CONTRACT["MODEL_VERSION"] == MODEL_VERSION,
        )),
        "outcome_and_closure_ledgers_exact": all((
            frozen_outcomes() == EXPECTED_OUTCOMES,
            frozen_closure_flags() == EXPECTED_CLOSURE_FLAGS,
            CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS,
        )),
        "upstream_pins_hash_exact": (
            _sha(UPSTREAM_PIN_SPEC) == EXPECTED_UPSTREAM_PIN_SHA256
        ),
        "contract_hash_exact": _sha(CLAIM_CONTRACT) == EXPECTED_CONTRACT_SHA256,
        "outcomes_hash_exact": _sha(EXPECTED_OUTCOMES) == EXPECTED_OUTCOMES_SHA256,
        "physical_failure_not_claimed": all((
            EXPECTED_OUTCOMES["physical_strong_coupling_or_instability_proved"] is False,
            EXPECTED_OUTCOMES["physical_dynamic_verdict_closed"] is False,
            CLAIM_CONTRACT["BRANCHES"]["physical_dynamic_verdict"] == "OPEN",
        )),
        "contract_and_outcome_overclaim_mutations_detected": all((
            _sha(contract_mutation) != EXPECTED_CONTRACT_SHA256,
            _sha(outcomes_mutation) != EXPECTED_OUTCOMES_SHA256,
        )),
    }
    return controls, {"contract": contract_mutation, "outcomes": outcomes_mutation}


def mutation_controls(
    evidence: dict[str, bool], upstream: dict[str, bool], decision: dict[str, bool],
) -> dict[str, bool]:
    missing = dict(evidence)
    missing.pop(next(iter(EVIDENCE_KEYS)))
    false_evidence = all(
        not all({**evidence, key: False}.values()) for key in EVIDENCE_KEYS
    )
    upstream_false = dict(upstream)
    upstream_false[next(iter(upstream_false))] = False
    unresolved_failure_assertion = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=False,
        reduced_classification_complete=False,
        reduced_physical_health_evidence=False,
        reduced_physical_failure_evidence=True,
    )
    resolved_healthy = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=True,
        reduced_classification_complete=True,
        reduced_physical_health_evidence=True,
        reduced_physical_failure_evidence=False,
    )
    resolved_failure = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=True,
        reduced_classification_complete=True,
        reduced_physical_health_evidence=False,
        reduced_physical_failure_evidence=True,
    )
    classified_without_evidence = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=True,
        reduced_classification_complete=True,
        reduced_physical_health_evidence=False,
        reduced_physical_failure_evidence=False,
    )
    contradictory_evidence = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=True,
        reduced_classification_complete=True,
        reduced_physical_health_evidence=True,
        reduced_physical_failure_evidence=True,
    )
    return {
        "each_single_false_evidence_item_blocks_audit": false_evidence,
        "missing_extra_nonboolean_evidence_rejected": all((
            not _strict_bool_map(missing, EVIDENCE_KEYS),
            not _strict_bool_map({**evidence, "extra": True}, EVIDENCE_KEYS),
            not _strict_bool_map({**evidence, next(iter(EVIDENCE_KEYS)): 1}, EVIDENCE_KEYS),
        )),
        "upstream_invalidity_blocks_integrity": all((
            not _strict_bool_map(upstream_false, UPSTREAM_KEYS)
            or not all(upstream_false.values()),
            warning_decision(
                evidence,
                upstream_false,
                constraint_reduction_complete=False,
                reduced_classification_complete=False,
                reduced_physical_health_evidence=False,
                reduced_physical_failure_evidence=False,
            )["direct_block_warning"] is False,
        )),
        "failure_requires_completed_constraint_classification": (
            unresolved_failure_assertion["physical_failure_proved"] is False
        ),
        "positive_health_evidence_can_resolve_without_failure": all((
            resolved_healthy["promotion_not_authorized"] is False,
            resolved_healthy["physical_verdict_open"] is False,
            resolved_healthy["physical_health_proved"] is True,
            resolved_healthy["physical_failure_proved"] is False,
        )),
        "failure_conclusion_changes_only_with_reduced_evidence": all((
            decision["physical_failure_proved"] is False,
            resolved_failure["physical_failure_proved"] is True,
        )),
        "classification_without_positive_evidence_remains_open": all((
            classified_without_evidence["promotion_not_authorized"] is True,
            classified_without_evidence["physical_verdict_open"] is True,
            classified_without_evidence["physical_health_proved"] is False,
            classified_without_evidence["physical_failure_proved"] is False,
        )),
        "contradictory_health_and_failure_evidence_promotes_neither": all((
            contradictory_evidence["promotion_not_authorized"] is True,
            contradictory_evidence["physical_verdict_open"] is True,
            contradictory_evidence["physical_health_proved"] is False,
            contradictory_evidence["physical_failure_proved"] is False,
        )),
    }


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, sp.MatrixBase):
        return [[_json_safe(item) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(sp.simplify(value))
    return value


def run() -> dict[str, Any]:
    upstream, upstream_diagnostics = upstream_integrity_controls()
    evidence, diagnostics = exact_controls()
    definition, _ = definition_controls()
    decision = warning_decision(
        evidence,
        upstream,
        constraint_reduction_complete=False,
        reduced_classification_complete=False,
        reduced_physical_health_evidence=False,
        reduced_physical_failure_evidence=False,
    )
    mutations = mutation_controls(evidence, upstream, decision)
    valid = bool(
        _strict_bool_map(evidence, EVIDENCE_KEYS)
        and all(evidence.values())
        and _strict_bool_map(upstream, UPSTREAM_KEYS)
        and all(upstream.values())
        and all(definition.values())
        and all(mutations.values())
        and _strict_bool_map(decision, DECISION_KEYS)
        and decision == {
            "direct_block_warning": True,
            "constraint_or_gauge_removal_open": True,
            "promotion_not_authorized": True,
            "physical_verdict_open": True,
            "physical_health_proved": False,
            "physical_failure_proved": False,
            "upstream_integrity_satisfied": True,
        }
    )
    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": valid,
        "status": (
            "PASS_EXACT_EXTERIOR_DIRECT_BLOCK_DIAGNOSTICS__NECESSARY_WARNING__"
            "PROMOTION_NOT_AUTHORIZED__PHYSICAL_VERDICT_OPEN"
            if valid else "INVALID_AUDIT_NO_ADJUDICATION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "outcomes": frozen_outcomes(),
        "closure_flags": frozen_closure_flags(),
        "decision": decision,
        "evidence": evidence,
        "upstream_controls": upstream,
        "upstream_diagnostics": upstream_diagnostics,
        "controls": {"definition": definition, "mutation": mutations},
        "diagnostics": _json_safe(diagnostics),
        "hashes": {
            "scientific_contract": _sha(CLAIM_CONTRACT),
            "outcomes": _sha(EXPECTED_OUTCOMES),
        },
    }


def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_ID,
            "model_version": MODEL_VERSION,
            "valid": False,
            "status": "INVALID_AUDIT_NO_ADJUDICATION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(_json_safe(report), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
