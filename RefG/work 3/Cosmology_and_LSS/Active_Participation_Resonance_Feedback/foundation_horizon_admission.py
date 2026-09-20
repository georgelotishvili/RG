"""Direct horizon admission of the existing common-pressure scalar candidate.

Exact null-cone/area identities plus an analytical conditional escape theorem.
No Einstein equations, new evolution, imposed pressure profile, or new flow law.
See FOUNDATION_HORIZON_ADMISSION_V1 in foundation_oscillon_minimum_closure.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import sympy as s

HERE = Path(__file__).resolve().parent
CLAIM = "FOUNDATION_HORIZON_ADMISSION_V1"
ACTION = HERE / "foundation_rate_limited_dynamics.py"
ACTION_HASH = "93447a6a656535846f95e762dbe726a06218b0f4b004724d6cf1288f9a3122b6"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    checks = {}

    def exact(name, expression):
        residual = s.simplify(expression)
        checks[name] = {"passed": residual == 0, "residual": str(residual)}

    t, r = s.symbols("t r", positive=True)
    p = s.Function("p")(t, r)
    pt, pr = s.diff(p, t), s.diff(p, r)
    R = r/p
    metric = s.diag(-p*p, p**-2)
    outgoing = s.Matrix([1/p, p])
    ingoing = s.Matrix([1/p, -p])
    exact("outgoing_null", (outgoing.T*metric*outgoing)[0])
    exact("ingoing_null", (ingoing.T*metric*ingoing)[0])
    exact("future_null_normalization", (outgoing.T*metric*ingoing)[0]+2)
    exact("outgoing_coordinate_speed", outgoing[1]/outgoing[0]-p*p)
    exact("ingoing_coordinate_speed", ingoing[1]/ingoing[0]+p*p)
    dR = s.Matrix([s.diff(R, t), s.diff(R, r)])
    theta_plus = s.simplify(2*(outgoing.T*dR)[0]/R)
    theta_minus = s.simplify(2*(ingoing.T*dR)[0]/R)
    plus_expected = -2*pt/p**2+2*p/r-2*pr
    minus_expected = -2*pt/p**2-2*p/r+2*pr
    exact("outgoing_area_expansion", theta_plus-plus_expected)
    exact("ingoing_area_expansion", theta_minus-minus_expected)
    exact("expansion_sum", theta_plus+theta_minus+4*pt/p**2)
    area_norm = s.simplify((dR.T*metric.inv()*dR)[0])
    exact("independent_area_gradient_norm",
          area_norm-((1-r*pr/p)**2-r*r*pt*pt/p**6))
    exact("area_norm_from_two_expansions", area_norm+R*R*theta_plus*theta_minus/4)
    exact("static_area_gradient_square",
          area_norm.subs(pt, 0)-(1-r*pr/p)**2)

    P, rate = s.symbols("P rate", positive=True)
    falling_sum = (theta_plus+theta_minus).subs({pt: -rate, p: P}, simultaneous=True)
    checks["falling_fixed_coordinate_pressure_cannot_future_trap"] = {
        "passed": s.simplify(falling_sum).is_positive is True,
        "positive_sum": str(s.simplify(falling_sum)),
        "scope": "p_t<0 at fixed preferred r, not the material derivative along an infalling body"}
    u_t, u_r = s.symbols("u_t u_r", real=True)
    plus_u = plus_expected.subs({pt: -P*u_t, pr: -P*u_r, p: P}, simultaneous=True)
    minus_u = minus_expected.subs({pt: -P*u_t, pr: -P*u_r, p: P}, simultaneous=True)
    exact("future_trapping_velocity_identity_plus", plus_u-2*(u_t/P+P*(1/r+u_r)))
    exact("future_trapping_velocity_identity_minus", minus_u-2*(u_t/P-P*(1/r+u_r)))

    # Static exterior diagnostic: r is isotropic, not areal radius.
    m = s.symbols("m", positive=True)
    p_ext = s.exp(-m/r)
    optical_potential = p_ext**4/r**2
    exact("static_photon_orbit_at_2m", s.diff(optical_potential, r).subs(r, 2*m))
    checks["static_photon_orbit_is_unstable_maximum"] = {
        "passed": s.simplify(s.diff(optical_potential, r, 2).subs(r, 2*m)).is_negative is True,
        "second_derivative": str(s.simplify(s.diff(optical_potential, r, 2).subs(r, 2*m)))}
    exact("photon_orbit_still_has_outgoing_radial_light",
          (p_ext**2).subs(r, 2*m)-s.exp(-1))
    exact("static_areal_minimum_at_m", s.diff(r/p_ext, r).subs(r, m))
    exact("areal_minimum_not_Killing_horizon", (-p_ext**2).subs(r, m)+s.exp(-2))

    # The global conclusion is proved by the displayed Cauchy--Schwarz
    # argument, not by an identity count or a numerical sampling interval.
    alpha, E, x, r0, t0 = s.symbols("alpha E x r0 t0", positive=True)
    q = s.symbols("q", nonnegative=True)
    V = q/2-q*q/4+q**3/24
    exact("positive_matter_potential", V-q*((q-3)**2+3)/24)
    exact("radial_Cauchy_Schwarz_weight", s.integrate(x**-2, (x, r, s.oo))-1/r)
    C = s.sqrt(alpha*E/(2*s.pi))
    lower_speed = s.exp(-2*C/s.sqrt(r))
    checks["speed_bound_increases_with_radius"] = {
        "passed": s.diff(lower_speed, r).is_positive is True,
        "derivative": str(s.diff(lower_speed, r))}
    checks["strict_positive_fixed_radius_speed_bound"] = {
        "passed": lower_speed.subs(r, r0).is_positive is True,
        "bound": str(lower_speed.subs(r, r0))}
    lower_ray = r0+lower_speed.subs(r, r0)*(t-t0)
    exact("outgoing_comparison_velocity", s.diff(lower_ray, t)-lower_speed.subs(r, r0))
    checks["outgoing_ray_lower_radius_unbounded"] = {
        "passed": s.limit(lower_ray, t, s.oo) == s.oo,
        "limit": str(s.limit(lower_ray, t, s.oo))}
    exact("uniform_asymptotic_lower_p", s.limit(s.exp(-C/s.sqrt(r)), r, s.oo)-1)
    exact("uniform_asymptotic_upper_p", s.limit(s.exp(C/s.sqrt(r)), r, s.oo)-1)
    checks["areal_radius_lower_bound_unbounded"] = {
        "passed": s.limit(r*s.exp(-C/s.sqrt(r)), r, s.oo) == s.oo}

    # Necessary assumptions control, not a proposed RefG solution:
    # positive p alone does not imply infinite future coordinate range.
    b = s.symbols("b", positive=True)
    p_control = 1/(1+b*t)
    exact("positive_pressure_only_control_finite_coordinate_range",
          s.integrate(p_control**2, (t, 0, s.oo))-1/b)

    # Smallest kinematic flow generalization preserving local p/p^2 units.
    w = s.symbols("w", real=True)
    flow_metric = s.Matrix([[-P**2+w*w/P**2, -w/P**2], [-w/P**2, 1/P**2]])
    exact("flow_metric_regular_determinant", flow_metric.det()+1)
    for label, speed in (("outgoing", w+P**2), ("ingoing", w-P**2)):
        direction = s.Matrix([1, speed])
        exact("flow_"+label+"_null", (direction.T*flow_metric*direction)[0])
    exact("comoving_clock_preserved",
          (s.Matrix([1, w]).T*flow_metric*s.Matrix([1, w]))[0]+P*P)
    exact("inward_horizon_outgoing_speed", (w+P*P).subs(w, -P*P))
    exact("inward_horizon_ingoing_speed", (w-P*P).subs(w, -P*P)+2*P*P)
    exact("stationary_flow_surface_is_null",
          flow_metric.inv()[1, 1].subs(w, -P*P))

    # Diagnostic only: merely replace derivatives by D_t and vary w.
    # Allow a stationary radial phase; do not assume it is zero.
    f, fp, ur, k, omega = s.symbols("f fp ur k omega", real=True)
    Om = omega+w*k
    gamma = 1/s.sqrt(1-w*w*ur*ur/(b*b*P*P))
    stationary_L = (b*b/(alpha*P*P)*(1-1/gamma)-ur*ur/(2*alpha)
                    +((w*fp)**2+f*f*Om*Om)/(2*P**4)
                    -(fp*fp+f*f*k*k)/2-V/P**2)
    shift_constraint = s.diff(stationary_L, w)
    radial_current = s.diff(stationary_L, k)
    expected_constraint = (w*(gamma*ur*ur/alpha+fp*fp)+Om*f*f*k)/P**4
    expected_current = f*f*(w*Om/P**4-k)
    exact("minimal_flow_variation", shift_constraint-expected_constraint)
    exact("radial_phase_current", radial_current-expected_current)
    exact("stationary_flow_positive_sum",
          shift_constraint+Om*radial_current/P**4
          -w/P**4*(gamma*ur*ur/alpha+fp*fp+f*f*Om*Om/P**4))
    G = s.symbols("gamma", positive=True)
    bracket = G*ur*ur/alpha+fp*fp+f*f*Om*Om/P**4
    checks["stationary_flow_bracket_nonnegative"] = {
        "passed": bracket.is_nonnegative is True,
        "bracket": str(bracket),
        "strict_condition": "at least one of ur, fp, f*Om is nonzero"}

    passed = all(item["passed"] for item in checks.values())
    return {
        "claim_id": CLAIM,
        "status": "PASS_SCOPED_IDENTITIES_AND_ADMISSION_AUDIT" if passed else "FAIL",
        "decision": ("REGULAR_FINITE_ENERGY_SPHERICAL_DIAGONAL_CANDIDATE_HAS_OUTWARD_ESCAPE"
                     if passed else "AUDIT_FAILED_DO_NOT_USE_CONCLUSION"),
        "checks": checks,
        "formulae": {
            "areal_radius": "R=r/p",
            "radial_light": "dr/dt=+/-p^2",
            "theta_plus": str(theta_plus), "theta_minus": str(theta_minus),
            "future_trapped_condition": "u_t < -p^2*abs(1/r+u_r)",
            "positive_energy_bound": "E >= (2*pi/alpha)*integral_0^infinity r^2*u_r^2 dr",
            "uniform_pressure_bounds": "exp(-sqrt(alpha*Emax/(2*pi*r))) <= p(t,r) <= exp(+sqrt(alpha*Emax/(2*pi*r)))",
            "outgoing_radius_bound": "r(t)>=r0+exp(-2*sqrt(alpha*Emax/(2*pi*r0)))*(t-t0)",
            "finite_detector_time_bound": "Delta_t <= (r_detector-r0)*exp(2*sqrt(alpha*Emax/(2*pi*r0)))",
            "kinematic_flow_light": "dr/dt=w+/-p^2",
        },
        "escape_theorem_assumptions": [
            "Spherical symmetry; global preferred diagonal chart for all future t and 0<=r<infinity.",
            "Smooth positive p and regular centre; u=-log(p), u(t,infinity)=0.",
            "Uniform finite upper bound on the full nonnegative canonical energy.",
            "The gradient term remains |grad u|^2/(2 alpha), alpha>0.",
            "Interpretation as absence of an event horizon additionally assumes the usual complete asymptotically flat future exterior.",
        ],
        "analytical_proof": [
            "For every r>0, u(r)=-integral_r^infinity u_x dx.",
            "Cauchy--Schwarz gives |u(r)|^2 <= (integral_r^infinity x^2*u_x^2 dx)/r <= alpha*Emax/(2*pi*r).",
            "Every future outgoing radial null curve has dr/dt=p^2>0, hence r>=r0>0.",
            "The energy bound then gives the uniform speed floor p^2>=exp(-2*sqrt(alpha*Emax/(2*pi*r0))).",
            "Every finite exterior detector radius is reached in finite coordinate time; R=r/p grows unboundedly with r.",
            "At a smooth positive-pressure centre, local continuity first lets a ray reach some r0>0.",
            "Thus a globally regular isolated member of this class cannot permanently trap light behind a finite-radius black-hole boundary.",
        ],
        "minimal_flow_admission": {
            "metric": "ds^2=-p^2 dt^2+p^-2[(dr-w dt)^2+r^2 dOmega^2]",
            "kinematic_horizon": "In a stationary metric, a fixed-radius surface w=-p^2 at p>0 is null and chart-regular; R_r>0 gives the usual outgoing/ingoing orientation. Its event-horizon status still requires the global solution.",
            "time_dependent_caveat": "An instantaneous w+p^2=0 is only zero outgoing coordinate velocity, not a proof of an event horizon.",
            "coordinate_caveat": "A coordinate rewriting of the same solution does not create an event horizon.",
            "tested_completion": "Only substitute D_t=partial_t+w*partial_r in the old action and vary w; no new w derivative energy.",
            "stationary_zero_flux_result": "J^r=0 and delta L/delta w=0 imply w[gamma*u_r^2/alpha+f_r^2+f^2*(omega+w*chi_r)^2/p^4]=0.",
            "conclusion": "This minimal stationary regular-centre completion forces w=0 wherever the bracket is positive.",
            "degenerate_sector": "All-zero bracket leaves w undetermined, not a physically sourced horizon.",
            "scope": "Stationary localized complex matter, allowing radial phase; zero steady charge flux at a regular centre; real rate-limited branch.",
            "time_dependent_flow_completion": "OPEN; no new dynamical flow law is supplied by these checks.",
        },
        "verified_flags": {
            "null_and_area_identities": passed,
            "conditional_outward_escape": passed,
            "static_photon_orbit_distinguished": passed,
            "minimal_stationary_flow_obstruction": passed,
        },
        "closure_flags": {key: False for key in (
            "global_PDE_existence", "all_RefG_geometries_excluded",
            "dynamic_flow_action_derived", "regular_black_hole_constructed",
            "singularity_resolution", "observational_pass")},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    ledger = HERE / "foundation_oscillon_minimum_closure.md"
    if CLAIM not in ledger.read_text(encoding="utf-8-sig"):
        raise ValueError("Admission contract missing")
    if digest(ACTION) != ACTION_HASH:
        raise ValueError("Inherited action changed")
    result = check()
    result["provenance"] = {"action_sha256": digest(ACTION),
                             "self_sha256": digest(Path(__file__)),
                             "ledger_sha256_at_run": digest(ledger),
                             "sympy": s.__version__}
    encoded = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        destination = args.output.resolve()
        if destination.parent != HERE:
            raise ValueError("Output must stay in this working package")
        destination.write_text(encoded+"\n", encoding="utf-8")
    print(encoded)
    if result["status"] == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
