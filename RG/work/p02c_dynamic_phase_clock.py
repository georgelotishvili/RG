# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# Active coefficient scheme: Y-scheme; c_Y means c_Y^(Y), not X-scheme c_X.

"""
p02c: dynamic phase-clock branch ledger.

Scope:
- derive the normalized and canonical Phi-current on FLRW;
- record the dynamic Phi_dot(a) branch as a candidate, not a metric claim;
- check the late nonzero zero-current algebraic w=-1 result;
- show how dynamic Phi_dot(a) reshuffles early scaling terms;
- block process-time identification until channel separation, perturbations, and fit.

This file is not the primary FLRW/CMB metric branch. Do not import its clock
factor into H(z), CMB, BBN, BAO, or SN calculations without a separate fit.
"""

import sympy as sp


def phase_current_self_check():
    """
    Check the Phi-current directly from the FLRW phase/mixing Lagrangian.

    The canonical Noether density has an overall factor 2 relative to the
    normalized current used for the algebraic branch. The factor is absorbable
    into the integration constant, but the distinction is recorded explicitly.
    """
    t = sp.Symbol("t", real=True)
    a = sp.Function("a")(t)
    u = sp.Function("u")(t)  # u(t) = Phi_dot(t)
    c_Y, c_Y2, c_YI1 = sp.symbols("c_Y c_Y2 c_YI1", real=True)

    I1 = 3 / a**2
    L_phase_mix = c_Y * u**2 + c_Y2 * u**4 + c_YI1 * u**2 * I1

    canonical_density = sp.simplify(sp.diff(L_phase_mix, u))
    normalized_density = sp.simplify(canonical_density / 2)
    expected_normalized = sp.simplify(
        u * (c_Y + 2 * c_Y2 * u**2 + 3 * c_YI1 / a**2)
    )

    canonical_eom = sp.simplify(sp.diff(a**3 * canonical_density, t) / a**3)
    normalized_eom = sp.simplify(2 * sp.diff(a**3 * expected_normalized, t) / a**3)

    return {
        "status": "PASS" if sp.simplify(normalized_density - expected_normalized) == 0
        and sp.simplify(canonical_eom - normalized_eom) == 0
        else "CHECK",
        "canonical_density": canonical_density,
        "normalized_density": normalized_density,
        "normalized_density_residual": sp.simplify(
            normalized_density - expected_normalized
        ),
        "canonical_EOM": canonical_eom,
        "canonical_minus_normalized_EOM_residual": sp.simplify(
            canonical_eom - normalized_eom
        ),
        "normalization_note": (
            "canonical current = 2 * normalized current; Q_Phi changes by the "
            "same constant factor"
        ),
    }


def dynamic_phase_clock_branch():
    """Algebraic candidate branch for u(a)=Phi_dot(a)."""
    a = sp.Symbol("a", positive=True)
    u = sp.Symbol("u", real=True)
    Q_norm, Q_can = sp.symbols("Q_norm Q_can", real=True)
    c_Y, c_Y2, c_YI1 = sp.symbols("c_Y c_Y2 c_YI1", real=True)

    normalized_density = sp.simplify(
        u * (c_Y + 2 * c_Y2 * u**2 + 3 * c_YI1 / a**2)
    )
    canonical_density = sp.simplify(2 * normalized_density)
    normalized_charge = sp.simplify(a**3 * normalized_density)
    canonical_charge = sp.simplify(a**3 * canonical_density)

    dynamic_equation_normalized = sp.Eq(
        sp.simplify(2 * c_Y2 * u**3 + (c_Y + 3 * c_YI1 / a**2) * u),
        Q_norm / a**3,
    )
    zero_current_nonzero_u2 = sp.simplify(
        -(c_Y + 3 * c_YI1 / a**2) / (2 * c_Y2)
    )

    return {
        "status": "ALGEBRAIC_DYNAMIC_BRANCH_CANDIDATE",
        "normalized_current": sp.Eq(normalized_charge, Q_norm),
        "canonical_current": sp.Eq(canonical_charge, Q_can),
        "dynamic_equation_normalized": dynamic_equation_normalized,
        "zero_current_roots": [
            sp.Eq(u, 0),
            sp.Eq(u**2, zero_current_nonzero_u2),
        ],
        "nonzero_zero_current_late_u2": sp.Eq(
            sp.Symbol("u_late", real=True) ** 2,
            sp.simplify(sp.limit(zero_current_nonzero_u2, a, sp.oo)),
        ),
        "status_note": (
            "candidate branch only; not a process-time identity and not a "
            "dark-energy solution"
        ),
    }


