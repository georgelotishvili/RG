"""Sourced spherical saturation: exact tests plus bounded numerical crosschecks.

No private article reads, no file writes, no saved PASS inheritance.
See spherical_saturation_matter_bridge.md for postulates and limits.
"""
import argparse
import json
import math
from pathlib import Path
import hashlib
import sys
sys.dont_write_bytecode = True

import mpmath as mp
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp


def run_checks():
    checks = []

    def exact(name, value, target=0):
        residual = s.factor(s.cancel(s.simplify(value-target)))
        checks.append(dict(name=name, kind="exact", passed=residual == 0,
                           residual=str(residual)))

    def gate(name, value, kind="inequality"):
        checks.append(dict(name=name, kind=kind, passed=bool(value)))

    def reject(name, residual):
        simplified = s.factor(s.simplify(residual))
        checks.append(dict(name=name, kind="mutation_rejected",
                           passed=simplified != 0, residual=str(simplified)))

    R, z, ell, M = s.symbols("R z ell M", positive=True)
    X = 1-R**2*z
    h = z/(1-ell**2*z)
    H = 6*h
    H2 = 2*z*(1-3*ell**2*z)/(1-ell**2*z)**2
    H3 = 4/(1-ell**2*z)**2
    H4 = 1-ell**2*z/(1-ell**2*z) + 2*ell**2*z*s.log(
        (1-ell**2*z)/(ell**2*z))
    # Coordinate derivatives (R,X), with z=(1-X)/R^2.
    Dr = lambda ex: s.diff(ex, R)-2*z/R*s.diff(ex, z)
    Dx = lambda ex: -s.diff(ex, z)/R**2
    h2, h3, h4 = R**2*H2, R*H3, R**2*H4
    bracket = h3-2*Dr(h4)
    alpha = s.simplify(h2+X*Dr(bracket))
    beta = s.simplify(X*Dx(bracket)-Dr(h4))
    exact("action_alpha", alpha, R**2*(H-2*z*s.diff(H, z)/3))
    exact("action_beta", beta, -R*s.diff(H, z)/3)
    exact("action_F_zero", Dx(alpha)-Dr(beta))
    exact("Einstein_alpha", s.limit(alpha, ell, 0), 2*R**2*z)
    exact("Einstein_beta", s.limit(beta, ell, 0), -2*R)
    exact("low_curvature_response_normalization", s.diff(h, z).subs(z, 0), 1)
    exact("hprime_positive_expression", s.diff(h, z), 1/(1-ell**2*z)**2)
    exact("H4_zero_curvature_value", s.limit(H4, z, 0, dir="+"), 1)
    gate("H4_derivative_zero_curvature_boundary",
         s.limit(s.diff(H4, z), z, 0, dir="+") == s.oo,
         "action_domain_boundary")

    # Arbitrary local orbit-space frame, not a vacuum-specialized identity.
    ut, ur, htt, htr, hrr = s.symbols("ut ur htt htr hrr", real=True)
    qmetric = s.diag(-1, 1)
    covgrad = s.Matrix([ut, ur])
    congrad = qmetric*covgrad
    Hess = s.Matrix([[htt, htr], [htr, hrr]])
    box = -htt+hrr
    E = beta*Hess-(alpha/2+beta*box)*qmetric
    trE = -E[0, 0]+E[1, 1]
    mu = R**3*H/12
    gradmu = Dr(mu)*covgrad+2*Dx(mu)*Hess*congrad
    current_rhs = (E*congrad-trE*covgrad)/2
    for i in range(2):
        exact("sourced_generalized_mass_balance_"+str(i),
              gradmu[i], current_rhs[i])
    nullvec = s.Matrix([1, 1])
    Enn = (nullvec.T*E*nullvec)[0]
    Rnn = -2*(nullvec.T*Hess*nullvec)[0]/R
    exact("radial_null_source_screening",
          Rnn, (1-ell**2*z)**2*Enn/R**2)

    # Direct orbit-space connection for a general flat FLRW geometry.
    t, chi = s.symbols("tau chi", real=True)
    a = s.Function("a")(t)
    coords = (t, chi)
    metric = s.diag(-1, a**2)
    inverse = metric.inv()
    radius = a*chi
    Gamma = [[[s.simplify(sum(
        inverse[i, d]*(s.diff(metric[d, k], coords[j])
                       +s.diff(metric[d, j], coords[k])
                       -s.diff(metric[j, k], coords[d]))/2
        for d in range(2))) for k in range(2)]
        for j in range(2)] for i in range(2)]
    actual_hess = s.Matrix(2, 2, lambda i, j:
        s.diff(radius, coords[i], coords[j])-sum(
            Gamma[k][i][j]*s.diff(radius, coords[k]) for k in range(2)))
    actual_ricci = s.Matrix(2, 2, lambda i, j: s.simplify(sum(
        s.diff(Gamma[k][i][j], coords[k])
        -s.diff(Gamma[k][i][k], coords[j])
        +sum(Gamma[k][k][l]*Gamma[l][i][j]
             -Gamma[k][j][l]*Gamma[l][i][k] for l in range(2))
        for k in range(2))))
    Hc, Hd, aa = s.symbols("Hc Hd a", real=True, nonzero=True)
    def substitute(ex):
        return s.simplify(ex.subs({
            s.diff(a, t, 2): a*(Hd+Hc**2),
            s.diff(a, t): a*Hc}).subs(chi, R/a).subs(a, aa))
    flrw_hess = actual_hess.applyfunc(substitute)
    boxR = s.simplify(sum(
        s.diag(-1, aa**-2)[i, j]*flrw_hess[i, j]
        for i in range(2) for j in range(2)))
    R2 = substitute(sum(inverse[i, j]*actual_ricci[i, j]
                        for i in range(2) for j in range(2)))
    exact("direct_FLRW_hessian_tt", flrw_hess[0, 0], R*(Hd+Hc**2))
    exact("direct_FLRW_hessian_tx", flrw_hess[0, 1])
    exact("direct_FLRW_box_radius", boxR, -R*(Hd+2*Hc**2))
    exact("direct_FLRW_orbit_curvature", R2, 2*(Hd+Hc**2))
    # Comoving boundary U=(1,0), outward n=(0,1/a):
    # K_tautau=-n.A; Gamma^chi_tautau=0, K_thetatheta=R n.grad R.
    exact("interior_boundary_K_tautau", substitute(Gamma[1][0][0]))
    exact("interior_boundary_K_thetatheta",
          substitute(radius*s.diff(radius, chi)/a), R)
    bb, al = beta.subs(z, Hc**2), alpha.subs(z, Hc**2)
    Ef = bb*flrw_hess-(al/2+bb*boxR)*s.diag(-1, aa**2)
    density_equation = H.subs(z, Hc**2)/2
    pressure_equation = (-H/2-s.diff(H, z)*Hd/3).subs(z, Hc**2)
    exact("full_FLRW_density_equation", Ef[0, 0]/R**2, density_equation)
    exact("full_FLRW_radial_pressure", Ef[1, 1]/(aa**2*R**2),
          pressure_equation)
    exact("full_FLRW_flux_zero", Ef[0, 1])
    hess2 = sum(s.diag(-1, aa**-2)[i, k]*s.diag(-1, aa**-2)[j, l]
                *flrw_hess[i, j]*flrw_hess[k, l]
                for i in range(2) for j in range(2)
                for k in range(2) for l in range(2))
    # Independent radius Euler equation; F=0 was established from the action.
    Er = (-bb*R2+Dr(alpha).subs(z, Hc**2)
          +2*Dr(beta).subs(z, Hc**2)*boxR
          +2*Dx(beta).subs(z, Hc**2)*(boxR**2-hess2))
    exact("independent_FLRW_angular_pressure", -Er/(4*R), pressure_equation)
    rho, P = s.symbols("rho P", real=True)
    zrho = 8*s.pi*rho/(3+8*s.pi*ell**2*rho)
    exact("dust_Friedmann_inverse", h.subs(z, zrho), 8*s.pi*rho/3)
    rhodot = -3*Hc*(rho+P)
    Hdot = -4*s.pi*(rho+P)/(s.diff(h, z).subs(z, Hc**2))
    exact("Friedmann_continuity_identity",
          s.diff(h, z).subs(z, Hc**2)*2*Hc*Hdot,
          8*s.pi*rhodot/3)
    dustHd = -s.Rational(3, 2)*z*(1-ell**2*z)
    exact("dust_acceleration_equation",
          (Hdot.subs(P, 0).subs(rho, 3*h/(8*s.pi))).subs(Hc**2, z),
          dustHd)
    rhoR = 3*M/(4*s.pi*R**3)
    zR = 2*M/(R**3+2*M*ell**2)
    qr = R**3/(R**3+2*M*ell**2)
    exact("boundary_density_response", zrho.subs(rho, rhoR), zR)
    exact("conserved_material_equals_generalized_mass", mu.subs(z, zR), M)
    exact("boundary_dust_current", s.diff(rhoR, R)+3*rhoR/R)
    reject("frozen_geometry_with_added_matter", 3*h-8*s.pi*(3*h/(8*s.pi)+rho))

    # Dust boundary dynamics and two-sided matching.
    speed = -R*s.sqrt(zR)
    f = 1-R**2*zR
    exact("surface_velocity_first_integral", speed**2, 1-f)
    acceleration = s.diff(speed**2, R)/2
    exact("surface_geodesic_acceleration", acceleration, -s.diff(f, R)/2)
    exact("junction_angular_extrinsic_curvature", f+speed**2, 1)
    # EF normalization with vdot =1/(1-Rdot); express f=1-b^2 first.
    b = s.symbols("b", real=True)
    exact("junction_EF_induced_metric",
          -(1-b**2)/(1-b)**2+2*b/(1-b), -1)
    exact("junction_EF_normal_radial_component", (1-b**2)/(1-b)-b, 1)
    # Direct connection for [[-f,1],[1,0]]:
    # Gamma^v_vv=f'/2, Gamma^R_vv=f*f'/2, Gamma^R_vR=-f'/2.
    fp = s.symbols("fprime", real=True)
    vdot = 1/(1-b)
    bdot = -fp/2
    vddot = bdot/(1-b)**2
    exact("junction_EF_geodesic_v", vddot+fp*vdot**2/2)
    exact("junction_EF_geodesic_R",
          bdot+(1-b**2)*fp*vdot**2/2-fp*vdot*b)
    exact("junction_z_continuity", (1-f)/R**2, zR)
    exact("surface_infinite_time_log_coefficient",
          s.limit((-1/speed)*R, R, 0), ell)
    exact("surface_near_zero_rate", s.limit(speed/R, R, 0), -1/ell)
    exact("surface_geometric_mass", R**3*zR/2, M*qr)
    exact("mass_increment_screening", s.diff(R**3*zR/2, M), qr**2)
    exact("surface_ADM_mass", s.limit(R**3*zR/2, R, s.oo), M)
    reject("double_counted_response_source", 3*z-3*h)

    # Interior curvature, evaluated from FLRW geometry.
    Rc = s.factor(6*(dustHd+2*z))
    Kc = s.factor(12*((dustHd+z)**2+z**2))
    exact("interior_Ricci", Rc, 3*z*(1+3*ell**2*z))
    exact("interior_Kretschmann", Kc,
          3*z**2*((3*ell**2*z-1)**2+4))
    exact("interior_Ricci_limit", Rc.subs(z, ell**-2), 12/ell**2)
    exact("interior_Kretschmann_limit", Kc.subs(z, ell**-2), 24/ell**4)
    x = s.symbols("x", real=True)
    Kpoly = s.expand((Kc*ell**4).subs(z, x/ell**2))
    exact("Ricci_bound_monotonicity",
          s.diff((Rc*ell**2).subs(z, x/ell**2), x), 3+18*x)
    # dK/dx=6x(18x^2-9x+5); quadratic has negative discriminant.
    exact("curvature_bound_derivative", s.diff(Kpoly, x),
          6*x*(18*x**2-9*x+5))
    gate("curvature_bound_quadratic_positive", s.discriminant(18*x**2-9*x+5, x)<0)
    gate("material_density_endpoint_unbounded", s.limit(rhoR, R, 0) == s.oo,
         "physical_limit")
    exact("null_response_screened", (1-ell**2*zR)**2, qr**2)
    exact("positive_source_focusing_tends_zero",
          s.limit(rho*(1-ell**2*zrho)**2, rho, s.oo))
    # Finite-dustball null rays must not be identified with an infinite FLRW patch.
    exact("formal_FLRW_affine_integrand_limit",
          s.limit(R/(-speed), R, 0), ell)

    # A true common-p compatibility discriminator, not a new source equation.
    ss, pp, dp, C = s.symbols("s p dp C", positive=True)
    areal_slope = 1/pp-ss*dp/pp**2
    exact("static_common_p_trapping_invariant",
          pp**2*areal_slope**2, (1-ss*dp/pp)**2)
    psol = ss/(ss+C)
    exact("common_p_reciprocal_outer_equation",
          ss*s.diff(psol, ss)-psol*(1-psol))
    exact("common_p_reciprocal_radius", ss/psol, ss+C)
    reject("Hayward_equals_exact_common_p_reciprocal",
           f-(1-M/R)**2)
    exact("candidate_q_centre", s.limit(qr, R, 0), 0)
    exact("candidate_static_lapse_squared_centre", s.limit(f, R, 0), 1)

    # Real alternative: minimal magnetic NLED source and its local health.
    FF, F0, rhostar = s.symbols("F F0 rho_star", positive=True)
    xx = (FF/F0)**s.Rational(3, 4)
    L = rhostar*xx**2/(1+xx)**2
    LF = s.diff(L, FF)
    characteristic = s.simplify((LF+2*FF*s.diff(LF, FF))/LF)
    exact("NLED_source_tangential_pressure",
          2*FF*LF-L, (3/(1+xx)-1)*L)
    exact("NLED_extra_mode_from_action", characteristic,
          (4-5*xx)/(2*(1+xx)))
    gate("NLED_negative_gradient_control",
         characteristic.subs({FF: 1, F0: 1, rhostar: 1}) < 0,
         "rejected_alternative")
    exact("NLED_core_characteristic_limit", s.limit(characteristic, FF, s.oo),
          -s.Rational(5, 2))

    # Numerical checks are independent of the algebraic ODE substitution.
    examples = []
    with mp.workdps(50):
        mass, length = mp.mpf(2), mp.mpf(1)
        A = 2*mass*length**2
        def primitive(rr):
            root = mp.sqrt(rr**3+A)
            return (2*root/(3*mp.sqrt(2*mass))
                    +length/3*mp.log((root-mp.sqrt(A))/(root+mp.sqrt(A))))
        def inverse_speed(rr):
            return mp.sqrt(rr**3+A)/(rr*mp.sqrt(2*mass))
        def lapse2(rr):
            return 1-2*mass*rr**2/(rr**3+A)
        roots = [mp.findroot(lapse2, ab)
                 for ab in [(mp.mpf("1.1"), mp.mpf("1.4")),
                            (mp.mpf("3.5"), mp.mpf("4.1"))]]
        for idx, root in enumerate(roots):
            gate("numeric_horizon_"+str(idx), abs(lapse2(root))<mp.mpf("1e-35"), "numeric")
        for label, rr in [("outer_horizon", roots[1]), ("inner_horizon", roots[0]),
                          ("late_surface", mp.mpf("0.05"))]:
            elapsed = primitive(mp.mpf(8))-primitive(rr)
            quadrature = mp.quad(inverse_speed, [rr, 4, 8])
            gate("surface_quadrature_"+label,
                 abs(elapsed-quadrature)<mp.mpf("1e-35"), "numeric")
            zz = 2*mass/(rr**3+A)
            frac = rr**3/(rr**3+A)
            examples.append(dict(event=label, radius=mp.nstr(rr, 18),
                proper_time=mp.nstr(elapsed, 18),
                geometric_mass=mp.nstr(mass*frac, 18),
                conserved_ADM_mass="2",
                interior_density=mp.nstr(3*mass/(4*mp.pi*rr**3), 12),
                interior_K=mp.nstr(3*zz**2*((3*length**2*zz-1)**2+4), 12)))
        gate("outer_then_inner_crossing", roots[1]>roots[0]>0)
        # Evolve log radius to preserve positivity without clipping.
        def rhs(_time, state):
            rr = math.exp(float(state[0]))
            return [-math.sqrt(4/(rr**3+4))]
        times = np.linspace(0, 12, 49)
        runs = []
        for tol in (1e-8, 1e-11):
            sol = solve_ivp(rhs, (0, 12), [math.log(8)], method="DOP853",
                            t_eval=times, rtol=tol, atol=tol/100)
            gate("ODE_success_"+str(tol), sol.success and len(sol.t)==len(times), "numeric")
            errs = []
            for tt, logR in zip(sol.t, sol.y[0]):
                # Independent monotone bisection of exact elapsed proper time.
                lo, hi = mp.mpf("1e-8"), mp.mpf(8)
                for _ in range(180):
                    mid = (lo+hi)/2
                    elapsed = primitive(mp.mpf(8))-primitive(mid)
                    if elapsed > mp.mpf(float(tt)):
                        lo = mid
                    else:
                        hi = mid
                target = float((lo+hi)/2)
                errs.append(abs(math.exp(float(logR))/target-1))
            runs.append(max(errs))
        gate("ODE_exact_trajectory_error", runs[1]<2e-8, "numeric")
        gate("ODE_tighter_tolerance_convergence",
             runs[1]<runs[0] or max(runs)<5e-13, "numeric")
        numerics = dict(ODE_max_relative_errors=runs,
                        ODE_relative_tolerances=[1e-8, 1e-11],
                        ODE_interval=[0, 12], examples=examples)

    failed = [v for v in checks if not v["passed"]]
    ok = not failed
    return dict(
        decision="CONDITIONAL_SOURCED_CURVATURE_REGULAR_CANDIDATE" if ok else "CHECK_FAILURE",
        checks=len(checks), passed=len(checks)-len(failed), failed=failed,
        scope=dict(spherical_action_verified=ok, sourced_mass_balance_verified=ok,
                   sourced_dust_solution=ok, spherical_no_shell_junction=ok,
                   curvature_bounded=ok, finite_time_horizon_crossings=ok,
                   full_RefG_pressure_join=False, universal_common_p=False,
                   completed_RefG_regular_black_hole=False,
                   global_geodesic_completeness=False, generic_stability=False,
                   oscillon_to_dust_derivation=False, assembly_mass_deficit=False,
                   observational_pass=False),
        versions=dict(python=sys.version.split()[0], sympy=s.__version__,
                      mpmath=mp.__version__),
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        numerics=numerics, details=checks)


