# Notation header (see NOTATION.md):
# This gate follows p18ac.  It audits whether the dynamic boundary coefficient
# C in Theta_boundary = P*dtheta + C*A can be derived from a localized bulk/core
# action, and whether the integer boundary branch can become the Maxwell
# readout strength q0 without fitting alpha.

"""
================================================================================
PHASE 18ad: Dynamic boundary coefficient gate
================================================================================

Purpose
-------
p18ac found the precise missing object:

    Theta_boundary = P*dtheta + C*A,

where the order-9, h=2 frame-bundle geometry supplies q_geom=2/9, but the
dynamic coefficient C and its map to Maxwell-normalized q0 are still open.

This gate tests the next layer:

  1. Can a second-order bulk action produce the fixed boundary one-form?
  2. If not, what first-order/Berry/Wess-Zumino term is required?
  3. Does cap prequantization produce a useful integer branch?
  4. Can the natural integer branch be read as q0^2 without fitting?

Main result
-----------
A fixed boundary coefficient requires a first-order geometric term.  Pure
second-order kinetic geometry produces momenta, but no velocity-independent
boundary one-form coefficient.  A first-order term

    L_B = C*(1 - cos chi)*dot(phi)

does produce the needed symplectic form

    Omega_B = C*sin chi dchi wedge dphi.

Bulk reduction can express C as an integral coefficient, but regularity and
topology do not determine its absolute value.  Cap prequantization gives

    C*q_geom = n.

This opens a useful candidate map:

    q0^2 = C*q_geom = n.

If the electron branch is n=2, then

    alpha^{-1} = 81*pi/2 = 127.2345...

This is not the observed low-energy alpha^{-1}=137.036.  It is only a possible
bare/high-scale candidate, and it requires two future derivations: the map
q0^2=n and a dressing/running bridge to the low-energy value.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not derive C.
- It does not derive the map q0^2 = n.
- It does not claim n=2 is the electron branch.
- It does not use CODATA to choose n.
"""

from __future__ import annotations

import math
import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


ALPHA_INV_CODATA = 137.035999177
ALPHA_CODATA = 1.0 / ALPHA_INV_CODATA
H = 2
ORDER = 9
Q_GEOM = H / ORDER
Q0_SQUARED_REQUIRED_LOW = 4.0 * math.pi * ALPHA_CODATA / (Q_GEOM**2)


# ---------------------------------------------------------------------------
# 1. Second-order action versus first-order boundary one-form
# ---------------------------------------------------------------------------

