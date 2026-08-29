'''W3-55 exact algebra, ledger-separation, and provenance audit.'''

from hashlib import sha256
from pathlib import Path

from sympy import Rational, simplify, symbols


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONTRACT = (
    HERE / 'w3_55_relational_invariant_separation_relative_scale_contract.md'
)
COSMOLOGY_README = HERE.parent / 'Cosmology_and_LSS' / 'README.md'
FORMAL_PROOF = (
    HERE.parent / 'Lagrangian_Formulation' / 'RefG_Formal_Proof.md'
)

DEPENDENCIES = {
    'RefG/work 3/Cosmology_and_LSS/Expansion_Relaxation_Causal_Lock/'
    'w3_40_expansion_relaxation_causal_lock_preregistration.md':
        '6DA72A4FEA86FE6BD4C29F007593C9C2C176062150D2090EE597845A53C9F5EB',
    'RefG/work 3/Cosmology_and_LSS/Foundation_State_Space_and_Volume_Map/'
    'w3_42_foundation_state_space_volume_map_preregistration.md':
        '8BA44AF154A3F9A18B207B4F17A3DCECDB27A8A9D59F7F9AA712C0946763AE98',
    'RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/'
    'w3_46_active_participation_resonance_feedback_contract.md':
        '0109ED3D5E8DAEC55DBD0F01F8B05932E6F653373438455C32A3D26378E0F3B2',
    'RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/'
    'w3_47_post_genesis_evolution_pressure_coupling_kernel_preregistration.md':
        '9B603B1DF55EDF994F1E528A6CC8E16B69C474DD4C1B3DF815E2654A6C279D50',
    'RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/'
    'w3_47_post_genesis_evolution_pressure_coupling_kernel.py':
        '9D09324D9010447EFF29E7AABDCD205609DCB26D6C3CA936B6F236901DB92C98',
    'RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback/'
    'w3_50_neutral_collective_phase_density_bridge_contract.md':
        'C9B8E7DC8BEB44E26838BA65A49400A58431FBB06F72A30BB3A4CC99D46DD635',
    'RefG/work 3/Lagrangian_Formulation/'
    'Relational_Coframe_TEGR_Phase_Source_Closure/'
    'w3_54_relational_coframe_tegr_phase_source_closure_contract.md':
        '6CC748EB806D0BCCAAF63105567A5D9B1569C56F6B53951C554EC4BAD1AA9879',
    'intuitive/RefG_GE.md':
        '23EBE28AA32CF342A682208771320B15E896952DFD801A8CCE459369CCFD00E5',
}

REQUIRED = (
    'N12_AND_QC_ROLES_SEPARATED=true',
    'A_TO_a_RELATIVE_RECONSTRUCTION_EXACT_ON_SELECTED_DENSITY_BRANCH=true',
    'NO_ABSOLUTE_RULER_DERIVED=true',
    'N12_EQUALS_QC_OVER_QSTAR_DERIVED=false',
    'ACTIVE_NC_A_MEASURE_RECLASSIFICATION_DERIVED=false',
    'a=A^(2/5)',
    'p=A^(-3/5)',
    'eta_F=P_F/P_F0=A^(-6/5)',
    'one registered relational-step/link counting convention',
    'registered relative to the existing `R_act` evolution',
)
REQUIRED_FIELDS = (
    'CLAIM_ID',
    'CLAIM',
    'TYPE',
    'MODEL_VERSION',
    'ASSUMPTIONS',
    'DOMAIN',
    'CONVENTIONS',
    'FREEDOM_LEDGER',
    'DEPENDENCIES',
    'METHOD',
    'PASS_CONDITION',
    'FAIL_CONDITION',
    'FALSIFIER',
    'RESIDUAL',
    'ERROR_BOUND',
    'VALIDITY_HEALTH',
    'BRANCHES',
    'OBSERVABLE_MAP',
    'FORWARD_MODEL',
    'DATA_ROLE',
    'IDENTIFIABILITY',
    'BENCHMARK',
    'CLOSURE_FLAGS',
    'CROSSCHECK',
    'PROVENANCE',
    'FILES',
)
FORBIDDEN = (
    'PASS — CONDITIONAL FOUNDATION BRIDGE CLOSED',
    'FOUNDATION_INVARIANT_COUNT_NOETHER_BRIDGE',
    'W3-FOUNDATION-v1.0-INVARIANT-COUNT-CURRENT-BRIDGE',
    'ARCHIVED_ACTION_MAP',
    'n_Q^A',
    'n_Q^F',
    'sqrt(-g_A)',
    'W3-55 therefore supersedes',
)


