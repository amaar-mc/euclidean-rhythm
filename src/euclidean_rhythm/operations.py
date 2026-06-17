"""Rotation and necklace operations on binary onset vectors."""

from __future__ import annotations


def rotate(rhythm: list[int], *, steps: int) -> list[int]:
    """Rotate a rhythm left by the given number of steps.

    A left rotation by 1 moves the first element to the end. Rotation is
    applied modulo the length of the rhythm, so rotating by len(rhythm)
    returns the original.

    Parameters
    ----------
    rhythm:
        A list of 0/1 onset values.
    steps:
        Number of positions to rotate left. May be negative (rotates right)
        or exceed len(rhythm) (wraps around).

    Returns
    -------
    list[int]
        The rotated rhythm, same length as the input.

    Examples
    --------
    >>> rotate([1, 0, 0, 1, 0, 0, 1, 0], steps=3)
    [1, 0, 0, 1, 0, 1, 0, 0]
    """
    n = len(rhythm)
    if n == 0:
        return []
    shift = steps % n
    return rhythm[shift:] + rhythm[:shift]


def necklace(rhythm: list[int]) -> list[int]:
    """Return the lexicographically minimal rotation of the rhythm.

    Two rhythms are rotation-equivalent (same necklace) if one can be
    obtained from the other by rotation. The necklace representative is
    the rotation that is smallest in lexicographic order, providing a
    canonical form for comparing rhythm classes.

    Parameters
    ----------
    rhythm:
        A list of 0/1 onset values.

    Returns
    -------
    list[int]
        The lexicographically smallest rotation of ``rhythm``.

    Examples
    --------
    >>> necklace([0, 1, 0, 0])
    [0, 0, 0, 1]
    """
    n = len(rhythm)
    if n == 0:
        return []
    # Try all rotations and pick the lexicographically smallest.
    # Booth's algorithm is O(n) but this O(n^2) version is clear and correct
    # for the small rhythms this library targets.
    best = rhythm[:]
    for i in range(1, n):
        candidate = rhythm[i:] + rhythm[:i]
        if candidate < best:
            best = candidate
    return best
