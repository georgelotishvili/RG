from __future__ import annotations

"""PHASE 18bt: substrate-node flux--photon spectral alpha gate.

This gate tests the most direct lattice-native interpretation of a
dimensionless electromagnetic coupling.  On a periodic cubic node network,
declare a Gaussian compact-U(1) Coulomb Hamiltonian

    H = (U/2) sum_links E_l^2 + (K/2) sum_plaquettes B_p^2.

Compactness fixes the primitive integer flux sector.  The ratio between the
energy of that sector and the lowest transverse-photon energy has a finite
continuum limit.  In the standard charge-lattice normalization that limit is
g^2/(4 pi): the fine-structure constant of the declared compact U(1) at that
scale.  It becomes electromagnetic alpha only after the primitive sector is
derived as the physical Q=T3+Y charge.  When the Hamiltonian is an infrared
effective description, U and K are the renormalized Coulomb-phase
coefficients, not microscopic bare rotor parameters.

The result is target independent.  It does not derive the Hamiltonian, its
dimensionless electric/magnetic shape U/K, a deconfined photon phase, the
physical Q=T3+Y bridge, or the running to the Thomson limit from the current
RefG action.  It identifies the precise spectral quantity that a substrate
node theory would have to calculate without using an electromagnetic target.
"""

import ast
import inspect

import sympy as sp


def compact_primitive_flux_normalization_theorem() -> dict[str, object]:
    """Fix the electric normalization by the compact holonomy period."""

    theta = sp.symbols("theta", real=True)
    m = sp.symbols("m", integer=True)
    u, k, lam, flux_period = sp.symbols(
        "U K lambda Phi", positive=True
    )
    wave = sp.exp(sp.I * m * theta)
    period_residual = sp.simplify(wave.subs(theta, theta + 2 * sp.pi) / wave)
    primitive_charge = 2 * sp.pi / flux_period
    general_alpha = sp.simplify(
        primitive_charge**2 * sp.sqrt(u / k) / (4 * sp.pi)
    )
    transformed_alpha = sp.simplify(
        (2 * sp.pi / (lam * flux_period)) ** 2
        * sp.sqrt((lam**2 * u) / (k / lam**2))
        / (4 * sp.pi)
    )

    return {
        "link_variable": "A_l modulo 2*pi",
        "noncontractible_holonomy": theta,
        "holonomy_period": 2 * sp.pi,
        "flux_wavefunction": wave,
        "large_gauge_period_residual": period_residual,
        "allowed_global_electric_flux": "m in Z",
        "electric_flux_object": "canonical electric displacement, not 2*pi magnetic flux",
        "primitive_nonzero_sector": 1,
        "higher_sector_energy_law": "Delta_E_flux(m)=m^2 Delta_E_flux(1)",
        "field_rescaling_freedom_after_primitive_charge_is_fixed": False,
        "general_period_primitive_charge": primitive_charge,
        "general_period_alpha": general_alpha,
        "field_redefinition": "A'=lambda*A, U'=lambda^2*U, K'=K/lambda^2, Phi'=lambda*Phi",
        "full_spectral_alpha_is_field_coordinate_invariant": sp.simplify(
            transformed_alpha - general_alpha
        )
        == 0,
        "reference_value_used": False,
    }


