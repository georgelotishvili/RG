# Preregistration: W3-30 True Stationary Branch

## 1. Hypothesis / Goal
To analytically derive the observable cosmological map (Redshift, Distances, Time Dilation, BAO) from the strict axioms of the RefG True Stationary Branch, where the background space is unexpanding ($a=\text{const}$) and the standard quantum rulers shrink ($p=\Omega=T_0/t$).

## 2. Unalterable Foundation (Axioms)
1. **Stationary Background:** $a = 1$.
2. **Shrinking Rulers:** $p = \Omega = T_0 / t$.
3. **Observable Scale Factor:** $A = a / p \implies A = 1/p = t/T_0$.
4. **Coordinate Light Speed:** $c_{\rm coord} = c_0 p^2$.

## 3. Derivation Goals (The Gates)
We will formally derive the following observables to see what this specific branch predicts:
1. **Gate 1: Spectral Redshift $z_{\rm spec}(A)$.** 
   - Does a photon emitted at time $t_e$ with wavelength $\lambda_e$ arrive at $t_0$ with $\lambda_0 = \lambda_e / A(t_e)$?
2. **Gate 2: Cosmic Chronometers $H_{\rm CC}(z)$.** 
   - What is the expected $H(z)$ measured by physical clocks?
3. **Gate 3: Distances ($D_M, D_L$).** 
   - Derive the comoving distance $D_M = \int c_{\rm coord} dt$ in terms of observable $z$.
4. **Gate 4: SN Time Dilation.** 
   - Does a process taking $\Delta \tau$ internally appear stretched by $(1+z)$ to us?
5. **Gate 5: Alcock-Paczyński (BAO).** 
   - Derive the geometric parameter $F_{\rm AP} = D_M H / c$.

## 4. Execution Plan
1. Create `w3_30_stationary_branch.py` to analytically compute and numerically plot these predicted observables against standard $\Lambda$CDM.
2. Output a structured JSON `w3_30_observables.json` containing the exact mathematical slopes and relations.
3. Determine if the strict stationary branch natively recovers $D_M \propto z$ and $F_{\rm AP} \propto z$, which would constitute strong falsifiable predictions.
