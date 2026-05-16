# Call Graph Accuracy Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve call graph accuracy for common Python import patterns while making uncertainty and advisory suggestions explicit.

**Architecture:** Extend the current analyzer and models with richer edge status metadata, then expose that metadata through the service and UI. Keep advisory suggestions in a separate structure so static truth and suggested interpretation remain distinct.

**Tech Stack:** Python 3.11 standard library, dataclasses, unittest, static HTML/CSS/JS frontend

---

### Task 1: Add coverage for accuracy metadata and alias resolution

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/fixtures/sample_repo/alias_case/helpers.py`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/fixtures/sample_repo/alias_case/main.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_analyzer.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_api.py`

- [ ] **Step 1: Write failing tests**
- [ ] **Step 2: Run targeted tests to verify failure**
- [ ] **Step 3: Add minimal fixture files and keep tests focused on alias resolution, ambiguity status, and advisory payload shape**
- [ ] **Step 4: Re-run targeted tests and confirm failures now reflect missing implementation**

### Task 2: Implement richer analyzer and model metadata

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/common/models.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/indexer/symbol_index.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/analyzer/file_analyzer.py`

- [ ] **Step 1: Add structured edge status and reason fields**
- [ ] **Step 2: Extend alias and dotted module resolution**
- [ ] **Step 3: Classify ambiguity separately from generic unresolved calls**
- [ ] **Step 4: Re-run analyzer tests until green**

### Task 3: Expose advisory suggestions and resolution basis through the API

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/common/models.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/app/service.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_api.py`

- [ ] **Step 1: Add advisory suggestion model and node detail edge payloads**
- [ ] **Step 2: Return deterministic advisory suggestions only for unresolved or ambiguous edges**
- [ ] **Step 3: Re-run API tests until green**

### Task 4: Surface uncertainty and advisory state in the UI

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/index.html`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/styles.css`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/app.js`

- [ ] **Step 1: Render status-specific styling for resolved, unresolved, and ambiguous edges/nodes**
- [ ] **Step 2: Show edge reasons and advisory suggestions in the detail panel**
- [ ] **Step 3: Run the full test suite**
