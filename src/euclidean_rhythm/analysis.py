"""Geometric rhythm analysis: evenness, syncopation, rhythmic oddity."""

from __future__ import annotations

import math


def evenness(rhythm: list[int]) -> float:
    """Compute Toussaint's geometric evenness of a rhythm.

    Places the k onsets on a unit circle at angles 2*pi*i/n (where n is
    the number of steps and i is each onset's position index), then sums
    the Euclidean chord lengths between all C(k, 2) pairs of onsets. The
    result is normalized by the maximum possible sum, which is achieved
    when the k onsets are equally spaced around the circle.

    The chord length between two unit-circle points at angles a and b is
    2 * sin(|a - b| / 2). For k equally spaced points the maximum sum is
    the same quantity computed for positions 2*pi*j/k (j = 0..k-1).

    A maximally even rhythm (e.g., euclidean(pulses=4, steps=8)) scores
    1.0. Clustered rhythms score lower, approaching 0 as all onsets
    collapse to the same point.

    Reference: Toussaint, G. (2005). The Euclidean algorithm generates
    traditional musical rhythms. Proceedings of BRIDGES.

    Parameters
    ----------
    rhythm:
        A list of 0/1 onset values with at least 2 onsets.

    Returns
    -------
    float
        Evenness score in (0, 1], where 1.0 means maximally even.

    Raises
    ------
    ValueError
        If the rhythm has fewer than 2 onsets.

    Examples
    --------
    >>> evenness([1, 0, 1, 0, 1, 0, 1, 0])
    1.0
    """
    n = len(rhythm)
    onset_indices = [i for i, v in enumerate(rhythm) if v == 1]
    k = len(onset_indices)
    if k < 2:
        raise ValueError(f"evenness requires at least 2 onsets, got {k}")

    # Sum chord lengths between all pairs of actual onsets
    actual = 0.0
    for a in range(k):
        for b in range(a + 1, k):
            angle_a = 2.0 * math.pi * onset_indices[a] / n
            angle_b = 2.0 * math.pi * onset_indices[b] / n
            actual += 2.0 * math.sin(abs(angle_a - angle_b) / 2.0)

    # Maximum sum: k equally spaced points on the unit circle
    max_sum = 0.0
    for a in range(k):
        for b in range(a + 1, k):
            angle_diff = 2.0 * math.pi * (b - a) / k
            max_sum += 2.0 * math.sin(angle_diff / 2.0)

    return float(actual / max_sum)


def syncopation(rhythm: list[int]) -> int:
    """Compute Keith's (1991) syncopation measure for a binary rhythm.

    A syncopation occurs when an onset falls on a metrically weak beat
    immediately followed by a rest at the next metrically stronger beat.
    The contribution of each such event is the difference in metric weight
    between the stronger beat (rest) and the weaker beat (onset).

    Metric weight function for position i in a rhythm of n steps:
    - weight(0) = n  (the downbeat has the highest weight)
    - weight(i) = the largest power of 2 that divides i, for i > 0

    A syncopation at position i contributes weight(next) - weight(i)
    to the total, but only when rhythm[i] = 1, rhythm[next] = 0, and
    weight(next) > weight(i).

    The measure is best defined when n is a power of 2 (binary meter),
    but the weight function generalizes to any n.

    Reference: Keith, M. (1991). From Polychords to Polya: Adventures in
    Musical Combinatorics. Vinculum Press.

    Parameters
    ----------
    rhythm:
        A list of 0/1 onset values.

    Returns
    -------
    int
        Total syncopation score (0 for no syncopation, positive otherwise).

    Examples
    --------
    >>> syncopation([1, 0, 1, 0, 1, 0, 1, 0])
    0
    """
    n = len(rhythm)
    if n == 0:
        return 0

    def weight(i: int) -> int:
        if i == 0:
            return n
        # Largest power of 2 dividing i
        w = 1
        x = i
        while x % 2 == 0:
            w *= 2
            x //= 2
        return w

    total = 0
    for i in range(n):
        if rhythm[i] == 1:
            j = (i + 1) % n
            if rhythm[j] == 0:
                wi = weight(i)
                wj = weight(j)
                if wj > wi:
                    total += wj - wi
    return total


def rhythmic_oddity(rhythm: list[int]) -> bool:
    """Check whether a rhythm has Pressing's rhythmic oddity property.

    A rhythm has the rhythmic oddity property if no two onsets are
    diametrically opposite on the rhythm circle - that is, no two onset
    positions p and q satisfy (q - p) mod n == n/2, where n is the number
    of steps. Equivalently, no two onsets partition the cycle into two
    equal halves.

    If n is odd there can be no equal partition, so all rhythms with odd
    step counts trivially have the property.

    Reference: Pressing, J. (1983). Cognitive isomorphisms between pitch
    and rhythm in world musics: West Africa, the Balkans and Western
    tonality. Studies in Music, 17, 38-61.

    Parameters
    ----------
    rhythm:
        A list of 0/1 onset values.

    Returns
    -------
    bool
        True if the rhythm has the rhythmic oddity property (no diametrically
        opposite onset pair exists).

    Examples
    --------
    >>> rhythmic_oddity([1, 0, 0, 1, 0, 0, 1, 0])  # son clave
    True
    >>> rhythmic_oddity([1, 0, 0, 0, 1, 0, 0, 0])  # two opposite onsets
    False
    """
    n = len(rhythm)
    if n % 2 != 0:
        # Odd step count: no equal partition possible
        return True

    half = n // 2
    onset_set = {i for i, v in enumerate(rhythm) if v == 1}
    return all((p + half) % n not in onset_set for p in onset_set)
