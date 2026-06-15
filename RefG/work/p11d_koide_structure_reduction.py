# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: this file uses particle-sector normal forms;
# no active c_Y sign claim is made here.

"""PHASE 38b (p11d): structural reduction of the C3 constants sqrt(2) and 2/9.

Goal of the phase-38 programme: derive the two measured C3 constants
(A = sqrt(2) at -0.43 sigma, theta = 2/9 at +0.41 sigma; p11b) from
structure rather than fit.  This gate does not close the derivation; it
REDUCES each constant to one sharp structural statement and proves the
reduction exactly.

  T1 (exact theorem). EQUIPARTITION REFORMULATION OF sqrt(2):
      decompose the sqrt-mass vector (sqrt(m_e), sqrt(m_mu), sqrt(m_tau))
      into its C3-singlet part (common mode, along (1,1,1)) and its
      C3-doublet part (relative three-phase modes).  Then

          Koide Q = 2/3   <=>   |doublet|^2 = |singlet|^2,

      i.e. the triplet's TOTAL MASS splits exactly 50/50 between the
      common channel and the relative channel.  (Total mass = squared
      norm of the sqrt-mass vector.)  The amplitude sqrt(2) is therefore
      not a bare constant but a PER-CHANNEL equipartition statement.
      Sharpening: naive per-MODE equipartition (the doublet has two
      modes) would give |doublet|^2 = 2|singlet|^2, i.e. Q = 1, the
      degenerate edge -- excluded by data.  The action-level question
      becomes: why does the lepton ground state equipartition mass
      between the singlet and doublet CHANNELS (e.g. equal channel
      stiffness in the F_min normal form)?

  T2 (exact lemma). ODOMETER REFORMULATION OF THE CYCLIC LIFT:
      C3(axis) x C3(phase) is not Z9 by itself (p11 cyclic_lift_gate).
      Brute-force over return maps proves:
        (a) every 'product' map (a,b) -> (a+r, b+s) has order 1 or 3 --
            it can NEVER make the nine slots one orbit;
        (b) a 'carry' map (a,b) -> (a+1, b + c(a)) visits all nine slots
            as ONE Z9 orbit  <=>  the total carry per axis cycle
            c(0)+c(1)+c(2) is nonzero mod 3.
      So the needed cyclic-lift theorem is EQUIVALENT to one physical
      statement: completing one full axis cycle advances the
      phase/braid sector by a nonzero unit (unit braid anholonomy).
      That is the single remaining input for the lift.

  T3 (conditional consistency). h = 2 FROM SPINORIAL FRAMING:
      in the locking normal form V ~ 1 - cos(pi*(9*theta - h)) the
      framing coordinate is measured in half-turn units (p11).  A
      spinorial (double-cover, Moebius) frame returns to orientation
      after TWO half-turns, so the oriented return inserts h = 2 -- the
      first oriented minimum is theta = 2/9, matching the measured
      theta_obs = 0.2222248 +- 6.3e-6 (p11b) at +0.41 sigma.  This makes
      h = 2 conditional on the spinorial-framing postulate (candidate
      map, charge/spin sector), NOT yet derived from the full action.

Net reduction of the task: {cyclic lift, h=2, sqrt(2)} -->
  {unit braid anholonomy per axis cycle (field-equation input),
   per-channel equipartition mechanism (action input)}.

Run:  python p11d_koide_structure_reduction.py all
"""

import math
import sys
from itertools import product

import sympy as sp


PDG_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}

H_SPINOR = 2
LATTICE = 9  # C3 x C3 slots


# --- T1: equipartition theorem ------------------------------------------------

def sym_equipartition_theorem():
    """Prove: Q - 2/3 == (|doublet|^2 - |singlet|^2) / (3*(sum sqrt m)^2 / ...).

    Concretely: with nu_k = mu*(1 + A*cos(theta + 2*pi*k/3)),
      |singlet|^2 = 3*mu^2,  |doublet|^2 = (3/2)*mu^2*A^2,
    and Q = 1/3 + A^2/6, so
      Q = 2/3  <=>  A^2 = 2  <=>  |doublet|^2 = |singlet|^2.
    Returns the symbolic residuals (all must be 0).
    """
    mu, A, th = sp.symbols("mu A theta", positive=True)
    nu = [mu * (1 + A * sp.cos(th + 2 * sp.pi * k / 3)) for k in range(3)]

    singlet = sum(nu) / 3  # component along (1,1,1)/sqrt(3), times sqrt(3)
    singlet_norm2 = 3 * singlet**2
    total_norm2 = sum(x**2 for x in nu)
    doublet_norm2 = sp.simplify(total_norm2 - singlet_norm2)

    r_singlet = sp.simplify(singlet_norm2 - 3 * mu**2)
    r_doublet = sp.simplify(doublet_norm2 - sp.Rational(3, 2) * mu**2 * A**2)

    Q = total_norm2 / (sum(nu)) ** 2
    # Q - 2/3 proportional to (doublet - singlet): check the exact identity
    identity = sp.simplify((Q - sp.Rational(2, 3))
                           - (doublet_norm2 - singlet_norm2) / (9 * singlet**2))
    return {
        "singlet_norm_residual": r_singlet,
        "doublet_norm_residual": r_doublet,
        "Q_equipartition_identity_residual": identity,
    }


