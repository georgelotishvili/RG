# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

"""
p03: solar-system / weak-field ledger.

Status:
- 1PN geometry check is conditional compatibility, not a full RG exterior proof.
- Mercury and 1PN Shapiro are sanity checks once gamma=beta=1 is derived.
- 2PN Shapiro/light-bending is a candidate discriminator until the active RG
  exterior optical index is derived.
- Frame dragging is blocked until the rotating solution and preferred-frame
  PPN parameters alpha_1, alpha_2, alpha_3 are derived.
"""

import math

import sympy as sp
from p01_core import get_polynomial_lagrangian


def coeff_U(expr, U, n):
    """Coefficient of U^n in a symbolic series."""
    return sp.simplify(sp.diff(expr, U, n).subs(U, 0) / sp.factorial(n))

def analyze_ppn():
    r, GM = sp.symbols('r GM', real=True, positive=True)
    U_expr = GM / r
    gamma, beta, a2 = sp.symbols('gamma beta a2', real=True)
    kappa = sp.Symbol('kappa', real=True)
    
    # Standard Schwarzschild-like PPN coordinates
    # B არის g_tt, A არის -g_rr
    A = 1 + 2*gamma*U_expr + a2*U_expr**2
    B = 1 - 2*U_expr + 2*(beta - 1)*U_expr**2

    # აინშტაინის ტენზორი G^mu_nu
    G_tt = -sp.diff(A, r) / (r * A**2) + (1/A - 1)/r**2
    G_rr = sp.diff(B, r) / (r * A * B) + (1/A - 1)/r**2
    G_thth = sp.diff(B, r, 2)/(2*A*B) - sp.diff(B, r)**2/(4*A*B**2) - sp.diff(A, r)*sp.diff(B, r)/(4*A**2*B) + sp.diff(B, r)/(2*r*A*B) - sp.diff(A, r)/(2*r*A**2)

    # U-ზე დაყვანა (GM = U * r)
    U = sp.Symbol('U', real=True, positive=True)
    G_tt_U = sp.simplify(G_tt.subs(GM, U * r))
    G_rr_U = sp.simplify(G_rr.subs(GM, U * r))
    G_thth_U = sp.simplify(G_thth.subs(GM, U * r))

    # Scale by r^2 რათა გახდეს უგანზომილებო პოლინომი U-ში
    G_tt_scaled = sp.simplify(sp.series(G_tt_U * r**2, U, 0, 3).removeO())
    G_rr_scaled = sp.simplify(sp.series(G_rr_U * r**2, U, 0, 3).removeO())
    G_thth_scaled = sp.simplify(sp.series(G_thth_U * r**2, U, 0, 3).removeO())

    # ინვარიანტები (სწორი იდენტიფიკაციით: Y=g^tt=1/B, I1=-g^rr-g^thth-g^phiphi=1/A+2)
    Y = 1/B
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
    
    T_tt = 2 * L_Y / B - L_eval
    T_rr = 2 * (L_I1 / A + 2 * L_I2 / A + L_I3 / A) - L_eval
    T_thth = 2 * (L_I1 + L_I2 * (1 + 1/A) + L_I3 / A) - L_eval

    T_tt_U = sp.simplify(T_tt.subs(GM, U * r))
    T_rr_U = sp.simplify(T_rr.subs(GM, U * r))
    T_thth_U = sp.simplify(T_thth.subs(GM, U * r))
    
    T_tt_series = sp.simplify(sp.series(T_tt_U, U, 0, 3).removeO())
    T_rr_series = sp.simplify(sp.series(T_rr_U, U, 0, 3).removeO())
    T_thth_series = sp.simplify(sp.series(T_thth_U, U, 0, 3).removeO())

    return U, gamma, beta, a2, G_tt_scaled, G_rr_scaled, G_thth_scaled, T_tt_series, T_rr_series, T_thth_series


def ppn_geometry_gate():
    """
    Geometry-only Schwarzschild-like PPN compatibility check.

    This shows what the vacuum Einstein-tensor part would require. It does not
    close the RG exterior solution until the RG stress constraints vanish.
    """
    res = analyze_ppn()
    U, gamma, beta, a2, G_tt_s, G_rr_s, G_thth_s, _, _, _ = res

    G_tt_O1 = coeff_U(G_tt_s, U, 1)
    G_rr_O1 = coeff_U(G_rr_s, U, 1)
    G_thth_O1 = coeff_U(G_thth_s, U, 1)
    G_tt_O2 = coeff_U(G_tt_s, U, 2)
    G_rr_O2 = coeff_U(G_rr_s, U, 2)
    G_thth_O2 = coeff_U(G_thth_s, U, 2)

    geometry_subs = {gamma: 1, a2: 4, beta: 1}

    return {
        "status": "CONDITIONAL_GEOMETRIC_VACUUM_COMPATIBILITY",
        "coordinate_system": "Schwarzschild-like / areal-radius PPN",
        "gamma_condition": [
            sp.Eq(G_rr_O1, 0),
            sp.Eq(G_thth_O1, 0),
        ],
        "a2_condition_after_gamma_1": sp.Eq(sp.simplify(G_tt_O2.subs(gamma, 1)), 0),
        "beta_condition_after_gamma_1_a2_4": [
            sp.Eq(sp.simplify(G_rr_O2.subs({gamma: 1, a2: 4})), 0),
            sp.Eq(sp.simplify(G_thth_O2.subs({gamma: 1, a2: 4})), 0),
        ],
        "residuals_after_geometry_conditions": [
            sp.simplify(G_tt_s.subs(geometry_subs)),
            sp.simplify(G_rr_s.subs(geometry_subs)),
            sp.simplify(G_thth_s.subs(geometry_subs)),
        ],
        "not_claimed": "full RG exterior solution; stress constraints remain open",
    }


def weak_field_stress_constraint_gate():
    """
    RG stress constraints through O(U^2) on the GR-like geometry branch.

    These are blockers: gamma=beta=1 is not an RG exterior proof until these
    coefficients are either derived to vanish or shown to be suppressed.
    """
    res = analyze_ppn()
    U, gamma, beta, a2, _, _, _, T_tt_s, T_rr_s, T_thth_s = res
    geometry_subs = {gamma: 1, a2: 4, beta: 1}

    components = {
        "T^t_t": sp.simplify(T_tt_s.subs(geometry_subs)),
        "T^r_r": sp.simplify(T_rr_s.subs(geometry_subs)),
        "T^theta_theta": sp.simplify(T_thth_s.subs(geometry_subs)),
    }
    coeffs = {
        comp: {
            "O(U^0)": coeff_U(expr, U, 0),
            "O(U^1)": coeff_U(expr, U, 1),
            "O(U^2)": coeff_U(expr, U, 2),
        }
        for comp, expr in components.items()
    }
    equations = {
        comp: [sp.Eq(value, 0) for value in orders.values()]
        for comp, orders in coeffs.items()
    }

    variables = sorted(
        list({
            symbol
            for orders in coeffs.values()
            for value in orders.values()
            for symbol in value.free_symbols
        }),
        key=lambda symbol: symbol.name,
    )
    eqs_o0 = [orders["O(U^0)"] for orders in coeffs.values()]
    eqs_o1 = [orders["O(U^1)"] for orders in coeffs.values()]
    eqs_o2 = [orders["O(U^2)"] for orders in coeffs.values()]
    leading_solution = sp.solve(eqs_o0 + eqs_o1, variables, dict=True)
    strict_solution = sp.solve(eqs_o0 + eqs_o1 + eqs_o2, variables, dict=True)
    leading_subs = leading_solution[0] if leading_solution else {}
    o2_after_leading = {
        comp: sp.simplify(orders["O(U^2)"].subs(leading_subs))
        for comp, orders in coeffs.items()
    }

    return {
        "status": "PARTIAL_1PN_STRESS_CLOSURE_WITH_2PN_OBSTRUCTION",
        "branch": "gamma=1, beta=1, a2=4 geometry inserted",
        "stress_series_after_geometry_conditions": components,
        "coefficients_to_vanish": coeffs,
        "equations_to_solve": equations,
        "leading_O0_O1_solution": leading_solution,
        "O2_residual_after_leading_solution": o2_after_leading,
        "strict_O0_O1_O2_solution": strict_solution,
        "warning": (
            "O(U^0) and O(U^1) have a nontrivial closure branch, but adding "
            "O(U^2) forces the trivial all-zero coefficient solution"
        ),
    }


def solar_1pn_closure_branch():
    """
    Nontrivial stress closure through O(U^1) on the GR-like 1PN branch.

    This strengthens the solar ledger: 1PN compatibility has a concrete
    coefficient branch. It does not close 2PN; the remaining residual is the
    next prediction/obstruction target.
    """
    c_Y2, c_YI1 = sp.symbols("c_Y2 c_YI1", real=True)
    branch = {
        sp.Symbol("c_I1", real=True): 4 * c_Y2 + 2 * c_YI1,
        sp.Symbol("c_I1sq", real=True): c_Y2,
        sp.Symbol("c_I2", real=True): -10 * c_Y2 - 3 * c_YI1,
        sp.Symbol("c_I3", real=True): 8 * c_Y2 + 4 * c_YI1,
        sp.Symbol("c_Y", real=True): -4 * c_Y2 - 2 * c_YI1,
    }
    K_phi = sp.simplify(branch[sp.Symbol("c_Y", real=True)] + 6 * c_Y2 + 3 * c_YI1)
    K_pi = sp.simplify(
        -branch[sp.Symbol("c_I1", real=True)]
        - 6 * branch[sp.Symbol("c_I1sq", real=True)]
        - 2 * branch[sp.Symbol("c_I2", real=True)]
        - branch[sp.Symbol("c_I3", real=True)]
        - c_YI1
    )

    return {
        "status": "NONTRIVIAL_1PN_STRESS_CLOSURE_BRANCH",
        "branch": branch,
        "free_parameters": [c_Y2, c_YI1],
        "phase_no_ghost_prefactor": K_phi,
        "solid_no_ghost_prefactor": K_pi,
        "healthy_window_needed": [
            sp.Gt(K_phi, 0),
            sp.Gt(K_pi, 0),
        ],
        "O2_residual_on_this_branch": {
            "T^t_t O(U^2)": 16 * c_Y2,
            "T^r_r O(U^2)": 16 * c_Y2,
            "T^theta_theta O(U^2)": 8 * c_YI1,
        },
        "interpretation": (
            "1PN Solar-System compatibility can be supported by a nontrivial "
            "coefficient branch; exact GR-like 2PN stress-free closure cannot "
            "be kept unless c_Y2=c_YI1=0, which collapses this branch"
        ),
    }


def solar_1pn_branch_derivation_theorem():
    """
    Machine-check that the printed 1PN branch is derived, not inserted.

    The theorem uses the O(U^0) and O(U^1) stress coefficients on the
    gamma=beta=1, a2=4 geometry branch. It verifies that the nontrivial branch
    listed in solar_1pn_closure_branch() makes all leading stress coefficients
    vanish and that the remaining O(U^2) terms reduce to the stated residuals.
    """
    stress_gate = weak_field_stress_constraint_gate()
    branch_gate = solar_1pn_closure_branch()
    branch = branch_gate["branch"]

    leading_residuals = []
    for orders in stress_gate["coefficients_to_vanish"].values():
        leading_residuals.append(sp.simplify(orders["O(U^0)"].subs(branch)))
        leading_residuals.append(sp.simplify(orders["O(U^1)"].subs(branch)))

    o2_residuals = {
        comp: sp.simplify(orders["O(U^2)"].subs(branch))
        for comp, orders in stress_gate["coefficients_to_vanish"].items()
    }
    expected_o2 = branch_gate["O2_residual_on_this_branch"]
    o2_expected_residuals = [
        sp.simplify(o2_residuals["T^t_t"] - expected_o2["T^t_t O(U^2)"]),
        sp.simplify(o2_residuals["T^r_r"] - expected_o2["T^r_r O(U^2)"]),
        sp.simplify(
            o2_residuals["T^theta_theta"]
            - expected_o2["T^theta_theta O(U^2)"]
        ),
    ]

    c_Y2, c_YI1 = sp.symbols("c_Y2 c_YI1", real=True)
    exact_2pn_solution = sp.solve(
        [
            sp.Eq(expected_o2["T^t_t O(U^2)"], 0),
            sp.Eq(expected_o2["T^theta_theta O(U^2)"], 0),
        ],
        [c_Y2, c_YI1],
        dict=True,
    )

    return {
        "status": (
            "PASS"
            if all(value == 0 for value in leading_residuals + o2_expected_residuals)
            else "CHECK"
        ),
        "branch": branch,
        "leading_O0_O1_residuals_after_branch": leading_residuals,
        "O2_residuals_after_branch": o2_residuals,
        "O2_expected_residual_check": o2_expected_residuals,
        "exact_2PN_stress_free_solution_on_branch": exact_2pn_solution,
        "conclusion": (
            "nontrivial O(U^0)-O(U^1) stress closure exists, while exact "
            "O(U^2) stress-free closure forces c_Y2=c_YI1=0 on this branch"
        ),
    }


