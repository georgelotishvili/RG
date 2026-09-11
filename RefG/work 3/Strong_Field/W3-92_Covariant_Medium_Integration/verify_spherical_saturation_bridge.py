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


def dynamics_checks(pilot=False, return_grid=False):
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

        def local_flux_check(self,state,eta=1e-6,diagnostic_radius=15.0):
            rhs = self.rhs(state)
            geom = self.geometry(*state)
            mdot = (self.geometry(*(state+eta*rhs))["mass"]-
                    self.geometry(*(state-eta*rhs))["mass"])/(2*eta)
            coefficient = self.r**2*geom["sigma"]*geom["N"]**2
            target = coefficient*np.real(np.conjugate(state[1])*geom["gradient"])
            scale = coefficient*abs(state[1])*abs(geom["gradient"])
            inside = self.r<=diagnostic_radius
            norm = lambda x: math.sqrt(float(np.sum(self.vol[inside]*x[inside]**2)))
            d4 = lambda x: (x[:-4]-8*x[1:-3]+8*x[3:-1]-x[4:])/(12*self.h)
            region = self.r[2:-2]<=diagnostic_radius
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

    if return_grid:
        if any(not c["passed"] for c in checks):
            raise RuntimeError("Dynamic equation prerequisite failed")
        return SaturationGrid,ref,dict(stationary_checks=source["checks"],
            stationary_passed=source["passed"],source_pins=source["source_pins"],
            exact_dynamic_checks=len(checks))

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


