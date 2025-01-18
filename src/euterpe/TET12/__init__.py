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
from .scale import (Aeorian, Aeorian_f5, AlteredSuperLocrian, Bluenote,
                    CombDiminish, Diminish, Dorian, Dorian_f2, Dorian_s4,
                    HarmonicMinor, Ionian, Ionian_s5, Locrian, Locrian_n6,
                    Lydian, Lydian_f7, Lydian_s2, Lydian_s5, Major,
                    MelodicMinor, Minor, MinorPentatonic, Mixolydian,
                    Mixolydian_f6, Mixolydian_f9, Pentatonic, Phrygian,
                    SuperLocrian, Wholetone)
from .tuner import (Equal12Tuner, JustIntonationTuner, MeantoneTuner,
                    PythagoreanTuner)

__all__ = [
    # Note classes
    "Key",
    "Note",
    "PitchClass",
    # Modes
    "Aeorian",
    "Aeorian_f5",
    "AlteredSuperLocrian",
    "Dorian",
    "Dorian_f2",
    "Dorian_s4",
    "Ionian",
    "Ionian_s5",
    "Locrian",
    "Locrian_n6",
    "Lydian",
    "Lydian_f7",
    "Lydian_s2",
    "Lydian_s5",
    "Mixolydian",
    "Mixolydian_f6",
    "Mixolydian_f9",
    "Phrygian",
    "SuperLocrian",
    # Scales
    "Bluenote",
    "CombDiminish",
    "Diminish",
    "HarmonicMinor",
    "Major",
    "MelodicMinor",
    "Minor",
    "MinorPentatonic",
    "Pentatonic",
    "Wholetone",
    # tuners
    "JustIntonationTuner",
    "MeantoneTuner",
    "PythagoreanTuner",
    "Equal12Tuner",
]
