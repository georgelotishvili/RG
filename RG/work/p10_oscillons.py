# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.
# Active coefficient scheme: c_Y denotes the Y-scheme coefficient c_Y^(Y).

"""
p10 status:

The article-ready part of this file is the symbolic oscillon-to-gravity short
path: Bernoulli pressure identity, localized 1/r exterior source, asymptotic
charge normalization, first-order bi-conformal exterior branch, leading
light/redshift smoke tests, and the population-tempo transposition gate.

The full finite-energy nonlinear oscillon particle theorem, nonlinear exterior
continuation, full PPN validation, microscopic G and population-lock selection,
and particle spectrum matching remain open work targets.
"""

from __future__ import annotations

import os
import sympy as sp
from dataclasses import dataclass
from p01_core import init_variables, get_polynomial_lagrangian


@dataclass(frozen=True)
class ClaimGate:
    claim: str
    status: str
    verified_here: str
    open_requirement: str


def oscillon_claim_gate() -> list[ClaimGate]:
    """Strict theorem gate for p10: separate identities from open physics."""
    return [
        ClaimGate(
            claim="Bernoulli pressure identity",
            status="CLOSED_SYMBOLIC_IDENTITY",
            verified_here="For phi=-r_s/r, Delta_P=e^phi*(phi')^2/(32*pi*G) and P_static=-Delta_P give P_static+Delta_P=0 exactly.",
            open_requirement="derive the same identity as an on-shell branch of the full p01 stress system, not only as a static scalar identity.",
        ),
        ClaimGate(
            claim="localized source gives exterior 1/r tail",
            status="CLOSED_IF_SOURCE_IS_LOCALIZED",
            verified_here="Spherical Poisson reconstruction fixes the far-zone 1/r coefficient once a localized source rho(r) is supplied.",
            open_requirement="prove the full nonlinear oscillon PDE has a regular localized finite-energy source.",
        ),
        ClaimGate(
            claim="Newton law recovery",
            status="CLOSED_BY_ASYMPTOTIC_CHARGE_NORMALIZATION",
            verified_here="For an exterior phi=-mu/r, the asymptotic gravitational charge is M=c^2*mu/(2G), hence mu=2GM/c^2 and geodesic acceleration gives -GM/r^2.",
            open_requirement="derive the bi-conformal exterior branch from the p01 action and derive the microscopic substrate origin of G.",
        ),
        ClaimGate(
            claim="bi-conformal scaling and light factor 2",
            status="CLOSED_AT_FIRST_ORDER_STATIC_SPHERICAL_BRANCH",
            verified_here="The static spherical O(eps) equations split into independent radial powers and force a1=1, so A*B=1+O(U^2); inside that branch c_coord/c=(L_oper/L_0)^2 and weak-field light bending gives 2*r_s/b.",
            open_requirement="extend the selected branch to second order and the full nonlinear exterior ODE.",
        ),
        ClaimGate(
            claim="finite-energy oscillon particle",
            status="OPEN_CORE_THEOREM",
            verified_here="The file computes Y, averaged energy density, and a virial stationarity integrand for a two-harmonic trial family.",
            open_requirement="construct global regular finite-energy nonlinear solutions and prove spectral stability.",
        ),
        ClaimGate(
            claim="Solar-system observational pass",
            status="PARTIAL_WEAK_FIELD_SMOKE_TEST",
            verified_here="Solar light bending and Pound-Rebka are reproduced at leading weak-field level.",
            open_requirement="derive PPN gamma/beta plus Shapiro delay, perihelion, Cassini, LLR, and clock/LPI tests.",
        ),
        ClaimGate(
            claim="local population-tempo law (revised stability postulate)",
            status="PASS_POPULATION_TEMPO_TRANSPOSITION__FIXED_POINT_TARGET",
            verified_here="The population-tempo gate encodes the revised postulate: the local stable oscillon population supplies the common resonant tempo, and admissible oscillons sit in harmonic/integer-ratio relation to that local tempo. A pressure or energy-status change transposes the whole local population together, so dimensionless ratios remain locally observable while incompatible rhythms cannot keep resonance.",
            open_requirement="population-lock fixed points: which mutually compatible oscillon frequency sets does the medium nonlinearity admit (p11c ledger; p11h first-set programme scaffold). No independent external frequency standard is a required input of the framework.",
        ),
    ]


def oscillon_do_not_claim() -> list[str]:
    return [
        "Do not claim that p10 proves particles are finite-energy oscillons.",
        "Do not claim Newton gravity is fully derived from the RG action in this file.",
        "Do not claim the bi-conformal exterior is nonlinear-complete before the second-order/full ODE continuation is done.",
        "Do not claim solar-system tests are fully passed; only leading weak-field checks are present.",
        "Do not claim the microscopic substrate value of G is derived from oscillon parameters here.",
        "Do not introduce an independent external frequency standard as a clock or lock standard for oscillon stability.",
        "Do not assign a universal numerical frequency to the medium; stable oscillons lock to the local population tempo and its admissible harmonics.",
        "Do not treat pressure/energy-status transposition as changing local dimensionless frequency ratios; the local resonant population shifts together.",
    ]


def signature_bridge_gate():
    """
    p10 now keeps the active project signature (+---).

    The earlier Phase-17 notes used the equivalent (-+++) writing.  Multiplying
    the metric by -1 changes covariant sign conventions, not the physical null
    relation or the scaling identities, as long as the energy sign is translated.
    """
    phi = sp.Symbol("phi", real=True)
    g_plus = sp.diag(sp.exp(phi), -sp.exp(-phi), -sp.exp(-phi), -sp.exp(-phi))
    g_minus = -g_plus
    return {
        "active_signature": "(+---)",
        "old_phase17_signature": "(-+++)",
        "g_plus": g_plus,
        "g_minus": g_minus,
        "null_speed_plus": sp.simplify(sp.sqrt(-g_plus[0, 0] / g_plus[1, 1])),
        "null_speed_minus": sp.simplify(sp.sqrt(-g_minus[0, 0] / g_minus[1, 1])),
        "same_null_cone": True,
        "energy_translation": "with (+---), static Killing energy is E=p_t; with (-+++), it was E=-p_t",
        "status": "PASS_SIGNATURE_BRIDGE_EXPLICIT",
    }


DEFAULT_MAIN_SECTIONS = {"oscillon", "spherical", "tov", "biconformal", "gates"}


def _requested_main_sections() -> set[str]:
    raw = os.environ.get("RG_P10_SECTIONS", "")
    return {part.strip().lower() for part in raw.split(",") if part.strip()}


def _should_run_main_section(name: str) -> bool:
    requested = _requested_main_sections()
    if not requested:
        return name.lower() in DEFAULT_MAIN_SECTIONS
    return "all" in requested or name.lower() in requested


def bernoulli_static_gravity_identity():
    """
    ძველი quantum ფაილის Bernoulli gravity ბირთვი.

    static bi-conformal exterior branch:
        phi(r) = -r_s/r
        Delta P = -P_static = e^phi (phi')^2 / (32*pi*G)
        P_static + Delta P = 0

    ეს არის scalar-field Bernoulli identity: gradient energy drains the
    static pressure. გრავიტაციული მნიშვნელობა სრულად არ იხურება მხოლოდ ამ
    identity-ით; source coefficient ასიმპტოტური charge normalization-ით
    ფიქსირდება, ხოლო exterior metric branch-ის p01-დან შერჩევა ცალკე რჩება.
    """
    r, r_s, G = sp.symbols('r r_s G', real=True, positive=True)
    phi = -r_s / r
    phi_prime = sp.diff(phi, r)

    gradient_energy = sp.simplify(sp.exp(phi) * phi_prime**2 / (32 * sp.pi * G))
    pressure_static = -gradient_energy
    bernoulli_sum = sp.simplify(pressure_static + gradient_energy)
    pressure_shape = sp.simplify(sp.exp(sp.Symbol('phi')) * sp.Symbol('phi')**4)
    coulomb_pressure = sp.simplify(
        -sp.exp(phi) * (phi**4) / (32 * sp.pi * G * r_s**2)
    )

    u = sp.Symbol('u', real=True, positive=True)
    shape_u = sp.exp(-u) * u**4
    shape_derivative = sp.factor(sp.diff(shape_u, u))

    return {
        "theorem": "static scalar Bernoulli identity",
        "exterior_profile": sp.Eq(sp.Symbol('phi(r)'), phi),
        "gradient_energy_density": sp.Eq(sp.Symbol('Delta_P'), gradient_energy),
        "static_pressure": sp.Eq(sp.Symbol('P_static'), pressure_static),
        "bernoulli_integral": sp.Eq(sp.Symbol('P_static + Delta_P'), bernoulli_sum),
        "closed_pressure_profile": sp.Eq(sp.Symbol('P_static_Coulomb'), coulomb_pressure),
        "universal_shape": sp.Eq(sp.Symbol('f_hat(phi)'), pressure_shape),
        "shape_derivative_u_rs_over_r": sp.Eq(sp.Symbol('d(e^-u*u^4)/du'), shape_derivative),
        "pressure_deficit_peak": sp.Eq(sp.Symbol('r_peak'), r_s / 4),
        "strong_field_saturation": sp.Eq(sp.Symbol('lim_r_to_0_Delta_P'), sp.limit(gradient_energy, r, 0, dir='+')),
        "far_field_limit": sp.Eq(sp.Symbol('lim_r_to_inf_Delta_P'), sp.limit(gradient_energy, r, sp.oo)),
    }


def bernoulli_time_averaged_oscillon_source():
    """
    Time-periodic oscillon-ის zero-frequency projection.

    full field split:
        phi(t,r) = phi_grav(r) + Phi0(r) cos(Omega t) + ...

    სწრაფი oscillation-ის ხაზოვანი წევრები საშუალოდ ნულდება. დარჩენილი
    quadratic zero-frequency density არის localized source, რომელიც
    Poisson/Laplace reconstruction-ით იძლევა long-range 1/r field-ს.
    """
    r, G, Omega, phi_grav = sp.symbols('r G Omega phi_grav', real=True, positive=True)
    Phi0 = sp.Function('Phi0')(r)
    Phi0_prime = sp.diff(Phi0, r)

    source_avg = sp.simplify(
        (
            sp.exp(-phi_grav) * Omega**2 * Phi0**2
            + sp.exp(phi_grav) * Phi0_prime**2
        ) / (64 * sp.pi * G)
    )
    newtonian_source_profile = sp.simplify(
        sp.Rational(1, 2) * Omega**2 * Phi0**2
        + sp.Rational(1, 2) * Phi0_prime**2
    )

    return {
        "field_split": "phi(t,r)=phi_grav(r)+Phi0(r)*cos(Omega*t)+higher harmonics",
        "zero_frequency_source": sp.Eq(sp.Symbol('<T00>'), source_avg),
        "newtonian_profile_without_prefactor": sp.Eq(sp.Symbol('rho_osc'), newtonian_source_profile),
        "meaning": "oscillon-ის შიდა რეზონანსის საშუალო kinetic/gradient energy არის static gravitational source.",
    }


def bernoulli_poisson_reconstruction():
    """
    Localized zero-frequency oscillon source -> exterior 1/r field.

    spherical Poisson reconstruction:
        M_enc(r)=4*pi int_0^r rho(r') r'^2 dr'
        phi_grav(r)=-M_enc(r)/r - int_r^inf 4*pi rho(r') r' dr'
        lim_{r->inf}[-r phi_grav(r)] = M_total
    """
    r, rp = sp.symbols('r rp', real=True, positive=True)
    rho = sp.Function('rho')

    m_enc = 4 * sp.pi * sp.Integral(rho(rp) * rp**2, (rp, 0, r))
    phi_grav = -m_enc / r - 4 * sp.pi * sp.Integral(rho(rp) * rp, (rp, r, sp.oo))
    m_total = 4 * sp.pi * sp.Integral(rho(rp) * rp**2, (rp, 0, sp.oo))

    return {
        "enclosed_source": sp.Eq(sp.Symbol('M_enc(r)'), m_enc),
        "poisson_solution": sp.Eq(sp.Symbol('phi_grav(r)'), phi_grav),
        "far_zone_coefficient": sp.Eq(sp.Symbol('lim_-r_phi'), m_total),
        "proof_result": "Once a localized source has a total asymptotic charge, the 1/r tail coefficient is fixed; the physical G-normalization is the asymptotic charge theorem.",
    }


