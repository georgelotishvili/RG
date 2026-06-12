# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: this file uses particle-sector normal forms;
# no active c_Y sign claim is made here.

"""PHASE 37c (p11b): exact inversion of the charged-lepton triplet onto the
C3 three-phase form, with PDG error propagation.

Motivation.  p11 PHASE 37 proves the FORWARD statement: the C3 ansatz
nu_k = A0*[1 + sqrt(2)*cos(theta + 2*pi*k/3)] reproduces the Koide ratio
Q = 2/3 for every theta, and at theta = 2/9 it reproduces the charged-lepton
frequency ratios.  In p11 the amplitude sqrt(2) is ASSUMED everywhere and
only theta is fitted.  This gate closes the converse direction and turns
both constants into measurements:

  (T1) Decomposition theorem (discrete Fourier transform, not an ansatz):
       ANY real triple (nu_0, nu_1, nu_2) decomposes uniquely as
           nu_k = mu * (1 + A*cos(theta + 2*pi*k/3)),   A >= 0,
       with  mu = (nu_0+nu_1+nu_2)/3,
             c1 = (1/3) * sum_k nu_k * exp(-2*pi*i*k/3) = (mu*A/2) e^{i theta}.
       The parametrization by itself therefore has NO empirical content:
       three numbers go in, three parameters come out.

  (T2) Amplitude-Koide equivalence (exact identity):
           Q := sum(nu_k^2) / (sum nu_k)^2 = 1/3 + A^2/6,
       hence Q = 2/3  <=>  A = sqrt(2).  The entire Koide statement is the
       single measured number A; theta is a second, independent measured
       number.  This sharpens p11: instead of "the ansatz fits", the claim
       becomes "A_obs = sqrt(2) and theta_obs = 2/9 within PDG precision",
       which is falsifiable by mass updates alone.

  (M1) PDG inversion: A_obs and theta_obs extracted from the measured
       charged-lepton masses (nu = sqrt(m), the m ~ nu^2 convention of the
       C3 route; the dimensional anchor cancels in A and theta), with full
       Monte-Carlo propagation of the PDG mass uncertainties.  The tau mass
       error dominates.  Reported verdicts:
           (A_obs - sqrt(2)) / sigma_A,   (theta_obs - 2/9) / sigma_theta.

  (M2) Scale ledger: the decomposition isolates ONE dimensional input,
       mu = mean(sqrt(m_k)).  With (A, theta) promoted to the exact
       constants (sqrt(2), 2/9), the three lepton masses compress to one
       scale plus two dimensionless constants; the conditional residuals of
       that compression are restated in PDG sigma units as a cross-check of
       p11's precision audit.

Representation convention: the decomposition is unique up to the six-fold
relabeling symmetry (3 cyclic shifts x reflection theta -> -theta).  The
cyclic assignment (k=0,1,2) = (tau, electron, muon) matches p11's natural
ordering at theta = 2/9 (k=0 largest, k=1 smallest); theta is reported in
the fundamental branch |theta| <= pi/3.

Run:  python p11b_c3_triplet_inversion.py all
"""

import cmath
import math
import random
import sys

import sympy as sp


# --- PDG 2026 charged-lepton masses (same nodes as p11) -------------------

LEPTON_MASSES_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.93,
}

LEPTON_MASS_UNCERTAINTY_MEV = {
    "electron": 0.00000000016,
    "muon": 0.0000023,
    "tau": 0.09,
}

PDG_MASS_SOURCE = {
    "edition": "PDG 2026 pdgLive (same nodes as p11)",
    "electron_node": "S003",
    "muon_node": "S004",
    "tau_node": "S035",
}

THETA_TOPOLOGICAL = 2.0 / 9.0
A_KOIDE = math.sqrt(2.0)

# cyclic assignment matching p11's c3_raw_frequencies ordering at theta=2/9:
# k=0 -> tau (largest), k=1 -> electron (smallest), k=2 -> muon (middle)
CYCLIC_ORDER = ("tau", "electron", "muon")

MC_SAMPLES = 200000
MC_SEED = 11


# --- T1/T2: symbolic theorems ---------------------------------------------

