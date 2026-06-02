# Notation header:
# signature (+---); compact branch uses positive metric functions
# B=exp(-r_s/r), A=exp(r_s/r) in ds^2=B c^2 dt^2-A dSigma^2.
#
# This gate searches for the foundational error exposed by the referee:
# raw F_min was treated as an ordinary exterior RHS source even though the
# intuitive theory treats it as a structural medium sector.  Tadpole/background
# subtraction is tested and rejected.  The result supports p05p: the compact
# tail is a double-counting diagnostic, not a physical active compact source.

from __future__ import annotations

import sympy as sp

from p05j_fmin_compact_exterior_gate import (
    _coefficient_symbols,
    _fmin_polynomial,
    solar_physical_fmin_coefficients,
)


def _mixed_stress_from_f(F, Y, lambda_r, lambda_t):
    F_Y = sp.diff(F, Y)
    F_lr = sp.diff(F, lambda_r)
    F_lt = sp.diff(F, lambda_t)
    return {
        "Theta^t_t": sp.simplify(2 * Y * F_Y - F),
        "Theta^r_r": sp.simplify(2 * lambda_r * F_lr - F),
        "Theta^theta_theta": sp.simplify(lambda_t * F_lt - F),
        "Theta^phi_phi": sp.simplify(lambda_t * F_lt - F),
    }


def derive_unit_background_tadpole_subtraction_gate():
    """
    Test the cleanest non-circular repair: subtract F_min background tadpoles.

    Define Q=(Y,lambda_r,lambda_t) and the homogeneous unit state
    Q0=(1,1,1).  The tadpole-renormalized density is

        F_R(Q)=F(Q)-F(Q0)-F_a(Q0)(Q^a-Q0^a).

    The physical Solar slice is already tadpole-free in the variables
    (Y,lambda_r,lambda_t).  Therefore this operation changes nothing.  If the
    compact tail remains, it is a Hessian/modulus effect rather than a bad
    background constant or first derivative.  In the compact source ledger it
    is then not repaired by subtraction; it is not inserted as ordinary RHS
    matter in the first place.
    """
    u, w = sp.symbols("u w", positive=True, real=True)
    coeff_symbols = _coefficient_symbols()
    _, c_Y2, _, _, _, _, _ = coeff_symbols
    Y, lambda_r, lambda_t = sp.symbols(
        "Y lambda_r lambda_t", positive=True, real=True
    )

    F = _fmin_polynomial(Y, lambda_r, lambda_t, coeff_symbols)
    F_solar = sp.simplify(F.subs(solar_physical_fmin_coefficients(coeff_symbols)))

    unit = {Y: 1, lambda_r: 1, lambda_t: 1}
    variables = [Y, lambda_r, lambda_t]
    F0 = sp.simplify(F_solar.subs(unit))
    grad0 = {var: sp.simplify(sp.diff(F_solar, var).subs(unit)) for var in variables}
    F_ren = sp.simplify(
        F_solar
        - F0
        - sum(grad0[var] * (var - unit[var]) for var in variables)
    )
    grad0_ren = {
        var: sp.simplify(sp.diff(F_ren, var).subs(unit)) for var in variables
    }
    hessian_same = {
        f"d2_{a}_{b}": sp.simplify(
            sp.diff(F_ren - F_solar, a, b).subs(unit)
        )
        for a in variables
        for b in variables
    }

    branch = {Y: w, lambda_r: 1 / w, lambda_t: 1 / w}
    raw_stress = _mixed_stress_from_f(F_solar, Y, lambda_r, lambda_t)
    ren_stress = _mixed_stress_from_f(F_ren, Y, lambda_r, lambda_t)
    raw_branch = {
        key: sp.factor(sp.simplify(value.subs(branch) / c_Y2))
        for key, value in raw_stress.items()
    }
    ren_branch = {
        key: sp.factor(sp.simplify(value.subs(branch) / c_Y2))
        for key, value in ren_stress.items()
    }
    raw_u_series = {
        key: sp.factor(sp.series(value.subs(w, sp.exp(u)), u, 0, 5).removeO())
        for key, value in raw_branch.items()
    }
    ren_u_series = {
        key: sp.factor(sp.series(value.subs(w, sp.exp(u)), u, 0, 5).removeO())
        for key, value in ren_branch.items()
    }

    leading_raw_order = {
        key: value.as_leading_term(u) for key, value in raw_u_series.items()
    }
    leading_ren_order = {
        key: value.as_leading_term(u) for key, value in ren_u_series.items()
    }

    stress_exact_zero = all(sp.simplify(value) == 0 for value in ren_branch.values())
    raw_tadpole_free = F0 == 0 and all(value == 0 for value in grad0.values())
    tadpole_removed = F0 == 0 and all(value == 0 for value in grad0_ren.values())
    hessian_preserved = all(value == 0 for value in hessian_same.values())

    return {
        "tadpole_subtraction_status": (
            "FAIL_TADPOLE_SUBTRACTION_DOES_NOT_REMOVE_COMPACT_LINEAR_TAIL"
            if raw_tadpole_free and tadpole_removed and hessian_preserved and not stress_exact_zero
            else "PASS_TADPOLE_SUBTRACTION_EXACTLY_SILENCES_COMPACT_FMIN"
            if tadpole_removed and hessian_preserved and stress_exact_zero
            else "CHECK_TADPOLE_SUBTRACTION"
        ),
        "raw_unit_F_over_cY2": sp.simplify(F0 / c_Y2),
        "raw_unit_gradient_over_cY2": {
            str(key): sp.simplify(value / c_Y2) for key, value in grad0.items()
        },
        "raw_slice_is_already_tadpole_free": raw_tadpole_free,
        "ren_unit_gradient": grad0_ren,
        "hessian_difference_at_unit": hessian_same,
        "raw_compact_stress_over_cY2": raw_branch,
        "ren_compact_stress_over_cY2": ren_branch,
        "raw_compact_stress_u_series": raw_u_series,
        "ren_compact_stress_u_series": ren_u_series,
        "raw_leading_terms": leading_raw_order,
        "ren_leading_terms": leading_ren_order,
        "meaning": (
            "The unit-background tadpoles are already zero on the physical "
            "Solar slice.  The compact 1/r F_min tail is therefore not a bad "
            "constant or first-derivative calibration; it is produced by the "
            "quadratic modulus along the compact biconformal direction.  This "
            "is the double-counting diagnostic: tadpole subtraction is not the "
            "repair; the p05p source ledger keeps F_min structural on the "
            "compact branch."
        ),
    }


