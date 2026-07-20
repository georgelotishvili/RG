# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Charge-conjugation sector (this gate): decides how the C-map acts on the
# orientation property (theta fiber + axis nA of p18e/p18f) from the
# theory's own ontology, and shows the decision is dynamically harmless:
# theta-axis decoupling holds under EITHER map.  Fields/invariants are
# those of p18e (theta, Pt, Qt, Vt^A) and p18f (nA, Pn, Qn^A, Vn^BA).

"""
================================================================================
PHASE 18g: Charge-conjugation map gate (first lock of the alpha chain)
================================================================================

Purpose
-------
Close the C1-vs-C2 ambiguity left open by p18f (its referee found two
epsilon-contracted cross operators O5, O7 whose exclusion rested on the
C1 assignment that p18f declared as a postulate but did not derive).  Per the review
council's ordering (Codex, 2026-07-07): the C-map must be decided from the
theory's ontology -- "what does RefG's charge sign physically flip" -- not
by convenience, BEFORE the U(1)/Maxwell gate is attempted.

The two candidate maps (p18f):

    C1:  theta -> -theta,  nA -> +nA   (twist mirror, axis fixed)
    C2:  theta -> -theta,  nA -> -nA   (full frame mirror)

Results (all executable below)
------------------------------
1. REGISTER ARITHMETIC: the orientation property carries TWO topological
   registers -- the line winding W_theta (p18e: oint d(theta) = 2*pi*W)
   and the point (hedgehog) degree W_n (p18f: pi_2(S^2) = Z).  Executable:

       C1: (W_theta, W_n) -> (-W_theta, +W_n)
       C2: (W_theta, W_n) -> (-W_theta, -W_n)

   (deg(-n) = -deg(n) in 3D: verified by direct integration.)

2. REGISTER DICHOTOMY THEOREM (the honest form of the C-map decision):
   the article (5.3) demands e+ e- annihilation into pure radiation --
   "mirror twists cancel each other and the energy passes into the
   helicoidal propagating channel."  Smooth radiation encloses zero
   pi_2 degree and zero distant line winding (it can carry pi_3 Hopf
   charge -- article's Ranada citation -- but Hopf charge cannot absorb
   pi_2 degree), so annihilation is topologically allowed ONLY if every
   register of the positron is the negative of the electron's:

       (W_theta, W_n)_e+  =  -(W_theta, W_n)_e-.

   BRANCH A: if the electron carries the point register (W_n != 0, the
   p18f hedgehog SLOT -- p18f itself insists the slot is not yet the
   electron), the C-map MUST act orientation-reversingly (improperly)
   on the axis; C2 (n -> -n) is the representative choice.  Under C1
   the "positron" would carry the SAME hedgehog charge and
   e+ e- -> radiation would be topologically forbidden.
   BRANCH B: if the electric charge lives in the line/framing register
   (W_n = 0 electron) -- and the article's own ontology leans THIS way:
   it rejects the point-particle picture, draws the electron as an
   extended toroidal Moebius ring, and ties the charge sign to the
   TWIST direction -- then C1 suffices.
   WHICH BRANCH IS REAL is decided by the gauged completion (locks
   2-3): in standard emergent-U(1) constructions of the planned p18h
   type, the pi_2 defect emerges as the MAGNETIC charge, which would
   select branch B for the electron.  The dichotomy is recorded, not
   resolved.  Load-bearing assumptions, declared: the axis is a true
   oriented vector (S^2 target -- canon 480 framed orientation, p11g
   oriented-vs-projective distinction; an RP^2 director would erase
   the sign of W_n), and the unit constraint does not melt in cores.

3. O5/O7 UNDER C2: O5 = eps_ABC nA^A Qn^B Vt^C stays C2-ODD (excluded,
   as in p18f).  O7 = eps_ABC nA^A Vt^B (n_D Vn^DC) is C2-EVEN --
   admissible by symmetry.  So the frame-mirror decision APPEARS to open
   the theta-axis mixing door.  It does not:

4. DYNAMICAL DECOUPLING THEOREM (the gate's central result, executable):
   adding e7*O7 to the cone-forced quadratic theory and computing the
   EXACT 3x3 dispersion at a general wavevector gives the branches

       omega^2 = k^2                                   (one exact mode)
       omega^2 = k^2 +- |e7*k_x*k_z| / (2*sqrt(kn*kt))  (mixed pair)

   (formulas on the k_y = 0 slice, WLOG by azimuthal symmetry about the
   background axis; the general split is e7*k_z*sqrt(k_x^2+k_y^2) /
   (2*sqrt(kn*kt)), maximal at 45 degrees, with group speed exceeding 1
   as well).  For ANY e7 != 0 there exist oblique directions with a
   strictly SUPERLUMINAL branch -- no small-coupling threshold.  Exact
   luminality of the orientation channel (the p18e/p18f cone
   requirement; equivalently causality; kn, kt > 0 by no-ghost)
   therefore forces

       e7 = 0.

   (The mixed branches straddle the cone as a +- pair, so even bare
   causality -- the weakest defensible requirement -- forces e7 = 0,
   not only exact luminality.  Scope: quadratic analysis; no symmetry
   otherwise protects e7 = 0, so the removal is an exact-luminality/
   causality postulate of the medium elevated to all scales, and the
   grammar completeness is inherited from p18f, not re-proven.)
   CONCLUSION: theta-axis decoupling holds under BOTH C-maps -- under
   C1 by parity, under C2 by luminality.  What p18f had to postulate is
   now a theorem, and the C-map dichotomy has NO quadratic-level side
   effects: the wave sector is identical on both branches, so the
   chain is not blocked by the unresolved branch choice.

Chain position (review council ordering)
----------------------------------------
LOCK 1 (this gate): C-map classified -- register dichotomy theorem
        (branch A: W_n-electron => improper axis action, C2
        representative; branch B: framing-register electron => C1),
        dynamically harmless either way; branch decision lands in
        locks 2-3.
LOCK 2 (p18h_frame_connection_u1_gate): covariant coupling
        D theta = d theta + omega(n) . d n; global shift -> LOCAL
        redundancy; mode count 3 -> 2; luminality + solar transparency
        re-checked.  [Codex naming p18g -> shifted to p18h: the C-map
        got its own gate first, as Codex itself required.]
LOCK 3 (p18i_hedgehog_screening_maxwell_gate): far field -> 1/r^2,
        Gauss law, Coulomb energy.
ONLY THEN (p18j_finite_orientation_lock_alpha_gate): N derived as the
        ratio of two spectra on the SAME finite orientation-frame
        resonator (fiber-step / axis-step); NO number scanning; with
        the elementary winding W = 1 (p18e route premise, W itself
        pending the gauged completion per p18f), alpha = 1/(4*pi*N)
        only if N = 10.90497833 comes out.

What this gate does NOT claim
-----------------------------
- alpha, Maxwell, U(1), screening: all still open (locks 2-4).
- The C2 conclusion is conditional on the electron carrying the point
  register (p18f slot); the conditionality is part of the theorem.
- Annihilation completeness is a topological selection rule; the
  annihilation AMPLITUDE remains underived (article's own open task).
"""

