from aulos.note import BaseKey, BaseNote, BasePitchClass


class PitchClass(
    BasePitchClass,
    intervals=(2, 2, 1, 2, 2, 2, 1),
    symbols_pitchclass=("C", "D", "E", "F", "G", "A", "B"),
    symbols_accidental=("bbb", "bb", "b", "#", "##", "###"),
):
    """
    PitchClass represents a musical pitch class with specific intervals and symbols.

    Attributes:
        intervals (tuple): A tuple representing the intervals between the pitch classes.
        symbols_pitchclass (tuple): A tuple of symbols representing the pitch classes.
        symbols_accidental (tuple): A tuple of symbols representing the accidentals.
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
    pitchclass=PitchClass,
):
    """
    Note class representing a musical note.

    Attributes:
        symbols_notenumber (range): Range of note numbers from 0 to 127.
        symbols_octave (tuple): Tuple of octave symbols from -1 to 9.
        pitchclass (PitchClass): The pitch class associated with the note.
    """


class Key(
    BaseKey[PitchClass],
    accidental=1,
    pitchclass=PitchClass,
):
    """
    Represents a musical key.

    Attributes:
        accidental (int): The accidental value of the key (e.g., 1 for sharp, -1 for flat).
        pitchclass (PitchClass): The pitch class associated with the key.
    """
