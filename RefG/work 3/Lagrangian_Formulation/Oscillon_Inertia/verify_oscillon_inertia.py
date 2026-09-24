"""REFG_COVARIANT_OSCILLON_INERTIA_V1. Stdout-only, no strong-field scan."""
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
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp

HERE = Path(__file__).resolve().parent
W58 = HERE.parent / "One_Oscillon_Coframe_Localized_Core" / "w3_58_one_oscillon_coframe_localized_core.py"
W54 = HERE.parent / "Relational_Coframe_TEGR_Phase_Source_Closure" / "w3_54_relational_coframe_tegr_phase_source_closure.py"
W58_HASH = "b2c7d4380ba06eafefcae83391d321fd9cccb311a2f2a369a3d3b1406ad3dd57"
ALPHA = .001
CHARGE = 190.401136223484
VELOCITIES = (.2, .6, .8)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_seed_module():
    assert digest(W58) == W58_HASH, "W58 dependency changed"
    spec = importlib.util.spec_from_file_location("inertia_w58", W58)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def potential(f):
    return f*f/2-f**4/4+f**6/24


def force(f):
    return f-f**3+f**5/4


def exact_checks():
    checks = {}

    def zero(name, value):
        checks[name] = bool(sp.simplify(value) == 0)

    f, w, alpha = sp.symbols("f omega alpha", positive=True)
    V = f**2/2-f**4/4+f**6/24
    zero("bounded_positive_potential_factorization",
         V-f**2*((f**2-3)**2+3)/24)
    zero("potential_force", sp.diff(V, f)-(f-f**3+f**5/4))

    # Same-action radial variation BEFORE using the equilibrium equations.
    r = sp.symbols("r", positive=True)
    ff, F, sig = [sp.Function(n)(r) for n in ("f", "F", "sigma")]
    fp = sp.diff(ff, r)
    Vr = V.subs(f, ff)
    lag = sig*r**2*(w*w*ff**2/(2*sig**2*F)-F*fp**2/2-Vr)
    kg = sp.diff(lag, ff)-sp.diff(sp.diff(lag, fp), r)
    target = sp.diff(sig*r**2*F*fp, r)+sig*r**2*(w*w*ff/(sig**2*F)-sp.diff(Vr, ff))
    zero("radial_scalar_action_variation", kg-target)
    zero("phase_current_normalization", sp.diff(lag, w)-w*r**2*ff**2/(sig*F))
    kin, grad, pot = sp.symbols("T X V", real=True)
    rho, pr, pt = kin+grad+pot, kin+grad-pot, kin-grad-pot
    zero("komar_source_contains_all_stresses", rho+pr+2*pt-(4*kin-2*pot))

    # Flat Laue/virial identity and the full boosted field (not rigid f(x-vt)).
    E, S, v = sp.symbols("E stress v", real=True)
    gamma = 1/sp.sqrt(1-v*v)
    Eg = gamma*(E+v*v*S)
    Pg = gamma*v*(E+S)
    zero("laue_total_energy_boost", Eg.subs(S, 0)-gamma*E)
    zero("laue_total_momentum_boost", Pg.subs(S, 0)-gamma*E*v)
    checks["omitted_stress_control_rejected"] = sp.simplify(Pg-gamma*E*v) != 0
    ft = sp.Function("f")(r)
    radial_lag = r**2*(sp.diff(ft, r)**2/2+potential(ft)-w*w*ft*ft/2)
    virial_div = sp.diff(r**3*(sp.diff(ft,r)**2/2+w*w*ft*ft/2-potential(ft)), r)
    fpp = force(ft)-w*w*ft-2*sp.diff(ft,r)/r
    zero("flat_stress_virial_boundary",
         virial_div.subs(sp.diff(ft,r,2),fpp)
         -r*r*(-sp.diff(ft,r)**2/2+3*w*w*ft*ft/2-3*potential(ft)))

    # Compute ADM surface integrands from the entire Lorentz-transformed
    # asymptotic metric, independently of E=gamma*M.
    x,y,z,t,mu = sp.symbols("x y z t mu", real=True)
    g = 1/sp.sqrt(1-v*v)
    radius = sp.sqrt(x*x+y*y+g*g*(z-v*t)**2)
    eta = sp.diag(-1,1,1,1)
    velocity_cov = sp.Matrix([-g,0,0,g*v])
    h = 2*mu/radius*(eta+2*velocity_cov*velocity_cov.T)
    coords = (x,y,z)
    trace = sum(h[i+1,i+1] for i in range(3))
    evec = [sum(sp.diff(h[i+1,j+1],coords[j]) for j in range(3))
            -sp.diff(trace,coords[i]) for i in range(3)]
    K = sp.Matrix(3,3,lambda i,j:
        (sp.diff(h[0,j+1],coords[i])+sp.diff(h[0,i+1],coords[j])
         -sp.diff(h[i+1,j+1],t))/2)
    mom = [K[2,j]-(sp.trace(K) if j==2 else 0) for j in range(3)]
    # On t=0, axisymmetry permits y=0, x=r sin(theta).
    q = sp.symbols("q", positive=True)
    # q=gamma >=1 and v=sqrt(q^2-1)/q avoids square-root identities.
    substitutions = {t:0,y:0}
    en = sp.simplify(sum(evec[i]*coords[i] for i in range(3)).subs(substitutions))
    pn = sp.simplify(sum(mom[i]*coords[i] for i in range(3)).subs(substitutions))
    target_den = (x*x+g*g*z*z)**sp.Rational(3,2)
    zero("adm_energy_integrand_from_metric",
         en-4*mu*g*g*(x*x+z*z)/target_den)
    zero("adm_momentum_integrand_from_shift_and_K",
         pn-2*mu*g*g*v*(x*x+z*z)/target_den)
    c = sp.symbols("c", real=True)
    zero("adm_angular_primitive",
         sp.diff(c/sp.sqrt(1+(q*q-1)*c*c),c)
         -(1+(q*q-1)*c*c)**sp.Rational(-3,2))
    zero("adm_angular_integral", 2/q-2/sp.sqrt(1+(q*q-1)))
    # Deliberately omit shift; the surface integrand must change.
    Kbad = sp.Matrix(3,3,lambda i,j:-sp.diff(h[i+1,j+1],t)/2)
    pb = sum((Kbad[2,j]-(sp.trace(Kbad) if j==2 else 0))*coords[j]
             for j in range(3)).subs(substitutions)
    checks["omitted_shift_control_rejected"] = sp.simplify(pb-pn) != 0

    # Inertia is a derivative of the derived momentum, not an assignment.
    zero("inertial_mass_from_ADM_momentum", sp.diff(gamma*E*v,v).subs(v,0)-E)
    zero("invariant_ADM_mass", (gamma*E)**2-(gamma*E*v)**2-E**2)
    zero("energy_quadratic_coefficient", sp.diff(gamma*E,v,2).subs(v,0)-E)
    L = -E*sp.sqrt(1-v*v)
    zero("worldline_momentum_from_action", sp.diff(L,v)-gamma*E*v)
    zero("worldline_energy_from_action", v*sp.diff(L,v)-L-gamma*E)
    zero("longitudinal_force_coefficient", sp.diff(gamma*E*v,v)-E*gamma**3)
    u = sp.symbols("u", real=True)
    Lext = -E*sp.sqrt(1-2*u-(1+2*u)*v*v)
    zero("passive_mass_from_universal_metric", sp.diff(Lext,u).subs({u:0,v:0})-E)
    zero("weak_gradient_acceleration_normalization",
         sp.diff(Lext,u).subs({u:0,v:0})/
         sp.diff(Lext,v,2).subs({u:0,v:0})-1)
    p,b,ut = sp.symbols("p b ut", positive=True)
    rate = b*b/(alpha*p*p)*(1-sp.sqrt(1-ut*ut/(b*b*p*p)))
    zero("APR_rate_parameter_does_not_repair_quadratic_inertia",
         sp.diff(rate,ut,2).subs(ut,0)-1/(alpha*p**4))
    # Explicit inheritance boundary: neither exact common-p nor old APR
    # source balance is silently assigned to the covariant branch.
    mass,R = sp.symbols("mass R", positive=True)
    isotropic_N=(1-mass/(2*R))/(1+mass/(2*R))
    isotropic_A=(1+mass/(2*R))**2
    zero("isotropic_clock_ruler_product",isotropic_N*isotropic_A-(1-mass**2/(4*R**2)))
    checks["exact_common_p_inheritance_rejected"] = sp.simplify(isotropic_N*isotropic_A-1) != 0
    return checks

