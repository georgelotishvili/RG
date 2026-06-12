# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: this file uses particle-sector normal forms;
# no active c_Y sign claim is made here.

"""PHASE 37d (p11c): population mutual-lock ledger.

Revised stability postulate (replaces the substrate-frequency lock).
The old tail condition required the oscillon to match the substrate
frequency nu0 or its harmonics; that version failed on its own numbers
(nu0/nu_C ~ 1e10, and the oscillon is a SUB-harmonic of the substrate,
not an overtone).  The revised condition splits into two filters:

  (F1) KINEMATIC: the tail must propagate in the substrate (dispersion
       admits the external trace).  The substrate is the coupling
       channel, not the metronome.
  (F2) DYNAMIC (population): the form must co-exist with the frequency
       set of the ALREADY EXISTING particles.  Whatever has a decay
       channel into the existing set decays into it; whatever has none
       stays.  Stability is a property of the spectrum, not of a
       particle in isolation.

This gate verifies the three pillars the revised postulate stands on:

  T1 (symbolic). TRANSPOSITION INVARIANCE: the C3 chord observables
      (Q, A, theta) are invariant under a common rescaling of all
      frequencies nu_k -> s*nu_k.  The lepton chord is therefore a
      MUTUAL relation that needs no external frequency standard, and a
      change of the substrate energy status (gravity) transposes the
      whole population without breaking any lock.

  T2 (numeric toy). MUTUAL SYNC WITHOUT A MASTER CLOCK: three coupled
      phase oscillators (Kuramoto) with distinct natural frequencies
      entrain to a common frequency set by the population itself (the
      mean), with no external reference; below critical coupling they
      do not lock.  Demonstrates that a population can be its own
      standard (Huygens / laser mode-locking / Kuramoto class).

  T3 (numeric toy). INTEGER-RATIO LOCK PLATEAU (Arnold tongue): the
      phase difference psi = theta_1 - 2*theta_2 of a 2:1 pair obeys an
      Adler equation dpsi/dt = Delta - K*sin(psi); for |Delta| < K the
      ratio locks exactly (psi -> const), outside it drifts.
      Demonstrates that integer/rational mutual locks are generic
      attractors with finite robustness windows.

  D1 (data anchors). SPECTRUM-RELATIVE STABILITY: PDG mass ordering
      realizes filter F2 in nature -- the electron is the lightest
      charged particle (no decay channel: stable), the proton is the
      lightest baryon, while mu/tau decay INTO the existing lighter
      set.  Recorded as machine-checked ordering statements, not as
      derivations.

Open (the real prize of the population fixed-point programme): compute the
mutually compatible attractor SETS of the F_min nonlinearity inside the
p01 stability window -- the "first set" problem.  This gate does not
attempt it.

Run:  python p11c_population_lock_ledger.py all
"""

import math
import sys

import sympy as sp


# --- T1: transposition invariance (symbolic) --------------------------------

def sym_transposition_invariance():
    """Q, A, theta of the C3 chord are invariant under nu_k -> s*nu_k.

    Returns dict of residuals; the theorem holds iff all are 0.
    """
    mu, A, th, s = sp.symbols("mu A theta s", positive=True)
    nu = [mu * (1 + A * sp.cos(th + 2 * sp.pi * k / 3)) for k in range(3)]
    nu_scaled = [s * x for x in nu]

    def Q_of(vals):
        return sum(v**2 for v in vals) / (sum(vals)) ** 2

    # Koide ratio: homogeneous of degree zero
    rQ = sp.simplify(Q_of(nu_scaled) - Q_of(nu))

    # DFT-extracted amplitude and phase: c1 = (1/3) sum nu_k w^k
    w = sp.exp(-2 * sp.pi * sp.I * sp.Rational(1, 3))
    c1 = sp.Rational(1, 3) * sum(nu[k] * w**k for k in range(3))
    c1_s = sp.Rational(1, 3) * sum(nu_scaled[k] * w**k for k in range(3))
    mean = sum(nu) / 3
    mean_s = sum(nu_scaled) / 3
    # A = 2|c1|/mean is degree-zero; theta = arg(c1) unchanged by s>0
    rA = sp.simplify(2 * sp.Abs(c1_s) / mean_s - 2 * sp.Abs(c1) / mean)
    rTheta = sp.simplify(sp.arg(c1_s) - sp.arg(c1))

    return {"Q_residual": rQ, "A_residual": rA, "theta_residual": rTheta}


