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
        self.assertFalse(unresolved_edges[0].resolved)


if __name__ == "__main__":
    unittest.main()
