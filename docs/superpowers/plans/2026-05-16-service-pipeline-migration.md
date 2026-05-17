# Service Pipeline Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use markdown checkbox markers for tracking.

**Goal:** Move `ExplorerService` off direct Python implementation imports and behind a thin language adapter / pipeline boundary.

**Architecture:** Introduce a small orchestration layer in `backend/app` that owns adapter selection, symbol index construction, and graph analysis dispatch. Keep service focused on caching, node detail assembly, and advisory output.

**Tech Stack:** Python 3.11 standard library, unittest, static HTML/CSS/JS frontend, git milestone workflow

---

### Task 1: Lock scope and design in docs

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-16-service-pipeline-requirements.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-16-service-pipeline-design.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/superpowers/plans/2026-05-16-service-pipeline-migration.md`

- [x] **Step 1: Keep scope on service orchestration, not feature expansion**
- [x] **Step 2: Define the pipeline boundary and adapter contract**
- [x] **Step 3: Name what remains in service after migration**
- [x] **Step 4: Re-read for vague terms and hidden behavior changes**

### Task 2: Add boundary tests

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_api.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_repository_governance.py`

- [x] **Step 1: Add failing tests that require a pipeline execution boundary**
- [x] **Step 2: Keep existing API behavior assertions intact**
- [x] **Step 3: Add governance coverage for the new migration docs if needed**
- [x] **Step 4: Run focused tests and confirm the failure shape**

### Task 3: Implement the thin pipeline

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/app/pipeline.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/app/service.py`

- [x] **Step 1: Introduce a small pipeline class with an explicit active adapter**
- [x] **Step 2: Move symbol-index construction and file analysis dispatch into the pipeline**
- [x] **Step 3: Keep service caching and node-detail behavior unchanged**
- [x] **Step 4: Run focused API tests**

### Task 4: Update docs and verify

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/project-structure.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`

- [x] **Step 1: Document the service-to-adapter execution path**
- [x] **Step 2: Keep architecture docs aligned with real code**
- [x] **Step 3: Run the full quality gate**
- [x] **Step 4: Review diff scope, then commit and push**