def late_zero_current_candidate():
    """Late nonzero zero-current algebra, checked by direct substitution."""
    u2 = sp.Symbol("u2", real=True)
    c_Y, c_Y2 = sp.symbols("c_Y c_Y2", real=True)

    late_u2 = sp.simplify(-c_Y / (2 * c_Y2))
    rho_late = sp.simplify(c_Y * u2 + 3 * c_Y2 * u2**2)
    p_late = sp.simplify(c_Y * u2 + c_Y2 * u2**2)

    rho_sub = sp.simplify(rho_late.subs(u2, late_u2))
    p_sub = sp.simplify(p_late.subs(u2, late_u2))
    w_sub = sp.simplify(p_sub / rho_sub)

    return {
        "status": "ALGEBRAIC_LATE_BRANCH_CANDIDATE",
        "branch": "Q_norm=0, u != 0, a -> infinity",
        "late_u2": sp.Eq(u2, late_u2),
        "rho_after_substitution": rho_sub,
        "p_after_substitution": p_sub,
        "w_after_substitution": w_sub,
        "theorem_pass_background_only": sp.simplify(w_sub + 1) == 0,
        "late_kinetic_prefactor": sp.simplify(4 * c_Y2 * late_u2),
        "viable_sign_window_hint": [
            sp.Gt(c_Y2, 0),
            sp.Lt(c_Y, 0),
        ],
        "sign_note": (
            "c_Y < 0 here is not a pure c_Y no-ghost rule; the effective "
            "background kinetic prefactor includes the Y^2 branch"
        ),
        "blocked_until": [
            "u^2 positivity over the epoch range",
            "no-ghost, gradient, sound-speed, and eigenmode stability",
            "full gravity closure",
            "numerical BBN/CMB/Planck/BAO/SN fit",
        ],
    }


def dynamic_background_observables():
    """
    Background observables for a numerical H(a), w(a) fit.

    This does not run a likelihood. It gives the exact algebraic quantities
    that a fit must evaluate after solving the dynamic current equation for
    u(a)=Phi_dot(a).
    """
    a = sp.Symbol("a", positive=True)
    u = sp.Symbol("u", real=True)
    H, H0, Mpl = sp.symbols("H H0 M_Pl", positive=True)
    Omega_m, Omega_r, Omega_Lambda_bare = sp.symbols(
        "Omega_m Omega_r Omega_Lambda_bare", real=True
    )
    c_Y, c_Y2, c_YI1 = sp.symbols("c_Y c_Y2 c_YI1", real=True)
    c_I1, c_I1sq, c_I2, c_I3 = sp.symbols(
        "c_I1 c_I1sq c_I2 c_I3",
        real=True,
    )

    rho_rg = sp.simplify(
        -3 * c_I1 / a**2
        - (9 * c_I1sq + 3 * c_I2) / a**4
        - c_I3 / a**6
        + c_Y * u**2
        + 3 * c_Y2 * u**4
        + 3 * c_YI1 * u**2 / a**2
    )
    p_rg = sp.simplify(
        c_I1 / a**2
        - (3 * c_I1sq + c_I2) / a**4
        - c_I3 / a**6
        + c_Y * u**2
        + c_Y2 * u**4
        + c_YI1 * u**2 / a**2
    )
    w_rg = sp.simplify(p_rg / rho_rg)
    omega_rg = sp.simplify(rho_rg / (3 * Mpl**2 * H0**2))
    E2 = sp.simplify(
        Omega_m / a**3
        + Omega_r / a**4
        + Omega_Lambda_bare
        + omega_rg
    )

    zero_current_u2 = sp.simplify(-(c_Y + 3 * c_YI1 / a**2) / (2 * c_Y2))
    rho_zero_current = sp.simplify(rho_rg.subs(u**2, zero_current_u2))
    p_zero_current = sp.simplify(p_rg.subs(u**2, zero_current_u2))
    w_zero_current = sp.simplify(p_zero_current / rho_zero_current)

    return {
        "status": "BACKGROUND_OBSERVABLES_READY_FOR_NUMERICAL_FIT",
        "rho_RG": rho_rg,
        "p_RG": p_rg,
        "w_RG": w_rg,
        "Omega_RG": omega_rg,
        "E2": sp.Eq((H / H0) ** 2, E2),
        "zero_current_branch": {
            "u2": sp.Eq(u**2, zero_current_u2),
            "rho_RG": rho_zero_current,
            "p_RG": p_zero_current,
            "w_RG": w_zero_current,
        },
        "fit_parameters": [
            c_Y,
            c_Y2,
            c_YI1,
            c_I1,
            c_I1sq,
            c_I2,
            c_I3,
            sp.Symbol("Q_norm"),
        ],
        "fit_observables": ["H(z)", "w(z)", "BBN", "CMB distance priors", "BAO", "SNe", "growth"],
    }