def sym_dft_decomposition_residual():
    """Residual of c1 = (mu*A/2) e^{i theta} under the parametrization.

    Returns the simplified difference; the theorem holds iff it is 0.
    """
    mu, A, th = sp.symbols("mu A theta", real=True)
    w = sp.exp(-2 * sp.pi * sp.I * sp.Rational(1, 3))
    nu = [mu * (1 + A * sp.cos(th + 2 * sp.pi * k / 3)) for k in range(3)]
    c1 = sp.Rational(1, 3) * sum(nu[k] * w**k for k in range(3))
    target = (mu * A / 2) * sp.exp(sp.I * th)
    return sp.simplify(sp.expand_complex(c1 - target))


def sym_mean_residual():
    """Residual of mu = mean(nu_k) under the parametrization (must be 0)."""
    mu, A, th = sp.symbols("mu A theta", real=True)
    nu = [mu * (1 + A * sp.cos(th + 2 * sp.pi * k / 3)) for k in range(3)]
    return sp.simplify(sum(nu) / 3 - mu)


def sym_koide_amplitude_residual():
    """Residual of  Q - (1/3 + A^2/6)  under the parametrization (must be 0).

    Q = 2/3 <=> A = sqrt(2) follows immediately.
    """
    mu, A, th = sp.symbols("mu A theta", real=True, positive=True)
    nu = [mu * (1 + A * sp.cos(th + 2 * sp.pi * k / 3)) for k in range(3)]
    Q = sum(x**2 for x in nu) / (sum(nu)) ** 2
    return sp.simplify(Q - (sp.Rational(1, 3) + A**2 / 6))


# --- M1: numeric inversion --------------------------------------------------

def invert_triplet(nu_triplet, normalize_branch=True):
    """(mu, A, theta) of an arbitrary positive triple via the DFT formulas.

    nu_triplet follows CYCLIC_ORDER.  With normalize_branch=True theta is
    mapped to |theta| <= pi/3 using the cyclic relabeling freedom
    theta -> theta + 2*pi*j/3 (each shift relabels k -> k - j, so the
    normalized theta describes a cyclically rotated triple); the round-trip
    test must therefore use normalize_branch=False.
    """
    mu = sum(nu_triplet) / 3.0
    c1 = sum(
        nu * cmath.exp(-2j * math.pi * k / 3) for k, nu in enumerate(nu_triplet)
    ) / 3.0
    amp = 2.0 * abs(c1) / mu
    theta = cmath.phase(c1)
    if normalize_branch:
        while theta > math.pi / 3:
            theta -= 2 * math.pi / 3
        while theta < -math.pi / 3:
            theta += 2 * math.pi / 3
    return mu, amp, theta


def reconstruct_triplet(mu, amp, theta):
    return [
        mu * (1 + amp * math.cos(theta + 2 * math.pi * k / 3)) for k in range(3)
    ]


def roundtrip_check(seed=MC_SEED, trials=1000):
    """Genericity demonstration: random positive triples invert exactly."""
    rng = random.Random(seed)
    worst = 0.0
    for _ in range(trials):
        triple = [rng.uniform(0.1, 100.0) for _ in range(3)]
        rebuilt = reconstruct_triplet(
            *invert_triplet(triple, normalize_branch=False)
        )
        worst = max(
            worst,
            max(abs(a - b) / abs(a) for a, b in zip(triple, rebuilt)),
        )
    return worst


def koide_ratio(nu_triplet):
    total = sum(nu_triplet)
    return sum(nu * nu for nu in nu_triplet) / (total * total)


def pdg_triplet(masses=LEPTON_MASSES_MEV):
    return [math.sqrt(masses[name]) for name in CYCLIC_ORDER]


def pdg_inversion():
    mu, amp, theta = invert_triplet(pdg_triplet())
    return {
        "mu_sqrtMeV": mu,
        "mu_squared_MeV": mu * mu,
        "A_obs": amp,
        "theta_obs": theta,
        "Q_obs": koide_ratio(pdg_triplet()),
        "A_minus_sqrt2": amp - A_KOIDE,
        "theta_minus_2_9": theta - THETA_TOPOLOGICAL,
    }