def derive_compact_linear_tail_vs_solar_family_gate():
    """
    Check whether the Solar-family coefficients can also silence the mistaken
    compact RHS insertion of the biconformal F_min tail.

    p03 gives the Solar-family relations

        c_Y=-4 c_Y2-2 c_YI1,
        c_I1=4 c_Y2+2 c_YI1,
        c_I1sq=c_Y2,
        c_I2=-10 c_Y2-3 c_YI1,
        c_I3=8 c_Y2+4 c_YI1.

    The physical Solar q_2PN=7/4 scale uses c_YI1=2 c_Y2.  This gate asks a
    sharper diagnostic question: what value of c_YI1/c_Y2 would remove the
    first compact biconformal F_min stress tail if one forced F_min into the
    compact RHS ledger?
    """
    u, w = sp.symbols("u w", positive=True, real=True)
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = _coefficient_symbols()
    Y, lambda_r, lambda_t = sp.symbols(
        "Y lambda_r lambda_t", positive=True, real=True
    )

    F = _fmin_polynomial(Y, lambda_r, lambda_t, _coefficient_symbols())
    solar_family = {
        c_Y: -4 * c_Y2 - 2 * c_YI1,
        c_I1: 4 * c_Y2 + 2 * c_YI1,
        c_I1sq: c_Y2,
        c_I2: -10 * c_Y2 - 3 * c_YI1,
        c_I3: 8 * c_Y2 + 4 * c_YI1,
    }
    F_family = sp.simplify(F.subs(solar_family))
    branch = {Y: w, lambda_r: 1 / w, lambda_t: 1 / w}
    stress = _mixed_stress_from_f(F_family, Y, lambda_r, lambda_t)
    stress_branch = {
        key: sp.factor(sp.simplify(value.subs(branch)))
        for key, value in stress.items()
    }
    linear_tail = {
        key: sp.factor(
            sp.simplify(sp.diff(value.subs(w, sp.exp(u)), u).subs(u, 0))
        )
        for key, value in stress_branch.items()
    }
    tail_equations = [sp.Eq(value, 0) for value in linear_tail.values()]
    tail_solution = sp.solve(tail_equations, [c_YI1], dict=True)
    tail_solution_value = tail_solution[0][c_YI1] if tail_solution else None
    physical_solar_value = 2 * c_Y2
    compatible_with_physical_solar = (
        sp.simplify(tail_solution_value - physical_solar_value) == 0
        if tail_solution_value is not None
        else False
    )
    physical_linear_tail = {
        key: sp.simplify(value.subs(c_YI1, physical_solar_value))
        for key, value in linear_tail.items()
    }

    return {
        "compact_tail_vs_solar_family_status": (
            "PASS_SOLAR_PHYSICAL_SLICE_SILENCES_COMPACT_LINEAR_TAIL"
            if compatible_with_physical_solar
            else "FAIL_SOLAR_PHYSICAL_SLICE_CONFLICTS_WITH_COMPACT_FMIN_TAIL_SILENCING"
        ),
        "solar_family_relations": solar_family,
        "compact_linear_tail": linear_tail,
        "tail_silencing_solution": tail_solution,
        "physical_solar_q2pn_value": sp.Eq(c_YI1, physical_solar_value),
        "physical_solar_linear_tail": physical_linear_tail,
        "compatible_with_physical_solar_q2pn": compatible_with_physical_solar,
        "meaning": (
            "If the compact exponential branch is forced to use the same raw "
            "Solar F_min modulus, the physical Solar q_2PN=7/4 value does not "
            "silence the compact biconformal tail.  The formal error is using "
            "one structural F_min modulus as ordinary active RHS matter in "
            "both regimes.  The compact branch uses the p05p source ledger: "
            "projected deficit is active RHS, F_min is structural medium "
            "sector."
        ),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18m: F_min tadpole renormalization gate")
    print("=" * 72)
    sections = [
        ("1. Unit-background tadpole subtraction", derive_unit_background_tadpole_subtraction_gate()),
        ("2. Compact linear tail vs Solar family", derive_compact_linear_tail_vs_solar_family_gate()),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:46s}: {value}")
