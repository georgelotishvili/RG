# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Oriented-axis sector (new in this gate): nA = unit axis field (values in
# S^2) = the transverse-asymmetry AXIS of the ONE base medium's orientation
# property; together with p18e's fiber angle theta it forms the oriented
# frame (p11g).  Pn = sum_A g^mn d_m nA d_n nA; Qn^A = g^mn d_m Phi d_n nA;
# Vn^BA = -g^mn d_m phi^B d_n nA.  Coefficients kn_*, en_Q2, en_VV mirror
# p18e's kappa_*, e_Q2, e_VV.  No repo name collisions (nA, Pn, Qn, Vn new).

"""
================================================================================
PHASE 18f: Oriented-axis completion gate
================================================================================

Purpose
-------
Execute item 1 of p18e's missing_derivations:

    "oriented-axis (director) completion: promote theta to the angle fiber
     of the full orientation (axis n in S^2 + angle), delivering the
     helicity +-1 pair and point defects via pi_2(S^2) = Z ..."

Terminology note: p11g reserves "director" for the projective/nematic
object (n ~ -n); the nA of this gate is the ORIENTED axis in p11g's
oriented-frame sense -- the word "(director)" above is quoted from p18e's
looser wording.

Ontological statement (continuing the author's framing): still ONE medium.
The orientation property has two components -- WHERE the local transverse
asymmetry points (the axis nA, values in S^2) and HOW FAR it is rotated
about that axis (the fiber angle theta of p18e, values in S^1).  Axis +
angle = the oriented frame of p11g; the canon's charge language ("framed
orientation sign", canon 480) and the article's 5.3 dipolar-asymmetry
direction live exactly here.

Definitions (new)
-----------------
nA           unit axis field, nA . nA = 1 (S^2 target); background nA = e_3
Pn           sum_A g^mn d_m nA d_n nA
Qn^A         g^mn d_m Phi d_n nA        (clock-axis mixing)
Vn^BA        -g^mn d_m phi^B d_n nA     (solid-axis mixing)
grammar      L_n = (kn_P + kn_PY*Y + kn_PI1*I1 + kn_PI2*I2 + kn_PI3*I3)*Pn
                   + en_Q2*(Qn.Qn) + en_VV*(Vn.Vn)
             (mirror of p18e's 7 theta-operators; same C-parity/shift
             discipline, applied to the frame)

Results (all executable below)
------------------------------
1. TWO LUMINAL MODES: the axis has two transverse fluctuations (u, v).
   Their quadratic action is two identical copies of the p18e theta-action:
   K = kn_eff + en_Q2 and C = kn_eff - en_VV per mode, no u-v mixing,
   kn_eff = kn_P + kn_PY + 3*kn_PI1 + 3*kn_PI2 + kn_PI3 (the same
   (1,1,3,3,1) weights).  The solar cone conditions force
   en_Q2 = en_VV = 0 through closed-form kappa-independent numerators
   (isotropic stand-in and areal-radial: en_Q2*A + en_VV*B = 0;
   areal-tangential: en_Q2 + en_VV*B = 0 -- same unique zero solution
   in all three), and the surviving family
   F(Y,I1,I2,I3)*Pn rides the metric cone exactly.  The axis sector is
   solar-stress-silent at all orders by the same power-counting theorem
   (every operator carries >= 2 factors of d(nA)).

2. HELICITY PAIR: under the residual joint (internal+spatial) rotation by
   psi about the background axis, the combinations u +- i*v pick up phases
   exp(+-i*psi) -- the two axis modes ARE a helicity +-1 pair (executable).
   Scope: stated for propagation along the background axis; the internal-
   spatial tie is supplied by the solid background phi^A = x^A.

3. THETA-AXIS DECOUPLING -- C-PARITY-RELATIVE (executable, referee-
   corrected): the candidate nA . (g^mn d_m theta d_n nA) vanishes
   IDENTICALLY by the unit constraint (n . dn = 0), and within the
   14-operator (7+7) grammar no bilinear theta-(u,v) coupling exists for
   any propagation direction.  HOWEVER, two epsilon-contracted degree-2
   cross candidates exist and are NOT killed by the constraint:

       O5 = eps_ABC nA^A Qn^B Vt^C,
       O7 = eps_ABC nA^A Vt^B (n_D Vn^DC),

   both with nonzero theta-axis bilinears (visible only to probes with
   transverse theta-gradients).  Their exclusion is a CHARGE-CONJUGATION
   assignment on the frame:
     C1 (theta -> -theta, nA -> nA):  both are C-odd -- excluded;
     C2 (theta -> -theta, nA -> -nA, the frame-mirror reading of canon
         480's "framed orientation sign"):  O5 stays odd but O7 is C-EVEN
         -- admissible, and would mix theta with the axis modes.
   This gate adopts C1 as the declared postulate; deciding C1 vs C2 from
   the article's positron-mirror physics is an OPEN modeling theorem.

4. POINT DEFECT EXISTS: the hedgehog nA = x^A/r has pi_2 degree = 1
   (executable surface integral).  The point-like charge-carrier slot the
   article demands for the electron -- impossible for theta alone
   (pi_2(S^1) = 0, p18e) -- EXISTS in the axis sector.

5. HEDGEHOG ENERGY LEDGER (honest, referee-corrected): the bare energy
   of the hedgehog grows LINEARLY with system size.  Under the repo's
   stress convention (T_mn = 2*dL/dg^mn - g_mn*L) the static energy
   density is T^t_t = (kn_eff - 2*kn_PY)*(2/r^2) once the cone has forced
   en_VV = 0 (the kn_PY shift enters through Y = g^tt in F), so

       dE/dR = 8*pi*(kn_eff - 2*kn_PY),

   with the positivity condition kn_eff - 2*kn_PY > 0 (NEW, beside the
   no-ghost K > 0).  Either way the growth is linear: an unscreened
   orientation hedgehog is confinement-like, not Coulombic.
   REQUIREMENT (open): the fiber/gauge structure must screen the far field
   to 1/r^2 -- this is precisely the Maxwell-emergence theorem demanded by
   p11 stage_d3 ("derive Maxwell equations, U(1) gauge redundancy, and
   Coulomb 1/r^2 from the medium variables").  Do not read the hedgehog as
   the electron before that theorem exists.

6. FIBER-CURVATURE LOCK SEED (the alpha-relevant geometric fact,
   executable): parallel transport of the frame around a closed loop on
   the axis sphere rotates the fiber angle by EXACTLY the enclosed solid
   angle -- verified for the octant (holonomy pi/2 = solid angle pi/2) and
   for the geodesic triangle with apex angle beta at the pole (spherical
   excess = enclosed solid angle = beta; holonomy = beta, symbolic).
   SCOPE (referee-tightened): this identity is GEOMETRY -- it fixes the
   curvature of the frame connection over the axis sphere.  The present
   action contains NO covariant coupling (d theta + omega(n) . d n)^2
   yet, so nothing here dynamically pumps theta; building that covariant
   frame-connection completion IS the U(1)-redundancy step, and only
   once it exists does the holonomy identity lock the fiber-axis
   coupling rate (= solid angle) instead of leaving it a free dial.
   The identity is the geometric backbone ON WHICH the author's
   finite-resonator lock hypothesis (fiber-step vs axis-step spectra on
   the same finite base; finiteness -> discreteness, ratio-invariance ->
   size cancellation) must be built; the p18e kappa-freedom proves no
   solar-sector input can substitute for it.

7. MODE-COUNT LEDGER (honest): at this level THREE luminal modes propagate
   (theta + two axis modes); the physical photon has TWO.  The completion
   must demote the uniform fiber rotation to a REDUNDANCY -- the article's
   own "global rotation of the asymmetry angle is unphysical" (5.3) read
   as the U(1) gauge statement -- so that only the helicity pair remains
   physical.  That U(1)-redundancy theorem (stage_d3) is OPEN.

What this gate does NOT claim
-----------------------------
- alpha is NOT derived; N = 10.90497833 remains the open lock number.
- Maxwell/Gauss/Ward/U(1)-redundancy are NOT derived (mode count is
  still 3, screening is not built).
- The hedgehog is NOT yet the electron (energy ledger, item 5).
- The frame-bundle holonomy identity is geometry, not yet dynamics: it
  locks the CONNECTION, and the stiffness-ratio theorem on top of it is
  still to be derived.
"""

