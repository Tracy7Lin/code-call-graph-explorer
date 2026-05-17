# Frontend Readability Requirements

## Background

The project now has a solid architecture and a functioning prototype. The current UI already works, but it still reflects a first-pass visualization style:

- labels remain English-first
- the graph uses a simple ring layout
- large single-file graphs become visually dense very quickly
- node detail presents everything at once rather than guiding reading order

This means the prototype is usable, but not yet comfortable for sustained reading.

## Problem Statement

When the target file is large, the UI currently loses readability in three ways:

1. too many nodes are shown with similar visual weight
2. the user is not guided toward a reading order or "main path first" workflow
3. the detail panel becomes verbose without helping the user decide what matters next

The next frontend iteration should improve reading efficiency rather than adding visual noise.

## Goals

1. Localize the frontend into Chinese.
2. Make the graph more readable when a single file has many functions or methods.
3. Add reading guidance so users can identify the main path and secondary nodes faster.
4. Keep uncertainty visually explicit.
5. Improve the detail panel so large nodes are easier to inspect without dumping everything at once.

## Non-Goals

- major backend API redesign
- adding a new frontend framework
- implementing a full graph engine or force simulation
- changing graph truth semantics

## Functional Requirements

1. Main interface labels and actions should be Chinese-first.
2. The graph view should provide a more readable node arrangement than the current uniform circular layout for larger files.
3. The interface should surface a compact overview: file, node count, edge count, unresolved count, and suggested reading anchors.
4. The detail panel should help the user scan large nodes more effectively, including source truncation/expansion behavior.
5. The UI should let the user reduce visual noise for large graphs, such as focusing on core paths or filtering uncertainty.

## Quality Requirements

1. The redesign should increase legibility without making the codebase front-end-heavy or fragile.
2. The JS should stay reasonably modular even in a single-file static frontend setup.
3. The UI should work on both desktop and narrower layouts.
4. Visual states for resolved, ambiguous, and unresolved should remain easy to distinguish.

## Acceptance Criteria

This iteration is successful when:

- the UI is localized to Chinese
- large single-file graphs are easier to scan than before
- the detail panel feels more guided and less overwhelming
- the graph still preserves uncertainty and formal call relationships clearly
