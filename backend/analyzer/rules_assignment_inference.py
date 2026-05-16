from __future__ import annotations

import ast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.analyzer.resolution import CallResolver


def infer_constructor_assignment(value: ast.AST, resolver: "CallResolver") -> str | None:
    if not isinstance(value, ast.Call):
        return None
    return resolver.resolve_constructor(value.func)


def infer_factory_assignment(value: ast.AST, resolver: "CallResolver") -> str | None:
    if not isinstance(value, ast.Call):
        return None
    factory_symbol_id = resolver.resolve_direct_function_symbol(value.func)
    if factory_symbol_id:
        return resolver.symbol_index.resolve_factory_return_type(factory_symbol_id)
    return None