def equilibrium(flat, radius, tolerance, eps=1e-5, previous=None):
    x = np.linspace(eps, radius, 801)
    if previous is None:
        f, fp = flat.sol(x)
        omega = .8
        rho = .5*fp**2+.5*omega**2*f**2+potential(f)
        mass = cumulative_trapezoid(x*x*rho,x,initial=0)+rho[0]*eps**3/3
        q = cumulative_trapezoid(omega*x*x*f*f,x,initial=0)+omega*f[0]**2*eps**3/3
        ds = ALPHA*x*(fp*fp+omega*omega*f*f)
        integ = cumulative_trapezoid(ds,x,initial=0)
        sigma_log = integ-integ[-1]
        initial = np.vstack((f,fp,mass,sigma_log,q))
    else:
        initial = previous.sol(x)
        omega = float(1/(1+np.exp(-previous.p[0])))
    param = np.array([np.log(omega/(1-omega))])

    def fields(r,y,par):
        f,fp,mass,ls,q = y
        w = 1/(1+np.exp(-par[0]))
        sig = np.exp(ls)
        F = 1-2*ALPHA*mass/r
        T = w*w*f*f/(2*sig*sig*F)
        X = F*fp*fp/2
        rho = T+X+potential(f)
        mp = r*r*rho
        sp_ = ALPHA*r*(fp*fp+w*w*f*f/(sig*sig*F*F))
        Fp = -2*ALPHA*(mp/r-mass/(r*r))
        fpp = (force(f)-w*w*f/(sig*sig*F))/F-(2/r+sp_+Fp/F)*fp
        qp = w*r*r*f*f/(sig*F)
        return np.vstack((fp,fpp,mp,sp_,qp))

    def boundary(ya,yb,par):
        w = 1/(1+np.exp(-par[0]))
        f0,_,_,ls0,_ = ya
        sig0 = np.exp(ls0)
        f2 = (force(f0)-w*w*f0/(sig0*sig0))/6
        rho0 = w*w*f0*f0/(2*sig0*sig0)+potential(f0)
        k = np.sqrt(1-w*w)
        mu = ALPHA*yb[2]
        power = -1+mu*(2*w*w-1)/k
        return np.array([ya[1]-2*f2*eps,
                         ya[2]-rho0*eps**3/3,
                         ya[4]-w*f0*f0*eps**3/(3*sig0),
                         yb[3],
                         yb[1]+(k-power/radius)*yb[0],
                         yb[4]-CHARGE/(4*np.pi)])

    sol = solve_bvp(fields,boundary,x,initial,p=param,tol=tolerance,max_nodes=50000)
    if not sol.success:
        raise RuntimeError(sol.message)
    sol.inertia_rhs=fields
    sol.inertia_bc=boundary
    return sol


