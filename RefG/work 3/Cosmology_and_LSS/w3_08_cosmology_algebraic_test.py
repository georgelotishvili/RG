import sympy as sp
import sys

def main():
    t = sp.Symbol('t', real=True, positive=True)
    P = sp.Symbol('P', real=True, positive=True)
    
    P0 = sp.Symbol('P0', real=True, nonnegative=True) # Asymptotic vacuum pressure
    delta_P = sp.Symbol('delta_P', real=True, positive=True) # Pi - P0 > 0
    Pi = P0 + delta_P # Initial pressure (strictly > P0)
    kappa = sp.Symbol('kappa', real=True, positive=True) # Relaxation rate
    n = sp.Symbol('n', real=True, positive=True) # Readout power
    
    print("=== RefG Cosmology Algebraic Branch Tester ===\n")
    print("Assumption: Initial pressure Pi = P0 + delta_P (where delta_P > 0).")
    print("Codex Hypothesis check: If P -> P0 > 0, the universe eventually decelerates to a halt.")
    
    # 1. Exponential Decay to P0 > 0
    # P(t) decays from Pi to P0
    P_exp_P0 = P0 + delta_P * sp.exp(-kappa * t)
    a_pow = (Pi / P)**n
    a_t_P0 = a_pow.subs(P, P_exp_P0)
    
    H_t_P0 = sp.simplify(sp.diff(a_t_P0, t) / a_t_P0)
    q_t_P0 = sp.simplify(- (a_t_P0 * sp.diff(a_t_P0, t, 2)) / (sp.diff(a_t_P0, t)**2))
    
    print("BRANCH 1: P(t) decays exponentially to P0 > 0")
    print(f"a(t) = {a_t_P0}")
    print(f"H(t) = {H_t_P0}")
    print(f"q(t) = {q_t_P0}")
    print("Note: As t -> oo, exp(kappa*t) dominates numerator of q(t). Since Pi > P0, q(t) -> +oo.")
    print("Conclusion: Universe decelerates and stops at a_max = (Pi/P0)^n. Fails late-time acceleration.\n")
    
    # 2. Exponential Decay to P0 = 0
    P_exp_0 = Pi * sp.exp(-kappa * t)
    a_t_0 = a_pow.subs(P, P_exp_0)
    H_t_0 = sp.simplify(sp.diff(a_t_0, t) / a_t_0)
    q_t_0 = sp.simplify(- (a_t_0 * sp.diff(a_t_0, t, 2)) / (sp.diff(a_t_0, t)**2))
    
    print("BRANCH 2: P(t) decays exponentially to P0 = 0 (Total Vacuum Relaxation)")
    print(f"a(t) = {a_t_0}")
    print(f"H(t) = {H_t_0}")
    print(f"q(t) = {q_t_0}")
    print("Conclusion: Pure de Sitter expansion (H = const, q = -1). Yields exact de Sitter kinematics.\n")

    # 3. Adding Matter to the P0=0 case
    # If dot_P = -kappa * P - kappa_m * rho_m
    # In terms of scale factor, rho_m ~ 1/a^3 ~ P^(3n)
    # This leads to a coupled differential equation.
    print("NEXT STEP: Add matter density rho_m ~ a^{-3} to the relaxation differential equation to get the transition from q=0.5 (matter) to q=-1 (vacuum).")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    main()