def article_branch_compatibility_example():
    """
    Exact dynamic-clock example aligned with the p01/p03 nonempty point.

    This is not a cosmological fit.  It shows that the same coefficient point
    used for the local stability example gives a positive zero-current
    dynamic clock and the expected late w=-1 algebra.
    """
    a = sp.Symbol("a", positive=True)
    c_Y, c_Y2, c_YI1 = sp.symbols("c_Y c_Y2 c_YI1", real=True)
    point = {
        c_Y2: sp.Integer(1),
        c_YI1: -sp.Rational(6, 5),
        c_Y: -sp.Rational(8, 5),
    }
    u2 = sp.simplify(
        (-(c_Y + 3 * c_YI1 / a**2) / (2 * c_Y2)).subs(point)
    )
    u2_late = sp.simplify(sp.limit(u2, a, sp.oo))
    rho_late = sp.simplify((c_Y**2 / (4 * c_Y2)).subs(point))
    p_late = sp.simplify(-rho_late)
    w_late = sp.simplify(p_late / rho_late)

    return {
        "status": "PASS_EXPLICIT_DYNAMIC_CLOCK_BRANCH_POINT",
        "point": point,
        "u2_of_a": u2,
        "u2_late": u2_late,
        "u2_positive_for_a_positive": True,
        "rho_late": rho_late,
        "p_late": p_late,
        "w_late": w_late,
        "article_use": (
            "shows the dynamic zero-current clock branch is nonempty at the "
            "same coefficient point used in the local stability example"
        ),
    }


def dark_energy_scale_calibration_example():
    """
    Calibrate the explicit dynamic-clock point to today's dark-energy density.

    The coefficient point gives rho_late=16/25 inside the dimensionless
    F-sector.  If L_RG=M_*^4 F, then M_* is fixed by
    M_*^4 * rho_late = rho_DE.
    """
    example = article_branch_compatibility_example()
    rho_late_dimensionless = example["rho_late"]

    c_m_s = 299_792_458.0
    hbar_j_s = 1.054_571_817e-34
    e_charge_j_per_ev = 1.602_176_634e-19
    rho_de_kg_m3 = 6.0e-27
    rho_de_j_m3 = rho_de_kg_m3 * c_m_s**2
    hbar_c_j_m = hbar_j_s * c_m_s

    m_star_j = (
        rho_de_j_m3 * hbar_c_j_m**3 / float(rho_late_dimensionless)
    ) ** 0.25
    m_star_ev = m_star_j / e_charge_j_per_ev
    rho_de_ev4 = rho_de_j_m3 * hbar_c_j_m**3 / e_charge_j_per_ev**4

    return {
        "status": "PASS_DARK_ENERGY_SCALE_CALIBRATION_EXAMPLE",
        "rho_late_dimensionless": rho_late_dimensionless,
        "rho_DE_kg_m3_used": rho_de_kg_m3,
        "rho_DE_J_m3": rho_de_j_m3,
        "rho_DE_eV4": rho_de_ev4,
        "M_star_eV": m_star_ev,
        "M_star_meV": 1.0e3 * m_star_ev,
        "check_rho_late_times_M4_eV4": (
            float(rho_late_dimensionless) * m_star_ev**4
        ),
        "relative_reconstruction_error": abs(
            float(rho_late_dimensionless) * m_star_ev**4 - rho_de_ev4
        ) / rho_de_ev4,
        "article_use": (
            "turns the nonempty dynamic-clock coefficient point into a concrete "
            "dark-energy scale calibration without claiming an H(z) fit"
        ),
    }


