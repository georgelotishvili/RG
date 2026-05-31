# Notation header (see NOTATION.md):
# signature (+---); dimensionless frequency is Omega=omega*r_s/c.

"""
PHASE 18c: Variable-profile matrix QNM pole gate

This file continues p05b_core_spectrum.py without growing that ledger further.
The previous file derived an admissible variable eigenbasis profile and checked
its real-frequency finite-interval transfer matrix.  This file embeds that
transfer into a reduced complex pole condition.

The pole condition used here is matrix-valued:

    det(I - R_ext(Omega) R_core(Omega)) = 0.

R_ext is the diagonal exterior photon-barrier reflection matrix for the two
radial eigenchannels.  R_core is the finite-core reflection matrix obtained by
propagating the coupled variable-profile system, applying regular-center
reflection, and propagating back to the exterior interface.  In the eps=0 limit
this reduces to the two branch-corrected one-channel denominators already
checked in p05b.
"""

import cmath
import math

from p05b_core_spectrum import (
    _profile_p_minus_prime_value,
    _profile_p_minus_second_value,
    _profile_p_minus_value,
    _rk4_outgoing_jost,
    compute_branch_corrected_reduced_root_scan_gate,
    run_variable_profile_matrix_radial_system_gate,
)


S_MINUS = 9.0 / 17.0
S_PLUS = 1.0


def _complex_profile_rhs(z_value: float, state, omega_value: complex, eps_value: float):
    """First-order complex form of the variable-profile eigenbasis system."""
    a_minus, a_plus, v_minus, v_plus = state
    p_minus = _profile_p_minus_value(z_value, eps_value)
    p_prime = _profile_p_minus_prime_value(z_value, eps_value)
    p_second = _profile_p_minus_second_value(z_value, eps_value)
    denom = p_minus - 1.0

    gamma00 = p_prime / denom
    gamma10 = -p_prime / denom
    mix00 = p_second / denom
    mix10 = -p_second / denom

    k_minus_sq = omega_value**2 / S_MINUS
    k_plus_sq = omega_value**2 / S_PLUS

    acc_minus = -2.0 * gamma00 * v_minus - (k_minus_sq + mix00) * a_minus
    acc_plus = -2.0 * gamma10 * v_minus - mix10 * a_minus - k_plus_sq * a_plus
    return [v_minus, v_plus, acc_minus, acc_plus]


def _rk4_complex_profile_column(initial, omega_value: complex, eps_value: float, steps: int):
    h = 1.0 / steps
    state = [complex(value) for value in initial]
    z_value = 0.0

    def add_scaled(base, delta, scale):
        return [base[index] + scale * delta[index] for index in range(4)]

    for _ in range(steps):
        k1 = _complex_profile_rhs(z_value, state, omega_value, eps_value)
        k2 = _complex_profile_rhs(
            z_value + h / 2.0,
            add_scaled(state, k1, h / 2.0),
            omega_value,
            eps_value,
        )
        k3 = _complex_profile_rhs(
            z_value + h / 2.0,
            add_scaled(state, k2, h / 2.0),
            omega_value,
            eps_value,
        )
        k4 = _complex_profile_rhs(
            z_value + h,
            add_scaled(state, k3, h),
            omega_value,
            eps_value,
        )
        state = [
            state[index]
            + h * (k1[index] + 2.0 * k2[index] + 2.0 * k3[index] + k4[index]) / 6.0
            for index in range(4)
        ]
        z_value += h
    return state


def _complex_profile_transfer_matrix(
    omega_value: complex,
    eps_value: float,
    steps: int,
):
    columns = [
        _rk4_complex_profile_column(initial, omega_value, eps_value, steps)
        for initial in (
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        )
    ]
    return [[columns[col][row] for col in range(4)] for row in range(4)]


def _matmul(left, right):
    rows = len(left)
    inner = len(right)
    cols = len(right[0])
    return [
        [
            sum(left[row][k] * right[k][col] for k in range(inner))
            for col in range(cols)
        ]
        for row in range(rows)
    ]


def _diag2(a, b):
    return [[a, 0.0j], [0.0j, b]]


def _sub2(left, right):
    return [
        [left[row][col] - right[row][col] for col in range(2)]
        for row in range(2)
    ]


def _add2(left, right):
    return [
        [left[row][col] + right[row][col] for col in range(2)]
        for row in range(2)
    ]


