"""Exact, conditional F1 atemporal spectral-split candidate.

Scientific content retained from the original audit file
--------------------------------------------------------
The state is one real symmetric traceless 3 x 3 internal operator ``Q``.
``Q ~ R Q R.T`` for ``R in O(3)`` is an internal relabelling, not a rotation
of physical space.  The atemporal rule selects global minima of

    V(Q) = -alpha Tr(Q^2)/2 - b Tr(Q^3)/3 + c Tr(Q^2)^2/4,

on the open parameter domain ``alpha,b,c > 0``.  The script proves that the
nonzero global minimum is one O(3) quotient orbit, stable on its orbit-normal
slice, and that its state-generated spectral projectors have ranks one and
two.  This is an exact mathematical candidate relative to imported
primitives.  It does not derive those primitives and does not establish time,
space, nodes, relations, modes, gravity, or an observable prediction.
"""
from __future__ import annotations

import json
import sys
from typing import Any

import sympy as sp


MODEL_VERSION = "W2-F1-ATEMPORAL-SPECTRAL-SPLIT-v1.0-scientific"
CLAIM_ID = "W2_F1_ATEMPORAL_SPECTRAL_SPLIT_CANDIDATE_001"

ASSUMPTIONS = (
    "one internal carrier Q in Sym_0(3,R)",
    "Q and R Q R^T are equivalent for every R in O(3)",
    "Q -> -Q is not part of the declared equivalence",
    "alpha, b, and c are strictly positive",
    "physical candidates are global minima modulo O(3)",
)

IMPORTED_NOT_DERIVED = (
    "single_internal_carrier_Q",
    "Sym0_3_R_internal_configuration_space",
    "positive_definite_internal_delta_and_transpose",
    "matrix_product_and_Tr_alg",
    "O3_internal_conjugation_relabel_equivalence",
    "absence_of_Q_sign_relabel_symmetry",
    "atemporal_global_argmin_rule",
    "positive_open_parameter_domain_alpha_b_c",
    "quartic_invariant_functional_form_signs_and_truncation",
)

DEFERRED_OUTPUTS = (
    "physical node or persistent imprint",
    "operational relations and internal causal order",
    "independent additive physical modes",
    "spacetime dimension, metric, action, and gravity bridge",
    "observables and comparison with data",
)

PASS_CONDITIONS = (
    "the sharp invariant bound identifies one nonzero global-minimum orbit",
    "the origin is stationary but unstable for alpha>0",
    "the orbit-normal Hessian has one radial and two biaxial positive modes",
    "the only two zero Hessian modes are O(3)-orbit relabellings",
    "Q itself generates orthogonal projectors of ranks one and two",
    "N=1, N=2, b=0, coercivity, polarity, and source-preloading controls hold",
)

FALSIFIER = (
    "Any alpha,b,c>0 and Q in Sym_0(3,R) below the stated minimum, or any "
    "non-orbit perturbation with nonpositive second variation, falsifies the claim."
)


def matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def run_gate() -> dict[str, Any]:
    alpha, b, c, s = sp.symbols("alpha b c s", positive=True, real=True)
    x, y, u, v, w = sp.symbols("x y u v w", real=True)
    coordinates = (x, y, u, v, w)
    Q = sp.Matrix([[x, u, v], [u, y, w], [v, w, -x - y]])
    basis = tuple(Q.diff(variable) for variable in coordinates)
    gram = sp.Matrix([[sp.trace(a * d) for d in basis] for a in basis])
    I2 = sp.expand(sp.trace(Q**2))
    I3 = sp.expand(sp.trace(Q**3))
    V = sp.expand(-alpha * I2 / 2 - b * I3 / 3 + c * I2**2 / 4)
    gradient = sp.Matrix([sp.diff(V, variable) for variable in coordinates])
    hessian = sp.hessian(V, coordinates)

    zero = {variable: 0 for variable in coordinates}
    origin_gradient = sp.simplify(gradient.subs(zero))
    origin_hessian = sp.simplify(hessian.subs(zero))
    origin_exact = matrix_is_zero(origin_gradient) and matrix_is_zero(
        origin_hessian + alpha * gram
    )

    # For real eigenvalues l1+l2+l3=0, the discriminant gives the sharp bound
    # I2^3 >= 6 I3^2.  Equality is precisely the uniaxial spectrum.
    l1, l2 = sp.symbols("l1 l2", real=True)
    l3 = -l1 - l2
    I2_eig = sp.expand(l1**2 + l2**2 + l3**2)
    I3_eig = sp.expand(l1**3 + l2**3 + l3**3)
    discriminant = sp.expand(
        (l1 - l2) ** 2 * (l2 - l3) ** 2 * (l3 - l1) ** 2
    )
    sharp_bound_residual = sp.expand(I2_eig**3 - 6 * I3_eig**2 - 2 * discriminant)

    Delta = sp.sqrt(b**2 + 24 * alpha * c)
    s_plus = sp.simplify((b + Delta) / (4 * c))
    s_minus = sp.simplify((b - Delta) / (4 * c))
    s_minus_negative_form = -6 * alpha / (b + Delta)
    stationary_polynomial = lambda z: sp.simplify(2 * c * z**2 - b * z - 3 * alpha)
    roots_exact = stationary_polynomial(s_plus) == 0 and stationary_polynomial(s_minus) == 0

    star = {x: 2 * s / 3, y: -s / 3, u: 0, v: 0, w: 0}
    on_shell = {alpha: (2 * c * s**2 - b * s) / 3}
    Q_star = sp.simplify(Q.subs(star))
    star_gradient = sp.simplify(gradient.subs(star).subs(on_shell))
    star_energy = sp.factor(V.subs(star).subs(on_shell))
    expected_energy = s**3 * (b - 3 * c * s) / 27
    # Every critical eigenvalue obeys the same quadratic equation obtained
    # from the traceless matrix Euler equation below.  Hence a nonzero
    # critical 3x3 state has at most two eigenvalues and, by tracelessness,
    # multiplicities 1+2.  The two amplitudes are therefore exhaustive.
    eom_matrix = sp.simplify(
        -alpha * Q - b * (Q**2 - sp.eye(3) * I2 / 3) + c * I2 * Q
    )
    eom_coordinate_pairing = sp.Matrix([
        sp.expand(sp.trace(eom_matrix * direction)) for direction in basis
    ])
    eom_gradient_residual = sp.simplify(eom_coordinate_pairing - gradient)
    stationary_energy = sp.expand(
        -alpha * s**2 / 3 - 2 * b * s**3 / 27 + c * s**4 / 9
    )
    energy_plus = sp.simplify(stationary_energy.subs(s, s_plus))
    energy_minus = sp.simplify(stationary_energy.subs(s, s_minus))
    energy_order_residual = sp.simplify(
        energy_plus - energy_minus + b * Delta**3 / (432 * c**3)
    )
    positive_energy_gap = b * Delta**3 / (432 * c**3)
    minimum_below_origin_factor = sp.simplify(3 * c * s_plus - b)
    positive_minimum_factor = 2 * b + 72 * alpha * c / (Delta + b)
    negative_branch_exact = all((
        sp.simplify(s_minus - s_minus_negative_form) == 0,
        s_minus_negative_form.is_negative is True,
        (b * s_minus_negative_form).is_negative is True,
        sp.simplify(4 * c * s_minus - b + Delta) == 0,
    ))
    stationary_classification_exact = all((
        matrix_is_zero(eom_gradient_residual),
        roots_exact,
        negative_branch_exact,
        energy_order_residual == 0,
        positive_energy_gap.is_positive is True,
        sp.simplify(minimum_below_origin_factor - positive_minimum_factor / 4) == 0,
        positive_minimum_factor.is_positive is True,
    ))

    global_orbit_exact = all((
        sharp_bound_residual == 0,
        stationary_classification_exact,
        matrix_is_zero(star_gradient),
        sp.simplify(I2.subs(star) - 2 * s**2 / 3) == 0,
        sp.simplify(I3.subs(star) - 2 * s**3 / 9) == 0,
        sp.simplify(star_energy - expected_energy) == 0,
        sp.simplify(4 * c * s_plus - b) == Delta,
        sp.simplify(b * s_minus - b * (b - Delta) / (4 * c)) == 0,
    ))

    # Exact normal-slice Hessian decomposition.  The last two columns are
    # tangent to the relabelling orbit and therefore must be zero modes.
    hessian_star = sp.simplify(hessian.subs(star).subs(on_shell))
    modes = sp.Matrix.hstack(
        sp.Matrix([sp.Rational(2, 3), -sp.Rational(1, 3), 0, 0, 0]),
        sp.Matrix([0, 1, 0, 0, 0]),
        sp.Matrix([0, 0, 0, 0, 1]),
        sp.Matrix([0, 0, 1, 0, 0]),
        sp.Matrix([0, 0, 0, 1, 0]),
    )
    mode_gram = sp.simplify(modes.T * gram * modes)
    mode_hessian = sp.simplify(modes.T * hessian_star * modes)
    radial = s * (4 * c * s - b) / 3
    biaxial = b * s
    expected_hessian = sp.diag(
        mode_gram[0, 0] * radial,
        mode_gram[1, 1] * biaxial,
        mode_gram[2, 2] * biaxial,
        0,
        0,
    )
    hessian_residual = sp.simplify(mode_hessian - expected_hessian)
    quotient_stability_exact = all((
        modes.det() != 0,
        matrix_is_zero(hessian_residual),
        sp.simplify(4 * c * s_plus - b) == Delta,
        s_plus.is_positive is True,
    ))

    identity = sp.eye(3)
    P1 = sp.simplify(Q_star / s + identity / 3)
    P2 = sp.simplify(identity - P1)
    projector_exact = all((
        matrix_is_zero(P1**2 - P1),
        matrix_is_zero(P2**2 - P2),
        matrix_is_zero(P1 * P2),
        P1.rank() == 1,
        P2.rank() == 2,
        matrix_is_zero(Q_star - s * (P1 - identity / 3)),
    ))

    # O(3) invariance and faithful action modulo the central kernel {+I,-I}.
    theta = sp.symbols("theta", real=True)
    rotations = (
        sp.Matrix([[sp.cos(theta), -sp.sin(theta), 0], [sp.sin(theta), sp.cos(theta), 0], [0, 0, 1]]),
        sp.Matrix([[sp.cos(theta), 0, -sp.sin(theta)], [0, 1, 0], [sp.sin(theta), 0, sp.cos(theta)]]),
        sp.Matrix([[1, 0, 0], [0, sp.cos(theta), -sp.sin(theta)], [0, sp.sin(theta), sp.cos(theta)]]),
    )
    invariance_exact = True
    for rotation in rotations:
        rotated = sp.simplify(rotation * Q * rotation.T)
        invariance_exact &= sp.simplify(
            sp.trigsimp(sp.expand(sp.trace(rotated**2) - I2))
        ) == 0
        invariance_exact &= sp.simplify(
            sp.trigsimp(sp.expand(sp.trace(rotated**3) - I3))
        ) == 0
    reflection = sp.diag(-1, 1, 1)
    faithful_action_exact = matrix_is_zero(
        (-reflection) * Q * (-reflection).T - reflection * Q * reflection.T
    )

    # Boundary and target-preloading controls.
    qx, qy = sp.symbols("qx qy", real=True)
    Q2 = sp.Matrix([[qx, qy], [qy, -qx]])
    n1_traceless_state = sp.Matrix([[0]])
    n1_trivial = n1_traceless_state.rank() == 0
    n2_equal_rank = sp.trace(Q2**3) == 0
    N, t = sp.symbols("N t", integer=True, positive=True)
    ratio_N = sp.simplify(
        (N * (N - 1) * (N - 2) * t**3) ** 2
        / (N * (N - 1) * t**2) ** 3
    )
    dimension_control = all((
        n1_trivial,
        sp.simplify(ratio_N - (N - 2) ** 2 / (N * (N - 1))) == 0,
        ratio_N.subs(N, 2) == 0,
        ratio_N.subs(N, 3) == sp.Rational(1, 6),
        ratio_N.subs(N, 4) == sp.Rational(1, 3),
    ))
    r = sp.symbols("r", positive=True, real=True)
    reduced_V = -alpha * r**2 / 2 - b * r**3 / (3 * sp.sqrt(6)) + c * r**4 / 4
    c_bad = sp.symbols("c_bad", positive=True, real=True)
    coercivity_control = all((
        sp.limit(reduced_V.subs(c, 0), r, sp.oo) == -sp.oo,
        sp.limit(reduced_V.subs(c, -c_bad), r, sp.oo) == -sp.oo,
    ))
    unit_uniaxial = sp.sqrt(sp.Rational(3, 2)) * sp.diag(
        sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3)
    )
    unit_biaxial = sp.diag(1 / sp.sqrt(2), -1 / sp.sqrt(2), 0)
    b_zero_degeneracy = all((
        sp.simplify(sp.trace(unit_uniaxial**2)) == 1,
        sp.simplify(sp.trace(unit_biaxial**2)) == 1,
        sp.simplify(sp.trace(unit_uniaxial**3))
        != sp.simplify(sp.trace(unit_biaxial**3)),
    ))
    stable_null = alpha * I2 / 2 + c * I2**2 / 4
    stable_null_hessian = sp.simplify(sp.hessian(stable_null, coordinates).subs(zero))
    stable_positive_quadratic_null = matrix_is_zero(stable_null_hessian - alpha * gram)
    alpha_zero_marginal = matrix_is_zero(origin_hessian.subs(alpha, 0))
    sign_flip = {variable: -variable for variable in coordinates}
    polarity_control = sp.simplify(
        V.subs(sign_flip, simultaneous=True) - V.subs(b, -b)
    ) == 0
    h = sp.symbols("h", nonzero=True, real=True)
    prewired_gradient = sp.Matrix([
        sp.diff(V - h * x, variable) for variable in coordinates
    ]).subs(zero)
    source_preloading_detected = prewired_gradient[0] == -h
    controls_exact = all((
        n2_equal_rank,
        dimension_control,
        b_zero_degeneracy,
        stable_positive_quadratic_null,
        alpha_zero_marginal,
        coercivity_control,
        polarity_control,
        negative_branch_exact,
        source_preloading_detected,
    ))

    checks = {
        "origin_stationary_and_unstable": bool(origin_exact),
        "sharp_bound_and_unique_global_orbit": bool(global_orbit_exact),
        "stationary_branches_exhaustive_and_energy_ordered": bool(stationary_classification_exact),
        "orbit_normal_hessian_positive": bool(quotient_stability_exact),
        "state_generated_rank_1_rank_2_projectors": bool(projector_exact),
        "O3_invariance_and_faithful_quotient": bool(invariance_exact and faithful_action_exact),
        "N1_traceless_state_is_trivial": bool(n1_trivial),
        "N2_has_no_unequal_rank_cubic_split": bool(n2_equal_rank),
        "N3_N4_generalN_dimension_control": bool(dimension_control),
        "b_zero_quotient_is_degenerate": bool(b_zero_degeneracy),
        "positive_quadratic_null_has_stable_origin": bool(stable_positive_quadratic_null),
        "alpha_zero_origin_is_marginal": bool(alpha_zero_marginal),
        "c_nonpositive_is_noncoercive": bool(coercivity_control),
        "Q_sign_polarity_mirror_exact": bool(polarity_control),
        "negative_stationary_branch_rejected": bool(negative_branch_exact),
        "explicit_linear_source_is_detected": bool(source_preloading_detected),
        "all_boundary_null_and_preloading_controls": bool(controls_exact),
    }
    exact_candidate = all(checks.values())
    return {
        "MODEL_VERSION": MODEL_VERSION,
        "CLAIM_ID": CLAIM_ID,
        "STATUS": (
            "EXACT_ATEMPORAL_SPECTRAL_CANDIDATE_PASS__PHYSICAL_F1_OPEN"
            if exact_candidate else
            "ATEMPORAL_SPECTRAL_CANDIDATE_FAIL__PHYSICAL_F1_OPEN"
        ),
        "CHECKS": checks,
        "DIAGNOSTICS": {
            "sharp_bound_residual": str(sharp_bound_residual),
            "s_plus": str(s_plus),
            "s_minus": str(s_minus),
            "s_minus_negative_form": str(s_minus_negative_form),
            "stationary_E_plus_minus_E_minus": str(sp.simplify(energy_plus - energy_minus)),
            "stationary_energy_order_residual": str(energy_order_residual),
            "eom_gradient_residual": str(eom_gradient_residual),
            "Q_star": str(Q_star),
            "star_energy_on_shell": str(star_energy),
            "mode_hessian_residual": str(hessian_residual),
            "projector_ranks": [P1.rank(), P2.rank()],
            "general_N_cubic_ratio_squared": str(ratio_N),
        },
        "ASSUMPTIONS": list(ASSUMPTIONS),
        "IMPORTED_NOT_DERIVED": list(IMPORTED_NOT_DERIVED),
        "DEFERRED_OUTPUTS": list(DEFERRED_OUTPUTS),
        "PASS_CONDITIONS": list(PASS_CONDITIONS),
        "FALSIFIER": FALSIFIER,
        "SCOPE_CEILING": (
            "conditional exact atemporal internal candidate; no physical F1, "
            "F2, spacetime, gravity, or observation"
        ),
        "CLOSURE_FLAGS": {
            "ATEMPORAL_SPECTRAL_SPLIT_EXACT": exact_candidate,
            "QUOTIENT_STABILITY_EXACT": exact_candidate and quotient_stability_exact,
            "W2_F1_CONDITIONAL_CANDIDATE": exact_candidate,
            "W2_F1_SELF_DIFFERENTIATION": False,
        },
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["STATUS"].startswith("EXACT_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
