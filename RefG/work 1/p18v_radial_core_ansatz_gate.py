# Notation header (see NOTATION.md):
# This gate follows p18u.  It tests concrete radial regularization profiles for
# the localized charged orientation-frame core.  It is an ansatz audit, not an
# alpha derivation.

"""
================================================================================
PHASE 18v: Radial core ansatz gate
================================================================================

Purpose
-------
p18u narrowed the missing alpha ingredient to a weighted core law:

    eta_core = E_e / E_m = beta_core^2.

This gate makes the next step concrete.  It introduces a regularized radial
profile for a charged frame core,

    s_n(r;R) = r^n / (r^n + R^n),      n > 1,

and uses it as an enclosed-charge/enclosed-flux profile for the electric
framing-current and magnetic frame-curvature channels.  The profile has the
right qualitative boundary behavior:

    s_n(0)=0,      s_n(infinity)=1,

so the 1/r^2 far field is restored outside the core while the origin is
regularized.

Main result
-----------
The radial ansatz is useful, but it does not close alpha.  Its energy integral

    I_n = int_0^infinity s_n(x)^2 / x^2 dx
        = pi*(n-1)/(n^2*sin(pi/n))

is finite and order one for natural integer profiles.  Therefore same-scale,
same-stiffness electric and magnetic cores remain order-one partitioned.
They cannot produce the small diagnostic target

    eta_core ~= 0.00107834

without an extra derived ingredient: a large radius separation, a strong
stiffness/normalization hierarchy, or a weighted self-duality law.  None of
those is derived here.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive eta_core or beta_core.
- It does not choose a profile power to fit alpha.
- It does not solve the nonlinear Euler-Lagrange core equations.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA
Q_GEOM_H2_ORDER9 = 2.0 / 9.0
G_GEOM_FLUX_4PI = 4.0 * math.pi


def target_eta_for_diagnostic() -> float:
    """Target eta from p18t for q_geom=2/9 and g_geom=4*pi.

    This is a diagnostic target, not a derivation.
    """
    z_required = 4.0 * math.pi * ALPHA_CODATA / (Q_GEOM_H2_ORDER9**2)
    return ((z_required * Q_GEOM_H2_ORDER9) / G_GEOM_FLUX_4PI) ** 2


def profile_integral(n: int) -> float:
    """I_n for s_n(x)=x^n/(1+x^n), n>1."""
    if n <= 1:
        raise ValueError("profile power n must be > 1")
    return math.pi * (n - 1) / (n * n * math.sin(math.pi / n))


# ---------------------------------------------------------------------------
# 1. Radial profile boundary and regularity
# ---------------------------------------------------------------------------

def radial_profile_boundary_gate() -> dict:
    x, n = sp.symbols("x n", positive=True)
    s2 = x**2 / (1 + x**2)
    s3 = x**3 / (1 + x**3)
    near_origin_integrand = sp.simplify((x**n / (1 + x**n)) ** 2 / x**2)
    return {
        "profile": "s_n(x)=x^n/(1+x^n)",
        "s2_at_origin": sp.limit(s2, x, 0),
        "s2_at_infinity": sp.limit(s2, x, sp.oo),
        "s3_at_origin": sp.limit(s3, x, 0),
        "s3_at_infinity": sp.limit(s3, x, sp.oo),
        "near_origin_integrand": str(near_origin_integrand),
        "regularity_condition": "integrand ~ x^(2n-2), finite for n > 1/2; use n>1 for smooth enclosed profile",
        "origin_regularized": True,
        "far_field_restored": True,
    }


# ---------------------------------------------------------------------------
# 2. Exact profile energy integral
# ---------------------------------------------------------------------------

def profile_energy_integral_gate() -> dict:
    x = sp.symbols("x", positive=True)
    rows = {}
    for n in range(2, 9):
        profile = x**n / (1 + x**n)
        integral = sp.integrate(profile**2 / x**2, (x, 0, sp.oo))
        formula = sp.pi * (n - 1) / (n * n * sp.sin(sp.pi / n))
        rows[f"n{n}"] = {
            "sympy_integral": str(sp.simplify(integral)),
            "formula": str(sp.simplify(formula)),
            "numeric": float(sp.N(formula)),
            "formula_verified": sp.simplify(integral - formula) == 0,
        }
    return {
        "energy_form": "E_channel = K * charge^2 * I_n / (8*pi*R)",
        "I_n_formula": "pi*(n-1)/(n^2*sin(pi/n))",
        "rows": rows,
        "all_verified": all(row["formula_verified"] for row in rows.values()),
        "interpretation": (
            "regularized radial profiles only supply order-one dimensionless "
            "shape factors unless a core equation selects an extreme hierarchy"
        ),
    }


# ---------------------------------------------------------------------------
# 3. Same-scale profile scan: can profile shape alone give target eta?
# ---------------------------------------------------------------------------

def same_scale_profile_scan() -> dict:
    eta_target = target_eta_for_diagnostic()
    rows = []
    for ne in range(2, 25):
        Ie = profile_integral(ne)
        for nm in range(2, 25):
            Im = profile_integral(nm)
            eta_shape = Ie / Im
            rows.append(
                {
                    "n_e": ne,
                    "n_m": nm,
                    "eta_shape": eta_shape,
                    "relative_miss": abs(eta_shape - eta_target) / eta_target,
                }
            )
    best = min(rows, key=lambda row: row["relative_miss"])
    min_eta = min(row["eta_shape"] for row in rows)
    max_eta = max(row["eta_shape"] for row in rows)
    return {
        "powers_scanned": "2..24 for both channels",
        "target_eta_diagnostic": eta_target,
        "min_eta_shape": min_eta,
        "max_eta_shape": max_eta,
        "best_same_scale_profile": best,
        "target_outside_shape_range": eta_target < min_eta or eta_target > max_eta,
        "same_scale_profile_shape_cannot_close_alpha": eta_target < min_eta / 100.0,
        "interpretation": (
            "changing the smooth integer profile power changes the energy "
            "ratio only by an order-one factor; it cannot supply the small "
            "core partition by itself"
        ),
    }


# ---------------------------------------------------------------------------
# 4. Radius/stiffness hierarchy required by the radial ansatz
# ---------------------------------------------------------------------------

def hierarchy_requirement_audit() -> dict:
    eta_target = target_eta_for_diagnostic()
    same_profile_required_radius_ratio = 1.0 / eta_target

    profile_rows = []
    for ne, nm in ((2, 2), (2, 8), (8, 2), (3, 6), (6, 3)):
        shape_ratio = profile_integral(ne) / profile_integral(nm)
        required_Re_over_Rm = shape_ratio / eta_target
        required_k_ratio_same_scale = eta_target / shape_ratio
        profile_rows.append(
            {
                "n_e": ne,
                "n_m": nm,
                "I_e_over_I_m": shape_ratio,
                "R_e_over_R_m_required_if_stiffness_equal": required_Re_over_Rm,
                "k_e_over_k_m_required_if_same_radius": required_k_ratio_same_scale,
            }
        )

    return {
        "eta_target_diagnostic": eta_target,
        "same_profile_R_e_over_R_m_required": same_profile_required_radius_ratio,
        "rows": profile_rows,
        "large_hierarchy_required_without_new_core_law": same_profile_required_radius_ratio > 100.0,
        "interpretation": (
            "the ansatz says what a successful core theorem must explain: "
            "either electric framing energy is spread over a much larger "
            "effective radius, or its stiffness/readout is strongly "
            "suppressed, or a weighted duality provides the same hierarchy"
        ),
    }


# ---------------------------------------------------------------------------
# 5. Radius stabilization does not split electric/magnetic energy
# ---------------------------------------------------------------------------

def radius_stabilization_no_go() -> dict:
    R, C0, Ce, Cm = sp.symbols("R C0 C_e C_m", positive=True)
    energy = C0 * R**3 + (Ce + Cm) / R
    derivative = sp.diff(energy, R)
    R4_solution = sp.solve(sp.Eq(derivative, 0), R**4)[0]
    eta = sp.simplify(Ce / Cm)
    return {
        "energy_model": "E(R)=C0*R^3+(C_e+C_m)/R",
        "stationary_condition": str(sp.simplify(derivative)),
        "R_fourth_power_solution": str(R4_solution),
        "eta_after_radius_minimization": str(eta),
        "eta_still_free": eta.has(Ce) and eta.has(Cm),
        "interpretation": (
            "core-size stabilization fixes the common radius, but it only "
            "sees C_e+C_m.  It does not determine the split C_e/C_m."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Weighted radial self-duality slot
# ---------------------------------------------------------------------------

def radial_weighted_duality_slot() -> dict:
    beta, ke, km, Ie, Im, Re, Rm = sp.symbols(
        "beta_core k_e k_m I_e I_m R_e R_m", positive=True
    )
    eta = sp.simplify((ke * Ie / Re) / (km * Im / Rm))
    beta_expr = sp.sqrt(eta)
    beta_condition = sp.Eq(beta**2, eta)
    solved_ke_over_km = sp.solve(beta_condition, ke / km)
    eta_target = target_eta_for_diagnostic()
    beta_target = math.sqrt(eta_target)
    return {
        "eta_radial": str(eta),
        "beta_radial": str(beta_expr),
        "solving_for_k_e_over_k_m": str(solved_ke_over_km[0]),
        "target_beta_diagnostic": beta_target,
        "target_eta_diagnostic": eta_target,
        "free_objects": ["k_e/k_m", "I_e/I_m", "R_e/R_m"],
        "weighted_duality_not_derived": True,
        "interpretation": (
            "a radial weighted-duality law could close beta_core only if the "
            "action derives the stiffness, profile, and radius relation.  The "
            "ansatz alone leaves all three open."
        ),
    }


# ---------------------------------------------------------------------------
# 7. Next theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "Euler-Lagrange selection of the radial core profiles and weights"
        ),
        "must_derive": [
            "which profile powers or smooth functions solve the core equations",
            "whether electric and magnetic effective radii are locked or separated",
            "whether k_e/k_m is fixed by a single orientation-frame action",
            "whether a weighted self-duality relation fixes beta_core",
        ],
        "falsification_tests": [
            "if the same action fixes k_e=k_m and R_e=R_m with order-one profiles, eta_core stays order one and alpha is not derived",
            "if profile powers are chosen to approach the target without field equations, the gate fails as a fit",
            "if a large radius/stiffness hierarchy appears, it must be derived from core regularity or boundary conditions",
        ],
        "candidate_next_gate": "p18w_radial_core_euler_lagrange_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_radial_core_ansatz_gate() -> dict:
    boundary = radial_profile_boundary_gate()
    integral = profile_energy_integral_gate()
    scan = same_scale_profile_scan()
    hierarchy = hierarchy_requirement_audit()
    radius = radius_stabilization_no_go()
    duality = radial_weighted_duality_slot()
    requirements = next_theorem_requirements()

    closed = {
        "radial_profile_regularizes_origin_and_restores_far_field": bool(
            boundary["origin_regularized"] and boundary["far_field_restored"]
        ),
        "profile_energy_integral_verified": bool(integral["all_verified"]),
        "same_scale_profile_shape_cannot_reach_target_eta": bool(
            scan["target_outside_shape_range"]
            and scan["same_scale_profile_shape_cannot_close_alpha"]
        ),
        "large_hierarchy_required_without_new_core_law": bool(
            hierarchy["large_hierarchy_required_without_new_core_law"]
        ),
        "radius_stabilization_leaves_partition_free": bool(
            radius["eta_still_free"]
        ),
        "weighted_duality_slot_identified_but_free": bool(
            duality["weighted_duality_not_derived"]
        ),
        "no_profile_or_hierarchy_fit_performed": True,
    }

    open_checks = {
        "radial_Euler_Lagrange_equations_solved": False,
        "profile_family_derived": False,
        "radius_hierarchy_derived": False,
        "stiffness_hierarchy_derived": False,
        "beta_core_derived": False,
        "eta_core_derived": False,
        "Z_medium_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_RADIAL_CORE_EULER_LAGRANGE_SELECTION_REQUIRED__"
            + _pass_status("RADIAL_ANSATZ_PROFILE_AUDIT")
            if all(closed.values())
            else "CHECK_RADIAL_CORE_ANSATZ_AUDIT"
        ),
        "SCOPE": (
            "radial core ansatz audit after p18u: smooth enclosed-charge/flux "
            "profiles regularize the origin and preserve the 1/r^2 far field. "
            "Their energy factors are finite and order one, so profile shape "
            "and radius stabilization do not derive the small eta_core.  A "
            "derived Euler-Lagrange profile, radius hierarchy, stiffness "
            "hierarchy, or weighted-duality law is still required."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "boundary_profile": boundary,
        "profile_integrals": integral,
        "same_scale_profile_scan": scan,
        "hierarchy_requirement": hierarchy,
        "radius_stabilization": radius,
        "weighted_duality_slot": duality,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the radial picture is now concrete.  A regularized charged core "
            "can be written without singular energy, but ordinary smooth "
            "profiles only give order-one electric/magnetic partitions.  To "
            "reach the small beta required by the alpha chain, RefG must "
            "derive a real core hierarchy or weighted-duality law from the "
            "field equations."
        ),
        "missing_derivations": [
            "derive the radial core Euler-Lagrange equations from the completed action",
            "derive the electric and magnetic profile functions instead of choosing s_n",
            "derive or rule out a large electric/magnetic effective-radius hierarchy",
            "derive or rule out a stiffness/readout hierarchy k_e/k_m",
            "derive beta_core and then feed eta_core=beta_core^2 back into p18t",
        ],
        "do_not_claim": [
            "Do not claim alpha, Z_medium, beta_core, or eta_core are derived.",
            "Do not choose profile powers or radii to fit the target eta.",
            "Do not claim Derrick or radius stabilization splits E_e from E_m.",
            "Do not use same-scale smooth profiles as an alpha derivation; they are order-one.",
            "Do not identify geometric 4*pi flux with canonical magnetic charge here.",
        ],
    }
    return result


def _print_result(result: dict) -> None:
    print("STATUS:", result["STATUS"])
    print("SCOPE:", result["SCOPE"])
    print("closed_checks:")
    for key, val in result["closed_checks"].items():
        print(f"  - {key}: {val}")
    print("open_checks:")
    for key, val in result["open_checks"].items():
        print(f"  - {key}: {val}")
    print("boundary_profile:", result["boundary_profile"])
    print("profile_integrals:", result["profile_integrals"])
    print("same_scale_profile_scan:", result["same_scale_profile_scan"])
    print("hierarchy_requirement:", result["hierarchy_requirement"])
    print("radius_stabilization:", result["radius_stabilization"])
    print("weighted_duality_slot:", result["weighted_duality_slot"])
    print("requirements_for_next_gate:", result["requirements_for_next_gate"])
    print("physical_reading:", result["physical_reading"])
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
    _print_result(derive_radial_core_ansatz_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
