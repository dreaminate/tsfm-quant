# Contributing

Thanks for considering it. The short version:

1. **Issues first for anything non-trivial.** A short issue beats a long PR
   that solves the wrong problem. Template issues exist for bugs and
   features.
2. **Fork + branch from `main`.** Branch names like `feat/alpha-dir-chronos`
   or `fix/registry-slot-order`.
3. **Conventional commits.** `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`
   — the history is part of this repo's pitch, keep it readable.
4. **Green locally before pushing.** `ruff check src tests`,
   `ruff format --check src tests`, `pytest -q` — CI runs the same.
5. **Never commit data, checkpoints, or secrets.** `.gitignore` already
   excludes `data/` and `checkpoints/`; if a test needs data, generate it
   synthetically.

Good first contributions:

- a stub `BaseFMExpert` for an unimplemented slot (see
  `from tsfm_quant.experts import planned`),
- a data-fetch adapter for one exchange or metric source,
- tests for the no-leakage guards once they land.

Apache-2.0 applies to contributions as-is; no CLA.
