"""Verify the frozen W92 active-background matter response.

Author-written calculation; see matter_medium_source_response.md for the
action, domain, citations and interpretation. No project/private files are
read, and no files are written. Run with --verbose to print every residual.
"""

import argparse
import json

import mpmath as mp
import sympy as s


def medium_polynomial(x):
    """Frozen Stage 27 polynomial, shared by both bounded checks."""
    return x + x**2/2 - 282*x**3 + 802*x**4 - 624*x**5


def run_checks():
    checks = []

    def exact(name, actual, target=0):
        residual = s.simplify(actual - target)
        checks.append(dict(name=name, kind="exact", passed=residual == 0,
                           residual=str(residual)))

    def truth(name, value, kind="control"):
        checks.append(dict(name=name, kind=kind, passed=bool(value)))

    x = s.symbols("X", real=True)
    K = medium_polynomial(x)
    P, g = s.symbols("P g", positive=True)
    H, v, acc, Hd, ro, po = s.symbols(
        "H_c v acceleration H_c_dot rho_O p_O", real=True)
    k0, k1, k2 = s.symbols("K K_X K_XX", real=True)
    X = v**2/2
    rho = v**2*k1 - k0 + 3*g*H*v**3
    pressure = k0 - g*v**2*acc
    J = v*k1 + 3*g*H*v**2
    D = k1 + v**2*k2 + 6*g*H*v + 3*g**2*v**4/(2*P)
    acc_sol = (-3*H*v*k1 - 9*g*H**2*v**2
               + 3*g*v**4*(k1+3*g*H*v)/(2*P)
               + 3*g*v**2*(ro+po)/(2*P))/D
    hd_sol = -(v**2*k1 + 3*g*H*v**3
               - g*v**2*acc_sol + ro+po)/(2*P)
    Jdot = (k1+v**2*k2+6*g*H*v)*acc + 3*g*v**2*Hd
    exact("current_with_ordinary_source",
          (Jdot+3*H*J).subs({acc: acc_sol, Hd: hd_sol}))
    exact("Raychaudhuri_with_ordinary_source",
          (2*P*Hd+rho+pressure+ro+po).subs({acc: acc_sol, Hd: hd_sol}))
    rhodot = (v*k1+v**3*k2+9*g*H*v**2)*acc + 3*g*v**3*Hd
    exact("medium_energy_current_identity",
          rhodot+3*H*(rho+pressure), v*(Jdot+3*H*J))
    exact("total_energy_continuity",
          (rhodot-3*H*(ro+po)+3*H*(rho+pressure+ro+po)).subs(
              {acc: acc_sol, Hd: hd_sol}))

    # Independently vary the original minisuperspace action.
    a, adot, lapse, h = s.symbols("a a_dot lapse h", positive=True)
    hdot, w = s.symbols("h_dot theta_dot", real=True)
    U = s.Function("U")(h)
    ordinary_rho = (hdot**2+h**2*w**2)/2+U
    ordinary_p = (hdot**2+h**2*w**2)/2-U
    mini = (-3*P*a*adot**2/lapse
            + a**3*lapse*K.subs(x, v**2/(2*lapse**2))
            + g*a**2*adot*v**3/lapse**3
            + a**3*((hdot**2+h**2*w**2)/(2*lapse)-lapse*U))
    jets = {k0: K.subs(x, X), k1: s.diff(K, x).subs(x, X),
            k2: s.diff(K, x, 2).subs(x, X)}
    exact("lapse_variation_includes_canonical_matter",
          s.diff(mini, lapse).subs({lapse: 1, adot: a*H})/a**3,
          3*P*H**2-rho.subs(jets)-ordinary_rho)
    exact("medium_canonical_charge_from_action",
          s.diff(mini, v).subs({lapse: 1, adot: a*H})/a**3, J.subs(jets))
    mini1 = mini.subs(lapse, 1)
    momentum_a = s.diff(mini1, adot)
    ela = (s.diff(momentum_a, a)*adot
           + s.diff(momentum_a, adot)*a*(Hd+H**2)
           + s.diff(momentum_a, v)*acc-s.diff(mini1, a)).subs(adot, a*H)
    exact("scale_factor_variation_with_matter",
          ela/(-3*a**2), P*(3*H**2+2*Hd)+pressure.subs(jets)+ordinary_p)
    hddot = h*w**2-s.diff(U, h)-3*H*hdot
    wdot = -(3*H+2*hdot/h)*w
    ordinary_dot = (s.diff(ordinary_rho, h)*hdot
                    + s.diff(ordinary_rho, hdot)*hddot
                    + s.diff(ordinary_rho, w)*wdot)
    exact("canonical_matter_energy_continuity",
          ordinary_dot+3*H*(ordinary_rho+ordinary_p))
    eps = s.symbols("epsilon", positive=True)
    initial = {hdot: 0, w: s.sqrt(eps)/h, U: eps/2}
    exact("same_field_zero_initial_pressure", ordinary_p.subs(initial))
    exact("same_field_added_energy", ordinary_rho.subs(initial), eps)

    # Explicit curvature-induced ordinary source, including trace reversal.
    eta = s.diag(-1, 1, 1, 1)
    normal = s.Matrix([-v, 0, 0, 0])
    matter_tensor = s.diag(ro, po, po, po)
    trace = s.trace(eta*matter_tensor)
    forcing = (g/P*(normal.T*(matter_tensor-trace*eta/2)*normal))[0]
    exact("curvature_induced_matter_source", forcing, g*v**2*(ro+3*po)/(2*P))
    exact("constant_medium_has_no_curvature_forcing", forcing.subs(v, 0))
    truth("active_medium_has_nonzero_forcing",
          forcing.subs({P: 1, g: 1, v: 1, ro: 1, po: 0}) != 0)

    frozen = {P: 1, g: 1}
    rr = rho.subs(jets).subs(frozen)
    jj = J.subs(jets).subs(frozen)
    equations = s.Matrix([3*H**2-rr-eps, jj+1])
    origin = {H: 1, v: 1, eps: 0}
    variables = s.Matrix([H, v])
    jac = equations.jacobian(variables).subs(origin)
    exact("fixed_charge_jacobian_determinant", jac.det(), 27)
    first = -jac.inv()*equations.diff(eps).subs(origin)
    second_terms = s.Matrix([
        (first.T*s.hessian(expr, variables).subs(origin)*first)[0]
        for expr in equations])
    second = -jac.inv()*second_terms
    exact("H_first_source_response", first[0], s.Rational(1, 9))
    exact("v_first_source_response", first[1], -s.Rational(1, 9))
    exact("H_second_source_response", second[0], s.Rational(476, 243))
    exact("v_second_source_response", second[1], s.Rational(955, 243))
    rho_first = (s.Matrix([s.diff(rr, H), s.diff(rr, v)]).subs(origin).T*first)[0]
    exact("medium_energy_compensation", rho_first, -s.Rational(1, 3))
    exact("total_energy_response", 6*first[0], s.Rational(2, 3))
    total_second = 6*(first[0]**2+second[0])
    exact("positive_quadratic_total_response", total_second, s.Rational(958, 81))
    truth("frozen_background_cannot_accept_added_energy",
          equations[0].subs({H: 1, v: 1}) == -eps, "negative_control")
    H_fixed_v = (1+s.sqrt(1+4*eps/3))/2
    truth("fixed_v_comparison_changes_medium_charge",
          s.diff(jj.subs({v: 1, H: H_fixed_v}), eps).subs(eps, 0) == 1,
          "negative_control")
    physical_acc = acc_sol.subs(jets).subs(frozen)
    physical_hd = hd_sol.subs(jets).subs(frozen)
    for name, expr, target in [
        ("acceleration_source_response", physical_acc, -s.Rational(904, 81)),
        ("Hdot_source_response", physical_hd, -s.Rational(500, 81)),
    ]:
        response = (s.diff(expr, H)*first[0]+s.diff(expr, v)*first[1]
                    + s.diff(expr, ro)).subs({**origin, ro: 0, po: 0})
        exact(name, response, target)

    # Direct principal Hessian and Hilbert-stress expansion.
    q, deltaR, lam = s.symbols("lap_pi lap_Psi lambda", real=True)
    n_cov = s.Matrix([v, 0, 0, 0])
    hessian = s.diag(acc, -H*v+lam*q, -H*v, -H*v)
    box = s.trace(eta*hessian)
    square = s.trace(eta*hessian*eta*hessian)
    current_principal = k1*box + g*(square-box**2+lam*v**2*deltaR)
    C = k1+2*g*acc+4*g*H*v
    B = g*v**2
    exact("direct_scalar_Hessian_principal",
          s.diff(current_principal, lam).subs(lam, 0), C*q+B*deltaR)
    dX = -hessian*eta*n_cov
    scalar_dot_X = (n_cov.T*eta*dX)[0]
    tensor = (k1*n_cov*n_cov.T+k0*eta
              - g*box*n_cov*n_cov.T
              - g*(dX*n_cov.T+n_cov*dX.T)+g*eta*scalar_dot_X)
    exact("direct_medium_density", tensor[0, 0].subs(lam, 0), rho)
    exact("direct_medium_pressure", tensor[1, 1].subs(lam, 0), pressure)
    exact("direct_medium_spatial_density",
          s.diff(tensor[0, 0], lam).subs(lam, 0), -B*q)

    # Three-dimensional linear Einstein tensor, static local principal part.
    tt, xx, yy, zz = s.symbols("t x y z")
    coords = (tt, xx, yy, zz)
    Phi = s.Function("Phi_N")(xx, yy, zz)
    Psi = s.Function("Psi")(xx, yy, zz)
    perturb = s.diag(-2*Psi, -2*Phi, -2*Phi, -2*Phi)
    mixed = eta*perturb
    tr = s.trace(mixed)
    ricci = s.zeros(4)
    for i in range(4):
        for j in range(4):
            ricci[i, j] = sum(
                s.diff(mixed[k, j], coords[k], coords[i])
                + s.diff(mixed[k, i], coords[k], coords[j])
                - eta[k, k]*s.diff(perturb[i, j], coords[k], 2)
                for k in range(4))/2-s.diff(tr, coords[i], coords[j])/2
    einstein = ricci-eta*s.trace(eta*ricci)/2
    lap_phi = sum(s.diff(Phi, c, 2) for c in coords[1:])
    exact("independent_linear_Einstein_density", einstein[0, 0], 2*lap_phi)
    exact("independent_linear_anisotropic_equation",
          einstein[1, 2], s.diff(Phi-Psi, xx, yy))
    pp, ps, pi1 = s.symbols("grad_Phi grad_Psi grad_pi", real=True)
    static_l = P*(pp**2-2*pp*ps)-C*pi1**2/2-B*ps*pi1
    exact("static_action_Phi_equation", s.diff(static_l, pp), 2*P*(pp-ps))
    exact("static_action_Psi_equation", -s.diff(static_l, ps), 2*P*pp+B*pi1)
    exact("static_action_pi_equation", -s.diff(static_l, pi1), C*pi1+B*ps)
    A = C-B**2/(2*P)
    witness = {P: 1, g: 1, v: 1, H: 1, acc: s.Rational(1, 3), k1: -4}
    exact("witness_C", C.subs(witness), s.Rational(2, 3))
    exact("witness_A", A.subs(witness), s.Rational(1, 6))
    lap_psi = C*ro/(2*P*A)
    lap_pi = -B*ro/(2*P*A)
    exact("coupled_spatial_scalar_constraint", C*lap_pi+B*lap_psi)
    exact("coupled_spatial_metric_constraint", 2*P*lap_psi+B*lap_pi, ro)
    exact("witness_Poisson_source", lap_psi.subs(witness), 2*ro)
    exact("witness_scalar_source", lap_pi.subs(witness), -3*ro)
    exact("witness_G_ratio", (C/A).subs(witness), 4)
    exact("mixing_removed_reverts_to_EH", (C/A).subs(g, 0), 1)

    # Vacuum scalar-speed expression must change with ordinary background.
    theta = P*H-g*v**3/2
    theta_dot = P*hd_sol-3*g*v**2*acc_sol/2
    Fs = P**2*(H/theta-theta_dot/theta**2)-P
    effective_A = A.subs(acc, acc_sol)
    exact("nonzero_matter_scalar_gradient_correction",
          Fs*theta**2/(P**2*X)-effective_A, (ro+po)/(2*X))
    truth("vacuum_speed_formula_is_not_full_matter_formula",
          ((ro+po)/(2*X)).subs({ro: 1, po: 0, v: 1}) != 0,
          "negative_control")

    # Smooth finite-mass spherical source: symbolic spatial kernel only.
    r, width, mass, Geff = s.symbols("r L B_mass G_eff", positive=True)
    gaussian = mass*s.exp(-r**2/width**2)/(s.pi**s.Rational(3, 2)*width**3)
    potential = -Geff*mass*s.erf(r/width)/r
    exact("Gaussian_Poisson_equation",
          s.diff(r**2*s.diff(potential, r), r)/r**2, 4*s.pi*Geff*gaussian)
    exact("Gaussian_source_integral",
          s.integrate(4*s.pi*r**2*gaussian, (r, 0, s.oo)), mass)
    exact("Gaussian_finite_centre",
          s.limit(potential, r, 0, dir="+"), -2*Geff*mass/(s.sqrt(s.pi)*width))
    small, psi0, phi0 = s.symbols("small Psi_value Phi_value", real=True)
    clock = s.sqrt(1+2*small*psi0)
    rod = 1/s.sqrt(1-2*small*phi0)
    light = clock*rod
    exact("linear_common_clock_rod",
          s.diff(clock-rod.subs(phi0, psi0), small).subs(small, 0))
    exact("linear_light_readout", s.diff(light, small).subs(small, 0), psi0+phi0)

    # Finite same-charge initial data: two independent root algorithms.
    samples = []
    for value in ("0.000001", "0.00001", "0.0001"):
        with mp.workdps(60):
            e = mp.mpf(value)
            def kval(qx):
                return qx+qx*qx/2-282*qx**3+802*qx**4-624*qx**5
            def kprime(qx):
                return 1+qx-846*qx**2+3208*qx**3-3120*qx**4
            def rho_num(hh, vv):
                return vv**2*kprime(vv**2/2)-kval(vv**2/2)+3*hh*vv**3
            def charge_num(hh, vv):
                return vv*kprime(vv**2/2)+3*hh*vv**2
            hm, vm = mp.findroot(
                lambda hh, vv: (3*hh**2-rho_num(hh, vv)-e, charge_num(hh, vv)+1),
                (1+e/9, 1-e/9), tol=mp.mpf("1e-55"), maxsteps=50)
        with mp.workdps(90):
            e = mp.mpf(value)
            def h_of_v(vv):
                return (-1-vv*kprime(vv**2/2))/(3*vv**2)
            def reduced(vv):
                hh = h_of_v(vv)
                return 3*hh**2-rho_num(hh, vv)-e
            vn = mp.findroot(reduced, (1-e, mp.mpf(1)), solver="bisect",
                             tol=mp.mpf("1e-75"), maxsteps=400)
            hn = h_of_v(vn)
            rn = rho_num(hn, vn)
            residual = max(abs(3*hn**2-rn-e), abs(charge_num(hn, vn)+1))
            cross = max(abs(hn-hm), abs(vn-vm))
            truth("finite_constraint_"+value, residual < mp.mpf("1e-45"), "numeric_90_digits")
            truth("independent_root_"+value, cross < mp.mpf("1e-45"), "numeric_crosscheck")
            truth("partial_compensation_"+value,
                  0 < 3-rn < e and 0 < rn+e-3 < e, "numeric_branch")
            z = mp.findroot(lambda zz: zz-zz**2/2+zz**3/12-e, (e, e*(1+e)))
            amplitude, phase_rate = mp.sqrt(z), mp.sqrt(e/z)
            potential_o = z/2-z*z/4+z**3/24
            kinetic_o = z*phase_rate**2/2
            truth("canonical_source_realization_"+value,
                  max(abs(potential_o+kinetic_o-e), abs(kinetic_o-potential_o))
                  < mp.mpf("1e-70"), "numeric_canonical_scalar")
            samples.append(dict(
                epsilon=value, H_c=mp.nstr(hn, 22), v=mp.nstr(vn, 22),
                rho_medium=mp.nstr(rn, 22),
                total_density_increment=mp.nstr(rn+e-3, 22),
                compensated_fraction=mp.nstr((3-rn)/e, 18),
                ordinary_amplitude=mp.nstr(amplitude, 18),
                ordinary_phase_rate=mp.nstr(phase_rate, 18),
                max_constraint_residual=mp.nstr(residual, 8),
                independent_root_difference=mp.nstr(cross, 8)))

    failed = [row for row in checks if not row["passed"]]
    return dict(
        decision="ACTIVE_BACKGROUND_SOURCE_RESPONSE" if not failed else "CHECK_FAILURE",
        checks=len(checks), passed=len(checks)-len(failed), failed=failed,
        versions=dict(sympy=s.__version__, mpmath=mp.__version__),
        initial_source_samples=samples,
        exact_linear_response=dict(H_c="1/9", v="-1/9", rho_medium="-1/3",
                                   rho_total="2/3", quasistatic_G_ratio="4"),
        scope=dict(
            same_action_source_response_verified=not failed,
            fixed_medium_charge=True, quasistatic_kernel_is_conditional=True,
            original_RefG_pressure_map_derived=False,
            finite_matter_full_perturbation_health_proved=False,
            physical_EFT_scale_window_established=False,
            black_hole_mass_saturation=False, singularity_resolved=False),
        details=checks)


