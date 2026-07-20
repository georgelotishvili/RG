# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Active coefficient scheme: observational scaling ledger; no new action terms.

"""
PHASE 15: Medium response scaling gate.

This file is deliberately broader than the CQG article.  It records the
theory-axis question raised by the user:

    pressure/occupancy deficit -> volume/mass response,
    pressure/occupancy deficit -> length response,
    pressure/occupancy deficit -> clock/process-rate response,

while preserving the observational guardrails:

  * local c and local dimensionless ratios are invariant;
  * metric time dilation must reproduce the gravitational lapse;
  * Solar light deflection/Shapiro data require the spatial and temporal
    weak-field metric responses to have the same first-order strength
    (PPN gamma=1);
  * a compact object's far gravitational mass cannot be read as only the
    filtered external active core channel if the object is to become more
    compact; the remaining external charge must be in the deficit/dressing
    ledger and counted once.

Important distinction:
  - A gas/thermos free-molecular analogy may scale an intrinsic transfer rate
    with the amount of active carrier.
  - That does not automatically make the same factor the metric lapse.  The
    process-rate channel and the metric lapse are separate unless a
    stress/lapse/substrate bridge derives their equality.
"""

from __future__ import annotations

import sympy as sp


def derive_scaling_identities() -> dict[str, object]:
    """
    General power-law response to one active-volume/tension factor v.

    v is the active volume/occupancy/tension-state factor, normalized so that
    v=1 is the local reference state and 0<v<=1 is a deficit.

        M_active_readout/M0 = v^m
        L_oper/L0 = v^ell
        d tau/dt = v^tau

    The optical index splits into temporal and spatial halves:

        n_t = 1/(d tau/dt),     n_s = 1/(L_oper/L0).

    In the weak field q_v=-log(v), the PPN gamma analogue is ell/tau when the
    same response is used as a metric branch.  Solar gamma=1 therefore requires
    ell=tau for a metric lapse/spatial response.
    """
    v, m, ell, tau = sp.symbols("v m ell tau", positive=True, real=True)
    M0, R0, c = sp.symbols("M0 R0 c", positive=True, real=True)

    mass_readout = v**m
    length = v**ell
    lapse = v**tau
    period = sp.simplify(1 / lapse)
    temporal_index = sp.simplify(1 / lapse)
    spatial_index = sp.simplify(1 / length)
    optical_index = sp.simplify(temporal_index * spatial_index)
    coordinate_light_speed = sp.simplify(c / optical_index)

    # Local measurement uses the same local length and time standards, so c is
    # unchanged when the coordinate light speed is read with those standards.
    local_c_ratio = sp.simplify((coordinate_light_speed / c) * period / length)

    q_v = -sp.log(v)
    h_time = sp.simplify(-sp.log(lapse))
    h_space = sp.simplify(-sp.log(length))
    ppn_gamma = sp.simplify(h_space / h_time)
    gamma_minus_one = sp.simplify(ppn_gamma - 1)

    compactness_readout_scale = sp.simplify(mass_readout / length)
    mass_total = sp.Integer(1)
    dress_mass = sp.simplify(mass_total - mass_readout)
    compactness_total_scale = sp.simplify(mass_total / length)

    return {
        "status": "PASS_SYMBOLIC_MEDIUM_RESPONSE_SCALING_IDENTITIES",
        "active_volume_factor": v,
        "external_active_mass_readout_scale": sp.Eq(
            sp.Symbol("M_active_readout/M0"),
            mass_readout,
        ),
        "proper_inventory_guard": (
            "This is not the internal/proper mass inventory.  It is the "
            "external active readout channel used in the metric ledger."
        ),
        "linear_size_scale": sp.Eq(sp.Symbol("L_oper/L0"), length),
        "clock_rate_scale": sp.Eq(sp.Symbol("d_tau/dt"), lapse),
        "period_scale": sp.Eq(sp.Symbol("dt/d_tau"), period),
        "temporal_index": sp.Eq(sp.Symbol("n_t"), temporal_index),
        "spatial_index": sp.Eq(sp.Symbol("n_s"), spatial_index),
        "optical_index": sp.Eq(sp.Symbol("n"), optical_index),
        "coordinate_light_speed": sp.Eq(sp.Symbol("c_coord/c"), coordinate_light_speed / c),
        "local_c_ratio": sp.Eq(sp.Symbol("c_local/c"), local_c_ratio),
        "local_c_identity": sp.simplify(local_c_ratio - 1) == 0,
        "weak_deficit_variable": sp.Eq(sp.Symbol("q_v"), q_v),
        "time_metric_strength": sp.Eq(sp.Symbol("h_time"), h_time),
        "space_metric_strength": sp.Eq(sp.Symbol("h_space"), h_space),
        "ppn_gamma_analogue": sp.Eq(sp.Symbol("gamma_eff"), ppn_gamma),
        "solar_gamma_one_condition": sp.Eq(ell, tau),
        "gamma_minus_one": gamma_minus_one,
        "active_readout_compactness_scale": sp.Eq(
            sp.Symbol("C_active_readout/C0"),
            compactness_readout_scale,
        ),
        "total_mass_scale": sp.Eq(sp.Symbol("M_total/M0"), mass_total),
        "deficit_dressing_mass_scale": sp.Eq(sp.Symbol("M_dress/M0"), dress_mass),
        "total_compactness_scale": sp.Eq(sp.Symbol("C_total/C0"), compactness_total_scale),
        "meaning": (
            "The same local-c identity can hold for many exponent choices.  "
            "Solar gamma=1 is the sharper metric-branch condition: spatial and "
            "clock-rate exponents must match if both are used as metric factors."
        ),
    }


