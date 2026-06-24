"""Tests for rhythm analysis functions."""

from __future__ import annotations

import math

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from euclidean_rhythm import (
    euclidean,
    evenness,
    is_euclidean,
    necklace,
    rhythmic_oddity,
    rotate,
    syncopation,
)


def test_evenness_equally_spaced_4_in_8() -> None:
    rhythm = [1, 0, 1, 0, 1, 0, 1, 0]
    assert math.isclose(evenness(rhythm), 1.0, abs_tol=1e-9)


def test_evenness_equally_spaced_2_in_4() -> None:
    rhythm = [1, 0, 1, 0]
    assert math.isclose(evenness(rhythm), 1.0, abs_tol=1e-9)


def test_evenness_clustered_less_than_even() -> None:
    even = [1, 0, 1, 0]  # 2 in 4, maximally even
    clustered = [1, 1, 0, 0]  # 2 in 4, adjacent onsets
    assert evenness(clustered) < evenness(even)


def test_evenness_maximally_even_from_euclidean() -> None:
    # 4 in 8 is maximally even
    rhythm = euclidean(pulses=4, steps=8)
    assert math.isclose(evenness(rhythm), 1.0, abs_tol=1e-9)


def test_evenness_raises_zero_onsets() -> None:
    with pytest.raises(ValueError, match="onsets"):
        evenness([0, 0, 0, 0])


def test_evenness_raises_one_onset() -> None:
    with pytest.raises(ValueError, match="onsets"):
        evenness([1, 0, 0, 0])


def test_evenness_range() -> None:
    rhythm = euclidean(pulses=3, steps=8)
    score = evenness(rhythm)
    assert 0.0 < score <= 1.0


def test_syncopation_no_syncopation() -> None:
    # All onsets on beats 0, 2, 4, 6 in 8 steps.
    # For i=0: onset, next=1 (rest). weight(0)=8, weight(1)=1. wj=1 < wi=8. No contribution.
    # For i=2: onset, next=3 (rest). weight(2)=2, weight(3)=1. wj=1 < wi=2. No contribution.
    # For i=4: onset, next=5. weight(4)=4, weight(5)=1. No contribution.
    # For i=6: onset, next=7. weight(6)=2, weight(7)=1. No contribution.
    # Total = 0
    assert syncopation([1, 0, 1, 0, 1, 0, 1, 0]) == 0


def test_syncopation_basic_syncopation() -> None:
    # [0, 1, 0, 0] in 4 steps: onset at position 1 (odd beat)
    # i=1: onset, next=2 (rest). weight(1)=1, weight(2)=2. wj=2 > wi=1. Contribution: 1.
    assert syncopation([0, 1, 0, 0]) == 1


def test_syncopation_son_clave() -> None:
    # son clave [1,0,0,1,0,0,1,0], n=8
    # i=0 (onset): next=1 (rest). weight(0)=8, weight(1)=1. wj < wi. No contribution.
    # i=3 (onset): next=4 (rest). weight(3)=1, weight(4)=4. wj=4 > wi=1. Contribution: 3.
    # i=6 (onset): next=7 (rest). weight(6)=2, weight(7)=1. wj < wi. No contribution.
    # Total = 3
    assert syncopation([1, 0, 0, 1, 0, 0, 1, 0]) == 3


def test_syncopation_empty() -> None:
    assert syncopation([]) == 0


def test_syncopation_nonnegative() -> None:
    for steps in range(1, 9):
        for pulses in range(steps + 1):
            rhythm = euclidean(pulses=pulses, steps=steps)
            assert syncopation(rhythm) >= 0


def test_rhythmic_oddity_son_clave() -> None:
    # son clave [1,0,0,1,0,0,1,0]: onsets at 0, 3, 6
    # Check: (0+4)%8=4 not onset, (3+4)%8=7 not onset, (6+4)%8=2 not onset
    assert rhythmic_oddity([1, 0, 0, 1, 0, 0, 1, 0]) is True


def test_rhythmic_oddity_two_opposite() -> None:
    # Onsets at 0 and 4 in 8 steps: diametrically opposite
    assert rhythmic_oddity([1, 0, 0, 0, 1, 0, 0, 0]) is False


def test_rhythmic_oddity_odd_steps() -> None:
    # Odd step count: always has oddity property
    assert rhythmic_oddity([1, 0, 1, 0, 1]) is True


