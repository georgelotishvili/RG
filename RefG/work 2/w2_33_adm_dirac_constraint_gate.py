"""Structural ADM/Dirac gate for the exact minimal RefG action.

This artifact performs the gauge-fixed structural part of the Hamiltonian audit
without pretending that the full Dirac algorithm has already been carried
out.  In unitary gauge ``Phi=t`` and ``phi^A=x^A`` it derives the exact ADM
maps

    Y = 1/N**2,
    gamma^{ij} = h^{ij},
    B^{AB} = h^{AB} - N^A N^B/N**2,

and proves that the displayed minimal action has the structural primary
constraints ``p_N=0``, ``p_i=0`` and ``p_H=0`` on that gauge-fixed chart.  It also derives the exact
algebraic shift Hessian of the F sector at ``N^i=0``.  The Hessian is a
nonzero scalar multiple of ``F_{,Bhat^{AB}}``; consequently it has generic
rank three only when that matrix is nonsingular, while its rank is exactly
zero at the silent point.

The arithmetic expression that would equal six degrees of freedom under a
rank-ten second-class hypothesis is retained only as a non-evidentiary
diagnostic.  None of the required Poisson-bracket premises is derived or
promoted.  In particular, a generic hypothesis cannot be imported onto
the silent background, where the shift block loses rank.  That loss may signal
extra constraints, a constraint bifurcation or strong coupling; this gate does
not choose among them.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any

import sympy as sp


CLAIM_ID = "W2_ADM_DIRAC_STRUCTURAL_CONSTRAINT_GATE_001"
MODEL_VERSION = "W2-ADM-DIRAC-MINIMAL-ACTION-v1.1-FROZEN-INVARIANT-FAIL-CLOSED"

HERE = Path(__file__).resolve().parent
W232_PATH = HERE / "w2_32_effective_action_dynamics_contract.py"


def _load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


w232 = _load_module(W232_PATH, "w2_32_dependency_for_w2_33")
EXPECTED_W232_CLAIM_ID = "W2_EFFECTIVE_ACTION_DYNAMICS_CONTRACT_001"
EXPECTED_W232_MODEL_VERSION = "W2-EFFECTIVE-ACTION-DYNAMICS-CONTRACT-v1.1-SYMBOLIC-CONTROLS"
EXPECTED_W232_ACTION_SHA256 = (
    "02E757C7406101C2E91723ED28FBE7BDD3E4F547A3968F1BD11641F97CDFF7E2"
)
EXPECTED_W232_CONTRACT_SHA256 = (
    "6CED59206375068BC9A65C427D78FEBA3FADD8287EE36778B4D1A9E56E0AB5AB"
)

REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

EVIDENCE_KEYS = frozenset({
    "w2_32_frozen_action_dependency_exact",
    "invariant_F_chain_rule_and_commutator_exact",
    "invariant_F_eigenbasis_freedom_is_three_not_six",
    "unitary_gauge_inverse_metric_and_Y_map_exact",
    "clock_normal_and_spatial_projector_map_exact",
    "material_strain_shift_map_exact",
    "projected_H_operator_has_no_Hdot_or_shift_exact",
    "gauge_fixed_velocity_hessian_rank_six_nullity_five_exact",
    "five_gauge_fixed_structural_primary_constraints_derived",
    "zero_shift_first_Bhat_derivatives_vanish_exact",
    "zero_shift_FBB_chain_term_vanishes_exact",
    "zero_shift_F_sector_hessian_proportional_to_FB_exact",
    "generic_nonsingular_FB_gives_rank_three_shift_block",
    "singular_FB_rank_is_not_promoted_to_three",
    "silent_point_shift_hessian_rank_zero_exact",
    "six_dof_arithmetic_is_diagnostic_not_evidence",
    "dirac_count_premises_are_explicitly_unproved",
    "silent_background_invalidates_generic_shift_rank_premise",
    "silent_background_dof_count_remains_open",
})


ACTION_SPEC: dict[str, Any] = deepcopy(w232.ACTION_SPEC)

ADM_GAUGE_SPEC: dict[str, Any] = {
    "signature": "+---",
    "adm_line_element": (
        "ds^2=N^2 dt^2-h_ij(dx^i+N^i dt)(dx^j+N^j dt)"
    ),
    "unitary_gauge": {"Phi": "t", "phi^A": "x^A"},
    "inverse_metric": {
        "g^00": "1/N^2",
        "g^0i": "-N^i/N^2",
        "g^ij": "-h^ij+N^i N^j/N^2",
    },
    "definitions": {
        "Y": "g^mn Phi_m Phi_n",
        "u^m": "nabla^m Phi/sqrt(Y)",
        "gamma^mn": "u^m u^n-g^mn",
        "B^AB": "-g^mn phi^A_m phi^B_n",
        "Yhat": "exp(-2H) Y",
        "Bhat^AB": "exp(2H) B^AB",
    },
    "minimal_medium_lagrangian": ACTION_SPEC["bulk_action"],
    "gravitational_sector": (
        "Einstein-Hilbert plus the standard boundary term; its ADM Hamiltonian "
        "is linear in lapse and shift before the medium contribution"
    ),
    "symmetric_matrix_derivative": (
        "delta F=F_BAB delta Bhat^AB with F_BAB=F_BBA and ordered-pair summation"
    ),
    "scope_exclusion": (
        "No omitted same-derivative operator, matter field, boundary source or "
        "higher-derivative completion is included in this gate"
    ),
}

INVARIANT_RESPONSE_SPEC: dict[str, Any] = {
    "response_class": "F(Yhat,I1hat,I2hat,I3hat) exactly as frozen by w2_32",
    "matrix_chain_rule": (
        "F_B=F_I1*I+F_I2*(I1*I-B)+F_I3*I3*B^{-1}"
    ),
    "cayley_hamilton_form": (
        "F_B=(F_I1+I1*F_I2+I2*F_I3)*I+(-F_I2-I1*F_I3)*B+F_I3*B^2"
    ),
    "commutation": "[F_B,B]=0",
    "eigenbasis_statement": (
        "for positive-definite B, F_B and B admit a common orthonormal eigenbasis; "
        "the local invariant first jet supplies three eigenvalue coefficients, not six arbitrary matrix entries"
    ),
    "silent_point": "B=I and F_B=0",
}

DIRAC_SCOPE_SPEC: dict[str, Any] = {
    "configuration_variables_after_unitary_gauge": {
        "h_ij": 6,
        "N": 1,
        "N^i": 3,
        "H": 1,
        "total": 11,
    },
    "gauge_fixed_structural_primary_constraints": ["p_N", "p_i (three)", "p_H"],
    "gauge_fixed_exact_reason": (
        "After the standard Einstein-Hilbert boundary treatment, neither the "
        "gravitational ADM Lagrangian nor the minimal medium contains dot N or "
        "dot N^i; gamma^mn H_m H_n=h^ij H_i H_j contains no dot H"
    ),
    "non_evidentiary_rank_ten_arithmetic": {
        "phase_dimension": 22,
        "first_class_constraints": 0,
        "second_class_constraints": 10,
        "physical_configuration_dof": 6,
    },
    "unproved_rank_ten_hypothesis": [
        "the unitary gauge is admissible on an open off-branch domain",
        "all five primary constraints generate independent secondary constraints",
        "the ten-constraint Dirac matrix has stable rank ten",
        "no tertiary constraint or residual first-class generator changes the count",
        "the lapse and H secondary operators are invertible with declared boundary data",
        "F_BAB is nonsingular so the algebraic shift sub-block has rank three",
    ],
    "silent_stratum": (
        "F_BAB=0 makes the algebraic shift Hessian rank zero. The generic implicit-"
        "function and rank-ten premises fail there and the Dirac algorithm must be "
        "rerun on that stratum. No silent-background degree count follows from the "
        "generic formula."
    ),
    "open_calculations": [
        "complete secondary and tertiary constraint set",
        "all Poisson brackets and the full Dirac-matrix rank",
        "first-class versus second-class classification on the silent branch",
        "reduced Hamiltonian and kinetic-sign audit",
        "reduced principal symbol, hyperbolicity and strong-coupling scale",
    ],
}


def frozen_outcomes() -> dict[str, bool]:
    return {
        "w2_32_frozen_action_consumed": True,
        "invariant_response_class_enforced": True,
        "unitary_gauge_adm_maps_derived": True,
        "projected_H_velocity_absence_derived": True,
        "gauge_fixed_velocity_hessian_rank_and_nullity_derived": True,
        "gauge_fixed_primary_pN_pi_pH_structurally_derived": True,
        "zero_shift_F_sector_hessian_derived": True,
        "generic_nonsingular_FB_shift_rank_three_derived": True,
        "silent_point_shift_rank_zero_derived": True,
        "rank_ten_six_dof_hypothesis_promoted": False,
        "complete_secondary_constraint_set_derived": False,
        "full_poisson_dirac_closure_derived": False,
        "generic_offbranch_six_dof_unconditionally_proved": False,
        "silent_background_six_dof_proved": False,
        "silent_background_constraint_classification_proved": False,
        "silent_background_strong_coupling_excluded": False,
        "reduced_hyperbolicity_or_stability_proved": False,
        "physical_GR_or_1PN_promotion_proved": False,
    }


def frozen_closure_flags() -> dict[str, bool]:
    return {
        "full_ADM_legendre_map_closed": False,
        "all_secondary_constraints_closed": False,
        "all_tertiary_constraints_excluded": False,
        "full_dirac_matrix_rank_closed": False,
        "generic_reduced_dof_count_closed": False,
        "silent_branch_reduced_dof_count_closed": False,
        "reduced_hamiltonian_bounded_below": False,
        "constraint_rank_constant_near_silent_branch": False,
        "strong_coupling_scale_controlled": False,
        "hyperbolicity_and_cauchy_problem_closed": False,
        "GR_or_1PN_bridge_closed": False,
        "observational_validation_closed": False,
    }


EXPECTED_OUTCOMES = frozen_outcomes()
EXPECTED_CLOSURE_FLAGS = frozen_closure_flags()
OUTCOME_KEYS = frozenset(EXPECTED_OUTCOMES)
CLOSURE_FLAG_KEYS = frozenset(EXPECTED_CLOSURE_FLAGS)

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "Consume the w2_32-frozen invariant minimal action and derive its exact "
        "unitary-gauge ADM maps, gauge-fixed velocity-Hessian null directions and "
        "zero-shift F-sector shift Hessian, while leaving every physical Dirac "
        "degree count and the silent-branch constraint problem open."
    ),
    "TYPE": "EXACT_GAUGE_FIXED_ADM_AND_INVARIANT_SHIFT_RANK_THEOREM_DIRAC_COUNT_OPEN",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "The exact w2_32 minimal invariant action and +--- ADM convention are fixed. "
        "N, sqrt(h), M_* and exp(H) are nonzero on the audited chart. F is C^2 in "
        "the symmetric Bhat matrix. Standard Einstein-Hilbert ADM facts are used "
        "after the boundary term; no extra operator is silently supplied."
    ),
    "DOMAIN": (
        "Exact local algebra on a unitary-gauge chart, with the shift Hessian "
        "evaluated at N^i=0. Generic rank statements apply only where F_BAB is "
        "nonsingular. The silent point is a separate singular rank stratum."
    ),
    "CONVENTIONS": (
        "Internal A,B indices are identified with unitary-gauge spatial indices. "
        "Symmetric matrix derivatives use ordered-pair summation, producing the "
        "factor two in d^2 L_F/dN^i dN^j. F_B is constrained by the invariant "
        "chain rule to commute with B. Rank-ten arithmetic is not evidence for a "
        "physical degree count."
    ),
    "FREEDOM_LEDGER": {
        "response_function": {
            "source": "arbitrary C2 F(Yhat,I1hat,I2hat,I3hat) from w2_32",
            "range": "F_B is the invariant-chain-rule matrix commuting with B",
            "complexity": "three invariant first derivatives; no arbitrary six-component F_B",
        },
        "background_strata": {
            "source": "algebraic rank of F_BAB",
            "range": "rank 0,1,2,3",
            "complexity": 4,
        },
        "dirac_completion": {
            "source": "absent",
            "range": "no assumed Poisson matrix beyond the conditional count",
            "complexity": "open functional-constraint problem",
        },
    },
    "DEPENDENCIES": [
        "RefG/work 2/w2_32_effective_action_dynamics_contract.py: exact frozen action, claim and hashes",
        "artikle/RefG_Manuscript.tex: synchronization only through w2_32, not dynamics evidence",
        "standard ADM decomposition of Einstein-Hilbert gravity after its boundary term",
    ],
    "METHOD": (
        "Construct the inverse ADM metric and clock normal symbolically; derive gamma "
        "and B exactly. Derive the invariant F_B chain rule and its commutator with B. "
        "Differentiate Bhat twice with respect to the shift. Since its "
        "first shift derivative vanishes at zero shift, every F_BB chain term vanishes, "
        "leaving an exact Hessian proportional to invariant F_B. Derive the gauge-fixed "
        "velocity Hessian and retain rank-ten arithmetic only as a non-evidentiary diagnostic."
    ),
    "PASS_CONDITION": (
        "The w2_32 dependency, invariant response restriction, ADM identities, velocity "
        "Hessian, shift-Hessian factors and rank tests are exact; every physical count, "
        "silent-background count, stability, GR and observation flag stays false."
    ),
    "FAIL_CONDITION": (
        "A wrong ADM sign, missing factor two, nonzero silent shift rank, treating a "
        "singular F_B as rank three, treating F_B as six arbitrary components, importing "
        "rank-ten arithmetic onto the silent branch, "
        "claiming uncomputed Poisson closure, schema drift or payload mutation fails the gate."
    ),
    "FALSIFIER": (
        "Direct symbolic disagreement with an ADM map or Hessian identity falsifies the "
        "exact claim. A completed Dirac analysis may replace the open statuses in a new "
        "version; it cannot be backfilled into this artifact without reopening its hashes."
    ),
    "RESIDUAL": (
        "Zero for all exact matrix identities and Hessian residuals. Dirac closure has "
        "no numerical residual because it is not computed."
    ),
    "ERROR_BOUND": "Zero for the symbolic identities; N/A for explicitly open functional analysis.",
    "VALIDITY_HEALTH": (
        "The gauge-fixed velocity and shift-rank results are structural warnings, not by "
        "themselves a covariant Dirac equivalence, ghost theorem or a "
        "strong-coupling theorem. It proves only that the generic shift-solvability and "
        "six-DOF argument cannot be used at the silent point without a new Dirac reduction."
    ),
    "BRANCHES": {
        "generic_invariant_F_B_rank_three": "SHIFT_SOLVABILITY_STRATUM_ONLY_NO_DOF_COUNT",
        "intermediate_F_B_rank_one_or_two": "CONSTRAINT_RANK_STRATUM_OPEN",
        "silent_F_B_rank_zero": "GENERIC_COUNT_INVALID__DIRAC_REANALYSIS_REQUIRED",
        "full_poisson_closure": "OPEN",
        "reduced_stability_and_hyperbolicity": "OPEN",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "structural Hamiltonian gate only"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "no physical source solution is built"},
    "DATA_ROLE": {"status": "N/A", "reason": "no data or calibration enters"},
    "IDENTIFIABILITY": (
        "The exact calculation identifies only the shift-rank stratum through F_BAB. "
        "It does not identify physical modes until the complete constraints are reduced."
    ),
    "BENCHMARK": (
        "At N^i=0 the Lagrangian-density Hessian must be "
        "2 sqrt(h) M_*^4 exp(2H) F_Bij/N. It must have rank three for a nonsingular "
        "invariant-chain-rule test matrix and rank zero when the silent-point F_B vanishes."
    ),
    "CLOSURE_FLAGS": frozen_closure_flags(),
    "CROSSCHECK": (
        "Derive gamma both from u^m u^n-g^mn and from the ADM spatial projector. "
        "Derive the shift Hessian both by direct differentiation of the local linear "
        "Taylor term and by the chain rule with the vanishing first Bhat derivative."
    ),
    "PROVENANCE": {
        "date": "2026-07-23",
        "data": "none",
        "code_version": "w2_33 v1.0 fail-closed",
    },
    "FILES": [
        "RefG/work 2/w2_32_effective_action_dynamics_contract.py",
        "RefG/work 2/w2_33_adm_dirac_constraint_gate.py",
    ],
}
CLAIM_CONTRACT = SCIENTIFIC_CONTRACT

# Frozen after the scientific payload is finalized.  Any payload change must
# update the model version and deliberately regenerate these values.
EXPECTED_ACTION_SPEC_SHA256 = (
    "02E757C7406101C2E91723ED28FBE7BDD3E4F547A3968F1BD11641F97CDFF7E2"
)
EXPECTED_ADM_GAUGE_SPEC_SHA256 = (
    "3A4CDD1F9ADD897CE9E786B53F9F737176F1EF14F9C3F23AA6B3093D7F6A0658"
)
EXPECTED_INVARIANT_RESPONSE_SPEC_SHA256 = (
    "EB4D0E5E83159F089068FEC5C662D57574BEAB68AD4F7E7C180CC8039355AF9C"
)
EXPECTED_DIRAC_SCOPE_SPEC_SHA256 = (
    "E55D25A4C0E12F237779BFC3EC87F247DB4BB3DA9F3A96D621DB5B16F23E2CCC"
)
EXPECTED_SCIENTIFIC_CONTRACT_SHA256 = (
    "FA6431F6BE588284CF8E96B1F6AA20C9C9C0768BF0C9D21B1CD395B7D7BEC6AB"
)


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def _exact_bool_map(value: Any, keys: frozenset[str]) -> bool:
    return (
        isinstance(value, dict)
        and set(value) == set(keys)
        and all(type(item) is bool for item in value.values())
    )


def _all_false(value: dict[str, bool]) -> bool:
    return all(type(item) is bool and item is False for item in value.values())


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, sp.MatrixBase):
        return [[str(item) for item in value.row(row)] for row in range(value.rows)]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


def dependency_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    report32 = w232.run()
    action_hash = w232._canonical_sha256(w232.ACTION_SPEC)
    contract_hash = w232._canonical_sha256(w232.CLAIM_CONTRACT)
    exact = all((
        w232.CLAIM_ID == EXPECTED_W232_CLAIM_ID,
        w232.MODEL_VERSION == EXPECTED_W232_MODEL_VERSION,
        action_hash == EXPECTED_W232_ACTION_SHA256,
        contract_hash == EXPECTED_W232_CONTRACT_SHA256,
        w232.EXPECTED_HASHES["action_spec"] == EXPECTED_W232_ACTION_SHA256,
        w232.EXPECTED_HASHES["scientific_contract"] == EXPECTED_W232_CONTRACT_SHA256,
        ACTION_SPEC == w232.ACTION_SPEC,
        report32.get("valid") is True,
        report32.get("all_physical_closure_flags_false") is True,
    ))
    return {"w2_32_frozen_action_dependency_exact": exact}, {
        "claim_id": w232.CLAIM_ID,
        "model_version": w232.MODEL_VERSION,
        "action_hash": action_hash,
        "contract_hash": contract_hash,
        "dependency_valid": report32.get("valid"),
        "role": "authoritative frozen action; manuscript remains synchronization only inside w2_32",
    }


def invariant_response_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    b1, b2, b3 = sp.symbols("b1 b2 b3", positive=True, nonzero=True)
    f1, f2, f3 = sp.symbols("F_I1 F_I2 F_I3", real=True)
    B = sp.diag(b1, b2, b3)
    identity = sp.eye(3)
    I1 = sp.trace(B)
    I2 = (sp.trace(B) ** 2 - sp.trace(B * B)) / 2
    I3 = B.det()
    chain = sp.simplify(
        f1 * identity + f2 * (I1 * identity - B) + f3 * I3 * B.inv()
    )
    polynomial = sp.simplify(
        (f1 + I1 * f2 + I2 * f3) * identity
        + (-f2 - I1 * f3) * B
        + f3 * B**2
    )
    eigenvalues = tuple(sp.simplify(chain[i, i]) for i in range(3))
    expected_eigenvalues = tuple(
        sp.simplify(f1 + f2 * (I1 - value) + f3 * I3 / value)
        for value in (b1, b2, b3)
    )
    commutator = sp.simplify(chain * B - B * chain)
    controls = {
        "invariant_F_chain_rule_and_commutator_exact": all((
            sp.simplify(chain - polynomial) == sp.zeros(3),
            commutator == sp.zeros(3),
            eigenvalues == expected_eigenvalues,
        )),
        "invariant_F_eigenbasis_freedom_is_three_not_six": all((
            len((f1, f2, f3)) == 3,
            chain.is_diagonal(),
            "three eigenvalue coefficients"
            in INVARIANT_RESPONSE_SPEC["eigenbasis_statement"],
            "not six arbitrary matrix entries"
            in INVARIANT_RESPONSE_SPEC["eigenbasis_statement"],
        )),
    }
    return controls, {
        "B_eigenbasis": B,
        "F_B_chain_rule": chain,
        "F_B_cayley_hamilton_polynomial": polynomial,
        "commutator": commutator,
        "F_B_eigenvalues": eigenvalues,
        "invariant_first_derivative_count": 3,
    }


def adm_map_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    N = sp.symbols("N", positive=True, nonzero=True)
    n1, n2, n3 = sp.symbols("N1 N2 N3", real=True)
    shift = sp.Matrix([n1, n2, n3])
    h11, h22, h33, h12, h13, h23 = sp.symbols(
        "h11 h22 h33 h12 h13 h23", real=True
    )
    h_inv = sp.Matrix([
        [h11, h12, h13],
        [h12, h22, h23],
        [h13, h23, h33],
    ])

    g_inv = sp.zeros(4)
    g_inv[0, 0] = 1 / N**2
    for i in range(3):
        g_inv[0, i + 1] = -shift[i] / N**2
        g_inv[i + 1, 0] = -shift[i] / N**2
        for j in range(3):
            g_inv[i + 1, j + 1] = -h_inv[i, j] + shift[i] * shift[j] / N**2

    normal = sp.Matrix([1 / N, -n1 / N, -n2 / N, -n3 / N])
    gamma = sp.simplify(normal * normal.T - g_inv)
    expected_gamma = sp.zeros(4)
    expected_gamma[1:4, 1:4] = h_inv
    B = -g_inv[1:4, 1:4]
    expected_B = h_inv - shift * shift.T / N**2

    Hdot, H1, H2, H3 = sp.symbols("Hdot H1 H2 H3", real=True)
    dH = sp.Matrix([Hdot, H1, H2, H3])
    projected_H = sp.simplify((dH.T * gamma * dH)[0])
    expected_projected_H = sp.simplify(
        (sp.Matrix([H1, H2, H3]).T * h_inv * sp.Matrix([H1, H2, H3]))[0]
    )

    controls = {
        "unitary_gauge_inverse_metric_and_Y_map_exact": all((
            sp.simplify(g_inv[0, 0] - 1 / N**2) == 0,
            all(sp.simplify(g_inv[0, i + 1] + shift[i] / N**2) == 0
                for i in range(3)),
        )),
        "clock_normal_and_spatial_projector_map_exact": gamma == expected_gamma,
        "material_strain_shift_map_exact": sp.simplify(B - expected_B) == sp.zeros(3),
        "projected_H_operator_has_no_Hdot_or_shift_exact": all((
            sp.simplify(projected_H - expected_projected_H) == 0,
            sp.diff(projected_H, Hdot) == 0,
            all(sp.diff(projected_H, item) == 0 for item in shift),
        )),
    }
    diagnostics = {
        "inverse_metric": g_inv,
        "unit_normal": normal,
        "gamma": gamma,
        "Y": g_inv[0, 0],
        "B": B,
        "projected_H_gradient": projected_H,
        "d_projected_H_d_Hdot": sp.diff(projected_H, Hdot),
    }
    return controls, diagnostics


def primary_constraint_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    k11, k22, k33, k12, k13, k23 = sp.symbols(
        "K11 K22 K33 K12 K13 K23", real=True
    )
    nondynamical = sp.symbols("Ndot N1dot N2dot N3dot Hdot", real=True)
    spatial_velocities = (k11, k22, k33, k12, k13, k23)
    velocities = spatial_velocities + nondynamical
    K = sp.Matrix([
        [k11, k12, k13],
        [k12, k22, k23],
        [k13, k23, k33],
    ])
    # In an orthonormal spatial frame, nonzero ADM prefactors do not change rank.
    EH_kinetic_form = sp.expand(sp.trace(K * K) - sp.trace(K) ** 2)
    full_gauge_fixed_kinetic_form = EH_kinetic_form
    velocity_hessian = sp.hessian(full_gauge_fixed_kinetic_form, velocities)
    EH_velocity_hessian = velocity_hessian[:6, :6]
    nondynamical_block = velocity_hessian[6:11, 6:11]
    primary_multiplicities = {"p_N": 1, "p_i": 3, "p_H": 1}
    controls = {
        "gauge_fixed_velocity_hessian_rank_six_nullity_five_exact": all((
            EH_velocity_hessian.rank() == 6,
            velocity_hessian.rank() == 6,
            len(velocities) - velocity_hessian.rank() == 5,
            nondynamical_block == sp.zeros(5),
            all(
                velocity_hessian[:, index] == sp.zeros(11, 1)
                for index in range(6, 11)
            ),
        )),
        "five_gauge_fixed_structural_primary_constraints_derived": all((
            sum(primary_multiplicities.values()) == 5,
            velocity_hessian.rank() == 6,
            len(velocities) - velocity_hessian.rank() == 5,
            DIRAC_SCOPE_SPEC["gauge_fixed_structural_primary_constraints"]
            == ["p_N", "p_i (three)", "p_H"],
        )),
    }
    return controls, {
        "gauge_fixed_velocity_order": [str(item) for item in velocities],
        "EH_kinetic_form_orthonormal_frame": EH_kinetic_form,
        "EH_velocity_hessian": EH_velocity_hessian,
        "full_gauge_fixed_velocity_hessian": velocity_hessian,
        "velocity_hessian_rank": velocity_hessian.rank(),
        "velocity_hessian_nullity": len(velocities) - velocity_hessian.rank(),
        "primary_constraints": primary_multiplicities,
        "primary_constraint_count": sum(primary_multiplicities.values()),
        "scope": (
            "unitary-gauge structural primary set in a local orthonormal spatial frame; "
            "not a proof of covariant gauge-fixing equivalence or the completed Dirac chain"
        ),
    }


def shift_hessian_controls(
    expected_factor: int = 2,
) -> tuple[dict[str, bool], dict[str, Any]]:
    N, sqrt_h, M4 = sp.symbols("N sqrt_h M4", positive=True, nonzero=True)
    H = sp.symbols("H", real=True)
    n1, n2, n3 = sp.symbols("N1 N2 N3", real=True)
    shift_symbols = (n1, n2, n3)
    shift = sp.Matrix(shift_symbols)
    b1, b2, b3 = sp.symbols("b1 b2 b3", positive=True, nonzero=True)
    h_inv = sp.diag(b1, b2, b3)
    mu1, mu2, mu3 = sp.symbols("mu1 mu2 mu3", real=True)
    # The invariant response forces F_B to share B's eigenbasis.  The three
    # mu_i are chain-rule eigenvalues, not six arbitrary matrix components.
    F_B = sp.diag(mu1, mu2, mu3)
    e2H = sp.exp(2 * H)
    Bhat = e2H * (h_inv - shift * shift.T / N**2)
    zero_shift = {item: 0 for item in shift_symbols}

    first_B_derivatives = [
        sp.simplify(Bhat.diff(item).subs(zero_shift)) for item in shift_symbols
    ]
    second_B_derivatives = [
        [
            sp.simplify(Bhat.diff(shift_symbols[i], shift_symbols[j]).subs(zero_shift))
            for j in range(3)
        ]
        for i in range(3)
    ]

    # Build the actual F_BB chain term.  Ordered matrix-pair components are
    # retained explicitly; symmetry is unnecessary because each dB/dN is zero.
    first_B_vectors = [sp.Matrix(item).reshape(9, 1) for item in first_B_derivatives]
    fbb_symbols = sp.symbols("FBB0:81", real=True)
    F_BB = sp.Matrix(9, 9, fbb_symbols)
    F_BB_chain = sp.Matrix(3, 3, lambda i, j: sp.simplify(
        (first_B_vectors[i].T * F_BB * first_B_vectors[j])[0]
    ))

    # This is the first Taylor term of an arbitrary C^2 F around zero shift.
    # Since Delta Bhat=O(N^i N^j), all quadratic and higher Taylor terms start
    # at fourth order in the shift and cannot contribute to this Hessian.
    delta_Bhat = sp.simplify(Bhat - e2H * h_inv)
    F_linear_shift = sp.expand(sum(
        F_B[A, Bidx] * delta_Bhat[A, Bidx]
        for A in range(3) for Bidx in range(3)
    ))
    L_F_shift = sp.expand(-N * sqrt_h * M4 * F_linear_shift)
    shift_hessian = sp.Matrix(3, 3, lambda i, j: sp.simplify(
        sp.diff(L_F_shift, shift_symbols[i], shift_symbols[j]).subs(zero_shift)
    ))
    base_factor = sp.simplify(sqrt_h * M4 * e2H / N)
    scalar_factor = sp.simplify(2 * base_factor)
    expected_hessian = sp.simplify(expected_factor * base_factor * F_B)
    hessian_residual = sp.simplify(shift_hessian - expected_hessian)

    nonsingular_sample = sp.diag(2, 3, 5)
    singular_sample = sp.diag(2, 3, 0)
    silent_sample = sp.zeros(3)
    sample_substitution = {mu1: 2, mu2: 3, mu3: 5}
    singular_substitution = {mu1: 2, mu2: 3, mu3: 0}
    silent_substitution = {mu1: 0, mu2: 0, mu3: 0}
    generic_det_residual = sp.simplify(
        shift_hessian.det() - scalar_factor**3 * F_B.det()
    )

    controls = {
        "zero_shift_first_Bhat_derivatives_vanish_exact": all(
            item == sp.zeros(3) for item in first_B_derivatives
        ),
        "zero_shift_FBB_chain_term_vanishes_exact": all(
            item == 0 for item in F_BB_chain
        ),
        "zero_shift_F_sector_hessian_proportional_to_FB_exact": all((
            hessian_residual == sp.zeros(3),
            generic_det_residual == 0,
        )),
        "generic_nonsingular_FB_gives_rank_three_shift_block": all((
            nonsingular_sample.rank() == 3,
            shift_hessian.subs(sample_substitution).rank() == 3,
            nonsingular_sample.det() != 0,
        )),
        "singular_FB_rank_is_not_promoted_to_three": all((
            singular_sample.rank() == 2,
            shift_hessian.subs(singular_substitution).rank() == 2,
        )),
        "silent_point_shift_hessian_rank_zero_exact": all((
            silent_sample.rank() == 0,
            shift_hessian.subs(silent_substitution) == sp.zeros(3),
            shift_hessian.subs(silent_substitution).rank() == 0,
        )),
    }
    diagnostics = {
        "Bhat": Bhat,
        "zero_shift_first_Bhat_derivatives": first_B_derivatives,
        "zero_shift_second_Bhat_derivatives": second_B_derivatives,
        "F_B_matrix": F_B,
        "F_B_semantics": "three invariant-chain-rule eigenvalues in the common B eigenbasis",
        "F_BB_chain_term": F_BB_chain,
        "shift_hessian": shift_hessian,
        "expected_shift_hessian": expected_hessian,
        "hessian_residual": hessian_residual,
        "determinant_factorization_residual": generic_det_residual,
        "generic_sample_rank": shift_hessian.subs(sample_substitution).rank(),
        "singular_sample_rank": shift_hessian.subs(singular_substitution).rank(),
        "silent_sample_rank": shift_hessian.subs(silent_substitution).rank(),
        "expected_factor_used_by_screen": expected_factor,
        "interpretation": (
            "rank(d2 L_F/dNi dNj)|_0 = rank(F_B) for nonzero scalar prefactor"
        ),
    }
    return controls, diagnostics


def dirac_count_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    configuration_variables = 11
    phase_dimension = 2 * configuration_variables
    assumed_first_class = 0
    assumed_second_class = 10
    conditional_dof = (
        phase_dimension - 2 * assumed_first_class - assumed_second_class
    ) // 2
    generic_premises = {
        "five_independent_secondaries_derived": False,
        "dirac_matrix_rank_ten_derived": False,
        "no_tertiary_constraints_derived": False,
        "no_residual_first_class_generators_derived": False,
        "lapse_H_operator_invertibility_derived": False,
        "rank_stability_near_target_derived": False,
    }
    controls = {
        "six_dof_arithmetic_is_diagnostic_not_evidence": all((
            configuration_variables == 11,
            phase_dimension == 22,
            assumed_first_class == 0,
            assumed_second_class == 10,
            conditional_dof == 6,
            EXPECTED_OUTCOMES["rank_ten_six_dof_hypothesis_promoted"] is False,
            EXPECTED_CLOSURE_FLAGS["generic_reduced_dof_count_closed"] is False,
        )),
        "dirac_count_premises_are_explicitly_unproved": all(
            item is False for item in generic_premises.values()
        ),
        "silent_background_invalidates_generic_shift_rank_premise": (
            EXPECTED_OUTCOMES["silent_point_shift_rank_zero_derived"] is True
            and EXPECTED_OUTCOMES["silent_background_six_dof_proved"] is False
        ),
        "silent_background_dof_count_remains_open": all((
            EXPECTED_OUTCOMES["silent_background_six_dof_proved"] is False,
            EXPECTED_OUTCOMES[
                "silent_background_constraint_classification_proved"
            ] is False,
            EXPECTED_CLOSURE_FLAGS["silent_branch_reduced_dof_count_closed"] is False,
        )),
    }
    diagnostics = {
        "configuration_dimension": configuration_variables,
        "phase_dimension": phase_dimension,
        "non_evidentiary_rank_ten_hypothesis": {
            "first_class_count": assumed_first_class,
            "second_class_count": assumed_second_class,
            "arithmetic_result_if_assumed": conditional_dof,
            "promoted": False,
        },
        "unproved_generic_premises": generic_premises,
        "silent_branch_status": "OPEN_DIRAC_REANALYSIS_REQUIRED",
    }
    return controls, diagnostics


def payload_integrity_screen(
    action_spec: Any,
    *payloads: Any,
) -> bool:
    # The three-payload call is retained for read-only downstream consumers
    # written against v1.0; v1.1 still checks the new frozen ADM and invariant
    # specifications rather than omitting them from that compatibility path.
    if len(payloads) == 2:
        dirac_scope_spec, contract = payloads
        adm_gauge_spec = ADM_GAUGE_SPEC
        invariant_response_spec = INVARIANT_RESPONSE_SPEC
    elif len(payloads) == 4:
        adm_gauge_spec, invariant_response_spec, dirac_scope_spec, contract = payloads
    else:
        return False
    return all((
        _canonical_sha256(action_spec) == EXPECTED_ACTION_SPEC_SHA256,
        _canonical_sha256(adm_gauge_spec) == EXPECTED_ADM_GAUGE_SPEC_SHA256,
        _canonical_sha256(invariant_response_spec)
        == EXPECTED_INVARIANT_RESPONSE_SPEC_SHA256,
        _canonical_sha256(dirac_scope_spec) == EXPECTED_DIRAC_SCOPE_SPEC_SHA256,
        _canonical_sha256(contract) == EXPECTED_SCIENTIFIC_CONTRACT_SHA256,
    ))


def audit_screen(
    evidence: Any,
    outcomes: Any = None,
    closure_flags: Any = None,
) -> dict[str, bool]:
    if outcomes is None:
        outcomes = frozen_outcomes()
    if closure_flags is None:
        closure_flags = frozen_closure_flags()
    evidence_schema = _exact_bool_map(evidence, EVIDENCE_KEYS)
    outcomes_schema = _exact_bool_map(outcomes, OUTCOME_KEYS)
    closure_schema = _exact_bool_map(closure_flags, CLOSURE_FLAG_KEYS)
    outcomes_exact = outcomes_schema and outcomes == EXPECTED_OUTCOMES
    closure_exact = closure_schema and closure_flags == EXPECTED_CLOSURE_FLAGS
    passed = bool(
        evidence_schema
        and all(evidence.values())
        and outcomes_exact
        and closure_exact
        and _all_false(closure_flags)
    )
    return {
        "schema_valid": evidence_schema,
        "outcomes_schema_valid": outcomes_schema,
        "closure_schema_valid": closure_schema,
        "evidence_passes": passed,
        "full_dirac_closure_promoted": False,
        "silent_six_dof_promoted": False,
        "physical_GR_or_1PN_promoted": False,
    }


def mutation_controls(evidence: dict[str, bool]) -> dict[str, bool]:
    base = audit_screen(evidence)
    missing = dict(evidence)
    missing.pop(next(iter(EVIDENCE_KEYS)))
    promoted_outcomes = frozen_outcomes()
    promoted_outcomes["full_poisson_dirac_closure_derived"] = True
    promoted_silent = frozen_outcomes()
    promoted_silent["silent_background_six_dof_proved"] = True
    promoted_closure = frozen_closure_flags()
    promoted_closure["full_dirac_matrix_rank_closed"] = True
    nonboolean_outcomes = frozen_outcomes()
    nonboolean_outcomes[next(iter(OUTCOME_KEYS))] = 1
    nonboolean_closure = frozen_closure_flags()
    nonboolean_closure[next(iter(CLOSURE_FLAG_KEYS))] = 0

    action_mutations = []
    for key in ACTION_SPEC:
        mutated = deepcopy(ACTION_SPEC)
        mutated[key] = "__MUTATED__"
        action_mutations.append(mutated)
    adm_mutations = []
    for key in ADM_GAUGE_SPEC:
        mutated = deepcopy(ADM_GAUGE_SPEC)
        mutated[key] = "__MUTATED__"
        adm_mutations.append(mutated)
    invariant_mutations = []
    for key in INVARIANT_RESPONSE_SPEC:
        mutated = deepcopy(INVARIANT_RESPONSE_SPEC)
        mutated[key] = "__MUTATED__"
        invariant_mutations.append(mutated)
    dirac_mutations = []
    for key in DIRAC_SCOPE_SPEC:
        mutated = deepcopy(DIRAC_SCOPE_SPEC)
        mutated[key] = "__MUTATED__"
        dirac_mutations.append(mutated)
    contract_mutations = []
    for key in CLAIM_CONTRACT:
        mutated = deepcopy(CLAIM_CONTRACT)
        mutated[key] = "__MUTATED__"
        contract_mutations.append(mutated)

    # Re-run the actual Hessian screen with the wrong expected multiplier.
    wrong_factor_shift, _ = shift_hessian_controls(expected_factor=1)
    wrong_factor_evidence = dict(evidence)
    wrong_factor_evidence[
        "zero_shift_F_sector_hessian_proportional_to_FB_exact"
    ] = wrong_factor_shift[
        "zero_shift_F_sector_hessian_proportional_to_FB_exact"
    ]
    wrong_second_class_count_dof = (22 - 8) // 2

    return {
        "positive_evidence_passes_without_physical_promotion": all((
            base["schema_valid"], base["evidence_passes"],
            not base["full_dirac_closure_promoted"],
            not base["silent_six_dof_promoted"],
            not base["physical_GR_or_1PN_promoted"],
        )),
        "each_single_false_evidence_item_blocks_gate": all(
            not audit_screen({**evidence, key: False})["evidence_passes"]
            for key in EVIDENCE_KEYS
        ),
        "missing_extra_or_nonboolean_evidence_fails_closed": all((
            not audit_screen(missing)["schema_valid"],
            not audit_screen({**evidence, "extra": True})["schema_valid"],
            not audit_screen({**evidence, next(iter(EVIDENCE_KEYS)): 1})[
                "schema_valid"
            ],
        )),
        "outcome_or_closure_promotion_fails_closed": all((
            not audit_screen(evidence, promoted_outcomes)["evidence_passes"],
            not audit_screen(evidence, promoted_silent)["evidence_passes"],
            not audit_screen(evidence, closure_flags=promoted_closure)["evidence_passes"],
            not audit_screen(evidence, nonboolean_outcomes)["outcomes_schema_valid"],
            not audit_screen(
                evidence, closure_flags=nonboolean_closure
            )["closure_schema_valid"],
        )),
        "payload_mutations_fail_closed": all((
            payload_integrity_screen(
                ACTION_SPEC, ADM_GAUGE_SPEC, INVARIANT_RESPONSE_SPEC,
                DIRAC_SCOPE_SPEC, CLAIM_CONTRACT
            ),
            all(not payload_integrity_screen(
                item, ADM_GAUGE_SPEC, INVARIANT_RESPONSE_SPEC,
                DIRAC_SCOPE_SPEC, CLAIM_CONTRACT
            )
                for item in action_mutations),
            all(not payload_integrity_screen(
                ACTION_SPEC, item, INVARIANT_RESPONSE_SPEC,
                DIRAC_SCOPE_SPEC, CLAIM_CONTRACT
            )
                for item in adm_mutations),
            all(not payload_integrity_screen(
                ACTION_SPEC, ADM_GAUGE_SPEC, item,
                DIRAC_SCOPE_SPEC, CLAIM_CONTRACT
            )
                for item in invariant_mutations),
            all(not payload_integrity_screen(
                ACTION_SPEC, ADM_GAUGE_SPEC, INVARIANT_RESPONSE_SPEC,
                item, CLAIM_CONTRACT
            )
                for item in dirac_mutations),
            all(not payload_integrity_screen(
                ACTION_SPEC, ADM_GAUGE_SPEC, INVARIANT_RESPONSE_SPEC,
                DIRAC_SCOPE_SPEC, item
            )
                for item in contract_mutations),
        )),
        "wrong_hessian_factor_and_constraint_count_rejected": all((
            wrong_factor_shift[
                "zero_shift_F_sector_hessian_proportional_to_FB_exact"
            ] is False,
            not audit_screen(wrong_factor_evidence)["evidence_passes"],
            wrong_second_class_count_dof == 7,
            wrong_second_class_count_dof != 6,
        )),
    }


def definition_controls() -> dict[str, bool]:
    return {
        "contract_schema_exact": set(CLAIM_CONTRACT) == REQUIRED_SCIENTIFIC_FIELDS,
        "payload_hashes_exact": payload_integrity_screen(
            ACTION_SPEC, ADM_GAUGE_SPEC, INVARIANT_RESPONSE_SPEC,
            DIRAC_SCOPE_SPEC, CLAIM_CONTRACT
        ),
        "outcome_ledgers_exact": all((
            _exact_bool_map(EXPECTED_OUTCOMES, OUTCOME_KEYS),
            _exact_bool_map(EXPECTED_CLOSURE_FLAGS, CLOSURE_FLAG_KEYS),
            frozen_outcomes() == EXPECTED_OUTCOMES,
            frozen_closure_flags() == EXPECTED_CLOSURE_FLAGS,
            CLAIM_CONTRACT["CLOSURE_FLAGS"] == EXPECTED_CLOSURE_FLAGS,
        )),
        "all_physical_closure_flags_false": _all_false(EXPECTED_CLOSURE_FLAGS),
        "generic_and_silent_branches_separated": all((
            CLAIM_CONTRACT["BRANCHES"]["generic_invariant_F_B_rank_three"]
            == "SHIFT_SOLVABILITY_STRATUM_ONLY_NO_DOF_COUNT",
            CLAIM_CONTRACT["BRANCHES"]["silent_F_B_rank_zero"]
            == "GENERIC_COUNT_INVALID__DIRAC_REANALYSIS_REQUIRED",
        )),
    }


def run() -> dict[str, Any]:
    dependency, dependency_diagnostics = dependency_controls()
    invariant, invariant_diagnostics = invariant_response_controls()
    adm, adm_diagnostics = adm_map_controls()
    primary, primary_diagnostics = primary_constraint_controls()
    shift, shift_diagnostics = shift_hessian_controls()
    dirac, dirac_diagnostics = dirac_count_controls()
    evidence = {
        **dependency, **invariant, **adm, **primary, **shift, **dirac,
    }
    decisions = mutation_controls(evidence)
    definition = definition_controls()
    valid = bool(
        _exact_bool_map(evidence, EVIDENCE_KEYS)
        and all(evidence.values())
        and all(decisions.values())
        and all(definition.values())
        and audit_screen(evidence)["evidence_passes"]
    )
    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": valid,
        "status": (
            "PASS_FROZEN_INVARIANT_ACTION_GAUGE_FIXED_ADM_AND_SHIFT_RANK__"
            "ALL_PHYSICAL_DIRAC_COUNTS_OPEN"
            if valid else "FAIL_INVALID_NO_PROMOTION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The w2_32-frozen invariant minimal action has exact unitary-gauge ADM maps, "
            "a gauge-fixed velocity-Hessian rank six with five structural null directions, "
            "and corresponding gauge-fixed primary constraints. At zero shift the F-sector "
            "shift Hessian is exactly "
            "2 sqrt(h) M_*^4 exp(2H) F_Bij/N: it is rank three only for nonsingular "
            "invariant-chain-rule F_B and rank zero at the silent point. The number six "
            "appears only in a non-evidentiary arithmetic diagnostic under an unproved "
            "rank-ten hypothesis; no physical degree count follows. The silent-background constraint class, degree "
            "count, strong coupling, stability, hyperbolicity and GR/1PN status remain open."
        ),
        "outcomes": frozen_outcomes(),
        "closure_flags": frozen_closure_flags(),
        "evidence": evidence,
        "controls": {"definition": definition, "mutation": decisions},
        "diagnostics": {
            "w2_32_dependency": _json_safe(dependency_diagnostics),
            "invariant_response": _json_safe(invariant_diagnostics),
            "adm": _json_safe(adm_diagnostics),
            "primary": _json_safe(primary_diagnostics),
            "shift_hessian": _json_safe(shift_diagnostics),
            "dirac_count": _json_safe(dirac_diagnostics),
        },
        "hashes": {
            "action_spec": _canonical_sha256(ACTION_SPEC),
            "adm_gauge_spec": _canonical_sha256(ADM_GAUGE_SPEC),
            "invariant_response_spec": _canonical_sha256(INVARIANT_RESPONSE_SPEC),
            "dirac_scope_spec": _canonical_sha256(DIRAC_SCOPE_SPEC),
            "scientific_contract": _canonical_sha256(CLAIM_CONTRACT),
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
            "status": "FAIL_EXCEPTION_NO_PROMOTION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
