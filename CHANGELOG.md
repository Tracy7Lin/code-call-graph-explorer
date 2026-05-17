# Changelog

All notable changes to this repository will be documented in this file.

## [Unreleased]

### Added

- Richer call edge status metadata with explicit resolution reasons
- Advisory suggestion payloads for unresolved and ambiguous calls
- Accuracy-improvement design and execution documents
- Realistic `service_case` fixture covering package-style service orchestration flows
- Frontend readability planning documents for the Chinese-first UI iteration
- Frontend navigation planning documents for search, pinning, and local-focus controls
- Frontend path-reading planning documents for path-focused graph reading

### Changed

- Improved Python resolution for module alias function calls
- Distinct ambiguous vs unresolved rendering in the browser UI
- Improved Python resolution for module-alias class construction and follow-on service instance calls
- Reworked the browser UI into a Chinese-first reading workflow with overview metrics, reading anchors, low-noise filters, and a lane-based layout for larger single-file graphs
- Added large-graph navigation helpers to the browser UI, including graph-local search, fixed nodes, and a local-focus mode around selected or pinned nodes
- Added a path-focused reading mode to the browser UI so complex graphs can be reduced to the shortest visible thread between a selected node and a pinned node

## [0.1.0] - 2026-05-16

### Added

- Initial Python call graph explorer with file-centered AST analysis
- Lightweight repository symbol index for cross-file lookups
- Local browser UI for graph navigation and node detail inspection
- Governance baseline: project metadata, contributing guide, roadmap, and GitHub templates
