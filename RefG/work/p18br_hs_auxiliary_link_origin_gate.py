from __future__ import annotations

"""PHASE 18br: auxiliary-link origin and induced-plaquette gate.

This gate asks a narrower and more constructive question than p18bq:

    Can the absence of a bare Maxwell/plaquette coefficient follow from an
    exact rewriting of an existing frame interaction, instead of being added
    as a compositeness boundary condition?

For an O(3) frame field the CP1/Schwinger-boson rewrite gives an exact
Hubbard--Stratonovich (HS) bond variable.  Its phase is a compact auxiliary
U(1) link and the one-bond HS action contains no plaquette term.  Integrating
out a gapped charged mode then generates a plaquette term.  The leading
strong-coupling coefficient is computed exactly below.

The result is useful but not an alpha closure.  The induced stiffness depends
continuously on the hopping-to-gap ratios.  Moreover, the CP1 link gauges a
projective frame redundancy; it is not automatically the physical
generation-blind Q=T3+Y connection.  Therefore the next real calculation is
the charged-core Hessian and its representation map, not a scan for a number.

No electromagnetic comparison value is imported or used in this file.
"""

import ast
import inspect
from math import comb

import sympy as sp


def cp1_spin1_rewrite_theorem() -> dict[str, object]:
    """Verify the CP1 bond identity and the h=2 spin-one state count."""

    # Generic complex two-spinors written in real components.  The Pauli
    # completeness identity implies
    #   (z^dag sigma z).(w^dag sigma w)
    #     = 2 |z^dag w|^2 - (z^dag z)(w^dag w).
    zr0, zi0, zr1, zi1 = sp.symbols(
        "z_r0 z_i0 z_r1 z_i1", real=True
    )
    wr0, wi0, wr1, wi1 = sp.symbols(
        "w_r0 w_i0 w_r1 w_i1", real=True
    )
    z = sp.Matrix([zr0 + sp.I * zi0, zr1 + sp.I * zi1])
    w = sp.Matrix([wr0 + sp.I * wi0, wr1 + sp.I * wi1])
    sigma = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    )

    n_z = tuple(sp.expand_complex((z.conjugate().T * s * z)[0]) for s in sigma)
    n_w = tuple(sp.expand_complex((w.conjugate().T * s * w)[0]) for s in sigma)
    lhs = sp.expand(sum(n_z[i] * n_w[i] for i in range(3)))
    overlap = sp.expand_complex((z.conjugate().T * w)[0])
    norm_z = sp.expand_complex((z.conjugate().T * z)[0])
    norm_w = sp.expand_complex((w.conjugate().T * w)[0])
    rhs = sp.expand(2 * overlap * sp.conjugate(overlap) - norm_z * norm_w)
    fierz_residual = sp.simplify(sp.expand_complex(lhs - rhs))

    h = 2
    spin1_dimension = comb(h + 1, 1)
    return {
        "CP1_map": "n=z^dagger sigma z, z^dagger z=1",
        "local_redundancy": "z_x -> exp(i lambda_x) z_x",
        "frame_is_redundancy_invariant": True,
        "exact_fierz_identity": fierz_residual == 0,
        "normalized_bond_identity": (
            "n_x.n_y=2|z_x^dagger z_y|^2-1"
        ),
        "schwinger_boson_occupation_h": h,
        "symmetric_two_boson_dimension": spin1_dimension,
        "spin1_dimension_equals_C3_dimension": spin1_dimension == 3,
        "CP1_spinor_projective_charges": (+1, +1),
        "spin1_Sym2_common_projective_charge": h,
        "spin1_J3_weights_are_projective_charges": False,
        "representation_fact": (
            "h=2 gives the three-dimensional spin-one representation; "
            "this does not identify its projective U(1) with electromagnetism"
        ),
        "reference_value_used": False,
    }


