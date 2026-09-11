"""Exact inverse saturation candidate; no project reads or file writes.

See inverse_saturation_candidate.md for postulates, attribution and domain.
This verifies a conditional geometry, not a completed RefG material action.
"""

import argparse
import json
from functools import lru_cache

import mpmath as mp
import sympy as s


def run_checks():
    checks = []

    def exact(name, value, target=0):
        residual = s.factor(s.cancel(s.trigsimp(value-target)))
        checks.append(dict(name=name, kind="exact", passed=residual == 0,
                           residual=str(residual)))

    def gate(name, value, kind="inequality"):
        checks.append(dict(name=name, kind=kind, passed=bool(value)))

    r, M, ell = s.symbols("r M ell", positive=True)
    y, z = s.symbols("y z", positive=True)
    feedback = z-y*(1-ell**2*z)
    response = s.solve(feedback, z)[0]
    exact("postulated_feedback_solution", feedback.subs(z, response))
    exact("response_slope", s.diff(response, y), 1/(1+ell**2*y)**2)
    exact("finite_response_threshold", s.limit(response, y, s.oo), ell**-2)
    den = r**3+2*M*ell**2
    z_r = response.subs(y, 2*M/r**3)
    q = 1-ell**2*z_r
    mass = r**3*z_r/2
    f = s.factor(1-r**2*z_r)
    exact("mass_response_fraction", mass, M*q)
    exact("positive_fraction_formula", q, r**3/den)
    exact("mass_marginal_response", s.diff(mass, M), q**2)
    exact("mass_response_concavity", s.diff(mass, M, 2),
          -4*ell**2*r**6/den**3)
    exact("fixed_radius_mass_cap", s.limit(mass, M, s.oo), r**3/(2*ell**2))
    exact("finite_ADM_mass", s.limit(mass, r, s.oo), M)
    gate("positive_denominator_and_fraction",
         den.is_positive and (r**3/den).is_positive
         and (2*M*ell**2/den).is_positive)
    exact("Hayward_target_recovered", f, 1-2*M*r**2/den)
    exact("Einstein_control", s.limit(f, ell, 0), 1-2*M/r)
    exact("leading_far_field_correction",
          s.limit(r**4*(f-1+2*M/r), r, s.oo), 4*M**2*ell**2)

    # Exponential attenuation is a real rejected candidate, not a relabeling
    # of the original RefG operational exponential clock factor.
    x = s.symbols("x", positive=True)
    exponential_y = x*s.exp(x)/ell**2
    exact("exponential_implicit_feedback",
          x/ell**2-exponential_y*s.exp(-x))
    gate("exponential_inverse_load_unbounded",
         s.limit(exponential_y, x, s.oo) == s.oo)
    # x=W(2M ell^2/r^3), so r*x'=-3x/(1+x).
    exponential_slope = -2*x+3*x/(1+x)
    exponential_second = exponential_slope-3*x*s.diff(exponential_slope, x)/(1+x)
    exponential_K = (exponential_second**2+4*exponential_slope**2+4*x**2)/ell**4
    exact("exponential_control_curvature_growth",
          s.limit(exponential_K/x**2, x, s.oo), 24/ell**4)
    gate("exponential_control_is_singular",
         s.limit(exponential_K, x, s.oo) == s.oo, "rejected_candidate")
    reverse = s.solve(z-y*(1+ell**2*z), z)[0]
    exact("reverse_feedback_has_positive_load_pole",
          s.limit((y-ell**-2)*reverse, y, ell**-2), -ell**-4)

    # Independent lapse variation in the known reduced spherical action.
    F = s.Function("f")(r)
    N = s.Function("N")(r)
    H = s.Function("H")
    psi = (1-F)/r**2
    lagrangian = N*s.diff(r**3*H(psi), r)/12
    lapse_eq = s.diff(lagrangian, N)
    metric_eq = (s.diff(lagrangian, F)
                 -s.diff(s.diff(lagrangian, s.diff(F, r)), r))
    hz = s.diff(H(z), z).subs(z, psi)
    exact("independent_lapse_variation", lapse_eq, s.diff(r**3*H(psi), r)/12)
    exact("independent_radial_metric_variation", metric_eq, r*s.diff(N, r)*hz/12)
    H_candidate = 6*z/(1-ell**2*z)
    exact("candidate_radial_first_integral",
          r**3*H_candidate.subs(z, z_r), 12*M)
    exact("response_action_Einstein_normalization",
          s.diff(H_candidate, z).subs(z, 0), 6)

    # Direct geometry in the ingoing horizon-regular chart, before inserting f.
    vv, th, ph = s.symbols("v theta phi", real=True)
    coords = (vv, r, th, ph)
    ff = s.Function("F")(vv, r)
    metric = s.Matrix([[-ff, 1, 0, 0], [1, 0, 0, 0],
                       [0, 0, r**2, 0], [0, 0, 0, r**2*s.sin(th)**2]])
    inverse = metric.inv()

    @lru_cache(None)
    def connection(a, b, c):
        return s.simplify(sum(inverse[a, d] * (
            s.diff(metric[d, c], coords[b])+s.diff(metric[d, b], coords[c])
            -s.diff(metric[b, c], coords[d])) for d in range(4))/2)

    @lru_cache(None)
    def riemann_up(a, b, c, d):
        return s.simplify(
            s.diff(connection(a, d, b), coords[c])
            -s.diff(connection(a, c, b), coords[d])
            +sum(connection(a, c, e)*connection(e, d, b)
                 -connection(a, d, e)*connection(e, c, b) for e in range(4)))

    def riemann(a, b, c, d):
        return s.simplify(sum(metric[a, e]*riemann_up(e, b, c, d)
                              for e in range(4)))

    ricci = s.Matrix(4, 4, lambda b, d: s.simplify(
        sum(riemann_up(a, b, a, d) for a in range(4))))
    scalar_R = s.simplify(s.trace(inverse*ricci))
    mixed_G = s.simplify(inverse*(ricci-metric*scalar_R/2))
    fr, frr, fv = s.diff(ff, r), s.diff(ff, r, 2), s.diff(ff, vv)
    exact("ingoing_radial_determinant", metric[:2, :2].det(), -1)
    exact("direct_G_v_v", mixed_G[0, 0], (r*fr+ff-1)/r**2)
    exact("direct_G_r_r", mixed_G[1, 1], mixed_G[0, 0])
    exact("direct_G_r_v", mixed_G[1, 0], -fv/r)
    exact("direct_G_theta_theta", mixed_G[2, 2], frr/2+fr/r)
    exact("direct_G_phi_phi", mixed_G[3, 3], mixed_G[2, 2])
    exact("direct_Ricci_scalar", scalar_R, -frr-4*fr/r+2*(1-ff)/r**2)
    Rvrvr = riemann(0, 1, 0, 1)
    Rvtvt = riemann(0, 2, 0, 2)
    Rvtrt = riemann(0, 2, 1, 2)
    Rrtrt = riemann(1, 2, 1, 2)
    Rtptp = riemann(2, 3, 2, 3)
    exact("direct_radial_Riemann", Rvrvr, frr/2)
    exact("direct_time_angular_Riemann", Rvtvt, r*(ff*fr-fv)/2)
    exact("direct_mixed_angular_Riemann", Rvtrt, -r*fr/2)
    exact("direct_radial_angular_Riemann", Rrtrt)
    exact("direct_sphere_Riemann", Rtptp, r**2*(1-ff)*s.sin(th)**2)

    def substitute_static(expr):
        return s.simplify(expr.subs(ff, f).doit())

    rho = -substitute_static(mixed_G[0, 0])/(8*s.pi)
    pr = substitute_static(mixed_G[1, 1])/(8*s.pi)
    pt = substitute_static(mixed_G[2, 2])/(8*s.pi)
    cap = 3/(8*s.pi*ell**2)
    exact("source_density_mass_derivative", rho, s.diff(mass, r)/(4*s.pi*r**2))
    exact("source_density_response_fraction", rho, cap*(1-q)**2)
    exact("required_radial_pressure", pr, -rho)
    exact("required_tangential_pressure", pt, (3*q-1)*rho)
    exact("source_conservation",
          s.diff(pr, r)+(rho+pr)*s.diff(f, r)/(2*f)+2*(pr-pt)/r)
    exact("radial_null_source", rho+pr)
    exact("tangential_null_source", rho+pt, 3*q*rho)
    gate("positive_density", s.factor(rho).is_positive)
    exact("central_density_limit", s.limit(rho, r, 0), cap)
    exact("central_pressure_limit", s.limit(pt, r, 0), -cap)
    gate("dropping_pressure_fails_radial_Einstein_equation",
         substitute_static(mixed_G[1, 1]).subs({r: 1, M: 2, ell: 1}) != 0,
         "rejected_source")
    # DEC is not a material-health certificate for this effective tensor.
    qq = s.symbols("q", nonnegative=True)
    exact("tangential_DEC_boundary", ((3*qq-1)-1).subs(qq, s.Rational(2, 3)))
    gate("tangential_DEC_violation_control", (3*s.Rational(3, 4)-1)>1,
         "scope_boundary")

    # The four static orthonormal components, directly from the EF Riemann.
    AA = substitute_static(Rvrvr)
    BB = substitute_static(Rvtvt/ff/r**2)
    CC = substitute_static((Rvtvt/ff+2*Rvtrt+ff*Rrtrt)/r**2)
    DD = substitute_static(Rtptp/(r**4*s.sin(th)**2))
    K = s.factor(4*(AA**2+2*BB**2+2*CC**2+DD**2))
    exact("independent_static_Kretschmann",
          K, s.diff(f, r, 2)**2+4*(s.diff(f, r)/r)**2+4*((1-f)/r**2)**2)
    exact("central_Ricci", s.limit(substitute_static(scalar_R), r, 0), 12/ell**2)
    exact("central_Kretschmann", s.limit(K, r, 0), 24/ell**4)
    exact("curvature_component_polynomial",
          s.diff(f, r, 2), (1-q)*(18*q*(1-q)-2)/ell**2)
    exact("angular_component_polynomial",
          s.diff(f, r)/r, (1-q)*(3*q-2)/ell**2)
    # For 0<=q<=1: q(1-q)<=1/4, hence |f''|<=5/(2ell²),
    # |f'/r|<=2/ell², |(1-f)/r²|<=1/ell².
    exact("quarter_bound_certificate",
          s.Rational(1, 4)-qq*(1-qq), (qq-s.Rational(1, 2))**2)
    exact("global_sufficient_K_bound",
          (s.Rational(5, 2))**2+4*2**2+4, s.Rational(105, 4))

    # Analytic horizon count; numerical roots only illustrate the accepted branch.
    poly = r**3-2*M*r**2+2*M*ell**2
    critical = 3*s.sqrt(3)*ell/4
    exact("horizon_numerator", f*den, poly)
    exact("positive_horizon_minimum_location",
          s.diff(poly, r).subs(r, 4*M/3))
    exact("horizon_minimum_value", poly.subs(r, 4*M/3),
          2*M*(ell**2-16*M**2/27))
    exact("extremal_mass_and_radius",
          poly.subs({M: critical, r: s.sqrt(3)*ell}))
    exact("extremal_double_root",
          s.diff(poly, r).subs({M: critical, r: s.sqrt(3)*ell}))

    # Radial freely falling orthonormal frame across either simple horizon.
    E, w = s.symbols("E w", positive=True)
    f0, f1, f2 = s.symbols("f f_prime f_second", real=True)
    lapse_inverse = 1/(E+w)
    ur, nr = s.Matrix([lapse_inverse, -w]), s.Matrix([lapse_inverse, E])
    radial_metric = s.Matrix([[-f0, 1], [1, 0]])
    on_shell = {f0: E**2-w**2}
    exact("infall_frame_unit_time", (ur.T*radial_metric*ur)[0].subs(on_shell), -1)
    exact("infall_frame_unit_space", (nr.T*radial_metric*nr)[0].subs(on_shell), 1)
    exact("infall_frame_orthogonality", (ur.T*radial_metric*nr)[0].subs(on_shell))
    radial_tidal = f2/2*(ur[0]*nr[1]-ur[1]*nr[0])**2
    angular_tidal = (r*f0*f1/2*ur[0]**2-r*f1*ur[0]*ur[1])/r**2
    exact("radial_freely_falling_tide", radial_tidal, f2/2)
    exact("angular_freely_falling_tide", angular_tidal.subs(on_shell), f1/(2*r))
    exact("horizon_frame_is_finite", lapse_inverse.subs(w, E), 1/(2*E))
    exact("central_radial_tide", s.limit(s.diff(f, r, 2)/2, r, 0), -ell**-2)
    exact("central_angular_tide", s.limit(s.diff(f, r)/(2*r), r, 0), -ell**-2)
    exact("radial_acceleration", -s.diff(f, r)/2, M*r*(4*M*ell**2-r**3)/den**2)
    exact("clock_fraction_cannot_be_source_fraction", s.limit(f-q**2, r, 0), 1)

    # Marginal E=1 timelike geodesic: exact proper time and independent quadrature.
    speed = r*s.sqrt(2*M/den)
    exact("marginal_geodesic_first_integral", speed**2, 1-f)
    exact("marginal_exponential_endpoint_rate", s.limit(speed/r, r, 0), 1/ell)
    primitive = (2*s.sqrt(den)/(3*s.sqrt(2*M))
                 +ell*s.log((s.sqrt(den)-s.sqrt(2*M*ell**2))
                            /(s.sqrt(den)+s.sqrt(2*M*ell**2)))/3)
    exact("proper_time_primitive", s.diff(primitive, r), 1/speed)
    exact("logarithmic_proper_time_divergence",
          s.limit(r*s.diff(primitive, r), r, 0), ell)
    exact("general_timelike_central_speed_squared", s.limit(E**2-f, r, 0), E**2-1)

    # Smooth positive-mass ingoing loading: independently obtained G^r_v.
    Mf = s.Function("M")(vv)
    dynamic_mass = Mf*r**3/(r**3+2*Mf*ell**2)
    dynamic_f = 1-2*dynamic_mass/r
    dynamic_flux = s.simplify(mixed_G[1, 0].subs(ff, dynamic_f).doit()/(8*s.pi))
    exact("loading_flux_from_Einstein",
          dynamic_flux, s.diff(dynamic_mass, vv)/(4*s.pi*r**2))
    exact("loading_flux_suppression",
          dynamic_flux, s.diff(Mf, vv)*r**4/(4*s.pi*(r**3+2*Mf*ell**2)**2))
    mdot = s.symbols("M_dot", real=True)
    frozen_flux = dynamic_flux.subs({s.diff(Mf, vv): mdot, Mf: M})
    exact("loading_flux_central_limit", s.limit(frozen_flux, r, 0))
    exact("loading_flux_central_order",
          s.limit(frozen_flux/r**4, r, 0), mdot/(16*s.pi*M**2*ell**4))

    samples = []
    with mp.workdps(50):
        ff_num = s.lambdify(r, f.subs({M: 2, ell: 1}), "mpmath")
        roots = [mp.findroot(ff_num, interval)
                 for interval in [(mp.mpf("1.1"), mp.mpf("1.4")),
                                  (mp.mpf("3.5"), mp.mpf("4.1"))]]
        for i, root in enumerate(roots):
            gate("horizon_root_"+str(i), abs(ff_num(root)) < mp.mpf("1e-35"), "numeric")
        gate("two_horizon_trapped_region", ff_num((roots[0]+roots[1])/2) < 0)
        I = s.lambdify(r, primitive.subs({M: 2, ell: 1}), "mpmath")
        integrand = s.lambdify(r, (1/speed).subs({M: 2, ell: 1}), "mpmath")
        for endpoint in ("0.5", "0.05", "0.005"):
            rr = mp.mpf(endpoint)
            analytic = I(mp.mpf(8))-I(rr)
            numeric = mp.quad(integrand, [rr, 1, 4, 8])
            residual = abs(analytic-numeric)
            gate("proper_time_quadrature_"+endpoint,
                 residual < mp.mpf("1e-35"), "numeric_crosscheck")
            samples.append(dict(radius=endpoint, elapsed_proper_time=mp.nstr(analytic, 22),
                                quadrature_residual=mp.nstr(residual, 5)))
        root_report = [mp.nstr(root, 22) for root in roots]
    failed = [check for check in checks if not check["passed"]]
    return dict(
        decision="CONDITIONAL_REGULAR_GEOMETRY" if not failed else "CHECK_FAILURE",
        checks=len(checks), passed=len(checks)-len(failed), failed=failed,
        versions=dict(sympy=s.__version__, mpmath=mp.__version__),
        example=dict(M=2, ell=1, horizon_radii=root_report,
                     marginal_infall=samples),
        scope=dict(
            finite_threshold_postulate=True,
            geometry_is_known_Hayward_benchmark=True,
            postulated_feedback_verified=not failed,
            centre_curvature_regular=not failed,
            radial_freely_falling_tides_regular=not failed,
            marginal_infall_centre_at_infinite_proper_time=not failed,
            smooth_positive_mass_loading_flux_verified=not failed,
            source_fraction_is_clock_factor=False,
            full_RefG_action_derivation=False,
            ADM_mass_vs_oscillon_count_derived=False,
            full_four_dimensional_health=False,
            global_geodesic_completeness=False,
            generic_inner_horizon_stability=False,
            formation_from_oscillons=False,
            observational_pass=False),
        details=checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    result = run_checks()
    if not args.verbose:
        result.pop("details")
    print(json.dumps(result, indent=2, allow_nan=False))
    return int(bool(result["failed"]))


if __name__ == "__main__":
    raise SystemExit(main())
