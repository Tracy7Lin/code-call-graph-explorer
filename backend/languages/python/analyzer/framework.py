from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from backend.languages.python.analyzer.rules_assignment_inference import (
    infer_constructor_assignment,
    infer_factory_assignment,
)
from backend.languages.python.analyzer.rules_attribute_calls import (
    resolve_class_method,
    resolve_instance_method,
    resolve_module_alias_function,
    resolve_module_function,
    resolve_self_method,
)
from backend.languages.python.analyzer.rules_name_calls import (
    resolve_ambiguous_import,
    resolve_constructor_call,
    resolve_imported_function,
    resolve_local_function,
    resolve_top_level,
)
from backend.languages.python.analyzer.types import Resolution

if TYPE_CHECKING:
    from backend.languages.python.analyzer.resolution import CallResolver


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
        CallRule("local-function", resolve_local_function),
        CallRule("constructor-call", resolve_constructor_call),
        CallRule("imported-function", resolve_imported_function),
        CallRule("ambiguous-import", resolve_ambiguous_import),
        CallRule("top-level", resolve_top_level),
        CallRule("self-method", resolve_self_method),
        CallRule("instance-method", resolve_instance_method),
        CallRule("module-alias-function", resolve_module_alias_function),
        CallRule("module-function", resolve_module_function),
        CallRule("class-method", resolve_class_method),
    ]


def build_default_assignment_rules() -> list[AssignmentRule]:
    return [
        AssignmentRule("constructor-assignment", infer_constructor_assignment),
        AssignmentRule("factory-assignment", infer_factory_assignment),
    ]
