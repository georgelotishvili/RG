"""Independent fail-closed tests for the public RefG F1 proof package."""
from __future__ import annotations

import ast
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import sympy as sp


HERE = Path(__file__).resolve().parent
PROOF_PATH = HERE / "refg_f1_atemporal_structural_proof.py"
SPEC = importlib.util.spec_from_file_location("refg_public_f1_proof", PROOF_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import public proof: {PROOF_PATH}")
proof = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(proof)


class PublicF1ProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sections = {
            "singleton": proof.strict_singleton_no_go(),
            "equivariant": proof.deterministic_equivariant_fixed_set_no_go(),
            "spectral": proof.atemporal_spectral_construction(),
        }
        cls.report = proof.run_proof()

    def test_nominal_public_result_is_narrow_conditional_pass(self) -> None:
        self.assertEqual(self.report["STATUS"], proof.PASS_STATUS)
        self.assertIs(self.report["AUDIT_VALID"], True)
        self.assertIs(self.report["RAW_CANDIDATE_PASS"], True)
        self.assertIs(self.report["PROMOTED"], True)
        self.assertEqual(
            self.report["CLAIM"],
            "A conditional atemporal structural F1 follows relative to the "
            "explicitly imported Sym_0(3), O(3), quartic-law and argmin primitives.",
        )

    def test_section_check_registries_are_exact_and_all_true(self) -> None:
        expected = {
            "singleton": proof.SINGLETON_CHECK_KEYS,
            "equivariant": proof.EQUIVARIANT_CHECK_KEYS,
            "spectral": proof.SPECTRAL_CHECK_KEYS,
        }
        for name, keys in expected.items():
            with self.subTest(section=name):
                self.assertTrue(
                    proof.exact_true_map(self.sections[name]["checks"], keys)
                )

    def test_audit_and_evidence_registries_are_exact_and_all_true(self) -> None:
        self.assertTrue(
            proof.exact_true_map(self.report["AUDIT_CHECKS"], proof.AUDIT_CHECK_KEYS)
        )
        self.assertTrue(
            proof.exact_true_map(
                self.report["PROMOTION_EVIDENCE"], proof.F1_GATE_KEYS
            )
        )
        self.assertTrue(
            proof.exact_true_map(
                self.report["DECISION_LOGIC_CONTROLS"],
                proof.DECISION_CONTROL_KEYS,
            )
        )

    def test_singleton_positive_and_external_register_controls(self) -> None:
        diagnostics = self.sections["singleton"]["diagnostics"]
        self.assertEqual(diagnostics["state_count"], 1)
        self.assertEqual(diagnostics["deterministic_map_count"], 1)
        self.assertEqual(diagnostics["deterministic_image_sizes"], [1])
        self.assertEqual(diagnostics["normalized_kernel"], "Matrix([[1]])")
        self.assertEqual(diagnostics["density_matrix"], "Matrix([[1]])")
        self.assertEqual(diagnostics["external_binary_register_size"], 2)

    def test_equivariant_fixed_set_exhaustive_controls(self) -> None:
        diagnostics = self.sections["equivariant"]["diagnostics"]
        self.assertEqual(diagnostics["fixed_set_C2_three_states"], [2])
        self.assertEqual(diagnostics["fixed_set_C2_four_states"], [2, 3])
        self.assertGreater(diagnostics["equivariant_map_count_three_states"], 0)
        self.assertGreater(diagnostics["equivariant_map_count_four_states"], 0)
        self.assertGreater(diagnostics["unique_invariant_minimum_controls"], 0)

    def test_spectral_projectors_modes_and_exact_arithmetic(self) -> None:
        diagnostics = self.sections["spectral"]["diagnostics"]
        self.assertEqual(diagnostics["invariant_basis_degree_le_4"], ["I2", "I3", "I2^2"])
        self.assertEqual(diagnostics["projector_ranks"], [1, 2])
        self.assertEqual(diagnostics["orbit_zero_mode_count"], 2)
        self.assertEqual(diagnostics["data_fitted_parameters"], 0)
        self.assertFalse(proof.contains_float(self.sections))

    def test_imports_are_explicit_and_scope_is_entirely_open(self) -> None:
        self.assertEqual(set(proof.IMPORTED_PRIMITIVES), proof.IMPORTED_PRIMITIVE_KEYS)
        self.assertEqual(len(proof.IMPORTED_PRIMITIVES), 9)
        self.assertEqual(
            set(proof.IMPORTED_PRIMITIVES.values()), {"IMPORTED_NOT_DERIVED"}
        )
        self.assertEqual(proof.DATA_FITTED_PARAMETERS, 0)
        self.assertIs(type(proof.DATA_FITTED_PARAMETERS), int)
        self.assertTrue(proof.SCOPE_CEILING)
        self.assertEqual(set(proof.SCOPE_CEILING), proof.SCOPE_CEILING_KEYS)
        self.assertTrue(
            all(type(value) is bool and value is False for value in proof.SCOPE_CEILING.values())
        )

    def test_one_false_gate_is_valid_not_promoted_not_invalid(self) -> None:
        evidence = {key: True for key in proof.F1_GATE_KEYS}
        evidence["intrinsic_differentiation_certified"] = False
        result = proof.adjudicate(evidence, True)
        self.assertEqual(result["STATUS"], proof.NOT_PROMOTED_STATUS)
        self.assertIs(result["AUDIT_VALID"], True)
        self.assertIs(result["RAW_CANDIDATE_PASS"], False)
        self.assertIs(result["PROMOTED"], False)

    def test_invalid_audit_cannot_export_promotion(self) -> None:
        evidence = {key: True for key in proof.F1_GATE_KEYS}
        for invalid_audit in (False, 0, 1, "true", None):
            with self.subTest(audit=invalid_audit):
                result = proof.adjudicate(evidence, invalid_audit)
                self.assertEqual(result["STATUS"], proof.INVALID_STATUS)
                self.assertIs(result["PROMOTED"], False)

    def test_gate_schema_missing_extra_and_nonboolean_fail_closed(self) -> None:
        baseline = {key: True for key in proof.F1_GATE_KEYS}
        for gate in proof.F1_GATE_KEYS:
            missing = dict(baseline)
            missing.pop(gate)
            self.assertEqual(proof.adjudicate(missing, True)["STATUS"], proof.INVALID_STATUS)
            for bad_value in (1, 0, "true", None):
                mutant = dict(baseline)
                mutant[gate] = bad_value
                self.assertEqual(
                    proof.adjudicate(mutant, True)["STATUS"], proof.INVALID_STATUS
                )
        extra = dict(baseline)
        extra["unregistered_weight"] = True
        self.assertEqual(proof.adjudicate(extra, True)["STATUS"], proof.INVALID_STATUS)

    def test_decision_control_registry_missing_and_extra_fail_closed(self) -> None:
        baseline = proof.decision_logic_controls()
        missing = dict(baseline)
        missing.pop(next(iter(proof.DECISION_CONTROL_KEYS)))
        extra = dict(baseline)
        extra["unregistered_control"] = True

        for name, mutant in (("missing", missing), ("extra", extra)):
            with self.subTest(mutant=name), patch.object(
                proof, "decision_logic_controls", return_value=mutant
            ):
                report = proof.run_proof()
                self.assertIs(
                    report["AUDIT_CHECKS"][
                        "decision_logic_positive_negative_invalid_controls"
                    ],
                    False,
                )
                self.assertEqual(report["STATUS"], proof.INVALID_STATUS)
                self.assertIs(report["PROMOTED"], False)

    def test_public_witness_definition_and_selection_are_exact(self) -> None:
        self.assertEqual(
            proof.F1_WITNESS_KINDS,
            (
                "MULTIPLE_INEQUIVALENT_ACCEPTED_QUOTIENT_CLASSES",
                "ONE_ACCEPTED_QUOTIENT_CLASS_WITH_CANONICAL_COEXISTING_NONEXCHANGEABLE_ROLES",
            ),
        )
        self.assertEqual(proof.SELECTED_F1_WITNESS_KIND, proof.F1_WITNESS_KINDS[1])

        with patch.object(
            proof,
            "F1_WITNESS_KINDS",
            ("ONE_ACCEPTED_QUOTIENT_CLASS_WITH_CANONICAL_COEXISTING_NONEXCHANGEABLE_ROLES",),
        ):
            evidence = proof.build_f1_evidence(self.sections)
            self.assertIs(
                evidence["public_definition_accepts_both_witness_kinds"], False
            )
            self.assertIs(proof.adjudicate(evidence, True)["PROMOTED"], False)

    def test_unreferenced_false_section_check_invalidates_the_audit(self) -> None:
        spectral = copy.deepcopy(self.sections["spectral"])
        spectral["checks"][
            "positive_quadratic_null_keeps_undifferentiated_origin"
        ] = False
        with patch.object(
            proof, "atemporal_spectral_construction", return_value=spectral
        ):
            report = proof.run_proof()
        self.assertIs(
            report["AUDIT_CHECKS"]["section_checks_exact_and_all_true"], False
        )
        self.assertEqual(report["STATUS"], proof.INVALID_STATUS)
        self.assertIs(report["PROMOTED"], False)

    def test_nested_symbolic_float_invalidates_the_audit(self) -> None:
        spectral = copy.deepcopy(self.sections["spectral"])
        spectral["diagnostics"]["s_plus"] = (
            sp.Symbol("nested_float_control") + sp.Float("0.1")
        )
        self.assertIs(proof.contains_float(spectral), True)
        with patch.object(
            proof, "atemporal_spectral_construction", return_value=spectral
        ):
            report = proof.run_proof()
        self.assertIs(
            report["AUDIT_CHECKS"][
                "exact_symbolic_outputs_without_floating_tolerance"
            ],
            False,
        )
        self.assertEqual(report["STATUS"], proof.INVALID_STATUS)
        self.assertIs(report["PROMOTED"], False)

    def test_import_and_scope_relabelling_mutants_cannot_promote(self) -> None:
        import_key = next(iter(proof.IMPORTED_PRIMITIVES))
        with patch.dict(
            proof.IMPORTED_PRIMITIVES,
            {import_key: "DERIVED_BY_THIS_PROOF"},
            clear=False,
        ):
            evidence = proof.build_f1_evidence(self.sections)
            self.assertIs(
                evidence["all_registered_primitives_labelled_imported"], False
            )
            self.assertIs(proof.adjudicate(evidence, True)["PROMOTED"], False)

        renamed_imports = dict(proof.IMPORTED_PRIMITIVES)
        renamed_imports.pop(import_key)
        renamed_imports["fabricated_import_key"] = "IMPORTED_NOT_DERIVED"
        with patch.dict(proof.IMPORTED_PRIMITIVES, renamed_imports, clear=True):
            report = proof.run_proof()
            self.assertIs(
                report["AUDIT_CHECKS"]["imported_primitive_registry_exact"], False
            )
            self.assertEqual(report["STATUS"], proof.INVALID_STATUS)
            self.assertIs(report["PROMOTED"], False)

        scope_key = next(iter(proof.SCOPE_CEILING))
        with patch.dict(proof.SCOPE_CEILING, {scope_key: True}, clear=False):
            evidence = proof.build_f1_evidence(self.sections)
            self.assertIs(evidence["scope_ceiling_registry_exactly_false"], False)
            self.assertIs(proof.adjudicate(evidence, True)["PROMOTED"], False)

        renamed_scope = dict(proof.SCOPE_CEILING)
        renamed_scope.pop(scope_key)
        renamed_scope["fabricated_scope_key"] = False
        with patch.dict(proof.SCOPE_CEILING, renamed_scope, clear=True):
            report = proof.run_proof()
            self.assertIs(
                report["AUDIT_CHECKS"]["scope_ceiling_exactly_false"], False
            )
            self.assertEqual(report["STATUS"], proof.INVALID_STATUS)
            self.assertIs(report["PROMOTED"], False)

    def test_mathematical_candidate_failure_is_complete_not_promoted(self) -> None:
        sections = copy.deepcopy(self.sections)
        sections["spectral"]["checks"][
            "unique_nonzero_global_minimum_quotient_orbit_certified"
        ] = False
        evidence = proof.build_f1_evidence(sections)
        result = proof.adjudicate(evidence, True)
        self.assertEqual(result["STATUS"], proof.NOT_PROMOTED_STATUS)
        self.assertIs(result["AUDIT_VALID"], True)
        self.assertIs(result["PROMOTED"], False)

    def test_public_module_has_no_external_or_repository_dependency(self) -> None:
        source = PROOF_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(
                    alias.name.split(".", 1)[0] for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".", 1)[0])
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertNotEqual(node.func.id, "open")
                elif isinstance(node.func, ast.Attribute):
                    self.assertNotIn(
                        node.func.attr,
                        {"open", "read_text", "read_bytes", "write_text", "write_bytes"},
                    )
        self.assertLessEqual(
            imported_roots,
            {"__future__", "itertools", "json", "sys", "typing", "sympy"},
        )
        self.assertEqual(proof.EXTERNAL_FILE_DEPENDENCIES, ())

    def test_standalone_copy_runs_without_repository_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            copied = Path(temporary_directory) / PROOF_PATH.name
            shutil.copy2(PROOF_PATH, copied)
            completed = subprocess.run(
                [sys.executable, str(copied)],
                cwd=temporary_directory,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=60,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads(completed.stdout)
            self.assertEqual(report["STATUS"], proof.PASS_STATUS)
            self.assertIs(report["PROMOTED"], True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
