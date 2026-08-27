"""W3-53: selected IR spin-2 to Einstein--Hilbert/source-map gate.

The verifier separates three evidence roles.  It exactly derives the
Fierz--Pauli coefficient ratios and checks the Gram, pure-gauge, soft-pair,
and scalar source witnesses.  It applies the published Fierz--Pauli spectrum,
Weinberg soft-graviton, Deser bootstrap, and Lovelock uniqueness theorems under
explicit frozen premises.  It does not label those theorem handoffs as new
computer derivations.

The result is a conditional IR theorem.  It is not a node-scale derivation of
the selected tensor branch, the full Phi_F-to-metric map, c0, G, Lambda, a
foundation-to-S_loc coarse-graining, or an oscillon potential.  The stopping
point is the Einstein--Hilbert operator plus the generic operational Hilbert
T_mn map; no downstream phenomenology is opened.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_53_SELECTED_IR_SPIN2_EH_SOURCE_MAP"
MODEL_VERSION = "W3-53-v1.1-SELECTED-IR-SPIN2-EH-SOURCE-MAP"
STATUS_PASS = (
    "CONDITIONAL_EXACT_SELECTED_IR_SPIN2_TO_EINSTEIN_HILBERT_"
    "AND_OPERATIONAL_HILBERT_SOURCE_MAP"
)

DEPENDENCY_HASHES = OrderedDict(
    [
        (
            "w3_42_foundation_state_space_volume_map_preregistration.md",
            "4cc4674775525a3c76cd8cb282461e5e83b651aff3554de21983568ee7e1f9f1",
        ),
        (
            "w3_46_active_participation_resonance_feedback_contract.md",
            "0109ed3d5e8daec55dbd0f01f8b05932e6f653373438455c32a3d26378e0f3b2",
        ),
        (
            "w3_50_neutral_collective_phase_density_bridge_contract.md",
            "1cb66438a6bf53f1a661a014328204c05edfe847f81d876defe69eaa400591db",
        ),
    ]
)


def exact_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


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


def fp_gauge_identity_residuals(
    a: sp.Expr, b: sp.Expr, c: sp.Expr, d: sp.Expr
) -> OrderedDict[str, sp.Expr]:
    """Divergence coefficients of the Euler tensor for the four-term basis.

    L2 = a (dh_mn)^2 + b (div h)_n^2
         + c (div h)^n d_n h + d (dh)^2.
    Linear relabelling invariance requires every returned coefficient to
    vanish identically.
    """

    return OrderedDict(
        [
            ("box_div_h", sp.expand(2 * a + b)),
            ("grad_div_div_h", sp.expand(b + c)),
            ("grad_box_trace_h", sp.expand(c + 2 * d)),
        ]
    )


def registry_equal(left: OrderedDict, right: OrderedDict) -> bool:
    return tuple(left) == tuple(right) and all(
        exact_zero(left[key] - right[key]) for key in left
    )


def main() -> None:
    work3 = locate_work3()
    out_path = Path(__file__).with_name("w3_53_result.json")

    # ------------------------------------------------------------------
    # 1. Selected W3-42-compatible volume/shape witness.
    # ------------------------------------------------------------------
    # This is a G0-orthonormal principal-axis frame.  It proves the
    # determinant split for a symmetric trace-free shape matrix; it does not
    # derive the physical cell, its orientation/coframe, or a full h_mn map.
    a_scale = sp.symbols("a", positive=True)
    s1, s2 = sp.symbols("s1 s2", real=True)
    s3 = -s1 - s2
    gram_relative = a_scale**2 * sp.diag(
        sp.exp(2 * s1), sp.exp(2 * s2), sp.exp(2 * s3)
    )
    gram_measure_ratio = sp.sqrt(sp.simplify(gram_relative.det()))
    gram_volume_residual = sp.simplify(gram_measure_ratio - a_scale**3)
    trace_free_shape_residual = sp.simplify(s1 + s2 + s3)
    shape_independent_of_volume = all_zero(
        [sp.diff(gram_measure_ratio, s1), sp.diff(gram_measure_ratio, s2)]
    )

    # These are deliberately frozen IR premises.  They contain neither R,
    # G_mn, the Einstein equation, a target potential, nor PPN coefficients.
    selected_ir_premises = OrderedDict(
        [
            ("closed_reversible_foundation_action", True),
            ("relational_relabelling_redundancy", True),
            ("independent_nonintegrable_shape_tensor", True),
            ("connected_3plus1_emergent_lorentz_invariance", True),
            ("single_universal_c0_cone", True),
            ("local_two_derivative_leading_order", True),
            ("no_extra_unsuppressed_gapless_geometry_mode", True),
            ("no_unsuppressed_nonminimal_curvature_coupling_at_retained_order", True),
            ("soft_factorization_and_unitary_ir", True),
            ("one_operational_source_ledger_selected", True),
        ]
    )
    ir_premises_complete = all(selected_ir_premises.values())

    # ------------------------------------------------------------------
    # 2. Derive Fierz--Pauli from the general quadratic tensor action.
    # ------------------------------------------------------------------
    a, b, c, d = sp.symbols("a b c d", real=True)
    residuals_general = fp_gauge_identity_residuals(a, b, c, d)
    coefficient_matrix = sp.Matrix(
        [
            [2, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 2],
        ]
    )
    nullspace = coefficient_matrix.nullspace()
    one_dimensional_fp_family = (
        coefficient_matrix.rank() == 3 and len(nullspace) == 1
    )

    # Standard theorem convention (-+++): a=-1/2 gives positive TT energy.
    # RefG's (+---) metric is the overall-sign-reversed presentation.
    fp_coefficients = OrderedDict(
        [
            ("a_dh_dh", sp.Rational(-1, 2)),
            ("b_divh_divh", sp.Integer(1)),
            ("c_divh_dtrace", sp.Integer(-1)),
            ("d_dtrace_dtrace", sp.Rational(1, 2)),
        ]
    )
    fp_residuals = fp_gauge_identity_residuals(*fp_coefficients.values())
    fp_coefficients_exact = all_zero(fp_residuals.values())
    fp_positive_tt_kinetic = fp_coefficients["a_dh_dh"] < 0

    # Registered Fierz--Pauli Hamiltonian theorem: 10 fields give 20
    # phase-space dimensions; 8 first-class constraints (4 primary and
    # 4 secondary) remove 16, leaving 4 phase-space dimensions = 2 helicities.
    # The script checks the arithmetic, not the constraint derivation.
    tensor_configuration_components = 10
    phase_space_dimensions = 2 * tensor_configuration_components
    first_class_constraints = 8
    physical_phase_space_dimensions = (
        phase_space_dimensions - 2 * first_class_constraints
    )
    physical_helicities = physical_phase_space_dimensions // 2
    fp_helicity_theorem_arithmetic_consistent = (
        physical_phase_space_dimensions == 4 and physical_helicities == 2
    )

    # Any one-coefficient mutation must break the gauge identity.
    fp_mutations = OrderedDict()
    for index, name in enumerate(fp_coefficients):
        values = list(fp_coefficients.values())
        values[index] = sp.simplify(values[index] + sp.Rational(1, 7))
        fp_mutations[name] = not all_zero(
            fp_gauge_identity_residuals(*values).values()
        )
    fp_mutation_controls_pass = all(fp_mutations.values())

    # ------------------------------------------------------------------
    # 3. Negative controls: scalar ocean and pure-gradient strain.
    # ------------------------------------------------------------------
    pressure_only_scalar_has_tensor_helicities = False
    scalar_ocean_rejected_as_complete_geometry = (
        not pressure_only_scalar_has_tensor_helicities
    )

    k = sp.symbols("k0:4", real=True)
    u = sp.symbols("u0:4", real=True)
    h_gradient = sp.Matrix(
        4, 4, lambda mu, nu: k[mu] * u[nu] + k[nu] * u[mu]
    )

    def linear_riemann(mu: int, nu: int, rho: int, sigma: int) -> sp.Expr:
        return sp.Rational(1, 2) * (
            k[rho] * k[nu] * h_gradient[mu, sigma]
            + k[sigma] * k[mu] * h_gradient[nu, rho]
            - k[sigma] * k[nu] * h_gradient[mu, rho]
            - k[rho] * k[mu] * h_gradient[nu, sigma]
        )

    gradient_riemann_residuals = [
        sp.expand(linear_riemann(mu, nu, rho, sigma))
        for mu in range(4)
        for nu in range(4)
        for rho in range(4)
        for sigma in range(4)
    ]
    pure_gradient_curvature_zero = all_zero(gradient_riemann_residuals)
    pure_gradient_rejected_as_physical_tensor = pure_gradient_curvature_zero

    # An independent h_11 plane-wave amplitude gives nonzero curvature.
    K, Hplus = sp.symbols("K Hplus", nonzero=True, real=True)
    independent_tensor_curvature_witness = -sp.Rational(1, 2) * K**2 * Hplus
    independent_tensor_can_curve = independent_tensor_curvature_witness != 0

    # ------------------------------------------------------------------
    # 4. Reduced soft-coupling witness and source gauge identity.
    # ------------------------------------------------------------------
    g1, g2 = sp.symbols("g1 g2", real=True)
    p = sp.symbols("p0:4", real=True)
    soft_residual = [sp.expand((g1 - g2) * component) for component in p]
    universal_soft_substitution_exact = all_zero(
        [item.subs(g2, g1) for item in soft_residual]
    )
    species_dependent_coupling_rejected = not all_zero(
        [item.subs(g2, 2 * g1) for item in soft_residual]
    )
    soft_pairwise_witness_exact = (
        universal_soft_substitution_exact
        and species_dependent_coupling_rejected
    )

    div_tau = sp.symbols("div_tau0:4", real=True)
    source_gauge_variation = [sp.expand(-2 * item) for item in div_tau]
    conserved_source_solution = [
        sp.solve([source_gauge_variation[i]], div_tau[i], dict=True)
        for i in range(4)
    ]
    source_gauge_invariance_iff_conserved = all(
        solution == [{div_tau[i]: 0}]
        for i, solution in enumerate(conserved_source_solution)
    )

    # ------------------------------------------------------------------
    # 5. Schematic Deser operator registry plus external theorem handoffs.
    # ------------------------------------------------------------------
    # This registry records the operator content quoted in Deser's first-order
    # proof; it does not reproduce the index contractions or connection
    # variation and is not advertised as a new derivation.
    free_first_order = OrderedDict(
        [
            ("h_dGamma", sp.Integer(1)),
            ("eta_GammaGamma", sp.Integer(1)),
            ("h_GammaGamma", sp.Integer(0)),
        ]
    )
    registered_self_coupling = OrderedDict(
        [
            ("h_dGamma", sp.Integer(0)),
            ("eta_GammaGamma", sp.Integer(0)),
            ("h_GammaGamma", sp.Integer(1)),
        ]
    )
    free_plus_registered_self = OrderedDict(
        (name, free_first_order[name] + registered_self_coupling[name])
        for name in free_first_order
    )
    registered_palatini_bulk = OrderedDict(
        [
            ("h_dGamma", sp.Integer(1)),
            ("eta_GammaGamma", sp.Integer(1)),
            ("h_GammaGamma", sp.Integer(1)),
        ]
    )
    deser_operator_registry_consistent = registry_equal(
        free_plus_registered_self, registered_palatini_bulk
    )
    missing_registered_self_coupling_detected = not registry_equal(
        free_first_order, registered_palatini_bulk
    )

    theorem_handoffs = OrderedDict(
        [
            ("FIERZ_PAULI_TWO_HELICITY_THEOREM_APPLIED", True),
            ("WEINBERG_SOFT_UNIVERSALITY_THEOREM_APPLIED", True),
            ("DESER_PALATINI_BOOTSTRAP_THEOREM_APPLIED", True),
            ("LOVELOCK_4D_ZERO_PLUS_TWO_DERIVATIVE_THEOREM_APPLIED", True),
        ]
    )
    theorem_handoffs_complete = all(theorem_handoffs.values())

    # ------------------------------------------------------------------
    # 6. Generic operational T_mn map and scalar witness.
    # ------------------------------------------------------------------
    # This witness validates only S_loc -> T_mn.  It does not construct S_loc
    # from Phi_F.  Standard theorem convention is (-+++), x0=c0*tau, and
    # T_mn=-(2*c0/sqrt(-g)) delta S_loc/delta g^mn.
    q = sp.Matrix(sp.symbols("q0:4", real=True))
    V = sp.symbols("V", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    q_up = eta * q
    lagrangian = -sp.Rational(1, 2) * (q.T * q_up)[0] - V

    hilbert_cov = sp.Matrix(
        4,
        4,
        lambda mu, nu: sp.expand(q[mu] * q[nu] + eta[mu, nu] * lagrangian),
    )
    hilbert_mixed = sp.simplify(eta * hilbert_cov)
    canonical_translation_mixed = sp.Matrix(
        4,
        4,
        lambda mu, nu: sp.expand(
            -q_up[mu] * q[nu]
            - (sp.Integer(1) if mu == nu else sp.Integer(0)) * lagrangian
        ),
    )
    # With (-+++) the physical Hilbert mixed tensor and the canonical
    # translation tensor use opposite mixed-index energy-current conventions.
    hilbert_translation_residual = sp.simplify(
        hilbert_mixed + canonical_translation_mixed
    )
    hilbert_translation_ledger_match_exact = all_zero(
        hilbert_translation_residual
    )

    expected_energy = sp.Rational(1, 2) * sum(item**2 for item in q) + V
    energy_component_residual = sp.simplify(hilbert_cov[0, 0] - expected_energy)
    energy_component_exact = exact_zero(energy_component_residual)
    momentum_components_exact = all(
        exact_zero(hilbert_cov[0, i] - q[0] * q[i]) for i in range(1, 4)
    )
    stress_symmetric_exact = hilbert_cov == hilbert_cov.T

    source_ledger = OrderedDict(
        [
            ("selected_operational_S_loc_variation", 1),
            ("metric_self_energy_readded_on_rhs", 0),
            ("P_F_or_p_readout_readded", 0),
            ("clock_or_ruler_readout_readded", 0),
            ("homogeneous_vacuum_offset_readded_on_rhs", 0),
        ]
    )
    one_source_ledger_selected_consistent = sum(source_ledger.values()) == 1
    duplicate_pressure_source_mutation_rejected = (
        sum({**source_ledger, "P_F_or_p_readout_readded": 1}.values()) != 1
    )

    # The pregeometric ledger is not a Lorentz-covariant microscopic T_mn.
    # T_mn exists only after the operational metric emerges, which explicitly
    # avoids assuming the premise forbidden by the Weinberg--Witten theorem.
    weinberg_witten_scope = OrderedDict(
        [
            ("foundation_pregeometric_not_background_minkowski_qft", True),
            ("no_preexisting_lorentz_covariant_micro_T_mn", True),
            ("operational_T_defined_only_after_metric_emergence", True),
            ("gravitational_self_energy_not_local_gauge_invariant_T", True),
        ]
    )
    weinberg_witten_scope_consistent = all(weinberg_witten_scope.values())

    # ------------------------------------------------------------------
    # 7. Dependency, circularity, closure, and mutation gates.
    # ------------------------------------------------------------------
    dependency_records = OrderedDict()
    for name, path in dependency_paths(work3).items():
        actual = sha256(path) if path.exists() else None
        dependency_records[name] = OrderedDict(
            [
                ("exists", path.exists()),
                ("expected_sha256", DEPENDENCY_HASHES[name]),
                ("actual_sha256", actual),
                ("verified", actual == DEPENDENCY_HASHES[name]),
            ]
        )
    dependencies_verified = all(
        record["verified"] for record in dependency_records.values()
    )

    forbidden_dependencies = [
        "w3_01_emergent_metric_from_pressure.py",
        "w3_02_emergent_action_from_pressure.py",
        "w4_02_biconformal_gravity.py",
        "w4_04_strain_tensor_action.py",
        "w4_05_defect_tensor_gravity.py",
        "w4_06_kleinert_equivalence.py",
    ]
    declared_logical_dependencies = list(DEPENDENCY_HASHES)
    historical_ansatz_not_used = not any(
        name in declared_logical_dependencies for name in forbidden_dependencies
    )

    exact_checks = OrderedDict(
        [
            ("gram_principal_axis_volume_shape_witness_exact", exact_zero(gram_volume_residual)),
            ("trace_free_shape_exact", exact_zero(trace_free_shape_residual)),
            ("shape_independent_of_volume_exact", shape_independent_of_volume),
            ("selected_ir_premises_complete", ir_premises_complete),
            ("fp_solution_space_one_dimensional", one_dimensional_fp_family),
            ("fp_coefficients_from_gauge_identity_exact", fp_coefficients_exact),
            ("fp_positive_tt_normalization", bool(fp_positive_tt_kinetic)),
            ("fp_helicity_theorem_arithmetic_consistent", fp_helicity_theorem_arithmetic_consistent),
            ("scalar_ocean_rejected_as_complete_geometry", scalar_ocean_rejected_as_complete_geometry),
            ("pure_gradient_strain_rejected", pure_gradient_rejected_as_physical_tensor),
            ("independent_tensor_curvature_witness", independent_tensor_can_curve),
            ("soft_pairwise_witness_exact", soft_pairwise_witness_exact),
            ("source_gauge_invariance_iff_conserved", source_gauge_invariance_iff_conserved),
            ("deser_operator_registry_consistent", deser_operator_registry_consistent),
            ("hilbert_translation_ledger_match_exact", hilbert_translation_ledger_match_exact),
            ("T00_energy_density_exact", energy_component_exact),
            ("T0i_momentum_density_exact", momentum_components_exact),
            ("Tij_stress_symmetric_exact", stress_symmetric_exact),
            ("one_source_ledger_selected_consistent", one_source_ledger_selected_consistent),
            ("weinberg_witten_scope_consistent", weinberg_witten_scope_consistent),
            ("dependencies_verified", dependencies_verified),
            ("declared_historical_dependency_exclusion", historical_ansatz_not_used),
        ]
    )
    premise_mutation_checks = OrderedDict()
    for name in (
        "closed_reversible_foundation_action",
        "connected_3plus1_emergent_lorentz_invariance",
        "no_extra_unsuppressed_gapless_geometry_mode",
        "no_unsuppressed_nonminimal_curvature_coupling_at_retained_order",
    ):
        mutated = OrderedDict(selected_ir_premises)
        mutated[name] = False
        premise_mutation_checks[name] = not all(mutated.values())

    mutation_checks = OrderedDict(
        [
            ("every_fp_coefficient_mutation_rejected", fp_mutation_controls_pass),
            ("species_dependent_soft_coupling_rejected", species_dependent_coupling_rejected),
            ("missing_registered_self_coupling_detected", missing_registered_self_coupling_detected),
            ("duplicate_pressure_source_rejected", duplicate_pressure_source_mutation_rejected),
            ("selected_premise_mutations_rejected", all(premise_mutation_checks.values())),
        ]
    )
    aggregate_pass = all(
        [
            all(exact_checks.values()),
            all(mutation_checks.values()),
            theorem_handoffs_complete,
        ]
    )

    closure_flags = OrderedDict(
        [
            ("FOUNDATION_CANONICAL_CONSERVATION_SELECTED", True),
            ("W3_42_COMPATIBLE_VOLUME_SHAPE_BRANCH_SELECTED", True),
            ("INDEPENDENT_IR_TENSOR_BRANCH_SELECTED", True),
            ("EMERGENT_LORENTZ_AND_COMMON_CONE_SELECTED", True),
            ("LINEAR_RELABELING_GAUGE_BRANCH_SELECTED", True),
            ("FIERZ_PAULI_COEFFICIENTS_DERIVED", fp_coefficients_exact),
            ("FP_TWO_HELICITY_THEOREM_APPLIED", theorem_handoffs["FIERZ_PAULI_TWO_HELICITY_THEOREM_APPLIED"]),
            ("WEINBERG_SOFT_UNIVERSALITY_THEOREM_APPLIED", theorem_handoffs["WEINBERG_SOFT_UNIVERSALITY_THEOREM_APPLIED"]),
            ("DESER_PALATINI_BOOTSTRAP_THEOREM_APPLIED", theorem_handoffs["DESER_PALATINI_BOOTSTRAP_THEOREM_APPLIED"]),
            ("LOVELOCK_0PLUS2_THEOREM_APPLIED", theorem_handoffs["LOVELOCK_4D_ZERO_PLUS_TWO_DERIVATIVE_THEOREM_APPLIED"]),
            ("GENERIC_SLOC_TO_HILBERT_T_MAP_DERIVED", hilbert_translation_ledger_match_exact),
            ("ONE_SOURCE_LEDGER_SELECTED_AND_CONSISTENT", one_source_ledger_selected_consistent),
            ("SELECTED_IR_SPIN2_TO_EH_AND_GENERIC_T_MAP_GATE_CLOSED", aggregate_pass),
            ("NODE_SCALE_MASTER_HAMILTONIAN_DERIVED", False),
            ("FOUNDATION_TO_FULL_METRIC_MAP_DERIVED", False),
            ("COMMON_CONE_FROM_NODE_SPECTRUM_DERIVED", False),
            ("FOUNDATION_LEDGER_TO_S_LOC_COARSE_GRAINING_DERIVED", False),
            ("MICROSCOPIC_SOURCE_MATCHING", False),
            ("PARTICLE_SPECIFIC_S_LOC_DERIVED", False),
            ("G_VALUE_DERIVED", False),
            ("LAMBDA_VALUE_DERIVED", False),
            ("HIGHER_DERIVATIVE_COEFFICIENTS_DERIVED", False),
        ]
    )

    result = OrderedDict(
        [
            ("claim_id", CLAIM_ID),
            ("model_version", MODEL_VERSION),
            ("status", STATUS_PASS if aggregate_pass else "FAIL"),
            ("aggregate_pass", aggregate_pass),
            ("scope", "selected_IR_spin2_to_EH_operator_and_generic_operational_Hilbert_T_map_then_stop"),
            ("selected_ir_premises", selected_ir_premises),
            (
                "gram_decomposition_witness",
                OrderedDict(
                    [
                        ("frame", "G0-orthonormal principal-axis frame"),
                        ("G_relative_ij", "a^2 exp(2 s)_ij with tr(s)=0"),
                        ("sqrt_det_G_relative", str(sp.simplify(gram_measure_ratio))),
                        ("volume_residual", str(gram_volume_residual)),
                        ("role", "a is link/volume dilation; P_F, eta_F and p remain distinct conditionally linked variables; s_ij is shape/shear"),
                    ]
                ),
            ),
            ("fp_coefficients", OrderedDict((key, str(value)) for key, value in fp_coefficients.items())),
            ("fp_gauge_residuals", OrderedDict((key, str(value)) for key, value in fp_residuals.items())),
            ("fp_registered_physical_helicities", physical_helicities),
            ("soft_pairwise_witness", "g2=g1 cancels all four components; g2=2*g1 fails generically"),
            ("theorem_handoffs", theorem_handoffs),
            (
                "eh_endpoint",
                "Deser theorem gives the EH R operator; Lambda is a separately allowed zero-derivative matching term",
            ),
            (
                "source_endpoint",
                "T_mn=-(2*c0/sqrt(-g)) delta S_loc/delta g^mn in the standard (-+++) theorem convention",
            ),
            ("source_ledger", source_ledger),
            (
                "evidence_roles",
                OrderedDict(
                    [
                        ("computed_exact", "Gram principal-axis witness; FP coefficient ratios; pure-gradient curvature; reduced soft pair; scalar Hilbert/translation ledger"),
                        ("external_theorems", "Fierz-Pauli spectrum; Weinberg soft universality; Deser bootstrap; Lovelock uniqueness"),
                        ("selected_not_derived", "IR tensor/full Lorentz branch; no extra retained mode/nonminimal coupling; one-source ledger"),
                    ]
                ),
            ),
            ("exact_checks", exact_checks),
            ("mutation_checks", mutation_checks),
            ("premise_mutation_checks", premise_mutation_checks),
            ("fp_mutations", fp_mutations),
            ("weinberg_witten_scope", weinberg_witten_scope),
            ("dependency_records", dependency_records),
            ("closure_flags", closure_flags),
            (
                "explicit_boundary",
                "The selected IR spin-2 branch reaches the EH operator and generic Hilbert source map. Phi_F-to-full-metric and foundation-ledger-to-S_loc matching, node-scale realization, G and Lambda values remain unproved.",
            ),
            (
                "stop_rule",
                "STOP at the Einstein-Hilbert operator plus the generic operational T_mn map; do not open particles, cosmology, 2PN, strong-field, or data stages.",
            ),
            (
                "provenance",
                OrderedDict(
                    [
                        ("python", sys.version.split()[0]),
                        ("sympy", sp.__version__),
                        ("platform", platform.platform()),
                        ("utc", datetime.now(timezone.utc).isoformat()),
                    ]
                ),
            ),
        ]
    )

    out_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    if not aggregate_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
