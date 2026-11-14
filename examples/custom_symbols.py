"""♯・♭で表記する独自の具体クラスの定義.

体系を束ねる中間クラスを ``abstract=True`` で作り、各抽象基底と組み合わせる。
"""

from aulos import base
from aulos.western import WesternTag
from aulos.western import equal
from aulos.western import letters
from aulos.western.templates import chords
from aulos.western.templates import scales

typeset = base.Symbols(letters, "♯", "♭", 4, 4, 4)


class Typeset(base.Definition[WesternTag], abstract=True):
    notation = equal.notation
    symbols = typeset
    tag = WesternTag
    tuning = equal.tuning


class PitchClass(Typeset, base.PitchClass[WesternTag]):
    pass


class Pitch(Typeset, base.Pitch[WesternTag]):
    pitch_class_type = PitchClass


class Voicing(Typeset, base.Voicing[WesternTag]):
    pitch_type = Pitch
    templates = chords


class Chord(Typeset, base.Chord[WesternTag]):
    pitch_type = Pitch
    voicing_type = Voicing
    templates = chords


class Scale(Typeset, base.Scale[WesternTag]):
    pitch_type = Pitch
    chord_type = Chord
    templates = scales


print(Pitch("C♯4"), Chord("E♭m7").names)
print(Scale("B♭ major").names)
