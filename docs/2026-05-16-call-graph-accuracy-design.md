# Call Graph Accuracy Improvement Design

## Goal

Improve Python call graph accuracy without weakening trust in the graph itself.

## Core Principle

Static analysis remains the source of truth for confirmed graph edges. Any LLM-style enhancement must remain advisory and must never silently rewrite the primary graph.

## Scope of This Slice

This execution slice covers four concrete improvements:

1. Better resolution for imported module aliases and dotted module calls.
2. Explicit distinction between unresolved and ambiguous call targets.
3. Static resolution evidence in API payloads so the UI can explain why a call did or did not resolve.
4. Advisory suggestions kept separate from confirmed graph edges.

## Design Decisions

### Edge Status Model

Replace the old boolean-only resolution model with a richer status model:

- `resolved`
- `unresolved`
- `ambiguous`
- `llm_suggested` for advisory-only suggestions, never for confirmed graph edges

Each edge should also carry a short machine-readable reason, such as:

- `local_function`
- `imported_symbol`
- `module_alias_function`
- `instance_method`
- `self_method`
- `unknown_target`
- `ambiguous_top_level`
- `ambiguous_import`

### Symbol and Detail Enrichment

Node detail should include:

- inbound and outbound edges in structured form
- advisory suggestions separate from graph edges
- enough metadata to explain uncertainty in the UI

### Advisory Layer

This slice will not integrate a real external LLM provider. Instead, it will establish the API and model boundary for advisory suggestions so a real provider can be added later without changing graph truth semantics.

The first advisory implementation can be deterministic and local:

- unresolved or ambiguous edges produce a suggestion entry
- suggestion includes summary, reason, and candidate symbol ids when known

## Out of Scope

- full runtime semantics
- dataflow/type inference
- dynamic execution
- real provider-backed LLM calls
