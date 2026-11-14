"""周期の中の打点の集合としてのリズム型.

パルスは巡回群を成し、回転はその群の作用になる。生成元の連鎖から作る型は、
音高側の連鎖記譜と同じ構造を持つ。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from aulos.core.errors import RhythmError

if TYPE_CHECKING:
    from aulos.core.time import Duration


def _count(value: object, name: str) -> int:
    if type(value) is not int:
        msg = f"{name} must be an integer"
        raise TypeError(msg)
    return value


@dataclass(frozen=True, slots=True)
class Cycle:
    """``size`` 個のパルスからなる周期と、その中の打点.

    ``onsets`` は0以上 ``size`` 未満のパルス番号で、重複を除いて昇順に保持する。
    """

    size: int
    onsets: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        onsets = tuple(_count(onset, "an onset") for onset in self.onsets)
        if _count(self.size, "a cycle size") <= 0:
            msg = "a cycle needs at least one pulse"
            raise ValueError(msg)
        if any(not 0 <= onset < self.size for onset in onsets):
            msg = f"onsets must lie within the {self.size} pulses"
            raise ValueError(msg)
        object.__setattr__(self, "onsets", tuple(sorted(set(onsets))))

    @classmethod
    def generated(cls, size: int, generator: int, count: int) -> Cycle:
        """パルス0から ``generator`` ずつ進めた最初の ``count`` 個を打点とする型を返す.

        ``count`` 個の中で同じパルスに戻る組み合わせは拒否する。
        """
        if _count(count, "an onset count") < 0:
            msg = "an onset count must not be negative"
            raise ValueError(msg)
        empty = cls(size)
        onsets = {(_count(generator, "a generator") * link) % empty.size for link in range(count)}
        if len(onsets) != count:
            msg = f"{generator} returns to an onset within {count} links of {size} pulses"
            raise RhythmError(msg)
        return cls(size, tuple(onsets))

    @classmethod
    def euclidean(cls, size: int, count: int) -> Cycle:
        """``count`` 個の打点を ``size`` 個のパルスへ最も均等に配置した型を返す."""
        if not 0 <= _count(count, "an onset count") <= _count(size, "a cycle size"):
            msg = f"{count} onsets do not fit {size} pulses"
            raise ValueError(msg)
        return cls(size, tuple((index * size) // count for index in range(count)))

    @property
    def steps(self) -> tuple[int, ...]:
        """各打点から次の打点までのパルス数を返す。和は ``size`` に等しい."""
        if not self.onsets:
            return ()
        later = (*self.onsets[1:], self.onsets[0] + self.size)
        return tuple(high - low for low, high in zip(self.onsets, later, strict=True))

    @property
    def is_euclidean(self) -> bool:
        """最も均等な配置を回転した型か判定する."""
        even = Cycle.euclidean(self.size, len(self.onsets))
        return any(self.rotate(pulses) == even for pulses in range(self.size))

    def durations(self, pulse: Duration) -> tuple[Duration, ...]:
        """パルスの音価 ``pulse`` から、各打点の次の打点までの音価を返す."""
        return tuple(pulse * step for step in self.steps)

    def rotate(self, pulses: int) -> Cycle:
        """全打点を ``pulses`` だけ遅らせた型を返す。周期をまたぐ打点は先頭へ回る."""
        return Cycle(self.size, tuple((onset + _count(pulses, "a rotation")) % self.size for onset in self.onsets))

    def mode(self, index: int) -> Cycle:
        """``index`` 番目の打点が周期の頭に来るよう回転した型を返す."""
        if not self.onsets:
            msg = "a cycle without onsets has no mode"
            raise RhythmError(msg)
        return self.rotate(-self.onsets[_count(index, "a mode index") % len(self.onsets)])

    def complement(self) -> Cycle:
        """打点と休みを入れ替えた型を返す."""
        return Cycle(self.size, tuple(pulse for pulse in range(self.size) if pulse not in self.onsets))

    def refine(self, factor: int) -> Cycle:
        """周期の長さを保ったまま、各パルスを ``factor`` 個に分割した型を返す."""
        if _count(factor, "a refinement") <= 0:
            msg = "a refinement must be positive"
            raise ValueError(msg)
        return Cycle(self.size * factor, tuple(onset * factor for onset in self.onsets))

    def repeat(self, times: int) -> Cycle:
        """周期を ``times`` 回繰り返して一つの周期とした型を返す."""
        if _count(times, "a repetition") <= 0:
            msg = "a repetition must be positive"
            raise ValueError(msg)
        return Cycle(
            self.size * times, tuple(turn * self.size + onset for turn in range(times) for onset in self.onsets)
        )

    def _aligned(self, other: Cycle) -> tuple[Cycle, Cycle]:
        """二つの型を、同じ長さの周期を分割する共通のパルスにそろえる."""
        size = math.lcm(self.size, other.size)
        return self.refine(size // self.size), other.refine(size // other.size)

    def __or__(self, other: Cycle) -> Cycle:
        """同じ長さの周期に重ねた、どちらかにある打点の型を返す."""
        if not isinstance(other, Cycle):
            return NotImplemented
        first, second = self._aligned(other)
        return Cycle(first.size, first.onsets + second.onsets)

    def __and__(self, other: Cycle) -> Cycle:
        """同じ長さの周期に重ねた、両方にある打点の型を返す."""
        if not isinstance(other, Cycle):
            return NotImplemented
        first, second = self._aligned(other)
        return Cycle(first.size, tuple(set(first.onsets) & set(second.onsets)))
