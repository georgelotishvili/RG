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


# BEGIN AGGREGATE COLLAPSE EVOLUTION HELPERS
COLLAPSE_PREVIOUS_SHA256 = "6f88d0986e2ed1db7d903853ad2b776592fe6e683f0331c7348aca9419c42d8d"


def aggregate_phase_imprint(r, field, momentum, kappa=.1, length=4.):
    theta=kappa*length**2*(1-np.exp(-r*r/(2*length**2)))
    phase=np.exp(1j*theta)
    return np.array([field*phase,momentum*phase])


def aggregate_collapse_event(samples, floors):
    try:
        values=np.array([[s[k] for k in ("t","mass_R50","mass_R90","maximum_compactness")] for s in samples])
        valid=(len(samples)>=2 and np.all(np.isfinite(values)) and np.all(np.diff(values[:,0])>0)
               and values[0,0]>=0 and np.all(values[:,1:3]>0) and np.all((values[:,3]>=0)&(values[:,3]<1))
               and all(np.isfinite(floors[k]) and floors[k]>=0 for k in ("mass_R50","mass_R90","maximum_compactness")))
    except (KeyError,TypeError,ValueError,IndexError):
        valid=False
    if not valid:
        return dict(classification="INVALID_EVENT_INPUT",input_validation=False)
    t=np.array([s["t"] for s in samples])
    keys=("mass_R50","mass_R90")
    curves={k:np.array([s[k] for s in samples])/samples[0][k] for k in keys}
    minima={k:int(np.argmin(curves[k])) for k in keys}
    depths={k:float(1-curves[k][minima[k]]) for k in keys}
    contracted=all(depths[k]>=1e-3 and depths[k]>3*floors[k] for k in keys)
    compactness=np.array([s["maximum_compactness"] for s in samples])
    recovered=[]
    for j in range(len(samples)):
        if not contracted or any(t[j]-t[minima[k]]<8 for k in keys):
            continue
        radius_return=all(curves[k][j]-curves[k][minima[k]]>=.25*depths[k] and
                          curves[k][j]-curves[k][minima[k]]>3*floors[k] for k in keys)
        cp=int(np.argmax(compactness[:j+1]))
        if radius_return and cp<j and compactness[cp]-compactness[j]>max(1e-3,3*floors["maximum_compactness"]):
            recovered.append(j)
    return dict(classification="RESOLVED_CONTRACTION_AND_ARREST" if recovered else "FINITE_WINDOW_OUTCOME_OPEN",input_validation=True,
                resolved_contraction=bool(contracted),contraction_depths=depths,
                minimum_times={k:float(t[minima[k]]) for k in keys},numerical_control_floors=floors,
                shared_recovery_time=float(t[recovered[0]]) if recovered else None,
                scope="Finite-window aggregate contraction and partial recovery; not universal stability or singularity removal")


def aggregate_collapse_controls():
    t=np.arange(0.,96.25,.25)
    def sample(r,c):
        return [dict(t=float(x),mass_R50=float(a),mass_R90=float(2*a),maximum_compactness=float(b))
                for x,a,b in zip(t,r,c)]
    floors=dict(mass_R50=1e-5,mass_R90=1e-5,maximum_compactness=1e-5)
    u=sample(1-.1*np.sin(np.pi*t/96),.4+.1*np.sin(np.pi*t/96))
    flat=sample(np.ones_like(t),np.full_like(t,.4))
    inward=sample(1-.002*t,.4+.002*t)
    r=(np.arange(160)+.5)*.025;f=np.exp(-r*r);p=1j*f
    state=aggregate_phase_imprint(r,f,p);reverse=aggregate_phase_imprint(r,f,p,-.1)
    def inward_flux(s):
        grad=np.gradient(s[0],r)
        return (float(np.sum(r*r*np.real(np.conjugate(s[1])*grad)))>0 and
                float(np.sum(-r*r*np.imag(np.conjugate(s[0])*grad)))<0)
    controls=dict(
        manufactured_return_accepted=aggregate_collapse_event(u,floors)["classification"]=="RESOLVED_CONTRACTION_AND_ARREST",
        constant_radius_rejected=aggregate_collapse_event(flat,floors)["classification"]=="FINITE_WINDOW_OUTCOME_OPEN",
        continuing_contraction_rejected=aggregate_collapse_event(inward,floors)["classification"]=="FINITE_WINDOW_OUTCOME_OPEN",
        pointwise_charge_preserved=bool(np.max(abs(np.imag(np.conjugate(state[0])*state[1])-f*f))<1e-14),
        inward_phase_flux=inward_flux(state),reversed_phase_rejected=not inward_flux(reverse))
    for name,key,value in (("nonfinite","mass_R50",float("nan")),("invalid_radius","mass_R90",-1.),("nonmonotonic_time","t",-1.)):
        altered=[dict(s) for s in u];altered[30][key]=value
        controls[name+"_rejected"]=aggregate_collapse_event(altered,floors)["classification"]=="INVALID_EVENT_INPUT"
    return controls


def aggregate_collapse_background():
    from scipy.integrate import simpson
    module,mod65,mod64,sol,anchor,pins,base_sha=load_background()
    target=4*anchor["record"]["charge"];cache={}
    def charge(s,radius):
        x=np.linspace(mod64.EPS,radius,16001);f,fp,M,ls=s.sol(x)
        return float(simpson(x*x*mod64.omega_from_parameter(s.p)*f*f/
                             (np.exp(ls)*(1-2*ALPHA*M/x)),x=x))
    fanchor=float(mod65.ANCHOR_F0)
    cache[fanchor]=(sol,charge(sol,80.))
    sequence=list(np.arange(fanchor+.02,2.10,.02))+[2.10]
    for f0 in sequence:
        sol=mod65.solve_at(mod64,float(f0),sol,radius=80.,tolerance=1e-7)
        cache[float(f0)]=(sol,charge(sol,80.))
    f0,sol,main_root=aggregate_match_charge(mod65,mod64,target,cache,(2.08,2.10),80.,1e-7)
    sol=mod65.solve_at(mod64,f0,sol,radius=128.,tolerance=3e-8)
    f0,sol,final_root=aggregate_match_charge(mod65,mod64,target,{f0:(sol,charge(sol,128.))},(2.08,2.10),128.,3e-8)
    record=aggregate_observe(mod65,mod64,sol,f0,4,target,128.)
    if not all(record["gates"].values()):
        raise RuntimeError("The fresh fixed-Q n4 aggregate background failed its inherited gates")
    return module,mod64,sol,dict(record=record,seed_steps=len(sequence),main_root=main_root,final_root=final_root),pins,base_sha


def aggregate_collapse_case(module,mod64,solution,h=.1,duration=96.,radius=96.,kappa=.1,courant=.2,target_charge=None,
                            grid_factory=None,approach_floor=.05,local_check_stride=16,retain_final_state=False):
    grid=(module.Grid if grid_factory is None else grid_factory)(radius,h);r=grid.r
    f,fp,M,ls=solution.sol(r);omega=mod64.omega_from_parameter(solution.p)
    p0=1j*omega*f/(np.exp(ls)*(1-2*ALPHA*M/r))
    state=aggregate_phase_imprint(r,f,p0,kappa)
    qreference=float(np.sum(grid.vol*np.imag(np.conjugate(f)*p0)))
    intervals=int(round(duration/.25));dt=.25/int(np.ceil(.25/(courant*h)))
    steps=int(round(.25/dt));grid.time_step=dt
    result=dict(h=h,duration=duration,radius=radius,kappa=kappa,length=4.,dt=dt,courant=courant,
                samples=[],local_flux_checks=[],status="COMPLETED",boundary="Zero scalar boundary flux; larger-domain control required")
    started=time.perf_counter();t=0.;checkpoint=None
    def measure():
        row=grid.diagnostics(state,t);g=grid.geometry(*state)
        s=abs(state[0])**2;v=s/2-s*s/4+SEXTIC*s**3/6
        rho=g["N"]*(abs(state[1])**2+abs(g["gradient"])**2)/2+v
        row.update(mass_R50=float(np.interp(.5*g["mass_outer"],np.r_[0,g["mass"]],np.r_[0,r])),
                   mass_R90=float(np.interp(.9*g["mass_outer"],np.r_[0,g["mass"]],np.r_[0,r])),
                   maximum_compactness=float(1-min(g["N"])),maximum_density=float(max(rho)),
                   central_density=float((9*rho[0]-rho[1])/8),
                   mass_monotonicity_defect=float(max(0.,-min(np.diff(g["mass"])))/g["mass_outer"]))
        if not all(np.isfinite(v) for v in row.values()):
            raise FloatingPointError("Nonfinite aggregate diagnostic")
        return row
    try:
        first=measure();result["samples"].append(first);checkpoint=(t,state.copy())
        g=grid.geometry(*state);rhs=grid.rhs(state)
        mflux=r*r*g["sigma"]*g["N"]**2*np.real(np.conjugate(state[1])*g["gradient"])
        qflux=-r*r*g["c"]*np.imag(np.conjugate(state[0])*g["gradient"])
        qdot=grid.vol*np.imag(np.conjugate(rhs[0])*state[1]+np.conjugate(state[0])*rhs[1])
        square=abs(state[0])**2;pot=square/2-square**2/4+SEXTIC*square**3/6
        mprime=r*r*(g["N"]*(abs(state[1])**2+abs(g["gradient"])**2)/2+pot)
        initial_mass_rates={key:float((fraction*mflux[-1]-np.interp(first[key],r,mflux))/np.interp(first[key],r,mprime))
                            for key,fraction in (("mass_R50",.5),("mass_R90",.9))}
        result["initial"]=dict(same_grid_reference_charge=qreference,
            phase_charge_relative_error=abs(first["charge"]/qreference-1),
            continuum_target_charge=target_charge,
            continuum_charge_relative_error=abs(qreference/target_charge-1) if target_charge is not None else None,
            mass_radius_rates=initial_mass_rates,
            areal_charge_rms_rate=float(np.sum((r*r-first["charge_rms_areal"]**2)*qdot)/(2*first["charge"]*first["charge_rms_areal"])),
            inward_mass_flux_weighted=float(np.sum(grid.vol*mflux)),
            outward_charge_flux_weighted=float(np.sum(grid.vol*qflux)),
            unchirped_ADM_mass=float(grid.geometry(f.astype(complex),p0)["mass_outer"]))
        result["local_flux_checks"].append(dict(t=t,**grid.local_flux_check(state)))
        if hasattr(grid,"spatial_diagnostic"):
            result["local_flux_checks"][-1]["spatial_quadrature"]=grid.spatial_diagnostic(state)
        half=grid.local_flux_check(state,eta=5e-7)
        result["initial_directional_step_sensitivity"]=abs(result["local_flux_checks"][0]["local_mass_flux_relative_l2"]-half["local_mass_flux_relative_l2"])
        if first["minimum_N"]<approach_floor:
            result["status"]="APPROACH_LIMIT"
        for j in range(intervals):
            if result["status"]!="COMPLETED":
                break
            for _ in range(steps):
                k1=grid.rhs(state);k2=grid.rhs(state+dt*k1/2)
                k3=grid.rhs(state+dt*k2/2);k4=grid.rhs(state+dt*k3)
                state=state+dt*(k1+2*k2+2*k3+k4)/6;t+=dt
            row=measure();result["samples"].append(row);checkpoint=(t,state.copy())
            if (j+1)%local_check_stride==0 or j==intervals-1 or (grid_factory is not None and row["minimum_N"]<approach_floor):
                result["local_flux_checks"].append(dict(t=t,**grid.local_flux_check(state)))
                if hasattr(grid,"spatial_diagnostic"):
                    result["local_flux_checks"][-1]["spatial_quadrature"]=grid.spatial_diagnostic(state)
            if row["minimum_N"]<approach_floor:
                result["status"]="APPROACH_LIMIT"
    except Exception as error:
        result.update(status="NUMERICAL_DIAGNOSTIC_FAILED",error=f"{type(error).__name__}: {error}",
                      last_completed_time=float(t),failure_scope="Polar-areal chart or numerical diagnostic failure; not a detected singularity")
    if (result["status"]!="COMPLETED" or retain_final_state) and checkpoint is not None:
        ct,cs=checkpoint
        result["last_valid_sampled_state"]=dict(t=float(ct),r=r.tolist(),
            field_real=cs[0].real.tolist(),field_imaginary=cs[0].imag.tolist(),
            momentum_real=cs[1].real.tolist(),momentum_imaginary=cs[1].imag.tolist(),
            momentum_convention="Pi=phi_t/(sigma*N); geometry is reconstructed from this state")
    if result["samples"]:
        first=result["samples"][0];checks=result["local_flux_checks"]
        summary=dict(maximum_relative_charge_drift=max(abs(s["charge"]/first["charge"]-1) for s in result["samples"]),
                     maximum_relative_mass_drift=max(abs(s["ADM_mass"]/first["ADM_mass"]-1) for s in result["samples"]),
                     maximum_characteristic_Courant=dt*grid.stage_max_speed/h,
                     minimum_N_RHS_stages=grid.stage_min_N,minimum_sigma_RHS_stages=grid.stage_min_sigma,
                     maximum_negative_charge_fraction=max(s["negative_charge_fraction"] for s in result["samples"]))
        for key in ("local_mass_flux_relative_l2","mass_radial_constraint_relative_l2","lapse_radial_constraint_relative_l2"):
            summary["maximum_"+key]=max((c[key] for c in checks),default=1e300)
        summary["maximum_relative_semidiscrete_charge_rate"]=max((abs(c["semidiscrete_charge_rate"])/first["charge"] for c in checks),default=1e300)
        initial=result.get("initial",{})
        gates=dict(completed=result["status"]=="COMPLETED",
            charge_budget=summary["maximum_relative_charge_drift"]<1e-5,mass_budget=summary["maximum_relative_mass_drift"]<5e-3,
            pointwise_charge=initial.get("phase_charge_relative_error",1)<1e-12,
            characteristic_Courant=summary["maximum_characteristic_Courant"]<.45,
            semidiscrete_charge=summary["maximum_relative_semidiscrete_charge_rate"]<1e-10,
            initial_directional_step=result.get("initial_directional_step_sensitivity",1)<1e-6,
            monotone_mass=max(s["mass_monotonicity_defect"] for s in result["samples"])<1e-9)
        if kappa>0:
            gates["initial_inward_flow"]=all(v<0 for v in initial.get("mass_radius_rates",{"missing":1}).values()) and initial.get("areal_charge_rms_rate",1)<0
        result.update(summary=summary,gates={k:bool(v) for k,v in gates.items()})
    result["elapsed_seconds"]=time.perf_counter()-started
    if hasattr(grid,"maximum_cell_delta_J"):
        result["maximum_cell_delta_J"]=grid.maximum_cell_delta_J
        result["spatial_method"]="Positive cell-local GL4 mass integration with unchanged scalar equations and lapse quadrature"
        result["approach_floor"]=approach_floor
    print(f"Aggregate evolution h={h} kappa={kappa} R={radius}: {result['status']}, t={t:.3f}",file=sys.stderr,flush=True)
    return result