def classify_candidate_regimes() -> dict[str, object]:
    """
    Compare the main candidate readings discussed in the conversation.

    The exponent convention is always with respect to v, the active volume or
    pressure-occupancy factor:

        M_active_readout/M0 = v^m, L/L0 = v^ell, d tau/dt = v^tau.
    """
    ids = derive_scaling_identities()
    v, m, ell, tau = sp.symbols("v m ell tau", positive=True, real=True)

    gamma_expr = ids["ppn_gamma_analogue"].rhs
    core_c = ids["active_readout_compactness_scale"].rhs
    total_c = ids["total_compactness_scale"].rhs
    dress = ids["deficit_dressing_mass_scale"].rhs
    local_c_identity = ids["local_c_identity"]

    candidates = {
        "volume_mass_metric_branch": {
            "exponents": {m: 1, ell: sp.Rational(1, 3), tau: sp.Rational(1, 3)},
            "interpretation": (
                "external active mass readout follows active volume; isotropic "
                "linear size and metric clock rate follow the cube root"
            ),
            "metric_lapse_status": "PASS_SOLAR_GAMMA_ONE",
            "process_rate_status": "metric clock, not free-molecular transfer rate",
        },
        "volume_mass_free_molecular_process": {
            "exponents": {m: 1, ell: sp.Rational(1, 3), tau: 1},
            "interpretation": (
                "external active mass readout follows volume and an intrinsic "
                "transfer rate is proportional to carrier amount"
            ),
            "metric_lapse_status": "FAILS_SOLAR_GAMMA_IF_USED_AS_METRIC_LAPSE",
            "process_rate_status": "allowed only as a tagged non-metric process-rate channel",
        },
        "continuum_gas_like_process": {
            "exponents": {m: 1, ell: sp.Rational(1, 3), tau: 0},
            "interpretation": (
                "external active mass readout follows volume, but transfer rate "
                "is pressure independent as in a continuum gas regime"
            ),
            "metric_lapse_status": "FAILS_GRAVITATIONAL_REDSHIFT_IF_USED_AS_METRIC_LAPSE",
            "process_rate_status": "possible process analogy only; not the metric clock",
        },
        "p10_biconformal_point_scale": {
            "exponents": {m: 1, ell: 1, tau: 1},
            "interpretation": (
                "p10-style single scale: external/Killing mass, operational "
                "length, and metric clock rate share one factor"
            ),
            "metric_lapse_status": "PASS_SOLAR_GAMMA_ONE",
            "process_rate_status": "point/dressed-excitation scale, not bulk volume-mass law",
        },
    }

    rows = {}
    for name, row in candidates.items():
        subs = row["exponents"]
        gamma_value = sp.simplify(gamma_expr.subs(subs))
        core_compactness = sp.simplify(core_c.subs(subs))
        total_compactness = sp.simplify(total_c.subs(subs))
        dressing_mass = sp.simplify(dress.subs(subs))
        solar_metric_pass = sp.simplify(gamma_value - 1) == 0
        core_becomes_more_compact = sp.simplify(
            core_compactness.subs(v, sp.Rational(1, 2)) > 1
        )
        total_becomes_more_compact = sp.simplify(
            total_compactness.subs(v, sp.Rational(1, 2)) > 1
        )
        rows[name] = {
            **row,
            "gamma_eff": gamma_value,
            "solar_gamma_pass": solar_metric_pass,
            "active_readout_compactness_scale": core_compactness,
            "active_readout_compactness_grows_at_v_half": core_becomes_more_compact,
            "total_compactness_scale_if_mass_conserved": total_compactness,
            "total_compactness_grows_at_v_half": total_becomes_more_compact,
            "dressing_mass_needed_for_total_mass": dressing_mass,
            "local_c_identity": local_c_identity,
        }

    return {
        "status": "PASS_CANDIDATE_REGIMES_CLASSIFIED_BY_OBSERVATIONAL_GUARDRAILS",
        "candidate_rows": rows,
        "main_result": (
            "If the external active mass readout and active volume scale "
            "together, M_active_readout/M0=V_eff/V0 is natural.  This is not "
            "the internal/proper inventory.  A free-molecular transfer-rate "
            "exponent tau=1 cannot also be the Solar metric lapse when "
            "isotropic length scales as V^(1/3); Solar gamma=1 instead "
            "selects tau=ell=1/3 for the metric branch.  The tau=1 law may "
            "survive only as a separate intrinsic process-rate channel."
        ),
    }


