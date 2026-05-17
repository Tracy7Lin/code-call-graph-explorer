# Roadmap

## Current Milestone

Ship a reliable local tool that helps a human start reading an unfamiliar Python file by showing:

- the central call chain
- cross-file definition jumps
- explicit unresolved calls
- optional node explanations

## Near-Term Priorities

1. Expand realistic fixture repositories and improve trustworthy Python call-resolution coverage.
2. Add better graph layout and more legible edge grouping in the UI.
3. Introduce richer node insight generation with configurable LLM providers.
4. Repository-wide pre-indexing and caching for larger codebases.
5. Additional language support after the Python flow is stable.

## Framework References

- Requirements: `docs/2026-05-16-global-framework-requirements.md`
- Design: `docs/2026-05-16-global-framework-design.md`
- Plan: `docs/superpowers/plans/2026-05-16-global-framework-upgrade.md`
- Python adapter migration requirements: `docs/2026-05-16-python-adapter-migration-requirements.md`
- Python adapter migration design: `docs/2026-05-16-python-adapter-migration-design.md`
- Python adapter migration plan: `docs/superpowers/plans/2026-05-16-python-adapter-migration.md`
- Service pipeline migration requirements: `docs/2026-05-16-service-pipeline-requirements.md`
- Service pipeline migration design: `docs/2026-05-16-service-pipeline-design.md`
- Service pipeline migration plan: `docs/superpowers/plans/2026-05-16-service-pipeline-migration.md`
- Language adapter framework requirements: `docs/2026-05-16-language-adapter-framework-requirements.md`
- Language adapter framework design: `docs/2026-05-16-language-adapter-framework-design.md`
- Language adapter framework plan: `docs/superpowers/plans/2026-05-16-language-adapter-framework.md`
- Core model migration requirements: `docs/2026-05-16-core-model-migration-requirements.md`
- Core model migration design: `docs/2026-05-16-core-model-migration-design.md`
- Core model migration plan: `docs/superpowers/plans/2026-05-16-core-model-migration.md`
- Core model direct-import requirements: `docs/2026-05-17-core-model-direct-import-requirements.md`
- Core model direct-import design: `docs/2026-05-17-core-model-direct-import-design.md`
- Core model direct-import plan: `docs/superpowers/plans/2026-05-17-core-model-direct-import.md`
- Iteration 2 requirements: `docs/2026-05-17-iteration-2-requirements.md`
- Iteration 2 design: `docs/2026-05-17-iteration-2-design.md`
- Iteration 2 plan: `docs/superpowers/plans/2026-05-17-iteration-2-accuracy-and-fixtures.md`

## Later Work

1. More precise confidence scoring and explanation of why a call is unresolved.
2. Export and sharing workflows for graph snapshots or reports.
