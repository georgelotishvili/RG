"""W88: static native phase reduction; finite JSON stdout, no file writes."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import platform
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

HERE = Path(__file__).resolve()
ROOT = HERE.parents[4]
BASE = "RefG/work 3/Strong_Field/"
PINS = {
    "CODES.md": "27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41",
    BASE + "W3-84_Minimal_Node_Link_Candidate/w3_84_node_link.py": "acd70be11d4734b5b208fa5b7166475166c48ee5f090640a05e19dfa081c3916",
    BASE + "W3-84_Minimal_Node_Link_Candidate/w3_84_node_link_contract.md": "ff1b94280a533e6aba4109465de7afcd2b5c7019c5292cb78c1040982c47d1dd",
    BASE + "W3-87_State_Dependent_Gravitational_Response/w3_87_state_dependent_response_contract.md": "7c47bcd4efe292a91d13717a3ec3962776488b01c521dfb27b9df1e989fcee80",
    BASE + "W3-88_Native_Phase_Effective_Action/w3_88_native_phase_contract.md": "3295abe77253eee38b3fd8fb479145a8531d802d9087b63035315424e1080b60",
    "intuitive/RefG_GE.md": "7c28f8848ae5ac441efae05e5a551973f37cca711202a0865e007793e282acd1",
    "intuitive/RefG_EN.tex": "6e69d616229688d885320d9b26b8c4637c563ae47f8da006feee8548d6ad910e",
    "intuitive/idea.txt": "a73a06e1ed5b75298fae1bf22c88418e175b6628b12fa08a9e9c3992da59b48e",
    "intuitive/Dictionary.txt": "f6e12b67f38e49bb547d37e6c92375a2ee5b2f596ed481a866cbc490be32ed0b",
}
CHECKS = {}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(group, name, condition):
    CHECKS.setdefault(group, {})[name] = bool(condition)


def zero(group, name, expression):
    residual = sp.simplify(expression)
    check(group, name, residual == 0)
    return str(residual)


def symbolic(model):
    q, s, delta = sp.symbols("q s delta", real=True)
    B, C, I = sp.symbols("B C I", positive=True)
    n, nb, P, v, w, eta = sp.symbols("n nbar P v w eta", real=True)
    k = sp.Function("K")(q)
    kp, kpp = sp.diff(k, q), sp.diff(k, q, 2)
    V = B*q*q/2 + k*s
    H = (n-nb)**2/(2*C) + P*P/(2*I) + V
    L = (n*v + P*w-H).subs({n: nb+C*v, P: I*w})
    residuals = {
        "L": zero("Legendre_elimination", "exact_L", L-(nb*v+C*v*v/2+I*w*w/2-V)),
        "n_EL": zero("Legendre_elimination", "n_EL", (v-sp.diff(H,n)).subs(n,nb+C*v)),
        "P_EL": zero("Legendre_elimination", "P_EL", (w-sp.diff(H,P)).subs(P,I*w)),
    }
    stationarity, D = sp.diff(V,q), sp.diff(V,q,2)
    qs = -kp/D
    residuals["implicit_derivative"] = zero("static_envelope", "implicit_derivative", D*qs+kp)
    # Explicitly remove the stationary factor; no off-shell identity is claimed.
    total_Ws = sp.diff(V,s)+sp.diff(V,q)*qs
    residuals["envelope"] = zero("static_envelope", "envelope_on_shell", total_Ws-k-stationarity*qs)
    Wss = sp.diff(k,q)*qs
    residuals["concavity"] = zero("static_envelope", "second_envelope", Wss+kp**2/D)
    S = (Wss*sp.sin(delta)**2+k*sp.cos(delta)).subs(s,1-sp.cos(delta))
    K84,Kp84,Kpp84 = model.coupling(q,sp.exp)
    A84,b84,D84 = model.stiffness(q,delta,exp=sp.exp,sin=sp.sin,cos=sp.cos)
    mapped = S.subs({k:K84,kp:Kp84,kpp:Kpp84,B:model.B}, simultaneous=True)
    residuals["Schur_regression"] = zero("static_envelope", "W84_Schur", mapped-(A84-b84**2/D84))

    k0,k1,k2 = sp.symbols("k0 k1 k2", real=True)
    a2,a4 = sp.symbols("a2 a4")
    q_series = a2*delta**2+a4*delta**4
    # K through q^2 is sufficient for V through Delta^6 and V_q through Delta^4.
    Vpoly = B*q*q/2+(k0+k1*q+k2*q*q/2)*(1-sp.cos(delta))
    force_series = sp.series(sp.diff(Vpoly,q).subs(q,q_series),delta,0,6).removeO().expand()
    solved = sp.solve([force_series.coeff(delta,2),force_series.coeff(delta,4)],(a2,a4),dict=True)[0]
    expected_q = {a2:-k1/(2*B), a4:k1/(24*B)+k1*k2/(4*B**2)}
    for sym,target in expected_q.items():
        residuals[str(sym)] = zero("Taylor_reduction", str(sym), solved[sym]-target)
    Wpoly = sp.series(Vpoly.subs(q,q_series.subs(solved)),delta,0,8).removeO().expand()
    targets = {2:k0/2, 4:-k0/24-k1*k1/(8*B),
               6:k0/720+k1*k1/(48*B)+k2*k1*k1/(16*B*B)}
    for degree,target in targets.items():
        residuals[f"W{degree}"] = zero("Taylor_reduction", f"W{degree}", Wpoly.coeff(delta,degree)-target)
    frozen = {k0:K84.subs(q,0),k1:Kp84.subs(q,0),k2:Kpp84.subs(q,0),B:model.B}
    for degree,target in {2:sp.Rational(1,2),4:-sp.Rational(13,24),6:sp.Rational(601,720)}.items():
        zero("Taylor_reduction", f"frozen_W{degree}", Wpoly.coeff(delta,degree).subs(frozen)-target)
    # Altered quartic expressions pass through exactly the baseline residual evaluator.
    def quartic_residual(candidate):
        return sp.simplify((candidate-Wpoly.coeff(delta,4)).subs(frozen))
    check("mutation_controls", "baseline_quartic", quartic_residual(targets[4]) == 0)
    controls = {}
    for name,candidate in {
        "frozen_link":-k0/24,
        "omit_cosine_quartic":-k1*k1/(8*B),
        "reverse_induced_sign":-k0/24+k1*k1/(8*B),
    }.items():
        r = quartic_residual(candidate)
        controls[name] = str(r)
        check("mutation_controls", name, r != 0)

    # Mapping between solutions under a uniform n shift, not gauge equivalence.
    zero("native_state_variable_test", "phase_rate_shift", sp.diff(H,n).subs(n,n+eta)-sp.diff(H,n)-eta/C)
    zero("native_state_variable_test", "link_force_shift", sp.diff(H,q).subs(n,n+eta)-sp.diff(H,q))
    zero("native_state_variable_test", "strain_energy_independent_of_n", sp.diff(V,n))
    return {"symbolic_residuals":residuals,"wrong_quartic_residuals":controls,
            "derived_q_series":str(q_series.subs(solved)),"derived_W_series":str(Wpoly)}


def minimum(delta, iterations):
    """Independent unexpanded potential and its force; same frozen Hamiltonian."""
    s = 1-mp.cos(delta)
    def potential(q):
        return q*q/2+mp.exp(1-q-mp.exp(q))*s
    def derivative(q):
        return q-(1+mp.exp(q))*mp.exp(1-q-mp.exp(q))*s
    if s == 0:
        return mp.mpf(0), mp.mpf(0), mp.mpf(0)
    lo,hi = mp.mpf(0),mp.mpf(4)
    if not (derivative(lo)<0<derivative(hi)):
        raise ArithmeticError("Inherited root bracket failed")
    for _ in range(iterations):
        mid = (lo+hi)/2
        if derivative(mid)>0:
            hi=mid
        else:
            lo=mid
    q=(lo+hi)/2
    return q,potential(q),abs(derivative(q))


def numerical(model):
    reports, raw = [], {}
    for digits,iterations in ((80,260),(100,330)):
        with mp.workdps(digits):
            q_errors,w_errors,rows = [],[],[]
            for angle in ("0.08","0.04","0.02"):
                d=mp.mpf(angle)
                q,W,r=minimum(d,iterations)
                q_ratio=(q-d*d)/d**4
                w_ratio=(W-(d*d/2-mp.mpf(13)*d**4/24))/d**6
                qe=abs(q_ratio+mp.mpf(19)/12)
                we=abs(w_ratio-mp.mpf(601)/720)
                q_errors.append(qe); w_errors.append(we)
                check("direct_energy_check",f"force_{digits}_{angle}",r<mp.mpf("1e-60"))
                check("direct_energy_check",f"q_remainder_{digits}_{angle}",qe<mp.mpf(".05")*19/12)
                check("direct_energy_check",f"W_remainder_{digits}_{angle}",we<mp.mpf(".05")*601/720)
                raw[digits,angle]=(q,W)
                rows.append({"angle":angle,"q":mp.nstr(q,24),"W":mp.nstr(W,24),
                             "force_residual":mp.nstr(r,8),"q_remainder_over_angle4":mp.nstr(q_ratio,24),
                             "W_remainder_over_angle6":mp.nstr(w_ratio,24)})
            check("direct_energy_check",f"q_error_monotone_{digits}",q_errors[0]>q_errors[1]>q_errors[2])
            check("direct_energy_check",f"W_error_monotone_{digits}",w_errors[0]>w_errors[1]>w_errors[2])
            reports.append({"digits":digits,"bisections":iterations,"probes":rows})
    with mp.workdps(100):
        precision=[]
        for angle in ("0.08","0.04","0.02"):
            diffs=[abs(a-b) for a,b in zip(raw[80,angle],raw[100,angle])]
            check("direct_energy_check",f"precision_{angle}",max(diffs)<mp.mpf("1e-60"))
            precision.append({"angle":angle,"q_W_differences":[mp.nstr(x,8) for x in diffs]})
        states=[]
        for name,Q in (("zero",mp.mpf(0)),("pi/6",mp.pi/6)):
            q,W,r=minimum(Q,330)
            A,b,D=model.stiffness(q,Q,exp=mp.exp,sin=mp.sin,cos=mp.cos)
            S=A-b*b/D
            check("native_state_variable_test",name+"_stable",S>0 and D>0)
            check("native_state_variable_test",name+"_force_root",r<mp.mpf("1e-60"))
            theta=np.arange(model.N)*float(Q)
            pos=np.array([theta,np.full(model.N,float(q))])
            reference_force=model.forces(pos)
            check("native_state_variable_test",name+"_full_force",np.max(np.abs(reference_force))<1e-12)
            for nn in (.5,1.,2.):
                momentum=np.array([np.full(model.N,nn),np.zeros(model.N)])
                vel=model.velocities(momentum)
                check("native_state_variable_test",f"{name}_n{nn}_velocity",np.max(np.abs(vel[0]-(nn-model.NBAR)/model.C))<1e-12 and np.max(np.abs(vel[1]))<1e-12)
                # q and Delta determine production forces, independent of momenta.
                delta=np.roll(theta,-1)-theta
                AA,bb,DD=model.stiffness(pos[1],delta)
                check("native_state_variable_test",f"{name}_n{nn}_stiffness",np.max(np.abs(AA-bb*bb/DD-float(S)))<1e-12)
                check("native_state_variable_test",f"{name}_n{nn}_force",np.max(np.abs(model.forces(pos)-reference_force))<1e-12)
            states.append({"twist":name,"q":mp.nstr(q,24),"S":mp.nstr(S,24),"rotor_n_values":[.5,1,2]})
        gap=abs(mp.mpf(states[0]["S"])-mp.mpf(states[1]["S"]))
        check("native_state_variable_test","same_n_different_S",gap>mp.mpf(".001"))
        Q=mp.pi/6
        q,W,r=minimum(Q,330)
        A,b,D=model.stiffness(q,Q,exp=mp.exp,sin=mp.sin,cos=mp.cos)
        S=A-b*b/D
        fd=[]; errors=[]
        for hs in ("1e-5","5e-6"):
            h=mp.mpf(hs)
            measured=(minimum(Q+h,330)[1]-2*W+minimum(Q-h,330)[1])/h**2
            err=abs(measured-S)
            errors.append(err)
            check("direct_energy_check","curvature_"+hs,err<mp.mpf("1e-8"))
            fd.append({"h":hs,"energy_curvature":mp.nstr(measured,24),"error":mp.nstr(err,12)})
            # The same finite-difference residual detects the omitted Schur term.
            check("mutation_controls","omit_Schur_"+hs,abs(measured-A)>mp.mpf("1e-8"))
        check("direct_energy_check","curvature_refinement",errors[1]<=mp.mpf(".4")*errors[0] or max(errors)<mp.mpf("1e-20"))
    return {"Taylor_probes":reports,"precision_comparison":precision,"uniform_states":states,
            "same_rotor_n_stiffness_gap":mp.nstr(gap,24),"curvature_finite_differences":fd}


def main():
    initial={path:sha(ROOT/path) for path in PINS}
    for path,target in PINS.items():
        check("provenance",path,initial[path]==target)
    if not all(CHECKS["provenance"].values()):
        print(json.dumps({"status":"FAIL","reason":"source hash mismatch","checks":CHECKS},indent=2))
        return 1
    path=ROOT/BASE/"W3-84_Minimal_Node_Link_Candidate/w3_84_node_link.py"
    spec=importlib.util.spec_from_file_location("w84",path)
    model=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    check("provenance","frozen_constants",all(getattr(model,k)==1 for k in ("B","C","I","K0","D0","KAPPA","NBAR")) and model.N==48)
    exact=symbolic(model)
    numeric=numerical(model)
    check("provenance","protected_sources_unchanged",all(sha(ROOT/p)==initial[p] for p in PINS))
    flags={name:all(rows.values()) for name,rows in CHECKS.items()}
    passed=all(flags.values())
    flags.update({k:False for k in ("microscopic_gravitational_F_derived","physical_current_map",
        "full_dynamical_equivalence","regular_black_hole","singularity_resolved","observational_pass",
        "active_theory_changed","intuitive_files_changed")})
    print(json.dumps({"status":"PASS" if passed else "FAIL","check_count":sum(map(len,CHECKS.values())),
        "checks":CHECKS,"closure_flags":flags,"exact":exact,"numerical":numeric,
        "source_hashes":initial,"verifier_sha256":sha(HERE),
        "versions":{"Python":platform.python_version(),"SymPy":sp.__version__,"NumPy":np.__version__,"mpmath":mp.__version__}},indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