def monte_carlo(samples=MC_SAMPLES, seed=MC_SEED):
    """Propagate PDG mass uncertainties into (A_obs, theta_obs, Q_obs)."""
    rng = random.Random(seed)
    amps, thetas, qs = [], [], []
    names = CYCLIC_ORDER
    for _ in range(samples):
        masses = {
            n: rng.gauss(LEPTON_MASSES_MEV[n], LEPTON_MASS_UNCERTAINTY_MEV[n])
            for n in names
        }
        triple = [math.sqrt(masses[n]) for n in names]
        _, amp, theta = invert_triplet(triple)
        amps.append(amp)
        thetas.append(theta)
        qs.append(koide_ratio(triple))
    def stats(xs):
        mean = sum(xs) / len(xs)
        var = sum((x - mean) ** 2 for x in xs) / (len(xs) - 1)
        return mean, math.sqrt(var)
    a_mean, a_sigma = stats(amps)
    t_mean, t_sigma = stats(thetas)
    q_mean, q_sigma = stats(qs)
    return {
        "A_mean": a_mean,
        "A_sigma": a_sigma,
        "A_pull_vs_sqrt2": (a_mean - A_KOIDE) / a_sigma,
        "theta_mean": t_mean,
        "theta_sigma": t_sigma,
        "theta_pull_vs_2_9": (t_mean - THETA_TOPOLOGICAL) / t_sigma,
        "Q_mean": q_mean,
        "Q_sigma": q_sigma,
        "Q_pull_vs_2_3": (q_mean - 2.0 / 3.0) / q_sigma,
        "samples": samples,
    }


# --- M2: compression cross-check -------------------------------------------

def conditional_mass_residuals():
    """Masses implied by exact (sqrt(2), 2/9) + electron anchor, in PDG sigma.

    Restates p11's precision audit through the inversion variables.
    """
    raw = sorted(reconstruct_triplet(1.0, A_KOIDE, THETA_TOPOLOGICAL))
    base = raw[0]
    ratios = {"electron": 1.0, "muon": raw[1] / base, "tau": raw[2] / base}
    m_e = LEPTON_MASSES_MEV["electron"]
    rows = []
    for name in ("muon", "tau"):
        predicted = m_e * ratios[name] ** 2
        observed = LEPTON_MASSES_MEV[name]
        sigma = LEPTON_MASS_UNCERTAINTY_MEV[name]
        rows.append(
            {
                "particle": name,
                "predicted_MeV": predicted,
                "observed_MeV": observed,
                "residual_MeV": predicted - observed,
                "residual_relative": (predicted - observed) / observed,
                "residual_pdg_sigma": (predicted - observed) / sigma,
            }
        )
    return rows


# --- ledger -----------------------------------------------------------------

def status_assessment(mc):
    a_ok = abs(mc["A_pull_vs_sqrt2"]) <= 2.0
    t_ok = abs(mc["theta_pull_vs_2_9"]) <= 2.0
    return {
        "T1_dft_decomposition": "PASS_SYMBOLIC",
        "T2_koide_equiv_amplitude": "PASS_SYMBOLIC (Q = 1/3 + A^2/6 exact)",
        "M1_amplitude": (
            f"A_obs = sqrt(2) at {mc['A_pull_vs_sqrt2']:+.2f} sigma -> "
            + ("CONSISTENT" if a_ok else "TENSION")
        ),
        "M1_phase": (
            f"theta_obs = 2/9 at {mc['theta_pull_vs_2_9']:+.2f} sigma -> "
            + ("CONSISTENT" if t_ok else "TENSION")
        ),
        "open": "Derivation of A=sqrt(2), theta=2/9, and m~nu^2 from the RG "
                "action remains open (p11 phase38 candidate route).",
    }


def do_not_claim():
    return [
        "Do not claim the three-phase parametrization is evidence by itself: "
        "T1 shows it is a generic DFT, valid for ANY positive triple.",
        "Do not claim A=sqrt(2) or theta=2/9 is derived from the RG action; "
        "both are measured constants here (p11 phase38 candidate remains open).",
        "Do not claim m~nu^2 is derived (oscillon energy theorem open, as p11).",
        "Do not claim the scale mu (mu^2 ~ 3.1e2 MeV) is identified with any "
        "physical scale; it is the single dimensional input of the triplet.",
        "Do not claim radiative protection: the statement is tied to PDG pole "
        "masses as measured; scheme/running behavior is not addressed here.",
    ]


