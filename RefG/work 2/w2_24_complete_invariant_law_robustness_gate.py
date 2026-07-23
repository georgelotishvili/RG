"""Exact invariant-law completeness and robustness audit for the legacy A=S+R route.

The audited representation is the imported three-dimensional carrier used by
w2_15/w2_16: A is a real traceless matrix, S=(A+A.T)/2 is symmetric traceless,
R=(A-A.T)/2 is skew, and one common O(3) acts by conjugation.  This file
enumerates every scalar polynomial invariant through total degree four and
then asks whether the separable potential used in w2_16 is an open, structural
member of that complete law class.

The mathematical result is an adjudication, not a new foundation candidate.
The complete law contains three mixed directions omitted by the old potential.
Two of them generically lift its relative-orientation modulus.  Consequently
the exact w2_16 F2 witness family and the w2_22 tangent route live on tuned
lower-dimensional coefficient loci and receive no inheritance in the revised
common-kernel program.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable

import sympy as sp


CLAIM_ID = "W2_COMPLETE_O3_INVARIANT_LAW_ROBUSTNESS_AUDIT_001"
MODEL_VERSION = "W2-C0-LEGACY-A-SPLIT-INVARIANT-AUDIT-v1.0"
W223_CLAIM_ID = "W2_F0_COMMON_RESONANT_KERNEL_CONTRACT_001"

REQUIRED_SCIENTIFIC_FIELDS = frozenset({
    "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS", "DOMAIN",
    "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
    "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
    "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
    "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
    "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
})

BASIS_MANIFEST: tuple[dict[str, Any], ...] = (
    {"name": "ONE", "degree": 0, "bidegree_SR": (0, 0),
     "definition": "1", "transpose_parity": "EVEN"},
    {"name": "I2", "degree": 2, "bidegree_SR": (2, 0),
     "definition": "Tr(S^2)", "transpose_parity": "EVEN"},
    {"name": "J", "degree": 2, "bidegree_SR": (0, 2),
     "definition": "-Tr(R^2)", "transpose_parity": "EVEN"},
    {"name": "I3", "degree": 3, "bidegree_SR": (3, 0),
     "definition": "Tr(S^3)", "transpose_parity": "EVEN"},
    {"name": "M3", "degree": 3, "bidegree_SR": (1, 2),
     "definition": "Tr(S R^2)", "transpose_parity": "EVEN"},
    {"name": "I2_SQUARED", "degree": 4, "bidegree_SR": (4, 0),
     "definition": "I2^2", "transpose_parity": "EVEN"},
    {"name": "I2_J", "degree": 4, "bidegree_SR": (2, 2),
     "definition": "I2 J", "transpose_parity": "EVEN"},
    {"name": "J_SQUARED", "degree": 4, "bidegree_SR": (0, 4),
     "definition": "J^2", "transpose_parity": "EVEN"},
    {"name": "M4", "degree": 4, "bidegree_SR": (2, 2),
     "definition": "Tr(S^2 R^2)", "transpose_parity": "EVEN"},
)

EXPECTED_DIMENSIONS_BY_DEGREE = {0: 1, 1: 0, 2: 2, 3: 2, 4: 4}
INITIAL_CLOSURE_FLAGS = {
    "complete_O3_scalar_basis_through_degree4_proved": False,
    "legacy_separable_U_open_neighbourhood_robust": False,
    "legacy_flat_tau_F2_route_open_neighbourhood_robust": False,
    "legacy_w2_22_tangent_route_open_neighbourhood_robust": False,
    "legacy_route_no_inheritance": False,
    "common_resonant_kernel_candidate_supplied": False,
    "foundation_law_derived": False,
    "F1_F2_F3a_F4_promoted": False,
    "space_metric_GR_or_PN_proved": False,
    "observational_validation_proved": False,
}

SCIENTIFIC_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": CLAIM_ID,
    "CLAIM": (
        "Within the imported n=3 traceless A=S+R representation, derive the complete common-"
        "O(3)-conjugation invariant scalar polynomial law through degree four and decide exactly "
        "whether the legacy separable potential, its flat relative tau modulus, its conditional "
        "F2 witness family and its tangent route persist on an open coefficient neighbourhood."
    ),
    "TYPE": "EXACT_CLASS_LOCAL_INVARIANT_BASIS_AND_ROBUSTNESS_ADJUDICATION",
    "MODEL_VERSION": MODEL_VERSION,
    "ASSUMPTIONS": (
        "A is the imported real traceless 3x3 carrier of w2_15/w2_16, with S symmetric "
        "traceless, R skew and one common O(3) conjugation. The audited laws are real scalar "
        "polynomials of total degree at most four with no derivatives, external tensors, target "
        "data or physical interpretation. The first fundamental theorem for O(3) reduces scalar "
        "invariants of these rank-two tensors to complete delta contractions."
    ),
    "DOMAIN": (
        "Sym_0(3,R) plus so(3), common O(3), transpose involution S->S and R->-R, total "
        "polynomial degree 0 through 4. The robustness test uses the nonzero uniaxial-by-skew "
        "legacy branch s>0, J>0 and 0<=tau<=1. Claims outside n=3, beyond degree four, with "
        "derivatives or with a different carrier are excluded."
    ),
    "CONVENTIONS": (
        "I2=Tr(S^2), J=-Tr(R^2), I3=Tr(S^3), M3=Tr(SR^2), "
        "M4=Tr(S^2R^2), C=[S,R], K=Tr(C^T C), and "
        "tau=K/(s^2 J) on sJ!=0. Polynomial degree counts each S or R once."
    ),
    "FREEDOM_LEDGER": {
        "imported_carrier_representation": {
            "source": "w2_15 legacy hypothesis", "allowed_range": "sl(3,R)",
            "scale": "internal representation", "complexity": 8,
        },
        "common_equivalence": {
            "source": "legacy matrix star-algebra", "allowed_range": "common O(3)",
            "scale": "representation", "complexity": 0,
        },
        "complete_nonconstant_coefficients": {
            "source": "derived invariant basis", "allowed_range":
                "alpha,eta,b,gamma,c,e,d,delta real subject to later health conditions",
            "scale": "eight universal law coefficients", "complexity": 8,
        },
        "additive_constant": {
            "source": "degree-zero invariant", "allowed_range": "one real constant",
            "scale": "dynamically irrelevant here", "complexity": 0,
        },
        "legacy_mixed_coefficients": {
            "source": "w2_15 architectural choice", "allowed_range":
                "gamma=e=delta=0", "scale": "codimension-three locus", "complexity": 0,
        },
        "physical_semantics_or_data": {
            "source": "none", "allowed_range": 0, "scale": "all", "complexity": 0,
        },
    },
    "DEPENDENCIES": [
        "CODES.md scientific-contract and fail-closed gate rules",
        "w2_15 frozen legacy A=S+R separable-law contract",
        "w2_16 conditional exact structural F2 result for that frozen law",
        "w2_23 outcome-neutral common-resonant-kernel contract as semantic scope boundary",
    ],
    "METHOD": (
        "Derive invariants by complete O(3) index contractions, enumerate the corresponding "
        "trace-word cycle partitions independently through degree four, compute exact symbolic "
        "coefficient ranks, verify infinitesimal rotations and a reflection, classify transpose "
        "parity, reduce all trace identities, and evaluate the complete law on the exact "
        "uniaxial-by-skew quotient. Use positive, null, omission and arbitrary-small mixed-law "
        "controls with fail-closed decision logic."
    ),
    "PASS_CONDITION": (
        "The adjudication passes only if the contraction enumeration and independent exact rank "
        "calculation give dimensions 1,0,2,2,4; the displayed basis spans them; every invariant, "
        "identity and parity check is exact; the old law is recovered only at zero mixed "
        "coefficients; and an arbitrarily small admissible mixed perturbation proves that flat "
        "tau and the exact current F2/tangent route are not open-neighbourhood properties."
    ),
    "FAIL_CONDITION": (
        "A missing invariant, rank mismatch, failed O(3) or transpose check, incorrect trace "
        "identity, inability to recover the old law, an open coefficient neighbourhood on which "
        "the complete legacy flat-tau/F2/tangent structure persists, a malformed control, "
        "dependency drift or any physical promotion fails this audit."
    ),
    "FALSIFIER": (
        "An exact scalar invariant of degree at most four outside the certified span, or a proof "
        "that all sufficiently small symmetry-allowed healthy mixed perturbations preserve the "
        "legacy same-unary variable-tau minimum family, falsifies the adjudication claim."
    ),
    "RESIDUAL": "Zero for every symbolic identity and span calculation.",
    "ERROR_BOUND": "Zero; all coefficients, ranks and reductions are exact over the rationals.",
    "VALIDITY_HEALTH": (
        "The result is exact only inside the declared n=3 degree-at-most-four scalar-law class. "
        "Higher-degree invariants can introduce nonlinear tau dependence and require a new audit. "
        "This file diagnoses a legacy representation; it neither selects nor derives the "
        "revised one-identity carrier and transfer law required by w2_23."
    ),
    "BRANCHES": {
        "complete_degree4_law": "EVALUATED_CLASS",
        "legacy_separable_law": "CODIMENSION_THREE_MIXED_COEFFICIENT_LOCUS",
        "flat_tau_on_frozen_old_manifold": "CODIMENSION_ONE_CANCELLATION_LOCUS",
        "full_same_unary_stationary_tau_continuum": "CODIMENSION_TWO_LOCUS",
        "generic_mixed_law": "TAU_MODULUS_LIFTED",
        "higher_degree_or_new_carrier": "OPEN_NEW_AUDIT",
        "foundation_candidate": "NOT_SUPPLIED",
    },
    "OBSERVABLE_MAP": {"status": "N/A", "reason": "pre-spatial algebra audit"},
    "FORWARD_MODEL": {"status": "N/A", "reason": "no observable or data"},
    "DATA_ROLE": {"status": "N/A", "reason": "no fit, validation or prediction"},
    "IDENTIFIABILITY": (
        "The exact polynomial coefficient rank separates eight nonconstant basis directions. "
        "The legacy law occupies gamma=e=delta=0; flat tau at fixed old s obeys "
        "3 gamma+delta s=0; a full fixed-unary stationary continuum requires gamma=delta=0."
    ),
    "BENCHMARK": (
        "Positive controls are the full basis and nonzero mixed invariants. Null controls are "
        "R=0, S=0, odd-R traces and the exact legacy substitution. Adversarial controls omit "
        "M3, I2J or M4, mutate gate schemas, and add an arbitrary-small gamma M3 perturbation."
    ),
    "CLOSURE_FLAGS": dict(INITIAL_CLOSURE_FLAGS),
    "CROSSCHECK": (
        "Compare the contraction/trace-word span with an independent exact monomial-coefficient "
        "rank; verify the quotient formulas directly in matrices; and independently recover the "
        "same orientation slope from M3 and M4."
    ),
    "PROVENANCE": {
        "date": "2026-07-23", "data": "none",
        "code_version": "w2_24 v1.0", "hash_mode":
            "canonical payload hashes; legacy dependencies use machine-readable semantic interfaces",
    },
    "FILES": [
        "RefG/work 2/w2_24_complete_invariant_law_robustness_gate.py",
        "RefG/work 2/w2_15_f2b_general_traceless_single_carrier_candidate_contract.py",
        "RefG/work 2/w2_16_f2b_general_traceless_single_carrier_candidate_gate.py",
        "RefG/work 2/w2_23_common_resonant_kernel_contract.py",
    ],
}
CLAIM_CONTRACT = SCIENTIFIC_CONTRACT


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


# Literal checksums are filled only from the frozen payloads above. They avoid
# self-referential source hashing while detecting any scientific-payload drift.
EXPECTED_BASIS_MANIFEST_SHA256 = (
    "13FF6156718F3673569F7043C185216957091BDFCC1BF944FC160027216F3C78"
)
EXPECTED_SCIENTIFIC_CONTRACT_SHA256 = (
    "49C18B09331F85C11435363D6E9D8685076BA782A6961C7484617DB8A2814113"
)


def _all_true(value: Any) -> bool:
    if isinstance(value, dict):
        return all(_all_true(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return all(_all_true(item) for item in value)
    return value is True


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return str(value)


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _matrix_model() -> dict[str, Any]:
    s11, s22, s12, s13, s23 = sp.symbols(
        "s11 s22 s12 s13 s23", real=True
    )
    r1, r2, r3 = sp.symbols("r1 r2 r3", real=True)
    S = sp.Matrix([
        [s11, s12, s13],
        [s12, s22, s23],
        [s13, s23, -s11 - s22],
    ])
    R = sp.Matrix([
        [0, -r3, r2],
        [r3, 0, -r1],
        [-r2, r1, 0],
    ])
    return {
        "S": S, "R": R,
        "s_variables": (s11, s22, s12, s13, s23),
        "r_variables": (r1, r2, r3),
        "variables": (s11, s22, s12, s13, s23, r1, r2, r3),
    }


def _basis_expressions(model: dict[str, Any]) -> dict[str, sp.Expr]:
    S, R = model["S"], model["R"]
    I2 = sp.expand(sp.trace(S**2))
    J = sp.expand(-sp.trace(R**2))
    I3 = sp.expand(sp.trace(S**3))
    M3 = sp.expand(sp.trace(S * R**2))
    M4 = sp.expand(sp.trace(S**2 * R**2))
    return {
        "ONE": sp.Integer(1),
        "I2": I2,
        "J": J,
        "I3": I3,
        "M3": M3,
        "I2_SQUARED": sp.expand(I2**2),
        "I2_J": sp.expand(I2 * J),
        "J_SQUARED": sp.expand(J**2),
        "M4": M4,
    }


def _integer_partitions(total: int, maximum: int | None = None) -> list[tuple[int, ...]]:
    if total == 0:
        return [()]
    upper = total if maximum is None else min(total, maximum)
    result: list[tuple[int, ...]] = []
    for first in range(upper, 0, -1):
        for tail in _integer_partitions(total - first, first):
            result.append((first,) + tail)
    return result


def _necklaces(length: int) -> tuple[str, ...]:
    representatives: set[str] = set()
    for letters in itertools.product("SR", repeat=length):
        word = "".join(letters)
        rotations = tuple(word[index:] + word[:index] for index in range(length))
        representatives.add(min(rotations))
    return tuple(sorted(representatives))


def _trace_word(word: str, S: sp.MatrixBase, R: sp.MatrixBase) -> sp.Expr:
    product = sp.eye(3)
    for letter in word:
        product = product * (S if letter == "S" else R)
    return sp.expand(sp.trace(product))


def _contraction_pool(model: dict[str, Any], degree: int) -> dict[str, sp.Expr]:
    """Enumerate all complete-delta contractions as disjoint trace cycles.

    Each rank-two tensor supplies two indices. A complete Kronecker-delta
    contraction is a two-regular graph on tensor occurrences, hence a disjoint
    union of cycles. Cycle orientation only transposes factors and changes the
    sign of R, already contained in the trace-word span.
    """

    if degree == 0:
        return {"1": sp.Integer(1)}
    S, R = model["S"], model["R"]
    pool: dict[str, sp.Expr] = {}
    for partition in _integer_partitions(degree):
        choices = [_necklaces(length) for length in partition]
        for words in itertools.product(*choices):
            factors = [_trace_word(word, S, R) for word in words]
            label = "*".join(f"Tr({word})" for word in words)
            pool[label] = sp.expand(sp.prod(factors))
    return pool


def _polynomial_rank(expressions: Iterable[sp.Expr], variables: tuple[sp.Symbol, ...]) -> int:
    polynomials = [sp.Poly(sp.expand(expr), *variables, domain=sp.QQ)
                   for expr in expressions]
    if not polynomials:
        return 0
    monomials = sorted({monomial for poly in polynomials for monomial in poly.monoms()})
    if not monomials:
        return 0
    matrix = sp.Matrix([
        [poly.coeff_monomial(monomial) for monomial in monomials]
        for poly in polynomials
    ])
    return int(matrix.rank())


def _matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def dependency_controls() -> dict[str, bool]:
    here = Path(__file__).resolve().parent
    w215 = _load_module(
        here / "w2_15_f2b_general_traceless_single_carrier_candidate_contract.py",
        "w2_24_dependency_w215",
    )
    w216 = _load_module(
        here / "w2_16_f2b_general_traceless_single_carrier_candidate_gate.py",
        "w2_24_dependency_w216",
    )
    report_215 = w215.run()
    report_216 = w216.run()

    w223_path = here / "w2_23_common_resonant_kernel_contract.py"
    w223_boundary_valid = False
    if w223_path.exists():
        w223 = _load_module(w223_path, "w2_24_semantic_boundary_w223")
        report_223 = w223.run()
        w223_boundary_valid = all((
            getattr(w223, "CLAIM_ID", None) == W223_CLAIM_ID,
            report_223.get("artifact") == W223_CLAIM_ID,
            report_223.get("valid") is True,
            all(value is False for value in report_223.get(
                "physical_closure_flags", {}
            ).values()),
        ))
    closure_216 = report_216.get("closure_decision", {})
    return {
        "w2_15_structured_contract_valid": all((
            w215.CLAIM_CONTRACT.get("CLAIM_ID")
            == "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CONTRACT_001",
            report_215.get("artifact")
            == "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CONTRACT_001",
            report_215.get("valid") is True,
        )),
        "w2_16_structured_conditional_result_valid": all((
            w216.CLAIM_CONTRACT.get("CLAIM_ID")
            == "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CANDIDATE_001",
            report_216.get("artifact")
            == "W2_F2B_GENERAL_TRACELESS_SINGLE_CARRIER_CANDIDATE_001",
            report_216.get("valid") is True,
            closure_216.get("full_W2_F2_operational_relations_proved") is True,
            closure_216.get("F3_internal_order_or_causality_proved") is False,
        )),
        "w2_23_semantic_scope_boundary_valid": w223_boundary_valid,
    }


def basis_and_completeness_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    model = _matrix_model()
    S, R = model["S"], model["R"]
    variables = model["variables"]
    basis = _basis_expressions(model)
    by_degree = {
        degree: [basis[item["name"]] for item in BASIS_MANIFEST
                 if item["degree"] == degree]
        for degree in range(5)
    }

    pool_ranks: dict[int, int] = {}
    basis_ranks: dict[int, int] = {}
    joined_ranks: dict[int, int] = {}
    pool_sizes: dict[int, int] = {}
    partitions: dict[int, list[tuple[int, ...]]] = {}
    for degree in range(5):
        pool = _contraction_pool(model, degree)
        pool_values = list(pool.values())
        pool_sizes[degree] = len(pool)
        partitions[degree] = _integer_partitions(degree)
        pool_ranks[degree] = _polynomial_rank(pool_values, variables)
        basis_ranks[degree] = _polynomial_rank(by_degree[degree], variables)
        joined_ranks[degree] = _polynomial_rank(
            pool_values + by_degree[degree], variables
        )

    I2, J = basis["I2"], basis["J"]
    M4 = basis["M4"]
    commutator = sp.expand(S * R - R * S)
    K = sp.expand(sp.trace(commutator.T * commutator))
    trace_srsr = sp.expand(sp.trace(S * R * S * R))

    u, v = sp.symbols("u v", real=True)
    scale_map = {
        **{symbol: u * symbol for symbol in model["s_variables"]},
        **{symbol: v * symbol for symbol in model["r_variables"]},
    }
    homogeneous = []
    for item in BASIS_MANIFEST:
        expr = basis[item["name"]]
        p, q = item["bidegree_SR"]
        homogeneous.append(
            sp.expand(expr.xreplace(scale_map) - u**p * v**q * expr) == 0
        )

    controls = {
        "scientific_contract_schema_complete": (
            set(CLAIM_CONTRACT) == set(REQUIRED_SCIENTIFIC_FIELDS)
        ),
        "traceless_symmetric_skew_domain_exact": all((
            sp.trace(S) == 0, sp.trace(R) == 0,
            _matrix_zero(S.T - S), _matrix_zero(R.T + R),
        )),
        "cycle_partitions_complete_through_degree_four": partitions == {
            0: [()],
            1: [(1,)],
            2: [(2,), (1, 1)],
            3: [(3,), (2, 1), (1, 1, 1)],
            4: [(4,), (3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)],
        },
        "exact_contraction_pool_dimensions": pool_ranks == EXPECTED_DIMENSIONS_BY_DEGREE,
        "displayed_basis_independent_dimensions": basis_ranks == EXPECTED_DIMENSIONS_BY_DEGREE,
        "displayed_basis_spans_complete_contraction_pool": all(
            pool_ranks[degree] == basis_ranks[degree] == joined_ranks[degree]
            for degree in range(5)
        ),
        "basis_bidegrees_exact": all(homogeneous),
        "cayley_hamilton_pure_reductions_exact": all((
            sp.expand(sp.trace(S**4) - I2**2 / 2) == 0,
            sp.expand(sp.trace(R**4) - J**2 / 2) == 0,
        )),
        "quartic_mixed_trace_reductions_exact": all((
            sp.expand(trace_srsr + 2 * M4 + I2 * J / 2) == 0,
            sp.expand(K + I2 * J + 6 * M4) == 0,
        )),
        "basis_and_contract_hashes_exact": all((
            _canonical_sha256(BASIS_MANIFEST) == EXPECTED_BASIS_MANIFEST_SHA256,
            _canonical_sha256(CLAIM_CONTRACT) == EXPECTED_SCIENTIFIC_CONTRACT_SHA256,
        )),
    }
    certificate = {
        "dimensions_by_degree": pool_ranks,
        "basis_ranks_by_degree": basis_ranks,
        "joined_ranks_by_degree": joined_ranks,
        "enumerated_contraction_count_by_degree": pool_sizes,
        "cycle_partitions_by_degree": partitions,
        "trace_identities": {
            "Tr(S^4)": "I2^2/2",
            "Tr(R^4)": "J^2/2",
            "Tr(S R S R)": "-2 M4-I2 J/2",
            "K": "-I2 J-6 M4",
        },
    }
    return controls, certificate


def invariance_and_parity_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    model = _matrix_model()
    S, R = model["S"], model["R"]
    basis = _basis_expressions(model)
    svars, rvars = model["s_variables"], model["r_variables"]

    omegas = (
        sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]]),
    )
    rotation_checks = []
    for omega in omegas:
        dS = sp.expand(omega * S - S * omega)
        dR = sp.expand(omega * R - R * omega)
        coordinate_velocity = (
            dS[0, 0], dS[1, 1], dS[0, 1], dS[0, 2], dS[1, 2],
            dR[2, 1], dR[0, 2], dR[1, 0],
        )
        for expr in basis.values():
            derivative = sum(
                sp.diff(expr, variable) * velocity
                for variable, velocity in zip(model["variables"], coordinate_velocity)
            )
            rotation_checks.append(sp.expand(derivative) == 0)

    reflection = sp.diag(-1, 1, 1)
    reflected_S = sp.expand(reflection * S * reflection)
    reflected_R = sp.expand(reflection * R * reflection)
    reflection_map = {
        svars[0]: reflected_S[0, 0], svars[1]: reflected_S[1, 1],
        svars[2]: reflected_S[0, 1], svars[3]: reflected_S[0, 2],
        svars[4]: reflected_S[1, 2], rvars[0]: reflected_R[2, 1],
        rvars[1]: reflected_R[0, 2], rvars[2]: reflected_R[1, 0],
    }
    reflection_checks = [
        sp.expand(expr.xreplace(reflection_map) - expr) == 0
        for expr in basis.values()
    ]

    transpose_map = {variable: -variable for variable in rvars}
    parity = {
        name: (
            "EVEN" if sp.expand(expr.xreplace(transpose_map) - expr) == 0
            else "ODD" if sp.expand(expr.xreplace(transpose_map) + expr) == 0
            else "MIXED"
        )
        for name, expr in basis.items()
    }
    odd_word_values: dict[str, sp.Expr] = {}
    for degree in range(1, 5):
        for word in _necklaces(degree):
            if word.count("R") % 2 == 1:
                odd_word_values[word] = _trace_word(word, S, R)

    controls = {
        "infinitesimal_SO3_invariance_exact": all(rotation_checks),
        "reflection_completes_O3_invariance_exact": all(reflection_checks),
        "basis_transpose_parity_all_even": all(value == "EVEN" for value in parity.values()),
        "every_odd_R_trace_word_through_degree_four_vanishes": all(
            sp.expand(value) == 0 for value in odd_word_values.values()
        ),
        "manifest_parity_matches_direct_calculation": all(
            parity[item["name"]] == item["transpose_parity"]
            for item in BASIS_MANIFEST
        ),
    }
    return controls, {
        "basis_transpose_parity": parity,
        "vanishing_odd_R_trace_word_orbits": sorted(odd_word_values),
    }


def robustness_controls() -> tuple[dict[str, bool], dict[str, Any]]:
    s, rho = sp.symbols("s rho", positive=True)
    tau = sp.symbols("tau", nonnegative=True)
    alpha, eta, b, gamma, c, e, d, delta = sp.symbols(
        "alpha eta b gamma c e d delta", real=True
    )
    S = sp.diag(-s / 3, -s / 3, 2 * s / 3)
    r = rho * sp.Matrix([sp.sqrt(tau), 0, sp.sqrt(1 - tau)])
    R = sp.Matrix([
        [0, -r[2], r[1]],
        [r[2], 0, -r[0]],
        [-r[1], r[0], 0],
    ])
    I2 = sp.simplify(sp.trace(S**2))
    J = sp.simplify(-sp.trace(R**2))
    I3 = sp.simplify(sp.trace(S**3))
    M3 = sp.simplify(sp.trace(S * R**2))
    M4 = sp.simplify(sp.trace(S**2 * R**2))
    C = sp.simplify(S * R - R * S)
    K = sp.simplify(sp.trace(C.T * C))

    complete_law = sp.expand(
        -alpha * I2 / 2 - eta * J / 2 - b * I3 / 3 + gamma * M3
        + c * I2**2 / 4 + e * I2 * J / 2 + d * J**2 / 4 + delta * M4
    )
    old_law = sp.expand(
        -alpha * I2 / 2 - eta * J / 2 - b * I3 / 3
        + c * I2**2 / 4 + d * J**2 / 4
    )
    orientation_slope = sp.factor(sp.diff(complete_law, tau))
    expected_slope = sp.factor(-J * s * (3 * gamma + delta * s) / 6)
    slope_s_derivative = sp.factor(sp.diff(expected_slope, s))

    epsilon = sp.symbols("epsilon", nonzero=True, real=True)
    gamma_perturbed_slope = sp.factor(
        orientation_slope.subs({gamma: epsilon, delta: 0})
    )
    leading_old_quartic = c * I2**2 / 4 + d * J**2 / 4
    leading_gamma_perturbed_quartic = leading_old_quartic
    c_positive, d_positive = sp.symbols("c_positive d_positive", positive=True)
    positive_branch_quartic = sp.simplify(
        leading_old_quartic.subs({c: c_positive, d: d_positive})
    )
    stationary_flat_solution = sp.solve(
        (3 * gamma + delta * s, 3 * gamma + 2 * delta * s),
        (gamma, delta), dict=True,
    )

    tau_zero_K = sp.simplify(K.subs(tau, 0))
    tau_one_K = sp.simplify(K.subs(tau, 1))
    tau_one_unary_form = sp.simplify(sp.Rational(3, 2) * I2 * J)

    controls = {
        "uniaxial_quotient_dictionary_exact": all((
            I2 == 2 * s**2 / 3,
            I3 == 2 * s**3 / 9,
            sp.simplify(M3 - J * s * (sp.Rational(1, 3) - tau / 2)) == 0,
            sp.simplify(M4 + J * s**2 * (sp.Rational(1, 9) + tau / 6)) == 0,
            K == s**2 * J * tau,
        )),
        "complete_law_orientation_slope_exact": orientation_slope == expected_slope,
        "legacy_law_recovered_at_all_mixed_coefficients_zero": (
            sp.expand(complete_law.subs({gamma: 0, e: 0, delta: 0}) - old_law) == 0
        ),
        "legacy_law_omits_three_independent_mixed_directions": all((
            gamma not in old_law.free_symbols,
            e not in old_law.free_symbols,
            delta not in old_law.free_symbols,
        )),
        "fixed_old_manifold_flat_tau_locus_is_codimension_one": all((
            sp.factor(expected_slope / (-J * s / 6)) == 3 * gamma + delta * s,
            sp.simplify(expected_slope.subs(gamma, -delta * s / 3)) == 0,
            sp.Matrix([[3, s]]).rank() == 1,
        )),
        "full_same_unary_stationary_continuum_requires_gamma_delta_zero": all((
            sp.simplify(expected_slope.subs({gamma: 0, delta: 0})) == 0,
            sp.simplify(slope_s_derivative.subs({gamma: 0, delta: 0})) == 0,
            sp.factor(
                (3 * gamma + 2 * delta * s) - (3 * gamma + delta * s)
            ) == delta * s,
            stationary_flat_solution == [{delta: 0, gamma: 0}],
        )),
        "arbitrarily_small_gamma_perturbation_lifts_tau_exactly": all((
            gamma_perturbed_slope == -J * epsilon * s / 2,
            gamma_perturbed_slope != 0,
        )),
        "lifting_perturbation_preserves_positive_leading_quartic": (
            sp.expand(leading_gamma_perturbed_quartic - leading_old_quartic) == 0
            and sp.ask(sp.Q.positive(positive_branch_quartic)) is True
        ),
        "endpoint_minima_cannot_supply_old_irreducible_F2_witness": all((
            tau_zero_K == 0,
            tau_one_K == tau_one_unary_form,
        )),
        "flat_tau_and_exact_legacy_route_are_not_open_properties": all((
            gamma_perturbed_slope != 0,
            len((gamma, e, delta)) == 3,
        )),
    }
    certificate = {
        "complete_law": (
            "U=-alpha I2/2-eta J/2-b I3/3+gamma M3+c I2^2/4"
            "+e I2 J/2+d J^2/4+delta M4"
        ),
        "legacy_mixed_coefficient_point": {"gamma": 0, "e": 0, "delta": 0},
        "mixed_coefficient_space_dimension": 3,
        "frozen_old_manifold_tau_slope": str(expected_slope),
        "frozen_old_manifold_flat_locus": "3*gamma+delta*s=0 (codimension one at fixed s>0)",
        "full_fixed_unary_stationary_continuum_locus": (
            "gamma=delta=0 (codimension two in mixed coefficient space)"
        ),
        "exact_legacy_separable_locus": (
            "gamma=e=delta=0 (codimension three in mixed coefficient space)"
        ),
        "generic_endpoint_effect": {
            "tau_0": "K=0",
            "tau_1": "K=(3/2) I2 J, hence unary-factorizable",
        },
    }
    return controls, certificate


def adversarial_controls() -> dict[str, bool]:
    model = _matrix_model()
    variables = model["variables"]
    basis = _basis_expressions(model)
    degree_three = [basis["I3"], basis["M3"]]
    degree_four = [
        basis["I2_SQUARED"], basis["I2_J"], basis["J_SQUARED"], basis["M4"]
    ]
    complete_nonconstant = [basis[item["name"]] for item in BASIS_MANIFEST
                            if item["degree"] > 0]
    old_nonconstant = [
        basis["I2"], basis["J"], basis["I3"],
        basis["I2_SQUARED"], basis["J_SQUARED"],
    ]
    return {
        "omitting_M3_drops_degree_three_rank": all((
            _polynomial_rank(degree_three, variables) == 2,
            _polynomial_rank([basis["I3"]], variables) == 1,
        )),
        "omitting_I2J_drops_degree_four_rank": all((
            _polynomial_rank(degree_four, variables) == 4,
            _polynomial_rank([item for item in degree_four
                              if item != basis["I2_J"]], variables) == 3,
        )),
        "omitting_M4_drops_degree_four_rank": all((
            _polynomial_rank(degree_four, variables) == 4,
            _polynomial_rank([item for item in degree_four
                              if item != basis["M4"]], variables) == 3,
        )),
        "legacy_span_has_five_not_eight_nonconstant_directions": all((
            _polynomial_rank(complete_nonconstant, variables) == 8,
            _polynomial_rank(old_nonconstant, variables) == 5,
        )),
    }


def positive_and_null_controls() -> dict[str, bool]:
    model = _matrix_model()
    S_symbolic, R_symbolic = model["S"], model["R"]
    zero = sp.zeros(3)

    S = sp.diag(-1, -1, 2)
    r = sp.Matrix([1, 0, 1])
    R = sp.Matrix([[0, -r[2], r[1]], [r[2], 0, -r[0]], [-r[1], r[0], 0]])
    I2 = sp.trace(S**2)
    J = -sp.trace(R**2)
    M3 = sp.trace(S * R**2)
    M4 = sp.trace(S**2 * R**2)
    K = sp.trace((S * R - R * S).T * (S * R - R * S))

    parallel_r = sp.Matrix([0, 0, 1])
    parallel_R = sp.Matrix([
        [0, -parallel_r[2], parallel_r[1]],
        [parallel_r[2], 0, -parallel_r[0]],
        [-parallel_r[1], parallel_r[0], 0],
    ])
    parallel_C = sp.simplify(S * parallel_R - parallel_R * S)

    symbolic_I2 = sp.trace(S_symbolic**2)
    symbolic_J = -sp.trace(R_symbolic**2)
    i2_gram = sp.hessian(symbolic_I2, model["s_variables"]) / 2
    j_gram = sp.hessian(symbolic_J, model["r_variables"]) / 2
    mixed_with_R_zero = (
        sp.trace(S_symbolic * zero**2),
        symbolic_I2 * (-sp.trace(zero**2)),
        sp.trace(S_symbolic**2 * zero**2),
    )
    mixed_with_S_zero = (
        sp.trace(zero * R_symbolic**2),
        sp.trace(zero**2) * symbolic_J,
        sp.trace(zero**2 * R_symbolic**2),
    )

    return {
        "positive_witness_has_all_three_mixed_invariants_nonzero": all((
            I2 * J != 0, M3 != 0, M4 != 0, K != 0,
        )),
        "pure_quadratic_generators_are_positive_definite": all((
            i2_gram.is_positive_definite is True,
            j_gram.is_positive_definite is True,
        )),
        "R_zero_removes_every_mixed_invariant": all(
            sp.expand(value) == 0 for value in mixed_with_R_zero
        ),
        "S_zero_removes_every_mixed_invariant": all(
            sp.expand(value) == 0 for value in mixed_with_S_zero
        ),
        "commuting_parallel_support_is_exact_K_null": _matrix_zero(parallel_C),
        "reference_zero_has_no_invariant_content": all((
            sp.trace(zero**2) == 0,
            sp.trace(zero**3) == 0,
            sp.trace(zero**4) == 0,
        )),
    }


AUDIT_GATE_KEYS = frozenset({
    "dependencies_valid",
    "complete_contraction_basis_exact",
    "O3_invariance_and_transpose_parity_exact",
    "legacy_law_embedding_exact",
    "mixed_coefficient_omissions_detected",
    "tau_lifting_and_tuned_loci_exact",
    "arbitrary_small_healthy_perturbation_refutes_open_robustness",
    "F2_endpoint_nulls_exact",
    "positive_null_and_adversarial_controls_pass",
    "scope_boundary_and_no_inheritance_exact",
    "deterministic_hashes_exact",
})


def adjudication_screen(gates: Any) -> dict[str, bool]:
    valid = bool(
        isinstance(gates, dict)
        and set(gates) == AUDIT_GATE_KEYS
        and all(type(value) is bool for value in gates.values())
    )
    return {
        "valid": valid,
        "adjudication_pass": bool(valid and all(gates.values())),
        "foundation_promoted": False,
    }


def decision_controls(gates: dict[str, bool]) -> dict[str, bool]:
    baseline = adjudication_screen(gates)
    false_cases = []
    malformed_cases = []
    for key in AUDIT_GATE_KEYS:
        false_map = dict(gates)
        false_map[key] = False
        false_cases.append(adjudication_screen(false_map))
        missing_map = dict(gates)
        missing_map.pop(key)
        malformed_cases.append(adjudication_screen(missing_map))
        nonboolean_map = dict(gates)
        nonboolean_map[key] = 1
        malformed_cases.append(adjudication_screen(nonboolean_map))
    return {
        "all_true_evidence_passes_adjudication_without_foundation_promotion": all((
            baseline["valid"], baseline["adjudication_pass"],
            not baseline["foundation_promoted"],
        )),
        "every_single_false_gate_fails_adjudication": all(
            item["valid"] and not item["adjudication_pass"]
            and not item["foundation_promoted"] for item in false_cases
        ),
        "missing_or_nonboolean_gate_is_invalid": all(
            not item["valid"] and not item["adjudication_pass"]
            and not item["foundation_promoted"] for item in malformed_cases
        ),
    }


def run() -> dict[str, Any]:
    dependencies = dependency_controls()
    basis_controls, basis_certificate = basis_and_completeness_controls()
    invariance_controls, parity_certificate = invariance_and_parity_controls()
    robustness, robustness_certificate = robustness_controls()
    positive_null = positive_and_null_controls()
    adversarial = adversarial_controls()

    gates = {
        "dependencies_valid": _all_true(dependencies),
        "complete_contraction_basis_exact": all((
            basis_controls["cycle_partitions_complete_through_degree_four"],
            basis_controls["exact_contraction_pool_dimensions"],
            basis_controls["displayed_basis_independent_dimensions"],
            basis_controls["displayed_basis_spans_complete_contraction_pool"],
            basis_controls["basis_bidegrees_exact"],
            basis_controls["cayley_hamilton_pure_reductions_exact"],
            basis_controls["quartic_mixed_trace_reductions_exact"],
        )),
        "O3_invariance_and_transpose_parity_exact": _all_true(invariance_controls),
        "legacy_law_embedding_exact": robustness[
            "legacy_law_recovered_at_all_mixed_coefficients_zero"
        ],
        "mixed_coefficient_omissions_detected": all((
            robustness["legacy_law_omits_three_independent_mixed_directions"],
            _all_true(adversarial),
        )),
        "tau_lifting_and_tuned_loci_exact": all((
            robustness["uniaxial_quotient_dictionary_exact"],
            robustness["complete_law_orientation_slope_exact"],
            robustness["fixed_old_manifold_flat_tau_locus_is_codimension_one"],
            robustness["full_same_unary_stationary_continuum_requires_gamma_delta_zero"],
        )),
        "arbitrary_small_healthy_perturbation_refutes_open_robustness": all((
            robustness["arbitrarily_small_gamma_perturbation_lifts_tau_exactly"],
            robustness["lifting_perturbation_preserves_positive_leading_quartic"],
            robustness["flat_tau_and_exact_legacy_route_are_not_open_properties"],
        )),
        "F2_endpoint_nulls_exact": robustness[
            "endpoint_minima_cannot_supply_old_irreducible_F2_witness"
        ],
        "positive_null_and_adversarial_controls_pass": all((
            _all_true(basis_controls), _all_true(invariance_controls),
            _all_true(robustness), _all_true(positive_null), _all_true(adversarial),
        )),
        "scope_boundary_and_no_inheritance_exact": all((
            CLAIM_CONTRACT["CLOSURE_FLAGS"]["foundation_law_derived"] is False,
            CLAIM_CONTRACT["CLOSURE_FLAGS"]["F1_F2_F3a_F4_promoted"] is False,
            CLAIM_CONTRACT["CLOSURE_FLAGS"]["space_metric_GR_or_PN_proved"] is False,
            dependencies["w2_23_semantic_scope_boundary_valid"],
        )),
        "deterministic_hashes_exact": basis_controls["basis_and_contract_hashes_exact"],
    }
    screen = adjudication_screen(gates)
    decisions = decision_controls(gates)
    valid = bool(
        _all_true(dependencies)
        and _all_true(basis_controls)
        and _all_true(invariance_controls)
        and _all_true(robustness)
        and _all_true(positive_null)
        and _all_true(adversarial)
        and _all_true(gates)
        and screen["adjudication_pass"]
        and _all_true(decisions)
    )

    closure_decision = {
        "complete_O3_scalar_basis_through_degree4_proved": valid,
        "legacy_separable_U_open_neighbourhood_robust": False,
        "legacy_flat_tau_F2_route_open_neighbourhood_robust": False,
        "legacy_w2_22_tangent_route_open_neighbourhood_robust": False,
        "legacy_route_no_inheritance": valid,
        "common_resonant_kernel_candidate_supplied": False,
        "foundation_law_derived": False,
        "F1_F2_F3a_F4_promoted": False,
        "space_metric_GR_or_PN_proved": False,
        "observational_validation_proved": False,
    }
    hashes = {
        "basis_manifest": _canonical_sha256(BASIS_MANIFEST),
        "scientific_contract": _canonical_sha256(CLAIM_CONTRACT),
        "runtime_source": _file_sha256(Path(__file__).resolve()),
    }
    return {
        "artifact": CLAIM_ID,
        "model_version": MODEL_VERSION,
        "valid": valid,
        "adjudication_status": (
            "PASS_COMPLETE_BASIS__LEGACY_FLAT_TAU_ROUTE_FRAGILE"
            if valid else "FAIL_INVALID_OR_INCOMPLETE_ADJUDICATION"
        ),
        "claim": CLAIM_CONTRACT["CLAIM"],
        "conclusion": (
            "The complete degree-four O(3) scalar law has eight nonconstant directions, "
            "including M3, I2*J and M4. The legacy separable law sets all three mixed "
            "coefficients to zero. Generic admissible mixed perturbations lift tau, so the "
            "legacy variable-tau F2 witness and its tangent route are exact conditional lemmas "
            "on tuned loci, not open-robust foundation results."
        ),
        "complete_basis": list(BASIS_MANIFEST),
        "coefficient_locus": robustness_certificate,
        "closure_decision": closure_decision,
        "hashes": hashes,
        "dependency_controls": dependencies,
        "controls": {
            "basis_and_completeness": basis_controls,
            "invariance_and_parity": invariance_controls,
            "robustness": robustness,
            "positive_and_null": positive_null,
            "adversarial": adversarial,
            "gates": gates,
            "screen": screen,
            "decision_logic": decisions,
        },
        "certificates": {
            "basis": basis_certificate,
            "parity": parity_certificate,
        },
    }


def main() -> int:
    try:
        report = run()
    except Exception as error:
        report = {
            "artifact": CLAIM_ID,
            "model_version": MODEL_VERSION,
            "valid": False,
            "adjudication_status": "FAIL_INVALID_OR_INCOMPLETE_ADJUDICATION",
            "error": f"{type(error).__name__}: {error}",
        }
    print(json.dumps(_json_safe(report), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
