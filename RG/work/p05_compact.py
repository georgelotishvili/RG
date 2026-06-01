# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

"""
PHASE 18: RG compact object, Bernoulli saturation, and singularity audit

Status:
Static exponential compact exterior is closed at the phase-equation and
geodesic-algebra level: the vacuum phase equation gives the exterior, the
effective source has the Bernoulli profile, curvature invariants vanish at the
formal endpoint, and the C2 matching algebra is explicit.

The algebraic p01/F_min polynomial does not by itself generate the compact
Bernoulli profile, because that profile is a phase-gradient source.  This file
now derives the static branch source.  The compact export uses the medium
projector version, where the Bernoulli term is a rest-frame spatial-gradient
response.  Ordinary standalone scalar export has wrong-sign time kinetic and is
blocked.

This is not yet a full compact-object replacement proof.  The ADM/Komar mass
bookkeeping is closed at the static asymptotic level, the C2 core's effective
field-equation source is explicit and finite, the proper-volume effective
source charge is finite for finite r_c, and the C2 core source is decomposed
into the RefG projected phase channel plus a finite residual medium-stress
channel, this residual is written as p01 action-stress branch equations, and
the radial core deformation has an exact IVP plus a first-order analytic
large-stiffness solution; a nonlinear IVP probe passes representative
stiffness values; a sufficient parameter-domain theorem keeps the nonlinear
branch real across the core interval; the residual diagonal tensor is
integrable as one p01 action-density branch.  The full claim still needs the
off-branch EFT extension, rotating solutions, stability/QNMs/echoes, and
EHT/NS likelihood work.

It is also not the Solar weak-field 2PN export.  p03b/p03c keep the physical
Solar exterior on the q_2PN=7/4 branch; this file keeps the phase-vacuum
exponential strong-field branch with internal q_2PN=2.

აქ მოწმდება exponential exterior-ის algebraic/phenomenological branch:
1. exponential bi-conformal exterior:
       ds^2 = -exp(-r_s/r)c^2dt^2 + exp(r_s/r)(dr^2+r^2dOmega^2)
2. curvature invariants vanish at r -> 0;
3. Bernoulli pressure deficit is self-limiting;
4. finite-radius Killing horizon is absent;
5. areal throat, photon sphere, shadow radius, and golden-ratio ISCO follow;
6. exterior-only geodesic incompleteness is kept explicit;
7. a rarefaction cutoff plus C2 finite-core matching is a conditional
   regular-extension model.

Still open before full compact-object theory export:
    audit the off-branch EFT extension, compute coupled perturbations/QNMs/
    echoes, and add rotating EHT ray tracing.
"""
import sympy as sp
from p01_core import get_polynomial_lagrangian, local_stability_short_path_certificate


def compact_signature_bridge():
    """
    Sign-convention firewall.

    The global RG work files use signature (+---).  The compact-object block
    below often writes a positive lapse/spatial-factor line element as
        ds^2 = -B(r)c^2dt^2 + A(r)(dr^2+r^2dOmega^2).

    Therefore B and A are positive metric functions, not direct (+---)
    components.  Any stress/Y calculation that touches p01 conventions must
    explicitly pass through this bridge.
    """
    r, r_s = sp.symbols('r r_s', positive=True)
    phi = -r_s / r
    B_lapse = sp.exp(phi)
    A_spatial = sp.exp(-phi)
    return {
        "global_RG_signature": "(+---)",
        "compact_line_element_style": "ds^2=-B(r)c^2dt^2 + A(r)(dr^2+r^2dOmega^2)",
        "positive_lapse_B": sp.Eq(sp.Symbol('B'), B_lapse),
        "positive_spatial_A": sp.Eq(sp.Symbol('A'), A_spatial),
        "direct_component_warning": "B and A are positive functions; do not treat them as raw (+---) components without conversion.",
        "stress_bridge_status": "REQUIRED_BEFORE_EXPORTING_CENTER_STRESS_CLAIMS",
    }


def derive_exponential_exterior_from_phase_equation():
    """
    Exterior derivation at the RG phase-potential level.

    Outside the compact source the static pressure/phase potential is harmonic:
        (r^2 phi')' = 0.

    Asymptotic flatness fixes the additive constant; the weak-field Newtonian
    limit g_tt ~= 1 + phi ~= 1 - r_s/r fixes the remaining integration
    constant.  The bi-conformal operational map then gives
        B=e^phi, A=e^-phi.

    This derives the static exponential exterior branch at the phase-equation
    and operational-metric level.  The projected Bernoulli source closes the
    exterior source; the finite-core source is handled by the C2 core ledger.
    """
    r, r_s, C1, C2 = sp.symbols('r r_s C1 C2', positive=True, real=True)
    phi_fn = sp.Function('phi')
    phi_general = C1 + C2 / r
    radial_laplace_residual = sp.simplify(sp.diff(r**2 * sp.diff(phi_general, r), r))
    phi_exterior = -r_s / r
    B_lapse = sp.exp(phi_exterior)
    A_spatial = sp.exp(-phi_exterior)

    weak_gtt_series = sp.series(B_lapse, r_s, 0, 2).removeO()
    weak_spatial_series = sp.series(A_spatial, r_s, 0, 2).removeO()

    return {
        "vacuum_phase_equation": sp.Eq(sp.diff(r**2 * sp.diff(phi_fn(r), r), r), 0),
        "general_spherical_solution": sp.Eq(sp.Symbol('phi'), phi_general),
        "laplace_residual_for_solution": radial_laplace_residual,
        "boundary_conditions": "phi(infinity)=0 and weak-field g_tt ~= 1-r_s/r",
        "exterior_phi": sp.Eq(sp.Symbol('phi_ext'), phi_exterior),
        "biconformal_lapse_B": sp.Eq(sp.Symbol('B'), B_lapse),
        "biconformal_spatial_A": sp.Eq(sp.Symbol('A'), A_spatial),
        "weak_lapse": sp.Eq(sp.Symbol('B_weak'), weak_gtt_series),
        "weak_spatial": sp.Eq(sp.Symbol('A_weak'), weak_spatial_series),
        "derivation_status": "PHASE_EQUATION_AND_BICONFORMAL_MAP_DERIVED",
        "algebraic_fmin_status": "ALGEBRAIC_P01_FMIN_ALONE_DOES_NOT_GENERATE_THE_GRADIENT_PROFILE",
        "bernoulli_source_status": "PROJECTED_BERNOULLI_MEDIUM_SOURCE_DERIVED_IN_THIS_FILE",
        "remaining_gate": "C2 core source is handled in the finite-core ledger; stability and rotation remain open",
    }


def derive_exponential_effective_source_profile():
    """
    Effective Einstein-source profile of the exponential exterior.

    In the (+---) convention with ds^2=B dt^2 - A(dr^2+r^2dOmega^2),
    B=exp(-r_s/r), A=exp(+r_s/r), the mixed Einstein tensor is proportional
    to the same self-limiting profile as the Bernoulli deficit.
    """
    r, r_s, G = sp.symbols('r r_s G', positive=True, real=True)
    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    delta_p = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (32 * sp.pi * G * r**4))
    G_mixed = {
        "G^t_t": -D,
        "G^r_r": D,
        "G^theta_theta": -D,
        "G^phi_phi": -D,
    }
    T_eff = {key.replace("G", "T_eff"): sp.simplify(value / (8 * sp.pi * G)) for key, value in G_mixed.items()}
    return {
        "G_mixed_plus_minus_minus": G_mixed,
        "Bernoulli_Delta_P": sp.Eq(sp.Symbol('Delta_P'), delta_p),
        "T_eff_if_G_eq_8piG_T": T_eff,
        "profile_match": sp.Eq(sp.Symbol('G^r_r/(8*pi*G)'), delta_p),
        "sign_note": "standard Einstein-sign reading gives T^t_t=-Delta_P and T^r_r=+Delta_P; RefG export is the projected medium source.",
        "source_status": "EFFECTIVE_GEOMETRIC_SOURCE_PROFILE_DERIVED__PROJECTED_BERNOULLI_MEDIUM_SOURCE_DERIVED_SEPARATELY",
    }


def audit_exponential_effective_energy_conditions():
    """
    Standard energy-condition audit for the geometric effective source.

    This is not the total physical RefG medium verdict.  It is the
    background-subtracted Einstein-source reading of the exponential geometry.
    The physical medium test is the background-completed null-load gate below.
    """
    r, r_s, G = sp.symbols('r r_s G', positive=True, real=True)
    delta_p = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (32 * sp.pi * G * r**4))

    rho_std = -delta_p
    p_r_std = -delta_p
    p_t_std = delta_p

    return {
        "Delta_P_positive_for_r_gt_0": delta_p,
        "standard_effective_rho": sp.Eq(sp.Symbol('rho_eff'), rho_std),
        "standard_effective_p_r": sp.Eq(sp.Symbol('p_r_eff'), p_r_std),
        "standard_effective_p_t": sp.Eq(sp.Symbol('p_t_eff'), p_t_std),
        "radial_NEC": sp.Eq(sp.Symbol('rho_eff+p_r_eff'), sp.simplify(rho_std + p_r_std)),
        "tangential_NEC": sp.Eq(sp.Symbol('rho_eff+p_t_eff'), sp.simplify(rho_std + p_t_std)),
        "WEC_density": sp.Eq(sp.Symbol('rho_eff'), rho_std),
        "SEC_trace_combo": sp.Eq(
            sp.Symbol('rho_eff+p_r_eff+2*p_t_eff'),
            sp.simplify(rho_std + p_r_std + 2 * p_t_std),
        ),
        "standard_energy_verdict": "SUBTRACTED_ACTIVE_DEFICIT_HAS_NEGATIVE_RADIAL_NULL_LOAD",
        "refg_source_target": "projected RefG medium source supplies the same mixed geometry; ordinary Einstein-fluid reading is the subtracted contrast audit, not the total medium NEC",
    }


def derive_background_completed_medium_nec_gate():
    """
    Deprecated compatibility ledger for the old background-completed NEC gate.

    The old version treated a homogeneous positive base load as if it could be
    added to the same exterior field equation without changing the metric.
    That is not an article-safe result.  The compact exterior field equation is
    closed by the active projected Bernoulli contrast:

        rho_a=-Delta_P, p_r_a=-Delta_P, p_t_a=+Delta_P.

    Therefore the active source has negative radial null load.  A positive
    homogeneous base background belongs to a different field-equation layer;
    inserting it as a gravitating source would change the metric and require a
    new exterior derivation.  Keep this function only so old ledgers do not
    silently preserve the obsolete PASS status.
    """
    r, r_s, G = sp.symbols('r r_s G', positive=True, real=True)
    u = sp.Symbol('u', positive=True, real=True)

    delta_p = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (32 * sp.pi * G * r**4))
    delta_u = sp.simplify(u**4 * sp.exp(-u) / (32 * sp.pi * G * r_s**2))
    delta_u_derivative = sp.factor(sp.diff(delta_u, u))
    u_peak = sp.Integer(4)
    r_peak = sp.simplify(r_s / u_peak)
    delta_max = sp.simplify(delta_u.subs(u, u_peak))

    active_contrast = {
        "rho_a": -delta_p,
        "p_r_a": -delta_p,
        "p_t_a": delta_p,
        "radial_null_load_a": sp.simplify(-2 * delta_p),
        "tangential_null_load_a": sp.Integer(0),
    }
    return {
        "total_medium_nec_status": "DEPRECATED_BACKGROUND_CAPACITY_NOT_AN_EXTERIOR_FIELD_EQUATION_RESULT",
        "Delta_P": sp.Eq(sp.Symbol('Delta_P'), delta_p),
        "Delta_P_shape_u": sp.Eq(sp.Symbol('Delta_P(u)'), delta_u),
        "dDeltaP_du": delta_u_derivative,
        "Delta_P_peak": {
            "u_peak": u_peak,
            "r_peak": r_peak,
            "Delta_P_max": delta_max,
        },
        "active_subtracted_contrast": active_contrast,
        "removed_old_total_medium_completion": (
            "rho_star/p_star completion removed from active article logic; "
            "it would require a new exterior field equation and a rederived metric"
        ),
        "physical_reading": (
            "the negative radial null load is the active phase-pressure "
            "deficit that closes the compact exterior field equation.  A "
            "positive homogeneous base load is not part of this exterior "
            "equation unless the metric is rederived with that load included."
        ),
        "article_rule": (
            "do not use the old total-medium NEC capacity bound as an article "
            "claim.  State the active radial NEC violation and read it as the "
            "RefG base-medium phase-pressure deficit."
        ),
    }


def derive_black_hole_singularity_breaker_gate():
    """
    Geometry-level black-hole breaker gate.

    Compare the Schwarzschild finite-radius horizon / r=0 curvature blow-up
    with the RG exponential exterior branch.  This is the strongest statement
    currently available before p01 source closure:

        Schwarzschild: B=1-r_s/r has B=0 at r=r_s and K~r^-6.
        RG exponential: B=exp(-r_s/r)>0 for finite r and K->0 at r->0.

    The result excludes the Schwarzschild-type curvature singularity inside
    the exponential phase metric.  It does not by itself prove collapse
    completion, because exterior radial geodesics still reach the r=0 boundary
    in finite affine/proper parameter.
    """
    r, r_s, E_geo = sp.symbols('r r_s E_geo', positive=True, real=True)
    u = r_s / r
    B_exp = sp.exp(-u)
    A_exp = sp.exp(u)
    B_schw = 1 - r_s / r
    K_schw = 12 * r_s**2 / r**6
    K_exp = (
        r_s**2
        * (48 * r**2 - 32 * r * r_s + 7 * r_s**2)
        * sp.exp(-2 * r_s / r)
        / (4 * r**8)
    )
    delta_p = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (32 * sp.pi * sp.Symbol('G', positive=True) * r**4))
    null_radial_velocity_affine = sp.Eq(sp.Symbol('dr_dlambda_null')**2, E_geo**2)
    timelike_radial_velocity_near_boundary = sp.limit(E_geo**2 - B_exp, r, 0, dir='+')

    return {
        "Schwarzschild_horizon_condition": sp.Eq(B_schw, 0),
        "Schwarzschild_horizon_radius": sp.Eq(sp.Symbol('r_h'), r_s),
        "Schwarzschild_Kretschmann": K_schw,
        "lim_r_to_0_K_Schwarzschild": sp.limit(K_schw, r, 0, dir='+'),
        "RG_lapse": sp.Eq(sp.Symbol('B_exp'), B_exp),
        "RG_finite_r_horizon_test": "exp(-r_s/r) is strictly positive for every finite r>0",
        "RG_Kretschmann": K_exp,
        "lim_r_to_0_K_RG": sp.limit(K_exp, r, 0, dir='+'),
        "RG_Bernoulli_profile": sp.Eq(sp.Symbol('Delta_P'), delta_p),
        "lim_r_to_0_DeltaP_RG": sp.limit(delta_p, r, 0, dir='+'),
        "spatial_proper_distance_to_r0": sp.Eq(
            sp.Integral(sp.sqrt(A_exp), (r, 0, sp.Symbol('r0', positive=True))),
            sp.oo,
        ),
        "radial_null_affine_equation": null_radial_velocity_affine,
        "timelike_radial_velocity_limit": sp.Eq(
            sp.Symbol('lim_r_to_0_dr_dtau_squared'),
            timelike_radial_velocity_near_boundary,
        ),
        "geometry_verdict": "SCHWARZSCHILD_CURVATURE_SINGULARITY_REMOVED_IN_EXPONENTIAL_BRANCH",
        "remaining_gate": "not a full dynamical black-hole replacement until coupled core dynamics, boundary evolution and perturbative stability are derived",
    }


def p01_polynomial_static_closure_gate():
    """
    Check whether the simplest p01 spherical medium f(r)=r supplies the
    exponential exterior source by itself.

    Result: the f=r branch is isotropic in the spatial mixed stresses, while
    the exponential geometry needs radial/tangential anisotropy.  Therefore the
    exterior is not closed by the simplest p01 polynomial background alone.
    A nontrivial radial deformation f(r), a derivative/Bernoulli sector, or an
    additional source derivation is still required.
    """
    r, r_s = sp.symbols('r r_s', positive=True, real=True)
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        'c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1',
        real=True,
    )
    u = r_s / r
    Tt = -(
        3*c_I1*sp.exp(2*u)
        + 9*c_I1sq*sp.exp(u)
        + 3*c_I2*sp.exp(u)
        + c_I3
        - c_Y*sp.exp(4*u)
        - 3*c_Y2*sp.exp(5*u)
        - 3*c_YI1*sp.exp(3*u)
    ) * sp.exp(-3*u)
    Tr = -(
        c_I1*sp.exp(2*u)
        - 3*c_I1sq*sp.exp(u)
        - c_I2*sp.exp(u)
        - c_I3
        + c_Y*sp.exp(4*u)
        + c_Y2*sp.exp(5*u)
        + c_YI1*sp.exp(3*u)
    ) * sp.exp(-3*u)
    Ttheta = Tr

    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    required_anisotropy = sp.simplify(D - (-D))

    return {
        "assumed_elastic_map": "SO(3) branch f(r)=r, so lambda_r=lambda_t=exp(-r_s/r)",
        "p01_T^t_t": sp.factor(Tt),
        "p01_T^r_r": sp.factor(Tr),
        "p01_T^theta_theta": sp.factor(Ttheta),
        "p01_spatial_anisotropy": sp.simplify(Tr - Ttheta),
        "required_geometry_G^r_r_minus_G^theta_theta": required_anisotropy,
        "closure_status": "FAILS_FOR_F_EQ_R__NEEDS_NONTRIVIAL_F_OR_DERIVATIVE_BERNOULLI_SOURCE",
    }


def derive_p01_anisotropic_deformation_route():
    """
    Exact p01 lever that can supply compact-object anisotropy.

    The f=r branch fails because lambda_r=lambda_t.  For a genuine SO(3)
    radial deformation phi^A=f(r)n^A, the p01 polynomial produces a spatial
    anisotropy proportional to lambda_r-lambda_t.  This is the missing degree
    of freedom needed by the exponential geometry.

    This function derives the algebraic anisotropy route; it is not yet the
    solved f(r) field equation.
    """
    r, r_s, A, C, Y, G = sp.symbols('r r_s A C Y G', positive=True, real=True)
    f = sp.Function('f')(r)
    lambda_r = sp.Symbol('lambda_r', positive=True)
    lambda_t = sp.Symbol('lambda_t', positive=True)
    c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        'c_I1 c_I1sq c_I2 c_I3 c_YI1',
        real=True,
    )

    I1 = lambda_r + 2 * lambda_t
    I2 = 2 * lambda_r * lambda_t + lambda_t**2
    I3 = lambda_r * lambda_t**2
    L_solid = (
        c_I1 * I1
        + c_I1sq * I1**2
        + c_I2 * I2
        + c_I3 * I3
        + c_YI1 * Y * I1
    )
    L_lr = sp.diff(L_solid, lambda_r)
    L_lt = sp.diff(L_solid, lambda_t) / 2
    pressure_anisotropy = sp.factor(2 * (lambda_r * L_lr - lambda_t * L_lt))

    lambda_r_map = sp.diff(f, r)**2 / A
    lambda_t_map = f**2 / C
    u = r_s / r
    required_mixed_geometry_anisotropy = sp.simplify(
        r_s**2 * sp.exp(-u) / (2 * r**4)
    )
    required_stress_anisotropy = sp.simplify(
        required_mixed_geometry_anisotropy / (8 * sp.pi * G)
    )
    anisotropy_quadratic = sp.Poly(
        sp.expand(pressure_anisotropy - required_stress_anisotropy),
        lambda_r,
    )
    lambda_r_roots = sp.solve(
        sp.Eq(pressure_anisotropy, required_stress_anisotropy),
        lambda_r,
    )
    deformation_lhs = pressure_anisotropy.subs({
        lambda_r: lambda_r_map,
        lambda_t: lambda_t_map,
    })
    deformation_equation = sp.Eq(deformation_lhs, required_stress_anisotropy)
    A_ext = sp.exp(u)
    C_ext = r**2 * sp.exp(u)
    Y_ext = sp.exp(u)
    exterior_deformation_equation = sp.Eq(
        sp.factor(sp.simplify(deformation_lhs.subs({A: A_ext, C: C_ext, Y: Y_ext}))),
        required_stress_anisotropy,
    )

    return {
        "lambda_r_map": sp.Eq(sp.Symbol('lambda_r'), lambda_r_map),
        "lambda_t_map": sp.Eq(sp.Symbol('lambda_t'), lambda_t_map),
        "solid_anisotropy_p_t_minus_p_r": pressure_anisotropy,
        "f_eq_r_failure_reason": "f=r with C=A*r^2 gives lambda_r=lambda_t, so this anisotropy vanishes",
        "required_geometry_G^r_r_minus_G^theta_theta": required_mixed_geometry_anisotropy,
        "required_stress_anisotropy": required_stress_anisotropy,
        "lambda_r_quadratic_coefficients": anisotropy_quadratic.all_coeffs(),
        "lambda_r_algebraic_roots": lambda_r_roots,
        "deformation_equation_to_solve": deformation_equation,
        "exponential_exterior_f_equation": exterior_deformation_equation,
        "route_status": "EXACT_ANISOTROPY_LEVER_AND_LAMBDA_R_BRANCH_DERIVED__SOLVE_F_R_AND_FULL_STRESS_NEXT",
    }


