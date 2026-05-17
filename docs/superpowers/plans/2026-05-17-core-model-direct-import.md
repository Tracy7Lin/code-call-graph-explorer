# Core Model Direct Import Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use markdown checkbox markers for tracking.

**Goal:** Move runtime code to direct `backend.core.models` imports while keeping `backend.common.models` as a compatibility-only layer.

**Architecture:** Preserve the canonical shared model definitions in `backend/core/models.py`, update runtime modules to import from that path, and keep structural tests that separate canonical imports from compatibility exports.

**Tech Stack:** Python 3.11 standard library, unittest, static HTML/CSS/JS frontend, git milestone workflow

---

### Task 1: Lock scope and design in docs

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-17-core-model-direct-import-requirements.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-17-core-model-direct-import-design.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/superpowers/plans/2026-05-17-core-model-direct-import.md`

- [x] **Step 1: Keep the scope on runtime import adoption, not model redesign**
- [x] **Step 2: Define runtime modules as the migration target**
- [x] **Step 3: Keep compatibility exports explicit**
- [x] **Step 4: Re-read for hidden scope creep**

### Task 2: Add structural tests

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_resolution_framework.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_repository_governance.py`

- [x] **Step 1: Add failing tests for runtime modules importing from `backend.core.models`**
- [x] **Step 2: Preserve compatibility-export assertions**
- [x] **Step 3: Keep tests narrow and structural**
- [x] **Step 4: Run focused tests and confirm the failure shape**

### Task 3: Migrate runtime imports

**Files:**
- Modify: active runtime modules under `E:/Jarvis_fun/python-call-graph-explorer/backend/app/*`
- Modify: active runtime modules under `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/*`

- [x] **Step 1: Move all active runtime imports from `backend.common.models` to `backend.core.models`**
- [x] **Step 2: Keep `backend.common.models` untouched as a compatibility export layer**
- [x] **Step 3: Avoid unnecessary behavioral edits**
- [x] **Step 4: Run focused tests**

### Task 4: Update docs and verify

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/CONTRIBUTING.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/project-structure.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`

- [x] **Step 1: Document `backend.core.models` as the canonical runtime import path**
- [x] **Step 2: Keep `backend.common` clearly transitional**
- [x] **Step 3: Run the full quality gate**
- [x] **Step 4: Review diff scope, then commit and push**
