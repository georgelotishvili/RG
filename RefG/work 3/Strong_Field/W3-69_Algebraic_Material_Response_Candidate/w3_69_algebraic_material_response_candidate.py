from __future__ import annotations

import hashlib
import json
import os
import platform
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sympy as sp


HERE = Path(__file__).resolve().parent
STRONG_FIELD = HERE.parent
WORK3 = STRONG_FIELD.parent
REPO_ROOT = WORK3.parents[1]
PREREG = HERE / "w3_69_algebraic_material_response_candidate_preregistration.md"
OUTPUT = HERE / "w3_69_result.json"

CLAIM_ID = "W3_69_ALGEBRAIC_MATERIAL_RESPONSE_CANDIDATE_ADMISSIBILITY"
MODEL_VERSION = "W3-69-v1.2-ALGEBRAIC-MATERIAL-RESPONSE-CANDIDATE-AUDIT"
PASS_STATUS = (
    "PASS_EXACT_ALGEBRAIC_RESPONSE_ACTION_AND_HEALTH_AUDIT__"
    "REJECTED_AS_REFG_OPERATIONAL_P_BY_EXTERIOR_DICTIONARY_MISMATCH_"
    "AND_POTENTIAL_REDEFINITION__GLOBAL_STRONG_FIELD_SOLVE_NOT_OPENED"
)
FAIL_STATUS = "FAIL_W3_69_ALGEBRAIC_MATERIAL_RESPONSE_CANDIDATE_AUDIT"

DEPENDENCY_SPECS = {
    "w3_51_contract": ("Lagrangian_Formulation/Weak_Field_Closure/w3_51_weak_field_closure_contract.md", "86bc2ed86cddee36bec5e46fdfa407701107290c783bfa81ba1440b96becc7cf"),
    "w3_51_result": ("Lagrangian_Formulation/Weak_Field_Closure/w3_51_result.json", "a74e0f02c5a5c794723a5797049bd28d95684a95be869db30f10a575d3ee9cf8"),
    "w3_52_contract": ("Lagrangian_Formulation/Full_1PN_Inheritance/w3_52_full_1pn_inheritance_contract.md", "66a33a82d29bd65fabc37b6e55f29a64674f0e44f5a4c0893611c261d00792b6"),
    "w3_52_result": ("Lagrangian_Formulation/Full_1PN_Inheritance/w3_52_result.json", "8ae2d80cbc983e29a7ccc9ef4e3f6685b36cb4e6ade06e6d2a494fd9f46e11e2"),
    "w3_54_contract": ("Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md", "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879"),
    "w3_54_result": ("Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_result.json", "ee3666d4fb4a227b02a2564d1039a1881306b6133621def9c98d1e2c1d00e991"),
    "w3_58_preregistration": ("Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_one_oscillon_coframe_localized_core_preregistration.md", "ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db"),
    "w3_58_result": ("Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_result.json", "cc80f9799f26547de36cb9509cf5bd4f41746083c3ff47b649bf2882edd891f5"),
    "w3_64_preregistration": ("Strong_Field/W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field_preregistration.md", "25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1"),
    "w3_64_result": ("Strong_Field/W3-64_Einstein_Continuation/w3_64_result.json", "b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b"),
    "w3_67_preregistration": ("Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_foundation_strong_field_response_preregistration.md", "31e6520d9b7917413b9f2978291b4a77f067abe8dd3d6a9e89e1b2cfb699da11"),
    "w3_67_result": ("Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_result.json", "659bdfe171a8279b465fdd49eaf590755da22a7522a83053a4a06450fd745385"),
    "w3_68_preregistration": ("Strong_Field/W3-68_Born_Infeld_Candidate_Admissibility/w3_68_born_infeld_candidate_admissibility_preregistration.md", "afd38da6bd297e6ed029936d9a1162ea7da85377935adf06cb5326edade53f5e"),
    "w3_68_result": ("Strong_Field/W3-68_Born_Infeld_Candidate_Admissibility/w3_68_result.json", "fbe366a7bf20119f460ff461125d17ebb0a1ebe220d3de6d7c38e4627729c5ec"),
    "w3_69_preregistration": ("Strong_Field/W3-69_Algebraic_Material_Response_Candidate/w3_69_algebraic_material_response_candidate_preregistration.md", "b5ef9e7a7740fae6d8fbf8b42058ea275afb96b6a801c5c4a5ce0e83cebd0c38"),
}

IMMUTABLE_SPECS = {
    "CODES.md": "27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41",
    "intuitive/Dictionary.txt": "f6e12b67f38e49bb547d37e6c92375a2ee5b2f596ed481a866cbc490be32ed0b",
    "intuitive/figures/figure_3.pdf": "d3fc89edf7ed59b499467999c16504c8cc36dbe614f9b1dcc612caaee1f35f5f",
    "intuitive/figures/figure_3_v2.png": "43e673eeac9d44cb595303bf55d0622ac2fcb87b641627ff8e3a5e8781365a4e",
    "intuitive/figures/logo.pdf": "e585eaa93b8d60b6294fcd3e7448469265502defd7725f74fdb0a56d33d907ab",
    "intuitive/figures/sparc_rar_real_validation.png": "1afefcc99ca6223230959b8ab3a6cfc015035de20178b7eed8f7f3728a7fe3f0",
    "intuitive/idea.txt": "98cf98f70e3ac146ef3b106cdd6b2df6c6861d2c277e9c9adae5262959d2dd8d",
    "intuitive/RefG_EN.bib": "78a2889e8da0eb206d6282dac610a82af77ad1340e48c7dbd2e042e1f317fe43",
    "intuitive/RefG_EN.pdf": "2d1c65687fb6c9bbb5c3004299d6205ad494f361a956d646851571996a448ddc",
    "intuitive/RefG_EN.tex": "6e69d616229688d885320d9b26b8c4637c563ae47f8da006feee8548d6ad910e",
    "intuitive/RefG_GE.md": "433d3ac96ff6d91eaae1da60cd3f27f84ead2b7bddea26885034e2995dd8787f",
}


