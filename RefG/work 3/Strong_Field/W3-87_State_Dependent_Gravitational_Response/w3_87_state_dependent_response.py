"""W87 exact action-response verification. Run with python -B; stdout only.

Implementation provenance: the first run (source a6868fe5f242f889fdac7aca0a059be3fe6850473e79de2f23ea45755181e1b9)
passed all algebra groups but failed the wrong-density negative control because
SymPy returned None for whether n*(6*K*H**2*F'+rho') equals zero. The detector
now uses the exact retained F=1, rho=n regular dust witness, giving residual n.
No action, physical function selection, threshold or frozen contract changed.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import sympy as s


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = HERE / "w3_87_state_dependent_response_contract.md"
PINS = {
    "CODES.md": "27842a2b5d2c602c039dd712cda4086e9b89105ddad81b4d4edbf1585aa8db41",
    "intuitive/RefG_GE.md": "7c28f8848ae5ac441efae05e5a551973f37cca711202a0865e007793e282acd1",
    "intuitive/RefG_EN.tex": "6e69d616229688d885320d9b26b8c4637c563ae47f8da006feee8548d6ad910e",
    "intuitive/idea.txt": "a73a06e1ed5b75298fae1bf22c88418e175b6628b12fa08a9e9c3992da59b48e",
    "intuitive/Dictionary.txt": "f6e12b67f38e49bb547d37e6c92375a2ee5b2f596ed481a866cbc490be32ed0b",
    "RefG/work 3/Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md": "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
    "RefG/work 3/Strong_Field/W3-84_Minimal_Node_Link_Candidate/w3_84_node_link_contract.md": "ff1b94280a533e6aba4109465de7afcd2b5c7019c5292cb78c1040982c47d1dd",
    "RefG/work 3/Strong_Field/W3-86_Localized_Node_Link_Feedback/w3_86_localized_node_link_feedback_contract.md": "d39071b760d27a2882f3a442f0b69578905d0d157130e114c2ef92c9f323b070",
}
CONTRACT_SHA = "7c47bcd4efe292a91d13717a3ec3962776488b01c521dfb27b9df1e989fcee80"
CHECKS: dict[str, list[bool]] = {}
DETAILS: dict[str, object] = {}
MUTATIONS: dict[str, bool] = {}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def zero(group: str, expression: s.Expr) -> None:
    residual = s.simplify(expression.doit())
    CHECKS.setdefault(group, []).append(residual == 0)
    if residual != 0:
        DETAILS.setdefault("failed_residuals", []).append({"group": group, "residual": str(residual)})


def mutation(name: str, residual: s.Expr) -> None:
    residual = s.simplify(residual.doit())
    # A negative control must be symbolically nonzero, not just printed FAIL.
    MUTATIONS[name] = bool(residual != 0 and residual.equals(0) is False)


def density_variations() -> None:
    eps = s.symbols("epsilon", real=True)
    eta = s.diag(-1, 1, 1, 1)
    n0 = s.Integer(2)
    u = s.Matrix([s.Rational(5, 4), s.Rational(3, 4), 0, 0])
    ud = eta * u
    J = n0 * u
    projection = eta + ud * ud.T
    b = s.symbols("b", real=True)
    for i in range(4):
        for j in range(i, 4):
            direction = s.zeros(4)
            direction[i, j] = 1
            direction[j, i] = 1
            invg = eta + eps * direction
            g = invg.inv()
            e = s.sqrt(-g.det())
            nv = s.sqrt(-(J.T * g * J)[0]) / e
            variation = s.diff(nv, eps).subs(eps, 0)
            multiplicity = 1 if i == j else 2
            zero("density_variation", variation - n0 * projection[i, j] * multiplicity / 2)
            zero("density_variation", 2 * b * variation / multiplicity - n0 * b * projection[i, j])
    for A in range(4):
        for mu in range(4):
            E = s.eye(4)
            E[A, mu] += eps
            g = E.T * eta * E
            nv = s.sqrt(-(J.T * g * J)[0]) / E.det()
            expected = -n0 * (int(A == mu) + ud[A] * u[mu])
            zero("density_variation", s.diff(nv, eps).subs(eps, 0) - expected)
    for mu in range(4):
        Jv = J.copy()
        Jv[mu] += eps
        nv = s.sqrt(-(Jv.T * eta * Jv)[0])
        zero("density_variation", s.diff(nv, eps).subs(eps, 0) + ud[mu])
    zero("density_variation", (u.T * (n0 * b * projection) * u)[0])
    zero("density_variation", sum(eta[i, i] * projection[i, i] for i in range(4)) - 3)


def weighted_and_current() -> None:
    x = s.symbols("x", real=True)
    e, f, v, R = [s.Function(name)(x) for name in ("e", "F", "v", "R")]
    T = -R + 2 * s.diff(e * v, x) / e
    lhs = -e * f * T
    rhs = e * f * R + 2 * e * v * s.diff(f, x) - 2 * s.diff(e * f * v, x)
    zero("weighted_identity", lhs - rhs)
    mutation("omit_weighted_bulk_gradient", lhs - (rhs - 2 * e * v * s.diff(f, x)))

    n, K, T, e0 = s.symbols("n K T e", positive=True)
    rho, F = s.Function("rho")(n), s.Function("F")(n)
    mu = s.diff(rho, n) + K * T * s.diff(F, n)
    zero("current_stress_exchange", s.diff(mu, T) - K * s.diff(F, n))
    zero("current_stress_exchange", s.diff(-e0 * (rho + K * F * T), n, T) + e0 * K * s.diff(F, n))
    mutation("hold_F_independent_in_current", mu - s.diff(rho, n))
    # Projection identity in a locally inertial instantaneous fluid rest frame.
    eta = s.diag(-1, 1, 1, 1)
    u = s.Matrix([1, 0, 0, 0]); ud = eta * u
    rp, rpp, b, th = s.symbols("rho_prime rho_second b expansion", real=True)
    ng = s.symbols("dn0:4"); bg = s.symbols("db0:4")
    U = s.Matrix(4, 4, lambda a, c: 0 if c == 0 else s.Symbol(f"du{a}{c}", real=True))
    C = ng[0] + n * sum(U[i, i] for i in range(1, 4))
    m = rp + b
    mg = [rpp * ng[a] + bg[a] for a in range(4)]
    for nu in range(4):
        divergence = 0
        bare_divergence = 0
        for a in range(4):
            dr = (m + n * rpp) * ng[a] + n * bg[a]
            dp = (b + n * rpp) * ng[a] + n * bg[a]
            derivative = dr * ud[a] * ud[nu] + n * m * (U[a, a] * ud[nu] + ud[a] * U[a, nu]) + dp * eta[a, nu]
            bare = (rp + n * rpp) * ng[a] * ud[a] * ud[nu] + n * rp * (U[a, a] * ud[nu] + ud[a] * U[a, nu]) + n * rpp * ng[a] * eta[a, nu]
            divergence += eta[a, a] * derivative
            bare_divergence += eta[a, a] * bare
        curl = mg[0] * ud[nu] + m * U[0, nu] - mg[nu] * ud[0] - m * U[nu, 0]
        target = m * ud[nu] * C + n * curl + b * ng[nu]
        zero("current_stress_exchange", divergence - target)
        if nu == 1:
            mutation("omit_density_induced_pressure", bare_divergence - target)
    zero("constant_coefficient_recovery", mu.subs(F, s.Integer(1)).doit() - s.diff(rho, n))


def connection_equation() -> None:
    t, x, y, z = s.symbols("t x y z", real=True)
    coords = [t, x, y, z]
    a, N, f, B = s.Function("a")(t), s.Function("N")(t), s.Function("F_state")(t), s.Function("B")(x)

    def spin(E: s.Matrix, A: int, C: int) -> s.Expr:
        inv = E.inv()
        flux = [E.det() * sum((inv[nu, A] * inv[mu, C] - inv[nu, C] * inv[mu, A]) * s.diff(f, coords[mu]) / 2 for mu in range(4)) for nu in range(4)]
        return s.simplify(sum(s.diff(flux[nu], coords[nu]) for nu in range(4)))

    for A in range(4):
        for C in range(A + 1, 4):
            zero("connection_variation", spin(s.diag(N, a, a, a), A, C))
    witness = spin(s.diag(1, 1, B, 1), 0, 1)
    zero("connection_variation", witness + s.diff(B, x) * s.diff(f, t) / 2)
    CHECKS["connection_variation"].append(witness.equals(0) is False)
    zero("constant_coefficient_recovery", witness.subs(f, s.Integer(1)).doit())
    DETAILS["off_shell_connection_witness"] = str(witness)


def homogeneous_action() -> None:
    t = s.symbols("t", real=True)
    K, n = s.symbols("K n", positive=True)
    H, D = s.symbols("H D", real=True)
    a, N, j, theta = [s.Function(name)(t) for name in ("a", "N", "j", "theta")]
    rho, F = s.Function("rho"), s.Function("F")
    nv = j / a**3
    # Direct W54 torsion contractions for Cartesian diag(N,a,a,a).
    metric = [-N**2, a**2, a**2, a**2]
    torsion = {}
    for i in range(1, 4):
        torsion[i, 0, i] = s.diff(a, t) / a
        torsion[i, i, 0] = -s.diff(a, t) / a
    I1 = sum(metric[r] / (metric[m] * metric[v]) * value**2 for (r, m, v), value in torsion.items())
    I2 = sum(value * torsion.get((v, m, r), 0) / metric[m] for (r, m, v), value in torsion.items())
    trace = [sum(torsion.get((v, v, m), 0) for v in range(4)) for m in range(4)]
    TT = I1 / 4 + I2 / 2 - sum(trace[m]**2 / metric[m] for m in range(4))
    zero("lapse_preserving_dynamics", TT - 6 * (s.diff(a, t) / (N * a))**2)
    L = -K * N * a**3 * F(nv) * TT - N * a**3 * rho(nv) + j * s.diff(theta, t)

    def EL(lagrangian: s.Expr, q: s.Expr) -> s.Expr:
        return s.simplify(s.diff(lagrangian, q) - s.diff(s.diff(lagrangian, s.diff(q, t)), t))

    def reduce(expr: s.Expr) -> s.Expr:
        substitutions = {s.diff(j, t): 0, s.diff(N, t): 0, N: 1,
                         s.diff(a, t, 2): a * (D + H**2), s.diff(a, t): a * H, j: a**3 * n}
        return s.simplify(expr.subs(substitutions, simultaneous=True).doit())

    EN, EA, EJ, Eth = [EL(L, q) for q in (N, a, j, theta)]
    zero("lapse_preserving_dynamics", EN - a**3 * (6*K*F(nv)*(s.diff(a,t)/(N*a))**2 - rho(nv)))
    zero("lapse_preserving_dynamics", Eth + s.diff(j, t))
    zero("lapse_preserving_dynamics", reduce(EJ) - (s.diff(theta,t) - s.diff(rho(n),n) - 6*K*H**2*s.diff(F(n),n)))
    p = n * s.diff(rho(n), n) - rho(n)
    target = 2*F(n)*D + 3*(F(n)-n*s.diff(F(n),n))*H**2 + p/(2*K)
    zero("lapse_preserving_dynamics", reduce(EA)/(6*K*a**2) - target)
    h2 = rho(n)/(6*K*F(n))
    dH = -n*(s.diff(rho(n),n)-rho(n)*s.diff(F(n),n)/F(n))/(4*K*F(n))
    zero("lapse_preserving_dynamics", target.subs(D,dH).subs(H**2,h2))
    constraint_derivative = (6*K*s.diff(F(n),n)*H**2-s.diff(rho(n),n))*(-3*H*n)+12*K*F(n)*H*D
    zero("lapse_preserving_dynamics", constraint_derivative.subs(D,dH).subs(H**2,h2))
    zero("constant_coefficient_recovery", dH.subs(F(n),1).doit()+n*s.diff(rho(n),n)/(4*K))
    frozen_target = 2*F(n)*D + 3*F(n)*H**2 + p/(2*K)
    mutation("freeze_F_in_scale_variation", reduce(EA)/(6*K*a**2)-frozen_target)
    wrong_n = j/(N*a**3)
    wrong_L = -K*N*a**3*F(wrong_n)*TT-N*a**3*rho(wrong_n)+j*s.diff(theta,t)
    bad_density = reduce(EL(wrong_L,N)-EN)/a**3
    mutation("wrong_lapse_in_density", bad_density.subs({F(n):1,rho(n):n}).doit())
    CHECKS["lapse_preserving_dynamics"].append(s.simplify((6*K*F(n)*H**2-rho(n)).subs(H,0)) == -rho(n))
    DETAILS["homogeneous_dH_dproper_time"] = str(dH)
    DETAILS["flat_finite_density_bounce"] = "EXCLUDED when F,rho are finite and strictly positive"


def curvature_and_time() -> None:
    t, x, y, z = s.symbols("tau x y z", real=True)
    coords = [t,x,y,z]; a=s.Function("a")(t)
    gd = [-s.Integer(1),a**2,a**2,a**2]
    g = s.diag(*gd)
    Gamma = {}
    for r in range(4):
        for m in range(4):
            for v in range(4):
                value = s.simplify((s.diff(g[r,v],coords[m])+s.diff(g[r,m],coords[v])-s.diff(g[m,v],coords[r]))/(2*gd[r]))
                if value != 0: Gamma[r,m,v]=value
    def G(r,m,v): return Gamma.get((r,m,v),s.Integer(0))
    Riemann = {}
    for r in range(4):
        for b in range(4):
            for m in range(4):
                for v in range(4):
                    value=s.simplify(s.diff(G(r,v,b),coords[m])-s.diff(G(r,m,b),coords[v])+sum(G(r,m,k)*G(k,v,b)-G(r,v,k)*G(k,m,b) for k in range(4)))
                    if value != 0: Riemann[r,b,m,v]=value
    Ricci=s.Matrix(4,4,lambda b,v:sum(Riemann.get((r,b,r,v),0) for r in range(4)))
    scalar=sum(Ricci[i,i]/gd[i] for i in range(4))
    kretsch=sum(gd[r]*value**2/(gd[b]*gd[m]*gd[v]) for (r,b,m,v),value in Riemann.items())
    H=s.diff(a,t)/a; D=s.diff(H,t)
    zero("curvature_and_time_filter", scalar-6*(D+2*H**2))
    zero("curvature_and_time_filter", kretsch-12*((D+H**2)**2+H**4))
    zero("curvature_and_time_filter", Ricci[0,0]+Ricci[1,1]/a**2+2*D)
    momentum=s.symbols("momentum",positive=True)
    kt=momentum/a; kx=momentum/a**2
    zero("curvature_and_time_filter", -kt**2+a**2*kx**2)
    zero("curvature_and_time_filter", s.diff(kt,t)*kt+G(0,1,1)*kx**2)
    zero("curvature_and_time_filter", s.diff(kx,t)*kt+2*G(1,0,1)*kt*kx)
    n,h=s.symbols("n h",positive=True); delta=s.symbols("delta",real=True)
    hp=-h*n**(-delta/2); ndot=-3*hp*n; dp=s.diff(hp,n)*ndot
    zero("curvature_and_time_filter", dp-s.Rational(3,2)*delta*hp**2)
    proper_integrand=1/ndot
    affine_integrand=n**(-s.Rational(1,3))/ndot
    zero("curvature_and_time_filter", proper_integrand-n**(-1+delta/2)/(3*h))
    zero("curvature_and_time_filter", affine_integrand-n**(-s.Rational(4,3)+delta/2)/(3*h))
    decisions=[]
    for d in [-s.Integer(1),s.Integer(0),s.Rational(1,3),s.Rational(2,3),s.Integer(1)]:
        pr=s.integrate(3*h*proper_integrand.subs(delta,d),(n,1,s.oo))
        af=s.integrate(3*h*affine_integrand.subs(delta,d),(n,1,s.oo))
        Kp=12*((dp+hp**2)**2+hp**4)
        central_limit=s.limit(Kp.subs(delta,d),n,s.oo)
        CHECKS.setdefault("curvature_and_time_filter",[]).extend([
            (pr==s.oo)==bool(d>=0), (af==s.oo)==bool(d>=s.Rational(2,3)),
            (central_limit!=s.oo)==bool(d>=0)])
        decisions.append({"delta":str(d),"proper_integral":str(pr),"null_affine_integral":str(af),"curvature_limit":str(central_limit)})
    exp_affine=s.integrate(s.exp(-h*t),(t,0,s.oo))
    zero("curvature_and_time_filter",exp_affine-1/h)
    # Actual wrong time-map: integrating 1 instead of a gives infinity.
    wrong_affine=s.integrate(s.Integer(1),(t,0,s.oo))
    MUTATIONS["equate_affine_and_comoving_time"] = bool(wrong_affine==s.oo and exp_affine.is_finite)
    DETAILS["asymptotic_filter"]={"delta":"beta-gamma", "bounded_homogeneous_curvature_and_infinite_comoving_time":"delta >= 0", "infinite_radial_null_affine_length_in_patch":"delta >= 2/3", "exact_integral_crosschecks":decisions, "exponential_patch_null_affine_length":str(exp_affine)}


def main() -> None:
    before={name:digest(ROOT/name) for name in PINS}
    CHECKS["provenance"]=[digest(CONTRACT)==CONTRACT_SHA]+[before[k]==v for k,v in PINS.items()]
    density_variations(); weighted_and_current(); connection_equation()
    homogeneous_action(); curvature_and_time()
    after={name:digest(ROOT/name) for name in PINS}
    CHECKS["provenance"].append(before==after)
    CHECKS["mutation_controls"]=list(MUTATIONS.values())
    gates={key:bool(values and all(values)) for key,values in CHECKS.items()}
    passed=all(gates.values())
    output={"package":"W3-87-v1.0", "algebraic_verification":"PASS" if passed else "FAIL",
            "claim":"State-dependent-stiffness candidate: exact response and conditional contraction filters",
            "gates":gates,"check_counts":{k:len(v) for k,v in CHECKS.items()},
            "negative_controls":MUTATIONS,"details":DETAILS,
            "physical_status":{"density_geometry_coupling_verified":passed,
                "microscopic_F_derived":False,"generic_4d_health":False,
                "weak_field_observational_pass":False,"spherical_collapse_solved":False,
                "regular_black_hole":False,"global_completion":False,"singularity_resolved":False,
                "active_theory_changed":False,"intuitive_files_changed":False},
            "scope":"The F(n)T operator is an explicit constitutive candidate; no physical F was selected. Homogeneous patch tests are not a black-hole solution.",
            "provenance":{"contract":digest(CONTRACT),"verifier":digest(Path(__file__)),
                          "source_and_protected_hashes":after,"python":platform.python_version(),"sympy":s.__version__}}
    print(json.dumps(output,ensure_ascii=False,indent=2,allow_nan=False))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
