import unittest
from pathlib import Path

from backend.analyzer.file_analyzer import analyze_file
from backend.indexer.symbol_index import SymbolIndex


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "sample_repo"


class AnalyzerTests(unittest.TestCase):
    def test_builds_direct_function_and_cross_file_edges(self) -> None:
        index = SymbolIndex.build(FIXTURE_ROOT)
        graph = analyze_file(
            repo_root=FIXTURE_ROOT,
            target_file=FIXTURE_ROOT / "pkg" / "main.py",
            symbol_index=index,
        )

        center_ids = set(graph.center_symbol_ids)
        self.assertEqual(center_ids, {"pkg/main.py::start"})

        node_ids = {node.symbol_id for node in graph.nodes}
        self.assertIn("pkg/helpers.py::helper", node_ids)
        self.assertIn("pkg/worker.py::Worker.run", node_ids)

        edges = {(edge.caller_id, edge.callee_id, edge.resolved) for edge in graph.edges}
        self.assertIn(("pkg/main.py::start", "pkg/helpers.py::helper", True), edges)
        self.assertIn(("pkg/main.py::start", "pkg/worker.py::Worker.run", True), edges)

    def test_resolves_imported_constructor_calls_without_marking_them_unresolved(self) -> None:
        index = SymbolIndex.build(FIXTURE_ROOT)
        graph = analyze_file(
            repo_root=FIXTURE_ROOT,
            target_file=FIXTURE_ROOT / "pkg" / "main.py",
            symbol_index=index,
        )

        constructor_edges = [edge for edge in graph.edges if edge.call_expr == "Worker"]
        self.assertEqual(len(constructor_edges), 1)
        self.assertEqual(constructor_edges[0].status, "resolved")
        self.assertEqual(constructor_edges[0].reason, "constructor_call")
        self.assertEqual(constructor_edges[0].callee_id, "pkg/worker.py::Worker")
        self.assertNotIn(constructor_edges[0].callee_id, graph.unresolved_ids)

    def test_resolves_self_method_calls(self) -> None:
        index = SymbolIndex.build(FIXTURE_ROOT)
        graph = analyze_file(
            repo_root=FIXTURE_ROOT,
            target_file=FIXTURE_ROOT / "pkg" / "worker.py",
            symbol_index=index,
        )

        edges = {(edge.caller_id, edge.callee_id, edge.resolved) for edge in graph.edges}
        self.assertIn(("pkg/worker.py::Worker.run", "pkg/worker.py::Worker.normalize", True), edges)

    def test_marks_unresolved_dynamic_call_nodes(self) -> None:
        repo_root = FIXTURE_ROOT / "dynamic_case"
        index = SymbolIndex.build(repo_root)
        graph = analyze_file(
            repo_root=repo_root,
            target_file=repo_root / "main.py",
            symbol_index=index,
        )

        unresolved_edges = [edge for edge in graph.edges if not edge.resolved]
        self.assertEqual(len(unresolved_edges), 1)
        self.assertEqual(graph.unresolved_ids, [unresolved_edges[0].callee_id])

    def test_duplicate_symbol_names_do_not_resolve_ambiguously(self) -> None:
        repo_root = FIXTURE_ROOT / "duplicates_case"
        index = SymbolIndex.build(repo_root)
        graph = analyze_file(
            repo_root=repo_root,
            target_file=repo_root / "main.py",
            symbol_index=index,
        )

        unresolved_edges = [edge for edge in graph.edges if edge.call_expr == "shared"]
        self.assertEqual(len(unresolved_edges), 1)
        self.assertEqual(unresolved_edges[0].status, "ambiguous")
        self.assertEqual(unresolved_edges[0].reason, "ambiguous_top_level")

    def test_resolves_dotted_module_alias_calls(self) -> None:
        repo_root = FIXTURE_ROOT
        index = SymbolIndex.build(repo_root)
        graph = analyze_file(
            repo_root=repo_root,
            target_file=repo_root / "alias_case" / "main.py",
            symbol_index=index,
        )

        matching_edges = [edge for edge in graph.edges if edge.call_expr == "helpers_mod.helper"]
        self.assertEqual(len(matching_edges), 1)
        self.assertEqual(matching_edges[0].status, "resolved")
        self.assertEqual(matching_edges[0].reason, "module_alias_function")
        self.assertEqual(matching_edges[0].callee_id, "alias_case/helpers.py::helper")

    def test_unresolved_dynamic_calls_include_reason(self) -> None:
        repo_root = FIXTURE_ROOT / "dynamic_case"
        index = SymbolIndex.build(repo_root)
        graph = analyze_file(
            repo_root=repo_root,
            target_file=repo_root / "main.py",
            symbol_index=index,
        )

        unresolved_edge = next(edge for edge in graph.edges if edge.call_expr == "handler")
        self.assertEqual(unresolved_edge.status, "unresolved")
        self.assertEqual(unresolved_edge.reason, "unknown_target")
        self.assertEqual(unresolved_edge.candidate_symbol_ids, [])

    def test_resolves_method_calls_on_values_returned_from_simple_factories(self) -> None:
        repo_root = FIXTURE_ROOT
        index = SymbolIndex.build(repo_root)
        graph = analyze_file(
            repo_root=repo_root,
            target_file=repo_root / "factory_case" / "main.py",
            symbol_index=index,
        )

        edges_by_expr = {edge.call_expr: edge for edge in graph.edges}
        self.assertEqual(edges_by_expr["make_worker"].status, "resolved")
        self.assertEqual(edges_by_expr["make_worker"].reason, "imported_symbol")
        self.assertEqual(edges_by_expr["worker.run"].status, "resolved")
        self.assertEqual(edges_by_expr["worker.run"].reason, "instance_method")
        self.assertEqual(edges_by_expr["worker.run"].callee_id, "factory_case/worker.py::Worker.run")

    def test_resolves_annotated_assignments_before_instance_method_calls(self) -> None:
        repo_root = FIXTURE_ROOT
        index = SymbolIndex.build(repo_root)
        graph = analyze_file(
            repo_root=repo_root,
            target_file=repo_root / "annotated_case" / "main.py",
            symbol_index=index,
        )

        edges_by_expr = {edge.call_expr: edge for edge in graph.edges}
        self.assertEqual(edges_by_expr["Worker"].status, "resolved")
        self.assertEqual(edges_by_expr["worker.run"].status, "resolved")
        self.assertEqual(edges_by_expr["worker.run"].reason, "instance_method")
        self.assertEqual(edges_by_expr["worker.run"].callee_id, "annotated_case/worker.py::Worker.run")


if __name__ == "__main__":
    unittest.main()