def supercritical_data_checks(return_data=False):
    """One supercritical, initially untrapped charged packet; stdout only."""
    from scipy.integrate import solve_ivp,simpson
    from scipy.optimize import brentq
    Grid,ref,prerequisite = dynamics_checks(return_grid=True)
    alpha,ell = ref.ALPHA,2.0
    rin,rout,centre,width = 20.0,40.0,30.0,10.0
    wave_number,omega,velocity = 1.0,math.sqrt(2),1/math.sqrt(2)
    critical = 3*math.sqrt(3)*ell/(4*alpha)
    target,cap = 2*critical,2.2*critical
    lower_B = 1-2*alpha*target/rin
    checks = []
    def test(name,condition,**evidence):
        checks.append(dict(name=name,passed=bool(condition),**evidence))
    def exact(name,expression):
        residual = s.factor(s.simplify(expression))
        test(name,residual==0,residual=str(residual))
    rr,aa,ll,MM = s.symbols("r alpha ell M",positive=True)
    qq = rr**3/(rr**3+2*aa*ll**2*MM)
    BB = 1-2*aa*MM*qq/rr
    critical_symbol = 3*s.sqrt(3)*ll/(4*aa)
    polynomial = rr**3-2*aa*MM*rr**2+2*aa*ll**2*MM
    exact("horizon_critical_double_root",polynomial.subs({MM:critical_symbol,rr:s.sqrt(3)*ll}))
    exact("horizon_critical_stationary_root",s.diff(polynomial,rr).subs({MM:critical_symbol,rr:s.sqrt(3)*ll}))
    f,amp,b,db,k,w,v = s.symbols("f a b db k omega v",real=True)
    field,derivative,momentum = amp*b,amp*(db+s.I*k*b),amp*(v*db+s.I*w*b)
    exact("packet_positive_charge",s.im(s.conjugate(field)*momentum)-w*amp**2*b*b)
    exact("packet_inward_charge_current",s.im(s.conjugate(field)*derivative)-k*amp**2*b*b)
    exact("packet_inward_energy_current",s.re(s.conjugate(momentum)*derivative)-amp**2*(v*db**2+w*k*b*b))
    potential = f*f/2-f**4/4+f**6/24
    exact("nonnegative_amplitude_source_force",s.diff(potential,f)-f*(1-f*f/2)**2)
    exact("amplitude_variation_mass_coefficient",s.diff(BB,MM)+2*aa*qq*qq/rr)
    test("analytic_initial_untrapped_bound",lower_B>0,bound=lower_B)
    test("positive_shooting_trial_bound",1-2*alpha*cap/rin>0,bound=1-2*alpha*cap/rin)

    def profile(radius):
        x = (np.asarray(radius)-centre)/width
        inside = abs(x)<1
        safe = np.where(inside,1-x*x,1.0)
        b = np.where(inside,np.exp(1-1/safe),0.0)
        db = -2*x*b/(width*safe*safe)
        return b,db

    def coefficients(radius,amplitude):
        b,db = profile(radius)
        f = amplitude*b
        unit_kinetic = (1+velocity**2)*db**2+(wave_number**2+omega**2)*b*b
        kinetic = amplitude**2*unit_kinetic
        V = f*f/2-f**4/4+f**6/24
        return b,unit_kinetic,kinetic,V

    def radial_solution(amplitude,tolerance=1e-12,max_step=0.05,stop_at_cap=False):
        def rhs(radius,y):
            M,L,Q,dM = y
            b,unit_kinetic,kinetic,V = coefficients(radius,amplitude)
            q = radius**3/(radius**3+2*alpha*ell*ell*M)
            B = 1-2*alpha*M*q/radius
            if B<=0 or not np.all(np.isfinite(y)):
                raise FloatingPointError("Shooting left the registered untrapped branch")
            Vf = amplitude*b*(1-(amplitude*b)**2/2)**2
            return [radius**2*(B*kinetic/2+V),alpha*radius*q*q*kinetic,
                    radius**2*omega*amplitude**2*b*b,
                    -alpha*radius*q*q*kinetic*dM+radius**2*(B*amplitude*unit_kinetic+Vf*b)]
        def cutoff(radius,y):
            return y[0]-cap
        cutoff.terminal,cutoff.direction = True,1
        sol = solve_ivp(rhs,(rin,rout),[0.,0.,0.,0.],method="DOP853",rtol=tolerance,
                        atol=tolerance*0.01,max_step=max_step,dense_output=True,
                        events=cutoff if stop_at_cap else None)
        if not sol.success:
            raise RuntimeError(sol.message)
        return sol

    attempts = []
    def mass_residual(amplitude):
        if amplitude==0:
            return -target
        trial = radial_solution(amplitude,stop_at_cap=True)
        mass = float(trial.y[0,-1])
        attempts.append(dict(amplitude=float(amplitude),mass=mass,last_radius=float(trial.t[-1])))
        return mass-target
    upper = 0.05
    for _ in range(8):
        if mass_residual(upper)>0:
            break
        upper *= 2
    else:
        raise RuntimeError("Registered amplitude bracket exhausted")
    amplitude = brentq(mass_residual,0,upper,xtol=1e-13,rtol=1e-13)
    solution = radial_solution(amplitude)
    loose = radial_solution(amplitude,tolerance=1e-10,max_step=0.1)
    mass,log_total,charge,mass_derivative = (float(z) for z in solution.y[:,-1])
    test("source_mass_target",abs(mass/target-1)<1e-9,error=abs(mass/target-1))
    test("positive_charge_and_amplitude_derivative",charge>0 and mass_derivative>0,
         charge=charge,dM_da=mass_derivative)
    for index,name in ((0,"mass"),(1,"log_lapse"),(2,"charge")):
        error = abs(loose.y[index,-1]-solution.y[index,-1])/max(abs(solution.y[index,-1]),1e-14)
        test("ODE_tolerance_"+name,error<1e-8,error=float(error))

    def continuum(radius):
        clipped = np.clip(radius,rin,rout)
        y = solution.sol(clipped)
        M,L = y[0],y[1]
        q = radius**3/(radius**3+2*alpha*ell*ell*M)
        B = 1-2*alpha*M*q/radius
        return dict(M=M,q=q,B=B,sigma=np.exp(L-log_total))

    x = np.linspace(rin,rout,16001)
    geom = continuum(x)
    b,unit_S,S,V = coefficients(x,amplitude)
    source_mass = float(simpson(x*x*(geom["B"]*S/2+V),x=x))
    source_charge = float(simpson(x*x*omega*amplitude**2*b*b,x=x))
    source_log = float(simpson(alpha*x*geom["q"]**2*S,x=x))
    for name,value,reference in (("mass",source_mass,mass),("charge",source_charge,charge),("log_lapse",source_log,log_total)):
        err = abs(value/reference-1)
        test("independent_source_integral_"+name,err<1e-8,error=err)
    sensitivity_step = amplitude*1e-4
    numerical_derivative = (radial_solution(amplitude+sensitivity_step).y[0,-1]-
                            radial_solution(amplitude-sensitivity_step).y[0,-1])/(2*sensitivity_step)
    test("amplitude_sensitivity_crosscheck",abs(numerical_derivative/mass_derivative-1)<1e-7,
         relative_error=float(abs(numerical_derivative/mass_derivative-1)))

    def initial(grid,outward=False):
        b,db = profile(grid.r)
        phase = np.exp(1j*wave_number*grid.r)
        state = np.array([amplitude*b*phase,amplitude*phase*(velocity*db+1j*omega*b)])
        if outward:
            state = np.array([np.conjugate(state[0]),-np.conjugate(state[1])])
        return state

    rows = []
    for h in (0.1,0.05,0.025):
        grid = Grid(60,h)
        state = initial(grid)
        geometry = grid.geometry(*state)
        reference = continuum(grid.r)
        Q = float(np.sum(grid.vol*np.imag(np.conjugate(state[0])*state[1])))
        current_E = np.real(np.conjugate(state[1])*geometry["gradient"])
        current_Q = np.imag(np.conjugate(state[0])*geometry["gradient"])
        Mdot = grid.r**2*geometry["sigma"]*geometry["N"]**2*current_E
        Qflux = -grid.r**2*geometry["c"]*current_Q
        errors = dict(mass_profile=float(np.max(abs(geometry["mass"]-reference["M"]))/target),
            radial_metric=float(np.max(abs(geometry["N"]/reference["B"]-1))),
            lapse=float(np.max(abs(geometry["sigma"]/reference["sigma"]-1))),
            charge=abs(Q/charge-1))
        local = grid.local_flux_check(state,diagnostic_radius=50)
        half = grid.local_flux_check(state,eta=5e-7,diagnostic_radius=50)
        normalized_step_difference = abs(local["local_mass_flux_relative_l2"]-half["local_mass_flux_relative_l2"])
        rho = geometry["N"]*(abs(state[1])**2+abs(geometry["gradient"])**2)/2+\
              abs(state[0])**2/2-abs(state[0])**4/4+abs(state[0])**6/24
        test(f"h{h}_positive_source_geometry",np.min(rho)>=0 and np.min(geometry["N"])>=lower_B-1e-4
             and np.min(geometry["sigma"])>0 and np.min(geometry["q"])>0)
        test(f"h{h}_inward_energy_and_charge",np.min(Mdot)>=-1e-12 and np.max(Mdot)>0
             and np.max(Qflux)<=1e-12 and np.min(Qflux)<0)
        # A centred stencil samples across the compact support boundary.
        # Exact flatness applies to the resolved cavity away from that
        # one-cell edge; separately retain and bound its tiny leakage.
        cavity = grid.r<rin-2*h
        edge_leakage = float(np.max(abs(geometry["mass"][grid.r<rin]))/target)
        test(f"h{h}_regular_empty_centre",np.max(abs(geometry["mass"][cavity]))==0
             and np.max(abs(geometry["N"][cavity]-1))==0 and edge_leakage<1e-12,
             source_edge_fractional_mass=edge_leakage,cavity_radius=rin-2*h)
        test(f"h{h}_fixed_point",grid.maximum_fixed_point_defect<2e-13)
        test(f"h{h}_directional_step",normalized_step_difference<1e-6,error=normalized_step_difference)
        reversed_geometry = grid.geometry(*initial(grid,outward=True))
        reversed_Q = float(np.sum(grid.vol*np.imag(np.conjugate(initial(grid,True)[0])*initial(grid,True)[1])))
        test(f"h{h}_opposite_flux_equal_geometry_charge",
             max(np.max(abs(reversed_geometry[key]-geometry[key])) for key in ("mass","N","sigma"))<1e-10
             and abs(reversed_Q-Q)<1e-10)
        opposite = initial(grid,True)
        test(f"h{h}_opposite_flux_sign",
             np.max(abs(np.real(np.conjugate(opposite[1])*reversed_geometry["gradient"])+current_E))<1e-12
             and np.max(abs(np.imag(np.conjugate(opposite[0])*reversed_geometry["gradient"])+current_Q))<1e-12)
        row = dict(h=h,mass=float(geometry["mass_outer"]),charge=Q,
            minimum_B=float(np.min(geometry["N"])),central_lapse=float(geometry["sigma0"]),
            maximum_density=float(np.max(rho)),minimum_q=float(np.min(geometry["q"])),
            maximum_inward_mass_rate=float(np.max(Mdot)),most_negative_outward_charge_flux=float(np.min(Qflux)),
            charge_rms_areal=float(np.sqrt(np.sum(grid.vol*np.imag(np.conjugate(state[0])*state[1])*grid.r**2)/Q)),
            errors=errors,local=local,fixed_point_defect=grid.maximum_fixed_point_defect)
        rows.append(row)
    for key in rows[-1]["errors"]:
        values = [row["errors"][key] for row in rows]
        test("grid_ODE_"+key,values[-1]<3e-4 and all(b<1e-7 or b<0.6*a for a,b in zip(values,values[1:])),errors=values)
    for key in ("local_mass_flux_relative_l2","mass_radial_constraint_relative_l2","lapse_radial_constraint_relative_l2"):
        values = [row["local"][key] for row in rows]
        test("local_refinement_"+key,values[-1]<2e-3 and all(b<1e-7 or b<0.6*a for a,b in zip(values,values[1:])),errors=values)
    domain_grid = Grid(80,0.025)
    domain = domain_grid.geometry(*initial(domain_grid))
    for key in ("N","sigma","mass"):
        error = float(np.max(abs(domain[key][:len(grid.r)]-geometry[key]))/max(1,np.max(abs(geometry[key]))))
        test("domain_"+key,error<1e-10,error=error)
    zero_grid = Grid(60,0.1)
    zeros = np.zeros(len(zero_grid.r),dtype=complex)
    zero = zero_grid.geometry(zeros,zeros)
    test("zero_field_flat_limit",np.all(zero["mass"]==0) and np.all(zero["N"]==1) and np.all(zero["sigma"]==1))
    def positive_vacuum_roots(M):
        roots = np.roots([1,-2*alpha*M,0,2*alpha*ell*ell*M])
        return sorted(float(z.real) for z in roots if abs(z.imag)<1e-8 and z.real>0)
    roots = positive_vacuum_roots(target)
    test("subcritical_vacuum_control",len(positive_vacuum_roots(critical/2))==0)
    test("supercritical_vacuum_control",len(roots)==2 and max(roots)<rin)
    test("potential_roots_are_not_initial_horizons",all(float(continuum(np.array([r]))["B"][0])==1 for r in roots))
    failed = [c for c in checks if not c["passed"]]
    result = dict(decision="SUPERCRITICAL_INWARD_DATA_READY" if not failed else "INITIAL_DATA_CHECK_FAILURE",
        checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,
        parameters=dict(alpha=alpha,ell=ell,rin=rin,rout=rout,amplitude=amplitude,k=wave_number,
                        omega=omega,v=velocity,critical_mass=critical,target_mass=target,analytic_B_bound=lower_B),
        continuum=dict(mass=mass,charge=charge,central_lapse=math.exp(-log_total),dM_da=mass_derivative,
                       potential_vacuum_horizon_radii=roots),
        shooting_trials=attempts,grids=rows,prerequisite=prerequisite,
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        engine_sha256=hashlib.sha256(Path(ref.__file__).read_bytes()).hexdigest(),
        scope=dict(initial_data_ready=not failed,same_saturation_action=True,non_equilibrium_charged_packet=True,
            equilibrium_oscillon_rescaled=False,black_hole_formation=False,singularity_removal=False,
            full_RefG_pressure_join=False,phase_charge_is_particle_count=False,time_evolution_performed=False))
    if return_data:
        if failed:
            raise RuntimeError("Supercritical source prerequisite failed")
        return result,Grid,ref,initial
    return result