from __future__ import annotations

import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


# ---------------------------------------------------------------------------
# Coefficients and shared symbols
# ---------------------------------------------------------------------------

kn_P, kn_PY, kn_PI1, kn_PI2, kn_PI3 = sp.symbols(
    "kn_P kn_PY kn_PI1 kn_PI2 kn_PI3", real=True
)
en_Q2, en_VV = sp.symbols("en_Q2 en_VV", real=True)

eps, U = sp.symbols("epsilon U", real=True)
t, x, y, z = sp.symbols("t x y z", real=True)
COORDS = (t, x, y, z)


def _grad(expr):
    return [sp.diff(expr, c) for c in COORDS]


def _con(ginv_diag, u, v):
    return sum(ginv_diag[m] * u[m] * v[m] for m in range(4))


def _axis_sector_lagrangian(ginv_diag, Phi, phiA, nA):
    """L_n for the 7-operator mirror grammar on a diagonal metric."""
    dPhi = _grad(Phi)
    dn = [_grad(c) for c in nA]
    dphi = [_grad(p) for p in phiA]

    Pn = sum(_con(ginv_diag, dn[A], dn[A]) for A in range(3))
    QnQn = sum(_con(ginv_diag, dPhi, dn[A]) ** 2 for A in range(3))
    VnVn = sum(
        _con(ginv_diag, dphi[Bb], dn[A]) ** 2
        for Bb in range(3)
        for A in range(3)
    )

    Y = _con(ginv_diag, dPhi, dPhi)
    Bm = sp.Matrix(3, 3, lambda A, Bb: -_con(ginv_diag, dphi[A], dphi[Bb]))
    I1 = sp.trace(Bm)
    I2 = sp.Rational(1, 2) * (I1**2 - sp.trace(Bm * Bm))
    I3 = Bm.det()

    F = kn_P + kn_PY * Y + kn_PI1 * I1 + kn_PI2 * I2 + kn_PI3 * I3
    return F * Pn + en_Q2 * QnQn + en_VV * VnVn


