from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from backend.analyzer.types import ResolutionReason, ResolutionStatus

if TYPE_CHECKING:
    from backend.analyzer.resolution import CallResolver
    from backend.analyzer.types import Resolution


def resolve_local_function(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> "Resolution | None":
    if isinstance(func, ast.Name) and func.id in resolver.local_functions:
        return resolver.make_resolution(
            resolver.local_functions[func.id],
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.LOCAL_FUNCTION,
            confidence="high",
        )
    return None


def resolve_constructor_call(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> "Resolution | None":
    class_symbol_id = resolver.resolve_constructor(func)
    if class_symbol_id:
        return resolver.make_resolution(
            class_symbol_id,
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.CONSTRUCTOR_CALL,
            confidence="high",
        )
    return None


def resolve_imported_function(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> "Resolution | None":
    if not isinstance(func, ast.Name):
        return None
    imported_candidates = resolver.imported_function_candidates(func.id)
    if len(imported_candidates) == 1:
        return resolver.make_resolution(
            imported_candidates[0],
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.IMPORTED_SYMBOL,
            confidence="high",
        )
    return None


def resolve_ambiguous_import(func: ast.AST, caller_id: str, line: int, resolver: "CallResolver") -> "Resolution | None":
    if not isinstance(func, ast.Name):
        return None
    imported_candidates = resolver.imported_function_candidates(func.id)
    if len(imported_candidates) > 1:
        return resolver.make_ambiguous_resolution(
            caller_id=caller_id,
            line=line,
            expr=func.id,
            reason=ResolutionReason.AMBIGUOUS_IMPORT,
            candidates=imported_candidates,
        )
    return None


def resolve_top_level(func: ast.AST, caller_id: str, line: int, resolver: "CallResolver") -> "Resolution | None":
    if not isinstance(func, ast.Name):
        return None
    candidates = resolver.symbol_index.resolve_top_level_candidates(func.id)
    if len(candidates) == 1:
        return resolver.make_resolution(
            candidates[0],
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.TOP_LEVEL_UNIQUE,
            confidence="medium",
        )
    if len(candidates) > 1:
        return resolver.make_ambiguous_resolution(
            caller_id=caller_id,
            line=line,
            expr=func.id,
            reason=ResolutionReason.AMBIGUOUS_TOP_LEVEL,
            candidates=candidates,
        )
    return None
