from aulos._core import BasePitchClass


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
