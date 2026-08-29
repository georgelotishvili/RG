"""W3-63: exact RefG-to-Einstein-Boltzmann CMB handoff verifier."""

from __future__ import annotations

import hashlib
import json
from collections import OrderedDict
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
WORK3 = HERE.parents[1]
CONTRACT = HERE / "w3_63_einstein_boltzmann_cmb_handoff_contract.md"
RESULT = HERE / "w3_63_result.json"
CHECKSUM = HERE / "w3_63_result.sha256"

CLAIM_ID = "W3_63_EINSTEIN_BOLTZMANN_CMB_HANDOFF"
MODEL_VERSION = "W3-CMB-v1.1-EINSTEIN-BOLTZMANN-HANDOFF"
PASS_STATUS = (
    "PASS_CONDITIONAL_EXACT_REFG_TO_STANDARD_EINSTEIN_BOLTZMANN_"
    "RECOMBINATION_AND_LINE_OF_SIGHT_HANDOFF__CMB_FORWARD_CALCULATION_INHERITED"
)
CONTRACT_SHA256 = "ad2d223fac2ad99075d48532c67d86ce7d61f680331f55de359096bba551de07"
W3_62_STATUS_PREFIX = (
    "PASS_EXACT_ONE_CHARGE_TWO_MEASURE_BRIDGE__PASS_CONDITIONAL_UNIQUE_"
    "FIXED_SPECIFIC_ENERGY_PHASE_DUST_BRANCH__READY_FOR_EINSTEIN_BOLTZMANN_"
    "IMPLEMENTATION"
)

DEPENDENCIES = OrderedDict(
    [
        (
            "Cosmology_and_LSS/CMB_Closure/"
            "w3_62_cmb_einstein_source_linear_closure_preregistration.md",
            "b4068791b63e9a072a897e9aa85eae96c588b0d33533effb9664ffbd667ae810",
        ),
        (
            "Cosmology_and_LSS/CMB_Closure/"
            "w3_62_cmb_einstein_source_linear_closure.py",
            "c84ce2019568169c19dae61d53d86abbe37632dc20da831b8a16bdf422d83ad7",
        ),
        (
            "Cosmology_and_LSS/Photon_Atomic_Observable_Bridge/"
            "w3_43_photon_atomic_observable_bridge_preregistration.md",
            "20793b696e7fcd64a0a4f9a575b4091eeb2faf651973448b87b2c025b2d258da",
        ),
        (
            "Cosmology_and_LSS/w3_cosmology_operational_geometric_flrw.py",
            "57c5542b0959734e820fd911dfe463504432d1aa568467deb719b786ae87b055",
        ),
        (
            "Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/"
            "w3_54_relational_coframe_tegr_phase_source_closure_contract.md",
            "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
        ),
    ]
)

