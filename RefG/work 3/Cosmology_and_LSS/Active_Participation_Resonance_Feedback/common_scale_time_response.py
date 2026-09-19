"""Frozen weak-field time test of the NEW scalar composite-metric candidate.

Registered before execution: alpha=.003; R=60; dr=.12,.06,.03; RK4
dt=.2 dr; T=24; samples every .12; equilibrium and perturbed controls.
The perturbation is delta_u=.005 inside r=8, C2 tapered to zero at r=12.
All initial fields/cadence follow the common rescaling in the inner region;
one declared initial phase-momentum normalization preserves discrete Q.

Thresholds: |u|<.1, relative charge drift<1e-7, energy drift<1e-6;
medium/fine core pressure and charge-radius differences<2e-3 relative;
baseline-subtracted response differences decrease on refinement unless
both are below 1e-10 absolute. A restoring turn is reported only if found
within the frozen T=24, never manufactured by damping or extending time.

The conservative radial finite-volume system follows one discrete
Hamiltonian, including its outer Robin energy. This is a local test of
the candidate, not an EH calculation, strong-field run or no-zero proof.
H_u is the u-field kinetic/gradient response energy; no independent
stored background-tension energy U_tension(P_F) has been derived here.
No output files or caches are written; stdout contains the result.

Diagnostic extension after the first frozen run: central phase cadence,
local clock integral, sector-energy exchange and resolution-qualified turn
times. These add no success gate and change no evolution or frozen threshold.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import platform
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np
from scipy.integrate import simpson
from scipy.signal import find_peaks

HERE = Path(__file__).resolve().parent
SOURCE = Path(__file__).resolve()
CANDIDATE = HERE / "common_scale_finite_source_candidate.py"
CANDIDATE_HASH = "6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8"
ALPHA = 0.003
RADIUS = 60.0
SPACINGS = (0.12, 0.06, 0.03)
END_TIME = 24.0
SAMPLE_DT = 0.12
EPSILON = 0.005
MAX_WALL_SECONDS = 240.0


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class RadialHamiltonian:
    """Cell volume weights, shared positive gradient form, natural centre."""

    def __init__(self, spacing):
        self.cells = int(round(RADIUS/spacing))
        self.dr = RADIUS/self.cells
        faces = np.arange(self.cells+1)*self.dr
        self.r = (np.arange(self.cells)+0.5)*self.dr
        self.volume = (faces[1:]**3-faces[:-1]**3)/3
        self.conductance = faces[1:-1]**2/self.dr
        # Eliminate the boundary trace: half-cell spring in series with
        # the exact exterior energy R u(R)^2/(2 alpha).
        half_cell = RADIUS**2/(self.dr/2)
        self.boundary_u = half_cell*RADIUS/(half_cell+RADIUS)
        self.boundary_matter = half_cell

    @staticmethod
    def potential(s):
        return s/2-s*s/4+s*s*s/24

    def laplace(self, value, boundary):
        flux = self.conductance*(value[1:]-value[:-1])
        divergence = np.empty_like(value)
        divergence[0] = flux[0]
        divergence[1:-1] = flux[1:]-flux[:-1]
        divergence[-1] = -boundary*value[-1]-flux[-1]
        return divergence/self.volume

    def gradient_energy(self, value, boundary):
        return 0.5*(
            np.dot(self.conductance, np.diff(value)**2)
            + boundary*value[-1]**2
        )

    def gradient_energy_rate(self, value, velocity, boundary):
        return (
            np.dot(self.conductance, np.diff(value)*np.diff(velocity))
            + boundary*value[-1]*velocity[-1]
        )

    def rhs(self, state):
        u, a, b, pu, pa, pb = state
        e2 = np.exp(2*u)
        e_minus4 = 1/(e2*e2)
        modulus = a*a+b*b
        v = self.potential(modulus)
        derivative = 1-modulus+modulus*modulus/4
        velocities_u = ALPHA*e_minus4*pu
        velocities_a = e_minus4*pa
        velocities_b = e_minus4*pb
        return np.vstack((
            velocities_u, velocities_a, velocities_b,
            self.laplace(u, self.boundary_u)/ALPHA
            + 2*e_minus4*(ALPHA*pu*pu+pa*pa+pb*pb)-2*e2*v,
            self.laplace(a, self.boundary_matter)-e2*a*derivative,
            self.laplace(b, self.boundary_matter)-e2*b*derivative,
        ))

    def observables(self, state, actual_time):
        u, a, b, pu, pa, pb = state
        flow = self.rhs(state)
        ut, at, bt, put, pat, pbt = flow
        e2, p = np.exp(2*u), np.exp(-u)
        e_minus4 = 1/(e2*e2)
        density_q = a*pb-b*pa
        charge = float(4*np.pi*np.dot(self.volume, density_q))
        charge_dot = float(4*np.pi*np.dot(
            self.volume, at*pb+a*pbt-bt*pa-b*pat
        ))
        radius_q = math.sqrt(float(
            4*np.pi*np.dot(self.volume*self.r**2, density_q)/charge
        ))
        v = self.potential(a*a+b*b)
        potential_factor = 1-(a*a+b*b)+(a*a+b*b)**2/4
        energy_u = float(4*np.pi*(
            np.dot(self.volume, ALPHA*e_minus4*pu*pu/2)
            + self.gradient_energy(u, self.boundary_u)/ALPHA
        ))
        energy_matter = float(4*np.pi*(
            np.dot(self.volume, e_minus4*(pa*pa+pb*pb)/2+e2*v)
            + self.gradient_energy(a, self.boundary_matter)
            + self.gradient_energy(b, self.boundary_matter)
        ))
        # Cellwise p_tt from two independent forms of the SAME discrete PDE.
        utt = ALPHA*e_minus4*put-4*ut*ut
        ptt_direct = p*(ut*ut-utt)
        budget = np.vstack((
            -p**5*self.laplace(u, self.boundary_u),
            3*p*ut*ut,
            -2*ALPHA*p*(at*at+bt*bt),
            2*ALPHA*p**3*v,
        ))
        residual = ptt_direct-np.sum(budget, axis=0)
        # Even quadratic extrapolation is diagnostic only; evolution remains
        # cell-centred with its natural zero-area central flux.
        centre_u = float((9*u[0]-u[1])/8)
        centre_ut = float((9*ut[0]-ut[1])/8)
        centre_p = math.exp(-centre_u)
        centre_modulus = a[:2]**2+b[:2]**2
        if np.any(centre_modulus <= 1e-20):
            raise FloatingPointError("Central phase cadence undefined at a field zero")
        frequency_cells = (a[:2]*bt[:2]-b[:2]*at[:2])/centre_modulus
        centre_frequency = float((9*frequency_cells[0]-frequency_cells[1])/8)
        exchange = float(4*np.pi*np.dot(
            self.volume, 2*ut*(e_minus4*(pa*pa+pb*pb)-e2*v)
        ))
        response_rate = float(4*np.pi*(
            np.dot(self.volume,
                   -2*ALPHA*e_minus4*pu*pu*ut + ALPHA*e_minus4*pu*put)
            + self.gradient_energy_rate(u, ut, self.boundary_u)/ALPHA
        ))
        matter_rate = float(4*np.pi*(
            np.dot(self.volume,
                   e_minus4*(pa*pat+pb*pbt)
                   -2*e_minus4*(pa*pa+pb*pb)*ut
                   +2*e2*v*ut + e2*potential_factor*(a*at+b*bt))
            + self.gradient_energy_rate(a, at, self.boundary_matter)
            + self.gradient_energy_rate(b, bt, self.boundary_matter)
        ))
        negative_charge = float(4*np.pi*np.dot(
            self.volume, np.maximum(-density_q, 0)
        ))
        return {
            "time": actual_time, "central_p": centre_p,
            "central_p_t": -centre_p*centre_ut,
            "central_coordinate_phase_cadence": centre_frequency,
            "central_local_phase_cadence": centre_frequency/centre_p,
            "charge_radius": radius_q,
            "charge": charge, "charge_dot": charge_dot,
            "minimum_charge_density": float(np.min(density_q)),
            "integrated_negative_charge_fraction": negative_charge/abs(charge),
            "energy": energy_u+energy_matter,
            "energy_scale_response": energy_u, "energy_matter": energy_matter,
            "maximum_abs_u": float(np.max(np.abs(u))),
            "minimum_p": float(np.min(p)),
            "acceleration_budget_max_residual": float(np.max(np.abs(residual))),
            "first_cell_pressure_acceleration": float(ptt_direct[0]),
            "first_cell_budget_terms": budget[:, 0].tolist(),
            "core_u_momentum_max": float(np.max(np.abs(ut[self.r<12]))),
            "energy_exchange_to_scale_response": exchange,
            "scale_response_energy_rate_from_discrete_H": response_rate,
            "matter_energy_rate_from_discrete_H": matter_rate,
            "sector_exchange_identity_residual": max(
                abs(response_rate-exchange), abs(matter_rate+exchange)
            ),
        }


def equilibrium():
    if digest(CANDIDATE) != CANDIDATE_HASH:
        raise RuntimeError("Frozen scalar candidate source changed")
    candidate = load_module("common_scale_finite_source_for_time", CANDIDATE)
    if candidate.digest(candidate.W58) != candidate.W58_SHA256:
        raise RuntimeError("Frozen W58 source changed")
    w58 = load_module("w58_for_time_no_write", candidate.W58)
    reference = w58.solve_profile(0.8, radius=80, tolerance=1e-8)
    x = np.linspace(0, 80, 24001)
    f = reference.sol(x)[0]
    charge = float(4*np.pi*0.8*simpson(x*x*f*f, x=x))
    weak = candidate.coupled_profile(
        reference, charge, 0.001, RADIUS, 3e-8
    )
    solution = candidate.coupled_profile(
        reference, charge, ALPHA, RADIUS, 3e-8, previous=weak
    )
    return solution, charge


def initial_state(model, solution, perturbed):
    r = model.r
    omega = float(solution.p[0])
    f_eq, _, u_eq, _, _ = solution.sol(r)
    zero = np.zeros_like(r)
    base_pb = np.exp(4*u_eq)*omega*f_eq
    discrete_charge = float(4*np.pi*np.dot(model.volume, f_eq*base_pb))
    if not perturbed:
        return np.vstack((u_eq, f_eq, zero, zero, zero, base_pb)), {
            "initial_discrete_charge": discrete_charge,
            "phase_momentum_charge_factor": 1.0,
            "maximum_common_scale_shift": 0.0,
        }
    z = np.clip((r-8)/4, 0, 1)
    bump = 1-10*z**3+15*z**4-6*z**5
    delta = EPSILON*bump
    mapped_r = r*np.exp(delta)
    f, _, mapped_u, _, _ = solution.sol(mapped_r)
    u = mapped_u+delta
    pb = np.exp(4*u)*omega*np.exp(-delta)*f
    trial_charge = float(4*np.pi*np.dot(model.volume, f*pb))
    correction = discrete_charge/trial_charge
    pb *= correction
    return np.vstack((u, f, zero, zero, zero, pb)), {
        "initial_discrete_charge": discrete_charge,
        "phase_momentum_charge_factor": correction,
        "charge_correction_minus_one": correction-1,
        "maximum_common_scale_shift": float(np.max(delta)),
        "taper": "C2 quintic from r=8 to r=12",
        "meaning": "finite physical common-scale perturbation with taper; not global symmetry",
    }


def evolve(model, solution, perturbed, started):
    state, initial_info = initial_state(model, solution, perturbed)
    step = 0.2*model.dr
    steps = int(round(END_TIME/step))
    sample_steps = int(round(SAMPLE_DT/step))
    history = []
    for iteration in range(steps+1):
        if iteration % sample_steps == 0:
            history.append(model.observables(state, iteration*step))
            history[-1]["central_tau"] = (
                0.0 if len(history) == 1 else
                history[-2]["central_tau"]
                + (history[-1]["time"]-history[-2]["time"])
                * (history[-1]["central_p"]+history[-2]["central_p"])/2
            )
            if history[-1]["maximum_abs_u"] >= 0.1:
                raise RuntimeError("Frozen weak-field guard |u|<.1 failed")
            if time.monotonic()-started > MAX_WALL_SECONDS:
                raise TimeoutError("Frozen 240-second execution bound exceeded")
        if iteration == steps:
            break
        k1 = model.rhs(state)
        k2 = model.rhs(state+step*k1/2)
        k3 = model.rhs(state+step*k2/2)
        k4 = model.rhs(state+step*k3)
        state += step*(k1+2*k2+2*k3+k4)/6
        if not np.all(np.isfinite(state)):
            raise FloatingPointError("Nonfinite state in frozen evolution")
    e0, q0 = history[0]["energy"], history[0]["charge"]
    summary = {
        "dr": model.dr, "dt": step, "cells": model.cells,
        "perturbed": perturbed, "initialization": initial_info,
        "energy_initial": e0, "charge_initial": q0,
        "energy_relative_drift": max(abs(row["energy"]/e0-1) for row in history),
        "charge_relative_drift": max(abs(row["charge"]/q0-1) for row in history),
        "maximum_abs_u": max(row["maximum_abs_u"] for row in history),
        "minimum_p": min(row["minimum_p"] for row in history),
        "maximum_charge_rhs_relative": max(abs(row["charge_dot"]/q0) for row in history),
        "maximum_pressure_acceleration_budget_residual": max(
            row["acceleration_budget_max_residual"] for row in history
        ),
        "maximum_sector_exchange_identity_residual": max(
            row["sector_exchange_identity_residual"] for row in history
        ),
        "minimum_charge_density": min(row["minimum_charge_density"] for row in history),
        "maximum_negative_charge_fraction": max(
            row["integrated_negative_charge_fraction"] for row in history
        ),
        "final": history[-1],
    }
    return summary, history


def response(control, perturbed):
    values = []
    for baseline, physical in zip(control, perturbed):
        values.append((
            physical["time"],
            physical["central_p"]-baseline["central_p"],
            physical["charge_radius"]-baseline["charge_radius"],
            physical["central_p_t"]-baseline["central_p_t"],
        ))
    return np.array(values)


def event_summary(series, pressure_error, radius_error):
    # A central-pressure return is read directly from the baseline-subtracted
    # trace. Radius is independently monitored, not presumed equivalent.
    t, dp, dr, dpt = series.T
    selected = [0, len(t)//4, len(t)//2, 3*len(t)//4, len(t)-1]
    radius_slope = np.gradient(dr, t)
    def extrema(values, error):
        high = find_peaks(values, prominence=2*error)[0]
        low = find_peaks(-values, prominence=2*error)[0]
        return np.sort(np.concatenate((high, low)))
    pressure_extrema = extrema(dp, pressure_error)
    radius_extrema = extrema(dr, radius_error)
    pressure_cross = np.flatnonzero(dp[:-1]*dp[1:] < 0)+1
    radius_cross = np.flatnonzero(dr[:-1]*dr[1:] < 0)+1
    return {
        "selected_baseline_subtracted_rows": series[selected].tolist(),
        "central_pressure_min_max": [float(np.min(dp)), float(np.max(dp))],
        "charge_radius_min_max": [float(np.min(dr)), float(np.max(dr))],
        "central_pressure_turn_times_sampled": t[pressure_extrema].tolist(),
        "radius_turn_times_sampled": t[radius_extrema].tolist(),
        "central_pressure_crossing_times_sampled": t[pressure_cross].tolist(),
        "radius_crossing_times_sampled": t[radius_cross].tolist(),
        "turn_diagnostic_prominence_thresholds": {
            "central_p": 2*pressure_error, "charge_radius": 2*radius_error,
            "rule": "twice measured medium-fine response error; diagnostic only",
        },
        "central_pressure_restoring_motion_seen": bool(
            np.any((dp*dp[0] > 0) & (dp*dpt < -1e-10))
        ),
        "radius_restoring_motion_seen": bool(
            np.any((dr*dr[0] > 0) & (dr*radius_slope < -1e-10))
        ),
        "sampling_time_uncertainty": SAMPLE_DT,
        "pressure_spike_interpretation": "inward spherical pulse from finite taper, not a pure normal mode",
        "final_relaxation_claimed": False,
    }


def independent_hamiltonian_crosscheck():
    """Post-run implementation audit; no evolution or physical threshold fit.

    A deterministic off-shell direction differentiates the actual Hamiltonian
    by finite differences, independently of the formula used in rhs().
    Nonzero outer field values exercise the boundary energy as well.
    """
    model = RadialHamiltonian(0.12)
    z = np.exp(-model.r**2/16)
    state = np.vstack((
        .001+.02*z, .0001+1.3*z, .0002+.1*z,
        .002*z, .1*z, .8*z,
    ))
    direction = np.random.default_rng(73421).standard_normal(state.shape)
    direction /= np.linalg.norm(direction)
    flow = model.rhs(state)
    canonical = float(4*np.pi*np.sum(model.volume*(
        -np.sum(flow[3:]*direction[:3], axis=0)
        + np.sum(flow[:3]*direction[3:], axis=0)
    )))
    rows = []
    for step in (1e-4, 1e-5, 1e-6):
        plus = model.observables(state+step*direction, 0)["energy"]
        minus = model.observables(state-step*direction, 0)["energy"]
        derivative = (plus-minus)/(2*step)
        rows.append({
            "step": step, "energy_finite_difference": derivative,
            "canonical_directional_derivative": canonical,
            "relative_error": abs(derivative-canonical)/max(1, abs(canonical)),
        })
    return {
        "passed": min(row["relative_error"] for row in rows) < 1e-7,
        "rows": rows, "random_seed": 73421,
        "scope": "independent discrete Hamiltonian/RHS audit, added after first dynamics run",
    }


def run():
    started = time.monotonic()
    solution, continuum_charge = equilibrium()
    runs, traces, raw_histories = [], {}, {}
    for spacing in SPACINGS:
        model = RadialHamiltonian(spacing)
        control_summary, control = evolve(model, solution, False, started)
        pert_summary, pert = evolve(model, solution, True, started)
        runs.extend((control_summary, pert_summary))
        traces[spacing] = response(control, pert)
        raw_histories[spacing] = (control, pert)
    checks = {}
    for row in runs:
        key = f"dr{row['dr']:g}_" + ("perturbed" if row["perturbed"] else "control")
        checks[key+"_energy"] = row["energy_relative_drift"] < 1e-6
        checks[key+"_charge"] = row["charge_relative_drift"] < 1e-7
        checks[key+"_weak_regular"] = row["maximum_abs_u"] < 0.1
        checks[key+"_actual_pressure_equation_budget"] = (
            row["maximum_pressure_acceleration_budget_residual"] < 1e-11
        )
    changes = {}
    for key, column in (("central_p", 1), ("charge_radius", 2)):
        coarse = float(np.max(np.abs(traces[SPACINGS[0]][:, column]-traces[SPACINGS[1]][:, column])))
        fine = float(np.max(np.abs(traces[SPACINGS[1]][:, column]-traces[SPACINGS[2]][:, column])))
        medium_pert = np.array([row[key] for row in raw_histories[SPACINGS[1]][1]])
        fine_pert = np.array([row[key] for row in raw_histories[SPACINGS[2]][1]])
        absolute = float(np.max(np.abs(medium_pert-fine_pert)))
        relative = absolute/max(float(np.max(np.abs(fine_pert))), 1e-30)
        changes[key] = {
            "coarse_medium_response_max_abs": coarse,
            "medium_fine_response_max_abs": fine,
            "response_difference_ratio": coarse/max(fine, 1e-30),
            "medium_fine_raw_max_abs": absolute,
            "medium_fine_raw_relative": relative,
        }
        checks[key+"_response_refines"] = fine < coarse or max(coarse, fine) < 1e-10
        checks[key+"_medium_fine_agreement"] = relative < 2e-3
    fine_series = traces[SPACINGS[-1]]
    events = event_summary(
        fine_series, changes["central_p"]["medium_fine_response_max_abs"],
        changes["charge_radius"]["medium_fine_response_max_abs"],
    )
    fine_control, fine_pert = raw_histories[SPACINGS[-1]]
    checkpoints = [0, 50, 100, 150, 200]
    budgets = [
        {
            "time": fine_pert[i]["time"],
            "p_tt_first_cell": fine_pert[i]["first_cell_pressure_acceleration"],
            "terms": fine_pert[i]["first_cell_budget_terms"],
            "energy_scale_response": fine_pert[i]["energy_scale_response"],
            "energy_matter": fine_pert[i]["energy_matter"],
            "exchange_to_scale_response": fine_pert[i]["energy_exchange_to_scale_response"],
            "scale_response_energy_rate": fine_pert[i]["scale_response_energy_rate_from_discrete_H"],
            "matter_energy_rate": fine_pert[i]["matter_energy_rate_from_discrete_H"],
            "central_p": fine_pert[i]["central_p"],
            "central_tau": fine_pert[i]["central_tau"],
            "central_coordinate_phase_cadence": fine_pert[i]["central_coordinate_phase_cadence"],
            "central_local_phase_cadence": fine_pert[i]["central_local_phase_cadence"],
        }
        for i in checkpoints
    ]
    checks["source_candidate_unchanged"] = digest(CANDIDATE) == CANDIDATE_HASH
    crosscheck = independent_hamiltonian_crosscheck()
    passed = all(checks.values()) and crosscheck["passed"]
    return {
        "claim": "COMMON_SCALE_WEAK_TIME_RESPONSE_V1",
        "passed": passed,
        "status": "FINITE_TIME_NUMERICAL_RESPONSE_PASS" if passed else "FROZEN_NUMERICAL_GATE_FAILED",
        "checks": checks,
        "independent_hamiltonian_crosscheck": crosscheck,
        "configuration": {
            "alpha": ALPHA, "R": RADIUS, "spacings": SPACINGS,
            "T": END_TIME, "epsilon": EPSILON, "sample_dt": SAMPLE_DT,
            "continuum_equilibrium_charge": continuum_charge,
            "equilibrium_omega": float(solution.p[0]),
            "no_added_damping": True,
            "boundary": "conservative matter Dirichlet and scalar Robin, natural centre",
            "boundary_distance_from_perturbation": RADIUS-12,
            "boundary_return_cannot_reach_core_by_T": True,
        },
        "runs": runs,
        "refinement": changes,
        "fine_response_events": events,
        "pressure_budget_terms": [
            "-p^5 discrete_Laplacian(u)", "3p u_t^2",
            "-2alpha p |psi_t|^2", "2alpha p^3 V",
        ],
        "fine_actual_source_energy_budget_samples": budgets,
        "response_trace_columns": ["t", "delta_central_p", "delta_charge_radius", "delta_central_p_t"],
        "fine_baseline_subtracted_response": fine_series.tolist(),
        "scope": {
            "new_scalar_candidate_only": True, "full_RefG_or_EH_completion": False,
            "stored_background_tension_energy_derived": False,
            "energy_scale_response_meaning": "u-field kinetic/gradient energy, not P_F or stored static tension",
            "global_no_zero_pressure_proof": False, "strong_field_calculation": False,
            "final_damping_or_equilibrium_proved": False, "observational_pass": False,
            "restoring_motion_is_measured_not_imposed": True,
            "writes_files": False,
        },
        "provenance": {
            "script_sha256": digest(SOURCE), "candidate_sha256": digest(CANDIDATE),
            "python": platform.python_version(), "numpy": np.__version__,
            "elapsed_seconds": time.monotonic()-started,
        },
    }


if __name__ == "__main__":
    try:
        report = run()
    except Exception as error:
        report = {
            "passed": False, "status": "EXECUTION_FAILED",
            "error_type": type(error).__name__, "error": str(error),
            "writes_files": False,
        }
    print(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False))
    raise SystemExit(0 if report["passed"] else 1)
