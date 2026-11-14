"""拍子やテンポに依存しない記譜上の時間.

音価は全音符を1とする有理数で、加算について群を成す。時刻は音価を加えて移動する点で、
時刻同士は加算できない。秒への評価は ``Tempo`` が与えて初めて決まる。
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import overload

from aulos.core.maths import factorize


def rational(value: object, name: str) -> Fraction:
    """整数またはFractionをFractionにそろえ、boolや浮動小数点数を拒否する."""
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        msg = f"{name} must be an integer or a Fraction"
        raise TypeError(msg)
    return Fraction(value)


@dataclass(frozen=True, slots=True, order=True)
class Duration:
    """全音符を1とする符号付きの音価。四分音符は ``Duration(Fraction(1, 4))``.

    加算と整数・有理数倍ができ、音価同士の除算は比を返す。負の値は時刻の差として現れる。
    """

    value: Fraction | int

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", rational(self.value, "a duration"))

    @property
    def primes(self) -> frozenset[int]:
        """全音符の分割に使う素数を返す。二分割だけなら2、三連符を含めば3が加わる."""
        return frozenset(factorize(Fraction(self.value).denominator))

    def __add__(self, other: Duration) -> Duration:
        """二つの音価の和を返す."""
        if not isinstance(other, Duration):
            return NotImplemented
        return Duration(self.value + other.value)

    def __neg__(self) -> Duration:
        """符号を反転した音価を返す."""
        return Duration(-self.value)

    def __sub__(self, other: Duration) -> Duration:
        """二つの音価の差を返す."""
        if not isinstance(other, Duration):
            return NotImplemented
        return self + (-other)

    def __mul__(self, factor: Fraction | int) -> Duration:
        """整数または有理数倍した音価を返す."""
        if isinstance(factor, bool) or not isinstance(factor, (int, Fraction)):
            return NotImplemented
        return Duration(self.value * factor)

    __rmul__ = __mul__

    @overload
    def __truediv__(self, other: Duration) -> Fraction: ...

    @overload
    def __truediv__(self, other: Fraction | int) -> Duration: ...

    def __truediv__(self, other: Duration | Fraction | int) -> Fraction | Duration:
        """音価で割れば比を、整数や有理数で割れば音価を返す."""
        if isinstance(other, Duration):
            return Fraction(self.value) / other.value
        if isinstance(other, bool) or not isinstance(other, (int, Fraction)):
            return NotImplemented
        return Duration(Fraction(self.value) / other)


@dataclass(frozen=True, slots=True, order=True)
class Position:
    """原点からの音価で表す記譜上の時刻."""

    value: Fraction | int

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", rational(self.value, "a position"))

    def __add__(self, duration: Duration) -> Position:
        """音価だけ進めた時刻を返す."""
        if not isinstance(duration, Duration):
            return NotImplemented
        return Position(self.value + duration.value)

    @overload
    def __sub__(self, other: Position) -> Duration: ...

    @overload
    def __sub__(self, other: Duration) -> Position: ...

    def __sub__(self, other: Position | Duration) -> Duration | Position:
        """時刻との差の音価、または音価だけ戻した時刻を返す."""
        if isinstance(other, Duration):
            return Position(self.value - other.value)
        if isinstance(other, Position):
            return Duration(self.value - other.value)
        return NotImplemented
