from __future__ import annotations

from pathlib import Path

from backend.languages.python.analyzer.file_analyzer import analyze_file
from backend.languages.python.indexer.symbol_index import SymbolIndex
from backend.languages.types import LanguageAdapter


class PythonLanguageAdapter(LanguageAdapter):
    language_id = "python"

    def build_symbol_index(self, repo_root: Path) -> SymbolIndex:
        return SymbolIndex.build(repo_root)

    def analyze_file(self, repo_root: Path, target_file: Path, symbol_index: SymbolIndex):
        return analyze_file(repo_root, target_file, symbol_index)
