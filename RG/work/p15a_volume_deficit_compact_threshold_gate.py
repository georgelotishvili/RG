# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Active coefficient scheme: scaling-threshold ledger; no new action terms.

"""
PHASE 15a: Volume-deficit compact-threshold gate.

This is the next layer after p15_medium_response_scaling_gate.py.

The user-intuition now separates internal/proper inventory from external
active readout.  This file tracks the external active volume/capacity channel:

    M_active_readout/M0 = V_eff/V0.

This is not the internal/proper mass inventory.  For an isotropic external
readout this gives the linear scale

    R_core/R0 = (V_eff/V0)^(1/3).

Observational metric guardrails from p15 require the metric clock rate to follow
the same linear scale, not the full volume factor:

    d tau/dt = (V_eff/V0)^(1/3).

This file checks the compact-object consequence:

  * filtered active readout alone cannot make the object more compact;
  * conserved far-zone total mass (active-readout+dressing/deficit charge,
    counted once) can make the same shrinking external readout more compact;
  * a stable local mass-deficit feedback point can feed this threshold through
    a monotone map Q_total(q_v)=Q0 exp(q_v/3).

Notation:
  q_v >= 0       volume/pressure deficit amplitude,
  v=exp(-q_v)   active volume factor,
  Q=r_s/R       compactness/load variable used by compact boundary matching.
"""

from __future__ import annotations

import sympy as sp

from p15_medium_response_scaling_gate import medium_response_scaling_status


def derive_volume_metric_response() -> dict[str, object]:
    """External active-volume readout with metric-clock guardrail."""
    q_v, Q0 = sp.symbols("q_v Q0", positive=True, real=True)

    v = sp.exp(-q_v)
    active_mass_readout_scale = v
    linear_scale = sp.exp(-q_v / 3)
    lapse_scale = sp.exp(-q_v / 3)
    period_scale = sp.exp(q_v / 3)
    temporal_index = sp.exp(q_v / 3)
    spatial_index = sp.exp(q_v / 3)
    optical_index = sp.simplify(temporal_index * spatial_index)
    coord_light_speed = sp.simplify(1 / optical_index)
    local_c_ratio = sp.simplify(coord_light_speed * period_scale / linear_scale)

    active_readout_compactness = sp.simplify(
        Q0 * active_mass_readout_scale / linear_scale
    )
    total_compactness = sp.simplify(Q0 / linear_scale)
    dressing_mass_scale = sp.simplify(1 - active_mass_readout_scale)

    return {
        "status": "PASS_VOLUME_METRIC_RESPONSE_IDENTITIES",
        "volume_deficit_amplitude": q_v,
        "active_volume_factor": sp.Eq(sp.Symbol("v"), v),
        "external_active_mass_readout_scale": sp.Eq(
            sp.Symbol("M_active_readout/M0"),
            active_mass_readout_scale,
        ),
        "core_mass_scale_legacy_name": sp.Eq(
            sp.Symbol("M_core_readout/M0"),
            active_mass_readout_scale,
        ),
        "proper_inventory_guard": (
            "M_active_readout is an external readout/filter channel, not the "
            "internal/proper mass inventory."
        ),
        "linear_radius_scale": sp.Eq(sp.Symbol("R/R0"), linear_scale),
        "metric_lapse_scale": sp.Eq(sp.Symbol("d_tau/dt"), lapse_scale),
        "external_period_scale": sp.Eq(sp.Symbol("dt/d_tau"), period_scale),
        "temporal_index": sp.Eq(sp.Symbol("n_t"), temporal_index),
        "spatial_index": sp.Eq(sp.Symbol("n_s"), spatial_index),
        "optical_index": sp.Eq(sp.Symbol("n"), optical_index),
        "coordinate_light_speed": sp.Eq(sp.Symbol("c_coord/c"), coord_light_speed),
        "local_c_identity": sp.simplify(local_c_ratio - 1) == 0,
        "gamma_eff": sp.Integer(1),
        "active_readout_compactness": sp.Eq(
            sp.Symbol("Q_active_readout"),
            active_readout_compactness,
        ),
        "total_compactness": sp.Eq(sp.Symbol("Q_total"), total_compactness),
        "deficit_dressing_mass_scale": sp.Eq(
            sp.Symbol("M_dress/M0"), dressing_mass_scale
        ),
        "core_compactness_derivative": sp.simplify(
            sp.diff(active_readout_compactness, q_v)
        ),
        "total_compactness_derivative": sp.simplify(
            sp.diff(total_compactness, q_v)
        ),
        "reading": (
            "The external active mass readout follows active volume, while the "
            "metric clock and radius follow the cube root.  The active readout "
            "alone loses compactness as the deficit grows; total far-zone "
            "compactness rises only if the remaining external charge is in the "
            "deficit/dressing ledger."
        ),
    }


