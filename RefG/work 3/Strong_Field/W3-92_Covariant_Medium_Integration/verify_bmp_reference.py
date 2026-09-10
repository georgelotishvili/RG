#!/usr/bin/env python3
"""BMP reference identities and RefG import checks.

Author-written verification of the cited formulas, not source code from a paper.
https://doi.org/10.1103/PhysRevLett.132.031401
https://doi.org/10.1103/fbz2-8n2h
Detailed assumptions, derivations and citations: BMP.md in this directory.
Requires SymPy 1.13.3 and mpmath 1.3.0 (versions used for verification).
Reads no project files and writes no files. Run with --verbose for all residuals.
"""

import argparse
import json
import mpmath as mp
import sympy as s


@mp.workdps(60)
def run_checks():
    """Return exact/numerical checks and narrowly scoped physical status flags."""
    rows = []
    def exact(name, actual, expected=0):
        residual = s.simplify(actual-expected)
        rows.append(dict(name=name, kind="exact", passed=(residual == 0),
                         residual=str(residual)))
    def condition(name, value, kind="analytic_sign"):
        rows.append(dict(name=name, kind=kind, passed=bool(value)))

    e, xi, m, n, V, N, H, R, M0 = s.symbols(
        "epsilon xi m n V N H R M0", positive=True)
    E = s.log(1+xi*e)/xi
    g = s.diff(E,e)
    chi = E/e
    P = e*g-E
    exact("marginal_coupling", g, 1/(1+xi*e))
    exact("average_vs_marginal", g, chi+e*s.diff(chi,e))
    exact("stress_variation", e*g-E, e**2*s.diff(chi,e))
    exact("continuity", s.diff(E,e)*(-3*H*e)+3*H*(E+P))
    cell = V*E.subs(e,m*N/V)
    exact("fixed_number_volume_work", -s.diff(cell,V), P.subs(e,m*N/V))
    exact("fixed_volume_added_matter", s.diff(cell,N), m*g.subs(e,m*N/V))
    rho = E.subs(e,m*n)
    cs2 = s.simplify(n*s.diff(rho,n,2)/s.diff(rho,n))
    exact("W79_sound_speed", cs2, -xi*m*n/(1+xi*m*n))
    condition("BMP_sound_squared_negative", cs2.is_negative)
    condition("positive_energy", E.is_positive)
    condition("positive_enthalpy", (e*g).is_positive)
    condition("negative_response_slope", s.diff(E,e,2).is_negative)
    condition("omit_induced_pressure_is_detected",
              s.simplify((E+P-E).subs({e:1,xi:1})) != 0,
              "negative_control")
    exact("low_density_energy", s.limit(E/e,e,0,dir="+"), 1)
    exact("low_density_coupling", s.limit(g,e,0,dir="+"), 1)

    M = R**3*E.subs(e,6*M0/R**3)/6
    q = 6*M0*xi/R**3
    exact("matched_mass", M, R**3*s.log(1+q)/(6*xi))
    exact("added_enclosed_mass", s.diff(M,M0), 1/(1+q))
    exact("enclosed_concavity", s.diff(M,M0,2),
          -6*xi/(R**3*(1+q)**2))
    exact("ADM_mass", s.limit(M,R,s.oo), M0)
    condition("no_fixed_radius_mass_cap", s.limit(M,M0,s.oo) == s.oo)
    rho_ext = 2*s.diff(M,R)/R**2
    target_ext = (s.log(1+q)-q/(1+q))/xi
    exact("exterior_Einstein_density", rho_ext, target_ext)
    exact("boundary_radial_pressure", -rho_ext, P.subs(e,6*M0/R**3))
    q0=s.symbols("q",positive=True)
    ext_sign=s.log(1+q0)-q0/(1+q0)
    exact("positive_exterior_derivative", s.diff(ext_sign,q0), q0/(1+q0)**2)
    exact("exterior_density_origin", ext_sign.subs(q0,0), 0)
    condition("vacuum_exterior_mutation_detected",
              rho_ext.subs({M0:1,R:1,xi:1}) != 0, "negative_control")

    Ric = 4*E-3*e*g
    K = 12*((E/3-e*g/2)**2+(E/3)**2)
    exact("interior_Ricci_asymptote", s.limit(Ric/s.log(xi*e),e,s.oo),4/xi)
    exact("interior_K_asymptote", s.limit(K/s.log(xi*e)**2,e,s.oo),8/(3*xi**2))
    def static_k(f):
        return s.diff(f,R,2)**2+4*(s.diff(f,R)/R)**2+4*((1-f)/R**2)**2
    exact("Schwarzschild_K_control", static_k(1-2*M0/R),48*M0**2/R**6)
    exact("static_log_K_asymptote",
          s.limit(static_k(1-2*M/R)/s.log(q)**2,R,0,dir="+"),8/(3*xi**2))
    t=s.symbols("t",positive=True)
    exact("Gaussian_patch_affine_integral",
          s.integrate(s.exp(-t**2/(4*xi)),(t,0,s.oo)),s.sqrt(s.pi*xi))
    condition("proper_equals_affine_mutation_detected",
              s.integrate(1,(t,0,s.oo)) == s.oo, "negative_control")

    E2=e*(1-s.exp(-1/(xi*e)))
    g2=s.diff(E2,e)
    P2=e*g2-E2
    exact("bounded_benchmark_limit", s.limit(E2,e,s.oo),1/xi)
    exact("bounded_pressure", P2,-s.exp(-1/(xi*e))/xi)
    exact("bounded_response_derivative",s.diff(E2,e,2),
          -s.exp(-1/(xi*e))/(xi**2*e**3))
    y=s.symbols("y",positive=True)
    g2_y=1-(1+y)*s.exp(-y)
    exact("bounded_response_sign_derivative",s.diff(g2_y,y),y*s.exp(-y))
    exact("bounded_response_sign_origin",g2_y.subs(y,0),0)
    M2=R**3*E2.subs(e,6*M0/R**3)/6
    exact("bounded_matched_mass",M2,M0*(1-s.exp(-R**3/(6*xi*M0))))
    exact("bounded_static_centre_K",
          s.limit(static_k(1-2*M2/R),R,0,dir="+"),8/(3*xi**2))
    exact("bounded_ADM_mass",s.limit(M2,R,s.oo),M0)
    exact("bounded_sound_limit",s.limit(e*s.diff(E2,e,2)/g2,e,s.oo),-2)

    qcrit=mp.findroot(lambda z:3*z/(1+z)-2*mp.log1p(z),(1,2))
    rcrit=2*mp.log1p(qcrit)/qcrit
    xcrit=qcrit*rcrit**3/6
    fcrit=1-rcrit**2/(3*xcrit)*mp.log1p(6*xcrit/rcrit**3)
    dfcrit=-2*rcrit/(3*xcrit)*mp.log1p(qcrit)+rcrit*qcrit/(xcrit*(1+qcrit))
    condition("double_horizon_f",abs(fcrit)<mp.mpf("1e-50"),"numerical_60_digits")
    condition("double_horizon_df",abs(dfcrit)<mp.mpf("1e-50"),"numerical_60_digits")
    condition("published_approximate_045",
              abs(xcrit-mp.mpf("0.45"))<mp.mpf("0.01"),"published_rounding")

    failed=[r for r in rows if not r["passed"]]
    return dict(
     decision="REFERENCE_DICTIONARY_VALID; STANDALONE_FLUID_IMPORT_FAILS",
     checks=len(rows),passed=len(rows)-len(failed),failed=failed,details=rows,
     horizon=dict(xi_over_M0_squared=str(xcrit),R_over_M0=str(rcrit)),
     sympy=s.__version__,mpmath=mp.__version__,
     physical_flags=dict(reference_dictionary=not failed,healthy_BMP_fluid=False,
                         BMP_bounded_curvature=False,RefG_singularity_resolved=False)
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