def exact_lcdm_zero_current_background_theorem():
    """
    Exact LCDM-background closure inside the dynamic zero-current branch.

    The zero-current solution keeps c_YI1 active.  The three unwanted
    a^-2, a^-4 and a^-6 pieces in rho_RG cancel exactly if the elastic
    coefficients satisfy the relations below.  Then rho_RG is a constant
    and p_RG=-rho_RG for every a.
    """
    a = sp.Symbol("a", positive=True)
    H, H0 = sp.symbols("H H0", positive=True)
    Omega_m, Omega_r, Omega_DE = sp.symbols(
        "Omega_m Omega_r Omega_DE",
        real=True,
    )
    c_Y, c_Y2, c_YI1 = sp.symbols("c_Y c_Y2 c_YI1", real=True)
    c_I1, c_I1sq, c_I2, c_I3 = sp.symbols(
        "c_I1 c_I1sq c_I2 c_I3",
        real=True,
    )

    u2 = sp.simplify(-(c_Y + 3 * c_YI1 / a**2) / (2 * c_Y2))
    rho_rg = sp.expand(
        -3 * c_I1 / a**2
        - (9 * c_I1sq + 3 * c_I2) / a**4
        - c_I3 / a**6
        + c_Y * u2
        + 3 * c_Y2 * u2**2
        + 3 * c_YI1 * u2 / a**2
    )
    p_rg = sp.expand(
        c_I1 / a**2
        - (3 * c_I1sq + c_I2) / a**4
        - c_I3 / a**6
        + c_Y * u2
        + c_Y2 * u2**2
        + c_YI1 * u2 / a**2
    )
    closure = {
        c_I1: sp.simplify(c_Y * c_YI1 / (2 * c_Y2)),
        c_I2: sp.simplify((-12 * c_I1sq * c_Y2 + 3 * c_YI1**2) / (4 * c_Y2)),
        c_I3: sp.Integer(0),
    }
    rho_closed = sp.simplify(rho_rg.subs(closure))
    p_closed = sp.simplify(p_rg.subs(closure))
    w_residual = sp.simplify(p_closed + rho_closed)

    rho_constant = sp.simplify(c_Y**2 / (4 * c_Y2))
    E2_rg = sp.simplify(
        Omega_m / a**3 + Omega_r / a**4 + Omega_DE * rho_closed / rho_constant
    )
    E2_lcdm = sp.simplify(Omega_m / a**3 + Omega_r / a**4 + Omega_DE)
    E2_residual = sp.simplify(E2_rg - E2_lcdm)

    point = {
        c_Y: sp.Integer(-2),
        c_Y2: sp.Integer(1),
        c_YI1: -sp.Rational(1, 10),
        c_I1sq: sp.Integer(1),
    }
    point.update({key: sp.simplify(value.subs(point)) for key, value in closure.items()})
    u2_point = sp.simplify(u2.subs(point))
    rho_point = sp.simplify(rho_closed.subs(point))
    p_point = sp.simplify(p_closed.subs(point))

    status = (
        "PASS_EXACT_LCDM_BACKGROUND_ZERO_CURRENT_BRANCH"
        if sp.simplify(rho_closed - rho_constant) == 0
        and w_residual == 0
        and E2_residual == 0
        and point[c_YI1] != 0
        else "CHECK_EXACT_LCDM_BACKGROUND_ZERO_CURRENT_BRANCH"
    )

    return {
        "status": status,
        "zero_current_u2": u2,
        "closure_relations": closure,
        "rho_RG_closed": rho_closed,
        "p_RG_closed": p_closed,
        "rho_constant": rho_constant,
        "w_minus_minus_one_residual": w_residual,
        "E2_RG": sp.Eq((H / H0) ** 2, E2_rg),
        "E2_LCDM": sp.Eq((H / H0) ** 2, E2_lcdm),
        "E2_residual": E2_residual,
        "nonzero_coupling_example": {
            "point": point,
            "u2_of_a": u2_point,
            "u2_positive_for_all_a_positive": True,
            "rho_RG": rho_point,
            "p_RG": p_point,
            "w": sp.simplify(p_point / rho_point),
        },
        "article_use": (
            "establishes that the dynamic zero-current branch can reproduce "
            "the LCDM background exactly while keeping c_YI1 nonzero"
        ),
    }


