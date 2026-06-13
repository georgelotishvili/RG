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
        "p13_refractive_force.py": [
            "active stress source S_h = p_rad' - 2*Delta_p/r",
            "h_eff' = S_h/(c^2 rho_eff)",
            "n_eff = exp(h_eff)",
            "local Bernoulli and vortex channels add in one source ledger",
        ],
        "p11_particles.py": [
            "C3/order-9 charged-lepton internal spectral candidate",
            "m proportional to nu^2 still needs oscillon-energy derivation",
            "C3 block should become an internal sector of L_RG",
        ],
        "p09_bullet.py": [
            "cluster residuals are a three-channel problem",
            "cosmic-node baseline, local oscillon-tail retention, vortex/MOND transport",
        ],
        "p08_cmb.py": [
            "same-input CMB branch is closed only as inheritance",
            "no-particle-DM and long-mode replacement require Boltzmann likelihoods",
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
    master = master_spectral_equations()
    symbol = principal_symbol_candidate()
    channel_operator = channel_sum_operator_candidate()
    internal_block = internal_c3_block_embedding_candidate()
    elastic_projector = elastic_projector_operator_candidate()
    pressure_bridge = pressure_deficit_to_refractive_bridge()
    formula_candidate = unified_master_formula_candidate()
    chladni = chladni_node_readout_toy_model()
    clusters = cosmic_node_pressure_ledger()
    particles = particle_sector_bridge_ledger()
    gates = unified_formula_claim_gate()

    pass_checks = [
        master["status"] == "PASS_MASTER_SPECTRAL_EQUATION_SKELETON",
        bridge_map["status"] == "PASS_EXISTING_WORK_BRIDGE_MAP",
        channel_operator["status"] == "PASS_CHANNEL_SUM_OPERATOR_CANDIDATE",
        internal_block["status"] == "PASS_INTERNAL_BLOCK_EMBEDDING_CANDIDATE",
        elastic_projector["status"] == "PASS_ELASTIC_PROJECTOR_OPERATOR_CANDIDATE",
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
        "master_equations": master,
        "principal_symbol_candidate": symbol,
        "channel_sum_operator_candidate": channel_operator,
        "internal_c3_block_embedding_candidate": internal_block,
        "elastic_projector_operator_candidate": elastic_projector,
        "pressure_deficit_to_refractive_bridge": pressure_bridge,
        "unified_master_formula_candidate": formula_candidate,
        "chladni_node_readout": chladni,
        "cosmic_node_pressure_ledger": clusters,
        "particle_sector_bridge": particles,
        "claim_gates": gates,
        "falsifiable_targets": falsifiable_targets(),
        "next_derivation_steps": [
            "replace the scalar channel-sum symbol by the full tensor operator C^{ij}_{AB}",
            "derive the pressure-node readout S[psi] from stress/energy deficit",
            "embed the p11 C3/order-9 particle operator as a finite internal block",
            "derive DeltaP_node for long modes and export it to p09 clusters",
            "build a numerical toy solver before any CMB/BAO/LSS claim",
        ],
    }


if __name__ == "__main__":
    status = unified_formula_status()
    print("PHASE 17: unified spectral formula")
    print("file_status:", status["file_status"])
    print("article_status:", status["article_status"])
    print("master:", status["master_equations"]["status"])
    print("bridge map:", status["existing_work_bridge_map"]["status"])
    print("channel operator:", status["channel_sum_operator_candidate"]["status"])
    print("internal C3 block:", status["internal_c3_block_embedding_candidate"]["status"])
    print("elastic projector:", status["elastic_projector_operator_candidate"]["status"])
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
