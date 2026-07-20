# Notation header (see NOTATION.md):
# signature (+---); x=r/r_s, beta=b/r_s, tau=c*t/r_s.

"""
PHASE 18d: Static ray baseline and first-order rotating compact rays

This file continues the p05 compact-object chain after p05c.  It separates two
claims:

1. the static exponential exterior gives a closed optical baseline:
       n(x)=exp(1/x), beta(x)=x*exp(1/x), beta_c=e,
       x_ph=1, x_ISCO=phi_golden^2;
2. a first-order stationary spin layer can be ray-traced at the equatorial
   photon-edge level using an asymptotic Lense-Thirring-calibrated cross term.

The spin layer is not a full rotating solution of the RefG action.  It is the
next controlled ray-tracing gate needed before any EHT likelihood statement.
"""

import math

import sympy as sp

from p05_compact import analyze_photon_shadow_isco


def derive_static_exponential_ray_baseline_gate():
    """
    Static optical ray and ISCO ledger for the exponential exterior.

    For the compact phase-vacuum branch,

        B=exp(-1/x), A=exp(1/x), n=sqrt(A/B)=exp(1/x).

    A null ray has local impact function beta(x)=n*x.  The critical shadow edge
    is the minimum of beta(x).  Massive circular orbit stability gives the
    golden-ratio ISCO polynomial.
    """
    x = sp.Symbol("x", positive=True)
    r_s = sp.Symbol("r_s", positive=True, real=True)
    phi_golden = (1 + sp.sqrt(5)) / 2
    p05_static = analyze_photon_shadow_isco()

    B = sp.exp(-1 / x)
    A = sp.exp(1 / x)
    n = sp.sqrt(A / B)
    beta_of_x = sp.simplify(x * n)
    beta_prime = sp.factor(sp.diff(beta_of_x, x))
    beta_second_at_ph = sp.simplify(sp.diff(beta_of_x, x, 2).subs(x, 1))
    beta_c = sp.simplify(beta_of_x.subs(x, 1))

    photon_barrier = sp.simplify(B / (A * x**2))
    photon_barrier_prime = sp.factor(sp.diff(photon_barrier, x))

    ell = sp.Symbol("ell", positive=True)
    v_eff = sp.exp(-1 / x) + ell**2 * sp.exp(-2 / x) / x**2
    ell_circ_sq = sp.simplify(x**2 * sp.exp(1 / x) / (2 * (x - 1)))
    e_circ_sq = sp.simplify(
        sp.exp(-1 / x) + ell_circ_sq * sp.exp(-2 / x) / x**2
    )
    stability_second = sp.factor(
        sp.simplify(sp.diff(v_eff, x, 2).subs(ell**2, ell_circ_sq))
    )
    isco_poly = x**2 - 3 * x + 1
    isco_roots = sp.solve(sp.Eq(isco_poly, 0), x)
    isco_physical = sp.simplify(isco_roots[1])

    shadow_gr = 3 * sp.sqrt(3) / 2
    shadow_ratio = sp.N(beta_c / shadow_gr, 12)
    p05_beta_c = sp.simplify(p05_static["critical_impact_parameter"].rhs / r_s)
    p05_isco = sp.simplify(p05_static["ISCO_physical"].rhs / r_s)

    return {
        "static_ray_baseline_status": (
            "PASS_STATIC_EXPONENTIAL_RAY_BASELINE"
            if sp.simplify(beta_c - sp.E) == 0
            and sp.simplify(isco_physical - phi_golden**2) == 0
            and sp.simplify(p05_beta_c - beta_c) == 0
            and sp.simplify(p05_isco - isco_physical) == 0
            else "CHECK_STATIC_EXPONENTIAL_RAY_BASELINE"
        ),
        "metric_functions": {
            "B": sp.Eq(sp.Symbol("B"), B),
            "A": sp.Eq(sp.Symbol("A"), A),
            "n": sp.Eq(sp.Symbol("n"), n),
        },
        "impact_function": sp.Eq(sp.Symbol("beta(x)"), beta_of_x),
        "impact_derivative": sp.Eq(sp.Symbol("d_beta_dx"), beta_prime),
        "photon_sphere": sp.Eq(sp.Symbol("x_ph"), 1),
        "beta_second_at_photon_sphere": beta_second_at_ph,
        "critical_impact_parameter": sp.Eq(sp.Symbol("beta_c"), beta_c),
        "photon_barrier": sp.Eq(sp.Symbol("U_null"), photon_barrier),
        "photon_barrier_derivative": sp.Eq(
            sp.Symbol("d_U_null_dx"),
            photon_barrier_prime,
        ),
        "timelike_effective_potential": sp.Eq(sp.Symbol("V_eff"), v_eff),
        "specific_L_squared_circular": sp.Eq(sp.Symbol("ell_circ^2"), ell_circ_sq),
        "specific_E_squared_circular": sp.Eq(sp.Symbol("E_circ^2"), e_circ_sq),
        "stability_second_derivative": stability_second,
        "ISCO_polynomial": sp.Eq(isco_poly, 0),
        "ISCO_roots": isco_roots,
        "ISCO_physical": sp.Eq(sp.Symbol("x_ISCO"), isco_physical),
        "golden_ratio_identity": sp.Eq(sp.Symbol("x_ISCO"), phi_golden**2),
        "shadow_ratio_RG_over_GR_static": shadow_ratio,
        "shadow_shift_percent_static": float((shadow_ratio - 1) * 100),
        "reading": (
            "the static optical edge is fixed by the minimum of x*exp(1/x); "
            "the ISCO is fixed by the marginal-stability polynomial, not by a "
            "fit."
        ),
    }


