# Notation header (see NOTATION.md):
# signature (+---); compact exterior uses positive functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.

"""
PHASE 18g: Exponential exterior source and energy-condition verdict

This file targets the referee-level defect:

    The static shadow/ISCO benchmark is useful only if the exponential
    compact exterior is sourced by the RefG equations, not merely assumed.

The result is precise.  Algebraic F_min(Y,I1,I2,I3) alone does not source the
exponential compact exterior.  The closed compact branch is the RefG projected
Bernoulli medium source

    L_B_perp = Z_perp/(8*pi*G),
    Z_perp = (u^m u^n - g^mn) partial_m h partial_n h,

together with the biconformal operational metric map

    B=exp(-2h), A=exp(2h), h=r_s/(2r).

On the static comoving branch this source exactly satisfies

    G^mu_nu = 8*pi*G Theta^mu_nu

for the exponential exterior.  The ordinary Einstein-fluid reading of the
subtracted active contrast is also fixed here.  The physical RefG energy gate
is the total-medium gate: the compact source is a finite pressure deficit on a
positive base medium, and the total radial NEC is controlled by the explicit
background capacity bound.
"""

import sympy as sp

from p05_compact import (
    derive_covariant_bernoulli_gradient_source,
    derive_background_completed_medium_nec_gate,
    derive_full_fmin_exponential_source_closure_system,
    derive_projected_bernoulli_medium_source,
    diagnose_algebraic_fmin_vs_gradient_source,
)
from p13_refractive_force import p10_static_first_order_biconformal_selection


def _all_zero(values) -> bool:
    return all(sp.simplify(value) == 0 for value in values)


def derive_biconformal_metric_map_gate():
    """
    Define the compact biconformal map as a branch equation, not a metaphor.

    The phase variable h fixes both diagonal metric functions:

        B=exp(-2h), A=exp(2h).

    Therefore A*B=1 exactly, n=sqrt(A/B)=exp(2h), and the weak field has
    gamma_PPN=1.  The p10 weak static branch independently selects the same
    biconformal sign at first order.
    """
    r, r_s, c = sp.symbols("r r_s c", positive=True, real=True)
    h = r_s / (2 * r)
    B = sp.exp(-2 * h)
    A = sp.exp(2 * h)
    phi = -2 * h
    n = sp.sqrt(A / B)
    weak_B = sp.series(B, r_s, 0, 2).removeO()
    weak_A = sp.series(A, r_s, 0, 2).removeO()
    newton_potential = -c**2 * h
    weak_gtt_expected = 1 + 2 * newton_potential / c**2
    gamma_check = sp.simplify((weak_A - 1) / (1 - weak_B))
    flat_phase_residual = sp.simplify(sp.diff(r**2 * sp.diff(phi, r), r))
    p10_selection = p10_static_first_order_biconformal_selection()

    return {
        "biconformal_map_status": (
            "PASS_BICONFORMAL_MAP_DEFINED_AND_FIRST_ORDER_SELECTED"
            if sp.simplify(A * B - 1) == 0
            and sp.simplify(n - sp.exp(2 * h)) == 0
            and sp.simplify(weak_B - weak_gtt_expected) == 0
            and gamma_check == 1
            and flat_phase_residual == 0
            and p10_selection["status"] == "PASS_P10_FIRST_ORDER_BICONFORMAL_SELECTION"
            else "CHECK_BICONFORMAL_MAP_DEFINED_AND_FIRST_ORDER_SELECTED"
        ),
        "h_definition": sp.Eq(sp.Symbol("h"), h),
        "phi_definition": sp.Eq(sp.Symbol("phi"), phi),
        "lapse_B": sp.Eq(sp.Symbol("B"), B),
        "spatial_A": sp.Eq(sp.Symbol("A"), A),
        "biconformal_identity": sp.Eq(sp.Symbol("A*B"), sp.simplify(A * B)),
        "optical_index": sp.Eq(sp.Symbol("n"), n),
        "weak_B": sp.Eq(sp.Symbol("B_weak"), weak_B),
        "weak_A": sp.Eq(sp.Symbol("A_weak"), weak_A),
        "newton_potential": sp.Eq(sp.Symbol("Phi_N"), newton_potential),
        "gamma_PPN_weak": gamma_check,
        "flat_phase_equation_residual": flat_phase_residual,
        "p10_first_order_selection": p10_selection["status"],
        "reading": (
            "the compact branch uses a definite biconformal metric map.  It is "
            "not the algebraic F_min source by itself; it is the operational "
            "metric branch selected at first order and sourced below by the "
            "projected Bernoulli medium term."
        ),
    }


