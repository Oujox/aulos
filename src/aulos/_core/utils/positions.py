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
class Positions(t.Sequence[int]):
    _positions: tuple[int]
    _limit: int

    def __init__(self, iterable: t.Iterable[int], limit: int) -> None:
        positions = set(iterable)
        positions.add(0)
        object.__setattr__(self, "_positions", tuple(sorted(positions)))
        object.__setattr__(self, "_limit", limit)

    @property
    def limit(self) -> int:
        return self._limit

    def to_intervals(self) -> Intervals:
        from aulos._core.utils import Intervals

        intervals = diff([*self._positions, self._limit])
        return Intervals(intervals)

    def __iter__(self) -> t.Iterator[int]:
        return self._positions.__iter__()

    def __len__(self) -> int:
        return self._positions.__len__()

    def __contains__(self, key: object) -> bool:
        return self._positions.__contains__(key)

    @t.overload
    def __getitem__(self, index: int) -> int: ...
    @t.overload
    def __getitem__(self, index: slice) -> tuple[int, ...]: ...
    def __getitem__(self, index: int | slice) -> int | tuple[int, ...]:
        return self._positions.__getitem__(index)
