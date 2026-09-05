#!/usr/bin/env python3
"""No-write checks of W3-75 identities; the general theorem is proved in its contract."""

from __future__ import annotations

import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path

sys.dont_write_bytecode = True
import sympy as sp

HERE = Path(__file__).resolve().parent
WORK3 = HERE.parent.parent
CONTRACT = HERE / "w3_75_dynamical_relaxation_response_contract.md"
MODEL_VERSION = "W3-75-v1.0"
CONTRACT_HASH = "31a1e6bd28b6698e64b790fd4692aba6616af5613c3919f322a790c7296d9f4a"
PINS = {
    "Cosmology_and_LSS/Active_Participation_Resonance_Feedback/w3_47_post_genesis_evolution_pressure_coupling_kernel_preregistration.md": "9b603b1df55edf994f1e528a6cc8e16b69c474dd4c1b3df815e2654a6c279d50",
    "Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md": "6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879",
    "Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/w3_58_one_oscillon_coframe_localized_core_preregistration.md": "ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db",
    "Cosmology_and_LSS/CMB_Closure/w3_62_cmb_einstein_source_linear_closure_preregistration.md": "b4068791b63e9a072a897e9aa85eae96c588b0d33533effb9664ffbd667ae810",
    "Strong_Field/W3-71_Horizon_Material_Scale_Separation/w3_71_horizon_material_scale_separation_preregistration.md": "1d3f74489f6cc52061253b6e1ea3d7f96e5d423f8b2afb88e79a44a38ae916c3",
}
FALSE_FLAGS = (
    "microscopic_pressure_map_derived", "resonance_amplitude_map_derived",
    "direct_oscillon_collective_transfer_derived", "singularity_resolution",
    "observational_pass", "intuitive_files_changed",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "MISSING"


def clean(value):
    return sp.simplify(value)


@lru_cache(maxsize=None)
def polytrope(w, exponent):
    """Check the proposed history against continuity and Friedmann independently."""
    t = sp.symbols("Delta_tau", nonnegative=True)
    ni, hi, k, M = sp.symbols("n_i H_i kappa M", positive=True)
    n = sp.symbols("n", positive=True)
    u = 1 + sp.Rational(3, 2) * (1 + w) * hi * t
    x, h = u**exponent, hi / u
    rho = M * n**(1 + w)
    p, pf = x**sp.Rational(1, 5), x**sp.Rational(2, 5)
    return {
        "continuity": clean(sp.diff(ni * x, t) + 3 * h * ni * x),
        "friedmann": clean(3 * h**2 - k * rho.subs(n, ni * x).subs(M, 3 * hi**2 / (k * ni**(1 + w)))),
        "scale_rate": clean(sp.diff(p, t) + sp.Rational(3, 5) * h * p),
        "pressure_rate": clean(sp.diff(pf, t) + sp.Rational(6, 5) * h * pf),
        "sound_speed": clean(n * sp.diff(rho, n, 2) / sp.diff(rho, n) - w),
    }


def build_report():
    n, n0, k, P0, z = sp.symbols("n n_0 kappa P_0 p_symbol", positive=True)
    B, R, lam = sp.symbols("B R Lambda", nonnegative=True)
    rho = sp.Function("rho_C")(n)
    x = n / n0
    E = rho + B * x + R * x**sp.Rational(4, 3)
    H = sp.sqrt((k * E + lam) / 3)
    nd = -3 * H * n
    hd = -k * n * sp.diff(E, n) / 2
    p, PF = x**sp.Rational(1, 5), P0 * x**sp.Rational(2, 5)
    ap, af = sp.Rational(3, 5), sp.Rational(6, 5)
    dpd, dfd = ap * p * (hd - ap * H**2), af * PF * (hd - af * H**2)

    # Explicit Euler--Lagrange and Ward identities of the additive actions.
    A, h, chi = sp.symbols("A h chi", positive=True)
    v, acc, qo, qod, qc, nn = sp.symbols("chi_dot chi_ddot thetaO_dot thetaO_ddot thetaC_dot n_dot", real=True)
    thetaC, thetaO = sp.symbols("theta_C theta_O", real=True)
    m, ell, g = sp.symbols("m lambda_scalar g", positive=True)
    V = m**2 * chi**2 / 2 - ell * chi**4 / 4 + g * chi**6 / 6
    L = A**3 * (n * qc - rho + v**2 / 2 + chi**2 * qo**2 / 2 - V)
    rates = {A: h * A, n: nn, chi: v, v: acc, qo: qod, thetaC: qc, thetaO: qo}

    def dt(expr):
        return sum(sp.diff(expr, symbol) * rate for symbol, rate in rates.items())

    wardC = clean((dt(sp.diff(L, qc)) - sp.diff(L, thetaC)) / A**3)
    wardO = clean((dt(sp.diff(L, qo)) - sp.diff(L, thetaO)) / A**3)
    elChi = clean((dt(sp.diff(L, v)) - sp.diff(L, chi)) / A**3)
    PC = n * sp.diff(rho, n) - rho
    rhoO, PO = v**2 / 2 + chi**2 * qo**2 / 2 + V, v**2 / 2 + chi**2 * qo**2 / 2 - V
    balC = dt(rho) + 3 * h * (rho + PC)
    balO = dt(rhoO) + 3 * h * (rhoO + PO)
    onC = {nn: -3 * h * n}
    onO = {acc: chi * qo**2 - sp.diff(V, chi) - 3 * h * v, qod: -(3 * h + 2 * v / chi) * qo}
    base = {
        "phase_current_variation": wardC - (nn + 3 * h * n),
        "ordinary_phase_current_variation": wardO - (chi**2 * qod + 2 * chi * v * qo + 3 * h * chi**2 * qo),
        "collective_chemical_equation": sp.diff(L, n) / A**3 - (qc - sp.diff(rho, n)),
        "ordinary_amplitude_equation": elChi - (acc + 3 * h * v - chi * qo**2 + sp.diff(V, chi)),
        "collective_energy_Ward_identity": balC - sp.diff(rho, n) * wardC,
        "ordinary_energy_Ward_identity": balO - v * elChi - qo * wardO,
        "p_current_chain_rule": sp.diff(p, n) * nd + ap * H * p,
        "pressure_current_chain_rule": sp.diff(PF, n) * nd + af * H * PF,
        "Hilbert_enthalpy": n * sp.diff(E, n) - (n * sp.diff(rho, n) + B * x + sp.Rational(4, 3) * R * x**sp.Rational(4, 3)),
        "operational_scale": clean(p**sp.Rational(-5, 3) - x**sp.Rational(-1, 3)),
        "W47_eta_rate_overlap": sp.diff(p**2, n) * nd + af * H * p**2,
        "dust_pressure_distinct_from_P_F": PC.subs(rho, m * n).doit(),
    }
    ws = (sp.Integer(0), sp.Rational(1, 3), sp.Integer(1))
    canonical = {"n_ratio": z**5, "ndot": nd, "Hdot": hd, "Dp_dot": dpd, "DF_dot": dfd,
                 "powers": tuple(-2 / (1 + w) for w in ws), "Q_C": sp.Integer(0), "Q_O": sp.Integer(0), "interaction": sp.Integer(0)}

    def validate(candidate):
        """Canonical and perturbed candidates go through these same physical identities."""
        lag = L / A**3 - candidate["interaction"]
        Dp = -sp.diff(p, n) * candidate["ndot"]
        DF = -sp.diff(PF, n) * candidate["ndot"]
        residuals = dict(base)
        residuals.update({
            "density_volume_map": candidate["n_ratio"] - z**3 * z**2,
            "current_conservation": candidate["ndot"] + 3 * H * n,
            "Friedmann_Raychaudhuri": candidate["Hdot"] - sp.diff(H, n) * candidate["ndot"],
            "material_loss_chain_rule": candidate["Dp_dot"] - sp.diff(Dp, n) * candidate["ndot"],
            "pressure_loss_chain_rule": candidate["DF_dot"] - sp.diff(DF, n) * candidate["ndot"],
            "collective_separate_energy_balance": balC.subs(onC) - candidate["Q_C"],
            "ordinary_separate_energy_balance": balO.subs(onO) - candidate["Q_O"],
            "exchange_sum": candidate["Q_C"] + candidate["Q_O"],
            "direct_n_chi_response": sp.diff(lag, n, chi),
            "direct_n_ordinary_phase_response": sp.diff(lag, n, thetaO),
            "direct_n_ordinary_phase_rate_response": sp.diff(lag, n, qo),
        })
        for w, power in zip(ws, candidate["powers"]):
            residuals.update({f"polytrope_w={w}_{name}": value for name, value in polytrope(w, power).items()})
        return {name: clean(value) for name, value in residuals.items()}

    exact = validate(canonical)
    identity_checks = {name: value == 0 for name, value in exact.items()}
    eps = sp.symbols("epsilon", positive=True)
    mutations = {
        "old_foundation_density_exponent": {"n_ratio": z**2},
        "reversed_current": {"ndot": -nd},
        "wrong_Raychaudhuri_coefficient": {"Hdot": 2 * hd},
        "wrong_loss_rate_coefficient": {"DF_dot": dfd / 2},
        "extra_pressure_factor": {"Dp_dot": dpd * p},
        "wrong_polytropic_power": {"powers": (-sp.Integer(1), canonical["powers"][1], canonical["powers"][2])},
        "noncancelling_internal_exchange": {"Q_C": eps, "Q_O": eps},
        "cancelling_but_unintroduced_direct_exchange": {"Q_C": eps, "Q_O": -eps},
        "added_n_chi_squared_interaction": {"interaction": eps * n * chi**2},
    }
    mutation_results = {}
    for name, changes in mutations.items():
        residuals = validate({**canonical, **changes})
        failed = {key: sp.sstr(value) for key, value in residuals.items() if value != 0}
        mutation_results[name] = {"detected": bool(failed), "nonzero_production_residuals": failed}

    # Signs use the declared positive rho and mu, not assumptions hidden in flags.
    rpos, mu = sp.symbols("rho_positive mu_positive", positive=True)
    eh = n * mu + B * x + sp.Rational(4, 3) * R * x**sp.Rational(4, 3)
    hh = sp.sqrt((k * (rpos + B * x + R * x**sp.Rational(4, 3)) + lam) / 3)
    hhd = -k * eh / 2
    sign_expressions = {"source_positive": hh**2, "enthalpy_positive": eh,
                        "Hdot_negative": -hhd, "material_loss_positive": ap * hh * p,
                        "pressure_loss_positive": af * hh * PF,
                        "material_loss_decreasing": -ap * p * (hhd - ap * hh**2),
                        "pressure_loss_decreasing": -af * PF * (hhd - af * hh**2)}
    sign_checks = {name: expr.is_positive is True for name, expr in sign_expressions.items()}

    t, delta = sp.symbols("Delta_tau delta_H", nonnegative=True)
    hi, hs, s = sp.symbols("H_i H_s s", positive=True)
    bounds = {"density": (n0, sp.Integer(3)), "material": (sp.Integer(1), ap), "pressure": (P0, af)}
    bound_residuals = {}
    for name, (initial, rate) in bounds.items():
        bound = initial * sp.exp(-rate * hi * t)
        bound_residuals[name] = clean(sp.diff(bound, t) + rate * hi * bound)
    log_bound = sp.log(n0 / n) / (3 * hi)
    integral_residual = clean(sp.integrate(1 / (3 * s * hi), (s, n, n0)) - log_bound)
    comparison = clean(1 / (3 * n * hs) - 1 / (3 * n * (hs + delta)))
    endpoint_checks = {"exponential_bounds_exact": all(v == 0 for v in bound_residuals.values()),
                       "integrated_log_bound_exact": integral_residual == 0,
                       "integrand_comparison_nonnegative": comparison.is_nonnegative is True,
                       "log_bound_diverges": sp.limit(log_bound, n, 0, dir="+") == sp.oo}
    amplitude_checks = {"two_distinct_normalized_readouts": bool(clean(p - p**2) != 0 and p.subs(n, n0) == 1 and (p**2).subs(n, n0) == 1),
                        "no_resonance_amplitude_in_action_or_H": "c_lock" not in str(L) + str(H)}

    dependencies = {path: {"expected": expected, "actual": digest(WORK3 / path)} for path, expected in PINS.items()}
    dependency_checks = {path: entry["actual"] == entry["expected"] for path, entry in dependencies.items()}
    dependency_checks["own_contract"] = digest(CONTRACT) == CONTRACT_HASH
    flags = {"variational_and_background_identities_exact": all(identity_checks.values()),
             "source_domain_signs_verified": all(sign_checks.values()),
             "finite_time_and_endpoint_comparison_algebra_exact": all(endpoint_checks.values()),
             "resonance_readout_nonselection_witness": all(amplitude_checks.values()),
             "production_mutation_controls_pass": all(v["detected"] for v in mutation_results.values()),
             "dependency_hashes_exact": all(dependency_checks.values())}
    flags.update({name: False for name in FALSE_FLAGS})
    passed = all(flags[name] for name in flags if name not in FALSE_FLAGS) and all(not flags[name] for name in FALSE_FLAGS)
    return {"claim_id": "W3_75_DYNAMICAL_HOMOGENEOUS_RELAXATION_RESPONSE", "model_version": MODEL_VERSION,
            "decision_status": "PASS_CONDITIONAL_DYNAMICAL_RELAXATION__DIRECT_RESONANCE_RESPONSE_OPEN" if passed else "FAIL_W3_75",
            "aggregate_pass": passed, "closure_flags": flags,
            "residuals": {name: sp.sstr(value) for name, value in exact.items()}, "identity_checks": identity_checks,
            "source_domain_sign_checks": sign_checks, "endpoint_checks": endpoint_checks,
            "endpoint_comparison": sp.sstr(comparison), "amplitude_checks": amplitude_checks,
            "negative_controls": mutation_results, "dependencies": dependencies, "dependency_checks": dependency_checks,
            "proof_scope": "The general future-time theorem uses the analytic proof and regular positive source domain in contract sections 2-3. These symbolic identities, signs, comparison and exact benchmarks check its algebra; flags or finite samples alone are not an existence proof. No inhomogeneous or singularity conclusion follows.",
            "provenance": {"contract_sha256": digest(CONTRACT), "source_sha256": digest(Path(__file__)), "python": sys.version.split()[0], "sympy": sp.__version__},
            "writes_files": False, "data_role": "NO_DATA_READ_OR_FITTED"}


def main():
    try:
        report = build_report()
    except Exception as exc:
        report = {"model_version": MODEL_VERSION, "aggregate_pass": False, "decision_status": "FAIL_W3_75",
                  "error": f"{type(exc).__name__}: {exc}", "writes_files": False}
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["aggregate_pass"] else 1)


if __name__ == "__main__":
    main()