def measure_equilibrium(sol,points):
    r = np.linspace(sol.x[0],sol.x[-1],points)
    f,fp,m,ls,q = sol.sol(r)
    sig = np.exp(ls)
    w = float(1/(1+np.exp(-sol.p[0])))
    F = 1-2*ALPHA*m/r
    N = sig*np.sqrt(F)
    T = w*w*f*f/(2*sig*sig*F)
    X = F*fp*fp/2
    V = potential(f)
    rho,pr,pt = T+X+V,T+X-V,T-X-V
    mp = r*r*rho
    ds = ALPHA*r*(fp*fp+w*w*f*f/(sig*sig*F*F))
    Fp = -2*ALPHA*(mp/r-m/r**2)
    vp = ds+Fp/(2*F)
    fpp = (force(f)-w*w*f/(sig*sig*F))/F-(2/r+ds+Fp/F)*fp
    Tp = w*w/(sig*sig*F)*(f*fp-f*f*ds-f*f*Fp/(2*F))
    Xp = Fp*fp*fp/2+F*fp*fpp
    Vp = force(f)*fp
    rhop = Tp+Xp+Vp
    mpp = 2*r*rho+r*r*rhop
    Fpp = -2*ALPHA*(mpp/r-2*mp/r**2+2*m/r**3)
    dss = ALPHA*(fp*fp+w*w*f*f/(sig*sig*F*F))
    dss += ALPHA*r*(2*fp*fpp+w*w/(sig*sig*F*F)*(2*f*fp-2*f*f*ds-2*f*f*Fp/F))
    vpp = dss+(Fpp/F-Fp*Fp/(F*F))/2
    lp = -Fp/(2*F)
    # These are on-shell algebraic consistency identities: the derivatives
    # above are reconstructed from the same ODEs. The independent numerical
    # controls are solve_bvp's spline residual and separate mass quadratures.
    angular = F*(vpp+vp*vp-vp*lp+(vp-lp)/r)-2*ALPHA*pt
    conservation = Tp+Xp-Vp+vp*(rho+pr)-2*(pt-pr)/r
    # Include origin series. Tail amplitude and a domain increase provide
    # numerical tail control, not an interval-certified omitted-tail bound.
    Eadm = 4*np.pi*m[-1]
    Evol = 4*np.pi*(simpson(r*r*rho,x=r)+rho[0]*r[0]**3/3)
    Ekomar = 4*np.pi*(simpson(sig*r*r*(rho+pr+2*pt),x=r)
                       +sig[0]*(rho[0]+pr[0]+2*pt[0])*r[0]**3/3)
    Ekomar_surface = 4*np.pi*sig[-1]*(m[-1]+r[-1]**3*pr[-1])
    Qvol = 4*np.pi*(simpson(w*r*r*f*f/(sig*F),x=r)
                     +w*f[0]**2*r[0]**3/(3*sig[0]))
    proper_energy = 4*np.pi*simpson(r*r*rho/np.sqrt(F),x=r)
    mu = ALPHA*m[-1]
    R = r[-1]
    iso_R=(R-mu+np.sqrt(R*(R-2*mu)))/2
    iso_integral=cumulative_trapezoid((1/np.sqrt(F)-1)/r,r,initial=0)
    lnA=np.log(R/iso_R)+iso_integral[-1]-iso_integral
    NA = N*np.exp(lnA)
    return dict(radius=float(R),epsilon=float(r[0]),points=points,
                omega=w,f_centre=float(f[0]),Q=Qvol,energy_ADM=Eadm,
                energy_volume=Evol,energy_Komar=Ekomar,
                energy_Komar_surface=float(Ekomar_surface),
                proper_matter_energy=float(proper_energy),
                lapse_centre=float(N[0]),min_F=float(F.min()),
                min_lapse=float(N.min()),min_profile=float(f.min()),
                max_abs_profile_tail=float(abs(f[-1])),
                max_bvp_residual=float(max(sol.rms_residuals)),
                boundary_residual=float(max(abs(sol.inertia_bc(sol.y[:,0],sol.y[:,-1],sol.p)))),
                angular_Einstein_algebraic_residual=float(max(abs(angular))),
                matter_conservation_algebraic_residual=float(max(abs(conservation))),
                max_clock_ruler_product_deviation=float(max(abs(NA-1))),
                centre_clock_ruler_product=float(NA[0]),
                exterior_clock_ruler_product=float(NA[-1]))


