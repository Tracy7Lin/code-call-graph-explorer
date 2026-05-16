from __future__ import annotations


class SharedResolutionStatus:
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    AMBIGUOUS = "ambiguous"
    LLM_SUGGESTED = "llm_suggested"


class SharedResolutionReason:
    LOCAL_FUNCTION = "local_function"
    CONSTRUCTOR_CALL = "constructor_call"
    IMPORTED_SYMBOL = "imported_symbol"
    AMBIGUOUS_IMPORT = "ambiguous_import"
    TOP_LEVEL_UNIQUE = "top_level_unique"
    AMBIGUOUS_TOP_LEVEL = "ambiguous_top_level"
    SELF_METHOD = "self_method"
    INSTANCE_METHOD = "instance_method"
    MODULE_ALIAS_FUNCTION = "module_alias_function"
    MODULE_FUNCTION = "module_function"
    AMBIGUOUS_MODULE_FUNCTION = "ambiguous_module_function"
    CLASS_METHOD = "class_method"
    UNKNOWN_TARGET = "unknown_target"
