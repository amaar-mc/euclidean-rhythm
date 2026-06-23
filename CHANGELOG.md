# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-17

### Added
- `offbeatness(rhythm)`: Toussaint's offbeatness -- count of onsets landing on off-beat
  positions. Off-beat positions are those p with gcd(p, n) == 1 (equivalently, positions
  not covered by any regular subdivision).
- `inter_onset_intervals(rhythm)`: gaps in pulses between consecutive onsets, wrapping
  around the cycle. Always sums to n. Raises ValueError for zero onsets.
- `ioi_histogram(rhythm)`: histogram (interval length -> count) of inter-onset intervals.
- `onset_positions(rhythm)`: indices of onsets in a 0/1 rhythm vector.
- `pattern_from_onsets(*, positions, steps)`: inverse converter -- build a 0/1 pattern
  from onset indices. Completes a round-trip with onset_positions.

## [0.1.0] - 2026-06-17

### Added
- `euclidean(*, pulses, steps)`: Bjorklund's algorithm for Euclidean rhythm generation.
- `rotate(rhythm, *, steps)`: Left rotation by steps (mod len).
- `necklace(rhythm)`: Lexicographically minimal rotation (canonical necklace form).
- `evenness(rhythm)`: Toussaint's geometric evenness on the unit circle, normalized to [0, 1].
- `syncopation(rhythm)`: Keith's (1991) syncopation measure based on metric weight differences.
- `rhythmic_oddity(rhythm)`: Pressing's (1983) rhythmic oddity property.
- `euclidean-rhythm` CLI: print a generated rhythm as `x`/`.` characters.
