"""時間上の構造を直列と並列で組み立てる木.

長さは直列で和、並列で最大値になる。載せる値の型は問わず、音高や和音を置ける。
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import NamedTuple

from aulos.core.time import Duration
from aulos.core.time import Position
from aulos.core.time import rational

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterator
    from fractions import Fraction


class Placed[T](NamedTuple):
    """時刻に置かれた値."""

    start: Position
    duration: Duration
    value: T


class Part[T](ABC):
    """長さを持つ構造。``+`` で直列に、``|`` で並列に合成する."""

    __slots__ = ()

    @property
    @abstractmethod
    def duration(self) -> Duration:
        """構造全体の音価を返す."""

    @abstractmethod
    def stretch(self, factor: Fraction | int) -> Part[T]:
        """すべての音価を正の ``factor`` 倍した構造を返す."""

    @abstractmethod
    def map[U](self, function: Callable[[T], U]) -> Part[U]:
        """休みを除くすべての値に ``function`` を適用した構造を返す."""

    @abstractmethod
    def _place(self, start: Position) -> Iterator[Placed[T]]: ...

    def events(self, start: Position | None = None) -> tuple[Placed[T], ...]:
        """``start`` (省略時は原点)から始めたときの、休みを除く値を時刻順に返す."""
        return tuple(sorted(self._place(Position(0) if start is None else start), key=lambda placed: placed.start))

    def _serial(self) -> tuple[Part[T], ...]:
        return (self,)

    def _parallel(self) -> tuple[Part[T], ...]:
        return (self,)

    def __add__[U](self, other: Part[U]) -> Serial[T | U]:
        """``other`` を後ろに続けた構造を返す。値の型が異なる構造も合成できる."""
        if not isinstance(other, Part):
            return NotImplemented
        return Serial((*self._serial(), *other._serial()))

    def __or__[U](self, other: Part[U]) -> Parallel[T | U]:
        """``other`` と同時に始まる構造を返す。値の型が異なる構造も合成できる."""
        if not isinstance(other, Part):
            return NotImplemented
        return Parallel((*self._parallel(), *other._parallel()))


def _factor(factor: Fraction | int) -> Fraction:
    value = rational(factor, "a stretch factor")
    if value <= 0:
        msg = "a stretch factor must be positive"
        raise ValueError(msg)
    return value


def _parts[T](parts: tuple[Part[T], ...]) -> tuple[Part[T], ...]:
    values = tuple(parts)
    if any(not isinstance(part, Part) for part in values):
        msg = "a structure is composed of Part objects"
        raise TypeError(msg)
    return values


@dataclass(frozen=True, slots=True)
class Event[T](Part[T]):
    """音価 ``length`` の間続く一つの値。値がNoneなら休み."""

    length: Duration
    value: T | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.length, Duration):
            msg = "an event needs a Duration"
            raise TypeError(msg)
        if self.length < Duration(0):
            msg = "an event cannot have a negative duration"
            raise ValueError(msg)

    @property
    def duration(self) -> Duration:
        """値が続く音価を返す."""
        return self.length

    def stretch(self, factor: Fraction | int) -> Event[T]:
        """音価を正の ``factor`` 倍した値を返す."""
        return Event(self.length * _factor(factor), self.value)

    def map[U](self, function: Callable[[T], U]) -> Event[U]:
        """休みでなければ値に ``function`` を適用する."""
        return Event(self.length, None if self.value is None else function(self.value))

    def _place(self, start: Position) -> Iterator[Placed[T]]:
        if self.value is not None:
            yield Placed(start, self.length, self.value)


@dataclass(frozen=True, slots=True)
class Serial[T](Part[T]):
    """順に続く構造の列。長さは各部分の和."""

    parts: tuple[Part[T], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "parts", _parts(self.parts))

    @property
    def duration(self) -> Duration:
        """各部分の音価の和を返す."""
        return sum((part.duration for part in self.parts), Duration(0))

    def stretch(self, factor: Fraction | int) -> Serial[T]:
        """各部分の音価を正の ``factor`` 倍した列を返す."""
        return Serial(tuple(part.stretch(factor) for part in self.parts))

    def map[U](self, function: Callable[[T], U]) -> Serial[U]:
        """各部分の値に ``function`` を適用した列を返す."""
        return Serial(tuple(part.map(function) for part in self.parts))

    def _place(self, start: Position) -> Iterator[Placed[T]]:
        for part in self.parts:
            yield from part._place(start)
            start += part.duration

    def _serial(self) -> tuple[Part[T], ...]:
        return self.parts


@dataclass(frozen=True, slots=True)
class Parallel[T](Part[T]):
    """同時に始まる構造の組。長さは最も長い部分に等しい."""

    parts: tuple[Part[T], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "parts", _parts(self.parts))

    @property
    def duration(self) -> Duration:
        """最も長い部分の音価を返す."""
        return max((part.duration for part in self.parts), default=Duration(0))

    def stretch(self, factor: Fraction | int) -> Parallel[T]:
        """各部分の音価を正の ``factor`` 倍した組を返す."""
        return Parallel(tuple(part.stretch(factor) for part in self.parts))

    def map[U](self, function: Callable[[T], U]) -> Parallel[U]:
        """各部分の値に ``function`` を適用した組を返す."""
        return Parallel(tuple(part.map(function) for part in self.parts))

    def _place(self, start: Position) -> Iterator[Placed[T]]:
        for part in self.parts:
            yield from part._place(start)

    def _parallel(self) -> tuple[Part[T], ...]:
        return self.parts