def run_aggregate_collapse_suite(pilot=False,flow_strength=.1):
    if flow_strength not in (.1,.01):
        raise ValueError("Only the two preregistered aggregate-flow strengths are available")
    result=dict(code_sha256=sha(__file__),previous_source_sha256=COLLAPSE_PREVIOUS_SHA256,
                controls=aggregate_collapse_controls(),cases={},pilot=bool(pilot),flow_strength=flow_strength)
    started=time.perf_counter()
    try:
        module,mod64,solution,background,pins,base_sha=aggregate_collapse_background()
        result.update(background=background,base_source_sha256=base_sha,dependency_sha256=pins)
        specifications=[("flow_coarse",.1,96.,flow_strength,.2)]
        if not pilot:
            specifications += [("flow_middle",.05,96.,flow_strength,.2),("flow_fine",.025,96.,flow_strength,.2),
                               ("zero_middle",.05,96.,0.,.2),("zero_fine",.025,96.,0.,.2),
                               ("half_time_step",.025,96.,flow_strength,.1),("larger_domain",.05,128.,flow_strength,.2)]
        for name,h,radius,kappa,courant in specifications:
            result["cases"][name]=aggregate_collapse_case(module,mod64,solution,h,12. if pilot else 96.,radius,kappa,courant,
                                                         target_charge=background["record"]["target_Q"])
        cases=result["cases"]
        gates=dict(controls=all(result["controls"].values()),
                   case_numerics=all(all(c.get("gates",{"missing":False}).values()) for c in cases.values()),
                   source_unchanged=sha(__file__)==result["code_sha256"],
                   dependencies_unchanged=sha(HERE/"nonlinear_equilibrium_evolution.py")==base_sha and all(sha(module.SF/p)==v for p,v in pins.items()))
        if any(c["status"]=="NUMERICAL_DIAGNOSTIC_FAILED" for c in cases.values()):
            result["status"]="NUMERICAL_DIAGNOSTIC_FAILED"
        elif any(c["status"]=="APPROACH_LIMIT" for c in cases.values()):
            result["status"]="APPROACH_LIMIT"
        elif pilot:
            result["status"]="PILOT_NUMERICS_PASSED" if all(gates.values()) else "PILOT_NUMERICS_OPEN"
        else:
            keys=("mass_R50","mass_R90","charge_rms_areal","charge_rms_proper","central_amplitude","minimum_N")
            wave=lambda case,key:np.array([s[key] for s in case["samples"]])
            def errors(a,b):
                return {k:float(np.sqrt(np.mean((wave(a,k)-wave(b,k))**2))/max(np.sqrt(np.mean(wave(b,k)**2)),1e-14)) for k in keys}
            coarse,middle,fine=[cases[k] for k in ("flow_coarse","flow_middle","flow_fine")]
            e01,e12=errors(coarse,middle),errors(middle,fine)
            et,ed=errors(fine,cases["half_time_step"]),errors(middle,cases["larger_domain"])
            ratios={k:e12[k]/max(e01[k],1e-14) for k in keys}
            gates.update(spatial_convergence=all(e12[k]<5e-3 or ratios[k]<.6 for k in keys),
                         timestep_control=max(et.values())<5e-3,domain_control=max(ed.values())<5e-3)
            for key in ("local_mass_flux_relative_l2","mass_radial_constraint_relative_l2","lapse_radial_constraint_relative_l2"):
                a=middle["summary"]["maximum_"+key];b=fine["summary"]["maximum_"+key]
                gates[key]=b<5e-3 and (b<1e-6 or b/max(a,1e-14)<.6)
            floors={}
            for k in ("mass_R50","mass_R90","maximum_compactness"):
                def delta(case):
                    z=wave(case,k)
                    return z/z[0]-1 if k!="maximum_compactness" else z-z[0]
                envelope=lambda a:float(max(abs(a)))
                floors[k]=max(envelope(delta(fine)-delta(middle)),envelope(delta(fine)-delta(cases["half_time_step"])),
                              envelope(delta(middle)-delta(cases["larger_domain"])),envelope(delta(cases["zero_fine"])),1e-12)
            event=aggregate_collapse_event(fine["samples"],floors)
            gates["event_input_validation"]=event["input_validation"]
            result.update(convergence=dict(coarse_middle=e01,middle_fine=e12,ratios=ratios,half_step=et,domain=ed),
                          event=event)
            result["status"]=event["classification"] if all(gates.values()) else "NUMERICAL_VALIDATION_OPEN"
        result["gates"]={k:bool(v) for k,v in gates.items()}
        result["scope"]=dict(model="Spherical neutral scalar aggregate at Q=4Q0 with an externally prepared inward phase gradient",
            requested_flow_strength=flow_strength,
            fixed_charge_not_particle_count=True,no_charge_projection=True,finite_duration_only=True,
            no_universal_stability_or_black_hole_or_singularity_claim=True,
            mass_budget="Closed-domain ADM energy, including energy added by preparation; not a radiated mass measurement")
    except Exception as error:
        result.update(status="NUMERICAL_DIAGNOSTIC_FAILED",error=f"{type(error).__name__}: {error}")
    result["elapsed_seconds"]=time.perf_counter()-started
    print(json.dumps(result,indent=2,allow_nan=False))
    return 0 if result.get("status") in ("RESOLVED_CONTRACTION_AND_ARREST","FINITE_WINDOW_OUTCOME_OPEN","PILOT_NUMERICS_PASSED") else 1
# END AGGREGATE COLLAPSE EVOLUTION HELPERS


# BEGIN CELL-LOCAL SPATIAL REPAIR HELPERS
SPATIAL_PREVIOUS_SHA256 = "c199c4e7f423df635635a9f04ccf461c7507b9b5f6b6a276dfc539c3668c1f27"
_FITTED_MASS_COMPILED = None


def _fitted_mass_recurrence(q,b,h,nodes,weights):
    """M'=b-q*M; positive quadrature, no growing integrating factor."""
    mass=np.empty(len(q))
    length=h/2
    first=0.
    for j in range(len(nodes)):
        u=(nodes[j]+1)/2
        remaining=.5*q[0]*length*(1-u*u)
        first+=weights[j]*np.exp(-remaining)*b[0]*u*u
    mass[0]=length*first/2
    maximum_jump=q[0]*length/2
    for i in range(1,len(q)):
        jump=.5*h*(q[i-1]+q[i])
        value=0.
        for j in range(len(nodes)):
            u=(nodes[j]+1)/2
            remaining=.5*h*(1-u)*(q[i-1]*(1-u)+q[i]*(1+u))
            value+=weights[j]*np.exp(-remaining)*((1-u)*b[i-1]+u*b[i])
        mass[i]=np.exp(-jump)*mass[i-1]+h*value/2
        maximum_jump=max(maximum_jump,jump)
    jump=q[-1]*length
    phi1=-np.expm1(-jump)/jump if jump!=0 else 1.
    outer=np.exp(-jump)*mass[-1]+length*b[-1]*phi1
    return mass,outer,max(maximum_jump,jump)


def fitted_mass_kernel():
    global _FITTED_MASS_COMPILED
    if _FITTED_MASS_COMPILED is None:
        from numba import njit
        _FITTED_MASS_COMPILED=njit(cache=False,fastmath=False)(_fitted_mass_recurrence)
    return _FITTED_MASS_COMPILED


def fitted_grid_factory(module,order=4):
    kernel=fitted_mass_kernel()
    nodes,weights=np.polynomial.legendre.leggauss(order)
    class FittedGrid(module.Grid):
        def __init__(self,radius,h):
            super().__init__(radius,h)
            self.maximum_cell_delta_J=0.
        def geometry(self,field,momentum):
            grad=self.gradient(field);square=abs(field)**2
            potential=square/2-square**2/4+SEXTIC*square**3/6
            kinetic=abs(momentum)**2+abs(grad)**2
            q=ALPHA*self.r*kinetic;b=self.r**2*(kinetic/2+potential)
            if not np.all(np.isfinite(q)) or not np.all(np.isfinite(b)) or np.min(b)<0:
                raise FloatingPointError("Invalid source in positive cell-local mass recurrence")
            J=self.primitive(q,1);Jouter=J[-1]+q[-1]*self.h/2
            mass,mass_outer,jump=kernel(q,b,self.h,nodes,weights)
            self.maximum_cell_delta_J=max(self.maximum_cell_delta_J,float(jump))
            N=1-2*ALPHA*mass/self.r;sigma=np.exp(J-Jouter);sigma0=float(np.exp(-Jouter))
            if not np.all(np.isfinite(mass)) or not np.isfinite(mass_outer) or np.min(N)<=0 or np.min(sigma)<=0 or sigma0<=0:
                raise FloatingPointError("Cell-local evolution left the regular polar-areal chart or resolved lapse range")
            return dict(N=N,sigma=sigma,c=N*sigma,mass=mass,mass_outer=float(mass_outer),sigma0=sigma0,gradient=grad)
        def spatial_diagnostic(self,state):
            g=self.geometry(*state);s=abs(state[0])**2
            kinetic=abs(state[1])**2+abs(g["gradient"])**2
            q=ALPHA*self.r*kinetic;b=self.r**2*(kinetic/2+s/2-s*s/4+SEXTIC*s**3/6)
            n8,w8=np.polynomial.legendre.leggauss(8)
            m8,out8,jump=kernel(q,b,self.h,n8,w8);N8=1-2*ALPHA*m8/self.r
            errors=dict(mass_profile=float(max(abs(g["mass"]-m8)/np.maximum(abs(m8),1e-30))),
                        outer_mass=float(abs(g["mass_outer"]/out8-1)) if out8>0 else float(abs(g["mass_outer"]-out8)),
                        N_profile=float(max(abs(g["N"]-N8)/np.maximum(abs(N8),1e-14))))
            return dict(quadrature_order=order,control_order=8,maximum_cell_delta_J=float(jump),
                        maximum_seen_cell_delta_J=self.maximum_cell_delta_J,relative_errors=errors,
                        quadrature_pass=bool(max(errors.values())<1e-6))
    return FittedGrid


def fitted_spatial_controls(module):
    kernel=fitted_mass_kernel()
    n4,w4=np.polynomial.legendre.leggauss(4);n8,w8=np.polynomial.legendre.leggauss(8)
    q=np.full(32,.8);b=np.full(32,.7);h=.25
    mass,out,_=kernel(q,b,h,n4,w4)
    exact=mass[0]*np.exp(-q[0]*h*np.arange(len(q)))+b[0]/q[0]*(-np.expm1(-q[0]*h*np.arange(len(q))))
    constant_error=float(max(abs(mass-exact)))
    # A continuous piecewise-linear source with q=0 integrates exactly;
    # the centre separately uses its declared r^2 regular series.
    r=(np.arange(32)+.5)*h;poly=1.3*r*r
    zero,zero_out,_=kernel(np.zeros(32),poly,h,n4,w4)
    expected=poly[0]*r[0]/3+np.r_[0,np.cumsum((poly[:-1]+poly[1:])*h/2)]
    centre_error=abs(zero[0]-1.3*r[0]**3/3)
    zero_error=float(max(abs(zero-expected)))
    qvar=.2+2*np.sin(r)**2;bvar=.1+r*r*np.exp(-r)
    a,ao,jump=kernel(qvar,bvar,h,n4,w4);c,co,_=kernel(qvar,bvar,h,n8,w8)
    quadrature_error=float(max(max(abs(a-c))/max(c),abs(ao-co)/co))
    grid=fitted_grid_factory(module)(8.,.1);vacuum=grid.geometry(np.zeros(80,complex),np.zeros(80,complex))
    tests=dict(constant_coefficient_ODE=constant_error<1e-12,
               zero_q_piecewise_polynomial=zero_error<1e-12,regular_centre_polynomial=centre_error<1e-14,
               nonnegative_source_positive_mass=bool(min(a)>0 and ao>0),
               GL4_GL8_agreement=quadrature_error<1e-8,
               vacuum_geometry=bool(max(abs(vacuum["mass"]))==0 and vacuum["mass_outer"]==0 and
                                    max(abs(vacuum["N"]-1))==0 and max(abs(vacuum["sigma"]-1))==0))
    return dict(tests={k:bool(v) for k,v in tests.items()},errors=dict(constant=constant_error,zero_q=zero_error,centre=float(centre_error),
                                       quadrature=quadrature_error),maximum_test_cell_delta_J=float(jump),
                method_order="Piecewise-linear source and retained field gradients: second-order spatial method")