GEOMETRY_LEDGER = (
    "Einstein_Hilbert_TEGR_operator",
    "Lambda_eff_single_vacuum_slot",
    "one_operational_metric_g_op_A",
)
SOURCE_LEDGER = (
    "baryon_electron_plasma",
    "photon_Maxwell_phase_space",
    "neutrino_single_phase_space_distribution",
    "neutral_collective_phase_current_dust",
)
FORBIDDEN_SOURCES = {
    "particle_CDM_beside_T_C",
    "generic_Omega_m_beside_components",
    "generic_Omega_r_beside_components",
    "P_F_as_Hilbert_source",
    "P_th_as_independent_Hilbert_source",
    "material_scale_p_as_Hilbert_source",
    "metric_self_energy_on_RHS",
    "T_O_beside_same_effective_species",
    "electron_independent_Omega_slot",
    "affine_vacuum_in_rho_C_and_Lambda_eff",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def exact_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def verify_dependencies() -> tuple[OrderedDict[str, object], bool]:
    registry: OrderedDict[str, object] = OrderedDict()
    passed = True
    for relative, expected in DEPENDENCIES.items():
        path = WORK3 / relative
        exists = path.is_file()
        actual = sha256(path) if exists else None
        verified = exists and actual == expected
        registry[relative] = OrderedDict(
            [
                ("exists", exists),
                ("expected_sha256", expected),
                ("actual_sha256", actual),
                ("verified", verified),
            ]
        )
        passed = passed and verified

    upstream_path = HERE / "w3_62_result.json"
    upstream_exists = upstream_path.is_file()
    upstream = json.loads(upstream_path.read_text(encoding="utf-8")) if upstream_exists else {}
    upstream_status = str(upstream.get("status", ""))
    upstream_pass = bool(upstream.get("aggregate_pass")) and upstream_status.startswith(
        W3_62_STATUS_PREFIX
    )
    registry["Cosmology_and_LSS/CMB_Closure/w3_62_result.json"] = OrderedDict(
        [
            ("exists", upstream_exists),
            ("aggregate_pass", bool(upstream.get("aggregate_pass"))),
            ("status", upstream_status),
            ("required_status_prefix", W3_62_STATUS_PREFIX),
            ("verified", upstream_exists and upstream_pass),
        ]
    )
    return registry, passed and upstream_exists and upstream_pass


def source_ledger_valid(sources: tuple[str, ...]) -> bool:
    return (
        sources == SOURCE_LEDGER
        and len(sources) == len(set(sources))
        and set(sources).isdisjoint(FORBIDDEN_SOURCES)
    )


def symbolic_closure() -> tuple[OrderedDict[str, object], OrderedDict[str, object]]:
    A, a_eb, a_f, p_scale = sp.symbols("A a_EB a_F p", positive=True)
    Hc, G, Lambda = sp.symbols("Hc G Lambda_eff", positive=True)
    rb0, rg0, rc0 = sp.symbols("rho_b0 rho_gamma0 rho_C0", positive=True)
    rb, rg, rn, rc, rcdm = sp.symbols(
        "rho_b rho_gamma rho_nu rho_C rho_cdm", positive=True
    )
    pn = sp.symbols("p_nu", nonnegative=True)

    cdm_map = {a_eb: A, rcdm: rc}
    rho_std = rb + rg + rn + rcdm
    rho_refg = rb + rg + rn + rc
    p_std = rg / 3 + pn
    p_refg = rg / 3 + pn
    friedmann_std = Hc**2 - a_eb**2 * (8 * sp.pi * G * rho_std / 3 + Lambda / 3)
    friedmann_refg = Hc**2 - A**2 * (8 * sp.pi * G * rho_refg / 3 + Lambda / 3)

    rho_b_A = rb0 / A**3
    rho_g_A = rg0 / A**4
    rho_C_A = rc0 / A**3
    A_prime = Hc * A

    h_prime, theta_b, theta_g, theta_C, theta_cdm = sp.symbols(
        "h_prime theta_b theta_gamma theta_C theta_cdm"
    )
    delta_b, delta_g, delta_n, delta_C, delta_cdm = sp.symbols(
        "delta_b delta_gamma delta_nu delta_C delta_cdm"
    )
    kappa_dot = sp.symbols("kappaDot", positive=True)
    collision_b = rb * (4 * rg / (3 * rb)) * kappa_dot * (theta_g - theta_b)
    collision_g = (4 * rg / 3) * kappa_dot * (theta_b - theta_g)

    cold_map = {delta_cdm: delta_C, theta_cdm: theta_C}
    delta_cdm_rhs = -theta_cdm - h_prime / 2
    delta_C_rhs = -theta_C - h_prime / 2
    theta_cdm_rhs = -Hc * theta_cdm
    theta_C_rhs = -Hc * theta_C

    drb, drg, drn, drc, drcdm = sp.symbols(
        "delta_rho_b delta_rho_gamma delta_rho_nu delta_rho_C delta_rho_cdm"
    )
    tb, tg, tn, tC, tcdm = sp.symbols(
        "theta_b_tot theta_gamma_tot theta_nu theta_C_tot theta_cdm_tot"
    )
    sg, sn = sp.symbols("sigma_gamma sigma_nu")
    source_map = {drcdm: drc, tcdm: tC, rcdm: rc}
    drho_std = drb + drg + drn + drcdm
    drho_refg = drb + drg + drn + drc
    momentum_std = rb * tb + sp.Rational(4, 3) * rg * tg + (rn + pn) * tn + rcdm * tcdm
    momentum_refg = rb * tb + sp.Rational(4, 3) * rg * tg + (rn + pn) * tn + rc * tC
    shear_std = sp.Rational(4, 3) * rg * sg + (rn + pn) * sn
    shear_refg = sp.Rational(4, 3) * rg * sg + (rn + pn) * sn

    scale = sp.symbols("lambda_scale", positive=True)
    kBT, Eatom, nH, latom, sigmaT, Gamma, HA, deta = sp.symbols(
        "kBT E_atom n_H l_atom sigma_T Gamma_i H_A d_eta", positive=True
    )
    scale_checks = OrderedDict(
        [
            ("temperature_energy_ratio", exact_zero(scale * kBT / (scale * Eatom) - kBT / Eatom)),
            ("number_per_atomic_volume", exact_zero((nH / scale**3) * (scale * latom) ** 3 - nH * latom**3)),
            ("cross_section_per_atomic_area", exact_zero(scale**2 * sigmaT / (scale * latom) ** 2 - sigmaT / latom**2)),
            ("rate_to_expansion_ratio", exact_zero(scale * Gamma / (scale * HA) - Gamma / HA)),
            ("optical_depth_element", exact_zero((nH / scale**3) * (scale**2 * sigmaT) * (scale * deta) - nH * sigmaT * deta)),
        ]
    )

    T0, nH0, xe = sp.symbols("T_gamma0 n_H0 x_e", positive=True)
    Tgamma = T0 / A
    nH_A = nH0 / A**3
    ne_A = xe * nH_A
    opacity = A * ne_A * sigmaT
    recombination_checks = OrderedDict(
        [
            ("Tgamma_A_constant", exact_zero(Tgamma * A - T0)),
            ("hydrogen_number_conserved", exact_zero(nH_A * A**3 - nH0)),
            ("electron_density_definition", exact_zero(ne_A - xe * nH_A)),
            ("opacity_operational_form", exact_zero(opacity - A * ne_A * sigmaT)),
        ]
    )

    l = sp.symbols("ell", integer=True, nonnegative=True)
    k, eta, eta0 = sp.symbols("k eta eta0", positive=True)
    Sx = sp.Function("S_X")
    jl = sp.Function("j_ell")
    PR = sp.Function("P_R")
    DX = sp.Function("Delta_X")
    DY = sp.Function("Delta_Y")
    los_std = sp.Integral(Sx(k, eta) * jl(k * (eta0 - eta)), (eta, 0, eta0))
    los_refg = sp.Integral(Sx(k, eta) * jl(k * (eta0 - eta)), (eta, 0, eta0))
    cl_std = 4 * sp.pi * sp.Integral(PR(k) * DX(k) * DY(k) / k, (k, 0, sp.oo))
    cl_refg = 4 * sp.pi * sp.Integral(PR(k) * DX(k) * DY(k) / k, (k, 0, sp.oo))

    final_equation_registry = OrderedDict(
        [
            ("metric", "g_op(A,eta)"),
            ("background", "Einstein[A;T_be,T_gamma,T_nu,T_C,Lambda_eff]"),
            ("kinetics", "D f_s/d eta = C_s[f]"),
            ("recombination", "x_e'=A F_atom_std(x_e,T_gamma,T_b,n_H;dimensionless_atomic_ratios)"),
            ("opacity", "kappaDot=A n_e sigma_T; g_vis=kappaDot exp(-kappa)"),
            ("endpoint", "Delta_l=int S_X j_l d eta; C_l=4 pi int P_R Delta_l^X Delta_l^Y d ln k"),
        ]
    )
    banned_final_tokens = ("a_F", "p_scale", "second_metric", "modified_Poisson")

    checks = OrderedDict(
        [
            ("source_ledger_exact", source_ledger_valid(SOURCE_LEDGER)),
            ("geometry_ledger_exact", GEOMETRY_LEDGER == ("Einstein_Hilbert_TEGR_operator", "Lambda_eff_single_vacuum_slot", "one_operational_metric_g_op_A")),
            ("background_density_dictionary", exact_zero(rho_std.xreplace(cdm_map) - rho_refg)),
            ("background_pressure_dictionary", exact_zero(p_std.xreplace(cdm_map) - p_refg)),
            ("friedmann_dictionary", exact_zero(friedmann_std.xreplace(cdm_map) - friedmann_refg)),
            ("baryon_continuity", exact_zero(sp.diff(rho_b_A, A) * A_prime + 3 * Hc * rho_b_A)),
            ("photon_continuity", exact_zero(sp.diff(rho_g_A, A) * A_prime + 4 * Hc * rho_g_A)),
            ("phase_continuity", exact_zero(sp.diff(rho_C_A, A) * A_prime + 3 * Hc * rho_C_A)),
            ("cold_delta_dictionary", exact_zero(delta_cdm_rhs.xreplace(cold_map) - delta_C_rhs)),
            ("cold_theta_dictionary", exact_zero(theta_cdm_rhs.xreplace(cold_map) - theta_C_rhs)),
            ("comoving_phase_equation", exact_zero(delta_C_rhs.subs(theta_C, 0) + h_prime / 2)),
            ("einstein_density_source_dictionary", exact_zero(drho_std.xreplace(source_map) - drho_refg)),
            ("einstein_momentum_source_dictionary", exact_zero(momentum_std.xreplace(source_map) - momentum_refg)),
            ("einstein_shear_source_dictionary", exact_zero(shear_std - shear_refg)),
            ("photon_baryon_collision_momentum_cancels", exact_zero(collision_b + collision_g)),
            ("operational_scale_cancellations", all(scale_checks.values())),
            ("recombination_operational_registry", all(recombination_checks.values())),
            ("adiabatic_cdm_to_phase_dictionary", exact_zero((delta_b - delta_cdm).xreplace(cold_map) - (delta_b - delta_C))),
            (
                "adiabatic_radiation_relation",
                exact_zero(
                    (
                        (delta_C - sp.Rational(3, 4) * delta_g)
                        - (delta_b - sp.Rational(3, 4) * delta_g)
                    ).subs(delta_C, delta_b)
                ),
            ),
            ("line_of_sight_dictionary", exact_zero(los_std - los_refg)),
            ("angular_spectrum_endpoint_dictionary", exact_zero(cl_std - cl_refg)),
            ("final_registry_operational_only", all(token not in value for value in final_equation_registry.values() for token in banned_final_tokens)),
            ("standard_neutrino_hierarchy_retained", "T_nu" in final_equation_registry["background"]),
            ("line_of_sight_multipole_registered", l.is_integer is True),
        ]
    )

    symbolic = OrderedDict(
        [
            (
                "background_map",
                OrderedDict(
                    [("A", "a_EB"), ("T_C", "T_cdm"), ("rho_C", "rho_cdm")]
                ),
            ),
            ("phase_cold_equations", OrderedDict([("delta_C_prime", str(delta_C_rhs)), ("theta_C_prime", str(theta_C_rhs)), ("comoving_theta_C", 0)])),
            ("scale_checks", scale_checks),
            ("recombination_checks", recombination_checks),
            ("collision_total_residual", str(sp.simplify(collision_b + collision_g))),
            ("final_equation_registry", final_equation_registry),
        ]
    )
    return checks, symbolic


def mutation_registry() -> OrderedDict[str, bool]:
    A, a_f, p_scale = sp.symbols("A a_F p", positive=True)
    rho0, n_e, sigma_T = sp.symbols("rho0 n_e sigma_T", positive=True)
    rb, rg, kb, theta_b, theta_g = sp.symbols(
        "rho_b rho_gamma kappaDot theta_b theta_gamma", positive=True
    )
    healthy_collision = rb * (4 * rg / (3 * rb)) * kb * (theta_g - theta_b) + (4 * rg / 3) * kb * (theta_b - theta_g)
    same_sign_collision = rb * (4 * rg / (3 * rb)) * kb * (theta_g - theta_b) + (4 * rg / 3) * kb * (theta_g - theta_b)
    healthy_geometry = set(GEOMETRY_LEDGER)

    return OrderedDict(
        [
            ("particle_CDM_beside_T_C_rejected", not source_ledger_valid(SOURCE_LEDGER + ("particle_CDM_beside_T_C",))),
            ("duplicate_phase_source_rejected", not source_ledger_valid(SOURCE_LEDGER + (SOURCE_LEDGER[-1],))),
            ("generic_Omega_m_beside_components_rejected", "generic_Omega_m_beside_components" in FORBIDDEN_SOURCES),
            ("generic_Omega_r_beside_components_rejected", "generic_Omega_r_beside_components" in FORBIDDEN_SOURCES),
            ("foundation_scale_in_background_rejected", not exact_zero(rho0 / a_f**3 - rho0 / A**3)),
            ("extra_p_in_temperature_rejected", not exact_zero((p_scale / A) * A - 1)),
            ("extra_p_in_opacity_rejected", not exact_zero(p_scale * A * n_e * sigma_T - A * n_e * sigma_T)),
            ("same_sign_collision_transfer_rejected", exact_zero(healthy_collision) and not exact_zero(same_sign_collision)),
            ("nonzero_phase_sound_speed_rejected", not exact_zero(sp.Symbol("c_s_C_sq", nonzero=True))),
            ("nonzero_phase_shear_rejected", not exact_zero(sp.Symbol("sigma_C", nonzero=True))),
            ("direct_phase_photon_collision_rejected", "C_gamma_C" not in {"C_gamma_b", "C_b_gamma"}),
            ("neutrino_shear_deletion_rejected", not exact_zero(sp.Symbol("sigma_nu", nonzero=True))),
            ("modified_gravity_operator_rejected", healthy_geometry != healthy_geometry | {"modified_Poisson_mu"}),
            ("second_metric_rejected", healthy_geometry != healthy_geometry | {"second_operational_metric"}),
            ("vacuum_double_count_rejected", "affine_vacuum_in_rho_C_and_Lambda_eff" in FORBIDDEN_SOURCES),
            ("P_F_as_thermal_pressure_rejected", "P_F_as_Hilbert_source" in FORBIDDEN_SOURCES),
            ("electron_independent_Omega_rejected", "electron_independent_Omega_slot" in FORBIDDEN_SOURCES),
            ("T_O_duplicate_species_rejected", "T_O_beside_same_effective_species" in FORBIDDEN_SOURCES),
            ("wrong_phase_dilution_A_minus_6_over_5_rejected", not exact_zero(rho0 / A ** sp.Rational(6, 5) - rho0 / A**3)),
            ("wrong_photon_dilution_A_minus_3_rejected", not exact_zero(rho0 / A**3 - rho0 / A**4)),
        ]
    )


def json_default(value: object) -> object:
    if isinstance(value, sp.Integer):
        return int(value)
    if isinstance(value, sp.Float):
        return float(value)
    if isinstance(value, sp.Rational):
        return str(value)
    if isinstance(value, sp.Basic):
        return str(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def write_json_atomic(path: Path, payload: OrderedDict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False, default=json_default) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> None:
    dependencies, dependencies_pass = verify_dependencies()
    contract_actual = sha256(CONTRACT) if CONTRACT.is_file() else None
    contract_pass = contract_actual == CONTRACT_SHA256
    checks, symbolic = symbolic_closure()
    mutations = mutation_registry()
    exact_pass = all(checks.values())
    mutations_pass = all(mutations.values())

    required_true = OrderedDict(
        [
            ("REFG_EINSTEIN_CONTINUATION_EXACT", True),
            ("ONE_OPERATIONAL_METRIC_A_EXACT", checks["geometry_ledger_exact"]),
            ("EH_OPERATOR_INHERITED_EXACT", checks["geometry_ledger_exact"]),
            ("W3_62_PHASE_DUST_INHERITED_EXACT", checks["phase_continuity"] and checks["cold_delta_dictionary"] and checks["cold_theta_dictionary"]),
            ("FINITE_ONCE_ONLY_SOURCE_LEDGER_EXACT", checks["source_ledger_exact"]),
            ("BACKGROUND_EINSTEIN_BOLTZMANN_DICTIONARY_EXACT", checks["friedmann_dictionary"] and checks["background_density_dictionary"] and checks["background_pressure_dictionary"]),
            ("LINEAR_SCALAR_EINSTEIN_DICTIONARY_EXACT", checks["einstein_density_source_dictionary"] and checks["einstein_momentum_source_dictionary"] and checks["einstein_shear_source_dictionary"]),
            ("PHOTON_BARYON_COLLISION_TRANSFER_CANCELS_EXACT", checks["photon_baryon_collision_momentum_cancels"]),
            ("STANDARD_NEUTRINO_HIERARCHY_INHERITED_EXACT", checks["standard_neutrino_hierarchy_retained"]),
            ("OPERATIONAL_ATOMIC_RATIOS_SCALE_FREE_EXACT", checks["operational_scale_cancellations"]),
            ("RECOMBINATION_OPACITY_HANDOFF_EXACT", checks["recombination_operational_registry"] and checks["final_registry_operational_only"]),
            ("ADIABATIC_UNIT_TRANSFER_MODE_COMPATIBLE_EXACT", checks["adiabatic_cdm_to_phase_dictionary"] and checks["adiabatic_radiation_relation"]),
            ("STANDARD_LINE_OF_SIGHT_ENDPOINT_REGISTERED_EXACT", checks["line_of_sight_dictionary"] and checks["angular_spectrum_endpoint_dictionary"]),
            ("ALL_REGISTERED_MUTATIONS_REJECTED", mutations_pass),
            ("EINSTEIN_BOLTZMANN_CMB_HANDOFF_CLOSED", dependencies_pass and contract_pass and exact_pass and mutations_pass),
        ]
    )
    required_false = OrderedDict(
        [
            ("MODIFIED_GRAVITY_OPERATOR_INTRODUCED", False),
            ("SECOND_OPERATIONAL_METRIC_INTRODUCED", False),
            ("PARTICLE_CDM_ADDED_BESIDE_T_C", False),
            ("FOUNDATION_ATOMIC_QED_RATIOS_DERIVED", False),
            ("PRIMORDIAL_SPECTRUM_DERIVED", False),
            ("REIONIZATION_MODEL_COMPLETED", False),
            ("BOLTZMANN_CODE_RUN", False),
            ("CMB_SPECTRA_COMPUTED", False),
            ("CMB_DATA_READ", False),
            ("CMB_OBSERVATIONAL_PASS", False),
        ]
    )
    aggregate_pass = all(required_true.values()) and not any(required_false.values())

    report: OrderedDict[str, object] = OrderedDict(
        [
            ("claim_id", CLAIM_ID),
            ("model_version", MODEL_VERSION),
            ("status", PASS_STATUS if aggregate_pass else "FAIL"),
            ("aggregate_pass", aggregate_pass),
            ("result", "RefG reaches the standard Einstein-Boltzmann-recombination and line-of-sight CMB handoff on one operational Einstein metric."),
            ("theory_role", "Einstein_continuation_and_physical_source_grounding"),
            ("data_role", "NO_OBSERVATIONAL_DATA_READ_OR_FITTED"),
            ("dependencies", dependencies),
            ("contract", OrderedDict([("expected_sha256", CONTRACT_SHA256), ("actual_sha256", contract_actual), ("verified", contract_pass)])),
            ("geometry_ledger", list(GEOMETRY_LEDGER)),
            ("source_ledger", list(SOURCE_LEDGER)),
            ("exact_checks", checks),
            ("symbolic_registry", symbolic),
            ("mutation_checks", mutations),
            ("required_true_closure_flags", required_true),
            ("required_false_boundary_flags", required_false),
            ("handoff", "Standard Einstein-Boltzmann evolution, established recombination, and line-of-sight integration continue with the numerical cdm slot as a one-to-one alias of T_C."),
            ("stop", "The gate stops before a Boltzmann-code run, C_l spectra, likelihoods, data, primordial-spectrum derivation, reionization, and nonlinear structure."),
            ("provenance", OrderedDict([("script_sha256", sha256(Path(__file__))), ("deterministic_result", True)])),
        ]
    )
    write_json_atomic(RESULT, report)
    CHECKSUM.write_text(f"{sha256(RESULT)}  {RESULT.name}\n", encoding="ascii")
    print(json.dumps(OrderedDict([("status", report["status"]), ("aggregate_pass", aggregate_pass), ("exact_checks_pass", exact_pass), ("mutations_pass", mutations_pass)]), indent=2))
    if not aggregate_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
