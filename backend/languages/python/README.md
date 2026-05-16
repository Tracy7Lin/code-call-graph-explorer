# Python Language Adapter

This package is the first language-specific adapter boundary for the call graph explorer.

Current responsibilities:

- build Python symbol indexes
- analyze Python files into shared graph models
- provide the default adapter entrypoint for Python repositories

Canonical implementation now lives under:

- `backend/languages/python/analyzer`
- `backend/languages/python/indexer`

Top-level legacy modules under `backend/analyzer` and `backend/indexer` are transitional compatibility wrappers and should stay thin.