def fitted_equilibrium_control(module,mod64,solution):
    factory=fitted_grid_factory(module);rows={}
    reference_mass=float(solution.sol(48.)[2])
    reference_lapse=float(np.exp(solution.sol(mod64.EPS)[3]))
    omega=mod64.omega_from_parameter(solution.p)
    for h in (.025,.0125,.00625):
        grid=factory(48.,h);f,fp,M,ls=solution.sol(grid.r)
        N=1-2*ALPHA*M/grid.r;p=1j*omega*f/(np.exp(ls)*N)
        g=grid.geometry(f.astype(complex),p)
        rows[str(h)]=dict(mass=abs(g["mass_outer"]/reference_mass-1),
                         central_lapse=abs(g["sigma0"]/reference_lapse-1),
                         metric_N=float(max(abs(g["N"]/N-1))))
    middle,fine=rows["0.0125"],rows["0.00625"]
    gates={k:fine[k]<5e-3 and (fine[k]<1e-6 or fine[k]/max(middle[k],1e-14)<.6) for k in fine}
    return dict(relative_errors=rows,gates={k:bool(v) for k,v in gates.items()})


def spatial_prefix_verdict(cases,end):
    names=("coarse","middle","fine","half_step","domain")
    keys=("mass_R50","mass_R90","charge_rms_areal","charge_rms_proper","central_amplitude","minimum_N")
    if end<1 or int(end)!=end or not all(n in cases for n in names):
        return dict(end=end,passed=False,gates={"all_cases":False})
    rows={n:[s for s in cases[n]["samples"] if s["t"]<=end+1e-7] for n in names}
    checks={n:[s for s in cases[n]["local_flux_checks"] if s["t"]<=end+1e-7] for n in names}
    covered=all(len(rows[n])==round(4*end)+1 and
        all(abs(s["t"]-i*.25)<1e-7 for i,s in enumerate(rows[n])) and
        all(any(abs(d["t"]-t)<1e-7 and "spatial_quadrature" in d for d in checks[n])
            for t in range(int(end)+1)) for n in names)
    if not covered:
        return dict(end=end,passed=False,gates={"complete_sample_and_diagnostic_coverage":False})
    budgets={}
    for n in names:
        first=rows[n][0];initial=cases[n]["initial"]
        budgets[n]=dict(
            charge=max(abs(s["charge"]/first["charge"]-1) for s in rows[n]),
            mass=max(abs(s["ADM_mass"]/first["ADM_mass"]-1) for s in rows[n]),
            semidiscrete_charge=max(abs(d["semidiscrete_charge_rate"])/first["charge"] for d in checks[n]),
            quadrature=max(max(d["spatial_quadrature"]["relative_errors"].values()) for d in checks[n]))
    gates=dict(complete_sample_and_diagnostic_coverage=True,
        charge_budget=max(b["charge"] for b in budgets.values())<1e-5,
        mass_budget=max(b["mass"] for b in budgets.values())<5e-3,
        semidiscrete_charge=max(b["semidiscrete_charge"] for b in budgets.values())<1e-10,
        quadrature=max(b["quadrature"] for b in budgets.values())<1e-6,
        initial_preparation=all(cases[n]["initial"]["phase_charge_relative_error"]<1e-12
            and all(v<0 for v in cases[n]["initial"]["mass_radius_rates"].values())
            and cases[n]["initial"]["areal_charge_rms_rate"]<0
            and cases[n]["initial_directional_step_sensitivity"]<1e-6 for n in names),
        CFL=all(cases[n]["summary"]["maximum_characteristic_Courant"]<.45 for n in names),
        monotone_mass=all(max(s["mass_monotonicity_defect"] for s in rows[n])<1e-9 for n in names))
    wave=lambda n,k:np.array([s[k] for s in rows[n]])
    def error(a,b):
        return {k:float(np.sqrt(np.mean((wave(a,k)-wave(b,k))**2))/
                  max(np.sqrt(np.mean(wave(b,k)**2)),1e-14)) for k in keys}
    e01,e12,et,ed=error("coarse","middle"),error("middle","fine"),error("fine","half_step"),error("middle","domain")
    ratios={k:e12[k]/max(e01[k],1e-14) for k in keys}
    gates.update(spatial_convergence=all(e12[k]<5e-3 or ratios[k]<.6 for k in keys),
                 timestep=max(et.values())<5e-3,domain=max(ed.values())<5e-3)
    local={}
    for k in ("local_mass_flux_relative_l2","mass_radial_constraint_relative_l2","lapse_radial_constraint_relative_l2"):
        values={n:max(d[k] for d in checks[n]) for n in names}
        ratio=values["fine"]/max(values["middle"],1e-14)
        gates[k]=values["fine"]<5e-3 and (values["fine"]<1e-6 or ratio<.6)
        local[k]=dict(maxima=values,fine_middle_ratio=ratio)
    return dict(end=end,passed=bool(all(gates.values())),gates={k:bool(v) for k,v in gates.items()},
        budgets=budgets,local_checks=local,convergence=dict(coarse_middle=e01,middle_fine=e12,
        ratios=ratios,half_step=et,domain=ed),fine_initial=rows["fine"][0],fine_final=rows["fine"][-1])


def run_spatial_repair_suite():
    started=time.perf_counter()
    result=dict(code_sha256=sha(__file__),previous_source_sha256=SPATIAL_PREVIOUS_SHA256,cases={})
    try:
        module,mod64,solution,background,pins,base_sha=aggregate_collapse_background()
        result.update(background=background,dependency_sha256=pins,base_source_sha256=base_sha)
        result["method_controls"]=fitted_spatial_controls(module)
        result["equilibrium_geometry_control"]=fitted_equilibrium_control(module,mod64,solution)
        factory=fitted_grid_factory(module)
        equilibrium=[]
        for h in (.025,.0125,.00625):
            grid=factory(48.,h);f,fp,M,ls=solution.sol(grid.r)
            pi=1j*mod64.omega_from_parameter(solution.p)*f/(np.exp(ls)*(1-2*ALPHA*M/grid.r))
            g=grid.geometry(f,pi)
            equilibrium.append(dict(h=h,ADM_mass=g["mass_outer"],
                relative_mass_error=abs(g["mass_outer"]/background["record"]["ADM_mass"]-1),
                quadrature=grid.spatial_diagnostic(np.array([f.astype(complex),pi]))))
        eqerr=[v["relative_mass_error"] for v in equilibrium]
        prechecks=dict(method_controls=all(result["method_controls"]["tests"].values()),
            stationary_geometry=all(result["equilibrium_geometry_control"]["gates"].values()),
            stationary_limit=eqerr[-1]<5e-3 and (eqerr[-1]<1e-8 or eqerr[-1]/eqerr[-2]<.6),
            stationary_quadrature=all(v["quadrature"]["quadrature_pass"] for v in equilibrium))
        result.update(equilibrium=equilibrium,prechecks=prechecks)
        if not all(prechecks.values()):
            raise RuntimeError("Spatial-method prerequisite failed")
        specs=(("coarse",.025,48.,.2),("middle",.0125,48.,.2),("fine",.00625,48.,.2),
               ("half_step",.00625,48.,.1),("domain",.0125,64.,.2))
        for name,h,radius,courant in specs:
            result["cases"][name]=aggregate_collapse_case(module,mod64,solution,h=h,duration=32.,
                radius=radius,kappa=.1,courant=courant,target_charge=background["record"]["target_Q"],
                grid_factory=factory,approach_floor=.01,local_check_stride=4,retain_final_state=True)
        last=min(c["samples"][-1]["t"] if c["samples"] else 0 for c in result["cases"].values())
        common=int(np.floor(last+1e-7))
        result["common_interval"]=spatial_prefix_verdict(result["cases"],common)
        result["latest_validated_prefix"]=None
        for end in range(common,0,-1):
            verdict=spatial_prefix_verdict(result["cases"],end)
            if verdict["passed"]:
                result["latest_validated_prefix"]=verdict
                break
        integrity=dict(source_unchanged=sha(__file__)==result["code_sha256"],
            dependencies_unchanged=sha(HERE/"nonlinear_equilibrium_evolution.py")==base_sha
                and all(sha(module.SF/p)==v for p,v in pins.items()))
        result["integrity"]=integrity
        if not all(integrity.values()):
            result["status"]="SOURCE_INTEGRITY_FAILED"
        elif common>=32 and result["common_interval"]["passed"] and all(c["status"]=="COMPLETED" for c in result["cases"].values()):
            result["status"]="STRONG_FLOW_VALIDATED_TO_T32"
        elif result["latest_validated_prefix"]:
            result["status"]="VALIDATED_PREFIX_ENDPOINT_OPEN"
        else:
            result["status"]="SPATIAL_REPAIR_OPEN"
        result["scope"]=dict(unchanged_continuum_action=True,unchanged_strong_initial_preparation=True,
            method="Cell-local radial mass quadrature; retained second-order field flux and gradient",
            physical_endpoint="Infer only within validated prefix; positive-F guard is not a horizon or singularity",
            horizon_crossing=False,singularity_resolution=False)
    except Exception as error:
        result.update(status="DIAGNOSTIC_FAILED",error=f"{type(error).__name__}: {error}")
    result["elapsed_seconds"]=time.perf_counter()-started
    print(json.dumps(result,indent=2,allow_nan=False))
    return 0 if result.get("status")=="STRONG_FLOW_VALIDATED_TO_T32" else 1
# END CELL-LOCAL SPATIAL REPAIR HELPERS


# BEGIN SAME-SLICE HORIZON-REGULAR HELPERS
REGULAR_PREVIOUS_SHA256 = "64c8ae6e0105fbba2753b299f5862557f3388def4c068c9088aecc69ac115c76"


