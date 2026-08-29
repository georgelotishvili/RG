# CMB Closure

This package develops the cosmic-microwave-background sector as a direct
continuation of Einstein gravity. The operational metric and its field
equation retain the Einstein--Hilbert/TEGR geometry selected in Work 3. RefG
adds the foundation origin, physical interpretation, and covariant dynamics
of the sources on the right-hand side.

W3-62 fixes the operational/foundation density dictionary, closes the
once-only CMB source ledger, and derives the linear scalar behavior of the
conserved collective phase source. W3-63 then carries that source into the
standard Einstein--Boltzmann background, perturbation, collision,
recombination, and line-of-sight equations.

## Files

- `w3_62_cmb_einstein_source_linear_closure_preregistration.md`
- `w3_62_cmb_einstein_source_linear_closure.py`
- `w3_62_result.json`
- `w3_62_result.sha256`
- `w3_63_einstein_boltzmann_cmb_handoff_contract.md`
- `w3_63_einstein_boltzmann_cmb_handoff.py`
- `w3_63_result.json`
- `w3_63_result.sha256`

## Stopping rule

Stop when the RefG source registry has reached the standard
Einstein--Boltzmann--recombination system and its formal line-of-sight
endpoint. The established CMB calculation continues from that point.
Boltzmann-code execution, numerical spectra, likelihoods, and data inference
are outside this package.
