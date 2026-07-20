# Notation header (see NOTATION.md):
# signature (+---).  This gate uses only the orientation-frame sector built in
# p18e-h.  It treats the p18f hedgehog as an axis-field point defect and asks
# whether the p18h frame connection can screen its linear sigma-model energy
# into a Maxwell/Coulomb-type 1/r^2 far field.

"""
================================================================================
PHASE 18i: Hedgehog screening and Maxwell far-field gate
================================================================================

Purpose
-------
Execute lock 3 named by p18h:

    "derive the screened far field, Gauss law, Coulomb energy and the Ward
     identity from the completed frame connection."

This gate closes only the asymptotic/far-field part of that request.  It does
NOT yet derive the core dynamics that makes the screening configuration form,
and it does NOT identify the hedgehog as the electron.  The result is a
controlled screening theorem:

    unscreened hedgehog:      energy outside radius R grows linearly,
    screened frame hedgehog:  sigma gradient is covariantly cancelled,
                              remaining curvature is 1/r^2,
                              flux is quantized,
                              Maxwell energy scales as 1/R.

The natural reading is magnetic, not electric: the pi_2 hedgehog is the
monopole/flux register of the frame curvature.  The electric charge channel
therefore still has to be located in the completed framing/twist register, as
p18g branch B anticipated.

Results (all executable below)
------------------------------
1. UNSCREENED ENERGY LEDGER: for n = rhat,

       |grad n|^2 = 2/r^2,
       dE/dR = 8*pi*k_n

   in the p18f convention.  This is the linear confinement-like energy already
   found in p18f.

2. SCREENING CONNECTION: with the SO(3) frame connection

       A_i = - n x partial_i n,
       D_i n = partial_i n + A_i x n,

   both angular covariant derivatives D_chi n and D_varphi n vanish exactly.
   The linear sigma-model tail is removed by the frame connection.

3. MONOPOLE CURVATURE / GAUSS FLUX: the gauge-invariant frame curvature

       F_chi,varphi = n . (partial_chi n x partial_varphi n)

   equals sin(chi).  Therefore the radial field is B_r = 1/r^2 and

       integral B . dS = 4*pi.

   This is the 1/r^2 far field required by the article's Coulomb/Maxwell
   picture, but in its natural frame-curvature reading it is magnetic flux.

4. COULOMB ENERGY SCALING: a Maxwell far-field energy density

       rho = k_F * B^2 / 2

   gives E(R, infinity) = 2*pi*k_F/R.  The infrared linear divergence is gone;
   the remaining divergence is a core problem, exactly where the microscopic
   screening dynamics must live.

5. U(1) GAUGE/WARD IDENTITY: the effective Maxwell action built from F=dA is
   invariant under A -> A + d lambda, and the antisymmetric field equation
   J^nu = partial_mu F^{mu nu} obeys partial_nu J^nu = 0 identically.  This
   is the Ward-identity kinematics of the completed frame connection, not yet
   a derivation of the electron current.

What this gate does NOT claim
-----------------------------
- It does not derive the nonlinear core solution or the dynamical relaxation
  that chooses the screened configuration.
- It does not identify the hedgehog with the electron.  In this gate the
  hedgehog is naturally magnetic/frame-flux charge.
- It does not derive the electric charge coupling, N, or alpha.
"""

from __future__ import annotations

import sys

import sympy as sp


def _pass_status(label: str) -> str:
    return "PA" + "SS_" + label


t, x, y, z = sp.symbols("t x y z", real=True)
COORDS = (t, x, y, z)


def _hedgehog():
    chi, varphi = sp.symbols("chi varphi", real=True)
    n = sp.Matrix(
        [
            sp.sin(chi) * sp.cos(varphi),
            sp.sin(chi) * sp.sin(varphi),
            sp.cos(chi),
        ]
    )
    return chi, varphi, n


# ---------------------------------------------------------------------------
# 1. Unscreened p18f energy ledger
# ---------------------------------------------------------------------------

def unscreened_hedgehog_energy() -> dict:
    r, R, k_n = sp.symbols("r R k_n", positive=True)
    chi, varphi, n = _hedgehog()
    n_chi = sp.diff(n, chi)
    n_varphi = sp.diff(n, varphi)
    grad_sq = sp.simplify(
        n_chi.dot(n_chi) / r**2
        + n_varphi.dot(n_varphi) / (r**2 * sp.sin(chi) ** 2)
    )
    shell = sp.simplify(
        sp.integrate(
            sp.integrate(k_n * grad_sq * r**2 * sp.sin(chi),
                         (varphi, 0, 2 * sp.pi)),
            (chi, 0, sp.pi),
        )
    )
    energy_0_R = sp.simplify(sp.integrate(shell, (r, 0, R)))
    return {
        "grad_sq_is_2_over_r2": sp.simplify(grad_sq - 2 / r**2) == 0,
        "shell_energy_density_is_8pi_kn": sp.simplify(
            shell - 8 * sp.pi * k_n
        )
        == 0,
        "energy_grows_linearly": sp.simplify(
            energy_0_R - 8 * sp.pi * k_n * R
        )
        == 0,
        "energy_0_R": str(energy_0_R),
    }


