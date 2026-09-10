#!/usr/bin/env python3
"""RefG two-function exterior and moving-boundary source checks.

Author-written verification of the cited formulas, not source code from a paper.
https://doi.org/10.1103/PhysRevLett.132.031401
RefG W3-64, W3-79 and W3-92 source conventions; see BMP.md.
Detailed assumptions, derivations and citations: BMP.md in this directory.
Requires SymPy 1.13.3 (versions used for verification).
Reads no project files and writes no files. Run with --verbose for all residuals.
"""

import argparse
import json
import sympy as s


def run_checks():
    """Return exact/numerical checks and narrowly scoped physical status flags."""
    rows=[]
    def check(name,actual,expected=0):
        res=s.simplify(actual-expected)
        rows.append(dict(name=name,passed=(res==0),kind="exact",residual=str(res)))
    def truth(name,passed,kind="analytic"):
        rows.append(dict(name=name,passed=bool(passed),kind=kind))

    t,R,th,ph=s.symbols("t R theta phi",real=True)
    G=s.symbols("G",positive=True)
    F=s.Function("f")(R)
    d=s.Function("d")(R)
    coords=(t,R,th,ph)
    metric=s.diag(-s.exp(2*d)*F,1/F,R**2,R**2*s.sin(th)**2)
    inverse=s.diag(*[1/metric[i,i] for i in range(4)])
    Gamma={}
    for a in range(4):
        for b in range(4):
            for c in range(4):
                Gamma[a,b,c]=s.simplify(inverse[a,a]*(
                    s.diff(metric[a,c],coords[b])+s.diff(metric[a,b],coords[c])
                    -s.diff(metric[b,c],coords[a]))/2)
    Ric=[]
    for a in range(4):
        component=0
        for c in range(4):
            component+=s.diff(Gamma[c,a,a],coords[c])-s.diff(Gamma[c,a,c],coords[a])
            for k in range(4):
                component+=Gamma[c,c,k]*Gamma[k,a,a]-Gamma[c,a,k]*Gamma[k,a,c]
        Ric.append(s.simplify(component))
    scalar=s.simplify(sum(inverse[a,a]*Ric[a] for a in range(4)))
    Einstein=[s.simplify(Ric[a]-metric[a,a]*scalar/2) for a in range(4)]
    rho_geo=s.simplify(Einstein[0]/(-metric[0,0])/(8*s.pi*G))
    pr_geo=s.simplify(Einstein[1]/metric[1,1]/(8*s.pi*G))
    mass=R*(1-F)/(2*G)
    check("direct_Einstein_mass",s.diff(mass,R),4*s.pi*R**2*rho_geo)
    check("direct_Einstein_clock",rho_geo+pr_geo,
          F*s.diff(d,R)/(4*s.pi*G*R))
    check("one_function_source_restriction",(rho_geo+pr_geo).subs(s.diff(d,R),0))

    def static_sources(f,delta,derivative,radius):
        """Total Einstein-frame sources; no EOS or extra medium term inserted."""
        rho=(1-f-radius*derivative(f))/(8*s.pi*G*radius**2)
        pr=-rho+f*derivative(delta)/(4*s.pi*G*radius)
        return s.simplify(rho),s.simplify(pr)
    def surface_stress(rho,pr,S,v):
        return (s.simplify((v*(rho+pr)+(1+v*v)*S)/(1-v*v)),
                s.simplify((v*v*rho+2*v*S+pr)/(1-v*v)))
    def source_gate(mass_jump,q_jump,p_jump,beta,rdot,radius):
        return dict(mass=mass_jump,flux=q_jump,traction=p_jump,
                    mass_rate=4*s.pi*radius**2*(beta*q_jump-rdot*p_jump),
                    necessary_source_match=all(s.simplify(z)==0
                        for z in (mass_jump,q_jump,p_jump)))

    x,mg=s.symbols("r_isotropic m_g",positive=True)
    u=mg/x
    Ra=x*s.exp(u)
    fexp=(1-u)**2
    dexp=-u-s.log(1-u)  # outer branch x>mg
    DR=lambda expr:s.simplify(s.diff(expr,x)/s.diff(Ra,x))
    rex,pex=static_sources(fexp,dexp,DR,Ra)
    target=-u**2/(8*s.pi*G*Ra**2)
    check("RefG_medium_density",rex,target)
    check("RefG_medium_pressure",pex,target)
    check("RefG_medium_clock",DR(dexp),-u**2/(Ra*(1-u)**2))
    check("RefG_metric_time_coefficient",s.exp(2*dexp)*fexp,s.exp(-2*u))
    rfrozen,pfrozen=static_sources(fexp,s.S.Zero,DR,Ra)
    check("same_mass_same_density",rfrozen,rex)
    check("frozen_clock_pressure_error",pfrozen-pex,u**2/(4*s.pi*G*Ra**2))
    truth("frozen_clock_is_detected",s.simplify(pfrozen-pex)!=0,"negative_control")
    clock_error=1-s.exp(s.Rational(1,2))/2
    truth("illustrative_clock_error",0.17<float(clock_error)<0.18,"numerical_evaluation")

    h,hp,Omega,sigma,ff,V=s.symbols("h h_prime Omega sigma f_value V",positive=True)
    rhoO=ff*hp**2/2+Omega**2*h**2/(2*sigma**2*ff)+V
    prO=ff*hp**2/2+Omega**2*h**2/(2*sigma**2*ff)-V
    sumO=ff*hp**2+Omega**2*h**2/(sigma**2*ff)
    check("actual_W64_null_sum",rhoO+prO,sumO)
    truth("nonzero_oscillon_requires_clock_response",sumO.is_positive)
    alpha=s.symbols("alpha",positive=True)
    check("W64_scaled_clock_equation",
          (4*s.pi*G*R*(rhoO+prO)/ff).subs(G,alpha/(4*s.pi)),
          alpha*R*sumO/ff)

    rho,pr,S,v,w,mu,n,pc=s.symbols("rho pr S v w mu n P_C",real=True)
    qB,pB=surface_stress(rho,pr,S,v)
    boost=s.Matrix([[1,v],[v,1]])/s.sqrt(1-v*v)  # |v|<1
    tensor=s.Matrix([[rho,S],[S,pr]])
    direct=boost*tensor*boost.T
    check("independent_flux_boost",qB,direct[0,1])
    check("independent_pressure_boost",pB,direct[1,1])

    Pi,Phi=s.symbols("Pi Phi",real=True)
    rs=(Pi**2+Phi**2)/2+V
    ps=(Pi**2+Phi**2)/2-V
    ss=Pi*Phi
    qs,psb=surface_stress(rs,ps,ss,v)
    check("scalar_surface_flux",qs,(Pi+v*Phi)*(Phi+v*Pi)/(1-v*v))
    rc=n*mu/(1-w*w)-pc
    sc=-n*mu*w/(1-w*w)
    prc=n*mu*w*w/(1-w*w)+pc
    qc,pcb=surface_stress(rc,prc,sc,v)
    check("collective_surface_flux",qc,
          n*mu*(v-w)*(1-v*w)/((1-v*v)*(1-w*w)))
    check("collective_surface_pressure",pcb,
          n*mu*(v-w)**2/((1-v*v)*(1-w*w))+pc)
    qt,pt=surface_stress(rs+rc,ps+prc,ss+sc,v)
    check("single_counted_total_flux",qt,qs+qc)
    check("single_counted_total_pressure",pt,psb+pcb)

    z,sig=s.symbols("zeta sigma_pg",positive=True)
    gamma=1/s.sqrt(1-v*v)
    mr=4*s.pi*R**2*(rho+z*S)
    mt=4*s.pi*sig*R**2*(z*(rho+pr)+(1+z*z)*S)
    U_m=gamma*(mt/sig+(v-z)*mr)
    rdot=gamma*(v-z)
    beta=gamma*(1-v*z)
    check("boundary_mass_from_W79",U_m,4*s.pi*R**2*(beta*qB-rdot*pB))
    check("boundary_angular_identity",beta**2-rdot**2,1-z*z)

    re,pe,ve,fe=s.symbols("rho_ext pr_ext v_ext f_ext",real=True)
    qe,pse=surface_stress(re,pe,0,ve)
    ge=1/s.sqrt(1-ve*ve)
    bex=ge*s.sqrt(fe)
    rdex=ge*ve*s.sqrt(fe)
    check("static_exterior_mass_rate",bex*qe-rdex*pse,rdex*re)
    check("BMP_flux_all_boundary_frames",qe.subs(pe,-re))
    check("BMP_pressure_all_boundary_frames",pse.subs(pe,-re),-re)
    truth("moving_exponential_zero_flux_import_fails",
          s.simplify(qe.subs({re:rex,pe:pex,ve:s.Rational(1,2)}))!=0,
          "negative_control")

    b0,r0,qd,pd=s.symbols("beta Rdot Delta_q Delta_P",real=True)
    delta_gate=source_gate(0,qd,pd,b0,r0,R)
    check("jump_mass_propagation",delta_gate["mass_rate"],
          4*s.pi*R**2*(b0*qd-r0*pd))
    good=source_gate(0,0,0,b0,r0,R)
    check("matched_source_preserves_mass",good["mass_rate"])
    truth("matched_source_is_admitted",good["necessary_source_match"])
    truth("unmatched_mass_is_rejected",
          not source_gate(1,0,0,b0,r0,R)["necessary_source_match"],"negative_control")
    const=s.symbols("rho_constant",positive=True)
    check("constant_source_mass_work",
          s.diff(4*s.pi*const*R**3/3,R)*r0,
          -4*s.pi*R**2*(-const)*r0)
    badp=source_gate(0,0,const,b0,r0,R)  # omit interior P=-const
    check("omitted_pressure_mass_error",badp["mass_rate"],-4*s.pi*R**2*const*r0)
    truth("snapshot_mass_cannot_hide_pressure_error",badp["mass_rate"]!=0,"negative_control")
    truth("pressure_mismatch_is_rejected",not badp["necessary_source_match"],"negative_control")
    badq=source_gate(0,-qd,0,b0,r0,R)
    truth("snapshot_mass_cannot_hide_flux_error",badq["mass_rate"]!=0,"negative_control")
    truth("flux_mismatch_is_rejected",not badq["necessary_source_match"],"negative_control")
    badscalar=surface_stress(2*rs,2*ps,2*ss,v)
    truth("duplicate_scalar_pressure_detected",
          s.simplify(badscalar[1]-psb)!=0,"negative_control")

    # Independent radial acceleration from the directly computed connection.
    # Proper-time normalization fixes Tdot^2; angular matching f+Rdot^2=C0
    # implies Rddot=-f'/2 on a moving comoving FLRW boundary.
    rv,ra=s.symbols("Rdot_static Rddot_static",real=True)
    tdot2=(F+rv**2)/(s.exp(2*d)*F**2)
    acc=s.simplify(ra+Gamma[1,0,0]*tdot2+Gamma[1,1,1]*rv**2)
    check("boundary_acceleration_from_connection",acc,
          ra+s.diff(F,R)/2+s.diff(d,R)*(F+rv**2))
    restricted=s.simplify(acc.subs(ra,-s.diff(F,R)/2))
    check("second_fundamental_form_clock_restriction",restricted,
          s.diff(d,R)*(F+rv**2))
    truth("nonzero_clock_gradient_breaks_special_matching",
          restricted.subs({s.diff(d,R):1,F:1,rv:1})!=0,"negative_control")

    failed=[r for r in rows if not r["passed"]]
    return dict(
     decision="REFG_CLOCK_AND_MOVING_BOUNDARY_SOURCE_GATE",
     sympy=s.__version__,
     checks=len(rows),passed=len(rows)-len(failed),failed=failed,details=rows,
     clock_example=dict(correct=float(s.exp(-s.Rational(1,2))),forced=0.5,
                        relative_error=float(clock_error)),
     physical_flags=dict(source_boundary_gate_verified=not failed,
                         new_constitutive_law=False,full_junction_solved=False,
                         singularity_resolution=False,original_models_changed=False)
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verbose", action="store_true", help="Include every check and residual."
    )
    args = parser.parse_args()
    result = run_checks()
    if not args.verbose:
        result.pop("details")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(bool(result["failed"]))


if __name__ == "__main__":
    raise SystemExit(main())
