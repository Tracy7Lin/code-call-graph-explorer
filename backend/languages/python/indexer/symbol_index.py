from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path

from backend.core.models import Symbol


@dataclass(frozen=True)
class ImportRef:
    kind: str
    module: str | None
    name: str


@dataclass
class SymbolIndex:
    repo_root: Path
    symbols_by_id: dict[str, Symbol] = field(default_factory=dict)
    symbols_by_file: dict[str, list[Symbol]] = field(default_factory=dict)
    top_level_by_name: dict[str, list[str]] = field(default_factory=dict)
    methods_by_class: dict[str, dict[str, str]] = field(default_factory=dict)
    classes_by_module: dict[str, dict[str, str]] = field(default_factory=dict)
    imports_by_file: dict[str, dict[str, ImportRef]] = field(default_factory=dict)
    module_aliases_by_file: dict[str, dict[str, str]] = field(default_factory=dict)
    module_to_file: dict[str, str] = field(default_factory=dict)
    factory_return_types: dict[str, str] = field(default_factory=dict)

    @classmethod
    def build(cls, repo_root: Path) -> "SymbolIndex":
        repo_root = Path(repo_root).resolve()
        index = cls(repo_root=repo_root)
        python_files = sorted(path for path in repo_root.rglob("*.py") if "__pycache__" not in path.parts)
        for path in python_files:
            rel_path = index.rel_path(path)
            module_name = index.module_name(path)
            index.module_to_file[module_name] = rel_path
            index.symbols_by_file.setdefault(rel_path, [])
            index.imports_by_file[rel_path] = {}
            index.module_aliases_by_file[rel_path] = {}

        for path in python_files:
            index._scan_file(path)
        for path in python_files:
            index._scan_factory_returns(path)
        return index

    def rel_path(self, path: Path) -> str:
        return str(path.resolve().relative_to(self.repo_root)).replace("\\", "/")

    def module_name(self, path: Path) -> str:
        rel = path.resolve().relative_to(self.repo_root).with_suffix("")
        parts = list(rel.parts)
        if parts and parts[-1] == "__init__":
            parts = parts[:-1]
        return ".".join(parts)

    def get_symbol(self, symbol_id: str) -> Symbol:
        return self.symbols_by_id[symbol_id]

    def symbols_for_file(self, rel_path: str) -> list[Symbol]:
        return list(self.symbols_by_file.get(rel_path, []))

    def resolve_imported_symbol(self, current_file: str, imported_name: str) -> str | None:
        candidates = self.resolve_imported_symbol_candidates(current_file, imported_name)
        return candidates[0] if len(candidates) == 1 else None

    def resolve_imported_symbol_candidates(self, current_file: str, imported_name: str) -> list[str]:
        ref = self.imports_by_file.get(current_file, {}).get(imported_name)
        if not ref or ref.kind != "symbol" or not ref.module:
            return []
        file_path = self.module_to_file.get(ref.module)
        if not file_path:
            return []
        return [
            symbol.symbol_id
            for symbol in self.symbols_by_file.get(file_path, [])
            if symbol.name == ref.name and symbol.symbol_type in {"function", "class"}
        ]

    def resolve_module_alias(self, current_file: str, alias: str) -> str | None:
        return self.module_aliases_by_file.get(current_file, {}).get(alias)

    def resolve_top_level(self, name: str) -> str | None:
        candidates = self.resolve_top_level_candidates(name)
        return candidates[0] if len(candidates) == 1 else None

    def resolve_top_level_candidates(self, name: str) -> list[str]:
        return list(self.top_level_by_name.get(name, []))

    def resolve_module_function_candidates(self, module_name: str, function_name: str) -> list[str]:
        module_file = self.module_to_file.get(module_name)
        if not module_file:
            return []
        return [
            symbol.symbol_id
            for symbol in self.symbols_for_file(module_file)
            if symbol.name == function_name and symbol.symbol_type == "function"
        ]

    def resolve_method(self, class_symbol_id: str, method_name: str) -> str | None:
        return self.methods_by_class.get(class_symbol_id, {}).get(method_name)

    def resolve_class(self, module_name: str, class_name: str) -> str | None:
        return self.classes_by_module.get(module_name, {}).get(class_name)

    def _scan_file(self, path: Path) -> None:
        source = path.read_text(encoding="utf-8")
        rel_path = self.rel_path(path)
        module_name = self.module_name(path)
        tree = ast.parse(source, filename=str(path))
        lines = source.splitlines()

        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    alias_name = alias.asname or alias.name.split(".")[-1]
                    self.module_aliases_by_file[rel_path][alias_name] = alias.name
            elif isinstance(node, ast.ImportFrom):
                imported_module = self._resolve_from_module(module_name, node.module, node.level)
                for alias in node.names:
                    alias_name = alias.asname or alias.name
                    self.imports_by_file[rel_path][alias_name] = ImportRef(
                        kind="symbol",
                        module=imported_module,
                        name=alias.name,
                    )

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                symbol = self._make_symbol(rel_path, node, lines, "function")
                self.symbols_by_id[symbol.symbol_id] = symbol
                self.symbols_by_file[rel_path].append(symbol)
                self.top_level_by_name.setdefault(symbol.name, []).append(symbol.symbol_id)
            elif isinstance(node, ast.ClassDef):
                class_symbol = self._make_symbol(rel_path, node, lines, "class")
                self.symbols_by_id[class_symbol.symbol_id] = class_symbol
                self.symbols_by_file[rel_path].append(class_symbol)
                self.classes_by_module.setdefault(module_name, {})[class_symbol.name] = class_symbol.symbol_id
                self.methods_by_class.setdefault(class_symbol.symbol_id, {})
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        method_symbol = self._make_symbol(rel_path, child, lines, "method", node.name)
                        self.symbols_by_id[method_symbol.symbol_id] = method_symbol
                        self.symbols_by_file[rel_path].append(method_symbol)
                        self.methods_by_class[class_symbol.symbol_id][method_symbol.name] = method_symbol.symbol_id

    def _make_symbol(
        self,
        rel_path: str,
        node: ast.FunctionDef | ast.ClassDef,
        lines: list[str],
        symbol_type: str,
        class_name: str | None = None,
    ) -> Symbol:
        qualname = node.name if not class_name else f"{class_name}.{node.name}"
        signature = self._signature_for(node, symbol_type)
        source = "\n".join(lines[node.lineno - 1 : node.end_lineno])
        symbol_id = f"{rel_path}::{qualname}"
        return Symbol(
            symbol_id=symbol_id,
            name=node.name,
            qualname=qualname,
            file_path=rel_path,
            start_line=node.lineno,
            end_line=node.end_lineno or node.lineno,
            signature=signature,
            symbol_type=symbol_type,
            class_name=class_name,
            docstring=ast.get_docstring(node),
            source=source,
        )

    def _signature_for(self, node: ast.FunctionDef | ast.ClassDef, symbol_type: str) -> str:
        if symbol_type == "class":
            return f"class {node.name}"
        args = [arg.arg for arg in node.args.args]
        return f"def {node.name}({', '.join(args)})"

    def _resolve_from_module(self, current_module: str, imported_module: str | None, level: int) -> str:
        if level == 0:
            return imported_module or ""
        current_parts = current_module.split(".") if current_module else []
        base_parts = current_parts[:-level]
        if imported_module:
            base_parts.extend(imported_module.split("."))
        return ".".join(part for part in base_parts if part)

    def resolve_factory_return_type(self, symbol_id: str) -> str | None:
        return self.factory_return_types.get(symbol_id)

    def _infer_factory_return_type(self, node: ast.FunctionDef, rel_path: str) -> str | None:
        if len(node.body) != 1 or not isinstance(node.body[0], ast.Return):
            return None
        return_value = node.body[0].value
        if not isinstance(return_value, ast.Call):
            return None
        constructor = return_value.func
        if isinstance(constructor, ast.Name):
            local_class = next(
                (
                    symbol.symbol_id
                    for symbol in self.symbols_by_file.get(rel_path, [])
                    if symbol.symbol_type == "class" and symbol.name == constructor.id
                ),
                None,
            )
            if local_class:
                return local_class
            imported_class = self.resolve_imported_symbol(rel_path, constructor.id)
            if imported_class and self.get_symbol(imported_class).symbol_type == "class":
                return imported_class
        return None

    def _scan_factory_returns(self, path: Path) -> None:
        source = path.read_text(encoding="utf-8")
        rel_path = self.rel_path(path)
        tree = ast.parse(source, filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            returned_class = self._infer_factory_return_type(node, rel_path)
            if not returned_class:
                continue
            symbol_id = f"{rel_path}::{node.name}"
            self.factory_return_types[symbol_id] = returned_class