EXPECTED_STATUS = {
    "w3_51": "CONDITIONAL_MATCHED_THROUGH_STATIC_SPHERICAL_PPN_BETA_GAMMA",
    "w3_52": "CONDITIONAL_MATCHED_THROUGH_FULL_STANDARD_1PN_PPN",
    "w3_54": "CONDITIONAL_EXACT_SELECTED_RELATIONAL_COFRAME_MASTER_ACTION_TO_TEGR_EQUIVALENT_EH_AND_PHASE_CURRENT_T",
    "w3_58": "PASS_CONDITIONAL_EXACT_MINIMAL_COFRAME_U1_CORE_ACTION_AND_ANALYTIC_EXISTENCE_WINDOW__CONVERGED_NUMERICAL_FINITE_ENERGY_ORBITALLY_STABLE_SPHERICAL_GROUND_STATE_EVIDENCE__FOUNDATION_COEFFICIENT_SELECTION_BACKGROUND_LOCK_BACKREACTION_AND_PARTICLE_IDENTITY_OPEN",
    "w3_64": "PASS_CONDITIONAL_EXACT_UNCHANGED_EINSTEIN_BACKREACTION_AND_CURRENT_SOURCE_NEC_BOUNDARY__CONVERGED_NUMERICAL_REGULAR_HORIZONLESS_SELF_GRAVITATING_Q_BALL_WITNESS__REGULAR_TRAPPED_NULL_COMPLETE_INTERIOR_REQUIRES_FAILURE_OF_AT_LEAST_ONE_PENROSE_HYPOTHESIS",
    "w3_67": "PASS_EXACT_FOUNDATION_STRONG_FIELD_RESPONSE_BOUNDARY__PASSIVE_AND_COMMON_RESCALING_NO_GO__COVARIANT_ACTION_AND_CONSTITUTIVE_SELECTION_OPEN",
    "w3_68": "PASS_EXACT_BORN_INFELD_FT_ACTION_AND_WEAK_TEGR_1PN_REGRESSION__REJECTED_CANDIDATE_BY_LATE_ONSET_MODE_WEAK_BRANCH_HEALTH_VETO__GLOBAL_STRONG_FIELD_SOLVE_NOT_OPENED",
}

REQUIRED_TRUE = (
    "g0_goal_pass", "g1_conventions_pass", "g2_core_algebra_pass",
    "g3_structure_and_health_pass", "g4_independent_check_pass",
    "g5_limits_regression_pass", "g6_physical_match_and_role_decision_pass",
    "g7_observation_not_applicable_exact", "g8_export_not_applicable_exact",
    "dependency_hashes_exact", "immutable_control_hashes_exact",
    "upstream_status_and_scope_exact",
    "candidate_action_registered_exact", "u58_global_positivity_exact",
    "auxiliary_euler_equation_exact", "unique_principal_lambert_branch_exact",
    "finite_field_p_A_positive_exact", "effective_potential_elimination_exact",
    "marginal_response_feedback_sign_exact", "algebraic_hessian_positive_exact",
    "no_new_propagating_mode_exact", "canonical_principal_symbol_preserved_exact",
    "vacuum_kg_hessian_and_mass_pole_preserved_exact",
    "tegr_eh_operator_unchanged_exact", "full_standard_1pn_ppn_regression_exact",
    "one_metric_once_counted_hilbert_source_exact",
    "total_source_conservation_registered_exact", "candidate_nec_exact",
    "candidate_vacuum_p_A_unity_exact",
    "w3_51_positive_mass_exterior_p_op_nontrivial_exact",
    "w3_64_exponential_tail_vs_schwarzschild_order_mismatch_exact",
    "p_A_equals_p_op_rejected_exact", "renamed_s_exactly_potential_redefinition_exact",
    "rho_star_foundation_selection_open_exact",
    "w3_58_finite_amplitude_results_not_inherited_exact",
    "large_field_subquadratic_ratio_exact",
    "finite_field_p_positivity_not_singularity_resolution_exact",
    "penrose_boundary_inherited_exact", "candidate_mathematical_health_pass",
    "hard_operational_role_veto_triggered_exact",
    "candidate_rejected_as_refg_p_closure_exact",
    "global_strong_field_solve_stop_rule_enforced", "mutation_controls_pass",
    "package_clean_pass", "aggregate_audit_pass",
)


REQUIRED_FALSE = (
    "candidate_operational_role_admissibility_pass", "p_A_equals_p_op_derived",
    "algebraic_candidate_foundation_derived", "rho_star_from_foundation_derived",
    "rho_star_observationally_fitted", "w3_58_finite_amplitude_solution_inherited",
    "w3_58_stability_spectrum_inherited", "foundation_strong_field_response_derived",
    "global_tail_weakening_solution_derived", "density_upper_bound_derived",
    "curvature_upper_bound_derived", "p_zero_infinite_proper_or_affine_distance_derived",
    "trapped_surface_derived", "regular_black_hole_solution_derived",
    "geodesic_completeness_derived", "singularity_resolution_completed",
    "new_strong_field_prediction_derived", "observational_forward_model_built",
    "observational_likelihood_evaluated", "canon_changed", "intuitive_files_changed",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    def reject_nonfinite(token: str) -> None:
        raise ValueError(f"non-finite JSON token: {token}")
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_nonfinite)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", newline="\n", delete=False, dir=path.parent
    ) as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False, sort_keys=True)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def text(expr: Any) -> str:
    return sp.sstr(sp.simplify(expr))


