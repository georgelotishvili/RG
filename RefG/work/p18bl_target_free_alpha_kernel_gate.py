from __future__ import annotations

import hashlib
import inspect
import math
from dataclasses import asdict, dataclass, fields

import sympy as sp

from p11b_c3_triplet_inversion import (
    LEPTON_MASSES_MEV,
    LEPTON_MASS_UNCERTAINTY_MEV,
    PDG_MASS_SOURCE,
)
from p18bh_boundary_slot_count_theorem_gate import (
    boundary_rank_nullity_theorem,
)
from p18bj_hidden_slot_variational_readout_gate import hidden_density_readout


C3_ORDER = 3
H_BRANCH = 2
ORDER_NINE = 9
QED_B1_PER_LEPTON = 2.0 / (3.0 * math.pi)
QED_B1_THREE_LEPTONS = 2.0 / math.pi


@dataclass(frozen=True)
class SheetNormalization:
    h_branch: int
    diagonal_sheet_count: int
    order_nine: int
    q_geom: float
    unit_sheet_ratio: float
    q0_squared: float
    bare_inverse_alpha: float
    formula: str
    sheet_count_identified_with_h: bool
    derived_from_current_p01_action: bool


@dataclass(frozen=True)
class PredictionRecord:
    branch: str
    h_branch: int
    hidden_dimension: int
    tau_over_e: float
    muon_over_e: float
    bare_inverse_alpha: float
    internal_inverse_alpha: float
    inverse_alpha: float
    alpha: float
    boundary_readout: float
    equation_residual: float
    mass_input_sigma_inverse_alpha: float | None
    theory_systematic_sigma: float | None
    mass_source: str
    covariance_assumption: str


def diagonal_sheet_normalization(
    h: int = H_BRANCH,
    order: int = ORDER_NINE,
    sheet_count: int | None = None,
    unit_sheet_ratio: float = 1.0,
) -> SheetNormalization:
    """Reduce h identical gauge sheets to the diagonal photon.

    For one sheet write K_* for the Maxwell stiffness and k_* for the source
    coefficient, and define eta_*=k_*^2/K_*.  Coherent diagonal reduction of
    n identical sheets gives

        q0^2 = n eta_*,
        q_geom = h/9,
        alpha_bare^-1 = 4 pi / (q0^2 q_geom^2).

    The working candidate makes the two additional identifications n=h and
    eta_*=1, producing 324 pi/h^3.  Neither identification follows from the
    present p01 action.  In particular, n cannot be justified merely by the
    two photon helicities: they are polarizations of one canonical U(1), not
    automatically two additive Maxwell sheets.
    """

    if sheet_count is None:
        sheet_count = h
    if h <= 0 or order <= 0 or sheet_count <= 0 or unit_sheet_ratio <= 0.0:
        raise ValueError(
            "h, order, sheet_count and unit_sheet_ratio must be positive"
        )
    q_geom = h / order
    q0_squared = sheet_count * unit_sheet_ratio
    bare_inverse = 4.0 * math.pi / (q0_squared * q_geom**2)
    return SheetNormalization(
        h_branch=h,
        diagonal_sheet_count=sheet_count,
        order_nine=order,
        q_geom=q_geom,
        unit_sheet_ratio=unit_sheet_ratio,
        q0_squared=q0_squared,
        bare_inverse_alpha=bare_inverse,
        formula="alpha_bare^-1=4*pi*9^2/(n*eta_* h^2); working candidate n=h",
        sheet_count_identified_with_h=sheet_count == h,
        derived_from_current_p01_action=False,
    )


def exact_c3_mass_ratios() -> tuple[float, float]:
    amplitude = math.sqrt(2.0)
    theta = 2.0 / 9.0
    tau, electron, muon = (
        1.0 + amplitude * math.cos(theta + 2.0 * math.pi * k / 3.0)
        for k in range(3)
    )
    return (tau / electron) ** 2, (muon / electron) ** 2


def internal_inverse_alpha(
    tau_over_e: float,
    muon_over_e: float,
    normalization: SheetNormalization,
) -> float:
    if tau_over_e <= 0.0 or muon_over_e <= 0.0:
        raise ValueError("mass ratios must be positive")
    h = normalization.h_branch
    log_argument = ((C3_ORDER * h) ** 2) ** 3 * tau_over_e**5 / muon_over_e
    return normalization.bare_inverse_alpha + QED_B1_PER_LEPTON * math.log(
        log_argument
    )