def pdg_channel_split():
    """Numeric: the PDG lepton triplet splits its total mass between the
    singlet and doublet channels in ratio 1 within ~1e-4."""
    roots = [math.sqrt(PDG_MEV[n]) for n in ("electron", "muon", "tau")]
    mean = sum(roots) / 3
    singlet2 = 3 * mean**2
    total2 = sum(r * r for r in roots)
    doublet2 = total2 - singlet2
    ratio = doublet2 / singlet2
    return {
        "singlet_MeV": singlet2,
        "doublet_MeV": doublet2,
        "total_mass_MeV": total2,
        "channel_ratio": ratio,
        "per_mode_alternative_ratio": 2.0,
        "per_mode_excluded": abs(ratio - 2.0) > 0.9,
        "equipartition_holds_1e3": abs(ratio - 1.0) < 1e-3,
    }


# --- T2: odometer lemma ---------------------------------------------------------

def map_order_and_orbit(step):
    """Order of the permutation defined by `step` on Z3 x Z3, and whether the
    orbit of (0,0) covers all nine slots."""
    state = (0, 0)
    seen = [state]
    while True:
        state = step(state)
        if state == seen[0]:
            break
        seen.append(state)
    return len(seen), len(set(seen)) == LATTICE


def odometer_lemma():
    """Exhaustive check of both families of return maps on C3 x C3."""
    # (a) product maps: (a,b) -> (a+r, b+s) -- independent rotations, no carry
    product_orders = set()
    for r, s in product(range(3), range(3)):
        order, full = map_order_and_orbit(
            lambda ab, r=r, s=s: ((ab[0] + r) % 3, (ab[1] + s) % 3)
        )
        product_orders.add((order, full))
    product_never_nine = all(not full for _, full in product_orders)

    # (b) carry maps: (a,b) -> (a+1, b + c(a)) for all carry functions c: Z3->Z3
    carry_results = []
    for c0, c1, c2 in product(range(3), repeat=3):
        carry = (c0, c1, c2)
        order, full = map_order_and_orbit(
            lambda ab, carry=carry: ((ab[0] + 1) % 3,
                                     (ab[1] + carry[ab[0]]) % 3)
        )
        total_carry = sum(carry) % 3
        carry_results.append((carry, order, full, total_carry))
    equivalence_holds = all(
        full == (total != 0) for _, _, full, total in carry_results
    )
    return {
        "product_maps_max_order": max(o for o, _ in product_orders),
        "product_never_single_9_orbit": product_never_nine,
        "carry_single_orbit_iff_total_carry_nonzero": equivalence_holds,
        "carry_cases_checked": len(carry_results),
        "needed_physical_input": (
            "unit (nonzero mod 3) braid anholonomy per full axis cycle of the "
            "charged oriented defect -- to be derived from the field equations"
        ),
    }


# --- T3: h=2 conditional consistency --------------------------------------------

def locking_minimum(h=H_SPINOR):
    """First oriented minimum of V ~ 1 - cos(pi*(9*theta - h)): theta = h/9."""
    theta = h / LATTICE
    v = 1.0 - math.cos(math.pi * (LATTICE * theta - h))
    return theta, v


def h2_consistency():
    theta_pred, v_min = locking_minimum()
    theta_obs, sigma = 0.222224761, 6.25e-06  # p11b MC values
    pull = (theta_obs - theta_pred) / sigma
    return {
        "framing_units": "half-turns (the pi in the lock normal form)",
        "spinorial_return": "double cover returns orientation after TWO half-turns -> h=2",
        "theta_predicted": theta_pred,
        "V_at_minimum": v_min,
        "theta_observed_p11b": theta_obs,
        "pull_sigma": pull,
        "conditional_on": "spinorial (Moebius) framing postulate -- candidate map, not action-derived",
    }


