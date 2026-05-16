# Global Framework Upgrade Requirements

## Background

The project has already proven the core idea: a local tool can help a developer start reading an unfamiliar Python file by exposing the central call graph, uncertainty states, and advisory guidance.

However, the current codebase is still early-stage:

- Python logic remains the de facto default implementation shape
- extension points are emerging but not yet locked as repository-wide standards
- future language support would become expensive if the current boundaries drift

This document defines the requirements for the next structural phase so future work remains incremental rather than repeatedly disruptive.

## Problem Statement

Without a global framework, the project risks three kinds of quality failure:

1. language-specific logic leaking into shared layers
2. rule growth turning into large branching files again
3. advisory / LLM behavior drifting into graph truth semantics

If these boundaries are not fixed now, every future language, resolution rule, and UI enhancement will cost more and create a higher regression risk.

## Goals

1. Define a language-agnostic core model that every analyzer must target.
2. Define a language-specific adapter boundary so new languages can be added without rewriting the service or UI layers.
3. Define a rule-registration pattern so new static-analysis behaviors are added as new rules rather than more ad hoc branching.
4. Keep advisory reasoning separate from confirmed graph truth.
5. Make planning, design, and execution documents a required part of meaningful changes.

## Non-Goals

- immediate support for a second language in this phase
- full runtime semantics or execution tracing
- replacing the current Python implementation wholesale
- adding a provider-backed LLM integration in this phase

## Users and Use Cases

### Primary User

A developer opening an unfamiliar repository or file who needs to understand:

- what the main call path is
- where a symbol is defined
- which calls are trustworthy vs uncertain
- what to inspect next

### Secondary User

A maintainer extending the tool itself who needs to:

- add a new Python resolution rule
- add a new language adapter
- reason about where a change belongs

## Functional Requirements

1. The project must have a documented distinction between shared core modules and language-specific modules.
2. The static-analysis pipeline must support rule registration rather than direct growth of large branching logic.
3. The system must keep confirmed graph edges separate from advisory suggestions.
4. New resolution states and reasons must come from centralized definitions rather than scattered strings.
5. Framework-level documentation must exist for requirements, design, and execution plan before major framework changes proceed.

## Quality Requirements

1. No single analyzer file should become the dumping ground for traversal, rule selection, and rule implementation simultaneously.
2. New capabilities should be addable by filling in an existing framework slot, not redesigning the architecture each time.
3. Tests must protect both behavior and extension structure where practical.
4. Shared layers must not depend on Python-specific assumptions if those assumptions belong in the Python adapter.

## Acceptance Criteria

This phase is successful when:

- the framework is documented clearly enough that a second language can be planned without rethinking the whole project
- the rule system has a stable extension pattern
- the core/advisory separation is explicit and enforceable
- future implementation plans can refer to these documents as authoritative standards
