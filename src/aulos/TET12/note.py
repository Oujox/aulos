from aulos._core import BaseKey, BaseNote, BasePitchClass


class PitchClass(
    BasePitchClass,
    intervals=(2, 2, 1, 2, 2, 2, 1),
    symbols_pitchclass=("C", "D", "E", "F", "G", "A", "B"),
    symbols_accidental=("bbb", "bb", "b", "#", "##", "###"),
):
    """
    Represents a musical pitch class, which is a set of all pitches that are a whole number of octaves apart.

    This class extends the BasePitchClass and provides specific intervals and symbols for the pitch class.
    It is used to define the basic properties of musical notes in terms of their pitch class.
    """


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
    reference_notenumber=60,
    pitchclass=PitchClass,
):
    """
    Represents a musical note with various properties and methods for manipulation.

    This class extends the BaseNote and associates it with a specific PitchClass.
    It provides a range of note numbers and octave symbols, allowing for the representation
    and manipulation of musical notes in a theoretical context.
    """


class Key(
    BaseKey[PitchClass],
    accidental=1,
    pitchclass=PitchClass,
):
    """
    Represents a musical key in a theoretical context.

    This class extends the BaseKey and is associated with a specific PitchClass.
    It provides functionality to define and manipulate musical keys, including handling accidentals.
    """
