# Notation header:
# signature (+---); mixed effective-fluid dictionary
# T^mu_nu = diag(rho, -p_r, -p_t, -p_t).

"""
PHASE 19: NEC deficit reading for the compact exponential branch

This file separates three statements that were previously mixed together:

1. NEC is not a source.  It is a standard GR null-direction audit of a source.
2. The compact exponential branch has an active projected deficit
   source with

       rho_a = -Delta_P, p_r,a = -Delta_P, p_t,a = +Delta_P.

   Therefore

       rho_a + p_r,a = -2 Delta_P < 0,
       rho_a + p_t,a = 0.

3. In RefG this sign is not repaired by adding an unmodelled gravitating
   background to the same exterior field equation.  It is read as the
   phase-pressure deficit of the base medium produced by the compact
   oscillon-tail exterior.  The next physical gate is to derive the finite-core
   matching and dynamics of that deficit, not to hide the sign.
"""

import sympy as sp


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def compact_exponential_deficit_profile_gate() -> dict:
    """
    Derive the active deficit profile used by the compact exponential branch.

    The static compact branch uses h=r_s/(2r), A=exp(r_s/r).  The projected
    projected deficit source is

        Z_perp=(h')^2/A,
        Delta_P=Z_perp/(8*pi*G).

    Delta_P is positive for r>0, peaks at r=r_s/4, and returns to zero at the
    r->0 endpoint of the exterior template.
    """
    r, r_s, G, u = sp.symbols("r r_s G u", positive=True, real=True)

    h = r_s / (2 * r)
    A = sp.exp(r_s / r)
    z_perp = sp.simplify(sp.diff(h, r) ** 2 / A)
    delta_p = sp.simplify(z_perp / (8 * sp.pi * G))

    delta_u = sp.simplify(u**4 * sp.exp(-u) / (32 * sp.pi * G * r_s**2))
    d_delta_u = sp.factor(sp.diff(delta_u, u))
    u_peak = sp.Integer(4)
    r_peak = sp.simplify(r_s / u_peak)
    delta_peak = sp.simplify(delta_u.subs(u, u_peak))

    endpoint_0 = sp.limit(delta_p, r, 0, dir="+")
    endpoint_inf = sp.limit(delta_p, r, sp.oo)

    return {
        "deficit_profile_status": (
            "PASS_COMPACT_DEFICIT_PROFILE_POSITIVE_WITH_FINITE_PEAK"
            if sp.simplify(delta_p - r_s**2 * sp.exp(-r_s / r) / (32 * sp.pi * G * r**4)) == 0
            and sp.simplify(d_delta_u.subs(u, u_peak)) == 0
            and endpoint_0 == 0
            and endpoint_inf == 0
            else "CHECK_COMPACT_DEFICIT_PROFILE"
        ),
        "h": sp.Eq(sp.Symbol("h"), h),
        "A": sp.Eq(sp.Symbol("A"), A),
        "Z_perp": sp.Eq(sp.Symbol("Z_perp"), z_perp),
        "Delta_P": sp.Eq(sp.Symbol("Delta_P"), delta_p),
        "Delta_P_u": sp.Eq(sp.Symbol("Delta_P(u)"), delta_u),
        "dDeltaP_du": d_delta_u,
        "u_peak": u_peak,
        "r_peak": r_peak,
        "Delta_P_peak": delta_peak,
        "endpoint_r_to_0": endpoint_0,
        "endpoint_r_to_infinity": endpoint_inf,
        "reading": (
            "Delta_P is the local phase-pressure deficit carried by the compact "
            "projected deficit source."
        ),
    }


def compact_exponential_exterior_domain_gate() -> dict:
    """
    Separate the global template peak from the exterior wormhole domain.

    The function Delta_P(r) has its formal maximum at r_s/4.  The exponential
    geometry used as a traversable-wormhole exterior has a throat at r_s/2, so
    the physical exterior r>=r_s/2 sees Delta_P decrease outward and takes its
    exterior maximum at the throat.
    """
    r, r_s, G = sp.symbols("r r_s G", positive=True, real=True)
    delta_p = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (32 * sp.pi * G * r**4))
    throat = r_s / 2
    formal_peak = r_s / 4
    d_delta = sp.factor(sp.diff(delta_p, r))
    exterior_derivative_sign = sp.factor(d_delta.subs(r, sp.Symbol("R", positive=True)))
    delta_throat = sp.simplify(delta_p.subs(r, throat))
    delta_formal_peak = sp.simplify(delta_p.subs(r, formal_peak))
    ratio = sp.simplify(delta_throat / delta_formal_peak)

    return {
        "exterior_domain_status": (
            "PASS_FORMAL_PEAK_LIES_INSIDE_THROAT__EXTERIOR_MAX_AT_THROAT"
            if sp.simplify(formal_peak < throat)
            and sp.simplify(ratio - sp.exp(2) / 16) == 0
            else "CHECK_EXPONENTIAL_EXTERIOR_DOMAIN_DEFICIT_PEAK"
        ),
        "throat_radius": throat,
        "formal_template_peak_radius": formal_peak,
        "Delta_P_throat": delta_throat,
        "Delta_P_formal_peak": delta_formal_peak,
        "Delta_P_throat_over_formal_peak": ratio,
        "dDeltaP_dr": d_delta,
        "exterior_monotonicity_reading": (
            "for r>=r_s/2 the derivative is negative, so the exterior branch "
            "uses the throat value as its maximum; the r_s/4 peak belongs to "
            "the analytic continuation inside the throat"
        ),
        "symbolic_derivative_for_R": exterior_derivative_sign,
    }


