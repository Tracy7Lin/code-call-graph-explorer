from __future__ import annotations

from pathlib import Path

from backend.common.models import FileGraph
from backend.languages.python import PythonLanguageAdapter
from backend.languages.python.indexer.symbol_index import SymbolIndex


class AnalysisPipeline:
    def __init__(self, repo_root: Path, adapter: PythonLanguageAdapter | None = None) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.adapter = adapter or PythonLanguageAdapter()
        self.symbol_index: SymbolIndex = self.adapter.build_symbol_index(self.repo_root)

    def analyze_file(self, target_file: Path) -> FileGraph:
        target_file = Path(target_file).resolve()
        return self.adapter.analyze_file(self.repo_root, target_file, self.symbol_index)