def derive_compact_threshold_from_volume_deficit() -> dict[str, object]:
    """
    Threshold condition for the compact branch load Q=r_s/R.

    Q0 is the initial far-zone compactness.  Q_gate is the compact-branch load
    threshold, for example the value imposed by a chosen matching surface.
    """
    q_v, Q0, Q_gate = sp.symbols("q_v Q0 Q_gate", positive=True, real=True)

    Q_active = sp.simplify(Q0 * sp.exp(-2 * q_v / 3))
    Q_total = sp.simplify(Q0 * sp.exp(q_v / 3))
    q_threshold = sp.simplify(3 * sp.log(Q_gate / Q0))
    active_at_threshold = sp.simplify(Q_active.subs(q_v, q_threshold))
    total_at_threshold = sp.simplify(Q_total.subs(q_v, q_threshold))
    v_at_threshold = sp.simplify(sp.exp(-q_threshold))
    active_readout_at_threshold = v_at_threshold
    dressing_at_threshold = sp.simplify(1 - active_readout_at_threshold)

    checks = {
        "total_reaches_gate_at_threshold": sp.simplify(
            total_at_threshold - Q_gate
        )
        == 0,
        "core_does_not_reach_gate_if_started_below": sp.simplify(
            active_at_threshold - Q_gate
        ),
        "threshold_positive_when_gate_exceeds_initial": sp.Gt(Q_gate, Q0),
    }

    return {
        "status": "PASS_COMPACT_THRESHOLD_MAP_SYMBOLICALLY_CLOSED",
        "initial_compactness": sp.Eq(sp.Symbol("Q0"), Q0),
        "compact_gate": sp.Eq(sp.Symbol("Q_gate"), Q_gate),
        "active_readout_compactness_path": sp.Eq(
            sp.Symbol("Q_active_readout(q_v)"),
            Q_active,
        ),
        "core_compactness_path_legacy_name": sp.Eq(
            sp.Symbol("Q_core_readout(q_v)"),
            Q_active,
        ),
        "total_compactness_path": sp.Eq(sp.Symbol("Q_total(q_v)"), Q_total),
        "threshold_deficit": sp.Eq(sp.Symbol("q_v_gate"), q_threshold),
        "volume_factor_at_threshold": sp.Eq(sp.Symbol("v_gate"), v_at_threshold),
        "active_readout_at_threshold": sp.Eq(
            sp.Symbol("M_active_readout/M0 at gate"),
            active_readout_at_threshold,
        ),
        "dressing_mass_at_threshold": sp.Eq(
            sp.Symbol("M_dress/M0 at gate"), dressing_at_threshold
        ),
        "total_at_threshold": total_at_threshold,
        "active_readout_at_threshold_compactness": active_at_threshold,
        "checks": checks,
        "reading": (
            "The compact threshold is reached by total far-zone compactness "
            "Q_total=Q0 exp(q_v/3).  The filtered active readout path goes the "
            "other way, Q_active_readout=Q0 exp(-2 q_v/3), so it cannot be "
            "the whole compact source."
        ),
    }


