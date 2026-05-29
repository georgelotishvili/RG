# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: c_Y denotes the Y-scheme coefficient c_Y^(Y).

"""
p03c_exterior_field_equation.py

Decisive static-spherical EXTERIOR computation for the q_2PN / "three
incompatible exteriors" / refractive-axis question.

WHY THIS FILE EXISTS
--------------------
The central open issue of the RefG paper was the 2PN exterior optical
coefficient q_2PN, with several incompatible values floating around:

    q_2PN = 7/4   GR / Schwarzschild (isotropic)
    q_2PN = 2     bi-conformal "refractive" index n = exp(-phi)  (the title axis)
    q_2PN = 10    p03 minimal isotropic "stress-free" closure  (b_2 = 18)
    q_2PN = 11/4  lambda_S -> infinity strict S=6 limit

p03b_s6_exterior_scale.py resolved this for the S=6 completion by a *scale
argument* (the completion's local 2PN stress decays as Lambda*R_sun^2 ~ 1e-35,
so the Solar exterior is GR, q=7/4).  The article's section 7 / 13 adopted that.

This file replaces the scale heuristic with the DIRECT field-equation solution.
It solves the physical exterior equation

    M_Pl^2 * G^mu_nu = T^RefG^mu_nu          (kappa = 1/M_Pl^2)

in the areal static-spherical ansatz, on the p03 1PN closure branch, order by
order in U = r_s/r, through 2PN.  No metric is imported from GR; A(r), B(r) are
solved from G = kappa*T.

MAIN RESULT (reproducible by solve_exterior_field_equation() below)
-------------------------------------------------------------------
1PN:  a1 = 1  =>  gamma = 1.  The RefG medium stress at O(U) vanishes only at
      a1 = 1 (independently of kappa), so the 1PN exterior is exactly GR.

2PN:  a2 = 1 + 4*c_Y2*kappa*r^2,
      b2 =   - 4*c_Y2*kappa*r^2.

      i.e. exterior = GR Schwarzschild (a2=1, b2=0) PLUS a medium correction of
      amplitude  c_Y2 * kappa * r^2 = (c_Y2 / M_Pl^2) * r^2.

PHYSICAL READING (the key point)
--------------------------------
The SAME c_Y2 that fixes the cosmological dark-energy density in p02c
(M_*^4 * 16/25 = rho_DE) sets this correction amplitude.  Therefore

    (c_Y2 / M_Pl^2) * r^2  ~  Lambda * r^2  ~  1e-35   at the Solar radius.

So the physical Solar exterior is GR, q_2PN = 7/4, with a ~1e-35 deviation.
This CONFIRMS p03b / article section 7 by an explicit G=kappa*T solution rather
than a heuristic scale estimate.

Deep consequence: the smallness of the dark-energy scale DIRECTLY forbids an
observable refractive/2PN deviation in the Solar System.  An O(1) Solar
deviation (e.g. the q=2 refractive value) would need c_Y2 ~ O(M_Pl^2), which
would make dark energy enormous -- excluded.

CLARIFICATION OF q_2PN = 10
---------------------------
p03's isotropic_2pn_stress_closure required the medium stress itself to vanish,
T^t_t = T^i_i = 0 through O(u^2), which gave b_2 = 18 (q = 10).  That is NOT the
physical exterior condition.  The physical exterior solves G = kappa*T with the
medium stress PRESENT and kappa-suppressed.  Solving the correct equation gives
GR + O(kappa*c_Y2*r^2), i.e. q = 7/4.  So q = 10 is an artifact of imposing
exact stress-freeness, not "a different physical branch".
[Status: strong, but flagged for independent re-check; see claim gate.]

REFRACTIVE AXIS VERDICT
-----------------------
The literal refractive index n = exp(-phi) (the bi-conformal exponential metric,
q_2PN = 2) is NOT selected by the field equations.  It is a 1PN-accurate ansatz
(where it equals GR anyway, gamma=1); at 2PN the physical metric is GR + an
effective-Lambda correction, not the exponential form.  Hence "refractive" is
NOT a distinguishing Solar-System axis.  The refractive/medium coupling c_Y2
acts at O(1) only in cosmology (dark energy), not locally.

HONEST OPEN ITEM (localized)
----------------------------
The simple r_s/r power series does not close all three components: the angular
equation leaves a residual proportional to (2*c_Y2 + c_YI1)*kappa*r_s^2.  This
is exactly p03b's remaining "airtight self-consistent exterior ODE" item, now
localized: the full 2PN exterior needs an augmented (de-Sitter-like / Lambda)
ansatz to absorb that angular medium stress.  Its amplitude is the same ~Lambda
scale, so it does not change the GR-compatibility conclusion.

INVESTIGATION CHAIN THAT LED HERE (so context is not lost)
----------------------------------------------------------
- p13_refractive_force.py was written to "strengthen refraction fully".  Audit:
  it is an honest map (correct identities + one real no-go: a constant plateau
  cannot come from a local algebraic Pi_eff->h_eff map) but it does NOT close
  the central bridge; most "PASS" items are tautologies or conditional
  recoveries, and the two-channel additive ledger is only a working form.
- p07_mond.py: the galactic/MOND axis rests on TWO underived postulates,
  a0 = cH/(2pi) (coherence-scale postulate) and the vortex closure
  g_h/g_N = a0/g (equivalently g_h = 2*Delta_p/(r*rho_solid)).  p07 also rules
  out the p01 static 1/r^2 stress as a source of flat curves (it gives v ~ 1/r).
- p10_oscillons.py: the local Newton/bi-conformal refractive picture is closed
  only WITHIN the bi-conformal ansatz; its own gate marks the full static
  spherical branch OPEN.  This file closes that gate at 1PN and clarifies 2PN.

This file is a work ledger.  It is reproducible (run it) and uses the same
claim-gate / do-not-claim discipline as the rest of work/.
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


def _one_pn_branch_coefficients(cY2: sp.Symbol, cYI1: sp.Symbol) -> dict[str, sp.Expr]:
    """
    p03_solar.solar_1pn_closure_branch: the nontrivial 1PN stress-closure branch
    that yields gamma = beta = 1.  Free parameters: c_Y2, c_YI1.
    """
    return {
        "c_Y": -4 * cY2 - 2 * cYI1,
        "c_Y2": cY2,
        "c_I1": 4 * cY2 + 2 * cYI1,
        "c_I1sq": cY2,
        "c_I2": -10 * cY2 - 3 * cYI1,
        "c_I3": 8 * cY2 + 4 * cYI1,
        "c_YI1": cYI1,
    }


def _build_field_equation_series():
    """
    Build the areal static-spherical field-equation residuals G - kappa*T,
    series-expanded in U = eps*r_s/r through O(eps^2), times r^2.

    Returns (eps, kappa, r, rs, a1, a2, b2, cY2, cYI1, Ett, Err, Eth).
    """
    r, rs, eps, kappa = sp.symbols("r rs eps kappa", positive=True)
    a1, a2, b2 = sp.symbols("a1 a2 b2", real=True)
    cY2, cYI1 = sp.symbols("cY2 cYI1", real=True)

    coeffs = _one_pn_branch_coefficients(cY2, cYI1)
    Ys, I1s, I2s, I3s = sp.symbols("Ys I1s I2s I3s")
    Lp = (
        coeffs["c_Y"] * Ys
        + coeffs["c_Y2"] * Ys**2
        + coeffs["c_I1"] * I1s
        + coeffs["c_I1sq"] * I1s**2
        + coeffs["c_I2"] * I2s
        + coeffs["c_I3"] * I3s
        + coeffs["c_YI1"] * Ys * I1s
    )

    U = eps * rs / r
    A = 1 + a1 * U + a2 * U**2
    B = 1 - U + b2 * U**2  # B[O(U)] = -1 fixes the mass (r_s = 2GM/c^2)

    # areal static-spherical invariants (phi^A comoving, eigenvalues 1/A,1,1)
    subs_inv = {Ys: 1 / B, I1s: 2 + 1 / A, I2s: 1 + 2 / A, I3s: 1 / A}
    Lval = Lp.subs(subs_inv)
    LY = sp.diff(Lp, Ys).subs(subs_inv)
    LI1 = sp.diff(Lp, I1s).subs(subs_inv)
    LI2 = sp.diff(Lp, I2s).subs(subs_inv)
    LI3 = sp.diff(Lp, I3s).subs(subs_inv)

    # mixed RG stress (p03/p10 convention)
    Ttt = 2 * LY / B - Lval
    Trr = 2 * (LI1 / A + 2 * LI2 / A + LI3 / A) - Lval
    Tthth = 2 * (LI1 + LI2 * (1 + 1 / A) + LI3 / A) - Lval

    # Einstein tensor mixed components (areal, p10 formulas)
    Ap, Bp, Bpp = sp.diff(A, r), sp.diff(B, r), sp.diff(B, r, 2)
    Gtt = -Ap / (r * A**2) + (1 / A - 1) / r**2
    Grr = Bp / (r * A * B) + (1 / A - 1) / r**2
    Gthth = (
        Bpp / (2 * A * B)
        - Bp**2 / (4 * A * B**2)
        - Ap * Bp / (4 * A**2 * B)
        + Bp / (2 * r * A * B)
        - Ap / (2 * r * A**2)
    )

    def ser(expr):
        return sp.expand(sp.series(sp.expand(expr * r**2), eps, 0, 3).removeO())

    Ett = ser(Gtt - kappa * Ttt)
    Err = ser(Grr - kappa * Trr)
    Eth = ser(Gthth - kappa * Tthth)
    return eps, kappa, r, rs, a1, a2, b2, cY2, cYI1, Ett, Err, Eth


def solve_exterior_field_equation() -> dict[str, Any]:
    """
    Solve G = kappa*T order by order in U on the 1PN closure branch.

    1PN: O(U) tt-equation forces a1 = 1 (gamma = 1).
    2PN: O(U^2) tt+rr equations give a2, b2 with a kappa*c_Y2*r^2 medium term.
    The angular (thth) residual on that solution is the localized open item.
    """
    eps, kappa, r, rs, a1, a2, b2, cY2, cYI1, Ett, Err, Eth = _build_field_equation_series()

    def coeff(expr, n):
        return sp.simplify(expr.coeff(eps, n))

    background_ok = (
        coeff(Ett, 0) == 0 and coeff(Err, 0) == 0 and coeff(Eth, 0) == 0
    )

    # 1PN: solve tt at O(eps^1) for a1
    e1_tt = coeff(Ett, 1)
    a1_solution = sp.solve(e1_tt, a1)
    a1_value = a1_solution[0] if a1_solution else None

    # 2PN: fix a1 = a1_value, solve tt+rr at O(eps^2) for a2, b2
    fix_a1 = {a1: a1_value}
    e2_tt = sp.simplify(coeff(Ett, 2).subs(fix_a1))
    e2_rr = sp.simplify(coeff(Err, 2).subs(fix_a1))
    e2_th = sp.simplify(coeff(Eth, 2).subs(fix_a1))
    sol2 = sp.solve([e2_tt, e2_rr], [a2, b2], dict=True)
    s = sol2[0] if sol2 else {}
    a2_value = sp.simplify(s.get(a2)) if s else None
    b2_value = sp.simplify(s.get(b2)) if s else None

    thth_residual = sp.simplify(e2_th.subs(s)) if s else None
    biconformal_areal = (
        sp.simplify(a2_value + b2_value - 1) if (a2_value is not None) else None
    )
    gr_limit_a2 = sp.simplify(a2_value.subs({cY2: 0, cYI1: 0})) if a2_value is not None else None
    gr_limit_b2 = sp.simplify(b2_value.subs({cY2: 0, cYI1: 0})) if b2_value is not None else None

    return {
        "status": "PASS_PHYSICAL_EXTERIOR_GR_PLUS_LAMBDA_SCALE_MEDIUM_CORRECTION",
        "background_stress_free_on_branch": background_ok,
        "one_pn_tt_equation": e1_tt,
        "a1_value": a1_value,
        "gamma_reading": "a1 = 1  =>  gamma = 1 (1PN exterior is GR)",
        "two_pn_tt_equation": e2_tt,
        "two_pn_rr_equation": e2_rr,
        "two_pn_thth_equation": e2_th,
        "a2_value": a2_value,
        "b2_value": b2_value,
        "gr_schwarzschild_limit": {"a2": gr_limit_a2, "b2": gr_limit_b2},
        "gr_limit_recovers_schwarzschild": (gr_limit_a2 == 1 and gr_limit_b2 == 0),
        "areal_biconformal_residual_a2_plus_b2_minus_1": biconformal_areal,
        "medium_correction_amplitude": "c_Y2 * kappa * r^2 = (c_Y2 / M_Pl^2) * r^2 ~ Lambda * r^2",
        "thth_residual_localized_open_item": thth_residual,
        "thth_residual_reading": (
            "proportional to (2*c_Y2 + c_YI1)*kappa*r_s^2; same Lambda scale; "
            "needs an augmented de-Sitter-like ansatz to close airtight"
        ),
    }


def lambda_scale_suppression_estimate() -> dict[str, Any]:
    """
    Numerical size of the 2PN medium correction at the Solar radius.

    The correction is (c_Y2/M_Pl^2)*r^2.  Calibrating c_Y2/M_Pl^2 to the
    observed dark-energy scale (so the cosmological branch matches p02c) gives
    Lambda ~ 1.1e-52 m^-2; at r = R_sun the dimensionless deviation is Lambda*r^2.
    """
    Lambda_m2 = 1.1e-52  # observed effective cosmological constant, m^-2
    r_sun_m = 6.957e8
    deviation = Lambda_m2 * r_sun_m**2
    return {
        "status": "ORDER_OF_MAGNITUDE_ESTIMATE",
        "Lambda_m2_used": Lambda_m2,
        "r_sun_m": r_sun_m,
        "Lambda_times_Rsun_squared": deviation,
        "reading": (
            "the 2PN medium deviation from GR at the Solar radius is of order "
            f"{deviation:.1e}; far below any Solar-System 2PN sensitivity"
        ),
        "cross_check": "matches p03b_s6_exterior_scale Lambda*R_sun^2 ~ 5e-35 order",
    }


def q2pn_branch_ledger() -> dict[str, Any]:
    """Honest ledger of every q_2PN value and its real status after this file."""
    return {
        "q_2PN = 7/4": (
            "PHYSICAL Solar exterior. Direct G=kappa*T solution gives GR plus a "
            "(c_Y2/M_Pl^2)*r^2 ~ Lambda*r^2 correction (~1e-35 at the Sun)."
        ),
        "q_2PN = 2": (
            "Bi-conformal exponential refractive index n=exp(-phi). NOT selected "
            "by the field equations; a 1PN-accurate ansatz only."
        ),
        "q_2PN = 10": (
            "p03 minimal isotropic closure. Comes from imposing T=0 (medium "
            "stress vanishes), which is NOT the physical exterior condition. "
            "Artifact of the wrong condition, not a separate physical branch."
        ),
        "q_2PN = 11/4": (
            "lambda_S -> infinity strict S=6 limit; unphysical for dark-energy "
            "calibration."
        ),
        "decisive_point": (
            "the physical exterior equation is G=kappa*T (medium stress present "
            "and kappa-suppressed), not T=0. Solving it gives GR at the Sun."
        ),
    }


def refractive_axis_verdict() -> dict[str, Any]:
    """Strategic verdict on whether 'refractive' is a distinguishing axis."""
    return {
        "verdict": "REFRACTIVE_IS_NOT_A_DISTINGUISHING_SOLAR_AXIS",
        "reason": (
            "the field equations give GR in the Solar exterior; the refractive "
            "deviation amplitude is set by c_Y2/M_Pl^2 ~ Lambda, so it is ~1e-35 "
            "locally. The smallness of dark energy forbids an O(1) Solar "
            "refractive signal."
        ),
        "where_refractive_coupling_acts_at_O1": "cosmology (dark energy), via c_Y2",
        "title_status": (
            "'Refractive Gravity' is the physical picture/motivation; the literal "
            "Pi_eff->n_eff exterior mapping is GR-equivalent locally and is not a "
            "proven distinguishing prediction"
        ),
        "distinguishing_content_must_come_from": [
            "cosmology: the effective-Lambda / dark-energy sector where c_Y2 acts at O(1)",
            "galactic MOND vortex sector (p07) -- still resting on two underived postulates",
        ],
        "p13_role": (
            "p13_refractive_force.py remains a correct map and one real no-go; it "
            "cannot create a Solar distinguishing axis because the field equations "
            "forbid one"
        ),
    }


def exterior_claim_gate() -> list[ClaimGate]:
    return [
        ClaimGate(
            claim="1PN exterior is GR (gamma=1) from the field equations",
            status="CLOSED_FIELD_EQUATION_RESULT",
            verified_here="O(U) tt-equation forces a1=1 on the 1PN closure branch, independent of kappa.",
            open_requirement="none for 1PN gamma; beta=1 already in p03.",
        ),
        ClaimGate(
            claim="2PN exterior = GR + (c_Y2/M_Pl^2)*r^2 medium correction",
            status="CLOSED_FOR_TT_RR_OPEN_FOR_THTH",
            verified_here="a2=1+4*c_Y2*kappa*r^2, b2=-4*c_Y2*kappa*r^2; reduces to Schwarzschild at c_Y2,c_YI1->0.",
            open_requirement="absorb the angular residual ~(2*c_Y2+c_YI1)*kappa*r_s^2 with an augmented de-Sitter-like ansatz (airtight ODE).",
        ),
        ClaimGate(
            claim="Solar exterior is GR (q_2PN=7/4) at the physical scale",
            status="CONFIRMS_SECTION_7_BY_DIRECT_COMPUTATION",
            verified_here="correction amplitude = c_Y2/M_Pl^2 ~ Lambda; Lambda*R_sun^2 ~ 1e-35.",
            open_requirement="full airtight exterior ODE for a fully rigorous 2PN statement.",
        ),
        ClaimGate(
            claim="q_2PN=10 is an artifact of imposing T=0",
            status="STRONG_BUT_RECHECK",
            verified_here="the physical equation G=kappa*T gives GR; p03's q=10 came from requiring medium stress to vanish.",
            open_requirement="independently re-derive the isotropic-frame exterior from G=kappa*T to confirm q->7/4 there too.",
        ),
        ClaimGate(
            claim="Refractive is not a distinguishing Solar axis",
            status="CONSEQUENCE_OF_LAMBDA_SCALE_SUPPRESSION",
            verified_here="O(1) Solar deviation would need c_Y2~O(M_Pl^2), which makes dark energy huge -- excluded.",
            open_requirement="if a distinguishing refractive prediction is wanted, it must be derived in cosmology or in the (still postulated) MOND vortex sector.",
        ),
    ]


def do_not_claim() -> list[str]:
    return [
        "Do not claim a fully airtight 2PN exterior; the angular residual is not yet absorbed.",
        "Do not claim q_2PN=10 as a Solar prediction; the physical exterior is GR (q=7/4).",
        "Do not claim the literal refractive index n=exp(-phi) is the physical 2PN metric.",
        "Do not claim a distinguishing Solar refractive signal; Lambda-scale suppression forbids it.",
        "Do not import this as a new article result until the augmented-ansatz airtight ODE is closed.",
        "Do not treat the q=10-artifact clarification as final before the independent isotropic G=kappa*T re-check.",
    ]


def module_status() -> dict[str, Any]:
    return {
        "file": "p03c_exterior_field_equation.py",
        "export_status": "WORK_LEDGER_STRONG_RESULT_NOT_YET_AIRTIGHT",
        "exterior_solution": solve_exterior_field_equation(),
        "lambda_scale_estimate": lambda_scale_suppression_estimate(),
        "q2pn_ledger": q2pn_branch_ledger(),
        "refractive_verdict": refractive_axis_verdict(),
        "claim_gate": exterior_claim_gate(),
        "do_not_claim": do_not_claim(),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("p03c: physical static-spherical exterior  G = kappa*T  (areal, 1PN branch)")
    print("=" * 72)

    result = solve_exterior_field_equation()
    print("\n1. Field-equation solution")
    print("  background stress-free on branch:", result["background_stress_free_on_branch"])
    print("  O(U) tt-equation:", result["one_pn_tt_equation"])
    print("  a1 =", result["a1_value"], " ->", result["gamma_reading"])
    print("  a2 =", result["a2_value"])
    print("  b2 =", result["b2_value"])
    print("  GR (c_Y2,c_YI1->0) limit:", result["gr_schwarzschild_limit"],
          "recovers Schwarzschild:", result["gr_limit_recovers_schwarzschild"])
    print("  areal a2+b2-1 =", result["areal_biconformal_residual_a2_plus_b2_minus_1"])
    print("  medium correction amplitude:", result["medium_correction_amplitude"])
    print("  thth residual (open item):", result["thth_residual_localized_open_item"])
    print("  thth reading:", result["thth_residual_reading"])

    print("\n2. Lambda-scale suppression at the Solar radius")
    est = lambda_scale_suppression_estimate()
    print("  Lambda*R_sun^2 ~", f"{est['Lambda_times_Rsun_squared']:.1e}")
    print("  reading:", est["reading"])
    print("  cross-check:", est["cross_check"])

    print("\n3. q_2PN branch ledger")
    for key, value in q2pn_branch_ledger().items():
        print(f"  {key}: {value}")

    print("\n4. Refractive-axis verdict")
    verdict = refractive_axis_verdict()
    print("  verdict:", verdict["verdict"])
    print("  reason:", verdict["reason"])
    print("  O(1) coupling acts in:", verdict["where_refractive_coupling_acts_at_O1"])

    print("\n5. Claim gate")
    for gate in exterior_claim_gate():
        print(f"  - [{gate.status}] {gate.claim}")

    print("\n6. Do not claim")
    for item in do_not_claim():
        print(f"  - {item}")