def _mul2(left, right):
    return [
        [
            left[row][0] * right[0][col] + left[row][1] * right[1][col]
            for col in range(2)
        ]
        for row in range(2)
    ]


def _det2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def _inv2(matrix):
    det = _det2(matrix)
    return [
        [matrix[1][1] / det, -matrix[0][1] / det],
        [-matrix[1][0] / det, matrix[0][0] / det],
    ]


def _identity2():
    return [[1.0 + 0.0j, 0.0j], [0.0j, 1.0 + 0.0j]]


def _block2(matrix, row_block: int, col_block: int):
    r0 = 2 * row_block
    c0 = 2 * col_block
    return [
        [matrix[r0 + row][c0 + col] for col in range(2)]
        for row in range(2)
    ]


def _state_from_amplitude_matrix(omega_value: complex):
    k_minus = omega_value / math.sqrt(S_MINUS)
    k_plus = omega_value
    return [
        [1.0 + 0.0j, 0.0j, 1.0 + 0.0j, 0.0j],
        [0.0j, 1.0 + 0.0j, 0.0j, 1.0 + 0.0j],
        [1j * k_minus, 0.0j, -1j * k_minus, 0.0j],
        [0.0j, 1j * k_plus, 0.0j, -1j * k_plus],
    ]


def _amplitude_from_state_matrix(omega_value: complex):
    k_minus = omega_value / math.sqrt(S_MINUS)
    k_plus = omega_value
    return [
        [0.5, 0.0j, 1.0 / (2.0j * k_minus), 0.0j],
        [0.0j, 0.5, 0.0j, 1.0 / (2.0j * k_plus)],
        [0.5, 0.0j, -1.0 / (2.0j * k_minus), 0.0j],
        [0.0j, 0.5, 0.0j, -1.0 / (2.0j * k_plus)],
    ]


def _profile_core_reflection_matrix(
    omega_value: complex,
    eps_value: float,
    ell_value: int,
    profile_steps: int,
):
    """
    Reflection matrix at the outer edge of the finite profile.

    Amplitudes are ordered as right-moving minus/plus followed by left-moving
    minus/plus.  The regular center gives the channel reflection phase
    (-1)^(ell+1).  For eps=0 this returns diag(R_c exp(2ik_-), R_c exp(2ik_+)).
    """
    state_transfer = _complex_profile_transfer_matrix(
        omega_value,
        eps_value,
        steps=profile_steps,
    )
    amp_transfer = _matmul(
        _matmul(_amplitude_from_state_matrix(omega_value), state_transfer),
        _state_from_amplitude_matrix(omega_value),
    )

    m_pp = _block2(amp_transfer, 0, 0)
    m_pm = _block2(amp_transfer, 0, 1)
    m_mp = _block2(amp_transfer, 1, 0)
    m_mm = _block2(amp_transfer, 1, 1)
    center_phase = complex((-1) ** (ell_value + 1))
    r_center = _diag2(center_phase, center_phase)

    numerator = _add2(_mul2(m_pp, r_center), m_pm)
    denominator = _add2(_mul2(m_mp, r_center), m_mm)
    return _mul2(numerator, _inv2(denominator))


def _max_offdiag_abs2(matrix):
    return max(abs(matrix[0][1]), abs(matrix[1][0]))


def _max_abs2(matrix):
    return max(abs(value) for row in matrix for value in row)


def _matrix_pole_determinant(
    omega_value: complex,
    eps_value: float,
    branch_times,
    ell_value: int,
    q_value: float,
    x_out: float,
    jost_steps: int,
    profile_steps: int,
):
    """
    Reduced matrix pole determinant det(I - R_ext R_core).

    The profile interval has unit length in its normalized coordinate.  A
    diagonal calibration phase supplies the remaining branch travel time, so
    eps=0 reproduces the p05b branch-corrected one-channel denominators.
    """
    r_profile = _profile_core_reflection_matrix(
        omega_value,
        eps_value,
        ell_value,
        profile_steps,
    )
    delay_minus = branch_times["minus"] - 1.0 / math.sqrt(S_MINUS)
    delay_plus = branch_times["plus"] - 1.0
    delay = _diag2(
        cmath.exp(2j * omega_value * delay_minus),
        cmath.exp(2j * omega_value * delay_plus),
    )
    r_core = _mul2(delay, r_profile)

    r_minus = _rk4_outgoing_jost(
        omega_value,
        ell_value,
        q_value,
        x_out=x_out,
        steps=jost_steps,
        s_value=S_MINUS,
    )["R_ph"]
    r_plus = _rk4_outgoing_jost(
        omega_value,
        ell_value,
        q_value,
        x_out=x_out,
        steps=jost_steps,
        s_value=S_PLUS,
    )["R_ph"]
    r_ext = _diag2(r_minus, r_plus)
    roundtrip = _mul2(r_ext, r_core)
    determinant = _det2(_sub2(_identity2(), roundtrip))
    return {
        "determinant": determinant,
        "core_reflection_matrix": r_core,
        "profile_reflection_matrix": r_profile,
        "exterior_reflection_matrix": r_ext,
        "roundtrip_matrix": roundtrip,
    }


