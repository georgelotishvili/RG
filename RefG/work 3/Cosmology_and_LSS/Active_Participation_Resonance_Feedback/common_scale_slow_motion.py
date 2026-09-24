"""APR_DRESSED_SLOW_MOTION_V1: fixed-charge translation of the retained core.

One coupling, two restored domains, two l=1 finite-element resolutions.
The old stdout-only solver is imported as an unchanged input dependency;
its radial Hessian and old acceptance campaign are never executed here.
See common_scale_finite_source_candidate.md section 4. Results: stdout only.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import scipy
import sympy as sp
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import spsolve

HERE = Path(__file__).resolve().parent
OLD = HERE / "common_scale_finite_source_candidate.py"
OLD_HASH = "6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8"
Q = 190.401136223484
ALPHA = .001
ANCHOR = 176.739457346
DOMAINS = ((40., 1e-7), (60., 3e-8))
CELLS = (600, 1200)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def relative(a, b):
    return abs(a-b) / max(abs(b), 1e-30)


def exact_checks():
    checks = {}
    # Fixed-Q elimination: the O(v^2) frequency correction cancels in L-Q*w.
    w, dw, v, inertia0, di, cross, kinetic, phase = sp.symbols(
        "w dw v I dI B A phase", real=True)
    lag = (inertia0+v**2*di)*(w+v**2*dw)**2/2 - v**2*w*cross
    lag += v**2*(kinetic-phase)/2
    routh = lag - w*inertia0*(w+v**2*dw)
    coefficient = sp.expand(routh).coeff(v, 2)
    checks["fixed_charge_frequency_correction_cancels"] = sp.simplify(
        coefficient - (w**2*di/2-w*cross+(kinetic-phase)/2)) == 0
    # Background profile variations cancel by stationary fixed-Q field EL.
    # Phase EL gives omega*cross=-phase, yielding (kinetic+phase)/2.
    checks["phase_stationarity_reduces_routhian"] = sp.simplify(
        coefficient.subs({di:0, cross:-phase/w})-(kinetic+phase)/2) == 0
    aint, fint, grad, agrad, kc = sp.symbols("A F D Da K", real=True)
    bz = -w*(aint-fint)  # phase EL tested against z
    phase_norm = w**2*fint-2*w*bz+kc
    gap = agrad/3 + phase_norm - (w**2*aint+grad/3)
    checks["exact_inertia_gap_square_completion"] = sp.expand(
        gap-((agrad-grad)/3+w**2*(aint-fint)+kc)) == 0
    e, m, u = sp.symbols("E M u", real=True)
    body = -sp.exp(-u)*e+sp.exp(3*u)*m*v**2/2
    source = sp.diff(body,u).subs(u,0)
    flat = body.subs(u,0)
    momentum = sp.diff(flat,v)
    energy = v*momentum-flat
    checks["background_source_equals_energy_plus_v_momentum"] = sp.simplify(
        source-energy-v*momentum) == 0
    checks["passive_mass_equals_rest_energy"] = source.subs(v,0) == e
    rho,z = sp.symbols("rho z", positive=True)
    green = 1/sp.sqrt(z**2+(1-v**2)*rho**2)
    wave = sp.diff(green,rho,2)+sp.diff(green,rho)/rho+(1-v**2)*sp.diff(green,z,2)
    checks["moving_weak_green_solves_exterior_operator"] = sp.simplify(wave) == 0
    # Flux normalization by y_perp=sqrt(1-v^2)*R_perp, y_z=R_z
    # cancels the anisotropic operator's delta-function Jacobian.
    mu = sp.symbols("mu", real=True)
    expansion = sp.series((e+3*m*v**2/2)/sp.sqrt(1-v**2*(1-mu**2)),v,0,4).removeO()
    checks["moving_exterior_quadratic_coefficient"] = sp.expand(
        expansion-e-v**2*((3*m+e)/2-e*mu**2/2)) == 0
    boost_source = e*(1+v**2)/sp.sqrt(1-v**2)
    checks["zero_self_gravity_stress_boost_source"] = sp.series(
        boost_source,v,0,4).removeO() == e+3*e*v**2/2
    c, alpha, radius = sp.symbols("C alpha R", positive=True)
    tail = sp.pi*c/(3*alpha)*(sp.exp(4*c/radius)-1)
    checks["full_foundation_translation_tail_integral"] = sp.simplify(
        sp.diff(tail,radius)+4*sp.pi*c**2*sp.exp(4*c/radius)/(3*alpha*radius**2)) == 0
    b,p,ut = sp.symbols("b p ut", positive=True)
    rate = b**2/(alpha*p**2)*(1-sp.sqrt(1-ut**2/(b**2*p**2)))
    checks["rate_limiter_retains_quadratic_kinetic_coefficient"] = sp.simplify(
        sp.diff(rate,ut,2).subs(ut,0)-1/(alpha*p**4)) == 0
    # Derive the dipole phase EL from the angularly integrated Routhian.
    rr = sp.symbols("r", positive=True)
    hh, ff, aa = [sp.Function(name)(rr) for name in ("h", "f", "a")]
    hp = sp.diff(hh,rr)
    phase_lag = -ff**2*(rr**2*hp**2+2*hh**2)/2-w*aa*ff**2*(rr**2*hp+2*rr*hh)
    phase_el = sp.diff(phase_lag,hh)-sp.diff(sp.diff(phase_lag,hp),rr)
    expected_el = sp.diff(rr**2*ff**2*hp,rr)-2*ff**2*hh+w*rr**2*sp.diff(aa*ff**2,rr)
    checks["dipole_phase_equation_from_action"] = sp.simplify(phase_el-expected_el)==0
    spherical_charge = sp.series(source*sp.atanh(v)/v,v,0,4).removeO()
    checks["spherical_gauss_charge_differs_from_wave_charge"] = sp.expand(
        spherical_charge-e-v**2*(3*m/2+e/3))==0
    checks["naive_moving_source_energy_omits_v_momentum"] = sp.simplify(source-energy) == m*v**2
    return checks


def phase_response(solution, radius, cells, old):
    """P1 weak solve for k=h+Omega*r; no division by the exponential f tail."""
    step = radius/cells
    gx, gw = np.polynomial.legendre.leggauss(6)
    r = step*(np.arange(cells)[:,None]+(gx+1)/2)
    weights = np.broadcast_to(step*gw/2,r.shape)
    shape = np.array([(1-gx)/2,(1+gx)/2])
    deriv = np.array([-1/step,1/step])
    f,fp,u,up,_ = solution.sol(r.ravel()).reshape(5,cells,-1)
    omega = float(solution.p[0])
    a = np.exp(4*u)
    am1 = np.expm1(4*u)
    rows,cols,data = [],[],[]
    rhs = np.zeros(cells+1)
    for i in range(2):
        local_rhs = np.sum(-omega*weights*am1*f**2*(r**2*deriv[i]+2*r*shape[i]),axis=1)
        np.add.at(rhs,np.arange(cells)+i,local_rhs)
        for j in range(2):
            kij = np.sum(weights*f**2*(r**2*deriv[i]*deriv[j]+2*shape[i]*shape[j]),axis=1)
            rows.extend(np.arange(cells)+i)
            cols.extend(np.arange(cells)+j)
            data.extend(kij)
    matrix = coo_matrix((data,(rows,cols)),shape=(cells+1,cells+1)).tocsr()[1:,1:]
    rhs = rhs[1:]
    # Symmetric diagonal scaling preserves the weak system despite tiny f^2.
    scaling = 1/np.sqrt(matrix.diagonal())
    ds = diags(scaling)
    scaled = (ds@matrix@ds).tocsc()
    y = spsolve(scaled,scaling*rhs)
    k = np.r_[0.,scaling*y]
    residual = np.linalg.norm(matrix@k[1:]-rhs)/np.linalg.norm(rhs)
    kval = k[:-1,None]*shape[0]+k[1:,None]*shape[1]
    kp = (k[1:]-k[:-1])[:,None]/step
    h = kval-omega*r
    hp = kp-omega

    def integral(value):
        return float(np.sum(weights*value))

    factor = 4*np.pi/3
    phase_mass = factor*integral(f**2*(r**2*hp**2+2*h**2))
    phase_momentum = -factor*omega*integral(a*f**2*(r**2*hp+2*r*h))
    C = float(radius*solution.sol(radius)[2])
    tail_mass = np.pi*C/(3*ALPHA)*np.expm1(4*C/radius)
    tail_energy = 2*np.pi*C**2/(ALPHA*radius)
    mass_matter = factor*integral(r**2*a*fp**2)
    mass_foundation = factor*integral(r**2*a*up**2/ALPHA)+tail_mass
    mass = phase_mass+mass_matter+mass_foundation
    energy = 4*np.pi*integral(r**2*(a*omega**2*f**2/2+fp**2/2+np.exp(2*u)*old.potential(f)+up**2/(2*ALPHA)))+tail_energy
    gap_gradient = factor*integral(r**2*am1*(fp**2+up**2/ALPHA))
    gap_gradient += tail_mass-4*np.pi*C**2/(3*ALPHA*radius)
    gap_phase = 4*np.pi*omega**2*integral(r**2*am1*f**2)
    gap_correction = factor*integral(f**2*(r**2*kp**2+2*kval**2))
    decomposition = gap_gradient+gap_phase+gap_correction
    # z is represented exactly in the P1 test space (with z=0 at the centre).
    first_moment = factor*integral(f**2*(r**2*hp+2*r*h))
    first_moment_target = -4*np.pi*omega*integral(r**2*a*f**2)
    return {
        "radius":radius,"phase_cells":cells,"omega":omega,
        "energy_rest":energy,"mass_inertial":mass,"inertia_minus_rest":mass-energy,
        "fractional_inertia_excess":(mass-energy)/energy,"passive_acceleration_ratio":energy/mass,
        "phase_mass":phase_mass,"phase_momentum_mass":phase_momentum,
        "amplitude_translation_mass":mass_matter,"foundation_translation_mass":mass_foundation,
        "exterior_translation_mass":tail_mass,"exterior_rest_energy":tail_energy,
        "gap_gradient":gap_gradient,"gap_phase":gap_phase,"gap_phase_correction":gap_correction,
        "gap_decomposition":decomposition,"gap_identity_absolute_residual":abs(mass-energy-decomposition),
        "linear_relative_residual":float(residual),"phase_momentum_relative":relative(phase_mass,phase_momentum),
        "first_moment_relative":relative(first_moment,first_moment_target),
        "energy_anchor_relative":relative(energy,ANCHOR),
        "min_u":float(np.min(u)),"max_abs_u":float(np.max(abs(u))),"max_f_squared":float(np.max(f**2)),
        "endpoint_f":float(solution.sol(radius)[0]),"C":C,
        "profile_max_rms_residual":float(np.max(solution.rms_residuals)),
        "frozen_phase_weak_residual_norm":float(np.linalg.norm(rhs)),
        "moving_source_v_squared_coefficient":1.5*mass,
        "moving_exterior_isotropic_v_squared_coefficient":(3*mass+energy)/2,
        "moving_exterior_directional_v_squared_coefficient":-energy/2,
    }


def main():
    assert digest(OLD)==OLD_HASH, "Retained action source changed"
    old = import_path("apr_retained_candidate",OLD)
    assert digest(old.W58)==old.W58_SHA256,"Retained seed changed"
    checks = exact_checks()
    print(json.dumps({"claim_id":"APR_DRESSED_SLOW_MOTION_V1","alpha":ALPHA,"charge":Q,
        "source_sha256":digest(Path(__file__)),"retained_source_sha256":digest(OLD),
        "contract_sha256":digest(HERE/"common_scale_finite_source_candidate.md"),
        "seed_sha256":digest(old.W58),"python":platform.python_version(),
        "numpy":np.__version__,"scipy":scipy.__version__,"sympy":sp.__version__,
        "exact_checks":checks},sort_keys=True),flush=True)
    seed_module = import_path("apr_retained_seed",old.W58)
    reference = seed_module.solve_profile(.8,radius=80.,tolerance=1e-8)
    previous = None
    results = []
    for radius,tolerance in DOMAINS:
        solution = old.coupled_profile(reference,Q,ALPHA,radius,tolerance,previous=previous)
        previous = solution
        for cells in CELLS:
            row = phase_response(solution,radius,cells,old)
            results.append(row)
            print(json.dumps(row,sort_keys=True),flush=True)
            label=f"R{radius:g}_N{cells}"
            checks[label+"_linear_residual"] = row["linear_relative_residual"]<1e-9
            checks[label+"_independent_momentum"] = row["phase_momentum_relative"]<1e-9
            checks[label+"_first_moment"] = row["first_moment_relative"]<1e-9
            checks[label+"_restored_energy_anchor"] = row["energy_anchor_relative"]<3e-7
            checks[label+"_positive_source_domain"] = bool(row["min_u"]>0 and row["max_abs_u"]<.03 and row["max_f_squared"]<6 and row["omega"]>.75)
            # This is an exact identity evaluated on an approximate BVP.
            checks[label+"_gap_identity"] = row["gap_identity_absolute_residual"]<3e-7*row["energy_rest"]
            checks[label+"_phase_required"] = row["frozen_phase_weak_residual_norm"]>1e-6
    pairs=((0,1),(2,3),(1,3))
    changes=[]
    for i,j in pairs:
        left,right=results[i],results[j]
        label=f"refinement_{i}_{j}"
        checks[label+"_mass"] = relative(left["mass_inertial"],right["mass_inertial"])<2e-5
        checks[label+"_gap"] = relative(left["inertia_minus_rest"],right["inertia_minus_rest"])<2e-3
        changes.append(abs(left["inertia_minus_rest"]-right["inertia_minus_rest"]))
    best=results[-1]
    checks["positive_gap_resolved"] = best["inertia_minus_rest"]>10*max(changes)
    checks["exterior_tail_is_resolved_contribution"] = best["exterior_translation_mass"]>10*max(changes)
    checks={key:bool(value) for key,value in checks.items()}
    passed=all(checks.values())
    print(json.dumps({"checks":checks,"passed":sum(bool(x) for x in checks.values()),"total":len(checks),
        "acceptance_passed":passed,"largest_gap_refinement_change":max(changes),
        "rest_inertial_passive_mass_equality":False if checks["positive_gap_resolved"] else None,
        "old_static_energy_mass_result_retained":True,"finite_velocity_branch_proved":False,
        "full_ppn_validated":False,"strong_field_completed":False},sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