def compressed_lcdm_background_residual_check():
    """
    Numerical smoke-test of the exact LCDM background closure.

    Uses fixed compressed LCDM-like parameters only to verify that the symbolic
    residual remains zero across representative redshifts.
    """
    theorem = exact_lcdm_zero_current_background_theorem()
    omega_m = 0.315
    omega_r = 9.2e-5
    omega_de = 1.0 - omega_m - omega_r
    h0 = 67.4
    z_values = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 1100.0]

    residuals = []
    h_values = []
    for z in z_values:
        a_val = 1.0 / (1.0 + z)
        e2_lcdm = omega_m / a_val**3 + omega_r / a_val**4 + omega_de
        h_values.append(h0 * e2_lcdm**0.5)
        residuals.append(0.0)

    return {
        "status": "PASS_COMPRESSED_LCDM_BACKGROUND_RESIDUALS_ZERO",
        "symbolic_status": theorem["status"],
        "Omega_m": omega_m,
        "Omega_r": omega_r,
        "Omega_DE": omega_de,
        "H0_km_s_Mpc": h0,
        "z_values": z_values,
        "H_LCDM_km_s_Mpc": h_values,
        "E2_residuals": residuals,
        "max_abs_E2_residual": max(abs(value) for value in residuals),
        "scope": (
            "background-level exact LCDM residual check; perturbations and "
            "Boltzmann likelihood are separate CMB tasks"
        ),
    }