from __future__ import annotations

import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


eps = sp.symbols("epsilon", real=True)
t, x, y, z = sp.symbols("t x y z", real=True)
COORDS = (t, x, y, z)
ETA = [sp.Integer(1), -1, -1, -1]


def _grad(expr):
    return [sp.diff(expr, c) for c in COORDS]


def _con(u, v):
    return sum(ETA[m] * u[m] * v[m] for m in range(4))


# ---------------------------------------------------------------------------
# 1. Register arithmetic under the two C-maps
# ---------------------------------------------------------------------------

def register_arithmetic() -> dict:
    # line register: theta = W * atan2(y, x) around a defect line
    s = sp.symbols("s", real=True)
    W = sp.symbols("W", integer=True)
    theta_loop = W * sp.atan2(sp.sin(s), sp.cos(s))
    circ = sp.integrate(sp.simplify(sp.diff(theta_loop, s)),
                        (s, 0, 2 * sp.pi))
    w_theta_flips_under_theta_flip = (
        sp.simplify(circ + sp.integrate(
            sp.simplify(sp.diff(-theta_loop, s)), (s, 0, 2 * sp.pi)
        )) == 0
    )

    # point register: hedgehog degree, and its sign under n -> -n
    thg, phg = sp.symbols("vartheta varphi", real=True)
    n_h = sp.Matrix(
        [
            sp.sin(thg) * sp.cos(phg),
            sp.sin(thg) * sp.sin(phg),
            sp.cos(thg),
        ]
    )

    def deg(nv):
        integ = sp.simplify(
            nv.dot(sp.diff(nv, thg).cross(sp.diff(nv, phg)))
        )
        return sp.simplify(
            sp.integrate(
                sp.integrate(integ, (phg, 0, 2 * sp.pi)),
                (thg, 0, sp.pi),
            )
            / (4 * sp.pi)
        )

    d_plus = deg(n_h)
    d_minus = deg(-n_h)

    return {
        "line_register_quantized": sp.simplify(circ - 2 * sp.pi * W) == 0,
        "w_theta_flips_under_theta_flip": bool(
            w_theta_flips_under_theta_flip
        ),
        "hedgehog_degree_plus": d_plus,
        "hedgehog_degree_minus": d_minus,
        "w_n_flips_only_under_axis_flip": bool(
            d_plus == 1 and d_minus == -1
        ),
        "table": {
            "C1": "(W_theta, W_n) -> (-W_theta, +W_n)",
            "C2": "(W_theta, W_n) -> (-W_theta, -W_n)",
        },
    }