def _newton_complex_determinant_root(
    initial: complex,
    eps_value: float,
    branch_times,
    ell_value: int,
    q_value: float,
    x_out: float,
    jost_steps: int,
    profile_steps: int,
    max_iter: int = 7,
):
    z = initial
    history = []
    converged = False

    def f(value):
        return _matrix_pole_determinant(
            value,
            eps_value,
            branch_times,
            ell_value,
            q_value,
            x_out,
            jost_steps,
            profile_steps,
        )["determinant"]

    for index in range(max_iter):
        residual = f(z)
        residual_abs = abs(residual)
        history.append({
            "iteration": index,
            "Omega_real": z.real,
            "Omega_imag": z.imag,
            "residual_abs": residual_abs,
        })
        if residual_abs < 1.0e-9:
            converged = True
            break

        h = 1.0e-5 * (1.0 + abs(z))
        derivative = (f(z + h) - f(z - h)) / (2.0 * h)
        if abs(derivative) < 1.0e-14:
            break
        z -= residual / derivative

    final = _matrix_pole_determinant(
        z,
        eps_value,
        branch_times,
        ell_value,
        q_value,
        x_out,
        jost_steps,
        profile_steps,
    )
    final_residual = final["determinant"]
    return {
        "Omega_real": z.real,
        "Omega_imag": z.imag,
        "determinant_abs": abs(final_residual),
        "converged": converged or abs(final_residual) < 1.0e-9,
        "iterations": len(history),
        "history": history,
        "core_offdiag_abs": _max_offdiag_abs2(final["core_reflection_matrix"]),
        "roundtrip_offdiag_abs": _max_offdiag_abs2(final["roundtrip_matrix"]),
        "max_core_entry_abs": _max_abs2(final["core_reflection_matrix"]),
    }


