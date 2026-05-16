from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

from backend.common.models import CallEdge, FileGraph, Symbol
from backend.indexer.symbol_index import SymbolIndex


@dataclass(frozen=True)
class Resolution:
    callee_id: str
    resolved: bool
    confidence: str


def analyze_file(repo_root: Path, target_file: Path, symbol_index: SymbolIndex) -> FileGraph:
    repo_root = Path(repo_root).resolve()
    target_file = Path(target_file).resolve()
    rel_path = symbol_index.rel_path(target_file)
    source = target_file.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(target_file))
    local_symbols = symbol_index.symbols_for_file(rel_path)
    local_symbol_ids = {symbol.symbol_id for symbol in local_symbols if symbol.symbol_type in {"function", "method"}}
    nodes_by_id: dict[str, Symbol] = {symbol.symbol_id: symbol for symbol in local_symbols if symbol.symbol_type != "class"}
    edges: list[CallEdge] = []
    unresolved_ids: list[str] = []
    local_functions = {symbol.name: symbol.symbol_id for symbol in local_symbols if symbol.symbol_type == "function"}
    local_classes = {symbol.name: symbol.symbol_id for symbol in local_symbols if symbol.symbol_type == "class"}
    module_name = symbol_index.module_name(target_file)

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            caller_id = f"{rel_path}::{node.name}"
            collector = CallCollector(symbol_index, rel_path, local_functions, local_classes, None, module_name)
            function_edges = collector.collect(node, caller_id)
            for edge in function_edges:
                edges.append(edge)
                if not edge.resolved:
                    unresolved_ids.append(edge.callee_id)
                    nodes_by_id.setdefault(edge.callee_id, make_unresolved_symbol(edge.callee_id, rel_path, edge.line, edge.call_expr))
                else:
                    nodes_by_id.setdefault(edge.callee_id, symbol_index.get_symbol(edge.callee_id))
        elif isinstance(node, ast.ClassDef):
            class_id = f"{rel_path}::{node.name}"
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    caller_id = f"{rel_path}::{node.name}.{child.name}"
                    collector = CallCollector(symbol_index, rel_path, local_functions, local_classes, class_id, module_name)
                    function_edges = collector.collect(child, caller_id)
                    for edge in function_edges:
                        edges.append(edge)
                        if not edge.resolved:
                            unresolved_ids.append(edge.callee_id)
                            nodes_by_id.setdefault(edge.callee_id, make_unresolved_symbol(edge.callee_id, rel_path, edge.line, edge.call_expr))
                        else:
                            nodes_by_id.setdefault(edge.callee_id, symbol_index.get_symbol(edge.callee_id))

    center_ids = sorted(local_symbol_ids)
    return FileGraph(
        center_file=rel_path,
        center_symbol_ids=center_ids,
        nodes=list(nodes_by_id.values()),
        edges=edges,
        unresolved_ids=unresolved_ids,
    )


def make_unresolved_symbol(symbol_id: str, file_path: str, line: int, expr: str) -> Symbol:
    return Symbol(
        symbol_id=symbol_id,
        name=expr,
        qualname=expr,
        file_path=file_path,
        start_line=line,
        end_line=line,
        signature=expr,
        symbol_type="unresolved",
        docstring=None,
        source="",
    )


class CallCollector(ast.NodeVisitor):
    def __init__(
        self,
        symbol_index: SymbolIndex,
        rel_path: str,
        local_functions: dict[str, str],
        local_classes: dict[str, str],
        current_class_id: str | None,
        module_name: str,
    ) -> None:
        self.symbol_index = symbol_index
        self.rel_path = rel_path
        self.local_functions = local_functions
        self.local_classes = local_classes
        self.current_class_id = current_class_id
        self.module_name = module_name
        self.edges: list[CallEdge] = []
        self.caller_id = ""
        self.local_var_types: dict[str, str] = {}

    def collect(self, node: ast.FunctionDef, caller_id: str) -> list[CallEdge]:
        self.caller_id = caller_id
        for statement in node.body:
            self.visit(statement)
        return self.edges

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return None

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Call):
            class_symbol_id = self._resolve_constructor(node.value.func)
            if class_symbol_id:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.local_var_types[target.id] = class_symbol_id
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        resolution = self._resolve_call(node.func)
        expr = render_expr(node.func)
        line = node.lineno
        if resolution is None:
            unresolved_id = f"unresolved:{self.rel_path}:{self.caller_id}:{line}:{expr}"
            resolution = Resolution(unresolved_id, False, "low")
        edge = CallEdge(
            edge_id=f"{self.caller_id}->{resolution.callee_id}@{line}",
            caller_id=self.caller_id,
            callee_id=resolution.callee_id,
            call_expr=expr,
            line=line,
            confidence=resolution.confidence,
            resolved=resolution.resolved,
            cross_file=self._is_cross_file(resolution.callee_id),
        )
        self.edges.append(edge)
        self.generic_visit(node)

    def _resolve_call(self, func: ast.AST) -> Resolution | None:
        if isinstance(func, ast.Name):
            if func.id in self.local_functions:
                return Resolution(self.local_functions[func.id], True, "high")
            imported_symbol = self.symbol_index.resolve_imported_symbol(self.rel_path, func.id)
            if imported_symbol and self.symbol_index.get_symbol(imported_symbol).symbol_type == "function":
                return Resolution(imported_symbol, True, "high")
            candidate = self.symbol_index.resolve_top_level(func.id)
            if candidate:
                return Resolution(candidate, True, "medium")
            return None

        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            owner = func.value.id
            method_name = func.attr
            if owner == "self" and self.current_class_id:
                target = self.symbol_index.resolve_method(self.current_class_id, method_name)
                if target:
                    return Resolution(target, True, "high")
            if owner in self.local_var_types:
                target = self.symbol_index.resolve_method(self.local_var_types[owner], method_name)
                if target:
                    return Resolution(target, True, "high")
            module_name = self.symbol_index.resolve_module_alias(self.rel_path, owner)
            if module_name:
                module_file = self.symbol_index.module_to_file.get(module_name)
                if module_file:
                    candidates = [
                        symbol.symbol_id
                        for symbol in self.symbol_index.symbols_for_file(module_file)
                        if symbol.name == method_name and symbol.symbol_type == "function"
                    ]
                    if len(candidates) == 1:
                        return Resolution(candidates[0], True, "high")
            class_symbol_id = self.local_classes.get(owner) or self.symbol_index.resolve_imported_symbol(self.rel_path, owner)
            if class_symbol_id:
                target = self.symbol_index.resolve_method(class_symbol_id, method_name)
                if target:
                    return Resolution(target, True, "medium")
        return None

    def _resolve_constructor(self, func: ast.AST) -> str | None:
        if isinstance(func, ast.Name):
            if func.id in self.local_classes:
                return self.local_classes[func.id]
            imported_class = self.symbol_index.resolve_imported_symbol(self.rel_path, func.id)
            if imported_class and self.symbol_index.get_symbol(imported_class).symbol_type == "class":
                return imported_class
        return None

    def _is_cross_file(self, callee_id: str) -> bool:
        return not callee_id.startswith(f"{self.rel_path}::") and not callee_id.startswith("unresolved:")


def render_expr(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{render_expr(node.value)}.{node.attr}"
    return "<call>"