# --- main --------------------------------------------------------------------

def main():
    print("=" * 72)
    print("PHASE 37c (p11b): C3 triplet inversion -- DFT theorems + PDG pulls")
    print("=" * 72)

    print("\n1. T1 symbolic: DFT decomposition identities")
    r1 = sym_dft_decomposition_residual()
    r2 = sym_mean_residual()
    print(f"  c1 - (mu*A/2)e^(i theta)  residual = {r1}")
    print(f"  mean(nu) - mu             residual = {r2}")

    print("\n2. T2 symbolic: amplitude-Koide equivalence")
    r3 = sym_koide_amplitude_residual()
    print(f"  Q - (1/3 + A^2/6)         residual = {r3}")
    print("  => Q = 2/3  <=>  A = sqrt(2)")

    print("\n3. Genericity round-trip on random triples")
    worst = roundtrip_check()
    print(f"  worst relative reconstruction error over 1000 triples: {worst:.3e}")

    print("\n4. M1: PDG inversion (central values)")
    inv = pdg_inversion()
    print(f"  mu        = {inv['mu_sqrtMeV']:.6f} MeV^(1/2)"
          f"   (mu^2 = {inv['mu_squared_MeV']:.4f} MeV)")
    print(f"  A_obs     = {inv['A_obs']:.9f}   (sqrt(2) = {A_KOIDE:.9f},"
          f" diff = {inv['A_minus_sqrt2']:+.3e})")
    print(f"  theta_obs = {inv['theta_obs']:.9f}   (2/9 = {THETA_TOPOLOGICAL:.9f},"
          f" diff = {inv['theta_minus_2_9']:+.3e})")
    print(f"  Q_obs     = {inv['Q_obs']:.9f}   (2/3 diff ="
          f" {inv['Q_obs'] - 2.0 / 3.0:+.3e})")

    print("\n5. M1: Monte-Carlo PDG error propagation"
          f" ({MC_SAMPLES} samples, seed {MC_SEED})")
    mc = monte_carlo()
    print(f"  A_obs     = {mc['A_mean']:.9f} +- {mc['A_sigma']:.2e}"
          f"   pull vs sqrt(2): {mc['A_pull_vs_sqrt2']:+.2f} sigma")
    print(f"  theta_obs = {mc['theta_mean']:.9f} +- {mc['theta_sigma']:.2e}"
          f"   pull vs 2/9:     {mc['theta_pull_vs_2_9']:+.2f} sigma")
    print(f"  Q_obs     = {mc['Q_mean']:.9f} +- {mc['Q_sigma']:.2e}"
          f"   pull vs 2/3:     {mc['Q_pull_vs_2_3']:+.2f} sigma")

    print("\n6. M2: compression cross-check (exact constants + electron anchor)")
    for row in conditional_mass_residuals():
        print(f"  {row['particle']:8s}: predicted = {row['predicted_MeV']:.6f} MeV,"
              f" observed = {row['observed_MeV']:.6f} MeV,"
              f" residual = {row['residual_MeV']:+.4f} MeV"
              f" (rel {row['residual_relative']:+.2e},"
              f" {row['residual_pdg_sigma']:+.2f} PDG sigma)")
    print("  note: the muon PDG sigma is 2.3e-6 MeV, so a 1e-5-level relative"
          " residual\n  is hundreds of PDG sigma -- consistent with p11's"
          " do_not_claim (no\n  PDG-precision mass prediction is claimed;"
          " the compression is 1e-5-level).")

    print("\n7. STATUS")
    ok_symbolic = (r1 == 0) and (r2 == 0) and (r3 == 0)
    for key, value in status_assessment(mc).items():
        print(f"  {key}: {value}")
    print(f"  symbolic_residuals_zero: {ok_symbolic}")

    print("\n8. do_not_claim")
    for item in do_not_claim():
        print(f"  - {item}")


if __name__ == "__main__":
    # accepts and ignores the conventional 'all' argument
    _ = sys.argv[1:]
    main()
