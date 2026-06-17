"""Tests for Euclidean rhythm generation."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from euclidean_rhythm import euclidean


def test_zero_pulses() -> None:
    assert euclidean(pulses=0, steps=4) == [0, 0, 0, 0]


def test_full_pulses() -> None:
    assert euclidean(pulses=4, steps=4) == [1, 1, 1, 1]


def test_single_pulse() -> None:
    assert euclidean(pulses=1, steps=4) == [1, 0, 0, 0]


def test_son_clave() -> None:
    # The son clave: 3 onsets over 8 steps.
    # Bjorklund trace: [[1],[1],[1]] + [[0],[0],[0],[0],[0]]
    # Round 1: pair 3+3 -> [[1,0],[1,0],[1,0]], remainder [[0],[0]]
    # Round 2: pair 2+2 -> [[1,0,0],[1,0,0]], remainder [[1,0]]
    # Stop (1 remainder). Flatten: [1,0,0,1,0,0,1,0]
    assert euclidean(pulses=3, steps=8) == [1, 0, 0, 1, 0, 0, 1, 0]


def test_bossa_nova() -> None:
    # The bossa nova clave: 5 onsets over 8 steps.
    # Bjorklund trace: [[1]]*5 + [[0]]*3
    # Round 1: pair 3+3 -> [[1,0],[1,0],[1,0]], leftover [[1],[1]] become remainders
    # Round 2: pair 2+2 -> [[1,0,1],[1,0,1]], leftover [[1,0]] becomes remainder
    # Stop (1 remainder). Flatten: [1,0,1,1,0,1,1,0]
    assert euclidean(pulses=5, steps=8) == [1, 0, 1, 1, 0, 1, 1, 0]


def test_four_on_the_floor() -> None:
    # 4 equally spaced beats over 8 steps
    assert euclidean(pulses=4, steps=8) == [1, 0, 1, 0, 1, 0, 1, 0]


def test_two_over_four() -> None:
    assert euclidean(pulses=2, steps=4) == [1, 0, 1, 0]


def test_invalid_steps_zero() -> None:
    with pytest.raises(ValueError, match="steps"):
        euclidean(pulses=0, steps=0)


def test_invalid_pulses_negative() -> None:
    with pytest.raises(ValueError, match="pulses"):
        euclidean(pulses=-1, steps=4)


def test_invalid_pulses_exceed_steps() -> None:
    with pytest.raises(ValueError, match="pulses"):
        euclidean(pulses=5, steps=4)


@given(
    steps=st.integers(min_value=1, max_value=32),
    pulses=st.integers(min_value=0, max_value=32),
)
@settings(max_examples=200)
def test_pulse_count(steps: int, pulses: int) -> None:
    if pulses > steps:
        return
    rhythm = euclidean(pulses=pulses, steps=steps)
    assert sum(rhythm) == pulses


@given(
    steps=st.integers(min_value=1, max_value=32),
    pulses=st.integers(min_value=0, max_value=32),
)
@settings(max_examples=200)
def test_length(steps: int, pulses: int) -> None:
    if pulses > steps:
        return
    rhythm = euclidean(pulses=pulses, steps=steps)
    assert len(rhythm) == steps


@given(
    steps=st.integers(min_value=1, max_value=32),
    pulses=st.integers(min_value=0, max_value=32),
)
@settings(max_examples=200)
def test_binary_values(steps: int, pulses: int) -> None:
    if pulses > steps:
        return
    rhythm = euclidean(pulses=pulses, steps=steps)
    assert all(v in (0, 1) for v in rhythm)