def ppn_scope_and_preferred_frame_gate():
    """
    Article-facing boundary for Solar-System claims.

    The current p03 theorem is a static, spherically symmetric, areal-radius
    branch.  It is not yet the full standard PPN calculation for moving
    sources or preferred-frame parameters.
    """
    return {
        "status": "STATIC_SPHERICAL_1PN_ONLY_FULL_PPN_OPEN",
        "closed_here": (
            "gamma=beta=1 on the nontrivial static spherical areal-radius "
            "coefficient branch, with stress closed through O(U^1)"
        ),
        "coordinate_warning": (
            "standard Solar-System bounds are quoted in isotropic PPN gauge; "
            "the areal-radius branch must be mapped before a final PPN export"
        ),
        "preferred_frame_risk": (
            "solid/supersolid backgrounds can generate preferred-frame effects "
            "unless alpha_1, alpha_2, alpha_3 are explicitly derived as zero"
        ),
        "required_before_full_solar_claim": [
            "coordinate bridge to standard isotropic PPN form",
            "moving-source solution",
            "alpha_1=alpha_2=alpha_3 derivation",
            "rotating-source g_0i / frame-dragging solution",
        ],
    }

if __name__ == "__main__":
    res = analyze_ppn()
    U, gamma, beta, a2, G_tt_s, G_rr_s, G_thth_s, T_tt_s, T_rr_s, T_thth_s = res
    
    print("--- PPN ექსპანსია და აინშტაინის განტოლებები ---")
    print("გამოყენებულია სტანდარტული სფერული (Schwarzschild-like) PPN კოორდინატები:")
    print("g_tt = B(r) = 1 - 2U + 2(beta-1)U^2")
    print("g_rr = -A(r) = -(1 + 2*gamma*U + a2*U^2)")
    print("g_thth = -r^2\n")

    print("განზომილებათა აცდენა:")
    print("G^mu_nu ტენზორის კომპონენტები შეიცავენ 1/r^2 ფაქტორს. რადგან U = GM/r, 1/r^2 = U^2/(GM)^2.")
    print("ამიტომ G_scaled = G * r^2 იწყება O(U) რიგით, რაც ნიშნავს G ~ U/r^2 ~ 1/r^3.")
    print("T^mu_nu სტრეს-ტენზორი იწყება O(1) და O(U) რიგით, ანუ T ~ 1 + 1/r.")

    geometry_gate = ppn_geometry_gate()
    stress_gate = weak_field_stress_constraint_gate()

    G_tt_O1 = coeff_U(G_tt_s, U, 1)
    G_rr_O1 = coeff_U(G_rr_s, U, 1)
    G_thth_O1 = coeff_U(G_thth_s, U, 1)

    print("\n--- O(U) რიგის გეომეტრიული ნაწილი (პროპორციულია 1/r^3-ის) ---")
    print("G^t_t (O(U)) =", G_tt_O1)
    print("G^r_r (O(U)) =", G_rr_O1)
    print("G^th_th (O(U)) =", G_thth_O1)
    print("რადგან T^mu_nu-ში 1/r^3 წევრები არ არის (ისინი O(U^3)-ზე იწყება), ეს გეომეტრიული")
    print("წევრები დამოუკიდებლად უნდა განულდეს ვაკუუმში:")
    print(f"G^r_r = 0  =>  {G_rr_O1} = 0  =>  gamma = 1")
    print(f"G^th_th = 0 =>  {G_thth_O1} = 0  =>  gamma = 1")

    G_tt_O2 = coeff_U(G_tt_s, U, 2)
    G_rr_O2 = coeff_U(G_rr_s, U, 2)
    G_thth_O2 = coeff_U(G_thth_s, U, 2)

    G_tt_O2_g1 = sp.simplify(G_tt_O2.subs(gamma, 1))
    G_rr_O2_g1 = sp.simplify(G_rr_O2.subs(gamma, 1))
    G_thth_O2_g1 = sp.simplify(G_thth_O2.subs(gamma, 1))

    print("\n--- O(U^2) რიგის გეომეტრიული ნაწილი (gamma=1 ჩასმით, პროპორციულია 1/r^4-ის) ---")
    print("G^t_t (O(U^2)) =", G_tt_O2_g1)
    print("G^r_r (O(U^2)) =", G_rr_O2_g1)
    print("G^th_th (O(U^2)) =", G_thth_O2_g1)

    print("ვაკუუმში 1/r^4 წევრებიც უნდა განულდეს:")
    print(f"G^t_t = 0  =>  {G_tt_O2_g1} = 0  =>  a2 = 4")

    G_rr_O2_g1_a2 = sp.simplify(G_rr_O2_g1.subs(a2, 4))
    G_thth_O2_g1_a2 = sp.simplify(G_thth_O2_g1.subs(a2, 4))
    print(f"G^r_r (a2=4 ჩასმით) = {G_rr_O2_g1_a2}")
    print(f"G^th_th (a2=4 ჩასმით) = {G_thth_O2_g1_a2}")
    print(f"ორივე განტოლება იძლევა თავსებად პირობას: {G_rr_O2_g1_a2} = 0 (ან {G_thth_O2_g1_a2} = 0)  =>  beta = 1")

    print("\n--- სუპერსოლიდის T_mn constraint gate O(U^2)-მდე ---")
    print("სტატუსი:", stress_gate["status"])
    print("ჩასმული გეომეტრიული შტო:", stress_gate["branch"])
    for comp, coeffs in stress_gate["coefficients_to_vanish"].items():
        print(comp, "coefficients:", coeffs)
    print("O(U^0)+O(U^1) nontrivial solution:", stress_gate["leading_O0_O1_solution"])
    print("O(U^2) residual after that solution:", stress_gate["O2_residual_after_leading_solution"])
    print("strict O(U^0)+O(U^1)+O(U^2) solution:", stress_gate["strict_O0_O1_O2_solution"])
    print("დასკვნა:", stress_gate["warning"])
    
    print("\n--- აგენტთა საბჭოს დასკვნები ---")
    print("1. A და B კოდში სწორადაა იდენტიფიცირებული: B=g_tt, A=-g_rr. სტრეინები B^{AB} ითვლება -1/g_ij-ით (სწორია).")
    print("2. A=1/B წინასწარ აღარ იდება. გამოყვანილია დამოუკიდებელი a2 პარამეტრით G^t_t=0 პირობიდან.")
    print("3. beta=1 დგინდება G^r_r=0 და G^th_th=0 განტოლებებიდან a2=4 ჩასმის შემდეგ.")
    print("4. G^th_th კომპონენტიც დაემატა; corrected O(U), O(U^2) კოეფიციენტებით სისტემა უკვე შეიძლება ერთობლივად შემოწმდეს.")
    print("5. კოორდინატები ცხადად გამოცხადდა როგორც Standard Schwarzschild PPN (არა isotropic).")
    print("6. 1PN stress closure არსებობს, მაგრამ 2PN exact-GR stress-free closure ტრივიალიზდება.")
    print("geometry gate:", geometry_gate["status"])
    print("1PN closure branch:", solar_1pn_closure_branch()["status"])

# ===================== CONSOLIDATED PHASE SECTIONS =====================


# ===================== merged from p03_solar.py =====================

# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

"""
დაკვირვებითი sanity-check.
ეს ბლოკი დამოუკიდებლად არ ამტკიცებს RG მეტრიკას. ის ამოწმებს, რომ
თუ gamma=1 და beta=1 უკვე გამოყვანილია, მერკურის GR/PPN წევრი სწორად ბრუნდება.
"""
import math

def calculate_mercury_precession():
    # გრავიტაციული და ფიზიკური მუდმივები (SI ერთეულებში)
    G_val = 6.67430e-11
    M_sun = 1.98847e30
    c_val = 299792458.0
    
    # მერკურის ორბიტის პარამეტრები
    a_mercury = 57.90905e9   # მეტრი (დიდი ნახევარღერძი)
    e_mercury = 0.205630     # ექსცენტრისიტეტი
    
    # კეპლერის პერიოდი T = 2π√(a³/GM), ფარული ემპირიული შენატანის თავიდან ასაცილებლად
    T_mercury_sec = 2 * math.pi * math.sqrt(a_mercury**3 / (G_val * M_sun))
    T_mercury_days = T_mercury_sec / (24.0 * 3600.0)
    days_per_century = 36525.0
    
    # პირობითი PPN პარამეტრები; მათი RG-დან გამოყვანა stress gate-ს ელოდება.
    gamma_val = 1.0
    beta_val = 1.0
    
    # თეორიული PPN ფაქტორი: (2 + 2*gamma - beta) / 3
    ppn_factor = (2 + 2 * gamma_val - beta_val) / 3.0
    
    # პრეცესია თითო ორბიტაზე (რადიანებში)
    delta_phi_rad = (6 * math.pi * G_val * M_sun) / (c_val**2 * a_mercury * (1 - e_mercury**2)) * ppn_factor
    
    # გადაყვანა არკწამებში თითო საუკუნეზე
    orbits_per_century = days_per_century / T_mercury_days
    rad_to_arcsec = (180.0 / math.pi) * 3600.0
    precession_arcsec_per_century = delta_phi_rad * orbits_per_century * rad_to_arcsec
    
    return ppn_factor, precession_arcsec_per_century


def mercury_precession_gate():
    """Mercury perihelion gate once gamma=beta=1 is independently derived."""
    ppn_factor, precession = calculate_mercury_precession()
    return {
        "status": "MATCHES_STANDARD_GR_TERM_IF_GAMMA_BETA_1",
        "ppn_factor": ppn_factor,
        "precession_arcsec_per_century": precession,
        "reference_value_arcsec_per_century": 42.98,
        "not_claimed": (
            "independent RG proof of gamma=beta=1; this is a conditional "
            "solar-system sanity check"
        ),
    }

if __name__ == "__main__":
    ppn_factor, precession = calculate_mercury_precession()
    print("--- მერკურის პერიჰელიონის პრეცესია: conditional sanity-check ---")
    print(f"PPN ფაქტორი ((2 + 2*gamma - beta)/3): {ppn_factor}")
    print(f"გამოთვლილი პრეცესია: {precession:.2f} არკწამი/საუკუნეში")
    print("სტანდარტული GR/PPN მნიშვნელობა: 42.98 არკწამი/საუკუნეში")
    assert abs(precession - 42.98) < 0.1, f"ცდომილება დიდია: პრეცესია = {precession}"
    print("სტატუსი:", mercury_precession_gate()["status"])


# ===================== merged from p03_solar.py =====================

# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

"""
Shapiro Time Delay (1PN) Sanity-Check.
ეს ფაილი არ გამოჰყავს gamma-ს, არამედ იყენებს p03_solar.py-ში
მიღებულ პირობით შედეგს (gamma=1), რათა შეამოწმოს 1PN ფორმა და Cassini gate.
"""
import sympy as sp

def calculate_shapiro_delay():
    x, b, G, M, c_sym = sp.symbols('x b G M c', real=True, positive=True)
    gamma_sym = sp.Symbol('gamma', real=True)

    # მანძილი გრავიტაციულ ცენტრამდე (r) ტრაექტორიის გასწვრივ (სადაც b არის impact parameter)
    r = sp.sqrt(x**2 + b**2)
    U = G * M / (c_sym**2 * r)

    # ეფექტური რეფრაქციული ინდექსი PPN მეტრიკაში სინათლისთვის (1PN მიახლოება)
    # n(r) = c / c_coord ≈ 1 + (1 + gamma) * U
    n_r = 1 + (1 + gamma_sym) * U

    # დაყოვნების ნაწილი: Delta_n = n(r) - 1
    delta_n = (1 + gamma_sym) * U

    # დროის ინტეგრალი dt = (dx / c) * n(x)
    # \Delta t = \int_{-x_0}^{x_1} (delta_n / c) dx
    x0, x1 = sp.symbols('x0 x1', real=True, positive=True)

    delay_integrand = delta_n / c_sym
    
    # ინტეგრაცია (გვაძლევს asinh(x/b), რაც ლოგარითმში გადადის)
    # asinh(x/b) = ln(x/b + sqrt((x/b)^2 + 1)) = ln((x + sqrt(x^2 + b^2))/b)
    integral_res = (1 + gamma_sym) * G * M / c_sym**3 * sp.ln(x + sp.sqrt(x**2 + b**2))
    
    # ინტეგრალის საზღვრები: -x0-დან x1-მდე
    log_term = sp.ln((x1 + sp.sqrt(x1**2 + b**2)) * (x0 + sp.sqrt(x0**2 + b**2)) / b**2)
    coef = (1 + gamma_sym) * G * M / c_sym**3
    # ვიყენებთ Mul(..., evaluate=False) რათა coef არ შევიდეს log-ის შიგნით (base**coef)
    delta_t_general = sp.Mul(coef, log_term, evaluate=False)
    
    return delta_n, delta_t_general, gamma_sym


def cassini_gamma_gate(gamma_value=1.0):
    """
    Cassini 1PN gamma gate.

    Bertotti, Iess, Tortora (Nature 2003): gamma - 1 = (2.1 +/- 2.3)e-5.
    This gate is passed only after gamma is independently derived in the RG
    exterior branch.
    """
    central = 2.1e-5
    sigma = 2.3e-5
    conservative_bound = abs(central) + sigma
    deviation = abs(gamma_value - 1.0)
    return {
        "status": "PASS_IF_GAMMA_DERIVED" if deviation <= conservative_bound else "FAIL",
        "gamma_value": gamma_value,
        "abs_gamma_minus_1": deviation,
        "cassini_central_gamma_minus_1": central,
        "cassini_sigma": sigma,
        "conservative_bound": conservative_bound,
        "source": "Bertotti, Iess, Tortora, Nature 425, 374-376 (2003)",
        "not_claimed": "Cassini pass before gamma is derived from RG stress/exterior equations",
    }


