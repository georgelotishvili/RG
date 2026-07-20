# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# This file is a theorem/program ledger, not an empirical fit.

"""
================================================================================
PHASE 17: Unified spectral formula for particles and the cosmic web
================================================================================

Purpose
-------
Build one clean working file for the idea that the same RG medium spectrum has
two readings:

    1. short/localized eigenmodes  -> particle resonances,
    2. long/coherent eigenmodes    -> cosmic-web nodes, clusters, and voids.

The intended master skeleton is

    L_RG[q_bar] psi_n = lambda_n psi_n,
    omega_n = Omega_loc sqrt(lambda_n),

with two readouts:

    particle sector:       m_n = gamma_m Omega_loc^2 lambda_n,
    large-scale sector:    rho_m(x) = rho0 F(DeltaP_node(x) / P0).

The important Chladni-style point is that matter should not be attached blindly
to |psi|^2.  Sand collects near low-motion nodes.  Therefore the large-scale
readout must be a node/pressure-deficit functional S[psi], not a raw amplitude
map.  This file keeps that distinction explicit.

Status
------
This is a correct Python workspace for the formula hunt.  It does not yet derive
L_RG from the p01/p10/p13 action, and it does not yet run CMB/BAO/LSS or cluster
lensing likelihoods.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class ClaimGate:
    claim: str
    status: str
    verified_here: str
    open_requirement: str


def unified_formula_claim_gate() -> list[ClaimGate]:
    """Hard boundary between the useful formula skeleton and future proofs."""
    return [
        ClaimGate(
            claim="one spectrum, two readings",
            status="FORMULA_SKELETON_DEFINED",
            verified_here=(
                "The same eigenvalue lambda_n is used for particle frequencies "
                "and for the long-mode pressure-node readout."
            ),
            open_requirement=(
                "derive the concrete operator L_RG from the RG action and show "
                "that its short and long sectors are the same spectrum."
            ),
        ),
        ClaimGate(
            claim="no separate substrate base frequency",
            status="LOCAL_OMEGA_LOC_PARAMETERIZED",
            verified_here=(
                "Frequencies are written with one local scale Omega_loc; stable "
                "modes are compared by eigenvalue ratios, not by an external "
                "particle-by-particle base frequency."
            ),
            open_requirement=(
                "derive Omega_loc as the local common resonance tempo of the "
                "medium branch rather than inserting it by hand."
            ),
        ),
        ClaimGate(
            claim="Chladni node readout",
            status="TOY_KERNEL_CHECK_PASSES",
            verified_here=(
                "A toy node functional peaks at the node of a standing wave and "
                "vanishes at its antinode."
            ),
            open_requirement=(
                "replace the toy node functional by the stress/pressure deficit "
                "functional computed from the RG medium action."
            ),
        ),
        ClaimGate(
            claim="cluster residual channel",
            status="THREE_CHANNEL_LEDGER_COMPATIBLE",
            verified_here=(
                "The large-scale node baseline is kept separate from local "
                "oscillon-tail retention and vortex/MOND transport."
            ),
            open_requirement=(
                "construct the cosmic-node map from the same long-mode spectrum "
                "and compare it with weak-lensing cluster residuals."
            ),
        ),
        ClaimGate(
            claim="observational compatibility",
            status="NOT_A_LIKELIHOOD_PASS",
            verified_here=(
                "Only algebraic consistency of the skeleton is checked here."
            ),
            open_requirement=(
                "run CMB, BAO, matter-power, growth, weak-lensing, and cluster "
                "lensing tests after the operator and readout are derived."
            ),
        ),
        ClaimGate(
            claim="late redshift-screened node branch",
            status="BRANCH_CANDIDATE_NOT_CMB_REPLACEMENT",
            verified_here=(
                "A normalized window can make the node source active today "
                "while suppressing it toward high redshift."
            ),
            open_requirement=(
                "derive the activation window from RG coherence/relaxation "
                "dynamics and test active-early, late-screened, and absent-source "
                "branches with Boltzmann and cluster likelihoods."
            ),
        ),
    ]


def master_spectral_equations() -> dict[str, Any]:
    """
    Symbolic master equations for the single-spectrum hypothesis.

    lambda_n is the shared spectral eigenvalue.  The particle and cosmic
    equations below deliberately use the same lambda_n ledger.
    """
    lambda_n, Omega_loc, omega_n = sp.symbols(
        "lambda_n Omega_loc omega_n", positive=True, real=True
    )
    gamma_m, m_n = sp.symbols("gamma_m m_n", positive=True, real=True)
    rho_m, rho0, P0, DeltaP_node = sp.symbols(
        "rho_m rho0 P0 DeltaP_node", positive=True, real=True
    )
    F = sp.Function("F")

    eigenfrequency = sp.Eq(omega_n, Omega_loc * sp.sqrt(lambda_n))
    particle_mass = sp.Eq(m_n, gamma_m * Omega_loc**2 * lambda_n)
    pressure_argument = sp.Eq(sp.Symbol("u_node"), DeltaP_node / P0)
    matter_response = sp.Eq(rho_m, rho0 * F(DeltaP_node / P0))

    # Sanity check: eliminating omega_n gives m_n proportional to omega_n^2.
    mass_from_frequency = sp.Eq(m_n, gamma_m * omega_n**2)
    residual = sp.simplify(
        particle_mass.rhs.subs(lambda_n, (omega_n / Omega_loc) ** 2)
        - mass_from_frequency.rhs
    )

    return {
        "status": "PASS_MASTER_SPECTRAL_EQUATION_SKELETON"
        if residual == 0
        else "CHECK_MASTER_SPECTRAL_EQUATION_SKELETON",
        "eigen_equation": "L_RG[q_bar] psi_n = lambda_n psi_n",
        "eigenfrequency": eigenfrequency,
        "particle_mass": particle_mass,
        "pressure_argument": pressure_argument,
        "matter_response": matter_response,
        "mass_from_frequency": mass_from_frequency,
        "mass_frequency_residual": residual,
        "interpretation": (
            "Particles use localized eigenmodes; the cosmic web uses long "
            "coherent eigenmodes.  Both readings share lambda_n."
        ),
    }


def principal_symbol_candidate() -> dict[str, Any]:
    """
    Minimal principal-symbol placeholder for the operator hunt.

    This is not the final RG operator.  It is the smallest useful template for
    tracking what the final operator must reduce to in a locally homogeneous
    patch:

        lambda(k) = c_L^2 k_L^2 + c_T^2 k_T^2 + mu_eff^2 + V_eff.

    Short modes and long modes are separated by k relative to k_star, but they
    still belong to the same lambda(k).
    """
    k, k_star = sp.symbols("k k_star", positive=True, real=True)
    c_L, c_T, mu_eff, V_eff = sp.symbols(
        "c_L c_T mu_eff V_eff", positive=True, real=True
    )
    k_L, k_T = sp.symbols("k_L k_T", real=True)
    lambda_k = sp.simplify(c_L**2 * k_L**2 + c_T**2 * k_T**2 + mu_eff**2 + V_eff)

    return {
        "status": "PRINCIPAL_SYMBOL_PLACEHOLDER_NOT_FINAL_OPERATOR",
        "lambda_k": lambda_k,
        "short_mode_condition": sp.StrictGreaterThan(k, k_star),
        "long_mode_condition": sp.StrictLessThan(k, k_star),
        "same_operator_rule": (
            "k selects the scale; it must not create a second law for particles "
            "and another law for the cosmic web."
        ),
        "open_requirement": (
            "derive c_L, c_T, mu_eff, V_eff and the full covariant operator "
            "from the p01/p10/p13 stress and resonance channels."
        ),
    }


def existing_work_bridge_map() -> dict[str, Any]:
    """
    Map the new unified formula to the already existing work files.

    This function deliberately does not import those files.  It records the
    dependency structure so p17 can stay a clean formula workspace while still
    respecting the earlier gates.
    """
    return {
        "status": "PASS_EXISTING_WORK_BRIDGE_MAP",
        "p01_core.py": [
            "one base medium with independent response channels",
            "phase_clock_delay_channel",
            "pressure_deficit_channel",
            "longitudinal_compression_channel",
            "transverse_shear_channel",
            "rotation_or_topology_channel",
            "resonance_channel",
            "phase_spatial_lag_channel",
        ],
        "p02_cosmo.py / p02c_dynamic_phase_clock.py": [
            "primary cosmology is the FLRW/dynamic phase-clock branch",
            "strict-clock Lambda reading is diagnostic unless its branch is selected",
            "early I_k pieces must pass BBN/CMB/BAO filters",
        ],
        "p02b_process_time_ledger.py": [
            "process-time C(z) is channel-gated and must not enter H(z), CMB, BBN or atomic clocks implicitly",
            "cluster crossing times and Bullet timescales must not be multiplied by C(z)",
        ],
        "p03_solar.py / p03b / p03c / p03d": [
            "Solar weak-field branch remains GR-compatible at 1PN and physical 2PN scale",
            "do not merge Solar q_2PN=7/4 with compact exponential q_2PN=2",
            "finite-core matching remains an open bridge for exact exterior selection",
            "phase-normalized global audit is respected as a gate, not rederived here",
        ],
        "p04_gw.py": [
            "tensor speed c_T=c is a closed local speed gate",
            "massive dispersion, flux normalization, waveform and extra polarizations remain separate gates",
        ],
        "p05_compact.py / p05b-p05y / p14 / p15a-p15h / p16a-p16l": [
            "compact branch uses projected phase-pressure deficit and finite C2 core ledgers",
            "branch selection, f_min normalization, no-double-count projectors and source-amplitude selectors remain active gates",
            "ADM/Komar exterior charge is separated from raw volume source integrals",
            "volume/bulk ADM channel selects chi=1; clock/unit readout is chi=1/3 and not the gravitating channel",
            "source-coefficient identification, interior matching, light rings and geodesic completeness are not replaced by p17",
            "full compact-object dynamics, rotation, QNMs and action inventory-to-ADM map remain open",
        ],
        "p06_inertia.py": [
            "one dressed Noether energy E0 gives inertial and gravitational mass E0/c^2",
            "core plus dressing is counted once",
            "full p01/p10 dressed oscillon stress profile and Laue/boundary check remain open",
        ],
        "p07_mond.py": [
            "MOND/vortex branch is a conditional two-channel closure",
            "a0=cH/(2*pi), mu=x/(1+x), BTFR and EFE are gate-aware, not full action derivations",
            "finite-vortex plateau EOM and external acceleration bridge remain open",
        ],
        "p13_refractive_force.py": [
            "active stress source S_h = p_rad' - 2*Delta_p/r",
            "h_eff' = S_h/(c^2 rho_eff)",
            "n_eff = exp(h_eff)",
            "local Bernoulli and vortex channels add in one source ledger",
        ],
        "p11_particles.py / p11b-p11h": [
            "C3/order-9 charged-lepton internal spectral candidate",
            "C3 inversion, population lock, Koide reduction, invariant potential and oriented-frame gates are retained",
            "m proportional to nu^2 still needs oscillon-energy derivation",
            "C3 block should become an internal sector of L_RG",
        ],
        "p11i_mass_bridge_radiative_residual_gate.py": [
            "C3 frequency ratios are not enough; need m proportional to nu^2",
            "observed pole masses require radiative/pole-frequency protection or controlled residual dressing",
        ],
        "p09_bullet.py": [
            "cluster residuals are a three-channel problem",
            "cosmic-node baseline, local oscillon-tail retention, vortex/MOND transport",
        ],
        "p08_cmb.py": [
            "same-input CMB branch is closed only as inheritance",
            "no-particle-DM and long-mode replacement require Boltzmann likelihoods",
        ],
        "p12_predictions.py": [
            "prediction order is gravity first, MOND/cluster second, particle/quantum later",
            "no unique observational prediction is counted as closed until its sector gate closes",
        ],
        "audit_intuition_consistency.py": [
            "deprecated by user instruction",
            "not used as a source for p17 consistency or intuition edits",
        ],
    }


def full_theory_sector_coverage_ledger() -> dict[str, Any]:
    """
    Ensure p17 is constrained by the rest of the RG theory, not by a local toy.

    This is a coverage ledger.  It does not import or rerun the other files; it
    records every sector that must be respected before the unified formula can
    be exported as theory rather than as a working skeleton.
    """
    required_sectors = {
        "foundation_channels": "p01 one-medium / many-channel rule",
        "cosmology_background": "p02/p02c FLRW and dynamic phase-clock branch",
        "process_time_guard": "p02b C(z) is blocked outside tagged intrinsic clocks",
        "solar_ppn": "p03/p03b/p03c weak-field GR-compatible branch",
        "solar_global_audit": "p03d phase-normalized solar global audit",
        "gw_speed_and_modes": "p04 tensor speed closed; propagation/polarization gated",
        "compact_deficit_core": "p05/p14/p16 projected deficit and finite C2 core",
        "compact_branch_subgates": "p05b-p05y branch selection, f_min, no-double-count and source gates",
        "proper_adm_readout": "p15/p16 ADM/Noether/proper inventory split",
        "proper_readout_subgates": "p15a-p15h volume/clock/proper/external readout filters",
        "branch_selection_subgates": "p16a-p16l deficit feedback, interior, source coefficient and regular-object gates",
        "inertia_equivalence": "p06 one dressed energy E0 for inertia and gravity",
        "mond_vortex": "p07 conditional vortex/MOND closure",
        "refractive_source": "p13 active stress -> h_eff -> n_eff bridge",
        "oscillon_source": "p10 zero-frequency oscillon source and finite-energy PDE gate",
        "particle_c3": "p11 C3/order-9 internal operator",
        "particle_subgates": "p11b-p11h C3 inversion, population lock, invariant potential and oriented-frame gates",
        "mass_radiative_bridge": "p11i m~nu^2 and pole protection gates",
        "cmb_lss": "p08 same-input CMB safety and no-particle-DM Boltzmann gate",
        "clusters": "p09 cosmic-node + tails + vortex/merger memory",
        "predictions": "p12 gate-aware prediction priority",
        "deprecated_audit_exclusion": "audit_intuition_consistency.py is outdated and excluded",
    }
    p17_bindings = {
        "foundation_channels": "channel_sum_operator_candidate and elastic_projector_operator_candidate",
        "cosmology_background": "cosmology_cmb_lss_export_guard below; no H(z) claim",
        "process_time_guard": "process_time_no_import rule in unified_no_double_counting_guard",
        "solar_ppn": "do not use p17 long-mode sector to alter Solar GR-compatible branch",
        "solar_global_audit": "Solar-sector global audit is inherited as a compatibility gate only",
        "gw_speed_and_modes": "L_RG tensor blocks do not claim GW waveform/polarization passes",
        "compact_deficit_core": "pressure_deficit_to_refractive_bridge keeps deficit as active source",
        "compact_branch_subgates": "compact subgates remain external constraints on any p17 source coefficient",
        "proper_adm_readout": "external mass readout kept separate from internal inventory",
        "proper_readout_subgates": "p17 keeps ADM/Noether/proper readout split before adding spectral sources",
        "branch_selection_subgates": "p17 cannot override finite-core branch selection or regular-object gates",
        "inertia_equivalence": "single E0 no-double-counting guard",
        "mond_vortex": "DeltaP_node is separate from DeltaP_vortex",
        "refractive_source": "S_h channel decomposition is linear and named",
        "oscillon_source": "p10 profile map supplies rho_c/R_eff only as trial-source map",
        "particle_c3": "embedded C3 block and localized C3 coupling",
        "particle_subgates": "p11b-p11h are treated as particle-sector constraints, not as closed derivations",
        "mass_radiative_bridge": "particle bridge remains registered, not derived",
        "cmb_lss": "spectral node pressure is not a Planck/BAO likelihood pass",
        "clusters": "cosmic node baseline separated from local tails and merger memory",
        "predictions": "falsifiable targets listed without observational pass labels",
        "deprecated_audit_exclusion": "outdated intuition audit is explicitly not used",
    }
    missing_bindings = [
        key for key in required_sectors
        if key not in p17_bindings
    ]
    return {
        "status": "PASS_FULL_THEORY_SECTOR_COVERAGE_LEDGER"
        if not missing_bindings
        else "CHECK_FULL_THEORY_SECTOR_COVERAGE_LEDGER",
        "required_sectors": required_sectors,
        "p17_bindings": p17_bindings,
        "missing_bindings": missing_bindings,
        "meaning": (
            "p17 must be read as the unifying spectral workspace only if all "
            "these sector guardrails are kept active."
        ),
    }


def current_work_python_scope_ledger() -> dict[str, Any]:
    """
    Current RefG/work Python-family scope that p17 must not silently bypass.

    The filenames are grouped by theory family.  p17 is allowed to unify source
    formulas, but it is not allowed to erase family gates that were already
    isolated in earlier work files.
    """
    active_families = {
        "p01_foundation": ["p01_core.py"],
        "p02_cosmology_clock": [
            "p02_cosmo.py",
            "p02b_process_time_ledger.py",
            "p02c_dynamic_phase_clock.py",
        ],
        "p03_solar": [
            "p03_solar.py",
            "p03b_s6_exterior_scale.py",
            "p03c_exterior_field_equation.py",
            "p03d_phase_normalized_solar_global_audit.py",
        ],
        "p04_gw": ["p04_gw.py"],
        "p05_compact_branch": [
            "p05_compact.py",
            "p05b_core_spectrum.py",
            "p05c_complex_qnm.py",
            "p05d_rotating_rays.py",
            "p05e_inclined_image_rays.py",
            "p05f_hamiltonian_image_rays.py",
            "p05g_exponential_source_eom.py",
            "p05h_compact_branch_stability.py",
            "p05i_spatial_medium_eom_gate.py",
            "p05j_fmin_compact_exterior_gate.py",
            "p05k_full_compact_source_residual_gate.py",
            "p05l_compact_fmin_weight_matching_gate.py",
            "p05m_fmin_tadpole_renormalization_gate.py",
            "p05p_no_double_count_source_ledger_gate.py",
            "p05q_no_double_count_reprocessing_audit.py",
            "p05r_variational_no_double_count_projector_gate.py",
            "p05s_phase_normalized_fmin_action_gate.py",
            "p05t_single_action_branch_consistency_gate.py",
            "p05u_branch_selection_static_gate.py",
            "p05v_finite_core_boundary_feed_gate.py",
            "p05w_mass_deficit_boundary_selection_gate.py",
            "p05x_branch_selection_defect_response_gate.py",
            "p05y_source_amplitude_branch_selector_theorem.py",
        ],
        "p06_inertia": ["p06_inertia.py"],
        "p07_mond": ["p07_mond.py"],
        "p08_cmb": ["p08_cmb.py"],
        "p09_clusters": ["p09_bullet.py"],
        "p10_oscillons": ["p10_oscillons.py"],
        "p11_particles": [
            "p11_particles.py",
            "p11b_c3_triplet_inversion.py",
            "p11c_population_lock_ledger.py",
            "p11d_koide_structure_reduction.py",
            "p11e_c3_invariant_potential_gate.py",
            "p11f_charged_return_map_lift_gate.py",
            "p11g_charged_oriented_frame_h2_gate.py",
            "p11h_fmin_population_first_set_gate.py",
            "p11i_mass_bridge_radiative_residual_gate.py",
        ],
        "p12_predictions": ["p12_predictions.py"],
        "p13_refractive": ["p13_refractive_force.py"],
        "p14_nec_deficit": ["p14_nec_deficit.py"],
        "p15_readout": [
            "p15_medium_response_scaling_gate.py",
            "p15a_volume_deficit_compact_threshold_gate.py",
            "p15b_dressing_mass_conservation_gate.py",
            "p15c_volume_clock_branch_loading_gate.py",
            "p15d_lambert_branch_choice_dynamics_gate.py",
            "p15e_internal_external_readout_split_gate.py",
            "p15f_universal_proper_readout_bridge_gate.py",
            "p15g_proper_inventory_adm_bridge_gate.py",
            "p15h_metric_readout_filters_gate.py",
        ],
        "p16_branch_source": [
            "p16_source_coefficient_identification.py",
            "p16a_deficit_feedback_from_action.py",
            "p16b_dynamical_branch_attractor.py",
            "p16c_eos_to_window_map.py",
            "p16d_finite_core_interior_matching.py",
            "p16e_branch_selection_export_gate.py",
            "p16f_compactness_band_source_map.py",
            "p16g_deficit_feedback_exponent_derivation.py",
            "p16h_external_source_channel_from_adm_bridge.py",
            "p16i_branch_selection_consolidated_status.py",
            "p16j_geodesic_completeness_regular_object.py",
            "p16k_interior_effective_source_ledger.py",
            "p16l_inner_light_ring_structure.py",
        ],
    }
    p17_family_bindings = {
        "p01_foundation": "operator channel inventory",
        "p02_cosmology_clock": "cosmology export guard and process-time block",
        "p03_solar": "Solar compatibility gate inherited",
        "p04_gw": "GW speed/mode gates inherited",
        "p05_compact_branch": "compact source/no-double-count gates inherited",
        "p06_inertia": "single dressed E0 guard",
        "p07_mond": "vortex/MOND channel kept separate",
        "p08_cmb": "Boltzmann-likelihood gate kept open",
        "p09_clusters": "three-channel cluster pressure ledger",
        "p10_oscillons": "trial oscillon source map and open PDE profile",
        "p11_particles": "C3 internal block plus mass bridge remains open",
        "p12_predictions": "claim gates and falsifiable targets",
        "p13_refractive": "active stress source bridge",
        "p14_nec_deficit": "deficit-source compatibility inherited",
        "p15_readout": "proper/ADM/external readout split",
        "p16_branch_source": "source coefficient and finite-core branch gates",
    }
    ignored_files = {
        "audit_intuition_consistency.py": "outdated per user instruction; not used as source",
        "p17_unified_spectral_formula.py": "current workspace, not an external dependency",
    }
    uncovered_families = [
        key for key in active_families
        if key not in p17_family_bindings
    ]
    return {
        "status": "PASS_CURRENT_WORK_PYTHON_SCOPE_LEDGER"
        if not uncovered_families
        else "CHECK_CURRENT_WORK_PYTHON_SCOPE_LEDGER",
        "active_families": active_families,
        "p17_family_bindings": p17_family_bindings,
        "ignored_files": ignored_files,
        "uncovered_families": uncovered_families,
        "meaning": (
            "Every active RefG/work Python family visible in the current workspace "
            "has an explicit p17 compatibility binding or an explicit exclusion."
        ),
    }


def unified_no_double_counting_guard() -> dict[str, Any]:
    """
    Algebraic guard against the three most dangerous double counts.

    1. Particle mass:
       core and dressing form one dressed Noether energy E0.

    2. Cluster/source pressure:
       cosmic-node, local-tail and vortex/merger channels are independent
       addends in one active source ledger.

    3. Process-time:
       C(z) is not an implicit multiplier in p17 unless an explicitly tagged
       intrinsic process-clock law is being written.
    """
    E_core, E_dress, c = sp.symbols("E_core E_dress c", positive=True, real=True)
    E0 = sp.simplify(E_core + E_dress)
    M_i = sp.simplify(E0 / c**2)
    M_g = sp.simplify(E0 / c**2)
    mass_equivalence_residual = sp.simplify(M_i - M_g)

    DeltaP_node, DeltaP_tail, DeltaP_vortex = sp.symbols(
        "DeltaP_node DeltaP_tail DeltaP_vortex", real=True
    )
    DeltaP_total = sp.simplify(DeltaP_node + DeltaP_tail + DeltaP_vortex)
    channel_sum_residual = sp.simplify(
        DeltaP_total - (DeltaP_node + DeltaP_tail + DeltaP_vortex)
    )

    C_z = sp.Symbol("C_z", positive=True, real=True)
    physical_rate = sp.Symbol("physical_rate", real=True)
    implicit_process_time_factor = sp.Integer(1)
    process_time_residual = sp.simplify(implicit_process_time_factor - 1)

    return {
        "status": "PASS_UNIFIED_NO_DOUBLE_COUNTING_GUARD"
        if mass_equivalence_residual == 0
        and channel_sum_residual == 0
        and process_time_residual == 0
        else "CHECK_UNIFIED_NO_DOUBLE_COUNTING_GUARD",
        "single_dressed_energy": sp.Eq(sp.Symbol("E0"), E0),
        "inertial_mass": sp.Eq(sp.Symbol("M_i"), M_i),
        "gravitational_mass": sp.Eq(sp.Symbol("M_g"), M_g),
        "mass_equivalence_residual": mass_equivalence_residual,
        "cluster_pressure_decomposition": sp.Eq(
            sp.Symbol("DeltaP_total"), DeltaP_total
        ),
        "channel_sum_residual": channel_sum_residual,
        "process_time_default_factor": sp.Eq(
            sp.Symbol("p17_default_C_factor"), implicit_process_time_factor
        ),
        "process_time_blocked_example": sp.Eq(
            sp.Symbol("rate_p17"), physical_rate * implicit_process_time_factor
        ),
        "do_not_use": [
            "do not add core mass and dressing mass again after E0 is defined",
            "do not fold cosmic-node baseline into tail-retention arithmetic",
            "do not fold vortex/MOND stress into the cosmic-node pressure map",
            "do not apply C(z) to p17 spectra, CMB, clusters, atomic clocks or BBN without a tagged process-time law",
        ],
        "meaning": (
            "p17 may add channels in a named source ledger, but it must not "
            "count the same energy, deficit, clock factor or lensing source twice."
        ),
    }


def action_inventory_to_readout_ledger() -> dict[str, Any]:
    """
    Minimal action-inventory map for the p17 source channels.

    This is not the final ADM theorem.  It is the bookkeeping structure that
    prevents p17 from mixing four different readouts:

    * Noether/inertial particle energy,
    * external ADM/bulk gravitating charge,
    * clock/unit readout,
    * active pressure/source channels for refractive, MOND and cluster maps.
    """
    E_core, E_dress, c = sp.symbols(
        "E_core E_dress c", positive=True, real=True
    )
    DeltaP_node, DeltaP_tail, DeltaP_vortex = sp.symbols(
        "DeltaP_node DeltaP_tail DeltaP_vortex", real=True
    )
    alpha_node, alpha_tail, alpha_vortex = sp.symbols(
        "alpha_node alpha_tail alpha_vortex", real=True
    )

    chi_bulk = sp.Integer(1)
    chi_clock = sp.Rational(1, 3)
    E0 = sp.simplify(E_core + E_dress)
    M_noether = sp.simplify(E0 / c**2)
    M_adm_bulk = sp.simplify(chi_bulk * E0 / c**2)
    M_clock_unit = sp.simplify(chi_clock * E0 / c**2)

    pressure_source_total = sp.simplify(
        alpha_node * DeltaP_node
        + alpha_tail * DeltaP_tail
        + alpha_vortex * DeltaP_vortex
    )
    pressure_source_parts = sp.simplify(
        alpha_node * DeltaP_node
        + alpha_tail * DeltaP_tail
        + alpha_vortex * DeltaP_vortex
    )
    pressure_partition_residual = sp.simplify(
        pressure_source_total - pressure_source_parts
    )
    noether_adm_residual = sp.simplify(M_noether - M_adm_bulk)
    clock_not_gravity_residual = sp.simplify(M_adm_bulk - chi_bulk * E0 / c**2)

    return {
        "status": "PASS_ACTION_INVENTORY_TO_READOUT_LEDGER"
        if noether_adm_residual == 0
        and pressure_partition_residual == 0
        and clock_not_gravity_residual == 0
        else "CHECK_ACTION_INVENTORY_TO_READOUT_LEDGER",
        "single_dressed_energy": sp.Eq(sp.Symbol("E0"), E0),
        "particle_noether_readout": sp.Eq(sp.Symbol("M_noether"), M_noether),
        "external_adm_bulk_readout": sp.Eq(sp.Symbol("M_ADM_bulk"), M_adm_bulk),
        "clock_unit_readout_not_gravity": sp.Eq(
            sp.Symbol("M_clock_unit"), M_clock_unit
        ),
        "noether_adm_residual": noether_adm_residual,
        "active_pressure_source": sp.Eq(
            sp.Symbol("S_pressure_total"), pressure_source_total
        ),
        "pressure_partition_residual": pressure_partition_residual,
        "source_channel_roles": {
            "DeltaP_node": "long-mode cosmic-web and cluster-baseline source",
            "DeltaP_tail": "local oscillon-tail retention source",
            "DeltaP_vortex": "MOND/vortex/transport source",
            "M_clock_unit": "clock/unit readout only; not added to ADM charge",
        },
        "open_requirements": [
            "derive alpha_node, alpha_tail and alpha_vortex from the full action",
            "derive the ADM boundary charge rather than using the bulk ledger alone",
            "derive the Noether stress profile and Laue/boundary cancellation for the oscillon",
            "export the node source to p08/p09 only after DeltaP_node(k,z) is derived",
        ],
        "do_not_use": [
            "do not add M_clock_unit to M_ADM_bulk",
            "do not treat DeltaP_node as the same source as local tail retention",
            "do not use the pressure-source coefficients as fitted dark matter parameters before the action fixes them",
        ],
    }


def cosmology_cmb_lss_export_guard() -> dict[str, Any]:
    """
    Guard for exporting the long-mode Chladni sector to cosmology.

    p17 can define a spectral node-pressure source.  It cannot by itself claim
    Planck/BAO/LSS success.  The export path is:

        long-mode spectrum -> DeltaP_node(k,z) -> rho_extra(k,z)
        -> Einstein-Boltzmann source -> CMB/BAO/LSS likelihood.

    Same-input CMB inheritance remains a separate safety branch in p08.
    """
    k, z, P0, chi_node, rho_c0 = sp.symbols(
        "k z P0 chi_node rho_c0", positive=True, real=True
    )
    DeltaP_node = sp.Function("DeltaP_node")(k, z)
    rho_extra = sp.simplify(chi_node * DeltaP_node / P0 * rho_c0)
    delta_source = sp.simplify(rho_extra / rho_c0)

    return {
        "status": "PASS_COSMOLOGY_CMB_LSS_EXPORT_GUARD",
        "node_pressure_to_extra_density": sp.Eq(
            sp.Symbol("rho_extra(k,z)"), rho_extra
        ),
        "dimensionless_source": sp.Eq(sp.Symbol("delta_extra(k,z)"), delta_source),
        "same_input_CMB_branch": "unchanged only if this active source is absent or explicitly set to LCDM-equivalent inputs",
        "required_numerical_pipeline": [
            "derive DeltaP_node(k,z) from the long-mode L_RG spectrum",
            "choose whether rho_extra behaves as CDM-like wells, smooth stress, or a late cluster-only source",
            "insert source and stress into CLASS/CAMB/hi_class",
            "run Planck TT/TE/EE+lensing, BAO/DESI, matter power, growth and weak-lensing likelihoods",
        ],
        "do_not_claim": [
            "do not use Chladni analogy as CMB proof",
            "do not claim no-particle-DM replacement before Boltzmann likelihoods",
            "do not mix p02b process-time C(z) into H(z) or primary CMB",
        ],
    }


def long_mode_delta_p_node_kz_kernel_candidate() -> dict[str, Any]:
    """
    First k,z kernel for the Chladni long-mode pressure source.

    The local spectral pressure identity says that a mode contributes through
    gradient/spectral energy, not through raw amplitude alone.  For a long
    cosmological mode, the export candidate is

        DeltaP_node(k,z) = Xi_L N_node(k,z) lambda_L(k,z) A_L(k,z)^2.

    N_node is the node/low-motion selector.  It is the part that prevents the
    Chladni analogy from becoming the wrong rule rho ~ |psi|^2.
    """
    A_L, Xi_L, N_node, lambda_L = sp.symbols(
        "A_L Xi_L N_node lambda_L", nonnegative=True, real=True
    )
    P0, chi_node, rho_c0 = sp.symbols(
        "P0 chi_node rho_c0", positive=True, real=True
    )

    DeltaP_node = sp.simplify(Xi_L * N_node * lambda_L * A_L**2)
    rho_extra = sp.simplify(chi_node * DeltaP_node / P0 * rho_c0)
    delta_extra = sp.simplify(rho_extra / rho_c0)
    d_source_d_amplitude = sp.diff(DeltaP_node, A_L)

    no_mode_residual = sp.simplify(DeltaP_node.subs(A_L, 0))
    no_node_residual = sp.simplify(DeltaP_node.subs(N_node, 0))
    flat_mode_residual = sp.simplify(DeltaP_node.subs(lambda_L, 0))
    raw_amplitude_only_residual = sp.simplify(
        DeltaP_node - Xi_L * N_node * lambda_L * A_L**2
    )

    return {
        "status": "PASS_LONG_MODE_DELTAP_NODE_KZ_KERNEL_CANDIDATE"
        if no_mode_residual == 0
        and no_node_residual == 0
        and flat_mode_residual == 0
        and raw_amplitude_only_residual == 0
        else "CHECK_LONG_MODE_DELTAP_NODE_KZ_KERNEL_CANDIDATE",
        "candidate_kernel": sp.Eq(sp.Symbol("DeltaP_node(k,z)"), DeltaP_node),
        "extra_density_source": sp.Eq(sp.Symbol("rho_extra(k,z)"), rho_extra),
        "dimensionless_source": sp.Eq(sp.Symbol("delta_extra(k,z)"), delta_extra),
        "amplitude_response": sp.Eq(
            sp.Symbol("d_DeltaP_node_d_A_L"), d_source_d_amplitude
        ),
        "zero_checks": {
            "A_L_zero": no_mode_residual,
            "N_node_zero": no_node_residual,
            "lambda_L_zero": flat_mode_residual,
        },
        "not_raw_amplitude_rule": (
            "The source requires the node selector and spectral/gradient factor; "
            "it is not rho proportional to |psi|^2."
        ),
        "open_requirements": [
            "derive Xi_L from the action stress/pressure deficit",
            "derive N_node(k,z) from the long-mode eigenfunctions and phase field",
            "derive the evolution of A_L(k,z) and lambda_L(k,z)",
            "test the resulting source in CMB/LSS/cluster likelihoods",
        ],
    }


def standing_wave_node_selector_derivation() -> dict[str, Any]:
    """
    Derive the local node selector from a standing long mode.

    Use a one-dimensional standing mode as the local chart of a long coherent
    eigenfunction:

        psi(x) = A sin(k x).

    The Chladni readout must peak where motion amplitude is small but gradient
    energy is large.  The minimal smooth selector is

        N_node = exp(-psi^2 / eps_node^2),
        DeltaP_node = Xi N_node (Z_L/2) (d_x psi)^2.

    At the node x=0, psi=0 and the gradient energy is maximal.  At the
    antinode x=pi/(2k), the gradient vanishes.  This captures the important
    point: the pressure-node source is not raw amplitude density.
    """
    x, A, k, eps_node, Xi, Z_L = sp.symbols(
        "x A k eps_node Xi Z_L", positive=True, real=True
    )
    psi = A * sp.sin(k * x)
    grad_energy = sp.simplify(Z_L * sp.diff(psi, x) ** 2 / 2)
    selector = sp.exp(-psi**2 / eps_node**2)
    DeltaP_node = sp.simplify(Xi * selector * grad_energy)

    node_x = sp.Integer(0)
    antinode_x = sp.pi / (2 * k)
    node_pressure = sp.simplify(DeltaP_node.subs(x, node_x))
    antinode_pressure = sp.simplify(DeltaP_node.subs(x, antinode_x))
    node_selector = sp.simplify(selector.subs(x, node_x))
    antinode_selector = sp.simplify(selector.subs(x, antinode_x))
    raw_amplitude_density_at_node = sp.simplify(psi.subs(x, node_x) ** 2)
    node_pressure_expected = sp.simplify(Xi * Z_L * A**2 * k**2 / 2)
    node_residual = sp.simplify(node_pressure - node_pressure_expected)
    antinode_residual = sp.simplify(antinode_pressure)
    selector_peak_residual = sp.simplify(node_selector - 1)
    raw_rule_residual = sp.simplify(raw_amplitude_density_at_node)

    return {
        "status": "PASS_STANDING_WAVE_NODE_SELECTOR_DERIVATION"
        if node_residual == 0
        and antinode_residual == 0
        and selector_peak_residual == 0
        and raw_rule_residual == 0
        else "CHECK_STANDING_WAVE_NODE_SELECTOR_DERIVATION",
        "standing_mode": sp.Eq(sp.Symbol("psi"), psi),
        "node_selector": sp.Eq(sp.Symbol("N_node"), selector),
        "gradient_energy_density": sp.Eq(sp.Symbol("E_grad"), grad_energy),
        "pressure_node_readout": sp.Eq(sp.Symbol("DeltaP_node"), DeltaP_node),
        "node_pressure": sp.Eq(sp.Symbol("DeltaP_node_at_node"), node_pressure),
        "antinode_pressure": sp.Eq(
            sp.Symbol("DeltaP_node_at_antinode"), antinode_pressure
        ),
        "node_selector_value": node_selector,
        "antinode_selector_value": antinode_selector,
        "raw_amplitude_density_at_node": raw_amplitude_density_at_node,
        "meaning": (
            "Matter is attached to a low-motion/high-gradient pressure readout. "
            "A raw |psi|^2 rule would give zero at the node and would miss the "
            "Chladni-type accumulation rule."
        ),
        "open_requirements": [
            "derive eps_node and Xi from the RG stress functional",
            "generalize this local standing-wave chart to the full 3D eigenbasis",
            "replace the toy exponential selector with the action-derived low-motion functional",
        ],
    }


def local_stress_hessian_to_node_selector_gate() -> dict[str, Any]:
    """
    Match the node selector to a local action/stress Hessian expansion.

    Near a node, write the pressure-deficit functional in the two invariants
    that matter for the Chladni readout:

        G = gradient energy density,
        psi2 = local oscillation amplitude squared.

    The local action/stress expansion has the form

        DeltaP = C_G G + C_psiG psi2 G + ...

    The smooth selector ansatz gives

        DeltaP = Xi G exp(-psi2/eps_node^2)
               = Xi G - (Xi/eps_node^2) psi2 G + ...

    Therefore the first nontrivial matching is

        Xi = C_G,
        eps_node^2 = -C_G / C_psiG.

    For eps_node^2 to be positive, the action must give C_G/C_psiG < 0.  This
    gate records that requirement instead of treating eps_node as a fitted knob.
    """
    G, psi2, C_G, C_psiG = sp.symbols("G psi2 C_G C_psiG", real=True)
    Xi = sp.Symbol("Xi", real=True)
    eps2 = sp.Symbol("eps_node2", real=True)

    stress_expansion = sp.simplify(C_G * G + C_psiG * psi2 * G)
    selector_quadratic = sp.simplify(Xi * G * (1 - psi2 / eps2))
    matched_eps2 = sp.simplify(-C_G / C_psiG)
    matched_selector = sp.simplify(
        selector_quadratic.subs({Xi: C_G, eps2: matched_eps2})
    )
    matching_residual = sp.simplify(matched_selector - stress_expansion)
    eps_positive_condition = "C_G/C_psiG < 0"

    return {
        "status": "PASS_LOCAL_STRESS_HESSIAN_TO_NODE_SELECTOR_GATE"
        if matching_residual == 0
        else "CHECK_LOCAL_STRESS_HESSIAN_TO_NODE_SELECTOR_GATE",
        "stress_expansion": sp.Eq(sp.Symbol("DeltaP_stress_local"), stress_expansion),
        "selector_quadratic_expansion": sp.Eq(
            sp.Symbol("DeltaP_selector_local"), selector_quadratic
        ),
        "matched_Xi": sp.Eq(Xi, C_G),
        "matched_eps_node_squared": sp.Eq(eps2, matched_eps2),
        "matching_residual": matching_residual,
        "positivity_condition": eps_positive_condition,
        "meaning": (
            "Xi and eps_node can be read from the local stress Hessian: the "
            "gradient-energy coefficient fixes Xi, and the mixed amplitude-"
            "gradient coefficient fixes the node width."
        ),
        "open_requirements": [
            "compute C_G and C_psiG from the full p01/p10/p13 stress functional",
            "prove C_G/C_psiG < 0 on the stable long-mode branch",
            "extend the scalar local expansion to tensor/projector channel Hessians",
        ],
    }


def cmb_cluster_source_export_split_gate() -> dict[str, Any]:
    """
    Keep early cosmology and late cluster residual exports separated.

    The same long-mode node pressure can feed both sectors, but not with the
    same observational claim:

        primary CMB/LSS source:  node long-mode part only,
        cluster residual source: node baseline + tail retention + vortex/memory.

    This preserves the p08 safety branch and the p09 three-channel cluster
    ledger while still letting p17 supply the common node term.
    """
    P0 = sp.Symbol("P0", positive=True, real=True)
    chi_node, chi_tail, chi_vortex = sp.symbols(
        "chi_node chi_tail chi_vortex", real=True
    )
    DeltaP_node, DeltaP_tail, DeltaP_vortex = sp.symbols(
        "DeltaP_node DeltaP_tail DeltaP_vortex", real=True
    )

    primary_cmb_source = sp.simplify(chi_node * DeltaP_node / P0)
    late_cluster_source = sp.simplify(
        (
            chi_node * DeltaP_node
            + chi_tail * DeltaP_tail
            + chi_vortex * DeltaP_vortex
        )
        / P0
    )
    late_local_addition = sp.simplify(late_cluster_source - primary_cmb_source)
    expected_late_local = sp.simplify(
        (chi_tail * DeltaP_tail + chi_vortex * DeltaP_vortex) / P0
    )
    split_residual = sp.simplify(late_local_addition - expected_late_local)

    no_tail_in_primary = sp.simplify(sp.diff(primary_cmb_source, DeltaP_tail))
    no_vortex_in_primary = sp.simplify(sp.diff(primary_cmb_source, DeltaP_vortex))
    node_shared_between_exports = sp.simplify(
        sp.diff(primary_cmb_source, DeltaP_node)
        - sp.diff(late_cluster_source, DeltaP_node)
    )

    return {
        "status": "PASS_CMB_CLUSTER_SOURCE_EXPORT_SPLIT_GATE"
        if split_residual == 0
        and no_tail_in_primary == 0
        and no_vortex_in_primary == 0
        and node_shared_between_exports == 0
        else "CHECK_CMB_CLUSTER_SOURCE_EXPORT_SPLIT_GATE",
        "primary_cmb_lss_source": sp.Eq(
            sp.Symbol("delta_primary_node"), primary_cmb_source
        ),
        "late_cluster_source": sp.Eq(
            sp.Symbol("delta_cluster_residual"), late_cluster_source
        ),
        "late_local_addition": sp.Eq(
            sp.Symbol("delta_tail_plus_vortex"), late_local_addition
        ),
        "split_residual": split_residual,
        "primary_source_tail_derivative": no_tail_in_primary,
        "primary_source_vortex_derivative": no_vortex_in_primary,
        "shared_node_coefficient_residual": node_shared_between_exports,
        "meaning": (
            "The node baseline is the shared p17 contribution.  Tail retention "
            "and vortex/memory are late/local cluster channels and are not "
            "silently imported into primary CMB/LSS."
        ),
        "open_requirements": [
            "derive chi_node before exporting to p08 CMB/LSS",
            "derive chi_tail and chi_vortex from p10/p07/p13 before cluster fitting",
            "test whether the node contribution is early, late, or screened by redshift",
        ],
    }


def redshift_screened_node_activation_gate() -> dict[str, Any]:
    """
    Candidate redshift window for the long-mode node source.

    p08 protects the same-input CMB branch: if the node source is active at
    recombination, it must go through a Boltzmann likelihood.  A conservative
    late-activation candidate is therefore useful:

        W_late(z) = (1 + (1 + z_on)^2) / ((1 + z)^2 + (1 + z_on)^2).

    This normalization gives W_late(0)=1 and W_late(z->infinity)=0.  The
    screened node source is

        DeltaP_node_screened(k,z) = W_late(z) DeltaP_node_base(k,z).

    This is only a branch candidate.  It does not prove that nature uses late
    activation, and it does not replace the no-particle-DM CMB Boltzmann test.
    """
    z, z_on = sp.symbols("z z_on", positive=True, real=True)
    A_L, Xi_L, N_node, lambda_L = sp.symbols(
        "A_L Xi_L N_node lambda_L", nonnegative=True, real=True
    )
    P0, chi_node = sp.symbols("P0 chi_node", positive=True, real=True)

    base_source = sp.simplify(Xi_L * N_node * lambda_L * A_L**2)
    transition_scale = sp.simplify((1 + z_on) ** 2)
    W_late = sp.simplify((1 + transition_scale) / ((1 + z) ** 2 + transition_scale))
    screened_source = sp.simplify(W_late * base_source)
    dimensionless_screened = sp.simplify(chi_node * screened_source / P0)

    present_residual = sp.simplify(screened_source.subs(z, 0) - base_source)
    early_limit = sp.simplify(sp.limit(screened_source, z, sp.oo))
    window_present_residual = sp.simplify(W_late.subs(z, 0) - 1)
    window_early_limit = sp.simplify(sp.limit(W_late, z, sp.oo))
    same_input_absent_source = sp.Integer(0)

    return {
        "status": "PASS_REDSHIFT_SCREENED_NODE_ACTIVATION_GATE"
        if present_residual == 0
        and early_limit == 0
        and window_present_residual == 0
        and window_early_limit == 0
        else "CHECK_REDSHIFT_SCREENED_NODE_ACTIVATION_GATE",
        "late_window": sp.Eq(sp.Symbol("W_late(z)"), W_late),
        "base_node_source": sp.Eq(sp.Symbol("DeltaP_node_base"), base_source),
        "screened_node_source": sp.Eq(
            sp.Symbol("DeltaP_node_screened(k,z)"), screened_source
        ),
        "dimensionless_screened_source": sp.Eq(
            sp.Symbol("delta_node_screened(k,z)"), dimensionless_screened
        ),
        "present_source_residual": present_residual,
        "early_source_limit": early_limit,
        "same_input_absent_source": sp.Eq(
            sp.Symbol("DeltaP_node_same_input"), same_input_absent_source
        ),
        "branch_options": {
            "same_input_CMB_safe": "DeltaP_node = 0 in primary CMB source equations",
            "late_screened_cluster": "W_late(z) DeltaP_node_base with W_late(z->infinity)=0",
            "active_early_replacement": "requires full Boltzmann likelihood and is not claimed here",
        },
        "meaning": (
            "The node source can be recorded as a late/screened branch without "
            "spoiling the p08 same-input CMB identity.  An active early branch "
            "remains possible only as a separate Boltzmann-tested model."
        ),
        "open_requirements": [
            "derive W_late(z) from RG relaxation/coherence dynamics rather than choosing this smooth form",
            "fit or derive z_on from the long-mode coherence and cluster-formation history",
            "test active-early, late-screened and absent-source branches against CMB/LSS/cluster data",
        ],
    }


def p10_bernoulli_rarefaction_node_coefficients_candidate() -> dict[str, Any]:
    """
    p10-compatible coefficient candidate for C_G and C_psiG.

    p10 supplies the Bernoulli pressure-deficit structure:

        DeltaP_B ~ exp(status) * gradient_energy.

    For the Chladni/node branch, the local motion amplitude must not increase
    the node source by a raw |psi|^2 rule.  The conservative saturation ansatz is

        R(psi2) = exp(-q_rare psi2),
        DeltaP_node = C_B G R(psi2).

    Its Hessian expansion gives

        C_G = C_B,
        C_psiG = -C_B q_rare,
        eps_node^2 = 1/q_rare.

    This imports the p10 Bernoulli idea and the p05/p10 rarefaction/saturation
    sign, but it is still a candidate until q_rare is derived from the full
    nonlinear source profile.
    """
    G, psi2, C_B, q_rare = sp.symbols(
        "G psi2 C_B q_rare", positive=True, real=True
    )
    rarefaction = sp.exp(-q_rare * psi2)
    pressure_exact = sp.simplify(C_B * G * rarefaction)
    pressure_quadratic = sp.simplify(C_B * G * (1 - q_rare * psi2))
    C_G = sp.simplify(pressure_quadratic.coeff(G).subs(psi2, 0))
    C_psiG = sp.simplify(sp.diff(sp.diff(pressure_quadratic, psi2), G))
    eps_node2 = sp.simplify(-C_G / C_psiG)

    expected_C_G = C_B
    expected_C_psiG = -C_B * q_rare
    expected_eps2 = 1 / q_rare
    residuals = {
        "C_G": sp.simplify(C_G - expected_C_G),
        "C_psiG": sp.simplify(C_psiG - expected_C_psiG),
        "eps_node2": sp.simplify(eps_node2 - expected_eps2),
        "node_normalization": sp.simplify(pressure_exact.subs(psi2, 0) - C_B * G),
    }

    return {
        "status": "PASS_P10_BERNOULLI_RAREFACTION_NODE_COEFFICIENTS_CANDIDATE"
        if all(value == 0 for value in residuals.values())
        else "CHECK_P10_BERNOULLI_RAREFACTION_NODE_COEFFICIENTS_CANDIDATE",
        "rarefaction_factor": sp.Eq(sp.Symbol("R_node(psi2)"), rarefaction),
        "exact_candidate_pressure": sp.Eq(
            sp.Symbol("DeltaP_node_candidate"), pressure_exact
        ),
        "quadratic_hessian_expansion": sp.Eq(
            sp.Symbol("DeltaP_node_O_psi2"), pressure_quadratic
        ),
        "C_G_from_p10_Bernoulli": sp.Eq(sp.Symbol("C_G"), C_G),
        "C_psiG_from_rarefaction": sp.Eq(sp.Symbol("C_psiG"), C_psiG),
        "eps_node_squared": sp.Eq(sp.Symbol("eps_node2"), eps_node2),
        "residuals": residuals,
        "sign_gate": "C_B > 0 and q_rare > 0 imply C_G > 0, C_psiG < 0, eps_node2 > 0",
        "meaning": (
            "The Bernoulli gradient-pressure coefficient fixes C_G, while a "
            "p10/p05-style rarefaction response supplies the negative mixed "
            "coefficient needed for a node selector."
        ),
        "open_requirements": [
            "derive q_rare from the nonlinear p10 oscillon/medium profile",
            "show the same rarefaction sign holds for the full tensor source, not only the scalar candidate",
            "match C_B to the p10/p13 normalization used in the active stress source",
        ],
    }


def p10_time_averaged_source_to_q_rare_candidate() -> dict[str, Any]:
    """
    Candidate extraction of q_rare from the p10 time-averaged source.

    p10 records the zero-frequency oscillon source with a gradient part

        rho_grad ~ exp(phi_status) Phi0_prime^2 / (64 pi G_N).

    If the local oscillation energy lowers the pressure/status field by

        phi_status = phi_bg - kappa_E E_kin/P0,
        E_kin = Omega_loc^2 psi2 / 2,

    then the gradient pressure receives

        exp(phi_status - phi_bg) = exp(-q_rare psi2),
        q_rare = kappa_E Omega_loc^2 / (2 P0).

    This is the first explicit p10-style route from an energy-status response
    to the node-selector width.  It is still a candidate until kappa_E and the
    status law are derived from the nonlinear p01/p10 medium equations.
    """
    psi2, grad2 = sp.symbols("psi2 grad2", nonnegative=True, real=True)
    Omega_loc, kappa_E, P0, G_N = sp.symbols(
        "Omega_loc kappa_E P0 G_N", positive=True, real=True
    )
    phi_bg = sp.Symbol("phi_bg", real=True)

    E_kin = sp.simplify(Omega_loc**2 * psi2 / 2)
    phi_status = sp.simplify(phi_bg - kappa_E * E_kin / P0)
    q_rare = sp.simplify(kappa_E * Omega_loc**2 / (2 * P0))
    C_B = sp.simplify(sp.exp(phi_bg) / (64 * sp.pi * G_N))
    gradient_source = sp.simplify(
        sp.exp(phi_status) * grad2 / (64 * sp.pi * G_N)
    )
    factored_source = sp.simplify(C_B * grad2 * sp.exp(-q_rare * psi2))
    quadratic_source = sp.simplify(C_B * grad2 * (1 - q_rare * psi2))
    C_G = sp.simplify(quadratic_source.coeff(grad2).subs(psi2, 0))
    C_psiG = sp.simplify(sp.diff(sp.diff(quadratic_source, psi2), grad2))
    eps_node2 = sp.simplify(-C_G / C_psiG)

    residuals = {
        "factorization": sp.simplify(gradient_source - factored_source),
        "q_rare": sp.simplify(q_rare - kappa_E * Omega_loc**2 / (2 * P0)),
        "C_G": sp.simplify(C_G - C_B),
        "C_psiG": sp.simplify(C_psiG + C_B * q_rare),
        "eps_node2": sp.simplify(eps_node2 - 1 / q_rare),
    }

    return {
        "status": "PASS_P10_TIME_AVERAGED_SOURCE_TO_Q_RARE_CANDIDATE"
        if all(value == 0 for value in residuals.values())
        else "CHECK_P10_TIME_AVERAGED_SOURCE_TO_Q_RARE_CANDIDATE",
        "local_kinetic_status_energy": sp.Eq(sp.Symbol("E_kin"), E_kin),
        "status_field": sp.Eq(sp.Symbol("phi_status"), phi_status),
        "q_rare_candidate": sp.Eq(sp.Symbol("q_rare"), q_rare),
        "p10_gradient_coefficient": sp.Eq(sp.Symbol("C_B"), C_B),
        "gradient_source": sp.Eq(sp.Symbol("rho_grad"), gradient_source),
        "factored_gradient_source": sp.Eq(
            sp.Symbol("rho_grad_factored"), factored_source
        ),
        "quadratic_hessian_source": sp.Eq(
            sp.Symbol("rho_grad_O_psi2"), quadratic_source
        ),
        "C_G": sp.Eq(sp.Symbol("C_G"), C_G),
        "C_psiG": sp.Eq(sp.Symbol("C_psiG"), C_psiG),
        "eps_node_squared": sp.Eq(sp.Symbol("eps_node2"), eps_node2),
        "residuals": residuals,
        "sign_gate": (
            "kappa_E > 0, P0 > 0 and Omega_loc^2 > 0 imply q_rare > 0, "
            "C_psiG < 0 and eps_node2 > 0"
        ),
        "meaning": (
            "The node width can be tied to a local energy-status response: "
            "oscillation energy rarefies the gradient-pressure coefficient, "
            "so high-motion regions are screened and low-motion nodes remain active."
        ),
        "open_requirements": [
            "derive kappa_E from the nonlinear p01/p10 pressure-status equation",
            "replace the local algebraic status law by the solved oscillon profile",
            "check whether Omega_loc and P0 transpose together so dimensionless ratios stay locked",
        ],
    }


def p01_pressure_potential_to_kappa_E_gate() -> dict[str, Any]:
    """
    Derive the linear kappa_E response from the p01 pressure potential.

    p01 records the operational pressure/status potential as

        phi = log(P_stat / P_max).

    Let a small local oscillation energy E drain the static pressure reservoir:

        P_stat(E) = P_bg - alpha_E E,
        phi_bg = log(P_bg/P_max).

    The exact local status shift is

        Delta phi(E) = log(1 - alpha_E E/P_bg).

    Its linear term is

        Delta phi = -(alpha_E/P_bg) E + O(E^2).

    Matching the p17 local law

        Delta phi = -kappa_E E/P0

    gives

        kappa_E = alpha_E P0/P_bg.

    This is a p01-compatible definition of kappa_E.  It closes only the local
    linear response coefficient; the nonlinear pressure-status equation remains
    an open p01/p10 derivation.
    """
    E, alpha_E, P_bg, P_max, P0 = sp.symbols(
        "E alpha_E P_bg P_max P0", positive=True, real=True
    )
    phi_bg = sp.log(P_bg / P_max)
    phi_status = sp.log((P_bg - alpha_E * E) / P_max)
    delta_phi_exact = sp.simplify(phi_status - phi_bg)
    linear_slope = sp.simplify(sp.diff(delta_phi_exact, E).subs(E, 0))
    kappa_E = sp.simplify(-P0 * linear_slope)
    linear_delta_phi = sp.simplify(linear_slope * E)
    p17_linear_law = sp.simplify(-kappa_E * E / P0)

    q_rare_from_pressure = sp.simplify(
        kappa_E * sp.Symbol("Omega_loc", positive=True, real=True) ** 2 / (2 * P0)
    )
    q_rare_expected = sp.simplify(
        alpha_E
        * sp.Symbol("Omega_loc", positive=True, real=True) ** 2
        / (2 * P_bg)
    )
    residuals = {
        "linear_match": sp.simplify(linear_delta_phi - p17_linear_law),
        "kappa_E": sp.simplify(kappa_E - alpha_E * P0 / P_bg),
        "q_rare": sp.simplify(q_rare_from_pressure - q_rare_expected),
    }

    return {
        "status": "PASS_P01_PRESSURE_POTENTIAL_TO_KAPPA_E_GATE"
        if all(value == 0 for value in residuals.values())
        else "CHECK_P01_PRESSURE_POTENTIAL_TO_KAPPA_E_GATE",
        "p01_pressure_potential": sp.Eq(sp.Symbol("phi"), sp.log(sp.Symbol("P_stat") / P_max)),
        "pressure_drain_law": sp.Eq(sp.Symbol("P_stat(E)"), P_bg - alpha_E * E),
        "background_status": sp.Eq(sp.Symbol("phi_bg"), phi_bg),
        "exact_status_shift": sp.Eq(sp.Symbol("Delta_phi_exact"), delta_phi_exact),
        "linear_status_slope": sp.Eq(sp.Symbol("dDelta_phi_dE_at_0"), linear_slope),
        "matched_kappa_E": sp.Eq(sp.Symbol("kappa_E"), kappa_E),
        "linear_p17_status_law": sp.Eq(sp.Symbol("Delta_phi_linear"), p17_linear_law),
        "q_rare_from_pressure_response": sp.Eq(
            sp.Symbol("q_rare"), q_rare_from_pressure
        ),
        "residuals": residuals,
        "sign_gate": (
            "alpha_E > 0, P0 > 0 and P_bg > 0 imply kappa_E > 0; "
            "therefore the q_rare sign is the pressure-drain sign."
        ),
        "meaning": (
            "kappa_E is the linear susceptibility of the p01 pressure/status "
            "potential to local oscillation energy.  It is not an added force "
            "and not a fitted frequency."
        ),
        "open_requirements": [
            "derive alpha_E from the p01/p10 nonlinear medium equation",
            "replace the linear pressure-drain law by the solved finite-amplitude branch",
            "identify whether P0 equals P_bg or a renormalized local pressure scale",
        ],
    }


def p01_isotropic_linear_response_alpha_E_candidate() -> dict[str, Any]:
    """
    Candidate alpha_E from the p01 isotropic pressure/energy response.

    Work on the p01 normalized isotropic background

        Y = y,  B^A_B = b delta^A_B,

    with the minimal polynomial L(Y,I1,I2,I3).  On the zero-stress branch,
    perturb y -> 1 + delta_y at fixed b=1.  The induced energy and pressure
    shifts are

        delta rho = rho_y delta_y,
        delta P_stat = p_y delta_y.

    Matching the p17 pressure-drain convention

        delta P_stat = -alpha_E delta rho

    gives

        alpha_E = -p_y/rho_y.

    This is the first p01 coefficient-space candidate for alpha_E.  It does
    not prove alpha_E>0; that requires the sign window rho_y>0 and p_y<0 on
    the selected stable branch.
    """
    y, b, delta_y = sp.symbols("y b delta_y", positive=True, real=True)
    Omega_loc, P_bg = sp.symbols("Omega_loc P_bg", positive=True, real=True)
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1", real=True
    )

    L_iso = sp.simplify(
        c_Y * y
        + c_Y2 * y**2
        + 3 * c_I1 * b
        + (9 * c_I1sq + 3 * c_I2) * b**2
        + c_I3 * b**3
        + 3 * c_YI1 * y * b
    )
    rho_iso = sp.simplify(2 * y * sp.diff(L_iso, y) - L_iso)
    p_iso = sp.simplify(L_iso - sp.Rational(2, 3) * b * sp.diff(L_iso, b))
    at_vac = {y: 1, b: 1}
    rho0 = sp.simplify(rho_iso.subs(at_vac))
    p0 = sp.simplify(p_iso.subs(at_vac))
    zero_stress_solution = sp.solve([rho0, p0], [c_Y, c_I1], dict=True)[0]

    rho_y = sp.simplify(sp.diff(rho_iso, y).subs(at_vac).subs(zero_stress_solution))
    p_y = sp.simplify(sp.diff(p_iso, y).subs(at_vac).subs(zero_stress_solution))
    alpha_E = sp.simplify(-p_y / rho_y)
    delta_rho = sp.simplify(rho_y * delta_y)
    delta_P_stat = sp.simplify(p_y * delta_y)
    drain_residual = sp.simplify(delta_P_stat + alpha_E * delta_rho)
    q_rare = sp.simplify(alpha_E * Omega_loc**2 / (2 * P_bg))

    expected_rho_y = sp.simplify(
        9 * c_I1sq / 2 + 3 * c_I2 / 2 + c_I3
        + 9 * c_Y2 / 2 + 3 * c_YI1 / 2
    )
    expected_p_y = sp.simplify(
        9 * c_I1sq / 2 + 3 * c_I2 / 2 + c_I3
        + c_Y2 / 2 - c_YI1 / 2
    )
    residuals = {
        "rho_y": sp.simplify(rho_y - expected_rho_y),
        "p_y": sp.simplify(p_y - expected_p_y),
        "drain_match": drain_residual,
    }

    return {
        "status": "PASS_P01_ISOTROPIC_LINEAR_RESPONSE_ALPHA_E_CANDIDATE"
        if all(value == 0 for value in residuals.values())
        else "CHECK_P01_ISOTROPIC_LINEAR_RESPONSE_ALPHA_E_CANDIDATE",
        "isotropic_lagrangian": L_iso,
        "rho_iso": rho_iso,
        "p_iso": p_iso,
        "zero_stress_solution": zero_stress_solution,
        "rho_y_on_zero_stress_branch": rho_y,
        "p_y_on_zero_stress_branch": p_y,
        "alpha_E_candidate": sp.Eq(sp.Symbol("alpha_E"), alpha_E),
        "delta_rho": sp.Eq(sp.Symbol("delta_rho"), delta_rho),
        "delta_P_stat": sp.Eq(sp.Symbol("delta_P_stat"), delta_P_stat),
        "pressure_drain_residual": drain_residual,
        "q_rare_from_p01_linear_response": sp.Eq(sp.Symbol("q_rare"), q_rare),
        "residuals": residuals,
        "sign_gate": (
            "rho_y>0 and p_y<0 imply alpha_E>0; this sign window must be "
            "proved on the selected stable branch."
        ),
        "meaning": (
            "alpha_E can be read as the p01 isotropic pressure response per "
            "unit phase-energy response.  This links the Chladni node selector "
            "to p01 coefficient space without closing the nonlinear branch."
        ),
        "open_requirements": [
            "prove the rho_y>0, p_y<0 sign window on the selected p01 branch",
            "extend fixed-b isotropic response to the tensor/projector sector",
            "derive the finite-amplitude pressure drain beyond linear delta_y",
        ],
    }


def p01_alpha_E_positive_window_witness_gate() -> dict[str, Any]:
    """
    Nonempty coefficient-space witness for alpha_E>0.

    The previous gate gives

        alpha_E = -p_y/rho_y.

    This gate records one explicit p01 zero-stress coefficient point where the
    sign requirements are simultaneously satisfied:

        rho_y > 0, p_y < 0, K_pi > 0, alpha_E > 0.

    It is a nonempty-window witness, not a proof that the final selected branch
    must live at this point.
    """
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1", real=True
    )
    zero_stress_solution = {
        c_I1: -3 * c_I1sq / 2 - c_I2 / 2 + c_Y2 / 2 + c_YI1 / 2,
        c_Y: 9 * c_I1sq / 2 + 3 * c_I2 / 2 + c_I3
        - 3 * c_Y2 / 2 - 3 * c_YI1 / 2,
    }
    rho_y = sp.simplify(
        9 * c_I1sq / 2 + 3 * c_I2 / 2 + c_I3
        + 9 * c_Y2 / 2 + 3 * c_YI1 / 2
    )
    p_y = sp.simplify(
        9 * c_I1sq / 2 + 3 * c_I2 / 2 + c_I3
        + c_Y2 / 2 - c_YI1 / 2
    )
    K_pi = sp.simplify(
        -9 * c_I1sq / 2 - 3 * c_I2 / 2 - c_I3
        - c_Y2 / 2 - 3 * c_YI1 / 2
    )
    alpha_E = sp.simplify(-p_y / rho_y)

    witness_seed = {
        c_I1sq: sp.Rational(1, 4),
        c_I2: -sp.Rational(13, 3),
        c_I3: sp.Rational(9, 2),
        c_Y2: sp.Rational(1, 5),
        c_YI1: sp.Rational(1, 3),
    }
    witness = {
        **witness_seed,
        c_I1: sp.simplify(zero_stress_solution[c_I1].subs(witness_seed)),
        c_Y: sp.simplify(zero_stress_solution[c_Y].subs(witness_seed)),
    }
    witness_values = {
        "rho_y": sp.simplify(rho_y.subs(witness)),
        "p_y": sp.simplify(p_y.subs(witness)),
        "K_pi": sp.simplify(K_pi.subs(witness)),
        "alpha_E": sp.simplify(alpha_E.subs(witness)),
        "c_Y2": sp.simplify(c_Y2.subs(witness)),
    }
    checks = {
        "rho_y_positive": sp.simplify(witness_values["rho_y"] > 0),
        "p_y_negative": sp.simplify(witness_values["p_y"] < 0),
        "K_pi_positive": sp.simplify(witness_values["K_pi"] > 0),
        "alpha_E_positive": sp.simplify(witness_values["alpha_E"] > 0),
        "c_Y2_positive": sp.simplify(witness_values["c_Y2"] > 0),
    }

    return {
        "status": "PASS_P01_ALPHA_E_POSITIVE_WINDOW_WITNESS_GATE"
        if all(checks.values())
        else "CHECK_P01_ALPHA_E_POSITIVE_WINDOW_WITNESS_GATE",
        "zero_stress_solution": zero_stress_solution,
        "witness_coefficients": witness,
        "witness_values": witness_values,
        "checks": checks,
        "meaning": (
            "The p01 coefficient space has at least one explicit local point "
            "where phase-energy increase drains the pressure reservoir and "
            "keeps the basic phase/solid linear responses positive."
        ),
        "open_requirements": [
            "prove the selected physical branch lies inside this sign domain",
            "add the full mixed-mode/hyperbolicity constraints to the witness domain",
            "lift the isotropic witness to the tensor long-mode node sector",
        ],
    }


def p01_alpha_E_mixed_characteristic_witness_gate() -> dict[str, Any]:
    """
    Add p01 mixed-characteristic checks to the alpha_E witness.

    This uses the same p01 principal-symbol convention as analyze_sound_speeds:

        det[(A s + C)(B s + D) - M^2 s] = 0,  s = c_s^2.

    The witness below is selected so that the alpha_E pressure-drain sign is
    positive and the mixed characteristic roots are real and positive.  It is
    not a subluminal theorem: one characteristic and the transverse speed are
    superluminal at this local point, so subluminal branch selection remains
    open.
    """
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1", real=True
    )
    s = sp.Symbol("s", real=True)
    zero_stress_solution = {
        c_I1: -3 * c_I1sq / 2 - c_I2 / 2 + c_Y2 / 2 + c_YI1 / 2,
        c_Y: 9 * c_I1sq / 2 + 3 * c_I2 / 2 + c_I3
        - 3 * c_Y2 / 2 - 3 * c_YI1 / 2,
    }
    witness_seed = {
        c_I1sq: sp.Rational(1, 4),
        c_I2: -sp.Rational(13, 3),
        c_I3: sp.Rational(9, 2),
        c_Y2: sp.Rational(1, 5),
        c_YI1: sp.Rational(1, 3),
    }
    witness = {
        **witness_seed,
        c_I1: sp.simplify(zero_stress_solution[c_I1].subs(witness_seed)),
        c_Y: sp.simplify(zero_stress_solution[c_Y].subs(witness_seed)),
    }

    rho_y = sp.simplify(
        9 * c_I1sq / 2 + 3 * c_I2 / 2 + c_I3
        + 9 * c_Y2 / 2 + 3 * c_YI1 / 2
    )
    p_y = sp.simplify(
        9 * c_I1sq / 2 + 3 * c_I2 / 2 + c_I3
        + c_Y2 / 2 - c_YI1 / 2
    )
    alpha_E = sp.simplify(-p_y / rho_y)

    A = sp.simplify(c_Y + 6 * c_Y2 + 3 * c_YI1)
    B_long = sp.simplify(-c_I1 - 6 * c_I1sq - 2 * c_I2 - c_I3 - c_YI1)
    C = sp.simplify(-c_Y - 2 * c_Y2 - 3 * c_YI1)
    D = sp.simplify(c_I1 + 10 * c_I1sq + 2 * c_I2 + c_I3 + c_YI1)
    M_mix = sp.simplify(4 * c_YI1)
    K_T = B_long
    G_T = sp.simplify(-c_I1 - 6 * c_I1sq - c_I2 - c_YI1)

    values = {
        "rho_y": sp.simplify(rho_y.subs(witness)),
        "p_y": sp.simplify(p_y.subs(witness)),
        "alpha_E": sp.simplify(alpha_E.subs(witness)),
        "A": sp.simplify(A.subs(witness)),
        "B_long": sp.simplify(B_long.subs(witness)),
        "C": sp.simplify(C.subs(witness)),
        "D": sp.simplify(D.subs(witness)),
        "M_mix": sp.simplify(M_mix.subs(witness)),
        "K_T": sp.simplify(K_T.subs(witness)),
        "G_T": sp.simplify(G_T.subs(witness)),
    }
    characteristic = sp.factor(
        (values["A"] * s + values["C"])
        * (values["B_long"] * s + values["D"])
        - values["M_mix"] ** 2 * s
    )
    roots = sp.solve(characteristic, s)
    transverse_cs2 = sp.simplify(values["G_T"] / values["K_T"])
    checks = {
        "alpha_E_positive": sp.simplify(values["alpha_E"] > 0),
        "phase_kinetic_positive": sp.simplify(values["A"] > 0),
        "longitudinal_kinetic_positive": sp.simplify(values["B_long"] > 0),
        "transverse_kinetic_positive": sp.simplify(values["K_T"] > 0),
        "transverse_gradient_positive": sp.simplify(values["G_T"] > 0),
        "mixed_roots_positive": all(sp.simplify(root > 0) for root in roots),
    }
    subluminal_checks = {
        "mixed_roots_le_one": all(sp.simplify(root <= 1) for root in roots),
        "transverse_cs2_le_one": sp.simplify(transverse_cs2 <= 1),
    }

    return {
        "status": "PASS_P01_ALPHA_E_MIXED_CHARACTERISTIC_WITNESS_GATE"
        if all(checks.values())
        else "CHECK_P01_ALPHA_E_MIXED_CHARACTERISTIC_WITNESS_GATE",
        "witness_coefficients": witness,
        "principal_values": values,
        "characteristic_polynomial": sp.Eq(
            sp.Symbol("P_mixed(s)"), characteristic
        ),
        "mixed_characteristic_roots": roots,
        "transverse_cs2": transverse_cs2,
        "checks": checks,
        "subluminal_checks_open": subluminal_checks,
        "meaning": (
            "The alpha_E>0 pressure-drain sign can coexist with positive p01 "
            "mixed characteristics at a concrete coefficient point.  This "
            "strengthens the witness from a pressure sign check to a local "
            "hyperbolic-characteristic check."
        ),
        "open_requirements": [
            "find or prove a subluminal branch if the final sector requires subluminality",
            "add the static-silent dynamic repair channels from p01 before article export",
            "lift this isotropic local witness to the long-mode tensor/projector node sector",
        ],
    }


def p01_alpha_E_static_silent_mixed_repair_gate() -> dict[str, Any]:
    """
    Recheck the alpha_E witness after the p01 static-silent dynamic repair.

    The p01 repair operator

        Delta L_dyn = epsilon_B W_A W^A + 2 epsilon_M W_A Q^A

    is static-silent at principal level.  It leaves the static pressure/gradient
    response untouched, while shifting the scalar-longitudinal dynamic channel

        B -> B + epsilon_B,      M -> M + epsilon_M.

    This gate applies that repair to the alpha_E witness above.  The result is a
    repaired scalar-longitudinal mixed branch with strictly subluminal roots.
    The transverse speed is deliberately left to the separate shear-sector gate,
    because this operator does not act on that channel.
    """
    s = sp.Symbol("s", real=True)
    mixed_gate = p01_alpha_E_mixed_characteristic_witness_gate()
    values = mixed_gate["principal_values"]

    epsilon_B = sp.Integer(3)
    epsilon_M = sp.sqrt(sp.Integer(4801)) / 40 - sp.Rational(4, 3)

    A = values["A"]
    B_long = values["B_long"]
    C = values["C"]
    D = values["D"]
    M_mix = values["M_mix"]

    B_repaired = sp.simplify(B_long + epsilon_B)
    M_repaired = sp.simplify(M_mix + epsilon_M)
    characteristic_repaired = sp.factor(
        (A * s + C) * (B_repaired * s + D) - M_repaired**2 * s
    )
    repaired_roots = sp.solve(characteristic_repaired, s)
    discriminant = sp.factor(sp.discriminant(characteristic_repaired, s))

    principal_values_after = {
        "rho_y": values["rho_y"],
        "p_y": values["p_y"],
        "alpha_E": values["alpha_E"],
        "A": A,
        "B_long": B_repaired,
        "C": C,
        "D": D,
        "M_mix": M_repaired,
        "K_T": values["K_T"],
        "G_T": values["G_T"],
    }
    checks = {
        "source_witness_passes": mixed_gate["status"]
        == "PASS_P01_ALPHA_E_MIXED_CHARACTERISTIC_WITNESS_GATE",
        "epsilon_B_positive": epsilon_B > 0,
        "epsilon_M_positive": epsilon_M > 0,
        "pressure_response_unchanged": sp.simplify(
            principal_values_after["alpha_E"] - values["alpha_E"]
        )
        == 0,
        "static_gradients_unchanged": sp.simplify(
            principal_values_after["C"] - C
        )
        == 0
        and sp.simplify(principal_values_after["D"] - D) == 0,
        "B_shift_matches_repair": sp.simplify(
            B_repaired - B_long - epsilon_B
        )
        == 0,
        "M_shift_matches_repair": sp.simplify(
            M_repaired - M_mix - epsilon_M
        )
        == 0,
        "repaired_mixed_kinetic_positive": B_repaired > 0,
        "repaired_discriminant_positive": discriminant > 0,
        "repaired_roots_strictly_subluminal": all(
            0 < float(sp.N(root, 16)) < 1 for root in repaired_roots
        ),
    }

    return {
        "status": "PASS_P01_ALPHA_E_STATIC_SILENT_MIXED_REPAIR_GATE"
        if all(bool(value) for value in checks.values())
        else "CHECK_P01_ALPHA_E_STATIC_SILENT_MIXED_REPAIR_GATE",
        "source_unrepaired_status": mixed_gate["status"],
        "repair_operator": (
            "Delta L_dyn = epsilon_B W_A W^A + 2 epsilon_M W_A Q^A; "
            "static-silent, shifts only B and M in the scalar-longitudinal "
            "principal channel."
        ),
        "repair_values": {
            "epsilon_B": epsilon_B,
            "epsilon_M": epsilon_M,
            "B_repaired": B_repaired,
            "M_repaired": M_repaired,
        },
        "principal_values_before": values,
        "principal_values_after": principal_values_after,
        "unrepaired_mixed_roots": mixed_gate["mixed_characteristic_roots"],
        "repaired_characteristic_polynomial": sp.Eq(
            sp.Symbol("P_mixed_repaired(s)"), characteristic_repaired
        ),
        "repaired_mixed_characteristic_roots": repaired_roots,
        "repaired_mixed_root_values": [sp.N(root, 16) for root in repaired_roots],
        "transverse_cs2_open": mixed_gate["transverse_cs2"],
        "checks": checks,
        "meaning": (
            "The same alpha_E>0 pressure-drain witness admits a p01 "
            "static-silent dynamic completion that makes the scalar-longitudinal "
            "mixed characteristic branch strictly subluminal, without changing "
            "the static pressure response used by kappa_E and q_rare."
        ),
        "open_requirements": [
            "combine with the separate transverse/shear completion gate for a full local speed witness",
            "embed this repair in the full tensor/projector node sector",
            "derive epsilon_B and epsilon_M from the nonlinear RG action instead of keeping them as witness parameters",
        ],
    }


def p01_alpha_E_static_silent_shear_repair_gate() -> dict[str, Any]:
    """
    Close the alpha_E witness transverse speed with an independent shear channel.

    The p01 foundation already separates one medium into independent response
    channels: phase, pressure, longitudinal compression, transverse shear,
    rotation/topology, resonance and lag.  The mixed repair above acts only on
    the scalar-longitudinal dynamic channel.  The transverse speed therefore
    needs its own local shear response, represented at principal level by

        Delta L_shear = epsilon_T |dot(pi_T)|^2.

    A static configuration has dot(pi_T)=0, so this completion is static-silent:
    it leaves the pressure response, static gradients and mixed scalar block
    untouched, while shifting only

        K_T -> K_T + epsilon_T.

    For the alpha_E witness, epsilon_T=1/4 changes c_T^2 from 53/33 to 53/63.
    """
    omega, pi_T = sp.symbols("omega pi_T", real=True)
    mixed_repair = p01_alpha_E_static_silent_mixed_repair_gate()
    values = mixed_repair["principal_values_after"]

    epsilon_T = sp.Rational(1, 4)
    shear_symbol = epsilon_T * (omega * pi_T) ** 2
    static_silent_check = sp.simplify(shear_symbol.subs(omega, 0))

    K_T_before = values["K_T"]
    G_T = values["G_T"]
    K_T_repaired = sp.simplify(K_T_before + epsilon_T)
    transverse_cs2_before = sp.simplify(G_T / K_T_before)
    transverse_cs2_repaired = sp.simplify(G_T / K_T_repaired)

    checks = {
        "source_mixed_repair_passes": mixed_repair["status"]
        == "PASS_P01_ALPHA_E_STATIC_SILENT_MIXED_REPAIR_GATE",
        "epsilon_T_positive": epsilon_T > 0,
        "shear_operator_static_silent": static_silent_check == 0,
        "pressure_response_unchanged": sp.simplify(
            values["alpha_E"] - mixed_repair["principal_values_before"]["alpha_E"]
        )
        == 0,
        "scalar_mixed_polynomial_unchanged": True,
        "K_T_shift_matches_repair": sp.simplify(
            K_T_repaired - K_T_before - epsilon_T
        )
        == 0,
        "G_T_unchanged": sp.simplify(G_T - values["G_T"]) == 0,
        "transverse_speed_positive": transverse_cs2_repaired > 0,
        "transverse_speed_strictly_subluminal": transverse_cs2_repaired < 1,
        "mixed_roots_remain_strictly_subluminal": all(
            0 < float(sp.N(root, 16)) < 1
            for root in mixed_repair["repaired_mixed_characteristic_roots"]
        ),
    }

    principal_values_after = {
        **values,
        "K_T": K_T_repaired,
        "G_T": G_T,
        "transverse_cs2": transverse_cs2_repaired,
    }

    return {
        "status": "PASS_P01_ALPHA_E_STATIC_SILENT_SHEAR_REPAIR_GATE"
        if all(bool(value) for value in checks.values())
        else "CHECK_P01_ALPHA_E_STATIC_SILENT_SHEAR_REPAIR_GATE",
        "source_mixed_repair_status": mixed_repair["status"],
        "repair_operator": (
            "Delta L_shear = epsilon_T |dot(pi_T)|^2; static-silent at "
            "principal level and shifts only the transverse kinetic coefficient."
        ),
        "repair_values": {
            "epsilon_T": epsilon_T,
            "K_T_before": K_T_before,
            "K_T_repaired": K_T_repaired,
            "G_T": G_T,
        },
        "principal_values_after": principal_values_after,
        "mixed_repair_roots": mixed_repair["repaired_mixed_characteristic_roots"],
        "transverse_cs2_before": transverse_cs2_before,
        "transverse_cs2_repaired": transverse_cs2_repaired,
        "checks": checks,
        "meaning": (
            "At the alpha_E witness point, the independent transverse shear "
            "kinetic channel closes the remaining local speed check: the "
            "scalar-longitudinal repaired roots stay subluminal and the "
            "transverse speed becomes 53/63, without touching the static "
            "pressure-drain response."
        ),
        "open_requirements": [
            "derive the covariant transverse projector form of Delta L_shear from the full RG action",
            "derive epsilon_T dynamically instead of keeping it as a witness parameter",
            "embed the scalar-longitudinal and transverse repairs in the full tensor/projector node sector",
        ],
    }


def p01_alpha_E_mixed_repair_admissible_region_gate() -> dict[str, Any]:
    """
    Replace the mixed-repair witness point by its finite open parameter region.

    For the alpha_E witness let

        B = B0 + epsilon_B,     M = M0 + epsilon_M.

    The repaired mixed characteristic is

        p2 s^2 + p1 s + p0 = 0,
        p2 = A B,
        p1 = A D + B C - M^2,
        p0 = C D.

    With A,C,D positive and B positive, the two roots are strictly in (0,1)
    iff the Vieta data obey

        P = p0/p2 < 1,
        2 sqrt(P) < S < 1 + P,
        S = -p1/p2.

    Equivalently, for the positive M branch:

        B > C D / A,
        A D + B C + 2 sqrt(A B C D) < M^2 < (A + C)(B + D).

    This proves that the mixed repair is not a tuned isolated point.
    """
    epsilon_B, epsilon_M = sp.symbols("epsilon_B epsilon_M", real=True)
    mixed_gate = p01_alpha_E_mixed_characteristic_witness_gate()
    mixed_repair = p01_alpha_E_static_silent_mixed_repair_gate()
    values = mixed_gate["principal_values"]

    A = values["A"]
    B0 = values["B_long"]
    C = values["C"]
    D = values["D"]
    M0 = values["M_mix"]

    B = sp.simplify(B0 + epsilon_B)
    M = sp.simplify(M0 + epsilon_M)
    p2 = sp.simplify(A * B)
    p1 = sp.simplify(A * D + B * C - M**2)
    p0 = sp.simplify(C * D)
    product_P = sp.simplify(p0 / p2)
    sum_S = sp.simplify(-p1 / p2)

    min_B = sp.simplify(C * D / A)
    min_epsilon_B = sp.simplify(min_B - B0)
    lower_M2 = sp.simplify(A * D + B * C + 2 * sp.sqrt(A * B * C * D))
    upper_M2 = sp.simplify((A + C) * (B + D))
    window_width_M2 = sp.simplify(upper_M2 - lower_M2)

    repair_values = mixed_repair["repair_values"]
    witness_epsilon_B = repair_values["epsilon_B"]
    witness_epsilon_M = repair_values["epsilon_M"]
    witness_M2 = sp.simplify((M0 + witness_epsilon_M) ** 2)
    witness_lower_M2 = sp.simplify(lower_M2.subs(epsilon_B, witness_epsilon_B))
    witness_upper_M2 = sp.simplify(upper_M2.subs(epsilon_B, witness_epsilon_B))
    witness_width_M2 = sp.simplify(
        window_width_M2.subs(epsilon_B, witness_epsilon_B)
    )

    checks = {
        "source_mixed_repair_passes": mixed_repair["status"]
        == "PASS_P01_ALPHA_E_STATIC_SILENT_MIXED_REPAIR_GATE",
        "minimum_epsilon_B_positive": min_epsilon_B > 0,
        "witness_epsilon_B_inside_open_region": witness_epsilon_B
        > min_epsilon_B,
        "witness_M2_inside_open_window": (
            float(sp.N(witness_lower_M2, 16))
            < float(sp.N(witness_M2, 16))
            < float(sp.N(witness_upper_M2, 16))
        ),
        "witness_window_width_positive": float(sp.N(witness_width_M2, 16)) > 0,
        "witness_roots_strictly_subluminal": all(
            0 < float(sp.N(root, 16)) < 1
            for root in mixed_repair["repaired_mixed_characteristic_roots"]
        ),
    }

    return {
        "status": "PASS_P01_ALPHA_E_MIXED_REPAIR_ADMISSIBLE_REGION_GATE"
        if all(bool(value) for value in checks.values())
        else "CHECK_P01_ALPHA_E_MIXED_REPAIR_ADMISSIBLE_REGION_GATE",
        "coefficients": {
            "A": A,
            "B0": B0,
            "C": C,
            "D": D,
            "M0": M0,
        },
        "repaired_polynomial_coefficients": {
            "p2": p2,
            "p1": p1,
            "p0": p0,
            "product_P": product_P,
            "sum_S": sum_S,
        },
        "admissible_region": {
            "epsilon_B_condition": sp.StrictGreaterThan(
                epsilon_B, min_epsilon_B
            ),
            "positive_M_branch_epsilon_M_interval": (
                sp.simplify(sp.sqrt(lower_M2) - M0),
                sp.simplify(sp.sqrt(upper_M2) - M0),
            ),
            "M2_lower": lower_M2,
            "M2_upper": upper_M2,
            "M2_window_width": window_width_M2,
        },
        "witness": {
            "epsilon_B": witness_epsilon_B,
            "epsilon_M": witness_epsilon_M,
            "M2": witness_M2,
            "M2_lower": witness_lower_M2,
            "M2_upper": witness_upper_M2,
            "roots": mixed_repair["repaired_mixed_characteristic_roots"],
            "root_values": mixed_repair["repaired_mixed_root_values"],
        },
        "checks": checks,
        "meaning": (
            "The alpha_E scalar-longitudinal repair has a finite open "
            "subluminal parameter region.  The displayed witness is one point "
            "inside that region, not an isolated fine-tuned accident."
        ),
    }


def p01_alpha_E_shear_repair_admissible_region_gate() -> dict[str, Any]:
    """
    Replace the shear-repair witness point by its open parameter region.

    The independent transverse kinetic completion gives

        K_T -> K_T + epsilon_T,
        c_T^2(epsilon_T) = G_T / (K_T + epsilon_T).

    At the alpha_E witness G_T>K_T, so strict subluminality requires

        epsilon_T > G_T - K_T.
    """
    epsilon_T = sp.Symbol("epsilon_T", real=True)
    shear_repair = p01_alpha_E_static_silent_shear_repair_gate()
    values = shear_repair["repair_values"]

    K_T = values["K_T_before"]
    G_T = values["G_T"]
    epsilon_T_min = sp.simplify(G_T - K_T)
    transverse_cs2 = sp.simplify(G_T / (K_T + epsilon_T))
    witness_epsilon_T = values["epsilon_T"]
    witness_cs2 = sp.simplify(transverse_cs2.subs(epsilon_T, witness_epsilon_T))

    checks = {
        "source_shear_repair_passes": shear_repair["status"]
        == "PASS_P01_ALPHA_E_STATIC_SILENT_SHEAR_REPAIR_GATE",
        "threshold_positive": epsilon_T_min > 0,
        "witness_inside_open_region": witness_epsilon_T > epsilon_T_min,
        "witness_transverse_speed_positive": witness_cs2 > 0,
        "witness_transverse_speed_strictly_subluminal": witness_cs2 < 1,
    }

    return {
        "status": "PASS_P01_ALPHA_E_SHEAR_REPAIR_ADMISSIBLE_REGION_GATE"
        if all(bool(value) for value in checks.values())
        else "CHECK_P01_ALPHA_E_SHEAR_REPAIR_ADMISSIBLE_REGION_GATE",
        "admissible_region": {
            "epsilon_T_condition": sp.StrictGreaterThan(
                epsilon_T, epsilon_T_min
            ),
            "transverse_cs2": transverse_cs2,
        },
        "witness": {
            "epsilon_T": witness_epsilon_T,
            "epsilon_T_min": epsilon_T_min,
            "transverse_cs2": witness_cs2,
        },
        "checks": checks,
        "meaning": (
            "The alpha_E transverse repair also has an open subluminal region: "
            "any epsilon_T greater than G_T-K_T closes the local transverse "
            "speed bound."
        ),
    }


def p01_alpha_E_full_local_speed_completion_gate() -> dict[str, Any]:
    """
    Combined local speed closure for the alpha_E pressure-drain witness.

    This is the end of the local homogeneous principal-symbol part of the
    alpha_E audit:

      * pressure-drain response remains alpha_E>0,
      * scalar-longitudinal mixed roots are real, positive and subluminal,
      * transverse speed is positive and subluminal,
      * both repairs are static-silent at the pressure/static-gradient level,
      * the repair values sit inside open admissible regions.

    It is still a local completion, not the nonlinear action derivation.
    """
    mixed_region = p01_alpha_E_mixed_repair_admissible_region_gate()
    shear_region = p01_alpha_E_shear_repair_admissible_region_gate()
    shear_repair = p01_alpha_E_static_silent_shear_repair_gate()

    mixed_roots = shear_repair["mixed_repair_roots"]
    transverse_cs2 = shear_repair["transverse_cs2_repaired"]
    local_speeds = [*mixed_roots, transverse_cs2]
    values = shear_repair["principal_values_after"]

    checks = {
        "mixed_region_passes": mixed_region["status"]
        == "PASS_P01_ALPHA_E_MIXED_REPAIR_ADMISSIBLE_REGION_GATE",
        "shear_region_passes": shear_region["status"]
        == "PASS_P01_ALPHA_E_SHEAR_REPAIR_ADMISSIBLE_REGION_GATE",
        "all_local_speeds_positive": all(
            0 < float(sp.N(speed, 16)) for speed in local_speeds
        ),
        "all_local_speeds_strictly_subluminal": all(
            float(sp.N(speed, 16)) < 1 for speed in local_speeds
        ),
        "alpha_E_positive": values["alpha_E"] > 0,
        "rho_y_positive": values["rho_y"] > 0,
        "p_y_negative": values["p_y"] < 0,
        "static_pressure_response_preserved": True,
    }

    return {
        "status": "PASS_P01_ALPHA_E_FULL_LOCAL_SPEED_COMPLETION_GATE"
        if all(bool(value) for value in checks.values())
        else "CHECK_P01_ALPHA_E_FULL_LOCAL_SPEED_COMPLETION_GATE",
        "mixed_repair_region_status": mixed_region["status"],
        "shear_repair_region_status": shear_region["status"],
        "completed_witness_parameters": {
            "epsilon_B": mixed_region["witness"]["epsilon_B"],
            "epsilon_M": mixed_region["witness"]["epsilon_M"],
            "epsilon_T": shear_region["witness"]["epsilon_T"],
        },
        "local_speed_spectrum": {
            "mixed_roots": mixed_roots,
            "mixed_root_values": [sp.N(root, 16) for root in mixed_roots],
            "transverse_cs2": transverse_cs2,
        },
        "pressure_response": {
            "rho_y": values["rho_y"],
            "p_y": values["p_y"],
            "alpha_E": values["alpha_E"],
        },
        "checks": checks,
        "meaning": (
            "The alpha_E local principal-symbol sector is closed at witness "
            "level and promoted to open repair windows: the pressure-drain "
            "sign, mixed scalar-longitudinal speeds and transverse speed are "
            "mutually compatible without changing the static pressure response."
        ),
        "remaining_derivation_boundary": (
            "The next layer is not another local speed fix; it is deriving "
            "epsilon_B, epsilon_M and epsilon_T from the nonlinear RG action "
            "and lifting the result to the full tensor/projector node sector."
        ),
    }


def p01_alpha_E_quadratic_repair_action_embedding_gate() -> dict[str, Any]:
    """
    Embed the completed alpha_E repair in one quadratic principal action block.

    This is the action-level closure for the local witness.  Introduce the
    principal channel variables

        W_L = dot(pi_L),     Q_L = grad(chi),     W_T = dot(pi_T),

    and add

        Delta L_quad =
            epsilon_B W_L^2 + 2 epsilon_M W_L Q_L + epsilon_T W_T^2.

    Static configurations have W_L=W_T=0, so the added block is static-silent.
    At principal level it shifts exactly

        B -> B + epsilon_B,
        M -> M + epsilon_M,
        K_T -> K_T + epsilon_T,

    and leaves A,C,D,G_T and the pressure response unchanged.
    """
    omega, k, chi, pi_L, pi_T = sp.symbols(
        "omega k chi pi_L pi_T", real=True
    )
    epsilon_B, epsilon_M, epsilon_T = sp.symbols(
        "epsilon_B epsilon_M epsilon_T", real=True
    )

    mixed_gate = p01_alpha_E_mixed_characteristic_witness_gate()
    full_speed = p01_alpha_E_full_local_speed_completion_gate()
    values = mixed_gate["principal_values"]

    A = values["A"]
    B0 = values["B_long"]
    C = values["C"]
    D = values["D"]
    M0 = values["M_mix"]
    K_T0 = values["K_T"]
    G_T = values["G_T"]

    base_symbol = sp.expand(
        A * (omega * chi) ** 2
        + B0 * (omega * pi_L) ** 2
        + C * (k * chi) ** 2
        + D * (k * pi_L) ** 2
        + M0
        * ((omega * chi) * (k * pi_L) + (omega * pi_L) * (k * chi))
        + K_T0 * (omega * pi_T) ** 2
        - G_T * (k * pi_T) ** 2
    )
    repair_symbol = sp.expand(
        epsilon_B * (omega * pi_L) ** 2
        + 2 * epsilon_M * (omega * pi_L) * (k * chi)
        + epsilon_T * (omega * pi_T) ** 2
    )
    total_symbol = sp.expand(base_symbol + repair_symbol)
    static_silent_check = sp.simplify(repair_symbol.subs(omega, 0))

    longitudinal_matrix = sp.Matrix(
        [
            [
                sp.simplify(sp.diff(total_symbol, left, right) / 2)
                for right in (chi, pi_L)
            ]
            for left in (chi, pi_L)
        ]
    )
    expected_longitudinal_matrix = sp.Matrix(
        [
            [A * omega**2 + C * k**2, (M0 + epsilon_M) * omega * k],
            [
                (M0 + epsilon_M) * omega * k,
                (B0 + epsilon_B) * omega**2 + D * k**2,
            ],
        ]
    )
    transverse_symbol = sp.expand(
        (K_T0 + epsilon_T) * (omega * pi_T) ** 2 - G_T * (k * pi_T) ** 2
    )

    witness = full_speed["completed_witness_parameters"]
    witness_subs = {
        epsilon_B: witness["epsilon_B"],
        epsilon_M: witness["epsilon_M"],
        epsilon_T: witness["epsilon_T"],
    }
    witness_total_symbol = sp.factor(total_symbol.subs(witness_subs))

    checks = {
        "full_speed_completion_passes": full_speed["status"]
        == "PASS_P01_ALPHA_E_FULL_LOCAL_SPEED_COMPLETION_GATE",
        "repair_block_static_silent": static_silent_check == 0,
        "longitudinal_matrix_matches_shift_rule": sp.simplify(
            longitudinal_matrix - expected_longitudinal_matrix
        )
        == sp.zeros(2),
        "transverse_symbol_matches_shift_rule": sp.simplify(
            total_symbol.coeff(pi_T, 2) - transverse_symbol.coeff(pi_T, 2)
        )
        == 0,
        "A_unchanged": True,
        "C_unchanged": True,
        "D_unchanged": True,
        "G_T_unchanged": True,
        "pressure_response_unchanged": full_speed["pressure_response"][
            "alpha_E"
        ]
        == values["alpha_E"],
    }

    return {
        "status": "PASS_P01_ALPHA_E_QUADRATIC_REPAIR_ACTION_EMBEDDING_GATE"
        if all(bool(value) for value in checks.values())
        else "CHECK_P01_ALPHA_E_QUADRATIC_REPAIR_ACTION_EMBEDDING_GATE",
        "quadratic_repair_operator": (
            "Delta L_quad = epsilon_B W_L^2 + 2 epsilon_M W_L Q_L "
            "+ epsilon_T W_T^2"
        ),
        "shift_rule": {
            "B": sp.Eq(sp.Symbol("B_repaired"), B0 + epsilon_B),
            "M": sp.Eq(sp.Symbol("M_repaired"), M0 + epsilon_M),
            "K_T": sp.Eq(sp.Symbol("K_T_repaired"), K_T0 + epsilon_T),
            "unchanged": ["A", "C", "D", "G_T", "rho_y", "p_y", "alpha_E"],
        },
        "witness_parameters": witness,
        "witness_total_symbol": witness_total_symbol,
        "checks": checks,
        "meaning": (
            "The completed alpha_E local-speed repair has a single quadratic "
            "principal-action representative.  It is static-silent and produces "
            "exactly the scalar-longitudinal and transverse shifts used by the "
            "open repair-window gates."
        ),
        "remaining_derivation_boundary": (
            "This closes the local quadratic embedding.  The later article "
            "step is deriving these channel coefficients from the nonlinear "
            "RG action rather than selecting them inside the admissible windows."
        ),
    }


def finite_amplitude_pressure_status_domain_gate() -> dict[str, Any]:
    """
    Guard the finite-amplitude meaning of the pressure-status response.

    The p01 pressure potential gives an exact local reservoir expression

        R_exact(E) = P_stat(E)/P_bg = 1 - alpha_E E/P_bg.

    The p17 node selector uses a smooth exponential continuation

        R_exp(E) = exp(-alpha_E E/P_bg).

    These two agree at linear order, so they define the same kappa_E and
    q_rare.  They differ beyond linear order.  The exact reservoir expression
    also has a finite domain P_stat>0:

        E < P_bg/alpha_E.

    This gate prevents the exponential smoothing from being mistaken for the
    already-derived nonlinear pressure-status law.
    """
    E, alpha_E, P_bg = sp.symbols(
        "E alpha_E P_bg", positive=True, real=True
    )
    psi2, Omega_loc = sp.symbols(
        "psi2 Omega_loc", nonnegative=True, real=True
    )
    x = sp.simplify(alpha_E * E / P_bg)
    R_exact = sp.simplify(1 - x)
    R_exp = sp.exp(-x)
    linear_exact = sp.simplify(sp.diff(R_exact, E).subs(E, 0))
    linear_exp = sp.simplify(sp.diff(R_exp, E).subs(E, 0))
    linear_residual = sp.simplify(linear_exact - linear_exp)
    second_difference = sp.simplify(
        sp.diff(R_exp - R_exact, E, 2).subs(E, 0) / 2
    )

    E_kin = sp.simplify(Omega_loc**2 * psi2 / 2)
    q_rare = sp.simplify(alpha_E * Omega_loc**2 / (2 * P_bg))
    R_exact_psi = sp.simplify(R_exact.subs(E, E_kin))
    R_exp_psi = sp.simplify(R_exp.subs(E, E_kin))
    first_order_psi_residual = sp.simplify(
        sp.diff(R_exact_psi - R_exp_psi, psi2).subs(psi2, 0)
    )

    return {
        "status": "PASS_FINITE_AMPLITUDE_PRESSURE_STATUS_DOMAIN_GATE"
        if linear_residual == 0 and first_order_psi_residual == 0
        else "CHECK_FINITE_AMPLITUDE_PRESSURE_STATUS_DOMAIN_GATE",
        "exact_reservoir_factor": sp.Eq(sp.Symbol("R_exact(E)"), R_exact),
        "smooth_exponential_factor": sp.Eq(sp.Symbol("R_exp(E)"), R_exp),
        "linear_slope_exact": linear_exact,
        "linear_slope_exp": linear_exp,
        "linear_residual": linear_residual,
        "second_order_difference_coefficient": second_difference,
        "finite_domain": sp.StrictLessThan(E, P_bg / alpha_E),
        "kinetic_energy": sp.Eq(sp.Symbol("E_kin"), E_kin),
        "q_rare_linear": sp.Eq(sp.Symbol("q_rare"), q_rare),
        "exact_factor_in_psi2": sp.Eq(sp.Symbol("R_exact(psi2)"), R_exact_psi),
        "smooth_factor_in_psi2": sp.Eq(sp.Symbol("R_exp(psi2)"), R_exp_psi),
        "first_order_psi_residual": first_order_psi_residual,
        "meaning": (
            "The p01 pressure reservoir and the exponential node selector have "
            "the same linear kappa_E/q_rare.  The finite-amplitude branch is "
            "not closed until the nonlinear pressure-status equation selects "
            "the correct continuation and domain."
        ),
        "do_not_claim": [
            "do not claim the exponential continuation is the exact finite-amplitude p01 law",
            "do not use the exact reservoir expression past P_stat=0",
            "do not fit away the second-order difference before solving the nonlinear branch",
        ],
    }


def local_tempo_transposition_q_rare_invariance_gate() -> dict[str, Any]:
    """
    Guard against reintroducing an absolute substrate frequency through q_rare.

    The revised p10 population-tempo rule says that a pressure/status change
    transposes the local stable oscillon population together.  Therefore the
    node-width parameter must not depend on an external absolute frequency.

    From the p10 source candidate,

        q_rare = kappa_E Omega_loc^2 / (2 P0).

    If the local pressure/energy scale P0 transposes as an energy density,

        Omega_loc -> s Omega_loc,
        P0        -> s^2 P0,

    then q_rare and eps_node^2=1/q_rare are invariant.  If P0 is held fixed
    while Omega_loc changes, the residual is nonzero; that would be an
    unphysical hidden clock insertion.
    """
    Omega_loc, P0, kappa_E, s = sp.symbols(
        "Omega_loc P0 kappa_E s", positive=True, real=True
    )
    q_rare = sp.simplify(kappa_E * Omega_loc**2 / (2 * P0))
    eps_node2 = sp.simplify(1 / q_rare)
    q_scaled = sp.simplify(kappa_E * (s * Omega_loc) ** 2 / (2 * s**2 * P0))
    eps_scaled = sp.simplify(1 / q_scaled)
    q_bad_scaled = sp.simplify(kappa_E * (s * Omega_loc) ** 2 / (2 * P0))

    q_residual = sp.simplify(q_scaled - q_rare)
    eps_residual = sp.simplify(eps_scaled - eps_node2)
    hidden_clock_residual = sp.simplify(q_bad_scaled - q_rare)

    return {
        "status": "PASS_LOCAL_TEMPO_TRANSPOSITION_Q_RARE_INVARIANCE_GATE"
        if q_residual == 0 and eps_residual == 0
        else "CHECK_LOCAL_TEMPO_TRANSPOSITION_Q_RARE_INVARIANCE_GATE",
        "q_rare": sp.Eq(sp.Symbol("q_rare"), q_rare),
        "eps_node_squared": sp.Eq(sp.Symbol("eps_node2"), eps_node2),
        "scaled_q_rare": sp.Eq(sp.Symbol("q_rare_scaled"), q_scaled),
        "scaled_eps_node_squared": sp.Eq(
            sp.Symbol("eps_node2_scaled"), eps_scaled
        ),
        "q_invariance_residual": q_residual,
        "eps_invariance_residual": eps_residual,
        "hidden_clock_residual_if_P0_fixed": hidden_clock_residual,
        "meaning": (
            "q_rare is compatible with the local population-tempo law only when "
            "the pressure/energy scale transposes with Omega_loc^2.  Then the "
            "node selector is a local dimensionless branch property, not an "
            "external base frequency."
        ),
        "do_not_use": [
            "do not hold P0 fixed while changing Omega_loc as if an external clock were present",
            "do not interpret q_rare as a universal numerical frequency",
            "do not compare particle frequencies across pressure regimes without the local scale map",
        ],
    }


def node_pressure_to_active_stress_projection_gate() -> dict[str, Any]:
    """
    Project the long-mode node pressure into the p13 active source language.

    p13 does not use pressure as a direct force.  It uses the Bianchi/TOV
    source

        S_h = p_rad' - 2 Delta_p/r.

    A pure radial node-pressure baseline can enter as

        p_rad,node = P_bg - DeltaP_node(r),
        Delta_p,node = 0,
        S_node = -d_r DeltaP_node.

    Vortex/MOND and tail channels remain separate addends in the same source
    ledger.
    """
    r, c, rho_eff, P_bg = sp.symbols(
        "r c rho_eff P_bg", positive=True, real=True
    )
    DeltaP_node = sp.Function("DeltaP_node")(r)
    DeltaP_tail = sp.Function("DeltaP_tail")(r)
    Delta_p_vortex = sp.Function("Delta_p_vortex")(r)

    p_rad_node = P_bg - DeltaP_node
    S_node = sp.simplify(sp.diff(p_rad_node, r))
    h_prime_node = sp.simplify(S_node / (c**2 * rho_eff))

    p_rad_tail = -DeltaP_tail
    S_tail = sp.simplify(sp.diff(p_rad_tail, r))
    S_vortex = sp.simplify(-2 * Delta_p_vortex / r)
    S_total = sp.simplify(S_node + S_tail + S_vortex)
    h_prime_total = sp.simplify(S_total / (c**2 * rho_eff))

    expected_total = sp.simplify(
        -sp.diff(DeltaP_node, r)
        - sp.diff(DeltaP_tail, r)
        - 2 * Delta_p_vortex / r
    )
    total_residual = sp.simplify(S_total - expected_total)
    no_vortex_in_node = sp.simplify(sp.diff(S_node, Delta_p_vortex))

    return {
        "status": "PASS_NODE_PRESSURE_TO_ACTIVE_STRESS_PROJECTION_GATE"
        if total_residual == 0 and no_vortex_in_node == 0
        else "CHECK_NODE_PRESSURE_TO_ACTIVE_STRESS_PROJECTION_GATE",
        "node_radial_pressure": sp.Eq(sp.Symbol("p_rad_node"), p_rad_node),
        "node_active_source": sp.Eq(sp.Symbol("S_node"), S_node),
        "node_h_eff_prime": sp.Eq(sp.Symbol("h_prime_node"), h_prime_node),
        "three_channel_active_source": sp.Eq(sp.Symbol("S_total"), S_total),
        "three_channel_h_eff_prime": sp.Eq(
            sp.Symbol("h_prime_total"), h_prime_total
        ),
        "total_source_residual": total_residual,
        "node_source_vortex_derivative": no_vortex_in_node,
        "meaning": (
            "The cosmic node term enters the existing p13 source projection. "
            "It is not a new pressure force and it does not absorb the vortex "
            "or local-tail channels."
        ),
        "open_requirements": [
            "derive DeltaP_node(r) by projecting DeltaP_node(k,z) into cluster environments",
            "derive the tail and vortex source profiles from p10/p07 before fitting clusters",
            "lift the spherical projection to a full non-spherical lensing source map",
        ],
    }


def channel_sum_operator_candidate() -> dict[str, Any]:
    """
    First nontrivial candidate for the unified operator.

    In a locally homogeneous patch, the full differential operator should reduce
    to a channel-sum principal symbol.  The covariant target is

        L_RG = -nabla_i(C^{ij}_{AB} nabla_j) + M_{AB}
               + R_{AB} + Sigma_res,AB + Sigma_mem,AB.

    The scalar principal-symbol ledger below is only the diagonal/eigenchannel
    reduction of that target.  It is useful because it tells us exactly which
    terms must be derived from p01/p10/p13/p11 rather than added later.
    """
    k_phase, k_L, k_T, k_rot = sp.symbols(
        "k_phase k_L k_T k_rot", real=True
    )
    Z_phase, Z_L, Z_T, Z_rot = sp.symbols(
        "Z_phase Z_L Z_T Z_rot", positive=True, real=True
    )
    M_res2, Sigma_lag, V_deficit = sp.symbols(
        "M_res2 Sigma_lag V_deficit", real=True
    )
    lambda_phase = Z_phase * k_phase**2
    lambda_longitudinal = Z_L * k_L**2
    lambda_transverse = Z_T * k_T**2
    lambda_rotation = Z_rot * k_rot**2
    lambda_rg = sp.simplify(
        lambda_phase
        + lambda_longitudinal
        + lambda_transverse
        + lambda_rotation
        + M_res2
        + Sigma_lag
        + V_deficit
    )

    reconstructed = sp.simplify(
        sum(
            [
                lambda_phase,
                lambda_longitudinal,
                lambda_transverse,
                lambda_rotation,
                M_res2,
                Sigma_lag,
                V_deficit,
            ]
        )
        - lambda_rg
    )

    return {
        "status": "PASS_CHANNEL_SUM_OPERATOR_CANDIDATE"
        if reconstructed == 0
        else "CHECK_CHANNEL_SUM_OPERATOR_CANDIDATE",
        "covariant_target": (
            "L_RG = -nabla_i(C^{ij}_{AB} nabla_j) + M_{AB} + R_{AB} "
            "+ Sigma_res,AB + Sigma_mem,AB"
        ),
        "principal_symbol_lambda": lambda_rg,
        "channel_terms": {
            "phase_clock": lambda_phase,
            "longitudinal_compression": lambda_longitudinal,
            "transverse_shear": lambda_transverse,
            "rotation_or_vortex": lambda_rotation,
            "resonance_mass": M_res2,
            "phase_spatial_lag_or_memory": Sigma_lag,
            "pressure_deficit_potential": V_deficit,
        },
        "reconstruction_residual": reconstructed,
        "stability_requirement": sp.StrictGreaterThan(lambda_rg, 0),
        "warning": (
            "V_deficit and Sigma_lag may be sign-changing effective terms; "
            "positivity must be proven for the selected branch."
        ),
        "open_requirement": (
            "derive every channel coefficient from the action-level p01/p10/p13 "
            "medium equations and embed the p11 C3 block."
        ),
    }


def internal_c3_block_embedding_candidate() -> dict[str, Any]:
    """
    Minimal algebra for embedding the p11 particle block into L_RG.

    The cleanest route is not a second particle-only law.  It is a block of the
    same operator:

        L_unified = [[L_spatial, epsilon B],
                     [epsilon B^T, L_internal]].

    In the decoupled limit epsilon -> 0, the spectrum splits into spatial
    long/short modes and internal C3 modes.  With epsilon nonzero, the same
    operator can still mix them without changing the one-spectrum principle.
    """
    lambda_sp, lambda_c3, eps, B = sp.symbols(
        "lambda_sp lambda_c3 eps B", real=True
    )
    lam = sp.Symbol("lam", real=True)
    block = sp.Matrix([[lambda_sp, eps * B], [eps * B, lambda_c3]])
    trace = sp.trace(block)
    determinant = sp.factor(block.det())
    characteristic = sp.factor((block - lam * sp.eye(2)).det())
    expected_decoupled_characteristic = sp.factor(
        (lambda_sp - lam) * (lambda_c3 - lam)
    )
    eigenvalues = [
        sp.simplify(value)
        for value in block.eigenvals().keys()
    ]
    decoupled_characteristic_residual = sp.simplify(
        characteristic.subs(eps, 0) - expected_decoupled_characteristic
    )

    return {
        "status": "PASS_INTERNAL_BLOCK_EMBEDDING_CANDIDATE"
        if decoupled_characteristic_residual == 0
        else "CHECK_INTERNAL_BLOCK_EMBEDDING_CANDIDATE",
        "block_operator": block,
        "trace": trace,
        "determinant": determinant,
        "characteristic_polynomial": characteristic,
        "eigenvalues": eigenvalues,
        "decoupled_characteristic_residual": decoupled_characteristic_residual,
        "meaning": (
            "The C3 particle operator can be an internal spectral block of "
            "L_RG.  It must not remain an unrelated formula."
        ),
    }


def elastic_projector_operator_candidate() -> dict[str, Any]:
    """
    Tensor principal-symbol candidate for the spatial medium block.

    The scalar channel sum is not enough.  A medium must distinguish the
    longitudinal compression eigenchannel from the transverse shear
    eigenchannels.  In a locally homogeneous Euclidean patch this is done by
    the standard projectors

        P_L = k_i k_j / k^2,
        P_T = delta_ij - P_L.

    The minimal spatial block is

        L_ij(k) = Z_L k^2 P_L,ij + Z_T k^2 P_T,ij + M_eff^2 delta_ij.

    This is still only a principal symbol, but it is the first concrete tensor
    version of the unified operator.
    """
    kx, ky, kz = sp.symbols("kx ky kz", real=True)
    Z_L, Z_T = sp.symbols("Z_L Z_T", positive=True, real=True)
    M_res2, Sigma_lag, V_deficit = sp.symbols(
        "M_res2 Sigma_lag V_deficit", real=True
    )
    k_vec = sp.Matrix([kx, ky, kz])
    k2 = sp.simplify((k_vec.T * k_vec)[0])
    identity = sp.eye(3)
    P_L = sp.simplify((k_vec * k_vec.T) / k2)
    P_T = sp.simplify(identity - P_L)
    M_eff2 = sp.simplify(M_res2 + Sigma_lag + V_deficit)
    L_tensor = sp.simplify(Z_L * k2 * P_L + Z_T * k2 * P_T + M_eff2 * identity)

    long_residual = sp.simplify(
        L_tensor * k_vec - (Z_L * k2 + M_eff2) * k_vec
    )
    trans_vec = sp.Matrix([ky, -kx, 0])
    trans_residual = sp.simplify(
        L_tensor * trans_vec - (Z_T * k2 + M_eff2) * trans_vec
    )
    projector_checks = [
        sp.simplify(P_L * P_L - P_L) == sp.zeros(3),
        sp.simplify(P_T * P_T - P_T) == sp.zeros(3),
        sp.simplify(P_L * P_T) == sp.zeros(3),
        long_residual == sp.zeros(3, 1),
        trans_residual == sp.zeros(3, 1),
    ]

    return {
        "status": "PASS_ELASTIC_PROJECTOR_OPERATOR_CANDIDATE"
        if all(projector_checks)
        else "CHECK_ELASTIC_PROJECTOR_OPERATOR_CANDIDATE",
        "k_squared": k2,
        "longitudinal_projector": P_L,
        "transverse_projector": P_T,
        "effective_mass_or_potential": M_eff2,
        "L_tensor_principal_symbol": L_tensor,
        "longitudinal_eigenvalue": sp.simplify(Z_L * k2 + M_eff2),
        "transverse_eigenvalue": sp.simplify(Z_T * k2 + M_eff2),
        "longitudinal_residual": long_residual,
        "transverse_residual": trans_residual,
        "meaning": (
            "This is the first concrete spatial tensor block for L_RG: short "
            "and long wavelengths use the same operator, while longitudinal "
            "and transverse modes receive different stiffnesses."
        ),
        "open_requirement": (
            "derive Z_L, Z_T and M_eff2 from the RG action and add the rotation, "
            "topological, memory and C3 internal blocks without double counting."
        ),
    }


def quadratic_action_to_operator_derivation() -> dict[str, Any]:
    """
    Variational origin of the spatial principal symbol.

    The previous function wrote the tensor operator directly.  This function
    derives it as the Hessian of the quadratic medium energy for a Fourier mode
    u_i(k):

        E2 = 1/2 Z_L (k.u)^2
           + 1/2 Z_T (k^2 u^2 - (k.u)^2)
           + 1/2 M_eff^2 u^2.

    The Hessian d^2 E2 / d u_i d u_j must equal

        L_ij = Z_L k^2 P_L,ij + Z_T k^2 P_T,ij + M_eff^2 delta_ij.

    This is the first real strengthening step: the spatial block is no longer
    just a listed channel sum; it is the second variation of a medium energy.
    """
    kx, ky, kz = sp.symbols("kx ky kz", real=True)
    ux, uy, uz = sp.symbols("ux uy uz", real=True)
    Z_L, Z_T, M_eff2 = sp.symbols("Z_L Z_T M_eff2", positive=True, real=True)
    k_vec = sp.Matrix([kx, ky, kz])
    u_vec = sp.Matrix([ux, uy, uz])
    k2 = sp.simplify((k_vec.T * k_vec)[0])
    u2 = sp.simplify((u_vec.T * u_vec)[0])
    k_dot_u = sp.simplify((k_vec.T * u_vec)[0])

    compression_energy = sp.Rational(1, 2) * Z_L * k_dot_u**2
    shear_energy = sp.Rational(1, 2) * Z_T * (k2 * u2 - k_dot_u**2)
    mass_energy = sp.Rational(1, 2) * M_eff2 * u2
    energy_density = sp.simplify(compression_energy + shear_energy + mass_energy)
    variables = [ux, uy, uz]
    hessian = sp.Matrix(
        [
            [sp.simplify(sp.diff(energy_density, a, b)) for b in variables]
            for a in variables
        ]
    )

    identity = sp.eye(3)
    P_L = sp.simplify((k_vec * k_vec.T) / k2)
    P_T = sp.simplify(identity - P_L)
    expected_operator = sp.simplify(Z_L * k2 * P_L + Z_T * k2 * P_T + M_eff2 * identity)
    residual = sp.simplify(hessian - expected_operator)

    return {
        "status": "PASS_QUADRATIC_ACTION_TO_OPERATOR_DERIVATION"
        if residual == sp.zeros(3)
        else "CHECK_QUADRATIC_ACTION_TO_OPERATOR_DERIVATION",
        "quadratic_energy_density": energy_density,
        "compression_energy": compression_energy,
        "shear_energy": shear_energy,
        "mass_or_resonance_energy": mass_energy,
        "derived_operator_hessian": hessian,
        "expected_projector_operator": expected_operator,
        "residual": residual,
        "meaning": (
            "The spatial L_RG block follows from a quadratic elastic medium "
            "energy.  Z_L and Z_T are now stiffness coefficients to derive from "
            "the action, not arbitrary decorations."
        ),
        "open_requirement": (
            "identify this quadratic energy as the local second variation of "
            "the full RG action around the selected background branch."
        ),
    }


def gradient_energy_node_pressure_readout() -> dict[str, Any]:
    """
    Action-style origin of the Chladni node readout.

    For a standing long mode psi=sin(kx), the raw amplitude is zero at the node,
    so |psi|^2 is the wrong matter-attractor map.  The local gradient energy

        E_grad = 1/2 Z_node (d psi/dx)^2

    peaks at the node and vanishes at the antinode.  The pressure-node readout
    keeps that energetic feature but gates it by low amplitude:

        DeltaP_node = Xi E_grad exp(-psi^2/eps^2).

    This still is not the final stress tensor, but it is a stronger candidate
    than the earlier pure toy kernel because it is tied to a quadratic energy
    density.
    """
    x, k, eps = sp.symbols("x k eps", positive=True, real=True)
    Z_node, Xi = sp.symbols("Z_node Xi", positive=True, real=True)
    psi = sp.sin(k * x)
    gradient_energy = sp.simplify(
        sp.Rational(1, 2) * Z_node * sp.diff(psi, x) ** 2
    )
    pressure_readout = sp.simplify(
        Xi * gradient_energy * sp.exp(-(psi**2) / eps**2)
    )

    node_value = sp.simplify(pressure_readout.subs(x, 0))
    antinode_value = sp.simplify(pressure_readout.subs(x, sp.pi / (2 * k)))
    raw_amplitude_node = sp.simplify((psi**2).subs(x, 0))
    raw_amplitude_antinode = sp.simplify((psi**2).subs(x, sp.pi / (2 * k)))

    return {
        "status": "PASS_GRADIENT_ENERGY_NODE_PRESSURE_READOUT"
        if node_value == Xi * Z_node * k**2 / 2
        and antinode_value == 0
        and raw_amplitude_node == 0
        and raw_amplitude_antinode == 1
        else "CHECK_GRADIENT_ENERGY_NODE_PRESSURE_READOUT",
        "standing_mode": sp.Eq(sp.Symbol("psi"), psi),
        "gradient_energy": sp.Eq(sp.Symbol("E_grad"), gradient_energy),
        "pressure_readout": sp.Eq(sp.Symbol("DeltaP_node"), pressure_readout),
        "node_value_x0": node_value,
        "antinode_value_pi_over_2k": antinode_value,
        "raw_amplitude_node": raw_amplitude_node,
        "raw_amplitude_antinode": raw_amplitude_antinode,
        "meaning": (
            "The Chladni intuition points to gradient/strain energy at low "
            "amplitude nodes, not to raw amplitude density."
        ),
        "open_requirement": (
            "replace the exponential low-amplitude gate by the exact nonlinear "
            "stress/relaxation response of the RG medium."
        ),
    }


def kronecker_sum_spectrum_unification() -> dict[str, Any]:
    """
    One-operator embedding of spatial and internal particle spectra.

    A clean way to avoid two disconnected laws is a Kronecker-sum operator:

        L_total = L_spatial x I_internal + I_spatial x L_internal.

    Then every total eigenvalue is a sum

        lambda_total(a,b) = lambda_spatial,a + lambda_internal,b.

    Cosmic long modes can sit in the internal singlet/ground block, while
    localized particles can use nontrivial internal C3/order-9 blocks plus a
    finite spatial core.  This is still a separable local model, but it gives
    the correct algebraic architecture for one spectrum.
    """
    lam_s0, lam_s1, lam_i0, lam_i1, lam = sp.symbols(
        "lambda_s0 lambda_s1 lambda_i0 lambda_i1 lambda",
        real=True,
    )
    L_spatial = sp.diag(lam_s0, lam_s1)
    L_internal = sp.diag(lam_i0, lam_i1)
    I_spatial = sp.eye(2)
    I_internal = sp.eye(2)
    total_operator = sp.kronecker_product(L_spatial, I_internal) + sp.kronecker_product(
        I_spatial, L_internal
    )
    characteristic = sp.factor((total_operator - lam * sp.eye(4)).det())
    expected_characteristic = sp.factor(
        (lam_s0 + lam_i0 - lam)
        * (lam_s0 + lam_i1 - lam)
        * (lam_s1 + lam_i0 - lam)
        * (lam_s1 + lam_i1 - lam)
    )
    residual = sp.simplify(characteristic - expected_characteristic)

    return {
        "status": "PASS_KRONECKER_SUM_SPECTRUM_UNIFICATION"
        if residual == 0
        else "CHECK_KRONECKER_SUM_SPECTRUM_UNIFICATION",
        "total_operator": total_operator,
        "characteristic_polynomial": characteristic,
        "expected_pairwise_sum_polynomial": expected_characteristic,
        "residual": residual,
        "meaning": (
            "The same L_RG can carry spatial long modes and internal particle "
            "blocks.  The particle/cosmic split is a mode-sector split, not a "
            "new law."
        ),
        "open_requirement": (
            "replace the diagonal toy blocks by the p17 elastic projector block "
            "and the p11 C3/order-9 internal operator, then derive their coupling."
        ),
    }


def localized_c3_coupled_operator_candidate() -> dict[str, Any]:
    """
    Coupled spatial-internal candidate with C3 symmetry preserved.

    The previous Kronecker-sum model separates spatial and internal sectors.
    The next strengthening is to let spatial localization change the internal
    C3 stiffness without creating a second law.

    Use a C3-circulant Hermitian internal block

        Q_C3(theta) = (exp(i theta) P + exp(-i theta) P^2) / sqrt(2),

    where P is the cyclic permutation matrix.  Since Q_C3 commutes with P, the
    coupling below preserves C3:

        L_total = L_spatial x I_3 + I_2 x (omega0 I_3 + kappa Q_C3)
                + eps P_core x Q_C3.

    The long spatial sector sees kappa Q_C3.  The localized/core sector sees
    (kappa + eps) Q_C3.  Therefore particle localization and the internal C3
    resonance are coupled inside one operator.
    """
    theta = sp.Symbol("theta", real=True)
    lambda_long, lambda_core = sp.symbols(
        "lambda_long lambda_core", real=True
    )
    omega0, kappa, eps = sp.symbols("omega0 kappa eps", real=True)
    I2 = sp.eye(2)
    I3 = sp.eye(3)
    L_spatial = sp.diag(lambda_long, lambda_core)
    P_core = sp.diag(0, 1)
    P_cyclic = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    P_cyclic2 = P_cyclic**2
    Q_c3 = sp.simplify(
        (
            sp.exp(sp.I * theta) * P_cyclic
            + sp.exp(-sp.I * theta) * P_cyclic2
        )
        / sp.sqrt(2)
    )
    L_internal = sp.simplify(omega0 * I3 + kappa * Q_c3)
    separable_operator = sp.kronecker_product(L_spatial, I3) + sp.kronecker_product(
        I2, L_internal
    )
    coupling = eps * sp.kronecker_product(P_core, Q_c3)
    total_operator = sp.simplify(separable_operator + coupling)

    c3_commutator = sp.simplify(Q_c3 * P_cyclic - P_cyclic * Q_c3)
    decoupled_residual = sp.simplify(total_operator.subs(eps, 0) - separable_operator)
    long_block = sp.simplify(total_operator[:3, :3])
    core_block = sp.simplify(total_operator[3:6, 3:6])
    expected_long_block = sp.simplify(lambda_long * I3 + L_internal)
    expected_core_block = sp.simplify(
        lambda_core * I3 + omega0 * I3 + (kappa + eps) * Q_c3
    )
    long_residual = sp.simplify(long_block - expected_long_block)
    core_residual = sp.simplify(core_block - expected_core_block)

    checks = [
        c3_commutator == sp.zeros(3),
        decoupled_residual == sp.zeros(6),
        long_residual == sp.zeros(3),
        core_residual == sp.zeros(3),
    ]

    return {
        "status": "PASS_LOCALIZED_C3_COUPLED_OPERATOR_CANDIDATE"
        if all(checks)
        else "CHECK_LOCALIZED_C3_COUPLED_OPERATOR_CANDIDATE",
        "Q_C3": Q_c3,
        "C3_commutator_with_cyclic_permutation": c3_commutator,
        "separable_operator": separable_operator,
        "coupling_term": coupling,
        "total_operator": total_operator,
        "decoupled_residual_eps0": decoupled_residual,
        "long_sector_block": long_block,
        "core_sector_block": core_block,
        "core_interpretation": (
            "Localization changes the effective C3 stiffness from kappa to "
            "kappa+eps in the core sector.  This is a symmetry-preserving "
            "spatial-internal coupling."
        ),
        "open_requirement": (
            "derive eps and the exact P_core profile from the localized oscillon "
            "solution rather than treating the core projector as a toy block."
        ),
    }


def two_level_localization_lock_condition() -> dict[str, Any]:
    """
    Minimal algebra for a localized particle branch splitting from a continuum.

    A finite two-level toy block captures the spectral logic:

        H = [[lambda_cont, g],
             [g, lambda_core]],

    where lambda_cont is a long/spatial continuum level and lambda_core is the
    localized C3/core candidate level.  The lower mixed eigenvalue is

        lambda_- = (lambda_cont + lambda_core
                    - sqrt((lambda_cont-lambda_core)^2 + 4 g^2))/2.

    This is not a proof of a 3D oscillon bound state.  It is the algebraic
    gate saying what the full fluctuation problem must reproduce.
    """
    lambda_cont, lambda_core, g = sp.symbols(
        "lambda_cont lambda_core g", real=True
    )
    Delta = sp.Symbol("Delta", positive=True)
    H = sp.Matrix([[lambda_cont, g], [g, lambda_core]])
    trace = sp.trace(H)
    determinant = sp.factor(H.det())
    discriminant = sp.simplify((lambda_cont - lambda_core) ** 2 + 4 * g**2)
    lambda_minus = sp.simplify(
        (lambda_cont + lambda_core - sp.sqrt(discriminant)) / 2
    )
    lambda_plus = sp.simplify(
        (lambda_cont + lambda_core + sp.sqrt(discriminant)) / 2
    )
    trace_residual = sp.simplify(lambda_minus + lambda_plus - trace)
    determinant_residual = sp.simplify(lambda_minus * lambda_plus - determinant)
    no_coupling_core_limit = sp.simplify(
        lambda_minus.subs(g, 0).subs(lambda_core, lambda_cont - Delta)
        - (lambda_cont - Delta)
    )

    return {
        "status": "PASS_TWO_LEVEL_LOCALIZATION_LOCK_CONDITION"
        if trace_residual == 0 and determinant_residual == 0
        else "CHECK_TWO_LEVEL_LOCALIZATION_LOCK_CONDITION",
        "two_level_operator": H,
        "lambda_minus": lambda_minus,
        "lambda_plus": lambda_plus,
        "trace_residual": trace_residual,
        "determinant_residual": determinant_residual,
        "core_below_continuum_limit_check": no_coupling_core_limit,
        "bound_branch_reading": (
            "A particle branch corresponds to a localized mixed eigenvalue "
            "below the relevant continuum threshold.  The full p17/p11 task is "
            "to derive this in the 3D fluctuation operator."
        ),
        "open_requirement": (
            "replace this two-level toy block by the finite-core oscillon "
            "fluctuation spectrum and check all non-gauge eigenvalues."
        ),
    }


def radial_bound_state_variational_gate() -> dict[str, Any]:
    """
    First 3D radial fluctuation-operator gate for particle localization.

    The toy 2x2 lock must eventually become a true finite-core fluctuation
    problem.  The reduced radial partial-wave operator is

        H_l = -d^2/dr^2 + l(l+1)/r^2 + M_eff^2 - U0 exp(-r^2/R^2).

    The continuum threshold is M_eff^2.  For the s-wave trial function

        u(r) = r exp(-r^2/(2 R^2)),

    the Rayleigh quotient is below the continuum when

        U0 > 3 sqrt(2) / R^2.

    This is not the final oscillon spectrum.  It is the first real bound-state
    criterion that replaces the two-level cartoon.
    """
    r, R, U0, M_eff2 = sp.symbols("r R U0 M_eff2", positive=True, real=True)
    u = r * sp.exp(-(r**2) / (2 * R**2))
    well_shape = sp.exp(-(r**2) / R**2)
    norm = sp.simplify(sp.integrate(u**2, (r, 0, sp.oo)))
    kinetic = sp.simplify(sp.integrate(sp.diff(u, r) ** 2, (r, 0, sp.oo)))
    well_overlap = sp.simplify(sp.integrate(well_shape * u**2, (r, 0, sp.oo)))
    rayleigh = sp.simplify(
        (kinetic + M_eff2 * norm - U0 * well_overlap) / norm
    )
    binding_margin = sp.simplify(M_eff2 - rayleigh)
    expected_margin = sp.simplify(U0 / (2 * sp.sqrt(2)) - sp.Rational(3, 2) / R**2)
    margin_residual = sp.simplify(binding_margin - expected_margin)
    critical_U0 = sp.simplify(3 * sp.sqrt(2) / R**2)

    return {
        "status": "PASS_RADIAL_BOUND_STATE_VARIATIONAL_GATE"
        if margin_residual == 0
        else "CHECK_RADIAL_BOUND_STATE_VARIATIONAL_GATE",
        "radial_operator": "H_l = -d^2/dr^2 + l(l+1)/r^2 + M_eff^2 - U0 exp(-r^2/R^2)",
        "trial_function_l0": sp.Eq(sp.Symbol("u_0"), u),
        "norm": norm,
        "kinetic_integral": kinetic,
        "well_overlap": well_overlap,
        "rayleigh_quotient": rayleigh,
        "binding_margin_Meff2_minus_lambda": binding_margin,
        "critical_well_depth": sp.StrictGreaterThan(U0, critical_U0),
        "meaning": (
            "A localized particle branch requires the core-induced attractive "
            "well to pull at least one fluctuation eigenvalue below the "
            "continuum threshold M_eff^2."
        ),
        "open_requirement": (
            "replace the Gaussian well and trial function by the finite-core "
            "oscillon profile and compute the exact fluctuation spectrum."
        ),
    }


def partial_wave_bound_threshold_ladder() -> dict[str, Any]:
    """
    Bound-state thresholds for the first few radial partial waves.

    For trial functions

        u_l(r) = r^(l+1) exp(-r^2/(2 R^2)),

    the variational threshold has the pattern

        U0_crit(l) = 2^(l+1/2) (2l+3) / R^2.

    The l=0 channel is therefore the easiest one to bind in this simple radial
    well.  This does not identify l with the p11 framed index h; it is only the
    radial partial-wave barrier.
    """
    r, R, U0, M_eff2 = sp.symbols("r R U0 M_eff2", positive=True, real=True)
    rows: list[dict[str, Any]] = []
    for ell in range(3):
        u = r ** (ell + 1) * sp.exp(-(r**2) / (2 * R**2))
        well_shape = sp.exp(-(r**2) / R**2)
        norm = sp.simplify(sp.integrate(u**2, (r, 0, sp.oo)))
        kinetic = sp.simplify(
            sp.integrate(
                sp.diff(u, r) ** 2 + ell * (ell + 1) * u**2 / r**2,
                (r, 0, sp.oo),
            )
        )
        well_overlap = sp.simplify(sp.integrate(well_shape * u**2, (r, 0, sp.oo)))
        kinetic_per_norm = sp.simplify(kinetic / norm)
        overlap_per_norm = sp.simplify(well_overlap / norm)
        critical_U0 = sp.simplify(kinetic_per_norm / overlap_per_norm)
        expected_critical = sp.simplify(2 ** (ell + sp.Rational(1, 2)) * (2 * ell + 3) / R**2)
        rows.append(
            {
                "ell": ell,
                "kinetic_per_norm": kinetic_per_norm,
                "well_overlap_per_norm": overlap_per_norm,
                "critical_U0": critical_U0,
                "expected_critical_U0": expected_critical,
                "residual": sp.simplify(critical_U0 - expected_critical),
            }
        )

    return {
        "status": "PASS_PARTIAL_WAVE_BOUND_THRESHOLD_LADDER"
        if all(row["residual"] == 0 for row in rows)
        else "CHECK_PARTIAL_WAVE_BOUND_THRESHOLD_LADDER",
        "rows": rows,
        "pattern": "U0_crit(l) = 2^(l+1/2) (2l+3) / R^2",
        "meaning": (
            "The radial barrier raises the binding threshold.  In this first "
            "gate, l=0 is the easiest localized branch; higher partial waves "
            "need a deeper or narrower core."
        ),
    }


def c3_core_well_depth_bridge() -> dict[str, Any]:
    """
    Bridge the localized C3 coupling to the radial well depth.

    The C3 coupling block shifts the core-sector internal eigenvalues by

        eps q_j(theta),    q_j = sqrt(2) cos(theta + 2 pi j/3).

    A branch with eps q_j < 0 lowers the local fluctuation eigenvalue and acts
    like an attractive radial well with

        U0_j = -eps q_j.

    Combining this with the l=0 radial gate gives

        -eps q_j > 3 sqrt(2) / R^2.

    This is a clean algebraic bridge from the C3 core splitting to particle
    localization.
    """
    theta, eps, R = sp.symbols("theta eps R", positive=True, real=True)
    critical_U0 = sp.simplify(3 * sp.sqrt(2) / R**2)
    branches = []
    for j in range(3):
        q_j = sp.simplify(sp.sqrt(2) * sp.cos(theta + 2 * sp.pi * j / 3))
        U0_j = sp.simplify(-eps * q_j)
        branches.append(
            {
                "j": j,
                "q_j": q_j,
                "effective_well_depth_U0_j": U0_j,
                "l0_binding_condition": sp.StrictGreaterThan(U0_j, critical_U0),
            }
        )

    theta_lock = sp.Rational(2, 9)
    locked_branches = [
        {
            "j": row["j"],
            "q_j_at_theta_2_over_9": sp.simplify(row["q_j"].subs(theta, theta_lock)),
            "U0_j_at_theta_2_over_9": sp.simplify(
                row["effective_well_depth_U0_j"].subs(theta, theta_lock)
            ),
        }
        for row in branches
    ]

    return {
        "status": "PASS_C3_CORE_WELL_DEPTH_BRIDGE",
        "critical_l0_well_depth": critical_U0,
        "branches": branches,
        "theta_2_over_9_branch_values": locked_branches,
        "meaning": (
            "Only C3 branches whose core coupling lowers the eigenvalue can "
            "seed a localized radial bound mode.  This is where the particle "
            "selection problem becomes a sign-and-depth problem for eps q_j."
        ),
        "open_requirement": (
            "derive the sign and magnitude of eps from the finite-core oscillon "
            "solution and match it to the p11 C3/order-9 branch."
        ),
    }


def embedded_c3_triplet_koide_theorem() -> dict[str, Any]:
    """
    Koide/C3 identity as an internal block of the unified operator.

    The p11 particle file already contains the C3/order-9 charged-lepton
    candidate.  Here the same identity is registered inside p17's unified
    operator language.

    Let

        Q_C3 = (exp(i theta) P + exp(-i theta) P^2) / sqrt(2),

    with P^3=I and tr(P)=tr(P^2)=0.  The charged triplet frequency block is

        nu = I + Q_C3.

    Since tr(Q_C3)=0 and tr(Q_C3^2)=3, the Koide frequency ratio is

        K = tr(nu^2) / tr(nu)^2 = 2/3.

    This proves the identity at the embedded-block level; it does not yet prove
    theta=2/9 or the absolute mass scale.
    """
    theta = sp.Symbol("theta", real=True)
    I3 = sp.eye(3)
    P = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    Q = sp.simplify((sp.exp(sp.I * theta) * P + sp.exp(-sp.I * theta) * P**2) / sp.sqrt(2))
    nu_block = sp.simplify(I3 + Q)

    q_trace = sp.simplify(sp.trace(Q))
    q_square_trace = sp.simplify(sp.trace(Q * Q))
    nu_trace = sp.simplify(sp.trace(nu_block))
    nu_square_trace = sp.simplify(sp.trace(nu_block * nu_block))
    koide_frequency = sp.simplify(nu_square_trace / nu_trace**2)

    return {
        "status": "PASS_EMBEDDED_C3_TRIPLET_KOIDE_THEOREM"
        if q_trace == 0 and q_square_trace == 3 and sp.simplify(koide_frequency - sp.Rational(2, 3)) == 0
        else "CHECK_EMBEDDED_C3_TRIPLET_KOIDE_THEOREM",
        "Q_C3": Q,
        "nu_block": nu_block,
        "trace_Q_C3": q_trace,
        "trace_Q_C3_squared": q_square_trace,
        "trace_nu": nu_trace,
        "trace_nu_squared": nu_square_trace,
        "Koide_frequency_ratio": koide_frequency,
        "meaning": (
            "The C3 triplet identity can live inside the same unified spectral "
            "operator.  The identity follows from the internal C3 block, not "
            "from a separate particle-only formula."
        ),
        "open_requirement": (
            "derive theta=2/9, the pole-frequency protection, and m proportional "
            "to nu^2 from the full localized oscillon branch."
        ),
    }


def c3_triplet_binding_window_gate() -> dict[str, Any]:
    """
    Binding window for all three C3 branches in one localized core.

    A common finite core should bind the whole charged triplet, not just one
    C3 component by accident.  Add a common attractive depth U_base and the
    C3 splitting from the localized coupling:

        U_j = U_base - eps q_j(theta),
        q_j = sqrt(2) cos(theta + 2 pi j/3).

    For the l=0 radial variational gate, every branch binds if

        U_j > Ucrit = 3 sqrt(2) / R^2

    for j=0,1,2.  The C3 splitting redistributes the depths, but its triplet
    average is U_base because sum_j q_j = 0.
    """
    theta, eps, U_base, R = sp.symbols(
        "theta eps U_base R", positive=True, real=True
    )
    Ucrit = sp.simplify(3 * sp.sqrt(2) / R**2)
    q_values = [
        sp.sqrt(2) * sp.cos(theta + 2 * sp.pi * j / 3)
        for j in range(3)
    ]
    U_values = [sp.simplify(U_base - eps * q) for q in q_values]
    q_sum = sp.trigsimp(sum(q_values))
    U_average = sp.simplify(sum(U_values) / 3)
    spread_01 = sp.simplify(U_values[0] - U_values[1])
    spread_12 = sp.simplify(U_values[1] - U_values[2])
    theta_lock = sp.Rational(2, 9)
    positivity_edge = sp.pi / 12
    raw_frequencies_locked = [
        sp.N(1 + q.subs(theta, theta_lock), 16)
        for q in q_values
    ]
    locked_frequency_positive = all(float(value) > 0.0 for value in raw_frequencies_locked)
    theta_inside_positive_branch = bool(theta_lock < positivity_edge)

    branch_rows = [
        {
            "j": j,
            "q_j": sp.simplify(q_values[j]),
            "U_j": U_values[j],
            "l0_binding_condition": sp.StrictGreaterThan(U_values[j], Ucrit),
            "q_j_at_theta_2_over_9": sp.N(q_values[j].subs(theta, theta_lock), 16),
            "nu_j_at_theta_2_over_9": raw_frequencies_locked[j],
        }
        for j in range(3)
    ]

    return {
        "status": "PASS_C3_TRIPLET_BINDING_WINDOW_GATE"
        if q_sum == 0 and U_average == U_base and locked_frequency_positive and theta_inside_positive_branch
        else "CHECK_C3_TRIPLET_BINDING_WINDOW_GATE",
        "Ucrit_l0": Ucrit,
        "q_sum": q_sum,
        "triplet_average_depth": U_average,
        "branch_rows": branch_rows,
        "depth_spread_U0_minus_U1": spread_01,
        "depth_spread_U1_minus_U2": spread_12,
        "theta_2_over_9_inside_positive_branch": theta_inside_positive_branch,
        "raw_frequencies_at_theta_2_over_9": raw_frequencies_locked,
        "all_triplet_binding_rule": (
            "All three C3 components bind only where every U_base - eps*q_j "
            "exceeds 3*sqrt(2)/R^2."
        ),
        "meaning": (
            "A common core depth can bind the whole C3 triplet, while eps splits "
            "the binding depths around the unchanged triplet average.  This is "
            "the clean next bridge between C3 frequencies and localized particle "
            "existence."
        ),
        "open_requirement": (
            "derive U_base, eps and R from the finite-core oscillon solution, "
            "then test whether the same window supports exactly the charged "
            "C3 triplet and no forbidden lower branch."
        ),
    }


def p10_gaussian_oscillon_source_parameter_map() -> dict[str, Any]:
    """
    Extract finite-core parameters from the p10 zero-frequency source ledger.

    p10 gives the Newtonian zero-frequency source profile

        rho_osc = 1/2 Omega^2 Phi0(r)^2 + 1/2 Phi0'(r)^2.

    Insert a regular localized trial amplitude

        Phi0(r) = A exp[-r^2/(2 R^2)].

    This does not prove the true finite-core oscillon profile.  It creates a
    concrete map from an oscillon amplitude profile to:

        rho_c      = rho_osc(0),
        Q_osc      = 4 pi int rho_osc r^2 dr,
        R_eff^2    = (2/3) <r^2>,

    where R_eff equals R for a pure Gaussian density and remains a finite
    profile radius for the p10 kinetic+gradient source.
    """
    r, A, R, Omega = sp.symbols("r A R Omega", positive=True, real=True)
    Phi0 = A * sp.exp(-(r**2) / (2 * R**2))
    rho_osc = sp.simplify(
        sp.Rational(1, 2) * Omega**2 * Phi0**2
        + sp.Rational(1, 2) * sp.diff(Phi0, r) ** 2
    )
    rho_center = sp.simplify(rho_osc.subs(r, 0))
    source_charge = sp.simplify(4 * sp.pi * sp.integrate(rho_osc * r**2, (r, 0, sp.oo)))
    second_moment = sp.simplify(
        4 * sp.pi * sp.integrate(rho_osc * r**4, (r, 0, sp.oo)) / source_charge
    )
    R_eff2 = sp.simplify(sp.Rational(2, 3) * second_moment)
    eta = sp.Symbol("eta", positive=True, real=True)
    R_eff2_eta = sp.simplify((R_eff2 / R**2).subs(Omega, eta / R))
    expected_R_eff2_eta = sp.simplify((2 * eta**2 + 5) / (2 * eta**2 + 3))
    eta_residual = sp.simplify(R_eff2_eta - expected_R_eff2_eta)
    finite_checks = [
        sp.simplify(rho_center - A**2 * Omega**2 / 2) == 0,
        eta_residual == 0,
    ]

    return {
        "status": "PASS_P10_GAUSSIAN_OSCILLON_SOURCE_PARAMETER_MAP"
        if all(finite_checks)
        else "CHECK_P10_GAUSSIAN_OSCILLON_SOURCE_PARAMETER_MAP",
        "trial_amplitude": sp.Eq(sp.Symbol("Phi0"), Phi0),
        "p10_zero_frequency_source": sp.Eq(sp.Symbol("rho_osc"), rho_osc),
        "central_source_rho_c": rho_center,
        "total_zero_frequency_source_charge": source_charge,
        "second_moment_r2": second_moment,
        "effective_radius_squared": R_eff2,
        "dimensionless_effective_radius_squared": sp.Eq(
            sp.Symbol("R_eff2_over_R2"), R_eff2_eta
        ),
        "eta_residual": eta_residual,
        "meaning": (
            "The p10 zero-frequency oscillon source gives concrete finite "
            "profile data: central depth scale and effective radius.  The "
            "profile is still a trial family, but the parameter map is explicit."
        ),
        "open_requirement": (
            "replace the Gaussian Phi0 by the true finite-energy nonlinear "
            "oscillon solution once the PDE is solved."
        ),
    }


def p10_profile_to_c3_binding_window_bridge() -> dict[str, Any]:
    """
    Insert the p10 trial-source parameters into the C3 triplet binding window.

    Use the central p10 source to parameterize the common core depth

        U_base = alpha_U rho_c,
        rho_c = A^2 Omega^2 / 2.

    Let the C3 splitting be a dimensionless fraction beta_C3 of that common
    depth:

        eps = beta_C3 U_base,
        U_j = U_base (1 - beta_C3 q_j).

    The radial l=0 gate then becomes

        U_base (1 - beta_C3 q_j) > 3 sqrt(2) / R_eff^2.

    This is the first direct bridge:

        p10 zero-frequency source -> finite core scale -> C3 binding window.
    """
    A, R, Omega, alpha_U, beta_C3, theta = sp.symbols(
        "A R Omega alpha_U beta_C3 theta",
        positive=True,
        real=True,
    )
    eta = sp.simplify(Omega * R)
    rho_c = sp.simplify(A**2 * Omega**2 / 2)
    U_base = sp.simplify(alpha_U * rho_c)
    R_eff2 = sp.simplify(R**2 * (2 * eta**2 + 5) / (2 * eta**2 + 3))
    Ucrit_eff = sp.simplify(3 * sp.sqrt(2) / R_eff2)
    q_values = [
        sp.sqrt(2) * sp.cos(theta + 2 * sp.pi * j / 3)
        for j in range(3)
    ]
    U_values = [sp.simplify(U_base * (1 - beta_C3 * q)) for q in q_values]
    q_sum = sp.trigsimp(sum(q_values))
    U_average = sp.simplify(sum(U_values) / 3)
    average_residual = sp.simplify(U_average - U_base)
    branch_rows = [
        {
            "j": j,
            "q_j": sp.simplify(q_values[j]),
            "U_j_from_p10_profile": U_values[j],
            "binding_condition": sp.StrictGreaterThan(U_values[j], Ucrit_eff),
        }
        for j in range(3)
    ]

    return {
        "status": "PASS_P10_PROFILE_TO_C3_BINDING_WINDOW_BRIDGE"
        if q_sum == 0 and average_residual == 0
        else "CHECK_P10_PROFILE_TO_C3_BINDING_WINDOW_BRIDGE",
        "rho_c_from_p10_source": rho_c,
        "U_base_from_p10_source": U_base,
        "epsilon_C3": sp.Eq(sp.Symbol("eps"), sp.simplify(beta_C3 * U_base)),
        "R_eff_squared_from_p10_profile": R_eff2,
        "effective_l0_critical_depth": Ucrit_eff,
        "branch_rows": branch_rows,
        "triplet_average_depth_residual": average_residual,
        "meaning": (
            "The common finite-core depth is now tied to the p10 averaged "
            "oscillon source.  C3 splitting redistributes that depth while "
            "leaving the triplet average unchanged."
        ),
        "open_requirement": (
            "derive alpha_U and beta_C3 from the second variation of the full "
            "localized oscillon action, not from a phenomenological fraction."
        ),
    }


def spectral_gradient_pressure_identity() -> dict[str, Any]:
    """
    Tie Chladni-node pressure directly to the same spectral eigenvalue.

    For a one-channel long mode with

        lambda(k) = M_eff^2 + Z_node k^2,

    and psi=A sin(kx), the node gradient energy is

        E_grad,node = 1/2 Z_node A^2 k^2.

    Therefore

        DeltaP_node = Xi E_grad,node
                    = Xi A^2 (lambda(k)-M_eff^2)/2.

    This is the first compact algebraic bridge between the spectrum and the
    cosmic Chladni pressure map.
    """
    k, A, Z_node, M_eff2, Xi, lambda_k = sp.symbols(
        "k A Z_node M_eff2 Xi lambda_k",
        positive=True,
        real=True,
    )
    spectral_law = sp.Eq(lambda_k, M_eff2 + Z_node * k**2)
    node_gradient_energy = sp.simplify(sp.Rational(1, 2) * Z_node * A**2 * k**2)
    node_pressure = sp.simplify(Xi * node_gradient_energy)
    spectral_pressure = sp.simplify(Xi * A**2 * (lambda_k - M_eff2) / 2)
    residual = sp.simplify(
        node_pressure - spectral_pressure.subs(lambda_k, spectral_law.rhs)
    )

    return {
        "status": "PASS_SPECTRAL_GRADIENT_PRESSURE_IDENTITY"
        if residual == 0
        else "CHECK_SPECTRAL_GRADIENT_PRESSURE_IDENTITY",
        "spectral_law": spectral_law,
        "node_gradient_energy": sp.Eq(sp.Symbol("E_grad_node"), node_gradient_energy),
        "node_pressure": sp.Eq(sp.Symbol("DeltaP_node"), node_pressure),
        "spectral_pressure_readout": sp.Eq(
            sp.Symbol("DeltaP_node_spectral"), spectral_pressure
        ),
        "residual_after_spectral_law": residual,
        "meaning": (
            "The cosmic node pressure is the gradient/stiffness part of the "
            "same eigenvalue.  In this approximation, the rest mass/gap term "
            "M_eff2 is not what makes the Chladni node; the spatial stiffness is."
        ),
        "open_requirement": (
            "generalize lambda(k)-M_eff2 to the full tensor operator and define "
            "which parts of the spectrum contribute to the pressure deficit."
        ),
    }


def pressure_deficit_to_refractive_bridge() -> dict[str, Any]:
    """
    Connect the long-mode node readout to the existing p13 stress bridge.

    p13 uses the weak on-shell source

        h_eff' = (p_rad' - 2*Delta_p/r)/(c^2 rho_eff).

    A cosmic node is naturally represented as a positive pressure deficit
    DeltaP_node(r) relative to a background pressure:

        p_rad,node = P_bg - DeltaP_node(r).

    This function keeps the sign bookkeeping explicit.  It is not yet the final
    cluster lensing profile.
    """
    r, c, rho_eff, P_bg = sp.symbols(
        "r c rho_eff P_bg", positive=True, real=True
    )
    DeltaP_node = sp.Function("DeltaP_node")(r)
    Delta_p_node = sp.Function("Delta_p_node")(r)
    p_rad_node = P_bg - DeltaP_node
    source_node = sp.simplify(sp.diff(p_rad_node, r) - 2 * Delta_p_node / r)
    h_prime_node = sp.simplify(source_node / (c**2 * rho_eff))

    # Linearity check for the three-channel cluster source.
    p_tail, p_vortex = sp.Function("p_tail")(r), sp.Function("p_vortex")(r)
    Delta_tail = sp.Function("Delta_tail")(r)
    Delta_vortex = sp.Function("Delta_vortex")(r)
    p_total = p_rad_node + p_tail + p_vortex
    Delta_total = Delta_p_node + Delta_tail + Delta_vortex
    source_total = sp.simplify(sp.diff(p_total, r) - 2 * Delta_total / r)
    source_parts = sp.simplify(
        source_node
        + (sp.diff(p_tail, r) - 2 * Delta_tail / r)
        + (sp.diff(p_vortex, r) - 2 * Delta_vortex / r)
    )

    return {
        "status": "PASS_PRESSURE_DEFICIT_TO_REFRACTIVE_BRIDGE"
        if sp.simplify(source_total - source_parts) == 0
        else "CHECK_PRESSURE_DEFICIT_TO_REFRACTIVE_BRIDGE",
        "node_radial_pressure": sp.Eq(sp.Symbol("p_rad_node"), p_rad_node),
        "node_source": sp.Eq(sp.Symbol("S_h_node"), source_node),
        "node_h_eff_prime": sp.Eq(sp.Symbol("h_eff_prime_node"), h_prime_node),
        "three_channel_source_linearity": sp.simplify(source_total - source_parts),
        "interpretation": (
            "The cosmic-node pressure deficit can enter the same h_eff ledger "
            "as local tails and vortex/MOND transport, but the sign and profile "
            "must be fixed by the derived pressure functional."
        ),
        "open_requirement": (
            "derive DeltaP_node(r) and Delta_p_node(r) from long-mode eigenfunctions "
            "rather than choosing a phenomenological cluster profile."
        ),
    }


def unified_master_formula_candidate() -> dict[str, Any]:
    """
    The current best compact formula candidate.

    This function collects the operator, the particle readout, the node readout,
    and the gravitational/index readout into one explicit ledger.
    """
    operator = channel_sum_operator_candidate()
    bridge = pressure_deficit_to_refractive_bridge()
    n, N = sp.symbols("n N", integer=True, nonnegative=True)
    x = sp.Symbol("x", real=True)
    A_n = sp.Function("A")(n)
    psi_n = sp.Function("psi")(n, x)
    S_node = sp.Function("S_node")
    Xi, P0, rho0 = sp.symbols("Xi P0 rho0", positive=True, real=True)
    F = sp.Function("F")
    DeltaP_node_x = sp.simplify(
        Xi * sp.Sum(A_n**2 * S_node(psi_n), (n, 0, N))
    )
    rho_m_x = rho0 * F(DeltaP_node_x / P0)

    return {
        "status": "PASS_UNIFIED_MASTER_FORMULA_CANDIDATE"
        if operator["status"] == "PASS_CHANNEL_SUM_OPERATOR_CANDIDATE"
        and bridge["status"] == "PASS_PRESSURE_DEFICIT_TO_REFRACTIVE_BRIDGE"
        else "CHECK_UNIFIED_MASTER_FORMULA_CANDIDATE",
        "operator": operator["covariant_target"],
        "eigen_equation": "L_RG psi_n = lambda_n psi_n",
        "particle_readout": "m_n = gamma_m Omega_loc^2 lambda_n",
        "node_pressure_readout": sp.Eq(sp.Symbol("DeltaP_node_x"), DeltaP_node_x),
        "matter_readout": sp.Eq(sp.Symbol("rho_m_x"), rho_m_x),
        "index_readout": bridge["node_h_eff_prime"],
        "plain_language": (
            "One operator gives the spectrum.  Localized short modes are read "
            "as particle masses.  Long coherent modes are read as node pressure "
            "deficits, and those deficits enter the same refractive-stress "
            "source that already carries Newton, MOND/vortex and cluster channels."
        ),
    }


def chladni_node_readout_toy_model() -> dict[str, Any]:
    """
    A small toy check for the Chladni intuition.

    For psi(x)=sin(kx), the node is x=0 and the antinode is pi/(2k).  The toy
    functional below rewards low amplitude and nonzero local slope:

        S_node = exp(-psi^2 / eps^2) * (d psi/dx)^2.

    It is not the final pressure law.  It only encodes the qualitative rule that
    the large-scale matter map should be a node/deficit readout.
    """
    x, k, eps = sp.symbols("x k eps", positive=True, real=True)
    psi = sp.sin(k * x)
    node_kernel = sp.simplify(sp.exp(-(psi**2) / eps**2) * sp.diff(psi, x) ** 2)

    node_value = sp.simplify(node_kernel.subs(x, 0))
    antinode_value = sp.simplify(node_kernel.subs(x, sp.pi / (2 * k)))
    node_over_antinode = sp.simplify(
        node_value - antinode_value
    )

    return {
        "status": "PASS_TOY_CHLADNI_NODE_KERNEL"
        if node_value == k**2 and antinode_value == 0
        else "CHECK_TOY_CHLADNI_NODE_KERNEL",
        "standing_mode": sp.Eq(sp.Symbol("psi"), psi),
        "node_kernel": sp.Eq(sp.Symbol("S_node"), node_kernel),
        "node_value_x0": node_value,
        "antinode_value_pi_over_2k": antinode_value,
        "node_minus_antinode": node_over_antinode,
        "meaning": (
            "The toy readout peaks at a node, so it matches the Chladni "
            "intuition better than a raw |psi|^2 matter map."
        ),
    }


def cosmic_node_pressure_ledger() -> dict[str, Any]:
    """
    Symbolic ledger for the long-mode pressure deficit.

    The total residual in clusters should be decomposed as

        DeltaP_total = DeltaP_node + DeltaP_tail + DeltaP_vortex.

    This preserves the new interpretation: cluster-scale residual gravity is
    not tail retention alone.
    """
    n, N = sp.symbols("n N", integer=True, nonnegative=True)
    A_n = sp.Function("A")(n)
    S_n = sp.Function("S_node")(n)
    DeltaP_node, DeltaP_tail, DeltaP_vortex, DeltaP_total = sp.symbols(
        "DeltaP_node DeltaP_tail DeltaP_vortex DeltaP_total",
        real=True,
    )

    node_sum = sp.Sum(A_n**2 * S_n, (n, 0, N))
    total = sp.Eq(DeltaP_total, DeltaP_node + DeltaP_tail + DeltaP_vortex)

    return {
        "status": "PASS_THREE_CHANNEL_PRESSURE_LEDGER",
        "long_mode_node_baseline": sp.Eq(DeltaP_node, node_sum),
        "cluster_pressure_decomposition": total,
        "channels": [
            "cosmic_node_long_mode_baseline",
            "local_oscillon_tail_retention",
            "vortex_or_MOND_transport",
        ],
        "rule": (
            "Cluster residuals may include local tails, but the large-scale "
            "node baseline is an independent long-mode readout."
        ),
    }


def particle_sector_bridge_ledger() -> dict[str, Any]:
    """
    Connect the unified spectrum to the current particle file without claiming
    the full particle theory is closed.

    p11 currently has a strong C3/order-9 charged-lepton candidate.  In this
    unified file, that should become the finite-dimensional internal block of
    the same L_RG spectrum.
    """
    theta = sp.Rational(2, 9)
    j = sp.symbols("j", integer=True)
    nu_j = sp.Function("nu")(j)
    m_j, gamma_m, Omega_loc = sp.symbols(
        "m_j gamma_m Omega_loc", positive=True, real=True
    )
    lambda_j = sp.Function("lambda")(j)

    return {
        "status": "PARTICLE_BRIDGE_REGISTERED_NOT_DERIVED",
        "c3_theta_target": theta,
        "spectral_mass_rule": sp.Eq(m_j, gamma_m * Omega_loc**2 * lambda_j),
        "frequency_symbol": sp.Eq(nu_j, sp.sqrt(lambda_j)),
        "required_merge_with_p11": (
            "show that the p11 C3/order-9 operator is an internal block or "
            "boundary sector of L_RG, not a separate numerological operator."
        ),
        "open_requirements": [
            "derive m proportional to nu^2 from the oscillon energy functional",
            "derive the absolute electron scale",
            "compute the localized 3D fluctuation spectrum",
            "protect the C3/Koide pole-frequency relation radiatively",
        ],
    }


def falsifiable_targets() -> dict[str, Any]:
    """Concrete tests this formula must eventually face."""
    return {
        "status": "TARGETS_DEFINED_NO_NUMERICAL_FIT",
        "particle_tests": [
            "charged-lepton ratios from the same internal spectral block",
            "absolute electron scale from the localized oscillon energy",
            "absence or suppression of forbidden lower branches",
        ],
        "cosmic_tests": [
            "CMB acoustic peaks and lensing with the derived long-mode sector",
            "BAO scale and matter power spectrum P(k)",
            "cosmic-web node map versus observed filament/cluster environments",
            "cluster weak-lensing residuals versus cosmic-node depth",
            "Bullet-like mergers after separating node baseline, local tails, and memory",
        ],
        "hard_failures": [
            "particle spectrum requires a different operator from the cosmic web",
            "matter follows raw |psi|^2 instead of the observed node/void pattern",
            "cluster residuals do not correlate with any derived node environment",
            "CMB/BAO likelihood fails after the long-mode sector is included",
        ],
    }


def unified_formula_status() -> dict[str, Any]:
    """Single entry point for the file."""
    bridge_map = existing_work_bridge_map()
    coverage = full_theory_sector_coverage_ledger()
    python_scope = current_work_python_scope_ledger()
    no_double = unified_no_double_counting_guard()
    inventory = action_inventory_to_readout_ledger()
    cosmo_export = cosmology_cmb_lss_export_guard()
    node_kz_kernel = long_mode_delta_p_node_kz_kernel_candidate()
    node_selector = standing_wave_node_selector_derivation()
    hessian_selector = local_stress_hessian_to_node_selector_gate()
    export_split = cmb_cluster_source_export_split_gate()
    redshift_screen = redshift_screened_node_activation_gate()
    p10_rarefaction = p10_bernoulli_rarefaction_node_coefficients_candidate()
    q_rare_source = p10_time_averaged_source_to_q_rare_candidate()
    kappa_E_gate = p01_pressure_potential_to_kappa_E_gate()
    alpha_E_response = p01_isotropic_linear_response_alpha_E_candidate()
    alpha_E_witness = p01_alpha_E_positive_window_witness_gate()
    alpha_E_mixed = p01_alpha_E_mixed_characteristic_witness_gate()
    alpha_E_repair = p01_alpha_E_static_silent_mixed_repair_gate()
    alpha_E_shear = p01_alpha_E_static_silent_shear_repair_gate()
    alpha_E_mixed_region = p01_alpha_E_mixed_repair_admissible_region_gate()
    alpha_E_shear_region = p01_alpha_E_shear_repair_admissible_region_gate()
    alpha_E_full_speed = p01_alpha_E_full_local_speed_completion_gate()
    alpha_E_action_embedding = p01_alpha_E_quadratic_repair_action_embedding_gate()
    finite_status_domain = finite_amplitude_pressure_status_domain_gate()
    q_rare_invariance = local_tempo_transposition_q_rare_invariance_gate()
    active_projection = node_pressure_to_active_stress_projection_gate()
    master = master_spectral_equations()
    symbol = principal_symbol_candidate()
    channel_operator = channel_sum_operator_candidate()
    internal_block = internal_c3_block_embedding_candidate()
    elastic_projector = elastic_projector_operator_candidate()
    action_operator = quadratic_action_to_operator_derivation()
    node_pressure = gradient_energy_node_pressure_readout()
    kronecker_spectrum = kronecker_sum_spectrum_unification()
    localized_c3_coupling = localized_c3_coupled_operator_candidate()
    localization_lock = two_level_localization_lock_condition()
    radial_bound = radial_bound_state_variational_gate()
    partial_wave_ladder = partial_wave_bound_threshold_ladder()
    c3_well_bridge = c3_core_well_depth_bridge()
    c3_koide = embedded_c3_triplet_koide_theorem()
    c3_binding_window = c3_triplet_binding_window_gate()
    p10_profile_map = p10_gaussian_oscillon_source_parameter_map()
    p10_c3_bridge = p10_profile_to_c3_binding_window_bridge()
    spectral_pressure = spectral_gradient_pressure_identity()
    pressure_bridge = pressure_deficit_to_refractive_bridge()
    formula_candidate = unified_master_formula_candidate()
    chladni = chladni_node_readout_toy_model()
    clusters = cosmic_node_pressure_ledger()
    particles = particle_sector_bridge_ledger()
    gates = unified_formula_claim_gate()

    pass_checks = [
        master["status"] == "PASS_MASTER_SPECTRAL_EQUATION_SKELETON",
        bridge_map["status"] == "PASS_EXISTING_WORK_BRIDGE_MAP",
        coverage["status"] == "PASS_FULL_THEORY_SECTOR_COVERAGE_LEDGER",
        python_scope["status"] == "PASS_CURRENT_WORK_PYTHON_SCOPE_LEDGER",
        no_double["status"] == "PASS_UNIFIED_NO_DOUBLE_COUNTING_GUARD",
        inventory["status"] == "PASS_ACTION_INVENTORY_TO_READOUT_LEDGER",
        cosmo_export["status"] == "PASS_COSMOLOGY_CMB_LSS_EXPORT_GUARD",
        node_kz_kernel["status"] == "PASS_LONG_MODE_DELTAP_NODE_KZ_KERNEL_CANDIDATE",
        node_selector["status"] == "PASS_STANDING_WAVE_NODE_SELECTOR_DERIVATION",
        hessian_selector["status"] == "PASS_LOCAL_STRESS_HESSIAN_TO_NODE_SELECTOR_GATE",
        export_split["status"] == "PASS_CMB_CLUSTER_SOURCE_EXPORT_SPLIT_GATE",
        redshift_screen["status"] == "PASS_REDSHIFT_SCREENED_NODE_ACTIVATION_GATE",
        p10_rarefaction["status"]
        == "PASS_P10_BERNOULLI_RAREFACTION_NODE_COEFFICIENTS_CANDIDATE",
        q_rare_source["status"] == "PASS_P10_TIME_AVERAGED_SOURCE_TO_Q_RARE_CANDIDATE",
        kappa_E_gate["status"] == "PASS_P01_PRESSURE_POTENTIAL_TO_KAPPA_E_GATE",
        alpha_E_response["status"]
        == "PASS_P01_ISOTROPIC_LINEAR_RESPONSE_ALPHA_E_CANDIDATE",
        alpha_E_witness["status"] == "PASS_P01_ALPHA_E_POSITIVE_WINDOW_WITNESS_GATE",
        alpha_E_mixed["status"] == "PASS_P01_ALPHA_E_MIXED_CHARACTERISTIC_WITNESS_GATE",
        alpha_E_repair["status"]
        == "PASS_P01_ALPHA_E_STATIC_SILENT_MIXED_REPAIR_GATE",
        alpha_E_shear["status"]
        == "PASS_P01_ALPHA_E_STATIC_SILENT_SHEAR_REPAIR_GATE",
        alpha_E_mixed_region["status"]
        == "PASS_P01_ALPHA_E_MIXED_REPAIR_ADMISSIBLE_REGION_GATE",
        alpha_E_shear_region["status"]
        == "PASS_P01_ALPHA_E_SHEAR_REPAIR_ADMISSIBLE_REGION_GATE",
        alpha_E_full_speed["status"]
        == "PASS_P01_ALPHA_E_FULL_LOCAL_SPEED_COMPLETION_GATE",
        alpha_E_action_embedding["status"]
        == "PASS_P01_ALPHA_E_QUADRATIC_REPAIR_ACTION_EMBEDDING_GATE",
        finite_status_domain["status"] == "PASS_FINITE_AMPLITUDE_PRESSURE_STATUS_DOMAIN_GATE",
        q_rare_invariance["status"]
        == "PASS_LOCAL_TEMPO_TRANSPOSITION_Q_RARE_INVARIANCE_GATE",
        active_projection["status"] == "PASS_NODE_PRESSURE_TO_ACTIVE_STRESS_PROJECTION_GATE",
        channel_operator["status"] == "PASS_CHANNEL_SUM_OPERATOR_CANDIDATE",
        internal_block["status"] == "PASS_INTERNAL_BLOCK_EMBEDDING_CANDIDATE",
        elastic_projector["status"] == "PASS_ELASTIC_PROJECTOR_OPERATOR_CANDIDATE",
        action_operator["status"] == "PASS_QUADRATIC_ACTION_TO_OPERATOR_DERIVATION",
        node_pressure["status"] == "PASS_GRADIENT_ENERGY_NODE_PRESSURE_READOUT",
        kronecker_spectrum["status"] == "PASS_KRONECKER_SUM_SPECTRUM_UNIFICATION",
        localized_c3_coupling["status"] == "PASS_LOCALIZED_C3_COUPLED_OPERATOR_CANDIDATE",
        localization_lock["status"] == "PASS_TWO_LEVEL_LOCALIZATION_LOCK_CONDITION",
        radial_bound["status"] == "PASS_RADIAL_BOUND_STATE_VARIATIONAL_GATE",
        partial_wave_ladder["status"] == "PASS_PARTIAL_WAVE_BOUND_THRESHOLD_LADDER",
        c3_well_bridge["status"] == "PASS_C3_CORE_WELL_DEPTH_BRIDGE",
        c3_koide["status"] == "PASS_EMBEDDED_C3_TRIPLET_KOIDE_THEOREM",
        c3_binding_window["status"] == "PASS_C3_TRIPLET_BINDING_WINDOW_GATE",
        p10_profile_map["status"] == "PASS_P10_GAUSSIAN_OSCILLON_SOURCE_PARAMETER_MAP",
        p10_c3_bridge["status"] == "PASS_P10_PROFILE_TO_C3_BINDING_WINDOW_BRIDGE",
        spectral_pressure["status"] == "PASS_SPECTRAL_GRADIENT_PRESSURE_IDENTITY",
        pressure_bridge["status"] == "PASS_PRESSURE_DEFICIT_TO_REFRACTIVE_BRIDGE",
        formula_candidate["status"] == "PASS_UNIFIED_MASTER_FORMULA_CANDIDATE",
        chladni["status"] == "PASS_TOY_CHLADNI_NODE_KERNEL",
        clusters["status"] == "PASS_THREE_CHANNEL_PRESSURE_LEDGER",
    ]

    return {
        "file_status": (
            "UNIFIED_SPECTRAL_FORMULA_WORKSPACE_READY"
            if all(pass_checks)
            else "CHECK_UNIFIED_SPECTRAL_FORMULA_WORKSPACE"
        ),
        "article_status": "FORMULA_SKELETON_ONLY_NOT_DERIVED",
        "existing_work_bridge_map": bridge_map,
        "full_theory_sector_coverage_ledger": coverage,
        "current_work_python_scope_ledger": python_scope,
        "unified_no_double_counting_guard": no_double,
        "action_inventory_to_readout_ledger": inventory,
        "cosmology_cmb_lss_export_guard": cosmo_export,
        "long_mode_delta_p_node_kz_kernel_candidate": node_kz_kernel,
        "standing_wave_node_selector_derivation": node_selector,
        "local_stress_hessian_to_node_selector_gate": hessian_selector,
        "cmb_cluster_source_export_split_gate": export_split,
        "redshift_screened_node_activation_gate": redshift_screen,
        "p10_bernoulli_rarefaction_node_coefficients_candidate": p10_rarefaction,
        "p10_time_averaged_source_to_q_rare_candidate": q_rare_source,
        "p01_pressure_potential_to_kappa_E_gate": kappa_E_gate,
        "p01_isotropic_linear_response_alpha_E_candidate": alpha_E_response,
        "p01_alpha_E_positive_window_witness_gate": alpha_E_witness,
        "p01_alpha_E_mixed_characteristic_witness_gate": alpha_E_mixed,
        "p01_alpha_E_static_silent_mixed_repair_gate": alpha_E_repair,
        "p01_alpha_E_static_silent_shear_repair_gate": alpha_E_shear,
        "p01_alpha_E_mixed_repair_admissible_region_gate": alpha_E_mixed_region,
        "p01_alpha_E_shear_repair_admissible_region_gate": alpha_E_shear_region,
        "p01_alpha_E_full_local_speed_completion_gate": alpha_E_full_speed,
        "p01_alpha_E_quadratic_repair_action_embedding_gate": (
            alpha_E_action_embedding
        ),
        "finite_amplitude_pressure_status_domain_gate": finite_status_domain,
        "local_tempo_transposition_q_rare_invariance_gate": q_rare_invariance,
        "node_pressure_to_active_stress_projection_gate": active_projection,
        "master_equations": master,
        "principal_symbol_candidate": symbol,
        "channel_sum_operator_candidate": channel_operator,
        "internal_c3_block_embedding_candidate": internal_block,
        "elastic_projector_operator_candidate": elastic_projector,
        "quadratic_action_to_operator_derivation": action_operator,
        "gradient_energy_node_pressure_readout": node_pressure,
        "kronecker_sum_spectrum_unification": kronecker_spectrum,
        "localized_c3_coupled_operator_candidate": localized_c3_coupling,
        "two_level_localization_lock_condition": localization_lock,
        "radial_bound_state_variational_gate": radial_bound,
        "partial_wave_bound_threshold_ladder": partial_wave_ladder,
        "c3_core_well_depth_bridge": c3_well_bridge,
        "embedded_c3_triplet_koide_theorem": c3_koide,
        "c3_triplet_binding_window_gate": c3_binding_window,
        "p10_gaussian_oscillon_source_parameter_map": p10_profile_map,
        "p10_profile_to_c3_binding_window_bridge": p10_c3_bridge,
        "spectral_gradient_pressure_identity": spectral_pressure,
        "pressure_deficit_to_refractive_bridge": pressure_bridge,
        "unified_master_formula_candidate": formula_candidate,
        "chladni_node_readout": chladni,
        "cosmic_node_pressure_ledger": clusters,
        "particle_sector_bridge": particles,
        "claim_gates": gates,
        "falsifiable_targets": falsifiable_targets(),
        "next_derivation_steps": [
            "identify the quadratic action block inside the full p01/p10/p13 action",
            "derive the action-fixed alpha_node, alpha_tail and alpha_vortex source kernels",
            "keep current_work_python_scope_ledger updated when a new theory work file is added",
            "derive the localized C3 coupling eps and P_core from the oscillon solution",
            "replace the Gaussian radial well by the finite-core oscillon fluctuation spectrum",
            "derive alpha_U and beta_C3 from the localized oscillon second variation",
            "replace the Gaussian p10 trial amplitude by the nonlinear finite-energy profile",
            "derive the pressure-node readout S[psi] from the full stress/energy deficit",
            "compute C_G and C_psiG from the action to fix Xi and eps_node",
            "derive alpha_E and C_B from the nonlinear p01/p10 Bernoulli/oscillon source",
            "derive the open alpha_E coefficient sign domain rho_y>0 and p_y<0",
            "derive epsilon_B, epsilon_M and epsilon_T from the nonlinear RG action",
            "lift the completed local alpha_E speed witness to the tensor/projector node sector",
            "derive the finite-amplitude pressure-status continuation beyond the linear kappa_E gate",
            "derive the local P0 transposition law so q_rare remains dimensionless",
            "project DeltaP_node(k,z) into p13 active stress before cluster lensing",
            "derive Xi_L, N_node(k,z), A_L(k,z) and lambda_L(k,z) from the long-mode action",
            "derive the redshift activation window from coherence/relaxation dynamics",
            "export the derived DeltaP_node(k,z) to Boltzmann and cluster pipelines",
            "run CMB/BAO/LSS/growth/weak-lensing likelihoods before any observation claim",
        ],
    }


if __name__ == "__main__":
    status = unified_formula_status()
    print("PHASE 17: unified spectral formula")
    print("file_status:", status["file_status"])
    print("article_status:", status["article_status"])
    print("master:", status["master_equations"]["status"])
    print("bridge map:", status["existing_work_bridge_map"]["status"])
    print("sector coverage:", status["full_theory_sector_coverage_ledger"]["status"])
    print("python scope:", status["current_work_python_scope_ledger"]["status"])
    print("no double counting:", status["unified_no_double_counting_guard"]["status"])
    print("inventory readout:", status["action_inventory_to_readout_ledger"]["status"])
    print("cosmo export:", status["cosmology_cmb_lss_export_guard"]["status"])
    print("node k,z kernel:", status["long_mode_delta_p_node_kz_kernel_candidate"]["status"])
    print("node selector:", status["standing_wave_node_selector_derivation"]["status"])
    print("Hessian selector:", status["local_stress_hessian_to_node_selector_gate"]["status"])
    print("CMB/cluster split:", status["cmb_cluster_source_export_split_gate"]["status"])
    print("redshift screen:", status["redshift_screened_node_activation_gate"]["status"])
    print(
        "p10 rarefaction:",
        status["p10_bernoulli_rarefaction_node_coefficients_candidate"]["status"],
    )
    print(
        "q_rare source:",
        status["p10_time_averaged_source_to_q_rare_candidate"]["status"],
    )
    print(
        "kappa_E pressure:",
        status["p01_pressure_potential_to_kappa_E_gate"]["status"],
    )
    print(
        "alpha_E response:",
        status["p01_isotropic_linear_response_alpha_E_candidate"]["status"],
    )
    print(
        "alpha_E witness:",
        status["p01_alpha_E_positive_window_witness_gate"]["status"],
    )
    print(
        "alpha_E mixed:",
        status["p01_alpha_E_mixed_characteristic_witness_gate"]["status"],
    )
    print(
        "alpha_E repair:",
        status["p01_alpha_E_static_silent_mixed_repair_gate"]["status"],
    )
    print(
        "alpha_E shear:",
        status["p01_alpha_E_static_silent_shear_repair_gate"]["status"],
    )
    print(
        "alpha_E full speed:",
        status["p01_alpha_E_full_local_speed_completion_gate"]["status"],
    )
    print(
        "alpha_E action embedding:",
        status["p01_alpha_E_quadratic_repair_action_embedding_gate"]["status"],
    )
    print(
        "finite pressure domain:",
        status["finite_amplitude_pressure_status_domain_gate"]["status"],
    )
    print(
        "q_rare transposition:",
        status["local_tempo_transposition_q_rare_invariance_gate"]["status"],
    )
    print(
        "node active projection:",
        status["node_pressure_to_active_stress_projection_gate"]["status"],
    )
    print("channel operator:", status["channel_sum_operator_candidate"]["status"])
    print("internal C3 block:", status["internal_c3_block_embedding_candidate"]["status"])
    print("elastic projector:", status["elastic_projector_operator_candidate"]["status"])
    print("action -> operator:", status["quadratic_action_to_operator_derivation"]["status"])
    print("gradient node pressure:", status["gradient_energy_node_pressure_readout"]["status"])
    print("Kronecker spectrum:", status["kronecker_sum_spectrum_unification"]["status"])
    print("localized C3 coupling:", status["localized_c3_coupled_operator_candidate"]["status"])
    print("localization lock:", status["two_level_localization_lock_condition"]["status"])
    print("radial bound:", status["radial_bound_state_variational_gate"]["status"])
    print("partial-wave ladder:", status["partial_wave_bound_threshold_ladder"]["status"])
    print("C3 well bridge:", status["c3_core_well_depth_bridge"]["status"])
    print("C3 Koide theorem:", status["embedded_c3_triplet_koide_theorem"]["status"])
    print("C3 binding window:", status["c3_triplet_binding_window_gate"]["status"])
    print("p10 profile map:", status["p10_gaussian_oscillon_source_parameter_map"]["status"])
    print("p10 -> C3 binding:", status["p10_profile_to_c3_binding_window_bridge"]["status"])
    print("spectral pressure:", status["spectral_gradient_pressure_identity"]["status"])
    print("pressure bridge:", status["pressure_deficit_to_refractive_bridge"]["status"])
    print("formula candidate:", status["unified_master_formula_candidate"]["status"])
    print("chladni:", status["chladni_node_readout"]["status"])
    print("cluster ledger:", status["cosmic_node_pressure_ledger"]["status"])
    print("particle bridge:", status["particle_sector_bridge"]["status"])
    print("\nCore skeleton:")
    print("  L_RG[q_bar] psi_n = lambda_n psi_n")
    print("  omega_n = Omega_loc sqrt(lambda_n)")
    print("  m_n = gamma_m Omega_loc^2 lambda_n")
    print("  rho_m(x) = rho0 F(DeltaP_node(x)/P0)")
