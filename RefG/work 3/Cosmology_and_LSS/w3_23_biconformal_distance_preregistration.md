# W3_23 Preregistration: Biconformal Distance and Observational Provenance

## 1. Hypothesis & Rationale
In W3_22, the distance integral for supernovae was improperly computed using the metric expansion rate $H_t(z)$ without accounting for the biconformal scaling factor $p$. According to the biconformal metric definition in RefG, the correct comoving distance is evaluated with respect to the structural Hubble rate:
$d_C \propto \int \frac{dz}{H_\tau}$

This preregistration defines the W3_23 execution, which corrects this integral. We expect the CC fit to remain identical to W3_22 ($H_\tau$ successfully fits CC), while the SN tension will revert to its original magnitude from W3_20 ($\Delta \chi^2 \approx 27.7$). 

## 2. Mathematical Map
1. **Structural Rate:** $H_\tau(z) = K + B(1+z)^{1.5}$
2. **Metric Rate:** $H_t(z) = \Omega(z) H_\tau(z)$
3. **Luminosity Distance (Biconformal):** 
   $$ D_L(z) = (1+z) \int_0^z \frac{dz'}{H_\tau(z')} $$
   *(This implicitly includes the $p$ factor as $d_C = \int \frac{p dz}{H_t} = \int \frac{dz}{H_\tau}$)*

## 3. Data & Observational Targets
- **Cosmic Chronometers (CC):** Will be fitted against $H_\tau(z)$ directly.
- **Pantheon SNe:** Will be tested using the biconformal $D_L(z)$.
- **JWST:** A theoretical interval ($z=10 \to 5$) will be calculated to demonstrate the $\tau / t \approx 2.4$ ratio, but the actual physical constraint of JWST galaxy maturity is declared strictly **OPEN** for a future dedicated test incorporating $\Gamma_{\rm struct}$.

## 4. Deliverables
- `w3_23_biconformal_distance.py` (Script)
- `w3_23_result.json` (Numerical Output)
- Verification that $\Delta \chi^2 \approx 27.7$ on Pantheon.