def solar_ansatz_scope_table():
    """
    Reviewer-facing map of the Solar ansatzes used in the article.

    The weak-field section uses three related but distinct metric/coordinate
    ansatzes.  Keeping them in one table prevents the minimal truncation,
    isotropic 2PN closure, and S=6 completion branch from being read as the
    same exterior solution.
    """
    U, u, gamma, beta, b2 = sp.symbols("U u gamma beta b_2", real=True)
    A_area = "Schwarzschild-like areal radial coefficient, expanded through 1PN"
    B_area = "Schwarzschild-like time coefficient, expanded through 1PN"
    A_iso = 1 - 2 * u + 2 * beta * u**2
    B_iso = 1 + 2 * gamma * u + b2 * u**2
    A_completion = 1 + 2 * U + 4 * U**2
    B_completion = 1 - 2 * U

    static_spherical_invariants = {
        "B_AB_eigenvalues": [sp.Symbol("A") ** -1, 1, 1],
        "I1": 2 + sp.Symbol("A") ** -1,
        "I2": 1 + 2 * sp.Symbol("A") ** -1,
        "I3": sp.Symbol("A") ** -1,
        "Y": sp.Symbol("B") ** -1,
    }

    return {
        "status": "PASS_SOLAR_ANSATZ_SCOPE_TABLE",
        "static_spherical_invariant_derivation": static_spherical_invariants,
        "rows": [
            {
                "ansatz": "areal-radius PN",
                "A_r": A_area,
                "B_t": B_area,
                "scope": "minimal 7-coefficient truncation, 1PN stress closure",
            },
            {
                "ansatz": "isotropic 2PN",
                "A_r": A_iso,
                "B_t": B_iso,
                "scope": "minimal isotropic closure and b2/q_2PN derivation",
            },
            {
                "ansatz": "S=6 completion 1PN",
                "A_r": A_completion,
                "B_t": B_completion,
                "scope": "completion branch showing LCDM plus Solar 1PN closure",
            },
        ],
        "article_rule": (
            "q_2PN=10 belongs to the minimal isotropic closure; the S=6 "
            "completion needs a separate isotropic 2PN exterior before q_2PN "
            "can be assigned to it"
        ),
    }


def q2pn_cassini_scale_estimate(q_rg=sp.Integer(10), b_over_r_sun=1.0):
    """
    Numerical scale of the q_2PN=10 branch near the solar limb.

    This is not a Cassini likelihood and not a formal exclusion.  It converts
    the minimal isotropic 2PN branch into the size of the local optical-index
    correction and the one-way 2PN Shapiro delay scale.
    """
    q_gr = sp.Rational(7, 4)
    delta_q = sp.simplify(q_rg - q_gr)

    rg_sun_m = 1.4766250385e3  # GM_sun/c^2
    r_sun_m = 6.957e8
    c_m_s = 299_792_458.0
    u_limb = rg_sun_m / (r_sun_m * b_over_r_sun)

    local_equiv_delta_gamma = float(delta_q) * u_limb
    local_relative_to_1pn_index = local_equiv_delta_gamma / 2.0
    extra_delay_s = float(delta_q) * math.pi * rg_sun_m**2 / (
        c_m_s * r_sun_m * b_over_r_sun
    )
    extra_path_m = c_m_s * extra_delay_s

    cassini_central = 2.1e-5
    cassini_sigma = 2.3e-5
    cassini_conservative = abs(cassini_central) + cassini_sigma

    return {
        "status": "NEAR_CASSINI_SENSITIVITY_REQUIRES_FULL_2PN_FIT",
        "q_RG": q_rg,
        "q_GR": q_gr,
        "Delta_q": delta_q,
        "solar_limb_u": u_limb,
        "b_over_R_sun": b_over_r_sun,
        "local_equivalent_gamma_minus_1_proxy": local_equiv_delta_gamma,
        "local_relative_to_1PN_index": local_relative_to_1pn_index,
        "one_way_extra_2PN_delay_seconds": extra_delay_s,
        "one_way_extra_2PN_light_path_meters": extra_path_m,
        "cassini_gamma_minus_1_central": cassini_central,
        "cassini_gamma_sigma": cassini_sigma,
        "cassini_conservative_gamma_bound": cassini_conservative,
        "proxy_in_sigma_units": local_equiv_delta_gamma / cassini_sigma,
        "proxy_fraction_of_conservative_bound": (
            local_equiv_delta_gamma / cassini_conservative
        ),
        "proxy_verdict": (
            "not a formal exclusion by itself; the signal is close enough to "
            "Cassini sensitivity that a full 2PN Doppler/Shapiro fit is mandatory"
        ),
    }


def derive_general_q2pn_optical_observables(q_rg=sp.Integer(10), b_over_r_sun=1.0):
    """
    General isotropic 2PN optical observables for n=1+2u+q*u^2.

    This block is deliberately independent of the old exponential candidate.
    If a metric branch gives q_2PN=q, the Shapiro and bending coefficients
    below are the direct observables to compare with GR.
    """
    q, s, y, r_g, b, c = sp.symbols("q s y r_g b c", positive=True)
    q_gr = sp.Rational(7, 4)
    delta_q = sp.simplify(q - q_gr)

    n_2pn = 1 + 2 * s + q * s**2

    z = sp.Symbol("z", real=True)
    shapiro_integral = sp.integrate(
        1 / (b**2 + z**2),
        (z, -sp.oo, sp.oo),
    )
    shapiro_delta = sp.simplify(delta_q * r_g**2 * shapiro_integral / c)

    # Fermat bending derivation.  With x=b/r and endpoint x0=n(x0),
    # x0=1+2s+(q+4)s^2.  Setting x=x0*y gives regular integrals on [0,1].
    I0 = sp.pi / 2
    I1 = sp.Integer(2)
    I2 = sp.pi * (q + 2) / 2
    phi_half = I0 + I1 * s + I2 * s**2
    bending = sp.simplify(2 * phi_half - sp.pi)
    bending_gr = sp.simplify(bending.subs(q, q_gr))
    bending_delta = sp.simplify(bending - bending_gr)

    q_rg_value = sp.sympify(q_rg)
    delta_q_rg = sp.simplify(q_rg_value - q_gr)
    rg_sun_m = 1.4766250385e3
    r_sun_m = 6.957e8
    c_m_s = 299_792_458.0
    u_limb = rg_sun_m / (r_sun_m * b_over_r_sun)
    rad_to_microarcsec = 180.0 / math.pi * 3_600.0 * 1_000_000.0

    extra_shapiro_s = float(delta_q_rg) * math.pi * rg_sun_m**2 / (
        c_m_s * r_sun_m * b_over_r_sun
    )
    bending_1pn_rad = 4.0 * u_limb
    bending_gr_2pn_rad = float(sp.pi * (q_gr + 2)) * u_limb**2
    bending_rg_2pn_rad = float(sp.pi * (q_rg_value + 2)) * u_limb**2
    bending_delta_rad = float(sp.pi * delta_q_rg) * u_limb**2

    endpoint_integrand_series = {
        "I0_integrand": "1/sqrt(1-y^2)",
        "I1_integrand": "2/((1+y)*sqrt(1-y^2))",
        "I2_integrand": (
            "(q*(1+y)^2 + 2*y^2 + 4)/(sqrt(1-y)*(1+y)^(5/2))"
        ),
    }

    return {
        "status": "DERIVED_GENERAL_Q2PN_OPTICAL_OBSERVABLES",
        "input_optical_index": sp.Eq(sp.Symbol("n"), n_2pn),
        "q_GR": q_gr,
        "Delta_q": sp.Eq(sp.Symbol("Delta_q"), delta_q),
        "turning_point_x0": sp.Eq(sp.Symbol("x0"), 1 + 2 * s + (q + 4) * s**2),
        "bending_integrals": {
            "regularized_integrands": endpoint_integrand_series,
            "I0": I0,
            "I1": I1,
            "I2": I2,
        },
        "bending_angle_general": sp.Eq(sp.Symbol("Delta_theta"), bending),
        "bending_angle_GR": sp.Eq(sp.Symbol("Delta_theta_GR"), bending_gr),
        "bending_angle_RG_minus_GR": sp.Eq(
            sp.Symbol("Delta_theta_RG_minus_GR"),
            bending_delta,
        ),
        "shapiro_master_integral_infinite": shapiro_integral,
        "shapiro_RG_minus_GR": sp.Eq(sp.Symbol("Delta_t"), shapiro_delta),
        "q10_results": {
            "q_RG": q_rg_value,
            "Delta_q": delta_q_rg,
            "Delta_t_one_way_seconds_at_solar_limb": extra_shapiro_s,
            "Delta_t_one_way_light_path_meters": c_m_s * extra_shapiro_s,
            "bending_1PN_rad": bending_1pn_rad,
            "bending_GR_2PN_rad": bending_gr_2pn_rad,
            "bending_RG_2PN_rad": bending_rg_2pn_rad,
            "bending_RG_minus_GR_rad": bending_delta_rad,
            "bending_RG_minus_GR_microarcsec": bending_delta_rad * rad_to_microarcsec,
            "RG_over_GR_2PN_bending_ratio": float((q_rg_value + 2) / (q_gr + 2)),
        },
        "checks": {
            "GR_bending_coefficient": sp.simplify((q_gr + 2) * sp.pi),
            "old_exponential_q2_bending_ratio": sp.simplify(
                (sp.Integer(2) + 2) / (q_gr + 2)
            ),
            "q10_bending_ratio": sp.simplify((q_rg_value + 2) / (q_gr + 2)),
            "q10_shapiro_coefficient": sp.simplify(delta_q_rg * sp.pi),
        },
        "promotion_rule": (
            "usable for article only after the RG exterior metric fixes q_2PN "
            "and the coordinate bridge to isotropic optical variables is derived"
        ),
    }


def cassini_2pn_tracking_proxy_theorem(
    q_rg=sp.Integer(10),
    b_over_r_sun=1.6,
    r_earth_au=1.0,
    r_spacecraft_au=8.43,
):
    """
    Finite-endpoint two-way Shapiro/Doppler proxy for the q_2PN branch.

    This is still a proxy, not a reconstruction of the raw Cassini Doppler
    likelihood.  It is stronger than a local scale estimate because it keeps
    the transmitter/receiver distances finite and compares the induced 2PN
    Doppler scaling to the published gamma-1 central value and sigma.
    """
    q_gr = sp.Rational(7, 4)
    q_rg_value = sp.sympify(q_rg)
    delta_q = float(q_rg_value - q_gr)

    rg_sun_m = 1.4766250385e3
    r_sun_m = 6.957e8
    au_m = 149_597_870_700.0
    c_m_s = 299_792_458.0

    b_m = b_over_r_sun * r_sun_m
    r1_m = r_earth_au * au_m
    r2_m = r_spacecraft_au * au_m
    if b_m >= min(r1_m, r2_m):
        raise ValueError("impact parameter must be smaller than both endpoints")

    z1_m = math.sqrt(r1_m**2 - b_m**2)
    z2_m = math.sqrt(r2_m**2 - b_m**2)
    endpoint_angle = math.acos(b_m / r1_m) + math.acos(b_m / r2_m)
    shapiro_2pn_integral = endpoint_angle / b_m
    d_integral_db = (
        -endpoint_angle / b_m**2
        - (1.0 / b_m) * (1.0 / z1_m + 1.0 / z2_m)
    )

    log_argument = ((r1_m + z1_m) * (r2_m + z2_m)) / b_m**2
    shapiro_1pn_log = math.log(log_argument)
    d_log_db = (
        -b_m / (z1_m * (r1_m + z1_m))
        - b_m / (z2_m * (r2_m + z2_m))
        - 2.0 / b_m
    )

    one_way_2pn_extra_s = (
        delta_q * rg_sun_m**2 * shapiro_2pn_integral / c_m_s
    )
    two_way_2pn_extra_s = 2.0 * one_way_2pn_extra_s
    delay_equivalent_gamma = (
        two_way_2pn_extra_s / (2.0 * rg_sun_m * shapiro_1pn_log / c_m_s)
    )
    doppler_equivalent_gamma = delta_q * rg_sun_m * d_integral_db / d_log_db

    cassini_central = 2.1e-5
    cassini_sigma = 2.3e-5
    conservative_bound = abs(cassini_central) + cassini_sigma
    sigma_distance = abs(doppler_equivalent_gamma - cassini_central) / cassini_sigma

    gamma_per_delta_q = rg_sun_m * d_integral_db / d_log_db
    q_interval_1sigma = (
        float(q_gr) + (cassini_central - cassini_sigma) / gamma_per_delta_q,
        float(q_gr) + (cassini_central + cassini_sigma) / gamma_per_delta_q,
    )
    q_interval_conservative = (
        float(q_gr) - conservative_bound / abs(gamma_per_delta_q),
        float(q_gr) + conservative_bound / abs(gamma_per_delta_q),
    )
    q_passes_1sigma = q_interval_1sigma[0] <= float(q_rg_value) <= q_interval_1sigma[1]
    q_passes_conservative = (
        q_interval_conservative[0]
        <= float(q_rg_value)
        <= q_interval_conservative[1]
    )

    status = (
        "PASS_CASSINI_2PN_TRACKING_PROXY_DEFAULT_GEOMETRY"
        if q_passes_1sigma and q_passes_conservative
        else "CHECK_CASSINI_2PN_TRACKING_PROXY_DEFAULT_GEOMETRY"
    )

    return {
        "status": status,
        "q_RG": q_rg_value,
        "q_GR": q_gr,
        "Delta_q": sp.simplify(q_rg_value - q_gr),
        "geometry": {
            "b_over_R_sun": b_over_r_sun,
            "r_earth_AU": r_earth_au,
            "r_spacecraft_AU": r_spacecraft_au,
            "endpoint_angle_rad": endpoint_angle,
            "shapiro_1PN_log": shapiro_1pn_log,
        },
        "finite_endpoint_integrals": {
            "I_2PN": shapiro_2pn_integral,
            "dI_2PN_db": d_integral_db,
            "dlog_1PN_db": d_log_db,
        },
        "two_way_2PN_extra_seconds": two_way_2pn_extra_s,
        "two_way_2PN_extra_light_path_meters": c_m_s * two_way_2pn_extra_s,
        "delay_equivalent_gamma_minus_1": delay_equivalent_gamma,
        "doppler_equivalent_gamma_minus_1": doppler_equivalent_gamma,
        "cassini_gamma_minus_1_central": cassini_central,
        "cassini_gamma_sigma": cassini_sigma,
        "sigma_distance_from_central": sigma_distance,
        "q_interval_1sigma_from_proxy": q_interval_1sigma,
        "q_interval_conservative_from_proxy": q_interval_conservative,
        "q_passes_1sigma_proxy": q_passes_1sigma,
        "q_passes_conservative_proxy": q_passes_conservative,
        "scope": (
            "finite-endpoint two-way Shapiro/Doppler proxy; full raw Doppler "
            "time-series likelihood and ephemeris nuisance fit are not included"
        ),
    }


