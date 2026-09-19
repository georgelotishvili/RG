"""FOUNDATION_TENSION_ENERGY_AUDIT_V1 -- stdout-only exact diagnostic.

Frozen target: distinguish the new scalar candidate's kinetic/gradient
response energy H_u from its retained pressure readout P_F=P_F0 p^2.
Verify the exchange sign, the separately scoped W75 density derivative,
and the obstruction to silently adding a derivative-free stored-energy
potential while retaining exact background scaling and a flat vacuum.

Domain: alpha>0, p>0, w=p^-2; unchanged scalar action and positive sextic
potential. W75 statements additionally use its own conserved-current
description, n/n0=p^5 and mu=d rho_C/dn>0. This density dictionary is not
imported into the scalar's fixed-coordinate-volume homogeneous cell.
No new EOS, pressure floor, fitted reservoir, gravity or observation is
introduced. The potential test concerns only an added term -W(u).

PASS: every exact residual vanishes and negative controls reject the
specified sign/readout errors. Physical constitutive closure is not a
PASS consequence. This script changes no existing artifact and writes
only to stdout; the candidate dependency is checked before and after.
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

    def gate(name, condition, witness):
        checks[name] = {"passed": bool(condition), "witness": str(witness)}

    before = digest(CANDIDATE)
    gate("candidate_unchanged_before", before == CANDIDATE_SHA256, before)
    t, x, y, z = s.symbols("t x y z", real=True)
    coordinates, spatial = (t, x, y, z), (x, y, z)
    alpha = s.symbols("alpha", positive=True)
    u, a, b = (s.Function(name)(*coordinates) for name in ("u", "a", "b"))

    def grad2(field):
        return sum(s.diff(field, c)**2 for c in spatial)

    def el(lagrangian, field):
        return (sum(s.diff(s.diff(lagrangian, s.diff(field, c)), c)
                    for c in coordinates)-s.diff(lagrangian, field))

    f2 = a*a+b*b
    potential = f2/2-f2*f2/4+f2**3/24
    kinetic = s.diff(a, t)**2+s.diff(b, t)**2
    lu = (s.exp(4*u)*s.diff(u, t)**2-grad2(u))/(2*alpha)
    lm = s.exp(4*u)*kinetic/2-(grad2(a)+grad2(b))/2-s.exp(2*u)*potential
    lagrangian = lu+lm
    source = s.diff(lm, u)
    hu = s.diff(u, t)*s.diff(lu, s.diff(u, t))-lu
    current = [s.diff(u, t)*s.diff(lu, s.diff(u, c)) for c in spatial]
    balance = s.diff(hu, t)+sum(s.diff(j, c) for j, c in zip(current, spatial))
    exact("foundation_energy_from_action",
          hu-(s.exp(4*u)*s.diff(u, t)**2+grad2(u))/(2*alpha))
    exact("foundation_exchange_off_shell",
          balance-s.diff(u, t)*el(lagrangian, u)-s.diff(u, t)*source)
    reservoir = s.Function("W")
    exact("added_potential_changes_variational_source",
          el(lagrangian-reservoir(u), u)-el(lagrangian, u)-s.diff(reservoir(u), u))
    # Uniform static vacuum: response energy vanishes at every background.
    background_u = s.symbols("u_background", real=True)
    exact("uniform_static_Hu_zero", hu.subs(u, background_u).doit())
    p, PF0 = s.symbols("p PF0", positive=True)
    pf = PF0*p*p
    gate("negative_control_Hu_equal_PF", pf.is_positive,
         "uniform static vacuum: H_u=0 but P_F=PF0*p^2>0")

    # Homogeneous initial data are free Cauchy data of the scalar candidate.
    # w=1, w_t=1, psi=1, psi_t=i, so V=7/24 and K=1.
    wh, ah, bh = (s.Function(name)(t) for name in ("w", "a_h", "b_h"))
    kh = s.diff(ah, t)**2+s.diff(bh, t)**2
    magnitude = ah*ah+bh*bh
    vh = magnitude/2-magnitude*magnitude/4+magnitude**3/24
    lhom = s.diff(wh, t)**2/(8*alpha)+wh*wh*kh/2-wh*vh
    wh_el = s.diff(s.diff(lhom, s.diff(wh, t)), t)-s.diff(lhom, wh)
    wh_tt = 4*alpha*(wh*kh-vh)
    exact("homogeneous_w_equation_from_action",
          wh_el-(s.diff(wh, t, 2)-wh_tt)/(4*alpha))
    xchange = s.diff(wh, t)*(wh*kh-vh)
    hu_hom = s.diff(wh, t)**2/(8*alpha)
    exact("homogeneous_foundation_exchange",
          s.diff(hu_hom, t).subs(s.diff(wh, t, 2), wh_tt)-xchange)
    witness = {wh: 1, s.diff(wh, t): 1, ah: 1, bh: 0,
               s.diff(ah, t): 0, s.diff(bh, t): 1}
    actual_pressure_rate = s.diff(1/wh, t).subs(witness)
    actual_exchange = xchange.subs(witness)
    exact("witness_potential", vh.subs(witness)-s.Rational(7, 24))
    exact("witness_pressure_rate", actual_pressure_rate+1)
    exact("witness_positive_exchange", actual_exchange-s.Rational(17, 24))
    exact("witness_nonzero_charge",
          (wh*wh*(ah*s.diff(bh, t)-bh*s.diff(ah, t))).subs(witness)-1)
    sign_flip_residual = 2*actual_exchange
    gate("negative_control_reversed_exchange", sign_flip_residual != 0,
         "actual H_u,t - (-X) = "+str(sign_flip_residual))

    # W75's own current/volume dictionary, without transferring its n into
    # the distinct scalar fixed-coordinate-volume cell.
    n, n0, mu, volume, count, volume0 = s.symbols(
        "n n0 mu volume N_C volume0", positive=True)
    rho = s.Function("rho_C")
    density_map = n0*p**5
    derivative = s.diff(rho(density_map), p)/s.diff(pf, p)
    expected_derivative = (5*density_map/(2*pf)
                           *s.diff(rho(n), n).subs(n, density_map))
    exact("W75_density_pressure_derivative", derivative-expected_derivative)
    gate("W75_density_derivative_positive_under_mu",
         (5*n*mu/(2*PF0*p*p)).is_positive, "n,mu,PF0,p>0")
    extensive = volume*rho(count/volume)
    pressure = n*s.diff(rho(n), n)-rho(n)
    exact("fixed_medium_charge_first_law",
          s.diff(extensive, volume)+pressure.subs(n, count/volume))
    exact("scalar_cell_conserved_density_map",
          n0*p**3*(volume0*p**-3)-n0*volume0)
    exact("importing_W75_map_changes_scalar_cell_charge",
          density_map*(volume0*p**-3)-n0*volume0*p*p)
    gate("negative_control_imported_density_dictionary",
         s.diff(density_map*volume0*p**-3, p).is_positive,
         "fixed scalar coordinate volume plus n=n0*p^5 gives N_C=n0*volume0*p^2, not constant")

    # A coordinate potential must share the inherited action weight.
    U, delta, C = s.symbols("U delta C", real=True)
    scale_residual = reservoir(U+delta)-s.exp(2*delta)*reservoir(U)
    generator = s.diff(scale_residual, delta).subs(delta, 0).doit()
    exact("potential_scaling_generator",
          generator-(s.diff(reservoir(U), U)-2*reservoir(U)))
    allowed = C*s.exp(2*U)
    exact("potential_scaling_solution", s.diff(allowed, U)-2*allowed)
    exact("potential_finite_scaling",
          allowed.subs(U, U+delta)-s.exp(2*delta)*allowed)
    exact("allowed_potential_local_density_constant", s.exp(-2*U)*allowed-C)
    flat_force = s.diff(allowed, U).subs(U, 0)
    exact("flat_static_vacuum_force", flat_force-2*C)
    gate("flat_static_vacuum_forces_zero_potential",
         s.solve(s.Eq(flat_force, 0), C) == [0], "2C=0 requires C=0")
    subtracted = allowed-allowed.subs(U, 0)
    exact("constant_subtraction_leaves_vacuum_force",
          s.diff(subtracted, U).subs(U, 0)-2*C)
    corrected = subtracted-2*C*U
    exact("tadpole_subtraction_flattens_vacuum", s.diff(corrected, U).subs(U, 0))
    wrong_scale = (corrected.subs(U, U+delta)-s.exp(2*delta)*corrected)
    control = wrong_scale.subs({U: 0, delta: s.log(2), C: 1})
    gate("negative_control_tadpole_breaks_scaling", control != 0, control)

    # Finite-energy stationary virial with a hypothetical added W.
    # Integrals T,G,V,F,Wint,Wprime stand for their full spatial values.
    Tint, Gint, Vint, Fint, Wint, Wprime = s.symbols("T G V F Wint Wprime")
    lam = s.symbols("lambda", positive=True)
    dilated_action = lam**3*(Tint-Vint-Wint)-lam*(Gint+Fint)
    virial = s.diff(dilated_action, lam).subs(lam, 1)
    exact("potential_virial_from_dilation",
          virial-(3*(Tint-Vint-Wint)-Gint-Fint))
    energy = Tint+Gint+Vint+Fint+Wint
    mass = 4*Tint-2*Vint-Wprime
    mass_minus_energy = (mass-energy).subs(Gint, 3*(Tint-Vint-Wint)-Fint)
    exact("potential_on_shell_mass_difference", mass_minus_energy-(2*Wint-Wprime))
    exact("allowed_potential_preserves_virial_identity",
          mass_minus_energy.subs(Wprime, 2*Wint))
    gate("candidate_unchanged_after", digest(CANDIDATE) == before, digest(CANDIDATE))

    failed = [name for name, item in checks.items() if not item["passed"]]
    passed = not failed
    return {
        "claim_id": "FOUNDATION_TENSION_ENERGY_AUDIT_V1",
        "passed": passed, "check_count": len(checks), "failed": failed,
        "decision": "RESPONSE_ENERGY_DISTINCT_FROM_STORED_TENSION_NO_SILENT_RESERVOIR",
        "results": {
            "scalar_energy": "H_u=(w_t^2+|grad w|^2/w^2)/(8alpha) is response energy, not P_F",
            "pressure": "P_F=P_F0/w; uniform static H_u=0 at arbitrary positive P_F",
            "admissible_initial_witness": {
                "w": 1, "w_t": 1, "a": 1, "b": 0, "a_t": 0, "b_t": 1,
                "potential": "7/24", "charge_density": 1,
                "P_F_t_over_P_F0": str(actual_pressure_rate),
                "energy_transfer_to_response_sector": str(actual_exchange),
            },
            "W75": "d rho_C/dP_F=5n mu/(2P_F)>0 within its n/n0=p^5, mu>0 homogeneous-current class",
            "extensive_energy": "at fixed medium charge N_C, d(rho_C V)=-Pi_C dV, Pi_C=n rho_C'-rho_C; sign depends on Pi_C and dV",
            "dictionary_boundary": "scalar fixed coordinate cell has Vproper proportional p^-3; the same conserved N_C would imply n proportional p^3, not p^5",
            "potential_obstruction": [
                "Exact background action weight requires W(u+delta)=exp(2delta)W(u), hence W'=2W and W=C exp(2u).",
                "Writing W=sqrt(-g)rho gives rho=C: this allowed coordinate potential is constant local energy density.",
                "An asymptotically flat static vacuum u=0 requires W'(0)=0, hence C=0.",
                "Subtracting a constant leaves the vacuum force 2C; subtracting its tadpole breaks the exact scaling symmetry.",
                "For a localized on-shell static solution with finite potential integrals, M-E=integral(2W-W')d^3x.",
            ],
        },
        "closure_flags": {
            "response_energy_interpretation_audited": passed,
            "original_exchange_sign_verified": passed,
            "W75_local_density_monotonicity_conditional": passed,
            "single_potential_shortcut_obstruction": passed,
            "stored_foundation_tension_energy_law_derived": False,
            "new_EOS_adopted": False,
            "scalar_and_W75_actions_identified": False,
            "full_RefG_closure": False,
            "observational_pass": False,
            "singularity_resolution": False,
        },
        "checks": checks,
        "provenance": {"candidate_sha256": before, "self_sha256": digest(Path(__file__)),
                       "python": sys.version.split()[0], "sympy": s.__version__},
        "writes_files": False,
    }


if __name__ == "__main__":
    report = run()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["passed"] else 1)
