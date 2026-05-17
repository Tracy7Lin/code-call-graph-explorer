# Frontend Path Reading Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use markdown checkbox markers for tracking.

**Goal:** Improve complex-graph readability with a path-focused reading mode derived from selected and pinned nodes.

**Architecture:** Keep path logic fully front-end local and derived from the existing graph state. Reuse current search, pinning, and filter controls.

**Tech Stack:** Static HTML/CSS/JS, existing local backend API, git milestone workflow

---

### Task 1: Extend the UI for path reading

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/index.html`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/styles.css`

- [x] **Step 1: Add a path-focus filter entry**
- [x] **Step 2: Add concise path summary messaging**
- [x] **Step 3: Keep the controls understandable in the left column**
- [x] **Step 4: Review wording and empty-state clarity**

### Task 2: Add path derivation logic

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/app.js`

- [x] **Step 1: Derive a shortest path from selected and pinned nodes**
- [x] **Step 2: Handle forward, reverse, and no-path outcomes explicitly**
- [x] **Step 3: Integrate path mode into graph view derivation**
- [x] **Step 4: Keep helper boundaries clear**

### Task 3: Add path rendering emphasis

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/app.js`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/styles.css`

- [x] **Step 1: Highlight path nodes and path edges**
- [x] **Step 2: Surface endpoint and path-length information**
- [x] **Step 3: Keep failure states explicit when no path exists**
- [x] **Step 4: Preserve existing search and pin behavior**

### Task 4: Verify, review, and ship

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/CHANGELOG.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`

- [x] **Step 1: Verify frontend syntax and run the quality gate**
- [x] **Step 2: Review the diff specifically for path-reading maintainability**
- [x] **Step 3: Update docs and roadmap**
- [x] **Step 4: Commit and push the milestone**