def origin_quartic_budget(snapshot,h):
    """Leading flat-principal truncation estimate; not a full error bound."""
    r = np.asarray(snapshot["r"][:3])
    field = np.asarray(snapshot["phi_real"][:3])+1j*np.asarray(snapshot["phi_imag"][:3])
    P = np.asarray(snapshot["P_real"][:3])+1j*np.asarray(snapshot["P_imag"][:3])
    slopes = np.diff(field)/np.diff(r*r)
    f4 = (slopes[1]-slopes[0])/(r[2]**2-r[0]**2)
    P0 = (150*P[0]-25*P[1]+3*P[2])/128
    coefficient = snapshot["central"]["three_point"]["L"]*h*h*float(np.real(np.conjugate(P0)*f4))
    return dict(phi4_real=float(f4.real),phi4_imag=float(f4.imag),
        predicted_central_mudot_defect=4*coefficient,
        measured_central_mudot_defect=snapshot["central"]["three_point"]["mudot_defect"],
        predicted_first_cell_constraint_rate=2*coefficient,
        measured_first_cell_constraint_rate=snapshot["constraint_rate"][0])


class RadialNodalPair:
    """Fourth-order parity pair; Q_h=sum(h*r**2*Im(conj(psi)*P))."""
    def __init__(self,r,h):
        from scipy.sparse import coo_matrix
        self.r,self.h = r,h
        n = len(r)
        def reflected(rows,offsets,weights,parity):
            ii,jj,vv = [],[],[]
            for offset,weight in zip(offsets,weights):
                row = np.arange(rows)
                col = row+offset
                sign = np.ones(rows)
                low,high = col<0,col>=n
                col[low],col[high] = -col[low]-1,2*n-col[high]-1
                sign[low|high] = parity
                ii.extend(row); jj.extend(col); vv.extend(weight*sign)
            return coo_matrix((vv,(ii,jj)),shape=(rows,n)).tocsr()
        self.E = reflected(n,(-2,-1,1,2),np.array([1.,-8.,8.,-1.])/(12*h),1)
        # Sixth-order staggered derivative is needed before division by r^2:
        # fourth-order alone leaves a quartic centre defect.
        self.G = reflected(n+1,(-3,-2,-1,0,1,2),
                          np.array([-9.,125.,-2250.,2250.,-125.,9.])/(1920*h),1)
        self.I = reflected(n+1,(-2,-1,0,1),np.array([-1.,9.,9.,-1.])/16,1)
        self.ET,self.GT = self.E.T.tocsr(),self.G.T.tocsr()
        self.face_weights = np.ones(n+1)
        self.face_weights[[0,-1]] = .5
        self.face_measure = self.face_weights*(np.arange(n+1)*h)**2
        self.weights = h*r*r
        absG = abs(self.G)
        row_bound = (absG.T@(self.face_measure*(absG@(1/r))))/r
        self.wave_frequency_bound = math.sqrt(float(max(row_bound)))
        self.maximum_wave_RK_number = 0.

    def wave(self,field,c):
        cf = self.I@c
        if not np.all(np.isfinite(cf)) or np.min(cf)<=0:
            raise FloatingPointError("Nonpositive paired face wave coefficient")
        return -(self.GT@(self.face_measure*cf*(self.G@field)))/self.r**2

    def transport(self,field,P,beta):
        first = beta*(self.E@field)
        second = -(self.ET@(self.weights*beta*P))/self.weights
        return first,second