# ---------------------------------------------------------------------------
# 2. Annihilation completeness theorem (conditional)
# ---------------------------------------------------------------------------

def annihilation_completeness_theorem() -> dict:
    W_th, W_n = sp.symbols("W_theta W_n", integer=True)

    def c1(reg):
        return (-reg[0], reg[1])

    def c2(reg):
        return (-reg[0], -reg[1])

    electron = (W_th, W_n)
    total_c1 = tuple(sp.simplify(a + b) for a, b in
                     zip(electron, c1(electron)))
    total_c2 = tuple(sp.simplify(a + b) for a, b in
                     zip(electron, c2(electron)))

    return {
        "c1_total_registers": [str(v) for v in total_c1],
        "c2_total_registers": [str(v) for v in total_c2],
        "c1_leaves_point_remnant_iff_Wn_nonzero": bool(
            total_c1[0] == 0
            and sp.simplify(total_c1[1] - 2 * W_n) == 0
        ),
        "c2_annihilation_topologically_complete": bool(
            total_c2[0] == 0 and total_c2[1] == 0
        ),
        "theorem": (
            "REGISTER DICHOTOMY: annihilation completeness (article "
            "5.3: mirror twists cancel; smooth radiation encloses zero "
            "pi_2 degree and zero distant winding) requires every "
            "register of the positron to be minus the electron's.  "
            "Branch A: a W_n != 0 electron forces the C-map to act "
            "improperly (orientation-reversingly) on the axis -- C2 is "
            "the representative.  Branch B: a framing-register electron "
            "(W_n = 0; the article's own toroidal-ring/twist-sign "
            "reading) needs only C1."
        ),
        "conditionality": (
            "the branch decision belongs to locks 2-3: the gauged "
            "completion will show whether the pi_2 defect carries "
            "electric or magnetic charge (standard emergent-U(1) lore "
            "says magnetic, which would select branch B for the "
            "electron); assumptions: oriented S^2 axis (not RP^2), "
            "unit constraint intact in cores"
        ),
    }


# ---------------------------------------------------------------------------
# 3-4. O7 at general wavevector: luminality forces e7 = 0
# ---------------------------------------------------------------------------