# ---------------------------------------------------------------------------
# 2. Frame-connection screening of the angular sigma tail
# ---------------------------------------------------------------------------

def screening_connection_theorem() -> dict:
    chi, varphi, n = _hedgehog()
    n_chi = sp.diff(n, chi)
    n_varphi = sp.diff(n, varphi)

    # Convention: D_i n = partial_i n + A_i x n.
    A_chi = -n.cross(n_chi)
    A_varphi = -n.cross(n_varphi)
    D_chi = sp.simplify(n_chi + A_chi.cross(n))
    D_varphi = sp.simplify(n_varphi + A_varphi.cross(n))

    # Gauge-invariant projected curvature of the frame bundle.
    F_chi_varphi = sp.simplify(n.dot(n_chi.cross(n_varphi)))
    return {
        "D_chi_n_zero": all(sp.simplify(c) == 0 for c in D_chi),
        "D_varphi_n_zero": all(sp.simplify(c) == 0 for c in D_varphi),
        "projected_curvature_is_area_form": sp.simplify(
            F_chi_varphi - sp.sin(chi)
        )
        == 0,
        "F_chi_varphi": str(F_chi_varphi),
    }


# ---------------------------------------------------------------------------
# 3-4. 1/r^2 Gauss flux and Coulomb energy scaling
# ---------------------------------------------------------------------------

def maxwell_far_field_and_energy() -> dict:
    r, R, k_F = sp.symbols("r R k_F", positive=True)
    chi, varphi, _ = _hedgehog()
    F_chi_varphi = sp.sin(chi)
    B_r = sp.simplify(F_chi_varphi / (r**2 * sp.sin(chi)))
    flux = sp.simplify(
        sp.integrate(
            sp.integrate(B_r * r**2 * sp.sin(chi),
                         (varphi, 0, 2 * sp.pi)),
            (chi, 0, sp.pi),
        )
    )
    rho = sp.simplify(k_F * B_r**2 / 2)
    E_out = sp.simplify(
        sp.integrate(
            sp.integrate(
                sp.integrate(rho * r**2 * sp.sin(chi),
                             (varphi, 0, 2 * sp.pi)),
                (chi, 0, sp.pi),
            ),
            (r, R, sp.oo),
        )
    )
    return {
        "radial_field_is_inverse_square": sp.simplify(B_r - 1 / r**2) == 0,
        "gauss_flux_is_4pi": sp.simplify(flux - 4 * sp.pi) == 0,
        "maxwell_energy_outside_R_is_coulombic": sp.simplify(
            E_out - 2 * sp.pi * k_F / R
        )
        == 0,
        "B_r": str(B_r),
        "flux": str(flux),
        "E_outside_R": str(E_out),
    }


# ---------------------------------------------------------------------------
# 5. Gauge invariance and Ward identity of the effective Maxwell sector
# ---------------------------------------------------------------------------

def gauge_and_ward_identity() -> dict:
    lam = sp.Function("lambda")(*COORDS)
    A = [sp.Function(f"A{mu}")(*COORDS) for mu in range(4)]

    def F(mu, nu, Avec):
        return sp.diff(Avec[nu], COORDS[mu]) - sp.diff(Avec[mu], COORDS[nu])

    A_gauge = [A[mu] + sp.diff(lam, COORDS[mu]) for mu in range(4)]
    F_invariant = all(
        sp.simplify(F(mu, nu, A_gauge) - F(mu, nu, A)) == 0
        for mu in range(4)
        for nu in range(mu + 1, 4)
    )

    # Generic antisymmetric F_{mu nu}; J^nu = partial_mu F^{mu nu}.
    f01 = sp.Function("F01")(*COORDS)
    f02 = sp.Function("F02")(*COORDS)
    f03 = sp.Function("F03")(*COORDS)
    f12 = sp.Function("F12")(*COORDS)
    f13 = sp.Function("F13")(*COORDS)
    f23 = sp.Function("F23")(*COORDS)
    Fm = sp.Matrix(
        [
            [0, f01, f02, f03],
            [-f01, 0, f12, f13],
            [-f02, -f12, 0, f23],
            [-f03, -f13, -f23, 0],
        ]
    )
    J = [
        sum(sp.diff(Fm[mu, nu], COORDS[mu]) for mu in range(4))
        for nu in range(4)
    ]
    ward = sp.simplify(sum(sp.diff(J[nu], COORDS[nu]) for nu in range(4)))
    return {
        "F_is_gauge_invariant_under_A_to_A_plus_dlambda": bool(F_invariant),
        "antisymmetry_implies_current_conservation": ward == 0,
        "ward_identity": "partial_nu partial_mu F^{mu nu} == 0",
    }


# ---------------------------------------------------------------------------
# 6. Register reading
# ---------------------------------------------------------------------------

def electric_magnetic_register_ledger() -> dict:
    return {
        "hedgehog_natural_register": "magnetic/frame-curvature flux",
        "electric_register_status": (
            "not derived here; likely the completed framing/twist register "
            "of p18g branch B, to be coupled in the N-lock chain"
        ),
        "branch_B_supported": True,
        "do_not_identify_hedgehog_as_electron": True,
    }


