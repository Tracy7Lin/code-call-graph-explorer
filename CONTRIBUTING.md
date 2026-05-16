# Contributing

## Development Principles

- Keep the call graph trustworthy. Prefer explicit unresolved states over speculative resolution.
- Treat the static analyzer, service layer, and UI as separate responsibilities.
- Avoid adding runtime dependencies unless they materially improve the tool.
- Keep documentation aligned with the shipped milestone.

## Local Workflow

1. Create a focused branch for a single change.
2. Write or update a failing test first when behavior changes.
3. Make the smallest code change that turns the test green.
4. Run the full test suite before asking for review.
5. Update `CHANGELOG.md` if behavior, developer workflow, or repository structure changed.

## Useful Commands

```bash
python -m unittest discover -s tests -v
python run.py --repo-root fixtures/sample_repo --target-file fixtures/sample_repo/pkg/main.py
python scripts/dev.py test
python scripts/dev.py serve-sample
```

## Repository Expectations

- `backend/analyzer` owns AST parsing and edge extraction.
- `backend/indexer` owns repository-wide symbol lookup.
- `backend/app` owns service orchestration and HTTP serving.
- `frontend` stays dependency-light and consumes the backend API surface directly.
- `fixtures` contains deterministic sample repositories for tests and demos.

## Pull Requests

- Keep PR scope narrow.
- Explain the user-facing effect and the verification you ran.
- Call out any remaining ambiguity in resolution behavior or UI interactions.