def compute_variable_profile_matrix_pole_gate():
    """
    Embed the variable-profile transfer into the reduced complex pole condition.

    This is stronger than the real-frequency transfer test in p05b: it forms
    the two-channel determinant and solves it in the lower half-plane.  Its
    scope is still reduced because the exterior barrier is the p05b Jost
    reflection model and rotation is not included.
    """
    profile_gate = run_variable_profile_matrix_radial_system_gate()
    branch_scan = compute_branch_corrected_reduced_root_scan_gate()
    ell_value = branch_scan["ell"]
    q_value = branch_scan["q"]
    branch_by_name = {row["branch"]: row for row in branch_scan["branches"]}
    branches = {
        "minus": branch_by_name["minus"],
        "plus": branch_by_name["plus_transverse"],
    }
    branch_times = {
        "minus": branches["minus"]["T_branch_over_rs_c"],
        "plus": branches["plus"]["T_branch_over_rs_c"],
    }

    x_out = 80.0
    jost_steps = 5000
    profile_steps = 1800

    rows = []
    eps0_checks = []
    for branch_name, branch_data in branches.items():
        old_root = branch_data["fine_root"]
        initial = complex(old_root["Omega_real"], old_root["Omega_imag"])
        eps0_eval = _matrix_pole_determinant(
            initial,
            0.0,
            branch_times,
            ell_value,
            q_value,
            x_out,
            jost_steps,
            profile_steps,
        )
        eps0_checks.append({
            "branch": branch_name,
            "Omega_real": initial.real,
            "Omega_imag": initial.imag,
            "determinant_abs": abs(eps0_eval["determinant"]),
            "core_offdiag_abs": _max_offdiag_abs2(eps0_eval["core_reflection_matrix"]),
        })

        root = _newton_complex_determinant_root(
            initial,
            1.0,
            branch_times,
            ell_value,
            q_value,
            x_out,
            jost_steps,
            profile_steps,
        )
        root["branch_seed"] = branch_name
        root["initial_Omega_real"] = initial.real
        root["initial_Omega_imag"] = initial.imag
        root["root_shift_abs"] = abs(
            complex(root["Omega_real"], root["Omega_imag"]) - initial
        )
        rows.append(root)

    max_eps0_det = max(row["determinant_abs"] for row in eps0_checks)
    max_eps0_offdiag = max(row["core_offdiag_abs"] for row in eps0_checks)
    max_eps1_det = max(row["determinant_abs"] for row in rows)
    max_eps1_offdiag = max(row["roundtrip_offdiag_abs"] for row in rows)
    roots_lower_half = all(row["Omega_imag"] <= 1.0e-12 for row in rows)
    roots_converged = all(row["converged"] for row in rows)

    return {
        "variable_profile_matrix_pole_status": (
            "PASS_VARIABLE_PROFILE_MATRIX_COMPLEX_POLE_GATE"
            if profile_gate["variable_profile_matrix_status"]
            == "PASS_VARIABLE_PROFILE_MATRIX_RADIAL_TRANSFER"
            and branch_scan["branch_corrected_scan_status"]
            == "PASS_BRANCH_CORRECTED_REDUCED_ROOT_SCAN_LOWER_HALF_PLANE"
            and max_eps0_det < 5.0e-5
            and max_eps0_offdiag < 1.0e-8
            and roots_converged
            and roots_lower_half
            and max_eps1_det < 1.0e-8
            and max_eps1_offdiag > 1.0e-6
            else "CHECK_VARIABLE_PROFILE_MATRIX_COMPLEX_POLE_GATE"
        ),
        "scope": (
            "two-channel reduced complex pole determinant with variable-profile "
            "core transfer and diagonal exterior photon-barrier reflection; "
            "rotation and full asymptotic tail improvement remain separate gates"
        ),
        "ell": ell_value,
        "q": q_value,
        "eps0_constant_limit_checks": eps0_checks,
        "eps1_variable_profile_roots": rows,
        "max_eps0_determinant_abs": max_eps0_det,
        "max_eps0_core_offdiag_abs": max_eps0_offdiag,
        "max_eps1_determinant_abs": max_eps1_det,
        "max_eps1_roundtrip_offdiag_abs": max_eps1_offdiag,
        "x_out": x_out,
        "jost_steps": jost_steps,
        "profile_steps": profile_steps,
        "reading": (
            "the admissible variable profile is now inside the complex pole "
            "determinant.  The eps=0 limit collapses back to the p05b branch "
            "roots, while eps=1 keeps the two roots in the lower half-plane and "
            "activates a nonzero channel-mixing round trip."
        ),
        "next_gate": (
            "continue in p05d_rotating_rays.py: static ray baseline and "
            "first-order rotating compact edge"
        ),
    }


def p05c_central_qnm_gate(pole_gate=None):
    if pole_gate is None:
        pole_gate = compute_variable_profile_matrix_pole_gate()
    return {
        "p05c_status": (
            "PASS_P05C_VARIABLE_PROFILE_COMPLEX_QNM_LAYER"
            if pole_gate["variable_profile_matrix_pole_status"]
            == "PASS_VARIABLE_PROFILE_MATRIX_COMPLEX_POLE_GATE"
            else "CHECK_P05C_VARIABLE_PROFILE_COMPLEX_QNM_LAYER"
        ),
        "variable_profile_matrix_pole": pole_gate[
            "variable_profile_matrix_pole_status"
        ],
        "eps1_roots": pole_gate["eps1_variable_profile_roots"],
        "max_eps1_determinant_abs": pole_gate["max_eps1_determinant_abs"],
        "max_eps1_roundtrip_offdiag_abs": pole_gate[
            "max_eps1_roundtrip_offdiag_abs"
        ],
        "next_gates": [
            (
                "p05d_rotating_rays.py adds the static ray baseline and "
                "first-order rotating compact edge"
            ),
        ],
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 18c: Variable-profile matrix QNM pole gate")
    print("=" * 72)

    pole_gate_result = compute_variable_profile_matrix_pole_gate()
    sections = [
        ("1. Variable-profile matrix pole", pole_gate_result),
        ("2. Central p05c gate", p05c_central_qnm_gate(pole_gate_result)),
    ]
    for title, result in sections:
        print(f"\n{title}")
        for key, value in result.items():
            print(f"  {key:36s}: {value}")
