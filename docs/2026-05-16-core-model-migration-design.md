# Core Model Migration Design

## Design Goal

Move shared graph-facing models into the explicit core boundary while keeping compatibility for existing imports.

## Current State

Today the repository has:

- `backend/core/semantics.py` for shared resolution semantics
- `backend/common/models.py` for shared dataclasses such as `Symbol`, `CallEdge`, `FileGraph`, and `NodeDetail`

This means core semantics and core models are split across two ownership areas, which is not the intended long-term structure.

## Target State

The near-term target should be:

```text
backend/
  core/
    semantics.py
    models.py
  common/
    models.py  # compatibility exports only
```

This keeps the change small while still making core ownership explicit.

## Migration Strategy

### 1. Canonical Move, Compatibility First

The canonical shared model definitions move into `backend/core/models.py`.

During the transition:

- existing imports from `backend.common.models` continue to work
- `backend/common/models.py` becomes a thin forwarding compatibility file

### 2. Keep Behavior Frozen

This migration is structural, not behavioral.

The following must stay unchanged:

- dataclass field sets
- `to_dict()` behavior
- API payload shapes
- test expectations

### 3. Limit Scope

Do not redesign model layering more than needed for this slice. A single `backend/core/models.py` file is enough for now and avoids unnecessary fragmentation.

## Testing Consequences

Tests should verify:

- canonical core model path exists
- compatibility imports still work
- framework docs and governance docs reference the new migration docs

## Documentation Consequences

The migration should update:

- `README.md`
- `CONTRIBUTING.md`
- `docs/project-structure.md`
- `docs/roadmap.md`

These docs should describe `backend/core` as the canonical home for shared semantics and shared graph-facing models.

## Risks

### Import Drift

If some modules are updated to the new core path and others silently keep evolving the compatibility path, the migration will lose value.

Mitigation:

- make `backend/common/models.py` a pure forwarding file
- update documentation immediately
- protect the structure with tests

### Over-Splitting Too Early

Breaking models into too many submodules now would add complexity without much payoff.

Mitigation:

- use one clear `backend/core/models.py` file in this phase
- revisit finer-grained model packaging only when the model surface grows materially

## Deferred Follow-Up

1. Migrate service and language code to import from `backend/core.models` directly once the compatibility layer has settled.
2. Reduce `backend/common` further or remove it once remaining compatibility obligations are gone.