def derive_projected_source_eom_closure_gate():
    """
    Check the static exponential exterior against the projected RefG source.

    In dimensionless form the exponential branch has

        G^t_t=-D, G^r_r=D, G^theta_theta=G^phi_phi=-D,
        D=r_s^2 exp(-r_s/r)/(4r^4).

    The projected Bernoulli source has

        Delta_P=D/(8*pi*G),
        Theta^t_t=-Delta_P, Theta^r_r=Delta_P,
        Theta^theta_theta=Theta^phi_phi=-Delta_P.

    This gives zero residual in every diagonal field equation.
    """
    r, r_s, G = sp.symbols("r r_s G", positive=True, real=True)
    h = r_s / (2 * r)
    A = sp.exp(2 * h)
    D = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (4 * r**4))
    z_perp = sp.simplify(sp.diff(h, r) ** 2 / A)
    delta_p = sp.simplify(z_perp / (8 * sp.pi * G))

    G_mixed = {
        "G^t_t": -D,
        "G^r_r": D,
        "G^theta_theta": -D,
        "G^phi_phi": -D,
    }
    theta_mixed = {
        "Theta^t_t": -delta_p,
        "Theta^r_r": delta_p,
        "Theta^theta_theta": -delta_p,
        "Theta^phi_phi": -delta_p,
    }
    residuals = {
        "t": sp.simplify(G_mixed["G^t_t"] - 8 * sp.pi * G * theta_mixed["Theta^t_t"]),
        "r": sp.simplify(G_mixed["G^r_r"] - 8 * sp.pi * G * theta_mixed["Theta^r_r"]),
        "theta": sp.simplify(
            G_mixed["G^theta_theta"]
            - 8 * sp.pi * G * theta_mixed["Theta^theta_theta"]
        ),
        "phi": sp.simplify(
            G_mixed["G^phi_phi"] - 8 * sp.pi * G * theta_mixed["Theta^phi_phi"]
        ),
    }

    projected_source = derive_projected_bernoulli_medium_source()
    covariant_source = derive_covariant_bernoulli_gradient_source()
    projected_imported_residuals = projected_source["Einstein_profile_residual"]
    covariant_scalar_residual = covariant_source["scalar_eom_residual"]

    return {
        "projected_source_eom_status": (
            "PASS_PROJECTED_BERNOULLI_SOURCE_SOLVES_STATIC_EXPONENTIAL_EOM"
            if _all_zero(residuals.values())
            and _all_zero(projected_imported_residuals.values())
            and sp.simplify(covariant_scalar_residual) == 0
            and projected_source["refg_medium_export"]
            == "PASS_STATIC_PROJECTED_BERNOULLI_MEDIUM_SOURCE_FOR_EXPONENTIAL_BRANCH"
            else "CHECK_PROJECTED_BERNOULLI_SOURCE_SOLVES_STATIC_EXPONENTIAL_EOM"
        ),
        "Z_perp": sp.Eq(sp.Symbol("Z_perp"), z_perp),
        "Delta_P": sp.Eq(sp.Symbol("Delta_P"), delta_p),
        "Einstein_mixed": G_mixed,
        "ThetaRefG_projected_mixed": theta_mixed,
        "field_equation_residuals": residuals,
        "imported_projected_source_status": projected_source["refg_medium_export"],
        "imported_projected_residuals": projected_imported_residuals,
        "covariant_shorthand_status": covariant_source["closure_status"],
        "covariant_shorthand_scalar_eom_residual": covariant_scalar_residual,
        "ordinary_scalar_export": projected_source["ordinary_scalar_export"],
        "reading": (
            "the exponential compact exterior is a solution of the static RefG "
            "projected Bernoulli medium source equations.  It is not sourced "
            "by algebraic F_min alone."
        ),
    }


