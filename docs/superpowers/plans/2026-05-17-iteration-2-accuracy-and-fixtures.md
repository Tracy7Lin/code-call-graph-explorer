# Iteration 2 Accuracy And Fixtures Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use markdown checkbox markers for tracking.

**Goal:** Improve the practical usefulness of the prototype by expanding realistic fixtures and strengthening trustworthy Python static-analysis coverage.

**Architecture:** Reuse the existing core/language/pipeline framework. Concentrate changes in realistic fixture design, analyzer/indexer rule expansion, and stronger regression tests.

**Tech Stack:** Python 3.11 standard library, unittest, static HTML/CSS/JS frontend, git milestone workflow

---

### Task 1: Add realistic fixture repositories and failing tests

**Files:**
- Create: new fixture directories under `E:/Jarvis_fun/python-call-graph-explorer/fixtures/sample_repo/`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_analyzer.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_api.py`

- [x] **Step 1: Add realistic multi-file fixture shapes for common Python service/module flows**
- [x] **Step 2: Write failing analyzer tests first**
- [x] **Step 3: Add API-level checks only where projection behavior matters**
- [x] **Step 4: Run focused tests and confirm the failure shape**

### Task 2: Implement the next tier of trustworthy Python resolution rules

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/python/analyzer/*`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/python/indexer/*`

- [x] **Step 1: Extend only statically trustworthy resolution cases**
- [x] **Step 2: Keep unresolved and ambiguous outcomes explicit where certainty is insufficient**
- [x] **Step 3: Preserve rule-family boundaries and avoid growing central mixed-responsibility files**
- [x] **Step 4: Re-run focused analyzer/API tests until green**

### Task 3: Review regression quality and harden test coverage

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_analyzer.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_api.py`

- [x] **Step 1: Review whether each new fixture is actually pulling its weight**
- [x] **Step 2: Add missing assertions for uncertainty states and cross-file call paths**
- [x] **Step 3: Keep test names and failure messages specific**
- [x] **Step 4: Run the full quality gate**

### Task 4: Update roadmap/docs and ship the milestone

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/CHANGELOG.md`

- [x] **Step 1: Document the richer fixture/accuracy milestone**
- [x] **Step 2: Keep roadmap ordering aligned with actual execution**
- [x] **Step 3: Review diff scope and remaining risks**
- [x] **Step 4: Commit and push the milestone**
