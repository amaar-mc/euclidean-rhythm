"""Tests for rotation and necklace operations."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from euclidean_rhythm import complement, euclidean, necklace, rotate


def test_rotate_basic() -> None:
    assert rotate([1, 0, 0], steps=1) == [0, 0, 1]


def test_rotate_full_cycle() -> None:
    r = [1, 0, 0, 1, 0]
    assert rotate(r, steps=len(r)) == r


def test_rotate_zero_steps() -> None:
    r = [1, 0, 1, 0]
    assert rotate(r, steps=0) == r


def test_rotate_negative() -> None:
    # rotate left -1 == rotate left (n-1) == rotate right 1
    r = [1, 0, 0, 1]
    assert rotate(r, steps=-1) == [1, 1, 0, 0]


def test_rotate_empty() -> None:
    assert rotate([], steps=5) == []


def test_necklace_is_rotation_invariant() -> None:
    r = euclidean(pulses=3, steps=8)
    ref = necklace(r)
    for s in range(8):
        assert necklace(rotate(r, steps=s)) == ref


def test_necklace_idempotent() -> None:
    r = euclidean(pulses=5, steps=8)
    n1 = necklace(r)
    assert necklace(n1) == n1


def test_necklace_empty() -> None:
    assert necklace([]) == []


def test_necklace_lexicographic() -> None:
    # [0, 1, 0, 0] is lex smaller than [1, 0, 0, 0]
    # But [0, 0, 0, 1] is smallest
    assert necklace([1, 0, 0, 0]) == [0, 0, 0, 1]


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=1, max_size=16),
    steps=st.integers(min_value=0, max_value=32),
)
@settings(max_examples=200)
def test_rotate_preserves_length(rhythm: list[int], steps: int) -> None:
    assert len(rotate(rhythm, steps=steps)) == len(rhythm)


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=1, max_size=16),
    steps=st.integers(min_value=0, max_value=32),
)
@settings(max_examples=200)
def test_rotate_preserves_onset_count(rhythm: list[int], steps: int) -> None:
    assert sum(rotate(rhythm, steps=steps)) == sum(rhythm)


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=1, max_size=16),
    steps=st.integers(min_value=0, max_value=32),
)
@settings(max_examples=200)
def test_necklace_rotation_invariant(rhythm: list[int], steps: int) -> None:
    assert necklace(rotate(rhythm, steps=steps)) == necklace(rhythm)


# ---------------------------------------------------------------------------
# complement
# ---------------------------------------------------------------------------


def test_complement_son_clave() -> None:
    # complement(10010010) == 01101101
    son = [1, 0, 0, 1, 0, 0, 1, 0]
    assert complement(son) == [0, 1, 1, 0, 1, 1, 0, 1]


def test_complement_empty() -> None:
    assert complement([]) == []


def test_complement_all_rests() -> None:
    assert complement([0, 0, 0, 0]) == [1, 1, 1, 1]


def test_complement_all_onsets() -> None:
    assert complement([1, 1, 1, 1]) == [0, 0, 0, 0]


def test_complement_preserves_length() -> None:
    r = [1, 0, 1, 1, 0]
    assert len(complement(r)) == len(r)


def test_complement_returns_new_list() -> None:
    r = [1, 0, 1]
    c = complement(r)
    assert c is not r
    assert r == [1, 0, 1]


def test_complement_raises_bad_values() -> None:
    with pytest.raises(ValueError, match="0 or 1"):
        complement([1, 0, 2])


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=0, max_size=32),
)
@settings(max_examples=300)
def test_complement_is_involution(rhythm: list[int]) -> None:
    # Applying complement twice returns the original rhythm.
    assert complement(complement(rhythm)) == rhythm


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=1, max_size=32),
)
@settings(max_examples=300)
def test_complement_onset_count(rhythm: list[int]) -> None:
    # The complement has n - k onsets.
    n = len(rhythm)
    k = sum(rhythm)
    assert sum(complement(rhythm)) == n - k


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=0, max_size=32),
)
@settings(max_examples=300)
def test_complement_preserves_length_property(rhythm: list[int]) -> None:
    assert len(complement(rhythm)) == len(rhythm)
