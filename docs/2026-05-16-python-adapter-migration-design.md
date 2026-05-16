# Python Adapter Migration Design

## Design Goal

Turn `backend/languages/python` from a facade into the canonical home for Python-specific implementation, while keeping the current product working and keeping migration risk low.

## Current State

The repository already has:

- `backend/core/semantics.py` for shared resolution semantics
- `backend/languages/python/__init__.py` for a minimal adapter entrypoint
- `backend/analyzer/*` for Python analysis implementation
- `backend/indexer/symbol_index.py` for Python repository indexing

The structural gap is that the canonical implementation still lives outside the Python adapter area.

## Target State

The near-term canonical Python layout should become:

```text
backend/
  core/
    semantics.py
  languages/
    python/
      __init__.py
      README.md
      analyzer/
        __init__.py
        collector.py
        file_analyzer.py
        framework.py
        resolution.py
        rules_assignment_inference.py
        rules_attribute_calls.py
        rules_name_calls.py
        types.py
      indexer/
        __init__.py
        symbol_index.py
```

Legacy paths can remain temporarily, but only as compatibility layers:

- `backend/analyzer/*`
- `backend/indexer/*`

## Migration Strategy

### 1. Canonical Move, Compatibility First

The canonical Python implementation moves into `backend/languages/python/...`.

During migration:

- existing imports may continue to work
- top-level legacy modules should become narrow wrappers where practical
- service and tests can be switched incrementally

This avoids a single high-risk rename wave while still making the new structure real.

### 2. Preserve Core Boundaries

The migration must not move shared semantics back into language code.

Shared ownership remains:

- `backend/core`: language-agnostic semantics
- `backend/common`: shared payload dataclasses until a later core-model migration
- `backend/app`: service and delivery orchestration

Python-only behavior belongs under `backend/languages/python`.

### 3. Boundary Tests

The migration should be protected with structural tests that answer:

- does a canonical Python analyzer path exist?
- does a canonical Python indexer path exist?
- does the adapter use the Python language package rather than legacy globals?

These are architecture tests, not only behavior tests.

## Immediate Module Strategy

### Python Analyzer

Move these modules under `backend/languages/python/analyzer`:

- `collector.py`
- `file_analyzer.py`
- `framework.py`
- `resolution.py`
- `rules_assignment_inference.py`
- `rules_attribute_calls.py`
- `rules_name_calls.py`
- `types.py`

### Python Indexer

Move this module under `backend/languages/python/indexer`:

- `symbol_index.py`

### Compatibility Layer

Legacy top-level modules should either:

- re-export the canonical implementation, or
- remain as a thin forwarding file with no extra logic

The compatibility layer must not become a second implementation source.

## Documentation Consequences

The migration requires updates to:

- `README.md`
- `CONTRIBUTING.md`
- `docs/project-structure.md`
- `docs/roadmap.md`

These docs should describe:

- what is canonical now
- what remains transitional
- how future contributors should extend Python code

## Risks

### Import Breakage

Moving files can break internal imports if relative and absolute imports are mixed carelessly.

Mitigation:

- migrate in small slices
- keep compatibility re-exports
- run full tests after each slice

### Duplicate Logic During Transition

If both legacy and new modules start evolving independently, the migration will fail.

Mitigation:

- designate one canonical location
- keep wrappers thin
- update docs immediately

## Deferred Follow-Up

1. Move shared models from `backend/common` into a more explicit core-model package.
2. Introduce a language-detection/pipeline layer that dispatches by language adapter instead of direct Python assumptions.
3. Remove compatibility wrappers once imports have been fully migrated and stabilized.
