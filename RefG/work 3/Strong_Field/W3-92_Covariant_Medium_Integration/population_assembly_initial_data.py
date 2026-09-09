"""Bounded same-field assembly, initial-response and equilibrium diagnostics.

Default assembly and response modes do not establish stationary equilibria.
The aggregate-equilibrium mode separately solves retained spherical equations
at fixed total Noether charge; its n counts separated reference objects only.
No mode establishes a black hole or removal of a spacetime singularity.
Only stdout is produced. Original W65 backgrounds are recomputed and pinned.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
sys.dont_write_bytecode = True

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import CubicSpline, PchipInterpolator, RegularGridInterpolator
from scipy.signal import find_peaks
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import splu

HERE = Path(__file__).resolve().parent
ALPHA, SEXTIC = 0.04, 0.25
NUMERICAL_CONTRACT = {
    "outer_max": 32, "inner_max": 120, "psi_relaxation": 0.55,
    "background_relaxation": 0.5, "inner_update_tolerance": 1e-10,
    "outer_background_tolerance": 2e-8,
    "discrete_residual_tolerance": 5e-7,
    "charge_preparation_tolerance": 1e-10,
    "pilot_anchor_relative_tolerance": 0.03,
    "pilot_independent_flux_relative_tolerance": 0.03,
    "pilot_is_continuum_verification": False,
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_background():
    path = HERE / "nonlinear_equilibrium_evolution.py"
    before = sha(path)
    spec = importlib.util.spec_from_file_location("w92_population_background", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    mod65, mod64, solution, anchor, pins = module.background()
    return module, mod65, mod64, solution, anchor, pins, before


class IsolatedCore:
    def __init__(self, mod64, solution, anchor):
        rmax = float(solution.x[-1])
        r = np.linspace(0, rmax, 32001)
        f, fp, mass, logsigma = solution.sol(np.maximum(r, mod64.EPS))
        mass[0], fp[0] = 0.0, 0.0
        N = np.ones_like(r)
        N[1:] = 1-2*ALPHA*mass[1:]/r[1:]
        if np.min(N) <= 0:
            raise ValueError("Anchor is outside the regular isotropic map")
        self.mass = float(mass[-1])
        self.omega = float(mod64.omega_from_parameter(solution.p))
        g = np.zeros_like(r)
        g[1:] = (1/np.sqrt(N[1:])-1)/r[1:]
        integral = cumulative_trapezoid(g, r, initial=0.0)
        m = ALPHA*self.mass
        iso_max = (rmax-m+np.sqrt(rmax*(rmax-2*m)))/2
        q = np.log(iso_max/rmax)-(integral[-1]-integral)
        isotropic = r*np.exp(q)
        psi = np.exp(-q/2)
        lapse = np.exp(logsigma)*np.sqrt(N)
        proper_momentum = self.omega*f/lapse
        self.psi0, self.lapse0, self.f0 = map(float, (psi[0], lapse[0], f[0]))
        self.iso_max = float(iso_max)
        outer_isotropic_derivative = float(fp[-1]*rmax*np.sqrt(N[-1])/iso_max)
        self.f = CubicSpline(isotropic, f, bc_type=((1, 0.0), (1, outer_isotropic_derivative)))
        self.pi = PchipInterpolator(isotropic, proper_momentum, extrapolate=False)
        self.psi = PchipInterpolator(isotropic, psi, extrapolate=False)
        self.lapse = PchipInterpolator(isotropic, lapse, extrapolate=False)
        # Q convention factors out 4 pi, as in W65.
        charge_radial = isotropic**2*psi**6*f*proper_momentum
        cum = cumulative_trapezoid(charge_radial, isotropic, initial=0.0)
        self.mapping_charge = float(cum[-1])
        self.charge = float(anchor["record"]["charge"])
        self.r90 = float(np.interp(0.9*cum[-1], cum, isotropic))
        self.coordinate_rms = float(np.sqrt(np.trapz(
            charge_radial*isotropic**2, isotropic)/cum[-1]))
        self.mapping = {
            "areal_boundary": rmax, "isotropic_boundary": self.iso_max,
            "radial_samples": len(r), "tail_boundary_assumption": "vacuum Schwarzschild",
            "charge": self.charge, "mapping_integrated_charge": self.mapping_charge,
            "mapping_charge_relative_error": abs(self.mapping_charge/self.charge-1),
            "ADM_mass": self.mass,
            "psi_centre": self.psi0, "lapse_centre": self.lapse0,
            "f_centre": self.f0, "coordinate_charge_rms": self.coordinate_rms,
            "coordinate_charge_r90": self.r90,
        }

    def evaluate(self, x):
        x = np.asarray(x)
        cut = np.minimum(x, self.iso_max)
        inside = x < self.iso_max
        f = np.where(inside, self.f(cut), 0.0)
        df = np.where(inside, self.f(cut, 1), 0.0)
        pi = np.where(inside, self.pi(cut), 0.0)
        psi = np.where(inside, self.psi(cut),
                       1+ALPHA*self.mass/(2*np.maximum(x, self.iso_max)))
        lapse = np.where(inside, self.lapse(cut),
                         (2*psi-psi**2)/psi**2)
        return f, df, pi, psi, lapse


class CylindricalGrid:
    """Cell-centred conservative flat cylindrical Laplacian, full signed z."""
    def __init__(self, radius, half_height, h):
        self.radius, self.half_height, self.h = map(float, (radius, half_height, h))
        self.nr, self.nz = round(radius/h), round(2*half_height/h)
        if min(self.nr, self.nz) < 8 or max(
                abs(self.nr*h-radius), abs(self.nz*h-2*half_height)) > 1e-10:
            raise ValueError("Domain boundaries must be integer cell multiples")
        self.r = (np.arange(self.nr)+0.5)*h
        self.z = -half_height+(np.arange(self.nz)+0.5)*h
        self.R, self.Z = np.meshgrid(self.r, self.z, indexing="ij")
        self.dv = 2*np.pi*self.R*h*h
        rows, cols, data = [], [], []
        for i in range(self.nr):
            for j in range(self.nz):
                k = i*self.nz+j
                diagonal = 0.0
                left = i*h/self.r[i]/h**2
                right = (i+1)*h/self.r[i]/h**2
                for ni, coefficient in ((i-1, left), (i+1, right)):
                    if 0 <= ni < self.nr:
                        rows.append(k); cols.append(ni*self.nz+j); data.append(coefficient)
                        diagonal -= coefficient
                    elif ni == self.nr:
                        diagonal -= 2*coefficient
                for nj in (j-1, j+1):
                    if 0 <= nj < self.nz:
                        rows.append(k); cols.append(i*self.nz+nj); data.append(1/h**2)
                        diagonal -= 1/h**2
                    else:
                        diagonal -= 2/h**2
                rows.append(k); cols.append(k); data.append(diagonal)
        self.L = coo_matrix((data, (rows, cols)), shape=(self.nr*self.nz,)*2).tocsc()
        self.factor = splu(self.L)
        self.bc_one = self.boundary_force(lambda r, z: np.ones(np.broadcast(r, z).shape))
        self.bc_inv_radius = self.boundary_force(lambda r, z: 1/np.sqrt(r*r+z*z))

    def boundary_force(self, function):
        force = np.zeros((self.nr, self.nz))
        force[-1] += 2*self.radius/self.r[-1]/self.h**2*function(self.radius, self.z)
        force[:, 0] += 2/self.h**2*function(self.r, -self.half_height)
        force[:, -1] += 2/self.h**2*function(self.r, self.half_height)
        return force

    def integral(self, value):
        return float(np.sum(self.dv*value))

    def axis_values(self, value):
        return (9*value[0]-value[1])/8

    def centre_values(self, value, centres):
        return CubicSpline(self.z, self.axis_values(value), extrapolate=False)(centres)

    def solve_poisson(self, source, monopole):
        rhs = -source-self.bc_one-monopole*self.bc_inv_radius
        return self.factor.solve(rhs.ravel()).reshape(self.R.shape)

    def independent_surface_flux(self, value, monopole):
        # Quadratic boundary derivative, independent of the production half-cell stencil.
        h = self.h
        bc_r = 1+monopole/np.sqrt(self.radius**2+self.z**2)
        bc_z = 1+monopole/np.sqrt(self.r**2+self.half_height**2)
        dr = (8*bc_r/3-3*value[-1]+value[-2]/3)/h
        dz_up = (8*bc_z/3-3*value[:, -1]+value[:, -2]/3)/h
        dz_down = (8*bc_z/3-3*value[:, 0]+value[:, 1]/3)/h
        return float(2*np.pi*self.radius*h*np.sum(dr)
                     +2*np.pi*h*np.sum(self.r*(dz_up+dz_down)))

    def independent_interior_residual(self, value, signed_source):
        """Fourth-order differential stencil, excluding axis/boundary layers."""
        h = self.h
        middle = value[2:-2, 2:-2]
        dr = (value[:-4, 2:-2]-8*value[1:-3, 2:-2]+8*value[3:-1, 2:-2]-value[4:, 2:-2])/(12*h)
        drr = (-value[:-4, 2:-2]+16*value[1:-3, 2:-2]-30*middle+
               16*value[3:-1, 2:-2]-value[4:, 2:-2])/(12*h*h)
        dzz = (-value[2:-2, :-4]+16*value[2:-2, 1:-3]-30*middle+
               16*value[2:-2, 3:-1]-value[2:-2, 4:])/(12*h*h)
        residual = drr+dr/self.R[2:-2, 2:-2]+dzz+signed_source[2:-2, 2:-2]
        normalization = max(float(np.max(abs(signed_source))), 1e-14)
        return float(np.max(abs(residual))/normalization)


def prepare(grid, core, centres, factors):
    pieces, derivatives_r, derivatives_z, momenta = [], [], [], []
    for centre, b in zip(centres, factors):
        dz = grid.Z-centre
        distance = np.sqrt(grid.R**2+dz**2)
        f, df, pi, psiself, _ = core.evaluate(b*b*distance)
        pieces.append(f)
        derivatives_r.append(df*b*b*grid.R/distance)
        derivatives_z.append(df*b*b*dz/distance)
        # Fixed conformal canonical density during the inner elliptic solve.
        momenta.append(b**6*psiself**6*pi)
    phi = np.sum(pieces, axis=0)
    normalizations = []
    for i in range(len(momenta)):
        before = grid.integral(phi*momenta[i])/(4*np.pi)
        if before <= 0:
            raise FloatingPointError("Nonpositive prepared component charge")
        normalization = core.charge/before
        momenta[i] *= normalization
        normalizations.append(normalization)
    P = np.sum(momenta, axis=0)
    grad2 = np.sum(derivatives_r, axis=0)**2+np.sum(derivatives_z, axis=0)**2
    square = phi**2
    potential = square/2-square**2/4+SEXTIC*square**3/6
    return dict(phi=phi, P=P, Pi_components=tuple(momenta), pieces=tuple(pieces),
                grad2=grad2, potential=potential,
                charge_normalizations=normalizations)


def sources(psi, data):
    pi2 = data["P"]**2/psi**12
    spatial = data["grad2"]/psi**4
    density = (pi2+spatial)/2+data["potential"]
    stress_trace = 1.5*pi2-0.5*spatial-3*data["potential"]
    return density, stress_trace


def solve_hamiltonian(grid, psi, data):
    update = np.inf
    for iteration in range(1, NUMERICAL_CONTRACT["inner_max"]+1):
        density, _ = sources(psi, data)
        M = grid.integral(psi**5*density)/(4*np.pi)
        candidate = grid.solve_poisson(ALPHA/2*psi**5*density, ALPHA*M/2)
        if not np.all(np.isfinite(candidate)) or np.min(candidate) <= 0:
            raise FloatingPointError("Hamiltonian iteration left positive conformal branch")
        update = float(np.max(np.abs(candidate/psi-1)))
        psi = (1-NUMERICAL_CONTRACT["psi_relaxation"])*psi+NUMERICAL_CONTRACT["psi_relaxation"]*candidate
        if update < NUMERICAL_CONTRACT["inner_update_tolerance"]:
            return psi, iteration, update, True
    return psi, iteration, update, False


def solve_lapse(grid, psi, data):
    density, stress = sources(psi, data)
    coefficient = ALPHA/2*psi**4*(density+2*stress)
    operator = grid.L-diags(coefficient.ravel(), format="csc")
    factor = splu(operator)
    u = factor.solve(-grid.bc_one.ravel()).reshape(psi.shape)
    v = factor.solve(-grid.bc_inv_radius.ravel()).reshape(psi.shape)
    Iu = grid.integral(coefficient*u)/(4*np.pi)
    Iv = grid.integral(coefficient*v)/(4*np.pi)
    denominator = 1+Iv
    if abs(denominator) < 1e-9:
        raise FloatingPointError("Maximal-lapse boundary closure is degenerate")
    monopole = -Iu/denominator
    W = u+monopole*v
    residual = (grid.L@W.ravel()).reshape(W.shape)+grid.bc_one+monopole*grid.bc_inv_radius-coefficient*W
    return W/psi, W, monopole, coefficient, residual


def run_case(core, count=1, separation=28.0, h=0.5, radius=32.0, half_height=64.0, state_sink=None):
    grid = CylindricalGrid(radius, half_height, h)
    centres = (np.arange(count)-(count-1)/2)*separation
    if np.max(abs(centres))+3*core.r90 >= half_height:
        raise ValueError("Prepared cores too close to axial domain boundary")
    factors = np.ones(count)
    psi = np.ones_like(grid.R)
    for centre in centres:
        distance = np.sqrt(grid.R**2+(grid.Z-centre)**2)
        psi += core.evaluate(distance)[3]-1
    history, converged = [], False
    for outer in range(1, NUMERICAL_CONTRACT["outer_max"]+1):
        data = prepare(grid, core, centres, factors)
        psi, inner, update, inner_pass = solve_hamiltonian(grid, psi, data)
        new_factors = grid.centre_values(psi, centres)/core.psi0
        background_update = float(np.max(abs(new_factors/factors-1)))
        history.append(dict(outer=outer, inner=inner, inner_update=update,
                            background_update=background_update,
                            inner_converged=inner_pass))
        if not inner_pass:
            break
        if background_update < NUMERICAL_CONTRACT["outer_background_tolerance"]:
            converged = True
            break
        factors = ((1-NUMERICAL_CONTRACT["background_relaxation"])*factors+
                   NUMERICAL_CONTRACT["background_relaxation"]*new_factors)
    density, stress = sources(psi, data)
    M = grid.integral(psi**5*density)/(4*np.pi)
    source = ALPHA/2*psi**5*density
    residual = (grid.L@psi.ravel()).reshape(psi.shape)+grid.bc_one+ALPHA*M/2*grid.bc_inv_radius+source
    h_residual = float(np.max(abs(residual))/max(float(np.max(abs(source))), 1e-14))
    lapse, W, W_monopole, coefficient, lapse_residual = solve_lapse(grid, psi, data)
    l_residual = float(np.max(abs(lapse_residual))/max(float(np.max(abs(coefficient*W))), 1e-14))
    independent_h_residual = grid.independent_interior_residual(psi, source)
    independent_l_residual = grid.independent_interior_residual(W, -coefficient*W)
    M_flux = -grid.independent_surface_flux(psi, ALPHA*M/2)/(2*np.pi*ALPHA)
    lapse_centres = grid.centre_values(lapse, centres)
    psi_centres = grid.centre_values(psi, centres)
    phi_centres = grid.centre_values(data["phi"], centres)
    proper_pi_centres = grid.centre_values(data["P"]/psi**6, centres)
    nearest = np.argmin(abs(grid.Z[None, :, :]-centres[:, None, None]), axis=0)
    seed_path = np.linspace(0, core.coordinate_rms, 601)
    seed_proper_length = float(np.trapz(core.evaluate(seed_path)[3]**2, seed_path))
    regional_masses = []
    core_outputs = []
    for index, centre in enumerate(centres):
        charge_weight = data["phi"]*data["Pi_components"][index]
        Q = grid.integral(charge_weight)/(4*np.pi)
        coordinate_square = grid.R**2+(grid.Z-centre)**2
        coordinate_rms = np.sqrt(grid.integral(charge_weight*coordinate_square)/(4*np.pi*Q))
        # Variation of the inferred external conformal factor across a core.
        axis_psi = CubicSpline(grid.z, grid.axis_values(psi))
        psi_interpolator = RegularGridInterpolator((grid.r, grid.z), psi)
        variations, tidal_variations = {}, {}
        for name, reference_width in (("r90", core.r90), ("charge_rms", core.coordinate_rms)):
            width = reference_width/factors[index]**2
            ambient_samples = []
            for displacement in (-width, 0.0, width):
                selfpsi = float(core.evaluate(np.array(abs(displacement)*factors[index]**2))[3])
                ambient_samples.append(float(axis_psi(centre+displacement))/selfpsi)
            radial_selfpsi = float(core.evaluate(np.array(reference_width))[3])
            radial_sample = float(psi_interpolator([[width, centre]])[0])/radial_selfpsi
            variations[name] = float(max(abs(np.array(ambient_samples+[radial_sample])/ambient_samples[1]-1)))
            tidal_variations[name] = float(abs(ambient_samples[0]+ambient_samples[2]-2*ambient_samples[1])/ambient_samples[1])
        ambient_lapse = float(lapse_centres[index]/core.lapse0)
        width = core.coordinate_rms/factors[index]**2
        path = np.linspace(0, width, 601)
        axial_plus = float(np.trapz(axis_psi(centre+path)**2, path))
        axial_minus = float(np.trapz(axis_psi(centre-path)**2, path))
        radial_psi_at_z = CubicSpline(grid.z, psi, axis=1)(centre)
        radial_line = CubicSpline(np.r_[0.0, grid.r],
                                   np.r_[float(axis_psi(centre)), radial_psi_at_z],
                                   bc_type=((1, 0.0), "natural"))
        transverse = float(np.trapz(radial_line(path)**2, path))
        regional_mass = grid.integral(psi**5*density*(nearest==index))/(4*np.pi)
        regional_masses.append(regional_mass)
        core_outputs.append(dict(
            label=index, centre_z=float(centre), assigned_Q=core.charge, prepared_Q=Q,
            canonical_momentum_normalization=data["charge_normalizations"][index],
            ambient_psi=float(factors[index]),
            geometric_ambient_psi=float(psi_centres[index]/core.psi0),
            centre_lapse=float(lapse_centres[index]), ambient_lapse=ambient_lapse,
            prescribed_coordinate_size_factor=float(factors[index]**-2),
            coordinate_charge_rms=float(coordinate_rms),
            centre_converted_proper_rms_proxy=float(psi_centres[index]**2*coordinate_rms),
            intrinsic_seed_rms_region_proper_length=seed_proper_length,
            actual_proper_rms_region_length_axial_plus=axial_plus,
            actual_proper_rms_region_length_axial_minus=axial_minus,
            actual_proper_rms_region_length_transverse=transverse,
            proper_length_ratios_to_seed=[axial_plus/seed_proper_length,
                                         axial_minus/seed_proper_length,
                                         transverse/seed_proper_length],
            actual_centre_normal_momentum=float(proper_pi_centres[index]),
            normal_momentum_ratio_to_seed=float(proper_pi_centres[index]/(core.omega*core.f0/core.lapse0)),
            centre_amplitude_ratio_to_seed=float(phi_centres[index]/core.f0),
            instantaneous_proper_phase_rate_ratio_to_seed=float(
                (proper_pi_centres[index]/phi_centres[index])/(core.omega/core.lapse0)),
            voronoi_ADM_source_contribution=regional_mass,
            ambient_clock_times_spatial_factor=float(ambient_lapse*factors[index]**2),
            ambient_conformal_variation_across_r90=variations["r90"],
            ambient_conformal_variation_across_charge_rms=variations["charge_rms"],
            ambient_axial_second_difference_across_charge_rms=tidal_variations["charge_rms"]))
    diagonal_charge = sum(grid.integral(f*p)/(4*np.pi)
                          for f, p in zip(data["pieces"], data["Pi_components"]))
    Q_total = grid.integral(data["phi"]*data["P"])/(4*np.pi)
    axis_phi = grid.axis_values(data["phi"])
    peaks, _ = find_peaks(axis_phi, prominence=0.2*core.f0,
                         distance=max(1, int(0.6*separation/h)))
    charge_error = max(abs(item["prepared_Q"]/core.charge-1) for item in core_outputs)
    flux_error = abs(M_flux/M-1)
    gates = dict(
        fixed_point_converged=converged,
        hamiltonian_discrete_residual=h_residual < NUMERICAL_CONTRACT["discrete_residual_tolerance"],
        lapse_discrete_residual=l_residual < NUMERICAL_CONTRACT["discrete_residual_tolerance"],
        positive_conformal_factor=bool(np.min(psi)>0), positive_maximal_lapse=bool(np.min(lapse)>0),
        charge_preparation=charge_error < NUMERICAL_CONTRACT["charge_preparation_tolerance"],
        momentum_constraint_exact_real_phi_imaginary_Pi=True,
        intended_distinct_peak_count=len(peaks)==count,
        pilot_surface_flux=flux_error < NUMERICAL_CONTRACT["pilot_independent_flux_relative_tolerance"])
    calibration = None
    if count == 1:
        calibration = dict(
            mass_relative=abs(M/core.mass-1),
            psi_centre_relative=abs(float(psi_centres[0])/core.psi0-1),
            lapse_centre_relative=abs(float(lapse_centres[0])/core.lapse0-1))
        gates["pilot_isolated_anchor_calibration"] = max(calibration.values()) < NUMERICAL_CONTRACT["pilot_anchor_relative_tolerance"]
    if state_sink is not None:
        state_sink.update(grid=grid, core=core, data=data, psi=psi, lapse=lapse,
                          factors=factors, centres=centres)
    return dict(
        status="INITIAL_DATA_ONLY", numerical_pilot_pass=bool(all(gates.values())),
        count=count, separation=separation, h=h, radius=radius, half_height=half_height,
        cells=grid.nr*grid.nz, iteration_history=history, gates=gates,
        ADM_volume_mass=M, ADM_independent_quadratic_boundary_flux_mass=M_flux,
        ADM_flux_relative_error=flux_error, maximal_W_monopole=W_monopole,
        stationary_W_monopole_for_comparison=-ALPHA*M/2,
        total_charge=Q_total, total_charge_target=count*core.charge,
        regional_ADM_source_sum=float(sum(regional_masses)),
        regional_ADM_source_sum_relative_residual=abs(sum(regional_masses)/M-1),
        overlap_charge_fraction=float((Q_total-diagonal_charge)/Q_total),
        hamiltonian_normalized_residual=h_residual,
        lapse_normalized_residual=l_residual,
        independent_fourth_order_interior_hamiltonian_residual=independent_h_residual,
        independent_fourth_order_interior_lapse_residual=independent_l_residual,
        min_lapse=float(np.min(lapse)),
        max_conformal_factor=float(np.max(psi)), peak_count=len(peaks),
        peak_z=[float(grid.z[i]) for i in peaks], cores=core_outputs,
        isolated_anchor_calibration=calibration,
        scope={
            "canonical_momentum": "P=psi^6 Pi fixed during each inner constraint solve",
            "component_charge": "Prepared partition weights, not separately conserved core charges",
            "ambient_scaling": "Prescribed locally constant conformal rescaling of isolated profiles",
            "lapse": "Maximal-slicing elliptic gauge with independent monopole; not a Killing lapse",
            "boundary": "Independent asymptotically flat monopoles; higher multipoles omitted",
            "regional_mass": "Coordinate Voronoi partition of the total ADM source integral, not separately observable ADM masses",
            "centre_converted_proper_rms_proxy": "Centre conformal factor times coordinate RMS, not integrated proper distance",
            "matter": "One real initial scalar sum; one imaginary normal momentum; sextic cross terms retained",
            "evolution_performed": False, "equilibrium_proved": False,
            "common_clock_ruler_scaling_proved": False,
            "medium_F_or_PF_derived": False, "black_hole_or_singularity_claim": False,
            "continuum_or_domain_convergence_proved": False})


# BEGIN INITIAL CURRENT RESPONSE HELPERS
RESPONSE_PREVIOUS_SOURCE_SHA256 = "04c1b038fde6bea877b7990d24622ef65bf99c58840366628d630f5fa0962ee2"


def current_acceleration_flux(grid, f, y, psi, lapse, order=2):
    """d/dt of outward charge flux at real phi, imaginary normal momentum."""
    fr = np.zeros((grid.nr+1, grid.nz))
    fz = np.zeros((grid.nr, grid.nz+1))
    pref_r = (lapse[:-1]+lapse[1:])/2*((psi[:-1]+psi[1:])/2)**2
    pref_z = (lapse[:, :-1]+lapse[:, 1:])/2*((psi[:, :-1]+psi[:, 1:])/2)**2
    fr[1:-1] = pref_r*(y[:-1]*f[1:]-f[:-1]*y[1:])/grid.h
    fz[:, 1:-1] = pref_z*(y[:, :-1]*f[:, 1:]-f[:, :-1]*y[:, 1:])/grid.h
    if order == 4:
        def face(a, axis):
            v = np.moveaxis(a, axis, 0)
            average = (-v[:-3]+9*v[1:-2]+9*v[2:-1]-v[3:])/16
            derivative = (v[:-3]-27*v[1:-2]+27*v[2:-1]-v[3:])/(24*grid.h)
            return np.moveaxis(average, 0, axis), np.moveaxis(derivative, 0, axis)
        for axis in (0, 1):
            ff, df = face(f, axis)
            yy, dy = face(y, axis)
            pp, _ = face(psi, axis)
            nn, _ = face(lapse, axis)
            value = nn*pp**2*(yy*df-ff*dy)
            if axis == 0:
                fr[2:-2] = value
            else:
                fz[:, 2:-2] = value
    elif order != 2:
        raise ValueError("Only second/fourth face stencils are registered")
    return fr, fz


def current_response_moments(grid, D, flux_r, flux_z, centres):
    """All regional derivatives include charge transfer across their boundary."""
    redges = np.arange(grid.nr+1)*grid.h
    Dtt = -(np.diff(redges[:, None]*flux_r, axis=0)/(grid.R*grid.h)+
            np.diff(flux_z, axis=1)/grid.h)
    Q = grid.integral(D)/(4*np.pi)
    Qtt = grid.integral(Dtt)/(4*np.pi)
    mean = grid.integral(grid.Z*D)/(4*np.pi*Q)
    total_acceleration = (grid.integral(grid.Z*Dtt)/(4*np.pi)-mean*Qtt)/Q
    nearest = np.argmin(abs(grid.Z[None, :, :]-centres[:, None, None]), axis=0)
    regions = []
    for i, centre in enumerate(centres):
        mask = nearest == i
        q = grid.integral(D*mask)/(4*np.pi)
        qtt = grid.integral(Dtt*mask)/(4*np.pi)
        zmean = grid.integral(grid.Z*D*mask)/(4*np.pi*q)
        square = grid.R**2+(grid.Z-zmean)**2
        r2 = grid.integral(square*D*mask)/(4*np.pi*q)
        zacc = (grid.integral(grid.Z*Dtt*mask)/(4*np.pi)-zmean*qtt)/q
        r2acc = (grid.integral(square*Dtt*mask)/(4*np.pi)-r2*qtt)/q
        columns = np.flatnonzero(mask[0])
        outflux = 2*np.pi*grid.h*np.sum(grid.r*(
            flux_z[:, columns[-1]+1]-flux_z[:, columns[0]]))/(4*np.pi)
        regions.append(dict(
            label=i, nominal_centre_z=float(centre), initial_centroid_z=float(zmean),
            regional_Q=q, regional_Qtt=qtt, regional_outward_flux_derivative=float(outflux),
            regional_balance_residual=float(qtt+outflux),
            coordinate_centroid_acceleration=float(zacc),
            coordinate_charge_R2=float(r2),
            coordinate_central_R2_second_derivative=float(r2acc)))
    omitted_tail = max(float(np.max(abs(flux_r[-2]))),
                       float(np.max(abs(flux_z[:, 1]))),
                       float(np.max(abs(flux_z[:, -2]))))
    flux_scale = max(float(np.max(abs(flux_r))), float(np.max(abs(flux_z))), 1e-30)
    return dict(
        total_Q=Q, total_Qtt=Qtt, total_initial_centroid_z=float(mean),
        total_coordinate_centroid_acceleration=float(total_acceleration),
        integrated_absolute_Dtt=grid.integral(abs(Dtt))/(4*np.pi),
        max_abs_flux_derivative=flux_scale, outermost_internal_flux_ratio=omitted_tail/flux_scale,
        regions=regions)


def field_modulus_acceleration(grid, f, y, psi, lapse, order=2):
    """Initial second coordinate-time derivative of |phi| squared."""
    fr = np.zeros((grid.nr+1, grid.nz))
    fz = np.zeros((grid.nr, grid.nz+1))
    fr[1:-1] = (lapse[:-1]+lapse[1:])/2*((psi[:-1]+psi[1:])/2)**2*np.diff(f, axis=0)/grid.h
    fz[:, 1:-1] = (lapse[:, :-1]+lapse[:, 1:])/2*((psi[:, :-1]+psi[:, 1:])/2)**2*np.diff(f, axis=1)/grid.h
    if order == 4:
        for axis in (0, 1):
            v, pp, nn = [np.moveaxis(a, axis, 0) for a in (f, psi, lapse)]
            df = (v[:-3]-27*v[1:-2]+27*v[2:-1]-v[3:])/(24*grid.h)
            pface = (-pp[:-3]+9*pp[1:-2]+9*pp[2:-1]-pp[3:])/16
            nface = (-nn[:-3]+9*nn[1:-2]+9*nn[2:-1]-nn[3:])/16
            value = np.moveaxis(nface*pface**2*df, 0, axis)
            if axis == 0:
                fr[2:-2] = value
            else:
                fz[:, 2:-2] = value
    elif order != 2:
        raise ValueError("Only second/fourth face stencils are registered")
    redges = np.arange(grid.nr+1)*grid.h
    divergence = (np.diff(redges[:, None]*fr, axis=0)/(grid.R*grid.h)+
                  np.diff(fz, axis=1)/grid.h)
    potential_derivative = f-f**3+SEXTIC*f**5
    return 2*f*lapse*divergence/psi**6-2*lapse**2*f*potential_derivative+2*y**2


def regional_field_modulus_control(state, moments, order):
    grid,core,data,psi,lapse,centres,factors=[state[k] for k in
        ("grid","core","data","psi","lapse","centres","factors")]
    f=data["phi"]
    y=lapse*data["P"]/psi**6
    Btt=field_modulus_acceleration(grid,f,y,psi,lapse,order)
    dzf=np.zeros_like(f)
    for centre,b in zip(centres,factors):
        distance=np.sqrt(grid.R**2+(grid.Z-centre)**2)
        dzf+=core.evaluate(b*b*distance)[1]*b*b*(grid.Z-centre)/distance
    derivative_modulus=2*f*dzf
    density=f*data["P"]
    nearest=np.argmin(abs(grid.Z[None,:,:]-centres[:,None,None]),axis=0)
    normalization=2*core.f0**2*(core.omega/core.lapse0)**2
    outputs=[]
    for i,region in enumerate(moments["regions"]):
        mask=nearest==i
        comoving=Btt+region["coordinate_centroid_acceleration"]*derivative_modulus
        projected=comoving/lapse**2
        raw=Btt/lapse**2
        weight=grid.integral(density*mask)
        rms=float(np.sqrt(grid.integral(density*mask*projected**2)/weight)/normalization)
        raw_rms=float(np.sqrt(grid.integral(density*mask*raw**2)/weight)/normalization)
        centre_value=float(grid.centre_values(projected,centres)[i]/normalization)
        outputs.append(dict(label=i,normal_projection_comoving_modulus_RMS=rms,
                            normal_projection_raw_modulus_RMS=raw_rms,
                            normalized_centre_comoving_modulus_second_derivative=centre_value,
                            normalization=normalization))
    return outputs


def initial_response_algebra_controls():
    """Synthetic controls, not a physical evolution or calibration fit."""
    grid = CylindricalGrid(8.0, 12.0, 0.25)
    f = np.exp(-(grid.R**2+(grid.Z-0.7)**2)/2)
    psi = 1+0.02*np.exp(-(grid.R**2+grid.Z**2)/16)
    lapse = 0.95+0.02*np.tanh(grid.Z/4)
    omega = 0.73
    constant_errors = []
    for order in (2, 4):
        fr, fz = current_acceleration_flux(grid, f, omega*f, psi, lapse, order)
        constant_errors.append(max(float(np.max(abs(fr))), float(np.max(abs(fz)))))
    # With constant proper phase rate, the discrete cross product gives the
    # lapse-gradient force with the same face normalization on both sides.
    fr, fz = current_acceleration_flux(grid, f, omega*lapse*f, psi, lapse)
    expected_r = -omega*(lapse[:-1]+lapse[1:])/2*((psi[:-1]+psi[1:])/2)**2*f[:-1]*f[1:]*np.diff(lapse, axis=0)/grid.h
    expected_z = -omega*(lapse[:, :-1]+lapse[:, 1:])/2*((psi[:, :-1]+psi[:, 1:])/2)**2*f[:, :-1]*f[:, 1:]*np.diff(lapse, axis=1)/grid.h
    rest_error = max(float(np.max(abs(fr[1:-1]-expected_r))),
                     float(np.max(abs(fz[:, 1:-1]-expected_z))))
    # A translated localized positive density with Fdot=a D has mean
    # coordinate acceleration a and zero central-width second derivative.
    D = np.exp(-(grid.R**2+(grid.Z-0.7)**2))
    acceleration = 0.03
    sr = np.zeros((grid.nr+1, grid.nz))
    sz = np.zeros((grid.nr, grid.nz+1))
    sz[:, 1:-1] = acceleration*(D[:, :-1]+D[:, 1:])/2
    translation = current_response_moments(grid, D, sr, sz, np.array([0.7]))["regions"][0]
    inverse = current_response_moments(grid, D, sr, -sz, np.array([0.7]))["regions"][0]
    omitted = current_response_moments(grid, D, sr, np.zeros_like(sz), np.array([0.7]))["regions"][0]
    constant_f=np.full_like(f,0.2)
    ones=np.ones_like(f)
    correct_frequency=np.sqrt(1-0.2**2+SEXTIC*0.2**4)
    exact_modulus=field_modulus_acceleration(grid,constant_f,correct_frequency*constant_f,ones,ones)
    wrong_modulus=field_modulus_acceleration(grid,constant_f,constant_f,ones,ones)
    wrong_rate_flux=current_acceleration_flux(grid,constant_f,constant_f,ones,ones)
    gates = dict(
        constant_coordinate_phase_rate_zero_flux=max(constant_errors)<1e-12,
        constant_proper_phase_rate_face_identity=rest_error<1e-12,
        synthetic_translation_centroid=abs(translation["coordinate_centroid_acceleration"]-acceleration)<1e-9,
        synthetic_translation_zero_central_R2=abs(translation["coordinate_central_R2_second_derivative"])<1e-9,
        reversed_flux_reverses_acceleration=abs(inverse["coordinate_centroid_acceleration"]+acceleration)<1e-9,
        omitted_nonzero_flux_rejected=abs(omitted["coordinate_centroid_acceleration"]-acceleration)>1e-9,
        homogeneous_exact_frequency_modulus_stationary=float(np.max(abs(exact_modulus)))<1e-12,
        homogeneous_wrong_frequency_detected=float(np.max(abs(wrong_modulus-0.003168)))<1e-12,
        zero_current_does_not_imply_KG_equilibrium=(
            max(float(np.max(abs(a))) for a in wrong_rate_flux)<1e-12 and
            float(np.max(abs(wrong_modulus)))>0.003))
    return dict(gates={k: bool(v) for k, v in gates.items()},
                constant_rate_max_errors=constant_errors, proper_rate_face_error=rest_error,
                synthetic_translation=translation,
                omitted_flux_translation=omitted,
                homogeneous_correct_frequency=float(correct_frequency),
                homogeneous_wrong_frequency_modulus_acceleration=float(wrong_modulus[0,0]))


def initial_response_case(core, count=1, h=0.5, radius=48.0, half_height=96.0, D=24.0):
    state = {}
    assembly = run_case(core, count=count, separation=D, h=h, radius=radius,
                        half_height=half_height, state_sink=state)
    grid, data, psi, lapse = [state[k] for k in ("grid", "data", "psi", "lapse")]
    f = data["phi"]
    normal_momentum = data["P"]/psi**6
    y = lapse*normal_momentum
    density = f*data["P"]
    results = {}
    for order, name in ((2, "production"), (4, "independent")):
        fr, fz = current_acceleration_flux(grid, f, y, psi, lapse, order)
        results[name] = current_response_moments(grid, density, fr, fz, state["centres"])
        results[name]["field_modulus_controls"]=regional_field_modulus_control(state,results[name],order)
    constant_errors = []
    for order in (2, 4):
        fr, fz = current_acceleration_flux(grid, f, core.omega*f, psi, lapse, order)
        constant_errors.append(max(float(np.max(abs(fr))), float(np.max(abs(fz)))))
    gates = dict(assembly_constraints=bool(assembly["numerical_pilot_pass"]),
                 constant_frequency_control=max(constant_errors)<1e-12)
    for name, result in results.items():
        acc = [r["coordinate_centroid_acceleration"] for r in result["regions"]]
        widths = [r["coordinate_central_R2_second_derivative"] for r in result["regions"]]
        qscale = result["total_Q"]*max(1.0, core.omega**2)
        gates[name+"_finite"] = all(np.isfinite(v) for v in acc+widths)
        gates[name+"_field_modulus_finite"] = all(
            np.isfinite(v) for region in result["field_modulus_controls"] for v in region.values())
        gates[name+"_total_charge_acceleration"] = abs(result["total_Qtt"])/qscale < 1e-10
        gates[name+"_zero_net_centroid_acceleration"] = abs(result["total_coordinate_centroid_acceleration"]) < 1e-10
        gates[name+"_mirror_centroid_parity"] = max(abs(np.asarray(acc)+np.asarray(acc)[::-1])) < 1e-10
        gates[name+"_regional_current_balance"] = max(abs(r["regional_balance_residual"]) for r in result["regions"])/qscale < 1e-10
        gates[name+"_outer_tail_flux_negligible"] = result["outermost_internal_flux_ratio"] < 1e-8
    return dict(
        status="INITIAL_RESPONSE_ONLY", assembly=assembly,
        gates={k: bool(v) for k, v in gates.items()}, response=results,
        constant_frequency_control_max_flux=constant_errors,
        scope={
            "derivative": "Exact initial Noether-current derivative, spatially discretized",
            "time": "Coordinate time of the prepared maximal slice with zero shift",
            "centroid": "Charge centroid of a coordinate Voronoi region, including regional charge transfer",
            "width": "Coordinate central R-squared only; not proper deformation or shape preservation",
            "field_modulus": "Normal-clock-normalized comoving-profile initial KG residual; not proper width or a stability theorem",
            "metric_first_derivative": "Zero at K_ij=0, zero shift; no second metric derivative supplied",
            "evolution_performed": False, "relaxation_proved": False,
            "equilibrium_proved": False, "singularity_resolution": False})


def compare_initial_response_packets(main_packets, domain_packet):
    """Primary motion resolved separately from optional coordinate-width response."""
    assembly_main = {n: dict(p, cases={h: c["assembly"] for h, c in p["cases"].items()})
                     for n, p in main_packets.items()}
    assembly_domain = dict(domain_packet, cases={n: c["assembly"] for n, c in domain_packet["cases"].items()})
    assembly_check = compare_assembly_packets(assembly_main, assembly_domain)
    algebra = initial_response_algebra_controls()
    gates = dict(assembly_validated=assembly_check["status"]=="ASSEMBLY_INITIAL_DATA_VALIDATED",
                 algebra_controls=all(algebra["gates"].values()))
    all_cases = [c for p in main_packets.values() for c in p["cases"].values()]+list(domain_packet["cases"].values())
    gates["all_initial_response_gates"] = all(all(c["gates"].values()) for c in all_cases)
    primary, secondary, modulus_secondary = {}, {}, {}

    def case(n, grid):
        return (domain_packet["cases"][str(n)] if grid=="domain"
                else main_packets[str(n)]["cases"][grid])

    def assess(fine, coarse, extended, stencil):
        errors = dict(grid=abs(fine-coarse), domain=abs(extended-coarse),
                      independent_stencil=abs(fine-stencil))
        resolved = abs(fine) > max(1e-12, 3*max(errors.values()))
        return dict(fine=fine, coarse=coarse, domain_control=extended,
                    independent_stencil=stencil, discrepancies=errors,
                    resolved=bool(resolved),
                    direction="positive" if fine>0 else "negative" if fine<0 else "zero")

    for n in (2, 3):
        for i in (0, n-1):
            key=f"N{n}_core{i}"
            orientation=1.0 if i==0 else -1.0
            def motion(grid, stencil="production"):
                return orientation*case(n, grid)["response"][stencil]["regions"][i]["coordinate_centroid_acceleration"]
            primary[key]=assess(motion("0.25"),motion("0.5"),motion("domain"),motion("0.25","independent"))
            primary[key]["interpretation"]="positive means initially inward in the chosen coordinate gauge"
            gates[key+"_motion_resolved"]=primary[key]["resolved"]
        for i in range(n):
            key=f"N{n}_core{i}"
            def width(grid, stencil="production"):
                a=case(n,grid)["response"][stencil]["regions"][i]["coordinate_central_R2_second_derivative"]
                b=case(1,grid)["response"][stencil]["regions"][0]["coordinate_central_R2_second_derivative"]
                return a-b
            secondary[key]=assess(width("0.25"),width("0.5"),width("domain"),width("0.25","independent"))
            def modulus(grid,stencil="production"):
                a=case(n,grid)["response"][stencil]["field_modulus_controls"][i]["normal_projection_comoving_modulus_RMS"]
                b=case(1,grid)["response"][stencil]["field_modulus_controls"][0]["normal_projection_comoving_modulus_RMS"]
                return a-b
            modulus_secondary[key]=assess(modulus("0.25"),modulus("0.5"),modulus("domain"),modulus("0.25","independent"))
            floor=case(1,"0.25")["response"]["production"]["field_modulus_controls"][0]["normal_projection_comoving_modulus_RMS"]
            modulus_secondary[key]["isolated_fine_RMS_floor"]=floor
            modulus_secondary[key]["resolved"]=bool(
                modulus_secondary[key]["resolved"] and abs(modulus_secondary[key]["fine"])>3*floor)
    return dict(
        status="INITIAL_CENTROID_RESPONSE_VALIDATED" if all(gates.values()) else "INITIAL_CENTROID_RESPONSE_OPEN",
        gates={k:bool(v) for k,v in gates.items()}, primary_coordinate_motion=primary,
        secondary_isolated_subtracted_coordinate_R2=secondary,
        secondary_status="RESOLVED" if all(v["resolved"] for v in secondary.values()) else "OPEN",
        secondary_isolated_subtracted_modulus_RMS=modulus_secondary,
        modulus_secondary_status="RESOLVED" if all(v["resolved"] for v in modulus_secondary.values()) else "OPEN",
        assembly_comparison=assembly_check, algebra_controls=algebra,
        scope={"primary": "Instantaneous coordinate charge-centroid response of prepared cores",
               "secondary": "Coordinate second moment, not proper deformation",
               "full_evolution":False,"equilibrium":False,"PF_closure":False,"singularity_resolution":False})


def run_response_suite():
    start=time.perf_counter()
    output=dict(code_sha256=sha(__file__))
    try:
        module,mod65,mod64,solution,anchor,pins,base_sha=load_background()
        core=IsolatedCore(mod64,solution,anchor)
        def unchanged():
            return sha(HERE/"nonlinear_equilibrium_evolution.py")==base_sha and all(sha(module.SF/p)==v for p,v in pins.items())
        common=dict(source_sha256=sha(__file__),base_source_sha256=base_sha,
                    dependency_sha256=pins,background=core.mapping)
        main={}
        for n in (1,2,3):
            main[str(n)]=dict(common,count=n,cases={str(h):initial_response_case(
                core,count=n,h=h,radius=48.0,half_height=96.0,D=24.0) for h in (.5,.25)},
                inputs_unchanged=unchanged())
        domain=dict(common,cases={str(n):initial_response_case(
            core,count=n,h=.5,radius=64.0,half_height=128.0,D=24.0) for n in (1,2,3)},
            inputs_unchanged=unchanged())
        output.update(main=main,domain=domain,comparison=compare_initial_response_packets(main,domain),
                      inputs_unchanged=unchanged())
    except Exception as error:
        output.update(status="DIAGNOSTIC_FAILED",error=f"{type(error).__name__}: {error}")
    output["elapsed_seconds"]=time.perf_counter()-start
    print(json.dumps(output,indent=2,allow_nan=False))
    return 0 if output.get("inputs_unchanged") and output.get("comparison",{}).get("status")=="INITIAL_CENTROID_RESPONSE_VALIDATED" else 1
# END INITIAL CURRENT RESPONSE HELPERS


# BEGIN ASSEMBLY COMPARISON AND REPRODUCTION HELPERS
ASSEMBLY_NUMERICS_BASELINE_SHA256 = "7a02a07bc3e908dcb025d21bf59e7a2034c9e6e693a1d4c813501166613646a6"


def compare_assembly_packets(main_packets, domain_packet):
    """Validate existing packets without recomputing or mutating any case."""
    gates, response = {}, {}

    def finite_tree(value):
        if isinstance(value, dict):
            return all(finite_tree(item) for item in value.values())
        if isinstance(value, (tuple, list)):
            return all(finite_tree(item) for item in value)
        if isinstance(value, (int, float, np.number)):
            return bool(np.isfinite(value))
        return True

    try:
        if set(main_packets) != {"1", "2", "3"} or set(domain_packet["cases"]) != {"1", "2", "3"}:
            raise ValueError("Exactly N=1,2,3 are required in both main and domain packets")
        first = main_packets["1"]
        all_packets = list(main_packets.values())+[domain_packet]
        gates["provenance_same_source"] = len({p["source_sha256"] for p in all_packets}) == 1
        gates["provenance_same_background_source"] = len({p["base_source_sha256"] for p in all_packets}) == 1
        gates["provenance_same_dependencies"] = all(p["dependency_sha256"] == first["dependency_sha256"] for p in all_packets)
        gates["provenance_same_background"] = all(p["background"] == first["background"] for p in main_packets.values())
        if "background" in domain_packet:
            gates["provenance_domain_background"] = domain_packet["background"] == first["background"]
        gates["input_sources_unchanged"] = all(p["inputs_unchanged"] is True for p in all_packets)
        gates["finite_packet_numbers"] = all(finite_tree(p) for p in all_packets)
        gates["fixed_background"] = (
            abs(first["background"]["ADM_mass"]/7.9689569805342035-1) < 1e-10
            and abs(first["background"]["charge"]/8.58838286008662-1) < 1e-10)
        base_flags = (
            "fixed_point_converged", "hamiltonian_discrete_residual",
            "lapse_discrete_residual", "positive_conformal_factor",
            "positive_maximal_lapse", "charge_preparation",
            "momentum_constraint_exact_real_phi_imaginary_Pi",
            "intended_distinct_peak_count", "pilot_surface_flux")
        for count in (1, 2, 3):
            packet = main_packets[str(count)]
            gates[f"N{count}_packet_count"] = packet["count"] == count
            gates[f"N{count}_grid_set"] = set(packet["cases"]) == {"0.5", "0.25"}
            controls = [(f"h{h}", packet["cases"][h], float(h), 48.0, 96.0)
                        for h in ("0.5", "0.25")]
            controls.append(("domain", domain_packet["cases"][str(count)], 0.5, 64.0, 128.0))
            centres = (np.arange(count)-(count-1)/2)*24.0
            for name, case, h, radius, height in controls:
                prefix = f"N{count}_{name}"
                gates[prefix+"_geometry"] = (
                    case["count"] == count and case["h"] == h and
                    case["separation"] == 24.0 and case["radius"] == radius and
                    case["half_height"] == height)
                gates[prefix+"_case_gates"] = (
                    case["status"] == "INITIAL_DATA_ONLY" and
                    case["numerical_pilot_pass"] is True and
                    all(case["gates"].get(k) is True for k in base_flags) and
                    all(v is True for v in case["gates"].values()))
                gates[prefix+"_equation_residuals"] = (
                    case["hamiltonian_normalized_residual"] < 5e-7 and
                    case["lapse_normalized_residual"] < 5e-7)
                gates[prefix+"_charge"] = (
                    abs(case["total_charge"]/(count*first["background"]["charge"])-1) < 1e-10 and
                    all(abs(c["prepared_Q"]/first["background"]["charge"]-1) < 1e-10 for c in case["cores"]))
                gates[prefix+"_overlap"] = abs(case["overlap_charge_fraction"]) < 0.01
                gates[prefix+"_adiabatic_spatial_control"] = (
                    len(case["cores"]) == count and
                    max(c["ambient_conformal_variation_across_charge_rms"] for c in case["cores"]) < 0.02)
                gates[prefix+"_peak_locations"] = (
                    case["peak_count"] == count and len(case["peak_z"]) == count and
                    bool(np.max(abs(np.sort(case["peak_z"])-centres)) <= h+1e-10))
                gates[prefix+"_source_ledger"] = (
                    case["ADM_volume_mass"] > 0 and
                    abs(sum(c["voronoi_ADM_source_contribution"] for c in case["cores"])/case["ADM_volume_mass"]-1) < 1e-10)
                gates[prefix+"_scope"] = all(case["scope"].get(k) is False for k in (
                    "evolution_performed", "equilibrium_proved",
                    "common_clock_ruler_scaling_proved", "medium_F_or_PF_derived",
                    "black_hole_or_singularity_claim", "continuum_or_domain_convergence_proved"))
        calibration = main_packets["1"]["cases"]["0.25"]["isolated_anchor_calibration"]
        gates["fine_isolated_calibration"] = all(calibration[k] < 0.01 for k in (
            "mass_relative", "psi_centre_relative", "lapse_centre_relative"))

        def masses(grid):
            if grid == "domain":
                return {n: domain_packet["cases"][str(n)]["ADM_volume_mass"] for n in (1, 2, 3)}
            return {n: main_packets[str(n)]["cases"][grid]["ADM_volume_mass"] for n in (1, 2, 3)}

        values = {name: masses(name) for name in ("0.5", "0.25", "domain")}
        combinations = {
            "two_core_deficit": lambda m: 2*m[1]-m[2],
            "three_core_deficit": lambda m: 3*m[1]-m[3],
            "second_increment_drop": lambda m: 2*m[2]-m[1]-m[3]}
        for name, combination in combinations.items():
            coarse, fine, domain = [float(combination(values[k])) for k in ("0.5", "0.25", "domain")]
            grid_error, domain_error = abs(fine-coarse), abs(domain-coarse)
            resolved = abs(fine) > 3*grid_error and abs(fine) > 3*domain_error
            response[name] = dict(
                fine=fine, coarse=coarse, domain_control=domain,
                grid_discrepancy=grid_error, domain_discrepancy=domain_error,
                sign_resolved=bool(resolved),
                direction=("positive" if fine > 0 else "negative" if fine < 0 else "zero"),
                decision=("resolved_positive" if fine > 0 else "resolved_negative")
                if resolved else "unresolved")
            gates[name+"_sign_resolved"] = resolved
        fine = values["0.25"]
        increments = dict(first=fine[1], second=fine[2]-fine[1], third=fine[3]-fine[2])
        return dict(
            status="ASSEMBLY_INITIAL_DATA_VALIDATED" if all(gates.values()) else "ASSEMBLY_INITIAL_DATA_OPEN",
            gates={k: bool(v) for k, v in gates.items()}, response=response,
            fine_masses=fine, fine_added_increments=increments,
            source_sha256=first["source_sha256"], base_source_sha256=first["base_source_sha256"],
            numerical_functions_baseline_sha256=ASSEMBLY_NUMERICS_BASELINE_SHA256,
            scope={
                "literal_count": "Resolved localized initial profiles; charge is a separate quantity",
                "regional_mass": "Coordinate partition of total source integral, not individual ADM charges",
                "direction": "Either resolved sign is an accepted output; no sign was fitted",
                "validated": "Constraint-satisfying locally dilated Cauchy assembly in this bounded dilute domain",
                "equilibrium_proved": False, "medium_PF_or_F_derived": False,
                "singularity_resolution": False, "merger_or_observational_fit": False})
    except (KeyError, TypeError, ValueError, IndexError) as error:
        gates["packet_structure_valid"] = False
        return dict(status="ASSEMBLY_INITIAL_DATA_OPEN",
                    gates={k: bool(v) for k, v in gates.items()},
                    error=f"{type(error).__name__}: {error}",
                    equilibrium_proved=False, singularity_resolution=False)


def run_registered_suite():
    """Reproduce all registered data with one fresh background; stdout only."""
    start = time.perf_counter()
    result = {"contract": NUMERICAL_CONTRACT, "code_sha256": sha(__file__)}
    try:
        module, mod65, mod64, solution, anchor, pins, base_sha = load_background()
        core = IsolatedCore(mod64, solution, anchor)

        def unchanged():
            return (sha(HERE / "nonlinear_equilibrium_evolution.py") == base_sha and
                    all(sha(module.SF/path) == digest for path, digest in pins.items()))

        common = dict(source_sha256=sha(__file__), base_source_sha256=base_sha,
                      dependency_sha256=pins, background=core.mapping)
        main_packets = {}
        for count in (1, 2, 3):
            cases = {str(h): run_case(core, count=count, separation=24.0, h=h,
                                      radius=48.0, half_height=96.0) for h in (0.5, 0.25)}
            main_packets[str(count)] = dict(common, count=count, cases=cases,
                                            inputs_unchanged=unchanged())
        domain = dict(common, cases={
            str(n): run_case(core, count=n, separation=24.0, h=0.5,
                             radius=64.0, half_height=128.0) for n in (1, 2, 3)},
            inputs_unchanged=unchanged())
        result.update(main=main_packets, domain=domain,
                      comparison=compare_assembly_packets(main_packets, domain),
                      inputs_unchanged=unchanged())
    except Exception as error:
        result.update(status="DIAGNOSTIC_FAILED", error=f"{type(error).__name__}: {error}")
    result["elapsed_seconds"] = time.perf_counter()-start
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result.get("inputs_unchanged") and result.get("comparison", {}).get("status") == "ASSEMBLY_INITIAL_DATA_VALIDATED" else 1
# END ASSEMBLY COMPARISON AND REPRODUCTION HELPERS


# BEGIN FIXED-CHARGE AGGREGATE EQUILIBRIUM HELPERS
AGGREGATE_PREVIOUS_SHA256 = "32299ba3daa1277def4483bf8a41b6457ccaf4f7aaebd6eff299975854962fd5"


def aggregate_record_gates(record):
    def finite(value):
        if isinstance(value,dict):
            return all(finite(v) for v in value.values())
        if isinstance(value,(tuple,list)):
            return all(finite(v) for v in value)
        return bool(np.isfinite(value)) if isinstance(value,(int,float,np.number)) else True
    mass=record["ADM_mass"]
    denominators_positive=mass>0 and record["Q"]>0 and record["proper_energy"]>0
    discrepancies = {
        "mass_gauss": abs(record["mass_gauss"]/mass-1),
        "Komar_volume": abs(record["Komar_volume"]/mass-1),
        "Komar_boundary": abs(record["Komar_boundary"]/mass-1),
        "charge_gauss": abs(record["charge_gauss"]/record["Q"]-1),
        "proper_energy_gauss": abs(record["proper_energy_gauss"]/record["proper_energy"]-1),
        "areal_radius_gauss": abs(record["charge_rms_areal_gauss"]/record["charge_rms_areal"]-1),
        "proper_radius_gauss": abs(record["charge_rms_proper_gauss"]/record["charge_rms_proper"]-1)}
    gates=dict(
        inherited_profile=record["inherited_profile_pass"] is True,
        finite=finite(record), positive_source=denominators_positive,
        regular_static_chart=record["minimum_N"]>0 and record["maximum_compactness"]<1 and record["central_lapse"]>0,
        fixed_charge=abs(record["Q"]/record["target_Q"]-1)<2e-8,
        independent_ledgers=max(discrepancies.values())<5e-6)
    return {k:bool(v) for k,v in gates.items()},discrepancies


def aggregate_sign_decision(value, errors, reference_scale=1.):
    resolved=abs(value)>max(1e-8*reference_scale,3*max(errors.values()))
    return dict(value=float(value),errors={k:float(v) for k,v in errors.items()},
                reference_mass=float(reference_scale),fraction=float(value/reference_scale),
                fractional_errors={k:float(v/reference_scale) for k,v in errors.items()},
                minimum_fractional_floor=1e-8,
                resolved=bool(resolved),direction="positive" if value>0 else "negative" if value<0 else "zero")


def aggregate_validator_controls():
    import copy
    base=dict(ADM_mass=2.,Q=3.,target_Q=3.,proper_energy=2.2,mass_gauss=2.,
              Komar_volume=2.,Komar_boundary=2.,charge_gauss=3.,proper_energy_gauss=2.2,
              charge_rms_areal=4.,charge_rms_areal_gauss=4.,
              charge_rms_proper=4.5,charge_rms_proper_gauss=4.5,
              inherited_profile_pass=True,minimum_N=.7,maximum_compactness=.3,
              central_lapse=.8,maximum_Kretschmann=.5)
    tests=dict(positive_control=all(aggregate_record_gates(base)[0].values()))
    mutations={"Q":3.1,"charge_rms_proper":float("nan"),"minimum_N":-.1,"mass_gauss":4.}
    names={"Q":"charge_mismatch","charge_rms_proper":"nonfinite","minimum_N":"horizon_chart","mass_gauss":"duplicated_mass_source"}
    for key,value in mutations.items():
        changed=copy.deepcopy(base);changed[key]=value
        tests[names[key]+"_rejected"]=not all(aggregate_record_gates(changed)[0].values())
    tests["positive_binding_sign_accepted"]=aggregate_sign_decision(1.,{"test":.01})["resolved"]
    tests["negative_binding_sign_accepted"]=aggregate_sign_decision(-1.,{"test":.01})["resolved"]
    tests["unresolved_sign_rejected"]=not aggregate_sign_decision(.01,{"test":.02})["resolved"]
    tests["fractional_floor_enforced"]=not aggregate_sign_decision(1e-7,{"test":0.},100.)["resolved"]
    return tests


def aggregate_observe(mod65,mod64,solution,f0,n,target_Q,radius):
    from scipy.integrate import simpson
    obs=mod65.observe(mod64,solution,f0,radius=radius,points=16001,with_residuals=True)
    inherited=mod65.compact_record(f0,obs)
    # Distinct composite Gauss integration, six nodes on each <=0.1 interval.
    count=int(np.ceil(radius/.1));edges=np.linspace(0,radius,count+1)
    nodes,weights=np.polynomial.legendre.leggauss(6)
    x=((edges[:-1,None]+edges[1:,None])/2+
       (edges[1:,None]-edges[:-1,None])*nodes/2).ravel()
    w=((edges[1:,None]-edges[:-1,None])*np.broadcast_to(weights,(count,6))/2).ravel()
    f,fp,mass,logsigma=solution.sol(x)
    omega=mod64.omega_from_parameter(solution.p)
    fields=mod64.matter_arrays(f,fp,mass,logsigma,x,ALPHA,omega)
    sigma,N,rho,pr,pt=[fields[k] for k in ("sigma","N","rho","p_r","p_t")]
    qdensity=x*x*omega*f*f/(sigma*N)
    # Proper distance is independently accumulated on a regular dense grid;
    # the small omitted origin interval has N=1+O(r^2).
    dense=np.linspace(mod64.EPS,radius,32001)
    yd=solution.sol(dense)
    Nd=1-2*ALPHA*yd[2]/dense
    length=mod64.EPS+cumulative_trapezoid(1/np.sqrt(Nd),dense,initial=0)
    length_at_x=PchipInterpolator(np.r_[0.,dense],np.r_[0.,length])(x)
    qd=dense*dense*omega*yd[0]**2/(np.exp(yd[3])*Nd)
    qg=float(np.sum(w*qdensity))
    qdense=float(simpson(qd,x=dense))
    fields_end=mod64.matter_arrays(yd[0,-1:],yd[1,-1:],yd[2,-1:],yd[3,-1:],
                                   dense[-1:],ALPHA,omega)
    record=dict(
        reference_core_count=n,target_Q=target_Q,f0=float(f0),Omega=float(omega),
        ADM_mass=obs["misner_sharp_adm_mass_dimensionless"],
        Q=obs["noether_charge_dimensionless"],proper_energy=obs["proper_energy_dimensionless"],
        charge_rms_areal=obs["charge_rms_radius_dimensionless"],
        charge_rms_proper=float(np.sqrt(simpson(qd*length**2,x=dense)/qdense)),
        mass_R99_areal=float(np.interp(.99*yd[2,-1],yd[2],dense)),
        maximum_compactness=obs["maximum_compactness_2alphaM_over_x"],
        minimum_N=obs["minimum_N"],central_lapse=obs["central_lapse_sigma"],
        maximum_abs_Ricci=obs["maximum_abs_Ricci_over_m_squared"],
        maximum_Kretschmann=obs["maximum_Kretschmann_over_m_four"],
        mass_gauss=float(np.sum(w*x*x*rho)),
        charge_gauss=qg,proper_energy_gauss=float(np.sum(w*x*x*rho/np.sqrt(N))),
        Komar_volume=float(np.sum(w*x*x*sigma*(rho+pr+2*pt))),
        Komar_boundary=float(fields_end["sigma"][0]*(yd[2,-1]+radius**3*fields_end["p_r"][0])),
        charge_rms_areal_gauss=float(np.sqrt(np.sum(w*qdensity*x*x)/qg)),
        charge_rms_proper_gauss=float(np.sqrt(np.sum(w*qdensity*length_at_x**2)/qg)),
        inherited_profile_pass=bool(mod65.basic_profile_pass(inherited)),
        inherited_profile_record=inherited,quadrature_panel_max=.1,quadrature_order=6)
    gates,discrepancies=aggregate_record_gates(record)
    record.update(gates=gates,ledger_relative_discrepancies=discrepancies)
    return record


def aggregate_match_charge(mod65,mod64,target_Q,seed_cache,bracket,radius,tolerance):
    from scipy.optimize import brentq
    from scipy.integrate import simpson
    calls=0
    def at(f0):
        nonlocal calls
        f0=float(f0)
        if f0 not in seed_cache:
            if calls>=20:
                raise RuntimeError("Matched-charge root exceeded 20 new BVP evaluations")
            nearest=min(seed_cache,key=lambda k:abs(k-f0))
            seed=seed_cache[nearest][0]
            sol=mod65.solve_at(mod64,f0,seed,radius=radius,tolerance=tolerance)
            x=np.linspace(mod64.EPS,radius,16001);f,fp,M,ls=sol.sol(x)
            N=1-2*ALPHA*M/x;om=mod64.omega_from_parameter(sol.p)
            charge=float(simpson(x*x*om*f*f/(np.exp(ls)*N),x=x))
            seed_cache[f0]=(sol,charge);calls+=1
        return seed_cache[f0][1]-target_Q
    lo,hi=map(float,bracket)
    if lo==hi:
        root=lo
    else:
        root=float(brentq(at,lo,hi,xtol=2e-10,rtol=2e-14,maxiter=20))
    residual=at(root)
    if abs(residual/target_Q)>=2e-8:
        raise RuntimeError("Matched-charge root did not meet its frozen Q tolerance")
    return root,seed_cache[root][0],dict(new_BVP_calls=calls,charge_residual=residual,bracket=[lo,hi])


def run_aggregate_equilibrium_suite():
    """Fixed-Q spherical equilibrium energy/radius benchmark, not a merger."""
    from scipy.integrate import simpson
    started=time.perf_counter()
    result=dict(code_sha256=sha(__file__),previous_source_sha256=AGGREGATE_PREVIOUS_SHA256,
                validator_controls=aggregate_validator_controls())
    try:
        module,mod65,mod64,anchor_solution,anchor,pins,base_sha=load_background()
        q0=float(anchor["record"]["charge"]);fanchor=float(mod65.ANCHOR_F0)
        result.update(base_source_sha256=base_sha,dependency_sha256=pins,reference_Q0=q0)
        def charge(sol,radius):
            x=np.linspace(mod64.EPS,radius,16001);f,fp,M,ls=sol.sol(x)
            return float(simpson(x*x*mod64.omega_from_parameter(sol.p)*f*f/
                                  (np.exp(ls)*(1-2*ALPHA*M/x)),x=x))
        cache={fanchor:(anchor_solution,charge(anchor_solution,80.))}
        cursor=fanchor;seed_sol=anchor_solution;seed_steps=0
        roots={1:(fanchor,anchor_solution,dict(new_BVP_calls=0,charge_residual=cache[fanchor][1]-q0,bracket=[fanchor,fanchor]))}
        for n in (2,3,4):
            target=n*q0
            lower=cursor
            while cache[cursor][1]<target:
                lower=cursor
                cursor=min(2.18,cursor+.02)
                if cursor<=lower or seed_steps>=24:
                    raise RuntimeError("Target charge not bracketed before the registered finite branch limit")
                seed_sol=mod65.solve_at(mod64,cursor,seed_sol,radius=80.,tolerance=1e-7)
                cache[cursor]=(seed_sol,charge(seed_sol,80.));seed_steps+=1
            roots[n]=aggregate_match_charge(mod65,mod64,target,cache,(lower,cursor),80.,1e-7)
        configurations={}
        for name,radius,tolerance in (("main",80.,1e-7),("tight",80.,3e-8),("domain",100.,3e-8)):
            records={}
            for n in (1,2,3,4):
                f0,sol,rootinfo=roots[n];target=n*q0
                if name!="main":
                    sol=mod65.solve_at(mod64,f0,sol,radius=radius,tolerance=tolerance)
                    local={f0:(sol,charge(sol,radius))}
                    tolerance_Q=2e-8 if n==1 else 1e-11
                    if abs(local[f0][1]/target-1)>=tolerance_Q:
                        lo=max(fanchor-(1e-5 if n==1 else 0),f0-(1e-5 if n==1 else .002))
                        hi=min(2.18,f0+(1e-5 if n==1 else .002))
                        f0,sol,rootinfo=aggregate_match_charge(mod65,mod64,target,local,(lo,hi),radius,tolerance)
                    else:
                        rootinfo=dict(new_BVP_calls=1,charge_residual=local[f0][1]-target,bracket=[f0,f0])
                row=aggregate_observe(mod65,mod64,sol,f0,n,target,radius)
                row["root_diagnostics"]=rootinfo
                records[str(n)]=row
            M1=records["1"]["ADM_mass"]
            for n in (1,2,3,4):
                row=records[str(n)]
                row.update(matched_separated_reference_mass=n*M1,
                           canonical_separated_reference_mass=n*anchor["record"]["ADM_mass"],
                           available_binding_energy=n*M1-row["ADM_mass"],
                           available_binding_fraction=(n*M1-row["ADM_mass"])/(n*M1))
            configurations[name]=dict(radius=radius,tolerance=tolerance,records=records)
        gates=dict(validator_controls=all(result["validator_controls"].values()),
                   all_equilibrium_gates=all(all(row["gates"].values()) for cfg in configurations.values() for row in cfg["records"].values()))
        comparisons={}
        for n in (1,2,3,4):
            key=str(n);a,b,c=[configurations[k]["records"][key] for k in ("main","tight","domain")]
            changes={k:max(abs(a[k]-b[k]),abs(b[k]-c[k]))/max(abs(b[k]),1e-30)
                     for k in ("ADM_mass","Q","charge_rms_areal","charge_rms_proper","mass_R99_areal")}
            if n>1:
                changes["binding_fraction"]=max(abs(a["available_binding_fraction"]-b["available_binding_fraction"]),
                    abs(b["available_binding_fraction"]-c["available_binding_fraction"]))/max(abs(b["available_binding_fraction"]),1e-30)
            gates["N"+key+"_resolution_domain"]=max(changes.values())<5e-5
            comparisons[key]=dict(relative_changes=changes)
            if n>1:
                single=configurations["tight"]["records"]["1"]
                errors=dict(tolerance=abs(a["available_binding_energy"]-b["available_binding_energy"]),
                    domain=abs(b["available_binding_energy"]-c["available_binding_energy"]),
                    quadrature=abs(b["mass_gauss"]-b["ADM_mass"])+n*abs(single["mass_gauss"]-single["ADM_mass"]),
                    charge_mismatch=b["Omega"]*abs(b["Q"]-b["target_Q"])+n*single["Omega"]*abs(single["Q"]-single["target_Q"]))
                decision=aggregate_sign_decision(b["available_binding_energy"],errors,b["matched_separated_reference_mass"])
                comparisons[key]["binding_decision"]=decision
                gates["N"+key+"_binding_sign_resolved"]=decision["resolved"]
        unchanged=(sha(HERE/"nonlinear_equilibrium_evolution.py")==base_sha and
                   all(sha(module.SF/path)==v for path,v in pins.items()))
        gates["inputs_unchanged"]=unchanged
        gates["source_unchanged_during_run"]=sha(__file__)==result["code_sha256"]
        result.update(configurations=configurations,comparisons=comparisons,gates={k:bool(v) for k,v in gates.items()},
            main_seed_steps=seed_steps,inputs_unchanged=unchanged,
            status="FIXED_CHARGE_AGGREGATE_EQUILIBRIA_VALIDATED" if all(gates.values()) else "FIXED_CHARGE_AGGREGATE_EQUILIBRIA_OPEN",
            scope={"model":"Retained neutral complex scalar spherical equilibrium benchmark",
                   "n":"Number of separated anchor reference objects used to set total Q, not a universal oscillon or electron count",
                   "binding":"Available stationary binding energy at fixed total Q, not a simulated radiated fraction",
                   "merged_cores_remain_identifiable":False,"time_evolution":False,"new_stability_proof":False,
                   "medium_PF_closure":False,"black_hole_or_singularity_resolution":False},
            units={"energy":"(4 pi m_s/lambda) times dimensionless energy",
                   "charge":"(4 pi/lambda) times dimensionless Q","radius":"dimensionless radius/m_s"})
    except Exception as error:
        result.update(status="DIAGNOSTIC_FAILED",error=f"{type(error).__name__}: {error}")
    result["elapsed_seconds"]=time.perf_counter()-started
    print(json.dumps(result,indent=2,allow_nan=False))
    return 0 if result.get("status")=="FIXED_CHARGE_AGGREGATE_EQUILIBRIA_VALIDATED" else 1
# END FIXED-CHARGE AGGREGATE EQUILIBRIUM HELPERS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--suite", action="store_true")
    parser.add_argument("--initial-response", action="store_true")
    parser.add_argument("--response-suite", action="store_true")
    parser.add_argument("--aggregate-equilibrium-suite", action="store_true")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--separation", type=float, default=28.0)
    parser.add_argument("--h", type=float, default=0.5)
    parser.add_argument("--radius", type=float, default=32.0)
    parser.add_argument("--half-height", type=float, default=64.0)
    args = parser.parse_args()
    if args.aggregate_equilibrium_suite:
        return run_aggregate_equilibrium_suite()
    if args.response_suite:
        return run_response_suite()
    if args.suite:
        return run_registered_suite()
    start = time.perf_counter()
    result = {"contract": NUMERICAL_CONTRACT, "code_sha256": sha(__file__)}
    try:
        if args.count < 1:
            raise ValueError("Count must be positive")
        module, mod65, mod64, solution, anchor, pins, source_sha = load_background()
        core = IsolatedCore(mod64, solution, anchor)
        result["background"] = core.mapping
        result["background_source_sha256"] = source_sha
        result["dependency_sha256"] = pins
        result["pilot"] = bool(args.pilot)
        if args.pilot:
            count, h, radius, height = 1, 0.5, 32.0, 64.0
        else:
            count, h, radius, height = args.count, args.h, args.radius, args.half_height
        if args.initial_response:
            result["case"] = initial_response_case(core, count=count, D=args.separation,
                                                   h=h, radius=radius, half_height=height)
        else:
            result["case"] = run_case(core, count=count, separation=args.separation,
                                      h=h, radius=radius, half_height=height)
        result["inputs_unchanged"] = (
            sha(HERE / "nonlinear_equilibrium_evolution.py") == source_sha
            and all(sha(module.SF/path)==digest for path, digest in pins.items()))
    except Exception as error:
        result["status"] = "DIAGNOSTIC_FAILED"
        result["error"] = f"{type(error).__name__}: {error}"
    result["elapsed_seconds"] = time.perf_counter()-start
    print(json.dumps(result, indent=2, allow_nan=False))
    case_pass = (all(result.get("case", {}).get("gates", {}).values())
                 if args.initial_response else result.get("case", {}).get("numerical_pilot_pass"))
    return 0 if result.get("inputs_unchanged") and result.get("case") and case_pass else 1


if __name__ == "__main__":
    sys.exit(main())