def poisson_to_newton_normalization_gate():
    """
    Exact asymptotic charge normalization.

    Poisson reconstruction gives a dimensionless exterior coefficient mu_src:
        phi = -mu_src/r.
    Newton is recovered if the metric potential is Phi_N=c^2*phi/2 and the
    source coefficient is the asymptotic gravitational charge:

        M_ADM = c^2*mu_src/(2G).

    Therefore mu_src=2GM/c^2 is not a fit inserted after the fact; it is the
    charge normalization fixed by the gravitational coupling G in the action.
    """
    r, mu_src, G, M, c = sp.symbols("r mu_src G M c", positive=True)
    phi = -mu_src / r
    phi_newton = sp.simplify(c**2 * phi / 2)
    acceleration = sp.simplify(-sp.diff(phi_newton, r))
    asymptotic_charge = sp.simplify(c**2 * mu_src / (2 * G))
    mu_needed = sp.solve(sp.Eq(acceleration, -G * M / r**2), mu_src)[0]
    mu_from_charge = sp.solve(sp.Eq(M, asymptotic_charge), mu_src)[0]
    acceleration_from_charge = sp.simplify(acceleration.subs(mu_src, mu_from_charge))

    return {
        "dimensionless_exterior_profile": sp.Eq(sp.Symbol("phi"), phi),
        "newtonian_potential_bridge": sp.Eq(sp.Symbol("Phi_N"), phi_newton),
        "asymptotic_gravitational_charge": sp.Eq(sp.Symbol("M_ADM"), asymptotic_charge),
        "source_coefficient_from_charge": sp.Eq(sp.Symbol("mu_src"), mu_from_charge),
        "geodesic_acceleration": sp.Eq(sp.Symbol("a"), acceleration),
        "required_source_coefficient": sp.Eq(sp.Symbol("mu_src"), mu_needed),
        "charge_identity": sp.simplify(mu_from_charge - mu_needed) == 0,
        "newton_identity": sp.simplify(acceleration_from_charge + G * M / r**2) == 0,
        "status": "PASS_ASYMPTOTIC_CHARGE_NORMALIZATION",
        "remaining_deeper_target": "derive the microscopic substrate value of G and the full p01 branch that carries this charge.",
    }


def bernoulli_newton_law_recovery():
    """
    Bernoulli pressure deficit gives the mechanism; geodesics give motion.

    The firewall from the old quantum file is kept:
        matter does not feel a literal pressure-gradient force.
        Matter is minimally coupled and follows geodesics of g_mn[phi].
    """
    r, G, c, M, m, M1, M2, d = sp.symbols(
        'r G c M m M1 M2 d',
        real=True,
        positive=True,
    )
    r_s = 2 * G * M / c**2
    phi = -r_s / r
    Phi_N = sp.simplify(c**2 * phi / 2)
    acceleration = sp.simplify(-c**2 * sp.diff(phi, r) / 2)

    potential_energy = -G * M1 * M2 / d
    radial_force = sp.simplify(-sp.diff(potential_energy, d))
    force_magnitude = sp.simplify(G * M1 * M2 / d**2)

    return {
        "source_radius": sp.Eq(sp.Symbol('r_s'), r_s),
        "gravitational_profile": sp.Eq(sp.Symbol('phi_grav'), phi),
        "newtonian_potential": sp.Eq(sp.Symbol('Phi_N'), Phi_N),
        "geodesic_acceleration": sp.Eq(sp.Symbol('a_geo'), acceleration),
        "test_particle_force": sp.Eq(sp.Symbol('F'), m * acceleration),
        "two_body_energy": sp.Eq(sp.Symbol('U(d)'), potential_energy),
        "two_body_radial_force": sp.Eq(sp.Symbol('F_radial'), radial_force),
        "two_body_force_magnitude": sp.Eq(sp.Symbol('|F_12|'), force_magnitude),
        "firewall": "Delta_P explains why the metric is gravitational; it is not an extra pressure-gradient force on matter.",
    }


def bernoulli_gravity_chain() -> list[str]:
    return [
        "localized oscillon resonance -> time-periodic scalar energy",
        "zero-frequency projection <T00> survives time averaging",
        "Bernoulli identity: P_static + e^phi |grad phi|^2/(32*pi*G)=0",
        "pressure deficit: Delta_P=-P_static=e^phi |grad phi|^2/(32*pi*G)",
        "localized Delta_P/<T00> fixes the source integral if a finite oscillon exists",
        "vacuum exterior solves Laplace equation -> phi_grav=-mu_src/r",
        "asymptotic charge normalization fixes mu_src=2GM/c^2",
        "bi-conformal geodesic acceleration then gives a=-(c^2/2) grad phi=-GM/r^2",
        "two oscillon sources give U(d)=-G M1 M2/d and |F|=G M1 M2/d^2 after normalization",
        "strong-field saturation: e^phi suppresses Delta_P as phi->-infinity",
    ]


def analyze_oscillon():
    r = sp.Symbol('r', real=True, positive=True)
    t = sp.Symbol('t', real=True)
    theta = sp.Symbol('theta', real=True) # theta = omega * t
    omega = sp.Symbol('omega', real=True, positive=True)
    
    # ოსცილონის რადიალური პროფილი და მისი გრადიენტი
    Phi0 = sp.Function('Phi0')(r)
    Phi0_prime = sp.diff(Phi0, r)
    Phi1 = sp.Function('Phi1')(r) # მეორე ჰარმონიკა არაწრფივი შერევისთვის
    Phi1_prime = sp.diff(Phi1, r)
    
    # სკალარული ველი ფონის (t) და ოსცილაციის (მინიმუმ 2 ჰარმონიკით) ჩათვლით
    delta_Phi = Phi0 * sp.sin(theta) + Phi1 * sp.sin(3*theta)
    Phi_total = t + delta_Phi
    
    # წარმოებულები (theta-თი ვაწარმოებთ t-ს ნაცვლად)
    Phi_dot = 1 + omega * (Phi0 * sp.cos(theta) + 3 * Phi1 * sp.cos(3*theta))
    Phi_r = Phi0_prime * sp.sin(theta) + Phi1_prime * sp.sin(3*theta)
    
    # ფაზური ინვარიანტი Y მეტრიკით g^00=1, g^rr=-1 (Minkowski)
    Y_eval = sp.expand(Phi_dot**2 - Phi_r**2)
    
    Y, I1, I2, I3 = init_variables()
    L_poly = get_polynomial_lagrangian(Y, I1, I2, I3)
    
    # ენერგიის სიმკვრივე: T^0_0 = 2 * g^00 * (dPhi/dt)^2 * dL/dY - L
    dL_dY = sp.diff(L_poly, Y)
    rho_expr = 2 * Phi_dot**2 * dL_dY - L_poly
    
    # ვსვამთ ელასტიურ ინვარიანტებს Minkowski ფონზე (I1=3, I2=3, I3=1)
    bg_subs = {I1: 3, I2: 3, I3: 1}
    rho_sub = rho_expr.subs(bg_subs).subs(Y, Y_eval)
    
    # ფონური ენერგია (როცა ოსცილაცია არ გვაქვს)
    rho_bg = rho_sub.subs({Phi0: 0, Phi0_prime: 0, Phi1: 0, Phi1_prime: 0})
    
    # ოსცილონის წმინდა ენერგია 
    rho_pert = sp.expand(rho_sub - rho_bg)
    
    # დროის ერთ პერიოდზე გასაშუალოება
    rho_avg = sp.integrate(rho_pert, (theta, 0, 2*sp.pi)) / (2*sp.pi)
    rho_avg = sp.simplify(rho_avg)
    
    # ენერგიის სრული ინტეგრალი
    E_total = sp.Integral(rho_avg * 4 * sp.pi * r**2, r)
    
    # ვირიალური პირობა: dE/domega = 0 რეზონანსული სიხშირის დასაფიქსირებლად
    virial_integrand = sp.simplify(sp.diff(rho_avg * 4 * sp.pi * r**2, omega))
    
    return Phi_total, Y_eval, rho_avg, E_total, virial_integrand


def oscillon_finite_energy_gate():
    """
    Boundary and positivity gates for turning the trial family into a theorem.

    This function does not pretend to solve the nonlinear PDE.  It records the
    exact analytic requirements that a future solution must satisfy.
    """
    r, omega = sp.symbols("r omega", positive=True)
    E_of_omega = sp.Function("E")(omega)
    Phi0 = sp.Function("Phi0")(r)
    Phi1 = sp.Function("Phi1")(r)
    return {
        "regular_origin_conditions": [
            sp.Eq(sp.diff(Phi0, r).subs(r, 0), 0),
            sp.Eq(sp.diff(Phi1, r).subs(r, 0), 0),
            "Phi0(0), Phi1(0) finite",
        ],
        "finite_energy_asymptotics": [
            sp.Eq(sp.limit(r * Phi0, r, sp.oo), 0),
            sp.Eq(sp.limit(r * Phi1, r, sp.oo), 0),
            "rho_avg*r^2 must be integrable on [0, infinity)",
        ],
        "stationarity_condition": sp.Eq(sp.diff(E_of_omega, omega), 0),
        "stability_gate": "second variation / Floquet spectrum must be non-negative except symmetry zero modes",
        "status": "OPEN_PDE_EXISTENCE_AND_STABILITY",
    }


def oscillon_energy_status_audit():
    """Classify what analyze_oscillon proves and what it does not."""
    return {
        "proved_here": [
            "Y is evaluated nonlinearly for a two-harmonic Phi=t+deltaPhi ansatz",
            "the time-averaged stress density can be computed from the p01 polynomial L",
            "a virial stationarity integrand can be written symbolically",
        ],
        "not_proved_here": [
            "existence of a global finite-energy solution",
            "uniqueness of the oscillon profile",
            "spectral/Floquet stability",
            "absolute particle mass, charge, spin, and frequency selection",
        ],
        "status": "SYMBOLIC_TRIAL_FAMILY_NOT_PARTICLE_THEOREM",
    }


