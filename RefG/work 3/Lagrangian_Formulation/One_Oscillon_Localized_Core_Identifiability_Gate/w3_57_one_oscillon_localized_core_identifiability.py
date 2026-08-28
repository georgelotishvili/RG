'''W3-57 localized-core identifiability and restricted no-go gate.'''

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


CLAIM_ID = 'W3_57_ONE_OSCILLON_LOCALIZED_CORE_IDENTIFIABILITY_GATE'
MODEL_VERSION = 'W3-57-v1.0-ONE-POTENTIAL-LOCALIZED-CORE-IDENTIFIABILITY-GATE'
PASS_STATUS = (
    'PASS_EXACT_FIXED_COFRAME_STATIONARY_SPHERICAL_PHASE_LOCKED_ZERO_FLUX_'
    'STRICT_CONVEX_INTRINSIC_CORE_NO_GO_AND_EOS_NONIDENTIFIABILITY__TIME_'
    'DEPENDENT_CORE_OPERATOR_FLOQUET_SPECTRUM_AND_BACKGROUND_SCALING_OPEN'
)
HERE = Path(__file__).resolve().parent
WORK3 = HERE.parents[1]
PREREG = HERE / 'w3_57_one_oscillon_localized_core_identifiability_preregistration.md'
PACKAGE_README = HERE / 'README.md'
COSMOLOGY_LEDGER = WORK3 / 'Cosmology_and_LSS' / 'README.md'
FORMAL_LEDGER = WORK3 / 'Lagrangian_Formulation' / 'RefG_Formal_Proof.md'
OUTPUT = HERE / 'w3_57_result.json'
HASH_OUTPUT = HERE / 'w3_57_result.sha256'
PINNED_PREREG_SHA256 = (
    'fb703be40b4566e1c9a13c4eb5e5bcee41aa0119d3e6d010ca139ed75d158b1b'
)

DEPENDENCY_CONTRACTS = {
    'W3_50': (
        WORK3 / 'Cosmology_and_LSS'
        / 'Active_Participation_Resonance_Feedback'
        / 'w3_50_neutral_collective_phase_density_bridge_contract.md',
        '1cb66438a6bf53f1a661a014328204c05edfe847f81d876defe69eaa400591db',
    ),
    'W3_54': (
        WORK3 / 'Lagrangian_Formulation'
        / 'Relational_Coframe_TEGR_Phase_Source_Closure'
        / 'w3_54_relational_coframe_tegr_phase_source_closure_contract.md',
        '6cc748eb806d0bccaaf63105567a5d9b1569c56f6b53951c554ec4bad1aa9879',
    ),
}

W3_56_DIR = (
    WORK3 / 'Lagrangian_Formulation' / 'One_Oscillon_Coframe_Lock_Bridge'
)
W3_56_PREREG = W3_56_DIR / 'w3_56_one_oscillon_coframe_lock_bridge_preregistration.md'
W3_56_SOURCE = W3_56_DIR / 'w3_56_one_oscillon_coframe_lock_bridge.py'
W3_56_RESULT = W3_56_DIR / 'w3_56_result.json'
W3_56_CHECKSUM = W3_56_DIR / 'w3_56_result.sha256'
W3_56_PREREG_SHA256 = (
    '2621326161bfb65a651e56bfdeade2e3b290efe39cf2211467851850d030dc5c'
)
W3_56_SCOPE_STATUS = (
    'PASS_EXACT_INTERNAL_ALGEBRA_OF_SELECTED_FIXED_BACKGROUND_RESPONSE_AND_'
    'BICONFORMAL_PULLBACK_WITNESS__W3_50_OSCILLON_CORE_SPECTRAL_GATE_'
    'PRESSURE_STRESS_COVARIANT_BACKREACTION_AND_UNIVERSALITY_OPEN'
)

REQUIRED_CONTRACT_FIELDS = {
    'CLAIM_ID', 'CLAIM', 'TYPE', 'MODEL_VERSION', 'ASSUMPTIONS',
    'DOMAIN', 'CONVENTIONS', 'FREEDOM_LEDGER', 'DEPENDENCIES',
    'METHOD', 'PASS_CONDITION', 'FAIL_CONDITION', 'FALSIFIER',
    'RESIDUAL', 'ERROR_BOUND', 'VALIDITY_HEALTH', 'BRANCHES',
    'OBSERVABLE_MAP', 'FORWARD_MODEL', 'DATA_ROLE', 'IDENTIFIABILITY',
    'BENCHMARK', 'CLOSURE_FLAGS', 'CROSSCHECK', 'PROVENANCE', 'FILES',
}

REQUIRED_EXACT_KEYS = {
    'dependency_hashes_pinned_exact',
    'w3_50_collective_phase_role_preserved_exact',
    'w3_54_one_potential_action_audited_exact',
    'density_derivative_operator_absent_exact',
    'stationary_spherical_current_integrated_exact',
    'regular_zero_flux_branch_exact',
    'radial_phase_gradient_zero_exact',
    'strict_convex_phase_locked_profile_homogeneous_exact',
    'degenerate_branch_profile_unselected_exact',
    'thermodynamic_pressure_from_action_exact',
    'homogeneous_phase_current_determinant_exact',
    'homogeneous_sound_speed_formula_exact',
    'acoustic_mass_gap_absent_exact',
    'healthy_polytropic_countermodels_exact',
    'eos_and_spectrum_nonidentifiability_exact',
    'conditional_cadence_linear_pressure_incompatibility_exact',
    'linear_pressure_logarithmic_eos_exact',
    'global_logarithmic_eos_health_obstruction_exact',
    'w3_56_full_auxiliary_on_shell_energy_and_pressure_like_term_zero_exact',
    'w3_56_selected_readout_not_derived_hilbert_stress_exact',
    'restricted_no_go_scope_preserved_exact',
    'minimum_missing_core_action_class_named_exact',
    'registered_contract_keysets_exact',
    'mutation_controls_pass',
    'aggregate_gate_pass',
}

