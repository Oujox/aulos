from euterpe import _Key
from euterpe import _Note
from euterpe import _PitchClass


class PitchClass(
    _PitchClass,
    intervals=(2, 2, 1, 2, 2, 2, 1),
    symbols_pitchclass=("C", "D", "E", "F", "G", "A", "B"),
    symbols_accidental=("bbb", "bb", "b", "#", "##", "###"),
):
    """ """

class Note(
    _Note,
    symbols_notenumber=range(128),
    symbols_octave=("<N>-1","<N>0","<N>1","<N>2","<N>3","<N>4","<N>5","<N>6","<N>7","<N>8","<N>9"),
    reference_notenumber=60,
    reference_octave=5,
    base=PitchClass,
):
    """ """

class Key(
    _Key,
    accidental=1,
    base=PitchClass,
):
    """ """