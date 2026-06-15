# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: particle-sector framed-closure normal forms only.

"""PHASE 49 (p11g): charged oriented-frame gate for h=2.

The order-9 lift supplies a reduced lattice coordinate theta=h/9, but it does
not by itself choose h.  This gate isolates the finite selection logic.

If the charged defect couples only to a projective/nematic director, then
h=1 is allowed because n and -n are the same physical line.  In that case
h=2 is not derived.

If the charged defect couples to an oriented frame/current, the sign of the
frame matters.  Then h=1 sends n -> -n and does not close the charged
boundary data.  The first non-trivial oriented closure is h=2.

The finite selection is therefore closed only conditionally:

    oriented charged coupling + non-trivial defect + positive C3 branch
        -> h=2.

The remaining physical theorem is to derive the oriented charged-frame
coupling from the RG action or localized charged defect equations, rather
than inserting it as a selection rule.
"""

from __future__ import annotations

import math


ORDER9_SLOTS = 9
SELECTED_H = 2


def director_after_half_turns(h: int) -> tuple[int, int]:
    """Director in a 2D slice after h half-turns, rounded to exact signs."""
    angle = math.pi * h
    return (round(math.cos(angle)), round(math.sin(angle)))


def projective_closed(h: int) -> bool:
    """Projective/nematic closure identifies n with -n."""
    n = director_after_half_turns(h)
    return n in ((1, 0), (-1, 0))


def oriented_closed(h: int) -> bool:
    """Oriented charged frame closure keeps the sign of n."""
    return director_after_half_turns(h) == (1, 0)


def c3_raw_frequencies(theta: float) -> list[float]:
    return [
        1.0 + math.sqrt(2.0) * math.cos(theta + 2.0 * math.pi * k / 3.0)
        for k in range(3)
    ]


def c3_positive(theta: float) -> bool:
    return all(value > 0.0 for value in c3_raw_frequencies(theta))


def positivity_edge() -> float:
    """First small-theta edge where the lowest C3 frequency reaches zero."""
    return math.pi / 12.0


def coupling_closure_residuals(h: int) -> dict[str, object]:
    """Compare projective and oriented coupling closures at branch h."""
    n0 = (1, 0)
    nh = director_after_half_turns(h)
    projective_tensor_residual = 0
    oriented_vector_residual = (nh[0] - n0[0], nh[1] - n0[1])
    return {
        "h": h,
        "director": nh,
        "projective_tensor_residual": projective_tensor_residual,
        "oriented_vector_residual": oriented_vector_residual,
        "projective_closed": projective_closed(h),
        "oriented_closed": oriented_closed(h),
    }


def h_branch_table(max_h: int = 6) -> list[dict[str, object]]:
    rows = []
    for h in range(max_h + 1):
        theta = h / ORDER9_SLOTS
        nontrivial = h != 0
        orient_ok = oriented_closed(h)
        positive = c3_positive(theta)
        selected = h == SELECTED_H and nontrivial and orient_ok and positive
        rows.append(
            {
                **coupling_closure_residuals(h),
                "theta": theta,
                "nontrivial": nontrivial,
                "positive_c3_branch": positive,
                "below_first_positive_edge": theta < positivity_edge(),
                "selected_if_oriented_charged": selected,
            }
        )
    return rows


def conditional_h2_selection_theorem() -> dict[str, object]:
    table = h_branch_table()
    oriented_candidates = [
        row["h"]
        for row in table
        if row["nontrivial"]
        and row["oriented_closed"]
        and row["positive_c3_branch"]
    ]
    return {
        "assumptions": [
            "charged defect boundary data are oriented-frame data, not nematic/projective line data",
            "h=0 is the trivial no-winding/no-generation-splitting branch",
            "the charged-lepton C3 operator stays on the small positive-frequency branch",
        ],
        "oriented_positive_candidates_checked": oriented_candidates,
        "selected_h": oriented_candidates[0] if oriented_candidates else None,
        "theta_selected": SELECTED_H / ORDER9_SLOTS,
        "h0_status": "rejected as trivial",
        "h1_status": "projective/nematic closure only; oriented charged vector changes sign",
        "h2_status": "first non-trivial oriented closure on the positive C3 branch",
        "higher_h_status": "no lower non-trivial oriented positive branch appears before h=2",
        "finite_selection_closed": oriented_candidates[:1] == [SELECTED_H],
    }


def charged_oriented_frame_h2_gate() -> dict[str, object]:
    theorem = conditional_h2_selection_theorem()
    finite_closed = theorem["finite_selection_closed"]
    return {
        "status": (
            "PASS_FINITE_H2_SELECTION_IF_ORIENTED_CHARGED_COUPLING__ACTION_DERIVATION_OPEN"
            if finite_closed
            else "CHECK_H2_SELECTION"
        ),
        "finite_theorem": theorem,
        "projective_counterfactual": (
            "if the charged sector is only nematic/projective, h=1 cannot be "
            "excluded and h=2 is not selected"
        ),
        "physical_theorem_open": (
            "derive an orientation-sensitive charged-frame current/coupling "
            "from the RG action or localized charged defect equations"
        ),
        "allowed_language": "h=2 is conditionally selected by oriented charged-frame closure",
        "forbidden_language": "h=2 is derived from the full RG action",
        "do_not_claim": [
            "Do not claim h=2 is action-derived until the charged oriented-frame coupling is derived.",
            "Do not reject h=1 unless the charged sector is proven oriented rather than projective/nematic.",
            "Do not use the h=2 gate as a substitute for the full localized 3D fluctuation spectrum.",
            "Do not identify the oriented-frame sign with electric charge before the charge-current theorem exists.",
        ],
    }


def main() -> None:
    gate = charged_oriented_frame_h2_gate()
    print("PHASE 49: charged oriented-frame h=2 gate")
    print(f"status: {gate['status']}")
    theorem = gate["finite_theorem"]
    print(f"selected_h: {theorem['selected_h']}")
    print(f"theta_selected: {theorem['theta_selected']}")
    print(f"h1: {theorem['h1_status']}")
    print(f"open: {gate['physical_theorem_open']}")


if __name__ == "__main__":
    main()
