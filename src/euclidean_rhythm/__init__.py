"""Euclidean rhythms and geometric rhythm analysis in pure Python."""

from .analysis import evenness, is_euclidean, rhythmic_oddity, syncopation
from .generation import euclidean
from .metrics import (
    inter_onset_intervals,
    ioi_histogram,
    offbeatness,
    onset_positions,
    pattern_from_onsets,
)
from .operations import complement, necklace, rotate

__all__ = [
    "complement",
    "euclidean",
    "evenness",
    "inter_onset_intervals",
    "ioi_histogram",
    "is_euclidean",
    "necklace",
    "offbeatness",
    "onset_positions",
    "pattern_from_onsets",
    "rhythmic_oddity",
    "rotate",
    "syncopation",
]
__version__ = "0.3.0"