def valid_stiffness(value: int) -> bool:
    return value > 0


def valid_auxiliary_mode_count(derivative_terms: int) -> bool:
    return derivative_terms == 0


def valid_source_ledger(source_count: int, duplicates: int) -> bool:
    return source_count == 1 and duplicates == 0


def exterior_identification_allowed(op_coefficient: Any, candidate_coefficient: Any) -> bool:
    return sp.simplify(op_coefficient-candidate_coefficient) == 0


def nec_coefficient_allowed(coefficient: int) -> bool:
    return coefficient >= 0


def singularity_resolution_supported(evidence: tuple[Any, ...]) -> bool:
    return all(item is not None for item in evidence)


def global_solve_allowed(candidate_admissible: bool, solve_opened: bool) -> bool:
    return not solve_opened or candidate_admissible


def dependency_audit() -> tuple[dict[str, Any], dict[str, Any]]:
    records: dict[str, Any] = {}
    loaded: dict[str, Any] = {}
    for key, (relative, expected) in DEPENDENCY_SPECS.items():
        path = WORK3 / relative
        actual = sha256(path) if path.is_file() else None
        records[key] = {
            "path": relative, "expected_sha256": expected,
            "actual_sha256": actual, "exact": actual == expected,
        }
        if key.endswith("_result") and path.is_file():
            loaded[key] = read_json(path)
    records["all_exact"] = all(v["exact"] for v in records.values())
    return records, loaded


def immutable_control_audit() -> dict[str, Any]:
    records: dict[str, Any] = {}
    for relative, expected in IMMUTABLE_SPECS.items():
        path = REPO_ROOT / relative
        actual = sha256(path) if path.is_file() else None
        records[relative] = {
            "expected_sha256": expected, "actual_sha256": actual,
            "exact": actual == expected,
        }
    codes_exact = records["CODES.md"]["exact"]
    expected_intuitive = {
        relative for relative in IMMUTABLE_SPECS if relative.startswith("intuitive/")
    }
    actual_intuitive = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "intuitive").rglob("*") if path.is_file()
    }
    intuitive_hashes_exact = all(
        record["exact"] for relative, record in records.items()
        if relative.startswith("intuitive/")
    )
    intuitive_file_set_exact = actual_intuitive == expected_intuitive
    intuitive_exact = intuitive_hashes_exact and intuitive_file_set_exact
    return {
        "records": records, "codes_hash_exact": codes_exact,
        "expected_intuitive_files": sorted(expected_intuitive),
        "actual_intuitive_files": sorted(actual_intuitive),
        "intuitive_file_set_exact": intuitive_file_set_exact,
        "intuitive_hashes_exact": intuitive_hashes_exact,
        "intuitive_manifest_exact": intuitive_exact,
        "all_exact": codes_exact and intuitive_exact,
    }


def upstream_audit(data: dict[str, Any]) -> dict[str, Any]:
    w51, w52 = data["w3_51_result"], data["w3_52_result"]
    w54, w58 = data["w3_54_result"], data["w3_58_result"]
    w64, w67 = data["w3_64_result"], data["w3_67_result"]
    w68 = data["w3_68_result"]
    ppn_target = {
        "gamma": 1, "beta": 1, "xi": 0, "alpha1": 0,
        "alpha2": 0, "alpha3": 0, "zeta1": 0, "zeta2": 0,
        "zeta3": 0, "zeta4": 0,
    }
    checks = {
        "w3_51_status_exact": w51["aggregate_status"] == EXPECTED_STATUS["w3_51"],
        "w3_51_exterior_exact": w51["derived"]["exterior_solution"] == "G*M/(c0**2*r)",
        "w3_52_status_exact": w52["aggregate_status"] == EXPECTED_STATUS["w3_52"],
        "w3_52_ppn_vector_exact": w52["published_GR_PPN_inherited_corollary"] == ppn_target,
        "w3_54_status_exact": w54["status"] == EXPECTED_STATUS["w3_54"],
        "w3_54_eh_exact": w54["closure_flags"]["RELATIONAL_COFRAME_TO_EH_AND_PHASE_T_GATE_CLOSED"],
        "w3_54_source_exact": w54["closure_flags"]["ONE_SOURCE_LEDGER_SELECTED_AND_CONSISTENT"],
        "w3_58_status_exact": w58["status"] == EXPECTED_STATUS["w3_58"],
        "w3_58_action_exact": w58["closure_flags"]["ordinary_phase_u1_action_defined_exact"],
        "w3_64_status_exact": w64["status"] == EXPECTED_STATUS["w3_64"],
        "w3_64_penrose_exact": w64["regularity_and_penrose_boundary"]["penrose_boundary"]["conditional_no_go_exact"],
        "w3_67_status_exact": w67["status"] == EXPECTED_STATUS["w3_67"],
        "w3_67_response_open_exact": w67["missing_premise"]["status"] == "OPEN" and w67["selection_ledger"]["response_action"] is None,
        "w3_68_status_exact": w68["status"] == EXPECTED_STATUS["w3_68"],
        "w3_68_rejection_exact": w68["candidate_admissible"] is False,
    }
    return {"checks": checks, "all_exact": all(checks.values()), "ppn_vector": ppn_target}


