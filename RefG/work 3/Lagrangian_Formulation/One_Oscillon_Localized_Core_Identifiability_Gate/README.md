# W3-57 One-Oscillon Localized-Core Identifiability Gate

W3-57 tests whether the active W3-50/W3-54 phase-current action already
contains enough physics to derive one localized oscillon core, its stability
operator, and the W3-56 pressure/cadence scaling. The answer on the registered
branch is exact and negative.

The exact bounded result is

```text
PASS_EXACT_FIXED_COFRAME_STATIONARY_SPHERICAL_PHASE_LOCKED_ZERO_FLUX_STRICT_CONVEX_INTRINSIC_CORE_NO_GO_AND_EOS_NONIDENTIFIABILITY__TIME_DEPENDENT_CORE_OPERATOR_FLOQUET_SPECTRUM_AND_BACKGROUND_SCALING_OPEN
```

On a fixed non-backreacting Minkowski coframe with an infinite asymptotically
homogeneous radial domain, the stationary spherical globally phase-locked
branch makes `r^2 n_C u^r` constant. Regularity at the centre and zero flux
at infinity set that constant to zero. The phase equation then gives
`rho_C'(n_C(r))=Omega`. On every strict-convex healthy branch
`rho_C''>0`, this forces `n_C` to be spatially constant. Matching the
background therefore leaves no nontrivial intrinsic core on this branch. If
`rho_C'` is constant throughout a nonzero density interval, equivalently the
equation of state is affine there, the profile is algebraically degenerate
and the action supplies no surface stiffness or localization scale.

On an infinite homogeneous fixed background, the longitudinal phase-current
plane-wave branch is gapless acoustic, with
`c_s^2=n_C rho_C''/rho_C'`. Two equally admissible equations of state,
`rho_C=kappa n_C^(4/3)` and `rho_C=kappa n_C^2`, give different sound cones
and different pressure powers while preserving the same W3-50 charge law.
Thus the free equation of state cannot identify a core or its spectrum.

The audit also closes two tempting shortcuts. First, if the collective phase
rate is conditionally identified with the desired common cadence, it implies
`p_C proportional to n_C^(3/2)`, not `n_C`. Conversely, exact
`p_C proportional to n_C` selects a logarithmic equation of state; it is not
forced by the action and cannot satisfy the declared global healthy branch
over all positive density. Second, the full displayed W3-56 auxiliary
response potential and its density derivative vanish on its algebraic
equilibrium. Its separately selected `K b^2/2` channel is therefore not
derived or identifiable as a Hilbert stress from that reduced model.

This is not a theorem against every future oscillon. It proves that the
current one-potential bulk sector does not uniquely derive the requested
intrinsic core. The minimum missing class of physical input is a
coframe-coupled localized-core constitutive action containing its
dispersive/amplitude-gradient response, bounded binding nonlinearity,
ordinary oscillon phase distinct from the
collective phase, and an action-derived stress projection. Only after that
action is obtained is there an honest radial/PDE and Floquet problem to
solve.

Run:

```powershell
python w3_57_one_oscillon_localized_core_identifiability.py
```

The package stops at this exact gate. It does not select a potential, solve a
particle catalogue, use Koide/C3, enter the Planck hierarchy, alter
cosmology, or edit the intuitive manuscripts.
