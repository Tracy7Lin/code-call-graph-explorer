# Core Model Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `backend/core` the canonical home for shared graph/detail/advisory models while preserving compatibility through `backend/common/models.py`.

**Architecture:** Move the dataclass definitions into `backend/core/models.py`, keep `backend/common/models.py` as a thin forwarding compatibility layer, and update docs to reflect explicit core ownership.

**Tech Stack:** Python 3.11 standard library, unittest, static HTML/CSS/JS frontend, git milestone workflow

---

### Task 1: Lock scope and design in docs

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-16-core-model-migration-requirements.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-16-core-model-migration-design.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/superpowers/plans/2026-05-16-core-model-migration.md`

- [ ] **Step 1: Keep the scope structural, not behavioral**
- [ ] **Step 2: Define the canonical core model path**
- [ ] **Step 3: State the compatibility strategy explicitly**
- [ ] **Step 4: Re-read for hidden schema changes or overreach**

### Task 2: Add structure tests

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_resolution_framework.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_repository_governance.py`

- [ ] **Step 1: Add failing tests for canonical core model path existence**
- [ ] **Step 2: Add failing tests for compatibility exports**
- [ ] **Step 3: Keep tests narrow and structural**
- [ ] **Step 4: Run focused tests and confirm the failure shape**

### Task 3: Implement the compatibility-first move

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/core/models.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/core/__init__.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/common/models.py`

- [ ] **Step 1: Move canonical model definitions into `backend/core/models.py`**
- [ ] **Step 2: Re-export through `backend/common/models.py` without extra logic**
- [ ] **Step 3: Keep runtime behavior unchanged**
- [ ] **Step 4: Run focused tests**

### Task 4: Update docs and verify

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/CONTRIBUTING.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/project-structure.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`

- [ ] **Step 1: Document `backend/core` as the canonical home for shared models and semantics**
- [ ] **Step 2: Mark `backend/common` as transitional where appropriate**
- [ ] **Step 3: Run the full quality gate**
- [ ] **Step 4: Review diff scope, then commit and push**
