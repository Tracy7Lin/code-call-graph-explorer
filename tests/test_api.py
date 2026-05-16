import json
import unittest
from pathlib import Path

from backend.app.pipeline import AnalysisPipeline
from backend.app.service import ExplorerService


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "sample_repo"


class ExplorerServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ExplorerService(FIXTURE_ROOT)
        self.target_file = FIXTURE_ROOT / "pkg" / "main.py"

    def test_service_uses_analysis_pipeline_boundary(self) -> None:
        self.assertIsInstance(self.service.pipeline, AnalysisPipeline)
        self.assertEqual(self.service.pipeline.adapter.language_id, "python")
        self.assertEqual(self.service.pipeline.__class__.__module__, "backend.app.pipeline")
        self.assertEqual(self.service.pipeline.adapter.__class__.__module__, "backend.languages.python")
        self.assertEqual(self.service.pipeline.language_id, "python")

    def test_analyze_file_returns_stable_shape(self) -> None:
        payload = self.service.analyze_file(self.target_file).to_dict()
        self.assertEqual(payload["center_file"], "pkg/main.py")
        self.assertIn("nodes", payload)
        self.assertIn("edges", payload)

    def test_node_detail_without_llm_omits_insight(self) -> None:
        graph = self.service.analyze_file(self.target_file)
        detail = self.service.get_node_detail(graph.center_symbol_ids[0], with_llm=False).to_dict()
        self.assertIsNone(detail["insight"])

    def test_node_detail_with_llm_adds_insight_without_mutating_graph(self) -> None:
        before = json.dumps(self.service.analyze_file(self.target_file).to_dict(), sort_keys=True)
        detail = self.service.get_node_detail("pkg/main.py::start", with_llm=True).to_dict()
        after = json.dumps(self.service.analyze_file(self.target_file).to_dict(), sort_keys=True)

        self.assertIsNotNone(detail["insight"])
        self.assertEqual(before, after)
        self.assertIn("advisory_suggestions", detail)

    def test_expand_node_returns_incremental_graph(self) -> None:
        delta = self.service.expand_node("pkg/worker.py::Worker.run").to_dict()
        node_ids = {node["symbol_id"] for node in delta["nodes"]}

        self.assertEqual(delta["symbol_id"], "pkg/worker.py::Worker.run")
        self.assertIn("pkg/worker.py::Worker.normalize", node_ids)
        self.assertNotIn("pkg/main.py::start", node_ids)

    def test_node_detail_includes_structured_edge_metadata(self) -> None:
        detail = self.service.get_node_detail("pkg/main.py::start", with_llm=True).to_dict()

        self.assertIn("outbound_edges", detail)
        helper_edge = next(edge for edge in detail["outbound_edges"] if edge["call_expr"] == "helper")
        self.assertEqual(helper_edge["status"], "resolved")
        self.assertEqual(helper_edge["reason"], "imported_symbol")
        constructor_edge = next(edge for edge in detail["outbound_edges"] if edge["call_expr"] == "Worker")
        self.assertEqual(constructor_edge["status"], "resolved")
        self.assertEqual(constructor_edge["reason"], "constructor_call")

    def test_advisory_suggestions_only_appear_for_uncertain_edges(self) -> None:
        dynamic_service = ExplorerService(FIXTURE_ROOT / "dynamic_case")
        detail = dynamic_service.get_node_detail("main.py::call_dynamic", with_llm=True).to_dict()

        self.assertGreaterEqual(len(detail["advisory_suggestions"]), 1)
        self.assertEqual(detail["advisory_suggestions"][0]["edge_status"], "unresolved")
        self.assertEqual(detail["advisory_suggestions"][0]["candidate_symbol_ids"], [])

    def test_ambiguous_advisory_suggestions_include_candidates(self) -> None:
        duplicate_service = ExplorerService(FIXTURE_ROOT / "duplicates_case")
        detail = duplicate_service.get_node_detail("main.py::call", with_llm=True).to_dict()

        suggestion = detail["advisory_suggestions"][0]
        self.assertEqual(suggestion["edge_status"], "ambiguous")
        self.assertEqual(
            suggestion["candidate_symbol_ids"],
            ["a.py::shared", "b.py::shared"],
        )

    def test_factory_backed_instance_methods_appear_resolved_in_detail(self) -> None:
        factory_service = ExplorerService(FIXTURE_ROOT)
        detail = factory_service.get_node_detail("factory_case/main.py::start", with_llm=True).to_dict()

        method_edge = next(edge for edge in detail["outbound_edges"] if edge["call_expr"] == "worker.run")
        self.assertEqual(method_edge["status"], "resolved")
        self.assertEqual(method_edge["reason"], "instance_method")
        self.assertEqual(method_edge["callee_id"], "factory_case/worker.py::Worker.run")


if __name__ == "__main__":
    unittest.main()
