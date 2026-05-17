from __future__ import annotations

from pathlib import Path

from backend.core.models import FileGraph
from backend.languages import get_adapter, get_default_adapter
from backend.languages.python.indexer.symbol_index import SymbolIndex
from backend.languages.types import LanguageAdapter


class AnalysisPipeline:
    def __init__(self, repo_root: Path, adapter: LanguageAdapter | None = None, language_id: str | None = None) -> None:
        self.repo_root = Path(repo_root).resolve()
        selected_adapter = adapter
        if selected_adapter is None and language_id is not None:
            selected_adapter = get_adapter(language_id)
        if selected_adapter is None:
            selected_adapter = get_default_adapter()
        self.adapter = selected_adapter
        self.language_id = self.adapter.language_id
        self.symbol_index: SymbolIndex = self.adapter.build_symbol_index(self.repo_root)

    def analyze_file(self, target_file: Path) -> FileGraph:
        target_file = Path(target_file).resolve()
        return self.adapter.analyze_file(self.repo_root, target_file, self.symbol_index)