def flat_witness(flat):
    r=np.linspace(0,80,16001)
    f,fp=flat.sol(r)
    T=.5*.8**2*f*f
    X=.5*fp*fp
    V=potential(f)
    rho=T+X+V
    pr,pt=T+X-V,T-X-V
    energy=4*np.pi*simpson(r*r*rho,x=r)
    stress=4*np.pi*simpson(r*r*(pr+2*pt)/3,x=r)
    mi=4*np.pi*simpson(r*r*(.8**2*f*f+fp*fp/3),x=r)
    rows=[]
    for v in VELOCITIES:
        gamma=1/np.sqrt(1-v*v)
        # Boost the stress before integration; include contraction d^3x/gamma.
        boosted_energy=4*np.pi*simpson(r*r*gamma*(rho+v*v*(pr+2*pt)/3),x=r)
        momentum=4*np.pi*simpson(r*r*gamma*v*(rho+(pr+2*pt)/3),x=r)
        rows.append(dict(v=v,E=boosted_energy,P=momentum,
                         energy_relative_error=abs(boosted_energy/(gamma*energy)-1),
                         momentum_relative_error=abs(momentum/(gamma*v*energy)-1)))
    return dict(energy=float(energy),integrated_stress=float(stress),
                inertial_coefficient=float(mi),mass_relative_gap=float(mi/energy-1),
                boost_rows=rows)


def numerical_boosts(rest_mass):
    G=ALPHA/(4*np.pi)
    mu=G*rest_mass
    nodes,weights=np.polynomial.legendre.leggauss(64)
    rows=[]
    for v in VELOCITIES:
        gamma=1/np.sqrt(1-v*v)
        lam=np.sqrt(1+(gamma*gamma-1)*nodes*nodes)
        # Unit large-radius surface: factors of radius cancel.
        e_integrand=4*mu*gamma*gamma/lam**3
        p_integrand=2*mu*gamma*gamma*v/lam**3
        E=2*np.pi*np.dot(weights,e_integrand)/(16*np.pi*G)
        P=2*np.pi*np.dot(weights,p_integrand)/(8*np.pi*G)
        inv=np.sqrt(E*E-P*P)
        rows.append(dict(v=v,E=float(E),P=float(P),invariant_mass=float(inv),
                         energy_relative_error=float(abs(E/(gamma*rest_mass)-1)),
                         momentum_relative_error=float(abs(P/(gamma*v*rest_mass)-1)),
                         invariant_relative_error=float(abs(inv/rest_mass-1))))
    return rows


