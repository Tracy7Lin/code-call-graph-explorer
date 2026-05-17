# Frontend Readability And Chinese Localization Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use markdown checkbox markers for tracking.

**Goal:** Improve front-end readability, localize the UI to Chinese, and make large single-file graphs more manageable.

**Architecture:** Keep the existing static frontend stack. Improve information hierarchy, graph layout heuristics, filtering, and detail presentation without changing backend semantics.

**Tech Stack:** Static HTML/CSS/JS, existing local backend API, git milestone workflow

---

### Task 1: Localize and restructure the shell UI

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/index.html`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/styles.css`

- [x] **Step 1: Convert primary UI labels and helper text to Chinese**
- [x] **Step 2: Add overview and filter scaffolding**
- [x] **Step 3: Keep the layout readable on desktop and mobile**
- [x] **Step 4: Review for wording clarity and visual hierarchy**

### Task 2: Improve graph readability for large single-file views

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/app.js`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/styles.css`

- [x] **Step 1: Replace the current circular layout with a more readable lane-based layout**
- [x] **Step 2: Add lightweight heuristics for primary vs supporting nodes**
- [x] **Step 3: Add low-noise view filters**
- [x] **Step 4: Keep uncertainty states explicit**

### Task 3: Improve the detail reading workflow

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/app.js`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/frontend/styles.css`

- [x] **Step 1: Add summary-first node detail presentation**
- [x] **Step 2: Add source preview truncation and expansion**
- [x] **Step 3: Surface reading anchors and counts clearly**
- [x] **Step 4: Keep detail rendering code reasonably modular**

### Task 4: Verify, review, and ship

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/CHANGELOG.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`

- [x] **Step 1: Verify the frontend code path and run the full quality gate**
- [x] **Step 2: Review the diff specifically for readability and maintainability**
- [x] **Step 3: Update user-facing docs and changelog**
- [ ] **Step 4: Commit and push the milestone**