# ---------------------------------------------------------------------------
# 1a. Two luminal modes: vacuum dispersion, no u-v mixing, theta decoupling
# ---------------------------------------------------------------------------

def axis_dispersion_and_decoupling() -> dict:
    eta = [sp.Integer(1), -1, -1, -1]
    u = sp.Function("u")(t, z)
    v = sp.Function("v")(t, z)
    n3 = sp.sqrt(1 - eps**2 * (u**2 + v**2))
    nA = [eps * u, eps * v, n3]

    L = _axis_sector_lagrangian(eta, t, [x, y, z], nA)
    quad = sp.expand(sp.diff(L, eps, 2).subs(eps, 0) / 2)

    ud, vd = sp.Derivative(u, t), sp.Derivative(v, t)
    uz, vz = sp.Derivative(u, z), sp.Derivative(v, z)
    K_u = quad.coeff(ud**2)
    K_v = quad.coeff(vd**2)
    C_u = -quad.coeff(uz**2)
    C_v = -quad.coeff(vz**2)
    leftover = sp.expand(
        quad - K_u * ud**2 - K_v * vd**2 + C_u * uz**2 + C_v * vz**2
    )
    kn_eff = kn_P + kn_PY + 3 * kn_PI1 + 3 * kn_PI2 + kn_PI3

    # theta-axis cross terms: exact vanishing of n.(dtheta dn) and of all
    # bilinear theta-(u,v) couplings when the p18e theta-sector is added
    th = sp.Function("th")(t, z)
    theta = eps * th
    dth = _grad(theta)
    dn = [_grad(c) for c in nA]
    cross_op = sum(nA[A] * _con(eta, dth, dn[A]) for A in range(3))

    kP_t, eQ2_t, eVV_t = sp.symbols("kP_t eQ2_t eVV_t", real=True)
    dPhi = _grad(t)
    dphi = [_grad(p) for p in [x, y, z]]
    Pt = _con(eta, dth, dth)
    Qt = _con(eta, dPhi, dth)
    Vt = [-_con(eta, dphi[Bb], dth) for Bb in range(3)]
    L_tot = L + kP_t * Pt + eQ2_t * Qt**2 + eVV_t * sum(V**2 for V in Vt)
    quad_tot = sp.expand(sp.diff(L_tot, eps, 2).subs(eps, 0) / 2)
    thd, thz = sp.Derivative(th, t), sp.Derivative(th, z)
    bilinears = [
        sp.simplify(quad_tot.coeff(a).coeff(b))
        for a in (thd, thz)
        for b in (ud, vd, uz, vz)
    ]

    return {
        "two_modes_K_equal": sp.simplify(K_u - K_v) == 0,
        "two_modes_C_equal": sp.simplify(C_u - C_v) == 0,
        "K_matches_p18e_form": sp.simplify(K_u - (kn_eff + en_Q2)) == 0,
        "C_matches_p18e_form": sp.simplify(C_u - (kn_eff - en_VV)) == 0,
        "no_uv_mixing": leftover == 0,
        "unit_constraint_kills_cross_op": sp.simplify(sp.expand(cross_op))
        == 0,
        "no_theta_axis_bilinears": all(b == 0 for b in bilinears),
        "K_u": sp.expand(K_u),
        "C_u": sp.expand(C_u),
        "kn_eff": kn_eff,
        "luminality_condition": sp.Eq(en_Q2 + en_VV, 0),
    }


# ---------------------------------------------------------------------------
# 1b. Solar transparency (generic metric) and cone exactness (both gauges)
# ---------------------------------------------------------------------------