def run_pressure_map_checks():
    """Separate homogeneous density compensation from the RefG readout."""
    checks = []

    def exact(name, actual, target=0):
        residual = s.simplify(actual-target)
        checks.append(dict(name=name, kind="exact", passed=residual == 0,
                           residual=str(residual)))

    def control(name, condition):
        checks.append(dict(name=name, kind="identification_control",
                           passed=bool(condition)))

    P, A, source = s.symbols("P A_eff delta_rho_O", positive=True)
    B = s.symbols("B_mix", real=True)
    C = A+B**2/(2*P)
    # Solve both original spatial constraints; no source sign is prescribed.
    matrix = s.Matrix([[B, C], [2*P, B]])
    lap_psi, lap_pi = matrix.inv()*s.Matrix([0, source])
    extra = s.simplify(-B*lap_pi/source)
    ratio = s.simplify(2*P*lap_psi/source)
    exact("QS_medium_source_from_two_constraints", extra, B**2/(2*P*A))
    exact("QS_total_gravity_ratio", ratio, 1+extra)
    control("positive_principal_domain_has_nonnegative_extra_source",
            extra.is_nonnegative)
    exact("zero_mixing_control", extra.subs(B, 0))
    # Independent elimination in the quadratic static action.
    grad_phi, grad_psi, grad_pi = s.symbols("grad_Phi grad_Psi grad_pi")
    static = (P*(grad_phi**2-2*grad_phi*grad_psi)
              -C*grad_pi**2/2-B*grad_psi*grad_pi)
    reduced = s.factor(static.subs(
        {grad_phi: grad_psi, grad_pi: -B*grad_psi/C}))
    P_eff = P*A/C
    exact("independent_reduced_action", reduced, -P_eff*grad_psi**2)
    exact("action_and_constraint_source_agree",
          -s.diff(reduced, grad_psi)/grad_psi*lap_psi, source)
    state = {P: 1, A: s.Rational(1, 6), B: 1}
    exact("witness_positive_local_medium_density", extra.subs(state), 3)
    exact("witness_local_gravity_ratio", ratio.subs(state), 4)
    exact("witness_reduced_Einstein_coefficient", P_eff.subs(state),
          s.Rational(1, 4))

    # Reconstruct homogeneous derivative from its own original constraints.
    x, H, v, eps = s.symbols("X H_c v epsilon", real=True)
    K = medium_polynomial(x)
    k = K.subs(x, v**2/2)
    kx = s.diff(K, x).subs(x, v**2/2)
    rho = v**2*kx-k+3*H*v**3
    charge = v*kx+3*H*v**2
    constraints = s.Matrix([3*H**2-rho-eps, charge+1])
    origin = {H: 1, v: 1, eps: 0}
    response = -constraints.jacobian([H, v]).subs(origin).inv()*s.Matrix([-1, 0])
    density_response = (s.diff(rho, H)*response[0]
                        + s.diff(rho, v)*response[1]).subs(origin)
    exact("homogeneous_compensation_preserved", density_response,
          -s.Rational(1, 3))
    exact("mixing_response_channels_has_nonzero_residual",
          extra.subs(state)-density_response, s.Rational(10, 3))

    # Observable map only through the explicitly retained linear order.
    lam, psi = s.symbols("lambda Psi", real=True)
    clock = s.sqrt(1+2*lam*psi)
    rod = 1/s.sqrt(1-2*lam*psi)
    exact("linear_clock_rod_map",
          s.diff(clock-rod, lam).subs(lam, 0))
    exact("linear_coordinate_light_speed",
          s.diff(clock*rod, lam).subs(lam, 0), 2*psi)
    exact("linear_log_response",
          s.diff(-s.log(clock), lam).subs(lam, 0), -psi)
    # pi=-3 Psi/2 is a solution relation at this witness, not an absolute field map.
    exact("witness_perturbation_readout_relation",
          s.Rational(2, 3)*(-3*psi/2), -psi)

    # Inherited cosmological dictionary: its physical current identification
    # is conditional. A_op is the operational scale, not foundation scale.
    n, Aop = s.symbols("n_ratio A_operational", positive=True)
    p_map = n**s.Rational(1, 5)
    pressure_map = n**s.Rational(2, 5)
    exact("operational_foundation_volume_identity", p_map**3*pressure_map, n)
    exact("homogeneous_scale_identity",
          p_map.subs(n, Aop**-3), Aop**s.Rational(-3, 5))
    exact("homogeneous_pressure_identity",
          pressure_map.subs(n, Aop**-3), Aop**s.Rational(-6, 5))
    n_response = -(s.diff(charge, H)*response[0]
                   + s.diff(charge, v)*response[1]).subs(origin)
    exact("fixed_charge_family_has_zero_density_map_response", n_response)
    exact("fixed_charge_family_has_zero_cadence_response",
          s.diff(p_map, n).subs(n, 1)*n_response)
    exact("fixed_charge_family_has_zero_foundation_pressure_response",
          s.diff(pressure_map, n).subs(n, 1)*n_response)
    rho0 = rho.subs(origin)
    mechanical_pressure = k-v**2*s.Rational(1, 3)
    pressure0 = mechanical_pressure.subs(origin)
    exact("witness_medium_energy", rho0, 3)
    exact("witness_Hilbert_pressure", pressure0, -s.Rational(13, 3))
    rho_time = -3*(rho0+pressure0)
    pf_time = s.diff(pressure_map, n).subs(n, 1)*(-3)
    exact("energy_normalization_time_derivative", rho_time/rho0,
          s.Rational(4, 3))
    exact("inherited_pressure_time_derivative", pf_time, -s.Rational(6, 5))
    exact("direct_energy_pressure_identification_fails",
          rho_time/rho0-pf_time, s.Rational(38, 15))
    # W75's decreasing-loss theorem has a separate positive-enthalpy premise.
    Hdot = -(rho0+pressure0)/2
    cadence_second = s.Rational(9, 25)-s.Rational(3, 5)*Hdot
    exact("witness_Hdot_from_Hilbert_source", Hdot, s.Rational(2, 3))
    exact("inherited_cadence_second_derivative", cadence_second,
          -s.Rational(1, 25))
    control("W75_positive_enthalpy_premise_not_satisfied",
            rho0+pressure0 < 0)

    failed = [row for row in checks if not row["passed"]]
    return dict(
        decision=("LINEAR_READOUT_MATCH; DIRECT_PRESSURE_IDENTIFICATION_FAILS"
                  if not failed else "CHECK_FAILURE"),
        checks=len(checks), passed=len(checks)-len(failed), failed=failed,
        exact_results=dict(
            homogeneous_density_response=str(density_response),
            spatial_density_response=str(extra.subs(state)),
            spatial_gravity_ratio=str(ratio.subs(state)),
            normalized_energy_pressure_rate_mismatch=str(rho_time/rho0-pf_time)),
        scope=dict(
            linear_metric_readout_matched=not failed,
            response_channel_distinction_verified=not failed,
            direct_energy_pressure_identification_rejected=not failed,
            homogeneous_dictionary_is_conditional=True,
            quasistatic_sign_domain="P>0,A_eff>0; frozen leading spatial coefficients",
            full_RefG_pressure_law_derived=False,
            local_weak_gravity_suppression_demonstrated=False,
            all_strong_field_completions_excluded=False,
            singularity_resolved=False,
            observational_pass=False),
        details=checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--pressure-map-only", action="store_true",
                        help="Run the bounded pressure/readout identification audit.")
    args = parser.parse_args()
    result = run_pressure_map_checks() if args.pressure_map_only else run_checks()
    if not args.verbose:
        result.pop("details")
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return int(bool(result["failed"]))


if __name__ == "__main__":
    raise SystemExit(main())