def q2pn_observational_table(
    q_rg=sp.Integer(10),
    b_over_r_sun_values=(1.0, 1.5, 1.6, 2.0, 5.0, 10.0),
):
    """
    Table-ready q_2PN observables.

    This is the numerical payload for the article table/figure.  It keeps the
    result distinct from a Cassini raw likelihood: each row is a direct
    observable scale at a chosen impact parameter.
    """
    q_gr = sp.Rational(7, 4)
    q_rg_value = sp.sympify(q_rg)
    delta_q = float(q_rg_value - q_gr)

    rg_sun_m = 1.4766250385e3
    r_sun_m = 6.957e8
    c_m_s = 299_792_458.0
    rad_to_microarcsec = 180.0 / math.pi * 3_600.0 * 1_000_000.0

    rows = []
    for b_over_r_sun in b_over_r_sun_values:
        b_scale = float(b_over_r_sun)
        u = rg_sun_m / (r_sun_m * b_scale)
        one_way_delay_s = delta_q * math.pi * rg_sun_m**2 / (
            c_m_s * r_sun_m * b_scale
        )
        delta_bending_rad = delta_q * math.pi * u**2
        rows.append(
            {
                "b_over_R_sun": b_scale,
                "u": u,
                "Delta_gamma_eff_proxy": delta_q * u,
                "one_way_extra_delay_s": one_way_delay_s,
                "one_way_extra_path_m": c_m_s * one_way_delay_s,
                "two_way_extra_path_m": 2.0 * c_m_s * one_way_delay_s,
                "Delta_light_bending_microarcsec": (
                    delta_bending_rad * rad_to_microarcsec
                ),
            }
        )

    return {
        "status": "PASS_Q2PN_OBSERVATIONAL_TABLE",
        "q_RG": q_rg_value,
        "q_GR": q_gr,
        "Delta_q": sp.simplify(q_rg_value - q_gr),
        "rows": rows,
        "scope": (
            "direct q_2PN observable scales for article table/figure; not a "
            "replacement for raw Cassini Doppler or astrometric likelihood"
        ),
    }


def cassini_2pn_raw_likelihood_gate():
    """
    Exact form of the missing raw Cassini likelihood.

    The repository does not contain Cassini Doppler time series, spacecraft
    ephemerides, plasma calibration, covariance, or the original nuisance
    model.  This function therefore does not invent a likelihood value.  It
    records the model vector that must be fitted when those data are supplied.
    """
    q, q_gr, r_g, c, b = sp.symbols("q q_GR r_g c b", positive=True)
    r1, r2, z1, z2 = sp.symbols("r_1 r_2 z_1 z_2", positive=True)
    delta_q = q - q_gr
    endpoint_angle = sp.acos(b / r1) + sp.acos(b / r2)
    one_way_delta_t = sp.simplify(delta_q * r_g**2 * endpoint_angle / (c * b))
    two_way_delta_t = sp.simplify(2 * one_way_delta_t)
    doppler_template = sp.Symbol("d_dt") * two_way_delta_t

    proxy = cassini_2pn_tracking_proxy_theorem()
    table = q2pn_observational_table()

    return {
        "status": "FORMULATED_REQUIRES_RAW_CASSINI_DOPPLER_DATA",
        "model_vector": {
            "one_way_delta_t_2PN": one_way_delta_t,
            "two_way_delta_t_2PN": two_way_delta_t,
            "doppler_template": doppler_template,
        },
        "finite_endpoint_definitions": {
            "z_1": sp.Eq(z1, sp.sqrt(r1**2 - b**2)),
            "z_2": sp.Eq(z2, sp.sqrt(r2**2 - b**2)),
            "endpoint_angle": endpoint_angle,
        },
        "likelihood_form": (
            "chi2=(d-M(theta,q_2PN))^T C^-1 (d-M(theta,q_2PN)); "
            "theta must include orbit, plasma, clock, solar-corona and gamma "
            "nuisance parameters"
        ),
        "available_compressed_proxy": proxy["status"],
        "default_proxy_sigma_distance": proxy["sigma_distance_from_central"],
        "default_proxy_q_passes_1sigma": proxy["q_passes_1sigma_proxy"],
        "default_proxy_q_passes_conservative": (
            proxy["q_passes_conservative_proxy"]
        ),
        "table_payload_status": table["status"],
        "missing_inputs": [
            "Cassini Doppler residual time series",
            "spacecraft and Earth ephemerides during solar conjunction",
            "solar-plasma calibration and covariance",
            "clock/noise covariance matrix",
            "nuisance-parameter priors used in the radio-science fit",
        ],
        "article_rule": (
            "report q_2PN=10 as not excluded by the compressed proxy, but do "
            "not claim a final Cassini likelihood pass until the raw-data fit "
            "is run"
        ),
    }


def standard_ppn_alpha_i_export_table():
    """
    Article-ready preferred-frame PPN table.

    The symbolic matcher fixes alpha_i=0 after the RG moving-source vector
    source has vanished on the Solar 1PN branch.  This function packages the
    result with the observational bounds used in the text.
    """
    matcher = standard_ppn_alpha_i_matcher()
    chain = preferred_frame_alpha_i_closure_chain()
    limits = preferred_frame_velocity_risk_estimate()[
        "preferred_frame_limits_used"
    ]
    rows = []
    for key, bound in limits.items():
        value = matcher["alpha_i_values"][key]
        rows.append(
            {
                "parameter": key,
                "RG_minimal_value": value,
                "observational_bound_order": bound,
                "passes_bound": value == 0,
            }
        )

    status = (
        "PASS_STANDARD_PPN_ALPHA_I_EXPORT_TABLE"
        if chain["status"] == "PASS_MINIMAL_MOVING_SOURCE_ALPHA_I_CHAIN"
        and matcher["status"] == "PASS_STANDARD_PPN_MATCH_FORCES_ALPHA_I_ZERO"
        and all(row["passes_bound"] for row in rows)
        else "CHECK_STANDARD_PPN_ALPHA_I_EXPORT_TABLE"
    )

    return {
        "status": status,
        "rows": rows,
        "matcher_status": matcher["status"],
        "closure_chain_status": chain["status"],
        "scope": (
            "standard PPN alpha_i export after the minimal moving-source RG "
            "vector-source check; full solar-system likelihood remains separate"
        ),
    }


def preferred_frame_alpha_i_appendix_payload():
    """
    Full article appendix payload for alpha_1=alpha_2=alpha_3=0.

    This collects the four steps a reader needs to reproduce the preferred-
    frame claim without hunting through the code: boosted background stress,
    vector source, standard PPN matcher, and the final alpha table.
    """
    background = preferred_frame_background_stress_theorem()
    vector_source = moving_source_rg_vector_source_theorem()
    matcher = standard_ppn_alpha_i_matcher()
    export_table = standard_ppn_alpha_i_export_table()
    chain = preferred_frame_alpha_i_closure_chain()

    status = (
        "PASS_ALPHA_I_APPENDIX_PAYLOAD"
        if background["status"] == "PASS_BACKGROUND_PREFERRED_FRAME_STRESS_ON_1PN_BRANCH"
        and vector_source["status"] == "PASS_RG_VECTOR_SOURCE_ABSENT_ON_1PN_BRANCH"
        and matcher["status"] == "PASS_STANDARD_PPN_MATCH_FORCES_ALPHA_I_ZERO"
        and export_table["status"] == "PASS_STANDARD_PPN_ALPHA_I_EXPORT_TABLE"
        and chain["status"] == "PASS_MINIMAL_MOVING_SOURCE_ALPHA_I_CHAIN"
        else "CHECK_ALPHA_I_APPENDIX_PAYLOAD"
    )

    return {
        "status": status,
        "step_1_boosted_background": {
            "status": background["status"],
            "common_prefactor_K_pf": background["common_prefactor_K_pf"],
            "branch_prefactor": background["solar_1PN_branch_prefactor"],
            "T0i_residuals": background[
                "solar_1PN_branch_T0i_linear_residuals"
            ],
            "anisotropy_residuals": background[
                "solar_1PN_branch_spatial_anisotropy_residuals"
            ],
        },
        "step_2_rg_vector_source": {
            "status": vector_source["status"],
            "h_matrix_on_branch": vector_source[
                "h_linear_matrix_on_1PN_branch"
            ],
            "v_matrix_on_branch": vector_source[
                "v_linear_matrix_on_1PN_branch"
            ],
        },
        "step_3_standard_ppn_matcher": {
            "status": matcher["status"],
            "vector_coefficients": matcher["ppn_vector_coefficients"],
            "preferred_frame_coefficients": matcher[
                "ppn_g00_preferred_frame_coefficients"
            ],
            "solution": matcher["solution"],
            "residuals_after_solution": matcher["residuals_after_solution"],
            "remaining_non_alpha_condition": matcher[
                "remaining_non_alpha_condition"
            ],
        },
        "step_4_alpha_table": export_table["rows"],
        "scope": (
            "minimal one-metric moving-source alpha_i proof; raw solar-system "
            "ephemeris likelihood remains outside this appendix"
        ),
    }


def preferred_frame_velocity_risk_estimate():
    """
    Preferred-frame risk scale from the Solar System velocity relative to CMB.

    This does not derive alpha_i.  It quantifies why an O(1) preferred-frame
    coefficient would be fatal and why alpha_i must be derived as zero or
    screened/suppressed in the moving-source sector.
    """
    v_cmb_m_s = 369_000.0
    c_m_s = 299_792_458.0
    beta_cmb = v_cmb_m_s / c_m_s
    limits = {
        "alpha_1": 1.0e-4,
        "alpha_2": 1.0e-7,
        "alpha_3": 1.0e-20,
    }
    natural_signal_scale = {
        key: beta_cmb * value
        for key, value in {
            "alpha_1_if_O1": 1.0,
            "alpha_2_if_O1": 1.0,
            "alpha_3_if_O1": 1.0,
        }.items()
    }
    required_suppressions = {
        key: limit for key, limit in limits.items()
    }
    return {
        "status": "NOT_DERIVED_STATIC_BRANCH_INSUFFICIENT",
        "solar_system_speed_relative_to_CMB_m_s": v_cmb_m_s,
        "beta_CMB": beta_cmb,
        "beta_CMB_squared": beta_cmb**2,
        "preferred_frame_limits_used": limits,
        "natural_O1_velocity_signal_scale": natural_signal_scale,
        "required_alpha_i_suppression": required_suppressions,
        "verdict": (
            "the static spherical 1PN branch cannot determine alpha_i; a boosted "
            "or moving-source calculation must derive alpha_1=alpha_2=alpha_3=0 "
            "or an explicit suppression mechanism"
        ),
    }


