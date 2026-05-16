# Python Language Adapter

This package is the first language-specific adapter boundary for the call graph explorer.

Current responsibilities:

- build Python symbol indexes
- analyze Python files into shared graph models
- provide the default adapter entrypoint for Python repositories

Current implementation still delegates to the existing Python modules under `backend/analyzer` and `backend/indexer`. This is an intentional compatibility stage before a fuller directory migration.