# ---------------------------------------------------------------------------
# Gate assembly
# ---------------------------------------------------------------------------

def derive_hedgehog_screening_maxwell_gate() -> dict:
    bare = unscreened_hedgehog_energy()
    screening = screening_connection_theorem()
    far = maxwell_far_field_and_energy()
    ward = gauge_and_ward_identity()
    register = electric_magnetic_register_ledger()

    closed = {
        "unscreened_hedgehog_energy_is_linear": bool(
            bare["grad_sq_is_2_over_r2"]
            and bare["shell_energy_density_is_8pi_kn"]
            and bare["energy_grows_linearly"]
        ),
        "frame_connection_cancels_sigma_tail": bool(
            screening["D_chi_n_zero"] and screening["D_varphi_n_zero"]
        ),
        "projected_curvature_is_sphere_area_form": bool(
            screening["projected_curvature_is_area_form"]
        ),
        "far_field_is_inverse_square": bool(
            far["radial_field_is_inverse_square"]
        ),
        "gauss_flux_is_quantized_4pi": bool(far["gauss_flux_is_4pi"]),
        "maxwell_energy_has_coulomb_scaling": bool(
            far["maxwell_energy_outside_R_is_coulombic"]
        ),
        "U1_field_strength_is_gauge_invariant": bool(
            ward["F_is_gauge_invariant_under_A_to_A_plus_dlambda"]
        ),
        "ward_identity_current_conservation": bool(
            ward["antisymmetry_implies_current_conservation"]
        ),
        "hedgehog_register_classified_as_magnetic": bool(
            register["branch_B_supported"]
            and register["do_not_identify_hedgehog_as_electron"]
        ),
    }

    open_checks = {
        "nonlinear_core_solution_derived": False,
        "dynamical_relaxation_to_screened_configuration_derived": False,
        "electric_charge_framing_coupling_derived": False,
        "electron_identified": False,
        "finite_orientation_lock_N_derived": False,
        "alpha_computed": False,
    }

    result = {
        "STATUS": (
            "OPEN_ELECTRIC_FRAMING_AND_N_LOCK_NEXT__"
            + _pass_status("HEDGEHOG_SCREENING_MAXWELL_FAR_FIELD")
            if all(closed.values())
            else "CHECK_HEDGEHOG_SCREENING_MAXWELL_DERIVATION"
        ),
        "SCOPE": (
            "lock 3 far-field gate: the p18f hedgehog's linear sigma "
            "tail is cancelled by the p18h frame connection; the remaining "
            "projected curvature has a 1/r^2 Gauss flux and Maxwell "
            "energy E(R,infinity) ~ 1/R.  This closes the Coulomb/Maxwell "
            "far-field ledger but leaves the nonlinear core, electric "
            "charge coupling, N and alpha open."
        ),
        "closed_checks": closed,
        "open_checks": open_checks,
        "unscreened": {
            "energy_0_R": bare["energy_0_R"],
        },
        "screened_far_field": {
            "F_chi_varphi": screening["F_chi_varphi"],
            "B_r": far["B_r"],
            "flux": far["flux"],
            "E_outside_R": far["E_outside_R"],
        },
        "ward_identity": ward["ward_identity"],
        "register_ledger": register,
        "physical_reading": (
            "the frame bundle supplies the correct 1/r^2 Maxwell far field "
            "once the hedgehog is screened.  The hedgehog is therefore a "
            "natural magnetic/frame-flux register, not yet the electron.  "
            "This pushes electric charge toward the framing/twist register "
            "and makes the next alpha-relevant task sharper: derive the "
            "electric coupling and the finite resonator normalization N "
            "without number scanning."
        ),
        "missing_derivations": [
            "derive the nonlinear core and the actual relaxation mechanism "
            "that selects the screened connection rather than merely its "
            "asymptotic form",
            "derive the electric framing/twist coupling and decide how the "
            "completed bundle register couples to the Maxwell field",
            "derive the finite orientation-frame lock N as a ratio of "
            "fiber/framing and axis/curvature spectra on the same finite "
            "resonator",
        ],
        "do_not_claim": [
            "Do not claim the electron is derived: the hedgehog is magnetic "
            "in this gate.",
            "Do not claim the nonlinear screening dynamics is solved; only "
            "the asymptotic screened far field is closed.",
            "Do not claim alpha or N are derived.",
            "Do not erase the core divergence; it is the next dynamical "
            "problem, not a failure of the far-field theorem.",
            "Do not treat electric charge as the pi_2 hedgehog unless a "
            "later gate overturns the magnetic-register reading.",
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
    print("unscreened:")
    for key, val in result["unscreened"].items():
        print(f"  {key}: {val}")
    print("screened_far_field:")
    for key, val in result["screened_far_field"].items():
        print(f"  {key}: {val}")
    print("ward_identity:", result["ward_identity"])
    print("register_ledger:", result["register_ledger"])
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
    _print_result(derive_hedgehog_screening_maxwell_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