def gaussian_torus_flux_energy_theorem() -> dict[str, object]:
    """Minimize the Gaussian electric energy in a fixed torus-flux sector.

    A sector carrying flux m through every transverse N-by-N plane has total
    x-link field sum N*m.  Cauchy--Schwarz over the N^3 parallel links gives
    the exact Gaussian lower bound, saturated by the uniform zero mode.
    """

    n = sp.symbols("N", integer=True, positive=True)
    u = sp.symbols("U", positive=True)
    m = sp.symbols("m", integer=True)

    parallel_links = n**3
    transverse_links_per_plane = n**2
    total_field_sum = n * m
    uniform_field = sp.simplify(total_field_sum / parallel_links)
    cauchy_sum_square_bound = sp.simplify(total_field_sum**2 / parallel_links)
    electric_energy_bound = sp.simplify(u * cauchy_sum_square_bound / 2)
    uniform_energy = sp.simplify(u * parallel_links * uniform_field**2 / 2)
    primitive_gap = sp.simplify(electric_energy_bound.subs(m, 1))

    return {
        "periodic_lattice": "N^3 cubic torus",
        "parallel_link_count": parallel_links,
        "transverse_link_count_per_plane": transverse_links_per_plane,
        "sector_flux_per_plane": m,
        "total_parallel_field_sum": total_field_sum,
        "uniform_zero_mode_field": uniform_field,
        "cauchy_sum_E_squared_bound": cauchy_sum_square_bound,
        "minimum_flux_sector_energy": electric_energy_bound,
        "uniform_mode_saturates_bound": sp.simplify(
            uniform_energy - electric_energy_bound
        )
        == 0,
        "primitive_flux_gap": primitive_gap,
        "scope": (
            "globally Gaussian modes with compact harmonic zero mode, or the "
            "renormalized infrared Hamiltonian of a Coulomb phase"
        ),
        "strong_coupling_compact_rotor_string_energy_is_this_formula": False,
        "full_compact_interacting_phase_derived": False,
        "reference_value_used": False,
    }


def transverse_photon_gap_theorem() -> dict[str, object]:
    """Diagonalize the nearest-neighbour Gaussian transverse mode."""

    n = sp.symbols("N", integer=True, positive=True)
    u, k = sp.symbols("U K", positive=True)
    k_min = 2 * sp.pi / n
    laplacian_eigenvalue = sp.simplify(4 * sp.sin(k_min / 2) ** 2)
    omega_squared = sp.simplify(u * k * laplacian_eigenvalue)
    photon_gap = sp.simplify(2 * sp.sqrt(u * k) * sp.sin(sp.pi / n))

    return {
        "valid_size_domain": "integer N>=2",
        "minimum_valid_N": 2,
        "lowest_nonzero_momentum": k_min,
        "transverse_lattice_laplacian_eigenvalue": laplacian_eigenvalue,
        "photon_energy_gap_squared": omega_squared,
        "lowest_transverse_photon_gap": photon_gap,
        "dispersion_identity_pass": sp.simplify(photon_gap**2 - omega_squared)
        == 0,
        "polarizations": 2,
        "polarization_degeneracy_multiplies_one_photon_gap": False,
        "zero_total_momentum_two_photon_gap_used": False,
        "reference_value_used": False,
    }