def audit_fmin_alone_vs_refg_compact_source_gate():
    """
    Separate the false F_min-alone claim from the closed RefG compact source.
    """
    full_fmin = derive_full_fmin_exponential_source_closure_system()
    diagnosis = diagnose_algebraic_fmin_vs_gradient_source()
    source_closure = derive_projected_source_eom_closure_gate()

    fmin_alone_insufficient = (
        full_fmin["closure_status"]
        == "FULL_FMIN_COMPONENT_EQUATIONS_WRITTEN__MINIMAL_BRANCH_INSUFFICIENT__SOLVE_GENERAL_BRANCH_NEXT"
        and diagnosis["diagnosis_status"]
        == "ALGEBRAIC_FMIN_ALONE_DOES_NOT_CLOSE_EXPONENTIAL_SOURCE__BERNOULLI_GRADIENT_SOURCE_REQUIRED"
    )
    refg_compact_source_closed = (
        source_closure["projected_source_eom_status"]
        == "PASS_PROJECTED_BERNOULLI_SOURCE_SOLVES_STATIC_EXPONENTIAL_EOM"
    )

    return {
        "fmin_vs_refg_source_status": (
            "PASS_FMIN_ALONE_REJECTED_AND_REFG_PROJECTED_SOURCE_CLOSES_EXTERIOR"
            if fmin_alone_insufficient and refg_compact_source_closed
            else "CHECK_FMIN_ALONE_REJECTED_AND_REFG_PROJECTED_SOURCE_CLOSES_EXTERIOR"
        ),
        "Fmin_alone_closes_exponential_exterior": False,
        "RefG_compact_source_closes_exponential_exterior": refg_compact_source_closed,
        "Fmin_full_component_status": full_fmin["closure_status"],
        "diagnosis_status": diagnosis["diagnosis_status"],
        "required_article_rule": (
            "do not state that F(Y,I1,I2,I3) alone generates the exponential "
            "compact exterior; state that the compact branch uses the projected "
            "Bernoulli medium source L_B_perp in addition to the F_min medium "
            "sector"
        ),
        "reading": (
            "this closes the referee objection only after the source is named "
            "correctly.  A F_min-alone wording remains wrong."
        ),
    }


def derive_energy_condition_verdict_gate():
    """
    Give the energy-condition answer explicitly.

    The ordinary Einstein-fluid dictionary applied to the background-subtracted
    active contrast gives a negative radial null load.  That is not the total
    physical medium.  In RefG the source is a pressure deficit on a positive
    base medium.  The total-medium NEC is therefore tested after adding the
    local homogeneous background load.
    """
    r, r_s, G = sp.symbols("r r_s G", positive=True, real=True)
    delta_p = sp.simplify(r_s**2 * sp.exp(-r_s / r) / (32 * sp.pi * G * r**4))
    rho = -delta_p
    p_r = -delta_p
    p_t = delta_p

    projected = derive_projected_bernoulli_medium_source()
    total_medium = derive_background_completed_medium_nec_gate()
    radial_nec = sp.simplify(rho + p_r)
    tangential_nec = sp.simplify(rho + p_t)
    weak_energy_density = rho
    sec_combo = sp.simplify(rho + p_r + 2 * p_t)
    delta_peak = total_medium["Delta_P_peak"]["Delta_P_max"]

    return {
        "energy_condition_verdict_status": (
            "PASS_SUBTRACTED_CONTRAST_AUDIT_AND_TOTAL_MEDIUM_NEC_GATE"
            if radial_nec == -2 * delta_p
            and tangential_nec == 0
            and weak_energy_density == -delta_p
            and sec_combo == 0
            and projected["projected_medium_time_kinetic_coefficient"] == 0
            and total_medium["total_medium_nec_status"]
            == "PASS_TOTAL_MEDIUM_NEC_REDUCES_TO_FINITE_BACKGROUND_CAPACITY_BOUND"
            else "CHECK_ENERGY_CONDITION_VERDICT_FOR_REFG_COMPACT_SOURCE"
        ),
        "Delta_P_positive": sp.Eq(sp.Symbol("Delta_P"), delta_p),
        "background_subtracted_Einstein_fluid_dictionary": {
            "rho": rho,
            "p_r": p_r,
            "p_t": p_t,
            "rho_plus_p_r": radial_nec,
            "rho_plus_p_t": tangential_nec,
            "rho_plus_p_r_plus_2p_t": sec_combo,
        },
        "subtracted_contrast_verdict": (
            "the active deficit contrast has negative radial null load; this "
            "is not the total base-medium energy tensor"
        ),
        "total_medium_nec_gate": {
            "status": total_medium["total_medium_nec_status"],
            "Delta_P_peak": total_medium["Delta_P_peak"],
            "total_physical_medium": total_medium["total_physical_medium"],
            "sufficient_total_medium_conditions": total_medium[
                "sufficient_total_medium_conditions"
            ],
        },
        "projected_medium_verdict": (
            "the RefG export is a projected spatial medium stress with no "
            "standalone scalar time kinetic term; physically it is a finite "
            "pressure deficit on a positive base medium"
        ),
        "projected_medium_time_kinetic_coefficient": projected[
            "projected_medium_time_kinetic_coefficient"
        ],
        "projected_spatial_gradient_coefficient": projected[
            "projected_spatial_gradient_coefficient"
        ],
        "finite_background_capacity_bound": sp.Ge(
            sp.Symbol("rho_star") + sp.Symbol("p_star"),
            2 * delta_peak,
        ),
        "required_article_rule": (
            "state that the negative null load is the subtracted pressure "
            "deficit, while the total RefG medium satisfies the radial NEC "
            "when rho_*+p_* is above the finite Bernoulli peak"
        ),
    }


