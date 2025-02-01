"""
12-TET (12 equal temperament)
---

This module provides classes and functions for working with notes, pitch classes,
and scales in the 12-tone equal temperament system.
It includes definitions for various musical scales and modes.
"""

from .note import Key, Note, PitchClass

# Scales
# Modes
from .scale import (
    Aeorian,
    Aeorian_f5,
    AlteredSuperLocrian,
    Bluenote,
    CombDiminish,
    Diminish,
    Dorian,
    Dorian_f2,
    Dorian_s4,
    HarmonicMinor,
    Ionian,
    Ionian_s5,
    Locrian,
    Locrian_n6,
    Lydian,
    Lydian_f7,
    Lydian_s2,
    Lydian_s5,
    Major,
    MelodicMinor,
    Minor,
    MinorPentatonic,
    Mixolydian,
    Mixolydian_f6,
    Mixolydian_f9,
    Pentatonic,
    Phrygian,
    SuperLocrian,
    Wholetone,
)
from .tuner import Equal12Tuner, JustIntonationTuner, MeantoneTuner, PythagoreanTuner

__all__ = [
    # Modes
    "Aeorian",
    "Aeorian_f5",
    "AlteredSuperLocrian",
    # Scales
    "Bluenote",
    "CombDiminish",
    "Diminish",
    "Dorian",
    "Dorian_f2",
    "Dorian_s4",
    "Equal12Tuner",
    "HarmonicMinor",
    "Ionian",
    "Ionian_s5",
    # tuners
    "JustIntonationTuner",
    # Note classes
    "Key",
    "Locrian",
    "Locrian_n6",
    "Lydian",
    "Lydian_f7",
    "Lydian_s2",
    "Lydian_s5",
    "Major",
    "MeantoneTuner",
    "MelodicMinor",
    "Minor",
    "MinorPentatonic",
    "Mixolydian",
    "Mixolydian_f6",
    "Mixolydian_f9",
    "Note",
    "Pentatonic",
    "Phrygian",
    "PitchClass",
    "PythagoreanTuner",
    "SuperLocrian",
    "Wholetone",
]