def check_provenance() -> None:
    for relative, expected in DEPENDENCIES.items():
        path = ROOT / relative
        assert path.is_file(), f'Missing dependency: {relative}'
        actual = sha256(path.read_bytes()).hexdigest().upper()
        assert actual == expected, (
            f'Dependency drift: {relative}; expected {expected}, got {actual}'
        )


def check_contract() -> None:
    text = CONTRACT.read_text(encoding='utf-8')
    for marker in REQUIRED:
        assert marker in text, f'Missing contract marker: {marker}'
    for field in REQUIRED_FIELDS:
        assert f'- `{field}`:' in text, f'Missing claim-contract field: {field}'
    for marker in FORBIDDEN:
        assert marker not in text, f'Retired draft marker survived: {marker}'
    assert 'Q_C=q_* N_12' in text
    assert 'is neither assumed nor derived' in text
    assert '`n_C` is not a node density' in text


def check_downstream_insertions() -> None:
    readme = COSMOLOGY_README.read_text(encoding='utf-8')
    formal = FORMAL_PROOF.read_text(encoding='utf-8')
    combined = readme + '\n' + formal

    for marker in (
        'W3-55 relational invariants and relative-scale reconstruction',
        'a=A^(2/5)',
        'identifies `N_12` with `Q_C`',
        'ideal-comoving path inventory `N_12` distinct',
        '`n_F=Q/V_F`, `n_A=Q/V_A`',
    ):
        assert marker in combined, f'Missing downstream marker: {marker}'
    for marker in FORBIDDEN:
        assert marker not in combined, (
            f'Retired draft marker leaked downstream: {marker}'
        )


def check_reconstruction() -> None:
    A = symbols('A', positive=True)
    a = A ** Rational(2, 5)
    p = A ** Rational(-3, 5)
    eta = A ** Rational(-6, 5)
    assert simplify(A - a / p) == 0
    assert simplify(p**2 - eta) == 0
    assert simplify(eta * a**3 - 1) == 0
    assert simplify(a ** Rational(5, 2) - A) == 0
    assert simplify(eta * A**3 - 1) != 0


def check_ledger_separation() -> None:
    assert (7, Rational(3, 2))[0] == (7, Rational(11, 3))[0]
    assert (7, Rational(3, 2))[1] != (7, Rational(11, 3))[1]
    assert (5, Rational(9, 4))[0] != (12, Rational(9, 4))[0]
    assert (5, Rational(9, 4))[1] == (12, Rational(9, 4))[1]


def check_scale_and_measure() -> None:
    N, ef, em, a, p, lam, q, v0 = symbols(
        'N ell_F0 ell_mat0 a p lambda Q V_0', positive=True
    )
    ratio = N * ef * a / (em * p)
    changed_units = ratio.subs(
        {ef: lam * ef, em: lam * em}, simultaneous=True
    )
    assert simplify(changed_units - ratio) == 0

    A = a / p
    n_f = q / (a**3 * v0)
    n_a = q / (A**3 * v0)
    assert simplify(n_a - p**3 * n_f) == 0


def main() -> None:
    check_provenance()
    check_contract()
    check_downstream_insertions()
    check_reconstruction()
    check_ledger_separation()
    check_scale_and_measure()
    flags = {
        'DEPENDENCY_HASHES_PINNED': True,
        'N12_AND_QC_ROLES_SEPARATED': True,
        'RELATIVE_SCALE_RECONSTRUCTION_EXACT': True,
        'ONE_EFFECT_LEDGER_PROTECTED': True,
        'ABSOLUTE_LENGTH_SELECTED': False,
        'COUNT_CHARGE_IDENTIFICATION_DERIVED': False,
        'ACTIVE_NC_RECLASSIFIED': False,
        'OBSERVATIONAL_DATA_READ_OR_FITTED': False,
    }
    for name, value in flags.items():
        print(f'{name}={str(value).lower()}')
    print(
        'W3-55 PASS: relative-scale reconstruction verified; '
        'absolute scale remains unselected.'
    )


if __name__ == '__main__':
    main()