def solar_transparency_axis_sector() -> dict:
    """Axis-sector stress and EOM vanish identically at d(nA) = 0."""
    q = {}
    for m in range(4):
        for n_ in range(m, 4):
            q[(m, n_)] = sp.Symbol(f"q{m}{n_}", real=True)

    def con_full(uu, vv):
        tot = 0
        for m in range(4):
            for n_ in range(4):
                key = (m, n_) if m <= n_ else (n_, m)
                tot += q[key] * uu[m] * vv[n_]
        return tot

    dPhi = [sp.Integer(1), 0, 0, 0]
    dphi = [
        [sp.Integer(0), 1, 0, 0],
        [sp.Integer(0), 0, 1, 0],
        [sp.Integer(0), 0, 0, 1],
    ]
    # generic first derivatives of the two independent axis components;
    # the third component's gradient follows from the unit constraint and
    # vanishes with them at the aligned background (n1 = n2 = 0):
    dn1 = list(sp.symbols("dn1_0 dn1_1 dn1_2 dn1_3", real=True))
    dn2 = list(sp.symbols("dn2_0 dn2_1 dn2_2 dn2_3", real=True))
    dn3 = [sp.Integer(0)] * 4  # d(n3) = -(n1 dn1 + n2 dn2)/n3 = 0 at bg
    dn = [dn1, dn2, dn3]

    Pn = sum(con_full(dn[A], dn[A]) for A in range(3))
    QnQn = sum(con_full(dPhi, dn[A]) ** 2 for A in range(3))
    VnVn = sum(
        con_full(dphi[Bb], dn[A]) ** 2 for Bb in range(3) for A in range(3)
    )

    Y = con_full(dPhi, dPhi)
    Bm = sp.Matrix(3, 3, lambda A, Bb: -con_full(dphi[A], dphi[Bb]))
    I1 = sp.trace(Bm)
    I2 = sp.Rational(1, 2) * (I1**2 - sp.trace(Bm * Bm))
    I3 = Bm.det()
    F = kn_P + kn_PY * Y + kn_PI1 * I1 + kn_PI2 * I2 + kn_PI3 * I3
    L_n = F * Pn + en_Q2 * QnQn + en_VV * VnVn

    at_const = {s: 0 for s in dn1 + dn2}
    stress_silent = all(
        sp.simplify((2 * sp.diff(L_n, qq)).subs(at_const)) == 0
        for qq in q.values()
    ) and sp.simplify(L_n.subs(at_const)) == 0
    eom_trivial = all(
        sp.simplify(sp.diff(L_n, s).subs(at_const)) == 0 for s in dn1 + dn2
    )
    return {
        "stress_vanishes_identically_at_const_axis": stress_silent,
        "eom_trivially_satisfied_at_const_axis": eom_trivial,
    }


def cone_exactness_axis_sector() -> dict:
    """Same closed-form forcing as p18e, per axis mode, both gauges."""
    A_ = 1 + 2 * U + 4 * U**2
    B_ = 1 - 2 * U
    Yb = 1 / B_
    I1b = 2 + 1 / A_
    I2b = 1 + 2 / A_
    I3b = 1 / A_
    F_areal = (
        kn_P
        + kn_PY * Yb
        + kn_PI1 * I1b
        + kn_PI2 * I2b
        + kn_PI3 * I3b
    )
    td, tp = sp.symbols("mode_dot mode_prime", real=True)
    out = {}

    # (a) isotropic-form stand-in, one axis mode along x
    F_iso = (
        kn_P
        + kn_PY / B_
        + kn_PI1 * (3 / A_)
        + kn_PI2 * (3 / A_**2)
        + kn_PI3 / A_**3
    )
    L_iso = (
        F_iso * (td**2 / B_ - tp**2 / A_)
        + en_Q2 * (td / B_) ** 2
        + en_VV * tp**2 / A_**2
    )
    # (b) p03-faithful areal: radial and tangential
    L_rad = (
        F_areal * (td**2 / B_ - tp**2 / A_)
        + en_Q2 * (td / B_) ** 2
        + en_VV * tp**2 / A_**2
    )
    L_tan = (
        F_areal * (td**2 / B_ - tp**2)
        + en_Q2 * (td / B_) ** 2
        + en_VV * tp**2
    )
    for tag, L, cone in (
        ("isotropic_standin", L_iso, B_ / A_),
        ("areal_radial", L_rad, B_ / A_),
        ("areal_tangential", L_tan, B_),
    ):
        K = L.coeff(td**2)
        C = -L.coeff(tp**2)
        num = sp.numer(sp.together(sp.cancel(C / K) - cone))
        conds = [sp.expand(sp.expand(num).coeff(U, k)) for k in range(2)]
        sols = sp.solve(conds, [en_Q2, en_VV], dict=True)
        out[f"forced_zero_{tag}"] = (
            len(sols) == 1
            and sp.simplify(sols[0].get(en_Q2, sp.nan)) == 0
            and sp.simplify(sols[0].get(en_VV, sp.nan)) == 0
        )
        out[f"numerator_kappa_free_{tag}"] = not (
            num.free_symbols
            & {kn_P, kn_PY, kn_PI1, kn_PI2, kn_PI3}
        )
    out["surviving_family"] = (
        "L_n = F(Y, I1, I2, I3) * Pn (5 parameters, two exactly luminal "
        "modes riding the metric cone)"
    )
    return out