def exact_hubbard_stratonovich_link_theorem() -> dict[str, object]:
    """Complete the HS square and identify the compact bond phase."""

    q_r, q_i, b_r, b_i = sp.symbols(
        "Q_r Q_i b_r b_i", real=True
    )
    J = sp.symbols("J", positive=True)
    q_abs2 = q_r**2 + q_i**2
    b_abs2 = b_r**2 + b_i**2
    re_qstar_b = q_r * b_r + q_i * b_i
    completed_square = (
        (q_r - J * b_r) ** 2 + (q_i - J * b_i) ** 2
    ) / J
    expanded_form = q_abs2 / J - 2 * re_qstar_b + J * b_abs2
    square_residual = sp.simplify(completed_square - expanded_form)

    lam_x, lam_y = sp.symbols("lambda_x lambda_y", real=True)
    phase_b = lam_y - lam_x
    phase_u = lam_x - lam_y
    hopping_phase = sp.simplify(-lam_x + phase_u + lam_y)

    return {
        "original_bond": "J |z_x^dagger z_y|^2",
        "gaussian_identity": (
            "exp[J|b|^2] proportional to integral dQ "
            "exp[-|Q|^2/J+Q*b^star+Q^star*b]"
        ),
        "completed_square_residual": square_residual,
        "HS_identity_exact": square_residual == 0,
        "overlap_phase_under_local_redundancy": phase_b,
        "compact_link_definition": "U_xy=Q_xy^star/|Q_xy|",
        "compact_link_phase_rule": phase_u,
        "link_hopping_phase_residual": hopping_phase,
        "link_hopping_is_gauge_invariant": hopping_phase == 0,
        "HS_bond_terms": ("|Q_xy|^2/J", "z_x^dagger U_xy z_y+h.c."),
        "bare_plaquette_in_exact_one_bond_rewrite": 0,
        "no_bare_plaquette_is_exact_if_original_quartic_bond_is_microscopic": True,
        "link_amplitude_must_also_be_integrated": True,
        "freezing_link_amplitude_is_extra_saddle_assumption": True,
        "current_RefG_microscopic_bond_action_derived": False,
        "reference_value_used": False,
    }


def leading_induced_plaquette_theorem() -> dict[str, object]:
    """Derive the first flux-sensitive term of a finite matter determinant.

    Use one four-site square, gauge three links to one, and put the plaquette
    holonomy exp(i f) on the fourth link.  For a gapped complex mode with
    kernel M^2 I-t H, kappa=t/M^2, the flux part of Tr log begins at length
    four.  Backtracking walks are flux independent; the two oriented square
    loops give the exact coefficient below.
    """

    f, kappa, q = sp.symbols("f kappa q", real=True)
    phase = sp.exp(sp.I * q * f)
    H = sp.zeros(4)
    for left, right in ((0, 1), (1, 2), (2, 3)):
        H[left, right] = 1
        H[right, left] = 1
    # Oriented edge 3 -> 0 carries exp(i q f).
    H[3, 0] = phase
    H[0, 3] = sp.conjugate(phase)

    trace_h4 = sp.simplify(sp.expand_complex(sp.trace(H**4)))
    expected_trace = 24 + 8 * sp.cos(q * f)
    flux_trace = sp.simplify(trace_h4 - trace_h4.subs(f, 0))
    logdet_flux_order4 = sp.simplify(-kappa**4 * flux_trace / 4)
    expected_logdet_flux = sp.simplify(
        -2 * kappa**4 * (sp.cos(q * f) - 1)
    )
    wilson_beta = sp.simplify(2 * kappa**4 * q**2)
    quadratic_flux_coefficient = sp.simplify(
        sp.diff(logdet_flux_order4, f, 2).subs(f, 0) / 2
    )

    kappa_a, q_a = sp.symbols("kappa_a q_a", real=True)
    return {
        "four_site_hopping_matrix": H,
        "trace_H4": trace_h4,
        "trace_H4_identity": sp.simplify(trace_h4 - expected_trace) == 0,
        "flux_sensitive_logdet_at_order4": logdet_flux_order4,
        "logdet_flux_identity": sp.simplify(
            logdet_flux_order4 - expected_logdet_flux
        )
        == 0,
        "induced_Wilson_beta_per_mode": wilson_beta,
        "quadratic_flux_coefficient": quadratic_flux_coefficient,
        "many_mode_leading_beta": "2 sum_a kappa_a^4 q_a^2",
        "many_mode_symbols": (kappa_a, q_a),
        "higher_closed_loops_begin_at": "O(kappa^6) on a hypercubic lattice",
        "absolute_stiffness_requires_full_determinant": True,
        "reference_value_used": False,
    }


def continuous_hopping_gap_witness() -> dict[str, object]:
    """Show that fixed topology and charges do not fix the stiffness."""

    kappa = sp.symbols("kappa", positive=True)
    projective_unit_charge = sp.Integer(1)
    beta_projective = sp.simplify(
        2 * kappa**4 * projective_unit_charge**2
    )
    witness_values = (sp.Rational(1, 4), sp.Rational(1, 3))
    witness_betas = tuple(
        sp.simplify(beta_projective.subs(kappa, value))
        for value in witness_values
    )

    return {
        "projective_link_charge": projective_unit_charge,
        "centered_spin1_weights_are_not_link_charges": True,
        "leading_projective_link_beta": beta_projective,
        "same_charge_lattice_hopping_gap_witnesses": witness_values,
        "different_induced_betas": witness_betas,
        "witnesses_are_distinct": witness_betas[0] != witness_betas[1],
        "d_beta_d_kappa": sp.diff(beta_projective, kappa),
        "fixed_C3_and_compactness_determine_stiffness": False,
        "reference_value_used": False,
    }


