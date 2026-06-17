"""Euclidean rhythms and geometric rhythm analysis in pure Python."""

from .analysis import evenness, rhythmic_oddity, syncopation
from .generation import euclidean
from .operations import necklace, rotate

__all__ = [
    "euclidean",
    "evenness",
    "necklace",
    "rhythmic_oddity",
    "rotate",
    "syncopation",
]
__version__ = "0.1.0"
