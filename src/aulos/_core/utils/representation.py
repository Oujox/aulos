from __future__ import annotations

import typing as t
from dataclasses import dataclass
from itertools import accumulate, tee


def diff(iterable: t.Iterable[int]) -> t.Iterator[int]:
    a, b = tee(iterable)
    next(b, None)
    return (x[1] - x[0] for x in zip(a, b, strict=False))


@dataclass(init=False, frozen=True, slots=True)
class Intervals(t.Sequence[int]):
    _intervals: tuple[int]

    def __init__(self, iterable: t.Iterable[int]) -> None:
        object.__setattr__(self, "_intervals", tuple(iterable))

    def left(self, num: int = 1) -> Intervals:
        num %= len(self)
        return Intervals(self._intervals[num:] + self._intervals[:num])

    def right(self, num: int = 1) -> Intervals:
        num %= len(self)
        return Intervals(self._intervals[-num:] + self._intervals[:-num])

    def to_positions(self) -> Positions:
        return Positions(accumulate(self._intervals[:-1]), sum(self._intervals))

    def __iter__(self) -> t.Iterator[int]:
        return self._intervals.__iter__()

    def __len__(self) -> int:
        return self._intervals.__len__()

    @t.overload
    def __getitem__(self, index: int) -> int: ...
    @t.overload
    def __getitem__(self, index: slice) -> tuple[int, ...]: ...
    def __getitem__(self, index: int | slice) -> int | tuple[int, ...]:
        return self._intervals.__getitem__(index)


@dataclass(init=False, frozen=True, slots=True)
class Positions(t.AbstractSet[int]):
    _positions: set[int]
    _pmax: int

    def __init__(self, iterable: t.Iterable[int], pmax: int) -> None:
        object.__setattr__(self, "_positions", set(iterable))
        object.__setattr__(self, "_pmax", pmax)
        self._positions.add(0)

    def to_intervals(self) -> Intervals:
        intervals = diff([*sorted(self._positions), self._pmax])
        return Intervals(intervals)

    def __iter__(self) -> t.Iterator[int]:
        return iter(sorted(self._positions))

    def __len__(self) -> int:
        return self._positions.__len__()

    def __contains__(self, item: object) -> bool:
        return self._positions.__contains__(item)