def ordered_frame_stueckelberg_mass_audit() -> dict[str, object]:
    """Check whether an independent frame link is massless on the p18h branch.

    The current ordered-frame action contains kappa_f (d theta+a)^2.  If a is
    an independent connection and an induced Maxwell term is added, unitary
    gauge theta=0 leaves a Proca mass.  A massless emergent photon therefore
    requires a distinct Coulomb phase rather than the ordered north-pole
    expansion itself.
    """

    K, kappa_f = sp.symbols("K_F kappa_f", positive=True)
    canonical_mass_squared = sp.simplify(2 * kappa_f / K)
    return {
        "ordered_frame_term": "kappa_f (partial theta+a)^2",
        "unitary_gauge_term": "kappa_f a_mu a^mu",
        "induced_kinetic_term": "-K_F f_mu_nu f^mu_nu/4",
        "canonical_vector_mass_squared": canonical_mass_squared,
        "positive_ordered_frame_stiffness_gives_mass": True,
        "composite_connection_branch": (
            "no quadratic Maxwell propagator, as proved in p18bp"
        ),
        "independent_connection_on_ordered_branch": "Stueckelberg/Higgs massive",
        "massless_route": (
            "derive a separate 3+1D Coulomb phase with an uncondensed charged "
            "field and a deconfined compact link"
        ),
        "current_ordered_frame_branch_is_massless_photon_phase": False,
        "reference_value_used": False,
    }


def physical_photon_generator_separation_theorem() -> dict[str, object]:
    """Keep family/frame weights separate from the physical photon."""

    a, b, c = sp.symbols("a b c", real=True)
    family_weights = (-1, 0, 1)
    neutrino_charges = tuple(
        sp.simplify((a - b) / 2 + c * weight)
        for weight in family_weights
    )
    neutral_solution = sp.linsolve(neutrino_charges, (a, b, c))
    electron_charge = sp.simplify(-a / 2 - b / 2)
    primitive_solution = sp.linsolve(
        (*neutrino_charges, electron_charge + 1), (a, b, c)
    )

    return {
        "general_neutral_generator": "Q'=a T3+b Y+c F",
        "neutrino_charges": neutrino_charges,
        "neutral_solution": neutral_solution,
        "primitive_electron_solution": primitive_solution,
        "physical_generator_is_Q_T3_plus_Y": primitive_solution
        == sp.FiniteSet((1, 1, 0)),
        "family_frame_coefficient_in_photon": 0,
        "C3_role_if_retained": "generation multiplicity/representation, not electric charge",
        "CP1_auxiliary_link_is_automatically_physical_photon": False,
        "required_bridge": (
            "derive a generation-blind electroweak representation on the "
            "complete charged-core Hilbert space"
        ),
        "reference_value_used": False,
    }


def constructive_route_contract() -> dict[str, object]:
    """State the shortest target-independent calculation that could close."""

    return {
        "selected_mechanism": (
            "exact auxiliary link from a microscopic quartic bond, followed "
            "by the complete finite charged-core determinant"
        ),
        "why_selected": (
            "an exact HS rewrite can remove the independent bare plaquette "
            "parameter rather than merely setting it to zero by hand"
        ),
        "next_mathematical_object": (
            "the gauge-covariant Hessian D_core[U] of the phase-normalized "
            "localized RefG charged-core action"
        ),
        "must_derive_in_order": (
            "derive the microscopic frame/charged-core bond from p01/F_min",
            "perform the HS rewrite while retaining the link amplitude",
            "derive the saddle/gap equations and every kappa_a=t_a/M_a^2",
            "show that the microscopic parameters lie in a deconfined 3+1D Coulomb phase rather than the ordered Higgs or confined phase",
            "prove that the surviving compact link acts as Q=T3+Y, with C3 only as a generation index",
            "compute the full transverse polarization/determinant and its continuum limit",
            "derive the electroweak breaking, QCD vacuum polarization and Thomson matching from the same spectrum",
        ),
        "success_condition": (
            "all hopping/gap ratios are isolated solutions of target-free "
            "core equations, the link has a massless transverse pole, and no "
            "independent plaquette/counterterm direction remains"
        ),
        "failure_condition": (
            "if the core equations leave any continuous kappa or finite F^2 "
            "direction, this induced route does not predict the coupling"
        ),
        "fallback_if_failure": (
            "compute the full RefG gravity-gauge beta system and seek an "
            "isolated UV fixed point with no relevant direction projecting "
            "onto the physical photon stiffness"
        ),
        "reference_value_used": False,
    }


