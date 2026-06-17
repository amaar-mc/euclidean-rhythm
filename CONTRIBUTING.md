# Contributing to euclidean-rhythm

Thanks for your interest. This project values correctness, precise definitions, and zero
runtime dependencies.

## Development

```sh
uv venv
uv pip install -e ".[dev]"
uv run pytest -q
uv run ruff check .
uv run mypy src
```

A standard virtual environment with `pip install -e ".[dev]"` works the same way.

## Guidelines

- No runtime dependencies. Standard library `math` is enough.
- All functions are pure, with keyword-only parameters and no default values.
- Every function needs exact-value tests and, where applicable, property tests (Hypothesis).
- A bug fix starts with a failing test.
- Run `uv run ruff format .` before committing.
- Commit messages follow `type(scope): description`.
- No em dash characters in code, comments, or commit messages.

## Reporting issues

Open an issue with the rhythm vector, the function called, and what you expected versus
what you observed.
