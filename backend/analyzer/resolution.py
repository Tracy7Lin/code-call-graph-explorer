from __future__ import annotations

import ast

from backend.analyzer.framework import build_default_assignment_rules, build_default_call_rules
from backend.analyzer.types import Resolution
from backend.analyzer.types import ResolutionReason, ResolutionStatus
from backend.indexer.symbol_index import SymbolIndex


def render_expr(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{render_expr(node.value)}.{node.attr}"
    return "<call>"


def ambiguous_id(rel_path: str, caller_id: str, line: int, expr: str) -> str:
    return f"ambiguous:{rel_path}:{caller_id}:{line}:{expr}"


class CallResolver:
    def __init__(
        self,
        symbol_index: SymbolIndex,
        rel_path: str,
        local_functions: dict[str, str],
        local_classes: dict[str, str],
        current_class_id: str | None,
        local_var_types: dict[str, str],
    ) -> None:
        self.symbol_index = symbol_index
        self.rel_path = rel_path
        self.local_functions = local_functions
        self.local_classes = local_classes
        self.current_class_id = current_class_id
        self.local_var_types = local_var_types
        self.assignment_rules = build_default_assignment_rules()
        self.call_rules = build_default_call_rules()

    def resolve_call(self, func: ast.AST, caller_id: str, line: int) -> Resolution | None:
        for rule in self.call_rules:
            resolution = rule.handler(func, caller_id, line, self)
            if resolution is not None:
                return resolution
        return None

    def resolve_assigned_class_symbol(self, value: ast.AST) -> str | None:
        for rule in self.assignment_rules:
            class_symbol_id = rule.handler(value, self)
            if class_symbol_id is not None:
                return class_symbol_id
        return None

    def resolve_constructor(self, func: ast.AST) -> str | None:
        if isinstance(func, ast.Name):
            if func.id in self.local_classes:
                return self.local_classes[func.id]
            imported_class = self.symbol_index.resolve_imported_symbol(self.rel_path, func.id)
            if imported_class and self.symbol_index.get_symbol(imported_class).symbol_type == "class":
                return imported_class
        return None

    def resolve_direct_function_symbol(self, func: ast.AST) -> str | None:
        if not isinstance(func, ast.Name):
            return None
        if func.id in self.local_functions:
            return self.local_functions[func.id]
        imported_symbol = self.symbol_index.resolve_imported_symbol(self.rel_path, func.id)
        if imported_symbol and self.symbol_index.get_symbol(imported_symbol).symbol_type == "function":
            return imported_symbol
        candidate = self.symbol_index.resolve_top_level(func.id)
        if candidate and self.symbol_index.get_symbol(candidate).symbol_type == "function":
            return candidate
        return None

    def imported_function_candidates(self, imported_name: str) -> list[str]:
        imported_candidates = self.symbol_index.resolve_imported_symbol_candidates(self.rel_path, imported_name)
        return [
            symbol_id
            for symbol_id in imported_candidates
            if self.symbol_index.get_symbol(symbol_id).symbol_type == "function"
        ]

    def make_resolution(self, callee_id: str, *, status: str, reason: str, confidence: str) -> Resolution:
        return Resolution(callee_id, True, confidence, status, reason, [])

    def make_ambiguous_resolution(
        self,
        *,
        caller_id: str,
        line: int,
        expr: str,
        reason: str,
        candidates: list[str],
    ) -> Resolution:
        return Resolution(
            ambiguous_id(self.rel_path, caller_id, line, expr),
            False,
            "low",
            ResolutionStatus.AMBIGUOUS,
            reason,
            candidates,
        )

    def render_expr(self, node: ast.AST) -> str:
        return render_expr(node)