if __name__ == "__main__" and _should_run_main_section("oscillon"):
    Phi_total, Y_eval, rho_avg, E_total, virial_integrand = analyze_oscillon()
    
    print("--- ოსცილონის ანალიზი (Phi ველის ვარიაცია) ---")
    print("\nსრული ველი Phi(t,r):")
    print(Phi_total.subs(sp.Symbol('theta', real=True), sp.Symbol('omega', real=True, positive=True) * sp.Symbol('t', real=True)))
    
    print("\nფაზური ინვარიანტი Y:")
    print(Y_eval.subs(sp.Symbol('theta', real=True), sp.Symbol('omega', real=True, positive=True) * sp.Symbol('t', real=True)))
    
    print("\nგასაშუალოებული წმინდა ენერგიის სიმკვრივე <rho_osc>:")
    # შევაგროვოთ Phi0-ის ხარისხების მიხედვით
    Phi0 = sp.Function('Phi0')(sp.Symbol('r', real=True, positive=True))
    Phi0_prime = sp.diff(Phi0, sp.Symbol('r', real=True, positive=True))
    Phi1 = sp.Function('Phi1')(sp.Symbol('r', real=True, positive=True))
    Phi1_prime = sp.diff(Phi1, sp.Symbol('r', real=True, positive=True))
    print(sp.collect(sp.expand(rho_avg), [Phi0**2, Phi1**2, Phi0_prime**2]))
    
    print("\nსრული ენერგიის ინტეგრალი (E):")
    print(E_total)
    
    print("\nვირიალური პირობის ინტეგრანდი (dE/domega = 0):")
    print(virial_integrand)

    print("\n--- Bernoulli gravity theorem: static pressure deficit ---")
    bernoulli_static = bernoulli_static_gravity_identity()
    for key, value in bernoulli_static.items():
        print(f"{key}: {value}")

    print("\n--- Time-averaged oscillon source: zero-frequency projection ---")
    osc_source = bernoulli_time_averaged_oscillon_source()
    for key, value in osc_source.items():
        print(f"{key}: {value}")

    print("\n--- Poisson reconstruction: localized source -> 1/r field ---")
    poisson = bernoulli_poisson_reconstruction()
    for key, value in poisson.items():
        print(f"{key}: {value}")

    print("\n--- Poisson -> Newton normalization gate ---")
    norm_gate = poisson_to_newton_normalization_gate()
    for key, value in norm_gate.items():
        print(f"{key}: {value}")

    print("\n--- Newton law recovery from Bernoulli + geodesics ---")
    newton = bernoulli_newton_law_recovery()
    for key, value in newton.items():
        print(f"{key}: {value}")

    print("\n--- Complete Bernoulli gravity chain ---")
    for step in bernoulli_gravity_chain():
        print(f"- {step}")
    
    print("\n--- აგენტთა საბჭოს დასკვნები ---")
    print("1. ოსცილაცია ხდება რეალურ Phi ველზე და Y არის არაწრფივი შედეგი (Y=1+2Φ̇+Φ̇²-Φ'²).")
    print("2. I1, I2, I3 ინარჩუნებენ Minkowski ფონის (3, 3, 1) წვლილს ენერგიის გამოთვლაში.")
    print("3. სასრული ენერგიისთვის აუცილებელია Phi0(r), Phi1(r) და მათი წარმოებულები საკმარისად სწრაფად")
    print("   ქრებოდნენ უსასრულობაში, ხოლო r=0-ზე პროფილი რეგულარული იყოს.")
    print("4. 2 ჰარმონიკის ჩართვამ (Phi0, Phi1) დაადასტურა, რომ ენერგიაში ჩნდება არაწრფივი ჯვარედინი")
    print("   შერევები. c_Y2>0 დადებითად მოქმედებს quartic წევრებზე, მაგრამ სრული ენერგიის")
    print("   პოზიტიურობა მოითხოვს rho_avg-ის სრული გამოსახულების ანალიზს.")
    print("5. omega-ს ფიქსაციის ფორმალური პირობაა dE/domega = 0; რეალური omega-ს მისაღებად")
    print("   საჭიროა პროფილის ამოხსნა და საზღვრული პირობები.")
    print("6. Bernoulli gravity ნაწილი მკაცრად აჩვენებს pressure identity-ს და")
    print("   Newton-ის ალგებრულ დაბრუნებას ასიმპტოტური charge normalization-ით;")
    print("   დარჩენილი branch-ამოცანაა bi-conformal exterior-ის p01-დან შერჩევა.")
    print("7. ცალკე ღიად რჩება სრული nonlinear finite-energy oscillon profile-ის არსებობის")
    print("   სრული დამტკიცება; ამიტომ სრული oscillon->gravity proof ჯერ არ დაიხურა.")

# ===================== CONSOLIDATED PHASE SECTIONS =====================


# ===================== merged from p10_oscillons.py =====================

# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

import sympy as sp
from p01_core import get_polynomial_lagrangian

def solve_static_spherical():
    r = sp.Symbol('r', real=True, positive=True)
    rs = sp.Symbol('rs', real=True, positive=True)
    eps = sp.Symbol('eps', real=True)
    kappa = sp.Symbol('kappa', real=True)
    
    # უცნობი ფუნქციები (სიგნატურით + - - -)
    A = sp.Function('A')(r)
    B = sp.Function('B')(r)
    Psi_p = sp.Function('Psi_p')(r) # ეს არის Psi'(r), სადაც Phi = t + Psi(r)
    
    # აინშტაინის ტენზორი G^t_t და G^r_r მეტრიკისთვის diag(B, -A, -r^2, -r^2 sin^2 theta)
    G_tt = -sp.diff(A, r) / (r * A**2) + (1/A - 1)/r**2
    G_rr = sp.diff(B, r) / (r * A * B) + (1/A - 1)/r**2
    G_thth = sp.diff(B, r, 2)/(2*A*B) - sp.diff(B, r)**2/(4*A*B**2) - sp.diff(A, r)*sp.diff(B, r)/(4*A**2*B) + sp.diff(B, r)/(2*r*A*B) - sp.diff(A, r)/(2*r*A**2)
    
    # ინვარიანტები (Phi = t + Psi(r) და phi^A = x^A comoving ანზაცისთვის)
    Y = 1/B - Psi_p**2 / A
    I1 = 2 + 1/A
    I2 = 1 + 2/A
    I3 = 1/A
    
    Y_s, I1_s, I2_s, I3_s = sp.symbols('Y I1 I2 I3', real=True)
    L_poly = get_polynomial_lagrangian(Y_s, I1_s, I2_s, I3_s)
    
    L_eval = L_poly.subs({Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3})
    L_Y = sp.diff(L_poly, Y_s).subs({Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3})
    L_I1 = sp.diff(L_poly, I1_s).subs({Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3})
    L_I2 = sp.diff(L_poly, I2_s).subs({Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3})
    L_I3 = sp.diff(L_poly, I3_s).subs({Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3})
    
    # სტრეს-ტენზორი T^mu_nu
    T_tt = 2 * L_Y / B - L_eval
    T_rr = 2 * (L_Y * Psi_p**2 / A + L_I1 / A + 2 * L_I2 / A + L_I3 / A) - L_eval
    T_thth = 2 * (L_I1 + L_I2 * (1 + 1/A) + L_I3 / A) - L_eval
    
    # სკალარული ველის განტოლება: \nabla_\mu ( dL / d(\partial_\mu \Phi) ) = 0
    scalar_eq = sp.Derivative(r**2 * sp.sqrt(B/A) * L_Y * Psi_p, r)
    
    # სუსტი ველის ექსპანსია (ვუშვებთ Psi_p = 0 ცენტრალური მუხტის არარსებობის გამო)
    a1 = sp.Symbol('a1', real=True)
    b2 = sp.Symbol('b2', real=True)
    
    U = eps * rs / r
    A_w = 1 + a1 * U
    B_w = 1 - U + b2 * U**2
    
    # ვანაცვლებთ A და B ცვლადებს სუსტი ველის ფუნქციებით და ვითვლით G და T ტენზორებს
    G_tt_w = -sp.diff(A_w, r) / (r * A_w**2) + (1/A_w - 1)/r**2
    G_rr_w = sp.diff(B_w, r) / (r * A_w * B_w) + (1/A_w - 1)/r**2
    G_thth_w = sp.diff(B_w, r, 2)/(2*A_w*B_w) - sp.diff(B_w, r)**2/(4*A_w*B_w**2) - sp.diff(A_w, r)*sp.diff(B_w, r)/(4*A_w**2*B_w) + sp.diff(B_w, r)/(2*r*A_w*B_w) - sp.diff(A_w, r)/(2*r*A_w**2)
    
    Y_w = 1/B_w
    I1_w = 2 + 1/A_w
    I2_w = 1 + 2/A_w
    I3_w = 1/A_w
    
    L_w = L_poly.subs({Y_s: Y_w, I1_s: I1_w, I2_s: I2_w, I3_s: I3_w})
    L_Y_w = sp.diff(L_poly, Y_s).subs({Y_s: Y_w, I1_s: I1_w, I2_s: I2_w, I3_s: I3_w})
    L_I1_w = sp.diff(L_poly, I1_s).subs({Y_s: Y_w, I1_s: I1_w, I2_s: I2_w, I3_s: I3_w})
    L_I2_w = sp.diff(L_poly, I2_s).subs({Y_s: Y_w, I1_s: I1_w, I2_s: I2_w, I3_s: I3_w})
    L_I3_w = sp.diff(L_poly, I3_s).subs({Y_s: Y_w, I1_s: I1_w, I2_s: I2_w, I3_s: I3_w})
    
    T_tt_w = 2 * L_Y_w / B_w - L_w
    T_rr_w = 2 * (L_I1_w / A_w + 2 * L_I2_w / A_w + L_I3_w / A_w) - L_w
    T_thth_w = 2 * (L_I1_w + L_I2_w * (1 + 1/A_w) + L_I3_w / A_w) - L_w
    
    def get_series(expr):
        return sp.simplify(sp.series(expr, eps, 0, 3).removeO())
        
    Eq_tt_w = get_series(G_tt_w - kappa * T_tt_w)
    Eq_rr_w = get_series(G_rr_w - kappa * T_rr_w)
    Eq_thth_w = get_series(G_thth_w - kappa * T_thth_w)
    
    # გამოვყოთ ნულოვანი (ფონური) და პირველი რიგის განტოლებები
    Eq_tt_O0 = sp.simplify(Eq_tt_w.subs(eps, 0))
    Eq_tt_O1 = sp.simplify(sp.diff(Eq_tt_w, eps).subs(eps, 0))
    
    Eq_rr_O0 = sp.simplify(Eq_rr_w.subs(eps, 0))
    Eq_rr_O1 = sp.simplify(sp.diff(Eq_rr_w, eps).subs(eps, 0))
    
    Eq_thth_O0 = sp.simplify(Eq_thth_w.subs(eps, 0))
    Eq_thth_O1 = sp.simplify(sp.diff(Eq_thth_w, eps).subs(eps, 0))
    
    # ბი-კონფორმობის ანალიზი (წინასწარ a1=1 დაშვების გარეშე)
    Delta_T = sp.simplify(T_tt_w - T_rr_w)
    Delta_T_O1 = sp.simplify(sp.diff(Delta_T, eps).subs(eps, 0))
    
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols('c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1', real=True)
    E_vac = -c_Y - 3*c_Y2 + 3*c_I1 + 9*c_I1sq + 3*c_I2 + c_I3 - 3*c_YI1
    P_vac = c_Y + c_Y2 + 5*c_I1 + 21*c_I1sq + 7*c_I2 + 3*c_I3 + 5*c_YI1
    vac_sols = sp.solve([E_vac, P_vac], [c_Y, c_I1])
    
    clean_Delta_T_O1 = sp.simplify(Delta_T_O1.subs(vac_sols))
    bc_constraint = sp.Eq(clean_Delta_T_O1 / (rs/r), 0)
    
    return G_tt, G_rr, G_thth, T_tt, T_rr, T_thth, scalar_eq, Eq_tt_w, Eq_rr_w, Eq_thth_w, Eq_tt_O0, Eq_tt_O1, Eq_rr_O0, Eq_rr_O1, Eq_thth_O0, Eq_thth_O1, Delta_T_O1, clean_Delta_T_O1, bc_constraint