def flux_photon_spectral_alpha_theorem() -> dict[str, object]:
    """Derive the finite-volume estimator and its continuum limit."""

    n = sp.symbols("N", integer=True, positive=True)
    n_cont = sp.symbols("N_cont", positive=True)
    u, k = sp.symbols("U K", positive=True)
    g, a, hbar, v = sp.symbols("g a hbar v", positive=True)

    flux_gap = u / (2 * n)
    photon_gap = 2 * sp.sqrt(u * k) * sp.sin(sp.pi / n)
    raw_ratio = sp.simplify(flux_gap / photon_gap)
    continuum_ratio = sp.simplify(
        sp.limit(
            sp.sqrt(u) / (4 * sp.sqrt(k) * n_cont * sp.sin(sp.pi / n_cont)),
            n_cont,
            sp.oo,
        )
    )
    finite_volume_corrected_ratio = sp.simplify(
        raw_ratio * n * sp.sin(sp.pi / n) / sp.pi
    )

    length = n * a
    emergent_speed = a * sp.sqrt(u * k) / hbar
    effective_g_squared = sp.sqrt(u) / sp.sqrt(k)
    continuum_flux_gap = sp.simplify(
        hbar * emergent_speed * effective_g_squared / (2 * length)
    )
    continuum_photon_gap = sp.simplify(
        2 * sp.pi * hbar * emergent_speed / length
    )
    speed_independent_ratio = sp.simplify(
        continuum_flux_gap / continuum_photon_gap
    )

    u_ks = hbar * v * g**2 / a
    k_ks = hbar * v / (g**2 * a)
    standard_alpha = g**2 / (4 * sp.pi)
    normalized_ratio = sp.simplify(
        continuum_ratio.subs({u: u_ks, k: k_ks})
    )

    return {
        "primitive_flux_gap": flux_gap,
        "lowest_photon_gap": photon_gap,
        "raw_finite_N_spectral_ratio": raw_ratio,
        "continuum_spectral_ratio": continuum_ratio,
        "exact_finite_volume_corrected_ratio": finite_volume_corrected_ratio,
        "emergent_photon_speed": emergent_speed,
        "continuum_primitive_flux_gap": continuum_flux_gap,
        "continuum_photon_gap": continuum_photon_gap,
        "speed_independent_continuum_ratio": speed_independent_ratio,
        "emergent_speed_cancels": sp.simplify(
            speed_independent_ratio - continuum_ratio
        )
        == 0,
        "standard_charge_lattice_U": u_ks,
        "standard_charge_lattice_K": k_ks,
        "normalization_unit_convention": "U and K are energies; v=a*sqrt(U*K)/hbar",
        "standard_alpha_at_declared_Coulomb_scale": standard_alpha,
        "normalized_spectral_ratio": normalized_ratio,
        "spectral_ratio_equals_alpha_at_declared_scale": sp.simplify(
            normalized_ratio - standard_alpha
        )
        == 0,
        "operational_interpretation": (
            "the compact-U(1) alpha at the declared Coulomb scale is the "
            "continuum ratio of the primitive global electric-flux energy "
            "to the first transverse-photon energy"
        ),
        "identification_as_alpha_EM_requires_physical_Q_bridge": True,
        "microscopic_compact_model_requires_renormalized_coefficients": True,
        "N_to_infinity_scope": (
            "long-wavelength or large-volume limit of the Gaussian effective "
            "theory; not by itself an interacting microscopic continuum limit"
        ),
        "reference_value_used": False,
    }


def common_transposition_and_shape_theorem() -> dict[str, object]:
    """Separate an invisible common scale from the alpha-setting shape."""

    n = sp.symbols("N", integer=True, positive=True)
    u0, k0, s, lam = sp.symbols("U0 K0 s lambda", positive=True)

    u = s * lam * u0
    k = s * k0 / lam
    flux_gap = sp.simplify(u / (2 * n))
    photon_gap = sp.simplify(2 * sp.sqrt(u * k) * sp.sin(sp.pi / n))
    corrected_ratio = sp.simplify(
        (flux_gap / photon_gap) * n * sp.sin(sp.pi / n) / sp.pi
    )

    common_only_ratio = sp.simplify(corrected_ratio.subs(lam, 1))
    base_ratio = sp.sqrt(u0 / k0) / (4 * sp.pi)
    photon_shape_residual = sp.simplify(sp.sqrt(u * k) - s * sp.sqrt(u0 * k0))

    a, rho, g = sp.symbols("a rho g", positive=True)
    alpha_at_a = sp.simplify(
        sp.sqrt((g**2 / a) / (1 / (g**2 * a))) / (4 * sp.pi)
    )
    alpha_at_rescaled_a = sp.simplify(
        sp.sqrt((g**2 / (rho * a)) / (1 / (g**2 * rho * a)))
        / (4 * sp.pi)
    )

    return {
        "electric_coefficient": u,
        "magnetic_ring_coefficient": k,
        "common_energy_transposition": s,
        "dimensionless_electric_magnetic_shape": lam,
        "primitive_flux_gap": flux_gap,
        "photon_gap": photon_gap,
        "finite_volume_corrected_ratio": corrected_ratio,
        "common_transposition_cancels": sp.simplify(
            common_only_ratio - base_ratio
        )
        == 0,
        "photon_gap_is_shape_blind_under_dual_deformation": photon_shape_residual
        == 0,
        "alpha_changes_with_internal_shape": sp.simplify(
            sp.diff(corrected_ratio, lam)
        )
        != 0,
        "lattice_spacing_cancels": sp.simplify(
            alpha_at_rescaled_a - alpha_at_a
        )
        == 0,
        "refg_readout_bridge": (
            "compatible with the p10 common-tempo transposition and its "
            "frequency-ratio invariance; that ledger does not determine lambda"
        ),
        "not_the_same_operation_as": (
            "multiplying a quantum action at fixed hbar while leaving the time "
            "standard unchanged"
        ),
        "sharp_conclusion": (
            "a uniform weakening of every node Hamiltonian energy scale is "
            "invisible to alpha; the relative electric-versus-ring shape is not"
        ),
        "reference_value_used": False,
    }


