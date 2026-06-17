"""Euclidean rhythm generation via Bjorklund's algorithm."""

from __future__ import annotations


def euclidean(*, pulses: int, steps: int) -> list[int]:
    """Generate an Euclidean rhythm with the given number of pulses and steps.

    Uses Bjorklund's algorithm to distribute ``pulses`` onsets as evenly as
    possible over ``steps`` positions. The result is the canonical front-loaded
    form: the first position is always an onset (when pulses > 0), and the
    distribution is lexicographically maximal (earliest onsets first within
    the even-distribution constraint).

    The algorithm works by iterative Euclidean division of onset and rest
    groups. At each step, rest groups are appended to onset groups until
    only one type of group remains as the remainder. This mirrors the
    Euclidean algorithm for GCD and was described by Bjorklund (2003) in
    the context of neutron accelerator timing.

    Parameters
    ----------
    pulses:
        Number of onsets (1s) in the rhythm. Must satisfy 0 <= pulses <= steps.
    steps:
        Total number of positions in the rhythm. Must be >= 1.

    Returns
    -------
    list[int]
        A list of length ``steps`` containing 0s and 1s, with exactly
        ``pulses`` ones distributed as evenly as possible. The first
        element is 1 when pulses > 0.

    Raises
    ------
    ValueError
        If steps < 1, or if pulses < 0, or if pulses > steps.

    Examples
    --------
    The son clave (3 over 8):

    >>> euclidean(pulses=3, steps=8)
    [1, 0, 0, 1, 0, 0, 1, 0]

    The bossa nova clave (5 over 8):

    >>> euclidean(pulses=5, steps=8)
    [1, 0, 1, 1, 0, 1, 1, 0]
    """
    if steps < 1:
        raise ValueError(f"steps must be >= 1, got {steps}")
    if pulses < 0:
        raise ValueError(f"pulses must be >= 0, got {pulses}")
    if pulses > steps:
        raise ValueError(f"pulses ({pulses}) must be <= steps ({steps})")

    if pulses == 0:
        return [0] * steps
    if pulses == steps:
        return [1] * steps

    # Bjorklund's algorithm: distribute pulses over steps using Euclidean GCD logic.
    # Start with `pulses` singleton groups of [1] and `steps-pulses` of [0].
    # At each iteration, pair each remainder group with a main group by appending.
    # The leftover main groups become the new remainders.
    # Repeat until at most one remainder remains.
    groups: list[list[int]] = [[1]] * pulses
    remainders: list[list[int]] = [[0]] * (steps - pulses)

    while len(remainders) > 1:
        n = min(len(groups), len(remainders))
        new_groups: list[list[int]] = [groups[i] + remainders[i] for i in range(n)]

        if len(groups) > len(remainders):
            # Leftover onset groups become the next round's remainders
            new_remainders: list[list[int]] = groups[len(remainders):]
        elif len(remainders) > len(groups):
            new_remainders = remainders[len(groups):]
        else:
            new_remainders = []

        groups = new_groups
        remainders = new_remainders

        if not remainders:
            break

    result: list[int] = []
    for g in groups:
        result.extend(g)
    for r in remainders:
        result.extend(r)
    return result