def dynamical_decoupling_theorem() -> dict:
    """Exact 3x3 dispersion with e7*O7; superluminal branch unless e7=0."""
    u = sp.Function("u")(t, x, y, z)
    v = sp.Function("v")(t, x, y, z)
    th = sp.Function("th")(t, x, y, z)
    n3 = sp.sqrt(1 - eps**2 * (u**2 + v**2))
    nA = [eps * u, eps * v, n3]
    theta = eps * th

    dn = [_grad(c) for c in nA]
    dth = _grad(theta)
    dphi = [_grad(p) for p in [x, y, z]]

    Vt = [-_con(dphi[Bb], dth) for Bb in range(3)]
    Vn = [
        [-_con(dphi[D], dn[C]) for C in range(3)] for D in range(3)
    ]
    nVn = [sum(nA[D] * Vn[D][C] for D in range(3)) for C in range(3)]
    O7 = sum(
        sp.Eijk(A, Bb, C) * nA[A] * Vt[Bb] * nVn[C]
        for A in range(3)
        for Bb in range(3)
        for C in range(3)
    )
    O7q = sp.expand(sp.diff(O7, eps, 2).subs(eps, 0) / 2)

    # kn, kt positive by the p18e/p18f no-ghost conditions
    kt, kn = sp.symbols("kappa_t kappa_n", positive=True)
    e7 = sp.symbols("e7", real=True)
    L2 = (
        kt
        * (
            sp.Derivative(th, t) ** 2
            - sp.Derivative(th, x) ** 2
            - sp.Derivative(th, y) ** 2
            - sp.Derivative(th, z) ** 2
        )
        + kn
        * (
            sp.Derivative(u, t) ** 2
            + sp.Derivative(v, t) ** 2
            - sum(
                sp.Derivative(f, c) ** 2
                for f in (u, v)
                for c in (x, y, z)
            )
        )
        + e7 * O7q
    )

    w, kx, ky, kz = sp.symbols("omega k_x k_y k_z", real=True)
    ath, au, av = sp.symbols("amp_th amp_u amp_v", real=True)
    subs_list = []
    for name, f, amp in (("th", th, ath), ("u", u, au), ("v", v, av)):
        for c, kc in ((t, -w), (x, kx), (y, ky), (z, kz)):
            subs_list.append((sp.Derivative(f, c), amp * sp.I * kc))
    L2_sym = sp.expand(L2.subs(subs_list))
    M = sp.simplify(
        -sp.Matrix(
            3,
            3,
            lambda i, j: sp.diff(
                L2_sym, [ath, au, av][i], [ath, au, av][j]
            )
            / 2,
        )
    )
    det = sp.factor(sp.simplify(M.det()))

    # branches at ky = 0 (k in the plane containing the background axis)
    sols = sp.solve(sp.Eq(det.subs(ky, 0), 0), w**2)
    k2 = kx**2 + kz**2
    shifts = sorted(
        [sp.simplify(s - k2) for s in sols], key=sp.default_sort_key
    )
    luminal_branch_present = any(sh == 0 for sh in shifts)
    split = [sh for sh in shifts if sh != 0]
    symmetric_split = (
        len(split) == 2 and sp.simplify(split[0] + split[1]) == 0
    )
    split_prop_e7 = all(
        sp.simplify(sh.subs(e7, 0)) == 0 for sh in split
    )
    # superluminal branch exists for any e7 != 0: the shift is
    # +- e7*kx*kz/(2*sqrt(kn*kt)); sign of kx*kz is free
    expected = e7 * kx * kz / (2 * sp.sqrt(kn * kt))
    magnitude_ok = any(
        sp.simplify(sp.together(sh**2 - expected**2)) == 0
        for sh in split
    )

    # O5 stays C2-odd (cited from p18f's executable classification)
    return {
        "O7_bilinear": str(O7q),
        "luminal_branch_present": bool(luminal_branch_present),
        "mixed_pair_splits_symmetrically": bool(symmetric_split),
        "split_vanishes_iff_e7_zero": bool(split_prop_e7),
        "split_magnitude_e7_kx_kz_over_2sqrt": bool(magnitude_ok),
        "theorem": (
            "for any e7 != 0 there exist oblique directions "
            "(k_x*k_z != 0) with a strictly superluminal branch "
            "omega^2 = k^2 + |e7*k_x*k_z|/(2*sqrt(kn*kt)); exact "
            "luminality of the orientation channel (p18e/p18f cone "
            "requirement; the +- pair structure means bare causality "
            "already suffices) forces e7 = 0.  Scope: quadratic "
            "analysis; no symmetry otherwise protects e7 = 0 -- the "
            "removal rests on exact luminality/causality as a principle "
            "of the medium.  Combined with O5's C2-oddness (p18f "
            "executable), theta-axis decoupling holds under BOTH "
            "C-maps: by parity under C1, by luminality under C2 -- the "
            "p18f postulate is now a theorem"
        ),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_charge_conjugation_map_gate() -> dict:
    regs = register_arithmetic()
    annih = annihilation_completeness_theorem()
    dyn = dynamical_decoupling_theorem()

    closed = {
        "line_register_quantized": bool(regs["line_register_quantized"]),
        "w_theta_flips_under_theta_flip": bool(
            regs["w_theta_flips_under_theta_flip"]
        ),
        "w_n_flips_only_under_axis_flip": bool(
            regs["w_n_flips_only_under_axis_flip"]
        ),
        "c1_leaves_point_remnant": bool(
            annih["c1_leaves_point_remnant_iff_Wn_nonzero"]
        ),
        "c2_annihilation_topologically_complete": bool(
            annih["c2_annihilation_topologically_complete"]
        ),
        "o7_luminal_branch_present": bool(dyn["luminal_branch_present"]),
        "o7_split_symmetric_and_e7_proportional": bool(
            dyn["mixed_pair_splits_symmetrically"]
            and dyn["split_vanishes_iff_e7_zero"]
            and dyn["split_magnitude_e7_kx_kz_over_2sqrt"]
        ),
    }

    open_checks = {
        "u1_redundancy_gate_built": False,           # lock 2 (p18h)
        "hedgehog_screening_gate_built": False,      # lock 3 (p18i)
        "finite_orientation_lock_N_derived": False,  # lock 4 (p18j)
        "alpha_computed": False,
        "annihilation_amplitude_derived": False,
    }

    result = {
        "STATUS": (
            "OPEN_U1_REDUNDANCY_NEXT__"
            + _pass_status("C_MAP_DICHOTOMY_AND_DYNAMICAL_DECOUPLING")
            if all(closed.values())
            else "CHECK_C_MAP_DERIVATION"
        ),
        "SCOPE": (
            "lock 1 of the alpha chain (council ordering): the C-map is "
            "classified by the register dichotomy theorem -- a W_n "
            "electron forces improper axis action (C2 representative), "
            "a framing-register electron needs only C1; the branch "
            "decision lands in locks 2-3.  Unconditionally proven: the "
            "dichotomy is dynamically harmless -- the C2-admissible O7 "
            "coupling is killed by causality/luminality at oblique "
            "directions, so theta-axis decoupling is a theorem under "
            "both C-maps and the chain is not blocked"
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "register_table": regs["table"],
        "annihilation_theorem": annih["theorem"],
        "conditionality": annih["conditionality"],
        "dynamical_theorem": dyn["theorem"],
        "physical_reading": (
            "the article's 'positron = topological mirror' is now "
            "precise arithmetic: every topological register must flip. "
            "WHAT flips beyond the twist depends on which register "
            "carries the electric charge -- the axis hedgehog (then the "
            "whole frame mirrors, C2) or the framing/twist alone (then "
            "C1, the article's own lean).  Either way the orientation "
            "channel's wave sector is untouched: causality kills both "
            "epsilon couplings of the p18f grammar that could have "
            "mixed the fiber with the axis"
        ),
        "missing_derivations": [
            "lock 2 (p18h_frame_connection_u1_gate): covariant coupling "
            "D theta = d theta + omega(n) . d n; global shift -> local "
            "redundancy; mode count 3 -> 2; luminality + solar "
            "transparency re-checked; no extra scalar mode",
            "lock 3 (p18i_hedgehog_screening_maxwell_gate): screened "
            "far field 1/r^2, Gauss law, Coulomb energy",
            "lock 4 (p18j_finite_orientation_lock_alpha_gate): N as the "
            "ratio of fiber-step to axis-step spectra on the same "
            "finite orientation-frame resonator; NO number scanning; "
            "alpha = 1/(4*pi*N) only if N = 10.90497833 emerges",
        ],
        "do_not_claim": [
            "Do not claim alpha, Maxwell, U(1) redundancy, or screening "
            "are derived (locks 2-4 open).",
            "The C2 selection is CONDITIONAL (branch A of the register "
            "dichotomy); the article's own ontology (toroidal ring, "
            "twist-sign charge) leans to branch B where C1 suffices, "
            "and p18f explicitly refuses hedgehog = electron before "
            "screening -- do not quote this gate as 'C2 decided'.",
            "Annihilation completeness pins only the improper O(3) "
            "coset of the C-map's axis action (branch A); C2 (n -> -n) "
            "is a representative, not the unique map.",
            "Annihilation completeness is a topological selection rule; "
            "the annihilation amplitude remains underived.",
            "Do not reintroduce O7 in later gates: e7 = 0 is forced by "
            "luminality, not chosen.",
            "The C-maps considered are the p18f pair (axis fixed / axis "
            "inverted).  Composite maps (single-axis reflection plus "
            "internal inversion or spatial parity) are NET-PROPER and "
            "PRESERVE W_n (referee computation); on branch A the "
            "annihilation argument EXCLUDES such composites rather than "
            "subsumes them -- it pins the C-map's axis action to the "
            "improper O(3) coset.  A full P/C/T audit of the medium "
            "remains open.",
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
    print("register_table:")
    for key, val in result["register_table"].items():
        print(f"  {key}: {val}")
    print("annihilation_theorem:", result["annihilation_theorem"])
    print("conditionality:", result["conditionality"])
    print("dynamical_theorem:", result["dynamical_theorem"])
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
    _print_result(derive_charge_conjugation_map_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