def main():
    checks=exact_checks()
    print(json.dumps(dict(claim_id="REFG_COVARIANT_OSCILLON_INERTIA_V1",
        python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__,
        verifier_sha256=digest(Path(__file__)),contract_sha256=digest(HERE/"oscillon_inertia.md"),
        W58_sha256=digest(W58),W54_sha256=digest(W54),alpha=ALPHA,Q=CHARGE,
        exact_checks=checks),sort_keys=True),flush=True)
    seed=load_seed_module()
    flat=seed.solve_profile(.8,radius=80.,tolerance=1e-8)
    flatrow=flat_witness(flat)
    print(json.dumps(dict(flat=flatrow),sort_keys=True),flush=True)
    checks["flat_stress_balance"]=abs(flatrow["integrated_stress"])/flatrow["energy"]<3e-6
    checks["flat_translation_inertia"]=abs(flatrow["mass_relative_gap"])<3e-6
    for row in flatrow["boost_rows"]:
        checks["flat_boost_"+str(row["v"])]=max(row["energy_relative_error"],row["momentum_relative_error"])<3e-6
    records=[]
    previous=None
    specs=((40.,1e-7,1e-5,8001),(60.,3e-8,1e-5,16001),(60.,3e-8,5e-6,16001))
    for radius,tol,eps,points in specs:
        sol=equilibrium(flat,radius,tol,eps,previous)
        row=measure_equilibrium(sol,points)
        records.append(row)
        previous=sol
        print(json.dumps(dict(equilibrium=row),sort_keys=True),flush=True)
        label="R"+str(radius)+"_eps"+str(eps)
        E=row["energy_ADM"]
        checks[label+"_charge"]=abs(row["Q"]/CHARGE-1)<2e-6
        checks[label+"_boundary"]=row["boundary_residual"]<1e-7
        checks[label+"_bvp"]=row["max_bvp_residual"]<1.1*tol
        checks[label+"_weak_regular"]=row["min_lapse"]>.9 and row["min_F"]>0 and row["min_profile"]>-1e-10
        checks[label+"_ADM_volume"]=abs(row["energy_volume"]/E-1)<3e-5
        checks[label+"_ADM_Komar"]=abs(row["energy_Komar"]/E-1)<3e-5
        checks[label+"_Komar_surface"]=abs(row["energy_Komar_surface"]/E-1)<3e-5
        checks[label+"_Einstein_angular_identity"]=row["angular_Einstein_algebraic_residual"]<1e-7
        checks[label+"_stress_conservation_identity"]=row["matter_conservation_algebraic_residual"]<1e-7
        checks[label+"_localized_tail"]=row["max_abs_profile_tail"]<1e-8
    for i in (0,1):
        for key in ("energy_ADM","omega","lapse_centre"):
            checks["convergence_"+str(i)+"_"+key]=abs(records[i][key]/records[i+1][key]-1)<3e-5
    boosts=numerical_boosts(records[-1]["energy_ADM"])
    for row in boosts:
        label="ADM_boost_"+str(row["v"])
        checks[label]=max(row["energy_relative_error"],row["momentum_relative_error"],row["invariant_relative_error"])<1e-10
    print(json.dumps(dict(adm_boosts=boosts),sort_keys=True),flush=True)
    checks={k:bool(v) for k,v in checks.items()}
    passed_all=all(checks.values())
    status=("COVARIANT_BRANCH_INERTIA_DERIVED_WITH_WEAK_EQUILIBRIUM_WITNESS"
            if passed_all else "VERIFICATION_FAILED")
    result=dict(passed=sum(checks.values()),total=len(checks),all_passed=passed_all,checks=checks,
                status=status,
                exact_APR_dynamics_repaired=False,exact_common_p_retained=False,
                independent_microphysical_action_derived=False,full_nonlinear_stability_proved=False,
                strong_field_work_performed=False,observational_validation=False)
    print(json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