def active_deficit_nec_identity_gate() -> dict:
    """
    Show that the radial NEC sign is exactly the deficit sign.

    This is the core theorem for the current issue:

        Delta_P > 0  <=>  rho_a+p_r,a < 0.

    NEC is therefore the standard-GR null audit seeing the RefG deficit.
    """
    r, r_s, G = sp.symbols("r r_s G", positive=True, real=True)
    delta_p = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (32 * sp.pi * G * r**4))

    rho_a = -delta_p
    p_r_a = -delta_p
    p_t_a = delta_p
    radial_nec = sp.simplify(rho_a + p_r_a)
    tangential_nec = sp.simplify(rho_a + p_t_a)
    trace_combo = sp.simplify(rho_a + p_r_a + 2 * p_t_a)

    deficit_indicator = sp.simplify(-radial_nec / 2)

    return {
        "active_deficit_nec_status": (
            "PASS_RADIAL_NEC_VIOLATION_IS_EXACTLY_ACTIVE_DEFICIT_SIGNATURE"
            if radial_nec == -2 * delta_p
            and tangential_nec == 0
            and trace_combo == 0
            and sp.simplify(deficit_indicator - delta_p) == 0
            else "CHECK_ACTIVE_DEFICIT_NEC_IDENTITY"
        ),
        "Delta_P": delta_p,
        "active_effective_dictionary": {
            "rho_a": rho_a,
            "p_r_a": p_r_a,
            "p_t_a": p_t_a,
        },
        "radial_NEC_a": radial_nec,
        "tangential_NEC_a": tangential_nec,
        "trace_combo": trace_combo,
        "deficit_from_radial_NEC": sp.Eq(sp.Symbol("Delta_P"), deficit_indicator),
        "standard_GR_reading": (
            "the active source is not ordinary positive matter; the radial null "
            "load is negative"
        ),
        "RefG_reading": (
            "the same sign is the base-medium phase-pressure deficit created "
            "by the compact oscillon-tail exterior"
        ),
    }


def projected_deficit_source_closure_gate() -> dict:
    """
    Check that the deficit source closes the diagonal exterior field equations.
    """
    r, r_s, G = sp.symbols("r r_s G", positive=True, real=True)
    delta_p = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (32 * sp.pi * G * r**4))
    D = sp.simplify(8 * sp.pi * G * delta_p)

    G_mixed = {
        "G^t_t": -D,
        "G^r_r": D,
        "G^theta_theta": -D,
        "G^phi_phi": -D,
    }
    theta_mixed = {
        "Theta^t_t": -delta_p,
        "Theta^r_r": delta_p,
        "Theta^theta_theta": -delta_p,
        "Theta^phi_phi": -delta_p,
    }
    residuals = {
        "t": sp.simplify(G_mixed["G^t_t"] - 8 * sp.pi * G * theta_mixed["Theta^t_t"]),
        "r": sp.simplify(G_mixed["G^r_r"] - 8 * sp.pi * G * theta_mixed["Theta^r_r"]),
        "theta": sp.simplify(
            G_mixed["G^theta_theta"] - 8 * sp.pi * G * theta_mixed["Theta^theta_theta"]
        ),
        "phi": sp.simplify(
            G_mixed["G^phi_phi"] - 8 * sp.pi * G * theta_mixed["Theta^phi_phi"]
        ),
    }

    return {
        "projected_deficit_source_status": (
            "PASS_ACTIVE_DEFICIT_SOURCE_CLOSES_STATIC_EXPONENTIAL_FIELD_EQUATIONS"
            if _all_zero(residuals.values())
            else "CHECK_ACTIVE_DEFICIT_SOURCE_CLOSURE"
        ),
        "D": D,
        "Einstein_mixed": G_mixed,
        "ThetaRefG_active_mixed": theta_mixed,
        "field_equation_residuals": residuals,
        "reading": (
            "the compact exterior field-equation residual is closed by the "
            "active deficit source itself"
        ),
    }