def preferred_frame_background_stress_theorem():
    """
    Necessary boosted-background check for preferred-frame safety.

    This is not the full standard PPN alpha_i derivation.  It closes the first
    algebraic subproblem: a Solar-System frame moving with small velocity v_i
    through the normalized RG medium must not see an O(v_i) background momentum
    flux T_0i from the RG sector.
    """
    t, x, y, z = sp.symbols("t x y z", real=True)
    vx, vy, vz = sp.symbols("v_x v_y v_z", real=True)
    coords = (t, x, y, z)

    q00, q11, q22, q33 = sp.symbols("q00 q11 q22 q33", real=True)
    q01, q02, q03, q12, q13, q23 = sp.symbols(
        "q01 q02 q03 q12 q13 q23",
        real=True,
    )
    g_inv = sp.Matrix([
        [q00, q01, q02, q03],
        [q01, q11, q12, q13],
        [q02, q12, q22, q23],
        [q03, q13, q23, q33],
    ])

    # Linear boost is enough for the PPN preferred-frame source T_0i=O(v_i).
    Phi = t - vx * x - vy * y - vz * z
    phi_fields = (
        x - vx * t,
        y - vy * t,
        z - vz * t,
    )
    d_Phi = [sp.diff(Phi, coord) for coord in coords]
    d_phi = [
        [sp.diff(field, coord) for coord in coords]
        for field in phi_fields
    ]

    Y = sp.simplify(
        sum(g_inv[i, j] * d_Phi[i] * d_Phi[j] for i in range(4) for j in range(4))
    )
    B = sp.zeros(3, 3)
    for A in range(3):
        for B_idx in range(3):
            B[A, B_idx] = sp.simplify(
                sum(
                    -g_inv[i, j] * d_phi[A][i] * d_phi[B_idx][j]
                    for i in range(4)
                    for j in range(4)
                )
            )

    I1 = sp.simplify(B.trace())
    I2 = sp.simplify(sp.Rational(1, 2) * (I1**2 - (B * B).trace()))
    I3 = sp.simplify(B.det())
    L = get_polynomial_lagrangian(Y, I1, I2, I3)

    minkowski_subs = {
        q00: 1,
        q11: -1,
        q22: -1,
        q33: -1,
        q01: 0,
        q02: 0,
        q03: 0,
        q12: 0,
        q13: 0,
        q23: 0,
    }
    velocity_zero = {vx: 0, vy: 0, vz: 0}
    offdiag_vars = (q01, q02, q03)
    velocity_vars = (vx, vy, vz)
    labels = ("T_01", "T_02", "T_03")

    T0i = [
        sp.simplify(sp.diff(L, q_var).subs(minkowski_subs))
        for q_var in offdiag_vars
    ]
    T11 = sp.simplify((2 * sp.diff(L, q11) + L).subs(minkowski_subs))
    T22 = sp.simplify((2 * sp.diff(L, q22) + L).subs(minkowski_subs))
    T33 = sp.simplify((2 * sp.diff(L, q33) + L).subs(minkowski_subs))
    T12 = sp.simplify(sp.diff(L, q12).subs(minkowski_subs))
    T13 = sp.simplify(sp.diff(L, q13).subs(minkowski_subs))
    T23 = sp.simplify(sp.diff(L, q23).subs(minkowski_subs))

    linear_coefficients = {
        label: sp.simplify(sp.diff(component, velocity).subs(velocity_zero))
        for label, component, velocity in zip(labels, T0i, velocity_vars)
    }
    common_prefactor = sp.simplify(-linear_coefficients["T_01"] / 2)
    prefactor_checks = [
        sp.simplify(-linear_coefficients[label] / 2 - common_prefactor)
        for label in labels
    ]
    spatial_anisotropy_coefficients = {
        "T_11_minus_T_22_vx2": sp.simplify(
            sp.diff(T11 - T22, vx, 2).subs(velocity_zero) / 2
        ),
        "T_11_minus_T_22_vy2": sp.simplify(
            sp.diff(T11 - T22, vy, 2).subs(velocity_zero) / 2
        ),
        "T_11_minus_T_33_vx2": sp.simplify(
            sp.diff(T11 - T33, vx, 2).subs(velocity_zero) / 2
        ),
        "T_11_minus_T_33_vz2": sp.simplify(
            sp.diff(T11 - T33, vz, 2).subs(velocity_zero) / 2
        ),
        "T_22_minus_T_33_vy2": sp.simplify(
            sp.diff(T22 - T33, vy, 2).subs(velocity_zero) / 2
        ),
        "T_22_minus_T_33_vz2": sp.simplify(
            sp.diff(T22 - T33, vz, 2).subs(velocity_zero) / 2
        ),
        "T_12_vxvy": sp.simplify(sp.diff(sp.diff(T12, vx), vy).subs(velocity_zero)),
        "T_13_vxvz": sp.simplify(sp.diff(sp.diff(T13, vx), vz).subs(velocity_zero)),
        "T_23_vyvz": sp.simplify(sp.diff(sp.diff(T23, vy), vz).subs(velocity_zero)),
    }

    branch = solar_1pn_closure_branch()["branch"]
    branch_residuals = {
        label: sp.simplify(value.subs(branch))
        for label, value in linear_coefficients.items()
    }
    branch_spatial_anisotropy_residuals = {
        label: sp.simplify(value.subs(branch))
        for label, value in spatial_anisotropy_coefficients.items()
    }
    branch_prefactor = sp.simplify(common_prefactor.subs(branch))

    status = (
        "PASS_BACKGROUND_PREFERRED_FRAME_STRESS_ON_1PN_BRANCH"
        if branch_prefactor == 0
        and all(value == 0 for value in branch_residuals.values())
        and all(value == 0 for value in branch_spatial_anisotropy_residuals.values())
        and all(value == 0 for value in prefactor_checks)
        else "CHECK_BACKGROUND_PREFERRED_FRAME_STRESS"
    )

    return {
        "status": status,
        "linear_boost_fields": {
            "Phi": Phi,
            "phi_1": phi_fields[0],
            "phi_2": phi_fields[1],
            "phi_3": phi_fields[2],
        },
        "T0i_linear_coefficients": linear_coefficients,
        "common_prefactor_K_pf": common_prefactor,
        "all_direction_prefactor_checks": prefactor_checks,
        "spatial_anisotropy_quadratic_coefficients": spatial_anisotropy_coefficients,
        "solar_1PN_branch_prefactor": branch_prefactor,
        "solar_1PN_branch_T0i_linear_residuals": branch_residuals,
        "solar_1PN_branch_spatial_anisotropy_residuals": (
            branch_spatial_anisotropy_residuals
        ),
        "closed_here": (
            "the normalized boosted background has no O(v_i) RG momentum flux "
            "and no O(v_i v_j) spatial anisotropic stress on the nontrivial "
            "1PN stress-closure branch"
        ),
        "not_closed_here": (
            "full alpha_1, alpha_2, alpha_3 PPN proof still requires the "
            "moving-source metric solution, matter velocity potentials, and "
            "standard PPN gauge matching"
        ),
    }


def standard_ppn_alpha_i_matcher():
    """
    Standard PPN alpha_i algebraic matcher.

    This block is the gauge-side half of the preferred-frame proof.  It uses
    the Will-Nordtvedt alpha-zeta PPN form and asks: if RG's moving-source
    metric has the GR vector coefficients and no w-dependent preferred-frame
    metric terms, what values are forced for alpha_1, alpha_2, alpha_3?
    """
    gamma, xi, zeta1 = sp.symbols("gamma xi zeta_1", real=True)
    alpha1, alpha2, alpha3 = sp.symbols("alpha_1 alpha_2 alpha_3", real=True)

    coeff_V = -sp.Rational(1, 2) * (
        4 * gamma + 3 + alpha1 - alpha2 + zeta1 - 2 * xi
    )
    coeff_W = -sp.Rational(1, 2) * (
        1 + alpha2 - zeta1 + 2 * xi
    )
    coeff_wU_g0i = -sp.Rational(1, 2) * (alpha1 - 2 * alpha2)
    coeff_wUij_g0i = -alpha2

    coeff_w2U_g00 = -(alpha1 - alpha2 - alpha3)
    coeff_wiwjUij_g00 = -alpha2
    coeff_wV_g00 = 2 * alpha3 - alpha1

    gr_match_equations = [
        sp.Eq(gamma, 1),
        sp.Eq(coeff_V, -sp.Rational(7, 2)),
        sp.Eq(coeff_W, -sp.Rational(1, 2)),
        sp.Eq(coeff_wU_g0i, 0),
        sp.Eq(coeff_wUij_g0i, 0),
        sp.Eq(coeff_w2U_g00, 0),
        sp.Eq(coeff_wiwjUij_g00, 0),
        sp.Eq(coeff_wV_g00, 0),
    ]
    solution = sp.solve(
        gr_match_equations,
        [gamma, alpha1, alpha2, alpha3, zeta1],
        dict=True,
    )
    first_solution = solution[0] if solution else {}
    residuals = [
        sp.simplify((eq.lhs - eq.rhs).subs(first_solution))
        for eq in gr_match_equations
    ]

    alpha_zero = (
        first_solution.get(alpha1) == 0
        and first_solution.get(alpha2) == 0
        and first_solution.get(alpha3) == 0
    )
    status = (
        "PASS_STANDARD_PPN_MATCH_FORCES_ALPHA_I_ZERO"
        if alpha_zero and all(value == 0 for value in residuals)
        else "CHECK_STANDARD_PPN_ALPHA_MATCH"
    )

    return {
        "status": status,
        "ppn_vector_coefficients": {
            "V_i": coeff_V,
            "W_i": coeff_W,
            "w_i_U": coeff_wU_g0i,
            "w_j_U_ij": coeff_wUij_g0i,
        },
        "ppn_g00_preferred_frame_coefficients": {
            "w2_U": coeff_w2U_g00,
            "w_i_w_j_U_ij": coeff_wiwjUij_g00,
            "w_i_V_i": coeff_wV_g00,
        },
        "gr_matching_equations": gr_match_equations,
        "solution": solution,
        "residuals_after_solution": residuals,
        "alpha_i_values": {
            "alpha_1": first_solution.get(alpha1),
            "alpha_2": first_solution.get(alpha2),
            "alpha_3": first_solution.get(alpha3),
        },
        "remaining_non_alpha_condition": sp.Eq(zeta1, 2 * xi),
        "closed_here": (
            "standard PPN algebra: GR vector coefficients plus absence of "
            "w-dependent preferred-frame metric terms force alpha_i=0"
        ),
        "not_closed_here": (
            "RG must still derive the moving-source metric coefficients before "
            "this matcher can be promoted to a full PPN pass"
        ),
    }


def moving_source_rg_vector_source_theorem():
    """
    RG-sector vector-source check for the 1.5PN moving-source equation.

    We include both a small inverse-metric vector q_0i=h_i and a small boost
    velocity v_i of the normalized phase-solid background.  The mixed vector
    source is represented by dL/dq_0i.  If its linear coefficients in h_i and
    v_i vanish on the Solar 1PN branch, the RG sector does not add an
    independent vector source to the GR/matter gravitomagnetic equation.
    """
    t, x, y, z = sp.symbols("t x y z", real=True)
    h1, h2, h3 = sp.symbols("h_1 h_2 h_3", real=True)
    vx, vy, vz = sp.symbols("v_x v_y v_z", real=True)
    q00, q11, q22, q33 = sp.symbols("q00 q11 q22 q33", real=True)
    coords = (t, x, y, z)
    h_vars = (h1, h2, h3)
    v_vars = (vx, vy, vz)

    g_inv = sp.Matrix([
        [q00, h1, h2, h3],
        [h1, q11, 0, 0],
        [h2, 0, q22, 0],
        [h3, 0, 0, q33],
    ])

    Phi = t - vx * x - vy * y - vz * z
    phi_fields = (
        x - vx * t,
        y - vy * t,
        z - vz * t,
    )
    d_Phi = [sp.diff(Phi, coord) for coord in coords]
    d_phi = [
        [sp.diff(field, coord) for coord in coords]
        for field in phi_fields
    ]

    Y = sp.simplify(
        sum(g_inv[i, j] * d_Phi[i] * d_Phi[j] for i in range(4) for j in range(4))
    )
    B = sp.zeros(3, 3)
    for A in range(3):
        for B_idx in range(3):
            B[A, B_idx] = sp.simplify(
                sum(
                    -g_inv[i, j] * d_phi[A][i] * d_phi[B_idx][j]
                    for i in range(4)
                    for j in range(4)
                )
            )

    I1 = sp.simplify(B.trace())
    I2 = sp.simplify(sp.Rational(1, 2) * (I1**2 - (B * B).trace()))
    I3 = sp.simplify(B.det())
    L = get_polynomial_lagrangian(Y, I1, I2, I3)

    diagonal_subs = {q00: 1, q11: -1, q22: -1, q33: -1}
    zero_subs = {
        h1: 0,
        h2: 0,
        h3: 0,
        vx: 0,
        vy: 0,
        vz: 0,
    }
    vector_sources = [
        sp.simplify(sp.diff(L, h_var).subs(diagonal_subs))
        for h_var in h_vars
    ]
    h_linear_matrix = [
        [sp.simplify(sp.diff(source, h_var).subs(zero_subs)) for h_var in h_vars]
        for source in vector_sources
    ]
    v_linear_matrix = [
        [sp.simplify(sp.diff(source, v_var).subs(zero_subs)) for v_var in v_vars]
        for source in vector_sources
    ]

    branch = solar_1pn_closure_branch()["branch"]
    h_branch = [
        [sp.simplify(value.subs(branch)) for value in row]
        for row in h_linear_matrix
    ]
    v_branch = [
        [sp.simplify(value.subs(branch)) for value in row]
        for row in v_linear_matrix
    ]
    all_branch_values = [value for row in h_branch + v_branch for value in row]
    status = (
        "PASS_RG_VECTOR_SOURCE_ABSENT_ON_1PN_BRANCH"
        if all(value == 0 for value in all_branch_values)
        else "CHECK_RG_VECTOR_SOURCE_ON_1PN_BRANCH"
    )

    return {
        "status": status,
        "linearized_inverse_metric_vector": {
            "q_01": h1,
            "q_02": h2,
            "q_03": h3,
        },
        "boost_velocity": {
            "v_x": vx,
            "v_y": vy,
            "v_z": vz,
        },
        "mixed_vector_sources_dL_dq0i": vector_sources,
        "h_linear_matrix": h_linear_matrix,
        "v_linear_matrix": v_linear_matrix,
        "h_linear_matrix_on_1PN_branch": h_branch,
        "v_linear_matrix_on_1PN_branch": v_branch,
        "closed_here": (
            "the minimal RG sector adds no linear q_0i source and no linear "
            "boost-velocity vector source on the nontrivial Solar 1PN branch"
        ),
        "not_closed_here": (
            "the Einstein-Hilbert vector Green function and matter velocity "
            "potentials are still represented by the standard one-metric GR "
            "side of the PPN matcher"
        ),
    }