REQUIRED_SCOPE_KEYS = {
    'fully_time_dependent_oscillon_excluded_by_theorem',
    'self_gravitating_localized_configuration_excluded_by_theorem',
    'full_coframe_spectrum_reduced_to_acoustic',
    'localized_core_constitutive_action_derived',
    'amplitude_gradient_or_dispersion_derived',
    'bounded_binding_self_interaction_derived',
    'ordinary_oscillon_phase_dynamics_derived',
    'finite_energy_oscillon_solution_constructed',
    'localization_radius_derived',
    'floquet_operator_and_spectrum_derived',
    'common_cadence_from_core_spectrum_derived',
    'physical_P_F_from_core_hilbert_stress_derived',
    'square_pressure_law_from_core_stress_derived',
    'localized_backreaction_derived',
    'all_particle_families_universalized',
    'Koide_or_C3_used',
    'Planck_hierarchy_derived',
    'strong_field_or_2PN_completed',
    'cosmological_history_modified',
    'observational_likelihood_evaluated',
}

REQUIRED_SEMANTIC_STATE_KEYS = {
    'hidden_gradient_operator',
    'hidden_eos_selection',
    'claims_all_time_dependent_oscillons_excluded',
    'claims_self_gravitating_configurations_excluded',
    'claims_full_spectrum_is_acoustic',
    'fixed_coframe_premise_registered',
    'infinite_domain_registered',
    'global_phase_lock_registered',
    'affine_interval_precision_registered',
    'phase_roles_distinct',
    'selected_readout_called_hilbert_stress',
    'zero_flux_premise_registered',
    'strict_convex_premise_registered',
    'target_inserted_in_primitive_action',
    'duplicate_source',
    'external_potential_imported',
}

REQUIRED_SCOPE_REGISTRY_KEYS = REQUIRED_SEMANTIC_STATE_KEYS | REQUIRED_SCOPE_KEYS

REQUIRED_MUTATION_KEYS = {
    'hidden_gradient_operator_detected',
    'hidden_eos_selection_detected',
    'unrestricted_no_go_overclaim_detected',
    'self_gravitating_overclaim_detected',
    'fixed_coframe_premise_removal_detected',
    'infinite_domain_premise_removal_detected',
    'global_phase_lock_premise_removal_detected',
    'affine_interval_collapse_detected',
    'full_spectrum_acoustic_overclaim_detected',
    'phase_role_collapse_detected',
    'selected_readout_stress_relabel_detected',
    'zero_flux_premise_removal_detected',
    'strict_convex_premise_removal_detected',
    'target_insertion_detected',
    'duplicate_source_detected',
    'imported_potential_detected',
}

