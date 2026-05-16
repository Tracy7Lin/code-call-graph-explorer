# Project Structure

## Top-Level Layout

- `backend/`: application code
- `frontend/`: static browser UI
- `fixtures/`: sample repositories and analysis fixtures
- `tests/`: regression and contract tests
- `docs/`: roadmap and project-level guidance

## Backend Responsibilities

### `backend/analyzer`

Transitional compatibility layer for older imports. New Python analyzer implementation should live under `backend/languages/python/analyzer`.

### `backend/indexer`

Transitional compatibility layer for older imports. New Python indexer implementation should live under `backend/languages/python/indexer`.

### `backend/core`

Holds shared semantics that should remain language-agnostic.

### `backend/languages`

Holds the shared adapter contract and registry, plus language-specific implementations.

### `backend/languages/python`

Canonical home for Python-specific analysis and indexing code.

### `backend/app`

Owns delivery orchestration, including the service layer, the service-to-adapter pipeline, and the local HTTP server.

### `backend/common`

Holds shared dataclasses and API-facing models until a later core-model migration.

## Frontend Responsibilities

The frontend is intentionally simple:

- submits analysis requests
- renders the current graph
- loads node detail panels
- triggers graph expansion and file jumps

## Testing Strategy

- `tests/test_analyzer.py`: static analysis behavior
- `tests/test_api.py`: service/API behavior
- `tests/test_repository_governance.py`: repository baseline artifacts
- `tests/test_resolution_framework.py`: framework and structural boundary contracts