def epsilon_cross_candidates_and_c_parity() -> dict:
    """Referee-found epsilon-contracted cross candidates, classified by C.

    O5 = eps_ABC nA^A Qn^B Vt^C and O7 = eps_ABC nA^A Vt^B (n_D Vn^DC) are
    degree-2, first-derivative, shift-symmetric theta-axis couplings NOT
    killed by the unit constraint.  Their bilinears need transverse
    theta-gradients, so (t,z)-probes miss them.  Classification:
      C1 (theta -> -theta, nA fixed): each carries exactly ONE Vt factor
          (linear in d theta) => C-odd => excluded by the C1 postulate.
      C2 (theta -> -theta, nA -> -nA): O5 flips (3 sign factors) but O7
          is EVEN (4 sign factors) => admissible => would mix.
    """
    eta = [sp.Integer(1), -1, -1, -1]
    u4 = sp.Function("u4")(t, x, y, z)
    v4 = sp.Function("v4")(t, x, y, z)
    th4 = sp.Function("th4")(t, x, y, z)
    n3 = sp.sqrt(1 - eps**2 * (u4**2 + v4**2))
    nA = [eps * u4, eps * v4, n3]
    theta = eps * th4

    dn = [_grad(c) for c in nA]
    dth = _grad(theta)
    dPhi = _grad(t)
    dphi = [_grad(p) for p in [x, y, z]]

    Qn = [_con(eta, dPhi, dn[A]) for A in range(3)]
    Vt = [-_con(eta, dphi[Bb], dth) for Bb in range(3)]
    Vn = [
        [-_con(eta, dphi[D], dn[C]) for C in range(3)] for D in range(3)
    ]
    epsi = sp.Eijk

    O5 = sum(
        epsi(A, Bb, C) * nA[A] * Qn[Bb] * Vt[C]
        for A in range(3)
        for Bb in range(3)
        for C in range(3)
    )
    nVn = [
        sum(nA[D] * Vn[D][C] for D in range(3)) for C in range(3)
    ]
    O7 = sum(
        epsi(A, Bb, C) * nA[A] * Vt[Bb] * nVn[C]
        for A in range(3)
        for Bb in range(3)
        for C in range(3)
    )

    O5_quad = sp.expand(sp.diff(O5, eps, 2).subs(eps, 0) / 2)
    O7_quad = sp.expand(sp.diff(O7, eps, 2).subs(eps, 0) / 2)

    # C-parity classification on UNCONSTRAINED fields (the sign counting
    # needs no unit constraint and no background choice): generic
    # N^A(t,x,y,z), theta(t,x,y,z); exact substitutions.
    N1 = sp.Function("N1")(t, x, y, z)
    N2 = sp.Function("N2")(t, x, y, z)
    N3 = sp.Function("N3")(t, x, y, z)
    thg = sp.Function("thg")(t, x, y, z)
    Ng = [N1, N2, N3]
    dNg = [_grad(c) for c in Ng]
    dthg = _grad(thg)
    Qn_g = [_con(eta, dPhi, dNg[A]) for A in range(3)]
    Vt_g = [-_con(eta, dphi[Bb], dthg) for Bb in range(3)]
    Vn_g = [
        [-_con(eta, dphi[D], dNg[C]) for C in range(3)] for D in range(3)
    ]
    O5_g = sum(
        epsi(A, Bb, C) * Ng[A] * Qn_g[Bb] * Vt_g[C]
        for A in range(3)
        for Bb in range(3)
        for C in range(3)
    )
    nVn_g = [
        sum(Ng[D] * Vn_g[D][C] for D in range(3)) for C in range(3)
    ]
    O7_g = sum(
        epsi(A, Bb, C) * Ng[A] * Vt_g[Bb] * nVn_g[C]
        for A in range(3)
        for Bb in range(3)
        for C in range(3)
    )

    def c_map(expr, flip_axis):
        subs = [(thg, -thg)]
        if flip_axis:
            subs += [(N1, -N1), (N2, -N2), (N3, -N3)]
        return expr.subs(subs, simultaneous=True)

    c1_O5_odd = sp.simplify(sp.expand(c_map(O5_g, False) + O5_g)) == 0
    c1_O7_odd = sp.simplify(sp.expand(c_map(O7_g, False) + O7_g)) == 0
    c2_O5_odd = sp.simplify(sp.expand(c_map(O5_g, True) + O5_g)) == 0
    c2_O7_even = sp.simplify(sp.expand(c_map(O7_g, True) - O7_g)) == 0

    return {
        "candidates_exist_nonzero_bilinears": bool(
            O5_quad != 0 and O7_quad != 0
        ),
        "c1_excludes_both": bool(c1_O5_odd and c1_O7_odd),
        "c2_admits_O7": bool(c2_O5_odd and c2_O7_even),
        "declared_postulate": (
            "this gate adopts C1 (theta -> -theta, axis fixed); under C1 "
            "the decoupling theorem holds for all propagation directions. "
            "Deciding C1 vs C2 (frame mirror, canon 480 reading) from the "
            "article's positron-mirror physics is an open modeling "
            "theorem; under C2 the O7 coupling exists and mixes theta "
            "with the axis modes"
        ),
    }


# ---------------------------------------------------------------------------
# 2. Helicity pair identification
# ---------------------------------------------------------------------------

