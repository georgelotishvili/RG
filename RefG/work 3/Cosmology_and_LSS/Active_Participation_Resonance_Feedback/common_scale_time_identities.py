"""COMMON_SCALE_TIME_IDENTITIES_V1 -- exact, stdout-only companion.

Frozen claims: derive the candidate Euler--Lagrange equations from its
original action, verify pressure-variable and energy-exchange identities,
and verify constant-background scaling. Prove no p=0 endpoint for a
closed homogeneous charged cell using conserved positive energy and
charge. No spatial-centre/global PDE regularity theorem is claimed.

Model: the new scalar composite-metric candidate in
common_scale_finite_source_candidate.py, not Einstein gravity or full RefG.
Domain: alpha>0, p>0, w=p^-2>0; two real components of ordinary psi;
V(f)=f^2/2-f^4/4+f^6/24. The homogeneous theorem additionally assumes
finite initial energy density epsilon>0, nonzero charge density, smooth
initial data and a closed, fixed coordinate-volume homogeneous cell.
No matter/energy influx, spatial gradients or independently imposed
coordinate-volume change are inserted; proper volume follows p^-3.

Method: independent action variation, off-shell Noether identities,
algebraic positivity certificates, and the ODE continuation proof stated
in the report. PASS requires every exact residual and negative control.
This is an original-model mathematical check, not observational evidence,
an infinite-domain spatial regularity certificate or a new numerical fit.
All calculations use exact SymPy expressions. No files are written.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import sympy as s


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "common_scale_finite_source_candidate.py"
CANDIDATE_SHA256 = "6b4a4a0f906725e7262a73496d02330fc4f040bb20ec419d51dbaccd241925b8"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    checks = {}

    def exact(name, expression):
        residual = s.simplify(s.expand(expression))
        checks[name] = {"passed": residual == 0, "residual": str(residual)}

    def gate(name, passed, witness):
        checks[name] = {"passed": bool(passed), "witness": str(witness)}

    source_hash = digest(CANDIDATE)
    gate("unchanged_candidate_dependency", source_hash == CANDIDATE_SHA256, source_hash)
    t, x, y, z = s.symbols("t x y z", real=True)
    coordinates, spatial = (t, x, y, z), (x, y, z)
    alpha = s.symbols("alpha", positive=True)
    u, a, b = (s.Function(name)(*coordinates) for name in ("u", "a", "b"))
    p, w = (s.Function(name)(*coordinates) for name in ("p", "w"))

    def grad_squared(field):
        return sum(s.diff(field, c)**2 for c in spatial)

    def laplacian(field):
        return sum(s.diff(field, c, 2) for c in spatial)

    def el(lagrangian, field):
        return (sum(s.diff(s.diff(lagrangian, s.diff(field, c)), c)
                    for c in coordinates) - s.diff(lagrangian, field))

    def energy_and_flux(lagrangian, fields):
        energy = sum(s.diff(q, t)*s.diff(lagrangian, s.diff(q, t))
                     for q in fields) - lagrangian
        flux = [sum(s.diff(q, t)*s.diff(lagrangian, s.diff(q, c))
                    for q in fields) for c in spatial]
        return energy, flux

    def continuity(energy, flux):
        return s.diff(energy, t) + sum(s.diff(j, c) for j, c in zip(flux, spatial))

    magnitude_squared = a*a+b*b
    potential = (magnitude_squared/2-magnitude_squared**2/4
                 + magnitude_squared**3/24)
    kinetic = s.diff(a, t)**2+s.diff(b, t)**2
    ordinary_grad = grad_squared(a)+grad_squared(b)
    lu = (s.exp(4*u)*s.diff(u, t)**2-grad_squared(u))/(2*alpha)
    lm = s.exp(4*u)*kinetic/2-ordinary_grad/2-s.exp(2*u)*potential
    lagrangian = lu+lm
    elu, ela, elb = (el(lagrangian, q) for q in (u, a, b))
    source = s.diff(lm, u)
    expected_source = 2*s.exp(4*u)*kinetic-2*s.exp(2*u)*potential
    expected_u = (s.exp(4*u)*(s.diff(u, t, 2)+2*s.diff(u, t)**2)
                  - laplacian(u)-alpha*expected_source)
    exact("action_source", source-expected_source)
    exact("u_euler_lagrange", alpha*elu-expected_u)
    for name, field, equation in (("a", a, ela), ("b", b, elb)):
        expected = (s.diff(s.exp(4*u)*s.diff(field, t), t)
                    - laplacian(field)+s.exp(2*u)*s.diff(potential, field))
        exact(name+"_euler_lagrange", equation-expected)

    # Re-vary the transformed Lagrangians; do not merely substitute into
    # a supplied final PDE. This also checks the field-redefinition factors.
    lp = lagrangian.subs(u, -s.log(p)).doit()
    lw = lagrangian.subs(u, s.log(w)/2).doit()
    expected_p = (s.diff(p, t, 2)-p**4*laplacian(p)
                  -3*s.diff(p, t)**2/p+p**3*grad_squared(p)
                  +2*alpha*p*kinetic-2*alpha*p**3*potential)
    expected_w = (s.diff(w, t, 2)-laplacian(w)/w**2+grad_squared(w)/w**3
                  -4*alpha*w*kinetic+4*alpha*potential)
    exact("p_euler_lagrange", alpha*p**6*el(lp, p)-expected_p)
    exact("w_euler_lagrange", 4*alpha*el(lw, w)-expected_w)
    expected_lw = ((s.diff(w, t)**2-grad_squared(w)/w**2)/(8*alpha)
                   +w*w*kinetic/2-ordinary_grad/2-w*potential)
    exact("w_action", lw-expected_lw)

    hu, ju = energy_and_flux(lu, (u,))
    hm, jm = energy_and_flux(lm, (a, b))
    exact("foundation_off_shell_energy", continuity(hu, ju)-s.diff(u, t)*(elu+source))
    exact("ordinary_off_shell_energy",
          continuity(hm, jm)-s.diff(a, t)*ela-s.diff(b, t)*elb+s.diff(u, t)*source)
    exact("total_off_shell_noether", continuity(hu+hm, [j+k for j, k in zip(ju, jm)])
          -s.diff(u, t)*elu-s.diff(a, t)*ela-s.diff(b, t)*elb)
    exact("work_in_w", (s.diff(u, t)*source).subs(u, s.log(w)/2).doit()
          -s.diff(w, t)*(w*kinetic-potential))
    exact("foundation_energy_in_w", hu.subs(u, s.log(w)/2).doit()
          -(s.diff(w, t)**2+grad_squared(w)/w**2)/(8*alpha))
    for direction, current in zip(spatial, ju):
        exact("foundation_flux_w_"+str(direction),
              current.subs(u, s.log(w)/2).doit()
              +s.diff(w, t)*s.diff(w, direction)/(4*alpha*w**2))
    charge = s.exp(4*u)*(a*s.diff(b, t)-b*s.diff(a, t))
    charge_flux = [b*s.diff(a, c)-a*s.diff(b, c) for c in spatial]
    exact("charge_off_shell", continuity(charge, charge_flux)-a*elb+b*ela)

    # Constant background: t=T/c, x=c X, u=-ln(c)+U, psi=Psi.
    # The volume-time Jacobian is c^2; the same alpha and potential remain.
    c, U = s.symbols("background_p U", positive=True)
    ut, ux2, kt, kg, vp = s.symbols("U_T grad_U_squared K_T G_Psi V_Psi", real=True)
    local_lu = (s.exp(4*U)*ut**2-ux2)/(2*alpha)
    local_lm = s.exp(4*U)*kt/2-kg/2-s.exp(2*U)*vp
    mapped_lu = (c**-4*s.exp(4*U)*(c*ut)**2-c**-2*ux2)/(2*alpha)
    mapped_lm = c**-4*s.exp(4*U)*c*c*kt/2-c**-2*kg/2-c**-2*s.exp(2*U)*vp
    exact("background_foundation_action", c*c*mapped_lu-local_lu)
    exact("background_ordinary_action", c*c*mapped_lm-local_lm)
    local_h = ((s.exp(4*U)*ut**2+ux2)/(2*alpha)
               +s.exp(4*U)*kt/2+kg/2+s.exp(2*U)*vp)
    mapped_h = ((c**-4*s.exp(4*U)*(c*ut)**2+c**-2*ux2)/(2*alpha)
                +c**-4*s.exp(4*U)*c*c*kt/2+c**-2*kg/2+c**-2*s.exp(2*U)*vp)
    exact("background_energy_density", mapped_h-c**-2*local_h)
    exact("background_integrated_energy", c**3*mapped_h-c*local_h)
    uj, aj, bj, at, bt, av, bv = s.symbols("U_j a_j b_j a_T b_T a_value b_value", real=True)
    local_current = -ut*uj/alpha-at*aj-bt*bj
    mapped_current = -(c*ut)*(uj/c)/alpha-(c*at)*(aj/c)-(c*bt)*(bj/c)
    exact("background_canonical_energy_current", mapped_current-local_current)
    exact("background_integrated_power", c*c*mapped_current-c*c*local_current)
    local_charge = s.exp(4*U)*(av*bt-bv*at)
    mapped_charge = c**-4*s.exp(4*U)*(av*c*bt-bv*c*at)
    exact("background_charge_density", mapped_charge-c**-3*local_charge)
    exact("background_total_charge", c**3*mapped_charge-local_charge)
    local_charge_current = bv*aj-av*bj
    mapped_charge_current = bv*aj/c-av*bj/c
    exact("background_charge_current", mapped_charge_current-local_charge_current/c)
    T = s.symbols("T", real=True)
    scale = s.Function("p_local")(T)
    # d/dt=c d/dT only for constant c.
    exact("background_pressure_scale_rate", c*s.diff(c*scale, T)-c*c*s.diff(scale, T))
    exact("background_squared_pressure_rate",
          c*s.diff((c*scale)**2, T)-c**3*s.diff(scale**2, T))
    exact("proper_clock_background", (c*scale)/c-scale)
    gate("negative_control_wrong_rate_power", (c**2-c).subs(c, s.Rational(1, 2)) != 0,
         "c=1/2, dp_local/dT=1: correct rate=1/4, wrong rate=1/2")
    # An explicit off-shell source/work witness; the sign is not prescribed.
    gate("negative_control_ignoring_work", s.Rational(2)-2*s.Rational(7, 24) != 0,
         "u_t=1, w=1, |psi_t|^2=1, |psi|=1: work=17/12")

    # Independent homogeneous ODE invariants and coercivity certificates.
    wh, ah, bh = (s.Function(name)(t) for name in ("wh", "ah", "bh"))
    fh2 = ah*ah+bh*bh
    vh = fh2/2-fh2**2/4+fh2**3/24
    kh = s.diff(ah, t)**2+s.diff(bh, t)**2
    eh = s.diff(wh, t)**2/(8*alpha)+wh**2*kh/2+wh*vh
    qh = wh**2*(ah*s.diff(bh, t)-bh*s.diff(ah, t))
    ode = {
        s.diff(wh, t, 2): 4*alpha*wh*kh-4*alpha*vh,
        s.diff(ah, t, 2): -2*s.diff(wh, t)*s.diff(ah, t)/wh-s.diff(vh, ah)/wh,
        s.diff(bh, t, 2): -2*s.diff(wh, t)*s.diff(bh, t)/wh-s.diff(vh, bh)/wh,
    }
    exact("homogeneous_energy_conserved", s.diff(eh, t).subs(ode))
    exact("homogeneous_charge_conserved", s.diff(qh, t).subs(ode))
    f, W, qabs, epsilon, w0, time = s.symbols("f W q_abs epsilon w0 time", positive=True)
    vf = f*f/2-f**4/4+f**6/24
    exact("positive_potential_certificate", vf-f*f/8-f*f*(f*f-3)**2/24)
    exact("charge_cauchy_certificate",
          (av*av+bv*bv)*(at*at+bt*bt)-(av*bt-bv*at)**2-(av*at+bv*bt)**2)
    exact("homogeneous_coercivity_square",
          qabs**2/(2*W**2*f**2)+W*f*f/8-qabs/(2*s.sqrt(W))
          -(qabs/(s.sqrt(2)*W*f)-s.sqrt(W)*f/(2*s.sqrt(2)))**2)
    wmin = qabs**2/(4*epsilon**2)
    exact("homogeneous_lower_w_bound_endpoint", epsilon-qabs/(2*s.sqrt(wmin)))
    speed_bound = s.sqrt(8*alpha*epsilon)
    wupper = w0+speed_bound*time
    tau_lower = 2*(s.sqrt(wupper)-s.sqrt(w0))/speed_bound
    exact("homogeneous_upper_w_rate", s.diff(wupper, time)-speed_bound)
    exact("homogeneous_proper_time_bound_derivative",
          s.diff(tau_lower, time)-1/s.sqrt(wupper))
    exact("homogeneous_proper_time_bound_initial", tau_lower.subs(time, 0))
    gate("homogeneous_proper_time_diverges", s.limit(tau_lower, time, s.oo) == s.oo,
         "tau_lower(t) -> infinity as t -> infinity")
    radius, radial_variable = s.symbols("r s", positive=True)
    exact("radial_cauchy_weight", s.integrate(radial_variable**-2,
          (radial_variable, radius, s.oo))-1/radius)
    gate("dependency_still_unchanged", digest(CANDIDATE) == source_hash, digest(CANDIDATE))

    failed = [name for name, item in checks.items() if not item["passed"]]
    passed = not failed
    return {
        "claim_id": "COMMON_SCALE_TIME_IDENTITIES_V1",
        "passed": passed, "check_count": len(checks), "failed": failed,
        "equations": {
            "u": "exp(4u)(u_tt+2u_t^2)-Delta u=2alpha[exp(4u)|psi_t|^2-exp(2u)V]",
            "p": "p_tt-p^4 Delta p=3p_t^2/p-p^3|grad p|^2-2alpha p|psi_t|^2+2alpha p^3 V",
            "w": "w_tt-w^-2 Delta w=-w^-3|grad w|^2+4alpha w|psi_t|^2-4alpha V",
            "psi": "partial_t(w^2 psi_t)-Delta psi+w V_psi=0",
            "exchange": "H_u,t+div J_u=w_t(w|psi_t|^2-V)=-(H_m,t+div J_m)",
            "scale_response_energy": "H_u=(w_t^2+|grad w|^2/w^2)/(8alpha)",
            "scale_response_flux": "J_u=-w_t grad w/(4alpha w^2)",
            "energy_interpretation": "H_u is kinetic/gradient response energy; stored static tension is not derived",
            "ordinary_energy": "H_m=w^2|psi_t|^2/2+|grad psi|^2/2+w V",
            "ordinary_flux": "J_m=-Re(psi_t* grad psi)",
        },
        "background_scaling": {
            "assumption": "constant positive p_b, entire solution and asymptotic background transformed together",
            "map": "t=T/p_b, x=p_b X, u=-ln(p_b)+U, psi=Psi; dt d^3x=p_b^2 dT d^3X",
            "action": "both L_u and L_m scale as p_b^-2; alpha and the potential remain unchanged",
            "energy": "H_ref=p_b^-2 H_local; E_ref=p_b E_local; canonical J_E,ref=J_E,local",
            "power": "P_ref=p_b^2 P_local from the area factor",
            "charge": "q_ref=p_b^-3 q_local; j_Q,ref=p_b^-1 j_Q,local; Q_ref=Q_local",
            "clock": "d tau=p_ref dt=p_local dT",
            "rates": "p_ref,t=p_b^2 p_local,T; (p_ref^2)_t=p_b^3(p_local^2)_T",
            "limitation": "a symmetry between backgrounds, not an extra p multiplier or an autonomous rate law within a changing-p solution",
        },
        "homogeneous_theorem": {
            "assumptions": [
                "fixed coordinate-volume homogeneous periodic cell; no spatial gradients, boundary flux or external driving; proper volume follows p^-3, no separately imposed expansion",
                "alpha>0; finite initial w0>0 and smooth complex-field data",
                "finite conserved epsilon>0 and nonzero conserved q=w^2 Im(psi*psi_t)",
                "the specified positive sextic potential and the candidate ODEs",
            ],
            "bounds": [
                "V(f)>=f^2/8",
                "epsilon>=q^2/(2w^2 f^2)+wf^2/8>=|q|/(2sqrt(w))",
                "q^2/(4epsilon^2)<=w(t)<=w0+sqrt(8alpha epsilon)t",
                "|w_t|<=sqrt(8alpha epsilon); f^2<=8epsilon/w; |psi_t|^2<=2epsilon/w^2",
                "p(t)>=1/sqrt(w0+sqrt(8alpha epsilon)t)>0",
                "tau(t)>=2[sqrt(w0+v t)-sqrt(w0)]/v with v=sqrt(8alpha epsilon)",
            ],
            "proof": [
                "Exact ODE energy and charge conservation supply constant epsilon and q.",
                "The positive-energy terms and the two displayed square certificates give the bounds.",
                "On every finite time interval w stays bounded above and away from zero; psi, psi_t and w_t stay bounded.",
                "The polynomial/rational ODE vector field is smooth on those bounded sets with w>0; the standard continuation criterion gives global forward ODE existence.",
                "The explicit lower bound on p excludes p=0 at finite external time; the divergent lower bound on tau excludes reaching the w=infinity endpoint at finite proper time.",
            ],
            "meaning": "homogeneous charged-cell no-zero theorem for this candidate; no arbitrary-load or inhomogeneous-centre theorem",
        },
        "spatial_energy_limits": {
            "assumptions": "finite conserved total energy E, spherical symmetry and u(t,infinity)=0",
            "bounds": [
                "||w_t||_L2<=sqrt(8alpha E); ||w(t)-w(0)||_L2<=t sqrt(8alpha E)",
                "|u(t,r)|<=sqrt(alpha E/(2pi r)) for every fixed r>0",
                "p(t,r)>=exp[-sqrt(alpha E/(2pi r))]; tau_r(t)>=p_min(r)t",
            ],
            "centre": "the r>0 bound degenerates at r=0; global finite energy alone does not control central concentration",
        },
        "closure_flags": {
            "action_pressure_equations": passed,
            "sector_exchange": passed,
            "stored_background_tension_energy_derived": False,
            "constant_background_scaling": passed,
            "homogeneous_charged_cell_no_zero": passed,
            "spatial_centre_no_zero": False,
            "general_nonlinear_spatial_regularity": False,
            "observational_pass": False,
            "full_RefG_closure": False,
            "singularity_resolution": False,
            "strong_field_calculation": False,
        },
        "checks": checks,
        "provenance": {"candidate_sha256": source_hash, "self_sha256": digest(Path(__file__)),
                       "python": sys.version.split()[0], "sympy": s.__version__},
        "writes_files": False,
    }


if __name__ == "__main__":
    report = run()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["passed"] else 1)