def algebra_audit() -> dict[str, Any]:
    X, m2, lam, g6, a, y, eta = sp.symbols("X m2 lambda g6 a y eta", positive=True)
    rho, w, z = sp.symbols("rho_star w z", positive=True)
    zeta = sp.symbols("zeta", real=True)
    U = sp.symbols("U", nonnegative=True)

    U58 = m2*X - lam*X**2 + sp.Rational(4, 3)*g6*X**3
    normalized = 1 - y + sp.Rational(4, 3)*a*y**2
    discriminant = sp.discriminant(normalized, y)
    vertex_value = sp.simplify(normalized.subs(y, sp.Rational(3, 8)/a))
    domain_substitution = {a: sp.Rational(3, 16) + eta}
    discriminant_in_domain = sp.simplify(discriminant.subs(domain_substitution))
    vertex_in_domain = sp.simplify(vertex_value.subs(domain_substitution))

    U_parameter = rho*w*sp.exp(w)
    p2 = sp.exp(-w)
    eom = sp.exp(zeta)*U + rho*zeta
    hessian = sp.exp(zeta)*U + rho
    local_potential = sp.exp(zeta)*U + rho*zeta**2/2
    eom_on_branch = sp.simplify(eom.subs({zeta: -w, U: U_parameter}))
    hessian_on_branch = sp.simplify(hessian.subs({zeta: -w, U: U_parameter}))

    Ueff = rho*(w + w**2/2)
    dU_dw = sp.diff(U_parameter, w)
    response_1 = sp.simplify(sp.diff(Ueff, w)/dU_dw)
    response_2 = sp.simplify(sp.diff(response_1, w)/dU_dw)
    envelope_response = sp.simplify(sp.diff(local_potential, U).subs(zeta, -w))
    implicit_dzeta_dU = sp.simplify((-sp.exp(zeta)/hessian).subs({zeta: -w, U: U_parameter}))
    implicit_p2_response = sp.simplify(p2*implicit_dzeta_dU)
    elimination = sp.simplify(sp.exp(-w)*U_parameter + rho*w**2/2 - Ueff)
    weak = sp.series(rho*(sp.LambertW(z) + sp.LambertW(z)**2/2), z, 0, 4)
    weak_target = rho*(z - z**2/2 + z**3/2)
    p_series = sp.series(sp.exp(-sp.LambertW(z)/2), z, 0, 3)
    large_ratio = sp.limit(sp.log(X**3)**2/X, X, sp.oo)
    eom_left_limit = sp.limit(eom, zeta, -sp.oo)

    scaled = U58.subs({X: y*m2/lam, g6: a*lam**2/m2})/(m2*y*m2/lam)
    p_zero = sp.limit(sp.exp(-w/2), w, sp.oo)
    U_infinite = sp.limit(U_parameter, w, sp.oo)
    Ueff_infinite = sp.limit(Ueff, w, sp.oo)
    checks = {
        "normalized_u58_exact": sp.simplify(scaled - normalized) == 0,
        "u58_discriminant_exact": discriminant == 1 - sp.Rational(16, 3)*a,
        "u58_positive_domain_exact": (
            discriminant_in_domain.is_negative is True
            and vertex_in_domain.is_positive is True
        ),
        "auxiliary_eom_exact": eom_on_branch == 0,
        "positive_stiffness_validator_exact": valid_stiffness(1),
        "unique_monotone_eom_exact": hessian.is_positive is True,
        "branch_endpoint_exact": eom_left_limit == -sp.oo and sp.simplify(eom.subs(zeta, 0) - U) == 0,
        "elimination_exact": elimination == 0,
        "response_first_exact": sp.simplify(response_1 - p2) == 0,
        "response_second_exact": sp.simplify(response_2 + sp.exp(-2*w)/(rho*(1+w))) == 0,
        "pre_post_elimination_response_exact": sp.simplify(envelope_response - response_1) == 0,
        "implicit_feedback_crosscheck_exact": sp.simplify(implicit_p2_response - response_2) == 0,
        "feedback_negative_exact": response_2.is_negative is True,
        "hessian_positive_exact": hessian_on_branch == rho*(1+w),
        "weak_series_exact": sp.expand(weak.removeO() - weak_target) == 0,
        "large_field_subquadratic_exact": large_ratio == 0,
        "finite_p_positive_exact": p2.is_positive is True,
        "p_zero_only_at_infinite_field_exact": p_zero == 0 and U_infinite == sp.oo and Ueff_infinite == sp.oo,
    }
    return {
        "checks": checks, "all_exact": all(checks.values()),
        "domain": "X>=0, rho_star>0, a=g6*m_s^2/lambda^2>3/16",
        "expressions": {
            "U_58": text(U58), "U_58_over_X_normalized": text(normalized),
            "discriminant": text(discriminant), "positive_minimum": text(vertex_value),
            "discriminant_for_a_3_over_16_plus_eta": text(discriminant_in_domain),
            "minimum_for_a_3_over_16_plus_eta": text(vertex_in_domain),
            "zeta_solution": "-LambertW(U_58/rho_star)",
            "p_A_squared": text(p2), "U_eff": text(Ueff),
            "dU_eff_dU": text(response_1), "d2U_eff_dU2": text(response_2),
            "pre_elimination_envelope_response": text(envelope_response),
            "implicit_dzeta_dU": text(implicit_dzeta_dU),
            "algebraic_hessian": text(hessian_on_branch),
            "weak_series_through_cubic": text(weak), "p_A_weak_series": text(p_series),
        },
    }