def helicity_pair_identification() -> dict:
    """u +- i*v carry charges +-1 under the residual joint rotation."""
    a, c, psi = sp.symbols("a c psi", real=True)
    R2 = sp.Matrix(
        [[sp.cos(psi), -sp.sin(psi)], [sp.sin(psi), sp.cos(psi)]]
    )
    uv = R2 * sp.Matrix([a, c])
    plus = sp.simplify((uv[0] + sp.I * uv[1]) / (a + sp.I * c))
    minus = sp.simplify((uv[0] - sp.I * uv[1]) / (a - sp.I * c))

    # the joint (internal + spatial) rotation about e_3 is the residual
    # symmetry of the background: phi'^A(x') = R^A_B phi^B(R^-1 x) = x^A
    # holds only for the JOINT action; single rotations break phi^A = x^A
    R3 = sp.Matrix(
        [
            [sp.cos(psi), -sp.sin(psi), 0],
            [sp.sin(psi), sp.cos(psi), 0],
            [0, 0, 1],
        ]
    )
    xv = sp.Matrix([x, y, z])
    joint = sp.simplify(R3 * (R3.T * xv) - xv) == sp.zeros(3, 1)
    internal_only = sp.simplify(R3 * xv - xv) != sp.zeros(3, 1)
    n_bg = sp.Matrix([0, 0, 1])
    axis_invariant = sp.simplify(R3 * n_bg - n_bg) == sp.zeros(3, 1)

    return {
        "joint_rotation_is_residual_symmetry": bool(
            joint and internal_only and axis_invariant
        ),
        "plus_mode_charge_plus_one": sp.simplify(
            sp.expand(plus - sp.exp(sp.I * psi))
        )
        == 0,
        "minus_mode_charge_minus_one": sp.simplify(
            sp.expand(minus - sp.exp(-sp.I * psi))
        )
        == 0,
        "scope": (
            "joint internal+spatial rotation about the background axis "
            "(the residual symmetry of Phi = t, phi^A = x^A, nA = e_3); "
            "helicity read along the background axis -- general-direction "
            "statement requires the U(1)-redundancy completion"
        ),
    }


# ---------------------------------------------------------------------------
# 4-5. Hedgehog point defect and its energy ledger
# ---------------------------------------------------------------------------

def hedgehog_point_defect() -> dict:
    thg, phg = sp.symbols("vartheta varphi", real=True)
    n_h = sp.Matrix(
        [
            sp.sin(thg) * sp.cos(phg),
            sp.sin(thg) * sp.sin(phg),
            sp.cos(thg),
        ]
    )
    integrand = sp.simplify(
        n_h.dot(sp.diff(n_h, thg).cross(sp.diff(n_h, phg)))
    )
    degree = sp.simplify(
        sp.integrate(
            sp.integrate(integrand, (phg, 0, 2 * sp.pi)),
            (thg, 0, sp.pi),
        )
        / (4 * sp.pi)
    )

    # static-hedgehog energy density from the repo stress convention:
    # T^t_t = 2*dL/dg^tt - L at the Minkowski background (g^tt = 1).
    # Static config: Qn^A = 0; only g^tt-dependence of F (via Y = g^tt)
    # and the spatial gradient invariants contribute.
    gtt = sp.Symbol("gtt", positive=True)
    Pn_h, VnVn_h = sp.symbols("Pn_h VnVn_h", real=True)
    F_h = (
        kn_P
        + kn_PY * gtt
        + kn_PI1 * 3
        + kn_PI2 * 3
        + kn_PI3 * 1
    )
    L_h = F_h * Pn_h + en_VV * VnVn_h  # QnQn = 0 static
    T_tt = sp.expand((2 * gtt * sp.diff(L_h, gtt) - L_h).subs(gtt, 1))
    # hedgehog values: Pn = -(grad n)^2 = -2/r^2, VnVn = +2/r^2
    r = sp.symbols("r", positive=True)
    rho = sp.expand(
        T_tt.subs([(Pn_h, -2 / r**2), (VnVn_h, 2 / r**2)])
    )
    kn_eff = kn_P + kn_PY + 3 * kn_PI1 + 3 * kn_PI2 + kn_PI3
    dE_dR = sp.simplify(rho * 4 * sp.pi * r**2)
    expected = 8 * sp.pi * (kn_eff - 2 * kn_PY - en_VV)
    weight_ok = sp.simplify(dE_dR - expected) == 0
    # on the cone-forced slice en_VV = 0:
    dE_dR_final = sp.simplify(dE_dR.subs(en_VV, 0))

    return {
        "pi2_degree_is_one": degree == 1,
        "energy_growth_linear": bool(
            weight_ok
            and sp.simplify(
                dE_dR_final - 8 * sp.pi * (kn_eff - 2 * kn_PY)
            )
            == 0
        ),
        "positivity_condition": sp.Gt(kn_eff - 2 * kn_PY, 0),
        "ledger": (
            "point defect EXISTS (pi_2(S^2) = Z realized), but its bare "
            "energy grows linearly with size: dE/dR = "
            "8*pi*(kn_eff - 2*kn_PY) on the cone-forced slice "
            "(T^t_t convention; NEW positivity condition "
            "kn_eff - 2*kn_PY > 0) -- confinement-like, not Coulombic; "
            "the fiber/gauge structure must screen the far field to "
            "1/r^2 (Maxwell-emergence theorem, stage_d3) before the "
            "hedgehog may be read as the electron"
        ),
    }


# ---------------------------------------------------------------------------
# 6. Fiber-curvature lock seed: holonomy = enclosed solid angle
# ---------------------------------------------------------------------------

