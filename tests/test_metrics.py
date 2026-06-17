"""Tests for metric-position and inter-onset interval analysis."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from euclidean_rhythm import (
    euclidean,
    inter_onset_intervals,
    ioi_histogram,
    offbeatness,
    onset_positions,
    pattern_from_onsets,
)
from euclidean_rhythm.metrics import (
    _offbeat_positions_divisor_union,
    _offbeat_positions_gcd,
)

# ---------------------------------------------------------------------------
# offbeatness
# ---------------------------------------------------------------------------


def test_offbeatness_son_clave() -> None:
    # son clave [1,0,0,1,0,0,1,0], n=8
    # Off-beat positions in 8: {1,3,5,7} (odd indices, gcd(p,8)==1 only for p=1,3,5,7)
    # Onsets at 0, 3, 6. Only 3 is off-beat.
    assert offbeatness([1, 0, 0, 1, 0, 0, 1, 0]) == 1


def test_offbeatness_bossa_nova() -> None:
    # bossa nova [1,0,1,1,0,1,1,0], n=8
    # Off-beat positions: {1,3,5,7}. Onsets at 0,2,3,5,6. Off-beat onsets: 3, 5.
    assert offbeatness([1, 0, 1, 1, 0, 1, 1, 0]) == 2


def test_offbeatness_all_onsets_on_beat() -> None:
    # [1,0,1,0,1,0,1,0], n=8: onsets at 0,2,4,6. gcd(0,8)=8, gcd(2,8)=2, gcd(4,8)=4, gcd(6,8)=2.
    # None coprime to 8. All on-beat.
    assert offbeatness([1, 0, 1, 0, 1, 0, 1, 0]) == 0


def test_offbeatness_n12_known_offbeat_set() -> None:
    # n=12: off-beat positions are {1,5,7,11}
    # Rhythm with onsets at those positions
    rhythm = pattern_from_onsets(positions=[1, 5, 7, 11], steps=12)
    assert offbeatness(rhythm) == 4


def test_offbeatness_n16_off_beat_set() -> None:
    # n=16: off-beat positions are the 8 odd indices {1,3,5,7,9,11,13,15}
    # All 8 are odd; phi(16) = 8
    odd_onsets = list(range(1, 16, 2))  # [1,3,5,7,9,11,13,15]
    rhythm = pattern_from_onsets(positions=odd_onsets, steps=16)
    assert offbeatness(rhythm) == 8


def test_offbeatness_zero_onsets_counts_zero() -> None:
    # No onsets -> offbeatness is 0
    assert offbeatness([0, 0, 0, 0]) == 0


def test_offbeatness_raises_empty() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        offbeatness([])


def test_offbeatness_between_zero_and_onset_count() -> None:
    for steps in range(2, 13):
        for pulses in range(steps + 1):
            rhythm = euclidean(pulses=pulses, steps=steps)
            ob = offbeatness(rhythm)
            assert 0 <= ob <= pulses


def test_offbeatness_n12_off_beat_set_exact() -> None:
    # Verify the documented example: n=12 off-beat positions are {1,5,7,11}
    gcd_set = _offbeat_positions_gcd(12)
    assert gcd_set == frozenset({1, 5, 7, 11})


def test_offbeatness_n16_off_beat_set_exact() -> None:
    # Verify the documented example: n=16 off-beat positions are the 8 odd indices
    gcd_set = _offbeat_positions_gcd(16)
    assert gcd_set == frozenset(range(1, 16, 2))


def test_gcd_and_divisor_union_characterizations_agree() -> None:
    # Both characterizations of off-beat positions must agree for n in 2..64.
    # This validates the comment in offbeatness() that documents both methods.
    for n in range(2, 65):
        gcd_set = _offbeat_positions_gcd(n)
        div_set = _offbeat_positions_divisor_union(n)
        assert gcd_set == div_set, (
            f"Characterizations disagree at n={n}: "
            f"gcd={sorted(gcd_set)} vs divisor-union={sorted(div_set)}"
        )


# ---------------------------------------------------------------------------
# inter_onset_intervals
# ---------------------------------------------------------------------------


def test_ioi_son_clave() -> None:
    # [1,0,0,1,0,0,1,0]: onsets at 0,3,6. Gaps: 3-0=3, 6-3=3, (0+8)-6=2.
    assert inter_onset_intervals([1, 0, 0, 1, 0, 0, 1, 0]) == [3, 3, 2]


def test_ioi_bossa_nova() -> None:
    # [1,0,1,1,0,1,1,0]: onsets at 0,2,3,5,6. Gaps: 2,1,2,1,2.
    assert inter_onset_intervals([1, 0, 1, 1, 0, 1, 1, 0]) == [2, 1, 2, 1, 2]


def test_ioi_single_onset_wraps_to_n() -> None:
    # Single onset at position 0: gap wraps all the way around.
    assert inter_onset_intervals([1, 0, 0, 0]) == [4]


def test_ioi_single_onset_not_at_zero() -> None:
    # Single onset at position 2 in 5 steps: the one interval spans the full cycle.
    result = inter_onset_intervals([0, 0, 1, 0, 0])
    assert result == [5]
    assert sum(result) == 5


def test_ioi_sum_equals_n() -> None:
    rhythm = [1, 0, 0, 1, 0, 0, 1, 0]
    iois = inter_onset_intervals(rhythm)
    assert sum(iois) == len(rhythm)


def test_ioi_sum_equals_n_bossa() -> None:
    rhythm = [1, 0, 1, 1, 0, 1, 1, 0]
    iois = inter_onset_intervals(rhythm)
    assert sum(iois) == len(rhythm)


def test_ioi_raises_no_onsets() -> None:
    with pytest.raises(ValueError, match="onset"):
        inter_onset_intervals([0, 0, 0, 0])


def test_ioi_raises_empty() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        inter_onset_intervals([])


def test_ioi_all_onsets() -> None:
    # All positions are onsets: every gap is 1.
    rhythm = [1, 1, 1, 1]
    assert inter_onset_intervals(rhythm) == [1, 1, 1, 1]


# ---------------------------------------------------------------------------
# ioi_histogram
# ---------------------------------------------------------------------------


def test_histogram_son_clave() -> None:
    # IOIs are [3,3,2]: {3: 2, 2: 1}
    assert ioi_histogram([1, 0, 0, 1, 0, 0, 1, 0]) == {3: 2, 2: 1}


def test_histogram_bossa_nova() -> None:
    # IOIs are [2,1,2,1,2]: {2: 3, 1: 2}
    assert ioi_histogram([1, 0, 1, 1, 0, 1, 1, 0]) == {2: 3, 1: 2}


def test_histogram_counts_sum_to_onset_count() -> None:
    rhythm = euclidean(pulses=5, steps=16)
    hist = ioi_histogram(rhythm)
    assert sum(hist.values()) == 5


def test_histogram_raises_no_onsets() -> None:
    with pytest.raises(ValueError, match="onset"):
        ioi_histogram([0, 0, 0])


# ---------------------------------------------------------------------------
# onset_positions
# ---------------------------------------------------------------------------


def test_onset_positions_son_clave() -> None:
    assert onset_positions([1, 0, 0, 1, 0, 0, 1, 0]) == [0, 3, 6]


def test_onset_positions_empty_rhythm() -> None:
    assert onset_positions([]) == []


def test_onset_positions_no_onsets() -> None:
    assert onset_positions([0, 0, 0, 0]) == []


def test_onset_positions_all_onsets() -> None:
    assert onset_positions([1, 1, 1]) == [0, 1, 2]


# ---------------------------------------------------------------------------
# pattern_from_onsets
# ---------------------------------------------------------------------------


def test_pattern_from_onsets_son_clave() -> None:
    assert pattern_from_onsets(positions=[0, 3, 6], steps=8) == [1, 0, 0, 1, 0, 0, 1, 0]


def test_pattern_from_onsets_empty_positions() -> None:
    assert pattern_from_onsets(positions=[], steps=4) == [0, 0, 0, 0]


def test_pattern_from_onsets_raises_invalid_steps() -> None:
    with pytest.raises(ValueError, match="steps"):
        pattern_from_onsets(positions=[], steps=0)


def test_pattern_from_onsets_raises_out_of_range() -> None:
    with pytest.raises(ValueError, match="out of range"):
        pattern_from_onsets(positions=[8], steps=8)


def test_pattern_from_onsets_raises_duplicates() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        pattern_from_onsets(positions=[2, 2], steps=5)


# ---------------------------------------------------------------------------
# Round-trip: onset_positions <-> pattern_from_onsets
# ---------------------------------------------------------------------------


def test_round_trip_positions_to_pattern() -> None:
    original = [1, 0, 1, 1, 0, 1, 1, 0]
    positions = onset_positions(original)
    reconstructed = pattern_from_onsets(positions=positions, steps=len(original))
    assert reconstructed == original


def test_round_trip_pattern_to_positions() -> None:
    positions = [0, 3, 6]
    pattern = pattern_from_onsets(positions=positions, steps=8)
    recovered = onset_positions(pattern)
    assert recovered == positions


# ---------------------------------------------------------------------------
# Hypothesis property tests
# ---------------------------------------------------------------------------


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=1, max_size=32).filter(
        lambda r: any(v == 1 for v in r)
    )
)
@settings(max_examples=300)
def test_ioi_always_sum_to_n(rhythm: list[int]) -> None:
    assert sum(inter_onset_intervals(rhythm)) == len(rhythm)


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=1, max_size=32).filter(
        lambda r: any(v == 1 for v in r)
    )
)
@settings(max_examples=300)
def test_ioi_all_positive(rhythm: list[int]) -> None:
    for interval in inter_onset_intervals(rhythm):
        assert interval > 0


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=1, max_size=32)
)
@settings(max_examples=300)
def test_offbeatness_in_range(rhythm: list[int]) -> None:
    ob = offbeatness(rhythm)
    onset_count = sum(rhythm)
    assert 0 <= ob <= onset_count


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=1, max_size=32).filter(
        lambda r: any(v == 1 for v in r)
    ),
    shift=st.integers(min_value=0, max_value=31),
)
@settings(max_examples=300)
def test_rotation_preserves_ioi_multiset(rhythm: list[int], shift: int) -> None:
    # Rotating the rhythm by any amount cyclically permutes the IOI sequence
    # but preserves the multiset (histogram).
    from euclidean_rhythm import rotate

    n = len(rhythm)
    rotated = rotate(rhythm, steps=shift % n)
    assert sorted(inter_onset_intervals(rhythm)) == sorted(inter_onset_intervals(rotated))


@given(
    rhythm=st.lists(st.integers(min_value=0, max_value=1), min_size=1, max_size=32)
)
@settings(max_examples=300)
def test_round_trip_property(rhythm: list[int]) -> None:
    positions = onset_positions(rhythm)
    reconstructed = pattern_from_onsets(positions=positions, steps=len(rhythm))
    assert reconstructed == rhythm
