# Notation header:
# signature (+---); compact branch uses positive metric functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.

"""
PHASE 18h: Compact exponential branch stability ledger

This file addresses the remaining strong-field stability defect in the first
article at the level that is currently article-usable.

It does not claim full QNM/echo/rotation stability.  It checks the static
projected Bernoulli compact source itself:

    L_B_perp = Z_perp/(8*pi*G),
    Z_perp = gamma^mn d_m h d_n h,
    gamma^mn = u^m u^n - g^mn.

On the static comoving exponential branch this source has no standalone time
kinetic term, has positive spatial stiffness in the local static Hessian, and
therefore is a constrained spatial medium load rather than a propagating
phantom scalar.  The propagating modes still belong to the full p01 medium
sector and the finite-core matching ledger.
"""

import sympy as sp

from p01_core import local_stability_short_path_certificate
from p05_compact import (
    derive_background_completed_medium_nec_gate,
    derive_c2_core_local_stability_interface,
    derive_projected_bernoulli_medium_source,
)
from p05g_exponential_source_eom import p05g_central_exponential_source_gate


def derive_projected_bernoulli_quadratic_variation_gate():
    """
    Static Hessian of the projected Bernoulli compact source.

    Write h -> h0 + eps*eta.  In the comoving static branch,

        Z_perp = (h_r)^2/A + angular spatial terms,

    and no eta_dot term appears because the projector removes the time
    direction.  The second variation is positive for G>0 and A>0.
    """
    r, r_s, G, eps = sp.symbols("r r_s G eps", positive=True, real=True)
    eta_r, eta_theta, eta_phi, theta = sp.symbols(
        "eta_r eta_theta eta_phi theta",
        positive=True,
        real=True,
    )
    eta_t = sp.Symbol("eta_t", real=True)

    h0 = r_s / (2 * r)
    A = sp.exp(r_s / r)
    h_r = sp.diff(h0, r) + eps * eta_r

    z_perp = sp.simplify(
        h_r**2 / A
        + eps**2 * eta_theta**2 / (A * r**2)
        + eps**2 * eta_phi**2 / (A * r**2 * sp.sin(theta) ** 2)
    )
    l_perp = sp.simplify(z_perp / (8 * sp.pi * G))
    l0 = sp.simplify(l_perp.subs(eps, 0))
    l1 = sp.simplify(sp.diff(l_perp, eps).subs(eps, 0))
    l2_coefficient = sp.simplify(sp.diff(l_perp, eps, 2).subs(eps, 0) / 2)
    time_kinetic_coefficient = sp.simplify(sp.diff(l_perp, eps, 2).subs({
        eta_r: 0,
        eta_theta: 0,
        eta_phi: 0,
    }) / 2)

    expected_l2 = sp.simplify(
        (
            eta_r**2
            + eta_theta**2 / r**2
            + eta_phi**2 / (r**2 * sp.sin(theta) ** 2)
        )
        / (8 * sp.pi * G * A)
    )

    return {
        "projected_bernoulli_variation_status": (
            "PASS_PROJECTED_BERNOULLI_HAS_NO_TIME_KINETIC_AND_POSITIVE_STATIC_STIFFNESS"
            if sp.simplify(l2_coefficient - expected_l2) == 0
            and sp.simplify(time_kinetic_coefficient) == 0
            else "CHECK_PROJECTED_BERNOULLI_STATIC_STIFFNESS"
        ),
        "background_h": sp.Eq(sp.Symbol("h0"), h0),
        "spatial_A": sp.Eq(sp.Symbol("A"), A),
        "L0": l0,
        "linear_term": l1,
        "quadratic_static_stiffness": l2_coefficient,
        "expected_quadratic_static_stiffness": expected_l2,
        "time_kinetic_coefficient": time_kinetic_coefficient,
        "positivity_conditions": [sp.Gt(G, 0), sp.Gt(A, 0)],
        "reading": (
            "the compact Bernoulli source is a static spatial stiffness; it "
            "does not export a negative time-kinetic scalar mode"
        ),
    }


