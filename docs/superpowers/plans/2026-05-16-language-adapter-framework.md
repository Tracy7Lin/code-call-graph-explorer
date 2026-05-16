# Language Adapter Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable language adapter framework with registry and adapter selection while still supporting only Python at runtime.

**Architecture:** Define a small adapter contract, register available adapters centrally, and route the pipeline through registry-based selection. Keep the system intentionally Python-only in behavior, but no longer Python-hardcoded in framework shape.

**Tech Stack:** Python 3.11 standard library, unittest, static HTML/CSS/JS frontend, git milestone workflow

---

### Task 1: Lock scope and framework intent in docs

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-16-language-adapter-framework-requirements.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-16-language-adapter-framework-design.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/superpowers/plans/2026-05-16-language-adapter-framework.md`

- [ ] **Step 1: Keep scope on framework reuse, not adding a second language**
- [ ] **Step 2: Define the adapter contract and registry responsibilities**
- [ ] **Step 3: Define how pipeline selection should work**
- [ ] **Step 4: Re-read for hidden multi-language complexity**

### Task 2: Add framework tests

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_api.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_resolution_framework.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_repository_governance.py`

- [ ] **Step 1: Add failing tests for a registered adapter lookup path**
- [ ] **Step 2: Add failing tests for pipeline selection through the registry**
- [ ] **Step 3: Keep tests narrow and structural**
- [ ] **Step 4: Run focused tests and confirm the failure shape**

### Task 3: Implement the registry framework

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/types.py`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/registry.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/__init__.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/python/__init__.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/app/pipeline.py`

- [ ] **Step 1: Define a small adapter protocol or shared type**
- [ ] **Step 2: Register Python centrally**
- [ ] **Step 3: Migrate pipeline to registry-based selection**
- [ ] **Step 4: Run focused framework and API tests**

### Task 4: Update docs and verify

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/project-structure.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`

- [ ] **Step 1: Document the adapter registry framework**
- [ ] **Step 2: Keep wording explicit that only Python is implemented today**
- [ ] **Step 3: Run the full quality gate**
- [ ] **Step 4: Review diff scope, then commit and push**
