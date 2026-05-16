from __future__ import annotations

from backend.languages.python import PythonLanguageAdapter
from backend.languages.types import LanguageAdapter


_REGISTERED_ADAPTERS: dict[str, LanguageAdapter] = {
    "python": PythonLanguageAdapter(),
}


def list_adapters() -> list[str]:
    return sorted(_REGISTERED_ADAPTERS.keys())


def get_adapter(language_id: str) -> LanguageAdapter:
    try:
        return _REGISTERED_ADAPTERS[language_id]
    except KeyError as exc:
        raise KeyError(f"Unsupported language adapter: {language_id}") from exc


def get_default_adapter() -> LanguageAdapter:
    return get_adapter("python")
