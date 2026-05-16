# Roadmap

## Current Milestone

Ship a reliable local tool that helps a human start reading an unfamiliar Python file by showing:

- the central call chain
- cross-file definition jumps
- explicit unresolved calls
- optional node explanations

## Near-Term Priorities

1. Improve call resolution around imported modules, constructors, and method dispatch.
2. Add better graph layout and more legible edge grouping in the UI.
3. Introduce richer node insight generation with configurable LLM providers.
4. Add fixture repositories that mimic real service and package layouts.

## Later Work

1. Repository-wide pre-indexing and caching for larger codebases.
2. More precise confidence scoring and explanation of why a call is unresolved.
3. Additional language support after the Python flow is stable.
4. Export and sharing workflows for graph snapshots or reports.
