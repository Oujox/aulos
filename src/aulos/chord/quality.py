from __future__ import annotations

import typing as t
from dataclasses import dataclass

from aulos._core.utils import index

if t.TYPE_CHECKING:
    from aulos._core.utils import Intervals, Positions


class _OptionalQualityProperty(t.TypedDict, total=False):
    areas: tuple[str, ...]


class _RequiredQualityProperty(t.TypedDict, total=True):
    name: str
    positions: tuple[int, ...]


class QualityProperty(_RequiredQualityProperty, _OptionalQualityProperty):
    """ """


def on_candidates(intervals: Intervals) -> tuple[int, ...]:
    return tuple(sum(intervals[inv:]) for inv in range(len(intervals)))


@dataclass(init=False, frozen=True, slots=False)
class Quality:
    name: str
    intervals: Intervals
    inversion: int

    def __init__(self, *, name: str, positions: Positions, inversion: int | None = None) -> None:
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "intervals", positions.to_intervals())
        object.__setattr__(self, "inversion", inversion or 0)

    @property
    def positions(self) -> Positions:
        return self.intervals.to_positions()

    @property
    def on(self) -> int:
        return on_candidates(self.intervals)[self.inversion]

    def inverse(self, inversion: int) -> Quality:
        intervals = self.intervals.left(inversion)
        return Quality(
            name=self.name,
            positions=intervals.to_positions(),
            inversion=inversion % len(intervals),
        )

    def inverse_from_on(self, on: int) -> Quality:
        return self.inverse(index(on_candidates(self.intervals), on) or 0)
