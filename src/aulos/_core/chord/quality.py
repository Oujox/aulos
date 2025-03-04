from __future__ import annotations

import typing as t
from dataclasses import dataclass

from aulos._core.utils import index

if t.TYPE_CHECKING:
    from aulos._core.utils import Intervals, Positions  # pragma: no cover


class _OptionalQualityProperty(t.TypedDict, total=False):
    areas: tuple[str, ...]


class _RequiredQualityProperty(t.TypedDict, total=True):
    name: str
    positions: tuple[int, ...]


class QualityProperty(_RequiredQualityProperty, _OptionalQualityProperty):
    """ """


@dataclass(init=False, frozen=True, slots=False)
class Quality:
    name: str
    intervals: Intervals
    inversion: int
    base: int

    def __init__(
        self, *, name: str, positions: Positions, inversion: int | None = None, base: int | None = None
    ) -> None:
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "intervals", positions.to_intervals())
        object.__setattr__(self, "inversion", inversion or 0)
        object.__setattr__(self, "base", base or 0)

        if (base_inversion := index(self.base_candidates, base)) is not None:
            intervals = self.intervals.left(base_inversion)
            object.__setattr__(self, "intervals", intervals)
            object.__setattr__(self, "inversion", base_inversion % len(intervals))
            object.__setattr__(self, "base", 0)

    @property
    def positions(self) -> Positions:
        return self.intervals.to_positions()

    @property
    def root(self) -> int:
        return self.root_candidates[self.inversion]

    @property
    def root_candidates(self) -> tuple[int, ...]:
        return tuple(sum(self.intervals[inv:]) for inv in range(len(self.intervals), 0, -1))

    @property
    def base_candidates(self) -> tuple[int, ...]:
        return tuple(-sum(self.intervals[inv:]) for inv in range(len(self.intervals)))

    def inverse(self, inversion: int) -> Quality:
        intervals = self.intervals.left(inversion)
        return Quality(
            name=self.name,
            positions=intervals.to_positions(),
            inversion=(self.inversion + inversion) % len(intervals),
            base=self.base,
        )

    def from_base(self, base: int) -> Quality:
        return Quality(name=self.name, positions=self.positions, base=base)

    def is_inverted(self) -> bool:
        return self.inversion != 0

    def is_onchord(self) -> bool:
        return self.base != 0