def regular_grid_factory(module):
    class RegularGrid(module.Grid):
        def __init__(self,radius,h,lapse=None):
            super().__init__(radius,h)
            self.lapse=np.ones_like(self.r) if lapse is None else np.array(lapse,dtype=float)
            self.lapse_r=self.derivative(self.lapse)
            self.lapse_centre=float((9*self.lapse[0]-self.lapse[1])/8)
            self.maximum_courant=0.
        def derivative(self,y):
            out=self.gradient(y)
            out[-1]=(3*y[-1]-4*y[-2]+y[-3])/(2*self.h)
            return out
        def geometry(self,state):
            if not np.all(np.isfinite(state)):
                raise FloatingPointError("Nonfinite horizon-regular state")
            field,P=state[:2];mass,k=state[2].real,state[3].real
            v=self.r*k;F=1-2*ALPHA*mass/self.r;A=F+v*v
            if min(A)<=0 or min(self.lapse)<=0:
                raise FloatingPointError("General areal slice lost A>0 or positive lapse")
            root=np.sqrt(A);grad=self.derivative(field);s=abs(field)**2
            V=s/2-s*s/4+SEXTIC*s**3/6
            rho=A*(abs(P)**2+abs(grad)**2)/2+V
            S=root*np.real(np.conjugate(P)*grad);beta=self.lapse*v
            return dict(A=A,F=F,v=v,beta=beta,root=root,gradient=grad,rho=rho,V=V,S=S,
                        pr=rho-2*V,Kr=k+self.r*self.derivative(k)-ALPHA*self.r*S)
        def rhs(self,state):
            g=self.geometry(state);field,P=state[:2];M,k=state[2].real,state[3].real
            L=self.lapse;r=self.r;c=L*g["root"];beta=g["beta"]
            speed=float(max(abs(beta)+c))
            if self.time_step is not None:
                number=self.time_step*speed/self.h
                self.maximum_courant=max(self.maximum_courant,number)
                if number>=.4:
                    raise FloatingPointError("Horizon-regular Courant bound exceeded")
            # Divergence and its negative weighted adjoint form a charge pair.
            advflux=np.zeros(len(r)+1,complex);waveflux=advflux.copy()
            B=self.edges[1:-1]**2*(beta[:-1]+beta[1:])/2
            advflux[1:-1]=B*(P[:-1]+P[1:])/2
            advfield=np.zeros(len(r),complex)
            face=B*np.diff(field)/2
            advfield[:-1]+=face/self.vol[:-1];advfield[1:]+=face/self.vol[1:]
            waveflux[1:-1]=self.edges[1:-1]**2*(c[:-1]+c[1:])/2*np.diff(field)/self.h
            square=abs(field)**2;force=(1-square+SEXTIC*square**2)*field
            out=np.zeros_like(state)
            out[0]=c*P+advfield
            out[1]=np.diff(waveflux+advflux)/self.vol-L*force/g["root"]
            out[2]=L*r*r*(g["v"]*g["A"]*(abs(P)**2+abs(g["gradient"])**2)
                         +(g["A"]+g["v"]**2)*g["S"])
            out[3]=beta*self.derivative(k)+L*(k*k+ALPHA*M/r**3+ALPHA*g["pr"])-g["A"]*self.lapse_r/r
            return out
        def measure(self,state,t):
            g=self.geometry(state);rhs=self.rhs(state);f,P=state[:2];M,k=state[2].real,state[3].real
            r=self.r
            d4=lambda a:(a[:-4]-8*a[1:-3]+8*a[3:-1]-a[4:])/(12*self.h)
            inside=r[2:-2]<=min(15.,self.radius-2*self.h)
            rms=lambda z:float(np.linalg.norm(z[inside]))
            source=r*r*(g["rho"]+g["v"]*g["S"])
            ham=rms(d4(M)-source[2:-2])/max(rms(source[2:-2]),1e-14)
            At=-2*ALPHA*rhs[2].real/r+2*r*r*k*rhs[3].real
            target=g["beta"][2:-2]*d4(g["A"])-(
                2*r*k*g["A"]*self.lapse_r+2*ALPHA*self.lapse*r*g["A"]*g["S"])[2:-2]
            # Normalize by unsummed physical terms, including an O(rho) scale.
            scale=(abs(At)+abs(2*r*k*g["A"]*self.lapse_r)+
                   abs(2*ALPHA*self.lapse*r*g["A"]*g["S"])+ALPHA*self.lapse*(abs(g["rho"])+abs(g["pr"])))[2:-2]
            metric=rms(At[2:-2]-target)/max(rms(scale),1e-14)
            charge=float(np.sum(self.vol*np.imag(np.conjugate(f)*P)))
            qrate=float(np.sum(self.vol*np.imag(np.conjugate(rhs[0])*P+np.conjugate(f)*rhs[1])))
            centre=lambda a:(9*a[0]-a[1])/8
            monotone=np.all(np.diff(M)>=-1e-9*max(abs(M[-1]),1.))
            # Origin-sensitive checks supplement bulk D4 residuals, which omit
            # the first two cells. A smooth spherical source obeys these to O(h^2).
            origin_ham=abs(3*M[0]/r[0]**3-(g["rho"][0]+g["v"][0]*g["S"][0]))/max(abs(g["rho"][0]),1e-14)
            origin_isotropy=float(max(abs(g["Kr"][:2]-k[:2]))/max(
                np.sqrt(ALPHA*max(abs(g["rho"][:2]))),max(abs(k[:2])),1e-14))
            return dict(t=float(t),central_proper_time=float(t*self.lapse_centre),
                charge=charge,ADM_mass=float(M[-1]),central_amplitude=float(abs(centre(f))),
                central_density=float(centre(g["rho"])),maximum_density=float(max(g["rho"])),
                minimum_F=float(min(g["F"])),minimum_A=float(min(g["A"])),
                maximum_compactness=float(1-min(g["F"])),maximum_abs_k=float(max(abs(k))),
                hamiltonian_residual=ham,metric_evolution_residual=metric,
                relative_charge_rate=abs(qrate)/max(abs(charge),1e-14),
                maximum_Courant=self.maximum_courant,
                origin_hamiltonian_residual=float(origin_ham),
                origin_isotropy_residual=origin_isotropy,
                mass_R50=float(np.interp(.5*M[-1],np.r_[0,M],np.r_[0,r])) if monotone else None,
                mass_R90=float(np.interp(.9*M[-1],np.r_[0,M],np.r_[0,r])) if monotone else None)
    return RegularGrid


def origin_regular_grid_factory(module):
    """Polar initializer with explicit regular radial powers in M'=b-q*M.

    Interpolate q/r and b/r**2, rather than q and b.  Constant smooth core
    sources then retain their exact r and r**2 dependence in every cell.
    The continuum constraint and the scalar gradient are unchanged.
    """
    from numba import njit
    nodes,weights=np.polynomial.legendre.leggauss(8)

    @njit(cache=False,fastmath=False)
    def recurrence(qfactor,ufactor,h,nodes,weights):
        n=len(qfactor);mass=np.empty(n);J=np.empty(n);r0=h/2
        J[0]=qfactor[0]*r0*r0/2;value=0.
        for j in range(len(nodes)):
            u=(nodes[j]+1)/2;r=r0*u
            remaining=qfactor[0]*r0*r0*(1-u*u)/2
            value+=weights[j]*np.exp(-remaining)*r*r*ufactor[0]
        mass[0]=r0*value/2;maximum_jump=J[0]
        for i in range(1,n):
            a=(i-.5)*h;q0=qfactor[i-1];q1=qfactor[i]
            jump=h*(q0*(a/2+h/6)+q1*(a/2+h/3))
            value=0.
            for j in range(len(nodes)):
                u=(nodes[j]+1)/2;z=1-u;r=a+h*u
                # Positive endpoint weights avoid cancellation for steep q.
                remaining=h*(q0*z*z*(a/2+h*(1+2*u)/6)+
                             q1*z*(a*(1+u)/2+h*(1+u+u*u)/3))
                source=r*r*(z*ufactor[i-1]+u*ufactor[i])
                value+=weights[j]*np.exp(-remaining)*source
            mass[i]=np.exp(-jump)*mass[i-1]+h*value/2
            J[i]=J[i-1]+jump;maximum_jump=max(maximum_jump,jump)
        # Last half-cell holds the smooth factors constant, not q and b.
        a=(n-.5)*h;length=h/2;outer_r=n*h
        jump=qfactor[-1]*(outer_r*outer_r-a*a)/2;value=0.
        for j in range(len(nodes)):
            u=(nodes[j]+1)/2;r=a+length*u
            remaining=qfactor[-1]*(outer_r-r)*(outer_r+r)/2
            value+=weights[j]*np.exp(-remaining)*r*r*ufactor[-1]
        outer=np.exp(-jump)*mass[-1]+length*value/2
        return mass,outer,J,J[-1]+jump,max(maximum_jump,jump)

    class OriginRegularGrid(module.Grid):
        def __init__(self,radius,h):
            super().__init__(radius,h)
            self.maximum_cell_delta_J=0.
        def geometry(self,field,momentum):
            grad=self.gradient(field);square=abs(field)**2
            potential=square/2-square*square/4+SEXTIC*square**3/6
            kinetic=abs(momentum)**2+abs(grad)**2
            qfactor=ALPHA*kinetic;ufactor=kinetic/2+potential
            if (not np.all(np.isfinite(qfactor)) or not np.all(np.isfinite(ufactor))
                    or np.min(qfactor)<0 or np.min(ufactor)<0):
                raise FloatingPointError("Invalid source in origin-regular mass quadrature")
            mass,outer,J,Jouter,jump=recurrence(qfactor,ufactor,self.h,nodes,weights)
            self.maximum_cell_delta_J=max(self.maximum_cell_delta_J,float(jump))
            N=1-2*ALPHA*mass/self.r;sigma=np.exp(J-Jouter);sigma0=float(np.exp(-Jouter))
            if (not np.all(np.isfinite(mass)) or not np.isfinite(outer) or np.min(N)<=0
                    or np.min(sigma)<=0 or sigma0<=0):
                raise FloatingPointError("Origin-regular initializer left positive-F polar slice")
            return dict(N=N,sigma=sigma,c=N*sigma,mass=mass,mass_outer=float(outer),
                        sigma0=sigma0,gradient=grad)
    return OriginRegularGrid


def regular_initial_data(module,mod64,solution,h,radius,kappa):
    old=origin_regular_grid_factory(module)(radius,h);r=old.r
    f,fp,M,ls=solution.sol(r);omega=mod64.omega_from_parameter(solution.p)
    P=1j*omega*f/(np.exp(ls)*(1-2*ALPHA*M/r))
    prepared=aggregate_phase_imprint(r,f,P,kappa)
    g=old.geometry(*prepared);L=g["sigma"]*np.sqrt(g["N"])
    grid=regular_grid_factory(module)(radius,h,L)
    state=np.array([prepared[0],prepared[1],g["mass"],np.zeros_like(r)],complex)
    new=grid.geometry(state)
    qold=float(np.sum(old.vol*np.imag(np.conjugate(prepared[0])*prepared[1])))
    qnew=float(np.sum(grid.vol*np.imag(np.conjugate(state[0])*state[1])))
    matching=dict(field=float(max(abs(state[0]-prepared[0]))),momentum=float(max(abs(state[1]-prepared[1]))),
        mass=float(max(abs(state[2].real-g["mass"]))),spatial_metric=float(max(abs(new["A"]-g["N"]))),
        charge=abs(qnew/qold-1),normal_momentum=float(max(abs(new["root"]*state[1]-np.sqrt(g["N"])*prepared[1]))))
    return grid,state,matching


def regular_algebra_controls():
    import sympy as sp
    r,a,M,k,kr,L,Lr,P2,D2,S,V=sp.symbols("r a M k kr L Lr P2 D2 S V",real=True)
    v=r*k;A=1-2*a*M/r+v*v;rho=(P2+A*D2)/2+V;pr=rho-2*V
    Mr=r*r*(rho+v*S);Ar=2*a*M/r**2-2*a*Mr/r+2*r*k*k+2*r*r*k*kr
    Kr=k+r*kr-a*r*S
    kt=L*v*kr+L*(k*k+a*M/r**3+a*pr)-A*Lr/r
    admkt=L*v*kr+L*((1-A)/r**2-Ar/(2*r)+(Kr+2*k)*k-2*a*V)-A*Lr/r
    Mt=L*r*r*(v*(P2+A*D2)+(A+v*v)*S)
    At=-2*a*Mt/r+2*r*r*k*kt
    identity=sp.simplify(At-L*v*Ar+2*r*k*A*Lr+2*a*L*r*A*S)
    bad=sp.simplify(identity+2*a/r*L*r*r*v*(P2+A*D2))
    return dict(ADM_angular=sp.simplify(kt-admkt)==0,independent_metric=identity==0,
                omitted_shift_mass_term_rejected=bad!=0,
                horizon_characteristics=sp.simplify(A-v*v-(1-2*a*M/r))==0)


def regular_case(module,mod64,solution,h=.05,duration=12.,radius=32.,courant=.1,kappa=.1):
    grid,state,match=regular_initial_data(module,mod64,solution,h,radius,kappa)
    sample_dt=.05;steps=int(np.ceil(sample_dt/(courant*h)));dt=sample_dt/steps
    grid.time_step=dt;records=[];status="COMPLETED";reason=None;t=0.
    try:
        records.append(grid.measure(state,t))
        for j in range(round(duration/sample_dt)):
            for i in range(steps):
                a=grid.rhs(state);b=grid.rhs(state+dt*a/2)
                c=grid.rhs(state+dt*b/2);d=grid.rhs(state+dt*c)
                state=state+dt*(a+2*b+2*c+d)/6;t+=dt
            records.append(grid.measure(state,t))
            if records[-1]["minimum_F"]<-.02:
                status="TRAPPED_REGION_CANDIDATE"
                break
    except Exception as error:
        status="NUMERICAL_OR_SLICE_LIMIT";reason=f"{type(error).__name__}: {error}"
    first=records[0] if records else None
    summary=dict(maximum_Courant=grid.maximum_courant)
    if records:
        summary.update(charge_drift=max(abs(s["charge"]/first["charge"]-1) for s in records),
            mass_drift=max(abs(s["ADM_mass"]/first["ADM_mass"]-1) for s in records),
            maximum_hamiltonian=max(s["hamiltonian_residual"] for s in records),
            maximum_metric_residual=max(s["metric_evolution_residual"] for s in records),
            maximum_charge_rate=max(s["relative_charge_rate"] for s in records))
    print(f"Regular gauge h={h} kappa={kappa} R={radius}: {status}, t={t:.4f}",file=sys.stderr,flush=True)
    return dict(h=h,radius=radius,courant=courant,dt=dt,kappa=kappa,duration=duration,
                status=status,error=reason,matching=match,summary=summary,samples=records,
                initial_lapse_centre=grid.lapse_centre)