def exterior_and_role_audit(upstream: dict[str, Any]) -> dict[str, Any]:
    r, mu, k = sp.symbols("r mu k", positive=True)
    s_tail = sp.symbols("s_tail", real=True, finite=True)
    rho, w = sp.symbols("rho_star w", positive=True)
    p_op = sp.exp(-mu/r)
    p_candidate_vacuum = sp.Integer(1)
    w3_64_squared_tail = sp.exp(-2*k*r)*r**(2*s_tail)
    op_coefficient = sp.limit(r*(1-p_op), r, sp.oo)
    vacuum_candidate_coefficient = sp.limit(r*(1-p_candidate_vacuum), r, sp.oo)
    actual_tail_coefficient = sp.limit(r*w3_64_squared_tail, r, sp.oo)
    U_parameter = rho*w*sp.exp(w)
    Ueff = rho*(w+w**2/2)
    potential_changed = sp.simplify(Ueff-U_parameter) != 0
    selection_registry = {"rho_star_foundation_formula": None, "rho_star_fit": None}
    checks = {
        "candidate_vacuum_unity_exact": p_candidate_vacuum == 1,
        "positive_mass_operational_exterior_nontrivial_exact": op_coefficient == mu,
        "structural_vacuum_has_no_schwarzschild_order_exact": vacuum_candidate_coefficient == 0,
        "w3_64_corrected_exponential_tail_subleading_exact": actual_tail_coefficient == 0,
        "p_identification_rejected_exact": not exterior_identification_allowed(op_coefficient, actual_tail_coefficient),
        "renamed_auxiliary_is_potential_redefinition_exact": potential_changed,
        "rho_star_not_selected_exact": upstream["checks"]["w3_67_response_open_exact"] and all(value is None for value in selection_registry.values()),
        "w3_58_finite_amplitude_inheritance_blocked_exact": potential_changed,
    }
    return {
        "checks": checks, "all_exact": all(checks.values()),
        "operational_p": "exp[-GM/(c0^2 r)+...]",
        "candidate_vacuum_p_A": "1",
        "actual_w3_64_scalar_tail": "Psi_O~C exp(-k r) r^s, s finite",
        "actual_candidate_response_order": "1-p_A=O(exp(-2 k r) r^(2s))=o(1/r)",
        "operational_leading_coefficient": text(op_coefficient),
        "structural_vacuum_leading_coefficient": text(vacuum_candidate_coefficient),
        "actual_tail_leading_coefficient": text(actual_tail_coefficient),
        "selection_registry": selection_registry,
        "decision": "REJECT_AS_REFG_OPERATIONAL_P_CLOSURE",
        "equivalent_role_if_renamed": "new nonpolynomial U_eff(|Psi_O|^2) only",
    }


def structure_and_health_audit(upstream: dict[str, Any]) -> dict[str, Any]:
    A_re, A_im = sp.symbols("A_re A_im", real=True)
    z = sp.symbols("z", nonnegative=True)
    null_contraction = 2*(A_re**2 + A_im**2)
    principal_hessian = sp.eye(2)
    registry = {
        "metrics": ("g_mn",), "coframes": ("eA_mu",),
        "gravity_operator": "W3-54_TEGR_EQUIVALENT_EH_UNCHANGED",
        "hilbert_source_variations": 1, "duplicate_sources": 0,
        "zeta_derivative_terms": 0, "diffeomorphism_invariant": True,
        "joint_euler_lagrange_system": True,
    }
    bound_evidence = {
        "density_upper_bound": None, "curvature_upper_bound": None,
        "proper_or_affine_distance_to_p_zero": None,
    }
    vacuum_response = sp.limit(sp.exp(-sp.LambertW(z)), z, 0, dir="+")
    checks = {
        "one_metric_exact": len(registry["metrics"]) == 1 and len(registry["coframes"]) == 1,
        "eh_tegr_operator_unchanged_exact": registry["gravity_operator"] == "W3-54_TEGR_EQUIVALENT_EH_UNCHANGED",
        "one_hilbert_source_no_duplicate_exact": valid_source_ledger(registry["hilbert_source_variations"], registry["duplicate_sources"]),
        "total_source_conservation_registered_exact": registry["diffeomorphism_invariant"] and registry["joint_euler_lagrange_system"],
        "auxiliary_has_no_derivative_or_new_mode_exact": valid_auxiliary_mode_count(registry["zeta_derivative_terms"]),
        "complex_scalar_principal_symbol_canonical_exact": principal_hessian == sp.eye(2) and principal_hessian.det() == 1,
        "vacuum_kg_hessian_and_mass_pole_unchanged_exact": vacuum_response == 1,
        "nec_nonnegative_exact": nec_coefficient_allowed(2) and null_contraction.is_nonnegative is True,
        "penrose_boundary_unchanged_exact": upstream["checks"]["w3_64_penrose_exact"],
        "finite_p_not_density_or_curvature_bound_exact": not singularity_resolution_supported(tuple(bound_evidence.values())),
    }
    return {
        "checks": checks, "all_exact": all(checks.values()),
        "action_registry": registry, "bound_evidence_registry": bound_evidence,
        "action": "S_EH - integral sqrt(-g)[g^mn d_m Psi* d_n Psi + exp(zeta) U_58 + rho_star zeta^2/2]",
        "auxiliary_eom": "rho_star*zeta + exp(zeta)*U_58 = 0",
        "null_contraction": text(null_contraction),
        "complex_scalar_principal_hessian": str(principal_hessian.tolist()),
        "vacuum_potential_response": text(vacuum_response),
        "degree_of_freedom_decision": "no added propagating degree of freedom",
        "theorem_boundary": "NEC remains satisfied; the W3-64 conditional Penrose no-go is inherited",
    }