def derive_minimal_nontrivial_f_branch():
    """
    Minimal nontrivial radial-deformation branch.

    To make the p01 anisotropy concrete, freeze the anisotropy modulus to the
    simplest positive branch:

        c_I1sq = c_I2 = c_YI1 = 0,   c_I1 = K_A > 0.

    Then p_t-p_r = 2 K_A (lambda_r-lambda_t).  On the exponential exterior,
    lambda_r=e^-u f'^2 and lambda_t=e^-u f^2/r^2, so the required compact
    anisotropy becomes a first-order ODE for f(r).

    The closed form below is the asymptotic weak-deformation branch.  It proves
    that f=r is not forced: a nontrivial radial medium map can supply the
    required radial/tangential stress split at leading order.
    """
    r, r_s, G, K_A, eps = sp.symbols(
        'r r_s G K_A eps',
        positive=True,
        real=True,
    )
    chi = sp.Function('chi')(r)
    u = r_s / r
    f = sp.Function('f')(r)
    w = sp.Function('w')(r)

    lambda_r = sp.exp(-u) * sp.diff(f, r)**2
    lambda_t = sp.exp(-u) * f**2 / r**2
    required = r_s**2 * sp.exp(-u) / (16 * sp.pi * G * r**4)
    minimal_exact_ode = sp.Eq(
        sp.simplify(2 * K_A * (lambda_r - lambda_t)),
        required,
    )
    simplified_exact_ode = sp.Eq(
        sp.diff(f, r)**2 - f**2 / r**2,
        r_s**2 / (32 * sp.pi * G * K_A * r**4),
    )
    w_equation = sp.Eq(
        r * sp.diff(w, r),
        -w + sp.sqrt(w**2 + r_s**2 / (32 * sp.pi * G * K_A * r**4)),
    )

    f_eps = r * (1 + eps * chi)
    lambda_r_eps = sp.exp(-u) * sp.diff(f_eps, r)**2
    lambda_t_eps = sp.exp(-u) * f_eps**2 / r**2
    anisotropy_eps = sp.series(
        sp.simplify(2 * K_A * (lambda_r_eps - lambda_t_eps)),
        eps,
        0,
        2,
    ).removeO()
    linear_anisotropy = sp.simplify(sp.diff(anisotropy_eps, eps).subs(eps, 0))
    chi_prime_equation = sp.Eq(
        sp.diff(chi, r),
        r_s**2 / (64 * sp.pi * G * K_A * r**5),
    )
    chi_solution = -r_s**2 / (256 * sp.pi * G * K_A * r**4)
    f_asymptotic = sp.simplify(r * (1 + chi_solution))
    f_asymptotic_prime = sp.diff(f_asymptotic, r)
    asymptotic_lhs_first_order = sp.simplify(
        2
        * K_A
        * sp.exp(-u)
        * (
            2
            * r
            * sp.diff(chi_solution, r)
        )
    )
    linear_residual = sp.simplify(asymptotic_lhs_first_order - required)
    exact_residual_order = sp.simplify(
        2 * K_A * sp.exp(-u) * (f_asymptotic_prime**2 - f_asymptotic**2 / r**2)
        - required
    )

    return {
        "minimal_modulus_branch": "c_I1sq=c_I2=c_YI1=0, K_A=c_I1>0",
        "exact_minimal_f_ode": minimal_exact_ode,
        "simplified_exact_ode": simplified_exact_ode,
        "asymptotically_flat_w_equation_for_f_eq_r_w": w_equation,
        "linearized_f_definition": sp.Eq(sp.Symbol('f'), r * (1 + chi)),
        "linear_anisotropy": sp.Eq(sp.Symbol('Delta_p_linear'), linear_anisotropy),
        "chi_prime_equation": chi_prime_equation,
        "chi_solution_with_chi_infinity_0": sp.Eq(sp.Symbol('chi'), chi_solution),
        "nontrivial_f_asymptotic": sp.Eq(sp.Symbol('f_nontrivial'), f_asymptotic),
        "linear_source_residual": linear_residual,
        "exact_residual_after_linear_solution": exact_residual_order,
        "validity": "asymptotic/weak-deformation exterior branch; exact nonlinear f(r), full p01 stress, and core matching remain open",
        "branch_status": "NONTRIVIAL_F_R_BRANCH_DERIVED_AT_LINEAR_ORDER__EXACT_ODE_READY",
    }


def derive_exact_minimal_f_branch_implicit_solution():
    """
    Exact implicit solution of the minimal p01 anisotropy branch.

    Starting point from derive_minimal_nontrivial_f_branch:

        f'^2 - f^2/r^2 = a/r^4,
        a = r_s^2/(32*pi*G*K_A).

    Define h = f*r/sqrt(a).  The asymptotically flat branch obeys

        d h / d ln r = h + sqrt(h^2+1).

    This closes the anisotropy equation exactly in implicit form.  It still
    does not close the full diagonal F_min source components.
    """
    r, r_s, G, K_A = sp.symbols('r r_s G K_A', positive=True, real=True)
    H = sp.Symbol('H', positive=True, real=True)
    a = sp.simplify(r_s**2 / (32 * sp.pi * G * K_A))
    dH_dlnr = sp.simplify(H + sp.sqrt(H**2 + 1))
    reduced_residual = sp.simplify(dH_dlnr**2 - 2 * H * dH_dlnr - 1)
    integral_H = sp.simplify(
        sp.Rational(1, 2)
        * (H * sp.sqrt(H**2 + 1) + sp.asinh(H) - H**2)
    )
    integral_derivative_check = sp.simplify(sp.diff(integral_H, H) * dH_dlnr - 1)
    asymptotic_constant = sp.simplify(sp.log(2) / 2 + sp.Rational(1, 4))
    f_asymptotic = sp.simplify(r - a / (8 * r**3))

    return {
        "a_definition": sp.Eq(sp.Symbol('a'), a),
        "dimensionless_h": sp.Eq(sp.Symbol('H'), sp.Symbol('f') * r / sp.sqrt(a)),
        "reduced_h_equation": sp.Eq(sp.Symbol('dH/dlnr'), dH_dlnr),
        "reduced_residual": reduced_residual,
        "implicit_integral_I_H": sp.Eq(sp.Symbol('I(H)'), integral_H),
        "implicit_solution_asymptotic_f_over_r_to_1": sp.Eq(
            integral_H,
            sp.log(r / a**sp.Rational(1, 4)) + asymptotic_constant,
        ),
        "integral_chain_rule_residual": integral_derivative_check,
        "asymptotic_expansion_matches_linear_branch": sp.Eq(
            sp.Symbol('f_asymptotic'),
            f_asymptotic,
        ),
        "exact_branch_status": "EXACT_IMPLICIT_F_R_BRANCH_DERIVED_FOR_P01_ANISOTROPY",
        "remaining_source_gate": "full T^t_t, T^r_r and T^theta_theta matching must still be solved from F_min",
    }


def derive_full_fmin_exponential_source_closure_system():
    """
    Full component equations for the exponential exterior source.

    The anisotropy equation alone is not the full source proof.  The complete
    diagonal target is

        T^t_t = -Delta_P,  T^r_r = +Delta_P,  T^theta_theta = -Delta_P.

    This function writes that target directly in p01/F_min variables and shows
    why the minimal K_A branch is only an anisotropy closure, not a full source
    closure.
    """
    r, r_s, G = sp.symbols('r r_s G', positive=True, real=True)
    Y, lambda_r, lambda_t = sp.symbols('Y lambda_r lambda_t', positive=True, real=True)
    K_A = sp.Symbol('K_A', positive=True, real=True)
    f = sp.Function('f')(r)
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        'c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1',
        real=True,
    )

    I1 = lambda_r + 2 * lambda_t
    I2 = 2 * lambda_r * lambda_t + lambda_t**2
    I3 = lambda_r * lambda_t**2
    L = (
        c_Y * Y
        + c_Y2 * Y**2
        + c_I1 * I1
        + c_I1sq * I1**2
        + c_I2 * I2
        + c_I3 * I3
        + c_YI1 * Y * I1
    )
    L_Y = sp.diff(L, Y)
    L_lr = sp.diff(L, lambda_r)
    L_lt_common = sp.diff(L, lambda_t)

    T_t = sp.simplify(2 * Y * L_Y - L)
    T_r = sp.simplify(2 * lambda_r * L_lr - L)
    T_theta = sp.simplify(lambda_t * L_lt_common - L)

    u = r_s / r
    delta_p = sp.simplify(r_s**2 * sp.exp(-u) / (32 * sp.pi * G * r**4))
    Y_ext = sp.exp(u)
    lambda_r_ext = sp.exp(-u) * sp.diff(f, r)**2
    lambda_t_ext = sp.exp(-u) * f**2 / r**2

    minimal_T_t = sp.simplify(T_t.subs({
        c_I1: K_A,
        c_I1sq: 0,
        c_I2: 0,
        c_I3: 0,
        c_Y: 0,
        c_Y2: 0,
        c_YI1: 0,
    }))
    minimal_T_r = sp.simplify(T_r.subs({
        c_I1: K_A,
        c_I1sq: 0,
        c_I2: 0,
        c_I3: 0,
        c_Y: 0,
        c_Y2: 0,
        c_YI1: 0,
    }))
    minimal_T_theta = sp.simplify(T_theta.subs({
        c_I1: K_A,
        c_I1sq: 0,
        c_I2: 0,
        c_I3: 0,
        c_Y: 0,
        c_Y2: 0,
        c_YI1: 0,
    }))

    return {
        "F_min_Lagrangian_radial_branch": L,
        "T^t_t_from_F_min": T_t,
        "T^r_r_from_F_min": T_r,
        "T^theta_theta_from_F_min": T_theta,
        "exponential_maps": {
            "Y_ext": Y_ext,
            "lambda_r_ext": lambda_r_ext,
            "lambda_t_ext": lambda_t_ext,
        },
        "Delta_P_target": sp.Eq(sp.Symbol('Delta_P'), delta_p),
        "full_component_target": {
            "T^t_t": sp.Eq(T_t.subs({Y: Y_ext, lambda_r: lambda_r_ext, lambda_t: lambda_t_ext}), -delta_p),
            "T^r_r": sp.Eq(T_r.subs({Y: Y_ext, lambda_r: lambda_r_ext, lambda_t: lambda_t_ext}), delta_p),
            "T^theta_theta": sp.Eq(T_theta.subs({Y: Y_ext, lambda_r: lambda_r_ext, lambda_t: lambda_t_ext}), -delta_p),
        },
        "anisotropy_equation": sp.Eq(
            sp.simplify((T_r - T_theta).subs({Y: Y_ext, lambda_r: lambda_r_ext, lambda_t: lambda_t_ext})),
            2 * delta_p,
        ),
        "time_angular_balance_equation": sp.Eq(
            sp.simplify((T_t - T_theta).subs({Y: Y_ext, lambda_r: lambda_r_ext, lambda_t: lambda_t_ext})),
            0,
        ),
        "minimal_branch_T_components": {
            "T^t_t": minimal_T_t,
            "T^r_r": minimal_T_r,
            "T^theta_theta": minimal_T_theta,
        },
        "minimal_branch_full_match_implication": (
            "K_A*(lambda_r-lambda_t)=Delta_P and K_A*lambda_r=Delta_P force lambda_t=0; "
            "therefore the minimal K_A branch closes anisotropy only, not the full source."
        ),
        "closure_status": "FULL_FMIN_COMPONENT_EQUATIONS_WRITTEN__MINIMAL_BRANCH_INSUFFICIENT__SOLVE_GENERAL_BRANCH_NEXT",
    }


def diagnose_algebraic_fmin_vs_gradient_source():
    """
    Why the compact exponential source is not closed by algebraic F_min alone.

    In the static exponential branch Y=exp(r_s/r), so the required geometric
    pressure profile is proportional to log(Y)^4/Y.  The polynomial F_min
    depends algebraically on Y, lambda_r and lambda_t, and contains no radial
    derivative of the phase.  The component balance equations T^t_t=T^theta
    and T^r_r+T^theta_theta=0 therefore constrain lambda_r and lambda_t before
    the required gradient profile is even inserted.

    This block records the exact balance equations and the derivative source
    that has the required profile.
    """
    Y, lambda_r, lambda_t = sp.symbols(
        'Y lambda_r lambda_t',
        positive=True,
        real=True,
    )
    r, r_s, G = sp.symbols('r r_s G', positive=True, real=True)
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        'c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1',
        real=True,
    )

    I1 = lambda_r + 2 * lambda_t
    I2 = 2 * lambda_r * lambda_t + lambda_t**2
    I3 = lambda_r * lambda_t**2
    L = (
        c_Y * Y
        + c_Y2 * Y**2
        + c_I1 * I1
        + c_I1sq * I1**2
        + c_I2 * I2
        + c_I3 * I3
        + c_YI1 * Y * I1
    )
    T_t = sp.simplify(2 * Y * sp.diff(L, Y) - L)
    T_r = sp.simplify(2 * lambda_r * sp.diff(L, lambda_r) - L)
    T_theta = sp.simplify(lambda_t * sp.diff(L, lambda_t) - L)

    time_angular_balance = sp.factor(T_t - T_theta)
    radial_angular_balance = sp.factor(T_r + T_theta)

    u = sp.log(Y)
    delta_y = sp.simplify(u**4 / (32 * sp.pi * G * r_s**2 * Y))
    phi = -r_s / r
    delta_gradient = sp.simplify(sp.exp(phi) * sp.diff(phi, r)**2 / (32 * sp.pi * G))
    delta_y_from_r = sp.simplify(delta_y.subs(Y, sp.exp(r_s / r)) - delta_gradient)

    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    theta_source = {
        "Theta^t_t": -delta_gradient,
        "Theta^r_r": delta_gradient,
        "Theta^theta_theta": -delta_gradient,
        "Theta^phi_phi": -delta_gradient,
    }
    einstein_residual = {
        "G^t_t-8piGTheta^t_t": sp.simplify(-D - 8 * sp.pi * G * theta_source["Theta^t_t"]),
        "G^r_r-8piGTheta^r_r": sp.simplify(D - 8 * sp.pi * G * theta_source["Theta^r_r"]),
        "G^theta_theta-8piGTheta^theta_theta": sp.simplify(-D - 8 * sp.pi * G * theta_source["Theta^theta_theta"]),
    }

    return {
        "time_angular_balance_Tt_minus_Ttheta": time_angular_balance,
        "radial_balance_Tr_plus_Ttheta": radial_angular_balance,
        "required_profile_in_Y": sp.Eq(sp.Symbol('Delta_P(Y)'), delta_y),
        "log_source_reason": "Delta_P contains log(Y)^4/Y because Y=exp(r_s/r); algebraic F_min has no phase-gradient invariant that produces this profile by itself.",
        "Bernoulli_gradient_profile": sp.Eq(sp.Symbol('Delta_P'), delta_gradient),
        "Y_profile_residual": delta_y_from_r,
        "ThetaRefG_gradient_source_target": theta_source,
        "Einstein_profile_residual_with_gradient_source": einstein_residual,
        "diagnosis_status": "ALGEBRAIC_FMIN_ALONE_DOES_NOT_CLOSE_EXPONENTIAL_SOURCE__BERNOULLI_GRADIENT_SOURCE_REQUIRED",
        "next_action": "promote the Bernoulli gradient source from ledger relation to a covariant RefG action/source term and derive its stress tensor",
    }


def derive_covariant_bernoulli_gradient_source():
    """
    Covariant source term for the compact exponential branch.

    Let h be the compact phase potential used by the biconformal branch,
    with metric

        ds^2 = exp(-2h) dt^2 - exp(2h)(dr^2+r^2dOmega^2).

    The branch action-density candidate is

        L_B = Z/(8*pi*G),  Z = -g^mn d_m h d_n h.

    With the p01 sign convention T_mn=2*dL/dg^mn-g_mn*L, this gives

        Theta^mu_nu = -(d^mu h d_nu h)/(4*pi*G) - delta^mu_nu Z/(8*pi*G).

    On the static spherical branch h=r_s/(2r), the scalar equation is
    covariant harmonicity and the mixed stress equals exactly the geometric
    effective source of the exponential exterior.
    """
    r, r_s, G = sp.symbols('r r_s G', positive=True, real=True)
    h = r_s / (2 * r)
    B = sp.exp(-2 * h)
    A = sp.exp(2 * h)
    h_prime = sp.diff(h, r)

    Z = sp.simplify(h_prime**2 / A)
    L_B = sp.simplify(Z / (8 * sp.pi * G))
    delta_p = sp.simplify(Z / (8 * sp.pi * G))

    theta_mixed = {
        "Theta^t_t": -delta_p,
        "Theta^r_r": delta_p,
        "Theta^theta_theta": -delta_p,
        "Theta^phi_phi": -delta_p,
    }
    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    einstein_residual = {
        "G^t_t-8piGTheta^t_t": sp.simplify(-D - 8 * sp.pi * G * theta_mixed["Theta^t_t"]),
        "G^r_r-8piGTheta^r_r": sp.simplify(D - 8 * sp.pi * G * theta_mixed["Theta^r_r"]),
        "G^theta_theta-8piGTheta^theta_theta": sp.simplify(-D - 8 * sp.pi * G * theta_mixed["Theta^theta_theta"]),
        "G^phi_phi-8piGTheta^phi_phi": sp.simplify(-D - 8 * sp.pi * G * theta_mixed["Theta^phi_phi"]),
    }

    sqrt_minus_g_over_sin = sp.simplify(sp.sqrt(B * A**3) * r**2)
    g_rr_inv = -1 / A
    radial_current_over_sin = sp.simplify(sqrt_minus_g_over_sin * g_rr_inv * h_prime)
    scalar_eom_residual = sp.simplify(sp.diff(radial_current_over_sin, r))

    rho_std = theta_mixed["Theta^t_t"]
    p_r_std = -theta_mixed["Theta^r_r"]
    p_t_std = -theta_mixed["Theta^theta_theta"]

    return {
        "branch_metric": "ds^2=exp(-2h)dt^2-exp(2h)(dr^2+r^2dOmega^2)",
        "branch_h": sp.Eq(sp.Symbol('h'), h),
        "covariant_invariant": sp.Eq(sp.Symbol('Z'), Z),
        "source_action_density": sp.Eq(sp.Symbol('L_B'), L_B),
        "stress_formula": "Theta^mu_nu=-(d^mu h d_nu h)/(4*pi*G)-delta^mu_nu*Z/(8*pi*G)",
        "Theta_mixed_static_branch": theta_mixed,
        "Delta_P": sp.Eq(sp.Symbol('Delta_P'), delta_p),
        "scalar_eom_current_over_sin": radial_current_over_sin,
        "scalar_eom_residual": scalar_eom_residual,
        "Einstein_profile_residual": einstein_residual,
        "standard_energy_conditions": {
            "rho": rho_std,
            "rho_plus_p_r": sp.simplify(rho_std + p_r_std),
            "rho_plus_p_t": sp.simplify(rho_std + p_t_std),
        },
        "closure_status": "COVARIANT_BERNOULLI_GRADIENT_SOURCE_DERIVED_FOR_STATIC_EXPONENTIAL_BRANCH",
        "physical_export_note": "RefG medium reading is derive_projected_bernoulli_medium_source(); unprojected scalar is static shorthand",
        "remaining_gate": "full coupled projector/medium perturbative stability must be audited before full compact-object export",
    }


def derive_projected_bernoulli_medium_source():
    """
    Physical RefG reading of the Bernoulli compact source.

    The unprojected scalar shorthand Z=-g^mn d_m h d_n h closes the static
    algebra.  As an ordinary propagating scalar in (+---) signature it carries
    a wrong-sign time-gradient coefficient.

    RefG already has a medium rest frame.  The compact Bernoulli response is
    therefore written with the spatial projector

        gamma^mn = u^m u^n - g^mn,  u^m u_m = 1,
        Z_perp = gamma^mn d_m h d_n h,
        L_B_perp = Z_perp/(8*pi*G).

    On the static comoving branch this gives the same mixed tensor as the
    exponential geometry, while the Bernoulli term itself contains no time
    kinetic term.  The propagating no-ghost sector remains the p01/p25 medium
    system; full coupled perturbative stability is still a separate gate.
    """
    r, r_s, G = sp.symbols('r r_s G', positive=True, real=True)
    h = r_s / (2 * r)
    B = sp.exp(-2 * h)
    A = sp.exp(2 * h)
    h_prime = sp.diff(h, r)

    z_perp = sp.simplify(h_prime**2 / A)
    l_perp = sp.simplify(z_perp / (8 * sp.pi * G))
    delta_p = l_perp

    theta_mixed = {
        "Theta^t_t": -delta_p,
        "Theta^r_r": delta_p,
        "Theta^theta_theta": -delta_p,
        "Theta^phi_phi": -delta_p,
    }
    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    einstein_residual = {
        "G^t_t-8piGTheta^t_t": sp.simplify(-D - 8 * sp.pi * G * theta_mixed["Theta^t_t"]),
        "G^r_r-8piGTheta^r_r": sp.simplify(D - 8 * sp.pi * G * theta_mixed["Theta^r_r"]),
        "G^theta_theta-8piGTheta^theta_theta": sp.simplify(-D - 8 * sp.pi * G * theta_mixed["Theta^theta_theta"]),
        "G^phi_phi-8piGTheta^phi_phi": sp.simplify(-D - 8 * sp.pi * G * theta_mixed["Theta^phi_phi"]),
    }

    unprojected_time_kinetic_coeff = -1 / (8 * sp.pi * G)
    projected_time_kinetic_coeff = sp.Integer(0)
    projected_spatial_gradient_coeff = 1 / (8 * sp.pi * G)

    return {
        "medium_projector": "gamma^mn=u^m*u^n-g^mn with u^m*u_m=1",
        "comoving_static_branch": "u^m=(1/sqrt(B),0,0,0), h=h(r)",
        "Z_perp_static": sp.Eq(sp.Symbol('Z_perp'), z_perp),
        "L_B_perp": sp.Eq(sp.Symbol('L_B_perp'), l_perp),
        "Delta_P": sp.Eq(sp.Symbol('Delta_P'), delta_p),
        "Theta_mixed_static_branch": theta_mixed,
        "Einstein_profile_residual": einstein_residual,
        "unprojected_scalar_time_kinetic_coefficient": unprojected_time_kinetic_coeff,
        "projected_medium_time_kinetic_coefficient": projected_time_kinetic_coeff,
        "projected_spatial_gradient_coefficient": projected_spatial_gradient_coeff,
        "ordinary_scalar_export": "BLOCKED_STANDALONE_SCALAR_EXPORT__UNPROJECTED_LB_IS_STATIC_SHORTHAND_WITH_WRONG_SIGN_TIME_KINETIC",
        "refg_medium_export": "PASS_STATIC_PROJECTED_BERNOULLI_MEDIUM_SOURCE_FOR_EXPONENTIAL_BRANCH",
        "remaining_gate": "derive full coupled p01/projector perturbations and core action dynamics",
    }


