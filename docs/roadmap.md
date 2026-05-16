# Roadmap

## Current Milestone

Ship a reliable local tool that helps a human start reading an unfamiliar Python file by showing:

- the central call chain
- cross-file definition jumps
- explicit unresolved calls
- optional node explanations

## Near-Term Priorities

1. Establish the global framework for language-agnostic core models, language adapters, and rule registries.
2. Improve call resolution around imported modules, constructors, and method dispatch.
3. Add better graph layout and more legible edge grouping in the UI.
4. Introduce richer node insight generation with configurable LLM providers.
5. Add fixture repositories that mimic real service and package layouts.

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

## Later Work

1. Improve call resolution around imported modules, constructors, and method dispatch.
2. Repository-wide pre-indexing and caching for larger codebases.
3. More precise confidence scoring and explanation of why a call is unresolved.
4. Additional language support after the Python flow is stable.
5. Export and sharing workflows for graph snapshots or reports.