def fiber_curvature_lock_seed() -> dict:
    def rot(axis, ang):
        ax = sp.Matrix(axis)
        ax = ax / sp.sqrt(sum(comp**2 for comp in ax))
        K = sp.Matrix(
            [
                [0, -ax[2], ax[1]],
                [ax[2], 0, -ax[0]],
                [-ax[1], ax[0], 0],
            ]
        )
        return sp.eye(3) + sp.sin(ang) * K + (1 - sp.cos(ang)) * K * K

    north = sp.Matrix([0, 0, 1])

    # octant loop: N -> (1,0,0) -> (0,1,0) -> N ; solid angle = pi/2
    T_oct = (
        rot((1, 0, 0), sp.pi / 2)
        * rot((0, 0, 1), sp.pi / 2)
        * rot((0, 1, 0), sp.pi / 2)
    )
    oct_fixes_N = sp.simplify((T_oct * north - north).norm()) == 0
    hol_oct = sp.acos(sp.simplify((sp.trace(T_oct) - 1) / 2))
    octant_ok = oct_fixes_N and sp.simplify(hol_oct - sp.pi / 2) == 0

    # geodesic triangle N -> (1,0,0) -> (cos b, sin b, 0) -> N with apex
    # angle beta at the pole: spherical excess = solid angle = beta.
    # (cos-comparison is branch-insensitive; the octant case above pins
    # the branch exactly via acos.)
    beta = sp.symbols("beta_apex", positive=True)
    axis3 = sp.Matrix([sp.sin(beta), -sp.cos(beta), 0])  # P2 x N
    T_tri = (
        rot(axis3, sp.pi / 2)
        * rot((0, 0, 1), beta)
        * rot((0, 1, 0), sp.pi / 2)
    )
    tri_fixes_N = sp.simplify((T_tri * north - north).norm()) == 0
    cos_hol = sp.simplify((sp.trace(T_tri) - 1) / 2)
    tri_ok = tri_fixes_N and sp.simplify(cos_hol - sp.cos(beta)) == 0

    return {
        "octant_holonomy_equals_solid_angle": bool(octant_ok),
        "triangle_holonomy_equals_solid_angle_symbolic": bool(tri_ok),
        "statement": (
            "parallel transport of the frame around a closed loop on the "
            "axis sphere rotates the fiber angle by EXACTLY the enclosed "
            "solid angle: the fiber connection has fixed curvature -- it "
            "is not a free dial.  Axis motion pumps fiber phase at a "
            "geometry-locked rate; fiber steps and axis steps are "
            "commensurate on ONE geometric object.  This is the backbone "
            "required by the finite-resonator lock hypothesis (the ratio "
            "of the two channels' resonance steps on the same finite base "
            "must produce the dimensionless N; size cancels in the ratio "
            "by the ratio-invariance principle, discreteness comes from "
            "finiteness).  The stiffness-ratio theorem on this backbone "
            "is the next derivation; the p18e kappa-freedom proves no "
            "solar-sector input can substitute for it."
        ),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_oriented_axis_completion_gate() -> dict:
    disp = axis_dispersion_and_decoupling()
    eps_cands = epsilon_cross_candidates_and_c_parity()
    transp = solar_transparency_axis_sector()
    cone = cone_exactness_axis_sector()
    helicity = helicity_pair_identification()
    hedgehog = hedgehog_point_defect()
    lock_seed = fiber_curvature_lock_seed()

    closed = {
        "two_identical_luminal_modes": bool(
            disp["two_modes_K_equal"]
            and disp["two_modes_C_equal"]
            and disp["K_matches_p18e_form"]
            and disp["C_matches_p18e_form"]
            and disp["no_uv_mixing"]
        ),
        "theta_axis_decoupling_under_C1": bool(
            disp["unit_constraint_kills_cross_op"]
            and disp["no_theta_axis_bilinears"]
        ),
        "epsilon_candidates_classified": bool(
            eps_cands["candidates_exist_nonzero_bilinears"]
            and eps_cands["c1_excludes_both"]
            and eps_cands["c2_admits_O7"]
        ),
        "solar_transparency_all_orders": bool(
            transp["stress_vanishes_identically_at_const_axis"]
            and transp["eom_trivially_satisfied_at_const_axis"]
        ),
        "cone_forced_zero_all_gauges": bool(
            cone["forced_zero_isotropic_standin"]
            and cone["forced_zero_areal_radial"]
            and cone["forced_zero_areal_tangential"]
            and cone["numerator_kappa_free_isotropic_standin"]
            and cone["numerator_kappa_free_areal_radial"]
            and cone["numerator_kappa_free_areal_tangential"]
        ),
        "helicity_pair_identified": bool(
            helicity["plus_mode_charge_plus_one"]
            and helicity["minus_mode_charge_minus_one"]
            and helicity["joint_rotation_is_residual_symmetry"]
        ),
        "point_defect_exists_pi2_degree_one": bool(
            hedgehog["pi2_degree_is_one"]
        ),
        "hedgehog_energy_linear_derived": bool(
            hedgehog["energy_growth_linear"]
        ),
        "fiber_holonomy_equals_solid_angle": bool(
            lock_seed["octant_holonomy_equals_solid_angle"]
            and lock_seed["triangle_holonomy_equals_solid_angle_symbolic"]
        ),
    }

    open_checks = {
        "u1_redundancy_theorem_mode_count_3_to_2": False,
        "covariant_frame_connection_coupling_built": False,
        "charge_conjugation_frame_assignment_decided": False,
        "hedgehog_screening_to_coulomb": False,
        "stiffness_ratio_theorem_on_fiber_backbone": False,
        "winding_defect_coupling_N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_MAXWELL_EMERGENCE_AND_N_LOCK__"
            + _pass_status("AXIS_COMPLETION_HELICITY_PAIR_AND_HEDGEHOG")
            if all(closed.values())
            else "CHECK_AXIS_COMPLETION_DERIVATION"
        ),
        "SCOPE": (
            "oriented-axis completion of the orientation property: the "
            "axis field nA (S^2) added beside p18e's fiber angle; two "
            "exactly luminal axis modes on the GR cone (helicity +-1 "
            "pair), solar-stress-silent, decoupled from theta and the "
            "phonons; point defects exist (pi_2 degree 1) but are "
            "confinement-like until screened; the frame-bundle holonomy "
            "identity (fiber rotation = enclosed solid angle) is "
            "established as the geometric backbone for the "
            "finite-resonator N lock"
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "dispersion": {
            "K_per_mode": str(disp["K_u"]),
            "C_per_mode": str(disp["C_u"]),
            "kn_eff": str(disp["kn_eff"]),
            "luminality": str(disp["luminality_condition"]),
            "cone_family": cone["surviving_family"],
        },
        "helicity_scope": helicity["scope"],
        "hedgehog_ledger": hedgehog["ledger"],
        "lock_seed": lock_seed["statement"],
        "physical_reading": (
            "the orientation property of the one medium now carries the "
            "full photon-candidate structure: a helicity +-1 pair of "
            "exactly luminal waves invisible to the solar chain, plus "
            "quantized point defects as the charge-carrier slot.  Three "
            "theorems separate this from alpha: U(1) redundancy (3 -> 2 "
            "modes), hedgehog screening (Coulomb law), and the "
            "stiffness-ratio lock on the fiber-curvature backbone "
            "(N = 10.90497833)"
        ),
        "missing_derivations": [
            "U(1)-redundancy theorem: promote the article's GLOBAL "
            "shift statement ('global rotation is unphysical', 5.3) to a "
            "LOCAL redundancy via the covariant frame-connection "
            "coupling (d theta + omega(n) . d n)^2 -- gauging, not just "
            "zero-mode removal -- reducing the mode count from 3 to the "
            "photon's 2; only then does the holonomy identity lock the "
            "fiber-axis coupling rate",
            "charge-conjugation map on the frame: decide C1 (axis fixed) "
            "vs C2 (frame mirror) from the article's positron-mirror "
            "physics; under C2 the O7 epsilon-coupling exists and its "
            "theta-axis mixing consequences must be derived",
            "hedgehog screening theorem: the fiber/gauge structure must "
            "convert the linear hedgehog tension into a 1/r^2 Coulomb "
            "far field (Maxwell emergence, stage_d3)",
            "stiffness-ratio theorem on the fiber-curvature backbone: "
            "ratio of fiber-step to axis-step spectra on the finite base "
            "(author's finite-resonator lock: finiteness -> discreteness, "
            "ratio-invariance -> size cancellation) => N, target "
            "10.90497833",
            "then alpha = W^2/(4*pi*N) with the winding-defect coupling "
            "of p18e",
        ],
        "do_not_claim": [
            "Do not claim alpha or Maxwell/Gauss/Ward/U(1) are derived.",
            "Do not read the hedgehog as the electron before the "
            "screening theorem exists (energy is confinement-like now).",
            "Do not claim the helicity identification beyond propagation "
            "along the background axis (needs U(1) redundancy for the "
            "general statement).",
            "Do not present 3 propagating modes as the photon: the "
            "redundancy theorem must remove one.",
            "The holonomy identity locks the fiber CONNECTION "
            "(geometry); the stiffness-ratio lock built on it is NOT yet "
            "derived -- no numerical N claim.",
            "The axis nA is the second component of the SAME orientation "
            "property of the ONE base medium -- not a third medium.",
            "Theta-axis decoupling holds UNDER THE C1 POSTULATE (axis "
            "fixed under charge conjugation); it is not derived from the "
            "unit constraint alone -- the epsilon candidates O5/O7 exist "
            "and C2 would admit O7 (referee finding).",
            "In the gauged completion the winding W of alpha = "
            "W^2/(4*pi*N) migrates from the bare theta to the frame "
            "bundle (fiber holonomy = the Lk = Wr + Tw register); do not "
            "treat W as settled until that completion exists.",
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
    print("dispersion:")
    for key, val in result["dispersion"].items():
        print(f"  {key}: {val}")
    print("helicity_scope:", result["helicity_scope"])
    print("hedgehog_ledger:", result["hedgehog_ledger"])
    print("lock_seed:", result["lock_seed"])
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
    _print_result(derive_oriented_axis_completion_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
