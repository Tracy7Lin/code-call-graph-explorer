# Frontend Navigation Enhancement Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use markdown checkbox markers for tracking.

**Goal:** Improve large-graph navigation with search, pinning, and local-focus controls while preserving the current Chinese-first reading workflow.

**Architecture:** Keep all new state in the static frontend. Build on top of the current lane-based graph view without changing backend APIs.

**Tech Stack:** Static HTML/CSS/JS, existing local backend API, git milestone workflow

---

### Task 1: Add navigation UI scaffolding

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/index.html`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/styles.css`

- [x] **Step 1: Add search and pinned-node scaffolding**
- [x] **Step 2: Add a local-focus filter entry**
- [x] **Step 3: Keep the left column visually compact**
- [x] **Step 4: Review wording and hierarchy**

### Task 2: Add search and pin state

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/app.js`

- [x] **Step 1: Add local frontend state for search query and pinned nodes**
- [x] **Step 2: Add search matching and result rendering helpers**
- [x] **Step 3: Add pin/unpin helpers and pinned-node rendering**
- [x] **Step 4: Keep state flow clear and testable**

### Task 3: Add local-focus graph behavior

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/app.js`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/styles.css`

- [x] **Step 1: Add a local-focus filter mode**
- [x] **Step 2: Build immediate-neighborhood derivation from selected and pinned nodes**
- [x] **Step 3: Highlight search matches and pinned nodes in the graph**
- [x] **Step 4: Keep empty states explicit when there is no local-focus context**

### Task 4: Verify, review, and ship

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/CHANGELOG.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`

- [x] **Step 1: Verify frontend syntax and run the quality gate**
- [x] **Step 2: Review the diff specifically for large-graph maintainability**
- [x] **Step 3: Update docs and roadmap**
- [x] **Step 4: Commit and push the milestone**
