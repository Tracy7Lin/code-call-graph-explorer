from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from backend.languages.python.analyzer.types import ResolutionReason, ResolutionStatus

if TYPE_CHECKING:
    from backend.languages.python.analyzer.resolution import CallResolver
    from backend.languages.python.analyzer.types import Resolution


def resolve_self_method(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> "Resolution | None":
    if not isinstance(func, ast.Attribute) or resolver.current_class_id is None:
        return None
    if resolver.render_expr(func.value) != "self":
        return None
    target = resolver.symbol_index.resolve_method(resolver.current_class_id, func.attr)
    if target:
        return resolver.make_resolution(
            target,
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.SELF_METHOD,
            confidence="high",
        )
    return None


def resolve_instance_method(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> "Resolution | None":
    if not isinstance(func, ast.Attribute):
        return None
    owner = resolver.render_expr(func.value)
    if owner not in resolver.local_var_types:
        return None
    target = resolver.symbol_index.resolve_method(resolver.local_var_types[owner], func.attr)
    if target:
        return resolver.make_resolution(
            target,
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.INSTANCE_METHOD,
            confidence="high",
        )
    return None


def resolve_module_alias_function(
    func: ast.AST, caller_id: str, line: int, resolver: "CallResolver"
) -> "Resolution | None":
    if not isinstance(func, ast.Attribute):
        return None
    owner = resolver.render_expr(func.value)
    module_name = resolver.symbol_index.resolve_module_alias(resolver.rel_path, owner)
    if not module_name:
        return None
    candidates = resolver.symbol_index.resolve_module_function_candidates(module_name, func.attr)
    if len(candidates) == 1:
        return resolver.make_resolution(
            candidates[0],
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.MODULE_ALIAS_FUNCTION,
            confidence="high",
        )
    if len(candidates) > 1:
        return resolver.make_ambiguous_resolution(
            caller_id=caller_id,
            line=line,
            expr=resolver.render_expr(func),
            reason=ResolutionReason.AMBIGUOUS_MODULE_FUNCTION,
            candidates=candidates,
        )
    return None


def resolve_module_function(func: ast.AST, caller_id: str, line: int, resolver: "CallResolver") -> "Resolution | None":
    if not isinstance(func, ast.Attribute):
        return None
    owner = resolver.render_expr(func.value)
    candidates = resolver.symbol_index.resolve_module_function_candidates(owner, func.attr)
    if len(candidates) == 1:
        return resolver.make_resolution(
            candidates[0],
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.MODULE_FUNCTION,
            confidence="high",
        )
    if len(candidates) > 1:
        return resolver.make_ambiguous_resolution(
            caller_id=caller_id,
            line=line,
            expr=resolver.render_expr(func),
            reason=ResolutionReason.AMBIGUOUS_MODULE_FUNCTION,
            candidates=candidates,
        )
    return None


def resolve_class_method(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> "Resolution | None":
    if not isinstance(func, ast.Attribute):
        return None
    owner = resolver.render_expr(func.value)
    class_symbol_id = resolver.local_classes.get(owner) or resolver.symbol_index.resolve_imported_symbol(resolver.rel_path, owner)
    if not class_symbol_id:
        return None
    target = resolver.symbol_index.resolve_method(class_symbol_id, func.attr)
    if target:
        return resolver.make_resolution(
            target,
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.CLASS_METHOD,
            confidence="medium",
        )
    return None