# --- ledger ----------------------------------------------------------------------

def status_assessment(t1, n1, t2, t3):
    sym_ok = all(v == 0 for v in t1.values())
    return {
        "T1": "PASS_SYMBOLIC_EQUIPARTITION_THEOREM" if sym_ok
              else "T1_DID_NOT_VERIFY",
        "T1_numeric": "PASS_PDG_CHANNEL_SPLIT_UNITY"
                      if (n1["equipartition_holds_1e3"] and n1["per_mode_excluded"])
                      else "T1N_DID_NOT_VERIFY",
        "T2": "PASS_ODOMETER_LEMMA_EXHAUSTIVE"
              if (t2["product_never_single_9_orbit"]
                  and t2["carry_single_orbit_iff_total_carry_nonzero"])
              else "T2_DID_NOT_VERIFY",
        "T3": "PASS_H2_SPINORIAL_CONSISTENCY_CONDITIONAL"
              if abs(t3["pull_sigma"]) < 2.0 else "T3_DID_NOT_VERIFY",
        "open": "OPEN_TWO_PHYSICAL_INPUTS -- (i) unit braid anholonomy per "
                "axis cycle from the charged defect field equations; "
                "(ii) per-channel equipartition mechanism from the F_min "
                "normal form. These two close sqrt(2) and 2/9.",
    }


def do_not_claim():
    return [
        "Do not claim sqrt(2) is derived: T1 is an exact REFORMULATION "
        "(equipartition of mass between singlet and doublet channels); the "
        "mechanism selecting equipartition is open.",
        "Do not claim theta=2/9 is derived: T2 reduces the cyclic lift to "
        "the unit-anholonomy statement, and T3 makes h=2 conditional on the "
        "spinorial-framing candidate map; neither is yet an action theorem.",
        "Do not claim per-mode equipartition: it is EXCLUDED by data "
        "(would give Q=1); the verified statement is per-CHANNEL.",
        "Do not claim the odometer lemma is itself physics: it is exact "
        "finite group theory that pinpoints WHICH physical statement is "
        "needed (nonzero total carry = braid anholonomy).",
    ]


# --- main -------------------------------------------------------------------------

def main():
    print("=" * 72)
    print("PHASE 38b (p11d): structural reduction of sqrt(2) and 2/9")
    print("=" * 72)

    print("\n1. T1 symbolic: equipartition theorem")
    t1 = sym_equipartition_theorem()
    for key, val in t1.items():
        print(f"  {key} = {val}")
    print("  => Q = 2/3  <=>  |doublet|^2 = |singlet|^2  (A = sqrt(2))")

    print("\n2. T1 numeric: PDG channel split")
    n1 = pdg_channel_split()
    print(f"  singlet channel = {n1['singlet_MeV']:.4f} MeV,"
          f" doublet channel = {n1['doublet_MeV']:.4f} MeV"
          f" (total {n1['total_mass_MeV']:.4f})")
    print(f"  channel ratio = {n1['channel_ratio']:.8f}   (equipartition = 1;"
          f" per-mode alternative = 2 -- excluded: {n1['per_mode_excluded']})")

    print("\n3. T2: odometer lemma on C3 x C3 (exhaustive)")
    t2 = odometer_lemma()
    print(f"  product maps: max order = {t2['product_maps_max_order']},"
          f" single 9-orbit impossible = {t2['product_never_single_9_orbit']}")
    print(f"  carry maps ({t2['carry_cases_checked']} cases): single 9-orbit"
          f" <=> total carry != 0 mod 3 : {t2['carry_single_orbit_iff_total_carry_nonzero']}")
    print(f"  needed physical input: {t2['needed_physical_input']}")

    print("\n4. T3: h=2 spinorial consistency (conditional)")
    t3 = h2_consistency()
    print(f"  framing in {t3['framing_units']}; {t3['spinorial_return']}")
    print(f"  theta_pred = {t3['theta_predicted']:.9f}, theta_obs ="
          f" {t3['theta_observed_p11b']:.9f}, pull = {t3['pull_sigma']:+.2f} sigma")
    print(f"  conditional on: {t3['conditional_on']}")

    print("\n5. STATUS")
    for key, val in status_assessment(t1, n1, t2, t3).items():
        print(f"  {key}: {val}")

    print("\n6. do_not_claim")
    for item in do_not_claim():
        print(f"  - {item}")


if __name__ == "__main__":
    _ = sys.argv[1:]
    main()