def test_rhythmic_oddity_empty() -> None:
    # No onsets: trivially true
    assert rhythmic_oddity([]) is True


def test_rhythmic_oddity_all_onsets_even_steps() -> None:
    # [1,1,1,1]: onsets at 0,1,2,3. 0 and 2 are diametrically opposite in 4 steps.
    assert rhythmic_oddity([1, 1, 1, 1]) is False


# ---------------------------------------------------------------------------
# is_euclidean
# ---------------------------------------------------------------------------


def test_is_euclidean_son_clave() -> None:
    # E(3, 8) = 10010010 is Euclidean by construction.
    son = euclidean(pulses=3, steps=8)
    assert son == [1, 0, 0, 1, 0, 0, 1, 0]
    assert is_euclidean(son) is True


def test_is_euclidean_all_rotations_of_son_clave() -> None:
    # Every rotation of E(3, 8) is also Euclidean.
    son = euclidean(pulses=3, steps=8)
    for s in range(8):
        assert is_euclidean(rotate(son, steps=s)) is True


def test_is_euclidean_non_euclidean_3_in_8() -> None:
    # 11100000: three onsets bunched together, not maximally even.
    clustered = [1, 1, 1, 0, 0, 0, 0, 0]
    assert sum(clustered) == 3
    # It must differ from the son clave necklace to be non-Euclidean.
    assert necklace(clustered) != necklace(euclidean(pulses=3, steps=8))
    assert is_euclidean(clustered) is False


def test_is_euclidean_bossa_nova_5_in_8() -> None:
    bossa = euclidean(pulses=5, steps=8)
    assert bossa == [1, 0, 1, 1, 0, 1, 1, 0]
    assert is_euclidean(bossa) is True


def test_is_euclidean_e4_16() -> None:
    e = euclidean(pulses=4, steps=16)
    assert e == [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    assert is_euclidean(e) is True


def test_is_euclidean_e2_5() -> None:
    e = euclidean(pulses=2, steps=5)
    assert e == [1, 0, 1, 0, 0]
    assert is_euclidean(e) is True


def test_is_euclidean_bossa_nova_5_16() -> None:
    # The "Bossa-Nova" E(5, 16).
    e = euclidean(pulses=5, steps=16)
    assert e == [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    assert is_euclidean(e) is True


def test_is_euclidean_all_rotations_of_tresillo() -> None:
    # The tresillo is E(3, 8); all rotations are Euclidean.
    tresillo = euclidean(pulses=3, steps=8)
    for s in range(8):
        assert is_euclidean(rotate(tresillo, steps=s)) is True


def test_is_euclidean_all_rests_trivial() -> None:
    # k = 0: all-rest rhythm is trivially Euclidean.
    assert is_euclidean([0, 0, 0, 0, 0]) is True


def test_is_euclidean_all_onsets_trivial() -> None:
    # k = n: all-onset rhythm is trivially Euclidean.
    assert is_euclidean([1, 1, 1, 1]) is True


def test_is_euclidean_single_onset() -> None:
    assert is_euclidean([1, 0, 0, 0]) is True
    assert is_euclidean([0, 1, 0, 0]) is True


def test_is_euclidean_raises_empty() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        is_euclidean([])


def test_is_euclidean_raises_bad_values() -> None:
    with pytest.raises(ValueError, match="0 or 1"):
        is_euclidean([1, 0, 2, 0])


@given(
    pulses=st.integers(min_value=0, max_value=16),
    steps=st.integers(min_value=1, max_value=16),
    shift=st.integers(min_value=0, max_value=31),
)
@settings(max_examples=300)
def test_is_euclidean_true_for_every_generated_rotation(
    pulses: int, steps: int, shift: int
) -> None:
    # Any rotation of a generated Euclidean rhythm must be recognized.
    if pulses > steps:
        pulses = steps
    e = euclidean(pulses=pulses, steps=steps)
    assert is_euclidean(rotate(e, steps=shift % steps)) is True


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=1, max_size=16),
    shift=st.integers(min_value=0, max_value=31),
)
@settings(max_examples=300)
def test_is_euclidean_rotation_invariant(rhythm: list[int], shift: int) -> None:
    # is_euclidean depends only on the rotation class, never on the rotation.
    rotated = rotate(rhythm, steps=shift % len(rhythm))
    assert is_euclidean(rhythm) == is_euclidean(rotated)
