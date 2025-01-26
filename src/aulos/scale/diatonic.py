import typing as t
from itertools import pairwise

from .._core.utils import classproperty, rotated
from ..note import BaseKey, BasePitchClass
from .scale import Scale


class DiatonicScale[KEY: BaseKey, PITCHCLASS: BasePitchClass](Scale[KEY, PITCHCLASS]):
    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is DiatonicScale:
            raise TypeError("DiatonicScale cannot be instantiated directly.")
        return super().__new__(cls)

    def __init_subclass__(
        cls,
        *,
        intervals: t.Sequence[int],
        shift: int = 0,
        key: type[KEY],
        pitchclass: type[PITCHCLASS],
        **kwargs,
    ) -> None:
        super().__init_subclass__(
            intervals=rotated(intervals, -shift),
            key=key,
            pitchclass=pitchclass,
            **kwargs,
        )


class NondiatonicScale[KEY: BaseKey, PITCHCLASS: BasePitchClass](
    Scale[KEY, PITCHCLASS]
):
    _extensions: t.ClassVar[tuple[tuple[int, ...], ...]]
    _base: t.ClassVar[type[Scale]]

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is NondiatonicScale:
            raise TypeError("NondiatonicScale cannot be instantiated directly.")
        return super().__new__(cls)

    def __init_subclass__(
        cls,
        *,
        extensions: t.Sequence[t.Sequence[int]],
        base: type[DiatonicScale],
        key: type[KEY],
        pitchclass: type[PITCHCLASS],
        **kwargs,
    ) -> None:
        super().__init_subclass__(
            intervals=base.intervals,
            key=key,
            pitchclass=pitchclass,
            **kwargs,
        )
        cls._base = base
        cls._extensions = tuple(tuple(inner) for inner in extensions)

    @classproperty
    def intervals(cls) -> tuple[int, ...]:
        intervals = tuple(
            b - a for a, b in pairwise(cls.positions + (sum(super().intervals),))
        )
        return intervals

    @classproperty
    def positions(cls) -> tuple[int, ...]:
        positions = tuple(
            pos + ext
            for pos, exts in zip(super().positions, cls._extensions)
            for ext in exts
        )
        return positions

    @property
    def signatures(self) -> tuple[int, ...]:
        signatures = tuple(
            sig + ext
            for sig, exts in zip(super().signatures, self._extensions)
            for ext in exts
        )
        return signatures