def derive_mass_volume_compactness_ledger() -> dict[str, object]:
    """
    Consequence of the external active-volume readout intuition.

    If size means active external volume, then the external active mass readout
    follows volume:

        M_active_readout/M0 = V_eff/V0.

    This is not the internal/proper mass inventory.  In an isotropic external
    readout L/L0=(V_eff/V0)^(1/3).  Therefore the filtered active readout alone
    becomes less compact.  Compact-object behavior requires the total far-zone
    gravitational charge to be active readout plus deficit/dressing, counted
    once.
    """
    v = sp.symbols("v", positive=True, real=True)
    M0, R0 = sp.symbols("M0 R0", positive=True, real=True)

    M_active = sp.simplify(M0 * v)
    R_core = sp.simplify(R0 * v ** sp.Rational(1, 3))
    C_active_ratio = sp.simplify((M_active / R_core) / (M0 / R0))

    M_total = M0
    M_dress = sp.simplify(M_total - M_active)
    C_total_ratio = sp.simplify((M_total / R_core) / (M0 / R0))

    checks = {
        "active_readout_equals_volume": sp.simplify(M_active / M0 - v) == 0,
        "linear_is_cube_root_volume": sp.simplify(R_core / R0 - v ** sp.Rational(1, 3)) == 0,
        "active_readout_compactness_decreases_for_v_half": sp.simplify(
            C_active_ratio.subs(v, sp.Rational(1, 2)) < 1
        ),
        "total_compactness_increases_for_v_half": sp.simplify(
            C_total_ratio.subs(v, sp.Rational(1, 2)) > 1
        ),
        "dressing_nonnegative_for_deficit": sp.simplify(M_dress.subs(v, sp.Rational(1, 2)) > 0),
    }

    return {
        "status": (
            "PASS_VOLUME_MASS_LEDGER_REQUIRES_DRESSING_FOR_COMPACTNESS"
            if all(checks.values())
            else "CHECK_VOLUME_MASS_COMPACTNESS_LEDGER"
        ),
        "checks": checks,
        "active_volume_factor": sp.Eq(sp.Symbol("v"), sp.Symbol("V_eff/V0")),
        "external_active_mass_readout_scale": sp.Eq(
            sp.Symbol("M_active_readout/M0"),
            v,
        ),
        "linear_radius_scale": sp.Eq(sp.Symbol("R_core/R0"), v ** sp.Rational(1, 3)),
        "active_readout_compactness_scale": sp.Eq(
            sp.Symbol("C_active_readout/C0"),
            C_active_ratio,
        ),
        "total_mass_ledger": sp.Eq(sp.Symbol("M_total"), M_total),
        "deficit_dressing_mass": sp.Eq(sp.Symbol("M_dress"), M_dress),
        "total_compactness_scale": sp.Eq(sp.Symbol("C_total/C0"), C_total_ratio),
        "reading": (
            "The law M_active_readout~V_eff is compatible with external "
            "depletion/filtering, but it cannot by itself make a black-hole-like "
            "compact object.  The far gravitational mass must be the conserved "
            "active-readout+dressing charge if compactness is to grow while the "
            "external active volume decreases."
        ),
    }


