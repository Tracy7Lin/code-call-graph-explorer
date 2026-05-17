# Python Adapter Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use markdown checkbox markers for tracking.

**Goal:** Make `backend/languages/python` the canonical home for Python-specific analysis and indexing behavior without breaking the current product.

**Architecture:** Migrate Python implementation modules into `backend/languages/python`, keep legacy top-level modules as thin compatibility layers where needed, and protect the new structure with tests and documentation.

**Tech Stack:** Python 3.11 standard library, unittest, static HTML/CSS/JS frontend, git milestone workflow

---

### Task 1: Lock the migration in docs

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-16-python-adapter-migration-requirements.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-16-python-adapter-migration-design.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/superpowers/plans/2026-05-16-python-adapter-migration.md`

- [x] **Step 1: Define the migration scope as Python-structure work, not feature expansion**
- [x] **Step 2: Name the canonical future module locations**
- [x] **Step 3: State the compatibility strategy explicitly**
- [x] **Step 4: Re-read for vague wording and hidden structural decisions**

### Task 2: Add architecture tests for the canonical Python boundary

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_resolution_framework.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_repository_governance.py`

- [x] **Step 1: Add failing tests that require canonical Python analyzer/indexer paths**
- [x] **Step 2: Add failing tests that distinguish canonical modules from compatibility wrappers where practical**
- [x] **Step 3: Keep tests narrow and structural**
- [x] **Step 4: Run the focused tests and confirm the failure shape**

### Task 3: Migrate the first Python implementation slice

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/python/analyzer/__init__.py`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/python/indexer/__init__.py`
- Create or move: canonical Python analyzer/indexer modules under `backend/languages/python/...`
- Modify: legacy `backend/analyzer/*` and `backend/indexer/*` modules into thin wrappers where needed

- [x] **Step 1: Create canonical Python analyzer/indexer package paths**
- [x] **Step 2: Move implementation modules while keeping imports working**
- [x] **Step 3: Keep wrapper files thin and obvious**
- [x] **Step 4: Run focused analyzer/framework tests**

### Task 4: Update contributor docs and product structure docs

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/CONTRIBUTING.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/project-structure.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`

- [x] **Step 1: Document the Python adapter as the canonical extension area**
- [x] **Step 2: Mark legacy top-level analyzer/indexer paths as transitional if they remain**
- [x] **Step 3: Keep contributor guidance aligned with the real directory structure**
- [x] **Step 4: Re-read docs for contradictions with the codebase**

### Task 5: Verify, commit, and push the milestone

**Files:**
- No new product files required

- [x] **Step 1: Run focused tests for framework/governance/analyzer**
- [x] **Step 2: Run the full quality gate**
- [x] **Step 3: Review diff scope for accidental structural drift**
- [x] **Step 4: Commit and push the milestone once the workspace is clean enough**