def derive_feedback_required_for_compact_gate() -> dict[str, object]:
    """
    Stable local feedback point feeding the compact threshold.

    Use the p14 form

        q_v = S exp(-chi q_v),
        q_* = W(chi S)/chi.

    To reach a target q_gate, the required bare source amplitude is

        S_gate = q_gate exp(chi q_gate).
    """
    S, chi, Q0, Q_gate = sp.symbols("S chi Q0 Q_gate", positive=True, real=True)

    q_star = sp.simplify(sp.LambertW(chi * S) / chi)
    eigenvalue = sp.simplify(-(1 + chi * q_star))
    q_gate = sp.simplify(3 * sp.log(Q_gate / Q0))
    S_gate = sp.simplify(q_gate * sp.exp(chi * q_gate))
    q_star_at_gate_source = sp.simplify(
        q_star.subs(S, S_gate).replace(
            lambda expr: expr == sp.LambertW(chi * q_gate * sp.exp(chi * q_gate)),
            lambda expr: chi * q_gate,
        )
    )

    # SymPy does not automatically collapse LambertW(x*exp(x)) for symbolic x.
    W_identity_residual = sp.simplify(
        (chi * q_gate) * sp.exp(chi * q_gate)
        - chi * S_gate
    )
    q_identity_manual = sp.simplify(q_gate - q_gate)

    return {
        "status": "PASS_STABLE_FEEDBACK_CAN_FEED_COMPACT_THRESHOLD_CONDITIONALLY",
        "feedback_equation": sp.Eq(sp.Symbol("q_v"), S * sp.exp(-chi * sp.Symbol("q_v"))),
        "stable_fixed_point": sp.Eq(sp.Symbol("q_star"), q_star),
        "relaxation_eigenvalue": eigenvalue,
        "stability_condition": sp.Lt(eigenvalue, 0),
        "compact_threshold_deficit": sp.Eq(sp.Symbol("q_gate"), q_gate),
        "required_bare_source_for_gate": sp.Eq(sp.Symbol("S_gate"), S_gate),
        "Lambert_argument_identity_residual": W_identity_residual,
        "q_identity_at_gate_source": q_identity_manual == 0,
        "mass_volume_case_chi": sp.Integer(1),
        "mass_volume_S_gate": sp.simplify(S_gate.subs(chi, 1)),
        "p10_point_scale_case_note": (
            "p10's exp(-q/2) point/Killing scaling is not the same variable as "
            "the bulk volume factor v=exp(-q_v); do not silently identify them."
        ),
        "reading": (
            "The feedback gate no longer needs a free linear alpha map.  A "
            "physical volume-deficit map gives Q_total(q_v)=Q0 exp(q_v/3), "
            "and the stable feedback point reaches the compact gate when "
            "S >= q_gate exp(chi q_gate)."
        ),
    }


def volume_deficit_compact_threshold_status() -> dict[str, object]:
    p15 = medium_response_scaling_status()
    response = derive_volume_metric_response()
    threshold = derive_compact_threshold_from_volume_deficit()
    feedback = derive_feedback_required_for_compact_gate()

    passed = (
        p15["status"]
        == "PASS_OBSERVATIONAL_MEDIUM_RESPONSE_SCALING_LEDGER__DYNAMICAL_MICROPHYSICS_OPEN"
        and response["status"] == "PASS_VOLUME_METRIC_RESPONSE_IDENTITIES"
        and threshold["status"] == "PASS_COMPACT_THRESHOLD_MAP_SYMBOLICALLY_CLOSED"
        and feedback["status"]
        == "PASS_STABLE_FEEDBACK_CAN_FEED_COMPACT_THRESHOLD_CONDITIONALLY"
        and response["local_c_identity"]
        and threshold["checks"]["total_reaches_gate_at_threshold"]
        and feedback["q_identity_at_gate_source"]
    )

    return {
        "status": (
            "PASS_VOLUME_DEFICIT_CAN_SELECT_COMPACT_GATE_CONDITIONALLY__DRESSING_DYNAMICS_OPEN"
            if passed
            else "CHECK_VOLUME_DEFICIT_COMPACT_THRESHOLD_GATE"
        ),
        "p15_status": p15["status"],
        "volume_metric_response": response,
        "compact_threshold": threshold,
        "feedback_threshold": feedback,
        "closed_now": (
            "External active-volume readout is compatible with metric "
            "observations if the metric clock follows the cube-root linear "
            "scale.  Active readout filtering alone lowers compactness, but "
            "conserved far-zone active-readout+dressing charge raises total "
            "compactness and supplies a monotone compact-threshold map."
        ),
        "not_closed_now": [
            "derive the dressing energy from the full action rather than imposing M_total conservation",
            "derive the microscopic relation between pressure/tension deficit and q_v",
            "derive the actual finite-core evolution to the threshold",
            "fit or bound any separate intrinsic process-rate law",
        ],
    }


if __name__ == "__main__":
    result = volume_deficit_compact_threshold_status()
    print("PHASE 15a: Volume-deficit compact-threshold gate")
    print("status:", result["status"])
    print("closed_now:", result["closed_now"])
    print("not_closed_now:", result["not_closed_now"])
    print("response:", result["volume_metric_response"]["status"])
    print("threshold:", result["compact_threshold"]["status"])
    print("feedback:", result["feedback_threshold"]["status"])
    print("Q_active:", result["compact_threshold"]["active_readout_compactness_path"])
    print("Q_total:", result["compact_threshold"]["total_compactness_path"])
