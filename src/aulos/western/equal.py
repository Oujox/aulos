"""コンマのない西洋式七文字記譜と12平均律."""

from fractions import Fraction

from aulos.base import Chord as BaseChord
from aulos.base import Definition
from aulos.base import Notation
from aulos.base import Pitch as BasePitch
from aulos.base import PitchClass as BasePitchClass
from aulos.base import Scale as BaseScale
from aulos.base import Symbols
from aulos.base import Temperament
from aulos.base import Tuning
from aulos.base import Voicing as BaseVoicing
from aulos.western import WesternTag
from aulos.western import chain
from aulos.western import letters
from aulos.western.templates import chords
from aulos.western.templates import scales

notation = Notation[WesternTag](chain)
symbols = Symbols(letters, "#", "b", 4, 4, 4)
tuning = Tuning(Temperament.equal_division((2, 3), 12, Fraction(2)), (100.0,))


class _Equal(Definition[WesternTag], abstract=True):
    """七文字の記譜・表示規約と12平均律を共有する中間定義."""

    notation = notation
    symbols = symbols
    tag = WesternTag
    tuning = tuning


class PitchClass(_Equal, BasePitchClass[WesternTag]):
    """C#などの音名から作る音高クラス."""


class Pitch(_Equal, BasePitch[WesternTag]):
    """C#4などの音名から作る音高."""

    pitch_class_type = PitchClass


class Voicing(_Equal, BaseVoicing[WesternTag]):
    """m7などのテンプレート名から作る音程列."""

    pitch_type = Pitch
    templates = chords


class Chord(_Equal, BaseChord[WesternTag]):
    """Cm7などのコード記号から作る和音."""

    pitch_type = Pitch
    voicing_type = Voicing
    templates = chords


class Scale(_Equal, BaseScale[WesternTag]):
    """C majorなどの音階名から作る音階."""

    pitch_type = Pitch
    chord_type = Chord
    templates = scales


__all__ = ["Chord", "Pitch", "PitchClass", "Scale", "Voicing", "notation", "symbols", "tuning"]