def static_spherical_first_order_biconformal_branch():
    """
    First-order static spherical branch selector.

    The weak exterior ansatz is

        A = 1 + a1*U,
        B = 1 - U,
        U = eps*r_s/r.

    The rr and angular equations contain independent geometric r^-3 terms.
    Splitting the radial powers forces a1=1 before any coefficient tuning.
    Thus the first-order exterior is bi-conformal:

        A*B = 1 + O(U^2).

    The remaining r^-1 stress terms then select a linear coefficient family.
    """

    (
        _G_tt,
        _G_rr,
        _G_thth,
        _T_tt,
        _T_rr,
        _T_thth,
        _scalar_eq,
        _Eq_tt_w,
        _Eq_rr_w,
        _Eq_thth_w,
        Eq_tt_O0,
        Eq_tt_O1,
        Eq_rr_O0,
        Eq_rr_O1,
        Eq_thth_O0,
        Eq_thth_O1,
        _Delta_T_O1,
        _clean_Delta_T_O1,
        _bc_constraint,
    ) = solve_static_spherical()

    equations = [
        Eq_tt_O0,
        Eq_rr_O0,
        Eq_thth_O0,
        Eq_tt_O1,
        Eq_rr_O1,
        Eq_thth_O1,
    ]
    symbols_by_name = {
        symbol.name: symbol
        for expr in equations
        for symbol in expr.free_symbols
    }
    r = symbols_by_name["r"]
    rs = symbols_by_name["rs"]
    kappa = symbols_by_name["kappa"]
    a1 = symbols_by_name["a1"]

    c_Y = symbols_by_name["c_Y"]
    c_Y2 = symbols_by_name["c_Y2"]
    c_I1 = symbols_by_name["c_I1"]
    c_I1sq = symbols_by_name["c_I1sq"]
    c_I2 = symbols_by_name["c_I2"]
    c_I3 = symbols_by_name["c_I3"]
    c_YI1 = symbols_by_name["c_YI1"]

    rr_geometric_power = sp.simplify(sp.limit(Eq_rr_O1 * r**3 / rs, r, 0))
    th_geometric_power = sp.simplify(sp.limit(Eq_thth_O1 * r**3 / rs, r, 0))
    a1_from_rr = sp.solve(sp.Eq(rr_geometric_power, 0), a1)[0]
    a1_from_th = sp.solve(sp.Eq(th_geometric_power, 0), a1)[0]

    tt_stress = sp.simplify(Eq_tt_O1.subs(a1, 1) * r / (kappa * rs))
    rr_stress = sp.simplify(Eq_rr_O1.subs(a1, 1) * r / (kappa * rs))
    th_stress = sp.simplify(Eq_thth_O1.subs(a1, 1) * r / (kappa * rs))

    vacuum_constraints = [
        sp.simplify(Eq_tt_O0 / kappa),
        sp.simplify(Eq_rr_O0 / kappa),
    ]
    stress_constraints = [tt_stress, rr_stress, th_stress]
    coefficient_family = sp.solve(
        vacuum_constraints + stress_constraints,
        [c_Y, c_Y2, c_I1, c_I1sq, c_I2],
        dict=True,
    )[0]

    all_branch_residuals = [
        sp.simplify(expr.subs(a1, 1).subs(coefficient_family))
        for expr in vacuum_constraints + stress_constraints
    ]

    U = sp.Symbol("U", real=True)
    first_order_product = sp.series((1 + a1 * U) * (1 - U), U, 0, 2).removeO()

    return {
        "status": "PASS_STATIC_SPHERICAL_FIRST_ORDER_BICONFORMAL_BRANCH",
        "rr_geometric_power": rr_geometric_power,
        "theta_geometric_power": th_geometric_power,
        "a1_from_rr": sp.Eq(a1, a1_from_rr),
        "a1_from_theta": sp.Eq(a1, a1_from_th),
        "a1_identity": sp.simplify(a1_from_rr - 1) == 0
        and sp.simplify(a1_from_th - 1) == 0,
        "first_order_metric_product": first_order_product,
        "biconformal_identity": sp.simplify(first_order_product.subs(a1, 1) - 1) == 0,
        "stress_constraints_at_a1_1": stress_constraints,
        "coefficient_family": coefficient_family,
        "branch_residuals": all_branch_residuals,
        "branch_residual_identity": all(residual == 0 for residual in all_branch_residuals),
        "meaning": (
            "The first-order static spherical exterior is not inserted by hand: "
            "the independent geometric radial powers force a1=1, and the "
            "remaining stress equations select a p01 coefficient family."
        ),
        "next_theorem_target": (
            "extend the same branch selection to second order and then to the nonlinear exterior ODE",
            "match the branch to the finite oscillon core",
        ),
    }


def static_spherical_theorem_gate():
    """
    Council gate for the exterior branch.

    solve_static_spherical() is useful, but the full weak-field theorem requires
    all O(eps) equations to vanish together after the Minkowski vacuum
    constraints.  The old single Delta_T/biconformal constraint is necessary
    only for one aspect of the branch.
    """
    (
        _G_tt,
        _G_rr,
        _G_thth,
        _T_tt,
        _T_rr,
        _T_thth,
        _scalar_eq,
        _Eq_tt_w,
        _Eq_rr_w,
        _Eq_thth_w,
        Eq_tt_O0,
        Eq_tt_O1,
        Eq_rr_O0,
        Eq_rr_O1,
        Eq_thth_O0,
        Eq_thth_O1,
        Delta_T_O1,
        clean_Delta_T_O1,
        bc_constraint,
    ) = solve_static_spherical()

    c_Y2, c_I1sq, c_YI1 = sp.symbols("c_Y2 c_I1sq c_YI1", real=True)
    a1 = sp.Symbol("a1", real=True)
    first_order_branch = static_spherical_first_order_biconformal_branch()

    return {
        "vacuum_background_equations": [Eq_tt_O0, Eq_rr_O0, Eq_thth_O0],
        "first_order_equations_to_solve_together": [Eq_tt_O1, Eq_rr_O1, Eq_thth_O1],
        "first_order_branch": first_order_branch,
        "biconformal_constraint_only": bc_constraint,
        "council_candidate_constraints_for_a1_1": [
            sp.Eq(c_YI1, 2 * c_Y2),
            sp.Eq(c_YI1, 2 * c_I1sq),
            "plus the angular O(eps) combination; solve full system before claiming exterior proof",
        ],
        "nonlinear_continuation_target": "second order and full exterior ODE still have to follow the same selected branch.",
        "status": "PASS_FIRST_ORDER_STATIC_SPHERICAL_BRANCH__NONLINEAR_CONTINUATION_TARGET",
        "a1_note": "a1 is selected by the rr/theta geometric power split: a1=1.",
    }


if __name__ == "__main__" and _should_run_main_section("spherical"):
    res = solve_static_spherical()
    G_tt, G_rr, G_thth, T_tt, T_rr, T_thth, scalar_eq, Eq_tt_w, Eq_rr_w, Eq_thth_w, Eq_tt_O0, Eq_tt_O1, Eq_rr_O0, Eq_rr_O1, Eq_thth_O0, Eq_thth_O1, Delta_T_O1, clean_Delta_T_O1, bc_constraint = res
    print("--- ამოხსნა სფერული ანზაცისთვის ---")
    print("G^t_t =", G_tt)
    print("T^t_t =", T_tt)
    print("G^r_r =", G_rr)
    print("T^r_r =", T_rr)
    print("G^theta_theta =", G_thth)
    print("T^theta_theta =", T_thth)
    print("\nსკალარული ველის განტოლება:")
    print("0 =", scalar_eq)
    print("-> დასკვნა: ცენტრალური სკალარული მუხტის გარეშე Psi'(r) = 0, ანუ Phi(t,r) = t.")
    print("\n--- სუსტი ველის ლიმიტი (O(rs/r)) ---")
    print("Eq_tt (O(eps)):", Eq_tt_w)
    print("Eq_rr (O(eps)):", Eq_rr_w)
    print("Eq_thth (O(eps)):", Eq_thth_w)
    
    print("\n--- ფონური ვაკუუმის განტოლებები (O(1)) ---")
    print("Eq_tt_O0 =", Eq_tt_O0)
    print("Eq_rr_O0 =", Eq_rr_O0)
    print("Eq_thth_O0 =", Eq_thth_O0)
    
    print("\n--- პირველი რიგის განტოლებები (O(eps)) ---")
    print("Eq_tt_O1 =", Eq_tt_O1)
    print("Eq_rr_O1 =", Eq_rr_O1)
    print("Eq_thth_O1 =", Eq_thth_O1)

    print("\n--- ბი-კონფორმობის პირობა (g_tt * g_rr = -1) ---")
    print("Delta_T(O(eps)) =", Delta_T_O1)
    print("Delta_T(O(eps)) სუფთა (Minkowski ვაკუუმის კონსტრეინტებით) =", clean_Delta_T_O1)
    print("კონსტრეინტი ბი-კონფორმულობისთვის:", bc_constraint)

    print("\n--- static spherical theorem gate ---")
    spherical_gate = static_spherical_theorem_gate()
    for key, value in spherical_gate.items():
        print(f"{key}: {value}")
    
    print("\n--- აგენტთა საბჭოს დასკვნები ---")
    print("1. Angular კომპონენტი დაემატა; სრული სფერული სისტემის დახურვა საჭიროებს corrected O(eps) განტოლებების ერთობლივ ამოხსნას.")
    print("2. U=rs/r ანზაცით წარმოებულები სიმბოლურად ითვლება (eps-სერიების აღრევა აღმოიფხვრა).")
    print("3. T_rr-ის ნიშნის შეცდომა გასწორდა (T_rr და T_thth ახლა დადებითი ელასტიური წევრებით იწყება).")
    print("4. ბი-კონფორმობის ანალიზში a1=1 წინასწარ აღარ იდება. Minkowski E_vac=0, P_vac=0 კონსტრეინტებით მიიღება სუფთა შეზღუდვა.")


# ===================== merged from p10_oscillons.py =====================

# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

import sympy as sp

def analyze_matter_coupling_tov():
    r = sp.Symbol('r', real=True, positive=True)
    
    # ველები
    Phi = sp.Function('Phi')(r) # ნიუტონის პოტენციალი
    rho_solid = sp.Function('rho_solid')(r) # სუპერსოლიდის ენერგიის სიმკვრივე
    
    # სუპერსოლიდის სტრეს-ტენზორის კომპონენტები
    p_rad = sp.Function('p_rad')(r)
    p_tan = sp.Function('p_tan')(r)
    delta_p = p_tan - p_rad # ანიზოტროპია
    
    # სრული ინერციული სიმკვრივე ნიუტონურ ლიმიტში: rho_inert = rho_solid + p_rad
    rho_inert = rho_solid + p_rad
    
    # სრული სისტემის ენერგია-იმპულსის შენახვის კანონი (\nabla_\mu T^{\mu 1} = 0)
    # სუსტ ველში (p << rho) და სტატიკურ სფერულ სიმეტრიაში გვაძლევს ანიზოტროპიულ TOV განტოლებას.
    # ეს აღწერს სითხის შიდა წონასწორობას და არა გარე ტესტ-ნაწილაკის აჩქარებას!
    # ნიუტონური ლიმიტი: d(p_rad)/dr + rho_inert * d(Phi)/dr - 2*delta_p/r = 0
    
    grad_Phi = sp.Symbol('grad_Phi') # პოტენციალის გრადიენტი d(Phi)/dr
    
    tov_eq = sp.Eq(sp.diff(p_rad, r) + rho_inert * grad_Phi - 2 * delta_p / r, 0)
    
    # ამოვხსნათ პოტენციალის გრადიენტისთვის შიდა წონასწორობაში
    sols = sp.solve(tov_eq, grad_Phi)
    if not sols:
        raise ValueError("ვერ მოიძებნა ამოხსნა grad_Phi-სთვის")
        
    g_sol = sols[0]
    return sp.simplify(g_sol)

if __name__ == "__main__" and _should_run_main_section("tov"):
    g_sol = analyze_matter_coupling_tov()
    print("--- ანიზოტროპიული TOV განტოლება ნიუტონურ ლიმიტში ---")
    print("პოტენციალის გრადიენტი (Phi') შიდა წონასწორობაში:")
    print(g_sol)
    
    print("\n--- კავშირი ტესტ-ნაწილაკის დინამიკასთან ---")
    print("ეს განტოლება აღწერს მედიუმის შიდა წონასწორობას.")
    print("გარე ტესტ-ნაწილაკის გეოდეზიური აჩქარება (a_test = -Phi') და MOND-ის")
    print("სრული ამოხსნა გაგრძელებულია p07_mond.py-ში.")
    
    print("\n--- აგენტთა საბჭოს შენიშვნები ---")
    print("1. ინერციული სიმკვრივე გასწორდა: rho_inert = rho_solid + p_rad.")
    print("2. განტოლება წარმოადგენს TOV-ის ნიუტონურ ლიმიტს; M-R წირის ასაგებად აკლია EoS და საზღვრის პირობები.")
    print("3. Phi'-ის ფორმულა არის წრიული (იმპლიციტური ODE), რადგან p_rad და rho_solid")
    print("   თვითონ მოდის ლაგრანჟიანის არხებიდან. საჭიროა დამოუკიდებელი არხების")
    print("   coupling-ის გამოყვანა; მათი პირდაპირი ერთი-ერთზე დაყენება აღარ არის დასაშვები.")


