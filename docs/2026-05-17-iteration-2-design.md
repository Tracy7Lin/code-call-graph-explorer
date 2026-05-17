# Iteration 2 Design

## Design Goal

Use the stabilized framework to improve real-world usefulness through better fixtures and the next layer of trustworthy Python resolution rules.

## Strategic Focus

This iteration should optimize for **trustworthy realism**:

- realism in fixture shape
- trustworthiness in resolution behavior

That means the architecture largely stays put. The main work moves into:

- `fixtures/`
- `tests/`
- `backend/languages/python/analyzer/`
- `backend/languages/python/indexer/`

## Fixture Design

The current sample set proves specific behaviors, but the next iteration needs fixtures that model more realistic repository shapes, such as:

- package-level service modules
- helper/util modules
- alias-heavy imports
- simple orchestrator entrypoints
- constructors plus factory/helpers in the same flow
- duplicated names in separate modules inside a larger shape

Fixture guidance:

- keep them small enough for fast tests
- keep them realistic enough that a human would recognize them as "actual code structure"
- prefer several medium fixtures over one huge fixture

## Accuracy Scope

The next resolution improvements should target patterns that are still common and statically explainable, for example:

- slightly richer imported class and method flows
- more robust local variable type propagation in straightforward cases
- clearer handling of helper/object orchestration flows across multiple files

The iteration should still avoid pretending to solve:

- arbitrary dynamic dispatch
- reflection-heavy patterns
- advanced dependency injection
- runtime-only type inference

## Testing Strategy

This iteration should lean heavily on test shape.

Three layers matter:

1. analyzer tests
   - graph truth
   - resolution status
   - ambiguity handling

2. API tests
   - projection stability
   - node detail accuracy
   - advisory behavior staying separate

3. governance/structure tests
   - only when the iteration changes repository contracts

The analyzer tests should become the primary quality signal for this iteration.

## Execution Shape

Recommended sequence:

1. add realistic fixtures
2. write failing analyzer/API tests for those fixtures
3. implement the next resolution rules
4. re-run focused tests
5. run full suite

## Risks

### Fake Realism

If fixtures are still too toy-like, the iteration will create false confidence.

Mitigation:

- make fixtures resemble recognizable service code
- include multi-file call flows instead of isolated single examples

### Overfitting to Fixtures

If the implementation is too tuned to specific sample shapes, the project will gain tests but not robustness.

Mitigation:

- use multiple fixtures that stress related patterns differently
- keep rules general, not path-specific

### Premature UI Work

If this iteration shifts into UI polishing, the parser baseline will remain too soft.

Mitigation:

- treat parser/fixture realism as the primary objective
- defer major UI improvements until the new accuracy baseline is in place

## Deferred Follow-Up

After this iteration lands, the project will be better positioned for:

1. stronger UI readability work
2. richer advisory / LLM enhancements
3. performance and caching work on larger repositories
