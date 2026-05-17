# Frontend Navigation Requirements

## Background

The Chinese-first readability iteration improved the visual baseline, but large single-file graphs still have a practical navigation gap:

- the graph is easier to look at
- the detail panel is easier to read
- but the user still lacks fast ways to locate and hold onto important nodes

For realistic files, readability depends not only on layout but also on navigation control.

## Problem Statement

When a target file contains many functions or methods, users still lose time in three situations:

1. they know a function name and want to locate it quickly
2. they want to keep one or two important nodes in view while reading around them
3. they want to temporarily reduce the graph to a local neighborhood instead of re-reading the whole lane layout

The next frontend iteration should improve navigation efficiency for large graphs without inventing fake structural certainty.

## Goals

1. Add graph-local search for fast node lookup.
2. Add lightweight pinning so users can keep important nodes visible and easy to revisit.
3. Add a local-focus mode that reduces noise around selected or pinned nodes.
4. Keep the UI Chinese-first and consistent with the current reading workflow.
5. Keep implementation modular enough that future features such as bookmarks or graph search ranking do not require a rewrite.

## Non-Goals

- backend API redesign
- persistent server-side bookmarks
- graph editing
- force-directed or animated layout systems

## Functional Requirements

1. The UI should provide a graph search input that filters or highlights matching nodes by label or qualified name.
2. The UI should let the user pin at least one node from the current graph.
3. The UI should expose a low-noise local view based on the current selection and pinned nodes.
4. The UI should clearly show what is currently pinned and allow removing pins.
5. Search and pinning should work without changing graph truth semantics.

## Quality Requirements

1. New navigation state should stay front-end local and not leak into backend contracts.
2. The front-end code should remain decomposed into understandable helpers rather than one growing event script.
3. The new controls should not overwhelm the existing interface.
4. The implementation should degrade gracefully when nothing is selected or pinned.

## Acceptance Criteria

This iteration is successful when:

- a user can search for a node by name and jump to it quickly
- a user can pin key nodes and revisit them without rescanning the whole graph
- a user can switch to a more local view for large graphs
- the new controls feel additive rather than noisy