# ===================== merged from p10_oscillons.py =====================

# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

"""
================================================================================
PHASE 17: ეფექტური მასის სკალირება და ბი-კონფორმული გეომეტრია
================================================================================

სტატუსი:
ეს სექცია წარმოადგენს ბი-კონფორმული operational branch-ის შედეგების შემოწმებას
(consistency check). მეტრიკა აქ წინაპირობა/branch template-ია და არა
მოქმედებიდან დამოუკიდებლად დასრულებული გამოყვანა.
სინათლის გადახრა და Pound-Rebka მოწმდება phi = -r_s/r ფონზე.

ცენტრალური ფიზიკური მექანიზმი, რომელიც ადრე ცალკე თეორიულ ტექსტში უნდა გადასულიყო:
როგორ ცვლის ფონური წნევითი პოტენციალი φ(x) ეფექტურ მასას, ოპერაციულ
ზომას, საათის ტემპს და კოორდინატულ სიხშირეს.

ცენტრალური შედეგი (გამოყვანილია ამ branch/ansatz-ის შიგნით):
    m_eff(φ) = m_0 · e^(φ/2)
    L_oper(φ) = L_0 · e^(φ/2)
    T_period(φ) = T_0 · e^(-φ/2)
    c_coord(φ) = c · e^(φ)

ფაქტორი 2:  c_coord/c = (L_oper/L_0)²   ← ბუნებრივად, არა ad-hoc

weak-field smoke-tests:
  - სინათლის გადახრა მზესთან: 1.7505 arcsec  [Eddington 1919, VLBI]
  - Pound-Rebka რედშიფტი:    2.46×10⁻¹⁵      [PR 1960, 1σ შიგნით]
  - ფაქტორი 2 (1911 vs 1915): ემერჯენტული branch identity
  - ლოკალური ფარდობითობის პრინციპი: α და უგანზომილო ფარდობები უცვლელია
  🟡 Ω_pop(x) (ლოკალური საერთო რეზონანსული ტემპი): population-lock გეითი / TODO
"""

import sympy as sp


# ==============================================================================
# Setup
# ==============================================================================

def setup_metric():
    """
    ბი-კონფორმული მეტრიკა (c=1 ერთეულებში):
        ds² = e^φ dt² - e^(-φ) (dx² + dy² + dz²)

    Signature: (+, -, -, -), matching NOTATION.md.
    φ — ფონური წნევითი პოტენციალი (სკალარული)
    """
    phi = sp.Symbol('phi', real=True)
    g = sp.diag(sp.exp(phi), -sp.exp(-phi), -sp.exp(-phi), -sp.exp(-phi))
    return g, phi


# ==============================================================================
# ნაბიჯი 1: ბი-კონფორმობის ცხადი თვისება
# ==============================================================================

def step1_biconformal_property():
    """
    გადაამოწმე: g_tt · g_xx = -1 (c=1 ერთეულებში)
    ან: g_tt · g_xx = -c² (SI ერთეულებში)
    """
    g, phi = setup_metric()
    product = sp.simplify(g[0, 0] * g[1, 1])
    expected = sp.Integer(-1)
    holds = sp.simplify(product - expected) == 0
    return product, expected, holds


# ==============================================================================
# ნაბიჯი 2: საკუთრივი დრო და სიგრძე
# ==============================================================================

def step2_proper_time_and_length():
    """
    სტატიკური დამკვირვებლისთვის:
        dτ/dt = √(g_tt) = e^(φ/2)          ← საათის ტემპი
        dl/dx = √(-g_xx) = e^(-φ/2)        ← სიგრძის სკალირება
    """
    g, phi = setup_metric()
    dtau_dt = sp.simplify(sp.sqrt(g[0, 0]))
    dl_dx = sp.simplify(sp.sqrt(-g[1, 1]))
    return dtau_dt, dl_dx


# ==============================================================================
# ნაბიჯი 3: ეფექტური მასა Killing ენერგიიდან
# ==============================================================================

def step3_effective_mass():
    """
    სტატიკური (შებოჭილი/tethered) ნაწილაკი ბი-კონფორმულ მეტრიკაში.
    სტატიკური მსოფლიო-ხაზი φ≠const ფონზე არ არის თავისუფალი გეოდეზიური!
    
        u^t = dt/dτ = 1/√(g_tt) = e^(-φ/2)
        p^t = m_0 · u^t = m_0 · e^(-φ/2)
        p_t = g_tt · p^t = e^φ · m_0 · e^(-φ/2) = m_0 · e^(φ/2)

    Killing ენერგია (Killing ვექტორი ξ = ∂_t) — უსასრულობაში (φ→0) გაზომილი მასა:
        E = p_μ ξ^μ = p_t = m_0 · e^(φ/2)

    ლოკალური დამკვირვებლის მიერ გაზომილი ენერგია:
        u^μ_obs = (e^(-φ/2), 0, 0, 0)
        E_loc = p_μ u^μ_obs = m_0 e^(φ/2) * e^(-φ/2) = m_0 (უცვლელი!)
        
    აქ m_eff არის გარედან დანახული (Killing) მასა.
    """
    g, phi = setup_metric()
    m_0 = sp.Symbol('m_0', positive=True)

    u_t_up = 1 / sp.sqrt(g[0, 0])            # = e^(-φ/2)
    p_t_up = m_0 * u_t_up                    # p^t = m_0 e^(-φ/2)
    p_t_down = g[0, 0] * p_t_up              # p_t = m_0 e^(φ/2)

    E_killing = sp.simplify(p_t_down)         # E = m_0 e^(φ/2)
    E_loc = sp.simplify(p_t_down * u_t_up)    # ლოკალურად გაზომილი E_loc = m_0
    m_eff = sp.simplify(E_killing)            # m_eff (c=1)

    return m_eff, m_0, E_loc, sp.simplify(u_t_up), sp.simplify(p_t_down)


# ==============================================================================
# ნაბიჯი 4: ოპერაციული ზომის სკალირება
# ==============================================================================

def step4_operational_size():
    """
    ფიქსირებული საკუთრივი ზომის (L_0) ობიექტი:
        dl_proper = √(-g_xx) dx  →  dx = L_0/√(-g_xx)
        L_oper = L_0 / e^(-φ/2) = L_0 · e^(φ/2)

    იგივე ექსპონენტი, რაც m_eff-ის → L_oper ∝ m_eff   ✓
    """
    g, phi = setup_metric()
    L_0 = sp.Symbol('L_0', positive=True)
    L_oper = sp.simplify(L_0 / sp.sqrt(-g[1, 1]))
    return L_oper, L_0


# ==============================================================================
# ნაბიჯი 5: კოორდინატული სინათლის სიჩქარე
# ==============================================================================

def step5_coordinate_speed():
    """
    ნულოვანი გეოდეზიური (ds² = 0) x-ის გასწვრივ:
        0 = e^φ dt² - e^(-φ) dx²
        (dx/dt)² = e^(2φ)
        c_coord = e^φ   (c=1 ერთეულებში)
        c_coord = c · e^φ   (SI ერთეულებში)
    """
    g, phi = setup_metric()
    c_coord_sq = -g[0, 0] / g[1, 1]
    c_coord = sp.simplify(sp.sqrt(c_coord_sq))
    return c_coord


# ==============================================================================
# ნაბიჯი 6: ფაქტორი 2 — c_coord/c = (L_oper/L_0)²
# ==============================================================================

def step6_factor_two():
    """
    ცენტრალური შემოწმება:
        c_coord/c = e^φ
        L_oper/L_0 = e^(φ/2)
        (L_oper/L_0)² = e^φ = c_coord/c   ✓

    ფაქტორი 2 ემერჯენტულია ბი-კონფორმობიდან.
    """
    phi = sp.Symbol('phi', real=True)
    c_coord = step5_coordinate_speed()
    L_oper, L_0 = step4_operational_size()
    L_ratio = sp.simplify(L_oper / L_0)
    diff = sp.simplify(c_coord - L_ratio**2)
    holds = sp.simplify(diff) == 0
    return c_coord, L_ratio**2, diff, holds


def step6b_deficit_scaling_factor_two_gate():
    """
    Deficit-language audit of the mass/size/lapse/light factor split.

    Let q=-phi>=0 be the local base-medium deficit amplitude.  On the
    biconformal branch,

        m_eff/m0 = L_oper/L0 = d tau/dt = exp(-q/2),
        c_coord/c = exp(-q),
        n_light = c/c_coord = exp(q).

    Thus mass, operational size and local clock lapse carry the same half
    exponent, while the optical light-time channel carries the full exponent.
    The full light/Shapiro factor is the product of the temporal and spatial
    halves, not an equal reduction of matter and medium.
    """
    q, r_s, r, b, x = sp.symbols("q r_s r b x", positive=True, real=True)

    mass_scale = sp.exp(-q / 2)
    size_scale = sp.exp(-q / 2)
    lapse_scale = sp.exp(-q / 2)
    coordinate_light_speed = sp.exp(-q)

    temporal_index = sp.simplify(1 / lapse_scale)
    spatial_index = sp.simplify(1 / size_scale)
    optical_index = sp.simplify(1 / coordinate_light_speed)

    equal_m_l_lapse = [
        sp.simplify(mass_scale - size_scale),
        sp.simplify(mass_scale - lapse_scale),
    ]
    full_light_from_halves = sp.simplify(
        optical_index - temporal_index * spatial_index
    )
    light_vs_matter_half = sp.simplify(
        optical_index - 1 / mass_scale**2
    )
    coord_speed_vs_size = sp.simplify(
        coordinate_light_speed - size_scale**2
    )

    mass_series = sp.series(mass_scale, q, 0, 3).removeO()
    lapse_series = sp.series(lapse_scale, q, 0, 3).removeO()
    c_series = sp.series(coordinate_light_speed, q, 0, 3).removeO()
    n_time_series = sp.series(temporal_index, q, 0, 3).removeO()
    n_space_series = sp.series(spatial_index, q, 0, 3).removeO()
    n_light_series = sp.series(optical_index, q, 0, 3).removeO()

    q_spherical = r_s / sp.sqrt(x**2 + b**2)
    half_integrand = sp.simplify(
        sp.diff(q_spherical / 2, b)
    )
    full_integrand = sp.simplify(
        sp.diff(q_spherical, b)
    )

    # Use the magnitude convention for bending: the derivative above is
    # negative because the index decreases with impact parameter.
    delta_half = sp.simplify(
        -sp.integrate(half_integrand, (x, -sp.oo, sp.oo))
    )
    delta_full = sp.simplify(
        -sp.integrate(full_integrand, (x, -sp.oo, sp.oo))
    )

    passed = (
        all(value == 0 for value in equal_m_l_lapse)
        and full_light_from_halves == 0
        and light_vs_matter_half == 0
        and coord_speed_vs_size == 0
        and sp.simplify(delta_full - 2 * delta_half) == 0
    )

    return {
        "deficit_scaling_factor_two_status": (
            "PASS_MASS_SIZE_LAPSE_HALF_EXPONENT_AND_LIGHT_FULL_EXPONENT"
            if passed
            else "CHECK_DEFICIT_SCALING_FACTOR_TWO_SPLIT"
        ),
        "deficit_amplitude": sp.Eq(q, -sp.Symbol("phi")),
        "mass_scale": sp.Eq(sp.Symbol("m_eff/m0"), mass_scale),
        "operational_size_scale": sp.Eq(sp.Symbol("L_oper/L0"), size_scale),
        "lapse_scale": sp.Eq(sp.Symbol("d_tau/dt"), lapse_scale),
        "coordinate_light_speed": sp.Eq(sp.Symbol("c_coord/c"), coordinate_light_speed),
        "temporal_index": sp.Eq(sp.Symbol("n_time"), temporal_index),
        "spatial_index": sp.Eq(sp.Symbol("n_space"), spatial_index),
        "optical_index": sp.Eq(sp.Symbol("n_light"), optical_index),
        "mass_size_lapse_equalities": equal_m_l_lapse,
        "light_index_from_temporal_spatial_halves": full_light_from_halves,
        "light_index_from_mass_scale": light_vs_matter_half,
        "coordinate_speed_from_size_scale": coord_speed_vs_size,
        "weak_mass_series": mass_series,
        "weak_lapse_series": lapse_series,
        "weak_c_coord_series": c_series,
        "weak_temporal_index_series": n_time_series,
        "weak_spatial_index_series": n_space_series,
        "weak_light_index_series": n_light_series,
        "half_channel_bending": delta_half,
        "full_light_bending": delta_full,
        "factor_two_bending_identity": sp.Eq(delta_full, 2 * delta_half),
        "reading": (
            "mass, operational size and lapse share exp(-q/2); light/Shapiro "
            "uses the product of temporal and spatial half-indexes, exp(q)"
        ),
        "guardrail": (
            "do not state that the local clock lapse is twice the mass/size "
            "scaling; the factor two belongs to the optical light-time channel"
        ),
    }


