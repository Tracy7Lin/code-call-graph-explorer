# Python Adapter Migration Requirements

## Background

The repository already has the first global framework pieces in place:

- shared resolution semantics live in `backend/core`
- a Python adapter boundary exists in `backend/languages/python`
- rule registration is explicit and split by rule family
- local quality and CI gates are present

However, the actual Python implementation still mostly lives in the legacy paths:

- `backend/analyzer`
- `backend/indexer`

That means the architecture is only partially real. The adapter boundary exists, but most Python-specific implementation is still outside it.

## Problem Statement

If the current Python implementation remains in legacy top-level modules, the project keeps three structural problems:

1. the language adapter remains a thin facade instead of the true home for Python behavior
2. future language work will not have a real directory contract to copy
3. shared, language-specific, and compatibility responsibilities will keep drifting together

This is the point where the repository should make the Python adapter boundary real, while preserving current behavior.

## Goals

1. Move the repository closer to a real `core + languages/python` structure.
2. Make `backend/languages/python` the canonical home for Python-specific indexing and analysis behavior.
3. Preserve current API, frontend, and test behavior during the migration.
4. Keep compatibility shims narrow so existing imports do not break abruptly.
5. Update contributor-facing documentation so the new structure is discoverable and enforceable.

## Non-Goals

- adding a second language in this phase
- redesigning the service/API surface
- changing graph semantics or advisory behavior
- introducing a new parser or runtime dependency
- deleting all legacy compatibility modules in one step

## Primary Users

### Maintainers

Maintainers need to know where to place:

- Python-specific rules
- Python indexing logic
- future Python traversal helpers

without guessing whether a change belongs in shared core or language code.

### Future Language Implementers

Anyone adding `typescript` or `go` later should be able to look at the Python layout and copy the pattern rather than inventing a new one.

## Functional Requirements

1. `backend/languages/python` must become the canonical home for Python-specific analysis and indexing modules.
2. Existing entrypoints must keep working during migration through narrow compatibility wrappers or stable imports.
3. Shared layers must not absorb Python-specific logic as part of the migration.
4. The repository must document which modules are canonical and which are transitional compatibility layers.
5. Tests must cover the adapter boundary so future work cannot silently bypass it.

## Quality Requirements

1. Migration should preserve high cohesion and low coupling.
2. No new large mixed-responsibility module should be created during the move.
3. Compatibility layers must stay thin and obvious.
4. The new structure should make future rule additions a local change inside the Python adapter area.

## Acceptance Criteria

This task is successful when:

- the Python adapter directory contains the canonical Python implementation modules
- legacy top-level Python analyzer/indexer imports are either thin wrappers or clearly transitional
- tests protect the adapter boundary
- project documentation describes the new structure and migration status accurately