def run_regular_suite(pilot=False):
    result=dict(code_sha256=sha(__file__),previous_sha256=REGULAR_PREVIOUS_SHA256,
                algebra=regular_algebra_controls(),cases={},pilot=bool(pilot))
    try:
        result["validation_controls"]=regular_validation_controls()
        if not all(result["validation_controls"].values()):
            raise RuntimeError("Regular gauge result-validator control failed")
        module,mod64,sol,bg,pins,base=aggregate_collapse_background()
        result.update(base_sha256=base,dependency_sha256=pins)
        result["origin_control"]=regular_origin_controls(module)
        if not all(result["origin_control"]["gates"].values()):
            raise RuntimeError("Regular origin consistency control failed")
        grid=regular_grid_factory(module)(8.,.05)
        zero=np.zeros((4,len(grid.r)),complex)
        controls=dict(vacuum=bool(max(abs(grid.rhs(zero)).ravel())==0))
        y=zero.copy();r=grid.r
        y[0]=.01*np.exp(-r*r)*(1+.2j*r*r);y[1]=.02j*np.exp(-r*r)
        y[2]=.01*r**3/(1+r**3);y[3]=.01*np.exp(-r*r)
        controls["charge_adjoint"]=grid.measure(y,0)["relative_charge_rate"]<1e-12
        pg=[]
        for h in (.05,.025,.0125):
            test=regular_grid_factory(module)(8.,h);r=test.r
            state=np.zeros((4,len(r)),complex);state[2]=25.
            state[3]=np.sqrt(2*ALPHA*25/r**3)
            rhs=test.rhs(state);g=test.geometry(state);inside=(r>=1)&(r<=7)
            error=float(max(abs(rhs[3,inside])/(1.5*abs(state[3,inside])**2)))
            pg.append(dict(h=h,error=error,minimum_A=float(min(g["A"])),
                           crosses_F_zero=bool(min(g["F"])<0 and max(g["F"])>0)))
        result["Schwarzschild_PG_control"]=pg
        controls["Schwarzschild_PG"]=pg[-1]["error"]<5e-3 and pg[-1]["error"]/pg[-2]["error"]<.6 and all(v["crosses_F_zero"] for v in pg)
        result["controls"]={k:bool(v) for k,v in controls.items()}
        if not all(result["algebra"].values()) or not all(controls.values()):
            raise RuntimeError("Regular gauge algebra or charge control failed")
        specs=[("coarse",.05,32.,.1,.1)]
        if not pilot:
            specs += [("middle",.025,32.,.1,.1),("fine",.0125,32.,.1,.1),
                      ("half_step",.0125,32.,.05,.1),("domain",.025,48.,.1,.1),
                      ("zero_middle",.025,32.,.1,0.),("zero_fine",.0125,32.,.1,0.)]
        for name,h,radius,courant,kappa in specs:
            result["cases"][name]=regular_case(module,mod64,sol,h=h,radius=radius,
                                               courant=courant,kappa=kappa)
        if not pilot:
            refs={}
            for h in (.0125,.00625):
                old=module.Grid(32.,h);r=old.r;f,fp,M,ls=sol.sol(r)
                P=1j*mod64.omega_from_parameter(sol.p)*f/(np.exp(ls)*(1-2*ALPHA*M/r))
                state=aggregate_phase_imprint(r,f,P,.1)
                old.time_step=.1*h
                rows=[];t=0.;tau=0.;previous_lapse=None
                for j in range(401):
                    g=old.geometry(*state);s=abs(state[0])**2
                    rho=g["N"]*(abs(state[1])**2+abs(g["gradient"])**2)/2+s/2-s*s/4+SEXTIC*s**3/6
                    if previous_lapse is not None:tau+=.025*(previous_lapse+g["sigma0"])
                    previous_lapse=g["sigma0"]
                    rows.append(dict(t=t,central_proper_time=tau,
                        central_amplitude=float(abs((9*state[0,0]-state[0,1])/8)),
                        central_density=float((9*rho[0]-rho[1])/8)))
                    if j%20==0:
                        rows[-1]["local_mass_flux_relative_l2"]=old.local_flux_check(state)["local_mass_flux_relative_l2"]
                    if j==400:break
                    for i in range(round(.05/old.time_step)):
                        dt=old.time_step;a=old.rhs(state);b=old.rhs(state+dt*a/2)
                        c=old.rhs(state+dt*b/2);d=old.rhs(state+dt*c)
                        state+=dt*(a+2*b+2*c+d)/6;t+=dt
                refs[str(h)]=rows
            result["polar_centre_references"]=refs
            last=min(c["samples"][-1]["t"] for c in result["cases"].values())
            last_tenth=int(np.floor(10*last+1e-6))
            result["last_common_interval"]=regular_verdict(result["cases"],refs,last_tenth/10)
            result["validated_prefix"]=None
            for n in range(last_tenth,0,-1):
                verdict=regular_verdict(result["cases"],refs,n/10)
                if verdict["passed"]:
                    result["validated_prefix"]=verdict
                    break
        result["source_unchanged"]=sha(__file__)==result["code_sha256"]
        result["dependencies_unchanged"]=sha(HERE/"nonlinear_equilibrium_evolution.py")==base and all(sha(module.SF/p)==v for p,v in pins.items())
        result["status"]=("PILOT_RECORDED" if pilot else "VALIDATED_REGULAR_PREFIX_ENDPOINT_OPEN"
            if result["validated_prefix"] and result["source_unchanged"] and result["dependencies_unchanged"]
            else "REGULAR_GAUGE_VALIDATION_OPEN")
    except Exception as error:
        result.update(status="DIAGNOSTIC_FAILED",error=f"{type(error).__name__}: {error}")
    print(json.dumps(result,indent=2,allow_nan=False))
    # Execution alone never closes the cross-gauge/refinement gates.
    return 0 if (pilot and result.get("status")=="PILOT_RECORDED"
        and result.get("source_unchanged") and result.get("dependencies_unchanged")
        and all(c["status"]=="COMPLETED" for c in result["cases"].values())) else 1


def regular_verdict(cases,refs,end,reference_key="local_mass_flux_relative_l2"):
    from scipy.interpolate import PchipInterpolator
    names=("coarse","middle","fine","half_step","domain")
    # Result validation must reject corrupt/shifted data, not just count rows.
    try:
        if not np.isfinite(end) or end<=0 or abs(end/.05-round(end/.05))>1e-7:
            return dict(end=end,passed=False,gates={"window":False})
        expected=np.arange(round(end/.05)+1)*.05
        all_names=names+("zero_middle","zero_fine")
        rows={n:[s for s in cases[n]["samples"] if s["t"]<=end+1e-7] for n in all_names}
        required=("t","central_proper_time","charge","ADM_mass","central_amplitude",
            "central_density","minimum_F","minimum_A","maximum_Courant",
            "relative_charge_rate","hamiltonian_residual","metric_evolution_residual",
            "origin_hamiltonian_residual","origin_isotropy_residual")
        for n in all_names:
            trace=rows[n]
            if len(trace)!=len(expected) or not np.allclose(
                    [s["t"] for s in trace],expected,rtol=0,atol=1e-7):
                return dict(end=end,passed=False,gates={"coverage":False})
            if (not np.all(np.isfinite([[s[k] for k in required] for s in trace]))
                or trace[0]["charge"]==0 or trace[0]["ADM_mass"]==0
                or not np.all(np.diff([s["central_proper_time"] for s in trace])>0)
                or abs(trace[0]["central_proper_time"])>1e-7
                or not cases[n]["matching"]
                or not np.all(np.isfinite(list(cases[n]["matching"].values())))):
                return dict(end=end,passed=False,gates={"finite_inputs":False})
        for h in ("0.0125","0.00625"):
            trace=refs[h];flux=[s[reference_key] for s in trace if reference_key in s]
            if (len(trace)<2 or not flux or not np.all(np.isfinite(flux))
                or not np.all(np.isfinite([[s[k] for k in
                    ("central_proper_time","central_amplitude","central_density")] for s in trace]))
                or abs(trace[0]["central_proper_time"])>1e-7
                or not np.all(np.diff([s["central_proper_time"] for s in trace])>0)):
                return dict(end=end,passed=False,gates={"reference_inputs":False})
    except (KeyError,TypeError,ValueError):
        return dict(end=end,passed=False,gates={"input_structure":False})
    keys=("central_amplitude","central_density","minimum_F","minimum_A")
    budgets={n:dict(Q=max(abs(s["charge"]/rows[n][0]["charge"]-1) for s in rows[n]),
                    M=max(abs(s["ADM_mass"]/rows[n][0]["ADM_mass"]-1) for s in rows[n]),
                    CFL=max(s["maximum_Courant"] for s in rows[n]),
                    Qrate=max(s["relative_charge_rate"] for s in rows[n])) for n in names}
    wave=lambda n,k:np.array([s[k] for s in rows[n]])
    def errors(a,b):
        return {k:float(np.sqrt(np.mean((wave(a,k)-wave(b,k))**2))/max(np.sqrt(np.mean(wave(b,k)**2)),1e-14)) for k in keys}
    em,ef,et,ed=errors("coarse","middle"),errors("middle","fine"),errors("fine","half_step"),errors("middle","domain")
    ratios={k:ef[k]/max(em[k],1e-14) for k in keys}
    gates=dict(coverage=True,finite_inputs=True,reference_inputs=True,
        charge=max(v["Q"] for v in budgets.values())<1e-5,
        mass=max(v["M"] for v in budgets.values())<5e-3,CFL=max(v["CFL"] for v in budgets.values())<.4,
        semidiscrete_charge=max(v["Qrate"] for v in budgets.values())<1e-10,
        initial_matching=all(max(cases[n]["matching"].values())<1e-10 for n in names),
        refinement=all(ef[k]<5e-3 or ratios[k]<.6 for k in keys),
        time_control=max(et.values())<5e-3,domain_control=max(ed.values())<5e-3)
    residuals={}
    for key in ("hamiltonian_residual","metric_evolution_residual",
                "origin_hamiltonian_residual","origin_isotropy_residual"):
        middle=max(s[key] for s in rows["middle"]);fine=max(s[key] for s in rows["fine"])
        ratio=fine/max(middle,1e-14);gates[key]=fine<5e-3 and (fine<1e-6 or ratio<.6)
        residuals[key]=dict(middle=middle,fine=fine,ratio=ratio)
    cross={}
    common_tau=min(rows["fine"][-1]["central_proper_time"],rows["middle"][-1]["central_proper_time"],
                   refs["0.00625"][-1]["central_proper_time"],refs["0.0125"][-1]["central_proper_time"])
    target=np.linspace(0,common_tau,301)
    for name,h in (("middle","0.0125"),("fine","0.00625")):
        cross[name]={}
        for key in ("central_amplitude","central_density"):
            def curve(data):
                return PchipInterpolator([s["central_proper_time"] for s in data],[s[key] for s in data])(target)
            a,b=curve(rows[name]),curve(refs[h])
            cross[name][key]=float(max(abs(a-b))/max(max(abs(b)),1e-14))
    gates["cross_gauge"]=all(cross["fine"][k]<5e-3 and
        (cross["fine"][k]<1e-6 or cross["fine"][k]/max(cross["middle"][k],1e-14)<.6) for k in cross["fine"])
    ref_residual={h:max(s.get(reference_key,0.) for s in refs[h]) for h in refs}
    ref_gate="polar_reference_accuracy" if reference_key=="local_mass_flux_relative_l2" else "fixed_reference_accuracy"
    gates[ref_gate]=ref_residual["0.00625"]<5e-3 and ref_residual["0.00625"]/max(ref_residual["0.0125"],1e-14)<.6
    zero={}
    for name in ("zero_middle","zero_fine"):
        trace=[s for s in cases[name]["samples"] if s["t"]<=end+1e-7]
        zero[name]={k:max(abs(s[k]/trace[0][k]-1) for s in trace) for k in ("central_amplitude","central_density","ADM_mass","charge")}
    gates["zero_flow"]=max(zero["zero_fine"].values())<5e-3
    return dict(end=end,passed=bool(all(gates.values())),gates={k:bool(v) for k,v in gates.items()},
        budgets=budgets,residuals=residuals,convergence=dict(middle_fine=ef,ratios=ratios,half_step=et,domain=ed),
        cross_gauge=dict(proper_time_end=common_tau,
            covers_regular_prefix=bool(common_tau>=rows["fine"][-1]["central_proper_time"]-1e-7),
            errors=cross,reference_residual_kind=reference_key,
            reference_residual=ref_residual),zero_flow=zero,
        first=rows["fine"][0],last=rows["fine"][-1])


def regular_validation_controls(return_fixture=False):
    """Synthetic parser/verdict checks, not physical evolutions."""
    from copy import deepcopy
    names=("coarse","middle","fine","half_step","domain","zero_middle","zero_fine")
    cases={}
    for n in names:
        residual=.0004 if n in ("coarse","middle","domain","zero_middle") else .0001
        samples=[dict(t=.05*j,central_proper_time=.025*j,charge=1.,ADM_mass=1.,
            central_amplitude=2.,central_density=4.,minimum_F=.6,minimum_A=.6,
            maximum_Courant=.1,relative_charge_rate=0.,hamiltonian_residual=residual,
            metric_evolution_residual=residual,origin_hamiltonian_residual=residual,
            origin_isotropy_residual=residual) for j in range(5)]
        cases[n]=dict(samples=samples,matching={"field":0.})
    refs={h:[dict(s,local_mass_flux_relative_l2=res) for s in cases["fine"]["samples"]]
          for h,res in (("0.0125",.0004),("0.00625",.0001))}
    if return_fixture:return cases,refs
    controls={"valid_fixture":regular_verdict(cases,refs,.2)["passed"]}
    mutations={
        "shifted_time":("t",.11), "nonfinite_field":("central_amplitude",float("nan")),
        "nonfinite_residual":("metric_evolution_residual",float("nan")),
        "charge_drift":("charge",1.01), "mass_drift":("ADM_mass",1.01),
        "hamiltonian_failure":("hamiltonian_residual",.1),
        "metric_failure":("metric_evolution_residual",.1),
        "origin_failure":("origin_isotropy_residual",.1)}
    for name,(key,value) in mutations.items():
        bad=deepcopy(cases);bad["fine"]["samples"][2][key]=value
        controls[name+"_rejected"]=not regular_verdict(bad,refs,.2)["passed"]
    bad=deepcopy(cases);bad["zero_fine"]["samples"].pop()
    controls["missing_zero_sample_rejected"]=not regular_verdict(bad,refs,.2)["passed"]
    bad=deepcopy(cases);bad["fine"]["matching"]["field"]=.01
    controls["mismatched_initial_slice_rejected"]=not regular_verdict(bad,refs,.2)["passed"]
    bad=deepcopy(refs);bad["0.00625"][2]["central_proper_time"]=0.
    controls["nonmonotone_reference_rejected"]=not regular_verdict(cases,bad,.2)["passed"]
    controls["uncovered_window_rejected"]=not regular_verdict(cases,refs,.3)["passed"]
    shorter={h:trace[:-1] for h,trace in refs.items()}
    controls["overlap_not_full_coverage"]=not regular_verdict(cases,shorter,.2)["cross_gauge"]["covers_regular_prefix"]
    return {k:bool(v) for k,v in controls.items()}


