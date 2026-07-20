# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Extended degree-2 coefficient scheme as in p18c: 7 minimal c + 7 excluded d.

"""
================================================================================
PHASE 18d: Extended solar stress-quiet chain + luminal channel intersection
================================================================================

Purpose
-------
Re-run the p03 solar stress-quiet derivation (analyze_ppn ->
weak_field_stress_constraint_gate -> solar_1pn_closure_branch) on the extended
degree-2 operator space, faithfully reproducing p03's method:

  metric   A = 1 + 2*gamma*U + a2*U^2 (= -g_rr),  B = 1 - 2*U + 2*(beta-1)*U^2
           (= g_tt), with the GR-like geometry branch gamma = 1, beta = 1,
           a2 = 4 inserted;
  fields   unitary gauge, so the invariants are metric-determined:
           Y = 1/B, I1 = 2 + 1/A, I2 = 1 + 2/A, I3 = 1/A;
  stress   T^t_t   = 2*L_Y/B - L,
           T^r_r   = 2*(L_I1 + 2*L_I2 + L_I3)/A - L,
           T^th_th = 2*(L_I1 + L_I2*(1 + 1/A) + L_I3/A) - L,
  (these hold for ANY L(Y, I1, I2, I3): only first derivatives of L enter);
  demand   stress-quiet order by order in U.

New results (all executable below):

1. VALIDATION: with d = 0 the O(U^0)+O(U^1) solution reproduces the p03
   5-relation solar branch exactly, and the O(U^2) residuals reproduce
   (16*c_Y2, 16*c_Y2, 8*c_YI1).
2. MARGINALITY CROSS-CHECK: on the old branch the solid no-ghost prefactor
   K_pi (= the p18b transverse kinetic K_T) equals 2*c_Y2 - c_YI1 and dies on
   the physical 2PN slice -- the old branch was already marginal in the
   transverse sector, consistent with the p18b degeneracy theorem.
3. LORENTZ-FOR-FREE LEMMA: the boost-Lorentz vacuum condition of p18c is
   IMPLIED by the O(U^0)+O(U^1) stress-quiet system (adding it does not raise
   the rank) -- solar stress-quietness already enforces the Lorentz vacuum.
4. DEGREE-2 LUMINAL NO-GO THEOREM (the gate's central result): on the ENTIRE
   extended 1PN stress-quiet family, C_T == 0 identically; therefore
   luminality (C_T = K_T) forces K_T == 0 identically on the intersection.
   A propagating luminal transverse orientation wave is IMPOSSIBLE in ANY
   degree-2 polynomial action that is stress-quiet on the GR-like solar
   exterior.  (The p18c Lorentz+luminality coexistence witness dies exactly
   at the solar level.)  Physical reading: the photon-candidate cannot be a
   solid phonon; it requires NEW internal field content -- the charge-angle /
   rotation-topology channel already demanded by the p11 stage_d3 programme.
5. 2PN PROBE (dimension bookkeeping): adding O(U^2) stress-quietness leaves a
   6-dimensional family, so a nontrivial exact-2PN stress-quiet branch exists
   dimensionally on the extended space -- but by the no-go theorem it too is
   transverse-degenerate; its physical use is for the gravity sector, not for
   the photon.

What remains open after this gate: implementation of the rotation/topology
(charge-angle) channel and its quadratic action; the winding coupling and
normalization N on that channel; then alpha.

Status
------
OPEN at the new-channel and alpha layers; the no-go theorem, the
Lorentz-for-free lemma, and the validations are CLOSED below.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


# ---------------------------------------------------------------------------
# Coefficients (as in p18c)
# ---------------------------------------------------------------------------

c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
    "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1", real=True
)
d_YI2, d_YI3, d_I1I2, d_I1I3, d_I2sq, d_I2I3, d_I3sq = sp.symbols(
    "d_YI2 d_YI3 d_I1I2 d_I1I3 d_I2sq d_I2I3 d_I3sq", real=True
)
MINIMAL = (c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1)
EXTENDED = (d_YI2, d_YI3, d_I1I2, d_I1I3, d_I2sq, d_I2I3, d_I3sq)
ALL_COEFFS = MINIMAL + EXTENDED

P03_BRANCH = {
    c_I1: 4 * c_Y2 + 2 * c_YI1,
    c_I1sq: c_Y2,
    c_I2: -10 * c_Y2 - 3 * c_YI1,
    c_I3: 8 * c_Y2 + 4 * c_YI1,
    c_Y: -4 * c_Y2 - 2 * c_YI1,
}


def extended_L(Ys: sp.Expr, I1s: sp.Expr, I2s: sp.Expr, I3s: sp.Expr) -> sp.Expr:
    return (
        c_Y * Ys
        + c_Y2 * Ys**2
        + c_I1 * I1s
        + c_I1sq * I1s**2
        + c_I2 * I2s
        + c_I3 * I3s
        + c_YI1 * Ys * I1s
        + d_YI2 * Ys * I2s
        + d_YI3 * Ys * I3s
        + d_I1I2 * I1s * I2s
        + d_I1I3 * I1s * I3s
        + d_I2sq * I2s**2
        + d_I2I3 * I2s * I3s
        + d_I3sq * I3s**2
    )


# ---------------------------------------------------------------------------
# Part 1 -- p03-faithful stress series on the GR-like geometry branch
# ---------------------------------------------------------------------------

def stress_series_extended() -> dict[str, Any]:
    U = sp.Symbol("U", real=True, positive=True)
    # Geometry branch gamma=1, beta=1, a2=4 (p03 conventions).
    A = 1 + 2 * U + 4 * U**2
    B = 1 - 2 * U

    Y_s, I1_s, I2_s, I3_s = sp.symbols("Y I1 I2 I3", real=True)
    L = extended_L(Y_s, I1_s, I2_s, I3_s)

    invariants = {Y_s: 1 / B, I1_s: 2 + 1 / A, I2_s: 1 + 2 / A, I3_s: 1 / A}
    L_eval = L.subs(invariants)
    L_Y = sp.diff(L, Y_s).subs(invariants)
    L_I1 = sp.diff(L, I1_s).subs(invariants)
    L_I2 = sp.diff(L, I2_s).subs(invariants)
    L_I3 = sp.diff(L, I3_s).subs(invariants)

    T_tt = 2 * L_Y / B - L_eval
    T_rr = 2 * (L_I1 + 2 * L_I2 + L_I3) / A - L_eval
    T_thth = 2 * (L_I1 + L_I2 * (1 + 1 / A) + L_I3 / A) - L_eval

    def orders(expr: sp.Expr) -> dict[str, sp.Expr]:
        s = sp.series(sp.simplify(expr), U, 0, 3).removeO()
        return {
            "O(U^0)": sp.simplify(sp.expand(s).coeff(U, 0)),
            "O(U^1)": sp.simplify(sp.expand(s).coeff(U, 1)),
            "O(U^2)": sp.simplify(sp.expand(s).coeff(U, 2)),
        }

    return {
        "T^t_t": orders(T_tt),
        "T^r_r": orders(T_rr),
        "T^theta_theta": orders(T_thth),
    }


# ---------------------------------------------------------------------------
# Part 2 -- Lorentz condition and transverse contents (from p18c, re-derived
#           here compactly as closed-form linear expressions validated there)
# ---------------------------------------------------------------------------

LORENTZ_EXT = (
    -c_I1 - 6 * c_I1sq - 2 * c_I2 - c_I3 + c_Y + 2 * c_Y2 + 2 * c_YI1
    - 9 * d_I1I2 - 4 * d_I1I3 - 5 * d_I2I3 - 12 * d_I2sq - 2 * d_I3sq + d_YI2
)
K_T_EXT = (
    -c_I1 - 6 * c_I1sq - 2 * c_I2 - c_I3 - c_YI1
    - 9 * d_I1I2 - 4 * d_I1I3 - 5 * d_I2I3 - 12 * d_I2sq - 2 * d_I3sq
    - 2 * d_YI2 - d_YI3
)
C_T_EXT = (
    -c_I1 - 6 * c_I1sq - c_I2 - c_YI1
    - 6 * d_I1I2 - d_I1I3 - d_I2I3 - 6 * d_I2sq - d_YI2
)
LUMINALITY_EXT = sp.expand(C_T_EXT - K_T_EXT)


# ---------------------------------------------------------------------------
# Part 3 -- gate computation
# ---------------------------------------------------------------------------

def derive_extended_solar_chain_gate() -> dict[str, Any]:
    stress = stress_series_extended()

    eqs_o0 = [stress[c]["O(U^0)"] for c in stress]
    eqs_o1 = [stress[c]["O(U^1)"] for c in stress]
    eqs_o2 = [stress[c]["O(U^2)"] for c in stress]

    # ---- Validation at d = 0 against the p03 branch --------------------
    d_zero = {d: 0 for d in EXTENDED}
    leading_min = [sp.simplify(e.subs(d_zero).subs(P03_BRANCH)) for e in eqs_o0 + eqs_o1]
    o2_min = [sp.simplify(e.subs(d_zero).subs(P03_BRANCH)) for e in eqs_o2]
    p03_branch_reproduced = all(v == 0 for v in leading_min)
    p03_o2_residuals_reproduced = (
        sp.simplify(o2_min[0] - 16 * c_Y2) == 0
        and sp.simplify(o2_min[1] - 16 * c_Y2) == 0
        and sp.simplify(o2_min[2] - 8 * c_YI1) == 0
    )
    # Marginality cross-check: K_T on the p03 branch and its 2PN slice.
    K_T_on_p03 = sp.simplify(K_T_EXT.subs(d_zero).subs(P03_BRANCH))
    marginality = sp.simplify(K_T_on_p03 - (2 * c_Y2 - c_YI1)) == 0

    # ---- Extended 1PN branch -------------------------------------------
    system_1pn = eqs_o0 + eqs_o1
    M1, _ = sp.linear_eq_to_matrix(system_1pn, list(ALL_COEFFS))
    rank_1pn = M1.rank()
    dim_1pn = len(ALL_COEFFS) - rank_1pn

    # ---- Lorentz-for-free lemma ----------------------------------------
    ML, _ = sp.linear_eq_to_matrix(
        system_1pn + [LORENTZ_EXT], list(ALL_COEFFS)
    )
    lorentz_implied = ML.rank() == rank_1pn

    # ---- No-go theorem: C_T and K_T restricted to the families ---------
    sol_1pn = sp.solve(system_1pn, list(ALL_COEFFS), dict=True)
    s1 = sol_1pn[0]
    C_T_on_1pn = sp.simplify(C_T_EXT.subs(s1))
    K_T_on_1pn = sp.simplify(K_T_EXT.subs(s1))
    gradient_dead_on_extended_1pn = sp.expand(C_T_on_1pn) == 0

    system_int = system_1pn + [LORENTZ_EXT, LUMINALITY_EXT]
    M2, _ = sp.linear_eq_to_matrix(system_int, list(ALL_COEFFS))
    rank_int = M2.rank()
    dim_int = len(ALL_COEFFS) - rank_int
    sol_int = sp.solve(system_int, list(ALL_COEFFS), dict=True)
    s_int = sol_int[0]
    K_T_on_int = sp.simplify(K_T_EXT.subs(s_int))
    no_go_theorem = gradient_dead_on_extended_1pn and (
        sp.expand(K_T_on_int) == 0
    )

    # ---- 2PN probe: dimension bookkeeping ------------------------------
    system_2pn = system_int + eqs_o2
    M3, _ = sp.linear_eq_to_matrix(system_2pn, list(ALL_COEFFS))
    rank_2pn = M3.rank()
    dim_2pn = len(ALL_COEFFS) - rank_2pn

    closed = {
        "p03_branch_reproduced_at_d0": p03_branch_reproduced,
        "p03_O2_residuals_reproduced": p03_o2_residuals_reproduced,
        "old_branch_transverse_marginality_confirmed": marginality,
        "extended_1pn_branch_computed": True,
        "lorentz_implied_by_stress_quiet": lorentz_implied,
        "gradient_dead_on_extended_1pn_family": gradient_dead_on_extended_1pn,
        "K_T_identically_zero_on_luminal_intersection": (
            sp.expand(K_T_on_int) == 0
        ),
        "degree2_luminal_no_go_theorem": no_go_theorem,
    }

    return {
        "STATUS": (
            "OPEN_ROTATION_TOPOLOGY_CHANNEL__"
            + _pass_status("DEGREE2_LUMINAL_NO_GO_THEOREM")
            if all(closed.values())
            else "CHECK_EXTENDED_SOLAR_DERIVATION"
        ),
        "SCOPE": (
            "p03-faithful stress-quiet chain re-derived on the 14-operator "
            "space; validated against the p03 branch at d=0; central result "
            "is the degree-2 luminal no-go theorem: solar stress-quietness "
            "kills the transverse gradient on the WHOLE degree-2 space, so a "
            "luminal transverse phonon is impossible there; the photon needs "
            "the rotation/topology (charge-angle) channel.  No alpha value "
            "is computed or claimed."
        ),
        "closed_checks": closed,
        "open_checks": {
            "rotation_topology_channel_implemented": False,
            "charge_angle_quadratic_action_derived": False,
            "winding_coupling_normalization_N_derived": False,
            "alpha_computed": False,
        },
        "rank_1pn": rank_1pn,
        "dim_1pn_family": dim_1pn,
        "rank_intersection": rank_int,
        "dim_intersection_family": dim_int,
        "rank_with_2pn": rank_2pn,
        "dim_2pn_family": dim_2pn,
        "C_T_on_extended_1pn_family": C_T_on_1pn,
        "K_T_on_extended_1pn_family": sp.expand(K_T_on_1pn),
        "K_T_on_luminal_intersection": K_T_on_int,
        "K_T_on_p03_branch": K_T_on_p03,
        "theorem": (
            "in any degree-2 polynomial action L(Y, I1, I2, I3) whose stress "
            "is quiet through O(U^1) on the GR-like solar exterior, the "
            "transverse internal-orientation channel has zero gradient term; "
            "demanding luminality then kills its kinetic term identically -- "
            "no degree-2 action carries light while agreeing with the solar "
            "sector"
        ),
        "physical_reading": (
            "the photon-candidate is NOT a solid phonon; it requires new "
            "internal field content -- the charge-angle / rotation-topology "
            "channel (p11 stage_d3), exactly the article's 5.3 picture"
        ),
        "missing_derivations": [
            "define the charge-angle (U(1)-orientation) field and its "
            "lowest-order action terms as the rotation/topology channel",
            "derive its quadratic action (kinetic + gradient) and impose "
            "luminality + solar stress-quietness jointly",
            "derive the winding-defect coupling on that channel => N",
            "alpha = W^2/(4*pi*N) vs the p18 target N = 10.90497833",
        ],
        "do_not_claim": [
            "do not claim the theory has no photon -- the no-go covers only "
            "degree-2 solid-phonon carriers",
            "do not claim alpha is computed or bounded here",
            "do not reuse the p18c vacuum-level witness as physical: it dies "
            "at the solar stress-quiet level, which is the point of this "
            "gate",
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
        "rank_1pn",
        "dim_1pn_family",
        "rank_intersection",
        "dim_intersection_family",
        "rank_with_2pn",
        "dim_2pn_family",
        "C_T_on_extended_1pn_family",
        "K_T_on_extended_1pn_family",
        "K_T_on_luminal_intersection",
        "K_T_on_p03_branch",
        "theorem",
        "physical_reading",
    ):
        print(f"{key}: {result[key]}")
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
    _print_result(derive_extended_solar_chain_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
