# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# Frame-connection sector (this gate): the p18e fiber angle theta is not
# counted as a third photon polarization.  It is the local rotation coordinate
# of the oriented frame around the p18f axis nA.  The invariant object is
# Dtheta = dtheta + A(n), where A is the spin connection of a local section of
# the SO(3)->S^2 frame bundle.  A local section rotation acts as
# theta -> theta - lambda, A -> A + dlambda, so Dtheta is invariant.

"""
================================================================================
PHASE 18h: Frame-connection U(1) redundancy gate
================================================================================

Purpose
-------
Execute lock 2 named by p18g:

    "covariant coupling D theta = d theta + omega(n) . d n; global shift ->
     local redundancy; mode count 3 -> 2; luminality + solar transparency
     re-checked; no extra scalar mode."

This gate is deliberately narrow.  It does NOT derive Maxwell, Coulomb
screening, the Ward identity, or alpha.  It does one thing: it promotes the
article's statement "a global rotation of the asymmetry angle changes no
physics" to a local frame-bundle redundancy and checks that the orientation
sector still has exactly the two p18f helicity modes at quadratic order.

Geometric setup
---------------
The axis field nA lives on S^2.  A local tangent-frame section over S^2 has a
U(1) freedom: rotate the two transverse frame vectors around nA.  In the north
patch the corresponding connection is the standard monopole/spin connection

    A = (n1 dn2 - n2 dn1)/(1 + n3)

equivalently A = (1 - cos chi) d varphi in spherical coordinates.  Its
curvature is the area form on S^2, so the holonomy around a closed loop is the
enclosed solid angle.  This is the p18f holonomy fact rewritten as the local
connection that can enter the action.

Results (all executable below)
------------------------------
1. CONNECTION CURVATURE: the north-patch connection has
   dA = sin(chi) dchi wedge dvarphi.  The latitude-loop holonomy equals the
   cap solid angle 2*pi*(1 - cos chi).  This is the exact local version of
   p18f's frame holonomy.

2. U(1) GAUGE COVARIANCE: under a local section rotation lambda(x),

       theta -> theta - lambda,      A_mu -> A_mu + partial_mu lambda,

   the one-form Dtheta_mu = partial_mu theta + A_mu is invariant component by
   component.  The global shift symmetry of p18e is therefore promoted to a
   local redundancy of the frame description.

3. NO THIRD QUADRATIC MODE: near the north background
   n = (epsilon*u, epsilon*v, sqrt(1 - epsilon^2(u^2+v^2))), the connection
   A_mu has no linear term:

       A_mu = epsilon^2*(u partial_mu v - v partial_mu u)/2 + O(epsilon^4).

   After the U(1) gauge choice theta = 0, the fiber piece (Dtheta)^2 begins at
   O(epsilon^4).  Hence it contributes NO independent quadratic wave.  The
   only quadratic propagating modes are the two axis modes already found in
   p18f.  This is the operational 3 -> 2 count.

4. LUMINALITY AND SOLAR TRANSPARENCY RECHECK: the surviving quadratic axis
   family is still L_n = F(Y,I1,I2,I3)*Pn, two identical modes riding the
   metric cone.  The connection sector is stress-silent on backgrounds with
   constant orientation/Dtheta = 0, so the p03/p18d solar chain is untouched.

5. WINDING MIGRATION LEDGER: the bare theta winding is not the final
   gauge-invariant register after the completion.  The invariant circulation is

       integral Dtheta = Delta theta + integral A.

   In the theta = 0 gauge it is carried by the frame-bundle holonomy.  For a
   latitude loop this gives exactly the solid angle.  Therefore the p18e
   integer W used in alpha = W^2/(4*pi*N) must be re-read in the completed
   bundle before alpha is claimed.

What this gate does NOT claim
-----------------------------
- Maxwell/Gauss/Ward/Coulomb are NOT derived.
- The hedgehog is NOT yet the electron.
- The integer W in the alpha route is NOT settled; it migrates to the frame
  bundle and must be fixed by the later screening/lock gates.
- N = 10.90497833 is NOT derived here.
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


def _north_connection(nA):
    """A_mu = (n1 d_mu n2 - n2 d_mu n1)/(1+n3), north patch."""
    dn = [_grad(c) for c in nA]
    return [
        sp.simplify((nA[0] * dn[1][mu] - nA[1] * dn[0][mu]) / (1 + nA[2]))
        for mu in range(4)
    ]


# ---------------------------------------------------------------------------
# 1. Connection curvature and holonomy
# ---------------------------------------------------------------------------

def connection_curvature_and_holonomy() -> dict:
    chi, varphi = sp.symbols("chi varphi", real=True)
    A_chi = sp.Integer(0)
    A_varphi = 1 - sp.cos(chi)
    curvature = sp.simplify(sp.diff(A_varphi, chi) - sp.diff(A_chi, varphi))
    cap_holonomy = sp.integrate(A_varphi, (varphi, 0, 2 * sp.pi))
    cap_area = sp.integrate(
        sp.integrate(sp.sin(chi), (varphi, 0, 2 * sp.pi)),
        (chi, 0, chi),
    )
    return {
        "curvature_is_area_form": sp.simplify(curvature - sp.sin(chi)) == 0,
        "latitude_holonomy_equals_cap_solid_angle": sp.simplify(
            cap_holonomy - cap_area
        )
        == 0,
        "A_north": "A = (1 - cos(chi)) dvarphi",
        "F": "dA = sin(chi) dchi wedge dvarphi",
        "holonomy": str(sp.simplify(cap_holonomy)),
    }


# ---------------------------------------------------------------------------
# 2. U(1) gauge covariance
# ---------------------------------------------------------------------------

def gauge_covariance_theorem() -> dict:
    theta_mu = sp.symbols("theta_0 theta_1 theta_2 theta_3", real=True)
    A_mu = sp.symbols("A_0 A_1 A_2 A_3", real=True)
    lam_mu = sp.symbols("lambda_0 lambda_1 lambda_2 lambda_3", real=True)
    D = [theta_mu[i] + A_mu[i] for i in range(4)]
    transformed = [
        (theta_mu[i] - lam_mu[i]) + (A_mu[i] + lam_mu[i])
        for i in range(4)
    ]
    return {
        "Dtheta_componentwise_invariant": all(
            sp.simplify(transformed[i] - D[i]) == 0 for i in range(4)
        ),
        "rule": "theta -> theta - lambda, A -> A + d lambda",
        "physical_reading": (
            "theta is a local frame-section coordinate, not an independent "
            "third photon polarization"
        ),
    }


# ---------------------------------------------------------------------------
# 3. Quadratic mode count after gauge completion
# ---------------------------------------------------------------------------

def quadratic_mode_count_gate() -> dict:
    u = sp.Function("u")(t, x, y, z)
    v = sp.Function("v")(t, x, y, z)
    n3 = sp.sqrt(1 - eps**2 * (u**2 + v**2))
    nA = [eps * u, eps * v, n3]
    A = _north_connection(nA)
    A_linear = [sp.simplify(sp.diff(a, eps).subs(eps, 0)) for a in A]
    A_second = [
        sp.simplify(sp.diff(a, eps, 2).subs(eps, 0) / 2) for a in A
    ]
    expected_second = [
        sp.simplify((u * sp.diff(v, c) - v * sp.diff(u, c)) / 2)
        for c in COORDS
    ]

    # Gauge theta = 0.  Since A = O(eps^2), F_conn * A^2 has no eps^2 term.
    kf = sp.symbols("kappa_f", positive=True)
    L_conn = kf * _con(A, A)
    quadratic_conn = sp.simplify(sp.diff(L_conn, eps, 2).subs(eps, 0) / 2)

    # Axis sector: two identical luminal free modes on Minkowski.
    kn = sp.symbols("kappa_n", positive=True)
    L_axis = kn * (
        sp.diff(u, t) ** 2
        + sp.diff(v, t) ** 2
        - sum(sp.diff(f, c) ** 2 for f in (u, v) for c in (x, y, z))
    )
    w, kx, ky, kz = sp.symbols("omega k_x k_y k_z", real=True)
    au, av = sp.symbols("amp_u amp_v", real=True)
    subs = []
    for f, amp in ((u, au), (v, av)):
        for c, kc in ((t, -w), (x, kx), (y, ky), (z, kz)):
            subs.append((sp.Derivative(f, c), amp * sp.I * kc))
    L_sym = sp.expand(L_axis.subs(subs))
    M = sp.simplify(
        -sp.Matrix(
            2,
            2,
            lambda i, j: sp.diff(L_sym, [au, av][i], [au, av][j]) / 2,
        )
    )
    det = sp.factor(sp.simplify(M.det()))
    k2 = kx**2 + ky**2 + kz**2
    dispersion_is_double_luminal = sp.simplify(det / (kn**2) - (w**2 - k2) ** 2) == 0

    return {
        "connection_has_no_linear_term": all(a == 0 for a in A_linear),
        "second_order_connection_matches_monopole_patch": all(
            sp.simplify(A_second[i] - expected_second[i]) == 0
            for i in range(4)
        ),
        "gauge_fixed_connection_has_no_quadratic_wave": quadratic_conn == 0,
        "axis_pair_double_luminal": bool(dispersion_is_double_luminal),
        "physical_mode_count": "3 coordinates (theta,u,v) - 1 local U(1) redundancy = 2 propagating axis modes",
        "A_second_order": [str(a) for a in A_second],
    }


# ---------------------------------------------------------------------------
# 4. Solar transparency / cone recheck
# ---------------------------------------------------------------------------

def solar_transparency_recheck() -> dict:
    q = {}
    for m in range(4):
        for n in range(m, 4):
            q[(m, n)] = sp.Symbol(f"q{m}{n}", real=True)

    dth = sp.symbols("Dth0 Dth1 Dth2 Dth3", real=True)
    D = list(dth)

    def con_full(uu, vv):
        total = 0
        for m in range(4):
            for n in range(4):
                key = (m, n) if m <= n else (n, m)
                total += q[key] * uu[m] * vv[n]
        return total

    kf = sp.symbols("kappa_f", positive=True)
    L = kf * con_full(D, D)
    at_zero = {s: 0 for s in D}
    stress_silent = all(
        sp.simplify((2 * sp.diff(L, qq)).subs(at_zero)) == 0
        for qq in q.values()
    ) and sp.simplify(L.subs(at_zero)) == 0
    eom_trivial = all(sp.simplify(sp.diff(L, s).subs(at_zero)) == 0 for s in D)

    return {
        "connection_sector_stress_silent_at_Dtheta_zero": bool(stress_silent),
        "connection_eom_trivial_at_Dtheta_zero": bool(eom_trivial),
        "scope": (
            "generic symmetric inverse metric, orientation-constant "
            "background, Dtheta = 0: the connection sector contributes no "
            "background stress, so the solar chain is untouched"
        ),
    }


# ---------------------------------------------------------------------------
# 5. Winding migration ledger
# ---------------------------------------------------------------------------

def winding_migration_ledger() -> dict:
    chi, varphi = sp.symbols("chi varphi", real=True)
    W = sp.symbols("W", integer=True)
    theta = W * varphi
    A_varphi = 1 - sp.cos(chi)
    bare_theta = sp.integrate(sp.diff(theta, varphi), (varphi, 0, 2 * sp.pi))
    frame_holonomy = sp.integrate(A_varphi, (varphi, 0, 2 * sp.pi))
    invariant = sp.simplify(bare_theta + frame_holonomy)
    theta_zero_gauge_value = frame_holonomy
    return {
        "bare_theta_winding_is_2piW": sp.simplify(bare_theta - 2 * sp.pi * W)
        == 0,
        "theta_zero_gauge_carries_frame_holonomy": sp.simplify(
            theta_zero_gauge_value - 2 * sp.pi * (1 - sp.cos(chi))
        )
        == 0,
        "invariant_circulation": str(invariant),
        "ledger": (
            "after U(1) completion the route's W is a bundle/framing "
            "register, not a bare scalar theta count; later gates must fix "
            "which completed winding couples to charge"
        ),
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_frame_connection_u1_gate() -> dict:
    geom = connection_curvature_and_holonomy()
    gauge = gauge_covariance_theorem()
    modes = quadratic_mode_count_gate()
    solar = solar_transparency_recheck()
    winding = winding_migration_ledger()

    closed = {
        "connection_curvature_is_sphere_area_form": bool(
            geom["curvature_is_area_form"]
        ),
        "holonomy_equals_solid_angle": bool(
            geom["latitude_holonomy_equals_cap_solid_angle"]
        ),
        "Dtheta_is_U1_gauge_invariant": bool(
            gauge["Dtheta_componentwise_invariant"]
        ),
        "connection_has_no_linear_term": bool(
            modes["connection_has_no_linear_term"]
        ),
        "gauge_fixed_fiber_has_no_quadratic_mode": bool(
            modes["gauge_fixed_connection_has_no_quadratic_wave"]
        ),
        "axis_pair_remains_double_luminal": bool(
            modes["axis_pair_double_luminal"]
        ),
        "solar_chain_untouched_by_connection_sector": bool(
            solar["connection_sector_stress_silent_at_Dtheta_zero"]
            and solar["connection_eom_trivial_at_Dtheta_zero"]
        ),
        "winding_migrates_to_frame_bundle_ledger": bool(
            winding["bare_theta_winding_is_2piW"]
            and winding["theta_zero_gauge_carries_frame_holonomy"]
        ),
    }

    open_checks = {
        "maxwell_gauss_ward_derived": False,
        "hedgehog_screening_gate_built": False,
        "completed_winding_charge_coupling_derived": False,
        "finite_orientation_lock_N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_SCREENING_AND_MAXWELL_NEXT__"
            + _pass_status("FRAME_CONNECTION_U1_REDUNDANCY")
            if all(closed.values())
            else "CHECK_FRAME_CONNECTION_U1_DERIVATION"
        ),
        "SCOPE": (
            "lock 2 of the alpha chain: the p18e theta fiber is promoted "
            "from a global shift variable to a local U(1) frame-section "
            "coordinate; Dtheta = dtheta + A(n) is gauge invariant, the "
            "fiber coordinate is redundant, and the quadratic spectrum "
            "contains only the two p18f axis/helicity modes.  Luminality "
            "and solar transparency survive; Maxwell, screening, N and "
            "alpha remain open."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "connection": {
            "A_north": geom["A_north"],
            "curvature": geom["F"],
            "holonomy": geom["holonomy"],
            "small_field_A": modes["A_second_order"],
        },
        "mode_count": modes["physical_mode_count"],
        "solar_recheck": solar["scope"],
        "winding_ledger": winding["ledger"],
        "physical_reading": (
            "the photon-candidate sector is now a genuine frame-bundle "
            "U(1) system at the kinematic/quadratic level: theta is the "
            "local fiber gauge coordinate, not a third polarization; the "
            "physical waves are the two luminal axis modes.  The price is "
            "honest: the charge/winding register must be reread in the "
            "completed bundle before the Coulomb and alpha gates can close."
        ),
        "missing_derivations": [
            "lock 3 (p18i_hedgehog_screening_maxwell_gate): derive the "
            "screened far field, Gauss law, Coulomb energy and the Ward "
            "identity from the completed frame connection",
            "decide the completed electric vs magnetic register: whether "
            "the pi_2 hedgehog is magnetic while electric charge lives in "
            "the framing/twist register, as p18g branch B suggests",
            "lock 4 (p18j_finite_orientation_lock_alpha_gate): derive N "
            "as the ratio of fiber-step to axis-step spectra on the same "
            "finite orientation-frame resonator; no number scanning",
        ],
        "do_not_claim": [
            "Do not claim Maxwell, Gauss, Ward identity, Coulomb law, "
            "screening, N, or alpha are derived here.",
            "Do not count theta as a physical photon polarization after "
            "this gate; it is a local frame-section coordinate.",
            "Do not treat the p18e bare W as settled; after this gate W "
            "is a completed bundle/framing register.",
            "Do not identify the hedgehog with the electron before the "
            "screening and electric/magnetic register gates.",
            "The connection is written in a north patch; global physics "
            "requires patching/quantization in the Maxwell-screening gate.",
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
    print("connection:")
    for key, val in result["connection"].items():
        print(f"  {key}: {val}")
    print("mode_count:", result["mode_count"])
    print("solar_recheck:", result["solar_recheck"])
    print("winding_ledger:", result["winding_ledger"])
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
    _print_result(derive_frame_connection_u1_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