def _beta_of_x_static(x_value: float) -> float:
    return x_value * math.exp(1.0 / x_value)


def _outer_turning_point(beta_value: float) -> float | None:
    if beta_value <= math.e:
        return None

    lo = 1.0
    hi = max(2.0, beta_value + 1.0)
    while _beta_of_x_static(hi) < beta_value:
        hi *= 2.0

    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if _beta_of_x_static(mid) < beta_value:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _static_deflection_angle(beta_value: float, intervals: int = 8000) -> float | None:
    x0 = _outer_turning_point(beta_value)
    if x0 is None:
        return None

    if intervals % 2:
        intervals += 1

    def integrand(t_value: float) -> float:
        if t_value == 0.0:
            beta_prime_x0 = math.exp(1.0 / x0) * (1.0 - 1.0 / x0)
            root_slope = 2.0 * beta_value * beta_prime_x0
            return 2.0 * beta_value / math.sqrt(root_slope * x0)
        if t_value == 1.0:
            return 2.0 * beta_value / x0
        x_value = x0 / (1.0 - t_value**2)
        n_value = math.exp(1.0 / x_value)
        root_argument = max((n_value * x_value) ** 2 - beta_value**2, 0.0)
        root = math.sqrt(root_argument)
        dphi_dx = beta_value / (x_value * root)
        dx_dt = 2.0 * x0 * t_value / (1.0 - t_value**2) ** 2
        return dphi_dx * dx_dt

    h = 1.0 / intervals
    total = integrand(0.0) + integrand(1.0)
    for index in range(1, intervals):
        weight = 4.0 if index % 2 else 2.0
        total += weight * integrand(index * h)
    half_angle = total * h / 3.0
    return 2.0 * half_angle - math.pi


def run_static_ray_tracing_numeric_gate():
    """
    Numerical equatorial ray tracing in the static optical metric.

    beta<e is captured, beta=e is the critical edge, and beta>e has an outer
    turning point.  The deflection integral is evaluated directly from the
    optical metric and gives the weak-bending check at large beta.
    """
    baseline = derive_static_exponential_ray_baseline_gate()
    beta_values = (2.5, math.e, 3.0, 5.0, 10.0, 20.0)
    rows = []

    for beta_value in beta_values:
        x_turn = _outer_turning_point(beta_value)
        deflection = (
            _static_deflection_angle(beta_value, intervals=6000)
            if x_turn is not None
            else None
        )
        rows.append({
            "beta": beta_value,
            "class": (
                "captured"
                if beta_value < math.e
                else "critical"
                if abs(beta_value - math.e) < 1.0e-12
                else "scattered"
            ),
            "outer_turning_x": x_turn,
            "deflection_rad": deflection,
            "weak_leading_2_over_beta": (
                2.0 / beta_value if deflection is not None else None
            ),
            "deflection_over_leading": (
                deflection / (2.0 / beta_value)
                if deflection is not None
                else None
            ),
        })

    scattered = [row for row in rows if row["class"] == "scattered"]
    weak_row = next(row for row in rows if abs(row["beta"] - 20.0) < 1.0e-12)
    turning_ok = all(
        row["outer_turning_x"] is not None and row["outer_turning_x"] > 1.0
        for row in scattered
    )
    capture_ok = rows[0]["outer_turning_x"] is None
    weak_ok = 0.9 < weak_row["deflection_over_leading"] < 1.2

    return {
        "static_ray_tracing_status": (
            "PASS_STATIC_EXPONENTIAL_RAY_TRACING_NUMERIC"
            if baseline["static_ray_baseline_status"]
            == "PASS_STATIC_EXPONENTIAL_RAY_BASELINE"
            and turning_ok
            and capture_ok
            and weak_ok
            else "CHECK_STATIC_EXPONENTIAL_RAY_TRACING_NUMERIC"
        ),
        "beta_critical": math.e,
        "sample_rows": rows,
        "weak_beta20_ratio_to_2_over_beta": weak_row["deflection_over_leading"],
        "reading": (
            "the numerical ray tracer sees the same capture/scatter boundary "
            "as the analytic beta_c=e edge and approaches the expected weak "
            "2/beta bending scale."
        ),
    }


