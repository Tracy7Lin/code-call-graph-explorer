# Language Adapter Framework Requirements

## Background

The repository now has:

- shared semantics in `backend/core`
- canonical Python implementation under `backend/languages/python`
- a service pipeline that routes analysis through a Python language adapter

This is already cleaner than the earlier Python-first structure, but the pipeline still hardcodes a single adapter class. That means the framework shape is not yet reusable even though the boundaries are improving.

## Problem Statement

If the pipeline hardcodes `PythonLanguageAdapter`, the repository still has a structural limitation:

1. the language adapter contract is implicit instead of formalized
2. adapter selection is not a reusable framework concern
3. future languages would require pipeline rewrites instead of adapter registration

We do not need a second language yet, but we do need the framework that makes adding one incremental later.

## Goals

1. Define a reusable language adapter contract.
2. Add a registry or equivalent framework mechanism for adapter lookup.
3. Keep the runtime behavior Python-only for now.
4. Make the pipeline depend on the framework, not on a specific concrete adapter class.
5. Improve code reuse without speculative multi-language complexity.

## Non-Goals

- implementing a second language adapter
- adding complex automatic language detection heuristics
- changing graph semantics, advisory behavior, or frontend payloads
- introducing a plugin system or dynamic loading mechanism

## Functional Requirements

1. The repository must have a single place where language adapters are registered.
2. The pipeline must resolve the active adapter through that framework rather than direct Python wiring.
3. The current Python adapter must satisfy the shared contract.
4. Tests must prove the registry exists and the pipeline uses it.
5. The framework should support explicit language ids even if only `python` exists today.

## Quality Requirements

1. The adapter contract should be small and stable.
2. The registry should be simple, deterministic, and easy to test.
3. The pipeline should remain orchestration-only.
4. The framework should increase reuse without introducing abstraction layers that do not pay for themselves yet.

## Acceptance Criteria

This task is successful when:

- the pipeline resolves adapters through a reusable framework boundary
- Python remains the only registered implementation
- tests protect the registry and selection behavior
- full regression still passes
