# Architecture

`euclidean-rhythm` is a collection of pure functions operating on binary onset vectors
(`list[int]` of 0s and 1s). There are zero runtime dependencies; only the standard
library `math` module is used.

## Module layout

- `generation.py`: Bjorklund's algorithm for Euclidean rhythm generation.
- `operations.py`: Rotation and necklace (canonical form) operations.
- `analysis.py`: Toussaint evenness, Keith syncopation, Pressing rhythmic oddity.
- `cli.py`: Minimal command-line wrapper around `euclidean()`.

## Bjorklund's algorithm

Given `pulses` onsets and `steps` total positions, Bjorklund's algorithm distributes
the onsets as evenly as possible using a process analogous to the Euclidean GCD algorithm.

**Step-by-step:**

1. Start with `pulses` groups of `[1]` and `(steps - pulses)` groups of `[0]`.
2. Pair each `[0]` group with a `[1]` group by appending (creating groups like `[1, 0]`).
3. If there are more `[1]` groups than `[0]` groups, the unpaired `[1]` groups become
   the new remainder; otherwise unpaired `[0]` groups are the remainder.
4. Repeat from step 2 with the new groups and remainder until at most 1 remainder remains.
5. Concatenate all groups and the final remainder.

This mirrors computing GCD(pulses, steps - pulses) through repeated subtraction/division.

**Canonical form:** The algorithm naturally produces a front-loaded result starting with
an onset at position 0 (when pulses > 0). This matches the musicological convention for
named patterns like the son clave.

**Reference:** Bjorklund, E. (2003). The theory of rep-rate pattern generation in the
SNS timing system. Los Alamos National Laboratory.

## Toussaint evenness

Onsets are placed on a unit circle at angles `2*pi*i/n` for each onset index `i` (where
`n` is the number of steps). The evenness score is the sum of all pairwise chord lengths,
normalized by the maximum achievable sum.

**Chord length:** `2 * sin(|theta_a - theta_b| / 2)` for angles `theta_a`, `theta_b`.

**Normalization:** The maximum sum is computed for `k` equally spaced points on the unit
circle (angles `2*pi*j/k` for j = 0..k-1). A maximally even rhythm (e.g., onsets
evenly dividing the circle) scores exactly 1.0.

**Reference:** Toussaint, G. (2005). The Euclidean algorithm generates traditional
musical rhythms. Proceedings of BRIDGES.

## Keith syncopation

The metric weight of position `i` in a rhythm of `n` steps is:
- `weight(0) = n` (the downbeat)
- `weight(i) = largest power of 2 dividing i` for `i > 0`

A syncopation event occurs when an onset at position `i` is followed by a rest at
position `j = (i + 1) mod n`, and the rest position is metrically stronger: `weight(j) > weight(i)`.
The contribution to the syncopation score is `weight(j) - weight(i)`.

The total syncopation is the sum of all such contributions. A rhythm with no syncopation
(all onsets on metrically strong beats) scores 0.

**Reference:** Keith, M. (1991). From Polychords to Polya: Adventures in Musical
Combinatorics. Vinculum Press.

## Pressing rhythmic oddity

A rhythm has the rhythmic oddity property if no two onsets are diametrically opposite
on the rhythm circle. Formally, for a rhythm of `n` steps, no two onset positions `p`
and `q` satisfy `(q - p) mod n == n / 2`.

Odd step counts trivially satisfy the property (no equal partition is possible).

**Reference:** Pressing, J. (1983). Cognitive isomorphisms between pitch and rhythm in
world musics: West Africa, the Balkans and Western tonality. Studies in Music, 17, 38-61.