def regular_origin_controls(module):
    """Exact static constant-potential core; tests include the FIRST cell."""
    rows=[]
    for h in (.05,.025,.0125,.00625):
        data={"h":h}
        for name,factory in (("old",fitted_grid_factory),("corrected",origin_regular_grid_factory)):
            grid=factory(module)(4.,h);r=grid.r
            field=np.full(len(r),np.sqrt(2),complex);P=np.zeros(len(r),complex)
            g=grid.geometry(field,P);lapse=g["sigma"]*np.sqrt(g["N"])
            new=regular_grid_factory(module)(4.,h,lapse)
            state=np.array([field,P,g["mass"],np.zeros(len(r))],complex)
            rhs=new.rhs(state)
            exact_mass=r**3/9
            data[name]=dict(central_k_rate=float(abs(rhs[3,0])),
                mass_relative_error=float(max(abs(g["mass"]/exact_mass-1))),
                scalar_rate=float(max(abs(rhs[:2]).ravel())))
        rows.append(data)
    coarse,fine=rows[-2],rows[-1]
    error=fine["corrected"]["central_k_rate"]
    gates=dict(constant_density_mass=fine["corrected"]["mass_relative_error"]<1e-11,
        scalar_stationarity=fine["corrected"]["scalar_rate"]<1e-12,
        corrected_central_stationarity=error<1e-6 and
            (error<1e-10 or error/coarse["corrected"]["central_k_rate"]<.6),
        original_bias_detected=fine["old"]["central_k_rate"]>1e-4 and
            fine["old"]["central_k_rate"]/coarse["old"]["central_k_rate"]>.9)
    return dict(rows=rows,gates={k:bool(v) for k,v in gates.items()})
# END SAME-SLICE HORIZON-REGULAR HELPERS


# BEGIN REGULAR CENTRAL VARIABLES / DYNAMICAL CLOCK
CLOCK_PREVIOUS_SHA256="ee348a45a6c683674e328ba945f2c6dff4232693a97f96e9a67e8ef20e487730"
CLOCK_TARGET_PROPER_TIME=3.549321393


class CentralClockGrid:
    """Same spherical system in (phi,P,mu,k,log L,tau_c); no source change."""
    def __init__(self,module,radius,h,mode="harmonic"):
        if mode not in ("harmonic","one_plus_log","frozen"):
            raise ValueError("Unknown lapse prescription")
        self.engine=regular_grid_factory(module)(radius,h)
        self.r,self.h,self.radius=self.engine.r,h,radius
        self.mode=mode
    def cell_k(self,state):
        return state[3].real
    def unpack(self,state):
        if state.shape!=(6,len(self.r)) or not np.all(np.isfinite(state)):
            raise FloatingPointError("Invalid regular central state")
        self.engine.lapse=np.exp(state[4].real)
        self.engine.lapse_r=self.engine.derivative(self.engine.lapse)
        self.engine.lapse_centre=float(np.exp((9*state[4,0].real-state[4,1].real)/8))
        return np.array([state[0],state[1],self.r**3*state[2].real,self.cell_k(state)],complex)
    def rhs(self,state):
        raw=self.unpack(state);e=self.engine;g=e.geometry(raw);r=self.r
        L=e.lapse;mu,k,ell=state[2].real,self.cell_k(state),state[4].real
        f=2/L if self.mode=="one_plus_log" else np.ones_like(r)
        gauge_speed=max(abs(g["beta"])+L*g["root"]*np.sqrt(f))
        if e.time_step is not None:
            e.maximum_courant=max(e.maximum_courant,e.time_step*gauge_speed/self.h)
            if e.maximum_courant>=.4:
                raise FloatingPointError("Dynamical-clock matter/gauge Courant bound exceeded")
        old=e.rhs(raw);out=np.zeros_like(state);out[:2]=old[:2]
        B=g["root"]*np.real(np.conjugate(state[1])*(g["gradient"]/r))
        ell_r=e.derivative(ell);k_r=e.derivative(k)
        out[2]=L*(k*g["A"]*(abs(state[1])**2+abs(g["gradient"])**2)
                   +(g["A"]+r*r*k*k)*B)
        out[3]=g["beta"]*k_r+L*(k*k+ALPHA*mu+ALPHA*g["pr"]-g["A"]*ell_r/r)
        K=3*k+r*k_r-ALPHA*r*r*B
        if self.mode!="frozen":out[4]=g["beta"]*ell_r-L*f*K
        out[5]=e.lapse_centre
        return out
    def measure(self,state,t):
        raw=self.unpack(state);e=self.engine;row=e.measure(raw,t)
        rhs=self.rhs(state);g=e.geometry(raw);r=self.r;L=e.lapse
        mu,k,ell=state[2].real,self.cell_k(state),state[4].real
        B=g["S"]/r;H=k*k-2*ALPHA*mu
        constraint=3*mu+r*e.derivative(mu)-g["rho"]-r*r*k*B
        row["regular_centre_constraint"]=float(max(abs(constraint[:2]))/max(max(abs(g["rho"][:2])),1e-14))
        terms=(2*k*self.cell_k(rhs),-2*ALPHA*rhs[2].real,
               -L*k*(2*H+r*e.derivative(H)),
               2*L*k*g["A"]*e.derivative(ell)/r,2*ALPHA*L*g["A"]*B)
        active=r<=15.
        scale=sum(abs(x) for x in terms)+ALPHA*L*(abs(g["rho"])+abs(g["pr"]))
        row["regular_metric_residual"]=float(np.linalg.norm(sum(terms)[active])/max(np.linalg.norm(scale[active]),1e-14))
        row["central_proper_time"]=float(state[5,0].real)
        row["central_lapse"]=e.lapse_centre
        row["minimum_lapse"]=float(min(L))
        row["maximum_Courant"]=e.maximum_courant
        j=int(np.argmin(g["F"]));theta_plus=2*(g["root"]-g["v"])/r
        theta_minus=-2*(g["root"]+g["v"])/r
        row["minimum_F_areal_radius"]=float(r[j])
        row["outgoing_expansion_at_minimum_F"]=float(theta_plus[j])
        row["ingoing_expansion_at_minimum_F"]=float(theta_minus[j])
        row["future_trapped_points"]=int(np.sum((theta_plus<0)&(theta_minus<0)))
        marginal=[]
        for i in np.flatnonzero(g["F"][:-1]*g["F"][1:]<0):
            weight=-g["F"][i]/(g["F"][i+1]-g["F"][i])
            if (1-weight)*g["v"][i]+weight*g["v"][i+1]>0:
                marginal.append(float(r[i]+weight*self.h))
        row["future_marginal_radii"]=marginal
        return row


class StaggeredClockGrid(CentralClockGrid):
    """Store v=r*k on radial faces; ell stays on cells. v(0)=0 by parity."""
    def cell_k(self,state):
        faces=np.r_[0.,state[3].real]
        return (faces[:-1]+faces[1:])/(2*self.r)
    def to_faces(self,x):
        return np.r_[(x[:-1]+x[1:])/2,1.5*x[-1]-.5*x[-2]]
    def face_gradient(self,x):
        return np.r_[np.diff(x)/self.h,(2*x[-1]-3*x[-2]+x[-3])/self.h]
    def divergence(self,v):
        return np.diff(self.engine.edges**2*np.r_[0.,v])/self.engine.vol
    def rhs(self,state):
        out=super().rhs(state);raw=self.unpack(state);e=self.engine
        g=e.geometry(raw);r=self.r;rf=e.edges[1:]
        vf=state[3].real;ell=state[4].real;L=e.lapse
        ellf=self.to_faces(ell);Lf=np.exp(ellf);muf=self.to_faces(state[2].real)
        Af=1-2*ALPHA*rf*rf*muf+vf*vf
        if np.min(Af)<=0 or not np.all(np.isfinite(Af)):
            raise FloatingPointError("Staggered faces lost positive A")
        f=2/L if self.mode=="one_plus_log" else np.ones_like(r)
        ff=2/Lf if self.mode=="one_plus_log" else np.ones_like(rf)
        if e.time_step is not None:
            speed=max(abs(Lf*vf)+Lf*np.sqrt(Af*ff))
            e.maximum_courant=max(e.maximum_courant,e.time_step*speed/self.h)
            if e.maximum_courant>=.4:raise FloatingPointError("Staggered gauge Courant bound exceeded")
        dv=np.r_[(np.r_[vf[1:],0.]-np.r_[0.,vf[:-1]])[:-1]/(2*self.h),
                   (3*vf[-1]-4*vf[-2]+vf[-3])/(2*self.h)]
        out[3]=Lf*vf*dv+ALPHA*Lf*rf*(muf+self.to_faces(g["pr"]))-Lf*Af*self.face_gradient(ell)
        if self.mode!="frozen":
            out[4]=g["beta"]*e.derivative(ell)-L*f*(self.divergence(vf)-ALPHA*r*g["S"])
        return out


def clock_initial_data(module,mod64,solution,h,radius,kappa,mode,staggered=False):
    old,raw,matching=regular_initial_data(module,mod64,solution,h,radius,kappa)
    factory=StaggeredClockGrid if staggered else CentralClockGrid
    grid=factory(module,radius,h,mode)
    state=np.zeros((6,len(grid.r)),complex)
    state[:2]=raw[:2];state[2]=raw[2]/grid.r**3;state[3]=raw[3]
    state[4]=np.log(old.lapse)
    if staggered and max(abs(raw[3]))!=0:
        raise ValueError("Staggered initializer requires the registered zero-k initial slice")
    mapped=grid.unpack(state)
    matching=dict(matching,regular_variable_map=float(max(abs(mapped-raw).ravel())),
                  lapse_map=float(max(abs(grid.engine.lapse-old.lapse))))
    return grid,state,matching


def clock_rk4(grid,state,dt):
    a=grid.rhs(state);b=grid.rhs(state+dt*a/2)
    c=grid.rhs(state+dt*b/2);d=grid.rhs(state+dt*c)
    return state+dt*(a+2*b+2*c+d)/6


def clock_controls(module,staggered=False):
    import sympy as sp
    r,L,k,A,B,P2,D2=sp.symbols("r L k A B P2 D2",real=True)
    mut=L*(k*A*(P2+D2)+(A+r*r*k*k)*B)
    Mt=L*r*r*(r*k*A*(P2+D2)+(A+r*r*k*k)*r*B)
    checks={"mass_equivalence":sp.simplify(r**3*mut-Mt)==0}
    factory=StaggeredClockGrid if staggered else CentralClockGrid
    grid=factory(module,4.,.1)
    zero=np.zeros((6,len(grid.r)),complex)
    rhs=grid.rhs(zero)
    checks["vacuum"]=bool(max(abs(rhs[:5]).ravel())==0 and max(abs(rhs[5]-1))==0)
    errors={}
    # Exact contracting flat-slice constant-potential spacetime: k,mu fixed;
    # only L and tau evolve. This independently tests the dynamical clock.
    for mode in ("harmonic","one_plus_log"):
        vals=[]
        for dt in (.05,.025):
            g=factory(module,4.,.1,mode);s=zero.copy()
            kval=np.sqrt(2*ALPHA/9);L0=.7
            s[0]=np.sqrt(2);s[2]=1/9;s[3]=kval;s[4]=np.log(L0)
            if staggered:s[3]=kval*g.engine.edges[1:]
            for _ in range(round(1/dt)):s=clock_rk4(g,s,dt)
            lapse=L0/(1+3*kval*L0) if mode=="harmonic" else L0*np.exp(-6*kval)
            tau=np.log1p(3*kval*L0)/(3*kval) if mode=="harmonic" else L0*(-np.expm1(-6*kval))/(6*kval)
            vals.append(float(max(abs(np.exp(s[4,0].real)-lapse),abs(s[5,0].real-tau),
                                      max(abs(s[2]-1/9)),max(abs(g.cell_k(s)-kval)))))
        errors[mode]=vals
        checks[mode+"_clock"]=vals[-1]<1e-8 and (vals[-1]<1e-12 or vals[-1]/max(vals[0],1e-30)<.2)
    if staggered:
        r=grid.r;rf=grid.engine.edges[1:];n=len(r);h=grid.h
        checks["quadratic_face_gradient"]=max(abs(grid.face_gradient(r*r)-2*rf))<1e-11
        checks["linear_radial_divergence"]=max(abs(grid.divergence(rf)-3))<1e-11
        G=np.diff(np.eye(n),axis=0)/h
        Wc=np.diag(grid.engine.vol);Wf=np.diag(rf[:-1]**2*h)
        D=np.column_stack([grid.divergence(np.r_[np.eye(n-1)[:,j],0.]) for j in range(n-1)])
        adjoint=float(np.linalg.norm(Wc@D+G.T@Wf))
        checks["gauge_weighted_adjoint"]=adjoint<1e-11
        errors["gauge_adjoint_residual"]=adjoint
    from copy import deepcopy
    cases,refs=regular_validation_controls(return_fixture=True)
    for case in cases.values():
        for s in case["samples"]:
            s.update(regular_centre_constraint=s["hamiltonian_residual"],
                regular_metric_residual=s["metric_evolution_residual"],future_trapped_points=0,
                outgoing_expansion_at_minimum_F=1.,ingoing_expansion_at_minimum_F=-1.)
    for trace in refs.values():
        for s in trace:s["reference_accuracy_residual"]=s["local_mass_flux_relative_l2"]
    checks["clock_verdict_fixture"]=clock_verdict(cases,refs,.2)["passed"]
    for key in ("regular_centre_constraint","regular_metric_residual"):
        bad=deepcopy(cases);bad["fine"]["samples"][2][key]=float("nan")
        checks[key+"_nonfinite_rejected"]=not clock_verdict(bad,refs,.2)["passed"]
    return dict(gates={k:bool(v) for k,v in checks.items()},clock_errors=errors)