def solve_boundary_relation(Y: float, hidden_dimension: int) -> float:
    """Solve y=Y-(2/pi)/(N y) on the large positive branch."""

    if Y <= 0.0 or hidden_dimension <= 0:
        raise ValueError("Y and hidden_dimension must be positive")
    discriminant = Y**2 - 4.0 * QED_B1_THREE_LEPTONS / hidden_dimension
    if discriminant <= 0.0:
        raise ValueError("the large positive branch does not exist")
    return (Y + math.sqrt(discriminant)) / 2.0


def _prediction_from_ratios(
    branch: str,
    tau_over_e: float,
    muon_over_e: float,
    mass_sigma: float | None,
    mass_source: str,
    unit_sheet_ratio: float = 1.0,
) -> PredictionRecord:
    normalization = diagonal_sheet_normalization(
        unit_sheet_ratio=unit_sheet_ratio
    )
    boundary = boundary_rank_nullity_theorem()
    N = boundary.kernel_dimension
    Y = internal_inverse_alpha(tau_over_e, muon_over_e, normalization)
    y = solve_boundary_relation(Y, N)
    alpha = 1.0 / y
    readout = hidden_density_readout(alpha)
    residual = y - Y + QED_B1_THREE_LEPTONS * readout.normalized_interface_readout

    return PredictionRecord(
        branch=branch,
        h_branch=normalization.h_branch,
        hidden_dimension=N,
        tau_over_e=tau_over_e,
        muon_over_e=muon_over_e,
        bare_inverse_alpha=normalization.bare_inverse_alpha,
        internal_inverse_alpha=Y,
        inverse_alpha=y,
        alpha=alpha,
        boundary_readout=readout.normalized_interface_readout,
        equation_residual=residual,
        mass_input_sigma_inverse_alpha=mass_sigma,
        theory_systematic_sigma=None,
        mass_source=mass_source,
        covariance_assumption="diagonal covariance; listed pole-mass inputs treated as independent",
    )


def predict_exact_c3_branch(
    unit_sheet_ratio: float = 1.0,
) -> PredictionRecord:
    tau_over_e, muon_over_e = exact_c3_mass_ratios()
    return _prediction_from_ratios(
        branch="exact_C3_ratios",
        tau_over_e=tau_over_e,
        muon_over_e=muon_over_e,
        mass_sigma=None,
        mass_source="exact candidate A=sqrt(2), theta=2/9; no measured mass input",
        unit_sheet_ratio=unit_sheet_ratio,
    )


def _dy_dY(Y: float, hidden_dimension: int) -> float:
    discriminant = Y**2 - 4.0 * QED_B1_THREE_LEPTONS / hidden_dimension
    return 0.5 * (1.0 + Y / math.sqrt(discriminant))


def empirical_mass_jacobian(
    unit_sheet_ratio: float = 1.0,
) -> dict[str, float]:
    masses = LEPTON_MASSES_MEV
    normalization = diagonal_sheet_normalization(
        unit_sheet_ratio=unit_sheet_ratio
    )
    tau_over_e = masses["tau"] / masses["electron"]
    muon_over_e = masses["muon"] / masses["electron"]
    Y = internal_inverse_alpha(tau_over_e, muon_over_e, normalization)
    N = boundary_rank_nullity_theorem().kernel_dimension
    prefactor = _dy_dY(Y, N) * QED_B1_PER_LEPTON
    log_mass_coefficients = {"electron": -4.0, "muon": -1.0, "tau": 5.0}
    return {
        name: prefactor * log_mass_coefficients[name] / masses[name]
        for name in ("electron", "muon", "tau")
    }


def propagate_empirical_mass_sigma(
    unit_sheet_ratio: float = 1.0,
) -> tuple[float, dict[str, float]]:
    jacobian = empirical_mass_jacobian(unit_sheet_ratio)
    contributions = {
        name: jacobian[name] * LEPTON_MASS_UNCERTAINTY_MEV[name]
        for name in jacobian
    }
    sigma = math.sqrt(sum(value**2 for value in contributions.values()))
    return sigma, contributions


