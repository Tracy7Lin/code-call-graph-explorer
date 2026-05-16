# Global Framework Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a durable global architecture for the call graph explorer so current Python work stays maintainable and future languages can be added incrementally.

**Architecture:** Preserve the existing working Python tool while steadily separating shared semantics from language-specific logic. Use explicit rule registration, centralized resolution semantics, and progressively clearer core-vs-language boundaries.

**Tech Stack:** Python 3.11 standard library, unittest, static HTML/CSS/JS frontend, git-based milestone workflow

---

### Task 1: Lock documentation standards and framework boundaries

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-16-global-framework-requirements.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/2026-05-16-global-framework-design.md`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/docs/superpowers/plans/2026-05-16-global-framework-upgrade.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/docs/roadmap.md`

- [ ] **Step 1: Keep the scope on framework standards, not unrelated feature expansion**
- [ ] **Step 2: Define core-vs-language boundaries in writing**
- [ ] **Step 3: Add roadmap references so future work points back to the framework docs**
- [ ] **Step 4: Re-read the docs and remove vague wording or hidden decisions**

### Task 2: Create the shared-semantics layer

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/core/__init__.py`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/core/semantics.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/common/models.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/analyzer/types.py`
- Test: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_resolution_framework.py`

- [ ] **Step 1: Write the failing test for centralized shared semantics imports if behavior changes**
- [ ] **Step 2: Move or re-export resolution statuses and reasons through a clear shared core location**
- [ ] **Step 3: Keep analyzer-facing imports stable or introduce narrow compatibility shims**
- [ ] **Step 4: Run the focused framework tests**

### Task 3: Formalize Python as a language adapter

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/__init__.py`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/python/__init__.py`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/languages/python/README.md`
- Modify: existing Python analyzer/indexer modules or add compatibility wrappers
- Test: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_analyzer.py`

- [ ] **Step 1: Introduce the language adapter directory without breaking current imports**
- [ ] **Step 2: Move or wrap Python-specific modules under the adapter boundary**
- [ ] **Step 3: Keep the current product working while making the future directory contract explicit**
- [ ] **Step 4: Run analyzer-focused tests**

### Task 4: Split the rule framework into rule families

**Files:**
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/analyzer/rules_name_calls.py`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/analyzer/rules_attribute_calls.py`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/backend/analyzer/rules_assignment_inference.py`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/backend/analyzer/framework.py`
- Test: `E:/Jarvis_fun/python-call-graph-explorer/tests/test_resolution_framework.py`

- [ ] **Step 1: Keep framework.py as the registry entrypoint only**
- [ ] **Step 2: Move rule implementations into family-based modules**
- [ ] **Step 3: Preserve explicit ordering and existing behavior**
- [ ] **Step 4: Run framework and full regression tests**

### Task 5: Add delivery and quality guardrails

**Files:**
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/scripts/dev.py`
- Create: `E:/Jarvis_fun/python-call-graph-explorer/.github/workflows/test.yml`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/README.md`
- Modify: `E:/Jarvis_fun/python-call-graph-explorer/CONTRIBUTING.md`

- [ ] **Step 1: Add a single local quality command that covers the expected test baseline**
- [ ] **Step 2: Add CI that runs the same baseline command**
- [ ] **Step 3: Document the quality gate in contributor-facing docs**
- [ ] **Step 4: Re-run the full test suite and verify the workflow file is coherent**
