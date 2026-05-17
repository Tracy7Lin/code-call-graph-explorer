# Frontend Shell Simplification Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use markdown checkbox markers for tracking.

**Goal:** Simplify the front-end shell with a graph-first layout, a left control drawer, and a right detail drawer.

**Architecture:** Keep all functionality in the static frontend. Reorganize layout and interaction without changing backend contracts.

**Tech Stack:** Static HTML/CSS/JS, existing local backend API, git milestone workflow

---

### Task 1: Restructure the page shell

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/index.html`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/styles.css`

- [x] **Step 1: Replace the persistent three-column shell with a graph-first shell**
- [x] **Step 2: Add a left control drawer and right detail drawer**
- [x] **Step 3: Keep the default visible surface compact**
- [x] **Step 4: Review copy and visual hierarchy**

### Task 2: Add drawer state management

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/app.js`

- [x] **Step 1: Add UI state for control and detail drawers**
- [x] **Step 2: Open and close drawers explicitly**
- [x] **Step 3: Keep detail drawer behavior aligned with node selection**
- [x] **Step 4: Preserve existing analysis and navigation behavior**

### Task 3: Adapt detail and controls to the new shell

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/index.html`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/app.js`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/styles.css`

- [x] **Step 1: Move control sections into the left drawer**
- [x] **Step 2: Move node detail into the right drawer**
- [x] **Step 3: Keep graph summary visible without side clutter**
- [x] **Step 4: Keep empty states explicit**

### Task 4: Verify, review, and ship

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/CHANGELOG.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`

- [x] **Step 1: Verify frontend syntax and run the quality gate**
- [x] **Step 2: Review the diff specifically for shell simplicity and maintainability**
- [x] **Step 3: Update docs and roadmap**
- [ ] **Step 4: Commit and push the milestone**
