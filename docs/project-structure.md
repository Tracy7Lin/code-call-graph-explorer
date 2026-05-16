# Project Structure

## Top-Level Layout

- `backend/`: application code
- `frontend/`: static browser UI
- `fixtures/`: sample repositories and analysis fixtures
- `tests/`: regression and contract tests
- `docs/`: roadmap and project-level guidance

## Backend Responsibilities

### `backend/analyzer`

Parses Python files, extracts symbols, and builds call edges for the current target file.

### `backend/indexer`

Builds lightweight repository symbol maps used for cross-file lookup and ambiguity detection.

### `backend/app`

Exposes the analyzer through a service layer and the local HTTP server.

### `backend/common`

Holds shared dataclasses and API-facing models.

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
