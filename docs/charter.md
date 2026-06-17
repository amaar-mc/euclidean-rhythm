# Project Charter

## Mission

`euclidean-rhythm` provides a correct, well-tested, zero-dependency Python library for
generating Euclidean rhythms and computing standard geometric rhythm measures. It extends
a growing ecosystem of music-theory libraries (pcset, tonnetz, melodic-contour) into the
domain of rhythm.

## Scope

The library covers:
- Euclidean rhythm generation via Bjorklund's algorithm
- Rotation and necklace canonical forms
- Toussaint's geometric evenness measure
- Keith's syncopation measure
- Pressing's rhythmic oddity property

Out of scope for the initial release:
- Audio playback or MIDI export
- Non-binary rhythms (weighted or continuous)
- NumPy-accelerated paths

## Design principles

- Zero runtime dependencies (standard library only).
- Pure functions with explicit keyword-only parameters and no default values.
- Strict typing (mypy strict mode).
- Every function tested with both exact values and property tests.
- Precise definitions in docstrings and architecture docs, with references.