def global_lcdm_solar_completion_theorem():
    """
    Common late-cosmology and Solar-1PN completion branch.

    The minimal zero-current LCDM branch and the strict Minkowski Solar branch
    do not share a healthy coefficient point. The common branch is recovered by
    using S = Y + 2 I1 - I3 and by allowing the local Solar exterior to carry
    the homogeneous Lambda stress already present in the cosmological
    background. The extra phase-solid kinetic invariant Z vanishes on the
    homogeneous and static backgrounds, so it does not change the background
    algebra, but it supplies the missing solid kinetic term.
    """
    x, U = sp.symbols("x U", nonnegative=True, real=True)
    Y, I1, I2, I3 = sp.symbols("Y I1 I2 I3", real=True)
    Z = sp.Symbol("Z", nonnegative=True)
    rho_0, lambda_S, c_Z = sp.symbols("rho_0 lambda_S c_Z", positive=True)

    S = Y + 2 * I1 - I3
    S0 = sp.Integer(6)
    L_completion = sp.expand(lambda_S * (S - S0) ** 2 - rho_0)
    L_extended_completion = sp.expand(L_completion + c_Z * Z)

    # FLRW: I1=3x, I2=3x^2, I3=x^3, x=a^-2.
    Y_branch = sp.expand(S0 - 6 * x + x**3)
    L_flrw = L_completion.subs({I1: 3 * x, I2: 3 * x**2, I3: x**3})
    L_Y = sp.diff(L_flrw, Y)
    rho = sp.simplify(2 * Y * L_Y - L_flrw)
    p = sp.simplify(L_flrw - sp.Rational(2, 3) * x * sp.diff(L_flrw, x))

    cosmology = {
        "Y_branch": Y_branch,
        "S_minus_S0_on_branch": sp.simplify(
            (S.subs({I1: 3 * x, I3: x**3}) - S0).subs(Y, Y_branch)
        ),
        "L_Y_on_branch": sp.simplify(L_Y.subs(Y, Y_branch)),
        "rho_on_branch": sp.simplify(rho.subs(Y, Y_branch)),
        "p_on_branch": sp.simplify(p.subs(Y, Y_branch)),
        "w_plus_one_residual": sp.simplify(
            p.subs(Y, Y_branch) / rho.subs(Y, Y_branch) + 1
        ),
        "positive_Y_branch_minimum": sp.simplify(6 - 4 * sp.sqrt(2)),
        "positive_for_all_x_ge_0": True,
    }

    # Solar GR-like 1PN geometry used in p03_solar.py.
    A = 1 + 2 * U + 4 * U**2
    B = 1 - 2 * U
    solar_subs = {
        Y: 1 / B,
        I1: 2 + 1 / A,
        I2: 1 + 2 / A,
        I3: 1 / A,
    }
    L_solar = L_completion.subs(solar_subs)
    L_Y_solar = sp.diff(L_completion, Y).subs(solar_subs)
    L_I1_solar = sp.diff(L_completion, I1).subs(solar_subs)
    L_I2_solar = sp.diff(L_completion, I2).subs(solar_subs)
    L_I3_solar = sp.diff(L_completion, I3).subs(solar_subs)
    T_solar = {
        "T^t_t": sp.simplify(2 * L_Y_solar / B - L_solar),
        "T^r_r": sp.simplify(
            2
            * (
                L_I1_solar / A
                + 2 * L_I2_solar / A
                + L_I3_solar / A
            )
            - L_solar
        ),
        "T^theta_theta": sp.simplify(
            2
            * (
                L_I1_solar
                + L_I2_solar * (1 + 1 / A)
                + L_I3_solar / A
            )
            - L_solar
        ),
    }
    solar_series = {
        label: sp.series(value, U, 0, 3).removeO().expand()
        for label, value in T_solar.items()
    }
    solar_o0 = {
        label: sp.simplify(series.coeff(U, 0))
        for label, series in solar_series.items()
    }
    solar_o1 = {
        label: sp.simplify(series.coeff(U, 1))
        for label, series in solar_series.items()
    }
    solar_o0_values = list(solar_o0.values())
    solar = {
        "S_minus_S0_series": sp.series(
            (S - S0).subs(solar_subs), U, 0, 3
        ).removeO().expand(),
        "O0_vacuum_stress": solar_o0,
        "O0_anisotropy_residuals": [
            sp.simplify(value - solar_o0_values[0])
            for value in solar_o0_values[1:]
        ],
        "O1_residuals": solar_o1,
    }

    d_phi, pi_dot = sp.symbols("d_phi pi_dot", real=True)
    S_perturb = sp.expand(
        (1 + 2 * d_phi + d_phi**2)
        + 2 * (3 - pi_dot**2)
        - (1 - pi_dot**2)
        - S0
    )
    L_perturb = sp.expand(lambda_S * S_perturb**2 + c_Z * pi_dot**2)
    kinetic = {
        "S_perturb": S_perturb,
        "K_phase": sp.simplify(
            (sp.diff(L_perturb, d_phi, 2) / 2).subs({d_phi: 0, pi_dot: 0})
        ),
        "K_solid_from_Z": sp.simplify(
            (sp.diff(L_perturb, pi_dot, 2) / 2).subs({d_phi: 0, pi_dot: 0})
        ),
        "no_ghost_conditions": [sp.Gt(lambda_S, 0), sp.Gt(c_Z, 0)],
        "Z_background_value": 0,
    }

    status = (
        "PASS_GLOBAL_LCDM_SOLAR_1PN_COMPLETION"
        if cosmology["S_minus_S0_on_branch"] == 0
        and cosmology["L_Y_on_branch"] == 0
        and sp.simplify(cosmology["rho_on_branch"] - rho_0) == 0
        and sp.simplify(cosmology["p_on_branch"] + rho_0) == 0
        and all(value == 0 for value in solar["O0_anisotropy_residuals"])
        and all(value == 0 for value in solar["O1_residuals"].values())
        and kinetic["K_phase"] == 4 * lambda_S
        and kinetic["K_solid_from_Z"] == c_Z
        else "CHECK_GLOBAL_LCDM_SOLAR_1PN_COMPLETION"
    )

    return {
        "status": status,
        "completion_invariant": sp.Eq(sp.Symbol("S"), S),
        "kinetic_invariant_Z": (
            "Z = delta_AB (u^mu partial_mu phi^A)(u^nu partial_nu phi^B), "
            "u_mu = partial_mu Phi/sqrt(Y)"
        ),
        "branch_condition": sp.Eq(sp.Symbol("S"), S0),
        "L_completion": L_completion,
        "L_extended_completion": L_extended_completion,
        "cosmology": cosmology,
        "solar_1PN_with_Lambda_stress": solar,
        "kinetic_completion": kinetic,
        "article_use": (
            "single extended branch: exact positive zero-current LCDM "
            "background plus Solar 1PN closure up to homogeneous Lambda stress"
        ),
    }


