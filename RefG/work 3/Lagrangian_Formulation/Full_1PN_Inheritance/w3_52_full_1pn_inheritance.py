"""W3-52: conditional full standard 1PN inheritance for RefG.

The program audits a conditional theorem.  It does not derive the
Einstein--Hilbert action or the published GR PPN vector from the RefG
foundation.  Its exact claim is: once that effective action, universal
coupling, conserved one-source problem and 1PN suppression boundary are
frozen, their GR 1PN solution is inherited without a second RefG force or
source.  Published PPN data are explicit benchmark inputs with integrity
locks, never fitted targets.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import OrderedDict
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_52_REFG_FULL_1PN_INHERITANCE"
MODEL_VERSION = "W3-52-v1.1-FULL-1PN-INHERITANCE"
AGGREGATE_PASS = "CONDITIONAL_MATCHED_THROUGH_FULL_STANDARD_1PN_PPN"
IMPLICATION_PASS = "CONDITIONAL_IMPLICATION_PASS"
EXACT_COROLLARY = "EXACT_1PN_INHERITANCE_ON_SELECTED_EH_OPERATIONAL_BRANCH"

# Integrity locks for the explicitly documented Will--Nordtvedt/Will
# standard PPN registry and its published GR parameter vector.  They protect
# against accidental target or transcription changes; they do not constitute
# a derivation of those external benchmark theorems.
PPN_FORMULA_REGISTRY_SHA256 = (
    "f0f71df9c86aae05aca8487ff551ba605d7aad72e0bf4cb44e567b699f3a10bd"
)
GR_PPN_VECTOR_SHA256 = (
    "eedc1c9b0c727171a171182199f7e5df9a1370cebc547604e1511b8b51e14f87"
)


def zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_registry_sha256(registry: OrderedDict) -> str:
    payload = json.dumps(
        [[key, value] for key, value in registry.items()],
        ensure_ascii=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def registry_residual(
    left: OrderedDict[str, sp.Expr],
    right: OrderedDict[str, sp.Expr],
) -> OrderedDict[str, sp.Expr]:
    if tuple(left) != tuple(right):
        raise ValueError("coefficient registries use different bases")
    return OrderedDict(
        (name, sp.simplify(left[name] - right[name])) for name in left
    )


def all_zero(registry: OrderedDict[str, sp.Expr]) -> bool:
    return all(zero(value) for value in registry.values())


def universal_single_metric(couplings: OrderedDict[str, str]) -> bool:
    return len(set(couplings.values())) == 1


def one_conserved_source(
    ledger: OrderedDict[str, int], conservation_identity: bool
) -> bool:
    return sum(ledger.values()) == 1 and conservation_identity


def exact_order_registry(
    actual: OrderedDict[str, sp.Rational],
    required: OrderedDict[str, sp.Rational],
) -> bool:
    return actual == required


def after_retained_orders(
    actual: OrderedDict[str, sp.Rational],
    first_omitted: OrderedDict[str, sp.Rational],
) -> bool:
    return tuple(actual) == tuple(first_omitted) and all(
        actual[name] >= first_omitted[name] for name in first_omitted
    )


def exact_eh_action(
    selected: OrderedDict[str, sp.Expr],
    canonical: OrderedDict[str, sp.Expr],
) -> bool:
    return tuple(selected) == tuple(canonical) and all_zero(
        registry_residual(selected, canonical)
    )


def inheritance_antecedent(
    *,
    action_ok: bool,
    couplings: OrderedDict[str, str],
    ledger: OrderedDict[str, int],
    conserved: bool,
    no_preferred_direction: bool,
    shared_problem: bool,
    component_orders: OrderedDict[str, sp.Rational],
    required_orders: OrderedDict[str, sp.Rational],
    lambda_orders: OrderedDict[str, sp.Rational],
    higher_orders: OrderedDict[str, sp.Rational],
    first_omitted: OrderedDict[str, sp.Rational],
) -> bool:
    return all(
        [
            action_ok,
            universal_single_metric(couplings),
            one_conserved_source(ledger, conserved),
            no_preferred_direction,
            shared_problem,
            exact_order_registry(component_orders, required_orders),
            after_retained_orders(lambda_orders, first_omitted),
            after_retained_orders(higher_orders, first_omitted),
        ]
    )


def stringify_orders(registry: OrderedDict[str, sp.Rational]) -> OrderedDict:
    return OrderedDict((name, str(value)) for name, value in registry.items())


def main() -> None:
    # ------------------------------------------------------------------
    # 1. Explicit effective premises and their basis-level consequences
    # ------------------------------------------------------------------
    G, c0, Lambda = sp.symbols("G c0 Lambda", positive=True)
    kappa = 8 * sp.pi * G / c0**4

    # These two independently written registries audit the selected premise.
    # Equality is not advertised as a foundation derivation.
    canonical_eh_action = OrderedDict(
        [
            ("sqrt_minus_g_R", sp.Integer(1)),
            ("sqrt_minus_g_Lambda", -2 * Lambda),
            ("S_matter_of_g_and_Psi", sp.Integer(1)),
            ("extra_long_range_scalar_at_1PN", sp.Integer(0)),
            ("extra_long_range_vector_at_1PN", sp.Integer(0)),
            ("second_operational_metric_at_1PN", sp.Integer(0)),
            ("unsuppressed_higher_operator_at_1PN", sp.Integer(0)),
        ]
    )
    selected_refg_effective_action = OrderedDict(
        [
            ("sqrt_minus_g_R", sp.Integer(1)),
            ("sqrt_minus_g_Lambda", -2 * Lambda),
            ("S_matter_of_g_and_Psi", sp.Integer(1)),
            ("extra_long_range_scalar_at_1PN", sp.Integer(0)),
            ("extra_long_range_vector_at_1PN", sp.Integer(0)),
            ("second_operational_metric_at_1PN", sp.Integer(0)),
            ("unsuppressed_higher_operator_at_1PN", sp.Integer(0)),
        ]
    )
    action_premise_residual = registry_residual(
        selected_refg_effective_action, canonical_eh_action
    )
    assumed_eh_action_ok = exact_eh_action(
        selected_refg_effective_action, canonical_eh_action
    )

    # Registered EH basis variations: delta(sqrt(-g)R)->G_mn,
    # delta(-2 Lambda sqrt(-g))->Lambda g_mn after normalization, and
    # delta S_matter->-(8 pi G/c0^4)T_mn.
    derived_field_equation = OrderedDict(
        [
            ("G_mn", selected_refg_effective_action["sqrt_minus_g_R"]),
            (
                "Lambda_g_mn",
                sp.simplify(
                    -selected_refg_effective_action[
                        "sqrt_minus_g_Lambda"
                    ]
                    / (2 * Lambda)
                ),
            ),
            (
                "T_mn",
                -kappa
                * selected_refg_effective_action["S_matter_of_g_and_Psi"],
            ),
        ]
    )
    canonical_einstein_equation = OrderedDict(
        [
            ("G_mn", sp.Integer(1)),
            ("Lambda_g_mn", sp.Integer(1)),
            ("T_mn", -kappa),
        ]
    )
    field_equation_residual = registry_residual(
        derived_field_equation, canonical_einstein_equation
    )
    eh_variation_corollary_ok = all_zero(field_equation_residual)

    div_T = sp.symbols("div_T", real=True)
    divergence_equation = sp.Eq(-kappa * div_T, 0)
    divergence_solutions = sp.solve(divergence_equation, div_T)
    conservation_corollary_ok = divergence_solutions == [sp.Integer(0)]

    couplings = OrderedDict(
        [
            ("massive_matter", "g_mn"),
            ("radiation", "g_mn"),
            ("material_clocks", "g_mn"),
            ("material_rulers", "g_mn"),
        ]
    )
    source_ledger = OrderedDict(
        [
            ("T_mn_from_S_matter", 1),
            ("p_readout_as_extra_source", 0),
            ("foundation_pressure_as_extra_source", 0),
            ("cadence_readout_as_extra_source", 0),
        ]
    )
    shared_problem_registry = OrderedDict(
        [
            ("same_measured_G", True),
            ("same_matter_action_and_source_data", True),
            ("same_standard_PPN_gauge", True),
            ("same_local_background_subtraction", True),
            ("same_boundary_conditions", True),
        ]
    )
    shared_problem_ok = all(shared_problem_registry.values())
    no_preferred_direction = True  # explicit selected-branch premise

    # q~U/c0^2~v^2/c0^2.  Values are powers of q through which each metric
    # component is retained, followed by its first omitted power.
    required_component_orders = OrderedDict(
        [
            ("g00", sp.Rational(2)),
            ("g0i", sp.Rational(3, 2)),
            ("gij", sp.Rational(1)),
        ]
    )
    selected_component_orders = OrderedDict(
        [
            ("g00", sp.Rational(2)),
            ("g0i", sp.Rational(3, 2)),
            ("gij", sp.Rational(1)),
        ]
    )
    first_omitted_orders = OrderedDict(
        [
            ("g00", sp.Rational(3)),
            ("g0i", sp.Rational(5, 2)),
            ("gij", sp.Rational(2)),
        ]
    )
    lambda_effect_first_orders = OrderedDict(first_omitted_orders)
    higher_effect_first_orders = OrderedDict(first_omitted_orders)

    component_orders_ok = exact_order_registry(
        selected_component_orders, required_component_orders
    )
    local_remainder_ok = after_retained_orders(
        lambda_effect_first_orders, first_omitted_orders
    ) and after_retained_orders(
        higher_effect_first_orders, first_omitted_orders
    )

    antecedent_ok = inheritance_antecedent(
        action_ok=assumed_eh_action_ok and eh_variation_corollary_ok,
        couplings=couplings,
        ledger=source_ledger,
        conserved=conservation_corollary_ok,
        no_preferred_direction=no_preferred_direction,
        shared_problem=shared_problem_ok,
        component_orders=selected_component_orders,
        required_orders=required_component_orders,
        lambda_orders=lambda_effect_first_orders,
        higher_orders=higher_effect_first_orders,
        first_omitted=first_omitted_orders,
    )

    # ------------------------------------------------------------------
    # 2. Published full PPN benchmark: integrity and transcription audit
    # ------------------------------------------------------------------
    gamma, beta, xi = sp.symbols("gamma beta xi", real=True)
    alpha1, alpha2, alpha3 = sp.symbols(
        "alpha1 alpha2 alpha3", real=True
    )
    zeta1, zeta2, zeta3, zeta4 = sp.symbols(
        "zeta1 zeta2 zeta3 zeta4", real=True
    )
    ppn_parameters = (
        gamma,
        beta,
        xi,
        alpha1,
        alpha2,
        alpha3,
        zeta1,
        zeta2,
        zeta3,
        zeta4,
    )
    symbol_table = {str(parameter): parameter for parameter in ppn_parameters}

    # Standard PPN metric in the (-,+,+,+) convention.  Powers of c0 are
    # absorbed into the standard potentials.  These strings are a published
    # benchmark fixture, not an ansatz fitted by this program.
    ppn_formula_text = OrderedDict(
        [
            ("g00_U", "2"),
            ("g00_U2", "-2*beta"),
            ("g00_PhiW", "-2*xi"),
            (
                "g00_Phi1",
                "2*gamma + 2 + alpha3 + zeta1 - 2*xi",
            ),
            (
                "g00_Phi2",
                "2*(3*gamma - 2*beta + 1 + zeta2 + xi)",
            ),
            ("g00_Phi3", "2*(1 + zeta3)"),
            ("g00_Phi4", "2*(3*gamma + 3*zeta4 - 2*xi)"),
            ("g00_A", "-(zeta1 - 2*xi)"),
            ("g00_w2U", "-(alpha1 - alpha2 - alpha3)"),
            ("g00_wwUij", "-alpha2"),
            ("g00_wV", "2*alpha3 - alpha1"),
            (
                "g0i_Vi",
                "-(4*gamma + 3 + alpha1 - alpha2 + zeta1 - 2*xi)/2",
            ),
            (
                "g0i_Wi",
                "-(1 + alpha2 - zeta1 + 2*xi)/2",
            ),
            ("g0i_wiU", "-(alpha1 - 2*alpha2)/2"),
            ("g0i_wjUij", "-alpha2"),
            ("gij_U_deltaij", "2*gamma"),
        ]
    )
    formula_registry_hash = canonical_registry_sha256(ppn_formula_text)
    formula_integrity_ok = formula_registry_hash == PPN_FORMULA_REGISTRY_SHA256
    ppn_coefficients = OrderedDict(
        (
            name,
            sp.sympify(formula, locals=symbol_table),
        )
        for name, formula in ppn_formula_text.items()
    )

    published_gr_ppn = OrderedDict(
        [
            ("gamma", 1),
            ("beta", 1),
            ("xi", 0),
            ("alpha1", 0),
            ("alpha2", 0),
            ("alpha3", 0),
            ("zeta1", 0),
            ("zeta2", 0),
            ("zeta3", 0),
            ("zeta4", 0),
        ]
    )
    gr_vector_hash = canonical_registry_sha256(published_gr_ppn)
    gr_benchmark_integrity_ok = gr_vector_hash == GR_PPN_VECTOR_SHA256
    gr_substitution = {
        symbol_table[name]: sp.Integer(value)
        for name, value in published_gr_ppn.items()
    }
    published_gr_coefficients = OrderedDict(
        (name, sp.simplify(expr.subs(gr_substitution)))
        for name, expr in ppn_coefficients.items()
    )

    # This inversion is deliberately classified only as a transcription and
    # formal-identifiability regression.  It is not an independent EH->PPN
    # derivation and does not establish the published benchmark values.
    coefficient_equations = [
        sp.simplify(
            ppn_coefficients[name] - published_gr_coefficients[name]
        )
        for name in ppn_coefficients
    ]
    coefficient_rank = sp.Matrix(coefficient_equations).jacobian(
        ppn_parameters
    ).rank()
    regression_solutions = sp.solve(
        coefficient_equations, ppn_parameters, dict=True, simplify=True
    )
    expected_solution = {
        symbol_table[name]: sp.Integer(value)
        for name, value in published_gr_ppn.items()
    }
    transcription_regression_ok = (
        coefficient_rank == len(ppn_parameters)
        and len(regression_solutions) == 1
        and all(
            zero(
                regression_solutions[0][parameter]
                - expected_solution[parameter]
            )
            for parameter in ppn_parameters
        )
    )

    benchmark_audit_ok = all(
        [
            formula_integrity_ok,
            gr_benchmark_integrity_ok,
            transcription_regression_ok,
        ]
    )
    conditional_full_1pn_inheritance_ok = antecedent_ok and benchmark_audit_ok
    inherited_ppn = OrderedDict(published_gr_ppn)
    inherited_ppn_flags = OrderedDict(
        (
            f"PPN_{name.upper()}_INHERITED_COROLLARY",
            bool(conditional_full_1pn_inheritance_ok),
        )
        for name in inherited_ppn
    )

    # ------------------------------------------------------------------
    # 3. Static pressure readout: clock exact, ruler to retained spatial order
    # ------------------------------------------------------------------
    eps, u = sp.symbols("eps u", real=True)
    p_clock = (1 - eps * u / 2) / (1 + eps * u / 2)
    p_ruler = (1 + eps * u / 2) ** -2
    p_clock_series = sp.series(p_clock, eps, 0, 3).removeO().expand()
    p_ruler_series = sp.series(p_ruler, eps, 0, 3).removeO().expand()
    common_clock_ruler_linear_ok = zero(
        p_clock_series.coeff(eps, 1) - p_ruler_series.coeff(eps, 1)
    )

    minus_log_p_clock = sp.series(
        -sp.log(p_clock), eps, 0, 4
    ).removeO().expand()
    log_readout_residuals = OrderedDict(
        (
            f"eps^{order}",
            sp.simplify((minus_log_p_clock - eps * u).coeff(eps, order)),
        )
        for order in (1, 2)
    )
    static_g00 = sp.series(p_clock**2, eps, 0, 3).removeO().expand()
    static_spatial = sp.series(
        (1 + eps * u / 2) ** 4, eps, 0, 2
    ).removeO().expand()
    static_beta = sp.simplify(static_g00.coeff(eps, 2) / (2 * u**2))
    static_gamma = sp.simplify(static_spatial.coeff(eps, 1) / (2 * u))
    static_readout_ok = all(
        [
            all_zero(log_readout_residuals),
            common_clock_ruler_linear_ok,
            zero(static_beta - 1),
            zero(static_gamma - 1),
        ]
    )

    # Identical action, matter, gauge, source and boundary problems have the
    # same weak-body 1PN extremals.  EIH is therefore an inherited corollary,
    # not a re-derived microscopic world-tube result in this gate.
    published_eih_theorem_registered = True
    eih_inherited_corollary_ok = (
        conditional_full_1pn_inheritance_ok
        and published_eih_theorem_registered
    )

    # ------------------------------------------------------------------
    # 4. Controls: each mutation must break its targeted implication/audit
    # ------------------------------------------------------------------
    eta, a = sp.symbols("eta a", real=True, nonzero=True)

    extra_scalar_action = OrderedDict(selected_refg_effective_action)
    extra_scalar_action["extra_long_range_scalar_at_1PN"] = eta
    extra_scalar_breaks_inheritance = not inheritance_antecedent(
        action_ok=exact_eh_action(extra_scalar_action, canonical_eh_action),
        couplings=couplings,
        ledger=source_ledger,
        conserved=conservation_corollary_ok,
        no_preferred_direction=no_preferred_direction,
        shared_problem=shared_problem_ok,
        component_orders=selected_component_orders,
        required_orders=required_component_orders,
        lambda_orders=lambda_effect_first_orders,
        higher_orders=higher_effect_first_orders,
        first_omitted=first_omitted_orders,
    )

    extra_vector_action = OrderedDict(selected_refg_effective_action)
    extra_vector_action["extra_long_range_vector_at_1PN"] = eta
    extra_vector_breaks_inheritance = not exact_eh_action(
        extra_vector_action, canonical_eh_action
    )

    bimetric_couplings = OrderedDict(couplings)
    bimetric_couplings["radiation"] = "h_mn"
    bimetric_breaks_inheritance = not universal_single_metric(
        bimetric_couplings
    )

    duplicated_source_ledger = OrderedDict(source_ledger)
    duplicated_source_ledger["p_readout_as_extra_source"] = 1
    duplicated_source_breaks_inheritance = not one_conserved_source(
        duplicated_source_ledger, conservation_corollary_ok
    )
    nonconserved_source_breaks_inheritance = not one_conserved_source(
        source_ledger, conservation_identity=False
    )

    missing_g0i_orders = OrderedDict(selected_component_orders)
    del missing_g0i_orders["g0i"]
    missing_g0i_breaks_inheritance = not exact_order_registry(
        missing_g0i_orders, required_component_orders
    )
    wrong_g0i_orders = OrderedDict(selected_component_orders)
    wrong_g0i_orders["g0i"] = sp.Rational(1)
    wrong_g0i_order_breaks_inheritance = not exact_order_registry(
        wrong_g0i_orders, required_component_orders
    )

    preferred_direction_breaks_inheritance = not inheritance_antecedent(
        action_ok=assumed_eh_action_ok and eh_variation_corollary_ok,
        couplings=couplings,
        ledger=source_ledger,
        conserved=conservation_corollary_ok,
        no_preferred_direction=False,
        shared_problem=shared_problem_ok,
        component_orders=selected_component_orders,
        required_orders=required_component_orders,
        lambda_orders=lambda_effect_first_orders,
        higher_orders=higher_effect_first_orders,
        first_omitted=first_omitted_orders,
    )

    unsuppressed_higher_orders = OrderedDict(higher_effect_first_orders)
    unsuppressed_higher_orders["g00"] = sp.Rational(2)
    higher_operator_breaks_inheritance = not after_retained_orders(
        unsuppressed_higher_orders, first_omitted_orders
    )
    unsuppressed_lambda_orders = OrderedDict(lambda_effect_first_orders)
    unsuppressed_lambda_orders["gij"] = sp.Rational(1)
    local_lambda_breaks_inheritance = not after_retained_orders(
        unsuppressed_lambda_orders, first_omitted_orders
    )

    mutated_gr_vector = OrderedDict(published_gr_ppn)
    mutated_gr_vector["beta"] = 2
    benchmark_target_mutation_detected = (
        canonical_registry_sha256(mutated_gr_vector) != GR_PPN_VECTOR_SHA256
    )
    mutated_formula_registry = OrderedDict(ppn_formula_text)
    mutated_formula_registry["g0i_wjUij"] = "-alpha1"
    formula_mutation_detected = (
        canonical_registry_sha256(mutated_formula_registry)
        != PPN_FORMULA_REGISTRY_SHA256
    )

    p_log_mutation = sp.exp(-eps * u + a * eps**2 * u**2)
    mutated_g00 = sp.series(
        p_log_mutation**2, eps, 0, 3
    ).removeO().expand()
    mutated_beta = sp.simplify(
        mutated_g00.coeff(eps, 2) / (2 * u**2)
    )
    static_constitutive_mutation_detected = zero(mutated_beta - (1 + a))

    controls = OrderedDict(
        [
            (
                "extra_scalar_breaks_exact_inheritance",
                extra_scalar_breaks_inheritance,
            ),
            (
                "extra_vector_breaks_exact_inheritance",
                extra_vector_breaks_inheritance,
            ),
            (
                "bimetric_coupling_breaks_exact_inheritance",
                bimetric_breaks_inheritance,
            ),
            (
                "duplicated_source_breaks_exact_inheritance",
                duplicated_source_breaks_inheritance,
            ),
            (
                "nonconserved_source_breaks_exact_inheritance",
                nonconserved_source_breaks_inheritance,
            ),
            (
                "missing_g0i_breaks_full_1PN_scope",
                missing_g0i_breaks_inheritance,
            ),
            (
                "wrong_g0i_order_breaks_full_1PN_scope",
                wrong_g0i_order_breaks_inheritance,
            ),
            (
                "preferred_direction_breaks_exact_inheritance",
                preferred_direction_breaks_inheritance,
            ),
            (
                "unsuppressed_higher_operator_breaks_1PN_boundary",
                higher_operator_breaks_inheritance,
            ),
            (
                "unsuppressed_local_lambda_breaks_1PN_boundary",
                local_lambda_breaks_inheritance,
            ),
            (
                "published_beta_target_mutation_detected",
                benchmark_target_mutation_detected,
            ),
            ("PPN_formula_mutation_detected", formula_mutation_detected),
            (
                "second_order_log_mutation_detected",
                static_constitutive_mutation_detected,
            ),
        ]
    )
    controls_ok = all(controls.values())

    # ------------------------------------------------------------------
    # 5. Fail-closed aggregation with evidence roles kept explicit
    # ------------------------------------------------------------------
    flags: OrderedDict[str, bool] = OrderedDict(
        [
            ("ASSUMED_EH_ACTION_THROUGH_1PN_REGISTERED", assumed_eh_action_ok),
            ("EH_VARIATION_COROLLARY", eh_variation_corollary_ok),
            ("BIANCHI_CONSERVATION_COROLLARY", conservation_corollary_ok),
            ("UNIVERSAL_SINGLE_METRIC_PREMISE_REGISTERED", universal_single_metric(couplings)),
            ("ONE_SOURCE_LEDGER_PREMISE_REGISTERED", one_conserved_source(source_ledger, conservation_corollary_ok)),
            ("FULL_1PN_COMPONENT_ORDER_REGISTRY", component_orders_ok),
            ("COMPONENTWISE_LOCAL_REMAINDER_BOUND", local_remainder_ok),
            ("PPN_FORMULA_BENCHMARK_INTEGRITY", formula_integrity_ok),
            ("GR_PPN_VECTOR_BENCHMARK_INTEGRITY", gr_benchmark_integrity_ok),
            ("PPN_REGISTRY_RANK_TEN", coefficient_rank == 10),
            ("PPN_TRANSCRIPTION_REGRESSION", transcription_regression_ok),
            ("CONDITIONAL_FULL_1PN_INHERITANCE", conditional_full_1pn_inheritance_ok),
        ]
    )
    flags.update(inherited_ppn_flags)
    flags.update(
        [
            ("STATIC_PRESSURE_READOUT_REGRESSION", static_readout_ok),
            ("EIH_1PN_INHERITED_COROLLARY", eih_inherited_corollary_ok),
            ("MUTATION_CONTROLS", controls_ok),
            ("FOUNDATION_TO_EH_DERIVATION", False),
            ("FOUNDATION_TO_FULL_METRIC_MAP", False),
            ("MICROSCOPIC_SOURCE_MATCHING", False),
            ("STRONG_FIELD_AND_2PN_COMPLETION", False),
        ]
    )

    tested_flags = [
        name
        for name in flags
        if name
        not in {
            "FOUNDATION_TO_EH_DERIVATION",
            "FOUNDATION_TO_FULL_METRIC_MAP",
            "MICROSCOPIC_SOURCE_MATCHING",
            "STRONG_FIELD_AND_2PN_COMPLETION",
        }
    ]
    gate_pass = all(flags[name] for name in tested_flags)

    script_path = Path(__file__).resolve()
    contract_path = script_path.with_name(
        "w3_52_full_1pn_inheritance_contract.md"
    )
    result_path = script_path.with_name("w3_52_result.json")

    premise_evidence = OrderedDict(
        [
            ("EH_action_through_1PN", "FROZEN_EFFECTIVE_PREMISE"),
            ("universal_single_metric", "FROZEN_EFFECTIVE_PREMISE"),
            ("one_conserved_source_ledger", "FROZEN_EFFECTIVE_PREMISE"),
            ("no_preferred_operational_direction", "FROZEN_EFFECTIVE_PREMISE"),
            ("componentwise_suppression_boundary", "FROZEN_EFFECTIVE_PREMISE"),
            ("published_GR_PPN_vector", "EXTERNAL_BENCHMARK_THEOREM"),
            ("published_EIH_result", "EXTERNAL_BENCHMARK_THEOREM"),
        ]
    )
    result = OrderedDict(
        [
            ("claim_id", CLAIM_ID),
            ("model_version", MODEL_VERSION),
            ("gate_status", "PASS" if gate_pass else "FAIL"),
            ("implication_status", IMPLICATION_PASS if gate_pass else "FAIL"),
            ("aggregate_status", AGGREGATE_PASS if gate_pass else "FAIL"),
            ("exact_corollary", EXACT_COROLLARY if gate_pass else "FAIL"),
            (
                "claim_boundary",
                "selected EH operational branch; isolated generic weak-field "
                "slow-motion conserved sources; full standard 1PN/PPN",
            ),
            ("premise_evidence", premise_evidence),
            (
                "action_premise_residuals",
                OrderedDict(
                    (name, str(value))
                    for name, value in action_premise_residual.items()
                ),
            ),
            (
                "EH_variation_residuals",
                OrderedDict(
                    (name, str(value))
                    for name, value in field_equation_residual.items()
                ),
            ),
            ("source_conservation_solution", [str(x) for x in divergence_solutions]),
            ("coupling_registry", couplings),
            ("source_ledger", source_ledger),
            ("shared_problem_registry", shared_problem_registry),
            (
                "component_orders_in_q",
                stringify_orders(selected_component_orders),
            ),
            (
                "first_omitted_orders_in_q",
                stringify_orders(first_omitted_orders),
            ),
            (
                "published_GR_PPN_inherited_corollary",
                inherited_ppn,
            ),
            ("PPN_formula_registry_sha256", formula_registry_hash),
            ("GR_PPN_vector_sha256", gr_vector_hash),
            ("PPN_registry_rank", coefficient_rank),
            ("PPN_parameter_count", len(ppn_parameters)),
            ("PPN_transcription_solution_count", len(regression_solutions)),
            (
                "static_pressure_readout",
                OrderedDict(
                    [
                        ("p_clock_exact", str(p_clock)),
                        ("p_ruler_exact", str(p_ruler)),
                        ("p_clock_series", str(p_clock_series)),
                        ("p_ruler_series", str(p_ruler_series)),
                        ("minus_log_p_clock_series", str(minus_log_p_clock)),
                        ("beta", str(static_beta)),
                        ("gamma", str(static_gamma)),
                        (
                            "clock_ruler_common_through_spatial_order",
                            common_clock_ruler_linear_ok,
                        ),
                    ]
                ),
            ),
            ("log_mutation_beta", str(mutated_beta)),
            ("mutation_controls", controls),
            ("closure_flags", flags),
            (
                "scope_boundary",
                OrderedDict(
                    [
                        ("foundation_to_EH_derivation", "OPEN"),
                        ("foundation_to_full_metric_map", "OPEN"),
                        ("microscopic_source_matching", "OPEN"),
                        ("strong_field_and_2PN", "NOT_TESTED"),
                        ("radiation_reaction_2p5PN", "NOT_TESTED"),
                    ]
                ),
            ),
            (
                "evidence_roles",
                OrderedDict(
                    [
                        (
                            "primary",
                            "conditional functional-identity theorem",
                        ),
                        (
                            "secondary",
                            "published PPN fixture integrity, rank and transcription regression",
                        ),
                        (
                            "bounded_regression",
                            "static isotropic clock/ruler readout through retained orders",
                        ),
                    ]
                ),
            ),
            (
                "provenance",
                OrderedDict(
                    [
                        ("python_version", sys.version.split()[0]),
                        ("sympy_version", sp.__version__),
                        ("script_sha256", sha256(script_path)),
                        ("contract_sha256", sha256(contract_path)),
                        ("external_project_file_dependencies", []),
                        ("runtime_packages", ["Python standard library", "SymPy"]),
                    ]
                ),
            ),
        ]
    )

    result_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not gate_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