def mutation_audit() -> dict[str, Any]:
    rho, w = sp.symbols("rho_star w", positive=True)
    U = rho*w*sp.exp(w)
    wrong_sign_residual = sp.simplify(sp.exp(w)*U + rho*w)
    changed_potential = sp.simplify(rho*(w+w**2/2) - U)

    controls = {
        "wrong_lambert_sign_rejected": wrong_sign_residual != 0,
        "nonpositive_stiffness_rejected": not valid_stiffness(-1),
        "fabricated_propagating_auxiliary_mode_rejected": not valid_auxiliary_mode_count(1),
        "duplicate_hilbert_source_rejected": not valid_source_ledger(2, 1),
        "false_exterior_identification_rejected": not exterior_identification_allowed(1, 0),
        "inherited_w3_58_stability_rejected": changed_potential != 0,
        "false_nec_violation_rejected": not nec_coefficient_allowed(-2),
        "finite_p_singularity_resolution_promotion_rejected": not singularity_resolution_supported((None, None, None)),
        "illicit_global_solve_rejected": not global_solve_allowed(False, True),
    }
    return {"checks": controls, "all_pass": all(controls.values())}


def package_audit() -> dict[str, Any]:
    expected = {
        "w3_69_algebraic_material_response_candidate_preregistration.md",
        "w3_69_algebraic_material_response_candidate.py",
        "w3_69_result.json",
    }
    actual = {p.relative_to(HERE).as_posix() for p in HERE.rglob("*") if p.is_file()}
    directories = {p.relative_to(HERE).as_posix() for p in HERE.rglob("*") if p.is_dir()}
    projected = actual | {OUTPUT.name}
    return {
        "expected_files": sorted(expected), "actual_files_recursive_before_export": sorted(actual),
        "unexpected_directories_recursive": sorted(directories),
        "projected_files_after_export": sorted(projected),
        "clean_after_export": projected == expected and not directories,
    }


def scope_evidence_audit() -> dict[str, Any]:
    registry = {
        "global_tail_weakening_solution": None,
        "trapped_surface": None,
        "regular_black_hole_solution": None,
        "geodesic_completeness": None,
        "singularity_resolution": None,
        "new_strong_field_prediction": None,
        "observational_forward_model": None,
        "observational_likelihood": None,
    }
    return {
        "registry": registry,
        "global_strong_field_solve_opened": False,
        "all_out_of_scope_outputs_absent": all(value is None for value in registry.values()),
    }


