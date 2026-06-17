"""Command-line interface for euclidean-rhythm."""

from __future__ import annotations

import sys

from .generation import euclidean


def run(argv: list[str]) -> int:
    """Run the CLI with the given argument list (excluding the program name).

    Parameters
    ----------
    argv:
        List of string arguments: [pulses, steps].

    Returns
    -------
    int
        Exit code: 0 on success, 1 on error.
    """
    if len(argv) != 2:
        print("Usage: euclidean-rhythm <pulses> <steps>", file=sys.stderr)
        print("Example: euclidean-rhythm 3 8", file=sys.stderr)
        return 1
    try:
        pulses = int(argv[0])
        steps = int(argv[1])
    except ValueError:
        print("Error: pulses and steps must be integers.", file=sys.stderr)
        return 1
    try:
        rhythm = euclidean(pulses=pulses, steps=steps)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print("".join("x" if v else "." for v in rhythm))
    return 0


def main() -> None:
    """Entry point for the euclidean-rhythm CLI."""
    sys.exit(run(sys.argv[1:]))