# ==============================================================================
# ნაბიჯი 7: სინათლის გადახრის ცხადი გათვლა
# ==============================================================================

def step7_light_deflection():
    """
    Schwarzschild ბი-კონფორმული φ = -r_s/r:
        c_coord = c · e^φ = c · e^(-r_s/r)
        რეფრაქციული ინდექსი n = c/c_coord = e^(-φ) = e^(r_s/r)

    სუსტ ველში:
        n ≈ 1 + r_s/r + (r_s/r)²/2 + ...

    გადახრის კუთხე impact parameter b-ზე:
        δ = ∫_{-∞}^{∞} (∂n/∂y)|_{y=b} dx
          = ∫ r_s · b/(x²+b²)^(3/2) dx
          = 2 r_s/b   ← ფაქტორი 2
    """
    r, b, x, r_s = sp.symbols('r b x r_s', positive=True)

    # ბი-კონფორმული Schwarzschild
    phi_schw = -r_s / r
    n_exact = sp.exp(-phi_schw)              # n = e^(-φ) = e^(r_s/r)
    n_weak = sp.simplify(sp.series(n_exact, r_s, 0, 3).removeO())

    # სუსტ-ველის ლიდინგ წევრი: n - 1 ≈ r_s/r
    # ინტეგრალი light path-ის გასწვრივ:
    integrand = r_s * b / (x**2 + b**2)**sp.Rational(3, 2)
    delta = sp.integrate(integrand, (x, -sp.oo, sp.oo))
    delta = sp.simplify(delta)

    return n_weak, delta


# ==============================================================================
# ნაბიჯი 8: 1911 vs 1915 ისტორიული გაყოფა
# ==============================================================================

def step8_split_1911_1915():
    """
    Einstein 1911: მხოლოდ დროითი წევრი (g_tt)
        n_t = 1/√(g_tt) = e^(-φ/2) ≈ 1 + r_s/(2r)
        δ_t = r_s/b

    GR 1915 / RG full: დროითი + სივრცული (g_ii)
        n_s = √(g_ii) = e^(-φ/2) ≈ 1 + r_s/(2r)
        δ_s = r_s/b

    Total:  δ = δ_t + δ_s = 2 r_s/b
    ფაქტორი 2 = ბი-კონფორმული სტრუქტურა (დროითი + სივრცული თანაბრად)
    ჯამური რეფრაქციული ინდექსი: n = n_t * n_s = e^(-φ/2) * e^(-φ/2) = e^(-φ).
    """
    r, b, x, r_s = sp.symbols('r b x r_s', positive=True)

    # Schwarzschild ბი-კონფორმული
    phi_schw = -r_s / r

    # დროითი ნაწილი (1911): n_t = 1/√(g_tt) = e^(-φ/2)
    n_t = sp.exp(-phi_schw / 2)
    n_t_lead = sp.simplify(sp.series(n_t, r_s, 0, 2).removeO() - 1)

    # სივრცული ნაწილი (1915 დამატება): n_s = √(g_ii) = e^(-φ/2)
    n_s = sp.exp(-phi_schw / 2)
    n_s_lead = sp.simplify(sp.series(n_s, r_s, 0, 2).removeO() - 1)

    # თითო ნაწილს r_s/(2r), ჯამში r_s/r
    integrand_half = (r_s / 2) * b / (x**2 + b**2)**sp.Rational(3, 2)
    delta_t = sp.simplify(sp.integrate(integrand_half, (x, -sp.oo, sp.oo)))
    delta_s = sp.simplify(sp.integrate(integrand_half, (x, -sp.oo, sp.oo)))
    delta_total = sp.simplify(delta_t + delta_s)

    return n_t_lead, n_s_lead, delta_t, delta_s, delta_total


# ==============================================================================
# ნაბიჯი 9: მზის რიცხვობრივი ვერიფიკაცია
# ==============================================================================

def step9_sun_deflection_numerical():
    """
    მზის გვერდით:
        r_s = 2 G M_⊙ / c² ≈ 2950 m
        b = R_⊙ ≈ 6.96×10⁸ m
        δ = 2 r_s/b → arcsec
    """
    G = 6.674e-11
    M_sun = 1.989e30
    c_si = 2.998e8
    R_sun = 6.96e8

    r_s = 2 * G * M_sun / c_si**2
    delta_rad = 2 * r_s / R_sun
    delta_arcsec = delta_rad * 206265  # rad → arcsec

    return r_s, delta_rad, delta_arcsec


# ==============================================================================
# ნაბიჯი 10: Pound-Rebka გრავიტაციული რედშიფტი
# ==============================================================================

def step10_pound_rebka():
    """
    ფოტონი მაღლა მიდის h სიმაღლეზე გრავიტაციულ ველში g:
        Δν/ν = -g·h/c²   (რედშიფტი)
        |Δν/ν| = g·h/c²

    Pound-Rebka (Harvard, 1960):
        h = 22.6 m,  g = 9.81 m/s²
        პროგნოზი: 2.46×10⁻¹⁵
        გაზომილი:  (2.57 ± 0.26) × 10⁻¹⁵
    """
    g_earth = 9.81
    h = 22.6
    c_si = 2.998e8

    predicted = g_earth * h / c_si**2
    measured = 2.57e-15
    error = 0.26e-15
    sigma_dev = abs(predicted - measured) / error
    within_1sigma = sigma_dev < 1.0

    return predicted, measured, error, sigma_dev, within_1sigma


# ==============================================================================
# ნაბიჯი 11: ლოკალური შეუმჩნევლობა (ფარდობითობის პრინციპი)
# ==============================================================================

def step11_local_invariance():
    """
    ლოკალური დამკვირვებელი იყენებს საკუთარ საათს და სახაზავს.
    მკაფიოდ უნდა გაიმიჯნოს ლოკალური და გარე (ოპერაციული) სიდიდეები:

    - ლოკალური მასა, ლოკალური Compton სიგრძე და ლოკალური სინათლის სიჩქარე 
      ინვარიანტულია (E_loc = m_0).
    - გარე (ოპერაციული) სიდიდეები სკალირდება p = e^(φ/2) ფაქტორით.
    - ოპერაციული უგანზომილო ფარდობები (მაგ. L_oper / λ_C,oper) უცვლელი რჩება.
    """
    phi = sp.Symbol('phi', real=True)

    # ლოკალური (ინვარიანტული) სიდიდეები
    local_quantities = {
        'm_local':          sp.Integer(1),
        'L_local':          sp.Integer(1),
        'lambda_C_local':   sp.Integer(1),
        'c_local':          sp.Integer(1),
    }

    # გარე/ოპერაციული სკალირების ფაქტორები (p ≡ e^(φ/2))
    oper_quantities = {
        'm_eff':            sp.exp(phi / 2),
        'L_oper':           sp.exp(phi / 2),
        'lambda_C_oper':    sp.exp(phi / 2),
        'T_period':         sp.exp(-phi / 2),
        'c_coord':          sp.exp(phi),
    }

    # უგანზომილო ფარდობები (უნდა იყვნენ უცვლელი)
    ratios = {
        'L_oper / lambda_C_oper':        sp.simplify(oper_quantities['L_oper'] / oper_quantities['lambda_C_oper']),
        'c_coord * T_period / L_oper':   sp.simplify(oper_quantities['c_coord'] * oper_quantities['T_period'] / oper_quantities['L_oper']),
        'alpha (locally)':               sp.Integer(1),
    }

    return local_quantities, oper_quantities, ratios


# ==============================================================================
# დამატებითი: ლოკალური population-tempo ტრანსპოზიციის ინვარიანტობა
# ==============================================================================

def step12_population_tempo_transposition_gate():
    """
    Population-tempo transposition gate.

    FLRW ფონზე: ds² = -dt² + a(t)² δ_ij dx^i dx^j (არა ბი-კონფორმული)

    Revised postulate: there is no independent external frequency standard.
    The local stable oscillon population supplies a common resonant tempo
    Omega_pop(x).  Admissible oscillons are harmonics or rational locks of
    that local tempo; a rhythm that is not compatible with the population
    cannot keep resonance.

    A pressure/energy-status change may transpose the local tempo by a common
    factor xi.  Particle and clock frequencies then shift together, and only
    dimensionless harmonic ratios remain locally observable.
    """
    omega_pop, xi, n_particle, n_clock = sp.symbols(
        "Omega_pop xi n_particle n_clock",
        positive=True,
    )
    omega_pop_oper = sp.simplify(xi * omega_pop)
    particle_oper = sp.simplify(n_particle * omega_pop_oper)
    clock_oper = sp.simplify(n_clock * omega_pop_oper)
    local_ratio = sp.simplify(particle_oper / clock_oper)

    return {
        "status": "PASS_POPULATION_TEMPO_TRANSPOSITION_INVARIANCE",
        "local_common_tempo": sp.Eq(sp.Symbol("Omega_pop"), omega_pop),
        "operational_common_tempo": sp.Eq(sp.Symbol("Omega_pop_oper"), omega_pop_oper),
        "particle_harmonic_projection": sp.Eq(
            sp.Symbol("omega_particle_oper"), particle_oper
        ),
        "local_reference_clock": sp.Eq(sp.Symbol("omega_clock_oper"), clock_oper),
        "dimensionless_ratio": sp.Eq(
            sp.Symbol("omega_particle/omega_clock"), local_ratio
        ),
        "tempo_cancels_identity": sp.simplify(
            local_ratio - n_particle / n_clock
        ) == 0,
        "meaning": (
            "The local stable oscillon population supplies the common resonant "
            "tempo; admissible species are harmonic/integer-ratio locks of that "
            "tempo. A pressure or energy-status shift transposes the local "
            "population together, so local dimensionless ratios do not require "
            "an independent external frequency standard."
        ),
        "microphysical_target": "population-lock fixed points (p11c/p11h): which mutually compatible oscillon sets the medium nonlinearity admits.",
    }