def clock_case(module,mod64,solution,h=.05,duration=24.,radius=32.,courant=.1,kappa=.1,mode="harmonic",staggered=False,interior=False):
    grid,state,matching=clock_initial_data(module,mod64,solution,h,radius,kappa,mode,staggered)
    steps=int(np.ceil(.05/(courant*h)));dt=.05/steps;grid.engine.time_step=dt
    rows=[];t=0.;status="COMPLETED";reason=None
    try:
        rows.append(interior_measure(grid,state,t) if interior else grid.measure(state,t))
        for j in range(round(duration/.05)):
            for _ in range(steps):state=clock_rk4(grid,state,dt);t+=dt
            rows.append(interior_measure(grid,state,t) if interior else grid.measure(state,t))
            if not interior and rows[-1]["minimum_F"]<-.02:
                status="TRAPPED_REGION_CANDIDATE";break
    except Exception as error:
        status="NUMERICAL_LIMIT";reason=f"{type(error).__name__}: {error}"
    print(f"Clock {mode} h={h} kappa={kappa} R={radius}: {status}, t={t:.4f}",file=sys.stderr,flush=True)
    return dict(h=h,radius=radius,courant=courant,dt=dt,kappa=kappa,mode=mode,staggered=staggered,duration=duration,
                status=status,error=reason,matching=matching,samples=rows)


def clock_verdict(cases,refs,end):
    try:
        required=("regular_centre_constraint","regular_metric_residual",
            "future_trapped_points","outgoing_expansion_at_minimum_F","ingoing_expansion_at_minimum_F")
        if not all(np.all(np.isfinite([[s[k] for k in required] for s in c["samples"] if s["t"]<=end+1e-7]))
                   for c in cases.values()):
            return dict(end=end,passed=False,gates={"clock_finite_inputs":False})
    except (KeyError,TypeError,ValueError):
        return dict(end=end,passed=False,gates={"clock_input_structure":False})
    result=regular_verdict(cases,refs,end,reference_key="reference_accuracy_residual")
    if not result.get("budgets"):return result
    for key in ("regular_centre_constraint","regular_metric_residual"):
        values={n:max(s[key] for s in cases[n]["samples"] if s["t"]<=end+1e-7) for n in ("middle","fine")}
        a,b=values["middle"],values["fine"];ratio=b/max(a,1e-14)
        result["gates"][key]=bool(np.isfinite(b) and b<.005 and (b<1e-6 or ratio<.6))
        result["residuals"][key]=dict(middle=a,fine=b,ratio=ratio)
    result["passed"]=all(result["gates"].values())
    result["proper_time_extended"]=bool(result["passed"] and result["last"]["central_proper_time"]>CLOCK_TARGET_PROPER_TIME)
    last={n:[s for s in cases[n]["samples"] if s["t"]<=end+1e-7][-1]
          for n in ("coarse","middle","fine","half_step","domain")}
    result["future_trapped_region_resolved"]=bool(result["passed"] and
        last["fine"]["future_trapped_points"]>=4 and all(
            s["minimum_F"]<-.005 and s["future_trapped_points"]>0 and
            s["outgoing_expansion_at_minimum_F"]<0 and s["ingoing_expansion_at_minimum_F"]<0
            for s in last.values()))
    return result


def clock_parallel_job(spec):
    name,h,radius,courant,kappa,mode,staggered=spec
    module,mod64,sol,_,_,_=aggregate_collapse_background()
    if mode=="fixed":
        return regular_case(module,mod64,sol,h=h,radius=radius,duration=9.4)
    return clock_case(module,mod64,sol,h=h,radius=radius,courant=courant,
                      kappa=kappa,mode=mode,staggered=staggered)


def run_clock_suite(mode="harmonic",pilot=False,checks_only=False,staggered=False,pilot_h=.05):
    result=dict(code_sha256=sha(__file__),previous_sha256=CLOCK_PREVIOUS_SHA256,mode=mode,staggered=staggered,cases={})
    try:
        module,mod64,sol,bg,pins,base=aggregate_collapse_background()
        result.update(base_sha256=base,dependency_sha256=pins,controls=clock_controls(module,staggered))
        if not all(result["controls"]["gates"].values()):
            raise RuntimeError("Dynamical-clock control failed")
        if not checks_only:
            specs=[("coarse",pilot_h if pilot else .05,32.,.1,.1)]
            if not pilot:
                specs += [("middle",.025,32.,.1,.1),("fine",.0125,32.,.1,.1),
                    ("half_step",.0125,32.,.05,.1),("domain",.025,48.,.1,.1),
                    ("zero_middle",.025,32.,.1,0.),("zero_fine",.0125,32.,.1,0.)]
            precomputed_refs={}
            if staggered and not pilot:
                from concurrent.futures import ProcessPoolExecutor
                jobs=[(*s,mode,staggered) for s in specs]+[
                    ("reference_"+str(h),h,32.,.1,.1,"fixed",False) for h in (.0125,.00625)]
                with ProcessPoolExecutor(max_workers=3) as pool:
                    for spec,value in zip(jobs,pool.map(clock_parallel_job,jobs)):
                        name=spec[0]
                        if name.startswith("reference_"):precomputed_refs[name[10:]]=value
                        else:result["cases"][name]=value
                result["parallel_workers"]=3
            else:
                for name,h,radius,courant,kappa in specs:
                    result["cases"][name]=clock_case(module,mod64,sol,h=h,radius=radius,
                                                   courant=courant,kappa=kappa,mode=mode,staggered=staggered)
            if not pilot:
                refs={}
                for h in (.0125,.00625):
                    reference=precomputed_refs[str(h)] if precomputed_refs else regular_case(module,mod64,sol,h=h,duration=9.4)
                    if reference["status"]!="COMPLETED":raise RuntimeError("Fixed-lapse reference failed")
                    rows=reference["samples"]
                    for row in rows:
                        row["reference_accuracy_residual"]=max(row[k] for k in (
                            "hamiltonian_residual","metric_evolution_residual","origin_hamiltonian_residual","origin_isotropy_residual"))
                    refs[str(h)]=rows
                result["fixed_references"]=refs
                last=min(c["samples"][-1]["t"] for c in result["cases"].values())
                last_tenth=int(np.floor(10*last+1e-6))
                result["last_common_interval"]=clock_verdict(result["cases"],refs,last_tenth/10)
                result["validated_prefix"]=None
                for j in range(last_tenth,0,-1):
                    verdict=clock_verdict(result["cases"],refs,j/10)
                    if verdict["passed"]:result["validated_prefix"]=verdict;break
        result["source_unchanged"]=sha(__file__)==result["code_sha256"]
        result["dependencies_unchanged"]=sha(HERE/"nonlinear_equilibrium_evolution.py")==base and all(sha(module.SF/p)==v for p,v in pins.items())
        if not result["source_unchanged"] or not result["dependencies_unchanged"]:
            raise RuntimeError("Dynamical-clock input/source changed during run")
        result["status"]=("CLOCK_CONTROLS_PASSED" if checks_only else "CLOCK_PILOT_RECORDED" if pilot
            else "CLOCK_PREFIX_EXTENDED_ENDPOINT_OPEN" if result["validated_prefix"] and result["validated_prefix"]["proper_time_extended"]
            else "CLOCK_EXTENSION_OPEN")
    except Exception as error:
        result.update(status="DIAGNOSTIC_FAILED",error=f"{type(error).__name__}: {error}")
    print(json.dumps(result,indent=2,allow_nan=False))
    return 0 if checks_only and result["status"]=="CLOCK_CONTROLS_PASSED" else 1
# END REGULAR CENTRAL VARIABLES / DYNAMICAL CLOCK


# BEGIN INTERIOR CURVATURE DIAGNOSTIC
INTERIOR_PREVIOUS_SHA256="e2fd0b51e8c64758a54b59e85a958b7789fbf3cf896e584e994d1b0670afa4d7"
INTERIOR_TARGET_PROPER_TIME=3.853043340
CURVATURE_KEYS=("central_Ricci_scalar","central_Ricci_square",
                "central_Kretschmann","maximum_abs_Kretschmann")


def spherical_curvature(mu,rho,pr,pt,normal_flux):
    """On-shell invariants, -+++ and G_ab=2*ALPHA*T_ab; flux is orthonormal."""
    R=2*ALPHA*(rho-pr-2*pt)
    Ricci2=4*ALPHA**2*(rho*rho+pr*pr+2*pt*pt-2*normal_flux**2)
    Weyl2=48*ALPHA**2*(mu-(rho-pr+pt)/3)**2
    return dict(Ricci_scalar=R,Ricci_square=Ricci2,Weyl_square=Weyl2,
                Kretschmann=Weyl2+2*Ricci2-R*R/3)


def interior_measure(grid,state,t):
    row=grid.measure(state,t);g=grid.engine.geometry(grid.unpack(state))
    P=state[1];D=g["gradient"]
    inv=scalar_curvature(state[2].real,g["A"],P,D,g["V"])
    for key,values in inv.items():
        if not np.all(np.isfinite(values)):
            raise FloatingPointError("Nonfinite curvature: "+key)
        # Signed extrapolation estimate: even a squared invariant can have
        # a small negative O(h^4) estimate when its exact central value is zero.
        row["central_"+key]=float((9*values[0]-values[1])/8)
        row["maximum_abs_"+key]=float(max(abs(values)))
    # Algebraically nonnegative canonical-scalar radial null contractions.
    row["minimum_radial_null_source"]=float(min(np.minimum(
        g["A"]*abs(P+D)**2,g["A"]*abs(P-D)**2)))
    return row


def scalar_curvature(mu,A,P,D,V):
    """Equivalent scalar-specific sum-of-squares form reduces cancellation."""
    z=A*(abs(P)**2-abs(D)**2);I=np.imag(A*np.conjugate(P)*D)
    W=mu-z/6-V/3
    return dict(Ricci_scalar=2*ALPHA*(4*V-z),
        Ricci_square=4*ALPHA**2*((z-V)**2+3*V**2+2*I**2),
        Weyl_square=48*ALPHA**2*W**2,
        Kretschmann=48*ALPHA**2*W**2+4*ALPHA**2*(
            5*(z-2*V/5)**2/3+12*V**2/5+4*I**2))


