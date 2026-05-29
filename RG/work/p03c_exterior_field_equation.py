# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: c_Y denotes the Y-scheme coefficient c_Y^(Y).

"""
p03c_exterior_field_equation.py

Static-spherical exterior diagnostic for the q_2PN / "three incompatible
exteriors" / refractive-axis question.

WHY THIS FILE EXISTS
--------------------
The central open issue of the RefG paper was the 2PN exterior optical
coefficient q_2PN, with several incompatible values floating around:

    q_2PN = 7/4   GR / Schwarzschild (isotropic)
    q_2PN = 2     bi-conformal "refractive" index n = exp(-phi)  (the title axis)
    q_2PN = 10    p03 minimal isotropic "stress-free" closure  (b_2 = 18)
    q_2PN = 11/4  lambda_S -> infinity strict S=6 limit

p03b_s6_exterior_scale.py gives a *scale argument* for the S=6 completion:
the completion's local 2PN stress is suppressed by Lambda*R_sun^2 ~ 1e-35.
That strongly supports Solar-GR compatibility, but it is not a finished
exterior ODE.

This file tests the physical exterior equation

    M_Pl^2 * G^mu_nu = T^RefG^mu_nu          (kappa = 1/M_Pl^2)

in a restricted areal static-spherical power ansatz, on the p03 1PN closure
branch, order by order in U = r_s/r, through 2PN.

IMPORTANT CAVEAT
----------------
The 2PN "solution" returned by the restricted constant-coefficient ansatz is

    a2 = 1 + 4*c_Y2*kappa*r^2,
    b2 =   - 4*c_Y2*kappa*r^2.

Because a2 and b2 depend on r, this is NOT a self-consistent solution of the
original constant-coefficient ansatz. If the correction is radial, its
derivatives must be included from the beginning. Therefore this file is a
diagnostic/obstruction ledger, not a closed 2PN exterior proof.

WHAT SURVIVES
-------------
1PN: The O(U) tt-equation supports a1=1 on the generic nondegenerate branch,
     consistent with the p03 1PN GR branch.  The degenerate combination
     2*c_Y2+c_YI1=0 must not be hidden; p03 remains the stronger 1PN ledger.

2PN: The tt/rr diagnostic points to a Lambda-scale radial correction, but the
     restricted ansatz is incomplete and the angular equation still has a
     residual.  A proper augmented ansatz or full ODE is required.

PHYSICAL READING (the key point)
--------------------------------
The SAME c_Y2 that fixes the cosmological dark-energy density in p02c
(M_*^4 * 16/25 = rho_DE) sets this correction amplitude.  Therefore

    (c_Y2 / M_Pl^2) * r^2  ~  Lambda * r^2  ~  1e-35   at the Solar radius.

So the Solar-GR-compatible q_2PN = 7/4 target remains supported at the
~1e-35 scale.
This is consistent with the p03b scale argument, but it does not replace the
full exterior ODE.

Scale consequence: the smallness of the dark-energy scale strongly suppresses an
observable refractive/2PN deviation in the Solar System.  An O(1) Solar
deviation (e.g. the q=2 refractive value) would need c_Y2 ~ O(M_Pl^2), which
would make dark energy enormous -- excluded.

CLARIFICATION OF q_2PN = 10
---------------------------
p03's isotropic_2pn_stress_closure required the medium stress itself to vanish,
T^t_t = T^i_i = 0 through O(u^2), which gave b_2 = 18 (q = 10).  That is NOT the
physical exterior condition.  The physical exterior solves G = kappa*T with the
medium stress PRESENT and kappa-suppressed.  Solving the correct equation gives
GR + O(kappa*c_Y2*r^2).  This supports the view that q = 10 is a diagnostic
artifact of imposing exact stress-freeness, but p03c alone does not prove the
full physical 2PN exterior.

REFRACTIVE AXIS VERDICT
-----------------------
The literal refractive index n = exp(-phi) (the bi-conformal exponential metric,
q_2PN = 2) is not selected by this restricted 2PN diagnostic.  It remains a
1PN-accurate ansatz unless a full exterior branch derives it.

HONEST OPEN ITEM (localized)
----------------------------
The simple r_s/r power series does not close all three components: the angular
equation leaves a residual proportional to (2*c_Y2 + c_YI1)*kappa*r_s^2, and
the tt/rr coefficients become r-dependent.  These are warning signs that the
constant-coefficient ansatz is too narrow.  The full 2PN exterior needs an
augmented radial ansatz or a genuine ODE solve.

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
  spherical branch OPEN.  This file supports the generic 1PN branch and exposes
  why the restricted 2PN ansatz is not enough.

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
    Restricted diagnostic for G = kappa*T on the 1PN closure branch.

    The 1PN tt-equation supports a1 = 1 on the generic nondegenerate branch.
    The 2PN tt+rr equations return r-dependent "coefficients"; this is useful
    as a diagnostic for the missing radial/Lambda-like response, but it is not
    a self-consistent constant-coefficient 2PN solution.
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
    r_dependent_coefficients = (
        (a2_value is not None and a2_value.has(r))
        or (b2_value is not None and b2_value.has(r))
    )
    ansatz_status = (
        "FAIL_AS_CONSTANT_COEFFICIENT_2PN_SOLUTION__DIAGNOSTIC_ONLY"
        if r_dependent_coefficients
        else "PASS_CONSTANT_COEFFICIENT_ANSATZ"
    )
    one_pn_degeneracy_warning = (
        "O(U) tt equation is proportional to (a1-1)*(2*c_Y2+c_YI1); "
        "it supports a1=1 generically but is degenerate if 2*c_Y2+c_YI1=0."
    )

    return {
        "status": "DIAGNOSTIC_RESTRICTED_ANSATZ_NOT_A_CLOSED_2PN_EXTERIOR",
        "background_stress_free_on_branch": background_ok,
        "one_pn_tt_equation": e1_tt,
        "a1_value": a1_value,
        "gamma_reading": "a1 = 1 on the generic branch; p03 remains the main 1PN closure ledger",
        "one_pn_degeneracy_warning": one_pn_degeneracy_warning,
        "two_pn_tt_equation": e2_tt,
        "two_pn_rr_equation": e2_rr,
        "two_pn_thth_equation": e2_th,
        "a2_value": a2_value,
        "b2_value": b2_value,
        "r_dependent_2pn_coefficients": r_dependent_coefficients,
        "ansatz_consistency_status": ansatz_status,
        "gr_schwarzschild_limit": {"a2": gr_limit_a2, "b2": gr_limit_b2},
        "gr_limit_recovers_schwarzschild": (gr_limit_a2 == 1 and gr_limit_b2 == 0),
        "areal_biconformal_residual_a2_plus_b2_minus_1": biconformal_areal,
        "medium_correction_amplitude": (
            "diagnostic radial scale c_Y2*kappa*r^2 = (c_Y2/M_Pl^2)*r^2 ~ Lambda*r^2"
        ),
        "thth_residual_localized_open_item": thth_residual,
        "thth_residual_reading": (
            "proportional to (2*c_Y2 + c_YI1)*kappa*r_s^2; together with the "
            "r-dependent tt/rr coefficients, this requires an augmented radial "
            "ansatz or full ODE before any 2PN exterior proof is claimed"
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
            "Supported physical Solar target from GR compatibility and p03b scale "
            "argument. p03c is consistent with a Lambda-scale radial correction, "
            "but does not by itself close the 2PN exterior."
        ),
        "q_2PN = 2": (
            "Bi-conformal exponential refractive index n=exp(-phi). Not selected "
            "by this restricted diagnostic; a 1PN-accurate ansatz unless a full "
            "exterior branch derives it."
        ),
        "q_2PN = 10": (
            "p03 minimal isotropic closure. Comes from imposing T=0 (medium "
            "stress vanishes), which is not the physical exterior condition. "
            "Likely diagnostic artifact, but final wording needs the full "
            "G=kappa*T exterior re-check."
        ),
        "q_2PN = 11/4": (
            "lambda_S -> infinity strict S=6 limit; unphysical for dark-energy "
            "calibration."
        ),
        "decisive_point": (
            "the physical exterior equation should be G=kappa*T, not T=0. "
            "The restricted p03c ansatz diagnoses the scale of the correction, "
            "but the full radial ODE is still open."
        ),
    }


def refractive_axis_verdict() -> dict[str, Any]:
    """Strategic verdict on whether 'refractive' is a distinguishing axis."""
    return {
        "verdict": "NO_SOLAR_REFRACTIVE_DISTINGUISHER_FROM_THIS_DIAGNOSTIC",
        "reason": (
            "the restricted diagnostic and p03b scale argument point to "
            "Lambda-scale local corrections, ~1e-35 at the Sun. This supports "
            "Solar GR-compatibility but is not a closed no-go theorem for every "
            "possible refractive exterior branch."
        ),
        "where_refractive_coupling_acts_at_O1": "cosmology (dark energy), via c_Y2",
        "title_status": (
            "'Refractive Gravity' is the physical picture/motivation; the literal "
            "Pi_eff->n_eff exterior mapping still requires the p13 bridge and the "
            "full exterior ODE"
        ),
        "distinguishing_content_must_come_from": [
            "cosmology: the effective-Lambda / dark-energy sector where c_Y2 acts at O(1)",
            "galactic MOND vortex sector (p07) -- still resting on two underived postulates",
        ],
        "p13_role": (
            "p13_refractive_force.py remains a correct map and one real no-go; it "
            "does not by itself create a Solar distinguishing axis"
        ),
    }


def exterior_claim_gate() -> list[ClaimGate]:
    return [
        ClaimGate(
            claim="1PN generic branch supports gamma=1",
            status="GENERIC_SUPPORTS_P03_1PN_BRANCH",
            verified_here=(
                "O(U) tt-equation is proportional to (a1-1)*(2*c_Y2+c_YI1), "
                "so it supports a1=1 on the generic nondegenerate branch."
            ),
            open_requirement=(
                "keep p03 as the main 1PN closure proof; handle the degenerate "
                "2*c_Y2+c_YI1=0 branch explicitly if it is used."
            ),
        ),
        ClaimGate(
            claim="2PN exterior = GR + (c_Y2/M_Pl^2)*r^2 medium correction",
            status="DIAGNOSTIC_ONLY_R_DEPENDENT_COEFFICIENTS",
            verified_here=(
                "tt/rr equations return a2=1+4*c_Y2*kappa*r^2 and "
                "b2=-4*c_Y2*kappa*r^2; their r-dependence invalidates the "
                "constant-coefficient ansatz as a closed solution."
            ),
            open_requirement=(
                "redo with radial 2PN functions, de-Sitter/Lambda-like terms, "
                "or a full static-spherical ODE solve."
            ),
        ),
        ClaimGate(
            claim="Solar q_2PN=7/4 target is supported at the physical scale",
            status="SUPPORTED_BY_SCALE_DIAGNOSTIC_NOT_PROVED_HERE",
            verified_here="diagnostic correction scale = c_Y2/M_Pl^2 ~ Lambda; Lambda*R_sun^2 ~ 1e-35.",
            open_requirement="full airtight exterior ODE for a rigorous 2PN statement.",
        ),
        ClaimGate(
            claim="q_2PN=10 is an artifact of imposing T=0",
            status="PLAUSIBLE_DIAGNOSTIC_NOT_FINAL",
            verified_here="p03's q=10 came from requiring medium stress to vanish; p03c suggests this is not the physical condition.",
            open_requirement="derive the full G=kappa*T exterior and then reclassify q=10.",
        ),
        ClaimGate(
            claim="Refractive is not a distinguishing Solar axis",
            status="NO_DISTINGUISHER_FROM_THIS_RESTRICTED_SOLAR_DIAGNOSTIC",
            verified_here="dark-energy-scale c_Y2 gives only Lambda*R_sun^2 suppression in this diagnostic.",
            open_requirement="finish the refractive bridge and full exterior ODE before making a final Solar no-go claim.",
        ),
    ]


def do_not_claim() -> list[str]:
    return [
        "Do not claim a fully airtight 2PN exterior; the angular residual is not yet absorbed.",
        "Do not claim p03c is a direct 2PN solution; its 2PN coefficients depend on r inside a constant-coefficient ansatz.",
        "Do not claim q_2PN=10 as a Solar prediction; the supported Solar target is q=7/4 by the scale argument.",
        "Do not claim the literal refractive index n=exp(-phi) is the physical 2PN metric.",
        "Do not claim a final Solar refractive no-go from this restricted diagnostic alone.",
        "Do not import this as a new article result until the augmented-ansatz airtight ODE is closed.",
        "Do not treat the q=10-artifact clarification as final before the independent isotropic G=kappa*T re-check.",
    ]


def module_status() -> dict[str, Any]:
    return {
        "file": "p03c_exterior_field_equation.py",
        "export_status": "WORK_LEDGER_DIAGNOSTIC_ONLY_NOT_ARTICLE_READY",
        "exterior_solution": solve_exterior_field_equation(),
        "lambda_scale_estimate": lambda_scale_suppression_estimate(),
        "q2pn_ledger": q2pn_branch_ledger(),
        "refractive_verdict": refractive_axis_verdict(),
        "claim_gate": exterior_claim_gate(),
        "do_not_claim": do_not_claim(),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("p03c: restricted static-spherical exterior diagnostic  G = kappa*T")
    print("=" * 72)

    result = solve_exterior_field_equation()
    print("\n1. Restricted field-equation diagnostic")
    print("  status:", result["status"])
    print("  background stress-free on branch:", result["background_stress_free_on_branch"])
    print("  O(U) tt-equation:", result["one_pn_tt_equation"])
    print("  a1 =", result["a1_value"], " ->", result["gamma_reading"])
    print("  1PN warning:", result["one_pn_degeneracy_warning"])
    print("  a2 =", result["a2_value"])
    print("  b2 =", result["b2_value"])
    print("  r-dependent 2PN coefficients:", result["r_dependent_2pn_coefficients"])
    print("  ansatz consistency:", result["ansatz_consistency_status"])
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
    print("  O(1) coupling candidate acts in:", verdict["where_refractive_coupling_acts_at_O1"])

    print("\n5. Claim gate")
    for gate in exterior_claim_gate():
        print(f"  - [{gate.status}] {gate.claim}")

    print("\n6. Do not claim")
    for item in do_not_claim():
        print(f"  - {item}")
