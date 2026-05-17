# Core Model Direct Import Requirements

## Background

The repository already completed the first core-model migration:

- canonical shared graph/detail/advisory models now live in `backend/core/models.py`
- `backend/common/models.py` remains as a compatibility export layer

That structural move was necessary, but it is only half the migration. Runtime code still imports models from `backend.common.models` in several places, which means the compatibility layer is still part of normal execution rather than a fallback path.

## Problem Statement

If runtime modules continue importing `backend.common.models`, the repository keeps an unnecessary ambiguity:

1. canonical core ownership exists, but daily code still points at the compatibility layer
2. new contributors may keep using `backend.common` as though it were still primary
3. `backend/common` cannot shrink cleanly because it remains on the main execution path

The next step is to move runtime code to direct `backend.core.models` imports while preserving compatibility exports for older import paths.

## Goals

1. Make runtime code import shared models directly from `backend.core.models`.
2. Keep `backend.common.models` available as a compatibility-only export surface.
3. Preserve all runtime behavior and API payloads.
4. Update docs so canonical and compatibility paths are unambiguous.

## Non-Goals

- removing `backend.common.models` entirely in this phase
- changing model schemas or serialization behavior
- adding new product features
- restructuring `backend/core/models.py` into smaller modules yet

## Functional Requirements

1. Runtime modules in `backend/app`, `backend/languages`, and other active execution paths must import shared models from `backend.core.models`.
2. Compatibility tests for `backend.common.models` must remain in place.
3. Tests must protect the direct-import rule for runtime modules.
4. Existing API behavior, UI behavior, and test fixtures must remain unchanged.

## Quality Requirements

1. `backend.common` should become clearly transitional rather than operational.
2. The migration should reduce ambiguity, not add more alias layers.
3. Structural tests should make regressions obvious.
4. Documentation should explicitly state the canonical import path.

## Acceptance Criteria

This task is successful when:

- runtime modules import from `backend.core.models`
- `backend.common.models` remains compatibility-only
- structural tests enforce the direct-import rule
- full regression still passes
