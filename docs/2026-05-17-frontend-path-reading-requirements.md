# Frontend Path Reading Requirements

## Background

The UI now supports search, pinned nodes, and local-focus filtering. That improves navigation, but complex files still present a harder problem:

- users often need to understand how one important node relates to another
- large graphs remain cognitively expensive when the question is really path-shaped
- local neighborhoods help, but they are still broader than the exact thread a reader may want

## Problem Statement

For complex graphs, users commonly ask:

1. how does this entry function reach that helper or method
2. what is the shortest visible chain between two important nodes
3. can I temporarily hide everything except the thread I care about

The next iteration should improve path-oriented readability without pretending the graph knows semantic importance beyond its static edges.

## Goals

1. Add a path-reading mode for complex graphs.
2. Let the user derive a focused path between the selected node and a pinned node.
3. Keep the interaction explainable and deterministic.
4. Preserve the current Chinese-first reading workflow and existing filters.

## Non-Goals

- backend path computation APIs
- semantic ranking of paths with LLMs
- persistence of traced paths across reloads
- multi-graph comparison

## Functional Requirements

1. The UI should expose a path-focused filter mode.
2. When a selected node and at least one pinned node exist, the UI should compute a shortest visible path between them if one exists.
3. The UI should surface whether a path was found, and between which endpoints.
4. The graph should emphasize path nodes and de-emphasize unrelated nodes while in path mode.
5. The interface should explain empty states when there is no selected node, no pinned node, or no path.

## Quality Requirements

1. Path logic should remain front-end local and use the existing graph edges.
2. The algorithm should be simple and inspectable.
3. The code should stay modular enough to support future multi-hop or multi-endpoint tracing.

## Acceptance Criteria

This iteration is successful when:

- a user can choose a node, pin another node, and view a focused path if one exists
- the graph becomes significantly easier to read for thread-specific questions
- path mode fails clearly rather than silently when no path is available
