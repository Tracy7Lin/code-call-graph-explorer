from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from backend.core.models import FileGraph


@runtime_checkable
class LanguageAdapter(Protocol):
    language_id: str

    def build_symbol_index(self, repo_root: Path):
        ...

    def analyze_file(self, repo_root: Path, target_file: Path, symbol_index) -> FileGraph:
        ...
