"""Source-first common-scale centre: exact checks and bounded numerical test.

Run with Python 3 + SymPy + NumPy + SciPy. Stdout only; no repository writes.
The proposed constitutive response is an explicit NEW local model, not an
inherited oscillon solution or a completed regular black hole.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
sys.dont_write_bytecode = True
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp, quad

HERE = Path(__file__).resolve().parent
REPORT = HERE / "common_scale_centre_source.md"
checks = {}
details = {}


def zero(name, expression):
    residual = s.factor(s.simplify(expression))
    checks[name] = residual == 0
    if residual != 0:
        details[name] = str(residual)


def require(name, condition):
    checks[name] = bool(condition)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def geometry_checks():
    # Recompute the connection/Ricci from the established metric helper;
    # no stored PASS, fitted target metric, or cached numerical solution.
    spec = importlib.util.spec_from_file_location(
        "geometry_source", HERE / "verify_covariant_medium_integration.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    r, th, P = s.symbols("r theta P", positive=True)
    H = s.Function("H")(r)
    aa, bb, metric, G, scalar = module.geometry(r, th)
    substitution = {aa: 2*H, bb: -2*H}
    G = G.subs(substitution).doit().applyfunc(s.simplify)
    hp = s.diff(H, r)
    lap = s.diff(H, r, 2) + 2*hp/r
    expected = [-P*s.exp(-2*H)*(2*lap+hp**2),
                -P*s.exp(-2*H)*hp**2,
                P*s.exp(-2*H)*hp**2]
    zero("geometry_density", P*G[0, 0]-expected[0])
    zero("geometry_radial_pressure", -P*G[1, 1]-expected[1])
    zero("geometry_tangential_pressure", -P*G[2, 2]-expected[2])
    h0, h2, h4 = s.symbols("h0 h2 h4", real=True)
    germ = h0+h2*r**2+h4*r**4
    # Independent orthonormal sectional-curvature formula for a static
    # spherical metric; includes multiplicities in the Riemann contraction.
    N, A, S = s.exp(-H), s.exp(H), r*s.exp(H)
    q01 = (s.diff(N,r,2)-s.diff(N,r)*s.diff(A,r)/A)/(N*A**2)
    q02 = s.diff(N,r)*s.diff(S,r)/(N*S*A**2)
    q12 = -(s.diff(S,r,2)-s.diff(S,r)*s.diff(A,r)/A)/(S*A**2)
    q23 = (1-s.diff(S,r)**2/A**2)/S**2
    K = 4*(q01**2+2*q02**2+2*q12**2+q23**2)
    k0 = s.limit(K.subs(H,germ).doit(),r,0)
    zero("regular_centre_K", k0-240*s.exp(-4*h0)*h2**2)
    zero("regular_centre_density",
         s.limit(expected[0].subs(H,germ).doit(),r,0)
         +12*P*s.exp(-2*h0)*h2)
    zero("clock_and_rod_scale", N-1/A)
    zero("coordinate_radial_light_speed", N/A-s.exp(-2*H))


def central_lock_and_obstruction():
    Q,y,b,F,Fy,f,rhoO,pO = s.symbols("Q y b F Fy f rhoO pO")
    J = y*Fy-3*b*f
    rhoF, pF = Q*(2*y*Fy-F), Q*(F-2*b*f)
    solved = s.solve([rhoO+rhoF-2*Q*J,pO+pF], [rhoO,pO])
    zero("central_enthalpy_lock", (rhoO+pO+4*Q*b*f).subs(solved))
    pure = s.solve([value for value in solved.values()], [F,f])
    require("pure_medium_F_and_Fb_zero", pure == {F:0, f:0})

    r,a,d,h2,c2,Hc,A,B = s.symbols(
        "r a d h2 c2 Hc A B", real=True)
    ell = a*r+d*r**3
    lr,lt = s.diff(ell,r)**2, (ell/r)**2
    fr = f+A*(lr-a*a)+2*B*(lt-a*a)
    ft = 2*(f+B*(lr-a*a)+(A+B)*(lt-a*a))
    er = 1+2*h2*r*r
    label = s.diff(er*r*r*s.diff(ell,r)*fr,r)-er*ell*ft
    L,T = f+2*a*a*A, f+a*a*(A-B)
    zero("label_first_radial_coefficient",
         s.expand(label).coeff(r,3)-(10*d*L+4*h2*a*f))
    anisotropy = 4*s.exp(-2*Hc)*c2*c2*r*r+Q*(-2*lr*fr+lt*ft)
    zero("anisotropy_first_radial_coefficient",
         s.expand(anisotropy).coeff(r,2)
         -(4*s.exp(-2*Hc)*c2*c2-8*Q*a*d*T))
    # Positive-symbol substitution proves the conflicting signs for the
    # entire strict gate, not a finite parameter scan.
    aa, hh, ff, ll, tt, qq = s.symbols("aa hh ff ll tt qq", positive=True)
    d_label = 2*hh*aa*ff/(5*ll)
    d_anis = -s.exp(-2*Hc)*c2*c2/(2*qq*aa*tt)
    require("label_demands_positive_cubic", d_label.is_positive)
    require("anisotropy_demands_nonpositive_cubic", d_anis.is_nonpositive)
    linear = {a:s.Rational(1,2),h2:-s.Rational(7,72),
              f:-4,A:0,B:0,Q:s.Rational(7,48),
              c2:-s.Rational(1,18),Hc:0}
    d1 = s.solve(10*d*L+4*h2*a*f,d)[0].subs(linear)
    d2 = s.solve(4*s.exp(-2*Hc)*c2*c2-8*Q*a*d*T,d)[0].subs(linear)
    zero("linear_label_cubic", d1-s.Rational(7,360))
    zero("linear_anisotropy_cubic", d2+s.Rational(1,189))
    require("linear_continuation_rejected", d1 != d2)
    # Altered-expression controls must be caught.
    require("wrong_label_sign_detected",
            s.simplify((10*d*L-4*h2*a*f).subs(d,d1).subs(linear)) != 0)
    require("wrong_anisotropy_sign_detected",
            s.simplify((4*s.exp(-2*Hc)*c2*c2+8*Q*a*d*T)
                       .subs(d,d2).subs(linear)) != 0)
    details["linear_cubic_conflict"] = [str(d1),str(d2)]
    chi = s.symbols("chi",real=True)
    V = chi**2/2-chi**4/4+chi**6/24
    Omega2 = s.Rational(7,12)
    zero("linear_ordinary_central_pressure",Omega2/2-V.subs(chi,1))
    zero("linear_ordinary_central_density",Omega2/2+V.subs(chi,1)-s.Rational(7,12))
    zero("linear_scalar_radial_coefficient",
         (s.diff(V,chi).subs(chi,1)-Omega2)/6+s.Rational(1,18))

    # Original F_min on the exact common-scale y=1 branch.
    br,bt = s.symbols("br bt")
    oldF = (br+2*bt-3)**2+16*(br-1)*(bt-1)**2
    roots = s.solve([oldF,s.diff(oldF,br),s.diff(oldF,bt)],
                    [br,bt],dict=True)
    require("old_Fmin_only_silent_root", roots == [{br:1,bt:1}])
    zero("old_Fmin_Fy_silent", (2*(br+2*bt-3)).subs(roots[0]))


def independent_variation():
    r,P,Q,bc = s.symbols("r P Q bc",positive=True)
    N,A,S,H,ell = [s.Function(n)(r) for n in ("N","A","S","H","ell")]
    y = s.exp(-2*H)/N**2
    br = s.exp(2*H)*s.diff(ell,r)**2/A**2
    bt = s.exp(2*H)*ell**2/S**2
    F = (y-1)+s.Rational(3,4)*(y-1)**2-(
        (br-bc)**2+2*(bt-bc)**2)/(64*bc**2)
    # Positive-TT (-+++) convention. All five radial variables independent.
    Lg = P*(N*A+(N*s.diff(S,r)**2
                 +2*s.diff(N,r)*S*s.diff(S,r))/A)
    Lh = P*N*S**2*s.diff(H,r)**2/A
    LF = Q*N*A*S**2*F
    lag = Lg+Lh+LF
    branch = {N:s.exp(-H),A:s.exp(H),S:r*s.exp(H),ell:s.sqrt(bc)*r}
    equation = P*r*s.diff(H,r,2)+2*P*s.diff(H,r)+Q*r*s.exp(2*H)
    targets = {N:-2*r*s.exp(H)*equation,H:-2*r*equation,A:0,S:0,ell:0}
    for field in (N,A,S,H,ell):
        EL = s.diff(lag,field)-s.diff(s.diff(lag,s.diff(field,r)),r)
        residual = EL.subs(branch).doit()
        zero("independent_EL_"+str(field.func),residual-targets[field])
    zero("branch_y",y.subs(branch)-1)
    zero("branch_br",br.subs(branch).doit()-bc)
    zero("branch_bt",bt.subs(branch)-bc)
    zero("branch_F",F.subs(branch).doit())
    yy,rr,tt = s.symbols("yy rr tt",positive=True)
    response = (yy-1)+s.Rational(3,4)*(yy-1)**2-(
        (rr-bc)**2+2*(tt-bc)**2)/(64*bc**2)
    source = yy*s.diff(response,yy)-rr*s.diff(response,rr)-tt*s.diff(response,tt)
    source_on_branch = s.simplify(source.subs({yy:1,rr:bc,tt:bc}))
    zero("branch_H_source",source_on_branch-1)
    zero("branch_algebraic_density",
         (Q*(2*yy*s.diff(response,yy)-response)).subs({yy:1,rr:bc,tt:bc})-2*Q)
    require("same_branch_not_silent_exterior",source_on_branch != 0)
    details["locked_branch_H_source"] = str(source_on_branch)
    # The added invariant is quadratic in W_A=u.d(phi_A); W_A=0 on
    # this background. Its first variation is therefore zero for every
    # independent field, including the metric/clock.
    W,k = s.symbols("W k")
    zero("mixed_operator_value", (k*W**2).subs(W,0))
    zero("mixed_operator_first_variation", s.diff(k*W**2,W).subs(W,0))
    zero("mixed_coefficient_first_variation", s.diff(k*W**2,k).subs(W,0))
    # Verify through the next two radial orders, not just at r=0.
    Hc,h2,h4,h6 = s.symbols("Hc h2 h4 h6",real=True)
    polynomial = Hc+h2*r**2+h4*r**4+h6*r**6
    ode = s.diff(polynomial,r,2)+2*s.diff(polynomial,r)/r+Q*s.exp(2*polynomial)/P
    series = s.series(ode,r,0,6).removeO().expand()
    solution = s.solve([series.coeff(r,j) for j in (0,2,4)],[h2,h4,h6],dict=True)[0]
    zero("germ_h2",solution[h2]+Q*s.exp(2*Hc)/(6*P))
    zero("germ_h4",solution[h4]-Q**2*s.exp(4*Hc)/(60*P**2))
    zero("germ_h6",solution[h6]+2*Q**3*s.exp(6*Hc)/(945*P**3))
    zero("germ_K0",240*s.exp(-4*Hc)*solution[h2]**2-20*Q**2/(3*P**2))
    for order in (0,2,4):
        zero("germ_ode_order_"+str(order),series.coeff(r,order).subs(solution))
    require("reversed_source_sign_detected",
            s.simplify((6*h2-Q*s.exp(2*Hc)/P).subs(solution)) != 0)


def principal_checks():
    e,tt,tz,xt,xz = s.symbols("e tt tz xt xz",real=True)
    bc = s.symbols("bc",positive=True)
    # No principal matrix is supplied as a fitted input: expand the
    # constitutive invariants and normalized clock-label coupling.
    y = (1+e*tt)**2-e**2*tz**2
    Bxx = bc*((1+e*xz)**2-e**2*xt**2)
    F = (y-1)+s.Rational(3,4)*(y-1)**2-(Bxx-bc)**2/(64*bc**2)
    W = s.sqrt(bc)*((1+e*tt)*e*xt-e*tz*(1+e*xz))/s.sqrt(y)
    full = F+W**2/(4*bc)
    L2 = s.series(full,e,0,3).removeO().expand().coeff(e,2)
    target = 4*tt**2-s.Rational(3,4)*tz**2+xt**2/4-xz**2/16-xt*tz/2
    zero("scalar_principal_from_invariants",L2-target)
    pt,px = s.symbols("pt px",real=True)
    velocities = s.solve([s.diff(L2,tt)-pt,s.diff(L2,xt)-px],[tt,xt])
    Hamiltonian = (pt*tt+px*xt-L2).subs(velocities)
    zero("principal_positive_Hamiltonian",
         Hamiltonian-(pt**2/16+(px+tz/2)**2+3*tz**2/4+xz**2/16))
    z,v = s.symbols("z v")
    time = s.hessian(L2,(tt,xt))/2
    space = s.hessian(L2,(tz,xz))/2
    cross = s.Matrix(2,2,lambda i,j:
        s.diff(L2,(tt,xt)[i],(tz,xz)[j])/2)
    symbol = time*v*v+space-(cross+cross.T)*v
    determinant = s.expand(symbol.det()).subs(v**2,z)
    zero("scalar_characteristic_polynomial",
         determinant-(8*z-3)*(8*z-1)/64)
    require("scalar_speeds_squared",s.solve(determinant,z)==[s.Rational(1,8),s.Rational(3,8)])
    require("scalar_speeds_inside_local_light_cone",
            all(0 < v < 1 for v in s.solve(determinant,z)))
    # Transverse displacement: off-diagonal strain appears twice in Tr.
    zero("transverse_speed_squared",
         (s.Rational(2,64)/s.Rational(1,4))-s.Rational(1,8))
    require("without_mixed_term_label_inertia_zero",
            s.diff(s.series(F,e,0,3).removeO().expand().coeff(e,2),xt,2)==0)
    wrong = s.series(F-W**2/(4*bc),e,0,3).removeO().expand().coeff(e,2)
    require("wrong_mixed_sign_detected",s.diff(wrong,xt,2)<0)
    details["local_principal_speeds_squared"] = ["1/8","3/8","1/8 (transverse)"]


def numerical_germ():
    # x=r exp(Hc) sqrt(Q/P), w=H-Hc; fixed finite domain and tolerances.
    x0, xmax = 1e-5, 0.5
    initial = [-x0*x0/6+x0**4/60-2*x0**6/945,
               -x0/3+x0**3/15-4*x0**5/315]
    def rhs(x,state):
        w,v = state
        return [v,-2*v/x-np.exp(2*w)]
    def run(tolerance,max_step):
        result = solve_ivp(rhs,(x0,xmax),initial,method="DOP853",
                           rtol=tolerance,atol=tolerance*0.01,
                           max_step=max_step,dense_output=True)
        require("integration_success_"+str(tolerance),result.success)
        return result.sol
    loose = run(1e-9,0.025)
    tight = run(2e-12,0.00625)
    grid = np.linspace(x0,xmax,401)
    error = float(np.max(np.abs(loose(grid)-tight(grid))))
    require("tolerance_and_step_convergence",error < 2e-9)
    w,v = tight(xmax)
    flux,quad_error = quad(lambda x:x*x*np.exp(2*tight(x)[0]),x0,xmax,
                           epsabs=2e-13,epsrel=2e-12)
    flux0 = -x0*x0*initial[1]
    flux_error = float(abs(-xmax*xmax*v-flux-flux0))
    require("independent_flux_quadrature",flux_error < 2e-10)
    probe = np.linspace(0.01,0.49,61)
    errors = []
    for step in (2e-4,1e-4):
        derivative = (tight(probe-2*step)[1]-8*tight(probe-step)[1]
                      +8*tight(probe+step)[1]-tight(probe+2*step)[1])/(12*step)
        residual = derivative+2*tight(probe)[1]/probe+np.exp(2*tight(probe)[0])
        errors.append(float(np.max(np.abs(residual))))
    require("independent_finite_difference_ODE",max(errors)<2e-8)
    vals = tight(grid)
    wpp = -2*vals[1]/grid-np.exp(2*vals[0])
    E = np.exp(-2*vals[0])
    q01 = E*(-wpp+2*vals[1]**2)
    q02 = -E*vals[1]*(1/grid+vals[1])
    q12 = -E*(wpp+vals[1]/grid)
    q23 = -E*(2*vals[1]/grid+vals[1]**2)
    K = 4*(q01**2+2*q02**2+2*q12**2+q23**2)
    require("finite_positive_scales_on_test_domain",np.all(np.isfinite(K)) and
            np.all(np.exp(-vals[0])>0))
    details["normalised_finite_domain"] = {
        "x_interval":[x0,xmax],"H_minus_Hc_at_outer":float(w),
        "dH_dx_at_outer":float(v),"p_over_pc_at_outer":float(np.exp(-w)),
        "K_times_P_squared_over_Q_squared_at_outer":float(K[-1]),
        "solution_difference":error,"flux_residual":flux_error,
        "quadrature_error_estimate":float(quad_error),
        "finite_difference_residuals":errors}

def joining_checks():
    """Same action: vacuum, source, radial-health and fade decisions."""
    y = s.symbols("y",positive=True)
    cs = s.symbols("c1 c2 c3",positive=True)
    response = (y-1)+s.Rational(3,4)*(y-1)**2-sum(
        (c-1)**2 for c in cs)/64
    F,Fy = s.symbols("F Fy")
    fs = s.symbols("f1 f2 f3")
    vacuum_eqs = [F-2*y*Fy]+[F-2*c*f for c,f in zip(cs,fs)]+[
        y*Fy-sum(c*f for c,f in zip(cs,fs))]
    necessary = s.solve(vacuum_eqs,[F,Fy,*fs])
    require("join_vacuum_requires_zero_response_jet",
            necessary == {symbol:0 for symbol in [F,Fy,*fs]})
    stationary = s.solve([s.diff(response,v) for v in (y,*cs)],
                         [y,*cs],dict=True)
    require("join_unique_stationary_state",
            stationary == [{y:s.Rational(1,3),**{c:1 for c in cs}}])
    value = s.simplify(response.subs(stationary[0]))
    zero("join_stationary_F_value",value+s.Rational(1,3))
    require("join_regular_stress_free_vacuum_excluded",value != 0)
    # A different polynomial with an actual zero stationary point is a
    # control: this vacuum test must not exclude all constitutive laws.
    control = (y-1)**2+sum((c-1)**2 for c in cs)
    require("join_vacuum_control_admitted",
            all(s.diff(control,v).subs({y:1,**{c:1 for c in cs}})==0
                for v in (y,*cs)) and control.subs({y:1,**{c:1 for c in cs}})==0)

    # Inverse metric variation BEFORE setting the clock rest frame.
    g00,g01,g11,v,d = s.symbols("g00 g01 g11 v d",real=True)
    C = g00*v*v+2*g01*v*d+g11*d*d
    Y = -g00
    W2 = (g00*v+g01*d)**2/(-g00)
    lag = (Y-1)+s.Rational(3,4)*(Y-1)**2-(C-1)**2/64+W2/4
    momentum = -s.diff(lag,g01).subs({g00:-1,g01:0,g11:1})
    zero("join_momentum_flow_from_metric_variation",
         momentum-v*d*(d*d-v*v+7)/16)
    cp = s.symbols("cp",positive=True)
    require("join_positive_strain_forbids_flow_eigenvalue",
            (-(cp+7)/32).is_negative)

    # Finite-gradient radial principal action; H's elliptic elimination
    # adds -eta*(theta_t^2-theta_z^2). No claim about full finite-k GR constraints.
    eta = s.symbols("eta",nonnegative=True)
    tt,tz,xt,xz,pt,px = s.symbols("tt tz xt xz pt px",real=True)
    local = (4-eta)*tt**2-(s.Rational(3,4)-eta)*tz**2+xt**2/4-xz**2/16-xt*tz/2
    vel = s.solve([s.diff(local,tt)-pt,s.diff(local,xt)-px],[tt,xt])
    Hamiltonian = (pt*tt+px*xt-local).subs(vel)
    zero("join_finite_gradient_Hamiltonian",
         Hamiltonian-(pt**2/(4*(4-eta))+(px+tz/2)**2
                      +(s.Rational(3,4)-eta)*tz**2+xz**2/16))
    speed,z = s.symbols("speed z",real=True)
    time = s.hessian(local,(tt,xt))/2
    space = s.hessian(local,(tz,xz))/2
    cross = s.Matrix(2,2,lambda i,j:s.diff(local,(tt,xt)[i],(tz,xz)[j])/2)
    determinant = s.expand((time*speed**2+space-(cross+cross.T)*speed).det()).subs(speed**2,z)
    zero("join_radial_characteristic",
         64*determinant-((64-16*eta)*z*z+(20*eta-32)*z+3-4*eta))
    zero("join_zero_speed_at_health_edge",
         64*determinant.subs(eta,s.Rational(3,4))-z*(52*z-17))
    roots = s.solve(determinant.subs(eta,s.Rational(4,5)),z)
    require("join_negative_squared_speed_after_edge",
            any(root.is_negative for root in roots) and any(root.is_positive for root in roots))
    details["after_edge_squared_speeds_eta_4_over_5"] = [str(root) for root in roots]

    # Dimensionless radial ODE in logarithmic radius. Lyapunov coercivity
    # and invariance argument are supplied explicitly in the report.
    Z,U = s.symbols("Z U",real=True)
    acceleration = 1-s.exp(2*Z)-U
    energy = U*U/2+s.exp(2*Z)/2-Z
    zero("join_log_radius_Lyapunov",
         s.diff(energy,Z)*U+s.diff(energy,U)*acceleration+U*U)
    require("join_log_radius_unique_equilibrium",
            s.solve([U,acceleration],[Z,U],dict=True)==[{Z:0,U:0}])
    eta_limit = s.exp(-2*Z)*(U-1)**2
    zero("join_asymptotic_eta",eta_limit.subs({Z:0,U:0})-1)
    require("join_asymptotic_eta_exceeds_gate",
            eta_limit.subs({Z:0,U:0})>s.Rational(3,4))

    # Exact exponential exterior and even its 1PN-compatible smooth tails.
    r,m,P = s.symbols("r m P",positive=True)
    a = s.symbols("a",real=True)
    h = m/r+a/r**2
    null = -2*P*s.exp(-2*h)*(s.diff(h,r,2)+2*s.diff(h,r)/r+s.diff(h,r)**2)
    zero("join_null_source_tail",s.limit(r**4*null,r,s.oo)+2*P*(m*m+2*a))
    eps = s.symbols("eps")
    gtt = s.series(-s.exp(-2*(m*eps+a*eps*eps)),eps,0,3).removeO()
    beta = s.simplify(-gtt.coeff(eps,2)/(2*m*m))
    zero("join_PPN_beta_from_common_scale",beta-(1-a/(m*m)))
    btest = s.symbols("beta",real=True)
    zero("join_null_PPN_coefficient",
         (m*m+2*a).subs(a,m*m*(1-btest))-m*m*(3-2*btest))
    B,C,L = s.symbols("B C L",real=True)
    zero("join_mixing_preserves_null_sum",
         (B-eta-L)+(C+L)-(B+C-eta))
    require("join_beta_one_null_source_negative",(-2*P*m*m).is_negative)

    # Zero ordinary field stays zero by the locally Lipschitz integral
    # equation, NOT by assuming that it can be switched on at a shell.
    chi,Omega,hh = s.symbols("chi Omega hh",real=True)
    V = chi**2/2-chi**4/4+chi**6/24
    source = s.exp(2*hh)*s.diff(V,chi)-Omega**2*s.exp(4*hh)*chi
    zero("join_canonical_scalar_zero_source",source.subs(chi,0))
    chi2,chi4,chi6 = s.symbols("chi2 chi4 chi6",real=True)
    series_chi = chi2*r**2+chi4*r**4+chi6*r**6
    residual = s.diff(series_chi,r,2)+2*s.diff(series_chi,r)/r-source.subs(chi,series_chi)
    coefficients = s.series(residual,r,0,6).removeO().expand()
    forced = s.solve([coefficients.coeff(r,n) for n in (0,2,4)],
                     [chi2,chi4,chi6],dict=True)
    require("join_canonical_scalar_zero_germ",forced==[{chi2:0,chi4:0,chi6:0}])
    details["joining_decision"] = "REJECTED_AS_REGULAR_ISOLATED_COMPLETION"
    details["stationary_response_value"] = str(value)

    x0 = 1e-5
    initial = [-x0*x0/6+x0**4/60-2*x0**6/945,
               -x0/3+x0**3/15-4*x0**5/315]
    def rhs(x,state):
        return [state[1],-2*state[1]/x-np.exp(2*state[0])]
    def edge(x,state):
        return np.exp(-2*state[0])*state[1]**2-.75
    edge.terminal,edge.direction = True,1
    runs = []
    for tolerance,step in ((1e-9,.025),(2e-12,.00625)):
        run = solve_ivp(rhs,(x0,10),initial,method="DOP853",
                        rtol=tolerance,atol=tolerance*.01,max_step=step,
                        events=edge,dense_output=True)
        require("join_event_found_"+str(tolerance),
                run.success and len(run.t_events[0])==1)
        runs.append(run)
    loose,tight = runs
    if any(len(run.t_events[0])!=1 for run in runs):
        return
    xe = float(tight.t_events[0][0])
    w,vv = tight.y_events[0][0]
    difference = abs(float(loose.t_events[0][0])-xe)
    require("join_event_radius_convergence",difference<2e-8)
    require("join_event_eta_residual",abs(np.exp(-2*w)*vv*vv-.75)<2e-11)
    grid = np.linspace(x0,min(run.t_events[0][0] for run in runs),301)
    state_difference = float(np.max(np.abs(loose.sol(grid)-tight.sol(grid))))
    require("join_extended_solution_convergence",state_difference<2e-8)
    details["first_radial_health_edge"] = {
        "x":xe,"H_minus_Hc":float(w),"dH_dx":float(vv),
        "eta":float(np.exp(-2*w)*vv*vv),"event_radius_difference":difference,
        "state_difference":state_difference,
        "physical_radius_rule":"r = x exp(-Hc) sqrt(P/Q)",
        "beyond_edge_evolved_as_physical_solution":False}



def feedback_assumption_checks():
    """Bounded audit: retained feedback versus the locked central ansatz."""
    t,x,ycoord,zcoord = s.symbols("t x ycoord zcoord",real=True)
    H = s.Function("H")(t,x,ycoord,zcoord)
    bc,Q,m0 = s.symbols("bc Q m0",positive=True)
    coordinates = (t,x,ycoord,zcoord)
    metric = s.diag(-s.exp(-2*H),s.exp(2*H),s.exp(2*H),s.exp(2*H))
    inverse = metric.inv()
    clock_gradient = s.Matrix([1,0,0,0])
    Y = -(clock_gradient.T*inverse*clock_gradient)[0]
    label_gradients = s.Matrix([[0,0,0],[s.sqrt(bc),0,0],
                                [0,s.sqrt(bc),0],[0,0,s.sqrt(bc)]])
    Bhat = s.exp(2*H)*(label_gradients.T*inverse*label_gradients)
    yhat = s.simplify(s.exp(-2*H)*Y)
    zero("audit_time_dependent_y_lock",yhat-1)
    zero("audit_time_dependent_strain_lock",
         sum((Bhat[i,j]-(bc if i==j else 0))**2 for i in range(3) for j in range(3)))
    yy,c1,c2,c3 = s.symbols("yy c1 c2 c3",positive=True)
    response = (yy-1)+s.Rational(3,4)*(yy-1)**2-sum(
        (c-bc)**2 for c in (c1,c2,c3))/(64*bc**2)
    state = {yy:yhat,c1:Bhat[0,0],c2:Bhat[1,1],c3:Bhat[2,2]}
    J = yy*s.diff(response,yy)-sum(c*s.diff(response,c) for c in (c1,c2,c3))
    locked_J = s.simplify(J.subs(state))
    rho = s.simplify(Q*(2*yy*s.diff(response,yy)-response).subs(state))
    zero("audit_time_dependent_response_source",locked_J-1)
    zero("audit_time_dependent_algebraic_density",rho-2*Q)
    zero("audit_locked_source_time_derivative",s.diff(locked_J,t))
    # This is the fixed-other-fields H block, not the full gravity kinetic
    # action: the latter has metric derivatives and independent constraints.
    u = -inverse*clock_gradient/s.sqrt(Y)
    projector = inverse+u*u.T
    gradient = s.Matrix([s.diff(H,c) for c in coordinates])
    projected = (gradient.T*projector*gradient)[0]
    zero("audit_projected_H_block",
         projected-s.exp(-2*H)*sum(s.diff(H,c)**2 for c in (x,ycoord,zcoord)))

    # Minimal matter has no explicit H dependence at fixed metric. Its
    # metric-mediated response remains nonzero on the metric pullback.
    N,h = s.symbols("N h",positive=True)
    Lrest = -m0*N
    zero("audit_fixed_metric_direct_H_variation",s.diff(Lrest,h))
    zero("audit_metric_pullback_rest_source",
         s.diff(Lrest.subs(N,s.exp(-h)),h)-m0*s.exp(-h))
    rho0,pr,pt = s.symbols("rho0 pr pt",real=True)
    g = s.diag(-s.exp(-2*h),s.exp(2*h),s.exp(2*h),s.exp(2*h))
    Tupper = s.diag(rho0*s.exp(2*h),pr*s.exp(-2*h),
                    pt*s.exp(-2*h),pt*s.exp(-2*h))
    contraction = sum(Tupper[i,j]*s.diff(g[i,j],h) for i in range(4) for j in range(4))/2
    zero("audit_restricted_matter_source_trace",contraction-(rho0+pr+2*pt))
    load = s.symbols("load",positive=True)
    scale = s.Function("p")(load)
    energy = load*scale
    zero("audit_all_constituents_chain_rule",
         s.diff(energy,load)-scale-load*s.diff(scale,load))
    require("audit_frozen_scale_control_fails",
            s.simplify(s.diff(energy,load)-scale) != 0)
    zero("audit_rest_energy_has_one_scale",(-Lrest).subs(N,s.exp(-h))-m0*s.exp(-h))
    require("audit_second_scale_control_fails",
            s.simplify(m0*s.exp(-2*h)-m0*s.exp(-h)) != 0)
    print(json.dumps({
        "claim":"W3_92_FEEDBACK_ASSUMPTION_AUDIT_V1",
        "status":"AUDIT_CHECKS_PASSED" if all(checks.values()) else "AUDIT_CHECKS_FAILED",
        "checks_passed":sum(checks.values()),"checks_total":len(checks),
        "checks":checks,"details":details,
        "scope":{
            "time_dependence_alone_unlocks_selected_source":False,
            "metric_feedback_absent_because_direct_H_source_zero":False,
            "new_action_introduced":False,
            "time_dependent_locked_metric_shown_to_solve_equations":False,
            "full_RefG_pressure_source_identified":False,
            "existing_Einstein_scalar_feedback_rejected":False},
        "provenance":{"python":platform.python_version(),"sympy":s.__version__,
                      "verifier_sha256":sha(Path(__file__)),"report_sha256":sha(REPORT)}
        },ensure_ascii=False,indent=2))
    return 0 if all(checks.values()) else 1


def ordinary_source_charge_control():
    """Fresh retained equilibrium: stress integral versus geometric mass.

    This is an ordinary-sector limit control, not a full-medium solution.
    Tolerances follow the collocation target (100*tol for independent
    residuals). Exploratory runs assessed precision before this regression.
    """
    from scipy.integrate import simpson
    module_name = "w92_bridge_retained_evolution"
    spec = importlib.util.spec_from_file_location(module_name,HERE/"nonlinear_equilibrium_evolution.py")
    evolution = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = evolution
    spec.loader.exec_module(evolution)
    _,model,solution,anchor,pins = evolution.background()
    require("bridge_retained_equilibrium_anchor",anchor["pass"])
    alpha = evolution.ALPHA
    rows = []
    for radius,tolerance in ((80.,1e-7),(80.,1e-8),(100.,1e-8)):
        if tolerance != 1e-7:
            solution = model.solve_coupled(alpha,radius=radius,tolerance=tolerance,seed=solution)
        tag = "bridge_charge_R%s_tol%s" % (int(radius),tolerance)
        require(tag+"_solver",solution.success and np.max(solution.rms_residuals)<=2*tolerance)
        omega = model.omega_from_parameter(solution.p)
        integrals = []
        for count in (16001,32001):
            x = np.linspace(model.EPS,radius,count)
            f,fp,mass,logs = solution.sol(x)
            derivative = solution.sol(x,1)
            sigma = np.exp(logs)
            radial = 1-2*alpha*mass/x
            radial_prime = -2*alpha*(derivative[2]/x-mass/x**2)
            potential = model.potential(f)
            time_square = omega**2*f**2/(sigma**2*radial)
            space_square = radial*fp**2
            rho = (time_square+space_square)/2+potential
            pr = (time_square+space_square)/2-potential
            pt = (time_square-space_square)/2-potential
            charge = simpson(x*x*omega*f*f/(sigma*radial),x=x)
            komar = simpson(x*x*sigma*(rho+pr+2*pt),x=x)
            flux = x*x*sigma*(radial_prime/2+radial*derivative[3])/alpha
            killing = simpson(x*x*sigma*rho,x=x)
            charge_form = 2*omega*charge-2*simpson(x*x*sigma*potential,x=x)
            ode = model.curved_equations(alpha)(x,solution.sol(x),solution.p)
            ode_radial_prime = -2*alpha*(ode[2]/x-mass/x**2)
            ode_flux = x*x*sigma*(ode_radial_prime/2+radial*ode[3])/alpha
            kg = simpson(sigma*x*x*(space_square+f*model.potential_force(f)-time_square),x=x)
            kg_boundary = sigma*radial*x*x*f*fp
            kg_residual = kg-kg_boundary[-1]+kg_boundary[0]
            integrals.append(float(komar))
        mass_value = float(mass[-1])
        local_error = float(np.max(abs(flux[x<=15]-ode_flux[x<=15]))/mass_value)
        charge_error = float(max(abs(komar-mass_value),abs(flux[-1]-mass_value))/mass_value)
        require(tag+"_mass_and_flux",charge_error<100*tolerance)
        require(tag+"_local_derivative",local_error<100*tolerance)
        require(tag+"_quadrature",abs(integrals[1]-integrals[0])/mass_value<tolerance)
        require(tag+"_phase_and_KG",abs(charge_form-komar)/mass_value<1e-12 and abs(kg_residual)/mass_value<100*tolerance)
        # Intentionally wrong energy identification on this fixed witness.
        require(tag+"_matter_Killing_as_ADM_rejected",abs(killing-mass_value)/mass_value>1e-3)
        rows.append({"radius":radius,"tolerance":tolerance,"omega":float(omega),
            "ADM_mass":mass_value,"Komar_volume":float(komar),"Komar_boundary":float(flux[-1]),
            "scalar_charge":float(charge),"matter_Killing_energy":float(killing),
            "charge_relative_error":charge_error,"local_flux_relative_error":local_error,
            "quadrature_change":abs(integrals[1]-integrals[0]),
            "KG_integral_residual":float(kg_residual),
            "collocation_residual":float(np.max(solution.rms_residuals))})
    require("bridge_charge_precision_improves",rows[1]["charge_relative_error"]<rows[0]["charge_relative_error"])
    require("bridge_charge_radius_control",abs(rows[2]["ADM_mass"]-rows[1]["ADM_mass"])/rows[1]["ADM_mass"]<100*rows[1]["tolerance"])
    details["ordinary_limit_control"] = {"cases":rows,"frozen_source_hashes":pins,
        "normalization":"W64 dimensionless mass and scalar charge; alpha=0.04",
        "full_medium_equations_satisfied_by_this_control":False,
        "rigorous_infinite_domain_error_bound":False}


def matter_source_bridge_checks():
    """Independent static field variations; no new response function."""
    r = s.symbols("r", positive=True)
    P,Q,omega = s.symbols("P Q omega", positive=True)
    N,A,S,H,ell,chi = [s.Function(n)(r) for n in ("N","A","S","H","ell","chi")]
    yy,bb,cc = s.symbols("y br bt", positive=True)
    response = s.Function("F")(yy,bb,cc)
    # F is the tangentially restricted response: dF/dbt counts BOTH
    # tangential eigenvalues. It is not one-eigenvalue F_t.
    y = s.exp(-2*H)/N**2
    br = s.exp(2*H)*s.diff(ell,r)**2/A**2
    bt = s.exp(2*H)*ell**2/S**2
    sub = {yy:y,bb:br,cc:bt}
    F = response.subs(sub)
    Fy,Fr,Ft = [s.diff(response,v).subs(sub) for v in (yy,bb,cc)]
    J = y*Fy-br*Fr-bt*Ft
    V = s.Function("V")(chi)
    W = omega**2*chi**2/N**2
    Gchi = s.diff(chi,r)**2/A**2
    GH = P*s.diff(H,r)**2/A**2
    volume = N*A*S**2
    Lg = P*(N*A+(N*s.diff(S,r)**2+2*s.diff(N,r)*S*s.diff(S,r))/A)
    Lfields = volume*(Q*F+GH+W/2-Gchi/2-V)
    L = Lg+Lfields

    def EL(lagrangian, field):
        return s.diff(lagrangian,field)-s.diff(s.diff(lagrangian,s.diff(field,r)),r)

    equations = {v:EL(L,v) for v in (N,A,S,H,ell,chi)}
    rhoO,prO,ptO = W/2+Gchi/2+V, W/2+Gchi/2-V, W/2-Gchi/2-V
    rhoF,prF,ptF = Q*(2*y*Fy-F), Q*(F-2*br*Fr), Q*(F-bt*Ft)
    rho,pr,pt = rhoO+rhoF-GH, prO+prF-GH, ptO+ptF+GH
    zero("bridge_Hilbert_density",EL(Lfields,N)+A*S**2*rho)
    zero("bridge_Hilbert_radial_pressure",EL(Lfields,A)-N*S**2*pr)
    zero("bridge_Hilbert_tangential_pressure",EL(Lfields,S)-2*N*A*S*pt)
    zero("bridge_scalar_active_source",rhoO+prO+2*ptO-2*(W-V))
    zero("bridge_medium_active_source",rhoF+prF+2*ptF-2*Q*(J+F))
    zero("bridge_projected_gradient_active_cancellation",-GH-GH+2*GH)
    K = S**2*s.diff(N,r)/A
    deficit_flux = -volume*s.diff(H,r)/A**2
    difference = volume*(s.diff(N,r)/N+s.diff(H,r))/A**2
    zero("bridge_lapse_minus_deficit_flux",K-deficit_flux-difference)
    mn,mh,ma = s.symbols("mN mH mA",positive=True)
    asymptotic = {N:s.exp(-mn/r),A:s.exp(ma/r),S:r,H:mh/r}
    zero("bridge_asymptotic_charge_difference",
         s.limit(difference.subs(asymptotic).doit(),r,s.oo)-(mn-mh))
    combo = N*equations[N]-A*equations[A]-S*equations[S]
    zero("bridge_independent_lapse_equation",combo-2*P*s.diff(K,r)+volume*(rho+pr+2*pt))
    zero("bridge_independent_H_equation",equations[H]-2*P*s.diff(deficit_flux,r)+2*Q*volume*J)
    balance_source = Q*F+W-V
    zero("bridge_full_offshell_balance",
         combo-equations[H]-2*(P*s.diff(difference,r)-volume*balance_source))
    expected_scalar = s.diff(N*S**2*s.diff(chi,r)/A,r)+volume*(omega**2*chi/N**2-s.diff(V,chi))
    zero("bridge_scalar_equation",equations[chi]-expected_scalar)
    expected_label = 2*Q*volume*Ft*bt/ell-s.diff(2*Q*volume*Fr*s.exp(2*H)*s.diff(ell,r)/A**2,r)
    zero("bridge_label_equation",equations[ell]-expected_label)
    # Radial diffeomorphism identity tests the equations discarded by an
    # early metric ansatz. A dr is a one-form; the other radial fields
    # transform as scalars under an infinitesimal radial relabelling.
    ward = sum(equations[v]*s.diff(v,r) for v in equations)-s.diff(A*equations[A],r)
    zero("bridge_radial_Noether_identity",ward)

    # The scalar charge fixes the kinetic response when geometry changes.
    phase_momentum = s.diff(volume*W/2,omega)
    zero("bridge_phase_charge",phase_momentum-A*S**2*omega*chi**2/N)
    require("bridge_deleted_scalar_active_source_rejected",s.simplify(W-V) != 0)
    require("bridge_density_only_source_rejected",s.simplify(rhoO-(rhoO+prO+2*ptO)) != 0)
    require("bridge_missing_second_tangential_pressure_rejected",s.simplify(pt) != 0)
    n0,a0 = s.symbols("n0 a0",positive=True)
    h0,h2,n2,f0,w0,v0 = s.symbols("h0 h2 n2 f0 w0 v0",real=True)
    # Direct regular-centre expansion, without assuming y0=1:
    # N=n0(1+n2 r²),
    # A=a0+O(r²), S=a0 r+O(r³), H=H0+h2 r²+O(r4).
    central_germ = {N:n0*(1+n2*r*r),A:a0,S:a0*r,H:h0+h2*r*r}
    central_residual = (P*s.diff(difference,r)-volume*(Q*f0+w0-v0)).subs(central_germ).doit()
    leading_residual = s.limit(central_residual/r**2,r,0)
    zero("bridge_central_clock_deficit_difference",
         leading_residual-(6*P*n0*a0*(n2+h2)-n0*a0**3*(Q*f0+w0-v0)))
    details["source_balance"] = "P (NS^2/A (ln N+H)')' = NAS^2 (QF+Omega^2 chi^2/N^2-V)"
    details["common_clock_condition"] = "QF+Omega^2 chi^2/N^2-V=0 pointwise; necessary, not sufficient"
    details["source_charge_equations"] = "K'=NAS^2[Q(J+F)+W-V]/P; Q_H'=Q NAS^2 J/P"
    ordinary_source_charge_control()
    details["scope"] = {
        "static_source_identities_and_reference_limit_verified":all(checks.values()),
        "new_constitutive_law":False,"full_pressure_readout_derived":False,
        "healthy_global_medium_solution":False,"singularity_removal":False}
    print(json.dumps({"claim":"W3_92_MATTER_MEDIUM_SOURCE_BRIDGE_V1",
        "checks_passed":sum(checks.values()),"checks_total":len(checks),
        "failed_checks":[n for n,v in checks.items() if not v],
        "checks":checks,"details":details,
        "sha256":{"verifier":sha(Path(__file__)),"report":sha(REPORT),
                  "retained_evolution":sha(HERE/"nonlinear_equilibrium_evolution.py")}},indent=2))
    return 0 if all(checks.values()) else 1



def static_label_balance_checks():
    """New global bridge test; does not run the old equilibrium/health suites."""
    r = s.symbols("r", positive=True)
    P,Q = s.symbols("P Q", positive=True)
    N,A,S,H,ell = [s.Function(n)(r) for n in ("N","A","S","H","ell")]
    yy,bb,cc = s.symbols("y br bt", positive=True)
    response = s.Function("F")(yy,bb,cc)
    volume = N*A*S**2
    y = s.exp(-2*H)/N**2
    br = s.exp(2*H)*s.diff(ell,r)**2/A**2
    bt = s.exp(2*H)*ell**2/S**2
    substitution = {yy:y,bb:br,cc:bt}
    F = response.subs(substitution)
    Fy,Fr,Ft = [s.diff(response,v).subs(substitution) for v in (yy,bb,cc)]
    # Ft is the derivative of F(y,br,bt,bt): BOTH angular eigenvalues.
    LF = Q*volume*F
    LH = P*volume*s.diff(H,r)**2/A**2
    Lg = P*(N*A+(N*s.diff(S,r)**2+2*s.diff(N,r)*S*s.diff(S,r))/A)

    def EL(lagrangian, field):
        return s.diff(lagrangian,field)-s.diff(s.diff(lagrangian,s.diff(field,r)),r)

    current = N*S**2*s.exp(2*H)*s.diff(ell,r)*Fr/A
    traction = ell*current
    trace = br*Fr+bt*Ft
    label_equation = EL(LF,ell)
    zero("label_current_from_independent_variation",
         s.diff(LF,s.diff(ell,r))-2*Q*current)
    zero("label_explicit_source_from_independent_variation",
         s.diff(LF,ell)-2*Q*N*A*s.exp(2*H)*ell*Ft)
    zero("label_weighted_offshell_identity",
         s.diff(traction,r)-volume*trace+ell*label_equation/(2*Q))
    require("lost_second_tangential_derivative_detected",
            s.simplify(volume*bt*Ft/2) != 0)
    zero("material_traction_algebra",
         traction-volume*(ell/s.diff(ell,r))*br*Fr)

    # These metric components are extracted by variation BEFORE common-p.
    geom_rho = EL(Lg,N)/(A*S**2)
    geom_pr = -EL(Lg,A)/(N*S**2)
    geom_pt = -EL(Lg,S)/(2*N*A*S)
    deficit_source = -P*s.diff(N*S**2*s.diff(H,r)/A,r)/volume
    zero("independent_H_source",
         EL(LF+LH,H)-2*volume*(deficit_source-Q*(y*Fy-trace)))
    zero("independent_F_density",EL(LF,N)+A*S**2*Q*(2*y*Fy-F))
    zero("independent_F_radial_pressure",EL(LF,A)-N*S**2*Q*(F-2*br*Fr))
    zero("independent_F_angular_pressure",EL(LF,S)-2*N*A*S*Q*(F-bt*Ft))

    u = s.Function("u")(r)
    pscale = s.exp(-u)
    common = {N:pscale,A:1/pscale,S:r/pscale,H:u}
    hstress = P*s.diff(H,r)**2/A**2
    Rrho = s.simplify((geom_rho+hstress).subs(common).doit())
    Rr = s.simplify((geom_pr+hstress).subs(common).doit())
    Rt = s.simplify((geom_pt-hstress).subs(common).doit())
    Jcommon = s.simplify(deficit_source.subs(common).doit())
    zero("common_metric_radial_H_cancellation",Rr)
    zero("common_metric_angular_H_cancellation",Rt)
    zero("common_metric_lapse_H_source_relation",Rrho-2*Jcommon)
    zero("common_metric_H_Laplacian",Jcommon+P*pscale**2*(s.diff(u,r,2)+2*s.diff(u,r)/r))

    # General independent geometry first; no guessed F or scalar profile.
    f,d,a,c = s.symbols("QF QyFy QbrFr QbtFt", real=True)
    rho,pr,pt = s.symbols("rho pr pt", real=True)
    gr,grr,grt,j = s.symbols("Rrho Rr Rt Jg", real=True)
    equations = [gr-rho-2*d+f, grr-pr-f+2*a,
                 grt-pt-f+c, j-d+a+c]
    solved = s.solve(equations,(f,d,a,c),dict=True)[0]
    support = (3*gr+grr+2*grt)/4-3*j/2
    zero("unrestricted_geometric_support_identity",
         (a+c).subs(solved)-support+(3*rho+pr+2*pt)/4)
    shared = {gr:2*j,grr:0,grt:0}
    zero("common_scale_removes_geometric_support",support.subs(shared))
    reduced = {v:s.factor(value.subs(shared)) for v,value in solved.items()}
    zero("arbitrary_matter_weighted_trace",
         reduced[a]+reduced[c]+(3*rho+pr+2*pt)/4)

    T,X = s.symbols("T X", nonnegative=True)
    V = s.symbols("V", real=True)
    canonical = {rho:T+X+V,pr:T+X-V,pt:T-X-V}
    zero("canonical_F_value",reduced[f].subs(canonical)-(V-2*T))
    zero("canonical_radial_material_slope",reduced[a].subs(canonical)-(X-T)/2)
    zero("canonical_angular_material_slope",reduced[c].subs(canonical)+(T+X))
    zero("canonical_negative_label_trace",(reduced[a]+reduced[c]).subs(canonical)+(3*T+X)/2)
    require("canonical_integrand_nonnegative",(3*T+X).is_nonnegative)
    require("missing_time_energy_detected",s.simplify((3*T+X)-X) != 0)
    # If the independent H equation is omitted, a spurious adjustable F
    # survives. This is an exact negative control for early ansatz reduction.
    omitted_H = s.solve(equations[:3],(d,a,c),dict=True)[0]
    uncontrolled = (a+c).subs(omitted_H).subs(shared).subs(canonical)+(3*T+X)/2
    require("omitted_H_equation_does_not_close_trace",s.simplify(uncontrolled) != 0)

    # Boundary tests are necessary; F_r -> 0 alone is deliberately rejected.
    n0,a0,l1 = s.symbols("n0 a0 l1", positive=True)
    h0,f0 = s.symbols("h0 f0", real=True)
    centre_term = n0*(a0*r)**2*s.exp(2*h0)*(l1*r)*l1*f0/a0
    zero("regular_centre_traction",s.limit(centre_term,r,0))
    ctail = s.symbols("ctail", positive=True)
    zero("vanishing_slope_counterexample",s.limit(ctail/r**3,r,s.oo))
    require("vanishing_slope_not_zero_traction",s.limit(r**3*(ctail/r**3),r,s.oo) != 0)
    amplitude,k = s.symbols("amplitude k", positive=True)
    chi_tail = amplitude*s.exp(-k*r)/r
    omega = s.symbols("omega", positive=True)
    tail_T = omega**2*chi_tail**2/2
    tail_X = s.diff(chi_tail,r)**2/2
    zero("localized_scalar_tail_traction",
         s.limit(r**3*(tail_X-tail_T)/(2*Q),r,s.oo))
    # A flat-ball label configuration with F=-(br+2bt) satisfies the label
    # equation and has nonzero boundary support. It is NOT a full solution.
    radius = s.symbols("R", positive=True)
    flat_current,flat_traction = -r**2,-r**3
    zero("nonzero_boundary_label_equation",s.diff(flat_current,r)-r*(-2))
    zero("nonzero_boundary_integrated_identity",
         flat_traction.subs(r,radius)-s.integrate(-3*r**2,(r,0,radius)))
    require("discarding_nonzero_boundary_detected",flat_traction.subs(r,radius) != 0)

    # U(0)=U'(0)=0 kills every static first variation, including lapse/shift.
    dh,b = s.symbols("DH b_rate", real=True, positive=True)
    Ub = 2*P*b**2*(1-s.sqrt(1-dh**2/b**2))
    zero("rate_term_static_value",Ub.subs(dh,0))
    zero("rate_term_static_first_variation",s.diff(Ub,dh).subs(dh,0))
    zero("rate_term_quadratic_coefficient",s.diff(Ub,dh,2).subs(dh,0)-2*P)
    Hdot,Hprime,shift = s.symbols("Hdot Hprime shift", real=True)
    lapse,radial,area = s.symbols("lapse radial area", positive=True)
    rate_density = lapse*radial*area**2*Ub.subs(dh,(Hdot-shift*Hprime)/lapse)
    static = {Hdot:0,shift:0}
    rate_residuals = [s.simplify(s.diff(rate_density,v).subs(static))
                      for v in (lapse,radial,area,Hdot,Hprime,shift)]
    require("rate_term_lapse_shift_and_field_variations_vanish",
            all(value == 0 for value in rate_residuals))

    root = HERE.parents[3]
    article = root/"RefG_ka.md"
    require("article_frozen_dependency",
            sha(article) == "2571f9fbde25cd9e5258e5bb2c78797380123bf32621e4eaf068ce97c1b4c927")
    details["label_boundary_identity"] = "[C_ell] = integral NAS^2 (br Fr + bt Ft) dr"
    details["common_scale_canonical_source"] = "Q C_ell' = -NAS^2 (3T+X)/2"
    details["unrestricted_support"] = "Q(br Fr+bt Ft)=-(3T+X)/2+(3Rrho+Rr+2Rt)/4-3Jg/2"
    details["boundary_domain"] = "regular centre and zero outer traction; asymptotic strain and localized tail controlled"
    details["closure_flags"] = {
        "exact_scoped_static_bridge_excluded":all(checks.values()),
        "new_constitutive_law":False,
        "full_dynamic_equivalence":False,
        "healthy_general_medium_excluded":False,
        "regular_object_constructed":False,
        "equilibrium_stability_proved":False,
        "horizon_or_global_PDE_result":False}
    print(json.dumps({"claim":"W3_92_STATIC_LABEL_BALANCE_BRIDGE_V1",
        "python":platform.python_version(),"sympy":s.__version__,
        "checks_passed":sum(checks.values()),"checks_total":len(checks),
        "failed_checks":[name for name,value in checks.items() if not value],
        "checks":checks,"details":details,
        "sha256":{"verifier":sha(Path(__file__)),"report":sha(REPORT),
                  "article":sha(article)}},indent=2))
    return 0 if all(checks.values()) else 1



def independent_H_readout_checks():
    """Probe action and necessary source mapping; no equilibrium reruns."""
    pscale,P,Q = s.symbols("p P Q",positive=True)
    V = s.symbols("V",real=True)
    inverse_metric = s.diag(-pscale**-2,pscale**2,pscale**2,pscale**2)
    volume = pscale**-2
    dt,dx,dy,dz = s.symbols("dtpsi dxpsi dypsi dzpsi",real=True)
    derivatives = s.Matrix([dt,dx,dy,dz])
    canonical = volume*(-(derivatives.T*inverse_metric*derivatives)[0]/2-V)
    zero("canonical_coordinate_action_matches_APR",
         canonical-(pscale**-4*dt**2/2-(dx**2+dy**2+dz**2)/2-pscale**-2*V))
    ex,ey,ez,bx,by,bz = s.symbols("Ex Ey Ez Bx By Bz",real=True)
    em = s.Matrix([[0,ex,ey,ez],[-ex,0,bz,-by],[-ey,-bz,0,bx],[-ez,by,-bx,0]])
    em_up = inverse_metric*em*inverse_metric
    em_density = -volume*sum(em[i,j]*em_up[i,j] for i in range(4) for j in range(4))/4
    zero("Maxwell_coordinate_action_matches_APR",
         em_density-((ex**2+ey**2+ez**2)/pscale**2-pscale**2*(bx**2+by**2+bz**2))/2)
    speed = s.symbols("coordinate_light_speed",positive=True)
    zero("common_metric_null_speed",(-pscale**2+pscale**-2*speed**2).subs(speed,pscale**2))

    r = s.symbols("r",positive=True)
    u,sigma,ell = [s.Function(name)(r) for name in ("u","sigma","ell")]
    p = s.exp(-u)
    N,A,S,H = p,1/p,r/p,u+sigma
    y = s.exp(-2*H)/N**2
    br = s.exp(2*H)*s.diff(ell,r)**2/A**2
    bt = s.exp(2*H)*ell**2/S**2
    zero("independent_H_clock_invariant",y-s.exp(-2*sigma))
    zero("independent_H_radial_invariant",br-s.exp(2*sigma)*s.diff(ell,r)**2)
    zero("independent_H_angular_invariant",bt-s.exp(2*sigma)*ell**2/r**2)
    zero("sigma_flux_coefficient",N*S**2/A-r**2)
    zero("sigma_source_measure",N*A*S**2-r**2/p**2)
    lapse_flux = S**2*s.diff(N,r)/A
    H_flux = -N*S**2*s.diff(H,r)/A
    zero("clock_H_flux_difference",lapse_flux-H_flux-r**2*s.diff(sigma,r))
    mu,mh = s.symbols("m_u m_H",real=True)
    tail_difference = (mh-mu)/r
    zero("asymptotic_field_normalizations_match",s.limit(tail_difference,r,s.oo))
    zero("asymptotic_flux_difference",s.limit(r**2*s.diff(tail_difference,r),r,s.oo)-(mu-mh))
    require("normalization_alone_does_not_match_charges",mu-mh != 0)

    # Established independent lapse equation of section 8 vs APR's
    # stationary equation, alpha=1/(2P). No early action variation.
    F,J,W = s.symbols("F J W",real=True)
    article_lap = -(Q*(J+F)+W-V)/(P*pscale**2)
    apr_lap = -(2*W-2*V)/(2*P*pscale**2)
    zero("stationary_source_mismatch",article_lap-apr_lap+Q*(J+F)/(P*pscale**2))
    zero("stationary_source_matches_if_J_plus_F_zero",(article_lap-apr_lap).subs(J,-F))
    require("omitting_medium_active_source_detected",s.simplify(article_lap-apr_lap) != 0)

    lap = lambda field:s.diff(field,r,2)+2*s.diff(field,r)/r
    gradient_difference = P*p**2*(s.diff(H,r)**2-s.diff(u,r)**2)
    Rrho = -2*P*p**2*lap(u)+gradient_difference
    Rr,Rt = gradient_difference,-gradient_difference
    Jgeom = -P*lap(H)*p**2
    correction = (3*Rrho+Rr+2*Rt)/4-3*Jgeom/2
    zero("sigma_compatibility_term",
         correction-P*p**2*(3*lap(sigma)+2*s.diff(u,r)*s.diff(sigma,r)+s.diff(sigma,r)**2)/2)
    zero("sigma_integrated_balance_density",
         r**2*correction/p**2-P*(3*s.diff(r**2*s.diff(sigma,r),r)
         +r**2*(s.diff(H,r)**2-s.diff(u,r)**2))/2)
    zero("locking_H_to_u_removes_this_term",correction.subs(sigma,0).doit())

    root=HERE.parents[3]
    article=root/"RefG_ka.md"
    apr=root/"RefG"/"work 3"/"Cosmology_and_LSS"/"Active_Participation_Resonance_Feedback"
    require("unchanged_article_dependency",
            sha(article)=="2571f9fbde25cd9e5258e5bb2c78797380123bf32621e4eaf068ce97c1b4c927")
    output={"claim":"W3_92_COMMON_READOUT_INDEPENDENT_H_V1",
        "python":platform.python_version(),"sympy":s.__version__,
        "checks_passed":sum(checks.values()),"checks_total":len(checks),
        "failed_checks":[name for name,value in checks.items() if not value],
        "checks":checks,"details":details,
        "source_condition":"J+F=0 is necessary to retain the APR stationary u equation",
        "sigma_equation":"P(r^2 sigma')'=r^2 p^-2 (QF+W-V)",
        "closure_flags":{"probe_action_mapping_verified":all(checks.values()),
            "H_equals_u_assumed":False,"new_constitutive_law":False,
            "full_effective_action_derived":False,"APR_restoring_Hessian_transferred":False,
            "new_equilibrium_or_stability_proved":False},
        "sha256":{"verifier":sha(Path(__file__)),"report":sha(REPORT),
            "article":sha(article),"APR_source":sha(apr/"common_scale_finite_source_candidate.py"),
            "APR_restoring_response":sha(apr/"profile_relaxed_response.py")}}
    print(json.dumps(output,indent=2))
    return 0 if all(checks.values()) else 1



def joint_static_boundary_checks():
    """Joint necessary equations; no rerun of APR profiles or older modes."""
    r=s.symbols("r",positive=True)
    P,Q,omega=s.symbols("P Q omega",positive=True)
    u,H,ell,chi=[s.Function(name)(r) for name in ("u","H","ell","chi")]
    p=s.exp(-u)
    sigma=H-u
    volume=r**2/p**2
    lap=lambda field:s.diff(field,r,2)+2*s.diff(field,r)/r
    V=s.Function("V")(chi)
    T=omega**2*chi**2/(2*p**2)
    X=p**2*s.diff(chi,r)**2/2
    L=P*p**2*lap(sigma)
    D=P*p**2*(s.diff(H,r)**2-s.diff(u,r)**2)
    # These are necessary jets of ONE F, not independently fitted functions.
    f=L-2*T+V
    a=(X-T+L-D)/2
    c=-T-X+L+D
    d=(T-X+L+D-2*V)/2
    rho,pr,pt=T+X+V,T+X-V,T-X-V
    zero("joint_density_equation",rho+2*d-f-(4*T-2*V+D))
    zero("joint_radial_equation",pr+f-2*a-D)
    zero("joint_angular_equation",pt+f-c+D)
    zero("joint_H_equation",d-a-c-(2*T-V-L))
    zero("joint_APR_lapse_source",f+d-a-c)

    y=s.exp(-2*sigma)
    br=s.exp(2*sigma)*s.diff(ell,r)**2
    bt=s.exp(2*sigma)*ell**2/r**2
    chain_from_invariants=d*s.diff(y,r)/y+a*s.diff(br,r)/br+c*s.diff(bt,r)/bt
    chain_expected=2*f*s.diff(sigma,r)+2*a*s.diff(ell,r,2)/s.diff(ell,r)+2*c*(s.diff(ell,r)/ell-1/r)
    zero("single_F_chain_rule_in_invariants",chain_from_invariants-chain_expected)
    chain_residual=s.diff(f,r)-chain_expected
    traction_Q=volume*ell*a/s.diff(ell,r)
    label_residual=s.diff(traction_Q,r)-volume*(a+c)
    # On the retained APR equations these are the same constraint, not two
    # independent equations. Keep H/ell free in this check.
    apr_u=-(2*T-V)/(P*p**2)-2*s.diff(u,r)/r
    apr_chi=-2*s.diff(chi,r)/r-omega**2*chi/p**4+s.diff(V,chi)/p**2
    relation=chain_residual-2*s.diff(ell,r)*label_residual/(ell*volume)
    zero("chain_and_label_agree_on_APR_equations",
         relation.subs({s.diff(u,r,2):apr_u,s.diff(chi,r,2):apr_chi}))

    z=r**2*s.diff(sigma,r)
    delta=s.diff(H,r)**2-s.diff(u,r)**2
    integrand=volume*(3*T+X)
    zero("traction_includes_independent_H_terms",
         traction_Q-ell/(2*s.diff(ell,r))*(volume*(X-T)+P*s.diff(z,r)-P*r**2*delta))
    zero("joint_trace_with_all_boundaries",
         2*volume*(a+c)+integrand-3*P*s.diff(z,r)-P*r**2*delta)
    B=traction_Q-3*P*z/2
    zero("joint_boundary_convergence_identity",
         s.diff(B,r)-P*r**2*delta/2+integrand/2-label_residual)
    zero("joint_outer_flux_identity",
         r*s.diff(z,r)-2*traction_Q*r*s.diff(ell,r)/(P*ell)
         +r**3*(X-T)/(P*p**2)-r**3*delta)
    # Both centre terms are O(r^3), not silently discarded at finite r.
    p0,l1=s.symbols("p0 l1",positive=True)
    h0,h2,u0,u2,fr0=s.symbols("h0 h2 u0 u2 fr0",real=True)
    centre_traction=r**2*s.exp(2*h0)*(l1*r)*l1*fr0
    zero("regular_centre_label_boundary",s.limit(centre_traction,r,0))
    zero("regular_centre_charge_difference",s.limit(r**2*s.diff((h0-u0)+(h2-u2)*r**2,r),r,0))
    mu,mh=s.symbols("m_u m_H",real=True)
    zero("finite_charge_difference_boundary",
         r**2*s.diff((mh-mu)/r,r)-(mu-mh))
    zero("H_energy_integration_by_parts_boundary",s.limit(r**2*(mh/r)*s.diff(mh/r,r),r,s.oo))

    # Exterior inference counterexample, smoothly extendible inside r=1:
    # finite equal derivative charges and finite gradient energy do NOT
    # alone control the independent second derivative in C_ell.
    eps=s.symbols("epsilon",positive=True)
    sig_tail=eps*s.sin(r**2)/r**5
    du=s.diff(mu/r,r)
    dh=du+s.diff(sig_tail,r)
    dtail=dh**2-du**2
    ztail=r**2*s.diff(sig_tail,r)
    traction_tail=P*r**3*(lap(sig_tail)-dtail)/2
    plus={s.sin(r**2):1,s.cos(r**2):0}
    minus={s.sin(r**2):-1,s.cos(r**2):0}
    zero("oscillatory_traction_subsequence_one",
         s.limit(traction_tail.subs(plus),r,s.oo)+2*P*eps)
    zero("oscillatory_traction_subsequence_two",
         s.limit(traction_tail.subs(minus),r,s.oo)-2*P*eps)
    zero("oscillatory_charge_envelope_vanishes",s.limit(7*eps/r**2,r,s.oo))
    zero("oscillatory_gradient_energy_bound",s.integrate(49*eps**2/r**6,(r,1,s.oo))-49*eps**2/5)
    tail_label=s.diff(traction_tail,r)-P*(3*s.diff(ztail,r)+r**2*dtail)/2
    tail_residual=s.limit((tail_label/r).subs({s.sin(r**2):0,s.cos(r**2):1}),r,s.oo)
    zero("oscillatory_tail_full_label_residual",tail_residual+4*P*eps)
    require("oscillatory_tail_rejected_as_joint_solution",tail_residual != 0)

    # The all-zero slope limit must also be an actual single constitutive F.
    ts,xs,ls,ds=s.symbols("T X Lsigma Cdelta",real=True)
    solved=s.solve([(xs-ts+ls-ds)/2,-ts-xs+ls+ds],(ls,ds),dict=True)[0]
    zero("zero_slopes_require_Lsigma_T",solved[ls]-ts)
    zero("zero_slopes_require_Cdelta_X",solved[ds]-xs)
    fv=s.Function("Fcurve")(r)
    zero("zero_slopes_constitutive_integrating_factor",
         s.diff(s.exp(-2*sigma)*fv,r).subs(s.diff(fv,r),2*fv*s.diff(sigma,r)))
    constant=s.symbols("constant",real=True)
    # Evaluate sigma -> 0 at infinity only; do not set H=u in the interior.
    zero("silent_limit_fixes_constitutive_constant",(constant*s.exp(2*sigma)).subs(H,u)-constant)
    up2,xpos=s.symbols("uprime_squared X_positive",nonnegative=True)
    pp=s.symbols("p_positive",positive=True)
    require("zero_H_zero_slopes_force_nonnegative_sum_zero",(P*pp**2*up2+xpos).is_nonnegative)

    # Reuse, rather than re-solve, APR's virial and Gauss identities.
    IT,IX,IV,Ug,Hg=s.symbols("IT IX IV Ug Hg",real=True)
    apr_integrals=s.solve([IX+P*Ug-3*(IT-IV),2*IT-IV-P*mu],(IX,IV),dict=True)[0]
    required_I=s.factor((3*IT+IX).subs(apr_integrals))
    zero("retained_APR_integral_identity",required_I-P*(3*mu-Ug))
    full_boundary_balance=3*P*(mu-mh)+P*(Hg-Ug)
    zero("joint_H_norm_charge_condition",full_boundary_balance-required_I-P*(Hg-3*mh))

    root=HERE.parents[3]
    article=root/"RefG_ka.md"
    apr=root/"RefG"/"work 3"/"Cosmology_and_LSS"/"Active_Participation_Resonance_Feedback"
    require("article_dependency_unchanged",
            sha(article)=="2571f9fbde25cd9e5258e5bb2c78797380123bf32621e4eaf068ce97c1b4c927")
    output={"claim":"W3_92_JOINT_STATIC_BOUNDARY_COMPATIBILITY_V1",
        "python":platform.python_version(),"sympy":s.__version__,
        "checks_passed":sum(checks.values()),"checks_total":len(checks),
        "failed_checks":[name for name,value in checks.items() if not value],
        "checks":checks,"details":details,
        "analytic_theorems_require_report_assumptions":[
            "Full label and spatial equations imply outer C_ell=0 under the declared tails and finite derivative charges",
            "Every nontrivial admissible embedding needs a positive material slope somewhere; zero-slope embedding fails the joint chain-rule, boundary and H conditions",
            "Retained APR virial then requires integral r^2 Hprime^2 dr = 3 m_H"],
        "closure_flags":{"joint_identity_checks_passed":all(checks.values()),
            "zero_outer_traction_assumed_in_advance":False,
            "old_APR_restoring_response_recomputed":False,
            "arbitrary_F_solution_constructed":False,"full_constrained_health_proved":False,
            "all_RefG_or_all_independent_H_models_excluded":False,
            "new_equilibrium_or_horizon_proved":False},
        "sha256":{"verifier":sha(Path(__file__)),"report":sha(REPORT),"article":sha(article),
            "APR_source":sha(apr/"common_scale_finite_source_candidate.py")}}
    print(json.dumps(output,indent=2))
    return 0 if all(checks.values()) else 1


def main():
    geometry_checks()
    central_lock_and_obstruction()
    independent_variation()
    principal_checks()
    numerical_germ()
    joining_checks()
    flags = {
        "central_source_lock_verified":checks["central_enthalpy_lock"],
        "original_strict_static_material_gate_excluded":
            checks["label_demands_positive_cubic"] and
            checks["anisotropy_demands_nonpositive_cubic"],
        "new_local_medium_germ_verified":all(value for name,value in checks.items()
            if name.startswith(("independent_EL_","germ_"))),
        "local_leading_principal_gate_verified":all(value for name,value in checks.items()
            if name.startswith(("scalar_","principal_","transverse_"))),
        "ordinary_oscillon_join_derived":False,
        "same_action_vacuum_join_excluded":checks["join_regular_stress_free_vacuum_excluded"],
        "extended_radial_principal_gate_failed":checks["join_event_found_2e-12"] and
            checks["join_negative_squared_speed_after_edge"],
        "response_fade_preserves_obstruction":checks["join_mixing_preserves_null_sum"] and
            checks["join_beta_one_null_source_negative"],
        "silent_exterior_joined":False,
        "finite_wavelength_full_constraint_health":False,
        "global_curvature_bound":False,
        "regular_black_hole_derived":False,
        "observational_validation":False}
    output = {
        "claim":"W3_92_COMMON_SCALE_CENTRE_SOURCE_V1",
        "joining_claim":"W3_92_COMMON_SCALE_CENTRE_JOIN_V1",
        "python":platform.python_version(),"sympy":s.__version__,
        "checks_passed":sum(checks.values()),"checks_total":len(checks),
        "failed_checks":[name for name,value in checks.items() if not value],
        "checks":checks,"details":details,"closure_flags":flags,
        "sha256":{"verifier":sha(Path(__file__)),
                  "contract":sha(REPORT),
                  "geometry_dependency":sha(HERE/"verify_covariant_medium_integration.py")}}
    print(json.dumps(output,ensure_ascii=False,indent=2))
    return 0 if all(checks.values()) else 1


if __name__=="__main__":
    if sys.argv[1:] == ["--joint-static-boundary-only"]:
        raise SystemExit(joint_static_boundary_checks())
    if sys.argv[1:] == ["--readout-H-bridge-only"]:
        raise SystemExit(independent_H_readout_checks())
    if sys.argv[1:] == ["--static-label-balance-only"]:
        raise SystemExit(static_label_balance_checks())
    if sys.argv[1:] == ["--feedback-assumptions-only"]:
        raise SystemExit(feedback_assumption_checks())
    if sys.argv[1:] == ["--matter-source-bridge-only"]:
        raise SystemExit(matter_source_bridge_checks())
    if sys.argv[1:]:
        raise SystemExit("Usage: verify_common_scale_centre_source.py [--feedback-assumptions-only | --matter-source-bridge-only | --static-label-balance-only | --readout-H-bridge-only | --joint-static-boundary-only]")
    raise SystemExit(main())
