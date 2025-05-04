from __future__ import annotations

import typing as t
from dataclasses import dataclass
from itertools import tee
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aulos._core.utils import Intervals  # pragma: no cover


def diff(iterable: t.Iterable[int]) -> t.Iterator[int]:
    a, b = tee(iterable)
    next(b, None)
    return (x[1] - x[0] for x in zip(a, b, strict=False))


@dataclass(init=False, frozen=True, slots=True)
class Positions(t.AbstractSet[int]):
    _positions: set[int]
    _pmax: int

    def __init__(self, iterable: t.Iterable[int], pmax: int) -> None:
        object.__setattr__(self, "_positions", set(iterable))
        object.__setattr__(self, "_pmax", pmax)
        self._positions.add(0)

    def to_intervals(self) -> Intervals:
        from aulos._core.utils import Intervals

        intervals = diff([*sorted(self._positions), self._pmax])
        return Intervals(intervals)

    def __iter__(self) -> t.Iterator[int]:
        return iter(sorted(self._positions))

    def __len__(self) -> int:
        return self._positions.__len__()

    def __contains__(self, item: object) -> bool:
        return self._positions.__contains__(item)