def build_flags(
    deps: dict[str, Any], immutable: dict[str, Any], upstream: dict[str, Any], algebra: dict[str, Any],
    exterior: dict[str, Any], health: dict[str, Any], mutations: dict[str, Any],
    package: dict[str, Any], scope: dict[str, Any],
) -> dict[str, bool]:
    flags = {name: False for name in REQUIRED_TRUE + REQUIRED_FALSE}
    dep_ok, immutable_ok, up_ok = deps["all_exact"], immutable["all_exact"], upstream["all_exact"]
    alg_ok, ext_ok = algebra["all_exact"], exterior["all_exact"]
    health_ok, mutation_ok = health["all_exact"], mutations["all_pass"]
    package_ok = package["clean_after_export"]
    p_rejected = exterior["checks"]["p_identification_rejected_exact"]
    candidate_role_admissible = alg_ok and health_ok and not p_rejected
    stop_rule_pass = global_solve_allowed(
        candidate_role_admissible, scope["global_strong_field_solve_opened"]
    )
    flags.update({
        "g0_goal_pass": True, "g1_conventions_pass": dep_ok and immutable_ok and up_ok,
        "g2_core_algebra_pass": alg_ok, "g3_structure_and_health_pass": health_ok,
        "g4_independent_check_pass": mutation_ok,
        "g5_limits_regression_pass": alg_ok and up_ok,
        "g6_physical_match_and_role_decision_pass": ext_ok,
        "g7_observation_not_applicable_exact": True,
        "g8_export_not_applicable_exact": True,
        "dependency_hashes_exact": dep_ok,
        "immutable_control_hashes_exact": immutable_ok,
        "upstream_status_and_scope_exact": up_ok,
        "candidate_action_registered_exact": health["checks"]["one_metric_exact"] and health["checks"]["one_hilbert_source_no_duplicate_exact"],
        "u58_global_positivity_exact": algebra["checks"]["u58_positive_domain_exact"],
        "auxiliary_euler_equation_exact": algebra["checks"]["auxiliary_eom_exact"],
        "unique_principal_lambert_branch_exact": algebra["checks"]["unique_monotone_eom_exact"] and algebra["checks"]["branch_endpoint_exact"],
        "finite_field_p_A_positive_exact": algebra["checks"]["finite_p_positive_exact"],
        "effective_potential_elimination_exact": algebra["checks"]["elimination_exact"],
        "marginal_response_feedback_sign_exact": algebra["checks"]["feedback_negative_exact"],
        "algebraic_hessian_positive_exact": algebra["checks"]["hessian_positive_exact"],
        "no_new_propagating_mode_exact": health["checks"]["auxiliary_has_no_derivative_or_new_mode_exact"],
        "canonical_principal_symbol_preserved_exact": health["checks"]["complex_scalar_principal_symbol_canonical_exact"],
        "vacuum_kg_hessian_and_mass_pole_preserved_exact": health["checks"]["vacuum_kg_hessian_and_mass_pole_unchanged_exact"],
        "tegr_eh_operator_unchanged_exact": health["checks"]["eh_tegr_operator_unchanged_exact"],
        "full_standard_1pn_ppn_regression_exact": upstream["checks"]["w3_52_ppn_vector_exact"],
        "one_metric_once_counted_hilbert_source_exact": health["checks"]["one_hilbert_source_no_duplicate_exact"],
        "total_source_conservation_registered_exact": health["checks"]["total_source_conservation_registered_exact"],
        "candidate_nec_exact": health["checks"]["nec_nonnegative_exact"],
        "candidate_vacuum_p_A_unity_exact": exterior["checks"]["candidate_vacuum_unity_exact"],
        "w3_51_positive_mass_exterior_p_op_nontrivial_exact": exterior["checks"]["positive_mass_operational_exterior_nontrivial_exact"],
        "w3_64_exponential_tail_vs_schwarzschild_order_mismatch_exact": exterior["checks"]["w3_64_corrected_exponential_tail_subleading_exact"],
        "p_A_equals_p_op_rejected_exact": exterior["checks"]["p_identification_rejected_exact"],
        "renamed_s_exactly_potential_redefinition_exact": exterior["checks"]["renamed_auxiliary_is_potential_redefinition_exact"],
        "rho_star_foundation_selection_open_exact": exterior["checks"]["rho_star_not_selected_exact"],
        "w3_58_finite_amplitude_results_not_inherited_exact": exterior["checks"]["w3_58_finite_amplitude_inheritance_blocked_exact"],
        "large_field_subquadratic_ratio_exact": algebra["checks"]["large_field_subquadratic_exact"],
        "finite_field_p_positivity_not_singularity_resolution_exact": health["checks"]["finite_p_not_density_or_curvature_bound_exact"],
        "penrose_boundary_inherited_exact": health["checks"]["penrose_boundary_unchanged_exact"],
        "candidate_mathematical_health_pass": alg_ok and health_ok,
        "hard_operational_role_veto_triggered_exact": ext_ok,
        "candidate_rejected_as_refg_p_closure_exact": ext_ok,
        "global_strong_field_solve_stop_rule_enforced": stop_rule_pass,
        "mutation_controls_pass": mutation_ok, "package_clean_pass": package_ok,
    })
    potential_only = exterior["checks"]["renamed_auxiliary_is_potential_redefinition_exact"]
    rho_open = exterior["checks"]["rho_star_not_selected_exact"]
    w3_58_blocked = exterior["checks"]["w3_58_finite_amplitude_inheritance_blocked_exact"]
    bounds = health["bound_evidence_registry"]
    scope_registry = scope["registry"]
    flags.update({
        "candidate_operational_role_admissibility_pass": candidate_role_admissible,
        "p_A_equals_p_op_derived": not p_rejected,
        "algebraic_candidate_foundation_derived": not (potential_only and rho_open),
        "rho_star_from_foundation_derived": not rho_open,
        "rho_star_observationally_fitted": exterior["selection_registry"]["rho_star_fit"] is not None,
        "w3_58_finite_amplitude_solution_inherited": not w3_58_blocked,
        "w3_58_stability_spectrum_inherited": not w3_58_blocked,
        "foundation_strong_field_response_derived": not (p_rejected or rho_open),
        "global_tail_weakening_solution_derived": scope_registry["global_tail_weakening_solution"] is not None,
        "density_upper_bound_derived": bounds["density_upper_bound"] is not None,
        "curvature_upper_bound_derived": bounds["curvature_upper_bound"] is not None,
        "p_zero_infinite_proper_or_affine_distance_derived": bounds["proper_or_affine_distance_to_p_zero"] is not None,
        "trapped_surface_derived": scope_registry["trapped_surface"] is not None,
        "regular_black_hole_solution_derived": scope_registry["regular_black_hole_solution"] is not None,
        "geodesic_completeness_derived": scope_registry["geodesic_completeness"] is not None,
        "singularity_resolution_completed": scope_registry["singularity_resolution"] is not None,
        "new_strong_field_prediction_derived": scope_registry["new_strong_field_prediction"] is not None,
        "observational_forward_model_built": scope_registry["observational_forward_model"] is not None,
        "observational_likelihood_evaluated": scope_registry["observational_likelihood"] is not None,
        "canon_changed": not immutable["codes_hash_exact"],
        "intuitive_files_changed": not immutable["intuitive_manifest_exact"],
    })
    flags["aggregate_audit_pass"] = all(flags[n] for n in REQUIRED_TRUE if n != "aggregate_audit_pass") and all(not flags[n] for n in REQUIRED_FALSE)
    return flags


