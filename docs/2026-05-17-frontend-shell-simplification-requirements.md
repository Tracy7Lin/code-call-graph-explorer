# Frontend Shell Simplification Requirements

## Background

The frontend has become more capable, but the current shell now exposes too much at once:

- a full left control column
- a large central graph surface
- a full right detail column

Even though each section is individually useful, the overall layout has become visually heavy and spatially expensive.

## Problem Statement

The current page feels bloated in two ways:

1. the graph competes with persistent side content for space
2. the user sees too many control and detail sections at the same time

This reduces readability, especially when the graph itself is already complex.

## Goals

1. Simplify the page shell so the graph becomes the primary surface.
2. Move secondary information into progressive disclosure patterns such as drawers or overlays.
3. Preserve existing capabilities without keeping them all permanently visible.
4. Keep the UI Chinese-first and consistent with the current reading workflow.

## Non-Goals

- changing backend APIs
- removing current navigation features
- introducing a frontend framework

## Functional Requirements

1. The main graph should occupy most of the viewport width by default.
2. The main controls and navigation helpers should move into a left-side drawer or equivalent overlay.
3. Node detail should move into a right-side drawer or equivalent overlay.
4. The default state should remain usable even before any drawer is opened.
5. Drawer state should be explicit and reversible.

## Quality Requirements

1. The simplified shell should reduce visual clutter, not just move it around.
2. The code should remain modular enough to support future shell changes.
3. Desktop and narrower layouts should both remain readable.

## Acceptance Criteria

This iteration is successful when:

- the graph is the obvious main surface
- controls feel available but not always in the way
- detail inspection feels intentional rather than permanently crowded
