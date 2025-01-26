from ..note import BaseKey, BaseNote, BasePitchClass


class PitchClass(
    BasePitchClass,
    intervals=(2, 2, 1, 2, 2, 2, 1),
    symbols_pitchclass=("C", "D", "E", "F", "G", "A", "B"),
    symbols_accidental=("bbb", "bb", "b", "#", "##", "###"),
):
    """ """


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
    reference_octave=5,
    pitchclass=PitchClass,
):
    """ """


class Key(
    BaseKey[PitchClass],
    accidental=1,
    pitchclass=PitchClass,
):
    """ """
