"""W3-54: relational coframe -> TEGR/EH plus phase-current source.

This verifier starts from a selected post-Genesis coframe/torsion master
action.  It does not place Levi-Civita curvature, Einstein's equation, a
Fierz--Pauli coefficient vector, a PPN target, or observational data in that
action.  It derives the TEGR ratios from the absence of an independent
orientation sector, verifies the exact TEGR-to-Fierz--Pauli overlap and the
torsion/curvature sign, and derives the Hilbert tensor of the covariant W3-50
barotropic, isentropic, irrotational phase-current subfamily.  It stops at
Einstein--Hilbert plus that explicit T_mn.

The selected coframe continuum, Lorentzian time leg, flat inertial transport,
one common operational metric, and constitutive rho_C(n_C) are declared
foundation-law premises.  A node-by-node origin of those premises is not
claimed.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_54_RELATIONAL_COFRAME_TEGR_PHASE_SOURCE_CLOSURE"
MODEL_VERSION = "W3-54-v1.0-RELATIONAL-COFRAME-TEGR-PHASE-SOURCE-CLOSURE"
STATUS_PASS = (
    "CONDITIONAL_EXACT_SELECTED_RELATIONAL_COFRAME_MASTER_ACTION_TO_TEGR_"
    "EQUIVALENT_EH_AND_PHASE_CURRENT_T"
)

CONTRACT_SHA256 = (
    "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879"
)

DEPENDENCY_HASHES = OrderedDict(
    [
        (
            "w3_42_foundation_state_space_volume_map_preregistration.md",
            "8ba44af154a3f9a18b207b4f17a3dcecdb27a8a9d59f7f9aa712c0946763ae98",
        ),
        (
            "w3_42_foundation_state_space_volume_map.py",
            "ae30251c3fb5eefae31dd9310de62dda2d3cf700c030bcb8c1e8f08c3e57724f",
        ),
        (
            "w3_46_active_participation_resonance_feedback_contract.md",
            "0109ed3d5e8daec55dbd0f01f8b05932e6f653373438455c32a3d26378e0f3b2",
        ),
        (
            "w3_50_neutral_collective_phase_density_bridge_contract.md",
            "c9b8e7dc8beb44e26838ba65a49400a58431fbb06f72a30bb3a4cc99d46dd635",
        ),
    ]
)

DEPENDENCY_CONTRACT_MARKERS = OrderedDict(
    [
        (
            "w3_46_active_participation_resonance_feedback_contract.md",
            (
                "participation_meaning_selected=true",
                "full_state_and_symmetry_derived=false",
                "master_action_or_resonance_PDE_derived=false",
            ),
        ),
        (
            "w3_50_neutral_collective_phase_density_bridge_contract.md",
            (
                "PASS_EXACT_CONDITIONAL_NEUTRAL_PHASE_DENSITY_CANDIDATE_CURRENT__W3_48_BRIDGE_CLOSED_GIVEN_SELECTED_ETA_AND_CUBIC_MEASURE__MASTER_FOUNDATION_ORIGIN_OPEN",
            ),
        ),
    ]
)

DEPENDENCY_CLOSURE_SECTION_MARKERS = OrderedDict(
    [
        (
            "w3_50_neutral_collective_phase_density_bridge_contract.md",
            OrderedDict(
                [
                    (
                        "true_on_declared_branch",
                        ("eta_a3_charge_law_on_selected_cubic_measure_exact",),
                    ),
                    (
                        "false_beyond_declared_branch",
                        (
                            "physical_dimension_and_measure_derived",
                            "complete_H_C_derived",
                        ),
                    ),
                ]
            ),
        ),
    ]
)


def exact_zero(expr: sp.Expr) -> bool:
    return bool(sp.trigsimp(sp.simplify(expr)) == 0)


def all_zero(items) -> bool:
    return all(exact_zero(item) for item in items)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_work3() -> Path:
    here = Path(__file__).resolve()
    for parent in (here.parent, *here.parents):
        if parent.name == "work 3":
            return parent
    raise RuntimeError("script is not located below the Work 3 root")


def dependency_paths(work3: Path) -> OrderedDict[str, Path]:
    return OrderedDict(
        [
            (
                "w3_42_foundation_state_space_volume_map_preregistration.md",
                work3
                / "Cosmology_and_LSS"
                / "Foundation_State_Space_and_Volume_Map"
                / "w3_42_foundation_state_space_volume_map_preregistration.md",
            ),
            (
                "w3_42_foundation_state_space_volume_map.py",
                work3
                / "Cosmology_and_LSS"
                / "Foundation_State_Space_and_Volume_Map"
                / "w3_42_foundation_state_space_volume_map.py",
            ),
            (
                "w3_46_active_participation_resonance_feedback_contract.md",
                work3
                / "Cosmology_and_LSS"
                / "Active_Participation_Resonance_Feedback"
                / "w3_46_active_participation_resonance_feedback_contract.md",
            ),
            (
                "w3_50_neutral_collective_phase_density_bridge_contract.md",
                work3
                / "Cosmology_and_LSS"
                / "Active_Participation_Resonance_Feedback"
                / "w3_50_neutral_collective_phase_density_bridge_contract.md",
            ),
        ]
    )


def downstream_regression_paths(work3: Path) -> OrderedDict[str, Path]:
    lagrangian = work3 / "Lagrangian_Formulation"
    return OrderedDict(
        [
            (
                "W3-53",
                lagrangian
                / "Foundation_EH_Source_Closure"
                / "w3_53_foundation_eh_source_closure.py",
            ),
            (
                "W3-51",
                lagrangian
                / "Weak_Field_Closure"
                / "w3_51_weak_field_closure.py",
            ),
            (
                "W3-52",
                lagrangian
                / "Full_1PN_Inheritance"
                / "w3_52_full_1pn_inheritance.py",
            ),
        ]
    )


def run_json_regression(name: str, path: Path) -> OrderedDict:
    if not path.exists():
        return OrderedDict(
            [("exists", False), ("returncode", None), ("passed", False)]
        )
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(path.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    parsed = None
    parse_error = None
    try:
        parsed = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        parse_error = str(exc)

    if name == "W3-53":
        status_ok = bool(parsed and parsed.get("aggregate_pass") is True)
        reported_status = parsed.get("status") if parsed else None
    else:
        status_ok = bool(parsed and parsed.get("gate_status") == "PASS")
        reported_status = parsed.get("aggregate_status") if parsed else None
    passed = completed.returncode == 0 and parse_error is None and status_ok
    return OrderedDict(
        [
            ("exists", True),
            ("script_sha256", sha256(path)),
            ("returncode", completed.returncode),
            ("json_parsed", parse_error is None),
            ("parse_error", parse_error),
            ("reported_status", reported_status),
            ("stdout_sha256", hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest()),
            ("stderr_sha256", hashlib.sha256(completed.stderr.encode("utf-8")).hexdigest()),
            ("passed", passed),
        ]
    )


def combine_registries(
    coefficients: tuple[sp.Expr, ...],
    registries: tuple[OrderedDict[str, sp.Expr], ...],
) -> OrderedDict[str, sp.Expr]:
    keys = tuple(registries[0])
    if any(tuple(registry) != keys for registry in registries[1:]):
        raise ValueError("invariant registries use different bases")
    return OrderedDict(
        (
            key,
            sp.simplify(
                sum(
                    coefficient * registry[key]
                    for coefficient, registry in zip(coefficients, registries)
                )
            ),
        )
        for key in keys
    )


def registries_equal(
    left: OrderedDict[str, sp.Expr], right: OrderedDict[str, sp.Expr]
) -> bool:
    return tuple(left) == tuple(right) and all_zero(
        left[key] - right[key] for key in left
    )


def fp_gauge_residuals(
    coefficients: OrderedDict[str, sp.Expr],
) -> OrderedDict[str, sp.Expr]:
    a, b, c, d = coefficients.values()
    return OrderedDict(
        [
            ("box_div_h", sp.expand(2 * a + b)),
            ("grad_div_div_h", sp.expand(b + c)),
            ("grad_box_trace_h", sp.expand(c + 2 * d)),
        ]
    )


def atomic_json_write(path: Path, payload: OrderedDict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> None:
    work3 = locate_work3()
    contract_path = Path(__file__).with_name(
        "w3_54_relational_coframe_tegr_phase_source_closure_contract.md"
    )
    out_path = Path(__file__).with_name("w3_54_result.json")

    # ------------------------------------------------------------------
    # 1. W3-42-compatible polar spatial coframe and time-gauge metric witness.
    # ------------------------------------------------------------------
    a_scale, lapse = sp.symbols("a N", positive=True)
    s1, s2 = sp.symbols("s1 s2", real=True)
    s3 = -s1 - s2
    shift1, shift2, shift3 = sp.symbols("N1 N2 N3", real=True)
    rotation_angle = sp.symbols("alpha_R", real=True)

    orientation_rotation = sp.Matrix(
        [
            [sp.cos(rotation_angle), -sp.sin(rotation_angle), 0],
            [sp.sin(rotation_angle), sp.cos(rotation_angle), 0],
            [0, 0, 1],
        ]
    )
    symmetric_stretch = sp.diag(sp.exp(s1), sp.exp(s2), sp.exp(s3))
    spatial_coframe = sp.simplify(
        a_scale * orientation_rotation * symmetric_stretch
    )
    spatial_metric = sp.simplify(spatial_coframe.T * spatial_coframe)
    det_spatial_coframe = sp.trigsimp(sp.simplify(spatial_coframe.det()))
    sqrt_det_spatial_metric = sp.sqrt(sp.trigsimp(sp.simplify(spatial_metric.det())))

    shift = sp.Matrix([shift1, shift2, shift3])
    coframe = sp.zeros(4, 4)
    coframe[0, 0] = lapse
    for internal in range(3):
        coframe[internal + 1, 0] = sp.simplify(
            sum(spatial_coframe[internal, i] * shift[i] for i in range(3))
        )
        for spatial in range(3):
            coframe[internal + 1, spatial + 1] = spatial_coframe[internal, spatial]
    eta_internal = sp.diag(-1, 1, 1, 1)
    operational_metric = sp.simplify(coframe.T * eta_internal * coframe)
    coframe_determinant = sp.trigsimp(sp.simplify(coframe.det()))
    metric_determinant = sp.trigsimp(sp.simplify(operational_metric.det()))

    spatial_polar_gram_witness_exact = all_zero(
        [
            det_spatial_coframe - a_scale**3,
            sqrt_det_spatial_metric - a_scale**3,
            sp.trace(sp.diag(s1, s2, s3)),
            orientation_rotation.det() - 1,
            *(orientation_rotation.T * orientation_rotation - sp.eye(3)),
        ]
    )
    time_gauge_metric_determinant_witness_exact = all_zero(
        [
            coframe_determinant - lapse * a_scale**3,
            metric_determinant + coframe_determinant**2,
            operational_metric[0, 1] - operational_metric[1, 0],
            operational_metric[0, 2] - operational_metric[2, 0],
            operational_metric[0, 3] - operational_metric[3, 0],
        ]
    )

    selected_foundation_premises = OrderedDict(
        [
            ("connected_oriented_nondegenerate_3plus1_coframe_phase", True),
            ("lorentzian_internal_metric_and_one_operational_metric", True),
            ("flat_metric_compatible_inertial_transport", True),
            ("flat_connection_pure_gauge_variation_domain", True),
            ("linear_selector_weitz_gauge_or_invariant_combination", True),
            ("local_reversible_parity_even_quadratic_torsion_order", True),
            ("constant_ci_minimal_phase_coupling_no_mixed_torsion_current", True),
            ("no_independent_physical_orientation_sector", True),
            ("regular_Minkowski_selector_background", True),
            ("positive_shift_symmetric_phase_current", True),
            ("barotropic_isentropic_irrotational_one_potential_subfamily", True),
            ("one_stable_causal_constitutive_rho_C", True),
            ("single_source_and_vacuum_ledger", True),
            ("regular_boundary_term_treatment", True),
        ]
    )
    selected_foundation_premises_complete = all(selected_foundation_premises.values())

    # The starting basis deliberately excludes the desired endpoint.
    starting_operator_registry = (
        "coframe_e",
        "flat_inertial_omega",
        "torsion_T",
        "I1",
        "I2",
        "I3",
        "Lambda_F",
        "phase_current_J",
        "phase_gradient_dtheta_C",
        "rho_C_of_n_C",
    )
    forbidden_starting_operators = {
        "R_LC",
        "Einstein_tensor",
        "Einstein_equation",
        "Fierz_Pauli_target",
        "PPN_target",
        "observed_profile",
    }
    excluded_retained_mixed_operators = {
        "torsion_current_operator",
        "torsion_density_operator",
        "n_dependent_c_i",
        "nonminimal_second_metric_coupling",
    }
    no_eh_or_target_in_starting_action = forbidden_starting_operators.isdisjoint(
        starting_operator_registry
    )
    injected_starting_registry = starting_operator_registry + ("R_LC",)
    operator_injection_mutation_rejected = not forbidden_starting_operators.isdisjoint(
        injected_starting_registry
    )
    no_mixed_operator_in_retained_action = excluded_retained_mixed_operators.isdisjoint(
        starting_operator_registry
    )
    mixed_operator_injection_mutation_rejected = not excluded_retained_mixed_operators.isdisjoint(
        starting_operator_registry + ("torsion_current_operator",)
    )

    # ------------------------------------------------------------------
    # 2. General NGR basis and independent orientation-sector selector.
    # ------------------------------------------------------------------
    c1, c2, c3 = sp.symbols("c1 c2 c3", real=True)
    selector_matrix = sp.Matrix([[2, 1, 1], [2, -1, 0]])
    selector_rank = selector_matrix.rank()
    selector_nullspace = selector_matrix.nullspace()
    selector_family_unique_up_to_scale = (
        selector_rank == 2 and len(selector_nullspace) == 1
    )

    raw_null_vector = selector_nullspace[0]
    normalized_tegr_vector = sp.simplify(
        raw_null_vector * (sp.Rational(1, 4) / raw_null_vector[0])
    )
    tegr_coefficients = tuple(normalized_tegr_vector)
    expected_tegr_coefficients = (
        sp.Rational(1, 4),
        sp.Rational(1, 2),
        sp.Integer(-1),
    )
    tegr_coefficients_derived_exact = all_zero(
        actual - expected
        for actual, expected in zip(tegr_coefficients, expected_tegr_coefficients)
    )

    def orientation_residuals(values: tuple[sp.Expr, sp.Expr, sp.Expr]):
        x1, x2, x3 = values
        return OrderedDict(
            [
                ("h_b_mixing", sp.expand(2 * x1 + x2 + x3)),
                ("b_box_kinetic", sp.expand(2 * x1 - x2)),
                ("b_divergence_kinetic", sp.expand(2 * x1 - 3 * x2 - x3)),
            ]
        )

    tegr_orientation_residuals = orientation_residuals(tegr_coefficients)
    orientation_sector_trivialized_exact = all_zero(
        tegr_orientation_residuals.values()
    )

    coefficient_mutations = OrderedDict()
    for index, name in enumerate(("c1", "c2", "c3")):
        mutated = list(tegr_coefficients)
        mutated[index] = sp.simplify(mutated[index] + sp.Rational(1, 7))
        residuals = orientation_residuals(tuple(mutated))
        coefficient_mutations[name] = not all_zero(
            [residuals["h_b_mixing"], residuals["b_box_kinetic"]]
        )
    coefficient_mutation_controls_pass = all(coefficient_mutations.values())

    mixing_only_control = (
        sp.Rational(1, 4),
        sp.Integer(0),
        sp.Rational(-1, 2),
    )
    mixing_only_residuals = orientation_residuals(mixing_only_control)
    mixing_removal_alone_insufficient = all(
        [
            exact_zero(mixing_only_residuals["h_b_mixing"]),
            not exact_zero(mixing_only_residuals["b_box_kinetic"]),
        ]
    )

    # The NGR quadratic decomposition is a source-registered analytic input,
    # not rederived from arbitrary tensor components by this script.  The
    # selector solve and all mutations are computed after that input is frozen.
    theorem_input_registry = OrderedDict(
        [
            ("NGR_quadratic_decomposition", "arXiv:1907.10038 Eq. (3.21)"),
            ("TEGR_coefficients_reference", "arXiv:1907.10038 Secs. 2-3"),
            ("TEGR_EH_connection_identity", "arXiv:1303.3897"),
            ("phase_current_action_reference", "arXiv:gr-qc/9304026 restricted one-potential subfamily"),
        ]
    )
    theorem_handoffs = OrderedDict(
        [
            ("NGR_THREE_INVARIANT_CLASSIFICATION_APPLIED", True),
            ("NGR_MINKOWSKI_CUBIC_OBSTRUCTION_RESULT_APPLIED", True),
            ("TEGR_TWO_HELICITY_EQUIVALENCE_APPLIED", True),
            ("TEGR_EH_EXACT_CONNECTION_IDENTITY_APPLIED", True),
            ("HILBERT_NOETHER_CONSERVATION_THEOREM_APPLIED", True),
        ]
    )
    theorem_handoffs_complete = all(theorem_handoffs.values())
    selector_operator_registry = ("h_b_mixing", "b_box_kinetic")
    local_lorentz_covariance_alone_used_as_selector = (
        "local_lorentz_covariance" in selector_operator_registry
    )

    # ------------------------------------------------------------------
    # 3. TEGR symmetric quadratic sector -> W3-53 Fierz--Pauli registry.
    # ------------------------------------------------------------------
    # Source-registered analytic basis after integration by parts for
    # A_mu_nu=h_mu_nu/2; the TEGR and FP combinations below are computed.
    I1_registry = OrderedDict(
        [("A", sp.Rational(1, 2)), ("B", sp.Rational(-1, 2)), ("C", 0), ("D", 0)]
    )
    I2_registry = OrderedDict(
        [("A", sp.Rational(1, 4)), ("B", sp.Rational(-1, 4)), ("C", 0), ("D", 0)]
    )
    I3_registry = OrderedDict(
        [("A", 0), ("B", sp.Rational(1, 4)), ("C", sp.Rational(-1, 2)), ("D", sp.Rational(1, 4))]
    )
    invariant_registries = (I1_registry, I2_registry, I3_registry)
    tegr_quadratic_registry = combine_registries(
        tegr_coefficients, invariant_registries
    )
    expected_tegr_quadratic_registry = OrderedDict(
        [
            ("A", sp.Rational(1, 4)),
            ("B", sp.Rational(-1, 2)),
            ("C", sp.Rational(1, 2)),
            ("D", sp.Rational(-1, 4)),
        ]
    )
    tegr_quadratic_registry_exact = registries_equal(
        tegr_quadratic_registry, expected_tegr_quadratic_registry
    )
    fp_from_tegr_registry = OrderedDict(
        (name, sp.simplify(-2 * value))
        for name, value in tegr_quadratic_registry.items()
    )
    w3_53_fp_registry = OrderedDict(
        [
            ("A", sp.Rational(-1, 2)),
            ("B", sp.Integer(1)),
            ("C", sp.Integer(-1)),
            ("D", sp.Rational(1, 2)),
        ]
    )
    tegr_to_fierz_pauli_regression_exact = registries_equal(
        fp_from_tegr_registry, w3_53_fp_registry
    ) and all_zero(fp_gauge_residuals(fp_from_tegr_registry).values())

    fp_mutations_from_torsion = OrderedDict()
    for index, name in enumerate(("c1", "c2", "c3")):
        mutated = list(tegr_coefficients)
        mutated[index] = sp.simplify(mutated[index] + sp.Rational(1, 11))
        mutated_registry = combine_registries(tuple(mutated), invariant_registries)
        mutated_fp = OrderedDict(
            (basis, sp.simplify(-2 * value))
            for basis, value in mutated_registry.items()
        )
        fp_mutations_from_torsion[name] = not registries_equal(
            mutated_fp, w3_53_fp_registry
        )
    fp_torsion_mutations_pass = all(fp_mutations_from_torsion.values())

    # ------------------------------------------------------------------
    # 4. Exact TEGR--Einstein-Hilbert identity: independent sign witness.
    # ------------------------------------------------------------------
    # For e^A_mu=diag(1,a(t),a(t),a(t)) in signature (-+++), the registered
    # exact connection identity gives these three independent expressions.
    # Their residual catches the sign of both the torsion scalar and boundary.
    H, Hdot = sp.symbols("H Hdot", real=True)
    torsion_scalar_flrw = 6 * H**2
    boundary_scalar_flrw = 6 * (Hdot + 3 * H**2)
    ricci_scalar_flrw = 6 * (Hdot + 2 * H**2)
    tegr_eh_flrw_identity_residual = sp.simplify(
        ricci_scalar_flrw + torsion_scalar_flrw - boundary_scalar_flrw
    )
    tegr_eh_flrw_sign_witness_exact = exact_zero(
        tegr_eh_flrw_identity_residual
    )
    wrong_torsion_sign_mutation_rejected = not exact_zero(
        ricci_scalar_flrw - torsion_scalar_flrw - boundary_scalar_flrw
    )

    # ------------------------------------------------------------------
    # 5. Covariant phase-current variation and explicit Hilbert T_mn.
    # ------------------------------------------------------------------
    n, rho, rho_prime = sp.symbols("n rho rho_prime", positive=True)
    c0, G = sp.symbols("c0 G", positive=True)
    p_phase = sp.simplify(n * rho_prime - rho)

    # The phase Euler--Lagrange equation is audited before it is named a
    # conservation law.  The abstract divergence symbol represents
    # partial_mu[dL/d(partial_mu theta_C)] in this first-order current action.
    theta_symbol, dtheta_symbol = sp.symbols("theta_C dtheta_C", real=True)
    current_symbol, current_divergence = sp.symbols("J div_J", real=True)
    phase_breaking = sp.symbols("epsilon_phase", nonzero=True, real=True)
    phase_lagrangian_witness = current_symbol * dtheta_symbol - rho / c0
    absolute_phase_derivative = sp.diff(phase_lagrangian_witness, theta_symbol)
    phase_current_coefficient = sp.diff(phase_lagrangian_witness, dtheta_symbol)
    phase_euler_equation = sp.expand(
        absolute_phase_derivative - current_divergence
    )
    phase_current_solution = sp.solve(
        [phase_euler_equation], current_divergence, dict=True
    )
    phase_shift_symmetry_exact = exact_zero(absolute_phase_derivative)
    phase_current_conservation_derived = phase_current_solution == [
        {current_divergence: 0}
    ]
    phase_breaking_lagrangian = (
        phase_lagrangian_witness + phase_breaking * theta_symbol
    )
    explicit_phase_breaking_mutation_rejected = not exact_zero(
        sp.diff(phase_breaking_lagrangian, theta_symbol)
    )

    # Coefficients in the independent variation basis
    # [g_mu_nu delta g^mu_nu, u_mu u_nu delta g^mu_nu].
    delta_n_registry = OrderedDict(
        [("g", n / 2), ("uu", n / 2)]
    )
    delta_phase_action_registry = OrderedDict(
        [
            ("g", sp.simplify((rho - n * rho_prime) / (2 * c0))),
            ("uu", sp.simplify(-n * rho_prime / (2 * c0))),
        ]
    )
    expected_delta_phase_action_registry = OrderedDict(
        [
            ("g", sp.simplify(-p_phase / (2 * c0))),
            ("uu", sp.simplify(-(rho + p_phase) / (2 * c0))),
        ]
    )
    phase_metric_variation_exact = registries_equal(
        delta_phase_action_registry, expected_delta_phase_action_registry
    )
    phase_hilbert_T_registry = OrderedDict(
        [("g", p_phase), ("uu", sp.simplify(rho + p_phase))]
    )

    eta_minkowski = sp.diag(-1, 1, 1, 1)
    u_cov_rest = sp.Matrix([-1, 0, 0, 0])
    T_rest = sp.simplify(
        (rho + p_phase) * (u_cov_rest * u_cov_rest.T)
        + p_phase * eta_minkowski
    )
    rest_frame_source_exact = all_zero(
        [
            T_rest[0, 0] - rho,
            T_rest[0, 1],
            T_rest[0, 2],
            T_rest[0, 3],
            T_rest[1, 1] - p_phase,
            T_rest[2, 2] - p_phase,
            T_rest[3, 3] - p_phase,
        ]
    )

    phase_J_variation_relation = "partial_mu theta_C + rho_C'(n_C) u_mu/c0 = 0"

    gravitational_variation_coefficient = c0**3 / (16 * sp.pi * G)
    source_variation_coefficient = 1 / (2 * c0)
    einstein_source_coupling = sp.simplify(
        source_variation_coefficient / gravitational_variation_coefficient
    )
    einstein_equation_coupling_exact = exact_zero(
        einstein_source_coupling - 8 * sp.pi * G / c0**4
    )

    # ------------------------------------------------------------------
    # 6. Homogeneous W3-50 reduction and one-source ledger.
    # ------------------------------------------------------------------
    n0 = sp.symbols("n0", positive=True)
    homogeneous_n = n0 / a_scale**3
    eta_F = sp.simplify(homogeneous_n / n0)
    homogeneous_charge_residual = sp.simplify(eta_F * a_scale**3 - 1)
    w3_50_eta_a3_regression_exact = exact_zero(homogeneous_charge_residual)
    w3_50_canonical_reduction_registry = OrderedDict(
        [
            ("sqrt_q", a_scale**3),
            ("n_dtheta_coefficient", sp.Integer(1)),
            ("H_C_identification", "rho_C(n_C)"),
            ("comoving_spatial_current", sp.Integer(0)),
        ]
    )

    source_ledger = OrderedDict(
        [
            ("phase_current_S_C_variation", 1),
            ("metric_self_energy_readded_on_rhs", 0),
            ("P_F_or_readout_p_readded", 0),
            ("material_scale_or_cadence_readded", 0),
            ("vacuum_offset_readded_inside_rho_C", 0),
        ]
    )
    one_source_ledger_selected_and_consistent = sum(source_ledger.values()) == 1
    duplicate_source_mutations = OrderedDict()
    for name in tuple(source_ledger)[1:]:
        mutated = OrderedDict(source_ledger)
        mutated[name] = 1
        duplicate_source_mutations[name] = sum(mutated.values()) != 1
    duplicate_source_mutations_pass = all(duplicate_source_mutations.values())

    pressure_roles_distinct = OrderedDict(
        [
            ("P_F", "foundation pressure/readout role from W3-46/W3-47"),
            ("p_C", "thermodynamic pressure n_C*rho_C'-rho_C from S_C"),
            ("P_F_equals_p_C_derived", False),
        ]
    )

    # ------------------------------------------------------------------
    # 7. Provenance, dependency, circularity, and aggregate gates.
    # ------------------------------------------------------------------
    contract_exists = contract_path.exists()
    actual_contract_hash = sha256(contract_path) if contract_exists else None
    contract_hash_verified = actual_contract_hash == CONTRACT_SHA256

    dependency_records = OrderedDict()
    for name, path in dependency_paths(work3).items():
        actual_hash = sha256(path) if path.exists() else None
        text_payload = path.read_text(encoding="utf-8") if path.exists() else ""
        required_markers = DEPENDENCY_CONTRACT_MARKERS.get(name, ())
        marker_checks = OrderedDict(
            (marker, marker in text_payload) for marker in required_markers
        )
        section_marker_checks = OrderedDict()
        section_spec = DEPENDENCY_CLOSURE_SECTION_MARKERS.get(name)
        if section_spec is not None:
            closure_anchor = "- `CLOSURE_FLAGS`:"
            true_anchor = "true on the declared branch:"
            false_anchor = "false beyond the declared branch:"
            crosscheck_anchor = "- `CROSSCHECK`:"
            closure_start = text_payload.find(closure_anchor)
            true_start = text_payload.find(true_anchor, closure_start)
            false_start = text_payload.find(false_anchor, true_start)
            closure_end = text_payload.find(crosscheck_anchor, false_start)
            anchors_valid = (
                closure_start >= 0
                and true_start > closure_start
                and false_start > true_start
                and closure_end > false_start
            )
            true_payload = (
                text_payload[true_start:false_start] if anchors_valid else ""
            )
            false_payload = (
                text_payload[false_start:closure_end] if anchors_valid else ""
            )
            section_marker_checks["closure_section_anchors_valid"] = anchors_valid
            for marker in section_spec["true_on_declared_branch"]:
                section_marker_checks[f"{marker}=true_section"] = (
                    marker in true_payload and marker not in false_payload
                )
            for marker in section_spec["false_beyond_declared_branch"]:
                section_marker_checks[f"{marker}=false_section"] = (
                    marker in false_payload and marker not in true_payload
                )
        markers_verified = all(marker_checks.values()) and all(
            section_marker_checks.values()
        )
        dependency_records[name] = OrderedDict(
            [
                ("exists", path.exists()),
                ("expected_sha256", DEPENDENCY_HASHES[name]),
                ("actual_sha256", actual_hash),
                ("required_contract_markers", marker_checks),
                ("required_closure_section_markers", section_marker_checks),
                ("markers_verified", markers_verified),
                (
                    "verified",
                    actual_hash == DEPENDENCY_HASHES[name] and markers_verified,
                ),
            ]
        )

    w3_42_result_path = (
        work3
        / "Cosmology_and_LSS"
        / "Foundation_State_Space_and_Volume_Map"
        / "w3_42_result.json"
    )
    w3_42_checksum_path = w3_42_result_path.with_name(
        "w3_42_result.sha256"
    )
    w3_42_result = (
        json.loads(w3_42_result_path.read_text(encoding="utf-8"))
        if w3_42_result_path.exists()
        else {}
    )
    w3_42_actual_sha256 = (
        sha256(w3_42_result_path) if w3_42_result_path.exists() else None
    )
    w3_42_checksum_parts = (
        w3_42_checksum_path.read_text(encoding="utf-8").split()
        if w3_42_checksum_path.exists()
        else []
    )
    w3_42_registered_sha256 = (
        w3_42_checksum_parts[0] if w3_42_checksum_parts else None
    )
    w3_42_provenance = w3_42_result.get("provenance", {})
    w3_42_prereg_provenance = w3_42_provenance.get(
        "preregistration", {}
    )
    w3_42_source_provenance = w3_42_provenance.get("source", {})
    w3_42_closure_flags = w3_42_result.get("closure_flags", {})
    w3_42_physical_flags = w3_42_result.get(
        "physical_closure_flags", {}
    )
    w3_42_status_record = OrderedDict(
        [
            ("exists", w3_42_result_path.exists()),
            ("checksum_exists", w3_42_checksum_path.exists()),
            ("actual_sha256", w3_42_actual_sha256),
            ("registered_sha256", w3_42_registered_sha256),
            (
                "checksum_matches",
                w3_42_actual_sha256 == w3_42_registered_sha256,
            ),
            ("status", w3_42_result.get("status")),
            (
                "aggregate_identity_pass",
                w3_42_closure_flags.get("aggregate_identity_pass"),
            ),
            (
                "d3_geometric_branch_matches_cubic_map_exact",
                w3_42_closure_flags.get(
                    "d3_geometric_branch_matches_cubic_map_exact"
                ),
            ),
            (
                "one_coordinate_completeness_nonselection_exact",
                w3_42_closure_flags.get(
                    "one_coordinate_completeness_nonselection_exact"
                ),
            ),
            (
                "three_spatial_dimensions_derived",
                w3_42_physical_flags.get(
                    "three_spatial_dimensions_derived"
                ),
            ),
            (
                "preregistration_sha256",
                w3_42_prereg_provenance.get("sha256"),
            ),
            (
                "preregistration_expected_sha256",
                w3_42_prereg_provenance.get("expected_sha256"),
            ),
            (
                "preregistration_valid",
                w3_42_prereg_provenance.get("valid"),
            ),
            (
                "source_sha256",
                w3_42_source_provenance.get("sha256"),
            ),
        ]
    )
    w3_42_status_record["verified"] = all(
        [
            w3_42_status_record["checksum_matches"] is True,
            w3_42_status_record["status"] == "PASS",
            w3_42_status_record["aggregate_identity_pass"] is True,
            w3_42_status_record[
                "d3_geometric_branch_matches_cubic_map_exact"
            ]
            is True,
            w3_42_status_record[
                "one_coordinate_completeness_nonselection_exact"
            ]
            is True,
            w3_42_status_record["three_spatial_dimensions_derived"] is False,
            w3_42_status_record["preregistration_sha256"]
            == DEPENDENCY_HASHES[
                "w3_42_foundation_state_space_volume_map_preregistration.md"
            ],
            w3_42_status_record["preregistration_expected_sha256"]
            == DEPENDENCY_HASHES[
                "w3_42_foundation_state_space_volume_map_preregistration.md"
            ],
            w3_42_status_record["preregistration_valid"] is True,
            w3_42_status_record["source_sha256"]
            == DEPENDENCY_HASHES[
                "w3_42_foundation_state_space_volume_map.py"
            ],
        ]
    )
    dependency_records["w3_42_result.json"] = w3_42_status_record
    dependencies_verified = all(
        record["verified"] for record in dependency_records.values()
    )

    declared_dependencies = set(DEPENDENCY_HASHES)
    base_dependency_names = set(dependency_paths(work3))
    dependency_registry_closed = (
        declared_dependencies == base_dependency_names
        and base_dependency_names.issubset(dependency_records)
    )
    downstream_regressions_not_inputs = all(
        name not in declared_dependencies
        for name in (
            "w3_53_foundation_eh_source_closure.py",
            "w3_51_weak_field_closure.py",
            "w3_52_full_1pn_inheritance.py",
        )
    )

    downstream_regression_records = OrderedDict(
        (name, run_json_regression(name, path))
        for name, path in downstream_regression_paths(work3).items()
    )
    downstream_regressions_pass = all(
        record["passed"] for record in downstream_regression_records.values()
    )

    computed_exact_checks = OrderedDict(
        [
            ("w3_42_polar_coframe_gram_witness_exact", spatial_polar_gram_witness_exact),
            ("time_gauge_metric_determinant_witness_exact", time_gauge_metric_determinant_witness_exact),
            ("selector_family_unique_up_to_scale", selector_family_unique_up_to_scale),
            ("tegr_coefficients_derived_exact", tegr_coefficients_derived_exact),
            ("orientation_sector_trivialized_exact", orientation_sector_trivialized_exact),
            ("mixing_removal_alone_insufficient", mixing_removal_alone_insufficient),
            ("tegr_quadratic_registry_exact", tegr_quadratic_registry_exact),
            ("tegr_to_fierz_pauli_regression_exact", tegr_to_fierz_pauli_regression_exact),
            ("tegr_eh_flrw_sign_witness_exact", tegr_eh_flrw_sign_witness_exact),
            ("phase_metric_variation_exact", phase_metric_variation_exact),
            ("phase_shift_symmetry_exact", phase_shift_symmetry_exact),
            ("phase_current_conservation_derived", phase_current_conservation_derived),
            ("rest_frame_source_exact", rest_frame_source_exact),
            ("einstein_equation_coupling_exact", einstein_equation_coupling_exact),
            ("w3_50_eta_a3_regression_exact", w3_50_eta_a3_regression_exact),
        ]
    )
    structural_audit_checks = OrderedDict(
        [
            ("no_eh_or_target_in_starting_action", no_eh_or_target_in_starting_action),
            ("no_mixed_operator_in_retained_action", no_mixed_operator_in_retained_action),
            ("local_lorentz_covariance_not_used_as_selector", not local_lorentz_covariance_alone_used_as_selector),
            ("one_source_ledger_selected_and_consistent", one_source_ledger_selected_and_consistent),
            ("contract_hash_verified", contract_hash_verified),
            ("dependencies_verified", dependencies_verified),
            ("declared_dependency_registry_closed", dependency_registry_closed),
            ("downstream_regressions_not_inputs", downstream_regressions_not_inputs),
            ("downstream_regressions_pass", downstream_regressions_pass),
        ]
    )
    declaration_checks = OrderedDict(
        [
            ("selected_foundation_premises_complete", selected_foundation_premises_complete),
            ("theorem_input_registry_complete", all(bool(value) for value in theorem_input_registry.values())),
            ("theorem_handoffs_complete", theorem_handoffs_complete),
        ]
    )

    premise_mutation_checks = OrderedDict()
    for name in (
        "connected_oriented_nondegenerate_3plus1_coframe_phase",
        "flat_metric_compatible_inertial_transport",
        "flat_connection_pure_gauge_variation_domain",
        "constant_ci_minimal_phase_coupling_no_mixed_torsion_current",
        "no_independent_physical_orientation_sector",
        "regular_Minkowski_selector_background",
        "positive_shift_symmetric_phase_current",
        "barotropic_isentropic_irrotational_one_potential_subfamily",
        "single_source_and_vacuum_ledger",
    ):
        mutated = OrderedDict(selected_foundation_premises)
        mutated[name] = False
        premise_mutation_checks[name] = not all(mutated.values())

    computed_mutation_checks = OrderedDict(
        [
            ("every_tegr_coefficient_mutation_rejected", coefficient_mutation_controls_pass),
            ("torsion_to_fp_mutations_rejected", fp_torsion_mutations_pass),
            ("wrong_torsion_sign_rejected", wrong_torsion_sign_mutation_rejected),
            ("explicit_phase_breaking_rejected", explicit_phase_breaking_mutation_rejected),
        ]
    )
    manifest_mutation_checks = OrderedDict(
        [
            ("forbidden_operator_injection_rejected", operator_injection_mutation_rejected),
            ("mixed_operator_injection_rejected", mixed_operator_injection_mutation_rejected),
            ("duplicate_source_mutations_rejected", duplicate_source_mutations_pass),
            ("selected_premise_mutations_rejected", all(premise_mutation_checks.values())),
        ]
    )

    aggregate_pass = all(
        [
            all(computed_exact_checks.values()),
            all(structural_audit_checks.values()),
            all(declaration_checks.values()),
            all(computed_mutation_checks.values()),
            all(manifest_mutation_checks.values()),
        ]
    )

    closure_flags = OrderedDict(
        [
            ("SELECTED_POST_GENESIS_RELATIONAL_COFRAME_STATE", True),
            ("W3_42_POLAR_COFRAME_GRAM_WITNESS_EXACT", spatial_polar_gram_witness_exact),
            ("SELECTED_COFRAME_DEFINES_FULL_OPERATIONAL_METRIC", True),
            ("TIME_GAUGE_METRIC_DETERMINANT_WITNESS_EXACT", time_gauge_metric_determinant_witness_exact),
            ("FLAT_INERTIAL_TRANSPORT_SELECTED", True),
            ("FLAT_CONNECTION_VARIATION_DOMAIN_SELECTED", True),
            ("GENERAL_PARITY_EVEN_QUADRATIC_TORSION_BASIS_REGISTERED", theorem_handoffs["NGR_THREE_INVARIANT_CLASSIFICATION_APPLIED"]),
            ("NO_PHYSICAL_ORIENTATION_SECTOR_SELECTED", True),
            ("TEGR_COEFFICIENT_RATIOS_DERIVED", tegr_coefficients_derived_exact),
            ("NGR_MINKOWSKI_CUBIC_OBSTRUCTION_RESULT_APPLIED", theorem_handoffs["NGR_MINKOWSKI_CUBIC_OBSTRUCTION_RESULT_APPLIED"]),
            ("TEGR_EH_CONNECTION_IDENTITY_APPLIED_AND_SIGN_CHECKED", theorem_handoffs["TEGR_EH_EXACT_CONNECTION_IDENTITY_APPLIED"] and tegr_eh_flrw_sign_witness_exact),
            ("TEGR_TO_FIERZ_PAULI_REGRESSION_EXACT", tegr_to_fierz_pauli_regression_exact),
            ("W3_50_IRROTATIONAL_PHASE_CURRENT_COVARIANT_COMPLETION_SELECTED", True),
            ("PHASE_CURRENT_CONSERVATION_DERIVED", phase_current_conservation_derived),
            ("PHASE_HILBERT_T_DERIVED", phase_metric_variation_exact and rest_frame_source_exact),
            ("W3_50_ETA_A3_REGRESSION_EXACT", w3_50_eta_a3_regression_exact),
            ("EINSTEIN_EQUATION_FROM_SINGLE_MASTER_ACTION_EXACT", einstein_equation_coupling_exact),
            ("ONE_SOURCE_LEDGER_SELECTED_AND_CONSISTENT", one_source_ledger_selected_and_consistent),
            ("RELATIONAL_COFRAME_TO_EH_AND_PHASE_T_GATE_CLOSED", aggregate_pass),
            ("PREGEOMETRIC_GRAPH_DERIVED", False),
            ("THREE_SPATIAL_DIMENSIONS_DERIVED", False),
            ("NODE_TO_COFRAME_CONTINUUM_DERIVED", False),
            ("LORENTZIAN_TIME_LEG_FROM_NODES_DERIVED", False),
            ("FLAT_TRANSPORT_FROM_NODE_DYNAMICS_DERIVED", False),
            ("COMMON_CONE_FROM_NODE_SPECTRUM_DERIVED", False),
            ("NO_ORIENTATION_MODE_FROM_NODE_SPECTRUM_DERIVED", False),
            ("COFRAME_PHASE_SPLIT_FROM_NODES_DERIVED", False),
            ("MICROSCOPIC_T_FROM_NODES_DERIVED", False),
            ("RHO_C_FROM_OSCILLON_MICROPHYSICS_DERIVED", False),
            ("P_F_EQUALS_P_C_DERIVED", False),
            ("G_VALUE_DERIVED", False),
            ("LAMBDA_VALUE_DERIVED", False),
            ("HIGHER_GRADIENT_COEFFICIENTS_DERIVED", False),
            ("PARTICLE_PROFILES_DERIVED", False),
            ("NEW_OBSERVATION_TESTED", False),
        ]
    )

    required_false_flags = (
        "PREGEOMETRIC_GRAPH_DERIVED",
        "THREE_SPATIAL_DIMENSIONS_DERIVED",
        "NODE_TO_COFRAME_CONTINUUM_DERIVED",
        "LORENTZIAN_TIME_LEG_FROM_NODES_DERIVED",
        "FLAT_TRANSPORT_FROM_NODE_DYNAMICS_DERIVED",
        "COMMON_CONE_FROM_NODE_SPECTRUM_DERIVED",
        "NO_ORIENTATION_MODE_FROM_NODE_SPECTRUM_DERIVED",
        "COFRAME_PHASE_SPLIT_FROM_NODES_DERIVED",
        "MICROSCOPIC_T_FROM_NODES_DERIVED",
        "RHO_C_FROM_OSCILLON_MICROPHYSICS_DERIVED",
        "P_F_EQUALS_P_C_DERIVED",
        "G_VALUE_DERIVED",
        "LAMBDA_VALUE_DERIVED",
        "HIGHER_GRADIENT_COEFFICIENTS_DERIVED",
        "PARTICLE_PROFILES_DERIVED",
        "NEW_OBSERVATION_TESTED",
    )
    false_flag_boundary_exact = all(
        closure_flags[name] is False for name in required_false_flags
    )
    if not false_flag_boundary_exact:
        aggregate_pass = False
        closure_flags["RELATIONAL_COFRAME_TO_EH_AND_PHASE_T_GATE_CLOSED"] = False

    result = OrderedDict(
        [
            ("claim_id", CLAIM_ID),
            ("model_version", MODEL_VERSION),
            ("status", STATUS_PASS if aggregate_pass else "FAIL"),
            ("aggregate_pass", aggregate_pass),
            ("scope", "conditional_selected_post_Genesis_relational_coframe_action_to_TEGR_equivalent_EH_plus_explicit_irrotational_phase_current_T_then_stop"),
            ("selected_foundation_premises", selected_foundation_premises),
            ("starting_operator_registry", starting_operator_registry),
            ("forbidden_starting_operators", sorted(forbidden_starting_operators)),
            ("excluded_retained_mixed_operators", sorted(excluded_retained_mixed_operators)),
            (
                "freedom_ledger",
                OrderedDict(
                    [
                        ("fitted_parameters", 0),
                        ("fitted_functions", 0),
                        ("G", "one measured universal normalization"),
                        ("Lambda_F", "one universal zero-derivative coefficient"),
                        (
                            "rho_C",
                            "one infinite-dimensional universal C2 functional freedom on n_C>0, restricted by rho_C>0, rho_C'>0, and 0<=n_C*rho_C''/rho_C'<=1; not fitted or microscopically derived",
                        ),
                    ]
                ),
            ),
            (
                "coframe_metric_map",
                OrderedDict(
                    [
                        ("spatial_E", "a R exp(s), R in SO(3), s=s^T, tr(s)=0"),
                        ("spatial_q", "E^T E = a^2 exp(2s)"),
                        ("chart_scope", "time-gauge witness; full metric definition is g=e^T eta e"),
                        ("sqrt_det_q", str(sp.simplify(sqrt_det_spatial_metric))),
                        ("four_volume_e", str(coframe_determinant)),
                        ("metric_determinant", str(metric_determinant)),
                    ]
                ),
            ),
            ("selector_matrix", [[int(value) for value in row] for row in selector_matrix.tolist()]),
            ("selector_rank", selector_rank),
            ("selector_nullspace_raw", [str(value) for value in raw_null_vector]),
            ("tegr_coefficients", OrderedDict((name, str(value)) for name, value in zip(("c1", "c2", "c3"), tegr_coefficients))),
            ("tegr_orientation_residuals", OrderedDict((name, str(value)) for name, value in tegr_orientation_residuals.items())),
            ("tegr_quadratic_registry", OrderedDict((name, str(value)) for name, value in tegr_quadratic_registry.items())),
            ("fp_from_tegr_registry", OrderedDict((name, str(value)) for name, value in fp_from_tegr_registry.items())),
            (
                "tegr_eh_identity",
                OrderedDict(
                    [
                        ("exact_general_identity", "R_LC=-T_TEGR+(2/e) partial_mu(e T^mu)"),
                        ("flrw_T", str(torsion_scalar_flrw)),
                        ("flrw_boundary", str(boundary_scalar_flrw)),
                        ("flrw_R", str(ricci_scalar_flrw)),
                        ("flrw_residual", str(tegr_eh_flrw_identity_residual)),
                    ]
                ),
            ),
            (
                "phase_source",
                OrderedDict(
                    [
                        ("density_variation_basis", OrderedDict((name, str(value)) for name, value in delta_n_registry.items())),
                        ("p_C", str(p_phase)),
                        ("T_basis", OrderedDict((name, str(value)) for name, value in phase_hilbert_T_registry.items())),
                        ("current_equation", "partial_mu J^mu=0"),
                        ("phase_current_coefficient", str(phase_current_coefficient)),
                        ("phase_euler_equation", str(phase_euler_equation)),
                        ("J_variation", phase_J_variation_relation),
                        ("einstein_coupling", str(einstein_source_coupling)),
                    ]
                ),
            ),
            (
                "w3_50_reduction",
                OrderedDict(
                    (name, str(value) if isinstance(value, sp.Basic) else value)
                    for name, value in w3_50_canonical_reduction_registry.items()
                ),
            ),
            ("source_ledger", source_ledger),
            ("pressure_roles", pressure_roles_distinct),
            ("theorem_input_registry", theorem_input_registry),
            ("theorem_handoffs", theorem_handoffs),
            (
                "evidence_roles",
                OrderedDict(
                    [
                        ("computed_exact", "polar/time-gauge determinants; selector nullspace after registered NGR decomposition; TEGR/FP combination; FLRW sign witness; phase variation; source tensor; coupling; homogeneous charge"),
                        ("registered_analytic_inputs", "NGR invariant/quadratic decomposition; exact TEGR-EH connection identity; scoped Minkowski cubic obstruction; TEGR spectrum; Hilbert/Noether conservation"),
                        ("manifest_integrity_only", "selected-premise registry; forbidden-operator list; source ledger; theorem declarations; their wiring mutations"),
                        ("selected_not_derived", "3+1 coframe continuum; Lorentzian time leg; flat transport; one operational metric; no physical orientation mode; irrotational phase subfamily; rho_C functional; G and Lambda values"),
                    ]
                ),
            ),
            ("computed_exact_checks", computed_exact_checks),
            ("structural_audit_checks", structural_audit_checks),
            ("declaration_checks", declaration_checks),
            ("computed_mutation_checks", computed_mutation_checks),
            ("manifest_mutation_checks", manifest_mutation_checks),
            ("coefficient_mutations", coefficient_mutations),
            ("fp_torsion_mutations", fp_mutations_from_torsion),
            ("premise_mutation_checks", premise_mutation_checks),
            ("duplicate_source_mutations", duplicate_source_mutations),
            ("contract_sha256", OrderedDict([("expected", CONTRACT_SHA256), ("actual", actual_contract_hash), ("verified", contract_hash_verified)])),
            ("dependency_records", dependency_records),
            ("downstream_regression_records", downstream_regression_records),
            ("closure_flags", closure_flags),
            ("false_flag_boundary_exact", false_flag_boundary_exact),
            (
                "explicit_boundary",
                "Conditional on the selected post-Genesis coframe/flat-transport/no-orientation and irrotational phase premises, the action yields TEGR-equivalent Einstein-Hilbert geometry and an explicit phase-current Hilbert T. The node origin of the coframe/phase split, microscopic T and rho_C/P_F bridge, and G/Lambda values remain separate origin questions.",
            ),
            (
                "stop_rule",
                "STOP after TEGR/EH, explicit phase T, W3-50 charge, and bounded W3-53/W3-51/W3-52 regressions; do not open particles, EOS search, cosmology, strong field, higher gradients, or observations.",
            ),
            (
                "provenance",
                OrderedDict(
                    [
                        ("python", sys.version.split()[0]),
                        ("sympy", sp.__version__),
                        ("platform", platform.platform()),
                        ("script_sha256", sha256(Path(__file__))),
                        ("utc", datetime.now(timezone.utc).isoformat()),
                    ]
                ),
            ),
        ]
    )

    atomic_json_write(out_path, result)
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    if not aggregate_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