def preferred_frame_alpha_i_closure_chain():
    """
    Combine the RG vector-source checks with the standard PPN matcher.

    The chain is intentionally split into machine-checkable pieces:
    RG background preferred-frame stress, RG vector-source absence, and the
    standard alpha_i algebraic matcher.
    """
    background = preferred_frame_background_stress_theorem()
    vector_source = moving_source_rg_vector_source_theorem()
    matcher = standard_ppn_alpha_i_matcher()

    status = (
        "PASS_MINIMAL_MOVING_SOURCE_ALPHA_I_CHAIN"
        if background["status"] == "PASS_BACKGROUND_PREFERRED_FRAME_STRESS_ON_1PN_BRANCH"
        and vector_source["status"] == "PASS_RG_VECTOR_SOURCE_ABSENT_ON_1PN_BRANCH"
        and matcher["status"] == "PASS_STANDARD_PPN_MATCH_FORCES_ALPHA_I_ZERO"
        else "CHECK_MINIMAL_MOVING_SOURCE_ALPHA_I_CHAIN"
    )

    return {
        "status": status,
        "background_preferred_frame_stress": background["status"],
        "rg_vector_source": vector_source["status"],
        "standard_ppn_matcher": matcher["status"],
        "alpha_i_values": matcher["alpha_i_values"],
        "claim_scope": (
            "minimal one-metric 1.5PN chain: no RG vector/preferred-frame "
            "source on the Solar 1PN branch, so the standard GR vector matcher "
            "forces alpha_1=alpha_2=alpha_3=0"
        ),
        "remaining_for_full_ppn": [
            "write the explicit coordinate/gauge map in final PPN notation",
            "derive the stationary rotating compact-source g_0i solution",
            "keep 2PN q_2PN discriminator separate from alpha_i",
        ],
    }


if __name__ == "__main__":
    delta_n, dt_gen, gamma_sym = calculate_shapiro_delay()
    print("--- Shapiro Time Delay (1PN) ---")
    print("ეფექტური რეფრაქციის დანამატი (Delta n):", delta_n)
    print("ზოგადი 1PN დაყოვნება:", dt_gen)
    print("RG/GR დაყოვნება (gamma = 1 პირობაში):", dt_gen.subs(gamma_sym, 1))
    print("Cassini gate:", cassini_gamma_gate())

    print("\n--- აგენტთა საბჭოს შენიშვნები / მათემატიკური იდენტობა ---")
    print("1. საზღვრების (x1 და -x0) ჩასმისას ვიღებთ: ln(x1 + sqrt(x1^2+b^2)) - ln(-x0 + sqrt(x0^2+b^2))")
    print("2. მნიშვნელი გარდაიქმნება იდენტობით: (-x0 + sqrt(x0^2+b^2)) = b^2 / (x0 + sqrt(x0^2+b^2))")
    print("3. ეს გვაძლევს ფიზიკურად გამჭვირვალე ფორმას: ln[(x1+l1)(x0+l0)/b^2].")
    print("4. gamma=1 პარამეტრი პირობითია; Cassini pass ძალაშია მხოლოდ RG exterior proof-ის შემდეგ.")


# ===================== merged from p03_solar.py =====================

# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

"""
PHASE 14: 2PN Shapiro and light-bending discriminator.

ძველი ISPG Appendix 5/6-ის კანდიდატი discriminator ახალ RG ენაზე:
1PN დონეზე RG და GR ემთხვევა, რადგან gamma=beta=1.
განსხვავება იწყება 2PN რიგში, თუ RG-ის exterior optical index დაიხურა როგორც

    n_RG = exp(2 r_g/r),

ხოლო GR-ის isotropic Schwarzschild optical index არის rational ფორმა:

    n_GR = (1+r_g/(2r))^3/(1-r_g/(2r)).

ამ ansatz-ის closed differential შედეგებია:
    Delta t_2PN^(RG-GR) = (r_g^2/(c b)) * (pi/4),
    Delta theta_RG = 2 r_s/b + pi*r_s^2/b^2 + O(r_s^3/b^3),
    Delta theta_2PN^RG / Delta theta_2PN^GR = 16/15.
"""

import sympy as sp


def calculate_shapiro_2pn_discriminator():
    """
    Candidate RG-GR 2PN Shapiro difference.

    Straight reference path:
        r_0(z)^2 = b^2 + z^2.

    Expansions:
        n_RG = 1 + 2r_g/r + 2r_g^2/r^2 + ...
        n_GR  = 1 + 2r_g/r + (7/4)r_g^2/r^2 + ...

    Shared 1PN bending/path terms cancel in the RG-GR difference, so the
    differential coefficient is controlled by alpha_RG-alpha_GR = 1/4.
    """
    z, b, r_g, c, z_1, z_2 = sp.symbols(
        'z b r_g c z_1 z_2',
        real=True,
        positive=True,
    )
    eps = sp.Symbol('eps', real=True, positive=True)
    r = sp.sqrt(b**2 + z**2)

    n_rg = sp.exp(2 * eps * r_g / r)
    n_gr = (1 + eps * r_g / (2 * r))**3 / (1 - eps * r_g / (2 * r))

    alpha_rg = sp.simplify(
        sp.series(n_rg, eps, 0, 3).coeff(eps, 2) * r**2 / r_g**2
    )
    alpha_gr = sp.simplify(
        sp.series(n_gr, eps, 0, 3).coeff(eps, 2) * r**2 / r_g**2
    )
    delta_alpha = sp.simplify(alpha_rg - alpha_gr)

    master_integral_infinite = sp.integrate(1 / (b**2 + z**2), (z, -sp.oo, sp.oo))
    master_integral_finite = sp.integrate(1 / (b**2 + z**2), (z, -z_1, z_2))
    delta_t_infinite = sp.simplify(delta_alpha * r_g**2 * master_integral_infinite / c)
    delta_t_finite = sp.simplify(delta_alpha * r_g**2 * master_integral_finite / c)
    dimensionless_delta_b = sp.simplify(delta_t_infinite * c * b / r_g**2)

    return {
        "status": "CANDIDATE_2PN_DISCRIMINATOR",
        "input_status": "BLOCKED_UNTIL_RG_EXTERIOR_OPTICAL_INDEX_DERIVED",
        "n_RG": sp.Eq(sp.Symbol('n_RG'), n_rg.subs(eps, 1)),
        "n_GR_isotropic": sp.Eq(sp.Symbol('n_GR'), n_gr.subs(eps, 1)),
        "alpha_RG": alpha_rg,
        "alpha_GR": alpha_gr,
        "delta_alpha": delta_alpha,
        "master_integral_infinite": master_integral_infinite,
        "master_integral_finite": master_integral_finite,
        "Delta_t_2PN_RG_minus_GR": sp.Eq(sp.Symbol('Delta_t'), delta_t_infinite),
        "finite_endpoint_Delta_t": sp.Eq(sp.Symbol('Delta_t_finite'), delta_t_finite),
        "Delta_B": sp.Eq(sp.Symbol('Delta_B'), dimensionless_delta_b),
        "candidate_result": "if n_RG=exp(2*r_g/r), then Delta_B=pi/4",
        "coordinate_warning": (
            "this block is isotropic optical-index language; it must be bridged "
            "to the areal-radius PPN block before theory export"
        ),
    }


def calculate_light_deflection_2pn_discriminator():
    """
    Old Appendix 5 candidate recovered under the exponential optical-index ansatz.

    RG:
        Delta theta = 2 r_s/b + pi r_s^2/b^2 + ...
    GR:
        Delta theta = 2 r_s/b + (15pi/16) r_s^2/b^2 + ...
    """
    b, r_s = sp.symbols('b r_s', real=True, positive=True)

    theta_1pn = 2 * r_s / b
    theta_2pn_rg = sp.pi * r_s**2 / b**2
    theta_2pn_gr = sp.Rational(15, 16) * sp.pi * r_s**2 / b**2
    ratio = sp.simplify(theta_2pn_rg / theta_2pn_gr)
    delta = sp.simplify(theta_2pn_rg - theta_2pn_gr)

    return {
        "status": "CANDIDATE_2PN_BENDING_DISCRIMINATOR",
        "input_status": "HARD_CODED_UNTIL_RAY_EQUATION_DERIVED_FROM_RG_METRIC",
        "theta_1PN_shared": theta_1pn,
        "theta_2PN_RG": theta_2pn_rg,
        "theta_2PN_GR": theta_2pn_gr,
        "theta_total_RG": theta_1pn + theta_2pn_rg,
        "theta_total_GR": theta_1pn + theta_2pn_gr,
        "RG_over_GR_2PN_ratio": ratio,
        "RG_2PN_enhancement_percent": sp.N((ratio - 1) * 100, 8),
        "Delta_theta_2PN_RG_minus_GR": delta,
        "candidate_result": (
            "if the exponential optical-index branch holds, RG has a 16/15 "
            "enhancement of the GR 2PN bending term"
        ),
    }


def isotropic_optical_index_2pn_bridge():
    """
    General 2PN optical-index bridge in isotropic coordinates.

    For a static isotropic metric

        ds^2 = A(r) dt^2 - B(r) (dr^2 + r^2 dOmega^2),
        A = 1 - 2u + 2 beta u^2,
        B = 1 + 2 gamma u + b2 u^2,

    null rays see n=sqrt(B/A). This is the missing bridge between a metric
    calculation and the older optical-index Shapiro/bending candidates.
    """
    u, beta, gamma, b2, q = sp.symbols("u beta gamma b2 q", real=True)

    A = 1 - 2 * u + 2 * beta * u**2
    B = 1 + 2 * gamma * u + b2 * u**2
    n_series = sp.series(sp.sqrt(B / A), u, 0, 3).removeO()
    q_2pn = sp.simplify(sp.expand(n_series).coeff(u, 2))

    gr_q = sp.simplify(q_2pn.subs({gamma: 1, beta: 1, b2: sp.Rational(3, 2)}))
    exp_q = sp.Integer(2)
    b2_for_exp = sp.solve(
        sp.Eq(q_2pn.subs({gamma: 1, beta: 1}), exp_q),
        b2,
        dict=True,
    )

    return {
        "status": "METRIC_TO_OPTICAL_2PN_BRIDGE_DERIVED",
        "metric": {
            "A": A,
            "B": B,
            "u": "GM/(c^2 r_iso)",
        },
        "optical_index": sp.Eq(sp.Symbol("n"), n_series),
        "q_2PN": sp.Eq(q, q_2pn),
        "GR_isotropic": {
            "b2": sp.Rational(3, 2),
            "q_2PN": gr_q,
            "n_GR": "1 + 2u + 7u^2/4 + O(u^3)",
        },
        "exponential_branch": {
            "n_exp": "exp(2u)=1+2u+2u^2+O(u^3)",
            "required_q_2PN": exp_q,
            "required_b2_when_gamma_beta_1": b2_for_exp,
        },
        "reading": (
            "the old n_RG=exp(2u) candidate is equivalent, at 2PN in "
            "isotropic gauge with gamma=beta=1, to requiring b2=2 rather "
            "than the GR value b2=3/2"
        ),
    }


