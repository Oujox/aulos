import typing as t
from itertools import pairwise
from typing import TYPE_CHECKING

from aulos._core.utils import classproperty, rotated

from .scale import Scale

# type annotaion
if TYPE_CHECKING:
    from aulos._core.note import BaseKey, BasePitchClass


class DiatonicScale[KEY: BaseKey, PITCHCLASS: BasePitchClass](Scale[KEY, PITCHCLASS]):
    """
    Represents a diatonic scale, which is a musical scale consisting of seven distinct pitch classes.

    This class provides the foundational structure for creating and manipulating diatonic scales,
    allowing for the specification of intervals, key, and optional shifts in the scale's starting point.
    """

    def __init_subclass__(
        cls,
        *,
        intervals: t.Sequence[int],
        shift: int = 0,
        key: type[KEY],
    ) -> None:
        super().__init_subclass__(
            intervals=rotated(intervals, -shift),
            key=key,
        )


class NondiatonicScale[KEY: BaseKey, PITCHCLASS: BasePitchClass](
    Scale[KEY, PITCHCLASS],
):
    """
    Represents a nondiatonic scale, which extends a diatonic scale with additional intervals.

    This class allows for the creation and manipulation of scales that include extra notes beyond the
    traditional diatonic framework, providing flexibility in defining unique musical scales with
    extended harmonic possibilities.
    """

    _extensions: t.ClassVar[tuple[tuple[int, ...], ...]]
    _base: t.ClassVar[type[Scale]]

    def __init_subclass__(
        cls,
        *,
        extensions: t.Sequence[t.Sequence[int]],
        base: type[DiatonicScale],
        key: type[KEY],
    ) -> None:
        super().__init_subclass__(
            intervals=base.intervals,
            key=key,
        )
        cls._base = base
        cls._extensions = tuple(tuple(inner) for inner in extensions)

    @classproperty
    def intervals(self) -> tuple[int, ...]:
        return tuple(b - a for a, b in pairwise((*self.positions, sum(super().intervals))))

    @classproperty
    def positions(self) -> tuple[int, ...]:
        return tuple(pos + ext for pos, exts in zip(super().positions, self._extensions, strict=False) for ext in exts)

    @property
    def signatures(self) -> tuple[int, ...]:
        return tuple(sig + ext for sig, exts in zip(super().signatures, self._extensions, strict=False) for ext in exts)