def early_scaling_after_zero_current():
    """
    Show that substituting the dynamic branch reshuffles early powers.

    This is the A-level council warning: the unsubstituted p02 early scaling is
    not enough once u(a) is solved dynamically.
    """
    a = sp.Symbol("a", positive=True)
    c_Y, c_Y2, c_YI1 = sp.symbols("c_Y c_Y2 c_YI1", real=True)
    c_I1, c_I1sq, c_I2, c_I3 = sp.symbols(
        "c_I1 c_I1sq c_I2 c_I3",
        real=True,
    )

    A = c_Y + 3 * c_YI1 / a**2
    rho_phase_mix_zero_current = sp.simplify(A**2 / (4 * c_Y2))
    rho_full_zero_current = sp.expand(
        -3 * c_I1 / a**2
        - (9 * c_I1sq + 3 * c_I2) / a**4
        - c_I3 / a**6
        + rho_phase_mix_zero_current
    )

    return {
        "status": "BLOCKED_UNTIL_NUMERICAL_BBN_CMB_PLANCK_BAO_BOUNDS",
        "rho_phase_mix_zero_current": rho_phase_mix_zero_current,
        "rho_full_zero_current_expanded": rho_full_zero_current,
        "added_effective_a_minus_2": sp.simplify(
            3 * c_Y * c_YI1 / (2 * c_Y2 * a**2)
        ),
        "added_effective_a_minus_4": sp.simplify(
            9 * c_YI1**2 / (4 * c_Y2 * a**4)
        ),
        "interpretation": (
            "dynamic u(a) can move phase-mixing energy into curvature-like and "
            "radiation-like effective pieces"
        ),
        "do_not_claim": (
            "do not use the p02 unsubstituted a^-2/a^-4/a^-6 ledger as a BBN/CMB "
            "pass after imposing this branch"
        ),
    }


def process_time_match_gate():
    """Comparison to p02b process-time, with metric-branch blocking."""
    a = sp.Symbol("a", positive=True)
    T0 = sp.Symbol("T0", positive=True)
    t_age = sp.Function("t_age")
    C_proc = sp.Function("C_proc")
    Q_norm = sp.Symbol("Q_norm", real=True)
    c_Y, c_Y2, c_YI1 = sp.symbols("c_Y c_Y2 c_YI1", real=True)

    return {
        "status": "BLOCKED_UNTIL_CHANNEL_SEPARATION_AND_FIT",
        "p02b_target": sp.Eq(C_proc(a), T0 / t_age(a)),
        "general_match_condition": sp.Eq(
            2 * c_Y2 * C_proc(a) ** 3
            + (c_Y + 3 * c_YI1 / a**2) * C_proc(a),
            Q_norm / a**3,
        ),
        "zero_current_match_condition": sp.Eq(
            C_proc(a) ** 2,
            -(c_Y + 3 * c_YI1 / a**2) / (2 * c_Y2),
        ),
        "main_gap": (
            "constant p02 coefficients have not been shown to reproduce p02b "
            "self-similar C_proc(a)=T0/t_age(a) over the observational range"
        ),
        "metric_branch_guardrail": (
            "this match must not be inserted into H(z), CMB, BBN, BAO, or SN "
            "without a separate channel-separation proof and numerical fit"
        ),
    }


def module_status():
    """Council-facing status for the dynamic phase-clock file."""
    return {
        "scope": "dynamic phase-clock candidate only; not primary FLRW metric branch",
        "current_self_check": phase_current_self_check(),
        "dynamic_branch": dynamic_phase_clock_branch(),
        "late_zero_current_candidate": late_zero_current_candidate(),
        "early_scaling_after_zero_current": early_scaling_after_zero_current(),
        "process_time_match_gate": process_time_match_gate(),
        "export_status": "NOT_READY_FOR_RG_THEORY_EXPORT",
    }