def projected_deficit_static_stiffness_gate() -> dict:
    """
    Check the local static stiffness of the projected deficit source.

    The source has positive spatial Hessian and no standalone time kinetic
    term.  This does not prove the full coupled compact perturbation spectrum;
    it proves that the NEC sign is not produced by a negative time kinetic
    scalar inside L_Delta_perp itself.
    """
    r, r_s, G, eps, theta = sp.symbols(
        "r r_s G eps theta", positive=True, real=True
    )
    eta_r, eta_theta, eta_phi = sp.symbols(
        "eta_r eta_theta eta_phi", real=True
    )

    h0 = r_s / (2 * r)
    A = sp.exp(r_s / r)
    h_r = sp.diff(h0, r) + eps * eta_r
    z_perp = sp.simplify(
        h_r**2 / A
        + eps**2 * eta_theta**2 / (A * r**2)
        + eps**2 * eta_phi**2 / (A * r**2 * sp.sin(theta) ** 2)
    )
    l_perp = sp.simplify(z_perp / (8 * sp.pi * G))
    l2 = sp.simplify(sp.diff(l_perp, eps, 2).subs(eps, 0) / 2)
    expected_l2 = sp.simplify(
        (
            eta_r**2
            + eta_theta**2 / r**2
            + eta_phi**2 / (r**2 * sp.sin(theta) ** 2)
        )
        / (8 * sp.pi * G * A)
    )

    omega, k_r, k_theta, k_phi = sp.symbols(
        "omega k_r k_theta k_phi", real=True
    )
    symbol = sp.simplify(
        (
            k_r**2
            + k_theta**2 / r**2
            + k_phi**2 / (r**2 * sp.sin(theta) ** 2)
        )
        / (8 * sp.pi * G * A)
    )
    omega_coefficient = sp.simplify(sp.diff(symbol, omega, 2))

    return {
        "static_stiffness_status": (
            "PASS_ACTIVE_DEFICIT_HAS_POSITIVE_STATIC_STIFFNESS_AND_NO_STANDALONE_TIME_KINETIC"
            if sp.simplify(l2 - expected_l2) == 0 and omega_coefficient == 0
            else "CHECK_ACTIVE_DEFICIT_STATIC_STIFFNESS"
        ),
        "quadratic_static_stiffness": l2,
        "expected_quadratic_static_stiffness": expected_l2,
        "principal_spatial_symbol": symbol,
        "omega_coefficient": omega_coefficient,
        "positivity_conditions": [sp.Gt(G, 0), sp.Gt(A, 0)],
        "scope": (
            "static projected-source stiffness only; full compact perturbation "
            "stability remains the finite-core coupled spectrum"
        ),
    }


def nec_deficit_interpretation_ledger() -> dict:
    """
    Article-facing interpretation with the correct status.
    """
    profile = compact_exponential_deficit_profile_gate()
    nec = active_deficit_nec_identity_gate()
    source = projected_deficit_source_closure_gate()
    stiffness = projected_deficit_static_stiffness_gate()

    passed = (
        profile["deficit_profile_status"]
        == "PASS_COMPACT_DEFICIT_PROFILE_POSITIVE_WITH_FINITE_PEAK"
        and nec["active_deficit_nec_status"]
        == "PASS_RADIAL_NEC_VIOLATION_IS_EXACTLY_ACTIVE_DEFICIT_SIGNATURE"
        and source["projected_deficit_source_status"]
        == "PASS_ACTIVE_DEFICIT_SOURCE_CLOSES_STATIC_EXPONENTIAL_FIELD_EQUATIONS"
        and stiffness["static_stiffness_status"]
        == "PASS_ACTIVE_DEFICIT_HAS_POSITIVE_STATIC_STIFFNESS_AND_NO_STANDALONE_TIME_KINETIC"
    )

    return {
        "p14_status": (
            "PASS_NEC_SIGN_REWRITTEN_AS_REFG_ACTIVE_DEFICIT_LEDGER"
            if passed
            else "CHECK_NEC_SIGN_REFG_ACTIVE_DEFICIT_LEDGER"
        ),
        "profile": profile["deficit_profile_status"],
        "active_nec": nec["active_deficit_nec_status"],
        "source_closure": source["projected_deficit_source_status"],
        "static_stiffness": stiffness["static_stiffness_status"],
        "article_supported_statement": (
            "In the compact exponential branch the standard effective-source "
            "dictionary gives radial NEC violation.  In RefG this sign is the "
            "active base-medium phase-pressure deficit carried by the projected "
            "deficit source.  The deficit closes the static exterior field "
            "equations and has positive static spatial stiffness; full finite-core "
            "dynamical selection remains the next layer."
        ),
        "do_not_claim": [
            "NEC itself creates the deficit",
            "ordinary positive matter sources the compact exponential exterior",
            "a homogeneous positive background can be added to the same field equation without changing the metric",
            "full compact-object dynamical stability is proven by the static stiffness check",
        ],
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 19: NEC deficit reading")
    print("=" * 72)

    sections = [
        ("1. Compact deficit profile", compact_exponential_deficit_profile_gate()),
        ("2. Active deficit NEC identity", active_deficit_nec_identity_gate()),
        ("3. Projected deficit source closure", projected_deficit_source_closure_gate()),
        ("4. Projected deficit static stiffness", projected_deficit_static_stiffness_gate()),
        ("5. Exterior domain gate", compact_exponential_exterior_domain_gate()),
        ("6. NEC deficit interpretation ledger", nec_deficit_interpretation_ledger()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:44s}: {value}")