def isotropic_2pn_stress_closure_theorem():
    """
    Direct isotropic-gauge RG stress closure through 2PN.

    This is stronger than the old optical ansatz.  In isotropic coordinates with
    gamma=beta=1, write

        A = 1 - 2u + 2u^2,
        B = 1 + 2u + b2*u^2,
        Y=1/A, I1=3/B, I2=3/B^2, I3=1/B^3.

    Requiring the RG background stress T^t_t and T^i_i to vanish through
    O(u^2) yields either the trivial sector or a nontrivial branch with b2=18.
    That b2 is not GR-like and not the old exponential optical candidate, so
    this is an obstruction for the minimal static isotropic closure.
    """
    u, b2 = sp.symbols("u b2", real=True)
    c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1 = sp.symbols(
        "c_Y c_Y2 c_I1 c_I1sq c_I2 c_I3 c_YI1",
        real=True,
    )
    Y_s, I1_s, I2_s, I3_s = sp.symbols("Y I1 I2 I3", real=True)

    A = 1 - 2 * u + 2 * u**2
    B = 1 + 2 * u + b2 * u**2
    Y = 1 / A
    I1 = 3 / B
    I2 = 3 / B**2
    I3 = 1 / B**3
    L_poly = get_polynomial_lagrangian(Y_s, I1_s, I2_s, I3_s)
    subs = {Y_s: Y, I1_s: I1, I2_s: I2, I3_s: I3}
    L = L_poly.subs(subs)
    L_Y = sp.diff(L_poly, Y_s).subs(subs)
    L_I1 = sp.diff(L_poly, I1_s).subs(subs)
    L_I2 = sp.diff(L_poly, I2_s).subs(subs)
    L_I3 = sp.diff(L_poly, I3_s).subs(subs)

    T_t = sp.simplify(2 * L_Y / A - L)
    T_i = sp.simplify(2 * (L_I1 / B + 2 * L_I2 / B**2 + L_I3 / B**3) - L)
    T_t_series = sp.series(T_t, u, 0, 3).removeO()
    T_i_series = sp.series(T_i, u, 0, 3).removeO()
    t_coeffs = [
        sp.expand(T_t_series).coeff(u, n)
        for n in range(3)
    ]
    i_coeffs = [
        sp.expand(T_i_series).coeff(u, n)
        for n in range(3)
    ]
    equations = t_coeffs + i_coeffs
    leading_equations = t_coeffs[:2] + i_coeffs[:2]

    leading_solutions = sp.solve(
        leading_equations,
        [c_Y, c_I1, c_I1sq, c_I3],
        dict=True,
    )

    full_solutions = sp.solve(
        equations,
        [c_Y, c_Y2, c_I1, c_I1sq, c_I2, c_I3, c_YI1, b2],
        dict=True,
    )
    nontrivial = [
        sol for sol in full_solutions
        if sol.get(b2) == 18
    ]
    trivial = [
        sol for sol in full_solutions
        if sol.get(c_Y, None) == 0
        and sol.get(c_Y2, None) == 0
        and sol.get(c_YI1, None) == 0
    ]
    solution_residuals = [
        [sp.simplify(eq.subs(sol)) for eq in equations]
        for sol in full_solutions
    ]

    q_gamma_beta_1 = b2 / 2 + 1
    q_b2_18 = sp.Rational(18, 2) + 1
    q_gr = sp.Rational(7, 4)
    q_exp = sp.Integer(2)

    return {
        "status": "ISOTROPIC_2PN_STRESS_CLOSURE_OBSTRUCTION",
        "T_t_series": sp.factor(T_t_series),
        "T_i_series": sp.factor(T_i_series),
        "leading_O0O1_solutions": leading_solutions,
        "solutions": full_solutions,
        "solution_residuals": solution_residuals,
        "nontrivial_branch": nontrivial,
        "trivial_branch": trivial,
        "nontrivial_branch_b2": sp.Eq(b2, 18),
        "q_2PN_when_gamma_beta_1": sp.Eq(sp.Symbol("q_2PN"), q_gamma_beta_1),
        "optical_q_on_nontrivial_branch": sp.Eq(sp.Symbol("q_2PN"), q_b2_18),
        "GR_q_2PN": q_gr,
        "exponential_candidate_q_2PN": q_exp,
        "verdict": (
            "in the minimal isotropic unitary-gauge stress closure, the exact "
            "nontrivial 2PN stress-free branch has b2=18, giving q_2PN=10; "
            "the only alternative is the trivial coefficient sector.  Thus the "
            "old b2=2 optical candidate is not derived by this closure."
        ),
        "article_reading": (
            "the Solar 2PN sector is a hard gate: RG must either derive a "
            "different exterior map/screening mechanism, accept the large "
            "b2=18 deviation, or collapse to the trivial sector in this ansatz"
        ),
    }


if __name__ == "__main__":
    print("--- Shapiro Time Delay (2PN): RG-GR candidate discriminator ---")
    shapiro = calculate_shapiro_2pn_discriminator()
    for key, value in shapiro.items():
        print(f"{key:34s}: {value}")

    print("\n--- Light deflection (2PN): exponential optical index ---")
    bending = calculate_light_deflection_2pn_discriminator()
    for key, value in bending.items():
        print(f"{key:34s}: {value}")

    print("\n--- აგენტთა საბჭოს შენიშვნები / ტექნიკური შეზღუდვები ---")
    print("1. 1PN დონეზე RG და GR ემთხვევა: gamma=beta=1.")
    print("2. 2PN Shapiro-ში shared bent-ray/path terms ქრება RG-GR სხვაობაში.")
    print("3. candidate operational discriminator არის Delta_B=pi/4.")
    print("4. 2PN light bending-ში candidate კოეფიციენტი არის 16/15-ჯერ დიდი GR-ის 2PN წევრზე.")
    print("5. theory export დაბლოკილია, სანამ optical index და null geodesics RG metric-იდან არ გამოვა.")


# ===================== merged from p03_solar.py =====================

# Notation header (see NOTATION.md):
# signature (+---); Y = g^mn d_m Phi d_n Phi; B^AB = -g^mn d_m phi^A d_n phi^B.
# T_mn = 2*dL/dg^mn - g_mn*L; off-diagonal symmetric variables use factor 1.
# Horndeski/EFT bridge only: X = -1/2 g^mn d_m Phi d_n Phi, so Y = -2X.

"""
================================================================================
PHASE 30: Lense-Thirring frame dragging — Gravity Probe B
================================================================================

რეფერენცია: p03_solar.py frame-dragging/PPN სამუშაო ბლოკი

დაკვირვება — Gravity Probe B (Everitt et al. 2011):
- gyroscope on satellite, Earth-orbit
- geodetic precession: 6601.8 ± 18.3 mas/yr (GR: 6606.1)
- frame-dragging (Lense-Thirring): 37.2 ± 7.2 mas/yr (GR: 39.2)

GR Lense-Thirring formula:
Ω_LT = (G/c²r³) · [3(S·r̂)r̂ - S]

RG-ის ცდა:
- bi-conformal scalar — gravitomagnetic g_0i sector
- phase8 PPN γ=1: geodetic + leading 1.5PN gravitomagnetic sector is conditional
- preferred-frame/vector-PPN proof remains the tightening task
"""

import math


GP_B = {
    "geodetic_precession_obs": 6601.8,  # mas/yr, Everitt et al. 2011
    "geodetic_precession_err": 18.3,
    "geodetic_GR": 6606.1,  # GR prediction
    "Lense_Thirring_obs": 37.2,  # mas/yr
    "Lense_Thirring_err": 7.2,
    "Lense_Thirring_GR": 39.2,
}


def gr_lense_thirring_formula():
    """GR Lense-Thirring formula summary."""
    return {
        "formula": "Ω_LT = (G/c²r³) · [3(S·r̂)r̂ - S]",
        "Earth_S": "Earth angular momentum I·ω",
        "satellite_orbit": "GP-B 642 km altitude polar orbit",
        "GR_prediction_mas_yr": GP_B["Lense_Thirring_GR"],
    }


def rg_gravitomagnetic_open():
    """RG bi-conformal gravitomagnetic sector — tightening tasks."""
    return [
        "Leading 1.5PN Lense-Thirring is conditional on the one-metric minimal-coupling GR sector.",
        "Full stationary rotating bi-conformal solution should derive the same g_0i coefficient.",
        "BLOCKER: PPN preferred-frame parameters (α_1, α_2, α_3) must be derived as zero.",
        "MOND rotational bridge must remain inert in the Solar System: Z_rot≈a0/g << 1.",
        "LARES/LARES-2/GINGER are observational context only, not RG proof.",
    ]


def lageos_lares_comparison():
    """LAGEOS + LARES — improved frame-dragging measurements."""
    return {
        "status": "OBSERVATIONAL_CONTEXT_NOT_USED_AS_RG_PROOF",
        "LAGEOS_I_II_2011": "reported Lense-Thirring tests; systematics debated",
        "LARES_2016": "reported improved frame-dragging tests; source-tag before export",
        "LARES-2": "targeted/reported high precision; do not use as proof here",
        "GINGER": "Earth-based ring-laser program; future/context only",
    }


def rg_predictions():
    """RG-ის ცდა Lense-Thirring-ისთვის."""
    return {
        "PPN_gamma_1PN": "γ=1 branch — geodetic precession matches GR only after stress gate closes",
        "Lense_Thirring_RG": "leading 1.5PN chain: Ω_LT = GR under the closed vector-source/alpha_i checks",
        "MOND_rotational_slot": "Z_rot≈a0/g, so Solar-System correction is <10^-8 to 10^-11",
        "preferred_frame_PPN": preferred_frame_alpha_i_closure_chain()["status"],
        "current_status": frame_dragging_minimal_1p5pn_chain()["status"],
    }


def frame_dragging_minimal_1p5pn_chain():
    """
    Minimal leading-order RG frame-dragging chain.

    At 1.5PN order, the one-metric Einstein-Hilbert vector operator is the GR
    operator.  The only possible minimal-RG obstruction would be an additional
    RG vector source or preferred-frame vector term.  Those are checked by the
    moving-source vector-source theorem and the alpha_i closure chain.
    """
    G, c, r = sp.symbols("G c r", positive=True)
    S_parallel_term, S_vector = sp.symbols("3S_parallel_rhat S_vector", real=True)
    omega_gr = G * (S_parallel_term - S_vector) / (c**2 * r**3)
    delta_rg_vector_source = sp.Integer(0)
    omega_rg = sp.simplify(omega_gr + delta_rg_vector_source)
    residual = sp.simplify(omega_rg - omega_gr)

    vector_source = moving_source_rg_vector_source_theorem()
    alpha_chain = preferred_frame_alpha_i_closure_chain()

    gp_b_lt_delta = GP_B["Lense_Thirring_obs"] - GP_B["Lense_Thirring_GR"]
    gp_b_lt_sigma = abs(gp_b_lt_delta) / GP_B["Lense_Thirring_err"]
    gp_b_geodetic_delta = GP_B["geodetic_precession_obs"] - GP_B["geodetic_GR"]
    gp_b_geodetic_sigma = abs(gp_b_geodetic_delta) / GP_B["geodetic_precession_err"]

    status = (
        "PASS_MINIMAL_1P5PN_FRAME_DRAGGING_CHAIN"
        if residual == 0
        and vector_source["status"] == "PASS_RG_VECTOR_SOURCE_ABSENT_ON_1PN_BRANCH"
        and alpha_chain["status"] == "PASS_MINIMAL_MOVING_SOURCE_ALPHA_I_CHAIN"
        else "CHECK_MINIMAL_1P5PN_FRAME_DRAGGING_CHAIN"
    )

    return {
        "status": status,
        "Omega_LT_GR": sp.Eq(sp.Symbol("Omega_LT_GR"), omega_gr),
        "Omega_LT_RG_minimal_1p5PN": sp.Eq(sp.Symbol("Omega_LT_RG"), omega_rg),
        "RG_minus_GR_residual": residual,
        "required_subchecks": {
            "moving_source_rg_vector_source": vector_source["status"],
            "preferred_frame_alpha_i_chain": alpha_chain["status"],
        },
        "GP_B_numeric_context": {
            "Lense_Thirring_delta_mas_yr": gp_b_lt_delta,
            "Lense_Thirring_sigma": gp_b_lt_sigma,
            "geodetic_delta_mas_yr": gp_b_geodetic_delta,
            "geodetic_sigma": gp_b_geodetic_sigma,
        },
        "closed_here": (
            "leading 1.5PN Lense-Thirring equals GR in the minimal one-metric "
            "branch because RG contributes no vector source and alpha_i=0"
        ),
        "not_closed_here": (
            "nonperturbative Kerr-like strong-field rotation and high-order "
            "spin corrections remain separate strong-field work"
        ),
    }


def frame_dragging_gate():
    """Strict gate for Solar-System rotating-sector claims."""
    chain = frame_dragging_minimal_1p5pn_chain()
    return {
        "status": chain["status"],
        "GP_B_reference": GP_B,
        "closed_for_leading_1p5PN": [
            "RG vector source absent on the Solar 1PN branch",
            "alpha_1=alpha_2=alpha_3=0 in the minimal moving-source chain",
            "one-metric Einstein-Hilbert vector operator gives the GR Lense-Thirring coefficient",
        ],
        "remaining_beyond_this_gate": [
            "nonperturbative stationary rotating compact-source solution",
            "higher-spin/higher-PN corrections",
            "strong-field rotating black-hole/neutron-star regime",
        ],
        "not_claimed": "strong-field Kerr-like rotating solution",
    }


if __name__ == "__main__":
    print("=" * 72)
    print("PHASE 30: Lense-Thirring frame dragging — Gravity Probe B")
    print("რეფერენცია: Everitt 2011, p03_solar frame-dragging/PPN ბლოკი")
    print("=" * 72)

    print("\n1. დაკვირვება (Gravity Probe B)")
    for key, val in GP_B.items():
        print(f"  {key:30s}: {val}")

    print("\n2. GR Lense-Thirring formula")
    gr = gr_lense_thirring_formula()
    for key, val in gr.items():
        print(f"  {key:25s}: {val}")

    print("\n3. RG-ის გასამკაცრებელი ნაბიჯები")
    for i, task in enumerate(rg_gravitomagnetic_open(), 1):
        print(f"  {i}. {task}")

    print("\n4. LAGEOS/LARES გადახედვა")
    for key, val in lageos_lares_comparison().items():
        print(f"  {key:25s}: {val}")

    print("\n5. RG predictions")
    for key, val in rg_predictions().items():
        print(f"  {key:25s}: {val}")

    print("\n6. სტატუსი")
    print("  - GR L-T 39.2 mas/yr vs GP-B 37.2±7.2 — within 1σ")
    print("  - RG leading 1.5PN frame-dragging is conditional on one-metric minimal coupling.")
    print("  - preferred-frame α_1, α_2, α_3 derivation is a blocker.")
    print("  - gate:", frame_dragging_gate()["status"])


# =============================================================================
# STAGE C1: OLD solar-system precision gate
# =============================================================================

