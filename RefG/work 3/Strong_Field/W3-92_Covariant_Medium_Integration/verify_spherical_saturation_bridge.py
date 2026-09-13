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


def saturation_curvature(rho,pr,pt,J,z,alpha,ell):
    """On-shell four-curvature of the same spherical action, in any orbit frame.

    J=T(n,e), not the coordinate flux S. No division by the trapping
    function occurs. Lorentzian contractions retain the negative flux term.
    """
    u = ell**2*z
    q,b = 1-u,alpha*(1-u)**2
    C = z*(1-3*u)/2
    hnn,hee,hne = -(C+b*pr),C-b*rho,-b*J
    box = -hnn+hee
    hess2 = hnn**2+hee**2-2*hne**2
    orbit = (2*z*(1-9*u+9*u**2)+2*b*(1-6*u)*(pr-rho)-4*b*pt
             +8*alpha**2*ell**2*q**3*(rho*pr-J**2))
    return dict(orbit_Ricci=orbit,Ricci_scalar=orbit+2*z-4*box,
                Kretschmann=orbit**2+8*hess2+4*z**2,
                hnn_over_r=hnn,hee_over_r=hee,hne_over_r=hne)


def saturation_curvature_checks():
    """Exact action, metric, frame and conditional smooth-centre crosschecks."""
    checks = []
    def exact(name,value,target=0):
        residual = s.factor(s.cancel(value-target))
        checks.append(dict(name="curvature_"+name,passed=residual==0,
                           residual=str(residual)))
    r,z,ell,a = s.symbols("r z ell alpha",positive=True)
    rho,pr,pt,J = s.symbols("rho pr pt J",real=True)
    u,q = ell**2*z,1-ell**2*z
    c = saturation_curvature(rho,pr,pt,J,z,a,ell)
    hnn,hee,hne = (c[k] for k in ("hnn_over_r","hee_over_r","hne_over_r"))
    box,hess2 = r*(-hnn+hee),r*r*(hnn**2+hee**2-2*hne**2)
    beta = -2*r/q**2
    ar = 4*ell**2*r*z*z*(1+3*u)/q**3
    br,bx = (-2+10*u)/q**3,4*ell**2/(r*q**3)
    exact("angular_action",-beta*c["orbit_Ricci"]+ar+2*br*box
          +2*bx*(box**2-hess2)+8*a*r*pt)
    exact("Einstein_Ricci",c["Ricci_scalar"].subs(ell,0),2*a*(rho-pr-2*pt))
    m = s.symbols("m",positive=True)
    zs = 2*m/(r**3+2*m*ell**2)
    f = 1-r*r*zs
    vacuum = saturation_curvature(0,0,0,0,zs,a,ell)
    exact("vacuum_orbit_direct_metric",vacuum["orbit_Ricci"],-s.diff(f,r,2))
    exact("vacuum_Ricci_direct_metric",vacuum["Ricci_scalar"],
          -s.diff(f,r,2)-4*s.diff(f,r)/r+2*(1-f)/r**2)
    exact("vacuum_K_direct_metric",vacuum["Kretschmann"],
          s.diff(f,r,2)**2+4*(s.diff(f,r)/r)**2+4*((1-f)/r**2)**2)
    dust = saturation_curvature(3*z/(2*a*q),0,0,0,z,a,ell)
    exact("FLRW_dust_Ricci",dust["Ricci_scalar"],3*z*(1+3*u))
    exact("FLRW_dust_K",dust["Kretschmann"],3*z*z*((3*u-1)**2+4))
    # Rational rapidity covers arbitrary finite boosts away from v=+/-1.
    v = s.symbols("v",real=True)
    ch,sh = (1+v*v)/(1-v*v),2*v/(1-v*v)
    rb,pb = ch*ch*rho+2*ch*sh*J+sh*sh*pr,sh*sh*rho+2*ch*sh*J+ch*ch*pr
    jb = ch*sh*(rho+pr)+(ch*ch+sh*sh)*J
    boosted = saturation_curvature(rb,pb,pt,jb,z,a,ell)
    for key in ("orbit_Ricci","Ricci_scalar","Kretschmann"):
        exact("boost_"+key,boosted[key],c[key])
    p = s.symbols("p",real=True)
    centre = saturation_curvature(3*z/(2*a*q),p,p,0,z,a,ell)
    X = z*(1-3*u)/2+a*q*q*p
    exact("regular_centre_orbit",centre["orbit_Ricci"],-2*X)
    exact("regular_centre_Ricci",centre["Ricci_scalar"],6*(z-X))
    exact("regular_centre_K",centre["Kretschmann"],12*(X*X+z*z))
    uu,w = s.symbols("u w",real=True)
    x = uu*(1-3*uu+3*(1-uu)*w)/2
    kd = 12*(x*x+uu*uu)
    exact("centre_w_convex",s.diff(kd,w,2),54*uu*uu*(1-uu)**2)
    km,kp = kd.subs(w,-1),kd.subs(w,1)
    exact("centre_minus_endpoint",km,24*uu*uu)
    exact("centre_plus_endpoint",kp,12*uu*uu*(9*uu*uu-12*uu+5))
    exact("centre_plus_monotonic",s.diff(kp,uu),
          24*uu*(18*(uu-s.Rational(1,2))**2+s.Rational(1,2)))
    exact("centre_endpoint_bound",kp.subs(uu,1),24)
    centre_checks = [item for item in checks if "centre_" in item["name"]]
    checks.append(dict(name="curvature_conditional_centre_bound",
        passed=all(item["passed"] for item in centre_checks),
        evidence="Exact convexity and monotone endpoints give ell^4 K<=24 for "
        "0<=u<=1, |p|<=rho, rho=3z/(2alpha q), and a smooth isotropic centre; "
        "this does not establish persistence of centre regularity."))
    flat = saturation_curvature(0,0,0,0,s.Integer(0),a,ell)
    V = s.symbols("V",nonnegative=True)
    zv = 2*a*V/(3+2*a*ell**2*V)
    potential = saturation_curvature(V,-V,-V,0,zv,a,ell)
    for key,target in (("orbit_Ricci",2*zv),("Ricci_scalar",12*zv),("Kretschmann",24*zv*zv)):
        exact("flat_"+key,flat[key])
        exact("constant_potential_"+key,potential[key],target)
    return checks


def source_concentration_checks():
    """Bounded source-cap decision: exact identities and a fixed-mass PG family.

    These are distinct smooth constrained initial slices, with no time
    evolution or inference about blow-up of the retained charged packet.
    """
    entry_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    checks = list(saturation_curvature_checks())
    def exact(name,value,target=0):
        residual = s.factor(s.cancel(value-target))
        checks.append(dict(name="concentration_"+name,passed=residual==0,
                           residual=str(residual)))
    def gate(name,condition,**evidence):
        checks.append(dict(name="concentration_"+name,passed=bool(condition),**evidence))
    r,z,a,ell = s.symbols("r z alpha ell",positive=True)
    rho,pr,pt,J = s.symbols("rho pr pt J",real=True)
    u,q = ell**2*z,1-ell**2*z
    C,b = z*(1-3*u)/2,a*q*q
    trace,det = pr-rho,rho*pr-J*J
    curv = saturation_curvature(rho,pr,pt,J,z,a,ell)
    hess = curv["hnn_over_r"]**2+curv["hee_over_r"]**2-2*curv["hne_over_r"]**2
    exact("invariant_orbit_reduction",curv["orbit_Ricci"],
          2*z*(1-9*u+9*u*u)+2*b*(1-6*u)*trace-4*b*pt+8*a*a*ell*ell*q**3*det)
    exact("invariant_hessian_reduction",hess,2*C*C+2*C*b*trace+b*b*(trace*trace+2*det))
    # Canonical scalar: X=|n psi|^2, Y=|e psi|^2, J=n psi dot e psi.
    p0,p1,d0,d1 = s.symbols("p0 p1 d0 d1",real=True)
    X,Y,j = p0*p0+p1*p1,d0*d0+d1*d1,p0*d0+p1*d1
    V,y = s.symbols("V y",nonnegative=True)
    kin = (X+Y)/2
    rr,pp,tt = kin+V,kin-V,(X-Y)/2-V
    delta = rr*pp-j*j
    exact("canonical_gram_nonnegative",X*Y-j*j,(p0*d1-p1*d0)**2)
    exact("canonical_potential_nonnegative",y/2-y*y/4+y**3/24,y*((y-3)**2+3)/24)
    exact("canonical_pr_bounds_lower",rr-pp,2*V)
    exact("canonical_pr_bounds_upper",rr+pp,X+Y)
    exact("canonical_pt_bounds_lower",rr-tt,Y+2*V)
    exact("canonical_pt_bounds_upper",rr+tt,X)
    exact("canonical_flux_bound",rr*rr-j*j,(X-Y)**2/4+(p0*d1-p1*d0)**2+2*kin*V+V*V)
    exact("canonical_det_upper",rr*rr-delta,V*(X+Y+2*V)+j*j)
    exact("canonical_det_lower",rr*rr+delta,(X*X+Y*Y)/2+(X*Y-j*j)+V*(X+Y))
    uu,E = s.symbols("u E",nonnegative=True)
    cc = uu*(1-3*uu)/2
    exact("bound_C_lower",cc+1,(1-uu)*(3*uu+2)/2)
    exact("bound_C_upper",cc,s.Rational(1,24)-s.Rational(3,2)*(uu-s.Rational(1,6))**2)
    exact("bound_vacuum_polynomial",1-9*uu+9*uu*uu,9*(uu-s.Rational(1,2))**2-s.Rational(5,4))
    exact("bound_vacuum_polynomial_upper",1-(1-9*uu+9*uu*uu),9*uu*(1-uu))
    qq = s.symbols("q",positive=True)
    source_scale = a*ell**2*qq**s.Rational(3,2)*rho
    exact("bound_linear_source_weight",a*ell**2*qq**2*rho,s.sqrt(qq)*source_scale)
    exact("bound_quadratic_source_weight",a*a*ell**4*qq**3*rho*rho,source_scale**2)
    exact("centre_source_scale",source_scale.subs({rho:3*z/(2*a*qq)}),
          s.Rational(3,2)*ell**2*z*s.sqrt(qq))
    exact("centre_source_scale_bound",s.Rational(1,3)-s.Rational(9,4)*uu**2*(1-uu),
          (3*uu-2)**2*(3*uu+1)/12)
    B = s.Rational(5,2)+24*E+8*E*E
    bound_R,bound_K = B+10+8*E,B*B+16*(1+E)**2+16*E*E+4
    proof_checks = [item for item in checks if item["name"].startswith("concentration_")]
    gate("conditional_source_bounds",all(item["passed"] for item in proof_checks),
         domain="0<=u<1, V>=0, canonical scalar, alpha>0, ell>0",
         premise="E=alpha ell^2 q^(3/2) rho is bounded in the monitored orthonormal frame",
         orbit_bound=str(B),Ricci_bound=str(bound_R),K_bound=str(bound_K),
         argument="Canonical SOS identities give |pr|,|pt|,|J|<=rho and |det|<=rho^2. "
         "With |ell^2 C|<=1, |1-6u|<=5, q<=1 and vacuum polynomial <=5/4 in magnitude, "
         "triangle inequalities yield the displayed bounds. E bounded is a premise, not an action-derived result.")
    e,m,vr,v = s.symbols("e m vr v",positive=True)
    kinetic = saturation_curvature(e,e,e,0,z,a,ell)
    exact("kinetic_orbit",kinetic["orbit_Ricci"],2*z*(1-9*u+9*u*u)-4*b*e+8*a*a*ell*ell*q**3*e*e)
    exact("kinetic_hessian",kinetic["hnn_over_r"]**2+kinetic["hee_over_r"]**2,2*C*C+2*b*b*e*e)
    leading = s.Poly(s.expand(kinetic["Kretschmann"]),e).coeff_monomial(e**4)
    exact("kinetic_K_leading",leading,64*a**4*ell**4*q**6)
    missing_term_orbit = kinetic['orbit_Ricci']-8*a*a*ell*ell*q**3*e*e
    missing_term_K = kinetic['Kretschmann']-kinetic['orbit_Ricci']**2+missing_term_orbit**2
    missing_leading = s.Poly(s.expand(missing_term_K),e).coeff_monomial(e**4)
    gate('omitted_quadratic_source_detected',s.factor(leading-missing_leading)!=0,
         coefficient_difference=str(s.factor(leading-missing_leading)))
    # Flat PG slice A=L=1, v^2=r^2 z, psi=D=0, P=sqrt(2 rho).
    zm = 2*a*m/(r**3+2*a*ell*ell*m)
    qm,Cm = 1-ell*ell*zm,zm*(1-3*ell*ell*zm)/2
    vv = r*r*zm
    vvprime = s.diff(vv,r)+s.diff(vv,m)*r*r*e
    exact("PG_radial_constraint",-vvprime/2,r*(Cm-a*qm*qm*e))
    exact("PG_momentum_constraint",2*(vr-v/r)/r-2*(vr/r-v/r**2))
    vt = r*(v*(vr/r-v/r**2)+(v/r)**2+C+b*e)
    exact("PG_normal_action",-vt+v*vr,-r*(C+b*e))
    Mt = 2*r*r*v*e
    vt_pg = vvprime/2+r*(Cm+a*qm*qm*e)
    At_pg = -r*r*s.diff(zm,m)*Mt+2*v*vt_pg
    exact("PG_mixed_action",At_pg/2)
    # Direct metric R2 from K^r_r=v_r-alpha*r*q^2*S and S_t=rho_r
    # on this slice. Density derivatives cancel using the scalar equation.
    zr = (2*a*q*q*e-3*z*q)/r
    metric_orbit = -2*(C+r*s.diff(C,z)*zr+b*e+r*s.diff(b,z)*zr*e)
    exact('PG_direct_metric_orbit',metric_orbit,kinetic['orbit_Ricci'])
    gp,M0,width,r0 = s.symbols("g M0 width r0",positive=True)
    peak_density = M0*gp/(width*r0*r0)
    exact("fixed_mass_shell_density",r0*r0*peak_density,M0*gp/width)
    positive_leading = 64*a**4*ell**4*qq**6
    gate("positive_thin_shell_leading",positive_leading.is_positive,
         coefficient=str(positive_leading),scope="K grows as width^-4 across distinct smooth initial slices")
    def normalization(dps):
        with mp.workdps(dps):
            bump = lambda x: mp.exp(-2/(1-x*x)) if abs(x)<1 else mp.mpf(0)
            integral = mp.quad(bump,[-1,0,1])
            left = mp.quad(bump,[-1,0])/integral
            return +integral,+left
    I40,left40 = normalization(40)
    I60,left60 = normalization(60)
    examples = []
    with mp.workdps(60):
        relative = abs(I40-I60)/I60
        gate("bump_normalization_precision",relative<mp.mpf("1e-30"),relative_error=float(relative))
        gate("bump_midpoint_symmetry",abs(left40-mp.mpf('.5'))<mp.mpf('1e-35')
             and abs(left60-mp.mpf('.5'))<mp.mpf('1e-55'),G_midpoint=float(left60))
        aa,ll,rr0 = mp.mpf('.04'),mp.mpf(2),mp.mpf(3)
        mass = 3*mp.sqrt(3)*ll/(2*aa)
        g0 = mp.exp(-2)/I60
        recovered = mass*mp.quad(lambda x:mp.exp(-2/(1-x*x))/I60 if abs(x)<1 else 0,[-1,0,1])
        gate("shell_total_mass",abs(recovered-mass)/mass<mp.mpf('1e-55'),mass=float(mass))
        zm = aa*mass/(rr0**3+aa*ll*ll*mass)
        qm = 1-ll*ll*zm
        for ww in (mp.mpf('.5'),mp.mpf('.25'),mp.mpf('.125'),mp.mpf('.0625')):
            density = mass*g0/(ww*rr0*rr0)
            values = saturation_curvature(density,density,density,mp.mpf(0),zm,aa,ll)
            scaled_K = ll**4*values['Kretschmann']
            escale = aa*ll*ll*qm**mp.mpf('1.5')*density
            BB = mp.mpf('2.5')+24*escale+8*escale*escale
            valid = all(mp.isfinite(value) for value in values.values()) and 0<qm<1
            bound_ok = (abs(ll*ll*values['orbit_Ricci'])<=BB
                        and abs(ll*ll*values['Ricci_scalar'])<=BB+10+8*escale
                        and abs(scaled_K)<=BB*BB+16*(1+escale)**2+16*escale*escale+4)
            row = dict(width=float(ww),mass=float(mass),q=float(qm),u=float(ll*ll*zm),
                       rho=float(density),ell4_K=float(scaled_K),E=float(escale),
                       F=float(1-rr0*rr0*zm),A=1.0,G_midpoint=.5)
            examples.append(row)
            gate("shell_width_"+str(float(ww)),valid and bound_ok,finite=bool(valid),conditional_bounds=bool(bound_ok))
    gate("fixed_mass_and_response",len({row['mass'] for row in examples})==1
         and len({row['q'] for row in examples})==1 and len({row['u'] for row in examples})==1)
    gate("finite_counterexample_exceeds_centre_bound",any(row['ell4_K']>24 for row in examples),
         scope="Generic off-centre cap excluded; the regular-centre theorem is unchanged")
    end_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    gate("source_unchanged",entry_hash==end_hash)
    failed = [item['name'] for item in checks if not item['passed']]
    return dict(decision="AUTOMATIC_INTERIOR_CURVATURE_CAP_EXCLUDED" if not failed else "SOURCE_CONCENTRATION_CHECK_FAILURE",
                checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,examples=examples,
                scope=dict(local_source_criterion=not failed,
                    automatic_uniform_cap_excluded=not failed,
                    uniform_cap_from_saturation_alone=False if not failed else None,
                    smooth_fixed_mass_family=not failed,
                    bounded_source_derived=False,fixed_packet_blowup=False,
                    global_regularity=False,singularity_removal=False,full_RefG_pressure_join=False,
                    interpretation='Conditional source bounds and a family of distinct smooth initial slices; no evolution or singularity formation claim'),
                source_hashes={Path(__file__).name:entry_hash})


