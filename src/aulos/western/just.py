"""西洋式七文字記譜の5リミット純正律.

短7度を9/5とするなどの比の選択は規約の一例であり、コード記号から一意には決まらない。
"""

from fractions import Fraction

from aulos.base import ChainInterval
from aulos.base import Chord as BaseChord
from aulos.base import Comma
from aulos.base import CommaSymbols
from aulos.base import Definition
from aulos.base import Notation
from aulos.base import Pitch as BasePitch
from aulos.base import PitchClass as BasePitchClass
from aulos.base import Realization
from aulos.base import Scale as BaseScale
from aulos.base import Symbols
from aulos.base import Tuning
from aulos.base import Voicing as BaseVoicing
from aulos.western import WesternTag
from aulos.western import chain
from aulos.western import letters
from aulos.western.templates import chords
from aulos.western.templates import scales

notation = Notation[WesternTag](chain, (Comma(5, Fraction(81, 80)),))
symbols = Symbols(letters, "#", "b", 4, 4, 4, (CommaSymbols(5, "↑", "↓"),))
tuning = Tuning.just((2, 3, 5))
# 複音程も同じ比の周期倍で定義する。
realization = Realization(
    tuple(
        (ChainInterval(generators, periods + turns), ratio * 2**turns)
        for generators, periods, ratio in (
            (-5, 3, Fraction(16, 15)),
            (2, -1, Fraction(9, 8)),
            (9, -5, Fraction(75, 64)),
            (-3, 2, Fraction(6, 5)),
            (4, -2, Fraction(5, 4)),
            (-8, 5, Fraction(32, 25)),
            (-1, 1, Fraction(4, 3)),
            (6, -3, Fraction(45, 32)),
            (-6, 4, Fraction(64, 45)),
            (1, 0, Fraction(3, 2)),
            (8, -4, Fraction(25, 16)),
            (-4, 3, Fraction(8, 5)),
            (3, -1, Fraction(5, 3)),
            (-2, 2, Fraction(9, 5)),
            (5, -2, Fraction(15, 8)),
            (-9, 6, Fraction(128, 75)),
        )
        for turns in (0, 1)
    )
)


class _Just(Definition[WesternTag], abstract=True):
    """七文字とコンマの記譜・表示規約、および純正律を共有する中間定義."""

    notation = notation
    symbols = symbols
    tag = WesternTag
    tuning = tuning


class PitchClass(_Just, BasePitchClass[WesternTag]):
    """C#↑などの音名から作る音高クラス."""


class Pitch(_Just, BasePitch[WesternTag]):
    """C#4↑などの音名から作る音高."""

    pitch_class_type = PitchClass


class Voicing(_Just, BaseVoicing[WesternTag]):
    """5リミット規約でテンプレート名を解釈する音程列."""

    pitch_type = Pitch
    templates = chords
    realization = realization


class Chord(_Just, BaseChord[WesternTag]):
    """5リミット規約でコード記号を解釈する和音."""

    pitch_type = Pitch
    voicing_type = Voicing
    templates = chords
    realization = realization


class Scale(_Just, BaseScale[WesternTag]):
    """5リミット規約で音階名を解釈する音階."""

    pitch_type = Pitch
    chord_type = Chord
    templates = scales
    realization = realization


__all__ = ["Chord", "Pitch", "PitchClass", "Scale", "Voicing", "notation", "realization", "symbols", "tuning"]
