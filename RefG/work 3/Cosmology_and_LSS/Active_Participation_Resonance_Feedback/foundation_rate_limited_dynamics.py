"""New rate-limited foundation/oscillon candidate, not inherited EH gravity.

Contract: FOUNDATION_RATE_LIMITED_DYNAMICS_V1 in the adjacent working ledger.
An explicit proper-time constitutive rate b is postulated, not fitted.
Exact action/energy/causality checks and a homogeneous-cell evolution.
No strong-field collapse, curvature bound or global PDE regularity claim.
Stdout only. Run with python -X utf8 -B; --symbolic-only skips the ODE tests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

sys.dont_write_bytecode = True
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

HERE = Path(__file__).resolve().parent
CLAIM = "FOUNDATION_RATE_LIMITED_DYNAMICS_V1"
LEDGER = HERE / "foundation_oscillon_minimum_closure.md"
PINS = {
    "static_scalar_candidate": (
        HERE / "common_scale_finite_source_candidate.py",
        "6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8"),
    "profile_relaxed_response": (
        HERE / "profile_relaxed_response.py",
        "7d8059fb2123778f890c1e679f374820c9f9010e54ec4d34a1e5efc10458a7ba"),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def symbolic_checks():
    checks, controls = {}, {}

    def exact(name, expression):
        residual = s.simplify(expression)
        checks[name] = {"passed": residual == 0, "residual": str(residual)}

    p, b, alpha = s.symbols("p b alpha", positive=True)
    w, wtt, lap, source = s.symbols("u_t u_tt lap_u S_m", real=True)
    gam = 1/s.sqrt(1-w**2/(b*p)**2)
    kinetic = b*b/(alpha*p*p)*(1-1/gam)
    du = lambda expression: -p*s.diff(expression, p)
    momentum = s.diff(kinetic, w)
    exact("canonical_momentum", momentum-p**-4*gam*w/alpha)
    hkin = w*momentum-kinetic
    exact("Legendre_energy", hkin-b*b/(alpha*p*p)*(gam-1))
    exact("velocity_Hessian", s.diff(momentum, w)-p**-4*gam**3/alpha)
    EL = s.diff(momentum, w)*wtt+du(momentum)*w-lap/alpha-du(kinetic)-source
    expected_EL = (p**-4*gam**3*wtt-lap
                   +b*b*p**-2*(gam**3+gam-2))/alpha-source
    exact("complete_foundation_equation", EL-expected_EL)
    exact("static_temporal_energy_zero", kinetic.subs(w, 0))
    exact("static_extra_force_zero", du(kinetic).subs(w, 0))
    exact("static_quadratic_operator_preserved",
          s.diff(kinetic, w, 2).subs(w, 0)-p**-4/alpha)
    expansion = s.series(kinetic, w, 0, 6).removeO()
    exact("slow_rate_expansion",
          expansion-w*w/(2*alpha*p**4)-w**4/(8*alpha*b*b*p**6))
    scale = s.symbols("scale", positive=True)
    exact("exact_constant_operational_scaling",
          kinetic.subs({p: scale*p, w: scale*w}, simultaneous=True)-kinetic/scale**2)
    exact("proper_rate_scaling_invariant",
          (w/(b*p)).subs({p: scale*p, w: scale*w}, simultaneous=True)-w/(b*p))

    z, pi = s.symbols("z pi_u", real=True)
    R = s.sqrt(1+z*z)
    H = b*b/(alpha*p*p)*(s.sqrt(1+(alpha*pi*p**3/b)**2)-1)
    ut = s.diff(H, pi)
    z_rule = {pi: b*z/(alpha*p**3)}
    exact("canonical_velocity_all_finite_momenta", ut.subs(z_rule)-b*p*z/R)
    exact("canonical_momentum_equation",
          -du(H).subs(z_rule)-b*b/(alpha*p*p)*(R+2-3/R))
    exact("canonical_strict_convexity",
          s.diff(H, pi, 2).subs(z_rule)-alpha*p**4/R**3)
    exact("rate_strictly_inside_limit", 1-(z/R)**2-1/(1+z*z))
    exact("positive_energy_rationalization", (R-1)-z*z/(R+1))
    checks["positive_finite_state_kinetic"] = {
        "passed": (alpha*p**4/R**3).is_positive is True,
        "coefficient": str(alpha*p**4/R**3)}
    checks["nonnegative_kinetic_energy"] = {
        "passed": (z*z/(R+1)).is_nonnegative is True,
        "factor": str(z*z/(R+1))}
    exact("scalar_characteristic_speed", (1/alpha)/(p**-4*R**3/alpha)-p**4/R**3)
    exact("cone_inside_light", 1-(1/R**3)-(R**3-1)/R**3)
    checks["characteristic_speed_causal"] = {
        "passed": (z*z*(R*R+R+1)/(R+1)).is_nonnegative is True,
        "reason": "sqrt(1+z^2)>=1 for all real finite z",
        "speed_squared": str(p**4/R**3)}

    mt2, gx2, pot, electric2, magnetic2 = s.symbols(
        "matter_t_squared matter_grad_squared V electric_squared magnetic_squared", real=True)
    Lm = mt2/(2*p**4)-gx2/2-pot/p**2
    Llight = electric2/(2*p**2)-p**2*magnetic2/2
    exact("matter_action_constant_operational_scaling",
          Lm.subs({p: scale*p, mt2: scale**2*mt2, gx2: gx2/scale**2},
                  simultaneous=True)-Lm/scale**2)
    exact("Maxwell_action_constant_operational_scaling",
          Llight.subs({p: scale*p, magnetic2: magnetic2/scale**4},
                      simultaneous=True)-Llight/scale**2)
    Sm = 2*mt2/p**4-2*pot/p**2
    Slight = electric2/p**2+p**2*magnetic2
    exact("oscillon_source_from_same_action", du(Lm)-Sm)
    exact("light_source_from_same_action", du(Llight)-Slight)
    exact("light_source_twice_energy",
          Slight-2*(electric2/(2*p**2)+p**2*magnetic2/2))
    controls["light_source_must_not_be_omitted"] = {
        "passed": s.simplify(Slight.subs({electric2: 1, magnetic2: 0})) != 0,
        "nonzero_missing_source": str(Slight.subs({electric2: 1, magnetic2: 0}))}

    # Independent local Noether identity in 1+1 jets (the transverse
    # components and spatial directions add the same identity).
    tt, xx = s.symbols("t x", real=True)
    fields = [s.Function(name)(tt, xx) for name in ("u", "a", "c")]
    U, a, c = fields
    rates = [s.diff(f, tt) for f in fields]
    gradients = [s.diff(f, xx) for f in fields]
    P = s.exp(-U)
    q = a*a+c*c
    V = q/2-q*q/4+q**3/24
    L = (b*b/(alpha*P*P)*(1-s.sqrt(1-rates[0]**2/(b*b*P*P)))
         -gradients[0]**2/(2*alpha)
         +(rates[1]**2+rates[2]**2)/(2*P**4)
         -(gradients[1]**2+gradients[2]**2)/2-V/P**2)
    moms = [s.diff(L, x) for x in rates]
    fluxes = [s.diff(L, x) for x in gradients]
    equations = [s.diff(m, tt)+s.diff(f, xx)-s.diff(L, field)
                 for m, f, field in zip(moms, fluxes, fields)]
    energy = sum(v*m for v, m in zip(rates, moms))-L
    flux = sum(v*f for v, f in zip(rates, fluxes))
    exact("independent_local_total_energy_identity",
          s.diff(energy, tt)+s.diff(flux, xx)
          -sum(v*eq for v, eq in zip(rates, equations)))
    exact("unchanged_foundation_energy_flux", rates[0]*fluxes[0]+rates[0]*gradients[0]/alpha)
    light = s.Function("A_y")(tt, xx)
    light_t, light_x = s.diff(light, tt), s.diff(light, xx)
    Llight_plane = light_t**2/(2*P**2)-P**2*light_x**2/2
    light_mom = s.diff(Llight_plane, light_t)
    light_flux_derivative = s.diff(Llight_plane, light_x)
    light_eq = s.diff(light_mom, tt)+s.diff(light_flux_derivative, xx)
    Hlight = light_t*light_mom-Llight_plane
    Jlight = light_t*light_flux_derivative
    exact("independent_light_energy_exchange",
          s.diff(Hlight, tt)+s.diff(Jlight, xx)-light_t*light_eq
          +rates[0]*s.diff(Llight_plane, U))
    exact("light_cone_unchanged",
          -s.diff(Llight_plane, light_x, 2)/s.diff(Llight_plane, light_t, 2)-P**4)

    # The homogeneous numerical system is checked independently from
    # Hamiltonian derivatives, not merely by monitoring its integral.
    aa, cc, Pa, Pc = s.symbols("a c Pi_a Pi_c", real=True)
    q = aa*aa+cc*cc
    V = q/2-q*q/4+q**3/24
    Htot = H+p**4*(Pa*Pa+Pc*Pc)/2+V/p**2
    exact("homogeneous_matter_source",
          -du(Htot)+du(H)-2*p**4*(Pa*Pa+Pc*Pc)+2*V/p**2)
    qrate = s.diff(Htot, Pa)*Pc-s.diff(Htot, Pc)*Pa
    qrate += aa*(-s.diff(Htot, cc))-cc*(-s.diff(Htot, aa))
    exact("homogeneous_conserved_charge", qrate)
    amp2 = s.symbols("amplitude_squared", nonnegative=True)
    exact("positive_sextic_potential",
          amp2/2-amp2**2/4+amp2**3/24-amp2*((amp2-3)**2+3)/24)
    exact("potential_lower_quadratic_bound",
          amp2/2-amp2**2/4+amp2**3/24-amp2/8-amp2*(amp2-3)**2/24)
    Hmatter = p**4*(Pa*Pa+Pc*Pc)/2+V/p**2
    charge = aa*Pc-cc*Pa
    for sign in (-1, 1):
        square_bound = ((p*p*Pa+sign*cc/(2*p))**2
                        +(p*p*Pc-sign*aa/(2*p))**2)/2+q*(q-3)**2/(24*p*p)
        exact("homogeneous_energy_charge_bound_sign_"+str(sign),
              Hmatter-sign*p*charge/2-square_bound)

    p0, t, tau = s.symbols("p0 t tau", positive=True)
    lower = p0/(1+b*p0*t)
    tau_lower = s.log(1+b*p0*t)/b
    exact("external_clock_comparison_solution", s.diff(lower, t)+b*lower**2)
    exact("proper_clock_lower_integral", s.diff(tau_lower, t)-lower)
    exact("own_clock_comparison_solution",
          s.diff(p0*s.exp(-b*tau), tau)+b*p0*s.exp(-b*tau))
    PF, PF0 = s.symbols("P_F P_F0", positive=True)
    PFt, PFgrad2 = s.symbols("P_F_t P_F_gradient_squared", real=True)
    pressure_energy = (b*b*PF0/(alpha*PF)
        *(1/s.sqrt(1-PF0*PFt**2/(4*b*b*PF**3))-1)
        +PFgrad2/(8*alpha*PF**2))
    grad_u2 = s.symbols("gradient_u_squared", nonnegative=True)
    exact("pressure_variable_rearrangement_energy",
          pressure_energy.subs({PF: PF0*p*p, PFt: -2*PF0*p*p*w,
                                PFgrad2: 4*PF0**2*p**4*grad_u2})
          -hkin-grad_u2/(2*alpha))
    exact("static_uniform_pressure_has_zero_response_energy",
          pressure_energy.subs({PFt: 0, PFgrad2: 0}))
    checks["infinite_future_foundation_proper_time"] = {
        "passed": s.limit(tau_lower, t, s.oo) == s.oo,
        "lower_integral_limit": str(s.limit(tau_lower, t, s.oo))}
    controls["external_slowing_alone_is_not_two_clock_proof"] = {
        "passed": s.integrate(p0*s.exp(-b*t), (t, 0, s.oo)) == p0/b,
        "proper_time_of_exponential_counterexample": str(p0/b)}
    controls["old_unrestricted_kinetic_does_not_impose_new_cap"] = {
        "passed": s.simplify((alpha*p**4*pi/(b*p)).subs(pi, 2*b/(alpha*p**3))) == 2,
        "old_rate_over_new_bound": "2"}
    controls["positive_p_does_not_bound_stress"] = {
        "passed": s.limit(H.subs(p, 1), pi, s.oo) == s.oo,
        "finite_pressure_factor": "1",
        "kinetic_energy_density_as_momentum_diverges": str(s.limit(H.subs(p, 1), pi, s.oo)),
        "meaning": "No pressure-zero theorem implies a curvature or stress bound."}
    return checks, controls


def potential(q):
    return q/2-q*q/4+q*q*q/24


def rhs(t, y, alpha, b):
    u, momentum, a, c, Pa, Pc, tau = y
    p = np.exp(-u)
    z = alpha*p**3*momentum/b
    R = np.hypot(1.0, z)
    q = a*a+c*c
    V = potential(q)
    # Rationalized R+2-3/R avoids subtractive cancellation at small z.
    temporal_force = z*z*(R+3)/(R*(R+1))
    source = 2*p**4*(Pa*Pa+Pc*Pc)-2*V/p**2
    Vprime_over_f = 1-q+q*q/4
    return np.array([
        alpha*p**4*momentum/R,
        b*b/(alpha*p*p)*temporal_force+source,
        p**4*Pa, p**4*Pc,
        -a*Vprime_over_f/p**2, -c*Vprime_over_f/p**2, p])


def diagnostics(y, alpha, b):
    u, momentum, a, c, Pa, Pc, tau = y
    p = np.exp(-u)
    z = alpha*p**3*momentum/b
    R = np.hypot(1.0, z)
    foundation = b*b/(alpha*p*p)*z*z/(R+1)
    matter = p**4*(Pa*Pa+Pc*Pc)/2+potential(a*a+c*c)/p**2
    return p, z/R, foundation+matter, a*Pc-c*Pa, foundation, matter


def numerical_checks():
    alpha = .003
    times = np.linspace(0, 12, 601)
    results = []
    specs = [(b, v, False) for b in (.5, 1., 2.) for v in (0., .9)]
    specs.append((1., .9, True))
    for b, v, empty in specs:
        y0 = np.array([0., b*v/(alpha*np.sqrt(1-v*v)),
                       0. if empty else 1., 0., 0., 0. if empty else .8, 0.])
        runs = []
        for rtol, atol, step in ((1e-8, 1e-10, .02), (1e-10, 1e-12, .01)):
            solution = solve_ivp(
                lambda t, y: rhs(t, y, alpha, b), (0., 12.), y0,
                method="DOP853", t_eval=times, rtol=rtol, atol=atol, max_step=step)
            if not solution.success or solution.y.shape[1] != len(times):
                results.append({"b": b, "initial_v": v, "empty": empty,
                                "passed": False, "message": solution.message})
                break
            runs.append(solution.y)
        if len(runs) != 2:
            continue
        fine = runs[1]
        p, rate, energy, charge, foundation, matter = diagnostics(fine, alpha, b)
        comparison = float(np.max(np.abs(runs[0]-fine)/(1+np.abs(fine))))
        energy_error = float(np.max(np.abs(energy-energy[0]))/max(1., abs(energy[0])))
        charge_error = float(np.max(np.abs(charge-charge[0]))/max(1., abs(charge[0])))
        external_margin = float(np.min(p-1/(1+b*times)))
        proper_margin = float(np.min(fine[-1]-np.log1p(b*times)/b))
        own_clock_margin = float(np.min(p-np.exp(-b*fine[-1])))
        passed = (comparison < 2e-5 and energy_error < 2e-6
                  and np.max(np.abs(rate)) < 1 and np.min(p) > 0
                  and external_margin >= -1e-7 and proper_margin >= -1e-7
                  and own_clock_margin >= -1e-7
                  and np.all(np.isfinite(fine)))
        results.append({
            "b": b, "initial_v": v, "empty": empty, "passed": bool(passed),
            "energy_relative_error": energy_error, "charge_relative_error": charge_error,
            "two_resolution_state_difference": comparison,
            "external_bound_margin": external_margin,
            "proper_clock_integral_margin": proper_margin,
            "own_clock_pressure_margin": own_clock_margin,
            "minimum_p": float(np.min(p)), "final_p": float(p[-1]),
            "max_rate_fraction": float(np.max(np.abs(rate))),
            "final_foundation_proper_time": float(fine[-1, -1]),
            "energy_initial": float(energy[0]), "energy_final": float(energy[-1]),
            "foundation_energy_final": float(foundation[-1]), "matter_energy_final": float(matter[-1]),
        })
    return results


def reviewer_hamiltonian_check():
    """Post-first-run exploratory regression, not a preregistered physics gate."""
    rng = np.random.default_rng(20260919)
    alpha, step = .003, 1e-28

    def independent_energy(y, b):
        u, momentum, a, c, Pa, Pc, _ = y
        p = np.exp(-u)
        z = alpha*p**3*momentum/b
        R = np.sqrt(1+z*z)
        q = a*a+c*c
        return (b*b/(alpha*p*p)*z*z/(R+1)
                +p**4*(Pa*Pa+Pc*Pc)/2+(q/2-q*q/4+q**3/24)/p**2)

    maximum = 0.
    for i in range(60):
        b = (.5, 1., 2.)[i % 3]
        y = np.array([rng.uniform(-.4, .8), rng.uniform(-600, 600),
                      *rng.uniform(-1, 1, 4), 0.])
        derivatives = []
        for j in range(6):
            point = y.astype(complex)
            point[j] += 1j*step
            derivatives.append(np.imag(independent_energy(point, b))/step)
        expected = np.array([derivatives[1], -derivatives[0],
                             derivatives[4], derivatives[5],
                             -derivatives[2], -derivatives[3], np.exp(-y[0])])
        actual = rhs(0., y, alpha, b)
        maximum = max(maximum, float(np.max(np.abs(actual-expected)/(1+np.abs(expected)))))
    vacuum = rhs(0., np.zeros(7), alpha, 1.)
    return {"passed": bool(maximum < 2e-10 and np.array_equal(vacuum, [0, 0, 0, 0, 0, 0, 1])),
            "maximum_scaled_rhs_difference": maximum, "cases": 60,
            "rng_seed": 20260919, "vacuum_rhs": vacuum.tolist(),
            "scope": "Reviewer-added deterministic code regression after the first time run."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbolic-only", action="store_true")
    args = parser.parse_args()
    if CLAIM not in LEDGER.read_text(encoding="utf-8-sig"):
        raise ValueError("Frozen contract is missing.")
    provenance = {key: {"path": str(path), "sha256": digest(path),
                        "expected_sha256": expected, "passed": digest(path) == expected}
                  for key, (path, expected) in PINS.items()}
    if not all(item["passed"] for item in provenance.values()):
        raise RuntimeError("Inherited source changed; review contract.")
    checks, controls = symbolic_checks()
    numerical = [] if args.symbolic_only else numerical_checks()
    reviewer = reviewer_hamiltonian_check()
    symbolic_pass = all(x["passed"] for x in [*checks.values(), *controls.values()])
    numerical_pass = bool(numerical) and len(numerical) == 7 and all(x["passed"] for x in numerical)
    passed = symbolic_pass and reviewer["passed"] and (args.symbolic_only or numerical_pass)
    result = {
        "claim_id": CLAIM, "status": "PASS_DECLARED_CANDIDATE_GATES" if passed else "FAIL",
        "checks": checks, "negative_controls": controls, "homogeneous_evolutions": numerical,
        "reviewer_added_code_regression": reviewer,
        "sources": provenance, "self_sha256": digest(Path(__file__)),
        "ledger_sha256_at_run": digest(LEDGER),
        "software": {"python": platform.python_version(), "sympy": s.__version__,
                     "numpy": np.__version__, "scipy": scipy.__version__},
        "new_postulate": "Finite proper foundation response rate b, implemented by the displayed action.",
        "verified_flags": {
            "variational_source_and_energy": symbolic_pass,
            "static_scalar_equilibria_inherited": symbolic_pass,
            "two_foundation_clock_pressure_bound": symbolic_pass,
            "homogeneous_nonzero_charge_global_continuation": symbolic_pass,
            "homogeneous_numerical_energy_and_bounds": numerical_pass},
        "closure_flags": {key: False for key in (
            "background_tension_EOS_derived", "b_observationally_calibrated",
            "full_gravitational_theory", "tensor_radiation_completion", "full_PPN",
            "global_PDE_continuation", "curvature_bounded", "geodesically_complete",
            "singularity_resolution", "observational_pass")},
        "scope": "Positive initial p, classical solution interval; proper-clock theorem is along the foundation congruence, not all moving observers or null geodesics.",
        "homogeneous_global_theorem_assumptions": [
            "Zero Maxwell field, homogeneous unit periodic coordinate cell.",
            "Finite initial energy E>0 and nonzero conserved phase charge Q.",
            "The retained positive sextic potential, alpha>0, b>0, p0>0.",
            "No inference of global localized PDE continuation from this ODE theorem."],
        "static_branch_warning": "Static equations are unchanged, including any pre-existing singular static branches.",
        "side_effects": "stdout only; no manuscript, old action or strong-field evolution changed",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        raise AssertionError("At least one declared candidate gate failed.")


if __name__ == "__main__":
    main()
