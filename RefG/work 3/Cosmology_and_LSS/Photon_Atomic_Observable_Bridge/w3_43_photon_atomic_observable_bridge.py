"""Exact verifier for the conditional photon--atomic observable bridge.

The program reads only pinned local dependency files, reads no data, performs
no fit, writes no files, and emits one deterministic JSON report on stdout.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path

import sympy as sp


CLAIM_ID = "W3_43_PHOTON_ATOMIC_OBSERVABLE_BRIDGE"
MODEL_VERSION = "W3-COSMOLOGY-v1.2-PHOTON-ATOMIC-OBSERVABLE-BRIDGE"
PASS_STATUS = (
    "PASS_CONDITIONAL_IDEAL_OBSERVABLE_MAP__"
    "ASTROPHYSICAL_FORWARD_MODEL_AND_DATA_TEST_OPEN"
)

EXPECTED_PREREG_SHA256 = (
    "20793b696e7fcd64a0a4f9a575b4091eeb2faf651973448b87b2c025b2d258da"
)
EXPECTED_BACKGROUND_SHA256 = (
    "57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055"
)
OPTICAL_REGISTRY = (
    "comoving_universal_local_atomic_proper_frequency",
    "minimally_coupled_Maxwell_geometric_optics",
    "transparent_photon_number_conserving_transport",
)
IDEAL_SOURCE_REGISTRY = (
    "local_proper_isotropic_or_isotropic_equivalent_bolometric_source_power",
    "ideal_bolometric_operational_flux_measurement",
)
FREEDOM_LEDGER = (
    "H_A0",
    "Omega_m0",
    "Omega_r0",
)
EXPECTED_OPTICAL_REGISTRY = frozenset(
    {
        "comoving_universal_local_atomic_proper_frequency",
        "minimally_coupled_Maxwell_geometric_optics",
        "transparent_photon_number_conserving_transport",
    }
)
EXPECTED_IDEAL_SOURCE_REGISTRY = frozenset(
    {
        "local_proper_isotropic_or_isotropic_equivalent_bolometric_source_power",
        "ideal_bolometric_operational_flux_measurement",
    }
)
EXPECTED_FREEDOM_LEDGER = frozenset(
    {
        "H_A0",
        "Omega_m0",
        "Omega_r0",
    }
)

REQUIRED_TRUE_FLAGS = (
    "upstream_background_pass_verified",
    "operational_scale_time_dictionary_exact",
    "pinned_dependency_hashes_exact",
    "operational_metric_branch_pinned",
    "minimal_Maxwell_branch_selected",
    "local_atomic_proper_frequency_selected",
    "transparent_photon_number_transport_selected",
    "generic_atomic_chronometer_boundary_exact",
    "photon_null_geodesic_exact",
    "photon_frequency_transport_exact",
    "coordinate_cadence_cancellation_exact",
    "spectroscopic_redshift_exact",
    "arrival_time_dilation_exact",
    "kinematic_Hubble_map_exact",
    "redshift_background_substitution_exact",
    "comoving_distance_exact",
    "angular_diameter_distance_exact",
    "photon_flux_ledger_exact",
    "Etherington_reciprocity_exact",
    "luminosity_distance_exact",
    "distance_modulus_definition_exact",
    "low_redshift_Hubble_slope_exact",
    "finite_optical_registry_complete",
    "finite_ideal_source_registry_complete",
    "finite_freedom_ledger_complete",
    "mutation_controls_pass",
    "schema_keysets_exact",
)

REQUIRED_FALSE_FLAGS = (
    "Maxwell_sector_derived_from_foundation",
    "atomic_spectrum_derived_from_foundation",
    "nonmetric_or_opacity_branches_excluded_by_data",
    "stellar_population_clock_derived",
    "supernova_intrinsic_luminosity_derived",
    "survey_selection_and_likelihood_supplied",
    "numerical_background_calibrated",
    "H_A0_identified_with_specific_measured_H0",
    "observational_data_fit_performed",
    "observational_pass",
)

EXPECTED_RESIDUAL_KEYS = frozenset(
    {
        "affine_frequency_invariant",
        "affine_endpoint_frequency_ratio",
        "angular_diameter_endpoint",
        "angular_diameter_normalized",
        "arrival_time_dilation",
        "atomic_coordinate_endpoint_ratio",
        "christoffel_chi_tauchi",
        "christoffel_tau_chichi",
        "chronometer_clock_boundary",
        "comoving_covector_invariant",
        "comoving_distance_A_anchor",
        "comoving_distance_A_lower_derivative",
        "comoving_distance_A_upper_derivative",
        "comoving_distance_change_of_variable",
        "comoving_distance_z_anchor",
        "comoving_distance_z_derivative",
        "coordinate_ratio_cancellation",
        "distance_duality_endpoint",
        "distance_modulus_definition",
        "eikonal_frequency_transport",
        "eikonal_null_dispersion",
        "endpoint_atomic_factorization",
        "endpoint_coordinate_dimensionless_ratio",
        "endpoint_frequency_ratio",
        "Etherington_reciprocity",
        "foundation_null_dictionary",
        "frequency_arrival_consistency",
        "generic_atomic_endpoint_factorization",
        "generic_atomic_Hubble_map",
        "generic_present_redshift_boundary",
        "geodesic_null_constraint",
        "ideal_present_Hubble",
        "kinematic_Hubble_map",
        "low_redshift_Hubble_slope",
        "luminosity_distance_anchor",
        "luminosity_distance_derivative",
        "luminosity_distance_endpoint_geometry",
        "luminosity_distance_flux_square",
        "luminosity_distance_normalized",
        "luminosity_distance_routes",
        "neighboring_null_fronts",
        "operational_scale_rate_pullback",
        "operational_space_metric_pullback",
        "process_time_metric_pullback",
        "photon_coordinate_endpoint_ratio",
        "photon_flux_ledger",
        "present_background_normalization",
        "redshift_background_substitution",
        "selected_atomic_branch_recovery",
        "selected_g1_redshift_recovery",
        "sphere_area_geometry",
        "spectroscopic_redshift",
    }
)
EXPECTED_MUTATION_KEYS = frozenset(
    {
        "extra_endpoint_cadence_factor",
        "omitted_chronometer_clock_factor",
        "omitted_generic_atomic_drift",
        "missing_arrival_rate_flux_loss",
        "retired_z_times_one_plus_z_distance",
        "wrong_A_inverse_square_photon_law",
        "wrong_single_factor_distance_duality",
    }
)
EXPECTED_CLOSURE_FLAG_KEYS = frozenset(
    {
        "upstream_background_pass_verified",
        "operational_scale_time_dictionary_exact",
        "pinned_dependency_hashes_exact",
        "operational_metric_branch_pinned",
        "minimal_Maxwell_branch_selected",
        "local_atomic_proper_frequency_selected",
        "transparent_photon_number_transport_selected",
        "generic_atomic_chronometer_boundary_exact",
        "photon_null_geodesic_exact",
        "photon_frequency_transport_exact",
        "coordinate_cadence_cancellation_exact",
        "spectroscopic_redshift_exact",
        "arrival_time_dilation_exact",
        "kinematic_Hubble_map_exact",
        "redshift_background_substitution_exact",
        "comoving_distance_exact",
        "angular_diameter_distance_exact",
        "photon_flux_ledger_exact",
        "Etherington_reciprocity_exact",
        "luminosity_distance_exact",
        "distance_modulus_definition_exact",
        "low_redshift_Hubble_slope_exact",
        "finite_optical_registry_complete",
        "finite_ideal_source_registry_complete",
        "finite_freedom_ledger_complete",
        "mutation_controls_pass",
        "schema_keysets_exact",
        "Maxwell_sector_derived_from_foundation",
        "atomic_spectrum_derived_from_foundation",
        "nonmetric_or_opacity_branches_excluded_by_data",
        "stellar_population_clock_derived",
        "supernova_intrinsic_luminosity_derived",
        "survey_selection_and_likelihood_supplied",
        "numerical_background_calibrated",
        "H_A0_identified_with_specific_measured_H0",
        "observational_data_fit_performed",
        "observational_pass",
        "conditional_ideal_observable_map_pass",
    }
)
EXPECTED_DEPENDENCY_HASH_KEYS = frozenset(
    {
        "preregistration",
        "upstream_background_source",
    }
)
EXPECTED_REPORT_KEYS = frozenset(
    {
        "schema_version",
        "claim_id",
        "model_version",
        "decision_status",
        "data_role",
        "writes_files",
        "optical_registry",
        "ideal_source_registry",
        "freedom_ledger",
        "freedoms_derived_from_ideal_map",
        "required_true_flags",
        "required_false_flags",
        "closure_flags",
        "residuals",
        "mutation_residuals",
        "mutation_detection",
        "ideal_observable_map",
        "generic_atomic_clock_boundary",
        "forward_model_open",
        "dependency_hashes",
        "dependency_hashes_exact",
        "canonical_dependency_text",
        "upstream_background_status",
        "runtime",
        "source_sha256",
    }
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_lf(path: Path) -> bool:
    raw = path.read_bytes()
    return (
        not raw.startswith(b"\xef\xbb\xbf")
        and b"\r" not in raw
        and raw.endswith(b"\n")
        and not raw.endswith(b"\n\n")
    )


def _zero(expression: sp.Expr) -> bool:
    return sp.simplify(expression) == 0


def _nonzero(expression: sp.Expr) -> bool:
    return sp.simplify(expression) != 0


def _load_read_only_report(
    path: Path, module_name: str
) -> dict[str, object]:
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load pinned upstream background verifier.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_report()


def _symbolic_checks() -> tuple[
    dict[str, sp.Expr],
    dict[str, sp.Expr],
    frozenset[str],
]:
    """Return exact residuals, negative mutations, and actual freedoms."""

    A, A_e, A_o = sp.symbols("A A_e A_o", positive=True)
    A_tau = sp.symbols("A_tau", real=True)
    a = sp.symbols("a", positive=True)
    c0, H_A0 = sp.symbols("c0 H_A0", positive=True)
    Omega_m0, Omega_r0 = sp.symbols(
        "Omega_m0 Omega_r0", nonnegative=True
    )
    Omega_Lambda0 = 1 - Omega_m0 - Omega_r0

    # Self-contained pullback from the foundation-coordinate dictionary to
    # operational proper time and scale.
    foundation_t = sp.symbols("foundation_t", real=True)
    a_foundation = sp.Function("a_foundation")(foundation_t)
    p_foundation = sp.Function("p_foundation")(foundation_t)
    dt_dtau = 1 / p_foundation
    process_time_metric_pullback = (
        p_foundation**2 * dt_dtau**2 - 1
    )
    operational_space_metric_pullback = (
        a_foundation**2 / p_foundation**2
        - (a_foundation / p_foundation) ** 2
    )
    operational_scale_rate_pullback = (
        sp.diff(sp.log(a_foundation / p_foundation), foundation_t)
        / p_foundation
        - (
            sp.diff(a_foundation, foundation_t) / a_foundation
            - sp.diff(p_foundation, foundation_t) / p_foundation
        )
        / p_foundation
    )

    q, K_tau, K_chi = sp.symbols("q K_tau K_chi", positive=True)
    nu_atom_e, nu_atom_o = sp.symbols(
        "nu_atom_e nu_atom_o", positive=True
    )
    delta_tau_e = sp.symbols("delta_tau_e", positive=True)

    # Derive the radial 1+1 Christoffel symbols directly from the metric.
    tau, chi_coordinate = sp.symbols("tau chi_coordinate", real=True)
    A_function = sp.Function("A")(tau)
    coordinates = (tau, chi_coordinate)
    metric = sp.diag(c0**2, -A_function**2)
    inverse_metric = sp.simplify(metric.inv())

    def christoffel(mu: int, alpha: int, beta: int) -> sp.Expr:
        return sp.simplify(
            sp.Rational(1, 2)
            * sum(
                inverse_metric[mu, nu]
                * (
                    sp.diff(metric[nu, beta], coordinates[alpha])
                    + sp.diff(metric[nu, alpha], coordinates[beta])
                    - sp.diff(metric[alpha, beta], coordinates[nu])
                )
                for nu in range(2)
            )
        )

    gamma_tau_chichi_function = christoffel(0, 1, 1)
    gamma_chi_tauchi_function = christoffel(1, 0, 1)
    metric_substitution = {
        A_function: A,
        sp.diff(A_function, tau): A_tau,
    }
    gamma_tau_chichi = sp.simplify(
        gamma_tau_chichi_function.subs(metric_substitution)
    )
    gamma_chi_tauchi = sp.simplify(
        gamma_chi_tauchi_function.subs(metric_substitution)
    )
    christoffel_tau_chichi = gamma_tau_chichi - A * A_tau / c0**2
    christoffel_chi_tauchi = gamma_chi_tauchi - A_tau / A

    # Homogeneous eikonal route. Build the null Hamilton-Jacobi equation
    # from the inverse metric, then solve its positive-frequency branch.
    omega_symbol = sp.symbols("omega_symbol", positive=True)
    inverse_metric_at_A = inverse_metric.subs(A_function, A)
    eikonal_covector = sp.Matrix([omega_symbol, q])
    eikonal_null_equation = sp.simplify(
        (
            eikonal_covector.T
            * inverse_metric_at_A
            * eikonal_covector
        )[0]
    )
    positive_omega_solutions = [
        solution
        for solution in sp.solve(
            sp.Eq(eikonal_null_equation, 0), omega_symbol
        )
        if solution.is_positive
    ]
    if len(positive_omega_solutions) != 1:
        raise RuntimeError("Positive eikonal frequency branch is not unique.")
    omega = positive_omega_solutions[0]
    eikonal_null_dispersion = eikonal_null_equation.subs(
        omega_symbol, omega
    )
    omega_A_derivative = sp.diff(omega, A)
    H_A = A_tau / A
    omega_tau = omega_A_derivative * A_tau
    eikonal_transport = omega_tau + H_A * omega

    omega_e = c0 * q / A_e
    omega_o = c0 * q / A_o
    endpoint_frequency_ratio = omega_o / omega_e - A_e / A_o

    # Independent affine-geodesic route. The positive spatial null branch is
    # solved from the metric, then inserted into the two geodesic equations.
    geodesic_null_equation = c0**2 * K_tau**2 - A**2 * K_chi**2
    positive_K_chi_solutions = [
        solution
        for solution in sp.solve(
            sp.Eq(geodesic_null_equation, 0), K_chi
        )
        if solution.is_positive
    ]
    if len(positive_K_chi_solutions) != 1:
        raise RuntimeError("Positive radial null branch is not unique.")
    K_chi_solution = positive_K_chi_solutions[0]
    geodesic_null_constraint = geodesic_null_equation.subs(
        K_chi, K_chi_solution
    )
    dK_tau_dlambda = -gamma_tau_chichi * K_chi_solution**2
    affine_frequency_invariant = (
        A_tau * K_tau**2 + A * dK_tau_dlambda
    )
    dK_chi_dlambda = (
        -2 * gamma_chi_tauchi * K_tau * K_chi_solution
    )
    comoving_covector_invariant = (
        2 * A * A_tau * K_tau * K_chi_solution
        + A**2 * dK_chi_dlambda
    )
    affine_momentum = sp.symbols("affine_momentum", positive=True)
    K_chi_from_covector = affine_momentum / A**2
    K_tau_symbol = sp.symbols("K_tau_symbol", positive=True)
    affine_null_with_covector = (
        c0**2 * K_tau_symbol**2
        - A**2 * K_chi_from_covector**2
    )
    positive_K_tau_solutions = [
        solution
        for solution in sp.solve(
            sp.Eq(affine_null_with_covector, 0), K_tau_symbol
        )
        if solution.is_positive
    ]
    if len(positive_K_tau_solutions) != 1:
        raise RuntimeError("Positive affine frequency branch is not unique.")
    K_tau_from_covector = positive_K_tau_solutions[0]
    affine_K_tau_e = K_tau_from_covector.subs(A, A_e)
    affine_K_tau_o = K_tau_from_covector.subs(A, A_o)
    affine_endpoint_frequency_ratio = (
        affine_K_tau_o / affine_K_tau_e - A_e / A_o
    )

    # Generic atomic endpoint factorization. The photon endpoint
    # frequency comes from the independently solved eikonal transport.
    nu_gamma_e = nu_atom_e
    nu_gamma_o = nu_gamma_e * (omega_o / omega_e)
    endpoint_factorization = (
        nu_atom_o / nu_gamma_o
        - (A_o / A_e) * (nu_atom_o / nu_atom_e)
    )
    spectroscopic_redshift = (
        nu_atom_o / nu_gamma_o - A_o / A_e
    ).subs(nu_atom_o, nu_atom_e)

    # Keep the generic atomic and stellar-clock boundary executable. Write
    # nu_A(A)=nu_A0/g(A), with g(1)=1, while
    # C(A)=d tau_SPS/d tau is an independently calibrated clock response.
    g_function = sp.Function("g")
    C_function = sp.Function("C")
    nu_A0 = sp.symbols("nu_A0", positive=True)
    g_Ae = g_function(A_e)
    g_Ao = g_function(A_o)
    nu_A_model_e = nu_A0 / g_Ae
    nu_A_model_o = nu_A0 / g_Ao
    nu_gamma_model_o = nu_A_model_e * (omega_o / omega_e)
    one_plus_z_generic_endpoint = (
        nu_A_model_o / nu_gamma_model_o
    )
    generic_atomic_endpoint_factorization = (
        one_plus_z_generic_endpoint
        - (A_o / A_e) * (g_Ae / g_Ao)
    )
    g_A = g_function(A)
    C_A = C_function(A)
    one_plus_z_generic = g_A / A
    generic_present_redshift_boundary = (
        one_plus_z_generic_endpoint
        .subs(A_o, 1)
        .subs(g_function(1), 1)
        .subs(A_e, A)
        - one_plus_z_generic
    )
    H_spec_from_definition = sp.simplify(
        -A_tau
        * sp.diff(one_plus_z_generic, A)
        / one_plus_z_generic
    )
    H_spec_closed_form = H_A * (
        1 - A * sp.diff(g_A, A) / g_A
    )
    generic_atomic_Hubble_map = (
        H_spec_from_definition - H_spec_closed_form
    )
    H_CC_from_definition = H_spec_from_definition / C_A
    chronometer_clock_boundary = (
        H_CC_from_definition - H_spec_closed_form / C_A
    )
    selected_atomic_branch_recovery = (
        H_spec_closed_form
        .subs(sp.diff(g_A, A), 0)
        .subs(g_A, 1)
        - H_A
    )
    selected_g1_redshift_recovery = (
        one_plus_z_generic.subs(g_A, 1) - A**-1
    )

    # The common foundation-coordinate cadence cancels at each endpoint.
    p_e = A_e ** sp.Rational(-3, 5)
    p_o = A_o ** sp.Rational(-3, 5)
    nu_atom_t_o = p_o * nu_atom_o
    nu_gamma_t_o = p_o * nu_gamma_o
    nu_atom_t_e = p_e * nu_atom_e
    nu_gamma_t_e = p_e * nu_gamma_e
    coordinate_ratio_cancellation = (
        nu_atom_t_o / nu_gamma_t_o - nu_atom_o / nu_gamma_o
    )
    photon_coordinate_endpoint_ratio = (
        (p_o * omega_o) / (p_e * omega_e)
        - (p_o / p_e) * (A_e / A_o)
    )
    atomic_coordinate_endpoint_ratio = (
        (p_o * nu_atom_o) / (p_e * nu_atom_e) - p_o / p_e
    ).subs(nu_atom_o, nu_atom_e)
    endpoint_coordinate_dimensionless_ratio = (
        (nu_atom_t_o / nu_gamma_t_o)
        / (nu_atom_t_e / nu_gamma_t_e)
        - (A_o / A_e) * (nu_atom_o / nu_atom_e)
    )

    # Neighboring radial null fronts. Solve their common-distance variation
    # for the observer interval rather than inserting the dilation target.
    delta_tau_o_symbol = sp.symbols(
        "delta_tau_o_symbol", positive=True
    )
    neighboring_null_equation = (
        delta_tau_o_symbol / A_o - delta_tau_e / A_e
    )
    delta_tau_o_solutions = sp.solve(
        sp.Eq(neighboring_null_equation, 0), delta_tau_o_symbol
    )
    if len(delta_tau_o_solutions) != 1:
        raise RuntimeError("Neighboring-null arrival branch is not unique.")
    delta_tau_o = delta_tau_o_solutions[0]
    neighboring_null_fronts = neighboring_null_equation.subs(
        delta_tau_o_symbol, delta_tau_o
    )
    arrival_time_dilation = (
        delta_tau_o / delta_tau_e - A_o / A_e
    )
    frequency_arrival_consistency = (
        delta_tau_e / delta_tau_o - omega_o / omega_e
    )

    # Present-normalized redshift and ideal kinematic expansion rate.
    z = sp.symbols("z", nonnegative=True)
    z_of_A = A**-1 - 1
    dz_dtau = sp.diff(z_of_A, A) * A_tau
    H_kin = -dz_dtau / (1 + z_of_A)
    kinematic_Hubble_map = H_kin - H_A

    E_A_squared = (
        Omega_r0 * A**-4
        + Omega_m0 * A**-3
        + Omega_Lambda0
    )
    E_z_squared = (
        Omega_r0 * (1 + z) ** 4
        + Omega_m0 * (1 + z) ** 3
        + Omega_Lambda0
    )
    redshift_background_substitution = (
        E_A_squared.subs(A, 1 / (1 + z)) - E_z_squared
    )
    present_normalization = E_z_squared.subs(z, 0) - 1

    # Radial null distance in endpoint A, normalized z, and the foundation
    # coordinate dictionary.
    v, u = sp.symbols("v u", positive=True)
    E_v = sp.sqrt(
        Omega_r0 * v**-4
        + Omega_m0 * v**-3
        + Omega_Lambda0
    )
    chi_A_endpoint = c0 / H_A0 * sp.Integral(
        1 / (v**2 * E_v), (v, A_e, A_o)
    )
    E_Ae = sp.sqrt(
        Omega_r0 * A_e**-4
        + Omega_m0 * A_e**-3
        + Omega_Lambda0
    )
    E_Ao = sp.sqrt(
        Omega_r0 * A_o**-4
        + Omega_m0 * A_o**-3
        + Omega_Lambda0
    )
    comoving_distance_A_lower_derivative = (
        sp.diff(chi_A_endpoint, A_e)
        + c0 / (H_A0 * A_e**2 * E_Ae)
    )
    comoving_distance_A_upper_derivative = (
        sp.diff(chi_A_endpoint, A_o)
        - c0 / (H_A0 * A_o**2 * E_Ao)
    )
    comoving_distance_A_anchor = chi_A_endpoint.subs(A_o, A_e)

    E_u = sp.sqrt(
        Omega_r0 * (1 + u) ** 4
        + Omega_m0 * (1 + u) ** 3
        + Omega_Lambda0
    )
    E_z = sp.sqrt(E_z_squared)
    chi_z = c0 / H_A0 * sp.Integral(1 / E_u, (u, 0, z))
    comoving_distance_z_derivative = (
        sp.diff(chi_z, z) - c0 / (H_A0 * E_z)
    )
    comoving_distance_z_anchor = chi_z.subs(z, 0)
    v_of_u = 1 / (1 + u)
    comoving_distance_change_of_variable = (
        -(
            (1 / (v**2 * E_v)).subs(v, v_of_u)
            * sp.diff(v_of_u, u)
        )
        - 1 / E_u
    )

    p_of_a = a ** sp.Rational(-3, 2)
    A_of_a = a ** sp.Rational(5, 2)
    foundation_null_dictionary = p_of_a / A_of_a - a**-4

    # Derive transverse geometry and the observer sphere from the flat metric.
    chi_ray, delta_theta, luminosity = sp.symbols(
        "chi_ray delta_theta luminosity", positive=True
    )
    theta, phi = sp.symbols("theta phi", real=True)
    transverse_metric_component_e = A_e**2 * chi_ray**2
    proper_transverse_length_e = (
        sp.sqrt(transverse_metric_component_e) * delta_theta
    )
    D_A_endpoint = proper_transverse_length_e / delta_theta
    angular_diameter_endpoint = D_A_endpoint - A_e * chi_ray

    sphere_area_integrand = (
        A_o**2 * chi_ray**2 * sp.sin(theta)
    )
    sphere_area_o = sp.integrate(
        sphere_area_integrand,
        (theta, 0, sp.pi),
        (phi, 0, 2 * sp.pi),
    )
    sphere_area_geometry = (
        sphere_area_o - 4 * sp.pi * (A_o * chi_ray) ** 2
    )
    D_G_endpoint = sp.sqrt(sphere_area_o / (4 * sp.pi))
    Etherington_reciprocity = (
        D_G_endpoint - (A_o / A_e) * D_A_endpoint
    )

    # Photon energy and arrival-rate losses were derived independently above.
    photon_energy_factor = sp.simplify(omega_o / omega_e)
    photon_arrival_rate_factor = sp.simplify(
        delta_tau_e / delta_tau_o
    )
    flux_o = (
        luminosity
        * photon_energy_factor
        * photon_arrival_rate_factor
        / sphere_area_o
    )
    D_L_unknown = sp.symbols("D_L_unknown", positive=True)
    luminosity_distance_definition_equation = (
        4 * sp.pi * flux_o * D_L_unknown**2 - luminosity
    )
    positive_D_L_solutions = [
        solution
        for solution in sp.solve(
            sp.Eq(luminosity_distance_definition_equation, 0),
            D_L_unknown,
        )
        if solution.is_positive
    ]
    if len(positive_D_L_solutions) != 1:
        raise RuntimeError(
            "Positive luminosity-distance branch is not unique."
        )
    D_L_endpoint = positive_D_L_solutions[0]
    luminosity_distance_flux_square = (
        luminosity_distance_definition_equation.subs(
            D_L_unknown, D_L_endpoint
        )
    )
    luminosity_distance_endpoint_geometry = (
        D_L_endpoint - A_o**2 * chi_ray / A_e
    )
    D_L_reciprocity = (A_o / A_e) * D_G_endpoint
    luminosity_distance_routes = (
        D_L_endpoint - D_L_reciprocity
    )
    distance_duality_endpoint = (
        D_L_endpoint - (A_o / A_e) ** 2 * D_A_endpoint
    )
    photon_flux_ledger = (
        flux_o * sphere_area_o / luminosity
        - (A_e / A_o) ** 2
    )

    endpoint_to_redshift = {
        A_o: 1,
        A_e: 1 / (1 + z),
        chi_ray: sp.symbols("X", positive=True),
    }
    X = endpoint_to_redshift[chi_ray]
    angular_diameter_normalized = (
        D_A_endpoint.subs(endpoint_to_redshift) - X / (1 + z)
    )
    luminosity_distance_normalized = (
        D_L_endpoint.subs(endpoint_to_redshift) - (1 + z) * X
    )

    # Distance modulus equivalence and low-z Hubble slope.
    pc, D_L_symbol = sp.symbols("pc D_L_symbol", positive=True)
    mu_10pc = 5 / sp.log(10) * sp.log(D_L_symbol / (10 * pc))
    mu_Mpc = (
        5 / sp.log(10) * sp.log(D_L_symbol / (10**6 * pc)) + 25
    )
    distance_modulus_definition = mu_10pc - mu_Mpc

    D_L_z = D_L_endpoint.subs(
        {
            A_o: 1,
            A_e: 1 / (1 + z),
            chi_ray: chi_z,
        }
    )
    luminosity_distance_derivative = (
        sp.diff(D_L_z / (1 + z), z)
        - c0 / (H_A0 * E_z)
    )
    luminosity_distance_anchor = D_L_z.subs(z, 0)
    low_redshift_Hubble_slope = (
        sp.diff(D_L_z, z).subs(z, 0) - c0 / H_A0
    )
    ideal_present_Hubble = (
        (H_A0 * E_z).subs(z, 0) - H_A0
    )

    # Freedom audit uses only actual background-observable expressions.
    observable_expressions = (
        E_z_squared,
        H_A0 * E_z,
        chi_z,
        D_L_z,
    )
    nonfreedom_symbols = {z, u, c0}
    actual_freedoms = frozenset(
        symbol.name
        for expression in observable_expressions
        for symbol in expression.free_symbols - nonfreedom_symbols
    )

    residuals = {
        "process_time_metric_pullback": process_time_metric_pullback,
        "operational_space_metric_pullback": operational_space_metric_pullback,
        "operational_scale_rate_pullback": operational_scale_rate_pullback,
        "christoffel_tau_chichi": christoffel_tau_chichi,
        "christoffel_chi_tauchi": christoffel_chi_tauchi,
        "eikonal_null_dispersion": eikonal_null_dispersion,
        "eikonal_frequency_transport": eikonal_transport,
        "endpoint_frequency_ratio": endpoint_frequency_ratio,
        "geodesic_null_constraint": geodesic_null_constraint,
        "affine_frequency_invariant": affine_frequency_invariant,
        "affine_endpoint_frequency_ratio": (
            affine_endpoint_frequency_ratio
        ),
        "comoving_covector_invariant": comoving_covector_invariant,
        "endpoint_atomic_factorization": endpoint_factorization,
        "generic_atomic_endpoint_factorization": (
            generic_atomic_endpoint_factorization
        ),
        "generic_present_redshift_boundary": (
            generic_present_redshift_boundary
        ),
        "generic_atomic_Hubble_map": generic_atomic_Hubble_map,
        "chronometer_clock_boundary": chronometer_clock_boundary,
        "selected_atomic_branch_recovery": (
            selected_atomic_branch_recovery
        ),
        "selected_g1_redshift_recovery": (
            selected_g1_redshift_recovery
        ),
        "spectroscopic_redshift": spectroscopic_redshift,
        "coordinate_ratio_cancellation": coordinate_ratio_cancellation,
        "photon_coordinate_endpoint_ratio": (
            photon_coordinate_endpoint_ratio
        ),
        "atomic_coordinate_endpoint_ratio": (
            atomic_coordinate_endpoint_ratio
        ),
        "endpoint_coordinate_dimensionless_ratio": (
            endpoint_coordinate_dimensionless_ratio
        ),
        "neighboring_null_fronts": neighboring_null_fronts,
        "arrival_time_dilation": arrival_time_dilation,
        "frequency_arrival_consistency": (
            frequency_arrival_consistency
        ),
        "kinematic_Hubble_map": kinematic_Hubble_map,
        "redshift_background_substitution": (
            redshift_background_substitution
        ),
        "present_background_normalization": present_normalization,
        "comoving_distance_A_lower_derivative": (
            comoving_distance_A_lower_derivative
        ),
        "comoving_distance_A_upper_derivative": (
            comoving_distance_A_upper_derivative
        ),
        "comoving_distance_A_anchor": comoving_distance_A_anchor,
        "comoving_distance_change_of_variable": (
            comoving_distance_change_of_variable
        ),
        "comoving_distance_z_derivative": (
            comoving_distance_z_derivative
        ),
        "comoving_distance_z_anchor": comoving_distance_z_anchor,
        "foundation_null_dictionary": foundation_null_dictionary,
        "angular_diameter_endpoint": angular_diameter_endpoint,
        "sphere_area_geometry": sphere_area_geometry,
        "Etherington_reciprocity": Etherington_reciprocity,
        "luminosity_distance_flux_square": (
            luminosity_distance_flux_square
        ),
        "luminosity_distance_endpoint_geometry": (
            luminosity_distance_endpoint_geometry
        ),
        "luminosity_distance_routes": luminosity_distance_routes,
        "distance_duality_endpoint": distance_duality_endpoint,
        "angular_diameter_normalized": angular_diameter_normalized,
        "luminosity_distance_normalized": (
            luminosity_distance_normalized
        ),
        "photon_flux_ledger": photon_flux_ledger,
        "distance_modulus_definition": distance_modulus_definition,
        "luminosity_distance_derivative": (
            luminosity_distance_derivative
        ),
        "luminosity_distance_anchor": luminosity_distance_anchor,
        "low_redshift_Hubble_slope": low_redshift_Hubble_slope,
        "ideal_present_Hubble": ideal_present_Hubble,
    }

    # Negative controls must remain generically nonzero.
    wrong_photon_power = (
        sp.diff(c0 * q / A**2, A) * A_tau
        + H_A * (c0 * q / A**2)
    )
    extra_endpoint_cadence = (
        (A_o / A_e) * (p_o / p_e) - A_o / A_e
    )
    flux_without_arrival_rate = (
        luminosity * photon_energy_factor / sphere_area_o
    )
    missing_arrival_rate_flux = (
        4 * sp.pi * flux_without_arrival_rate * D_L_endpoint**2
        - luminosity
    )
    wrong_distance_duality = (
        (A_o / A_e) * D_A_endpoint - D_L_endpoint
    )
    retired_distance = c0 / H_A0 * z * (1 + z)
    retired_distance_derivative = (
        sp.diff(retired_distance / (1 + z), z)
        - c0 / (H_A0 * E_z)
    )
    omitted_generic_atomic_drift = H_A - H_spec_closed_form
    omitted_chronometer_clock_factor = (
        H_spec_closed_form - H_CC_from_definition
    )

    mutations = {
        "wrong_A_inverse_square_photon_law": wrong_photon_power,
        "extra_endpoint_cadence_factor": extra_endpoint_cadence,
        "missing_arrival_rate_flux_loss": missing_arrival_rate_flux,
        "wrong_single_factor_distance_duality": wrong_distance_duality,
        "retired_z_times_one_plus_z_distance": (
            retired_distance_derivative
        ),
        "omitted_generic_atomic_drift": (
            omitted_generic_atomic_drift
        ),
        "omitted_chronometer_clock_factor": (
            omitted_chronometer_clock_factor
        ),
    }
    return residuals, mutations, actual_freedoms


def build_report() -> dict[str, object]:
    source_path = Path(__file__).resolve()
    bridge_dir = source_path.parent
    cosmology_dir = bridge_dir.parent
    prereg_path = bridge_dir / (
        "w3_43_photon_atomic_observable_bridge_preregistration.md"
    )
    background_path = (
        cosmology_dir / "w3_cosmology_operational_geometric_flrw.py"
    )
    dependency_hashes = {
        "preregistration": _sha256(prereg_path),
        "upstream_background_source": _sha256(background_path),
    }
    dependency_hashes_exact = {
        "preregistration": (
            dependency_hashes["preregistration"]
            == EXPECTED_PREREG_SHA256
        ),
        "upstream_background_source": (
            dependency_hashes["upstream_background_source"]
            == EXPECTED_BACKGROUND_SHA256
        ),
    }
    canonical_dependencies = all(
        _canonical_lf(path)
        for path in (
            prereg_path,
            background_path,
        )
    )

    upstream_report = _load_read_only_report(
        background_path, "w3_operational_background_dependency"
    )
    background_pass = bool(
        upstream_report["closure_flags"]["conditional_background_pass"]
    )
    background_pass = background_pass and (
        upstream_report["decision_status"]
        == (
            "PASS_CONDITIONAL_BACKGROUND_EQUATION__"
            "MICROPHYSICS_PARAMETERS_AND_OBSERVABLES_OPEN"
        )
    )
    background_pass = background_pass and (
        frozenset(upstream_report["freedom_ledger"])
        == EXPECTED_FREEDOM_LEDGER
    )
    pinned_dependencies_exact = bool(
        all(dependency_hashes_exact.values())
        and canonical_dependencies
        and frozenset(dependency_hashes)
        == EXPECTED_DEPENDENCY_HASH_KEYS
        and frozenset(dependency_hashes_exact)
        == EXPECTED_DEPENDENCY_HASH_KEYS
    )

    residual_expressions, mutation_expressions, actual_freedoms = (
        _symbolic_checks()
    )
    residuals = {
        name: sp.sstr(sp.simplify(expression))
        for name, expression in residual_expressions.items()
    }
    exact = {
        name: _zero(expression)
        for name, expression in residual_expressions.items()
    }
    mutations = {
        name: sp.sstr(sp.factor(sp.simplify(expression)))
        for name, expression in mutation_expressions.items()
    }
    mutation_detection = {
        name: _nonzero(expression)
        for name, expression in mutation_expressions.items()
    }

    optical_registry_exact = (
        frozenset(OPTICAL_REGISTRY) == EXPECTED_OPTICAL_REGISTRY
    )
    ideal_source_registry_exact = (
        frozenset(IDEAL_SOURCE_REGISTRY)
        == EXPECTED_IDEAL_SOURCE_REGISTRY
    )
    freedoms_exact = (
        frozenset(FREEDOM_LEDGER)
        == EXPECTED_FREEDOM_LEDGER
        == actual_freedoms
    )

    def all_exact(names: tuple[str, ...]) -> bool:
        return all(exact[name] for name in names)

    photon_geodesic_exact = all_exact(
        (
            "christoffel_tau_chichi",
            "christoffel_chi_tauchi",
            "geodesic_null_constraint",
            "affine_frequency_invariant",
            "affine_endpoint_frequency_ratio",
            "comoving_covector_invariant",
        )
    )
    photon_transport_exact = all_exact(
        (
            "eikonal_null_dispersion",
            "eikonal_frequency_transport",
            "endpoint_frequency_ratio",
        )
    )
    generic_atomic_clock_exact = all_exact(
        (
            "generic_atomic_endpoint_factorization",
            "generic_present_redshift_boundary",
            "generic_atomic_Hubble_map",
            "chronometer_clock_boundary",
            "selected_atomic_branch_recovery",
            "selected_g1_redshift_recovery",
        )
    )
    coordinate_cancellation_exact = all_exact(
        (
            "coordinate_ratio_cancellation",
            "photon_coordinate_endpoint_ratio",
            "atomic_coordinate_endpoint_ratio",
            "endpoint_coordinate_dimensionless_ratio",
            "foundation_null_dictionary",
        )
    )
    comoving_distance_exact = all_exact(
        (
            "comoving_distance_A_lower_derivative",
            "comoving_distance_A_upper_derivative",
            "comoving_distance_A_anchor",
            "comoving_distance_change_of_variable",
            "comoving_distance_z_derivative",
            "comoving_distance_z_anchor",
        )
    )
    angular_diameter_exact = all_exact(
        (
            "angular_diameter_endpoint",
            "angular_diameter_normalized",
        )
    )
    photon_flux_exact = all_exact(
        (
            "sphere_area_geometry",
            "photon_flux_ledger",
            "luminosity_distance_flux_square",
        )
    )
    reciprocity_exact = all_exact(
        (
            "Etherington_reciprocity",
            "distance_duality_endpoint",
        )
    )
    luminosity_distance_exact = all_exact(
        (
            "luminosity_distance_flux_square",
            "luminosity_distance_endpoint_geometry",
            "luminosity_distance_routes",
            "distance_duality_endpoint",
            "luminosity_distance_normalized",
            "luminosity_distance_derivative",
            "luminosity_distance_anchor",
        )
    )
    optical_entries = frozenset(OPTICAL_REGISTRY)
    flags = {
        "upstream_background_pass_verified": background_pass,
        "operational_scale_time_dictionary_exact": all_exact(
            (
                "process_time_metric_pullback",
                "operational_space_metric_pullback",
                "operational_scale_rate_pullback",
            )
        ),
        "pinned_dependency_hashes_exact": pinned_dependencies_exact,
        "operational_metric_branch_pinned": (
            background_pass
            and all_exact(
                (
                    "process_time_metric_pullback",
                    "operational_space_metric_pullback",
                    "operational_scale_rate_pullback",
                )
            )
            and pinned_dependencies_exact
        ),
        "minimal_Maxwell_branch_selected": (
            optical_registry_exact
            and "minimally_coupled_Maxwell_geometric_optics"
            in optical_entries
        ),
        "local_atomic_proper_frequency_selected": (
            optical_registry_exact
            and "comoving_universal_local_atomic_proper_frequency"
            in optical_entries
        ),
        "transparent_photon_number_transport_selected": (
            optical_registry_exact
            and "transparent_photon_number_conserving_transport"
            in optical_entries
        ),
        "generic_atomic_chronometer_boundary_exact": (
            generic_atomic_clock_exact
        ),
        "photon_null_geodesic_exact": photon_geodesic_exact,
        "photon_frequency_transport_exact": photon_transport_exact,
        "coordinate_cadence_cancellation_exact": (
            coordinate_cancellation_exact
        ),
        "spectroscopic_redshift_exact": all_exact(
            (
                "endpoint_atomic_factorization",
                "spectroscopic_redshift",
            )
        ),
        "arrival_time_dilation_exact": all_exact(
            (
                "neighboring_null_fronts",
                "arrival_time_dilation",
                "frequency_arrival_consistency",
            )
        ),
        "kinematic_Hubble_map_exact": all_exact(
            (
                "kinematic_Hubble_map",
                "ideal_present_Hubble",
            )
        ),
        "redshift_background_substitution_exact": all_exact(
            (
                "redshift_background_substitution",
                "present_background_normalization",
            )
        ),
        "comoving_distance_exact": comoving_distance_exact,
        "angular_diameter_distance_exact": angular_diameter_exact,
        "photon_flux_ledger_exact": photon_flux_exact,
        "Etherington_reciprocity_exact": reciprocity_exact,
        "luminosity_distance_exact": luminosity_distance_exact,
        "distance_modulus_definition_exact": exact[
            "distance_modulus_definition"
        ],
        "low_redshift_Hubble_slope_exact": exact[
            "low_redshift_Hubble_slope"
        ],
        "finite_optical_registry_complete": optical_registry_exact,
        "finite_ideal_source_registry_complete": (
            ideal_source_registry_exact
        ),
        "finite_freedom_ledger_complete": freedoms_exact,
        "mutation_controls_pass": all(mutation_detection.values()),
        "schema_keysets_exact": False,
        "Maxwell_sector_derived_from_foundation": False,
        "atomic_spectrum_derived_from_foundation": False,
        "nonmetric_or_opacity_branches_excluded_by_data": False,
        "stellar_population_clock_derived": False,
        "supernova_intrinsic_luminosity_derived": False,
        "survey_selection_and_likelihood_supplied": False,
        "numerical_background_calibrated": False,
        "H_A0_identified_with_specific_measured_H0": False,
        "observational_data_fit_performed": False,
        "observational_pass": False,
        "conditional_ideal_observable_map_pass": False,
    }

    report = {
        "schema_version": "1.0",
        "claim_id": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "decision_status": "PENDING_SCHEMA_CHECK",
        "data_role": "NO_DATA_READ_OR_FITTED",
        "writes_files": False,
        "optical_registry": list(OPTICAL_REGISTRY),
        "ideal_source_registry": list(IDEAL_SOURCE_REGISTRY),
        "freedom_ledger": list(FREEDOM_LEDGER),
        "freedoms_derived_from_ideal_map": sorted(actual_freedoms),
        "required_true_flags": list(REQUIRED_TRUE_FLAGS),
        "required_false_flags": list(REQUIRED_FALSE_FLAGS),
        "closure_flags": flags,
        "residuals": residuals,
        "mutation_residuals": mutations,
        "mutation_detection": mutation_detection,
        "ideal_observable_map": {
            "spectroscopic_redshift": "1+z=A_o/A_e; A_o=1 -> 1/A_e",
            "arrival_time_dilation": "Delta_tau_o=(1+z) Delta_tau_e",
            "kinematic_expansion_rate": "H_kin(z)=H_A0 E_z(z)",
            "redshift_background": (
                "E_z^2=Omega_r0(1+z)^4+Omega_m0(1+z)^3"
                "+1-Omega_m0-Omega_r0"
            ),
            "comoving_distance": (
                "chi=(c0/H_A0) integral_0^z du/E_z(u)"
            ),
            "angular_diameter_distance": "D_A=chi/(1+z)",
            "luminosity_distance": "D_L=(1+z)chi=(1+z)^2 D_A",
            "distance_modulus": "mu=5 log10[D_L/(10 pc)]",
            "ideal_present_rate": "H_kin(0)=H_A0",
        },
        "generic_atomic_clock_boundary": {
            "atomic_frequency": "nu_A(A)=nu_A0/g(A), g(1)=1",
            "spectroscopic_redshift": (
                "1+z_spec=(A_o/A_e)g(A_e)/g(A_o); "
                "A_o=1 -> g(A_e)/A_e"
            ),
            "spectroscopic_rate": (
                "H_spec=H_A[1-d ln g/d ln A]"
            ),
            "chronometer_rate": (
                "H_CC=H_A[1-d ln g/d ln A]/C(A), "
                "C=d tau_SPS/d tau"
            ),
            "selected_ideal_branch": "g=1 gives H_kin=H_A",
            "status": "g(A), C(A), and measured-estimator calibration open",
        },
        "forward_model_open": [
            "absolute-luminosity and light-curve standardization",
            "source population, host, dust, and spectral evolution",
            "K-corrections, calibration, selection, and covariance",
            "lensing and peculiar-velocity perturbations",
            "stellar-population-synthesis chronometer clock",
            "numerical parameter inference and observational likelihood",
        ],
        "dependency_hashes": dependency_hashes,
        "dependency_hashes_exact": dependency_hashes_exact,
        "canonical_dependency_text": canonical_dependencies,
        "upstream_background_status": upstream_report["decision_status"],
        "runtime": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
        "source_sha256": _sha256(source_path),
    }
    schema_keysets_exact = bool(
        frozenset(residual_expressions) == EXPECTED_RESIDUAL_KEYS
        and frozenset(residuals) == EXPECTED_RESIDUAL_KEYS
        and frozenset(exact) == EXPECTED_RESIDUAL_KEYS
        and frozenset(mutation_expressions) == EXPECTED_MUTATION_KEYS
        and frozenset(mutations) == EXPECTED_MUTATION_KEYS
        and frozenset(mutation_detection) == EXPECTED_MUTATION_KEYS
        and frozenset(dependency_hashes)
        == EXPECTED_DEPENDENCY_HASH_KEYS
        and frozenset(dependency_hashes_exact)
        == EXPECTED_DEPENDENCY_HASH_KEYS
        and frozenset(flags) == EXPECTED_CLOSURE_FLAG_KEYS
        and frozenset(report) == EXPECTED_REPORT_KEYS
        and len(REQUIRED_TRUE_FLAGS) == len(set(REQUIRED_TRUE_FLAGS))
        and len(REQUIRED_FALSE_FLAGS) == len(set(REQUIRED_FALSE_FLAGS))
        and set(REQUIRED_TRUE_FLAGS).isdisjoint(REQUIRED_FALSE_FLAGS)
        and "conditional_ideal_observable_map_pass"
        not in REQUIRED_TRUE_FLAGS
    )
    flags["schema_keysets_exact"] = schema_keysets_exact
    aggregate_pass = all(
        flags[name] for name in REQUIRED_TRUE_FLAGS
    ) and all(not flags[name] for name in REQUIRED_FALSE_FLAGS)
    flags["conditional_ideal_observable_map_pass"] = aggregate_pass
    report["decision_status"] = PASS_STATUS if aggregate_pass else "FAIL"
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    return (
        0
        if report["closure_flags"][
            "conditional_ideal_observable_map_pass"
        ]
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
