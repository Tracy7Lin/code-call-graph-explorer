# Iteration 2 Requirements

## Background

The project has completed its first major architecture phase:

- shared semantics and shared models now have canonical core ownership
- Python analysis lives under a language adapter boundary
- the service executes through a pipeline and adapter registry
- compatibility layers are increasingly explicit rather than accidental
- testing, CI, roadmap, and implementation-plan discipline are in place

This means the project is past the "prove the architecture" stage. The next iteration should optimize for product usefulness rather than more foundational restructuring.

## Problem Statement

The current prototype is structurally solid, but it still has a product-risk gap:

1. accuracy is mostly validated on small and intentionally simple fixtures
2. parsing confidence is not yet stress-tested against more realistic repository shapes
3. future UI and LLM work would currently sit on a validation base that is still too narrow

If the next iteration skips realistic fixture coverage and accuracy hardening, later work will optimize presentation and explanation on top of insufficiently representative inputs.

## Goals

1. Introduce more realistic Python fixture repositories that resemble actual project layouts.
2. Expand static-analysis accuracy for the next tier of common Python patterns.
3. Turn those fixtures into stronger regression tests so future parser work has a trustworthy baseline.
4. Keep uncertainty explicit rather than adding speculative resolution.

## Non-Goals

- adding a second language in this iteration
- deep LLM integration beyond current advisory scaffolding
- major frontend redesign work
- runtime tracing or dynamic execution

## Product Goals

By the end of this iteration, the tool should feel meaningfully more useful when pointed at unfamiliar but realistic Python code. The outcome should not just be "more architecture"; it should be a visibly better reading aid.

## Functional Requirements

1. Add fixture repositories that reflect common multi-file Python application patterns.
2. Cover imported classes, module aliases, simple service objects, utility modules, and factory/helper flows in more realistic combinations.
3. Expand static analysis only for patterns that can be resolved with trustworthy rules.
4. Add regression tests that bind each new realistic pattern to expected graph behavior.
5. Keep unresolved and ambiguous states explicit where the analyzer still cannot safely decide.

## Quality Requirements

1. New parsing rules must plug into the existing rule framework without bloating central modules.
2. Realistic fixtures should remain deterministic and small enough for fast test execution.
3. New tests should reveal whether a regression is caused by indexing, resolution, or API projection.
4. The iteration should improve confidence in the prototype, not just feature count.

## Acceptance Criteria

This iteration is successful when:

- the repository contains richer realistic fixtures
- regression tests cover those fixtures meaningfully
- the analyzer resolves more real-world Python patterns without blurring uncertainty semantics
- the full suite remains green and the new tests materially raise confidence in future work