def collapse_checks(pilot_only=False,origin_audit=False,origin_finer=False,origin_controls=False,paired_origin=False):
    """Same-action horizon-regular evolution; frozen finite-window decision."""
    import time
    hash_paths = tuple(Path(__file__).with_name(name) for name in
        (Path(__file__).name,"population_assembly_initial_data.py","nonlinear_equilibrium_evolution.py"))
    entry_hashes = {path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in hash_paths}
    source,PolarGrid,ref,initial = supercritical_data_checks(return_data=True)
    legacy = ref.load("saturation_staggered_reference",Path(__file__).with_name("population_assembly_initial_data.py"))
    alpha,ell = ref.ALPHA,2.0
    def relative_array_error(a,b):
        a,b = np.asarray(a),np.asarray(b)
        return float(np.max(abs(a-b))/max(np.max(abs(a)),1e-30))
    checks = []
    def test(name,condition,**evidence):
        checks.append(dict(name=name,passed=bool(condition),**evidence))
    def exact(name,expression):
        residual = s.factor(s.simplify(expression))
        test(name,residual==0,residual=str(residual))
    r,M,k,kr,L,Lr,rho,p,S,a,le = s.symbols("r M k kr L Lr rho p S alpha ell",real=True)
    q = r**3/(r**3+2*a*le**2*M)
    z = 2*a*M*q/r**3
    v = r*k
    A = 1-r*r*z+v*v
    Mr = r*r*(rho+v*S)
    Mt = L*r*r*(v*(rho+p)+(A+v*v)*S)
    kt = L*v*kr+L*(k*k+z*(1-3*le**2*z)/2+a*q*q*p)-A*Lr/r
    Ar = s.diff(A,r)+s.diff(A,M)*Mr+s.diff(A,k)*kr
    At = s.diff(A,M)*Mt+s.diff(A,k)*kt
    exact("regular_metric_action_identity",At-L*v*Ar+2*v*A*Lr+2*a*q*q*L*r*A*S)
    exact("regular_Einstein_k_limit",kt.subs(le,0)-(L*v*kr+L*(k*k+a*M/r**3+a*p)-A.subs(le,0)*Lr/r))
    exact("null_expansion_product",(2*(s.sqrt(A)-v)/r)*(-2*(s.sqrt(A)+v)/r)+4*(1-r*r*z)/r**2)
    # Action projections in an orthonormal orbit frame, beta=-2r/q^2.
    C = z*(1-3*le**2*z)/2
    J,pt = s.symbols("J pt",real=True)
    Hnn,Hee,Hne = -r*(C+a*q*q*p),r*(C-a*q*q*rho),-r*a*q*q*J
    beta,aa = -2*r/q**2,2*r*r*z*(1-3*le**2*z)/q**2
    box = -Hnn+Hee
    for name,expr in (("nn",beta*Hnn+aa/2+beta*box-2*a*r*r*rho),
                      ("ee",beta*Hee-aa/2-beta*box-2*a*r*r*p),
                      ("ne",beta*Hne-2*a*r*r*J)):
        exact("orbit_action_"+name,expr)

    class SaturationClock(legacy.StaggeredClockGrid):
        """Retain parity/adjoint stencils; replace every gravity equation."""
        def __init__(self,radius,h,length=ell):
            super().__init__(ref,radius,h,"harmonic")
            self.length = length
            self.density_scale = 1.0
            self.minimum_stage_A = self.minimum_stage_face_A = math.inf
            self.minimum_stage_lapse = self.minimum_stage_q = math.inf
            self.minimum_stage_mu = self.minimum_stage_u = math.inf
            self.maximum_stage_q = 0.0
            self.charge_weights = self.engine.vol

        def field_derivative(self,field):
            return self.engine.derivative(field)

        def action_domain(self,mu,q,z):
            u = self.length**2*z
            self.minimum_stage_mu = min(self.minimum_stage_mu,float(np.min(mu)))
            self.minimum_stage_u = min(self.minimum_stage_u,float(np.min(u)))
            self.maximum_stage_q = max(self.maximum_stage_q,float(np.max(q)))
            # The logarithmic action has 0<u<1 plus the checked u=0 limit.
            # No clipping or negative-curvature action is introduced.
            if self.length and np.min(u)<-100*np.finfo(float).eps:
                raise FloatingPointError("NUMERICAL_ACTION_DOMAIN_LIMIT: resolved negative u")
            if not np.all(np.isfinite(u)) or np.max(u)>=1:
                raise FloatingPointError("NUMERICAL_ACTION_DOMAIN_LIMIT: nonfinite or saturated u")

        def geometry(self,state):
            if state.shape!=(6,len(self.r)) or not np.all(np.isfinite(state)):
                raise FloatingPointError("Nonfinite saturation evolution state")
            field,P = state[:2]
            mu,k = state[2].real,self.cell_k(state)
            logL = state[4].real
            if np.max(abs(logL))>500:
                raise FloatingPointError("Unresolved lapse exponential")
            L = np.exp(logL)
            q = 1/(1+2*alpha*self.length**2*mu)
            z = 2*alpha*mu*q
            v = self.r*k
            F = 1-self.r**2*z
            A = F+v*v
            if any(not np.all(np.isfinite(x)) or np.min(x)<=0 for x in (A,q,L)):
                raise FloatingPointError("Saturation cell left positive A,q,L chart")
            self.action_domain(mu,q,z)
            D = self.field_derivative(field)
            square = abs(field)**2
            V = square/2-square**2/4+square**3/24
            root = np.sqrt(A)
            rho = A*(abs(P)**2+abs(D)**2)/2+V
            S = root*np.real(np.conjugate(P)*D)
            if any(not np.all(np.isfinite(x)) for x in (D,V,rho,S)):
                raise FloatingPointError("Nonfinite saturation scalar source")
            return dict(A=A,F=F,L=L,q=q,z=z,v=v,k=k,root=root,D=D,V=V,rho=rho,
                        p=rho-2*V,S=S,beta=L*v)

        def rhs(self,state):
            g = self.geometry(state)
            e,r = self.engine,self.r
            field,P = state[:2]
            L,A,v,q = g["L"],g["A"],g["v"],g["q"]
            c,beta = L*g["root"],g["beta"]
            rf = e.edges[1:]
            vf,logL = state[3].real,state[4].real
            muf = self.to_faces(state[2].real)
            qf = 1/(1+2*alpha*self.length**2*muf)
            zf = 2*alpha*muf*qf
            Af = 1-rf*rf*zf+vf*vf
            Lf = np.exp(self.to_faces(logL))
            if any(not np.all(np.isfinite(x)) or np.min(x)<=0 for x in (Af,qf,Lf)):
                raise FloatingPointError("Saturation face left positive finite A,q,L chart")
            self.action_domain(muf,qf,zf)
            speed = max(np.max(abs(beta)+c),np.max(Lf*(abs(vf)+np.sqrt(Af))))
            if e.time_step is not None:
                e.maximum_courant = max(e.maximum_courant,e.time_step*speed/self.h)
                if e.maximum_courant>=0.4:
                    raise FloatingPointError("Saturation matter/gauge Courant bound exceeded")
            self.minimum_stage_A = min(self.minimum_stage_A,float(np.min(A)))
            self.minimum_stage_face_A = min(self.minimum_stage_face_A,float(np.min(Af)))
            self.minimum_stage_lapse = min(self.minimum_stage_lapse,float(np.min(L)),float(np.min(Lf)))
            self.minimum_stage_q = min(self.minimum_stage_q,float(np.min(q)),float(np.min(qf)))
            # Same weighted-adjoint matter flux pair as the retained engine.
            edge_beta = e.edges[1:-1]**2*(beta[:-1]+beta[1:])/2
            advflux = np.zeros(len(r)+1,complex)
            waveflux = advflux.copy()
            advflux[1:-1] = edge_beta*(P[:-1]+P[1:])/2
            face = edge_beta*np.diff(field)/2
            advfield = np.zeros_like(field)
            advfield[:-1] += face/e.vol[:-1]
            advfield[1:] += face/e.vol[1:]
            waveflux[1:-1] = e.edges[1:-1]**2*(c[:-1]+c[1:])/2*np.diff(field)/self.h
            square = abs(field)**2
            force = (1-square+square**2/4)*field
            out = np.zeros_like(state)
            out[0] = c*P+advfield
            out[1] = np.diff(advflux+waveflux)/e.vol-L*force/g["root"]
            out[2] = L*(g["k"]*A*(abs(P)**2+abs(g["D"])**2)+(A+v*v)*g["S"]/r)
            dv = np.r_[(np.r_[vf[1:],0.]-np.r_[0.,vf[:-1]])[:-1]/(2*self.h),
                       (3*vf[-1]-4*vf[-2]+vf[-3])/(2*self.h)]
            out[3] = Lf*vf*dv+Lf*rf*(zf*(1-3*self.length**2*zf)/2+
                        alpha*qf*qf*self.to_faces(g["p"]))-Lf*Af*self.face_gradient(logL)
            out[4] = beta*e.derivative(logL)-L*(self.divergence(vf)-alpha*r*q*q*g["S"])
            out[5] = np.exp((9*logL[0]-logL[1])/8)
            if not np.all(np.isfinite(out)):
                raise FloatingPointError("Nonfinite saturation evolution RHS")
            return out

        def measure(self,state,t):
            g = self.geometry(state)
            rhs = self.rhs(state)
            e,r = self.engine,self.r
            mu,k,L,q = state[2].real,g["k"],g["L"],g["q"]
            M = r**3*mu
            d4 = lambda x: (x[:-4]-8*x[1:-3]+8*x[3:-1]-x[4:])/(12*self.h)
            active = r[2:-2]<=80
            norm = lambda x: float(np.linalg.norm(x[active]))
            mass_source = r*r*(g["rho"]+g["v"]*g["S"])
            mass_error = norm(d4(M)-mass_source[2:-2])/max(norm(mass_source[2:-2]),1e-14)
            H = k*k-g["z"]
            Ht = 2*k*self.cell_k(rhs)-2*alpha*q*q*rhs[2].real
            term0 = Ht[2:-2]
            term1 = -L[2:-2]*k[2:-2]*(2*H[2:-2]+r[2:-2]*d4(H))
            term2 = (2*L*k*g["A"])[2:-2]*d4(state[4].real)/r[2:-2]
            term3 = (2*alpha*q*q*L*g["A"]*g["S"]/r)[2:-2]
            scale = abs(term0)+abs(term1)+abs(term2)+abs(term3)+(
                    alpha*L*(abs(g["rho"])+abs(g["p"])))[2:-2]
            metric_error = norm(term0+term1+term2+term3)/max(norm(scale),1e-14)
            origin = 3*mu+r*e.derivative(mu)-g["rho"]-g["v"]*g["S"]
            origin_abs = float(max(abs(origin[:2])))
            origin_scale = max(self.density_scale,float(max(abs(g["rho"][:2]))),1e-14)
            weights = self.charge_weights*np.imag(np.conjugate(state[0])*state[1])
            Q = float(np.sum(weights))
            radius2 = float(np.sum(weights*r*r)/Q)
            if Q<=0 or radius2<=0:
                raise FloatingPointError("Charge-radius diagnostic left positive domain")
            qrate = float(np.sum(self.charge_weights*np.imag(np.conjugate(rhs[0])*state[1]+
                                              np.conjugate(state[0])*rhs[1])))
            j = int(np.argmin(g["F"]))
            theta_minus = -2*(g["root"]+g["v"])/r
            # Direct expression also handles regions with negative shift.
            theta_plus = 2*(g["root"]-g["v"])/r
            safe = g["root"]+g["v"]>1e-8
            theta_plus[safe] = 2*g["F"][safe]/(r[safe]*(g["root"]+g["v"])[safe])
            trapped = (theta_plus<0)&(theta_minus<0)
            longest,current = 0,0
            for value in trapped:
                current = current+1 if value else 0
                longest = max(longest,current)
            monotone = np.all(np.diff(M)>=-1e-9*max(abs(M[-1]),1.))
            return dict(t=float(t),central_proper_time=float(state[5,0].real),
                mass=float(M[-1]),charge=Q,charge_rms_areal=math.sqrt(radius2),
                maximum_density=float(max(g["rho"])),central_density=float((9*g["rho"][0]-g["rho"][1])/8),
                central_lapse=float(np.exp((9*state[4,0].real-state[4,1].real)/8)),
                minimum_F=float(g["F"][j]),minimum_F_radius=float(r[j]),minimum_A=float(min(g["A"])),
                minimum_q=float(min(q)),minimum_lapse=float(min(L)),
                outgoing_expansion=float(theta_plus[j]),ingoing_expansion=float(theta_minus[j]),
                trapped_cells=int(np.sum(trapped)),contiguous_trapped_cells=longest,
                mass_R50=float(np.interp(0.5*M[-1],np.r_[0,M],np.r_[0,r])) if monotone else None,
                radial_constraint=mass_error,regular_metric_residual=metric_error,
                origin_constraint=origin_abs/origin_scale,origin_constraint_absolute=origin_abs,
                origin_density_scale=origin_scale,origin_local_density=float(max(abs(g["rho"][:2]))),
                relative_charge_rate=abs(qrate)/Q,
                charge_legacy_volume=float(np.sum(e.vol*np.imag(np.conjugate(state[0])*state[1]))),
                charge_nodal=float(np.sum(self.h*r*r*np.imag(np.conjugate(state[0])*state[1]))))

        def origin_terms(self,state):
            g = self.geometry(state)
            rhs = self.rhs(state)
            e,r = self.engine,self.r
            field,P = state[:2]
            mu = state[2].real
            mudot = rhs[2].real
            vdot = r*self.cell_k(rhs)
            Adot = -2*alpha*r*r*g["q"]**2*mudot+2*g["v"]*vdot
            D,Ddot = g["D"],self.field_derivative(rhs[0])
            force = (1-abs(field)**2+abs(field)**4/4)*field
            rhodot = Adot*(abs(P)**2+abs(D)**2)/2+g["A"]*np.real(
                np.conjugate(P)*rhs[1]+np.conjugate(D)*Ddot)+np.real(np.conjugate(force)*rhs[0])
            Sdot = Adot*np.real(np.conjugate(P)*D)/(2*g["root"])+g["root"]*np.real(
                np.conjugate(rhs[1])*D+np.conjugate(P)*Ddot)
            terms = dict(three_mu=3*mu,radial_mu=r*e.derivative(mu),minus_rho=-g["rho"],minus_vS=-g["v"]*g["S"])
            rates = dict(three_mudot=3*mudot,radial_mudot=r*e.derivative(mudot),minus_rhodot=-rhodot,
                         minus_vdotS=-vdot*g["S"],minus_vSdot=-g["v"]*Sdot)
            return g,rhs,terms,rates

        def origin_snapshot(self,state,t):
            g,rhs,terms,rates = self.origin_terms(state)
            e,r = self.engine,self.r
            ext2 = lambda x:(9*x[0]-x[1])/8
            ext3 = lambda x:(150*x[0]-25*x[1]+3*x[2])/128
            central = {}
            for name,ext in (("two_point",ext2),("three_point",ext3)):
                f0,P0,mu0 = ext(state[0]),ext(state[1]),ext(state[2].real)
                rho0 = abs(P0)**2/2+abs(f0)**2/2-abs(f0)**4/4+abs(f0)**6/24
                force0 = (1-abs(f0)**2+abs(f0)**4/4)*f0
                rhodot0 = float(np.real(np.conjugate(P0)*ext(rhs[1])+np.conjugate(force0)*ext(rhs[0])))
                f2 = (-34*state[0,0]+39*state[0,1]-5*state[0,2])/(48*self.h**2)
                k0 = (8*state[3,0].real-state[3,1].real)/(6*self.h)
                L0 = math.exp(float(ext(state[4].real)))
                expected = L0*(k0*abs(P0)**2+2*np.real(np.conjugate(P0)*f2))
                mudot0 = float(ext(rhs[2].real))
                central[name] = dict(mu=float(mu0),rho=float(rho0),constraint=float(3*mu0-rho0),
                    source_extrapolation_constraint=float(3*mu0-ext(g["rho"])),
                    mudot=mudot0,rhodot=rhodot0,constraint_rate=3*mudot0-rhodot0,
                    continuum_mudot=float(expected),mudot_defect=float(mudot0-expected),
                    rhodot_defect=float(rhodot0-3*expected),k=k0,L=L0)
            C = sum(terms.values())
            Cdot = sum(rates.values())
            fixed = fixed_mass_audit(r,state[2].real,g["rho"]+g["v"]*g["S"])
            take = lambda x:[float(y) for y in x[:8]]
            snapshot = dict(t=t,r=take(r),constraint=take(C),constraint_rate=take(Cdot),
                terms={key:take(value) for key,value in terms.items()},
                rates={key:take(value) for key,value in rates.items()},central=central,fixed_radius=fixed,
                phi_real=take(state[0].real),phi_imag=take(state[0].imag),P_real=take(state[1].real),P_imag=take(state[1].imag))
            snapshot["leading_quartic_budget"] = origin_quartic_budget(snapshot,self.h)
            return snapshot

    class PairedSaturationClock(SaturationClock):
        """Same continuum source/gauge with an adjoint nodal matter pair."""
        def __init__(self,radius,h,length=ell):
            super().__init__(radius,h,length)
            self.pair = RadialNodalPair(self.r,h)
            self.charge_weights = self.pair.weights

        def field_derivative(self,field):
            return self.pair.E@field

        def rhs(self,state):
            # Gravity still evolves by its own time equations, never a
            # projection onto the radial or centre constraint.
            out = super().rhs(state)
            g = self.geometry(state)
            field,P = state[:2]
            if self.engine.time_step is not None:
                cmax = max(float(max(g["L"]*g["root"])),float(max(self.pair.I@(g["L"]*g["root"]))))
                number = self.engine.time_step*cmax*self.pair.wave_frequency_bound
                self.pair.maximum_wave_RK_number = max(self.pair.maximum_wave_RK_number,number)
                if number>=2.5:
                    raise FloatingPointError("Paired frozen-wave RK4 bound exceeded")
            advfield,advP = self.pair.transport(field,P,g["beta"])
            force = (1-abs(field)**2+abs(field)**4/4)*field
            out[0] = g["L"]*g["root"]*P+advfield
            out[1] = self.pair.wave(field,g["L"]*g["root"])+advP-g["L"]*force/g["root"]
            if not np.all(np.isfinite(out)):
                raise FloatingPointError("Nonfinite paired saturation RHS")
            return out

    def fixed_mass_audit(r,mu,source):
        from scipy.interpolate import CubicSpline
        # Independent nodal reconstructions and exact polynomial quadratures.
        # No centre/edge or source-density/mass identification is imposed.
        n = int(np.searchsorted(r,.8))+4
        x = np.r_[-r[:n][::-1],r[:n]]
        cubic_mu = CubicSpline(x,np.r_[mu[:n][::-1],mu[:n]])
        cubic_source = CubicSpline(x,np.r_[source[:n][::-1],source[:n]])
        def linear_even(y,points):
            out = np.interp(points**2,r[:n]**2,y[:n])
            low = points<r[0]
            out[low] = y[0]+(points[low]**2-r[0]**2)*(y[1]-y[0])/(r[1]**2-r[0]**2)
            return out
        nodes,weights = np.polynomial.legendre.leggauss(3)
        result = []
        for R in (.1,.2,.4):
            breaks = np.r_[0.,r[r<R],R]
            centres,widths = (breaks[1:]+breaks[:-1])/2,np.diff(breaks)/2
            points = (centres[:,None]+widths[:,None]*nodes).ravel()
            w = (widths[:,None]*weights).ravel()*points**2
            mass_cubic = float(R**3*cubic_mu(R))
            mass_linear = float(R**3*linear_even(mu,np.array([R]))[0])
            int_cubic = float(np.sum(w*cubic_source(points)))
            int_linear = float(np.sum(w*linear_even(source,points)))
            result.append(dict(r=R,mass_cubic=mass_cubic,source_mass_cubic=int_cubic,
                constraint_cubic=(mass_cubic-int_cubic)/R**3,
                constraint_linear=(mass_linear-int_linear)/R**3,
                quadrature_source_difference=abs(int_cubic-int_linear)/R**3))
        return result

    zero_grid = SaturationClock(4,.1)
    zero = np.zeros((6,len(zero_grid.r)),complex)
    zr = zero_grid.rhs(zero)
    test("horizon_zero_field",np.max(abs(zr[:5]))==0 and np.max(abs(zr[5]-1))==0)
    bad = zero.copy()
    bad[2] = -1e-5
    try:
        zero_grid.rhs(bad)
        rejected = False
    except FloatingPointError:
        rejected = True
    test("negative_action_branch_rejected",rejected)
    bad = zero.copy()
    bad[4,-2],bad[4,-1] = 500,-500
    with np.errstate(under="ignore",over="ignore",invalid="ignore"):
        try:
            zero_grid.rhs(bad)
            rejected = False
        except FloatingPointError:
            rejected = True
    test("nonpositive_face_lapse_rejected",rejected)
    old = legacy.StaggeredClockGrid(ref,4,.1)
    new = SaturationClock(4,.1,length=0)
    state = zero.copy()
    state[0] = .2*np.exp(-(new.r/2)**2)*(1+.1j)
    state[1] = (.03+.12j)*np.exp(-(new.r/2)**2)
    state[2] = .01*np.exp(-(new.r/3)**2)
    state[3] = .01*new.engine.edges[1:]
    state[4] = -.03*np.exp(-(new.r/2)**2)
    discrepancy = float(np.max(abs(old.rhs(state)-new.rhs(state))))
    test("horizon_full_Einstein_RHS_limit",discrepancy<1e-12,error=discrepancy)
    kval = math.sqrt(2*alpha/(9+2*alpha*ell*ell))
    core_errors = []
    for dt in (.05,.025):
        grid = SaturationClock(4,.1)
        core = zero.copy()
        core[0],core[2],core[3],core[4] = math.sqrt(2),1/9,kval*grid.engine.edges[1:],math.log(.7)
        for _ in range(round(1/dt)):
            core = legacy.clock_rk4(grid,core,dt)
        lapse = .7/(1+3*kval*.7)
        proper = math.log1p(3*kval*.7)/(3*kval)
        error = float(max(np.max(abs(core[:2]-np.array([np.full(len(grid.r),math.sqrt(2)),np.zeros(len(grid.r))]))),
            np.max(abs(core[2]-1/9)),np.max(abs(grid.cell_k(core)-kval)),
            np.max(abs(np.exp(core[4].real)-lapse)),np.max(abs(core[5]-proper))))
        core_errors.append(error)
    test("saturated_core_harmonic_clock",core_errors[-1]<1e-8 and (core_errors[-1]<1e-12 or core_errors[-1]<.2*core_errors[0]),errors=core_errors)
    if origin_audit:
        test("origin_list_comparison_control",relative_array_error([1.,-2.],[1.,-2.])==0 and
             abs(relative_array_error([1.,-2.],[1.,-1.])-.5)<1e-15)
        polynomial_errors = []
        for h in (.1,.05,.025):
            grid = SaturationClock(4,h)
            r = grid.r
            src = 1+.2*r*r+.03*r**4
            mu = 1/3+.04*r*r+.03*r**4/7
            result = fixed_mass_audit(r,mu,src)
            polynomial_errors.append(max(abs(row["constraint_cubic"]) for row in result))
            C = 3*mu+r*grid.engine.derivative(mu)-src
            expected = 4*(.03/7)*r[:2]**2*h*h
            test("origin_even_polynomial_"+str(h),np.max(abs(C[:2]-expected))<1e-14)
            # Off-shell isolated principal part, evaluated by the actual RHS.
            # This does not project a collapse state or change its evolution.
            manufactured = np.zeros((6,len(r)),complex)
            manufactured[0],manufactured[1] = r**4,1.
            out = grid.rhs(manufactured)
            force = (1-r**8+r**16/4)*r**4
            wave = (out[1]+force).real
            mass_rate = 3*out[2].real+r*grid.engine.derivative(out[2].real)
            wave_error = float(np.max(abs(wave[:2]-20*r[:2]**2-h*h*np.array([10.,78/7]))))
            mass_error = float(np.max(abs(mass_rate[:2]-20*r[:2]**2-12*h*h)))
            budget_error = float(np.max(abs((mass_rate-wave)[:2]-h*h*np.array([2.,6/7]))))
            test("origin_quartic_production_operators_"+str(h),
                 max(wave_error,mass_error,budget_error)<1e-12,
                 wave_error=wave_error,mass_error=mass_error,budget_error=budget_error)
        test("fixed_radius_polynomial_refinement",polynomial_errors[-1]<1e-6 and
             polynomial_errors[-1]<.2*polynomial_errors[-2],errors=polynomial_errors)
        grid = SaturationClock(4,.1)
        g,rhs,terms,rates = grid.origin_terms(state)
        eps = 1e-6
        def C_at(y):
            gg = grid.geometry(y)
            return 3*y[2].real+grid.r*grid.engine.derivative(y[2].real)-gg["rho"]-gg["v"]*gg["S"]
        fd = (C_at(state+eps*rhs)-C_at(state-eps*rhs))/(2*eps)
        error = float(np.max(abs(fd[:8]-sum(rates.values())[:8])))
        test("origin_constraint_rate_chain_rule",error<1e-8,error=error)
    if paired_origin:
        sixth_errors = []
        for h in (.1,.05,.025):
            grid = PairedSaturationClock(4,h)
            r,pair = grid.r,grid.pair
            manufactured = np.zeros((6,len(r)),complex)
            manufactured[0],manufactured[1] = r**4,1.
            out = grid.rhs(manufactured)
            wave = pair.wave(r**4,np.ones_like(r))
            mass_rate = 3*out[2].real+r*grid.engine.derivative(out[2].real)
            error = float(np.max(abs((mass_rate-wave)[:2])))
            poly = max(float(np.max(abs(pair.wave(r**power,np.ones_like(r))[:3]-
                (np.zeros(3) if power==0 else power*(power+1)*r[:3]**(power-2)))))
                for power in (0,2,4))
            test("paired_centre_polynomial_"+str(h),max(error,poly)<1e-10,
                 mass_wave_mismatch=error,polynomial_error=poly)
            mixed_error = float(max(abs(pair.wave(r*r,1+.2*r*r)[:3]-(6+2*r[:3]**2))))
            test("paired_variable_coefficient_"+str(h),mixed_error<1e-10,error=mixed_error)
            sixth_errors.append(float(max(abs(pair.wave(r**6,np.ones_like(r))[:3]-42*r[:3]**4))))
        test("paired_sixth_power_refinement",sixth_errors[-1]<.1*sixth_errors[-2] and
             sixth_errors[-2]<.1*sixth_errors[0],errors=sixth_errors)
        grid = PairedSaturationClock(4,.1)
        r,pair = grid.r,grid.pair
        rng = np.random.default_rng(92011)
        field = rng.normal(size=len(r))+1j*rng.normal(size=len(r))
        P = rng.normal(size=len(r))+1j*rng.normal(size=len(r))
        beta = .02*r*np.exp(-r*r)
        advfield,advP = pair.transport(field,P,beta)
        wave = pair.wave(field,.7+.1*np.exp(-r*r))
        terms = pair.weights*np.imag(np.conjugate(advfield)*P+np.conjugate(field)*(advP+wave))
        error = float(abs(np.sum(terms))/max(np.sum(abs(terms)),1e-30))
        test("paired_charge_adjoint_identity",error<1e-13,error=error)
        spectra = []
        for cf in (np.ones(len(r)+1),pair.I@(.7+.1*np.exp(-r*r)),
                   pair.I@(.3+.7*r*r/(1+r*r)),np.where(np.arange(len(r)+1)==4,100.,1.)):
            a = pair.face_measure*cf
            base = -(pair.GT@pair.G.multiply(a[:,None])).toarray()
            matrix = base/r[:,None]/r[None,:]
            eigen = np.linalg.eigvalsh(matrix)
            spectra.append(float(eigen[-1]/max(abs(eigen[0]),1)))
        test("paired_wave_spectrum_controls",max(spectra)<1e-12 and np.min(pair.weights)>0,
             largest_normalized_eigenvalues=spectra)
        test("paired_wave_RK_bound",.1*grid.h*pair.wave_frequency_bound<2.5,
             unit_speed_RK_number=.1*grid.h*pair.wave_frequency_bound)
        manufactured = np.zeros((6,len(r)),complex)
        manufactured[0] = .2*np.exp(-r*r)*(1+.2j)
        manufactured[1] = (.05+.1j)*np.exp(-r*r)
        manufactured[2] = .01*np.exp(-r*r/4)
        manufactured[3] = .01*grid.engine.edges[1:]
        manufactured[4] = -.03*np.exp(-r*r)
        rhs = grid.rhs(manufactured)
        qterms = pair.weights*np.imag(np.conjugate(rhs[0])*manufactured[1]+np.conjugate(manufactured[0])*rhs[1])
        test("paired_full_RHS_charge",abs(float(np.sum(qterms)))<1e-12,
             charge_rate=float(np.sum(qterms)))
        g,rhs,terms,rates = grid.origin_terms(manufactured)
        def paired_C(y):
            gg = grid.geometry(y)
            return 3*y[2].real+r*grid.engine.derivative(y[2].real)-gg["rho"]-gg["v"]*gg["S"]
        eps = 1e-6
        fd = (paired_C(manufactured+eps*rhs)-paired_C(manufactured-eps*rhs))/(2*eps)
        error = float(np.max(abs(fd[:8]-sum(rates.values())[:8])))
        test("paired_constraint_chain_rule",error<1e-8,error=error)
    if any(not c["passed"] for c in checks):
        failed = [c for c in checks if not c["passed"]]
        return dict(decision="COLLAPSE_PREFLIGHT_FAILURE",checks=len(checks),passed=len(checks)-len(failed),
                    failed=failed,details=checks)
    if origin_controls:
        test("unchanged_run_sources",all(hashlib.sha256(path.read_bytes()).hexdigest()==entry_hashes[path.name] for path in hash_paths))
        failed = [c for c in checks if not c["passed"]]
        return dict(decision=("PAIRED_ORIGIN_CONTROLS_ONLY" if paired_origin else "ORIGIN_CONTROLS_ONLY") if not failed else "ORIGIN_DIAGNOSTIC_CONTROL_FAILURE",
            checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,
            code_sha256=entry_hashes[Path(__file__).name],source_hashes=entry_hashes)

    def run(h,duration=80.,radius=120.,courant=.1,event_stop=False):
        start = time.perf_counter()
        polar = PolarGrid(radius,h)
        packet = initial(polar)
        geometry = polar.geometry(*packet)
        grid = (PairedSaturationClock if paired_origin else SaturationClock)(radius,h)
        state = np.zeros((6,len(grid.r)),complex)
        state[:2] = packet
        state[2] = geometry["mass"]/grid.r**3
        state[4] = np.log(geometry["sigma"]*np.sqrt(geometry["N"]))
        grid.density_scale = float(max(grid.geometry(state)["rho"]))
        steps = math.ceil(.25/(courant*h))
        dt = .25/steps
        grid.engine.time_step = dt
        rows,status,error = [],"COMPLETED",None
        snapshots = []
        event_time = None
        try:
            rows.append(grid.measure(state,0))
            for n in range(round(duration/.25)):
                for _ in range(steps):
                    state = legacy.clock_rk4(grid,state,dt)
                t = (n+1)*.25
                row = grid.measure(state,t)
                rows.append(row)
                if origin_audit and t in (27.5,27.75,28.):
                    snapshots.append(grid.origin_snapshot(state,t))
                if n%40==39:
                    print(f"Saturation h={h} R={radius} t={t}: Fmin={row['minimum_F']:.6g}",file=sys.stderr,flush=True)
                if event_stop and event_time is None and row["minimum_F"]<-.02 and row["trapped_cells"]>0:
                    event_time = t
                if event_stop and event_time is not None and t>=event_time+1:
                    status = "TRAPPING_CANDIDATE"
                    break
        except (FloatingPointError,ValueError) as exc:
            status,error = "NUMERICAL_LIMIT",str(exc)
        print(f"Saturation h={h} R={radius}: {status}, last={rows[-1]['t'] if rows else 0}, {time.perf_counter()-start:.1f}s",file=sys.stderr,flush=True)
        return dict(h=h,radius=radius,courant=courant,dt=dt,status=status,error=error,
            elapsed_seconds=time.perf_counter()-start,samples=rows,origin_snapshots=snapshots,
            stage_minimum_A=grid.minimum_stage_A,stage_minimum_face_A=grid.minimum_stage_face_A,
            stage_minimum_lapse=grid.minimum_stage_lapse,stage_minimum_q=grid.minimum_stage_q,
            stage_minimum_mu=grid.minimum_stage_mu,stage_minimum_u=grid.minimum_stage_u,
            stage_maximum_q=grid.maximum_stage_q,
            maximum_Courant=grid.engine.maximum_courant,
            maximum_paired_wave_RK_number=grid.pair.maximum_wave_RK_number if paired_origin else None)

    if origin_audit and not paired_origin:
        cases = (dict(finer=run(.0125,28.)) if origin_finer else
                 dict(coarse=run(.1,28.),middle=run(.05,28.),fine=run(.025,28.),half_step=run(.025,28.,courant=.05)))
        for name,case in cases.items():
            test("origin_replay_completed_"+name,case["status"]=="COMPLETED" and case["samples"][-1]["t"]==28.)
        if not origin_finer:
            expected = dict(middle=.00012779792090901636,fine=.00019595006468986798)
            for name,target in expected.items():
                actual = max(row["origin_constraint"] for row in cases[name]["samples"] if row["t"]<=27.75)
                test("reproduce_original_origin_"+name,abs(actual-target)<1e-10,actual=actual,expected=target)
            a,b = cases["fine"]["origin_snapshots"][1],cases["half_step"]["origin_snapshots"][1]
            error = relative_array_error(a["constraint"][:2],b["constraint"][:2])
            test("origin_time_step_control",error<1e-3,relative_error=error)
        test("unchanged_run_sources",all(hashlib.sha256(path.read_bytes()).hexdigest()==entry_hashes[path.name] for path in hash_paths))
        # Keep the requested transition records, not an extra generated dataset.
        for case in cases.values():
            case["samples"] = [row for row in case["samples"] if row["t"]==0 or row["t"]>=26.]
        failed = [c for c in checks if not c["passed"]]
        return dict(decision="ORIGIN_DIAGNOSTIC_COMPUTED" if not failed else "ORIGIN_DIAGNOSTIC_CONTROL_FAILURE",
            checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,cases=cases,
            code_sha256=entry_hashes[Path(__file__).name],source_hashes=entry_hashes,
            scope=dict(changed_evolution_equations=False,changed_original_gate=False,resolved_trapping=False,singularity_removal=False))

    pilot = run(.1,28.) if paired_origin else run(.1,event_stop=True)
    if pilot_only:
        test("unchanged_run_sources",all(hashlib.sha256(path.read_bytes()).hexdigest()==entry_hashes[path.name] for path in hash_paths))
        failed = [c for c in checks if not c["passed"]]
        return dict(decision="COLLAPSE_PILOT_ONLY",checks=len(checks),passed=len(checks)-len(failed),failed=failed,
            details=checks,pilot=pilot,code_sha256=entry_hashes[Path(__file__).name],source_hashes=entry_hashes)
    endpoint = 28. if paired_origin else pilot["samples"][-1]["t"]-(.5 if pilot["status"]=="NUMERICAL_LIMIT" else 0)
    if endpoint<.25:
        raise RuntimeError("No finite pilot interval to refine")
    cases = dict(coarse=pilot,middle=run(.05,endpoint),fine=run(.025,endpoint),
                 half_step=run(.025,endpoint,courant=.05),domain=run(.025,endpoint,radius=160))

    def verdict(end,case_set=None):
        gates,residuals,differences = {},{},{}
        selected = {name:[row for row in case["samples"] if row["t"]<=end+1e-10]
                    for name,case in (cases if case_set is None else case_set).items()}
        if any(not rows or abs(rows[-1]["t"]-end)>1e-8 for rows in selected.values()):
            return dict(passed=False,gates=dict(common_time=False),end=end,resolved_trapping=False)
        required = ("t","mass","charge","radial_constraint","regular_metric_residual","origin_constraint",
                    "minimum_F","maximum_density","charge_rms_areal","central_proper_time",
                    "contiguous_trapped_cells","trapped_cells","outgoing_expansion","ingoing_expansion")
        if any(not np.isfinite(row[key]) for rows in selected.values() for row in rows for key in required):
            return dict(passed=False,gates=dict(finite_diagnostics=False),end=end,resolved_trapping=False)
        for name,rows in selected.items():
            gates[name+"_charge"] = max(abs(row["charge"]/rows[0]["charge"]-1) for row in rows)<1e-5
            gates[name+"_mass"] = max(abs(row["mass"]/rows[0]["mass"]-1) for row in rows)<5e-3
        for key in ("radial_constraint","regular_metric_residual","origin_constraint"):
            middle = max(row[key] for row in selected["middle"])
            fine = max(row[key] for row in selected["fine"])
            gates[key] = fine<5e-3 and (fine<1e-6 or fine<.6*middle)
            residuals[key] = dict(middle=middle,fine=fine)
        for key in ("minimum_F","maximum_density","charge_rms_areal","central_proper_time"):
            arrays = {name:np.array([row[key] for row in rows]) for name,rows in selected.items()}
            scale = max(float(np.max(abs(arrays["fine"]))),1e-12)
            normdiff = lambda a,b:float(np.max(abs(arrays[a]-arrays[b]))/scale)
            cm,mf = normdiff("coarse","middle"),normdiff("middle","fine")
            half,domain = normdiff("half_step","fine"),normdiff("domain","fine")
            gates[key+"_refinement"] = mf<1e-4 or mf<.6*cm
            gates[key+"_controls"] = max(half,domain)<1e-3
            differences[key] = dict(coarse_middle=cm,middle_fine=mf,half_step=half,domain=domain)
        resolved = False
        if all(gates.values()) and min(len(x) for x in selected.values())>=2:
            resolved = True
            for offset in (-2,-1):
                last = {name:rows[offset] for name,rows in selected.items()}
                uncertainty = 3*max(abs(last["fine"]["minimum_F"]-last[name]["minimum_F"])
                                     for name in ("middle","half_step","domain"))
                resolved &= last["fine"]["contiguous_trapped_cells"]>=4 and all(
                    row["minimum_F"]<-max(.005,uncertainty) and row["outgoing_expansion"]<0
                    and row["ingoing_expansion"]<0 and row["trapped_cells"]>0 for row in last.values())
        return dict(passed=bool(all(gates.values())),gates={k:bool(v) for k,v in gates.items()},
                    end=end,residuals=residuals,differences=differences,resolved_trapping=bool(resolved))

    def certify(end,case_set=None):
        accepted,first_rejected,first_trapping = None,None,None
        for stop in np.arange(.25,end+1e-9,.25):
            current = verdict(float(stop),case_set)
            if not current["passed"]:
                first_rejected = current
                break
            accepted = current
            if current["resolved_trapping"] and first_trapping is None:
                first_trapping = current
        return accepted,first_rejected,first_trapping

    # Decision-only fixtures: no evolution and no change to physical budgets.
    fixture_rows = []
    for t,Fval in zip((0.,.25,.5,.75),(.7,-.02,-.02,.1)):
        fixture_rows.append(dict(t=t,mass=1.,charge=1.,radial_constraint=1e-8,
            regular_metric_residual=1e-8,origin_constraint=1e-8,minimum_F=Fval,
            maximum_density=1.,charge_rms_areal=1.,central_proper_time=t,
            contiguous_trapped_cells=4 if Fval<0 else 0,trapped_cells=4 if Fval<0 else 0,
            outgoing_expansion=-1. if Fval<0 else 1.,ingoing_expansion=-1.))
    fixture = {name:dict(samples=[dict(row) for row in fixture_rows]) for name in cases}
    fa,fr,ft = certify(.75,fixture)
    test("transient_trapping_certificate_retained",fa["end"]==.75 and fr is None and
         ft is not None and ft["end"]==.5 and not fa["resolved_trapping"])
    for key in ("radial_constraint","regular_metric_residual","origin_constraint","mass","charge"):
        saved = fixture["fine"]["samples"][-1][key]
        fixture["fine"]["samples"][-1][key] = float("nan")
        test("nonfinite_"+key+"_rejected",not verdict(.75,fixture)["passed"])
        fixture["fine"]["samples"][-1][key] = saved

    terminal = verdict(endpoint)
    accepted,first_rejected,first_trapping = certify(endpoint)
    for name,condition in terminal.get("gates",{}).items():
        test("terminal_"+name,condition)
    sources_unchanged = all(hashlib.sha256(path.read_bytes()).hexdigest()==entry_hashes[path.name] for path in hash_paths)
    test("unchanged_run_sources",sources_unchanged)
    failed = [c for c in checks if not c["passed"]]
    certification_valid = all(c["passed"] for c in checks if not c["name"].startswith("terminal_"))
    trapping = first_trapping is not None and certification_valid
    return dict(decision="INVALID_CERTIFICATION_CONTROLS" if not certification_valid else
                ("PAIRED_ORIGIN_REPAIR_VALIDATED" if accepted is not None and accepted["end"]==28. else "PAIRED_ORIGIN_REPAIR_OPEN") if paired_origin else
                "VALIDATED_FUTURE_TRAPPING" if trapping else
                "VALIDATED_PRETRAPPING_PREFIX" if accepted else "UNRESOLVED_COLLAPSE",
        checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,
        pilot_end=endpoint,terminal=terminal,accepted_prefix=accepted,first_rejected=first_rejected,
        first_trapping=first_trapping,cases=cases,
        source_prerequisite=dict(checks=source["checks"],passed=source["passed"],parameters=source["parameters"]),
        code_sha256=entry_hashes[Path(__file__).name],engine_sha256=entry_hashes[Path(legacy.__file__).name],
        source_hashes=entry_hashes,
        scope=dict(resolved_trapping=trapping,global_regularity=False,singularity_removal=False,
                   full_RefG_pressure_join=False,same_saturation_action=True,
                   paired_nodal_method=paired_origin,charge_quadrature="h*r^2" if paired_origin else "cell_volume"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--oscillon-source", action="store_true")
    parser.add_argument("--oscillon-dynamics", action="store_true")
    parser.add_argument("--dynamics-pilot", action="store_true")
    parser.add_argument("--supercritical-data", action="store_true")
    parser.add_argument("--saturation-collapse", action="store_true")
    parser.add_argument("--collapse-pilot", action="store_true")
    parser.add_argument("--origin-audit", action="store_true")
    parser.add_argument("--origin-finer", action="store_true")
    parser.add_argument("--origin-controls", action="store_true")
    parser.add_argument("--paired-origin", action="store_true")
    parser.add_argument("--paired-controls", action="store_true")
    args = parser.parse_args()
    if (args.saturation_collapse or args.collapse_pilot or args.origin_audit or args.origin_finer or args.origin_controls or args.paired_origin or args.paired_controls) and (args.supercritical_data or args.oscillon_source or args.oscillon_dynamics or args.dynamics_pilot):
        parser.error("Choose collapse or a previous stage")
    if args.supercritical_data and (args.oscillon_source or args.oscillon_dynamics or args.dynamics_pilot):
        parser.error("Choose initial data or the existing source/dynamics tests")
    if args.oscillon_source and (args.oscillon_dynamics or args.dynamics_pilot):
        parser.error("Choose stationary or dynamical checks")
    result = (collapse_checks(pilot_only=args.collapse_pilot,
                             origin_audit=args.origin_audit or args.origin_finer or args.origin_controls or args.paired_origin or args.paired_controls,
                             origin_finer=args.origin_finer,origin_controls=args.origin_controls or args.paired_controls,
                             paired_origin=args.paired_origin or args.paired_controls)
              if args.saturation_collapse or args.collapse_pilot or args.origin_audit or args.origin_finer or args.origin_controls or args.paired_origin or args.paired_controls else
              supercritical_data_checks() if args.supercritical_data else
              dynamics_checks(pilot=args.dynamics_pilot) if args.oscillon_dynamics or args.dynamics_pilot
              else oscillon_checks() if args.oscillon_source else run_checks())
    if not args.verbose:
        result.pop("details")
    print(json.dumps(result, indent=2, allow_nan=False))
    return int(bool(result["failed"]))


if __name__ == "__main__":
    raise SystemExit(main())