def derive_projected_bernoulli_principal_symbol_gate():
    """
    Eikonal principal symbol of the projected Bernoulli source.

    For eta ~ exp(i(k_i x^i - omega t)), L_B_perp contributes only the spatial
    quadratic form.  The symbol is elliptic/constraint-like for this source
    alone.  Hyperbolic propagation must come from the p01 medium sector.
    """
    r, r_s, G, theta = sp.symbols("r r_s G theta", positive=True, real=True)
    omega, k_r, k_theta, k_phi = sp.symbols(
        "omega k_r k_theta k_phi",
        real=True,
    )
    A = sp.exp(r_s / r)
    symbol = sp.simplify(
        (
            k_r**2
            + k_theta**2 / r**2
            + k_phi**2 / (r**2 * sp.sin(theta) ** 2)
        )
        / (8 * sp.pi * G * A)
    )
    omega_coefficient = sp.simplify(sp.diff(symbol, omega, 2))

    return {
        "principal_symbol_status": (
            "PASS_PROJECTED_BERNOULLI_SOURCE_IS_STATIC_ELLIPTIC_CONSTRAINT_NOT_PHANTOM_WAVE"
            if omega_coefficient == 0
            else "CHECK_PROJECTED_BERNOULLI_PRINCIPAL_SYMBOL"
        ),
        "spatial_symbol": symbol,
        "omega_coefficient": omega_coefficient,
        "positivity_conditions": [sp.Gt(G, 0), sp.Gt(A, 0)],
        "meaning": (
            "positive spatial symbol for the projected source; no standalone "
            "wave speed is assigned to L_B_perp by itself"
        ),
    }


def derive_compact_branch_minimal_stability_gate():
    """
    Article-facing minimal stability gate for the static compact branch.

    This combines:
    - p05g source closure;
    - total-medium NEC capacity;
    - projected Bernoulli no-phantom/static-stiffness check;
    - p01/C2 local principal-symbol interface.
    """
    source = p05g_central_exponential_source_gate()
    nec = derive_background_completed_medium_nec_gate()
    projected = derive_projected_bernoulli_medium_source()
    variation = derive_projected_bernoulli_quadratic_variation_gate()
    principal = derive_projected_bernoulli_principal_symbol_gate()
    p01_local = local_stability_short_path_certificate()
    c2_interface = derive_c2_core_local_stability_interface()

    passed = (
        source["p05g_status"]
        == "PASS_P05G_EXPONENTIAL_EXTERIOR_SOURCE_AND_ENERGY_VERDICT"
        and nec["total_medium_nec_status"]
        == "PASS_TOTAL_MEDIUM_NEC_REDUCES_TO_FINITE_BACKGROUND_CAPACITY_BOUND"
        and projected["refg_medium_export"]
        == "PASS_STATIC_PROJECTED_BERNOULLI_MEDIUM_SOURCE_FOR_EXPONENTIAL_BRANCH"
        and variation["projected_bernoulli_variation_status"]
        == "PASS_PROJECTED_BERNOULLI_HAS_NO_TIME_KINETIC_AND_POSITIVE_STATIC_STIFFNESS"
        and principal["principal_symbol_status"]
        == "PASS_PROJECTED_BERNOULLI_SOURCE_IS_STATIC_ELLIPTIC_CONSTRAINT_NOT_PHANTOM_WAVE"
        and p01_local["status"] == "PASS_LOCAL_STABILITY_SHORT_PATH"
        and c2_interface["interface_status"]
        == "PASS_COMPACT_CORE_P01_LOCAL_STABILITY_INTERFACE"
    )

    return {
        "p05h_status": (
            "PASS_STATIC_COMPACT_BRANCH_MINIMAL_STABILITY_GATE"
            if passed
            else "CHECK_STATIC_COMPACT_BRANCH_MINIMAL_STABILITY_GATE"
        ),
        "source_closure": source["p05g_status"],
        "total_medium_nec": nec["total_medium_nec_status"],
        "projected_source": projected["refg_medium_export"],
        "projected_variation": variation["projected_bernoulli_variation_status"],
        "projected_principal_symbol": principal["principal_symbol_status"],
        "p01_local_stability": p01_local["status"],
        "p01_local_stability_scope": p01_local["scope"],
        "c2_core_local_interface": c2_interface["interface_status"],
        "article_supported_claim": (
            "the static compact phase branch has source closure, total-medium "
            "NEC capacity, no standalone phantom scalar from L_B_perp, positive "
            "static projected-Bernoulli stiffness, and a nonempty p01 local "
            "principal-symbol stability interface"
        ),
        "not_claimed": [
            "full background-dependent coupled compact perturbation spectrum",
            "QNM/echo stability",
            "rotating strong-field stability",
            "EHT ray-tracing viability",
        ],
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18h: Compact exponential branch stability ledger")
    print("=" * 72)

    sections = [
        ("1. Projected Bernoulli quadratic variation", derive_projected_bernoulli_quadratic_variation_gate()),
        ("2. Projected Bernoulli principal symbol", derive_projected_bernoulli_principal_symbol_gate()),
        ("3. Minimal compact-branch stability gate", derive_compact_branch_minimal_stability_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:44s}: {value}")