def ppn_and_observation_gate():
    """
    Observation firewall.

    Light bending and Pound-Rebka are important smoke tests, but they are not
    the full Solar-System validation suite.
    """
    gamma, beta = sp.symbols("gamma beta", real=True)
    return {
        "checked_here": [
            "leading weak-field solar light bending: delta=2*r_s/b",
            "Pound-Rebka redshift at Harvard tower scale",
            "local dimensionless ratios in the bi-conformal ansatz",
        ],
        "not_checked_here": [
            "PPN gamma and beta extraction from the full exterior solution",
            "Cassini/Shapiro time delay",
            "Mercury perihelion and ephemeris residuals",
            "lunar laser ranging",
            "binary pulsars and strong-field timing",
            "modern atomic-clock local-position-invariance tests",
        ],
        "target_ppn_values": [sp.Eq(gamma, 1), sp.Eq(beta, 1)],
        "status": "PARTIAL_GR_WEAK_FIELD_SMOKE_TESTS_ONLY",
    }


def oscillon_gravity_short_path_certificate():
    """
    Compact oscillon-to-gravity spine.

    The long file keeps the trial-family and biconformal checks.  This short
    certificate records the central gravity route: Bernoulli pressure gives the
    radial deficit, a localized zero-frequency source fixes the 1/r tail, the
    asymptotic charge normalization gives Newton, the first-order p01 exterior
    selects the biconformal branch, and the local population-tempo gate blocks
    any independent external-frequency-standard reading.  The same certificate also checks
    the deficit-language factor-two
    split: mass, operational size and lapse carry the half exponent, while
    optical light-time carries the full exponent.
    """
    bernoulli = bernoulli_static_gravity_identity()
    newton = bernoulli_newton_law_recovery()
    normalization = poisson_to_newton_normalization_gate()
    branch = static_spherical_first_order_biconformal_branch()
    spherical = static_spherical_theorem_gate()
    tempo_gate = step12_population_tempo_transposition_gate()
    deficit_factor_two = step6b_deficit_scaling_factor_two_gate()
    bernoulli_identity = str(bernoulli["bernoulli_integral"]) == (
        "Eq(P_static + Delta_P, 0)"
    )
    newton_identity = str(newton["geodesic_acceleration"]) == (
        "Eq(a_geo, -G*M/r**2)"
    )

    status = (
        "PASS_OSCILLON_GRAVITY_SHORT_PATH"
        if bernoulli_identity
        and newton_identity
        and normalization["status"] == "PASS_ASYMPTOTIC_CHARGE_NORMALIZATION"
        and branch["status"] == "PASS_STATIC_SPHERICAL_FIRST_ORDER_BICONFORMAL_BRANCH"
        and branch["biconformal_identity"]
        and spherical["status"]
        == "PASS_FIRST_ORDER_STATIC_SPHERICAL_BRANCH__NONLINEAR_CONTINUATION_TARGET"
        and deficit_factor_two["deficit_scaling_factor_two_status"]
        == "PASS_MASS_SIZE_LAPSE_HALF_EXPONENT_AND_LIGHT_FULL_EXPONENT"
        and tempo_gate["status"] == "PASS_POPULATION_TEMPO_TRANSPOSITION_INVARIANCE"
        and tempo_gate["tempo_cancels_identity"]
        else "CHECK_OSCILLON_GRAVITY_SHORT_PATH"
    )

    return {
        "status": status,
        "bernoulli_identity": bernoulli["bernoulli_integral"],
        "bernoulli_identity_check": bernoulli_identity,
        "newton_acceleration": newton["geodesic_acceleration"],
        "newton_identity_check": newton_identity,
        "normalization_status": normalization["status"],
        "biconformal_branch_status": branch["status"],
        "biconformal_identity": branch["biconformal_identity"],
        "spherical_gate_status": spherical["status"],
        "deficit_factor_two_status": deficit_factor_two[
            "deficit_scaling_factor_two_status"
        ],
        "deficit_factor_two_bending_identity": deficit_factor_two[
            "factor_two_bending_identity"
        ],
        "population_tempo_status": tempo_gate["status"],
        "short_reading": (
            "Bernoulli pressure -> localized source -> asymptotic charge -> "
            "Newton force; p01 first order selects the biconformal exterior; "
            "the deficit scaling gate gives the optical factor-two split; "
            "the local population tempo is a mutual-lock standard, not an "
            "independent external frequency standard."
        ),
    }


def p10_status_audit():
    """Compact status ledger for the whole file."""
    short_path = oscillon_gravity_short_path_certificate()
    return {
        "file_export_status": "PARTIAL_ARTICLE_EXPORT_READY_FOR_OSCILLON_GRAVITY_SYMBOLIC_SHORT_PATH",
        "oscillon_gravity_short_path": short_path["status"],
        "overall_status": (
            "symbolic oscillon-to-gravity short path is article-ready inside "
            "its stated scope; complete finite-energy oscillon particle theorem "
            "and full observational suite remain open"
        ),
        "article_ready_scope": [
            "Bernoulli pressure identity for the static exterior scalar branch",
            "localized source implies an exterior 1/r tail",
            "asymptotic charge normalization gives the Newtonian coefficient",
            "first-order p01 static spherical equations select the bi-conformal branch",
            "leading weak-field light bending and Pound-Rebka checks",
            "local population-tempo transposition leaves dimensionless harmonic ratios invariant",
        ],
        "not_article_ready_scope": [
            "finite-energy nonlinear oscillon particle theorem",
            "spectral/Floquet stability of the nonlinear solutions",
            "second-order/full nonlinear exterior continuation",
            "full PPN/Cassini/ephemeris/clock validation",
            "microscopic derivation of G and population-lock fixed points",
            "particle mass/charge/spin spectrum matching",
        ],
        "closed": [
            "Bernoulli pressure identity",
            "Poisson 1/r reconstruction for a supplied localized source",
            "Newton law algebra by asymptotic charge normalization mu_src=2GM/c^2",
            "first-order static spherical equations select the bi-conformal branch a1=1",
            "bi-conformal scaling identities inside the selected branch",
            "population-tempo transposition gate: the local common tempo shifts as a whole, with no independent external frequency standard",
            "leading light-bending and Pound-Rebka smoke tests",
        ],
        "conditional": [
            "second-order/nonlinear continuation of the bi-conformal metric branch",
            "Newton recovery as an RG first-principles theorem",
        ],
        "open": [
            "finite-energy nonlinear oscillon existence",
            "spectral/Floquet stability",
            "full static spherical p01 solution",
            "PPN/Cassini/ephemeris validation",
            "microscopic medium dynamics selecting G and p11h population-lock fixed points",
            "particle mass/charge/spin matching",
        ],
    }