def source_budget_checks():
    """Existing-action instantaneous normal-frame feedback, without evolution.

    Directional differences test the on-shell curvature/source readouts along
    the exact initial RHS. They are not later physical solution states.
    """
    entry_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    prerequisite = source_concentration_checks()
    checks = list(prerequisite['details'])
    def exact(name,value,target=0):
        residual = s.factor(s.cancel(value-target))
        checks.append(dict(name='budget_'+name,passed=residual==0,residual=str(residual)))
    def gate(name,condition,**evidence):
        checks.append(dict(name='budget_'+name,passed=bool(condition),**evidence))
    r,a,ell,z,rho,mu = s.symbols('r alpha ell z rho mu',positive=True)
    acc,srad,Kg,k = s.symbols('acc srad Kg k',real=True)
    pi = s.symbols('pi0 pi1',real=True)
    chi = s.symbols('chi0 chi1',real=True)
    epi = s.symbols('epi0 epi1',real=True)
    echi = s.symbols('echi0 echi1',real=True)
    force = s.symbols('force0 force1',real=True)
    V = s.symbols('V',real=True)
    PP,DD = sum(x*x for x in pi),sum(x*x for x in chi)
    rr,pr,pt = (PP+DD)/2+V,(PP+DD)/2-V,(PP-DD)/2-V
    J = sum(x*y for x,y in zip(pi,chi))
    npi = [echi[i]+(acc+2*srad/r)*chi[i]+(Kg+2*k)*pi[i]-force[i] for i in range(2)]
    nchi = [epi[i]+acc*pi[i]+Kg*chi[i] for i in range(2)]
    nrho_KG = sum(pi[i]*npi[i]+chi[i]*nchi[i]+force[i]*pi[i] for i in range(2))
    eJ = sum(epi[i]*chi[i]+pi[i]*echi[i] for i in range(2))
    conservation = eJ+2*(acc+srad/r)*J+Kg*(rr+pr)+2*k*(rr+pt)
    exact('canonical_energy_conservation',nrho_KG,conservation)
    for component in range(2):
        exact('potential_rate_cancellation_'+str(component),s.diff(nrho_KG,force[component]))
    psi = s.symbols('psi0 psi1',real=True)
    amplitude2 = sum(x*x for x in psi)
    retained_V = amplitude2/2-amplitude2**2/4+amplitude2**3/24
    vacuum = {x:0 for x in psi+chi}
    exact('initial_potential_rate',sum(s.diff(retained_V,psi[i])*pi[i] for i in range(2)).subs(vacuum))
    exact('initial_gradient_energy_rate',sum(chi[i]*nchi[i] for i in range(2)).subs(vacuum))
    nJ = sum(npi[i]*chi[i]+pi[i]*nchi[i] for i in range(2))
    exact('initial_PG_flux_rate',nJ.subs(vacuum).subs(acc,0),sum(pi[i]*epi[i] for i in range(2)))
    M,v,A,S,pressure = s.symbols('M v A S pressure',real=True)
    Mr = r*r*(rho+v*S)
    Mt_over_L = r*r*(v*(rho+pressure)+(A+v*v)*S)
    nmu = (Mt_over_L-v*Mr)/r**3+3*M*v/r**4
    exact('normal_mass_budget',nmu,(v/r)*(3*M/r**3+pressure)+A*S/r)
    qmu = 1/(1+2*a*ell*ell*mu)
    mdot,rdot = s.symbols('nmu nrho',real=True)
    exact('response_chain',s.diff(qmu,mu)*mdot,-2*a*ell*ell*qmu*qmu*mdot)
    Emu = a*ell*ell*qmu**s.Rational(3,2)*rho
    exact('weighted_source_chain',s.diff(Emu,mu)*mdot+s.diff(Emu,rho)*rdot,
          a*ell*ell*qmu**s.Rational(3,2)*(rdot-3*a*ell*ell*qmu*rho*mdot))
    u,q = ell*ell*z,1-ell*ell*z
    kk = s.sqrt(z)
    C = z*(1-3*u)/2
    mus = z/(2*a*q)
    Kpg = (-C+a*q*q*rho)/kk
    gamma_rho = 2*(Kpg+2*kk)
    gamma_feedback = -3*a*ell*ell*q*kk*(rho+3*mus)
    gamma_E = s.Rational(3,2)*kk*(2-u)+a*rho*q*(2-5*u)/kk
    exact('PG_density_positive',gamma_rho,3*kk*(1+u)+2*a*q*q*rho/kk)
    exact('PG_source_feedback',gamma_rho+gamma_feedback,gamma_E)
    turning = 3*z*(2-u)/(2*a*q*(5*u-2))
    exact('PG_turning_threshold',gamma_E,-a*q*(5*u-2)/kk*(rho-turning))
    pfield,vr = s.symbols('P vr',real=True)
    exact('PG_direct_KG_density',pfield*((vr+2*kk)*pfield),2*(vr+2*kk)*(pfield*pfield/2))
    pf,vf = s.Function('P')(r),s.Function('v')(r)
    exact('PG_scalar_normal_transport',s.diff(r*r*vf*pf,r)/r**2-vf*s.diff(pf,r),
          (s.diff(vf,r)+2*vf/r)*pf)
    # At psi=D=0, V and its first normal rate vanish; pr=pt=rho and
    # J=0. K has no term linear in J, so the two-variable tangent is exact.
    kinetic = saturation_curvature(rho,rho,rho,0,z,a,ell)
    KK = kinetic['Kretschmann']
    EE = a*ell*ell*q**s.Rational(3,2)*rho
    n_rho,n_z = rho*gamma_rho,2*a*q*q*kk*(rho+3*mus)
    n_E = s.simplify(s.diff(EE,rho)*n_rho+s.diff(EE,z)*n_z)
    n_K = s.diff(KK,rho)*n_rho+s.diff(KK,z)*n_z
    exact('PG_curvature_rate_leading',s.Poly(s.expand(n_K),rho).coeff_monomial(rho**5),
          256*a**5*ell**4*q**7*(2-5*u)/kk)
    exact('PG_E_directional_chain',n_E,EE*gamma_E)
    generic_pr,generic_pt,generic_J = s.symbols('pr pt J',real=True)
    full = saturation_curvature(rho,generic_pr,generic_pt,generic_J,z,a,ell)
    exact('kinetic_zero_flux_first_variation',s.diff(full['Kretschmann'],generic_J).subs(generic_J,0))
    rates = s.lambdify((rho,z,a,ell),(gamma_rho,gamma_feedback,gamma_E,n_rho,n_z,n_E,n_K,turning),'numpy')
    examples = []
    for source_row in prerequisite['examples']:
        density,aa,ll = source_row['rho'],.04,2.0
        zz = source_row['u']/(ll*ll)
        values = rates(density,zz,aa,ll)
        gr,gf,ge,nr,nz,ne,nk,threshold = map(float,values)
        escale = aa*ll*ll*(1-ll*ll*zz)**1.5*density
        tag = str(source_row['width'])
        directional = []
        for step in (1e-6,5e-7):
            rp,zp = density+step*nr,zz+step*nz
            rm,zm = density-step*nr,zz-step*nz
            qp,qm = 1-ll*ll*zp,1-ll*ll*zm
            admissible = min(rp,rm,qp,qm)>0 and max(qp,qm)<1
            if admissible:
                kp = saturation_curvature(rp,rp,rp,0.,zp,aa,ll)['Kretschmann']
                km = saturation_curvature(rm,rm,rm,0.,zm,aa,ll)['Kretschmann']
                ep,em = aa*ll*ll*qp**1.5*rp,aa*ll*ll*qm**1.5*rm
                dk,de = (kp-km)/(2*step),(ep-em)/(2*step)
                errors = dict(K=abs(dk-nk)/max(1.,abs(nk)),E=abs(de-ne)/max(1.,abs(ne)))
                finite = all(math.isfinite(value) for value in (dk,de,*errors.values()))
            else:
                dk=de=math.nan
                errors=dict(K=math.inf,E=math.inf)
                finite=False
            gate('directional_'+tag+'_'+str(step),admissible and finite and max(errors.values())<1e-5,
                 error=errors,step=step,admissible=admissible,
                 interpretation='Centred readout derivative along the initial normal RHS; not time evolution')
            directional.append(dict(step=step,nK_difference=float(dk),nE_difference=float(de),errors=errors))
        gate('budget_balance_'+tag,abs(gr+gf-ge)<1e-12*max(1.,abs(gr),abs(gf)))
        gate('threshold_equivalence_'+tag,(ge<0)==(density>threshold),u=source_row['u'])
        gate('density_positive_'+tag,nr>0)
        examples.append(dict(width=source_row['width'],rho=density,q=source_row['q'],u=source_row['u'],
            E=escale,gamma_rho=gr,gamma_feedback=gf,gamma_E=ge,nrho=nr,nz=nz,nE=ne,nK=nk,
            rho_turn=threshold,initial_weighted_source_decreasing=ge<0,initial_curvature_decreasing=nk<0,
            directional_checks=directional))
    end_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    gate('source_unchanged',entry_hash==end_hash)
    failed = [item['name'] for item in checks if not item['passed']]
    feedback = not failed and len(examples)==4 and all(row['gamma_E']<0 for row in examples[-2:])
    curvature_reduction = not failed and len(examples)==4 and all(row['nK']<0 for row in examples[-2:])
    return dict(decision=('EXISTING_ACTION_INITIAL_FEEDBACK_VERIFIED' if feedback else
                         'EXISTING_ACTION_BUDGET_VERIFIED' if not failed else 'SOURCE_BUDGET_CHECK_FAILURE'),
        checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,examples=examples,
        scope=dict(local_budget_derived=not failed,initial_feedback_demonstrated=feedback,
            initial_curvature_reduction=curvature_reduction,persistent_regulation=False,
            fixed_packet_continuation=False,
            existing_action=True,modified_action=False,time_evolution_performed=False,
            global_regularity=False,singularity_removal=False,stability=False,full_RefG_pressure_join=False,
            derivative='n=L^-1 partial_t-v partial_r; normal proper direction, not fixed-r coordinate time',
            interpretation='Instantaneous feedback on four distinct constrained kinetic slices; no later-time, uniform-cap or complete-collapse claim'),
        source_hashes={Path(__file__).name:entry_hash})


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


