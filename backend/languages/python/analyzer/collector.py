from __future__ import annotations

import ast

from backend.core.models import CallEdge
from backend.languages.python.analyzer.resolution import CallResolver, Resolution, render_expr
from backend.languages.python.indexer.symbol_index import SymbolIndex


class CallCollector(ast.NodeVisitor):
    def __init__(
        self,
        symbol_index: SymbolIndex,
        rel_path: str,
        local_functions: dict[str, str],
        local_classes: dict[str, str],
        current_class_id: str | None,
    ) -> None:
        self.symbol_index = symbol_index
        self.rel_path = rel_path
        self.local_functions = local_functions
        self.local_classes = local_classes
        self.current_class_id = current_class_id
        self.edges: list[CallEdge] = []
        self.caller_id = ""
        self.local_var_types: dict[str, str] = {}
        self.resolver = CallResolver(
            symbol_index=symbol_index,
            rel_path=rel_path,
            local_functions=local_functions,
            local_classes=local_classes,
            current_class_id=current_class_id,
            local_var_types=self.local_var_types,
        )

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
        class_symbol_id = self.resolver.resolve_assigned_class_symbol(node.value)
        if class_symbol_id:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.local_var_types[target.id] = class_symbol_id
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name) and node.value is not None:
            class_symbol_id = self.resolver.resolve_assigned_class_symbol(node.value)
            if class_symbol_id:
                self.local_var_types[node.target.id] = class_symbol_id
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        resolution = self.resolver.resolve_call(node.func, self.caller_id, node.lineno)
        expr = render_expr(node.func)
        line = node.lineno
        if resolution is None:
            unresolved_id = f"unresolved:{self.rel_path}:{self.caller_id}:{line}:{expr}"
            resolution = Resolution(unresolved_id, False, "low", "unresolved", "unknown_target", [])
        self.edges.append(self._make_edge(resolution, expr, line))
        self.generic_visit(node)

    def _make_edge(self, resolution: Resolution, expr: str, line: int) -> CallEdge:
        return CallEdge(
            edge_id=f"{self.caller_id}->{resolution.callee_id}@{line}",
            caller_id=self.caller_id,
            callee_id=resolution.callee_id,
            call_expr=expr,
            line=line,
            confidence=resolution.confidence,
            resolved=resolution.resolved,
            cross_file=self._is_cross_file(resolution.callee_id),
            status=resolution.status,
            reason=resolution.reason,
            candidate_symbol_ids=resolution.candidate_symbol_ids,
        )

    def _is_cross_file(self, callee_id: str) -> bool:
        return not callee_id.startswith(f"{self.rel_path}::") and not callee_id.startswith("unresolved:")