def predict_empirical_mass_branch(
    unit_sheet_ratio: float = 1.0,
) -> PredictionRecord:
    masses = LEPTON_MASSES_MEV
    sigma, _ = propagate_empirical_mass_sigma(unit_sheet_ratio)
    source = (
        f"{PDG_MASS_SOURCE['edition']}; nodes "
        f"{PDG_MASS_SOURCE['electron_node']}, "
        f"{PDG_MASS_SOURCE['muon_node']}, "
        f"{PDG_MASS_SOURCE['tau_node']}"
    )
    return _prediction_from_ratios(
        branch="empirical_pole_mass_ratios",
        tau_over_e=masses["tau"] / masses["electron"],
        muon_over_e=masses["muon"] / masses["electron"],
        mass_sigma=sigma,
        mass_source=source,
        unit_sheet_ratio=unit_sheet_ratio,
    )


def finite_difference_mass_jacobian() -> dict[str, float]:
    masses = dict(LEPTON_MASSES_MEV)

    def evaluate(local: dict[str, float]) -> float:
        normalization = diagonal_sheet_normalization()
        Y = internal_inverse_alpha(
            local["tau"] / local["electron"],
            local["muon"] / local["electron"],
            normalization,
        )
        return solve_boundary_relation(
            Y, boundary_rank_nullity_theorem().kernel_dimension
        )

    result: dict[str, float] = {}
    for name, mass in masses.items():
        step = max(abs(mass) * 1.0e-6, 1.0e-10)
        plus = dict(masses)
        minus = dict(masses)
        plus[name] += step
        minus[name] -= step
        result[name] = (evaluate(plus) - evaluate(minus)) / (2.0 * step)
    return result


def prediction_digest(record: PredictionRecord) -> str:
    payload = repr(tuple(sorted(asdict(record).items()))).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def derivation_hypotheses() -> tuple[str, ...]:
    return (
        "The charged branch is the oriented h=2 branch with q_geom=h/9.",
        "The number n of genuinely additive locked gauge sheets equals the return index h; photon helicity counting alone does not prove n=h.",
        "The unit-sheet ratio eta_*=k_*^2/K_* equals one; current p01 does not derive this normalization.",
        "The core matching scale obeys mu_core=(3h)^2 m_tau^2/m_e.",
        "The matching register is the lepton-only one-loop threshold chain with coefficients 3,2,1.",
        "The boundary response space and photon map are those of the conditional p18bh Herm(V) theorem.",
        "The hidden kernel is U(34)-isotropic and the two-helicity interface has unit normalization as in p18bj.",
    )


def normalization_identifiability_audit() -> dict[str, object]:
    """Prove that current symmetry/topology data do not fix eta_* or n=h."""

    a, b, kappa = sp.symbols("a b kappa", positive=True)
    K = a * sp.eye(2) + b * sp.ones(2)
    source = kappa * sp.ones(2, 1)
    q0_squared_exchange = sp.simplify((source.T * K.inv() * source)[0])

    k0, k1, kJ = sp.symbols("kappa_0 kappa_1 k_J", positive=True)
    h = sp.Integer(H_BRANCH)
    order = sp.Integer(ORDER_NINE)
    lambda_h = sp.simplify(k0 + 4 * k1 * sp.sin(sp.pi * h / order) ** 2)
    q0_squared_circulant = sp.simplify(kJ**2 / lambda_h)

    # For C=m/2, C*(2/9)=m/9 is integral first at m=9.  If C itself is
    # restricted to integers, 2C/9 is integral first at C=9.
    spinorial_C = sp.Rational(9, 2)
    spinorial_cap_integer = sp.simplify(spinorial_C * sp.Rational(2, 9))
    integer_C = sp.Integer(9)
    integer_cap_integer = sp.simplify(integer_C * sp.Rational(2, 9))

    return {
        "level_action": (
            "q0^2=n*eta_*, alpha_bare^-1=4*pi*9^2/(n*eta_* h^2)"
        ),
        "working_identifications": ("n=h", "eta_*=1"),
        "exchange_symmetric_q0_squared": str(q0_squared_exchange),
        "exchange_symmetry_leaves_continuous_parameters": bool(
            q0_squared_exchange.has(a, b, kappa)
        ),
        "z9_mode_stiffness": str(lambda_h),
        "z9_q0_squared": str(q0_squared_circulant),
        "z9_symmetry_leaves_continuous_parameters": bool(
            q0_squared_circulant.has(k0, k1, kJ)
        ),
        "sphere_prequantization_condition": "(1/(2*pi))*integral_S2 Omega_B=2C is an integer",
        "cap_is_not_a_closed_two_cycle": True,
        "minimal_spinorial_C_if_extra_cap_rule_imposed": str(spinorial_C),
        "spinorial_cap_integer": int(spinorial_cap_integer),
        "minimal_integer_C_if_extra_cap_rule_imposed": int(integer_C),
        "integer_cap_integer": int(integer_cap_integer),
        "two_photon_helicities_do_not_supply_two_Coulomb_charge_units": True,
        "oriented_return_index_is_not_yet_an_action_level": True,
        "target_value_used": False,
    }


