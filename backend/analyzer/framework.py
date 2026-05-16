from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from backend.analyzer.types import Resolution, ResolutionReason, ResolutionStatus

if TYPE_CHECKING:
    from backend.analyzer.resolution import CallResolver


@dataclass(frozen=True)
class CallRule:
    name: str
    handler: Callable[[ast.AST, str, int, "CallResolver"], Resolution | None]


@dataclass(frozen=True)
class AssignmentRule:
    name: str
    handler: Callable[[ast.AST, "CallResolver"], str | None]


def build_default_call_rules() -> list[CallRule]:
    return [
        CallRule("local-function", _resolve_local_function),
        CallRule("constructor-call", _resolve_constructor_call),
        CallRule("imported-function", _resolve_imported_function),
        CallRule("ambiguous-import", _resolve_ambiguous_import),
        CallRule("top-level", _resolve_top_level),
        CallRule("self-method", _resolve_self_method),
        CallRule("instance-method", _resolve_instance_method),
        CallRule("module-alias-function", _resolve_module_alias_function),
        CallRule("module-function", _resolve_module_function),
        CallRule("class-method", _resolve_class_method),
    ]


def build_default_assignment_rules() -> list[AssignmentRule]:
    return [
        AssignmentRule("constructor-assignment", _infer_constructor_assignment),
        AssignmentRule("factory-assignment", _infer_factory_assignment),
    ]


def _resolve_local_function(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> Resolution | None:
    if isinstance(func, ast.Name) and func.id in resolver.local_functions:
        return resolver.make_resolution(
            resolver.local_functions[func.id],
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.LOCAL_FUNCTION,
            confidence="high",
        )
    return None


def _resolve_constructor_call(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> Resolution | None:
    class_symbol_id = resolver.resolve_constructor(func)
    if class_symbol_id:
        return resolver.make_resolution(
            class_symbol_id,
            status=ResolutionStatus.RESOLVED,
            reason=ResolutionReason.CONSTRUCTOR_CALL,
            confidence="high",
        )
    return None


def _resolve_imported_function(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> Resolution | None:
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


def _resolve_ambiguous_import(func: ast.AST, caller_id: str, line: int, resolver: "CallResolver") -> Resolution | None:
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


def _resolve_top_level(func: ast.AST, caller_id: str, line: int, resolver: "CallResolver") -> Resolution | None:
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


def _resolve_self_method(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> Resolution | None:
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


def _resolve_instance_method(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> Resolution | None:
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


def _resolve_module_alias_function(func: ast.AST, caller_id: str, line: int, resolver: "CallResolver") -> Resolution | None:
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


def _resolve_module_function(func: ast.AST, caller_id: str, line: int, resolver: "CallResolver") -> Resolution | None:
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


def _resolve_class_method(func: ast.AST, _caller_id: str, _line: int, resolver: "CallResolver") -> Resolution | None:
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


def _infer_constructor_assignment(value: ast.AST, resolver: "CallResolver") -> str | None:
    if not isinstance(value, ast.Call):
        return None
    return resolver.resolve_constructor(value.func)


def _infer_factory_assignment(value: ast.AST, resolver: "CallResolver") -> str | None:
    if not isinstance(value, ast.Call):
        return None
    factory_symbol_id = resolver.resolve_direct_function_symbol(value.func)
    if factory_symbol_id:
        return resolver.symbol_index.resolve_factory_return_type(factory_symbol_id)
    return None
