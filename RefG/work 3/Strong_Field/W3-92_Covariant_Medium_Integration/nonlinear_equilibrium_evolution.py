# Bounded nonlinear Einstein--scalar evolution; stdout only.
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import time
sys.dont_write_bytecode = True
import numpy as np
import scipy
import sympy as sp

HERE = Path(__file__).resolve().parent
SF = HERE.parent
ALPHA, SEXTIC, F0 = 0.04, 0.25, 1.820210505787701
PINS = {
    "W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field.py":
        "99bc4331bec07219308bd15e43a945792ecd59c60ef959d17684944a6635aa77",
    "W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field_preregistration.md":
        "25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1",
    "W3-65_First_Turning_Point/w3_65_fixed_alpha_first_turning_point.py":
        "5cc24de6951bbd57e0091b687ab467dac2070eb73403d71c52ff91386dae1b73",
    "W3-65_First_Turning_Point/w3_65_fixed_alpha_first_turning_point_preregistration.md":
        "385402e843850725ed562a449adb246b510b65038685cad6521d9ff1c8be3942",
    "W3-66_Physical_Radial_Mode/w3_66_result.json":
        "a876dfb9a073d2960db7c12cb48f8ef43c944b91754f8b42a3260351d556e34f",
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def background():
    actual = {p: sha(SF / p) for p in PINS}
    if actual != PINS:
        raise RuntimeError("DEPENDENCY_FAILURE: " + json.dumps(actual))
    mod65 = load("w92_time_w65", SF / next(p for p in PINS if p.endswith(".py") and "W3-65" in p))
    dep, mod64 = mod65.dependency_gate()
    if not dep["all_pass"]:
        raise RuntimeError("Original W65 dependency gate failed")
    anchor, solution, _ = mod65.anchor_gate(mod64)
    if not anchor["pass"]:
        raise RuntimeError("Fresh W65 anchor failed")
    return mod65, mod64, solution, anchor, actual


def exact_tests():
    x, a, b, eps, w = sp.symbols("x a b eps w", real=True)
    v = x**2 / 2 - x**4 / 4 + x**6 / 24
    force = x - x**3 + x**5 / 4
    z, p = a + sp.I*b, x + sp.I*w
    tests = {
        "sextic_force": sp.simplify(sp.diff(v, x)-force) == 0,
        "nonnegative_potential_factorization": sp.simplify(
            v-x**2*((x**2-3)**2+3)/24) == 0,
        "wrong_cubic_force_rejected": sp.simplify(sp.diff(v, x)-(x+x**3+x**5/4)) != 0,
        "real_velocity_kick_preserves_initial_charge":
            sp.simplify(sp.im(x*(sp.I*w+eps*x))-x*w) == 0,
        "real_potential_has_zero_phase_torque":
            sp.simplify(sp.im(sp.conjugate(z)*a*z)) == 0,
        "kinematic_term_has_zero_charge_torque":
            sp.simplify(sp.im(sp.conjugate(p)*a*p)) == 0,
        "shared_edge_charge_cancellation":
            sp.simplify(sp.im((sp.conjugate(z)-sp.conjugate(p))*(p-z))) == 0,
    }
    h = sp.symbols("h", positive=True)
    tests["centre_quadratic_laplacian"] = sp.simplify(
        h**2 * (((3*h/2)**2-(h/2)**2)/h) / (h**3/3)-6) == 0
    r, S, M, pot = sp.symbols("r S M pot", positive=True)
    tests["linear_mass_constraint"] = sp.simplify(
        r**2*((1-2*a*M/r)*S/2+pot)+a*r*S*M-r**2*(S/2+pot)) == 0
    return tests


class Grid:
    def __init__(self, radius, h):
        n = round(radius/h)
        if n < 8 or abs(n*h-radius) > 1e-10:
            raise ValueError("Radius must be an integer number of cells")
        self.h, self.radius = float(h), float(radius)
        self.r = (np.arange(n)+0.5)*h
        self.edges = np.arange(n+1)*h
        self.vol = np.diff(self.edges**3)/3
        self.time_step = None
        self.stage_max_speed = 0.0
        self.stage_min_N = self.stage_min_sigma = math.inf

    def gradient(self, z):
        out = np.empty_like(z)
        out[1:-1] = (z[2:]-z[:-2])/(2*self.h)
        out[0] = (z[1]-z[0])/(2*self.h)
        out[-1] = (z[-1]-z[-2])/(2*self.h)
        return out

    def primitive(self, y, origin_power):
        # y~constant*r^origin_power at the regular centre.
        result = np.empty_like(y)
        result[0] = y[0]*self.r[0]/(origin_power+1)
        result[1:] = result[0] + np.cumsum((y[:-1]+y[1:])*(self.h/2))
        return result

    def geometry(self, field, momentum):
        grad = self.gradient(field)
        square = abs(field)**2
        potential = square/2-square**2/4+SEXTIC*square**3/6
        kinetic = abs(momentum)**2+abs(grad)**2
        jprime = ALPHA*self.r*kinetic
        J = self.primitive(jprime, 1)
        Jouter = J[-1]+jprime[-1]*self.h/2
        if not np.all(np.isfinite(J)) or Jouter > 500:
            raise FloatingPointError("Nonfinite or unresolved integrating factor")
        integrand = np.exp(J)*self.r**2*(kinetic/2+potential)
        integral = self.primitive(integrand, 2)
        mass = np.exp(-J)*integral
        mass_outer = math.exp(-Jouter)*(integral[-1]+integrand[-1]*self.h/2)
        N = 1-2*ALPHA*mass/self.r
        sigma = np.exp(J-Jouter)
        if (not np.all(np.isfinite(mass)) or np.min(N) <= 0
                or np.min(sigma) <= 0 or not math.isfinite(mass_outer)):
            raise FloatingPointError("Evolution left the regular polar-areal chart")
        return dict(N=N, sigma=sigma, c=N*sigma, mass=mass,
                    mass_outer=mass_outer, sigma0=math.exp(-Jouter), gradient=grad)

    def rhs(self, state):
        field, momentum = state
        g = self.geometry(field, momentum)
        self.stage_max_speed = max(self.stage_max_speed, float(np.max(g["c"])))
        self.stage_min_N = min(self.stage_min_N, float(np.min(g["N"])))
        self.stage_min_sigma = min(self.stage_min_sigma, float(np.min(g["sigma"])))
        if self.time_step is not None and self.time_step*self.stage_max_speed/self.h >= 0.45:
            raise FloatingPointError("Registered characteristic Courant bound exceeded")
        cedge = (g["c"][:-1]+g["c"][1:])/2
        flux = np.zeros(len(field)+1, dtype=complex)
        flux[1:-1] = self.edges[1:-1]**2*cedge*np.diff(field)/self.h
        square = abs(field)**2
        force = (1-square+SEXTIC*square**2)*field
        return np.array([g["c"]*momentum, np.diff(flux)/self.vol-g["sigma"]*force])

    def diagnostics(self, state, t):
        field, momentum = state
        g = self.geometry(field, momentum)
        density = np.imag(np.conjugate(field)*momentum)
        weighted = self.vol*density
        charge = float(np.sum(weighted))
        proper_r = self.primitive(1/np.sqrt(g["N"]), 0)
        ar2 = float(np.sum(weighted*self.r**2)/charge)
        pr2 = float(np.sum(weighted*proper_r**2)/charge)
        if charge <= 0 or min(ar2, pr2) <= 0:
            raise FloatingPointError("Charge-weighted radius left declared domain")
        centre = (9*field[0]-field[1])/8
        derivative = g["c"]*momentum
        centre_dot = (9*derivative[0]-derivative[1])/8
        local_frequency = float(np.imag(np.conjugate(centre)*centre_dot)/
                                (abs(centre)**2*g["sigma0"]))
        return dict(t=float(t), charge=charge, ADM_mass=float(g["mass_outer"]),
                    central_amplitude=float(abs(centre)), maximum_amplitude=float(max(abs(field))),
                    central_lapse=float(g["sigma0"]), minimum_N=float(min(g["N"])),
                    minimum_sigma=float(min(g["sigma"])),
                    charge_rms_areal=math.sqrt(ar2), charge_rms_proper=math.sqrt(pr2),
                    central_proper_frequency=local_frequency,
                    negative_charge_fraction=float(np.sum(abs(weighted[weighted < 0]))/charge))

    def local_flux_check(self, state, eta=1e-6):
        # Independent Einstein tr: Mdot=r^2 sigma N^2 Re(conj(Pi)*phi_r).
        # Obtain Mdot by differentiating the constraint solution along the
        # actual numerical vector field, not by substituting this target.
        rhs = self.rhs(state)
        g = self.geometry(*state)
        mass_plus = self.geometry(*(state+eta*rhs))["mass"]
        mass_minus = self.geometry(*(state-eta*rhs))["mass"]
        mdot = (mass_plus-mass_minus)/(2*eta)
        coefficient = self.r**2*g["sigma"]*g["N"]**2
        expected = coefficient*np.real(np.conjugate(state[1])*g["gradient"])
        scale = coefficient*abs(state[1])*abs(g["gradient"])
        inside = self.r <= 15
        norm = lambda a: math.sqrt(float(np.sum(self.vol[inside]*a[inside]**2)))
        qrate = float(np.sum(self.vol*np.imag(
            np.conjugate(rhs[0])*state[1]+np.conjugate(state[0])*rhs[1])))
        # Independent fourth-order derivative, not the reconstruction quadrature.
        d4 = lambda a: (a[:-4]-8*a[1:-3]+8*a[3:-1]-a[4:])/(12*self.h)
        region = (self.r[2:-2] <= 15)
        square = abs(state[0])**2
        kinetic = abs(state[1])**2+abs(g["gradient"])**2
        potential = square/2-square**2/4+SEXTIC*square**3/6
        mass_source = (self.r**2*(g["N"]*kinetic/2+potential))[2:-2]
        lapse_source = (ALPHA*self.r*kinetic)[2:-2]
        ratio = lambda residual, source: float(np.linalg.norm(residual[region])/
                                                max(np.linalg.norm(source[region]), 1e-14))
        return dict(local_mass_flux_absolute_l2=norm(mdot-expected),
                    local_mass_flux_relative_l2=norm(mdot-expected)/max(norm(scale), 1e-14),
                    mass_radial_constraint_relative_l2=ratio(d4(g["mass"])-mass_source, mass_source),
                    lapse_radial_constraint_relative_l2=ratio(d4(np.log(g["sigma"]))-lapse_source, lapse_source),
                    semidiscrete_charge_rate=qrate, directional_step=eta,
                    radial_diagnostic_domain=[0.0, 15.0])


def run_case(solution, mod64, h=0.1, epsilon=0.0, duration=96.0, radius=80.0,
             courant=0.2, sample_interval=0.5):
    if min(h, duration, radius, courant, sample_interval) <= 0:
        raise ValueError("Positive numerical scales required")
    grid = Grid(radius, h)
    f, _, mass, logsigma = solution.sol(grid.r)
    omega = mod64.omega_from_parameter(solution.p)
    originalN = 1-2*ALPHA*mass/grid.r
    originalPi = 1j*omega*f/(np.exp(logsigma)*originalN)
    kick = epsilon*f*np.exp(-(grid.r/4)**2)
    state = np.array([f.astype(complex), originalPi+kick])
    initialQ = float(np.sum(grid.vol*np.imag(np.conjugate(f)*originalPi)))
    first = grid.diagnostics(state, 0.0)
    charge_initial_error = abs(first["charge"]-initialQ)/abs(initialQ)
    intervals = max(1, math.ceil(duration/sample_interval))
    sample_dt = duration/intervals
    per_sample = max(1, math.ceil(sample_dt/(courant*h)))
    dt = sample_dt/per_sample
    grid.time_step = dt
    samples = [first]
    local_checks = [dict(t=0.0, **grid.local_flux_check(state))]
    half_eta_check = grid.local_flux_check(state, eta=5e-7)
    t = 0.0
    started = time.perf_counter()
    minimum_N, minimum_sigma = first["minimum_N"], first["minimum_sigma"]
    for j in range(intervals):
        for _ in range(per_sample):
            k1 = grid.rhs(state)
            k2 = grid.rhs(state+dt*k1/2)
            k3 = grid.rhs(state+dt*k2/2)
            k4 = grid.rhs(state+dt*k3)
            state = state+dt*(k1+2*k2+2*k3+k4)/6
            t += dt
        row = grid.diagnostics(state, t)
        samples.append(row)
        minimum_N = min(minimum_N, row["minimum_N"])
        minimum_sigma = min(minimum_sigma, row["minimum_sigma"])
        if (j+1) % 16 == 0 or j == intervals-1:
            local_checks.append(dict(t=float(t), **grid.local_flux_check(state)))
    qdrift = max(abs(row["charge"]/first["charge"]-1) for row in samples)
    mdrift = max(abs(row["ADM_mass"]/first["ADM_mass"]-1) for row in samples)
    amplitude_drift = max(abs(row["central_amplitude"]/first["central_amplitude"]-1) for row in samples)
    radius_drift = max(abs(row["charge_rms_proper"]/first["charge_rms_proper"]-1) for row in samples)
    summary = dict(maximum_relative_charge_drift=qdrift, maximum_relative_mass_drift=mdrift,
                   maximum_relative_central_amplitude_change=amplitude_drift,
                   maximum_relative_proper_radius_change=radius_drift,
                   minimum_N_sampled=minimum_N, minimum_sigma_sampled=minimum_sigma,
                   fixed_charge_initial_error=charge_initial_error,
                   maximum_local_flux_relative_l2=max(r["local_mass_flux_relative_l2"] for r in local_checks),
                   maximum_mass_constraint_relative_l2=max(r["mass_radial_constraint_relative_l2"] for r in local_checks),
                   maximum_lapse_constraint_relative_l2=max(r["lapse_radial_constraint_relative_l2"] for r in local_checks),
                   maximum_characteristic_Courant=dt*grid.stage_max_speed/h,
                   minimum_N_RHS_stages=grid.stage_min_N,
                   minimum_sigma_RHS_stages=grid.stage_min_sigma,
                   maximum_semidiscrete_charge_rate=max(abs(r["semidiscrete_charge_rate"]) for r in local_checks))
    summary["maximum_relative_semidiscrete_charge_rate"] = (
        summary["maximum_semidiscrete_charge_rate"]/abs(first["charge"]))
    summary["initial_directional_step_sensitivity"] = abs(
        local_checks[0]["local_mass_flux_relative_l2"]-half_eta_check["local_mass_flux_relative_l2"])
    gates = dict(finite_horizonless_execution=True, initial_charge_preserved=charge_initial_error < 1e-13,
                 characteristic_Courant=summary["maximum_characteristic_Courant"] < 0.45,
                 charge_budget=qdrift < 1e-5, mass_budget=mdrift < 5e-3,
                 directional_step_control=summary["initial_directional_step_sensitivity"] < 1e-6,
                 bounded_amplitude=amplitude_drift < 0.2, bounded_radius=radius_drift < 0.2)
    return dict(h=h, epsilon=epsilon, duration=duration, radius=radius, dt=dt,
                steps=intervals*per_sample, elapsed_seconds=time.perf_counter()-started,
                summary=summary, gates=gates, samples=samples, local_flux_checks=local_checks,
                initial_half_directional_step_check=half_eta_check,
                boundary="Zero scalar flux; finite-domain effects tested against larger radius.")


def waveform(case, key):
    return np.array([r[key] for r in case["samples"]])


def compare_waveforms(left, right, floor=1e-12):
    result = {}
    for key in ("central_amplitude", "charge_rms_proper", "central_lapse"):
        a, b = waveform(left, key), waveform(right, key)
        if len(a) != len(b):
            raise ValueError("Mismatched sampling")
        result[key] = float(np.sqrt(np.mean((a-b)**2))/max(np.sqrt(np.mean(b*b)), floor))
    return result


def hamiltonian_directional_check():
    rows = []
    for h in (0.1, 0.05, 0.025, 0.0125):
        grid = Grid(30, h)
        f = 1.5*np.exp(-(grid.r/3)**2).astype(complex)
        pi = 0.8j*f
        bump = np.zeros_like(grid.r)
        mask = grid.r < 5
        bump[mask] = np.exp(-1/(1-(grid.r[mask]/5)**2))
        df = (0.03+0.02j)*f*bump
        dpi = (0.025+0.04j)*f*bump
        eta = 1e-5
        direct = (grid.geometry(f+eta*df, pi+eta*dpi)["mass_outer"]-
                  grid.geometry(f-eta*df, pi-eta*dpi)["mass_outer"])/(2*eta)
        geom = grid.geometry(f, pi)
        square = abs(f)**2
        expected = np.sum(grid.vol*geom["sigma"]*(
            geom["N"]*np.real(np.conjugate(pi)*dpi+
                             np.conjugate(geom["gradient"])*grid.gradient(df))+
            (1-square+SEXTIC*square**2)*np.real(np.conjugate(f)*df)))
        rows.append(dict(h=h, finite_variation=float(direct), functional_variation=float(expected),
                         relative_error=float(abs(direct-expected)/max(abs(expected), 1e-14))))
    ratios = [b["relative_error"]/a["relative_error"] for a, b in zip(rows, rows[1:])]
    return dict(rows=rows, successive_error_ratios=ratios,
                passed=all(r < 0.6 for r in ratios) and rows[-1]["relative_error"] < 1e-4)


def kinetic_feedback_check(mod64, solution):
    """Fixed-profile Cauchy-data concavity, not equilibrium loading."""
    omega = mod64.omega_from_parameter(solution.p)
    rows = []
    for h in (0.1, 0.05, 0.025, 0.0125):
        grid = Grid(80, h)
        f, _, mass, logsigma = solution.sol(grid.r)
        f = f.astype(complex)
        b = omega*f/(np.exp(logsigma)*(1-2*ALPHA*mass/grid.r))
        k = f*np.exp(-(grid.r/4)**2)
        radial_k2 = grid.r*abs(k)**2
        integral = grid.primitive(radial_k2, 1)
        remaining = integral[-1]+radial_k2[-1]*h/2-integral
        reference_q = float(np.sum(grid.vol*np.imag(np.conjugate(f)*1j*b)))
        for load_s in (0.01, 0.1, 1.0, 5.0):
            def geometry_at(s):
                return grid.geometry(f, 1j*b+math.sqrt(s)*k)
            geometry = geometry_at(load_s)
            step = 1e-3*max(1, load_s)
            plus = geometry_at(load_s+step)["mass_outer"]
            minus = geometry_at(load_s-step)["mass_outer"]
            total = geometry["mass_outer"]
            first = (plus-minus)/(2*step)
            second = (plus-2*total+minus)/step**2
            weight = grid.vol*geometry["sigma"]*geometry["N"]*abs(k)**2
            expected_first = float(np.sum(weight)/2)
            expected_second = float(-ALPHA*np.sum(weight*remaining))
            q = float(np.sum(grid.vol*np.imag(
                np.conjugate(f)*(1j*b+math.sqrt(load_s)*k))))
            rows.append(dict(h=h, load_s=load_s, mass=total,
                first_difference=first, second_difference=second,
                integral_first=expected_first, integral_second=expected_second,
                relative_first_error=abs(first-expected_first)/abs(expected_first),
                relative_second_error=abs(second-expected_second)/abs(expected_second),
                relative_charge_change=abs(q-reference_q)/abs(reference_q),
                minimum_N=float(np.min(geometry["N"]))))
    errors = []
    for h in (0.1, 0.05, 0.025, 0.0125):
        group = [row for row in rows if row["h"] == h]
        errors.append(dict(h=h,
            first=max(row["relative_first_error"] for row in group),
            second=max(row["relative_second_error"] for row in group)))
    gates = dict(positive_first=all(row["first_difference"] > 0 for row in rows),
        negative_second=all(row["second_difference"] < 0 for row in rows),
        fixed_charge=all(row["relative_charge_change"] < 1e-13 for row in rows),
        regular_chart=all(row["minimum_N"] > 0 for row in rows),
        fine_accuracy=max(errors[-1]["first"], errors[-1]["second"]) < 1e-3,
        refinement=all(new[key] < 0.6*old[key]
            for old, new in zip(errors, errors[1:]) for key in ("first", "second")))
    gates = {name: bool(value) for name, value in gates.items()}
    return dict(rows=rows, errors=errors, gates=gates,
        scope="Fixed-profile, fixed-charge kinetic-loaded initial data; not equilibrium population loading.")


def announce(case):
    print("Finished h={h} eps={epsilon} T={duration}: {summary}".format(**case),
          file=sys.stderr, flush=True)


def suite(mod65, mod64, solution, reference_f0=F0, radius=80.0,
          domain_radius=100.0, duration=96.0, kick=0.02, require_resolved=False):
    cases, tests = {}, {}
    for h in (0.1, 0.05, 0.025):
        for eps in (0.0, kick, -kick):
            print(f"Evolution h={h} epsilon={eps} T={duration} R={radius}", file=sys.stderr, flush=True)
            case = run_case(solution, mod64, h=h, epsilon=eps, duration=duration, radius=radius)
            announce(case)
            cases[f"{h}:{eps}"] = case
            tests[f"case_{h}_{eps}"] = all(case["gates"].values())
    convergence = {}
    for eps in (0.0, kick, -kick):
        coarse, middle, fine = (cases[f"{h}:{eps}"] for h in (0.1, 0.05, 0.025))
        e01, e12 = compare_waveforms(coarse, middle), compare_waveforms(middle, fine)
        ratios = {key:e12[key]/max(e01[key], 1e-12) for key in e01}
        convergence[str(eps)] = dict(coarse_middle=e01, middle_fine=e12, ratios=ratios)
        tests[f"spatial_convergence_{eps}"] = all(e12[k] < 1e-4 or ratios[k] < 0.6 for k in ratios)
        eflux_mid = middle["summary"]["maximum_local_flux_relative_l2"]
        eflux_fine = fine["summary"]["maximum_local_flux_relative_l2"]
        tests[f"independent_mass_flux_{eps}"] = (
            eflux_fine < 5e-3 and (eflux_fine < 1e-6 or eflux_fine/max(eflux_mid, 1e-14) < 0.6))
        tests[f"semidiscrete_charge_{eps}"] = (
            fine["summary"]["maximum_relative_semidiscrete_charge_rate"] < 1e-10)
        convergence[str(eps)]["independent_local_mass_flux_ratio"] = eflux_fine/max(eflux_mid, 1e-14)
        convergence[str(eps)]["radial_constraint_ratios"] = {
            key: fine["summary"][key]/max(middle["summary"][key], 1e-14)
            for key in ("maximum_mass_constraint_relative_l2", "maximum_lapse_constraint_relative_l2")}
        tests[f"radial_constraint_convergence_{eps}"] = all(
            fine["summary"][key] < 5e-3 and (
                fine["summary"][key] < 1e-6 or
                convergence[str(eps)]["radial_constraint_ratios"][key] < 0.6)
            for key in convergence[str(eps)]["radial_constraint_ratios"])
    # Exact harmonic background has constant central amplitude and lapse.
    zero_errors = {}
    reference_sigma0 = float(np.exp(solution.sol(np.array([mod64.EPS]))[3, 0]))
    for h in (0.1, 0.05, 0.025):
        zero = cases[f"{h}:0.0"]
        zero_errors[str(h)] = {
            "central_amplitude": float(np.sqrt(np.mean((waveform(zero, "central_amplitude")/reference_f0-1)**2))),
            "central_lapse": float(np.sqrt(np.mean((waveform(zero, "central_lapse")/reference_sigma0-1)**2)))}
    tests["unkicked_harmonic_reference"] = all(
        zero_errors["0.025"][key] < 1e-4 or
        zero_errors["0.025"][key]/max(zero_errors["0.05"][key], 1e-14) < 0.6
        for key in zero_errors["0.025"])
    print("Fine-grid half-timestep control", file=sys.stderr, flush=True)
    temporal = run_case(solution, mod64, h=0.025, epsilon=kick, courant=0.1,
                        duration=duration, radius=radius)
    announce(temporal)
    time_error = compare_waveforms(cases[f"0.025:{kick}"], temporal)
    tests["half_timestep"] = all(temporal["gates"].values()) and max(time_error.values()) < 1e-3
    print(f"Original BVP radius={domain_radius} and domain evolution control", file=sys.stderr, flush=True)
    extended = mod65.solve_at(mod64, reference_f0, solution, radius=domain_radius)
    domain = run_case(extended, mod64, h=0.05, epsilon=kick, radius=domain_radius, duration=duration)
    announce(domain)
    domain_error = compare_waveforms(cases[f"0.05:{kick}"], domain)
    tests["outer_domain"] = all(domain["gates"].values()) and max(domain_error.values()) < 1e-3
    returns = {}
    resolution = {}
    for eps in (kick, -kick):
        delta = waveform(cases[f"0.025:{eps}"], "central_amplitude")-waveform(cases["0.025:0.0"], "central_amplitude")
        active = np.sign(delta[abs(delta) > 1e-5])
        crossings = int(np.count_nonzero(active[1:] != active[:-1]))
        returns[str(eps)] = dict(sign_crossings=crossings, maximum_excursion=float(max(abs(delta))))
        tests[f"oscillatory_returns_{eps}"] = crossings >= 2
        mid_delta = waveform(cases[f"0.05:{eps}"], "central_amplitude")-waveform(cases["0.05:0.0"], "central_amplitude")
        response = float(np.sqrt(np.mean(delta**2))/reference_f0)
        zero_error = zero_errors["0.025"]["central_amplitude"]
        grid_error = float(np.sqrt(np.mean((delta-mid_delta)**2))/reference_f0)
        resolution[str(eps)] = dict(fractional_RMS_response=response,
            fractional_zero_control_RMS=zero_error, fractional_response_grid_error=grid_error,
            response_over_zero_error=response/max(zero_error, 1e-30),
            response_over_grid_error=response/max(grid_error, 1e-30))
        if require_resolved:
            tests[f"resolved_signed_response_{eps}"] = response > 3*max(zero_error, grid_error)
    odd = (waveform(cases[f"0.025:{kick}"], "central_amplitude")-
           waveform(cases[f"0.025:{-kick}"], "central_amplitude"))/2
    odd_mid = (waveform(cases[f"0.05:{kick}"], "central_amplitude")-
               waveform(cases[f"0.05:{-kick}"], "central_amplitude"))/2
    resolution["odd_supplementary"] = dict(
        fractional_RMS=float(np.sqrt(np.mean(odd**2))/reference_f0),
        fractional_grid_error=float(np.sqrt(np.mean((odd-odd_mid)**2))/reference_f0))
    return dict(cases=cases, convergence=convergence, unkicked_exact_reference_errors=zero_errors,
                temporal_control=temporal,
                temporal_error=time_error, domain_control=domain, domain_error=domain_error,
                oscillatory_returns=returns, signed_response_resolution=resolution, gates=tests)


def compact_background(mod65, mod64, anchor):
    target = 2.168601437933647
    previous = anchor
    for f0 in mod65.MAIN_F0_GRID[1:]:
        if f0 > 2.16+1e-12:
            break
        previous = mod65.solve_at(mod64, f0, previous)
    previous = mod65.solve_at(mod64, target, previous)
    previous = mod65.solve_at(mod64, target, previous, radius=160.0)
    record = mod65.compact_record(target, mod65.observe(
        mod64, previous, target, radius=160.0, with_residuals=True))
    if not mod65.basic_profile_pass(record):
        raise RuntimeError("Fresh compact static background gate failed")
    saved = json.loads((SF/"W3-66_Physical_Radial_Mode/w3_66_result.json").read_text(encoding="utf-8"))
    mode = min(saved["primary_modes"], key=lambda r: abs(r["f0"]-target))
    if abs(mode["f0"]-target) > 1e-12 or mode["Lambda"] <= 0:
        raise RuntimeError("Registered stable compact radial benchmark not found")
    return previous, dict(record=record, saved_radial_Lambda=mode["Lambda"],
        saved_lowest_radial_period=2*math.pi/math.sqrt(mode["Lambda"]),
        saved_spectrum_is_not_freshly_recomputed=True)


def compact_refinement_verdict(outputs):
    """Combine three --compact-refinement-case JSON outputs with provenance."""
    if len(outputs) != 3:
        raise ValueError("Exactly three CLI outputs required.")
    reference = 2.168601437933647
    sources = {out["source_sha256"] for out in outputs}
    if len(sources) != 1 or any(len(s) != 64 for s in sources):
        raise ValueError("Matching solver source hashes required.")
    for source in sources:
        int(source, 16)
    packets = []
    for out in outputs:
        if (out["dependency_hashes"] != PINS or not out["upstream_files_unchanged"]
                or not all(out["exact_checks"].values())
                or not out["hamiltonian_directional_check"]["passed"]):
            raise ValueError("Dependency or inherited diagnostic failure.")
        if out["model_parameters"] != dict(alpha=ALPHA, sextic=SEXTIC):
            raise ValueError("Registered action parameters required.")
        if abs(out["compact_background"]["record"]["f0"]-reference) > 1e-12:
            raise ValueError("Registered compact background required.")
        cases = out["refinement_cases"]
        if set(cases) != {"0.025", "0.0125"}:
            raise ValueError("Registered grid pair required.")
        eps = float(cases["0.025"]["epsilon"])
        packed = {}
        for key, case in cases.items():
            h = float(key)
            if (case["h"] != h or case["epsilon"] != eps
                    or case["radius"] != 160.0 or case["duration"] != 256.0
                    or abs(case["dt"]-0.2*h) > 1e-14
                    or case["steps"] != round(256.0/(0.2*h))):
                raise ValueError("Mismatched case parameters.")
            times = np.array([row["t"] for row in case["samples"]])
            if len(times) != 513 or not np.allclose(times, np.arange(513)*0.5,
                                                   rtol=0, atol=1e-7):
                raise ValueError("Mismatched sampling times.")
            waves = {name: waveform(case, name) for name in
                     ("central_amplitude", "central_lapse", "charge_rms_proper")}
            if not all(np.all(np.isfinite(a)) for a in waves.values()):
                raise ValueError("Nonfinite waveform.")
            packed[key] = dict(summary=case["summary"], gates=case["gates"], waves=waves)
        packets.append(dict(epsilon=eps, cases=packed, inputs_unchanged=True))
    runs = {float(p["epsilon"]): p for p in packets}
    if set(runs) != {0.0, 0.002, -0.002}:
        raise ValueError("Matching zero and both registered signed packets required.")
    rms = lambda x: float(np.sqrt(np.mean(np.asarray(x)**2)))
    wave = lambda eps, h: np.asarray(runs[eps]["cases"][h]["waves"]["central_amplitude"])
    old_zero, new_zero = wave(0.0, "0.025"), wave(0.0, "0.0125")
    if len(old_zero) != 513 or len(new_zero) != 513:
        raise ValueError("Expected the registered T=256, sampling=0.5 waveforms.")
    zero_old = rms(old_zero/reference-1)
    zero_new = rms(new_zero/reference-1)
    tests = dict(provenance_and_sampling=True,
                 inputs_unchanged=all(p["inputs_unchanged"] for p in packets),
                 zero_control_refinement=zero_new < 0.6*zero_old)
    for eps, packet in runs.items():
        cases = packet["cases"]
        for h in ("0.025", "0.0125"):
            tests[f"case_{eps}_{h}"] = all(cases[h]["gates"].values())
        tests[f"semidiscrete_charge_{eps}"] = (
            cases["0.0125"]["summary"]["maximum_relative_semidiscrete_charge_rate"] < 1e-10)
        for key in ("maximum_local_flux_relative_l2",
                    "maximum_mass_constraint_relative_l2",
                    "maximum_lapse_constraint_relative_l2"):
            old, new = (cases[h]["summary"][key] for h in ("0.025", "0.0125"))
            tests[f"{key}_{eps}"] = new < 5e-3 and (new < 1e-6 or new < 0.6*old)
    resolution = {}
    for eps in (0.002, -0.002):
        old_delta = wave(eps, "0.025")-old_zero
        new_delta = wave(eps, "0.0125")-new_zero
        response = rms(new_delta)/reference
        discrepancy = rms(new_delta-old_delta)/reference
        resolution[str(eps)] = dict(response=response, zero_error=zero_new,
            grid_error=discrepancy, response_over_zero=response/max(zero_new, 1e-30),
            response_over_grid=response/max(discrepancy, 1e-30))
        tests[f"resolved_response_{eps}"] = response > 3*max(zero_new, discrepancy)
        active = np.sign(new_delta[abs(new_delta) > 1e-5])
        crossings = int(np.count_nonzero(active[1:] != active[:-1]))
        resolution[str(eps)]["sign_crossings"] = crossings
        tests[f"oscillatory_returns_{eps}"] = crossings >= 2
    return dict(gates={key: bool(value) for key, value in tests.items()},
        zero_error_old=zero_old, zero_error_new=zero_new, resolution=resolution,
        new_half_step_or_domain_run=False, original_compact_suite_status="OPEN",
        scope="Supplementary spatial resolution; original time/domain controls retained.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--pilot", action="store_true")
    modes.add_argument("--run-case", action="store_true")
    modes.add_argument("--compact-suite", action="store_true")
    modes.add_argument("--compact-refinement-case", action="store_true")
    modes.add_argument("--source-feedback-only", action="store_true")
    parser.add_argument("--h", type=float, default=0.1)
    parser.add_argument("--epsilon", type=float, default=0.02)
    parser.add_argument("--T", type=float, default=96.0)
    parser.add_argument("--radius", type=float, default=80.0)
    parser.add_argument("--courant", type=float, default=0.2)
    args = parser.parse_args(argv)
    result = dict(status="OPEN", source_sha256=sha(__file__), exact_checks=exact_tests(),
                  model_parameters=dict(alpha=ALPHA, sextic=SEXTIC))
    try:
        if not all(result["exact_checks"].values()):
            raise RuntimeError("Exact equation control failed")
        hamiltonian = hamiltonian_directional_check()
        result["hamiltonian_directional_check"] = hamiltonian
        if not hamiltonian["passed"]:
            raise RuntimeError("Independent ADM Hamiltonian check failed")
        print("Recomputing original W65 anchor", file=sys.stderr, flush=True)
        mod65, mod64, solution, anchor, actual = background()
        result.update(anchor=anchor, dependency_hashes=actual)
        if args.source_feedback_only:
            result["kinetic_feedback"] = kinetic_feedback_check(mod64, solution)
            passed = all(result["kinetic_feedback"]["gates"].values())
            result["status"] = "FIXED_PROFILE_KINETIC_FEEDBACK_PASS" if passed else "OPEN"
        elif args.compact_refinement_case:
            if args.epsilon not in (0.0, 0.002, -0.002):
                raise ValueError("Specify registered --epsilon 0, 0.002 or -0.002.")
            solution, compact_info = compact_background(mod65, mod64, solution)
            result["compact_background"] = compact_info
            result["refinement_cases"] = {}
            for h in (0.025, 0.0125):
                case = run_case(solution, mod64, h=h, epsilon=args.epsilon,
                                duration=256.0, radius=160.0)
                announce(case)
                result["refinement_cases"][str(h)] = case
            passed = all(all(case["gates"].values())
                for case in result["refinement_cases"].values())
            result["status"] = "REFINEMENT_CASES_ONLY" if passed else "OPEN"
            result["resolution_requires_matching_zero_and_signed_cases"] = True
        elif args.compact_suite:
            print("Continuing to registered compact stable core", file=sys.stderr, flush=True)
            solution, compact_info = compact_background(mod65, mod64, solution)
            result["compact_background"] = compact_info
            result["suite"] = suite(mod65, mod64, solution,
                reference_f0=2.168601437933647, radius=160.0, domain_radius=200.0,
                duration=256.0, kick=0.002, require_resolved=True)
            passed = all(result["suite"]["gates"].values())
            result["status"] = "BOUNDED_COMPACT_NONLINEAR_RESPONSE_PASS" if passed else "OPEN"
        elif args.pilot or args.run_case:
            if args.radius != 80:
                solution = mod65.solve_at(mod64, F0, solution, radius=args.radius)
            case = run_case(solution, mod64, h=args.h, epsilon=args.epsilon,
                            duration=12.0 if args.pilot else args.T,
                            radius=args.radius, courant=args.courant)
            announce(case)
            result["case"] = case
            passed = all(case["gates"].values())
            result["status"] = "PILOT_ONLY" if args.pilot and passed else "BOUNDED_CASE_PASS" if passed else "OPEN"
        else:
            result["suite"] = suite(mod65, mod64, solution)
            passed = all(result["suite"]["gates"].values())
            result["status"] = "BOUNDED_NONLINEAR_RESPONSE_PASS" if passed else "OPEN"
        unchanged = actual == {p:sha(SF/p) for p in PINS}
        result["upstream_files_unchanged"] = unchanged
        if not unchanged:
            passed = False
            result["status"] = "DEPENDENCY_FAILURE"
        result["scope"] = dict(new_action=False, asymptotic_relaxation_proved=False,
            universal_nonlinear_stability=False, finite_mass_cap=False,
            foundation_pressure_closure=False, black_hole=False,
            exact_semidiscrete_charge=True, exactly_charge_preserving_RK4=False)
        result["versions"] = dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__)
    except Exception as exc:
        passed = False
        result.update(status="OPEN_EXECUTION_FAILURE", error=type(exc).__name__+": "+str(exc))
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
