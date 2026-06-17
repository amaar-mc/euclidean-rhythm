# euclidean-rhythm

Pure-Python Euclidean rhythm generation and analysis. Zero runtime dependencies.

## Commands

- Create env and install: `uv venv && uv pip install -e ".[dev]"`
- Test: `uv run pytest -q`
- Lint: `uv run ruff check .` (format with `uv run ruff format .`)
- Types: `uv run mypy src`
- Build: `uv build` (then `uv run --with twine twine check dist/*` before publishing)

## Architecture

`src/euclidean_rhythm/`:
- `generation.py`: Bjorklund's algorithm for euclidean()
- `operations.py`: rotate() and necklace()
- `analysis.py`: evenness(), syncopation(), rhythmic_oddity()
- `cli.py`: euclidean-rhythm CLI
- `__init__.py`: public surface

See `docs/architecture.md` for precise definitions and references.

## Conventions

- Rhythms are `list[int]` of 0/1 onset values.
- All parameters are keyword-only with no default values.
- Pure functions, strict typing, zero runtime dependencies (only `math`).
- Validate inputs and raise clear ValueError messages.

## Testing rules

- Golden values for named rhythms (son clave, bossa nova).
- Hypothesis property tests for pulse count, length, rotation invariance.
- Exact values for evenness (1.0 for maximally even) and syncopation.
- Bug fixes start with a failing test.

## Release

- Semantic versioning; update CHANGELOG.md and __version__.
- Gates: `uv run pytest && uv run ruff check . && uv run mypy src && uv build && uv run --with twine twine check dist/*`.
- Do NOT publish to PyPI (pending quota reset). Tag vX.Y.Z and GitHub release.

## Style

- No em dash characters in docs, comments, or commit messages.
- Comments explain non-obvious reasoning only.
