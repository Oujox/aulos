"""完全5度から作る五文字の連鎖記譜.

基本文字a b c d eを高さ順に配置する独立した体系で、調律は束ねない。
+と~は上方・下方の変化記号。
"""

from fractions import Fraction

from aulos.base import ChainNotation
from aulos.base import Chord as BaseChord
from aulos.base import Definition
from aulos.base import Notation
from aulos.base import NotationError
from aulos.base import NotationTag
from aulos.base import Pitch as BasePitch
from aulos.base import PitchClass as BasePitchClass
from aulos.base import Scale as BaseScale
from aulos.base import Symbols
from aulos.base import Voicing as BaseVoicing
from aulos.pentatonic.templates import chords
from aulos.pentatonic.templates import scales


class PentatonicTag(NotationTag):
    """オクターブ内の完全5度の五文字連鎖という分類."""

    @classmethod
    def validate(cls, spec: Notation) -> None:
        """五文字の連鎖であることを検証する."""
        if spec.chain != ChainNotation(Fraction(2), Fraction(3, 2), 5):
            msg = "pentatonic notation needs the five-letter fifth chain"
            raise NotationError(msg)


notation = Notation[PentatonicTag](ChainNotation(Fraction(2), Fraction(3, 2), 5))
symbols = Symbols(("a", "b", "c", "d", "e"), "+", "~", 4, 0, 4)


class _Pentatonic(Definition[PentatonicTag], abstract=True):
    """五文字の記譜・表示規約を共有する、調律を束ねない中間定義."""

    notation = notation
    symbols = symbols
    tag = PentatonicTag


class PitchClass(_Pentatonic, BasePitchClass[PentatonicTag]):
    """c+などの音名から作る音高クラス."""


class Pitch(_Pentatonic, BasePitch[PentatonicTag]):
    """c+4などの音名から作る音高."""

    pitch_class_type = PitchClass


class Voicing(_Pentatonic, BaseVoicing[PentatonicTag]):
    """テンプレート名から作る音程列."""

    pitch_type = Pitch
    templates = chords


class Chord(_Pentatonic, BaseChord[PentatonicTag]):
    """五文字体系の積み重ねを表す和音."""

    pitch_type = Pitch
    voicing_type = Voicing
    templates = chords


class Scale(_Pentatonic, BaseScale[PentatonicTag]):
    """五文字体系の自然音階。anaturalではなくa naturalと表す."""

    pitch_type = Pitch
    chord_type = Chord
    templates = scales


__all__ = ["Chord", "PentatonicTag", "Pitch", "PitchClass", "Scale", "Voicing", "notation", "symbols"]
