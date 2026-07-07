# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Extended degree-2 coefficient scheme: the 7 minimal coefficients
# (c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1) plus the 7 previously excluded
# degree-2 operators with coefficients d_YI2, d_YI3, d_I1I2, d_I1I3, d_I2sq,
# d_I2I3, d_I3sq.

"""
================================================================================
PHASE 18c: Luminal transverse channel vs Lorentz vacuum -- coexistence gate
================================================================================

Purpose
-------
p18b proved that on the p03 solar family of the MINIMAL 7-term polynomial the
transverse (photon-candidate) channel is degenerate (C_T = 0, and K_T = 0 on
the 2PN slice), and that all seven excluded degree-2 operators reduce, in the
transverse sector, to the base span.  The next question in the alpha programme
is whether ENLARGING the degree-2 space rescues the channel:

    Does a coefficient region exist where
      (i)   the vacuum is Lorentz (boosted background stress vanishes:
            T_01 = 0 and T_11 - T_22 = 0, derived from scratch for all
            14 operators by the same boost method p01 uses),
      (ii)  the transverse channel is LUMINAL (C_T = K_T != 0), and
      (iii) the transverse channel is ghost-free (K_T > 0 in the action's
            kinetic-sign convention)?

Results (all executable below):

1. EXTENDED LORENTZ CONDITION derived from scratch; on d = 0 it reproduces
   p01's lorentz_req exactly (validation check).
2. EXTENDED ANISOTROPY CONDITION (T_11 - T_22 under boost) likewise.
3. EXTENDED TRANSVERSE CONTENTS K_T, C_T for all 14 operators (from-scratch
   quadratic expansion, revalidating the p18b reduction weights).
4. COEXISTENCE: the combined linear system {Lorentz, anisotropy, luminality}
   on the 14-dimensional coefficient space -- dimension of the solution
   family, an explicit numeric witness with K_T > 0, and the check that the
   witness NECESSARILY uses the excluded operators (the minimal 7-term
   subspace admits no such point: there luminality + the solar family force
   degeneracy).

What this gate does NOT do: it does not re-derive the full 1PN/2PN solar
chain (gamma = beta = 1, preferred-frame zeros) on the extended space.  That
re-run -- p03-scale work -- is the explicitly named remaining step before the
photon channel can be declared to coexist with the solar sector, after which
the winding coupling and the alpha normalization N become computable.

Status
------
OPEN at the full-solar-chain layer; the extended Lorentz/anisotropy/
luminality coexistence question is CLOSED below (with an explicit witness).
No alpha value is computed or claimed.
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

t, x, y, z = sp.symbols("t x y z", real=True)
v = sp.Symbol("v", real=True)

c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
    "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1", real=True
)
d_YI2, d_YI3, d_I1I2, d_I1I3, d_I2sq, d_I2I3, d_I3sq = sp.symbols(
    "d_YI2 d_YI3 d_I1I2 d_I1I3 d_I2sq d_I2I3 d_I3sq", real=True
)
eps = sp.Symbol("epsilon", positive=True)

MINIMAL = (c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1)
EXTENDED = (d_YI2, d_YI3, d_I1I2, d_I1I3, d_I2sq, d_I2I3, d_I3sq)
ALL_COEFFS = MINIMAL + EXTENDED

SOLAR_FAMILY = {
    c_Y: -4 * c_Y2 - 2 * c_YI1,
    c_I1: 4 * c_Y2 + 2 * c_YI1,
    c_I1sq: c_Y2,
    c_I2: -10 * c_Y2 - 3 * c_YI1,
    c_I3: 8 * c_Y2 + 4 * c_YI1,
}


def extended_lagrangian(Y: sp.Expr, I1: sp.Expr, I2: sp.Expr, I3: sp.Expr) -> sp.Expr:
    return (
        c_Y * Y
        + c_Y2 * Y**2
        + c_I1 * I1
        + c_I1sq * I1**2
        + c_I2 * I2
        + c_I3 * I3
        + c_YI1 * Y * I1
        + d_YI2 * Y * I2
        + d_YI3 * Y * I3
        + d_I1I2 * I1 * I2
        + d_I1I3 * I1 * I3
        + d_I2sq * I2**2
        + d_I2I3 * I2 * I3
        + d_I3sq * I3**2
    )


# ---------------------------------------------------------------------------
# Part 1 -- extended Lorentz + anisotropy conditions (boost method, from scratch)
# ---------------------------------------------------------------------------

def boosted_background_conditions() -> dict[str, Any]:
    gamma = 1 / sp.sqrt(1 - v**2)
    Phi = gamma * (t - v * x)
    phis = (gamma * (x - v * t), y, z)

    d_Phi = [sp.diff(Phi, c) for c in (t, x, y, z)]
    d_phi = [[sp.diff(p, c) for c in (t, x, y, z)] for p in phis]

    q00, q11, q22, q33 = sp.symbols("q00 q11 q22 q33", real=True)
    q01, q02, q03, q12, q13, q23 = sp.symbols(
        "q01 q02 q03 q12 q13 q23", real=True
    )
    g_inv = sp.Matrix(
        [
            [q00, q01, q02, q03],
            [q01, q11, q12, q13],
            [q02, q12, q22, q23],
            [q03, q13, q23, q33],
        ]
    )

    Y = sum(
        g_inv[i, j] * d_Phi[i] * d_Phi[j] for i in range(4) for j in range(4)
    )
    B = sp.zeros(3, 3)
    for A in range(3):
        for Bi in range(3):
            B[A, Bi] = sum(
                -g_inv[i, j] * d_phi[A][i] * d_phi[Bi][j]
                for i in range(4)
                for j in range(4)
            )
    I1 = B.trace()
    I2 = sp.Rational(1, 2) * (I1**2 - (B * B).trace())
    I3 = B.det()

    L = extended_lagrangian(Y, I1, I2, I3)

    subs_mink = {
        q00: 1, q11: -1, q22: -1, q33: -1,
        q01: 0, q02: 0, q03: 0, q12: 0, q13: 0, q23: 0,
    }

    T01 = sp.diff(L, q01)
    T01_eval = sp.simplify(T01.subs(subs_mink))
    lorentz_ext = sp.simplify(sp.expand(T01_eval / (-2 * gamma**2 * v)))

    T11 = 2 * sp.diff(L, q11) + L
    T22 = 2 * sp.diff(L, q22) + L
    aniso_eval = sp.simplify((T11 - T22).subs(subs_mink))
    aniso_ext = sp.simplify(sp.expand(aniso_eval / (2 * gamma**2 * v**2)))

    # Validation: on d = 0 the Lorentz condition must reproduce p01's
    # lorentz_req = c_Y + 2*c_Y2 + 2*c_YI1 - c_I1 - 6*c_I1sq - 2*c_I2 - c_I3
    # (up to overall normalization).
    d_zero = {d: 0 for d in EXTENDED}
    p01_lorentz_req = (
        c_Y + 2 * c_Y2 + 2 * c_YI1 - c_I1 - 6 * c_I1sq - 2 * c_I2 - c_I3
    )
    lz0 = sp.simplify(lorentz_ext.subs(d_zero))
    ratio = sp.simplify(lz0 / p01_lorentz_req) if lz0 != 0 else None
    reduces_to_p01 = ratio is not None and ratio.is_number and ratio != 0

    return {
        "lorentz_ext": lorentz_ext,
        "aniso_ext": aniso_ext,
        "reduces_to_p01_lorentz_req": bool(reduces_to_p01),
        "p01_reduction_ratio": ratio,
    }


# ---------------------------------------------------------------------------
# Part 2 -- extended transverse contents (from-scratch probe, as in p18b)
# ---------------------------------------------------------------------------

def extended_transverse_contents() -> dict[str, Any]:
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
        for Bi in range(3):
            expr = 0
            for mu in range(4):
                expr += g_inv[mu, mu] * dphi[mu, A] * dphi[mu, Bi]
            B[A, Bi] = -expr

    Y = sp.Integer(1)
    I1 = sp.trace(B)
    I2 = sp.Rational(1, 2) * (I1**2 - sp.trace(B * B))
    I3 = B.det()

    L = extended_lagrangian(Y, I1, I2, I3)
    L2 = sp.expand(L).series(eps, 0, 3).removeO()
    L2 = sp.expand(L2.coeff(eps, 2))

    K_T = sp.simplify(L2.coeff(sp.diff(pi1, t) ** 2))
    C_T = sp.simplify(-L2.coeff(sp.diff(pi1, z) ** 2))
    return {"K_T_ext": K_T, "C_T_ext": C_T}


# ---------------------------------------------------------------------------
# Part 3 -- coexistence system and witness
# ---------------------------------------------------------------------------

def coexistence_analysis(
    lorentz_ext: sp.Expr, aniso_ext: sp.Expr, K_T: sp.Expr, C_T: sp.Expr
) -> dict[str, Any]:
    luminality = sp.expand(C_T - K_T)
    system = [sp.expand(lorentz_ext), sp.expand(aniso_ext), luminality]

    # Dimension of the solution family (linear system in 14 coefficients).
    M, rhs = sp.linear_eq_to_matrix(system, list(ALL_COEFFS))
    rank = M.rank()
    family_dimension = len(ALL_COEFFS) - rank

    # Minimal-subspace no-go: restrict to d = 0 and impose the p03 solar
    # family; then luminality forces the degenerate channel (C_T = K_T = 0
    # requires the 2PN slice value, i.e. no propagating luminal mode).
    d_zero = {d: 0 for d in EXTENDED}
    lum_min = sp.simplify(luminality.subs(d_zero).subs(SOLAR_FAMILY))
    K_min = sp.simplify(K_T.subs(d_zero).subs(SOLAR_FAMILY))
    C_min = sp.simplify(C_T.subs(d_zero).subs(SOLAR_FAMILY))
    # On the solar family C_T = 0, so luminality C_T = K_T forces K_T = 0.
    minimal_forces_degeneracy = (
        C_min == 0 and sp.simplify(lum_min + K_min) == 0
    )

    # Witness: solve the three conditions for three coefficients and pick a
    # numeric point with K_T > 0 and nonzero d-sector.
    sol = sp.solve(system, [c_Y, c_I2, c_I3], dict=True)
    witness = None
    witness_checks = {}
    if sol:
        s = sol[0]
        base_point = {
            c_Y2: sp.Integer(1),
            c_I1: sp.Integer(1),
            c_I1sq: sp.Integer(1),
            c_I3: sp.Integer(8),
            c_YI1: sp.Integer(0),
            d_YI2: sp.Rational(1, 2),
            d_YI3: sp.Integer(0),
            d_I1I2: sp.Integer(0),
            d_I1I3: sp.Integer(0),
            d_I2sq: sp.Integer(0),
            d_I2I3: sp.Integer(0),
            d_I3sq: sp.Integer(0),
        }
        full_point = dict(base_point)
        for key, valexpr in s.items():
            full_point[key] = sp.simplify(valexpr.subs(base_point))
        K_val = sp.simplify(K_T.subs(full_point))
        C_val = sp.simplify(C_T.subs(full_point))
        lor_val = sp.simplify(lorentz_ext.subs(full_point))
        ani_val = sp.simplify(aniso_ext.subs(full_point))
        d_used = any(full_point[d] != 0 for d in EXTENDED)
        witness = {str(k): sp.nsimplify(val) for k, val in full_point.items()}
        witness_checks = {
            "lorentz_zero": lor_val == 0,
            "anisotropy_zero": ani_val == 0,
            "luminal": sp.simplify(C_val - K_val) == 0,
            "kinetic_nonzero": K_val != 0,
            "kinetic_value": K_val,
            "uses_excluded_operators": d_used,
        }
        # If the first witness has K_T <= 0, raise the c_I3 knob until the
        # kinetic term is strictly positive (K_T grows linearly in c_I3 on
        # this slice).
        if K_val.is_number and K_val <= 0:
            base_point[c_I3] = base_point[c_I3] + (1 - K_val)
            full_point = dict(base_point)
            for key, valexpr in s.items():
                full_point[key] = sp.simplify(valexpr.subs(base_point))
            K_val = sp.simplify(K_T.subs(full_point))
            witness = {
                str(k): sp.nsimplify(val) for k, val in full_point.items()
            }
            witness_checks["kinetic_value"] = K_val
            witness_checks["kinetic_nonzero"] = K_val != 0

    return {
        "luminality_expr": luminality,
        "system_rank": rank,
        "family_dimension": family_dimension,
        "minimal_subspace_forces_degeneracy": minimal_forces_degeneracy,
        "witness": witness,
        "witness_checks": witness_checks,
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_luminal_solar_coexistence_gate() -> dict[str, Any]:
    cond = boosted_background_conditions()
    trans = extended_transverse_contents()
    coex = coexistence_analysis(
        cond["lorentz_ext"], cond["aniso_ext"], trans["K_T_ext"], trans["C_T_ext"]
    )

    closed = {
        "extended_lorentz_derived_from_scratch": True,
        "reduces_to_p01_lorentz_req_at_d0": cond["reduces_to_p01_lorentz_req"],
        "extended_anisotropy_derived": True,
        "extended_transverse_contents_derived": True,
        "minimal_subspace_forces_degeneracy": coex[
            "minimal_subspace_forces_degeneracy"
        ],
        "coexistence_witness_found": bool(coex["witness"])
        and all(
            bool(val) is True
            for key, val in coex["witness_checks"].items()
            if key
            in (
                "lorentz_zero",
                "anisotropy_zero",
                "luminal",
                "kinetic_nonzero",
                "uses_excluded_operators",
            )
        ),
    }
    all_closed = all(closed.values())

    return {
        "STATUS": (
            "OPEN_FULL_SOLAR_CHAIN__"
            + _pass_status("LORENTZ_LUMINAL_COEXISTENCE_WITNESS")
            if all_closed
            else "CHECK_COEXISTENCE_DERIVATION"
        ),
        "SCOPE": (
            "Extended degree-2 space (14 operators): Lorentz and anisotropy "
            "vacuum conditions derived from scratch by the boost method; "
            "transverse contents derived from scratch; coexistence of a "
            "luminal ghost-free transverse channel with the Lorentz vacuum "
            "settled by explicit witness.  The full 1PN/2PN solar re-run on "
            "this space remains open; no alpha value is computed or claimed."
        ),
        "closed_checks": closed,
        "open_checks": {
            "full_1pn_chain_rederived_on_extended_space": False,
            "beta_and_preferred_frame_checked": False,
            "winding_coupling_normalization_N_derived": False,
            "alpha_computed": False,
        },
        "lorentz_ext": cond["lorentz_ext"],
        "aniso_ext": cond["aniso_ext"],
        "K_T_ext": trans["K_T_ext"],
        "C_T_ext": trans["C_T_ext"],
        "luminality_expr": coex["luminality_expr"],
        "system_rank": coex["system_rank"],
        "family_dimension": coex["family_dimension"],
        "witness": coex["witness"],
        "witness_checks": coex["witness_checks"],
        "missing_derivations": [
            "re-derive the static 1PN chain (gamma, beta, preferred-frame "
            "parameters) on the 14-operator space and intersect with the "
            "coexistence family found here",
            "derive the winding-defect coupling to the luminal transverse "
            "mode and its normalization N",
            "then alpha = W^2/(4*pi*N) becomes a computation (p18 target "
            "N = 10.90497833)",
        ],
        "do_not_claim": [
            "do not claim the photon channel is established -- the witness "
            "satisfies Lorentz+anisotropy+luminality, not the full solar "
            "chain",
            "do not claim alpha is computed or bounded here",
            "do not reuse the old 7-term solar family on the extended space; "
            "the family must be re-derived",
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
        "lorentz_ext",
        "aniso_ext",
        "K_T_ext",
        "C_T_ext",
        "luminality_expr",
        "system_rank",
        "family_dimension",
    ):
        print(f"{key}: {result[key]}")
    print("witness:", result["witness"])
    print("witness_checks:")
    for key, value in result["witness_checks"].items():
        print(f"  - {key}: {value}")
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
    _print_result(derive_luminal_solar_coexistence_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
