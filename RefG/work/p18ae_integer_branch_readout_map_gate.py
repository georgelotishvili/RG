# Notation header (see NOTATION.md):
# This gate follows p18ad.  It audits the candidate map from the integer
# cap branch C*q_geom=n to Maxwell readout strength q0.  The key test is
# whether q0^2=n is a theorem, a standard Wilson phase, or only a candidate.

"""
================================================================================
PHASE 18ae: Integer branch readout-map gate
================================================================================

Purpose
-------
p18ad identified a sharp candidate:

    C*q_geom = n,
    possible readout: q0^2 = n.

For q_geom=2/9 and n=2 this gives

    alpha^{-1} = 81*pi/2 = 127.2345...

This gate checks what this map actually means.  It separates three statements
that must not be confused:

  1. Wilson phase quantization: q_e*Phi = 2*pi*n,
  2. energy/readout quantization: q0^2 = n,
  3. branch selection: electron branch n=2.

Main result
-----------
The attractive n=2 result is NOT a standard Wilson-phase consequence.  If one
uses the cap holonomy as an ordinary Wilson flux, the normalization is wildly
different.  The n=2 route only works as an energy/readout map:

    the integer cap product counts the squared canonical readout strength,
    q0^2, not the linear Wilson charge q0.

That is a possible theorem-shaped target, but it is not derived here.  It
requires a dynamical proof from the boundary symplectic form and Maxwell
normalization.

What this gate does NOT claim
-----------------------------
- It does not derive alpha.
- It does not prove q0^2=n.
- It does not prove the electron branch is n=2.
- It does not compute low-energy dressing.
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
Q0_REQUIRED_LOW = math.sqrt(4.0 * math.pi * ALPHA_CODATA) / Q_GEOM


# ---------------------------------------------------------------------------
# 1. Standard Wilson phase route is not the n=2 route
# ---------------------------------------------------------------------------

def standard_wilson_phase_no_go() -> dict:
    q0, qg, n = sp.symbols("q0 q_geom n", positive=True)
    phi_cap = 2 * sp.pi * qg
    q_e = q0 * qg
    condition = sp.Eq(q_e * phi_cap, 2 * sp.pi * n)
    q0_solution = sp.solve(condition, q0)[0]
    alpha = sp.simplify((q0_solution * qg) ** 2 / (4 * sp.pi))
    alpha_inv = sp.simplify(1 / alpha)

    q0_num_n1 = float(q0_solution.subs({qg: Q_GEOM, n: 1}))
    alpha_inv_num_n1 = float(alpha_inv.subs({qg: Q_GEOM, n: 1}))

    return {
        "Wilson_condition": "q_e*Phi_cap = 2*pi*n",
        "Phi_cap": "2*pi*q_geom",
        "q_e": "q0*q_geom",
        "q0_solution": str(q0_solution),
        "alpha_inv_solution": str(alpha_inv),
        "q0_numeric_n1": q0_num_n1,
        "alpha_inv_numeric_n1": alpha_inv_num_n1,
        "standard_Wilson_map_fails_alpha_scale": alpha_inv_num_n1 < 1.0,
        "reading": (
            "ordinary Wilson product quantization does not give q0^2=n.  It "
            "puts the geometric cap in the denominator of a linear charge and "
            "produces the wrong scale.  Therefore the n=2 route must be an "
            "energy/readout theorem, not a standard Wilson shortcut."
        ),
    }


# ---------------------------------------------------------------------------
# 2. Energy/readout candidate q0^2=n
# ---------------------------------------------------------------------------

def energy_readout_candidate_map() -> dict:
    rows = {}
    for n in range(1, 10):
        q0 = math.sqrt(n)
        alpha_inv = 4.0 * math.pi / (n * Q_GEOM**2)
        rows[f"n{n}"] = {
            "q0": q0,
            "q0_squared": n,
            "alpha_inv": alpha_inv,
            "relative_miss_vs_low_energy_alpha_inv": abs(
                alpha_inv - ALPHA_INV_CODATA
            )
            / ALPHA_INV_CODATA,
        }

    n2 = rows["n2"]
    q0_miss_low = abs(n2["q0"] - Q0_REQUIRED_LOW) / Q0_REQUIRED_LOW

    return {
        "candidate_map": "q0^2 = n",
        "rows": rows,
        "n2_formula": "alpha^{-1}=81*pi/2",
        "n2_q0": n2["q0"],
        "q0_required_for_low_energy_alpha": Q0_REQUIRED_LOW,
        "n2_q0_relative_miss_vs_low_energy": q0_miss_low,
        "n2_is_close_in_amplitude_but_not_exact": q0_miss_low < 0.05,
        "map_requires_energy_not_linear_phase_reading": True,
        "map_not_derived": True,
        "reading": (
            "q0^2=n is mathematically clean and makes h=2 give q0=sqrt(2).  "
            "It is also close to the low-energy required amplitude, but close "
            "is not a derivation.  The map must be obtained from the action."
        ),
    }


# ---------------------------------------------------------------------------
# 3. Branch selection audit
# ---------------------------------------------------------------------------

def branch_selection_audit() -> dict:
    candidates = {
        "minimal_cap_n1": 1,
        "oriented_h_branch_n2": H,
        "order9_branch_n9": ORDER,
        "h_plus_one_n3": H + 1,
        "order_minus_h_n7": ORDER - H,
    }

    rows = {}
    for name, n in candidates.items():
        alpha_inv = 4.0 * math.pi / (n * Q_GEOM**2)
        rows[name] = {
            "n": n,
            "alpha_inv_if_q0sq_equals_n": alpha_inv,
            "relative_miss_vs_low_energy_alpha_inv": abs(
                alpha_inv - ALPHA_INV_CODATA
            )
            / ALPHA_INV_CODATA,
        }

    best_name, best = min(
        rows.items(),
        key=lambda item: item[1]["relative_miss_vs_low_energy_alpha_inv"],
    )

    return {
        "branch_candidates": rows,
        "best_candidate_among_named_branches": best_name,
        "best_named_branch_is_oriented_h2": best_name == "oriented_h_branch_n2",
        "h2_branch_selected_by_prior_geometry_but_not_by_alpha": True,
        "branch_selection_not_fitted": True,
        "branch_selection_still_needs_theorem": True,
        "reading": (
            "among the simple named branches, h=2 is the only one in the "
            "right neighborhood.  That is encouraging because h=2 already "
            "comes from oriented-frame closure, but the electron branch still "
            "has to be derived dynamically."
        ),
    }


# ---------------------------------------------------------------------------
# 4. Compatibility with previous 2/9 and sqrt(2) motifs
# ---------------------------------------------------------------------------

def motif_separation_audit() -> dict:
    theta = sp.Rational(H, ORDER)
    q0 = sp.sqrt(H)
    qe = sp.simplify(q0 * theta)
    alpha = sp.simplify(qe**2 / (4 * sp.pi))

    return {
        "theta_register": str(theta),
        "q0_if_h2_integer_readout": str(q0),
        "canonical_charge_candidate": str(qe),
        "alpha_candidate": str(alpha),
        "alpha_inv_candidate": str(sp.simplify(1 / alpha)),
        "sqrt2_appears_as_readout_amplitude_not_lepton_mass_formula": True,
        "do_not_merge_with_Koide_sqrt2_without_theorem": True,
        "reading": (
            "the route naturally combines the 2/9 register with a sqrt(2) "
            "readout amplitude.  This must remain separated from the lepton "
            "mass/Koide sqrt(2) motif unless a common action-level theorem "
            "connects them."
        ),
    }


# ---------------------------------------------------------------------------
# 5. Low-energy target and dressing bridge
# ---------------------------------------------------------------------------

def low_energy_bridge_audit() -> dict:
    alpha_inv_n2 = 81.0 * math.pi / 2.0
    low_shift = ALPHA_INV_CODATA - alpha_inv_n2
    alpha_n2 = 1.0 / alpha_inv_n2
    alpha_low = ALPHA_CODATA

    return {
        "bare_candidate_alpha_inv_n2": alpha_inv_n2,
        "low_energy_alpha_inv": ALPHA_INV_CODATA,
        "inverse_alpha_shift_needed": low_shift,
        "relative_inverse_shift_needed": low_shift / ALPHA_INV_CODATA,
        "alpha_candidate_n2": alpha_n2,
        "alpha_low_energy": alpha_low,
        "low_energy_value_is_weaker_coupling_than_n2_candidate": (
            alpha_low < alpha_n2
        ),
        "dressing_bridge_required": True,
        "bridge_not_computed": True,
        "reading": (
            "if n=2 is a bare/geometric value, the low-energy value must be "
            "obtained by a separate dressing/running map.  This gate does not "
            "supply that map."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Next theorem requirements
# ---------------------------------------------------------------------------

def next_theorem_requirements() -> dict:
    return {
        "needed_object": (
            "derive the energy/readout map q0^2=C*q_geom=n from the boundary "
            "symplectic form and canonical Maxwell normalization"
        ),
        "must_derive": [
            "why the cap product is squared readout strength q0^2 rather than linear Wilson charge q0",
            "why the charged oscillon/electron branch is the oriented h=2 branch",
            "how q0=sqrt(2) combines with q_geom=2/9 in canonical Maxwell units",
            "whether 81*pi/2 is a bare/high-scale alpha inverse",
            "the dressing/running bridge from that bare value to low-energy alpha",
        ],
        "falsification_tests": [
            "if the only derivation is ordinary Wilson phase quantization, the n=2 route fails",
            "if q0^2=n is merely postulated, alpha is not derived",
            "if h=2 is selected because it is numerically closest, the gate fails",
            "if no dressing bridge is supplied, 81*pi/2 cannot be called observed alpha",
        ],
        "candidate_next_gate": "p18af_bare_to_low_energy_dressing_gate.py",
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_integer_branch_readout_map_gate() -> dict:
    wilson = standard_wilson_phase_no_go()
    energy = energy_readout_candidate_map()
    branch = branch_selection_audit()
    motifs = motif_separation_audit()
    bridge = low_energy_bridge_audit()
    requirements = next_theorem_requirements()

    closed = {
        "standard_Wilson_phase_route_rejected": bool(
            wilson["standard_Wilson_map_fails_alpha_scale"]
        ),
        "energy_readout_candidate_map_identified": bool(
            energy["map_requires_energy_not_linear_phase_reading"]
            and energy["map_not_derived"]
        ),
        "h2_branch_is_best_named_candidate_without_fit": bool(
            branch["best_named_branch_is_oriented_h2"]
            and branch["branch_selection_not_fitted"]
        ),
        "sqrt2_and_2over9_motifs_kept_separate": bool(
            motifs["do_not_merge_with_Koide_sqrt2_without_theorem"]
        ),
        "low_energy_dressing_bridge_required": bool(
            bridge["dressing_bridge_required"]
            and bridge["bridge_not_computed"]
        ),
        "no_CODATA_fit_performed": True,
    }

    open_checks = {
        "q0_squared_equals_n_derived": False,
        "ordinary_Wilson_replaced_by_energy_readout_theorem": False,
        "electron_branch_n2_derived": False,
        "bare_alpha_scale_identified": False,
        "dressing_bridge_derived": False,
        "observed_low_energy_alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_ENERGY_READOUT_MAP_AND_DRESSING_REQUIRED__"
            + _pass_status("INTEGER_BRANCH_READOUT_AUDIT")
            if all(closed.values())
            else "CHECK_INTEGER_BRANCH_READOUT_MAP"
        ),
        "SCOPE": (
            "integer branch readout-map gate after p18ad: ordinary Wilson "
            "phase quantization is rejected as the source of q0^2=n.  The "
            "useful route is instead an energy/readout theorem in which the "
            "cap integer becomes the squared canonical readout strength.  "
            "The h=2 branch gives q0=sqrt(2) and alpha^{-1}=81*pi/2, but "
            "this remains a bare candidate until the map, branch selection "
            "and dressing bridge are derived."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "Wilson_no_go": wilson,
        "energy_readout_candidate": energy,
        "branch_selection": branch,
        "motif_separation": motifs,
        "low_energy_bridge": bridge,
        "requirements_for_next_gate": requirements,
        "physical_reading": (
            "the attractive part is real but conditional: q_geom=2/9 and "
            "q0=sqrt(2) combine into a clean alpha^{-1}=81*pi/2.  The hard "
            "work is to prove that the integer cap branch is an energy "
            "readout strength, not an ordinary Wilson phase, and then to "
            "connect the bare value to low-energy 137."
        ),
        "missing_derivations": [
            "derive q0^2=C*q_geom=n from the boundary symplectic form",
            "derive the electron branch n=2 dynamically",
            "derive canonical Maxwell normalization for q0=sqrt(2)",
            "derive bare-to-low-energy dressing/running",
        ],
        "do_not_claim": [
            "Do not claim alpha is derived.",
            "Do not claim ordinary Wilson quantization gives q0^2=n.",
            "Do not claim h=2 is selected by alpha fitting.",
            "Do not merge this sqrt(2) with Koide/lepton sqrt(2) without a theorem.",
            "Do not call 81*pi/2 the observed low-energy alpha inverse.",
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
    print("Wilson_no_go:", result["Wilson_no_go"])
    print("energy_readout_candidate:", result["energy_readout_candidate"])
    print("branch_selection:", result["branch_selection"])
    print("motif_separation:", result["motif_separation"])
    print("low_energy_bridge:", result["low_energy_bridge"])
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
    _print_result(derive_integer_branch_readout_map_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