def primitive_charge_and_physical_q_bridge_audit() -> dict[str, object]:
    """Keep topology, flux normalization, and physical charge distinct."""

    return {
        "compactness_fixes_integer_flux_lattice": True,
        "primitive_sector_fixes_field_normalization": True,
        "higher_flux_sector_scales_as_m_squared": True,
        "C3_can_label_generation_or_representation_structure": True,
        "C3_alone_fixes_U_over_K": False,
        "h2_oriented_closure_alone_fixes_U_over_K": False,
        "q_rare_has_the_required_dimensionless_transposition_invariance": True,
        "q_rare_is_currently_linked_to_physical_Maxwell_charge": False,
        "physical_photon_generator_required": "Q=T3+Y",
        "primitive_node_flux_is_derived_as_primitive_electron_charge": False,
        "best_candidate_reason": (
            "it measures the compact node network by two physical spectral "
            "gaps and is independent of arbitrary field coordinates"
        ),
        "reference_value_used": False,
    }


def refg_node_hamiltonian_derivability_audit() -> dict[str, object]:
    """State exactly what remains before the spectral invariant predicts a number."""

    return {
        "declared_candidate_Hamiltonian": (
            "H=(U/2) sum E_l^2+(K/2) sum B_p^2 on a periodic node network"
        ),
        "Hamiltonian_derived_from_current_Fmin": False,
        "local_node_Hilbert_space_and_Gauss_constraint_derived": False,
        "deconfined_3plus1D_Coulomb_phase_derived": False,
        "primitive_flux_to_physical_Q_bridge_derived": False,
        "dimensionless_shape_U_over_K_derived": False,
        "renormalized_Coulomb_stiffness_from_microscopic_nodes_derived": False,
        "charged_core_spectrum_and_vacuum_polarization_derived": False,
        "running_to_Thomson_limit_derived": False,
        "current_numeric_alpha_prediction": False,
        "closed_result": (
            "for the declared Gaussian Coulomb Hamiltonian, alpha at that "
            "scale is exactly the primitive-flux/photon spectral ratio"
        ),
        "next_strict_calculation": (
            "derive one microscopic node Hamiltonian with its Gauss law, "
            "primitive physical-Q defect, ring amplitude and unique vacuum; "
            "then compute U/K without an electromagnetic target and run the "
            "derived charged spectrum to the Thomson limit"
        ),
        "reference_value_used": False,
    }