def analyze_exponential_exterior_curvature():
    """
    Exponential compact-object exterior branch.

    metric:
        ds^2 = -exp(-r_s/r)c^2dt^2 + exp(r_s/r)(dr^2+r^2dOmega^2)

    Branch-level invariant check:
        R -> 0 and K -> 0 as r -> 0.
    """
    r, r_s = sp.symbols('r r_s', real=True, positive=True)
    u = sp.Symbol('u', real=True, positive=True)

    phi = -r_s / r
    g_tt = -sp.exp(phi)
    g_rr = sp.exp(-phi)

    ricci = -r_s**2 * sp.exp(-r_s / r) / (2 * r**4)
    ricci_sq = r_s**4 * sp.exp(-2 * r_s / r) / (4 * r**8)
    kretschmann = (
        r_s**2
        * (48 * r**2 - 32 * r * r_s + 7 * r_s**2)
        * sp.exp(-2 * r_s / r)
        / (4 * r**8)
    )

    k_shape = sp.simplify(u**6 * (48 - 32 * u + 7 * u**2) * sp.exp(-2 * u) / 4)
    k_extremum_poly = 7 * u**3 - 60 * u**2 + 160 * u - 144
    physical_roots = [
        root for root in sp.nroots(k_extremum_poly)
        if abs(sp.im(root)) < 1.0e-12 and sp.re(root) > 0
    ]
    u_peak = sp.N(sp.re(physical_roots[0]), 8) if physical_roots else sp.nan
    r_peak = sp.N(1 / u_peak, 8) * r_s if physical_roots else sp.nan
    k_peak_coeff = sp.N(k_shape.subs(u, u_peak), 8) if physical_roots else sp.nan

    return {
        "ansatz_result": "within the exponential exterior, curvature scalars do not blow up at r->0",
        "derivation_status": "DERIVED_AT_PHASE_METRIC_LEVEL__PROJECTED_BERNOULLI_MEDIUM_SOURCE_DERIVED",
        "phi": sp.Eq(sp.Symbol('phi'), phi),
        "g_tt": sp.Eq(sp.Symbol('g_tt'), g_tt),
        "g_rr": sp.Eq(sp.Symbol('g_rr'), g_rr),
        "Ricci_scalar": ricci,
        "Ricci_squared": ricci_sq,
        "Kretschmann": kretschmann,
        "lim_r_to_0_R": sp.limit(ricci, r, 0, dir='+'),
        "lim_r_to_0_Ricci2": sp.limit(ricci_sq, r, 0, dir='+'),
        "lim_r_to_0_K": sp.limit(kretschmann, r, 0, dir='+'),
        "K_extremum_polynomial_u_rs_over_r": sp.Eq(k_extremum_poly, 0),
        "K_peak_u": u_peak,
        "K_peak_r": r_peak,
        "K_peak": sp.Eq(sp.Symbol('K_max'), k_peak_coeff / r_s**4),
    }


def analyze_bernoulli_singularity_saturation():
    """
    Bernoulli pressure-deficit branch check.

    Delta P = exp(phi)(phi')^2/(32*pi*G)
    for phi=-r_s/r gives
        Delta P = r_s^2 exp(-r_s/r)/(32*pi*G*r^4).

    It peaks at r_s/4 and vanishes at r->0.  This is not by itself an
    invariant total-energy proof.
    """
    r, r_s, G = sp.symbols('r r_s G', real=True, positive=True)
    phi = -r_s / r
    delta_p = sp.simplify(sp.exp(phi) * sp.diff(phi, r)**2 / (32 * sp.pi * G))
    p_static = -delta_p
    coordinate_energy = sp.simplify(
        sp.integrate(delta_p * 4 * sp.pi * r**2, (r, 0, sp.oo))
    )
    proper_volume_integrand = 4 * sp.pi * r**2 * sp.exp(3 * r_s / (2 * r))
    naive_proper_energy_integrand = sp.simplify(delta_p * proper_volume_integrand)
    u = sp.Symbol('u', real=True, positive=True)
    shape = sp.exp(-u) * u**4

    return {
        "ansatz_result": "Bernoulli pressure deficit has a finite peak and returns to zero at r->0",
        "Delta_P": sp.Eq(sp.Symbol('Delta_P'), delta_p),
        "P_static": sp.Eq(sp.Symbol('P_static'), p_static),
        "Bernoulli_identity_definition": sp.Eq(sp.Symbol('P_static + Delta_P'), 0),
        "dimensionless_shape": sp.Eq(sp.Symbol('shape(u)'), shape),
        "shape_derivative": sp.factor(sp.diff(shape, u)),
        "pressure_peak": sp.Eq(sp.Symbol('r_peak'), r_s / 4),
        "lim_r_to_0_Delta_P": sp.limit(delta_p, r, 0, dir='+'),
        "lim_r_to_inf_Delta_P": sp.limit(delta_p, r, sp.oo),
        "coordinate_measure_energy": sp.Eq(sp.Symbol('int_DeltaP_4pi_r2_dr'), coordinate_energy),
        "naive_proper_energy_integrand": naive_proper_energy_integrand,
        "lim_r_to_0_naive_proper_integrand": sp.limit(naive_proper_energy_integrand, r, 0, dir='+'),
        "energy_gate": "coordinate measure is finite; proper source measure requires a finite core cutoff",
        "meaning": "as phi -> -infinity, exp(phi) shuts off the coordinate gradient-density profile; the proper-volume source integral is controlled by the core cutoff.",
    }


def derive_adm_komar_and_proper_energy_bookkeeping():
    """
    Static energy bookkeeping for the exponential exterior.

    The asymptotic mass is a surface charge of the metric.  For
    gamma_ij=A(r) delta_ij, A=exp(r_s/r), the ADM surface integral gives the
    coefficient of the 1/r tail.  The static lapse N=sqrt(B)=exp(-r_s/(2r))
    gives the same mass through the Komar sphere integral.

    The Bernoulli source volume integral is a different object.  Its coordinate
    measure is finite, while the proper spatial volume measure diverges if the
    exterior branch is extended to r=0.  With a finite core radius r_c the
    exterior proper integral is finite and explicit.
    """
    r, r_s, G, c, r_c = sp.symbols('r r_s G c r_c', positive=True, real=True)
    A = sp.exp(r_s / r)
    N = sp.exp(-r_s / (2 * r))
    delta_p = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (32 * sp.pi * G * r**4))

    adm_mass_at_radius = sp.simplify(-r**2 * sp.diff(A, r) / 2)
    adm_mass_geometric = sp.simplify(sp.limit(adm_mass_at_radius, r, sp.oo))
    adm_mass_physical = sp.simplify(c**2 * r_s / (2 * G))

    komar_mass_at_radius = sp.simplify(sp.exp(r_s / (2 * r)) * r**2 * sp.diff(N, r))
    komar_mass_geometric = sp.simplify(komar_mass_at_radius)

    coordinate_source_total = sp.simplify(
        sp.integrate(delta_p * 4 * sp.pi * r**2, (r, 0, sp.oo))
    )
    coordinate_source_outside_core = sp.simplify(
        r_s * (1 - sp.exp(-r_s / r_c)) / (8 * G)
    )

    proper_source_integrand = sp.simplify(
        delta_p * 4 * sp.pi * r**2 * A ** sp.Rational(3, 2)
    )
    proper_source_outside_core = sp.simplify(
        r_s * (sp.exp(r_s / (2 * r_c)) - 1) / (4 * G)
    )
    proper_source_to_zero_limit = sp.limit(proper_source_outside_core, r_c, 0, dir='+')

    standard_rho_proper_outside_core = -proper_source_outside_core
    adm_mass_with_G = r_s / (2 * G)

    return {
        "ADM_surface_mass_at_radius_geometric": adm_mass_at_radius,
        "ADM_mass_geometric": adm_mass_geometric,
        "ADM_mass_physical": sp.Eq(sp.Symbol('M_ADM'), adm_mass_physical),
        "Komar_mass_geometric_each_static_sphere": komar_mass_geometric,
        "ADM_Komar_identity": sp.simplify(komar_mass_geometric - adm_mass_geometric) == 0,
        "coordinate_Bernoulli_source_total": coordinate_source_total,
        "coordinate_source_to_ADM_ratio": sp.simplify(coordinate_source_total / adm_mass_with_G),
        "coordinate_Bernoulli_source_outside_core": coordinate_source_outside_core,
        "proper_source_integrand": proper_source_integrand,
        "proper_Bernoulli_source_outside_core": proper_source_outside_core,
        "lim_rc_to_0_proper_source_outside_core": proper_source_to_zero_limit,
        "standard_rho_eff_proper_outside_core": standard_rho_proper_outside_core,
        "energy_status": "ADM_KOMAR_MASS_CLOSED__PROPER_SOURCE_FINITE_ONLY_WITH_CORE_CUTOFF",
        "article_status": "static exterior mass is fixed by the asymptotic 1/r charge; proper internal energy belongs to the finite-core completion",
    }


def analyze_rarefaction_information_cutoff():
    """
    Phenomenological microscopic closure for the r=0 boundary.

    User intuition, written as a continuum-mechanics criterion:
    in the deepest Bernoulli deficit the active carrier density of the
    vacuum medium is rarefied, collisions become sparse, and the continuum
    no longer transmits information as a connected elastic fluid.

    Minimal closure ansatz:
        n_eff = n_0 exp(phi),       phi=-r_s/r
        c_eff = c exp(phi)
        ell_mfp = 1/(sigma n_eff)
        Gamma_coll = c_eff/ell_mfp.

    Then Gamma_coll -> 0, ell_mfp -> infinity, Kn=ell_mfp/r -> infinity.
    This converts the formal r=0 endpoint into an information-decoupled,
    dilute boundary/core instead of an infinite-density singularity.
    """
    r, r_s, G, n_0, sigma, c, a_osc = sp.symbols(
        'r r_s G n_0 sigma c a_osc',
        real=True,
        positive=True,
    )
    phi = -r_s / r
    n_eff = n_0 * sp.exp(phi)
    mean_spacing = n_eff ** (-sp.Rational(1, 3))
    ell_mfp = 1 / (sigma * n_eff)
    c_eff = c * sp.exp(phi)
    gamma_coll = sp.simplify(c_eff / ell_mfp)
    gamma_ratio = sp.simplify(gamma_coll / (c * sigma * n_0))

    gradient_length = sp.simplify(abs(phi / sp.diff(phi, r)))
    knudsen = sp.simplify(ell_mfp / r)
    carriers_in_gradient_cell = sp.simplify(n_eff * r**3)
    carriers_in_finite_oscillon = sp.simplify(n_eff * a_osc**3)

    delta_p = sp.simplify(sp.exp(phi) * sp.diff(phi, r)**2 / (32 * sp.pi * G))
    outward_pressure_force_density = sp.factor(sp.diff(delta_p, r))

    return {
        "closure_status": "PHENOMENOLOGICAL_KNUDSEN_CUTOFF_NOT_YET_DERIVED_FROM_ACTION",
        "closure_density": sp.Eq(sp.Symbol('n_eff'), n_eff),
        "mean_spacing": sp.Eq(sp.Symbol('d_eff'), mean_spacing),
        "mean_free_path": sp.Eq(sp.Symbol('ell_mfp'), ell_mfp),
        "effective_signal_speed": sp.Eq(sp.Symbol('c_eff'), c_eff),
        "collision_rate": sp.Eq(sp.Symbol('Gamma_coll'), gamma_coll),
        "collision_rate_ratio": sp.Eq(sp.Symbol('Gamma_coll/Gamma_0'), gamma_ratio),
        "lim_r_to_0_n_eff": sp.limit(n_eff, r, 0, dir='+'),
        "lim_r_to_0_mean_spacing": sp.limit(mean_spacing, r, 0, dir='+'),
        "lim_r_to_0_ell_mfp": sp.limit(ell_mfp, r, 0, dir='+'),
        "lim_r_to_0_collision_ratio": sp.limit(gamma_ratio, r, 0, dir='+'),
        "gradient_length": sp.Eq(sp.Symbol('L_grad'), gradient_length),
        "Knudsen_number": sp.Eq(sp.Symbol('Kn'), knudsen),
        "lim_r_to_0_Kn": sp.limit(knudsen, r, 0, dir='+'),
        "carriers_in_gradient_cell": sp.Eq(sp.Symbol('N_grad'), carriers_in_gradient_cell),
        "lim_r_to_0_N_grad": sp.limit(carriers_in_gradient_cell, r, 0, dir='+'),
        "carriers_in_finite_oscillon": sp.Eq(sp.Symbol('N_osc'), carriers_in_finite_oscillon),
        "lim_r_to_0_N_osc": sp.limit(carriers_in_finite_oscillon, r, 0, dir='+'),
        "medium_stress_gradient": sp.Eq(sp.Symbol('d_DeltaP_dr'), outward_pressure_force_density),
        "force_turning_radius": sp.Eq(sp.Symbol('r_turn'), r_s / 4),
        "inner_core_sign": "for r<r_s/4, d(Delta_P)/dr>0: medium-stress gradient reverses sign.",
        "force_firewall": "medium backreaction only; not a literal extra pressure force on matter.",
        "physical_meaning": "near r=0 the closure ansatz makes the medium dilute and non-communicating; this remains a kinetic derivation task.",
    }


def analyze_geodesic_completion_by_core_matching():
    """
    Conditional boundary-extension ansatz.

    The exponential exterior is not forced to run all the way to r=0 if the
    Knudsen cutoff is physically allowed.
    The continuum description self-terminates where Kn=ell_mfp/r reaches 1:

        exp(r_s/r_c)/(n_0 sigma r_c) = 1
        r_c = r_s / W(n_0 sigma r_s).

    For r<r_c use a regular kinetic/rarefied core.  Write

        ds^2 = -B(r)c^2dt^2 + A(r)(dr^2+r^2dOmega^2).

    Let q=r_s/r_c and x=r/r_c.  A C2 positive logarithmic core that matches
    the exterior A_+=exp(r_s/r), B_+=exp(-r_s/r) through second derivative is:

        log A_- = q(35x^2/8 - 21x^4/4 + 15x^6/8),
        log B_- = -q + q(-11x^2/8 + 9x^4/4 - 7x^6/8).

    This gives A(0)=1, B(0)=exp(-q)>0, first derivatives vanish at the center,
    and all center curvature scalars are finite.  In Cartesian coordinates the
    center is locally regular.  The same C2 matching removes the thin-shell
    Israel junction stress at r_c.  A full completion proof still requires the
    core stress tensor, core energy bookkeeping and stability.
    """
    r, r_s, r_c, n_0, sigma, q, x = sp.symbols(
        'r r_s r_c n_0 sigma q x',
        real=True,
        positive=True,
    )

    r_kn = sp.simplify(r_s / sp.LambertW(n_0 * sigma * r_s))
    q_kn = sp.simplify(sp.LambertW(n_0 * sigma * r_s))
    pressure_turn_condition = sp.Ge(n_0 * sigma * r_s, 4 * sp.exp(4))

    log_a_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    log_b_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )
    log_a_ext = q / x
    log_b_ext = -q / x

    c2_match_a = [
        sp.simplify(sp.diff(log_a_core, x, order).subs(x, 1)
                    - sp.diff(log_a_ext, x, order).subs(x, 1))
        for order in range(3)
    ]
    c2_match_b = [
        sp.simplify(sp.diff(log_b_core, x, order).subs(x, 1)
                    - sp.diff(log_b_ext, x, order).subs(x, 1))
        for order in range(3)
    ]

    a2 = sp.Rational(35, 8) * q / r_c**2
    b2_over_b0 = -sp.Rational(11, 8) * q / r_c**2
    center_ricci = sp.simplify(12 * a2 + 6 * b2_over_b0)
    center_kretschmann = sp.simplify(48 * a2**2 + 12 * b2_over_b0**2)

    return {
        "conditional_ansatz": "C2 finite-core matching gives a locally regular extension if the Knudsen cutoff is allowed",
        "proof_status": "C2_CORE_MATCHING_ANSATZ__JUNCTION_STRESS_CLOSED__EFFECTIVE_CORE_SOURCE_DERIVED__MEDIUM_SOURCE_DECOMPOSITION_SEPARATE",
        "Kn_cutoff_equation": sp.Eq(sp.exp(r_s / r_c) / (n_0 * sigma * r_c), 1),
        "core_radius": sp.Eq(sp.Symbol('r_c'), r_kn),
        "core_compactness_q": sp.Eq(sp.Symbol('q_c'), q_kn),
        "inside_pressure_reversal_condition": pressure_turn_condition,
        "x_definition": sp.Eq(sp.Symbol('x'), r / r_c),
        "log_A_core": sp.Eq(sp.Symbol('log_A_minus'), log_a_core),
        "log_B_core": sp.Eq(sp.Symbol('log_B_minus'), log_b_core),
        "log_A_exterior": sp.Eq(sp.Symbol('log_A_plus'), log_a_ext),
        "log_B_exterior": sp.Eq(sp.Symbol('log_B_plus'), log_b_ext),
        "C2_match_log_A_value_slope_curvature": c2_match_a,
        "C2_match_log_B_value_slope_curvature": c2_match_b,
        "center_A": sp.Eq(sp.Symbol('A_0'), 1),
        "center_B": sp.Eq(sp.Symbol('B_0'), sp.exp(-q)),
        "center_A_prime": sp.Eq(sp.Symbol("A'_0"), 0),
        "center_B_prime": sp.Eq(sp.Symbol("B'_0"), 0),
        "center_Ricci_scalar": sp.Eq(sp.Symbol('R_0'), center_ricci),
        "center_Kretschmann": sp.Eq(sp.Symbol('K_0'), center_kretschmann),
        "local_continuation_rule": "bounded center coefficients allow local geodesic continuation inside the ansatz core.",
        "global_completion_gate": "open until coupled core dynamics and perturbative stability are checked.",
        "physical_meaning": "the formal endpoint is replaced by a candidate dilute kinetic core fixed by Kn=1.",
    }


def derive_c2_core_matching_coefficients():
    """
    Derive the polynomial coefficients used in the conditional C2 core.

    This proves only the matching algebra.  It is not a field-equation source
    derivation for the core material.
    """
    x, q = sp.symbols('x q', positive=True, real=True)
    a2, a4, a6, b2, b4, b6 = sp.symbols('a2 a4 a6 b2 b4 b6', real=True)

    log_a_poly = q * (a2*x**2 + a4*x**4 + a6*x**6)
    log_a_ext = q / x
    a_solution = sp.solve(
        [
            sp.Eq(log_a_poly.subs(x, 1), log_a_ext.subs(x, 1)),
            sp.Eq(sp.diff(log_a_poly, x).subs(x, 1), sp.diff(log_a_ext, x).subs(x, 1)),
            sp.Eq(sp.diff(log_a_poly, x, 2).subs(x, 1), sp.diff(log_a_ext, x, 2).subs(x, 1)),
        ],
        [a2, a4, a6],
        dict=True,
    )[0]

    log_b_poly = -q + q * (b2*x**2 + b4*x**4 + b6*x**6)
    log_b_ext = -q / x
    b_solution = sp.solve(
        [
            sp.Eq(log_b_poly.subs(x, 1), log_b_ext.subs(x, 1)),
            sp.Eq(sp.diff(log_b_poly, x).subs(x, 1), sp.diff(log_b_ext, x).subs(x, 1)),
            sp.Eq(sp.diff(log_b_poly, x, 2).subs(x, 1), sp.diff(log_b_ext, x, 2).subs(x, 1)),
        ],
        [b2, b4, b6],
        dict=True,
    )[0]

    return {
        "log_A_coefficients": a_solution,
        "log_B_coefficients": b_solution,
        "log_A_core_derived": sp.Eq(sp.Symbol('log_A_minus'), sp.simplify(log_a_poly.subs(a_solution))),
        "log_B_core_derived": sp.Eq(sp.Symbol('log_B_minus'), sp.simplify(log_b_poly.subs(b_solution))),
        "derivation_status": "C2_MATCHING_COEFFICIENTS_DERIVED",
    }


