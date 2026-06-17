"""Metric-position and inter-onset interval analysis."""

from __future__ import annotations

import math


def offbeatness(rhythm: list[int]) -> int:
    """Count onsets that fall on off-beat positions (Toussaint's offbeatness).

    Two equivalent characterizations of off-beat positions in a cycle of n pulses:

    GCD characterization: position p is off-beat iff gcd(p, n) == 1. These are
    the positions that share no common factor with n, so they are never hit by
    any regular subdivision of the cycle.

    Divisor-union characterization: on-beat positions are the union over all
    divisors d of n with 1 < d < n of the sets {k * n / d : k = 0..d-1}. The
    off-beat positions are those in 0..n-1 not in that union (excluding position 0,
    which is the downbeat and always on-beat). Both characterizations produce
    identical off-beat sets; this is verified by tests across n in 2..64.

    Worked examples:
    - n=16: off-beat positions are the 8 odd indices {1,3,5,7,9,11,13,15}.
    - n=12: off-beat positions are {1,5,7,11} (those coprime to 12).

    Note: position 0 is the downbeat. gcd(0, n) = n != 1 for n > 1, so position
    0 is always on-beat, consistent with both characterizations.

    Parameters
    ----------
    rhythm:
        A list of 0/1 onset values. Must be non-empty.

    Returns
    -------
    int
        Count of onsets that fall on off-beat positions, in range [0, sum(rhythm)].

    Raises
    ------
    ValueError
        If the rhythm is empty.

    Examples
    --------
    >>> offbeatness([1, 0, 0, 1, 0, 0, 1, 0])  # son clave, n=8
    2
    """
    if not rhythm:
        raise ValueError("rhythm must be non-empty")
    n = len(rhythm)
    off_beats = _offbeat_positions_gcd(n)
    return sum(1 for p, v in enumerate(rhythm) if v == 1 and p in off_beats)


def _offbeat_positions_gcd(n: int) -> frozenset[int]:
    """Return the set of off-beat positions for a cycle of n pulses (GCD method).

    Position p is off-beat iff gcd(p, n) == 1 and p != 0.
    Position 0 (downbeat) is excluded even though gcd(0, n) = n.
    """
    return frozenset(p for p in range(1, n) if math.gcd(p, n) == 1)


def _offbeat_positions_divisor_union(n: int) -> frozenset[int]:
    """Return the set of off-beat positions for a cycle of n pulses (divisor-union method).

    On-beat positions are 0 plus the union of {k * n // d for k in 0..d-1}
    for each proper divisor d of n with 1 < d < n. Off-beat positions are
    the complement in 1..n-1.
    """
    on_beats: set[int] = {0}
    for d in range(2, n):
        if n % d == 0:
            for k in range(d):
                on_beats.add(k * n // d)
    return frozenset(p for p in range(1, n) if p not in on_beats)


def inter_onset_intervals(rhythm: list[int]) -> list[int]:
    """Return the inter-onset intervals (IOIs) for the rhythm.

    Computes the gap in pulses between each consecutive pair of onsets,
    wrapping from the last onset back to the first onset around the cycle.
    The intervals always sum to n (the total number of pulses).

    Parameters
    ----------
    rhythm:
        A list of 0/1 onset values. Must contain at least one onset.

    Returns
    -------
    list[int]
        A list of k positive integers (where k is the onset count), each
        giving the number of pulses from one onset to the next around the
        cycle. Their sum equals len(rhythm).

    Raises
    ------
    ValueError
        If the rhythm has no onsets, or if the rhythm is empty.

    Examples
    --------
    >>> inter_onset_intervals([1, 0, 0, 1, 0, 0, 1, 0])  # son clave
    [3, 3, 2]
    """
    if not rhythm:
        raise ValueError("rhythm must be non-empty")
    positions = [i for i, v in enumerate(rhythm) if v == 1]
    if not positions:
        raise ValueError("rhythm must contain at least one onset")
    n = len(rhythm)
    k = len(positions)
    if k == 1:
        # One onset spans the whole cycle.
        return [n]
    iois: list[int] = []
    for idx in range(k):
        current = positions[idx]
        nxt = positions[(idx + 1) % k]
        gap = (nxt - current) % n
        iois.append(gap)
    return iois


def ioi_histogram(rhythm: list[int]) -> dict[int, int]:
    """Return a histogram of the inter-onset intervals.

    Parameters
    ----------
    rhythm:
        A list of 0/1 onset values. Must contain at least one onset.

    Returns
    -------
    dict[int, int]
        A mapping from interval length to the number of times that interval
        appears in the IOI sequence.

    Raises
    ------
    ValueError
        If the rhythm has no onsets or is empty.

    Examples
    --------
    >>> ioi_histogram([1, 0, 0, 1, 0, 0, 1, 0])  # son clave
    {3: 2, 2: 1}
    """
    iois = inter_onset_intervals(rhythm)
    hist: dict[int, int] = {}
    for interval in iois:
        hist[interval] = hist.get(interval, 0) + 1
    return hist


def onset_positions(rhythm: list[int]) -> list[int]:
    """Return the indices of the onsets in a 0/1 rhythm vector.

    This is the complementary converter for the 0/1 binary pattern representation.
    Use pattern_from_onsets to convert back, completing the round-trip.

    Parameters
    ----------
    rhythm:
        A list of 0/1 onset values. May be empty (returns empty list).

    Returns
    -------
    list[int]
        Sorted list of zero-based pulse indices at which onsets occur.

    Examples
    --------
    >>> onset_positions([1, 0, 0, 1, 0, 0, 1, 0])
    [0, 3, 6]
    """
    return [i for i, v in enumerate(rhythm) if v == 1]


def pattern_from_onsets(*, positions: list[int], steps: int) -> list[int]:
    """Build a 0/1 rhythm vector from onset positions.

    This is the inverse of onset_positions: given a sorted list of onset
    indices and the total step count, returns the full binary pattern.

    Parameters
    ----------
    positions:
        Sorted list of zero-based onset indices. All values must be in
        range [0, steps - 1]. May be empty.
    steps:
        Total number of pulses. Must be >= 1.

    Returns
    -------
    list[int]
        A list of length ``steps`` with 1 at each onset position and 0 elsewhere.

    Raises
    ------
    ValueError
        If steps < 1, or if any position is out of range [0, steps - 1],
        or if any position appears more than once.

    Examples
    --------
    >>> pattern_from_onsets(positions=[0, 3, 6], steps=8)
    [1, 0, 0, 1, 0, 0, 1, 0]
    """
    if steps < 1:
        raise ValueError(f"steps must be >= 1, got {steps}")
    if len(positions) != len(set(positions)):
        raise ValueError("positions must not contain duplicates")
    for p in positions:
        if p < 0 or p >= steps:
            raise ValueError(f"position {p} is out of range [0, {steps - 1}]")
    pattern = [0] * steps
    for p in positions:
        pattern[p] = 1
    return pattern