def oscillon_checks(return_background=False):
    """Fixed-charge scalar source for the already-postulated spherical action."""
    import importlib.util
    from types import SimpleNamespace
    from scipy.integrate import solve_bvp, simpson, cumulative_trapezoid
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("saturation_scalar_reference",here/"nonlinear_equilibrium_evolution.py")
    ref = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = ref
    spec.loader.exec_module(ref)
    _,model,anchor,anchor_check,pins = ref.background()
    checks = []
    def test(name,condition,**evidence):
        checks.append(dict(name=name,passed=bool(condition),**evidence))
    def exact(name,expression):
        residual = s.factor(s.simplify(expression))
        test(name,residual==0,residual=str(residual))
    test("retained_anchor",anchor_check["pass"])
    r,z,length,coupling,rho,pr,sigma = s.symbols("r z ell alpha rho pr sigma",positive=True)
    q = 1-length**2*z
    B = 1-r*r*z
    Bp = r*z*(1-3*length**2*z)-2*coupling*r*q*q*rho
    lp = coupling*r*q*q*(rho+pr)/B
    beta = -2*r/q**2
    alpha_orbit = 2*r*r*z*(1-3*length**2*z)/q**2
    box = Bp+B*lp
    htt = -sigma**2*B*(Bp/2+B*lp)
    hrr = Bp/(2*B)
    ett = beta*htt+(alpha_orbit/2+beta*box)*sigma**2*B
    err = beta*hrr-(alpha_orbit/2+beta*box)/B
    exact("scalar_saturation_tt_equation",ett/(sigma**2*B)-2*coupling*r*r*rho)
    exact("scalar_saturation_rr_equation",err*B-2*coupling*r*r*pr)
    mass = s.Function("M")(r)
    z_mass = 2*coupling*mass/(r**3+2*coupling*length**2*mass)
    exact("scalar_saturation_metric_derivative",
          s.diff(1-r*r*z_mass,r).subs(s.diff(mass,r),r*r*rho)-Bp.subs(z,z_mass))
    exact("scalar_saturation_Einstein_metric",(1-r*r*z_mass).subs(length,0)-(1-2*coupling*mass/r))
    exact("scalar_saturation_Einstein_lapse",lp.subs(length,0)-coupling*r*(rho+pr)/B)
    u,w = s.symbols("u w",real=True)
    scaled_K = 12*u*u*(1+(3*w*(1-u)-1)**2)
    exact("central_curvature_convex_in_energy_fraction",s.diff(scaled_K,w,2)-216*u*u*(1-u)**2)
    exact("central_curvature_endpoint_zero",scaled_K.subs(w,0)-24*u*u)
    exact("central_curvature_endpoint_one_monotonic",
          s.diff(scaled_K.subs(w,1),u)-24*u*(18*(u-s.Rational(1,2))**2+s.Rational(1,2)))
    exact("central_curvature_endpoint_maximum",scaled_K.subs({w:1,u:1})-24)
    c = s.symbols("chi",real=True)
    exact("retained_potential_nonnegative_form",
          c*c/2-c**4/4+c**6/24-c*c*((c*c-3)**2+3)/24)
    n0,z0,n2 = s.symbols("N0 z0 n2",real=True,nonzero=True)
    lapse = n0*(1+n2*r*r)
    radial_scale = 1/s.sqrt(1-z0*r*r)
    # Independent static orthonormal sectional curvatures at a regular
    # areal centre. Signs drop out of the Kretschmann contraction.
    c01 = (s.diff(lapse,r,2)-s.diff(lapse,r)*s.diff(radial_scale,r)/radial_scale)/(lapse*radial_scale**2)
    c02 = s.diff(lapse,r)/(lapse*r*radial_scale**2)
    c12 = s.diff(radial_scale,r)/(r*radial_scale**3)
    c23 = (1-1/radial_scale**2)/r**2
    centre_K = s.limit(4*(c01**2+2*c02**2+2*c12**2+c23**2),r,0)
    exact("independent_central_curvature",centre_K-12*z0*z0-48*n2*n2)
    alpha = ref.ALPHA
    target_charge = 8.588382857985234

    def fields(x,y,param,ell):
        f,g,M,L = y[:4]
        omega = model.omega_from_parameter(param)
        sigma = np.exp(L)
        z = 2*alpha*M/(x**3+2*alpha*ell**2*M)
        q = 1-ell**2*z
        B = 1-x*x*z
        W = omega**2*f*f/(sigma*sigma*B)
        X = B*g*g
        V = model.potential(f)
        rho,pr,pt = (W+X)/2+V,(W+X)/2-V,(W-X)/2-V
        lp = alpha*x*q*q*(rho+pr)/B
        bp = x*z*(1-3*ell**2*z)-2*alpha*x*q*q*rho
        return omega,sigma,z,q,B,W,rho,pr,pt,lp,bp

    def ode(ell):
        def rhs(x,y,param):
            f,g = y[:2]
            omega,sigma,z,q,B,W,rho,pr,pt,lp,bp = fields(x,y,param,ell)
            gp = (model.potential_force(f)-omega**2*f/(sigma*sigma*B))/B-(2/x+lp+bp/B)*g
            return np.vstack((g,gp,x*x*rho,lp,x*x*omega*f*f/(sigma*B)))
        return rhs

    def boundary(radius):
        def bc(ya,yb,param):
            omega = model.omega_from_parameter(param)
            sig0 = math.exp(float(ya[3]))
            f0 = float(ya[0])
            f2 = (float(model.potential_force(f0))-omega**2*f0/sig0**2)/6
            rho0 = omega**2*f0*f0/(2*sig0**2)+float(model.potential(f0))
            k = math.sqrt(1-omega**2)
            power = -1+alpha*float(yb[2])*(2*omega**2-1)/k
            return np.array([ya[1]-2*f2*model.EPS,
                ya[2]-rho0*model.EPS**3/3,
                ya[4]-omega*f0*f0*model.EPS**3/(3*sig0),
                yb[3],yb[1]+(k-power/radius)*yb[0],yb[4]-target_charge])
        return bc

    # Seed uses the retained reference only; its source and geometry are
    # recomputed by the new BVP. The fifth variable enforces fixed charge.
    seed = anchor
    rows = []
    jobs = [(ell,80.,1e-7) for ell in (0.,0.5,1.,2.)]+[(2.,80.,1e-8),(2.,100.,1e-8)]
    for ell,radius,tol in jobs:
        # The independent angular equation differentiates M/r^3 twice.
        # Resolve the regular centre explicitly; an absolute BVP residual
        # for tiny M alone is insufficient for that curvature check.
        x = np.unique(np.concatenate((np.linspace(model.EPS,2.,1201),
                                      np.linspace(2.,radius,801))))
        # W64 expects four fields; the conserved-charge integral is our
        # fifth field and must not be passed into its four-field adapter.
        four_field_seed = SimpleNamespace(x=seed.x,p=seed.p,
                                           sol=lambda xx: seed.sol(xx)[:4])
        old,p = model.seed_from_solution(x,four_field_seed,alpha)
        omega,sigma,z,q,B,*_ = fields(x,old,p,ell)
        if seed.y.shape[0]==5 and radius<=seed.x[-1]:
            charge_seed = seed.sol(x)[4]
        else:
            density = x*x*omega*old[0]**2/(sigma*B)
            charge_seed = cumulative_trapezoid(density,x,initial=0)+density[0]*x[0]/3
            charge_seed *= target_charge/charge_seed[-1]
        guess = np.vstack((old,charge_seed))
        # Cubic-spline second derivatives converge more slowly than the
        # first-order collocation residual. Oversolve, keeping the original
        # independently registered validation tolerance unchanged.
        solver_tol = tol/100
        solution = solve_bvp(ode(ell),boundary(radius),x,guess,p=p,tol=solver_tol,
                             max_nodes=model.MAX_NODES,verbose=0)
        tag = "ell%s_R%s_tol%s"%(ell,int(radius),tol)
        test(tag+"_solver",solution.success and np.max(solution.rms_residuals)<=2*solver_tol,
             message=solution.message)
        if not solution.success:
            return dict(decision="CONTINUATION_UNRESOLVED",checks=len(checks),
                passed=sum(v["passed"] for v in checks),failed=[v for v in checks if not v["passed"]],
                numerics=rows,details=checks)
        quad = []
        for points in (16001,32001):
            xx = np.linspace(model.EPS,radius,points)
            yy = solution.sol(xx)
            omega,sigma,z,q,B,W,rho,pr,pt,lp,bp = fields(xx,yy,solution.p,ell)
            quad.append((float(simpson(xx*xx*rho,x=xx)),
                         float(simpson(xx*xx*omega*yy[0]**2/(sigma*B),x=xx))))
        M = float(yy[2,-1])
        Q = float(yy[4,-1])
        test(tag+"_domain",np.all(np.isfinite(yy)) and np.min(B)>0 and np.min(sigma)>0
             and np.min(q)>0 and np.min(z)>=0 and np.min(rho)>=0 and 0<omega<1)
        integral_error = max(abs(quad[-1][0]-M)/M,abs(quad[-1][1]-Q)/Q)
        quad_error = max(abs(quad[-1][0]-quad[0][0])/M,abs(quad[-1][1]-quad[0][1])/Q)
        test(tag+"_source_integrals",integral_error<100*tol and quad_error<tol)
        test(tag+"_fixed_charge",abs(Q/target_charge-1)<100*tol)
        # Independent orbit/angular equations use derivatives of the BVP
        # spline, not RHS values substituted into the equations being tested.
        cut = (xx>=0.03)&(xx<=radius-1)
        rr = xx[cut]
        f,g,mm,ll,cc = yy[:,cut]
        yp,ypp = solution.sol(rr,1),solution.sol(rr,2)
        sig = sigma[cut]; zz=z[cut]; qq=q[cut]; bb=B[cut]
        zzp = 2*alpha*qq**2*(yp[2]/rr**3-3*mm/rr**4)
        qqp = -ell**2*zzp
        zzpp = 2*alpha*(2*qq*qqp*(yp[2]/rr**3-3*mm/rr**4)
                        +qq**2*(ypp[2]/rr**3-6*yp[2]/rr**4+12*mm/rr**5))
        bprime = -2*rr*zz-rr**2*zzp
        bsecond = -2*zz-4*rr*zzp-rr**2*zzpp
        lprime,lsecond = yp[3],ypp[3]
        R2 = -bsecond-3*bprime*lprime-2*bb*(lsecond+lprime**2)
        box = bprime+bb*lprime
        hess2 = (bprime/2+bb*lprime)**2+(bprime/2)**2
        beta = -2*rr/qq**2
        dalpha = 4*ell**2*rr*zz**2*(1+3*ell**2*zz)/qq**3
        dbeta = (-2+10*ell**2*zz)/qq**3
        xbeta = 4*ell**2/(rr*qq**3)
        Er = -beta*R2+dalpha+2*dbeta*box+2*xbeta*(box**2-hess2)
        angular_source = -Er/(4*rr)
        angular_res = angular_source-2*alpha*pt[cut]
        angular_error = float(np.max(abs(angular_res))/(2*alpha*np.max(rho)))
        wprime = 2*omega**2*f*yp[0]/(sig**2*bb)-W[cut]*(2*lprime+bprime/bb)
        prprime = wprime/2+bprime*g*g/2+bb*g*yp[1]-model.potential_force(f)*yp[0]
        tov = prprime+(rho[cut]+pr[cut])*(lprime+bprime/(2*bb))+2*(pr[cut]-pt[cut])/rr
        tov_error = float(np.max(abs(tov))/np.max(rho))
        rhs_error = float(np.max(abs(yp-ode(ell)(rr,yy[:,cut],solution.p))/(1+abs(yp))))
        test(tag+"_independent_equations",max(angular_error,tov_error,rhs_error)<100*tol)
        f0,L0 = float(yy[0,0]),float(yy[3,0])
        W0 = omega**2*f0*f0/math.exp(2*L0)
        rho0 = W0/2+float(model.potential(f0))
        z0 = 2*alpha*rho0/(3+2*alpha*ell**2*rho0)
        q0 = 1-ell**2*z0
        n2 = alpha*q0*q0*W0/2-z0/2
        K0 = 12*z0*z0+48*n2*n2
        test(tag+"_regular_centre",math.isfinite(K0) and K0>=0 and (ell==0 or K0*ell**4<=24+1e-10))
        test(tag+"_central_redshift",0<math.exp(L0)<1)
        row = dict(ell=ell,radius=radius,validation_tolerance=tol,solver_tolerance=solver_tol,omega=float(omega),
            central_amplitude=f0,central_lapse=math.exp(L0),central_response_q=q0,
            central_density=rho0,central_K=K0,minimum_radial_metric=float(np.min(B)),
            ADM_mass=M,scalar_charge=Q,source_integral_error=integral_error,
            angular_relative_residual=angular_error,matter_conservation_residual=tov_error,
            spline_ODE_residual=rhs_error,quadrature_error=quad_error,
            collocation_residual=float(np.max(solution.rms_residuals)))
        rows.append(row)
        seed = solution
    test("Einstein_anchor_mass_regression",abs(rows[0]["ADM_mass"]/float(anchor.y[2,-1])-1)<1e-6)
    test("Einstein_anchor_frequency_regression",abs(rows[0]["omega"]-model.omega_from_parameter(anchor.p))<1e-6)
    for field in ("ADM_mass","central_lapse","central_K"):
        test("refinement_"+field,abs(rows[-3][field]/rows[-2][field]-1)<1e-4)
        test("domain_"+field,abs(rows[-2][field]/rows[-1][field]-1)<1e-4)
    test("nontrivial_saturation_on_actual_source",rows[-1]["central_response_q"]<0.99)
    failed = [v for v in checks if not v["passed"]]
    result = dict(decision="CONDITIONAL_STATIONARY_OSCILLON_COUPLED" if not failed else "CHECK_FAILURE",
        checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,numerics=rows,
        source_pins=pins,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scope=dict(new_gravitational_action=False,existing_saturation_postulate=True,
            scalar_source_solved=not failed,fixed_charge=True,horizonless=True,
            full_RefG_pressure_join=False,universal_common_p=False,
            perturbative_stability=False,black_hole_formation=False,singularity_removal=False))
    if return_background:
        if failed:
            raise RuntimeError("Stationary source prerequisite failed")
        return result,ref,model,solution
    return result


