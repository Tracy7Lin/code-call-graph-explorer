# Frontend Readability Design

## Design Goal

Make the prototype feel like a code-reading tool rather than just a graph renderer.

## Design Principles

### 1. Reading First, Graph Second

The graph is a navigation aid, not the entire experience. The UI should help the user answer:

- where should I start?
- what looks central?
- what is confirmed vs uncertain?
- what should I open next?

### 2. Layered Attention

Large files should not show every node with equal emphasis.

The UI should establish at least three attention levels:

- primary reading anchors
- secondary/supporting nodes
- uncertain/noisy nodes

### 3. Chinese-First Interaction

Primary labels, controls, and explanatory text should be Chinese. Internal identifiers and source code remain as-is.

## Proposed UI Changes

### A. Overview Card

Add a compact overview block that shows:

- current target file
- node count
- edge count
- unresolved count
- suggested reading anchors

This gives the user a quick orientation before touching the graph.

### B. Better Graph Layout

Replace the current two-ring layout with a lane-based layout:

- center-file nodes in a vertical middle lane
- external/supporting nodes in side lanes
- ordering biased by node degree and reading relevance

This is simpler than a force layout, more deterministic, and easier to scan for large files.

### C. Readability Filters

Add lightweight view controls such as:

- show all
- focus on main path
- hide unresolved noise

These controls should be heuristic and frontend-only.

### D. Guided Detail Panel

The detail panel should present:

- quick facts first
- inbound/outbound summaries
- resolution basis grouped clearly
- source preview truncated by default, with expand/collapse

This keeps large functions readable without removing access to the full source block.

## Implementation Shape

The existing static frontend can support this without new dependencies by:

- expanding `index.html` with overview/filter areas
- restructuring `app.js` into clearer render helpers
- updating `styles.css` for the new visual hierarchy and responsive behavior

## Risks

### Too Many Controls

If the redesign adds too many buttons or modes, the UI will become heavier instead of clearer.

Mitigation:

- keep only a few high-value filters
- use clear defaults

### Fake "Main Path" Heuristics

If the main-path view pretends to know more than it does, it will reduce trust.

Mitigation:

- use simple, explainable heuristics such as center-file membership and node degree
- keep unresolved nodes visibly uncertain even when filtered

### Layout Fragility

If the layout depends on precise node counts or arbitrary screen sizes, it may break on realistic graphs.

Mitigation:

- use deterministic lane placement
- allow scrolling in the graph container
- keep node positioning rules simple

## Deferred Follow-Up

1. Manual node pinning or bookmarking
2. Search within graph nodes
3. More advanced path highlighting
4. Richer LLM-generated reading guides once the parser baseline is stronger
