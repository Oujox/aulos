"""
12-TET (12 equal temperament)
---

This module provides various musical scales, modes, and tuners.
Classes:
    Key: Represents a musical key.
    Note: Represents a musical note.
    PitchClass: Represents a pitch class.
Scales and Modes:
    Aeorian: Represents the Aeorian scale.
    Aeorian_f5: Represents the Aeorian flat 5 scale.
    AlteredSuperLocrian: Represents the Altered Super Locrian scale.
    Bluenote: Represents the Bluenote scale.
    CombDiminish: Represents the Comb Diminish scale.
    Diminish: Represents the Diminish scale.
    Dorian: Represents the Dorian scale.
    Dorian_f2: Represents the Dorian flat 2 scale.
    Dorian_s4: Represents the Dorian sharp 4 scale.
    HarmonicMinor: Represents the Harmonic Minor scale.
    Ionian: Represents the Ionian scale.
    Ionian_s5: Represents the Ionian sharp 5 scale.
    Locrian: Represents the Locrian scale.
    Locrian_n6: Represents the Locrian natural 6 scale.
    Lydian: Represents the Lydian scale.
    Lydian_f7: Represents the Lydian flat 7 scale.
    Lydian_s2: Represents the Lydian sharp 2 scale.
    Lydian_s5: Represents the Lydian sharp 5 scale.
    Major: Represents the Major scale.
    MelodicMinor: Represents the Melodic Minor scale.
    Minor: Represents the Minor scale.
    MinorPentatonic: Represents the Minor Pentatonic scale.
    Mixolydian: Represents the Mixolydian scale.
    Mixolydian_f6: Represents the Mixolydian flat 6 scale.
    Mixolydian_f9: Represents the Mixolydian flat 9 scale.
    Pentatonic: Represents the Pentatonic scale.
    Phrygian: Represents the Phrygian scale.
    SuperLocrian: Represents the Super Locrian scale.
    Wholetone: Represents the Wholetone scale.
Tuners:
    Equal12Tuner: Represents the Equal Temperament 12 Tuner.
    JustIntonationTuner: Represents the Just Intonation Tuner.
    MeantoneTuner: Represents the Meantone Tuner.
    PythagoreanTuner: Represents the Pythagorean Tuner.
__all__:
    A list of all public classes and functions provided by this module.
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