def interior_controls():
    import sympy as sp
    mu,rho,pr,pt,j=sp.symbols("mu rho pr pt j",real=True)
    a=sp.Rational(1,25)
    R=2*a*(rho-pr-2*pt);Ricci2=4*a*a*(rho*rho+pr*pr+2*pt*pt-2*j*j)
    W2=48*a*a*(mu-(rho-pr+pt)/3)**2
    # Independently contract the six spherical orthonormal curvature blocks.
    x=a*(rho-pr+2*pt)-2*a*mu;y=a*(pr+mu);z=a*(rho-mu);w=2*a*mu;b=a*j
    contraction=4*(x*x+2*y*y+2*z*z+w*w-4*b*b)
    checks={"spherical_tensor_contraction":sp.expand(contraction-W2-2*Ricci2+R*R/3)==0}
    flat=spherical_curvature(0.,0.,0.,0.,0.)
    checks["Minkowski"]=all(v==0 for v in flat.values())
    vac=spherical_curvature(2.,0.,0.,0.,0.)
    checks["Schwarzschild"]=abs(vac["Kretschmann"]-48*(ALPHA*2)**2)<1e-13
    V=1/3;core=spherical_curvature(V/3,V,-V,-V,0.)
    checks["constant_potential"]=max(abs(core["Ricci_scalar"]-8*ALPHA*V),
        abs(core["Ricci_square"]-16*ALPHA**2*V*V),abs(core["Weyl_square"]),
        abs(core["Kretschmann"]-32*ALPHA**2*V*V/3))<1e-13
    # Radial Lorentz boost of a fixed tensor; angular sectional curvature
    # and areal mass are boost invariant. This exposes a missing A in flux².
    v=.37;c=1/np.sqrt(1-v*v);s=v*c
    d,p,q,f=2.,.7,.2,.3
    old=spherical_curvature(.5,d,p,q,f)
    new=spherical_curvature(.5,c*c*d+2*c*s*f+s*s*p,
        s*s*d+2*c*s*f+c*c*p,q,c*s*(d+p)+(c*c+s*s)*f)
    checks["radial_boost"]=max(abs(new[k]-old[k]) for k in old)<1e-12
    A=.3;P=1.2+.7j;D=.3-.4j;V=.2
    X=A*abs(P)**2;Y=A*abs(D)**2
    direct=spherical_curvature(.4,(X+Y)/2+V,(X+Y)/2-V,(X-Y)/2-V,A*np.real(np.conjugate(P)*D))
    stable=scalar_curvature(.4,A,P,D,V)
    checks["scalar_positive_form"]=max(abs(direct[k]-stable[k]) for k in direct)<1e-12
    from copy import deepcopy
    cases,refs=regular_validation_controls(return_fixture=True)
    for case in cases.values():
        for row in case["samples"]:
            row.update(regular_centre_constraint=row["hamiltonian_residual"],
                regular_metric_residual=row["metric_evolution_residual"],
                future_trapped_points=0,outgoing_expansion_at_minimum_F=1.,
                ingoing_expansion_at_minimum_F=-1.)
            for key in CURVATURE_KEYS:row[key]=1+.1*row["central_proper_time"]
    for trace in refs.values():
        for row in trace:
            row["reference_accuracy_residual"]=row["local_mass_flux_relative_l2"]
            for key in CURVATURE_KEYS:row[key]=1+.1*row["central_proper_time"]
    checks["curvature_validator_fixture"]=interior_verdict(cases,refs,.2)["passed"]
    bad=deepcopy(cases);bad["fine"]["samples"][2]["central_Kretschmann"]=float("nan")
    checks["nonfinite_curvature_rejected"]=not interior_verdict(bad,refs,.2)["passed"]
    bad=deepcopy(cases)
    for row in bad["fine"]["samples"]:row["central_Kretschmann"]*=2
    checks["unconverged_curvature_rejected"]=not interior_verdict(bad,refs,.2)["passed"]
    bad=deepcopy(refs);bad["0.00625"][1]["central_Kretschmann"]=float("nan")
    checks["nonfinite_reference_curvature_rejected"]=not interior_verdict(cases,bad,.2)["passed"]
    x1,x2,y1,y2=sp.symbols("x1 x2 y1 y2",real=True)
    radial=x1*x1+x2*x2+y1*y1+y2*y2
    dot=x1*y1+x2*y2
    checks["canonical_radial_null_contraction"]=all(sp.expand(
        radial+2*sgn*dot-(x1+sgn*y1)**2-(x2+sgn*y2)**2)==0 for sgn in (-1,1))
    # Null convergence is independent of the potential:
    # T_ab l^a l^b = |l^a partial_a phi|² for each null l.
    return {k:bool(v) for k,v in checks.items()}


def interior_verdict(cases,refs,end):
    keys=CURVATURE_KEYS
    try:
        for case in cases.values():
            data=[[s[k] for k in keys] for s in case["samples"] if s["t"]<=end+1e-7]
            if not data or not np.all(np.isfinite(data)):
                return dict(end=end,passed=False,gates={"curvature_finite":False})
    except (KeyError,TypeError,ValueError):
        return dict(end=end,passed=False,gates={"curvature_structure":False})
    result=clock_verdict(cases,refs,end)
    if not result.get("budgets"):return result
    rows={n:[s for s in c["samples"] if s["t"]<=end+1e-7] for n,c in cases.items()}
    def errors(a,b):
        out={}
        for key in keys:
            x=np.array([s[key] for s in rows[a]]);y=np.array([s[key] for s in rows[b]])
            out[key]=float(np.linalg.norm(x-y)/max(np.linalg.norm(y),1e-14))
        return out
    em,ef,et,ed=errors("coarse","middle"),errors("middle","fine"),errors("fine","half_step"),errors("middle","domain")
    ratios={k:ef[k]/max(em[k],1e-14) for k in keys}
    result["gates"].update(curvature_finite=True,
        curvature_refinement=all(ef[k]<.005 or ratios[k]<.6 for k in keys),
        curvature_step=max(et.values())<.005,curvature_domain=max(ed.values())<.005)
    result["curvature_convergence"]=dict(middle_fine=ef,ratios=ratios,half_step=et,domain=ed)
    from scipy.interpolate import PchipInterpolator
    central_keys=keys[:3];cross={}
    try:
        upper=min(rows["middle"][-1]["central_proper_time"],rows["fine"][-1]["central_proper_time"],
                  refs["0.0125"][-1]["central_proper_time"],refs["0.00625"][-1]["central_proper_time"])
        tau=np.linspace(0,upper,161)
        for name,h in (("middle","0.0125"),("fine","0.00625")):
            cross[name]={}
            for key in central_keys:
                def mapped(trace):
                    values=np.array([s[key] for s in trace])
                    if not np.all(np.isfinite(values)):raise ValueError("Nonfinite reference curvature")
                    return PchipInterpolator([s["central_proper_time"] for s in trace],values)(tau)
                x,y=mapped(rows[name]),mapped(refs[h])
                cross[name][key]=float(np.linalg.norm(x-y)/max(np.linalg.norm(y),1e-14))
        result["gates"]["curvature_cross_gauge"]=all(cross["fine"][k]<.005 and (
            cross["fine"][k]<1e-6 or cross["fine"][k]/max(cross["middle"][k],1e-14)<.6) for k in central_keys)
        result["curvature_cross_gauge"]=dict(proper_time_end=upper,errors=cross)
    except (KeyError,TypeError,ValueError):
        result["gates"]["curvature_cross_gauge"]=False
    result["passed"]=all(result["gates"].values())
    result["interior_prefix_validated"]=result["passed"]
    result["proper_time_extended"] &= result["passed"]
    result["curvature_extended"]=bool(result["passed"] and result["last"]["central_proper_time"]>INTERIOR_TARGET_PROPER_TIME)
    result["future_trapped_region_resolved"] &= result["passed"]
    result["singularity_resolution"]=False
    return result


def interior_parallel_job(spec):
    name,h,radius,courant,kappa=spec
    module,mod64,sol,_,_,_=aggregate_collapse_background()
    if name.startswith("reference_"):
        reference=regular_case(module,mod64,sol,h=h,radius=radius,duration=9.4)
        for row in reference["samples"]:
            row["reference_accuracy_residual"]=max(row[k] for k in (
                "hamiltonian_residual","metric_evolution_residual",
                "origin_hamiltonian_residual","origin_isotropy_residual"))
            # At a smooth spherical centre the gradient/flux and Weyl vanish.
            # Reconstruct reference curvature from independent rho and |phi|.
            s=row["central_amplitude"]**2;V=s/2-s*s/4+SEXTIC*s**3/6
            rho=row["central_density"];p=rho-2*V
            for key,value in spherical_curvature(rho/3,rho,p,p,0.).items():
                row["central_"+key]=float(value)
        return reference
    return clock_case(module,mod64,sol,h=h,radius=radius,courant=courant,kappa=kappa,
                      staggered=True,interior=True)


def run_interior_suite(pilot=False,checks_only=False,pilot_h=.025):
    result=dict(code_sha256=sha(__file__),previous_sha256=INTERIOR_PREVIOUS_SHA256,cases={})
    try:
        module,mod64,sol,bg,pins,base=aggregate_collapse_background()
        result.update(base_sha256=base,dependency_sha256=pins,
            controls=interior_controls(),clock_controls=clock_controls(module,True))
        if not all(result["controls"].values()) or not all(result["clock_controls"]["gates"].values()):
            raise RuntimeError("Interior prerequisite control failed")
        if not checks_only:
            if pilot:
                result["cases"]["pilot"]=clock_case(module,mod64,sol,h=pilot_h,staggered=True,interior=True)
            else:
                from concurrent.futures import ProcessPoolExecutor
                jobs=[("coarse",.05,32.,.1,.1),("middle",.025,32.,.1,.1),
                    ("fine",.0125,32.,.1,.1),("half_step",.0125,32.,.05,.1),
                    ("domain",.025,48.,.1,.1),("zero_middle",.025,32.,.1,0.),
                    ("zero_fine",.0125,32.,.1,0.),("reference_0.0125",.0125,32.,.1,.1),
                    ("reference_0.00625",.00625,32.,.1,.1)]
                refs={}
                with ProcessPoolExecutor(max_workers=3) as pool:
                    for spec,value in zip(jobs,pool.map(interior_parallel_job,jobs)):
                        if spec[0].startswith("reference_"):
                            if value["status"]!="COMPLETED":raise RuntimeError("Fixed-lapse reference failed")
                            refs[spec[0][10:]]=value["samples"]
                        else:result["cases"][spec[0]]=value
                result["fixed_references"]=refs
                last=min(c["samples"][-1]["t"] for c in result["cases"].values())
                tenth=int(np.floor(10*last+1e-6));result["validated_prefix"]=None
                result["last_common_interval"]=interior_verdict(result["cases"],refs,tenth/10)
                for i in range(tenth,0,-1):
                    value=interior_verdict(result["cases"],refs,i/10)
                    if value["passed"]:result["validated_prefix"]=value;break
        result["source_unchanged"]=sha(__file__)==result["code_sha256"]
        result["dependencies_unchanged"]=sha(HERE/"nonlinear_equilibrium_evolution.py")==base and all(sha(module.SF/p)==v for p,v in pins.items())
        if not result["source_unchanged"] or not result["dependencies_unchanged"]:
            raise RuntimeError("Interior source/dependency changed during run")
        result["status"]=("INTERIOR_CONTROLS_PASSED" if checks_only else "INTERIOR_PILOT_RECORDED" if pilot
            else "INTERIOR_CURVATURE_EXTENDED_ENDPOINT_OPEN" if result["validated_prefix"] and result["validated_prefix"]["curvature_extended"]
            else "INTERIOR_EXTENSION_OPEN")
    except Exception as error:
        result.update(status="DIAGNOSTIC_FAILED",error=f"{type(error).__name__}: {error}")
    print(json.dumps(result,indent=2,allow_nan=False))
    return 0 if checks_only and result["status"]=="INTERIOR_CONTROLS_PASSED" else 1
# END INTERIOR CURVATURE DIAGNOSTIC


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--suite", action="store_true")
    parser.add_argument("--initial-response", action="store_true")
    parser.add_argument("--response-suite", action="store_true")
    parser.add_argument("--aggregate-equilibrium-suite", action="store_true")
    parser.add_argument("--aggregate-collapse-suite", action="store_true")
    parser.add_argument("--aggregate-collapse-pilot", action="store_true")
    parser.add_argument("--aggregate-weak-flow-suite", action="store_true")
    parser.add_argument("--aggregate-spatial-repair-suite", action="store_true")
    parser.add_argument("--horizon-regular-pilot", action="store_true")
    parser.add_argument("--horizon-regular-suite", action="store_true")
    parser.add_argument("--horizon-regular-checks", action="store_true")
    parser.add_argument("--clock-suite", action="store_true")
    parser.add_argument("--interior-suite", action="store_true")
    parser.add_argument("--interior-pilot", action="store_true")
    parser.add_argument("--interior-checks", action="store_true")
    parser.add_argument("--interior-pilot-h", type=float, default=.025)
    parser.add_argument("--clock-pilot", action="store_true")
    parser.add_argument("--clock-checks", action="store_true")
    parser.add_argument("--clock-mode", choices=("harmonic","one_plus_log"), default="harmonic")
    parser.add_argument("--clock-staggered", action="store_true")
    parser.add_argument("--clock-pilot-h", type=float, default=.05)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--separation", type=float, default=28.0)
    parser.add_argument("--h", type=float, default=0.5)
    parser.add_argument("--radius", type=float, default=32.0)
    parser.add_argument("--half-height", type=float, default=64.0)
    args = parser.parse_args()
    if args.interior_suite or args.interior_pilot or args.interior_checks:
        return run_interior_suite(args.interior_pilot,args.interior_checks,args.interior_pilot_h)
    if args.clock_suite or args.clock_pilot or args.clock_checks:
        return run_clock_suite(args.clock_mode,args.clock_pilot,args.clock_checks,args.clock_staggered,args.clock_pilot_h)
    if args.horizon_regular_checks:
        checks=dict(algebra=regular_algebra_controls(),validator=regular_validation_controls())
        spec=importlib.util.spec_from_file_location("regular_check_base",HERE/"nonlinear_equilibrium_evolution.py")
        module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
        origin=regular_origin_controls(module)
        checks["origin"]=origin["gates"]
        print(json.dumps({"origin_values":origin["rows"]},indent=2,allow_nan=False))
        print(json.dumps(checks,indent=2,allow_nan=False))
        return 0 if all(all(v.values()) for v in checks.values()) else 1
    if args.horizon_regular_pilot or args.horizon_regular_suite:
        return run_regular_suite(pilot=args.horizon_regular_pilot)
    if args.aggregate_spatial_repair_suite:
        return run_spatial_repair_suite()
    if args.aggregate_weak_flow_suite:
        return run_aggregate_collapse_suite(flow_strength=.01)
    if args.aggregate_collapse_suite or args.aggregate_collapse_pilot:
        return run_aggregate_collapse_suite(pilot=args.aggregate_collapse_pilot)
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