def medium_response_scaling_status() -> dict[str, object]:
    identities = derive_scaling_identities()
    candidates = classify_candidate_regimes()
    compactness = derive_mass_volume_compactness_ledger()
    passed = (
        identities["status"] == "PASS_SYMBOLIC_MEDIUM_RESPONSE_SCALING_IDENTITIES"
        and candidates["status"]
        == "PASS_CANDIDATE_REGIMES_CLASSIFIED_BY_OBSERVATIONAL_GUARDRAILS"
        and compactness["status"]
        == "PASS_VOLUME_MASS_LEDGER_REQUIRES_DRESSING_FOR_COMPACTNESS"
    )
    return {
        "status": (
            "PASS_OBSERVATIONAL_MEDIUM_RESPONSE_SCALING_LEDGER__DYNAMICAL_MICROPHYSICS_OPEN"
            if passed
            else "CHECK_OBSERVATIONAL_MEDIUM_RESPONSE_SCALING_LEDGER"
        ),
        "identities": identities,
        "candidate_regimes": candidates,
        "mass_volume_compactness": compactness,
        "closed_now": (
            "The allowed bookkeeping is explicit: the external active mass "
            "readout may track active volume; "
            "Solar metric data require the metric clock exponent to match the "
            "spatial exponent; and compactness growth requires conserved "
            "far-zone active-readout+dressing mass rather than the filtered "
            "active readout alone."
        ),
        "not_closed_now": [
            "derive the microscopic stress/lapse/substrate bridge that fixes ell and tau",
            "decide whether the free-molecular transfer law is a separate process-rate channel",
            "derive the deficit/dressing energy ledger from the full action",
            "fit or constrain any non-metric process-rate channel observationally",
        ],
    }


if __name__ == "__main__":
    result = medium_response_scaling_status()
    print("PHASE 15: Medium response scaling gate")
    print("status:", result["status"])
    print("main_result:", result["candidate_regimes"]["main_result"])
    print("mass_volume_status:", result["mass_volume_compactness"]["status"])
    for name, row in result["candidate_regimes"]["candidate_rows"].items():
        print(f"\n{name}")
        print("  gamma_eff:", row["gamma_eff"])
        print("  solar_gamma_pass:", row["solar_gamma_pass"])
        print("  metric_lapse_status:", row["metric_lapse_status"])
        print("  process_rate_status:", row["process_rate_status"])
        print("  active_readout_compactness_scale:", row["active_readout_compactness_scale"])
        print("  total_compactness_scale_if_mass_conserved:", row["total_compactness_scale_if_mass_conserved"])
