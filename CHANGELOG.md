# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- PyPI release (pending quota reset)

## [0.1.0] - 2026-06-17

### Added
- `euclidean(*, pulses, steps)`: Bjorklund's algorithm for Euclidean rhythm generation.
- `rotate(rhythm, *, steps)`: Left rotation by steps (mod len).
- `necklace(rhythm)`: Lexicographically minimal rotation (canonical necklace form).
- `evenness(rhythm)`: Toussaint's geometric evenness on the unit circle, normalized to [0, 1].
- `syncopation(rhythm)`: Keith's (1991) syncopation measure based on metric weight differences.
- `rhythmic_oddity(rhythm)`: Pressing's (1983) rhythmic oddity property.
- `euclidean-rhythm` CLI: print a generated rhythm as `x`/`.` characters.
