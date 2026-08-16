# W3-29: The Pressure, Ruler, and Light Gates (Analytical Formulation)

## 1. The Pressure Gate (Physical Derivation)
**Current Status:** OPEN (Algebraic Identity Passed)

In W3-28, we established the algebraic identity:
$$ P(\tau) = P_{\rm ref} e^{-2\tau/T_0} \implies \frac{dP}{d\tau} = -\frac{2P}{T_0} $$
This was derived simply by asserting $\tau = T_0 \ln(t/T_0)$ and $P/P_{\rm ref} = (T_0/t)^2$. 

**The Challenge:**
To close the Pressure Gate, this relationship must be derived directly from the fundamental RefG field equations. 
If the RefG stress-energy tensor or field equation dictates a relaxation of the background state where the pressure drops exponentially with internal processual time, then $dP/d\tau = -2P/T_0$ is not just a kinematic identity, but the true dynamic law of the universe.

## 2. The Ruler Gate (The $A = a/p$ Conflict)
**Current Status:** OPEN (Major Theoretical Conflict)

The core intuition of RefG posits a "stationary" background where the space itself does not expand, but the standard quantum rulers ($p$) shrink.
Mathematically, the observable scale factor $A$ is:
$$ A = \frac{a}{p} $$
where $p = \Omega = T_0 / t$.

In W3-28, we used the $\Lambda$CDM metric time $t(A)$ to map observations. However, this creates a profound contradiction:
$$ a(A) = A \cdot p(A) = A \frac{T_0}{t(A)} $$

During the matter-dominated era, $t(A) \propto A^{3/2}$. Therefore:
$$ a(A) \propto A \cdot A^{-3/2} = A^{-1/2} $$
During the radiation-dominated era, $t(A) \propto A^2$. Therefore:
$$ a(A) \propto A \cdot A^{-2} = A^{-1} $$

**The Problem:** $a(A)$ is not constant. The background space $a$ is actually contracting if we enforce this mapping onto standard $\Lambda$CDM time evolution.

**The Solution Path:**
If we strictly enforce $a = \text{constant}$ (stationary universe), then:
$$ p(A) = \frac{a}{A} \implies p(A) \propto A^{-1} $$
If $p = \Omega = T_0/t$, this means $t(A) \propto A$. 
But if $t(A) \propto A$, then $H_t(A) = \frac{1}{A} \frac{dA}{dt} \propto A^{-1}$, which does not match the observed expansion history (matter $H_t \propto A^{-3/2}$).

*We must theoretically resolve this: Does the background actually contract? Is $\Omega$ not strictly $p$? Or is the definition of $t(A)$ different?*

## 3. The Light Gate ($p^2$ Channel)
**Current Status:** OPEN

RefG dictates that light propagation is affected by the $p^2$ shrinking factor.
$$ \frac{c_{\rm coord}}{c_0} = p^2 $$
We must formally derive the observable consequences of this without double-counting the scale factor $A$:
1. **Spectral Redshift:** Does $p^2$ fully account for the $1+z$ observed in spectra?
2. **Time Dilation:** Supernova light curves stretch by $1+z$. How does $p^2$ map to $\Delta t_{\rm obs} = (1+z)\Delta t_{\rm emit}$?
3. **Luminosity Distance:** Derive $D_L(z)$ using $p^2$ geometry and compare it to the Pantheon standard.

## Next Steps
This document outlines the strict analytical requirements. We need physical postulates from the core RefG theory (action principle or field equations) to solve the $a(A)$ conflict and the $dP/d\tau$ derivation.