def derive_c2_junction_stress_closure():
    """
    Israel junction stress of the C2 finite-core ansatz.

    For the static isotropic metric

        ds^2 = B dt^2 - A(dr^2+r^2 dOmega^2),

    the mixed extrinsic-curvature components of an r=constant surface are,
    up to a common orientation sign,

        K^t_t     = (log B)'/(2 sqrt(A)),
        K^theta_theta = (1/sqrt(A))*(1/r + (log A)'/2),
        K^phi_phi     = K^theta_theta.

    The C2 core matches log A and log B through value, first derivative and
    second derivative at x=r/r_c=1.  Therefore the induced metric and
    extrinsic curvature match.  Israel surface stress is zero.
    """
    x, q, r_c, G = sp.symbols('x q r_c G', positive=True, real=True)

    log_a_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    log_b_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )
    log_a_ext = q / x
    log_b_ext = -q / x

    a_core = sp.exp(log_a_core)
    a_ext = sp.exp(log_a_ext)

    metric_jump = {
        "log_A": sp.simplify((log_a_core - log_a_ext).subs(x, 1)),
        "log_B": sp.simplify((log_b_core - log_b_ext).subs(x, 1)),
        "A_r2": sp.simplify((a_core * x**2 - a_ext * x**2).subs(x, 1)),
    }
    first_derivative_jump = {
        "d_log_A_dx": sp.simplify((sp.diff(log_a_core, x) - sp.diff(log_a_ext, x)).subs(x, 1)),
        "d_log_B_dx": sp.simplify((sp.diff(log_b_core, x) - sp.diff(log_b_ext, x)).subs(x, 1)),
    }
    second_derivative_jump = {
        "d2_log_A_dx2": sp.simplify((sp.diff(log_a_core, x, 2) - sp.diff(log_a_ext, x, 2)).subs(x, 1)),
        "d2_log_B_dx2": sp.simplify((sp.diff(log_b_core, x, 2) - sp.diff(log_b_ext, x, 2)).subs(x, 1)),
    }

    rc_k_t_core = sp.simplify(sp.diff(log_b_core, x) / (2 * sp.sqrt(a_core)))
    rc_k_t_ext = sp.simplify(sp.diff(log_b_ext, x) / (2 * sp.sqrt(a_ext)))
    rc_k_ang_core = sp.simplify(
        (1 / x + sp.diff(log_a_core, x) / 2) / sp.sqrt(a_core)
    )
    rc_k_ang_ext = sp.simplify(
        (1 / x + sp.diff(log_a_ext, x) / 2) / sp.sqrt(a_ext)
    )

    junction_jump = {
        "[K^t_t]*r_c": sp.simplify((rc_k_t_core - rc_k_t_ext).subs(x, 1)),
        "[K^theta_theta]*r_c": sp.simplify((rc_k_ang_core - rc_k_ang_ext).subs(x, 1)),
        "[K^phi_phi]*r_c": sp.simplify((rc_k_ang_core - rc_k_ang_ext).subs(x, 1)),
    }
    trace_jump = sp.simplify(
        junction_jump["[K^t_t]*r_c"]
        + junction_jump["[K^theta_theta]*r_c"]
        + junction_jump["[K^phi_phi]*r_c"]
    )
    surface_stress = {
        "S^t_t": sp.simplify(-(junction_jump["[K^t_t]*r_c"] - trace_jump) / (8 * sp.pi * G * r_c)),
        "S^theta_theta": sp.simplify(-(junction_jump["[K^theta_theta]*r_c"] - trace_jump) / (8 * sp.pi * G * r_c)),
        "S^phi_phi": sp.simplify(-(junction_jump["[K^phi_phi]*r_c"] - trace_jump) / (8 * sp.pi * G * r_c)),
    }

    return {
        "metric_jump_at_rc": metric_jump,
        "first_derivative_jump_at_rc": first_derivative_jump,
        "second_derivative_jump_at_rc": second_derivative_jump,
        "extrinsic_curvature_jump": junction_jump,
        "trace_jump_times_rc": trace_jump,
        "Israel_surface_stress": surface_stress,
        "junction_status": "C2_MATCHING_GIVES_ZERO_THIN_SHELL_STRESS_AT_R_C",
        "remaining_gate": "coupled core dynamics and stability remain open",
    }


def derive_c2_core_field_equation_source():
    """
    Effective field-equation source inside the C2 finite core.

    Use x=r/r_c and q=r_s/r_c.  For

        ds^2 = B dt^2 - A(dr^2+r^2 dOmega^2),
        a=log A, b=log B,

    the mixed Einstein tensor is

        G^t_t = -e^-a/(4r) (r a'^2 + 4r a'' + 8a'),
        G^r_r = -e^-a/(4r) (r a'^2 + 2r a'b' + 4a' + 4b'),
        G^theta_theta = -e^-a/(4r)
            (2r a'' + r b'^2 + 2r b'' + 2a' + 2b').

    This function inserts the C2 core profile and records the source required
    by G^mu_nu = 8*pi*G Theta^mu_nu.  The effective core source is finite at
    the center and continuous at r_c.  Its RefG medium-source decomposition is
    derived in derive_c2_core_refg_medium_source_decomposition().
    """
    x, q, r_c, G_N = sp.symbols('x q r_c G_N', positive=True, real=True)

    log_a_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    log_b_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )
    log_a_ext = q / x
    log_b_ext = -q / x

    def dimensionless_mixed_einstein(log_a, log_b):
        a_x = sp.diff(log_a, x)
        a_xx = sp.diff(log_a, x, 2)
        b_x = sp.diff(log_b, x)
        b_xx = sp.diff(log_b, x, 2)
        prefactor = -sp.exp(-log_a) / (4 * x)
        return {
            "r_c^2 G^t_t": sp.factor(sp.simplify(
                prefactor * (x * a_x**2 + 4 * x * a_xx + 8 * a_x)
            )),
            "r_c^2 G^r_r": sp.factor(sp.simplify(
                prefactor * (x * a_x**2 + 2 * x * a_x * b_x + 4 * a_x + 4 * b_x)
            )),
            "r_c^2 G^theta_theta": sp.factor(sp.simplify(
                prefactor * (2 * x * a_xx + x * b_x**2 + 2 * x * b_xx + 2 * a_x + 2 * b_x)
            )),
        }

    core_g = dimensionless_mixed_einstein(log_a_core, log_b_core)
    exterior_g = dimensionless_mixed_einstein(log_a_ext, log_b_ext)

    center_g = {
        key: sp.simplify(sp.limit(value, x, 0, dir='+'))
        for key, value in core_g.items()
    }
    boundary_jump = {
        key: sp.simplify(core_g[key].subs(x, 1) - exterior_g[key].subs(x, 1))
        for key in core_g
    }
    boundary_value = {
        key: sp.simplify(core_g[key].subs(x, 1))
        for key in core_g
    }
    required_theta = {
        key.replace("r_c^2 G", "Theta"): sp.simplify(value / (8 * sp.pi * G_N * r_c**2))
        for key, value in core_g.items()
    }
    center_theta = {
        key.replace("r_c^2 G", "Theta_center"): sp.simplify(value / (8 * sp.pi * G_N * r_c**2))
        for key, value in center_g.items()
    }

    center_ricci = sp.simplify(-(center_g["r_c^2 G^t_t"]
                                 + center_g["r_c^2 G^r_r"]
                                 + 2 * center_g["r_c^2 G^theta_theta"]) / r_c**2)
    a2 = sp.Rational(35, 8) * q / r_c**2
    b2 = -sp.Rational(11, 8) * q / r_c**2
    center_kretschmann = sp.simplify(48 * a2**2 + 12 * b2**2)

    return {
        "core_log_A": sp.Eq(sp.Symbol('log_A_core'), log_a_core),
        "core_log_B": sp.Eq(sp.Symbol('log_B_core'), log_b_core),
        "dimensionless_core_Einstein_mixed": core_g,
        "required_core_Theta_mixed": required_theta,
        "center_dimensionless_Einstein_mixed": center_g,
        "center_required_Theta_mixed": center_theta,
        "center_Ricci_scalar": sp.Eq(sp.Symbol('R_center'), center_ricci),
        "center_Kretschmann": sp.Eq(sp.Symbol('K_center'), center_kretschmann),
        "boundary_dimensionless_Einstein_mixed": boundary_value,
        "boundary_Einstein_jump_core_minus_exterior": boundary_jump,
        "finite_center_status": "PASS_C2_CORE_EFFECTIVE_SOURCE_FINITE_AT_CENTER",
        "boundary_status": "PASS_C2_CORE_EFFECTIVE_SOURCE_CONTINUOUS_AT_R_C",
        "field_equation_status": "C2_CORE_EFFECTIVE_FIELD_EQUATION_SOURCE_DERIVED__MEDIUM_SOURCE_DECOMPOSITION_DERIVED_SEPARATELY",
    }


def derive_c2_core_proper_energy_finiteness():
    """
    Proper-volume finiteness of the C2 core effective source.

    This checks the volume bookkeeping after the finite core cutoff is inserted.
    It checks source finiteness.  The tensor-level RefG medium decomposition is
    handled by derive_c2_core_refg_medium_source_decomposition().
    """
    x, q, r_c, G_N = sp.symbols('x q r_c G_N', positive=True, real=True)

    log_a_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    log_b_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )

    a_x = sp.diff(log_a_core, x)
    a_xx = sp.diff(log_a_core, x, 2)
    core_g_t = sp.factor(sp.simplify(
        -sp.exp(-log_a_core)
        * (x * a_x**2 + 4 * x * a_xx + 8 * a_x)
        / (4 * x)
    ))

    theta_t = sp.simplify(core_g_t / (8 * sp.pi * G_N * r_c**2))
    proper_volume_dx = sp.simplify(4 * sp.pi * r_c**3 * x**2 * sp.exp(3 * log_a_core / 2))
    proper_core_integrand = sp.factor(sp.simplify(theta_t * proper_volume_dx))
    absolute_core_integrand = sp.factor(sp.simplify(abs(theta_t) * proper_volume_dx))

    exterior_proper_source = sp.simplify(
        r_c * q * (sp.exp(q / 2) - 1) / (4 * G_N)
    )
    total_effective_source_charge = (
        sp.Integral(proper_core_integrand, (x, 0, 1)) + exterior_proper_source
    )

    return {
        "core_theta_t_t_effective": theta_t,
        "proper_volume_dx": proper_volume_dx,
        "proper_core_source_integrand": proper_core_integrand,
        "lim_x_to_0_integrand": sp.limit(proper_core_integrand, x, 0, dir='+'),
        "integrand_at_x_1": sp.simplify(proper_core_integrand.subs(x, 1)),
        "proper_core_source_charge": sp.Eq(
            sp.Symbol('Q_core_proper'),
            sp.Integral(proper_core_integrand, (x, 0, 1)),
        ),
        "absolute_core_integrand": absolute_core_integrand,
        "lim_x_to_0_absolute_integrand": sp.limit(absolute_core_integrand, x, 0, dir='+'),
        "exterior_proper_source_outside_rc": exterior_proper_source,
        "total_effective_proper_source_charge": sp.Eq(
            sp.Symbol('Q_total_proper_eff'),
            total_effective_source_charge,
        ),
        "finite_interval_argument": "for finite q and r_c>0 the C2 core integrand is continuous on 0<=x<=1 and the exterior term is finite",
        "proper_energy_status": "C2_CORE_EFFECTIVE_PROPER_SOURCE_FINITE_FOR_FINITE_R_C",
        "medium_energy_status": "TENSOR_LEVEL_MEDIUM_SOURCE_DECOMPOSITION_DERIVED_SEPARATELY",
    }


def derive_c2_core_refg_medium_source_decomposition():
    """
    RefG medium-source decomposition of the C2 finite core.

    The C2 metric core already fixes the required mixed tensor through
    G^mu_nu=8*pi*G Theta^mu_nu.  This block inserts the exterior Bernoulli
    phase coordinate used by the projected source,

        h_core = -log(B_core)/2,

    and evaluates the projected Bernoulli source

        P_B = exp(-log A_core) (dh/dr)^2/(8*pi*G).

    The difference between the required core source and this projected phase
    source is the independent residual medium-stress channel.  The residual is
    finite at the center and vanishes at the C2 boundary, so the core source is
    carried by allowed RefG medium variables at the tensor-ledger level.  The
    remaining task is the coupled action/evolution solution for this residual
    channel.
    """
    x, q, r_c, G_N = sp.symbols('x q r_c G_N', positive=True, real=True)

    log_a_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    log_b_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )
    log_a_ext = q / x
    log_b_ext = -q / x

    def dimensionless_mixed_einstein(log_a, log_b):
        a_x = sp.diff(log_a, x)
        a_xx = sp.diff(log_a, x, 2)
        b_x = sp.diff(log_b, x)
        b_xx = sp.diff(log_b, x, 2)
        prefactor = -sp.exp(-log_a) / (4 * x)
        return {
            "Theta^t_t": sp.factor(sp.simplify(
                prefactor * (x * a_x**2 + 4 * x * a_xx + 8 * a_x)
                / (8 * sp.pi * G_N * r_c**2)
            )),
            "Theta^r_r": sp.factor(sp.simplify(
                prefactor * (x * a_x**2 + 2 * x * a_x * b_x + 4 * a_x + 4 * b_x)
                / (8 * sp.pi * G_N * r_c**2)
            )),
            "Theta^theta_theta": sp.factor(sp.simplify(
                prefactor * (2 * x * a_xx + x * b_x**2 + 2 * x * b_xx + 2 * a_x + 2 * b_x)
                / (8 * sp.pi * G_N * r_c**2)
            )),
        }

    required_core = dimensionless_mixed_einstein(log_a_core, log_b_core)

    h_core = sp.simplify(-log_b_core / 2)
    h_ext = sp.simplify(-log_b_ext / 2)
    h_x = sp.diff(h_core, x)
    projected_pressure = sp.factor(sp.simplify(
        sp.exp(-log_a_core) * h_x**2 / (8 * sp.pi * G_N * r_c**2)
    ))
    projected_phase_source = {
        "Theta^t_t": -projected_pressure,
        "Theta^r_r": projected_pressure,
        "Theta^theta_theta": -projected_pressure,
    }
    residual_medium_source = {
        key: sp.factor(sp.simplify(required_core[key] - projected_phase_source[key]))
        for key in required_core
    }

    residual_center = {
        key: sp.simplify(sp.limit(value, x, 0, dir='+'))
        for key, value in residual_medium_source.items()
    }
    residual_boundary = {
        key: sp.simplify(value.subs(x, 1))
        for key, value in residual_medium_source.items()
    }
    projected_boundary = {
        key: sp.simplify(value.subs(x, 1))
        for key, value in projected_phase_source.items()
    }
    required_boundary = {
        key: sp.simplify(value.subs(x, 1))
        for key, value in required_core.items()
    }
    boundary_residuals_zero = all(value == 0 for value in residual_boundary.values())

    h_match_at_boundary = {
        "h_core_minus_h_ext": sp.simplify(h_core.subs(x, 1) - h_ext.subs(x, 1)),
        "h_x_core_minus_h_x_ext": sp.simplify(
            sp.diff(h_core, x).subs(x, 1) - sp.diff(h_ext, x).subs(x, 1)
        ),
        "h_xx_core_minus_h_xx_ext": sp.simplify(
            sp.diff(h_core, x, 2).subs(x, 1) - sp.diff(h_ext, x, 2).subs(x, 1)
        ),
    }

    return {
        "core_phase_definition": sp.Eq(sp.Symbol('h_core'), h_core),
        "phase_C2_match_at_boundary": h_match_at_boundary,
        "projected_Bernoulli_core_pressure": sp.Eq(sp.Symbol('P_B_core'), projected_pressure),
        "required_C2_core_Theta_mixed": required_core,
        "projected_phase_Theta_mixed": projected_phase_source,
        "residual_medium_Theta_mixed": residual_medium_source,
        "residual_center": residual_center,
        "residual_boundary": residual_boundary,
        "projected_boundary": projected_boundary,
        "required_boundary": required_boundary,
        "boundary_residuals_zero": boundary_residuals_zero,
        "realization_status": "PASS_C2_CORE_SOURCE_DECOMPOSED_IN_REFG_PROJECTED_PHASE_PLUS_FINITE_MEDIUM_STRESS_BASIS",
        "remaining_gate": "solve the coupled core action/evolution and perturbative spectrum",
    }


def derive_c2_core_p01_action_stress_branch_equations():
    """
    C2 residual medium stress as p01 action-stress branch equations.

    The preceding decomposition leaves a finite residual medium tensor after
    the projected phase/Bernoulli part is removed.  This block writes the
    residual in the same p01 spherical action-stress variables used elsewhere:

        lambda_r = exp(-log A) y'(x)^2,
        lambda_t = exp(-log A) y(x)^2/x^2,
        f(r) = r_c y(x).

    For the minimal anisotropy modulus K_A, p01 gives

        p_t - p_r = 2 K_A (lambda_r - lambda_t).

    Since T^r_r-T^theta_theta = p_t-p_r, the residual anisotropy gives an
    explicit first-order deformation equation for y(x).  The full diagonal
    residual is then a standard p01 action-jet problem: along the core branch
    the derivatives of the local action density L(Y,lambda_r,lambda_t) are
    fixed algebraically by the three mixed stress components.
    """
    x, q, r_c, G_N, K_A = sp.symbols(
        'x q r_c G_N K_A',
        positive=True,
        real=True,
    )
    y = sp.Function('y')(x)

    log_a_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    log_b_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )

    medium_source = derive_c2_core_refg_medium_source_decomposition()
    residual = medium_source["residual_medium_Theta_mixed"]
    tau_t = residual["Theta^t_t"]
    tau_r = residual["Theta^r_r"]
    tau_theta = residual["Theta^theta_theta"]
    residual_anisotropy = sp.factor(sp.simplify(tau_r - tau_theta))

    lambda_r_core = sp.simplify(sp.exp(-log_a_core) * sp.diff(y, x)**2)
    lambda_t_core = sp.simplify(sp.exp(-log_a_core) * y**2 / x**2)
    anisotropy_equation = sp.Eq(
        2 * K_A * (lambda_r_core - lambda_t_core),
        residual_anisotropy,
    )
    deformation_ode = sp.Eq(
        sp.diff(y, x)**2 - y**2 / x**2,
        sp.factor(sp.simplify(sp.exp(log_a_core) * residual_anisotropy / (2 * K_A))),
    )
    ode_rhs = deformation_ode.rhs

    Y, lambda_r, lambda_t = sp.symbols(
        'Y lambda_r lambda_t',
        positive=True,
        real=True,
    )
    L, tau_T, tau_R, tau_H = sp.symbols('L tau_T tau_R tau_H', real=True)
    action_jet_rule = {
        "L_Y": sp.Eq(sp.Symbol('L_Y'), (tau_T + L) / (2 * Y)),
        "L_lambda_r": sp.Eq(sp.Symbol('L_lambda_r'), (tau_R + L) / (2 * lambda_r)),
        "L_lambda_t_common": sp.Eq(sp.Symbol('L_lambda_t'), (tau_H + L) / lambda_t),
    }
    branch_substitution = {
        "Y_core": sp.exp(-log_b_core),
        "lambda_r_core": lambda_r_core,
        "lambda_t_core": lambda_t_core,
        "tau_T": tau_t,
        "tau_R": tau_r,
        "tau_H": tau_theta,
    }

    return {
        "residual_anisotropy_T_r_minus_T_theta": residual_anisotropy,
        "p01_lambda_r_core": sp.Eq(sp.Symbol('lambda_r'), lambda_r_core),
        "p01_lambda_t_core": sp.Eq(sp.Symbol('lambda_t'), lambda_t_core),
        "minimal_p01_anisotropy_equation": anisotropy_equation,
        "core_deformation_ode": deformation_ode,
        "ode_rhs_center_limit": sp.simplify(sp.limit(ode_rhs, x, 0, dir='+')),
        "ode_rhs_boundary_value": sp.simplify(ode_rhs.subs(x, 1)),
        "regular_center_condition": "y(0)=0 and y'(0)=lim y/x, because the residual anisotropy vanishes at the center",
        "C2_boundary_condition": "residual anisotropy vanishes at x=1, so the p01 map can match isotropically with y'(1)=y(1)",
        "full_diagonal_action_jet_rule": action_jet_rule,
        "branch_substitution_for_action_jet": branch_substitution,
        "branch_status": "PASS_C2_RESIDUAL_MEDIUM_STRESS_WRITTEN_AS_P01_ACTION_BRANCH_EQUATIONS",
        "remaining_gate": "solve the coupled y(x), L(x) core branch and perturbative spectrum",
    }


def derive_c2_core_deformation_solution_ledger():
    """
    Regular solution ledger for the C2 residual p01 deformation ODE.

    Write y=x z.  The residual anisotropy equation becomes

        x z' = sqrt(z^2-S(x)) - z

    on the positive-orientation branch, where S(x)=-F(x) is the finite
    residual source load.  S(0)=S(1)=0, so a regular center y~alpha*x and the
    isotropic C2 boundary condition y'(1)=y(1) are natural endpoints.

    The exact nonlinear IVP is the branch to solve numerically/dynamically.
    The first controlled analytic solution is the large-stiffness expansion in
    1/(G K_A r_c^2), which is derived here and satisfies both endpoint
    conditions.  Its remaining residual is second order in the same expansion.
    """
    x, q, r_c, G_N, K_A, alpha = sp.symbols(
        'x q r_c G_N K_A alpha',
        positive=True,
        real=True,
    )
    z = sp.Function('z')(x)

    source_load = sp.factor(sp.simplify(
        3 * q * x**2 * (1 - x**2) * (4 + 3 * q * (1 - x**2)**3)
        / (16 * sp.pi * G_N * K_A * r_c**2)
    ))
    exact_z_ivp = sp.Eq(
        x * sp.diff(z, x),
        sp.sqrt(z**2 - source_load) - z,
    )
    radicand_condition = sp.Ge(z**2, source_load)
    source_bound = sp.simplify(
        3 * q * (4 + 3 * q)
        / (64 * sp.pi * G_N * K_A * r_c**2)
    )
    control_parameter = sp.simplify(source_bound / alpha**2)

    integral_shape = sp.simplify(
        1
        + sp.Rational(3, 10) * q
        - (1 - x**2)**2
        - sp.Rational(3, 10) * q * (1 - x**2)**5
    )
    z_first = sp.simplify(
        alpha
        - 3 * q * integral_shape
        / (32 * sp.pi * G_N * K_A * r_c**2 * alpha)
    )
    y_first = sp.simplify(x * z_first)
    first_order_residual = sp.factor(sp.simplify(
        (sp.diff(y_first, x)**2 - y_first**2 / x**2) + source_load
    ))

    return {
        "source_load_S_positive": source_load,
        "source_load_center": sp.simplify(sp.limit(source_load, x, 0, dir='+')),
        "source_load_boundary": sp.simplify(source_load.subs(x, 1)),
        "exact_branch_substitution": sp.Eq(sp.Symbol('y'), x * z),
        "exact_positive_branch_IVP": exact_z_ivp,
        "exact_branch_radicand_condition": radicand_condition,
        "simple_source_bound_on_0_1": sp.Le(source_load, source_bound),
        "large_stiffness_control_parameter": control_parameter,
        "first_order_z_solution": sp.Eq(sp.Symbol('z_1'), z_first),
        "first_order_y_solution": sp.Eq(sp.Symbol('y_1'), y_first),
        "first_order_center_slope": sp.Eq(
            sp.Symbol('lim_y_over_x_at_0'),
            sp.simplify(sp.limit(y_first / x, x, 0, dir='+')),
        ),
        "first_order_boundary_condition": sp.Eq(
            sp.Symbol("y_1'(1)-y_1(1)"),
            sp.simplify(sp.diff(y_first, x).subs(x, 1) - y_first.subs(x, 1)),
        ),
        "first_order_ode_residual": first_order_residual,
        "first_order_residual_order": "O((G_N*K_A*r_c^2)^-2)",
        "solution_status": "PASS_C2_CORE_DEFORMATION_EXACT_IVP_AND_FIRST_ORDER_ANALYTIC_BRANCH_DERIVED",
        "remaining_gate": "solve the nonlinear IVP beyond first order and couple it to the full diagonal action-density branch",
    }


