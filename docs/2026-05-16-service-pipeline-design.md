# Service Pipeline Migration Design

## Design Goal

Move delivery orchestration onto a language adapter boundary so `backend/app` stops knowing Python implementation details.

## Current State

Today `ExplorerService` directly imports:

- `backend.analyzer.file_analyzer.analyze_file`
- `backend.indexer.symbol_index.SymbolIndex`

That means the app layer still knows:

- how to build the symbol index
- which analyzer entrypoint to call
- that Python is the current implementation shape

## Target State

The target execution shape is:

1. service asks a pipeline to analyze a target file
2. pipeline chooses the active language adapter
3. adapter builds the symbol index and analyzes the file
4. service consumes only shared graph payloads and symbol lookup behavior

Near-term repository shape:

```text
backend/
  app/
    pipeline.py
    service.py
  languages/
    python/
      __init__.py
```

## Pipeline Responsibilities

The pipeline should own:

- active adapter selection
- symbol index creation
- graph analysis dispatch

The pipeline should not own:

- HTTP concerns
- node-detail formatting
- advisory wording
- frontend payload choices

## Adapter Contract

The current Python adapter already exposes:

- `build_symbol_index(repo_root)`
- `analyze_file(repo_root, target_file, symbol_index)`

The pipeline will use that contract directly. This is enough for the current phase and avoids inventing a heavier abstraction too early.

## ExplorerService After Migration

After migration, `ExplorerService` should:

- create or receive a pipeline
- reuse the pipeline's symbol index
- call pipeline methods for file analysis
- retain cache, detail, and advisory assembly behavior

This keeps service focused on product behavior rather than language execution wiring.

## Testing Consequences

Tests should verify:

- the service no longer imports legacy Python implementation directly
- the pipeline exposes the active adapter boundary
- current API behavior remains stable

## Risks

### Over-Abstracting Too Early

If the pipeline tries to solve full multi-language detection now, it will become speculative architecture.

Mitigation:

- keep the first pipeline intentionally thin
- use explicit Python adapter wiring now
- leave broader adapter selection as a later extension

### Duplicate Orchestration

If both service and pipeline try to build indexes or choose adapters, the boundary will stay muddy.

Mitigation:

- put index creation and file analysis dispatch in the pipeline only
- let service consume pipeline outputs

## Deferred Follow-Up

1. Add a registry of language adapters once a second language exists.
2. Add file/language detection instead of fixed Python-first wiring.
3. Move more shared models from `backend/common` toward a dedicated core-model area.
