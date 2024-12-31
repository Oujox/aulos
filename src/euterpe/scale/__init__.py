"""Scale
---
* 一般に使用される音階・旋法を提供
"""

from .diatonic import DiatonicScale, NondiatonicScale
# harmonicminor mode
# melodicminor mode
# major mode
from .implements.mode import (Aeorian, Aeorian_f5, AlteredSuperLocrian, Dorian,
                              Dorian_f2, Dorian_s4, Ionian, Ionian_s5, Locrian,
                              Locrian_n6, Lydian, Lydian_f7, Lydian_s2,
                              Lydian_s5, Mixolydian, Mixolydian_f6,
                              Mixolydian_f9, Phrygian, SuperLocrian)
# scale
from .implements.scale import (Bluenote, CombDiminish, Diminish, HarmonicMinor,
                               Major, MelodicMinor, Minor, MinorPentatonic,
                               Pentatonic, Wholetone)
from .mode import Mode
from .scale import Scale

__all__ = [
    "Scale",
    "DiatonicScale",
    "NondiatonicScale",
    "Mode",
    "Major",
    "Minor",
    "MelodicMinor",
    "HarmonicMinor",
    "Pentatonic",
    "MinorPentatonic",
    "Bluenote",
    "Diminish",
    "CombDiminish",
    "Wholetone",
    "Ionian",
    "Dorian",
    "Phrygian",
    "Lydian",
    "Mixolydian",
    "Aeorian",
    "Locrian",
    "Dorian_f2",
    "Lydian_s5",
    "Lydian_f7",
    "Mixolydian_f6",
    "Aeorian_f5",
    "SuperLocrian",
    "Locrian_n6",
    "Ionian_s5",
    "Dorian_s4",
    "Mixolydian_f9",
    "Lydian_s2",
    "AlteredSuperLocrian",
]
