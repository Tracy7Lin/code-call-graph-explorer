import unittest
from pathlib import Path

from backend.common.models import FileGraph as CompatFileGraph, Symbol as CompatSymbol
from backend.analyzer.framework import (
    build_default_assignment_rules,
    build_default_call_rules,
)
from backend.analyzer.rules_assignment_inference import (
    infer_constructor_assignment,
    infer_factory_assignment,
)
from backend.analyzer.rules_attribute_calls import (
    resolve_class_method,
    resolve_instance_method,
    resolve_module_alias_function,
    resolve_module_function,
    resolve_self_method,
)
from backend.analyzer.rules_name_calls import (
    resolve_ambiguous_import,
    resolve_constructor_call,
    resolve_imported_function,
    resolve_local_function,
    resolve_top_level,
)
from backend.analyzer.types import ResolutionReason, ResolutionStatus
from backend.languages import get_adapter, get_default_adapter, list_adapters
from backend.core.models import FileGraph as CoreFileGraph, Symbol as CoreSymbol
from backend.core.semantics import SharedResolutionReason, SharedResolutionStatus
from backend.languages.python import PythonLanguageAdapter


class ResolutionFrameworkTests(unittest.TestCase):
    def test_resolution_status_and_reason_constants_are_centralized(self) -> None:
        self.assertEqual(ResolutionStatus.RESOLVED, "resolved")
        self.assertEqual(ResolutionStatus.AMBIGUOUS, "ambiguous")
        self.assertEqual(ResolutionReason.CONSTRUCTOR_CALL, "constructor_call")
        self.assertEqual(ResolutionReason.INSTANCE_METHOD, "instance_method")
        self.assertEqual(SharedResolutionStatus.RESOLVED, "resolved")
        self.assertEqual(SharedResolutionReason.CONSTRUCTOR_CALL, "constructor_call")

    def test_default_call_rules_are_registered_in_explicit_order(self) -> None:
        rule_names = [rule.name for rule in build_default_call_rules()]
        self.assertEqual(
            rule_names,
            [
                "local-function",
                "constructor-call",
                "imported-function",
                "ambiguous-import",
                "top-level",
                "self-method",
                "instance-method",
                "module-alias-function",
                "module-function",
                "class-method",
            ],
        )

    def test_default_assignment_rules_are_registered_in_explicit_order(self) -> None:
        rule_names = [rule.name for rule in build_default_assignment_rules()]
        self.assertEqual(
            rule_names,
            [
                "constructor-assignment",
                "factory-assignment",
            ],
        )

    def test_default_call_rules_are_loaded_from_rule_family_modules(self) -> None:
        handlers = [rule.handler for rule in build_default_call_rules()]
        self.assertEqual(
            handlers,
            [
                resolve_local_function,
                resolve_constructor_call,
                resolve_imported_function,
                resolve_ambiguous_import,
                resolve_top_level,
                resolve_self_method,
                resolve_instance_method,
                resolve_module_alias_function,
                resolve_module_function,
                resolve_class_method,
            ],
        )

    def test_default_assignment_rules_are_loaded_from_rule_family_modules(self) -> None:
        handlers = [rule.handler for rule in build_default_assignment_rules()]
        self.assertEqual(
            handlers,
            [
                infer_constructor_assignment,
                infer_factory_assignment,
            ],
        )

    def test_python_language_adapter_boundary_exists(self) -> None:
        adapter = PythonLanguageAdapter()
        self.assertEqual(adapter.language_id, "python")
        self.assertTrue(callable(adapter.build_symbol_index))
        self.assertTrue(callable(adapter.analyze_file))
        self.assertEqual(adapter.build_symbol_index.__module__, "backend.languages.python")
        self.assertEqual(adapter.analyze_file.__module__, "backend.languages.python")

    def test_canonical_python_packages_exist(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        self.assertTrue((repo_root / "backend" / "languages" / "python" / "analyzer" / "__init__.py").exists())
        self.assertTrue((repo_root / "backend" / "languages" / "python" / "indexer" / "__init__.py").exists())

    def test_language_adapter_registry_exposes_python(self) -> None:
        adapters = list_adapters()
        self.assertIn("python", adapters)
        self.assertIsInstance(get_adapter("python"), PythonLanguageAdapter)
        self.assertIsInstance(get_default_adapter(), PythonLanguageAdapter)

    def test_core_model_path_exists_and_common_models_are_compatibility_exports(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        self.assertTrue((repo_root / "backend" / "core" / "models.py").exists())
        self.assertIs(CoreSymbol, CompatSymbol)
        self.assertIs(CoreFileGraph, CompatFileGraph)

    def test_runtime_modules_import_models_from_core(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        runtime_paths = [
            repo_root / "backend" / "app" / "pipeline.py",
            repo_root / "backend" / "app" / "service.py",
            repo_root / "backend" / "languages" / "types.py",
            repo_root / "backend" / "languages" / "python" / "analyzer" / "collector.py",
            repo_root / "backend" / "languages" / "python" / "analyzer" / "file_analyzer.py",
            repo_root / "backend" / "languages" / "python" / "indexer" / "symbol_index.py",
        ]

        for path in runtime_paths:
            contents = path.read_text(encoding="utf-8")
            self.assertIn("backend.core.models", contents, str(path))
            self.assertNotIn("backend.common.models", contents, str(path))


if __name__ == "__main__":
    unittest.main()