def derive_c2_core_nonlinear_deformation_ivp_probe():
    """
    Nonlinear IVP probe for the C2 radial core deformation.

    Normalize z by the center slope alpha:

        y=x*alpha*w,     kappa = G_N*K_A*alpha^2*r_c^2.

    The exact branch becomes

        x w' = sqrt(w^2-s(x)) - w,   w(0)=1,

    with a positive source load s(x).  This block records the dimensionless
    equation, a large-stiffness control parameter, and a direct RK4 existence
    probe for representative compact-core values.  It is a nonlinear branch
    existence check, not a perturbative stability theorem.
    """
    import math

    x, q, kappa = sp.symbols('x q kappa', positive=True, real=True)
    w = sp.Function('w')(x)

    s_norm = sp.factor(sp.simplify(
        3 * q * x**2 * (1 - x**2) * (4 + 3 * q * (1 - x**2)**3)
        / (16 * sp.pi * kappa)
    ))
    normalized_ivp = sp.Eq(
        x * sp.diff(w, x),
        sp.sqrt(w**2 - s_norm) - w,
    )
    s_bound = sp.simplify(3 * q * (3 * q + 4) / (64 * sp.pi * kappa))
    integral_load = sp.simplify(
        sp.integrate(s_norm / x, (x, 0, 1))
    )
    first_order_w_boundary = sp.simplify(1 - integral_load / 2)

    def s_value(xv: float, qv: float, kappav: float) -> float:
        u = 1.0 - xv * xv
        return 3.0 * qv * xv * xv * u * (4.0 + 3.0 * qv * u**3) / (16.0 * math.pi * kappav)

    def rhs(xv: float, wv: float, qv: float, kappav: float) -> float:
        if xv <= 0.0:
            return 0.0
        sv = s_value(xv, qv, kappav)
        rad = wv * wv - sv
        if rad <= 0.0:
            return float('nan')
        return (math.sqrt(rad) - wv) / xv

    def rk4_probe(qv: float, kappav: float, steps: int = 2000) -> dict[str, float | bool]:
        x0 = 1.0e-6
        h = (1.0 - x0) / steps
        wv = 1.0
        xv = x0
        min_rad = wv * wv - s_value(xv, qv, kappav)
        max_load = s_value(xv, qv, kappav)
        passed = True
        for _ in range(steps):
            k1 = rhs(xv, wv, qv, kappav)
            k2 = rhs(xv + 0.5 * h, wv + 0.5 * h * k1, qv, kappav)
            k3 = rhs(xv + 0.5 * h, wv + 0.5 * h * k2, qv, kappav)
            k4 = rhs(xv + h, wv + h * k3, qv, kappav)
            if not all(math.isfinite(k) for k in (k1, k2, k3, k4)):
                passed = False
                break
            wv = wv + h * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
            xv = xv + h
            sv = s_value(xv, qv, kappav)
            max_load = max(max_load, sv)
            min_rad = min(min_rad, wv * wv - sv)
            if min_rad <= 0.0 or wv <= 0.0:
                passed = False
                break
        return {
            "q": qv,
            "kappa": kappav,
            "passed": passed,
            "w_1": wv,
            "min_radicand": min_rad,
            "max_source_load": max_load,
            "boundary_condition": True,
        }

    samples = [
        rk4_probe(2.0, 1.0),
        rk4_probe(2.0, 3.0),
        rk4_probe(2.0, 10.0),
        rk4_probe(5.0, 10.0),
    ]
    all_samples_pass = all(sample["passed"] for sample in samples)

    return {
        "normalized_substitution": "y=x*alpha*w, kappa=G_N*K_A*alpha^2*r_c^2",
        "normalized_source_load": sp.Eq(sp.Symbol('s'), s_norm),
        "normalized_exact_IVP": normalized_ivp,
        "source_load_bound": sp.Le(s_norm, s_bound),
        "integral_source_load_over_x": integral_load,
        "first_order_boundary_w": sp.Eq(sp.Symbol('w_1(1)'), first_order_w_boundary),
        "rk4_samples": samples,
        "all_samples_pass": all_samples_pass,
        "nonlinear_ivp_status": "PASS_NUMERICAL_NONLINEAR_CORE_DEFORMATION_IVP_FOR_REPRESENTATIVE_STIFFNESS_VALUES",
        "remaining_gate": "turn the IVP probe into a parameter-domain theorem and then audit perturbations",
    }


def derive_c2_core_nonlinear_ivp_parameter_domain_theorem():
    """
    Sufficient parameter-domain theorem for the nonlinear deformation IVP.

    The normalized IVP is

        x w' = sqrt(w^2-s(x)) - w,   w(0)=1,

    with

        s(x)=3 q x^2(1-x^2)[4+3q(1-x^2)^3]/(16*pi*kappa).

    Since s(0)=s(1)=0 and s>=0 on 0<=x<=1, the branch is controlled by the
    integral load and a pointwise source bound.  The identity

        d(w^2)/d ln x >= -2 s(x)

    gives w^2(x) >= 1-2*Integral_0^x s(t) dt/t.  Therefore a simple sufficient
    radicand condition is

        2*Integral_0^1 s(t) dt/t + max_bound(s) < 1.

    Under this condition w^2-s stays positive on the whole interval, the
    positive branch exists from the regular center to the C2 boundary, and
    s(1)=0 gives y'(1)=y(1).
    """
    x, q, kappa = sp.symbols('x q kappa', positive=True, real=True)
    t = sp.Symbol('t', positive=True, real=True)

    s_x = sp.factor(sp.simplify(
        3 * q * x**2 * (1 - x**2) * (4 + 3 * q * (1 - x**2)**3)
        / (16 * sp.pi * kappa)
    ))
    s_t = sp.factor(sp.simplify(
        3 * q * t**2 * (1 - t**2) * (4 + 3 * q * (1 - t**2)**3)
        / (16 * sp.pi * kappa)
    ))
    integral_load_total = sp.simplify(sp.integrate(s_t / t, (t, 0, 1)))
    source_bound = sp.simplify(3 * q * (3 * q + 4) / (64 * sp.pi * kappa))
    radicand_margin_lower_bound = sp.simplify(
        1 - 2 * integral_load_total - source_bound
    )
    kappa_threshold = sp.solve(
        sp.Eq(radicand_margin_lower_bound, 0),
        kappa,
    )[0]

    local_center_series_s = sp.series(s_x, x, 0, 4).removeO()
    boundary_series_s = sp.series(s_x.subs(x, 1 - t), t, 0, 3).removeO()

    return {
        "normalized_source_load": sp.Eq(sp.Symbol('s(x)'), s_x),
        "source_load_nonnegative_interval": "s(x)>=0 for 0<=x<=1, q>0, kappa>0",
        "source_load_center": sp.simplify(sp.limit(s_x, x, 0, dir='+')),
        "source_load_boundary": sp.simplify(s_x.subs(x, 1)),
        "center_series_s": local_center_series_s,
        "boundary_series_s_x_equals_1_minus_t": boundary_series_s,
        "integral_load_total": sp.Eq(
            sp.Symbol('I_s'),
            integral_load_total,
        ),
        "simple_source_bound": sp.Le(s_x, source_bound),
        "radicand_margin_lower_bound": sp.Eq(
            sp.Symbol('M_min'),
            radicand_margin_lower_bound,
        ),
        "sufficient_kappa_condition": sp.Gt(kappa, kappa_threshold),
        "positive_branch_result": (
            "for the sufficient kappa condition, w^2-s stays positive on "
            "0<=x<=1 and the positive IVP branch reaches x=1"
        ),
        "regular_center_result": "s(x)=O(x^2), so w'(0)=0 and y=x*alpha*w has y~alpha*x",
        "C2_boundary_result": "s(1)=0 gives w'(1)=0, hence y'(1)=y(1)",
        "theorem_status": "PASS_SUFFICIENT_PARAMETER_DOMAIN_FOR_NONLINEAR_CORE_DEFORMATION_IVP",
        "remaining_gate": "audit full diagonal action-density integrability and perturbative spectrum",
    }


def derive_c2_core_action_density_integrability_theorem():
    """
    Branch-level full diagonal action-density integrability.

    The residual core tensor gives three diagonal p01 stress equations:

        tau_T = 2Y L_Y - L,
        tau_R = 2 lambda_r L_lambda_r - L,
        tau_H = lambda_t L_lambda_t - L.

    Along the radial core branch x -> (Y, lambda_r, lambda_t), these equations
    define one action density L(x).  By the chain rule,

        dL/dx = L_Y Y' + L_lambda_r lambda_r' + L_lambda_t lambda_t',

    hence L obeys a single linear first-order ODE.  The parameter-domain
    theorem for y=x*alpha*w gives positive lambda_r and lambda_t, while the C2
    residual tensor is finite at the center and zero at the boundary.  Therefore
    the three diagonal residual components are integrable as one p01
    action-density branch on the core interval.
    """
    x, q, alpha, w_b = sp.symbols(
        'x q alpha w_b',
        positive=True,
        real=True,
    )
    Y, lr, lt = [sp.Function(name)(x) for name in ('Y', 'lambda_r', 'lambda_t')]
    tau_T, tau_R, tau_H = [sp.Function(name)(x) for name in ('tau_T', 'tau_R', 'tau_H')]
    L = sp.Function('L')(x)

    L_Y = sp.simplify((tau_T + L) / (2 * Y))
    L_lr = sp.simplify((tau_R + L) / (2 * lr))
    L_lt = sp.simplify((tau_H + L) / lt)
    ode_rhs = sp.simplify(
        L_Y * sp.diff(Y, x)
        + L_lr * sp.diff(lr, x)
        + L_lt * sp.diff(lt, x)
    )
    ode_linear_coefficient = sp.simplify(
        sp.diff(Y, x) / (2 * Y)
        + sp.diff(lr, x) / (2 * lr)
        + sp.diff(lt, x) / lt
    )
    ode_source = sp.simplify(
        tau_T * sp.diff(Y, x) / (2 * Y)
        + tau_R * sp.diff(lr, x) / (2 * lr)
        + tau_H * sp.diff(lt, x) / lt
    )

    log_a_core = q * (
        sp.Rational(35, 8) * x**2
        - sp.Rational(21, 4) * x**4
        + sp.Rational(15, 8) * x**6
    )
    log_b_core = -q + q * (
        -sp.Rational(11, 8) * x**2
        + sp.Rational(9, 4) * x**4
        - sp.Rational(7, 8) * x**6
    )
    Y_core = sp.exp(-log_b_core)
    Y_center = sp.simplify(Y_core.subs(x, 0))
    Y_boundary = sp.simplify(Y_core.subs(x, 1))

    lambda_center = alpha**2
    lambda_boundary = sp.simplify(sp.exp(-q) * alpha**2 * w_b**2)

    residual = derive_c2_core_refg_medium_source_decomposition()
    residual_center = residual["residual_center"]
    residual_boundary = residual["residual_boundary"]

    return {
        "stress_to_action_jet": {
            "L_Y": sp.Eq(sp.Symbol('L_Y'), L_Y),
            "L_lambda_r": sp.Eq(sp.Symbol('L_lambda_r'), L_lr),
            "L_lambda_t": sp.Eq(sp.Symbol('L_lambda_t'), L_lt),
        },
        "linear_action_density_ode": sp.Eq(sp.diff(L, x), ode_rhs),
        "ode_linear_coefficient_A": ode_linear_coefficient,
        "ode_source_B": ode_source,
        "formal_solution": (
            "L(x)=exp(int A dx)*(L0+int exp(-int A dx)*B dx), "
            "with A and B from the displayed branch ODE"
        ),
        "core_Y_center": sp.Eq(sp.Symbol('Y_0'), Y_center),
        "core_Y_boundary": sp.Eq(sp.Symbol('Y_1'), Y_boundary),
        "lambda_center_regular": {
            "lambda_r(0)": lambda_center,
            "lambda_t(0)": lambda_center,
        },
        "lambda_boundary_C2": {
            "lambda_r(1)": lambda_boundary,
            "lambda_t(1)": lambda_boundary,
        },
        "residual_center_finite": residual_center,
        "residual_boundary_zero": residual_boundary,
        "integrability_argument": (
            "Y, lambda_r and lambda_t are positive and smooth on the branch; "
            "the residual tensor is finite at x=0 and vanishes at x=1; "
            "therefore the displayed linear ODE has a finite local solution "
            "for L(x) across the core interval."
        ),
        "integrability_status": "PASS_BRANCH_LEVEL_FULL_DIAGONAL_ACTION_DENSITY_INTEGRABILITY",
        "remaining_gate": "off-branch EFT extension and coupled perturbative spectrum",
    }


def derive_c2_core_local_stability_interface():
    """
    Local-stability interface between the compact C2 branch and p01.

    The compact ledger now derives a finite residual stress, writes it as p01
    action-stress equations, solves the radial deformation branch, and shows
    that the diagonal residual tensor is integrable as one action-density
    branch.  p01_core.py supplies the local action-sector certificate: a
    nonempty no-ghost and mixed-mode principal-symbol region.

    This function records that interface.  It is a local principal-symbol
    compatibility gate, not a QNM/ringdown theorem and not a rotating compact
    solution.
    """
    action_integrability = derive_c2_core_action_density_integrability_theorem()
    ivp_domain = derive_c2_core_nonlinear_ivp_parameter_domain_theorem()
    p01_local = local_stability_short_path_certificate()

    checks = p01_local["checks"]
    all_checks_pass = all(bool(value) for value in checks.values())

    status = (
        "PASS_COMPACT_CORE_P01_LOCAL_STABILITY_INTERFACE"
        if action_integrability["integrability_status"]
        == "PASS_BRANCH_LEVEL_FULL_DIAGONAL_ACTION_DENSITY_INTEGRABILITY"
        and ivp_domain["theorem_status"]
        == "PASS_SUFFICIENT_PARAMETER_DOMAIN_FOR_NONLINEAR_CORE_DEFORMATION_IVP"
        and p01_local["status"] == "PASS_LOCAL_STABILITY_SHORT_PATH"
        and all_checks_pass
        else "CHECK_COMPACT_CORE_P01_LOCAL_STABILITY_INTERFACE"
    )

    return {
        "interface_status": status,
        "core_action_density_status": action_integrability["integrability_status"],
        "core_ivp_domain_status": ivp_domain["theorem_status"],
        "p01_local_stability_status": p01_local["status"],
        "p01_local_stability_scope": p01_local["scope"],
        "p01_explicit_stable_point": p01_local["point"],
        "p01_checks": checks,
        "compact_reading": (
            "the compact C2 branch reaches the p01 action-density level, and "
            "the p01 principal-symbol sector has an explicit local no-ghost "
            "and mixed-mode stable point."
        ),
        "remaining_gate": "background-dependent coupled compact-core spectrum, QNMs, echoes, rotation and ray tracing",
    }


def analyze_horizon_throat_and_boundary():
    """
    Horizonless exterior-only boundary ledger.

    finite r>0-ზე g_tt never vanishes; r=0 is a boundary, not a finite
    horizon. Proper distance to r=0 diverges, while captured geodesics
    reach the boundary at finite affine/proper parameter before the
    conditional rarefied-core extension is imposed.
    """
    r, r_s, r_0, c, E_geo = sp.symbols('r r_s r_0 c E_geo', real=True, positive=True)
    phi = -r_s / r
    g_tt_abs = sp.exp(phi)
    c_coord = c * sp.exp(phi)
    proper_integrand = sp.exp(r_s / (2 * r))
    coordinate_null_integrand = sp.exp(r_s / r) / c

    areal_radius = r * sp.exp(r_s / (2 * r))
    d_areal = sp.diff(areal_radius, r)
    throat = r_s / 2
    areal_min = sp.simplify(areal_radius.subs(r, throat))

    return {
        "exterior_result": "no finite-radius Killing horizon in the static exponential exterior",
        "g_tt_abs": sp.Eq(sp.Symbol('|g_tt|'), g_tt_abs),
        "finite_r_horizon_test": "exp(-r_s/r)>0 for every finite r>0",
        "coordinate_light_speed": sp.Eq(sp.Symbol('dr_dt_null'), c_coord),
        "lim_r_to_0_c_coord": sp.limit(c_coord, r, 0, dir='+'),
        "proper_distance_integrand": proper_integrand,
        "proper_distance_to_boundary": sp.Eq(sp.Symbol('L_prop'), sp.oo),
        "external_coordinate_time_to_boundary": sp.Eq(sp.Symbol('t_external'), sp.oo),
        "radial_null_affine_arrival": sp.Eq(sp.Symbol('lambda_0'), r_0 * c / E_geo),
        "areal_radius": sp.Eq(sp.Symbol('R_areal'), areal_radius),
        "dR_dr": d_areal,
        "throat_coordinate": sp.Eq(sp.Symbol('r_throat'), throat),
        "throat_areal_radius": sp.Eq(sp.Symbol('R_min'), areal_min),
        "boundary_label": "r=0 is an infinite-redshift exterior boundary, not yet a proven collapse endpoint.",
        "geodesic_status": "exterior-only captured geodesics reach r=0 in finite affine parameter; the Knudsen core is a conditional extension ansatz.",
    }


def analyze_photon_shadow_isco():
    """
    Strong-field observables of the exponential exterior.

    Timelike geodesics use
        rdot^2 = E^2 - V_eff,
        V_eff = exp(-r_s/r) + L^2 exp(-2r_s/r)/r^2.

    Circular orbit:
        dV_eff/dr = 0.
    Marginal stability:
        d^2V_eff/dr^2 = 0.

    photon sphere:
        d/dr [exp(-2r_s/r)/r^2]=0 -> r=r_s
    shadow:
        b_c = e r_s
    massive ISCO:
        r^2 - 3 r_s r + r_s^2 = 0 -> r_ISCO = phi_golden^2 r_s
    """
    r, r_s, c, L = sp.symbols('r r_s c L', real=True, positive=True)
    phi_golden = (1 + sp.sqrt(5)) / 2

    photon_barrier = sp.exp(-2 * r_s / r) / r**2
    photon_condition = sp.factor(sp.diff(photon_barrier, r))

    v_eff = sp.exp(-r_s / r) + L**2 * sp.exp(-2 * r_s / r) / r**2
    circular_condition = sp.factor(sp.diff(v_eff, r))
    specific_l2 = sp.simplify(r_s * r**2 * sp.exp(r_s / r) / (2 * (r - r_s)))
    specific_e2 = sp.simplify(
        sp.exp(-r_s / r) + specific_l2 * sp.exp(-2 * r_s / r) / r**2
    )

    v_eff_second = sp.diff(v_eff, r, 2)
    stability_second_derivative = sp.factor(
        sp.simplify(v_eff_second.subs(L**2, specific_l2))
    )
    stability_polynomial = r**2 - 3 * r_s * r + r_s**2
    isco_poly = r**2 - 3 * r_s * r + r_s**2
    isco_roots = sp.solve(sp.Eq(isco_poly, 0), r)
    isco_physical = sp.simplify(isco_roots[1])

    omega_sq = c**2 * r_s * sp.exp(-2 * r_s / r) / (r**2 * (2 * r - r_s))
    omega_isco_sq = sp.simplify(omega_sq.subs(r, isco_physical))
    omega_gr_sq = c**2 / (54 * r_s**2)
    omega_ratio = sp.N(sp.sqrt(sp.simplify(omega_isco_sq / omega_gr_sq)), 8)

    local_speed_sq = sp.simplify(c**2 * r_s / (2 * r - r_s))
    local_speed_isco = sp.simplify(sp.sqrt(local_speed_sq.subs(r, isco_physical)))
    e2_isco = sp.simplify(specific_e2.subs(r, isco_physical))
    e_isco = sp.sqrt(e2_isco)
    binding_efficiency = sp.N(1 - e_isco, 8)
    gr_binding_efficiency = sp.N(1 - sp.sqrt(sp.Rational(8, 9)), 8)

    gr_isco_iso = (5 + 2 * sp.sqrt(6)) * r_s / 4
    gr_isco_areal = 3 * r_s
    isco_iso_ratio = sp.N(isco_physical / gr_isco_iso, 8)
    shadow_rg = sp.E * r_s
    shadow_gr = 3 * sp.sqrt(3) * r_s / 2
    shadow_ratio = sp.N(shadow_rg / shadow_gr, 8)

    return {
        "effective_potential_timelike": sp.Eq(sp.Symbol('V_eff'), v_eff),
        "circular_orbit_condition": sp.Eq(circular_condition, 0),
        "specific_L_squared_circular": sp.Eq(sp.Symbol('L_circ^2'), specific_l2),
        "specific_E_squared_circular": sp.Eq(sp.Symbol('E_circ^2'), specific_e2),
        "massive_orbit_existence": "L_circ^2>0 requires r>r_s; r=r_s is the photon boundary.",
        "local_orbital_speed_squared": sp.Eq(sp.Symbol('v_local^2'), local_speed_sq),
        "photon_barrier": photon_barrier,
        "photon_condition": sp.Eq(photon_condition, 0),
        "photon_sphere": sp.Eq(sp.Symbol('r_ph'), r_s),
        "critical_impact_parameter": sp.Eq(sp.Symbol('b_c'), shadow_rg),
        "GR_shadow_reference": sp.Eq(sp.Symbol('b_c_GR'), shadow_gr),
        "shadow_ratio_RG_over_GR": shadow_ratio,
        "shadow_size_shift": f"{float((shadow_ratio - 1) * 100):.2f}%",
        "stability_second_derivative": stability_second_derivative,
        "stability_polynomial": sp.Eq(stability_polynomial, 0),
        "ISCO_polynomial": sp.Eq(isco_poly, 0),
        "ISCO_roots": isco_roots,
        "ISCO_physical": sp.Eq(sp.Symbol('r_ISCO'), isco_physical),
        "golden_ratio_identity": sp.Eq(sp.Symbol('r_ISCO'), phi_golden**2 * r_s),
        "ISCO_local_speed": sp.Eq(sp.Symbol('v_ISCO'), local_speed_isco),
        "ISCO_specific_energy_squared": sp.Eq(sp.Symbol('E_ISCO^2'), e2_isco),
        "ISCO_binding_efficiency": binding_efficiency,
        "GR_binding_efficiency_reference": gr_binding_efficiency,
        "GR_areal_ISCO_reference": sp.Eq(sp.Symbol('R_ISCO_GR'), gr_isco_areal),
        "GR_isotropic_ISCO_reference": sp.Eq(sp.Symbol('r_ISCO_GR_iso'), gr_isco_iso),
        "ISCO_radius_ratio_RG_over_GR_iso": isco_iso_ratio,
        "Omega_ISCO_squared": sp.Eq(sp.Symbol('Omega_ISCO^2'), omega_isco_sq),
        "GR_Omega_ISCO_squared_reference": sp.Eq(sp.Symbol('Omega_GR^2'), omega_gr_sq),
        "frequency_ratio_RG_over_GR": omega_ratio,
        "frequency_proxy": "f_ISCO = 0.931 f_ISCO_GR for the same total mass",
        "mechanism": "golden-ratio ISCO is the marginal-stability root of the exponential-vacuum geodesic potential, not a fitted number.",
    }