# --- T2: mutual sync without a master clock (Kuramoto N=3) -------------------

def kuramoto_run(omegas, K, t_end=400.0, dt=0.01, window=100.0):
    """Integrate dtheta_i/dt = omega_i + (K/N) sum_j sin(theta_j - theta_i).

    Returns effective frequencies measured over the final window.
    """
    n = len(omegas)
    theta = [0.0, 2.0, 4.0][:n]
    steps = int(t_end / dt)
    win_steps = int(window / dt)
    mark = None
    for step in range(steps):
        dth = []
        for i in range(n):
            coupling = sum(math.sin(theta[j] - theta[i]) for j in range(n))
            dth.append(omegas[i] + (K / n) * coupling)
        theta = [theta[i] + dt * dth[i] for i in range(n)]
        if step == steps - win_steps - 1:
            mark = list(theta)
    eff = [(theta[i] - mark[i]) / window for i in range(n)]
    return eff


def mutual_sync_gate():
    omegas = [1.00, 1.20, 1.35]
    mean = sum(omegas) / len(omegas)

    eff_locked = kuramoto_run(omegas, K=1.0)
    spread_locked = max(eff_locked) - min(eff_locked)
    locked = spread_locked < 1e-6
    common_eq_mean = abs(sum(eff_locked) / 3 - mean) < 1e-6

    eff_free = kuramoto_run(omegas, K=0.05)
    spread_free = max(eff_free) - min(eff_free)
    unlocked = spread_free > 0.1

    return {
        "natural": omegas,
        "eff_locked": eff_locked,
        "spread_locked": spread_locked,
        "population_frequency_equals_mean": common_eq_mean,
        "eff_free": eff_free,
        "spread_free": spread_free,
        "verdict_locked": locked,
        "verdict_unlocked_below_critical": unlocked,
    }


# --- T3: integer-ratio lock plateau (Adler equation) -------------------------

def adler_run(delta, K=0.5, t_end=400.0, dt=0.01, window=100.0):
    """Integrate dpsi/dt = delta - K*sin(psi) for psi = theta_1 - 2*theta_2.

    Returns the mean drift rate of psi over the final window
    (0 -> 2:1 lock; nonzero -> drift).
    """
    psi = 0.0
    steps = int(t_end / dt)
    win_steps = int(window / dt)
    mark = None
    for step in range(steps):
        psi += dt * (delta - K * math.sin(psi))
        if step == steps - win_steps - 1:
            mark = psi
    return (psi - mark) / window


def integer_lock_gate():
    K = 0.5
    inside = adler_run(delta=0.3, K=K)    # |Delta| < K: must lock
    outside = adler_run(delta=0.8, K=K)   # |Delta| > K: must drift
    # analytic drift rate outside the tongue: sqrt(Delta^2 - K^2)
    analytic = math.sqrt(0.8**2 - K**2)
    return {
        "K": K,
        "drift_inside_tongue": inside,
        "drift_outside_tongue": outside,
        "analytic_outside": analytic,
        "verdict_lock_inside": abs(inside) < 1e-8,
        "verdict_drift_outside": abs(outside - analytic) / analytic < 0.05,
        "tongue_width": "lock iff |Delta| <= K (finite robustness window)",
    }


# --- D1: spectrum-relative stability anchors (PDG data statements) -----------

PDG_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
    "proton": 938.27208943,
    "neutron": 939.56542052,
    "pion_pm": 139.57039,
    "kaon_pm": 493.677,
}


def spectrum_stability_anchors():
    m = PDG_MEV
    anchors = {
        "electron_lightest_charged": m["electron"] < min(
            m["muon"], m["tau"], m["proton"], m["pion_pm"], m["kaon_pm"]
        ),
        "proton_lightest_baryon_listed": m["proton"] < m["neutron"],
        "muon_decays_into_lighter_set": m["muon"] > m["electron"],
        "tau_decays_into_lighter_set": m["tau"] > m["muon"] > m["electron"],
    }
    return {
        "anchors": anchors,
        "all_hold": all(anchors.values()),
        "meaning": (
            "Stability in nature is defined RELATIVE to the spectrum: the "
            "electron is stable because no lighter charged state exists, "
            "not because it matches any substrate frequency. Filter F2 of "
            "the revised condition is the intuitive face of this fact."
        ),
    }