def dynamics_checks(pilot=False):
    """Frozen finite-window test; no new action or pressure/readout postulate."""
    import time
    source,ref,model,solution = oscillon_checks(return_background=True)
    alpha,ell = ref.ALPHA,2.0
    checks = []
    def test(name,condition,**evidence):
        checks.append(dict(name=name,passed=bool(condition),**evidence))
    def exact(name,expression):
        residual = s.factor(s.simplify(expression))
        test(name,residual==0,residual=str(residual))
    r,M,a,L,B,sig,S,j = s.symbols("r M a L B sigma S j",positive=True)
    q = r**3/(r**3+2*a*L**2*M)
    bm = 1-2*a*M*q/r
    Mt = r*r*sig*B*B*j
    Bt = -2*a*q*q*Mt/r
    exact("dynamic_metric_mass_derivative",s.diff(bm,M)+2*a*q*q/r)
    exact("action_tr_mass_flux",-r*Bt/(B*q*q)-2*a*r*r*sig*B*j)
    exact("mass_constraint_propagation",r*r*(Bt*S/2+B*B*(a*r*sig*q*q*S)*j))
    # Expand the scalar equations independently before using the metric
    # flux/lapse equations to cancel the remaining constraint defect.
    p0,p1,d0,d1,dd0,dd1,dp0,dp1,F0,F1,bp,sp,bt = s.symbols(
        "p0 p1 d0 d1 dd0 dd1 dp0 dp1 F0 F1 Bprime sigmaprime Btime",real=True)
    c,cp = sig*B,sp*B+sig*bp
    pt0,pt1 = c*(dd0+2*d0/r)+cp*d0-sig*F0,c*(dd1+2*d1/r)+cp*d1-sig*F1
    dt0,dt1 = cp*p0+c*dp0,cp*p1+c*dp1
    kv,jv = p0*p0+p1*p1+d0*d0+d1*d1,p0*d0+p1*d1
    rhot = bt*kv/2+B*(p0*pt0+p1*pt1+d0*dt0+d1*dt1)+c*(F0*p0+F1*p1)
    fluxprime = (2*r*sig*B*B+r*r*sp*B*B+2*r*r*sig*B*bp)*jv+\
                r*r*sig*B*B*(dp0*d0+dp1*d1+p0*dd0+p1*dd1)
    exact("scalar_equations_constraint_defect",r*r*rhot-fluxprime-r*r*(bt*kv/2+B*B*sp*jv))
    # The coefficient in delta M' is q^2, not the q used when freezing
    # the finite nonlinear constraint in the numerical fixed-point solve.
    exact("Hamiltonian_integrating_factor",s.diff(a*r*S*M*q,M)-a*r*S*q*q)
    eps,f,g,p = s.symbols("epsilon f g p",real=True)
    exact("kick_charge_preserved",s.im(f*(s.I*p+eps*r*g))-f*p)
    exact("kick_inward_energy_flux",s.re(s.conjugate(s.I*p+eps*r*g)*g)-eps*r*g*g)
    exact("opposite_kicks_equal_initial_kinetic_energy",
          s.expand_complex(abs(s.I*p+eps*r*g)**2-abs(s.I*p-eps*r*g)**2))

    class SaturationGrid(ref.Grid):
        def __init__(self,radius,h,length=ell):
            super().__init__(radius,h)
            self.ell = length
            self.mass_seed = None
            self.maximum_fixed_point_defect = 0.0
            self.maximum_iterations = 0

        def geometry(self,field,momentum):
            grad = self.gradient(field)
            square = abs(field)**2
            potential = square/2-square**2/4+square**3/24
            kinetic = abs(momentum)**2+abs(grad)**2
            source = self.r**2*(kinetic/2+potential)
            mass = self.primitive(source,2) if self.mass_seed is None else self.mass_seed.copy()
            for iteration in range(40):
                q = self.r**3/(self.r**3+2*alpha*self.ell**2*mass)
                jp = alpha*self.r*kinetic*q
                J = self.primitive(jp,1)
                Jo = J[-1]+jp[-1]*self.h/2
                if not np.all(np.isfinite(J)) or Jo>500:
                    raise FloatingPointError("Unresolved mass integrating factor")
                integrand = np.exp(J)*source
                integral = self.primitive(integrand,2)
                new = np.exp(-J)*integral
                defect = float(np.max(abs(new-mass))/(1+np.max(abs(new))))
                mass = new
                if defect<5e-15:
                    break
            else:
                raise FloatingPointError("Nonlinear mass constraint did not converge")
            self.maximum_fixed_point_defect = max(self.maximum_fixed_point_defect,defect)
            self.maximum_iterations = max(self.maximum_iterations,iteration+1)
            self.mass_seed = mass.copy()
            outer = math.exp(-Jo)*(integral[-1]+integrand[-1]*self.h/2)
            q = self.r**3/(self.r**3+2*alpha*self.ell**2*mass)
            B = 1-2*alpha*mass*q/self.r
            lp = alpha*self.r*q*q*kinetic
            log_lapse = self.primitive(lp,1)
            log_outer = log_lapse[-1]+lp[-1]*self.h/2
            sigma = np.exp(log_lapse-log_outer)
            if (not np.all(np.isfinite(mass)) or np.min(B)<=0 or np.min(q)<=0
                    or np.min(sigma)<=0 or not math.isfinite(outer)):
                raise FloatingPointError("Left positive polar-areal saturation branch")
            return dict(N=B,sigma=sigma,c=B*sigma,mass=mass,mass_outer=outer,
                        sigma0=math.exp(-log_outer),gradient=grad,q=q)

        def local_flux_check(self,state,eta=1e-6):
            rhs = self.rhs(state)
            geom = self.geometry(*state)
            mdot = (self.geometry(*(state+eta*rhs))["mass"]-
                    self.geometry(*(state-eta*rhs))["mass"])/(2*eta)
            coefficient = self.r**2*geom["sigma"]*geom["N"]**2
            target = coefficient*np.real(np.conjugate(state[1])*geom["gradient"])
            scale = coefficient*abs(state[1])*abs(geom["gradient"])
            inside = self.r<=15
            norm = lambda x: math.sqrt(float(np.sum(self.vol[inside]*x[inside]**2)))
            d4 = lambda x: (x[:-4]-8*x[1:-3]+8*x[3:-1]-x[4:])/(12*self.h)
            region = self.r[2:-2]<=15
            square = abs(state[0])**2
            kinetic = abs(state[1])**2+abs(geom["gradient"])**2
            potential = square/2-square**2/4+square**3/24
            ms = (self.r**2*(geom["N"]*kinetic/2+potential))[2:-2]
            ls = (alpha*self.r*geom["q"]**2*kinetic)[2:-2]
            ratio = lambda x,y: float(np.linalg.norm(x[region])/max(np.linalg.norm(y[region]),1e-14))
            qrate = float(np.sum(self.vol*np.imag(np.conjugate(rhs[0])*state[1]+
                                                np.conjugate(state[0])*rhs[1])))
            return dict(local_mass_flux_relative_l2=norm(mdot-target)/max(norm(scale),1e-14),
                mass_radial_constraint_relative_l2=ratio(d4(geom["mass"])-ms,ms),
                lapse_radial_constraint_relative_l2=ratio(d4(np.log(geom["sigma"]))-ls,ls),
                semidiscrete_charge_rate=qrate,directional_step=eta)

    # Independent directional derivative of the nonlinear ADM functional.
    hamiltonian = []
    for h in (0.1,0.05,0.025,0.0125):
        grid = SaturationGrid(30,h)
        field = 1.5*np.exp(-(grid.r/3)**2).astype(complex)
        pi = 0.8j*field
        bump = np.zeros_like(grid.r)
        mask = grid.r<5
        bump[mask] = np.exp(-1/(1-(grid.r[mask]/5)**2))
        df,dp = (0.03+0.02j)*field*bump,(0.025+0.04j)*field*bump
        eta = 1e-5
        direct = (grid.geometry(field+eta*df,pi+eta*dp)["mass_outer"]-
                  grid.geometry(field-eta*df,pi-eta*dp)["mass_outer"])/(2*eta)
        geom = grid.geometry(field,pi)
        square = abs(field)**2
        expected = np.sum(grid.vol*geom["sigma"]*(geom["N"]*np.real(
            np.conjugate(pi)*dp+np.conjugate(geom["gradient"])*grid.gradient(df))+
            (1-square+square**2/4)*np.real(np.conjugate(field)*df)))
        hamiltonian.append(dict(h=h,finite_variation=float(direct),functional_variation=float(expected),
            relative_error=float(abs(direct-expected)/abs(expected))))
    test("Hamiltonian_directional_accuracy",hamiltonian[-1]["relative_error"]<1e-4)
    test("Hamiltonian_directional_refinement",all(b["relative_error"]<0.6*a["relative_error"]
         for a,b in zip(hamiltonian,hamiltonian[1:])))
    gr_grid,zero_grid = ref.Grid(30,0.05),SaturationGrid(30,0.05,length=0)
    fgr = 1.5*np.exp(-(gr_grid.r/3)**2).astype(complex)
    original,new = gr_grid.geometry(fgr,0.8j*fgr),zero_grid.geometry(fgr,0.8j*fgr)
    for key in ("mass","N","sigma","mass_outer"):
        err = float(np.max(abs(np.asarray(original[key])-np.asarray(new[key]))))
        test("Einstein_limit_"+key,err<1e-12,error=err)
    if any(not c["passed"] for c in checks):
        failed = [c for c in checks if not c["passed"]]
        return dict(decision="PREREQUISITE_FAILURE",checks=len(checks),passed=len(checks)-len(failed),
                    failed=failed,details=checks,hamiltonian=hamiltonian)

    omega = model.omega_from_parameter(solution.p)
    observables = ("central_amplitude","charge_rms_areal","charge_rms_proper","central_lapse")
    def compare(left,right):
        differences = {}
        for key in observables:
            x,y = ref.waveform(left,key),ref.waveform(right,key)
            differences[key] = float(np.sqrt(np.mean((x-y)**2))/max(np.sqrt(np.mean(y*y)),1e-14))
        return differences

    def initial(grid,epsilon):
        f,derivative,mass,logsig = solution.sol(grid.r)[:4]
        q = grid.r**3/(grid.r**3+2*alpha*ell**2*mass)
        B = 1-2*alpha*mass*q/grid.r
        return np.array([f.astype(complex),1j*omega*f/(np.exp(logsig)*B)+epsilon*grid.r*derivative])

    def run(h,epsilon,duration=32,radius=40,courant=0.2):
        started = time.perf_counter()
        grid = SaturationGrid(radius,h)
        state = initial(grid,epsilon)
        first = grid.diagnostics(state,0)
        intervals = round(duration/0.5)
        per_sample = math.ceil(0.5/(courant*h))
        dt = 0.5/per_sample
        grid.time_step = dt
        samples = [first]
        local = [dict(t=0,**grid.local_flux_check(state))]
        half = grid.local_flux_check(state,eta=5e-7)
        for n in range(intervals):
            for _ in range(per_sample):
                k1 = grid.rhs(state)
                k2 = grid.rhs(state+dt*k1/2)
                k3 = grid.rhs(state+dt*k2/2)
                k4 = grid.rhs(state+dt*k3)
                state += dt*(k1+2*k2+2*k3+k4)/6
            t = (n+1)*0.5
            samples.append(grid.diagnostics(state,t))
            if (n+1)%16==0 or n==intervals-1:
                local.append(dict(t=t,**grid.local_flux_check(state)))
        summary = dict(maximum_relative_charge_drift=max(abs(row["charge"]/first["charge"]-1) for row in samples),
            maximum_relative_mass_drift=max(abs(row["ADM_mass"]/first["ADM_mass"]-1) for row in samples),
            minimum_B_RHS_stages=grid.stage_min_N,minimum_sigma_RHS_stages=grid.stage_min_sigma,
            maximum_fixed_point_defect=grid.maximum_fixed_point_defect,maximum_iterations=grid.maximum_iterations,
            maximum_characteristic_Courant=dt*grid.stage_max_speed/h,
            directional_step_sensitivity=abs(local[0]["local_mass_flux_relative_l2"]-half["local_mass_flux_relative_l2"]))
        for key in ("local_mass_flux_relative_l2","mass_radial_constraint_relative_l2",
                    "lapse_radial_constraint_relative_l2","semidiscrete_charge_rate"):
            summary["maximum_"+key] = max(abs(row[key]) for row in local)
        label = f"h{h}_eps{epsilon}_R{radius}_C{courant}"
        test(label+"_charge",summary["maximum_relative_charge_drift"]<1e-5)
        test(label+"_mass",summary["maximum_relative_mass_drift"]<5e-3)
        test(label+"_fixed_point",summary["maximum_fixed_point_defect"]<2e-13)
        test(label+"_directional_step",summary["directional_step_sensitivity"]<1e-6)
        print(f"Completed {label}: {time.perf_counter()-started:.1f}s",file=sys.stderr,flush=True)
        return dict(h=h,epsilon=epsilon,duration=duration,radius=radius,dt=dt,courant=courant,
            steps=intervals*per_sample,elapsed_seconds=time.perf_counter()-started,
            summary=summary,samples=samples,local_flux_checks=local)

    # A failure returns unresolved; it is not interpreted as physical collapse.
    cases,controls,responses = [],{},{}
    try:
        for epsilon in (0.0,0.01,-0.01):
            for h in ((0.1,) if pilot else (0.1,0.05,0.025)):
                cases.append(run(h,epsilon,duration=8 if pilot else 32))
        fine = {e:next(c for c in reversed(cases) if c["epsilon"]==e) for e in (0.0,0.01,-0.01)}
        for key in ("ADM_mass","charge","central_lapse"):
            err = abs(fine[0.01]["samples"][0][key]-fine[-0.01]["samples"][0][key])
            test("opposite_kicks_initial_"+key,err<1e-12,error=err)
        test("kick_initial_charge_matches_reference",
             abs(fine[0.01]["samples"][0]["charge"]/fine[0.0]["samples"][0]["charge"]-1)<1e-13)
        if not pilot:
            controls["half_step"] = run(0.025,0.01,courant=0.1)
            controls["larger_domain"] = run(0.025,0.01,radius=50)
            for name,case in controls.items():
                differences = compare(case,fine[0.01])
                test(name+"_waveforms",max(differences.values())<1e-3,differences=differences)
            for epsilon in (0.0,0.01,-0.01):
                coarse,middle,last = [c for c in cases if c["epsilon"]==epsilon]
                first_diff = compare(coarse,middle)
                second_diff = compare(middle,last)
                for key in first_diff:
                    test(f"eps{epsilon}_waveform_"+key,
                         second_diff[key]<1e-4 or second_diff[key]<0.6*first_diff[key],
                         coarse_middle=first_diff[key],middle_fine=second_diff[key])
                for key in ("local_mass_flux_relative_l2","mass_radial_constraint_relative_l2",
                            "lapse_radial_constraint_relative_l2"):
                    cm,cf = middle["summary"]["maximum_"+key],last["summary"]["maximum_"+key]
                    test(f"eps{epsilon}_accuracy_"+key,cf<5e-3 and (cf<1e-6 or cf<0.6*cm),
                         middle=cm,fine=cf)
        for epsilon in (0.01,-0.01):
            case,reference = fine[epsilon],fine[0.0]
            response = {}
            for key in observables:
                wave,base = ref.waveform(case,key),ref.waveform(reference,key)
                difference = (wave-wave[0])/wave[0]-(base-base[0])/base[0]
                reference_drift = float(np.max(abs(base/base[0]-1)))
                resolution_error = None
                if not pilot:
                    middle = next(c for c in cases if c["epsilon"]==epsilon and c["h"]==0.05)
                    middle_zero = next(c for c in cases if c["epsilon"]==0.0 and c["h"]==0.05)
                    midwave = ref.waveform(middle,key)
                    midbase = ref.waveform(middle_zero,key)
                    middle_response = (midwave-midwave[0])/midwave[0]-(midbase-midbase[0])/midbase[0]
                    resolution_error = float(np.max(abs(difference-middle_response)))
                control_errors = {}
                if not pilot and epsilon==0.01:
                    for name,control in controls.items():
                        control_wave = ref.waveform(control,key)
                        control_errors[name] = float(np.max(abs(wave/wave[0]-control_wave/control_wave[0])))
                threshold = None if pilot else 3*max(reference_drift,resolution_error,*control_errors.values())
                minimum_index = int(np.argmin(difference))
                response[key] = dict(minimum=float(np.min(difference)),maximum=float(np.max(difference)),
                    final=float(difference[-1]),time_of_minimum=case["samples"][int(np.argmin(difference))]["t"],
                    time_of_maximum=case["samples"][int(np.argmax(difference))]["t"],
                    reference_drift=reference_drift,resolution_error=resolution_error,
                    control_errors=control_errors,resolved_threshold=threshold,
                    resolved_decrease=bool(threshold is not None and np.min(difference)<-threshold),
                    resolved_increase=bool(threshold is not None and np.max(difference)>threshold))
                if key.startswith("charge_rms"):
                    later = difference[minimum_index+1:]
                    # A return past the initial radius must FOLLOW the minimum
                    # and persist for three stored samples. It is not damping.
                    returned = bool(threshold is not None and np.min(difference)<-threshold and
                        any(np.all(later[k:k+3]>threshold) for k in range(max(0,len(later)-2))))
                    response[key]["resolved_return_past_initial_radius"] = returned
                    response[key]["maximum_after_minimum"] = float(np.max(difference[minimum_index:]))
            responses[str(epsilon)] = response
    except (FloatingPointError,ValueError) as exc:
        test("finite_chart_execution",False,error=str(exc))
    failed = [c for c in checks if not c["passed"]]
    return dict(decision="UNRESOLVED_NUMERICAL_TEST" if failed else (
                "PILOT_ONLY" if pilot else "BOUNDED_DYNAMICAL_RESPONSE_COMPUTED"),
        checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,
        stationary_prerequisite=dict(checks=source["checks"],passed=source["passed"],source_pins=source["source_pins"]),
        hamiltonian=hamiltonian,cases=cases,controls=controls,responses=responses,
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        reused_evolution_sha256=hashlib.sha256(Path(ref.__file__).read_bytes()).hexdigest(),
        scope=dict(existing_saturation_postulate=True,new_postulate=False,
            finite_time_only=True,ell=ell,alpha=alpha,full_RefG_pressure_join=False,
            generic_stability=False,damping_proved=False,black_hole_formation=False,singularity_removal=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--oscillon-source", action="store_true")
    parser.add_argument("--oscillon-dynamics", action="store_true")
    parser.add_argument("--dynamics-pilot", action="store_true")
    args = parser.parse_args()
    if args.oscillon_source and (args.oscillon_dynamics or args.dynamics_pilot):
        parser.error("Choose stationary or dynamical checks")
    result = (dynamics_checks(pilot=args.dynamics_pilot) if args.oscillon_dynamics or args.dynamics_pilot
              else oscillon_checks() if args.oscillon_source else run_checks())
    if not args.verbose:
        result.pop("details")
    print(json.dumps(result, indent=2, allow_nan=False))
    return int(bool(result["failed"]))


if __name__ == "__main__":
    raise SystemExit(main())
