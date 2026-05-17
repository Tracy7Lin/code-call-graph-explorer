# Core Model Direct Import Design

## Design Goal

Finish the practical adoption of `backend/core/models.py` by moving runtime imports off `backend.common.models`.

## Current State

The repository currently has:

- canonical model definitions in `backend/core/models.py`
- compatibility exports in `backend/common/models.py`
- several runtime modules still importing from `backend.common.models`

This means the canonical path exists but is not yet the standard path for active code.

## Target State

Near-term target:

- runtime modules import from `backend.core.models`
- `backend.common.models` remains a compatibility file only
- tests protect both rules explicitly

Representative runtime areas that should move:

- `backend/app/*`
- `backend/languages/*`

## Migration Strategy

### 1. Direct Runtime Adoption

Update runtime modules to import:

- `Symbol`
- `CallEdge`
- `FileGraph`
- `FileGraphDelta`
- `NodeDetail`
- `NodeInsight`
- `AdvisorySuggestion`

from `backend.core.models` instead of `backend.common.models`.

### 2. Preserve Compatibility

Do not delete or expand `backend.common.models`. Keep it as a pure forwarding module so external or older internal imports still resolve.

### 3. Add Structural Tests

Tests should verify:

- runtime modules now reference `backend.core.models`
- compatibility exports still point to the same canonical classes

This gives a clear separation:

- canonical path for active code
- compatibility path for transition

## Documentation Consequences

Docs should describe:

- `backend/core` as the canonical home for shared semantics and models
- `backend/common` as compatibility-only
- the expectation that new runtime code imports from `backend.core.models`

## Risks

### Partial Migration

If only some runtime modules move, the architecture remains muddy.

Mitigation:

- migrate all current runtime references in one slice
- protect the direct-import rule with tests

### Compatibility Regression

If the compatibility layer breaks while direct imports are updated, some older paths may fail unexpectedly.

Mitigation:

- retain compatibility-export tests
- run full regression after the migration

## Deferred Follow-Up

1. Reduce or remove `backend/common` once compatibility is no longer needed.
2. Consider splitting `backend/core/models.py` only when the model surface grows significantly.
