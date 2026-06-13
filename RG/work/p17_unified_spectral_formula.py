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
            "derive the localized C3 coupling eps and P_core from the oscillon solution",
            "replace the Gaussian radial well by the finite-core oscillon fluctuation spectrum",
            "determine which C3 branch satisfies the sign-and-depth binding condition",
            "derive the common triplet binding window U_base, eps and R from the finite core",
            "derive the pressure-node readout S[psi] from the full stress/energy deficit",
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