def collapse_checks(pilot_only=False,origin_audit=False,origin_finer=False,origin_controls=False,paired_origin=False,paired_collapse=False,paired_interior=False,curvature_controls=False,feedback_evolution=False,feedback_controls=False,localization_case=None,localization_controls=False,metric_upgrade=False,metric_controls=False,metric_case=None,metric_case_results=None,positive_metric=None,source_domain=False):
    """Same-action horizon-regular evolution; frozen finite-window decision."""
    import time
    metric_specs = dict(coarse=(.1,120.,.1),middle=(.05,120.,.1),fine=(.025,120.,.1),
                        half_step=(.025,120.,.05),domain=(.025,160.,.1))
    if positive_metric not in (None,'controls','aggregate',*metric_specs):
        raise ValueError('Unknown source-positive metric case')
    positive_mode = positive_metric is not None
    if source_domain and not positive_mode:
        raise ValueError('Source-domain reconstruction requires the positive-metric test ladder')
    if positive_metric in metric_specs:
        metric_case = positive_metric
    metric_controls = metric_controls or positive_metric=='controls'
    metric_endpoint = 28. if positive_mode else 62.75
    if metric_case is not None and metric_case not in metric_specs:
        raise ValueError('Unknown metric-operator case')
    metric_mode = metric_upgrade or metric_controls or metric_case is not None or positive_mode
    if localization_case not in (None,'fine','finer'):
        raise ValueError('Unknown fixed curvature-localization case')
    localization = localization_case is not None or localization_controls or metric_mode
    feedback_evolution = feedback_evolution or localization_case is not None or metric_upgrade or metric_case is not None or positive_metric=='aggregate'
    feedback_controls = feedback_controls or localization_controls or metric_controls
    paired_interior = paired_interior or feedback_evolution
    curvature_controls = curvature_controls or feedback_controls
    paired_origin = paired_origin or paired_collapse or paired_interior or curvature_controls
    origin_audit = origin_audit or paired_origin
    origin_controls = origin_controls or curvature_controls
    hash_paths = tuple(Path(__file__).with_name(name) for name in
        (Path(__file__).name,"population_assembly_initial_data.py","nonlinear_equilibrium_evolution.py"))
    entry_hashes = {path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in hash_paths}
    source,PolarGrid,ref,initial = supercritical_data_checks(return_data=True)
    legacy = ref.load("saturation_staggered_reference",Path(__file__).with_name("population_assembly_initial_data.py"))
    alpha,ell = ref.ALPHA,2.0
    curvature_waves = ('central_Ricci','central_Kretschmann','maximum_abs_Ricci','maximum_abs_Kretschmann')
    curvature_errors = ('curvature_metric_R2_error','curvature_metric_Ricci_error','curvature_metric_K_error')
    feedback_waves = ('central_weighted_source','maximum_weighted_source','central_E_normal_rate')
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
            self.measure_curvature = False
            self.measure_feedback = False

        def field_derivative(self,field):
            return self.engine.derivative(field)

        def source_to_faces(self,mu):
            return self.to_faces(mu)

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
            muf = self.source_to_faces(state[2].real)
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

        def diagnostic_derivative(self,values,odd=False):
            # Fourth-order parity stencil; the outer four cells are excluded
            # from curvature validation, not reflected as physical data.
            ext = np.r_[(-1 if odd else 1)*values[:2][::-1],values]
            out = np.empty_like(values)
            out[:-2] = (ext[:-4]-8*ext[1:-3]+8*ext[3:-1]-ext[4:])/(12*self.h)
            out[-2:] = np.gradient(values,self.h,edge_order=2)[-2:]
            return out

        def metric_curvature_parts(self,state,rhs=None,derivative=None):
            g = self.geometry(state)
            rhs = self.rhs(state) if rhs is None else rhs
            r,L,A,k = self.r,g['L'],g['A'],g['k']
            D = self.diagnostic_derivative if derivative is None else derivative
            H = k*k-g['z']
            Hr = D(H)
            kt = self.cell_k(rhs)
            Ht = 2*k*kt-2*alpha*g['q']**2*rhs[2].real
            Ar,At = r*(2*H+r*Hr),r*r*Ht
            logLr,vr = D(state[4].real),k+r*D(k)
            acc = g['root']*logLr
            Kg = vr+(At/L-g['v']*Ar)/(2*A)+g['v']*logLr
            # These are geometric Hessian/r components, not source substitutes.
            hnn = -kt/L+k*vr-A*logLr/r
            hee = H+r*Hr/2-Kg*k
            hne = r*(Ht/L-k*(2*H+r*Hr))/(2*g['root'])+acc*k
            spatial_R2 = 2*(Kg*Kg+g['v']*D(Kg)-g['root']*D(acc,odd=True)-acc*acc)
            return dict(g=g,Kg=Kg,hnn=hnn,hee=hee,hne=hne,spatial_R2=spatial_R2)

        def curvature_readout(self,state,rhs=None):
            parts = self.metric_curvature_parts(state,rhs)
            g = parts['g']
            rhs = self.rhs(state) if rhs is None else rhs
            P = state[1]
            pt = g['A']*(abs(P)**2-abs(g['D'])**2)/2-g['V']
            curv = saturation_curvature(g['rho'],g['p'],pt,g['root']*g['S'],g['z'],alpha,self.length)
            active = (self.r<=80)&(np.arange(len(self.r))<len(self.r)-4)
            scale_R = max(float(np.max(abs(curv['Ricci_scalar'][active]))),self.length**-2)
            scale_R2 = max(float(np.max(abs(curv['orbit_Ricci'][active]))),self.length**-2)
            scale_K = max(float(np.max(abs(curv['Kretschmann'][active]))),self.length**-4)
            # Off-trajectory directional probes evaluate the metric's second
            # time derivative without changing any production state or guards.
            saved = {key:value for key,value in vars(self).items()
                     if key.startswith(('minimum_stage_','maximum_stage_'))}
            saved_courant = self.engine.maximum_courant
            saved_wave = self.pair.maximum_wave_RK_number
            geometric = []
            try:
                for eps in (1e-4,5e-5):
                    plus = self.metric_curvature_parts(state+eps*rhs)['Kg']
                    minus = self.metric_curvature_parts(state-eps*rhs)['Kg']
                    R2 = parts['spatial_R2']-(plus-minus)/(eps*g['L'])
                    Ricci = R2+2*g['z']-4*(-parts['hnn']+parts['hee'])
                    K = R2*R2+8*(parts['hnn']**2+parts['hee']**2-2*parts['hne']**2)+4*g['z']**2
                    geometric.append((R2,Ricci,K))
            except (FloatingPointError,ValueError) as exc:
                raise FloatingPointError('CURVATURE_PROBE_LIMIT: '+str(exc)) from exc
            finally:
                for key,value in saved.items():
                    setattr(self,key,value)
                self.engine.maximum_courant = saved_courant
                self.pair.maximum_wave_RK_number = saved_wave
            if any(not np.all(np.isfinite(value[active])) for value in
                   (*curv.values(),*geometric[0],*geometric[1])):
                raise FloatingPointError('Nonfinite saturation curvature diagnostic')
            ext0 = lambda x:float((9*x[0]-x[1])/8)
            sup = lambda x:float(np.max(abs(x[active])))
            trapped = active&(g['F']<0)&(g['v']>0)
            out = dict(central_Ricci=ext0(curv['Ricci_scalar']),
                central_Kretschmann=ext0(curv['Kretschmann']),
                maximum_abs_Ricci=sup(curv['Ricci_scalar']),
                maximum_abs_Kretschmann=sup(curv['Kretschmann']),
                minimum_Kretschmann=float(np.min(curv['Kretschmann'][active])),
                trapped_maximum_abs_Kretschmann=float(np.max(abs(curv['Kretschmann'][trapped]))) if np.any(trapped) else 0.,
                curvature_metric_R2_error=sup(geometric[0][0]-curv['orbit_Ricci'])/scale_R2,
                curvature_metric_Ricci_error=sup(geometric[0][1]-curv['Ricci_scalar'])/scale_R,
                curvature_metric_K_error=sup(geometric[0][2]-curv['Kretschmann'])/scale_K,
                curvature_time_probe_error=max(sup(a-b)/sc for a,b,sc in zip(geometric[0],geometric[1],(scale_R2,scale_R,scale_K))))
            return out

        def diagnostic_derivative6(self,values,odd=False):
            """Sixth-order parity derivative for readout controls only."""
            values = np.asarray(values)
            if len(values)<7 or self.h<=0:
                raise ValueError('Sixth-order diagnostic needs seven cells and positive spacing')
            ext = np.r_[(-1 if odd else 1)*values[:3][::-1],values]
            out = np.empty_like(values,dtype=np.result_type(values,float))
            out[:-3] = (-ext[:-6]+9*ext[1:-5]-45*ext[2:-4]+45*ext[4:-2]
                        -9*ext[5:-1]+ext[6:])/(60*self.h)
            out[-3:] = np.gradient(values,self.h,edge_order=2)[-3:]
            return out

        def curvature_localization_readout(self,state,rhs=None):
            """Fixed-state metric-curvature error decomposition; no acceptance substitution.

            D6 and the metric divergence form are independent readout controls.
            K0 uses one action equation and is solely a constraint-error probe.
            """
            if self.length<=0:
                raise ValueError('Curvature localization requires positive saturation length')
            rhs = self.rhs(state) if rhs is None else rhs
            r = self.r
            active = (r<=80)&(np.arange(len(r))<len(r)-6)
            if not np.any(active):
                raise ValueError('No active curvature-localization cells')
            derivatives = {'D4':self.diagnostic_derivative,'D6':self.diagnostic_derivative6}
            parts = {name:self.metric_curvature_parts(state,rhs,derivative=deriv)
                     for name,deriv in derivatives.items()}
            g = parts['D4']['g']
            L,A,v,q,root = g['L'],g['A'],g['v'],g['q'],g['root']
            pt = A*(abs(state[1])**2-abs(g['D'])**2)/2-g['V']
            action = saturation_curvature(g['rho'],g['p'],pt,root*g['S'],g['z'],alpha,self.length)['orbit_Ricci']
            sup = lambda x:float(np.max(abs(x[active])))
            scale = max(sup(action),self.length**-2)
            At = r*r*(2*g['k']*self.cell_k(rhs)-2*alpha*q*q*rhs[2].real)
            def k0(part,deriv):
                gg = part['g']
                return gg['k']+r*deriv(gg['k'])-alpha*r*gg['q']**2*gg['S']
            saved = {key:value for key,value in vars(self).items()
                     if key.startswith(('minimum_stage_','maximum_stage_'))}
            saved_courant = self.engine.maximum_courant
            saved_wave = self.pair.maximum_wave_RK_number
            variants,kt_rates,k0_rates = {},{},{}
            try:
                for name,deriv in derivatives.items():
                    base = parts[name]
                    Kg = base['Kg']
                    acc = root*deriv(state[4].real)
                    variants[name+'_expanded'],variants[name+'_flux'] = [],[]
                    kt_rates[name],k0_rates[name] = [],[]
                    for eps in (1e-4,5e-5):
                        plus = self.metric_curvature_parts(state+eps*rhs,derivative=deriv)
                        minus = self.metric_curvature_parts(state-eps*rhs,derivative=deriv)
                        Kt = (plus['Kg']-minus['Kg'])/(2*eps)
                        K0t = (k0(plus,deriv)-k0(minus,deriv))/(2*eps)
                        expanded = base['spatial_R2']-2*Kt/L
                        flux = -2*root/L*(Kt/root-Kg*At/(2*A*root)
                            +deriv(L*acc-L*v*Kg/root,odd=True))
                        variants[name+'_expanded'].append(expanded)
                        variants[name+'_flux'].append(flux)
                        kt_rates[name].append(Kt)
                        k0_rates[name].append(K0t)
            except (FloatingPointError,ValueError) as exc:
                raise FloatingPointError('CURVATURE_LOCALIZATION_PROBE_LIMIT: '+str(exc)) from exc
            finally:
                for key,value in saved.items():
                    setattr(self,key,value)
                self.engine.maximum_courant = saved_courant
                self.pair.maximum_wave_RK_number = saved_wave
            D = derivatives['D4']
            Kg,K0 = parts['D4']['Kg'],k0(parts['D4'],D)
            delta = Kg-K0
            deltat = kt_rates['D4'][0]-k0_rates['D4'][0]
            amplification = 2*(2*K0*delta+delta*delta-deltat/L+v*D(delta))
            acc = root*D(state[4].real)
            K0_curvature = 2*(K0*K0-k0_rates['D4'][0]/L+v*D(K0)-root*D(acc,odd=True)-acc*acc)
            H = g['k']**2-g['z']
            Ar = r*(2*H+r*D(H))
            constraint = At/L-v*Ar+2*v*A*D(state[4].real)+2*alpha*q*q*r*A*g['S']
            constraint_delta = constraint/(2*A)
            terms = dict(extrinsic_square=2*Kg*Kg,time_derivative=-2*kt_rates['D4'][0]/L,
                radial_advection=2*v*D(Kg),acceleration_derivative=-2*root*D(acc,odd=True),
                acceleration_square=-2*acc*acc)
            baseline = variants['D4_expanded'][0]
            residual = baseline-action
            remaining = residual-amplification
            arrays = [action,At,Kg,K0,delta,deltat,amplification,K0_curvature,constraint_delta,remaining,
                      *terms.values(),*(x for series in variants.values() for x in series)]
            if any(not np.all(np.isfinite(value[active])) for value in arrays):
                raise FloatingPointError('Nonfinite curvature-localization diagnostic')
            ids = np.flatnonzero(active)
            j = int(ids[np.argmax(abs(residual[active]))])
            def local_row(index):
                row_terms = {name:float(value[index]) for name,value in terms.items()}
                local_scale = max(abs(float(action[index])),abs(float(baseline[index])),self.length**-2)
                return dict(index=int(index),r=float(r[index]),action_R2=float(action[index]),
                    metric_R2=float(baseline[index]),signed_residual=float(residual[index]),
                    R2_terms=row_terms,cancellation_ratio=sum(abs(x) for x in row_terms.values())/local_scale,
                    L=float(L[index]),A=float(A[index]),q=float(q[index]),
                    constraint_delta=float(constraint_delta[index]),delta_K=float(delta[index]),
                    constraint_amplification=float(amplification[index]),remaining_residual=float(remaining[index]),
                    D6_metric_R2=float(variants['D6_expanded'][0][index]),
                    flux_metric_R2=float(variants['D4_flux'][0][index]))
            local_lo = max(int(ids[0]),j-3)
            local_hi = min(int(ids[-1])+1,local_lo+7)
            local_lo = max(int(ids[0]),local_hi-7)
            local_indices = [i for i in range(local_lo,local_hi) if active[i]]
            return dict(R2_scale=scale,
                variant_errors={name:sup(values[0]-action)/scale for name,values in variants.items()},
                D6_D4_sensitivity=sup(variants['D6_expanded'][0]-baseline)/scale,
                flux_D4_sensitivity=sup(variants['D4_flux'][0]-baseline)/scale,
                D6_flux_D6_sensitivity=sup(variants['D6_flux'][0]-variants['D6_expanded'][0])/scale,
                time_probe_sensitivity={name:sup(values[0]-values[1])/scale for name,values in variants.items()},
                constraint_amplification_norm=sup(amplification)/scale,
                residual_after_constraint_subtraction=sup(remaining)/scale,
                constraint_delta_identity_error=sup(delta-constraint_delta),
                constraint_curvature_identity_error=sup(baseline-K0_curvature-amplification)/scale,
                worst=local_row(j),local_rows=[local_row(i) for i in local_indices],
                interpretation='Fixed-state readout controls only; K0 and constraint subtraction do not replace the independent metric gate')

        def feedback_readout(self,state,rhs=None):
            """Nonlogarithmic local-source budget along n=L^-1 dt-v dr.

            The direct rate differentiates the actual semidiscrete RHS;
            the three budget terms use the continuum energy/mass equations.
            """
            rhs = self.rhs(state) if rhs is None else rhs
            parts = self.metric_curvature_parts(state,rhs)
            g = parts['g']
            r,L,A,v,q = self.r,g['L'],g['A'],g['v'],g['q']
            deriv = self.diagnostic_derivative
            field,P = state[:2]
            mu = state[2].real
            D,Ddot = g['D'],self.field_derivative(rhs[0])
            vdot = r*self.cell_k(rhs)
            Adot = -2*alpha*r*r*q*q*rhs[2].real+2*v*vdot
            force = (1-abs(field)**2+abs(field)**4/4)*field
            rhodot = Adot*(abs(P)**2+abs(D)**2)/2+A*np.real(
                np.conjugate(P)*rhs[1]+np.conjugate(D)*Ddot)+np.real(np.conjugate(force)*rhs[0])
            rho,pr = g['rho'],g['p']
            pt = A*(abs(P)**2-abs(D)**2)/2-g['V']
            J = g['root']*g['S']
            pref = alpha*self.length**2*q**1.5
            E = pref*rho
            Et = pref*(rhodot-3*alpha*self.length**2*q*rho*rhs[2].real)
            nE = Et/L-v*deriv(E)
            nrho = rhodot/L-v*deriv(rho)
            acc = g['root']*deriv(state[4].real)
            flux = pref*(g['root']*deriv(J,odd=True)+2*(acc+g['root']/r)*J)
            compression = pref*(parts['Kg']*(rho+pr)+2*g['k']*(rho+pt))
            nmu = g['k']*(3*mu+pr)+A*g['S']/r
            response = -pref*3*alpha*self.length**2*q*rho*nmu
            budget = flux+compression+response
            curv = saturation_curvature(rho,pr,pt,J,g['z'],alpha,self.length)
            active = (r<=80)&(np.arange(len(r))<len(r)-4)
            arrays = (E,Et,nE,nrho,rhodot,flux,compression,response,budget,
                      rho,pr,pt,J,acc,parts['Kg'],nmu,curv['Kretschmann'])
            if any(not np.all(np.isfinite(value[active])) for value in arrays):
                raise FloatingPointError('Nonfinite local-source feedback diagnostic')
            ids = np.flatnonzero(active)
            j = int(ids[np.argmax(abs(curv['Kretschmann'][active]))])
            trapped = active&(g['F']<0)&(v>0)
            ext0 = lambda x:float((9*x[0]-x[1])/8)
            sup = lambda x:float(np.max(abs(x[active])))
            scale = max(sup(abs(flux)+abs(compression)+abs(response)),1/self.length)
            return dict(feedback_budget_error=sup(nE-budget)/scale,
                central_weighted_source=ext0(E),maximum_weighted_source=float(np.max(E[active])),
                central_E_flux=ext0(flux),central_E_compression=ext0(compression),
                central_E_response=ext0(response),central_E_normal_rate=ext0(nE),
                central_density_normal_rate=ext0(nrho),
                K_peak_radius=float(r[j]),K_peak_rho=float(rho[j]),K_peak_q=float(q[j]),
                K_peak_E=float(E[j]),K_peak_E_flux=float(flux[j]),
                K_peak_E_compression=float(compression[j]),K_peak_E_response=float(response[j]),
                K_peak_E_normal_rate=float(nE[j]),K_peak_density_normal_rate=float(nrho[j]),
                trapped_maximum_weighted_source=float(np.max(E[trapped])) if np.any(trapped) else 0.)

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
            row = dict(t=float(t),central_proper_time=float(state[5,0].real),
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
            if self.measure_curvature:
                row.update(self.curvature_readout(state,rhs))
            if self.measure_feedback:
                row.update(self.feedback_readout(state,rhs))
            return row

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

    class MetricUpgradeClock(PairedSaturationClock):
        """Fourth-order centre-safe metric block; unchanged paired matter/action.

        The outermost six cell/face rows retain the legacy numerical closure.
        Interior gauge gradient/divergence form the existing weighted-adjoint
        G6 pair. The fixed outer closure is not reflected through nonzero v(R).
        """
        metric_outer_rows = 6

        def __init__(self,radius,h,length=ell):
            super().__init__(radius,h,length)
            if len(self.r)<8:
                raise ValueError('Metric upgrade needs at least eight cells')

        def cell_k(self,state):
            out = legacy.StaggeredClockGrid.cell_k(self,state)
            vf = np.r_[0.,state[3].real]
            ext = np.r_[-vf[1],vf]
            interpolated = (-ext[:-3]+9*ext[1:-2]+9*ext[2:-1]-ext[3:])/16
            interior = len(self.r)-self.metric_outer_rows
            out[:interior] = interpolated[:interior]/self.r[:interior]
            return out

        def to_faces(self,values):
            out = legacy.StaggeredClockGrid.to_faces(self,values)
            out[:-self.metric_outer_rows] = (self.pair.I@values)[1:-self.metric_outer_rows]
            return out

        def face_gradient(self,values):
            out = legacy.StaggeredClockGrid.face_gradient(self,values)
            out[:-self.metric_outer_rows] = (self.pair.G@values)[1:-self.metric_outer_rows]
            return out

        def divergence(self,velocity):
            out = legacy.StaggeredClockGrid.divergence(self,velocity)
            full_velocity = np.r_[0.,velocity]
            adjoint = -(self.pair.GT@(self.pair.face_measure*full_velocity))/self.r**2
            out[:-self.metric_outer_rows] = adjoint[:-self.metric_outer_rows]
            return out

        def metric_cell_derivative(self,values):
            out = self.engine.derivative(values)
            out[:-self.metric_outer_rows] = (self.pair.E@values)[:-self.metric_outer_rows]
            return out

        def face_velocity_derivative(self,velocity):
            out = np.r_[(np.r_[velocity[1:],0.]-np.r_[0.,velocity[:-1]])[:-1]/(2*self.h),
                (3*velocity[-1]-4*velocity[-2]+velocity[-3])/(2*self.h)]
            ext = np.r_[-velocity[0],0.,velocity]
            fourth = (ext[:-4]-8*ext[1:-3]+8*ext[3:-1]-ext[4:])/(12*self.h)
            interior = len(self.r)-self.metric_outer_rows
            out[:interior] = fourth[:interior]
            return out

        def rhs(self,state):
            # super retains the scalar pair, physical mass law and all guards;
            # its geometry calls use this class's metric reconstruction.
            out = super().rhs(state)
            g = self.geometry(state)
            r,rf = self.r,self.engine.edges[1:]
            vf,logL = state[3].real,state[4].real
            muf = self.source_to_faces(state[2].real)
            qf = 1/(1+2*alpha*self.length**2*muf)
            zf = 2*alpha*muf*qf
            Lf = np.exp(self.to_faces(logL))
            Af = 1-rf*rf*zf+vf*vf
            out[3] = (Lf*vf*self.face_velocity_derivative(vf)
                +Lf*rf*(zf*(1-3*self.length**2*zf)/2+alpha*qf*qf*self.to_faces(g['p']))
                -Lf*Af*self.face_gradient(logL))
            out[4] = (g['beta']*self.metric_cell_derivative(logL)
                -g['L']*(self.divergence(vf)-alpha*r*g['q']**2*g['S']))
            if not np.all(np.isfinite(out)):
                raise FloatingPointError('Nonfinite upgraded metric RHS')
            return out

    class PositiveMetricClock(MetricUpgradeClock):
        """Limit reconstructed source faces, retaining the same primary state.

        For nonnegative low-order L and negative high-order H, the maximal
        admissible convex blend has theta=L/(L-H) and face value zero.
        On admissible input this is exactly max(H,0), applied to source
        reconstruction only; lapse and signed stresses keep their stencils.
        """
        def __init__(self,radius,h,length=ell):
            super().__init__(radius,h,length)
            self.maximum_stage_limited_faces = 0
            self.minimum_stage_raw_source_face = math.inf
            self.maximum_stage_source_face_change = 0.0
            self.domain_failure = None

        def source_to_faces(self,mu):
            raw = self.to_faces(mu)
            low = np.r_[(mu[:-1]+mu[1:])/2,mu[-1]]
            limited = (raw<0)&(low>=0)
            out = raw.copy()
            # Evaluate the exact admissible endpoint without cancellation.
            out[limited] = 0.0
            self.maximum_stage_limited_faces = max(self.maximum_stage_limited_faces,int(np.sum(limited)))
            self.minimum_stage_raw_source_face = min(self.minimum_stage_raw_source_face,float(np.min(raw)))
            self.maximum_stage_source_face_change = max(self.maximum_stage_source_face_change,float(np.max(abs(out-raw))))
            return out

        def action_domain(self,mu,q,z):
            try:
                return super().action_domain(mu,q,z)
            except FloatingPointError as exc:
                import inspect
                u = self.length**2*np.asarray(z)
                if self.length and np.min(u)<-100*np.finfo(float).eps:
                    j = int(np.argmin(u))
                elif not np.all(np.isfinite(u)):
                    j = int(np.flatnonzero(~np.isfinite(u))[0])
                else:
                    j = int(np.argmax(u))
                stack = inspect.stack(context=0)
                try:
                    caller = stack[1].function if len(stack)>1 else 'unknown'
                    site = 'cell' if caller=='geometry' else 'face' if caller=='rhs' else 'unknown'
                    probe_steps = [float(frame.frame.f_locals['eps']) for frame in stack[1:]
                                   if frame.function in ('curvature_readout','curvature_localization_readout')
                                   and 'eps' in frame.frame.f_locals]
                    rk_stages = [1+sum(name in frame.frame.f_locals for name in ('a','b','c'))
                                 for frame in stack[1:] if frame.function=='clock_rk4']
                    radius = float((self.r if site=='cell' else self.engine.edges[1:])[j]) if site!='unknown' else None
                    value = lambda x:float(np.asarray(x)[j]) if np.isfinite(np.asarray(x)[j]) else str(np.asarray(x)[j])
                    self.domain_failure = dict(error=str(exc),site=site,index=j,radius=radius,
                        mu=value(mu),u=value(u),q=value(q),from_curvature_probe=bool(probe_steps),caller=caller,
                        probe_eps=probe_steps[0] if probe_steps else None,
                        rk_substage=rk_stages[0] if rk_stages else None)
                    caller_state = stack[1].frame.f_locals.get('state') if len(stack)>1 else None
                    if caller_state is not None and site in ('cell','face'):
                        primary = caller_state[2].real
                        left,right = (j-2,j+3) if site=='cell' else (j-1,j+3)
                        self.domain_failure['nearby_primary_mu'] = [
                            dict(index=i,radius=float(self.r[i]),mu=float(primary[i]))
                            for i in range(max(0,left),min(len(primary),right))]
                        if site=='face':
                            self.domain_failure['raw_source_face'] = value(self.to_faces(primary))
                            low = (primary[j]+primary[j+1])/2 if j<len(primary)-1 else primary[-1]
                            self.domain_failure['low_order_source_face'] = float(low)
                finally:
                    del stack
                raise

    class AdmissibleMetricClock(PositiveMetricClock):
        """Keep accepted source faces; reconstruct rejected negative-u faces.

        H is retained exactly whenever it is numerically admissible. A
        finite H on the positive-q branch with u below the existing guard
        uses the adjacent mean L only when L passes that same domain test.
        The physical state, signed stresses and original guards are intact.
        """
        def __init__(self,radius,h,length=ell):
            super().__init__(radius,h,length)
            self.maximum_stage_domain_fallback_faces = 0

        def source_domain_values(self,mu):
            """Use the production order q, then z, then u, including ell=0."""
            mu = np.asarray(mu)
            with np.errstate(divide='ignore',invalid='ignore',over='ignore'):
                q = 1/(1+2*alpha*self.length**2*mu)
                z = 2*alpha*mu*q
                u = self.length**2*z
            return q,z,u

        def source_domain_accepts(self,mu):
            """Scalar bool or elementwise mask for the existing source domain."""
            q,z,u = self.source_domain_values(mu)
            accepted = (np.isfinite(mu)&np.isfinite(q)&np.isfinite(z)&np.isfinite(u)
                        &(q>0)&(u<1))
            if self.length:
                accepted = accepted&(u>=-100*np.finfo(float).eps)
            return bool(accepted) if np.ndim(accepted)==0 else accepted

        def source_to_faces(self,mu):
            raw = self.to_faces(mu)
            low = np.r_[(mu[:-1]+mu[1:])/2,mu[-1]]
            q,z,u = self.source_domain_values(raw)
            trigger = (np.isfinite(raw)&np.isfinite(q)&np.isfinite(z)&np.isfinite(u)
                       &(q>0)&(u<-100*np.finfo(float).eps))
            if not self.length:
                trigger = np.zeros_like(trigger,dtype=bool)
            replaced = trigger&self.source_domain_accepts(low)
            out = raw.copy()
            out[replaced] = low[replaced]
            count = int(np.sum(replaced))
            change = float(np.max(abs(out[replaced]-raw[replaced]))) if count else 0.0
            self.maximum_stage_limited_faces = max(self.maximum_stage_limited_faces,count)
            self.maximum_stage_domain_fallback_faces = max(self.maximum_stage_domain_fallback_faces,count)
            self.minimum_stage_raw_source_face = min(self.minimum_stage_raw_source_face,float(np.min(raw)))
            self.maximum_stage_source_face_change = max(self.maximum_stage_source_face_change,change)
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
    if paired_interior or curvature_controls:
        checks.extend(saturation_curvature_checks())
        errors = []
        for h in (.1,.05,.025):
            grid = PairedSaturationClock(4,h)
            r = grid.r
            k0 = math.sqrt(2*alpha/(9+2*alpha*ell**2))
            state = np.zeros((6,len(r)),complex)
            state[0],state[2],state[3],state[4] = math.sqrt(2),1/9,k0*grid.engine.edges[1:],math.log(.8)
            row = grid.curvature_readout(state)
            errors.append(max(abs(row['central_Ricci']-12*k0*k0),
                              abs(row['central_Kretschmann']-24*k0**4)))
            test('curvature_constant_core_'+str(h),errors[-1]<1e-10 and
                 max(row[key] for key in ('curvature_metric_R2_error','curvature_metric_Ricci_error','curvature_metric_K_error','curvature_time_probe_error'))<1e-7,
                 readout=row)
            if feedback_evolution or feedback_controls:
                budget = grid.feedback_readout(state)
                core_q = 1/(1+2*alpha*ell**2/9)
                expected_E = alpha*ell**2*core_q**1.5/3
                test('feedback_constant_core_'+str(h),
                     budget['feedback_budget_error']<1e-10 and
                     abs(budget['central_weighted_source']-expected_E)<1e-12 and
                     max(abs(budget[key]) for key in ('central_E_flux','central_E_compression',
                         'central_E_response','central_E_normal_rate'))<1e-10,readout=budget)
                empty = grid.feedback_readout(np.zeros_like(state))
                test('feedback_empty_'+str(h),max(abs(empty[key]) for key in
                     ('feedback_budget_error',)+feedback_waves)<1e-12)
            # Direct static Hayward metric in a horizon-regular flat-slice chart.
            mass = source['parameters']['target_mass']
            rf = grid.engine.edges[1:]
            state[:] = 0
            state[2] = mass/r**3
            state[3] = rf*np.sqrt(2*alpha*mass/(rf**3+2*alpha*ell**2*mass))
            parts = grid.metric_curvature_parts(state,np.zeros_like(state))
            vacuum = saturation_curvature(0.,0.,0.,0.,parts['g']['z'],alpha,ell)
            active = (r>=.5)&(r<=3.)
            error = float(np.max(abs((parts['spatial_R2']-vacuum['orbit_Ricci'])[active])))
            test('curvature_static_metric_'+str(h),error<.01,error=error)
            errors.append(error)
        test('curvature_static_metric_refines',errors[-1]<.6*errors[-3] and errors[-3]<.6*errors[-5],errors=errors[1::2])
    if localization:
        flux_errors = []
        for h in (.1,.05,.025):
            grid = PairedSaturationClock(4,h)
            r = grid.r
            errors = []
            for degree in range(7):
                expected = np.zeros_like(r) if degree==0 else degree*r**(degree-1)
                actual = grid.diagnostic_derivative6(r**degree,odd=bool(degree%2))
                errors.append(float(np.max(abs(actual[:-6]-expected[:-6]))/max(np.max(abs(expected[:-6])),1.)))
            test('localization_D6_parity_polynomials_'+str(h),max(errors)<1e-9,errors=errors)
            state = np.zeros((6,len(r)),complex)
            k0 = math.sqrt(2*alpha/(9+2*alpha*ell**2))
            state[0],state[2],state[3],state[4] = math.sqrt(2),1/9,k0*grid.engine.edges[1:],math.log(.8)
            rhs = grid.rhs(state)
            saved = {key:value for key,value in vars(grid).items() if key.startswith(('minimum_stage_','maximum_stage_'))}
            saved.update(Courant=grid.engine.maximum_courant,wave=grid.pair.maximum_wave_RK_number)
            row = grid.curvature_localization_readout(state,rhs)
            after = {key:value for key,value in vars(grid).items() if key.startswith(('minimum_stage_','maximum_stage_'))}
            after.update(Courant=grid.engine.maximum_courant,wave=grid.pair.maximum_wave_RK_number)
            test('localization_guard_restore_'+str(h),saved==after)
            test('localization_core_metric_variants_'+str(h),max(row['variant_errors'].values())<1e-7,readout=row)
            state[:] = 0
            state[0] = .2*np.exp(-r*r)*(1+.2j)
            state[1] = (.05+.1j)*np.exp(-r*r)
            state[2] = .01*np.exp(-r*r/4)
            state[3] = .01*grid.engine.edges[1:]
            state[4] = -.03*np.exp(-r*r)
            original_state = state.copy()
            row = grid.curvature_localization_readout(state)
            baseline = grid.curvature_readout(state)
            test('localization_nontrivial_defect_'+str(h),row['constraint_amplification_norm']>1e-8 and np.array_equal(state,original_state),
                 amplification=row['constraint_amplification_norm'])
            test('localization_original_D4_'+str(h),abs(row['variant_errors']['D4_expanded']-baseline['curvature_metric_R2_error'])<1e-12)
            test('localization_constraint_identities_'+str(h),max(row['constraint_delta_identity_error'],row['constraint_curvature_identity_error'])<1e-8)
            test('localization_manufactured_probe_'+str(h),max(row['time_probe_sensitivity'].values())<1e-7)
            flux_errors.append(row['flux_D4_sensitivity'])
        test('localization_metric_divergence_refines',flux_errors[-1]<.2*flux_errors[-2] and flux_errors[-2]<.2*flux_errors[0],errors=flux_errors)
    if metric_mode:
        metric_factory = AdmissibleMetricClock if source_domain else PositiveMetricClock if positive_mode else MetricUpgradeClock
        manufactured_errors = []
        for h in (.1,.05,.025):
            grid = metric_factory(4,h)
            r,rf = grid.r,grid.engine.edges[1:]
            inside = slice(None,-9)
            state = np.zeros((6,len(r)),complex)
            polynomial_errors = []
            for degree in (1,3):
                state[3] = rf**degree
                polynomial_errors.extend((float(max(abs(grid.cell_k(state)[inside]-r[inside]**(degree-1)))),
                    float(max(abs(grid.divergence(rf**degree)[inside]-(degree+2)*r[inside]**(degree-1)))),
                    float(max(abs(grid.face_velocity_derivative(rf**degree)[inside]-degree*rf[inside]**(degree-1))))))
            polynomial_errors.extend((float(max(abs(grid.to_faces(r*r)[inside]-rf[inside]**2))),
                float(max(abs(grid.face_gradient(r**4)[inside]-4*rf[inside]**3))),
                float(max(abs(grid.metric_cell_derivative(r**4)[inside]-4*r[inside]**3)))))
            test('metric_polynomial_centre_'+str(h),max(polynomial_errors)<1e-9,errors=polynomial_errors)
            old = PairedSaturationClock(4,h)
            boundary_errors = [float(max(abs(getattr(grid,key)(r*r)[-6:]-getattr(old,key)(r*r)[-6:])))
                for key in ('to_faces','face_gradient')]
            boundary_errors.append(float(max(abs(grid.divergence(rf**3)[-6:]-old.divergence(rf**3)[-6:]))))
            test('metric_legacy_outer_closure_'+str(h),max(boundary_errors)==0.)
            rng = np.random.default_rng(9218)
            x,vf = rng.normal(size=(2,len(r)))
            x[-9:],vf[-9:] = 0.,0.
            terms = (h*r*r*x*grid.divergence(vf),h*grid.pair.face_measure[1:]*grid.face_gradient(x)*vf)
            adjoint_error = abs(sum(float(np.sum(x)) for x in terms))/max(sum(float(np.sum(abs(x))) for x in terms),1e-30)
            test('metric_compact_gauge_adjoint_'+str(h),adjoint_error<1e-13,error=adjoint_error)
            state[:] = 0
            k0 = math.sqrt(2*alpha/(9+2*alpha*ell**2))
            state[0],state[2],state[3],state[4] = math.sqrt(2),1/9,k0*rf,math.log(.7)
            row = grid.curvature_readout(state)
            budget = grid.feedback_readout(state)
            test('metric_constant_core_readout_'+str(h),max(row[key] for key in curvature_errors)<1e-7 and budget['feedback_budget_error']<1e-10)
            for _ in range(40):
                state = legacy.clock_rk4(grid,state,.025)
            core_error = max(float(max(abs(grid.cell_k(state)-k0))),
                abs(float(np.exp(state[4,0].real))-.7/(1+3*k0*.7)),
                abs(float(state[5,0].real)-math.log1p(3*k0*.7)/(3*k0)))
            test('metric_constant_core_clock_'+str(h),core_error<1e-8,error=core_error)
            def analytic(x):
                field = .2*(1+.2j)*np.exp(-x*x)
                P = (.05+.1j)*np.exp(-x*x)
                grad = -2*x*field
                mu = .01*np.exp(-x*x/4)
                v = .01*x+.002*x**3
                logL = -.03*np.exp(-x*x)
                q = 1/(1+2*alpha*ell**2*mu)
                z = 2*alpha*mu*q
                A = 1-x*x*z+v*v
                V = abs(field)**2/2-abs(field)**4/4+abs(field)**6/24
                p = A*(abs(P)**2+abs(grad)**2)/2-V
                S = np.sqrt(A)*np.real(np.conjugate(P)*grad)
                L = np.exp(logL)
                logLr = .06*x*np.exp(-x*x)
                vt = L*v*(.01+.006*x*x)+L*x*(z*(1-3*ell**2*z)/2+alpha*q*q*p)-L*A*logLr
                lt = L*v*logLr-L*(.03+.01*x*x-alpha*x*q*q*S)
                mut = L*((v/x)*A*(abs(P)**2+abs(grad)**2)+(A+v*v)*S/x)
                return field,P,mu,v,logL,vt,lt,mut
            field,P,mu,v,logL,vt,lt,mut = analytic(r)
            face_v,face_vt = analytic(rf)[3],analytic(rf)[5]
            state[:] = 0
            state[0],state[1],state[2],state[3],state[4] = field,P,mu,face_v,logL
            rhs = grid.rhs(state)
            active = r<2
            error = max(float(max(abs(rhs[2].real[active]-mut[active]))),
                float(max(abs(rhs[3].real[active]-face_vt[active]))),float(max(abs(rhs[4].real[active]-lt[active]))))
            manufactured_errors.append(error)
            charge = float(np.sum(grid.pair.weights*np.imag(np.conjugate(rhs[0])*state[1]+np.conjugate(state[0])*rhs[1])))
            test('metric_paired_charge_preserved_'+str(h),abs(charge)<1e-12,charge_rate=charge)
            if positive_mode:
                baseline = MetricUpgradeClock(4,h).rhs(state.copy())
                test('positive_inactive_full_RHS_unchanged_'+str(h),np.array_equal(rhs,baseline))
        test('metric_manufactured_RHS_refines',manufactured_errors[-1]<.2*manufactured_errors[-2] and
             manufactured_errors[-2]<.2*manufactured_errors[0],errors=manufactured_errors)
        for h in (.1,.05):
            energies = {}
            for tag,factory in (('legacy',PairedSaturationClock),('upgraded',metric_factory)):
                grid = factory(4,h)
                r,rf = grid.r,grid.engine.edges[1:]
                eye = np.eye(len(r))
                G = np.column_stack([grid.face_gradient(row) for row in eye])
                D = np.column_stack([grid.divergence(row) for row in eye])
                chain = max(float(max(abs(G@np.ones(len(r))))),float(max(abs(G@(r*r)-2*rf))),float(max(abs(D@rf-3))))
                test('metric_gauge_zero_chain_'+tag+'_'+str(h),chain<1e-9,error=chain)
                eigen = np.linalg.eigvals(D@G)*h*h
                order = np.argsort(abs(eigen))
                small,bulk = eigen[order[:2]],eigen[order[2:]]
                test('metric_gauge_nonzero_spectrum_'+tag+'_'+str(h),max(abs(small))<1e-6 and
                     max(bulk.real)<1e-8 and max(abs(bulk.imag))<1e-8,
                     zero_sector=[[float(x.real),float(x.imag)] for x in small],largest_bulk_real=float(max(bulk.real)))
                pulse = np.zeros(len(r))
                pulse[r<1] = np.exp(-1/(1-r[r<1]**2))
                y = np.array([pulse,np.zeros(len(r))])
                def linear_rhs(y):
                    return np.array([-D@y[1],-G@y[0]])
                def energy(y):
                    return float(h*np.sum(r*r*y[0]**2+grid.pair.face_measure[1:]*y[1]**2))
                initial_energy,largest,at_two = energy(y),1.,None
                dt = .1*h
                for step in range(round(4/dt)):
                    a0 = linear_rhs(y); b0 = linear_rhs(y+dt*a0/2)
                    c0 = linear_rhs(y+dt*b0/2); d0 = linear_rhs(y+dt*c0)
                    y = y+dt*(a0+2*b0+2*c0+d0)/6
                    ratio = energy(y)/initial_energy
                    largest = max(largest,ratio)
                    if step+1==round(2/dt):
                        at_two = ratio
                energies[tag] = dict(maximum=largest,at_two=at_two,finite=bool(np.all(np.isfinite(y))))
            test('metric_linear_boundary_response_'+str(h),all(x['finite'] for x in energies.values()) and
                 energies['upgraded']['maximum']<=1.05*energies['legacy']['maximum'] and abs(energies['upgraded']['at_two']-1)<1e-5,
                 energies=energies)
        if positive_mode:
            smooth_errors = []
            for h in (.1,.05,.025):
                grid = metric_factory(4,h)
                r,rf = grid.r,grid.engine.edges[1:]
                mu = 2+np.exp(-r*r)
                before = mu.copy()
                face = grid.source_to_faces(mu)
                active = rf<2
                smooth_errors.append(float(max(abs(face[active]-(2+np.exp(-rf[active]**2))))))
                test('positive_smooth_raw_and_state_'+str(h),np.array_equal(face,grid.to_faces(mu)) and np.array_equal(mu,before))
                zero = np.zeros_like(r)
                test('positive_empty_cavity_'+str(h),np.array_equal(grid.source_to_faces(zero),zero))
                steep = zero.copy(); steep[len(r)//2:] = 1.; steep[-2:] = (5.,1.)
                old_steep = steep.copy()
                selected,raw = grid.source_to_faces(steep),grid.to_faces(steep)
                test('positive_steep_and_outer_face_'+str(h),min(selected)>=0 and raw[-1]<0 and
                     selected[-1]==(1 if source_domain else 0) and np.array_equal(steep,old_steep) and np.array_equal(selected[raw>=0],raw[raw>=0]))
                signed = np.sin(2*r)-.3
                test('positive_signed_interpolation_unchanged_'+str(h),
                     np.array_equal(grid.to_faces(signed),MetricUpgradeClock(4,h).to_faces(signed)))
                bad = np.zeros((6,len(r)),complex); bad[2] = .01; bad[2,3] = -.001
                rejected = False
                try:
                    grid.rhs(bad)
                except FloatingPointError as exc:
                    rejected = 'resolved negative u' in str(exc)
                test('positive_negative_cell_still_rejected_'+str(h),rejected and grid.domain_failure['site']=='cell' and
                     grid.domain_failure['index']==3 and bad[2,3]==-.001)
                bad[2,3] = complex(float('nan'),0)
                rejected = False
                try:
                    grid.rhs(bad)
                except FloatingPointError as exc:
                    rejected = 'Nonfinite saturation evolution state' in str(exc)
                test('positive_nonfinite_cell_still_rejected_'+str(h),rejected)
            test('positive_smooth_fourth_order',smooth_errors[1]<.2*smooth_errors[0] and
                 smooth_errors[2]<.2*smooth_errors[1],errors=smooth_errors)
        if source_domain:
            domain_grid = AdmissibleMetricClock(24.,.1)
            strict_grid = PositiveMetricClock(24.,.1)
            guard_grid = SaturationClock(4.,.1)
            def original_source_guard(value):
                values = np.asarray([value],dtype=float)
                with np.errstate(divide='ignore',invalid='ignore',over='ignore'):
                    q0 = 1/(1+2*alpha*ell**2*values)
                    z0 = 2*alpha*values*q0
                # These checks are made before action_domain in production.
                if not np.all(np.isfinite(values)) or not np.all(np.isfinite(q0)) or np.min(q0)<=0:
                    return False
                try:
                    guard_grid.action_domain(values,q0,z0)
                except FloatingPointError:
                    return False
                return True
            primary = np.zeros_like(domain_grid.r)
            primary[200:204] = (1.165691706620534e-19,-4.378100645570907e-17,
                               -1.3239812564870792e-15,1.1123380066336225e-12)
            saved_primary = primary.copy()
            j = 201
            raw = domain_grid.to_faces(primary)
            selected = domain_grid.source_to_faces(primary)
            strict = strict_grid.source_to_faces(primary)
            low = float((primary[j]+primary[j+1])/2)
            test('source_domain_saved_RK3_stencil',abs(raw[j]-(-7.029049897307989e-14))<1e-28 and
                 abs(low-(-6.838811314713941e-16))<1e-30 and strict[j]==raw[j] and selected[j]==low and
                 not original_source_guard(strict[j]) and original_source_guard(selected[j]) and
                 all(original_source_guard(x) for x in primary[200:204]),
                 raw=float(raw[j]),low=low,selected=float(selected[j]),strict=float(strict[j]))
            test('source_domain_saved_primary_unchanged',np.array_equal(primary,saved_primary))
            tiny = np.full_like(primary,-1e-16)
            tiny_raw = domain_grid.to_faces(tiny)
            test('source_domain_accepted_negative_retained',
                 np.array_equal(domain_grid.source_to_faces(tiny),tiny_raw) and
                 all(original_source_guard(x) for x in tiny_raw))
            invalid = np.full_like(primary,-1e-10)
            invalid_raw = domain_grid.to_faces(invalid)
            test('source_domain_two_invalid_endpoints_unrepaired',
                 np.array_equal(domain_grid.source_to_faces(invalid),invalid_raw) and
                 not original_source_guard(float(invalid_raw[j])))
            edge = np.zeros_like(primary)
            edge[-2:] = (1e-12,-1e-16)
            edge_before = edge.copy()
            edge_raw,edge_selected = domain_grid.to_faces(edge),domain_grid.source_to_faces(edge)
            test('source_domain_outer_accepted_endpoint',not original_source_guard(float(edge_raw[-1])) and
                 edge_selected[-1]==edge[-1] and original_source_guard(float(edge_selected[-1])) and
                 np.array_equal(edge,edge_before),raw=float(edge_raw[-1]),selected=float(edge_selected[-1]))
            delta = 100*np.finfo(float).eps
            boundary = -delta/(2*alpha*ell**2*(1+delta))
            neighbours = [boundary]
            for direction in (-math.inf,math.inf):
                value = boundary
                for _ in range(8):
                    value = np.nextafter(value,direction)
                    neighbours.append(float(value))
            actual = [original_source_guard(x) for x in neighbours]
            predicted = [domain_grid.source_domain_accepts(x) for x in neighbours]
            test('source_domain_guard_boundary_order',actual==predicted and any(actual) and not all(actual),
                 values=neighbours,accepted=actual)
            # Adversarial interpolation inputs test guard preservation, not
            # admissibility of a physical primary state.
            for tag,donor in (('nonfinite_nan',math.nan),('nonfinite_inf',math.inf),
                              ('wrong_q',100.),('saturated_u',-1.6e21)):
                bad_source = np.zeros_like(primary)
                bad_source[200] = donor
                before_source = bad_source.copy()
                with np.errstate(divide='ignore',invalid='ignore',over='ignore'):
                    bad_raw = domain_grid.to_faces(bad_source)
                    bad_selected = domain_grid.source_to_faces(bad_source)
                same = bool(np.isnan(bad_raw[j]) and np.isnan(bad_selected[j])) or bad_raw[j]==bad_selected[j]
                test('source_domain_'+tag+'_not_repaired',same and
                     not original_source_guard(float(bad_raw[j])) and
                     not domain_grid.source_domain_accepts(float(bad_raw[j])) and
                     np.array_equal(bad_source,before_source,equal_nan=True))
            flat_limit = AdmissibleMetricClock(4.,.1,length=0.)
            flat_source = np.zeros_like(flat_limit.r)
            flat_source[10] = 1.
            flat_raw = flat_limit.to_faces(flat_source)
            test('source_domain_Einstein_limit_inactive',np.min(flat_raw)<0 and
                 np.array_equal(flat_limit.source_to_faces(flat_source),flat_raw) and
                 flat_limit.maximum_stage_domain_fallback_faces==0)
            bad_state = np.zeros((6,len(domain_grid.r)),complex)
            bad_state[2,3] = -.001
            before_state = bad_state.copy()
            rejected = False
            try:
                domain_grid.rhs(bad_state)
            except FloatingPointError as exc:
                rejected = 'resolved negative u' in str(exc)
            test('source_domain_negative_primary_still_rejected',rejected and
                 domain_grid.domain_failure['site']=='cell' and domain_grid.domain_failure['index']==3 and
                 np.array_equal(bad_state,before_state))
        # Post-production admissibility audit: test the actual packet before
        # authorizing any new metric replay. This leaves all action guards fixed.
        for h in (.1,.05,.025):
            polar = PolarGrid(120.,h)
            packet = initial(polar)
            initial_geometry = polar.geometry(*packet)
            grid = metric_factory(120.,h)
            state = np.zeros((6,len(grid.r)),complex)
            state[:2] = packet
            state[2] = initial_geometry['mass']/grid.r**3
            state[4] = np.log(initial_geometry['sigma']*np.sqrt(initial_geometry['N']))
            mu = state[2].real
            muf = grid.source_to_faces(mu)
            old_muf = legacy.StaggeredClockGrid.to_faces(grid,mu)
            face = int(np.argmin(muf))
            error = None
            try:
                grid.rhs(state)
            except (FloatingPointError,ValueError) as exc:
                error = str(exc)
            test('metric_initial_packet_admissibility_'+str(h),error is None,
                 error=error,minimum_cell_mu=float(min(mu)),minimum_face_mu=float(muf[face]),
                 minimum_legacy_face_mu=float(min(old_muf)),minimum_face_radius=float(grid.engine.edges[face+1]),
                 minimum_u=grid.minimum_stage_u)
            if positive_mode and error is None:
                original_state = state.copy()
                grid.measure_curvature = grid.measure_feedback = True
                grid.density_scale = float(max(grid.geometry(state)['rho']))
                row,error = None,None
                try:
                    rhs = grid.rhs(state)
                    stats = lambda:{key:value for key,value in vars(grid).items() if key in
                        ('maximum_stage_limited_faces','minimum_stage_raw_source_face','maximum_stage_source_face_change','maximum_stage_domain_fallback_faces')}
                    before_stats = stats()
                    row = grid.curvature_readout(state,rhs)
                    restored = stats()==before_stats
                    if source_domain:
                        grid.curvature_localization_readout(state)
                        restored = restored and stats()==before_stats
                    baseline_rhs = PairedSaturationClock(120.,h).rhs(state.copy())
                    # Active face limiting changes only the selected metric force;
                    # the source/matter rows are checked against the old engine at
                    # this zero-shift slice, where their input geometries coincide.
                    rows_unchanged = np.array_equal(rhs[[0,1,2,5]],baseline_rhs[[0,1,2,5]])
                except (FloatingPointError,ValueError) as exc:
                    error = str(exc); restored = rows_unchanged = False
                test('positive_packet_curvature_probe_'+str(h),error is None and row['curvature_time_probe_error']<1e-4,
                     error=error,readout=row,domain_failure=grid.domain_failure)
                test('positive_packet_state_and_source_'+str(h),np.array_equal(state,original_state) and rows_unchanged)
                test('positive_probe_limiter_stats_restored_'+str(h),restored)
    if any(not c["passed"] for c in checks):
        failed = [c for c in checks if not c["passed"]]
        return dict(decision="METRIC_OPERATOR_PREFLIGHT_FAILURE" if metric_mode else "COLLAPSE_PREFLIGHT_FAILURE",
                    checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,
                    code_sha256=entry_hashes[Path(__file__).name],source_hashes=entry_hashes)
    if origin_controls:
        test("unchanged_run_sources",all(hashlib.sha256(path.read_bytes()).hexdigest()==entry_hashes[path.name] for path in hash_paths))
        failed = [c for c in checks if not c["passed"]]
        return dict(decision=("SATURATION_METRIC_OPERATOR_CONTROLS" if metric_controls else "SATURATION_LOCALIZATION_CONTROLS" if localization_controls else "SATURATION_FEEDBACK_CONTROLS" if feedback_controls else "SATURATION_CURVATURE_CONTROLS" if curvature_controls else "PAIRED_ORIGIN_CONTROLS_ONLY" if paired_origin else "ORIGIN_CONTROLS_ONLY") if not failed else "ORIGIN_DIAGNOSTIC_CONTROL_FAILURE",
            checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,
            code_sha256=entry_hashes[Path(__file__).name],source_hashes=entry_hashes)

    def run(h,duration=80.,radius=120.,courant=.1,event_stop=False,localize=False):
        start = time.perf_counter()
        polar = PolarGrid(radius,h)
        packet = initial(polar)
        geometry = polar.geometry(*packet)
        grid = (metric_factory if metric_mode else PairedSaturationClock if paired_origin else SaturationClock)(radius,h)
        localize = localize or (metric_mode and not positive_mode and h==.025 and radius==120 and courant==.1)
        grid.measure_curvature = paired_interior
        grid.measure_feedback = feedback_evolution
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
        localizations = []
        event_time = None
        failure_context = None
        phase,attempted_time,state_time = 'initial_readout',0.,0.
        try:
            rows.append(grid.measure(state,0))
            for n in range(round(duration/.25)):
                for substep in range(steps):
                    phase,attempted_time = 'evolution',n*.25+(substep+1)*dt
                    if positive_mode:
                        grid.domain_failure = None
                    state = legacy.clock_rk4(grid,state,dt)
                    state_time = attempted_time
                t = (n+1)*.25
                phase,attempted_time = 'readout',t
                if positive_mode:
                    grid.domain_failure = None
                row = grid.measure(state,t)
                rows.append(row)
                if localize and t in (62.5,62.75):
                    localizations.append(dict(t=t,**grid.curvature_localization_readout(state)))
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
            if positive_mode:
                import traceback
                frames = traceback.extract_tb(exc.__traceback__)
                failure_context = dict(phase=phase,attempted_time=attempted_time,
                    last_accepted_RK_time=state_time,last_sample_time=rows[-1]['t'] if rows else None,
                    domain=getattr(grid,'domain_failure',None),
                    raising_location=dict(function=frames[-1].name,line=frames[-1].lineno,
                                          file=Path(frames[-1].filename).name))
        print(f"Saturation h={h} R={radius}: {status}, last={rows[-1]['t'] if rows else 0}, {time.perf_counter()-start:.1f}s",file=sys.stderr,flush=True)
        return dict(h=h,radius=radius,courant=courant,dt=dt,status=status,error=error,
            elapsed_seconds=time.perf_counter()-start,samples=rows,origin_snapshots=snapshots,curvature_localizations=localizations,
            failure_context=failure_context,
            source_face_limiter=({key:value for key,value in vars(grid).items() if key in
                ('maximum_stage_limited_faces','minimum_stage_raw_source_face','maximum_stage_source_face_change','maximum_stage_domain_fallback_faces')} if positive_mode else None),
            stage_minimum_A=grid.minimum_stage_A,stage_minimum_face_A=grid.minimum_stage_face_A,
            stage_minimum_lapse=grid.minimum_stage_lapse,stage_minimum_q=grid.minimum_stage_q,
            stage_minimum_mu=grid.minimum_stage_mu,stage_minimum_u=grid.minimum_stage_u,
            stage_maximum_q=grid.maximum_stage_q,
            maximum_Courant=grid.engine.maximum_courant,
            maximum_paired_wave_RK_number=grid.pair.maximum_wave_RK_number if paired_origin else None)

    if metric_case is not None:
        h,radius,courant = metric_specs[metric_case]
        case = run(h,metric_endpoint,radius,courant)
        test('metric_replay_completed',case['status']=='COMPLETED' and len(case['samples'])==1+round(metric_endpoint/.25) and
             all(abs(row['t']-.25*i)<1e-12 for i,row in enumerate(case['samples'])))
        test('unchanged_run_sources',all(hashlib.sha256(path.read_bytes()).hexdigest()==entry_hashes[path.name] for path in hash_paths))
        failed = [c for c in checks if not c['passed']]
        return dict(decision='METRIC_OPERATOR_REPLAY' if not failed else 'METRIC_OPERATOR_REPLAY_FAILURE',
            checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,case=case,source_hashes=entry_hashes)

    if localization_case is not None:
        case = run(.025 if localization_case=='fine' else .0125,62.75,localize=True)
        test('localization_replay_completed',case['status']=='COMPLETED' and case['samples'][-1]['t']==62.75 and len(case['curvature_localizations'])==2)
        test('unchanged_run_sources',all(hashlib.sha256(path.read_bytes()).hexdigest()==entry_hashes[path.name] for path in hash_paths))
        failed = [c for c in checks if not c['passed']]
        return dict(decision='CURVATURE_LOCALIZATION_REPLAY' if not failed else 'LOCALIZATION_REPLAY_FAILURE',
            checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,
            case=case,source_hashes=entry_hashes)

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

    paired_endpoint = metric_endpoint if metric_mode else 70. if feedback_evolution else 60. if paired_interior else 51.75 if paired_collapse else 28.
    pilot = metric_case_results['coarse']['case'] if metric_case_results is not None else run(.1,paired_endpoint) if paired_origin else run(.1,event_stop=True)
    if pilot_only:
        test("unchanged_run_sources",all(hashlib.sha256(path.read_bytes()).hexdigest()==entry_hashes[path.name] for path in hash_paths))
        failed = [c for c in checks if not c["passed"]]
        return dict(decision="COLLAPSE_PILOT_ONLY",checks=len(checks),passed=len(checks)-len(failed),failed=failed,
            details=checks,pilot=pilot,code_sha256=entry_hashes[Path(__file__).name],source_hashes=entry_hashes)
    endpoint = paired_endpoint if paired_origin else pilot["samples"][-1]["t"]-(.5 if pilot["status"]=="NUMERICAL_LIMIT" else 0)
    if endpoint<.25:
        raise RuntimeError("No finite pilot interval to refine")
    cases = ({name:value['case'] for name,value in metric_case_results.items()} if metric_case_results is not None else
             dict(coarse=pilot,middle=run(.05,endpoint),fine=run(.025,endpoint),
                  half_step=run(.025,endpoint,courant=.05),domain=run(.025,endpoint,radius=160)))
    if metric_case_results is not None:
        for name,result in metric_case_results.items():
            test('metric_worker_integrity_'+name,result['source_hashes']==entry_hashes and
                 result['checks']==result['passed'] and result.get('process_exit_code')==0)

    def verdict(end,case_set=None,include_curvature=True,include_feedback=True):
        gates,residuals,differences = {},{},{}
        selected = {name:[row for row in case["samples"] if row["t"]<=end+1e-10]
                    for name,case in (cases if case_set is None else case_set).items()}
        if any(not rows or abs(rows[-1]["t"]-end)>1e-8 for rows in selected.values()):
            return dict(passed=False,gates=dict(common_time=False),end=end,resolved_trapping=False)
        required = ("t","mass","charge","radial_constraint","regular_metric_residual","origin_constraint",
                    "minimum_F","maximum_density","charge_rms_areal","central_proper_time",
                    "contiguous_trapped_cells","trapped_cells","outgoing_expansion","ingoing_expansion")
        extra_curvature = paired_interior and include_curvature
        extra_feedback = feedback_evolution and extra_curvature and include_feedback
        if extra_curvature:
            required += curvature_waves+curvature_errors+('curvature_time_probe_error',)
        if extra_feedback:
            required += feedback_waves+('feedback_budget_error',)
        if any(key not in row or not np.isfinite(row[key]) for rows in selected.values() for row in rows for key in required):
            return dict(passed=False,gates=dict(finite_diagnostics=False),end=end,resolved_trapping=False)
        for name,rows in selected.items():
            gates[name+"_charge"] = max(abs(row["charge"]/rows[0]["charge"]-1) for row in rows)<1e-5
            gates[name+"_mass"] = max(abs(row["mass"]/rows[0]["mass"]-1) for row in rows)<5e-3
        for key in ("radial_constraint","regular_metric_residual","origin_constraint")+(curvature_errors if extra_curvature else ())+(('feedback_budget_error',) if extra_feedback else ()):
            middle = max(row[key] for row in selected["middle"])
            fine = max(row[key] for row in selected["fine"])
            gates[key] = fine<5e-3 and (fine<1e-6 or fine<.6*middle)
            residuals[key] = dict(middle=middle,fine=fine)
        if extra_curvature:
            gates['curvature_time_probe'] = max(row['curvature_time_probe_error'] for rows in selected.values() for row in rows)<1e-4
        for key in ("minimum_F","maximum_density","charge_rms_areal","central_proper_time")+(curvature_waves if extra_curvature else ())+(feedback_waves if extra_feedback else ()):
            arrays = {name:np.array([row[key] for row in rows]) for name,rows in selected.items()}
            scale = max(float(np.max(abs(arrays["fine"]))),1e-12)
            if extra_curvature and key in curvature_waves:
                scale = max(scale,ell**(-4 if 'Kretschmann' in key else -2))
            if extra_feedback and key in feedback_waves:
                scale = max(scale,ell**-1 if key=='central_E_normal_rate' else 1.)
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

    def certify(end,case_set=None,include_curvature=True,include_feedback=True):
        accepted,first_rejected,first_trapping = None,None,None
        for stop in np.arange(.25,end+1e-9,.25):
            current = verdict(float(stop),case_set,include_curvature,include_feedback)
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
    if paired_interior:
        for case in fixture.values():
            for row in case['samples']:
                row.update({key:1. for key in curvature_waves})
                row.update({key:1e-8 for key in curvature_errors+('curvature_time_probe_error',)})
                if feedback_evolution:
                    row.update({key:1. for key in feedback_waves})
                    row['feedback_budget_error'] = 1e-8
    fa,fr,ft = certify(.75,fixture)
    test("transient_trapping_certificate_retained",fa["end"]==.75 and fr is None and
         ft is not None and ft["end"]==.5 and not fa["resolved_trapping"])
    for key in ("radial_constraint","regular_metric_residual","origin_constraint","mass","charge"):
        saved = fixture["fine"]["samples"][-1][key]
        fixture["fine"]["samples"][-1][key] = float("nan")
        test("nonfinite_"+key+"_rejected",not verdict(.75,fixture)["passed"])
        fixture["fine"]["samples"][-1][key] = saved
    if paired_interior:
        for key,value in [('central_Kretschmann',float('nan')),('curvature_metric_K_error',.1),
                          ('curvature_time_probe_error',.01),('maximum_abs_Ricci',2.)]:
            saved = fixture['fine']['samples'][-1][key]
            fixture['fine']['samples'][-1][key] = value
            test('curvature_fixture_rejects_'+key,not verdict(.75,fixture)['passed'] and verdict(.75,fixture,include_curvature=False)['passed'])
            fixture['fine']['samples'][-1][key] = saved

    if feedback_evolution:
        for key,value in [('feedback_budget_error',.1),('central_E_normal_rate',float('nan'))]:
            saved = fixture['fine']['samples'][-1][key]
            fixture['fine']['samples'][-1][key] = value
            test('feedback_fixture_rejects_'+key,not verdict(.75,fixture)['passed'] and
                 verdict(.75,fixture,include_feedback=False)['passed'])
            fixture['fine']['samples'][-1][key] = saved
        test('feedback_incomplete_time_rejected',not verdict(1.,fixture)['passed'])
    if feedback_evolution and not metric_mode:
        expected = dict(coarse=(-.39643516997,.38104169092),middle=(-.39612408548,.38090692893),
                        fine=(-.39604343988,.38086094209),half_step=(-.39604343989,.38086094209),
                        domain=(-.39604343988,.38086094209))
        for name,(F60,K60) in expected.items():
            old = next((row for row in cases[name]['samples'] if row['t']==60.),None)
            test('feedback_reproduces_t60_'+name,old is not None and
                 max(abs(old['minimum_F']-F60),abs(old['central_Kretschmann']-K60))<1e-9)
        old = next((row for row in cases['fine']['samples'] if row['t']==60.),None)
        fine_reference = dict(maximum_density=21.3140696056,charge_rms_areal=3.59088044597,
            central_proper_time=36.6362859755,maximum_abs_Kretschmann=.38379914964)
        test('feedback_reproduces_t60_fine_readouts',old is not None and
             all(abs(old[key]-value)<1e-8 for key,value in fine_reference.items()))

    terminal = verdict(endpoint)
    accepted,first_rejected,first_trapping = certify(endpoint)
    curvature_accepted,curvature_rejected,curvature_trapping = certify(endpoint,include_feedback=False) if feedback_evolution else (accepted,first_rejected,first_trapping)
    base_accepted,base_rejected,base_trapping = certify(endpoint,include_curvature=False) if paired_interior else (accepted,first_rejected,first_trapping)
    for name,condition in terminal.get("gates",{}).items():
        test("terminal_"+name,condition)
    metric_reference = None
    if positive_mode:
        test('terminal_positive_unbroken_prefix',accepted is not None and accepted['end']==metric_endpoint and first_rejected is None)
    if metric_mode and not positive_mode:
        reference = dict(maximum_abs_Kretschmann=.40265105260158157,minimum_F=-.4584361584059753,
            maximum_density=22.682428840038963,central_proper_time=37.02380099012467,
            central_weighted_source=.5752730800428267)
        last = next((row for row in cases['fine']['samples'] if row['t']==62.75),None)
        differences = {key:abs(last[key]-value)/max(abs(value),1.) for key,value in reference.items()} if last else {}
        best_error = max(row['curvature_metric_R2_error'] for row in cases['fine']['samples'])
        test('terminal_metric_upgrade_precision',last is not None and best_error<.0013383642549746441,error=best_error)
        test('terminal_metric_upgrade_reference',last is not None and all(value<.001 for value in differences.values()),differences=differences)
        metric_reference = dict(reference=reference,normalized_differences=differences,R2_error=best_error)
    sources_unchanged = all(hashlib.sha256(path.read_bytes()).hexdigest()==entry_hashes[path.name] for path in hash_paths)
    test("unchanged_run_sources",sources_unchanged)
    failed = [c for c in checks if not c["passed"]]
    certification_valid = all(c["passed"] for c in checks if not c["name"].startswith("terminal_"))
    trapping = base_trapping is not None and certification_valid
    interior = bool(paired_interior and certification_valid and curvature_trapping is not None and curvature_accepted is not None and curvature_accepted['end']>51.75)
    feedback_validated = bool(feedback_evolution and certification_valid and first_trapping is not None and accepted is not None and accepted['end']>60.)
    trend = None
    if feedback_validated:
        end = accepted['end']
        start = max(60.,end-1.)
        changes = {}
        for name,case in cases.items():
            earlier = next(row for row in case['samples'] if row['t']==start)
            later = next(row for row in case['samples'] if row['t']==end)
            changes[name] = later['maximum_abs_Kretschmann']-earlier['maximum_abs_Kretschmann']
        uncertainty = 3*max(abs(value-changes['fine']) for value in changes.values())
        decrease = all(value<0 for value in changes.values()) and changes['fine'] < -uncertainty
        increase = all(value>0 for value in changes.values()) and changes['fine'] > uncertainty
        trend = dict(start=start,end=end,peak_curvature_changes=changes,three_times_control_spread=uncertainty,
                     classification='decreasing' if decrease else 'increasing' if increase else 'unresolved_or_flat',
                     interpretation='Maximum absolute curvature change over the last accepted model-time unit; not global stability')
    return dict(decision="INVALID_CERTIFICATION_CONTROLS" if not certification_valid else
                ("POSITIVE_METRIC_PREFIX_VALIDATED" if not failed else "POSITIVE_METRIC_PREFIX_OPEN") if positive_mode else
                ("METRIC_OPERATOR_REPAIR_VALIDATED" if not failed else "METRIC_OPERATOR_REPAIR_OPEN") if metric_mode else
                ("PAIRED_VALIDATED_FEEDBACK_EVOLUTION" if feedback_validated else "PAIRED_FEEDBACK_PREFIX_OPEN") if feedback_evolution else
                ("PAIRED_VALIDATED_POSTTRAPPING_CURVATURE" if interior else "PAIRED_CURVATURE_PREFIX_OPEN") if paired_interior else
                ("PAIRED_VALIDATED_FUTURE_TRAPPING" if trapping else
                 "PAIRED_VALIDATED_PRETRAPPING_PREFIX" if accepted else "PAIRED_UNRESOLVED_COLLAPSE") if paired_collapse else
                ("PAIRED_ORIGIN_REPAIR_VALIDATED" if accepted is not None and accepted["end"]==28. else "PAIRED_ORIGIN_REPAIR_OPEN") if paired_origin else
                "VALIDATED_FUTURE_TRAPPING" if trapping else
                "VALIDATED_PRETRAPPING_PREFIX" if accepted else "UNRESOLVED_COLLAPSE",
        checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,
        pilot_end=endpoint,terminal=terminal,accepted_prefix=accepted,first_rejected=first_rejected,
        first_trapping=first_trapping,cases=cases,
        base_evolution_certificate=dict(accepted=base_accepted,first_rejected=base_rejected,first_trapping=base_trapping) if paired_interior else None,
        curvature_certificate=dict(accepted=curvature_accepted,first_rejected=curvature_rejected,first_trapping=curvature_trapping) if feedback_evolution else None,
        peak_curvature_trend=trend,metric_upgrade_reference=metric_reference,
        source_prerequisite=dict(checks=source["checks"],passed=source["passed"],parameters=source["parameters"]),
        code_sha256=entry_hashes[Path(__file__).name],engine_sha256=entry_hashes[Path(legacy.__file__).name],
        source_hashes=entry_hashes,
        scope=dict(resolved_trapping=trapping,global_regularity=False,singularity_removal=False,
                   metric_operator_upgrade=bool(metric_mode and not positive_mode and not failed),
                   positive_source_reconstruction_prefix=bool(positive_mode and not failed),
                   feedback_evolution=feedback_validated,persistent_regulation=False,
                   posttrapping_curvature=interior,
                   full_RefG_pressure_join=False,same_saturation_action=True,
                   paired_nodal_method=paired_origin,charge_quadrature="h*r^2" if paired_origin else "cell_volume"))


def curvature_localization_checks():
    """Two isolated fixed-window replays; stdout only, no threshold promotion."""
    from concurrent.futures import ThreadPoolExecutor
    import subprocess
    import time
    start = time.perf_counter()
    preflight = collapse_checks(localization_controls=True)
    if preflight['failed']:
        return preflight
    def worker(name):
        command = [sys.executable,'-X','utf8','-B',str(Path(__file__).resolve()),'--localization-case',name]
        process = subprocess.run(command,stdout=subprocess.PIPE,text=True,encoding='utf-8')
        result = json.loads(process.stdout)
        if process.returncode or result['failed']:
            raise RuntimeError('Localization worker failed: '+name+' '+str(result.get('failed')))
        return result
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {name:pool.submit(worker,name) for name in ('fine','finer')}
        results = {name:future.result() for name,future in futures.items()}
    checks = list(preflight['details'])
    def test(name,condition,**evidence):
        checks.append(dict(name=name,passed=bool(condition),**evidence))
    for name,result in results.items():
        test('localization_worker_'+name,result['passed']==result['checks'])
        test('localization_hashes_'+name,result['source_hashes']==preflight['source_hashes'])
    cases = {name:result['case'] for name,result in results.items()}
    for t,expected in ((62.5,.004913400101441889),(62.75,.005154066711989016)):
        row = next(row for row in cases['fine']['samples'] if row['t']==t)
        test('localization_stage16_reproduction_'+str(t),abs(row['curvature_metric_R2_error']-expected)<1e-10,
             actual=row['curvature_metric_R2_error'],expected=expected)
    comparisons = []
    for t in (62.5,62.75):
        pair = {name:next(row for row in case['curvature_localizations'] if row['t']==t) for name,case in cases.items()}
        errors = {name:row['variant_errors']['D4_expanded'] for name,row in pair.items()}
        comparisons.append(dict(t=t,D4_error_finer_over_fine=errors['finer']/max(errors['fine'],1e-30),
            same_state_sensitivity_over_D4_residual={name:dict(D6=row['D6_D4_sensitivity']/max(errors[name],1e-30),
                divergence=row['flux_D4_sensitivity']/max(errors[name],1e-30),
                after_constraint_subtraction=row['residual_after_constraint_subtraction']/max(errors[name],1e-30)) for name,row in pair.items()}))
    error_keys = ('radial_constraint','regular_metric_residual','origin_constraint',
                  'curvature_metric_R2_error','curvature_metric_Ricci_error','curvature_metric_K_error',
                  'curvature_time_probe_error','feedback_budget_error')
    for name,case in cases.items():
        rows = case['samples']
        test('localization_sampling_'+name,len(rows)==252 and all(abs(row['t']-.25*i)<1e-12 for i,row in enumerate(rows)))
        test('localization_finite_diagnostics_'+name,all(np.isfinite(row[key]) for row in rows for key in error_keys))
        rejected = next((row['t'] for row in rows if row['curvature_metric_R2_error']>=.005),None)
        case['original_D4_absolute_gate'] = dict(ceiling=.005,first_rejected=rejected,
            sampled_through=rows[-1]['t'],maximum=max(row['curvature_metric_R2_error'] for row in rows),
            interpretation='Single-run absolute-error component only; not a replacement five-run certificate')
        case['prefix_error_maxima'] = {key:max(row[key] for row in rows) for key in error_keys}
        case['conservation'] = {key:max(abs(row[key]/rows[0][key]-1) for row in rows) for key in ('mass','charge')}
        case['samples'] = [row for row in rows if row['t'] in (0.,60.,62.5,62.75)]
        case.pop('origin_snapshots',None)
    test('localization_sources_unchanged',all(hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()==value
        for name,value in preflight['source_hashes'].items()))
    failed = [row for row in checks if not row['passed']]
    return dict(decision='CURVATURE_LOCALIZATION_COMPUTED' if not failed else 'LOCALIZATION_CONTROL_FAILURE',
        checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks,
        source_hashes=preflight['source_hashes'],elapsed_seconds=time.perf_counter()-start,cases=cases,comparisons=comparisons,
        scope=dict(same_action=True,changed_RHS=False,changed_original_gate=False,
            two_grid_diagnostic=True,five_run_certificate_extended=False,global_regularity=False,singularity_removal=False))


def metric_report_safe(result):
    """Strict JSON for failed reports; null never substitutes for a measured zero."""
    missing = []
    def clean(value,path):
        if isinstance(value,(float,np.floating)) and not math.isfinite(value):
            missing.append(dict(path=path,value='nan' if math.isnan(value) else '+inf' if value>0 else '-inf'))
            return None
        if isinstance(value,dict):
            return {key:clean(item,path+'.'+str(key)) for key,item in value.items()}
        if isinstance(value,(list,tuple)):
            return [clean(item,path+'['+str(i)+']') for i,item in enumerate(value)]
        return value
    safe = clean(result,'$')
    if not missing:
        return result
    safe['nonfinite_report_fields'] = missing
    if not safe.get('failed'):
        check = dict(name='metric_report_finite',passed=False)
        safe['failed'] = [check]
        safe.setdefault('details',[]).append(check)
        safe['checks'] = safe.get('checks',0)+1
        safe['decision'] = 'INVALID_METRIC_REPORT'
        safe.setdefault('scope',{})['metric_operator_upgrade'] = False
        safe['scope']['positive_source_reconstruction_prefix'] = False
    return safe


def metric_worker_report(name,returncode,stdout,stderr=''):
    """Retain worker failures rather than aborting collection of other grids."""
    try:
        result = json.loads(stdout)
        if not isinstance(result,dict):
            raise ValueError('Worker JSON is not an object')
        result = metric_report_safe(result)
    except (ValueError,TypeError) as exc:
        result = dict(worker_failure=str(exc),failed=[dict(name='worker_json_'+name,passed=False)])
    result['process_exit_code'] = returncode
    case = result.get('case')
    if (returncode!=0 or not isinstance(result.get('checks'),int) or
            not isinstance(result.get('failed'),list) or result.get('failed') or
            result.get('checks')!=result.get('passed') or not isinstance(case,dict) or
            case.get('status')!='COMPLETED' or not isinstance(case.get('samples'),list) or
            not case['samples'] or not isinstance(result.get('source_hashes'),dict)):
        result.setdefault('worker_failure','Nonzero exit, failed checks, or incomplete worker case')
        result['worker'] = name
        result['stdout_tail'],result['stderr_tail'] = stdout[-4000:],stderr[-4000:]
    return result


def metric_case_summary(case):
    """Retain the last actual sample, including an empty/early-stopped case."""
    case = dict(case)
    rows = case.get('samples',[])
    rows = rows if isinstance(rows,list) else []
    finite = lambda value:isinstance(value,(int,float,np.integer,np.floating)) and math.isfinite(value)
    keys = ('radial_constraint','regular_metric_residual','origin_constraint',
            'curvature_metric_R2_error','curvature_metric_Ricci_error','curvature_metric_K_error',
            'curvature_time_probe_error','feedback_budget_error')
    case['sample_count'] = len(rows)
    case['prefix_error_maxima'] = {key:max(row[key] for row in rows) if rows and
        all(isinstance(row,dict) and finite(row.get(key)) for row in rows) else None for key in keys}
    case['conservation'] = {key:max(abs(row[key]/rows[0][key]-1) for row in rows) if rows and
        all(isinstance(row,dict) and finite(row.get(key)) for row in rows) and rows[0][key]!=0 else None
        for key in ('mass','charge')}
    case['samples'] = [row for i,row in enumerate(rows) if i==len(rows)-1 or
        isinstance(row,dict) and row.get('t') in (0.,28.,50.5,60.,62.,62.25,62.5,62.75)]
    case.pop('origin_snapshots',None)
    return case


def metric_failed_workers(preflight,results):
    if not any(result.get('worker_failure') for result in results.values()):
        return None
    checks = list(preflight.get('details',[]))
    checks.extend(dict(name='metric_worker_available_'+name,passed=not bool(result.get('worker_failure')))
                  for name,result in results.items())
    failed = [item for item in checks if not item['passed']]
    workers = {name:dict(result,case=metric_case_summary(result['case'])) if
        isinstance(result.get('case'),dict) else result for name,result in results.items()}
    return dict(decision='METRIC_WORKER_FAILURE',checks=len(checks),passed=len(checks)-len(failed),
        failed=failed,details=checks,workers=workers,source_hashes=preflight.get('source_hashes'),
        scope=dict(metric_operator_upgrade=False,positive_source_reconstruction_prefix=False,five_run_certificate_extended=False),
        interpretation='All worker reports retained; missing/incomplete cases are not certified')


def metric_reporting_checks():
    """In-memory failure-reporting fixtures; no worker or evolution is run."""
    import copy
    checks = []
    def test(name,value):
        checks.append(dict(name=name,passed=bool(value)))
    good = dict(checks=1,passed=1,failed=[],details=[],source_hashes={'fixture':'fixed'},
        case=dict(status='COMPLETED',samples=[dict(t=0.),dict(t=62.75)]))
    test('finite_success_unchanged',json.dumps(metric_report_safe(good))==json.dumps(good))
    stopped = copy.deepcopy(good)
    stopped.update(checks=2,failed=[dict(name='completed',passed=False)])
    stopped['case'].update(status='NUMERICAL_LIMIT',error='original cause',stage_minimum_A=math.inf,
                           samples=[dict(t=0.),dict(t=25.75)])
    safe = metric_report_safe(stopped)
    test('sentinel_tagged_null',safe['case']['stage_minimum_A'] is None and
         safe['nonfinite_report_fields']==[dict(path='$.case.stage_minimum_A',value='+inf')])
    test('original_failure_retained',safe['case']['error']=='original cause' and
         safe['case']['status']=='NUMERICAL_LIMIT' and bool(safe['failed']))
    json.dumps(safe,allow_nan=False)
    for value,label in ((math.inf,'+inf'),(-math.inf,'-inf'),(math.nan,'nan')):
        fixture = copy.deepcopy(good); fixture['nested'] = [value]
        encoded = metric_report_safe(fixture)
        test('nonfinite_success_rejected_'+label,bool(encoded['failed']) and encoded['nested']==[None])
        json.dumps(encoded,allow_nan=False)
    success = metric_worker_report('good',0,json.dumps(good))
    test('successful_worker_unchanged',success==dict(good,process_exit_code=0))
    for name,code,payload in (('empty',1,''),('malformed',0,'{'),('nonobject',0,'[]'),
                              ('nonzero_exit',1,json.dumps(good)),('reported_failure',0,json.dumps(safe)),
                              ('missing_case',0,json.dumps(dict(checks=1,passed=1,failed=[])))):
        test('reject_'+name,bool(metric_worker_report(name,code,payload,'stderr retained')['worker_failure']))
    empty = copy.deepcopy(good); empty['case']['samples'] = []
    test('empty_case_rejected',bool(metric_worker_report('emptycase',0,json.dumps(empty))['worker_failure']))
    mixed = dict(good=success,stopped=metric_worker_report('stopped',1,json.dumps(safe)),
                 exception=metric_worker_report('exception',None,'','fixture OSError'))
    aggregate = metric_failed_workers(dict(details=[]),mixed)
    test('all_siblings_retained',set(aggregate['workers'])==set(mixed) and
         aggregate['workers']['good']['case']['status']=='COMPLETED')
    test('last_sample_retained',aggregate['workers']['stopped']['case']['samples'][-1]['t']==25.75)
    test('empty_summary_safe',metric_case_summary(dict(samples=[]))['sample_count']==0)
    test('successful_aggregate_path',metric_failed_workers(dict(details=[]),dict(good=success)) is None)
    invalid_positive = copy.deepcopy(good)
    invalid_positive.update(scope=dict(positive_source_reconstruction_prefix=True),unmeasured=math.inf)
    test('nonfinite_positive_scope_cleared',metric_report_safe(invalid_positive)['scope']['positive_source_reconstruction_prefix'] is False)
    json.dumps(metric_report_safe(aggregate),allow_nan=False)
    failed = [item for item in checks if not item['passed']]
    return dict(decision='METRIC_REPORTING_CONTROLS' if not failed else 'METRIC_REPORTING_FAILURE',
        checks=len(checks),passed=len(checks)-len(failed),failed=failed,details=checks)


def metric_upgrade_checks(positive=False,source_domain=False):
    """Fixed five-case operator repair, with process-isolated grids and stdout."""
    from concurrent.futures import ThreadPoolExecutor
    import subprocess
    import time
    start = time.perf_counter()
    if source_domain and not positive:
        raise ValueError('Source-domain reconstruction requires the positive-metric test ladder')
    preflight = collapse_checks(positive_metric='controls',source_domain=source_domain) if positive else collapse_checks(metric_controls=True)
    if preflight['failed']:
        return preflight
    def worker(name):
        try:
            command = [sys.executable,'-X','utf8','-B',str(Path(__file__).resolve()),
                '--positive-metric' if positive else '--metric-case',name]
            if source_domain:
                command.append('--source-domain')
            process = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
            if process.stderr:
                print(process.stderr,file=sys.stderr,end='',flush=True)
            return metric_worker_report(name,process.returncode,process.stdout,process.stderr)
        except Exception as exc:
            return metric_worker_report(name,None,'',repr(exc))
    results = {'coarse':worker('coarse')} if positive else {}
    failure = metric_failed_workers(preflight,results)
    if failure is not None:
        failure['decision'] = 'POSITIVE_SOURCE_PILOT_FAILED'
        failure['elapsed_seconds'] = time.perf_counter()-start
        return failure
    # The positive-source stage reaches further controls only after its pilot.
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {name:pool.submit(worker,name) for name in ('half_step','domain','fine','middle','coarse') if name not in results}
        for name,future in futures.items():
            try:
                results[name] = future.result()
            except Exception as exc:
                results[name] = metric_worker_report(name,None,'',repr(exc))
    failure = metric_failed_workers(preflight,results)
    if failure is not None:
        failure['elapsed_seconds'] = time.perf_counter()-start
        return failure
    result = (collapse_checks(positive_metric='aggregate',metric_case_results=results,source_domain=source_domain) if positive else
              collapse_checks(metric_upgrade=True,metric_case_results=results))
    same_hash = result.get('source_hashes')==preflight['source_hashes']
    hash_check = dict(name='metric_preflight_production_hash',passed=same_hash)
    result['details'].append(hash_check)
    result['checks'] += 1
    result['passed'] += int(same_hash)
    if not same_hash:
        result['failed'].append(hash_check)
        result['decision'] = 'INVALID_METRIC_PRODUCTION_HASH'
        result['scope']['metric_operator_upgrade'] = False
        result['scope']['positive_source_reconstruction_prefix'] = False
    for name,case in result.get('cases',{}).items():
        result['cases'][name] = metric_case_summary(case)
    result['elapsed_seconds'] = time.perf_counter()-start
    return result


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
    parser.add_argument("--paired-collapse", action="store_true",
                        help="Replay the repaired pair through the fixed t=51.75 trapping window")
    parser.add_argument('--paired-interior', action='store_true',help='Same-action curvature validation through fixed t=60')
    parser.add_argument('--curvature-controls', action='store_true',help='Curvature algebra/metric preflight only')
    parser.add_argument('--source-control', action='store_true',
                        help='Exact local-source bound and fixed-mass concentration test; no evolution')
    parser.add_argument('--source-budget', action='store_true',
                        help='Existing-action initial source-feedback and curvature-rate test; no evolution')
    parser.add_argument('--feedback-evolution',action='store_true',help='Same-packet source-budget and curvature evolution through fixed t=70')
    parser.add_argument('--feedback-controls',action='store_true',help='Source-budget readout preflight only; no collapse evolution')
    parser.add_argument('--curvature-localization',action='store_true',help='Two same-action replays to t=62.75; localize independent R2 error')
    parser.add_argument('--localization-controls',action='store_true',help='Fixed-state localization preflight; no collapse evolution')
    parser.add_argument('--localization-case',choices=('fine','finer'),help='Isolated worker for the fixed curvature-localization stage')
    parser.add_argument('--metric-upgrade',action='store_true',help='Five fixed-window higher-order metric-operator tests through t=62.75')
    parser.add_argument('--metric-controls',action='store_true',help='Higher-order metric operator preflight only')
    parser.add_argument('--metric-case',choices=('coarse','middle','fine','half_step','domain'),help='Isolated metric-operator replay worker')
    parser.add_argument('--positive-metric',choices=('controls','pilot','coarse','middle','fine','half_step','domain'),
                        help='Source-only face limiter: preflight or fixed t=28 pilot ladder')
    parser.add_argument('--source-domain',action='store_true',
                        help='With --positive-metric: use the existing source-domain tolerance instead of exact positivity')
    args = parser.parse_args()
    if args.source_domain and not args.positive_metric:
        parser.error('--source-domain requires --positive-metric')
    if args.positive_metric:
        if any(value for name,value in vars(args).items() if name not in ('positive_metric','source_domain','verbose')):
            parser.error('Choose the source-positive metric mode on its own')
        result = (metric_upgrade_checks(positive=True,source_domain=args.source_domain) if args.positive_metric=='pilot' else
                  collapse_checks(positive_metric=args.positive_metric,source_domain=args.source_domain))
        result['source_reconstruction'] = 'existing_domain_admissible_endpoint' if args.source_domain else 'exact_positive_zero_blend'
        result = metric_report_safe(result)
        if not args.verbose:
            result.pop('details',None)
        print(json.dumps(result,indent=2,allow_nan=False))
        return int(bool(result['failed']))
    if args.metric_upgrade or args.metric_controls or args.metric_case:
        modes = ('metric_upgrade','metric_controls','metric_case')
        if sum(bool(getattr(args,name)) for name in modes)!=1 or any(value for name,value in vars(args).items() if name not in modes+('verbose',)):
            parser.error('Choose one metric-operator mode on its own')
        result = metric_upgrade_checks() if args.metric_upgrade else collapse_checks(metric_case=args.metric_case,metric_controls=args.metric_controls)
        result = metric_report_safe(result)
        if not args.verbose:
            result.pop('details',None)
        print(json.dumps(result,indent=2,allow_nan=False))
        return int(bool(result['failed']))
    if args.curvature_localization or args.localization_controls or args.localization_case:
        modes = ('curvature_localization','localization_controls','localization_case')
        if sum(bool(getattr(args,name)) for name in modes)!=1 or any(value for name,value in vars(args).items() if name not in modes+('verbose',)):
            parser.error('Choose one localization mode on its own')
        result = curvature_localization_checks() if args.curvature_localization else collapse_checks(
            localization_case=args.localization_case,localization_controls=args.localization_controls)
        if not args.verbose:
            result.pop('details')
        print(json.dumps(result,indent=2,allow_nan=False))
        return int(bool(result['failed']))
    if args.feedback_evolution or args.feedback_controls:
        if (args.feedback_evolution and args.feedback_controls) or any(value for name,value in vars(args).items()
                if name not in ('feedback_evolution','feedback_controls','verbose')):
            parser.error('Choose the feedback stage on its own')
        result = collapse_checks(feedback_evolution=args.feedback_evolution,feedback_controls=args.feedback_controls)
        if not args.verbose:
            result.pop('details')
        print(json.dumps(result,indent=2,allow_nan=False))
        return int(bool(result['failed']))
    if args.source_budget:
        if any(value for name,value in vars(args).items()
               if name not in ('source_budget','verbose')):
            parser.error('Choose the local-source budget stage on its own')
        result = source_budget_checks()
        if not args.verbose:
            result.pop('details')
        print(json.dumps(result, indent=2, allow_nan=False))
        return int(bool(result['failed']))
    if args.source_control:
        if any(value for name,value in vars(args).items()
               if name not in ('source_control','verbose')):
            parser.error('Choose the local-source control stage on its own')
        result = source_concentration_checks()
        if not args.verbose:
            result.pop('details')
        print(json.dumps(result, indent=2, allow_nan=False))
        return int(bool(result['failed']))
    if args.paired_interior or args.curvature_controls:
        if args.paired_collapse or args.paired_origin or args.paired_controls or args.origin_audit or args.origin_finer or args.origin_controls or args.collapse_pilot or args.saturation_collapse or (args.paired_interior and args.curvature_controls):
            parser.error('Choose the curvature stage on its own')
        args.paired_origin = True
    if args.paired_collapse:
        if args.paired_origin or args.paired_controls or args.origin_audit or args.origin_finer or args.origin_controls or args.collapse_pilot or args.saturation_collapse:
            parser.error("Choose the paired collapse stage on its own")
        args.paired_origin = True
    if (args.saturation_collapse or args.collapse_pilot or args.origin_audit or args.origin_finer or args.origin_controls or args.paired_origin or args.paired_controls) and (args.supercritical_data or args.oscillon_source or args.oscillon_dynamics or args.dynamics_pilot):
        parser.error("Choose collapse or a previous stage")
    if args.supercritical_data and (args.oscillon_source or args.oscillon_dynamics or args.dynamics_pilot):
        parser.error("Choose initial data or the existing source/dynamics tests")
    if args.oscillon_source and (args.oscillon_dynamics or args.dynamics_pilot):
        parser.error("Choose stationary or dynamical checks")
    result = (collapse_checks(pilot_only=args.collapse_pilot,
                             origin_audit=args.origin_audit or args.origin_finer or args.origin_controls or args.paired_origin or args.paired_controls,
                             origin_finer=args.origin_finer,origin_controls=args.origin_controls or args.paired_controls,
                             paired_origin=args.paired_origin or args.paired_controls,
                             paired_collapse=args.paired_collapse,
                             paired_interior=args.paired_interior,curvature_controls=args.curvature_controls)
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
