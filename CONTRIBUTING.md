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
4. Run `python scripts/dev.py quality` before asking for review.
5. Update `CHANGELOG.md` if behavior, developer workflow, or repository structure changed.

## Useful Commands

```bash
python -m unittest discover -s tests -v
python scripts/dev.py quality
python run.py --repo-root fixtures/sample_repo --target-file fixtures/sample_repo/pkg/main.py
python scripts/dev.py test
python scripts/dev.py serve-sample
```

## Repository Expectations

- `backend/languages/python` is the canonical home for Python-specific analyzer and indexer code.
- `backend/analyzer` and `backend/indexer` are transitional compatibility layers and should not become the main place for new Python logic.
- `backend/app` owns service orchestration and HTTP serving.
- `backend/core` owns shared semantics and shared graph-facing models that should stay language-agnostic.
- `frontend` stays dependency-light and consumes the backend API surface directly.
- `fixtures` contains deterministic sample repositories for tests and demos.

## Import Expectations

- New runtime code should import shared graph/detail/advisory models from `backend.core.models`.
- `backend.common.models` is compatibility-only and should not be the default choice for new runtime imports.

## Migration Notes

- When extending Python analysis behavior, prefer `backend/languages/python/analyzer`.
- When extending Python repository indexing behavior, prefer `backend/languages/python/indexer`.
- If a legacy top-level module must remain, keep it as a thin forwarding wrapper only.

## Pull Requests

- Keep PR scope narrow.
- Explain the user-facing effect and the verification you ran.
- Call out any remaining ambiguity in resolution behavior or UI interactions.