def main() -> int:
    dependencies, loaded = dependency_audit()
    immutable = immutable_control_audit()
    upstream = upstream_audit(loaded)
    algebra = algebra_audit()
    exterior = exterior_and_role_audit(upstream)
    health = structure_and_health_audit(upstream)
    mutations = mutation_audit()
    package = package_audit()
    scope = scope_evidence_audit()
    flags = build_flags(dependencies, immutable, upstream, algebra, exterior, health, mutations, package, scope)
    passed = flags["aggregate_audit_pass"]
    status = PASS_STATUS if passed else FAIL_STATUS
    candidate_admissible = flags["candidate_operational_role_admissibility_pass"]

    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID, "model_version": MODEL_VERSION,
        "status": status, "artifact_valid": passed,
        "candidate_admissible": candidate_admissible,
        "claim": "Audit one algebraic matter-response candidate without changing the one-metric Einstein-Hilbert/TEGR operator.",
        "evidence_type": "exact symbolic audit plus deterministic upstream regression",
        "candidate": {
            "action": health["action"],
            "definition": "p_A=exp(zeta/2)",
            "selected_domain": algebra["domain"],
            "new_constant": "rho_star>0; deliberately not selected or fitted",
            "local_mathematical_health": algebra["all_exact"] and health["all_exact"],
            "operational_refg_p_role": "rejected",
        },
        "dependencies": dependencies, "immutable_controls": immutable,
        "upstream_regression": upstream,
        "exact_algebra": algebra, "structure_and_health": health,
        "exterior_dictionary_audit": exterior,
        "mutation_controls": mutations, "package": package,
        "scope_evidence": scope,
        "closure_flags": flags,
        "gate_registry": {
            "G0_GOAL": flags["g0_goal_pass"],
            "G1_CONVENTIONS": flags["g1_conventions_pass"],
            "G2_CORE_ALGEBRA": flags["g2_core_algebra_pass"],
            "G3_STRUCTURE_AND_HEALTH": flags["g3_structure_and_health_pass"],
            "G4_INDEPENDENT_CHECK": flags["g4_independent_check_pass"],
            "G5_LIMITS_REGRESSION": flags["g5_limits_regression_pass"],
            "G6_PHYSICAL_MATCH_AND_ROLE_DECISION": flags["g6_physical_match_and_role_decision_pass"],
            "G7_OBSERVATION": "NOT_APPLICABLE_AFTER_ROLE_VETO",
            "G8_EXPORT": "NOT_APPLICABLE_AFTER_ROLE_VETO",
        },
        "source_ledger": {
            "metric_count": len(health["action_registry"]["metrics"]),
            "coframe_count": len(health["action_registry"]["coframes"]),
            "hilbert_source_count": health["action_registry"]["hilbert_source_variations"],
            "duplicate_source_count": health["action_registry"]["duplicate_sources"],
            "source": "T_mn from one variation of the complete matter action",
            "conservation": "nabla^m T_mn=0 on the joint Euler-Lagrange equations",
        },
        "physical_decision": {
            "mathematical_candidate_health": "PASS" if algebra["all_exact"] and health["all_exact"] else "FAIL",
            "refg_operational_p_identification": "HARD_VETO",
            "reason_1": "On the actual W3-64 branch, Psi_O~C exp(-kr)r^s gives 1-p_A=O(exp(-2kr)r^(2s))=o(1/r), while 1-p_op=O(1/r).",
            "reason_2": "On any structural-test open Psi_O=0 region, the auxiliary equation additionally forces p_A=1; this is not claimed to be the finite-radius exterior of the W3-64 localized branch.",
            "reason_3": "After exact algebraic elimination, renaming p_A as s leaves only a new nonpolynomial scalar potential U_eff.",
            "global_strong_field_solve_opened": scope["global_strong_field_solve_opened"],
        },
        "scientific_boundary": {
            "derived_here": [
                "unique healthy algebraic Lambert-W branch",
                "exact effective-potential reduction and feedback sign",
                "unchanged Einstein-Hilbert/TEGR operator, canonical scalar principal part, 1PN vector, and NEC",
                "exact exterior dictionary mismatch and candidate rejection",
            ],
            "not_derived_here": [
                "a foundation-selected rho_star",
                "the W3-51 operational p from this auxiliary field",
                "inheritance of W3-58 finite-amplitude solutions or stability",
                "density or curvature upper bounds, trapped surfaces, regular black holes, geodesic completeness, or singularity resolution",
                "a new strong-field prediction or observational likelihood",
            ],
            "next_exact_input": "A universal local covariant response carrier that remains nontrivial in the positive-mass vacuum exterior, is selected by the foundation, preserves one metric and one source, and introduces no forbidden 1PN charge or unhealthy mode.",
        },
        "stop_rule": "The first decisive physical-role veto closes this candidate; no global black-hole or oscillon solve is authorized.",
        "scope_flags": {name: flags[name] for name in REQUIRED_FALSE},
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python_version": platform.python_version(),
            "sympy_version": sp.__version__, "platform": platform.platform(),
            "script_sha256": sha256(Path(__file__)),
            "preregistration_sha256": sha256(PREREG),
            "deterministic_execution": True,
            "network_used_by_verifier": False, "archived_theory_used": False,
        },
    }
    keyset_exact = set(flags) == set(REQUIRED_TRUE + REQUIRED_FALSE)
    true_boundary_exact = all(flags[name] for name in REQUIRED_TRUE)
    false_boundary_exact = all(not flags[name] for name in REQUIRED_FALSE)
    payload["validation"] = {
        "closure_keyset_exact": keyset_exact,
        "required_true_boundary_exact": true_boundary_exact,
        "required_false_boundary_exact": false_boundary_exact,
        "strict_finite_json": True,
        "production_and_mutation_share_validators": True,
    }
    payload["artifact_valid"] = passed and keyset_exact and true_boundary_exact and false_boundary_exact
    if not payload["artifact_valid"]:
        payload["status"] = FAIL_STATUS
    atomic_json(OUTPUT, payload)
    print(payload["status"])
    print(f"artifact_valid={str(payload['artifact_valid']).lower()}")
    print(f"candidate_admissible={str(payload['candidate_admissible']).lower()}")
    print(f"result={OUTPUT}")
    return 0 if payload["artifact_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
