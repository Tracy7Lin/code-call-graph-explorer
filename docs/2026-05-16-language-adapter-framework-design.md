# Language Adapter Framework Design

## Design Goal

Introduce a reusable adapter framework that makes language selection and adapter lookup explicit, while keeping the runtime behavior Python-only.

## Current State

The repository currently has:

- `PythonLanguageAdapter`
- `AnalysisPipeline`

But the pipeline still imports and instantiates `PythonLanguageAdapter` directly. That means there is no real shared adapter framework yet.

## Target State

The near-term framework should add three concepts:

1. a small adapter contract
2. a registry of available adapters
3. pipeline selection through the registry

This still leaves Python as the only concrete adapter.

## Proposed Shape

Recommended additions under `backend/languages`:

```text
backend/
  languages/
    __init__.py
    registry.py
    types.py
    python/
      __init__.py
```

## Adapter Contract

The contract should stay minimal:

- `language_id`
- `build_symbol_index(repo_root)`
- `analyze_file(repo_root, target_file, symbol_index)`

This is enough for the current system and avoids over-designing around functionality that does not exist yet.

## Registry Responsibilities

The registry should own:

- registering canonical adapters by language id
- returning the adapter for a given language id
- returning the default adapter for the current repository state

For now, “default” can simply mean Python, but the lookup should still go through the registry.

## Pipeline Responsibilities After Migration

The pipeline should:

- ask the registry for the active adapter
- build the symbol index through that adapter
- analyze files through that adapter

The pipeline should not:

- know Python implementation classes directly
- embed registry data itself

## Testing Consequences

Tests should verify:

- the registry exposes Python as the registered adapter
- the pipeline uses the registry-selected adapter
- current API behavior remains unchanged

## Risks

### Over-Generalizing

If the framework tries to solve full language detection or plugin loading now, it will become speculative.

Mitigation:

- keep the registry static and code-defined
- register only Python
- keep the adapter contract intentionally small

### Weak Contract

If the contract is only implied by convention, later adapters may drift.

Mitigation:

- define a shared adapter protocol or base type
- test the pipeline against the framework interface rather than concrete Python assumptions

## Deferred Follow-Up

1. Add explicit language detection from file extension or repository hints.
2. Register a second real adapter only after the framework has proven stable.
3. Refine the shared symbol-index typing once multiple adapters exist.
