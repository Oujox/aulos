"""音価を、一つの音符として書くための要素に分解する.

記号や文字列の規約は持たず、音符の種類・付点・連符という構造だけを扱う。
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from aulos.core.maths import strip_factor
from aulos.core.time import Duration


@dataclass(frozen=True, slots=True)
class NoteValue:
    """付点と連符を伴う一つの音符.

    ``base`` は付点も連符もない音符の音価で、全音符の2の冪倍。``dots`` は付点の数。
    ``division`` は連符の分割数で、1は連符なし、3は三連符を表す。連符は ``division`` 個で、
    それを超えない最大の2の冪の個数ぶんの長さを占める(三連符は3個で2個ぶん、五連符は5個で4個ぶん)。
    """

    base: Duration
    dots: int = 0
    division: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.base, Duration) or type(self.dots) is not int or type(self.division) is not int:
            msg = "a note value needs a Duration base and integer dots and division"
            raise TypeError(msg)
        value = Fraction(self.base.value)
        if value <= 0 or strip_factor(value.numerator, 2)[0] != 1 or strip_factor(value.denominator, 2)[0] != 1:
            msg = "the base of a note value must be a power of two of the whole note"
            raise ValueError(msg)
        if self.dots < 0 or self.division < 1 or self.division % 2 == 0:
            msg = "a note value needs nonnegative dots and an odd division"
            raise ValueError(msg)

    @classmethod
    def of(cls, duration: Duration) -> NoteValue | None:
        """正の音価を一つの音符に分解する。この形で書けず、タイなどで分ける必要があればNone.

        音価の分母に残る奇数を連符の分割数とし、連符を外した音価の分子に残る奇数が
        1, 3, 7, 15, ... であれば、その音符に付点を加えた形で書ける。
        """
        if not isinstance(duration, Duration):
            msg = "a note value is taken of a Duration"
            raise TypeError(msg)
        value = Fraction(duration.value)
        if value <= 0:
            msg = "only a positive duration is written as a note"
            raise ValueError(msg)
        division, _ = strip_factor(value.denominator, 2)
        written = value * division / _span(division)
        odd, _ = strip_factor(written.numerator, 2)
        if (odd + 1) & odd:
            return None
        dots = odd.bit_length() - 1
        return cls(Duration(written * 2**dots / odd), dots, division)

    @property
    def duration(self) -> Duration:
        """付点と連符を適用した実際の音価を返す."""
        dotted = self.base * (2 - Fraction(1, 2**self.dots))
        return dotted * Fraction(_span(self.division), self.division)


def _span(division: int) -> int:
    """連符 ``division`` 個が占める、付点も連符もない音符の個数を返す."""
    return 1 << (division.bit_length() - 1)