def primary_reference_ledger() -> tuple[dict[str, str], ...]:
    return (
        {
            "source": "https://arxiv.org/abs/2009.04499",
            "result": (
                "an emergent U(1) medium can extract electric coupling from "
                "global flux-sector energies and photon speed from its spectrum"
            ),
        },
        {
            "source": "https://doi.org/10.1103/PhysRevD.11.395",
            "result": (
                "Hamiltonian compact lattice gauge theory supplies the electric "
                "and plaquette normalization used by the conditional witness"
            ),
        },
        {
            "source": "https://arxiv.org/abs/cond-mat/0407140",
            "result": (
                "local bosonic/string-net systems can support emergent photons "
                "and charged excitations in a deconfined phase"
            ),
        },
        {
            "source": "https://arxiv.org/abs/cond-mat/0305401",
            "result": (
                "a deconfined three-dimensional U(1) phase has plane-flux "
                "sectors whose harmonic energy spreads uniformly and scales as 1/L"
            ),
        },
        {
            "source": "https://arxiv.org/abs/hep-lat/0311006",
            "result": (
                "the Coulomb-phase helicity modulus measures a renormalized, "
                "nonuniversal electromagnetic coupling"
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
    forbidden_text = ("CO" + "DATA", "observed " + "inverse", "13" + "7.")
    comparison_float = any(
        isinstance(value, float) and 100 < abs(value) < 200
        for value in numeric_literals
    )
    comparison_module = any(name in source for name in forbidden_modules)
    comparison_text = any(text in source for text in forbidden_text)
    return {
        "contains_comparison_numeric_literal": comparison_float,
        "imports_comparison_module": comparison_module,
        "contains_comparison_text": comparison_text,
        "target_isolation_pass": not (
            comparison_float or comparison_module or comparison_text
        ),
    }


def run_gate() -> None:
    compact = compact_primitive_flux_normalization_theorem()
    flux = gaussian_torus_flux_energy_theorem()
    photon = transverse_photon_gap_theorem()
    spectral = flux_photon_spectral_alpha_theorem()
    scaling = common_transposition_and_shape_theorem()
    charge = primitive_charge_and_physical_q_bridge_audit()
    refg = refg_node_hamiltonian_derivability_audit()
    firewall = source_firewall()

    assert compact["large_gauge_period_residual"] == 1
    assert compact["primitive_nonzero_sector"] == 1
    assert compact["full_spectral_alpha_is_field_coordinate_invariant"]
    assert flux["uniform_mode_saturates_bound"]
    assert flux["primitive_flux_gap"] == sp.symbols("U", positive=True) / (
        2 * sp.symbols("N", integer=True, positive=True)
    )
    assert photon["dispersion_identity_pass"]
    assert photon["minimum_valid_N"] == 2
    assert sp.simplify(
        spectral["continuum_spectral_ratio"]
        - sp.sqrt(
            sp.symbols("U", positive=True) / sp.symbols("K", positive=True)
        )
        / (4 * sp.pi)
    ) == 0
    assert spectral["spectral_ratio_equals_alpha_at_declared_scale"]
    assert spectral["emergent_speed_cancels"]
    assert scaling["common_transposition_cancels"]
    assert scaling["photon_gap_is_shape_blind_under_dual_deformation"]
    assert scaling["alpha_changes_with_internal_shape"]
    assert scaling["lattice_spacing_cancels"]
    assert charge["q_rare_is_currently_linked_to_physical_Maxwell_charge"] is False
    for open_key in (
        "Hamiltonian_derived_from_current_Fmin",
        "local_node_Hilbert_space_and_Gauss_constraint_derived",
        "deconfined_3plus1D_Coulomb_phase_derived",
        "primitive_flux_to_physical_Q_bridge_derived",
        "dimensionless_shape_U_over_K_derived",
        "renormalized_Coulomb_stiffness_from_microscopic_nodes_derived",
        "charged_core_spectrum_and_vacuum_polarization_derived",
        "running_to_Thomson_limit_derived",
    ):
        assert refg[open_key] is False
    assert refg["current_numeric_alpha_prediction"] is False
    assert firewall["target_isolation_pass"]

    for title, payload in (
        ("compact primitive-flux normalization", compact),
        ("Gaussian torus flux energy", flux),
        ("transverse photon gap", photon),
        ("flux-photon spectral alpha", spectral),
        ("common transposition versus internal shape", scaling),
        ("primitive charge and physical-Q bridge", charge),
        ("RefG node-Hamiltonian derivability", refg),
        ("source firewall", firewall),
    ):
        print(f"\n{title}")
        for key, value in payload.items():
            print(f"  {key}: {value}")

    print("\nprimary references")
    for row in primary_reference_ledger():
        print(f"  {row['source']}: {row['result']}")

    print(
        "\nSTATUS: OPEN_MICROSCOPIC_COMPACT_NODE_HAMILTONIAN_COULOMB_PHASE_"
        "RENORMALIZED_U_OVER_K_PRIMITIVE_PHYSICAL_Q_BRIDGE_ALPHA_SELECTION_"
        "CHARGED_SPECTRUM_AND_THOMSON_RUNNING__PASS_TARGET_INDEPENDENT_"
        "GAUSSIAN_COULOMB_TORUS_PRIMITIVE_FLUX_PHOTON_NORMALIZATION_COMMON_"
        "TRANSPOSITION_CANCELLATION_AND_INTERNAL_SHAPE_THEOREM"
    )


if __name__ == "__main__":
    run_gate()
