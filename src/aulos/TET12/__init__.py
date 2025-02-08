"""
TET12 Module Initialization
---------------------------

This module initializes the TET12 package, which is part of the Aulos library.
It provides functionalities for handling 12-tone equal temperament systems,
including musical notes, scales, and tuning systems.

Modules and Classes:
- note: Contains classes for musical notes, keys, and pitch classes.
- scale: Provides various musical scales and modes.
- tuner: Includes different tuning systems like Equal Temperament, Just Intonation, and more.

The `__all__` list defines the public API of the module, specifying which components
are accessible when the module is imported.
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
    "Aeorian",
    "Aeorian_f5",
    "AlteredSuperLocrian",
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
    "JustIntonationTuner",
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