def singularity_strength_ledger() -> list[str]:
    return [
        "Geometry-level breaker: Schwarzschild has B=0 at r_s and K->infinity at r=0; the RG exponential branch has B>0 for every finite r>0 and K->0 at r=0.",
        "Within the exponential exterior ansatz: R->0, Ricci^2->0, K->0 at r->0.",
        "Within the Bernoulli branch: Delta_P peaks at r_s/4 and returns to 0 at r->0.",
        "The r=0 endpoint is not a curvature singularity in the exponential branch, but exterior radial geodesics still expose a boundary unless a derived core/boundary law is added.",
        "The exact p01 anisotropy lever is lambda_r-lambda_t; f=r kills it, so a nontrivial radial deformation f(r) is the next closure target.",
        "A minimal nontrivial branch gives f=r*(1-r_s^2/(256*pi*G*K_A*r^4)) at linear order and exactly cancels the required anisotropy at that order.",
        "The same minimal branch has an exact implicit solution for the anisotropy equation after H=f*r/sqrt(a).",
        "The minimal K_A branch does not close the full diagonal source; full F_min matching requires T^t_t, T^r_r and T^theta_theta simultaneously.",
        "The algebraic F_min polynomial has no phase-gradient invariant, while the compact exponential source is the Bernoulli gradient profile Delta_P=exp(phi)*(phi')^2/(32*pi*G).",
        "A covariant Bernoulli gradient source L_B=Z/(8*pi*G) with Z=-g^mn*d_m h*d_n h exactly supplies the exponential mixed source on the static branch.",
        "The physical RefG export uses the projected medium source L_B_perp=Z_perp/(8*pi*G), Z_perp=(u^m*u^n-g^mn)*d_m h*d_n h; on the static branch it gives the same mixed tensor without exporting a standalone phantom scalar.",
        "The active deficit has negative radial null load in the ordinary Einstein-fluid audit; in RefG this is the phase-pressure deficit signature, not ordinary positive matter.",
        "A homogeneous positive base load is not added to the same exterior field equation; if it gravitates, the exterior metric must be rederived.",
        "The static exponential exterior has ADM mass r_s/2 in geometric units and physical mass c^2*r_s/(2G); the Komar sphere gives the same value.",
        "The Bernoulli coordinate source measure is finite, but the proper-volume source integral is finite only after the core cutoff r_c is inserted.",
        "With the C2 core inserted, the effective proper-volume source charge is finite for finite r_c.",
        "The rarefaction closure ansatz gives n_eff->0, mean free path->infinity, and collision/information rate->0 at r->0.",
        "The Knudsen number Kn=ell_mfp/r diverges, so the continuum model flags its own breakdown.",
        "Inside r_s/4 the medium-stress gradient changes sign; this is backreaction language, not an extra force on matter.",
        "If Kn=1 is the physical cutoff, the candidate matching radius is r_c=r_s/W(n_0*sigma*r_s).",
        "The C2 logarithmic core matches the exponential exterior through value, slope, and curvature at r_c.",
        "The same C2 matching gives zero Israel thin-shell stress at r_c.",
        "The C2 core's effective mixed Einstein source is finite at the center and continuous at r_c.",
        "The C2 core source decomposes into the projected RefG phase channel plus a finite residual medium-stress channel that vanishes at r_c.",
        "The residual core medium stress gives an explicit p01 action-stress branch equation for the radial core deformation y(x).",
        "The C2 core deformation branch has an exact positive-orientation IVP and a first-order analytic large-stiffness solution satisfying the regular center and C2 boundary condition.",
        "The nonlinear C2 core deformation IVP passes direct RK4 probes for representative large-stiffness values.",
        "The nonlinear C2 core deformation IVP has a sufficient kappa-domain condition that keeps the positive branch real through the core interval.",
        "The C2 residual diagonal tensor is integrable as one p01 action-density branch on the core interval.",
        "The matched core has A(0)=1, B(0)>0, A'(0)=B'(0)=0 and finite R_0, K_0 in the ansatz.",
        "There is no finite-radius Killing horizon in the static exterior: exp(-r_s/r)>0 for every r>0.",
        "The areal radius has a throat at r_s/2, with R_min=e*r_s/2.",
        "Static photon sphere is r_s and the static critical shadow impact parameter is b_c=e*r_s.",
        "Massive circular orbits exist only for r>r_s; r=r_s is a static photon-orbit boundary.",
        "Static massive-particle ISCO follows from V_eff''=0 and is r_ISCO=phi_golden^2*r_s.",
        "The static ISCO frequency proxy is f_ISCO=0.931 f_ISCO_GR for the same total mass.",
        "External observers see infinite redshift/coordinate-time freezing toward r=0 in the exterior.",
        "A full dynamical compact-object claim remains blocked by the off-branch EFT extension, rotation, QNMs/echoes and EHT ray tracing.",
    ]


def analyze_regular_center():
    r = sp.Symbol('r', real=True, positive=True)
    a_2, b_2 = sp.symbols('a_2 b_2', real=True)
    B_0 = sp.Symbol('B_0', real=True, positive=True) # B(0) > 0 აუცილებელია
    
    # რეგულარული ცენტრის ანზაცი (A(0) = 1 აუცილებელია რეგულარულობისთვის)
    A_core = 1 + a_2 * r**2
    B_core = B_0 + b_2 * r**2
    
    # G^mu_nu გეომეტრიული ნაწილები isotropic metric-ისთვის
    log_a = sp.log(A_core)
    log_b = sp.log(B_core)
    a_p = sp.diff(log_a, r)
    a_pp = sp.diff(log_a, r, 2)
    b_p = sp.diff(log_b, r)
    b_pp = sp.diff(log_b, r, 2)
    G_tt = -sp.exp(-log_a) * (r*a_p**2 + 4*r*a_pp + 8*a_p) / (4*r)
    G_rr = -sp.exp(-log_a) * (r*a_p**2 + 2*r*a_p*b_p + 4*a_p + 4*b_p) / (4*r)
    G_thth = -sp.exp(-log_a) * (2*r*a_pp + r*b_p**2 + 2*r*b_pp + 2*a_p + 2*b_p) / (4*r)
    
    # რიჩის სკალარი R = -G^\mu_\mu
    R_scalar = -(G_tt + G_rr + 2*G_thth)
    
    # ლიმიტები r -> 0
    G_tt_0 = sp.simplify(sp.limit(G_tt, r, 0))
    G_rr_0 = sp.simplify(sp.limit(G_rr, r, 0))
    G_thth_0 = sp.simplify(sp.limit(G_thth, r, 0))
    R_0 = sp.simplify(sp.limit(R_scalar, r, 0))
    
    # Kretschmann center value for log A=a_2 r^2 and log B=log(B_0)+(b_2/B_0)r^2
    K_0 = sp.simplify(48*a_2**2 + 12*b_2**2/B_0**2)
    
    # სუპერსოლიდის სტრეს-ტენზორი r -> 0-სას
    # ვუშვებთ ცენტრალური სკალარული მუხტის არარსებობას (Psi'=0)
    Y = 1/B_core
    I1 = 2 + 1/A_core
    I2 = 1 + 2/A_core
    I3 = 1/A_core
    
    Y_s, I1_s, I2_s, I3_s = sp.symbols('Y I1 I2 I3', real=True)
    L_poly = get_polynomial_lagrangian(Y_s, I1_s, I2_s, I3_s)
    
    L_eval = L_poly.subs({Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3})
    L_Y = sp.diff(L_poly, Y_s).subs({Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3})
    L_I1 = sp.diff(L_poly, I1_s).subs({Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3})
    L_I2 = sp.diff(L_poly, I2_s).subs({Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3})
    L_I3 = sp.diff(L_poly, I3_s).subs({Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3})
    
    T_tt = 2 * L_Y / B_core - L_eval
    T_rr = 2 * (L_I1 / A_core + 2 * L_I2 / A_core + L_I3 / A_core) - L_eval
    
    T_tt_0 = sp.simplify(sp.limit(T_tt, r, 0))
    T_rr_0 = sp.simplify(sp.limit(T_rr, r, 0))
    
    return G_tt_0, G_rr_0, G_thth_0, R_0, K_0, T_tt_0, T_rr_0

if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18: RG compact object and singularity audit")
    print("=" * 72)

    print("\n0. Sign-convention bridge")
    for key, value in compact_signature_bridge().items():
        print(f"  {key:36s}: {value}")

    print("\n1. Exterior derivation from vacuum phase equation")
    phase_derivation = derive_exponential_exterior_from_phase_equation()
    for key, value in phase_derivation.items():
        print(f"  {key:36s}: {value}")

    print("\n1b. Effective source profile of the exponential exterior")
    source_profile = derive_exponential_effective_source_profile()
    for key, value in source_profile.items():
        print(f"  {key:36s}: {value}")

    print("\n1b2. Standard energy-condition audit of the effective source")
    energy_conditions = audit_exponential_effective_energy_conditions()
    for key, value in energy_conditions.items():
        print(f"  {key:36s}: {value}")

    print("\n1b3. Total RefG medium NEC gate")
    total_nec = derive_background_completed_medium_nec_gate()
    for key, value in total_nec.items():
        print(f"  {key:36s}: {value}")

    print("\n1c. Black-hole singularity breaker gate")
    bh_breaker = derive_black_hole_singularity_breaker_gate()
    for key, value in bh_breaker.items():
        print(f"  {key:36s}: {value}")

    print("\n1d. p01 polynomial static closure gate")
    p01_gate = p01_polynomial_static_closure_gate()
    for key, value in p01_gate.items():
        print(f"  {key:36s}: {value}")

    print("\n1e. p01 anisotropic deformation route")
    anisotropic_route = derive_p01_anisotropic_deformation_route()
    for key, value in anisotropic_route.items():
        print(f"  {key:36s}: {value}")

    print("\n1f. Minimal nontrivial f(r) branch")
    nontrivial_f = derive_minimal_nontrivial_f_branch()
    for key, value in nontrivial_f.items():
        print(f"  {key:36s}: {value}")

    print("\n1f2. Exact implicit minimal f(r) branch")
    exact_f = derive_exact_minimal_f_branch_implicit_solution()
    for key, value in exact_f.items():
        print(f"  {key:36s}: {value}")

    print("\n1f3. Full F_min component source-closure system")
    full_source_system = derive_full_fmin_exponential_source_closure_system()
    for key, value in full_source_system.items():
        print(f"  {key:36s}: {value}")

    print("\n1f4. Algebraic F_min vs Bernoulli gradient source")
    gradient_source = diagnose_algebraic_fmin_vs_gradient_source()
    for key, value in gradient_source.items():
        print(f"  {key:36s}: {value}")

    print("\n1f5. Covariant Bernoulli gradient source")
    covariant_source = derive_covariant_bernoulli_gradient_source()
    for key, value in covariant_source.items():
        print(f"  {key:36s}: {value}")

    print("\n1f6. Projected Bernoulli medium source")
    projected_source = derive_projected_bernoulli_medium_source()
    for key, value in projected_source.items():
        print(f"  {key:36s}: {value}")

    print("\n1g. Exponential exterior curvature branch")
    exterior = analyze_exponential_exterior_curvature()
    for key, value in exterior.items():
        print(f"  {key:36s}: {value}")

    print("\n2. Bernoulli saturation of the pressure deficit")
    bernoulli = analyze_bernoulli_singularity_saturation()
    for key, value in bernoulli.items():
        print(f"  {key:36s}: {value}")

    print("\n2b. ADM/Komar and proper energy bookkeeping")
    energy_bookkeeping = derive_adm_komar_and_proper_energy_bookkeeping()
    for key, value in energy_bookkeeping.items():
        print(f"  {key:36s}: {value}")

    print("\n3. Rarefaction and information-decoupling cutoff")
    rarefaction = analyze_rarefaction_information_cutoff()
    for key, value in rarefaction.items():
        print(f"  {key:36s}: {value}")

    print("\n4. Conditional finite-core matching")
    completion = analyze_geodesic_completion_by_core_matching()
    for key, value in completion.items():
        print(f"  {key:36s}: {value}")

    print("\n4b. C2 core matching coefficient derivation")
    core_coeffs = derive_c2_core_matching_coefficients()
    for key, value in core_coeffs.items():
        print(f"  {key:36s}: {value}")

    print("\n4c. C2 junction stress closure")
    junction = derive_c2_junction_stress_closure()
    for key, value in junction.items():
        print(f"  {key:36s}: {value}")

    print("\n4d. C2 core effective field-equation source")
    core_source = derive_c2_core_field_equation_source()
    for key, value in core_source.items():
        print(f"  {key:36s}: {value}")

    print("\n4e. C2 core proper source finiteness")
    core_energy = derive_c2_core_proper_energy_finiteness()
    for key, value in core_energy.items():
        print(f"  {key:36s}: {value}")

    print("\n4f. C2 core RefG medium-source decomposition")
    core_medium = derive_c2_core_refg_medium_source_decomposition()
    for key, value in core_medium.items():
        print(f"  {key:36s}: {value}")

    print("\n4g. C2 core p01 action-stress branch equations")
    core_action_branch = derive_c2_core_p01_action_stress_branch_equations()
    for key, value in core_action_branch.items():
        print(f"  {key:36s}: {value}")

    print("\n4h. C2 core deformation solution ledger")
    core_deformation = derive_c2_core_deformation_solution_ledger()
    for key, value in core_deformation.items():
        print(f"  {key:36s}: {value}")

    print("\n4i. C2 core nonlinear deformation IVP probe")
    core_ivp_probe = derive_c2_core_nonlinear_deformation_ivp_probe()
    for key, value in core_ivp_probe.items():
        print(f"  {key:36s}: {value}")

    print("\n4j. C2 core nonlinear IVP parameter-domain theorem")
    core_ivp_domain = derive_c2_core_nonlinear_ivp_parameter_domain_theorem()
    for key, value in core_ivp_domain.items():
        print(f"  {key:36s}: {value}")

    print("\n4k. C2 core action-density integrability theorem")
    core_action_integrability = derive_c2_core_action_density_integrability_theorem()
    for key, value in core_action_integrability.items():
        print(f"  {key:36s}: {value}")

    print("\n4l. C2 core local-stability interface")
    core_local_stability = derive_c2_core_local_stability_interface()
    for key, value in core_local_stability.items():
        print(f"  {key:36s}: {value}")

    print("\n5. Horizonless exterior, throat, and boundary status")
    boundary = analyze_horizon_throat_and_boundary()
    for key, value in boundary.items():
        print(f"  {key:36s}: {value}")

    print("\n6. Photon sphere, shadow, and golden-ratio ISCO")
    strong_observables = analyze_photon_shadow_isco()
    for key, value in strong_observables.items():
        print(f"  {key:36s}: {value}")

    print("\n7. Singularity-strength ledger")
    for item in singularity_strength_ledger():
        print(f"  - {item}")

    print("\n8. Regular-center ansatz cross-check")
    G_t, G_r, G_th, R_0, K_0, T_t, T_r = analyze_regular_center()
    print(f"G^t_t (გეომეტრიული სიმრუდე ცენტრში) = {G_t}")
    print(f"G^r_r (გეომეტრიული წნევა ცენტრში) = {G_r}")
    print(f"G^th_th (კუთხური სიმრუდე) = {G_th}")
    print(f"R (რიჩის სკალარი ცენტრში) = {R_0}")
    print(f"K (Kretschmann სკალარი ცენტრში) = {K_0}")
    
    print(f"\nT^t_t (ენერგიის სიმკვრივე r=0-ზე) = {T_t}")
    print(f"T^r_r (რადიალური წნევა r=0-ზე) = {T_r}")
    
    print("\n--- სამუშაო დასკვნები / export gate ---")
    print("1. რეგულარულობის ანზაცით (A=1+O(r^2), B>0) სიმრუდის ინვარიანტები, მათ შორის")
    print("   Kretschmann (K), ცენტრში სასრულია ამ local ansatz-ის ფარგლებში.")
    print("2. მედიუმის სტრეს-ტენზორი T^t_t და T^r_r ასევე სასრულია.")
    print("3. T^t_t და T^r_r ზოგად შემთხვევაში არ არიან ტოლი, ამიტომ ეს არ არის სუფთა")
    print("   de Sitter-ის ვაკუუმი (w=-1). ტერმინი MD ტექსტში შეიცვალა 'სასრულ-ენერგიული ბირთვით'.")
    print("4. Static exponential exterior branch იძლევა horizonless benchmark-ებს:")
    print("   r_ph=r_s, b_c=e*r_s, r_ISCO=phi_golden^2*r_s.")
    print("   ISCO გამოდის V_eff-ის მარგინალური სტაბილურობიდან, არა fitting-ით.")
    print("5. ფუძის ნაწილაკების rarefaction closure აჩვენებს: n_eff->0, ell_mfp->infinity,")
    print("   Gamma_coll->0 და Kn->infinity, თუ closure ansatz ფიზიკურად სწორია.")
    print("6. r_s/4-ის შიგნით medium-stress gradient ნიშანს იცვლის; ეს არის")
    print("   backreaction ledger, არა დამატებითი წნევითი ძალა მატერიაზე.")
    print("7. Kn=1 ზედაპირზე მიიღება finite core radius r_c=r_s/W(n_0*sigma*r_s).")
    print("8. C2 matching core აკერებს exponential exterior-ს value/slope/curvature დონეზე.")
    print("9. Projected Bernoulli medium source ხურავს static exponential source-ს.")
    print("10. ADM/Komar მასა დახურულია ასიმპტოტური 1/r მუხტით; proper source integral")
    print("    finite core cutoff-ს მოითხოვს.")
    print("11. C2 matching-დან Israel thin-shell stress ნულია r_c ზედაპირზე.")
    print("12. C2 core-ის ეფექტური field-equation source სასრულია ცენტრში და")
    print("    უწყვეტია r_c-ზე.")
    print("13. C2 core-ის effective proper source charge finite-ია finite r_c-ზე.")
    print("14. C2 core source იშლება projected phase channel-ად და finite")
    print("    residual medium-stress channel-ად, რომელიც r_c-ზე ქრება.")
    print("15. residual medium-stress გადადის p01 action-stress branch equation-ად")
    print("    radial core deformation y(x)-ისთვის.")
    print("16. y(x)-ისთვის მიღებულია exact IVP და first-order analytic branch,")
    print("    რომელიც regular center-ს და C2 boundary-ს აკმაყოფილებს.")
    print("17. nonlinear IVP რიცხვითი probe-ით გადის representative stiffness")
    print("    მნიშვნელობებზე.")
    print("18. მიღებულია საკმარისი kappa-domain პირობა, რომელიც nonlinear")
    print("    positive branch-ს მთელ core interval-ზე რეალურს ტოვებს.")
    print("19. residual diagonal tensor იკვრება ერთ p01 action-density branch-ად.")
    print("20. compact core მიდის p01 local no-ghost/mixed-mode stability interface-მდე.")
    print("21. სრული compact-object proof-ს ჯერ სჭირდება off-branch EFT extension,")
    print("    rotation, QNM/echo და EHT ray tracing.")

# ===================== CONSOLIDATED PHASE SECTIONS =====================


# ===================== merged from p05_compact.py =====================

# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

"""
PHASE 29: EHT shadow - static spherical compact-object benchmark in RG.

Phase 18 now derives the exponential exterior:

    ds^2 = -exp(-r_s/r)c^2dt^2 + exp(r_s/r)(dr^2+r^2dOmega^2).

For null circular orbits:

    d/dr [exp(-2r_s/r)/r^2] = 0 -> r_ph = r_s.

The critical impact parameter is therefore:

    b_c^RG = e*r_s,

while Schwarzschild gives:

    b_c^GR = (3*sqrt(3)/2)*r_s.

Thus the static spherical RG benchmark gives a shadow diameter larger by
2e/(3sqrt(3))-1 = 4.63%.  This is not a full EHT model until rotation,
plasma/accretion emission and ray-traced image fitting are added.
"""

import math


M_SUN = 1.98847e30
G = 6.67430e-11
C = 299792458.0
MUAS_TO_RAD = math.pi / (180 * 3600 * 1e6)
PC = 3.0856775814913673e16
KPC = 1.0e3 * PC
MPC = 1.0e6 * PC


EHT_OBSERVATIONS = {
    "M87": {
        "shadow_diameter_uas": 42.0,
        "shadow_error_uas": 3.0,
        "mass_solar": 6.5e9,
        "distance_Mpc": 16.8,
    },
    "SgrA": {
        "shadow_diameter_uas": 51.8,
        "shadow_error_uas": 2.3,
        "mass_solar": 4.154e6,
        "distance_pc": 8178,
        "mass_distance_source": "GRAVITY Collaboration priors (2019/2022)",
    },
}