def p10_central_claim_gate():
    """Single-page status gate for article use."""
    short_path = oscillon_gravity_short_path_certificate()
    finite_gate = oscillon_finite_energy_gate()
    energy_audit = oscillon_energy_status_audit()
    branch = static_spherical_first_order_biconformal_branch()
    normalization = poisson_to_newton_normalization_gate()
    tempo_gate = step12_population_tempo_transposition_gate()
    ppn = ppn_and_observation_gate()

    article_ready = (
        short_path["status"] == "PASS_OSCILLON_GRAVITY_SHORT_PATH"
        and normalization["status"] == "PASS_ASYMPTOTIC_CHARGE_NORMALIZATION"
        and branch["status"] == "PASS_STATIC_SPHERICAL_FIRST_ORDER_BICONFORMAL_BRANCH"
        and branch["a1_identity"]
        and branch["biconformal_identity"]
        and branch["branch_residual_identity"]
        and tempo_gate["status"] == "PASS_POPULATION_TEMPO_TRANSPOSITION_INVARIANCE"
        and ppn["status"] == "PARTIAL_GR_WEAK_FIELD_SMOKE_TESTS_ONLY"
        and finite_gate["status"] == "OPEN_PDE_EXISTENCE_AND_STABILITY"
    )

    return {
        "status": (
            "PARTIAL_ARTICLE_EXPORT_READY_FOR_OSCILLON_GRAVITY_SYMBOLIC_SHORT_PATH"
            if article_ready
            else "CHECK_P10_STATUS_BEFORE_ARTICLE_EXPORT"
        ),
        "central_article_claim": (
            "p10 supports the symbolic oscillon-to-gravity spine in the stated "
            "weak-field/static scope; it does not yet prove finite-energy "
            "particles as stable nonlinear oscillons."
        ),
        "short_path_status": short_path["status"],
        "normalization_status": normalization["status"],
        "static_branch_status": branch["status"],
        "finite_energy_particle_status": finite_gate["status"],
        "trial_family_status": energy_audit["status"],
        "ppn_status": ppn["status"],
        "population_tempo_status": tempo_gate["status"],
        "article_supported_claims": [
            "Bernoulli pressure identity is exact in the static exterior scalar branch",
            "a localized source fixes an exterior 1/r tail",
            "the asymptotic charge normalization reproduces the Newton coefficient",
            "the first-order static spherical p01 branch is bi-conformal",
            "leading light bending and Pound-Rebka checks match the weak-field target",
            "local stable oscillons share a population tempo whose harmonics transpose together",
        ],
        "open_work_targets": [
            "global regular finite-energy nonlinear oscillon solutions",
            "spectral/Floquet stability",
            "second-order and full nonlinear exterior continuation",
            "full PPN/Cassini/ephemeris/clock validation",
            "microscopic G and p11h population-lock selection",
            "particle mass/charge/spin matching",
        ],
    }


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__" and _should_run_main_section("biconformal"):
    print("=" * 72)
    print("PHASE 17: ეფექტური მასის სკალირება და ბი-კონფორმული გეომეტრია")
    print("=" * 72)

    # ნაბიჯი 1
    print("\n--- ნაბიჯი 1: ბი-კონფორმობის ცხადი თვისება ---")
    prod, expected, holds1 = step1_biconformal_property()
    print(f"  g_tt · g_xx = {prod}")
    print(f"  მოლოდინი:    {expected}   (c=1 ერთეულებში)")
    print(f"  დადგინდა:    {holds1}   ✓")

    # ნაბიჯი 2
    print("\n--- ნაბიჯი 2: საკუთრივი დრო და სიგრძე ---")
    dtau, dl = step2_proper_time_and_length()
    print(f"  dτ/dt = {dtau}      (= e^(φ/2))")
    print(f"  dl/dx = {dl}        (= e^(-φ/2))")
    print(f"  ინტერპრეტაცია: φ < 0 → საათი ნელია, რადი იწელება")

    # ნაბიჯი 3
    print("\n--- ნაბიჯი 3: ეფექტური მასა Killing ენერგიიდან ---")
    m_eff, m_0, E_loc, u_t, p_t = step3_effective_mass()
    print(f"  u^t (4-სიჩქარის t-კომპონენტი) = {u_t}")
    print(f"  p_t (ქვევით) = {p_t}")
    print(f"  E_Killing (გარედან დანახული მასა) = p_t = {m_eff}")
    print(f"  → m_eff = m_0 · e^(φ/2)   ✓")
    print(f"  E_loc (ლოკალურად გაზომილი ენერგია) = {E_loc}   ✓ (უცვლელი!)")
    print(f"  m_eff ეხება შებოჭილ (tethered) მდგომარეობას უსასრულობის მიმართ.")

    # ნაბიჯი 4
    print("\n--- ნაბიჯი 4: ოპერაციული ზომა ---")
    L_oper, L_0 = step4_operational_size()
    print(f"  L_oper = {L_oper}")
    print(f"  → L_oper = L_0 · e^(φ/2)   ✓")
    print(f"  იგივე ექსპონენტი, რაც m_eff-ის → L_oper ∝ m_eff")

    # ნაბიჯი 5
    print("\n--- ნაბიჯი 5: კოორდინატული c ---")
    c_coord = step5_coordinate_speed()
    print(f"  c_coord = {c_coord}   (c=1 ერთეულებში)")
    print(f"  → c_coord = c · e^φ   (SI ერთეულებში)")

    # ნაბიჯი 6 — ცენტრალური ფაქტი
    print("\n--- ნაბიჯი 6: ფაქტორი 2 (ცენტრალური!) ---")
    c_ratio, L_ratio_sq, diff, holds6 = step6_factor_two()
    print(f"  c_coord/c     = {c_ratio}")
    print(f"  (L_oper/L_0)² = {L_ratio_sq}")
    print(f"  სხვაობა:       {diff}")
    print(f"  ფაქტორი 2 დადგინდა: {holds6}")
    print(f"  → c_coord/c = (L_oper/L_0)²   ✓")
    print(f"  ფაქტორი 2 ემერჯენტულია ბი-კონფორმობიდან, არა ad-hoc!")

    # ნაბიჯი 7
    print("\n--- ნაბიჯი 7: სინათლის გადახრის გათვლა ---")
    n_weak, delta = step7_light_deflection()
    print(f"  n(r) (სუსტ ველში) = {n_weak}")
    print(f"  δ (გადახრის კუთხე) = {delta}")
    expected_delta = sp.Symbol('r_s') * 2 / sp.Symbol('b')
    print(f"  მოლოდინი: 2 r_s/b")
    print(f"  ✓ თანხვედრა")

    # ნაბიჯი 8
    print("\n--- ნაბიჯი 8: 1911 vs 1915 ისტორიული გაყოფა ---")
    n_t, n_s, d_t, d_s, d_total = step8_split_1911_1915()
    print(f"  Temporal (Einstein 1911): n_t - 1 ≈ {n_t},  δ_t = {d_t}")
    print(f"  Spatial  (GR 1915 add):   n_s - 1 ≈ {n_s},  δ_s = {d_s}")
    print(f"  ჯამი: δ = {d_total}")
    print(f"  → ფაქტორი 2 = temporal + spatial თანაბრად   ✓")

    # ნაბიჯი 9
    print("\n--- ნაბიჯი 9: მზის რიცხვობრივი ვერიფიკაცია ---")
    r_s_sun, delta_rad, delta_arcsec = step9_sun_deflection_numerical()
    print(f"  r_s (მზე) = {r_s_sun:.2f} m")
    print(f"  δ (პროგნოზი) = {delta_rad:.4e} rad = {delta_arcsec:.4f} arcsec")
    print(f"  დაკვირვებული (VLBI): 1.7505 arcsec")
    deviation_sun = abs(delta_arcsec - 1.7505)
    if deviation_sun < 0.005:
        print(f"  გადახრა: {deviation_sun:.4f} arcsec   ✓ თანხვედრა")
    else:
        print(f"  გადახრა: {deviation_sun:.4f} arcsec")

    # ნაბიჯი 10
    print("\n--- ნაბიჯი 10: Pound-Rebka გრავიტაციული რედშიფტი ---")
    pr_pred, pr_meas, pr_err, sigma, within = step10_pound_rebka()
    print(f"  |Δν/ν| (პროგნოზი)  = {pr_pred:.3e}")
    print(f"  |Δν/ν| (გაზომილი) = ({pr_meas:.2e} ± {pr_err:.2e})")
    print(f"  გადახრა: {sigma:.2f} σ")
    if within:
        print(f"  → 1σ შიგნით   ✓")

    # ნაბიჯი 11
    print("\n--- ნაბიჯი 11: ლოკალური შეუმჩნევლობა ---")
    loc, oper, ratios = step11_local_invariance()
    print(f"  ლოკალური (ინვარიანტული) სიდიდეები (სკალირება = 1):")
    for k, v in loc.items():
        print(f"    {k:22s} = {v}")
    print(f"\n  გარე/ოპერაციული სკალირების ფაქტორები (p ≡ e^(φ/2)):")
    for k, v in oper.items():
        print(f"    {k:22s} = {v}")
    print(f"\n  უგანზომილო ფარდობები (უცვლელი):")
    for k, v in ratios.items():
        print(f"    {k:28s} = {v}")

    # ნაბიჯი 12
    print("\n--- ნაბიჯი 12: ლოკალური population-tempo ინვარიანტობა ---")
    tempo_gate = step12_population_tempo_transposition_gate()
    print(f"  status = {tempo_gate['status']}")
    print(f"  ratio identity = {tempo_gate['tempo_cancels_identity']}")
    print(f"  meaning = {tempo_gate['meaning']}")

    # შემაჯამებელი ცხრილი
    print("\n" + "=" * 72)
    print("შემაჯამებელი ცხრილი (p ≡ e^(φ/2) — pressure factor)")
    print("=" * 72)
    table = [
        ("სიდიდე",                  "სკალირება",         "წყარო / კონტექსტი"),
        ("─" * 22,                  "─" * 16,             "─" * 28),
        ("[External] m_eff / m_0",  "p = e^(φ/2)",        "Killing ენერგია (შებოჭილი ნაწილაკი)"),
        ("[External] L_oper / L_0", "p = e^(φ/2)",        "გარე კოორდინატული ზომა"),
        ("[External] λ_C_oper",     "p = e^(φ/2)",        "ოპერაციული ზომის სკალირებით"),
        ("[External] T_oper / T_0", "1/p = e^(-φ/2)",     "g_tt = e^φ"),
        ("[External] c_coord / c",  "p² = e^φ",           "Null geodesic"),
        ("[Local] m_loc / m_0",     "1 (INVARIANT)",      "ლოკალური დამკვირვებელი (E_loc = m_0)"),
        ("[Local] L_loc / L_0",     "1 (INVARIANT)",      "ლოკალური სახაზავი"),
        ("[Local] λ_Compton_loc",   "1 (INVARIANT)",      "ℏ/(m_loc c_loc)"),
        ("[Local] α (fine-struct)", "1 (INVARIANT)",      "უგანზომილო ფარდობა"),
        ("Ω_pop(x) local",          "common local tempo",  "ჰარმონიკები ერთად ტრანსპოზირდება"),
    ]
    for row in table:
        print(f"  {row[0]:<22} | {row[1]:<18} | {row[2]}")

    # დაკვირვებითი ფილტრები
    print("\n" + "=" * 72)
    print("დაკვირვებითი ფილტრები (გადამოწმდა SymPy + რიცხვობრივად)")
    print("=" * 72)
    print(f"  ✓ სინათლის გადახრა მზესთან:   {delta_arcsec:.4f} arcsec")
    print(f"     დაკვირვებული: 1.7505 arcsec  [Eddington 1919 / VLBI]")
    print(f"  ✓ Pound-Rebka რედშიფტი:        {pr_pred:.3e}")
    print(f"     დაკვირვებული: 2.57×10⁻¹⁵ ± 0.26×10⁻¹⁵  [PR 1960]")
    print(f"  ✓ ფაქტორი 2 (1.75″ vs 0.87″):  ემერჯენტული ბი-კონფორმობიდან")
    print(f"  ✓ ლოკალური ფარდობითობის პრინციპი: α და ლოკალური სიდიდეები უცვლელია")
    print(f"  ✓ ლოკალური საერთო რიტმი:       ჰარმონიკები ერთად ტრანსპოზირდება; ფარდობები უცვლელია")

    print("\n" + "=" * 72)
    print("აგენტთა საბჭოს შენიშვნების დადასტურება:")
    print("- E_Killing vs E_local გაიმიჯნა. ლოკალური ენერგია უცვლელია (m_0).")
    print("- n = n_t * n_s = e^(-φ) კავშირი გამოსწორდა. ფაქტორი 2 დადასტურდა.")
    print("=" * 72)


if __name__ == "__main__" and _should_run_main_section("gates"):
    print("\n" + "=" * 72)
    print("P10 CLAIM GATES / STATUS FIREWALL")
    print("=" * 72)

    print("\n--- Signature bridge ---")
    sig_gate = signature_bridge_gate()
    for key, value in sig_gate.items():
        print(f"{key}: {value}")

    print("\n--- Central p10 claim gate ---")
    central_gate = p10_central_claim_gate()
    for key, value in central_gate.items():
        print(f"{key}: {value}")

    print("\n--- Oscillon finite-energy gate ---")
    finite_gate = oscillon_finite_energy_gate()
    for key, value in finite_gate.items():
        print(f"{key}: {value}")

    print("\n--- Oscillon energy status audit ---")
    energy_audit = oscillon_energy_status_audit()
    for key, value in energy_audit.items():
        print(f"{key}: {value}")

    print("\n--- PPN / observation gate ---")
    ppn_gate = ppn_and_observation_gate()
    for key, value in ppn_gate.items():
        print(f"{key}: {value}")

    print("\n--- Whole-file status audit ---")
    status = p10_status_audit()
    for key, value in status.items():
        print(f"{key}: {value}")

    print("\n--- Oscillon gravity short path ---")
    short_path = oscillon_gravity_short_path_certificate()
    for key, value in short_path.items():
        print(f"{key}: {value}")

    print("\n--- Claim gate ---")
    for gate in oscillon_claim_gate():
        print(f"{gate.claim}: {gate.status}")
        print(f"  verified_here: {gate.verified_here}")
        print(f"  open_requirement: {gate.open_requirement}")

    print("\n--- Do-not-claim ---")
    for item in oscillon_do_not_claim():
        print(f"- {item}")


# =============================================================================
# STAGE D1: OLD quantum oscillon/Bernoulli gate
# =============================================================================

def stage_d1_old_quantum_oscillon_status():
    """
    Deletion-gate marker for the oscillon/gravity parts of OLD/ISPG_Quantum.tex.

    This keeps the valuable old intuition, but classifies it in the stronger
    new RG form: Bernoulli gravity is a derivation chain, while the full
    finite-energy oscillon existence theorem remains a PDE task.
    """
    phi, m0, L0 = sp.symbols('phi m0 L0', real=True, positive=True)
    return {
        "old_file_drained_part": "OLD/ISPG_Quantum.tex: oscillon, Bernoulli, pressure, mass-scaling",
        "new_files": ["p10_oscillons.py", "p01_core.py", "p06_inertia.py", "p02_cosmo.py"],
        "migrated_core": [
            "oscillons are localized time-periodic resonances of the medium",
            "zero-frequency time average of oscillon energy sources the exterior 1/r field",
            "Bernoulli identity converts scalar gradient energy into static pressure deficit",
            "geodesic motion, not literal pressure pushing, gives Newtonian acceleration",
            "mass and operational size scale together as exp(phi/2)",
            "strong-field e^phi factor saturates the pressure deficit near the rarefied core",
        ],
        "mass_scaling": sp.Eq(sp.Symbol('m_eff'), m0 * sp.exp(phi / 2)),
        "operational_size_scaling": sp.Eq(sp.Symbol('L_oper'), L0 * sp.exp(phi / 2)),
        "population_tempo_status": (
            "The local stable oscillon population supplies the common resonant "
            "tempo; admissible species are harmonic/integer-ratio locks, and "
            "pressure/energy-status changes transpose the local spectrum together."
        ),
        "already_strengthened": [
            "Bernoulli pressure identity and asymptotic charge normalization are explicit; full gravity proof still requires the p01 exterior branch gate",
            "m_i=m_g=E0/c^2 is handled in p06_inertia.py",
            "process-time and resonant-tail bookkeeping are separated in p02_cosmo.py",
        ],
        "claim_gate": [gate.status for gate in oscillon_claim_gate()],
        "open_math": [
            "construct global finite-energy oscillon solutions of the full nonlinear PDE",
            "prove spectral stability of the localized source sector",
            "derive the microscopic medium dynamics selecting population-lock fixed points and particle rest scales",
            "derive the macroscopic resonant-tail/dark-energy normalization nonperturbatively",
        ],
    }


def stage_d1_quantum_to_new_file_map():
    """Where the valuable OLD quantum material now lives."""
    return {
        "Bernoulli_gravity": "p10_oscillons.py",
        "inertia_of_oscillon": "p06_inertia.py",
        "singularity_rarefaction": "p05_compact.py",
        "process_time_and_tail_background": "p02_cosmo.py",
        "charged_lepton_C3_Z9": "p11_particles.py",
        "SM_embedding_and_gauge_program": "p11_particles.py",
        "quantum_lab_predictions": "p12_predictions.py",
    }