# --- ledger -------------------------------------------------------------------

def status_assessment(t1, t2, t3, d1):
    sym_ok = all(v == 0 for v in t1.values())
    return {
        "T1": "PASS_SYMBOLIC_TRANSPOSITION_INVARIANCE" if sym_ok
              else "T1_DID_NOT_VERIFY",
        "T2": "PASS_TOY_MUTUAL_SYNC_NO_MASTER_CLOCK"
              if (t2["verdict_locked"]
                  and t2["population_frequency_equals_mean"]
                  and t2["verdict_unlocked_below_critical"])
              else "T2_DID_NOT_VERIFY",
        "T3": "PASS_TOY_INTEGER_RATIO_LOCK_PLATEAU"
              if (t3["verdict_lock_inside"] and t3["verdict_drift_outside"])
              else "T3_DID_NOT_VERIFY",
        "D1": "PASS_SPECTRUM_RELATIVE_STABILITY_DATA_ANCHORS"
              if d1["all_hold"] else "D1_DID_NOT_VERIFY",
        "open": "OPEN_FMIN_POPULATION_ATTRACTOR_SETS -- compute the mutually "
                "compatible oscillon sets admitted by the F_min nonlinearity "
                "inside the p01 window (the 'first set' problem of the "
                "population fixed-point programme).",
    }


def do_not_claim():
    return [
        "Do not claim the toy models (Kuramoto, Adler) derive the SM "
        "spectrum; they demonstrate that the locking MECHANISM class exists "
        "and needs no master clock.",
        "Do not claim the C3 lepton chord is derived from mutual-lock "
        "dynamics; its action-level origin remains open (p11 phase38).",
        "Do not claim which lock set the medium selects; the F_min "
        "attractor-set computation is open (task 16).",
        "Do not claim the kinematic filter F1 is computed here; tail "
        "propagation lives in the p05/p13 weak-field chain.",
        "Do not read the PDG anchors as derivations; they are data "
        "statements that the dynamic filter F2 matches how stability "
        "actually works.",
    ]


# --- main ----------------------------------------------------------------------

def main():
    print("=" * 72)
    print("PHASE 37d (p11c): population mutual-lock ledger")
    print("=" * 72)

    print("\n1. T1 symbolic: transposition invariance of the C3 chord")
    t1 = sym_transposition_invariance()
    for key, val in t1.items():
        print(f"  {key} = {val}")

    print("\n2. T2 toy: mutual sync without a master clock (Kuramoto N=3)")
    t2 = mutual_sync_gate()
    print(f"  natural frequencies : {t2['natural']}")
    print(f"  locked   (K=1.00)   : eff = {['%.6f' % x for x in t2['eff_locked']]}"
          f"  spread = {t2['spread_locked']:.2e}")
    print(f"  population frequency = mean(omega): {t2['population_frequency_equals_mean']}")
    print(f"  unlocked (K=0.05)   : eff = {['%.6f' % x for x in t2['eff_free']]}"
          f"  spread = {t2['spread_free']:.3f}")

    print("\n3. T3 toy: 2:1 integer lock plateau (Adler)")
    t3 = integer_lock_gate()
    print(f"  K = {t3['K']}; drift inside tongue (Delta=0.3): {t3['drift_inside_tongue']:.2e}")
    print(f"  drift outside tongue (Delta=0.8): {t3['drift_outside_tongue']:.6f}"
          f"  (analytic sqrt(D^2-K^2) = {t3['analytic_outside']:.6f})")
    print(f"  {t3['tongue_width']}")

    print("\n4. D1: spectrum-relative stability anchors (PDG)")
    d1 = spectrum_stability_anchors()
    for name, ok in d1["anchors"].items():
        print(f"  {name}: {ok}")

    print("\n5. STATUS")
    for key, val in status_assessment(t1, t2, t3, d1).items():
        print(f"  {key}: {val}")

    print("\n6. do_not_claim")
    for item in do_not_claim():
        print(f"  - {item}")


if __name__ == "__main__":
    _ = sys.argv[1:]
    main()