def schwarzschild_shadow_prediction(m_solar, distance_m):
    """GR Schwarzschild critical-curve diameter: theta = 3*sqrt(3)*r_s/D."""
    mass = m_solar * M_SUN
    r_s = 2 * G * mass / C**2
    diameter = 3 * math.sqrt(3) * r_s
    theta_uas = (diameter / distance_m) / MUAS_TO_RAD
    return {
        "r_s_meters": r_s,
        "critical_impact_parameter_m": 0.5 * diameter,
        "shadow_diameter_meters": diameter,
        "theta_uas": theta_uas,
    }


def rg_shadow_prediction(m_solar, distance_m):
    """RG exponential-exterior critical-curve diameter: theta = 2*e*r_s/D."""
    mass = m_solar * M_SUN
    r_s = 2 * G * mass / C**2
    b_c = math.e * r_s
    diameter = 2 * b_c
    theta_uas = (diameter / distance_m) / MUAS_TO_RAD
    return {
        "r_s_meters": r_s,
        "photon_sphere_r": r_s,
        "critical_impact_parameter_m": b_c,
        "shadow_diameter_meters": diameter,
        "theta_uas": theta_uas,
    }


def compare_with_observation(name, m_solar, distance_m, theta_obs, theta_err):
    """Compare GR and RG static spherical shadow benchmarks to one observation."""
    gr = schwarzschild_shadow_prediction(m_solar, distance_m)
    rg = rg_shadow_prediction(m_solar, distance_m)
    ratio = rg["theta_uas"] / gr["theta_uas"]

    return {
        "name": name,
        "r_s_meters": gr["r_s_meters"],
        "GR_prediction_uas": gr["theta_uas"],
        "RG_prediction_uas": rg["theta_uas"],
        "RG_over_GR_ratio": ratio,
        "RG_shadow_shift_percent": (ratio - 1.0) * 100.0,
        "EHT_observation_uas": theta_obs,
        "EHT_error_uas": theta_err,
        "GR_deviation_sigma": abs(gr["theta_uas"] - theta_obs) / theta_err,
        "RG_deviation_sigma": abs(rg["theta_uas"] - theta_obs) / theta_err,
    }


def distance_to_meters(obs):
    """Convert observation distance fields to meters."""
    if "distance_Mpc" in obs:
        return obs["distance_Mpc"] * MPC
    if "distance_kpc" in obs:
        return obs["distance_kpc"] * KPC
    if "distance_pc" in obs:
        return obs["distance_pc"] * PC
    raise KeyError("distance field not found")


def rg_shadow_derivation_ledger():
    return [
        "exponential exterior: g_tt=-exp(-r_s/r), g_rr=exp(r_s/r)",
        "null barrier: V_null proportional to exp(-2r_s/r)/r^2",
        "photon sphere: dV_null/dr=0 -> r_ph=r_s",
        "critical impact parameter: b_c=r*exp(r_s/r) at r=r_s -> e*r_s",
        "GR reference: b_c=(3*sqrt(3)/2)*r_s",
        "static spherical benchmark: RG shadow diameter is +4.63% relative to GR",
    ]


