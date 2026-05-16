import json
import unittest
from pathlib import Path

from backend.app.service import ExplorerService


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "sample_repo"


class ExplorerServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ExplorerService(FIXTURE_ROOT)
        self.target_file = FIXTURE_ROOT / "pkg" / "main.py"

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

    def test_expand_node_returns_incremental_graph(self) -> None:
        delta = self.service.expand_node("pkg/worker.py::Worker.run").to_dict()
        node_ids = {node["symbol_id"] for node in delta["nodes"]}

        self.assertEqual(delta["symbol_id"], "pkg/worker.py::Worker.run")
        self.assertIn("pkg/worker.py::Worker.normalize", node_ids)
        self.assertNotIn("pkg/main.py::start", node_ids)


if __name__ == "__main__":
    unittest.main()
