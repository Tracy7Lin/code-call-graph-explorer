# Core Model Migration Requirements

## Background

The repository already has several framework improvements in place:

- shared resolution semantics in `backend/core`
- canonical Python implementation under `backend/languages/python`
- a service pipeline behind a language adapter boundary
- a reusable adapter registry framework

However, the shared graph/detail/advisory dataclasses still live in `backend/common/models.py`. That file is acting as a transitional shared bucket rather than a clearly named core ownership area.

## Problem Statement

If shared graph-facing models remain under `backend/common`, the architecture keeps an avoidable ambiguity:

1. shared product models do not live under the explicit core boundary
2. future language adapters still depend on a transitional location
3. `backend/common` remains overloaded instead of clearly transitional

The project should now make shared model ownership explicit in `backend/core` while preserving compatibility.

## Goals

1. Move canonical shared graph/detail/advisory models into a dedicated core model module or package.
2. Preserve all current runtime behavior and API payload shapes.
3. Keep legacy `backend/common/models.py` as a thin compatibility layer during transition.
4. Update docs so the repository clearly distinguishes canonical core ownership from transitional compatibility layers.

## Non-Goals

- redesigning the shared model schema
- changing serialization behavior
- moving every shared utility out of `backend/common` in one step
- adding new product features

## Functional Requirements

1. Canonical definitions for shared graph/detail/advisory models must exist under `backend/core`.
2. Existing imports through `backend/common/models.py` must continue to work during this migration.
3. Tests must protect both the canonical core path and the compatibility path.
4. The service layer, language adapters, and frontend-facing behavior must remain unchanged from the user's perspective.

## Quality Requirements

1. The migration should reduce ambiguity about where shared product models belong.
2. Compatibility files must stay thin and obvious.
3. The new core model location should be reusable for future language adapters.
4. Documentation should explicitly state that `backend/common` is transitional where relevant.

## Acceptance Criteria

This task is successful when:

- shared graph/detail/advisory models have a canonical home under `backend/core`
- `backend/common/models.py` is reduced to compatibility exports
- tests protect both canonical and compatibility paths
- full regression still passes
