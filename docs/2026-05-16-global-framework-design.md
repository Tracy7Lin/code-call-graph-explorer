# Global Framework Upgrade Design

## Design Goal

Define a durable architecture for the call graph explorer so current Python work remains high quality and future languages can be added incrementally.

## Architectural Principles

### 1. Core First

Shared product behavior belongs in a language-agnostic core. This includes:

- graph-facing data models
- resolution state semantics
- advisory suggestion semantics
- service/API response shapes
- frontend rendering contracts

The core must not assume Python AST nodes, Python import syntax, or Python-specific rule names beyond their mapped shared semantics.

### 2. Language Adapters

Every language gets its own adapter area. A language adapter is responsible for:

- building symbol indexes
- extracting symbols and call edges
- hosting resolution rules
- mapping language-specific evidence into shared core models

Recommended future repository shape:

```text
backend/
  core/
    models/
    semantics/
    advisory/
  languages/
    python/
      indexer/
      analyzer/
      rules/
    typescript/
      indexer/
      analyzer/
      rules/
    go/
      indexer/
      analyzer/
      rules/
```

The current repository does not need to fully migrate to this shape in one step, but every new framework change should move toward it.

### 3. Rule Registry, Not Branch Growth

Static-analysis behavior must be expressed as registered rules with explicit ordering, not as uncontrolled growth inside one resolver method.

The framework should distinguish at least:

- call-resolution rules
- assignment/type-propagation rules

Rules should be:

- small
- single-purpose
- order-aware
- independently testable

### 4. Advisory Isolation

Advisory reasoning is a separate layer with separate semantics.

Confirmed graph truth:

- `resolved`
- `unresolved`
- `ambiguous`

Advisory output:

- candidate targets
- explanatory summaries
- suggested next nodes
- future LLM-generated rationale

Advisory output can explain uncertainty, but it cannot silently mutate confirmed graph edges.

## Proposed Layer Model

### Layer A: Shared Core

Owns:

- `Symbol`
- `CallEdge`
- `FileGraph`
- `FileGraphDelta`
- `NodeDetail`
- `AdvisorySuggestion`
- resolution status / reason constants

Rules:

- no Python AST references
- no language-specific import logic

### Layer B: Language Adapter

Owns:

- language parser integration
- symbol indexing
- rule registration
- AST traversal helpers
- language-specific fixture suites

Rules:

- may know Python/TS/Go specifics
- must emit only shared core model structures upward

### Layer C: Analysis Pipeline

Owns:

1. detect target language
2. build language index
3. analyze target file
4. build shared graph payload
5. attach advisory suggestions

Rules:

- pipeline orchestration only
- no embedded language-specific rule logic

### Layer D: Delivery

Owns:

- local HTTP API
- browser UI
- future CLI/reporting surfaces

Rules:

- only consumes shared payloads
- no language-specific AST assumptions

## Documentation Standard

Major changes to the framework should follow this document chain:

1. requirements document
2. design document
3. implementation plan
4. code execution
5. changelog and roadmap updates

This is not optional for framework-level work.

## Immediate Design Consequences

1. Continue centralizing resolution constants.
2. Continue treating rule registration as the extension point.
3. Avoid pushing more direct logic into `service.py` or the frontend that belongs in language adapters.
4. Plan the eventual rename/split from `backend/analyzer` into `backend/core` + `backend/languages/python`.

## Deferred but Expected Follow-Up

1. Move current shared models into a dedicated core package.
2. Move current Python logic under a Python adapter package.
3. Split current rule framework by rule family once more rule families exist.
4. Add CI to lock the architecture and test baseline.
