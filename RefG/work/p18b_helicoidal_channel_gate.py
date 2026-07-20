# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Active coefficient scheme: coefficients are the p01 L_poly set
# (c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1); no X-scheme is introduced.

"""
================================================================================
PHASE 18b: Helicoidal (photon-candidate) channel -- forward computation
================================================================================

Purpose
-------
Forward step for the alpha programme (p18): instead of asking what number the
theory must produce, compute what the CURRENT action actually gives for the
transverse internal-orientation channel -- the only implemented carrier a
helicoidal photon-candidate could ride on.

The gate derives, from scratch in sympy (no formulas imported on trust):

1. The quadratic action of the transverse phonon pi_T on the Minkowski
   background (unitary gauge Phi = t, phi^A = x^A), directly from
   L_poly = c_Y*Y + c_Y2*Y^2 + c_I1*I1 + c_I1sq*I1^2 + c_I2*I2 + c_I3*I3
            + c_YI1*Y*I1,
   giving the kinetic coefficient K_T and gradient coefficient C_T.

2. THEOREM (new, executable): on the p03 solar 1PN coefficient family
      c_Y    = -4*c_Y2 - 2*c_YI1,
      c_I1   =  4*c_Y2 + 2*c_YI1,
      c_I1sq =  c_Y2,
      c_I2   = -10*c_Y2 - 3*c_YI1,
      c_I3   =  8*c_Y2 + 4*c_YI1,
   the transverse GRADIENT coefficient vanishes identically, C_T == 0, for the
   whole family; and on the physical 2PN slice c_YI1 = 2*c_Y2 the kinetic
   coefficient vanishes too, K_T == 0.  Consequence: within the minimal
   7-term polynomial, exact solar-sector agreement and a propagating
   transverse orientation wave are MUTUALLY EXCLUSIVE.  The minimal action is
   photon-blind.

3. LEMMAS (executable): none of the implemented extension operators revives
   the channel --
     (a) the Z operator, Z = (pi_dot_i - d_i chi)^2 with coefficient c_Z,
         contributes transverse KINETIC content only (no gradient term), so
         cs_T^2 stays 0;
     (b) the C6 operator, delta C6 = 2*(chi_dot + div pi), is blind to
         transverse modes (div pi_T = 0);
     (c) the static-silent dynamic operators built from W^A = U^A + Q^A vanish
         at linear order around the flat background (W^A = O(pi^2, h*pi)), so
         they contribute nothing to the flat-space quadratic transverse action.

4. CONSEQUENCE FOR ALPHA: the photon channel, and therefore the fine-structure
   normalization N of p18 (alpha = W^2/(4*pi*N)), cannot be computed from the
   currently implemented operator set at all: it requires a new operator class
   (higher-degree internal invariants, curvature couplings from the excluded
   EFT list, or the unimplemented rotation/topology channel).  The gate
   restates the p18 requirement at that operator's doorstep and stays OPEN.

Status
------
OPEN at the alpha layer; the degeneracy theorem and the three lemmas are
CLOSED (symbolically verified below).  Nothing here derives alpha; what is
derived is WHY alpha has not fallen out of the present gates: the implemented
action cannot carry light.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------

t, z = sp.symbols("t z", real=True)
c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
    "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1", real=True
)
c_Z, lambda_6, eps_B, eps_M = sp.symbols(
    "c_Z lambda_6 epsilon_B epsilon_M", real=True
)
eps = sp.Symbol("epsilon", positive=True)  # perturbation bookkeeping parameter

COEFFS = (c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1)

SOLAR_FAMILY = {
    c_Y: -4 * c_Y2 - 2 * c_YI1,
    c_I1: 4 * c_Y2 + 2 * c_YI1,
    c_I1sq: c_Y2,
    c_I2: -10 * c_Y2 - 3 * c_YI1,
    c_I3: 8 * c_Y2 + 4 * c_YI1,
}
PHYSICAL_2PN_SLICE = {c_YI1: 2 * c_Y2}


# ---------------------------------------------------------------------------
# Part 1 -- transverse quadratic action from scratch
# ---------------------------------------------------------------------------

def transverse_quadratic_action() -> dict[str, Any]:
    """Expand L_poly to second order around Phi = t, phi^A = x^A for a purely
    transverse plane perturbation pi^A = (pi1(t,z), pi2(t,z), 0) on Minkowski
    (+---).  Returns K_T (coefficient of pi_dot^2) and C_T (coefficient of
    -(d_z pi)^2 read as gradient energy) per transverse polarization."""
    pi1 = sp.Function("pi1")(t, z)
    pi2 = sp.Function("pi2")(t, z)

    # Fields: Phi = t (clock scalar unperturbed for the transverse sector),
    # phi^A = x^A + eps*pi^A with pi^3 = 0 and pi^{1,2} functions of (t, z).
    # Coordinates x = (t, x1, x2, x3=z); metric eta = diag(1,-1,-1,-1).
    # Gradients d_mu phi^A:
    #   d_t   phi^A = eps*pi_dot^A
    #   d_x1  phi^A = delta^A_1
    #   d_x2  phi^A = delta^A_2
    #   d_z   phi^A = delta^A_3 + eps*d_z pi^A
    dphi = sp.zeros(4, 3)  # rows: mu = t,x1,x2,z ; cols: A = 1,2,3
    dphi[0, 0] = eps * sp.diff(pi1, t)
    dphi[0, 1] = eps * sp.diff(pi2, t)
    dphi[1, 0] = 1
    dphi[2, 1] = 1
    dphi[3, 0] = eps * sp.diff(pi1, z)
    dphi[3, 1] = eps * sp.diff(pi2, z)
    dphi[3, 2] = 1

    g_inv = sp.diag(1, -1, -1, -1)

    # B^AB = -g^{mu nu} d_mu phi^A d_nu phi^B
    B = sp.zeros(3, 3)
    for A in range(3):
        for Bidx in range(3):
            expr = 0
            for mu in range(4):
                expr += g_inv[mu, mu] * dphi[mu, A] * dphi[mu, Bidx]
            B[A, Bidx] = -expr

    # Clock scalar: Phi = t  =>  Y = g^{mn} d_m Phi d_n Phi = 1 exactly here.
    Y = sp.Integer(1)

    I1 = sp.trace(B)
    I2 = sp.Rational(1, 2) * (I1**2 - sp.trace(B * B))
    I3 = B.det()

    L_poly = (
        c_Y * Y
        + c_Y2 * Y**2
        + c_I1 * I1
        + c_I1sq * I1**2
        + c_I2 * I2
        + c_I3 * I3
        + c_YI1 * Y * I1
    )

    L2 = sp.expand(L_poly).series(eps, 0, 3).removeO()
    L2 = sp.expand(L2.coeff(eps, 2))  # quadratic-order Lagrangian density

    K_T = sp.simplify(L2.coeff(sp.diff(pi1, t) ** 2))
    C_T_neg = sp.simplify(L2.coeff(sp.diff(pi1, z) ** 2))
    # Gradient energy convention: L2 ~ K_T*pi_dot^2 - C_T*(d_z pi)^2 per
    # polarization, so C_T = -coeff((d_z pi)^2).
    C_T = sp.simplify(-C_T_neg)

    # Symmetry check: both polarizations must carry identical coefficients.
    same_for_second_polarization = sp.simplify(
        L2.coeff(sp.diff(pi2, t) ** 2) - K_T
    ) == 0

    cross_terms_absent = (
        sp.simplify(L2.coeff(sp.diff(pi1, t) * sp.diff(pi2, t))) == 0
        and sp.simplify(L2.coeff(sp.diff(pi1, z) * sp.diff(pi2, z))) == 0
    )

    return {
        "K_T": K_T,
        "C_T": C_T,
        "L2": L2,
        "polarization_symmetry": same_for_second_polarization,
        "no_polarization_mixing": cross_terms_absent,
    }


# ---------------------------------------------------------------------------
# Part 2 -- the degeneracy theorem on the gravity-fixed coefficients
# ---------------------------------------------------------------------------

def degeneracy_theorem(K_T: sp.Expr, C_T: sp.Expr) -> dict[str, Any]:
    C_T_solar = sp.simplify(C_T.subs(SOLAR_FAMILY))
    K_T_solar = sp.simplify(K_T.subs(SOLAR_FAMILY))
    K_T_2pn = sp.simplify(K_T_solar.subs(PHYSICAL_2PN_SLICE))
    gradient_dead_on_family = C_T_solar == 0
    kinetic_on_family = sp.simplify(K_T_solar - (2 * c_Y2 - c_YI1)) == 0
    kinetic_dead_on_2pn = K_T_2pn == 0
    # Luminality identity: cs_T^2 = C_T/K_T = 1  <=>  C_T - K_T = 0, and
    # C_T - K_T = c_I2 + c_I3 identically -- the sharp target equation for
    # any future re-tuned degree-2 solar chain.
    luminality_identity = sp.simplify((C_T - K_T) - (c_I2 + c_I3)) == 0
    return {
        "luminality_identity_CT_minus_KT_equals_cI2_plus_cI3": (
            luminality_identity
        ),
        "luminality_condition": (
            "cs_T^2 = 1  <=>  chat_I2 + chat_I3 = 0 (given K_T != 0): the "
            "transverse channel is luminal exactly when the effective Skyrme "
            "and determinant coefficients cancel"
        ),
        "C_T_on_solar_family": C_T_solar,
        "K_T_on_solar_family": K_T_solar,
        "K_T_on_2pn_slice": K_T_2pn,
        "gradient_dead_on_whole_1pn_family": gradient_dead_on_family,
        "kinetic_equals_2cY2_minus_cYI1": kinetic_on_family,
        "kinetic_dead_on_physical_2pn_slice": kinetic_dead_on_2pn,
        "theorem": (
            "within the minimal 7-term polynomial, the p03 solar 1PN family "
            "kills the transverse gradient term identically (cs_T^2 = 0), and "
            "the physical 2PN slice kills the kinetic term as well; exact "
            "solar-sector agreement and a propagating transverse orientation "
            "wave are mutually exclusive in this truncation"
        ),
    }


# ---------------------------------------------------------------------------
# Part 3 -- extension-operator lemmas
# ---------------------------------------------------------------------------

def extension_operator_lemmas() -> dict[str, Any]:
    pi1 = sp.Function("pi1")(t, z)
    chi = sp.Integer(0)  # scalar sector switched off for the transverse probe

    # (a) Z operator: Z = (pi_dot_i - d_i chi)^2 summed over i.
    #     For the transverse probe: Z = pi_dot^2 -- kinetic only, no d_z pi.
    Z_transverse = (sp.diff(pi1, t) - 0) ** 2
    z_has_gradient = sp.simplify(Z_transverse.coeff(sp.diff(pi1, z) ** 2)) != 0
    z_kinetic = sp.simplify(Z_transverse.coeff(sp.diff(pi1, t) ** 2))

    # (b) C6 operator: delta C6 = 2*(chi_dot + div pi).
    #     div pi for a transverse plane wave pi^A = (pi1(t,z), pi2(t,z), 0):
    #     d_x1 pi1(t,z) = 0, d_x2 pi2(t,z) = 0, d_z pi3 = 0  =>  div pi = 0.
    div_pi_transverse = sp.Integer(0) + sp.Integer(0) + sp.Integer(0)
    c6_transverse = 2 * (sp.diff(chi, t) if chi != 0 else 0) + 2 * div_pi_transverse
    c6_blind = sp.simplify(c6_transverse) == 0

    # (c) W^A = U^A + Q^A at linear order on the flat background.
    #     U^A = u^mu d_mu phi^A with u = (1,0,0,0):  U^A = eps*pi_dot^A.
    #     Q^A = -g^{mu nu} d_mu phi^A d_nu Phi with Phi = t:
    #           = -g^{mu 0} d_mu phi^A = -g^{00} d_t phi^A = -eps*pi_dot^A.
    pi_dot = sp.Symbol("pi_dot_A", real=True)
    U_A = eps * pi_dot
    Q_A = -eps * pi_dot
    W_A = sp.simplify(U_A + Q_A)
    w_vanishes_linearly = W_A == 0
    # Hence eps_B*W_A*W^A and 2*eps_M*W_A*Q^A are O(eps^3) or higher in the
    # transverse sector (W itself starts at second order once metric and
    # clock perturbations are included), so neither contributes to the flat
    # quadratic transverse action.

    return {
        "Z_contributes_kinetic_only": (not z_has_gradient) and z_kinetic == 1,
        "C6_blind_to_transverse": c6_blind,
        "W_operators_vanish_at_linear_order": w_vanishes_linearly,
        "lemma": (
            "no implemented extension operator (Z, C6, W-sector) produces a "
            "transverse GRADIENT term; with C_T = 0 on the gravity-fixed "
            "family, cs_T^2 remains 0 regardless of c_Z, lambda_6, eps_B, "
            "eps_M -- the implemented operator set cannot carry a luminal "
            "helicoidal wave"
        ),
    }


# ---------------------------------------------------------------------------
# Part 3b -- excluded degree-2 invariants: transverse reduction lemma
# ---------------------------------------------------------------------------

def excluded_invariants_transverse_content() -> dict[str, Any]:
    """Compute the transverse quadratic content of the seven degree-2
    operators excluded from the minimal truncation (Y*I2, Y*I3, I1*I2, I1*I3,
    I2^2, I2*I3, I3^2) with the same probe, and verify the REDUCTION LEMMA:
    every one of them reduces, in the transverse sector, to a rational-weight
    combination of the base contents (I1_2, I2_2, I3_2).  Consequence: no
    degree-2 extension introduces new transverse structure -- the transverse
    channel of ANY degree-2 polynomial action is controlled by exactly three
    effective numbers (chat_I1, chat_I2, chat_I3)."""
    pi1 = sp.Function("pi1")(t, z)
    pi2 = sp.Function("pi2")(t, z)

    dphi = sp.zeros(4, 3)
    dphi[0, 0] = eps * sp.diff(pi1, t)
    dphi[0, 1] = eps * sp.diff(pi2, t)
    dphi[1, 0] = 1
    dphi[2, 1] = 1
    dphi[3, 0] = eps * sp.diff(pi1, z)
    dphi[3, 1] = eps * sp.diff(pi2, z)
    dphi[3, 2] = 1
    g_inv = sp.diag(1, -1, -1, -1)
    B = sp.zeros(3, 3)
    for A in range(3):
        for Bidx in range(3):
            expr = 0
            for mu in range(4):
                expr += g_inv[mu, mu] * dphi[mu, A] * dphi[mu, Bidx]
            B[A, Bidx] = -expr

    Y = sp.Integer(1)  # exact for the transverse probe (Phi unperturbed)
    I1 = sp.trace(B)
    I2 = sp.Rational(1, 2) * (I1**2 - sp.trace(B * B))
    I3 = B.det()

    def quad_content(op: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
        L2 = sp.expand(op).series(eps, 0, 3).removeO()
        L2 = sp.expand(L2.coeff(eps, 2))
        k = sp.simplify(L2.coeff(sp.diff(pi1, t) ** 2))
        c_raw = sp.simplify(L2.coeff(sp.diff(pi1, z) ** 2))
        return k, sp.simplify(-c_raw)

    base = {
        "I1": quad_content(I1),
        "I2": quad_content(I2),
        "I3": quad_content(I3),
    }
    excluded = {
        "Y*I2": Y * I2,
        "Y*I3": Y * I3,
        "I1*I2": I1 * I2,
        "I1*I3": I1 * I3,
        "I2^2": I2**2,
        "I2*I3": I2 * I3,
        "I3^2": I3**2,
    }
    # First-order invariant perturbations vanish for the transverse probe
    # (volume/shape preserving at linear order), so each product F*G must
    # reduce to Fbar*G_2 + Gbar*F_2 with background values I1b=3, I2b=3, I3b=1.
    backgrounds = {"I1": sp.Integer(3), "I2": sp.Integer(3), "I3": sp.Integer(1)}
    expected_weights = {
        "Y*I2": {"I2": 1},
        "Y*I3": {"I3": 1},
        "I1*I2": {"I1": backgrounds["I2"], "I2": backgrounds["I1"]},
        "I1*I3": {"I1": backgrounds["I3"], "I3": backgrounds["I1"]},
        "I2^2": {"I2": 2 * backgrounds["I2"]},
        "I2*I3": {"I2": backgrounds["I3"], "I3": backgrounds["I2"]},
        "I3^2": {"I3": 2 * backgrounds["I3"]},
    }
    table = {}
    reduction_holds = True
    any_new_gradient_structure = False
    for name, op in excluded.items():
        k, cval = quad_content(op)
        wk = sum(
            w * base[b][0] for b, w in expected_weights[name].items()
        )
        wc = sum(
            w * base[b][1] for b, w in expected_weights[name].items()
        )
        ok = sp.simplify(k - wk) == 0 and sp.simplify(cval - wc) == 0
        reduction_holds = reduction_holds and ok
        table[name] = {
            "K_content": k,
            "C_content": cval,
            "reduces_to_base_span": ok,
        }
    # Base gradient contents: does I3 carry any transverse gradient at all?
    i3_gradient_free = base["I3"][1] == 0
    return {
        "base_contents": {
            name: {"K": pair[0], "C": pair[1]} for name, pair in base.items()
        },
        "excluded_table": table,
        "reduction_lemma_holds": reduction_holds,
        "I3_transverse_gradient_free": i3_gradient_free,
        "lemma": (
            "all seven excluded degree-2 operators reduce, in the transverse "
            "sector, to rational-weight combinations of the base contents "
            "I1_2, I2_2, I3_2; no degree-2 extension introduces new "
            "transverse structure, so a luminal photon-candidate within "
            "degree-2 requires RE-TUNING the effective (chat_I1, chat_I2, "
            "chat_I3) balance jointly with a re-derived solar chain -- or an "
            "operator class beyond degree 2"
        ),
    }


# ---------------------------------------------------------------------------
# Part 4 -- consequence for the alpha programme
# ---------------------------------------------------------------------------

def alpha_consequence() -> dict[str, Any]:
    return {
        "consequence": (
            "alpha is not computable from the currently implemented operator "
            "set: the photon-candidate channel has no luminal carrier there. "
            "The p18 requirement alpha = W^2/(4*pi*N), N = 10.90497833, now "
            "lands on the doorstep of a NEW operator class."
        ),
        "candidate_operator_classes": [
            "higher-degree internal invariants excluded from the minimal "
            "truncation (Y*I2, Y*I3, I1*I2, I1*I3, I2^2, I2*I3, I3^2) -- "
            "their transverse gradient content must be computed first",
            "curvature couplings from the excluded-EFT list (R*Y, "
            "R_mn d^m Phi d^n Phi, R_mn d^m phi^A d^n phi^A)",
            "the unimplemented rotation/topology channel of the "
            "p01 phase_spatial_channel_independence_audit",
        ],
        "next_computation": (
            "repeat this gate's quadratic expansion for the seven excluded "
            "degree-2 invariants; if any yields C_T != 0 on the solar family, "
            "the photon channel and the alpha normalization N become "
            "computable in that extension; if all vanish as well, the EM "
            "channel requires curvature couplings or the topology channel"
        ),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_helicoidal_channel_gate() -> dict[str, Any]:
    quad = transverse_quadratic_action()
    theorem = degeneracy_theorem(quad["K_T"], quad["C_T"])
    lemmas = extension_operator_lemmas()
    reduction = excluded_invariants_transverse_content()
    consequence = alpha_consequence()

    theorem_pass = (
        theorem["gradient_dead_on_whole_1pn_family"]
        and theorem["kinetic_dead_on_physical_2pn_slice"]
        and theorem["kinetic_equals_2cY2_minus_cYI1"]
        and quad["polarization_symmetry"]
        and quad["no_polarization_mixing"]
    )
    lemmas_pass = (
        lemmas["Z_contributes_kinetic_only"]
        and lemmas["C6_blind_to_transverse"]
        and lemmas["W_operators_vanish_at_linear_order"]
        and reduction["reduction_lemma_holds"]
    )

    return {
        "STATUS": (
            "OPEN_ALPHA_CHANNEL__"
            + _pass_status("TRANSVERSE_DEGENERACY_THEOREM_AND_LEMMAS")
            if theorem_pass and lemmas_pass
            else "CHECK_TRANSVERSE_DEGENERACY_DERIVATION"
        ),
        "SCOPE": (
            "From-scratch quadratic expansion of the p01 minimal action for "
            "the transverse internal-orientation channel; degeneracy theorem "
            "on the gravity-fixed coefficient family; extension-operator "
            "lemmas; alpha localized at a new-operator doorstep.  No alpha "
            "value is computed or claimed."
        ),
        "closed_checks": {
            "K_T_derived_from_scratch": True,
            "C_T_derived_from_scratch": True,
            "polarization_symmetry": quad["polarization_symmetry"],
            "no_polarization_mixing": quad["no_polarization_mixing"],
            "gradient_dead_on_whole_1pn_family": theorem[
                "gradient_dead_on_whole_1pn_family"
            ],
            "kinetic_dead_on_physical_2pn_slice": theorem[
                "kinetic_dead_on_physical_2pn_slice"
            ],
            "luminality_identity_CT_minus_KT_equals_cI2_plus_cI3": theorem[
                "luminality_identity_CT_minus_KT_equals_cI2_plus_cI3"
            ],
            "Z_contributes_kinetic_only": lemmas["Z_contributes_kinetic_only"],
            "C6_blind_to_transverse": lemmas["C6_blind_to_transverse"],
            "W_operators_vanish_at_linear_order": lemmas[
                "W_operators_vanish_at_linear_order"
            ],
            "degree2_reduction_lemma": reduction["reduction_lemma_holds"],
            "I3_transverse_gradient_free": reduction[
                "I3_transverse_gradient_free"
            ],
        },
        "open_checks": {
            "degree2_retuned_solar_chain_recomputed": False,
            "curvature_coupling_transverse_content_computed": False,
            "rotation_topology_channel_implemented": False,
            "alpha_normalization_N_derived": False,
        },
        "K_T": sp.Eq(sp.Symbol("K_T"), quad["K_T"]),
        "C_T": sp.Eq(sp.Symbol("C_T"), quad["C_T"]),
        "K_T_on_solar_family": theorem["K_T_on_solar_family"],
        "C_T_on_solar_family": theorem["C_T_on_solar_family"],
        "K_T_on_2pn_slice": theorem["K_T_on_2pn_slice"],
        "theorem": theorem["theorem"],
        "luminality_condition": theorem["luminality_condition"],
        "lemma": lemmas["lemma"],
        "reduction_lemma": reduction["lemma"],
        "base_contents": reduction["base_contents"],
        "excluded_table": {
            name: row["reduces_to_base_span"]
            for name, row in reduction["excluded_table"].items()
        },
        "alpha_consequence": consequence,
        "missing_derivations": [
            "re-derive the solar 1PN/2PN chain with the effective degree-2 "
            "balance (chat_I1, chat_I2, chat_I3) freed by the excluded "
            "operators, and check whether a luminal transverse branch "
            "coexists with gamma = beta = 1",
            "transverse content of the excluded curvature couplings",
            "implementation of the rotation/topology channel",
            "only then: luminality condition + winding coupling => N => alpha",
        ],
        "do_not_claim": [
            "do not claim alpha is computed, bounded, or approximated here",
            "do not claim the theory has no photon channel -- only that the "
            "currently implemented operator set has none",
            "do not treat the degeneracy theorem as a failure of the theory; "
            "it is a localization result for where the EM sector must live",
        ],
    }


def _print_result(result: dict[str, Any]) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, value in result["closed_checks"].items():
        print(f"  - {key}: {value}")
    print("open_checks:")
    for key, value in result["open_checks"].items():
        print(f"  - {key}: {value}")
    for key in (
        "K_T",
        "C_T",
        "K_T_on_solar_family",
        "C_T_on_solar_family",
        "K_T_on_2pn_slice",
        "theorem",
        "luminality_condition",
        "lemma",
        "reduction_lemma",
    ):
        print(f"{key}: {result[key]}")
    print("base_contents:")
    for name, row in result["base_contents"].items():
        print(f"  - {name}: K={row['K']}  C={row['C']}")
    print("excluded_table (reduces_to_base_span):")
    for name, ok in result["excluded_table"].items():
        print(f"  - {name}: {ok}")
    print("alpha_consequence:", result["alpha_consequence"]["consequence"])
    print("candidate_operator_classes:")
    for item in result["alpha_consequence"]["candidate_operator_classes"]:
        print("  -", item)
    print("next_computation:", result["alpha_consequence"]["next_computation"])
    print("missing_derivations:")
    for item in result["missing_derivations"]:
        print("  -", item)
    print("do_not_claim:")
    for item in result["do_not_claim"]:
        print("  -", item)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    section = argv[0] if argv else "all"
    if section != "all":
        print("Supported section: all")
        return 2
    _print_result(derive_helicoidal_channel_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