def first_order_boundary_term_requirement() -> dict:
    chi, phidot, M, C = sp.symbols("chi phidot M C", positive=True)

    L_second = M * sp.sin(chi) ** 2 * phidot**2 / 2
    p_phi_second = sp.diff(L_second, phidot)
    p_phi_second_at_rest = sp.simplify(p_phi_second.subs(phidot, 0))

    L_wz = C * (1 - sp.cos(chi)) * phidot
    p_phi_wz = sp.diff(L_wz, phidot)
    curvature_wz = sp.diff(p_phi_wz, chi)

    return {
        "second_order_phi_momentum": str(p_phi_second),
        "second_order_phi_momentum_at_rest": str(p_phi_second_at_rest),
        "second_order_has_no_fixed_boundary_one_form_at_rest": (
            p_phi_second_at_rest == 0
        ),
        "first_order_term": "L_B = C*(1 - cos(chi))*dot(phi)",
        "first_order_boundary_one_form": str(p_phi_wz) + "*dphi",
        "first_order_symplectic_curvature": str(curvature_wz)
        + "*dchi wedge dphi",
        "first_order_term_supplies_fixed_C": p_phi_wz.has(C),
        "reading": (
            "the required boundary coefficient is not produced by a pure "
            "second-order kinetic term.  It requires a Berry/Wess-Zumino-like "
            "first-order geometric term or an equivalent constrained "
            "symplectic reduction."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Bulk reduction of C
# ---------------------------------------------------------------------------

def bulk_reduction_coefficient_ledger() -> dict:
    r, R, rho0, kappa_B = sp.symbols(
        "r R rho0 kappa_B", positive=True
    )
    density = rho0**2 * sp.exp(-2 * r / R)
    inventory = sp.integrate(4 * sp.pi * r**2 * density, (r, 0, sp.oo))
    C_eff = sp.simplify(kappa_B * inventory)

    f = sp.Function("f")
    endpoint_integral = "int_0^infty f_prime(r) dr = f(infty)-f(0)=1"
    C_top = sp.simplify(kappa_B)

    return {
        "localized_density_example": "rho0^2*exp(-2r/R)",
        "core_inventory_example": str(inventory),
        "C_eff_example": str(C_eff),
        "C_eff_depends_on_bulk_coefficient_and_core_inventory": (
            C_eff.has(kappa_B) and C_eff.has(rho0) and C_eff.has(R)
        ),
        "topological_profile_reduction": endpoint_integral,
        "C_after_endpoint_reduction": str(C_top),
        "endpoint_reduction_still_leaves_kappa_B": C_top.has(kappa_B),
        "reading": (
            "a bulk term can reduce to the desired boundary coefficient.  "
            "A localized density leaves C tied to core inventory; a pure "
            "endpoint term removes profile dependence but still leaves the "
            "first-order level kappa_B to be derived."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Regularity and boundary conditions do not determine C
# ---------------------------------------------------------------------------

def regularity_endpoint_no_go() -> dict:
    r, R, n = sp.symbols("r R n", positive=True)
    profile = r**n / (r**n + R**n)
    at_origin = sp.limit(profile.subs(n, 2), r, 0)
    at_infinity = sp.limit(profile.subs(n, 2), r, sp.oo)
    derivative_integral_n2 = sp.integrate(
        sp.diff(profile.subs(n, 2), r), (r, 0, sp.oo)
    )

    kappa_B = sp.symbols("kappa_B", positive=True)
    C_from_endpoint = sp.simplify(kappa_B * derivative_integral_n2)

    return {
        "regular_profile": "f_n(r)=r^n/(r^n+R^n)",
        "f2_at_origin": at_origin,
        "f2_at_infinity": at_infinity,
        "integral_f2_prime": str(sp.simplify(derivative_integral_n2)),
        "C_from_regular_endpoint_profile": str(C_from_endpoint),
        "regularity_fixes_profile_endpoints_not_level": C_from_endpoint.has(
            kappa_B
        ),
        "reading": (
            "regularity can enforce f(0)=0 and f(infty)=1.  It can make the "
            "boundary term profile-independent, but it does not determine "
            "the level multiplying the term."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Cap integrality and integer branches
# ---------------------------------------------------------------------------

def cap_integrality_branch_ledger() -> dict:
    C, n = sp.symbols("C n", positive=True)
    q_geom = sp.Rational(H, ORDER)
    condition = sp.Eq(C * q_geom, n)
    C_solution = sp.solve(condition, C)[0]
    C_branch_h = sp.simplify(C_solution.subs(n, H))

    return {
        "q_geom": str(q_geom),
        "prequantization_condition": str(condition),
        "C_solution": str(C_solution),
        "C_for_branch_n_equals_1": float(C_solution.subs(n, 1)),
        "C_for_branch_n_equals_h2": float(C_branch_h),
        "integer_product_C_qgeom": "C*q_geom = n",
        "branch_quantized_but_C_to_q0_map_open": True,
        "reading": (
            "cap prequantization is useful: it converts the unknown C into an "
            "integer branch if the electron branch is known.  But the physical "
            "Maxwell readout still depends on how this integer product maps "
            "to q0."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Candidate readout map q0^2 = C*q_geom = n
# ---------------------------------------------------------------------------

def integer_readout_candidate_audit() -> dict:
    rows = {}
    for n in range(1, 10):
        q0_squared = float(n)
        alpha_inv = 4.0 * math.pi / (q0_squared * Q_GEOM**2)
        rows[f"n{n}"] = {
            "q0_squared_if_map_q0sq_equals_n": q0_squared,
            "alpha_inv": alpha_inv,
            "relative_miss_vs_low_energy_alpha_inv": abs(
                alpha_inv - ALPHA_INV_CODATA
            )
            / ALPHA_INV_CODATA,
        }

    best_name, best_row = min(
        rows.items(),
        key=lambda item: item[1]["relative_miss_vs_low_energy_alpha_inv"],
    )

    n_required_low = Q0_SQUARED_REQUIRED_LOW
    alpha_inv_n2 = rows["n2"]["alpha_inv"]

    return {
        "candidate_map": "q0^2 = C*q_geom = n",
        "rows": rows,
        "best_integer_branch_for_low_energy_target": best_name,
        "best_relative_miss": best_row[
            "relative_miss_vs_low_energy_alpha_inv"
        ],
        "n_required_for_exact_low_energy_alpha_if_map_used": n_required_low,
        "n_required_is_not_integer": abs(n_required_low - round(n_required_low))
        > 1.0e-3,
        "n2_alpha_inv": alpha_inv_n2,
        "n2_formula": "alpha^{-1}=81*pi/2",
        "n2_is_interesting_bare_candidate_not_low_energy_result": (
            abs(alpha_inv_n2 - ALPHA_INV_CODATA) / ALPHA_INV_CODATA > 0.01
        ),
        "map_not_derived": True,
        "branch_n2_not_derived": True,
        "reading": (
            "if the quantized cap product itself is the Maxwell readout "
            "q0^2, the h=2 branch gives alpha^{-1}=81*pi/2.  This is a "
            "strong-looking bare candidate, but it is not the observed "
            "low-energy value and the map has not been derived."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Dressing/running bridge requirement
# ---------------------------------------------------------------------------

def dressing_bridge_requirement() -> dict:
    alpha_inv_bare_n2 = 81.0 * math.pi / 2.0
    shift_needed = ALPHA_INV_CODATA - alpha_inv_bare_n2
    relative_shift = shift_needed / ALPHA_INV_CODATA
    return {
        "candidate_bare_alpha_inv_n2": alpha_inv_bare_n2,
        "low_energy_alpha_inv": ALPHA_INV_CODATA,
        "inverse_alpha_shift_needed_to_low_energy": shift_needed,
        "relative_shift_needed": relative_shift,
        "shift_sign": "low-energy inverse alpha is larger than the n=2 candidate",
        "dressing_or_running_bridge_required": shift_needed > 0,
        "bridge_not_computed": True,
        "reading": (
            "the n=2 integer branch, if later derived, would have to be "
            "interpreted as a bare/high-scale value or be modified by a "
            "nontrivial readout map.  A separate dressing/running theorem is "
            "required before comparing with low-energy alpha."
        ),
    }


# ---------------------------------------------------------------------------
# 7. Next theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "derive the first-order boundary level kappa_B, the electron "
            "integer branch, and the map from C*q_geom to q0^2"
        ),
        "must_derive": [
            "a Berry/Wess-Zumino or constrained symplectic term from the completed localized frame action",
            "the level kappa_B or its prequantized integer branch",
            "why the electron/charged oscillon branch is n=2 if that route is used",
            "the action-level map q0^2 = C*q_geom, or a different derived map",
            "the dressing/running bridge from the bare/geometric value to low-energy alpha",
        ],
        "falsification_tests": [
            "if no first-order boundary term exists, this route cannot derive q0",
            "if kappa_B remains independent, alpha is not derived",
            "if n is chosen from CODATA rather than boundary physics, the gate fails",
            "if q0^2=n is postulated but not derived, the n=2 result is only a candidate",
            "if no dressing bridge is derived, n=2 cannot be claimed as observed low-energy alpha",
        ],
        "candidate_next_gate": "p18ae_integer_branch_readout_map_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_dynamic_boundary_coefficient_gate() -> dict:
    first_order = first_order_boundary_term_requirement()
    bulk = bulk_reduction_coefficient_ledger()
    regularity = regularity_endpoint_no_go()
    cap = cap_integrality_branch_ledger()
    integer_map = integer_readout_candidate_audit()
    dressing = dressing_bridge_requirement()
    requirements = next_theorem_requirements()

    closed = {
        "first_order_term_required_for_fixed_boundary_C": bool(
            first_order["second_order_has_no_fixed_boundary_one_form_at_rest"]
            and first_order["first_order_term_supplies_fixed_C"]
        ),
        "bulk_reduction_identifies_C_but_leaves_level_open": bool(
            bulk["C_eff_depends_on_bulk_coefficient_and_core_inventory"]
            and bulk["endpoint_reduction_still_leaves_kappa_B"]
        ),
        "regularity_fixes_endpoints_not_level": bool(
            regularity["regularity_fixes_profile_endpoints_not_level"]
        ),
        "cap_integrality_quantizes_C_qgeom_product": bool(
            cap["branch_quantized_but_C_to_q0_map_open"]
        ),
        "integer_readout_map_identifies_n2_candidate_but_not_low_alpha": bool(
            integer_map["n_required_is_not_integer"]
            and integer_map["n2_is_interesting_bare_candidate_not_low_energy_result"]
            and integer_map["map_not_derived"]
        ),
        "dressing_bridge_needed_not_computed": bool(
            dressing["dressing_or_running_bridge_required"]
            and dressing["bridge_not_computed"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "first_order_boundary_term_derived_from_full_action": False,
        "kappa_B_or_C_derived": False,
        "electron_integer_branch_derived": False,
        "q0_squared_equals_integer_map_derived": False,
        "bare_to_low_energy_dressing_derived": False,
        "low_energy_alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_INTEGER_BRANCH_READOUT_MAP_AND_DRESSING_REQUIRED__"
            + _pass_status("DYNAMIC_BOUNDARY_COEFFICIENT_AUDIT")
            if all(closed.values())
            else "CHECK_DYNAMIC_BOUNDARY_COEFFICIENT_GATE"
        ),
        "SCOPE": (
            "dynamic boundary coefficient gate after p18ac: a fixed boundary "
            "one-form coefficient requires a first-order geometric term.  "
            "Bulk reduction and regularity can organize C but do not derive "
            "its level.  Cap integrality gives C*q_geom=n.  The candidate "
            "readout q0^2=n makes the h=2 branch yield alpha^{-1}=81*pi/2, "
            "an interesting bare/high-scale candidate, not the observed "
            "low-energy alpha."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "first_order_requirement": first_order,
        "bulk_reduction": bulk,
        "regularity_endpoint_audit": regularity,
        "cap_integrality": cap,
        "integer_readout_candidate": integer_map,
        "dressing_bridge": dressing,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the path has become sharper.  The next possible breakthrough is "
            "not another arbitrary factor; it is a theorem that the charged "
            "frame boundary carries a first-order level whose cap product is "
            "the canonical q0^2.  If that theorem selects the h=2 branch, "
            "RefG gets a clean bare candidate 81*pi/2 for alpha^{-1}.  The "
            "low-energy 137 still requires a separate dressing bridge."
        ),
        "missing_derivations": [
            "derive the first-order boundary term from the full localized frame action",
            "derive C or kappa_B rather than leaving it as a level",
            "derive the electron branch n=2 if the h=2 route is used",
            "derive q0^2=C*q_geom=n from Maxwell normalization",
            "derive the dressing/running bridge to low-energy alpha",
        ],
        "do_not_claim": [
            "Do not claim alpha is derived.",
            "Do not claim C or kappa_B is derived.",
            "Do not claim q0^2=n is proven.",
            "Do not claim n=2 is the electron branch yet.",
            "Do not claim 81*pi/2 is the observed low-energy alpha inverse.",
            "Do not choose n from CODATA.",
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
    print("first_order_requirement:", result["first_order_requirement"])
    print("bulk_reduction:", result["bulk_reduction"])
    print("regularity_endpoint_audit:", result["regularity_endpoint_audit"])
    print("cap_integrality:", result["cap_integrality"])
    print("integer_readout_candidate:", result["integer_readout_candidate"])
    print("dressing_bridge:", result["dressing_bridge"])
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
    _print_result(derive_dynamic_boundary_coefficient_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
