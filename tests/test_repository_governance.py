import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RepositoryGovernanceTests(unittest.TestCase):
    def test_required_governance_artifacts_exist(self) -> None:
        required_paths = [
            "pyproject.toml",
            "CONTRIBUTING.md",
            "CHANGELOG.md",
            "scripts/dev.py",
            "docs/roadmap.md",
            "docs/project-structure.md",
            ".github/pull_request_template.md",
            ".github/ISSUE_TEMPLATE/bug_report.md",
            ".github/ISSUE_TEMPLATE/feature_request.md",
            ".github/ISSUE_TEMPLATE/config.yml",
        ]

        missing = [path for path in required_paths if not (REPO_ROOT / path).exists()]
        self.assertEqual(missing, [])

    def test_pyproject_declares_project_metadata_and_dev_commands(self) -> None:
        pyproject_path = REPO_ROOT / "pyproject.toml"
        contents = pyproject_path.read_text(encoding="utf-8")

        self.assertIn('name = "python-call-graph-explorer"', contents)
        self.assertIn('version = "0.1.0"', contents)
        self.assertIn('requires-python = ">=3.11"', contents)
        self.assertIn("python -m unittest discover -s tests -v", contents)
        self.assertIn("python run.py", contents)


if __name__ == "__main__":
    unittest.main()