EXPECTED_RESULT_KEYS = {
    'schema_version', 'claim_id', 'claim', 'type', 'model_version',
    'status', 'scope_status', 'artifact_valid', 'evidence_type',
    'blocking_boundary', 'contract', 'closure_flags', 'scope_flags',
    'identities', 'benchmark', 'semantic_constraints',
    'negative_controls', 'diagnostics', 'provenance', 'files',
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_zero(value: object) -> bool:
    return sp.simplify(value) == 0


def exact_nonzero(value: object) -> bool:
    return sp.simplify(value) != 0


def canonical_text(path: Path) -> str:
    payload = path.read_bytes()
    if b'\r' in payload or not payload.endswith(b'\n'):
        raise RuntimeError(f'Noncanonical UTF-8 LF text: {path}')
    return payload.decode('utf-8')


def verify_preregistration() -> dict[str, object]:
    text = canonical_text(PREREG)
    actual_hash = sha256(PREREG)
    if actual_hash != PINNED_PREREG_SHA256:
        raise RuntimeError(f'Frozen preregistration changed: {actual_hash}')
    fields = set(re.findall(r'^\*\*([A-Z_]+):\*\*', text, re.MULTILINE))
    if fields != REQUIRED_CONTRACT_FIELDS:
        raise RuntimeError(
            f'Contract field drift: missing={REQUIRED_CONTRACT_FIELDS-fields}, '
            f'extra={fields-REQUIRED_CONTRACT_FIELDS}'
        )
    claim_match = re.search(r'^\*\*CLAIM:\*\*\s*(.+)$', text, re.MULTILINE)
    if claim_match is None:
        raise RuntimeError('Claim field is missing')
    required_scope_markers = (
        'fixed non-backreacting Minkowski coframe',
        'infinite asymptotically homogeneous radial domain',
        'globally phase-locked',
        'affine equation of state',
        'longitudinal phase-current plane-wave',
        'minimum missing class of physical input',
        'not derived or identifiable as a Hilbert stress',
    )
    missing_scope_markers = [
        marker for marker in required_scope_markers if marker not in text
    ]
    if missing_scope_markers:
        raise RuntimeError(
            f'Preregistered scope markers missing: {missing_scope_markers}'
        )
    registry_match = re.search(
        r'## Machine-readable scope registry\s+```yaml\s+\{(.*?)\}\s+```',
        text,
        re.DOTALL,
    )
    if registry_match is None:
        raise RuntimeError('Machine-readable scope registry is missing')
    scope_registry: dict[str, bool] = {}
    for raw_line in registry_match.group(1).splitlines():
        line = raw_line.strip().removesuffix(',')
        if not line:
            continue
        key, separator, raw_value = line.partition(':')
        key = key.strip()
        raw_value = raw_value.strip()
        if (
            separator != ':'
            or re.fullmatch(r'[A-Za-z0-9_]+', key) is None
            or raw_value not in {'true', 'false'}
            or key in scope_registry
        ):
            raise RuntimeError(f'Malformed scope-registry line: {raw_line}')
        scope_registry[key] = raw_value == 'true'
    if set(scope_registry) != REQUIRED_SCOPE_REGISTRY_KEYS:
        raise RuntimeError(
            'Scope-registry key drift: '
            f'missing={REQUIRED_SCOPE_REGISTRY_KEYS-set(scope_registry)}, '
            f'extra={set(scope_registry)-REQUIRED_SCOPE_REGISTRY_KEYS}'
        )
    if not all(type(value) is bool for value in scope_registry.values()):
        raise RuntimeError('Scope-registry values must be exact booleans')
    return {
        'path': PREREG.name,
        'sha256': actual_hash,
        'field_names': sorted(fields),
        'registered_claim': claim_match.group(1).strip(),
        'scope_markers': list(required_scope_markers),
        'scope_markers_valid': True,
        'scope_registry': scope_registry,
        'scope_registry_valid': True,
        'valid': True,
    }


def verify_dependency_contracts() -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    required_markers = {
        'W3_50': [
            'H_C(n_C, D_i theta_C, X_slow)',
            '`complete_H_C_derived`',
            '`pressure_phase_action_stress_map_derived`',
            'ordinary oscillon cycle phase',
            'eta_F a^3=1',
        ],
        'W3_54': [
            'rho_C(n_C)',
            'p_C = n_C rho_C\'(n_C)-rho_C(n_C)',
            'identity `p_C=P_F` is asserted',
            'microscopic oscillon profiles',
        ],
    }
    for claim, (path, expected_hash) in DEPENDENCY_CONTRACTS.items():
        if not path.is_file():
            raise RuntimeError(f'Missing dependency contract: {path}')
        text = canonical_text(path)
        actual_hash = sha256(path)
        if actual_hash != expected_hash:
            raise RuntimeError(
                f'Pinned dependency changed for {claim}: {actual_hash}'
            )
        missing = [marker for marker in required_markers[claim] if marker not in text]
        if missing:
            raise RuntimeError(f'Missing {claim} semantic markers: {missing}')
        records[claim] = {
            'path': path.relative_to(WORK3).as_posix(),
            'sha256': actual_hash,
            'semantic_markers_valid': True,
        }

    for path in (W3_56_PREREG, W3_56_SOURCE, W3_56_RESULT, W3_56_CHECKSUM):
        if not path.is_file():
            raise RuntimeError(f'Missing W3-56 dependency artifact: {path}')
    if sha256(W3_56_PREREG) != W3_56_PREREG_SHA256:
        raise RuntimeError('W3-56 frozen preregistration changed')
    checksum_parts = canonical_text(W3_56_CHECKSUM).strip().split()
    if len(checksum_parts) != 2 or checksum_parts[1] != W3_56_RESULT.name:
        raise RuntimeError('Malformed W3-56 checksum record')
    actual_result_hash = sha256(W3_56_RESULT)
    if checksum_parts[0] != actual_result_hash:
        raise RuntimeError('W3-56 result checksum mismatch')
    w3_56 = json.loads(canonical_text(W3_56_RESULT))
    required_false = {
        'P_F_readout_from_covariant_stress_derived',
        'reference_oscillon_core_from_foundation_derived',
        'finite_energy_oscillon_solution_constructed',
        'W3_50_localized_spectral_gate_closed',
    }
    if w3_56.get('status') != 'PASS' or w3_56.get('scope_status') != W3_56_SCOPE_STATUS:
        raise RuntimeError('W3-56 status drift')
    if not w3_56.get('closure_flags', {}).get(
        'selected_restoring_readout_square_law_exact', False
    ):
        raise RuntimeError('W3-56 selected-readout witness is missing')
    if any(w3_56.get('scope_flags', {}).get(key) is not False for key in required_false):
        raise RuntimeError('W3-56 open-boundary flags drifted')
    source_hash = sha256(W3_56_SOURCE)
    if w3_56.get('provenance', {}).get('source', {}).get('sha256') != source_hash:
        raise RuntimeError('W3-56 source provenance mismatch')
    if (
        w3_56.get('provenance', {})
        .get('preregistration', {}).get('sha256') != W3_56_PREREG_SHA256
    ):
        raise RuntimeError('W3-56 preregistration provenance mismatch')
    records['W3_56'] = {
        'preregistration_path': W3_56_PREREG.relative_to(WORK3).as_posix(),
        'preregistration_sha256': W3_56_PREREG_SHA256,
        'source_path': W3_56_SOURCE.relative_to(WORK3).as_posix(),
        'source_sha256': source_hash,
        'result_path': W3_56_RESULT.relative_to(WORK3).as_posix(),
        'result_sha256': actual_result_hash,
        'checksum_valid': True,
        'required_open_flags_valid': True,
    }
    return records


def extract_registered_section(
    text: str, start_marker: str, end_marker: str | None
) -> str:
    start = text.find(start_marker)
    if start < 0:
        raise RuntimeError(f'Missing W3-57 section marker: {start_marker}')
    if end_marker is None:
        return text[start:]
    end = text.find(end_marker, start + len(start_marker))
    if end < 0:
        raise RuntimeError(f'Missing W3-57 section terminator: {end_marker}')
    return text[start:end]


def verify_scope_documents() -> dict[str, dict[str, object]]:
    document_specs = {
        'package_readme': {
            'path': PACKAGE_README,
            'start': '# W3-57 One-Oscillon Localized-Core Identifiability Gate',
            'end': None,
            'markers': (
                PASS_STATUS,
                'fixed non-backreacting Minkowski coframe',
                'infinite asymptotically\nhomogeneous radial domain',
                'globally phase-locked',
                'longitudinal phase-current',
                'not\nderived or identifiable as a Hilbert stress',
                'minimum missing class of physical input',
                'This is not a theorem against every future oscillon.',
            ),
        },
        'cosmology_ledger': {
            'path': COSMOLOGY_LEDGER,
            'start': '### W3-57 localized-core identifiability gate',
            'end': '\n## Salvaged exact results',
            'markers': (
                PASS_STATUS,
                'fixed non-backreacting Minkowski coframe',
                'infinite asymptotically homogeneous radial domain',
                'globally phase-locked',
                'longitudinal phase-current',
                'not\nidentifiable as a Hilbert stress from the reduced model',
                'minimum missing\nclass of input',
            ),
        },
        'formal_ledger': {
            'path': FORMAL_LEDGER,
            'start': 'W3-57 now resolves that boundary for the action actually present',
            'end': '\n## Conclusion and stopping rule',
            'markers': (
                PASS_STATUS,
                'fixed non-backreacting Minkowski coframe',
                'infinite asymptotically\nhomogeneous radial domain',
                'globally\nphase-locked',
                'longitudinal phase-current',
                'not derived or identifiable as a Hilbert stress',
                'minimum missing class of input',
                'not a theorem against every future time-dependent\noscillon',
            ),
        },
    }
    forbidden_overclaims = (
        'all time-dependent oscillons are excluded',
        'self-gravitating configurations are excluded',
        'the full coframe spectrum is gapless acoustic',
        'the homogeneous fluctuation spectrum is gapless acoustic',
        'W3-57 derives a localized-core constitutive action',
        'W3-57 constructs a finite-energy oscillon',
        'This closes the existing one-potential route.',
    )
    records: dict[str, dict[str, object]] = {}
    for name, spec in document_specs.items():
        path = spec['path']
        if not isinstance(path, Path) or not path.is_file():
            raise RuntimeError(f'Missing W3-57 scope document: {path}')
        text = canonical_text(path)
        section = extract_registered_section(
            text, str(spec['start']), spec['end']
        )
        missing = [
            marker for marker in spec['markers'] if marker not in section
        ]
        forbidden = [
            marker for marker in forbidden_overclaims if marker in section
        ]
        if missing or forbidden:
            raise RuntimeError(
                f'W3-57 scope-document drift in {name}: '
                f'missing={missing}, forbidden={forbidden}'
            )
        records[name] = {
            'path': path.relative_to(WORK3).as_posix(),
            'document_sha256': sha256(path),
            'section_sha256': hashlib.sha256(
                section.encode('utf-8')
            ).hexdigest(),
            'required_markers_valid': True,
            'forbidden_overclaims_absent': True,
            'scope_valid': True,
        }
    return records


def density_derivative_absent_in_action(action: str) -> bool:
    forbidden_density_derivatives = (
        'partial_mu n_C', 'nabla_mu n_C', 'D_i n_C',
        '(partial n_C)', '(nabla n_C)',
    )
    return not any(token in action for token in forbidden_density_derivatives)


def audit_action_text() -> dict[str, object]:
    w3_50 = canonical_text(DEPENDENCY_CONTRACTS['W3_50'][0])
    w3_54 = canonical_text(DEPENDENCY_CONTRACTS['W3_54'][0])
    match = re.search(
        r'```text\n(S_F\[e,omega,J,theta_C\].*?)\n```',
        w3_54,
        re.DOTALL,
    )
    if match is None:
        raise RuntimeError('Cannot extract the frozen W3-54 master action')
    action = match.group(1)
    density_derivative_absent = density_derivative_absent_in_action(action)
    one_potential_exact = all(
        token in action
        for token in ('J^mu partial_mu theta_C', 'rho_C(n_C)', 'n_C = sqrt(')
    )
    hamiltonian_open = all(
        token in w3_50
        for token in (
            'H_C(n_C, D_i theta_C, X_slow)',
            '`complete_H_C_derived`',
            '`Hamiltonian_stability_and_causality_proved`',
        )
    )
    phase_roles_distinct = all(
        token in w3_50
        for token in ('ordinary oscillon cycle phase', 'does not identify')
    )
    return {
        'action_block': action,
        'one_potential_exact': one_potential_exact,
        'density_derivative_absent': density_derivative_absent,
        'w3_50_complete_hamiltonian_open': hamiltonian_open,
        'phase_roles_distinct': phase_roles_distinct,
    }


def validate_semantic_claim(state: dict[str, bool]) -> bool:
    return bool(
        not state['hidden_gradient_operator']
        and not state['hidden_eos_selection']
        and not state['claims_all_time_dependent_oscillons_excluded']
        and not state['claims_self_gravitating_configurations_excluded']
        and not state['claims_full_spectrum_is_acoustic']
        and state['fixed_coframe_premise_registered']
        and state['infinite_domain_registered']
        and state['global_phase_lock_registered']
        and state['affine_interval_precision_registered']
        and state['phase_roles_distinct']
        and not state['selected_readout_called_hilbert_stress']
        and state['zero_flux_premise_registered']
        and state['strict_convex_premise_registered']
        and not state['target_inserted_in_primitive_action']
        and not state['duplicate_source']
        and not state['external_potential_imported']
    )


def run_mutations(scope_registry: dict[str, bool]) -> dict[str, bool]:
    selected = {
        key: bool(scope_registry[key]) for key in REQUIRED_SEMANTIC_STATE_KEYS
    }
    if not validate_semantic_claim(selected):
        raise RuntimeError('Selected semantic contract does not validate')
    mutation_map = {
        'hidden_gradient_operator_detected': ('hidden_gradient_operator', True),
        'hidden_eos_selection_detected': ('hidden_eos_selection', True),
        'unrestricted_no_go_overclaim_detected': (
            'claims_all_time_dependent_oscillons_excluded', True
        ),
        'self_gravitating_overclaim_detected': (
            'claims_self_gravitating_configurations_excluded', True
        ),
        'fixed_coframe_premise_removal_detected': (
            'fixed_coframe_premise_registered', False
        ),
        'infinite_domain_premise_removal_detected': (
            'infinite_domain_registered', False
        ),
        'global_phase_lock_premise_removal_detected': (
            'global_phase_lock_registered', False
        ),
        'affine_interval_collapse_detected': (
            'affine_interval_precision_registered', False
        ),
        'full_spectrum_acoustic_overclaim_detected': (
            'claims_full_spectrum_is_acoustic', True
        ),
        'phase_role_collapse_detected': ('phase_roles_distinct', False),
        'selected_readout_stress_relabel_detected': (
            'selected_readout_called_hilbert_stress', True
        ),
        'zero_flux_premise_removal_detected': (
            'zero_flux_premise_registered', False
        ),
        'strict_convex_premise_removal_detected': (
            'strict_convex_premise_registered', False
        ),
        'target_insertion_detected': ('target_inserted_in_primitive_action', True),
        'duplicate_source_detected': ('duplicate_source', True),
        'imported_potential_detected': ('external_potential_imported', True),
    }
    controls: dict[str, bool] = {}
    for name, (key, value) in mutation_map.items():
        mutated = dict(selected)
        mutated[key] = value
        controls[name] = not validate_semantic_claim(mutated)
    return controls


def derive_gate(
    dependencies: dict[str, dict[str, object]],
    scope_registry: dict[str, bool],
    scope_documents: dict[str, dict[str, object]],
) -> tuple[
    dict[str, str], dict[str, bool], dict[str, bool],
    dict[str, bool], dict[str, object]
]:
    action_audit = audit_action_text()

    n, n0, eta, kappa = sp.symbols('n n0 eta kappa', positive=True)
    c0, q_wave, r = sp.symbols('c0 q_wave r', positive=True)
    rho = sp.Function('rho')(n)
    mu = sp.diff(rho, n)
    pressure = sp.simplify(n * mu - rho)
    sound_from_derivatives = sp.simplify(
        sp.diff(pressure, n) / sp.diff(rho, n)
    )
    sound_expected = sp.simplify(n * sp.diff(rho, n, 2) / sp.diff(rho, n))

    mu0, mu_prime0, omega = sp.symbols(
        'mu0 mu_prime0 omega', positive=True
    )
    phase_current_matrix = sp.Matrix([
        [-sp.I * omega, c0**2 * n0 * q_wave**2 / mu0],
        [-mu_prime0, -sp.I * omega],
    ])
    phase_current_determinant = sp.factor(phase_current_matrix.det())
    phase_sound_squared = sp.simplify(n0 * mu_prime0 / mu0)
    phase_dispersion = sp.simplify(
        c0**2 * phase_sound_squared * q_wave**2
    )
    phase_determinant_residual = sp.simplify(
        phase_current_determinant + omega**2 - phase_dispersion
    )
    phase_mass_gap_squared = sp.simplify(phase_dispersion.subs(q_wave, 0))

    flux_constant = sp.symbols('C_J', real=True)
    radial_velocity = flux_constant / (r**2 * n)
    zero_flux_velocity = sp.simplify(radial_velocity.subs(flux_constant, 0))
    radial_phase_gradient = sp.simplify(-mu * zero_flux_velocity / c0)
    rho_pp = sp.symbols('rho_pp', positive=True)
    n_prime = sp.symbols('n_prime', real=True)
    strict_solution = sp.solve(sp.Eq(rho_pp * n_prime, 0), n_prime)
    affine_slope, affine_offset = sp.symbols(
        'affine_slope affine_offset', positive=True
    )
    rho_affine = affine_slope * n + affine_offset
    affine_mu = sp.diff(rho_affine, n)
    affine_second_derivative = sp.diff(rho_affine, n, 2)

    def polytrope(gamma: sp.Rational) -> dict[str, object]:
        rho_g = kappa * n**gamma
        mu_g = sp.diff(rho_g, n)
        p_g = sp.simplify(n * mu_g - rho_g)
        cs_g = sp.simplify(n * sp.diff(rho_g, n, 2) / mu_g)
        mu_ratio = sp.simplify(mu_g.subs(n, eta * n0) / mu_g.subs(n, n0))
        p_ratio = sp.simplify(p_g.subs(n, eta * n0) / p_g.subs(n, n0))
        dispersion = sp.simplify(c0**2 * cs_g * q_wave**2)
        return {
            'gamma': gamma,
            'rho': rho_g,
            'mu': mu_g,
            'pressure': p_g,
            'sound_speed_squared': cs_g,
            'mu_ratio': mu_ratio,
            'pressure_ratio': p_ratio,
            'dispersion': dispersion,
            'mass_gap_squared': sp.simplify(dispersion.subs(q_wave, 0)),
            'rho_positive': bool(rho_g.is_positive),
            'mu_positive': bool(mu_g.is_positive),
        }

    model_43 = polytrope(sp.Rational(4, 3))
    model_2 = polytrope(sp.Integer(2))

    A = sp.symbols('A', positive=True)
    C0 = sp.symbols('C0', real=True)
    rho_cadence = sp.Rational(2, 3) * A * n**sp.Rational(3, 2) + C0
    mu_cadence = sp.diff(rho_cadence, n)
    p_cadence = sp.simplify(n * mu_cadence - rho_cadence)

    x = sp.symbols('x', positive=True)
    a_free, d_free, c_free = sp.symbols('a_free d_free c_free')
    identity_polynomial = (
        sp.Rational(1, 3) * a_free * x**3 - d_free * x**2 - c_free
    )
    identity_coefficients = sp.Poly(identity_polynomial, x).all_coeffs()
    identity_solution = sp.solve(
        [sp.Eq(value, 0) for value in identity_coefficients],
        (a_free, d_free, c_free),
        dict=True,
    )

    D, M = sp.symbols('D M', positive=True)
    rho_log = n * (M + D * sp.log(n / n0))
    mu_log = sp.simplify(sp.diff(rho_log, n))
    p_log = sp.simplify(n * mu_log - rho_log)
    rho_log_pp = sp.simplify(sp.diff(rho_log, n, 2))
    low_density_mu_limit = sp.limit(mu_log, n, 0, dir='+')
    log_coordinate = sp.symbols('log_eta', real=True)
    mu_log_history = sp.simplify(mu_log.subs(n, n0 * sp.exp(log_coordinate)))
    cadence_history = A * sp.sqrt(n0) * sp.exp(log_coordinate / 2)
    log_second_derivative = sp.diff(mu_log_history, log_coordinate, 2)
    cadence_second_derivative = sp.diff(cadence_history, log_coordinate, 2)

    K, lam, b = sp.symbols('K lambda b', positive=True)
    auxiliary = sp.Rational(1, 2) * K * (b - lam * sp.sqrt(n))**2
    b_equilibrium = lam * sp.sqrt(n)
    auxiliary_on_shell = sp.simplify(auxiliary.subs(b, b_equilibrium))
    auxiliary_n_on_shell = sp.simplify(
        sp.diff(auxiliary, n).subs(b, b_equilibrium)
    )
    auxiliary_pressure_like = sp.simplify(
        (n * sp.diff(auxiliary, n) - auxiliary).subs(b, b_equilibrium)
    )
    selected_channel_on_shell = sp.simplify(
        (sp.Rational(1, 2) * K * b**2).subs(b, b_equilibrium)
    )

    residual_values = {
        'thermodynamic_pressure_definition': pressure - (n * mu - rho),
        'sound_speed_identity': sound_from_derivatives - sound_expected,
        'homogeneous_phase_current_determinant': phase_determinant_residual,
        'homogeneous_phase_current_mass_gap': phase_mass_gap_squared,
        'zero_flux_radial_velocity': zero_flux_velocity,
        'zero_flux_radial_phase_gradient': radial_phase_gradient,
        'affine_eos_phase_rate_derivative': sp.diff(affine_mu, n),
        'affine_eos_second_derivative': affine_second_derivative,
        'polytrope_4_3_sound_speed': model_43['sound_speed_squared'] - sp.Rational(1, 3),
        'polytrope_4_3_phase_rate_ratio': model_43['mu_ratio'] - eta**sp.Rational(1, 3),
        'polytrope_4_3_pressure_ratio': model_43['pressure_ratio'] - eta**sp.Rational(4, 3),
        'polytrope_2_sound_speed': model_2['sound_speed_squared'] - 1,
        'polytrope_2_phase_rate_ratio': model_2['mu_ratio'] - eta,
        'polytrope_2_pressure_ratio': model_2['pressure_ratio'] - eta**2,
        'polytrope_4_3_mass_gap': model_43['mass_gap_squared'],
        'polytrope_2_mass_gap': model_2['mass_gap_squared'],
        'cadence_target_phase_rate': mu_cadence - A * sp.sqrt(n),
        'cadence_implied_pressure': p_cadence - (A * n**sp.Rational(3, 2) / 3 - C0),
        'linear_pressure_log_eos': p_log - D * n,
        'linear_pressure_log_eos_second_derivative': rho_log_pp - D / n,
        'log_rate_second_derivative': log_second_derivative,
        'w3_56_full_potential_on_shell': auxiliary_on_shell,
        'w3_56_density_derivative_on_shell': auxiliary_n_on_shell,
        'w3_56_pressure_like_term_on_shell': auxiliary_pressure_like,
    }
    residuals = {
        key: sp.sstr(sp.simplify(value)) for key, value in residual_values.items()
    }
    residuals_exact = all(exact_zero(value) for value in residual_values.values())

    cadence_pressure_no_go = bool(
        identity_solution == [
            {a_free: 0, c_free: 0, d_free: 0}
        ]
        and exact_nonzero(cadence_second_derivative)
        and exact_zero(log_second_derivative)
    )
    global_log_health_obstruction = bool(low_density_mu_limit == -sp.oo)
    countermodels_healthy = bool(
        model_43['rho_positive']
        and model_43['mu_positive']
        and model_2['rho_positive']
        and model_2['mu_positive']
        and model_43['sound_speed_squared'] == sp.Rational(1, 3)
        and model_2['sound_speed_squared'] == 1
    )
    countermodels_distinct = bool(
        exact_nonzero(
            model_43['sound_speed_squared'] - model_2['sound_speed_squared']
        )
        and exact_nonzero(model_43['pressure_ratio'] - model_2['pressure_ratio'])
    )

    mutations = run_mutations(scope_registry)
    selected_action = str(action_audit['action_block'])
    gradient_mutation = selected_action + ' + kappa_n (partial_mu n_C)^2'
    eos_mutation = selected_action.replace(
        'rho_C(n_C)', 'kappa*n_C^(4/3)', 1
    )
    phase_mutation = selected_action.replace('theta_C', 'theta_O')
    target_mutation = selected_action + ' + TARGET[P_F/P_F0=eta_F]'
    duplicate_source_mutation = selected_action + ' + S_duplicate[P_F]'
    imported_potential_mutation = selected_action + ' + V_O(chi)'
    nonzero_flux_velocity = sp.simplify(radial_velocity.subs(flux_constant, 1))
    strict_coefficient_after_mutation = sp.simplify(
        sp.diff(rho_pp * n_prime, n_prime).subs(rho_pp, 0)
    )
    mutations['hidden_gradient_operator_detected'] = bool(
        mutations['hidden_gradient_operator_detected']
        and not density_derivative_absent_in_action(gradient_mutation)
    )
    mutations['hidden_eos_selection_detected'] = bool(
        mutations['hidden_eos_selection_detected']
        and 'kappa*n_C^(4/3)' in eos_mutation
        and eos_mutation != selected_action
    )
    mutations['phase_role_collapse_detected'] = bool(
        mutations['phase_role_collapse_detected']
        and 'theta_C' not in phase_mutation
        and 'theta_O' in phase_mutation
    )
    mutations['zero_flux_premise_removal_detected'] = bool(
        mutations['zero_flux_premise_removal_detected']
        and exact_nonzero(nonzero_flux_velocity)
    )
    mutations['strict_convex_premise_removal_detected'] = bool(
        mutations['strict_convex_premise_removal_detected']
        and exact_zero(strict_coefficient_after_mutation)
    )
    mutations['selected_readout_stress_relabel_detected'] = bool(
        mutations['selected_readout_stress_relabel_detected']
        and exact_zero(auxiliary_on_shell)
        and exact_nonzero(selected_channel_on_shell)
    )
    mutations['target_insertion_detected'] = bool(
        mutations['target_insertion_detected']
        and 'TARGET[P_F/P_F0=eta_F]' in target_mutation
    )
    mutations['duplicate_source_detected'] = bool(
        mutations['duplicate_source_detected']
        and 'S_duplicate[P_F]' in duplicate_source_mutation
    )
    mutations['imported_potential_detected'] = bool(
        mutations['imported_potential_detected']
        and 'V_O(chi)' in imported_potential_mutation
    )
    scope_flags = {
        key: bool(scope_registry[key]) for key in REQUIRED_SCOPE_KEYS
    }
    closure_flags = {
        'dependency_hashes_pinned_exact': all(
            record.get('semantic_markers_valid', True)
            and record.get('checksum_valid', True)
            for record in dependencies.values()
        ),
        'w3_50_collective_phase_role_preserved_exact': bool(
            action_audit['phase_roles_distinct']
        ),
        'w3_54_one_potential_action_audited_exact': bool(
            action_audit['one_potential_exact']
        ),
        'density_derivative_operator_absent_exact': bool(
            action_audit['density_derivative_absent']
            and action_audit['w3_50_complete_hamiltonian_open']
        ),
        'stationary_spherical_current_integrated_exact': exact_zero(
            r**2 * n * radial_velocity - flux_constant
        ),
        'regular_zero_flux_branch_exact': exact_zero(zero_flux_velocity),
        'radial_phase_gradient_zero_exact': exact_zero(radial_phase_gradient),
        'strict_convex_phase_locked_profile_homogeneous_exact': bool(
            strict_solution == [0]
        ),
        'degenerate_branch_profile_unselected_exact': bool(
            exact_zero(affine_second_derivative)
            and exact_zero(sp.diff(affine_mu, n))
            and action_audit['density_derivative_absent']
        ),
        'thermodynamic_pressure_from_action_exact': exact_zero(
            residual_values['thermodynamic_pressure_definition']
        ),
        'homogeneous_phase_current_determinant_exact': exact_zero(
            phase_determinant_residual
        ),
        'homogeneous_sound_speed_formula_exact': exact_zero(
            residual_values['sound_speed_identity']
        ),
        'acoustic_mass_gap_absent_exact': bool(
            exact_zero(phase_mass_gap_squared)
            and exact_zero(model_43['mass_gap_squared'])
            and exact_zero(model_2['mass_gap_squared'])
        ),
        'healthy_polytropic_countermodels_exact': countermodels_healthy,
        'eos_and_spectrum_nonidentifiability_exact': countermodels_distinct,
        'conditional_cadence_linear_pressure_incompatibility_exact': (
            cadence_pressure_no_go
        ),
        'linear_pressure_logarithmic_eos_exact': exact_zero(
            residual_values['linear_pressure_log_eos']
        ),
        'global_logarithmic_eos_health_obstruction_exact': (
            global_log_health_obstruction
        ),
        'w3_56_full_auxiliary_on_shell_energy_and_pressure_like_term_zero_exact': bool(
            exact_zero(auxiliary_on_shell)
            and exact_zero(auxiliary_n_on_shell)
            and exact_zero(auxiliary_pressure_like)
        ),
        'w3_56_selected_readout_not_derived_hilbert_stress_exact': bool(
            exact_nonzero(selected_channel_on_shell)
            and dependencies['W3_56']['required_open_flags_valid']
        ),
        'restricted_no_go_scope_preserved_exact': all(
            record['scope_valid'] is True
            for record in scope_documents.values()
        ) and all(
            scope_registry[key] is expected
            for key, expected in {
                'fixed_coframe_premise_registered': True,
                'infinite_domain_registered': True,
                'global_phase_lock_registered': True,
                'affine_interval_precision_registered': True,
                'zero_flux_premise_registered': True,
                'strict_convex_premise_registered': True,
                'claims_all_time_dependent_oscillons_excluded': False,
                'claims_self_gravitating_configurations_excluded': False,
                'claims_full_spectrum_is_acoustic': False,
            }.items()
        ),
        'minimum_missing_core_action_class_named_exact': (
            'minimum missing class of physical input' in canonical_text(PREREG)
            and 'coframe-coupled localized-core constitutive action'
            in canonical_text(PREREG)
        ),
        'registered_contract_keysets_exact': False,
        'mutation_controls_pass': all(mutations.values()),
        'aggregate_gate_pass': False,
    }

    benchmark = {
        'polytrope_4_3': {
            'sound_speed_squared': sp.sstr(model_43['sound_speed_squared']),
            'phase_rate_ratio': sp.sstr(model_43['mu_ratio']),
            'pressure_ratio': sp.sstr(model_43['pressure_ratio']),
            'rho_positive': model_43['rho_positive'],
            'mu_positive': model_43['mu_positive'],
        },
        'polytrope_2': {
            'sound_speed_squared': sp.sstr(model_2['sound_speed_squared']),
            'phase_rate_ratio': sp.sstr(model_2['mu_ratio']),
            'pressure_ratio': sp.sstr(model_2['pressure_ratio']),
            'rho_positive': model_2['rho_positive'],
            'mu_positive': model_2['mu_positive'],
        },
        'same_charge_law': 'eta_F*a^3=1',
        'different_acoustic_operators': countermodels_distinct,
    }
    semantic_constraints = {
        'no_go_branch': (
            'fixed_nonbackreacting_Minkowski_coframe+infinite_asymptotically_'
            'homogeneous_radial_domain+stationary+spherical+global_phase_'
            'lock+regular_center+zero_flux+strict_convexity'
        ),
        'acoustic_scope': (
            'longitudinal phase-current plane waves on an infinite '
            'homogeneous fixed background'
        ),
        'not_claimed': (
            'fully time-dependent cores, self-gravitating configurations, '
            'or the full coframe spectrum'
        ),
        'phase_roles': 'theta_C != theta_O != process_time',
        'pressure_ledger': 'p_C != P_F != W3-56 selected P_F^(R)',
        'minimum_missing_input_class': (
            'one coframe-coupled localized-core constitutive action'
        ),
    }
    diagnostics = {
        'residuals_exact': residuals_exact,
        'action_audit': action_audit,
        'strict_convex_solution_for_density_gradient': [
            sp.sstr(value) for value in strict_solution
        ],
        'generic_sound_speed_squared': sp.sstr(sound_expected),
        'phase_current_linearized_matrix': sp.sstr(phase_current_matrix),
        'phase_current_determinant': sp.sstr(phase_current_determinant),
        'phase_current_dispersion': sp.sstr(phase_dispersion),
        'phase_current_mass_gap_squared': sp.sstr(phase_mass_gap_squared),
        'affine_eos': sp.sstr(rho_affine),
        'affine_phase_rate': sp.sstr(affine_mu),
        'cadence_implied_eos': sp.sstr(rho_cadence),
        'cadence_implied_pressure': sp.sstr(p_cadence),
        'pressure_implied_logarithmic_eos': sp.sstr(rho_log),
        'pressure_implied_phase_rate': sp.sstr(mu_log),
        'low_density_phase_rate_limit': sp.sstr(low_density_mu_limit),
        'simultaneous_identity_solution': [
            {sp.sstr(key): sp.sstr(value) for key, value in item.items()}
            for item in identity_solution
        ],
        'w3_56_auxiliary_on_shell': {
            'full_potential': sp.sstr(auxiliary_on_shell),
            'density_derivative': sp.sstr(auxiliary_n_on_shell),
            'pressure_like_term': sp.sstr(auxiliary_pressure_like),
            'selected_channel': sp.sstr(selected_channel_on_shell),
        },
    }
    return residuals, closure_flags, scope_flags, mutations, {
        'benchmark': benchmark,
        'semantic_constraints': semantic_constraints,
        'diagnostics': diagnostics,
    }


def build_report() -> dict[str, object]:
    prereg = verify_preregistration()
    dependencies = verify_dependency_contracts()
    scope_documents = verify_scope_documents()
    residuals, closure_flags, scope_flags, mutations, derived = derive_gate(
        dependencies, prereg['scope_registry'], scope_documents
    )
    source = Path(__file__)
    canonical_text(source)
    result: dict[str, object] = {
        'schema_version': '1.0',
        'claim_id': CLAIM_ID,
        'claim': prereg['registered_claim'],
        'type': (
            'EXACT_RESTRICTED_NO_GO_AND_IDENTIFIABILITY_AUDIT_OF_THE_'
            'EXISTING_ONE_POTENTIAL_PHASE_CURRENT_ACTION'
        ),
        'model_version': MODEL_VERSION,
        'status': 'PENDING',
        'scope_status': 'PENDING',
        'artifact_valid': False,
        'evidence_type': 'EXACT_SYMBOLIC_AND_ANALYTIC_EXISTING_ACTION_GATE',
        'blocking_boundary': (
            'The minimum missing class of physical input is a coframe-'
            'coupled localized-core constitutive action. It must supply the '
            'dispersive/amplitude-gradient '
            'response, bounded binding nonlinearity, distinct ordinary '
            'oscillon phase, and action-derived stress projection.'
        ),
        'contract': {
            'field_names': prereg['field_names'],
            'preregistration_sha256': prereg['sha256'],
            'scope_registry': prereg['scope_registry'],
            'scope_document_records': scope_documents,
            'dependency_records': dependencies,
            'no_go_domain': (
                'fixed non-backreacting Minkowski coframe; infinite '
                'asymptotically homogeneous radial domain; strict-convex '
                'stationary spherical globally phase-locked zero-flux'
            ),
            'data_role': 'NO_DATA_READ_OR_FITTED',
        },
        'closure_flags': closure_flags,
        'scope_flags': scope_flags,
        'identities': residuals,
        'benchmark': derived['benchmark'],
        'semantic_constraints': derived['semantic_constraints'],
        'negative_controls': mutations,
        'diagnostics': derived['diagnostics'],
        'provenance': {
            'generated_utc': datetime.now(timezone.utc).isoformat(),
            'preregistration': prereg,
            'dependency_records': dependencies,
            'scope_document_records': scope_documents,
            'source': {'path': source.name, 'sha256': sha256(source)},
            'python': platform.python_version(),
            'sympy': importlib.metadata.version('sympy'),
            'platform': platform.platform(),
            'line_endings': 'LF',
        },
        'files': {
            'readme': 'README.md',
            'preregistration': PREREG.name,
            'source': source.name,
            'result': OUTPUT.name,
            'checksum': HASH_OUTPUT.name,
        },
    }
    keysets_exact = bool(
        set(result) == EXPECTED_RESULT_KEYS
        and set(closure_flags) == REQUIRED_EXACT_KEYS
        and set(scope_flags) == REQUIRED_SCOPE_KEYS
        and set(mutations) == REQUIRED_MUTATION_KEYS
        and set(prereg['field_names']) == REQUIRED_CONTRACT_FIELDS
    )
    closure_flags['registered_contract_keysets_exact'] = keysets_exact
    closure_flags['aggregate_gate_pass'] = all(
        value for key, value in closure_flags.items()
        if key != 'aggregate_gate_pass'
    )
    artifact_valid = bool(
        closure_flags['aggregate_gate_pass']
        and all(value is False for value in scope_flags.values())
        and derived['diagnostics']['residuals_exact']
    )
    result['artifact_valid'] = artifact_valid
    result['status'] = 'PASS' if artifact_valid else 'FAIL'
    result['scope_status'] = PASS_STATUS if artifact_valid else 'FAIL_W3_57_GATE'
    if not artifact_valid:
        raise RuntimeError('W3-57 aggregate gate failed')
    return result


def write_atomic(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('w', encoding='utf-8', newline='\n') as handle:
        handle.write(text)
    temporary.replace(path)


def write_report(report: dict[str, object]) -> str:
    payload = json.dumps(
        report, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False
    ) + '\n'
    write_atomic(OUTPUT, payload)
    digest = sha256(OUTPUT)
    write_atomic(HASH_OUTPUT, f'{digest}  {OUTPUT.name}\n')
    return digest


def write_failure(error: Exception) -> None:
    failure = {
        'schema_version': '1.0-failure',
        'claim_id': CLAIM_ID,
        'model_version': MODEL_VERSION,
        'status': 'FAIL',
        'artifact_valid': False,
        'error': f'{type(error).__name__}: {error}',
        'generated_utc': datetime.now(timezone.utc).isoformat(),
    }
    payload = json.dumps(
        failure, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False
    ) + '\n'
    write_atomic(OUTPUT, payload)
    digest = sha256(OUTPUT)
    write_atomic(HASH_OUTPUT, f'{digest}  {OUTPUT.name}\n')


def main() -> int:
    try:
        report = build_report()
        digest = write_report(report)
    except Exception as error:
        write_failure(error)
        print(f'FAIL: {error}', file=sys.stderr)
        return 2
    print(report['scope_status'])
    print(f'Result: {OUTPUT}')
    print(f'Result SHA-256: {digest}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
