# Work 3 Cosmology and LSS Ledger

## Current account

W3-36 is the current bookkeeping root for the cosmology branch:

- cosmic history has a finite origin;
- process time is elapsed time, tau(t)=int_0^t p(s) ds;
- foundation expansion and material-ruler evolution remain distinct;
- the operational scale is A=a/p, so a may increase while p decreases;
- neither a(t) nor p(t) is fitted or postulated by W3-36;
- foundation pressure P_F and thermodynamic pressure P_th are independent
  until an equation of state or transfer law is derived;
- global birth is a homogeneous temporal event; a local activation threshold
  is not the universe's outer edge.

w3_36_result.json passes only the exact dictionary, integrability,
threshold, conservation, and thermal-identifiability checks. The physical
dynamics, numerical process age, temperature history, redshift map,
H_CC(z), D_L(z), CMB/BBN calculation, and JWST growth model remain open.

One exact thermal result is already decisive for future work. On the
adiabatic radiation branch, Q_gamma=0 gives T A=constant; with the
conditional map 1+z=A0/Ae, this is the standard T_e=T_today(1+z) law.
Faster cadence alone cannot produce a lower temperature. A different
temperature requires a derived source history, equation of state, or
non-universal sector response.

## Salvaged exact results

W3-36 checks the useful metric, process-time, null-ray, radius, and volume
identities inside one self-contained symbolic artifact.

It also preserves a conditional-front assumption-consequence check. Under
the hypothetical constant-energy, spherical-volume, same-null-front closure,
define q=d ln a/d ln P_F and D=1+3q:

- D dR/dt=c0 p^2;
- d tau/dR=D/(c0 p);
- for 0<D<1 and p>=1, 0<Delta tau<R_final/c0;
- only the constant-D=D0>0, constant-q sub-branch has p proportional to
  t^(-3/8) and elapsed process time 8 T0/5.

This calculation is a conditional consistency benchmark. Its closure has not
been derived, and its local radial front is not the global birth geometry.
The source snapshots were removed after these valid results were made
self-contained in W3-36.

## Retired branch evidence

The superseded exploratory branches were removed from the active tree. They
encoded a superseded total-age postulate, an unresolved ruler note, a
stationary a=1 branch, an exploratory observational test, a superseded
requirements draft, and an arbitrary power-law fit. None is an input to
W3-36.

The strongest negative result from the strict stationary branch is preserved
here as an archival audit record, not as a reproducible gate. The removed
exploratory source/result were not provenance-complete, and W3-36 does not
depend on these numbers. Conditional on that branch's luminosity-distance
map, the 40-bin Pantheon comparison with the full supplied covariance gave:

- chi2_STB=401.0154718937386;
- chi2_LCDM=40.021348345228716;
- Delta_chi2=360.9941235485099;
- p_STB=1.2851783751590529e-61;
- 39 degrees of freedom.

For the branch's correctly transformed physical-clock chronometer
prediction, a fixed constant H_CC=1/T0 gave:

- chi2_STB=182.4119037277066;
- chi2_LCDM=14.872777476363384;
- p_STB=9.142349049942303e-24;
- 30 degrees of freedom.

These numbers reject the strict stationary observable map, not RefG as a
whole. Future derivations must not silently reduce to a=1, H_CC=constant,
or D_L proportional to z(1+z).

## Retained data

lcparam_DS17f.txt and sys_DS17f.txt are retained as the canonical local
Pantheon inputs for a future preregistered observable test. They do not
constitute a current RefG fit.
