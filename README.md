# Python Code Call Graph Explorer

A local web app for understanding unfamiliar Python files through a focused call graph, symbol details, and optional LLM-style explanations.

## Status

This repository is at the first working milestone:

- Python-only static analysis
- file-centered graph exploration
- local browser UI
- optional lightweight node insight

Planned work is tracked in [docs/roadmap.md](docs/roadmap.md).

## Features

- Analyze a target Python file inside a repository
- Build a file-centered call graph with explicit unresolved calls
- Jump to cross-file definitions through a lightweight repository index
- Inspect symbol signatures, source snippets, docstrings, and static facts
- Serve a zero-dependency browser UI from the local Python backend
- Read the graph through a Chinese-first interface with overview metrics, reading anchors, low-noise filters, graph search, pinned nodes, and local-focus navigation for larger files

## Architecture Status

The repository is now moving toward a real `core + language adapters` structure:

- `backend/core` holds shared semantics and canonical shared graph-facing models
- `backend/languages` holds the reusable adapter framework and registry
- `backend/languages/python` is the canonical home for Python-specific analysis and indexing
- `backend/app/pipeline.py` owns service-to-adapter execution wiring
- `backend/analyzer`, `backend/indexer`, and `backend/common` remain as transitional compatibility layers during migration

For active runtime code, shared graph/detail/advisory models should now be imported from `backend.core.models`.

Framework and migration guidance live in:

- [docs/2026-05-16-global-framework-design.md](docs/2026-05-16-global-framework-design.md)
- [docs/2026-05-16-python-adapter-migration-design.md](docs/2026-05-16-python-adapter-migration-design.md)
- [docs/2026-05-16-service-pipeline-design.md](docs/2026-05-16-service-pipeline-design.md)
- [docs/2026-05-16-language-adapter-framework-design.md](docs/2026-05-16-language-adapter-framework-design.md)
- [docs/2026-05-16-core-model-migration-design.md](docs/2026-05-16-core-model-migration-design.md)
- [docs/2026-05-17-core-model-direct-import-design.md](docs/2026-05-17-core-model-direct-import-design.md)

## Quick Start

```bash
python run.py --repo-root fixtures/sample_repo --target-file fixtures/sample_repo/pkg/main.py
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000).

The browser UI now emphasizes a reading workflow:

- scan the overview card first
- start with the suggested anchor nodes
- use `主干优先` or `仅看已确认` when a single-file graph becomes dense
- use graph search and fixed nodes when the graph is too large to rescan manually
- use `局部聚焦` to collapse attention around the selected or pinned nodes
- open node detail to inspect resolution basis and progressively expanded source

## Test

```bash
python -m unittest discover -s tests -v
python scripts/dev.py quality
```

## Developer Commands

- Run tests: `python -m unittest discover -s tests -v`
- Run the local quality gate: `python scripts/dev.py quality`
- Start the app: `python run.py --repo-root fixtures/sample_repo --target-file fixtures/sample_repo/pkg/main.py`
- Scripted test run: `python scripts/dev.py test`
- Scripted sample app run: `python scripts/dev.py serve-sample`

## Project Docs

- Contribution guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Change log: [CHANGELOG.md](CHANGELOG.md)
- Structure notes: [docs/project-structure.md](docs/project-structure.md)
- Roadmap: [docs/roadmap.md](docs/roadmap.md)
- Python adapter migration requirements: [docs/2026-05-16-python-adapter-migration-requirements.md](docs/2026-05-16-python-adapter-migration-requirements.md)
- Python adapter migration design: [docs/2026-05-16-python-adapter-migration-design.md](docs/2026-05-16-python-adapter-migration-design.md)
- Service pipeline migration requirements: [docs/2026-05-16-service-pipeline-requirements.md](docs/2026-05-16-service-pipeline-requirements.md)
- Service pipeline migration design: [docs/2026-05-16-service-pipeline-design.md](docs/2026-05-16-service-pipeline-design.md)
- Language adapter framework requirements: [docs/2026-05-16-language-adapter-framework-requirements.md](docs/2026-05-16-language-adapter-framework-requirements.md)
- Language adapter framework design: [docs/2026-05-16-language-adapter-framework-design.md](docs/2026-05-16-language-adapter-framework-design.md)
- Core model migration requirements: [docs/2026-05-16-core-model-migration-requirements.md](docs/2026-05-16-core-model-migration-requirements.md)
- Core model migration design: [docs/2026-05-16-core-model-migration-design.md](docs/2026-05-16-core-model-migration-design.md)
- Core model direct-import requirements: [docs/2026-05-17-core-model-direct-import-requirements.md](docs/2026-05-17-core-model-direct-import-requirements.md)
- Core model direct-import design: [docs/2026-05-17-core-model-direct-import-design.md](docs/2026-05-17-core-model-direct-import-design.md)
- Frontend readability requirements: [docs/2026-05-17-frontend-readability-requirements.md](docs/2026-05-17-frontend-readability-requirements.md)
- Frontend readability design: [docs/2026-05-17-frontend-readability-design.md](docs/2026-05-17-frontend-readability-design.md)
- Frontend navigation requirements: [docs/2026-05-17-frontend-navigation-requirements.md](docs/2026-05-17-frontend-navigation-requirements.md)
- Frontend navigation design: [docs/2026-05-17-frontend-navigation-design.md](docs/2026-05-17-frontend-navigation-design.md)
