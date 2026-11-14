"""記譜体系に結び付いた内部の音高値。公開クラスはこれを包む."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import overload

from aulos.core.chain import ChainInterval
from aulos.core.chain import Spelling
from aulos.core.notation import Interval
from aulos.core.notation import Notation

if TYPE_CHECKING:
    from fractions import Fraction


@dataclass(frozen=True, slots=True)
class PitchClassValue[N]:
    """体系・文字位置・変化量・コンマからなる不変の内部音高クラス."""

    notation: Notation[N]
    letter: int
    alteration: int = 0
    commas: tuple[tuple[int, int], ...] = ()

    def __post_init__(self) -> None:
        if type(self.letter) is not int or type(self.alteration) is not int:
            msg = "letter and alteration must be integers"
            raise TypeError(msg)
        if not 0 <= self.letter < self.notation.chain.size:
            msg = "letter is outside the notation"
            raise ValueError(msg)
        object.__setattr__(self, "commas", self.notation._normalize(self.commas))

    def at(self, register: int) -> PitchValue[N]:
        """指定した内部音域に音高クラスを置く."""
        return PitchValue(self, register)

    def __add__(self, interval: Interval[N]) -> PitchClassValue[N]:
        if not isinstance(interval, Interval):
            return NotImplemented
        return (self.at(0) + interval).pitch_class

    def __sub__(self, interval: Interval[N]) -> PitchClassValue[N]:
        if not isinstance(interval, Interval):
            return NotImplemented
        return self + (-interval)


@dataclass(frozen=True, slots=True)
class PitchValue[N]:
    """内部音高クラスと、原点から数えた整数の音域."""

    pitch_class: PitchClassValue[N]
    register: int = 0

    def __post_init__(self) -> None:
        if type(self.register) is not int:
            msg = "register must be an integer"
            raise TypeError(msg)

    @classmethod
    def of(cls, notation: Notation[N], spelling: Spelling, commas: tuple[tuple[int, int], ...] = ()) -> PitchValue[N]:
        """綴りとコンマ数を記譜体系の音高値にする."""
        return cls(PitchClassValue(notation, spelling.letter, spelling.alteration, commas), spelling.register)

    @property
    def notation(self) -> Notation[N]:
        """音高クラスに束ねた記譜体系を返す."""
        return self.pitch_class.notation

    @property
    def spelling(self) -> Spelling:
        """コンマを除いた連鎖上の綴りを返す."""
        return Spelling(self.pitch_class.letter, self.pitch_class.alteration, self.register)

    def interval(self) -> Interval[N]:
        """体系の原点からの変位を返す."""
        point = self.notation.chain._pitch(self.spelling)
        return Interval(self.notation, ChainInterval(point.generators, point.periods), self.pitch_class.commas)

    def ratio(self) -> Fraction:
        """記譜体系の原点に対する正確な比を返す."""
        return self.interval().ratio()

    def __add__(self, interval: Interval[N]) -> PitchValue[N]:
        if not isinstance(interval, Interval):
            return NotImplemented
        moved = self.interval() + interval
        # 音程と連鎖音高は同じ座標対を持つため、綴りへの変換を共用できる。
        return PitchValue.of(self.notation, self.notation.chain._spell(moved.chain), moved.commas)

    @overload
    def __sub__(self, other: PitchValue[N]) -> Interval[N]: ...

    @overload
    def __sub__(self, other: Interval[N]) -> PitchValue[N]: ...

    def __sub__(self, other: PitchValue[N] | Interval[N]) -> Interval[N] | PitchValue[N]:
        if isinstance(other, Interval):
            return self + (-other)
        if isinstance(other, PitchValue):
            return self.interval() - other.interval()
        return NotImplemented