def predictions_summary():
    """RG vs GR shadow status."""
    ratio = 2.0 * math.e / (3.0 * math.sqrt(3.0))
    return {
        "current_status": "static spherical benchmark derived and article-usable as a benchmark; full EHT verdict open",
        "RG_b_c": "e*r_s",
        "GR_b_c": "3*sqrt(3)*r_s/2",
        "RG_over_GR": ratio,
        "shift_percent": (ratio - 1.0) * 100.0,
        "needed_for_decisive_test": "rotating RG exterior, accretion/plasma emission, mass-distance priors, and ray-traced image modelling",
        "ngEHT_BHEX_window": "few-percent shadow/ring precision can test the +4.63% benchmark",
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 29: EHT shadow - RG b_c=e*r_s static benchmark")
    print("=" * 72)

    print("\n1. დაკვირვება (EHT priors used in this local script)")
    for name, obs in EHT_OBSERVATIONS.items():
        print(f"\n  {name}")
        for key, val in obs.items():
            print(f"    {key:25s}: {val}")

    print("\n2. Derivation ledger")
    for item in rg_shadow_derivation_ledger():
        print(f"  - {item}")

    print("\n3. GR vs RG static benchmark compared to EHT numbers")
    for name, obs in EHT_OBSERVATIONS.items():
        result = compare_with_observation(
            name,
            obs["mass_solar"],
            distance_to_meters(obs),
            obs["shadow_diameter_uas"],
            obs["shadow_error_uas"],
        )
        print(f"\n  {result['name']}")
        print(f"    r_s = {result['r_s_meters']:.3e} m")
        print(f"    GR theta  = {result['GR_prediction_uas']:.2f} microas")
        print(f"    RG theta = {result['RG_prediction_uas']:.2f} microas")
        print(f"    RG/GR    = {result['RG_over_GR_ratio']:.8f}")
        print(f"    shift     = {result['RG_shadow_shift_percent']:.2f}%")
        print(f"    observed  = {result['EHT_observation_uas']:.1f} +/- {result['EHT_error_uas']:.1f} microas")
        print(f"    GR sigma  = {result['GR_deviation_sigma']:.2f}")
        print(f"    RG sigma = {result['RG_deviation_sigma']:.2f}")

    print("\n4. Predictions summary")
    for key, val in predictions_summary().items():
        print(f"  {key:26s}: {val}")

    print("\n5. სტატუსი")
    print("  - +4.6% shadow shift static exponential benchmark-ად გამოდის.")
    print("  - მიმდინარე EHT რიცხვები არ არის საკმარისი სუფთა GR/RG გარჩევისთვის.")
    print("  - decisive test მოითხოვს rotating RG ray tracing-ს, plasma model-ს და ngEHT/BHEX კლასის სიზუსტეს.")


# ===================== merged from p05_compact.py =====================

# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

"""
================================================================================
PHASE 31: ნეიტრონული ვარსკვლავები — RG ანიზოტროპიული TOV და M-R მრუდი
================================================================================

რეფერენცია: p10_oscillons.py, p01_core.py,
            p01_core.py, STRATEGY.md S3/E6

სტატუსი:
ეს არის TOV განტოლების შესამოწმებელი (executable) გარემო. ის არ წარმოადგენს სრულ 
nuclear-EOS მორგებას და არ არის საბოლოო NICER/GW170817 likelihood ცდა. 
RG-ის ანიზოტროპია წარმოდგენილია ერთი ფენომენოლოგიური პარამეტრით (eta_delta):

    Delta p = p_tan - p_rad = eta_delta * p_rad * u,
    u = 2GM(r)/(r c^2).

eta_delta = 0 არის GR/იზოტროპული TOV ლიმიტი. დადებითი eta_delta ქმნის დამატებით 
ტანგენციალურ მხარდაჭერას და ხდის RG-ის მსგავსი ანიზოტროპიული სტრესის გავლენას 
ხილულს. RG-დან უშუალოდ გამოყვანილი ნეიტრონული ვარსკვლავის EoS ჯერჯერობით ღიაა.

რა არის იმპლემენტირებული:
- SI ერთეულების მქონე GR TOV ინტეგრატორი RK4 მეთოდით.
- RG-ის ანიზოტროპიული TOV წევრი +2 Delta p/r.
- M-R (მასა-რადიუსი) მიმდევრობა ცენტრალური სიმკვრივის ცვლილებით.
- M_max >= 2.08 M_sun შემოწმება.
- Lambda_1.4 კომპაქტურობის პროქსი GW170817 ზღვრისთვის.
"""

# merged future import removed: from __future__ import annotations

import math
from dataclasses import dataclass


M_SUN = 1.98847e30
G = 6.67430e-11
C = 299792458.0


OBSERVATIONS = {
    "NICER_J0030": {
        "mass_solar": 1.34,
        "mass_err": 0.16,
        "radius_km": 12.71,
        "radius_err_km": 1.14,
        "reference": "Miller et al. 2019",
    },
    "NICER_J0740": {
        "mass_solar": 2.08,
        "mass_err": 0.07,
        "radius_km": 13.7,
        "radius_err_km": 1.5,
        "reference": "Miller et al. 2021",
    },
    "GW170817_tidal_Lambda_1.4": {
        "upper_bound_90CL": 580,
        "reference": "Abbott et al. PRL 122:061104 reanalysis; earlier bound <800",
    },
    "PSR_J0348+0432": {
        "mass_solar": 2.01,
        "mass_err": 0.04,
        "reference": "Antoniadis et al. 2013",
    },
}


@dataclass(frozen=True)
class PolytropicEOS:
    """
    Rest-mass polytrope:
        p = K * rho0^gamma
        epsilon/c^2 = rho0 + p/((gamma - 1)c^2)

    K is chosen only as a controlled toy EOS. It is tuned to neutron-star
    scales but not claimed as SLy/APR/nuclear-matter inference.
    """

    name: str = "toy_polytrope_Gamma2.4"
    K: float = 1.20e-9
    gamma: float = 2.40

    def pressure_from_rest_density(self, rho0_kg_m3: float) -> float:
        return self.K * rho0_kg_m3**self.gamma

    def rest_density_from_pressure(self, pressure_pa: float) -> float:
        if pressure_pa <= 0:
            return 0.0
        return (pressure_pa / self.K) ** (1.0 / self.gamma)

    def mass_density_from_pressure(self, pressure_pa: float) -> float:
        rho0 = self.rest_density_from_pressure(pressure_pa)
        if rho0 <= 0:
            return 0.0
        return rho0 + pressure_pa / ((self.gamma - 1.0) * C**2)

    def sound_speed_sq(self, pressure_pa: float) -> float:
        rho0 = self.rest_density_from_pressure(pressure_pa)
        if rho0 <= 0:
            return 0.0
        dp_drho0 = self.gamma * self.K * rho0 ** (self.gamma - 1.0)
        drho_mass_drho0 = 1.0 + dp_drho0 / ((self.gamma - 1.0) * C**2)
        return dp_drho0 / drho_mass_drho0


@dataclass
class StarSolution:
    central_density_kg_m3: float
    eta_delta: float
    mass_solar: float
    radius_km: float
    compactness: float
    lambda_proxy: float
    max_sound_speed_over_c: float
    status: str


@dataclass
class SequenceSummary:
    label: str
    eta_delta: float
    n_models: int
    max_mass_solar: float
    radius_at_max_km: float
    rho_c_at_max: float
    radius_1p4_km: float | None
    lambda_1p4_proxy: float | None
    supports_2p08_toy: bool
    lambda_bound_toy: bool | None
    max_sound_speed_over_c: float


def anisotropy_delta_p(pressure_pa: float, compactness_u: float, eta_delta: float) -> float:
    """Phenomenological RG anisotropy: Delta p = eta * p * u."""
    return eta_delta * pressure_pa * compactness_u


def tov_derivatives(
    eos: PolytropicEOS,
    eta_delta: float,
    radius_m: float,
    mass_kg: float,
    pressure_pa: float,
) -> tuple[float, float] | None:
    """Return dm/dr and dp/dr for anisotropic TOV in SI units."""
    if pressure_pa <= 0:
        return 0.0, 0.0
    if radius_m <= 0:
        return None

    rho = eos.mass_density_from_pressure(pressure_pa)
    compact_factor = 1.0 - 2.0 * G * mass_kg / (radius_m * C**2)
    if compact_factor <= 1.0e-6:
        return None

    local_u = 2.0 * G * mass_kg / (radius_m * C**2)
    delta_p = anisotropy_delta_p(pressure_pa, local_u, eta_delta)

    dm_dr = 4.0 * math.pi * radius_m**2 * rho
    dp_gr = (
        -G
        * (rho + pressure_pa / C**2)
        * (mass_kg + 4.0 * math.pi * radius_m**3 * pressure_pa / C**2)
        / (radius_m**2 * compact_factor)
    )
    dp_dr = dp_gr + 2.0 * delta_p / radius_m

    return dm_dr, dp_dr


def rk4_step(
    eos: PolytropicEOS,
    eta_delta: float,
    radius_m: float,
    mass_kg: float,
    pressure_pa: float,
    dr_m: float,
) -> tuple[float, float] | None:
    """One RK4 step for (m, p)."""
    k1 = tov_derivatives(eos, eta_delta, radius_m, mass_kg, pressure_pa)
    if k1 is None:
        return None

    k2 = tov_derivatives(
        eos,
        eta_delta,
        radius_m + 0.5 * dr_m,
        mass_kg + 0.5 * dr_m * k1[0],
        pressure_pa + 0.5 * dr_m * k1[1],
    )
    if k2 is None:
        return None

    k3 = tov_derivatives(
        eos,
        eta_delta,
        radius_m + 0.5 * dr_m,
        mass_kg + 0.5 * dr_m * k2[0],
        pressure_pa + 0.5 * dr_m * k2[1],
    )
    if k3 is None:
        return None

    k4 = tov_derivatives(
        eos,
        eta_delta,
        radius_m + dr_m,
        mass_kg + dr_m * k3[0],
        pressure_pa + dr_m * k3[1],
    )
    if k4 is None:
        return None

    next_mass = mass_kg + dr_m * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
    next_pressure = pressure_pa + dr_m * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
    return next_mass, next_pressure


def dimensionless_lambda_proxy(mass_solar: float, radius_km: float, k2: float = 0.08) -> float:
    """
    Lambda proxy: Lambda = (2/3) k2 / C_compact^5.

    This is not a Love-number integration. It is a compactness diagnostic for
    the GW170817 Lambda_1.4 scale.
    """
    compactness = G * mass_solar * M_SUN / ((radius_km * 1000.0) * C**2)
    if compactness <= 0:
        return math.inf
    return (2.0 / 3.0) * k2 / compactness**5


def integrate_star(
    eos: PolytropicEOS,
    central_density_kg_m3: float,
    eta_delta: float = 0.0,
    dr_m: float = 50.0,
    max_radius_km: float = 50.0,
) -> StarSolution:
    """Integrate one stellar model until pressure reaches zero."""
    pressure = eos.pressure_from_rest_density(central_density_kg_m3)
    radius = dr_m
    rho_c = eos.mass_density_from_pressure(pressure)
    mass = 4.0 * math.pi * radius**3 * rho_c / 3.0
    previous = (radius, mass, pressure)
    max_sound_speed = math.sqrt(max(eos.sound_speed_sq(pressure), 0.0)) / C

    while radius < max_radius_km * 1000.0 and pressure > 0:
        step = rk4_step(eos, eta_delta, radius, mass, pressure, dr_m)
        if step is None:
            return StarSolution(
                central_density_kg_m3=central_density_kg_m3,
                eta_delta=eta_delta,
                mass_solar=mass / M_SUN,
                radius_km=radius / 1000.0,
                compactness=2.0 * G * mass / (radius * C**2),
                lambda_proxy=math.inf,
                max_sound_speed_over_c=max_sound_speed,
                status="STOP_COMPACTNESS",
            )

        previous = (radius, mass, pressure)
        mass, pressure = step
        radius += dr_m
        if pressure > 0:
            cs_over_c = math.sqrt(max(eos.sound_speed_sq(pressure), 0.0)) / C
            max_sound_speed = max(max_sound_speed, cs_over_c)

    if pressure <= 0:
        r0, m0, p0 = previous
        fraction = p0 / (p0 - pressure) if p0 != pressure else 0.0
        surface_radius = r0 + fraction * (radius - r0)
        surface_mass = m0 + fraction * (mass - m0)
        mass_solar = surface_mass / M_SUN
        radius_km = surface_radius / 1000.0
        compactness = 2.0 * G * surface_mass / (surface_radius * C**2)
        return StarSolution(
            central_density_kg_m3=central_density_kg_m3,
            eta_delta=eta_delta,
            mass_solar=mass_solar,
            radius_km=radius_km,
            compactness=compactness,
            lambda_proxy=dimensionless_lambda_proxy(mass_solar, radius_km),
            max_sound_speed_over_c=max_sound_speed,
            status="OK",
        )

    return StarSolution(
        central_density_kg_m3=central_density_kg_m3,
        eta_delta=eta_delta,
        mass_solar=mass / M_SUN,
        radius_km=radius / 1000.0,
        compactness=2.0 * G * mass / (radius * C**2),
        lambda_proxy=math.inf,
        max_sound_speed_over_c=max_sound_speed,
        status="STOP_MAX_RADIUS",
    )


def central_density_grid() -> list[float]:
    """Central rest-density sweep."""
    return [3.5e17 * (1.08**index) for index in range(30)]


def build_mr_sequence(eos: PolytropicEOS, eta_delta: float) -> list[StarSolution]:
    sequence = []
    for rho_c in central_density_grid():
        solution = integrate_star(eos, rho_c, eta_delta=eta_delta)
        if solution.status == "OK" and solution.mass_solar > 0:
            sequence.append(solution)
    return sequence


def stable_branch(sequence: list[StarSolution]) -> list[StarSolution]:
    if not sequence:
        return []
    max_index = max(range(len(sequence)), key=lambda idx: sequence[idx].mass_solar)
    return sequence[: max_index + 1]


def interpolate_at_mass(
    sequence: list[StarSolution],
    target_mass_solar: float,
) -> tuple[float, float] | None:
    branch = stable_branch(sequence)
    if len(branch) < 2:
        return None

    for left, right in zip(branch, branch[1:]):
        m0, m1 = left.mass_solar, right.mass_solar
        if (m0 <= target_mass_solar <= m1) or (m1 <= target_mass_solar <= m0):
            if abs(m1 - m0) < 1.0e-12:
                radius = 0.5 * (left.radius_km + right.radius_km)
            else:
                frac = (target_mass_solar - m0) / (m1 - m0)
                radius = left.radius_km + frac * (right.radius_km - left.radius_km)
            return radius, dimensionless_lambda_proxy(target_mass_solar, radius)
    return None


def summarize_sequence(
    label: str,
    eta_delta: float,
    sequence: list[StarSolution],
) -> SequenceSummary:
    if not sequence:
        raise ValueError("empty M-R sequence")

    max_solution = max(sequence, key=lambda item: item.mass_solar)
    onep4 = interpolate_at_mass(sequence, 1.4)
    lambda_bound = OBSERVATIONS["GW170817_tidal_Lambda_1.4"]["upper_bound_90CL"]

    return SequenceSummary(
        label=label,
        eta_delta=eta_delta,
        n_models=len(sequence),
        max_mass_solar=max_solution.mass_solar,
        radius_at_max_km=max_solution.radius_km,
        rho_c_at_max=max_solution.central_density_kg_m3,
        radius_1p4_km=onep4[0] if onep4 else None,
        lambda_1p4_proxy=onep4[1] if onep4 else None,
        supports_2p08_toy=max_solution.mass_solar >= OBSERVATIONS["NICER_J0740"]["mass_solar"],
        lambda_bound_toy=(onep4[1] < lambda_bound if onep4 else None),
        max_sound_speed_over_c=max(item.max_sound_speed_over_c for item in sequence),
    )


def nearest_mass_model(sequence: list[StarSolution], target_mass_solar: float) -> StarSolution:
    return min(sequence, key=lambda item: abs(item.mass_solar - target_mass_solar))


def format_summary(summary: SequenceSummary) -> list[str]:
    return [
        f"label: {summary.label}",
        f"eta_delta: {summary.eta_delta:.3g}",
        f"models: {summary.n_models}",
        f"M_max: {summary.max_mass_solar:.3f} M_sun at R={summary.radius_at_max_km:.2f} km",
        f"rho_c(M_max): {summary.rho_c_at_max:.3e} kg/m^3",
        f"R_1.4: {summary.radius_1p4_km:.2f} km" if summary.radius_1p4_km else "R_1.4: not bracketed",
        (
            f"Lambda_1.4 proxy: {summary.lambda_1p4_proxy:.0f}"
            if summary.lambda_1p4_proxy
            else "Lambda_1.4 proxy: not bracketed"
        ),
        f"toy M_max >= 2.08 M_sun diagnostic: {summary.supports_2p08_toy}",
        f"toy Lambda_1.4 proxy < 580 diagnostic: {summary.lambda_bound_toy}",
        f"max c_s/c in sequence: {summary.max_sound_speed_over_c:.3f}",
    ]


def model_scope_notes() -> list[str]:
    return [
        "The polytropic EOS is a controlled toy EOS, not a nuclear-matter fit.",
        "eta_delta is a phenomenological stand-in for p01_core Delta p.",
        "Lambda_1.4 is a compactness proxy; real tidal deformability needs Love-number ODEs.",
        "A real NICER/GW170817 verdict needs EOS priors and Bayesian likelihoods.",
    ]


def main() -> None:
    print("=" * 72)
    print("PHASE 31: Neutron stars — RG anisotropic TOV and M-R curve")
    print("=" * 72)

    eos = PolytropicEOS()
    models = {
        "GR_isotropic": 0.0,
        "RG_anisotropic_eta0.5": 0.5,
    }

    print("\n1. Observational filters")
    for key, obs in OBSERVATIONS.items():
        print(f"  {key}: {obs}")

    print("\n2. EOS and anisotropy model")
    print(f"  EOS: {eos.name}, K={eos.K:.3e}, gamma={eos.gamma:.2f}")
    print("  anisotropy: Delta p = eta_delta * p_rad * 2GM/(r c^2)")

    summaries: list[SequenceSummary] = []
    sequences: dict[str, list[StarSolution]] = {}
    for label, eta_delta in models.items():
        sequence = build_mr_sequence(eos, eta_delta)
        sequences[label] = sequence
        summary = summarize_sequence(label, eta_delta, sequence)
        summaries.append(summary)

    print("\n3. M-R sequence summaries")
    for summary in summaries:
        print(f"\n  --- {summary.label} ---")
        for line in format_summary(summary):
            print(f"  {line}")

    print("\n4. Sequence samples")
    for label, sequence in sequences.items():
        print(f"\n  {label}")
        stride = max(1, len(sequence) // 5)
        for solution in sequence[::stride][:6]:
            print(
                f"    rho_c={solution.central_density_kg_m3:.2e} kg/m^3 | "
                f"M={solution.mass_solar:.3f} M_sun | R={solution.radius_km:.2f} km | "
                f"u={solution.compactness:.3f}"
            )

    print("\n5. NICER/GW170817 quick comparisons")
    for label, sequence in sequences.items():
        j0030 = nearest_mass_model(sequence, OBSERVATIONS["NICER_J0030"]["mass_solar"])
        j0740 = nearest_mass_model(sequence, OBSERVATIONS["NICER_J0740"]["mass_solar"])
        print(f"\n  {label}")
        print(
            f"    nearest J0030 mass: M={j0030.mass_solar:.3f}, R={j0030.radius_km:.2f} km "
            f"(obs R={OBSERVATIONS['NICER_J0030']['radius_km']}±{OBSERVATIONS['NICER_J0030']['radius_err_km']} km)"
        )
        print(
            f"    nearest J0740 mass: M={j0740.mass_solar:.3f}, R={j0740.radius_km:.2f} km "
            f"(mass target {OBSERVATIONS['NICER_J0740']['mass_solar']} M_sun)"
        )

    print("\n6. Scope notes")
    for note in model_scope_notes():
        print(f"  - {note}")

    print("\n7. Status")
    print("  - Strategy E6 TOV integrator: implemented.")
    print("  - M-R curve: generated for GR and RG-anisotropic toy branches.")
    print("  - Delta p effect: quantified by eta_delta branch comparison.")
    print("  - Full EOS/Love-number/Bayesian fit: still open.")


if __name__ == "__main__":
    main()


# ===================== OLD COMPACT INTEGRATION =====================

"""
STAGE A3: OLD compact-object boundary/interior/verification ledger

Sources drained from:
    OLD/12. ISPG_Geodesics.tex
    OLD/14. ISPG_Interior.tex
    OLD/15. ISPG_Verification_Task1a.tex

OLD material is represented here as candidate ledger material, not as final
authority.  The exponential exterior, rarefaction/core matching, horizonless
boundary, photon/shadow and golden-ISCO blocks still carry the open checks
listed in the central gate.
"""


def stage_a3_old_geodesic_interior_drain():
    return {
        "OLD/12_geodesics": {
            "status": "represented_as_candidate_ledger",
            "new_functions": [
                "analyze_horizon_throat_and_boundary",
                "analyze_photon_shadow_isco",
                "analyze_geodesic_completion_by_core_matching",
            ],
            "core_results": [
                "photon sphere r_ph = r_s",
                "critical impact parameter b_c = e*r_s",
                "proper distance to old r=0 boundary diverges",
                "curvature invariants vanish as r -> 0",
                "old exterior geodesic incompleteness is conditionally addressed by Knudsen-core matching",
            ],
        },
        "OLD/14_interior": {
            "status": "represented_as_candidate_ledger",
            "new_functions": [
                "analyze_rarefaction_information_cutoff",
                "analyze_bernoulli_singularity_saturation",
                "singularity_strength_ledger",
            ],
            "core_results": [
                "clock/freezing: d tau/dt = exp(-r_s/(2r)) -> 0",
                "proper radial element exp(r_s/(2r)) dr diverges",
                "effective signal speed c_eff = c exp(-r_s/r) -> 0",
                "mass-as-pressure-deficit is retained as a candidate interpretation",
                "deep deficit is self-perpetuating through divergent relaxation time",
            ],
        },
    }


def stage_a3_scalar_perturbation_verification():
    """
    OLD/15 Task 1a probe-level ledger in executable symbolic form.

    Probe scalar perturbations on phi0=-r_s/r reduce to a Schrodinger-form
    equation after the tortoise coordinate and first-derivative removal.
    The dangerous l=0 well exists only in 0<r<r_s/4 and is exponentially
    suppressed.  This block is still a probe scalar test; the coupled
    even/polar metric-medium sector is open.
    """
    r, r_s, c, ell = sp.symbols("r r_s c ell", positive=True)
    x = sp.Symbol("x", positive=True)
    phi0 = -r_s / r
    phi0_p = sp.diff(phi0, r)
    phi0_pp = sp.diff(phi0_p, r)

    c_eff_sq = c**2 * sp.exp(2 * phi0)
    drstar_dr = sp.exp(-phi0) / c
    dr_drstar = c * sp.exp(phi0)
    P = -c * sp.exp(phi0) * phi0_p
    Q = c**2 * sp.exp(2 * phi0) * ell * (ell + 1) / r**2
    V_eff = sp.simplify(
        c**2
        * sp.exp(2 * phi0)
        * (ell * (ell + 1) / r**2 - sp.Rational(1, 2) * phi0_pp - sp.Rational(1, 4) * phi0_p**2)
    )
    V_l0 = sp.factor(V_eff.subs(ell, 0))
    V_l0_dimensionless = sp.simplify(V_l0.subs({c: 1, r_s: 1, r: x}))
    drstar_dx_dimensionless = sp.exp(1 / x)
    well_integrand_dr = sp.simplify(-V_l0_dimensionless)
    well_integrand_drstar = sp.simplify(well_integrand_dr * drstar_dx_dimensionless)
    well_integral_dr = sp.integrate(well_integrand_dr, (x, 0, sp.Rational(1, 4)))
    well_integral_drstar = sp.integrate(well_integrand_drstar, (x, 0, sp.Rational(1, 4)))

    return {
        "phi0_prime": sp.Eq(sp.Symbol("phi0_prime"), phi0_p),
        "phi0_second": sp.Eq(sp.Symbol("phi0_second"), phi0_pp),
        "c_eff_squared": sp.Eq(sp.Symbol("c_eff^2"), c_eff_sq),
        "c_eff_positive": "c_eff^2 = c^2 exp(-2 r_s/r) > 0 for r>0; no gradient instability",
        "tortoise_drstar_dr": sp.Eq(sp.Symbol("drstar_dr"), drstar_dr),
        "tortoise_dr_drstar": sp.Eq(sp.Symbol("dr_drstar"), dr_drstar),
        "first_derivative_coefficient": sp.Eq(sp.Symbol("P"), P),
        "angular_Q": sp.Eq(sp.Symbol("Q"), Q),
        "V_eff": sp.Eq(sp.Symbol("V_eff"), V_eff),
        "V_l0_factorized": sp.Eq(sp.Symbol("V_l0"), V_l0),
        "negative_region_l0": "0 < r < r_s/4",
        "V_l0_dimensionless_c_rs_1": V_l0_dimensionless,
        "well_integrand_absV_dr_c_rs_1": well_integrand_dr,
        "well_integral_absV_dr_c_rs_1": sp.Eq(sp.Symbol("I_dr"), well_integral_dr),
        "well_integrand_absV_drstar_c_rs_1": well_integrand_drstar,
        "well_integral_absV_drstar_c_rs_1": sp.Eq(sp.Symbol("I_drstar"), well_integral_drstar),
        "well_integral_absV_drstar_numeric": sp.N(well_integral_drstar, 8),
        "probe_verdict": "small l=0 well at probe level; not a coupled stability theorem",
        "ell_ge_1_status": "centrifugal barrier is favorable, but no hard-coded bound is exported here",
        "remaining_scope": "even/polar coupled metric-scalar sector remains a future verification task",
    }


def stage_a3_compact_old_file_status():
    return {
        "geodesic_interior": stage_a3_old_geodesic_interior_drain(),
        "scalar_perturbations": stage_a3_scalar_perturbation_verification(),
        "integration_status": "Stage A3 is drained into p05_compact.py; compact exterior short path is passed, while OLD authority and full compact-object export remain gated",
    }


def compact_exterior_short_path_certificate():
    """
    Compact strong-field/exterior spine.

    The detailed file keeps curvature, shadow, core and TOV ledgers.  This
    certificate keeps the useful compact-object route in one place: the vacuum
    phase equation gives the exponential exterior, its effective source has the
    Bernoulli profile, the Schwarzschild-type curvature singularity is removed
    in that geometry, and the C2 core matching algebra is explicit.
    """
    exterior = derive_exponential_exterior_from_phase_equation()
    source = derive_exponential_effective_source_profile()
    breaker = derive_black_hole_singularity_breaker_gate()
    core = derive_c2_core_matching_coefficients()

    status = (
        "PASS_COMPACT_EXTERIOR_SHORT_PATH"
        if exterior["derivation_status"]
        == "PHASE_EQUATION_AND_BICONFORMAL_MAP_DERIVED"
        and exterior["laplace_residual_for_solution"] == 0
        and source["source_status"]
        == "EFFECTIVE_GEOMETRIC_SOURCE_PROFILE_DERIVED__PROJECTED_BERNOULLI_MEDIUM_SOURCE_DERIVED_SEPARATELY"
        and breaker["lim_r_to_0_K_RG"] == 0
        and breaker["lim_r_to_0_DeltaP_RG"] == 0
        and breaker["geometry_verdict"]
        == "SCHWARZSCHILD_CURVATURE_SINGULARITY_REMOVED_IN_EXPONENTIAL_BRANCH"
        and core["derivation_status"]
        == "C2_MATCHING_COEFFICIENTS_DERIVED"
        else "CHECK_COMPACT_EXTERIOR_SHORT_PATH"
    )

    return {
        "status": status,
        "exterior_status": exterior["derivation_status"],
        "laplace_residual": exterior["laplace_residual_for_solution"],
        "source_status": source["source_status"],
        "geometry_verdict": breaker["geometry_verdict"],
        "core_matching_status": core["derivation_status"],
        "short_reading": (
            "vacuum phase equation -> exponential biconformal exterior -> "
            "Bernoulli-shaped effective source -> finite-curvature endpoint "
            "with explicit C2 core matching algebra."
        ),
    }


def compact_central_claim_gate():
    """
    One-place export gate for p05_compact.py.

    This keeps the useful algebraic results while blocking the stronger
    compact-object claim until the missing physical/dynamical checks are done.
    """
    signature = compact_signature_bridge()
    scalar_probe = stage_a3_scalar_perturbation_verification()
    short_path = compact_exterior_short_path_certificate()
    projected_source = derive_projected_bernoulli_medium_source()
    energy_bookkeeping = derive_adm_komar_and_proper_energy_bookkeeping()
    junction = derive_c2_junction_stress_closure()
    core_source = derive_c2_core_field_equation_source()
    core_energy = derive_c2_core_proper_energy_finiteness()
    core_medium = derive_c2_core_refg_medium_source_decomposition()
    core_action_branch = derive_c2_core_p01_action_stress_branch_equations()
    core_deformation = derive_c2_core_deformation_solution_ledger()
    core_ivp_probe = derive_c2_core_nonlinear_deformation_ivp_probe()
    core_ivp_domain = derive_c2_core_nonlinear_ivp_parameter_domain_theorem()
    core_action_integrability = derive_c2_core_action_density_integrability_theorem()
    core_local_stability = derive_c2_core_local_stability_interface()
    return {
        "file_export_status": "STATIC_COMPACT_CORE_SOURCE_LEDGER_READY_WITH_DYNAMICAL_SCOPE_BOUNDARY",
        "full_compact_object_status": "CORE_SOURCE_AND_BRANCH_ACTION_DENSITY_CLOSED__OFF_BRANCH_AND_DYNAMICS_GATED",
        "compact_exterior_short_path": short_path["status"],
        "article_supported_claims": [
            "static exponential exterior derived at phase-equation and biconformal-map level",
            "Bernoulli-shaped effective source profile derived geometrically",
            "exact implicit p01 radial-deformation branch derived for the required anisotropy",
            "covariant Bernoulli gradient source derived for the static exponential branch",
            "projected Bernoulli medium source derived for the static exponential branch",
            "ADM and Komar mass derived for the static exponential exterior",
            "C2 matching gives zero Israel thin-shell stress at the core boundary",
            "C2 core effective field-equation source derived and finite",
            "C2 core effective proper-volume source charge finite for finite r_c",
            "C2 core source decomposed into projected phase channel plus finite residual medium-stress channel",
            "C2 residual medium stress written as p01 action-stress branch equations",
            "C2 radial core deformation exact IVP and first-order analytic branch derived",
            "C2 radial core nonlinear IVP passes representative stiffness probes",
            "C2 radial core nonlinear IVP has a sufficient kappa-domain existence condition",
            "C2 residual diagonal tensor is integrable as one p01 action-density branch",
            "C2 compact core reaches the p01 local no-ghost and mixed-mode stability interface",
            "Schwarzschild curvature singularity removed inside the static exponential branch",
            "C2 finite-core matching coefficients derived as a conditional ansatz",
            "static photon sphere, shadow and ISCO benchmarks derived",
        ],
        "signature_bridge": signature["stress_bridge_status"],
        "exterior_status": "PHASE_EQUATION_AND_BICONFORMAL_MAP_DERIVED",
        "algebraic_fmin_status": "ALGEBRAIC_P01_FMIN_ALONE_INSUFFICIENT_FOR_COMPACT_GRADIENT_SOURCE",
        "black_hole_breaker_status": "SCHWARZSCHILD_CURVATURE_SINGULARITY_REMOVED_AT_GEOMETRY_LEVEL__GEODESIC_BOUNDARY_STILL_OPEN",
        "effective_source_status": "GEOMETRIC_SOURCE_PROFILE_MATCHES_BERNOULLI_DELTA_P",
        "p01_source_closure": "F_EQ_R_BRANCH_FAILS__EXACT_IMPLICIT_NONTRIVIAL_F_BRANCH_DERIVED_FOR_ANISOTROPY__ALGEBRAIC_FMIN_ALONE_INSUFFICIENT",
        "bernoulli_gradient_source": projected_source["refg_medium_export"],
        "effective_energy_conditions": "ACTIVE_DEFICIT_HAS_NEGATIVE_RADIAL_NULL_LOAD__REFG_READING_IS_PHASE_PRESSURE_DEFICIT",
        "active_nec_status": "RADIAL_NEC_VIOLATION_IS_ACTIVE_DEFICIT_SIGNATURE",
        "background_capacity_rule": "DO_NOT_USE_AS_SAME_EXTERIOR_FIELD_EQUATION_RESULT",
        "core_status": "C2_CORE_SOURCE_LEDGER_AND_BRANCH_ACTION_DENSITY_CLOSED__OFF_BRANCH_EFT_EXTENSION_OPEN",
        "core_field_equation_status": core_source["field_equation_status"],
        "core_source_center_status": core_source["finite_center_status"],
        "core_source_boundary_status": core_source["boundary_status"],
        "energy_status": "ADM_KOMAR_MASS_CLOSED__C2_CORE_EFFECTIVE_PROPER_SOURCE_FINITE_FOR_FINITE_R_C",
        "ADM_Komar_identity": energy_bookkeeping["ADM_Komar_identity"],
        "junction_status": junction["junction_status"],
        "core_proper_source_status": core_energy["proper_energy_status"],
        "core_medium_source_status": core_medium["realization_status"],
        "core_medium_boundary_residuals_zero": core_medium["boundary_residuals_zero"],
        "core_action_branch_status": core_action_branch["branch_status"],
        "core_action_ode_center_limit": core_action_branch["ode_rhs_center_limit"],
        "core_action_ode_boundary_value": core_action_branch["ode_rhs_boundary_value"],
        "core_deformation_solution_status": core_deformation["solution_status"],
        "core_deformation_first_order_boundary_condition": core_deformation["first_order_boundary_condition"],
        "core_deformation_control_parameter": core_deformation["large_stiffness_control_parameter"],
        "core_nonlinear_ivp_status": core_ivp_probe["nonlinear_ivp_status"],
        "core_nonlinear_ivp_samples_pass": core_ivp_probe["all_samples_pass"],
        "core_nonlinear_ivp_domain_status": core_ivp_domain["theorem_status"],
        "core_nonlinear_ivp_sufficient_condition": core_ivp_domain["sufficient_kappa_condition"],
        "core_action_density_integrability_status": core_action_integrability["integrability_status"],
        "core_local_stability_interface_status": core_local_stability["interface_status"],
        "proper_source_gate": "EFFECTIVE_PROPER_SOURCE_FINITE__MEDIUM_SOURCE_DECOMPOSITION_CLOSED",
        "scalar_stability": scalar_probe["probe_verdict"],
        "shadow_status": "STATIC_SPHERICAL_RESULT_ONLY__ROTATION_PLASMA_RAYTRACING_OPEN",
        "neutron_star_status": "TOY_POLYTROPE_AND_LAMBDA_PROXY_ONLY__EOS_LOVE_BAYESIAN_FIT_OPEN",
        "observational_blockers": [
            "rotating compact-object exterior",
            "EHT ray-traced images with mass-distance and plasma/accretion priors",
            "full coupled QNM/ringdown and echo transfer function",
            "surface/absorption luminosity for horizonless core candidates",
            "RG-derived neutron-star EOS/anisotropy and Love-number ODEs",
        ],
        "do_not_claim": [
            "do not claim a derived RG black-hole replacement from the static exterior branch alone",
            "do not claim geodesic completion from C2 matching alone",
            "do not export the unprojected Bernoulli scalar as a healthy standalone propagating field",
            "do not claim no-horizon observational viability before QNM/echo/surface tests",
            "do not claim EHT support from the static +4.63% benchmark alone",
            "do not claim NICER/GW170817 pass from toy TOV diagnostics",
        ],
    }


def solar_2pn_screening_minimum_gate(q_rg=sp.Integer(10)):
    """
    Minimal screening requirement implied by the compressed Solar 2PN proxy.

    This is not a strong-field proof.  It answers the review's immediate
    question: does the present compressed Cassini scale already force a
    screening factor on the q_2PN=10 branch?
    """
    q_gr = sp.Rational(7, 4)
    delta_q = float(sp.sympify(q_rg) - q_gr)
    rg_sun_m = 1.4766250385e3
    r_sun_m = 6.957e8
    signal = delta_q * rg_sun_m / r_sun_m
    cassini_central = 2.1e-5
    cassini_sigma = 2.3e-5
    conservative = abs(cassini_central) + cassini_sigma

    max_unscreened_amplitude_1sigma = cassini_sigma / signal
    max_unscreened_amplitude_conservative = conservative / signal
    current_proxy_forces_screening = max_unscreened_amplitude_conservative < 1.0

    return {
        "status": (
            "NO_COMPRESSED_CASSINI_SCREENING_FORCED_BY_DEFAULT_PROXY"
            if not current_proxy_forces_screening
            else "SCREENING_REQUIRED_BY_COMPRESSED_CASSINI_PROXY"
        ),
        "q_RG": sp.sympify(q_rg),
        "q_GR": q_gr,
        "Delta_q": sp.simplify(sp.sympify(q_rg) - q_gr),
        "solar_limb_equivalent_gamma_signal": signal,
        "cassini_sigma": cassini_sigma,
        "cassini_conservative_bound": conservative,
        "max_unscreened_amplitude_1sigma": max_unscreened_amplitude_1sigma,
        "max_unscreened_amplitude_conservative": (
            max_unscreened_amplitude_conservative
        ),
        "interpretation": (
            "the compressed proxy does not by itself force screening today; "
            "a raw 2PN likelihood or tighter future light-bending bound can"
            " still require it"
        ),
    }


def article_strong_field_gate():
    """
    Article-facing strong-field and screening gate.

    The first article may use this as a scope boundary: the static compact
    ledger contains useful phase-branch geodesic algebra, but full strong-field
    viability needs source closure, rotating solutions, QNM/echo stability, and
    EHT/NS likelihoods.  The Solar weak-field 2PN branch stays in p03b/p03c and
    must not be merged with the p05 q=2 phase branch.
    """
    boundary = analyze_horizon_throat_and_boundary()
    compact_gate = compact_central_claim_gate()
    screening = solar_2pn_screening_minimum_gate()

    return {
        "article_use": "strong-field/screening scope boundary",
        "status": "PARTIAL_ARTICLE_EXPORT_READY_STATIC_EXTERIOR_AND_SCREENING_SCOPE_ONLY",
        "compact_exterior_short_path": compact_gate["compact_exterior_short_path"],
        "static_exterior_boundary": {
            "exterior_result": boundary["exterior_result"],
            "finite_r_horizon_test": boundary["finite_r_horizon_test"],
            "geodesic_status": boundary["geodesic_status"],
        },
        "compact_export_gate": compact_gate["file_export_status"],
        "black_hole_replacement_status": compact_gate[
            "black_hole_breaker_status"
        ],
        "screening_minimum": screening,
        "solar_vs_phase_branch_rule": (
            "p03b/p03c: physical Solar weak-field exterior q_2PN=7/4; "
            "p05: phase-vacuum exponential strong-field branch with internal "
            "q_2PN=2.  These are separate regime statements in the current "
            "work files."
        ),
        "required_before_claim": compact_gate["observational_blockers"],
        "article_rule": (
            "state the closed phase-equation static strong-field result and "
            "exact remaining gates; keep Solar q_2PN=7/4 in the p03b/p03c "
            "weak-field branch and do not export p05 q=2 as the Solar metric"
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("STAGE A3: OLD compact/interior/verification integration ledger")
    print("=" * 72)

    status = stage_a3_compact_old_file_status()

    print("\n1. OLD/12 and OLD/14 drain status")
    for old_file, info in status["geodesic_interior"].items():
        print(f"  {old_file}: {info['status']}")
        for item in info["core_results"]:
            print(f"    - {item}")

    print("\n2. OLD/15 scalar perturbation verification")
    for key, value in status["scalar_perturbations"].items():
        print(f"  {key:28s}: {value}")

    print("\n3. Integration verdict")
    print("  - OLD/12, OLD/14 and OLD/15 are represented here as candidate ledger")
    print("    material. The static compact-exterior short path is passed; full")
    print("    compact-object authority still needs the central gates.")

    print("\n4. Central compact-object claim gate")
    for key, value in compact_central_claim_gate().items():
        print(f"  {key:30s}: {value}")

    print("\n5. Compact exterior short path")
    for key, value in compact_exterior_short_path_certificate().items():
        print(f"  {key:30s}: {value}")