def stage_c1_old_solar_precision_status():
    """Deletion-gate marker for OLD/4--OLD/8."""
    return {
        "OLD_4_PPN": {
            "status": "migrated_as_conditional_geometry_check",
            "target": "p03_solar.py",
            "core": "Schwarzschild-like weak-field geometry gives gamma=1, beta=1 if RG stress constraints close",
        },
        "OLD_5_light_deflection": {
            "status": "migrated_as_candidate_discriminator",
            "target": "p03_solar.py PHASE 14",
            "core": "1PN matches GR if gamma=beta=1; 2PN coefficient is candidate until RG optical index is derived",
        },
        "OLD_6_shapiro": {
            "status": "migrated_as_candidate_discriminator",
            "target": "p03_solar.py PHASE 14",
            "core": "finite RG-GR 2PN differential discriminator Delta_B=pi/4 under exponential optical-index ansatz",
        },
        "OLD_7_perihelion": {
            "status": "migrated_as_conditional_sanity_check",
            "target": "p03_solar.py Mercury block",
            "core": "PPN factor (2+2gamma-beta)/3=1 gives Mercury 42.98 arcsec/century",
        },
        "OLD_8_frame_dragging": {
            "status": "migrated_with_open_tightening",
            "target": "p03_solar.py PHASE 30",
            "core": "leading 1.5PN Lense-Thirring inherited under one-metric minimal coupling",
            "open": "derive preferred-frame/vector PPN alpha_1=alpha_2=alpha_3=0 explicitly",
        },
        "rotational_MOND_bridge": {
            "status": "kept_as_speculative_and_inert_in_solar_system",
            "suppression": "Z_rot approximately a0/g, so Earth/Sun frame-dragging correction is << current sensitivity",
        },
    }


def stage_c1_solar_falsification_targets():
    """What remains observationally useful after the 1PN GR match."""
    return {
        "closed_1PN": [
            "light bending, conditional on gamma=1",
            "Shapiro logarithmic delay, conditional on gamma=1",
            "perihelion precession, conditional on gamma=beta=1",
            "geodetic precession, conditional on gamma=1",
        ],
        "precision_discriminators": [
            "candidate 2PN Shapiro finite differential Delta_B=pi/4",
            "candidate 2PN bending coefficient enhancement 16/15",
            "strong-field lensing/timing near Sgr A*, pulsar-BH systems, ngEHT/BHEX",
        ],
        "theory_tightening": [
            "solve RG weak-field stress constraints through O(U^2)",
            "derive active RG exterior optical index and coordinate bridge",
            "full stationary rotating solution for g_0i",
            "preferred-frame PPN alpha_i proof",
            "nonperturbative null geodesics for compact-object imaging",
        ],
    }


def article_solar_theorem():
    """
    Article-facing weak-field ledger.

    This is the p03 bridge for the first article: it exports the nontrivial
    1PN coefficient branch, its kinetic health condition, and the 2PN residual
    that becomes the next discriminator.
    """
    geometry = ppn_geometry_gate()
    stress = weak_field_stress_constraint_gate()
    one_pn = solar_1pn_closure_branch()
    one_pn_derivation = solar_1pn_branch_derivation_theorem()
    ppn_scope = ppn_scope_and_preferred_frame_gate()
    ansatz_scope = solar_ansatz_scope_table()
    cassini = cassini_gamma_gate()
    q2pn_scale = q2pn_cassini_scale_estimate()
    q2pn_optical_observables = derive_general_q2pn_optical_observables()
    cassini_2pn_proxy = cassini_2pn_tracking_proxy_theorem()
    q2pn_table = q2pn_observational_table()
    cassini_raw_likelihood = cassini_2pn_raw_likelihood_gate()
    preferred_frame_scale = preferred_frame_velocity_risk_estimate()
    preferred_frame_background = preferred_frame_background_stress_theorem()
    alpha_i_matcher = standard_ppn_alpha_i_matcher()
    rg_vector_source = moving_source_rg_vector_source_theorem()
    alpha_i_chain = preferred_frame_alpha_i_closure_chain()
    alpha_i_export = standard_ppn_alpha_i_export_table()
    alpha_i_appendix = preferred_frame_alpha_i_appendix_payload()
    frame_dragging_chain = frame_dragging_minimal_1p5pn_chain()
    shapiro_2pn = calculate_shapiro_2pn_discriminator()
    bending_2pn = calculate_light_deflection_2pn_discriminator()
    optical_bridge = isotropic_optical_index_2pn_bridge()
    isotropic_closure = isotropic_2pn_stress_closure_theorem()

    return {
        "article_use": "1PN Solar-System compatibility branch and 2PN discriminator",
        "geometry_branch": {
            "status": geometry["status"],
            "coordinate_system": geometry["coordinate_system"],
            "residuals_after_geometry_conditions": geometry["residuals_after_geometry_conditions"],
        },
        "nontrivial_1PN_branch": {
            "status": one_pn["status"],
            "derivation_status": one_pn_derivation["status"],
            "branch": one_pn["branch"],
            "free_parameters": one_pn["free_parameters"],
            "phase_no_ghost_prefactor": one_pn["phase_no_ghost_prefactor"],
            "solid_no_ghost_prefactor": one_pn["solid_no_ghost_prefactor"],
            "healthy_window_needed": one_pn["healthy_window_needed"],
            "PPN_values": {
                "gamma": sp.Integer(1),
                "beta": sp.Integer(1),
            },
        },
        "cassini_gate": {
            "status": cassini["status"],
            "gamma_minus_1": cassini["abs_gamma_minus_1"],
            "bound_used": cassini["conservative_bound"],
        },
        "ppn_scope": ppn_scope,
        "solar_ansatz_scope_table": ansatz_scope,
        "preferred_frame_velocity_risk": preferred_frame_scale,
        "preferred_frame_background_stress": preferred_frame_background,
        "standard_ppn_alpha_i_matcher": alpha_i_matcher,
        "moving_source_rg_vector_source": rg_vector_source,
        "preferred_frame_alpha_i_closure_chain": alpha_i_chain,
        "standard_ppn_alpha_i_export_table": alpha_i_export,
        "preferred_frame_alpha_i_appendix_payload": alpha_i_appendix,
        "frame_dragging_minimal_1p5pn_chain": frame_dragging_chain,
        "two_pn_discriminator": {
            "status": "OPEN_DISCRIMINATOR",
            "O2_residual_on_1PN_branch": one_pn["O2_residual_on_this_branch"],
            "derived_O2_residual_check": one_pn_derivation["O2_expected_residual_check"],
            "exact_2PN_stress_free_solution_on_branch": (
                one_pn_derivation["exact_2PN_stress_free_solution_on_branch"]
            ),
            "strict_stress_free_solution": stress["strict_O0_O1_O2_solution"],
            "isotropic_2pn_stress_closure": {
                "status": isotropic_closure["status"],
                "leading_O0O1_solutions": isotropic_closure[
                    "leading_O0O1_solutions"
                ],
                "solutions": isotropic_closure["solutions"],
                "solution_residuals": isotropic_closure["solution_residuals"],
                "nontrivial_branch_b2": isotropic_closure[
                    "nontrivial_branch_b2"
                ],
                "optical_q_on_nontrivial_branch": isotropic_closure[
                    "optical_q_on_nontrivial_branch"
                ],
                "GR_q_2PN": isotropic_closure["GR_q_2PN"],
                "exponential_candidate_q_2PN": isotropic_closure[
                    "exponential_candidate_q_2PN"
                ],
                "article_reading": isotropic_closure["article_reading"],
            },
            "q2pn_observational_scale": q2pn_scale,
            "q2pn_general_optical_observables": q2pn_optical_observables,
            "cassini_2pn_tracking_proxy": cassini_2pn_proxy,
            "q2pn_observational_table": q2pn_table,
            "cassini_2pn_raw_likelihood_gate": cassini_raw_likelihood,
            "reading": (
                "Exact GR-like 2PN stress-free closure sends c_Y2=c_YI1=0 "
                "on the nontrivial 1PN branch; the nonzero O(U^2) residual is "
                "the solar-sector discriminator."
            ),
        },
        "two_pn_observable_candidates": {
            "status": "CONDITIONAL_CANDIDATES_NOT_FINAL_PREDICTIONS",
            "metric_to_optical_bridge": optical_bridge,
            "shapiro": {
                "status": shapiro_2pn["status"],
                "input_status": shapiro_2pn["input_status"],
                "n_RG": shapiro_2pn["n_RG"],
                "n_GR_isotropic": shapiro_2pn["n_GR_isotropic"],
                "delta_alpha": shapiro_2pn["delta_alpha"],
                "Delta_t_2PN_RG_minus_GR": shapiro_2pn[
                    "Delta_t_2PN_RG_minus_GR"
                ],
                "finite_endpoint_Delta_t": shapiro_2pn["finite_endpoint_Delta_t"],
                "Delta_B": shapiro_2pn["Delta_B"],
            },
            "light_bending": {
                "status": bending_2pn["status"],
                "input_status": bending_2pn["input_status"],
                "theta_2PN_RG": bending_2pn["theta_2PN_RG"],
                "theta_2PN_GR": bending_2pn["theta_2PN_GR"],
                "RG_over_GR_2PN_ratio": bending_2pn[
                    "RG_over_GR_2PN_ratio"
                ],
                "Delta_theta_2PN_RG_minus_GR": bending_2pn[
                    "Delta_theta_2PN_RG_minus_GR"
                ],
            },
            "blocking_condition": (
                "promote to final prediction only after n_RG is derived from "
                "the RG exterior metric and the areal-radius branch is mapped "
                "to isotropic PPN coordinates"
            ),
        },
        "article_status": {
            "one_pn": "CLOSED_COEFFICIENT_BRANCH",
            "full_ppn": ppn_scope["status"],
            "cassini_if_gamma_derived": cassini["status"],
            "solar_ansatz_scope_table": ansatz_scope["status"],
            "two_pn": "OPEN_DISCRIMINATOR",
            "two_pn_observational_scale": q2pn_scale["status"],
            "general_q2pn_optical_observables": q2pn_optical_observables["status"],
            "cassini_2pn_tracking_proxy": cassini_2pn_proxy["status"],
            "q2pn_observational_table": q2pn_table["status"],
            "cassini_2pn_raw_likelihood_gate": cassini_raw_likelihood["status"],
            "isotropic_2pn_closure": isotropic_closure["status"],
            "two_pn_observable_candidates": (
                "CONDITIONAL_CANDIDATES_NOT_FINAL_PREDICTIONS"
            ),
            "preferred_frame_velocity_risk": preferred_frame_scale["status"],
            "preferred_frame_background_stress": preferred_frame_background["status"],
            "standard_ppn_alpha_i_matcher": alpha_i_matcher["status"],
            "moving_source_rg_vector_source": rg_vector_source["status"],
            "preferred_frame_alpha_i_closure_chain": alpha_i_chain["status"],
            "standard_ppn_alpha_i_export_table": alpha_i_export["status"],
            "preferred_frame_alpha_i_appendix_payload": alpha_i_appendix["status"],
            "rotating_sources": frame_dragging_chain["status"],
        },
    }


def solar_system_claim_gate():
    """Top-level status ledger for p03."""
    stress_gate = weak_field_stress_constraint_gate()
    one_pn_branch = solar_1pn_closure_branch()
    return {
        "file_export_status": "NOT_READY_FOR_RG_THEORY_EXPORT",
        "ppn_geometry": ppn_geometry_gate()["status"],
        "rg_stress_constraints": stress_gate["status"],
        "solar_1PN_closure_branch": one_pn_branch["status"],
        "strict_2PN_stress_free_branch": (
            "TRIVIAL_ONLY" if stress_gate["strict_O0_O1_O2_solution"] else "CHECK"
        ),
        "mercury": mercury_precession_gate()["status"],
        "cassini_shapiro_1PN": cassini_gamma_gate()["status"],
        "q2pn_cassini_scale": q2pn_cassini_scale_estimate()["status"],
        "general_q2pn_optical_observables": (
            derive_general_q2pn_optical_observables()["status"]
        ),
        "cassini_2pn_tracking_proxy": cassini_2pn_tracking_proxy_theorem()["status"],
        "shapiro_2PN": calculate_shapiro_2pn_discriminator()["status"],
        "light_bending_2PN": calculate_light_deflection_2pn_discriminator()["status"],
        "frame_dragging": frame_dragging_gate()["status"],
        "preferred_frame": preferred_frame_velocity_risk_estimate()["status"],
        "preferred_frame_background_stress": (
            preferred_frame_background_stress_theorem()["status"]
        ),
        "standard_ppn_alpha_i_matcher": standard_ppn_alpha_i_matcher()["status"],
        "moving_source_rg_vector_source": moving_source_rg_vector_source_theorem()[
            "status"
        ],
        "preferred_frame_alpha_i_closure_chain": (
            preferred_frame_alpha_i_closure_chain()["status"]
        ),
        "frame_dragging_minimal_1p5pn_chain": (
            frame_dragging_minimal_1p5pn_chain()["status"]
        ),
        "do_not_claim": [
            "do not claim full Solar-System pass",
            "do not claim exact GR-like 2PN stress-free exterior for nonzero coefficients",
            "do not claim 2PN Delta_B=pi/4 as final until optical index is derived",
            "do not claim frame-dragging pass before rotating solution and alpha_i=0",
        ],
    }


if __name__ == "__main__":
    print("\n" + "=" * 72)
    print("p03 top-level claim gate")
    print("=" * 72)
    for key, value in solar_system_claim_gate().items():
        print(f"{key}: {value}")