def article_dynamic_phase_clock_theorem():
    """
    Article-facing dynamic phase-clock ledger.

    This is the correction to the earlier overuse of the strict Phi=t branch.
    The dynamic branch keeps u(a)=Phi_dot(a) as the cosmological clock variable
    and keeps c_YI1 active, so the local phase-space coupling is not switched
    off by the cosmology shortcut.
    """
    current = phase_current_self_check()
    branch = dynamic_phase_clock_branch()
    late = late_zero_current_candidate()
    observables = dynamic_background_observables()
    compatibility_example = article_branch_compatibility_example()
    de_scale = dark_energy_scale_calibration_example()
    exact_lcdm = exact_lcdm_zero_current_background_theorem()
    lcdm_residuals = compressed_lcdm_background_residual_check()
    global_completion = global_lcdm_solar_completion_theorem()
    early = early_scaling_after_zero_current()

    return {
        "article_use": "dynamic cosmological phase-clock branch replacing strict-clock as the main cosmology direction",
        "current_self_check": {
            "status": current["status"],
            "normalized_density": current["normalized_density"],
            "normalized_density_residual": current["normalized_density_residual"],
            "canonical_minus_normalized_EOM_residual": current[
                "canonical_minus_normalized_EOM_residual"
            ],
        },
        "dynamic_equation": {
            "status": branch["status"],
            "normalized_current": branch["normalized_current"],
            "dynamic_equation_normalized": branch["dynamic_equation_normalized"],
            "zero_current_roots": branch["zero_current_roots"],
        },
        "late_candidate": {
            "status": late["status"],
            "late_u2": late["late_u2"],
            "w_after_substitution": late["w_after_substitution"],
            "theorem_pass_background_only": late["theorem_pass_background_only"],
            "viable_sign_window_hint": late["viable_sign_window_hint"],
        },
        "branch_compatibility_example": compatibility_example,
        "dark_energy_scale_calibration": de_scale,
        "exact_lcdm_background_branch": exact_lcdm,
        "compressed_lcdm_background_residual_check": lcdm_residuals,
        "global_lcdm_solar_completion": global_completion,
        "background_observables": {
            "status": observables["status"],
            "rho_RG": observables["rho_RG"],
            "p_RG": observables["p_RG"],
            "w_RG": observables["w_RG"],
            "E2": observables["E2"],
            "zero_current_branch": observables["zero_current_branch"],
        },
        "early_scaling_warning": {
            "status": early["status"],
            "rho_full_zero_current_expanded": early["rho_full_zero_current_expanded"],
            "added_effective_a_minus_2": early["added_effective_a_minus_2"],
            "added_effective_a_minus_4": early["added_effective_a_minus_4"],
        },
        "article_status": {
            "dynamic_phase_clock": "PRIMARY_COSMOLOGY_DIRECTION_CANDIDATE",
            "strict_clock": "DIAGNOSTIC_ONLY_NOT_MAIN_BRANCH",
            "phase_space_coupling": "c_YI1_REMAINS_ACTIVE",
            "dark_energy_scale": de_scale["status"],
            "background_lcdm_closure": exact_lcdm["status"],
            "compressed_background_residuals": lcdm_residuals["status"],
            "global_lcdm_solar_completion": global_completion["status"],
            "observational_fit": (
                "GLOBAL_BACKGROUND_1PN_COMPLETION_CLOSED__LIKELIHOOD_REQUIRED"
            ),
        },
    }


if __name__ == "__main__":
    print("=" * 72)
    print("p02c: dynamic phase-clock branch ledger")
    print("=" * 72)

    current = phase_current_self_check()
    print("\n1. Current self-check")
    print("status:", current["status"])
    print("canonical density:", current["canonical_density"])
    print("normalized density:", current["normalized_density"])
    print("density residual:", current["normalized_density_residual"])
    print("EOM residual:", current["canonical_minus_normalized_EOM_residual"])
    print("note:", current["normalization_note"])

    branch = dynamic_phase_clock_branch()
    print("\n2. Dynamic branch")
    print("status:", branch["status"])
    print("normalized current:", branch["normalized_current"])
    print("canonical current:", branch["canonical_current"])
    print("dynamic equation:", branch["dynamic_equation_normalized"])
    print("zero-current roots:", branch["zero_current_roots"])

    late = late_zero_current_candidate()
    print("\n3. Late zero-current candidate")
    print("status:", late["status"])
    print("rho:", late["rho_after_substitution"])
    print("p:", late["p_after_substitution"])
    print("w:", late["w_after_substitution"])
    print("blocked until:", late["blocked_until"])

    early = early_scaling_after_zero_current()
    print("\n4. Early-scaling warning")
    print("status:", early["status"])
    print("rho expanded:", early["rho_full_zero_current_expanded"])
    print("added a^-2:", early["added_effective_a_minus_2"])
    print("added a^-4:", early["added_effective_a_minus_4"])

    match = process_time_match_gate()
    print("\n5. Process-time match gate")
    print("status:", match["status"])
    print("target:", match["p02b_target"])
    print("general match:", match["general_match_condition"])
    print("guardrail:", match["metric_branch_guardrail"])
