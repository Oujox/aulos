from aulos._core import BaseNote

from .pitchclass import PitchClass


class Note(
    BaseNote[PitchClass],
    symbols_notenumber=range(128),
    symbols_octave=(
        "<N>-1",
        "<N>0",
        "<N>1",
        "<N>2",
        "<N>3",
        "<N>4",
        "<N>5",
        "<N>6",
        "<N>7",
        "<N>8",
        "<N>9",
    ),
    pitchclass=PitchClass,
):
    """
    Represents a musical note with various properties and methods for manipulation.

    This class extends the BaseNote and associates it with a specific PitchClass.
    It provides a range of note numbers and octave symbols, allowing for the representation
    and manipulation of musical notes in a theoretical context.
    """