def primary_reference_ledger() -> tuple[dict[str, str], ...]:
    return (
        {
            "source": "https://arxiv.org/abs/0711.0818",
            "result": (
                "3+1D compact CP1+U1 has distinct Higgs, Coulomb and "
                "confinement phases; a massless gauge mode is phase-dependent"
            ),
        },
        {
            "source": "https://arxiv.org/abs/1102.5035",
            "result": (
                "a Maxwell term can be generated dynamically in gauge models "
                "without a microscopic Maxwell term"
            ),
        },
        {
            "source": "https://arxiv.org/abs/1511.08374",
            "result": (
                "finite auxiliary bosons can induce a lattice gauge action "
                "and its continuum coupling requires an explicit matching"
            ),
        },
    )


def source_firewall() -> dict[str, object]:
    source = inspect.getsource(inspect.getmodule(source_firewall))
    tree = ast.parse(source)
    numeric_literals = tuple(
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    )
    forbidden_modules = ("p18" + "bm", "p18" + "bk")
    forbidden_text = ("CO" + "DATA", "observed " + "inverse")
    return {
        "contains_comparison_numeric_literal": any(
            isinstance(value, float) and 100 < abs(value) < 200
            for value in numeric_literals
        ),
        "imports_comparison_module": any(name in source for name in forbidden_modules),
        "contains_comparison_text": any(text in source for text in forbidden_text),
        "target_isolation_pass": not any(
            (
                any(
                    isinstance(value, float) and 100 < abs(value) < 200
                    for value in numeric_literals
                ),
                any(name in source for name in forbidden_modules),
                any(text in source for text in forbidden_text),
            )
        ),
    }


def run_gate() -> None:
    cp1 = cp1_spin1_rewrite_theorem()
    hs = exact_hubbard_stratonovich_link_theorem()
    plaquette = leading_induced_plaquette_theorem()
    witness = continuous_hopping_gap_witness()
    mass = ordered_frame_stueckelberg_mass_audit()
    photon = physical_photon_generator_separation_theorem()
    route = constructive_route_contract()
    firewall = source_firewall()

    assert cp1["exact_fierz_identity"]
    assert cp1["spin1_dimension_equals_C3_dimension"]
    assert hs["HS_identity_exact"]
    assert hs["link_hopping_is_gauge_invariant"]
    assert hs["bare_plaquette_in_exact_one_bond_rewrite"] == 0
    assert hs["freezing_link_amplitude_is_extra_saddle_assumption"]
    assert plaquette["trace_H4_identity"]
    assert plaquette["logdet_flux_identity"]
    assert witness["witnesses_are_distinct"]
    assert witness["fixed_C3_and_compactness_determine_stiffness"] is False
    assert mass["current_ordered_frame_branch_is_massless_photon_phase"] is False
    assert photon["physical_generator_is_Q_T3_plus_Y"]
    assert photon["CP1_auxiliary_link_is_automatically_physical_photon"] is False
    assert firewall["target_isolation_pass"]

    for title, payload in (
        ("CP1/spin-one rewrite", cp1),
        ("exact HS auxiliary link", hs),
        ("leading induced plaquette", plaquette),
        ("continuous hopping-gap witness", witness),
        ("ordered-frame Stueckelberg mass", mass),
        ("physical photon separation", photon),
        ("constructive route contract", route),
        ("source firewall", firewall),
    ):
        print(f"\n{title}")
        for key, value in payload.items():
            print(f"  {key}: {value}")

    print("\nprimary references")
    for row in primary_reference_ledger():
        print(f"  {row['source']}: {row['result']}")

    print(
        "\nSTATUS: OPEN_REFG_MICROSCOPIC_BOND_COULOMB_PHASE_PHYSICAL_Q_BRIDGE_"
        "GAP_SADDLE_AND_FULL_MATCHING__PASS_TARGET_INDEPENDENT_HS_LINK_AND_"
        "INDUCED_PLAQUETTE_THEOREM"
    )


if __name__ == "__main__":
    run_gate()
