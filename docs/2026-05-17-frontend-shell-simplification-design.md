# Frontend Shell Simplification Design

## Design Goal

Reduce the UI from a three-column workspace to a graph-first reader with progressive disclosure.

## Design Principles

### 1. Graph First

The graph should dominate the screen because it is the primary reading surface.

### 2. Tools On Demand

Controls, search, filters, pinned nodes, and path notes are useful, but they do not need to be permanently visible.

### 3. Detail As Focus Mode

Node detail should feel like a focused inspection step, not permanent side clutter.

## Proposed UI Changes

### A. Compact Top Bar

Replace the heavy always-open left column with a lighter top shell:

- title
- current file summary
- button to open the control drawer
- button to open detail drawer

### B. Left Control Drawer

Move into the left drawer:

- repo and target file inputs
- overview metrics
- filters
- search
- pinned nodes
- path summary

### C. Right Detail Drawer

Move node detail into a dedicated right drawer:

- drawer stays closed until a node is selected or the user opens it
- actions stay near the detail content

### D. Cleaner Graph Stage

The graph panel becomes the center of the page:

- larger default width
- less competing chrome
- a lighter inline summary above the graph

## Implementation Shape

- restructure `index.html` into a compact shell plus two drawers
- add drawer state management in `app.js`
- update `styles.css` for overlay panels and graph-first layout

## Risks

### Drawer State Confusion

If users do not understand where controls went, the UI will feel hidden rather than simplified.

Mitigation:

- use clear labels on open buttons
- keep summary hints in the visible top bar

### Too Much Modal Feeling

If overlays feel heavy or block the graph too often, the UI could become annoying.

Mitigation:

- keep drawers narrow enough
- allow the graph to remain visible behind them
- open detail only when needed

## Deferred Follow-Up

1. Remember last-open drawer state
2. Resizable drawers
3. Keyboard shortcuts for open/close
