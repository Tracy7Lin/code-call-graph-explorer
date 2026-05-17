# Frontend Navigation Design

## Design Goal

Turn the graph view from a readable overview into a workable reading surface for larger files.

## Design Principles

### 1. Navigation Should Feel Lightweight

The interface should help the user move faster, not feel like a graph IDE. Search, pinning, and local focus should remain shallow controls.

### 2. Search and Pinning Should Reinforce Reading Order

These controls should support the existing reading workflow:

- start with suggested anchors
- search when you already know what you want
- pin the nodes that define the main thread
- temporarily collapse attention around those nodes

### 3. Frontend-Only State

Search query, pinned nodes, and local-focus state should remain client-side. No backend schema changes are needed.

## Proposed UI Changes

### A. Search Card

Add a compact graph search section in the left column:

- text input
- result count
- top few matches as clickable chips

This should act as quick navigation, not a full-text explorer.

### B. Pinned Nodes Strip

Add a small area that shows pinned nodes as removable chips. Pinning should be available from node detail and from graph interactions if convenient.

### C. Local Focus Filter

Add a new filter mode such as `局部聚焦`:

- if there is a selected node, show that node plus its immediate callers/callees
- if there are pinned nodes, include their immediate neighborhood
- if there is neither, fall back to the current visible set with a clear hint

This keeps the feature explainable and deterministic.

### D. Search Highlighting

When a query is present:

- matching nodes should be visually marked
- search results should be easy to click from the sidebar
- the graph summary should explain whether the user is looking at a filtered or highlighted set

## Implementation Shape

The current static front-end can support this by:

- extending `index.html` with navigation sections
- adding lightweight state for `searchQuery` and `pinnedNodeIds`
- refactoring `app.js` helpers so graph view derivation composes filters, search matches, and local-focus rules
- extending `styles.css` with search and pin chip states

## Risks

### Too Many Modes

Search, filters, and pinning can become confusing if each behaves like a separate app.

Mitigation:

- keep search as highlight + jump behavior
- keep local focus as one extra filter mode
- keep pinning as an explicit shortlist, not a saved workspace system

### Inconsistent Local Focus

If local focus behaves unpredictably, users will not trust it.

Mitigation:

- define neighborhood strictly as immediate inbound and outbound adjacency
- surface clear empty-state hints when there is no selected or pinned context

### Large `app.js`

Navigation logic can easily make the existing front-end script too big again.

Mitigation:

- group the implementation into state helpers, view derivation helpers, graph render helpers, and detail helpers
- keep each helper narrow and data-oriented

## Deferred Follow-Up

1. Keyboard navigation for search results
2. Persisted bookmarks across reloads
3. Multi-hop path tracing between two nodes
