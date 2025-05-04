from __future__ import annotations

import typing as t
from dataclasses import dataclass
from itertools import accumulate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aulos._core.utils import Positions  # pragma: no cover


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
        from aulos._core.utils import Positions

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