def derive_first_order_rotating_edge_gate():
    """
    First-order equatorial photon-edge split for a slow rotating exterior.

    The dimensionless stationary ansatz is

        ds^2/r_s^2 = -B d tau^2 + A(dx^2+x^2 dOmega^2)
                     + 2 D d tau d phi,

    with B=exp(-1/x), A=exp(1/x), C=A*x^2 and

        D(x) = -j/(2x)

    on the equator.  This D is the asymptotic Lense-Thirring-calibrated cross
    term in the same dimensionless variables.  Solving the circular null edge
    equations F=0 and F_x=0 to first order gives a signed impact-parameter
    pair.  The O(j) effect shifts the shadow center; the diameter changes only
    beyond first order in this gate.
    """
    x, j, sigma, beta_1, x_1 = sp.symbols(
        "x j sigma beta_1 x_1",
        real=True,
    )
    B = sp.exp(-1 / x)
    A = sp.exp(1 / x)
    C = A * x**2
    D = -j / (2 * x)
    beta = sigma * sp.E + j * beta_1
    x_edge = 1 + j * x_1

    F = sp.simplify(C + 2 * beta * D - B * beta**2)
    Fx = sp.diff(F, x)
    F_order_j = sp.expand(sp.series(F.subs(x, x_edge), j, 0, 2).removeO()).coeff(j, 1)
    Fx_order_j = sp.expand(sp.series(Fx.subs(x, x_edge), j, 0, 2).removeO()).coeff(j, 1)
    solution = sp.solve(
        [
            sp.Eq(F_order_j.subs(sigma**2, 1), 0),
            sp.Eq(Fx_order_j.subs(sigma**2, 1), 0),
        ],
        [beta_1, x_1],
        dict=True,
    )[0]
    beta_edge = sp.simplify(beta.subs(solution))
    x_ph_edge = sp.simplify(x_edge.subs(solution))

    beta_plus = sp.simplify(beta_edge.subs(sigma, 1))
    beta_minus = sp.simplify(beta_edge.subs(sigma, -1))
    x_plus = sp.simplify(x_ph_edge.subs(sigma, 1))
    x_minus = sp.simplify(x_ph_edge.subs(sigma, -1))
    center_shift = sp.simplify((beta_plus + beta_minus) / 2)
    diameter = sp.simplify(beta_plus - beta_minus)
    diameter_static = 2 * sp.E
    diameter_change_order_j = sp.simplify(
        sp.diff(diameter / diameter_static, j).subs(j, 0)
    )

    residual_F = sp.simplify(
        sp.series(F.subs({x: x_ph_edge, beta_1: solution[beta_1], x_1: solution[x_1]}), j, 0, 2).removeO()
        .subs(sigma**2, 1)
    )
    residual_Fx = sp.simplify(
        sp.series(Fx.subs({x: x_ph_edge, beta_1: solution[beta_1], x_1: solution[x_1]}), j, 0, 2).removeO()
        .subs(sigma**2, 1)
    )
    residual_on_edges = {
        "F_sigma_plus": sp.simplify(residual_F.subs(sigma, 1)),
        "F_sigma_minus": sp.simplify(residual_F.subs(sigma, -1)),
        "Fx_sigma_plus": sp.simplify(residual_Fx.subs(sigma, 1)),
        "Fx_sigma_minus": sp.simplify(residual_Fx.subs(sigma, -1)),
    }
    residuals_ok = all(value == 0 for value in residual_on_edges.values())

    sample_j = 0.1
    sample_edges = {
        "j": sample_j,
        "beta_plus": float(sp.N(beta_plus.subs(j, sample_j))),
        "beta_minus": float(sp.N(beta_minus.subs(j, sample_j))),
        "abs_beta_plus": abs(float(sp.N(beta_plus.subs(j, sample_j)))),
        "abs_beta_minus": abs(float(sp.N(beta_minus.subs(j, sample_j)))),
        "center_shift": float(sp.N(center_shift.subs(j, sample_j))),
        "diameter": float(sp.N(diameter.subs(j, sample_j))),
        "static_diameter": float(2.0 * math.e),
        "x_plus": float(sp.N(x_plus.subs(j, sample_j))),
        "x_minus": float(sp.N(x_minus.subs(j, sample_j))),
    }

    return {
        "first_order_rotating_edge_status": (
            "PASS_FIRST_ORDER_ROTATING_EQUATORIAL_RAY_EDGE"
            if residuals_ok
            and sp.simplify(diameter_change_order_j) == 0
            else "CHECK_FIRST_ORDER_ROTATING_EQUATORIAL_RAY_EDGE"
        ),
        "stationary_metric_ansatz": (
            "ds^2/r_s^2=-B*d tau^2+A*(dx^2+x^2*dOmega^2)+2D*d tau*dphi"
        ),
        "B": sp.Eq(sp.Symbol("B"), B),
        "A": sp.Eq(sp.Symbol("A"), A),
        "C_equatorial": sp.Eq(sp.Symbol("C"), C),
        "D_equatorial_first_order": sp.Eq(sp.Symbol("D"), D),
        "edge_equations": {
            "F": sp.Eq(sp.Symbol("F"), F),
            "F_x": sp.Eq(sp.Symbol("F_x"), Fx),
        },
        "first_order_solution": {
            "beta_sigma": sp.Eq(sp.Symbol("beta_sigma"), beta_edge),
            "x_ph_sigma": sp.Eq(sp.Symbol("x_ph_sigma"), x_ph_edge),
            "beta_plus": beta_plus,
            "beta_minus": beta_minus,
            "x_plus": x_plus,
            "x_minus": x_minus,
        },
        "shadow_center_shift_order_j": sp.Eq(sp.Symbol("Delta_beta_center"), center_shift),
        "shadow_diameter_order_j": sp.Eq(sp.Symbol("Delta_beta_diameter"), diameter),
        "diameter_fraction_linear_coefficient": diameter_change_order_j,
        "residual_checks_order_j": {
            "F": residual_F,
            "F_x": residual_Fx,
            "physical_edges": residual_on_edges,
        },
        "sample_j_0p1": sample_edges,
        "scope": (
            "first-order equatorial spin edge with an asymptotic frame-dragging "
            "cross term; full rotating RefG exterior, plasma images and "
            "inclined ray tracing remain later gates"
        ),
        "reading": (
            "spin splits the signed photon-edge radii and shifts the shadow "
            "center at first order.  The static diameter benchmark remains the "
            "diameter at O(j); size corrections start beyond this gate."
        ),
    }


