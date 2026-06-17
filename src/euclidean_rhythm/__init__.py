"""Euclidean rhythms and geometric rhythm analysis in pure Python."""

from .analysis import evenness, rhythmic_oddity, syncopation
from .generation import euclidean
from .metrics import (
    inter_onset_intervals,
    ioi_histogram,
    offbeatness,
    onset_positions,
    pattern_from_onsets,
)
from .operations import necklace, rotate

__all__ = [
    "euclidean",
    "evenness",
    "inter_onset_intervals",
    "ioi_histogram",
    "necklace",
    "offbeatness",
    "onset_positions",
    "pattern_from_onsets",
    "rhythmic_oddity",
    "rotate",
    "syncopation",
]
__version__ = "0.2.0"
