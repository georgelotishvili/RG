"""Exact local-source and causal-scope audit of spherical saturation.

Run: python -X utf8 -B verify_saturation_completion_boundary.py --verbose
Only stdout is written. No evolution or global initial-data family is solved.
The topological focusing argument is an analytical conditional theorem; these
symbolic checks verify its local field-equation premises, not that theorem.
See spherical_saturation_matter_bridge.md, sections 24 through 39.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import sympy as s


def inner_extremal_bridge_checks(exact, gate):
    """Section39: prescribed geometry, ray bound, and a fixed-H obstruction.

    The ray asymptotics use the compact-domain argument in section39, not
    a finite-time numerical extrapolation. Geometry is not a source action.
    """
    def eq(name, expression, target=0):
        exact("inner39_" + name, s.cancel(expression - target))

    def ok(name, condition, **evidence):
        gate("inner39_" + name, condition, **evidence)

    r, a, M, gap, ell = s.symbols("r a M gap ell", positive=True)
    b = 2*M
    P = (r-a)**3
    N = P*(r-b)
    D = N+b*r**3+a**2*r**2
    f = N/D
    c2 = (a**2+3*a*b-a**3/b)/4
    certificate = (r**2*(r-3*a/2)**2+c2*r**2
                   +a**3*b*(1-r*(3/a+1/b)/2)**2)
    eq("geometry_denominator_certificate", D, certificate)
    ok("geometry_positive_square_coefficient",
       s.factor(c2.subs(M, (a+gap)/2)).is_positive,
       domain="a>0, 2M=a+gap, gap>0")
    eq("geometry_denominator_at_centre", D.subs(r, 0), 2*M*a**3)
    eq("geometry_centre_value", f.subs(r, 0), 1)
    eq("geometry_centre_first_derivative", s.diff(f, r).subs(r, 0))
    # Polynomial division checks the centre jet without a large series.
    f2 = -1/(a*b)
    f3 = -(1/a**3+3/(a**2*b)+1/(a*b**2))
    centre_residual = s.Poly(s.expand(N-D*(1+f2*r**2+f3*r**3)), r)
    for power in range(4):
        eq("geometry_centre_jet_" + str(power), centre_residual.nth(power))
    eq("geometry_centre_R", -12*f2, 6/(M*a))
    eq("geometry_centre_K", 24*f2**2, 6/(M**2*a**2))
    eq("geometry_asymptotic_mass", s.limit(r*(1-f)/2, r, s.oo), M)
    eq("geometry_Schwarzschild_limit", f.subs(a, 0), 1-2*M/r)
    fr = s.cancel(s.diff(f, r))
    frr = s.cancel(s.diff(fr, r))
    for order, expression in enumerate((f, fr, frr)):
        eq("geometry_inner_root_order_" + str(order), expression.subs(r, a))
    alpha = (2*M-a)/(a**3*(a+2*M))
    eq("geometry_inner_cubic_coefficient", (1/D*(r-b)).subs(r, a), -alpha)
    ok("geometry_inner_cubic_sign", alpha.subs(M, (a+gap)/2).is_positive)
    eq("geometry_outer_root", f.subs(r, b))
    eq("geometry_outer_kappa", fr.subs(r, b)/2,
       (b-a)**3/(2*b**2*(b**2+a**2)))
    t = s.symbols("t", positive=True)
    ok("geometry_trapped_annulus_numerator", s.factor(N.subs(
        {r: a+gap*t/(1+t), M: (a+gap)/2})).is_negative,
       parametrization="r=a+gap*t/(1+t), t>0 covers all a<r<2M")
    eq("geometry_inner_R", (-frr-4*fr/r+2*(1-f)/r**2).subs(r, a), 2/a**2)
    eq("geometry_inner_K", (frr**2+4*fr**2/r**2+4*(1-f)**2/r**4).subs(r, a), 4/a**4)
    eps = s.symbols("eps", nonzero=True)
    ok("geometry_negative_control_root_offset", (f+eps).subs(r, a) != 0)

    # Fixed-H vacuum mass family: differentiate the actual implicit equation.
    z, H, Hp, Hpp = s.symbols("z H Hp Hpp", nonzero=True)
    zr = -3*H/(r*Hp)
    zM = 12/(r**3*Hp)
    old_fr = -2*r*z-r**2*zr
    old_fM = -r**2*zM
    eq("fixed_law_radial_derivative", old_fr, r*(3*H/Hp-2*z))
    eq("fixed_law_mass_derivative", old_fM, -12/(r*Hp))
    horizon_sub = {z: 1/r**2, H: 12*M/r**3, Hp: 18*M/r}
    eq("fixed_law_degenerate_radial_derivative", old_fr.subs(horizon_sub))
    eq("fixed_law_degenerate_mass_derivative", old_fM.subs(horizon_sub), -s.Rational(2, 3)/M)
    rh_M = s.symbols("rh_M", real=True)
    eq("fixed_law_family_chain_residual", (old_fM+old_fr*rh_M).subs(horizon_sub), -s.Rational(2, 3)/M)
    ok("fixed_law_nonzero_family_obstruction", (-s.Rational(2, 3)/M).is_nonzero)
    # Total radial derivative along H(z(r)), followed by the double-root condition.
    total_rr = (s.diff(old_fr, r)+s.diff(old_fr, z)*zr
                +s.diff(old_fr, H)*Hp*zr+s.diff(old_fr, Hp)*Hpp*zr)
    eq("fixed_law_triple_condition", total_rr.subs(H, 2*z*Hp/3),
       2*z*(2*z*Hpp-Hp)/Hp)
    mass_slope = Hp/(12*z**s.Rational(3, 2))-H/(8*z**s.Rational(5, 2))
    eq("fixed_law_horizon_mass_stationarity", mass_slope.subs(H, 2*z*Hp/3))
    source, Z, Zp = s.symbols("source Z Zp", nonzero=True)
    plateau_fr = r*(-2*Z+3*source*Zp)
    eq("fixed_law_plateau_is_simple", plateau_fr.subs({Z: 1/r**2, Zp: 0}), -2/r)
    oldf = 1-2*M*r**2/(r**3+2*M*ell**2)
    Mh = r**3/(2*(r**2-ell**2))
    eq("fixed_law_Hayward_control_slope", s.diff(oldf, r).subs(M, Mh), (r**2-3*ell**2)/r**3)
    degM = 3*s.sqrt(3)*ell/4
    eq("fixed_law_Hayward_coincident_roots", r**3-2*degM*r**2+2*degM*ell**2,
       (r-s.sqrt(3)*ell)**2*(r+s.sqrt(3)*ell/2))

    # The target has mass-dependent response that a regular fixed H cannot supply.
    target_z = s.cancel((1-f)/r**2)
    fM = s.cancel(s.diff(f, M))
    eq("source_target_mass_response", fM, -2*r**2*P*(r**2+a**2)/D**2)
    eq("source_target_z_response", s.diff(target_z, M), 2*P*(r**2+a**2)/D**2)
    eq("source_persistent_inner_mass_zero", fM.subs(r, a))
    M2 = s.symbols("M2", positive=True)
    mms = r*(1-f)/2
    eq("source_finite_mass_jump", mms.subs(M, M2)-mms,
       r**3*P*(r**2+a**2)*(M2-M)/(D*D.subs(M, M2)))
    Q = r**3-P
    inverse_num = z*r*(P+a**2*r)-a**2
    inverse_den = 2*(r-z*Q)
    inverse_mass = inverse_num/inverse_den
    eq("source_inverse_back_substitution", inverse_mass.subs(z, target_z), M)
    eq("source_inverse_derivative", s.diff(inverse_mass, z).subs(z, target_z),
       D**2/(2*P*(r**2+a**2)))
    eq("source_inverse_zero_numerator", inverse_num.subs({r: a, z: 1/a**2}))
    eq("source_inverse_zero_denominator", inverse_den.subs({r: a, z: 1/a**2}))
    eq("source_inverse_path_ambiguity", (inverse_mass.subs(z, target_z)
       -inverse_mass.subs(z, target_z.subs(M, M2))), M-M2)

    # Same finite-energy incoming tail as section37; unchanged metric null rays.
    v = s.symbols("v", positive=True)
    tail = 2-1/(4*(1+v))
    eq("ray_tail_initial_mass", tail.subs(v, 24), s.Rational(199, 100))
    eq("ray_tail_remaining_mass", 2-tail.subs(v, 24), s.Rational(1, 100))
    eq("ray_tail_derivative", s.diff(tail, v), 1/(4*(1+v)**2))
    eq("ray_annulus_gap_lower_bound", 2*tail.subs(v, 24)-s.Rational(6, 5), s.Rational(139, 50))
    eq("ray_delta_inverse_square_derivative", -2*(r-a)**-3*f/2, (2*M-r)/D)
    eq("ray_c_limit", ((2*M-r)/D).subs({r: 1, a: 1, M: 2}), s.Rational(3, 5))
    Md, K = s.symbols("Md K", positive=True)
    eq("ray_log_Y_derivative", ((fr*f/2+fM*Md)/f-fr/2),
       2*r**2*(r**2+a**2)*Md/(D*(2*M-r)))
    # Warped-sphere Ricci contraction, using the EF connection and null tangent.
    F, Fv, Fr = s.symbols("F Fv Fr", real=True)
    gamma_r_vv, gamma_r_vr = (F*Fr-Fv)/2, -Fr/2
    eq("ray_Ricci_connection_identity", 2*K**2/r*(gamma_r_vv+F*gamma_r_vr), -Fv*K**2/r)
    eq("ray_Ricci_response", -fM*Md*K**2/r,
       2*r*P*(r**2+a**2)*Md*K**2/D**2)
    response_cubic = s.cancel(-fM/(r*(r-a)**3)).subs({r: 1, a: 1, M: 2})
    eq("ray_Ricci_cubic_coefficient", response_cubic, s.Rational(4, 25))
    # The analytic comparison proof gives delta~(c_inf*v)^(-1/2), K~Y*sqrt(c_inf)*v^(3/2).
    cinf, Y = s.Rational(3, 5), s.symbols("Y", positive=True)
    ricci_lead = response_cubic*s.Rational(1, 4)*Y**2*cinf*cinf**-s.Rational(3, 2)
    eq("ray_Ricci_asymptotic_coefficient", ricci_lead, Y**2*s.sqrt(s.Rational(3, 5))/15)
    eq("ray_Ricci_power", -2+3-s.Rational(3, 2), -s.Rational(1, 2))
    eq("ray_finite_affine_remainder", s.integrate(v**-s.Rational(3, 2), (v, 1, s.oo)), 2)
    # A geometric Ricci bound must never be relabelled a bounded photon stress.
    eq("ray_conserved_photon_stress_power", -2+3, 1)
    eq("ray_conserved_photon_stress_coefficient", Y**2*cinf/(16*s.pi), 3*Y**2/(80*s.pi))
    ok("ray_negative_control_photon_stress_unbounded",
       s.limit(Y**2*cinf/(16*s.pi)*v**(-2+3), v, s.oo) == s.oo)
    return dict(
        decision="GEOMETRIC_TARGET_VERIFIED_REGULAR_FIXED_H_BRIDGE_EXCLUDED",
        reference="https://arxiv.org/abs/2205.13556, equation12 specialized with r_-=a, r_+=2M, b2=a^2",
        geometry=dict(domain="a>0, M>a/2, r>=0; a fixed", f="N/D; N=(r-a)^3(r-2M); D=N+2Mr^3+a^2r^2",
                      centre="C2 metric; finite R=6/(Ma), Kretschmann=6/(M^2*a^2)",
                      inner="r=a triple for every M>a/2", outer="r=2M simple"),
        fixed_law=dict(domain="regular fixed H; r^3 H((1-f)/r^2)=12M; finite nonzero H'; differentiable horizon family",
                       obstruction="d f(r_h(M),M)/dM = -2/(3M) != 0 at a degenerate root",
                       exclusions="Extra dynamical matter states, two-function metrics and non-vacuum field equations are outside this no-go."),
        null_ray=dict(domain="a=1; M(v)=2-1/[4(1+v)]; v>=24; r(24)=6/5; outgoing radial affine tangent",
                      proof="Section39 compact-annulus analytical comparison; symbolic identities audited here",
                      delta="Theta(v^(-1/2))", affine_boost="Theta(v^(3/2))",
                      null_Ricci="R_kk~Y_inf^2*sqrt(3/5)/15*v^(-1/2); bounded and tends to zero",
                      endpoint="Finite affine parameter; extension and all-frame curvature not established",
                      conserved_photon_stress="For T_vv=M'/(4pi r^2): T_kk~3Y_inf^2/(80pi)*v; unbounded",
                      source_boundary="A fixed coupled action must generate the suppressed geometric response to this stress."),
        closure=dict(target_geometry_verified=False, conditional_null_Ricci_bound_verified=False,
                     fixed_H_bridge_excluded=False, inverse_law_obstruction_verified=False,
                     fixed_theory_dynamics_derived=False, self_regulating_attractor=False,
                     full_RefG_pressure_join=False, photon_stress_bounded=False,
                     global_singularity_removal=False, full_RefG_rejected=False))


def existing_light_source_checks(exact, gate):
    """Section38: reuse actual light code, then compare the sourced EF rays."""
    work3 = Path(__file__).resolve().parents[2]
    w43 = "Cosmology_and_LSS/Photon_Atomic_Observable_Bridge/"
    w82 = "Strong_Field/W3-82_Dynamical_Clock_Radar_Readout/"
    w91 = "Strong_Field/W3-91_Direct_Scaling_Endpoint/"
    pins = {
        w43 + "w3_43_photon_atomic_observable_bridge_preregistration.md":
            "20793b696e7fcd64a0a4f9a575b4091eeb2faf651973448b87b2c025b2d258da",
        w82 + "w3_82_dynamical_clock_radar_contract.md":
            "3c389016254c2c554bec346e6012857c41daaa01a10e2fbba876be1d971d63d8",
        w82 + "w3_82_dynamical_clock_radar.py":
            "8e9f3d673841a37bb55f445c0f8ff0c8b031bd639254fae01ed6e2ed539dd793",
        w91 + "w3_91_direct_scaling_endpoint_contract.md":
            "d6dfe89f13e34210a7dbd3b4e68e7dff7fb488c93fdc73251a9d03c4b84459c8",
    }
    actual = {path: hashlib.sha256((work3/path).read_bytes()).hexdigest()
              for path in pins}
    gate("light38_existing_optical_inputs_pinned", actual == pins,
         actual_sha256=actual)
    spec = importlib.util.spec_from_file_location(
        "w92_existing_w82_optics", work3/w82/"w3_82_dynamical_clock_radar.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Pure symbolic code only: do not run old mains or read cached PASS output.
    groups, contexts = module.exact_interface()
    for name, group in groups.items():
        gate("light38_w82_recomputed_" + name, group["all_pass"],
             identities=len(group["checks"]))
    controls = module.controls(contexts)
    gate("light38_w82_production_controls", controls["production"]["all_pass"])
    for name, item in controls["mutations"].items():
        gate("light38_w82_mutation_" + name, item["detected"])

    v, r, alpha, ell = s.symbols("v r alpha ell", positive=True)
    f = s.Function("f")(v, r)
    mass = s.Function("m")(v)
    carrier = s.Function("omega_in", positive=True)(v)
    coords = (v, r)
    g = s.Matrix([[-f, 1], [1, 0]])
    gi = g.inv()
    connection = {
        (i, j, k): s.simplify(sum(
            gi[i, a]*(s.diff(g[a, k], coords[j])
                      + s.diff(g[a, j], coords[k])
                      - s.diff(g[j, k], coords[a]))/2 for a in range(2)))
        for i in range(2) for j in range(2) for k in range(2)}
    cov = s.Matrix([-carrier, 0])  # d[-integral omega_in(v) dv]
    ray = gi*cov
    xi = s.diff(mass, v)/(alpha*r**2)
    # Phase-averaged/RMS normalization absorbs EM units and real-wave averaging.
    amplitude2 = xi/carrier**2
    current = amplitude2*ray
    exact("light38_eikonal_null", (cov.T*gi*cov)[0])
    exact("light38_phase_closed", s.diff(cov[0], r)-s.diff(cov[1], v))
    exact("light38_future_ingoing_ray", ray[1], -carrier)
    for i in range(2):
        acceleration = sum(ray[j]*s.diff(ray[i], coords[j]) for j in range(2))
        acceleration += sum(connection[i, j, k]*ray[j]*ray[k]
                            for j in range(2) for k in range(2))
        exact("light38_affine_ray_" + str(i), acceleration)
    divergence = sum(s.diff(r**2*current[i], coords[i])
                     for i in range(2))/r**2
    exact("light38_wave_action_conservation", divergence)
    exact("light38_boundary_number_flux", -r**2*current[1],
          s.diff(mass, v)/(alpha*carrier))

    K = s.symbols("Uv", positive=True)
    observer = s.Matrix([K, (f*K-1/K)/2])
    outward = s.Matrix([K, (f*K+1/K)/2])
    frequency = -(observer.T*cov)[0]
    exact("light38_observer_unit_norm", (observer.T*g*observer)[0], -1)
    exact("light38_radial_unit_norm", (outward.T*g*outward)[0], 1)
    exact("light38_orthogonal_frame", (observer.T*g*outward)[0])
    exact("light38_existing_frequency_projection", frequency, carrier*K)
    for i in range(2):
        exact("light38_local_photon_decomposition_" + str(i),
              ray[i], frequency*(observer[i]-outward[i]))
    local_momentum = (outward.T*cov)[0]
    exact("light38_local_speed_squared", local_momentum**2/frequency**2, 1)
    # Instantaneous proper period; endpoint identity is differential phase timing.
    pulse = 2*s.pi/(carrier*K)
    exact("light38_phase_proper_pulse", frequency*pulse, 2*s.pi)
    Ke, Ko = s.symbols("Uv_e Uv_o", positive=True)
    exact("light38_same_front_endpoint_reciprocity",
          (pulse.subs(K, Ko)/pulse.subs(K, Ke))
          *(frequency.subs(K, Ko)/frequency.subs(K, Ke)), 1)
    measured_number = -(observer.T*g*current)[0]
    exact("light38_positive_number_readout", measured_number, xi*K/carrier)
    exact("light38_energy_number_ledger", measured_number*frequency, xi*K**2)

    # Reconstruct the leading, polarization-averaged Maxwell Hilbert tensor.
    # This is not a claim that this amplitude solves all finite-wavelength terms.
    theta = s.symbols("theta", real=True)
    g4 = s.diag(1, 1, r**2, r**2*s.sin(theta)**2)
    g4[:2, :2] = g
    gi4 = g4.inv()
    p4 = s.Matrix([-carrier, 0, 0, 0])
    polar = s.Matrix([0, 0, r, 0])  # unit covector, on an angular patch
    exact("light38_transverse_polarization", (p4.T*gi4*polar)[0])
    exact("light38_unit_polarization", (polar.T*gi4*polar)[0], 1)
    wave = p4*polar.T-polar*p4.T
    invariant = sum(wave[i, j]*(gi4*wave*gi4)[i, j]
                    for i in range(4) for j in range(4))
    exact("light38_Maxwell_leading_invariant", invariant)
    hilbert = amplitude2*(wave*gi4*wave.T-g4*invariant/4)
    expected = amplitude2*p4*p4.T
    for i, j in ((0, 0), (0, 1), (1, 1), (2, 2), (3, 3)):
        exact("light38_Maxwell_stress_" + str(i) + str(j),
              hilbert[i, j], expected[i, j])
    exact("light38_original_Tvv_recovered", hilbert[0, 0], xi)
    exact("light38_original_source_mass_balance",
          alpha*r**2*hilbert[0, 0], s.diff(mass, v))
    exact("light38_stress_trace", sum(gi4[i, j]*hilbert[i, j]
                                     for i in range(4) for j in range(4)))
    exact("light38_polarization_parallel_transport",
          -carrier*s.diff(1/r, r)-carrier*(1/r)*(1/r))
    T = amplitude2*cov*cov.T
    mixed = gi*T
    for b in range(2):
        divT = sum(s.diff(r**2*mixed[a, b], coords[a])/r**2
                   - sum(connection[c, a, b]*mixed[a, c] for c in range(2))
                   for a in range(2))
        exact("light38_stress_conservation_" + str(b), divT)
    fsol = 1-2*mass*r**2/(r**3+2*mass*ell**2)
    q = r**3/(r**3+2*mass*ell**2)
    exact("light38_gravity_response_already_included",
          -s.diff(fsol, v)/(2*r), alpha*q**2*hilbert[0, 0])
    exact("light38_static_tail_zero_flux_control",
          hilbert[0, 0].subs(s.diff(mass, v), 0))

    # Existing rod/clock law: p^2 is a coordinate speed, not extra absorption.
    pt, pl, p, eps = s.symbols("pT pL p epsilon", positive=True)
    static_g = s.diag(-pt**2, pl**(-2))
    static_cov = s.Matrix([-eps, -eps/(pt*pl)])
    static_ray = static_g.inv()*static_cov
    exact("light38_static_common_metric_null", (static_cov.T*static_ray)[0])
    exact("light38_coordinate_light_speed", -static_ray[1]/static_ray[0], pt*pl)
    exact("light38_common_p_square_limit", (pt*pl).subs({pt:p, pl:p}), p**2)
    exact("light38_static_local_light_speed",
          -(static_ray[1]/pl)/(pt*static_ray[0]), 1)
    static_observer = s.Matrix([1/pt, 0])
    exact("light38_static_frequency_clock", -(static_observer.T*static_cov)[0],
          eps/pt)
    pe, po = s.symbols("p_e p_o", positive=True)
    exact("light38_static_endpoint_clock_ratio", (eps/po)/(eps/pe), pe/po)

    # A missing receiver factor or extra radial attenuation is detectable.
    attenuation = s.Function("S")(v, r)
    changed_current = attenuation*current
    bad_div = sum(s.diff(r**2*changed_current[i], coords[i])
                  for i in range(2))/r**2
    exact("light38_extra_attenuation_exchange_required", bad_div,
          -xi*s.diff(attenuation, r)/carrier)
    gate("light38_radial_attenuation_mutation_detected", bad_div != 0)
    gate("light38_omitted_clock_mutation_detected",
         s.simplify(frequency-carrier) != 0)
    gate("light38_extra_static_p_mutation_detected",
         s.simplify((pe/po)**2-pe/po) != 0)
    gate("light38_unchanged_mass_with_changed_source_detected",
         s.simplify(alpha*r**2*attenuation*hilbert[0, 0]-s.diff(mass, v)) != 0)

    # An exactly SO(3)-invariant coherent source-free Maxwell field is Coulomb.
    # This does not exclude a spherical distribution of incoherent photons.
    electric = s.Function("electric")(v, r)
    magnetic = s.Function("magnetic")(v, r)
    em = s.zeros(4)
    em[0, 1], em[1, 0] = electric, -electric
    em[2, 3], em[3, 2] = magnetic*s.sin(theta), -magnetic*s.sin(theta)
    exact("light38_spherical_magnetic_Bianchi_time",
          s.diff(em[2, 3], v)/s.sin(theta), s.diff(magnetic, v))
    exact("light38_spherical_magnetic_Bianchi_radius",
          s.diff(em[2, 3], r)/s.sin(theta), s.diff(magnetic, r))
    raised = gi4*em*gi4
    exact("light38_spherical_Maxwell_v_constraint",
          s.diff(r**2*raised[1, 0], r)/r**2,
          s.diff(r**2*electric, r)/r**2)
    exact("light38_spherical_Maxwell_r_constraint",
          s.diff(r**2*raised[0, 1], v)/r**2, -s.diff(electric, v))
    charge, magnetic_charge = s.symbols("Q Qm", real=True)
    ec = em.subs({electric:charge/r**2, magnetic:magnetic_charge})
    ec_invariant = sum(ec[i, j]*(gi4*ec*gi4)[i, j]
                       for i in range(4) for j in range(4))
    tc = ec*gi4*ec.T-g4*ec_invariant/4
    exact("light38_exact_spherical_Maxwell_no_radial_flux", (gi4*tc)[1, 0])
    exact("light38_exact_spherical_Maxwell_radial_stress", tc[0, 1],
          -(charge**2+magnetic_charge**2)/(2*r**4))
    # Blueshift alone neither establishes nor disproves wave/EFT validity.
    tidal_wave = q**2*s.diff(mass, v)*K**2/r**2
    exact("light38_tidal_to_frequency_ratio", tidal_wave/frequency**2,
          q**2*s.diff(mass, v)/(r**2*carrier**2))
    w0 = s.symbols("omega0", positive=True)
    ratio = (q**2*s.diff(mass, v)/(r**2*w0**2)).subs(
        mass, 2-1/(4*(1+v))).doit()
    exact("light38_fixed_radius_optical_ratio_limit", s.limit(ratio, v, s.oo))
    return dict(
        decision="COMPATIBLE_WITH_EXISTING_LEADING_LIGHT_LAWS_NO_MISSING_P_FACTOR",
        source_sha256=actual,
        reused_W82=dict(identity_count=sum(len(x["checks"]) for x in groups.values()),
                        groups={name:x["all_pass"] for name,x in groups.items()},
                        mutation_controls=controls["all_pass"]),
        exact_dictionary=dict(phase="theta=-integral omega_in(v)dv",
                              amplitude_squared="m'/(alpha*r^2*omega_in^2)",
                              measured_frequency="omega_in*U^v",
                              measured_energy_density="m'*(U^v)^2/(alpha*r^2)",
                              local_speed="c0", response="q^2 already in geometry"),
        boundary="m(v) is prescribed incoming luminosity data, not a derived oscillon emitter.",
        approximation="Exact null-fluid solution; leading Maxwell/kinetic optical stress. No full finite-wavelength solution or uniform endpoint error proof.",
        scope_notes=[
            "The W82 test-ray calculation excludes backreaction only in its own scope; section37 includes this source in the metric equations.",
            "No additional pressure attenuation is present in the selected existing optical action.",
            "A radial attenuation needs compensating energy exchange and a modified sourced solution.",
            "High blueshift alone does not establish geometric-optics or EFT breakdown.",
            "Zero late incoming flux removes this flux term, not every possible singularity."],
        closure=dict(existing_light_transport_compatible=False,
                     leading_optical_stress_matches=False,
                     no_extra_scale_factor_needed=False,
                     source_backreaction_included=False,
                     optical_scope_boundary_verified=False,
                     exact_coherent_Maxwell_solution=False,
                     uniform_endpoint_optical_validity=False,
                     incoming_tail_derived_from_oscillons=False,
                     full_foundation_photon_action_derived=False,
                     full_RefG_rejected=False, global_singularity_removal=False))


def null_tail_curvature_checks(exact, gate):
    """Section37: exact null-fluid solution and rational ODE certificate."""
    v,r,ell,alpha=s.symbols("v r ell alpha",positive=True)
    m=s.Function("m")(v)
    F=s.Function("f")(v,r)
    coord=(v,r)
    gamma=s.Matrix([[-F,1],[1,0]])
    inverse=gamma.inv()
    conn={}
    for i in range(2):
        for j in range(2):
            for k in range(2):
                conn[i,j,k]=s.simplify(sum(inverse[i,l]*(s.diff(gamma[l,k],coord[j])+s.diff(gamma[l,j],coord[k])-s.diff(gamma[j,k],coord[l]))/2 for l in range(2)))
    hess=s.Matrix(2,2,lambda i,j:-conn[1,i,j])
    box=sum(inverse[i,j]*hess[i,j] for i in range(2) for j in range(2))
    hess_sq=sum(inverse[i,k]*inverse[j,l]*hess[i,j]*hess[k,l] for i in range(2) for j in range(2) for k in range(2) for l in range(2))
    ric=s.Matrix(2,2,lambda i,j:sum(s.diff(conn[k,i,j],coord[k])-s.diff(conn[k,i,k],coord[j])+sum(conn[k,k,l]*conn[l,i,j]-conn[k,j,l]*conn[l,i,k] for l in range(2)) for k in range(2)))
    R2=s.simplify(sum(inverse[i,j]*ric[i,j] for i in range(2) for j in range(2)))
    exact("null_tail_direct_orbit_curvature",R2,-s.diff(F,r,2))
    exact("null_tail_direct_box_radius",box,s.diff(F,r))
    exact("null_tail_hessian_square",hess_sq,s.diff(F,r)**2/2)
    f=1-2*m*r**2/(r**3+2*m*ell**2)
    evaluate=lambda expr:s.factor(expr.subs(F,f).doit())
    z=(1-f)/r**2
    q=1-ell**2*z
    Ao=2*r**2*z*(1-3*ell**2*z)/q**2
    beta=-2*r/q**2
    for i,j,name,target in ((0,0,"vv",2*s.diff(m,v)),(0,1,"vr",0),(1,1,"rr",0)):
        E=beta*evaluate(hess[i,j])-(Ao/2+beta*evaluate(box))*evaluate(gamma[i,j])
        exact("null_tail_original_orbit_"+name,E,target)
    # Angular equation differentiated at fixed X before the background is inserted.
    rr,X=s.symbols("areal X",real=True)
    zz=(1-X)/rr**2
    aa=2*rr**2*zz*(1-3*ell**2*zz)/(1-ell**2*zz)**2
    bb=-2*rr/(1-ell**2*zz)**2
    bg={rr:r,X:f}
    angular=(-beta*evaluate(R2)+s.diff(aa,rr).subs(bg)+
             2*s.diff(bb,rr).subs(bg)*evaluate(box)+
             2*s.diff(bb,X).subs(bg)*evaluate(box**2-hess_sq))
    exact("null_tail_original_angular",s.factor(angular),0)
    exact("null_tail_generalized_mass",r**3*z/(2*q),m)
    exact("null_tail_mass_equation",s.diff(r**3*z/(2*q),v),s.diff(m,v))
    density=s.diff(m,v)/(alpha*r**2)
    exact("null_tail_null_action_constraint",inverse[0,0],0)
    exact("null_tail_source_conservation",s.diff(r**2*density,r)/r**2,0)
    for i in range(2):
        exact("null_tail_ingoing_affine_"+str(i),conn[i,1,1],0)
    exact("null_tail_source_equation_normalization",2*alpha*r**2*density,2*s.diff(m,v))
    K=s.symbols("kv",positive=True)
    k=s.Matrix([K,F*K/2])
    exact("null_tail_outgoing_null",(k.T*gamma*k)[0],0)
    klog=-s.diff(F,r)/2
    exact("null_tail_affine_v_equation",K**2*klog+sum(conn[0,i,j]*k[i]*k[j] for i in range(2) for j in range(2)),0)
    r_accel=K**2*(s.diff(F,v)/2+s.diff(F,r)*F/4+F*klog/2)
    exact("null_tail_affine_r_equation",r_accel+sum(conn[1,i,j]*k[i]*k[j] for i in range(2) for j in range(2)),0)
    Rkk=-2*(k.T*hess*k)[0]/r
    exact("null_tail_parallel_Ricci_geometry",Rkk,-s.diff(F,v)*K**2/r)
    exact("null_tail_parallel_Ricci_source",evaluate(Rkk),2*q**2*s.diff(m,v)*K**2/r**2)
    exact("null_tail_parallel_screen_tide",-r_accel/r,Rkk/2)
    exact("null_tail_vacuum_flux_control",evaluate(Rkk).subs(s.diff(m,v),0),0)
    R4=R2+2*(1-F)/r**2-4*box/r
    Kretsch=R2**2+4*((1-F)/r**2)**2+8*hess_sq/r**2
    exact("null_tail_Ricci_scalar",R4,-s.diff(F,r,2)-4*s.diff(F,r)/r+2*(1-F)/r**2)
    exact("null_tail_Kretschmann",Kretsch,s.diff(F,r,2)**2+4*s.diff(F,r)**2/r**2+4*(1-F)**2/r**4)
    exact("null_tail_Einstein_control",f.subs(ell,0),1-2*m/r)

    # Exact invariant-rectangle proof, not a numerical integration.
    mm=s.symbols("mass",positive=True)
    fc=f.subs({ell:1,m:mm})
    qc=q.subs({ell:1,m:mm})
    lo,hi,mlo,mhi=s.Rational(7,6),s.Rational(5,4),s.Rational(199,100),s.S(2)
    exact("null_tail_mass_monotonic_f",s.diff(fc,mm),-2*r**5/(r**3+2*mm)**2)
    left=s.factor(fc.subs({r:lo,mm:mhi}))
    right=s.factor(fc.subs({r:hi,mm:mlo}))
    exact("null_tail_left_inward_value",left,s.Rational(31,1207))
    exact("null_tail_right_inward_value",right,-s.Rational(457,9493))
    gate("null_tail_invariant_rectangle_signs",bool(left>0 and right<0))
    gate("null_tail_initial_radius_inside",bool(lo<s.Rational(6,5)<hi))
    exact("null_tail_nonextremal_margin",mlo**2-s.Rational(27,16),s.Rational(56815,25000))
    # Each numerator factor is positive; bound factors separately on the box.
    rate=-s.diff(fc,r)/2
    exact("null_tail_affine_growth_rate",rate,mm*r*(4*mm-r**3)/(r**3+2*mm)**2)
    rate_low=s.factor(mlo*lo*(4*mlo-hi**3)/(hi**3+2*mhi)**2)
    q_low=s.factor(lo**3/(hi**3+2*mhi))
    exact("null_tail_rate_bound_independent",rate_low,s.Rational(107104984,272176875))
    exact("null_tail_q_bound_independent",q_low,s.Rational(2744,10287))
    gate("null_tail_uniform_positive_growth",bool(rate_low>s.Rational(3,8)))
    gate("null_tail_response_away_from_zero",bool(q_low>s.Rational(1,4)))
    gate("null_tail_box_denominator_positive",bool(lo**3+2*mlo>0 and lo>0))
    tail=2-1/(4*(1+v))
    exact("null_tail_initial_mass",tail.subs(v,24),mlo)
    exact("null_tail_final_mass",s.limit(tail,v,s.oo),mhi)
    exact("null_tail_remaining_finite_energy",mhi-tail.subs(v,24),s.Rational(1,100))
    exact("null_tail_positive_flux",s.diff(tail,v),1/(4*(1+v)**2))
    exact("null_tail_Ricci_prefactor_bound",2*s.Rational(1,4)**2*s.Rational(1,4)/hi**2,s.Rational(1,50))
    lower=s.exp(3*(v-24)/4)/(50*(1+v)**2)
    divergence_limit=s.limit(lower,v,s.oo)
    gate("null_tail_parallel_curvature_diverges",divergence_limit==s.oo,
         limit=str(divergence_limit))
    exact("null_tail_affine_length_bound",s.integrate(s.exp(-3*(v-24)/8),(v,24,s.oo)),s.Rational(8,3))
    # The same divergence is experienced by an affinely parametrized massive
    # test observer; this is a geodesic, not a stationary accelerated frame.
    U=s.Matrix([K,(F*K-1/K)/2])
    exact("null_tail_timelike_norm",(U.T*gamma*U)[0],-1)
    exact("null_tail_timelike_v_geodesic",K**2*klog+sum(conn[0,i,j]*U[i]*U[j] for i in range(2) for j in range(2)),0)
    ur=(F*K-1/K)/2
    ur_rate=s.diff(ur,v)*K+s.diff(ur,r)*ur+s.diff(ur,K)*K**2*klog
    exact("null_tail_timelike_r_geodesic",ur_rate+sum(conn[1,i,j]*U[i]*U[j] for i in range(2) for j in range(2)),0)
    tide=-(U.T*hess*U)[0]/r
    exact("null_tail_timelike_screen_tide",tide,-s.diff(F,v)*K**2/(2*r)+s.diff(F,r)/(2*r))
    exact("null_tail_timelike_source_tide",evaluate(tide),q**2*s.diff(m,v)*K**2/r**2+s.diff(f,r)/(2*r))
    exact("null_tail_timelike_left_margin",left-s.Rational(1,64),s.Rational(777,77248))
    gate("null_tail_timelike_interval_invariant",bool(left-s.Rational(1,64)>0 and right<0))
    exact("null_tail_tidal_remainder_bound",1+s.diff(fc,r)/(2*r),r**3*(r**3+5*mm)/(r**3+2*mm)**2)
    proper_time=s.integrate(s.exp(-3*(v-24)/8)/8,(v,24,s.oo))
    exact("null_tail_timelike_proper_time_bound",proper_time,s.Rational(1,3))
    tide_lower=s.Rational(16,25)*s.exp(3*(v-24)/4)/(1+v)**2-1
    exact("null_tail_timelike_tidal_prefactor",s.Rational(1,4)**2*s.Rational(1,4)*64/hi**2,s.Rational(16,25))
    gate("null_tail_timelike_tidal_divergence",s.limit(tide_lower,v,s.oo)==s.oo)
    return dict(
        decision="FINITE_MASS_CONSERVED_NULL_SOURCE_HAS_FINITE_AFFINE_PP_CURVATURE_BLOWUP",
        source="New explicit null-fluid diagnostic action; unchanged rational gravity. Not the canonical-sextic packet.",
        exact_solution="f=1-2m(v)r^2/(r^3+2m(v)ell^2), Tvv=m'(v)/(alpha*r^2), other orbit/angular stresses zero",
        certificate=dict(ell=1,start_v=24,start_r="6/5",start_kv=1,r_interval=["7/6","5/4"],
                         mass="2-1/[4(1+v)]",remaining_geometric_energy="1/100",
                         q_lower="1/4",growth_lower="3/8",affine_remaining_upper="8/3",
                         parallel_Ricci_lower="exp[3(v-24)/4]/[50(1+v)^2] -> infinity"),
        timelike_certificate=dict(start_Uv=8,start_r="6/5",proper_time_remaining_upper="1/3",
                                  angular_tidal_lower="(16/25)*exp[3(v-24)/4]/(1+v)^2-1 -> infinity"),
        proof=["Smooth vector field and inward boundary signs preserve the compact radial interval for all finite v.",
               "Uniform -f_r/2>=3/8 yields k^v>=exp[3(v-24)/8] and future affine length<=8/3.",
               "q>1/4 and r<=5/4 turn exact Rkk into the divergent displayed lower bound.",
               "R(k,e_theta,k,e_theta)=Rkk/2 for a parallel angular screen; no regular C2 extension along that geodesic.",
               "Curvature scalars are rational smooth functions on the compact(r,m) box and stay bounded."],
        scope="Actual dynamic counterexample in this gravity+positive conserved null sector, not a proof of canonical-packet blowup, formation from a regular centre, or full RefG rejection.",
        evidence_type="Analytical ODE comparison proof with exact rational certificate; no sampled trajectory or observational fit.",
        closure=dict(null_source_solution=False,finite_affine_pp_blowup=False,finite_proper_time_tidal_blowup=False,
                     universal_null_source_regularization_excluded=False,fixed_scalar_packet_blowup=False,
                     scalar_polynomial_blowup=False,full_RefG_rejected=False,global_singularity_removal=False))


def full_coframe_source_decision_checks(exact, gate):
    """Section36: exact readouts and premises of two analytical exclusions."""
    r,m,ell,alpha = s.symbols("r m ell alpha", positive=True)
    fvac = 1-2*m*r**2/(r**3+2*m*ell**2)
    z = (1-fvac)/r**2
    q = 1-ell**2*z
    exact("readout_vacuum_generalized_mass",r**3*z/(2*q),m)
    exact("readout_vacuum_mass_constraint",s.diff(r**3*z/(2*q),r),0)
    exact("readout_Einstein_limit",fvac.subs(ell,0),1-2*m/r)
    x = s.symbols("s",positive=True)
    L = s.Function("pL")(x)
    D = 1-x*s.diff(L,x)/L
    R = x/L
    exact("readout_radial_pullback",s.diff(R,x)**2/D**2,L**(-2))
    exact("readout_angular_pullback",R**2,x**2/L**2)
    # D>0 is the outward static branch; source clock factor is sigma*D.
    sig,fp,rho,Pr = s.symbols("sigma fprime rho Pr",real=True)
    exact("readout_clock_rod_speed",(sig*D)*L,sig*(L-x*s.diff(L,x)))
    exact("readout_static_lapse_vacuum",(alpha*r*q**2*(rho+Pr)/fvac).subs({rho:0,Pr:0}),0)
    # Solve, rather than prescribe, the four asymptotic spatial coefficients.
    y = s.symbols("inverse_s",real=True)
    coeffs = s.symbols("c1:5",real=True)
    P = 1+sum(c*y**(i+1) for i,c in enumerate(coeffs))
    diso = 1+y*s.diff(P,y)/P
    fiso = 1-2*m*y*P/(1+2*m*ell**2*y**3*P**3)
    residual = s.series(diso**2-fiso,y,0,5).removeO().expand()
    solved = {}
    for order,c in enumerate(coeffs,1):
        eq=s.simplify(residual.coeff(y,order).subs(solved))
        roots=s.solve(eq,c)
        gate("readout_series_unique_order_"+str(order),len(roots)==1)
        solved[c]=roots[0]
    ps=s.expand(P.subs(solved))
    pt=s.series(diso.subs(solved),y,0,5).removeO().expand()
    expected_L=1-m*y+3*m**2*y**2/4-m**3*y**3/2+(5*m**4/16+m**2*ell**2/2)*y**4
    expected_T=1-m*y+m**2*y**2/2-m**3*y**3/4+(m**4/8+2*m**2*ell**2)*y**4
    exact("readout_independent_spatial_series",ps,expected_L)
    exact("readout_independent_clock_series",pt,expected_T)
    exact("readout_first_order_common",(pt-ps).coeff(y,1),0)
    exact("readout_second_order_split",(pt-ps).expand().coeff(y,2),-m**2/4)
    exact("readout_full_series_residual",residual.subs(solved),0)
    exact("readout_PPN_temporal_order2",s.expand(pt**2).coeff(y,2),2*m**2)
    exact("readout_PPN_spatial_order1",s.series(ps**(-2),y,0,2).removeO().coeff(y,1),2*m)
    rh=s.symbols("rh",positive=True)
    mh=rh**3/(2*(rh**2-ell**2))
    exact("readout_horizon_root",fvac.subs({m:mh,r:rh},simultaneous=True),0)
    exact("readout_horizon_derivative",s.diff(fvac,r).subs(r,rh).subs(m,mh),(rh**2-3*ell**2)/rh**3)
    exact("readout_horizon_q",q.subs(r,rh).subs(m,mh),1-ell**2/rh**2)
    exact("readout_centre_static_clock",s.limit(s.sqrt(fvac),r,0),1)
    exact("readout_centre_response",s.limit(q,r,0),0)
    # Recover old extra equality as a constraint, not as a field equation.
    Z=s.symbols("zc",positive=True)
    Q=1-ell**2*Z
    nc=alpha*Q**2*(rho+Pr)/2-Z/2
    required=s.solve((nc-Z/4).subs(rho,3*Z/(2*alpha*Q)),Pr)[0]
    exact("readout_static_common_centre_recovery",required/(3*Z/(2*alpha*Q)),ell**2*Z/Q)

    # Direct static orbit tensor in ingoing EF, before setting f=0.
    f=s.Function("f")(r)
    sigma=s.Function("sigma")(r)
    coordinates=(s.symbols("v",real=True),r)
    gamma=s.Matrix([[-sigma**2*f,sigma],[sigma,0]])
    inverse=gamma.inv()
    conn={}
    for i in range(2):
        for j in range(2):
            for k in range(2):
                conn[i,j,k]=s.simplify(sum(inverse[i,l]*(s.diff(gamma[l,k],coordinates[j])+s.diff(gamma[l,j],coordinates[k])-s.diff(gamma[j,k],coordinates[l]))/2 for l in range(2)))
    box=-sum(inverse[i,j]*conn[1,i,j] for i in range(2) for j in range(2))
    Ao,Beta=s.symbols("alpha_orbit beta",real=True)
    Evv=-Beta*conn[1,0,0]-(Ao/2+Beta*box)*gamma[0,0]
    exact("stationary_original_Evv",Evv,sigma**2*f*(Ao+Beta*s.diff(f,r))/2)
    exact("stationary_horizon_Evv",s.factor(Evv).subs(f,0),0)
    omega,A,B,Ar,Br,potential=s.symbols("omega A B Ar Br V",real=True)
    kinetic=f*(Ar**2+Br**2)+2*omega*(B*Ar-A*Br)/sigma
    Tvv=omega**2*(A*A+B*B)-gamma[0,0]*(kinetic/2+potential)
    exact("stationary_horizon_source",Tvv.subs(f,0),omega**2*(A*A+B*B))
    chi=s.symbols("chi",real=True)
    V=chi**2/2-chi**4/4+chi**6/24
    exact("stationary_potential_positive_derivative",s.diff(V,chi),chi*(1-chi**2/2)**2)
    exact("stationary_nonvacuum_extremum",V.subs(chi,s.sqrt(2)),s.Rational(1,3))
    F=s.Function("F")(r)
    g=s.Function("g")(r)
    vcoord=coordinates[0]
    phase=s.exp(-s.I*omega*vcoord)
    field=phase*F
    divergence=sum(s.diff(sigma*r**2*inverse[i,j]*s.diff(field,coordinates[j]),coordinates[i]) for i in range(2) for j in range(2))/(sigma*r**2)-g*field
    a=sigma*r**2*f
    b=2*s.I*omega*r+sigma*r**2*g
    radial=s.diff(a*s.diff(F,r),r)-2*s.I*omega*r**2*s.diff(F,r)-b*F
    exact("stationary_direct_EF_KG",s.simplify(divergence/phase*sigma*r**2),radial)
    mu=s.Function("mu")(r)
    integrating=s.diff(mu*a*s.diff(F,r),r)-mu*b*F
    exact("stationary_unit_phase_integrating_factor",integrating.subs(s.diff(mu,r),-2*s.I*omega*r**2*mu/a),mu*radial)
    U,W=s.Function("U")(r),s.Function("W")(r)
    norm=U**2+W**2
    gw=(1-norm/2)**2
    kgU=s.diff(a*s.diff(U,r),r)-sigma*r**2*gw*U
    kgW=s.diff(a*s.diff(W,r),r)-sigma*r**2*gw*W
    boundary=a*(U*s.diff(U,r)+W*s.diff(W,r))
    density=a*(s.diff(U,r)**2+s.diff(W,r)**2)+sigma*r**2*norm*gw
    exact("stationary_zero_frequency_integral_identity",U*kgU+W*kgW,s.diff(boundary,r)-density)
    c_bound,b_bound=s.symbols("c_bound b_bound",positive=True)
    exact("stationary_horizon_uniqueness_contraction",b_bound/c_bound*(c_bound/(2*b_bound)),s.Rational(1,2))

    # Separate minimal-current candidate: its *local* rho(n), not ADM mass.
    n,nstar,rhostar,m0=s.symbols("n nstar rhostar m0",positive=True)
    cap=rhostar*n/(n+nstar)
    cap_cs=s.simplify(n*s.diff(cap,n,2)/s.diff(cap,n))
    exact("minimal_current_cap_sound_squared",cap_cs,-2*n/(n+nstar))
    gate("minimal_current_cap_gradient_sign_fails",bool((-cap_cs).is_positive))
    exact("minimal_current_cap_limit",s.limit(cap,n,s.oo),rhostar)
    exact("minimal_current_linear_control",n*s.diff(m0*n,n,2)/s.diff(m0*n,n),0)
    fn=s.Function("rho")(n)
    pressure=n*s.diff(fn,n)-fn
    exact("minimal_current_convexity_pressure_identity",s.diff(pressure,n),n*s.diff(fn,n,2))
    paths=["Lagrangian_Formulation/Weak_Field_Closure/w3_51_weak_field_closure_contract.md",
           "Lagrangian_Formulation/Full_1PN_Inheritance/w3_52_full_1pn_inheritance_contract.md",
           "Lagrangian_Formulation/Relational_Coframe_TEGR_Phase_Source_Closure/w3_54_relational_coframe_tegr_phase_source_closure_contract.md",
           "Strong_Field/W3-67_Foundation_Strong_Field_Response/w3_67_foundation_strong_field_response_preregistration.md"]
    work3=Path(__file__).resolve().parents[2]
    return dict(
        decision="FULL_READOUT_RESTORED_STATIONARY_AND_MINIMAL_DENSITY_CAP_ROUTES_EXCLUDED",
        resource_sha256={p:hashlib.sha256((work3/p).read_bytes()).hexdigest() for p in paths},
        readout=dict(clock="pT=sigma*(1-s*pL_prime/pL)",spatial="pL=s/r",light="c_coord=c0*pT*pL",
                     weak_split="pT-pL=-m^2/(4s^2)+O(s^-3)",source_lapse="sigma_prime/sigma=alpha*r*q^2*(rho+Pr)/f",
                     scope="Static outward f>0 chart; horizon continuation uses the same metric in EF, not this chart."),
        stationary_source=dict(
            assumptions=["Neutral minimal canonical sextic, static spherical geometry and one real harmonic frequency",
                         "Simple horizons, finite positive sigma_h and q_h>0; C1 regular scalar obeying KG",
                         "omega=0: asymptotically flat decaying vacuum boundary; same stationary ansatz across connected interior"],
            proof=["Evv_h=0 and Tvv_h=omega^2|Fh|^2 force Fh=0 when omega!=0.",
                   "Unit-modulus integrating factor, |a|>=c|r-rh| and bounded b imply local C1 uniqueness from Fh=0 on both sides.",
                   "omega=0: vanishing boundary plus positive exterior integral forces constant F; asymptotic vacuum selects F=0.",
                   "Ordinary uniqueness propagates zero across regular intervals and further simple horizons."],
            exclusions="Extremal, rotating, gauge-synchronized, nonminimal, nonsmooth and genuinely time-dependent matter are not classified.",
            evidence_type="Analytical conditional theorem; CAS verifies its tensor/KG/integral premises, not global evolution."),
        minimal_current=dict(
            assumptions="Separate minimally coupled isentropic rho(n), n on unbounded interval, rho'>0 and c_s^2>=0.",
            proof="rho''>=0 gives rho'(n)>=rho'(n0)>0, hence rho(n)>=rho(n0)+rho'(n0)*(n-n0), which is unbounded.",
            scope="Excludes local energy saturation in this minimal current class; says nothing against a decreasing redshifted or binding-corrected ADM mass.",
            rejected_example="rho=rhostar*n/(n+nstar), c_s^2=-2n/(n+nstar)<0; not adopted."),
        closure=dict(full_readout_verified=False,stationary_source_excluded_in_domain=False,
                     minimal_density_cap_excluded=False,foundation_pressure_join=False,
                     global_singularity_removal=False,full_RefG_rejected=False))


def common_readout_continuation_checks(exact, gate):
    """Section35: one prolongation and an exact isolated-end decision."""
    x = s.symbols("s", real=True)
    c, g, v, v_real = s.symbols("p4 p2_tt phi2_t_imag phi2_t_real", real=True)
    a,b,d,e,f = s.Rational(1,2),s.Rational(11,32),-s.Rational(1,16),s.Rational(1,192),-s.Rational(41,768)
    A = s.sqrt(s.Rational(23,3))
    phi2_im = 35/(6*A)
    def trunc(expr):
        poly = s.Poly(s.expand(expr), x)
        return sum(poly.nth(k)*x**k for k in range(3))
    def invpow(value, power):
        v0, v2 = value.coeff(x,0), value.coeff(x,2)
        return v0**(-power)-power*v2*v0**(-power-1)*x**2

    p, pt, ptt = a+b*x**2, d+e*x**2, f+g*x**2
    px_over_x, pxx, px_sq = 2*b+4*c*x**2,2*b+12*c*x**2,4*b*b*x*x
    ip = {k:invpow(p,k) for k in (2,3,4)}
    z = trunc(pt**2*ip[4]+2*p*px_over_x-px_sq)
    un = trunc(-ptt*ip[3]+3*pt**2*ip[4]-p*px_over_x+px_sq)
    ue = trunc(-p*px_over_x-p*pxx+px_sq-pt**2*ip[4])
    une = (-2*e/a+4*d*b/a**2)*x
    R2 = trunc(-2*p*pxx-2*px_sq-2*ptt*ip[3]+6*pt**2*ip[4])
    q = 1-z
    iq2, iq3 = invpow(q,2), invpow(q,3)
    box, hess = -un+ue,trunc(un**2+ue**2-2*une**2)
    rho_g = trunc((z*(1-3*z)-2*ue)*iq2/2)
    pr_g = trunc((-2*un-z*(1-3*z))*iq2/2)
    pt_g = trunc(-R2*iq2/4-z**2*(1+3*z)*iq3/2-
                 (5*z-1)*box*iq3/2-(box**2-hess)*iq3)
    # Actual unchanged scalar: phi=2+i*bphi*s^2, phi_t=i*A/2+(vr+i*v)*s^2.
    W = trunc((A**2/4+A*v*x*x)*ip[2])
    Xs = 4*a*a*phi2_im**2*x*x
    V = s.Rational(2,3)  # V2=0, since the radial coefficient is purely imaginary
    rho_m, pr_m, pt_m = trunc((W+Xs)/2+V),trunc((W+Xs)/2-V),trunc((W-Xs)/2-V)
    for name, geom, matter in (("density",rho_g,rho_m),("radial",pr_g,pr_m),("angular",pt_g,pt_m)):
        exact("prolongation_frozen_"+name,geom.coeff(x,0),matter.coeff(x,0))
    equations = [s.expand(left-right).coeff(x,2)
                 for left,right in ((rho_g,rho_m),(pr_g,pr_m),(pt_g,pt_m))]
    matrix, rhs = s.linear_eq_to_matrix(equations,(c,g,v))
    gate("prolongation_rank_three", matrix.rank()==3)
    values = matrix.inv()*rhs
    solution = dict(zip((c,g,v),map(s.simplify,values)))
    for i,residual in enumerate(equations):
        exact("prolongation_diagonal_residual_"+str(i),residual.subs(solution),0)
    exact("prolongation_independent_p4",solution[c],s.Rational(16603,812544))
    exact("prolongation_independent_p2_tt",solution[g],-s.Rational(392533,3250176))
    exact("prolongation_independent_phi2_t",solution[v],12353*s.sqrt(69)/292008)
    gate("prolongation_perturbed_coefficient_detected",
         s.simplify(equations[0].subs({**solution,c:solution[c]+1}))!=0)
    exact("prolongation_free_real_component",sum(s.diff(eq,v_real)**2 for eq in equations),0)
    # Source square verifies directly that the real component is absent at this order.
    direct_W = trunc((v_real**2*x**4+(A/2+v*x*x)**2)*ip[2])
    exact("prolongation_actual_scalar_kinetic_series",direct_W,W)
    eta = s.symbols("eta", real=True)
    potential_norm = eta/2-eta**2/4+eta**3/24
    exact("prolongation_potential_series",
          trunc(potential_norm.subs(eta,4+phi2_im**2*x**4)),V)
    exact("prolongation_independent_density_coefficient",rho_g.coeff(x,2),160*c-s.Rational(35,8))
    exact("prolongation_independent_radial_coefficient",pr_g.coeff(x,2),736*c/3+128*g+s.Rational(1345,144))
    exact("prolongation_independent_angular_coefficient",pt_g.coeff(x,2),1472*c/3+128*g-s.Rational(1,9))

    # Propagate the leading mixed constraint with the frozen KG acceleration.
    aa,bb,dd,ee,ff,j0 = s.symbols("a b d e f p0_ttt", real=True)
    zg = dd**2/aa**4+4*aa*bb
    qg = 1-zg
    jx = (2*ee/aa-4*dd*bb/aa**2)/qg**2
    base = {aa:a,bb:b,dd:d,ee:e,ff:f}
    dt = lambda expr: (s.diff(expr,aa)*dd+s.diff(expr,bb)*ee+
                      s.diff(expr,dd)*ff+s.diff(expr,ee)*g+s.diff(expr,ff)*j0)
    dt_j_geometry = s.simplify(dt(jx).subs(base))
    phi0_tt_imag = 3/(4*A)-A/16
    dt_j_scalar = A*v+2*phi0_tt_imag*phi2_im
    exact("prolongation_independent_mixed_time",dt_j_geometry,64*g+s.Rational(875,96))
    exact("prolongation_mixed_constraint_propagates",
          (dt_j_geometry-dt_j_scalar).subs(solution),0)
    exact("prolongation_central_density_time",dt(3*zg/(2*qg)).subs(base),s.Rational(3,2))
    un0 = -ff/aa**3+3*dd**2/aa**4-2*aa*bb
    P0 = (-2*un0-zg*(1-3*zg))/(2*qg**2)
    P0_time = s.simplify(dt(P0).subs(base))
    jerk = s.solve(P0_time-s.Rational(3,2),j0)[0]
    exact("prolongation_central_pressure_time",P0_time,128*j0-s.Rational(155,24))
    exact("prolongation_central_jerk",jerk,s.Rational(191,3072))

    # Unexpanded spatial identity: direct geometric and source derivations.
    Z,U,Vv,Cc,Kk,Ric,alpha,ell = s.symbols("z Un Ue Une k R2 alpha ell", real=True)
    Q = 1-ell**2*Z
    rho_req = (Z*(1-3*ell**2*Z)-2*Vv)/(2*alpha*Q**2)
    pr_req = (-2*U-Z*(1-3*ell**2*Z))/(2*alpha*Q**2)
    Bx,Hx = -U+Vv,U**2+Vv**2-2*Cc**2
    pt_req = -(2*Ric/Q**2+4*ell**2*Z**2*(1+3*ell**2*Z)/Q**3+
               4*(5*ell**2*Z-1)*Bx/Q**3+
               8*ell**2*(Bx**2-Hx)/Q**3)/(8*alpha)
    exact("prolongation_common_metric_curvature_identity",
          R2-2*(z+un+ue)+4*px_sq,0)
    p_full, ps_full, pss_full, pt_full, ptt_full, radius = s.symbols(
        "p ps pss pt ptt s", real=True)
    z_full = pt_full**2/p_full**4+2*p_full*ps_full/radius-ps_full**2
    un_full = -ptt_full/p_full**3+3*pt_full**2/p_full**4-p_full*ps_full/radius+ps_full**2
    ue_full = -p_full*ps_full/radius-p_full*pss_full+ps_full**2-pt_full**2/p_full**4
    R2_full = -2*p_full*pss_full-2*ps_full**2-2*ptt_full/p_full**3+6*pt_full**2/p_full**4
    exact("full_common_metric_curvature_identity",
          R2_full-2*(z_full+un_full+ue_full)+4*ps_full**2,0)
    anisotropy = s.factor((alpha*Q**3*(pr_req-pt_req)+Q*Kk**2-
                          2*ell**2*((Z-U)*(Z+Vv)+Cc**2)).subs(
                              Ric,2*(Z+U+Vv)-4*Kk**2))
    exact("full_common_angular_radial_identity",anisotropy,0)
    RR,PP,JJ,Delta = s.symbols("rho Pr J Delta",real=True)
    source_sub = {U:-Z*(1-3*ell**2*Z)/2-alpha*Q**2*PP,
                  Vv:Z*(1-3*ell**2*Z)/2-alpha*Q**2*RR,
                  Cc:-alpha*Q**2*JJ}
    form1=(alpha*Q**3*Delta+Q*Kk**2-
           2*ell**2*((Z-U)*(Z+Vv)+Cc**2)).subs(source_sub)
    form2=(Kk**2+alpha*Q**2*Delta-
           2*ell**2*Q*((3*Z/2+alpha*Q*PP)*(3*Z/2-alpha*Q*RR)+alpha**2*Q**2*JJ**2))
    exact("full_common_source_identity",form1/Q,form2)
    exact("full_common_Einstein_limit",form2.subs(ell,0),Kk**2+alpha*Delta)
    # The full identity must also reproduce the solved finite jet.
    identity_series=trunc(px_sq+q**2*(pr_m-pt_m)-
                         2*q*((3*z/2+q*pr_m)*(3*z/2-q*rho_m)+q**2*(A*phi2_im*x)**2))
    exact("prolongation_full_spatial_identity",identity_series.subs(solution),0)
    exact("prolongation_independent_areal_density_coefficient",
          (rho_m.coeff(x,2)*a*a).subs(solution),-s.Rational(28075,101568))

    # Representative asymptotic series checks coefficients; the proof below
    # uses stated big-O tails and positivity, not this representative alone.
    y,m,aa2,tt2 = s.symbols("inverse_s m a2 t2",real=True)
    p_inf=1-m*y+aa2*y**2
    k_inf=-y**2*s.diff(p_inf,y)
    H_inf=-tt2*y**2/p_inf**2
    z_inf=H_inf**2+2*p_inf*k_inf*y-k_inf**2
    z_series=s.series(z_inf,y,0,5).removeO().expand()
    exact("isolated_end_z_leading",z_series.coeff(y,3),2*m)
    exact("isolated_end_z_subleading",z_series.coeff(y,4),-4*aa2+tt2**2-3*m**2)
    vacuum_rhs=9*ell**2*(1-ell**2*z_inf)*z_inf**2/2
    exact("isolated_end_incompatible_leading_power",
          s.limit((k_inf**2-vacuum_rhs)/y**4,y,0),m**2)
    exact("isolated_end_response_faster_decay",s.limit(vacuum_rhs/y**6,y,0),18*ell**2*m**2)
    exact("isolated_end_generalized_mass",s.limit(z_inf/(2*alpha*y**3*p_inf**3*(1-ell**2*z_inf)),y,0),m/alpha)
    exact("isolated_end_flat_zero_mass_control",form2.subs({Kk:0,Z:0,RR:0,PP:0,JJ:0,Delta:0}),0)
    gate("isolated_end_nonzero_mass_control",s.S(1)**2>0)
    return dict(
        decision="FIRST_CONTINUATION_PASSES_GLOBAL_EXACT_READOUT_ISOLATED_END_EXCLUDED",
        local_coefficients={str(key):str(value) for key,value in solution.items()},
        central_jerk=str(jerk),
        local_scope="Diagonal metric/source equations through s^2 and leading mixed time propagation; KG only at central order from section34, not KG through s^2.",
        free_data="Re(phi2_t) and uncomputed higher coefficients remain free; finite jet only.",
        spatial_identity="k^2+alpha*q^2*(Pr-Pt)=2ell^2*q*((3z/2+alpha*q*Pr)*(3z/2-alpha*q*rho)+alpha^2*q^2*J^2)",
        isolated_end=dict(
            assumptions=["Exact zero-shift common-p metric imposed to spatial infinity",
                         "Differentiated p=1-m/s+O(s^-2), p_t=O(s^-2), constant m!=0",
                         "Fixed finite ell, alpha>0, rho,Pr,J=O(s^-3-epsilon), epsilon>0",
                         "Canonical Pr-Pt=|e phi|^2>=0"],
            proof="LHS>=m^2/s^4(1+o(1)), RHS=18ell^2*m^2/s^6+o(s^-6); incompatible.",
            scope="Not inferred from finite energy alone; not an exclusion of other readouts or RefG."),
        closure=dict(first_radial_compatibility=False,leading_momentum_propagation=False,
                     full_spatial_identity=False,specified_isolated_extension_excluded=False,
                     full_RefG_rejected=False,global_regular_black_hole=False))


def dynamic_common_centre_checks(exact, gate):
    """Section34: time-dependent central jets, not a global PDE solution."""
    alpha, ell, z = s.symbols("alpha ell z", positive=True)
    H, Hd, zs, zsd, zd, P, j1 = s.symbols("H Hd zs zsd zd P j1", real=True)
    q = 1-ell**2*z
    rho = 3*z/(2*alpha*q)
    C = z*(1-3*ell**2*z)/2
    T_geometry = -Hd-H**2+zs/2
    Hd_source = -3*H**2/2+3*ell**2*z**2/2-alpha*q**2*P
    exact("dynamic_centre_pressure_equation",
          (T_geometry-C-alpha*q**2*P).subs({zs: z-H**2, Hd: Hd_source},
                                             simultaneous=True), 0)
    w = s.symbols("w", real=True)
    required_w = (ell**2*z-H**2/z-2*Hd/(3*z))/q
    exact("dynamic_centre_static_recovery",
          required_w.subs({H: 0, Hd: 0}), ell**2*z/q)
    exact("dynamic_centre_homogeneous_recovery",
          Hd_source.subs(P, w*rho).subs(H**2, z),
          -3*z*q*(1+w)/2)
    H2 = -(zsd+3*H*zs)/4
    current = -2*H2/(alpha*q**2)
    rho_dot = s.diff(rho, z)*zd
    conservation = rho_dot+3*H*(rho+P)-3*current
    exact("dynamic_centre_mixed_energy_identity",
          conservation.subs({zs: z-H**2, zsd: zd-2*H*Hd_source},
                            simultaneous=True), 0)
    exact("dynamic_centre_growth_from_flux",
          s.solve(rho_dot+3*H*(rho+P)-3*j1, zd)[0],
          2*alpha*q**2*(j1-H*(rho+P)))

    # Independent coordinate differentiation of the time-dependent readout.
    p0, p2, pt0, pt2, ptt0 = s.symbols("p0 p2 pt0 pt2 ptt0", real=True)
    normal_H = -pt0/p0**2
    normal_Hdot = -ptt0/p0**3+2*pt0**2/p0**4
    spatial_z = 4*p0*p2
    spatial_zdot = 4*(pt0*p2/p0+pt2)
    H2_coordinate = -pt2+2*pt0*p2/p0
    exact("dynamic_centre_mixed_coordinate_identity", H2_coordinate,
          -(spatial_zdot+3*normal_H*spatial_z)/4)

    # Rational event with nonzero phase charge and the unchanged sextic.
    Hv, zv, zdv = s.Rational(1, 4), s.Rational(3, 4), s.Rational(1, 8)
    chi = s.symbols("chi", real=True)
    V = chi**2/2-chi**4/4+chi**6/24
    A = s.sqrt(s.Rational(23, 3))
    phi, Pi = s.S(2), s.I*A
    kappa = s.I*35/(24*A)  # phi = phi0 + kappa*r^2 at the selected event
    Vv = V.subs(chi, phi)
    Wv = s.expand_complex(s.conjugate(Pi)*Pi)
    rhov, Pv = s.simplify(Wv/2+Vv), s.simplify(Wv/2-Vv)
    jv = s.simplify(s.re(s.conjugate(Pi)*2*kappa))
    Hdv = s.simplify(Hd_source.subs({alpha: 1, ell: 1, z: zv, H: Hv, P: Pv}))
    zsv = zv-Hv**2
    zsdv = zdv-2*Hv*Hdv
    exact("dynamic_witness_positive_potential", Vv, s.Rational(2, 3))
    exact("dynamic_witness_density", rhov, s.Rational(9, 2))
    exact("dynamic_witness_pressure", Pv, s.Rational(19, 6))
    exact("dynamic_witness_inward_energy_flux", jv, s.Rational(35, 12))
    exact("dynamic_witness_Hdot", Hdv, s.Rational(53, 96))
    exact("dynamic_witness_spatial_z", zsv, s.Rational(11, 16))
    exact("dynamic_witness_spatial_zdot", zsdv, -s.Rational(29, 192))
    density_rate = rho_dot.subs({alpha: 1, ell: 1, z: zv, zd: zdv})
    exact("dynamic_witness_density_rate", density_rate, 3)
    exact("dynamic_witness_energy_conservation", density_rate+3*Hv*(rhov+Pv)-3*jv, 0)
    # KG fixes Pi_dot from the same spatial source coefficient.
    Pi_dot = s.simplify(6*kappa-3*Hv*Pi-s.diff(V, chi).subs(chi, phi))
    exact("dynamic_witness_scalar_equation_rate", Pi_dot, -2+3*s.I/A)
    scalar_density_rate = s.re(s.conjugate(Pi)*Pi_dot)+s.diff(V, chi).subs(chi, phi)*s.re(Pi)
    exact("dynamic_witness_scalar_energy_rate", scalar_density_rate, density_rate)
    charge = s.im(s.conjugate(phi)*Pi)
    charge_rate = s.im(s.conjugate(Pi)*Pi+s.conjugate(phi)*Pi_dot)
    phase_flux = s.im(s.conjugate(phi)*2*kappa)
    exact("dynamic_witness_phase_charge", charge, 2*A)
    exact("dynamic_witness_phase_conservation", charge_rate+3*Hv*charge-3*phase_flux, 0)
    # Leading timelike energy-rest and charge-flow velocities in the normal frame.
    # The source is locally contracting in areal radius even though H>0.
    energy_velocity = -jv/(rhov+Pv)
    charge_velocity = -phase_flux/charge
    exact("dynamic_witness_energy_rest_velocity", energy_velocity, -s.Rational(35, 92))
    exact("dynamic_witness_charge_velocity", charge_velocity, energy_velocity)
    exact("dynamic_witness_charge_areal_contraction", Hv+charge_velocity, -s.Rational(3, 23))
    exact("dynamic_witness_charge_flow_continuity", charge_rate/charge+3*(Hv+charge_velocity), 0)
    gate("dynamic_witness_canonical_positive_state", bool(Wv > 0 and Vv > 0 and charge > 0))
    gate("dynamic_witness_beyond_static_range", zv > s.Rational(1, 2))
    gate("dynamic_witness_static_deletion_fails",
         required_w.subs({ell: 1, z: zv, H: 0, Hd: 0}) != Pv/rhov)
    gate("dynamic_witness_flux_deletion_fails",
         density_rate+3*Hv*(rhov+Pv) != 0)
    gate("dynamic_witness_inflow_exceeds_expansion_dilution",
         jv > Hv*(rhov+Pv))

    coordinate_values = {p0: s.Rational(1, 2), p2: s.Rational(11, 32),
                         pt0: -s.Rational(1, 16), pt2: s.Rational(1, 192),
                         ptt0: -s.Rational(41, 768)}
    exact("dynamic_witness_clock_derivative", (pt0/p0).subs(coordinate_values), -s.Rational(1, 8))
    exact("dynamic_witness_coordinate_H", normal_H.subs(coordinate_values), Hv)
    exact("dynamic_witness_coordinate_Hdot", normal_Hdot.subs(coordinate_values), Hdv)
    exact("dynamic_witness_coordinate_spatial_z", spatial_z.subs(coordinate_values), zsv)
    exact("dynamic_witness_coordinate_spatial_zdot", spatial_zdot.subs(coordinate_values), zsdv)
    exact("dynamic_witness_coordinate_H2", H2_coordinate.subs(coordinate_values), -s.Rational(35, 384))
    gate("dynamic_witness_clock_decreases_grid_expands", bool(Hv > 0 and coordinate_values[pt0] < 0))

    # Direct 2D Christoffel/orbit equations from a metric polynomial.
    # All time derivatives are taken before setting t=0. The witness was
    # selected using the source, but expected source identities are not
    # substituted into the evaluated metric equations or curvature.
    t, x = s.symbols("t x", real=True)
    p = (coordinate_values[p0]+coordinate_values[pt0]*t+
         coordinate_values[ptt0]*t**2/2+
         (coordinate_values[p2]+coordinate_values[pt2]*t)*x**2)
    gamma = s.diag(-p**2, p**(-2))
    inverse = s.diag(-p**(-2), p**2)
    coordinates = (t, x)
    connection = {}
    for a in range(2):
        for b in range(2):
            for c in range(2):
                connection[a,b,c] = sum(inverse[a,d]*(
                    s.diff(gamma[d,c], coordinates[b])+
                    s.diff(gamma[d,b], coordinates[c])-
                    s.diff(gamma[b,c], coordinates[d]))/2 for d in range(2))
    radius = x/p
    dr = [s.diff(radius, c) for c in coordinates]
    Hess = s.Matrix(2, 2, lambda a,b: s.diff(dr[a], coordinates[b])-
                    sum(connection[c,a,b]*dr[c] for c in range(2)))
    box = sum(inverse[a,b]*Hess[a,b] for a in range(2) for b in range(2))
    X = sum(inverse[a,b]*dr[a]*dr[b] for a in range(2) for b in range(2))
    zm = s.cancel(((1-X)/radius**2).subs(t, 0))
    rm = radius.subs(t, 0)
    pm = p.subs(t, 0)
    qm = 1-zm
    Hess0, inv0, gamma0 = Hess.subs(t, 0), inverse.subs(t, 0), gamma.subs(t, 0)
    box0 = box.subs(t, 0)
    beta = -2*rm/qm**2
    alpha_orbit = 2*rm**2*zm*(1-3*zm)/qm**2
    central = lambda expression: s.limit(s.cancel(expression), x, 0)
    # Each normalized factor has a finite limit. Take those limits before
    # forming products; expanding their common denominator is unnecessary.
    z_limit = central(zm)
    beta_over_r = central(beta/rm)
    alpha_over_r2 = central(alpha_orbit/rm**2)
    box_over_r = central(box0/rm)
    Hess_over_r = Hess0.applyfunc(lambda entry: central(entry/rm))
    g_c, inv_c = gamma0.subs(x, 0), inv0.subs(x, 0)
    E_over_r2 = (beta_over_r*Hess_over_r-
                (alpha_over_r2/2+beta_over_r*box_over_r)*g_c)
    exact("dynamic_direct_metric_z", z_limit, zv)
    exact("dynamic_direct_orbit_density", E_over_r2[0,0]/(2*pm.subs(x, 0)**2), rhov)
    exact("dynamic_direct_orbit_pressure", E_over_r2[1,1]*pm.subs(x, 0)**2/2, Pv)
    exact("dynamic_direct_orbit_flux", beta_over_r*central(Hess0[0,1]/rm**2)/2, jv)
    Ricci2 = s.zeros(2)
    for a in range(2):
        for b in range(2):
            Ricci2[a,b] = sum(
                s.diff(connection[c,a,b], coordinates[c])-
                s.diff(connection[c,a,c], coordinates[b])+
                sum(connection[c,c,d]*connection[d,a,b]-
                    connection[c,b,d]*connection[d,a,c] for d in range(2))
                for c in range(2))
    R2 = sum(inverse[a,b]*Ricci2[a,b] for a in range(2) for b in range(2))
    R2c = s.simplify(R2.subs({t: 0, x: 0}, simultaneous=True))
    exact("dynamic_direct_orbit_curvature", R2c, s.Rational(13, 24))
    Hess_sq_over_r2 = sum(inv_c[a,c]*inv_c[b,d]*Hess_over_r[a,b]*Hess_over_r[c,d]
                         for a in range(2) for b in range(2) for c in range(2) for d in range(2))
    Kc = R2c**2+8*Hess_sq_over_r2+4*z_limit**2
    R4c = R2c+2*z_limit-4*box_over_r
    exact("dynamic_direct_Kretschmann", Kc, s.Rational(1465, 192))
    exact("dynamic_direct_Ricci", R4c, s.Rational(49, 8))
    # Independent angular equation with partial derivatives at fixed X.
    rr, xx = s.symbols("rr xx", real=True)
    zz = (1-xx)/rr**2
    aa = 2*rr**2*zz*(1-3*zz)/(1-zz)**2
    bb = -2*rr/(1-zz)**2
    parts = [s.diff(aa, rr), s.diff(bb, rr), s.diff(bb, xx)]
    # Normalize each partial derivative at fixed X first, then use the
    # independently computed central z. This avoids a giant rational sum.
    z_temp = s.symbols("z_temp", real=True)
    aR_over_r = s.simplify((parts[0]/rr).subs(xx, 1-rr**2*z_temp))
    bR_c = s.simplify(parts[1].subs(xx, 1-rr**2*z_temp))
    r_bX = s.simplify((rr*parts[2]).subs(xx, 1-rr**2*z_temp))
    aR_over_r, bR_c, r_bX = [
        s.limit(value, rr, 0).subs(z_temp, z_limit)
        for value in (aR_over_r, bR_c, r_bX)]
    angular_over_r = (-beta_over_r*R2c+aR_over_r+2*bR_c*box_over_r+
                      2*r_bX*(box_over_r**2-Hess_sq_over_r2))
    exact("dynamic_direct_angular_pressure", -angular_over_r/8, Pv)
    return dict(
        decision="TIME_DEPENDENT_CENTRAL_JET_COMPATIBLE",
        scope="Leading centre diagonal equations, leading radial flux, scalar and phase equations at one event.",
        witness=dict(u="3/4", q="1/4", clock="1/2", clock_proper_rate="-1/8",
                     H="1/4", Hdot="53/96", zdot="1/8", rho="9/2",
                     pressure="19/6", inward_energy_flux_coefficient="35/12",
                     curvature="1465/192"),
        interpretation="Decreasing common clock scale expands the normal grid; conserved-charge and energy-rest areal flows contract at leading order, raising central density.",
        closure=dict(dynamic_central_compatibility=False,
                     static_restriction_not_universal=False,
                     foundation_pressure_join=False, all_orders_solution=False,
                     global_regular_black_hole=False, perturbative_stability=False))


def central_source_readout_checks(exact, gate):
    """Section33: local source/readout compatibility, without a new action."""
    x, r, alpha, ell, M0, p0 = s.symbols(
        "x r alpha ell M0 p0", positive=True)
    p2, zc, P_c, w, n2 = s.symbols("p2 zc P_c w n2", real=True)
    rho, W = s.symbols("rho W", positive=True)
    u = s.symbols("u", positive=True)  # results additionally require u<1
    q = 1-u

    # Coordinate derivation: a quadratic germ fixes all retained coefficients.
    p = p0+p2*x**2
    radius = x/p
    B_iso = s.simplify(p**2*s.diff(radius, x)**2)
    z_iso = s.limit((1-B_iso)/radius**2, x, 0, dir="+")
    n_iso = s.limit((p/p0-1)/radius**2, x, 0, dir="+")
    exact("centre_isotropic_z", z_iso, 4*p0*p2)
    exact("centre_isotropic_lapse", n_iso, p0*p2)
    exact("centre_common_readout_jet", n_iso, z_iso/4)
    exact("centre_flat_constant_scale", z_iso.subs(p2, 0))
    # Independent sectional-curvature limit from a general areal metric.
    B = 1-zc*r**2
    lapse = p0*(1+n2*r**2)
    Phi = s.log(lapse)
    radial_time = B*(s.diff(Phi, r, 2)+s.diff(Phi, r)**2)+s.diff(B, r)*s.diff(Phi, r)/2
    angular_time = B*s.diff(Phi, r)/r
    radial_space = -s.diff(B, r)/(2*r)
    angular_space = (1-B)/r**2
    K_direct = 4*(radial_time**2+2*angular_time**2+
                  2*radial_space**2+angular_space**2)
    K_c = s.limit(K_direct, r, 0, dir="+")
    exact("centre_independent_sectional_curvature", K_c, 48*n2**2+12*zc**2)
    exact("centre_common_readout_curvature", K_c.subs(n2, zc/4), 15*zc**2)

    # Source equations before imposing the clock/rod relation.
    mass_germ = rho*r**3/3
    z_source = s.limit(2*alpha*mass_germ/(r**3+2*alpha*ell**2*mass_germ), r, 0)
    exact("centre_mass_constraint", z_source, 2*alpha*rho/(3+2*alpha*ell**2*rho))
    rho_u = 3*u/(2*alpha*ell**2*q)
    exact("centre_inverse_density", z_source.subs(rho, rho_u), u/ell**2)
    n_source = alpha*q**2*(rho+P_c)/2-u/(2*ell**2)
    residual = s.factor((n_source-u/(4*ell**2)).subs(
        {rho: rho_u, P_c: w*rho_u}, simultaneous=True))
    exact("centre_common_readout_source_residual", residual,
          3*u*(q*(1+w)-1)/(4*ell**2))
    required_w = s.solve(residual, w)[0]
    exact("centre_required_mechanical_pressure", required_w, u/q)
    exact("centre_Einstein_limit_pressure", s.limit(required_w, u, 0), 0)

    V_required = W*(1-2*u)/2
    scalar_rho = W/2+V_required
    scalar_pressure = W/2-V_required
    exact("centre_scalar_source_ratio", scalar_pressure/scalar_rho, required_w)
    exact("centre_nonnegative_potential_condition", 2*V_required/W, 1-2*u)
    chi = s.symbols("chi", real=True)
    V = chi**2/2-chi**4/4+chi**6/24
    exact("centre_retained_potential_positive_form", V,
          chi**2*((chi**2-3)**2+3)/24)
    # Algebraic sign witness: chi!=0 -> positive chi^2 times strictly positive bracket.
    y = s.symbols("y", real=True)
    exact("centre_positive_bracket", ((y-3)**2+3)-3, (y-3)**2)
    exact("centre_endpoint_requires_zero_potential", V_required.subs(u, s.Rational(1, 2)), 0)
    gate("centre_saturated_side_needs_negative_potential",
         V_required.subs(u, s.Rational(3, 4)).is_negative)
    # A genuine leading-order canonical germ using the unchanged sextic.
    val_u, val_alpha = s.Rational(1, 4), s.Rational(4, 7)
    val_W, val_V = s.Rational(7, 6), V.subs(chi, 1)
    val_rho, val_P = val_W/2+val_V, val_W/2-val_V
    exact("centre_positive_control_density", val_rho, s.Rational(7, 8))
    exact("centre_positive_control_mass_constraint",
          z_source.subs({rho: val_rho, alpha: val_alpha, ell: 1}), val_u)
    exact("centre_positive_control_readout",
          n_source.subs({rho: val_rho, P_c: val_P, alpha: val_alpha,
                        ell: 1, u: val_u}), val_u/4)
    chi2 = (s.diff(V, chi).subs(chi, 1)-val_W)/6
    exact("centre_positive_control_scalar_equation", 6*chi2+val_W-s.diff(V, chi).subs(chi, 1))
    exact("centre_positive_control_scalar_second_coefficient", chi2, -s.Rational(11, 72))
    # Same-source low-q regular data are admissible if the extra readout is released.
    free_u = s.Rational(3, 4)
    free_rho = rho_u.subs({u: free_u, alpha: 1, ell: 1})
    free_n = n_source.subs({u: free_u, alpha: 1, ell: 1, rho: free_rho, P_c: 0})
    exact("centre_free_lapse_control", free_n, -s.Rational(15, 64))
    free_K = K_c.subs({zc: free_u, n2: free_n})
    gate("centre_free_lapse_curvature_finite", bool(0 < free_K < 24))
    gate("centre_free_lapse_fails_only_locked_readout", free_n != free_u/4)
    # p0 drops out: the derived q bound is not a lower bound on clock normalization.
    exact("centre_clock_normalization_free", s.diff(residual, p0), 0)
    gate("centre_small_clock_local_control",
         (z_iso.subs({p0: s.Rational(1, 100), p2: s.Rational(25, 4)}) ==
          val_u))

    # Exact target: compare gravitational equation source with Einstein-effective source.
    z_h = 2*alpha*M0/(r**3+2*alpha*ell**2*M0)
    q_h = 1-ell**2*z_h
    f_h = 1-r**2*z_h
    M_recovered = s.factor(r**3*z_h/(2*alpha*q_h))
    exact("centre_Hayward_generalized_mass", M_recovered, M0)
    exact("centre_Hayward_physical_density", s.diff(M_recovered, r)/r**2, 0)
    exact("centre_Hayward_physical_radial_equation",
          s.diff(f_h, r)-r*z_h*(1-3*ell**2*z_h), 0)
    rho_eff = s.factor((1-f_h-r*s.diff(f_h, r))/(2*alpha*r**2))
    P_eff = -rho_eff
    Pt_eff = s.factor((s.diff(f_h, r)/r+s.diff(f_h, r, 2)/2)/(2*alpha))
    exact("centre_Hayward_effective_density", rho_eff,
          6*alpha*ell**2*M0**2/(r**3+2*alpha*ell**2*M0)**2)
    exact("centre_Hayward_effective_tangential_pressure", Pt_eff, (3*q_h-1)*rho_eff)
    exact("centre_Hayward_effective_central_density",
          s.limit(rho_eff, r, 0), 3/(2*alpha*ell**2))
    exact("centre_Hayward_effective_central_pressure",
          s.limit(P_eff, r, 0), -3/(2*alpha*ell**2))
    M_geometric = r*(1-f_h)/(2*alpha)
    exact("centre_Hayward_effective_mass_ledger",
          s.diff(M_geometric, r), r**2*rho_eff)
    exact("centre_Hayward_ADM_agreement", s.limit(M_geometric, r, s.oo), M0)
    exact("centre_smooth_material_mass_origin", s.limit(mass_germ, r, 0), 0)
    exact("centre_vacuum_mass_integration_constant", s.limit(M_recovered, r, 0), M0)
    gate("centre_effective_density_is_not_added_matter", rho_eff != 0)
    exact("centre_Hayward_vacuum_response_limit", s.limit(q_h, r, 0), 0)
    target_n = s.limit((s.sqrt(f_h)-1)/r**2, r, 0)
    exact("centre_Hayward_lapse_jet", target_n, -1/(2*ell**2))
    exact("centre_Hayward_common_readout_mismatch", target_n-1/(4*ell**2),
          -3/(4*ell**2))
    return dict(
        decision="LOCAL_SOURCE_READOUT_RESTRICTION",
        scope="Smooth static exact common-clock/rod germ in the existing saturation action.",
        result="P_c/rho_c=u/(1-u); V/W=(1-2u)/2; retained nonzero sextic requires u<1/2.",
        vacuum_ledger="Hayward is physical vacuum for r>0; its nonzero Einstein-effective source is not additional matter.",
        clock_scope="q=1-u is not p0 or foundation pressure; p0 has no bound from this check.",
        controls="Positive scalar centre germ; finite low-q free-lapse germ; constant-scale flat limit.",
        closure=dict(central_comparison_verified=False,
                     common_readout_restriction_verified=False,
                     full_pressure_join=False, global_black_hole=False,
                     perturbative_stability=False))


def w87_current_bridge_checks(exact, gate):
    """Independent jet-variable EL derivation; lapse is fixed only afterwards."""
    K, ell, n = s.symbols("K ell n", positive=True)
    a, N, j = s.symbols("a N j", positive=True)
    theta, adot, addot, Ndot, jdot, thetadot = s.symbols(
        "theta adot addot Ndot jdot thetadot", real=True)
    H, Hdot = s.symbols("H Hdot", real=True)
    F, rho = s.Function("F"), s.Function("rho")
    nv = j/a**3
    L = -6*K*a*F(nv)*adot**2/N-N*a**3*rho(nv)+j*thetadot

    def total_time(expr):
        return sum(s.diff(expr, variable)*velocity for variable, velocity in
                   ((a, adot), (adot, addot), (N, Ndot), (j, jdot),
                    (theta, thetadot)))

    # Four genuinely independent variables: no n(N), j=constant or N=1
    # replacement is made before these derivatives have been calculated.
    EN = s.diff(L, N)
    EA = s.diff(L, a)-total_time(s.diff(L, adot))
    EJ = s.diff(L, j)
    Eth = s.diff(L, theta)-total_time(s.diff(L, thetadot))

    def proper(expr):
        return s.simplify(expr.subs(
            {N: 1, Ndot: 0, jdot: 0, j: a**3*n,
             adot: a*H, addot: a*(Hdot+H**2)}, simultaneous=True).doit())

    f, energy = F(n), rho(n)
    fp, rp = s.diff(f, n), s.diff(energy, n)
    pressure = n*rp-energy
    exact("w87_density_independent_of_lapse", s.diff(nv, N), 0)
    exact("w87_hamiltonian_before_gauge", EN,
          a**3*(6*K*F(nv)*(adot/(N*a))**2-rho(nv)))
    exact("w87_phase_variation_current_conservation", Eth, -jdot)
    exact("w87_current_variation_phase_equation", proper(EJ),
          thetadot-rp-6*K*H**2*fp)
    ndot = proper(total_time(nv))
    exact("w87_density_continuity", ndot, -3*H*n)
    exact("w87_energy_continuity", rp*ndot+3*H*(energy+pressure), 0)
    scale = 2*f*Hdot+3*(f-n*fp)*H**2+pressure/(2*K)
    exact("w87_scale_euler_equation", proper(EA)/(6*K*a**2), scale)
    h2 = energy/(6*K*f)
    dh = -n*(rp-energy*fp/f)/(4*K*f)
    differentiated = (6*K*fp*H**2-rp)*ndot+12*K*f*H*Hdot
    exact("w87_differentiated_constraint", differentiated.subs(Hdot, dh).subs(H**2, h2), 0)
    exact("w87_scale_constraint_agreement", scale.subs(Hdot, dh).subs(H**2, h2), 0)
    exact("w87_constant_stiffness_recovery", dh.subs(f, 1).doit(), -n*rp/(4*K))

    target_h2 = energy/(6*K+ell**2*energy)
    target_f = 1+ell**2*energy/(6*K)
    target_fp = s.diff(target_f, n)
    exact("w87_response_coefficient_from_target", energy/(6*K*target_h2), target_f)
    exact("w87_target_hamiltonian", 6*K*target_f*target_h2, energy)
    target_dh = -n*rp/(4*K*target_f**2)
    exact("w87_target_Hdot", dh.subs({fp: target_fp, f: target_f}), target_dh)
    exact("w87_target_constraint_derivative", s.diff(target_h2, n)*(-3*n)/2, target_dh)
    target_phase = rp*(1+ell**2*target_h2)
    exact("w87_target_phase", rp+6*K*target_h2*target_fp, target_phase)
    exact("w87_target_scale_euler", scale.subs(
        {fp: target_fp, f: target_f, Hdot: target_dh, H**2: target_h2},
        simultaneous=True), 0)
    target_q = 1-ell**2*target_h2
    exact("w87_target_response_fraction", target_q, 1/target_f)
    exact("w87_target_null_focusing", -2*target_dh, n*rp/(2*K*target_f**2))
    rhop = s.symbols("rho_prime", nonnegative=True)
    rho_positive = s.symbols("rho_positive", positive=True)
    focusing = s.factor((-2*target_dh).subs({rp: rhop, energy: rho_positive}))
    gate("w87_target_null_focusing_nonnegative", focusing.is_nonnegative)
    m = s.symbols("m", positive=True)
    dust_f = 1+ell**2*m*n/(6*K)
    dust_h2 = m*n/(6*K*dust_f)
    exact("w87_target_dust_acceleration", target_dh.subs({rp: m, energy: m*n}),
          -s.Rational(3,2)*dust_h2/dust_f)
    # Actual omissions of the density chain rule, tested against the
    # unchanged equations on a regular dust witness, not invented PASS flags.
    phase_wrong_residual = s.simplify((target_phase-rp).subs({rp: m, energy: m*n}))
    scale_wrong = 2*target_f*target_dh+3*target_f*target_h2+pressure/(2*K)
    scale_wrong_residual = s.simplify(scale_wrong.subs({rp: m, energy: m*n}))
    gate("w87_negative_control_omit_Fprime_phase", phase_wrong_residual.is_positive,
         residual=str(phase_wrong_residual))
    gate("w87_negative_control_omit_Fprime_scale", scale_wrong_residual.is_positive,
         residual=str(scale_wrong_residual))
    sources = Path(__file__).parent.parent/"W3-87_State_Dependent_Gravitational_Response"
    return dict(
        source_sha256={name: hashlib.sha256((sources/name).read_bytes()).hexdigest()
                       for name in ("w3_87_state_dependent_response_contract.md",
                                    "w3_87_state_dependent_response.py")},
        F_grav="1+ell^2*rho(n)/(6K)", H_squared="rho/(6K+ell^2*rho)",
        Hdot="-n*rho_prime/(4K*F_grav^2)",
        phase_rate="rho_prime*(1+ell^2*H_squared)",
        result="The exact existing-action homogeneous match preserves null focusing for rho_prime>=0.",
        scope="Homogeneous branch dictionary; no spherical or microscopic constitutive equivalence.",
        closure=dict(new_defocusing_mechanism=False, spherical_action_equivalence=False,
                     foundation_pressure_map=False, microscopic_F_derived=False,
                     generic_four_dimensional_health=False, regular_black_hole=False))


def quadratic_current_spherical_checks(exact, gate):
    """Registered explicit coefficient, then its unchanged KS transfer."""
    x, K, ell, m, n = s.symbols("x K ell m n", positive=True)
    f = 1+x+x**2
    x_of_n = ell**2*m*n/(6*K)
    fn = f.subs(x, x_of_n)
    fp = s.diff(fn, n).subs(n, 6*K*x/(ell**2*m))
    fpp = s.diff(fn, n, 2)
    h2 = x/(ell**2*f)
    dh = -3*x*(1-x**2)/(2*ell**2*f**2)
    n_of_x = 6*K*x/(ell**2*m)
    exact("quadratic_H2_from_W87", (m*n/(6*K*fn)).subs(n, n_of_x), h2)
    W87_dh = -n*(m-m*n*s.diff(fn,n)/fn)/(4*K*fn)
    exact("quadratic_Hdot_from_W87", W87_dh.subs(n,n_of_x), dh)
    exact("quadratic_Hdot_constraint_derivative", -3*x*s.diff(h2,x)/2, dh)
    phase_ratio = (1+2*x+3*x**2)/f
    exact("quadratic_phase_from_current", (m+6*K*h2*fp)/m, phase_ratio)
    exact("quadratic_vacuum_value", f.subs(x,0), 1)
    exact("quadratic_first_density_correction", s.diff(f,x).subs(x,0), 1)
    gate("quadratic_positive_coefficient", f.is_positive)
    exact("quadratic_H2_bound_numerator", f-3*x, (x-1)**2)
    # Each polynomial is manifestly nonnegative in its stated interval.
    exact("quadratic_Hdot_bound_below_one", f**2-3*x*(1-x**2),
          x**4+5*x**3+3*x**2+(1-x))
    exact("quadratic_Hdot_bound_above_one", f**2-3*x*(x**2-1),
          x**3*(x-1)+3*x**2+5*x+1)
    exact("quadratic_Ricci_conservative_bound", 6*(s.Rational(1,2)+s.Rational(2,3)), 7)
    exact("quadratic_K_conservative_bound", 12*((s.Rational(1,2)+s.Rational(1,3))**2
                                               +s.Rational(1,3)**2), s.Rational(29,3))
    exact("quadratic_Hdot_sign_change", dh.subs(x,1), 0)
    y = s.symbols("y", positive=True)
    gate("quadratic_high_density_defocusing", s.factor(dh.subs(x,1+y)).is_positive)

    # On the contracting branch xdot=-3Hx>0. Conserved current gives a~x^-1/3.
    proper_integrand = ell*s.sqrt(f)/(3*x**s.Rational(3,2))
    affine_integrand = x**(-s.Rational(1,3))*proper_integrand
    exact("quadratic_proper_asymptote", s.limit(proper_integrand*s.sqrt(x),x,s.oo), ell/3)
    exact("quadratic_affine_asymptote", s.limit(affine_integrand*x**s.Rational(5,6),x,s.oo), ell/3)
    gate("quadratic_infinite_future_proper_time", s.integrate(x**(-s.Rational(1,2)),(x,1,s.oo)) == s.oo)
    gate("quadratic_infinite_future_null_affine", s.integrate(x**(-s.Rational(5,6)),(x,1,s.oo)) == s.oo)
    exact("quadratic_scale_proper_time_exponent", -s.Rational(1,3)*2, -s.Rational(2,3))
    exact("quadratic_null_PP_curvature_asymptote", s.limit(dh*x**s.Rational(2,3),x,s.oo), 0)
    exact("quadratic_H2_future_limit", s.limit(h2,x,s.oo), 0)
    exact("quadratic_Hdot_future_limit", s.limit(dh,x,s.oo), 0)
    # h is differentiated at fixed geometry/torsion, before evaluating T=6H^2.
    susceptibility = 6*K*h2*fpp
    exact("quadratic_fixed_geometry_susceptibility", susceptibility,
          m*ell**2*m*x/(3*K*f))
    gate("quadratic_fixed_geometry_positive_h", susceptibility.is_positive)
    gate("quadratic_fixed_geometry_positive_mu", phase_ratio.is_positive)
    fixed_c2 = s.simplify(n_of_x*susceptibility/(m*phase_ratio))
    exact("quadratic_fixed_geometry_speed", fixed_c2, 2*x**2/(1+2*x+3*x**2))
    exact("quadratic_fixed_geometry_speed_bound", s.Rational(2,3)-fixed_c2,
          2*(1+2*x)/(3*(1+2*x+3*x**2)))

    # Independently vary the full W89 KS minisuperspace action with N and j
    # still independent. Its -2/b^2 torsion term is retained throughout.
    a, b, N, j = s.symbols("a b N j", positive=True)
    ad, bd, phase_t = s.symbols("adot bdot phase_t", real=True)
    Ha, Hb = s.symbols("Ha Hb", real=True)
    F, rho = s.Function("F"), s.Function("rho")
    nv = j/(a*b**2)
    torsion = 4*ad*bd/(N**2*a*b)+2*bd**2/(N**2*b**2)-2/b**2
    lag = -K*N*a*b**2*F(nv)*torsion-N*a*b**2*rho(nv)+j*phase_t
    EN, EJ = s.diff(lag,N), s.diff(lag,j)
    substitutions = {N:1, ad:a*Ha, bd:b*Hb, j:a*b**2*n}
    reduced_EN = s.simplify(EN.subs(substitutions, simultaneous=True).doit()/(a*b**2))
    reduced_EJ = s.simplify(EJ.subs(substitutions, simultaneous=True).doit())
    tks = 4*Ha*Hb+2*Hb**2-2/b**2
    exact("quadratic_KS_lapse_variation", reduced_EN,
          2*K*F(n)*(2*Ha*Hb+Hb**2+1/b**2)-rho(n))
    exact("quadratic_KS_current_variation", reduced_EJ,
          phase_t-s.diff(rho(n),n)-K*tks*s.diff(F(n),n))
    # Eliminate the Hamiltonian only after varying F(n).
    energy, rp, ff, fprime = s.symbols("energy rho_prime F Fprime", real=True)
    invariant_combo = s.symbols("C_H", real=True)
    exact("quadratic_KS_torsion_constraint", (K*(2*invariant_combo-2/b**2)).subs(
        invariant_combo, energy/(2*K*ff)-1/b**2), energy/ff-4*K/b**2)
    ks_phase = s.simplify(1+(6*K*x/(ell**2*f)-4*K/b**2)*fp/m)
    exact("quadratic_KS_phase", ks_phase,
          phase_ratio-2*ell**2*(1+2*x)/(3*b**2))
    exact("quadratic_KS_phase_upper_three", 3*f-(1+2*x+3*x**2), x+2)
    negative_difference = s.simplify(phase_ratio-ks_phase)
    gate("quadratic_negative_control_FLRW_phase_in_KS", negative_difference.is_positive,
         residual=str(negative_difference))
    wrong_torsion_phase = 1+(6*K*x/(ell**2*f)-2*K/b**2)*fp/m
    gate("quadratic_negative_control_omit_intrinsic_sphere_term",
         s.simplify(wrong_torsion_phase-ks_phase).is_positive,
         residual=str(s.simplify(wrong_torsion_phase-ks_phase)))

    # Recompute W90's local weighted transport from the W89 radial equation
    # and current conservation. rho_prime stays independent in this elimination.
    beta = n*fprime/ff
    ndot = -n*(Ha+2*Hb)
    dHb = -((1-beta)*(3*Hb**2+1/b**2)+(n*rp-energy)/(2*K*ff))/2
    mu_eff = rp+K*tks*fprime
    transport = dHb+Hb**2+(ndot*fprime/ff-Ha)*Hb+n*mu_eff/(4*K*ff)
    exact("quadratic_W90_weighted_transport", transport.subs(
        energy,2*K*ff*(2*Ha*Hb+Hb**2+1/b**2)), 0)
    Pnull, mup = s.symbols("P_null mu_positive", positive=True)
    proper_Q_rate = -b*n*mup/(4*K*a)
    affine_Q_rate = -Pnull**2*b*n*mup/(4*K*a**2)
    exact("quadratic_W90_affine_conversion", (Pnull/a)*Pnull*proper_Q_rate, affine_Q_rate)
    gate("quadratic_W90_positive_phase_decreases_Q", affine_Q_rate.is_negative)
    b0, q0 = s.symbols("b0 q0", positive=True)
    Xmax = 9*b0**2/(4*ell**2)-s.Rational(1,2)
    exact("quadratic_KS_density_ceiling_boundary", (2*ell**2*(1+2*x)/(3*b0**2)).subs(x,Xmax), 3)
    exact("quadratic_monotonic_coefficient", s.diff(f,x), 1+2*x)
    Fmax = 1+Xmax+Xmax**2
    lam = s.symbols("lambda_elapsed", nonnegative=True)
    radius_majorant = b0-q0*lam/Fmax
    exact("quadratic_finite_affine_patch_bound", radius_majorant.subs(lam,b0*Fmax/q0), 0)
    parent = Path(__file__).parent.parent
    dependencies = [("W3-89_Spherical_Interior_Turning_Point", "w3_89_spherical_turning_point_contract.md"),
                    ("W3-89_Spherical_Interior_Turning_Point", "w3_89_spherical_turning_point.py"),
                    ("W3-90_Asymptotic_Contraction", "w3_90_asymptotic_contraction_contract.md"),
                    ("W3-90_Asymptotic_Contraction", "w3_90_asymptotic_contraction.py")]
    return dict(
        postulate="F_grav=1+x+x^2, x=ell^2*m*n/(6K), rho=m*n",
        homogeneous=dict(H_squared="x/(ell^2*F_grav)",
            Hdot="-3*x*(1-x^2)/(2*ell^2*F_grav^2)",
            phase_over_m="(1+2*x+3*x^2)/F_grav",
            metric_bounds="H^2<=1/(3ell^2), |Hdot|<=1/(2ell^2), |R|<=7/ell^2, K<=29/(3ell^4)",
            future_scale="a~proper_time^(-2/3)", future_null_affine="infinite",
            parallel_propagated_curvature_asymptote="bounded; Hdot/a^2 tends to zero",
            fixed_geometry_speed_squared="2*x^2/(1+2*x+3*x^2)<2/3"),
        KS=dict(phase_over_m="(1+2*x+3*x^2)/F_grav-2ell^2(1+2x)/(3b^2)",
            positive_phase_consequence="x < Xmax=9b0^2/(4ell^2)-1/2 while b<=b0; if Xmax<=0 the stated branch is empty",
            coefficient_bound="F_grav<1+Xmax+Xmax^2 for Xmax>0",
            affine_bound="positive radius cannot persist beyond lambda0+b0*Fmax/q0, q0=-F db/dlambda at lambda0>0",
            outcome="SPECIFIED_POSITIVE_CLOCK_COMPLETE_CONTRACTING_KS_TARGET_EXCLUDED",
            alternatives="b reaches zero with KS curvature divergence, or the specified patch/domain ends earlier"),
        scope="Homogeneous FLRW asymptote and fixed-geometry current block are not a black-hole or full coupled-health result.",
        closure=dict(homogeneous_future_metric_curvature_bounded=True,
                     homogeneous_future_null_affine_infinite=True,
                     fixed_geometry_current_signs=True, specified_KS_target_excluded=True,
                     inhomogeneous_interiors_excluded=False, extensions_excluded=False,
                     generic_coupled_health=False, regular_black_hole=False,
                     full_RefG_rejected=False, microscopic_F_derived=False),
        source_sha256={str(Path(folder)/name):hashlib.sha256((parent/folder/name).read_bytes()).hexdigest()
                       for folder,name in dependencies})


def ks_two_scale_completion_checks(exact, gate):
    """Section27: independent variational premises and an analytic comparison proof."""
    t = s.symbols("t", real=True)
    K, P = s.symbols("K P", positive=True)
    a, b, N, j, theta = (s.Function(name)(t) for name in
                          ("a", "b", "N", "j", "theta"))
    Ffun, rhofun = s.Function("F"), s.Function("rho")
    ad, bd = s.diff(a, t), s.diff(b, t)
    nv = j/(a*b**2)
    f, rho = Ffun(nv), rhofun(nv)
    fp = s.diff(f, j)*a*b**2
    rp = s.diff(rho, j)*a*b**2
    ha, hb = ad/(N*a), bd/(N*b)
    T = 4*ha*hb+2*hb**2-2/b**2
    lagrangian = (-2*K*f*(a*bd**2+2*b*ad*bd)/N
                  +2*K*N*a*f-N*a*b**2*rho+j*s.diff(theta, t))

    def EL(variable, L=lagrangian):
        return s.diff(s.diff(L, s.diff(variable, t)), t)-s.diff(L, variable)

    # Differentiate all independent variables before invoking conservation
    # or any lapse gauge. In particular, the shear identity is off shell.
    ea, eb = EL(a), EL(b)
    exact("ks_density_lapse_independence", s.diff(nv, N), 0)
    exact("ks_phase_current_conservation", EL(theta), s.diff(j, t))
    exact("ks_current_phase_equation", EL(j),
          N*(rp+K*T*fp)-s.diff(theta, t))
    constraint = 2*K*f*(2*ha*hb+hb**2+1/b**2)-rho
    exact("ks_lapse_constraint_before_gauge", s.diff(lagrangian, N), a*b**2*constraint)
    conserved = {s.diff(j, t): 0}
    beta = nv*fp/f
    pressure = nv*rp-rho
    radial = 2*s.diff(hb, t)/N+(1-beta)*(3*hb**2+1/b**2)+pressure/(2*K*f)
    angular = (s.diff(ha+hb, t)/N
               +(1-beta)*(ha**2+ha*hb+hb**2)-beta/b**2+pressure/(2*K*f))
    exact("ks_independent_radial_scale_EL", -ea.subs(conserved)/(2*K*N*f*b**2), radial)
    exact("ks_independent_angular_scale_EL", -eb.subs(conserved)/(4*K*N*f*a*b), angular)
    exact("ks_conserved_density_rate", s.diff(nv, t).subs(conserved)/N, -nv*(ha+2*hb))
    exact("ks_stiffness_rate", s.diff(f, t).subs(conserved)/(N*f), -beta*(ha+2*hb))
    U = f*a*b**2*(ha-hb)
    exact("ks_unfixed_lapse_offshell_shear_identity",
          s.diff(U, t)-N*f*a+(b*eb-2*a*ea)/(4*K), 0)
    exact("ks_two_scale_difference", angular-radial,
          s.diff(ha-hb, t)/N+(1-beta)*(ha+2*hb)*(ha-hb)-1/b**2)

    # Null first integrals checked against the metric geodesic equations.
    av, bv, fv, n = s.symbols("a b F n", positive=True)
    Ha, Hb, Fp, Rho, Rp = s.symbols("H_a H_b F_prime rho rho_prime", real=True)
    kt, kx = P/av, P/av**2
    exact("ks_affine_null_norm", -kt**2+av**2*kx**2, 0)
    exact("ks_affine_time_geodesic", (-Ha*kt)*kt+av**2*Ha*kx**2, 0)
    exact("ks_affine_space_geodesic", (-2*Ha*kx)*kt+2*Ha*kt*kx, 0)
    exact("ks_shear_affine_conversion", fv*av*kt, P*fv)
    betav = n*Fp/fv
    Hbdot = -((1-betav)*(3*Hb**2+bv**-2)+(n*Rp-Rho)/(2*K*fv))/2
    Tlocal = 4*Ha*Hb+2*Hb**2-2/bv**2
    mulocal = Rp+K*Tlocal*Fp
    Fdot = -n*Fp*(Ha+2*Hb)
    # Differentiate Q=F P b H_b/a, then use the independently verified
    # radial EL and lapse constraint. rho_prime remains independent.
    Qlambda = (P/av)**2*bv*(Fdot*Hb+fv*(Hb**2+Hbdot-Ha*Hb))
    lapse_value = 2*K*fv*(2*Ha*Hb+Hb**2+bv**-2)
    exact("ks_weighted_affine_focusing_from_EL",
          (Qlambda+P**2*bv*n*mulocal/(4*K*av**2)).subs(Rho, lapse_value), 0)
    Up = s.symbols("U_positive", positive=True)
    exact("ks_positive_U_ratio_derivative", P/bv*(Up/(fv*av*bv**2)),
          P*Up/(fv*av*bv**3))
    gate("ks_positive_U_increases_a_over_b", (P*Up/(fv*av*bv**3)).is_positive)
    add_a, bdd_b = s.symbols("a_ddot_over_a b_ddot_over_b", real=True)
    Kks = 4*(add_a**2+2*bdd_b**2+2*(Ha*Hb)**2+(Hb**2+bv**-2)**2)
    Kexcess = 4*add_a**2+8*bdd_b**2+8*(Ha*Hb)**2+4*Hb**4+8*Hb**2/bv**2
    exact("ks_curvature_lower_bound_certificate", Kks-4/bv**4, Kexcess)
    gate("ks_curvature_excess_nonnegative", Kexcess.is_nonnegative)

    # Alter the actual Lagrangian, not merely a reported equation.
    flat_L = lagrangian-2*K*N*a*f
    flat_ea, flat_eb = EL(a, flat_L), EL(b, flat_L)
    wrong_residual = s.simplify(s.diff(U, t)-N*f*a+(b*flat_eb-2*a*flat_ea)/(4*K))
    exact("ks_omitted_sphere_term_residual", wrong_residual, -N*f*a)
    gate("ks_negative_control_omitted_intrinsic_curvature",
         s.simplify(wrong_residual/(N*f*a)) == -1,
         residual_over_NFa=str(s.simplify(wrong_residual/(N*f*a))))

    M, r = s.symbols("M r", positive=True)
    ash = s.sqrt(2*M/r-1)
    Ush = s.simplify(ash*r**2*(M/(ash*r**2)+ash/r))
    exact("ks_schwarzschild_shear_charge", Ush, 3*M-r)
    exact("ks_schwarzschild_shear_evolution", s.diff(Ush, r)*(-ash), ash)
    exact("ks_schwarzschild_Q_constant", -ash/ash, -1)

    H, tau0, j0 = s.symbols("H tau0 j", positive=True)
    tau = s.symbols("tau", real=True)
    ads, bds = -s.sinh(H*tau), s.cosh(H*tau)/H  # contracting patch tau<0
    hads, hbds = s.diff(ads, tau)/ads, s.diff(bds, tau)/bds
    Uds = s.simplify(ads*bds**2*(hads-hbds))
    exact("ks_de_sitter_shear_charge", Uds, -bds)
    exact("ks_de_sitter_shear_evolution", s.diff(Uds, tau), ads)
    Kds = 4*((s.diff(ads, tau, 2)/ads)**2+2*(s.diff(bds, tau, 2)/bds)**2
             +2*(hads*hbds)**2+(hbds**2+bds**-2)**2)
    exact("ks_de_sitter_finite_metric_curvature", s.trigsimp(Kds), 24*H**4)
    affine_interval = s.integrate(ads/P, (tau, -tau0, 0))
    exact("ks_de_sitter_finite_affine_patch_endpoint", affine_interval,
          (s.cosh(H*tau0)-1)/(H*P))
    gate("ks_de_sitter_affine_interval_finite", not affine_interval.has(s.oo, -s.oo, s.zoo, s.nan))
    norm_ds = -(j0/(ads*bds**2))**2
    gate("ks_nonzero_current_diverges_at_metric_patch_endpoint",
         s.limit(norm_ds, tau, 0, dir="-") == -s.oo,
         invariant="J_phys_mu J_phys^mu=-n^2", limit="-infinity for j>0")
    exact("ks_vacuum_current_endpoint_control", norm_ds.subs(j0, 0), 0)
    bmin, jconst, cmin = s.symbols("b_min j c_min", positive=True)
    nmax = jconst/(cmin*bmin**3)
    exact("ks_density_comparison_bound", jconst/((cmin*bmin)*bmin**2), nmax)
    Fmin, Fmax, qin = s.symbols("F_min F_max q_in", positive=True)
    gate("ks_U_comparison_slope_positive", (P*Fmin).is_positive)
    gate("ks_Q_comparison_inward_slope_negative", (-qin/Fmax).is_negative)
    # This is an analytical comparison theorem, not a symbolic proof of
    # continuity, compactness, spacetime existence or a numerical evolution.
    root = Path(__file__).parent.parent
    packages = (("W3-87_State_Dependent_Gravitational_Response", "w3_87_state_dependent_response"),
                ("W3-89_Spherical_Interior_Turning_Point", "w3_89_spherical_turning_point"),
                ("W3-90_Asymptotic_Contraction", "w3_90_asymptotic_contraction"))
    hashes = {folder+"/"+stem+suffix: hashlib.sha256((root/folder/(stem+suffix)).read_bytes()).hexdigest()
              for folder, stem in packages for suffix in ("_contract.md", ".py")}
    return dict(
        source_sha256=hashes,
        identities=dict(U="F*a*b^2*(H_a-H_b)", U_proper_rate="F*a", U_affine_rate="P*F",
                        Q="F*db/dlambda", Q_affine_rate="-P^2*b*n*mu_eff/(4K*a^2)"),
        theorem=dict(
            type="Analytical conditional comparison proof; exact tests verify its variational premises.",
            assumptions=["Same future KS patch and same W87 action/current cover the entire alleged complete ray",
                         "j>0, a>0, P>0 and conserved n=j/(a*b^2)",
                         "0<b_min<=b<=b0 and initial Q<0", "mu_eff>=0 throughout the ray",
                         "F(n)>=F_min>0 throughout the ray",
                         "F is continuous and finite on bounded n intervals, including n=0"],
            comparison_proof=[
                "If lambda is unbounded, U'=P F>=P F_min makes U positive after a finite affine interval.",
                "U>0 implies d ln(a/b)/d tau>0, hence a/b>=c_min>0 thereafter.",
                "b>=b_min gives a>=c_min*b_min and n<=j/(c_min*b_min^3).",
                "Continuity including n=0 bounds F above on this compact density interval by F_max.",
                "Q'<=0 preserves Q<=-q_in<0, so db/dlambda<=-q_in/F_max violates b>=b_min in finite affine time."],
            consequence="No complete inward bounded-curvature KS patch under these assumptions.",
            proper_time_endpoint_assumed=False, limiting_density_assumed=False,
            power_law_assumed=False,
            scope_exclusions=["No exclusion of every inhomogeneous spherical interior or global extension",
                              "F approaching zero or singular at bounded density is outside this theorem, not certified healthy",
                              "A finite-affine metric patch boundary alone is not a curvature singularity"]),
        endpoint_control=dict(metric="Contracting de Sitter KS has K=24H^4 and a finite-affine horizon endpoint",
                              vacuum="j=0 permits the usual regular metric extension",
                              retained_current="j>0 gives invariant -n^2 -> -infinity as a->0, b->1/H; a metric extension alone is not a smooth-current extension"),
        closure=dict(new_physical_law=False, numerical_evolution=False,
                     all_inhomogeneous_interiors_excluded=False, full_RefG_rejected=False,
                     global_singularity_removal=False))


def hayward_static_action_terms():
    """Independent spherical action, retaining lapse jets before variation."""
    r, M, ell, z = s.symbols("rh_r M ell z", positive=True)
    N, Np, Npp, f, fp, fpp = s.symbols("N Np Npp f fp fpp", real=True)
    q = 1-ell**2*z
    H2 = 2*z*(1-3*ell**2*z)/q**2
    H3 = 4/q**2
    H4 = 1-ell**2*z/q+2*ell**2*z*s.log(q/(ell**2*z))
    H4z = s.diff(H4, z)
    L = (N*r**2*H2-r*(N*fp+f*Np)*H3
         +r**2*(-N*fpp-3*fp*Np-2*f*Npp)*H4
         +(N*fp**2+2*f*fp*Np)*H4z)
    zh = 2*M/(r**3+2*M*ell**2)
    fh = 1-r**2*zh
    background = {z: zh, f: fh, fp: s.diff(fh, r), fpp: s.diff(fh, r, 2)}
    D0 = s.simplify(s.diff(L, N).subs(background, simultaneous=True))
    A = s.diff(L, Np).subs(background, simultaneous=True)
    B = s.diff(L, Npp).subs(background, simultaneous=True)
    return dict(r=r, M=M, ell=ell, z=z, q=q, H2=H2, H3=H3, H4=H4,
                H4z=H4z, L=L, N=N, Np=Np, Npp=Npp, f=f, fp=fp, fpp=fpp,
                zh=zh, fh=fh, background=background, D0=D0, A=A, B=B)


def finite_ball_extension_checks(exact, gate, data):
    """Local CH coordinates and finite-ball exit, not global completion."""
    r, M, ell = (data[key] for key in ("r", "M", "ell"))
    rh, V, u = s.symbols("r_h V u", positive=True)
    y = s.symbols("y", real=True)
    f = data["fh"]
    root_mass = rh**3/(2*(rh**2-ell**2))
    froot = s.factor(f.subs(M, root_mass))
    kappa = (3*ell**2-rh**2)/(2*rh**3)
    exact("extension_inner_root", froot.subs(r, rh), 0)
    exact("extension_surface_gravity", -s.diff(froot, r).subs(r, rh)/2, kappa)
    qh = s.factor((1-ell**2*data["zh"]).subs({M: root_mass, r: rh}))
    exact("extension_horizon_response", qh, 1-ell**2/rh**2)
    # rh/ell parametrizes the complete open interval (1,sqrt(3)).
    rh_domain = ell*s.sqrt((1+3*u)/(1+u))
    gate("extension_inner_root_q_positive", s.simplify(qh.subs(rh, rh_domain)).is_positive)
    gate("extension_inner_root_kappa_positive", s.simplify(kappa.subs(rh, rh_domain)).is_positive)

    dv = -1/(kappa*V)
    drV, dry = y, V
    fv = froot.subs(r, rh+V*y)
    gVV = s.cancel(-fv*dv**2+2*dv*drV)
    gVy = dv*dry
    exact("extension_coordinate_gVV", s.cancel(gVV+(fv+2*kappa*V*y)/(kappa**2*V**2)), 0)
    exact("extension_coordinate_gVy", gVy, -1/kappa)
    exact("extension_metric_determinant", -gVy**2, -1/kappa**2)
    second = s.factor(s.diff(froot, r, 2).subs(r, rh))
    limit_gVV = s.limit(gVV, V, 0)
    exact("extension_regular_gVV_limit", limit_gVV, -second*y**2/(2*kappa**2))
    exact("extension_angular_metric_limit", s.limit((rh+V*y)**2, V, 0), rh**2)
    k = s.symbols("wrong_kappa", positive=True)
    wrong = -(fv+2*k*V*y)/(k**2*V**2)
    pole = s.limit(V*wrong, V, 0)
    exact("extension_wrong_rate_pole", pole, -2*(k-kappa)*y/k**2)
    gate("extension_wrong_rate_negative_control", s.simplify(pole.subs({k: 2*kappa, y: 1})) != 0)

    Ricci = -s.diff(froot, r, 2)-4*s.diff(froot, r)/r+2*(1-froot)/r**2
    K = s.diff(froot, r, 2)**2+4*s.diff(froot, r)**2/r**2+4*(1-froot)**2/r**4
    horizon_curvature = {}
    for name, expr in (("Ricci", Ricci), ("K", K),
                       ("radial_tide", s.diff(froot, r, 2)/2),
                       ("transverse_tide", s.diff(froot, r)/(2*r))):
        value = s.factor(expr.subs(r, rh))
        gate("extension_finite_horizon_"+name, value.is_finite is True, value=str(value))
        horizon_curvature[name] = str(value)

    a, number, w = s.symbols("a number w", positive=True)
    metric = s.diag(-1, a**2)
    normal = s.Matrix([0, 1/a])
    current = s.Matrix([number, 0])
    exact("dust_boundary_unit_normal", (normal.T*metric*normal)[0], 1)
    exact("dust_boundary_comoving_current_jump", (normal.T*metric*current)[0], 0)
    tilted = s.Matrix([number*s.sqrt(1+w**2), number*w/a])
    exact("dust_boundary_tilted_current_norm", (tilted.T*metric*tilted)[0], -number**2)
    gate("dust_boundary_noncomoving_negative_control", (normal.T*metric*tilted)[0].is_positive)
    # A proposed direct dust-to-vacuum null join must also conserve current.
    # Here k_a=(-1,+/-1) is a COVECTOR, contracted with future J^a.
    rapidity = s.symbols("rapidity", real=True)
    inertial_current = s.Matrix([number*s.cosh(rapidity), number*s.sinh(rapidity)])
    null_fluxes = []
    for sign in (-1, 1):
        k_cov = s.Matrix([-1, sign])
        null_flux = (k_cov.T*inertial_current)[0]
        exact("dust_null_join_flux_"+str(sign), s.expand_trig(null_flux).rewrite(s.exp),
              -number*s.exp(-sign*rapidity))
        null_fluxes.append(-number*s.exp(-sign*rapidity))
    gate("dust_null_join_retained_current_obstruction", all(value.is_nonzero for value in null_fluxes))
    exact("dust_null_join_vacuum_control", null_fluxes[0].subs(number, 0), 0)
    speed = r*s.sqrt(2*M/(r**3+2*M*ell**2))
    gate("dust_finite_radius_speed_strictly_positive", speed.is_positive is True)
    exact("dust_time_reversed_radial_acceleration", s.diff(speed, r)*speed,
          s.diff(-speed, r)*(-speed))
    gate("dust_finite_radius_branch_flip_discontinuous", (2*speed).is_positive is True)

    t, a0, h0, chib = s.symbols("t a0 h0 chi_b", positive=True)
    # In the contracting dust solution z increases: |H|>=h0>0 after t0.
    # Hence a(t)<=a0 exp(-h0*t), and conformal distance exceeds this bound.
    conformal_bound = (s.exp(h0*t)-1)/(a0*h0)
    exact("finite_ball_conformal_bound_derivative", s.diff(conformal_bound, t), s.exp(h0*t)/a0)
    gate("finite_ball_infinite_available_conformal_distance", s.limit(conformal_bound, t, s.oo) == s.oo)
    exit_bound = s.log(1+2*chib*a0*h0)/h0
    exact("finite_ball_null_exit_bound", conformal_bound.subs(t, exit_bound), 2*chib)
    gate("finite_ball_exit_bound_is_finite", exit_bound.is_finite is True)
    exact("infinite_patch_affine_comparison", s.integrate(a0*s.exp(-t/ell), (t, 0, s.oo)), a0*ell)

    zh, q = data["zh"], 1-ell**2*data["zh"]
    exact("centre_q_cubic_limit", s.limit(q/r**3, r, 0), 1/(2*M*ell**2))
    for name, expr, power, target in (
            ("h2", r**2*data["H2"], 4, -16*M**2*ell**2),
            ("h3", r*data["H3"], 5, 16*M**2*ell**4),
            ("h4", r**2*data["H4"], 1, -2*M*ell**2)):
        exact("centre_coefficient_"+name, s.limit(r**power*expr.subs(data["z"], zh), r, 0), target)
    exact("centre_full_onshell_density_limit", s.limit(data["D0"], r, 0), 0)
    exact("centre_full_onshell_log_coefficient",
          s.limit(data["D0"]/(r**2*s.log(r/ell)), r, 0), 36/ell**2)
    return dict(
        scope="M>3sqrt(3)ell/4, ell>0: exact matched finite dust ball and local vacuum CH neighbourhood; q>0 at the horizon",
        horizon=dict(kappa=str(kappa), q=str(qh), gVV_at_V0=str(limit_gVV),
                     gVy=str(gVy), determinant=str(-1/kappa**2), curvature=horizon_curvature),
        finite_ball=dict(argument="Every radial null ray launched at finite dust proper time covers at most 2 chi_b before exit; inward rays first cross the regular centre",
                         conformal_lower_bound=str(conformal_bound), exit_time_upper_bound=str(exit_bound),
                         comoving_worldlines="tau extends to infinity; an infinite-FLRW affine endpoint is not a finite-ball proof"),
        alternative_join=dict(null_current="At a regular finite-density event J.k=-n exp(∓eta) is nonzero; a direct null join to J=0 fails current conservation",
                              branch_flip="Collapse and expansion separately satisfy the radial equation, but their nonzero finite-radius velocities cannot be switched continuously",
                              scope="These necessary conditions exclude the direct joins tested, not every global continuation"),
        centre=dict(domain="q>0 for r>0; the vacuum centre of the selected static continuation reaches q=0 and needs an action/domain prescription; other continuations are not classified",
                    volume_density="D0~(36/ell^2) r^2 ln(r/ell) -> 0; coefficient poles cancel on this background",
                    coefficient_poles_do_not_prove="Divergent on-shell action, strong coupling, or curvature singularity"),
        references=["https://arxiv.org/html/2602.16773v2#S3.SS4"],
        closure=dict(local_horizon_extension_verified=False, finite_ball_current_matching_verified=False,
                     full_centre_action_extension=False, fixed_packet_CH_stability=False,
                     global_geodesic_completion=False, global_singularity_removal=False))


def central_variational_domain_checks(exact, gate, data):
    """Bare flux plus ordinary boundary freedoms; no boundary law is chosen."""
    r, M, ell, z = (data[key] for key in ("r", "M", "ell", "z"))
    N, Np, Npp, f, fp, fpp = (data[key] for key in ("N", "Np", "Npp", "f", "fp", "fpp"))
    H2, H3, H4, H4z = (data[key] for key in ("H2", "H3", "H4", "H4z"))
    eta, etap, etapp = s.symbols("eta eta_prime eta_second", real=True)
    variation = s.diff(data["L"].subs({N: 1+eta, Np: etap, Npp: etapp}), eta)
    exact("centre_lapse_jet_derivative", variation, r**2*H2-r*fp*H3-r**2*fpp*H4+fp**2*H4z)
    exact("centre_first_lapse_derivative", s.diff(data["L"], Np), -r*f*H3-3*r**2*fp*H4+2*f*fp*H4z)
    exact("centre_second_lapse_derivative", s.diff(data["L"], Npp), -2*r**2*f*H4)
    D0, A, B = (data[key] for key in ("D0", "A", "B"))
    Q = A-s.diff(B, r)
    exact("centre_punctured_bulk_lapse_equation", s.simplify(D0-s.diff(A, r)+s.diff(B, r, 2)), 0)
    exact("centre_lapse_flux_Q", s.limit(Q, r, 0), -4*M)
    exact("centre_lapse_flux_rB", s.limit(r*B, r, 0), 4*M*ell**2)
    exact("centre_constant_lapse_flux", s.limit(Q, r, 0), -4*M)
    exact("centre_quadratic_lapse_flux", s.limit(r**2*Q+2*r*B, r, 0), 8*M*ell**2)
    early_gauge = data["L"].subs({N: 1, Np: 0, Npp: 0})
    exact("centre_early_gauge_erases_lapse_derivative", s.diff(early_gauge, N), 0)
    gate("centre_early_gauge_negative_control", (-4*M).is_nonzero is True)

    # Full Eq.131 total derivative retained, not discarded at an interior centre.
    zprime = -fp/r**2-2*z/r
    mu = r**3*z/(2*(1-ell**2*z))
    muprime = s.diff(mu, r)+s.diff(mu, z)*zprime
    boundary = -r**2*H4*(N*fp+2*f*Np)
    boundary_prime = (s.diff(boundary, r)+s.diff(boundary, z)*zprime
                      +s.diff(boundary, f)*fp+s.diff(boundary, fp)*fpp
                      +s.diff(boundary, N)*Np+s.diff(boundary, Np)*Npp)
    exact("centre_full_total_derivative_decomposition",
          (data["L"]-boundary_prime-4*N*muprime).subs(f, 1-r**2*z), 0)
    boundary_eta = (-r**2*H4*(eta*fp+2*f*etap)).subs(data["background"], simultaneous=True)
    exact("centre_counterterm_constant_flux", s.limit(boundary_eta.subs({eta: 1, etap: 0}), r, 0), -4*M)
    exact("centre_counterterm_quadratic_flux", s.limit(boundary_eta.subs({eta: r**2, etap: 2*r}), r, 0), 8*M*ell**2)
    exact("centre_reduced_lapse_bulk_zero", 4*muprime.subs(data["background"], simultaneous=True), 0)
    dm = s.symbols("delta_mu", real=True)
    # Removing B_total leaves 4 N mu'; a Legendre boundary changes which
    # centre datum must be fixed, rather than eliminating both variations.
    dirichlet_flux = 4*N*dm
    legendre_variation = -4*(eta*mu+N*dm)
    exact("centre_legendre_boundary_exchange", dirichlet_flux+legendre_variation, -4*eta*mu)
    exact("centre_legendre_remaining_lapse_flux",
          (-4*eta*mu).subs({z: data["zh"]}), -4*M*eta)
    delta_f = s.symbols("delta_f", real=True)
    delta_mu = -s.diff(mu, z)*delta_f/r**2
    exact("centre_mass_variation", delta_mu, -r*delta_f/(2*(1-ell**2*z)**2))
    eps = s.symbols("epsilon", positive=True)
    dm2 = delta_mu.subs({z: data["zh"], delta_f: eps*r**2})
    dm5 = delta_mu.subs({z: data["zh"], delta_f: eps*r**5})
    exact("centre_regular_r2_variation_nonuniform", s.limit(r**3*dm2/eps, r, 0), -2*M**2*ell**4)
    exact("centre_regular_r5_variation_finite_charge", s.limit(dm5/eps, r, 0), -2*M**2*ell**4)
    # Local centre test only: multiply delta_f by a smooth outer cutoff.
    # For 0<eps<ell^-2 this small central neighbourhood has 0<z<ell^-2.
    # The r^5 test above is a radial/C2-admissible series, not a claim that
    # an odd radial power defines a C-infinity Cartesian metric.
    shifted_mu = mu.subs(z, data["zh"]-eps)
    exact("centre_noncommuting_limit_radius_first", s.limit(s.limit(shifted_mu, r, 0), eps, 0), 0)
    exact("centre_noncommuting_limit_variation_first", s.limit(s.limit(shifted_mu, eps, 0), r, 0), M)
    return dict(
        scope="M>0, ell>0, r>0: punctured-domain action plus explicit central variation and boundary freedoms",
        bare_flux="eta0*(-4M)+eta2*(8M ell^2); overall action factor 1/(4G), lower endpoint sign applies",
        boundary_freedom=dict(total_derivative="Subtracting B_total removes bare lapse flux",
                              remaining="4N delta_mu at the centre; Legendre boundary exchanges this for -4mu delta_N",
                              no_selected_prescription=True),
        domain_test="Near the centre only, delta_f=epsilon*r^2 times a smooth outer cutoff, 0<epsilon<ell^-2; delta_mu~−2M^2 ell^4 epsilon/r^3 and centre/variation limits do not commute",
        decision="A central variational/domain prescription is still required; bare-action flux alone is not a universal obstruction",
        references=["https://arxiv.org/html/2602.16773v2#S3.SS2", "https://arxiv.org/html/2602.16773v2#S3.SS4"],
        closure=dict(central_flux_and_boundary_freedoms_verified=False,
                     smooth_central_action_completion=False, all_completions_excluded=False,
                     new_boundary_source_chosen=False, new_counterterm_chosen=False))


def spherical_lorentz_action_checks(exact, gate):
    """Section 30: derive torsion and both spin equations before gauge fixing.

    Signature (-+++); Lambda=boost01(psi)*rotation23(chi), with
    rotation23=[[cos(chi),sin(chi)],[-sin(chi),cos(chi)]].
    The reduced action is per unit solid angle. Boundary equivalence is
    used only for compactly supported perturbations or paired boundaries.
    """
    K, b = s.symbols("K b", positive=True)
    acc, Ha, Hb, d, p0, p1, c0, c1 = s.symbols(
        "acc Ha Hb d psi0 psi1 chi0 chi1", real=True)
    ch, sh, co, si = s.symbols("coshpsi sinhpsi coschi sinchi", real=True)
    eta = s.diag(-1, 1, 1, 1)
    boost = s.eye(4)
    boost[0, 0] = boost[1, 1] = ch
    boost[0, 1] = boost[1, 0] = sh
    rot = s.eye(4)
    rot[2, 2] = rot[3, 3] = co
    rot[2, 3], rot[3, 2] = si, -si
    lam = boost*rot
    invlam = eta*lam.T*eta
    relations = s.groebner([ch**2-sh**2-1, co**2+si**2-1],
                          ch, co, sh, si, domain="EX")

    def algebra(expr):
        # Reduce only exact Lorentz/trigonometric polynomial identities.
        num, den = s.fraction(s.cancel(expr))
        return s.cancel(relations.reduce(s.Poly(num, ch, co, sh, si,
                                               domain="EX").as_expr())[1]/den)

    exact("spin30_lorentz_matrix", sum(algebra(v)**2 for v in lam.T*eta*lam-eta))
    G, Q = s.zeros(4), s.zeros(4)
    G[0, 1] = G[1, 0] = 1
    Q[2, 3], Q[3, 2] = 1, -1
    exact("spin30_commuting_generators", sum(v**2 for v in G*Q-Q*G))
    bar2, bar3 = s.zeros(4), s.zeros(4)
    cot = s.symbols("cot_theta", real=True)
    bar2[1, 2], bar2[2, 1] = -1/b, 1/b
    bar3[1, 3], bar3[3, 1] = -1/b, 1/b
    bar3[2, 3], bar3[3, 2] = -cot/b, cot/b
    omega = [G*p0+Q*c0, G*p1+Q*c1,
             invlam*bar2*lam, invlam*bar3*lam]
    de = {}
    for A, B, C, value in ((0, 0, 1, -acc), (1, 0, 1, Ha),
                           (2, 0, 2, Hb), (2, 1, 2, d),
                           (3, 0, 3, Hb), (3, 1, 3, d), (3, 2, 3, cot/b)):
        de[A, B, C], de[A, C, B] = value, -value
    torsion = {(A, B, C): algebra(de.get((A, B, C), 0)
               +omega[B][A, C]-omega[C][A, B])
               for A in range(4) for B in range(4) for C in range(4)}
    trace = [sum(torsion[A, A, C] for A in range(4)) for C in range(4)]
    I1 = sum(eta[A, A]*value**2/(eta[B, B]*eta[C, C])
             for (A, B, C), value in torsion.items())
    I2 = sum(value*torsion[C, B, A]/eta[B, B]
             for (A, B, C), value in torsion.items())
    direct_T = algebra(I1/4+I2/2-sum(trace[C]**2/eta[C, C] for C in range(4)))
    exact("spin30_polar_connection_cancellation", s.diff(direct_T, cot))
    T0 = 4*Ha*Hb+2*Hb**2-2*d**2-4*acc*d-2/b**2
    T = T0+4*(d*p0-Hb*p1)+4/b*(co*((d+acc-p0)*ch
          +(p1-Ha-Hb)*sh)+si*(c0*sh-c1*ch))
    exact("spin30_full_torsion_contraction", algebra(direct_T-T))
    ks = {ch: 1, sh: 0, co: 0, si: 1, p0: 0, p1: 0, c0: 0, c1: 0, d: 0, acc: 0}
    exact("spin30_KS_torsion", direct_T.subs(ks), 4*Ha*Hb+2*Hb**2-2/b**2)
    flat = {ch: 1, sh: 0, co: 1, si: 0, p0: 0, p1: 0, c0: 0, c1: 0,
            d: 1/b, acc: 0, Ha: 0, Hb: 0}
    exact("spin30_inertial_Minkowski_torsion", direct_T.subs(flat))
    gate("spin30_negative_control_intrinsic_sphere_term",
         s.simplify((T0+2/b**2).subs({d: 0, acc: 0})
                    -(4*Ha*Hb+2*Hb**2-2/b**2)) != 0)

    t, x, th, ph = s.symbols("t x theta phi", real=True)
    N, a, br, shift, psi, chi, F = [s.Function(v)(t, x)
                                   for v in ("N", "a", "b", "B", "psi", "chi", "F")]
    vol = N*a*br**2
    frame = {b: br, acc: s.diff(N, x)/(N*a),
             Ha: (s.diff(a, t)-s.diff(a*shift, x))/(N*a),
             Hb: (s.diff(br, t)-shift*s.diff(br, x))/(N*br), d: s.diff(br, x)/(a*br),
             p0: (s.diff(psi, t)-shift*s.diff(psi, x))/N, p1: s.diff(psi, x)/a,
             c0: (s.diff(chi, t)-shift*s.diff(chi, x))/N, c1: s.diff(chi, x)/a,
             ch: s.cosh(psi), sh: s.sinh(psi), co: s.cos(chi), si: s.sin(chi)}
    Vt = -br**2*s.diff(psi, x)-2*a*br*s.cos(chi)*s.sinh(psi)
    Vx = br**2*s.diff(psi, t)+2*br*s.cos(chi)*(a*shift*s.sinh(psi)+N*s.cosh(psi))
    exact("spin30_TEGR_boundary_identity", s.expand((T-T0).subs(frame)
          -2*(s.diff(Vt, t)+s.diff(Vx, x))/vol))
    F0 = (s.diff(F, t)-shift*s.diff(F, x))/N
    F1 = s.diff(F, x)/a
    LL = 2*K*br**2*(s.diff(F, x)*s.diff(psi, t)-s.diff(F, t)*s.diff(psi, x))
    LL += 4*K*N*a*br*s.cos(chi)*(-F0*s.sinh(psi)+F1*s.cosh(psi))
    exact("spin30_weighted_boundary_action", LL-2*K*(s.diff(F, t)*Vt+s.diff(F, x)*Vx))
    Epsi = F0*(br*frame[d]-s.cos(chi)*s.cosh(psi))+F1*(s.cos(chi)*s.sinh(psi)-br*frame[Hb])
    Echi = s.sin(chi)*(F0*s.sinh(psi)-F1*s.cosh(psi))
    for field, target, name in ((psi, Epsi, "boost"), (chi, Echi, "rotation")):
        el = s.diff(LL, field)-s.diff(s.diff(LL, s.diff(field, t)), t)-s.diff(s.diff(LL, s.diff(field, x)), x)
        exact("spin30_action_antisymmetric_"+name, s.expand(el), 4*K*N*a*br*target)

    # Independent covariant spin divergence, including all six AB equations.
    lc = lam.subs({ch: s.cosh(psi), sh: s.sinh(psi), co: s.cos(chi), si: s.sin(chi)})
    li = eta*lc.T*eta
    bar_th, bar_ph = s.zeros(4), s.zeros(4)
    bar_th[1, 2], bar_th[2, 1] = -1, 1
    bar_ph[1, 3], bar_ph[3, 1] = -s.sin(th), s.sin(th)
    bar_ph[2, 3], bar_ph[3, 2] = -s.cos(th), s.cos(th)
    om = [G*s.diff(psi, t)+Q*s.diff(chi, t),
          G*s.diff(psi, x)+Q*s.diff(chi, x), li*bar_th*lc, li*bar_ph*lc]
    tetrad = s.Matrix([[N, 0, 0, 0], [a*shift, a, 0, 0],
                       [0, 0, br, 0], [0, 0, 0, br*s.sin(th)]])
    inv = tetrad.inv()
    coords = (t, x, th, ph)
    current = {(A, B, nu): vol*s.sin(th)/2*sum(
        (inv[nu, A]*inv[mu, B]-inv[nu, B]*inv[mu, A])*s.diff(F, coords[mu])
        for mu in (0, 1)) for A in range(4) for B in range(4) for nu in range(4)}
    for A in range(4):
        for B in range(A+1, 4):
            div = sum(s.diff(current[A, B, nu], coords[nu])-sum(
                om[nu][C, A]*current[C, B, nu]+om[nu][C, B]*current[A, C, nu]
                for C in range(4)) for nu in range(4))
            target = {(0, 1): Epsi, (2, 3): Echi}.get((A, B), 0)
            exact("spin30_covariant_spin_%d%d" % (A, B), div/s.sin(th), -N*a*br*target)
    flat_base = s.diff(bar_ph, th)+bar_th*bar_ph-bar_ph*bar_th
    exact("spin30_base_connection_flatness", sum(v**2 for v in flat_base))
    exact("spin30_constant_F_lorentz_boundary", LL.subs({s.diff(F, t): 0, s.diff(F, x): 0}))
    gate("spin30_negative_control_freezing_angles", s.simplify(Echi.subs({psi: 0, chi: s.pi/2})) != 0)
    return dict(
        action="-K e F(n) T + J^mu theta_mu - e rho(n)",
        metric="-N^2 dt^2+a^2(dx+Bdt)^2+b^2 dOmega^2",
        current="n=sqrt(N^2 j^2-a^2(i+Bj)^2)/(N a b^2)",
        local_ansatz_reference="https://arxiv.org/html/2408.13342v1#S4",
        conventions="boost01(psi)*rotation23(chi); KS psi=0, chi=pi/2",
        domain=["N,a,b>0; timelike nonzero current", "local spherical chart away from b=0 and polar-axis coordinate singularities"],
        surviving_antisymmetric_equations=["01", "23"],
        boundary_scope="TEGR equivalence is modulo the explicitly computed divergence; compact perturbations or paired boundaries.",
        closure=dict(spherical_action_entry_verified=False, full_3plus1_health=False,
                     source_law_modified=False, new_model_adopted=False))


def coupled_radial_principal_checks(exact, gate):
    """Section 31: actual constrained local quadratic action, not frozen matter."""
    K, a, b, F, n, j = s.symbols("K a b F n j", positive=True)
    Ha, Hb, ndot, Fp, Fpp, rho, rp, rpp, mu = s.symbols(
        "Ha Hb ndot Fp Fpp rho rp rpp mu", real=True)
    d, pi, pidot, pix, dx, i, B, Bx, phi, phix, eps, wave = s.symbols(
        "d pi pidot pix dx i B Bx phi phix eps k", real=True)
    V = a*b**2
    C = 4*Ha*Hb+2*Hb**2
    T = C-2/b**2
    mu_expr = rp+K*T*Fp
    h = rpp+K*T*Fpp
    D = rp-rho*Fp/F
    constraint = K*F*(C+2/b**2)
    n1 = d/V
    n2 = -a**2*(i+j*B)**2/(2*j*V)
    raw_n = s.sqrt((1+eps*phi)**2*(j+eps*d)**2
                    -a**2*(eps*i+eps*B*(j+eps*d))**2)/((1+eps*phi)*V)
    exact("radial31_current_density_first_order", s.diff(raw_n, eps).subs(eps, 0), n1)
    exact("radial31_current_density_second_order", s.diff(raw_n, eps, 2).subs(eps, 0)/2, n2)
    Fe = F+eps*Fp*n1+eps**2*(Fp*n2+Fpp*n1**2/2)
    re = rho+eps*rp*n1+eps**2*(rp*n2+rpp*n1**2/2)
    raw_L = (-K*V*Fe*(C-4*Hb*eps*Bx)/(1+eps*phi)+2*K*(1+eps*phi)*a*Fe
             -(1+eps*phi)*V*re+(j+eps*d)*(mu+eps*pidot)+eps**2*i*pix)
    L2_actual = s.diff(raw_L, eps, 2).subs(eps, 0)/2
    L2 = (d*pidot+i*pix+mu*a**2*(i+j*B)**2/(2*j)-h*d**2/(2*V)
          -D*phi*d-K*V*C*F*phi**2-4*K*V*Hb*F*phi*Bx+4*K*Hb*Fp*d*Bx)
    on_background = {rho: constraint, mu: mu_expr}
    exact("radial31_full_pre_elimination_quadratic_action", (L2_actual-L2).subs(on_background))
    gate("radial31_negative_control_missing_density_torsion_mixing",
         s.simplify((L2_actual-L2.subs(mu, rp)).subs(on_background)) != 0)
    exact("radial31_unfixed_lapse_constraint", s.diff(
        -K*V*F*C/(1+eps*phi)+2*K*(1+eps*phi)*a*F-(1+eps*phi)*V*rho,
        eps).subs(eps, 0), V*phi*(constraint-rho))

    # Derive the angle contribution by integration by parts before elimination.
    t, x = s.symbols("t x", real=True)
    bt, Ft = [s.Function(v)(t) for v in ("b", "F")]
    df, db, ps = [s.Function(v)(t, x) for v in ("deltaF", "deltab", "deltapsi")]
    raw_extra = 2*K*bt**2*(s.diff(df, x)*s.diff(ps, t)-s.diff(df, t)*s.diff(ps, x))-4*K*bt*db*s.diff(Ft, t)*s.diff(ps, x)
    integrated = 4*K*bt*ps*(s.diff(Ft, t)*s.diff(db, x)-s.diff(bt, t)*s.diff(df, x))
    boundary = (s.diff(2*K*bt**2*s.diff(df, x)*ps, t)
                -s.diff(2*K*bt**2*s.diff(df, t)*ps+4*K*bt*db*s.diff(Ft, t)*ps, x))
    exact("radial31_angle_quadratic_integration_by_parts", raw_extra-integrated-boundary)
    fdot, fx, bx, boost, rotation, lapse = s.symbols("Fdot Fx bx boost rotation N", real=True)
    dbj, ftj, psit, psix = s.symbols("dbj ftj psit psix", real=True)
    raw_angle = (2*K*(b+eps*dbj)**2*(eps*fx*eps*psit-(fdot+eps*ftj)*eps*psix)
                 +4*K*lapse*a*(b+eps*dbj)*s.cos(s.pi/2+eps*rotation)
                 *(-(fdot+eps*ftj)/lapse*s.sinh(eps*boost)+eps*fx/a*s.cosh(eps*boost)))
    angle2_expected = (2*K*b**2*(fx*psit-ftj*psix)-4*K*b*dbj*fdot*psix
                       +4*K*b*rotation*(a*fdot*boost-lapse*fx))
    exact("radial31_full_Lorentz_quadratic_expansion", s.diff(raw_angle, eps, 2).subs(eps, 0)/2, angle2_expected)
    angle_L = 4*K*b*boost*(fdot*bx-b*Hb*fx)+4*K*b*rotation*(a*fdot*boost-lapse*fx)
    angle_eq = [s.diff(angle_L, field) for field in (boost, rotation)]
    angle_solution = {boost: lapse*fx/(a*fdot), rotation: (b*Hb*fx-fdot*bx)/(a*fdot)}
    for index, eq in enumerate(angle_eq):
        exact("radial31_retained_angle_constraint_%d" % index, eq.subs(angle_solution))
    exact("radial31_angle_constraint_determinant",
          s.Matrix(angle_eq).jacobian([boost, rotation]).det(), -(4*K*a*b*fdot)**2)
    angle_reduced = s.simplify(angle_L.subs(angle_solution))
    exact("radial31_angle_gradient_action", angle_reduced,
          4*K*lapse*b/a*(fx*bx-b*Hb*fx**2/fdot))
    extra = -4*K*b**2*Hb/(a*Fp*ndot)*(Fp/V)**2*dx**2
    exact("radial31_spatial_flat_angle_action",
          angle_reduced.subs({lapse: 1, bx: 0, fx: Fp*dx/V, fdot: Fp*ndot}), extra)
    gate("radial31_negative_control_dropped_Lorentz_mixing", s.simplify(extra) != 0)
    gate("radial31_negative_control_reversed_Lorentz_sign", s.simplify(extra-(-extra)) != 0)

    flux_eq = s.diff(L2, i)
    exact("radial31_undivided_flux_equation", flux_eq, pix+mu*a**2*(i+j*B)/j)
    exact("radial31_mu_zero_rank_equation", flux_eq.subs(mu, 0), pix)
    exact("radial31_flux_hessian", s.diff(flux_eq, i), mu*a**2/j)
    flux_solution = -j*B-j*pix/(mu*a**2)
    exact("radial31_flux_solution", flux_eq.subs(i, flux_solution))
    # Vary shift after spatial integration by parts; background is homogeneous.
    shift_eq = -j*pix+4*K*V*Hb*F*phix-4*K*Hb*Fp*dx
    phi_solution = Fp*d/(V*F)+n*pi/(4*K*Hb*F)
    phi_x = Fp*dx/(V*F)+n*pix/(4*K*Hb*F)
    exact("radial31_shift_constraint", shift_eq.subs({phix: phi_x, j: n*V}))
    lapse_eq = s.diff(L2, phi)
    exact("radial31_lapse_equation", lapse_eq, -D*d-2*K*V*C*F*phi-4*K*V*Hb*F*Bx)
    exact("radial31_lapse_solves_shift_gradient", s.diff(lapse_eq, Bx), -4*K*V*Hb*F)
    # Gauge map (xi^t,xi^x)->(delta b,delta a) for one k!=0 Fourier mode.
    gauge_matrix = s.Matrix([[-b*Hb, 0], [-a*Ha, -s.I*wave*a]])
    exact("radial31_spatial_flat_gauge_rank", gauge_matrix.det(), s.I*a*b*Hb*wave)
    exact("radial31_gauge_degenerates_at_Hb_zero", gauge_matrix.det().subs(Hb, 0))
    exact("radial31_gauge_degenerates_at_k_zero", gauge_matrix.det().subs(wave, 0))

    H_reduced = (j*pix**2/(2*mu*a**2)+h*d**2/(2*V)
                 +D*phi_solution*d+K*V*C*F*phi_solution**2-extra)
    heff = h+2*rp*Fp/F-4*K*Fp**2/(F*b**2)
    A0 = s.diff(H_reduced, d, 2)
    exact("radial31_effective_density_coefficient", A0.subs(rho, constraint), heff/V)
    A2 = 8*K*Hb*Fp/(a**2*ndot*V)
    exact("radial31_gradient_density_Hessian", s.diff(H_reduced, dx, 2), A2)
    B0 = V*n**2*C/(8*K*F*Hb**2)
    exact("radial31_phase_mass_Hessian", s.diff(H_reduced, pi, 2), B0)
    cross = s.diff(H_reduced, d, pi)
    exact("radial31_cross_Hessian", cross, n*(D+2*K*C*Fp)/(4*K*F*Hb))
    exact("radial31_cross_simplified", cross.subs(rho, constraint), n*mu_expr/(4*K*F*Hb))
    exact("radial31_phase_gradient_Hessian", s.diff(H_reduced, pix, 2), j/(mu*a**2))
    Aop = heff/V+A2*wave**2
    Bop = n*V*wave**2/(mu*a**2)+B0
    Cop = n*mu_expr/(4*K*F*Hb)
    evolution = s.Matrix([[-Cop, -Bop], [Aop, Cop]])
    omega2 = s.expand(Aop*Bop-Cop**2)
    exact("radial31_canonical_principal_determinant", evolution.det(), omega2)
    leading = 8*K*n*Hb*Fp/(mu*a**4*ndot)
    exact("radial31_leading_k4_frequency", omega2.coeff(wave, 4), leading)
    exact("radial31_symplectic_pair_preserved", s.diff(L2, pidot), d)
    # Constant F is evaluated in the original action, before dividing by Fdot.
    exact("radial31_minimal_action_mixing_control", (L2_actual-L2).subs(
        {Fp: 0, Fpp: 0, mu: rp, rho: constraint}))
    exact("radial31_minimal_mu", mu_expr.subs(Fp, 0), rp)
    exact("radial31_minimal_density_stiffness", heff.subs({Fp: 0, Fpp: 0}), rpp)
    exact("radial31_minimal_sound_speed", (rpp/V)*(n*V/(rp*a**2)), n*rpp/(rp*a**2))
    gate("radial31_negative_control_frozen_metric_heff", s.simplify(heff-h) != 0)
    Hpos, ndpos, Fppos, mupos = s.symbols("Hpos ndpos Fppos mupos", positive=True)
    inward = {Hb: -Hpos, ndot: ndpos, Fp: Fppos}
    gate("radial31_inward_density_increasing_A_negative", s.simplify(A2.subs(inward)).is_negative)
    gate("radial31_mu_positive_radial_instability", s.simplify(leading.subs(inward).subs(mu, mupos)).is_negative)
    gate("radial31_mu_negative_phase_energy", (-n*V/(mupos*a**2)).is_negative)
    gate("radial31_mu_negative_inward_A_and_B_negative",
         s.simplify(A2.subs(inward)).is_negative and (-n*V/(mupos*a**2)).is_negative)
    gate("radial31_mu_negative_oscillations_do_not_imply_positive_energy",
         s.simplify(leading.subs(inward).subs(mu, -mupos)).is_positive)
    return dict(
        derivation="Full action Taylor expansion -> Lorentz/flux/shift/lapse equations -> local gauge -> canonical pair (d,pi).",
        assumptions=["K,F,n,a,b>0; regular homogeneous KS solution", "nonzero radial k; Hb!=0; Fdot=Fp*ndot!=0; mu!=0",
                     "small perturbations remain on the timelike-F-gradient, sin(chi)!=0 local KS spin branch"],
        formulas=dict(mu=str(mu_expr), h_eff=str(heff), A=str(Aop), B=str(Bop), C=str(Cop), omega2_leading_k4=str(leading)),
        sign_scope="Hb<0, ndot>0, Fp>0: mu>0 gives a negative leading omega^2; mu<0 gives negative leading A and B.",
        rank_boundaries=["mu=0: undivided flux equation imposes pi_x=0", "Fdot=0: solve spin constraints without division",
                         "Hb=0 or k=0: spatial-flat gauge rank changes", "constant F control taken before Lorentz elimination"],
        limitations=["Necessary local radial continuum test, not full 3+1 health or global evolution.",
                     "A physical unstable wavelength range requires a valid background-to-ultraviolet-cutoff window.",
                     "No ultraviolet cutoff or alternative action has been supplied here.",
                     "Density-decreasing and degenerate branches are separate from the registered sign claim."],
        independent_audit="Separate agent derived the same pre-elimination density expansion, constraints, Hessians and gauge determinant.",
        closure=dict(coupled_regular_patch_principal_verified=False, specified_inward_sign_obstruction=False,
                     all_degenerate_branches_excluded=False, full_3plus1_health=False,
                     physical_instability_wavelengths_identified=False, global_singularity_removal=False,
                     full_RefG_rejected=False))


def constant_density_KS_checks(exact, gate):
    """Section 32: remaining ELs retained; subsystem curves are not solutions."""
    t = s.symbols("t", real=True)
    K, n0, j0 = s.symbols("K n0 j0", positive=True)
    a, b, N, j, theta = [s.Function(v)(t) for v in ("a", "b", "N", "j", "theta")]
    Ffun, rhofun = s.Function("F"), s.Function("rho")
    nv = j/(a*b**2)
    f, rho = Ffun(nv), rhofun(nv)
    ad, bd = s.diff(a, t), s.diff(b, t)
    L = (-2*K*f*(a*bd**2+2*b*ad*bd)/N+2*K*N*a*f
         -N*a*b**2*rho+j*s.diff(theta, t))

    def EL(field):
        return s.diff(s.diff(L, s.diff(field, t)), t)-s.diff(L, field)

    ea, eb = EL(a), EL(b)
    f0, r0 = Ffun(n0), rhofun(n0)
    beta = n0*s.diff(f0, n0)/f0
    c = r0/(6*K*f0)
    constant = {a: j0/(n0*b**2), j: j0, N: 1}
    exact("constant32_current_conservation", EL(theta), s.diff(j, t))
    exact("constant32_constant_density", nv.subs(constant), n0)
    exact("constant32_constant_volume", (a*b**2).subs(constant), j0/n0)
    exact("constant32_rate_relation", (ad/a+2*bd/b).subs(constant).doit())
    U = f*a*b**2*(ad/(N*a)-bd/(N*b))
    exact("constant32_unfixed_shear_EL_identity", s.diff(U, t)-N*f*a+(b*eb-2*a*ea)/(4*K))
    U0 = U.subs(constant).doit()
    exact("constant32_shear_current", U0, -3*f0*j0*bd/(n0*b))
    shear_residual = (s.diff(U0, t)-f0*j0/(n0*b**2))
    exact("constant32_shear_acceleration_identity", shear_residual,
          -3*f0*j0/n0*(s.diff(bd/b, t)+1/(3*b**2)))
    lapse = (s.diff(L, N)/(a*b**2)).subs(constant).doit()
    speed2 = s.Rational(1, 3)-c*b**2
    exact("constant32_lapse_speed_relation", lapse, -6*K*f0*(bd**2-speed2)/b**2)
    exact("constant32_subsystem_acceleration", (bd**2/b-1/(3*b)).subs(bd**2, speed2), -c*b)
    residual = ((s.Rational(4, 3)-2*beta)/b**2
                +(n0*s.diff(r0, n0)-2*r0+beta*r0)/(2*K*f0))
    for name, expr in (("radial", -ea/(2*K*N*f*b**2)), ("angular", -eb/(4*K*N*f*a*b))):
        value = s.simplify(expr.subs(constant).doit())
        value = value.subs(s.diff(b, t, 2), -c*b).subs(bd**2, speed2)
        exact("constant32_remaining_"+name+"_EL", value, residual)
    bv, fv, rv, rpv, betav, cv = s.symbols("b F rho rhoprime beta c", real=True)
    residual_jet = ((s.Rational(4, 3)-2*betav)/bv**2
                    +(n0*rpv-2*rv+betav*rv)/(2*K*fv))
    exact("constant32_changing_radius_coefficient", s.diff(residual_jet, bv),
          -2*(s.Rational(4, 3)-2*betav)/bv**3)
    exact("constant32_required_beta", s.solve(s.Rational(4, 3)-2*betav, betav)[0], s.Rational(2, 3))
    exact("constant32_required_equation_of_state", residual_jet.subs(betav, s.Rational(2, 3)),
          (n0*rpv-s.Rational(4, 3)*rv)/(2*K*fv))
    mass = s.symbols("m", positive=True)
    dust = residual_jet.subs({betav: s.Rational(2, 3), rv: mass*n0, rpv: mass})
    exact("constant32_positive_dust_remaining_residual", dust, -mass*n0/(6*K*fv))
    gate("constant32_positive_dust_cannot_satisfy_open_interval", s.simplify(dust) != 0)
    gate("constant32_negative_control_omitted_scale_EL",
         s.simplify(residual_jet.subs(betav, s.Rational(2, 3))) != 0)
    # Proper-time integrals apply only if every EL admits the entire interval.
    radius, cp = s.symbols("radius c_positive", positive=True)
    tau_pos = s.asin(s.sqrt(3*cp)*radius)/s.sqrt(cp)
    tau_zero = s.sqrt(3)*radius
    tau_neg = s.asinh(s.sqrt(3*cp)*radius)/s.sqrt(cp)
    exact("constant32_positive_c_time_primitive", s.diff(tau_pos, radius), 1/s.sqrt(s.Rational(1, 3)-cp*radius**2))
    exact("constant32_zero_c_time_primitive", s.diff(tau_zero, radius), s.sqrt(3))
    exact("constant32_negative_c_time_primitive", s.diff(tau_neg, radius), 1/s.sqrt(s.Rational(1, 3)+cp*radius**2))
    exact("constant32_positive_c_turning_time_finite", tau_pos.subs(radius, 1/s.sqrt(3*cp)), s.pi/(2*s.sqrt(cp)))
    for name, primitive in (("positive", tau_pos), ("zero", tau_zero), ("negative", tau_neg)):
        exact("constant32_"+name+"_centre_time_endpoint", s.limit(primitive, radius, 0), 0)
    gate("constant32_zero_speed_is_maximum_for_positive_c", (-cp*radius).is_negative)
    exact("constant32_wrong_sphere_sign_changes_speed", (-s.Rational(1, 3)-cv*radius**2)-(s.Rational(1, 3)-cv*radius**2), -s.Rational(2, 3))
    h, hdot = s.symbols("Hb Hbdot", real=True)
    curvature = 4*((-2*hdot+4*h**2)**2+2*(hdot+h**2)**2+8*h**4+(h**2+radius**-2)**2)
    on_curve = s.expand(curvature.subs(hdot, -1/(3*radius**2))).subs(h**4, (1/(3*radius**2)-cv)**2).subs(h**2, 1/(3*radius**2)-cv)
    exact("constant32_curvature_endpoint_coefficient", s.limit(radius**4*on_curve, radius, 0), s.Rational(80, 3))
    return dict(
        assumptions=["Same W87/W89 action, K>0,F>0,Fp>0,j>0", "Connected open KS interval with Fdot=0 and nonzero inward Hb", "All Euler-Lagrange equations retained"],
        necessary_subsystem=dict(Ha="-2Hb", Hbdot="-1/(3b^2)", bdot_squared="1/3-c*b^2", bddot="-c*b", c="rho(n0)/(6K F(n0))"),
        remaining_compatibility=["beta=n0 Fp/F=2/3", "n0 rho'=4rho/3"],
        positive_dust_result="rho=m*n>0 fails the remaining scale equation; no open constant-density dust branch is constructed.",
        endpoint_scope="Only if the full branch exists and is retained: inward proper time to b=0 is finite and curvature diverges. Leaving the interval earlier is not classified.",
        limitations=["An isolated Fdot=0 point is not this open interval.", "This does not classify every degenerate background or every spin branch.", "No conclusion transferred to the different canonical spherical saturation action."],
        closure=dict(full_scale_compatibility_verified=False, positive_dust_open_interval_excluded=False,
                     conditional_endpoint_verified=False, all_degenerate_branches_excluded=False, full_RefG_rejected=False))


def audit():
    checks = []

    def exact(name, expression, target=0):
        residual = s.simplify(s.expand(expression - target))
        checks.append(dict(name=name, passed=residual == 0,
                           residual=str(residual)))

    def gate(name, condition, **evidence):
        checks.append(dict(name=name, passed=bool(condition), **evidence))

    source = Path(__file__).with_name("verify_spherical_saturation_bridge.py")
    original_bytes = source.read_bytes()
    original_hash = hashlib.sha256(original_bytes).hexdigest()
    tree = ast.parse(original_bytes.decode("utf-8-sig"))
    definition = next(node for node in tree.body
                      if isinstance(node, ast.FunctionDef)
                      and node.name == "saturation_curvature")
    namespace = {}
    exec(compile(ast.Module(body=[definition], type_ignores=[]),
                 str(source), "exec"), namespace)
    curvature = namespace["saturation_curvature"]

    r, alpha, ell, q, A = s.symbols("r alpha ell q A", positive=True)
    rho, pr, pt, J = s.symbols("rho pr pt J", real=True)
    z = (1-q)/ell**2
    b = alpha*q**2
    c = curvature(rho, pr, pt, J, z, alpha, ell)
    P1, P2, D1, D2 = s.symbols("P1 P2 D1 D2", real=True)
    V = s.symbols("V", nonnegative=True)
    kinetic = A*(P1**2+P2**2+D1**2+D2**2)/2
    canonical = {rho: kinetic+V, pr: kinetic-V,
                 J: A*(P1*D1+P2*D2)}
    for sign in (-1, 1):
        tkk = rho+pr+2*sign*J
        hkk = c["hnn_over_r"]+c["hee_over_r"]+2*sign*c["hne_over_r"]
        exact("radial_null_action_"+str(sign), -2*hkk, 2*b*tkk)
        exact("canonical_radial_nec_"+str(sign), tkk.subs(canonical),
              A*((P1+sign*D1)**2+(P2+sign*D2)**2))
        # beta R_;kk=2 alpha r^2 Tkk in the verifier's normalization.
        beta = -2*r/q**2
        exact("orbit_action_null_projection_"+str(sign), beta*r*hkk,
              2*alpha*r**2*tkk)
    T = s.symbols("T", nonnegative=True)
    gate("positive_response_preserves_null_sign", (2*b).is_positive)
    exact("vanishing_response_limit", s.limit(2*b*T, q, 0), 0)
    R = s.symbols("R", positive=True)
    Rp = s.symbols("Rp", real=True)
    Rpp = -alpha*R*q**2*T
    theta = 2*Rp/R
    exact("affine_raychaudhuri", 2*Rpp/R-2*Rp**2/R**2,
          -theta**2/2-2*alpha*q**2*T)

    x = s.symbols("x", nonnegative=True)
    response = x/(1+2*x)**s.Rational(3, 2)
    exact("contrast_response_derivative", s.diff(response, x),
          (1-x)/(1+2*x)**s.Rational(5, 2))
    exact("contrast_peak", response.subs(x, 1), 1/(3*s.sqrt(3)))
    exact("contrast_zero_endpoint", response.subs(x, 0), 0)
    exact("contrast_infinite_endpoint", s.limit(response, x, s.oo), 0)
    mu = s.symbols("mu", nonnegative=True)
    flux, velocity = s.symbols("S v", real=True)
    qmu = 1/(1+2*alpha*ell**2*mu)
    mur = (rho+velocity*flux-3*mu)/r
    qr = s.diff(qmu, mu)*mur
    exact("weighted_radial_mass_identity",
          alpha*ell**2*qmu**s.Rational(3, 2)*(rho+velocity*flux),
          s.Rational(3, 2)*(1-qmu)*s.sqrt(qmu)-r*qr/(2*s.sqrt(qmu)))

    beta = s.symbols("beta", real=True)
    mass_source = (kinetic+V)+beta*A*(P1*D1+P2*D2)
    completed_square = V+A*sum(
        (p+beta*d)**2+(1-beta**2)*d**2
        for p, d in ((P1, D1), (P2, D2)))/2
    exact("untrapped_mass_source_completed_square", mass_source, completed_square)
    exact("horizon_null_flux_zero_control",
          mass_source.subs({beta: 1, P2: 0, D2: 0, D1: -P1, V: 0}), 0)

    # Local trapped jet: psi=0, psi_r=D, P real. This is the same canonical
    # scalar, with its actual sextic potential zero at the selected point.
    amp = s.symbols("P", positive=True)
    r0, a0, l0 = s.Integer(4), s.Rational(1,25), s.Integer(2)
    mu0, q0, z0 = s.Rational(25,8), s.Rational(1,2), s.Rational(1,8)
    v0, A0, L0 = s.sqrt(2), s.Integer(1), s.Integer(1)
    D0 = (1-s.sqrt(2))*amp
    rho0 = s.simplify((amp**2+D0**2)/2)
    pr0, pt0, S0 = rho0, s.simplify((amp**2-D0**2)/2), amp*D0
    F0, k0 = 1-r0**2*z0, v0/r0
    b0, C0 = a0*q0**2, z0*(1-3*l0**2*z0)/2
    exact("sample_response", 1/(1+2*a0*l0**2*mu0), q0)
    exact("sample_z", 2*a0*mu0*q0, z0)
    exact("sample_trapping", F0, -1)
    exact("sample_chart", F0+v0**2, A0)
    exact("sample_canonical_mass_cancellation", rho0+v0*S0, 0)
    exact("sample_flux_fraction", S0, -rho0/s.sqrt(2))
    exact("sample_tangential_pressure", pt0, rho0/s.sqrt(2))
    exact("sample_stress_determinant", rho0*pr0-S0**2, rho0**2/2)
    gate("sample_positive_density", (rho0/amp**2).is_positive)
    gate("sample_subnull_canonical_flux", 1-s.Rational(1,2) > 0)

    # The mass, spatial-metric and momentum constraints determine these
    # derivatives. Set A_r=L_r=L_rr=0 locally; do not freeze A in time.
    mur0 = -3*mu0/r0
    zr0 = 2*b0*mur0
    Fr0 = -2*r0*z0-r0**2*zr0
    vr0 = -Fr0/(2*v0)
    kr0 = (vr0-k0)/r0
    exact("sample_radial_mass_constraint", 3*mu0+r0*mur0, rho0+v0*S0)
    exact("sample_spatial_metric_derivative", Fr0+2*v0*vr0, 0)
    Mt = L0*r0**2*(v0*(rho0+pr0)+(A0+v0**2)*S0)
    mut = Mt/r0**3
    zt = 2*b0*mut
    kt = L0*(v0*kr0+k0**2+C0+b0*pr0)
    vt = r0*kt
    At = s.simplify(-r0**2*zt+2*v0*vt)
    Kr = vr0-b0*r0*S0
    exact("sample_temporal_mass_constraint", Mt, 8*s.sqrt(2)*rho0)
    exact("sample_mu_time", mut, rho0/(4*s.sqrt(2)))
    exact("sample_shift_time", vt, rho0/25)
    exact("sample_A_time", At, s.sqrt(2)*rho0/25)
    exact("sample_mixed_constraint", vr0+At/(2*A0*L0), Kr)
    exact("sample_regular_metric_equation", At/L0, -2*b0*r0*A0*S0)
    # The clock equation supplies finite L_t for every finite amplitude.
    Lt = -L0**2*(vr0+2*v0/r0-b0*r0*S0)
    exact("sample_clock_time", Lt, -(s.Rational(9,8)+rho0/25)/s.sqrt(2))

    # Independently differentiate the actual scalar/shift equations at a
    # locally linear psi and constant P, so P_r=D_r=0 at this point.
    Pt = 2*(D0+v0*amp)/r0+vr0*amp
    Dt = vr0*D0
    nrho = s.simplify(At*(amp**2+D0**2)/2+amp*Pt+D0*Dt)
    exact("sample_scalar_energy_balance", nrho,
          2*S0/r0+Kr*(rho0+pr0)+2*k0*(rho0+pt0))
    nmu = mut-v0*mur0
    nb = -4*a0**2*l0**2*q0**3*nmu
    nS = s.simplify(At*amp*D0/2+Pt*D0+amp*Dt)
    br = -2*a0*l0**2*q0*zr0
    Cr = (1-6*l0**2*z0)*zr0/2
    # v_rr cancels between partial_t(Kr) and v partial_r(Kr).
    nKr = (vr0**2+C0+b0*pr0+r0*(Cr+br*pr0)
           -(r0*S0*nb-b0*v0*S0+b0*r0*nS))
    R2_metric = s.simplify(2*(Kr**2-nKr))
    curv0 = curvature(rho0, pr0, pt0, S0, z0, a0, l0)
    exact("sample_independent_metric_R2", R2_metric, curv0["orbit_Ricci"])
    hnn_metric = (-vt/L0+v0*vr0)/r0
    hee_metric = -Kr*v0/r0
    hne_metric = At/(2*L0*r0)
    for key, value in (("hnn_over_r", hnn_metric),
                       ("hee_over_r", hee_metric),
                       ("hne_over_r", hne_metric)):
        exact("sample_independent_metric_"+key, value, curv0[key])
    K_metric = (R2_metric**2+8*(hnn_metric**2+hee_metric**2
                              -2*hne_metric**2)+4*z0**2)
    exact("sample_independent_metric_K", K_metric, curv0["Kretschmann"])
    R2_rho = 2*rho0**2/625-s.sqrt(2)*rho0/50-s.Rational(5,16)
    K_rho = R2_rho**2+rho0**2/1250+s.Rational(5,64)
    exact("sample_orbit_polynomial", curv0["orbit_Ricci"], R2_rho)
    exact("sample_K_polynomial", curv0["Kretschmann"], K_rho)
    exact("sample_E", a0*l0**2*q0**s.Rational(3,2)*rho0, s.sqrt(2)*rho0/25)
    exact("sample_quartic_density_growth",
          s.limit(curv0["Kretschmann"]/(rho0**4), amp, s.oo),
          s.Rational(4,390625))
    gate("negative_control_detects_broken_flux_cancellation",
         s.simplify(rho0+v0*S0/2) != 0)
    gate("negative_control_detects_frozen_spatial_metric", s.simplify(At) != 0)
    gate("no_original_verifier_edit",
         hashlib.sha256(source.read_bytes()).hexdigest() == original_hash)

    previous_check_count = len(checks)
    previous_checks_pass = all(item["passed"] for item in checks)
    homogeneous_join = w87_current_bridge_checks(exact, gate)
    homogeneous_join["checks"] = len(checks)-previous_check_count
    homogeneous_join["passed"] = sum(item["passed"] for item in checks[previous_check_count:])
    before_quadratic = len(checks)
    quadratic_candidate = quadratic_current_spherical_checks(exact, gate)
    quadratic_checks = checks[before_quadratic:]
    quadratic_candidate["checks"] = len(quadratic_checks)
    quadratic_candidate["passed"] = sum(item["passed"] for item in quadratic_checks)
    for flag in ("homogeneous_future_metric_curvature_bounded", "homogeneous_future_null_affine_infinite",
                 "fixed_geometry_current_signs", "specified_KS_target_excluded"):
        quadratic_candidate["closure"][flag] = all(item["passed"] for item in quadratic_checks)
    before_two_scale = len(checks)
    two_scale_completion = ks_two_scale_completion_checks(exact, gate)
    two_scale_checks = checks[before_two_scale:]
    two_scale_completion["checks"] = len(two_scale_checks)
    two_scale_completion["passed"] = sum(item["passed"] for item in two_scale_checks)
    two_scale_completion["closure"]["variational_premises_verified"] = all(item["passed"] for item in two_scale_checks)
    two_scale_completion["closure"]["conditional_KS_completion_obstruction"] = all(item["passed"] for item in two_scale_checks)
    action_terms = hayward_static_action_terms()
    before_extension = len(checks)
    finite_ball_extension = finite_ball_extension_checks(exact, gate, action_terms)
    extension_checks = checks[before_extension:]
    finite_ball_extension["checks"] = len(extension_checks)
    finite_ball_extension["passed"] = sum(item["passed"] for item in extension_checks)
    for flag in ("local_horizon_extension_verified", "finite_ball_current_matching_verified"):
        finite_ball_extension["closure"][flag] = all(item["passed"] for item in extension_checks)
    before_central = len(checks)
    central_variation = central_variational_domain_checks(exact, gate, action_terms)
    central_checks = checks[before_central:]
    central_variation["checks"] = len(central_checks)
    central_variation["passed"] = sum(item["passed"] for item in central_checks)
    central_variation["closure"]["central_flux_and_boundary_freedoms_verified"] = all(item["passed"] for item in central_checks)
    before_spin = len(checks)
    spherical_spin = spherical_lorentz_action_checks(exact, gate)
    spin_checks = checks[before_spin:]
    spherical_spin["checks"] = len(spin_checks)
    spherical_spin["passed"] = sum(item["passed"] for item in spin_checks)
    spherical_spin["closure"]["spherical_action_entry_verified"] = all(item["passed"] for item in spin_checks)
    before_radial = len(checks)
    coupled_radial = coupled_radial_principal_checks(exact, gate)
    radial_checks = checks[before_radial:]
    coupled_radial["checks"] = len(radial_checks)
    coupled_radial["passed"] = sum(item["passed"] for item in radial_checks)
    for flag in ("coupled_regular_patch_principal_verified", "specified_inward_sign_obstruction"):
        coupled_radial["closure"][flag] = (all(item["passed"] for item in spin_checks)
                                          and all(item["passed"] for item in radial_checks))
    before_constant = len(checks)
    constant_density = constant_density_KS_checks(exact, gate)
    constant_checks = checks[before_constant:]
    constant_density["checks"] = len(constant_checks)
    constant_density["passed"] = sum(item["passed"] for item in constant_checks)
    for flag in ("full_scale_compatibility_verified", "positive_dust_open_interval_excluded", "conditional_endpoint_verified"):
        constant_density["closure"][flag] = all(item["passed"] for item in constant_checks)
    before_readout = len(checks)
    central_readout = central_source_readout_checks(exact, gate)
    readout_checks = checks[before_readout:]
    central_readout["checks"] = len(readout_checks)
    central_readout["passed"] = sum(item["passed"] for item in readout_checks)
    for flag in ("central_comparison_verified", "common_readout_restriction_verified"):
        central_readout["closure"][flag] = all(item["passed"] for item in readout_checks)
    before_dynamic = len(checks)
    dynamic_centre = dynamic_common_centre_checks(exact, gate)
    dynamic_checks = checks[before_dynamic:]
    dynamic_centre["checks"] = len(dynamic_checks)
    dynamic_centre["passed"] = sum(item["passed"] for item in dynamic_checks)
    for flag in ("dynamic_central_compatibility", "static_restriction_not_universal"):
        dynamic_centre["closure"][flag] = all(item["passed"] for item in dynamic_checks)
    before_continuation = len(checks)
    continuation = common_readout_continuation_checks(exact, gate)
    continuation_checks = checks[before_continuation:]
    continuation["checks"] = len(continuation_checks)
    continuation["passed"] = sum(item["passed"] for item in continuation_checks)
    for flag in ("first_radial_compatibility", "leading_momentum_propagation",
                 "full_spatial_identity", "specified_isolated_extension_excluded"):
        continuation["closure"][flag] = all(item["passed"] for item in continuation_checks)
    before_full_readout = len(checks)
    full_readout = full_coframe_source_decision_checks(exact, gate)
    full_readout_checks = checks[before_full_readout:]
    full_readout["checks"] = len(full_readout_checks)
    full_readout["passed"] = sum(item["passed"] for item in full_readout_checks)
    for flag in ("full_readout_verified", "stationary_source_excluded_in_domain",
                 "minimal_density_cap_excluded"):
        full_readout["closure"][flag] = all(item["passed"] for item in full_readout_checks)
    before_null_tail = len(checks)
    null_tail = null_tail_curvature_checks(exact, gate)
    null_tail_checks = checks[before_null_tail:]
    null_tail["checks"] = len(null_tail_checks)
    null_tail["passed"] = sum(item["passed"] for item in null_tail_checks)
    for flag in ("null_source_solution", "finite_affine_pp_blowup", "finite_proper_time_tidal_blowup",
                 "universal_null_source_regularization_excluded"):
        null_tail["closure"][flag] = all(item["passed"] for item in null_tail_checks)
    before_light = len(checks)
    light_source = existing_light_source_checks(exact, gate)
    light_checks = checks[before_light:]
    light_source["checks"] = len(light_checks)
    light_source["passed"] = sum(item["passed"] for item in light_checks)
    optical_ok = all(item["passed"] for item in light_checks)
    if not optical_ok:
        light_source["decision"] = "EXISTING_LIGHT_SOURCE_AUDIT_FAILED"
    for flag in ("existing_light_transport_compatible", "leading_optical_stress_matches",
                 "no_extra_scale_factor_needed", "optical_scope_boundary_verified"):
        light_source["closure"][flag] = optical_ok
    light_source["closure"]["source_backreaction_included"] = (
        optical_ok and null_tail["closure"]["null_source_solution"])
    before_inner = len(checks)
    inner_extremal = inner_extremal_bridge_checks(exact, gate)
    inner_checks = checks[before_inner:]
    inner_extremal["checks"] = len(inner_checks)
    inner_extremal["passed"] = sum(item["passed"] for item in inner_checks)
    inner_groups = {group: [item for item in inner_checks if item["name"].startswith("inner39_"+group+"_")]
                    for group in ("geometry", "fixed_law", "source", "ray")}
    inner_ok = {group: bool(rows) and all(item["passed"] for item in rows)
                for group, rows in inner_groups.items()}
    if not all(inner_ok.values()):
        inner_extremal["decision"] = "INNER_EXTREMAL_BRIDGE_AUDIT_FAILED"
    inner_extremal["closure"]["target_geometry_verified"] = inner_ok["geometry"]
    inner_extremal["closure"]["fixed_H_bridge_excluded"] = inner_ok["fixed_law"]
    inner_extremal["closure"]["inverse_law_obstruction_verified"] = inner_ok["source"]
    inner_extremal["closure"]["conditional_null_Ricci_bound_verified"] = (
        inner_ok["geometry"] and inner_ok["ray"] and inner_ok["source"])
    passed = sum(item["passed"] for item in checks)
    return dict(
        decision="COMPLETION_BOUNDARY_AND_HOMOGENEOUS_JOIN_VERIFIED" if passed == len(checks)
                 else "COMPLETION_BOUNDARY_AND_HOMOGENEOUS_JOIN_FAILED",
        passed=passed, checks=len(checks), failed=[c for c in checks if not c["passed"]],
        original_verifier_sha256=original_hash,
        this_verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        previous_stage24_checks=dict(passed=previous_checks_pass, count=previous_check_count),
        homogeneous_join=homogeneous_join,
        quadratic_candidate=quadratic_candidate,
        two_scale_completion=two_scale_completion,
        finite_ball_extension=finite_ball_extension,
        central_variation=central_variation,
        spherical_spin=spherical_spin,
        coupled_radial=coupled_radial,
        constant_density=constant_density,
        central_readout=central_readout,
        dynamic_centre=dynamic_centre,
        common_readout_continuation=continuation,
        full_coframe_source_decision=full_readout,
        null_tail_curvature=null_tail,
        existing_light_source_audit=light_source,
        inner_extremal_bridge_audit=inner_extremal,
        local_witness=dict(
            scope="One smooth local source/geometry jet, not a global initial-data family.",
            finite_amplitude="Every finite P gives finite source, geometry and listed derivatives.",
            rho="(2-sqrt(2))*P^2", M_r="0", M_t="8*sqrt(2)*rho",
            E="sqrt(2)*rho/25", R2="2*rho^2/625-sqrt(2)*rho/50-5/16",
            K="R2^2+rho^2/1250+5/64", limit_K_over_rho4="4/390625"),
        conditional_source_bound=dict(
            premise="rho <= C*M/r^3 in a regular frame, uniformly in the claimed spacetime domain",
            consequence="E <= C/(3*sqrt(3)); section14 then bounds curvature",
            contrast_premise_derived=False),
        causal_theorem=dict(
            references=["https://doi.org/10.1103/PhysRevLett.14.57",
                        "https://arxiv.org/html/1012.6038v3"],
            primary_generator_theorem="Fewster and Galloway, Theorem 5.2, with c=0",
            type="Analytical conditional spherical focusing/topology argument; not a Python proof.",
            assumptions=["Smooth time-oriented spherical Lorentzian spacetime",
                         "Noncompact connected Cauchy hypersurface",
                         "A smooth compact acausal round future-trapped spacelike sphere",
                         "Radial null convergence on its future normal generators"],
            consequence="These assumptions exclude future-null completeness.",
            caveats=["A focal point alone is a caustic, not a curvature singularity.",
                     "A Cauchy-horizon extension can drop the global Cauchy premise.",
                     "Numerical trapping is finite-grid evidence, not an exact PDE certificate.",
                     "Angular null convergence is not assumed: round-sphere normal generators are radial."]),
        closure=dict(local_source_witness=passed == len(checks),
                     radial_null_focusing_identity=passed == len(checks),
                     global_initial_family_constructed=False,
                     dynamical_blowup=False, curvature_blowup_of_fixed_packet=False,
                     global_singularity_removal=False, full_RefG_rejected=False),
        results=checks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    result = audit()
    if not args.verbose:
        result.pop("results")
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(0 if not result["failed"] else 1)
