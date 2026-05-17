# Frontend Path Reading Design

## Design Goal

Give the reader a thread view for complex graphs: not just nearby nodes, but the concrete route between two important points.

## Design Principles

### 1. Deterministic Path Logic

Use only the existing visible graph edges. The UI should compute a shortest path with a small, predictable graph traversal.

### 2. Reuse Existing Interaction

The path workflow should build on current controls:

- select one node
- pin another important node
- switch to path mode

This avoids inventing a separate path picker UI.

### 3. Honest Empty States

If there is no selected node, no pin, or no connecting path, the UI should say so directly.

## Proposed UI Changes

### A. New `路径聚焦` Filter

Add a filter that derives the shortest path between:

- the currently selected node
- the first pinned node that can form a path with it

### B. Path Summary

Extend the graph summary area to state:

- current path endpoints
- whether a path was found
- path length in nodes or edges

### C. Path Highlighting

In path mode:

- path nodes get a strong visual class
- path edges get a strong visual class
- unrelated nodes are hidden by the filter

## Implementation Shape

- extend filter state with `path`
- build directed and reverse adjacency from current graph edges
- try shortest-path search from selected node to pinned nodes in order
- if no forward path exists, try reverse direction before failing
- keep the result in derived view state, not global persistent state

## Risks

### Directionality Confusion

Readers may not know whether the path is caller-to-callee or reverse.

Mitigation:

- include endpoints in the summary
- say when the found path is reversed relative to the current selection order

### Overloading Pins

Pins already mean “important nodes”. Reusing them for path endpoints could confuse users if implicit rules are unclear.

Mitigation:

- document that path mode uses the selected node plus the pinned shortlist
- clearly state which pinned node became the endpoint

## Deferred Follow-Up

1. Explicit endpoint picker
2. Multiple alternative paths
3. Saved path snapshots
