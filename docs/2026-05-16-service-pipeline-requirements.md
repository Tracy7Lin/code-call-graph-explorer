# Service Pipeline Migration Requirements

## Background

The repository now has:

- shared semantics in `backend/core`
- canonical Python implementation under `backend/languages/python`
- legacy top-level analyzer and indexer modules reduced to compatibility wrappers

The next remaining structural gap is in the delivery layer. `ExplorerService` still imports Python analysis and indexing directly, which means the service layer still knows too much about the current language implementation.

## Problem Statement

If `backend/app/service.py` continues to import Python analyzer and indexer modules directly, the project keeps a hidden Python-first architecture:

1. the service layer stays coupled to Python module layout
2. future language support would require rewriting service orchestration
3. the adapter boundary exists in code but is not the real execution path

This should be corrected before LLM expansion or larger frontend work proceeds.

## Goals

1. Make the service layer consume analysis through a language adapter boundary.
2. Introduce a thin pipeline/orchestration layer that owns adapter selection and graph execution.
3. Preserve current API behavior and current frontend payloads.
4. Keep the pipeline small and language-agnostic.
5. Update docs so the new execution path is clear.

## Non-Goals

- adding a second language in this phase
- redesigning the frontend API
- changing graph semantics, advisory semantics, or caching behavior beyond what the pipeline needs
- implementing automatic multi-language detection beyond the immediate Python-first path

## Functional Requirements

1. `ExplorerService` must stop importing legacy Python analyzer and indexer modules directly.
2. A pipeline or equivalent orchestration object must own symbol-index construction and file analysis dispatch.
3. The active language adapter must be explicit and testable.
4. Existing node detail, graph expansion, and advisory behavior must remain unchanged from the user's point of view.

## Quality Requirements

1. The new pipeline must remain thin and orchestration-only.
2. Language-specific logic must not move into the service layer as part of the migration.
3. The service layer should become easier to generalize for future languages, not just differently coupled.
4. Tests should protect the new execution boundary.

## Acceptance Criteria

This task is successful when:

- `ExplorerService` depends on a language adapter / pipeline boundary rather than direct Python implementation modules
- tests prove the boundary exists
- full regression still passes
- project docs describe the service execution path accurately