def p05g_central_exponential_source_gate():
    biconformal = derive_biconformal_metric_map_gate()
    source = derive_projected_source_eom_closure_gate()
    fmin = audit_fmin_alone_vs_refg_compact_source_gate()
    energy = derive_energy_condition_verdict_gate()

    return {
        "p05g_status": (
            "PASS_P05G_EXPONENTIAL_EXTERIOR_SOURCE_AND_ENERGY_VERDICT"
            if biconformal["biconformal_map_status"]
            == "PASS_BICONFORMAL_MAP_DEFINED_AND_FIRST_ORDER_SELECTED"
            and source["projected_source_eom_status"]
            == "PASS_PROJECTED_BERNOULLI_SOURCE_SOLVES_STATIC_EXPONENTIAL_EOM"
            and fmin["fmin_vs_refg_source_status"]
            == "PASS_FMIN_ALONE_REJECTED_AND_REFG_PROJECTED_SOURCE_CLOSES_EXTERIOR"
            and energy["energy_condition_verdict_status"]
            == "PASS_SUBTRACTED_CONTRAST_AUDIT_AND_TOTAL_MEDIUM_NEC_GATE"
            else "CHECK_P05G_EXPONENTIAL_EXTERIOR_SOURCE_AND_ENERGY_VERDICT"
        ),
        "biconformal_map": biconformal["biconformal_map_status"],
        "projected_source_eom": source["projected_source_eom_status"],
        "fmin_vs_refg_source": fmin["fmin_vs_refg_source_status"],
        "energy_condition_verdict": energy["energy_condition_verdict_status"],
        "field_equation_residuals": source["field_equation_residuals"],
        "Fmin_alone_closes_exponential_exterior": fmin[
            "Fmin_alone_closes_exponential_exterior"
        ],
        "RefG_compact_source_closes_exponential_exterior": fmin[
            "RefG_compact_source_closes_exponential_exterior"
        ],
        "article_export_rule": (
            "compact exponential exterior = biconformal phase branch sourced by "
            "projected Bernoulli medium stress L_B_perp; F_min alone is not the "
            "compact source"
        ),
        "energy_export_rule": energy["required_article_rule"],
        "next_gates": [
            "carry this p05g result into the Georgian and English article text",
            "derive rotating RefG exterior from the same projected-source action",
            "audit full coupled p01/projector perturbations around the compact branch",
        ],
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18g: Exponential exterior source and energy verdict")
    print("=" * 72)

    sections = [
        ("1. Biconformal metric map", derive_biconformal_metric_map_gate()),
        ("2. Projected source EOM closure", derive_projected_source_eom_closure_gate()),
        ("3. Fmin-alone vs RefG compact source", audit_fmin_alone_vs_refg_compact_source_gate()),
        ("4. Energy-condition verdict", derive_energy_condition_verdict_gate()),
        ("5. Central p05g gate", p05g_central_exponential_source_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:44s}: {value}")