def source_firewall() -> dict[str, object]:
    source = inspect.getsource(inspect.getmodule(source_firewall))
    forbidden = (
        "COD" + "ATA",
        "OBS" + "ERVED",
        "137.03" + "5999177",
        "best_" + "integer",
        "required_" + "from_alpha",
    )
    violations = tuple(token for token in forbidden if token in source)
    forbidden_fields = (
        "observed",
        "miss",
        "ppm",
        "z_score",
    )
    record_fields = tuple(field.name for field in fields(PredictionRecord))
    field_violations = tuple(
        name
        for name in record_fields
        if any(token in name.lower() for token in forbidden_fields)
    )
    return {
        "source_violations": violations,
        "prediction_field_violations": field_violations,
        "runtime_target_free": not violations and not field_violations,
        "historically_target_exposed": True,
        "independent_validation_completed": False,
    }


def run_gate() -> None:
    normalization = diagonal_sheet_normalization()
    exact = predict_exact_c3_branch()
    empirical = predict_empirical_mass_branch()
    analytic = empirical_mass_jacobian()
    finite = finite_difference_mass_jacobian()
    sigma, contributions = propagate_empirical_mass_sigma()
    firewall = source_firewall()
    identifiability = normalization_identifiability_audit()

    assert normalization.h_branch == 2
    assert normalization.diagonal_sheet_count == 2
    assert normalization.sheet_count_identified_with_h is True
    assert normalization.q0_squared == 2.0
    assert math.isclose(
        normalization.bare_inverse_alpha,
        81.0 * math.pi / 2.0,
        rel_tol=1.0e-15,
    )
    assert normalization.derived_from_current_p01_action is False
    assert exact.hidden_dimension == 34
    assert empirical.hidden_dimension == 34
    assert abs(exact.equation_residual) < 1.0e-14
    assert abs(empirical.equation_residual) < 1.0e-14
    assert exact.inverse_alpha != empirical.inverse_alpha
    assert sigma > 0.0
    assert contributions["tau"] > 0.0
    for name in analytic:
        assert math.isclose(analytic[name], finite[name], rel_tol=2.0e-5)
    assert prediction_digest(exact) == prediction_digest(
        predict_exact_c3_branch()
    )
    assert firewall["runtime_target_free"] is True
    assert firewall["historically_target_exposed"] is True
    assert firewall["independent_validation_completed"] is False
    assert identifiability["exchange_symmetry_leaves_continuous_parameters"]
    assert identifiability["z9_symmetry_leaves_continuous_parameters"]
    assert identifiability["spinorial_cap_integer"] == 1
    assert identifiability["integer_cap_integer"] == 2
    assert identifiability["target_value_used"] is False

    print("p18bl target-free conditional alpha kernel gate")
    print("sheet normalization")
    print(normalization)
    print()
    print("exact-C3 prediction record")
    print(exact)
    print()
    print("empirical-mass prediction record")
    print(empirical)
    print()
    print("mass uncertainty")
    print({"sigma_inverse_alpha": sigma, "contributions": contributions})
    print()
    print("source firewall")
    print(firewall)
    print()
    print("normalization identifiability audit")
    print(identifiability)
    print()
    print("derivation hypotheses")
    for item in derivation_hypotheses():
        print(f"- {item}")
    print()
    print(
        "STATUS: OPEN_ACTION_NORMALIZATION_THRESHOLD_AND_INTERFACE_DERIVATION__"
        "PASS_TARGET_FREE_CONDITIONAL_ALPHA_KERNEL"
    )


if __name__ == "__main__":
    run_gate()
