"""Existing oscillon exchange: local versus external clocks, stdout only.

No strong-field calculation, new interaction, or pressure evolution.
See oscillon_clock_transfer_audit.md for the frozen scope and proof.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import sympy as s

HERE = Path(__file__).resolve().parent
W76 = HERE / "w3_76_same_field_resonant_exchange.py"
W76_HASH = "c3ad4b140c7b89a3e6d587b6b46480db1da0bb94b6b5307a32237df876285a6f"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit():
    checks = []

    def exact(name, lhs, rhs=0):
        residual = s.simplify(s.expand(lhs-rhs))
        checks.append(dict(name=name, passed=residual == 0, residual=str(residual)))

    def gate(name, condition):
        checks.append(dict(name=name, passed=bool(condition)))

    # Verify the existing code before importing it, without running profiles.
    gate("unchanged_W76_source", digest(W76) == W76_HASH)
    if not checks[-1]["passed"]:
        return dict(passed=False, checks=checks, failure="W76 source changed")
    spec = importlib.util.spec_from_file_location("existing_w76_clock_audit", W76)
    w76 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(w76)
    for path, expected in w76.PINS.items():
        gate("W76_pin:" + path.name, w76.digest(path) == expected)
    inherited = w76.symbolic_gate()
    for name, ok in inherited["checks"].items():
        gate("W76:" + name, ok)
    for name, row in inherited["negative_controls"].items():
        gate("W76_negative:" + name, row["detected"])
    for name, ok in inherited["nonlinear_bound_checks"].items():
        gate("W76_bound:" + name, ok)

    p, D, omega = s.symbols("p D omega", positive=True)
    a, b, at, bt, ax, bx, ay, by, az, bz, V = s.symbols(
        "a b at bt ax bx ay by az bz V", real=True)
    U, Ut, Ux = a+s.I*b, at+s.I*bt, ax+s.I*bx
    norm2 = lambda z: s.expand(s.conjugate(z)*z)
    metric = s.diag(-p**2, p**-2, p**-2, p**-2)
    rootg = s.sqrt(-metric.det())
    local_grad2 = ax**2+bx**2+ay**2+by**2+az**2+bz**2
    coord_Ut, coord_Ux = p*Ut, Ux/p
    coord_grad2 = local_grad2/p**2
    local_L = norm2(Ut)/2-local_grad2/2-V
    coordinate_L = norm2(coord_Ut)/(2*p**2)-p**2*coord_grad2/2-V
    local_energy = norm2(Ut)/2+local_grad2/2+V
    coord_energy_density = rootg*(
        norm2(coord_Ut)/(2*p**2)+p**2*coord_grad2/2+V)
    exact("metric_volume_element", rootg, p**-2)
    exact("same_local_scalar_lagrangian", coordinate_L, local_L)
    exact("action_measure_per_reference_time", rootg*p**3, p)
    exact("integrated_reference_energy", coord_energy_density*p**3, p*local_energy)

    local_density = s.im(s.conjugate(U)*Ut)
    local_current = -s.im(s.conjugate(U)*Ux)
    jt = s.im(s.conjugate(U)*coord_Ut)/p**2
    jx = -p**2*s.im(s.conjugate(U)*coord_Ux)
    local_power_density = -s.re(s.conjugate(Ut)*Ux)
    power_current = -p**2*s.re(s.conjugate(coord_Ut)*coord_Ux)
    exact("charge_density_component", jt, local_density/p)
    exact("integrated_charge_invariant", rootg*jt*p**3, local_density)
    exact("charge_current_component", jx, p*local_current)
    exact("charge_surface_flux", rootg*jx*p**2, p*local_current)
    exact("energy_current_component", power_current, p**2*local_power_density)
    exact("energy_surface_flux", rootg*power_current*p**2, p**2*local_power_density)
    exact("charge_flux_clock_conversion", rootg*jx*p**2/p, local_current)
    exact("energy_flux_local_reconstruction", rootg*power_current*p**2/p**2,
          local_power_density)

    # Independent W76 integrated-kernel route; same local geometry.
    f = s.Function("f")
    K = s.pi*D*f(D/2)**2
    Dx = p*D
    Kx = s.pi*Dx*f(Dx/(2*p))**2
    exact("profile_kernel_clock_scaling", Kx, p*K)
    Delta = s.symbols("Delta", real=True)
    I = K*s.sin(Delta)
    Iext, Oext = p*I, p*omega
    Pext, Plocal = Oext*Iext, omega*I
    exact("pair_energy_power_two_factors", Pext, p**2*Plocal)
    exact("instantaneous_transfer_per_tick", Pext/(Oext/(2*s.pi)),
          p*Plocal/(omega/(2*s.pi)))
    exact("phase_cadence", Oext/p, omega)
    exact("zero_phase_transfer", I.subs(Delta, 0))
    exact("left_right_energy_balance", Pext+(-Oext*Iext))
    exact("isolated_harmonic_flux",
          -s.re(s.conjugate(s.I*omega*s.symbols("f0", real=True))
                *s.symbols("fp0", real=True)))

    # Use the same nonzero flux witness to reject missing/extra p factors.
    expected = p**2*Plocal
    witness = {p:s.Rational(1, 2), D:2, omega:s.Rational(4, 5),
               Delta:s.pi/2}
    for name, candidate in (
        ("missing_clock_factor", p*Plocal),
        ("extra_size_factor", p**3*Plocal),
        ("unchanged_external_power", Plocal),
    ):
        residual = s.simplify(
            (candidate-expected).subs(f(D/2), 1).subs(witness))
        gate("reject_" + name, residual.is_zero is False)

    # Only an identity for a time-dependent readout, not its dynamics.
    t = s.symbols("t", real=True)
    scale, tau = s.Function("p")(t), s.Function("tau")(t)
    energy = s.Function("E")(tau)
    exact("changing_reference_energy_chain_rule",
          s.diff(scale*energy, t).subs(s.diff(tau, t), scale),
          s.diff(scale, t)*energy+scale**2*s.diff(energy, tau))

    # Existing W75 local additive action: no invented exchange term.
    n, qc, qo, chi, chid = s.symbols("n qc qo chi chid", real=True)
    rho = s.Function("rho")(n)
    potential = s.Function("V")(chi)
    Ladd = n*qc-rho+chid**2/2+chi**2*qo**2/2-potential
    exact("W75_direct_density_amplitude_mixed_derivative", s.diff(Ladd, n, chi))
    exact("W75_direct_density_phase_rate_mixed_derivative", s.diff(Ladd, n, qo))

    # W47's extra-p control follows the unchanged volume dictionary.
    H = s.symbols("H", positive=True)
    eta_rate = -s.Rational(6, 5)*H*p**2
    gate("reject_extra_clock_in_W47_dictionary",
         s.simplify((p*eta_rate-eta_rate).subs({p:s.Rational(1, 2), H:1})) != 0)
    gate("W76_source_still_unchanged", digest(W76) == W76_HASH)

    passed = all(row["passed"] for row in checks)
    examples = [dict(p=str(value), length_ratio=str(value),
                     cadence_ratio=str(value), power_ratio=str(value**2))
                for value in (s.S.One, s.Rational(1, 10), s.Rational(1, 50))]
    return dict(
        decision="EXISTING_EXCHANGE_HAS_TWO_REFERENCE_FACTORS" if passed else "AUDIT_FAILED",
        passed=passed, check_count=len(checks),
        failed=[row for row in checks if not row["passed"]],
        scope="Same local W76 initial state in a prescribed constant uniform common-p patch.",
        result=dict(charge_rate_ratio="p", energy_rate_ratio="p^2", examples=examples),
        closure=dict(flux_readout_verified=passed,
                     independent_local_size_damping_derived=False,
                     collective_pressure_transfer_derived=False,
                     pressure_zero_inaccessibility_derived=False,
                     strong_field_calculation_performed=False),
        provenance=dict(self_sha256=digest(Path(__file__)),
                        note_sha256=digest(HERE/"oscillon_clock_transfer_audit.md"),
                        W76_sha256=digest(W76), python=sys.version.split()[0],
                        sympy=s.__version__),
        checks=checks, writes_files=False)


if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, indent=2, allow_nan=False))
    raise SystemExit(0 if report["passed"] else 1)