def p05d_central_rotating_ray_gate():
    static_baseline = derive_static_exponential_ray_baseline_gate()
    static_rays = run_static_ray_tracing_numeric_gate()
    rotating_edge = derive_first_order_rotating_edge_gate()

    return {
        "p05d_status": (
            "PASS_P05D_STATIC_RAYS_AND_FIRST_ORDER_ROTATION_LAYER"
            if static_baseline["static_ray_baseline_status"]
            == "PASS_STATIC_EXPONENTIAL_RAY_BASELINE"
            and static_rays["static_ray_tracing_status"]
            == "PASS_STATIC_EXPONENTIAL_RAY_TRACING_NUMERIC"
            and rotating_edge["first_order_rotating_edge_status"]
            == "PASS_FIRST_ORDER_ROTATING_EQUATORIAL_RAY_EDGE"
            else "CHECK_P05D_STATIC_RAYS_AND_FIRST_ORDER_ROTATION_LAYER"
        ),
        "static_ray_baseline": static_baseline["static_ray_baseline_status"],
        "static_ray_tracing": static_rays["static_ray_tracing_status"],
        "first_order_rotating_edge": rotating_edge["first_order_rotating_edge_status"],
        "beta_critical_static": static_rays["beta_critical"],
        "shadow_shift_percent_static": static_baseline["shadow_shift_percent_static"],
        "spin_sample_j_0p1": rotating_edge["sample_j_0p1"],
        "next_gates": [
            "derive the rotating RefG exterior from the action/source equations",
            (
                "p05e_inclined_image_rays.py extends the first-order compact "
                "edge to inclined image-plane curves"
            ),
            "add plasma/emission model before any EHT likelihood claim",
        ],
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18d: Static rays and first-order rotating compact edge")
    print("=" * 72)

    sections = [
        ("1. Static exponential ray baseline", derive_static_exponential_ray_baseline_gate()),
        ("2. Static ray-tracing numeric gate", run_static_ray_tracing_numeric_gate()),
        ("3. First-order rotating edge", derive_first_order_rotating_edge_gate()),
        ("4. Central p05d gate", p05d_central_rotating_ray_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:38s}: {value}")
