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


def complement(rhythm: list[int]) -> list[int]:
    """Return the rhythmic complement: swap onsets and rests (1 <-> 0).

    Each onset becomes a rest and each rest becomes an onset, preserving the
    length. The complement of a rhythm with k onsets over n steps has n - k
    onsets. Applying complement twice returns the original rhythm (it is an
    involution).

    Note that the complement of the Euclidean rhythm E(k, n) is generally not
    E(n - k, n): swapping onsets and rests does not in general preserve maximal
    evenness. For example, the complement of the son clave E(3, 8) =
    [1, 0, 0, 1, 0, 0, 1, 0] is [0, 1, 1, 0, 1, 1, 0, 1], which is a rotation of
    E(5, 8) here but not for every k and n.

    Parameters
    ----------
    rhythm:
        A list of 0/1 onset values. May be empty (returns an empty list).

    Returns
    -------
    list[int]
        A new list of the same length with every 0 turned into 1 and every 1
        turned into 0.

    Raises
    ------
    ValueError
        If any value is not 0 or 1.

    Examples
    --------
    >>> complement([1, 0, 0, 1, 0, 0, 1, 0])  # son clave
    [0, 1, 1, 0, 1, 1, 0, 1]
    """
    if any(v not in (0, 1) for v in rhythm):
        raise ValueError("rhythm values must be 0 or 1")
    return [1 - v for v in rhythm]
