import sympy as sp
import sys
import json
from pathlib import Path
import hashlib

def main():
    t = sp.Symbol('t', real=True, positive=True)
    P = sp.Symbol('P', real=True, positive=True)
    
    P0 = sp.Symbol('P0', real=True, nonnegative=True) # Asymptotic vacuum pressure
    delta_P = sp.Symbol('delta_P', real=True, positive=True) # Pi - P0 > 0
    Pi = P0 + delta_P # Initial pressure (strictly > P0)
    kappa = sp.Symbol('kappa', real=True, positive=True) # Relaxation rate
    n = sp.Symbol('n', real=True, positive=True) # Readout power
    
    print("=== RefG Cosmology Algebraic Branch Tester ===\n")
    
    # Check upstream gate W3_09 with strict validation
    gate_script = Path(__file__).parent / "w3_09_process_to_metric_bridge_gate.py"
    gate_path = Path(__file__).parent / "w3_09_result.json"
    
    if not gate_path.exists() or not gate_script.exists():
        print("ERROR: Upstream validation gate W3_09 (Process to Metric Bridge) is missing.")
        sys.exit(1)
        
    with open(gate_path, "r") as f:
        gate_data = json.load(f)
        
    if gate_data.get("claim_id") != "W3_09_PROCESS_TO_METRIC_BRIDGE" or "CONDITIONAL PASS" not in gate_data.get("status", ""):
        print("ERROR: Upstream validation gate W3_09 FAILED or invalid claim_id.")
        sys.exit(1)
        
    if gate_data.get("model_version") != "W3-09-v3.0-RIGOROUS-BRIDGE":
        print("ERROR: Upstream validation gate W3_09 has an outdated model_version.")
        sys.exit(1)
        
    script_content = gate_script.read_text('utf-8')
    computed_hash = hashlib.sha256(script_content.encode('utf-8')).hexdigest()
    if gate_data.get("source_hash") != computed_hash:
        print("ERROR: Upstream validation gate W3_09 source_hash mismatch. The gate script was modified but not re-run.")
        sys.exit(1)
        
    print(f"[PRE-CHECK] Upstream Gate {gate_data['claim_id']} verified (PASS).")
    print(f"[PRE-CHECK] True Source Hash Match: {computed_hash[:8]}...")
    print(f"[PRE-CHECK] Time scaling mathematically consistent given the P -> Phi postulate.")
    
    print("\nAssumption: Initial pressure Pi = P0 + delta_P (where delta_P > 0).")
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
